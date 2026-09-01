# Decca ESP32 Controller Housing Specification v1.1

**Status:** Rev A rejected for bulk and filament consumption. Rev B prototype required.  
**Scope:** Enclosure for the selected ESP32 DevKit and 30-pin terminal adapter only. The MOSFET board is excluded and remains separately mounted.

## Revision record

| Revision | Change |
|---|---|
| v1.0 | Initial housing specification. |
| v1.1 | Owner review rejects Rev A. Removes external lacing rails, mounting ears, USB plug, second clamp, four-screw lid, and sawtooth cable roofs. Introduces a shallow-base/deep-lid architecture, grouped-harness strain relief, two internal cabinet fixings, an integral fixed ledge plus one adjustable clamp, two lid screws plus locating hooks, and mandatory material-use gates. |

## 1. Design intent

Produce a compact, serviceable, support-free FDM enclosure around the ESP32 and its selected terminal adapter. The enclosure shall protect the electronics, retain the PCB without loading components, permit terminal and USB access, manage the actual grouped Decca harnesses, and minimise printed material.

Rev A is not the geometry baseline. Its verified dimensions do not justify retaining bulky features. Rev B may replace the earlier geometry freely within the existing housing PR.

## 2. Rev B architecture

### 2.1 Production parts

- **Housing_Base:** shallow tray with a continuous insulating floor, four local PCB supports, an integral fixed PCB ledge, two internal cable-tie locations per long side, two recessed cabinet mounting points, and four heat-set-insert bosses in total: two for the lid and two for the adjustable clamp.
- **Housing_Lid:** deep removable cover providing the top and most side protection, USB service opening, ventilation, and open-bottom cable windows.
- **PCB_Clamp_Adjustable:** one short adjustable edge clamp retained by two M3 screws.
- **Cabinet_Fastener_Caps:** only if separate caps are required to insulate the recessed cabinet screw heads.
- **Carrier_Fit_Gauge:** small prototype gauge for validating the 65–67 mm carrier width range.

### 2.2 Explicitly forbidden features

Do not include:

- external cable-lacing rails;
- sawtooth, crenellated, or bridge-roof cable openings;
- external cabinet mounting ears or feet;
- decorative ribs, fins, tabs, or unexplained projections;
- a USB blanking plug;
- per-terminal cable slots or guides based on thirty separate wires;
- a second full-width removable PCB clamp;
- a four-corner lid screw pattern.

Every external structure must have a stated functional requirement and a verification check. If neither exists, remove it.

## 3. Reference geometry and clearances

Use repository source dimensions and existing measured references as the design basis:

| Item | Requirement |
|---|---:|
| Terminal-adapter starting envelope | 66 × 63 × 1.6 mm |
| Required space below PCB | 2.5 mm starting value |
| Required component space above PCB | 24 mm starting value |
| General XY fit clearance | 0.5 mm per constrained side |
| Minimum top clearance | 2.0 mm |
| Minimum clearance below lowest component/solder feature | 2.0 mm |
| Minimum USB opening | 14 × 9 mm |
| Minimum usable cable-window height | 10 mm |
| Adjustable carrier-width range | 65–67 mm |

Repository dimensions remain assumptions until the physical prototype gates are completed. Do not infer precise EN/BOOT button positions from photographs.

## 4. Base requirements

1. Nominal floor thickness: **1.6 mm**.
2. Use local ribs and pads only where required; do not thicken the complete floor.
3. Maintain at least 2.0 mm clearance from the lowest PCB, solder, or pin feature to the enclosure floor or insulated fastener cover.
4. Support the board at four local edge/corner regions.
5. Retain one short PCB edge beneath an integral fixed ledge.
6. Retain the opposite short edge with one adjustable clamp and two M3 screws.
7. The ledge and clamp shall bear only on clear PCB-edge regions. They shall not load the ESP32 module, sockets, terminal blocks, solder joints, or components.
8. Provide two recessed cabinet fixing points within the enclosure footprint, positioned near the short ends and outside electronics keep-outs.
9. Do not use external mounting ears.
10. Cabinet fastener heads shall remain below the PCB support plane and shall be electrically isolated by integral geometry or printed insulating caps.
11. It is acceptable to remove the electronics before installing the cabinet fasteners.

## 5. Cable routing and strain relief

1. Model the wiring as grouped Decca harnesses, not as thirty independent wires.
2. Preserve screwdriver access to every terminal with the lid removed.
3. Use one or two simple open-bottom cable windows on each long side of the deep lid.
4. Cable windows shall begin at the lid's lower free edge so they print without bridging, support, or sawtooth roofs.
5. Provide two internal cable-tie positions per long side in the base. Cable ties shall wrap grouped bundles and transfer pull load into the base before conductors reach the terminals.
6. Do not provide external rails or terminal-indexed slots.
7. Window size and tie routing shall not pinch the harness when the lid is installed.

## 6. USB and controls

1. Provide an unobstructed USB service opening of at least 14 × 9 mm, aligned to the repository reference model.
2. Do not provide a separate USB blanking plug.
3. An optional small recessed label may read **USB / DISCONNECT 5V**.
4. Do not add EN or BOOT access holes to the lid until their positions are physically measured. The removable lid provides prototype access.

## 7. Ventilation and antenna

1. Use a modest set of simple top ventilation slots only.
2. Do not duplicate large ventilation arrays on the sides.
3. Keep fasteners, inserts, thick ribs, and cabinet metal outside the ESP32 antenna keep-out.
4. Nominal lid thickness over the antenna: 1.6 mm.
5. Ventilation shall remain adequate for the Decca controller's expected load without turning the lid into an unnecessarily large grille.

## 8. Lid retention

1. Nominal lid top thickness: **1.6 mm**.
2. Nominal lid skirt thickness: **1.2 mm**, suitable for three 0.4 mm perimeters.
3. Nominal lid/base overlap: **4.0 mm**.
4. Nominal fit allowance: **0.25 mm per mating side**, subject to the printer coupon.
5. Retain the lid with two M3 screws at one short end and two non-stressed locating hooks at the opposite end.
6. The hooks guide and locate the lid; they are not fatigue-loaded snap latches.
7. Do not use four corner screws, large corner piers, decorative bulk, or a large raised logo.

## 9. Envelope and material-use gates

The Rev A envelope of approximately 105 × 77 × 38.3 mm and approximately 68 cm³ of printed material is rejected.

### 9.1 Mandatory limits

| Metric | Mandatory limit | Preferred target |
|---|---:|---:|
| Complete outside envelope | ≤85 × 75 × 36 mm | smaller where clearances permit |
| Production-part solid volume | ≤35 cm³ | ≤30 cm³ |
| Estimated PETG mass at 1.27 g/cm³ | ≤45 g | ≤38 g |
| Base solid volume | — | ≤15 cm³ |
| Lid solid volume | — | ≤18 cm³ |
| Adjustable clamp solid volume | — | ≤2 cm³ |

The production-part total includes the base, lid, adjustable clamp, and mandatory fastener caps. It excludes the fit gauge and non-printing reference bodies.

No external feature may project beyond the main body envelope.

The generator and verifier shall report per-part and total solid volume plus estimated PETG mass. A production volume above 35 cm³ or estimated mass above 45 g is a failed gate, not a warning.

## 10. FDM design rules

- Material: PETG or PETG-HF.
- Nozzle: 0.4 mm.
- Layer height: 0.2 mm.
- Use three perimeters for the lid skirt; use four only at local bosses and hooks when structurally necessary.
- Use 15–20% infill only where slicer infill is unavoidable.
- Prefer thin shells, local ribs, and isolated pads over thick solids.
- No internal support material shall be required.
- Print the base floor-down.
- Print the lid top-face-down. Its open-bottom cable windows therefore grow upward without roofs or support.
- Orient the adjustable clamp for strength across its loaded section.

## 11. CAD component structure

Decca_ESP32_Controller_Housing

- REF_ESP32_DevKit_V1_30Pin
- REF_30Pin_Terminal_Adapter
- REF_Wired_Keepouts
- Housing_Base
- Housing_Lid
- PCB_Clamp_Adjustable
- Cabinet_Fastener_Caps
- Carrier_Fit_Gauge

Keep reference bodies visibly distinct from printable bodies. Do not export reference bodies as production meshes.

## 12. Deliverables

Keep established filenames where replacement avoids needless repository clutter, but identify the design and reports as Rev B.

Required:

- editable Fusion source;
- assembled housing STEP;
- separate base, lid, and adjustable-clamp STEP files;
- parametric generator and verification scripts;
- print-ready base, lid, adjustable-clamp, and fit-gauge STL files;
- cabinet-fastener-cap STL only if separate caps are required;
- updated build/verification report;
- updated review renders showing closed, open, exploded, cable-window, USB, cabinet-fixing, and strain-relief views;
- a material table showing every production part's volume and estimated PETG mass.

Remove obsolete Rev A production artefacts that would be mistaken for current deliverables. Do not deliver a fixed-clamp STL or USB-plug STL.

## 13. Automated verification gates

The verifier shall fail the build unless all applicable checks pass:

1. Every production mesh is manifold and watertight.
2. The base has a continuous insulating floor.
3. Electronics underside clearance is at least 2.0 mm.
4. Lid top clearance is at least 2.0 mm.
5. No fastener, insert, hook, rib, cap, or enclosure surface intersects an electronics keep-out.
6. All terminal screws remain accessible with the lid removed.
7. Each cable window provides at least 10 mm usable height.
8. The lid does not pinch grouped harness keep-outs.
9. Each internal strain-relief position accepts its cable tie and transfers pull load to the base.
10. The USB service envelope is clear through the opening.
11. The ESP32 antenna keep-out is clear of metal, inserts, and thick structure.
12. Lid overlap and fit allowance meet specification.
13. The fixed ledge and adjustable clamp contact only approved PCB-edge regions.
14. The clamp accommodates carrier widths from 65 to 67 mm.
15. The retention system does not load the ESP32, sockets, terminals, solder joints, or components.
16. Both cabinet fastener heads are recessed, insulated, and outside electronics keep-outs.
17. The two lid screws and two locating hooks permit a valid installation/removal sequence.
18. No production part requires slicer support.
19. The complete outside envelope is no greater than 85 × 75 × 36 mm.
20. Production-part solid volume is no greater than 35 cm³.
21. Estimated PETG mass is no greater than 45 g.
22. No forbidden rail, ear, sawtooth roof, USB plug, decorative projection, or unexplained external feature exists.

## 14. Prototype acceptance gates

The CAD revision is not production-approved until physical checks confirm:

- the fit gauge accepts the real terminal adapter without stress or excessive play;
- USB insertion and removal are unobstructed;
- all terminal screws are serviceable;
- grouped H1–H6 harnesses route through the windows and strain relief without pinch;
- lid assembly does not disturb wiring;
- cabinet fastener installation and insulation are practical;
- the board survives moderate cable pull without movement;
- antenna performance is acceptable;
- PETG print quality is acceptable without supports.

Record the results in the build report before release.

## 15. Change control

- Continue the work only in the dedicated housing branch and PR until prototype acceptance is complete.
- Do not merge the housing PR during the amendment sprint.
- Avoid unrelated wiring, firmware, or printing-work changes.
- Update the specification, generated CAD, verification scripts, exported artefacts, renders, build report, and PR description together.
- If any mandatory envelope or material gate cannot coexist with the clearance and service requirements, stop and document the conflict rather than silently relaxing the gate.
