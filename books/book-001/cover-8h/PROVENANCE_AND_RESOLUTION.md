# Candidate provenance and effective resolution

The scene placement is the same **8.5 × 6.9607568 inches** in both covers. PPI is measured from the embedded raster dimensions and placement, not from DPI metadata.

| Candidate | Source pixels | Source PPI | Real-ESRGAN ×4 pixels | Output-sampling PPI |
|---|---:|---:|---:|---:|
| A — original 8F B1 scene | 1102 × 903 | 129.65 × 129.73 | 4408 × 3612 | 518.59 × 518.91 |
| B — user replacement from 8G | 1386 × 1135 | 163.06 × 163.06 | 5544 × 4540 | 652.24 × 652.23 |

Both outputs exceed 300 PPI in *sampling density*. They contain model predictions, not newly captured original detail. Those numbers do not establish image fidelity, biological accuracy or print quality.

A source is the unchanged [8F native crop](../cover-8f/B1-scene-native-crop.png), SHA-256 `3627d8fa6d1f0be90968f56368222db4635ce4e2e16096d8c1686b40e54ff365`. A's separate reconstructed image is `assets/B1-original-realesrgan-x4.png`; its hash is recorded in the assessment. B is the unchanged [8G output](../cover-8g/assets/realesrgan-x4plus-candidate.png), SHA-256 `834567be0f1311c371b59cdbaf621ae3f0810beef480b7eb4c9b96833121f0a3`, derived from the user image in commit e40a32d. [8G provenance](../cover-8g/REPRODUCIBILITY.md) records the original source, software, model hashes and licensing references.

A uses the same `scripts/reconstruct_cover_8g.py` CPU pipeline and official Real-ESRGAN x4plus weights as B: four threads, 192-source-pixel tiles with 32-pixel context, model inference at 4× and no interpolation. The source and model binaries are not overwritten. A/B composition is placed in the same template-derived raster box; title, banner, supporting text, back cover and layout are identical. User review, artwork and font rights, model/source AI disclosure, color handling, anatomy, template page-box discrepancy, local printing and KDP Previewer remain open.

A's reconstructed PNG SHA-256 is `f0eb54a3d26280179360651a9d41115f2e6258634d4b20eba85b023bc3b67bad`. The original A and B assets are unchanged. At approximately 23:12 UTC on 2026-11-15, [Cornell's Northern Cardinal identification page](https://www.allaboutbirds.org/guide/Northern_Cardinal/id) returned HTTP 200 and described a short, very thick bill, prominent crest and black face around the bill. That supports only broad identification cues; it does not independently approve either drawing's anatomy.
