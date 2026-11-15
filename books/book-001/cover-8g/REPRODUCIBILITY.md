# Reconstruction provenance and reproduction

- User-supplied source: `Nature Observation Kit with Cardinal.png`, obtained byte-for-byte from [GitHub commit e40a32d](https://github.com/AmrAbdelwahed/kdp-publishing/commit/e40a32d19ce813c4ab7fc657a36058d8ae234853); recorded git blob `5019557820db2b0c44967c3c3ac232ba9e058bc3`; SHA-256 `592a55d6849e1bea6bc43d4b6c61d7b30122ffbad982c3afb4b3950c4923de79`. `assets/source-original.png` is identical, RGB 1386 × 1135. The user described it as newly generated; the creation tool and commercial license have not been independently established.
- Model: `realesrgan-x4plus` weights and parameters from the official [Real-ESRGAN v0.2.5.0 Ubuntu release](https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.2.5.0). The release archive, model `.bin` and `.param` SHA-256 values are recorded in [the original tool check](STATUS_AND_TOOL_CHECK.md). The [Real-ESRGAN code license](https://github.com/xinntao/Real-ESRGAN/blob/master/LICENSE) is BSD 3-Clause; a human must review applicable model, source-art and downstream commercial-use rights.
- Inference: `ncnn` Python 1.0.20261020, CPU, four threads, 192-source-pixel tiles and 32-source-pixel context around each tile, center cropped and joined, native 4× model output. No interpolation is used to create the candidate. The Vulkan executable reported no usable GPU. Output pixels are model predictions and can add or change details; no recovered original information or biological fidelity is claimed.
- A local environment with Pillow, NumPy, and the compatible `ncnn` package can reproduce the run with the official `.param` and `.bin` files, for example:

```sh
python scripts/reconstruct_cover_8g.py \
  books/book-001/cover-8g/assets/source-original.png \
  /tmp/bird-cover-reconstruction.png \
  --model-dir /path/to/official/realesrgan/models
```

The utility refuses to overwrite the output path. Model weights and temporary Python dependencies are not stored in the repository. Different machines or versions can differ; inspect and record each output and any tile seams. `scripts/build_cover_8g.py` reuses the existing vector layout to make review PDFs and comparison previews from the preserved source and candidate. Human review, rights and AI-content disclosure, KDP Previewer and a physical print remain outstanding.

Candidate output: `assets/realesrgan-x4plus-candidate.png`, RGB 5544 × 4540, SHA-256 `834567be0f1311c371b59cdbaf621ae3f0810beef480b7eb4c9b96833121f0a3`. The PDF writer reuses the PNG's lossless IDAT data with PDF FlateDecode/PNG predictor, avoiding ASCII85 expansion; tests verify that pixels extracted from each full-wrap PDF exactly match its corresponding PNG. Screen thumbnails and diagnostic downsampling are display/analysis only and are not the model input, candidate, or print raster.
