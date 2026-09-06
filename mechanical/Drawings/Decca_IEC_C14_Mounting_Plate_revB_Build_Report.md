# Decca IEC C14 Mounting Plate Rev B — CAD Build Report

**Status:** CAD PASS / prototype pending  
**Supersedes:** Rev A, rejected for incorrect rectangular inlet opening  
**Build date:** 2026-09-06

## 1. Correction made

Rev A used the 27.14 × 19.50 mm measured inlet envelope only to create a rectangular clearance opening. Physical review showed that this did not properly enclose the actual C14 profile.

Rev B promotes the owner-supplied **16.00 mm** and **14.00 mm** readings to governing profile datums and reconstructs the actual six-sided form.

Native profile:

- long flat / overall width **27.14 mm**;
- overall height **19.50 mm**;
- short flat **16.00 mm**;
- straight side **14.00 mm**;
- long-flat corners **R2.00**;
- other four corners **R0.40**.

Derived angled section per side:

- run **5.57 mm**;
- rise **5.50 mm**;
- diagonal length **7.828 mm**;
- native angle **44.638°**.

The production opening is the measured profile offset outward by **0.25 mm normal clearance**, then rotated 90° into the existing plate layout. Cut-out radii therefore become **R2.25** and **R0.65**.

## 2. Unchanged interfaces

- plate **40.00 × 50.00 × 3.00 mm**, R2 corners;
- four Decca holes Ø2.40 at `(±15.50, ±8.50)`, exact 31.00 × 17.00 grid;
- two C14 fixing holes Ø3.40 at `(0, ±19.50)`, exact 39.00 pitch.

## 3. Generated files

- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revB_cadquery.py`
- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revB_verify.py`
- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revB_drawing.py`
- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revB.step`
- `mechanical/STL/Decca_IEC_C14_Mounting_Plate_revB.stl`
- `mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_revB_views.png`

## 4. Exported-geometry validation

Independent STEP/STL verification results:

| Gate | Result | Evidence |
|---|---|---|
| Plate envelope | **PASS** | 40.000000 × 50.000000 × 3.000000 mm |
| One connected STEP solid | **PASS** | 1 solid |
| Correct profile topology | **PASS** | 6 straight edges + 6 circular arcs |
| Rotated profile envelope | **PASS** | 20.000000 × 27.640000 mm |
| Cut-out corner radii | **PASS** | 2 × R2.25, 4 × R0.65 |
| Angled sections | **PASS** | two equal lines; native 44.637701°, rotated 45.362299° |
| M2 pattern | **PASS** | `(±15.5, ±8.5)` |
| M3 pattern | **PASS** | `(0, ±19.5)`, 39.00 mm pitch |
| No opening/fixing intersection | **PASS** | minimum edge gap 3.980000 mm |
| Minimum ligament ≥3 mm | **PASS** | M2 min 4.300000; M3 min 3.980000 mm |
| STL envelope | **PASS** | 40 × 50 × 3 mm |
| STL manifold | **PASS** | watertight and winding-consistent |
| STL body count | **PASS** | 1 |
| Hidden/support features | **PASS** | none; broad-face no-support print |

STEP volume: **4325.997401 mm³**  
STL volume: **4326.486776 mm³**

## 5. Local build checksums

- CadQuery source: `f250960907e469c918e4fdcedf5afdaacd5c5fa8030b11cbf4834b3f000ce201`
- STEP: `a60416c8fb1f53fdb350dbb5a650b5539423d824014c4a421353b48734b1580e`
- STL: `f8f2b5cd85442c2af8480e3f829a39a151d1d11ab3b5c1a89496b39c6e7720e2`

## 6. Physical gate

Rev B is **not released** until a printed part confirms the actual socket profile is enclosed correctly, both M3 fixings and four M2 cabinet fixings align without forcing, the plate clamps flat and rear mains-terminal clearance is acceptable.
