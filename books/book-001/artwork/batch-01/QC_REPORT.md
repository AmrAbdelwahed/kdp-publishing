# Five-bird batch 01 — review report

**Status: stop for joint human review.** Five original AI candidates were generated with the user's visually approved revised cardinal PNG as the actual image reference. The reference's aesthetic was accepted by the user; its scientific and print checks are still open. No candidate is approved for scientific accuracy, print or release. Classifications below are preliminary visual triage, not automatic acceptance. No image was classified REGENERATE_REQUIRED because each concern could potentially be addressed with targeted work; that choice is for review.

| ID / species / intended pages | Preliminary class | Main issue for review |
|---|---|---|
| B02 Blue Jay, 4–5 | NEEDS_TARGETED_CORRECTION | Body and pose remain too cardinal-like for the user's stated distinction. The collar is filled black; check bill/head/tail proportions and jay marks against a field guide. Source/vector region count differs by one; label-overlap screening suggests a possible joined area around the tail/fence region. |
| B03 American Robin, 6–7 | NEEDS_TARGETED_CORRECTION | A continuous clear boundary for the orange underparts is not apparent; the face/neck has a scalloped contour. Check feet and leg attachment. Source/vector enclosed-region count differs by one; a possible joined area is near a foot. |
| B04 Black-capped Chickadee, 8–9 | READY_FOR_HUMAN_REVIEW | Compact, left-facing body and outlined cap/cheek/bib look distinguishable at overview scale. A reviewer still needs to check those boundaries, toe grip, lookalikes and line thickness. Equal region counts do not prove correctness. |
| B07 White-breasted Nuthatch, 14–15 | NEEDS_TARGETED_CORRECTION | Head-down trunk pose is distinct. The cap is solid black rather than colourable, and the trunk runs off the top and bottom of the source image. Added padding prevents the SVG reaching the page edge but cannot restore the missing ends of the scene. Check bill, tail, head and grip. |
| B13 Mourning Dove, 26–27 | READY_FOR_HUMAN_REVIEW | Small head, long pointed tail and different fence composition appear distinct. Check the facial spot, feet, wing/tail and small seedhead areas. Source/vector coarse region count differs by one; inspect whether tracing created a tiny region. |

The actual cardinal reference is used on pages 2–3 in the provisional proof. Its prior review records potential merged foot/branch spaces and unverified anatomy/line thickness. The style is visually accepted, but its technical concerns remain. The proof includes all five candidates, including those marked for correction, so the user can compare the batch together. Their presence is not approval or a claim they are accepted into the final book.

## Trace and print screening
Original PNGs are preserved under `originals/`. `processed/Bxx-v1/` contains its vector-only SVG, vector PDF and `quality.json`. Generation prompts, style-reference path/hash, original and vector hashes and approval status are in `manifest.json` and `generation-prompts.json`. The image tool supplied no model identifier, seed or exact generation timestamp; processing timestamps are separate and not misrepresented as generation times. Each image was prompted with the actual supplied PNG, not a textual description alone.

All five originals are approximately 1121–1122 × 1402–1403 px. After adding 80 pixels of white padding and fitting proportionally to the existing 507 × 435 pt placement box, the original raster sampling works out to about 258.5–258.7 effective PPI. This is below the user-reported 300 PPI threshold for raster use. The SVGs contain actual paths rather than embedded PNGs and can scale, but do not recreate source detail. Added padding is not new detail and cannot restore clipped content.

| ID | SVG paths | Source / trace enclosed white areas ≥25 px | Local-maximum samples below 0.75 pt | Source edge flag |
|---|---:|---:|---:|---|
| B02 | 2 | 32 / 31 | 2.68% | no |
| B03 | 2 | 35 / 34 | 4.54% | no |
| B04 | 4 | 22 / 22 | 2.96% | no |
| B07 | 15 | 27 / 27 | 3.26% | yes |
| B13 | 13 | 44 / 45 | 6.93% | no |

The topology count is coarse: a changed count flags a possible merge/split and equal counts do not prove closed colouring regions. For B02 and B03 an additional label-overlap screen suggests a possible merge, but anti-aliasing and threshold effects mean human inspection is required before asserting an actual defect. Stroke screening uses a distance-transform local-maximum approximation at the actual padded placement; its percentage is **not** the fraction of failed strokes. Corners and endpoints can trigger false positives. These are filled outlines, not uniform-width strokes, so the 0.75 pt minimum remains unproven. No candidate was rejected on that heuristic alone. The source/trace side-by-side sheet permits magnified manual inspection.

No pair has an identical source hash. A coarse 64-bit difference-hash screen detected no pair within ten bits, including the master cardinal. This does not detect every stylistic copy: the Blue Jay remains visibly too cardinal-like despite not triggering the screen. Page placement uses the existing mirrored safe-box layout; the original nuthatch crop still needs a compositional decision. Pale seams around placed SVG boundaries have appeared in prior proofs and should be checked at actual print size. Actual font licensing and KDP preview remain open.

## Evidence and next gate
On 2026-11-15 02:16 UTC direct requests to Cornell's five species `/id` pages all received proxy tunnel 403 before source content was retrieved. The user previously supplied externally checked robin and chickadee cues, but individual generated anatomy was not verified by that report. Blue Jay, White-breasted Nuthatch and Mourning Dove details, all range/season claims, activities, actual printing costs, and any review of individual output images remain pending. Do not infer sales or demand from this batch.

Review the five images as a set. Decide whether to adjust the master template or perform targeted changes to the three flagged candidates; visually inspect toes, field marks, outlines, margins, colouring space and line thickness at actual print scale. Then decide whether to authorize the remaining 24. User has not approved that next batch. No PDF upload, proof order, purchase or 30-bird generation took place.
