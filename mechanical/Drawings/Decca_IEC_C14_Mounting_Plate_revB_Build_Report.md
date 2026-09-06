# Decca IEC C14 Mounting Plate Rev B — CAD Build Report

**Status:** CAD PASS / profile geometry owner-confirmed / printed fit pending  
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

## 4. Clean exported-geometry validation

The committed Rev B source was rebuilt in GitHub Actions using CadQuery 2.8.0. The generated STEP and STL were then independently verified.

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
| Hidden fastening features | **PASS** | none |
| Support-dependent geometry | **PASS** | none; broad-face no-support print |

**Result: 15/15 Rev B CAD checks PASS.**

STEP volume: **4325.997401 mm³**  
STL volume: **4326.486776 mm³**

## 5. Clean-build checksums

- CadQuery source: `9059de6e1bbab96b47661f52f4956d324f0525bc6c3a7dd28f094467b303c1b3`
- STEP: `88490a052b2ffc9eee2647a45866b8bced727ce17cc5107601133e631fd2de1e`
- STL: `f8f2b5cd85442c2af8480e3f829a39a151d1d11ab3b5c1a89496b39c6e7720e2`

## 6. Owner profile-geometry confirmation — 2026-09-06

The owner reviewed the Rev B profile drawing and **confirmed that the six-sided outline, calculated angled sections and corner treatment match the intended IEC C14 socket geometry**.

This closes the **profile-definition/design-intent gate** that caused Rev A to fail.

It does **not** constitute full physical release because the Rev B part has not yet been printed and fitted. The remaining release gate is the actual printed-part test below.

## 7. Physical release gate

Rev B is **not released** until a printed part confirms:

1. the complete C14 profile enters without forcing and the plate visibly encloses the socket profile as intended;
2. both M3 fixings align without slotting;
3. all four Decca M2 holes align without forcing;
4. the plate clamps flat without cracking or distortion;
5. rear terminal and wire clearance is acceptable before mains energisation.

If Rev B fails, record the failed physical interface and amend the measured-profile model. Do not file, slot or drill the reference part to make a failure appear to pass.
