# Decca ESP32 Controller Housing Specification v1.3

**Status:** Rev A rejected for bulk. Rev B architecture approved; design-review findings addressed. **Physical prototype gates remain open** — nothing in this design has been printed or measured against hardware. Coupons required before any production print.  
**Scope:** Enclosure for the selected ESP32 DevKit and 30-pin terminal adapter only. The MOSFET board is excluded and remains separately mounted.

## Revision record

| Revision | Change |
|---|---|
| v1.0 | Initial housing specification. |
| v1.1 | Owner review rejects Rev A. Removes external lacing rails, mounting ears, USB plug, second clamp, four-screw lid, and sawtooth cable roofs. Introduces a shallow-base/deep-lid architecture, grouped-harness strain relief, two internal cabinet fixings, an integral fixed ledge plus one adjustable clamp, two lid screws plus locating hooks, and mandatory material-use gates. |
| v1.2 | Rev B architecture approved. Amends the prototype risks review found in it: strain relief must align with its own window and be checked as a fitted tie rather than an aperture; cabinet caps must be positively retained; the countersink must be sized from a declared maximum head envelope; the prototype tool must test the horizontal insert; the assembled electronics height becomes a release gate that blocks production printing; and real slicer evidence is required where the tooling exists. Envelope, volume and mass limits are unchanged. |
| v1.3 | The v1.2 cable-tie anchors were slender uprights of bare wall thickness, loaded near their tops. Adds section 5c: a cable-tie anchor is a compact continuation of the base wall with a declared minimum section in the cable-pull direction, declared minimum material around its aperture, a blended foot or root gusset, and generous root radii. Adds gates 28–30. Requires that the anchor be shown not to obstruct the terminals, the harness, the tie route or the lid's removal path, and that no verification claim be read as evidence of pull strength. Envelope, volume and mass limits are unchanged. |

## 1. Design intent

Produce a compact, serviceable, support-free FDM enclosure around the ESP32 and its selected terminal adapter. The enclosure shall protect the electronics, retain the PCB without loading components, permit terminal and USB access, manage the actual grouped Decca harnesses, and minimise printed material.

Rev A is not the geometry baseline. Its verified dimensions do not justify retaining bulky features. Rev B may replace the earlier geometry freely within the existing housing PR.

## 2. Rev B architecture

### 2.1 Production parts

- **Housing_Base:** shallow tray with a continuous insulating floor, four local PCB supports, an integral fixed PCB ledge, two internal cable-tie locations per long side, two recessed cabinet mounting points, and four heat-set-insert bosses in total: two for the lid and two for the adjustable clamp.
- **Housing_Lid:** deep removable cover providing the top and most side protection, USB service opening, ventilation, and open-bottom cable windows.
- **PCB_Clamp_Adjustable:** one short adjustable edge clamp retained by two M3 screws.
- **Cabinet_Fastener_Caps:** only if separate caps are required to insulate the recessed cabinet screw heads.
- **Carrier_Fit_Coupon** and **Insert_Fastener_Coupon:** two small prototype coupons. Between them they shall test the carrier edge and fixed ledge, the adjustable-clamp geometry, the vertical clamp insert, one **horizontal** lid-insert boss at production geometry, the cabinet countersink and the positively retained cap. They shall be materially minimal, and their combined solid volume shall not exceed that of the single gauge they replace.

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
10a. Each insulating cap shall be **positively retained**. A diametral clearance fit is not acceptable. Retention shall be by controlled light interference, by three or more compliant retention nibs, or by another clearly justified captive arrangement; it shall not depend on adhesive, and it shall not rely on a delicate snap feature that a 0.4 mm nozzle cannot print reliably. The cap shall remain centred over the fastener head, shall not fall out of an enclosure mounted vertically before the PCB is installed, shall remain removable for service without destroying the base, shall remain captive beneath the PCB after assembly, and shall preserve the section 3 underside clearance.
10b. The countersink shall be dimensioned from a **declared maximum screw-head envelope** plus a declared radial clearance, not from a nominal head diameter. The specification shall record the nominal head diameter, the maximum head envelope, the head angle and the clearance separately. The usable recess shall accommodate the maximum envelope plus its clearance with the head sitting fully below the cap, and shall retain at least 1.00 mm of floor beneath the countersink. Compatibility with any acquired screw shall not be claimed until that screw has been measured.
11. It is acceptable to remove the electronics before installing the cabinet fasteners.

## 5. Cable routing and strain relief

1. Model the wiring as grouped Decca harnesses, not as thirty independent wires.
2. Preserve screwdriver access to every terminal with the lid removed.
3. Use one or two simple open-bottom cable windows on each long side of the deep lid.
4. Cable windows shall begin at the lid's lower free edge so they print without bridging, support, or sawtooth roofs.
5. Provide two internal cable-tie positions per long side in the base — **one for each cable window**. Each tie position shall align with its own window and its own harness route, and lateral deviation between the terminal connection, the tie point and the exit window shall be minimised and reported. Cable ties shall wrap grouped bundles and transfer pull load into the base before conductors reach the terminals.
5a. The design shall carry **parameterised reference geometry for a real small cable tie**: nominal strap width and thickness, locking-head envelope, the complete loop around its associated bundle, the insertion route through the anchor, tightening-tool and finger access, and cut-tail clearance. The anchor aperture shall be open, at the strap's real cross-section, on **both** faces a fitter must reach — it is not sufficient for an aperture to exist.
5b. Verification of strain relief shall check the **fitted tie**: the loop around its bundle, the route through the anchor, head position and tool access. Checking only that an aperture and a tab exist is not sufficient.
5c. **Cable-tie anchor structure.** Each anchor shall be a compact, robust continuation of the base wall, not a slender upright:
   - one anchor per cable window, retaining the grouped-harness alignment of 5 and the practical tie route of 5a;
   - every feature inside the enclosure footprint;
   - at least **2.40 mm** of local material thickness in the cable-pull direction;
   - at least **2.00 mm** of material around the tie aperture, on every side of it;
   - a small internal triangular root gusset **or** a broad blended foot, whichever the surrounding geometry admits — and if neither is available in a given plane, the reason shall be stated;
   - generous root radii rather than a sharp tower-to-wall junction;
   - unsupported height minimised so far as terminal access and tie access allow;
   - the tie aperture retained at 4.00 mm for the modelled 2.50 × 1.10 mm strap, with its support-free peaked roof;
   - terminal screwdriver access and lid clearance preserved, **including the lid's removal path**, not only its seated position;
   - no external rails, no metal hardware, no bulky structures, and no decorative or unexplained projections;
   - additional production volume kept as low as practical, within the unchanged section 9.1 limits.

   These ties restrain lightweight low-voltage harnesses. The requirement is a feature that will not be snapped during wiring or normal handling — **not** one that resists abnormal pulling, and not a cable gland. **No pull-test coupon and no formal load test is required, and no geometric verification result shall be presented as evidence of physical pull strength.**

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

### 9.2 Slicer evidence

The solid-volume figure is a conservative design gate and shall be retained as
one. It is **not** predicted spool consumption and shall not be described as
such. Where a Bambu Studio or OrcaSlicer CLI is available, the complete
production set shall additionally be sliced with a declared profile — Bambu
P1S, PETG or PETG-HF, 0.4 mm nozzle, 0.2 mm layers, three perimeters, 15%
infill, no supports, each part in its stated orientation — and the build report
shall record filament grams and print time per part and in total, support usage
and any slicer warnings. If no suitable slicer is available that shall be
stated plainly.

### 9.3 Height release gate

The assumed 24.00 mm assembled electronics height shall not be changed without
a physical measurement. Because the closed height it produces leaves under
1 mm against the 36 mm limit, **the real assembled stack height shall be
measured before the base or the lid is printed.** No coupon validates it. This
is a release gate, not a design target.

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
- Carrier_Fit_Coupon
- Insert_Fastener_Coupon

Keep reference bodies visibly distinct from printable bodies. Do not export reference bodies as production meshes.

## 12. Deliverables

Keep established filenames where replacement avoids needless repository clutter, but identify the design and reports as Rev B.

Required:

- editable Fusion source;
- assembled housing STEP;
- separate base, lid, and adjustable-clamp STEP files;
- parametric generator and verification scripts;
- print-ready base, lid, adjustable-clamp, cap and prototype-coupon STL files;
- a cabinet-fastener-cap STL, which is mandatory because a recessed metal head installed after printing cannot be insulated by integral geometry;
- the slicer harness and its recorded output where a slicer CLI is available;
- updated build/verification report;
- updated review renders showing closed, open, exploded, cable-window, USB, cabinet-fixing and strain-relief views, and a close-up of the cable-tie anchor itself, uncluttered by keep-out volumes;
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
22. No forbidden rail, ear, sawtooth roof, USB plug, decorative projection, unexplained external feature, or superseded generated artefact exists.
23. Each cable tie is modelled as a fitted tie and its loop, insertion route, locking head, cut tail and tool access are all clear of every production part.
24. Each tie position aligns with its own cable window and its own bundle, both lie inside that window, and the bundle-to-tie lateral deviation is measured and reported.
25. Each cabinet cap is positively retained: the measured interference between the cap and its recess is greater than zero, and the cap remains removable through a pry feature.
26. The usable countersink accommodates the declared maximum head envelope plus its declared clearance. A recess smaller than that envelope is a failure.
27. The prototype coupons reproduce production geometry for the carrier edge and ledge, the vertical insert, the **horizontal** insert, the countersink and the retained cap, within the declared material budget.
28. Each cable-tie anchor's minimum local thickness in the cable-pull direction is measured and is at least 2.40 mm, and the material around its aperture is measured and is at least 2.00 mm on every side.
29. Each cable-tie anchor's root gusset or blended foot is present, and its radius, height and width are measured and reported.
30. No cable-tie anchor intersects the terminal, harness, lid or screwdriver keep-outs; the complete tie loop and tightening access remain valid; the lid's removal path clears every anchor; no part requires support; and the envelope, volume and mass limits of 9.1 still pass. Gates 28–30 measure geometry only and shall not be reported as proof of pull strength.

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
- PETG print quality is acceptable without supports;
- a **horizontal** heat-set insert can actually be driven into the coupon boss;
- the cabinet screw's real head diameter is inside the declared maximum
  envelope;
- the insulating cap presses in, stays in and comes out again on the real
  printer and filament;
- **the real assembled electronics height is measured.** This one is a release
  gate: the base and the lid shall not be printed until it is closed;
- the cable-tie anchors survive wiring and normal handling. Gates 28–30
  measure section, wall and blend; they do not measure strength, and no load
  test is required of them.

Record the results in the build report before release.

## 15. Change control

- Continue the work only in the dedicated housing branch and PR until prototype acceptance is complete.
- Do not merge the housing PR during the amendment sprint.
- Avoid unrelated wiring, firmware, or printing-work changes.
- Update the specification, generated CAD, verification scripts, exported artefacts, renders, build report, and PR description together.
- If any mandatory envelope or material gate cannot coexist with the clearance and service requirements, stop and document the conflict rather than silently relaxing the gate.
