# Final B1 scene comparison — recommendation for human review

**Recommend A: the original B1 scene reconstructed with Real-ESRGAN.** It best preserves the selected cover's intended composition: the gold/cream separator frames the heading, the notebook remains recognizable and the binoculars are less dominant and less tightly cropped. Its cleaner illustrated style also has a closer visual relationship to an activity book. This is a design judgment; it is not a claim that A will sell better, that the model recovered original detail, or that A is ready to print.

| Criterion | A — original B1, reconstructed | B — new replacement, reconstructed |
|---|---|---|
| Visual balance and commercial presentation | Keeps the approved field-guide composition and uncluttered transition below the heading; friendly graphic treatment. | More naturalistic foliage and larger, higher magnifier; visually rich but busier and changes the selected framing. |
| Cardinal and props | Cardinal remains the main focal subject; notebook and binoculars are visible and secondary. | Cardinal remains visible; larger binoculars compete more and are clipped at the lower/right edge. The title panel covers a little of the scene's top. |
| Thumbnail readability | Same vector title and banner as B. Main title reads well at 185 px; subtitle, age and lower line remain small. | Same typography and size; dense photo-like detail attracts more visual attention. No buyer test was performed. |
| Actual-size detail | Source 129.65 × 129.73 PPI; 4× model output 518.59 × 518.91 PPI. Sharper apparent lines are inferred, not recovered source detail. | Source 163.06 × 163.06 PPI; model output 652.24 × 652.23 PPI. Higher input and output sampling alone do not establish better print quality. |
| Anatomy and artifacts | Broad red plumage, crest, thick bill, facial mask and tail are plausible identification cues. The model strengthens streaks along the crest, face and wing; feet and feather anatomy need expert review. | Same broad cues; extra high-contrast hairlike detail along the face and wing and strongly textured details need review. Feet and branch grip remain hard to verify. |
| Trim and print | A's original composition keeps the binoculars more contained; the magnifier handle reaches the inner edge. Inspect print and binding tolerance. | Binoculars and scene detail meet the right/lower edge; the changed framing and crop need specific user approval. |

## A source versus reconstruction

The 4× output retains the source's overall crest, bill, wing, tail, feet, magnifier, notebook and binocular shapes in the screen comparisons. It adds emphasis to fine feather streaks, creates stronger light/dark edges and sharpens the eye and facial area; these are model interpretations and may look artificial at print size. The gold magnifier contour remains continuous in the inspected view, with stronger edge contrast worth checking for halos or ringing. The feet are small enough that a human should check the toes and branch grip against a reference. No independent ornithological approval has been obtained.

One model tile-junction region was visually inspected without an obvious straight seam at screen scale. A coarse diagnostic comparing candidate-versus-source boundary gradients with nearby bands found no large aggregate discontinuity; this does not rule out localized seams, ringing or invented details. The full image and actual-size print need human inspection. Cornell's [Northern Cardinal ID page](https://www.allaboutbirds.org/guide/Northern_Cardinal/id), retrieved HTTP 200 on 2026-11-15, supports a prominent crest, thick bill and dark face around the bill; it cannot certify this depiction or the model's feather details.

## What remains open

Print the actual-size front/back and detail pages at **100% / Actual Size**, with fit-to-page disabled; desktop printers can clip outer edges. No actual print or calibrated physical-size screen review has occurred. Review A's model texture, anatomy, rights and AI disclosure; check the original interior's outstanding scientific and print blockers separately. The review PDFs use embedded DejaVu fonts and RGB artwork, and retain no spine text, the template-derived barcode exclusion and the formula-derived wrap width. The supplied KDP template's MediaBox is 0.377 pt narrower than its drawn/formula width; color handling, KDP Previewer and physical-proof checks remain pending and require separate authorization where applicable. Neither candidate is publication-approved.

## Files

- [Full-size side-by-side fronts](full-size-front-comparison-REVIEW.pdf): each front is 8.5 × 11 in on a wider comparison page.
- [185-pixel thumbnails](thumbnail-comparison.png).
- [A original versus reconstruction, actual-size details](A-source-vs-reconstruction-details.pdf).
- [A versus B, actual-size details](A-vs-B-actual-size-details.pdf): each pair shows the same physical page region, so the birds appear at their respective positions.
- [A full-wrap review](A-full-wrap-REVIEW.pdf) and [A front/back at trim size](A-front-back-actual-size-REVIEW.pdf).
- [B full-wrap review](../cover-8g/reconstructed-integrated-REVIEW.pdf) and [B front/back at trim size](../cover-8g/reconstructed-front-back-actual-size-REVIEW.pdf).
- [Resolution and provenance](PROVENANCE_AND_RESOLUTION.md); both original scenes and both model outputs remain available.
