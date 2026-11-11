# KDP Publishing — research and editorial planning
Original, AI-assisted children's colouring/activity books. First candidate: **Backyard Bird Detectives: Color, Spot & Explore**, ages 6–9. US and Canadian paperback markets; low-cost print-on-demand pilot November 10–December 9, 2026.

## Status
**CONDITIONAL GO for editorial planning only; not a validated market opportunity or publication approval.** Both Week 1 originals are preserved and imported. All three sheets were read; scorecard and royalty arithmetic match formulas and cached values. Eighteen works are represented by 20 market/currency observations. Marketplace observations, bird facts and current KDP rules remain unverified; public-source requests are still proxy-denied. Milestone 0 remains partially delivered pending those external evidence gates.

## Setup and validation
Use the existing checkout. Python 3, no extra packages or secrets required for the current documents and CSV validator:

```sh
cd /workspace/kdp-publishing
python scripts/validate_milestone.py
```

To regenerate imported research, run `python scripts/import_week1.py`; this importer requires openpyxl, already installed in this workspace. The validator itself requires only Python standard library. No app, server, paid API or PDF generator is installed. CSV uses UTF-8 and blank cells for unknowns.

## Navigation
- docs/PROJECT_BRIEF.md: constraints and product hypothesis.
- docs/30_DAY_PILOT.md and docs/DECISIONS.md: milestones and decision gates.
- docs/RESEARCH_METHOD.md, research/evidence_gaps.md: evidence protocol and blockers.
- research/niche_scorecard.csv: arithmetic-audited source scores and weights; subjective inputs.
- research/competitors.csv: 18 source works / 20 market observations with provenance.
- research/IMPORT_AUDIT.md: source hashes, formula audit and normalization limitations.
- books/book-001/blueprint/: provisional 64-page editorial design.
- docs/PRODUCTION_PLAN.md: deferred Python production requirements.

## Next steps
Source import is complete. Collect at least 10 closely comparable US and 5 relevant Canadian listings with evidence. Verify species facts and official KDP requirements. Then approve or revise the blueprint before illustration or generator work. Budget remains unspent by this task.

## Milestone 1A — 2026-11-11
Manual capture workflow is ready; verification remains incomplete (0 US / 0 CA independently verified bird listings). Fresh public probes remained proxy-denied. Use [capture guide](research/marketplace/CAPTURE_GUIDE.md) and research/marketplace/capture_template.csv for 10 US and 5 CA paperbacks; all prior source data is preserved. The append-only importer validates captures, archives supporting files and flags duplicates/conflicts without promoting them to verified evidence. See research/marketplace/RECOMMENDATION.md: CONDITIONAL GO unchanged, scores unchanged. Missing current Amazon prices/ranks/ratings, edition metadata, age/feature evidence, customer feedback and official KDP costs still block a stronger recommendation.
