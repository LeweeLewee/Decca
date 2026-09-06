# Decca ESP32 Controller Housing — Rev C build report

> **Status: PROTOTYPE CAD. NOT PHYSICALLY VALIDATED.**
> Nothing here has been printed. Rev C is the first housing revision with any
> measured hardware in it, but most dimensions are still CAD starting values
> and every one is an open prototype gate. §7 lists them.

**Controlling document:** `Decca_ESP32_Controller_Housing_Spec_v1.0.md` — whose
content is specification revision **v1.6**. The filename is retained for link
stability.
**Generator:** `../CAD/Decca_ESP32_Controller_Housing_fusion.py`
**Independent verifier:** `../CAD/Decca_ESP32_Controller_Housing_verify.py`
**Slicer harness:** `../CAD/Decca_ESP32_Controller_Housing_slice.py`
**Date:** 2026-09-06 · **Material:** PETG / PETG-HF · **Method:** FDM, 0.40 mm
nozzle, 0.20 mm layers, **no support material on any part**

**Rev A and Rev B are both superseded. Their build report, exports and renders
are design history only and must not be printed.**

---

## 1. Why Rev C exists

Rev A was rejected for bulk: 105.00 × 77.00 × 38.30 mm and about 68 cm³ to hold
a board 66 × 63 mm, with all eighteen of its gates passing.

Rev B was rejected for something worse. It passed thirty gates and **could not
be wired**. It routed grouped harnesses over the tops of the terminal blocks,
because nobody had established how the acquired DORHEA adapter actually
connects. It connects from the **sides**: fifteen green screw terminals per long
side, screws operated from above, external conductors entering **horizontally**
through outward-facing ports. The two black vertical sockets carry the ESP32 and
are not wiring points at all.

Twice now a revision has satisfied every check it was given and still been the
wrong design, because the checks were written against the wrong picture. Rev C
starts from measured hardware.

## 2. What is measured, and what is not

The first housing revision with any measured hardware in it.

| Dimension | Value | Source |
|---|---:|---|
| Complete adapter + fitted ESP32, overall height | **20.00 mm** | owner, 2026-09-05 |
| Adapter PCB outline | **63 mm along the rows × 66 mm across them** | owner, 2026-09-06, axis corrected same day |
| Terminal blocks, outer face to outer face | **55.00 mm** | owner, 2026-09-06 |
| Terminal-block row length | **53.00 mm** | owner, 2026-09-06 |
| Terminal-block height | **9.00 mm** | owner, 2026-09-06 |
| Mounting-hole centre pitch | **60 mm across × 57 mm along** | owner, 2026-09-06; re-measured the same day, superseding 58 × 56 |
| Corner mounting-hole size | **M3** | owner, 2026-09-06 |
| Conductor entry position | just above the block base | owner, 2026-09-06 |

**The 66 mm is measured across the board, from one connector side to the
other**, and the 63 mm runs along the rows. Rev C as first built had these two
the wrong way round; the owner corrected it the same day, and the corrected
reading is also the self-consistent one:

| | correct | the wrong way round |
|---|---:|---:|
| Clear board outboard of each block face | (66 − 55) ÷ 2 = **5.50 mm** | (63 − 55) ÷ 2 = 4.00 mm |
| Clear board beyond each row end | (63 − 53) ÷ 2 = **5.00 mm** | (66 − 53) ÷ 2 = 6.50 mm |

Two ~5 mm margins is what a real board looks like. One 4.00 and one 6.50 was the
tell, and it was there to be noticed before the correction arrived.

Rev B had all three of these wrong anyway: blocks starting *at* the edge,
10.00 mm tall, spanning 49.00 mm.

Everything else — PCB thickness, the below-board protrusion, block depth in Y,
the USB position, conductor and ferrule sizes, the heat-set insert, the cabinet
screw head — remains a **STARTING** value, tagged as such in the generator's own
`STARTING` tuple and listed in §7.

### 2.1 Three assumptions, recorded so they cannot pass as measurements

| Assumption | If it is wrong |
|---|---|
| The terminal rows are centred along the 63.00 mm along-row dimension | the 5.00 mm clear ends move; one parameter |
| The USB connector is centred on its short edge | the notch is cut 16.00 mm wide against a 14.00 mm requirement to absorb it |
| The 9.00 mm block height is the block's own body height | if it was taken from the resting surface the block top drops, and the long walls are unaffected either way, because they are set by the board top face |

### 2.2 The hole pitch, first recorded as 58 × 56, re-measured as 60 × 57

The pitch was first given as 58 across × 56 along, on the grounds that it put
all four mounting holes at an equal inset from the nearest board edge. It did
not quite: on a 66 × 63 board that pair gives 4.00 mm across and 3.50 mm along,
0.50 mm short of equal, which meant one of the four numbers had to be 1.00 mm
out. Rather than pick one, the discrepancy was recorded and the owner re-took
the reading against a dimensioned top view.

**60.00 mm across × 57.00 mm along.** It closes exactly:

| | inset from the nearest edge |
|---|---:|
| across — (66 − 60) ÷ 2 | **3.00 mm** |
| along — (63 − 57) ÷ 2 | **3.00 mm** |

Equal on both axes with nothing left over — and it is the only resolution that
corrects both numbers at once instead of adjusting one of the four by 1.00 mm.
The holes also land clear of the terminal blocks in both directions: each hole
centre sits 2.50 mm outboard of the nearest block face, since the block faces
are 5.50 mm inboard of the long edges.

**No geometry moved.** `mount_pitch_x` and `mount_pitch_y` are recorded values
only — they appear in the generator's measured block and in the verifier's
constants, and are referenced by no derivation, no body and no gate. Retention
is the fixed ledge and the adjustable clamp on the short edges, per v1.6
§4.5–4.6.

### 2.3 The holes take M3, and the corner clearance is better than it looks

Reported by the owner on 2026-09-06. That is the **screw size, not a calliper
reading of the bore**, so `mount_hole_d` is recorded as a 3.20 mm starting value
— Ø3.00 is equally common and nothing here distinguishes them. Nothing in this
design uses it.

The orthogonal margins understate the real clearance, and it is worth writing
down why. A hole centre sits 2.00 mm beyond the row end and 2.50 mm outboard of
the block face — but it is outboard on **both** axes at once, so the nearest
block material is the block's **corner**, 3.202 mm away diagonally:

| At a corner hole | to the block corner | to the board edge |
|---|---:|---:|
| M3 socket cap, Ø5.50 | **+0.45 mm** | +0.25 mm |
| M3 pan, Ø5.60 | +0.40 mm | +0.20 mm |
| M3 countersunk, Ø6.00 | +0.20 mm | 0.00 mm |
| M3 with a DIN 125 washer, Ø7.00 | **−0.30 mm** | −0.50 mm |

So a plain M3 head fits and a washer does not. Separately — and this was not
designed in — **the four existing support pads already sit under the four
mounting holes.** Each pad spans x 23.00–31.00, y 28.75–31.75; each hole centre
is at (28.50, 30.00), inside that footprint. A Ø2.9 post through the hole would
overhang the pad's inboard edge by 0.20 mm, which a 0.50 mm pad widening
absorbs. §10 of the measurement request carries the decision that follows.

## 3. The one design move that decides everything

The owner reported the entry as "just above the base of the terminal block" and
ruled the port bore and internal depth out of scope, because they do not drive
housing geometry. **That is correct, and it is better than a measurement,
because it removes the dependency instead of pinning it.**

The only thing a port height was ever needed for was *how high can the long-side
wall rise before it stands in front of a terminal mouth*. "Just above the base"
answers it: **no useful wall height exists above the board on the long sides at
all.**

So v1.6 §5.3 requires the housing to clear the **entire 9.00 mm block height,
across the full 53.00 mm row, on both long sides.** Wherever the port actually
sits inside that block, nothing this housing owns is ever in front of it. **A
later port measurement cannot invalidate the geometry**, and the cost is nil,
because a wall in that band was never available.

Everything else follows:

- the base's long walls **stop at z 6.10**, the adapter's top face, leaving
  **17.90 mm of open side** above them;
- the lid carries **no long-side skirt** — one would have to be dragged through
  the fitted conductors to get the lid off;
- **all** retention, fastening and lid support move to the two short ends, into
  the 5.00 mm of clear board the measured rows leave there.

What replaces the port measurement is a **declared routing value** this design
owns: `straight_run` = **12.00 mm** from the block's outward face before a
conductor may bend. It is parameterised, gated and reported. The conductor
envelope follows the wire and ferrule actually installed, not the terminal bore.

## 4. Envelope and material

| Metric | Rev A | Rev B | **Rev C** | v1.6 limit | preferred |
|---|---:|---:|---:|---:|---:|
| Outside length | 105.00 | 81.60 | **78.10 mm** | ≤85 | — |
| Outside width | 77.00 | 70.10 | **73.10 mm** | ≤75 | — |
| Closed height | 38.30 | 35.30 | **27.20 mm** | ≤36 | — |
| Housing_Base | 49.66 | 16.85 | **18.65 cm³** | — | ≤15 |
| Housing_Lid | 14.84 | 16.07 | **9.56 cm³** | — | ≤18 |
| PCB_Clamp_Adjustable | 1.58 | 1.12 | **0.99 cm³** | — | ≤2 |
| Cabinet_Fastener_Cap × 2 | — | 0.16 | **0.16 cm³** | — | — |
| **Production total** | **67.93** | **34.20** | **29.36 cm³** | **≤35** | **≤30** |
| **Full-solid PETG mass** | **86.3** | **43.4** | **37.3 g** | **≤45** | **≤38** |

**Rev C is the first revision to meet the preferred targets as well as the
mandatory limits.** 29.36 cm³ against a 30 cm³ preference and 37.3 g against
38 g. Rev A's 68 cm³ is down by 57%. The width is the tightest of the three
dimensions at 73.10 mm against a 75 mm limit, because the 66 mm now runs across
the board and the terminal corridors are on that axis.

The height did it. Rev B's 35.30 mm closed height came from an unverified
24.00 mm "above PCB" assumption; the measured 20.00 mm overall, applied from the
assembly's own lowest underside feature, gives **27.20 mm** — 8.10 mm shorter,
and the lid falls from 16.07 to 9.56 cm³ because it is a flat cover instead of a
deep box.

### 4.1 Height chain, from the measured 20.00 mm

```
floor 1.60 | datum A 2.00 | PCB 4.50–6.10 | block top 15.10
          | assembly top 22.00 | cavity 24.00 | lid top 25.60
```

Datum A is the assembly's own lowest underside feature — the surface it rests on
— and the measured 20.00 mm runs from there to its highest point. **It is not
converted into an above-PCB value**, and Rev B's `assembly_above_pcb_h` does not
exist in this generator in any form.

### 4.2 Real slicer evidence

The solid-volume figure above is a conservative **design gate** and stays one. It
is not spool consumption. The set was sliced with the Bambu Studio CLI via
`../CAD/Decca_ESP32_Controller_Housing_slice.py` against a declared profile:
**Bambu Lab P1S, Generic PETG-HF, 0.40 mm nozzle, 0.20 mm layers, 3 perimeters,
15% infill, no supports, textured PEI plate**, each part in its stated
orientation.

| Part | Qty | Filament each | g total | Print time each |
|---|---:|---:|---:|---:|
| Housing_Base | 1 | 21.58 g | 21.58 | 1 h 9 m 8 s |
| Housing_Lid | 1 | 11.67 g | 11.67 | 23 m 23 s |
| PCB_Clamp_Adjustable | 1 | 1.07 g | 1.07 | 7 m 24 s |
| Cabinet_Fastener_Cap | 2 | 0.19 g | 0.38 | 2 m 22 s |
| **Production total** | | | **34.70 g** | **1 h 44 m 39 s** |

**Support usage: none.** `enable_support = 0` and the slicer emitted **zero
support features on all four parts**, which is the operational confirmation of
the geometric claim in §6. Every slice returned `return_code 0, "Success."` with
no warnings.

## 5. Architecture as built

**Housing_Base**, printed floor-down. Ten structures, each with a stated purpose
and a numbered gate. There is nothing else on the part.

| # | Feature | Purpose | Gate |
|---|---|---|---|
| 1 | Continuous 1.60 mm insulating floor | isolates the carrier from the cabinet | 2 |
| 2 | **Low long walls, stopping at z 6.10** | the whole architecture: nothing in front of a terminal mouth | 7, 8, 22 |
| 3 | Full-height short end walls + four corner returns | carry the lid, clear of the rows by 1.00 mm | 12, 17 |
| 4 | Four support pads at (±27.00, ±30.25) | carry the board in the 5.50 mm clear side strip, 1.25 mm to spare | 3, 13 |
| 5 | One integral fixed ledge, −X, 2.00 mm grip | retains the −X short edge | 13, 15 |
| 6 | Two clamp plinths, vertical M3 inserts | hard stop for the clamp | 13, 14, 15 |
| 7 | Two lid-screw bosses, **vertical** M3 inserts | lid retention at +X | 12, 17 |
| 8 | Two locating rebates, −X | lid location and capture | 17 |
| 9 | USB notch, open to the end-wall top | ≥14 × 9 service access with no bridge | 10 |
| 10 | Two recessed, capped cabinet fixings | cabinet mounting inside the footprint | 2, 16, 25, 26 |

**Housing_Lid**, printed **top-face-down**: flat 1.60 mm cover, skirts at the
**short ends and corners only**, two vertical M3 screws at +X (y ±26.00), two
locating lugs at −X, a USB notch open at the skirt's free edge, and five modest
top vents clear of the antenna keep-out.

**The lid screws are vertical.** Rev B had to use horizontal inserts because its
base wall was shallow; here the short end walls are full height, so the least
proven fastener in the whole programme is simply not needed.

### 5.1 Terminal entry, in detail

| | |
|---|---|
| Terminals | 15 per side, **3.533 mm pitch** over a measured 53.00 mm row |
| Block faces | 5.50 mm inboard of the long PCB edge, from the measured 55.00 mm across a 66.00 mm board |
| Corridor | the **whole** 9.00 mm block height, z 6.10 → 15.10, over the **whole** row, from the block face out past the enclosure |
| Long wall top | z 6.10, the board top face, leaving 17.90 mm of open side |
| Declared straight run | 12.00 mm to y 39.50; the outermost enclosure face is at 36.55, so a conductor is clear of the housing after **9.05 mm** and free for the remaining 2.95 |
| Grouping | conductors stay individual to y ±39.50; the four named bundles begin only beyond that |
| Screw access | 30 Ø6.00 mm corridors from z 15.10 upward, none obstructed, with representative wires fitted |

All **thirty** terminals are modelled with corridors and conductors, not only
the ones `docs/Wiring.md` uses, because the physical left-to-right terminal order
has not been recorded. Thirty is the superset, so the gates cannot be passed by
choosing convenient terminals.

### 5.2 Strain relief: none, and none justified

v1.6 §5.9 requires housing-mounted restraint to be shown unnecessary before it is
omitted. It is: the grouped cabinet wiring is secured immediately outside the
housing, nothing printed sits between a terminal mouth and the exterior, and
gate 22's 5 022 probes find **no printed feature of any kind** above the board
plane over either terminal row. No pull test, load test or anchor coupon is
required, and none exists.

## 6. Verification

Two independent suites. The in-CAD suite works on the BRep solids; the offline
suite reads **only** the exported STLs and re-derives every claim from triangles
against values typed in by hand. Neither imports the other's numbers.

```
30 CAD checks,  0 failed, 14 prototype gates open
29 mesh checks, 0 failed, 14 prototype, 3 installation
```

Together they cover all thirty v1.6 §13 gates.

### 6.1 What verification caught, and it was a lot

Every item below is a design change the checks forced. None was fixed by moving
a threshold.

- **A blanket underside keep-out left nowhere for a cabinet fixing.** Gates 3
  and 5 rejected the two recessed fixings the moment they were placed. A board
  does not have solder under all of it; the model now carries the **four actual
  joint rows** — two terminal blocks, two ESP32 sockets — and the fixings sit on
  the clear centreline between them. That the centreline really is clear
  underneath is a prototype gate, not a measurement.
- **The fixed ledge needed support.** Gate 18 measured 1.75 mm of unsupported
  reach against a 1.50 mm limit. The 45° lead-in went from 0.80 to 1.40 mm;
  reach is now 1.25 mm.
- **The cabinet pad was exactly tangent to the cavity wall.** At `cab_x` 27.00
  the 13.00 mm pad touched x −33.50 on a single line. Fusion reported a valid
  solid; the exported mesh had a **non-manifold edge** there and mesh gate 1
  failed. This is the same tangency trap the Rev B chamfer hit. Moving the
  fixings to x ±26.00 designs it out rather than checking for it.
- **The lid-screw bosses reached into the clamp bar.** The two suites
  disagreed — the offline verifier's hand-typed `LID_SCREW_Y` was the intended
  26.00 while the generator still had 22.00 — and the interference was real,
  about 38 mm³. That is exactly what hand-typing the expected values is for.
  CAD gate 14 now fails on the interference as well as the grip.
- **The clamp bar hit the +X wall at full travel.** Caught twice, once at rest
  and once at the 67.00 mm carrier. The fix is not a shorter bar but a bound:
  `bar_x1` is now derived from the wall position **at full travel**, and the
  clamp zone widened from 6.00 to 7.50 mm because four constraints — slot
  length, material beyond the slot, wall clearance at travel, and the insert
  bore staying inside the plinth — cannot all be met in 6.00 mm.
- **The clamp plinths reached under the board.** Bounded to the clamp zone.
- **Five bugs in the verifier itself**, all found by running it: a slot scan
  that measured the scan window instead of the slot; a plinth probe that landed
  down the insert bore; two radial profiles marching outward when they should
  have marched inward; a screw-hole probe sitting on the tessellation seam; and
  an `overhang_report` unpacked with the wrong arity.

## 7. Prototype gates — every one of these is still open

**The axis correction.** Rev C was first built with the 66 mm along the rows
and the 63 mm across. The owner corrected it the same day. The parametric model
absorbed it in one edit and every gate was re-run; the envelope changed from
81.10 × 70.10 to 78.10 × 73.10 mm and the volume by 0.01 cm³. It also improved
two clearances — the support pads gained 0.75 mm of margin in their strip — and
forced two consequential changes: the corner returns shortened from 6.00 to
4.00 mm to stay clear of the row ends, and the cabinet fixings moved from
x ±26.00 to ±24.00 to stay off the −X cavity wall. **The clamp's adjustable
range was also re-centred from the legacy 65–67 mm to 62–64 mm**, because it
works along the measured 63.00 mm dimension.

**Hardware still unmeasured:** PCB thickness (1.60) and the below-board
protrusion (2.50), which together set the 4.50 mm pad height; terminal-block
depth in Y (6.50); the heat-set insert (4.00 × 5.00, still unrecorded anywhere
in this repository); the acquired cabinet screw's head against the declared
6.20 mm maximum envelope; the USB connector position; real conductor and ferrule
sizes; EN and BOOT positions, so no holes are cut; and the mounting holes'
exact bore, recorded at 3.20 from the reported M3 and used by nothing.

**Behaviour nothing geometric can settle:** that nothing sits under the board
outside the four modelled joint rows; the 0.25 mm lid fit on this printer and
filament; the 0.12 mm cap nib interference; PETG print quality with no support;
antenna performance with the lid fitted.

**Plus the three assumptions in §2.1.**

**Installation gates:** cabinet fixing centres and the surface behind them; that
the grouped cabinet wiring is secured outside the housing; antenna performance.

## 8. Printing

| Part | Orientation | Filament | Time |
|---|---|---:|---:|
| Housing_Base | **floor down** | 21.58 g | 1 h 9 m 8 s |
| Housing_Lid | **top face down** — makes the USB notch and vents print with no bridge | 11.67 g | 23 m 23 s |
| PCB_Clamp_Adjustable | flat, loaded section across the layers | 1.07 g | 7 m 24 s |
| Cabinet_Fastener_Cap | flat, **2 off** | 0.19 g ea | 2 m 22 s ea |

No supports on any part. Worst unsupported reach 1.25 mm (CAD) / 0.75 mm (mesh)
against a self-declared 1.50 mm limit.

**Nothing is approved for printing yet.** The open gates in §7 come first, and
the most valuable next physical action is confirming the four §2.1 assumptions
and the below-board protrusion against the real board.

## 9. Files

**Current:** `../CAD/Decca_ESP32_Controller_Housing.f3d`, the assembly STEP, four
part STEPs, four print-ready STLs, this report, and twenty
`..._revC_*.png` renders.

**Removed as superseded:** all Rev B STLs and STEPs for the two prototype
coupons, and all twenty-three `..._revB_*.png` renders. The generator deletes
them on every run, and both verifiers fail if a forbidden mesh reappears. The
Rev A and Rev B build reports are retained as history with superseded banners.
