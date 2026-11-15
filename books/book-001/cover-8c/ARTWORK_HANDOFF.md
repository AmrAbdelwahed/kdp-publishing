# Artwork correction and import handoff

Use [the existing eight-bird source comparisons and focused edit briefs](../interior-8b/ARTWORK_EDIT_BRIEFS.md), [resolution table](../interior-8b/ARTWORK_RESOLUTION.csv), and [remaining blockers](../interior-8b/REMAINING_BLOCKERS.md). No speculative path edits or automatic approvals are authorized.

| ID | Reviewer decision / targeted action |
|---|---|
| B02 Blue Jay | Check white wingbar; retain plausible dark necklace unless a reviewer identifies an actual error. |
| B03 American Robin | Review whether a usable, reference-guided darker-head/orange-underparts separation is needed. |
| B09 Downy Woodpecker | Select a sex and regional form; inspect whether simplified light wing checks are needed. |
| B10 Hairy Woodpecker | Review wing checks and regional form separately from B09; retain longer bill. |
| B15 American Goldfinch | Check adult-male forehead boundary; change seedhead only if a print shows tiny areas are unusable. |
| B22 Dark-eyed Junco | Human expert and colorist decide whether the existing division suffices; do not force hidden white tail feathers. |
| B29 Northern Mockingbird | Check whether two pale wingbars are distinct in the selected pose. |
| B30 Eastern Bluebird | Check facial and rusty-breast boundaries against an adult-male reference. |
| B27 Common Grackle | Additional possible issue: inspect whether the adult golden iris is recognizable and colorable; severity unconfirmed. |

When corrected art is supplied later: record source, creator/tool, date, target species/form and hash; preserve the supplied file and all prior candidates; use a new versioned filename and output directory. Check pixel dimensions, composition, anatomy and effective resolution, then run the existing vectorization workflow on that new candidate only. Compare raster and vector at the exact final physical placement and inspect coloring boundaries and print margins. Update the manifest and backlog with the new version, source references, observations and distinct **pending** scientific and physical-print review statuses. Never overwrite a previous revision or mark human approval automatically. An actual command depends on the existing batch script's arguments and must be checked when importing.
