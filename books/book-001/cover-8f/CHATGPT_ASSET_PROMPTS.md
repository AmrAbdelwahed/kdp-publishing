# Exact replacement-art prompts and delivery specifications

Do **not** create a new full cover. The approved typography, back cover and design remain frozen. Attach [the existing B1 scene crop](B1-scene-native-crop.png) to ChatGPT @Create Image as the visual reference. An export advertised as 300 DPI, an ordinary enlargement, or interpolation of this existing 1102 × 903 crop does not provide new image detail. Request the dimensions below as **native generated pixels**. If the tool cannot supply that native resolution, retain its output as a reference and report its actual dimensions; do not upscale it and claim it meets the requirement.

## Preferred path: one registered detailed scene

Request a lossless PNG at **at least 2550 × 2089 native pixels**, approximately 1.2207:1 aspect ratio, for placement at **8.5 × 6.9608 in**, x=0 and y≈3.3146 in from the top-left of the trimmed front. Preserve the source framing and exact relative locations. This is one scene replacement, not an entire new book-cover layout.

> @Create Image: Using the attached B1 scene as a visual reference, create an original, genuinely high-detail replacement of this same lower scene at native dimensions of at least 2550 × 2089 pixels. Preserve the composition and relative proportions: adult male Northern Cardinal perched on a branch inside the large gold magnifier, notebook behind, secondary binoculars overlapping the lower right, dark natural green background and gold/ivory accents. Preserve the scene's crop and object positions; do not add text, logos, badges, page edges or a cover mockup. Keep the cardinal anatomically plausible: a prominent crest, short thick reddish bill, black face around the bill and throat, long tail, and naturally gripping toes. Use Cornell's Northern Cardinal identification page only as a reference, never trace or reproduce its photographs. Produce an original commercially usable illustration with natural feather detail, clean object boundaries and coherent light. Do not enlarge or sharpen the attached low-resolution reference and call it new detail. If you cannot create a native image at the requested resolution, state the actual native output size rather than upscaling it.

## Optional path: separately registered components

For editable reconstruction, attach the whole scene plus the relevant native-pixel reference crop. Each crop is an overlapping, non-transparent **position reference**; it is not a ready-to-place component. Preserve the source proportions, pose and exact pixel registration in the full scene. Give every returned component a transparent canvas and no lettering; document actual native dimensions. Rebuild simple rim, notebook, flat fields and shapes as vectors where they can be accurately drawn, then place detailed bird and binocular assets separately. Never force a differently framed image into a slot by stretching. These windows include intentional surrounding space; minimum sizes apply to the **entire output canvas**, including transparent margins.

| Reference / prompt | Canvas placement at frozen front trim, from top-left | Native minimum for complete window |
|---|---|---:|
| [Cardinal reference](cardinal-reference.png) | x=1.1184, y=4.4324 in; width=4.6665, height=4.5865 in | 1400 × 1376 px |
| [Magnifier and notebook reference](magnifier-notebook-reference.png) | x=0.1543, y=4.1240 in; width=6.7877, height=6.1514 in | 2037 × 1846 px |
| [Binoculars reference](binoculars-reference.png) | x=3.7795, y=7.8626 in; width=4.7205, height=2.4128 in | 1417 × 724 px |

For the cardinal window:

> @Create Image: Using the attached whole B1 scene and cardinal-position reference, make a separate original detailed illustration of the same adult male Northern Cardinal and the branch it grips, on a transparent canvas of at least 1400 × 1376 native pixels. Keep exactly the same pose, scale and location inside the reference window, including the long tail's relationship to the magnifier. Include no magnifier, notebook, binoculars, text or background. Use the Cornell Northern Cardinal identification page as an anatomy reference without tracing photographs. Preserve realistic crest, thick reddish bill, black facial mask and throat, wing, tail, legs and toes. Do not upscale the reference; report actual output dimensions.

For the magnifier/notebook window, use this only if hand-built vector geometry is insufficient:

> @Create Image: Using the attached B1 scene and magnifier/notebook position reference, make a separate original illustration of the same gold magnifier, handle, ivory field notebook and rings, on a transparent canvas of at least 2037 × 1846 native pixels. Keep their position, angles and size exactly registered to the reference window. Leave the lens interior transparent for a separately placed cardinal and background; omit birds, binoculars, text, badges and other surrounding scenery. Do not upscale the reference; report actual native dimensions.

For the binocular window:

> @Create Image: Using the attached B1 scene and binocular-position reference, make a separate original detailed illustration of the same green-and-gold binoculars and strap on a transparent canvas of at least 1417 × 724 native pixels. Preserve their exact pose, scale and location within the reference window; include no bird, notebook, text or background. Do not upscale the reference; report actual native dimensions.

A separate compatible lens/background layer must fill the scene behind these overlapping assets; preserve the existing layout, do not invent an unrecorded factual feature, and measure its actual native pixels at placement. Check clipping order, partially hidden tail, ring, toes and strap against the original. Separate generation can produce misregistration or inaccurate anatomy; human corrections may be necessary. Record creation date, tool, source, rights and hashes for every received file and use a new revision. A high pixel count is necessary but does not by itself establish fine detail, anatomy, rights or print approval.
