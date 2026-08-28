# Decca OLED Display Mount — CAD Build Review (Rev H)

Supersedes Rev G. Retention strengthened at both ends.
Platform: Autodesk Fusion 360, script-generated parametric build.

---

## 1. Solder pin interference

The part in your photo is **Rev F**, where the through cut-out was on the *opposite* edge
from the header — so the pins sat over a 0.60 mm shallow recess and bottomed out. That is
exactly the section you cut away by hand.

**Rev G already moved it**, and Rev H keeps it: full through cut-out, **16.00 mm wide**,
on the header edge, spanning from the PCB edge **6.30 mm inboard**. The header row is only
7.62 mm across and sits ~2.20 mm from the edge, so there is ample margin.

I briefly took the cut-out to 20.00 mm as insurance and reverted it — width was never the
problem, and the extra 4 mm cost 13 mm² of PCB bearing for nothing.

Solder tips modelled 2.00 mm proud verify **CLEAR** of the carrier.

---

## 2. Retention

### 2.1 Thicker nose on the sprung pegs

| | Rev G | **Rev H** |
|---|---:|---:|
| Barb Ø | 3.20 | **3.35** |
| Radial hook | 0.100 | **0.175 mm** |
| Peak bending strain | 1.64% | **2.87%** |

75% more grip, still comfortably inside PETG. Room to go further to Ø3.40 (0.20 mm hook,
3.3% strain) if it still feels light.

### 2.2 All four sprung is not possible — here is why

I tried. The two holes at the narrow end sit **0.70 mm** from the display window edge.

A durable sprung peg needs the Ø4.80 counterbore relief that lets its root fillet sit
*forward* of the PCB datum — without it, a root fillet lifts the board off its datum (the
Rev C fault) and pushes the glass into the Perspex. That relief needs 2.40 mm of radius
around the hole. There is 0.70 mm.

Building the peg without the relief gives a **short, unfilleted** peg:

| | Wide-end peg | Narrow-end peg (no relief) |
|---|---:|---:|
| Free flex length | 3.10 mm | **2.10 mm** |
| Peak strain at 0.175 hook | 2.87% | **6.25%** |

6.25% is past PETG yield. That is the Rev B geometry that snapped, and it would snap
again. So the answer is not four identical pegs.

### 2.3 What replaces it — a sprung retaining lip

A single leaf spring across the narrow end, retaining the board where a peg cannot:

| | |
|---|---:|
| Span | 26.00 mm |
| Section | 1.20 mm thick × 1.50 mm |
| Overlap onto the PCB rear face | 0.80 mm |
| Flex gap behind it | 3.30 mm |
| Peak strain at full deflection | **0.85%** |

**Why this does not repeat the Rev C failure.** In Rev C the spring's anchor legs sat
rigidly behind the PCB's corners, inside the insertion path, and the board could not go in
at all. Here the legs sit at y +13.05…+16.50 against a PCB edge at +12.75 — **entirely
outside the PCB footprint**. Only the sprung lip itself overlaps, and it is meant to
deflect.

Verified with the insertion-corridor sweep: the PCB's solid area swept in, mounting holes
excluded, meets **32.31 mm³** of carrier — the two snap noses and the sprung lip, and
nothing else. Every obstruction in the path is a spring.

**Result: retention at both ends** — two sprung pegs with a thicker nose at the header
end, one sprung lip at the far end, plus the two plain posts still locating.

---

## 3. Validation

| Pair | Result |
|---|---|
| Carrier × glass / active area / PCB / solder tips / header / Perspex / bezel | **all CLEAR** |

| Check | Result |
|---|---:|
| Glass → Perspex | 0.300 mm |
| PCB datum bearing | 99.4 mm² |
| Insertion corridor | sprung features only |
| Both cable-tie paths | CLEAR |
| Seats on the Perspex plane | yes |
| Carrier | 56.50 × 48.35 × 6.20 mm, 3.836 cm³, solid |

**Sliver audit:** the 0.05 and 0.10 mm crescents from the stadium clamp and the flange
blend are gone. Four 0.1500 mm edges remain — these are the *deliberate* 0.15 mm merge
overlap where the lip enters its legs, not boolean artifacts, and they sit below one
extrusion width so they will not print.

---

## 4. Still open

1. **`oled_active_off_y` = 4.00 mm is still assumed.** Light the display and report how
   many mm high or low the lit area sits.
2. **Firmware must mask 2 pixel rows top and bottom.**
3. **Bezel retention is adhesive** — mechanical clipping is blocked by the glass. Recessed
   pads are provided. The alternative is clamping the bezel under the M2 bolt heads, which
   breaks §4 and §12.
4. **Snap force** — if the 0.175 mm hook still feels light, `snap_barb_d` goes to 3.40.
5. **Lip force** — if the lip is too stiff to fit the board past, drop `lip_overlap` from
   0.80; if too weak, raise `lip_t` from 1.20.

---

## 5. Print guidance

PETG / PETG-HF. Carrier: Perspex seating face down, no supports. Bezel: cosmetic face down.
0.2 mm layers, 4 perimeters, ~40% infill.

Hardware: 2 × M2 heat-set insert (Ø3.2 × 4.0), 2 × M2 × 8 bolt, 1–2 cable ties, thin
removable double-sided strip for the bezel.
