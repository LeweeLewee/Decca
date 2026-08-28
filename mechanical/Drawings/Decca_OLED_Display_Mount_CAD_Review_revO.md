# Decca OLED Display Mount — CAD Redesign Specification (Rev O)

Supersedes Rev N as the active design direction for the OLED carrier.

Platform: Autodesk Fusion 360. Manufacture: FDM 3D print.

## 1. Reason for redesign

Physical print-and-fit iterations of Rev N showed that the front-loaded architecture had become constrained by OLED depth. Rev O changes the topology rather than further tuning the Rev N front plate and retainer arrangement.

The governing design objective is to place the OLED glass close to the inside face of the original Perspex while keeping all M2 screw preload out of the OLED glass and PCB.

## 2. Rev O architecture — mandatory topology

The OLED module shall load into the carrier from the rear.

The carrier shall sit behind the OLED PCB. The OLED glass/display projects forwards towards the inside face of the Perspex.

**No carrier front plate, seating land, shoulder, lip or other structural retention feature may occupy the space between the front face of the OLED PCB and the Perspex.** This explicitly rejects the failed Rev O implementation that recreated the Rev N 1.10 mm forward retention plane as short seating lands.

The OLED shall **not** be captured by the carrier alone. Final axial capture occurs only when the carrier is mounted to the Perspex. Snap pins or equivalent features may provide X/Y location and light handling retention before installation, but they are not the primary structural retention system.

The carrier/Perspex assembly therefore performs two independent functions:

1. **Structural load path:** M2 screw → carrier structural bosses / hard stops → Perspex.
2. **OLED location and capture:** Perspex-side boundary → OLED module → rear PCB support geometry in the carrier.

The glass must never be the structural compression stop.

## 3. Existing Decca interface — measured values are authoritative

Use the measured and print-confirmed dimensions already recorded in the repository, not the superseded Spec v1.0 values:

- Original Perspex thickness: 3.00 mm.
- Existing aperture: **35.20 mm W × 15.30 mm H**.
- Existing M2 fixing-hole pitch: **49.00 mm horizontal**.
- Fixing-hole centreline: vertically centred on the display aperture.
- No additional holes, cutting or irreversible modification to the original Perspex.
- M2 screws enter from the front of the Perspex and fasten into the rear carrier.

If any later physical measurement contradicts these values, the physical measurement wins and the parameter is updated explicitly.

## 4. Front bezel

The front bezel remains a separate cosmetic trim around the aperture only.

It must not include the M2 fixing holes and must not carry structural load. Retain the validated Rev N bezel unless physical testing identifies a specific reason to change it.

## 5. OLED loading, datum and retention

### 5.1 Rear loading

The OLED PCB shall insert into the carrier from the rear. The carrier shall provide open rear access around the header and solder joints.

### 5.2 Positive OLED Z datum from behind

OLED fore/aft position shall be established by **rear PCB support lands / shoulders acting on the rear face or rear-safe areas of the PCB**.

These support features may locate the PCB in Z but must not project ahead of the PCB front face.

The intended section is therefore:

```text
Perspex
  |
small controlled optical gap
  |
OLED glass
  |
OLED PCB
  ^
rear PCB support lands / datum
  |
rear carrier
```

Separate carrier structural bosses / hard stops shall contact the Perspex directly outside the OLED module envelope and carry the M2 preload.

### 5.3 Locating snap pins

The existing snap-pin concept may be retained only as a locating and light-retention mechanism.

Design intent:

- locate the PCB consistently in X/Y;
- prevent the loose OLED falling away during handling and installation;
- avoid significant PCB bending or insertion force;
- avoid any path where bonded glass must sweep past a barb or rigid post;
- do not rely on snap hooks for final axial capture once installed.

A full swept insertion/removal corridor check is mandatory before print release.

### 5.4 Retainer bar

Delete the separate retainer bar from Rev O.

The assembled carrier/Perspex geometry provides final axial capture of the OLED.

## 6. Optical depth and glass protection

Target nominal glass-to-Perspex gap: **0.15–0.30 mm**.

Select the final nominal from measured OLED geometry and realistic FDM tolerance. A nominal around 0.30 mm is acceptable if required for robustness.

Critical requirements:

- the OLED glass must not become the structural stop when the M2 screws are tightened;
- tightening the M2 screws must not alter OLED depth;
- there shall be no carrier material between the OLED PCB front face and Perspex used to establish this gap.

## 7. Solder-tip constraint — resolved by module preparation

The physical OLED solder tips project more than 2 mm from the PCB front face. They can be trimmed to a **maximum of 1.50 mm proud**.

This is an accepted assembly preparation step and shall be treated as the design input for Rev O.

Accordingly:

- model `oled_tip_proud = 1.50 mm maximum`;
- provide sufficient local carrier clearance around the solder joints and header;
- do not redesign the carrier topology merely to accommodate untrimmed >2 mm tips;
- verify that the trimmed 1.50 mm tips do not interfere with the Perspex or any carrier feature in the final assembly or insertion path.

If the measured glass proud and selected optical gap still make 1.50 mm incompatible with the Perspex, report that explicitly before changing architecture.

## 8. Carrier structural design

Rev O should restore sensible FDM section thicknesses behind and around the OLED module.

Guidance:

- approximately 2.0–3.0 mm structural wall thickness where geometry allows;
- reinforce M2 boss regions appropriately;
- use direct carrier-to-Perspex hard stops outside the OLED module envelope;
- avoid unnecessary thin membranes around the display window;
- leave rear access around the header and solder joints;
- maintain cable/header clearance and serviceability;
- minimise part count and avoid a separate retainer.

## 9. Required CAD changes from Rev N / failed Rev O implementation

1. Rear-load the OLED PCB.
2. Keep the carrier and all structural PCB datum geometry behind the PCB front face.
3. Establish OLED Z position from rear PCB support geometry.
4. Provide a clear forward path for the OLED glass with no forward PCB seating lands.
5. Add separate positive carrier-to-Perspex hard-stop geometry to carry M2 preload.
6. Retain/adapt snap pins only for X/Y location and light handling retention.
7. Delete the separate retainer bar.
8. Model solder tips at 1.50 mm maximum after trimming.
9. Use the measured 49.00 mm M2 pitch and 35.20 × 15.30 mm aperture.
10. Retain the existing bezel unless new test evidence requires a change.
11. Preserve active-area centring relative to the original Decca aperture.
12. Keep the design fully parametric in Fusion 360.

## 10. Mandatory CAD validation gate

Before Rev O is accepted for print, verify all of the following on the actual generated geometry:

- carrier × Perspex: clear except intended structural seating faces;
- no carrier geometry ahead of the OLED PCB front face within the OLED module envelope;
- rear PCB support contacts only intended PCB support areas;
- carrier × OLED glass: clear throughout insertion, seating and removal;
- carrier × OLED PCB: correct rear support and X/Y location;
- carrier × header and trimmed 1.50 mm solder joints: clear;
- trimmed solder joints × Perspex: clear;
- OLED glass × Perspex: 0.15–0.30 mm nominal gap;
- M2 load path terminates through carrier hard stops into Perspex, not OLED glass or PCB;
- snap features locate the PCB without excessive strain;
- OLED can be inserted and removed from the rear without bonded glass sweeping through a rigid barb/post envelope;
- carrier seats flat against Perspex;
- screen active area remains centred behind the bezel/aperture;
- no unprintable thin slivers or unsupported critical features;
- normal FDM wall thickness is restored in structural areas.

**A static final-position interference check is insufficient. A swept insertion/removal corridor check is mandatory.**

## 11. Design-review gate before Fusion build

Before generating the next Fusion model, produce and review a simple side-section / topology diagram showing:

- Perspex;
- optical gap;
- OLED glass;
- PCB;
- rear PCB support datum;
- structural carrier hard stops to Perspex;
- M2 load path;
- snap/location features.

The CAD build must not proceed if that section contains any carrier land, plate or shoulder between the PCB front face and Perspex.

## 12. Prototype acceptance tests

First corrected Rev O print is a geometry-validation prototype. Check:

1. rear insertion/removal of OLED;
2. snap-pin location and handling retention;
3. carrier seating flat against Perspex;
4. actual OLED-to-Perspex gap;
5. active-area centring when powered;
6. bezel alignment;
7. M2 tightening does not change OLED depth or stress the module;
8. trimmed solder joints and header clear the Perspex and carrier;
9. no rattle when assembled;
10. no separate retainer required.

## 13. Design decision

Rev N should receive no further architecture-level iteration.

The failed first Rev O implementation is rejected because it recreated the critical Rev N geometry as **1.10 mm forward PCB seating lands** and attempted to capture the OLED within the carrier alone.

The approved Rev O direction is: **rear-loaded OLED, rear PCB Z support, separate carrier-to-Perspex structural hard stops, no carrier geometry ahead of the PCB within the OLED envelope, locating/light-retention snap features only, trimmed solder tips at 1.50 mm maximum, and no separate retainer bar.**
