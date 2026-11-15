# Batch 2 quality and source review

**Status: human review required; no scientific, print or final artwork approval.** Six new originals were created, each using the accepted cardinal PNG as an image input for style. Prompts, reference hashes, original and vector hashes, and review statuses are in `generation-prompts.json`, `manifest.json`, and each `quality.json`. The generator did not report an exact model or generation time.

## Substantive issues to review

- **B05 Carolina Chickadee:** The silhouette and face are very close to B04; the bill and long legs need an independent reference check. A reader should not be asked to distinguish the two from this image alone.
- **B06 Tufted Titmouse:** The crest, facial boundary and pose look very close to the cardinal, undermining the requested species-specific silhouette. Check titmouse proportions and head marks; a targeted revision may be needed.
- **B08 Red-breasted Nuthatch:** Compare the outlined head stripes and compact form with a reliable source and with B07. The tree approaches the original canvas edge; the added white padding creates page clearance but cannot restore scene detail.
- **B09 Downy and B10 Hairy Woodpeckers:** Compare bill-to-head proportions and check actual facial and wing markings. Both contain filled dark bands that are not colourable. Their trunks approach the source edge. B09's drawn bill is shorter than B10's, but that does not verify identification.
- **B11 Red-bellied Woodpecker:** Check the cap/nape outline, back barring, tail and feet against a reliable reference. The tree approaches the source edge.
- **Prior-batch backlog:** B03 robin needs the orange-underparts boundary corrected; B02 jay necklace and wing bars still need reference verification. Their visual direction has been accepted, not their scientific or print accuracy.

## Trace and layout screening

Each SVG contains actual paths and no embedded raster; vector PDF artwork was inserted into the provisional proof. The pipeline added 80 pixels of white padding and removed tiny speckles after thresholding. All six source images are 1122 × 1402 pixels. The source sampling at the padded final-art placement is approximately **258.5 ppi**; vector scaling smooths traced contours but does not recover original detail. The padding may make truncated backgrounds less obvious without repairing them.

B06 and B11 each show a one-region change in the coarse enclosed-white-region screen; the other four counts match. This is a signal to inspect the outlines, not proof of a broken or closed colouring boundary. The local stroke-width screen reports small sub-0.75-point maxima in every image; it is an inconclusive raster-derived heuristic, not proof that every printed line meets 0.75 pt. Inspect original versus vector, print at actual size, and check eyes, bills, toes, fine feather lines, intended enclosed areas and line continuity. Smoothness, shape preservation, line thickness and final colourability remain human decisions. No image was rejected solely on a heuristic.

The 24-page review is a *selection*, not a complete interior. Each illustration precedes its matching activity; intended master page numbers are shown in the footer. The PDF requests facing-page viewing, with illustrations on intended even (left) pages. The selection begins with an intended even page; for physical duplex facing-page review, print with a blank first side so each illustration lands on the left. The approved 64-page master plan is unchanged. This document is not a KDP-ready interior; final font, margins, resolution, facts, page assembly and physical print remain to be checked for the completed book.

## Source and range limitations

All six were already listed in the proposed North American plan. The list alone is not independent verification of range, season, or identification details. On 2026-11-15 UTC, requests to all six Cornell ID pages failed with `Tunnel connection failed: 403 Forbidden`; `source-attempts.json` records each direct URL and timestamp. Consequently the cap, bib, eyebrow, stripe, bill proportions, barred patterns, anatomical details, and similarities mentioned in the prompts and shown in the illustrations **have not been checked against those sources**. No photo was copied or traced. Before publication, a knowledgeable reviewer should check each page, distribution and seasonal occurrence using the linked guides and a regional field guide, especially lookalike chickadees, nuthatches, and woodpeckers. Do not imply that any species occurs in every North American backyard or season. The plan is retained pending that check; no basis for a species replacement was independently established.

## Human review

1. Compare the 12-bird contact sheet and especially the lookalike pairs; decide whether B05 and B06 need targeted changes and whether the dark filled B09/B10 areas are acceptable.
2. Use the Cornell links when accessible to check identification marks, natural anatomy, size relationships, and regional/seasonal caveats. Record evidence; do not rely on a single drawing for similar species.
3. Print the 24-page selection at actual size, inspect the original-versus-vector sheet and individual SVGs, and test line thickness and colouring regions. Inspect activity text and paper margins.
4. Record separate visual, scientific and print decisions. Hold all artwork unapproved until those decisions have actually been made.
