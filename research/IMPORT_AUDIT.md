# Week 1 import and arithmetic audit

## Preservation and reproducibility
Both supplied files were copied byte-for-byte to research/raw/. The workbook upload name `week1_scorecard_1_.xlsx` was normalized to `week1_scorecard.xlsx`; its bytes were not changed. SHA-256 values:
- Workbook: `4c9a7d5ee8c4da5e1a47d19b8946fce53462957541ca0c6181b20ef6fec181f0`
- Markdown: `5ecbed35c25471c532549ad349a7a9b670d195497738b6c44fc14371436a30ba`

Run `python scripts/import_week1.py` using openpyxl (already installed in this workspace). This reads originals only, validates formulas/caches, and regenerates derived CSVs and workbook_cells.json. The manifest retains the first import time; a changed source hash stops the importer. The validator uses Python standard library only. No package installation, paid API, web request or spreadsheet execution is involved in importing. No macros/external links are executed.

All three sheets were read in full, including notes: Niche Scorecard (13 × 8), 18 Competitors (19 × 18), Royalty Scenarios (10 × 8). workbook_cells.json preserves every nonempty source cell's coordinate, raw value/formula and cached value. CSV rows include sheet/range lineage. The accompanying Markdown was read in full and agrees with the score inputs, ranking and conditional recommendation.

## Scorecard
Weights B6:F6: 0.30 demand, 0.25 differentiation, 0.20 competition ease, 0.15 economics, 0.10 KDP fit; sum = 1. Ratings are 1–5, with higher competition ease meaning easier competition. Formula: sum(rating × weight) / 5 × 100, exactly as the workbook; no subtraction of the scale minimum.

| Source row | Weighted /5 | Recomputed /100 | Cached /100 | Result |
|---|---:|---:|---:|---|
| 2 Backyard birds | 3.660 | 73.2 | 73.2 | Match |
| 3 Woodland wildlife | 3.165 | 63.3 | 63.3 | Match |
| 4 English–Arabic vehicles | 2.975 | 59.5 | 59.5 | Match |

Formula text and cached results were checked, with 1e-9 arithmetic tolerance. No missing formula caches in these result cells. Scores are unchanged. Arithmetic agreement does not validate demand or subjective input ratings. Criteria and weights are now retained in niche_scorecard.csv.

## Competitor normalization
18 distinct source works: 7 backyard-bird, 5 bilingual/construction-adjacent, 6 woodland. Two works carry both US and CA prices, resulting in **20 currency/market observations**, not 20 competitors. Stable work IDs link split observations. ISBN10 values stay distinct from confirmed-format ASIN claims; unknown identifiers and BSR remain blank in normalized fields, with original strings retained. Source price provenance and all primary/secondary/product links are preserved.

Publisher and retailer prices are not relabeled Amazon prices. MerchantWords observations are third-party snapshots, not live Amazon verification. No row is newly independently verified. The source's “Rating count” is retained as rating_count, not review_count; actual textual-review counts remain unknown. Source row 17 combines publisher specs with aggregator ratings without identifying an exact rating source URL; this ambiguity is explicitly flagged. Positioning strings preserve stated ages and features without treating analyst copy as verified metadata. Missing format/language/age fields remain blank until verified; relevant claims remain readable in source positioning.

The source research date is 2026-11-10, but individual retrieval timestamps are absent. Imported-at time is separate and must not be used as retrieval time. Blank dates, counts and ranks are not zero. No verbatim critical-review evidence exists in either source. The 7 bird works include adult, mixed-age and sticker/activity adjacencies; they are not a qualifying 10-listing close US cohort. The Canadian woodland snapshot is not bird-market evidence.

## Royalty scenarios
All six E:G formula sets and their cached values match an independent Decimal recomputation. royalty_scenarios.csv preserves prices, rates, costs and same-currency spend-coverage calculations. Rounded display uses decimal half-up to cents, matching the Markdown (e.g. Canada 12.99 × 0.50 − 3.53 = 2.965, displayed 2.97). Break-even ceilings use unrounded royalties, not the displayed cents.

At proposed launch prices: US 9.99 × 0.60 − 2.84 = 3.154, displayed US$3.15; CA 13.99 × 0.60 − 3.53 = 4.864, displayed C$4.86. These are mathematically consistent source assumptions, **not newly verified current KDP economics or profit**. Rates, tier thresholds and print costs still require official verification. Spend-coverage figures exclude taxes, proofs, returns, design time and other costs and are not a recommended ad budget or sales forecast.

## Reassessment
Retain CONDITIONAL GO for editorial planning. Source evidence supports adjacent products and shows that facts, puzzles and checklists already exist; the opportunity is a coherent, accurate learning sequence, not invention of those features. No reliable live demand, BSR, negative-review or exact cohort evidence supports upgrading the recommendation. Arabic paperback eligibility remains a source-reported unresolved gate, not independently confirmed current policy.

Fresh requests to the actual supplied Amazon links and official cost/royalty links were again proxy-denied; timestamps and URLs are in access_attempts.csv. No restrictions were bypassed. Direct known links now appear in MANUAL_VERIFICATION.md. No illustrations, spending, uploads or production implementation occurred.

## Validation performed
Importer assertions and the milestone validator passed. A repeated import produced byte-identical derived outputs. An isolated temporary changed-source test was rejected by the hash guard before parsing. Both stored originals were compared directly with uploaded attachment bytes and matched. The original Markdown retains its intentional trailing spaces; source formatting is not normalized.
