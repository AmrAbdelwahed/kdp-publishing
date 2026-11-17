# Pre-publication corrections and Previewer handoff — 17 November 2026

**Status: CONDITIONAL — existing PDFs are technically prepared review candidates; scientific, rights, colour, physical-print and publication approval remain open.** The user froze the 64-page interior and B1 Cover A, retained all 30 visual illustration candidates and asked for only confirmed material corrections. The user also clarified that they believe the artwork was all provided by ChatGPT and did not supply separate human artwork-review decisions. The repository records OpenAI/ChatGPT image generation or editing, plus Real-ESRGAN reconstruction of the selected cover. Human visual acceptance is not independent scientific, rights or physical-print approval.

## Decisions and corrections

The existing repository and prior conversation were reviewed; no later human scientific, physical-print, rights or CMYK approval records were identified. The user's prior visual acceptance of the collection and frozen designs is recorded in `ARTWORK_APPROVAL_REGISTER.csv`; all previously pending expert and print decisions remain pending. The user's confirmation of AI-generated images and some final wording, and the unresolved Blue Jay photograph source, are carried into `RIGHTS_APPROVAL_REGISTER.csv`. These registers document available evidence rather than inventing approvals. The former 16-item artwork register and full rights checklist remain unchanged in `../release-10/`.

The four priority concerns remain the Robin's coloring boundary (page 6), Mockingbird wingbars (58), Blue Jay wingbar (4) and Eastern Bluebird face/breast boundaries (60). The woodpeckers and other inherited fine-line/coloring questions remain on the register. **No new human-confirmed material correction was supplied or found.** Accordingly, no artwork was speculatively edited and no PDF was regenerated. The accepted visual designs and original files remain unchanged. The existing page 64 font-credit sentence was already corrected in Milestone 10; no further change is established by the present evidence.

## Files and checks

The unchanged [interior candidate](../release-10/interior-release-candidate.pdf), [CMYK B1 full-wrap candidate](../release-10/cover-b1-a-cmyk-release-candidate.pdf), [RGB/CMYK comparison](../release-10/rgb-vs-cmyk-front-comparison.pdf) and [physical review packet](../release-10/physical-review-packet.pdf) remain the concrete handoff files. The original RGB cover and AI source art are separately preserved. The 20 recorded source/output SHA-256 values in `../release-10/MANIFEST.json` all matched on this review.

On 17 November 2026, all **48** repository tests and `scripts/validate_milestone.py` passed with the existing VTracer tool path; Ghostscript's null renderer processed both candidates successfully. The tests include 64 individual letter pages, embedded fonts, text and vector safety bounds, no PDF Info/XML metadata or annotations, old woodpecker-art object removal, text/cover placement, cover dimensions and barcode/spine clearance. B09/B10 pages were additionally compared against the frozen review at 144 DPI and rendered identically. These are digital checks, not a physical print or scientific certification.

The cover measures 1252.377 × 810 pt, uses a 4408 × 3612 DeviceCMYK image at approximately 518.6 output-sampling PPI, and follows the formula-derived 17.394128 × 11.25 in wrap. The 0.3772 pt difference from the supplied template PDF MediaBox remains unresolved. The chosen SWOP CMYK condition remains provisional and shifts the screen colors; it is not confirmed as KDP's actual print condition. AI-upscaled pixels do not represent equivalent original detail. See `../release-10/COLOR_COMPARISON.md` and `../release-10/PREFLIGHT_AND_BLOCKERS.md`.

## Open gates before submission and publication

1. Obtain or record a knowledgeable scientific/coloring review of the priority birds and other unresolved illustration questions; only make a specific correction if a material issue is confirmed.
2. Resolve artwork input and similarity rights, Blue Jay photo provenance, Real-ESRGAN model-weight terms and font-notice handling. Prepare disclosure of AI-generated images and user-confirmed AI-generated text according to the current KDP form.
3. Decide the cover color treatment and resolve the template page-box discrepancy with a fresh KDP template or KDP guidance; inspect color, detail and trim in Previewer and a physical proof.
4. Obtain age-appropriate feedback and real print/proof review, including fine lines, coloring spaces, text, cover, binding, spine and gutter. The user reported not having a printer; no physical approval has been recorded.

Only after separate user authorization may the files be uploaded to KDP Print Previewer; ordering a paid proof and publishing likewise need authorization. This review did not perform any of those actions or incur expense.
