# Decca IEC C14 Mounting Plate — Rev A Specification

> **REJECTED 2026-09-06:** Physical review showed that the rectangular Rev A opening does not properly enclose the IEC C14 profile. **Do not build or install Rev A.** The controlling design is now `Decca_IEC_C14_Mounting_Plate_Spec_revB.md`.

**Status:** design inputs locked; ready for CAD build  
**Scope:** mechanical mounting plate only  
**Branch:** `feat/iec-c14-mounting-plate`

## 1. Purpose

Create a compact 3D-printed mounting plate for the purchased IEC C14 panel-mount mains inlet. The plate attaches to the Decca cabinet using the existing four-hole interface and carries the C14 inlet on its own two M3 fixings.

This part is a **mechanical carrier only**. It is not relied upon as primary electrical insulation, strain relief or mains protection.

## 2. Locked measured interfaces

### 2.1 Decca cabinet interface

- 4 × M2 fixing bolts.
- Rectangular fixing grid: **31.00 mm × 17.00 mm centre-to-centre**.
- All four hole centres are symmetric about the plate centre.

Using the plate centre as `(X,Y) = (0,0)`:

| Hole | X (mm) | Y (mm) |
|---|---:|---:|
| D1 | -15.50 | -8.50 |
| D2 | +15.50 | -8.50 |
| D3 | -15.50 | +8.50 |
| D4 | +15.50 | +8.50 |

### 2.2 IEC C14 inlet interface

Physical measurements supplied from the purchased inlet:

- Main body width: **27.14 mm**.
- Main body height: **19.50 mm**.
- 2 × M3 fixing holes.
- M3 fixing-hole spacing: **39.00 mm centre-to-centre**.
- Additional measured reference dimensions from the supplied photographs: **16.00 mm** and **14.00 mm**. Their exact feature datums are not required for the front plate geometry and must not be inferred or used to alter the mounting interface without a new physical measurement.

The inlet is rotated **90° in the plate** relative to the measured 27.14 × 19.50 body orientation. This gives better separation between the C14 cut-out and the four Decca M2 fixings.

The C14 fixing pair is centred on **both plate axes**. Its midpoint is exactly `(0,0)`:

| Hole | X (mm) | Y (mm) |
|---|---:|---:|
| C1 | 0.00 | -19.50 |
| C2 | 0.00 | +19.50 |

The spacing between C1 and C2 is exactly **39.00 mm**.

## 3. Rev A production geometry

### 3.1 Plate envelope

- Width: **40.00 mm**.
- Height: **50.00 mm**.
- Thickness: **3.00 mm**.
- Plate centred on `(0,0)`.
- Recommended outer corner radius: **R2.00 mm**.
- No countersinks or counterbores in Rev A.

The earlier 36 × 45 mm concept is superseded before CAD release. At 36 × 45 mm it left only about **1.3 mm of material outside the M2/M3 hole edges**, which is unnecessarily fragile for an FDM mains-inlet carrier. The 40 × 50 mm envelope keeps the design compact while increasing the edge ligament materially.

Nominal edge material with the specified hole clearances:

- Decca M2 side holes: approximately **3.3 mm** from hole edge to plate side.
- C14 M3 end holes: approximately **3.8 mm** from hole edge to plate top/bottom.

### 3.2 C14 body cut-out

Because the inlet is rotated 90°:

- Cut-out width in plate X: **20.00 mm**.
- Cut-out height in plate Y: **27.60 mm**.
- Cut-out centred at `(0,0)`.

This corresponds to the measured 19.50 × 27.14 mm rotated body envelope and gives approximately:

- **0.25 mm clearance per side** in X.
- **0.23 mm clearance per side** in Y.

The cut-out shall be a true clear rectangle. Do not add an internal corner radius that intrudes into the 20.00 × 27.60 mm clearance envelope. Small external corner relief beyond that rectangle is acceptable only if required by the modelling kernel or print process.

### 3.3 Through-hole sizes

- 4 × Decca fixing holes: **Ø2.40 mm through** for M2 clearance.
- 2 × C14 fixing holes: **Ø3.40 mm through** for M3 clearance.

Hole coordinates are fixed by sections 2.1 and 2.2. Do not move any hole to compensate for print shrinkage; tune only the clearance diameters if a physical print demonstrates the need.

### 3.4 Edge treatment

- Break exposed plate edges with approximately **0.5 mm** chamfer or equivalent small fillet where this does not affect mounting faces.
- Keep both mounting faces planar.
- No decorative ribs, bosses or external structures are required.

## 4. Structural intent

The design should remain deliberately simple:

- one flat connected solid;
- no supports required when printed flat;
- no heat-set inserts;
- no captive nuts;
- no unnecessary thickening or reinforcement;
- loads transfer directly through ordinary M2 and M3 bolt heads/washers into the 3.00 mm plate.

The minimum local material between any fixing hole and the C14 cut-out must remain at least **3.0 mm after subtracting the hole radius**. The nominal Rev A layout exceeds this.

## 5. Print recommendation

For the prototype/release print:

- Material: **PETG minimum; flame-retardant PETG/PC preferred** for a mains-adjacent part.
- Colour: black unless the installed finish requires otherwise.
- Layer height: approximately **0.20 mm**.
- Perimeters: **4 or more**.
- Infill: **100%** for this small part.
- Orientation: broad face flat on the bed.
- Supports: none.

Do not treat ordinary printed thermoplastic as an electrical barrier. Rear mains terminals must remain properly insulated/shrouded and mechanically protected by the electrical assembly design.

## 6. CAD and validation gates

The CAD build must prove all of the following before an STL is described as print-ready:

1. Plate envelope = **40.00 × 50.00 × 3.00 mm**.
2. One connected manifold solid.
3. Four M2 centres form an exact **31.00 × 17.00 mm** symmetric grid.
4. Two M3 centres are exactly **39.00 mm** apart.
5. M3 pair midpoint is exactly at `(0,0)`.
6. C14 cut-out is exactly centred at `(0,0)`.
7. C14 cut-out clear size is at least **20.00 × 27.60 mm** everywhere through the plate.
8. M2 holes are Ø2.40 mm through; M3 holes are Ø3.40 mm through.
9. No fixing hole intersects the C14 cut-out.
10. Minimum local ligament from fixing-hole edge to C14 cut-out is at least **3.0 mm**.
11. No countersinks, heat-set pockets or hidden fastening features are present.
12. Flat-bed print needs no support geometry.

## 7. Required deliverables

Use the existing mechanical repository structure.

Minimum release artefacts:

- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA_fusion.py` — parametric generator or equivalent reproducible source.
- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA.step` — neutral CAD.
- `mechanical/STL/Decca_IEC_C14_Mounting_Plate_revA.stl` — print mesh.
- `mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_revA_Build_Report.md` — dimensions and validation results.
- At least one dimensioned or orthographic PNG in `mechanical/Drawings/` showing the hole pattern and cut-out.

If Fusion 360 is available, also save the native `.f3d`. If it is not, do not fabricate an `.f3d`; the reproducible source + STEP + STL are sufficient.

## 8. Physical release check

Before final sign-off:

1. Offer the bare C14 inlet through the printed opening without forcing.
2. Confirm both M3 bolts pass through freely and the 39 mm pair aligns without slotting.
3. Confirm all four Decca M2 holes align with the existing **31 × 17 mm** cabinet grid without forcing.
4. Tighten only enough to verify the plate clamps flat with no cracking or visible distortion.
5. Confirm rear terminal and wire clearance separately before mains wiring is energised.

Any geometry change following a failed fit must be based on a new physical measurement and recorded in the build report.