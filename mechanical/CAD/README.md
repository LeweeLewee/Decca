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

> **READ THIS BEFORE PRINTING A BEZEL.** After the owner's interference-fit
> refinement the inset wall measures **36.20 × 17.20 mm** against a MEASURED
> Perspex opening of **35.20 × 15.30 mm** — 1.00 mm oversize across and
> **1.90 mm oversize up**. As modelled the part cannot enter the opening at
> all. Either `panel_open_h` is stale and the real opening needs re-measuring,
> or the vertical move overshoots. The geometry is exactly as instructed and
> fully validated; the fit is not. Build report §3.7 and §8.1.

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
| Bezel face opening, at the front face | **32.900 × 15.600**, R1.750 |
| Aperture | a **straight bore** — identical at the front face and the seating plane, taper 0.00° |
| Inset-wall outer envelope | **36.200 × 17.200** |
| Inset-wall inner envelope (derived) | 32.900 × 15.600 — **flush with the face opening on all four sides** |
| Wall | **1.650 sides** (4.125 loops) / **0.800 top+bottom** (2.000 loops) |
| Outer / inner corner radius | **R3.400** / R1.750 (derived from the side wall) |
| Wall depth | **2.800** into the 3.00 mm Perspex |
| Horizontal fit | **0.500 INTERFERENCE per side** |
| Vertical fit | **0.950 INTERFERENCE per side** |
| Entry lead-in | 0.200 × 45°, outer rear edge only |
| Rearmost material | z = **+0.200** — 0.200 clear of the Perspex rear face |
| Clearance to the OLED glass | **0.500** — the released Rev N/P value |
| Minimum distance to the Rev P.5 carrier | 0.602 |
| Effective clear optical opening | **32.900 × 15.600**, R1.750 |
| Seating face | one unbroken annulus, 195.850 mm² (adhesive pads deleted) |
| Volume | 0.6300 cm³ ≈ 0.80 g in PETG |

**52/52 gates PASS** in Fusion; **46/46 PASS** offline from the mesh. One shell,
one lump, zero slivers, no degenerate triangles; the wall's cross-section area
matches the analytic value to four decimals at three depths and in every region
including the corners; the interference is exactly 0.500 mm per side across and
0.950 mm up, nowhere more, and vanishes when the declared relief is applied;
zero interference with the OLED glass or the carrier; nothing behind the
Perspex rear face.

> **The fit is the open risk, and it is no longer a question of force.** The
> skirt is larger than the hole on both axes — see the warning above. If it
> does enter, insertion force is next: the horizontal interference is resisted
> by the **1.65 mm side** wall, about **70× stiffer in bending** than the
> original 0.40 mm and 8.8× stiffer than 0.80 mm, while the vertical is
> resisted by the far more compliant 0.80 mm top and bottom walls carrying
> nearly twice the interference. Brief §3.8 requires the printed wall to take
> the deflection and the Perspex to be left unstressed; CAD cannot settle it.
> **Print `Bezel_Fit_Gauge_revQ` first** — five tabs at
> 0.00/0.05/0.10/0.15/0.20 mm interference, each carrying the real wall
> section and the full 17.20 mm height. Build report §8.1.

> **The loop rule is a PRODUCTION gate, not a CAD one.** CAD proves the
> geometry admits the loops: sides 1.650/0.400 = 4.125, top and bottom
> 0.800/0.400 = 2.000 exactly, measured at all 720 stations (min 0.7950, max
> 1.6450) including 368 corner stations, loop centrelines 0.400 apart with
> corner radii 3.200 and 2.800 and no cusp. Only the slicer preview can prove
> it lays them. Build report §7.1 and §10 Stage 0b.

> **Four owner changes on top of the brief, each recorded and each reversible.**
> (1) The two recessed adhesive pads are **deleted** (`pads_enabled = False`).
> (2) The inset-wall outer corner went **R2.00 → R3.00**, because R2.00 did not
> match the real opening corner. (3) The aperture was made **flush** on the left
> and right — the face opening out 1.00 mm per side to 32.90 and the side wall
> derived from it — and the loop rule was clarified to **at least** two per
> side, with the sides and the top/bottom free to differ. (4) The
> **interference-fit refinement**: one extra 0.40 mm loop added outward on each
> side face, and the top and bottom walls moved 1.00 mm out each. Build report
> §3.5, §3.6 and §3.7.

> **The wall now GIVES BACK lit screen height.** The clear opening is
> 32.90 × 15.60, controlled by the skirt on all four sides with the face
> opening flush to it, and the visible active band goes 8.100 → **8.450 mm** —
> 0.350 mm *more* than Rev N, where every earlier issue lost height. Check the
> extra unlit board now visible below the active area in the powered test.
> Build report §5.

> **The aperture no longer tapers.** With the face opening flush to the skirt
> on all four sides there is nothing to blend, so the bore is straight from the
> front face through to the wall tip — no ledge, no set-back, no corner
> crescent. The forced Y taper that earlier issues carried (36.10°, to stop the
> top and bottom wall runs standing detached from the bezel face) is designed
> out, and the generator now **refuses to build** if the face opening drifts
> away from the skirt inner envelope. The window edge break is a 0.40 chamfer
> rather than the Rev N R0.40 fillet, because Fusion refuses a fillet on that
> edge at every radius. Build report §3.3 and §3.4.

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
