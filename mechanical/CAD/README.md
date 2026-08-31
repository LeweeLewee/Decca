# CAD

Source (editable, parametric) mechanical design files.

**Intended contents**
- Fusion 360 archives (`.f3d`) and/or OpenSCAD (`.scad`) source.
- Neutral exchange formats (STEP `.step`) for interop.

**Conventions**
- Keep source here; export print-ready meshes to `../STL/`.
- Parametric source is preferred so parts can be re-derived if dimensions change.
- Record revisions in `docs/Revision History.md`.

## ESP32 controller housing — current revision: **A — PROTOTYPE CAD, NOT physically validated**

Built to `../Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md`. Full write-up:
`../Drawings/Decca_ESP32_Controller_Housing_Build_Report_revA.md`.

**Nothing here has been printed, and no dimension in it has been measured off
the acquired hardware.** Every hardware figure is a CAD starting value taken
from the specification, and every one of them is a prototype gate. The
generator tags them in one place — the `STARTING` tuple — and both verification
tools refuse to mark any of them `PASS`.

Holds **only** the 30-pin ESP32 DevKit V1 / DOIT-style board and its matching
30-pin screw-terminal breakout. The MOSFET board, WAGO connectors, fuse, DC
socket, OLED, WiiM Pro, Fosi ZA3 and the future 12 V trigger are all mounted
separately and were not brought into this box to solve a layout problem.

| File | What it is |
|---|---|
| `Decca_ESP32_Controller_Housing_fusion.py` | The generator. `main()` builds all nine components, `validate()` runs the section 14 gates on the solids, `export()` writes every f3d/STEP/STL into this clone, `images()` regenerates the fourteen review PNGs. Idempotent: re-running rebuilds in place. |
| `Decca_ESP32_Controller_Housing_verify.py` | The independent offline verifier. Reads **only** the exported STLs. `--drawings` plots the two dimensioned views from the same triangles. |
| `Decca_ESP32_Controller_Housing.f3d` | Editable archive, 219 named user parameters. |
| `Decca_ESP32_Controller_Housing_assembly.step` | Assembly, keep-out solids removed for readability. |
| `ESP32_Controller_Housing_Base.step` | Base tray. |
| `ESP32_Controller_Housing_Lid.step` | Lid. |
| `ESP32_Controller_PCB_Clamps.step` | Both edge clamps in one exchange file. |
| `ESP32_Controller_Carrier_Fit_Gauge.step` | Fit gauge. |

**Retention uses no PCB hole.** The repository records no breakout
mounting-hole pattern and specification section 2 forbids inventing one, so
nothing enters the board: one short edge butts a hard datum, the other is held
by a printed clamp with ±1.00 mm of slot travel, and each clamp bottoms on a
plinth 0.20 mm above the board face so tightening cannot bow it.

> **The derived envelope is 105.00 × 77.00 × 38.30 mm against a 90 × 78 ×
> approximately 35 mm target, and that is an open owner decision, not an
> oversight.** Section 10's 72.0 mm body budget contains no length at all for
> the section 5.2 end clamps, their M3 screws, or the section 9 lid bosses that
> section 9 itself requires to sit outside the board outline. The height is
> forced by section 5.1, which measures its 3.00 mm clearance *beneath* the
> solder joints that hang 2.50 mm down. Build report section 5 gives the
> arithmetic and two documented ways to shorten it — one of which brings the
> length inside target by moving the ears to the long sides. Neither was
> applied unilaterally.

### Rebuilding

Inside Fusion (Utilities → Add-Ins → Scripts), or through the Fusion MCP
bridge, run in order:

```python
g = runpy.run_path("mechanical/CAD/Decca_ESP32_Controller_Housing_fusion.py")
g["main"](None)       # build or rebuild every component
g["validate"](None)   # 59 CAD gates; returns the failure count
g["export"](None)     # f3d, STEP and STL into this clone
g["images"](None)     # the fourteen review PNGs
```

Then, offline:

```bash
python mechanical/CAD/Decca_ESP32_Controller_Housing_verify.py
python mechanical/CAD/Decca_ESP32_Controller_Housing_verify.py --drawings
```

The verifier reads only the exported meshes and exits non-zero on failure, so
it works as a gate. It is deliberately not a second run of the generator's
recipe: it caught a floating lacing rail, four non-manifold tangency sites and
four lid legends that reported success while cutting zero material.


## Display bezel — current revision: **Q — COMPLETE, signed off 2026-08-31**

**Rev Q is bezel-only. The released Rev P.5 carrier is FROZEN and unchanged.**

Rev Q replaces the two Rev N side locating rails with **one continuous inset
masking wall** around the complete inside perimeter of the Perspex opening —
left, right, top, bottom and all four corners. The wall conceals the visible
cut edge and locates the bezel on an **interference fit on both axes**. It is
not a snap, not a clamp and carries no load. The two Rev N recessed adhesive
pads are DELETED at owner instruction, so retention is by the fit alone; if
adhesive is still wanted it goes on the flat seating face.

Built to brief commit `7b107f2` ("require two-loop inset wall"), then moved on
by four owner changes made on the model. Every wall carries **at least two
0.40 mm extrusion loops** — a minimum applied per side, not a fixed count.

> **THE PERSPEX OPENING HAS BEEN MEASURED, and it is not what this project
> believed.** For six revisions the model carried 35.20 × 15.30 from Rev C — a
> figure no released part had ever checked, because Rev N located on two side
> rails only. The owner printed the 35.400 × 15.450 insert, used it as a gauge
> block and read the slop: **1.34 mm horizontal, 1.00 mm vertical**. The opening
> is **36.74 × 16.45**, and the insert is now DERIVED from it:
> `insert outer = measured opening + declared interference`. Re-measuring is a
> two-number edit. Treat the reading as ±0.2 mm; a second iteration is expected.
> Build report §3.10.

| File | Role |
|---|---|
| `Decca_Display_Bezel_revQ_fusion.py` | **the generator — single source of truth for every Rev Q dimension** |
| `Decca_Display_Bezel_revQ_verify.py` | independent offline verification of the exported STL (numpy only) |
| `Decca_Display_Bezel_revQ_frozen_check.py` | proves the six frozen Rev P.5 files still match the Rev Q brief — run before and after any Rev Q work. Hashes text files as-is, forced LF and forced CRLF, so a line-ending difference cannot masquerade as tampering |
| `Decca_Display_Bezel_revQ.f3d` | **editable source** — named parameters, derived values written as real formulas |
| `Front_Bezel_revQ.step` | the bezel alone |
| `Decca_Display_Bezel_revQ_assembly.step` | bezel + measured Perspex + OLED glass proxy + the **unchanged Rev P.5 carrier**. Does **not** overwrite `Decca_Display_Mount_revP_assembly.step` |
| `Bezel_Fit_Gauge_revQ.step` | five-tab interference fit gauge — **print this before the bezel** |

Key dimensions, each verified by two independent tools:

| | mm |
|---|---:|
| Bezel face opening, at the front face | **34.440 × 15.000**, R3.000 |
| Aperture | a **straight bore** — identical at the front face and the seating plane, taper 0.00° |
| **Perspex opening, MEASURED 2026-08-31** | **36.740 × 16.450** |
| Inset-wall outer envelope | **36.940 × 16.600** — derived, opening + fit |
| Inset-wall inner envelope (derived) | 34.440 × 15.000 — **flush with the face opening on all four sides** |
| Wall | **1.250 sides** (3.125 loops) / **0.800 top+bottom** (2.000 loops) |
| Outer / inner corner radius | **R4.250** / R3.000 (derived from the side wall) |
| Wall depth | **2.800** into the 3.00 mm Perspex — 2.300 tried and reverted |
| Horizontal fit | **0.100 INTERFERENCE per side** |
| Vertical fit | **0.075 INTERFERENCE per side** |
| Entry lead-in | 0.200 × 45°, outer rear edge only — tip is 0.100 / 0.125 mm per side UNDER the opening |
| Rearmost material | z = **+0.200** — 0.200 clear of the Perspex rear face |
| Clearance to the OLED glass | **0.500** — the brief minimum, and the released Rev N/P value |
| Minimum distance to the Rev P.5 carrier | **0.339** — carry this forward |
| Effective clear optical opening | **34.440 × 15.000**, R3.000 |
| Seating face | one unbroken annulus, 210.867 mm² (adhesive pads deleted) |
| Volume | 0.5951 cm³ ≈ 0.76 g in PETG |

**52/52 gates PASS** in Fusion; **47/47 PASS** offline from the mesh. One shell,
one lump, zero slivers, no degenerate triangles; the wall's cross-section area
matches the analytic value to four decimals at three depths and in every region
including the corners; the interference is exactly 0.100 mm per side across and
0.075 mm up, nowhere more, and vanishes when the declared relief is applied;
zero interference with the OLED glass or the carrier; nothing behind the
Perspex rear face.

> ## Signed off — 2026-08-31
>
> **The bezel is complete.** Confirmed on printed parts: the interference
> fit, the opening corner (R4.25 a good match) and the opening dimensions
> themselves. A 2.30 mm insert depth was tried and **reverted** when the
> bottoming-out that prompted it turned out to be a printing issue rather
> than the geometry — the depth is back at the proven Rev N 2.80 mm.
>
> **Not separately reported at sign-off:** the slicer two-loop preview and
> the powered visibility test. Parts printed and fitted, so the wall
> evidently laid, but neither was run as a check.
>
> **One figure to carry forward:** the bezel passes within **0.339 mm** of
> the frozen Rev P.5 carrier. Zero interference, and it has been assembled,
> but worth re-checking if either part is reprinted on a different machine.
> Build report §3.11–§3.12.

> **The fit is the primary gate.** 0.100 / 0.075 mm per side is an ordinary
> press fit on paper, but acrylic is brittle and takes up interference by
> storing stress rather than deforming, the 1.25 mm side wall is ≈31× stiffer
> in bending than the original 0.40 mm, and **print tolerance is the same size
> as the fit** — ±0.10 mm on a small external dimension, so 0.100 mm intended
> arrives anywhere between 0.00 and 0.25 mm. No CAD check can touch that.
> **Print `Bezel_Fit_Gauge_revQ` first** — five tabs at
> 0.00/0.05/0.10/0.15/0.20 mm, which now brackets the declared value two either
> side, each carrying the real wall section, the full 16.60 mm height, the
> 2.80 mm depth and both R4.25 corners — and the sweep brackets the ±0.2 mm
> **measurement** error as well as the fit. Also plan on adhesive: **PETG
> creeps**, so a press fit slackens over months. Build report §8.1, §8.4.

> **The loop rule is a PRODUCTION gate, not a CAD one.** CAD proves the
> geometry admits the loops: sides 1.250/0.400 = 3.125, top and bottom
> 0.800/0.400 = 2.000 exactly, measured at all 720 stations (min 0.7950, max
> 1.2500) including 368 corner stations, loop centrelines 0.400 apart with
> corner radii 4.050 and 3.650 and no cusp — the easiest to slice at any issue.
> Only the slicer preview can prove it lays them. Build report §7.1 and §10
> Stage 0b.

> **The opening corner is largely closed — by a printed part.** The owner offered
> the R4.25 insert into the real opening and reports the corner **a good match**,
> retracting an earlier appearance-based revert in as many words. At R4.25
> against the measured opening the **flanks set the fit for every plausible
> opening corner**: penetration never leaves 0.100 mm from a sharp corner all the
> way to R4.00. `panel_open_corner_r` stays 0.00 in the model, because a
> qualitative match is evidence rather than a measurement and modelling the
> opening sharp keeps every figure at its worst case. Build report §8.3.

> **Seven owner changes on top of the brief, each recorded and each reversible.**
> (1) adhesive pads **deleted**; (2) outer corner **R2.00 → R3.00**; (3) aperture
> made **flush** on the left and right, loop rule clarified to **at least** two
> per side; (4) the **interference-fit refinement**, which appeared not to fit;
> (5) the **pull-back**; (6) the corner **reverted to R3.00** on the render;
> (7) **the opening measured** — which restored the corner to R4.25 on physical
> evidence, showed the recorded opening was 1.54 × 1.15 mm small, and made the
> insert derive from the measurement; (8) **the depth cut 2.80 → 2.30** after a
> printed part bottomed out before seating; and (9) that cut **reverted** when
> the cause proved to be a printing issue, followed by **sign-off**. Build report
> §3.5 to §3.12.

> **The wall no longer costs lit screen height.** The clear opening is
> 34.44 × 15.00, controlled by the skirt on all four sides with the face
> opening flush to it, and the visible active band goes 8.100 → **8.150 mm** —
> **above Rev N for the first time**, because the opening was always bigger than
> recorded. What is worth judging instead is the noticeably slimmer black
> border: the bezel flange is now 1.530 mm at the sides. Build report §5.

> **The aperture does not taper.** With the face opening flush to the skirt on
> all four sides there is nothing to blend, so the bore is straight from the
> front face through to the wall tip — no ledge, no set-back, no corner
> crescent. The forced Y taper earlier issues carried is designed out, and the
> generator **refuses to build** if the face opening drifts away from the skirt
> inner envelope. The window edge break is a 0.40 chamfer rather than the Rev N
> R0.40 fillet, because Fusion refuses a fillet on that edge at every radius.
> Build report §3.3 and §3.4.

### Rebuilding Rev Q

Inside Fusion (Utilities → Add-Ins → Scripts), point `OUT_DIR` at this clone's
`mechanical` folder and run `main()`, `import_carrier()`, `coupon()`,
`fit_study()`, `validate()`, `export()` and `snapshots()`. `main()` creates its
own new document and never opens, modifies or saves the Rev N, Rev O or Rev P
documents; `export()` refuses, in code, to write any path whose basename
contains `revN`, `revO` or `revP`. Then, offline:

```bash
python mechanical/CAD/Decca_Display_Bezel_revQ_verify.py
python mechanical/CAD/Decca_Display_Bezel_revQ_frozen_check.py
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
| `Front_Bezel_revN.step` | cosmetic bezel — **unchanged, still the file of record for Rev P**. Superseded for new work by the signed-off Rev Q above |

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
