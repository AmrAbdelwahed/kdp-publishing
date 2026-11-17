# Milestone 10 release-candidate package

These files are for review, not authorized KDP submission or publication. The existing artwork, design and old review PDFs are preserved.

- `interior-release-candidate.pdf` — 64-page individual-page interior; only page 64's font-credit wording changed.
- `cover-b1-a-cmyk-release-candidate.pdf` — selected full-wrap cover converted to a provisional SWOP CMYK condition; the original RGB source is `../preflight-9/selected-cover-full-wrap-CANDIDATE.pdf`.
- `rgb-vs-cmyk-front-comparison.pdf`, `rgb-vs-cmyk-screen.png` and `COLOR_COMPARISON.md` — review the effect and limits of color conversion.
- `ARTWORK_DECISION_REGISTER.csv` — 16 priority and inherited findings with evidence, conditional actions and pending approvals.
- `RIGHTS_AND_DISCLOSURE.md`, `TEXT_AUTHORSHIP_INVENTORY.csv`, and `FONT_LICENSE.txt` — provenance, user-confirmed AI text/image disclosure and open rights questions.
- `physical-review-packet.pdf` and `PHYSICAL_REVIEW.md` — actual-size review handoff.
- `PREFLIGHT_AND_BLOCKERS.md` — technical checks, unverified requirements and remaining release decisions.
- `MANIFEST.json` — source and output SHA-256 hashes.

The PDFs were built with `scripts/build_release_10.py` and checked by `scripts/test_release_10.py`. Rebuilding requires the recorded installed Artifex sRGB and SWOP profiles. A subsequent rebuild may produce different file hashes even if rendering is unchanged; it must be revalidated and separately recorded.
