# Decca OLED Display Mount — CAD Build Review (Rev K)

Supersedes Rev J. Four sprung pegs; integrated cantilever removed; optional glued
retainer bar added as a separate part.
Platform: Autodesk Fusion 360, script-generated parametric build.

---

## 1. The integrated retaining lip is gone

You were right about the printing. The Rev J lip was a **26 mm bridge starting 3.90 mm up
with an unsupported underside** — it would have drooped, and a drooped spring is the wrong
shape in the one dimension that matters.

**There is now no cantilever, bridge or unsupported overhang anywhere in the carrier.**
The carrier also shrinks back from 48.35 to **45.10 mm** tall, because the lip's anchor
legs needed 3.25 mm of extra cavity that is no longer required.

---

## 2. Four sprung pegs — and a correction

**I told you four sprung pegs was impossible. That was wrong**, and the reason I gave was
wrong too. I said the Ø4.80 counterbore needs 2.40 mm of material all round and the narrow
end only has 0.70 mm to the window edge. But the counterbore is a *removal* — where it
overhangs the window there is simply nothing there to remove, and the peg's root support
is no worse than the plain posts you confirmed work.

**The real constraint is the glass, not the window.** The counterbore moves the peg root
*forward*, and at 1.00 mm deep the narrow-end root lands at z −1.30 — in front of the
glass rear face at z −1.70. That produced a genuine carrier-to-glass interference on the
first attempt at this revision, which the validator caught.

So the narrow pair use a shallower relief and a correspondingly smaller nose to keep the
strain sensible:

| | Wide end (header) | Narrow end |
|---|---:|---:|
| Shaft Ø / slot | 2.80 / 0.70 | 2.80 / 0.70 |
| Relief depth | 1.00 mm | **0.40 mm** |
| Root position | z −1.30 | **z −1.90** (0.20 mm clear of the glass) |
| Root fillet | R0.80 | **R0.35** |
| Nose Ø / hook | 3.35 / 0.175 mm | **3.20 / 0.100 mm** |
| Free flex length | 3.10 mm | 2.50 mm |
| **Peak strain** | **2.87%** | **2.52%** |

The pegs themselves are identical; only the pocket around them and the nose differ. All
**four hooks verified engaged**. Insertion corridor is now **1.57 mm³** — the four noses
and nothing else.

> The 0.20 mm glass clearance rests on `oled_glass_off_y` and `oled_glass_h`, both still
> assumed. If the glass sits higher than modelled, the narrow pegs foul it. This is the
> first feature in the design that depends on the glass position, and it is worth
> measuring before committing to a production print.

---

## 3. Optional glued retainer bar — separate part

A separate flat plate, printed on its own, glued on **after** the board is in.

| | |
|---|---:|
| Size | 29.85 × 3.40 × 2.70 mm |
| Volume | 0.140 cm³ |
| Overlap onto the PCB rear face | 0.80 mm |
| Attachment | 2 × Ø2.40 × 1.30 mm locating pins into Ø2.55 holes |
| Glue area | the 1.80 mm shelf across the end wall |

**Attachment points on the carrier:** the end wall is machined down to a shelf at exactly
the PCB rear plane, so the bar's face contacts the shelf and the board on the same plane
and presses the board flat. Two blind holes locate it.

**It prints flat on its PCB-contact face** — no overhang, no bridge, no support, and the
one surface that matters is the bed face.

Because it goes on after assembly it needs no lead-in ramp, which is what made the
integrated version awkward in the first place.

---

## 4. Validation

| Pair | Result |
|---|---|
| Carrier × glass / active area / PCB / solder tips (both ends) / header / Perspex / bezel / bar | **all CLEAR** |
| Bar × glass / Perspex / PCB | **all CLEAR** (face contact only, no overlap) |

| Check | Result |
|---|---:|
| All four snap hooks | **ENGAGED** |
| Insertion corridor | 1.57 mm³ — four noses only |
| Glass → Perspex | 0.300 mm |
| PCB datum bearing | **86.7 mm²** (Rev J 93.0 — the two narrow reliefs cost 6.3) |
| Both cable-tie paths | CLEAR |
| Seats on the Perspex plane | yes |
| Slivers | **0** on both parts |
| Carrier | 56.50 × 45.10 × 6.20 mm, 3.232 cm³, solid |

---

## 5. Print and assembly

PETG / PETG-HF, 0.2 mm layers, 4 perimeters, ~40% infill.

- **Carrier** — Perspex seating face down. No supports.
- **Retainer bar** — PCB-contact face down. No supports.
- **Bezel** — cosmetic face down. Unchanged since Rev G.

Assembly: press the board in until all four pegs snap. If that holds well enough, stop —
the bar is optional. If you want belt and braces, drop the bar onto its two pins with a
little glue on the shelf.

---

## 6. Still open

1. **`oled_active_off_y` = 4.00 mm assumed** — light the display and report the offset.
2. **Glass position** now matters (see §2) — worth measuring.
3. **Firmware must mask 2 pixel rows top and bottom.**
4. **Bezel retention is adhesive**; recessed pads provided.
5. Snap force: `snap_barb_d` / `snap_barb_d_n` if grip is wrong either way.
