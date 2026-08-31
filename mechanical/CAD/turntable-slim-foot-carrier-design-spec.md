# Decca Turntable Slim Foot Carrier — Fusion 360 Design Specification

## 1. Purpose

Design a compact replacement carrier for the existing turntable feet so the turntable can fit within the Decca cabinet.

The original large plastic foot surround is to be removed. The replacement part must:

- reuse the existing turntable mounting holes;
- retain and reuse the original inner rubber foot;
- substantially reduce the lateral bulk of the original plastic carrier;
- provide an assembled height of approximately **25 mm from the underside of the turntable to the lowest contact surface of the rubber foot**;
- be suitable for FDM printing on a **Bambu Lab P1S**;
- be modelled parametrically in **Fusion 360**.

The intention is to preserve the original compliant rubber isolation element while replacing only the bulky plastic structure around it.

---

## 2. Source Measurements

Measurements taken from the original hardware and photographs:

| Feature | Value |
|---|---:|
| Target total assembled height | **25.0 mm** |
| Turntable mounting-hole centre-to-centre spacing | **39.0 mm** |
| Rubber foot outside diameter | **30.0 mm approx.** |
| Original plastic surround outside width | **39.0 mm approx.** |
| Original carrier internal/open diameter | **36.0 mm approx.** |
| Central / rubber-foot feature measured | **13.0 mm approx.** |
| Small screw thread OD | **2.55 mm approx.** |
| Larger screw thread OD | **2.90 mm approx.** |
| Example screw lengths observed | **11.33 mm / 14.81 mm** |

Treat photographed caliper measurements as prototype inputs, not precision manufacturing drawings. Critical interfaces should be made parametric and adjusted after the first test print if necessary.

---

## 3. Design Architecture

Use a **central circular foot carrier with two narrow opposing mounting ears**.

### Central body

- Nominal outside diameter: **31–32 mm**.
- Purpose: locate and support the original rubber foot.
- Keep the carrier only slightly wider than the rubber foot.
- Avoid recreating the original 39 mm full circular surround.
- Hollow or pocket non-structural material where practical.
- Add generous internal and external fillets where ears meet the body.

### Mounting ears

- Two ears extending from the central body to the existing mounting points.
- Hole centres: **39.0 mm apart**.
- Ears should be as narrow as practical while providing adequate stiffness.
- Suggested ear thickness: **3.0–3.5 mm minimum**.
- Use local bosses around the fixing holes rather than making the full structure thick.
- Use rounded/filleted external profiles, not sharp rectangular tabs.

### Rubber-foot interface

The original rubber foot remains the compliant load-bearing element.

Requirements:

- provide a circular locating seat/recess for the original rubber foot;
- nominal starting clearance for a 30.0 mm rubber OD: **30.2–30.4 mm**, subject to prototype fit;
- retain the original central fixing arrangement where applicable;
- prevent lateral movement of the rubber foot;
- ensure PETG does not bypass the rubber foot and contact the cabinet when assembled;
- preserve rubber compression and isolation behaviour as far as possible.

Do not make the replacement carrier itself the cabinet-contacting foot.

---

## 4. Height Strategy

The **25 mm requirement is the total assembled height**, measured:

**turntable underside → lowest surface of the installed original rubber foot**

Therefore:

`Printed carrier contribution = 25.0 mm - effective protruding height of rubber foot`

Do not simply create a 25 mm tall printed body.

The rubber foot effective height should be treated as a Fusion parameter so the model can be corrected rapidly after a physical trial.

Where the rubber nests into the printed carrier, account for the seat depth explicitly:

`Total assembled height = carrier structural height + rubber protrusion below carrier`

Target: **25.0 mm nominal**, with first prototype acceptance range of approximately **±0.5 mm** unless cabinet clearance demands tighter control.

---

## 5. Fusion 360 Parameters

Create the design fully parametrically. Suggested user parameters:

| Parameter | Initial value |
|---|---:|
| `Target_Total_Height` | 25.0 mm |
| `Mount_Hole_CTC` | 39.0 mm |
| `Rubber_OD` | 30.0 mm |
| `Rubber_Clearance` | 0.3 mm |
| `Rubber_Seat_Dia` | `Rubber_OD + Rubber_Clearance` |
| `Body_OD` | 31.5 mm |
| `Ear_Thickness` | 3.2 mm |
| `Mount_Hole_Dia` | provisional, based on measured screw / existing fit |
| `Boss_OD` | 6.0–7.0 mm initial |
| `Rubber_Seat_Depth` | provisional |
| `Rubber_Effective_Height` | provisional |
| `Carrier_Height` | driven from target assembled height |
| `Edge_Fillet` | 1.0–1.5 mm |
| `Ear_Root_Fillet` | 2.0–3.0 mm |

Any unknown interface should be a named parameter rather than a hard-coded sketch dimension.

---

## 6. Mounting Hole Treatment

The existing turntable holes must be reused without modification.

Because the exact required printed-hole diameter depends on the original screw type and whether the screw should pass freely or self-thread into plastic:

- model the hole diameter parametrically;
- start with a clearance-hole approach unless physical inspection confirms the screw is intended to cut into the plastic carrier;
- preserve sufficient radial material around each hole;
- add a local cylindrical or teardrop boss if required for strength;
- do not make the ear wider than necessary purely to match the original carrier shape.

If the original screws are reused, ensure required head clearance and seating face are included.

---

## 7. Structural Requirements

The carrier supports a continuously loaded turntable and should resist long-term creep and impact during handling.

Design targets:

- no thin unsupported neck between mounting ear and central body;
- smooth load path from fixing holes into the rubber-foot seat;
- minimum practical wall thickness around the rubber seat: approximately **2.0–2.5 mm**;
- local reinforcement at mounting bosses;
- filleted transitions throughout;
- avoid unnecessary solid mass.

The design should be compact rather than visually reproducing the original component.

---

## 8. Material and Printing

Preferred material: **PETG / Bambu PETG-HF**.

Printer: **Bambu Lab P1S**.

Recommended initial print approach:

- 0.20 mm layer height;
- 4 walls/perimeters;
- 5 top and bottom layers;
- 30–40% infill;
- gyroid or equivalent structural infill;
- increase local wall/boss thickness via geometry rather than using very high global infill;
- orient the part so the mounting ears have strong continuous perimeter paths and are not relying on weak inter-layer tension;
- avoid support if the geometry can be designed to print cleanly without it.

PLA is not preferred because of the continuous static load and greater creep risk.

---

## 9. Prototype Validation

Produce **one prototype carrier first**, not a full set.

Validate:

1. 39.0 mm mounting-hole alignment.
2. Screw fit and head seating.
3. Rubber foot insertion and retention.
4. Rubber foot remains the lowest contact point.
5. No plastic-to-cabinet contact under expected compression.
6. Total assembled height is approximately 25.0 mm.
7. Turntable sits level and stable.
8. No interference with the Decca cabinet.
9. No visible flexing around either mounting ear.
10. Rubber foot can still perform as an isolation element.

After validation, adjust only parameters and regenerate.

---

## 10. CAD Deliverables

Claude/Fusion should create:

- one fully parametric Fusion 360 component for the replacement carrier;
- clearly named sketches, features and user parameters;
- no unnecessary timeline clutter;
- manufacturable geometry with fillets/chamfers applied deliberately;
- final body suitable for export as STL/3MF;
- a simple dimensioned screenshot or inspection view showing:
  - 39 mm mounting-hole CTC;
  - central carrier OD;
  - rubber-foot seat diameter;
  - total carrier height;
  - mounting-hole diameter;
  - rubber-foot seat depth.

---

## 11. Design Intent Summary

This is **not a redesign of the original suspension**.

It is a packaging adaptation:

- retain the original rubber isolator;
- retain the original turntable attachment points;
- remove the oversized plastic surround;
- replace it with the smallest structurally credible printed carrier;
- achieve an overall assembled foot height of approximately 25 mm;
- make all uncertain physical dimensions parametric for rapid prototype iteration.

The preferred visual form is a compact central circular carrier with two restrained, filleted mounting ears at 39 mm centres.
