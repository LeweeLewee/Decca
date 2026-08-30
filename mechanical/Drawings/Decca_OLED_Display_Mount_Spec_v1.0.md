# Decca OLED Display Mount Specification v1.2

Status: **Approved design specification** · Mechanical implementation
**Rev P.5 carrier — RELEASED**, prototype built and physically validated 2026-08-30

**Rev Q bezel-only amendment — OPEN**, prototype fit and appearance testing required

Date: 2026-08-27 (v1.0) · 2026-08-28 (v1.1) · 2026-08-30 (v1.2)
Manufacturing method: **FDM 3D print**  
CAD platform: **Autodesk Fusion 360**

*This file keeps its original `_v1.0` filename so existing links stay valid; the document version is the one in the title above.*

## Revision record

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-27 | Initial approved specification. |
| — | 2026-08-30 | **Mechanical Rev P.5 released.** The carrier has been manufactured, installed and physically tested, and every test passed: Perspex fit and tolerances, OLED front insertion and removal, four sprung retaining posts, no collision with the original Decca lighting unit, bottom/open connector-side clearance, the 6.00 mm carrier thickness, the enlarged 14.00 × 4.19 mm four-pin opening, the rear closure and light-blocking features, the original fasteners and captive nuts, 49.00 mm horizontal pitch, the mounting points 7.00 mm lower giving the required OLED position, and installed fit, screen position, stiffness, retention, clearance and powered operation. **No value in this specification changes.** §2 remains the measured fascia authority; the as-built mechanical design is defined by `Decca_OLED_Display_Mount_CAD_Build_revP.md`. |
| **1.1** | **2026-08-28** | **Locked the measured Decca interface geometry in §2, §4, §5 and §10.** The v1.0 figures for the display opening and the M2 fixing pitch were pre-measurement estimates and were superseded by physical measurement at Rev C, print-confirmed at Rev D and re-confirmed by the project owner on 2026-08-28. Fixing pitch **48.00 → 49.00 mm**; display opening **35.50 × 15.80 → 35.20 × 15.30 mm**; hole centre from the opening edge **7.90 → 7.65 mm**. No other value is changed. |
| **1.2** | **2026-08-30** | Opens **Rev Q as a bezel-only amendment**. Replace the Rev N pair of locating side rails with a thin, continuous masking lip around the full inside perimeter of the measured Perspex opening. The lip must sit snugly but without interference, conceal the visible cut edge and remain parametric for test-print refinement. The released Rev P.5 display carrier is frozen and must not change. |

**Change control.** Where this document and a physical measurement disagree, the
measurement wins and this document is updated explicitly — that is what v1.1 is.
The same rule closed Rev P.5: the checks CAD could not settle were settled by
the built part, not by editing a check or a number.
Design-intent values elsewhere in this specification have also been superseded
by later mechanical revisions. The Rev P.5 carrier build review and the Rev Q
bezel brief are authoritative for their respective parts. §2 is the only
section that defines the **original fascia**, and it is now measured, not
estimated.

## 1. Purpose

Mount the 1.3-inch 128×64 SH1106 I²C OLED behind the original Decca **TUNING INDICATOR** opening while preserving the original fascia and using only the existing two M2 fixing holes.

The design comprises:

1. a small, non-structural front bezel surrounding only the original display opening; and
2. a structural rear OLED carrier fixed through the existing Perspex holes with two M2 bolts inserted from the front.

No additional drilling or cutting of the original Decca fascia is permitted.

## 2. Locked Decca interface geometry — MEASURED

Every dimension in this table is taken from the physical fascia. None is an
estimate. Do not substitute a value from any earlier document.

| Parameter | Dimension | Source |
|---|---:|---|
| Existing display opening | **35.20 mm W × 15.30 mm H** | measured, Rev C |
| Perspex thickness | **3.00 mm** | measured |
| Existing fixing-hole type | M2 clearance (Ø2.40 modelled) | measured |
| **Existing fixing-hole pitch** | **49.00 mm horizontal centres** | measured Rev C; **print-confirmed Rev D**; owner-confirmed 2026-08-28 |
| Hole vertical position | Exactly centred on the display opening | measured |
| Hole centre from opening top/bottom | 7.65 mm | derived from the measured opening height |
| Additional panel modification | None | — |

The display-opening centre is the primary datum for optical alignment.

> **⚠ The pitch is not recoverable by clearance.** An M2 screw in a Ø2.40 mm
> clearance hole has only 0.20 mm of radial play. Building at the superseded
> 48.00 mm would put each screw 0.50 mm off its hole and the carrier would not
> bolt on. The Rev O redesign brief inadvertently re-quoted the v1.0 figures and
> had to be corrected during the Rev O build; v1.1 exists so that cannot recur.

## 3. OLED reference geometry

Target module: Pi Hut 1.3-inch 128×64 SH1106 I²C OLED, SKU 105630.

The Fusion model must include a parametric reference component based on verified manufacturer mechanical geometry. Any downloaded/community CAD model may be used only as a secondary visual reference and must not override verified dimensions.

Nominal reference dimensions:

| Feature | Nominal dimension |
|---|---:|
| OLED PCB width | 35.40 mm |
| OLED PCB height | 33.50 mm |
| OLED active area | 29.42 mm W × 14.70 mm H |
| OLED viewing area | approx. 31.42 mm W × 16.70 mm H |
| PCB mounting holes | 4 × Ø3.0 mm |
| Vertical PCB-hole pitch | 28.50 mm |

Critical alignment rule: **OLED active-area centre must coincide with the Decca opening centre.** The PCB outline is not the optical datum.

## 4. Front bezel

The bezel is cosmetic only. It must surround the existing 35.20 × 15.30 mm opening and must **not** extend to, cover or incorporate the existing M2 fixing holes.

Design intent:

- approximate outer size: 39.5–40.5 mm W × 19.8–20.8 mm H;
- nominal visible OLED aperture: 30.40 mm W × 15.10 mm H;
- nominal face thickness: 1.0–1.4 mm;
- softly radiused external corners, visually sympathetic to the original opening;
- slight rear-side chamfer/flared aperture to reduce tunnel effect through the 3 mm Perspex;
- no branding or decorative detailing;
- preferred finish: matt/satin black.

The bezel must be independent of the structural fixing bolts.

### Bezel location/retention

Rev N is the dimensional and appearance baseline: 40.00 × 20.30 × 4.00 mm
overall, with a proven 2.80 mm engagement depth into the 3.00 mm Perspex. Rev Q
changes only the locating/masking feature.

- Replace the two Rev N side locating rails with one **continuous thin lip**
  around all four sides and corners of the inside of the Perspex opening.
- The lip is a cosmetic masking skirt: it must conceal the visible cut edge of
  the Perspex from normal viewing directions and locate the bezel, but it is not
  a clip, structural clamp or interference fit.
- Preserve the proven nominal outer lip envelope of **34.90 × 15.00 mm**, which
  gives 0.15 mm nominal clearance per side inside the measured
  35.20 × 15.30 mm opening.
- Preserve the **2.80 mm** nominal engagement depth. No bezel material may pass
  behind the 3.00 mm Perspex or reduce the released 0.50 mm clearance to the
  OLED glass.
- Start with a **0.40 mm nominal lip wall**, equivalent to one controlled
  extrusion width for the established print configuration. This is a
  provisional test-print value, not a released fit result.
- The continuous corner form must follow the real opening without forcing it.
  Reuse the proven Rev N corner relief where possible and expose corner radius
  or relief as a named parameter rather than assuming an unmeasured Perspex
  corner radius.
- The bezel face must remain snug against the front of the Perspex without
  rocking or visible gaps. It must be removable without marking, spreading or
  stressing the original Perspex.
- Retention remains removable/light adhesive on the existing recessed pads if
  required. The new lip must not be treated as snap retention.
- Test prints may adjust only the lip outer clearance, wall thickness, corner
  relief and lead-in. Changes to the released carrier, Perspex, fixing holes,
  bezel outer appearance or structural load path are forbidden.

The dedicated controlled brief is
`Decca_OLED_Display_Bezel_CAD_Brief_revQ.md`.

## 5. Rear OLED carrier

The rear carrier is the sole structural component.

Functions:

1. clamp against the rear of the original 3 mm Perspex;
2. accept the two existing front-entering M2 bolts at **49.00 mm** horizontal centres;
3. position the OLED active area centrally behind the original opening;
4. retain the OLED PCB without loading the OLED glass;
5. establish OLED-to-Perspex depth independently of screw torque;
6. provide unrestricted clearance for the I²C/header connection;
7. provide optional cable-strain-relief slots.

Approximate carrier width: 54–56 mm, sufficient to provide robust material around the ±24 mm M2 fixing positions.

The carrier should be substantially open around the PCB rather than a solid rear plate, reducing material, improving access and avoiding unnecessary thermal enclosure.

## 6. Structural M2 interface

Assembly sequence, front to rear:

1. M2 bolt head on original front face;
2. original Perspex fixing hole;
3. 3.00 mm Perspex;
4. rear OLED carrier;
5. M2 threaded interface in carrier.

The bezel is not part of this load path.

Preferred rear thread method: **M2 heat-set inserts**, provided the final boss geometry supports them reliably. Printed M2 threads are acceptable only if physical prototyping demonstrates adequate durability.

The carrier must seat directly against the rear Perspex so bolt torque cannot press the OLED glass into the Perspex.

## 7. OLED depth and optical clearance

Nominal OLED-to-Perspex clearance: **0.30 mm**.

Purpose:

- prevent rubbing/contact marks;
- accommodate manufacturing tolerance;
- avoid loading the OLED glass;
- maintain repeatable optical position independent of bolt torque.

This spacing must be generated by hard carrier datums, not by OLED compression.

## 8. OLED retention

Preferred concept:

- two printed locating pins using PCB holes for location only; and
- two sprung retention tabs acting only on the PCB.

Initial locating-pin target: **Ø2.6–2.7 mm** for nominal Ø3.0 mm PCB holes.

Retention tabs must not contact or load the OLED glass. Final snap geometry is subject to print/material prototype validation.

## 9. Cable/header clearance

The carrier must leave the OLED header side open and must not require bending of the module header.

Provide:

- at least approximately 8 mm clear envelope around the projecting pin/header area;
- optional pair of cable-tie slots for strain relief on the carrier;
- no glue-based cable restraint as a design requirement.

## 10. Fusion 360 parameterisation

The model should expose at least the following named user parameters:

```text
// Original Decca
panel_t              = 3.00 mm
panel_open_w         = 35.20 mm   // measured, Rev C
panel_open_h         = 15.30 mm   // measured, Rev C
panel_fix_pitch      = 49.00 mm   // measured Rev C, print-confirmed Rev D
panel_fix_y          = 0.00 mm

// OLED reference
oled_pcb_w           = 35.40 mm
oled_pcb_h           = 33.50 mm
oled_active_w        = 29.42 mm
oled_active_h        = 14.70 mm
oled_view_w          = 31.42 mm
oled_view_h          = 16.70 mm
oled_hole_d          = 3.00 mm
oled_hole_pitch_y    = 28.50 mm

// Design
bezel_window_w       = 30.40 mm
bezel_window_h       = 15.10 mm
bezel_lip_outer_w    = 34.90 mm   // provisional; 0.15 mm clearance per side
bezel_lip_outer_h    = 15.00 mm   // provisional; 0.15 mm clearance per side
bezel_lip_depth      = 2.80 mm    // proven Rev N engagement depth
bezel_lip_wall       = 0.40 mm    // provisional test-print value
bezel_lip_corner_r   = measured/proven Rev N value; do not assume
screen_panel_gap     = 0.30 mm
pcb_clearance        = 0.25 mm
locating_pin_d       = 2.70 mm
```

Important geometry must derive from named parameters rather than hidden sketch dimensions.

Recommended Fusion component structure:

```text
Decca_Display_Mount
├── REF_Decca_Panel
├── REF_SH1106_1P3
├── Front_Bezel
└── Rear_Display_Carrier
```

## 11. FDM design rules

Initial manufacturing assumptions:

- preferred material: PETG/PETG-HF;
- nominal structural wall: 1.6–2.0 mm;
- structural fixing bosses: minimum approximately 4 mm effective material width, subject to insert requirements;
- PCB/feature clearance: approximately 0.2–0.3 mm where appropriate;
- fillet stressed snap features, nominally R0.8–1.0 mm or greater;
- avoid supports where practical;
- orient parts to maximise dimensional accuracy at Perspex-contact and display-location datums.

Final tolerances must be validated against the physical OLED and a first printed prototype before production print.

## 12. Appearance intent

The modification should read as a clean, deliberate reinterpretation of the original tuning indicator, not as a large modern panel added to the fascia.

Preferred front appearance:

- narrow bezel surrounding only the existing rectangular opening;
- matt/satin black finish;
- existing fixing bolts remain visually separate from the bezel;
- original fascia graphics and Perspex retained intact.

## 13. Design evaluation and approval gate

The approved architecture was evaluated at approximately **98.9% design confidence** prior to CAD build.

Key strengths:

- preservation of original fascia: 100%;
- optical alignment: 99%;
- front appearance: 99%;
- structural integrity: 99%;
- printability/serviceability: 99% range.

Residual uncertainty is limited mainly to actual OLED manufacturing variation, print tolerance and retention-tab behaviour. These are prototype-validation issues rather than unresolved architecture issues.

## 14. Build control

This document authorises the **Fusion 360 CAD build** to begin from this specification.

Before manufacture, the completed CAD should be reviewed against this specification and the physical Pi Hut OLED. Any material deviation from the locked architecture or original-panel interface should be returned for approval before printing.
