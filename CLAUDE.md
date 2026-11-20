# CLAUDE.md

Guidance for Claude when working in this repository.

## Local folder (Windows)

The owner's local copy of this repo is:

```
C:\dev\brand-voice-checker-plugin
```

Use this exact path in every PowerShell command you give.

## How to give deploy instructions

- **Windows / PowerShell only.** Do not write Mac or Linux instructions.
- **Full paths, always.** Every command uses the full path above, for example
  `git -C "C:\dev\brand-voice-checker-plugin" pull origin main`, never a bare `cd` plus relative paths.
- **Whole files, never surgical edits.** When a file changes, provide or commit the complete file.
  Do not ask the owner to edit lines by hand unless they ask for that.
- Give each command in its own code block so it can be copied on its own.
- Include PowerShell instructions with every deploy or release.

## What this repo is

A Claude Code plugin that connects Claude to Brand Voice Checker. It runs no code of its own;
the tools live on the remote MCP server at `https://brandvoice.thelostagency.com/mcp`.

| Path | What it is |
| --- | --- |
| `.claude-plugin/plugin.json` | Plugin manifest (name, version, links, icon) |
| `.claude-plugin/marketplace.json` | Makes this repo its own marketplace, `thelostagency` |
| `.claude-plugin/icon.png` | 512x512 listing icon |
| `.mcp.json` | Points Claude at the remote MCP server |
| `skills/brand-voice-checker/SKILL.md` | When and how Claude uses the tools, and what they cost |
| `README.md` | Public listing page: install line, tools and costs, privacy |
| `.github/scripts/check_plugin.py` | Release checks (Python, standard library only) |
| `.github/workflows/plugin-checks.yml` | Runs the checks on push, PR and every Monday |

## Keep these in step

The release checks fail if any of these drift apart, so change them together:

- **Version:** `plugin.json` `version` and the `brand-voice-checker` entry's `version` in
  `marketplace.json`. Raise it (semver) in any change to `.claude-plugin/`, `.mcp.json` or `skills/`.
  Changes to `README.md`, `CLAUDE.md` or `.github/` alone need no bump.
- **Description:** same text in `plugin.json` and the `marketplace.json` entry.
- **Tools and prices:** the tools-and-costs table in `README.md` and the `## Costs` section of
  `SKILL.md` must list the same tools at the same prices. They must also match the live server's
  tool list.
- **Claims-rule count:** "17 rules" appears in `plugin.json`, `README.md` and `SKILL.md`; change all
  three if the server's count changes.

## Release checklist

1. Make the change; raise the version in both manifests if shipped files changed.
2. Run the checks locally (commands below); fix anything that fails.
3. Commit on a branch, open a PR to `main`, and wait for **Plugin checks** to go green.
4. Merge, then give the owner the PowerShell commands to update their local copy.

## Running the checks (PowerShell)

```powershell
python "C:\dev\brand-voice-checker-plugin\.github\scripts\check_plugin.py"
```

```powershell
python "C:\dev\brand-voice-checker-plugin\.github\scripts\check_plugin.py" --online
```

```powershell
npx --yes @anthropic-ai/claude-code@2.1.329 plugin validate --strict --profile directory "C:\dev\brand-voice-checker-plugin"
```

```powershell
npx --yes @anthropic-ai/claude-code@2.1.329 plugin validate --strict "C:\dev\brand-voice-checker-plugin\.claude-plugin\plugin.json"
```

To compare the version against `main` (as a PR does):

```powershell
python "C:\dev\brand-voice-checker-plugin\.github\scripts\check_plugin.py" --base-ref origin/main
```

## Test an install locally

```powershell
claude plugin marketplace add "C:\dev\brand-voice-checker-plugin"
```

```powershell
claude plugin install brand-voice-checker@thelostagency
```

## Notes

- `https://thelostagency.com` blocks non-browser requests; the link check retries it as a browser.
  A 403 from bot protection is a warning, not a failure.
- The validator is pinned to `@anthropic-ai/claude-code@2.1.329` in the workflow. Bump it on purpose.
- Never commit `.claude/settings.local.json` (it is in `.gitignore`).
