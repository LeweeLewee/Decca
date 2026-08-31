# Decca ESP32 Controller Housing Specification v1.0

Status: **CAD-ready design specification — prototype fit and installation validation required**

Date: 2026-08-31  
Manufacturing method: **FDM 3D print**  
CAD platform: **Autodesk Fusion 360**  
Scope: **ESP32 DevKit and its screw-terminal breakout only**

## 1. Purpose

Create a compact, electrically protective and fully serviceable housing for the
Decca controller assembly already defined by the repository:

1. one **30-pin ESP32 DevKit V1 / DOIT-style board**; and
2. its acquired **matching 30-pin screw-terminal breakout/adapter**.

The ESP32 remains plugged into the breakout in normal service. The enclosure is
mounted inside the Decca cabinet and protects the underside, ESP32, terminals
and wiring from accidental contact and loose conductive objects.

The following are explicitly outside this housing:

- the MOSFET lighting board, whether test or final;
- WAGO power-distribution connectors;
- the inline fuse and panel DC socket;
- the OLED;
- the WiiM Pro, Fosi ZA3 and future 12 V trigger interface.

Those items are mounted separately.

## 2. Repository-controlled hardware definition

The live repository is the component authority.

| Item | Controlling definition |
|---|---|
| Controller | 30-pin ESP32 DevKit V1 / DOIT-style, Wi-Fi, at least 4 MB flash |
| Breakout | Acquired matching 30-pin screw-terminal adapter for the installed controller |
| Normal power | Shared regulated 5 V rail connected to breakout terminal serving ESP32 5V/VIN |
| Normal firmware access | Authenticated OTA |
| Recovery access | ESP32 USB connector must remain physically accessible |
| Normal USB state | USB disconnected whenever the shared 5 V supply is connected |
| Connected interfaces | H1 pots, H2 on/off, H3 VHF and Stereo/Mono, H4 OLED, H5 lighting control; H6 future |
| Wiring | Ferruled 22–24 AWG where applicable; removable controller-end harnesses where practical |

The repository records the board family and pin count but not a manufacturer,
purchase link, exact breakout outline, mounting-hole pattern or assembled
height. CAD must therefore keep the hardware envelope parametric and use
non-hole-dependent retention. No fictional mounting-hole pattern may be added
to the breakout reference model.

## 3. Design architecture

The housing comprises four printable parts:

1. **Base tray**: insulated mounting surface, PCB support pads, cabinet mounting
   ears, cable-lacing features and lid bosses.
2. **Removable lid**: overlapping protective cover with ventilation, USB
   opening and Wi-Fi antenna clearance.
3. **Two adjustable PCB edge clamps**: retain the breakout at its bare short
   edges without using unverified PCB holes.
4. **Fit gauge**: a short low-material coupon proving PCB thickness, edge-clamp
   clearance and lid/base overlap before the full housing is printed.

The controller assembly lies horizontally. The ESP32 faces upwards, the
breakout screw terminals face the two long sides, and the ESP32 USB connector
faces a short end of the housing.

The lid is fixed by machine screws into heat-set inserts. Snap fits are not the
primary closure because repeated servicing is expected during commissioning.

## 4. Reference geometry and starting envelope

All dimensions below are named parameters, not hidden sketch dimensions.

The board dimensions are deliberately classified:

- **locked**: 30-pin DOIT-style ESP32 and matching 30-pin breakout;
- **CAD starting values**: initial breakout and assembly envelope used to
  generate the first prototype;
- **fit parameters**: values Claude must expose so the model can be corrected
  without redesign after offering up the acquired board.

| Parameter | Initial value | Status |
|---|---:|---|
| Breakout nominal length | 66.00 mm | CAD starting value |
| Breakout nominal width | 63.00 mm | CAD starting value |
| Breakout PCB thickness | 1.60 mm | CAD starting value |
| Maximum component height below PCB | 2.50 mm | conservative starting value |
| Maximum assembled height above PCB | 24.00 mm | conservative starting value |
| PCB perimeter clearance | 0.50 mm per side | design value |
| Clearance above highest component | 3.00 mm minimum | design value |
| Clearance beneath PCB solder joints | 3.00 mm minimum | design value |
| USB service envelope | 14.00 mm W × 9.00 mm H | design starting value |
| Terminal/wire access height | 10.00 mm minimum | design value |

The housing must tolerate at least ±1.0 mm adjustment in breakout length using
the edge clamps. The lid and base must not rely on the ESP32 PCB outline for
location.

If the acquired breakout does not fit the initial nominal envelope, change only
the named hardware-reference parameters and re-derive the housing. Do not
modify or force the PCB.

## 5. Base tray

### 5.1 Electrical isolation

- Solid floor beneath the complete breakout.
- Nominal floor thickness: **2.40 mm**.
- No screw, insert or cabinet fastener may project into the electrical clearance
  volume beneath the PCB.
- Maintain **at least 3.00 mm** air/printed clearance beneath solder joints.
- PCB supports may touch only bare PCB perimeter regions, never solder joints,
  tracks, components or terminal pins.

### 5.2 PCB support and retention

Do not use assumed breakout mounting holes.

- Support the breakout on four or more low perimeter pads.
- One short edge locates against a fixed end datum.
- The opposite short edge uses an adjustable printed clamp secured by two M3
  screws in slotted holes.
- A second removable clamp at the fixed end prevents lift while preserving the
  datum.
- Clamp contact is limited to bare PCB edge.
- Provide **0.20 mm nominal vertical clamp clearance** above the PCB before
  screw tightening; the clamp should retain, not bend, the board.
- Both clamps must be removable with the lid off and wiring still connected.
- The ESP32 must remain removable vertically from its breakout sockets after
  the lid and appropriate clamp are removed.

### 5.3 Cabinet mounting

Provide four external mounting ears integral with the base:

- four **4.0 × 8.0 mm slots** for small cabinet/wood screws;
- long axes aligned across the housing to allow installation adjustment;
- screw heads remain outside the PCB electrical envelope;
- mounting holes remain accessible with the lid fitted;
- nominal ear thickness: **3.0 mm**;
- fillet each ear into the base, minimum **R2.0 mm**;
- base must mount on either a horizontal or vertical internal wooden surface
  without relying on adhesive.

No drilling dimensions for the Decca cabinet are locked by this specification.
The external ears deliberately let the installed housing establish its own hole
positions.

## 6. Terminal and cable access

The two long sides must keep every breakout screw terminal usable.

- With the lid removed, a normal small terminal screwdriver must approach every
  terminal vertically without obstruction.
- Provide a continuous cable-exit zone along both terminal sides rather than
  one hole per GPIO.
- Minimum clear exit height: **10.0 mm**.
- Round every wire-contact edge, minimum **R1.0 mm**.
- No wire may be pinched between lid and base.
- Add an external lacing rail on each long side with at least four
  **2.5 × 6.0 mm** cable-tie slots.
- Cable ties provide strain relief after the terminal connection; they must not
  pull directly on the screw terminals.
- Preserve the documented harness separation where practical. Do not mould pin
  labels into the housing until the physical orientation of the breakout has
  been confirmed.

## 7. USB and controls

- Provide an unobstructed opening at the ESP32 USB end.
- The opening must accept the connector body and normal moulded cable shroud,
  not only the metal plug.
- USB must be insertable and removable without taking the housing off the
  cabinet.
- Add a removable printed USB blanking plug as an optional fifth part if it does
  not complicate the main lid. The plug is dust/contact protection only.
- Provide two recessed tool-access holes in the lid for **EN/RESET** and
  **BOOT**, derived from named ESP32 reference coordinates.
- Tool holes: nominal **3.0 mm diameter**, with underside lead-in.
- The lid must identify the USB end and the two button functions with small
  recessed text or symbols.

The normal electrical rule remains unchanged: do not connect USB while the
shared external 5 V rail is connected.

## 8. Wi-Fi and ventilation

The ESP32 uses Wi-Fi continuously for OTA and future WiiM control.

- Identify the PCB antenna end in the reference component.
- No heat-set insert, cabinet mounting screw, cable bundle or thick structural
  rib may sit directly above or within **10 mm laterally** of the antenna.
- Use a thin non-metallic lid region above the antenna, nominal **1.6 mm**.
- Provide ventilation slots above the ESP32/regulator region and on the upper
  sidewalls.
- Slot width: **2.0–2.5 mm**; bridge width: at least **2.0 mm**.
- Ventilation must not create a straight path for a loose screw to fall onto
  powered circuitry. Offset or louvre the top openings where practical.
- No fan is required.

## 9. Lid and closure

- Removable overlapping lid; no live circuit is exposed from above when fitted.
- Nominal structural wall: **2.0 mm**.
- Nominal top thickness: **1.8 mm**, reduced to **1.6 mm** over the antenna
  keep-out.
- Lid/base overlap: **5.0 mm** nominal.
- Sliding clearance on each mating face: **0.25 mm**.
- Four M3 machine screws into heat-set inserts in base corner bosses.
- Use M3 × 8 mm as the starting screw length; CAD must prove no screw can enter
  the PCB electrical envelope at full insertion.
- Insert bosses must be outside the breakout outline and terminal screwdriver
  corridors.
- A shallow underside tongue-and-groove or stepped overlap should prevent the
  lid shifting and prevent wire entry into the joint.
- External corners: nominal **R3.0 mm**.
- Internal stressed corners: minimum **R1.0 mm**.

The lid is protective, not load-bearing. Do not add decorative bulk or a large
logo. Small recessed text, **DECCA CONTROLLER**, is acceptable on the lid.

## 10. Initial overall envelope

Starting values for the first CAD build:

| Feature | Initial target |
|---|---:|
| Internal PCB plan envelope | 68.0 × 65.0 mm |
| Base wall thickness | 2.0 mm |
| Internal height above PCB support plane | 27.0 mm |
| Nominal body outside plan, excluding ears | approx. 72.0 × 69.0 mm |
| Nominal closed height | approx. 35.0 mm |
| Maximum target footprint including ears | 90.0 × 78.0 mm |

These are design targets, not permission to violate required electrical,
terminal, antenna or cable clearances. Claude should report the final derived
envelope rather than forcing these approximate totals.

## 11. Fusion 360 parameters

Expose at least:

```text
// Repository-controlled hardware
esp_pin_count             = 30
adapter_pcb_l             = 66.00 mm
adapter_pcb_w             = 63.00 mm
adapter_pcb_t             = 1.60 mm
adapter_below_h           = 2.50 mm
assembly_above_pcb_h      = 24.00 mm

// Clearances
pcb_xy_clear              = 0.50 mm
pcb_under_clear           = 3.00 mm
component_top_clear       = 3.00 mm
clamp_vertical_clear      = 0.20 mm
antenna_keepout           = 10.00 mm
lid_fit_clear             = 0.25 mm

// Structure
base_floor_t              = 2.40 mm
wall_t                    = 2.00 mm
lid_top_t                 = 1.80 mm
lid_antenna_t             = 1.60 mm
lid_overlap               = 5.00 mm
outer_corner_r            = 3.00 mm
inner_fillet_r            = 1.00 mm

// Access
wire_exit_h               = 10.00 mm
usb_open_w                = 14.00 mm
usb_open_h                = 9.00 mm
button_tool_d             = 3.00 mm
tie_slot_w                = 2.50 mm
tie_slot_l                = 6.00 mm

// Fasteners
lid_screw_nominal         = 3.00 mm
lid_screw_length          = 8.00 mm
cabinet_slot_w            = 4.00 mm
cabinet_slot_l            = 8.00 mm
ear_t                     = 3.00 mm
```

Recommended component structure:

```text
Decca_ESP32_Controller_Housing
├── REF_ESP32_DevKit_V1_30Pin
├── REF_30Pin_Terminal_Adapter
├── REF_Wired_Keepouts
├── Housing_Base
├── Housing_Lid
├── PCB_Clamp_Fixed_End
├── PCB_Clamp_Adjustable_End
├── USB_Blanking_Plug
└── Carrier_Fit_Gauge
```

All hardware reference components must be visibly marked non-manufacturing.

## 12. FDM design rules

- Preferred material: **PETG or PETG-HF**.
- Design for a 0.4 mm nozzle.
- Nominal layer height: **0.20 mm**.
- At least four perimeters around fastener bosses and mounting ears.
- At least three perimeters elsewhere.
- 20–30% infill is sufficient if walls and bosses meet the perimeter rules.
- Heat-set insert holes must be parameterised for the exact inserts used; do not
  assume a catalogue diameter without recording it.
- Avoid supports in electrical cavities and mating surfaces.
- Print the base floor-down.
- Print the lid top-face-down only if cosmetic finish and recessed markings
  remain correct; otherwise print open-side-down and bridge/angle vents so no
  internal support is required.
- Print clamps and fit gauge in their working orientation.
- Deburr all cable and USB openings before assembly.

## 13. CAD deliverables for Claude

Create:

### Editable and exchange files

- `mechanical/CAD/Decca_ESP32_Controller_Housing.f3d`
- `mechanical/CAD/Decca_ESP32_Controller_Housing_assembly.step`
- `mechanical/CAD/ESP32_Controller_Housing_Base.step`
- `mechanical/CAD/ESP32_Controller_Housing_Lid.step`
- `mechanical/CAD/ESP32_Controller_PCB_Clamps.step`
- `mechanical/CAD/ESP32_Controller_Carrier_Fit_Gauge.step`

### Parametric build and verification

- `mechanical/CAD/Decca_ESP32_Controller_Housing_fusion.py`
- `mechanical/CAD/Decca_ESP32_Controller_Housing_verify.py`

### Print files

- `mechanical/STL/ESP32_Controller_Housing_Base.stl`
- `mechanical/STL/ESP32_Controller_Housing_Lid.stl`
- `mechanical/STL/ESP32_Controller_PCB_Clamp_Fixed.stl`
- `mechanical/STL/ESP32_Controller_PCB_Clamp_Adjustable.stl`
- `mechanical/STL/ESP32_Controller_Carrier_Fit_Gauge.stl`
- optional `mechanical/STL/ESP32_Controller_USB_Plug.stl`

### Review evidence

- dimensioned overall and section views;
- lid removed view showing terminal screwdriver corridors;
- underside view showing the isolated PCB and cabinet fastener envelopes;
- USB insertion envelope;
- Wi-Fi antenna keep-out;
- exploded assembly;
- machine-readable verification report;
- build report under `mechanical/Drawings/`.

## 14. CAD verification gates

Claude’s independent verifier must establish at minimum:

1. every printable part is a closed manifold solid;
2. base floor is continuous below the complete PCB outline;
3. minimum underside electrical clearance is at least 3.00 mm;
4. no cabinet fastener or lid screw envelope intersects the PCB or wiring
   keep-out;
5. minimum component-to-lid clearance is at least 3.00 mm;
6. all breakout screw terminals have unobstructed top screwdriver corridors;
7. both long sides provide the required wire-exit height;
8. no lid material crosses the wire paths;
9. USB service envelope is unobstructed;
10. button tool holes align to the parameterised ESP32 reference;
11. antenna keep-out contains no screw, insert, thick rib or cable-lacing feature;
12. lid overlap and fit clearance are correct around the complete perimeter;
13. clamps contact only the permitted bare PCB edge zones;
14. the adjustable clamp provides at least ±1.0 mm longitudinal adjustment;
15. no retaining feature loads the ESP32 board or its socket headers;
16. all four cabinet slots are outside the electrical envelope;
17. base, lid and clamps can be assembled and removed in a valid sequence;
18. each part is printable in the stated orientation without internal supports.

Any check that depends on an unrecorded physical dimension must be reported as a
prototype gate, never marked as physically verified.

## 15. Prototype and installation acceptance

Print and test in this order:

1. fit gauge;
2. base and clamps;
3. lid;
4. optional USB plug.

Acceptance criteria:

- acquired breakout sits flat without forcing;
- clamps retain it securely without bending the PCB;
- ESP32 can be removed and refitted;
- every used screw terminal remains accessible;
- all harnesses exit without sharp bends or trapped insulation;
- cable ties transfer pull load to the housing rather than the terminals;
- lid fits and removes repeatedly without stressing wires;
- USB cable inserts and removes cleanly;
- EN/RESET and BOOT can be operated with a non-conductive tool;
- no fastener can touch the board or wiring;
- housing mounts firmly to the selected internal cabinet surface;
- powered controller completes startup and all local controls behave normally;
- OTA connects successfully with the lid fitted;
- no abnormal temperature is observed after at least 30 minutes powered;
- shake/handling test reveals no board movement or loose hardware.

Record the physical board dimensions and final successful parameter values in
the build report and repository. Those measured values then supersede the CAD
starting values.

## 16. Change control

This specification is the authority for the housing architecture. Claude may
refine fillets, ribs, print reliefs and derived dimensions while preserving the
requirements and named parameters.

Stop and return for a design decision if CAD reveals that any of the following
cannot coexist:

- full terminal screwdriver access;
- safe electrical separation from all fasteners;
- USB recovery access;
- antenna keep-out;
- removable wiring and controller service;
- the 90 × 78 × approximately 35 mm target envelope.

Do not incorporate the separately mounted MOSFET or power-distribution hardware
to solve a housing-layout conflict.
