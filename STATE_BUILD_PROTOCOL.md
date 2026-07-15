# State Line — Build Protocol

**Status:** LOCKED. Read in full before any state work.
**Last verified:** 2026-07-15 (every value below measured from live files/API, not assumed).

Credentials are NOT in this repo — it is public. See `AD_CREDENTIALS_<date>.txt` in Drive.
`/tmp` is wiped between sessions; re-mint the Shopify token every session and on any 401.

---

## 1. OPEN DEFECTS — live and customer-facing. Fix before new work.

Caused by the Option-2 merge (city products → state products). Products are correct; theme wiring is not.

**A. 16 broken PDPs**

| State | Defect | Fix |
|---|---|---|
| florida, nevada, california, illinois, colorado, massachusetts, washington | `templateSuffix` points to `templates/product.{state}.json` → **404**. PDP falls back to Shopify's default template: **no style picker at all**. | Create each template; point it at the state's existing section — which still has its OLD city name: `miami-combined`, `vegas-combined`, `losangeles-combined`, `chicago-combined`, `denver-combined`, `boston-combined`, `seattle-combined`. |
| newyork | Template exists, but `newyork-combined.liquid` has `styleOrder: [Western, Classic, Retro]` — no `Flag`. 96 variants exist; the Flag ones are unreachable in UI. | Add `Flag` to `styleOrder` + Flag branch in `treatUrl()` + `FLAG_VALID`. |
| all 8 above | Same missing-`Flag` wiring as newyork. | Same. |

**B. Shop All: 7 dead links.** Cards still point at `miami-`, `vegas-`, `losangeles-`, `chicago-`,
`denver-`, `boston-`, `seattle-always-delivers-tee` — all now **404** (renamed to their state handles).
Repoint to the state handle and rename the card label, or replace with the state card.

`texas-combined.liquid` is the **reference implementation** — correct and complete. Copy from it.

---

## 2. Current state (verified 2026-07-15)

**Print files — all 50 states, live and CDN-verified:**
- `printfiles/states/{CODE}_{light|dark}_{tee|hoodie}.png` — 200 files
- `printfiles/web/states/{CODE}_{light|dark}_{tee|hoodie}.png` — 200 files
- `heroes/grid/{folder}_{tee|hood}_{white|heather|navy|black}.webp` — 400 files
- `{CODE}` = `{STATE}FLAG` (e.g. `ALABAMAFLAG`). `{folder}` = `{state}flag` (e.g. `alabamaflag`).

**HOODIE FILES ARE `_r2`.** See §4. Tee files have no suffix.

**Products — 100 live, published, heroes set:**
- 41 plain states: handle `{state}-always-delivers-{tee|hoodie}`, **Color × Size only** (24 variants), `templateSuffix: state`, shared section `state-flag-combined.liquid`. **These are correct and done.**
- 9 merged states: `Color × Size × Style` (96 variants; texas 192). See §1 — theme wiring broken on 8.

**Texas — complete, 8 styles, 192 variants:** Western, Classic, Retro, Flag, AUS, DFW, HOU, SAT.

---

## 3. Placement math — LOCKED

Never estimate. Measure from the generated file every time.

| | Tee | Hoodie |
|---|---|---|
| Canvas | 3600×4800 (12″×16″) | 4200×4200 (14″×14″) |
| Flag top | 750px / 2.50″ | same |
| Flag height | 900px / 3.00″ | same |
| Gap flag→name | 450px / 1.50″ | same |
| Name box max | 3000×600px (10.00″×2.00″) | same |
| Gap name→wordmark | 720px / 2.40″ | same |
| Wordmark | 2172×598px (7.24″×2.00″) | same |
| Worst-case ends at | 13.45″ of 16″ (84%) | 13.45″ of 14″ (96%) |

- Flag: real colors, scaled to fixed 3.00″ height (width varies by flag aspect — expected, not a bug), **8px white border** (~0.027″).
- Name: Cinzel. Fit to **both** max-width AND max-height, whichever is more restrictive (`scale = min(w/nw, h/nh)`). Width-only overflows long names (Connecticut); height-only oversizes short names (Iowa/Ohio) and pushes past the hoodie limit.
- Wordmark: standard Patua One lockup, **flows from the measured name bottom + 720px** — never a fixed absolute Y.
- Ink: navy `#1e3a5f` on White/Athletic Heather; white on Navy/Black. Auto-switched by garment. **No ink picker.**

---

## 4. Hard-won rules — violate these and it breaks

**Transparency.** Print files must be RGBA with genuine transparency. Assert before pushing:
`assert not (np.array(img.split()[3])==255).all()`
An opaque background prints as a visible box on the garment. It also silently breaks trim-to-content
(chips come out at the wrong scale), because the "content" bbox becomes the whole canvas.

**Per-garment centering.** Center against the **actual garment canvas width** (`cw`), never a hardcoded
3600. Rendering at tee width and pasting onto the 4200px hoodie offsets everything 300px left.
Verify: content center must be within ~1px of `cw/2`.

**jsDelivr never re-serves a changed file.** The cache is permanent per filename; `?v=` does nothing;
purge does nothing (MD5-proven). To ship a correction, push a **new filename** (`_r2`, `_r3`) and update
every reference. This is why all hoodie state files are `_r2` — a centering fix.

**Verify on `raw.githubusercontent.com` or the Contents API — never trust a `raw` 404.**
`raw` lags after a push. The Contents API is authoritative. A "sha wasn't supplied" error on PUT means
the file already exists (i.e. success), not a failure.

**Shopify:**
- `productSet` needs an explicit `id` to UPDATE; without it → "handle in use".
- `productCreateMedia` → poll → `productReorderMedia(position 0)`. **Poll for `READY` *or* `FAILED`.**
  A bad source URL yields `FAILED`, and reordering a failed media silently no-ops — the old hero stays.
  Always check the URL 200s first, and verify `featuredImage` after.
- Token expires mid-session. On 401, re-mint.

**Multi-word names.** A blanket `replace('TEXAS','NEW YORK')` corrupts filename construction as happily
as it fixes titles. After cloning a section, grep for `{DISPLAY NAME}_` (name + underscore) — that
pattern is the signature of a broken URL. Single-word names can't produce this; that's why it hit
New York and LA but not Chicago.

**Large batches time out.** Make every push script resumable (skip files already 200 on raw), and expect
to re-run it 2–3 times.

---

## 5. Build a new state

1. **Read this doc + `PREFIX_VALIDATION_PROTOCOL.md`.** Check §1 for open defects first.
2. **Check what exists** — product, section, template, catalog entry. Never assume clean slate.
3. **Flag source:** `https://en.wikipedia.org/wiki/Special:FilePath/Flag_of_{State}.svg`
   → cairosvg at `--output-width 2400`. Underscores for multi-word (`New_Hampshire`).
   Rate-limited: sleep 1.5s between fetches or you get HTML error pages instead of SVGs.
4. **Pre-flight the name fit** for all states before generating anything (§3).
5. **Generate** print + web + grid heroes. Assert transparency and centering (§4).
6. **Push** with a resumable script. CDN-gate every file (must 200) before referencing it.
7. **Product:** `productSet`. Plain state = Color × Size, `templateSuffix: state`.
   With City/Airport styles = add Style axis, own section + **own template** (§1's bug).
8. **Verify live** — fetch `/products/{handle}.js` and confirm styles/variants; fetch the PDP HTML and
   confirm the section actually rendered.

---

## 6. Style architecture

One flat `Style` axis. Display names only — never a raw font name.

- **Flag** — all 50 states. No ink choice; ground auto-switches.
- **Western / Classic / Retro** — the 8 city-states (Rye / Cinzel / Monoton). Full 7-ink palette.
- **AUS / DFW / HOU / SAT** — Texas only. Restricted inks (§7).

Ink validity is **style-dependent**. `_vset(style, color)` dispatches per style; `getDefault()` must
validate its default against the current style's valid set or it returns an invalid ink.

Adding a style = product option + `styleOrder` + `_vset` branch + `treatUrl()` branch + chip.

---

## 7. State & Airport (Texas reference)

Files: `printfiles/{web/}stateairport/STATEAIRPORT_tx-{code}_{token}_{garment}_r2.png`
Codes: aus, dfw, hou, sat. Tokens: `fc_light`, `redstate_white`, `neonstate_white`, `goldstate_white`.

| Ink | Fabric | State opacity | Wordmark | Code opacity |
|---|---|---|---|---|
| Full Color (navy code / red state) | **White only** | 50% | 50% | 100% |
| Full Color | Dark | **REJECTED — never use** | | |
| Red / Neon / Gold state + white code | **Dark only** | 75% | 75% | 100% |

The airport code is **never** faded. Full Color on Dark was tested and rejected — don't re-propose.

**Harmony-scale:** state code at 10.00″ wide; `target = state_dims × 2/3`;
`scale = sqrt(x_scale × y_scale)` — uniform only, never distort letterforms. Code centered on the state.

**Overshoot correction is mandatory per new code** (Monoton). Verified: DFW none; HOU O-symmetric +
U-bottom; SAT S-symmetric. `monoton_correct.solve_width_corrected()` handles it — it also has a
whitespace fix for two-word prefixes.

**Verify opacity math** — sample a faded pixel, compare to `bg×(1−o) + fg×o`, must match within ~2.

---

## 8. Remaining work

1. **Fix §1** (16 broken products).
2. **Shop All** (`sections/shop-all.liquid` — NOT the orphaned `ad-all-prefixes.liquid`):
   remove 7 stale city cards (miami/vegas/losangeles/chicago/denver/boston/seattle — those handles are
   gone), add 50 state cards, alphabetical ("The X" sorts under X). The hoodie toggle already
   special-cases state cards for `_r2` — don't break it.
3. **`snippets/ad-items.liquid`** — 50 states absent. Home-page count reads from it.
4. **`catalog.json`** — 50 state entries; update the 9 merged.
5. **`fulfillment/fulfill.py`** — routing for 41 renamed handles + 9 merged + airport codes.
   Dry-run every combination against `raw` before pushing.
6. Optional: City/Airport styles for the other 41 states (none exist today).
