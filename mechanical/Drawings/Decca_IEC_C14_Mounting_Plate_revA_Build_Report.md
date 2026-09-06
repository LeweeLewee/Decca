# Decca IEC C14 Mounting Plate Rev A — CAD Build Report

**Status:** **REJECTED — physical fit FAIL**  
**Disposition date:** 2026-09-06  
**Superseded by:** Rev B corrected-profile design

## Failure

Rev A reproduced the locked Rev A specification correctly, and all 12 numerical CAD gates passed. The physical design nevertheless failed because the specification reduced the purchased IEC C14 interface to a **20.00 × 27.60 mm rectangular bounding opening**.

Owner physical review found that the plate **does not properly enclose the IEC C14 shape**.

This is not a print-tolerance issue. The opening geometry itself is wrong.

## Root cause

The earlier specification recorded measured values of **27.14 mm**, **19.50 mm**, **16.00 mm** and **14.00 mm**, but incorrectly declared the 16.00 mm and 14.00 mm readings non-governing for the front plate.

They are required to reconstruct the actual six-sided C14 profile and its angled sections.

## Rev A geometry retained for traceability

- Plate: 40.00 × 50.00 × 3.00 mm
- Decca holes: 4 × Ø2.40 mm on exact 31.00 × 17.00 mm grid
- C14 fixing holes: 2 × Ø3.40 mm at exact 39.00 mm pitch
- Rejected C14 opening: rectangular 20.00 × 27.60 mm
- CAD validation at time of build: 12/12 specified Rev A gates PASS

Passing those gates only proved conformance to an incomplete specification. It did not prove the physical interface was correctly represented.

## Required correction

Rev B must use the actual measured inlet profile:

- long flat / overall width: **27.14 mm**
- overall height: **19.50 mm**
- opposite short flat: **16.00 mm**
- straight side before angled section: **14.00 mm**
- derived angle run: **5.57 mm**
- derived angle rise: **5.50 mm**
- derived angle: **44.638°**
- long-flat corners: **R2.00 mm**
- remaining four corners: **R0.40 mm**

Rev A STL/STEP files are historical rejected artefacts only. **Do not print, install or modify Rev A into service.**
