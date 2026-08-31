# Decca ESP32 Controller Housing — Rev A build report

> **Status: PROTOTYPE CAD. NOT PHYSICALLY VALIDATED.**
> Nothing in this package has been printed, and no dimension in it has been
> measured off the acquired hardware. Every hardware figure is a CAD starting
> value taken from the controlling specification, and every one of them is a
> prototype gate. Read §7 before ordering filament.

**Controlling document:** `Decca_ESP32_Controller_Housing_Spec_v1.0.md`
**Generator:** `../CAD/Decca_ESP32_Controller_Housing_fusion.py`
**Independent verifier:** `../CAD/Decca_ESP32_Controller_Housing_verify.py`
**Date:** 2026-08-31 · **Material:** PETG / PETG-HF · **Method:** FDM, 0.40 mm
nozzle, 0.20 mm layers

---

## 1. What this is, and what it contains

A compact, electrically protective, fully serviceable housing for the Decca
controller assembly, holding **only**:

| Item | Repository status |
|---|---|
| 30-pin ESP32 DevKit V1 / DOIT-style board | ACQUIRED — USB→OTA verified |
| Its matching 30-pin screw-terminal breakout / adapter | ACQUIRED |

**Explicitly outside this housing**, mounted separately, and not modelled as
anything this box has to contain: the DAOKAI MOSFET test board; the selected
DFRobot DFR0457; the WAGO 221-415 distribution connectors; the inline fuse and
DC input hardware; the OLED; the WiiM Pro; the Fosi ZA3; and the future 12 V
trigger interface. None of them was used to solve a layout problem here.

**The electrical rule is unchanged and is moulded into no part of this design,
because it is a procedure, not a feature: do not connect USB while the shared
external 5 V rail is connected.** The USB opening exists for recovery, and the
optional blanking plug exists so the opening is not an invitation.

---

## 2. Files produced

### Editable and exchange

| File | Bytes |
|---|---:|
| `../CAD/Decca_ESP32_Controller_Housing.f3d` | ~1.30 MB |
| `../CAD/Decca_ESP32_Controller_Housing_assembly.step` | ~2.05 MB |
| `../CAD/ESP32_Controller_Housing_Base.step` | ~564 kB |
| `../CAD/ESP32_Controller_Housing_Lid.step` | ~1.19 MB |
| `../CAD/ESP32_Controller_PCB_Clamps.step` | ~43 kB |
| `../CAD/ESP32_Controller_Carrier_Fit_Gauge.step` | ~51 kB |

### Parametric build and verification

- `../CAD/Decca_ESP32_Controller_Housing_fusion.py` — `main()`, `validate()`,
  `export()`, `images()`
- `../CAD/Decca_ESP32_Controller_Housing_verify.py` — offline mesh gate suite,
  plus `--drawings`

### Print files

`../STL/ESP32_Controller_Housing_Base.stl`,
`..._Housing_Lid.stl`, `..._PCB_Clamp_Fixed.stl`,
`..._PCB_Clamp_Adjustable.stl`, `..._Carrier_Fit_Gauge.stl`,
`..._USB_Plug.stl`.

### Review evidence

Sixteen images, `Decca_ESP32_Controller_Housing_revA_01..16_*.png`, all
regenerated from the model by `images()` and `--drawings`; none is posed by
hand. The two dimensioned drawings are plotted from the exported triangles, so
the outlines in them are the manufacturing geometry and not a re-drawing of it.

### Component tree

```
Decca_ESP32_Controller_Housing
├── REF_ESP32_DevKit_V1_30Pin      NON-MANUFACTURING REFERENCE
├── REF_30Pin_Terminal_Adapter     NON-MANUFACTURING REFERENCE
├── REF_Wired_Keepouts             NON-MANUFACTURING REFERENCE
├── Housing_Base                   printable
├── Housing_Lid                    printable
├── PCB_Clamp_Fixed_End            printable
├── PCB_Clamp_Adjustable_End       printable
├── USB_Blanking_Plug              printable
└── Carrier_Fit_Gauge              printable
```

Every reference component carries the description *"NON-MANUFACTURING
REFERENCE. Dimensional starting values only — not measured hardware. Excluded
from every printable export."* No reference body appears in any STL. The
keep-out component is removed for the assembly STEP as well, because ten
deliberately overlapping solids make an assembly file unreadable.

---

## 3. Architecture as built

**Base tray, printed floor-down.** A continuous 2.40 mm insulating floor runs
beneath the whole board — no fastener, boss or slot penetrates it anywhere
under the electronics. Six low pads carry the board on the declared bare
long-edge perimeter only.

**Non-hole-dependent retention.** The repository records no breakout
mounting-hole pattern and §2 of the specification forbids inventing one, so
nothing enters the board. One short edge butts a hard datum face; the other is
held by a printed clamp with ±1.00 mm of slot travel. Each clamp is a flat bar
sitting on a plinth whose top is exactly `clamp_vertical_clear` above the board
face — so tightening the screws seats the bar on the plinth and the 0.20 mm gap
survives. The clamp retains; it cannot bow the board, because the plinth is the
hard stop.

**Cable exits.** One continuous window per long side, 12.00 mm of clear height
against a 10.00 mm requirement, with every wire-contact edge rolled to R1.00.
The window roof is a **45-degree sawtooth**: sixteen teeth whose rise equals
their run, so a 62 mm opening prints with no bridge and no support anywhere.

**Strain relief.** An external lacing rail on each long side, rooted on the
print bed and carrying six 2.50 × 6.00 mm tie slots that are open at the top —
so the rail needs no bridge either, and its slot floor still stands 3.00 mm
clear of a mounting face so a tie passes with the housing screwed flat to a
cabinet wall.

**Lid.** Removable, overlapping the **outside** of the base wall by 5.00 mm at
0.25 mm per face. It overlaps outside deliberately: an internal tongue would
have to sit inside the wall line, the wall line is 0.50 mm off the board, and
an internal tongue therefore lands inside the maximum-assembled-height
keep-out. Four M3 into heat-set inserts in corner piers. Thinned to 1.60 mm
over the antenna. Recessed `USB`, `EN`, `BOOT` and `DECCA CONTROLLER` legends,
cut 0.40 mm, printed top-face-down so they come off the bed crisp.

**Ventilation.** Six top slots over the ESP32 and regulator region, and
thirteen slots per long sidewall between the window roof and the lid skirt.
Every slot is 2.00 mm wide. That is narrower than an M3 shank and much narrower
than the 4.00 mm heat-set inserts, so **no fastener used in this build can fall
through a vent whatever path it takes** — which is a stronger guarantee than
offsetting or louvring gives, and it is the one the verifier gates on.

**Antenna.** The PCB antenna sits at the end opposite the USB. Its keep-out —
the antenna footprint grown 10.00 mm laterally, extruded to the lid — contains
no screw, insert, rib, boss or lacing feature. The only material inside it is
lid, at 1.60 mm.

---

## 4. Final derived dimensions

| Feature | Derived | Section 10 target | Note |
|---|---:|---:|---|
| Overall plan, ears and lacing rails | **105.00 × 77.00 mm** | 90.0 × 78.0 max | length **+15.00**, width −1.00 |
| Body plan, excluding ears and rails | **89.00 × 68.00 mm** | approx. 72.0 × 69.0 | length +17.00, width −1.00 |
| Closed height | **38.30 mm** | approx. 35 | **+3.30** |
| Plan area | 8085 mm² | 7020 mm² | +15.2% |
| Internal board plan envelope | 67.50 × 64.00 mm | 68.0 × 65.0 | inside target |
| Internal height above the support plane | 28.60 mm | 27.0 | +1.60, and forced |
| Board support-pad height | 5.50 mm | — | 2.50 + 3.00, derived |
| Clear cable-window height | 12.00 mm | 10.0 min | +2.00 |
| Wire-window roof apex | z +21.04 | — | 45° sawtooth |
| Lid overlap / per-face clearance | 5.00 / 0.25 mm | 5.00 / 0.25 | as specified |
| Adjustable clamp travel | ±1.00 mm | ±1.0 min | measured off the mesh |
| Board length window accepted | 65.00 – 67.00 mm | — | 66.00 nominal |

Vertical chain, all heights above the cavity floor:

```
-2.40  base underside                        floor 2.40
 0.00  cavity floor
 3.00  underside of the lowest solder joint  clear air 3.00
 5.50  board underside                       below-board parts 2.50
 7.10  board top face                        board 1.60
 7.30  clamp underside / plinth top          clamp clearance 0.20
17.10  top of the terminal blocks            block height 10.00
19.10  cable-window roof, valley             window 12.00 clear
21.04  cable-window roof, apex
29.10  lid skirt bottom                      overlap 5.00
31.10  maximum assembled component height    assembly 24.00
34.10  cavity ceiling / lid underside        headroom 3.00
35.90  lid outer face                        lid 1.80
```

Solid volumes as modelled — an upper bound; a printed part at 20–30% infill
weighs less. PETG at 1.27 g/cm³:

| Part | Volume | Solid mass |
|---|---:|---:|
| Housing_Base | 49.66 cm³ | 63.1 g |
| Housing_Lid | 14.84 cm³ | 18.8 g |
| PCB_Clamp_Fixed_End | 1.28 cm³ | 1.6 g |
| PCB_Clamp_Adjustable_End | 1.58 cm³ | 2.0 g |
| USB_Blanking_Plug | 0.57 cm³ | 0.7 g |
| Carrier_Fit_Gauge | 8.87 cm³ | 11.3 g |

---

## 5. Envelope deviation — an owner decision, not a silent change

Specification §10 gives approximate totals and then says, in terms: *"These are
design targets, not permission to violate required electrical, terminal,
antenna or cable clearances. Claude should report the final derived envelope
rather than forcing these approximate totals."* This build takes that
literally. Every required clearance is met in full; the envelope is reported.
§16 lists the envelope as a stop item, so it is raised here explicitly rather
than absorbed.

### 5.1 Height, +3.30 mm

```
2.40 floor + 2.50 below-board parts + 3.00 clear beneath those joints
   + 1.60 board + 24.00 assembly above the board + 3.00 headroom
   + 1.80 lid  =  38.30
```

§4 lists the 2.50 mm below-board height and the 3.00 mm beneath-joint
clearance as **two separate values**, and §5.1 requires the 3.00 mm to be
measured *beneath the solder joints*. They are therefore additive, and the
board support plane has to stand 5.50 mm off the floor. §10's "internal height
above PCB support plane 27.0 mm" is 1.60 mm short of the board, assembly and
headroom it has to contain; the derived figure is 28.60 mm.

This shrinks only if the two conservative starting values shrink. Measure the
real breakout: if below-board protrusion is 1.50 mm and assembled height above
the board is 21.00 mm, the housing drops to **34.30 mm** with no design change
at all — change two parameters and re-run.

### 5.2 Length, +15.00 mm

§10 budgets a 72.0 mm body: 68.0 mm of internal plan plus two 2.0 mm walls.
That leaves **nothing** for the §5.2 end clamps, their two M3 screws each, or
the four §9 lid-screw bosses — and §9 requires those bosses to be *outside the
breakout outline*, which in a cavity 1.00 mm wider than the board means beyond
the two short edges. The chain per end is not compressible without breaking a
different requirement:

| Fixed end, from the datum face | mm |
|---|---:|
| boss wall | 2.00 |
| heat-set insert hole | 4.00 |
| boss wall | 2.00 |
| wall | 2.00 |
| **subtotal** | **10.00** |

| Adjustable end, from the board clearance face | mm |
|---|---:|
| slot travel and bar edge margin | 9.50 |
| wall | 2.00 |
| **subtotal** | **11.50** |

66.00 board + 1.00 length adjustment + 0.50 clearance + 10.00 + 11.50 =
**89.00 mm body**. The four §5.3 ears then add 8.00 mm at each end — 2.00 mm
root gap, the 4.00 mm slot, 2.00 mm of edge material — giving **105.00 mm**.

### 5.3 Two documented ways to shorten it, neither taken here

1. **Move the ears to the long sides.** Overall becomes **89.00 × 84.00 mm**:
   length then sits 1.00 mm *inside* the 90 mm target and the overrun moves to
   the width, at +6.00 mm instead of +15.00. The cost is that the 8.00 mm slot
   axis then runs *along* the housing rather than across it, which is a literal
   departure from §5.3. It still delivers what §5.3 asks the slots for —
   installation adjustment — just along the other axis.
2. **Measure the board first.** §5.1's chain is driven by two conservative
   starting values; the length is not, so this only fixes the height.

Neither was applied unilaterally. §5.3's slot orientation is a stated
geometric requirement with no escape clause; §10's totals come with one. Ask
for option 1 and it is a two-line parameter change.

### 5.4 What was *not* done to make the numbers fit

No clearance was reduced. No clamp was deleted. No lid boss was moved inside
the board outline. Nothing separately mounted — MOSFET board, WAGO connectors,
fuse, DC socket — was brought into this enclosure to justify a bigger box.

---

## 6. Verification

Two independent suites, run on different things. The in-CAD suite works on the
BRep solids by boolean intersection; the offline suite reads **only** the
exported STLs and re-derives every claim from triangles, against expected
values typed in by hand from the controlling documents. Neither imports the
other's numbers.

```
59 CAD gates,  0 failed, 35 prototype gates open
65 mesh gates, 0 failed | 14 prototype-required | 4 installation-required
```

| §14 gate | Result | Measurement |
|---|---|---|
| 1 closed manifold solids | MESH-VERIFIED | all six: 0 bad edges, 0 bad windings, 1 component |
| 2 floor continuous under the board | MESH-VERIFIED | 575 probes at mid-floor, 0 gaps |
| 3 underside clearance ≥ 3.00 | MESH-VERIFIED | 3.00 mm minimum; pads stop at \|y\| 29.15, strip starts 29.00 |
| 4 fasteners out of the electrical envelope | MESH-VERIFIED | 12 axes, tightest 2.00 mm; screw tip 20.80 mm above the board |
| 5 component-to-lid ≥ 3.00 | MESH-VERIFIED | lowest lid material z +34.10, 3.00 mm of headroom |
| 6 terminal screwdriver corridors | MESH-VERIFIED | 30 corridors of Ø6.00, 0 obstructed |
| 7 wire-exit height ≥ 10.00 | MESH-VERIFIED | 12.00 mm narrowest, both sides |
| 8 no lid material on a wire path | MESH-VERIFIED | 30 runs, 0 crossings; 8.06 mm skirt-to-roof |
| 9 USB envelope unobstructed | MESH-VERIFIED | 14.00 × 9.00 swept to the connector, 0 obstructions |
| 10 button tool holes on the reference | MESH-VERIFIED | open at (−22.00, ±10.15); 12.60 mm of tool travel |
| 11 antenna keep-out clean | MESH-VERIFIED | 0 intrusions; closest fastener 0.75 mm outside; lid 1.60 mm |
| 12 lid overlap and fit clearance | MESH-VERIFIED | 72 perimeter probes, gap 0.25 mm, overlap 5.00 mm |
| 13 clamps on bare edge only | MESH-VERIFIED | checked at 65.00, 66.00 and 67.00 mm board length |
| 14 adjustable travel ≥ ±1.00 | MESH-VERIFIED | slot 5.40 measured, travel ±1.00 |
| 15 nothing loads the ESP32 or sockets | MESH-VERIFIED | controller and header envelopes, 0 intrusions |
| 16 cabinet slots outside the envelope | MESH-VERIFIED | four 8.00 mm slots, long axis across; 45.00 mm clear |
| 17 valid assembly and removal | MESH-VERIFIED | lid, both clamps and the ESP32 all lift vertically |
| 18 printable without internal support | MESH-VERIFIED | 0 mm² of facets steeper than 45°; worst bridge 11.00 mm |

**Result vocabulary, used exactly.** *CAD-verified* — proven on the BRep.
*Mesh-verified* — proven on the exported manufacturing geometry.
*Prototype-required* — cannot be settled without hardware in hand.
*Installation-required* — cannot be settled before it is in the cabinet. No
untested physical fit is recorded as passed anywhere in this package.

### 6.1 What verification caught, and what was changed to fix it

Recorded because the fixes are real design changes, not tuning:

- **The lacing rail floated.** Its first arrangement began at z +2.10 with
  nothing beneath it, so its whole first layer printed in mid-air, and its tie
  slots were closed by a 6 mm bridge. Rebuilt rooted on the bed with the slots
  open at the top. No check was relaxed.
- **Three tangent-surface sites made the mesh non-manifold.** Cylindrical lid
  bosses sitting tangent to the walls, a torus root fillet overrunning a wall,
  the sawtooth flanks landing exactly on the window end planes, and the gauge's
  clamp lip butting its plinth. All four are valid BRep solids that Fusion
  reports as solid, and all four tessellate to edges shared by four triangles.
  Fixed by geometry — square corner piers buried into the walls, a sawtooth run
  1.00 mm past each window end, an overlapping gauge lip — not by loosening the
  manifold check.
- **The lid legends cut nothing.** The first marking pass reported four
  successful cut extrudes that removed zero material, because a cut on a
  base-feature body needs `participantBodies` and a one-sided extent. The
  generator now measures the volume removed per legend and prints
  `CUT NOTHING` rather than counting a silent no-op as a legend.
- **The sidewall vents sat under the lid skirt.** Caught by arithmetic before
  it reached the model; the vent band is now derived from the skirt bottom.

---

## 7. Prototype gates — every one of these is still open

**Nothing below is verified. Nothing below may be treated as verified until the
acquired hardware is measured or the part is printed and offered up.**

### 7.1 Hardware dimensions that are CAD starting values

`adapter_pcb_l` 66.00 · `adapter_pcb_w` 63.00 · `adapter_pcb_t` 1.60 ·
`adapter_below_h` 2.50 · `assembly_above_pcb_h` 24.00 · `pcb_bare_edge` 3.00 ·
`pcb_bare_perim` 2.50 · `term_per_side` 15 · `term_pitch` 3.50 ·
`term_block_w` 8.00 · `term_block_h` 10.00 · `term_screw_inset` 4.00 ·
`term_screw_d` 2.60 · `term_wire_z` 4.00 · `esp_pcb_l` 51.50 · `esp_pcb_w`
28.30 · `esp_pcb_t` 1.60 · `esp_header_h` 8.50 · `esp_header_span` 22.86 ·
`esp_off_x` 0.00 · `esp_off_y` 0.00 · `esp_mod_l` 25.50 · `esp_mod_w` 18.00 ·
`esp_mod_h` 3.10 · `esp_ant_l` 15.00 · `esp_ant_w` 18.00 · `esp_usb_w` 7.50 ·
`esp_usb_l` 5.90 · `esp_usb_h` 2.70 · `esp_btn_x` −22.00 · `esp_btn_y` ±10.15
· `esp_btn_sz` 6.00 · `esp_btn_h` 4.30 · `insert_hole_d` 4.00 ·
`insert_depth` 6.00.

The last two matter most in the short term: **the exact heat-set insert has not
been recorded anywhere in the repository.** 4.00 mm × 6.00 mm is a common M3
short insert, and it is a guess. Record the actual part before printing the
base, or the four lid screws and four clamp screws have nowhere to live.

### 7.2 Physical behaviour nothing geometric can settle

- the acquired breakout sits flat on the six pads without forcing;
- the clamps retain it without bowing it;
- the ESP32 comes out of and goes back into its sockets with the lid off;
- every used terminal remains reachable with the owner's actual screwdriver;
- harnesses exit without sharp bends or trapped insulation;
- ties transfer pull to the housing and not to the terminals;
- the lid fits and removes repeatedly without stressing wiring;
- a USB cable with its moulded shroud inserts and removes cleanly;
- EN/RESET and BOOT operate with a non-conductive tool;
- no abnormal temperature after at least 30 minutes powered.

### 7.3 Installation-required

Cabinet mounting surface and hole positions — the external ears deliberately
let the installed housing set its own; final harness routing and tie positions;
OTA link with the lid fitted; the shake and handling test.

---

## 8. Printing

| Part | Orientation | Notes |
|---|---|---|
| Housing_Base | floor down | longest bridge 11.00 mm, the USB lintel |
| Housing_Lid | **top face down** | keeps the recessed legends crisp; no overhang at all |
| PCB_Clamp_Fixed_End | flat, as modelled | no overhang |
| PCB_Clamp_Adjustable_End | flat, as modelled | no overhang |
| USB_Blanking_Plug | flange face down | 3.00 mm flange step |
| Carrier_Fit_Gauge | plate down | 4.00 mm lip overhang |

PETG or PETG-HF. 0.40 mm nozzle, 0.20 mm layers. **Four perimeters** around the
lid-screw piers, the clamp plinths and the mounting ears; **three** elsewhere.
20–30% infill. **No support material on any part** — the verifier gates on it:
0 mm² of facet steeper than 45° from vertical on every part, in its stated
orientation. Deburr the cable windows and the USB opening before assembly.

### Recommended first print

**`ESP32_Controller_Carrier_Fit_Gauge.stl` alone, and nothing else.** It is
11 cm³ and about twenty minutes. Snap it at its two score grooves and it gives
three answers before any real material is spent:

1. **Zone A** — slide the acquired breakout's short edge into the 1.80 mm slot.
   It proves board thickness, the 0.20 mm clamp clearance and the 5.50 mm
   support-pad height in one go, against the real board.
2. **Zones B and C** — mate the male step into the female pocket. That is the
   lid-to-base overlap: 5.00 mm of engagement at 0.25 mm per face, on this
   printer, with this filament, at this flow.

If Zone A is tight, `adapter_pcb_t` is wrong. If B/C is tight or sloppy,
`lid_fit_clear` is wrong. Either is a one-line change and a re-run. Only then
print the base and clamps, then the lid, then optionally the plug — the order
§15 asks for.

---

## 9. Assembly, wiring and removal

1. Heat-set eight M3 inserts: four in the lid-screw piers, four in the clamp
   plinths.
2. Lay the breakout on the six pads, short edge against the fixed datum face.
3. Fit `PCB_Clamp_Fixed_End`, two M3 into the datum-end plinth.
4. Fit `PCB_Clamp_Adjustable_End`, slide until its lip sits on the bare edge,
   two M3 through the slots. ±1.00 mm of travel is available.
5. Wire the terminals. Route each harness out through the long-side window and
   lace it to the rail below. **The tie takes the pull, not the terminal.**
6. Plug the ESP32 into its sockets.
7. Fit the lid, four M3 × 8.

Removal is the reverse, and the two service cases are short: **the ESP32 comes
out with only the lid removed** — nothing crosses its vertical path — and
**both clamps come out with the lid off and every wire still connected.** Both
are gated (§14.17), by sweeping the corridors rather than by assertion.

---

## 10. Reconciliation with the specification

| § | Requirement | State |
|---|---|---|
| 3 | four printable parts plus fit gauge | as built, plus the optional USB plug |
| 4 | named parameters, no hidden sketch dimensions | 219 Fusion user parameters written |
| 5.1 | solid floor, 2.40 mm, no fastener in the clearance volume | met and gated |
| 5.2 | no assumed mounting holes, four-plus pads, datum, adjustable clamp, 0.20 mm clearance, both clamps removable | met and gated |
| 5.3 | four external ears, 4.0 × 8.0 slots across the housing, R2.0 fillets, 3.0 mm | met; ear-to-wall roots filleted R2.00, 4 of 4 |
| 6 | continuous exit zone, 10.0 mm minimum, R1.0 edges, lacing rails, four-plus tie slots | met; 12.00 mm provided, twelve tie slots |
| 7 | USB opening, blanking plug, two tool holes, lid identification | met |
| 8 | antenna keep-out, 1.6 mm lid there, vents, no fastener path | met; the vent guarantee is stronger than louvring |
| 9 | overlapping lid, 2.0/1.8/1.6, 5.0 overlap, 0.25 clearance, four M3, bosses outside the outline, R3.0 external | met |
| 10 | approximate envelope | **NOT met — see §5** |
| 11 | parameter list | all exposed, plus the derived chain |
| 12 | FDM rules | met; no support anywhere |
| 13 | deliverables | all present |
| 14 | eighteen gates | all pass, in two independent tools |
| 15 | print and acceptance order | recorded in §8 |
| 16 | change control | one stop item raised, in §5 |

---

## 11. After the first fit test

Record the measured values here, change the matching parameters, re-run
`main()`, `validate()`, `export()`, `images()` and the offline verifier, and
raise the revision. The measured values then supersede the starting values
everywhere, including in the specification.

| Parameter | Starting | Measured | Date |
|---|---:|---:|---|
| `adapter_pcb_l` | 66.00 | | |
| `adapter_pcb_w` | 63.00 | | |
| `adapter_pcb_t` | 1.60 | | |
| `adapter_below_h` | 2.50 | | |
| `assembly_above_pcb_h` | 24.00 | | |
| `term_per_side` / `term_pitch` | 15 / 3.50 | | |
| `term_block_h` / `term_screw_inset` | 10.00 / 4.00 | | |
| `esp_header_h` | 8.50 | | |
| `esp_btn_x` / `esp_btn_y` | −22.00 / ±10.15 | | |
| `insert_hole_d` / `insert_depth` | 4.00 / 6.00 | | |
| `lid_fit_clear` | 0.25 | | |

**The housing is not physically validated and must not be described as such
until a printed part has been tested against the acquired hardware.**
