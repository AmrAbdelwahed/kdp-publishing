# Milestone 8G — blocked pending original artwork

The user displayed a new B1 scene named `Nature Observation Kit with Cardinal.png` and reported 1386 × 1135 native pixels. The image is visible in the conversation but no corresponding source file or attachment identifier was made available in this workspace on 2026-11-15. The PNG has **not** been imported, hashed, reconstructed, or integrated. The user-supplied dimensions have not been independently verified. Do not replace it with a screenshot or a visually similar regenerated image; those would not preserve its original bytes or provenance.

At the existing 8.5 × 6.9607568-inch scene placement, the reported dimensions would be **163.06 × 163.06 effective PPI**. A hypothetical, exact 4× output would be 5544 × 4540 pixels, approximately **652.24 × 652.23 PPI** at that placement, but such a file has not been produced and the figure would describe output sampling, not recovered original detail or print approval. Anatomical accuracy, fine details, ringing, hallucination, borders and composition remain unassessed for the actual file.

## Open-source tool check

The official [Real-ESRGAN v0.2.5.0 Ubuntu release](https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.2.5.0) was downloaded to temporary storage. Its `realesrgan-ncnn-vulkan` executable returned `vkCreateInstance failed -9` and `invalid gpu device` in this environment; no Vulkan device was available. No interpolation was substituted.

A CPU capability smoke test **did** succeed with the BSD-3-licensed `ncnn` Python package 1.0.20261020 and the official `realesrgan-x4plus` model from that release, with Vulkan disabled. A 32 × 32 crop from the **old 8F scene** became a 128 × 128 model output in about 0.21 seconds. This was only a tool test, not a test on the new image, a full-image tiled run, a quality assessment, or an approved reconstruction. Both the package and model currently live in `/tmp` and are not committed.

Reproducibility identifiers:

- Official archive SHA-256 `e5aa6eb131234b87c0c51f82b89390f5e3e642b7b70f2b9bbe95b6a285a40c96`.
- `realesrgan-x4plus.bin` SHA-256 `713ee713b0353afaa27976f0563a64a5043bd70b9bd8936c2e26e25ebcdbcddf`.
- `realesrgan-x4plus.param` SHA-256 `35330ececcea33b6c397a72548e788d5d53becee4734c50b7fada36e89f10a86`.

## Free local alternative

On a computer with a working Vulkan GPU, use the official release for its operating system and follow its README. From the extracted directory, an example is:

```sh
./realesrgan-ncnn-vulkan -i 'Nature Observation Kit with Cardinal.png' -o 'candidate-x4.png' -n realesrgan-x4plus -s 4 -t 128 -m models
```

Keep the original unchanged. Verify the program and model's current license/terms for commercial use. A GPU implementation and the CPU inference route can behave differently; either needs a real source-versus-output review. Inspect the result at the actual PDF placement and in enlarged crops, including crest, mask, bill, wings, toes, tail, lens rims, notebook and binoculars; check for invented detail, seams, ringing and artificial texture. Fourfold pixel count is not a scientific, quality or KDP approval.

## Work still blocked

An accessible original PNG is required before preserving its bytes and SHA-256, comparing its composition, performing a meaningful reconstruction, integrating it into a new cover PDF, or producing the requested comparisons and preflight. Attach the actual PNG as a file or commit it to the repository and provide the path/commit. The prior B1 cover, official template and interior remain unchanged; no KDP upload, proof or publication occurred.
