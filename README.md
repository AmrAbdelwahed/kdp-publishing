# KDP Publishing — Milestone 0
Original, AI-assisted children's colouring/activity books. First candidate: **Backyard Bird Detectives: Color, Spot & Explore**, ages 6–9. US and Canadian paperback markets; low-cost print-on-demand pilot November 10–December 9, 2026.

## Status
**CONDITIONAL GO for editorial planning only; not a validated market opportunity or publication approval.** Scores and royalties in this repository are user-reported starting values, not audited workbook results. The repository and remote were empty on inspection. The two authoritative Week 1 artifacts were absent; no source files were changed or reconstructed. Public-source requests were proxy-denied. Milestone 0 is therefore partially delivered with explicit evidence blockers.

## Setup and validation
Use the existing checkout. Python 3, no extra packages or secrets required for the current documents and CSV validator:

```sh
cd /workspace/kdp-publishing
python scripts/validate_milestone.py
```

No app, server, paid API or PDF generator is installed. CSV uses UTF-8 and blank cells for unknowns.

## Navigation
- docs/PROJECT_BRIEF.md: constraints and product hypothesis.
- docs/30_DAY_PILOT.md and docs/DECISIONS.md: milestones and decision gates.
- docs/RESEARCH_METHOD.md, research/evidence_gaps.md: evidence protocol and blockers.
- research/niche_scorecard.csv: unaudited, user-reported scores.
- research/competitors.csv: schema only, no invented competitor records.
- books/book-001/blueprint/: provisional 64-page editorial design.
- docs/PRODUCTION_PLAN.md: deferred Python production requirements.

## Next steps
Supply research/raw/week1_scorecard.xlsx and research/raw/week1_niche_validation.md; audit all three sheets, import the 18 records and verify weighted calculations. Collect at least 10 closely comparable US and 5 relevant Canadian listings with evidence. Verify species facts and official KDP requirements. Then approve or revise the blueprint before illustration or generator work. Budget remains unspent by this task.
