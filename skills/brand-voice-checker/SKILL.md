---
name: brand-voice-checker
description: Use when writing, editing or reviewing marketing copy for a brand the user has in Brand Voice Checker — product descriptions, emails, ads, social posts, landing pages — or when the user asks whether copy is on-brand or compliant with advertising-claims rules, or asks about a page, a site audit or what is waiting in their Brand Voice account.
---

# Working with Brand Voice Checker

The Brand Voice Checker tools check marketing copy against the user's brand voice guide and
against 17 advertising-claims rules. Some tools are free; others spend the user's Brand Voice
credits.

## Costs — always say them first

- Free: `quick_scan`, `explain_rules`, `get_balance`, `list_register`, `get_brand`,
  `list_audits`, `get_audit_report`.
- Free with a verified account, daily limit: `get_guide`, `get_inbox`, `check_url_status`,
  `get_page_content`, `add_to_next_audit`, `detect_site`, `compare_audits`.
- 1 credit each: `check_compliance`, `check_brand_voice`.
- 1 credit per 2,000 characters: `rewrite_copy` (characters sent) and `draft_copy`
  (the `max_chars` requested, 200 to 8,000).

Before calling a paid tool, tell the user which tool you will run and what it costs, and wait
for them to agree, unless they have already asked for that check. Report the cost line from
each result. If a result says there are not enough credits, tell the user and do not retry;
credits are managed in their Brand Voice account on the website.

The daily-limit tools cost nothing, but each account has a daily allowance (reading a page live
has a lower one). Do not call them in loops over many pages; if a result says the limit is
reached, tell the user and stop. They need a verified email address on the account.

## Before writing copy for a brand

1. Ask which brand (website domain) the copy is for if it is not clear.
2. Call `get_brand` (free) for that domain to see whether it has a voice guide, its markets and
   audience, and what is in its register. With no guide, `check_brand_voice` and `draft_copy`
   cannot run yet: send the user to create the guide (the link is in the result).
3. Call `get_guide` for the guide itself (tone, rules, do's and don'ts, example copy) and write
   to it. Pass `brand` when one website has guides for several brands.
4. Call `list_register` for that domain and follow it: use approved claims as worded, never
   use never-say phrases, include required wording, and respect topic rules.
5. Write the copy, or use `draft_copy` when the user wants it written in the brand's voice
   from a brief.

## Before presenting copy as ready to publish

- Run `quick_scan` (free) on it and fix keyword hits you can fix.
- Offer `check_compliance` (1 credit) before the user publishes. Use the brand's markets from
  `get_brand`, or ask (for example UK, NL, AU, US, EU); with no markets the check is Global,
  the strictest.
- Never describe a quick scan with no keyword flags as compliant or cleared. Only
  `check_compliance` reads the judgement rules, the user's markets and their approved claims.

## One page of a website

- "What do we know about this page?": `check_url_status` gives the newest audit that read it
  (keyword hits, full check results), whether it is on the next-audit list, and the tracked
  content item made from it. Checks run without Track or Save & share are not stored, so they do
  not appear.
- "Check this page" or "rewrite this page": `get_page_content` returns its title, meta
  description, headings and main text (up to 6,000 characters), from an audit or read live
  (robots.txt honoured, nothing stored). Then run `quick_scan` on the text, and offer
  `check_compliance` (1 credit) or `rewrite_copy` as usual. Pass `live: false` to use audits only.
- `add_to_next_audit` puts the page on the list the next audit of that site reads first
  (`remove: true` takes it off). Nothing is read now.

## Site audits

A site content audit is a scan of many pages of a website, started and paid for on the website
(https://brandvoice.thelostagency.com/site-audit.html). These tools only read audits already run.

- "What did my audit of example.com find?", "which pages need work?": call `get_audit_report`
  with the domain (its latest finished audit) or an `audit_id` from `list_audits`.
- Lead with the pages with the most to review and the rules hit most; mention missing required
  wording and claims that are not approved yet. Give the link to the full report.
- "What changed since last time?", "did our fixes work?": `compare_audits` with the domain or an
  `audit_id` lists pages worse, better, gone, new or unchanged against the previous audit.
- Audit hits are keyword matches from the free layer, not a compliance verdict. For one page
  that matters, offer `check_compliance` (1 credit) on its copy.
- Before a first audit, `detect_site` reads the homepage, robots.txt and sitemap: the CMS, how
  many pages the sitemap lists, and which duplicate page types an audit should leave out.
- To start a new audit, or to re-run one, send the user to the site audit page; there is no
  tool for it. Paid full checks of audited pages (compliance, brand voice, or both, on the worst
  pages, ticked pages or every page the audit read) are also started there.
- An audit reads a sample of the site's pages, so a page can be missing from it. Say so plainly
  rather than treating the page as clean. Offer `add_to_next_audit` for it, or check that page's
  copy now with `get_page_content` and `quick_scan`, or `check_compliance` (1 credit).

## What is waiting for the user

`get_inbox` lists what waits for a decision across the account's brands: content in review,
returned or on hold, approvals waiting for evidence or expiring, guide updates to review, and
site audits running or finished recently. It is read only; decisions are made on the website.
Use it for "what needs my attention?" or at the start of a working session when the user asks.

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
- A daily-limit tool says the account is not verified: the user verifies their email address in
  their Brand Voice account first.
