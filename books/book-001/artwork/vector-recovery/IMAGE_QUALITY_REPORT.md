# Print-size vector experiment — 2026-11-14 Toronto

**Recommendation: REVISE; no artwork is approved for production.** The three SVG files contain actual filled vector paths and no embedded raster images. The conversion yields smooth-looking curves at contact-sheet scale and the principal silhouettes appear close to the supplied originals, but it cannot recover missing anatomy or certify 0.75-point line thickness. Detailed human anatomy and colouring-boundary review is still required. No image is labeled REJECTED_FOR_VECTOR because this pass has not established specific conversion damage; this is not a technical or anatomical pass.

## Method and placement
The original AI-generated 1199 × 1312 PNG files remain unchanged; SHA-256 matches the existing source manifest. Threshold grayscale at <160, remove isolated black components smaller than 4 pixels, add 80 white pixels on every side without stretching, then trace with VTracer Python package 0.6.15 (SVG generator identifies its core as 0.6.12), binary spline mode, speckle filter 4, precision 2. The padded canvas is 1359 × 1472 px, fitted proportionally in the existing 507 × 435 pt image box. The original and vector comparison pages use the same padded canvas and placement. Padding reduces the source drawing's physical dimensions to about 89.1% of the prior no-padding placement; it is not extra image detail. At this reduced size the original effective resolution is about 244 PPI, still below 300. The vector paths are resolution-independent representations of thresholded pixels; they contain no additional anatomical information. The 300-DPI PNG exports are renderings of those paths, not restored source detail.

| Candidate | Paths | Source / vector enclosed white regions ≥25 px | Threshold-mask intersection-over-union | Screening samples below 0.75 pt | Preliminary disposition |
|---|---:|---:|---:|---:|---|
| Cardinal | 6 | 23 / 23 | 0.8798 | 3.17% | PROVISIONAL_REVIEW_REQUIRED |
| Robin | 5 | 40 / 40 | 0.8892 | 1.45% | PROVISIONAL_REVIEW_REQUIRED |
| Chickadee | 1 | 23 / 23 | 0.8951 | 1.18% | PROVISIONAL_REVIEW_REQUIRED |

The region count is a coarse connected-component comparison; equal counts do not prove all individual regions remain open or closed correctly. The overlap statistic compares thresholded masks at input-canvas resolution, and is not a perceptual or anatomy score. The line-width screening rasterizes paths, uses distance-transform local maxima and a pixel-based width approximation at 435 pt height. Percentages are the fraction of these samples below the externally supplied 0.75 pt figure, **not** the percentage of total strokes that fail. Endpoints, corners and antialiasing can produce false positives. The traces are filled contours, so no stroke-width property can certify the thinnest segment. Treat the warnings as a reason for print-scale inspection and correction, not a definitive measurement or pass.

## Candidate review notes
- **Cardinal:** crest, short bill, wing and long tail remain visible in both versions. The face/mask boundary and curled toe shapes require comparison with a reliable cardinal reference; neither the original nor the traced boundary is independently validated. The vector smooths pixel edges, but visually inspect crest points, beak junction, wing feathers and toes at 100% in the comparison PDF. Thin-line screening has the highest warning rate of the three.
- **Robin:** bill, round body, legs, wing and tail remain visible. The breast colour boundary and head appearance may not be sufficiently clear for identifying a robin in uncoloured line art; the branch has open ends already present in the original. Check toes, foot overlap, feather boundaries and all printable enclosures. The vector should not be credited with correcting source features.
- **Chickadee:** cap/cheek/bib regions and overall outline are retained, but those boundaries, bill and feet require expert visual review. Original ink was 7 pixels from the left edge; 80 pixels of added padding gives the traced image an approximately 87-pixel left inset (~25.7 pt at final placement), before the page image-box margin. It is no longer at the SVG canvas edge, but the art becomes smaller; assess colouring space and no-bleed page placement at actual size. Padding cannot recover any source content that was clipped before generation.

A side-by-side screen review found no obvious whole-part disappearance; detailed crops, actual-size prints and knowledgeable human review remain needed to detect subtle fusions, jaggedness or lost identification detail. Graphic minimums, contours and real-world readability have not been proven. The only image removed during threshold cleanup was 1 isolated cardinal pixel; no full part was intentionally removed. All 3 sources, threshold and parameters are recorded in measurements.json. Review art before changing any asset manifest approval.

## Artifacts
- `original-review-sheet.png`: original images, labelled.
- `original-detail-crops.png` and `vector-detail-crops.png`: enlarged heads/bills, wings, feet, and tails/edges.
- `original-vs-vector-sheet.png`: padded-source and vector render side by side.
- `*-comparison-print-size.pdf`: two US-letter pages with original then vector at identical placement; view/print at 100% with no fit-to-page scaling.
- `*-vector-300dpi.png`: 2550 × 3300 px letter-page render of vector comparison page; the embedded page label is part of the review output.
- `three-bird-provisional-vector-prototype.pdf`: six-page review proof with vector art inserted, separately from the approved-asset builder and clearly marked NOT APPROVED. Its art pages contain no raster images; DejaVu fonts are embedded. This is not a final KDP interior or approval.

The three SVGs are 54–74 KB, vector-only art PDFs 23–30 KB, and combined prototype about 1 MB or less depending on font subsetting; size does not establish print acceptance. Comparison PDF page 1 intentionally contains a PNG; page 2 contains vector paths. See automated tests for structural checks. The user-supplied KDP minimums are externally reported and not freshly verified by Codex.

## Production approach comparison
| Approach | Quality | Reproducibility and effort | Cost |
|---|---|---|---|
| A. Native high-resolution raster | Can give enough actual PPI, but anatomy, closed regions and line widths still need review; generation resolution may be limited. | Simpler file handling; output quality varies, and a larger pixel count alone doesn't prove true detail. | No extra subscription assumed; human review still costs time. |
| B. AI art then automatic vectorization | Smooth curves and small scalable files; existing anatomical defects remain and tracing can alter or merge fine details. | Batchable, but parameters and thresholds must be checked for every image; no guaranteed 0.75 pt minimum. | Free local tools; review time remains. |
| C. AI art, manual corrections, then vectorization | Best control over anatomy, field marks, boundary closure and thin areas; vectors still need a print-scale check. | More hands-on time and skilled review, with versioned originals and approved edits; trace settings can be repeated. | Free tools are available, but human effort is material. |

Recommend **C as the primary candidate workflow**, conditional on the three corrected examples passing human and print-scale review. Use A when a truly native high-resolution raster preserves anatomy and colouring spaces cleanly; retain it if vectorization introduces damage. Use B only for simple art whose trace and line thickness have been individually checked. No approach justifies automatically accepting generated anatomy or guarantees KDP approval. Do not start the 30-image run before the user approves a demonstrated process.

## Reproduce
With Python 3, Pillow, NumPy, SciPy and PyMuPDF installed, install the free `vtracer==0.6.15` wheel in a local environment and run `python scripts/vector_recovery.py`. This session installed it to `/tmp/kdp-vector-tools` with `python -m pip install --target /tmp/kdp-vector-tools vtracer==0.6.15`; run with `PYTHONPATH=/tmp/kdp-vector-tools`. Outputs are deliberately isolated under artwork/vector-recovery and do not alter candidate originals, approved artwork or the approved-asset manifest. The script uses PyMuPDF to render vectors; it redacts and replaces only illustration areas in a *separate* prototype copy.
