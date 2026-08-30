# Decca OLED Display Bezel — Rev Q Build Report

Status: **OPEN — bezel-only integration prototype. NOT released, NOT for merge.**

Date: 2026-08-30
Controlled requirements: `Decca_OLED_Display_Bezel_CAD_Brief_revQ.md` at commit
`ebfa277eb5ee6ffc8c0e96232f2b6f9663f35aea`
Specification: `Decca_OLED_Display_Mount_Spec_v1.0.md` v1.2, §2 and §4
Carrier: **Rev P.5, RELEASED and FROZEN — unchanged, and proved unchanged (§9)**

> **The first Rev Q print is an integration prototype, not a release part.**
> Its job is to answer one question CAD cannot: what the corner radius of the
> real Perspex opening is, and therefore whether a continuous lip can be made
> to seat. Nothing in this report is a claim about appearance.

---

## 1. What Rev Q changes

One thing. The Rev N pair of side locating rails is deleted and replaced by a
single continuous rearward masking lip around the **complete** inside perimeter
of the Perspex opening — left, right, top, bottom and all four corners.

```text
front
BEZEL FACE
──────────────  seats against the Perspex front face,  z = +3.000
       │
       │  continuous 0.40 mm lip, 2.80 mm rearwards
PERSPEX│
───────┘        lip rear tip,                          z = +0.200
rear
```

The lip is a **masking and locating skirt**. It works on clearance, not
interference. It is not a snap, not a clamp, not a press fit, and it carries no
load. Retention remains removable adhesive on the unchanged recessed pads.

Nothing else changes: the 40.00 × 20.30 × 4.00 envelope, the R2.00 external
corners, the R0.40 front edge break, the 30.40 mm visible window width, the
R0.80 window corners, the seating face and both adhesive pads are all carried
over from Rev N unaltered.

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
| **Locating rails — TWO ONLY** | x 15.300…17.450 and mirror, **y −4.000…+4.000** | R0.600 cylinders at (±15.900/±16.850, ±3.400) |
| Rail depth | z +0.200 … +3.000 = **2.800 mm** | plane pair |
| Rail end relief | **R0.600** | cylindrical surfaces |

Cross-checked against the Rev P build review §16, which independently states
40.00 × 20.30 × 4.00, a 2.80 mm lip depth, rearmost material at z = +0.200 and
0.500 mm clearance to the OLED glass. Both sources agree exactly.

### 2.2 The Z-chain — unchanged from Rev N and Rev P.5

```text
z = +4.200   bezel front face
z = +3.000   Perspex FRONT face  == bezel seating plane
z =  0.000   Perspex REAR face   == DATUM A, carrier hard stop
z = -0.300   OLED glass front face
             lip rear tip at z = +0.200
             -> 0.200 mm clear of the Perspex rear face
             -> 0.500 mm clear of the OLED glass  (the RELEASED value)
```

### 2.3 What the Rev N rails actually proved, and what they did not

This matters and it is the crux of the revision.

* **PROVED:** the 34.90 mm outer envelope **in X**, and the 2.80 mm engagement
  depth. Both rails run at x = ±17.450 and both are 2.80 mm deep.
* **NOT PROVED — the 15.00 mm outer envelope in Y.** The rails span only
  y −4.000…+4.000. They never approach the top or bottom of the opening, so no
  Rev N surface has ever touched the top or bottom of the Perspex. The 15.00 mm
  figure is a nominal target (15.30 − 2 × 0.15), not a fit result.
* **NOT PROVED — anything at all about the corners.** Rev G's note that the
  rail design "tolerates opening corner radii to R3.65" is the giveaway: the
  side-rail architecture was chosen *precisely so that the unknown corner form
  would not matter*. Rev Q is the first bezel geometry in this project that has
  to go into those corners.

### 2.4 Measured fascia geometry — Spec v1.2 §2

| Parameter | Value | Source |
|---|---:|---|
| Display opening | **35.20 × 15.30 mm** | measured, Rev C |
| Perspex thickness | **3.00 mm** | measured |
| Opening corner radius | **NOT RECORDED** | — see §8 |

The released Rev P generator models the opening as a **sharp-cornered box**
(`build_panel` cuts a plain `box`). Rev Q's reference panel does the same, so
the two representations stay identical. That is a modelling convention, not a
measurement, and this report never treats it as one.

---

## 3. Named parameters

Created before any dependent geometry, and mirrored into Fusion user
parameters — the derived ones as real formulas, so the derivation is visible in
the UI. Source of truth is the `P` dict in
`../CAD/Decca_Display_Bezel_revQ_fusion.py`.

### 3.1 Controlling parameters

| Parameter | Value | Class | Note |
|---|---:|---|---|
| `panel_open_w` | 35.20 mm | MEASURED | Rev C |
| `panel_open_h` | 15.30 mm | MEASURED | Rev C |
| `panel_t` | 3.00 mm | MEASURED | |
| `panel_open_corner_r` | 0.00 mm | **UNRESOLVED** | modelled sharp, exactly as the released Rev P reference. Not a measurement. |
| `bezel_w` / `bezel_h` / `bezel_t` | 40.00 / 20.30 / 4.00 mm | PRESERVED | Rev N |
| `bezel_outer_r` | 2.00 mm | PRESERVED | Rev N |
| `bezel_edge_break` | 0.40 mm | PRESERVED | Rev N front fillet |
| `bezel_window_w` | 30.40 mm | PRESERVED | Rev N visible width |
| `bezel_window_r` | 0.80 mm | PRESERVED | Rev N window corner |
| `pad_x_half` / `pad_y0` / `pad_y1` / `pad_depth` | 12.00 / 7.85 / 9.85 / 0.30 mm | PRESERVED | adhesive pads |
| **`bezel_lip_outer_w`** | **34.90 mm** | PROVISIONAL | proven in X by the Rev N rails |
| **`bezel_lip_outer_h`** | **15.00 mm** | PROVISIONAL | **never physically proven** — see §2.3 |
| **`bezel_lip_depth`** | **2.80 mm** | PROVEN | Rev N engagement depth |
| **`bezel_lip_wall`** | **0.40 mm** | PROVISIONAL | one controlled extrusion width |
| **`bezel_lip_corner_r`** | **0.60 mm** | **UNRESOLVED** | Rev N rail-end relief — see §8 |
| **`bezel_lip_lead`** | **0.20 mm** | PROVISIONAL | minimum entry lead-in |

### 3.2 Derived — never entered twice

| Parameter | Formula | Value |
|---|---|---:|
| `bezel_lip_clear_x` | `(panel_open_w − bezel_lip_outer_w) / 2` | **0.150 mm** |
| `bezel_lip_clear_y` | `(panel_open_h − bezel_lip_outer_h) / 2` | **0.150 mm** |
| `bezel_lip_inner_w` | `bezel_lip_outer_w − 2 × bezel_lip_wall` | **34.100 mm** |
| `bezel_lip_inner_h` | `bezel_lip_outer_h − 2 × bezel_lip_wall` | **14.200 mm** |
| `bezel_lip_inner_r` | `bezel_lip_corner_r − bezel_lip_wall` | **0.200 mm** |
| `bezel_window_h` | `bezel_lip_inner_h` | **14.200 mm** |
| `bezel_face_t` | `bezel_t − bezel_lip_depth` | **1.200 mm** |
| `z_panel_front` | `panel_t` | **+3.000 mm** |
| `z_bezel_front` | `z_panel_front + bezel_face_t` | **+4.200 mm** |
| `z_lip_rear` | `z_panel_front − bezel_lip_depth` | **+0.200 mm** |

Two constraints are enforced in code and will refuse to build if violated:

* `bezel_lip_corner_r ≥ bezel_lip_wall` — a uniform wall makes the inner corner
  radius `corner_r − wall`, which cannot go negative. With the 0.40 mm wall the
  smallest buildable outer corner radius is **0.40 mm**.
* no export path may write a file whose name contains `revN`, `revO` or `revP`.

### 3.3 The one deliberate deviation from Rev N — the window height

**Rev N's window was 14.900 mm high. Rev Q's is 14.200 mm, derived from the
lip.** This is deliberate, it is the only Rev N face dimension that changes, and
it costs nothing optically. The reasoning:

The lip inner opening is 14.200 mm. Had the window stayed at 14.900 mm, then at
the top and bottom the lip's 0.400 mm wall would have met the bezel face over
only **0.050 mm** of its width — the face edge at y = ±7.450 against a lip
spanning y = 7.100…7.500. That is a knife-edge root: a sliver in the solid, a
0.05 mm ledge for a 2.80 mm tall standing wall to be printed on, and the obvious
place for the lip to snap off in handling.

Driving the window height from the lip inner opening lands the **full 0.400 mm
wall on solid face material** and makes the lip a true skirt continuing rearward
from the window edge — which is exactly the cross-section the brief draws.

It costs nothing optically because **the clear opening is 14.200 mm either
way**: the lip already controlled the height. All that is removed is a 0.35 mm
ledge of face material that overhung the lip and could never be seen through.
Brief §3.4 requires exactly this — *"the wall and the opening it creates must be
derived, not independently dimensioned."*

The window **width** is untouched at 30.400 mm, because there the lip inner
opening (34.100 mm) is far wider than the window and the Rev N face still
controls.

---

## 4. Exact resulting dimensions

| | mm |
|---|---:|
| Bezel envelope | **40.000 × 20.300 × 4.000** |
| Bezel face thickness | 1.200 |
| External corner radius | R2.000 |
| Front edge break | R0.400 |
| Seating plane (Perspex front) | z = +3.000 |
| Bezel front face | z = +4.200 |
| **Lip outer envelope** | **34.900 × 15.000** |
| **Lip inner envelope** | **34.100 × 14.200** |
| **Lip wall** | **0.400 everywhere** (measured min = max = 0.4000) |
| **Lip depth** | **2.800** (z +3.000 → +0.200) |
| Lip outer corner radius | R0.600 |
| Lip inner corner radius | R0.200 |
| Entry lead-in | 0.200 × 45°, outer rear edge only |
| **Clearance into the opening** | **0.150 per side, all four sides** |
| Rearmost material | z = **+0.200** — 0.200 clear of the Perspex rear face |
| Clearance to OLED glass front face | **0.500** — the released Rev N/P value |
| Minimum distance to the Rev P.5 carrier | **1.171** |
| Visible window | 30.400 × 14.200, R0.800 |
| Solid volume | 0.5243 cm³ (mesh 524.14 mm³) |
| Mass in PETG @ 1.27 g/cm³ | ≈ **0.67 g** |
| Mesh | 4448 triangles, 2224 vertices, closed and manifold |

---

## 5. Optical masking introduced by the lip

**This is the cost of the revision and it must not be glossed over.**

| | Rev N | Rev Q | change |
|---|---:|---:|---:|
| Clear opening width | 30.400 | **30.400** | 0 |
| Clear opening height | 14.900 | **14.200** | **−0.700 total, −0.350 per side** |
| Corner radius | R0.800 | R0.800 | 0 |

The clear height is now controlled by the **top and bottom lip**, not by the
bezel face. That is unavoidable: a continuous lip has to exist at the top and
bottom of the opening, it has to have a wall, and that wall stands inboard of
the opening.

### 5.1 Effect on the powered image

Taking the OLED position from the **released Rev P.5** model — active area
29.42 × 14.70 mm, active centre at y = +6.70 mm after the Rev P.5 +7.00 mm rise:

| | Rev N | Rev Q |
|---|---:|---:|
| Visible active width | 29.420 | **29.420** (unchanged) |
| Visible active height | 8.100 | **7.750** |
| Active height lost to the lip | — | **0.350 mm, all of it at the TOP edge** |
| Unlit board visible below the active area | 6.800 | **6.450** (0.350 mm *less*) |

The bottom edge of the aperture is nowhere near the active area — the active
area's own bottom edge sits at y = −0.650 mm, well inside the aperture — so the
bottom lip costs no active area at all and in fact hides 0.35 mm more of the
unlit board. **The entire optical cost is 0.350 mm off the top of the lit
band.**

For context, the already-released Rev P.5 condition is far larger than anything
Rev Q does: only 8.30 mm of the 14.70 mm active height falls inside the Perspex
opening at all, with about 6.40 mm sitting behind the fascia above it. Rev Q
takes a further 0.35 mm off the top of that.

`Decca_OLED_Display_Bezel_revQ_optical.png` shows this to scale.

> **CAD does not get a vote on whether this is acceptable.** It reports the
> geometry. Whether the intended screen content is still readable through a
> 30.40 × 14.20 mm aperture is settled by the powered test in §10, and by
> nothing else.

---

## 6. Validation results

Two independent tools. Neither check was altered, relaxed or removed.

### 6.1 In Fusion — `validate()` — **30/30 PASS**

| Group | Result |
|---|---|
| Solid integrity | one body, closed solid, **1 shell, 1 lump**, 0 sliver faces < 0.001 mm², 0 sliver edges < 0.005 mm |
| Envelope | 40.00000 × 20.30000 × 4.00000; front face +4.20000; rearmost +0.20000 |
| Lip continuity | material at **1440/1440 perimeter stations × 3 depths**, 0 voids |
| Lip continuity by region | left 203/203, right 203/203, top 493/493, bottom 493/493, **corners 48/48** |
| Lip outer envelope | no material outside 34.90 × 15.00 — 0 breaches |
| Lip wall | min 0.4000, max 0.4000 |
| Lip depth | 2.80000 |
| Clearance | 0.1500 per side in both axes |
| Perspex | interference **0.000000 mm³** |
| Behind the Perspex rear face | **0.000000 mm³** |
| OLED glass | interference 0.000000 mm³; clearance 0.5000 mm |
| **Rev P.5 carrier** | interference **0.000000 mm³**; minimum distance **1.1705 mm** |
| Print orientation | lip worst overhang **0.000°**; 0.0000 mm² of >45° overhang outside the R0.40 bed break |

### 6.2 Offline from the mesh — `Decca_Display_Bezel_revQ_verify.py` — **35/35 PASS**

Reads only `../STL/Front_Bezel_revQ.stl`, numpy only, exits non-zero on
failure. It re-derives every claim from triangles and compares against figures
typed in by hand from the controlled documents — deliberately *not* imported
from the generator.

```text
1. MESH TOPOLOGY          every edge shared by exactly 2 triangles; consistent
                          winding; ONE connected component; no orphan vertices;
                          no degenerate triangles; volume 524.1406 mm3
2. ENVELOPE               40.0000 x 20.3000 x 4.0000; front +4.2000; rear +0.2000
3. BEHIND THE PERSPEX     lowest z = +0.2000; 0.2000 clear of the rear face;
                          0.5000 clear of the OLED glass
4. LIP SECTIONS           34.9000 x 15.0000 at z = 0.45, 1.60 and 2.95
5. LIP CONTINUITY         720/720 stations x 3 depths, 0 voids
                          left 88/88  right 88/88  top 88/88  bottom 88/88
                          corner 368/368
                          measured wall  mean 0.4000  min 0.4000  max 0.4000
6. ENVELOPE + CLEARANCE   inner 34.1000 x 14.2000; depth 2.8000; clear 0.1500/side
7. OPTICAL OPENING        window 30.4000 x 14.2000; EFFECTIVE 30.4000 x 14.2000
8. LEAD-IN                tip 34.5020 (expected 34.5000); full envelope restored
                          by z = +0.400
RESULT: 35/35 PASS
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

**Orientation: bezel FRONT FACE flat on the bed, lip pointing up. No supports.**

This is the whole reason the part is printable. In this orientation:

* the 0.40 mm lip is a **vertical wall** — measured worst overhang across all
  26 lip faces is **0.000°**;
* the lip is printed **last**, standing on the already-solid bezel face, so it
  is supported at its root for its entire 2.80 mm height;
* the 0.20 mm entry lead-in is at the **top** of the print and tapers *inward*,
  so it is self-supporting;
* bed contact area is **295.4 mm²** of flat cosmetic face — good adhesion and
  the best possible finish on the only surface anyone sees.

The alternative (rear face down) is wrong: the lip would print first as an
unsupported free-standing ring, and the bezel face would then be a full 90°
overhang over it.

### 7.1 The single-width wall — this is the critical setting

`bezel_lip_wall = 0.40 mm` is **exactly one extrusion width** for the
established 0.40 mm nozzle configuration, the same convention the released
Rev P.5 carrier uses for its 0.80 mm split posts ("exactly two 0.40 mm
perimeters").

| Setting | Value | Why |
|---|---|---|
| Nozzle / extrusion width | **0.40 mm** | the wall *is* one extrusion |
| Layer height | 0.15–0.20 mm | 14–19 layers up the lip |
| Perimeters | let the slicer lay **one** perimeter in the lip | two will not fit and the slicer will either overlap-and-bulge or drop the wall |
| Thin-wall / gap fill | **ON** (`detect thin walls`, or Arachne/variable-width) | classic slicers can silently delete a 0.40 mm wall |
| External perimeter speed | **≤ 25 mm/s** in the lip | a 2.80 mm tall, 0.40 mm thick standing ring will ring and wobble at speed |
| Cooling | 100 % over the lip | tiny per-layer loop, very short layer time |
| Material | PETG / PETG-HF, matt or satin **black** | as Rev N |
| Supports | **none** | nothing needs them |
| Bed face | 4+ top/bottom layers or ironing | it is the visible cosmetic face |

> **Slice it and look at the preview before printing.** Confirm the lip appears
> as a continuous single-extrusion loop on every one of its layers, all the way
> round including the corners. If the slicer has dropped it, thinned it or
> broken it at the corners, fix the slicer settings — **do not** thicken
> `bezel_lip_wall` to work around it without recording why.

> **If your extrusion width is not 0.40 mm**, set `bezel_lip_wall` to one
> *actual* extrusion width and regenerate. Everything downstream —
> `bezel_lip_inner_w/h`, `bezel_window_h` and therefore the optical opening —
> is derived and will follow automatically. This is the same rule the Rev P.5
> STL README applies to `rear_light_shield_t`.

---

## 8. UNRESOLVED — the physical corner fit

**This is the single open risk of the revision and it cannot be closed in CAD.**

### 8.1 The problem

The corner radius of the real Perspex opening has never been measured and is
recorded nowhere in this project. It could not be recovered from Rev N, because
the Rev N side rails sat at y = ±4.000 and never went near a corner — that
architecture was chosen so the unknown would not matter. Rev Q is the first
bezel that has to enter those corners.

The brief anticipates this: §2 requires the corner form be kept parametric
"because the physical corner radius is not recorded", §3.5 forbids assuming one,
and §4 permits `bezel_lip_corner_r` to be recorded as *unresolved*. It is
recorded as unresolved. **No value has been assumed and no measurement has been
invented.**

### 8.2 The geometry, quantified

Computed by `corner_study()` in the generator, and independently offline. For a
lip outer corner radius `R_lip` inside an opening corner of radius `R_panel`:

| `R_lip` | seats if `R_panel` ≤ | with ≥0.05 mm clear |
|---:|---:|---:|
| 0.40 | 0.912 | 0.791 |
| **0.60** | **1.112** | **0.991** |
| 1.00 | 1.514 | 1.393 |
| 1.60 | 2.112 | 1.991 |
| 2.50 | 3.013 | 2.892 |

The relationship is essentially linear: **`R_panel_max ≈ R_lip + 0.51 mm`**.

Unmasked corner gap on the 45° bisector — how much cut edge stays visible at
each corner (negative = fouls, will not seat):

| `R_lip` \ `R_panel` | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 | 1.50 | 2.00 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.40 | 0.267 | 0.267 | 0.171 | 0.067 | −0.036 | −0.244 | −0.451 |
| **0.60** | **0.326** | **0.326** | **0.254** | **0.150** | **0.046** | −0.161 | −0.368 |
| 1.00 | 0.443 | 0.443 | 0.419 | 0.316 | 0.212 | 0.005 | −0.202 |
| 1.60 | 0.619 | 0.619 | 0.619 | 0.564 | 0.461 | 0.254 | 0.046 |
| 2.50 | 0.882 | 0.882 | 0.882 | 0.882 | 0.833 | 0.626 | 0.419 |

There is a genuine, irreducible trade-off here and no CAD value resolves it:

* **too small an `R_lip`** → the four corners bottom on the Perspex corner
  fillets and the bezel will not seat;
* **too large an `R_lip`** → it seats, but leaves the tabulated gap unmasked at
  each corner, which defeats the point of the revision.

### 8.3 Why 0.60 mm was chosen as the starting value

* It is the **proven Rev N corner relief** — R0.600 is the rail-end radius on
  the only Rev N feature that has ever been inside this opening. The brief asks
  for the proven Rev N relief "where possible", and this is it.
* It masks well: 0.326 mm corner gap against a sharp opening, 0.254 mm against
  an R0.50 opening, versus 0.150 mm on the flats.
* It is comfortably printable at a 0.40 mm wall (inner radius R0.200).
* **Its failure mode is safe, obvious and non-destructive.** If the real corner
  radius exceeds ~1.11 mm the bezel simply stands proud of the fascia. Nothing
  is forced, marked, spread or stressed. You can see it instantly and the fix is
  one parameter and a reprint.

### 8.4 How to close it — the corner gauge coupon

Rather than guess, measure — the method this project already uses for the
Rev P.5 captive-nut pocket (`Hex_Pocket_Fit_Coupon_revP`, "print this FIRST").

`Bezel_Corner_Gauge_revQ` is five loose L-tabs, notch-numbered 1…5, each
carrying a **real section of the Rev Q lip** — same 0.40 mm wall, same 2.80 mm
depth, same 34.90 × 15.00 outer envelope — at R0.40, R0.60, R1.00, R1.60 and
R2.50. Offer each into a corner of the real opening; the smallest that seats
flush is the value to set. Together they cover opening corner radii from 0.91 mm
to 3.01 mm. Total print ≈ 0.59 cm³, a few minutes.

> This coupon is an addition to the brief's file list. It is included because it
> converts the one unresolved unknown into a measurement using the project's own
> established method, and it is cheap. It is not required — the bezel can be
> printed directly and `bezel_lip_corner_r` stepped up if it does not seat.
> Drop it if it is unwanted; nothing else depends on it.

### 8.5 Second-order uncertainty — the 15.00 mm outer height

Separately from the corners: `bezel_lip_outer_h = 15.00 mm` has **never been
physically proven**, because no Rev N surface ever touched the top or bottom of
the opening (§2.3). It is 15.30 − 2 × 0.15, and the 0.15 mm figure is inherited
from the X direction where the rails did prove it. If the opening's measured
height is right, this is sound; if the top and bottom of the real opening are
not parallel or not exactly 15.30 mm apart, the top/bottom lip is where that
will show up first. The prototype tests it.

---

## 9. Frozen Rev P.5 carrier — hash comparison

Hashes computed **before** any modelling and **again** after all CAD work,
exports and snapshots. **All six frozen Rev P.5 files match the Rev Q brief §2
exactly. The freeze is intact.**

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

* `git status` — **no tracked file under `mechanical/` is modified**; every
  Rev Q artefact is a new file;
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
The content was never in doubt once the blob object ids were compared: they are
identical at `origin/main`, at the baseline commit `a7e6073`, at the
requirements commit `ebfa277` and at this commit.

`Decca_Display_Bezel_revQ_frozen_check.py` exists so this cannot mislead anyone
again: it hashes every text file three ways — as-is, forced LF and forced CRLF
— accepts a match on any, and reports which rendering matched. Binary files are
hashed as-is only. **No change to the brief is needed.**

---

## 10. Prototype test procedure

Print in **PETG, matt or satin black**, front face down, no supports, per §7.

### Stage 0 — corner gauge first (recommended)

1. Print `Bezel_Corner_Gauge_revQ` (5 tabs, ≈0.59 cm³).
2. Offer each tab into a corner of the real opening, notch 1 (R0.40) upward.
3. Record the **smallest** radius whose tab seats flush with no rock and no
   corner contact. Try all four corners — they need not agree.
4. Set `bezel_lip_corner_r` to that value and regenerate before printing the
   bezel. If none seats, the opening corner radius exceeds 3.01 mm — **stop and
   report**, because at that point a continuous lip masks nothing useful in the
   corners.

### Stage 1 — dry fit, unpowered, carrier not fitted

5. Offer the bezel to the opening by hand. It must enter under **finger
   pressure only**. If it needs force, stop — do not push.
6. Confirm the face seats **flush** against the Perspex with no rocking and no
   visible gap on any side.
7. Confirm it lifts out again cleanly, and inspect the Perspex for any marking,
   scuffing or stress whitening — especially at the four corners. Any mark at
   all is a fail: raise `bezel_lip_corner_r` and reprint.
8. Inspect the lip itself: it must be continuous, opaque, straight and unbroken
   all the way round. A wavy, translucent or locally missing lip is a **print**
   failure, not a design failure — revisit §7.1 before changing any dimension.

### Stage 2 — cut-edge masking, unpowered

9. With the bezel seated, view the opening from directly in front and then from
   oblique angles, left/right and up/down, in good light.
10. Confirm the Perspex cut edge is concealed on all four sides **and at the
    four corners**. Record which corners, if any, show a gap — §8.2 predicts
    0.326 mm at R_lip 0.60 against a sharp corner.
11. Photograph it. This is the appearance record the design decision rests on.

### Stage 3 — with the released carrier fitted

12. Fit the **unchanged Rev P.5 carrier** with the original bolts and captive
    nuts. Confirm the bezel remains independent of the bolts and of the carrier
    load path — it must lift out with the carrier still bolted up.
13. Confirm nothing about the carrier's fit, the OLED's insertion or its removal
    has changed. It should not have: the bezel never reaches z = 0.

### Stage 4 — powered

14. Power the OLED with the intended content and photograph the visible active
    area edges.
15. Confirm the required information is still readable through the
    **30.40 × 14.20 mm** aperture. The lit band is **7.750 mm** tall, 0.350 mm
    less than Rev N.
16. Check specifically for anything the lip could have introduced: a new edge
    shadow, a reflection off the inner face of the lip, or light leaking between
    the lip and the Perspex.
17. Run the cabinet lighting through its brightness range with the OLED showing
    black, dim and normal content, and check for light leak around the aperture.

### Acceptance

Rev Q may be considered for release only when 5–17 pass on a real part with the
real Perspex and the released carrier. Until then the revision stays **OPEN**.

If the fit needs adjustment, change only `bezel_lip_corner_r`,
`bezel_lip_outer_w`, `bezel_lip_outer_h`, `bezel_lip_wall` or `bezel_lip_lead`
and reprint. **Do not modify the Perspex, and do not modify the Rev P.5 carrier,
to make the bezel fit.**

---

## 11. Stop conditions — status

The brief's five stop conditions, honestly assessed:

| Condition | Status |
|---|---|
| Opening corner form cannot be derived | **PARTIALLY TRIGGERED — declared, not improvised.** It could not be derived. Rather than assume a radius, `bezel_lip_corner_r` is exposed as a named, unresolved parameter with a full tolerance study (§8), the failure mode is safe and visible, and a gauge coupon is provided to measure it. This is what §2, §3.5 and §4 of the brief instruct for exactly this case. **It is the #1 prototype gate.** |
| Continuous lip needs the Perspex or carrier modified | **NOT triggered.** Zero interference with either; 0.150 mm clearance per side; carrier untouched and proved unchanged. |
| Lip cannot be continuous without unacceptable masking | **NOT triggered geometrically** — the lip is continuous and costs 0.350 mm of lit height. **Whether that is acceptable is not a CAD judgement** and is deferred to the powered test (§10 stage 4). |
| Fusion produces unstable or non-manifold geometry | **NOT triggered.** One shell, one lump, closed solid, zero slivers; mesh manifold and single-component. |
| Any frozen Rev P.5 hash changes | **NOT triggered.** All six frozen Rev P.5 files match the brief §2 exactly, and the released Rev N bezel baseline is untouched. Confirmed four ways: the frozen-check script, `git status`, `git diff --name-only origin/main HEAD`, and direct blob-id comparison against `origin/main` (§9). |

---

## 12. Files

New, all of them. Nothing was overwritten.

| File | Role |
|---|---|
| `../CAD/Decca_Display_Bezel_revQ_fusion.py` | **the generator — single source of truth for every dimension** |
| `../CAD/Decca_Display_Bezel_revQ_verify.py` | independent offline mesh verification (numpy only) |
| `../CAD/Decca_Display_Bezel_revQ_frozen_check.py` | proves the six frozen Rev P.5 files are unchanged, line-ending-proof |
| `../CAD/Decca_Display_Bezel_revQ.f3d` | editable Fusion source |
| `../CAD/Front_Bezel_revQ.step` | the bezel, neutral format |
| `../STL/Front_Bezel_revQ.stl` | **print this** |
| `../CAD/Decca_Display_Bezel_revQ_assembly.step` | bezel + measured Perspex + OLED glass proxy + **unchanged Rev P.5 carrier** |
| `../CAD/Bezel_Corner_Gauge_revQ.step` | corner gauge coupon |
| `../STL/Bezel_Corner_Gauge_revQ_COUPON_R{040,060,100,160,250}.stl` | the five gauge tabs |
| `Decca_OLED_Display_Bezel_revQ_front.png` | front view |
| `Decca_OLED_Display_Bezel_revQ_rear.png` | rear view |
| `Decca_OLED_Display_Bezel_revQ_oblique.png` | oblique |
| `Decca_OLED_Display_Bezel_revQ_lip_oblique.png` | rear three-quarter — the lip as a continuous ring |
| `Decca_OLED_Display_Bezel_revQ_assembly.png` | seated on the measured Perspex |
| `Decca_OLED_Display_Bezel_revQ_section.png` | section on x = 0 |
| `Decca_OLED_Display_Bezel_revQ_section_detail.png` | **the lip masking the Perspex cut edge** |
| `Decca_OLED_Display_Bezel_revQ_optical.png` | the lit area behind the aperture, to scale |

`Front_Bezel_revN.*` remain untouched as the last **released** bezel baseline.

### Rebuilding

Inside Fusion (Utilities → Add-Ins → Scripts), point `OUT_DIR` at this clone's
`mechanical` folder and run `main()`, `import_carrier()`, `coupon()`,
`corner_study()`, `validate()`, `export()` and `snapshots()`. `main()` creates
its own new document and never touches the Rev N, Rev O or Rev P files. Then,
offline:

```bash
python mechanical/CAD/Decca_Display_Bezel_revQ_verify.py
```

---

## 13. Section detail

![Rev Q section detail — the continuous lip inside the Perspex opening, masking the cut edge](Decca_OLED_Display_Bezel_revQ_section_detail.png)

Black is the Rev Q bezel: the face across the top, the recessed adhesive pad in
its underside, and the 0.40 mm lip descending into the opening with its 0.20 mm
lead-in visible at the tip. Grey is the 3.00 mm Perspex. The lip covers the cut
edge from the seating face down to 0.200 mm short of the rear face.

![Rev Q optical view — the lit OLED area behind the Rev Q aperture, to scale](Decca_OLED_Display_Bezel_revQ_optical.png)

The lit area to scale behind the aperture. Most of what is hidden above the
window is the **released Rev P.5** condition, not Rev Q; Rev Q's own
contribution is 0.350 mm off the top of the lit band. CAD reports this; only the
powered test can say whether it is acceptable.
