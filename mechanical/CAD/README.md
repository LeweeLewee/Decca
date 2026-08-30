# CAD

Source (editable, parametric) mechanical design files.

**Intended contents**
- Fusion 360 archives (`.f3d`) and/or OpenSCAD (`.scad`) source.
- Neutral exchange formats (STEP `.step`) for interop.

**Conventions**
- Keep source here; export print-ready meshes to `../STL/`.
- Parametric source is preferred so parts can be re-derived if dimensions change.
- Record revisions in `docs/Revision History.md`.

## Display bezel — current revision: **Q — OPEN, bezel test print required**

**Rev Q is bezel-only. The released Rev P.5 carrier is FROZEN and unchanged.**

Rev Q replaces the two Rev N side locating rails with **one continuous masking
lip** around the complete inside perimeter of the Perspex opening — left, right,
top, bottom and all four corners. The lip conceals the visible cut edge of the
Perspex and locates the bezel. It works on clearance, not interference: it is
not a snap, not a clamp and not a press fit, and it carries no load. Retention
remains removable adhesive on the unchanged recessed pads.

Everything else about the Rev N bezel is carried over untouched — the
40.00 × 20.30 × 4.00 envelope, the R2.00 external corners, the R0.40 front edge
break, the 30.40 mm visible window width, the R0.80 window corners, the seating
face and both adhesive pads.

| File | Role |
|---|---|
| `Decca_Display_Bezel_revQ_fusion.py` | **the generator — single source of truth for every Rev Q dimension** |
| `Decca_Display_Bezel_revQ_verify.py` | independent offline verification of the exported STL (numpy only) |
| `Decca_Display_Bezel_revQ_frozen_check.py` | proves the six frozen Rev P.5 files still match the Rev Q brief — run before and after any Rev Q work. Hashes text files as-is, forced LF and forced CRLF, so a Windows/Linux line-ending difference cannot masquerade as tampering |
| `Decca_Display_Bezel_revQ.f3d` | **editable source** — named parameters, derived values written as real formulas |
| `Front_Bezel_revQ.step` | the bezel alone |
| `Decca_Display_Bezel_revQ_assembly.step` | bezel + measured Perspex + OLED glass proxy + the **unchanged Rev P.5 carrier**. Does **not** overwrite `Decca_Display_Mount_revP_assembly.step` |
| `Bezel_Corner_Gauge_revQ.step` | five-tab corner-radius gauge — **print this before the bezel** |

Key dimensions, each verified by two independent tools:

| | mm |
|---|---:|
| Lip outer envelope | **34.900 × 15.000** |
| Lip inner envelope (derived) | 34.100 × 14.200 |
| Lip wall | **0.400** — one controlled extrusion width |
| Lip depth | **2.800** into the 3.00 mm Perspex |
| Lip outer corner radius | R0.600 — **UNRESOLVED**, see below |
| Entry lead-in | 0.200 × 45°, outer rear edge only |
| Clearance into the measured opening | **0.150 per side, all four sides** |
| Rearmost material | z = **+0.200** — 0.200 clear of the Perspex rear face |
| Clearance to the OLED glass | **0.500** — the released Rev N/P value |
| Minimum distance to the Rev P.5 carrier | 1.171 |
| Effective clear optical opening | **30.400 × 14.200**, R0.800 |
| Volume | 0.5243 cm³ ≈ 0.67 g in PETG |

**30/30 gates PASS** in Fusion; **35/35 PASS** offline from the mesh. One shell,
one lump, zero slivers; the lip is continuous at 1440/1440 perimeter stations at
three depths; wall 0.4000 min and max; zero interference with the Perspex, the
glass or the carrier; nothing behind the Perspex rear face.

> **The opening corner radius has never been measured.** It could not be
> recovered from Rev N — those rails ran only y −4.00…+4.00 and never approached
> a corner, which is precisely why that architecture was chosen. So
> `bezel_lip_corner_r` is a named **UNRESOLVED** parameter, set to the proven
> Rev N rail-end relief R0.60. That seats for any opening corner radius up to
> **1.112 mm** (the rule is `R_panel_max ≈ R_lip + 0.51`). If the real corners
> are rounder, the bezel stands proud of the fascia — obvious, harmless, and
> fixed by raising one parameter and reprinting. **Print
> `Bezel_Corner_Gauge_revQ` first** and measure it. Build report §8.

> **The lip costs 0.350 mm of lit screen height.** The clear opening goes from
> 30.40 × 14.90 (Rev N) to 30.40 × 14.20, now controlled by the top and bottom
> lip rather than by the bezel face, and the visible active band drops 8.100 →
> **7.750 mm**, all of it at the top. The bottom loses nothing and in fact hides
> 0.35 mm more unlit board. **CAD reports this; only the powered test can say
> whether it is acceptable.** Build report §5.

> **One deliberate deviation from Rev N**, and only one: the window **height**
> is now derived from the lip at 14.200 mm instead of the Rev N 14.900 mm. At
> 14.900 the lip's 0.400 mm wall would have met the bezel face over just
> 0.050 mm at the top and bottom — a knife-edge root and a sliver. It costs
> nothing optically, because the lip already controlled the clear height. The
> window **width** is untouched. Build report §3.3.

### Rebuilding Rev Q

Inside Fusion (Utilities → Add-Ins → Scripts), point `OUT_DIR` at this clone's
`mechanical` folder and run `main()`, `import_carrier()`, `coupon()`,
`corner_study()`, `validate()`, `export()` and `snapshots()`. `main()` creates
its own new document and never opens, modifies or saves the Rev N, Rev O or
Rev P documents; `export()` refuses, in code, to write any path whose basename
contains `revN`, `revO` or `revP`. Then, offline:

```bash
python mechanical/CAD/Decca_Display_Bezel_revQ_verify.py
```

`Front_Bezel_revN.step` remains the last **released** bezel and is untouched.

---

## Display mount — current revision: **P.5 — RELEASED**

**The Rev P.5 carrier has been manufactured, installed and physically tested,
and every test passed:** Perspex fit and tolerances; OLED front insertion and
removal; all four sprung posts and retention; no collision with the original
Decca lighting unit; bottom / open connector-side clearance; the reduced
6.00 mm thickness; the enlarged 14.00 × 4.19 mm connector opening; the rear
closure and light-blocking features; the original fasteners and captive nuts;
49.00 mm horizontal pitch; the mounting points 7.00 mm lower giving the
required OLED position; and installed fit, screen position, stiffness,
retention, clearance and powered operation.

Rev P.2 is the corrected **flush-side-insertion** architecture, and it **passed**
its physical OLED-retention and Perspex-fit tests. **Rev P.3** amended only the
radio-side interface: the lighting-unit clearance cut and the original Decca
bolt / captive-nut interface that replaces the deleted M2 heat-set inserts.
**Rev P.4** makes two bounded corrections on top of that:

- the **synthetic lighting-unit keepout is deleted** — component, body,
  generator function, derived geometry, intersection checks and exports. Its
  boundary was asserted from the carrier's own pedestals, not measured off the
  radio, so it proved nothing and misrepresented the assembly. Nothing replaces
  it, and the physical rail cut it was invented to justify is kept exactly as
  printed. **Installed clearance is proven by physical test only** — see the
  build review §20.6;
- the **rear of the OLED bay is closed** by a 1.20 mm integral opaque light
  shield, part of the carrier, with a single local four-pin/header opening —
  build review §24.

**Rev P.5** is a mandatory amendment that changes load-bearing numbers:

- both **plain locating posts are deleted** and replaced by sprung
  locating-and-retaining posts — all four PCB mounting holes now hold a split
  sprung post, and no plain-post parameter, body, branch or probe survives;
- the complete OLED reference is rotated **180° in plane**, so the four-pin
  connector is at the **bottom**. The panel-fixed holes do not move. **The open
  lighting-unit end of the carrier travelled with the module, +Y → −Y**;
- both carrier fixing centres then move **7.00 mm toward that bottom** relative
  to the OLED group (`carrier_fix_y_from_previous = -7.00 mm`). The Perspex
  holes are untouched, so the equivalent — and the only implementation that
  lands the carrier holes *on* them — is to raise the OLED bay **+7.00 mm**.
  This **supersedes** the earlier active-area-bottom-to-opening-bottom rule and
  every PASS based on it;
- the carrier drops to **6.00 mm** deep, the finished rear opening grows 25 % to
  **14.00 × 4.19 mm**, and two integral **light-block** baffles are added
  beside it, running out into the sprung pedestals.

Nothing numeric is inherited: the depth reduction shortens every cantilever, so
the split slot goes 0.70 → 1.20 mm and the root relief 3.20 → 2.00 mm. Build
review §25.3 has the recalculation.

> **The screen is no longer fully visible.** Only **8.30 mm** of the 14.70 mm
> active height falls inside the Perspex opening; about **6.40 mm — 44 % —**
> sits behind the fascia above it, and the lowest 7.00 mm of the opening shows
> unlit board. Both tools **report** this and neither passes a check on it.
> Whether the intended screen information is still readable is a question only
> the powered fit test can answer. Build review §28.3.

> **The bonded-glass boundary is now THE print gate.** The two converted posts
> put a nose ahead of the PCB at holes the plain posts never reached, and the
> modelled glass envelope — which has never been measured, and which puts the
> glass over the mounting holes — says it fouls by 0.40 mm. Both tools report
> those checks as **BLOCKED**, not passed and not failed. Measure the boundary,
> enter it, set `oled_glass_measured` / `GLASS_MEASURED`, and they become
> ordinary hard gates. Build review §25.4.

The `.f3d` is the source of truth; the STEPs and the STL are derived exports.

| File | Role |
|---|---|
| `Decca_Display_Mount_revP.f3d` | **editable source of truth** — fully parametric, 192 named user parameters |
| `Decca_Display_Mount_revP_fusion.py` | the generator that builds the `.f3d`; single source of truth for every dimension |
| `Decca_Display_Mount_revP_verify.py` | independent offline verification of the exported STL (numpy only) |
| `Rear_Display_Carrier_revP.step` | the one structural part |
| `Decca_Display_Mount_revP_assembly.step` | carrier + Perspex + OLED + bezel + **original nuts / bolt envelope** references. **No lighting-unit keepout proxy** — Rev P.4 deleted it, and both tools assert its absence |
| `Hex_Pocket_Fit_Coupon_revP.step` | five-station captive-nut pocket fit coupon — print this **before** the carrier |
| `Front_Bezel_revN.step` | cosmetic bezel — **unchanged, still the file of record for Rev P, and the last RELEASED bezel**. Superseded for new work by the OPEN Rev Q above, which is not yet released |

Rev N files are retained as the last front-loaded design:
`Decca_Display_Mount_revN.f3d`, `Decca_Display_Mount_revN_assembly.step`,
`Rear_Display_Carrier_revN.step`, `Retainer_Bar_revN.step`. The Rev P
architecture deletes the retainer bar, so `Retainer_Bar_*` has no Rev P
equivalent.

### Rebuilding

Inside Fusion (Utilities → Add-Ins → Scripts), point `OUT_DIR` at this clone's
`mechanical` folder and run `main()`, `validate()`, `import_bezel()`,
`snapshots()`, `export()`, and `coupon()`. `main()` creates its own new document
and never modifies the Rev N or Rev O files; `snapshots()` regenerates the five
Drawings PNGs from the live model; `coupon()` builds and exports the hex-pocket
fit coupon in its own document. Then, offline:

```bash
python mechanical/CAD/Decca_Display_Mount_revP_verify.py
```

It reads only the exported STL and exits non-zero on failure, so it works as a
gate. See `../Drawings/Decca_OLED_Display_Mount_CAD_Build_revP.md` §13 for why
it is deliberately not a second run of the same recipe — and for the silent
Fusion `createTorus` failure it caught.

> **Rev P.5 is RELEASED.** Every item that was outstanding here — the
> bonded-glass clearance, the original nut and bolt fit, the hex-pocket
> allowance, installed lighting-unit clearance, the light-leak test and the
> powered fit — was closed by the built and tested prototype. Both tools record
> them as `[TEST]`, and neither check was changed to get there.

> **What is still a modelling caveat, and is not a blocker.** Two inputs in
> the parameter table were never measured, and the prototype passing did not
> measure them:
>
> - `oled_glass_w` / `_h` / `_off_y` — the bonded-glass envelope is still the
>   placeholder that puts glass over the mounting holes. The built part clears
>   the real glass; the **model** does not describe it. `oled_glass_measured`
>   stays `False`;
> - *(resolved 2026-08-30 — `original_nut_hex_width` was here; the 3.80 mm
>   across-flats reading is **confirmed**, so it is a measured value now)*
> - the original bolt length under the head. The bolts engage and clamp; the
>   length itself was not recorded.
>
> These matter only if the geometry is regenerated with changed dimensions. As
> built, the part is proven. Anyone changing a post, a nose, the glass keep-out
> or the nut pocket must measure first.
