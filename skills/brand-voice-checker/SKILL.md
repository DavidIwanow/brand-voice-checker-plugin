---
name: brand-voice-checker
description: Use when writing, editing or reviewing marketing copy for a brand the user has in Brand Voice Checker — product descriptions, emails, ads, social posts, landing pages — or when the user asks whether copy is on-brand or compliant with advertising-claims rules.
---

# Working with Brand Voice Checker

The Brand Voice Checker tools check marketing copy against the user's brand voice guide and
against 16 advertising-claims rules. Some tools are free; others spend the user's Brand Voice
credits.

## Costs — always say them first

- Free: `quick_scan`, `explain_rules`, `get_balance`, `list_register`.
- 1 credit each: `check_compliance`, `check_brand_voice`.
- 1 credit per 2,000 characters: `rewrite_copy` (characters sent) and `draft_copy`
  (the `max_chars` requested, 200 to 8,000).

Before calling a paid tool, tell the user which tool you will run and what it costs, and wait
for them to agree, unless they have already asked for that check. Report the cost line from
each result. If a result says there are not enough credits, pass on the top-up link and do not
retry.

## Before writing copy for a brand

1. Ask which brand (website domain) the copy is for if it is not clear.
2. Call `list_register` for that domain and follow it: use approved claims as worded, never
   use never-say phrases, include required wording, and respect topic rules.
3. Write the copy, or use `draft_copy` when the user wants it written in the brand's voice
   from a brief.

## Before presenting copy as ready to publish

- Run `quick_scan` (free) on it and fix keyword hits you can fix.
- Offer `check_compliance` (1 credit) before the user publishes. Ask which markets the copy is
  for (for example UK, NL, US, EU); with no markets the check is Global, the strictest.
- Never describe a quick scan with no keyword flags as compliant or cleared. Only
  `check_compliance` reads the judgement rules, the user's markets and their approved claims.

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
