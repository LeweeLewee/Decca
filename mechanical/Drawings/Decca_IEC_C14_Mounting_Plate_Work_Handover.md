# Work Handover — Build Decca IEC C14 Mounting Plate Rev A

## Mission

Build and validate the **IEC C14 mounting plate Rev A** for the Decca restoration, then add the reproducible CAD source and release artefacts to the existing feature branch.

This is a small, self-contained mechanical task. Do not broaden it into the wider mains wiring, ESP32 housing, OLED mount, speaker fit or rear-panel layout work.

## Repository and branch

- Repository: `LeweeLewee/Decca`
- Base: `main`
- Existing feature branch: **`feat/iec-c14-mounting-plate`**
- Continue on that branch. **Do not create or modify work on the open ESP32 housing branch/PR.**
- Keep this as its own focused mechanical PR.

Read before editing:

1. `CONTRIBUTING.md`
2. `mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_Spec_revA.md` — **controlling specification**
3. `mechanical/CAD/README.md`
4. `mechanical/STL/README.md`
5. `mechanical/Drawings/README.md`

If any older chat note or generic IEC C14 catalogue dimension conflicts with the controlling Rev A spec, **the Rev A spec wins**. The design is based on the actual purchased inlet measurements, not a generic C14 panel cut-out.

## Locked Rev A geometry

Use plate centre as `(0,0)`.

### Plate

- **40.00 mm wide × 50.00 mm high × 3.00 mm thick**
- Centred on `(0,0)`
- Outer corners: **R2.00 mm** recommended
- Small ~0.5 mm edge break/chamfer is acceptable where it does not alter mounting faces
- One flat connected solid
- No ribs, bosses, heat-set inserts, captive nuts, countersinks or unnecessary reinforcement

### Decca mounting holes

4 × **Ø2.40 mm through**, centres:

- `(-15.50, -8.50)`
- `(+15.50, -8.50)`
- `(-15.50, +8.50)`
- `(+15.50, +8.50)`

This is an exact **31.00 × 17.00 mm centre-to-centre grid** for the four M2 cabinet bolts.

### IEC C14 cut-out

The physical inlet body was measured **27.14 × 19.50 mm** and is intentionally rotated 90° in this plate.

Production cut-out:

- **20.00 mm X × 27.60 mm Y**
- centred exactly at `(0,0)`
- true clear rectangle through the full 3.00 mm thickness
- do not add an internal radius that intrudes into this clear envelope

### IEC C14 M3 mounting holes

2 × **Ø3.40 mm through**:

- `(0.00, -19.50)`
- `(0.00, +19.50)`

Requirements:

- exact **39.00 mm centre-to-centre** spacing
- pair lies on X = 0
- midpoint of the pair is exactly `(0,0)`
- therefore the M3 pair is centred on both the vertical and horizontal plate centrelines

### Other measured inlet values

Two additional physical readings, **16.00 mm** and **14.00 mm**, were captured from photographs. Their feature datums were not needed for the front mounting plate and are deliberately non-governing. **Do not infer what they represent or use them to alter the plate geometry.** If rear packaging later needs them, request/record an explicit datum first.

## Important correction already made before CAD

An earlier chat sketch used a 36 × 45 mm plate. Do **not** reproduce it.

That envelope left only about 1.3 mm of material beyond the fixing-hole edges. The controlling Rev A spec enlarges the plate symmetrically to **40 × 50 mm**, which retains a compact part while giving sensible edge ligament around both the M2 and M3 fixings.

## Build approach

Use a reproducible parametric model. Match existing repository practice where practical, but do not create fake native CAD files.

Preferred sequence:

1. Implement a compact parametric generator in `mechanical/CAD/`.
2. Generate the solid from the locked dimensions above.
3. Export a neutral **STEP**.
4. Export a manifold **STL**.
5. Independently verify the exported geometry, preferably from the STEP/STL rather than only from the same in-memory model.
6. Produce at least one dimensioned/orthographic PNG showing plate outline, C14 opening, M3 pair and M2 grid.
7. Write a concise build report with measured outputs and PASS/FAIL results.

If Autodesk Fusion 360 is genuinely available, a Fusion Python generator and native `.f3d` are acceptable and align with the repository's existing display work. If Fusion is not available, use a reproducible alternative such as CadQuery and commit its source. **Do not fabricate or placeholder an `.f3d`.**

## Required validation gates

Report explicit results for all twelve gates in §6 of the controlling spec. At minimum verify numerically:

- 40.00 × 50.00 × 3.00 mm envelope
- exactly one connected/manifold part
- M2 grid = exactly 31.00 × 17.00 mm
- M3 spacing = exactly 39.00 mm
- M3 midpoint = `(0,0)`
- C14 cut-out centred at `(0,0)`
- clear cut-out ≥ 20.00 × 27.60 mm through the full thickness
- M2 holes Ø2.40 mm through
- M3 holes Ø3.40 mm through
- no hole/cut-out intersections
- ≥3.0 mm local ligament between each fixing-hole edge and the C14 cut-out
- no hidden fastening features or support-dependent geometry

Do not weaken a gate to make the model pass. If the geometry contradicts the specification, stop and report the contradiction rather than silently changing a locked dimension.

## Required files

Create/update only what is needed for this part.

Expected minimum:

- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA_fusion.py` **or** an equivalently named reproducible parametric source appropriate to the chosen CAD kernel
- `mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revA.step`
- `mechanical/STL/Decca_IEC_C14_Mounting_Plate_revA.stl`
- `mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_revA_Build_Report.md`
- `mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_revA_views.png` or equivalent orthographic/dimensioned image

Also update the relevant mechanical README(s) and `docs/Revision History.md` once the CAD artefacts exist, in line with `CONTRIBUTING.md`.

## Print/release intent

Prototype recommendation from the controlling spec:

- PETG minimum; flame-retardant PETG/PC preferred for the mains-adjacent location
- 0.20 mm layers
- 4+ perimeters
- 100% infill
- broad face on bed
- no supports

The plate is **mechanical support only**. Do not claim electrical safety/compliance from the printed polymer. Rear C14 terminals and mains wiring require their own insulation, shrouding, strain relief/protection and electrical validation.

## Physical test gate

Do **not** mark Rev A fully released merely because CAD passes.

Final owner test must confirm:

1. C14 body passes through without forcing.
2. Both M3 fixings align at 39 mm without slotting.
3. All four Decca M2 holes align with the physical 31 × 17 mm grid without forcing.
4. Plate clamps flat without cracking/distortion.
5. Rear terminal/wire clearance is confirmed before energising mains.

Until those physical checks are recorded, status should be **CAD complete / prototype pending**, not released.

## Commit / PR discipline

Use Conventional Commits, e.g.:

`mech(c14-mount): build rev A mounting plate`

Keep the PR limited to this plate. Do not touch firmware, wiring topology, OLED/display geometry, ESP32 housing geometry or unrelated BOM choices.

At completion, leave a concise PR summary containing:

- final dimensions
- CAD validation result
- generated files
- any assumptions that remain
- explicit statement that physical fit is still pending unless the owner has actually tested the print.