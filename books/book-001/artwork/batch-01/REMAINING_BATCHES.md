# Remaining 24 birds — proposed batches

Stop after batch 01 for the user’s joint review. No later batch is authorized by this schedule. The six already covered are the visually accepted cardinal reference and five unapproved batch-01 candidates. Original cardinal anatomy and print checks remain open.

For each batch: verify identification references and regional caveats, vary pose and setting, generate one at a time with the actual cardinal image as style reference, preserve each original, trace and review individually, and track human/print approval. Use `python scripts/bird_prompt.py B05` for a draft prompt generated from SPECIES_LIST.csv; attach the cardinal image when using it. Batch-01 processing is per species and revision; to process another version of one of the five, save a new source under batch-01/originals and use a new `--revision` with `scripts/process_bird_batch.py`; existing outputs cannot be overwritten. When a future batch is authorized, `python scripts/bird_prompt.py --json B05 B06 ...` can prepare `generation-prompts.json` from SPECIES_LIST.csv. Record the exact prompt actually used, actual generation provenance and whether the master image was supplied before processing; then use `--batch books/book-001/artwork/batch-02` with a unique `--revision` per original. Never overwrite existing source images or processed revisions.

## Future batch 2 — 6 species

B05 Carolina Chickadee, B06 Tufted Titmouse, B08 Red-breasted Nuthatch, B09 Downy Woodpecker, B10 Hairy Woodpecker, B11 Red-bellied Woodpecker

## Future batch 3 — 6 species

B12 Northern Flicker, B14 Rock Pigeon, B15 American Goldfinch, B16 House Finch, B17 Purple Finch, B18 House Sparrow

## Future batch 4 — 6 species

B19 Song Sparrow, B20 White-throated Sparrow, B21 White-crowned Sparrow, B22 Dark-eyed Junco, B23 Chipping Sparrow, B24 Carolina Wren

## Future batch 5 — 6 species

B25 House Wren, B26 European Starling, B27 Common Grackle, B28 Red-winged Blackbird, B29 Northern Mockingbird, B30 Eastern Bluebird

## Milestone 2B update
The user provisionally accepted the chickadee and dove visuals and requested three revisions. Review the current `review-2b/` proof and decide whether to proceed; the remaining 24 have not been authorized for generation.
