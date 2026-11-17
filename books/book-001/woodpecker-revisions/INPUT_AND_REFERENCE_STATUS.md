# Woodpecker revisions — historical source-file blocker

**Resolved:** The user supplied the original files in commit `18e7336`. See `REVIEW_REPORT.md` and `ARTWORK_REVISIONS.json` for the current review. The text below preserves the prior state.

The user visually accepted two replacement illustrations for B09 Downy and B10 Hairy. Both are displayed in the chat, but the original PNG files were not mounted in the workspace or found in the existing repository when checked on 2026-11-17 UTC. No original PNG bytes, hashes, source provenance, or reliable filename-to-image mapping could be verified. The inline display is not a substitute for the source files: a screenshot, redrawing or regenerated image would not preserve the originals.

**Material blocker:** The two source PNGs are required before importing new revisions, tracing them, validating their coloring regions, replacing pages 18 and 20, or resolving the B09/B10 issue-register entries. No artwork, interior, cover or approval status has been altered. No new SVG or review interior is claimed.

## Evidence ready for the eventual review

- Cornell [Downy Woodpecker ID](https://www.allaboutbirds.org/guide/Downy_Woodpecker/id), directly retrieved HTTP 200 on 2026-11-17 at 05:19:03 UTC, describes a proportionally small bill, white-checked black wings and a boldly striped head.
- Cornell [Hairy Woodpecker ID](https://www.allaboutbirds.org/guide/Hairy_Woodpecker/id), directly retrieved HTTP 200 on 2026-11-17 at 05:19:03 UTC, describes a straight bill nearly as long as the head, black wings checked with white and head stripes. Size and bill length are comparative cues, not a substitute for expert identification.
- The first displayed image appears longer-billed than the second. The actual source filenames and visual content must be cross-checked on import; this observation does not assign a filename or confer scientific approval.
- Existing interior page 19 teaches a checked-wing pattern; page 21 says a striped head and checked wing with a hidden bill do not alone settle the species. These are the intended activities; consistency with the new art cannot be validated until its source files are available.
- The existing `scripts/process_bird_batch.py` / `scripts/vector_recovery.py` tracing workflow is present. VTracer 0.6.15 was importable through `PYTHONPATH=/tmp/kdp-vector-tools` at this check. The pipeline's regional and line-width metrics do not by themselves prove anatomical accuracy, closed coloring spaces or physical-print suitability.

The user has granted **visual-candidate approval**, not scientific or physical-print approval. Once the files are available, retain them byte-for-byte, record hashes and provenance, trace as new revisions, inspect source versus vector at actual placement, update only the two illustration pages and issue records, verify pages 19/21 remain consistent, and run the relevant tests.
