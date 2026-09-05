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
> **That gate is not satisfied.** This document is what has to be measured to
> open it. No replacement production geometry has been created.

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
| Actual PCB length and width | 66 × 63 mm | supplier-stated **reference only** |
| PCB thickness | 1.60 mm | **assumed** |
| Lowest underside feature | 2.50 mm below the PCB | **assumed** |
| Terminal-block height and depth | 10.00 mm / 8.00 mm | **assumed** |
| Terminal-mouth centre height from the lowest datum | — | **absent from the model entirely** |
| Terminal-mouth opening | — | **absent from the model entirely** |
| Usable conductor insertion depth | — | **absent from the model entirely** |
| Terminal pitch and exact positions | 3.50 mm pitch, span derived | **assumed** |
| Practical wire and ferrule envelope | 2.00 mm conductor Ø | **assumed** |
| Mounting-hole diameter and centres | — | **absent** |
| USB connector position | DevKit starting values | **assumed** |
| Component-free PCB-edge regions | 3.00 mm short / 2.50 mm long | **assumed** |
| **Complete assembly height** | **20.00 mm overall** | ✅ **MEASURED 2026-09-05** |

**One of thirteen is closed.** The four marked ★ in §4 below are the ones that
block the architecture, not merely the detail.

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
| **M1** | Terminal-mouth **centre height** | Datum A | callipers / depth gauge | v1.5 §5.2–5.3, gates 7–9 |
| **M2** | Terminal-mouth **opening**, width × height of the hole itself | — | callipers or pin gauges | wire + ferrule envelope, gate 9 |
| **M3** | **Usable insertion depth** — outward mouth face to the internal stop, with the screw backed off | mouth face | depth gauge or a marked wire | declared straight insertion length, gate 8 |
| **M4** | Terminal-block **outward face position**: is it flush with the PCB edge, proud of it, or set inboard — and by how much? | Datum C | callipers | whether the base wall can exist at all on the long sides |
| M5 | Terminal **pitch**, and centre of terminal 1 | Datum B | callipers over a known span (measure 1→15 and divide) | terminal positions, gate 28 |
| M6 | Terminal-block **height** (top face) and **depth** inboard | Datum A / Datum C | callipers | screw access, gate 6 |
| M7 | Screw **drive type and head size**, and how far the screw head sits below the block top face | Datum A | callipers | screwdriver corridor, gate 6 |

### Group 2 — board outline and vertical stack

| ID | Measure | From | Feeds |
|---|---|---|---|
| M8 | PCB **length** and **width** — confirm or correct the supplier's 66 × 63 | edge to edge | plan envelope, ledge and clamp |
| M9 | PCB **thickness** | — | retention, §3 |
| M10 | **What actually touches the table**, and the height of the **PCB underside** above Datum A | Datum A | floor clearance, gate 3 |
| M11 | **PCB top face** height | Datum A | all internal chains |
| M12 | **Which feature is the highest point** of the 20.00 mm assembly | — | confirms how the closed 20.00 mm is applied |
| M13 | Does **anything overhang** the PCB outline — terminal blocks, sockets, the USB shell? Where, and by how much? | Datum B / C | true plan envelope |

### Group 3 — fixings, USB and clear regions

| ID | Measure | From | Feeds |
|---|---|---|---|
| M14 | **Mounting-hole** diameter and each hole centre | Datum B and C | whether hole-based retention is even an option |
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

If time is short, **M1, M2, M3, M4** alone let the long-side architecture be
laid out and the base wall height fixed. **M8, M10, M11** then allow a complete
base. Everything else refines detail that can be parameterised in the meantime.

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
