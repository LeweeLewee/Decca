# Decca OLED Display Mount — CAD Build Review (Rev F)

Supersedes Rev E. Aesthetic reshaping of the carrier; no functional change.
Platform: Autodesk Fusion 360, script-generated parametric build.

---

## 1. Change from Rev D — cable-tie anchor

### 1.1 Top leaf spring and its anchor legs — removed

Rev C added a leaf spring across the top edge, anchored by two legs at x ±16.40 to
±18.20 sitting **behind the PCB's top corners**. They cleared the PCB in the solid model
(nothing to report as interference) but they were rigid material lying across the
insertion path, so the board could not be pushed in past them at all.

That was a bad addition on my part: a retention feature that only works if the part can
be rotated in, placed at the same end as the locating posts that prevent rotation.
Deleted entirely. The top now carries **nothing but the two plain locating posts.**

### 1.2 Bottom rigid hooks — removed, sprung snap pegs restored and stiffened

The Rev C rigid retaining lips along the bottom edge did not work. Reverted to the Rev B
sprung concept, made materially stiffer rather than marginally so:

| | Rev B (broke) | **Rev D** |
|---|---:|---:|
| Shaft Ø | 2.70 | **2.80** |
| Slot width | 1.00 | **0.70** |
| Half-section thickness | 0.85 | **1.05** |
| Barb Ø / radial hook | 3.30 / 0.15 | **3.20 / 0.10** |
| Free flex length | ~3.0 | **3.10** |
| Peak bending strain | ~2.1% | **1.64%** |

Net effect: **1.88× the bending stiffness** at **0.67×** the deflection. The thicker
half-section also puts materially more material across the layer boundary at the root,
which is where the Rev B pegs actually failed.

The R0.80 root fillet is retained, built as primitive torus geometry so both pegs are
identical by construction, and contained inside a Ø4.80 × 1.00 counterbore relief so it
sits forward of the PCB datum and cannot lift the board.

### 1.3 Bezel locating lip — 0.70 → 2.80 mm

The Rev C lip engaged only 0.70 mm into a 3.00 mm panel and did not locate. Now
**2.80 mm**, so it passes almost fully through the Perspex.

**Not the full 3.00 mm, deliberately.** At 3.00 the lip's rear face would sit exactly
flush with the rear of the Perspex, and the OLED glass is only 0.30 mm behind that. With
±0.15 mm print tolerance a full-depth lip could stand proud of the panel and close on the
glass. At 2.80 the lip rear face sits at Z +0.20, giving **0.50 mm to the glass** and
still 93% engagement. Say the word if you want the full 3.00.

Bezel envelope grows to 40.00 × 20.30 × 4.00 mm as a result.

### 1.4 Carried forward from Rev C

- Fixing pitch **49.00** — confirmed correct on the Rev C print.
- Opening **35.20 × 15.30**, bezel lip envelope 34.90 × 15.00 (0.15 mm/side clearance).
- Header solder relief as a **full through-slot**, 16.00 × 6.50 mm.
- Carrier width 56.50 mm (derived; 0.50 mm outside §5's range, forced by the pitch).
### 1.5 Cable-tie anchor — redesigned for rear access (Rev E)

The Rev D anchor was two slots cut straight through the flange in Z. That face is the
Perspex seating plane, so the slots opened onto the panel with zero gap — no tie could
be threaded. The concept was unbuildable, not merely tight.

A first attempt at a stand-off bar failed too, and the validator caught it: the aperture
ran in Y, straight into the tray wall 0.25 mm beyond its exit. Blocked at one end.

**Final form:** two stand-off bar anchors on the flange's **rear** face, with the
aperture running in **X** so both ends open into free space.

| | |
|---|---:|
| Aperture | 3.70 (Y) × 1.60 (Z) mm |
| Tunnel length | 6.00 mm, at x ±5.0 to ±11.0 |
| Stand-off from flange face | 1.60 mm |
| Bar section | 1.40 mm |

Everything is behind the carrier; nothing depends on the Perspex-seating face, and the
tie never touches the original panel. Verified by sweeping a 3.5 × 1.4 mm tie section
along X with 6 mm overshoot at each end — **clear through both anchors**.

The flange grows from 3.00 to 7.00 mm tall to carry the anchors, taking the carrier to
45.10 mm overall height. Purpose is §9's optional strain relief: tie the I²C harness so
cable movement never loads the OLED's 4-pin header. Set `tie_flange_h` to zero to delete
the flange and both anchors together.

### 1.6 Carrier reshaped (Rev F)

The Rev E carrier was functionally sound but visually crude — plain rectangular slabs
butt-joined at hard 90° steps, with no blending or rhythm. Reshaped for appearance only.
Every change is built from primitives, so the geometry is deterministic and symmetric by
construction rather than dependent on feature-fillet luck.

| | Rev E | **Rev F** |
|---|---|---|
| Tray corner radius | R2.5 | **R4.0** |
| Boss arms | 12.00 mm rectangular slabs | **7.50 mm stadium bar**, ends R3.75 centred exactly on the bolts, tangent to the Ø7.50 bosses |
| Arm ↔ tray junction | hard step | **R2.50 concave blend** |
| Tie flange | 40.0 mm full-width plain rectangle | **27.0 mm wide, R3.0 corners** |
| Flange ↔ tray junction | hard step | **R2.50 concave blend** |
| Tie anchor bars | square blocks | **R0.80 rounded** |

The arm ends and the bosses now share a radius, so the mounting lug reads as one
continuous form instead of a slab with a cylinder stuck on it. Mass drops from 3.908 to
**3.448 cm³** — the part got lighter as well as better looking.

**Edge softening was only partly successful.** Fusion's chamfer failed on the whole-face
edge sets (`ASM_BL_UNFIN`) at both 0.50 and 0.30 mm. A per-edge fallback applied 31
chamfers at 0.30 mm; **49 edges remain crisp**. The dominant visual improvement is the
primitive-built shaping, which is unaffected, and the residual crisp edges are not
noticeable at this scale — but they are there, and a manual chamfer pass in Fusion would
finish the job if you want it perfect.

**Nothing functional moved.** Re-validated after reshaping: all interference pairs clear,
both tie paths clear, PCB insertion corridor still meets only the 0.43 mm³ snap hooks,
driver corridors clear, carrier still seats on the Perspex plane, PCB datum bearing
unchanged at 133.0 mm², glass-to-Perspex still 0.300 mm.

---

## 2. Validation

| Pair | Result |
|---|---|
| Carrier × PCB / glass / active area / header / solder tips / Perspex | **all CLEAR** |
| Bezel × Perspex / glass / active area / carrier | **all CLEAR** |
| Perspex × solder tips | CLEAR |

**Insertion path** — the PCB's solid area swept along the insertion axis, with the four
mounting holes excluded, meets **0.43 mm³** of carrier material: the two snap barbs'
0.10 mm hooks, and nothing else. The board goes straight in; only the intended snap
resists.

| Check | Result |
|---|---:|
| Glass → Perspex | 0.300 mm |
| Bezel lip → glass | 0.500 mm |
| Solder tips → carrier | 1.300 mm |
| Active-area centre vs opening | X +0.0000, Y +0.0000 |
| PCB datum bearing | 133.0 mm² |
| Snap hook engagement | both pegs engaged |

| Part | Envelope | Volume |
|---|---|---:|
| Front_Bezel | 40.00 × 20.30 × 4.00 mm | 0.465 cm³ |
| Rear_Display_Carrier | 56.50 × 45.10 × 6.20 mm | 3.448 cm³ |

Both closed manifold solids.

---

## 3. Still open

1. **`oled_active_off_y` = 4.00 mm, still assumed.** With this print, light the display
   and report how many mm high or low the lit area sits; add if high, subtract if low.
2. **Firmware must mask 2 pixel rows top and bottom.** The 15.30 mm opening leaves only
   0.60 mm total against a 14.70 mm active area; at 64 rows the bezel window has 0.10 mm
   per side, which is not viable. At 60 rows it becomes 0.56 mm per side.
3. **Solder tip length.** The front plate is 2.30 mm and seats on the Perspex, so tips
   longer than that will now reach the panel through the slot. Modelled at 2.00 mm.
4. **Top-edge retention.** Held by posts only; the snaps are at the bottom. If the top
   lifts, the top pair converts to snap pegs — a one-parameter change.

---

## 4. Print guidance

PETG / PETG-HF. Carrier: Perspex seating face down, no supports — both datums land in
flat layers and posts, pegs and bosses all print upward. Bezel: cosmetic face down; the
2.80 mm lip blocks print upward. 0.2 mm layers, 4 perimeters, ~40% infill.

Hardware: 2 × M2 heat-set insert (Ø3.2 × 4.0), 2 × M2 × 8 bolt, 1–2 cable ties.
