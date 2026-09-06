# DORHEA 30-pin terminal adapter — measurement request

**Raised:** 2026-09-05 · **Blocks:** replacement (post-Rev-B) housing CAD
**Controlling document:** `Decca_ESP32_Controller_Housing_Spec_v1.0.md`, content
revision **v1.5**, §3, §5 and §15
**Subject:** DORHEA "ESP32 Expansion Board 30Pin GPIO Breakout Board 1 into 2
Module Terminal Adapter", **with the selected 30-pin ESP32 DevKit fitted**

> Specification v1.5 §15: *"Do not begin replacement production CAD until the
> physical terminal-entry measurements in sections 3, 5 and 14 are recorded. A
> supplier photograph establishes topology, not manufacturing dimensions."*
>
> **GATE CLOSED 2026-09-06.** The owner supplied the macro dimensions and
> ruled the fine terminal-port detail out of scope, on the grounds that the
> hole size and internal depth do not drive housing geometry. That is
> correct, and §11 records how the remaining dependency was designed out
> rather than measured. Replacement CAD is released to proceed.

---

## 1. What the repository actually holds

Searched: `mechanical/CAD`, `mechanical/STL`, `mechanical/Drawings`,
`hardware/PCB`, `hardware/Schematics`, `hardware/Wiring`, `assets/Photos`,
`docs/`, and the full git history for deleted models.

| | Result |
|---|---|
| A CAD model of the DORHEA adapter | **None.** No STEP, STL, f3d, DXF or PDF of the board exists, and none has ever been deleted from history. |
| A dimensioned drawing or datasheet | **None.** `hardware/PCB`, `hardware/Schematics` and `assets/Photos` contain only placeholder READMEs. |
| A photograph with a scale | **None** in the repository. |
| Any reference geometry at all | Only `REF_30Pin_Terminal_Adapter` inside the Rev B generator. It is a box-and-blocks approximation built entirely from values the generator itself lists in its `STARTING` tuple — *"a CAD starting value; NOT measured; an open prototype gate"*. **It also has no side ports of any kind**, because Rev B assumed the wrong topology. It cannot be used as a reference model. |

**Conclusion: the repository does not contain a geometrically accurate model of
this board, and twelve of the thirteen mandatory inputs are unmeasured.**

## 2. Measurement status of every mandatory input

| Mandatory input (sprint brief) | Value in the repository today | Status |
|---|---|---|
| Actual PCB length and width | **66 × 63 mm** | ✅ **MEASURED 2026-09-06** — owner confirmed the supplier figure |
| PCB thickness | 1.60 mm | **assumed** |
| Lowest underside feature | 2.50 mm below the PCB | **assumed** |
| Terminal-block height and depth | **9.00 mm high**; depth still open | ✅ **height MEASURED 2026-09-06**; per-block depth in Y still open |
| Terminal-mouth centre height from the lowest datum | — | **absent from the model entirely** |
| Terminal-mouth opening | — | **absent from the model entirely** |
| Usable conductor insertion depth | — | **absent from the model entirely** |
| Terminal pitch and exact positions | **row length 53.00 mm**; pitch consistent with 3.50 | ✅ **row length MEASURED 2026-09-06**; pitch inferred, not measured |
| Practical wire and ferrule envelope | 2.00 mm conductor Ø | **assumed** |
| Mounting-hole diameter and centres | **60 × 57 mm centre pitch; the holes take M3** | ✅ **CLOSED 2026-09-06** |
| USB connector position | DevKit starting values | **assumed** |
| Component-free PCB-edge regions | 3.00 mm short / 2.50 mm long | **assumed** |
| **Complete assembly height** | **20.00 mm overall** | ✅ **MEASURED 2026-09-05** |

**Five of thirteen are closed or part-closed, including M4.** Of the four
marked ★ in §4 — the ones that block the architecture rather than the detail —
**M4 is closed and M1, M2 and M3 remain open.** Those three are all on one
terminal block.

## 3. Datums — measure from these, and say which one each figure uses

Set the adapter down on a flat surface **with the ESP32 fitted**, terminal
screws upward.

| Datum | Definition |
|---|---|
| **A** | **Z zero.** The flat surface the assembly rests on — i.e. the assembly's actual lowest underside feature, whatever that turns out to be. This is the datum the confirmed 20.00 mm overall height already uses. |
| **B** | **X zero.** The PCB short edge **nearest the ESP32's USB connector**. |
| **C** | **Y zero.** One PCB long edge; nominate it as **side 1** and mark it. |

**Terminal numbering:** terminal **1** is the one nearest Datum B on side 1.
Number along each side away from B, 1–15.

Every dimension below is *from Datum A, B or C as stated*, not from the PCB top
face and not from a component.

## 4. Measurements required

### ★ Group 1 — the terminal ports. These block everything.

With side entry, the long-side wall of the base cannot rise above the bottom of
the terminal mouths. **M1–M4 therefore set the base wall height, the lid skirt
strategy and the whole architecture.** Nothing sensible can be drawn without
them.

| ID | Measure | From | Tool | Feeds |
|---|---|---|---|---|
| ~~**M1**~~ | ~~Terminal-mouth **centre height**~~ | Datum A | ✅ **CLOSED qualitatively: the hole sits just above the base of the terminal block**, owner 2026-09-06. Designed out — see §11. |
| ~~**M2**~~ | ~~Terminal-mouth **opening**~~ | — | ✅ **OUT OF SCOPE, owner 2026-09-06.** The hole is small; each terminal is approximately 3 mm wide. The housing never enters the hole, so its size does not drive housing geometry. |
| ~~**M3**~~ | ~~**Usable insertion depth**~~ | mouth face | ✅ **OUT OF SCOPE, owner 2026-09-06.** Depth *inside* the block is the manufacturer's business. What the housing must provide is a straight run *outside* the mouth, which is a declared routing value, not a board measurement. |
| ~~**M4**~~ | ~~Terminal-block **outward face position**~~ | Datum C | ✅ **CLOSED: outer faces 55.00 mm apart on a 63.00 mm board → each block face sits 4.00 mm inboard of its long PCB edge.** Owner, 2026-09-06. |
| M5 | Terminal **pitch**, and centre of terminal 1 | Datum B | callipers over a known span (measure 1→15 and divide) | ⚠ **PART-CLOSED: row length 53.00 mm**, owner 2026-09-06. 15 ways in 53.00 is consistent with a 3.50 mm pitch (15 × 3.50 = 52.50 plus end walls) but the pitch itself is **inferred, not measured**. Still wanted: terminal-1 centre from Datum B. |
| M6 | Terminal-block **height** and **depth** inboard | Datum A / Datum C | callipers | ⚠ **PART-CLOSED: total height 9.00 mm**, owner 2026-09-06 — recorded as the block's own body height; confirm whether it was taken from the PCB top face or from Datum A. Per-block **depth in Y** is still open: 55.00 mm outer-to-outer does not give it without the gap between the two rows. |
| M7 | Screw **drive type and head size**, and how far the screw head sits below the block top face | Datum A | callipers | screwdriver corridor, gate 6 |

### Group 2 — board outline and vertical stack

| ID | Measure | From | Feeds |
|---|---|---|---|
| ~~M8~~ | ~~PCB **length** and **width**~~ | edge to edge | ✅ **CLOSED: 66 × 63 mm**, owner, 2026-09-06. Confirms the supplier figure as the PCB outline. Whether anything **overhangs** that outline is still M13. |
| M9 | PCB **thickness** | — | retention, §3 |
| M10 | **What actually touches the table**, and the height of the **PCB underside** above Datum A | Datum A | floor clearance, gate 3 |
| M11 | **PCB top face** height | Datum A | all internal chains |
| M12 | **Which feature is the highest point** of the 20.00 mm assembly | — | confirms how the closed 20.00 mm is applied |
| M13 | Does **anything overhang** the PCB outline — terminal blocks, sockets, the USB shell? Where, and by how much? | Datum B / C | true plan envelope |

### Group 3 — fixings, USB and clear regions

| ID | Measure | From | Feeds |
|---|---|---|---|
| M14 | **Mounting-hole** diameter and each hole centre | Datum B and C | ⚠ **PART-CLOSED: centre pitch 60 mm across × 57 mm along**, owner 2026-09-06 (re-measured the same day, superseding 58 × 56). ✅ **CLOSED the same day: the holes take M3.** That is the screw size, not a calliper reading of the bore, which is recorded as a 3.20 mm starting value. It is enough to settle §10. |
| M15 | **USB opening** centre height, width, and position along the short edge; how far the shell protrudes past the PCB edge | Datum A / Datum C | ≥14 × 9 mm opening, gate 10 |
| M16 | **Component-free strip** along each PCB edge, **top face** | each edge | fixed ledge and clamp bearing, gate 13 |
| M17 | **Component-free strip** along each PCB edge, **underside**, and whether the board's centreline near each short end is clear underneath | each edge | support pads and the two recessed cabinet fixings, gates 3 and 16 |

### Group 4 — the installer's own hardware, not the board

| ID | Measure | Feeds |
|---|---|---|
| M18 | Insulated **outside diameter** of the 22–24 AWG conductor to be used | conductor envelope, gate 9 |
| M19 | **Ferrule** barrel outside diameter and length, plus collar diameter and length | fits M2 and M3, gate 9 |

### Group 5 — one observation, no tools needed

| ID | Record | Feeds |
|---|---|---|
| M20 | The **silkscreen label at each of the 30 terminals, in order**, side 1 then side 2 (photograph is fine). | Which terminals the Decca harnesses actually use, so only those get modelled corridors — gate 23 and the H1–H6 grouping in `docs/Wiring.md`. |

## 5. Photographs — only where they resolve a listed measurement

Requested **only** if the measurement itself proves awkward. A photograph
without a scale in the same plane as the feature resolves nothing.

| ID | Shot | Resolves |
|---|---|---|
| P1 | One long side, camera square-on, **steel rule laid in the same plane as the terminal mouths** | M1, M2 if callipers cannot reach |
| P2 | Single terminal block, close up, **callipers open across the mouth** | M2 |
| P3 | Underside, flat, rule across it | M10, M17 |
| P4 | Top face with the ESP32 **removed**, rule along a long edge | M5, M14, M16, M20 |

## 6. Minimum set to unblock

**M4 and M8 are now closed. Three numbers remain in the blocking set: M1, M2
and M3, and all three are on a single terminal block.** With those, the
long-side architecture can be laid out and the base wall height fixed. **M10
and M11** then allow a complete base. Everything else refines detail that can be
parameterised in the meantime.

## 7. What will not be assumed

- The supplier's **25 mm** dimension will not drive any CAD. Its datums are
  ambiguous (v1.5 §3).
- Terminal geometry will not be scaled off the listing photograph
  (brief: *"Do not estimate missing terminal geometry from the product
  photograph"*).
- The confirmed **20.00 mm** is an **overall envelope from Datum A**. It will
  **not** be converted into a replacement "above PCB" value by subtracting an
  assumed PCB thickness or underside allowance (v1.5 §9.3). It is used as-is,
  from the measured underside datum, once M10 and M11 establish where that
  datum sits relative to the board.
- Rev B's `assembly_above_pcb_h = 24.00 mm` is dead. It will not be carried
  into the replacement generator in any form.
- No measurement in §4 will be given a plausible-looking number and presented
  as validated geometry.

## 8. What happens when this is returned

1. The measured values are recorded in v1.5 §3 and in the replacement
   generator, tagged **MEASURED** with the date, not `STARTING`.
2. `REF_30Pin_Terminal_Adapter` is rebuilt to the real board, including the
   outward-facing ports it has never had, alongside the new
   `REF_Terminal_Entry_Corridors` and `REF_Installed_Wires_And_Ferrules`
   components v1.5 §11 requires.
3. Only then is replacement production geometry drawn, to the v1.5 §13 gates.

Until then, every Rev B housing body, STL, STEP, render and slice result stays
**superseded and not for printing**, as v1.5 §15 requires and as the CAD, STL
and Drawings READMEs and the Rev B build report already state at the top.

---

## 9. Measurements returned so far

| Date | ID | Value | Notes |
|---|---|---|---|
| 2026-09-05 | — | Complete assembly height **20.00 mm overall** | From the assembly's lowest underside feature (Datum A) to its highest point. Recorded in specification v1.5 §9.3. |
| 2026-09-06 | **M8** | PCB outline **66 × 63 mm** | Confirms the supplier-stated plan envelope. **Axis corrected by the owner the same day: the 66 mm is ACROSS the board, from one connector side to the other, and the 63 mm runs ALONG the rows.** Any overhang beyond this outline is still open (M13). |
| 2026-09-06 | **M14** | Mounting-hole centre pitch **60 mm across × 57 mm along**; the holes take **M3** | Re-measured the same day, superseding an earlier 58 × 56 reading. Every hole is then 3.00 mm from its nearest board edge — see below. **M14 is closed.** The exact bore is not calliper-measured and is recorded as a 3.20 mm starting value. |
| 2026-09-06 | **M4** | Terminal blocks **55.00 mm outer face to outer face** | On the 66.00 mm across dimension this puts each block's outward face **5.50 mm inboard of its long PCB edge**. |
| 2026-09-06 | **M5** (part) | Terminal-block row **length 53.00 mm** | 15 ways in 53.00 mm is consistent with 3.50 mm pitch. Pitch inferred, not measured. Leaves 5.00 mm of clear board beyond each end of the rows. |
| 2026-09-06 | **M6** (part) | Terminal-block **total height 9.00 mm** | Recorded as the block's own body height. Datum to confirm. Per-block depth in Y still open. |
| 2026-09-06 | **M1** | Wire hole sits **just above the base of the terminal block** | Qualitative. Designed out rather than dimensioned — see §11. |
| 2026-09-06 | **M2** | Terminal width **approximately 3 mm** each; hole itself small | Consistent with 53.00 mm ÷ 15 = 3.53 mm pitch. Owner ruled the hole size out of scope. |
| 2026-09-06 | **M3** | — | Owner ruled internal insertion depth out of scope. |

### What follows arithmetically from the batch above

These are consequences of the measured numbers, not new measurements:

- Each terminal block's outward face is **5.50 mm inboard** of its long PCB edge — (66.00 − 55.00) ÷ 2, using the corrected across dimension.
- The rows are 53.00 mm long on the 63.00 mm along dimension, leaving **5.00 mm of clear board beyond each end of the rows**, which is where the corner mounting holes and every retention feature sit.
- Both margins land near 5 mm, which is what a real board looks like. The wrong axis assignment gave 4.00 and 6.50 — the asymmetry was the tell.
- Rev B was wrong on all three: it modelled the blocks starting **at** the PCB edge, 10.00 mm tall, spanning 49.00 mm. Measured: 5.50 mm inboard, 9.00 mm tall, 53.00 mm long.
- On the re-measured 60 × 57 hole pitch every mounting hole sits **3.00 mm in from its nearest board edge**, which puts each hole centre 2.50 mm outboard of the nearest block face — clear of the blocks in both directions.

### The hole pitch, re-measured and now closed

**CLOSED 2026-09-06.** The pitch was first returned as 58 × 56, with the reason given that it put all four holes at an equal inset from the nearest edge. On a 66 × 63 board it did not: 4.00 mm across and 3.50 mm along, 0.50 mm short. That meant one of the four numbers was 1.00 mm out, and rather than pick one, the discrepancy was recorded as open.

The owner re-took the reading against a dimensioned top view and returned **60.00 mm across × 57.00 mm along**, which closes exactly — **3.00 mm from every board edge on both axes**, nothing left over. It is also the only resolution that corrects both numbers together rather than adjusting one of the four by 1.00 mm. The discrepancy is closed, not carried.

**M14 is closed.** The owner reported the holes as **M3** the same day, which is what §10 was waiting on.

These are recorded here as they arrive. They will be rolled into specification
§3 in one revision when the blocking set is complete, so the specification is
not versioned once per reading.

**Nothing is blocking. The gate is closed.**

## 11. How the last dependency was designed out instead of measured

The owner's position — that the hole size and internal depth do not impact the
design, and the macro dimensions are sufficient — is correct, and it is better
than a measurement because it removes the dependency instead of pinning it.

**The reasoning.** The only thing M1 was ever needed for was *how high can the
long-side wall rise before it stands in front of a terminal mouth*. The answer
"just above the base of the block" makes that question moot: the entry is low in
a block that itself starts at the PCB top face, so **no useful wall height
exists above the board on the long sides at all.**

**The design response.** Rather than model the mouth at a measured height and
tuck a wall beneath it, the replacement clears **the entire 9.00 mm block
height** across the full 53.00 mm row length on both long sides. The base's long
walls therefore stop at the PCB top face and the lid carries no long-side skirt.

That is conservative by construction: wherever the hole actually sits within the
block, nothing the housing owns is ever in front of it. **A later measurement of
M1, M2 or M3 cannot invalidate the geometry**, because the housing already
clears more than the worst case. The cost is nil — a wall in that band was never
available.

**What replaces M3.** The straight run a conductor needs before it may bend is
now a **declared routing value** owned by this design, not a board dimension. It
is parameterised, stated in the build report and gated, and it is measured from
the block's outward face to the enclosure exterior and beyond.

**M2 likewise.** The conductor envelope is driven by the wire and ferrule the
installer actually uses (M18, M19 — the installer's own hardware), not by the
terminal bore. The housing never enters the bore.

## 10. A question the mounting holes now raise

Specification v1.5 §4.5–4.6 mandates a fixed ledge at one short PCB edge and an
adjustable clamp with two M3 screws at the other, because §3 recorded no usable
mounting-hole pattern. There now is one: **60 mm across × 57 mm along, holes
taking M3**, every hole 3.00 mm from its nearest board edge.

### 10.1 The clearance is better than the orthogonal margins suggest

A hole centre sits 2.00 mm beyond the row end and 2.50 mm outboard of the block
face. Neither is the binding number, because the hole is outboard on **both**
axes at once — the nearest block material is the block's **corner**, 3.202 mm
away diagonally.

| At a corner hole | to the block corner | to the board edge |
|---|---:|---:|
| M3 socket cap, Ø5.50 | **+0.45 mm** | +0.25 mm |
| M3 pan, Ø5.60 | +0.40 mm | +0.20 mm |
| M3 countersunk, Ø6.00 | +0.20 mm | 0.00 mm |
| M3 with a DIN 125 washer, Ø7.00 | **−0.30 mm** | −0.50 mm |

A plain M3 head fits at all four corners. A washer does not, and a countersunk
head sits exactly flush with the board edge.

### 10.2 The support pads are already under the holes

Not designed in — noticed. Each of the four support pads spans x 23.00–31.00,
y 28.75–31.75, and each hole centre is at (28.50, 30.00), inside that footprint.
A Ø2.9 post through a hole spans y 28.55–31.45, overhanging the pad's inboard
edge by 0.20 mm; a 0.50 mm pad widening absorbs it. **The four pads that already
carry the board are in the right place to locate it as well.**

### 10.3 The decision

Two routes are now open, and they are not close in cost:

- **Posts, no hardware.** Four Ø2.9 posts grown off the existing pads, through
  the mounting holes, with the lid holding the board down. This deletes the
  fixed ledge, the adjustable clamp, its two M3 screws, its two heat-set
  inserts, the clamp slot, the plinths and the whole clamp-travel gate — one
  fastener family and one moving part gone, and the only unproven fastener in
  the programme (the heat-set insert) with them.
- **Keep §4.5–4.6.** The ledge and clamp, which work today and pass every gate.

**The real trade is tolerance, not material.** The clamp forgives ±1.00 mm of
board-length error by design; four rigid posts forgive only the hole clearance,
about 0.15 mm per side on a Ø3.20 bore, and they must all line up at once. The
classic mitigation is two round posts and two elongated into slots, which
constrains position and rotation without over-constraining. That is a real
design question and it has not been answered here.

It is also a **specification decision, not a CAD one** — §4.5–4.6 currently
forbid it, and they would have to be amended first. **It is raised here, not
acted on.** The board-edge retention route remains fully viable if the answer
is no.
