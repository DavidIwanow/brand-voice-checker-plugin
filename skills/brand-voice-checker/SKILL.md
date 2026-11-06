---
name: brand-voice-checker
description: Use when writing, editing or reviewing marketing copy for a brand the user has in Brand Voice Checker — product descriptions, emails, ads, social posts, landing pages — or when the user asks whether copy is on-brand or compliant with advertising-claims rules.
---

# Working with Brand Voice Checker

The Brand Voice Checker tools check marketing copy against the user's brand voice guide and
against 17 advertising-claims rules. Some tools are free; others spend the user's Brand Voice
credits.

## Costs — always say them first

- Free: `quick_scan`, `explain_rules`, `get_balance`, `list_register`, `get_brand`,
  `list_audits`, `get_audit_report`.
- 1 credit each: `check_compliance`, `check_brand_voice`.
- 1 credit per 2,000 characters: `rewrite_copy` (characters sent) and `draft_copy`
  (the `max_chars` requested, 200 to 8,000).

Before calling a paid tool, tell the user which tool you will run and what it costs, and wait
for them to agree, unless they have already asked for that check. Report the cost line from
each result. If a result says there are not enough credits, tell the user and do not retry;
credits are managed in their Brand Voice account on the website.

## Before writing copy for a brand

1. Ask which brand (website domain) the copy is for if it is not clear.
2. Call `get_brand` (free) for that domain to see whether it has a voice guide, its markets and
   audience, and what is in its register. With no guide, `check_brand_voice` and `draft_copy`
   cannot run yet: send the user to create the guide (the link is in the result).
3. Call `list_register` for that domain and follow it: use approved claims as worded, never
   use never-say phrases, include required wording, and respect topic rules.
4. Write the copy, or use `draft_copy` when the user wants it written in the brand's voice
   from a brief.

## Before presenting copy as ready to publish

- Run `quick_scan` (free) on it and fix keyword hits you can fix.
- Offer `check_compliance` (1 credit) before the user publishes. Use the brand's markets from
  `get_brand`, or ask (for example UK, NL, AU, US, EU); with no markets the check is Global,
  the strictest.
- Never describe a quick scan with no keyword flags as compliant or cleared. Only
  `check_compliance` reads the judgement rules, the user's markets and their approved claims.

## Site audits (free)

A site content audit is a scan of many pages of a website, started and paid for on the website
(https://brandvoice.thelostagency.com/site-audit.html). These tools only read audits already run.

- "What did my audit of example.com find?", "which pages need work?": call `get_audit_report`
  with the domain (its latest finished audit) or an `audit_id` from `list_audits`.
- Lead with the pages with the most to review and the rules hit most; mention missing required
  wording and claims that are not approved yet. Give the link to the full report.
- Audit hits are keyword matches from the free layer, not a compliance verdict. For one page
  that matters, offer `check_compliance` (1 credit) on its copy.
- To start a new audit, or to re-run one, send the user to the site audit page; there is no
  tool for it. Paid full checks of audited pages (compliance, brand voice, or both, on the worst
  pages, ticked pages or every page the audit read) are also started there.
- An audit reads a sample of the site's pages, so a page can be missing from it. Say so plainly
  rather than treating the page as clean. The user can add it to the site's next audit from the
  Brand Voice Checker Chrome extension ("Include in next audit", free) or check that page's copy
  now with `quick_scan` (free) or `check_compliance` (1 credit).

## The Chrome extension

The Brand Voice Checker Chrome extension works on the page the user is viewing; none of it runs
through these tools. If the user asks how to check a live web page in their browser, it offers a
free "Scan this page now" (keyword rules, reading ease, stock AI phrasing), a paid whole-page
compliance check (1 credit), how that page did in their site audits, and "Include in next
audit". It is installed and connected from the website.

## Reading results

- A compliance verdict of `hold` means do not publish as written; `needs_review` and `review`
  need the listed fixes or substantiation. Quote each flag's fix.
- Flags marked as approved claims are covered by the user's register; leave that wording alone.
- A brand voice score comes with lines that drift from the voice; offer `rewrite_copy` for them.
- A rewrite or draft is not compliance-checked. Say so, and offer `check_compliance` on it.

## When something is missing

- "No brand voice profile found for this domain": the user needs to create the brand's voice
  guide at https://brandvoice.thelostagency.com first.
- "Your seat is limited to specific clients": ask for one of the user's client domains.
