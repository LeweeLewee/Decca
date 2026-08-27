# Decca OLED Display Mount — CAD Build Review (Rev C)

Supersedes Rev B. Built from `Decca_OLED_Display_Mount_Spec_v1.0.md` plus corrections
measured off the Rev B printed prototype.
Platform: Autodesk Fusion 360, script-generated parametric build.

---

## 1. What changed from Rev B, and why

### 1.1 Panel geometry corrected from the prototype

Two of the spec's §2 "locked" interface dimensions were wrong on the real fascia:

| Parameter | Spec v1.0 | **Measured** | Consequence |
|---|---:|---:|---|
| `panel_fix_pitch` | 48.00 | **49.00** | Bosses moved to ±24.50; carrier width grows to 56.50 mm |
| `panel_open_w` | 35.50 | **35.20** | Bezel lip resized |
| `panel_open_h` | 15.80 | **15.30** | Bezel lip resized; **vertical budget now critical — see §3** |

`carrier_w` is now **derived** as `panel_fix_pitch + boss_od` = 56.50 mm, so the arms
always terminate tangent to the bosses. This is 0.50 mm outside §5's stated 54–56 mm
range — a deviation forced by the corrected fixing pitch, not a free choice.

### 1.2 Root cause of "screen does not seat flush" — corrected

The 4-pin header is soldered from the component side, and its pin tails leave **pointed
solder protrusions on the display side** of the PCB. Rev B did allow for these, but only
as a **0.60 mm deep pocket**. The real protrusions stand well over 0.60 mm proud, so they
bottomed out on the pocket floor and held the PCB off its datum — which is exactly the
symptom seen: PCB tilted, glass not parallel to the fascia.

**Fix:** the relief is now a **full through-slot** in the front plate, 16.00 × 6.50 mm,
so protrusion height cannot foul the seat at any length up to the plate thickness.

The slot sits at y −21.25 to −16.25, entirely outside the 15.30 mm fascia opening, so it
is invisible from the front. 1.80 mm of plate remains between the slot and the display
window.

> **Check before assembly:** the front plate is 2.30 mm thick, and the carrier's front
> face seats directly on the Perspex. Solder tips longer than **2.30 mm** will now pass
> through the slot and touch the original Perspex. Modelled at 2.00 mm, giving 0.30 mm
> headroom. If yours are longer, trim them flush-ish rather than letting them bear on
> the panel.

### 1.3 Snap pegs replaced

The Rev B split snap pegs broke. The cause is orientation, not just size: printed with
the seating face down, each peg half was a ~0.85 mm crescent whose root sat on a layer
boundary and was loaded in bending — the worst case for FDM. Making them thicker would
only have delayed the failure.

Rev C removes all springy round features:

- **Four plain locating posts**, Ø2.70, in the original (confirmed correct) hole
  positions. Top pair stands 0.50 mm proud of the PCB rear face; bottom pair engages
  1.20 mm so the board can be rotated in. No splits, no barbs.
- **Two rigid retention hooks** along the bottom edge at x ±11.00, clear of the header,
  overlapping the PCB rear face by 0.70 mm.
- **One leaf spring across the top**, 32.8 mm span, 1.20 mm thick, 0.80 mm overlap.
  Double-anchored so it bends *within* the layer plane rather than across it, with a
  1.10 mm flex gap behind it. Peak bending strain ≈ 0.5%, well inside PETG.

Assembly: engage the bottom edge under the two hooks, rotate the top down onto the
posts, and the top spring snaps over the PCB's top edge. To remove, lever the spring
back with a small screwdriver.

### 1.4 Bezel resized to the real opening

Lip envelope is now **34.90 × 15.00** in a 35.20 × 15.30 opening — 0.15 mm clearance per
side, versus Rev B's 0.20 mm *interference* in height, which is why it would not fit.
Lip corner blocks narrowed to 2.20 mm so they clear the window aperture.

---

## 2. Validation (final Rev C model)

| Pair | Result |
|---|---|
| Carrier × solder tips | **CLEAR** (1.300 mm) |
| Carrier × OLED glass | CLEAR |
| Carrier × active area | CLEAR |
| Carrier × OLED PCB | CLEAR |
| Carrier × header keep-out | CLEAR |
| Carrier × Perspex | CLEAR |
| Perspex × solder tips | CLEAR |
| Bezel × Perspex / glass / carrier | CLEAR |

| Check | Result |
|---|---:|
| OLED glass → Perspex rear face | **0.300 mm** |
| Active-area centre vs opening centre | X +0.0000, Y +0.0000 |
| PCB datum bearing area | 148.4 mm² |
| Bezel lip clearance in opening | 0.15 mm / side |

| Part | Envelope | Volume |
|---|---|---:|
| Front_Bezel | 40.00 × 20.30 × 1.90 mm | 0.424 cm³ |
| Rear_Display_Carrier | 56.50 × 42.10 × 5.60 mm | 3.296 cm³ |

Both closed manifold solids.

---

## 3. Vertical budget — needs a firmware change

The corrected 15.30 mm opening leaves only **0.60 mm total** between the opening and the
14.70 mm active area. Splitting that between bezel overlap and display clearance:

| Bezel window | Overlap onto opening | Clearance to lit area (64 rows) |
|---:|---:|---:|
| 14.90 (Rev C) | 0.20 / side | **0.10 / side — not viable** |

**Mask 2 pixel rows top and bottom** (60 of 64 used). Lit height becomes 13.78 mm and
clearance rises to **0.56 mm per side**, with the 0.20 mm bezel overlap retained. Four
rows is a cheap price for a workable tolerance, and it is the only way to make the bezel
overlap the opening edge at all with the true opening size.

---

## 4. Still assumed — unchanged from Rev B

| Parameter | Used | Status |
|---|---:|---|
| `oled_active_off_y` | 4.00 mm | **ASSUMED** — sets vertical centring |
| `oled_glass_standoff` | 0.60 mm | ASSUMED — feeds the 0.30 mm optical gap |
| `oled_glass_w/h` | 34.50 × 23.00 | ASSUMED — sizes the clearance window |
| `oled_hole_pitch_x` | 30.00 mm | Prototype-confirmed as correct |

`oled_active_off_y` is still the one to settle. With the Rev C print, light the display
and report how many mm high or low the lit area sits in the opening; add that to the
parameter if high, subtract if low.

---

## 5. Print guidance

- PETG / PETG-HF.
- **Carrier:** Perspex seating face down on the bed. Both datums land in flat layers;
  posts, hooks, bosses and the leaf spring all print upward. No supports.
  The leaf spring and hooks are short unsupported ledges off a wall — expect a little
  droop on the first layer of each; it is not a fit surface.
- **Bezel:** cosmetic face down. Watch elephant's foot on the R0.4 front edge.
- 0.2 mm layers, 4 perimeters, ~40% infill.

**Hardware:** 2 × M2 heat-set insert (Ø3.2 × 4.0), 2 × M2 × 8 bolt, 1–2 cable ties.

---

## 6. What to check on the Rev C print

1. Does the PCB now seat flat? (the through-slot fix)
2. Bezel drop-in fit in the opening — should be loose, 0.15 mm per side.
3. Leaf spring: enough grip, and does it survive being levered back?
4. Vertical centring of the lit area → the `oled_active_off_y` number.
5. Solder tips: do any touch the Perspex through the slot?
