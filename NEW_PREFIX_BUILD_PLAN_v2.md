# AlwaysDelivers — New Prefix Build Plan
### Step-by-step, gated. Each step ends with STOP for approval. Verify before claiming done. Clone, don't reinvent.

> **RULE 0 — REFER TO THIS MD BEFORE EVERY STEP AND BEFORE EVERY QUESTION.** At the start of each step, and before asking the user anything, re-read the relevant MD section first. Do not act from memory. Do not invent options. If the answer is in the MD, follow it; only ask the user when the MD genuinely leaves a decision open. Reading the MD is the first action of every step, every time.

> **RULE 0b — NO MOMENTUM.** Finishing a step does not start the next one. Every step boundary is a full stop regardless of context, chat history, or how natural the next action feels.

> **APPROVAL SCOPE.** A "yes" to building a step authorizes only the work named in that step. Any repo push, any Printful API call, any theme file deploy, or any other live state change requires its own explicit go-ahead. When in doubt, ask.

> **STOP GATE PROTOCOL — non-negotiable.** Every STOP is a hard wall:
>
> `STOPPED: [what was just completed]. Waiting for approval before: [exact next action — name the file, API, or tool].`
>
> Receiving a "yes" to a prior step is never approval for the next step or any push.

> **Definitions.** A *prefix* = one design concept = one Shopify product pair (Tee + Hoodie). Three independent axes — always check all three (Step 0b):
> - **Style** (font/script treatments, e.g. Classic/Heritage/Star/Retro/Watermark) → option3 = Style.
> - **Design** (distinct images, e.g. Creatures, Science) → option3 = Design; combined product with hybrid-map hero.
> - **Ink / treatment** (e.g. Navy / Red / Gold…) → line-item property, never a variant.

---

## STEP 0 — Define the prefix (no build yet)
State and get approval on EVERY item below. **Do not assume any of these — ask.**

**0a. Prefix word + lane** (faith / creature / gift / place / consumable / occasion / etc.).

**0b. Product structure — THREE QUESTIONS, always asked:**
1. Multiple STYLES? → Style option (option3). Check the master-sheet design array; multi-style unless user explicitly says ship one only.
2. Multiple distinct DESIGNS? → Combined product, Design = option3, hybrid-map hero.
3. Multiple INKS? → Ink = line-item property (NOT a variant), captured by PDP and read by fulfillment.

→ Structure:
- Single style, single ink (Crown, Stork): **Color × Size** (4 colors × 6 sizes = 24 variants). No option3.
- Multi-style (Jesus, Mom, Dad, God, America): **Color × Size × Style** (option3 = Style, e.g. 5 styles × 4 colors × 6 sizes = 120 variants). Ink = line-item property.
- Multi-design / combined (Creatures, Science): **Color × Size × Design** (option3 = Design); hybrid-map hero.

**0c. Exact styles/designs to ship** — list by name and master-sheet code. **Style display names = house adjective convention** (Classic/Heritage/Star/Retro/Watermark, Grace/Bold/Elegant, Monument/Varsity…), NEVER internal font names. Shopify Style option values MUST be display names — wrong values require a full rebuild.

**0d. Ink / treatment palette — CULL STEP (mandatory).**
- Render full palette as a numbered proof (light treatments on dark backdrop, dark on white). Standard pool: `navy`, `split` (Full Color), `red`, `black`, `gold`, `cream`, `white`, `ice`, `grey` (Heather Grey), `karmablue`.
- **`bred` (Bright Red) is ALWAYS culled** — redundant with `red`, removed from AMERICA Jun 2026. Never include.
- **`karma` is a KARMA-product-only spiral treatment key.** Never include in a standard prefix PDP valid map.
- User culls by tile number. Build only survivors.
- Reference hexes: navy `#1e3a5f`, cream `#f5f1e8`, red `#a8201a`, gold `#c08a2e`, black `#0a0a0a`, ice `#7fc4e0`, grey `#b9c0cb`, karmablue `#2f8fe2`. (Faith-lane lockup colors differ; see Step 1.)
- `split`/Full Color = navy on `_ALWAYS` + `_AD`, red on remainder. Contains BOTH navy and red.

**0e. Colors offered** — default **White, Athletic Heather, Navy, Black** unless user specifies otherwise.

**0f. Valid ink × garment-color matrix (GENERATE from contrast rule — do not eyeball).**

| Ink | White | Ath Heather | Navy | Black |
|---|---|---|---|---|
| navy, split, black | ✓ | ✓ | ✗ invisible | ✗ invisible |
| red | ✓ | ✓ | ✓ | ✓ |
| gold | ✓ | ✓ | ✓ | ✓ |
| ice | ✓ | ✓ | ✓ | ✓ |
| karmablue | ✓ | ✓ | ✗ | ✓ |
| cream | ✗ | ✗ | ✓ | ✓ |
| white | ✗ | ✗ | ✓ | ✓ |
| grey | ✗ | ✗ | ✓ | ✓ |

- **LOCKED:** navy/split/black on Navy/Black = invisible, never valid.
- **LOCKED:** cream/white/grey on White/AthHeather = invisible, never valid.
- **Watermark styles need separate dark-garment print files** for any ink valid on Navy/Black (see Step 5).
- Valid-map key: `ckey` = garment color lowercased, spaces removed (e.g. `white`, `athleticheather`, `navy`, `black`). Maps `ckey → [valid treatment keys]`.
- **Mockup count** = `Σ(valid inks per color) × styles × 2 garments`. NOT a fixed number.

**0g. Pricing** — Standard tier during build. Grand Opening 20% active: `price` = 20%-off number; `compare_at_price` = higher MAP. Fixed `.99` table in Step 4 — NEVER compute `round(sell/0.8)`.

**STOP — approve full definition (0a–0g) before any asset work.**

---

## STEP 1 — Print files
Convention (LOCKED): `printfiles/{design}/{code}_{treatment}.png`
- `{design}` = prefix slug (e.g. `america`, `dad`, `god`).
- `{code}` = master-sheet design code (e.g. `god-01`, `dad-02`, `usa-01`) — read from master sheet, never invent.
- `{treatment}` = ink key (e.g. `navy`, `red`, `grey`).

### Layout — TRIMMED-TO-CONTENT
- Render prefix word ~2010px wide.
- Render lockup at LOCK_RENDER_W = 1748px → trims to **1385px wide** (house-standard lockup width — absolute, not ratio).
- Stack: prefix on top, **GAP = 420px**, lockup centered below.
- **Crop to content bounding box.** Aspect ratio drives Printful placement. No fixed canvas.

### Condensed fonts
Size to target prefix HEIGHT matching a reference style, not width. Show side-by-side comparison before locking.

### Lockup color
Single color per treatment. General: navy `#1e3a5f` on light grounds, cream `#f5f1e8` on dark grounds; red treatment = all-red `#a8201a`. Faith lane: navy `#183048` / cream `#f0f0d8` — resolve from master sheet.

### Rendering pipeline (LOCKED)
- Install Patua One before any cairosvg render (`cp PatuaOne.ttf ~/.fonts/ && fc-cache -fv ~/.fonts`) — silently falls back to sans-serif otherwise.
- Extract lockup SVG from master sheet via Node (`wordmarkSVG(treat)`) → embed verbatim. **NEVER recompute the lockup in Python/PIL.** Pre-generate all treatment lockups to a JSON keyed by treatment.

### Naming
- **Ground-keyed** (MOM/JESUS legacy, 3-ink): `{code}_light`, `{code}_dark`, `{code}_redmono`.
- **Treatment-keyed** (DAD/GOD/AMERICA, full palette): `{code}_{treatment}.png`. Use for any multi-ink prefix.

### Audit each file
Transparent background (corner alpha = 0), lockup trims to 1385 (multi-style), single-color. Known false positive: cream/grey treatments flag near-white — accept if corners are alpha 0 and "fill" traces design strokes.

**STOP — show audited print files (embedded-image proof, hover-lens magnifier, white/dark backdrops) for approval.**

---

## STEP 2 — Mockups (Ghost, never flat-lay)
- Tee = Printful product **71** (Ghost 1120), Hoodie = product **146** (Ghost 1645).
- Naming: `mockups/{design}/{garment}_{style}_{color}_{ink}.jpg`
  - `{garment}` = `tee` or `hoodie` — **always `hoodie_` prefix, never `hood_`**
  - `{style}` = style key lowercased, no spaces (e.g. `classic`, `heritage`, `watermark`)
  - `{color}` = color key lowercased, no spaces (e.g. `white`, `athheather`, `navy`, `black`)
  - `{ink}` = treatment key (e.g. `navy`, `red`, `grey`)
- Placement: aspect ratio of print file drives fit via AREA + JESUS_BOX (see Step 6).

### Confirmed Printful variant IDs
| Color | Tee | Hoodie |
|---|---|---|
| White | 4011 | 5522 |
| Athletic Heather | 6948 | 5610 |
| Navy | 4111 | 5594 |
| Black | 4016 | 5530 |

Note: Shopify Color option = `"Athletic Heather"` for both tee and hoodie. Printful hoodie variant 5610 is internally labeled "Sport Grey" by Printful — this is Printful's name, not ours. In fulfill.py: `ckey='athleticheather'` → hoodie variant `5610`.

### Printful throttle (~1 task/min store-level)
- Submit one task → poll to `completed` → **~65s gap** → next. Two tasks within ~15s → 429.
- Build generator **resumable and repo-aware** — re-sync done list from repo at start of every run.
- Mockups do NOT block shipping. Generate card-swatch mockups first to unblock.
- **No `onerror` fallback on main PDP image** — missing = broken/pending (honest signal during audit).
- Color order in every grid: luminance-sorted lightest→darkest (White → AthHeather → Navy → Black).

**STOP — show mockup grid (or card-swatch subset) for approval.**

---

## STEP 3 — Push assets to repo
Paths: print files → `printfiles/{design}/`, mockups → `mockups/{design}/`, chips → `mockups/{design}/thumbs/`.

### GitHub Contents API protocol
```
URL:    https://api.github.com/repos/alwaysdelivers/ad-printfiles/contents/{path}
Method: PUT
Headers:
  Authorization: Bearer {PAT}        ← PAT saved at /tmp/_ghpat
  Content-Type:  application/json
  User-Agent:    AlwaysDelivers
Body:   {"message":"...", "content":"{base64}", "sha":"{existing_sha_or_omit}"}
```
- Fetch existing SHA before PUT (`GET` same URL); omit `sha` for new files; include for updates.
- Sleep ~3s after push before verify.
- **Verify by reading back via raw.githubusercontent** — CDN may lag.

### jsDelivr cache
- New file: may 404 on CDN while raw.githubusercontent = 200 (normal). Purge: `GET purge.jsdelivr.net/gh/alwaysdelivers/ad-printfiles@main/{path}`.
- **Content change:** purge alone unreliable. Always push under a NEW filename suffix (`_v2`, `_r2`, `_r3`) and update all references. Never overwrite CDN-served content in place.
- Main image URL has **no `?v=` query string** — cache-busting is handled by chip filename versioning, not query params.

**STOP — confirm all asset URLs resolve 200.**

---

## STEP 4 — Build the two Shopify products

### Shopify GraphQL protocol
```
URL:    https://rudjph-mx.myshopify.com/admin/api/2025-07/graphql.json
Header: X-Shopify-Access-Token: {token}   ← token saved at /tmp/_shoptoken
```
- Mint token: POST client_credentials grant (`client_id` + `client_secret`) to `/admin/oauth/access_token`. Save to `/tmp/_shoptoken`. ~24h lifespan.
- **Re-test `{ shop { name } }` before every batch of mutations; remint on `KeyError: 'data'`.**
- `productSet`: `synchronous:true` for ≤100 variants; `synchronous:false` + poll `productSetOperation` for >100.

### Product fields
- Title: `{Prefix} Always Delivers — Tee` / `{Prefix} Always Delivers — Hoodie`
- Handle: `{prefix}-always-delivers-tee` / `{prefix}-always-delivers-hoodie` (two separate handles)
- `templateSuffix`: `{design}`
- Options order: **1=Color, 2=Size, 3=Style|Design**. Style/Design values = display names (Step 0c).
- Category: TEE `aa-1-13-8`, HOODIE `aa-1-13-13`. Inventory `tracked:false`, policy `CONTINUE`.
- `body_html` description on both at build time.
- Publish to Online Store (publication `198208127144`).

### Pricing (Standard + Grand Opening 20%)
| | S–XL | 2XL | 3XL |
|---|---|---|---|
| Tee price / compare-at | $34.99 / $43.99 | $36.99 / $46.99 | $38.99 / $48.99 |
| Hoodie price / compare-at | $59.99 / $74.99 | $63.99 / $79.99 | $65.99 / $82.99 |

### Hero image
`productCreateMedia` (poll `status==READY`) → `productReorderMedia` position `"0"`.
Hero = `tee_classic_white_navy.jpg` / `hoodie_classic_white_navy.jpg` (or design-appropriate default style/color/ink). Ask for go-ahead separately before generating.

**STOP — verify products live via `.json`: options order, variant count, prices, hero, publication.**

---

## STEP 5 — Custom PDP section
Clone closest existing section (DAD/GOD for treatment-keyed multi-ink; MOM for ground-keyed). Re-namespace to `{ns}-` prefix.

**CSS/JS namespace `{ns}`:** choose a 4–6 char abbreviation for the prefix (e.g. `amep` for AMERICA, `dadr` for DAD, `godr` for GOD). All CSS classes and element IDs use `{ns}-` as prefix. Do NOT use `{design}p-` literally — it's a convention, not a template.

Layout: Garment toggle → main Ghost image → Style row → Ink row → Color swatches → Size → price pill → Add to cart → `{% render 'ad-pdp-footer' %}`.

Main image = jsDelivr CDN URL built from `style`, `color`, `ink` state variables. No `?v=` query string; no `onerror` fallback.

**Ink row:** primary inks first (Full Color → Navy → Red → Black), then rest. Both garment swatches AND style tiles grey + slash for invalid combos. Label row "Ink".

ATC: `/cart/add.js` with variant `id` + `properties:{Ink: <display label>}`. Cart sends DISPLAY LABEL (e.g. `"Heather Grey"`), not file key — fulfillment maps back (Step 6).

### Key PDP JS variables
| Variable | What it is |
|---|---|
| `TREATS` | JS array of all ink keys defined at top of script, e.g. `['navy','red','black','gold','white','grey','karmablue','ice']` |
| `TREAT_VALID_STD` | JS object: `ckey → [valid treatment keys]` for Classic/Heritage/Star/Retro styles |
| `TREAT_VALID_WM` | Same structure but for Watermark style only (different valid map) |
| `CFG.colorOrder` | Array of garment display names in luminance order, from embedded JSON config block |
| `PLACEHOLDER_URL` | Hardcoded CDN URL for the default preview: `CDN_BASE + 'mockups/{design}/tee_classic_white_navy.jpg'` (or design-appropriate default) |

### ⚠ IIFE SCOPE TRAP (LOCKED)
The section script is wrapped in `(function(){...})()`. **Any function defined inside is invisible to inline HTML `onclick` attributes.** Always expose via `window.fn=fn`:
```javascript
function resetPDP(){...}
window.resetPDP=resetPDP;  // required — onclick="resetPDP()" silently fails without this
```

### Empty/reset state (LOCKED)
On page load and after Reset: `treat=null`, `color=null`, `style='Classic'`. All ink buttons and garment swatches show with none selected, no slashes. Placeholder image always visible. ATC shows "Select ink + garment color".

**Six locations require null-state guards — ALL must be present:**
1. `getValid()`: `if(!color) return TREATS;` — all inks enabled when no garment selected
2. `treatUrl()`: `if(!treat||!color) return PLACEHOLDER_URL;` — placeholder always visible
3. `sync()` auto-snap: `if(color && treat && getValidForColor(color).indexOf(treat)<0){...}` — guard with both
4. `renderTreat()` snap: `if(treat && valid.indexOf(treat)<0){treat=getDefault();}` — skip snap when null
5. `styleAvail = treat ? (styleValid.indexOf(treat)>=0) : true` — all style tiles enabled when null
6. `colorOk = treat ? (getValidForColor(c).indexOf(treat)>=0) : true` — all swatches enabled when null; `b.disabled = treat ? !colorOk : false`

**Reset / defaultColorForTreat:**
```javascript
function defaultColorForTreat(t){
  var valid=CFG.colorOrder.filter(function(c){return (TREAT_VALID_STD[c]||[]).indexOf(t)>=0;});
  return valid.indexOf('White')>=0?'White':(valid[0]||'White');
}
function resetPDP(){style='Classic';treat=null;color=null;sync();}
window.resetPDP=resetPDP;
```
- `setTreat(v)`: **first** `if(getValid().indexOf(v)<0)return;` then `treat=v;` then if `!color` → `color=defaultColorForTreat(v);` then `sync()`.
- `syncSize()`: if `!size`, find and click M button before rendering.
- Reset button: `<button onclick="resetPDP()">↺ Reset</button>`, navy bg, hover red.

### Garment color swatches — invalid-ink disable (LOCKED)
```css
.{ns}-sw button.dis{opacity:.4;cursor:not-allowed;position:relative;}
.{ns}-sw button.dis::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;border-radius:50%;
  background:linear-gradient(135deg,transparent 44%,rgba(168,32,26,.85) 44%,rgba(168,32,26,.85) 56%,transparent 56%);
  pointer-events:none;}
```
- `getValidForColor(c)`: `return (style==='Watermark'?TREAT_VALID_WM:TREAT_VALID_STD)[c]||[];`
- `b.disabled=treat?!colorOk:false;` — unclickable when disabled; `b.onclick=null` when invalid
- Auto-snap in `sync()`: `if(color&&treat&&getValidForColor(color).indexOf(treat)<0)` → snap to first valid color

### Style tiles — invalid-ink disable (LOCKED)
```css
.{ns}-stthumb{...;position:relative;}  /* position:relative required or slash won't overlay */
.{ns}-stthumb.dis{opacity:.3;cursor:not-allowed;pointer-events:none;}
.{ns}-stthumb.dis::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:linear-gradient(135deg,transparent 44%,rgba(168,32,26,.7) 44%,rgba(168,32,26,.7) 56%,transparent 56%);
  pointer-events:none;}
```
- `styleAvail = treat ? (styleValid.indexOf(treat)>=0) : true`
- `b.disabled = treat ? !styleAvail : false`

### Chip versioning (LOCKED)
- **Never overwrite an existing chip filename.** CDN caches content; stale content under an old name persists even after purge. Use new suffix (`_r2`, `_r3`, etc.) on every content change.
- Chip URL builder (current suffixes — increment on next regeneration):
  `['white','grey'].indexOf(chipTreat)>-1 ? '_chip_v2_r2.jpg' : '_chip_r2.jpg'`
- **Per-style chipTreat** (null or invalid → first valid for that style):
  `var chipTreat=treat?((styleValid.indexOf(treat)>=0)?treat:(styleValid[0]||'navy')):(styleValid[0]||'navy');`
- **⚠ SPLIT INK TRAP (LOCKED — do not deviate):** `split` (Full Color) has NO CDN chip file. It is ALWAYS base64 from `CFG.sw[s]`, keyed per style name. `CFG.sw` contains one base64 entry per style (e.g. `{"Classic":"/9j/…","Varsity":"/9j/…","Retro":"/9j/…"}`). The correct `thumbSrc` condition is:
  ```javascript
  var thumbSrc = (treat === 'split')
    ? ('data:image/jpeg;base64,' + CFG.sw[s])   // ALL style tiles use base64 when split selected
    : ('…CDN…' + s.toLowerCase() + '_' + chipTreat + suffix);
  ```
  **NEVER** add `&& s === style` to the split condition — that would show base64 only for the selected tile and attempt a CDN fetch (404) for all others. **NEVER** add a fallback that overwrites `chipTreat` from `'split'` to a CDN ink — that is the same bug in reverse.
- Watermark dark chips: navy bg (`_chip_v2_r2.jpg`) for light inks (white/grey/ice); white bg (`_chip_r2.jpg`) for mid inks (gold/karmablue). If CDN still serves stale after purge, push as `_r3` and add special case to URL builder.

### Chips — canonical build rules
- 440×338 canvas, built from print art (never from a mockup).
- Full Color chip = base64 in PDP config `sw`, built from `_split` print art. Must contain both navy and red pixels. **`sw` is a per-style object — every style name is a key** (e.g. `sw.Classic`, `sw.Varsity`, `sw.Retro`). All style tiles show their own `sw[s]` chip when `split` is selected — not just the active style.
- **Composite correctly** — direct RGBA paste, convert RGB at save only:
  ```python
  chip = Image.new('RGBA', (440,338), (255,255,255,255))
  chip.paste(crop_r, ((440-w2)//2, (338-h2)//2), mask=crop_r.split()[3])  # direct paste
  chip.convert('RGB').save(buf, 'JPEG', quality=82)                         # convert at save
  ```
  Intermediate RGB canvas silently drops alpha → blank chip.
- Light-ink chips (white/cream/grey): navy background `#1e3a5f`.

### Watermark dark-garment print files (LOCKED)
When an ink is valid for Watermark on Navy/Black garments, a separate `watermark_{ink}_dark.png` is needed. Light-garment Watermark uses the original `watermark_{ink}.png`; dark garments route to the dark variant.

**Generation pattern:**
- Load the light-garment watermark print file `watermark_{ink}.png` as source (AMERICA source = `watermark_red.png` for structure reference; adapt pixel channels for each ink)
- Pixels fully opaque + AMERICA-dominant color = AMERICA text → replace with ink color, opaque
- Pixels fully opaque + lockup-dominant color = lockup text → replace with ink color, opaque
- Pixels semi-transparent = USA ghost → replace with contrasting color at chosen opacity
- Save as `printfiles/{design}/watermark_{ink}_dark.png`
- **Z-order note:** AMERICA and USA occupy DIFFERENT pixel positions (zero overlap). Changing z-order has no effect — requires SVG-layer regeneration.

**Approved dark variants (AMERICA):**
| Ink | AMERICA color | USA ghost | Opacity |
|---|---|---|---|
| red | #a8201a | white | 80% |
| gold | #c08a2e | cream #f5f1e8 | 75% |
| white | #ffffff | red #a8201a | 80% |
| karmablue | #2f8fe2 | white | 100% |
| grey | #b9c0cb | red #a8201a | 80% |

**Fulfill.py routing** (add after standard `fp=...` for Watermark):
```python
if st=='watermark' and tk=='{ink}' and ckey not in ('white','athleticheather','sportgrey'):
    fp='printfiles/{design}/watermark_{ink}_dark.png'
```

### Deep-link reader
MANDATORY in BOOT `ensure()` callback only — reads `?variant=`, preselects style/color/ink, falls back to defaults. Never in garment-toggle callback.

**Validate JS with `node --check` before push. Verify deployed file via GraphQL API readback. File size < 200KB.**

**STOP — show PDP working (all selectors, chips change with ink, empty state, reset button, deep-link) for approval.**

---

## STEP 6 — Fulfillment (fulfill.py)

### Printful API protocol
```
Header: Authorization: Bearer {TOKEN}   ← token saved at /tmp/_printfultoken
Mockup: POST https://api.printful.com/mockup-generator/create-task/{product_id}
Poll:   GET  https://api.printful.com/mockup-generator/task?task_key={tk}
```

### fulfill.py routing variables
| Variable | Meaning |
|---|---|
| `st` | Style key — `norm(style_option_value)` = lowercased, spaces stripped (e.g. `'watermark'`, `'classic'`) |
| `tk` | Treatment key — looked up from `{DESIGN}_INK[label.lower()]` (e.g. `'grey'`, `'karmablue'`) |
| `ckey` | Color key — garment color option value lowercased, spaces stripped (e.g. `'athleticheather'`, `'black'`) |
| `label` | Ink display label from cart line-item property `Ink` (e.g. `'Heather Grey'`, `'Full Color'`) |

### Maps needed (clone DAD/GOD)
- `{DESIGN}_STYLES` — `norm(Style)` → `(file_code, aspect_w_h)` e.g. `'classic':('usa-01', 2010/1363)`
- `{DESIGN}_INK` — display label (lowercased) → treatment key e.g. `'heather grey':'grey'`, `'full color':'split'`
- `{DESIGN}_VALID` — `ckey → [valid treatment keys]` (from Step 0f valid map)
- `{DESIGN}_DEFAULT` — `ckey → fallback treatment` when ink missing or invalid

**Resolution:** `tk=INK.get(label.lower())`; if None or `tk not in VALID[ckey]` → `tk=DEFAULT[ckey]`.

**Watermark dark routing** (add after standard `fp=...` line):
```python
if st=='watermark' and tk=='{ink}' and ckey not in ('white','athleticheather','sportgrey'):
    fp='printfiles/{design}/watermark_{ink}_dark.png'
```

**Placement** (global constants — same for every prefix):
```python
AREA = {'tee':(1800,2400), 'hoodie':(2100,2100)}
JESUS_BOX = {'tee':(1250,1100,480), 'hoodie':(1250,1100,470)}  # (maxw, maxh, top)
# Usage: aw,ah=AREA[g]; maxw,maxh,top=JESUS_BOX[g]; fit by aspect; left=(aw-w)//2
```
Athletic Heather hoodie → Printful variant `5610` (Printful calls it "Sport Grey" internally — use `ckey='athleticheather'` in routing, variant id `5610` for hoodie API call).

Edit fulfill.py by parse/replace + `py_compile` check; additive only (don't touch existing handlers).

**Dry-run every valid color × ink × style × garment against live repo; assert each URL = 200.**

**STOP — show dry-run 200-OK for all routings + fallbacks. Awaiting explicit push approval.**

---

## STEP 7 — Home grid + Shop All wiring
**Home grid (`front-grid.liquid`) — 8 tiles only.**
Combined product? Add to `FG_HYBRID` map + handle to `unless` skip-list. Single/style-only: no entry needed.

**Shop All (`ad-all-prefixes.liquid`):**
- One card per distinct design (e.g. 4 creatures, 4 science, 2 crosses = 10 cards total).
- Card needs 8 swatch mockups (4 colors × 2 garments) in hero style + default ink per color.
- Card schema: `name`, `tee_url`, `hoodie_url`, `colors[]` with keys `label`/`hex`/`tee`/`hoodie` (jsDelivr URLs — **`hoodie_` filename prefix**), Standard prices.
- **Insert via JSON parse → append → re-serialize → `node --check`. NEVER regex into the array.**

**Button count sync:** bump `ad_prefix_count` to equal Shop All card count.

**STOP — show rendered Shop All card (embedded-image proof) before push.**

---

## STEP 8 — Master sheet
**CURRENTLY SKIPPED per standing instruction.** Do not update during a build unless user explicitly asks.

---

## STEP 9 — Final done-checklist (verify each, live/API)
- [ ] Print files in `printfiles/{design}/` — trimmed-to-content, 1385 lockup (multi-style), transparent bg, single-color, {code} from master sheet
- [ ] Mockups generated + pushed; all URLs 200. Card swatches + heroes priority; backfill in progress is acceptable.
- [ ] Chips: light inks (white/cream/grey) on navy `_chip_v2_r2`; per-style chipTreat fallback correct; watermark dark chips exist for all valid dark-garment ink variants; all resolve 200
- [ ] Both products live: options Color/Size/Style order, correct variant count, Standard prices, hero set via `productCreateMedia` → poll READY → `productReorderMedia` position `"0"`
- [ ] `templateSuffix` set; PDP: all selectors render; chips change with ink; empty state correct (no ink/garment, placeholder shown, ATC = "Select ink + garment color"); reset button working; M pre-selected on size; deep-link works; `node --check` passed; <200KB
- [ ] Ink × garment × style audit: all valid combos have mockups; invalid combos slash/grey on PDP; `bred` and `karma` absent
- [ ] Watermark dark: print files exist for all valid dark-garment inks; routing in fulfill.py; chips exist
- [ ] fulfill.py: every valid combo routes to existing print file (dry-run 200); Watermark dark routing present; fallbacks correct; `py_compile` passed
- [ ] Valid-map consistent between PDP (TREAT_VALID_STD/WM) and fulfill.py ({DESIGN}_VALID)
- [ ] Home: 8 tiles; combined product in FG_HYBRID locked to hero; swatches luminance-sorted
- [ ] Shop All: card added with `hoodie_url`/`hoodie` keys; Standard prices; `node --check` passed; `ad_prefix_count` bumped
- [ ] Every push verified by reading deployed file back via API (not storefront — cache lags)

---

## Quick reference — locked constants
- **Shop:** `rudjph-mx.myshopify.com` · GraphQL 2025-07 · Theme `153615171752` · Publication `198208127144` · Home collection `345953960104`
- **Shopify token:** mint client_credentials (client_id `0262c5cd202eae65b92affa414c2aa84` + secret) → save `/tmp/_shoptoken`; header `X-Shopify-Access-Token: {token}`; ~24h; remint on `KeyError:'data'`
- **GitHub:** repo `alwaysdelivers/ad-printfiles` · PAT → `/tmp/_ghpat` · headers: `Authorization: Bearer {PAT}`, `User-Agent: AlwaysDelivers` · Contents API base: `https://api.github.com/repos/alwaysdelivers/ad-printfiles/contents/`
- **CDN:** `https://cdn.jsdelivr.net/gh/alwaysdelivers/ad-printfiles@main/` · RAW: `https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/` · Purge: `https://purge.jsdelivr.net/gh/alwaysdelivers/ad-printfiles@main/{path}`
- **Printful:** store `18259192` · token → `/tmp/_printfultoken` · header `Authorization: Bearer {TOKEN}` · Tee product `71` · Hoodie product `146` · throttle ~1 task/min store-level
- **Variant IDs:** White tee=4011/hoodie=5522 · AthHeather tee=6948/hoodie=5610 · Navy tee=4111/hoodie=5594 · Black tee=4016/hoodie=5530
- **Categories:** TEE `aa-1-13-8` · HOODIE `aa-1-13-13`
- **Placement:** AREA tee=(1800,2400) hoodie=(2100,2100) · JESUS_BOX tee=(1250,1100,480) hoodie=(1250,1100,470)
- **Color hexes:** White `#ffffff` · AthHeather `#b9c0cb` · Navy `#1e3a5f` · Black `#1a1a1a`
- **Combined products (hybrid map):** Creatures, Cross, Karma, Jesus, Faith, Science
- **Hoodie convention:** `hoodie_` everywhere — `hood_`, `HOODIE_` all retired
- **Sister docs:** `AD_BUILD_AND_DISPLAY_STANDARD.md` (design standards) · `tools/AD_Eyeball.html` (on-model placement verification)

---

## Reference builds (clone these)
- **Multi-style, treatment-keyed, full palette:** DAD (Classic/Varsity/Retro; 7 inks), GOD (Monument/Bold/Retro; 7 inks)
- **Multi-style, multi-ink, Watermark + dark variants:** AMERICA (Classic/Heritage/Star/Retro/Watermark; 8 inks) — clone for any prefix with Watermark style
- **Multi-style, ground-keyed (3-ink):** MOM, JESUS
- **Combined multi-design:** Creatures, Science (FG_HYBRID hero lock)
- **Single-style:** Crown, Stork (Color × Size only)

---

## Process discipline (binding)
- ONE task/decision at a time; give the exact next step, then STOP.
- ASK before ANY commit/push, Printful call, theme deploy, or live state change.
- Read from LIVE sources + this MD. Verify via GraphQL API (authoritative); storefront cache-lags.
- Present numbered options; never decide what's the user's to decide. Compute from measured specs — never eyeball.
- Proofs: openable HTML, cursor-following hover-lens magnifier, white background, base64-embedded. Never inline images in chat.
- **Migrations/renames:** create-new → verify resolves → repoint references → verify clean → ONLY THEN delete old. Audit dynamic URL construction, not just literal strings.
- Own mistakes tersely; re-read exact changed bytes before claiming done.

---

## STANDARDIZE EXISTING PREFIXES — Backport protocol

Six live multi-ink prefixes need backporting to current standards. Do ONE prefix per session. Do NOT start the next until current is complete and verified.

### Priority order (easiest → hardest)
1. **DAD** — has valid_map; missing empty/reset state, chip_r2, per_style_chip, getValidForColor
2. **GOD** — same as DAD
3. **MOM** — missing valid_map + all of the above
4. **FAITH** — same as MOM
5. **JESUS** — most styles/treatments, missing everything
6. **CROSS** — same as JESUS

### Pre-work for every prefix (MANDATORY before touching anything)
1. Fetch the live section via theme GraphQL API — read it in full
2. Extract and `node --check` the existing script block
3. Identify the existing namespace (`{ns}-`), variable names (`treat`/`ink`/`color`), and TREATS array
4. Note what valid-map structure exists (or doesn't)
5. Record the current chip URL builder pattern and suffix

### What NOT to change
- Do not rename variables, restructure the IIFE, or change working patterns
- Do not alter existing valid maps if present — only ADD to them
- Do not change the ATC, variant lookup, or deep-link reader
- Additive only — surgically insert new patterns, leave everything else intact

### Backport checklist (run in this order, STOP after each, verify before continuing)

**STOP A — valid map (only for MOM, FAITH, JESUS, CROSS)**
- Read all existing ink×garment combinations from current section + master sheet
- Build `TREAT_VALID_STD = { ckey: [treatments] }` from actual combinations
- Add `getValid()` using the map; add `getValidForColor(c)` helper
- Verify: `node --check`; verify `getValidForColor('white')` returns correct treatments
- STOP — show valid map for approval before pushing

**STOP B — empty/reset state (all 6 prefixes)**
Apply all 6 null-state guards (see Step 5 — Empty/reset state):
1. `getValid()`: add `if(!color) return TREATS;` at top
2. `treatUrl()`: add `if(!treat||!color) return PLACEHOLDER_URL;` — set PLACEHOLDER_URL = CDN URL for `{garment}_classic_{default_color}_{default_ink}.jpg` (or equivalent first style/color/ink combo for that prefix)
3. `sync()` auto-snap: guard with `if(color && treat && ...)`
4. `renderTreat()` snap: guard with `if(treat && ...)`
5. `styleAvail = treat ? ... : true`
6. `colorOk = treat ? ... : true`; `b.disabled = treat ? !colorOk : false`
Add `defaultColorForTreat()`, update `setTreat()` (guard first, then auto-snap), update `syncSize()` (M pre-select), add `resetPDP()` + `window.resetPDP=resetPDP`, add Reset button to HTML.
- Verify: `node --check`; load PDP; confirm all options show, none selected, placeholder visible, M pre-selected, Reset works
- STOP — show PDP screenshot for approval before pushing

**STOP C — chip versioning (all 6 prefixes)**
- Identify current chip suffix (likely no `_r2`)
- Push new chips under `_r2` suffix for any inks that need it
- Update chip URL builder to use `_r2` suffix
- Add per-style chipTreat: `var chipTreat=treat?((styleValid.indexOf(treat)>=0)?treat:(styleValid[0]||'navy')):(styleValid[0]||'navy');`
- Note: light-ink chips (white/cream/grey) must use `_chip_v2_r2.jpg` on navy background
- **If prefix has `split` ink:** `thumbSrc` must be `(treat==='split') ? base64_CFG.sw[s] : CDN`. No `&& s===style` qualifier. No CDN fallback for split. Verify all three style tiles show Full Color chip when split selected — not just the active tile.
- Verify: chips load correctly for all inks × styles on PDP
- STOP — verify chips before pushing

### Verification after all stops
- `node --check` on final section
- Load PDP fresh: empty state correct, chips work, reset works, deep-link works
- Verify deployed file via GraphQL API readback (not storefront)

### Per-prefix notes
| Prefix | Namespace | Styles | Has valid_map | Notes |
|---|---|---|---|---|
| DAD | `dadr-` or similar | Classic/Varsity/Retro | ✓ | Read existing map before adding guards |
| GOD | `godr-` or similar | Monument/Bold/Retro | ✓ | Read existing map before adding guards |
| MOM | mom namespace | Grace/Bold/Elegant/Retro | ✗ | Ground-keyed (light/dark/red) — build STD map from existing combos |
| FAITH | faith namespace | 1–2 styles | ✗ | Confirm style count before building map |
| JESUS | jes namespace | Grace/Script/Bold/Retro + cross | ✗ | Most complex — read section fully before planning |
| CROSS | cross namespace | same as JESUS | ✗ | Clone JESUS backport once JESUS is done |

