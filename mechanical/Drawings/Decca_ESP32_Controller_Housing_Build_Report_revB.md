# Decca ESP32 Controller Housing — Rev B build report

> **Status: PROTOTYPE CAD. NOT PHYSICALLY VALIDATED.**
> Nothing in this package has been printed, and no dimension in it has been
> measured off the acquired hardware. Every hardware figure is a CAD starting
> value carried forward from Rev A, and every one of them is still an open
> prototype gate. Read §9 before ordering filament.

**Controlling document:** `Decca_ESP32_Controller_Housing_Spec_v1.0.md` — whose
content is specification revision **v1.1**. The filename is retained
deliberately, to avoid repository clutter and keep existing links working.
**Generator:** `../CAD/Decca_ESP32_Controller_Housing_fusion.py`
**Independent verifier:** `../CAD/Decca_ESP32_Controller_Housing_verify.py`
**Date:** 2026-09-01 · **Material:** PETG / PETG-HF · **Method:** FDM, 0.40 mm
nozzle, 0.20 mm layers, **no support material on any part**

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
| Two external cable-lacing rails, twelve tie slots | ≈8 cm³, +6.8 mm of width | Four internal tie tabs formed **in the wall plane**, 0.20 cm³ |
| Four external cabinet mounting ears | +16.00 mm of length | Two recessed fixings **inside** the footprint |
| Sixteen-tooth sawtooth window roofs | design complexity | Open-bottom windows in a lid printed top-face-down |
| USB blanking plug | 0.57 cm³, one part | Deleted; the opening is simply an opening |
| Second full-width PCB clamp | 1.28 cm³, one part | One integral fixed ledge, no part at all |
| Four corner lid screws and their piers | +10.00 mm of length | Two M3 at one end, two locating hooks at the other |
| Thirty per-terminal wire guides | modelled as 30 wires | Six grouped Decca harnesses, four bundles |
| Three extra lid legends | — | One optional `USB / DISCONNECT 5V` |

**Rev A geometry was not the baseline for Rev B.** The base was redesigned from
the vertical chain outwards, not trimmed. Its solid volume falls from 49.66 cm³
to 15.65 cm³, which is not something cosmetic cuts produce.

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

| Metric | Rev A | Rev B | v1.1 §9 limit |
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
| Housing_Base | 49.66 cm³ | **15.65 cm³** | ≤15.00 |
| Housing_Lid | 14.84 cm³ | **16.64 cm³** | ≤18.00 |
| PCB_Clamp_Fixed_End | 1.28 cm³ | *deleted* | — |
| PCB_Clamp_Adjustable | 1.58 cm³ | **1.12 cm³** | ≤2.00 |
| USB_Blanking_Plug | 0.57 cm³ | *deleted* | — |
| Cabinet_Fastener_Cap × 2 | — | **0.19 cm³** | — |
| **Production total** | **67.93 cm³** | **33.60 cm³** | **≤35.00 mandatory** |
| **Estimated PETG mass** | **86.3 g** | **42.7 g** | **≤45.0 mandatory** |
| Carrier_Fit_Gauge (excluded) | 8.87 cm³ | 5.35 cm³ | — |

**Both mandatory gates pass: 33.60 cm³ against 35.00, and 42.7 g against 45.0.**
Material use is down **50.5%**.

### 2.3 The preferred targets are NOT met, and here is the arithmetic

v1.1 §9 also lists preferred targets of ≤30 cm³ and ≤38 g. Rev B misses both,
and misses the ≤15 cm³ preferred base by 0.65 cm³. This is reported rather
than absorbed.

The four shells, at the **thinnest wall v1.1 §8 and §10 permit**, over the
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

Rev B adds 3.61 cm³ of features to that shell and removes 2.02 cm³ in windows,
the USB slot, vents and bores, landing at 33.60 cm³.

### 2.4 The one measurement that would change this

`assembly_above_pcb_h` = **24.00 mm** is a starting value, not a measurement,
and it sets the lid skirt height directly. Every millimetre removed from it
takes 1.00 mm off the closed height and 0.358 cm³ off the lid:

| Assembled height above the carrier | Closed height | Lid | Production total | Mass |
|---:|---:|---:|---:|---:|
| 24.00 (current assumption) | 35.30 mm | 16.64 cm³ | 33.60 cm³ | 42.7 g |
| 22.00 | 33.30 mm | 15.92 cm³ | 32.88 cm³ | 41.8 g |
| 20.00 | 31.30 mm | 15.21 cm³ | 32.17 cm³ | 40.9 g |
| 18.00 | 29.30 mm | 14.49 cm³ | 31.45 cm³ | 39.9 g |

Measure the assembled stack and change one parameter. Nothing else moves.

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
| 7 | Four cable-tie tabs, two per long side, **in the wall plane** | grouped-harness strain relief | 9 |
| 8 | Two recessed, capped cabinet fixings on the centreline | cabinet mounting inside the footprint | 2, 16 |

There is nothing else on the part. Gate 22 measures 0.004 mm³ of base outside
its own rounded-rectangle envelope — there are no projections at all.

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
z 1.20 in a local pad; a 10.20 × 1.20 mm cap presses into a 10.40 mm recess
over it, topping out at z 2.40 — **2.10 mm below the carrier underside**. A
recessed metal head under the board cannot be insulated by integral geometry,
because the head has to be installed after the base is printed, so v1.1 §4.10
makes this a mandatory production part and it counts in the material gates.

**The board may be removed with the cabinet screws installed**, and the cabinet
screws may be installed with the board removed — v1.1 §4.11 explicitly allows
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

| Window | Harnesses | Conductors | Bundle Ø | Fits an 11.00 × 20.00 window |
|---|---|---:|---:|---|
| −Y, x −20 | H1 potentiometers, 4 × 3 | 12 | 7.97 mm | yes |
| −Y, x +20 | H2 on/off + H3 VHF and Stereo/Mono | 6 | 5.63 mm | yes |
| +Y, x −20 | H4 OLED + H5 dial-lighting control | 7 | 6.09 mm | yes |
| +Y, x +20 | H6 ZA3 trigger + 5 V/GND from the WAGO star points | 4 | 4.60 mm | yes |

Four windows, 20.00 mm wide, sill at z 9.00, top at z 20.00 — **11.00 mm of
usable height against a 10.00 mm requirement**, gated by sweeping a full-width
10.00 mm prism through each and requiring zero obstruction.

**Strain relief.** Each long side carries two tie tabs at x ±5.00. The tab is a
local extension of the wall itself from z 9.00 to 15.50, pierced by a
5.00 × 2.40 mm aperture with a 45° peaked roof so it prints with no bridge. A
tie passes through the aperture, wraps the bundle and cinches: pull on the
cable loads the tab, the tab loads the wall, the wall loads the floor and the
two cabinet screws. **The load never reaches a terminal.**

Building the anchors *in the wall plane* rather than as inward brackets is what
makes them free: the carrier fills the tray to within 0.50 mm and there is no
internal plan space to give them. Rev A solved the same problem with external
rails that cost 6.8 mm of width and about 8 cm³.

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
23 CAD gates,  0 failed, 10 prototype gates open
22 mesh gates, 0 failed, 11 prototype, 3 installation
```

| v1.1 §13 gate | Result | Measurement |
|---|---|---|
| 1 manifold, watertight production meshes | MESH-VERIFIED | 4 meshes: 0 bad edges, 0 bad windings, 1 component each |
| 2 continuous insulating floor | MESH-VERIFIED | 1485 probes, 0 gaps; 2 capped bores, cap 10.20 in a 10.40 recess over a 6.40 head |
| 3 underside clearance ≥ 2.00 | MESH-VERIFIED | base stops at z 0.00 under all four joint rows; tallest off-pad feature z 2.40, carrier at 4.50 → 2.10 clear |
| 4 lid top clearance ≥ 2.00 | MESH-VERIFIED | ceiling z 32.10 over a 30.10 component top |
| 5 no electronics keep-out entered | MESH-VERIFIED | 8744 probes over 3 keep-outs × 4 parts, 0 intrusions |
| 6 terminal screwdriver access | MESH-VERIFIED | 30 Ø6.00 corridors, 0 obstructed |
| 7 cable window ≥ 10.00 usable | MESH-VERIFIED | 4 windows, 11.00 mm clear, 0 obstructed probes |
| 8 no harness pinched by the lid | MESH-VERIFIED | 4 bundles, 29 conductors, largest Ø7.97, 0 pinch probes |
| 9 internal strain relief works | MESH-VERIFIED | 4/4 apertures open through the wall, 4/4 tabs solid |
| 10 USB envelope clear | MESH-VERIFIED | measured slot 14.75 × 17.45 against a 14.00 × 9.00 minimum |
| 11 antenna keep-out clean | MESH-VERIFIED | 0 intrusions; nearest metal 2.35 mm outside; lid skin 1.60 mm; 0 vents inside |
| 12 lid overlap and fit | MESH-VERIFIED | 62 perimeter probes, gap 0.247 mm mean (0.198–0.257); overlap 4.00 |
| 13 contact on bare edge only | MESH-VERIFIED | ledge overhang 1.95 (1.20 flat + 0.75 lead-in), clamp grip 2.00, both into a 3.00 bare edge |
| 14 65.00–67.00 mm accommodated | MESH-VERIFIED | measured slot 5.38 long, travel ±0.99, grip 2.00 at all three lengths |
| 15 retention loads nothing | MESH-VERIFIED | ledge underside z 6.32, clamp underside z 6.30, carrier top 6.10 |
| 16 cabinet heads recessed and insulated | MESH-VERIFIED | measured countersink 6.20 for a 6.40 head; head z 1.20, cap to 2.40, carrier at 4.50 |
| 17 valid two-screw / two-hook sequence | MESH+CAD-VERIFIED | 2/2 rebates, 2/2 lugs engaging 0.60 mm, 2/2 screw holes; lid lifts 0.20 mm then meets the capture ledge; a 12° tilt-and-withdraw clears with 0.000 mm³ of interference |
| 18 no slicer support required | MESH-VERIFIED | max unsupported reach 1.00 mm (mesh) / 1.25 mm (CAD) against a 1.50 limit; 0 downward facets in any window or the USB slot |
| 19 envelope ≤ 85 × 75 × 36 | MESH-VERIFIED | 81.60 × 70.10 × 35.30; 0 stray outboard features |
| 20 volume ≤ 35.00 cm³ | MESH-VERIFIED | 33.60 cm³ |
| 21 mass ≤ 45.0 g | MESH-VERIFIED | 42.7 g |
| 22 no forbidden Rev A feature | MESH-VERIFIED | 0 deleted meshes on disk; plan area 5720 mm² against 8085 |

### 6.1 What verification caught, and what changed as a result

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
  Rev A put its mounting features on external ears. v1.1 §4.8 requires the
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

### 6.2 One design rule this build states for itself

v1.1 §10 forbids **support material**. It sets no numeric limit on a short
unsupported overhang, and a ledge that retains a board over its edge cannot be
built without one. This build therefore declares its own rule and gates on it:

> **`OVERHANG_REACH_MAX = 1.50 mm.`** Every downward-facing surface on every
> production part, in its stated print orientation, is probed for how far it
> reaches from something holding it up — not its bounding-box size, which
> cannot tell a cantilever from a two-sided bridge. Cable windows and the USB
> slot are held to a stricter rule: no downward-facing facet at all.

Measured worst case: **1.00 mm** (mesh) on the base's fixed ledge, whose
1.20 mm flat is cut down from 2.00 mm by the 0.80 mm lead-in chamfer. The lid,
the clamp and the cap measure 0.25 mm, 0.00 and 0.00.

### 6.3 One capability removed

The Rev A verifier had a `--drawings` mode that plotted two dimensioned views
from the exported triangles. It is **not** carried forward. The plots described
Rev A's ears, lacing rails and sawtooth roofs and would need a complete rewrite;
v1.1 §12 does not ask for dimensioned drawings; and every number they carried
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
| `../CAD/ESP32_Controller_Carrier_Fit_Gauge.step` | ~48 kB |

### Print files

`../STL/ESP32_Controller_Housing_Base.stl`,
`..._Housing_Lid.stl`, `..._PCB_Clamp_Adjustable.stl`,
`..._Cabinet_Fastener_Cap.stl` (**print 2 off**),
`..._Carrier_Fit_Gauge.stl`.

### Removed as obsolete Rev A production artefacts

`../STL/ESP32_Controller_PCB_Clamp_Fixed.stl`,
`../STL/ESP32_Controller_USB_Plug.stl`,
`../CAD/ESP32_Controller_PCB_Clamps.step` (a two-clamp exchange file for a
design that now has one clamp), all sixteen `..._revA_*.png` renders, and the
Rev A build report. Their substantive findings are carried forward in §1 and
§6.1 of this document; git history retains the originals.

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
└── Carrier_Fit_Gauge              PROTOTYPE TOOL, excluded from §9
```

No reference body appears in any STL. 236 named Fusion user parameters.

### Review evidence

Sixteen images, `Decca_ESP32_Controller_Housing_revB_01..15_*.png`, all
regenerated from the model by `images()`; none is posed by hand. Keep-out
volumes render as translucent yellow and acquired hardware as green, so a
reader can tell manufacturing geometry from a dimensional assumption without
opening the browser.

---

## 8. Printing and assembly

| Part | Orientation | Notes |
|---|---|---|
| Housing_Base | **floor down** | worst unsupported reach 1.00 mm, at the fixed ledge |
| Housing_Lid | **top face down** | this is what makes the windows and USB slot roofless |
| PCB_Clamp_Adjustable | flat, as modelled | loaded section across the layers |
| Cabinet_Fastener_Cap | flat | **2 off** |
| Carrier_Fit_Gauge | plate down | prototype tool |

PETG or PETG-HF, 0.40 mm nozzle, 0.20 mm layers. **Three perimeters** on the
lid skirt (1.20 mm = 3 × 0.40); four only locally at the four bosses and the
two hook features. 15–20% infill. **No support material on any part.** Deburr
the cable windows and the USB slot before assembly.

### Recommended first print

**`ESP32_Controller_Carrier_Fit_Gauge.stl` alone, and nothing else.** 5.35 cm³
and about fifteen minutes. It reproduces at 1:1 the −X end wall, the real fixed
ledge with its lead-in, the 4.50 mm support height, the clamp plinth with its
insert, and three read-off steps at 65.00 / 66.00 / 67.00 mm standing *below*
the carrier plane so they never obstruct it. Slide the acquired breakout in
under the ledge and read which step its free edge lands on. That settles
`adapter_pcb_l`, `adapter_pcb_t`, `pad_h` and the 0.20 mm retention gap against
the real board before any real material is spent.

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
2.70 · `insert_hole_d` 4.00 · `insert_depth` 5.00.

Two matter most in the short term:

- **The exact heat-set insert is still not recorded anywhere in the
  repository.** 4.00 mm × 5.00 mm is a common M3 short insert and it is a
  guess. Record the real part before printing the base, or the two lid screws
  and two clamp screws have nowhere to live.
- **`assembly_above_pcb_h` 24.00** is worth 1.00 mm of height and 0.358 cm³ per
  millimetre. See §2.4.

### 9.2 New in Rev B, and load-bearing

- **Nothing on the carrier underside within y ±9.83 mm at x ±27.00 mm.** The
  refined four-row joint model in §6.1 is what allows the cabinet fixings to
  sit under the board. If the real breakout has anything there, the fixings
  move or the design goes back to external mounting.
- **EN and BOOT positions remain unmeasured**, so v1.1 §6.4 forbids access
  holes and none is cut. The removable lid is the prototype access route, and
  the lid carries no EN or BOOT legend, because marking a hole that does not
  exist is worse than not marking it.
- **H1–H6 conductor counts** in §5 are read from `docs/Wiring.md`, but real
  bundle diameters depend on the insulation and ferrules actually used.

### 9.3 Physical behaviour nothing geometric can settle

- the fit gauge accepts the real breakout without stress or excessive play;
- the carrier sits flat on the four pads and slides under the ledge without
  forcing;
- the clamp retains it without bowing it;
- the ESP32 comes out of and goes back into its sockets with the lid off;
- every used terminal is reachable with the owner's actual screwdriver;
- the grouped H1–H6 harnesses route through the windows and the tie tabs
  without pinch or sharp bends;
- the ties transfer pull to the housing and not to the terminals;
- the board survives moderate cable pull without moving;
- lid assembly does not disturb the wiring, and the two hooks locate it without
  being stressed;
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

## 10. Reconciliation with specification v1.1

| § | Requirement | State |
|---|---|---|
| 2.1 | five named production/tool components | as built |
| 2.2 | eight forbidden features | none present; gate 22 |
| 3 | reference geometry and clearances | met; all still prototype gates |
| 4 | base: floor, pads, ledge, clamp, cabinet fixings | met and gated |
| 5 | grouped harnesses, open-bottom windows, internal ties | met and gated |
| 6 | USB opening, no plug, no EN/BOOT holes | met |
| 7 | ventilation and antenna | met; 5 top slots, none inside the keep-out |
| 8 | lid retention: 2 screws + 2 hooks, 4.00 overlap | met and gated |
| 9 | envelope and material gates | **mandatory limits met**; preferred targets NOT met — see §2.3 |
| 10 | FDM rules | met; the one self-declared rule is stated in §6.2 |
| 11 | CAD component structure | as specified |
| 12 | deliverables | all present; obsolete Rev A artefacts removed |
| 13 | twenty-two verification gates | all pass, in two independent tools |
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

**The housing is not physically validated and must not be described as such
until a printed part has been tested against the acquired hardware.**
