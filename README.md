# Brand Voice Checker for Claude

Check marketing copy against your brand voice guide and 17 advertising-claims rules without
leaving Claude, and rewrite or draft copy in your brand's voice. This plugin connects Claude to
your [Brand Voice](https://brandvoice.thelostagency.com) account and adds a skill that tells
Claude when to use the checks and what they cost.

## Install

In Claude Code, run:

```
/plugin install brand-voice-checker --marketplace DavidIwanow/brand-voice-checker-plugin
```

On Claude Code older than 2.1.275, add the marketplace first, then install:

```
/plugin marketplace add DavidIwanow/brand-voice-checker-plugin
/plugin install brand-voice-checker@thelostagency
```

The first time Claude uses a Brand Voice tool, it asks you to sign in to your Brand Voice account.

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
| `check_url_status`, `get_page_content`, `add_to_next_audit`, `detect_site`, `get_guide`, `get_inbox`, `compare_audits` | Free (daily limit per account) |
| `check_compliance`, `check_brand_voice` | 1 credit |
| `rewrite_copy`, `draft_copy` | 1 credit per 2,000 characters |

Credits are bought on the Brand Voice website; the plugin cannot buy anything.

The free page, site, guide and inbox tools need a verified account and have a daily allowance
per account (live page reads and site detection: 20 a day, 100 after buying credits). The
limits, including the quick scan's from Claude (50 a day, 300 after buying credits), are listed in the [guide](https://brandvoice.thelostagency.com/guide-claude-connector.html#daily-limits).

## What it sends and stores

The plugin runs no code on your machine. When a tool is used, Claude sends the copy and the
options you chose (brand domain, markets, language) to `https://brandvoice.thelostagency.com`.
That copy is processed and returned, not kept. `get_page_content` and `detect_site` read public
web pages from Brand Voice's server when asked (robots.txt honoured, nothing stored). Brand Voice keeps a record of each connection
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
