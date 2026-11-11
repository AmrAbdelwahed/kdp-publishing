# Milestone 1A — manual Amazon capture
Date: 2026-11-11, America/Toronto. Current status: **0 US / 0 CA independently verified bird listings**. Infrastructure ready; marketplace verification incomplete. Blank template slots are not products.

## What to supply
Send a filled copy of capture_template.csv (10 US rows and 5 CA rows minimum), plus supporting screenshots or dated text notes. More observations are welcome. You may instead attach an XLSX spreadsheet or screenshots with URLs and capture times; Codex will preserve them and transcribe a CSV for review before importing. The importer accepts UTF-8 CSV only; it does not OCR screenshots or automatically parse XLSX. Keep the original uploads unchanged. Partial batches are useful; unknown optional values stay blank with reasons in missing_values. Do not delay all captures waiting for a field Amazon does not expose.

For screenshots: capture the title/selected paperback/price, product details (ASIN/pages/publisher/date), rating/BSR/category and relevant description/review passages. Multiple images per listing are fine. Include the URL in notes and capture time with timezone. Redact personal account/address/order/payment information before sending. Do not use any access-control bypass; skip unavailable pages and say why. Do not buy anything.

## Discovery and selection
Use an ordinary permitted browser, choose paperback and confirm the edition after every format change. Record actual displayed marketplace and currency. Use these discovery links:
- US bird colouring/activity: https://www.amazon.com/s?k=bird+coloring+activity+book+kids+6-9
- US backyard bird identification: https://www.amazon.com/s?k=backyard+bird+activity+book+children
- CA bird colouring/activity: https://www.amazon.ca/s?k=bird+colouring+activity+book+kids
- CA birdwatching activities: https://www.amazon.ca/s?k=birdwatching+activity+book+children

Starting product links retained from Week 1 (not freshly verified):
- Birds Coloring Book for Kids: https://www.amazon.com/dp/0648714314
- Backyard Bird Adventure Activity Book: https://a.co/d/0gZ9LkzD (resolve normally, copy final product URL and ASIN)
- Birds at Home: https://www.amazon.com/dp/1497205972 (adult adjacency)
- Backyard Birds Large Print: https://www.amazon.com/dp/B0HNHPZ8KF (adult adjacency)

seed_links.csv provides title-specific US and CA searches for all seven existing bird works. No Canadian product link is confirmed in the source; discover the actual Canadian paperback listing rather than assuming an ISBN guarantees availability. Retain search query and page context, including Sponsored labels. Do not infer organic discovery from a product page alone. Avoid selecting only highly rated books. Record exclusions and unavailable candidates in dated notes; inability to find/access a book is not low competition.

Aim for 10 relevant US and 5 relevant CA unique paperback ASINs, emphasizing closely matched children's bird colouring/activity books. Report direct and adjacent counts separately; adult, sticker-only or broad-age titles may be useful adjacencies but cannot silently satisfy the close-comparable objective. US/CA entries for the same work count separately by market, not twice within one market; repeated timestamps are observations, not more products.

## Fields to capture (exact CSV headers)
| Fields | Instructions |
|---|---|
| capture_id | Unique observation ID; e.g. US-01-capture1. New ID for every later observation or correction. |
| marketplace, product_title, asin, product_url | Exact title; Amazon.com or Amazon.ca; actual 10-character paperback ASIN. Set ASIN cells to text to retain leading zeroes. Copy final HTTPS /dp/ASIN or /gp/product/ASIN link matching that marketplace. |
| classification, classification_reason | direct / adjacent / uncertain. Analyst classification: direct = child-targeted bird colouring/activity product with substantial age-6–9 overlap. State observed rationale; do not treat overlap as exact age targeting. |
| age_range | Exact stated age text and location; blank if not stated. Do not invent from artwork. Explicit 6–9 vs overlap (4–8 or 6–10) matters. |
| format, page_count | format must be paperback. Pages as plain positive integer from selected edition's details. |
| price, currency, price_context | Current displayed new-paperback offer as decimal without symbol; USD or CAD. Note seller, new/used condition, displayed list vs sale price, coupon, tax/shipping exclusions and delivery region at country level. Do not substitute retailer prices or expose address. Unknown price stays blank. |
| bsr, bsr_category | Rank as plain positive integer and exact category, preferably Books overall. Never compare ranks from different categories as equivalent. Use one principal rank per observation; extra ranks in notes. Blank if unavailable, not zero. |
| star_rating, rating_count | Aggregate star score and number of customer ratings, not number of written reviews. Note if Amazon pools editions/markets; don't attribute all to paperback. |
| publication_date, publisher | Selected paperback details. Date YYYY-MM-DD only when exact; partial date goes in notes and normalized date stays blank. |
| educational_features | Faithful page-description/preview observations with location. Distinguish claimed features from actual interior preview. |
| key_differentiation | Analyst interpretation, explicitly labeled, comparing colour–identify–observe integration, age fit, field marks and regional caveats. Unknown feature is not absent feature. |
| customer_feedback, feedback_url, feedback_date | Short attributed excerpt or faithful paraphrase, exact review permalink and review date YYYY-MM-DD. Note rating, relevant edition and verified-purchase status only if visible. No fabricated complaints. Multiple reviews can use additional dated captures. |
| observed_weaknesses | Separate directly evidenced weaknesses from analyst hypotheses; name evidence. If none verified, say so. Absence of captured complaints does not establish no complaints. |
| discovery, search_query, discovery_url | sponsored / organic / unknown / direct_link, query and exact search URL. “Organic” requires visible search-context evidence. |
| source_url, collected_at | Actual Amazon product URL matching ASIN; capture time in ISO 8601 with timezone, e.g. 2026-11-11T14:30:00-05:00. Review permalink is separate. Don't use import time as observation time. |
| evidence_refs | Semicolon-separated repository-relative file paths, e.g. research/raw/marketplace/incoming/US01-details.png; preserve uploads first. Required; dated text capture notes are accepted when screenshots aren't available. |
| confidence | low / medium / high is collector's assessment of visible fields, not automatic verification. High requires clear supported edition/price/details and traceable captures. |
| missing_values, notes | List each absent field with why (not displayed / inaccessible / not collected); use “none” only if complete. Notes retain raw strings, limitations, partial dates, supplemental ranks and seller/edition ambiguity. |

## Capture protocol
1. Start with a copy of capture_template.csv; it has 10 US and 5 CA identity-only slots. Add rows as needed. Leave unknowns blank, never N/A or zero in numeric fields. Literal rating_count=0 is allowed only when observed.
2. Capture product identity/format, offer and details in the same session. Record exact capture time. Add supporting images/notes, including location for every populated field.
3. Where accessible, inspect recent critical reviews, not just average stars. Record actual evidence and contradictory/positive examples. Note sampling window and reviewed count; do not generalize one complaint. A single rank is not monthly sales.
4. Supply screenshots/CSV/XLSX as attachments. Codex stores originals under research/raw/marketplace/incoming/ without overwriting prior uploads, sets evidence_refs, and checks transcription with you when ambiguous. CSV formulas are not executed by the importer; use plain text and open untrusted CSV in a spreadsheet with formula execution disabled.

## Import and history
From the repository root, after originals and evidence files have been preserved:

```sh
python scripts/import_marketplace.py /path/to/completed.csv --dry-run
python scripts/import_marketplace.py /path/to/completed.csv
python scripts/import_marketplace.py --history
python -m unittest discover -s scripts -p 'test_import_marketplace.py'
```

Use one importer process at a time. Entire input validates before writing. It stores raw CSV bytes, normalized observations, copied evidence bytes with hashes, and flags under research/marketplace/batches/<CSV-SHA256>/. Prior batches and research/competitors.csv are never rewritten. Identical CSV bytes are idempotent. Reusing an existing capture_id with different input is rejected; assign a new ID for corrections and mention the superseded ID in notes. The history command prints the union of all observations, not a destructively merged latest-value table.

Report flags identify repeat marketplace+ASIN, same-time conflicting values, changed metadata, and same-title other-market/ASIN candidates. Price/rank/rating changes at later times are temporal observations, not automatically errors. Review flags manually; don't silently pick a winner. A partial correction never erases an earlier known value. All imported rows remain pending_human_evidence_review, regardless of confidence. Structural validation checks syntax/identity/provenance, not truth of screenshots. Human verification requires checking each populated field against the archived evidence and recording reviewer/date/accepted fields and unresolved flags in a separate dated review note; do not edit batch files.

After review, reassess unique eligible product counts, direct age-fit cohort and evidence coverage before changing scores or recommendation. Template completion alone is not commercial validation.
