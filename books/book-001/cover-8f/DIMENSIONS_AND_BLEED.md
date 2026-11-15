# B1 cover dimensions — formula and supplied template

On 2026-11-15 at 18:52:10 UTC, [KDP Paperback Submission Guidelines](https://kdp.amazon.com/en_US/help/topic/G201857950) returned HTTP 200. KDP specifies white-paper black-and-white spine width as page count × 0.002252 in and gives cover width = bleed + back trim + spine + front trim + bleed, and cover height = bleed + trim height + bleed. KDP specifies 0.125 in outer bleed. These are current source observations, not KDP approval of this file.

| Measurement | Unrounded calculation / observed value |
|---|---:|
| Spine | 64 × 0.002252 = **0.144128 in** = 10.377216 pt |
| Width | 0.125 + 8.5 + 0.144128 + 8.5 + 0.125 = **17.394128 in** = 1252.377216 pt |
| Height | 0.125 + 11 + 0.125 = **11.25 in** = 810 pt |
| Template printed labels | 17.394 × 11.250 in; spine 0.144 in |
| Template drawn right edge / actual MediaBox width | 1252.377197 pt / 1252 pt |
| Review PDF MediaBox | 1252.377 pt × 810 pt (rounded by PDF serialization) |

The drawn edge agrees with the formula to about 0.000019 pt, and both round to the printed 17.394-in label. The template's narrower MediaBox is 0.377197 pt (0.005239 in) short of that drawing. It is consistent with truncation to a whole point, but the source does not establish why it occurred. The review wrap follows the formula and drawn geometry, retaining 9 pt bleed at each outer edge; it does not crop content to match the smaller box. A fresh official template or KDP guidance and an eventual **KDP Previewer check remain pending**. Do not interpret this analysis as KDP approval.

The supplied template (unchanged [PDF](../cover-8e/source/KDP-template-original.pdf), SHA-256 `15c08c0ad55b241d6dc11c097f1fc6b35467aa6ff6bd6b302f7191c6eb06b9fa`) shows fold x-coordinates 621 and 631.377197 pt from the left. The barcode exclusion rectangle in top-origin points is (459, 696.6)–(603, 783), exactly 2 × 1.2 in. Its background remains clear of text and essential artwork. Spine text is absent. Text-safe positions and embedded fonts are checked in the tests; decorative image content reaches into the front edge/safe zone and needs a human trim review. See [8E template preflight](../cover-8e/KDP_TEMPLATE_PREFLIGHT.md) for measured live areas and color caveats.
