# State & Airport — Build Protocol

**Project name:** State & Airport
**Current subtitle:** Texas (varies per state as new states are built)
**Status:** LOCKED — this document governs every future State & Airport build. Read in full before starting a new state.

This is a standalone product line, independent of any prefix-style product (e.g. TEXAS the full-name product with Western/Classic/Retro). A state may have ONLY a State & Airport product and nothing else — the naming and file structure must never assume a parent "full-name" product exists.

---

## 1. Naming Convention — LOCKED

```
stateairport_{state}_{state}-{airport}_{ink}_{garment}.png
```

**Example:** `stateairport_tx_tx-aus_fc_light_tee.png`

- `stateairport` — fixed, identifies the product line
- `{state}` — 2-letter lowercase state code (e.g. `tx`)
- `{state}-{airport}` — 2-letter state + 3-letter airport code, lowercase, hyphenated (e.g. `tx-aus`)
- `{ink}` — ink/color token (see Section 3)
- `{garment}` — `tee` or `hoodie`

All lowercase. No `watermark` segment — `stateairport` already identifies the product line, so there is no second style layer to disambiguate.

Two-tone exploratory combos (color-state + white-code, not yet in the confirmed print-file set) use a descriptive ink token pattern: `{color}state-white`. Example: `stateairport_tx_tx-aus_redstate-white_dark_tee.png`. These stay OUT of the official print-file naming (`fc_light` only) until explicitly confirmed and promoted.

---

## 2. Canvas & Placement Math — LOCKED

Identical absolute pixel positions for every state, every airport code, every ink. Only the state name, airport code, and ink color change — never the geometry.

| | Tee | Hoodie |
|---|---|---|
| Canvas | 3600×4800px · 12.00″×16.00″ | 4200×4200px · 14.00″×14.00″ |
| Content top | 900px / 3.00″ | 900px / 3.00″ (same) |
| Gap (block → wordmark) | 720px / 2.40″ | 720px / 2.40″ (same) |
| Wordmark size | 2173×599px · 7.24″×2.00″ | same |
| Print-area usage | ~82% of 16″ | ~93% of 14″ (tighter — verify overflow every build) |

**Design block** (state name + airport code combined) is NOT a fixed size — it varies slightly by airport code length (harmony-scaled, see Section 4) but the state name always renders at a fixed 10.00″ width, so block height stays ~5.67″ regardless of airport code.

**Rule:** content is always top-anchored at 900px on the real print canvas — never measure or report placement math from a tight-crop preview canvas. Preview/review renders must be re-composited onto the true canvas (900px top, correct garment dimensions) before any math is reported or shown to Ati.

---

## 3. Ink & Fabric Rules — LOCKED

Confirmed through the Texas build. Apply identically to every new state unless Ati explicitly says otherwise for that state.

| Ink treatment | Fabric | Opacity (state backdrop / wordmark) | Front code opacity |
|---|---|---|---|
| Full Color (navy front / red state, split) | **White only** | 50% / 50% | 100% (always) |
| Full Color | Dark | **REJECTED — do not use** | — |
| Color-state + White-code (two-tone) | Dark only | 75% / 75% | 100% (always) |

- Full Color on Dark was tested and explicitly rejected ("it won't work") — never re-propose without being asked.
- The front/code element (e.g. the airport code) is NEVER faded — always 100% opacity regardless of fabric.
- Opacity standard applies uniformly: it is NOT decided per-ink-combination. White fabric = 50/50, Dark fabric = 75/75, no exceptions without an explicit new instruction.
- Any single-ink-everywhere treatment (Navy, Red, Black, Gold, White, Neon as standalone, non-two-tone options) is REMOVED from State & Airport. Full Color and the two-tone color-state/white-code combos are the only families in use.

---

## 4. Harmony-Scale Sizing Method — LOCKED

For any 2-letter state code + 3-letter airport code:

1. Render the state code at a fixed width of **10.00″** (3000px @ 300dpi), natural aspect ratio, letter-overshoot corrected (Section 5).
2. Render the airport code at natural aspect ratio, same correction method.
3. `target_box = state_dims × 2/3`
4. `x_scale = target_w / airport_natural_w`; `y_scale = target_h / airport_natural_h`
5. `uniform_scale = sqrt(x_scale × y_scale)` — geometric mean. **Never distort the airport code's letterforms** — always scale uniformly, never stretch x and y independently.
6. Composite: airport code in front (opaque, 100%), state code behind (at the opacity defined in Section 3).
7. Add the wordmark 720px below the combined block, centered.

---

## 5. Letter-Overshoot Correction — MANDATORY, PER NEW CODE

Monoton (or whichever display font is locked for State & Airport) has known optical-overshoot letters (curves like O, C, G, S render slightly oversized vs straight-edged letters at the same nominal size). Every NEW state code or airport code must be checked fresh — do not assume a previously-corrected letter behaves identically in a new word.

1. Render the new 2- or 3-letter code.
2. Check each letter against the reference correction table (symmetric correction for O/C/G/S, bottom-only for J/U).
3. If a code contains ONLY letters with no known overshoot issue, no correction is applied — confirm this explicitly, don't assume.
4. Log the correction decision for that specific code (e.g. "DFW: no overshoot, no correction needed" / "HOU: O symmetric + U bottom-only").

---

## 6. Lockup — LOCKED (inherited from main AlwaysDelivers standard)

The standard `_ALWAYS DELIVERS` lockup (Patua One, leading underscore, two lines, ™ at final S) is used, recolored to match the active ink treatment:
- Full Color / White fabric: lockup matches Full Color convention (split navy/red or as otherwise locked for FC).
- Two-tone combos: lockup color matches the state-color, at the same opacity as the state backdrop (75% on dark).
- Never a different lockup design for State & Airport — this is the same universal lockup used everywhere else in AlwaysDelivers.

---

## 7. Step-by-Step Build Process for a NEW State

Follow in order. Do not skip or reorder steps. Stop and get Ati's go-ahead before any state-changing action (file writes, uploads, print-file generation for real use).

### Step 1 — Confirm scope with Ati
- Which state?
- Which airport codes? (How many — match Texas's 4, or different?)
- Which ink treatments apply — default to Section 3's locked rules unless told otherwise.

### Step 2 — Overshoot check (Section 5)
- Run correction check on the state code AND every airport code.
- Present findings before proceeding — do not silently apply guessed corrections.

### Step 3 — Generate review renders
- Build all state × airport × ink combinations on the TIGHT-CROP preview canvas first (fast iteration).
- Composite onto FABRIC backgrounds for visual review (not just transparent).

### Step 4 — AUDIT CHECKPOINT 1: Visual review with Ati
- Present a numbered matrix: fabric × ink (or state × airport, whichever grid is relevant) exactly like the Texas fabric-cull exercise.
- Get explicit confirmation on which combinations survive.
- **Do not proceed to full-canvas generation until this is confirmed.**

### Step 5 — Regenerate on the REAL print canvas
- Composite the confirmed designs onto the actual Tee (3600×4800) and Hoodie (4200×4200) canvases, top-anchored at 900px (Section 2).
- **Never report placement math from the tight-crop preview** — always measure from the real canvas.

### Step 6 — AUDIT CHECKPOINT 2: Placement math verification
- Measure block top/bottom, gap, wordmark position, and ends-at position DIRECTLY from the generated files (pixel measurement, not calculation from assumptions).
- Compare against Section 2's locked values — they should match exactly (only block width/height varies slightly by code length).
- Flag any deviation before proceeding.

### Step 7 — AUDIT CHECKPOINT 3: Overflow / safety check
- For every hoodie file (tighter margin — Section 2 notes ~93% usage), verify the bottom margin is still safe (never <50px from canvas edge).
- For every tee file, same check even though margin is more generous.

### Step 8 — AUDIT CHECKPOINT 4: Compositing integrity check
- Verify no PIL alpha-compositing bugs (Section 8) — spot-check at least one faded element's actual pixel color against the expected math for that opacity.

### Step 9 — Final naming pass
- Rename every file to the Section 1 convention. Do this as a distinct, deliberate step — never generate directly to final names, to avoid silent naming drift.
- Cross-check the full file list against the expected count (states × airports × inks × garments) before delivery.

### Step 10 — Package and deliver
- Zip all files for delivery (per standing instruction: always zip multi-file deliveries).
- Include a fresh placement-math + full-palette HTML review (Tee + Hoodie side by side, matching the Texas review format) in the same zip.
- Confirm internal HTML `<title>` and `<h1>` say "State & Airport — {State}", not any older/inherited naming.

---

## 8. Known Bug — PIL Alpha Compositing (permanent reference)

`PIL.Image.paste(source, box, mask)` corrupts semi-transparent pixel colors when the destination is fully transparent (alpha=0) — it blends the source's RGB against the destination's hidden `(0,0,0)` placeholder rather than preserving true color. This silently produces washed-out, lower-contrast results than the intended opacity.

**Fix:** always use `Image.alpha_composite()` for any compositing step involving partial-opacity layers, regardless of whether the destination is transparent or opaque. Never use `.paste()` with a mask for anything but fully-opaque content (fully-opaque paste onto any destination is safe and behaves correctly).

Before trusting ANY new opacity-based render, spot-check: sample a pixel from the faded element, compute the expected color mathematically (`bg × (1 − opacity) + fg × opacity`), and confirm the actual rendered pixel matches within a few units. This check is now baked into Audit Checkpoint 4 (Section 7, Step 8) for every future build — not optional, not a one-time fix.

---

## 9. Presentation Standard (inherited, reaffirmed for State & Airport)

- Placement math shown as a card, full locked 9-row format (never condensed).
- Tee and Hoodie math shown side by side when both are relevant.
- Every design preview shows Tee + Hoodie together, not separately.
- Numbered matrices for any cull/decision grid.
- Full-resolution HTML proofs, browser-zoomable, not just inline low-res thumbnails.
- Large multi-file deliveries are always zipped.

---

## 10. Working-Style Rules (reaffirmed for State & Airport specifically)

- **One step at a time.** Do not pre-stage or pre-generate the next state's assets before Ati confirms the current state is done.
- **Never assume an opacity, ink, color, or naming decision is "obviously" the same as Texas's** — confirm explicitly for each new state, even though Section 3's rules are the default starting point.
- **Ask permission before any push/upload/state-changing action** — generating review renders locally is fine; writing to the repo, Shopify, or uploading final files to Drive requires explicit go-ahead.
- **Show the math.** Every placement claim is measured from the actual file, never estimated or assumed to carry over from Texas without verification.
