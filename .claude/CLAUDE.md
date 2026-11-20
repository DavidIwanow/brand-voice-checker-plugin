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
| `.claude/CLAUDE.md` | This file. Kept here, not at the root: a root `CLAUDE.md` ships with the plugin and fails the strict validator |

## No scripts, programs or bytecode

The plugin directory refuses scripts, programs and bytecode from organisations that are not
Verified, and the whole repo is the plugin (`source: "./"`). Do not add `.py` files, other scripts,
binaries or a CI workflow that needs them. `.gitignore` ignores `*.py`, `*.pyc` and `__pycache__/`.
Never commit with `git add -A` without checking `git status` first.

## Keep these in step

Nothing checks these automatically any more, so check them by hand before every release:

- **Version:** `plugin.json` `version` and the `brand-voice-checker` entry's `version` in
  `marketplace.json` must be the same. Raise it (semver) in any change to `.claude-plugin/`,
  `.mcp.json` or `skills/`. Changes to `README.md` or `.claude/CLAUDE.md` alone need no bump.
- **Description:** same text in `plugin.json` and the `marketplace.json` entry.
- **Tools and prices:** the tools-and-costs table in `README.md` and the `## Costs` section of
  `SKILL.md` must list the same tools at the same prices, and match the live server's tool list.
- **Claims-rule count:** "17 rules" appears in `plugin.json`, `README.md` and `SKILL.md`; change all
  three if the server's count changes.

## Release checklist

1. Make the change; raise the version in both manifests if shipped files changed.
2. Check the "Keep these in step" list above.
3. Run the official validator (below); fix anything it reports, warnings included.
4. Commit on a branch, open a PR to `main`, merge.
5. Give the owner the PowerShell commands to update their local copy.

## Validate (PowerShell)

The official validator. `--strict` fails on warnings; `--profile directory` adds the plugin
directory's submission checks. With `marketplace.json` present, validating the folder checks the
marketplace, so validate `plugin.json` on its own too.

```powershell
npx --yes @anthropic-ai/claude-code@latest plugin validate --strict --profile directory "C:\dev\brand-voice-checker-plugin"
```

```powershell
npx --yes @anthropic-ai/claude-code@latest plugin validate --strict "C:\dev\brand-voice-checker-plugin\.claude-plugin\plugin.json"
```

## Test an install locally

```powershell
claude plugin marketplace add "C:\dev\brand-voice-checker-plugin"
```

```powershell
claude plugin install brand-voice-checker@thelostagency
```

## Update the local copy after a merge

```powershell
git -C "C:\dev\brand-voice-checker-plugin" checkout main
```

```powershell
git -C "C:\dev\brand-voice-checker-plugin" pull origin main
```

## Notes

- `https://thelostagency.com` blocks non-browser requests (bot protection); a 403 from a script
  does not mean the link is dead. Check it in a browser.
- Never commit `.claude/settings.local.json` (it is in `.gitignore`).
