# Decca IEC C14 Mounting Plate — Rev B Specification

**Status:** corrected design inputs locked; CAD built / physical fit pending  
**Scope:** mechanical mounting plate only  
**Branch:** `feat/iec-c14-mounting-plate`

## 1. Rev A disposition

Rev A is **rejected** following owner physical review on 2026-09-06. Its 20.00 × 27.60 mm rectangular opening reproduced only the bounding clearance around the inlet and did not properly enclose the actual IEC C14 body profile. Rev A must not be released, installed or modified into service.

Rev B replaces only the inlet opening geometry. The plate envelope and Decca/C14 fixing datums remain unchanged.

## 2. Locked plate and fixing geometry

- Plate: **40.00 × 50.00 × 3.00 mm**, centred on `(0,0)`.
- Outer corners: **R2.00 mm**.
- Decca fixing holes: 4 × **Ø2.40 mm through** at `(±15.50, ±8.50)`; exact **31.00 × 17.00 mm** grid.
- C14 fixing holes: 2 × **Ø3.40 mm through** at `(0.00, ±19.50)`; exact **39.00 mm** pitch, midpoint `(0,0)`.

## 3. Measured C14 body/profile geometry

The actual purchased inlet profile is modelled from the owner-supplied measurements, in the inlet's native orientation before plate rotation:

- overall width / long flat: **27.14 mm**;
- overall height: **19.50 mm**;
- opposite short flat: **16.00 mm**;
- straight vertical side before each angled section: **14.00 mm**;
- the two corners at the ends of the long flat: **R2.00 mm**;
- the other four corners: **R0.40 mm**.

The 16.00 mm and 14.00 mm measurements are **governing profile datums in Rev B**. Rev A incorrectly treated them as non-governing.

### 3.1 Derived angled sections

With a symmetric profile:

- horizontal run of each angle = `(27.14 - 16.00) / 2` = **5.57 mm**;
- vertical rise of each angle = `19.50 - 14.00` = **5.50 mm**;
- diagonal length = `sqrt(5.57² + 5.50²)` = **7.828 mm**;
- native angle to the short/long flat = `atan(5.50 / 5.57)` = **44.638°**.

This is intentionally calculated from the measured datums rather than replaced with an assumed 45°.

## 4. Production cut-out

The plate opening shall follow the complete six-sided rounded C14 profile, not its rectangular bounding box.

- Normal profile clearance: **0.25 mm outward** around the measured profile.
- Therefore production cut-out corner radii are:
  - long-flat corners: **R2.25 mm**;
  - other four corners: **R0.65 mm**.
- The resulting clear bounding envelope before rotation is **27.64 × 20.00 mm**.
- The inlet profile is rotated **90°** in the plate, so the installed clear bounding envelope is **20.00 mm X × 27.64 mm Y**.
- The actual opening remains the six-sided profile with two calculated angled sides. Do not replace it with a 20.00 × 27.64 rectangle.

The CAD uses a +90° rotation, placing the long flat on plate `X = -10.00 mm`. Because the plate and fixing patterns are 180° symmetric, the complete plate can be installed rotated 180° if the opposite inlet orientation is preferred without changing geometry.

## 5. Structural checks

Exact exported-geometry measurements for Rev B are:

- minimum C14-profile-to-M2 hole-edge ligament: **4.30 mm**;
- minimum C14-profile-to-M3 hole-edge ligament: **3.98 mm**.

Both exceed the **3.0 mm** minimum requirement.

## 6. CAD validation gates

Before Rev B is print-ready, verify from the exported STEP/STL:

1. plate envelope = **40.00 × 50.00 × 3.00 mm**;
2. one connected manifold solid;
3. cut-out is a six-line / six-arc rounded profile, not a rectangle;
4. cut-out clear bounding envelope after rotation = **20.00 × 27.64 mm**;
5. profile has exactly two **R2.25** cut-out corners and four **R0.65** cut-out corners;
6. two diagonal sides retain the calculated native **44.638°** geometry;
7. M2 centres remain exact **31.00 × 17.00 mm** grid;
8. M3 centres remain exact **39.00 mm** pitch and midpoint `(0,0)`;
9. M2 holes remain Ø2.40 mm through and M3 holes Ø3.40 mm through;
10. no fixing hole intersects the C14 opening;
11. minimum fixing-hole edge to C14 profile ligament ≥ **3.0 mm**;
12. STL is watertight, winding-consistent and one body;
13. no countersinks, pockets, ribs, bosses, inserts or hidden fastening features;
14. broad-face print requires no support geometry.

## 7. Physical release gate

Rev B remains **prototype pending** until the owner confirms:

1. the complete C14 profile enters the opening without forcing and the plate visibly encloses the socket profile as intended;
2. both M3 fixings align without slotting;
3. all four Decca M2 holes align without forcing;
4. the plate clamps flat without cracking/distortion;
5. rear terminal and wire clearance is confirmed before mains energisation.
