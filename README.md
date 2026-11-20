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
- **Skill:** `brand-voice-checker` — read the brand's voice guide, approved claims and house
  rules before writing, run the free quick scan, ask before any tool that spends credits, offer
  the full compliance check before copy is published, and read pages, site audits and what is
  waiting in your account.

## Tools and costs

| Tool | Cost |
| --- | --- |
| `quick_scan`, `explain_rules`, `get_balance`, `list_register`, `get_brand`, `list_audits`, `get_audit_report` | Free |
| `get_guide`, `get_inbox`, `check_url_status`, `get_page_content`, `add_to_next_audit`, `detect_site`, `compare_audits` | Free with a verified account, daily limit |
| `check_compliance`, `check_brand_voice` | 1 credit |
| `rewrite_copy`, `draft_copy` | 1 credit per 2,000 characters |

What the account tools do:

- `get_guide` — the brand's saved voice guide: tone, rules, do's and don'ts, example copy.
- `get_inbox` — what waits for a decision: content in review or on hold, approvals, guide
  updates, recent site audits.
- `check_url_status` — what is recorded about one page: audits that read it, tracked content,
  whether it is on the next-audit list.
- `get_page_content` — one page's title, description, headings and text, from an audit or read
  live.
- `add_to_next_audit` — puts a page on the list the next site audit reads first.
- `detect_site` — the CMS a website uses and what its sitemap lists, before a first audit.
- `compare_audits` — what changed since the previous audit of a website.

Credits are bought on the Brand Voice website; the plugin cannot buy anything. Site audits are
started and paid for on the website, not from Claude.

## What it sends and stores

The plugin runs no code on your machine. When a tool is used, Claude sends the copy, page
addresses or website domains, and the options you chose (brand domain, markets, language) to
`https://brandvoice.thelostagency.com`. Copy is processed and returned, not kept. Pages read live
by `get_page_content` and sites read by `detect_site` are not stored; `add_to_next_audit` saves
the page address to that website's next-audit list. Brand Voice keeps a record of each connection
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
