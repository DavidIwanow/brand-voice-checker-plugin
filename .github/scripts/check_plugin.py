#!/usr/bin/env python3
"""Release checks for the Brand Voice Checker plugin.

Standard library only. Run from the repository root:

    python .github/scripts/check_plugin.py            # offline checks
    python .github/scripts/check_plugin.py --online   # also checks every URL and the MCP endpoint
    python .github/scripts/check_plugin.py --base-ref origin/main   # also requires a version bump

Exits 1 if any check fails.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
MCP_JSON = ROOT / ".mcp.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"
SKILLS_DIR = ROOT / "skills"

# Paths whose change ships a new plugin version to users.
RELEASE_PATHS = (".claude-plugin/", ".mcp.json", "skills/")

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOOL_NAME = re.compile(r"`([a-z]+(?:_[a-z]+)+)`")
RULE_COUNT = re.compile(r"(\d+)\s+(?:advertising[- ]claims\s+|claims\s+)rules", re.I)
URL = re.compile(r"https?://[^\s)<>\"'`]+")

failures: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  FAIL  {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"  WARN  {msg}")


def ok(msg: str) -> None:
    print(f"  ok    {msg}")


def load_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{path.relative_to(ROOT)} is missing")
        return None
    except json.JSONDecodeError as e:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {e}")
        return None
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must be a JSON object")
        return None
    ok(f"{path.relative_to(ROOT)} is valid JSON")
    return data


# ---------------------------------------------------------------- manifest
def check_manifest(manifest: dict) -> None:
    print("\nplugin.json")
    for field in ("name", "description", "version", "author", "license"):
        if not manifest.get(field):
            fail(f"plugin.json: '{field}' is missing or empty")
    name = manifest.get("name", "")
    if name and not SKILL_NAME.match(name):
        fail(f"plugin.json: name '{name}' must be lowercase kebab-case")
    version = manifest.get("version", "")
    if version and not SEMVER.match(version):
        fail(f"plugin.json: version '{version}' is not semver (x.y.z)")
    elif version:
        ok(f"version {version}")
    author = manifest.get("author")
    if isinstance(author, dict) and not author.get("name"):
        fail("plugin.json: author.name is missing")
    for key, value in manifest.items():
        if key.lower().endswith("url") or key in ("homepage", "repository"):
            if not isinstance(value, str) or not value.startswith("https://"):
                fail(f"plugin.json: '{key}' must be an https:// URL, got {value!r}")
    icon = manifest.get("icon")
    if icon:
        check_icon(ROOT / icon)
    if manifest.get("license") and not (ROOT / "LICENSE").exists():
        fail("plugin.json names a license but LICENSE is missing")


def check_icon(path: Path) -> None:
    if not path.exists():
        fail(f"icon {path.relative_to(ROOT)} does not exist")
        return
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"icon {path.relative_to(ROOT)} is not a PNG file")
        return
    width, height = struct.unpack(">II", head[16:24])
    if width != height:
        fail(f"icon must be square, is {width}x{height}")
    elif width < 256:
        fail(f"icon is {width}x{height}; use at least 256x256")
    else:
        ok(f"icon is a {width}x{height} PNG")
    size_kb = path.stat().st_size / 1024
    if size_kb > 1024:
        warn(f"icon is {size_kb:.0f} KB; keep it under 1 MB")


# ---------------------------------------------------------------- marketplace
def check_marketplace(manifest: dict, market: dict) -> None:
    print("\nmarketplace.json")
    mname = market.get("name", "")
    if not SKILL_NAME.match(mname or "-"):
        fail(f"marketplace.json: name '{mname}' must be lowercase kebab-case")
    if not isinstance(market.get("owner"), dict) or not market["owner"].get("name"):
        fail("marketplace.json: owner.name is missing")
    plugins = market.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("marketplace.json: 'plugins' must be a non-empty list")
        return
    names = [p.get("name") for p in plugins if isinstance(p, dict)]
    if len(names) != len(set(names)):
        fail("marketplace.json: plugin names must be unique")
    entry = next((p for p in plugins if isinstance(p, dict) and p.get("name") == manifest.get("name")), None)
    if entry is None:
        fail(f"marketplace.json does not list the plugin '{manifest.get('name')}'")
        return
    if entry.get("source") not in ("./", "."):
        fail(f"marketplace.json: '{entry['name']}' source should be './' (this repo), got {entry.get('source')!r}")
    # Fields that appear in both files must not drift apart.
    for field in ("version", "description", "license", "homepage", "repository"):
        if field in entry and entry[field] != manifest.get(field):
            fail(f"marketplace.json: {field} {entry[field]!r} differs from plugin.json {manifest.get(field)!r}")
    if not any("marketplace.json" in f for f in failures):
        ok(f"marketplace '{mname}' lists '{entry['name']}' {entry.get('version', '')} in step with plugin.json")


# ---------------------------------------------------------------- .mcp.json
def check_mcp(mcp: dict) -> list[str]:
    print("\n.mcp.json")
    servers = mcp.get("mcpServers")
    urls: list[str] = []
    if not isinstance(servers, dict) or not servers:
        fail(".mcp.json: 'mcpServers' must be a non-empty object")
        return urls
    for sname, cfg in servers.items():
        if not isinstance(cfg, dict):
            fail(f".mcp.json: server '{sname}' must be an object")
            continue
        stype = cfg.get("type")
        if stype in ("http", "sse"):
            url = cfg.get("url", "")
            if not url.startswith("https://"):
                fail(f".mcp.json: server '{sname}' url must be https://, got {url!r}")
            else:
                ok(f"server '{sname}' -> {url}")
                urls.append(url)
            if "headers" in cfg and any(
                re.search(r"(bearer|token|key|secret)", str(v), re.I) for v in cfg["headers"].values()
            ):
                fail(f".mcp.json: server '{sname}' has what looks like a credential in headers")
        elif stype == "stdio" or "command" in cfg:
            ok(f"server '{sname}' runs a local command")
        else:
            fail(f".mcp.json: server '{sname}' has unknown type {stype!r}")
    return urls


# ---------------------------------------------------------------- skills
def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith((" ", "\t", "#")):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            return None
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def check_skills() -> dict[str, str]:
    print("\nskills")
    texts: dict[str, str] = {}
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        fail("no skills/*/SKILL.md found")
    for path in skill_files:
        rel = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8")
        texts[rel] = text
        if "\r\n" in text:
            fail(f"{rel}: uses CRLF line endings; use LF")
            text = text.replace("\r\n", "\n")
        fm = parse_frontmatter(text)
        if fm is None:
            fail(f"{rel}: missing or malformed YAML front matter")
            continue
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if name != path.parent.name:
            fail(f"{rel}: front matter name '{name}' must match folder '{path.parent.name}'")
        if not SKILL_NAME.match(name or "-"):
            fail(f"{rel}: name '{name}' must be lowercase kebab-case")
        if not desc:
            fail(f"{rel}: description is empty")
        elif len(desc) > 1024:
            fail(f"{rel}: description is {len(desc)} chars; max 1024")
        if not any(rel in f for f in failures):
            ok(f"{rel}: front matter ok ({len(desc)}-char description)")
        lines = text.count("\n")
        if lines > 500:
            warn(f"{rel}: {lines} lines; skills over 500 lines load slowly")
    return texts


# ---------------------------------------------------------------- consistency
def readme_costs(readme: str) -> dict[str, str]:
    costs: dict[str, str] = {}
    for line in readme.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2 or not TOOL_NAME.search(cells[0]):
            continue
        for tool in TOOL_NAME.findall(cells[0]):
            costs[tool] = normalise_cost(cells[1])
    return costs


def skill_costs(skill: str) -> dict[str, str]:
    costs: dict[str, str] = {}
    m = re.search(r"^## Costs.*?\n(.*?)(?=^## |\Z)", skill, re.S | re.M)
    if not m:
        return costs
    # Join wrapped bullet lines, then read "- <cost>: `tool`, `tool`".
    bullets = re.split(r"\n- ", "\n" + m.group(1))
    for bullet in bullets:
        bullet = " ".join(bullet.split())
        bullet = re.sub(r"\([^)]*\)", "", bullet)  # drop notes such as "(the `max_chars` requested)"
        label, sep, rest = bullet.partition(":")
        if not sep:
            continue
        for tool in TOOL_NAME.findall(rest):
            costs[tool] = normalise_cost(label)
    return costs


def normalise_cost(text: str) -> str:
    t = text.lower()
    if "free" in t:
        return "free"
    if "per 2,000" in t or "per 2000" in t:
        return "1 per 2000 chars"
    if re.search(r"\b1 credit\b", t):
        return "1 credit"
    return t.strip()


def check_consistency(manifest: dict, skill_texts: dict[str, str], mcp_urls: list[str]) -> None:
    print("\nconsistency")
    readme = README.read_text(encoding="utf-8") if README.exists() else ""
    if not readme:
        fail("README.md is missing or empty")

    # Tool list and prices must match between README and the skill.
    rc = readme_costs(readme)
    sc: dict[str, str] = {}
    for text in skill_texts.values():
        sc.update(skill_costs(text))
    if not rc:
        fail("README.md: no tools-and-costs table found")
    if not sc:
        fail("SKILL.md: no '## Costs' section with tools found")
    if rc and sc:
        for tool in sorted(set(rc) | set(sc)):
            if tool not in rc:
                fail(f"tool `{tool}` is priced in SKILL.md but missing from the README table")
            elif tool not in sc:
                fail(f"tool `{tool}` is in the README table but missing from SKILL.md costs")
            elif rc[tool] != sc[tool]:
                fail(f"tool `{tool}` costs '{rc[tool]}' in README but '{sc[tool]}' in SKILL.md")
        if set(rc) == set(sc) and all(rc[t] == sc[t] for t in rc):
            ok(f"README and SKILL.md agree on {len(rc)} tools and their costs")

    # Every tool the skill mentions must be one it prices.
    for rel, text in skill_texts.items():
        mentioned = set(TOOL_NAME.findall(text))
        unknown = sorted(t for t in mentioned if t not in sc and t not in ("audit_id", "max_chars", "needs_review"))
        for t in unknown:
            fail(f"{rel}: mentions `{t}` but does not list its cost")

    # The number of claims rules must be the same everywhere.
    sources = {"plugin.json": manifest.get("description", ""), "README.md": readme, **skill_texts}
    counts = {src: set(RULE_COUNT.findall(text)) for src, text in sources.items()}
    found = set().union(*counts.values())
    if len(found) > 1:
        detail = ", ".join(f"{s}={sorted(c)}" for s, c in counts.items() if c)
        fail(f"claims-rule count differs between files: {detail}")
    elif found:
        ok(f"claims-rule count is {found.pop()} everywhere it is stated")

    # README must describe the same MCP endpoint as .mcp.json.
    for url in mcp_urls:
        if url not in readme:
            fail(f"README.md does not mention the MCP endpoint {url}")

    # Name in manifest should match the README heading/plugin naming.
    display = manifest.get("displayName")
    if display and display not in readme:
        warn(f"README.md never mentions the display name '{display}'")


# ---------------------------------------------------------------- version bump
def check_version_bump(manifest: dict, base_ref: str) -> None:
    print(f"\nversion bump vs {base_ref}")

    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout

    try:
        changed = git("diff", "--name-only", f"{base_ref}...HEAD").split()
    except subprocess.CalledProcessError as e:
        fail(f"could not diff against {base_ref}: {e.stderr.strip()}")
        return
    shipped = [p for p in changed if p.startswith(RELEASE_PATHS)]
    if not shipped:
        ok("no shipped files changed; no bump needed")
        return
    try:
        old = json.loads(git("show", f"{base_ref}:.claude-plugin/plugin.json")).get("version", "0.0.0")
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        ok("plugin.json is new on this branch")
        return
    new = manifest.get("version", "0.0.0")

    def key(v: str) -> tuple[int, ...]:
        m = SEMVER.match(v)
        return tuple(int(x) for x in m.groups()[:3]) if m else (0, 0, 0)

    if key(new) > key(old):
        ok(f"version bumped {old} -> {new}")
    else:
        fail(f"shipped files changed ({', '.join(shipped)}) but version is still {new} (base: {old})")


# ---------------------------------------------------------------- online
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)


def http_fetch(url: str, method: str = "GET", body: bytes | None = None,
               headers: dict | None = None) -> tuple[int, dict, str]:
    """Return (status, lower-cased headers, first 2 KB of body); status 0 = no response."""
    req = urllib.request.Request(url, data=body, method=method, headers={
        "User-Agent": "plugin-release-check/1.0", **(headers or {}),
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status, {k.lower(): v for k, v in resp.headers.items()}, ""
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 2:
                snippet = e.read(2048).decode("utf-8", "replace") if e.fp else ""
                return e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, snippet
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == 2:
                return 0, {}, ""
        time.sleep(2 * (attempt + 1))
    return 0, {}, ""


def http_status(url: str, method: str = "GET", body: bytes | None = None, headers: dict | None = None) -> int:
    return http_fetch(url, method, body, headers)[0]


def is_bot_challenge(headers: dict, body: str) -> bool:
    """True when a 403 is a bot-protection challenge (Cloudflare and similar), not a dead page."""
    if headers.get("cf-mitigated") == "challenge":
        return True
    server = headers.get("server", "").lower()
    markers = ("just a moment", "attention required", "cf-chl", "captcha", "challenge-platform",
               "bot protection", "sgcaptcha", "imunify360")
    return any(m in body.lower() for m in markers) or (
        server in ("cloudflare", "sucuri/cloudproxy", "akamaighost") and "<html" in body.lower()
    )


def check_link(url: str) -> None:
    page = url.split("#")[0]
    status, headers, body = http_fetch(page)
    if status == 403:
        # Many sites refuse non-browser clients and data-centre IPs; ask again as a browser.
        status, headers, body = http_fetch(page, headers={"User-Agent": BROWSER_UA, "Accept": "text/html"})
    if 200 <= status < 400:
        ok(f"{status} {url}")
    elif status in (403, 429) and is_bot_challenge(headers, body):
        warn(f"{url} returned {status} behind bot protection ({headers.get('server', 'unknown server')}); "
             "could not verify from CI, check it in a browser")
    else:
        server = headers.get("server", "unknown server")
        fail(f"{url} returned {status or 'no response'} ({server})")


def check_online(manifest: dict, skill_texts: dict[str, str], mcp_urls: list[str]) -> None:
    print("\nlinks")
    urls: set[str] = set()
    for key, value in manifest.items():
        if isinstance(value, str) and value.startswith("http"):
            urls.add(value)
    if isinstance(manifest.get("author"), dict) and manifest["author"].get("url"):
        urls.add(manifest["author"]["url"])
    for text in [README.read_text(encoding="utf-8"), *skill_texts.values()]:
        urls.update(u.rstrip(".,;:") for u in URL.findall(text))
    urls -= set(mcp_urls)
    for url in sorted(urls):
        check_link(url)

    print("\nMCP endpoint")
    init = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "plugin-release-check", "version": "1.0"}},
    }).encode()
    for url in mcp_urls:
        status = http_status(url, "POST", init, {
            "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        })
        # Unauthenticated: an OAuth-protected server answers 401; an open one answers 200.
        if status in (200, 401):
            ok(f"{url} answered {status} ({'needs sign-in, as expected' if status == 401 else 'open'})")
        else:
            fail(f"{url} answered {status or 'no response'}; expected 401 (sign-in) or 200")
        meta = url.split("/mcp")[0] + "/.well-known/oauth-protected-resource"
        if status == 401:
            ms = http_status(meta)
            if 200 <= ms < 300:
                ok(f"OAuth metadata found at {meta}")
            else:
                warn(f"no OAuth protected-resource metadata at {meta} ({ms or 'no response'})")


# ---------------------------------------------------------------- main
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true", help="check live URLs and the MCP endpoint")
    parser.add_argument("--base-ref", help="git ref to compare the version against, e.g. origin/main")
    args = parser.parse_args()

    print("files")
    manifest = load_json(PLUGIN_JSON) or {}
    mcp = load_json(MCP_JSON) or {}
    if manifest:
        check_manifest(manifest)
    if MARKETPLACE_JSON.exists():
        market = load_json(MARKETPLACE_JSON)
        if market and manifest:
            check_marketplace(manifest, market)
    mcp_urls = check_mcp(mcp) if mcp else []
    skill_texts = check_skills()
    check_consistency(manifest, skill_texts, mcp_urls)
    if args.base_ref:
        check_version_bump(manifest, args.base_ref)
    if args.online:
        check_online(manifest, skill_texts, mcp_urls)

    print(f"\n{len(failures)} failure(s), {len(warnings)} warning(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
