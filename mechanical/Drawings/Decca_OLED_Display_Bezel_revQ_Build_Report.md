# Decca OLED Display Bezel — Rev Q Build Report

Status: **OPEN — bezel-only integration prototype. NOT released, NOT for merge.**

Date: 2026-08-30
Controlled requirements: `Decca_OLED_Display_Bezel_CAD_Brief_revQ.md` at commit
`7b107f2389b2ce128c18bef2f5195ef5ab468890` ("require two-loop inset wall"),
which supersedes `ebfa277` via `edab34b` ("define Rev Q interference fit")
Specification: `Decca_OLED_Display_Mount_Spec_v1.0.md` v1.2, §2 and §4
Carrier: **Rev P.5, RELEASED and FROZEN — unchanged, and proved unchanged (§9)**

> **The first Rev Q print is an integration prototype, not a release part.**
> Two things it must settle, and CAD cannot: whether a **0.10 mm per side
> horizontal interference** seats without stressing the original Perspex now
> that the wall is **8× stiffer in bending**, and whether the production
> slicer really lays **two continuous 0.40 mm loops** all the way round.
> Nothing in this report is a claim about appearance.

---

## 1. What Rev Q changes

The Rev N pair of side locating rails is deleted and replaced by a single
continuous rearward inset wall around the **complete** inside perimeter of the
Perspex opening — left, right, top, bottom and all four corners.

```text
front
BEZEL FACE
──────────────  seats against the Perspex front face,  z = +3.000
       │
       │  continuous 0.80 mm inset wall, 2.80 mm rearwards,
       │  two 0.40 mm extrusion loops
PERSPEX│
───────┘        wall rear tip,                         z = +0.200
rear
```

The wall is a **masking and locating skirt**. Its only interference is the
declared **0.10 mm per horizontal side**; vertically it runs on a 0.05 mm
clearance. It is not a snap, not a clamp and not a structural feature, and it
carries no load. Retention remains removable adhesive on the unchanged
recessed pads.

### 1.1 What the two owner amendments changed

| | first issue (`ebfa277`) | as built now (`7b107f2`) |
|---|---:|---:|
| Bezel face opening | 30.40 × 14.90 | **30.90 × 15.35** |
| Inset-wall outer envelope | 34.90 × 15.00 | **35.40 × 15.20** |
| Horizontal fit | 0.15 clearance/side | **0.10 INTERFERENCE/side** |
| Vertical fit | 0.15 clearance/side | **0.05 clearance/side** |
| Wall | 0.40 (one loop) | **0.80 (two loops)** |
| Outer corner radius | R0.60, UNRESOLVED | **R2.00, specified** |
| Inner corner radius | R0.20 | **R1.20** |
| Wall inner envelope | 34.10 × 14.20 | **33.80 × 13.60** |
| Effective optical opening | 30.40 × 14.20 | **30.90 × 13.60** |
| Depth | 2.80 | 2.80 (unchanged) |

The corner radius has moved from being *the* open risk to being a specified
value. The open risk is now the **interference**, and the **slicer**.

---

## 2. Verified facts

### 2.1 Recovered from the released Rev N bezel — read-only evidence

`Front_Bezel_revN.step` was parsed as a BREP and every figure below was
measured out of it. The file was **not** opened for edit, not regenerated and
not re-exported.

| Recovered feature | Value | How |
|---|---|---|
| Overall envelope | 40.000 × 20.300 × 4.000 mm | vertex bounding box |
| X / Y extents | ±20.000 / ±10.150 mm | vertex bounding box |
| Z levels present | +0.200, +3.000, +3.300, +3.800, +4.200 | vertex Z census |
| External corner radius | **R2.000** at (±18.000, ±8.150) | cylindrical surfaces |
| Front edge break | **R0.400**, torus major 1.600 at the corners | toroidal surfaces |
| Visible window | 30.400 × 14.900, **R0.800** at (±14.400, ±6.650) | planes + cylinders |
| Window edge break | **R0.400**, torus major 1.200 | toroidal surfaces |
| Adhesive pads | x ±12.000, y 7.850…9.850 and −9.850…−7.850 | planes |
| Adhesive pad depth | 0.300 (floor at z = +3.300) | plane at z = 3.300 |
| **Locating rails — TWO ONLY** | x 15.300…17.450 and mirror, **y −4.000…+4.000** | R0.600 cylinders |
| Rail depth | z +0.200 … +3.000 = **2.800 mm** | plane pair |

Cross-checked against the Rev P build review §16, which independently states
40.00 × 20.30 × 4.00, a 2.80 mm lip depth, rearmost material at z = +0.200 and
0.500 mm clearance to the OLED glass. Both sources agree exactly.

> Note on the brief's `bezel_window_h` derivation. Brief §4 annotates
> 15.35 mm as "Rev N 15.10 + 0.25". 15.10 is the **v1.0 design-intent**
> figure from Spec §4; the **as-built** Rev N window measures **14.900 mm**
> in the released STEP. The 15.35 mm target itself is taken as authoritative
> and is built exactly; only the annotation's starting point is superseded.
> The width annotation ("Rev N 30.40 + 0.50") matches the as-built part.

### 2.2 The Z-chain — unchanged from Rev N and Rev P.5

```text
z = +4.200   bezel front face
z = +3.000   Perspex FRONT face  == bezel seating plane
z =  0.000   Perspex REAR face   == DATUM A, carrier hard stop
z = -0.300   OLED glass front face
             wall rear tip at z = +0.200
             -> 0.200 mm clear of the Perspex rear face
             -> 0.500 mm clear of the OLED glass  (the RELEASED value)
```

### 2.3 What the Rev N rails proved, and what they did not

* **PROVED:** the 2.80 mm engagement depth, and that a 34.90 mm outer envelope
  clears the opening in X.
* **NOT PROVED — anything in Y.** The rails span only y −4.000…+4.000. No Rev N
  surface has ever touched the top or bottom of the Perspex opening.
* **NOT PROVED — anything at any corner.** Rev G's note that the rail design
  "tolerates opening corner radii to R3.65" is the giveaway: that architecture
  was chosen *precisely so the unknown corner form would not matter*. Rev Q is
  the first bezel geometry that has to go into those corners.

### 2.4 Measured fascia geometry — Spec v1.2 §2

| Parameter | Value | Source |
|---|---:|---|
| Display opening | **35.20 × 15.30 mm** | measured, Rev C |
| Perspex thickness | **3.00 mm** | measured |
| Opening corner radius | **NOT RECORDED** | — see §8 |

The released Rev P generator models the opening as a **sharp-cornered box**.
Rev Q's reference panel does the same, so the two representations stay
identical. That is a modelling convention, not a measurement, and this report
never treats it as one.

---

## 3. Named parameters

Created before any dependent geometry and mirrored into Fusion user parameters,
the derived ones as real formulas so the derivation is visible in the UI.
Source of truth is the `P` dict in
`../CAD/Decca_Display_Bezel_revQ_fusion.py`.

### 3.1 Controlling parameters

| Parameter | Value | Class | Note |
|---|---:|---|---|
| `panel_open_w` | 35.20 mm | MEASURED | Rev C |
| `panel_open_h` | 15.30 mm | MEASURED | Rev C |
| `panel_t` | 3.00 mm | MEASURED | |
| `panel_open_corner_r` | 0.00 mm | **UNRESOLVED** | modelled sharp, as the released Rev P reference. Not a measurement. |
| `bezel_w` / `bezel_h` / `bezel_t` | 40.00 / 20.30 / 4.00 mm | PRESERVED | Rev N |
| `bezel_outer_r` | 2.00 mm | PRESERVED | Rev N external corner |
| `bezel_edge_break` | 0.40 mm | PRESERVED | front face break |
| `bezel_window_w` | **30.90 mm** | AMENDED | Rev N 30.40 + 0.50 |
| `bezel_window_h` | **15.35 mm** | AMENDED | face opening, **at the front face** |
| `bezel_window_r` | 0.80 mm | PRESERVED | window corner radius |
| `pad_*` | 12.00 / 7.85 / 9.85 / 0.30 mm | PRESERVED | adhesive pads |
| **`bezel_lip_outer_w`** | **35.40 mm** | AMENDED | Rev N 34.90 + 2 × 0.25 |
| **`bezel_lip_outer_h`** | **15.20 mm** | AMENDED | Rev N 15.00 + 2 × 0.10 |
| **`bezel_lip_depth`** | **2.80 mm** | PROVEN | Rev N engagement depth |
| **`bezel_lip_wall`** | **0.80 mm** | AMENDED | two 0.40 mm loops |
| **`bezel_lip_corner_r`** | **2.00 mm** | SPECIFIED | outer corner radius |
| **`bezel_lip_lead`** | **0.20 mm** | PROVISIONAL | minimum entry lead-in |
| **`extrusion_width`** | **0.40 mm** | PRODUCTION | the wall *is* two of these |
| `ap_root_relief` | 0.02 mm | MODELLING | anti-tangency, §3.4 |

### 3.2 Derived — never entered twice

| Parameter | Formula | Value |
|---|---|---:|
| `bezel_lip_interf_x` | `(bezel_lip_outer_w − panel_open_w) / 2` | **+0.100 mm** (interference) |
| `bezel_lip_clear_y` | `(panel_open_h − bezel_lip_outer_h) / 2` | **+0.050 mm** (clearance) |
| `bezel_lip_inner_w` | `bezel_lip_outer_w − 2 × bezel_lip_wall` | **33.800 mm** |
| `bezel_lip_inner_h` | `bezel_lip_outer_h − 2 × bezel_lip_wall` | **13.600 mm** |
| `bezel_lip_inner_r` | `bezel_lip_corner_r − bezel_lip_wall` | **1.200 mm** |
| `wall_loops` | `bezel_lip_wall / extrusion_width` | **2.000** |
| `aperture_rear_h` | `bezel_lip_inner_h + 2 × ap_root_relief` | 13.640 mm |
| `bezel_face_t` | `bezel_t − bezel_lip_depth` | 1.200 mm |
| `z_lip_rear` | `z_panel_front − bezel_lip_depth` | +0.200 mm |

Three constraints are enforced in code and refuse to build if violated:

* `bezel_lip_wall` must be a **whole multiple** of `extrusion_width`, and that
  multiple must be **at least 2** — otherwise the slicer cannot resolve the
  wall as complete loops and substitutes gap fill or a variable-width wall,
  which is exactly what this amendment exists to stop;
* `bezel_lip_corner_r ≥ bezel_lip_wall`, since the inner corner radius is
  `corner_r − wall` and cannot go negative;
* no export path may write a file whose name contains `revN`, `revO` or `revP`.

### 3.3 The aperture has to taper, and here is why

**This is the one modelling decision the amended numbers force, and it is not
optional.**

The amended face opening is **15.35 mm** high. The entire inset wall is only
**15.20 mm** high. So the face opening is **0.075 mm taller per side than the
outside of the wall**, and at the top and bottom the wall footprint
(|y| 6.800…7.600) falls *entirely inside it*.

A straight-walled face opening would therefore leave the top and bottom runs of
the wall **detached from the bezel face** — roughly 31 mm of free-standing
cantilever joined only near the corners, floating in the aperture. That is
unprintable without support and is not one sound solid.

In X there is no such problem: the face opening (half 15.450) is *narrower*
than the wall inner (half 16.900), so the left and right runs land on solid
face material with 1.450 mm to spare. **Only Y is affected.**

Resolution: the aperture is **30.900 mm wide throughout** and **tapers in Y**
from the wall inner opening at the seating plane to the specified face opening
at the front face.

| | value |
|---|---:|
| Aperture at the seating plane (z = +3.000) | 30.900 × 13.640 |
| Aperture at the front face (z = +4.200) | **30.900 × 15.350** |
| Taper angle from vertical | **35.47°** — self-supporting |
| Wall root landing on solid face material | 0.760 of the 0.800 mm |

Every published number survives: the bezel face opening is 30.90 × 15.35 at the
front face, the wall inner envelope is 33.80 × 13.60, and the effective optical
opening is 30.90 × 13.60 — with the **height controlled by the wall**, exactly
as brief §4 predicts. Spec v1.2 §4 asks for a flared aperture in any case, "to
reduce tunnel effect through the 3 mm Perspex".

### 3.4 Two small modelling measures, both declared

**`ap_root_relief` = 0.02 mm.** The aperture stops 0.02 mm per side *outside*
the wall inner opening rather than exactly on it. Landing it exactly on
y = ±6.800 makes the tapered wall tangent to the wall's inner face along a line
at z = 3.000, and the tessellator answers that with a seam of zero-area
triangles — **52 of them in the first export, all at exactly z = 3.0000**.
Backing the aperture off turns that tangency into an ordinary transverse
intersection and the degenerate triangles disappear entirely (verified: minimum
triangle area went from 0.000 to 6.297 × 10⁻⁴ mm²). The **wall still controls
the clear height at 13.600 mm**, because the aperture is now the wider of the
two.

**The window edge break is a chamfer, not a fillet.** The outer envelope keeps
the Rev N R0.40 *fillet* exactly. The window edge cannot: the tapered aperture
is a single NURBS surface whose front edge is one closed NURBS curve with a
varying dihedral — 90° down the vertical left and right walls, 53.9° where the
top and bottom lean back, sweeping between the two through the corners. Fusion
refuses a fillet there at **every radius tried (0.40, 0.30, 0.20, 0.10 — all
`ASM_BL_UNFIN_SHEET`)**, whole-loop and per-edge alike. A **0.40 × 45°
chamfer** succeeds cleanly and is what is built. At 0.40 mm on a matt black
part the two are indistinguishable by eye, and the window had already been
re-dimensioned and flared by the amendment, so its section could not have been
carried over from Rev N unchanged in any case. **This is a declared deviation
and the only one in the visible face detail.**

---

## 4. Exact resulting dimensions

| | mm |
|---|---:|
| Bezel envelope | **40.000 × 20.300 × 4.000** |
| Bezel face thickness | 1.200 |
| External corner radius | R2.000 |
| Front edge break, outer | R0.400 fillet |
| Front edge break, window | 0.400 × 45° chamfer (§3.4) |
| Seating plane (Perspex front) | z = +3.000 |
| Bezel front face | z = +4.200 |
| **Bezel face opening, at the front face** | **30.900 × 15.350**, R0.800 |
| Aperture at the seating plane | 30.900 × 13.640 |
| Aperture taper | 35.47° from vertical, Y only |
| **Inset-wall outer envelope** | **35.400 × 15.200** |
| **Inset-wall inner envelope** | **33.800 × 13.600** |
| **Wall thickness** | **0.800 everywhere, including through the corners** |
| **Wall depth** | **2.800** (z +3.000 → +0.200) |
| Outer corner radius | **R2.000** |
| Inner corner radius | **R1.200** |
| Entry lead-in | 0.200 × 45°, outer rear edge only |
| **Horizontal fit** | **0.100 INTERFERENCE per side** |
| **Vertical fit** | **0.050 clearance per side** |
| Interference volume, as modelled | 6.378 mm³ |
| Rearmost material | z = **+0.200** — 0.200 clear of the Perspex rear face |
| Clearance to OLED glass front face | **0.500** — the released Rev N/P value |
| Minimum distance to the Rev P.5 carrier | **0.939** |
| **Effective optical opening** | **30.900 × 13.600**, R0.800 |
| Solid volume | 0.6056 cm³ (mesh 605.46 mm³) |
| Mass in PETG @ 1.27 g/cm³ | ≈ **0.77 g** |
| Mesh | 7118 triangles, 3559 vertices, closed, manifold, no degenerates |

---

## 5. Optical masking introduced by the wall

**This is the cost of the revision and it must not be glossed over.**

| | Rev N | Rev Q | change |
|---|---:|---:|---:|
| Clear opening width | 30.400 | **30.900** | **+0.500** |
| Clear opening height | 14.900 | **13.600** | **−1.300 total, −0.650 per side** |
| Corner radius | R0.800 | R0.800 | 0 |

The clear height is controlled by the **top and bottom of the inset wall**, not
by the bezel face. That is unavoidable: a continuous wall has to exist at the
top and bottom of the opening, it has to have a wall thickness, and at 0.80 mm
it stands 0.80 mm inboard of the opening on each side.

Going from a 0.40 mm to a 0.80 mm wall cost a further **0.700 mm** of clear
height on top of the first issue's 0.700 mm.

### 5.1 Effect on the powered image

Taking the OLED position from the **released Rev P.5** model — active area
29.42 × 14.70 mm, active centre at y = +6.70 mm after the Rev P.5 +7.00 mm rise:

| | Rev N | Rev Q at 0.40 wall | **Rev Q as built (0.80)** |
|---|---:|---:|---:|
| Visible active width | 29.420 | 29.420 | **29.420** (unchanged) |
| Visible active height | 8.100 | 7.750 | **7.450** |
| Active height lost | — | 0.350 | **0.650**, all at the TOP edge |
| Unlit board visible below | 6.800 | 6.450 | **6.150** |

The bottom edge of the aperture is nowhere near the active area — the active
area's own bottom edge sits at y = −0.650 mm, well inside the aperture — so the
bottom of the wall costs no active area at all and in fact hides 0.65 mm more
unlit board. **The entire optical cost is 0.650 mm off the top of the lit
band**, about 8 % of what was visible at Rev N.

For context, the already-released Rev P.5 condition is far larger than anything
Rev Q does: only 8.30 mm of the 14.70 mm active height falls inside the Perspex
opening at all. Rev Q takes a further 0.65 mm off the top of that.

`Decca_OLED_Display_Bezel_revQ_optical.png` shows this to scale.

> **CAD does not get a vote on whether this is acceptable.** It reports the
> geometry. Whether the intended screen content is still readable through a
> 30.90 × 13.60 mm aperture is settled by the powered test in §10, and by
> nothing else.

---

## 6. Validation results

Two independent tools. Neither check was altered, relaxed or removed.

### 6.1 In Fusion — `validate()` — **46/46 PASS**

| Group | Result |
|---|---|
| Solid integrity | one body, closed solid, **1 shell, 1 lump**, 0 sliver faces < 0.001 mm², 0 sliver edges < 0.005 mm |
| Envelope | 40.00000 × 20.30000 × 4.00000; front face +4.20000; rearmost +0.20000 |
| **Wall continuity, by AREA** | full ring **76.2025 mm²** at z = 0.45, 1.60 and 2.95 — matching the analytic value to four decimals |
| Continuity by region | top **25.1200**, bottom **25.1200**, right **8.9600**, left **8.9600**, corners **8.0425 mm²** — every one exact |
| Wall through the R2.00 corners | corner area **8.0425** vs `π(2.00² − 1.20²) = 8.0425` |
| Outer envelope | exactly 35.4000 × 15.2000 |
| Two-loop wall | 0.800 / 0.40 = **2.0000** loops; corner loop radii **1.800** and **1.400**, no cusp; centrelines exactly **0.4000** apart |
| **Interference present** | **6.3779 mm³** of overlap |
| Interference located | only outboard of the opening wall, \|x\| = 17.7000 vs 17.6000; \|y\| max 6.2245 vs 7.6500; z 0.3000…3.0000 |
| Interference bounded | deepest **0.1000 mm** — exactly the declared value |
| Relief test | with 0.100 mm relief applied, overlap falls to **0.000000 mm³** |
| Behind the Perspex rear face | **0.000000 mm³** |
| OLED glass | 0.000000 mm³; clearance 0.5000 mm |
| **Rev P.5 carrier** | **0.000000 mm³**; minimum distance **0.9394 mm** |
| Optical opening, plug test | a 30.86 × 13.56 plug passes clean through (0.000000 mm³); a 30.94 × 13.64 plug does not |
| Print orientation | wall worst overhang **0.000°**; 0.0000 mm² of >45° overhang outside the bed-adjacent break |

Continuity is proved by **cross-section area**, not by point sampling.
`BRepBody.pointContainment` is not trustworthy on this body: with the tapered
aperture the face wall is a single NURBS surface, and containment then reports
the middle of the open aperture as solid and scattered points inside the wall
as void. Area, taken by boolean intersection with a thin slab, is exact — and
it is the **stronger** proof, because any break, thin spot or gap anywhere in
the ring removes area and an exact match leaves nowhere for one to hide.

### 6.2 Offline from the mesh — `Decca_Display_Bezel_revQ_verify.py` — **42/42 PASS**

Reads only `../STL/Front_Bezel_revQ.stl`, numpy only, exits non-zero on
failure. It re-derives every claim from triangles and compares against figures
typed in by hand from the controlled documents — deliberately *not* imported
from the generator.

```text
1. MESH TOPOLOGY       every edge shared by exactly 2 triangles; consistent
                       winding; ONE connected component; no orphan vertices;
                       NO degenerate triangles (min area 6.297e-04 mm2);
                       volume 605.4639 mm3
2. ENVELOPE            40.0000 x 20.3000 x 4.0000; front +4.2000; rear +0.2000
3. BEHIND THE PERSPEX  lowest z = +0.2000; 0.2000 clear of the rear face;
                       0.5000 clear of the OLED glass
4. WALL SECTIONS       35.4000 x 15.2000 at z = 0.45, 1.60 and 2.95
5. WALL CONTINUITY     720/720 stations x 3 depths, 0 voids
                       left 88/88  right 88/88  top 88/88  bottom 88/88
                       corner 368/368
                       measured wall mean 0.8000  min 0.8000  max 0.8000
                       through the R2.00 corners: 368 stations, 0.8000 flat
5b. TWO-LOOP WALL      exactly 2 x 0.40 loops; corner loop radii 1.80 / 1.40,
                       no cusp; centrelines 0.4000 apart; inner corner R1.20
6. ENVELOPE + FIT      inner 33.8000 x 13.6000; depth 2.8000;
                       INTERFERENCE +0.1000/side; clearance +0.0500/side
7. FACE + OPTICAL      aperture 13.9250 @ z=3.20 and 14.6375 @ z=3.70,
                       extrapolating to 13.6400 at the seating plane and
                       15.3500 at the front face; taper 35.47 deg;
                       face width 30.9000; EFFECTIVE 30.9000 x 13.6000
8. LEAD-IN             tip 35.0020 (expected 35.0000); full section restored
                       by z = +0.400
RESULT: 42/42 PASS
```

### 6.3 Sprung-post and module corridors

Covered rigorously rather than by inspection. A synthetic solid spanning
**everything behind the Perspex rear face** (the full opening footprint and far
beyond, z from −30 to 0) was intersected with the bezel: **0.000000 mm³**.

Every corridor of concern — the four sprung posts and their noses (forward-most
at z = −0.400), the module insertion and removal path, the glass, the PCB and
the carrier itself — lies entirely at z < 0. The bezel's rearmost material is at
z = +0.200 and it does not reach z = 0. It therefore cannot enter any of them,
and this is proved without needing to model any of them individually.

---

## 7. Print orientation and settings

**Orientation: bezel FRONT FACE flat on the bed, wall pointing up. No supports.**

In this orientation:

* the 0.80 mm wall is a **vertical wall** — measured worst overhang across all
  28 wall faces is **0.000°**;
* the wall is printed **last**, standing on the already-solid bezel face, so it
  is supported at its root for its entire 2.80 mm height;
* the 0.20 mm entry lead-in is at the **top** of the print and tapers *inward*,
  so it is self-supporting;
* the 35.47° aperture taper is well inside the 45° threshold;
* bed contact is **251.4 mm²** of flat cosmetic face.

The alternative (rear face down) is wrong: the wall would print first as an
unsupported free-standing ring, and the bezel face would then be a full 90°
overhang over it.

### 7.1 The two-loop wall — this is the whole point of the amendment

`bezel_lip_wall = 0.80 mm` is **exactly two 0.40 mm extrusion loops**. The
first issue's 0.40 mm wall resolved as a single loop, which is what this
amendment exists to fix.

What CAD can prove, and does:

| Property | Value |
|---|---|
| Wall / extrusion width | **0.800 / 0.400 = 2.000 exactly** |
| Measured wall, 720 stations | min **0.8000**, max **0.8000** |
| Measured wall through the corners | 368 stations, **0.8000** flat |
| Outer loop centreline radius at the corner | 2.00 − 0.20 = **1.800** |
| Inner loop centreline radius at the corner | 2.00 − 0.60 = **1.400** |
| Loop centreline separation | **0.400** — one extrusion, everywhere |
| Smallest offset radius | **1.400** — no cusp, no self-intersection |

Because the wall is a constant 0.80 mm offset with an R2.00 outer and R1.20
inner corner, both loop centrelines remain smooth closed curves the whole way
round, and neither collapses or merges at the corners.

> **CAD cannot prove what the slicer does.** It proves the geometry *admits*
> two continuous loops. The production slicer preview is a separate, physical
> gate — see §10 Stage 0b.

| Setting | Value | Why |
|---|---|---|
| Nozzle / extrusion width | **0.40 mm** | the wall *is* two of these |
| Layer height | 0.15–0.20 mm | 14–19 layers up the wall |
| Perimeters | **2** in the wall | not "auto", not variable-width |
| Thin-wall / gap fill | **OFF** if it can be | a full 0.80 mm needs no gap fill; if the slicer inserts any, the setting is wrong |
| Arachne / variable width | **prefer classic** | Arachne may merge 0.80 into one 0.8 mm-wide extrusion — that is a single loop and **fails** the requirement |
| External perimeter speed | ≤ 25 mm/s in the wall | a 2.80 mm tall standing ring |
| Cooling | 100 % over the wall | tiny per-layer loop |
| Material | PETG / PETG-HF, matt or satin **black** | as Rev N |
| Supports | **none** | nothing needs them |
| Bed face | 4+ top/bottom layers or ironing | it is the visible cosmetic face |

> **If your extrusion width is not 0.40 mm**, set `bezel_lip_wall` to **two**
> *actual* extrusion widths and regenerate. Everything downstream —
> `bezel_lip_inner_w/h`, `bezel_lip_inner_r`, the aperture and therefore the
> optical opening — is derived and will follow automatically. The generator
> refuses to build a wall that is not a whole multiple of `extrusion_width`.

---

## 8. Open risks

### 8.1 The interference fit — the primary risk now

The wall went 0.40 → 0.80 mm to get the second loop. **Bending stiffness scales
with thickness cubed, so the wall is about 8× stiffer than the one it
replaces**, and the same 0.10 mm per side of interference is resisted roughly
8× harder.

Brief §3.8 requires the *printed wall* to take the deflection and the original
Perspex to be left unspread and unstressed. At a 0.40 mm wall that split was
obvious. At 0.80 mm it is not, and **no CAD or mesh check in this repository
can settle it.** It is a physical test.

`Bezel_Fit_Gauge_revQ` exists to answer it before a whole bezel is committed:
five loose end-tabs at **0.00 / 0.05 / 0.10 / 0.15 / 0.20 mm** interference per
side, notch-numbered 1…5. Each is the complete right-hand end of the real
Rev Q wall — full 15.20 mm height, both R2.00 corners, the real 0.80 mm
two-loop wall, the real 2.80 mm depth — so it engages the interference exactly
as the bezel will. 1.54 cm³ for all five, about 2 g.

### 8.2 The slicer — the second physical gate

The two-loop requirement is a **production** requirement, not a geometric one.
A single variable-width wall, a missing second loop, gap-fill substitution or
locally merged loops all fail it, and all of them are slicer behaviours that
CAD cannot see. §10 Stage 0b is the check.

### 8.3 The opening corner radius — reduced, but still unmeasured

The corner radius of the real Perspex opening has never been measured and is
recorded nowhere in this project. It could not be recovered from Rev N (§2.3).

**The R2.00 outer corner has largely defused it.** The R2.00 arc pulls the wall
well away from the corner, so the unmeasured corner form no longer decides
whether the part seats — it only decides how much corner is left unmasked:

| assumed `R_panel` | deepest penetration | largest corner gap |
|---:|---:|---:|
| 0.00 | +0.100 | 0.562 |
| 0.50 | +0.100 | 0.562 |
| 1.00 | +0.100 | 0.383 |
| 1.50 | +0.100 | 0.180 |
| 2.00 | +0.100 | 0.050 |
| 2.50 | **+0.250** | 0.050 |

Penetration stays at exactly the declared **0.100 mm** for every opening corner
radius up to **2.050 mm** — the flanks set it, not the corners. Only beyond
that do the corners themselves start to bite harder than declared, which would
trip brief §8's "more interference than declared" stop condition. A routed
opening in a 15.30 mm tall window is very unlikely to carry a corner radius
above 2.05 mm, but it has still never been measured, and the fit gauge tabs
carry the real R2.00 corners so a first offering-up will show it immediately.

### 8.4 Second-order — the 15.20 mm outer height

`bezel_lip_outer_h = 15.20 mm` has never been physically proven, because no
Rev N surface ever touched the top or bottom of the opening (§2.3). It is
15.30 − 2 × 0.05. If the top and bottom of the real opening are not parallel or
not exactly 15.30 mm apart, that is where it will show up first.

---

## 9. Frozen Rev P.5 carrier — hash comparison

Hashes computed **before** any modelling and **again** after all CAD work,
exports and snapshots, for both the first issue and this amendment. **All six
frozen Rev P.5 files match the Rev Q brief §2 exactly. The freeze is intact.**

Reproduce with:

```bash
python mechanical/CAD/Decca_Display_Bezel_revQ_frozen_check.py
```

```text
  [PASS] Decca_Display_Mount_revP.f3d                    matches as as-is
  [PASS] Decca_Display_Mount_revP_fusion.py              matches as CRLF
  [PASS] Decca_Display_Mount_revP_verify.py              matches as CRLF
  [PASS] Rear_Display_Carrier_revP.step                  matches as as-is
  [PASS] Rear_Display_Carrier_revP.stl                   matches as as-is
  [PASS] Decca_Display_Mount_revP_assembly.step          matches as as-is

  RESULT: all 6 frozen Rev P.5 files match the Rev Q brief. FREEZE INTACT.
```

| File | Brief §2 | Before | After | Result |
|---|---|---|---|---|
| `CAD/Decca_Display_Mount_revP.f3d` | `d69bf537…c8e0c8ba` | same | same | **UNCHANGED** |
| `CAD/Decca_Display_Mount_revP_fusion.py` | `719ffd66…273d9656` | same | same | **UNCHANGED** |
| `CAD/Decca_Display_Mount_revP_verify.py` | `7cef57d4…549aa11907` | same | same | **UNCHANGED** |
| `CAD/Rear_Display_Carrier_revP.step` | `1b25a24d…1f05a0c359` | same | same | **UNCHANGED** |
| `STL/Rear_Display_Carrier_revP.stl` | `ec8a4adb…f224e5897` | same | same | **UNCHANGED** |
| `CAD/Decca_Display_Mount_revP_assembly.step` | `e7d9c40d…4173b2d24a` | same | same | **UNCHANGED** |

The released Rev N bezel baseline is likewise untouched:
`Front_Bezel_revN.step` `d15481bc…`, `Front_Bezel_revN.stl` `3547fe10…`,
`Decca_Display_Mount_revN.f3d` `be21762c…`.

Three further independent confirmations:

* `git status` — **no tracked file under `mechanical/` is modified** except the
  Rev Q artefacts themselves;
* `git diff --name-only origin/main HEAD` — **no path containing `revN`,
  `revO` or `revP` appears**;
* comparing blob object ids directly, `origin/main:<file>` and `HEAD:<file>`
  are **identical for all nine** frozen and baseline files.

The Rev P.5 carrier STEP was **read** — imported as a reference body for the
interference checks — and never written. The generator additionally refuses, in
code, to write any path whose basename contains `revN`, `revO` or `revP`.

### 9.1 A line-ending trap worth recording

Two of the six brief values, both `.py` files, do **not** match a plain
`sha256sum` of the bytes on disk in this clone. They match the **CRLF**
rendering of the same content.

This is not a discrepancy in the files, and it is not a defect in the brief.
The brief's table was produced on a Windows checkout, where git's
`core.autocrlf=true` writes text files to the working tree with CRLF endings.
In this clone the two `.py` files happen to sit as LF while the `.step` files
sit as CRLF, so a naive `sha256sum` sweep matches four entries and appears to
fail two.

It is worth recording because **it looks exactly like a frozen file has been
tampered with**, and it briefly did so during this work before being run down.
The content was never in doubt once the blob object ids were compared.

`Decca_Display_Bezel_revQ_frozen_check.py` exists so this cannot mislead anyone
again: it hashes every text file three ways — as-is, forced LF and forced CRLF
— accepts a match on any, and reports which rendering matched. **No change to
the brief is needed.**

---

## 10. Prototype test procedure

Print in **PETG, matt or satin black**, front face down, no supports, per §7.

### Stage 0 — fit gauge first

1. Print `Bezel_Fit_Gauge_revQ` (5 tabs, ≈1.54 cm³, ≈2 g) with the **production
   profile you will use for the bezel**.
2. Offer each tab into the end of the real opening, notch 1 (0.00 mm
   interference) first, working up.
3. Record the largest interference that still seats **fully, by hand, without
   excessive force**, and that releases without marking, spreading or whitening
   the Perspex. Check both ends of the opening — they need not agree.
4. If 0.10 mm does not seat cleanly, set `bezel_lip_interf_x` to what did by
   adjusting `bezel_lip_outer_w`, and regenerate. **Do not force it, and do not
   modify the Perspex.** If nothing at or below 0.10 mm seats without stressing
   the Perspex, **stop and report** — brief §8 first stop condition.

### Stage 0b — slicer preview, before any bezel is printed

5. Slice `Front_Bezel_revQ.stl` with the production profile.
6. Step through **every layer of the wall**, from the first layer above the
   bezel face to the top, and confirm **two continuous 0.40 mm loops** around
   the complete perimeter — both straight runs, both ends, **and all four
   R2.00 corners**.
7. **Reject** the profile if you see any of: a single variable-width wall, a
   missing second loop, gap fill substituted for a loop, or the two loops
   locally merged into one wide extrusion. Fix the slicer — do not thicken
   `bezel_lip_wall` to work around it without recording why.
8. The gauge tabs from Stage 0 carry the same section; slicing one is a quick
   proxy for the same check.

### Stage 1 — dry fit, unpowered, carrier not fitted

9. Offer the bezel to the opening by hand. It must seat with **light, even hand
   pressure** — snug, but not forced. If it needs real force, stop.
10. Confirm the face seats **flush** against the Perspex with no rocking and no
    visible gap on any side.
11. Confirm it lifts out again, and inspect the Perspex for marking, scuffing
    or stress whitening — especially at the four corners and along the two
    interference flanks. Any mark at all is a fail: reduce the interference and
    reprint.
12. Inspect the wall: continuous, opaque, straight and unbroken all the way
    round, with no wave, split or delamination between the two loops. A wavy or
    translucent wall is a **print** failure, not a design failure — revisit §7.1.

### Stage 2 — cut-edge masking, unpowered

13. With the bezel seated, view the opening from directly in front and then
    from oblique angles, left/right and up/down, in good light.
14. Confirm the Perspex cut edge is concealed on all four sides **and at the
    four corners**. Record which corners, if any, show a gap — §8.3 predicts up
    to 0.562 mm against a sharp corner.
15. Photograph it. This is the appearance record the design decision rests on.

### Stage 3 — with the released carrier fitted

16. Fit the **unchanged Rev P.5 carrier** with the original bolts and captive
    nuts. Confirm the bezel remains independent of the bolts and of the carrier
    load path — it must lift out with the carrier still bolted up.
17. Confirm nothing about the carrier's fit, the OLED's insertion or its removal
    has changed. It should not have: the bezel never reaches z = 0.

### Stage 4 — powered

18. Power the OLED with the intended content and photograph the visible active
    area edges.
19. Confirm the required information is still readable through the
    **30.90 × 13.60 mm** aperture. The lit band is **7.450 mm** tall, 0.650 mm
    less than Rev N.
20. Check specifically for anything the wall could have introduced: a new edge
    shadow, a reflection off the inner face of the wall, or light leaking
    between the wall and the Perspex.
21. Run the cabinet lighting through its brightness range with the OLED showing
    black, dim and normal content, and check for light leak around the aperture.

### Acceptance

Rev Q may be considered for release only when 5–21 pass on a real part with the
real Perspex and the released carrier. Until then the revision stays **OPEN**.

If the fit needs adjustment, change only `bezel_lip_outer_w`,
`bezel_lip_outer_h`, `bezel_lip_wall`, `bezel_lip_corner_r` or
`bezel_lip_lead` and reprint. **Do not modify the Perspex, and do not modify
the Rev P.5 carrier, to make the bezel fit.**

---

## 11. Stop conditions — status

The brief's six stop conditions, honestly assessed:

| Condition | Status |
|---|---|
| R2.00 corners or the declared interference cannot seat without damaging or visibly stressing the Perspex | **OPEN — the primary prototype gate.** CAD confirms the geometry is exactly as declared, and that penetration stays at 0.100 mm for any opening corner radius up to 2.05 mm. Whether an 8× stiffer wall takes that deflection instead of the Perspex is a physical question. Fit gauge first. §8.1 |
| Continuous wall needs more than 0.10 mm per horizontal side, or masks unacceptably | **NOT triggered geometrically** — interference is exactly 0.100 mm, bounded and located, and the wall is continuous. Whether the masking is acceptable is deferred to the powered test. |
| Slicer cannot maintain two continuous loops at 0.80 mm | **NOT triggered, but NOT closed.** The geometry is exactly two 0.40 mm loops with no thin spot and no corner cusp. Only the production slicer preview can close it. §10 Stage 0b |
| Wall reduces OLED visibility beyond the accepted presentation | **REPORTED, not judged.** Lit band 8.100 → 7.450 mm, all at the top. A powered-test decision. §5.1 |
| Rev P.5 carrier or its released files would need to change | **NOT triggered.** All six frozen files byte-identical; zero interference with the carrier; 0.939 mm minimum distance. §9 |
| Fusion cannot produce and verify a stable, parametric single solid | **NOT triggered.** One shell, one lump, closed solid, zero slivers; mesh manifold, single-component, no degenerate triangles. Two build obstacles were met and resolved in the open: the window-edge fillet (→ chamfer, §3.4) and a tangency seam of zero-area triangles (→ `ap_root_relief`, §3.4). |

---

## 12. Files

| File | Role |
|---|---|
| `../CAD/Decca_Display_Bezel_revQ_fusion.py` | **the generator — single source of truth for every dimension** |
| `../CAD/Decca_Display_Bezel_revQ_verify.py` | independent offline mesh verification (numpy only) |
| `../CAD/Decca_Display_Bezel_revQ_frozen_check.py` | proves the six frozen Rev P.5 files are unchanged, line-ending-proof |
| `../CAD/Decca_Display_Bezel_revQ.f3d` | editable Fusion source |
| `../CAD/Front_Bezel_revQ.step` | the bezel, neutral format |
| `../STL/Front_Bezel_revQ.stl` | **print this — second** |
| `../CAD/Decca_Display_Bezel_revQ_assembly.step` | bezel + measured Perspex + OLED glass proxy + **unchanged Rev P.5 carrier** |
| `../CAD/Bezel_Fit_Gauge_revQ.step` | interference fit gauge |
| `../STL/Bezel_Fit_Gauge_revQ_GAUGE_I{000,005,010,015,020}.stl` | **print these FIRST** |
| `Decca_OLED_Display_Bezel_revQ_front.png` | front view |
| `Decca_OLED_Display_Bezel_revQ_rear.png` | rear view |
| `Decca_OLED_Display_Bezel_revQ_oblique.png` | oblique |
| `Decca_OLED_Display_Bezel_revQ_lip_oblique.png` | rear three-quarter — the wall as a continuous ring |
| `Decca_OLED_Display_Bezel_revQ_assembly.png` | seated on the measured Perspex |
| `Decca_OLED_Display_Bezel_revQ_section.png` | section on x = 0 |
| `Decca_OLED_Display_Bezel_revQ_section_detail.png` | **the wall masking the Perspex cut edge** |
| `Decca_OLED_Display_Bezel_revQ_optical.png` | the lit area behind the aperture, to scale |

`Front_Bezel_revN.*` remain untouched as the last **released** bezel baseline.
The first issue's `Bezel_Corner_Gauge_revQ.*` files are **deleted**: the corner
radius is now specified at R2.00, so a corner gauge answers a question that is
no longer open, and `Bezel_Fit_Gauge_revQ.*` replaces it with one that is.

### Rebuilding

Inside Fusion (Utilities → Add-Ins → Scripts), point `OUT_DIR` at this clone's
`mechanical` folder and run `main()`, `import_carrier()`, `coupon()`,
`fit_study()`, `validate()`, `export()` and `snapshots()`. `main()` creates its
own new document and never touches the Rev N, Rev O or Rev P files. Then,
offline:

```bash
python mechanical/CAD/Decca_Display_Bezel_revQ_verify.py
python mechanical/CAD/Decca_Display_Bezel_revQ_frozen_check.py
```

---

## 13. Section detail

![Rev Q section detail — the continuous 0.80 mm inset wall inside the Perspex opening, masking the cut edge](Decca_OLED_Display_Bezel_revQ_section_detail.png)

Black is the Rev Q bezel: the face across the top with its R2.00 external
corner, the 35.47° tapered aperture, the recessed adhesive pad in the
underside, and the 0.80 mm inset wall descending into the opening with its
0.20 mm lead-in visible at the tip. Grey is the 3.00 mm Perspex. The wall
covers the cut edge from the seating face down to 0.200 mm short of the rear
face.

![Rev Q optical view — the lit OLED area behind the Rev Q aperture, to scale](Decca_OLED_Display_Bezel_revQ_optical.png)

The lit area to scale behind the aperture. Most of what is hidden above the
window is the **released Rev P.5** condition, not Rev Q; Rev Q's own
contribution is 0.650 mm off the top of the lit band. CAD reports this; only
the powered test can say whether it is acceptable.
