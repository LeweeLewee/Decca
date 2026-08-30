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
cut edge and locates the bezel on a **controlled 0.10 mm per side horizontal
interference**, with 0.05 mm vertical clearance. It is not a snap, not a clamp
and carries no load. The two Rev N recessed adhesive pads are DELETED at owner
instruction, so retention is now by the interference fit alone; if adhesive is
still wanted it goes on the flat seating face.

Built to brief commit `7b107f2` ("require two-loop inset wall"): the wall is
**0.80 mm**, exactly **two 0.40 mm extrusion loops**, because the first issue's
0.40 mm wall resolved as only one loop in the slicer.

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
| Bezel face opening, at the front face | **30.900 × 15.350**, R0.800 |
| Inset-wall outer envelope | **35.400 × 15.200** |
| Inset-wall inner envelope (derived) | 33.800 × 13.600 |
| Wall | **0.800** = exactly two 0.400 mm loops |
| Outer / inner corner radius | **R3.000** / R2.200 (derived) |
| Wall depth | **2.800** into the 3.00 mm Perspex |
| Horizontal fit | **0.100 INTERFERENCE per side** |
| Vertical fit | 0.050 clearance per side |
| Entry lead-in | 0.200 × 45°, outer rear edge only |
| Rearmost material | z = **+0.200** — 0.200 clear of the Perspex rear face |
| Clearance to the OLED glass | **0.500** — the released Rev N/P value |
| Minimum distance to the Rev P.5 carrier | 0.939 |
| Effective clear optical opening | **30.900 × 13.600**, R0.800 |
| Seating face | one unbroken annulus, 278.212 mm² (adhesive pads deleted) |
| Volume | 0.6304 cm³ ≈ 0.80 g in PETG |

**46/46 gates PASS** in Fusion; **42/42 PASS** offline from the mesh. One shell,
one lump, zero slivers, no degenerate triangles; the wall's cross-section area
matches the analytic value to four decimals at three depths and in every region
including the corners; interference is exactly 0.100 mm per side, located only
on the horizontal flanks and vanishing when the declared relief is applied;
zero interference with the OLED glass or the carrier; nothing behind the
Perspex rear face.

> **The interference is the open risk now.** The wall went 0.40 → 0.80 mm to
> get the second loop, and **bending stiffness scales with thickness cubed**,
> so it is about **8× stiffer** and resists the same 0.10 mm per side roughly
> 8× harder. Brief §3.8 requires the printed wall to take the deflection and
> the Perspex to be left unstressed; at 0.80 mm that split is no longer
> obvious and CAD cannot settle it. **Print `Bezel_Fit_Gauge_revQ` first** —
> five tabs at 0.00/0.05/0.10/0.15/0.20 mm interference, each carrying the real
> wall section. Build report §8.1.

> **Two continuous loops is a PRODUCTION gate, not a CAD one.** CAD proves the
> geometry admits them: 0.800/0.400 = 2.000 exactly, wall 0.8000 min and max
> over 720 stations including 368 corner stations, loop centrelines 0.400 apart
> with corner radii 2.800 and 2.400 and no cusp. Only the slicer preview can
> prove it lays them. Build report §7.1 and §10 Stage 0b.

> **Two owner changes on top of the brief, both single parameters and both
> reversible.** The two recessed adhesive pads are **deleted**
> (`pads_enabled = False`) — brief §3.1 asks for them preserved, but the
> interference fit makes bonded pads redundant, and the seating face is now one
> unbroken annulus. And the inset-wall outer corner is raised 50%, **R2.00 →
> R3.00**, because R2.00 did not match the real opening corner; penetration now
> holds at exactly 0.100 mm across the whole plausible range of opening corner
> radii, at the cost of a larger unmasked corner gap. Build report §3.5.

> **The wall costs 0.650 mm of lit screen height.** The clear opening is
> 30.90 × 13.60 — width by the face opening, **height by the wall** — and the
> visible active band drops 8.100 → **7.450 mm**, all of it at the top. Only
> the powered test can say whether that is acceptable. Build report §5.

> **One forced modelling decision, fully declared.** The amended face opening
> (15.35) is *taller than the whole wall* (15.20), so a straight-walled
> aperture would leave the top and bottom wall runs **detached** from the bezel
> face. The aperture therefore **tapers in Y**, 13.640 at the seating plane to
> 15.350 at the front face, at 35.47° — self-supporting, every published number
> preserved. The window edge break is a 0.40 chamfer rather than the Rev N
> R0.40 fillet, because Fusion refuses a fillet on the tapered aperture edge at
> every radius. Build report §3.3 and §3.4.

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
