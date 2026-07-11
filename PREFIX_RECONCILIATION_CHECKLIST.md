# Prefix Reconciliation — Learnings & Checklist
_Derived from the AMERICA reconciliation (2026-07-07). The HTML is the standard; everything flows from it._

---

## Core principle
**The per-prefix HTML layout file (in Drive) is the source of truth for which combinations are APPROVED.**
The live site and `catalog.json` are reconciled *to* the HTML — never to memory or to prior work.

Triangulate three sources for every prefix:
1. **Live Shopify product** — options (Color / Size / Style), variant count, handles (tee + hoodie).
2. **Drive HTML layout** — the approved style × colorway matrix (the standard).
3. **Repo print files** — what actually EXISTS on disk.

Resolution of conflicts:
- HTML wins on what is **approved / selectable**.
- Files win on what **exists**.
- Any gap between them is a **bug to fix**, not to hide.

---

## Per-prefix reconciliation checklist (do in order; ask before any live change)

- [ ] 1. Pull the prefix HTML from Drive (download, not just read — reader truncates large files).
- [ ] 2. Parse the HTML matrix: styles (rows) × colorways (columns); note any `—` / N/A cells.
- [ ] 3. Read the LIVE product JSON for **both** tee and hoodie: options, variant count, handles.
- [ ] 4. Enumerate the repo print files for the prefix; build the actual style × colorway matrix for **tee AND hoodie**.
- [ ] 5. Present **live vs HTML vs catalog** side by side (tee + hoodie) — AS A VISUAL HTML PROOF (numbered matrix of composites) — and get approval before writing.
- [ ] 6. Confirm the **fabric-color axis** (HTML usually omits it — carry it separately: White/Athletic Heather/Navy/Black, or baby colors).
- [ ] 7. Flag ink-naming issues (see "White = Cream" below) and get the decision.
- [ ] 8. Decide the **default ink** (Full Color where valid; otherwise decide for this prefix).
- [ ] 9. Write the catalog entry; **validate every combination resolves to a real file** (offline).
- [ ] 10. Deploy PDP validity/gating = exactly the HTML-approved set; **verify live** (not just offline).
- [ ] 11. Verify home + shop-all cards (catalog-driven `ad-grid` upgrader handles these once the catalog entry is right).
- [ ] 12. Confirm the prefix has a non-empty `groups` array in catalog.json; run `python3 tools/validate_groups.py catalog.json` (must pass, exit 0).
- [ ] 13. Mark `reconciled: true` in catalog; push; mirror to Drive.

---

## Data model (schema per prefix in catalog.json)
`status`, `reconciled`, `groups[]` (≥1 valid group key — MANDATORY), `product_type`, `handles{tee,hoodie}`, `folder`, `naming`, `html_source`,
`options{Color,Size,Style}`, `variants_per_product`, `ink_capture`, `designs[{code,label}]`,
`inks[{token,label,file_colorway?}]`, `colorway_rule`, `ink_validity*` (per fabric), `defaults`,
`files{tee,hoodie}`, `notes`, `ui_behavior`, `selectable_combinations`.

**Selectable set = exactly the HTML-approved set.** (AMERICA: 160 possible − 110 approved = 50 invisible/low-contrast combos excluded.)

---

## Naming / ink conventions (check every prefix)
- **"White" ink is almost always brand Cream `#f0f0d8`** (the on-dark light standard), NOT pure white.
  If so, rename `white`→`cream` in LOCKSTEP: print files, PDP token+label+dot, catalog validity,
  `fulfill.py`, and the HTML column.
- **Token ≠ filename ≠ label** can all differ (e.g. token `karmablue` → file `neonblue` → label "Neon Blue"). Capture all three.
- **Ink is a line-item property `Ink`**, not a 4th Shopify variant option (3-option cap is Color/Size/Style). Poller already reads it.
- **`fc` (Full Color) resolves by ground** → `fc_light` / `fc_dark`. Other inks are literal file tokens.
- **Cream/White/Heather-Grey ink dots need a border** to be visible on a light pill/page.

## Naming rules by lane (`naming` field → file colorway)
- `faith-lane` (jesus/faith/mom): `fc`→`{ground}`, `mono`→`{ground}_mono`, `red`→`redmono`, `black`→`blackmono`
- `two-color` (god/dad): `fc`→`fc_{ground}`, `neonblue`→`neonblue`, else literal
- `america`: `fc`→`fc_{ground}`, `karmablue`→`neonblue`, else literal
- `cross`: `fc`→`fc_{ground}`, else literal
- `crown`: `CROWN_{colorkey}{_split if split}` (color-name files, lowercase)
- `karma`: no ink axis; `KARMA_{code}` (fixed 2-color spiral)
- `science`: `SCIENCE_{design}_{token}` (ink via line-item property; default black on light / cream on dark)
- `creatures`: CAVEMAN/SASQUATCH/SNOWMAN → `{whitegarments|darkgarments}` by ground; YETI_ICE → `ICE_allgarments`
- `stork-color-only`: `STORK_{code}_{ground}` (no style/ink axis; baby colors tee-only)
- ground = dark if garment ∈ {Navy, Black} else light
- **All print-file URLs are under `printfiles/<folder>/…`** (don't drop the `printfiles/` prefix).

---

## UI standards (locked)
- **Default ink = Full Color** where valid; else decide per prefix.
- **Load/Reset = a PREVIEW, not a choice (locked 2026-07-09).** Nothing is chosen; ALL styles/fabrics/inks are enabled; the hero shows the default preview (e.g. Classic / White / Full Color). A default is a preview, not a choice.
- **Clicking commits that axis only.** Unchosen axes resolve via a single `effTriple()` resolver (best valid style/color/ink honoring chosen axes, preview-match scoring). ALL renders — hero, blank, rings, labels, sizes, cart `Ink` property — read from `effTriple()`. Chosen axes are NEVER silently overwritten; there is NO auto-switch. If a click makes the current mix invalid, the unchosen (preview) axes move.
- **Enablement rule:** an option is enabled iff SOME assignment of the unchosen axes makes it valid.
- **Verification is mandatory before deploy:** runtime harness (execute `effTriple`/`inkEnabled` in node with stubbed globals — `node --check` is NOT enough) + exhaustive BFS from reset over every enabled click: 0 invalid renders, ALL approved triples reachable.
- **Ink pills carry a color dot** (Option A): dot left of label; light inks get a border; Full Color = navy/red split dot; selected dot gets a white ring.
- **Unavailable combinations = greyed + red diagonal slash** on all three axes (style, ink, fabric), driven by the correct HTML-approved validity. The slash is only right if the data behind it is right.
- **Swatch order = light → dark by luminance** (White first … Black last). Grid default = lightest color.
- Style + Fabric tiles stay selectable where reachable; enablement on all three axes follows the rule above (no silent ink auto-switch — superseded 2026-07-09).

---

## Architecture
- **Single source of truth = `catalog.json`** (repo root; mirrored to Drive). Downstream is generated, not hand-edited.
- **Grids read the catalog live** via the shared `snippets/ad-grid.liquid` upgrader (fetch catalog → composite blank + resolved design → light→dark swatches). Baked `heroes/grid/` JPEGs kept as fallback.
- **PDP composites live** from the print files; grids now composite the same way → a catalog change dominoes to PDP + home + shop-all.
- Home grid caps at 8 (frontpage collection) + Shop All; shop-all shows all.
- **Deep-link reader (`?variant=<id>`) is mandatory on every prefix PDP** — a PDP without it is a defect.

---

## Failure modes to guard against (hard-won)
- **Don't over-interpret a single screenshot.** (Neon blue was made watermark-only from one image — the opposite of truth.) Confirm intent against the HTML before acting.
- **Don't add anything not in the HTML.** (Invented pattern pills; exposed 50 unapproved combos.) Only what the HTML approves.
- **Offline-pass ≠ live-pass.** Path bugs (dropped `printfiles/`) and CSS/behavior (dropped luminance sort) pass a Python mirror but fail live. Always verify on the live page.
- **CHECK THE TEMPLATE before editing a section.** Read `templates/product.X.json` → `order` → section `type`. (karma-combined-pdp was edited a full day while karma-combined was live.)
- **`node --check` is syntax only.** A ReferenceError killed the Crown PDP undetected. Run the runtime harness + BFS.
- **Ask before every change.** Diagnose + propose first; touch nothing (files, theme, catalog, Drive) until confirmed.
- **jsDelivr caches** — renames need cache-bust/purge (`_r2`, `_r3` suffixes for changed content); `raw.githubusercontent` serves current. Shopify asset readback + page cache can be stale — wait and re-fetch.
- **Deliver visual proofs as an openable HTML file** (full-res composites, numbered when a decision is needed) — never a text table for a visual decision.
