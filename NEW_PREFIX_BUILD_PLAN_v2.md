# AlwaysDelivers — Prefix Build & Backport Plan
### Step-by-step, gated. Each step ends with STOP for approval. Verify before claiming done.

---

## BINDING RULES — READ BEFORE EVERY ACTION

> **RULE 0 — READ THIS MD FIRST.** At the start of every step and before every question, re-read the relevant section. Do not act from memory. Do not invent options. If the answer is here, follow it. Only ask when the MD genuinely leaves a decision open.

> **RULE 0b — NO MOMENTUM.** Finishing a step does not start the next one. Every step boundary is a full stop. Do not pre-stage, do not frame "next I'll...", do not run STOP A through C in one script. One action. Report result. Wait.

> **RULE 0c — ONE PUSH PER RESPONSE.** Each Shopify deploy, GitHub push, or Printful API call is a separate action requiring its own explicit go-ahead. A "yes" to STOP A is not approval for STOP B or any push. A "yes" to STOP B is not approval for the section deploy.

> **RULE 0d — APPROVAL SCOPE IS EXACT.** `STOPPED: [what was just completed]. Waiting for approval before: [exact next action — name the file, API, or tool].` Receiving a "yes" to a prior step is never approval for the next step.

> **RULE 0e — NEVER DECIDE WHAT IS ATI'S TO DECIDE.** Present numbered options. Wait. Never choose on her behalf.

> **RULE 0f — NEVER EYEBALL. DO THE MATH.** Compute from measured specs. Show numbers.

> **RULE 0g — READ FROM LIVE SOURCES.** Every section fetch must be a live API call in the current response. Never rely on memory, transcript summary, or prior response content.

---

## MANDATORY PRE-PUSH VERIFICATION OATH

Before any section deploy or file push, confirm all six statements are true. If any is false, do not push — fix it first.

1. **I fetched the live section from Shopify via API in this response** — not from memory or /tmp cache.
2. **Every string I replaced was found via `assert` in the script** — not assumed to be present.
3. **`node --check` passed** on the extracted IIFE with the current line range.
4. **CDN HEAD-check passed (200) on every file the section references** — PLACEHOLDER_URL, all chip files, sample treatUrls. A 200 on raw.githubusercontent is NOT sufficient.
5. **Boot sequence walkthrough completed** — traced t=0 through reset, confirmed no blank states or broken URLs.
6. **I have not taken any action beyond what was explicitly approved in the immediately preceding message.**

---

## MANDATORY BOOT SEQUENCE WALKTHROUGH

Run this before every section push. Trace each stage:

- **t=0ms:** Hero `<img>` has no src. Is `_ph.src=PLACEHOLDER_URL` set before `ensure()` fires? If not, add it.
- **ensure() async fetch:** `prod()` returns null → `renderStyle()` exits immediately → no chips. Acceptable only if fast.
- **ensure() resolves → sync():** `setImg(treatUrl())`. `treat=null` → returns `PLACEHOLDER_URL`. Confirm PLACEHOLDER_URL is 200 on CDN.
- **renderStyle():** chips render. Confirm `CFG.sw` has base64 for all styles. Confirm all CDN chip files are 200.
- **renderTreat():** all buttons show, none selected (`treat=null`). Confirm `.dis` logic is correct for null state.
- **syncSize():** M pre-selected. ATC shows "Select ink + garment color".
- **User selects ink → setTreat() → sync() → setImg(treatUrl()):** URL matches actual filenames in repo. Verify one sample URL live.
- **Reset → resetPDP():** garment resets to tee, treat/color/size null, hero shows PLACEHOLDER, chips show fc base64.

**Cross-check against DAD (known-good):** After tracing, open DAD section and compare its boot sequence line by line. Any divergence is a bug candidate.

---

## DEFINITIONS

A *prefix* = one design concept = one Shopify product pair (Tee + Hoodie). Three independent axes — always check all three:
- **Style** (font/script treatments, e.g. Classic/Heritage/Star/Retro/Watermark) → option3 = Style.
- **Design** (distinct images, e.g. Creatures, Science) → option3 = Design; combined product with hybrid-map hero.
- **Ink / treatment** (e.g. Navy / Red / Gold…) → line-item property, never a variant.

Product structures:
- Single style, single ink (Crown, Stork): **Color × Size** (4×6 = 24 variants). No option3.
- Multi-style (Jesus, Mom, Dad, God, America, Faith): **Color × Size × Style** (option3 = Style). Ink = line-item property.
- Multi-design / combined (Creatures, Science, Cross): **Color × Size × Design** (option3 = Design); hybrid-map hero.

---

## STEP 0 — Define the prefix (no build yet)

State and get approval on EVERY item below. Do not assume any of these — ask.

**0a. Prefix word + lane** (faith / creature / gift / place / consumable / occasion / etc.)

**0b. Product structure — THREE QUESTIONS:**
1. Multiple STYLES? → Style option (option3). Check master-sheet design array.
2. Multiple distinct DESIGNS? → Combined product, Design = option3, hybrid-map hero.
3. Multiple INKS? → Ink = line-item property (NOT a variant), captured by PDP and read by fulfillment.

**0c. Exact styles/designs to ship** — list by name and master-sheet code. Style display names = house adjective convention (Classic/Heritage/Star/Retro/Watermark, Grace/Bold/Elegant, Monument/Varsity…). NEVER internal font names. Shopify Style option values MUST be display names — wrong values require a full rebuild.

**0d. Ink / treatment palette — CULL STEP (mandatory).**
- Render full palette as numbered proof (light treatments on dark backdrop, dark on white). Standard pool: `navy`, `split` (Full Color), `red`, `black`, `gold`, `cream`, `white`, `ice`, `grey` (Heather Grey), `karmablue`.
- **`bred` (Bright Red) ALWAYS culled** — retired Jun 2026. Never include.
- **`karma` is KARMA-product-only.** Never include in a standard prefix PDP.
- User culls by tile number. Build only survivors.
- Reference hexes: navy `#1e3a5f`, cream `#f5f1e8`, red `#a8201a`, gold `#c08a2e`, black `#0a0a0a`, ice `#7fc4e0`, grey `#b9c0cb`, karmablue `#2f8fe2`. Faith-lane lockup colors differ; see Step 1.
- `split`/Full Color = navy on `_ALWAYS` + `_AD`, red on remainder. Contains BOTH navy and red.

**0e. Colors offered** — default White, Athletic Heather, Navy, Black unless user specifies otherwise.

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
- Valid-map key: `ckey` = garment color lowercased, spaces removed (`white`, `athleticheather`, `navy`, `black`).
- **Mockup count** = `Σ(valid inks per color) × styles × 2 garments`. NOT a fixed number.

**0g. Pricing** — Standard tier. Grand Opening 20% active: `price` = 20%-off number; `compare_at_price` = higher MAP. Fixed `.99` table in Step 4.

**STOP — approve full definition (0a–0g) before any asset work.**

---

## STEP 1 — Print files

Convention (LOCKED): `printfiles/{design}/{code}_{treatment}.png`
- `{design}` = prefix slug (e.g. `america`, `dad`, `god`).
- `{code}` = master-sheet design code (e.g. `god-01`, `dad-02`) — read from master sheet, never invent.
- `{treatment}` = ink key (e.g. `navy`, `red`, `grey`).

### Layout — TRIMMED-TO-CONTENT
- Render prefix word ~2010px wide.
- Render lockup at LOCK_RENDER_W = 1748px → trims to **1385px wide** (house-standard lockup width — absolute, not ratio).
- Stack: prefix on top, **GAP = 420px**, lockup centered below.
- **Crop to content bounding box.** Aspect ratio drives Printful placement. No fixed canvas.

### Lockup color
Single color per treatment. General: navy `#1e3a5f` on light grounds, cream `#f5f1e8` on dark grounds; red treatment = all-red `#a8201a`. Faith lane: navy `#183048` / cream `#f0f0d8` — resolve from master sheet.

### Rendering pipeline (LOCKED)
- Install Patua One before any cairosvg render (`cp PatuaOne.ttf ~/.fonts/ && fc-cache -fv ~/.fonts`).
- Extract lockup SVG from master sheet via Node (`wordmarkSVG(treat)`) → embed verbatim. **NEVER recompute the lockup in Python/PIL.**

### Naming
- **Ground-keyed** (MOM/JESUS legacy, 3-ink): `{code}_light`, `{code}_dark`, `{code}_redmono`.
- **Treatment-keyed** (DAD/GOD/AMERICA, full palette): `{code}_{treatment}.png`.

### Audit each file
Transparent background (corner alpha = 0), lockup trims to 1385 (multi-style), single-color.

**STOP — show audited print files (embedded-image proof, hover-lens magnifier, white/dark backdrops) for approval.**

---

## STEP 2 — Mockups (Ghost, never flat-lay)

- Tee = Printful product **71**, Hoodie = product **146**.
- Naming: `mockups/{design}/{garment}_{style}_{color}_{ink}.jpg`
  - `{garment}` = `tee` or `hoodie` — **always `hoodie_` prefix, never `hood_`**
  - `{style}` = style code from SC map (e.g. `faith-01`, `dad-02`) — NOT display name, NOT lowercased display name
  - `{color}` = `White`, `AthHeather`, `Navy`, `Black` — exact casing, no spaces (AthHeather not athheather)
  - `{ink}` = treatment key (e.g. `fc`, `mono`, `red`, `navy`, `split`)

### PRINT FILE PLACEMENT — FULL-FRAME vs TRIMMED-CONTENT (LOCKED)

**Class A — Trimmed-content (JESUS_BOX):** Print file art fills most of the 4500×5400 canvas. Use JESUS_BOX:
```python
AREA = {'tee':(1800,2400), 'hoodie':(2100,2100)}
JESUS_BOX = {'tee':(1250,1100,480), 'hoodie':(1250,1100,470)}  # (maxw, maxh, top)
aw,ah=AREA[g]; maxw,maxh,top=JESUS_BOX[g]
if aspect>=maxw/maxh: w=maxw; h=int(maxw/aspect)
else: h=maxh; w=int(maxh*aspect)
left=(aw-w)//2
```
Examples: DAD, GOD, MOM, AMERICA.

**Class B — Full-frame (CROWN_AR):** Print file is full 4500×5400 canvas; art occupies only a portion. Aspect is always 0.8333. Use:
```python
CROWN_AR=4500.0/5400.0
aw,ah=AREA[g]
if aw/ah<=CROWN_AR: w=aw; h=int(aw/CROWN_AR)
else: h=ah; w=int(ah*CROWN_AR)
top=(ah-h)//2; left=(aw-w)//2
```
Examples: FAITH, CROWN.

**How to determine class:** Download the print file. Measure pixel content bounding box. If art fills >80% of canvas → Class A. If art occupies a small portion with significant whitespace → Class B. **Do NOT use the `aspect` from `fulfill.py STYLES` dict for Printful placement of full-frame files — that aspect is for fulfill.py's internal fit calculation only.**

**NEVER use JESUS_BOX on a full-frame print file. NEVER use CROWN_AR on a trimmed-content print file.**

### Confirmed Printful variant IDs
| Color | Tee | Hoodie |
|---|---|---|
| White | 4011 | 5522 |
| Athletic Heather | 6948 | 5610 |
| Navy | 4111 | 5594 |
| Black | 4016 | 5530 |

Note: Printful hoodie variant 5610 is internally "Sport Grey" — our name is Athletic Heather. Use `ckey='athleticheather'` in routing.

### Before generating mockups
1. Inventory what already exists in `mockups/{design}/` via GitHub API — do not regenerate existing files
2. List exactly which files are missing
3. Report the list and await approval before submitting any Printful tasks

### Printful throttle
Submit one task → poll to `completed` → **65s gap** → next. Two tasks within ~15s → 429.

### After generating mockups — CDN resolution gate
After pushing each mockup file, HEAD-check on `cdn.jsdelivr.net` before referencing it anywhere. A 200 on `raw.githubusercontent.com` does NOT mean CDN is ready.

**STOP — show mockup approval grid (openable HTML, hover-lens magnifier, white background, base64-embedded) for approval. Never show images inline in chat.**

---

## STEP 3 — Push assets to repo

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
- Fetch existing SHA before PUT; omit `sha` for new files; include for updates.
- Verify by reading back via raw.githubusercontent immediately after push.

### jsDelivr cache rules (LOCKED)
- **New file:** may 404 on CDN while raw.githubusercontent = 200. Purge: `GET purge.jsdelivr.net/gh/alwaysdelivers/ad-printfiles@main/{path}`.
- **Content change:** purge alone unreliable. Always push under a NEW filename suffix (`_v2`, `_r2`, `_r3`). Never overwrite CDN-served content in place.
- **403 on CDN:** permanent cache of a failed state. Purge will NOT fix it. Only fix: push under a completely new filename that jsDelivr has never seen.
- **Main image URLs:** no `?v=` query string — ever. Cache-busting via chip filename versioning only.

**STOP — confirm all asset URLs resolve 200 on CDN.**

---

## STEP 4 — Build the two Shopify products

### Shopify GraphQL protocol
```
URL:    https://rudjph-mx.myshopify.com/admin/api/2025-07/graphql.json
Header: X-Shopify-Access-Token: {token}   ← token saved at /tmp/_shoptoken
```
- Re-test `{ shop { name } }` before every batch of mutations; remint on `KeyError: 'data'`.
- `productSet`: `synchronous:true` for ≤100 variants; `synchronous:false` + poll for >100.

### Product fields
- Title: `{Prefix} Always Delivers — Tee` / `{Prefix} Always Delivers — Hoodie`
- Handle: `{prefix}-always-delivers-tee` / `{prefix}-always-delivers-hoodie`
- `templateSuffix`: `{design}`
- Options order: **1=Color, 2=Size, 3=Style|Design**. Values = display names.
- Category: TEE `aa-1-13-8`, HOODIE `aa-1-13-13`. Inventory `tracked:false`, policy `CONTINUE`.
- `body_html` on both at build time.
- Publish to Online Store (publication `198208127144`).

### Pricing (Standard + Grand Opening 20%)
| | S–XL | 2XL | 3XL |
|---|---|---|---|
| Tee price / compare-at | $34.99 / $43.99 | $36.99 / $46.99 | $38.99 / $48.99 |
| Hoodie price / compare-at | $59.99 / $74.99 | $63.99 / $79.99 | $65.99 / $82.99 |

**STOP — verify products live via `.json`: options order, variant count, prices, hero, publication.**

---

## STEP 5 — Custom PDP section

Clone closest existing section. Re-namespace to `{ns}-` prefix.

Layout: Garment toggle → main Ghost image → Style row → Ink row → Color swatches → Size → price pill → Add to cart → `{% render 'ad-pdp-footer' %}`.

Main image = jsDelivr CDN URL. **No `?v=` query string. No `onerror` fallback.**

ATC: `/cart/add.js` with variant `id` + `properties:{Ink: <display label>}`. Cart sends DISPLAY LABEL, not file key.

### Key PDP JS variables
| Variable | What it is |
|---|---|
| `TREATS` | Array of all ink keys e.g. `['navy','red','black','grey','karmablue','ice']` |
| `TREAT_VALID` | Object: `ckey → [valid treatment keys]` |
| `TREAT_DEFAULT` | Object: `ckey → fallback treatment` |
| `TREAT_LABEL` | Object: `treat key → display label` e.g. `{grey:'Heather Grey', karmablue:'Neon Blue'}` |
| `PLACEHOLDER_URL` | CDN URL for default preview image; shown when treat=null or color=null |

### IIFE scope trap (LOCKED)
The section script is wrapped in `(function(){...})()`. Any function defined inside is invisible to inline HTML `onclick` attributes. Always expose via `window.fn=fn`:
```javascript
function resetPDP(){...}
window.resetPDP=resetPDP;  // required — onclick="resetPDP()" silently fails without this
```

### Empty/reset state (LOCKED)
On page load and after Reset: `treat=null`, `color=null`, `style='Classic'`. All ink buttons and garment swatches show with none selected, no slashes. Placeholder image visible. ATC shows "Select ink + garment color".

**Six locations require null-state guards — ALL must be present:**
1. `getValid()`: `if(!color) return TREATS;`
2. `treatUrl()`: `if(!treat||!color) return PLACEHOLDER_URL;`
3. `sync()` auto-snap: `if(color && treat && getValidForColor(color).indexOf(treat)<0){treat=getDefault();}`
4. `renderTreat()` snap: `if(treat && valid.indexOf(treat)<0){treat=getDefault();}`
5. `styleAvail = treat ? (styleValid.indexOf(treat)>=0) : true`
6. `colorOk = treat ? (getValidForColor(c).indexOf(treat)>=0) : true`; `b.disabled = treat ? !colorOk : false`

### Reset / defaultColorForTreat
```javascript
function defaultColorForTreat(t){
  var valid=CFG.colorOrder.filter(function(c){return (TREAT_VALID[c]||[]).indexOf(t)>=0;});
  return valid.indexOf('White')>=0?'White':(valid[0]||'White');
}
function resetPDP(){style=CFG.defaultStyle||'Classic';treat=null;color=null;jesGarment('tee');}
window.resetPDP=resetPDP;
```
- `setTreat(v)`: **first** `if(getValid().indexOf(v)<0)return;` then `treat=v;` then if `!color` → `color=defaultColorForTreat(v);` then `sync()`.
- Reset button: `<button id="{ns}-reset" onclick="resetPDP()">↺ Reset</button>`, navy bg, hover red, exposed via `window.resetPDP`.
- **Hero pre-set:** add `var _ph=el('{ns}-hero');if(_ph)_ph.src=PLACEHOLDER_URL;` immediately before first `ensure()` call in boot sequence.

### Garment color swatches — invalid-ink disable (LOCKED)
```css
.{ns}-sw button{position:relative;}
.{ns}-sw button.dis{opacity:.4;cursor:not-allowed;}
.{ns}-sw button.dis::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;border-radius:50%;
  background:linear-gradient(135deg,transparent 44%,rgba(168,32,26,.85) 44%,rgba(168,32,26,.85) 56%,transparent 56%);
  pointer-events:none;}
```
- `b.disabled=treat?!colorOk:false;`
- `b.onclick=colorOk?function(){color=c;sync();}:null;`

### Style tiles — invalid-ink disable (LOCKED)
```css
.{ns}-stthumb{position:relative;}  /* position:relative required or slash won't overlay */
.{ns}-stthumb.dis{opacity:.3;cursor:not-allowed;pointer-events:none;}
.{ns}-stthumb.dis::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:linear-gradient(135deg,transparent 44%,rgba(168,32,26,.7) 44%,rgba(168,32,26,.7) 56%,transparent 56%);
  pointer-events:none;}
```

### Chip versioning (LOCKED)
- **Never overwrite an existing chip filename.** CDN caches content permanently. Use new suffix (`_r2`, `_r3`, etc.) on every content change.
- **CDN RESOLUTION GATE — mandatory, no exceptions:** After pushing every chip file, HEAD-check each one on `cdn.jsdelivr.net` before touching the section. A 200 on raw.githubusercontent is NOT sufficient. If any chip returns 403 or 404 on CDN, push under a new filename and re-check before proceeding.
- Per-style chipTreat (null or invalid → first valid for color):
  `var chipTreat=treat?((styleValid.indexOf(treat)>=0)?treat:(styleValid[0]||'navy')):'fc';`
- When treat=null: chipTreat defaults to `'fc'` → base64 from `CFG.sw[s]`.
- thumbSrc condition: `(!treat||treat==='fc') ? ('data:image/jpeg;base64,'+CFG.sw[s]) : CDN_chip_url`
- Light-ink chips (white/cream/grey): navy background chip (`_chip_v2_r2.jpg`). All others: white background (`_chip_r2.jpg`).
- **⚠ SPLIT INK TRAP (LOCKED):** `split` has NO CDN chip file. Always base64 from `CFG.sw[s]`. Never add `&& s===style`. Never CDN fallback for split.

### Deep-link reader
MANDATORY in BOOT `ensure()` callback only — reads `?variant=`, preselects style/color/ink, falls back to defaults.

**STOP — show PDP working (all selectors, chips change with ink, empty state, reset button, deep-link) for approval.**

---

## STEP 6 — Fulfillment (fulfill.py)

### Maps needed (clone DAD/GOD)
- `{DESIGN}_STYLES` — `norm(Style)` → `(file_code, aspect_w_h)`
- `{DESIGN}_INK` — display label (lowercased) → treatment key e.g. `'heather grey':'grey'`, `'full color':'split'`
- `{DESIGN}_VALID` — `ckey → [valid treatment keys]`
- `{DESIGN}_DEFAULT` — `ckey → fallback treatment`

**Resolution:** `tk=INK.get(label.lower())`; if None or `tk not in VALID[ckey]` → `tk=DEFAULT[ckey]`.

Edit fulfill.py by parse/replace + `py_compile` check; additive only (don't touch existing handlers).

**Dry-run every valid color × ink × style × garment against live repo; assert each URL = 200.**

**STOP — show dry-run 200-OK for all routings + fallbacks. Awaiting explicit push approval.**

---

## STEP 7 — Home grid + Shop All wiring

**Home grid (`front-grid.liquid`) — 8 tiles only.**
Combined product? Add to `FG_HYBRID` map + handle to `unless` skip-list.

**Shop All (`ad-all-prefixes.liquid`):**
- One card per distinct design.
- Card schema: `name`, `tee_url`, `hoodie_url`, `colors[]` with keys `label`/`hex`/`tee`/`hoodie` (jsDelivr URLs — **`hoodie_` filename prefix**), Standard prices.
- **Insert via JSON parse → append → re-serialize → `node --check`. NEVER regex into the array.**
- Bump `ad_prefix_count` to equal Shop All card count.

**STOP — show rendered Shop All card (embedded-image proof) before push.**

---

## STEP 8 — Master sheet

**CURRENTLY SKIPPED per standing instruction.** Do not update during a build unless user explicitly asks.

---

## STEP 9 — Final done-checklist

- [ ] Print files: trimmed-to-content, 1385 lockup width, transparent bg, single-color, `{code}` from master sheet
- [ ] Mockups: all URLs 200 on CDN. No regeneration of existing files.
- [ ] Chips: light inks on navy `_v2_r2`; per-style chipTreat fallback correct; all resolve 200 on CDN
- [ ] Both products live: options Color/Size/Style, correct variant count, Standard prices, hero set
- [ ] PDP: all selectors render; chips correct; empty state correct; reset button works; M pre-selected; deep-link works; `node --check` passed; <200KB
- [ ] Ink × garment × style audit: all valid combos have mockups; invalid combos slash/grey on PDP
- [ ] fulfill.py: every valid combo routes to existing print file; py_compile passed; valid-map matches PDP
- [ ] Home: 8 tiles; combined product in FG_HYBRID
- [ ] Shop All: card added; `node --check` passed; `ad_prefix_count` bumped
- [ ] Every push verified by reading back via API (not storefront)

---

## Quick reference — locked constants

- **Shop:** `rudjph-mx.myshopify.com` · GraphQL 2025-07 · Theme `153615171752` · Publication `198208127144`
- **Shopify token:** mint client_credentials → save `/tmp/_shoptoken`; header `X-Shopify-Access-Token`; ~24h; remint on `KeyError:'data'`
- **GitHub:** repo `alwaysdelivers/ad-printfiles` · PAT → `/tmp/_ghpat` · `User-Agent: AlwaysDelivers`
- **CDN:** `https://cdn.jsdelivr.net/gh/alwaysdelivers/ad-printfiles@main/` · RAW: `https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/` · Purge: `https://purge.jsdelivr.net/gh/alwaysdelivers/ad-printfiles@main/{path}`
- **Printful:** store `18259192` · token → `/tmp/_printfultoken` · Tee product `71` · Hoodie product `146` · throttle ~1 task/min
- **Variant IDs:** White tee=4011/hoodie=5522 · AthHeather tee=6948/hoodie=5610 · Navy tee=4111/hoodie=5594 · Black tee=4016/hoodie=5530
- **Categories:** TEE `aa-1-13-8` · HOODIE `aa-1-13-13`
- **Color hexes:** White `#ffffff` · AthHeather `#b9c0cb` · Navy `#1e3a5f` · Black `#1a1a1a`
- **Hoodie convention:** `hoodie_` everywhere — `hood_`, `HOODIE_` retired

---

## Reference builds (clone these)

- **Multi-style, treatment-keyed, full palette:** DAD (Classic/Varsity/Retro; 7 inks), GOD (Monument/Bold/Retro; 7 inks)
- **Multi-style, ground-keyed (3-ink):** MOM (Grace/Bold/Elegant/Retro), FAITH (Classic/Elegant/Strong)
- **Watermark + dark variants:** AMERICA (Classic/Heritage/Star/Retro/Watermark; 8 inks)
- **Combined multi-design:** Creatures, Science (FG_HYBRID hero lock)
- **Single-style:** Crown, Stork (Color × Size only)

---

## STANDARDIZE EXISTING PREFIXES — Backport protocol

Six live multi-ink prefixes. Do ONE prefix per session. Full stop after each stop gate. Do not start the next prefix until current is complete, deployed, and you have confirmed it working in browser.

### Priority order (easiest → hardest)
1. DAD ✓ complete
2. GOD ✓ complete
3. MOM ✓ complete
4. FAITH ✓ complete
5. CROWN ✓ complete
6. JESUS — most complex, read section fully before planning
7. CROSS — dual-family architecture; read audit report before planning

### GATE 0 — Mandatory read and report (BEFORE touching anything)

This gate must be completed and reported to Ati before writing any plan or any code. No exceptions.

1. **Fetch the live section from Shopify via API in this response.** Save to `/tmp/{prefix}-combined.liquid`.
2. **Print the full IIFE verbatim** — `sed -n '{start},{end}p'`. Do not summarize.
3. **Extract and report every exact string that will be replaced** — copy the literal bytes, not paraphrased descriptions. Run `assert` on each one before planning any replacement.
4. **Run `node --check`** on the extracted IIFE. Report pass/fail.
5. **List every function that exists but is NOT in the standard** — these are candidates for preservation. List them by exact name.
6. **List every unique architectural difference from DAD (standard):** different namespace, different URL pattern, different state variable names, different boot sequence, different family/product structure.
7. **Report all of the above to Ati.** Do not proceed until she says go.

Failure to complete Gate 0 means every plan produced is based on assumed content, not actual content. Gate 0 failures caused every audit error this session.

### STOP A — Valid map

- From the live section (Gate 0 output), extract the exact current ink×garment combinations.
- Build `TREAT_VALID` from actual combinations, not from memory.
- Add `TREATS`, `TREAT_VALID`, `TREAT_DEFAULT`, `TREAT_LABEL`, `getValid()`, `getValidForColor()`, `getDefault()`, `defaultColorForTreat()`.
- Run `node --check`. Report the map to Ati.

**STOP — show valid map. Await approval before writing any code.**

### STOP B — Null-state guards

Apply all 6 null-state guards (see Step 5). Also:
- Replace 3 URL functions → 1 `treatUrl()` with null guard. Remove all `?v=` suffixes.
- Replace `renderInk()` → `renderTreat()`.
- Replace `setInk()` → `setTreat()` with guard-first + auto-snap.
- Replace `renderColors()` — add `colorOk/.dis/onclick=null`.
- Update `setImg()` — null guard + opacity reset.
- Update `sync()` — remove hardcoded garment guards, add auto-snap.
- Update `syncSize()` — M pre-select + ATC guard + `TREAT_LABEL`.
- Add `resetPDP()` + `window.resetPDP`. Reset must call `jesGarment('tee')` (or equivalent), not just `sync()`.
- Update HTML ink button IDs from `{ns}i-{treat}` → `{ns}it-{treat}` + `data-treat` attribute.
- Add Reset button HTML.
- Add CSS: `position:relative` on stthumb, `.dis` slash on stthumb + sw button, treatrow styles, reset button.
- Add hero pre-set before `ensure()`.
- Run `node --check`.
- Run MANDATORY BOOT SEQUENCE WALKTHROUGH (see top of this MD).
- Run MANDATORY PRE-PUSH VERIFICATION OATH (see top of this MD).

**STOP — all 6 verification oath statements confirmed true. Await push approval.**

### STOP C — Chip versioning

- Identify current chip suffix in the section.
- Check which chip files exist in repo (`mockups/{design}/thumbs/`).
- Push new `_r2` chip files.
- **CDN RESOLUTION GATE:** HEAD-check every chip on `cdn.jsdelivr.net`. If any returns 403/404 — stop, push under new filename, re-check. Do NOT touch the section until all chips are 200 on CDN.
- Update chip URL builder in section.
- Push section.
- Run MANDATORY PRE-PUSH VERIFICATION OATH.

**STOP — CDN gate passed for all chips. Await section push approval.**

### Per-prefix notes (current state)

| Prefix | Namespace | Styles | Status | Notes |
|---|---|---|---|---|
| DAD | `dadp-` | Classic/Varsity/Retro | ✓ complete | Standard reference build |
| GOD | `godp-` | Monument/Bold/Retro | ✓ complete | Cream valid on Navy/Black |
| MOM | `madp-` | Grace/Elegant/Bold/Retro | ✓ complete | fc/mono/red; red valid all garments |
| FAITH | `jes-` / `jit-` | Classic/Elegant/Strong | ✓ complete | Full-frame print files (Class B); red valid all garments; chip suffix `_chip_w2_r2` |
| CROWN | `crown-` / `cit-` | None (no style axis) | ✓ complete | split/mono only; split invalid on Navy/Black; no STOP C |
| JESUS | `jesp-` | To be confirmed | pending | Most complex; read section fully before planning |
| CROSS | `crx-` | Dual-family (jesus-cross / the-cross) | pending | See Cross architecture notes below |

### Cross architecture notes (LOCKED — read before touching)

The cross section is a **dual-family** PDP serving two products simultaneously:
- **jesus-cross** (`family='jesus-cross'`): Single design (`cross-04`), no ink choices. Ink row hidden. `treat` irrelevant — `designValue()` returns `CFG.jesusCrossDesign` regardless.
- **the-cross** (`family='the-cross'`): Three treats — `std`, `split`, `red`. Red only valid on White and Black (`CFG.redColors=['White','Black']`). Ink row visible.

**`treat` is NOT initialized to null in this section.** It starts as `CFG.defaultTreat='std'` because `treat` drives `designValue()` → `dcode()` → product option3 matching → `curV()`. Setting `treat=null` without null-guarding `designValue()` and `dcode()` would break variant lookup on load.

**Decision recorded (pending Ati approval):**
- Option A: `treat=null` on init — add null guards to `designValue()`, `dcode()`, `imgUrl()` — user must pick treat before ATC works
- Option B: keep `treat=CFG.defaultTreat='std'` on init — ATC works immediately on load — `resetPDP()` resets to `treat='std'` not null

**Functions to preserve — do not alter:**
`designValue()`, `dcode()`, `gp()`, `imgUrl()`, `colorsForDesign()`, `sizesOf()`, `curV()`, `renderFamily()`, `setFamily()`, `isRed()`, `redOK()`, `priceLine()`, `zOpen()`, `zClose()`.

**Valid map for The Cross:**
| Garment | Valid treats |
|---|---|
| White | std, split, red |
| Athletic Heather | std, split |
| Navy | std, split |
| Black | std, split, red |

Jesus Cross: no treat axis — treat not relevant to valid map.

### Watermark dark-garment print files (LOCKED)
When an ink is valid for Watermark on Navy/Black garments, a separate `watermark_{ink}_dark.png` is needed.

**Approved dark variants (AMERICA):**
| Ink | AMERICA color | USA ghost | Opacity |
|---|---|---|---|
| red | #a8201a | white | 80% |
| gold | #c08a2e | cream #f5f1e8 | 75% |
| white | #ffffff | red #a8201a | 80% |
| karmablue | #2f8fe2 | white | 100% |
| grey | #b9c0cb | red #a8201a | 80% |

### Chip versioning history
| Prefix | Chip suffix | Notes |
|---|---|---|
| DAD | `_chip_r2.jpg` (standard) / `_chip_v2_r2.jpg` (light inks) | Current |
| GOD | `_chip_r2.jpg` / `_chip_v2_r2.jpg` | Current |
| MOM | `_mono_w2_r2.jpg` / `_red_w2_r2.jpg` | fc = base64 only |
| FAITH | `_chip_w2_r2.jpg` | All inks including red; fc = base64 |
| CROWN | No chip files | No style axis |
