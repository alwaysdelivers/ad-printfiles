# Prefix Validation Protocol

**Applies to:** every future prefix build (standard prefixes per `NEW_PREFIX_BUILD_PLAN_v2.md`, and state-series prefixes per `STATEANDAIRPORT_BUILD_PROTOCOL.md`).

**Rule:** every action below has a mandatory validation step. An action is not "done" until its validation passes and the result is shown. No action proceeds to the next step without its validation passing.

---

## 0. Every number is computed, never guessed

**Action:** Any numeric claim — position, dimension, percentage, ratio, opacity, color match, count — is computed from actual measured data (pixel measurement, API response, file property). It is never stated from visual impression, pattern-matching against a prior prefix, or "this looks about right."

**Expected outcome:** Every number in a response is traceable to a specific measurement or calculation, shown alongside the number.

**Validation:** For every numeric claim, show the actual computation: the raw measured input(s), the formula/method applied, and the resulting number — in that order. A number with no shown derivation is treated as unverified and must not be presented as fact. If two numbers are being compared (e.g. "does this match the spec"), show both source values and the delta, not just a verdict.

**Explicit bans:**
- No "should be about X" — measure it and state the actual X.
- No carrying a number forward from a prior prefix/session without re-measuring it for the current one, even if it's "always been that value."
- No rounding a measured value to match an expected one without stating the actual measured value first.
- If a measurement can't be taken (file inaccessible, API unavailable), say so explicitly — do not substitute an assumption.

---

## 1. Before touching any asset

**Action:** Fetch the live reference file for the closest structurally-similar existing prefix (section, print file, mockup, catalog entry) directly from source — GitHub API / Shopify Admin API — in this session.

**Expected outcome:** A real, current file, not a memory or transcript summary of one.

**Validation:** Confirm the fetch returned content (non-empty, correct length) and log its source URL/API call. If the fetch fails or returns unexpected structure, stop — do not proceed on assumption.

---

## 2. Canvas / print-file geometry

**Action:** Before generating any print file, state the exact canvas size, top-anchor, gap, and lockup width from the governing doc for this prefix type.

**Expected outcome:** Numbers match the governing doc exactly.

**Validation:** After generating a sample file, measure it directly (pixel bounding box, not visual estimate) and compare against the stated expected numbers. Print both side by side. They must match exactly or the file is rejected and regenerated — never adjusted "close enough."

---

## 3. Mockup generation — placement

**Action:** Before submitting any Printful mockup task, fetch `/mockup-generator/printfiles/{product_id}`, compute `width/dpi` and `height/dpi` in inches for the placement being used, and compare to the actual print file's real canvas dimensions.

**Expected outcome:** Placement box inches == print file canvas inches, exactly.

**Validation:** Print the computed placement-box inches and the print-file's actual inches together. If they don't match exactly, stop — identify the correct placement key before submitting a single task. (Failure mode already hit once: `front_large` = 15×18in was used when the file was 12×16in, causing 0.375in drift.)

---

## 4. Mockup generation — style

**Action:** Every mockup uses `option_groups=["Ghost"]`. No exceptions, no on-model option groups, ever, for any prefix.

**Expected outcome:** Flat garment only, no human model, in every generated mockup.

**Validation:** Visually confirm the first mockup of any new batch before continuing the batch. If a model appears, stop the batch immediately.

---

## 5. Any compositing involving partial opacity

**Action:** Use `Image.alpha_composite()` for any layer with opacity < 100%. Never use `Image.paste()` with a mask for partial-opacity content.

**Expected outcome:** Rendered pixel color matches the mathematical expectation for the stated opacity.

**Validation:** Sample a known semi-transparent pixel. Compute expected color: `background × (1 − opacity) + foreground × opacity`. Compare to the actual rendered pixel. Must match within ±3 per channel. Run this check once per new compositing function, before using it at scale.

---

## 6. File naming convention

**Action:** Before generating filenames for a new asset type, fetch the live reference prefix's actual current filenames for that same asset type (not the written spec, the *actual live files* — specs can be stale).

**Expected outcome:** New filenames follow the identical pattern, character for character.

**Validation:** Print the reference filename and the new filename side by side, with each token labeled (prefix/style/ink/garment/etc). Confirm every token position matches structurally.

---

## 7. CDN resolution gate

**Action:** After every push to the repo, HEAD-check the file on both `raw.githubusercontent.com` and `cdn.jsdelivr.net`.

**Expected outcome:** Both return 200.

**Validation:** Print the count of files checked and count of failures. Zero failures required before the file is referenced anywhere (section code, catalog.json, etc). Never reuse an existing CDN-served filename for changed content — always push under a new suffix and re-check.

---

## 8. Editing any live theme file

**Action:** Before editing any `.liquid` section, trace the actual live chain: fetch the page's template JSON → extract the section `type` → confirm the section file being edited is exactly `sections/{type}.liquid`. Never edit a plausibly-named file without this trace.

**Expected outcome:** The file being edited is provably the one the live page renders.

**Validation:** Print the template JSON's section type and the filename about to be edited together; confirm exact match before making any change. (Failure mode already hit once: edited `ad-all-prefixes.liquid`, an orphaned file, while the live page actually used `shop-all.liquid`.)

---

## 9. Inserting into an ordered list (Shop All, any sorted grid)

**Action:** Before inserting a new item, extract the *actual* sort logic from the live JS/code (not assumed alphabetical or chronological), and compute the correct insertion index programmatically.

**Expected outcome:** New item lands at the position the live sort function would produce.

**Validation:** After insertion, extract the full list of names from the live file, apply the same sort function to a copy of that list, and assert the two orders are identical.

---

## 10. Product creation (Step 4)

**Action:** `productCreateMedia` (Full Color / White garment, correct garment type) → poll to `READY` → `productReorderMedia` to position 0 — for both Tee and Hoodie — as part of product creation itself, not a later fix.

**Expected outcome:** `featuredImage` is set immediately on both products at creation time.

**Validation:** Query `featuredImage{url}` via Admin API immediately after product creation. Assert it is not null and matches the expected hero image URL, before moving to Step 5.

---

## 11. Ink/color validity matrix

**Action:** Before generating any files, state the full ink × color validity matrix for every style, and get explicit confirmation before building anything against it.

**Expected outcome:** The matrix used to generate files matches the confirmed matrix exactly.

**Validation:** Print the matrix used immediately before generation. No generation begins until this specific matrix has been explicitly confirmed in the current session — not carried over from memory of a prior prefix.

---

## 12. Fulfillment routing (Step 6)

**Action:** After adding routing code, dry-run every valid style × ink × color × garment combination and assert the resulting file URL is 200 live.

**Expected outcome:** 100% of valid combinations resolve.

**Validation:** Print total combinations checked and failure count. Zero failures required before pushing `fulfill.py`. `py_compile` must also pass.

---

## 13. Credentials at session start

**Action:** At the start of any session requiring GitHub/Shopify/Printful access, locate and test all three credentials before starting build work.

**Expected outcome:** Each credential authenticates successfully.

**Validation:** One lightweight authenticated call per credential (repo read, `{shop{name}}`, store list) — confirm success before proceeding. If any credential is missing, ask immediately rather than partway through a build.

---

## 14. State/city founding or establishment dates ("EST." lines)

**Action:** Before generating any print file with an "EST. [year]" or similar date line, search for and confirm the actual founding/incorporation year of that specific state or city. Never reuse another prefix's date, even when copying its format/structure/fonts exactly.

**Expected outcome:** The date shown matches the real, verifiable historical founding or incorporation year for that specific place.

**Validation:** Run a web search for "[place name] founded incorporated year" before writing any code. State which specific date is being used and its source (search result) in the same response where the print files are generated — not after. If a place has multiple credible dates (e.g. "founded" vs. "incorporated," which are often different years), state both and pick the one matching the convention already established for this brand (the earliest well-known "founded" milestone — e.g. Texas 1845 = statehood, Miami 1896 = incorporation as a city, Las Vegas 1905 = founding auction, not the 1911 incorporation), and say why.

**Explicit bans:**
- Never copy an "EST." year from a template/reference prefix (e.g. TEXAS) onto a new prefix without independently verifying the new prefix's own correct year.
- Never assume a round or "expected-looking" date is correct — a search must confirm it in the current session.
- If the search cannot confirm a clear date, stop and ask rather than guessing or omitting the date silently.

---

## 15. Find-replace template cloning (multi-word names)

**Action:** When cloning a section/file via blanket string replacement (e.g. `TEXAS` → `NEW YORK`), never use a display-name replacement value that contains characters unsafe for file paths or URLs (spaces, punctuation) without separately verifying where that replacement landed. A single blanket replace will just as happily corrupt a filename-construction string as it fixes a title string.

**Expected outcome:** After cloning, every internal filename/URL-construction reference uses the safe, no-space code form (e.g. `NEWYORK_`), while every user-facing display string uses the correct display form (e.g. "NEW YORK").

**Validation:** After the replace, grep the output for `{DISPLAY_NAME_WITH_SPACE}_` (the display name immediately followed by an underscore) — this pattern almost never belongs in real display text and is the signature of a corrupted filename/URL. If found, fix surgically (the corrupted occurrence only) without touching the correct display-text occurrences. Do this check for every multi-word name, every time — single-word names can't produce this bug, which is exactly why it went undetected for New York and Los Angeles while Chicago/Denver/Boston/Seattle were fine.

---

## 16. Chip/thumbnail generation requires genuine source transparency

**Action:** Before generating a style chip (or any thumbnail built via trim-to-content-bounding-box), verify the source print file has genuine transparency (alpha channel actually varies, not flat 255 everywhere). Trim-to-content works by finding the bounding box of non-transparent pixels — if the source's background was baked in as opaque (a real bug that happened with the first State & Airport TX/AUS build), the "content" bounding box becomes the entire canvas, and the resulting chip shows the design tiny and off-scale relative to chips built from correctly-transparent sources.

**Expected outcome:** Every style chip for a given product crops to the same tight bounding box around its actual design content, so all chips in a style row render at consistent, comparable scale — never one noticeably smaller/more zoomed-out than its siblings.

**Validation:** Before generating any chip, spot check the source file: `alpha = np.array(img.split()[3]); assert not (alpha==255).all()`. If this assertion would fail, the source has the opaque-background bug and must be fixed at the source (regenerate the print file with genuine transparency) before making a chip from it — do not just crop harder or guess a manual bounding box as a workaround. After generating a batch of chips for the same product, compare their pixel dimensions (e.g. all should share the same width and a similar height band) — a chip that's a noticeable outlier in scale versus its siblings is the signature of this bug, not a legitimate design difference.

**Reference standard:** DFW's chip crop (216×218 for the Texas Airport family) is the correctly-scaled reference — any sibling chip for the same product/family should match this scale when built from a correctly-transparent source.

---

## Standing rule across all 16

Every validation result gets shown, not just claimed. "Confirmed" without the actual comparison output shown is not confirmation.
