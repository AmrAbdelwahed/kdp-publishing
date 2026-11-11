# Deferred KDP production design
This is a requirements plan, not a generator. Do not implement until owner approval of the blueprint and explicit production authorization. Python with Pillow (image inspection), ReportLab (page composition) and pypdf (structural inspection) is a proposed small local toolchain. Pin reviewed versions only when implementation starts. No server, database or paid API is required.

## Inputs and approval
Use PAGE_PLAN.csv plus an explicit asset manifest: page/species ID, approved path, SHA-256, original pixel dimensions, intended placement dimensions, provenance, generation tool/date, rights/license, reviewer and approval state. Keep originals immutable; derivatives in a generated directory. Reject missing/unapproved assets, duplicate page mappings and content outside the locked plan. Hashes catch exact duplicates; contact-sheet human review catches near-duplicates. No image is approved by filename alone.

## Interior
8.5 × 11 inches = 612 × 792 PDF points, exactly 64 pages, black ink, white paper, no bleed. Provisional conservative layout margins: inside 0.625 inch, outside/top/bottom 0.5 inch; mirror inside margins on odd/even pages. These are design proposals, not a claim about current KDP minima. Recheck official margin/gutter tables for page count and stock before implementation. Keep art, folios, tasks and running elements inside safe boxes. Page plan includes all matter; no accidental blank pages. Cover is separate.

Check raster effective PPI as pixel dimension / placed inch dimension in both axes; target >=300 for line art and flag insufficient native detail. Do not trust embedded DPI or mere upscaling. Check colour spaces, transparency and unintended grey fills against current KDP requirements. Human print review confirms line weight, legibility and writing/colouring space.

## Fonts and layout
Choose a legible font with explicit commercial redistribution/embedding rights; retain license text and source/version. Embed every required font and verify embedding. No unlicensed system-font assumption. Check glyph coverage and line breaks; avoid relying on fallback fonts. English is the pilot language; bilingual production is outside current scope. Page 64 must fit source notes/keys at readable size; if it cannot, revise plan with approval rather than shrink beyond usability. Put activity answers locally where practical.

## Cover
After final trim/page count/stock freeze, obtain the current official KDP cover calculator/template. Record its inputs, date and output; derive complete wrap dimensions including bleed/spine from it, not a hard-coded remembered formula. Verify barcode exclusion, safe areas, spine text eligibility, front/back orientation and title/author metadata. Use appropriately resolved approved cover assets and embedded licensed fonts.

## Outputs and validation
Later outputs: versioned interior PDF, separate cover PDF, contact sheets and QA report with input hashes/tool versions. Validate page count/order, exact page geometry/boxes, no encryption, fonts embedded, minimum effective PPI, missing/duplicate assets, text overflow and safe-area bounds. pypdf alone cannot establish render correctness, font rights or anatomy. Render every page with a trusted renderer, inspect contact sheets and representative full-size pages; review all illustrations and activity keys. Test failure cases: missing image, duplicate mapping, low PPI, incorrect page size and unapproved asset. KDP Print Previewer and a separately authorized physical proof remain later human gates. No upload or proof order now.

## Policy and economics verification
Official source locators (not retrieved; network proxy denied access):
- Content guidelines / AI: https://kdp.amazon.com/en_US/help/topic/G200672390
- Paperback manuscript formatting: https://kdp.amazon.com/en_US/help/topic/G201857950
- Paperback printing costs: https://kdp.amazon.com/en_US/help/topic/G201834340
- Paperback royalties: https://kdp.amazon.com/en_US/help/topic/G201834330
- Cover calculator: https://kdp.amazon.com/cover-calculator

Expected policy requirement to verify from current official text: KDP requires disclosure of AI-generated text/images/translations, including generated content edited afterward; AI-assisted editing/brainstorming is treated differently. Log content origin at asset and text-section level; verify current definitions and answer upload disclosure accurately. ChatGPT-generated illustrations must not automatically be classified as merely assisted. Maintain rights, originality and content-quality review regardless of disclosure. No official policy was verified live here.

Before pricing approval, record market/currency, list price, applicable royalty rate/tier, printing charge for this exact format, channel and relevant tax/price conditions. Standard planning formula is applicable royalty rate × eligible list price minus printing cost, subject to official current rules. Proposed US$9.99/C$13.99 and reported US$3.15/C$4.86 remain unverified; royalties are not profit. Do not substitute US costs into Canadian calculations or assume expanded-distribution equivalence.

## Final human release gate
Owner signs off factual accuracy, educational quality, original/cleared assets, print QA, metadata, disclosure, current costs and budget. Explicit approval for spend, upload and publication is separate. Never promise acceptance, monetization or a release date before those gates.
