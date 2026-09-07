# Decca ESP32 Controller Housing Specification v1.7

**Status:** **REV C BUILT to this specification, 2026-09-06. Prototype gates remain open; nothing is approved for printing.** Rev A was rejected for bulk. Rev B is rejected because it routes grouped harnesses above the terminal blocks instead of modelling conductors entering the real screw terminals horizontally from both long sides. No Rev B housing part or coupon is approved for printing. The owner has supplied the macro board geometry and released replacement CAD to proceed.

**Scope:** Enclosure for the selected 30-pin ESP32 DevKit fitted to the acquired DORHEA 30-pin screw-terminal adapter only. The MOSFET board is excluded and remains separately mounted.

## Revision record

| Revision | Change |
|---|---|
| v1.0 | Initial housing specification. |
| v1.1 | Owner review rejects Rev A. Removes external lacing rails, mounting ears, USB plug, second clamp, four-screw lid, and sawtooth cable roofs. Introduces a shallow-base/deep-lid architecture, grouped-harness strain relief, two internal cabinet fixings, an integral fixed ledge plus one adjustable clamp, two lid screws plus locating hooks, and mandatory material-use gates. |
| v1.2 | Rev B architecture approved. Amends the prototype risks review found in it: strain relief must align with its own window and be checked as a fitted tie rather than an aperture; cabinet caps must be positively retained; the countersink must be sized from a declared maximum head envelope; the prototype tool must test the horizontal insert; the assembled electronics height becomes a release gate that blocks production printing; and real slicer evidence is required where the tooling exists. Envelope, volume and mass limits are unchanged. |
| v1.3 | The v1.2 cable-tie anchors were slender uprights of bare wall thickness, loaded near their tops. Adds section 5c: a cable-tie anchor is a compact continuation of the base wall with a declared minimum section in the cable-pull direction, declared minimum material around its aperture, a blended foot or root gusset, and generous root radii. Adds gates 28–30. Requires that the anchor be shown not to obstruct the terminals, the harness, the tie route or the lid's removal path, and that no verification claim be read as evidence of pull strength. Envelope, volume and mass limits are unchanged. |
| v1.4 | Identifies the acquired adapter as the DORHEA 30-pin terminal adapter shown at 66 × 63 mm. Rejects Rev B after confirming that its harness and tie geometry is based on the wrong connection path. External conductors enter the green screw-terminal blocks horizontally through their outward-facing long-side ports; the black vertical sockets are only for the ESP32 module. Replaces the elevated cable-window and tie-tower requirements with direct terminal-entry corridors, installed-wire and ferrule keep-outs, a cover removable with the wiring connected, and optional low-profile strain relief only after the conductors have cleared the terminal mouths. Existing envelope and material limits remain design targets, but all Rev B production and coupon geometry is superseded. |
| v1.5 | Records the owner's physical measurement of **20 mm overall height** for the complete DORHEA adapter plus fitted ESP32. This supersedes Rev B's unverified 24 mm “above PCB” assumption and closes the gross assembled-height measurement gate. The 20 mm value is an overall envelope, not an above-PCB dimension; replacement CAD shall reference it from the assembly's actual lowest underside feature to its highest point. Terminal-port and underside measurements remain open. |
| v1.6 | Records the owner's macro measurements of 2026-09-06 — PCB outline 66 × 63 mm, mounting-hole centre pitch 58 × 56 mm *(re-measured the same day as **60 mm across × 57 mm along** — see §3; the 58 × 56 pair left 1.00 mm unaccounted for)*, terminal blocks 55 mm outer face to outer face, row length 53 mm, block height 9 mm, and the wire entry sitting just above the base of the block. **Closes the §15 measurement gate and releases replacement CAD.** Supersedes the v1.5 §5.3 requirement for dimensioned port geometry: the terminal-port bore size and internal insertion depth do not drive housing geometry and are out of scope. In their place §5.3 now requires the housing to clear the **entire terminal-block height** across the full row length on both long sides, which is conservative whatever the port position, and to declare its own straight external run as a routing value. Envelope, volume and mass limits are unchanged. |
| v1.7 | **Replaces the adjustable clamp with hole-located retention**, adds §4.12, the lid-screw boss wall rule, and adds §14.0, which makes a prototype print of a small, cheap part a legitimate way to close a measurement gate rather than something that has to wait for one. The owner's 2026-09-06 measurements close the last gap: a 60 × 57 mm mounting-hole pitch with M3 holes, every hole 3.00 mm from its nearest board edge. §4.6 now requires the carrier to be located by features engaging its own mounting holes rather than gripped by its opposite short edge, and §4.5's fixed ledge is retained unchanged. Screws through those holes are **prohibited** and the reason is recorded in §4.6: the binding clearance is not the terminal block but the outermost conductor, 3.767 mm from the hole centre, which an M3 head of radius 2.75 fouls by 0.28 mm against a 2.60 mm ferrule. The adjustable-carrier-range requirement, the clamp's volume allowance, its print orientation, its STEP and STL deliverables and gate 14 all go with it; gate 14 becomes the hole-location gate. Envelope, volume and mass limits are unchanged, and the design moves further inside them. |

## 1. Design intent

Produce a compact, serviceable, support-free FDM enclosure around the ESP32 and its selected terminal adapter. The enclosure shall protect the electronics, retain the PCB without loading components, permit terminal and USB access, manage the actual grouped Decca harnesses, and minimise printed material.

Neither Rev A nor Rev B is the geometry baseline. A replacement design may reuse independently valid clearances, fastener concepts and material limits, but it shall not inherit either revision's cable-routing geometry.

## 2. Replacement architecture

### 2.1 Production parts

- **Housing_Base:** material-efficient tray with a continuous insulating floor, local PCB supports and retention, and internal cabinet mounting points. Its long-side geometry shall leave every required terminal mouth, ferrule and straight conductor approach unobstructed. It shall not place walls, tie towers or other features between a terminal mouth and the exterior.
- **Housing_Lid:** removable top cover providing top protection, USB service access and only the side coverage compatible with the horizontal terminal-entry corridors. It shall be removable and refittable while the terminal wiring remains connected.
- **Cabinet_Fastener_Caps:** only if separate caps are required to insulate the recessed cabinet screw heads.
- **Prototype coupons:** define only after the replacement production geometry exists. Reuse a coupon only if it reproduces unchanged production geometry. The Rev B coupons are superseded and shall not be printed as evidence for the replacement design.

### 2.2 Explicitly forbidden features

Do not include:

- external cable-lacing rails;
- sawtooth, crenellated, or bridge-roof cable openings;
- external cabinet mounting ears or feet;
- decorative ribs, fins, tabs, or unexplained projections;
- a USB blanking plug;
- per-terminal cable slots or guides based on thirty separate wires;
- any wall, skirt, tie anchor or other feature obstructing the horizontal conductor path into a screw-terminal mouth;
- any design that assumes the external wiring connects to the black vertical ESP32 sockets;
- any design that forces a conductor to turn upwards, downwards or sideways immediately after leaving a terminal mouth;
- elevated tie towers positioned between the terminal blocks and the enclosure exterior;
- a second full-width removable PCB clamp;
- a four-corner lid screw pattern.

Every external structure must have a stated functional requirement and a verification check. If neither exists, remove it.

## 3. Reference geometry and clearances

Use repository source dimensions and existing measured references as the design basis:

| Item | Requirement |
|---|---:|
| Selected terminal adapter | DORHEA 30-pin GPIO breakout / 1-into-2 terminal adapter |
| PCB plan outline | **63 mm ALONG the rows × 66 mm ACROSS them — owner-measured 2026-09-06**, axis assignment corrected by the owner the same day. The 66 mm is measured from one connector side to the other. |
| Terminal arrangement | 15 green screw terminals on each long side; screws operated from above; conductors enter horizontally through the outward-facing side ports |
| ESP32 connection | Two black vertical 15-pin sockets accept the ESP32 DevKit; these sockets are not external wiring points |
| Supplier image's additional dimension | 25 mm, reference only; datums are ambiguous and the value shall not drive CAD |
| Terminal blocks, outer face to outer face | **55 mm — owner-measured 2026-09-06**, so each block face sits **5.5 mm inboard** of its long PCB edge |
| Terminal-block row length | **53 mm — owner-measured 2026-09-06**, leaving 5.0 mm of clear board beyond each row end |
| Terminal-block height | **9 mm — owner-measured 2026-09-06** |
| Terminal width | approximately 3 mm each; consistent with 53 ÷ 15 = 3.53 mm pitch |
| Conductor entry position | **just above the base of the terminal block — owner, 2026-09-06.** Qualitative and sufficient: see §5.3 |
| Mounting-hole centre pitch | **60 mm across × 57 mm along — owner-measured 2026-09-06**, re-measured the same day and superseding an earlier 58 × 56 reading that left 1.00 mm unaccounted for. On the recorded 66 × 63 board this puts every hole **3.00 mm from its nearest edge on both axes**, and 2.50 mm outboard of the nearest block face. **Hole diameter still not measured**, and it alone decides whether hole-based retention could replace §4.5–4.6. |
| Adapter PCB thickness | 1.6 mm starting value; physically measure |
| Terminal-port bore size and internal insertion depth | **OUT OF SCOPE, owner 2026-09-06.** They do not drive housing geometry; §5.3 clears the whole block height instead |
| Corner mounting-hole size | **M3 — owner, 2026-09-06.** The screw size, not a calliper reading of the bore; Ø3.20 standard clearance is recorded as the working starting value. Hole-based retention is now geometrically possible — a plain M3 head clears the nearest block corner by 0.45 mm — but **§4.5–4.6 still forbid it** until they are amended. See the measurement request §10. |
| Complete adapter plus fitted ESP32 height | **20 mm overall — physically measured by the owner, 2026-09-05** |
| Required space below PCB | 2.5 mm starting value |
| General XY fit clearance | 0.5 mm per constrained side |
| Minimum top clearance | 2.0 mm |
| Minimum clearance below lowest component/solder feature | 2.0 mm |
| Minimum USB opening | 14 × 9 mm |
| Lid-screw heat-set insert | **Hanglife M3 threaded — owner, 2026-09-06.** Two off, vertical, in the +X lid-screw bosses. The **bore** is a starting value at Ø4.00 × 5.00 deep and shall be re-derived from the acquired insert's measured length and outer diameter before release. |
| Carrier location | **By the measured mounting holes — §4.6.** No adjustable range is required or permitted: the board's plan dimensions and its hole pitch are both measured, so there is nothing left for an adjustment to absorb. |

Supplier dimensions and repository dimensions remain assumptions until checked against the acquired board. Do not infer the terminal-port centre height, mounting-hole pitch, precise EN/BOOT positions or underside keep-outs from the listing photograph.

## 4. Base requirements

1. Nominal floor thickness: **1.6 mm**.
2. Use local ribs and pads only where required; do not thicken the complete floor.
3. Maintain at least 2.0 mm clearance from the lowest PCB, solder, or pin feature to the enclosure floor or insulated fastener cover.
4. Support the board at four local edge/corner regions.
5. Retain one short PCB edge beneath an integral fixed ledge.
6. Locate the carrier at the opposite short end by **integral posts engaging its own mounting holes**. The posts shall be sized to fit the reported M3 bore with at least 0.20 mm of radial clearance whether that bore is 3.00 or 3.20 mm, shall engage the full carrier thickness and stand at least 1.00 mm proud of it, and shall carry no fastener of any kind.
6a. **No screw shall pass through a carrier mounting hole.** The constraint is not the terminal block, which a head clears: a corner hole is outboard of the block on both axes, so a head meets the block's corner at 3.202 mm and an M3 cap head of radius 2.75 clears it by 0.45 mm. The constraint is the **outermost conductor**, whose axis lies 3.767 mm from the hole centre; against the declared 2.60 mm ferrule the same head fouls it by 0.28 mm. A 2.60 mm post clears it by 1.17 mm. Any future proposal to fasten through these holes shall re-derive this clearance against the conductor and ferrule actually installed.
6b. Posts shall be placed only where the carrier can be fitted and removed. Where a fixed ledge requires the carrier to translate at its final height, that end shall carry no post, and the tilt needed to clear the posts at the opposite end shall be shown not to bind the carrier beneath the ledge.
7. The ledge and posts shall bear only on clear PCB-edge regions and the bores of the mounting holes. They shall not load the ESP32 module, sockets, terminal blocks, solder joints, or components.
8. Provide two recessed cabinet fixing points within the enclosure footprint, positioned near the short ends and outside electronics keep-outs.
9. Do not use external mounting ears.
10. Cabinet fastener heads shall remain below the PCB support plane and shall be electrically isolated by integral geometry or printed insulating caps.
10a. Each insulating cap shall be **positively retained**. A diametral clearance fit is not acceptable. Retention shall be by controlled light interference, by three or more compliant retention nibs, or by another clearly justified captive arrangement; it shall not depend on adhesive, and it shall not rely on a delicate snap feature that a 0.4 mm nozzle cannot print reliably. The cap shall remain centred over the fastener head, shall not fall out of an enclosure mounted vertically before the PCB is installed, shall remain removable for service without destroying the base, shall remain captive beneath the PCB after assembly, and shall preserve the section 3 underside clearance.
10b. The countersink shall be dimensioned from a **declared maximum screw-head envelope** plus a declared radial clearance, not from a nominal head diameter. The specification shall record the nominal head diameter, the maximum head envelope, the head angle and the clearance separately. The usable recess shall accommodate the maximum envelope plus its clearance with the head sitting fully below the cap, and shall retain at least 1.00 mm of floor beneath the countersink. Compatibility with any acquired screw shall not be claimed until that screw has been measured.
11. It is acceptable to remove the electronics before installing the cabinet fasteners.
12. Each lid-screw boss shall **centre its insert bore** and retain at least **1.20 mm of wall around that bore in every direction**. A heat-set insert expands the surrounding plastic as it is driven in; a boss that is thin on one face splits there. The wall shall be re-checked against the acquired insert's measured outer diameter, not only against the modelled bore.

## 5. Cable routing and strain relief

1. Treat the selected adapter's green screw-terminal blocks as the external electrical connection. Conductors enter their ports **horizontally from the two long sides**. The black vertical sockets are used only to mount the ESP32 module.
2. Model a parameterised wire-and-ferrule envelope for every terminal used by the Decca wiring. Each envelope shall include the stripped/ferruled end inside the block, the insulated conductor outside it and a straight installation corridor from the terminal mouth to the enclosure exterior.
3. **The housing shall clear the entire measured terminal-block height across the full row length on both long sides.** This supersedes the v1.5 requirement for a dimensioned port centre height, bore size and internal insertion depth, which the owner has ruled out of scope because they do not drive housing geometry. Clearing the whole block is conservative wherever the port actually sits, so no later port measurement can invalidate the geometry. The minimum straight external run before a conductor may bend is a **declared routing value owned by this design**, parameterised, stated in the build report and verified — it is not a board measurement. The conductor envelope follows the wire and ferrule actually installed, not the terminal bore.
4. No housing surface, lid skirt, tie feature or fastener shall intersect a terminal-entry corridor. A conductor shall not be required to bend immediately on leaving its terminal mouth merely to clear the enclosure.
5. Preserve direct top access to every terminal screw with the cover removed. A fitted conductor and ferrule shall be insertable, clamped, released and withdrawn using ordinary tools without removing the adapter from the base.
6. Side openings may be continuous along each terminal row or divided into a small number of grouped openings. Choose the simplest support-free geometry that protects the board ends while keeping the terminal mouths and conductor corridors clear. Do not reproduce Rev B's elevated windows above the terminal blocks.
7. Model the conductors individually through the terminal-entry zone because their physical positions are fixed by the terminals. They may merge into the named grouped H1–H6 harness envelopes only after clearing the terminal mouths and the required straight approach distance.
8. The cover shall lift off and refit with all production terminal conductors connected. Its seated position and complete removal path shall clear the terminal screws, conductor insulation, ferrules and grouped harnesses.
9. Integrated strain relief is optional. First determine whether the existing cabinet wiring can be secured immediately outside the housing without adding printed structure. If housing-mounted restraint is justified, locate a small low-profile tie slot or anchor **downstream of the straight terminal-entry zone**. It shall not sit between the terminal mouths and the exterior, force an immediate cable bend, or require a tall tower.
10. Any modelled restraint shall suit only lightweight low-voltage wiring and ordinary assembly handling. No pull test, load test or dedicated strain-relief coupon is required.
11. Do not provide external rails, per-terminal printed guides, decorative projections or cable features without a stated installation need.

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
2. Nominal lid skirt thickness where a skirt is permitted: **1.2 mm**, suitable for three 0.4 mm perimeters.
3. Use overlap only at the short ends, corners or other regions that do not obstruct terminal-entry corridors. Rev B's continuous deep long-side skirt is not a requirement.
4. Nominal fit allowance: **0.25 mm per mating side**, subject to the printer coupon.
5. Prefer two M3 screws at one short end and two non-stressed locating hooks at the opposite end if the arrangement remains clear of the USB connector, wiring and removal path. An equally simple two-fastener arrangement is acceptable if the replacement geometry requires it.
6. The hooks guide and locate the lid; they are not fatigue-loaded snap latches.
7. Do not use four corner screws, large corner piers, decorative bulk, or a large raised logo.
8. The cover shall be removable without disconnecting any screw-terminal conductor.

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

The production-part total includes the base, lid, and mandatory fastener caps. It excludes the prototype coupons and non-printing reference bodies.

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

### 9.3 Measured assembly height

The complete DORHEA adapter plus fitted ESP32 is **20.00 mm high overall**, from
the owner's physical measurement on 2026-09-05. This supersedes Rev B's
unverified `assembly_above_pcb_h = 24.00 mm` assumption and closes the prior
gross-height release gate.

The two values are not interchangeable: 20.00 mm is the complete assembly
envelope, while the old 24.00 mm parameter purported to start at the adapter
PCB top face. Replacement CAD shall establish the real lowest underside datum
and model a 20.00 mm overall reference assembly from that datum, plus the
specified floor and top clearances. Do not subtract an assumed PCB thickness or
underside allowance to manufacture a new “above PCB” value.

## 10. FDM design rules

- Material: PETG or PETG-HF.
- Nozzle: 0.4 mm.
- Layer height: 0.2 mm.
- Use three perimeters for the lid skirt; use four only at local bosses and hooks when structurally necessary.
- Use 15–20% infill only where slicer infill is unavoidable.
- Prefer thin shells, local ribs, and isolated pads over thick solids.
- No internal support material shall be required.
- Print the base floor-down.
- Choose the cover orientation from the replacement geometry and verify it needs no support. Do not retain Rev B's top-face-down orientation merely to preserve its obsolete elevated cable windows.

## 11. CAD component structure

Decca_ESP32_Controller_Housing

- REF_ESP32_DevKit_V1_30Pin
- REF_30Pin_Terminal_Adapter
- REF_Terminal_Entry_Corridors
- REF_Installed_Wires_And_Ferrules
- REF_Grouped_Harness_Keepouts
- Housing_Base
- Housing_Lid
- PCB_Clamp_Adjustable
- Cabinet_Fastener_Caps

Rev C defines no prototype coupons: §2.1 requires a coupon to reproduce
*replacement* production geometry, and the Rev B coupons are superseded. One is
defined only when the owner elects to print it.

Keep reference bodies visibly distinct from printable bodies. Do not export reference bodies as production meshes.

## 12. Deliverables

Keep established filenames where replacement avoids needless repository clutter, but identify the replacement as a post-Rev-B redesign and state clearly that earlier Rev B exports are superseded.

Required:

- editable Fusion source;
- assembled housing STEP;
- separate base and lid STEP files;
- parametric generator and verification scripts;
- print-ready base, lid, cap and any justified prototype-coupon STL files;
- a cabinet-fastener-cap STL, which is mandatory because a recessed metal head installed after printing cannot be insulated by integral geometry;
- the slicer harness and its recorded output where a slicer CLI is available;
- updated build/verification report;
- updated review renders showing closed, open and exploded views; direct long-side terminal entry with representative fitted wires and ferrules; terminal screwdriver access; cover removal with wiring connected; USB access; cabinet fixings; and any justified downstream strain relief;
- a material table showing every production part's volume and estimated PETG mass.

Remove or clearly quarantine obsolete Rev A and Rev B production artefacts that could be mistaken for current deliverables. Do not deliver a fixed-clamp STL, an adjustable-clamp STL, a USB-plug STL or Rev B tie-anchor geometry.

## 13. Automated verification gates

The verifier shall fail the build unless all applicable checks pass:

1. Every production mesh is manifold and watertight.
2. The base has a continuous insulating floor.
3. Electronics underside clearance is at least 2.0 mm.
4. Lid top clearance is at least 2.0 mm.
5. No fastener, insert, hook, rib, cap, or enclosure surface intersects an electronics keep-out.
6. Every terminal screw remains accessible from above with the cover removed, including when its representative conductor and ferrule are fitted.
7. Every used terminal has a horizontal conductor-entry corridor from its outward-facing mouth to the enclosure exterior.
8. Every terminal-entry corridor preserves the declared straight insertion length and is clear of housing walls, cover skirts, fasteners and cable-management features.
9. Representative installed wire-and-ferrule envelopes enter the correct screw terminals and can be inserted and withdrawn without collision.
10. The USB service envelope is clear through the opening.
11. The ESP32 antenna keep-out is clear of metal, inserts, and thick structure.
12. Lid overlap, fit allowance and the lid-screw boss walls meet specification.
13. The fixed ledge, the locating posts and the support pads contact only approved PCB-edge regions and mounting-hole bores.
14. The carrier is located by its measured mounting holes: post diameter against the reported bore, engagement and proud height against the carrier, clearance to the outermost conductor, the holes that must be left empty, and the fitting tilt against the ledge gap.
15. The retention system does not load the ESP32, sockets, terminals, solder joints, or components, and carries no fastener that could be tightened onto the carrier.
16. Both cabinet fastener heads are recessed, insulated, and outside electronics keep-outs.
17. The complete cover installation and removal sequence clears all fitted conductors, ferrules and harnesses without disconnecting them.
18. No production part requires slicer support.
19. The complete outside envelope is no greater than 85 × 75 × 36 mm.
20. Production-part solid volume is no greater than 35 cm³.
21. Estimated PETG mass is no greater than 45 g.
22. No forbidden rail, ear, sawtooth roof, USB plug, decorative projection, elevated tie tower, unexplained external feature, or superseded generated artefact exists.
23. Conductors remain individual through the fixed terminal-entry zone and merge into grouped H1–H6 harness envelopes only after clearing the terminal mouths and straight insertion distance.
24. The seated cover neither pinches a conductor nor forces a bend inside the declared straight terminal-entry zone.
25. Each cabinet cap is positively retained: the measured interference between the cap and its recess is greater than zero, and the cap remains removable through a pry feature.
26. The usable countersink accommodates the declared maximum head envelope plus its declared clearance. A recess smaller than that envelope is a failure.
27. Any prototype coupon reproduces the corresponding replacement production geometry and is no larger than required to settle an identified physical uncertainty.
28. The reference assembly represents the selected DORHEA layout: 15 terminal positions per long side, top-operated screws, horizontal outward-facing conductor mouths and two vertical sockets used only by the ESP32 module.
29. Any housing-mounted strain relief lies beyond the straight terminal-entry zone, remains low profile, accepts the declared harness and does not obstruct terminal installation, screw access or cover removal.
30. No verification or render treats the vertical ESP32 sockets as external cable connections or reproduces Rev B's above-terminal grouped-cable route.

## 14. Prototype acceptance gates

### 14.0 A prototype print is a legitimate way to close a measurement gate

Where a part is **small, cheap and quick to print** — this housing is 20 g and
about an hour — a test print may be made and fitted *before* the §3 starting
values behind it have been measured, and the result used as the evidence that
closes them. On a part like this the print is the faster and better instrument:
callipers on a populated board give the nominal, while a fitted print gives the
answer to the question actually being asked, which is whether it seats.

This does not weaken anything. What it changes is the **order**:

1. A print made under this clause is a **prototype**, not a release. It is
   recorded as one, and §14 acceptance still has to be met before any part is
   production-approved.
2. **The result is recorded either way.** A print that fits closes the gates it
   demonstrably exercises and no others; a print that does not fit is a
   measurement in its own right and is recorded as one.
3. The specification states, per gate, **which starting values it rests on**, so
   that a fit obtained against an unmeasured value is never mistaken for a fit
   obtained against a measured one.
4. It does not extend to anything expensive, slow, or consumed by the attempt —
   a heat-set insert driven into a boss cannot be undone, so a boss geometry
   change still warrants a fresh part rather than a second attempt in the same
   hole.

The CAD revision is not production-approved until physical checks confirm:

- the acquired DORHEA board's overall length, width and PCB thickness;
- the terminal-block height and depth, terminal-port centre height and opening,
  practical ferrule envelope, mounting-hole pattern and underside features;
- any replacement carrier-fit coupon accepts the real terminal adapter without
  stress or excessive play;
- USB insertion and removal are unobstructed;
- a representative ferruled production conductor inserts horizontally into
  each terminal-row type without scraping or being forced to bend at the
  enclosure wall;
- all terminal screws are serviceable from above with representative wires fitted;
- individual conductors clear the terminal mouths before merging into the
  grouped H1–H6 harnesses;
- grouped H1–H6 harnesses leave the housing without pinch or sharp bends;
- the cover can be removed and refitted without disconnecting or disturbing wiring;
- cabinet fastener installation and insulation are practical;
- any selected strain-relief arrangement is practical for ordinary wiring and
  handling and does not load the terminal connections;
- antenna performance is acceptable;
- PETG print quality is acceptable without supports;
- a **horizontal** heat-set insert can actually be driven into the coupon boss;
- the cabinet screw's real head diameter is inside the declared maximum
  envelope;
- the insulating cap presses in, stays in and comes out again on the real
  printer and filament;
- the recorded 20.00 mm overall assembly height is represented from the actual
  lowest underside feature to the highest point, without reusing Rev B's
  incompatible 24.00 mm above-PCB datum;
- no pull test, load test or dedicated strain-relief coupon is required.

Record the results in the build report before release.

## 15. Change control

- Continue the work only in the dedicated housing branch and PR until prototype acceptance is complete.
- Treat every Rev B housing body, STL, STEP, render, slice result and verification result as superseded. Do not print or release them.
- Prototype printing is governed by §14.0, not by the measurement gate. A test print of a small, cheap part is a legitimate instrument and does not require the §3 starting values behind it to be measured first; its result is recorded under §14.
- The measurement gate is **CLOSED** as of 2026-09-06 and replacement production CAD is released. The macro geometry in §3 is owner-measured; the terminal-port bore and internal depth are out of scope under §5.3. A supplier photograph still establishes topology, not manufacturing dimensions, and no remaining assumption may be presented as a measurement.
- Do not merge the housing PR during the amendment sprint.
- Avoid unrelated wiring, firmware, or printing-work changes.
- A specification and hardware-identification correction may precede replacement CAD. Once replacement modelling begins, update the generated CAD, verification scripts, exported artefacts, renders, build report and PR description together.
- If any mandatory envelope or material gate cannot coexist with the clearance and service requirements, stop and document the conflict rather than silently relaxing the gate.
