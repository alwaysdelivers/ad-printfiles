# State Line — Build Protocol

**Status:** LOCKED. Single source of truth for the State line. Read in full before any state work.
**Last verified:** 2026-07-15 — every value below measured from live files/API, not assumed.

Supersedes `STATEANDAIRPORT_BUILD_PROTOCOL.md` (retired 2026-07-15; §6 absorbs it).
Absorbs `PREFIX_VALIDATION_PROTOCOL.md` for state work (§8). `AD_STANDING_INSTRUCTIONS.md` still governs
working style. `NEW_PREFIX_BUILD_PLAN_v2.md` governs prefix (non-state) products.

---

## 1. OPEN DEFECTS — live, customer-facing. Fix before new work.

Caused by the Option-2 merge (city products → state products). Products are correct; theme wiring is not.

**A. 16 broken PDPs**

| State | Defect | Fix |
|---|---|---|
| florida, nevada, california, illinois, colorado, massachusetts, washington | `templateSuffix` points at `templates/product.{state}.json` → **404**. PDP falls back to Shopify's default template: **no style picker at all**. | Create each template, pointing at the state's existing section — which still carries its OLD city name: `miami-combined`, `vegas-combined`, `losangeles-combined`, `chicago-combined`, `denver-combined`, `boston-combined`, `seattle-combined`. |
| newyork | Template exists, but `newyork-combined.liquid` has `styleOrder: [Western, Classic, Retro]` — no `Flag`. 96 variants exist; the Flag ones are unreachable in UI. | Add `Flag` to `styleOrder` + Flag branch in `treatUrl()` + `FLAG_VALID`. |
| all 8 above | Same missing-`Flag` wiring as newyork. | Same. |

**B. Shop All: 7 dead links.** Cards still point at `miami-`, `vegas-`, `losangeles-`, `chicago-`,
`denver-`, `boston-`, `seattle-always-delivers-tee` — all **404** since the rename.

`sections/texas-combined.liquid` is the **reference implementation** — correct and complete. Copy from it.

---

## 2. Session setup

`/tmp` is wiped between sessions. Credentials live in Drive (`AD_CREDENTIALS_<date>.txt`) — **never in this
repo; it is public** and GitHub secret-scanning auto-revokes exposed PATs. Paste the setup block from that
file to restore `/tmp/_ghpat`, `/tmp/_shop_client_id`, `/tmp/_shoptoken`, `/tmp/_printful_key`, then mint.

- **Shopify:** `/tmp/_shoptoken` is the CLIENT SECRET (`shpss_`), not usable as an API token. Mint the
  `shpat_` token via `client_credentials` → `/tmp/_shoptoken_live`. **It expires mid-session — on any 401,
  re-mint.** Shop `rudjph-mx.myshopify.com` · API `2025-07` · Theme (Horizon, LIVE) `153615171752` ·
  Publication `gid://shopify/Publication/198208127144` · Categories: tee `aa-1-13-8`, hoodie `aa-1-13-13`.
- **GitHub:** repo `alwaysdelivers/ad-printfiles` (**public**).
- **Printful:** store `18259192`, header `X-PF-Store-Id: 18259192`. Key scope is limited — `/store` returns
  403 (needs `stores_list/read`, not granted); **this is not a broken key**. Verified working 2026-07-15:
  `/stores`, `/orders`, `/mockup-generator`.

Verify each credential works before relying on it. Don't assume a 403 means dead.

---

## 3. Current state (verified 2026-07-15)

**Print files — all 50 states, live, CDN-verified:**
```
printfiles/states/{CODE}_{light|dark}_{tee|hoodie}.png          200 files
printfiles/web/states/{CODE}_{light|dark}_{tee|hoodie}.png      200 files
heroes/grid/{folder}_{tee|hood}_{white|heather|navy|black}.webp 400 files
```
`{CODE}` = `{STATE}FLAG` (e.g. `ALABAMAFLAG`) · `{folder}` = `{state}flag` (e.g. `alabamaflag`).
**All hoodie files carry `_r2`** (a centering fix — see §7). Tee files have no suffix.

**Products — 100 live, published, heroes set:**
- **41 plain states** — handle `{state}-always-delivers-{tee|hoodie}`, **Color × Size only** (24 variants),
  `templateSuffix: state`, shared section `state-flag-combined.liquid`. **Live and correct as flag-only; full-parity build (fonts + airports + hierarchical PDP) planned in waves — see locked list + decisions above.**
- **9 merged states** — `Color × Size × Style` (96 variants; texas 192). See §1: 8 are broken.

**Texas — complete. 8 styles / 192 variants:** Western, Classic, Retro, Flag, AUS, DFW, HOU, SAT.

---

## 4. Flag design — LOCKED geometry

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
| Worst case ends at | 13.45″ of 16″ (84%) | 13.45″ of 14″ (96%) |

- **Flag** — real colors, scaled to a fixed 3.00″ height. Width varies by flag aspect ratio (Ohio's
  swallowtail vs Colorado's rectangle) — **expected, not a bug**. **8px white border** (~0.027″) so it
  reads on dark fabric.
- **Name** — Cinzel. Fit to **both** max-width AND max-height, whichever binds:
  `scale = min(max_w/natural_w, max_h/natural_h)`. Width-only overflows long names (Connecticut);
  height-only oversizes short names (Iowa/Ohio) and pushes past the hoodie limit.
- **Wordmark** — standard Patua One lockup, positioned from the **measured name bottom + 720px**.
  Never a fixed absolute Y — name height varies.
- **Ink** — navy `#1e3a5f` on White/Athletic Heather; white on Navy/Black. Auto-switched by garment
  ground. **No ink picker for Flag.**

**Flag source:** `https://en.wikipedia.org/wiki/Special:FilePath/Flag_of_{State}.svg` → cairosvg
`--output-width 2400`. Underscores for multi-word (`New_Hampshire`). **Rate-limited — sleep 1.5s between
fetches** or you get HTML error pages saved as `.svg`. Always verify: `file X.svg` must say "SVG".

---

## 5. Style architecture

One flat `Style` axis. **Display names only — never a raw font name** as an option value (expensive to
change once variants exist).

| Style | Scope | Font | Ink |
|---|---|---|---|
| Flag | all 50 | — | none (auto light/dark) |
| Western / Classic / Retro | the 8 city-states | Rye / Cinzel / Monoton | full 7-ink palette |
| AUS / DFW / HOU / SAT | Texas only | Monoton | restricted (§6) |

**7-ink palette** (Western/Classic/Retro): `fc`, `navy`, `red`, `black`, `gold`, `white`, `karmablue`.
File token maps: `fc`→`fc_light`, `karmablue`→`neonblue`, else literal.
Validity: White/Ath.Heather → `fc,navy,red,black,gold,karmablue` · Navy → `red,gold,black,white,karmablue`
· Black → `navy,red,gold,white,karmablue`. Defaults: light→`fc`, dark→`red`.

**Ink validity is style-dependent.** `_vset(style, color)` dispatches per style. `getDefault()` **must**
validate its default against the current style's valid set — otherwise it returns an ink that style can't
use. (This was a real latent bug; fixed in `texas-combined.liquid`.)

Adding a style = product option + `styleOrder` + `_vset` branch + `treatUrl()` branch + chip. All five.

---

## 6. State & Airport (absorbed from the retired doc)

```
printfiles/{web/}stateairport/STATEAIRPORT_tx-{code}_{token}_{garment}_r2.png
```
Codes: `aus`, `dfw`, `hou`, `sat`. Tokens: `fc_light`, `redstate_white`, `neonstate_white`, `goldstate_white`.

**Ink & fabric — LOCKED**

| Ink | Fabric | State opacity | Wordmark | Code opacity |
|---|---|---|---|---|
| Full Color (navy code / red state) | **White only** | 50% | 50% | 100% |
| Full Color | Dark | **REJECTED — never use** | | |
| Red / Neon / Gold state + white code | **Dark only** | 75% | 75% | 100% |

The airport code is **never** faded — 100% on every fabric. Full Color on Dark was tested and explicitly
rejected; don't re-propose. Single-ink standalone treatments (navy/red/black/gold/white/neon alone) are
**removed** from State & Airport — only Full Color and the two-tone combos exist.

**Ghost sizing — RULE B (2026-07-15, supersedes "10.00″ wide"):** the state ghost code fits a
**3000×1701px box (10.00″×5.67″)**: `scale = min(3000/w, 1701/h)`. Wide ghosts (TX, NY) width-bind —
pixel-identical to the old rule; narrow ghosts (IL, HI, RI…) height-bind, which pins the wordmark at
y3321 (TX-identical rhythm). The old width-only rule CLIPPED the lockup off both canvases for IL —
never use it. **Harmony-scale sizing:** `target = state_dims × 2/3`;
`scale = sqrt(x_scale × y_scale)` (geometric mean) — **uniform only, never distort letterforms**. Airport
code centered on the state code, in front.

**Overshoot correction — mandatory per new code** (Monoton over-renders curves). Verified: DFW none ·
HOU O-symmetric + U-bottom-only · SAT S-symmetric · AUS none. `monoton_correct.solve_width_corrected()`
applies it automatically and also handles the whitespace fix for two-word prefixes. Log the decision per
code; don't assume a letter behaves the same in a different word.

**Lockup** — the standard `_ALWAYS DELIVERS` (Patua One), recolored to the ink; two-tone matches the
state color at the state's opacity. Never a bespoke lockup.

**Built so far (2026-07-15):** NY (ALB/BUF/JFK/LGA/ROC/SYR) and IL pilot (ORD/MDW, rule B) live
end-to-end. New files carry NO `_r2` (only tx- files do, legacy CDN fix).
**Locked airport list:** 94 code instances / 48 jurisdictions — canonical file
`state_airport_list_FINAL_2026-07-15.json` (Drive + outputs). Dual listings are SEPARATE designs:
CVG under both KY and OH; DCA under both VA and DC. Delaware: no airport style (state product only).
**Naming (final):** FULL state name in all three font styles and under every flag, D.C. included
("WASHINGTON D.C."). No abbreviations anywhere.
**PDP architecture (locked):** Name is a line-item PROPERTY (like Ink) — zero variant growth. UI:
large state pill + smaller alphabetical city pills; default = state view (state fonts + Flag + all
state airports); selecting a city filters to that city's fonts + its airport(s) (airport travels
with the city). Deep-link via `?name=`.
**ELASTIC FLAG RULE — LOCKED 2026-07-15 (supersedes fixed 3.00″ flag height).** Two independent
containers sharing a budget. Stack: 750px top + FLAG + 450 + NAME + 720 + WORDMARK(600), hoodie
ends-at ceiling 13.50″ (4050px) → FLAG_H + NAME_H ≤ 1530px. NAME: fit 3000×600 (unchanged).
FLAG: FLAG_H = 1530 − NAME_H, floored at its prior size (never shrink), width ≤ 3000. Result: ×1.00–1.30
growth, every regenerated design ends at exactly 13.49″. FILENAMES (CDN rule): ALL 50 states now
uniform `{STATE}FLAG_{ground}_tee_r2.png` / `_hoodie_r3.png` — the 9 floor states (AK HI ID IA KS ME
OH TX UT) are content-identical to prior files but renamed for uniformity.
**EMBLEM-DIRECT — AMENDED 2026-07-15 (evening): applies to ALL grounds, not dark only.** The four
white-field states (ALABAMA, ILLINOIS, MASSACHUSETTS, RHODE ISLAND) use emblem-direct on light AND
dark. Their flag files carry `_r3` tee / `_r4` hoodie on BOTH grounds (dark = content-identical
rename-copies); every other state stays `_r2`/`_r3`. Suffix resolution: `_flagsuf()` in fulfill.py,
`EMB[CFG.code]` in the shared section, hardcoded `_r4/_r3` in chicago/boston sections. Their grid
heroes live in `{state}flag2_*` folders (uniform `_r2`/`_r3`); chips `boston_flag_r3`,
`chicago_flag_r3`. Original locked text follows for dark-treatment mechanics (field flood-removal,
white name on dark, Illinois in-art lettering stripped):
**DARK-GROUND EMBLEM-DIRECT — LOCKED 2026-07-15.** White-field flags (ALABAMA, ILLINOIS,
MASSACHUSETTS, RHODE ISLAND) render on dark garments with the field flood-removed and the emblem
printed directly at full elastic size; the state name line renders WHITE; Illinois's in-artwork
"ILLINOIS" lettering is stripped (bottom band of the emblem). All other flags ship authentic on dark.
Light grounds always authentic. Chips for merged states renamed: cities `{city}_flag_r2.webp`,
newyork/texas `_flag_r3.webp`, georgia `_flag_r2.webp`.

**Doc correction:** the overshoot log's "AUS: none" is contradicted by the shipped file — U and S ARE
height-normalized in AUS. Per-glyph ink→[cap-top…baseline] normalization is the actual rule; the
layout engine derives glyph centers from font metrics (advances + glyph bboxes), validated against
the tx-aus reference (gaps 80/115, block 2623×863).

---

## 7. Hard-won rules — violating these breaks production

**Transparency.** Print files are RGBA with genuine transparency. Assert before pushing:
```python
assert not (np.array(img.split()[3]) == 255).all()
```
An opaque background prints as a **visible box** on the garment. It also silently breaks trim-to-content
(the "content" bbox becomes the whole canvas), so chips come out at the wrong scale.
**Reference:** a correct Texas airport chip is 216×218.

**Envelope asserts (2026-07-15, mandatory).** `Image.alpha_composite` silently clips content pasted past
the canvas edge — bbox/centering asserts will NOT catch it. Before composing: assert
`wm_top + lockup_h <= canvas_h`. After composing: assert measured content bottom == expected wordmark
bottom (±2px). The IL pilot shipped nothing only because a human caught it — the asserts must.

**Per-garment centering.** Center against the **actual garment canvas width** (`cw`), never a hardcoded
3600. Rendering at tee width and pasting onto the 4200px hoodie offsets everything 300px left (43px at web
scale). Verify: content center within ~1px of `cw/2`.

**Alpha compositing.** Always `Image.alpha_composite()`. **Never** `.paste(src, box, mask)` for
partial-opacity content — it blends against the destination's hidden `(0,0,0)` and silently washes out
colors. `.paste()` is safe only for fully-opaque content.
Verify any opacity render: sample a faded pixel, compare to `bg×(1−o) + fg×o`, must match within ~2.

**jsDelivr never re-serves a changed file.** Cache is permanent per filename. `?v=` does nothing. Purge
does nothing (MD5-proven). To ship a correction, push a **new filename** (`_r2`, `_r3`) and update every
reference. This is why all hoodie state files are `_r2`.

**Verification sources.** `raw.githubusercontent.com` **lags after a push** — a 404 there is not proof of
absence. The Contents API is authoritative. A `"sha wasn't supplied"` error on PUT means the file already
exists (success), not failure. CDN-gate every file (must 200) before referencing it anywhere.

**Shopify.**
- `productSet` needs an explicit `id` to UPDATE; without it → "handle in use".
- Hero: `productCreateMedia` → poll → `productReorderMedia(newPosition:'0')`.
  **Poll for `READY` *or* `FAILED`.** A bad source URL yields `FAILED`, and reordering failed media
  **silently no-ops** — the old hero stays and nothing errors. Check the URL 200s first; verify
  `featuredImage` after. (This bit once: the script used the handle-stripped name `alabama_hood_white_r2`
  instead of the real filename `alabamaflag_hood_white_r2`; all 41 silently failed.)
- `productSet synchronous:false` for >100 variants; poll `productSetOperation`.
- Theme asset PUT → wait 3s → read back and assert **byte-identity**. REST readback can serve stale
  content for seconds.
- Trace the live chain before editing any theme file: page/product template JSON → section `type` →
  `sections/{type}.liquid`. Shop All lives in `sections/shop-all.liquid` — **not** the orphaned
  `ad-all-prefixes.liquid`.

**Multi-word names.** A blanket `replace('TEXAS','NEW YORK')` corrupts filename construction as happily as
it fixes titles. After cloning a section, grep for `{DISPLAY NAME}_` (name + underscore) — that pattern is
the signature of a broken URL. Single-word names can't produce it; that's why it hit New York and LA but
not Chicago.

**Ordered lists.** Never assume position. Extract the full list, apply the real sort, assert the result.
"The X" sorts under X.

**Batches time out.** Every push script must be **resumable** (skip files already 200 on raw). Expect to
re-run 2–3 times. Sleep 0.25–0.4s between pushes; fetch SHA before PUT on an existing file.

**Printful placement.** Product 71 `front` = 12×16″ (1800×2400@150dpi); product 146 `front` = 14×14″
(2100×2100). **Never `front_large`** (15×18″ — wrong). Mockups: Ghost only (`option_groups:["Ghost"]`),
~1 task/min — submit one, sleep 65s. Verify the Printful placement box inches == the print file canvas
inches before submitting.

**EST. dates.** Never copy another prefix's year. Search and confirm the real founding year, and state the
source in the same response as the generation.

---

## 8. Validation — non-negotiable

**Every number is computed from measured data.** Show the raw measurement, the formula, and the result.
Never carry a value forward unverified from another state. Never report placement math from a preview
crop — always from the real canvas.

**Every claim is shown, not asserted.** "Verified" without the actual output is not verification.

**Check before you build.** Product, section, template, catalog entry, existing files. Never assume a
clean slate — several states already had partial/stale artifacts.

**Never eyeball.** If the tool won't render a preview, verify by measurement (bbox, pixel sample, MD5),
not by assuming.

**Ask before state changes.** Investigation verbs ("fix", "clean up", "look into") mean investigate,
report, stop. Finding the answer is the finish line.

---

## 9. Build a new state

1. Read §1 (open defects) and this doc. Set up credentials (§2).
2. **Check what already exists** — product, section, template, catalog, files.
3. **Pre-flight name fit** for the state (§4) *before* generating anything.
4. **Source the flag** (§4). Verify it's really an SVG.
5. **Generate** print + web + grid heroes. **Assert transparency and centering** (§7).
6. **Push** with a resumable script. **CDN-gate** every file.
7. **Product** via `productSet`. Plain state = Color × Size, `templateSuffix: state` (shared section, no
   new template needed). With City/Airport styles = Style axis + own section + **own template** (§1's bug).
8. **Publish**, set hero (`productCreateMedia` → poll READY/FAILED → reorder), verify `featuredImage`.
9. **Verify live** — `/products/{handle}.js` for styles/variants, and fetch the PDP HTML to confirm the
   section actually rendered.
10. Wire the downstream: Shop All, `ad-items.liquid`, `catalog.json`, `fulfill.py` (§10).

---

## 10. Remaining work

1. **Fix §1** — 16 broken PDPs + 7 dead Shop All links. Mechanical; copy `texas-combined.liquid`.
2. **Shop All** (`sections/shop-all.liquid`) — repoint/remove the 7 stale city cards, add 50 state cards,
   alphabetical. The hoodie toggle already special-cases state cards for `_r2` — don't break it.
3. **`snippets/ad-items.liquid`** — 50 states absent. The home-page count reads from it.
4. **`catalog.json`** — 50 state entries; update the 9 merged.
5. **`fulfillment/fulfill.py`** — routing for 41 renamed handles + 9 merged + 4 airport codes.
   **Dry-run every valid combination against raw before pushing.**
6. Optional/future: City and Airport styles for the other 41 states (none exist today).
