# Wiring

> **Status:** active. This is the authoritative interconnect reference. Pin
> assignments marked **(proposed)** are documented intent and have **not** been
> bench-verified. Confirmed items reflect the physical build.

Records every physical connection so the build is reproducible. The firmware pin
map (`src/hardware.h`) must be reconciled against this document before any build
(see Specification `HW-06`). `hardware.h` matches the status recorded below:
the four pot inputs and the VHF, MW and Gram source inputs are bench-verified;
LW and all other assigned pins remain proposed.

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

## Pin Map

All ESP32 pin numbers below are **(proposed)** unless stated otherwise.

| Signal                | ESP32 Pin       | Type        | Harness | Notes                                    |
|-----------------------|-----------------|-------------|---------|------------------------------------------|
| Volume pot wiper      | GPIO32 (bench-verified) | ADC1        | H1      | ADC1 required (Wi-Fi in Phase 2)         |
| Bass pot wiper        | GPIO33 (bench-verified) | ADC1        | H1      | ADC1 required                            |
| Treble pot wiper      | GPIO34 (bench-verified) | ADC1, in-only | H1    | ADC1; input-only pin, no pull-up needed  |
| Balance pot wiper     | GPIO35 (bench-verified) | ADC1, in-only | H1    | ADC1; input-only pin                     |
| On/off switch (Red)   | GPIO19 (proposed) | Digital in  | H2      | Internal pull-up; low-voltage logic only |
| Source: VHF           | GPIO16 (bench-verified) | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: MW            | GPIO17 (bench-verified) | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: LW            | GPIO18 (proposed) | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: Gram          | GPIO23 (bench-verified) | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: SW            | —               | —           | H3      | **NO FUNCTION in Phase 1** (see below)   |
| OLED SDA              | GPIO21 (proposed) | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| OLED SCL              | GPIO22 (proposed) | I²C         | H4      | Pi Hut SH1106, address 0x3C              |
| Dial lighting PWM     | GPIO25 (proposed) | PWM (LEDC)  | H5      | Gate of logic-level N-ch MOSFET          |

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

Termination (confirmed): ends soldered directly to the lugs, insulated with
heat-shrink, mechanically strain-relieved, and terminated through a removable
connector at the controller end.

Bench verification completed 2026-08-24 with each control connected to its
named ADC1 channel. All readings increased clockwise and the on-target
`test_pots` suite passed all six test cases.

| Control | GPIO | Anticlockwise | Approx. centre | Clockwise |
|---------|------|---------------|----------------|-----------|
| Volume  | 32   | 0             | 2047           | 4095      |
| Bass    | 33   | 0             | 2047           | 4095      |
| Treble  | 34   | 0             | 2047           | 4095      |
| Balance | 35   | 0             | 2047           | 4095      |

The controls have no centre detent, so the centre readings vary slightly with
manual positioning. The observed endpoints match the firmware's default
0–4095 calibration; no per-pot endpoint override or inversion is required.

## H2 — Original On/Off Switch

The original Decca on/off switch is retained, including its **original solder
joints and original cable**. It is a simple open/close switch.

- Active conductors (confirmed): **Red** and **Green**.
- Interface (proposed): **Red → ESP32 GPIO19** input with **internal pull-up
  enabled**; **Green → GND**.
- This is a **low-voltage logic input only**. It does **not** switch 230 V mains.
- Logical inversion may be applied in firmware after bench testing.

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
- SDA → GPIO21 (proposed)
- SCL → GPIO22 (proposed)

Check the labels printed on the delivered module before applying power because
four-pin OLED modules do not all use the same physical pin order. GPIO21 and
GPIO22 remain proposed until the H4 bench procedure passes.

## H5 — Dial Illumination

- 5 V warm-white lighting.
- Driven through a **logic-level N-channel MOSFET**; ESP32 drives the gate.
- **PWM** controlled by the ESP32 (proposed **GPIO25**, LEDC).
- ESP32 and lighting grounds are **common**.

Expected behaviours: fade up, fade down, configurable idle brightness, safe boot
state. Firmware support is implemented; GPIO25 and the MOSFET/load wiring remain
proposed until the dial-lighting bench procedure passes.

## Power Distribution

- Rails: 5 V and 3.3 V (see Hardware Architecture for the budget).
- The ESP32 carries **control and UI only**. It does **not** process or carry
  audio.

## Diagrams

Point-to-point harness diagrams are held in `hardware/Wiring/`.
