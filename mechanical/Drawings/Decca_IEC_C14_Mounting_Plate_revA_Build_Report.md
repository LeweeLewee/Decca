# Decca IEC C14 Mounting Plate Rev A — CAD Build Report

**Status:** CAD complete / prototype pending  
**Controlling specification:** `Decca_IEC_C14_Mounting_Plate_Spec_revA.md`  
**Branch:** `feat/iec-c14-mounting-plate`  
**Build date:** 2026-09-06

## 1. Build method

Fusion 360 was not available in the execution environment, so Rev A was built as a reproducible **CadQuery 2.8.0 / OCCT 7.9.3** parametric model. No `.f3d` has been fabricated or added.

Source:

- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA_cadquery.py`

Independent exported-geometry verifier:

- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA_verify.py`

Dimensioned drawing generator:

- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA_drawing.py`

Generated artefacts:

- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA.step`
- `mechanical/STL/Decca_IEC_C14_Mounting_Plate_revA.stl`
- `mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_revA_views.png`

The solid is a 40 × 50 × 3 mm rounded rectangular carrier, R2 outer corners, with one centred rectangular C14 through-cut, four M2 clearance through-holes and two M3 clearance through-holes. No countersinks, bosses, ribs, inserts, nut traps or hidden fastening features are present.

## 2. Locked geometry built

| Feature | Rev A result |
|---|---:|
| Plate envelope | **40.00 × 50.00 × 3.00 mm** |
| Outer corner radius | **R2.00 mm** |
| C14 clear cut-out | **20.00 × 27.60 mm**, centred at `(0,0)` |
| Decca holes | **4 × Ø2.40 mm through** |
| Decca hole centres | `(±15.50, ±8.50)` |
| Decca grid | **31.00 × 17.00 mm** |
| C14 mounting holes | **2 × Ø3.40 mm through** |
| C14 mounting centres | `(0.00, ±19.50)` |
| C14 mounting pitch | **39.00 mm** |
| M3 pair midpoint | **(0.00, 0.00)** |
| Minimum M2 edge-to-cut-out ligament | **4.30 mm** |
| Minimum M3 edge-to-cut-out ligament | **4.00 mm** |

The non-governing 16.00 mm and 14.00 mm photograph readings were not used, as required by the specification.

## 3. Validation method

Validation was run against the **exported STEP and STL**, rather than relying only on the in-memory generator model.

The verifier:

- re-imports the STEP and measures its bounding box and topology;
- identifies the four Ø2.40 and two Ø3.40 full-depth cylindrical faces from the STEP and reads their axis positions;
- identifies the four planar faces of the exported rectangular C14 through-cut;
- calculates fixing-to-cut-out ligament from the exported STEP-derived centres and radii;
- loads the exported STL independently with `trimesh`, welds coincident mesh vertices, and checks envelope, watertightness, winding consistency and connected-body count.

Measured volume:

- STEP: **4224.937174 mm³**
- STL: **4228.160935 mm³**

The small mesh-volume delta is the expected tessellation approximation of the exact STEP curves.

## 4. Required Rev A gates

| # | Gate | Result | Evidence |
|---:|---|---|---|
| 1 | Plate envelope = 40.00 × 50.00 × 3.00 mm | **PASS** | STEP measured **40.000000 × 50.000000 × 3.000000 mm**; STL same to mesh tolerance |
| 2 | One connected manifold solid | **PASS** | STEP solid count **1**; STL watertight, winding-consistent, body count **1** |
| 3 | M2 grid = exact 31.00 × 17.00 mm | **PASS** | STEP cylinder axes at `(±15.500000, ±8.500000)` |
| 4 | M3 spacing = exact 39.00 mm | **PASS** | STEP cylinder axes at `(0.000000, ±19.500000)`; measured pitch **39.000000 mm** |
| 5 | M3 midpoint = `(0,0)` | **PASS** | Exported centres midpoint **(0.000000, 0.000000)** |
| 6 | C14 cut-out centred at `(0,0)` | **PASS** | Exported inner planes at X = ±10.000000 and Y = ±13.800000 |
| 7 | C14 clear cut-out ≥ 20.00 × 27.60 mm through full thickness | **PASS** | STEP inner faces prove **20.000000 × 27.600000 × 3.000000 mm** through-clear rectangle |
| 8 | M2 Ø2.40 through; M3 Ø3.40 through | **PASS** | STEP full-depth cylinder radii **1.200000** and **1.700000 mm** |
| 9 | No fixing hole intersects cut-out | **PASS** | Minimum exported-geometry edge gap **4.000000 mm** |
| 10 | Minimum local ligament ≥ 3.0 mm | **PASS** | M2 minimum **4.300000 mm**; M3 minimum **4.000000 mm** |
| 11 | No hidden fastening features | **PASS** | No secondary concentric cylindrical features; only the specified through-features |
| 12 | No support-dependent geometry | **PASS** | Flat 3.00 mm carrier; all apertures are vertical through-cuts; broad face prints on bed |

**CAD validation result: 12/12 required gates PASS.**

## 5. Release artefact checksums

SHA-256 values at this build:

- CadQuery source: `15e5f76a40abd17572a3993bd375387b0677003fc396d91efcf562397f987232`
- STEP: `2b389b17fde813d7cbb8f438a507a25abd73ed8cc5299da8b32592de5a7ed041`
- STL: `13864c22977d82af3e72156815db1adc1498c7b232e3abfb2c29d55fe93f49a2`

These values are replaced from the generated files by the one-time branch build before the draft PR is opened.

## 6. Prototype print intent

Per the controlling specification:

- PETG minimum; flame-retardant PETG/PC preferred for this mains-adjacent location;
- 0.20 mm layers;
- 4+ perimeters;
- 100% infill;
- broad face on the bed;
- no supports.

This printed plate is a **mechanical carrier only**. It is not a claim of mains electrical safety or compliance. The C14 terminals and mains wiring still require appropriate insulation/shrouding, protection/strain relief and electrical validation.

## 7. Physical release gate remains open

Rev A is **not released** on CAD evidence alone. Owner physical testing must still confirm:

1. the purchased C14 body passes through the opening without forcing;
2. the two M3 fixings align at 39 mm without slotting;
3. all four Decca M2 holes align with the physical 31 × 17 mm cabinet grid without forcing;
4. the plate clamps flat without cracking or visible distortion;
5. rear terminal and wire clearance is confirmed before mains energisation.

Until those checks are recorded, status remains **CAD complete / prototype pending**.
