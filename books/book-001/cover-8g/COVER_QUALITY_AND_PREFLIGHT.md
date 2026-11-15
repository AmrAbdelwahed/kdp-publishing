# B1 replacement scene — review, not print approval

**Recommendation: REVISE / HUMAN REVIEW.** The 4× Real-ESRGAN candidate is the provisional sampling-density candidate for inspection; it is not a recovered original, approved artwork or an assurance of KDP print quality. It has been integrated without changing the established text, banner coordinates, back cover or KDP template geometry. The **new scene itself changes the approved B1 composition**, and the AI reconstruction makes fine details more assertive. A human must decide whether those changes are acceptable at actual size.

## Effective image resolution

| Scene in the same 8.5 × 6.9608-inch placement | Stored native/output pixels | Effective PPI at placement |
|---|---:|---:|
| Previous 8F B1 scene | 1102 × 903 | 129.65 × 129.73 |
| New user-supplied source | 1386 × 1135 | 163.06 × 163.06 |
| Real-ESRGAN x4plus output | 5544 × 4540 | 652.24 × 652.23 |

The candidate's output sampling exceeds 300 PPI; its input only contained the 1386 × 1135 source pixels. The model **predicts** additional detail and may invent it. Neither the higher number nor ordinary output resolution proves optical detail, anatomy, rights or print suitability. No interpolation was used to produce the 4× model candidate. Image DPI metadata does not determine these numbers; the actual embedded pixel dimensions and PDF image placement were measured.

## Composition and detailed inspection

The new source retains a red cardinal, magnifying glass, notebook, binoculars, and the green/gold palette, but compared with 8F its magnifier is larger and higher, the earlier long curved gold/cream separator is lost, foliage is denser, and the binoculars are larger and cut by the lower/right trim. The existing title panel covers a small portion of the top of the scene. The source was placed in the original image box without repositioning the title or changing the crop/scale. The new visual balance and edges require the user's approval; essential subject clearance and trim tolerance require physical review.

In the paired digital comparisons the candidate preserves the broad source silhouette, long tail, thick bill, crest, black face/throat, wing, branch, feet, magnifier and binoculars. The model enhances very fine light/dark strokes in crest, face edge and wing; these stronger, sometimes shiny or hairlike lines are model-generated interpretations, and the bark/foot textures also become more pronounced. The source itself leaves parts of the toes and branch grip hard to resolve. No expert anatomical approval is claimed, and no detail can be assumed biologically correct merely because it is sharper. Cornell's [Northern Cardinal identification page](https://www.allaboutbirds.org/guide/Northern_Cardinal/id), directly accessed for the prior 8E review on 2026-11-15, supports the broad red plumage, thick bill, crest and dark facial area; a knowledgeable reviewer must assess the actual pose, bill, feathering and feet.

A targeted view across the x=768/y=576 source-pixel tile junction showed no obvious straight seam at the inspected screen scale. A coarse diagnostic compared boundary gradients against the source after **diagnostic-only** 4× downsampling; average boundary differences were close to adjacent bands. This limited screen/aggregate check cannot exclude localized stitching, halos, ringing or artificial texture in the 48-tile result. The model strengthens thin edges and highlights; review all six [paired detail pages](enlarged-detail-comparison-REVIEW.pdf), particularly bright filaments around the mask, feather edges, toes, lens rims and notebook. No physical print or calibrated 100%-size visual check has occurred.

## Template, fonts and output

The review wrap remains 1252.377 × 810 pt, matching the earlier formula-derived drawing of 17.394128 × 11.25 inches; no spine text or template guide marks were added. The supplied template's PDF MediaBox is 1252 pt wide, 0.377 pt narrower than its drawn/formula width, and KDP Previewer confirmation remains open. Barcode zone and text-safe geometry use the prior template coordinates. The DejaVu font subsets are embedded, with no unused Helvetica; the PDF source and candidate rasters are RGB with no image soft mask, and each is embedded losslessly using the original PNG's Flate stream and predictor. Pixel identity with both respective PNGs is automatically checked. RGB/CMYK handling, flattening, legal rights, source-image rights and AI disclosure require final human/KDP review.

## Review files

- `assets/source-original.png`: exact PNG from user commit e40a32d; source dimensions and SHA-256 verified.
- `assets/realesrgan-x4plus-candidate.png`: lossless model output, SHA-256 `834567be0f1311c371b59cdbaf621ae3f0810beef480b7eb4c9b96833121f0a3`.
- `source-integrated-REVIEW.pdf` and `reconstructed-integrated-REVIEW.pdf`: full-wrap alternatives with identical vector layout; both unapproved. The latter is the provisional 4× candidate.
- `actual-size-comparison-REVIEW.pdf`: two letter-size pages showing the source and AI scene at the exact 8.5 × 6.9608-inch placement. Print at Actual Size/100%; a home printer may clip edges. The separate `source-front-back-actual-size-REVIEW.pdf` and `reconstructed-front-back-actual-size-REVIEW.pdf` show each integrated front and back at trim size.
- `enlarged-detail-comparison-REVIEW.pdf`: six labeled, same-size source/model detail pairs. `composition-comparison.png` compares the previous B1 front, new source and reconstruction.

## Remaining gates

1. User reviews the composition changes and whether binocular/handle and magnifier cropping are acceptable; do not treat the frozen layout check as approval of changed artwork.
2. Inspect the source and candidate on actual-size local prints, and have a knowledgeable reviewer check source/model anatomy, fine-feather invention, halos and all tile seams. Evaluate whether the 4× candidate or another genuinely detailed source is appropriate.
3. Confirm source/model/font commercial-use rights and KDP AI-generated-content disclosure; review interior artwork, science and age-suitability blockers independently.
4. Resolve the template page-box difference, current color handling and barcode safety, obtain human sign-off and perform KDP Previewer / physical-proof checks only when separately authorized. No KDP upload, proof order or publication has occurred.
