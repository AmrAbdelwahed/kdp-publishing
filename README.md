# KDP Publishing — research and editorial planning
Original, AI-assisted children's colouring/activity books. First candidate: **Backyard Bird Detectives: Color, Spot & Explore**, ages 6–9. US and Canadian paperback markets; low-cost print-on-demand pilot November 10–December 9, 2026.

## Status
**Milestone 4: 18 bird candidates are available for review.** The user kept the earlier visual directions, with the Downy and Hairy Woodpeckers provisional; the titmouse has a new unapproved v2 and six new species await review. See `books/book-001/artwork/batch-03/` for the 36-page selection, candidate manifest, provenance and scientific backlog. All scientific and print approval remains pending; market demand and current KDP rules remain unverified.

## Setup and validation
Use the existing checkout. Python 3, no extra packages or secrets required for the current documents and CSV validator:

```sh
cd /workspace/kdp-publishing
python scripts/validate_milestone.py
```

To regenerate imported research, run `python scripts/import_week1.py`; this importer requires openpyxl, already installed in this workspace. The validator itself requires only Python standard library. Prototype PDF scripts are available; no full 64-page production generator, server or paid API is required for this work. CSV uses UTF-8 and blank cells for unknowns.

## Navigation
- docs/PROJECT_BRIEF.md: constraints and product hypothesis.
- docs/30_DAY_PILOT.md and docs/DECISIONS.md: milestones and decision gates.
- docs/RESEARCH_METHOD.md, research/evidence_gaps.md: evidence protocol and blockers.
- research/niche_scorecard.csv: arithmetic-audited source scores and weights; subjective inputs.
- research/competitors.csv: 18 source works / 20 market observations with provenance.
- research/IMPORT_AUDIT.md: source hashes, formula audit and normalization limitations.
- books/book-001/blueprint/: provisional 64-page editorial design.
- books/book-001/artwork/batch-01/: six-bird provisional proof, five new candidates, visual reference, QC and schedule.
- docs/PRODUCTION_PLAN.md: deferred Python production requirements.

## Next steps
Review the seven new images together and complete source and print checks before approving any additional production. The 36-page PDF is a selection, not a complete interior or demand validation.

## Milestone 1A — 2026-11-11
Manual capture workflow is ready; verification remains incomplete (0 US / 0 CA independently verified bird listings). Fresh public probes remained proxy-denied. Use [capture guide](research/marketplace/CAPTURE_GUIDE.md) and research/marketplace/capture_template.csv for 10 US and 5 CA paperbacks; all prior source data is preserved. The append-only importer validates captures, archives supporting files and flags duplicates/conflicts without promoting them to verified evidence. See research/marketplace/RECOMMENDATION.md: CONDITIONAL GO unchanged, scores unchanged. Missing current Amazon prices/ranks/ratings, edition metadata, age/feature evidence, customer feedback and official KDP costs still block a stronger recommendation.
