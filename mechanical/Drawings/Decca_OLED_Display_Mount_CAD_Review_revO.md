# Decca OLED Display Mount — CAD Redesign Specification (Rev O)

Supersedes Rev N as the active design direction for the OLED carrier.

Platform: Autodesk Fusion 360. Manufacture: FDM 3D print.

## 1. Reason for redesign

Physical print-and-fit iterations of Rev N have shown that the current front-loaded architecture is over-constrained by the required screen depth.

To position the OLED glass close to the inside face of the original Perspex, Rev N reduced the carrier front plate to 1.10 mm. This in turn created solder-tip interference with the Perspex, reduced snap-hook effectiveness, and made the separate retainer bar the primary PCB retention feature.

Rev O changes the architecture rather than further tuning Rev N.

## 2. Rev O architecture

The OLED module shall be loaded into the carrier from the rear.

The OLED glass/display face shall project forwards through the carrier window towards the inside face of the Perspex. The carrier shall then be fixed to the original Perspex using the existing two M2 fixing holes at 48.00 mm centres.

The assembled geometry shall capture the OLED between the rear carrier and Perspex-side seating geometry, removing the need for a separate retainer bar.

The OLED glass must not be used as the structural compression stop. Bolt preload must be reacted by positive carrier-to-Perspex seating features and PCB support geometry.

## 3. Existing Decca interface — unchanged

- Original Perspex thickness: 3.00 mm.
- Existing aperture: 35.50 mm W × 15.80 mm H.
- Existing M2 fixing-hole pitch: 48.00 mm horizontal.
- Fixing-hole centreline: vertically centred on the display aperture.
- Hole centreline therefore lies 7.90 mm from the upper and lower aperture edges.
- No additional holes, cutting or irreversible modification to the original Perspex.
- M2 screws enter from the front of the Perspex and fasten into the rear carrier.

## 4. Front bezel — unchanged in principle

The front bezel remains a separate cosmetic trim around the aperture only.

It must not include the M2 fixing holes and must not carry structural load.

Its purpose is to mask the original aperture edge and provide a clean front finish.

Unless physical testing identifies a problem, the Rev N bezel geometry may be retained.

## 5. OLED loading and retention

### 5.1 Rear loading

The OLED PCB shall insert into the carrier from the rear.

The carrier shall include a rear-entry PCB pocket and a central forward clearance/window for the OLED glass.

### 5.2 Positive PCB datum

The PCB shall seat against defined support lands/shoulders in the carrier.

These lands establish the OLED fore/aft position and prevent M2 screw torque from loading the OLED glass.

### 5.3 Locating snap pins

The existing snap-pin concept may be retained, but its role changes.

The pins are approved as locating and light-retention features because physical prototypes show that they position the screen effectively within the carrier.

They must not be relied upon as the primary structural retention method.

Design intent:

- locate the PCB consistently in X/Y;
- provide enough light engagement to keep the OLED in the carrier during handling and assembly;
- avoid significant PCB bending or insertion force;
- avoid fine hook geometry that depends on very thin carrier sections.

If the current Rev N snap geometry can be adapted to the rear-loading architecture without excessive strain or tolerance sensitivity, reuse is preferred over inventing a new mechanism.

### 5.4 Retainer bar

Delete the separate retainer bar from Rev O.

The assembled carrier/Perspex geometry provides the primary capture of the OLED, with snap pins used only for location and handling retention.

## 6. Optical depth and glass protection

The target remains for the OLED display face to sit close to the inside face of the Perspex.

Target nominal glass-to-Perspex gap: 0.15–0.30 mm.

The exact final nominal may be selected during CAD validation based on measured module geometry and print tolerance.

Critical requirement: the glass must not become the structural stop when the M2 screws are tightened.

The carrier shall include positive hard stops so that full seating of the carrier against the Perspex defines the assembly depth independently of OLED glass thickness.

## 7. Carrier structural design

Rev O should take advantage of the reversed architecture to restore sensible FDM section thicknesses.

Guidance:

- use approximately 2.0–3.0 mm structural wall thickness where geometry allows;
- reinforce M2 boss regions appropriately;
- avoid unnecessary thin membranes around the display window;
- leave rear access around the header and solder joints;
- no requirement to trim OLED header solder tips solely to achieve panel fit;
- maintain cable/header clearance and serviceability.

The carrier should seat positively and flat against the inside face of the Perspex.

## 8. Load path

The intended structural load path is:

M2 screw → rear carrier → carrier/Perspex seating stops → Perspex.

OLED PCB support lands locate the module inside the carrier.

The OLED glass must not carry screw preload.

## 9. Required CAD changes from Rev N

1. Redesign the rear carrier around rear insertion of the OLED PCB.
2. Move the PCB seating datum to the rear-loaded geometry.
3. Create a forward glass clearance/window through the carrier.
4. Add positive carrier-to-Perspex hard-stop geometry.
5. Retain/adapt snap pins only as locating/light-retention features.
6. Delete the separate retainer bar.
7. Remove the Rev N dependency on the 1.10 mm thin front plate.
8. Remove the requirement to trim solder tips for panel clearance.
9. Retain the original 48.00 mm M2 interface.
10. Retain the existing bezel unless new test evidence requires a change.
11. Preserve active-area centring relative to the original Decca aperture.
12. Keep the design fully parametric in Fusion 360.

## 10. Validation requirements

Before Rev O is accepted for print, verify in CAD:

- carrier × Perspex: clear except intended seating faces;
- carrier × OLED glass: clear except intended non-load-bearing guidance;
- carrier × OLED PCB: correct support and clearance;
- carrier × header and solder joints: clear;
- OLED glass × Perspex: 0.15–0.30 mm target nominal gap;
- M2 fastener load does not pass through OLED glass;
- snap pins locate the PCB without excessive strain;
- no separate retainer is required;
- OLED can be inserted and removed from the rear without damaging glass or PCB;
- carrier seats flat against Perspex;
- screen active area remains centred behind the bezel/aperture;
- no unprintable thin slivers or unsupported features;
- normal FDM wall thickness restored in structural areas.

## 11. Prototype acceptance tests

First Rev O print should be treated as a geometry-validation prototype.

Check:

1. rear insertion/removal of OLED;
2. snap-pin location and handling retention;
3. carrier seating flat against Perspex;
4. actual OLED-to-Perspex gap;
5. active-area centring when powered;
6. bezel alignment;
7. M2 tightening does not change OLED depth or stress the module;
8. header and solder joints clear the Perspex and carrier;
9. no rattle when assembled;
10. no separate retainer required.

## 12. Design decision

Rev N should not receive further architecture-level iteration.

Rev O is the approved redesign direction: rear-loaded OLED PCB, positive PCB datum, carrier-to-Perspex hard stops, locating snap pins retained where useful, and no separate retainer bar.
