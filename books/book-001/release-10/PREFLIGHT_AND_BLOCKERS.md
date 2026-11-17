# Release-candidate preflight — conditional, not approved for upload

The user froze the current design and retained all 30 visual candidates. The files in this directory are technically prepared **review candidates**, not scientific, legal, physical-print or publication approval. No KDP upload, proof order or publishing has occurred.

## Interior

`interior-release-candidate.pdf` contains 64 individual 8.5 × 11 in pages. From the woodpecker-revision review PDF, it keeps every page and current illustration, including B09/B10 v2, in the same order. The only visible change is the requested page 64 font-credit sentence; the false promise to see accompanying notices was removed, while the Cornell attribution and 30 names remain. The full font notice is separately preserved in this package for rights review. The two unreferenced prior woodpecker art forms were removed and garbage collected; the current vectors remain. Existing source files are untouched.

Automated checks compare every unmodified page against the review source at 72 DPI, and page 64 outside the credit sentence; inspect text, page dimensions, page order, embedded fonts, object removal, annotations and blank document metadata; and check both page text and vector drawing bounds against 0.375-inch page-edge clearance. Oversized existing font Unicode mapping blocks were split without changing mappings, and Ghostscript's null renderer processed all 64 pages. These checks cannot prove all minimum line weights, gutter tolerances on a bound book, physical usability or scientific accuracy.

## Cover

`cover-b1-a-cmyk-release-candidate.pdf` is the selected B1 A, with unchanged media box, typography positions, scene placement, image pixel dimensions, barcode exclusion and no spine text or visible guides. All fonts remain embedded and the image is losslessly represented in DeviceCMYK. Document information and XML metadata were removed. The source RGB cover and original art remain untouched. The output scene uses inferred AI-upscaled pixels: 518.6 PPI output sampling does not mean 518.6 PPI of original detail. See `COLOR_COMPARISON.md` for the SWOP assumption, measurable color changes and unresolved profile handling.

The candidate is **1252.37695 × 810 pt**, consistent with KDP's formula: 64 × 0.002252 in spine and 0.125 in bleed yields **17.394128 × 11.25 in**. The supplied KDP template labels 17.394 × 11.25 in and its drawing extends to 1252.3772 pt, but its MediaBox stops at 1252 pt; the 0.3772 pt difference is still unexplained. The candidate retains full formula-derived bleed rather than cropping. A new template or KDP clarification and KDP Print Previewer review are still required. KDP acceptance is not asserted.

## Remaining gates

1. A knowledgeable reviewer must decide whether the four priority field-mark/color-boundary issues need correction. The user accepted and retained the two woodpeckers, but their fine patterns, feet and scientific accuracy are still pending. `ARTWORK_DECISION_REGISTER.csv` records 16 prioritized and inherited findings with evidence and the smallest conditional action; it does not certify the other 14 birds.
2. Human scientific, regional/seasonal, age-fit and source review remains open for the full book. The 30 clue sources and answers were rechecked in `../final-review/CLAIM_AND_ANSWER_REVIEW.csv`; this is not full biological or educator approval.
3. Confirm rights, font-notice treatment, third-party inputs, the Real-ESRGAN weights and generated-output similarity; disclose the user-confirmed AI-created images and some final text as required. See `RIGHTS_AND_DISCLOSURE.md`. Do not treat this review as legal clearance.
4. Resolve KDP's template box and CMYK-profile guidance; review the candidate's visibly shifted color and reconstructed feather detail with a human. If a different printer condition is required, make a new candidate and recheck it instead of modifying this one in place.
5. Obtain real print/reader feedback. Only after separate user authorization, use KDP Print Previewer to check trim, bleed, gutter, spine, barcode, colors and all warnings; only after separate purchase authorization obtain a physical proof. `PHYSICAL_REVIEW.md` and `physical-review-packet.pdf` provide the handoff.
