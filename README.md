# Brand Voice Checker for Claude

Check marketing copy against your brand voice guide and 16 advertising-claims rules without
leaving Claude, and rewrite or draft copy in your brand's voice. This plugin connects Claude to
your [Brand Voice](https://brandvoice.thelostagency.com) account and adds a skill that tells
Claude when to use the checks and what they cost.

## What it includes

- **Connector:** the remote MCP server at `https://brandvoice.thelostagency.com/mcp`
  (declared in `.mcp.json`). You sign in with your own Brand Voice account (OAuth) the first
  time Claude uses it.
- **Skill:** `brand-voice-checker` — read the brand's approved claims and house rules before
  writing, run the free quick scan, ask before any tool that spends credits, and offer the full
  compliance check before copy is published.

## Tools and costs

| Tool | Cost |
| --- | --- |
| `quick_scan`, `explain_rules`, `get_balance`, `list_register`, `get_brand`, `list_audits`, `get_audit_report` | Free |
| `check_compliance`, `check_brand_voice` | 1 credit |
| `rewrite_copy`, `draft_copy` | 1 credit per 2,000 characters |

Credits are bought on the Brand Voice website; the plugin cannot buy anything.

## What it sends and stores

The plugin runs no code on your machine. When a tool is used, Claude sends the copy and the
options you chose (brand domain, markets, language) to `https://brandvoice.thelostagency.com`.
That copy is processed and returned, not kept. Brand Voice keeps a record of each connection
(app name, dates, fingerprints of its tokens) and a usage record of each paid check. Details:
[privacy policy](https://brandvoice.thelostagency.com/privacy.html), section 6.

## Requirements

- A Brand Voice account with a verified email address.
- Credits for the paid tools.
- A voice guide for each brand you want scored, created at brandvoice.thelostagency.com.

## Help

Guide: <https://brandvoice.thelostagency.com/guide-claude-connector.html> ·
Support: support@brandvoice.thelostagency.com · Disconnect at any time under Account
settings → API keys → Connected AI assistants.
