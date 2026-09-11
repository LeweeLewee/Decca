# Wiring

> **Status:** active. This is the authoritative interconnect reference. Pin
> assignments marked **(proposed)** are documented intent and have **not** been
> bench-verified. Confirmed items reflect the physical build.

Records every physical connection so the build is reproducible. The firmware pin
map (`src/hardware.h`) must be reconciled against this document before any build
(see Specification `HW-06`). `hardware.h` matches the status recorded below: the
four pot inputs, OLED I²C GPIO21/22, on/off GPIO14, VHF GPIO26 and lighting PWM
GPIO18 are physically verified. Stereo/Mono firmware logic is assigned to
GPIO25; the retained switch fault remains open under HW-SW-01.

## Wiring Colour Standard

New control wiring follows a fixed colour standard:

| Colour  | Meaning                                             |
|---------|-----------------------------------------------------|
| Brown   | GND                                                 |
| Red     | 3.3 V                                               |
| Orange  | 5 V                                                 |
| White   | Analogue signal / controlled return where documented |

**Exception — original on/off switch.** The retained original on/off switch uses
its original conductors, **Red** and **Green**. These are pre-existing and are
**not** to be recoloured or reinterpreted under the general loom standard above.
See the on/off section.

**Exception — H3 VHF dry-contact pair.** The installed VHF source-selector pair
uses **two Black conductors**. They form an isolated dry contact, so colour does
not distinguish signal from return and either Black conductor may be connected
to GPIO26 with the other connected to GND. See the H3 section.

**Exception — H4 OLED harness.** The installed and bench-verified screen loom
uses **Orange for SCL** and **Yellow for SDA**. These are signal conductors in H4
and must **never** be connected to the 5 V rail. H4 retains Red for 3.3 V and
Brown for GND. This final orientation was physically confirmed on 2026-08-30. See the OLED section.

H3 now uses only the reliable VHF-derived dry-contact pair. It has its own
return and no common-return conductor. All other selector conductors are left
disconnected and individually insulated at the controller end.

## Harnesses

Each harness is removable at the controller end where practical.

| ID  | Harness                     |
|-----|-----------------------------|
| H1  | Potentiometer harness       |
| H2  | Original on/off switch harness |
| H3  | Radio/source button harness |
| H4  | OLED harness                |
| H5  | Dial-lighting harness       |
| H6  | WiiM-to-ZA3 trigger lead    |

## Pin Map

All ESP32 pin numbers below are **(proposed)** unless stated otherwise. The
**Board label** column records the silkscreen text printed beside the pin on the
30-pin ESP32 DevKit used in this build. For the four ADC inputs the printed
labels are simply `D32`, `D33`, `D34` and `D35` respectively.

| Signal                | ESP32 Pin       | Board label | Type        | Harness | Notes                                    |
|-----------------------|-----------------|-------------|-------------|---------|------------------------------------------|
| Volume pot wiper      | GPIO32 (bench-verified) | **D32** | ADC1        | H1      | ADC1 required (Wi-Fi in Phase 2)         |
| Bass pot wiper        | GPIO33 (bench-verified) | **D33** | ADC1        | H1      | ADC1 required                            |
| Treble pot wiper      | GPIO34 (bench-verified) | **D34** | ADC1, in-only | H1    | ADC1; input-only pin, no pull-up needed  |
| Balance pot wiper     | GPIO35 (bench-verified) | **D35** | ADC1, in-only | H1    | ADC1; input-only pin                     |
| On/off switch (Red)   | GPIO14 (physically verified) | D14 | Digital in | H2 | Internal pull-up; closed = ON |
| Source selector: VHF | GPIO26 (physically verified) | D26 | Digital in, pull-up | H3 | Closed = Digital Streamer; open = Vinyl |
| SW / MW / LW / Gram  | — | — | No individual GPIO | H3 | Mechanical positions release VHF and select Vinyl |
| Stereo/Mono          | GPIO25 (logic verified; switch fault open) | D25 | Digital in, pull-up | H3 | Open Stereo = lights requested on; closed Mono = off |
| OLED SDA              | GPIO21 (bench-verified) | D21 | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| OLED SCL              | GPIO22 (bench-verified) | D22 | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| Dial lighting PWM     | GPIO18 (physically verified) | D18 | PWM (LEDC), 1 kHz | H5 | Installed DFRobot DFR0457 control input; three-lamp bank |

> GPIO14, GPIO25 and GPIO26 support the required internal pull-ups and avoid the
> project's excluded ESP32 strapping pins GPIO0, GPIO2, GPIO5, GPIO12 and
> GPIO15. GPIO13, GPIO16, GPIO17, GPIO19 and GPIO23 are released; do not connect the unreliable
> source-selector contacts to them.

## H1 — Potentiometers

Four modern **10 kΩ linear** potentiometers used as **position sensors only**.
They are **not in the audio path**. Original Decca knobs are retained via a
mechanical adaptor strategy.

Controls: **Balance, Treble, Bass, Volume.**

Each potentiometer uses three conductors. Viewed from the **rear** of the
installed potentiometer:

| Lug     | Conductor | Function              |
|---------|-----------|-----------------------|
| Left    | Brown     | GND                   |
| Centre  | White     | Wiper / analogue signal |
| Right   | Red       | 3.3 V                 |

At the ESP32 terminal adapter, connect each **White centre/wiper conductor** to
the terminal carrying both the GPIO number and matching DevKit silkscreen label:

| Control | ESP32 GPIO | Printed board label |
|---------|------------|---------------------|
| Volume  | GPIO32     | **D32**             |
| Bass    | GPIO33     | **D33**             |
| Treble  | GPIO34     | **D34**             |
| Balance | GPIO35     | **D35**             |

Termination (confirmed): ends soldered directly to the lugs, insulated with
heat-shrink, mechanically strain-relieved, and terminated through a removable
connector at the controller end.

Bench verification completed 2026-08-24 with each control connected to its
named ADC1 channel. All readings increased clockwise and the on-target
`test_pots` suite passed all six test cases.

| Control | GPIO | Board label | Anticlockwise | Approx. centre | Clockwise |
|---------|------|-------------|---------------|----------------|-----------|
| Volume  | 32   | D32         | 0             | 2047           | 4095      |
| Bass    | 33   | D33         | 0             | 2047           | 4095      |
| Treble  | 34   | D34         | 0             | 2047           | 4095      |
| Balance | 35   | D35         | 0             | 2047           | 4095      |

The controls have no centre detent, so the centre readings vary slightly with
manual positioning. The observed endpoints match the firmware's default
0–4095 calibration; no per-pot endpoint override or inversion is required.

In Phase 2, the **Volume** position is translated by the ESP32 into WiiM output
volume. The Fosi ZA3's own level control is set during commissioning as a fixed
hardware ceiling and is not the normal user-volume control.

## H2 — Original On/Off Switch

The original Decca on/off switch is retained, including its **original solder
joints and original cable**. It is a simple open/close switch.

- Active conductors (confirmed): **Red** and **Green**.
- Interface (physically verified): **Red → ESP32 GPIO14 / board label D14** input
  with **internal pull-up enabled**; **Green → GND**.
- This is a **low-voltage logic input only**. It does **not** switch 230 V mains.
- Confirmed logic: closed/active-low = ON; open = STANDBY. Both directions were
  physically accepted on the former D19 route on 2026-08-30 and on D14 with
  v0.27.3 on 2026-09-08.
- The switch is a **system-state command**. ON makes the ESP32 restore the WiiM
  source/volume, illuminate the dial and enable the OLED. OFF stops WiiM playback,
  reverses the local actions and allows WiiM automatic standby to remove its
  direct trigger output to the ZA3.

## H3 — Radio/Source Button Bank

The original PCB and interlocked selector mechanism are retained mechanically
(ADR-0001). Repeated soldering and contact tests showed that multi-button
electrical reuse is not reliable. ADR-0016 retains the VHF behaviour established
by ADR-0013 while superseding its GPIO routing.

Only the physically accepted **VHF-derived two-Black-wire dry-contact pair** is
connected:

| VHF-derived pair | ESP32 termination | Status |
|-----------|-------------------|--------|
| Black conductor | GPIO26 / board label D26 | **Physically verified 2026-09-08** |
| Black conductor | GND | Existing dry-contact return; physically verified |

The two Black conductors may be swapped because this is an isolated dry contact.
GPIO26 uses the ESP32 internal pull-up and 25 ms software debounce. Do not connect
either conductor to 3.3 V or 5 V.

Authoritative source logic:

| Debounced VHF state | Logical source | Phase 2 WiiM action |
|----------------------|----------------|----------------------|
| Closed / latched | Digital Streamer | Restore phone-controlled digital playback |
| Open / released | Vinyl | Select Line-In |

Pressing SW, MW, LW or Gram releases VHF through the retained interlock. Those
positions have no individual ESP32 input; the open VHF state authoritatively
selects Vinyl. Their former conductors are disconnected and individually
insulated at the controller end. GPIO13, GPIO16, GPIO17, GPIO19 and GPIO23 are not
assigned.

A purpose-built replacement button panel is a deferred fallback if the two-state
scheme later proves insufficient. No LW solder repair is required for the
current design.

## Stereo/Mono Control

**GPIO25 / D25** is the active-low digital input with the ESP32
internal pull-up. Wire the isolated contact only:

| Stereo/Mono contact | ESP32 termination |
|---------------------|-------------------|
| Contact that closes in Mono | GPIO25 / board label D25 |
| Common / return | GND |

Do not connect either contact to 3.3 V or 5 V. Open/HIGH means **Stereo** and
requests dial lights on; closed/LOW means **Mono** and requests them off. The
switch behaviour was accepted on the previous GPIO17/TX2 route on 2026-08-30.
The GPIO25 firmware input and requested lighting logic are correct, but the
retained switch does not currently close in Mono; repair is open as HW-SW-01.
GPIO18 and the lamp load are commissioned separately. See ADR-0016.

## H4 — OLED Display

Purchased panel: Pi Hut SKU 105630, 1.3-inch white 128×64 **SH1106 I²C** OLED
with a pre-soldered four-pin header. Expected address: **0x3C**.

- VCC → 3.3 V (Red)
- GND → GND (Brown)
- SDA → GPIO21 / board label **D21** (Yellow, bench-verified)
- SCL → GPIO22 / board label **D22** (Orange, bench-verified)

The H4 Orange and Yellow signal colours are a documented exception to the
general loom colour standard. Orange is the SCL signal and Yellow is the SDA
signal; neither conductor is a power rail.

Check the labels printed on the delivered module before applying power because
four-pin OLED modules do not all use the same physical pin order.

Bench verification completed 2026-08-25. The panel responded as an SH1106 at
0x3C on GPIO21/GPIO22, all ten on-target `test_display` cases passed, and visual
inspection confirmed the startup and revised dashboard were upright, complete,
unclipped and free of persistent display artefacts. Final loom orientation was
physically confirmed on 2026-08-30: Brown = GND, Red = VCC, Orange = SCL and
Yellow = SDA.

## H5 — Dial Illumination

- Purchased lamp set: **ShuoHui E10 miniature screw LEDs**, ASIN
  **B0CFTLZFGT**, pack of 10; **6 V AC/DC, 0.2 W, 3000 K**. Three are required.
- The three-lamp bank is electrically accepted from the locked 5 V rail.
  Final holder fit, operating brightness and measured total current remain
  installation/commissioning checks.
- Wire the three validated lamps **in parallel**.
- Installed final switch: one **DFRobot Gravity MOSFET Power Controller,
  DFR0457**. Its 3.3 V control input is driven by ESP32 **GPIO18 / board label
  D18** and firmware PWM is set to its 1 kHz DC switching limit.
- Steady-light testing reports no flicker. The earlier v0.27.1 fade observations
  are superseded: installed LEDs held brightness and then switched only after the
  delay. Deployed v0.27.4 removes the fade engine and writes on/off duties
  immediately. Repeat the immediate transition, pot-stability, temperature and
  lamp-current checks before closing HW-LGT-01.
- The previously tested DAOKAI pack is retained as test stock but is superseded
  for the final installation.
- ESP32 and lighting grounds are **common**.
- Normal brightness is owner-approved at **85% / duty 217**, stored in
  non-volatile settings and treated as a setup value rather than a normal user
  control. Mono and logical standby command zero. The unused
  aerial control may be used temporarily for commissioning if convenient, but is
  not reserved permanently for lighting.

Expected behaviours: immediate Stereo/Mono and logical power response,
stored/configurable brightness and safe boot state. Firmware
support is implemented. GPIO18, the MOSFET stage and the
three-lamp electrical load passed the dial-lighting bench procedure on
2026-08-31. Subsequent 70%, 80% and 100% comparisons established the approved
normal level is now 85%; Mono and standby are off. Final DFR0457 integration and
installed-holder checks remain open.

## H6 — Fosi ZA3 12 V Trigger

- The **Fosi Audio ZA3** is the locked stereo power amplifier.
- H6 connects the WiiM Pro **12 V trigger output** directly to the ZA3 trigger
  input using the correct 2.5 mm-to-3.5 mm lead/adaptor (ADR-0018).
- The ESP32 must **not** connect to, source or sense the trigger voltage.
- WiiM awake/playback behaviour asserts the trigger and enables the ZA3; WiiM
  automatic standby removes it. Exact behaviour and delay require bench acceptance.
- No ESP32-controlled 230 V mains relay is required for the amplifier.

## Power Distribution

The approved low-voltage controller path is:

`external Phihong adapter -> soldered low-voltage connection -> reused inline 2 A fuse on +5 V -> +5 V / GND distribution -> ESP32 and H5 lighting`

- Locked controller architecture: **one regulated 5 V control rail**, with 3.3 V
  derived by the ESP32 board regulator for logic/ADC and the OLED as documented.
- Selected/acquired supply: **Phihong PSA15R-050P**, **5.0 V DC at 3.0 A
  (15 W)**.
- The adapter's enclosed mains side remains intact. Its isolated low-voltage
  output lead is soldered directly into the Decca low-voltage wiring; the
  purchased TopHomer panel DC sockets are obsolete and must not be fitted for
  this route.
- The original Decca inline fuse holder is implemented in the +5 V conductor
  immediately after that soldered connection and before distribution. One 2 A
  fuse is fitted and one is retained as a spare; recheck the rating against
  measured total lamp current during commissioning.
- Use two **WAGO 221-415 five-way lever connectors** from Pi Hut pack SKU
  **104130**: one as the +5 V star point and one as the common-GND star point.
  Retain the third connector in the pack as a spare.
- The +5 V distribution branches to the ESP32 **5V/VIN** terminal and the positive
  side of all three E10 lamps. Never connect this rail to the ESP32 **3V3**
  terminal.
- The GND distribution branches to ESP32 GND and the lighting MOSFET source/GND.
  The lamp negatives return through the MOSFET switched output; they must never
  be driven directly from GPIO18.
- Use 22–24 AWG stranded Orange wire for +5 V and Brown wire for GND, with
  correctly sized ferrules at screw and lever terminals.
- **No dedicated 6 V/6.3 V lighting rail** is required or planned.
- The WiiM Pro remains continuously powered and uses its own automatic standby.
- The Fosi ZA3 PSU may remain energised; the amplifier state is controlled by the
  direct WiiM-to-ZA3 H6 trigger connection.
- The single-mains-lead cabinet arrangement is an active implementation using an
  acquired IEC C14 inlet, an ordered UK C13 lead and an ordered enclosed
  Masterplug four-gang distribution block. The Rev B mounting plate is the only
  active plate design; it is CAD-passed but physical-fit pending. Do not use the
  rejected Rev A plate, and do not energise mains until inlet fit, fixing
  alignment, flat clamping, enclosure retention, earthing, terminal insulation
  and rear wire clearance have been verified.
- The ESP32 remains powered when the Decca front-panel switch is OFF so it can
  detect the next state change.
- The ESP32 carries **control and UI only**. It does **not** process or carry
  audio.

## Diagrams

Point-to-point harness diagrams are held in `hardware/Wiring/`.
