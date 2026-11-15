# Milestone 2B — six-bird review

**Scope:** one new Blue Jay and one targeted edit each for the robin and nuthatch. No other birds were generated. The user provisionally accepted the visual designs of B04 Black-capped Chickadee and B13 Mourning Dove, and continues to accept the cardinal as a visual style reference. These decisions do not certify anatomy, facts, print quality or KDP approval.

## Visual result

| Species | Current revision / editorial state | Review notes |
|---|---|---|
| Northern Cardinal | Existing master; visual style accepted | Source and vector unchanged. Prior possible foot/branch trace joins and facial-mask/line-thickness review remain open. |
| B02 Blue Jay | v2; NEEDS_TARGETED_CORRECTION | More horizontal, left-facing silhouette, longer barred tail and straighter bill make it visibly less cardinal-like. The necklace is still partly filled black instead of fully outlined; distinct wing bars need a field-guide comparison. Species accuracy and colouring-space/print checks remain open. |
| B03 American Robin | v2; NEEDS_TARGETED_CORRECTION | Ground pose and grass preserved; former scalloped neck is smoother. A clear separation of the orange-red underparts from darker upperparts is still not apparent, despite the prompt. Check feet/leg attachment against a reference. |
| B04 Black-capped Chickadee | v1; user provisionally accepted visual design | Original and traced candidate unchanged. Human scientific and final print review remain pending. |
| B07 White-breasted Nuthatch | v2; READY_FOR_HUMAN_REVIEW | Solid cap is now an outline; trunk has visible upper and lower ends with source whitespace. Head-down pose is preserved. Confirm cap boundaries, bill, feet/grip and scale against a field guide and at print size. |
| B13 Mourning Dove | v1; user provisionally accepted visual design | Original and traced candidate unchanged. Human scientific and final print review remain pending. |

The twelve-page proof includes the two flagged revisions so the user can assess the six together. The status label on each is informational, not acceptance into the final book. Review the Blue Jay's neck and wing pattern and the robin's underparts before treating them as complete.

## Source and reference provenance

The user-provided Blue Jay photograph was visible in the chat and informed the assistant's verbal description of an elongated body, tail, pointed bill, crest and necklace. It did not come with a workspace file or source/license metadata and was **not passed as a file to the image generator**, copied or traced. The actual cardinal PNG was supplied to the image tool solely as its visual style reference. For robin and nuthatch, the actual v1 source PNG was supplied as the first image for a targeted edit and the cardinal PNG as the second style reference. All input reference hashes and exact v2 prompts are in `revision-prompts-v2.json` and the processed quality records; the image tool did not report a model identifier, seed or exact generation time.

Direct requests to the user's three Cornell ID pages returned proxy tunnel 403 on 2026-11-15 02:33 UTC. The photographs/text were not independently retrieved from Cornell. Jay, robin and nuthatch anatomy remains pending a human check against legitimate sources. The blue-jay photo was not used to claim exact identification or copyright status. User-supplied external robin/chickadee cues from Milestone 1D remain recorded separately; those do not certify any generated drawing. Do not infer ranges or seasons from these revisions.

## Technical trace screening

| Revision | Source pixels | Raster effective PPI at padded placement | SVG paths | Source / vector enclosed white areas ≥25 px | Samples screened below 0.75 pt | Source edge warning |
|---|---:|---:|---:|---:|---:|---|
| B02 v2 | 1536 × 1024 | 240.9 | 4 | 27 / 27 | 2.17% | no |
| B03 v2 | 1122 × 1402 | 258.5 | 2 | 24 / 24 | 4.37% | no |
| B07 v2 | 1122 × 1402 | 258.5 | 11 | 29 / 29 | 2.33% | no |

All SVGs contain actual paths, no embedded source PNG; originals are preserved as `originals/Bxx-v2.png` and v1 files and v1 manifest entries remain intact. The raster PPI figures are below the user-reported 300 PPI criterion at the existing padded 507 × 435 pt fit. B02 is landscape and fits to the image-box width; B03/B07 fit to its height. SVG contours scale but do not recreate source detail. Eighty pixels of white padding retain page clearance; they do not supply content that was absent from the source.

The region counts are coarse; equal counts do not prove every colourable region is closed. The line screen is a distance-transform local-maximum heuristic at actual placed scale; percentages are **not** fractions of all printed lines, and endpoints/corners can trigger false positives. Filled vector contours have no single uniform stroke width, so a 0.75 pt minimum is not certified. No image was rejected solely on these figures. Inspect feet, feather separations, necklace and small areas at actual print size. The proof has faint boundaries around some SVG placements; check whether those are rendering seams before any final export.

## Layout and next gate

`review-2b/six-bird-provisional-proof.pdf` uses the existing 12-page layout: intended book spreads 2–3, 4–5, 6–7, 8–9, 14–15 and 26–27. The full 64-page sequence was not changed. Embedded DejaVu fonts, page size, artwork path structure, source hashes, statuses and layout checks are covered by automated checks, but the PDF is not a KDP submission and no physical proof has been ordered. Fact, line-width, range, font-license and final print reviews remain open.

The five-species set should be reviewed together, with special attention to whether a targeted Jay outline/wing correction and a Robin underparts boundary are needed. Human acceptance or a targeted editing decision is required; no print/scientific approval is inferred. The remaining 24 are still outside this milestone's authorization.
