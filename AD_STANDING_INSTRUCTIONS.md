# ALWAYS DELIVERS — STANDING INSTRUCTIONS
_Effective 2026-07-10 (v3.1 — black×Navy struck; ice×Navy corrected; true-placement mockups live). This is the complete, forward-only rule set._

---

## 1. OPERATING RULES (every task, every prefix)

1. **The prefix HTML in Google Drive is the basis.** Before ANY work on a prefix,
   download its Drive HTML (Prefixes/<PREFIX>/) and read the placement-math panel and
   the approved matrix. No number, treatment, or approved combination exists outside it.
2. **No unilateral action.** Diagnose → present findings with measured numbers and a
   visual HTML proof → numbered options → Ati picks → explicit "go" → execute exactly
   that, nothing more. Answering a question is never a "go".
3. **One task at a time.** No pre-staging the next step.
4. **Templates are law.** Any regenerated artifact is built FROM the existing artifact's
   own markup/CSS. Never redesign, never invent styling, states, or elements the source
   doesn't have.
5. **Numbers only from source.** Every figure shown is measured from the actual file or
   lifted verbatim from the rendered document — never retyped by hand.
6. **Verify before claiming.** Byte-hash or live-readback proof for every change;
   visual HTML proof for every visual claim.
7. **jsDelivr:** never reuse a filename for changed content (bump `_r2`, `_r3`, …).
   Use raw.githubusercontent to verify fulfillment-path content.
8. **Reconciliation queue:** FAITH → MOM → KARMA → SCIENCE → final test order,
   each per PREFIX_RECONCILIATION_CHECKLIST.md, each anchored to its Drive HTML.

---

## 2. STANDARD PILL TREATMENT — DECIDED

**The model is `america-combined`, verbatim.** Every ink selector on every prefix PDP
uses America's implementation exactly. Each prefix keeps its own ink SET; only the
treatment converges.

### Markup (per pill)
```html
<button id="<pfx>t-<token>" data-treat="<token>" type="button">
  <span class="tdot" style="background:<HEX>"></span><LABEL>
</button>
```

### CSS (exact)
```css
button base: background:#fff   /* pinned explicitly — never rely on theme defaults */
.<pfx>-treatrow button{border:1px solid #1e3a5f;border-radius:999px;padding:6px 12px;
  font-size:12px;display:inline-flex;align-items:center;gap:7px}
.tdot{width:13px;height:13px;border-radius:50%;flex:none;display:inline-block}
button.on{background:#1e3a5f;color:#fff}
button.on .tdot{box-shadow:0 0 0 2px #fff}          /* white ring — required */
button.dis{opacity:.4;cursor:not-allowed;border-color:#c2c8d0;color:#c2c8d0;
  position:relative;overflow:hidden}
.dis::after{content:"";position:absolute;top:0;left:0;right:0;bottom:0;
  background:linear-gradient(135deg,transparent 45%,rgba(168,32,26,.7) 45%,
  rgba(168,32,26,.7) 55%,transparent 55%);pointer-events:none}
```

### DECIDED
- **<RADIUS>: `999px`** — capsule/full stadium shape. DECIDED 2026-07-10. Note: this is
  a deliberate departure from america-combined's literal declared value (`8px`, verified
  live against theme 153615171752 — one declaration, no override found in base.css or
  theme settings vars). "Verbatim" for rollout purposes means every OTHER aspect of the
  template (markup, anatomy, other hexes/spacing) — radius is the one explicit exception.
- **Mono dot: per-prefix, matched to actual print output.** DECIDED 2026-07-10.
  Pixel-sampled from live print files (raw.githubusercontent) rather than assumed:
  - FAITH: split dot `linear-gradient(135deg,#1e3a5f 0 50%,#f5f1e9 50% 100%)` — its
    Mono ink is genuinely ground-adaptive (navy on light, cream on dark; sampled
    dark-ground value `#f5f1e9`).
  - MOM: split dot `linear-gradient(135deg,#1e3a5f 0 50%,#f0f0d8 50% 100%)` — also
    ground-adaptive, but its sampled dark-ground cream (`#f0f0d8`) is a DIFFERENT value
    than FAITH's (`#f5f1e9`). Pre-existing mismatch between the two prefixes' actual
    print files — NOT resolved by this decision, left open as a separate housekeeping
    item outside the pill rollout (flag for Ati if/when worth fixing at the source).
  - CROSS: solid dot `#1e3a5f` — its Mono is a single fixed file, not ground-adaptive,
    used unchanged on every valid ground including Black. Solid navy is accurate as-is.
- **CREATURES unified ink row: DECIDED + DEPLOYED 2026-07-10.** One Ink row on
  creatures-combined-pdp with ALL FIVE pills always visible — Full Color, Grey, Black,
  Ice-Blue, Greyscale (Yeti's two drawings are presented as inks in the same row; the
  separate sub-row is retired). Chosen-axes filtering, the store pattern:
  - Reset → every creature / pill / garment available; defaults shown (Caveman, White,
    Full Color) but nothing committed.
  - Committing a creature slashes the inks that don't apply (text creatures slash
    Ice-Blue/Greyscale; Yeti slashes Full Color/Grey/Black).
  - Committing an ink slashes incompatible creatures and garments.
  - Committing a garment slashes incompatible inks.
  - Uncommitted axes auto-correct so the displayed combination is always purchasable;
    committed axes never change under the user; ↺ Reset clears all commitments.
  Creature presentation order: A→Z (Abominable Snowman · Caveman · Sasquatch · Yeti);
  default stays Caveman.
  Ink validity (approved matrix; black-on-black struck at review, black-on-Navy struck
  2026-07-10 after live mockups proved it illegible):
  - White: Full Color, Black       - Athletic Heather: Full Color, Black
  - Navy: Grey only                - Black: Grey only
  - Greyscale: all four grounds; Ice-Blue: White, Ath. Heather, Black (NO Navy — the
    Yeti Ice-Blue × Navy variant does not exist; catalog source of truth).
  Both select the Yeti drawing.
  Ink is a line-item cart property (key `Ink`, values Full Color / Grey / Black /
  Ice-Blue / Greyscale). fulfill.py routes it via `_resolve_ink` with CRE_INK /
  CRE_VALID / CRE_DEFAULT / CRE_SUF (fc→whitegarments, grey→darkgarments,
  black→blackink); property absent = legacy ground routing; Yeti routing unchanged.
- **Black creature art: BUILT + SHIPPED 2026-07-10.** Method (supersedes the earlier
  "regenerate from v32" note, rejected on review): ink-only variants of an existing
  live design are the LIVE DESIGN ALPHA RE-INKED to the new hex — letterforms and
  placement bit-identical to the shipped art, never re-rendered. Black = core-set
  `#1a1a1a`. Files (repo): printfiles/creatures/{CAVEMAN|SASQUATCH|SNOWMAN}_blackink_
  {tee|hoodie}.png + matching web (450×600 / 600×600) and zoom (1600×2133 / 1600×1600)
  mirrors. Recorded in CREATURES_full_set_preview_2026-07-10_r2.html (Drive source of
  truth, Black ink column added).
- **Mockup placement standard: TRUE FULFILLMENT PLACEMENT.** All product-gallery
  mockups are generated with the production print file filling the exact Printful
  print area (tee 12×16″, hoodie 14×14″) — the mockup shows exactly what ships.
  The pre-2026-07-10 creature mockups overstated the art ~9.6% and sat ~1.3″ low;
  all 50 were regenerated and swapped 2026-07-10. Apply this standard to every
  future mockup run.

### PILL HEX TABLE — exact values

**Core set:**

| pill | dot hex |
|---|---|
| Full Color | split — `linear-gradient(135deg,#1e3a5f 0 50%,#c0301c 50% 100%)` |
| Navy | `#1e3a5f` |
| Red | `#c0301c` |
| Black | `#1a1a1a` |
| Gold | `#c08a2e` |
| Cream | `#f0f0d8` · `border:1px solid #cfcaae` |
| Heather Grey | `#b9c0cb` · `border:1px solid #a7aeb8` |
| Neon Blue | `#2f7ff0` |

**Prefix-specific inks (own hex, same anatomy):**

| pill | dot hex |
|---|---|
| Mono (FAITH) | split — `linear-gradient(135deg,#1e3a5f 0 50%,#f5f1e9 50% 100%)` |
| Mono (MOM) | split — `linear-gradient(135deg,#1e3a5f 0 50%,#f0f0d8 50% 100%)` |
| Mono (CROSS) | solid — `#1e3a5f` |
| White (DAD) | `#fafaf8` · `border:1px solid #cfcfcf` |
| Slate (CROWN) | `#a8c0c0` · `border:1px solid #8fa3a3` |
| Ice-Blue (CREATURES) | `#7fc4e0` |
| Greyscale (CREATURES) | `#9aa3ad` |
| Full Color (CREATURES non-Yeti) | split — `linear-gradient(135deg,#1e3a5f 0 50%,#a8201a 50% 100%)` |
| Grey (CREATURES non-Yeti) | `#9aa3ad` (same hex as Greyscale) |

---

## 3. PILL ROLLOUT — 10 SECTIONS

Execution: one section at a time — exact diff presented → Ati approves → deploy →
verify live → next. Sequence: Ati picks (table order, or folded into each prefix's
reconciliation pass).

| # | section | changes to reach the model |
|---|---|---|
| 1 | ad-stork-pdp | red dot → `#c0301c` (already anatomically identical) |
| 2 | dad-combined | navy → `#1e3a5f`, red → `#c0301c`, split dot → model, neonblue → `#2f7ff0`, add ring, disabled → `.4` + standard slash |
| 3 | jesus-combined | navy → `#1e3a5f`, red → `#c0301c`, split → model, add ring, cream border → standard border, disabled → `.4` + standard slash |
| 4 | crown-combined | hexes → model, add ring, slash → standard (remove `.85` alpha, `border-radius:50%`, line-through), disabled → `.4` |
| 5 | god-combined | add `tdot` to all 7 pills (model hexes; split FC), ring, disabled → `.4` |
| 6 | faith-combined | add dots to 3 pills (FC split, Mono, Red), ring, disabled → `.4` |
| 7 | mom-combined | same as faith (3 pills) |
| 8 | cross-combined | add dots to 4 pills (FC split, Mono, Heather Grey, Red), ring, disabled → `.4` |
| 9 | science-combined-pdp | rebuild JS pill renderer to standard markup (Black / Cream / Red dots), ring, full disabled + slash treatment |
| 10 | creatures-combined-pdp | ✅ DONE 2026-07-10 — unified five-pill ink row deployed to the standard (999px, ring, standard slash); sub-row retired |

Every section change also pins `background:#fff` and `border-radius:999px` explicitly.
