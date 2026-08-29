# Wiring

> **Status:** active. This is the authoritative interconnect reference. Pin
> assignments marked **(proposed)** are documented intent and have **not** been
> bench-verified. Confirmed items reflect the physical build.

Records every physical connection so the build is reproducible. The firmware pin
map (`src/hardware.h`) must be reconciled against this document before any build
(see Specification `HW-06`). `hardware.h` matches the status recorded below:
the four pot inputs, the VHF, MW and Gram source inputs, and OLED I²C GPIO21/22
are bench-verified; LW and all other assigned pins remain proposed.

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

**Exception — H4 OLED harness.** The installed and bench-verified screen loom
uses **Orange for SDA** and **Yellow for SCL**. These are signal conductors in H4:
the Orange SDA wire must **never** be connected to the 5 V rail. H4 retains Red
for 3.3 V and Brown for GND. See the OLED section.

H3 uses separate two-wire contact pairs; it has no common-return conductor.
The pairs are recorded in physical left-to-right order under H3. VHF, MW and
Gram are bench-verified; LW awaits repair and retest.

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
| On/off switch (Red)   | GPIO19 (proposed) | D19 | Digital in  | H2      | Internal pull-up; low-voltage logic only |
| Source: VHF           | GPIO16 (bench-verified) | RX2 | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: MW            | GPIO17 (bench-verified) | TX2 | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: LW            | GPIO18 (proposed) | D18 | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: Gram          | GPIO23 (bench-verified) | D23 | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: SW            | —               | — | —           | H3      | **NO FUNCTION in Phase 1** (see below)   |
| OLED SDA              | GPIO21 (bench-verified) | D21 | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| OLED SCL              | GPIO22 (bench-verified) | D22 | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| Dial lighting PWM     | GPIO25 (proposed) | D25 | PWM (LEDC)  | H5      | Gate of logic-level N-ch MOSFET          |
| ZA3 trigger control   | TBD             | TBD | Digital out | H6      | Drives 12 V trigger interface, never 12 V directly |

> The four source-button GPIOs avoid strapping pins and support internal
> pull-ups. GPIO16, GPIO17 and GPIO23 are bench-verified. GPIO18 remains
> proposed until the repaired LW pair passes the H3 verification procedure.

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
- Interface (proposed): **Red → ESP32 GPIO19 / board label D19** input with **internal pull-up
  enabled**; **Green → GND**.
- This is a **low-voltage logic input only**. It does **not** switch 230 V mains.
- Logical inversion may be applied in firmware after bench testing.
- The switch is a **system-state command**. ON causes the ESP32 to assert the ZA3
  trigger, illuminate the dial and enable the OLED; OFF reverses those actions
  and allows the WiiM Pro to use its own automatic standby behaviour.

## H3 — Radio/Source Button Bank

The **original PCB is retained** because it is the mechanical carrier for the
interlocked selector mechanism. It is **not** disposable and must not be removed.
See ADR-0001.

Fascia order (top to bottom): **VHF, SW, MW, LW, Gram.**

Confirmed wiring findings:

- Usable contact pairs were found and wired for **VHF, MW, LW, Gram**.
- A **unique SW-only** contact pair could **not** be found; the pair that closed
  for SW also switched with Gram.
- Therefore **SW is intentionally NO FUNCTION in the first pass**. No microswitch
  workaround is added in the current design.

Phase 1 behaviour:

| Button | Phase 1 state              |
|--------|----------------------------|
| VHF    | Selectable input state     |
| MW     | Selectable input state     |
| LW     | Selectable input state     |
| Gram   | Selectable input state     |
| SW     | No function / deferred     |

The four working inputs are treated as simple low-voltage GPIO signals with
software debounce. Final Phase 2 WiiM source mappings remain configurable in
software (see Specification and ADR-0004).

Controller termination, derived from physical pair order and tested one pair at
a time on 2026-08-24:

| Physical order | Button | Contact pair | ESP32 input | Board label | Individual return | Status |
|----------------|--------|--------------|-------------|-------------|-------------------|--------|
| Leftmost / top | VHF    | Yellow + Green (left-hand pair) | GPIO16 | RX2 | Green → GND | Bench-verified |
| —              | SW     | No unique isolated pair | — | — | No Phase 1 connection | Deferred |
| Second working pair | MW | Purple + Blue | GPIO17 | TX2 | Blue → GND | Bench-verified |
| Third working pair | LW | Yellow + Orange | GPIO18 | D18 | Orange → GND | Solder repair and retest required |
| Rightmost / bottom | Gram | Green + Yellow (right-hand pair) | GPIO23 | D23 | Yellow → GND | Bench-verified |

The first colour in each working pair is the GPIO conductor and the second is
its individual GND return. These are dry
contacts, so the two conductors within a pair may be swapped without changing
operation. There is no shared return in H3. The ESP32 provides the pull-up; do
not connect any contact to 3.3 V or 5 V. RX2 and TX2 are the board's silkscreen
labels for GPIO16 and GPIO17 and are available because UART2 is unused.
Firmware accepts a changed state after 25 ms of stability and emits one event
on each confirmed selection without repeating while held.

The VHF, MW and Gram pair tests passed. The LW pair was identified as Yellow +
Orange but failed electrically at the existing joint; repair and repeat the
GPIO18 test before marking LW bench-verified.

## Stereo/Mono Control

Retained mechanically, **unwired**, decorative in Phase 1, deferred for possible
future use. **No function assigned.** See ADR-0005.

## H4 — OLED Display

Purchased panel: Pi Hut SKU 105630, 1.3-inch white 128×64 **SH1106 I²C** OLED
with a pre-soldered four-pin header. Expected address: **0x3C**.

- VCC → 3.3 V (Red)
- GND → GND (Brown)
- SDA → GPIO21 / board label **D21** (Orange, bench-verified)
- SCL → GPIO22 / board label **D22** (Yellow, bench-verified)

The H4 Orange and Yellow signal colours are a documented exception to the
general loom colour standard. In particular, do not treat the Orange SDA
conductor as 5 V.

Check the labels printed on the delivered module before applying power because
four-pin OLED modules do not all use the same physical pin order.

Bench verification completed 2026-08-25. The panel responded as an SH1106 at
0x3C on GPIO21/GPIO22, all ten on-target `test_display` cases passed, and visual
inspection confirmed the startup and revised dashboard were upright, complete,
unclipped and free of persistent display artefacts.

## H5 — Dial Illumination

- **Three identical E10/MES warm-white LED lamps** in the three original holders.
- Target lamp geometry: approximately **24 mm overall length**, matching the
  original bulb form factor closely enough to retain the original optics/position.
- Preferred colour temperature: **2200–3000 K**.
- Lamps must be compatible with the locked **5 V lighting rail**. Accept nominal
  5 V devices or a specified operating range that includes 5 V (for example
  1–5 V or 3–6 V).
- The three lamps are wired **in parallel**.
- One **logic-level N-channel MOSFET** low-side switches the complete lamp bank;
  ESP32 drives the gate.
- **PWM** controlled by the ESP32 (proposed **GPIO25 / board label D25**, LEDC).
- ESP32 and lighting grounds are **common**.
- Brightness is set during commissioning, stored in non-volatile settings and
  then treated as a setup value rather than a normal user control. The unused
  aerial control may be used temporarily for commissioning if convenient, but is
  not reserved permanently for lighting.

Expected behaviours: fade up, fade down, stored/configurable brightness, safe
boot state. Firmware support is implemented; GPIO25 and the MOSFET/load wiring
remain proposed until the dial-lighting bench procedure passes.

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
- The panel-mount female DC socket must match the actual adapter plug and be rated
  for at least 5 V / 3 A. A 5.5 mm OD × 2.1 mm ID centre-positive connection is
  the provisional expectation only; verify the physical plug and polarity before
  ordering or wiring the socket.
- Fit a **2 A low-voltage fuse** in the +5 V conductor immediately after the
  socket and before distribution. Recheck the rating against measured total lamp
  current during commissioning.
- Use two three-way distribution connectors, preferred **Wago 221-413** or
  equivalent: one +5 V connector and one GND connector.
- The +5 V distribution branches to the ESP32 **5V/VIN** terminal and the positive
  side of all three E10 lamps. Never connect this rail to the ESP32 **3V3**
  terminal.
- The GND distribution branches to ESP32 GND and the lighting MOSFET source/GND.
  The lamp negatives return through the MOSFET switched output; they must never
  be driven directly from GPIO25.
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
