# Decca ESP32 Controller Housing — Rev C build report

> **Status: PROTOTYPE — PRINTED AND FITTED, NOT PRODUCTION APPROVED.**
> **PROTOTYPE PRINTED, FITTED AND INSTALLED — 2026-09-07.** See §10.
> Rev C is the first housing revision with measured hardware in it and the
> first ever to be printed. It fitted first time. It is **not production
> approved**: v1.7 §14 acceptance is outstanding, eleven prototype gates and
> three installation gates remain open, and several §3 values it was built
> on are still starting values rather than measurements.

**Controlling document:** `Decca_ESP32_Controller_Housing_Spec_v1.0.md` — whose
content is specification revision **v1.7**. The filename is retained for link
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
was the fixed ledge and an adjustable clamp on the short edges. Under v1.7
§4.6 the clamp is gone and the +X end is located by two posts through these
holes — see §2.4 and §5.3.

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
is at (28.50, 30.00), inside that footprint. §2.4 is what was done about it.

### 2.4 The clearance that actually decided it — and it is not the block

The M3 reading made screw-down retention look obvious, and the terminal block
does not stop it. What stops it is the **outermost conductor**.

The last terminal in each row sits at x 24.733 and the corner hole at 28.500 —
**3.767 mm apart**. Against the declared 2.60 mm ferrule:

| At a corner hole | clear of the outermost conductor |
|---|---:|
| M3 pan head, r 2.80 | **−0.33 mm** |
| M3 socket cap, r 2.75 | **−0.28 mm** |
| M2.5 socket cap, r 2.25 | +0.22 mm |
| **Ø2.60 locating post, r 1.30** | **+1.17 mm** |

No M3 head fits, and the M2.5 margin of 0.22 mm is not a margin at all when the
wire and ferrule sizes are themselves starting values. A post does fit, with
room to spare. So **the holes are used for location, not fastening** — v1.7
§4.6a now records the prohibition and the reason, so nobody re-proposes screws
without re-deriving this number against the conductors actually installed.

## 3. The one design move that decides everything

The owner reported the entry as "just above the base of the terminal block" and
ruled the port bore and internal depth out of scope, because they do not drive
housing geometry. **That is correct, and it is better than a measurement,
because it removes the dependency instead of pinning it.**

The only thing a port height was ever needed for was *how high can the long-side
wall rise before it stands in front of a terminal mouth*. "Just above the base"
answers it: **no useful wall height exists above the board on the long sides at
all.**

So v1.7 §5.3 requires the housing to clear the **entire 9.00 mm block height,
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

| Metric | Rev A | Rev B | Rev C, clamped | **Rev C, v1.7** | limit | preferred |
|---|---:|---:|---:|---:|---:|---:|
| Outside length | 105.00 | 81.60 | 78.10 | **75.50 mm** | ≤85 | — |
| Outside width | 77.00 | 70.10 | 73.10 | **73.10 mm** | ≤75 | — |
| Closed height | 38.30 | 35.30 | 27.20 | **27.20 mm** | ≤36 | — |
| Housing_Base | 49.66 | 16.85 | 18.65 | **17.98 cm³** | — | ≤15 |
| Housing_Lid | 14.84 | 16.07 | 9.56 | **9.25 cm³** | — | ≤18 |
| PCB_Clamp_Adjustable | 1.58 | 1.12 | 0.99 | **deleted** | — | — |
| Cabinet_Fastener_Cap × 2 | — | 0.16 | 0.16 | **0.16 cm³** | — | — |
| **Production total** | **67.93** | **34.20** | 29.36 | **27.39 cm³** | **≤35** | **≤30** |
| **Full-solid PETG mass** | **86.3** | **43.4** | 37.3 | **34.8 g** | **≤45** | **≤38** |

**Three production parts, not four**, and comfortably inside the preferred
targets rather than scraping them: 27.39 cm³ against a 30 cm³ preference and
34.8 g against 38 g. Rev A's 68 cm³ is down by 60%.

The length came from deleting the clamp. The +X floor beyond the board was a
7.50 mm clamp zone sized by a slot, the material beyond it, wall clearance at
full travel and an insert bore. With the clamp gone it carries nothing but the
two lid-screw bosses, so it is sized by **them** and nothing else — 5.40 mm, the
7.00 mm boss less the 1.60 mm end wall it merges into.

### 4.3 The 0.50 mm that was hiding in the lid-screw boss

Found while answering a question about the heat-set insert, and **it predates
the retention change** — Rev C carried it from the day it was built.

The boss was 6.00 mm deep with its screw 3.50 mm in from the outer face. That
leaves 1.50 mm of wall outboard of a Ø4.00 insert bore and **0.50 mm inboard** —
about one extrusion width, on the boss's free face. A heat-set insert expands
the plastic radially as it is driven in, so that face is exactly where the boss
splits, and this is the least proven fastener in the design.

The screw is now **centred** in a **7.00 mm** boss: **1.50 mm of wall in every
direction**, against a new v1.7 §4.12 minimum of 1.20 mm, gated in gate 12. It
costs 1.00 mm of enclosure length — 74.50 to 75.50 mm — against 9.50 mm of
remaining headroom to the 85 mm limit. Cheap.

The width is still the tightest dimension at 73.10 mm against a 75 mm limit,
because the 66 mm runs across the board and the terminal corridors are on that
axis.

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
| Housing_Base | 1 | 20.58 g | 20.58 | 1 h 7 m 30 s |
| Housing_Lid | 1 | 11.30 g | 11.30 | 22 m 57 s |
| Cabinet_Fastener_Cap | 2 | 0.19 g | 0.38 | 2 m 22 s |
| **Production total** | | | **32.26 g** | **1 h 35 m 11 s** |

**Support usage: none.** `enable_support = 0` and the slicer emitted **zero
support features on all three parts**, which is the operational confirmation of
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
| 4 | Four support pads at (±28.50, ±30.00) | carry the board, **centred on the measured mounting holes** | 3, 13 |
| 5 | One integral fixed ledge, −X, 2.00 mm grip | retains the −X short edge | 13, 15 |
| 6 | **Two Ø2.60 locating posts, +X** | locate the carrier by its own mounting holes | 5, 13, 14, 15 |
| 7 | Two lid-screw bosses, **vertical** M3 inserts, screw **centred**, 1.50 mm wall | lid retention at +X | 12, 17 |
| 8 | Two locating rebates, −X | lid location and capture | 17 |
| 9 | USB notch, open to the end-wall top | ≥14 × 9 service access with no bridge | 10 |
| 10 | Two recessed, capped cabinet fixings | cabinet mounting inside the footprint | 2, 16, 25, 26 |

### 5.3 Retention: one ledge, two posts, and no fastener at all

The −X short edge sits under the fixed ledge, 0.20 mm clear of the board top.
The +X end drops onto **two Ø2.60 posts through the two measured mounting
holes**. That is the whole retention system.

| | |
|---|---:|
| Post diameter in a bore reported as M3 | Ø2.60, **0.30 mm** radial clearance at 3.20 — and 0.20 at 3.00 |
| Engagement through the carrier | 1.60 mm, its full thickness |
| Proud of the carrier top | 1.40 mm |
| Clear of the outermost conductor | **1.17 mm** |
| Fitting tilt needed to clear the posts | 2.73°, lifting the ledge end **0.095 mm** inside its 0.20 mm gap |

**Only the +X pair carries a post, and that is not an economy.** The −X edge has
to slide in under the ledge at its final height, and it cannot do that with a
post already standing in a hole. The two −X holes are left empty, and the
assembly keep-out over them is left solid on purpose, so a stray feature there
still fails gate 5. The posts are bored out of that keep-out only where the
design is permitted to occupy it.

Fitting is: tilt the +X end up about 3 mm, slide the −X edge under the ledge,
lower the +X end onto the posts. Removal is the reverse — a deliberate two-part
motion, which is why the board is not going to walk off the posts on its own.

**What this deleted:** the whole `PCB_Clamp_Adjustable` part, two plinths, two
slotted M3 screws, two heat-set inserts, the clamp slot, the clamp travel, the
carrier-width range and 3.60 mm of enclosure length. Gate 15 is now a stronger
statement than it was: no fastener bears on this board anywhere, so there is
nothing left that could be over-tightened onto it.

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

v1.7 §5.9 requires housing-mounted restraint to be shown unnecessary before it is
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
30 CAD checks,  0 failed, 11 prototype gates open, 8 closed by the fitted prototype
29 mesh checks, 0 failed, 10 prototype, 3 installation, 8 closed by the fitted prototype
```

The two open counts differ by one because the suites classify the antenna
differently — the in-CAD suite calls it a prototype gate, the offline one an
installation gate. That is a deliberate difference, not drift: the suites are
independent, and 75 of the offline verifier's hand-typed constants were
cross-checked against the generator's derived chain with no disagreement.

Together they cover all thirty v1.7 §13 gates.

### 6.1 What verification caught, and it was a lot

Three of the six below concern the adjustable clamp, which v1.7 has since
deleted. They are kept as history: they are why the clamp cost what it cost, and
that is part of the case for replacing it.

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

## 7. Prototype gates — eleven still open, eight closed by the fitted print

**The axis correction.** Rev C was first built with the 66 mm along the rows
and the 63 mm across. The owner corrected it the same day. The parametric model
absorbed it in one edit and every gate was re-run; the envelope changed from
81.10 × 70.10 to 78.10 × 73.10 mm and the volume by 0.01 cm³. It also improved
two clearances — the support pads gained 0.75 mm of margin in their strip — and
forced two consequential changes: the corner returns shortened from 6.00 to
4.00 mm to stay clear of the row ends, and the cabinet fixings moved from
x ±26.00 to ±24.00 to stay off the −X cavity wall. The clamp's adjustable range
was re-centred at that point from the legacy 65–67 mm to 62–64 mm; v1.7 has
since deleted the clamp and the range with it, because a measured board and a
measured hole pitch leave nothing for an adjustment to absorb.

**Eight of these were closed on 2026-09-07 by the fitted prototype — see §10.**
What follows is what is left.

**Hardware still unmeasured:** PCB thickness (1.60) and the below-board
protrusion (2.50) — the fitted print shows the 4.50 mm pad height *works*, but
not what the two numbers behind it are; terminal-block
depth in Y (6.50); the heat-set insert **bore** (4.00 × 5.00 — the part is now
identified as **Hanglife M3 threaded**, owner 2026-09-06, the first time this
fastener has had a name anywhere in this repository, but its length and outer
diameter are still unmeasured and those are what the bore has to match); the
acquired cabinet screw's head against the declared
6.20 mm maximum envelope; the USB connector position; real conductor and ferrule
sizes; EN and BOOT positions, so no holes are cut; and the mounting holes'
exact bore, recorded at 3.20 from the reported M3 and used by nothing.

**Behaviour nothing geometric can settle:** that nothing sits under the board
outside the four modelled joint rows; the 0.25 mm lid fit on this printer and
filament; the 0.12 mm cap nib interference; PETG print quality with no support;
antenna performance with the lid fitted.

**Plus the one assumption left in §2.1** — the USB connector centred on its
short edge. The other two were closed by the fitted print (§10.1).

**Installation gates:** cabinet fixing centres and the surface behind them; that
the grouped cabinet wiring is secured outside the housing; antenna performance.

## 8. Printing

| Part | Orientation | Filament | Time |
|---|---|---:|---:|
| Housing_Base | **floor down** | 20.58 g | 1 h 7 m 30 s |
| Housing_Lid | **top face down** — makes the USB notch and vents print with no bridge | 11.30 g | 22 m 57 s |
| Cabinet_Fastener_Cap | flat, **2 off** | 0.19 g ea | 2 m 22 s ea |

No supports on any part. Worst unsupported reach 1.25 mm (CAD) / 0.75 mm (mesh)
against a self-declared 1.50 mm limit.

**It has been printed** — see §10 — and it is still **not production approved**.
v1.7 §14.0 makes a prototype print of a part this small a legitimate
instrument rather than something that has to wait for callipers, and §10
records gate by gate what the fitted print established and what it did not.

## 9. Files

**Current:** `../CAD/Decca_ESP32_Controller_Housing.f3d`, the assembly STEP,
three part STEPs, three print-ready STLs, this report, and twenty-one
`..._revC_*.png` renders — including `..._14b_locating_posts.png`, the two posts
standing in the two +X mounting holes with the two −X holes left empty.

**Removed as superseded:** `ESP32_Controller_PCB_Clamp_Adjustable.step` and
`.stl`, all Rev B STLs and STEPs for the two prototype coupons, and all
twenty-three `..._revB_*.png` renders. The generator deletes
them on every run, and both verifiers fail if a forbidden mesh reappears. The
Rev A and Rev B build reports are retained as history with superseded banners.

## 10. First physical validation — 2026-09-07

The owner printed this geometry, fitted the adapter, closed the lid and
installed the housing in the Decca. **It fitted first time.** No revision of
this housing had ever been printed before; Rev A and Rev B never got near a
printer.

The print was made ahead of the §3 starting values behind it being measured.
That is now explicitly allowed — v1.7 §14.0, added the same day — because on a
20 g part that prints in about an hour, the print is the faster and better
instrument: callipers on a populated board give the nominal, a fitted print
answers whether it seats.

### 10.1 What the fit closes

Eight gates, listed in both suites under **CLOSED BY PHYSICAL EVIDENCE** with
the observer and date on each:

| Closed | What the fit demonstrates |
|---|---|
| **The two locating posts enter the real mounting holes** | Ø2.60 posts at the measured 60 × 57 pitch went into the actual bores and the board seated. The single most novel thing in the design, and nobody had tried it. It also **confirms the re-measured pitch over the 58 × 56 first reported** — 58 × 56 would not have accepted these posts. |
| **The carrier fits** | Ledge, tilt-and-drop, posts and pads all worked as a sequence. |
| **The lid closes on the assembly** | Exercises the 0.25 mm per face fit, the 4.00 mm overlap at the ends and corners, and the whole height chain from the measured 20.00 mm assembly under a 24.00 mm ceiling. **Rev B died on a height assumption**; this is the first time one has been closed by a closed lid. |
| **The enclosure installs in the Decca** | The 75.50 × 73.10 mm envelope was accepted in the actual cabinet space. |
| **Nothing under the board outside the modelled joint rows** | The board seated on its four pads and over both cabinet pads with nothing fouling. Rev B's blanket keep-out is now disproved by a fitted board, not just by a gate. |
| **The terminal rows are centred on the 63.00 mm dimension** | Was an assumption. Ledge, pads and both posts all cleared, which they could not have done otherwise. |
| **The 9.00 mm block height is the block's own body height** | Was an assumption. The lid closed over the assembly, which is the consequence that was at risk. |
| **PETG prints this geometry with no support material** | On the owner's printer and filament. The slicer harness had independently emitted zero support features on all three parts. |

### 10.2 What it does not close, and the distinction matters

A board that seats proves the **4.50 mm pad height works**. It does not measure
the **PCB thickness** or the **below-board protrusion** it was derived from, and
those two still set the underside clearance. The same holds for the mounting-hole
**bore**: a Ø2.60 post demonstrably fits the real hole, but the bore is still
unmeasured and it is what decides how much play the board has.

That distinction is the whole of v1.7 §14.0 point 3, and both suites state it on
each entry rather than letting a fit against an unmeasured value pass for a fit
against a measured one.

**Eleven prototype gates and three installation gates remain open**, and several
things this print will have exercised are simply **not yet reported**: whether
the heat-set inserts drove into their bosses and the lid screws pulled the lid
down; whether the terminals are wired, which would close the entry corridors,
the screwdriver access and cover-removal-while-wired in one go; whether the two
cabinet fixings and their caps were used; and surface quality and cleanup.
