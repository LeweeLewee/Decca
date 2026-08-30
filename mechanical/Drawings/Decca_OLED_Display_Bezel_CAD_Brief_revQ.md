# Decca OLED Display Bezel — CAD Brief Rev Q

Status: **OPEN — bezel-only prototype revision**

Baseline: repository commit `a7e6073caff91e39ecb8143d2f361bcc7dc5518d`
(Rev P.5 merged and released), 2026-08-30.

## 1. Owner requirement

Add a thin lip around the complete inside perimeter of the Perspex display
opening. The lip shall conceal the cut edge of the Perspex and sit snugly to it.
Initial dimensions may be refined through bezel test prints.

**There shall be no change to the released Rev P.5 display carrier.**

Owner amendment, 2026-08-30: replace the initial clearance-fit target with a
controlled horizontal interference fit. Increase the visible opening by
0.50 mm horizontally and 0.25 mm vertically; move the inset walls outward by
0.25 mm on each horizontal side and 0.10 mm on each vertical side; add R2.00 mm
outer corners to the inset walls.

Owner correction, 2026-08-30: the slicer currently resolves the 0.40 mm inset
wall as only one wall loop. Increase the nominal wall to **0.80 mm** so the
established 0.40 mm extrusion configuration produces **two continuous wall
loops** around the complete inset lip.

## 2. Controlled baseline

Verified physical/interface facts:

- Perspex display opening: **35.20 × 15.30 mm**.
- Perspex thickness: **3.00 mm**.
- Rev N bezel overall envelope: **40.00 × 20.30 × 4.00 mm**.
- Rev N locating feature outer envelope: **34.90 × 15.00 mm**.
- Rev N engagement depth into the Perspex: **2.80 mm**.
- Rev N rear material remains 0.20 mm forward of the Perspex rear face and
  0.50 mm clear of the OLED glass.
- Rev N uses two side locating rails and removable adhesive retention.
- Rev P.5 carrier is released and physically validated.

Frozen Rev P.5 file hashes at the Rev Q baseline:

| File | SHA-256 |
|---|---|
| `mechanical/CAD/Decca_Display_Mount_revP.f3d` | `d69bf5373b80301f645f0ad79357090f4db45d8e425b55852bc12b1fc8e0c8ba` |
| `mechanical/CAD/Decca_Display_Mount_revP_fusion.py` | `719ffd666a31278f6553dae053d480f48a33cc9aba5a48521d61fc62273d9656` |
| `mechanical/CAD/Decca_Display_Mount_revP_verify.py` | `7cef57d4a6f813d858bbff466e70a67c5dc5504194e6033151b306549aa11907` |
| `mechanical/CAD/Rear_Display_Carrier_revP.step` | `1b25a24d3c216646dc70a5521cae8db3d456afd7e6760505a5c304ff1a05c359` |
| `mechanical/STL/Rear_Display_Carrier_revP.stl` | `ec8a4adb8e4e80f3452da2edf9d56c17e55b7aa80db075310e2af75e224c5897` |
| `mechanical/CAD/Decca_Display_Mount_revP_assembly.step` | `e7d9c40d250fd23d6b8aa250b2363714c8a396772bad623746ba594173d2b24a` |

Rev Q amended targets requiring test-print confirmation:

- full-perimeter lip wall: **0.80 mm nominal**, targeting two 0.40 mm loops;
- visible bezel opening: **30.90 × 15.35 mm**;
- Perspex inset-wall outer envelope: **35.40 × 15.20 mm**;
- horizontal fit: **0.10 mm nominal interference per side**;
- vertical fit: **0.05 mm nominal clearance per side**;
- inset-wall outer corner radius: **R2.00 mm**.

## 3. Required Rev Q topology

1. Preserve the Rev N bezel face, outer envelope, visible-window design,
   external radii, finish intent and recessed adhesive pads.
2. Replace the two side-only locating rails with one continuous rearward
   masking skirt around the left, right, top, bottom and all four corners.
3. Increase the skirt outer envelope from the Rev N baseline to
   **35.40 × 15.20 mm** and keep its rearward depth at **2.80 mm**.
4. Use a **0.80 mm** wall measured inward from that outer envelope. The
   wall and opening it creates must be derived, not independently dimensioned.
5. Apply **R2.00 mm** to all four outer inset-wall corners. Offset the inner
   corners from the outer profile so the nominal 0.80 mm wall remains constant.
6. Add only the minimum lead-in needed to prevent the thin lip catching on the
   Perspex edge. A lead-in must not reduce cut-edge coverage at the seated
   position.
7. The lip is cosmetic and locating only. Its sole interference is the declared
   **0.10 mm per horizontal side**. It must not become a snap, clamp or
   structural feature.
8. The thin printed lip shall flex to accommodate the interference; the
   original Perspex shall not be spread or visibly stressed. The bezel front
   seating face must remain flush and snug to the Perspex.
9. No lip material may extend behind the 3.00 mm Perspex, contact the OLED
   glass, touch the Rev P.5 carrier or enter its sprung-post corridors.
10. The new lip must not obscure the intended powered screen content. Report
   the exact change to the clear optical opening; do not declare it acceptable
   from CAD alone.

## 4. Named parameters

At minimum expose:

```text
panel_open_w         = 35.20 mm   // measured
panel_open_h         = 15.30 mm   // measured
panel_t              = 3.00 mm    // measured
bezel_window_w       = 30.90 mm   // Rev N 30.40 + 0.50
bezel_window_h       = 15.35 mm   // Rev N 15.10 + 0.25
bezel_lip_outer_w    = 35.40 mm   // Rev N 34.90 + 2 x 0.25
bezel_lip_outer_h    = 15.20 mm   // Rev N 15.00 + 2 x 0.10
bezel_lip_interf_x   = 0.10 mm    // derived per horizontal side
bezel_lip_clear_y    = 0.05 mm    // derived per vertical side
bezel_lip_depth      = 2.80 mm    // proven Rev N depth
bezel_lip_wall       = 0.80 mm    // two 0.40 mm wall loops
bezel_lip_corner_r   = 2.00 mm    // outer corner radius
bezel_lip_inner_w    = 33.80 mm   // derived: outer width - 2 x wall
bezel_lip_inner_h    = 13.60 mm   // derived: outer height - 2 x wall
bezel_lip_inner_r    = 1.20 mm    // derived: outer radius - wall
bezel_lip_lead       = provisional, minimum printable value
```

Do not bury fit values in sketches. Changing the interference/clearance, wall,
corner radius or lead-in must regenerate a valid single solid.

At the 0.80 mm wall, the lip—not the bezel face—limits the vertical
clear opening. The expected coaxial effective opening is therefore
**30.90 × 13.60 mm**: width controlled by the 30.90 mm face opening and height
controlled by the 13.60 mm lip inner envelope. CAD shall measure and report the
actual result.

## 5. File and revision control

- Create a **new standalone Rev Q bezel design**. Do not edit the released
  Rev P.5 carrier document or regenerate its carrier exports.
- Preserve `Front_Bezel_revN.*` as the last released bezel baseline.
- New source/export names shall be unambiguous, for example:
  `Decca_Display_Bezel_revQ.f3d`, `Front_Bezel_revQ.step` and
  `Front_Bezel_revQ.stl`.
- If an assembly is exported, name it Rev Q and reference the unchanged Rev
  P.5 carrier. Do not overwrite `Decca_Display_Mount_revP_assembly.step`.
- Record before/after SHA-256 hashes for every Rev P.5 carrier source and export
  and prove they are unchanged.

## 6. CAD and print checks

CAD must demonstrate:

- one connected, manifold bezel solid with no slivers;
- continuous lip coverage around all four sides and corners;
- 30.90 × 15.35 mm bezel face opening;
- 35.40 × 15.20 mm outer lip envelope and 2.80 mm depth;
- 0.10 mm horizontal interference per side and 0.05 mm vertical clearance per
  side against the measured opening;
- R2.00 mm outer corners and constant 0.80 mm wall through the corners;
- 33.80 × 13.60 mm derived lip inner envelope with R1.20 mm inner corners;
- exact wall thickness and the expected 30.90 × 13.60 mm effective optical
  opening;
- no intersection with the measured Perspex solid except the declared
  horizontal interference envelope, with deformation assigned to the thin lip;
- no material behind the Perspex rear face;
- at least the released 0.50 mm clearance to OLED glass;
- no intersection with the unchanged Rev P.5 carrier or its assembly/removal
  corridors;
- a support-free print orientation suitable for the thin continuous lip; and
- comparable front, rear and section views showing how the cut edge is masked.

The production slicer preview must additionally demonstrate exactly two
continuous 0.40 mm wall loops around every straight and curved section of the
lip. A single variable-width wall, missing loop, gap-fill substitution or
locally merged loops does not satisfy this requirement.

The first print is an **integration prototype**, not a release part.

## 7. Prototype acceptance

With the original Perspex and the released carrier installed:

1. The bezel seats fully against the Perspex with light, even hand pressure and
   without excessive force, rocking or a visible front-face gap.
2. The horizontal interference gives a snug fit, but the bezel remains
   removable and does not mark, spread or visibly stress the Perspex.
3. The Perspex cut edge is concealed continuously on all four sides and at the
   corners from normal front and oblique viewing positions.
4. The lip is not visibly wavy, broken or translucent.
5. The powered OLED retains the required visible content and has no new edge
   shadow, reflection or light leak.
6. The bezel remains independent of the mounting bolts and carrier load path.
7. The sliced and printed lip remains continuous at two-wall-loop thickness,
   including through all four R2.00 outer corners.

If fit needs adjustment, change the named clearance/corner parameters and
print another Rev Q prototype. Do not modify the Perspex or Rev P.5 carrier to
make the bezel fit.

## 8. Stop conditions

Stop and report rather than improvise if:

- the R2.00 wall corners or declared interference cannot seat without damaging
  or visibly stressing the Perspex;
- the continuous lip requires more interference than the declared 0.10 mm per
  horizontal side or creates unacceptable masking;
- the selected production slicer cannot maintain two continuous wall loops
  through the complete lip at 0.80 mm nominal thickness;
- the lip would reduce OLED visibility beyond the owner's accepted powered
  presentation;
- the Rev P.5 carrier or its released files would need to change; or
- Fusion cannot produce and verify a stable, parametric single solid.
