# Decca OLED Display Bezel — CAD Brief Rev Q

Status: **OPEN — bezel-only prototype revision**

Baseline: repository commit `a7e6073caff91e39ecb8143d2f361bcc7dc5518d`
(Rev P.5 merged and released), 2026-08-30.

## 1. Owner requirement

Add a thin lip around the complete inside perimeter of the Perspex display
opening. The lip shall conceal the cut edge of the Perspex and sit snugly to it.
Initial dimensions may be refined through bezel test prints.

**There shall be no change to the released Rev P.5 display carrier.**

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

Provisional values requiring test-print confirmation:

- full-perimeter lip wall: **0.40 mm nominal**;
- nominal lip clearance: **0.15 mm per side** from the measured opening;
- continuous corner radius/relief: derive from the proven Rev N geometry where
  possible and keep parametric because the physical corner radius is not
  recorded.

## 3. Required Rev Q topology

1. Preserve the Rev N bezel face, outer envelope, visible-window design,
   external radii, finish intent and recessed adhesive pads.
2. Replace the two side-only locating rails with one continuous rearward
   masking skirt around the left, right, top, bottom and all four corners.
3. Keep the skirt outer envelope at the proven initial
   **34.90 × 15.00 mm** and its rearward depth at **2.80 mm**.
4. Start with a **0.40 mm** wall measured inward from that outer envelope. The
   wall and opening it creates must be derived, not independently dimensioned.
5. Add only the minimum lead-in needed to prevent the thin lip catching on the
   Perspex edge. A lead-in must not reduce cut-edge coverage at the seated
   position.
6. The lip is cosmetic and locating only. It must use clearance, not
   interference, and must not become a snap, clamp or structural feature.
7. The bezel front seating face must remain flush and snug to the Perspex.
8. No lip material may extend behind the 3.00 mm Perspex, contact the OLED
   glass, touch the Rev P.5 carrier or enter its sprung-post corridors.
9. The new lip must not obscure the intended powered screen content. Report
   the exact change to the clear optical opening; do not declare it acceptable
   from CAD alone.

## 4. Named parameters

At minimum expose:

```text
panel_open_w         = 35.20 mm   // measured
panel_open_h         = 15.30 mm   // measured
panel_t              = 3.00 mm    // measured
bezel_lip_outer_w    = 34.90 mm   // provisional fit target
bezel_lip_outer_h    = 15.00 mm   // provisional fit target
bezel_lip_clear_x    = 0.15 mm    // derived per side
bezel_lip_clear_y    = 0.15 mm    // derived per side
bezel_lip_depth      = 2.80 mm    // proven Rev N depth
bezel_lip_wall       = 0.40 mm    // provisional test-print value
bezel_lip_corner_r   = extracted/proven value; unresolved if unavailable
bezel_lip_lead       = provisional, minimum printable value
```

Do not bury fit values in sketches. Changing the outer clearance, wall,
corner relief or lead-in must regenerate a valid single solid.

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
- 34.90 × 15.00 mm initial outer lip envelope and 2.80 mm depth;
- exact wall thickness and the resulting clear optical opening;
- no intersection with the measured Perspex solid other than the intended
  clearance relationship;
- no material behind the Perspex rear face;
- at least the released 0.50 mm clearance to OLED glass;
- no intersection with the unchanged Rev P.5 carrier or its assembly/removal
  corridors;
- a support-free print orientation suitable for the thin continuous lip; and
- comparable front, rear and section views showing how the cut edge is masked.

The first print is an **integration prototype**, not a release part.

## 7. Prototype acceptance

With the original Perspex and the released carrier installed:

1. The bezel seats fully against the Perspex without force, rocking or a
   visible front-face gap.
2. The lip is snug but removable and does not mark, spread or stress the
   Perspex.
3. The Perspex cut edge is concealed continuously on all four sides and at the
   corners from normal front and oblique viewing positions.
4. The lip is not visibly wavy, broken or translucent.
5. The powered OLED retains the required visible content and has no new edge
   shadow, reflection or light leak.
6. The bezel remains independent of the mounting bolts and carrier load path.

If fit needs adjustment, change the named clearance/corner parameters and
print another Rev Q prototype. Do not modify the Perspex or Rev P.5 carrier to
make the bezel fit.

## 8. Stop conditions

Stop and report rather than improvise if:

- the physical opening corner form cannot be derived from the Rev N design or
  existing evidence;
- a continuous lip cannot fit without interference or unacceptable masking;
- the lip would reduce OLED visibility beyond the owner's accepted powered
  presentation;
- the Rev P.5 carrier or its released files would need to change; or
- Fusion cannot produce and verify a stable, parametric single solid.
