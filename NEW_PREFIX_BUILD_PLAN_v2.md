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

> **RULE 0h — TRACE EVERY BRANCH.** For any section with multiple families, modes, or conditionally hidden rows (e.g. Cross jesus-cross/the-cross, any section that hides a UI row based on state), the boot sequence walkthrough MUST be traced separately for every branch. The happy path is not enough. If a row is hidden in branch A, everything inside it is also hidden — including the Reset button.

---

## MANDATORY PRE-PUSH VERIFICATION OATH

Before any section deploy or file push, confirm all six statements are true. If any is false, do not push — fix it first.

1. **I fetched the live section from Shopify via API in this response** — not from memory or /tmp cache.
2. **Every string I replaced was found via `assert` in the script** — not assumed to be present.
3. **`node --check` passed** on the extracted IIFE with the current line range.
4. **CDN HEAD-check passed (200) on every file the section references** — PLACEHOLDER_URL, all chip files, sample treatUrls. A 200 on raw.githubusercontent is NOT sufficient.
5. **Boot sequence walkthrough completed** — traced t=0 through reset, confirmed no blank states or broken URLs.
6. **I have not taken any action beyond what was explicitly approved in the immediately preceding message.**
7. **colorOrder is `["White", "Athletic Heather", "Navy", "Black"]`** — verified in deployed file.
8. **TREAT_LABEL display values match store standard** — verified: no internal key names shown to user.
9. **Reset button is outside any conditionally hidden wrapper** — verified: it remains visible in every branch/state.

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

**For sections with conditionally hidden rows (e.g. Cross, combined products):** Trace EVERY branch separately:
- Trace with family='jesus-cross' (or equivalent first branch): what shows, what hides, is Reset button still visible?
- Trace with family='the-cross' (or equivalent second branch): repeat full walkthrough.
- Trace the Reset path for each branch: does every element return to correct default state?

**Four additional checks before every push:**
1. **colorOrder** in CFG = `["White", "Athletic Heather", "Navy", "Black"]` (light→dark). Any other order is a bug.
2. **TREAT_LABEL values** match store standard: `navy:'Navy'`, `split:'Full Color'`, `red:'Red'`, `grey:'Heather Grey'`, `karmablue:'Neon Blue'`, `cream:'Cream'`, `black:'Black'`, `gold:'Gold'`, `ice:'Ice Blue'`. Never use internal key names as display labels (e.g. never show "std", "fc", "mono" to the user).
3. **Reset button is outside any conditionally hidden wrapper.** If the Reset button is inside a div that gets `display:none` for any state, it will disappear in that state. Reset must always be visible.
4. **Cross-check against DAD (known-good):** Open DAD section, compare boot sequence line by line. Any divergence is a bug candidate.

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

**0e. Colors offered** — default White, Athletic Heather, Navy, Black unless user specifies otherwise. **colorOrder MUST be this exact sequence: `["White", "Athletic Heather", "Navy", "Black"]` (luminance light→dark).** Any deviation is a defect.

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

**0h. Group membership (MANDATORY — no prefix ships without it).**
- Every prefix MUST belong to at least one group in the `catalog.json` `groups` registry. This is the browse/discovery axis (Family, Faith, States, Cities, Science, Spiritual, Music, Pets, Holidays, Humor, etc.).
- A prefix may belong to MANY groups (many-to-many). Set `catalog.json → prefixes → <NAME> → groups: [...]` with one or more existing group keys.
- If the prefix needs a NEW group that does not yet exist, add it to the `groups` registry first (`{label, order, status:"hidden"}`), then reference it. New groups start `hidden` until enough members exist to surface.
- Group assignment is Ati's call — propose the mapping, do not decide it.
- **Enforcement:** run `python3 tools/validate_groups.py catalog.json` — it MUST pass (exit 0) before the prefix is considered done. It fails on any prefix lacking a valid, non-empty `groups` array. Empty groups (placeholders) are allowed.

**STOP — approve full definition (0a–0h) before any asset work.**

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

### Mockup size consistency check
Before submitting for approval, compare new mockup print dimensions against existing mockups of the same prefix:
- Download 2 existing mockups (one matching garment+color) and measure the print bounding box in pixels using PIL
- Measure the same on new mockups
- Print widths must match within 10px. Print heights must match within 20px (ghost crop variance is acceptable)
- Center X and Y must match within 15px
- If new mockups are significantly smaller → wrong placement class (check Class A vs Class B). Regenerate before showing.

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

### ZOOM — Sloth pattern (LOCKED, 2026-07-12)
Every PDP uses the Sloth zoom — no exceptions, all 13 live PDPs converted 2026-07-12:
- Whole stage clickable: `#<pfx>-stage` gets `cursor:zoom-in` and `el('<pfx>-stage').addEventListener('click',zOpen)` (never bind the hero img alone).
- `zOpen` CLONES the live composite stage (blank+art) into `<div id="<pfx>-zoombox">` inside `#<pfx>-zoom`, sized `min(940px,94vw,94vh)`, square aspect, id stripped from the clone.
- Lightbox background is WHITE `#ffffff` (never black/dark rgba).
- Close: click ANYWHERE (overlay binding is plain `zClose`, no `e.target===this` guard), the × button, or Escape.
- `#<pfx>-zoombox{border-radius:8px;box-shadow:0 10px 40px rgba(0,0,0,.25);overflow:hidden}`.
- NEVER fetch a separate zoom image: `printfiles/zoom/` was DELETED 2026-07-12; no `drag-zoom-wrapper`, no hi-res swap, no `.<pfx>-zoom img` sizing rule.

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

### Store-standard display labels (LOCKED — never deviate)
`TREAT_LABEL` values must use these exact display strings. Internal keys are never shown to users.

| Treatment key | Display label |
|---|---|
| `navy` | Navy |
| `split` | Full Color |
| `red` | Red |
| `black` | Black |
| `grey` | Heather Grey |
| `karmablue` | Neon Blue |
| `cream` | Cream |
| `gold` | Gold |
| `ice` | Ice Blue |
| `white` | White |

For combined/multi-design products with treatment keys like `std`/`split`/`red`: map to the equivalent standard label (`std`→`Navy`, `split`→`Full Color`, `red`→`Red`).

### colorOrder standard (LOCKED)
`CFG.colorOrder` MUST be `["White", "Athletic Heather", "Navy", "Black"]` in every section. This drives swatch render order (left→right = light→dark). Any deviation is a defect — fix it, do not treat it as "how the section works."

### Reset button placement (LOCKED)
The Reset button MUST be in its own `<div>` that is never conditionally hidden. It must NEVER be placed inside a wrapper div that gets `display:none` for any state (e.g. inside an ink row wrapper that hides when a family has no ink axis). If a section hides any row conditionally, verify the Reset button is outside that row.

### ATC payload — Ink property
- Standard prefixes: send `properties:{Ink: TREAT_LABEL[treat]}` — display label, not file key.
- Combined/multi-design products (Cross, Creatures, Science): send `{id, quantity}` only — design is in option3, no Ink property needed.

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
- [ ] Shop All: card added; `node --check` passed; `ad_prefix_count` bumped; card carries `groups` array matching the prefix's catalog entry
- [ ] Group membership: prefix has non-empty `groups` in catalog.json; `python3 tools/validate_groups.py catalog.json` passes (exit 0)
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
6. CROSS — ⚠ section/products rebuilt and deployed, BUT mockup sizing bug unresolved (see "CROSS — KNOWN UNRESOLVED ISSUE" below). Do this FIRST in next session — do not start JESUS until Cross sizing is fixed and visually confirmed.
7. JESUS — most complex, not started, read section fully before planning

### GATE 0 — Mandatory read and report (BEFORE touching anything)

This gate must be completed and reported to Ati before writing any plan or any code. No exceptions.

1. **Fetch the live section from Shopify via API in this response.** Save to `/tmp/{prefix}-combined.liquid`.
2. **Print the full IIFE verbatim** — `sed -n '{start},{end}p'`. Do not summarize.
3. **Extract and report every exact string that will be replaced** — copy the literal bytes, not paraphrased descriptions. Run `assert` on each one before planning any replacement.
4. **Run `node --check`** on the extracted IIFE. Report pass/fail.
5. **List every function that exists but is NOT in the standard** — these are candidates for preservation. List them by exact name.
6. **List every unique architectural difference from DAD (standard):** different namespace, different URL pattern, different state variable names, different boot sequence, different family/product structure.
7. **Check colorOrder** in CFG block. Report exact value. If not `["White", "Athletic Heather", "Navy", "Black"]` — flag as defect to fix.
8. **Check TREAT_LABEL / existing ink labels** against store standard. Report any labels that don't match (e.g. "Standard" should be "Navy", "Full Red" should be "Red").
9. **Check Reset button placement** — is it inside any conditionally hidden wrapper? If yes, flag it.
10. **Report all of the above to Ati.** Do not proceed until she says go.

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
| CROSS | `crxp-` (rebuilt clean from DAD clone) | Jesus Cross / The Cross | ⚠ INCOMPLETE — mockup sizing bug unresolved | See "CROSS — KNOWN UNRESOLVED ISSUE" below before touching |

### CROSS — KNOWN UNRESOLVED ISSUE (read before touching — session ended without fix)

**Symptom:** On the PDP, Jesus Cross Mono and Red render visibly smaller than Jesus Cross Full Color, despite all three mockup files reporting identical pixel dimensions (2000×2000) and near-identical print-to-canvas ratios when measured programmatically (~82.8–82.9% of image height in bounding-box analysis).

**What was tried and did NOT fix it:**
1. Regenerating the 16 affected Jesus Cross mono/red mockups via fresh Printful tasks — still produced 1000×1000 output (Printful's mockup generator intermittently returns half-resolution images for reasons not yet identified; same task body, same params as the working 2000×2000 calls).
2. Upscaling the 1000×1000 outputs to 2000×2000 with PIL LANCZOS and re-pushing under the same filenames — CDN confirmed 2000×2000 after purge, bounding-box measurement confirmed ~83% height match — but the user re-reported the same visual size mismatch after this fix was deployed.

**What this means:** Pixel-dimension parity and bounding-box percentage parity are NOT sufficient to confirm visual parity. There is some other variable causing the visible size difference that was never identified — candidates not yet ruled out:
- Ghost-mockup garment scale/zoom may differ between Printful's two render paths (the 1000×1000 path may use a different camera distance/crop on the garment itself, independent of the print art's pixel size within the canvas)
- The upscale-from-1000 approach interpolates a lower-detail source — this preserves the same *proportion* but does NOT correct for a different underlying garment photograph/crop if that's the actual source of the mismatch
- Possible: the original 1000×1000 mockups were never actually placing the print at the same physical position/size on the garment — only LOOKED similar by % when measured against image height, because the garment itself occupies a different fraction of the 1000×1000 vs 2000×2000 canvas

**Required next step (do GATE 0 style investigation before any fix attempt):**
1. Do NOT rely on PIL bounding-box percentage as a proxy for "looks the same size." Pull up the actual rendered images side by side at the same physical display size and eyeball-measure the garment width-to-print-width ratio directly — measure print width as % of GARMENT chest width, not % of canvas height.
2. Compare the `position` object sent to Printful for a working fc/split task vs a mono/red task — confirm `area_width`/`area_height`/`width`/`height`/`top`/`left` are byte-identical for the same garment+color combo.
3. If params are identical and Printful still returns visually different garment scale, the difference may be in which Printful "mockup style"/template variant got selected — investigate via `mockup-generator/templates/{product_id}` to see if 1000×1000 vs 2000×2000 outputs map to different `template_id`s with different `print_area_width`/`print_area_height`/`print_area_top`/`print_area_left` baked into the template itself (this would explain why upscaling the image after the fact cannot fix it — the garment-to-print ratio was wrong at generation time, not just the output resolution).
4. Likely real fix: explicitly pass `template_id` in the create-task request body, hardcoded to the same `template_id` used for the working fc/split mockups, for every batch — not just `variant_ids`+`files`. Confirm via fresh template lookup (`mockup-generator/templates/71?variant_id={id}`) which template_id the working images correspond to, since the earlier attempt to pass `template_id` failed with "No variants to generate" (likely wrong template_id was guessed, not that the parameter itself is unusable).
5. Re-verify using actual side-by-side visual comparison (zoomed crop of just the print on identical-size garment renders), not pixel-dimension or bounding-box-percentage checks alone.

### RULE 0i — PIXEL DIMENSIONS AND BOUNDING-BOX PERCENTAGE ARE NOT PROOF OF VISUAL PARITY (LOCKED)

When comparing mockups for visual consistency (same print size across different inks/treatments of the same design):
- Confirming identical pixel dimensions (e.g. both 2000×2000) is NECESSARY but NOT SUFFICIENT.
- Confirming identical bounding-box-as-%-of-canvas is NECESSARY but NOT SUFFICIENT — this can match while the underlying garment photo itself is scaled/cropped differently.
- The only sufficient verification is: crop both images to just the garment, scale both garment crops to the same width, and confirm the print element occupies the same fraction of garment width/height in both. Or: show both images at literal identical display size side by side and visually confirm.
- If a user reports "this looks smaller" after you have confirmed pixel/percentage parity, do NOT re-assert that the fix worked — investigate the garment-scale variable specifically, per the Cross unresolved issue above.

### Cross architecture notes (LOCKED — read before touching)

**Cross was rebuilt from scratch this session as a clean clone of DAD's standard architecture.** The earlier "dual-family combined product" approach (separate `family` state variable, `jesus-cross`/`the-cross` design-value branching, single shared product with option3=Design) was found to be the wrong structure and was abandoned. Do NOT reintroduce family-based branching.

**Current correct structure (as of last session):**
- Two Shopify products: `cross-always-delivers-tee` (48 variants) and `cross-always-delivers-hoodie` (48 variants)
- option1=Color, option2=Size, **option3=Style** with values `"Jesus Cross"` / `"The Cross"` — same pattern as DAD/GOD/MOM/FAITH, NOT a Design-keyed combined product
- Ink = line-item property, NOT baked into option3 — same as every other standard prefix
- Namespace: `crxp-` / `crxpt-` / `crxpg-` (cloned from DAD's `dadp-`/`dadpt-`/`dadpg-`)
- `TREATS=["fc","mono","grey","red"]` — 4 inks, same set for BOTH styles
- `TREAT_VALID` — garment-specific: White/AthHeather=[fc,mono,red]; Navy=[grey,red]; Black=[fc,mono,grey,red]
- `SC` map: `{"Jesus Cross":"jesuscross","The Cross":"thecross"}` — used to build mockup/chip filenames
- Mockup naming: `{garment}_{jesuscross|thecross}_{Color}_{fc|mono|grey|red}.jpg` — standard convention
- Print files: `cross-04_fc_{light|dark}_r2.png` / `cross-04_mono_r2.png` / `cross-04_grey_r2.png` / `cross-04_red_r2.png` for Jesus Cross; `cross-08_fc_{light|dark}.png` / `cross-08_mono.png` / `cross-08_grey.png` / `cross-08_red.png` for The Cross
- Functions follow standard DAD pattern: `treatUrl()`, `renderStyle()`, `renderTreat()`, `setTreat()`, `resetPDP()`, `jesGarment()` (boot/toggle function — name inherited from clone source, not renamed)

**STOP C is a no-op for Cross** — chips are base64 `CFG.sw` for fc, CDN files for mono/red, built from print files with the standard 440×338 white-canvas direct-RGBA-paste method (same as every other prefix). No dual-family chip complexity.

**Valid map — SAME for both styles:**
| Garment | Valid inks |
|---|---|
| White | fc, mono, red |
| Athletic Heather | fc, mono, red |
| Navy | fc, mono, red |
| Black | fc, mono, red |

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
