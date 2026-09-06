# Wiring

> **Status:** active. This is the authoritative interconnect reference. Pin
> assignments marked **(proposed)** are documented intent and have **not** been
> bench-verified. Confirmed items reflect the physical build.

Records every physical connection so the build is reproducible. The firmware pin
map (`src/hardware.h`) must be reconciled against this document before any build
(see Specification `HW-06`). `hardware.h` matches the status recorded below:
the four pot inputs, sole VHF source input and OLED I²C GPIO21/22 are verified.
On/off GPIO26 and lighting PWM GPIO18 are new assignments awaiting the
controlled transition and physical verification; GPIO19 and GPIO25 are the
previously verified assignments.

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
to GPIO23 with the other connected to GND. See the H3 section.

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
| H6  | ZA3 12 V trigger harness    |

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
| On/off switch (Red)   | GPIO26 (verification pending) | D26 | Digital in | H2 | Internal pull-up; closed = ON; GPIO19/D19 previously verified |
| Source selector: VHF | GPIO23 (physically accepted) | D23 | Digital in | H3 | Closed = Digital Streamer; open = Vinyl |
| SW / MW / LW / Gram  | — | — | No individual GPIO | H3 | Mechanical positions release VHF and select Vinyl |
| Stereo/Mono          | GPIO17 (assigned) | TX2 | Digital in, pull-up | H3 | Open Stereo = lights requested on; closed Mono = off |
| OLED SDA              | GPIO21 (bench-verified) | D21 | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| OLED SCL              | GPIO22 (bench-verified) | D22 | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| Dial lighting PWM     | GPIO18 (verification pending) | D18 | PWM (LEDC), 1 kHz | H5 | DFR0457 control input; no external pull-down currently fitted; GPIO25/D25 previously accepted |
| ZA3 trigger control   | TBD             | TBD | Digital out | H6      | Drives 12 V trigger interface, never 12 V directly |

> GPIO23 and GPIO26 support the required internal pull-ups. GPIO18 and GPIO26
> are ordinary bidirectional GPIOs, are not ESP32 boot-strapping pins, and do
> not conflict with any enabled peripheral in this repository. GPIO16 remains
> released for future use. GPIO17 is
> reserved for the separate Stereo/Mono contact and must not be connected to
> the unreliable source-selector contacts.

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
- New interface (physical verification pending): **Red → ESP32 GPIO26 /
  board label D26** input with **internal pull-up enabled**; **Green → GND**.
- Historical fact: the same switch and polarity were bench-verified on
  **GPIO19 / D19** on 2026-08-30.
- This is a **low-voltage logic input only**. It does **not** switch 230 V mains.
- Confirmed logic: closed/active-low = ON; open = STANDBY. Both directions were
  physically accepted with production firmware on 2026-08-30.
- The switch is a **system-state command**. ON causes the ESP32 to assert the ZA3
  trigger, illuminate the dial and enable the OLED; OFF reverses those actions
  and allows the WiiM Pro to use its own automatic standby behaviour.

## H3 — Radio/Source Button Bank

The original PCB and interlocked selector mechanism are retained mechanically
(ADR-0001). Repeated soldering and contact tests showed that multi-button
electrical reuse is not reliable. ADR-0013 supersedes ADR-0011 and ADR-0004.

Only the physically accepted **VHF-derived two-Black-wire dry-contact pair** is
connected:

| VHF-derived pair | ESP32 termination | Status |
|-----------|-------------------|--------|
| Black conductor | GPIO23 / board label D23 | Bench-verified input |
| Black conductor | GND | Bench-verified return |

The two Black conductors may be swapped because this is an isolated dry contact.
GPIO23 uses the ESP32 internal pull-up and 25 ms software debounce. Do not connect
either conductor to 3.3 V or 5 V.

Authoritative source logic:

| Debounced VHF state | Logical source | Phase 2 WiiM action |
|----------------------|----------------|----------------------|
| Closed / latched | Digital Streamer | Restore phone-controlled digital playback |
| Open / released | Vinyl | Select Line-In |

Pressing SW, MW, LW or Gram releases VHF through the retained interlock. Those
positions have no individual ESP32 input; the open VHF state authoritatively
selects Vinyl. Their former conductors are disconnected and individually
insulated at the controller end. GPIO16 is not assigned; GPIO17 is reserved for
the separate Stereo/Mono contact and GPIO18 is now reserved for dial-light PWM.

A purpose-built replacement button panel is a deferred fallback if the two-state
scheme later proves insufficient. No LW solder repair is required for the
current design.

## Stereo/Mono Control

TX2 / **GPIO17** is assigned as an active-low digital input with the ESP32
internal pull-up. Wire the isolated contact only:

| Stereo/Mono contact | ESP32 termination |
|---------------------|-------------------|
| Contact that closes in Mono | GPIO17 / board label TX2 |
| Common / return | GND |

Do not connect either contact to 3.3 V or 5 V. Open/HIGH means **Stereo** and
requests dial lights on; closed/LOW means **Mono** and requests them off. This
assignment and both physical input states were accepted on 2026-08-30.
The lighting output and lamp load are commissioned separately. See ADR-0014, which
supersedes ADR-0005.

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
  DFR0457**. Its 3.3 V control input is assigned to ESP32 **GPIO18 / board label
  D18** and firmware PWM remains at its 1 kHz DC switching limit. A 10 kΩ
  resistor from the DFR0457 control/PWM input to common GND is recommended for
  defined reset-time safe-off, but the owner has elected not to fit it at this
  time.
- Steady-light and v0.27.1 fade testing report no flicker; cold startup and both
  approximately 4.34-second fade directions are owner-approved. Repeat
  pot-stability, temperature and lamp-current tests before closing HW-LGT-01.
- The previously tested DAOKAI pack is retained as test stock but is superseded
  for the final installation.
- ESP32 and lighting grounds are **common**.
- Normal brightness is owner-approved at **85% / duty 217**, stored in
  non-volatile settings and treated as a setup value rather than a normal user
  control. Mono and logical standby command zero. The unused
  aerial control may be used temporarily for commissioning if convenient, but is
  not reserved permanently for lighting.

Expected behaviours: fade up, fade down, stored/configurable brightness, safe
boot state. Firmware support is implemented. As a historical result, GPIO25,
the MOSFET stage and the three-lamp electrical load passed the dial-lighting
bench procedure on 2026-08-31. GPIO18/D18 awaits physical verification after
the controlled transition. Subsequent 70%, 80% and 100% comparisons established
the approved normal level is now 85%; Mono and standby are off. Final DFR0457
integration and installed-holder checks remain open.

### D18 control wiring

```text
ESP32 D18 / GPIO18 ----------------- DFR0457 control/PWM input
ESP32 GND -------------------------- DFR0457 GND / common 5 V return

5 V fused star --------------------- lamp positives / DFR0457 power path
DFR0457 switched output ------------- three lamp negatives in parallel
```

Firmware configures D18 as output LOW before any other peripheral
initialisation, then attaches LEDC at duty 0. Normal operation remains 1 kHz,
duty 217/255, with 20 ms one-count fade steps. Mono and logical standby fade to
duty 0 and hold the output LOW. Because no external pull-down is currently
fitted, the ESP32 cannot guarantee D18 LOW during reset and before `setup()`;
observe specifically for any lamp flash during physical verification.

### Controlled D19/D25 to D26/D18 transition

The known starting state is the ESP32 powered off with the switch signal still
on D19 and the DFR0457 control signal still on D25. Do not move either conductor
while powered.

1. Leave both old signal wires on D19/D25. The owner has explicitly deferred the
   recommended external D18 control-input pull-down.
2. After code review, successful builds/tests, hostname/IP/service checks and
   explicit owner approval, power the unchanged old wiring and upload v0.28.0
   by authenticated OTA only.
3. After reboot, D26 is disconnected and therefore reads HIGH/standby; D18 is
   disconnected from the DFR0457 and is driven safely LOW. Confirm OTA returns.
4. Power the ESP32 and shared 5 V rail off and confirm power-off before touching
   wiring.
5. Move only the on/off signal conductor from D19 to D26, retaining its GND
   conductor. Move only the DFR0457 control/PWM signal from D25 to D18.
6. Inspect and confirm the wiring before restoring power. Then verify OTA,
   active-low on/off behaviour, no boot flash, 1 kHz PWM, duty 217 and both
   approximately 4.34-second fades.

Stop if any prerequisite or conductor identity is uncertain. Do not adjust any
potentiometer as part of this transition.

## H6 — Fosi ZA3 12 V Trigger

- The **Fosi Audio ZA3** is the locked stereo power amplifier.
- Its operating state is controlled using the amplifier's **12 V trigger input**.
- The ESP32 must **not** connect directly to or source the 12 V trigger voltage.
- H6 therefore consists of an ESP32-controlled low-voltage driver stage plus a
  suitable 12 V source and the cable to the ZA3 trigger input.
- Exact GPIO, transistor/MOSFET or isolated driver, protection components and 12 V
  source remain **open implementation items** until component selection and bench
  verification.
- Trigger asserted = Decca system ON / ZA3 enabled.
- Trigger removed = Decca system OFF / ZA3 trigger-controlled off or standby.
- No ESP32-controlled 230 V mains relay is required for the amplifier.

## Power Distribution

The approved low-voltage controller path is:

`external Phihong adapter -> panel DC socket -> 2 A fuse on +5 V -> +5 V / GND distribution -> ESP32 and H5 lighting`

- Locked controller architecture: **one regulated 5 V control rail**, with 3.3 V
  derived by the ESP32 board regulator for logic/ADC and the OLED as documented.
- Selected/acquired supply: **Phihong PSA15R-050P**, **5.0 V DC at 3.0 A
  (15 W)**.
- The adapter remains enclosed and external by default. Only its isolated
  low-voltage output enters the cabinet; this controller path adds no internal
  230 V connection.
- Purchased input-socket set: **TopHomer ASIN B08HGXYS4J**, pack of five
  female two-terminal threaded-nut panel sockets, **5.5 mm OD × 2.1 mm ID** and
  rated **3 A**; one is required.
- The purchase closes socket procurement, not validation. Confirm the actual
  Phihong plug fit and centre-positive polarity before drilling or wiring the
  selected socket.
- Fit a **2 A low-voltage fuse** in the +5 V conductor immediately after the
  socket and before distribution. Recheck the rating against measured total lamp
  current during commissioning.
- Use two **WAGO 221-415 five-way lever connectors** from Pi Hut pack SKU
  **104130**: one as the +5 V star point and one as the common-GND star point.
  Retain the third connector in the pack as a spare.
- The +5 V distribution branches to the ESP32 **5V/VIN** terminal and the positive
  side of all three E10 lamps. Never connect this rail to the ESP32 **3V3**
  terminal.
- The GND distribution branches to ESP32 GND and the lighting MOSFET source/GND.
  The lamp negatives return through the MOSFET switched output; they must never
  be driven directly from GPIO18 (or the previous GPIO25 assignment).
- Use 22–24 AWG stranded Orange wire for +5 V and Brown wire for GND, with
  correctly sized ferrules at screw and lever terminals.
- **No dedicated 6 V/6.3 V lighting rail** is required or planned.
- The WiiM Pro remains continuously powered and uses its own automatic standby.
- The Fosi ZA3 PSU may remain energised; the amplifier state is controlled by H6
  via its 12 V trigger input.
- A future single-mains-lead cabinet arrangement remains a separate open design
  decision and must not be improvised from the low-voltage parts above.
- The ESP32 remains powered when the Decca front-panel switch is OFF so it can
  detect the next state change.
- The ESP32 carries **control and UI only**. It does **not** process or carry
  audio.

## Diagrams

Point-to-point harness diagrams are held in `hardware/Wiring/`.
