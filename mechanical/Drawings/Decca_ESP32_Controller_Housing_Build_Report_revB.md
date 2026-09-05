# Decca ESP32 Controller Housing — Rev B build report

> **SUPERSEDED BY SPECIFICATION v1.5. DO NOT PRINT THESE PARTS OR COUPONS.**
> The actual DORHEA adapter takes external conductors horizontally through the
> outward-facing screw-terminal ports. Rev B modelled grouped harnesses above
> the terminal blocks, so its cable routing, strain relief, slice evidence and
> verification results do not demonstrate a usable wired enclosure. This file
> is retained only as design history pending a replacement build report.

> **Status: PROTOTYPE CAD. NOT PHYSICALLY VALIDATED.**
> Nothing in this package has been printed, and no dimension in it has been
> measured off the acquired hardware. Every hardware figure is a CAD starting
> value carried forward from Rev A, and every one of them is still an open
> prototype gate. Read §9 before ordering filament.

**Controlling document:** `Decca_ESP32_Controller_Housing_Spec_v1.0.md` — whose
content is now specification revision **v1.5**. The filename is retained
deliberately, to avoid repository clutter and keep existing links working.
**Generator:** `../CAD/Decca_ESP32_Controller_Housing_fusion.py`
**Independent verifier:** `../CAD/Decca_ESP32_Controller_Housing_verify.py`
**Slicer harness:** `../CAD/Decca_ESP32_Controller_Housing_slice.py`
**Date:** 2026-09-02 · **Material:** PETG / PETG-HF · **Method:** FDM, 0.40 mm
nozzle, 0.20 mm layers, **no support material on any part**

> ### RELEASE GATE — the base and the lid may NOT be printed yet
>
> The 24.00 mm assembled electronics height is **assumed**, and it produces a
> closed height of 35.30 mm against a mandatory 36.00 mm — **0.70 mm of
> margin, and neither coupon tests it.** Measure the real assembled stack
> before committing filament to the base or the lid. The approved next
> physical action is printing the two prototype coupons, and nothing else.

---

## 0. What the v1.3 amendment changed, and why

**The cable-tie anchors were too tall and too thin.** As published in v1.2 each
one was a plain slab of the bare 1.60 mm wall thickness, 7.20 mm wide, standing
**14.00 mm above the wall top** and taking its load within 5 mm of its tip. That
is a feature you could snap with a thumb while wiring, and nothing in either
gate suite measured section, because neither suite had been asked to.

Each anchor is now a **buttressed pier**: 8.00 mm of wall carried up from the
print bed, **2.60 mm thick in the cable-pull direction**, with **2.00 mm of
material on every side of the aperture**, blended into the wall top on both
flanks by a generous **R9.00** root radius that leaves a foot 1.52 mm wider each
side at the sill. The unsupported height above that blended foot is **9.00 mm**,
down from 14.00.

| Property | v1.2 | v1.3 | v1.3 §5c requires |
|---|---:|---:|---:|
| Section in the cable-pull direction | 1.60 mm | **2.60 mm** | ≥ 2.40 |
| Width | 7.20 mm | **8.00 mm** | — |
| Material each side of the aperture | 1.60 mm | **2.00 mm** | ≥ 2.00 |
| Material above the aperture apex | 1.60 mm | **2.00 mm** | ≥ 2.00 |
| Root treatment | square butt onto the wall | **R9.00 blend, 5.00 mm tall** | gusset or blended foot |
| Foot half-width at the sill | 3.60 mm | **5.52 mm** | — |
| Unsupported height | 14.00 mm | **9.00 mm** | minimised |
| Root section area | 11.5 mm² | **25.6 mm²** | — |
| Aperture | 4.00 × 2.60, peaked roof | **4.00 × 2.30, peaked roof** | 4.00, support-free |
| Cost | — | **+0.85 cm³, +1.00 g sliced** | within the unchanged limits |

**No pull test was run and none is claimed.** These ties restrain lightweight
low-voltage harnesses; §5c asks for proportionate design judgement, not a
qualified load path. Gates 28–30 measure section, wall, blend and clearance —
geometry — and say so in their own output. No coupon was added for the anchor.

**Where the material went, and why it could not go anywhere else.** The usable
band on this wall is 3.55 mm: from the component keep-out at y 31.50 to the lid's
outer face at y 35.05. Inboard is blocked by the terminal blocks up to z 16.10
and by the assembled-electronics envelope above them — which is also why there
is **no inboard triangular gusset**: below the terminal tops there is 0.50 mm of
space, and above them there is nothing for a gusset to stand on. The only free
direction is outboard, into the anchor's own cable window, where the lid skirt
is cut away. The blend is therefore carried through the 1.60 mm wall band and
the buttress through the window — see §5.

### 0.1 Three consequences the gate suites found, and one design move

Putting material into a cable window has consequences, and all three were found
by the checks rather than by inspection:

| Found by | What it was | What changed |
|---|---|---|
| Gate 7 | An R9.00 blend carried through the **buttress** reached 0.70 mm into H1's harness corridor. | The blend is carried through the 1.60 mm wall band only, inboard of the wall face, where no corridor is defined and the lid can never reach. |
| Gate 17 | The lid is released by tilting its +X end up about the locating hooks and withdrawing in −X, and a tilt leans every lid feature −X in proportion to its height. With the anchor on the **+X** side of its window, the window's side wall walked straight into the buttress — 8.96 mm³ of interference. | **The tie and its bundle swap sides inside each window.** On the −X side the same motion carries the wall *away*. One tie per window, still inside it, still beside its own bundle, deviation still 9.80 mm, every clearance mirrored. The lid now withdraws **2.00 mm** past the buttress against the **0.60 mm** the hooks need. |
| Gate 22 | The buttress is, literally, base material outboard of the base wall — which gate 22 forbade outright. | Gate 22 is **re-scoped and tightened**: it now checks (i) that nothing on the base stands outside the *closed enclosure envelope*, which is the real limit and was never checked before, and (ii) that the only material outboard of the base wall lies inside the four **named** cable-tie buttresses. A rail, an ear or any other projection still fails, anywhere on the part. |

Gate 17 was also corrected while it was open. Its removal test used an
arbitrary 3.00 mm withdrawal; it now uses the withdrawal the hook geometry
actually requires — `hook_engage` + 0.50 = 1.10 mm — and adds a **second
stage** the old test never ran: lift the lid 30 mm clear and confirm zero
interference. Both stages measure 0.000 mm³.

### 0.2 Three repository inconsistencies corrected

1. The §6 gate table quoted the **superseded** cap and countersink figures —
   a 10.20 cap in a 10.40 recess over a 6.40 head. Replaced with the v1.2
   dimensions actually built: a 10.10 cap body with three r0.90 nibs to a
   10.64 crest in a 10.40 recess, over a declared 6.20 mm maximum head.
2. The specification status read "prototype risks closed by amendment", which
   overstated it. It now reads "design-review findings addressed; physical
   prototype gates remain open".
3. `Decca_ESP32_Controller_Housing_slice.py` read `APPDATA` and `TEMP` at
   import and died with an uncaught `KeyError` anywhere but Windows. It now
   reports every missing prerequisite in plain english and exits 2, saying
   explicitly that the full-solid figure is not a slicer estimate.

### 0.3 What the earlier v1.2 amendment changed

Rev B's architecture was approved on review. Five prototype risks were raised
against it, and all five are closed here. Nothing in the approved architecture
moved: the shallow base and deep lid, the absence of rails and ears, the
open-bottom windows, the grouped H1–H6 harnesses, the single ledge and single
clamp, the two internal cabinet fixings, the two screws and two hooks, the
support-free printing and all three mandatory gates are unchanged.

| # | Finding | What was wrong | What changed |
|---|---|---|---|
| 1 | Strain relief misaligned | Anchors at x ±5.00, windows at x ±20.00 — every bundle ran 15 mm inboard to its tie and 15 mm back out. **Worse: the anchor was unusable.** Its aperture opened outboard into the 0.25 mm lid-skirt gap and inboard into the 0.50 mm gap beside the terminal blocks, so no strap could be threaded through it at all. | One anchor per window, **inside that window**, beside its own bundle. Deviation 15.00 → **9.80 mm**. Aperture now opens outboard into the window void and inboard above the terminal blocks. A **real modelled tie** — loop, strap, head, tail, tool access — replaces the placeholder slot, and gate 9 checks the fitted tie. |
| 2 | Caps not retained | 10.20 cap in a 10.40 recess: a 0.10 mm per-side **clearance**, described in the report as a press fit. | Slide-fit 10.10 body with **three r0.90 compliant nibs** to a 10.64 crest — **+0.13 mm measured interference per side** — plus a 2.80 × 1.60 mm pry notch for removal. Measured on the meshes, not asserted. |
| 3 | No screw-head tolerance | One `cab_head_d` of 6.40 that the cone reached only at its top face. | Separate `cab_head_d_nom` 6.00, `cab_head_d_max` **6.20**, `cab_head_angle` 90°, `cab_head_clear_r` **0.25**, plus a 0.10 mm tessellation allowance. Usable recess **measured 6.76 mm** against a 6.70 mm requirement. |
| 4 | Gauge did not test the horizontal insert | One 5.35 cm³ near-full-width gauge testing the carrier interface and the **vertical** insert only. | **Two coupons, 4.69 cm³ together.** Coupon B carries a production-geometry **horizontal** lid-insert boss, a vertical clamp insert, the countersink and the retained cap. |
| 5 | Mass figure was not a slicer estimate | 42.7 g was a full-solid calculation labelled as if it predicted spool use. | Both are now reported and kept separate: **42.4 g full-solid design gate**, **39.69 g real Bambu Studio CLI estimate**. |

Two of these were found by the verifier, not by inspection: gate 9 failed the
moment it was rewritten to model a fitted tie, which is how the unusable
aperture surfaced, and it failed again when the tie loop was found to dip
1.10 mm into the base wall.

---

## 1. Why Rev B exists, and what happened to Rev A

Rev A was rejected on owner review: **105.00 × 77.00 × 38.30 mm and
approximately 68 cm³ of printed material** to hold a board 66 × 63 mm. All
eighteen of its automated gates passed. That is the point worth keeping: a
design can satisfy every check it is given and still be the wrong design,
because the checks were written against features that should not have existed.

Specification v1.1 therefore deletes those features by name, and Rev B does not
rebuild any of them:

| Deleted by v1.1 §2.2 | Rev A cost | Rev B |
|---|---:|---|
| Two external cable-lacing rails, twelve tie slots | ≈8 cm³, +6.8 mm of width | Four buttressed tie piers in the wall plane, **1.40 cm³** and no change to the envelope |
| Four external cabinet mounting ears | +16.00 mm of length | Two recessed fixings **inside** the footprint |
| Sixteen-tooth sawtooth window roofs | design complexity | Open-bottom windows in a lid printed top-face-down |
| USB blanking plug | 0.57 cm³, one part | Deleted; the opening is simply an opening |
| Second full-width PCB clamp | 1.28 cm³, one part | One integral fixed ledge, no part at all |
| Four corner lid screws and their piers | +10.00 mm of length | Two M3 at one end, two locating hooks at the other |
| Thirty per-terminal wire guides | modelled as 30 wires | Six grouped Decca harnesses, four bundles |
| Three extra lid legends | — | One optional `USB / DISCONNECT 5V` |

**Rev A geometry was not the baseline for Rev B.** The base was redesigned from
the vertical chain outwards, not trimmed. Its solid volume falls from 49.66 cm³
to 16.85 cm³, which is not something cosmetic cuts produce.

**What was kept from Rev A**, because it was right and is still right:

- The scope. This holds **only** the 30-pin ESP32 DevKit V1 / DOIT-style board
  and its matching 30-pin screw-terminal breakout. The DAOKAI MOSFET test
  board, the selected DFRobot DFR0457, the WAGO 221-415 connectors, the fuse
  and DC input hardware, the OLED, the WiiM Pro, the Fosi ZA3 and the future
  12 V trigger are all separately mounted, and none of them was brought into
  this enclosure to justify a bigger box.
- **No fastener enters the PCB.** The repository still records no breakout
  mounting-hole pattern, and inventing one is still forbidden.
- Two independent verification tools that do not import each other's numbers.
- The result vocabulary: *mesh-verified*, *prototype-required*,
  *installation-required*. No untested physical fit is recorded as passed.
- The electrical rule, which is a procedure and not a feature: **do not connect
  USB while the shared external 5 V rail is connected.**

---

## 2. Before and after

### 2.1 Envelope

| Metric | Rev A | Rev B | v1.3 §9 limit |
|---|---:|---:|---:|
| Outside length | 105.00 mm | **81.60 mm** | ≤85 |
| Outside width | 77.00 mm | **70.10 mm** | ≤75 |
| Closed height | 38.30 mm | **35.30 mm** | ≤36 |
| Plan area | 8085 mm² | **5720 mm²** | — |
| Base body, walls only | 89.00 × 68.00 mm | **78.70 × 67.20 mm** | — |
| Internal height above the support plane | 28.60 mm | 27.60 mm | — |

Length −22.3%, width −9.0%, height −7.8%, plan area **−29.3%**.

### 2.2 Material

Solid volume as modelled — an upper bound; a part printed at 15–20% infill
weighs less. PETG at 1.27 g/cm³.

| Part | Rev A | Rev B | Preferred |
|---|---:|---:|---:|
| Housing_Base | 49.66 cm³ | **16.85 cm³** | ≤15.00 |
| Housing_Lid | 14.84 cm³ | **16.07 cm³** | ≤18.00 |
| PCB_Clamp_Fixed_End | 1.28 cm³ | *deleted* | — |
| PCB_Clamp_Adjustable | 1.58 cm³ | **1.12 cm³** | ≤2.00 |
| USB_Blanking_Plug | 0.57 cm³ | *deleted* | — |
| Cabinet_Fastener_Cap × 2 | — | **0.16 cm³** | — |
| **Production total** | **67.93 cm³** | **34.20 cm³** | **≤35.00 mandatory** |
| **Full-solid PETG mass** | **86.3 g** | **43.4 g** | **≤45.0 mandatory** |
| Prototype coupons (excluded) | 8.87 cm³ | 4.69 cm³ | — |

**Both mandatory gates pass: 34.20 cm³ against 35.00, and 43.4 g against 45.0.**
Material use is down **49.7%**.

The four buttressed piers cost **+0.85 cm³** against the v1.2 slabs, all of it
in the base, which is why Housing_Base moved from 16.00 to 16.85 cm³. It is
also the whole of the margin lost: 0.80 cm³ and 1.6 g still stand between this
design and the mandatory limits, and neither limit was touched.

### 2.3 The preferred targets are NOT met, and here is the arithmetic

v1.3 §9 also lists preferred targets of ≤30 cm³ and ≤38 g. Rev B misses both,
and misses the ≤15 cm³ preferred base by 1.85 cm³. This is reported rather
than absorbed.

The four shells, at the **thinnest wall v1.3 §8 and §10 permit**, over the
**smallest plan the 66 × 63 mm carrier permits**, before a single boss, pad,
ledge, plinth, tab, clamp or cap is added:

| Shell | Calculation | Volume |
|---|---|---:|
| Base floor | 78.70 × 67.20 × 1.60 | 8.46 cm³ |
| Base walls | (2 × 78.70 × 1.60 + 67.20 × 4.00) × 9.00 | 4.69 cm³ |
| Lid top | 81.60 × 70.10 × 1.60 | 9.15 cm³ |
| Lid skirt | 298.6 × 1.20 × 27.10 | 9.71 cm³ |
| **Irreducible shell** | | **32.01 cm³** |

A 30 cm³ target is therefore **1.99 cm³ below the empty shell**. It cannot be
reached without one of: a floor thinner than the 1.60 mm §4.1 specifies, a
skirt thinner than the 1.20 mm §8.2 specifies, a lid top thinner than the
1.60 mm §7.4 requires over the antenna, or a plan smaller than the carrier.
The per-part preferred targets are also mutually inconsistent with the total:
15 + 18 + 2 = 35 cm³, not 30.

Rev B adds 4.90 cm³ of features to that shell and removes 2.71 cm³ in windows,
the USB slot, vents, bores and recesses, landing at 34.20 cm³.

The v1.2 amendment moved this by −0.25 cm³ net: the taller tie anchors cost
0.35 cm³ and raising the cable windows from 20.00 to 24.00 mm recovered
0.57 cm³, with the thinner cap giving back the rest. **The v1.3 amendment adds
0.85 cm³**, all of it in the four buttressed cable-tie piers, and takes nothing
back — the alternative was leaving a 1.60 mm upright that a thumb could break.
0.80 cm³ and 1.6 g of margin remain against the mandatory limits.

### 2.4 Real slicer evidence

The solid-volume figure above is a **conservative design gate** and stays one.
It is not spool consumption. The complete set was therefore sliced with the
Bambu Studio CLI, driven by `../CAD/Decca_ESP32_Controller_Housing_slice.py`,
against a declared profile: **Bambu Lab P1S, Generic PETG-HF, 0.40 mm nozzle,
0.20 mm layers, 3 perimeters, 15% infill, no supports, textured PEI plate**,
each part in its stated print orientation.

| Part | Qty | Filament, g each | g total | Print time each |
|---|---:|---:|---:|---:|
| Housing_Base | 1 | 19.91 | 19.91 | 1 h 4 m 8 s |
| Housing_Lid | 1 | 19.24 | 19.24 | 1 h 13 m 35 s |
| PCB_Clamp_Adjustable | 1 | 1.16 | 1.16 | 7 m 13 s |
| Cabinet_Fastener_Cap | 2 | 0.19 | 0.38 | 2 m 21 s |
| **Production total** | | | **40.69 g** | **2 h 29 m 38 s** |
| Carrier_Fit_Coupon | 1 | 3.24 | 3.24 | 21 m 32 s |
| Insert_Fastener_Coupon | 1 | 2.31 | 2.31 | 23 m 41 s |
| **Coupon total** | | | **5.55 g** | **45 m 13 s** |

**Support usage: none.** `enable_support = 0` in every slice and the slicer
emitted **zero support features** on all six parts — which is the operational
confirmation of the geometric claim in §6.2. Every slice returned
`return_code 0, "Success."` with no warnings.

Full-solid **43.4 g** against a sliced **40.69 g**: the gap is small because
these are thin-walled shells that are mostly perimeter, so infill saves little.
That is exactly why the solid figure remains the gate.

The buttressed piers cost **+1.00 g and +10 minutes** on the base against the
v1.2 slabs; every other part is unchanged to the gram. Re-sliced from the
regenerated STLs on 2026-09-02 — these are not carried-forward numbers.

**How the CLI had to be driven**, recorded so it is reproducible: `--slice`
needs `--arrange 1` for a bare STL or it reports "input files not found"; the
system presets' `inherits` chains must be flattened, and nothing else about
them rewritten; the P1S takes the **X1C** process presets, which is what its
own machine preset names; and PETG needs `curr_bed_type` declared or the slice
is refused.

### 2.5 The one measurement that would change this

`assembly_above_pcb_h` = **24.00 mm** is a starting value, not a measurement,
and it sets the lid skirt height directly. Every millimetre removed from it
takes 1.00 mm off the closed height and 0.358 cm³ off the lid:

| Assembled height above the carrier | Closed height | Lid | Production total | Mass |
|---:|---:|---:|---:|---:|
| 24.00 (current assumption) | 35.30 mm | 16.07 cm³ | 34.20 cm³ | 43.4 g |
| 22.00 | 33.30 mm | 15.35 cm³ | 33.48 cm³ | 42.5 g |
| 20.00 | 31.30 mm | 14.64 cm³ | 32.77 cm³ | 41.6 g |
| 18.00 | 29.30 mm | 13.92 cm³ | 32.05 cm³ | 40.7 g |

Measure the assembled stack and change one parameter. Nothing else moves.

**This is now a release gate, not an optimisation.** At the assumed height the
closed housing is 35.30 mm against a mandatory 36.00 mm limit. 0.70 mm is the
entire margin, no coupon tests it, and a stack 1 mm taller than assumed breaks
a mandatory gate. §9 lists it as the one gate that blocks printing the base and
the lid. It was **not** changed to chase the preferred 30 cm³ target, which
§2.3 shows is unreachable anyway.

---

## 3. Architecture as built

**Shallow base tray, deep lid.** The base wall is 9.00 mm; the lid skirt is
27.10 mm and carries most of the side protection. That inversion is what pays
for the internal cable-tie tabs and the recessed cabinet fixings: base wall
costs 0.52 cm³ per millimetre of height and lid skirt costs 0.36, so height
belongs in the lid.

**Housing_Base**, printed floor-down. Eight features, each with a stated
purpose and a numbered gate:

| # | Feature | Purpose | Gate |
|---|---|---|---|
| 1 | Continuous 1.60 mm insulating floor | isolates the carrier from the cabinet | 2 |
| 2 | Four local support pads, 9.00 × 2.20 at z 4.50 | carry the board on bare edge only | 3, 13 |
| 3 | One integral fixed ledge, two segments, 2.00 mm grip | retains the −X short edge | 13, 15 |
| 4 | Two clamp plinths with vertical M3 inserts | hard stop for the clamp; retains +X | 13, 14, 15 |
| 5 | Two lid-screw bosses with **horizontal** M3 inserts | lid retention at the +X end | 12, 17 |
| 6 | Two locating rebates in the −X outer face | lid location and capture at the far end | 17 |
| 7 | Four **buttressed cable-tie piers**, one per cable window | grouped-harness strain relief | 9, 9b, 9c |
| 8 | Two recessed, capped cabinet fixings on the centreline | cabinet mounting inside the footprint | 2, 16 |

There is nothing else on the part. Gate 22 measures **0.000 mm³ of base outside
the closed enclosure envelope** and 719.7 mm³ outboard of the base wall, all of
it inside the four named cable-tie buttresses, with 0.004 mm³ unaccounted for.

**The tie anchors, in detail.** Each is a **buttressed pier**: 8.00 mm wide,
**2.60 mm thick in the cable-pull direction**, carried from the print bed to a
cap top at z 23.00, pierced by a 4.00 × 2.30 mm aperture with a 45° peaked roof,
with **2.00 mm of material on every side of that aperture** and an **R9.00**
blend into the wall top on both flanks. Full dimensions are in §5.

Four things about its position are load-bearing, and the first published Rev B
got the first three wrong while the v1.2 amendment introduced the fourth:

- it sits **inside its own cable window**, 9.80 mm from its bundle's centre,
  so no harness detours to the enclosure centre and back;
- its **outboard** face opens into the window void, where the strap, the
  locking head and a finger all have room — not into the 0.25 mm lid-skirt gap;
- its **inboard** face sits 0.60 mm above the terminal-block tops, which is
  the only height on this wall where the inboard side is open at all — not
  into the 0.50 mm gap beside the blocks;
- it sits on the **−X side** of its window, because the lid is withdrawn in −X
  to release its locating hooks and a window side wall that travels toward the
  buttress collides with it. 2.00 mm of withdrawal path against the 0.60 mm the
  hooks need.

The anchor **cannot** be coaxial with its bundle, and that is geometry, not
laziness. A closed slot for a 2.50 mm strap wrapping a Y-running bundle needs
the strap's *width* across the wall — about 4.4 mm once it has usable walls —
and the band between the component keep-out at y 31.50 and the lid's outer face
at y 35.05 is 3.55 mm. 9.80 mm is the minimum the geometry allows, against
15.00 mm before the amendment.

That same 3.55 mm band is why the pier gains its section **outboard**. Inboard
is terminal block up to z 16.10 and assembled-electronics envelope above it;
outboard is the anchor's own cable window, where the lid skirt is cut away.

**Cap retention, in detail.** The cap body is 10.10 mm in a 10.40 mm recess —
a 0.15 mm per-side slide fit, so it enters square and does not shave swarf onto
the screw head — carrying **three r0.90 nibs** to a 10.64 mm crest. Measured on
the exported meshes: **+0.13 mm of interference per side** against a 10.38 mm
bore. The nibs are four and a half extrusion widths across, not a thin
cantilever snap, because a 0.4 mm nozzle cannot print a reliable one. A
2.80 × 1.60 mm pry notch through the recess rim takes a fine blade for service.
After assembly the carrier sits 2.10 mm above the cap, so it is captive
whatever the enclosure's attitude.

**Housing_Lid**, printed **top-face-down**. Six features: 1.60 mm top and
1.20 mm skirt at 4.00 mm overlap and 0.25 mm per face; four open-bottom cable
windows; one open-bottom USB service slot; five 2.00 mm top vent slots; two M3
clearance holes; two locating lugs.

**The open-bottom trick is the whole reason Rev A's sawtooth roofs could go.**
A notch that reaches the skirt's lower free edge, in a lid printed inverted,
only ever *grows* as the print proceeds — it never closes. No roof, no bridge,
no sawtooth, no support. The verifier gates on it directly: **zero
downward-facing facets inside any window or the USB slot.**

**PCB_Clamp_Adjustable**, printed flat so its 3.50 mm cantilever is stressed
along the layers and not across them. A 40.00 × 10.30 × 3.00 mm bar with two
5.40 mm slots giving ±1.00 mm of travel. Its underside is flat at z 6.30 and it
bottoms on the plinths, so tightening the two M3 screws **cannot** drive it
onto the board: the 0.20 mm gap is mechanically guaranteed, not assembly
discipline.

**Cabinet_Fastener_Cap**, print **2 off**. An M3 countersunk head sits flush at
z 1.40 in a local pad; a 10.10 × 1.00 mm cap with three retention nibs presses
into a 10.40 mm recess over it, topping out at z 2.40 — **2.10 mm below the
carrier underside**. A recessed metal head under the board cannot be insulated
by integral geometry, because the head has to be installed after the base is
printed, so v1.2 §4.10 makes this a mandatory production part and it counts in
the material gates.

**The countersink is sized from a declared envelope, not a nominal.** v1.2
§4.10b requires four separate figures, and they are: nominal head 6.00 mm
(ISO 10642 M3, assumed), **maximum head envelope 6.20 mm**, included angle 90°,
**radial clearance 0.25 mm**. That makes the requirement 6.70 mm at the recess
floor. The cone is cut 6.80 mm, because an exported STL renders a cone as a
faceted polygon whose across-flats is smaller than the ideal circle — the
verifier measured 6.64 on a nominal 6.70 before the allowance was added, and
the manufacturing geometry *is* the mesh. Measured after: **6.76 mm**, with
1.30 mm of floor still beneath the countersink. **No compatibility with any
acquired screw is claimed; that remains a prototype gate.**

**The board may be removed with the cabinet screws installed**, and the cabinet
screws may be installed with the board removed — v1.2 §4.11 explicitly allows
the latter, and it is what makes an under-board fixing legitimate.

---

## 4. Derived dimensions

### 4.1 Height chain, all above the cavity floor

```
-1.60  base underside                        floor 1.60
 0.00  cavity floor
 2.00  lowest solder / pin feature           2.00 clear above the floor
 4.50  carrier underside, support pad top    2.50 below-carrier protrusion
 5.00  lid skirt lower free edge             4.00 overlap on a 9.00 wall
 6.10  carrier top face                      carrier 1.60
 6.30  fixed ledge and clamp underside       0.20 retention clearance
 9.00  base wall top, cable-window sill
16.10  terminal block top                    block 10.00 above the carrier
20.00  cable window top                      11.00 clear above the sill
30.10  tallest assembled component           24.00 above the carrier
32.10  cavity ceiling, lid underside         2.00 headroom
33.70  lid outer face                        lid 1.60
```

Closed height **35.30 mm**.

### 4.2 Length chain

| x | What sets it |
|---:|---|
| −35.40 | base outer face, −X |
| −33.00 | carrier fixed edge and wall inner face — end wall **2.40 mm** |
| −31.00 | fixed ledge tip — 2.00 mm grip into a 3.00 mm bare short edge |
| +32.00 / +33.00 / +34.00 | carrier free edge at 65.00 / 66.00 / 67.00 |
| +34.50 | clamp plinth inner face — 0.50 mm clearance at the 67.00 worst case |
| +38.10 | clamp insert axis — 1.60 boss wall + 2.00 hole radius |
| +41.30 | clamp bar outer edge — 2.70 half-slot + 0.50 edge |
| +41.70 | +X wall inner face — 0.40 bar clearance, and 1.60 boss wall, which land on the same plane |
| +43.30 | base outer face, +X — wall 1.60 |

Base body **78.70 mm**; the lid adds 0.25 + 1.20 at each end → **81.60 mm**.

The −X end wall is 2.40 mm rather than 1.60 because it carries both the
integral ledge and both hook rebates, and an 0.80 mm rebate in a 1.60 mm wall
leaves 0.80 mm of skin. It costs 0.48 cm³ and 0.80 mm of length, and it is the
only part of the base thicker than 1.60 mm other than the four bosses.

### 4.3 Width chain

±31.50 carrier edge → ±32.00 cavity (0.50) → ±33.60 base outer (1.60) →
±33.85 skirt inner (0.25) → ±35.05 lid outer (1.20). Base **67.20 mm**, lid
**70.10 mm**.

### 4.4 Internal cavity corners are SQUARE

`cav_corner_r` is 0.00, not 1.40. A filleted internal corner eats 1.35 mm³ out
of the corner of a square-routed carrier, and the first Rev B build failed gate
5 on exactly that. If the acquired board turns out to have radiused corners it
only gains clearance.

---

## 5. Harness routing — six grouped harnesses, not thirty wires

Modelled from `docs/Wiring.md`, not invented. Bundle diameter is
1.15 × 2.00 × √n for n round conductors hexagonally packed and pulled together
by a tie.

| Window | Harnesses | Cond. | Bundle Ø | Bundle x | Its tie at x |
|---|---|---:|---:|---:|---:|
| −Y, centre −20 | H1 potentiometers, 4 × 3 | 12 | 7.97 mm | −15.20 | −25.00 |
| −Y, centre +20 | H2 on/off + H3 VHF and Stereo/Mono | 6 | 5.63 mm | +24.80 | +15.00 |
| +Y, centre −20 | H4 OLED + H5 dial-lighting control | 7 | 6.09 mm | −15.20 | −25.00 |
| +Y, centre +20 | H6 ZA3 trigger + 5 V/GND from the WAGO star points | 4 | 4.60 mm | +24.80 | +15.00 |

Four windows, **22.00 mm wide**, sill at z 9.00, top at z 24.00. Each bundle's
own corridor is gated clear for the full 10.00 mm requirement.

**Each anchor sits on the −X side of its window and its bundle on the +X side,
and that is not arbitrary.** The lid is released by tilting its +X end up about
the locating hooks and withdrawing in −X, which leans every lid feature −X in
proportion to its height. The anchor's buttress projects into the window, so a
window side wall that travels toward it collides with it; a window side wall
that travels away from it does not. On the −X side the lid withdraws **2.00 mm**
past the buttress against the **0.60 mm** the hooks need. Gate 17 found this by
failing, with the anchor on the other side.

**Strain relief — one tie per window, aligned with its own bundle.** Each long
side carries two anchors, one for each of its windows, and each sits inside the
window it serves. **Bundle-to-tie lateral deviation: 9.80 mm**, against 15.00 mm
before the amendment, when the anchors were at x ±5.00 and the windows at
x ±20.00 and every bundle had to run to the enclosure centre and back.

The **fitted tie** is now modelled, not assumed — strap, loop, locking head,
cut tail and tool volume — and gate 9 checks the route a fitter actually has to
take:

1. feed the tail inboard-to-outboard through the anchor aperture, which is
   open at the strap's real 2.50 × 1.10 mm cross-section right through the
   wall;
2. up the outboard face inside the window void;
3. across to the bundle at the top of the loop;
4. round the bundle — the loop passes **under** it, clearing the wall top by
   0.30 mm, which is what sets the bundle's ride height. Sizing that height
   from the bundle alone put the loop 1.10 mm inside the wall, and gate 9
   caught it;
5. back to the locking head, which sits inboard above the terminal blocks with
   an 11.00 mm tool and finger volume gated clear;
6. cut the tail, with 14.00 mm of clearance.

Pull on the cable loads the strap, the strap loads the anchor, the anchor is a
local raise of the wall itself, and the wall loads the floor and the two
cabinet screws. **The load never reaches a terminal.**

### The anchor itself — a buttressed pier, not an upright

| | |
|---|---|
| Pier | 8.00 mm wide × **2.60 mm** thick in the cable-pull direction, carried from the print bed (z −1.60) to the cap top (z 23.00) |
| Buttress | the outboard 1.00 mm of that section, projecting into the anchor's own cable window, y 33.60 → **34.60**, 0.45 mm inside the lid's outer face |
| Aperture | 4.00 mm wide × 2.30 mm high at z 16.70–19.00, 0.60 mm above the terminal tops, 2.60 mm deep through the pier, **2.00 mm of leg each side**, 45° peaked roof to an apex at 21.00 and **2.00 mm of cap** above it |
| Root blend | one **R9.00** arc per flank, tangent to the pier face at z 14.00 and running out to the wall top at z 9.00 — a 5.00 mm tall blend leaving a foot **1.52 mm wider each side** |
| Unsupported height | **9.00 mm** above the blended foot (v1.2: 14.00 mm above the wall top) |
| Root section | **25.6 mm²** against v1.2's 11.5 mm² |
| Clearances | 0.45 mm to the lid's outer face, 1.00 mm to the window head, 0.48 mm from the foot to the window side wall, **2.00 mm of lid withdrawal path** |

**The blend lives in the 1.60 mm wall band, not in the buttress**, and that is a
measured consequence rather than a preference: carried through the buttress it
reached 0.70 mm into H1's harness corridor (gate 7) and left only 0.48 mm of the
lid's withdrawal path (gate 17). Inboard of the wall face neither of those
exists, so that is where the blend goes.

**There is no inboard triangular gusset, and there cannot be one.** Below the
terminal tops at z 16.10 the space between the cavity wall and the terminal
blocks is 0.50 mm; above them there is nothing for a gusset to stand on. §5c
offers a blended foot as the alternative, and the blended foot is what the
geometry admits.

**No pull test.** Gates 28–30 measure section, aperture walls, blend and
clearance. They do not measure strength, they do not claim to, and the anchor's
robustness in a fitter's hands is recorded in §9.3 as a prototype gate.

Building the anchors *in the wall plane* rather than as inward brackets is what
makes them nearly free: the carrier fills the tray to within 0.50 mm and there
is no internal plan space to give them. Rev A solved the same problem with
external rails that cost 6.8 mm of width and about 8 cm³.

**All 30 terminal screws remain reachable with the lid removed** — thirty
Ø6.00 mm corridors from z 16.10 upward, zero obstructed by the base or the
clamp.

---

## 6. Verification

Two independent suites, run on different things. The in-CAD suite works on the
BRep solids by boolean intersection and point containment; the offline suite
reads **only** the exported STLs and re-derives every claim from triangles,
against values typed in by hand from the controlling documents. Neither imports
the other's numbers.

```
27 CAD checks,  0 failed, 15 prototype gates open
27 mesh checks, 0 failed, 16 prototype, 3 installation
```

Twenty-seven checks cover all thirty v1.3 §13 gates; each label cites the
specification gate it answers.

| v1.3 §13 gate | Result | Measurement |
|---|---|---|
| 1 manifold, watertight production meshes | MESH-VERIFIED | 4 meshes: 0 bad edges, 0 bad windings, 1 component each |
| 2 continuous insulating floor | MESH-VERIFIED | 1485 probes, 0 gaps; 2 capped bores, a **10.10 mm cap body with three r0.90 nibs to a 10.64 crest** in a 10.40 mm recess, over a declared **6.20 mm maximum head** in a 6.80 mm countersink. *(This row previously quoted the superseded 10.20 / 10.40 / 6.40 figures.)* |
| 3 underside clearance ≥ 2.00 | MESH-VERIFIED | base stops at z 0.00 under all four joint rows; tallest off-pad feature z 2.40, carrier at 4.50 → 2.10 clear |
| 4 lid top clearance ≥ 2.00 | MESH-VERIFIED | ceiling z 32.10 over a 30.10 component top |
| 5 no electronics keep-out entered | MESH-VERIFIED | 8744 probes over 3 keep-outs × 4 parts, 0 intrusions |
| 6 terminal screwdriver access | MESH-VERIFIED | 30 Ø6.00 corridors, 0 obstructed |
| 7 cable window ≥ 10.00 usable | MESH-VERIFIED | 4 windows 22.00 mm wide; every bundle corridor clear for the full 10.00 mm; 608 probes meet anchor buttress inside the full-width prisms and **0 of them fall outside the four named buttresses** |
| 8 no harness pinched by the lid | MESH-VERIFIED | 4 bundles, 29 conductors, largest Ø7.97, 0 pinch probes |
| 9 internal strain relief works | MESH-VERIFIED | 4/4 apertures pass a 2.50 × 1.10 strap right through the 2.60 mm pier; 4/4 open inboard above the 16.10 terminal tops; 4/4 open outboard into their own window; 4/4 loops pass under their bundle clear of the 9.00 sill; 0 obstructed tool probes |
| 28–30 anchor section, aperture walls, blended foot | MESH+CAD-VERIFIED | **2.60 mm** of section in the cable-pull direction against ≥2.40; **2.00 mm** of leg each side of a 4.00 mm aperture and **2.00 mm** above its apex, against ≥2.00 — the mesh probe reads the leg as 1.99 mm, which is representation tolerance, not thickness (see below); 8/8 blend probes on an R9.00 root radius 5.00 mm tall; unsupported height 9.00 (v1.2: 14.00); 0 probes foul the board edge; lid withdrawal 2.00 mm against the 0.60 the hooks need. **Geometry only — not a strength claim.** |
| 10 USB envelope clear | MESH-VERIFIED | measured slot 14.75 × 17.45 against a 14.00 × 9.00 minimum |
| 11 antenna keep-out clean | MESH-VERIFIED | 0 intrusions; nearest metal 2.35 mm outside; lid skin 1.60 mm; 0 vents inside |
| 12 lid overlap and fit | MESH-VERIFIED | 62 perimeter probes, gap 0.247 mm mean (0.198–0.257); overlap 4.00 |
| 24 tie aligned with its own window | MESH-VERIFIED | 4 ties, 4 windows, 1:1; bundle-to-tie deviation 9.80 mm, both inside a 22.00 mm window |
| 25 caps positively retained | MESH-VERIFIED | 3 nibs to a 10.64 crest in a 10.38 bore = **+0.130 mm interference per side**; 10.10 body = 0.140 slide fit; pry notch found on 15 of 180 rim probes |
| 26 countersink vs max head envelope | MESH-VERIFIED | usable recess 6.76 mm against a 6.70 mm requirement (6.20 max head + 2 × 0.25); 1.30 mm of floor beneath |
| 27 coupons cover the untested interfaces | MESH-VERIFIED | A 2.66 + B 2.03 = 4.69 cm³ against the 5.35 cm³ gauge they replace; horizontal insert bore present and bottomed at 5.00 mm |
| 13 contact on bare edge only | MESH-VERIFIED | ledge overhang 1.95 (1.20 flat + 0.75 lead-in), clamp grip 2.00, both into a 3.00 bare edge |
| 14 65.00–67.00 mm accommodated | MESH-VERIFIED | measured slot 5.38 long, travel ±0.99, grip 2.00 at all three lengths |
| 15 retention loads nothing | MESH-VERIFIED | ledge underside z 6.32, clamp underside z 6.30, carrier top 6.10 |
| 16 cabinet heads recessed and insulated | MESH-VERIFIED | see gate 26; head z 1.40, cap to 2.40, carrier at 4.50 |
| 17 valid two-screw / two-hook sequence | MESH+CAD-VERIFIED | 2/2 rebates, 2/2 lugs engaging 0.60 mm, 2/2 screw holes; lid lifts 0.20 mm then meets the capture ledge; **two stages** now — tilt 12°, withdraw the 1.10 mm the hook geometry requires, then lift 30 mm clear — **0.000 mm³ over both** |
| 18 no slicer support required | MESH-VERIFIED | max unsupported reach 1.00 mm (mesh) / 1.25 mm (CAD) against a 1.50 limit; 0 downward facets in any window or the USB slot |
| 19 envelope ≤ 85 × 75 × 36 | MESH-VERIFIED | 81.60 × 70.10 × 35.30; 0 stray outboard features |
| 20 volume ≤ 35.00 cm³ | MESH-VERIFIED | 34.20 cm³ |
| 21 mass ≤ 45.0 g | MESH-VERIFIED | 43.4 g full-solid; 40.69 g sliced |
| 22 no forbidden Rev A feature | MESH+CAD-VERIFIED | 0 deleted meshes on disk; plan area 5720 mm² against 8085; **0.000 mm³ of base outside the closed enclosure envelope**; 719.7 mm³ outboard of the base wall, all of it inside the four named cable-tie buttresses (0.004 mm³ unaccounted) |

**The aperture leg is 2.00 mm, and the mesh probe reads 1.99.** The CAD
nominal is **2.00 mm** — `tie_tab_half_w` 4.00 less half of a 4.00 mm aperture,
exactly, in the parametric model and in the STEP. The offline verifier marches
that leg in 0.01 mm steps across a triangulated surface and reports **1.99 mm**.
That difference is **tessellation and probe resolution — representation
tolerance in the measurement, not material missing from the part.** It is not a
request for thicker geometry and no geometry was added for it. Gate 9c's
`TIE_AP_WALL_MIN - 0.10` allowance exists precisely to absorb it, and it is
retained unchanged; §6.3 records the same effect on the countersink, where the
faceting was large enough to matter and the *cut* was compensated instead.

### 6.1 What verification caught in the v1.3 amendment

Every one of these is a design change the checks forced, not a threshold that
was moved to make a number fit.

- **The blend fouled a harness corridor.** Carried through the buttress, the
  R9.00 flank reached 0.70 mm into H1's corridor. Gate 7 measures the corridor
  outboard of the wall face, so the blend was moved inboard of it, into the
  1.60 mm wall band, where it costs nothing and reaches nothing.
- **The lid could not be taken off.** Gate 17 found 8.96 mm³ of interference:
  tilting the lid leans its window side walls −X in proportion to height, and
  the anchor was on the side those walls travel toward. The tie and its bundle
  now swap sides inside each window. That is the single largest design move in
  this amendment and it came from a failing check, not from a drawing.
- **Gate 17 was measuring the wrong thing anyway.** It withdrew the lid an
  arbitrary 3.00 mm and stopped. It now withdraws exactly what the hooks
  require and then lifts the lid 30 mm clear — a stage that had never been run.
- **Gate 22 forbade the fix outright**, because it forbade *all* base material
  outboard of the base wall. Rather than relax it, it was split: nothing may
  stand outside the closed enclosure envelope (new, and stricter), and the only
  material outboard of the base wall must lie inside the four **named**
  buttresses. Both are checked in both suites.
- **A probe-count typo in gate 9c itself** — 16 expected where the loops
  produce 8 — failed the gate on its first run and was corrected in the gate,
  not in the design.

### 6.2 What verification caught in the v1.2 amendment

- **The tie anchor could not be threaded, and nothing had noticed.** The
  published Rev B gate checked that an aperture and a tab existed. Rewriting it
  to model a *fitted* tie failed immediately: the aperture's outboard face
  opened into the 0.25 mm lid-skirt gap and its inboard face into the 0.50 mm
  gap beside the terminal blocks. Neither will take a 1.10 mm strap. The
  anchor moved into its window and up above the terminal tops.
- **The tie loop dipped 1.10 mm into the base wall.** With the anchor fixed,
  gate 9 failed again: the bundle's ride height had been sized from the bundle
  alone, so its loop fouled the wall it was tied to. The bundle height is now
  derived from the *loop* — sill + loop outer radius + 0.30 mm.
- **A "press fit" that was a clearance fit.** Gate 25 was written to measure
  the cap's own crest against the base's own bore. On the published geometry it
  would have returned −0.10 mm. It now returns +0.130 mm.
- **The countersink measured 6.64 on a nominal 6.70.** An exported cone is a
  faceted polygon and its across-flats is smaller than the ideal circle. The
  manufacturing geometry is the mesh, so the cone is now cut 0.10 mm oversize
  and measures 6.76.
- **Three verifier bugs of its own**, all found by the two suites disagreeing:
  the recess-bore probe took `max()` over angles and so measured the pry notch
  instead of the bore; the countersink was probed 0.04 mm below the seat and
  read 0.06 low; and a `box_pts` call was missing an argument.

### 6.3 What verification caught in the original Rev B build

Recorded because these are real design changes, not tuning. The offline
verifier failed **five** gates on the first complete Rev B build, and the CAD
suite failed two before that. Every one was a defect, not a threshold problem.

- **The chamfer cutter was mis-centred, and then it was non-manifold.** The
  first `chamfer_y` offset the diamond from the corner instead of centring it
  on it, so the ledge lead-in removed a lens of material rather than a 45°
  wedge — the CAD suite reported a 0.50 mm overhang reach while the mesh
  measured 2.00 mm. Centring the diamond fixed the cut and produced the
  documented Rev A failure mode instead: **eight tangency sites, eight
  non-manifold edges**, because a diamond centred on a corner has vertices
  lying exactly on both faces meeting there. The fix is geometric — the
  chamfer is now made by *intersecting* the segment with a large box whose face
  **is** the chamfer plane, which has no vertex anywhere near the part. The
  hook rebate chamfer was deleted outright: 0.80 mm of unsupported step is
  nothing, and removing it both cleared two tangency sites and doubled the
  hook's vertical capture.
- **A filleted internal cavity corner ate into the carrier.** R1.40 at the
  cavity corners put 1.35 mm³ of base inside the rectangular carrier envelope.
  Internal corners are now square.
- **The assembly-height keep-out was modelled wrongly**, covering the full
  carrier including the bare short-edge margins — so it reported the fixed
  ledge and the clamp lip as intrusions when both are *required* to be there.
  It now stops at the bare margins, bounded by the **shortest** carrier in the
  65–67 mm window so it stays valid across the whole clamp range.
- **The underside-joint model had to be refined, and that is itself a new
  prototype gate.** Rev A modelled the solder-joint envelope as one 58 × 52 mm
  blanket slab covering everything inboard of the bare margins. That slab makes
  an under-board cabinet fixing geometrically impossible, which is exactly why
  Rev A put its mounting features on external ears. v1.2 §4.8 requires the
  fixings inside the footprint, so the envelope is now modelled where joints
  actually are — two rows under the terminal blocks, two under the ESP32 socket
  headers — leaving the strip between the header rows clear. **Confirm before
  printing that the acquired breakout carries nothing on its underside within
  y ±9.83 mm at x ±27.00 mm.** This is listed in §9.
- **Three verifier bugs, found by disagreement with the CAD suite.** The clamp
  slot scan ran off the end of the bar and read open air as slot travel
  (±2.65 mm instead of ±1.00). The countersink was measured part-way down the
  cone and compared against the head diameter at the top. The underside-clearance
  scan counted the support pads — which are *supposed* to touch the carrier — as
  clearance violations. All three were fixed in the verifier, not the part.
- **The 06 section render showed the outside of a half, not the cut face.** The
  section is cut on y = 0 and viewed from +Y; the earlier camera looked along
  the wrong axis and produced a blank grey rectangle.

### 6.4 One design rule this build states for itself

v1.2 §10 forbids **support material**. It sets no numeric limit on a short
unsupported overhang, and a ledge that retains a board over its edge cannot be
built without one. This build therefore declares its own rule and gates on it:

> **`OVERHANG_REACH_MAX = 1.50 mm.`** Every downward-facing surface on every
> production part, in its stated print orientation, is probed for how far it
> reaches from something holding it up — not its bounding-box size, which
> cannot tell a cantilever from a two-sided bridge. Cable windows and the USB
> slot are held to a stricter rule: no downward-facing facet at all.

Measured worst case: **1.00 mm** (mesh) / 1.25 mm (CAD) on the base's fixed
ledge, whose 1.20 mm flat is cut down from 2.00 mm by the 0.80 mm lead-in
chamfer. The lid measures 0.75 mm, the clamp and the cap 0.00. The slicer
agrees operationally: **zero support features generated on any of the six
parts.**

### 6.5 One capability removed

The Rev A verifier had a `--drawings` mode that plotted two dimensioned views
from the exported triangles. It is **not** carried forward. The plots described
Rev A's ears, lacing rails and sawtooth roofs and would need a complete rewrite;
v1.2 §12 does not ask for dimensioned drawings; and every number they carried
is now printed by the verifier itself as a measured value with its tolerance.
The matplotlib dependency goes with it — the verifier now needs only numpy.

---

## 7. Files

### Editable and exchange

| File | Bytes |
|---|---:|
| `../CAD/Decca_ESP32_Controller_Housing.f3d` | ~833 kB |
| `../CAD/Decca_ESP32_Controller_Housing_assembly.step` | ~1.25 MB |
| `../CAD/ESP32_Controller_Housing_Base.step` | ~162 kB |
| `../CAD/ESP32_Controller_Housing_Lid.step` | ~836 kB |
| `../CAD/ESP32_Controller_PCB_Clamp_Adjustable.step` | ~25 kB |
| `../CAD/ESP32_Controller_Cabinet_Fastener_Cap.step` | ~23 kB |
| `../CAD/ESP32_Controller_Carrier_Fit_Coupon.step` | ~59 kB |
| `../CAD/ESP32_Controller_Insert_Fastener_Coupon.step` | ~36 kB |

### Print files

`../STL/ESP32_Controller_Housing_Base.stl`,
`..._Housing_Lid.stl`, `..._PCB_Clamp_Adjustable.stl`,
`..._Cabinet_Fastener_Cap.stl` (**print 2 off**),
`..._Carrier_Fit_Coupon.stl`, `..._Insert_Fastener_Coupon.stl`.

### Removed as obsolete or superseded

Rev A: `../STL/ESP32_Controller_PCB_Clamp_Fixed.stl`,
`../STL/ESP32_Controller_USB_Plug.stl`,
`../CAD/ESP32_Controller_PCB_Clamps.step` (a two-clamp exchange file for a
design that now has one clamp), all sixteen `..._revA_*.png` renders, and the
Rev A build report.

Superseded Rev B: `../STL/ESP32_Controller_Carrier_Fit_Gauge.stl` and
`../CAD/ESP32_Controller_Carrier_Fit_Gauge.step` — one near-full-width gauge
replaced by two coupons that test more for less filament. The verifier fails if
any of them reappears on disk. Also removed:
`Decca_ESP32_Controller_Housing_revB_09e_anchor_detail_outboard.png`, the first
cut of the v1.3 anchor close-up, replaced by `09d` and `09e` above — `images()`
deletes it on every run so it cannot be mistaken for current evidence.

Their substantive findings are carried forward in §0, §1 and §6 of this
document; git history retains the originals.

### Component tree

```
Decca_ESP32_Controller_Housing
├── REF_ESP32_DevKit_V1_30Pin      NON-MANUFACTURING REFERENCE
├── REF_30Pin_Terminal_Adapter     NON-MANUFACTURING REFERENCE
├── REF_Wired_Keepouts             NON-MANUFACTURING REFERENCE
├── Housing_Base                   production
├── Housing_Lid                    production
├── PCB_Clamp_Adjustable           production
├── Cabinet_Fastener_Caps          production, print 2 off
├── Carrier_Fit_Coupon             PROTOTYPE TOOL, excluded from §9
└── Insert_Fastener_Coupon         PROTOTYPE TOOL, excluded from §9
```

No reference body appears in any STL. 272 named Fusion user parameters.

### Review evidence

Twenty-three images, `Decca_ESP32_Controller_Housing_revB_01..17_*.png`, all
regenerated from the model by `images()`; none is posed by hand.

The v1.3 amendment adds two close-ups of the revised anchor, and **neither
contains a tool-clearance block or any other keep-out that would obscure it**:

- `09d_anchor_detail` — the pier, its outboard buttress, the R9.00 blend into
  the wall top, the aperture with its 45° peaked roof, and the cap. Base
  geometry only, nothing translucent, nothing orange.
- `09e_anchor_and_tie` — the same anchor in elevation with its tie fitted:
  strap through the aperture, loop closed on the bundle, locking head.

The earlier v1.2 amendment adds `09b_tie_alignment` (each harness from its terminals through its
aligned tie to its own window), `09c_tie_heads_and_tool` (locking heads and the
tightening pull), `11b_cabinet_fixing_section` (screw, countersink, retained cap
and carrier clearance in section), `15_coupon_a_carrier`,
`16_coupon_b_inserts` and `17_insert_test_features`. Keep-out
volumes render as translucent yellow and acquired hardware as green, so a
reader can tell manufacturing geometry from a dimensional assumption without
opening the browser.

---

## 8. Printing and assembly

| Part | Orientation | Filament | Time | Notes |
|---|---|---:|---:|---|
| Housing_Base | **floor down** | 19.91 g | 1 h 4 m 8 s | worst unsupported reach 1.00 mm, at the fixed ledge; the four cable-tie piers rise straight off the bed and need nothing under them |
| Housing_Lid | **top face down** | 19.24 g | 1 h 13 m 35 s | this is what makes the windows and USB slot roofless |
| PCB_Clamp_Adjustable | flat, as modelled | 1.16 g | 7 m 13 s | loaded section across the layers |
| Cabinet_Fastener_Cap | flat, **2 off** | 0.19 g ea | 2 m 21 s ea | the three nibs print as part of the rim |
| Carrier_Fit_Coupon | plate down | 3.24 g | 21 m 32 s | prototype tool |
| Insert_Fastener_Coupon | plate down | 2.31 g | 23 m 41 s | prototype tool |

Filament and time are the Bambu Studio CLI's own figures for the declared
profile in §2.4, not estimates. **Zero support features on every part.**

PETG or PETG-HF, 0.40 mm nozzle, 0.20 mm layers. **Three perimeters** on the
lid skirt (1.20 mm = 3 × 0.40); four only locally at the four bosses and the
two hook features. 15–20% infill. **No support material on any part.** Deburr
the cable windows and the USB slot before assembly.

### The approved next physical action: the two coupons, and nothing else

**5.55 g and 45 minutes for both.** The base and the lid must not be printed
until the release gate at the top of this report is closed.

**`ESP32_Controller_Carrier_Fit_Coupon.stl`** — 3.24 g, 21 m 32 s. Reproduces
at 1:1 the −X end wall, the real fixed ledge with its 0.80 mm lead-in, the
4.50 mm support height on four production-pattern pads, the clamp plinth with
its **vertical** insert, and three read-off steps at 65.00 / 66.00 / 67.00 mm
standing *below* the carrier plane so they never obstruct it. Slide the
acquired breakout in under the ledge and read which step its free edge lands
on. That settles `adapter_pcb_l`, `adapter_pcb_t`, `pad_h` and the 0.20 mm
retention gap against the real board.

**`ESP32_Controller_Insert_Fastener_Coupon.stl`** — 2.31 g, 23 m 41 s. Carries
one **horizontal** lid-screw boss at production geometry, one vertical clamp
insert, the cabinet countersink and the cap recess with its pry notch. The
horizontal insert is the point of it: a heat-set insert driven into a bore in a
wall printed on its side is the one fastener in this design whose feasibility
nobody has demonstrated, and 2.31 g is a cheap place to find out. Print two
caps alongside it, 0.19 g each, and check the press and release.

Together they cost **less filament than the single Rev B gauge they replace**
(5.55 g against that gauge's 6.8 g) and test three interfaces it never touched.

### Assembly

1. Heat-set four M3 inserts: two vertical in the clamp plinths, two
   **horizontal** in the +X lid-screw bosses.
2. With the board out, fit the two cabinet screws through the floor into the
   cabinet and press an insulating cap into each recess.
3. Slide the carrier in under the fixed ledge, −X first, onto the four pads.
4. Fit `PCB_Clamp_Adjustable`, slide until its lip sits on the bare +X edge,
   two M3 through the slots. ±1.00 mm of travel is available. The bar bottoms
   on the plinths; it cannot be tightened onto the board.
5. Wire the terminals. Route each grouped harness along the wall to its tie
   tab, tie it, then out through the window. **The tie takes the pull, not the
   terminal.**
6. Plug the ESP32 into its sockets.
7. Tilt the lid, engage both locating lugs in the −X rebates, lower the +X end,
   and fit two M3 × 8.

Removal is the reverse. Two service cases are short and both are gated: the
ESP32 comes out with only the lid removed, and the clamp comes off with the lid
off and every wire still connected.

---

## 9. Prototype gates — every one of these is still open

**Nothing below is verified. Nothing below may be treated as verified until the
acquired hardware is measured or the part is printed and offered up.**

### 9.1 Hardware dimensions that are CAD starting values

`adapter_pcb_l` 66.00 · `adapter_pcb_w` 63.00 · `adapter_pcb_t` 1.60 ·
`adapter_below_h` 2.50 · `assembly_above_pcb_h` 24.00 · `carrier_len_min`
65.00 · `carrier_len_max` 67.00 · `pcb_bare_edge` 3.00 · `pcb_bare_perim`
2.50 · `term_per_side` 15 · `term_pitch` 3.50 · `term_block_w` 8.00 ·
`term_block_h` 10.00 · `term_screw_inset` 4.00 · `term_screw_d` 2.60 ·
`term_wire_z` 4.00 · `esp_pcb_l` 51.50 · `esp_pcb_w` 28.30 · `esp_pcb_t` 1.60 ·
`esp_header_h` 8.50 · `esp_header_span` 22.86 · `esp_off_x` 0.00 · `esp_off_y`
0.00 · `esp_mod_l` 25.50 · `esp_mod_w` 18.00 · `esp_mod_h` 3.10 · `esp_ant_l`
15.00 · `esp_ant_w` 18.00 · `esp_usb_w` 7.50 · `esp_usb_l` 5.90 · `esp_usb_h`
2.70 · `insert_hole_d` 4.00 · `insert_depth` 5.00 · `cab_head_d_nom` 6.00 ·
`cab_head_d_max` 6.20.

Three matter most in the short term:

- **The exact heat-set insert is still not recorded anywhere in the
  repository.** 4.00 mm × 5.00 mm is a common M3 short insert and it is a
  guess. Record the real part before printing the base, or the two lid screws
  and two clamp screws have nowhere to live.
- **`assembly_above_pcb_h` 24.00** is worth 1.00 mm of height and 0.358 cm³
  per millimetre. See §2.5. **It is now a release gate: measure it before
  printing the base or the lid.** At the assumed value the closed housing is
  35.30 mm against a mandatory 36.00, so a stack 1 mm taller than assumed
  breaks a mandatory gate and neither coupon would catch it.
- **The acquired cabinet screw's head has never been measured.** 6.20 mm is a
  declared maximum envelope built on an ISO 10642 assumption. The countersink
  swallows it with 0.28 mm of measured radial margin, but no compatibility with
  a real screw is claimed.

### 9.2 New in Rev B, and load-bearing

- **Nothing on the carrier underside within y ±9.83 mm at x ±27.00 mm.** The
  refined four-row joint model in §6.1 is what allows the cabinet fixings to
  sit under the board. If the real breakout has anything there, the fixings
  move or the design goes back to external mounting.
- **EN and BOOT positions remain unmeasured**, so v1.2 §6.4 forbids access
  holes and none is cut. The removable lid is the prototype access route, and
  the lid carries no EN or BOOT legend, because marking a hole that does not
  exist is worse than not marking it.
- **H1–H6 conductor counts** in §5 are read from `docs/Wiring.md`, but real
  bundle diameters depend on the insulation and ferrules actually used. The
  bundle diameter sets the tie loop, and the loop sets the bundle's ride
  height, so a materially fatter bundle moves geometry.
- **The cable tie itself.** 2.50 × 1.10 mm strap with a 4.60 mm head is a
  standard small nylon tie and a starting value. Offer a real one up to the
  coupon before committing.
- **A horizontal heat-set insert has never been driven** into a wall printed on
  its side. Coupon B exists for this.
- **The cap's press and release force** on this printer and filament. 0.12 mm
  of radial interference on three r0.90 nibs is a design value, not a measured
  force.
- **The cable-tie anchor's robustness in a fitter's hands.** Gates 28–30
  measure 2.60 mm of section in the cable-pull direction, 8.00 mm of width,
  2.00 mm of material all round the aperture and an R9.00 root blend. That is
  section, not strength. **No pull test, no load test and no anchor coupon is
  required, none was run, and none is claimed** — these ties restrain
  lightweight low-voltage harnesses, and §5c asks only for a feature that is
  not snapped during wiring or normal handling. The acceptance step is the
  ordinary one: fit a real tie, thread it, tighten and crop it normally, and
  confirm the anchor is intact afterwards.

### 9.3 Physical behaviour nothing geometric can settle

- the carrier-fit coupon accepts the real breakout without stress or
  excessive play;
- the carrier sits flat on the four pads and slides under the ledge without
  forcing;
- the clamp retains it without bowing it;
- the ESP32 comes out of and goes back into its sockets with the lid off;
- every used terminal is reachable with the owner's actual screwdriver;
- the grouped H1–H6 harnesses route through the windows and the tie piers
  without pinch or sharp bends;
- a real cable tie fits and threads through the anchor, tightens and crops
  normally with ordinary tools, with the lid off;
- the anchor is intact after ordinary wiring and handling;
- the harness is restrained without loading the terminal connections;
- lid assembly does not disturb the wiring, and the two hooks locate it without
  being stressed;
- the lid comes off past the four buttresses without catching on one;
- the insulating cap presses in, stays in with the base held vertically, and
  comes out again with a fine blade;
- a USB cable with its moulded shroud inserts and removes cleanly;
- cabinet fastener installation and cap insulation are practical in the real
  cabinet;
- antenna performance is acceptable with the lid fitted;
- PETG print quality is acceptable with no support on any part;
- no abnormal temperature after at least 30 minutes powered.

### 9.4 Installation-required

Cabinet fixing centres and the surface behind them; final harness routing and
which two tie positions per side are actually used; the OTA link with the lid
fitted; the shake and handling test.

---

## 10. Reconciliation with specification v1.3

| § | Requirement | State |
|---|---|---|
| 2.1 | production parts plus two prototype coupons | as built |
| 2.2 | eight forbidden features | none present; gate 22 |
| 3 | reference geometry and clearances | met; all still prototype gates |
| 4 | base: floor, pads, ledge, clamp, cabinet fixings | met and gated |
| 4.10a | **positive cap retention** | met; +0.130 mm measured interference, gate 25 |
| 4.10b | **countersink from a declared max head envelope** | met; 6.76 measured against 6.70 required, gate 26 |
| 5 | grouped harnesses, open-bottom windows, internal ties | met and gated |
| 5, 5a, 5b | **one tie per window, real tie geometry, fitted-tie check** | met; 9.80 mm deviation, gates 9 and 24 |
| 5c | **anchor section, aperture walls, blended foot, root radii** | met; 2.60 / 2.00 / 2.00 mm on an R9.00 blend, gates 28–30. No inboard gusset: the reason is in §5 |
| 6 | USB opening, no plug, no EN/BOOT holes | met |
| 7 | ventilation and antenna | met; 5 top slots, none inside the keep-out |
| 8 | lid retention: 2 screws + 2 hooks, 4.00 overlap | met and gated |
| 9.1 | envelope and material gates | **mandatory limits met**; preferred targets NOT met — see §2.3 |
| 9.2 | **slicer evidence** | met; Bambu Studio CLI, §2.4 |
| 9.3 | **height release gate** | OPEN, and it blocks printing the base and lid |
| 10 | FDM rules | met; the one self-declared rule is stated in §6.3 |
| 11 | CAD component structure | as specified |
| 12 | deliverables | all present; obsolete and superseded artefacts removed |
| 13 | thirty verification gates | all pass, in two independent tools |
| 14 | prototype acceptance gates | all open, listed in §9 |
| 15 | change control | one item raised, in §2.3 |

---

## 11. After the first fit test

Record the measured values here, change the matching parameters, re-run
`main()`, `validate()`, `export()`, `images()` and the offline verifier, and
raise the revision. The measured values then supersede the starting values
everywhere, including in the specification.

| Parameter | Starting | Measured | Date |
|---|---:|---|---|
| `adapter_pcb_l` | 66.00 | | |
| `adapter_pcb_w` | 63.00 | | |
| `adapter_pcb_t` | 1.60 | | |
| `adapter_below_h` | 2.50 | | |
| `assembly_above_pcb_h` | 24.00 | | |
| `pcb_bare_edge` / `pcb_bare_perim` | 3.00 / 2.50 | | |
| `term_pitch` / `term_block_h` | 3.50 / 10.00 | | |
| `esp_header_h` | 8.50 | | |
| `insert_hole_d` / `insert_depth` | 4.00 / 5.00 | | |
| `lid_fit_clear` | 0.25 | | |
| underside clear strip at x ±27.00 | assumed clear | | |
| `cab_head_d_max` (real screw head) | 6.20 | | |
| `tie_w` / `tie_t` (real tie) | 2.50 / 1.10 | | |
| `cab_nib_int` (press/release felt) | 0.12 | | |
| horizontal insert drives into coupon B | assumed yes | | |

**The housing is not physically validated and must not be described as such
until a printed part has been tested against the acquired hardware.**
