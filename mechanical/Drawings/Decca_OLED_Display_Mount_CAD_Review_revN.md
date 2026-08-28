# Decca OLED Display Mount — CAD Build Review (Rev N)

Supersedes Rev M. Depth chain corrected from the measured screen recess.
Platform: Autodesk Fusion 360, script-generated parametric build.

---

## 1. The screen recess — corrected

You measured the glass sitting **1.50 mm** behind the flush seating face; it should be
0.30 mm (the §7 optical gap). That 1.20 mm error traces to a single wrong assumption.

I had `oled_glass_standoff` (0.60) + `oled_glass_t` (1.40) = **2.00 mm** of glass standing
proud of the PCB front face. Your measurement says it is actually **0.80 mm**. The front
plate was therefore 1.20 mm too thick and was holding the board that far back.

Those two guessed parameters are now replaced by one measurement-derived value,
`oled_glass_proud` = 0.80 mm, and the plate follows from it:

| | Before | **Rev N** |
|---|---:|---:|
| Glass proud of PCB face | 2.00 (assumed) | **0.80 (measured)** |
| Front plate thickness | 2.30 | **1.10 mm** |
| Glass front face | z −0.30 *modelled*, −1.50 *actual* | **z −0.30 actual** |
| Glass → Perspex | 0.30 | **0.300 mm** |

---

## 2. ⚠ Consequence: the solder tips now hit the Perspex

This is the thing to check before printing.

The front plate is the only thing standing between the header's solder tips and the
original Perspex. At 2.30 mm it swallowed them. At **1.10 mm it does not**.

Modelled at 2.00 mm proud, the tips now reach **0.90 mm past the seating face** and
strike the panel — verified, 2.91 mm³ of interference with the Perspex.

**The tips must be trimmed to under 1.10 mm proud**, or the carrier will not seat and the
whole assembly will sit skewed off the fascia.

This is not a design defect that can be engineered away. The chain is fixed:

```
glass to Perspex 0.30  +  glass proud of PCB 0.80  =  front plate 1.10
```

Anything on the PCB's front face taller than 1.10 mm collides with the panel. The only
alternatives are a thicker plate (which puts the screen back where it was) or trimming.
Trimming solder tips flush is normal practice and is the right answer here.

Measure yours before printing. If they cannot go below 1.10 mm, tell me and I will trade
some of the 0.30 mm optical gap back.

---

## 3. Knock-on: the snap pegs got shorter

A thinner front plate means less depth for the peg reliefs, so the springs are shorter.
Compensated by thinning the half-section (slot 0.70 → 1.00) and dropping the hook to
0.100 mm:

| | Wide end | Narrow end |
|---|---:|---:|
| Relief | 0.50 mm | **none** — the glass rear is now at the PCB face |
| Root | z −0.60 | z −1.10 |
| Free length | 2.60 mm | 2.10 mm |
| Hook | 0.100 mm | 0.100 mm |
| **Peak strain** | **2.00%** | **3.06%** |

Both within PETG, but the hooks are lighter than Rev M's 0.175 mm. **The retainer bar is
now the primary retention** and the pegs are mostly locating — which is the architecture
you proposed anyway.

All four hooks verified engaged.

One silver lining: **PCB datum bearing rises 86.7 → 97.4 mm²**, because the reliefs are
shallower and smaller.

---

## 4. Validation

| Pair | Result |
|---|---|
| Carrier × glass / active area / PCB / header / Perspex / bar | **all CLEAR** |
| Bar × glass / PCB / Perspex | **all CLEAR** |
| **Solder tips × Perspex** | **HIT — trim required (see §2)** |

| Check | Result |
|---|---:|
| Glass front face | z −0.300 (0.30 mm behind flush) |
| Glass → Perspex | 0.300 mm |
| All four snap hooks | ENGAGED |
| PCB datum bearing | 97.4 mm² |
| Seats on the Perspex plane | yes |
| Slivers | 0 on both parts |
| Carrier | 56.50 × 45.10 × 6.20 mm, 3.004 cm³ |
| Retainer bar | 38.65 × 6.00 × 3.05 mm, 0.705 cm³ |

---

## 5. Still open

1. **Solder tip length** — measure and trim to under 1.10 mm. Blocking.
2. **`oled_active_off_y` = 4.00 mm assumed** — light the display and report the offset.
3. **Glass thickness split** — modelled worst case (glass sitting straight on the PCB).
   Only affects the narrow peg relief, which is now zero anyway.
4. **Firmware must mask 2 pixel rows top and bottom.**
5. **Bezel retention is adhesive**; recessed pads provided. Bezel unchanged since Rev G.
