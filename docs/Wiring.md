# Wiring

> **Status:** active. This is the authoritative interconnect reference. Pin
> assignments marked **(proposed)** are documented intent and have **not** been
> bench-verified. Confirmed items reflect the physical build.

Records every physical connection so the build is reproducible. The firmware pin
map (`src/hardware.h`) must be reconciled against this document before any build
(see Specification `HW-06`). `hardware.h` matches the status recorded below:
the four pot inputs are bench-verified; all other assigned pins remain proposed.

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

For the button harness, wires are identified by **function label**, not by colour
(button-harness colours are not yet fully locked).

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
| Source: VHF           | (proposed)      | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: MW            | (proposed)      | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: LW            | (proposed)      | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: Gram          | (proposed)      | Digital in  | H3      | Internal pull-up + software debounce     |
| Source: SW            | —               | —           | H3      | **NO FUNCTION in Phase 1** (see below)   |
| OLED SDA              | GPIO21 (proposed) | I²C         | H4      | SH1106/SSD1306-compatible                |
| OLED SCL              | GPIO22 (proposed) | I²C         | H4      | Standard I²C SCL                         |
| Dial lighting PWM     | GPIO25 (proposed) | PWM (LEDC)  | H5      | Gate of logic-level N-ch MOSFET          |

> Specific GPIOs for the four working source buttons are **not yet assigned**;
> they are to be selected from free digital-capable, pull-up-capable pins during
> firmware bring-up and recorded here.

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

## Stereo/Mono Control

Retained mechanically, **unwired**, decorative in Phase 1, deferred for possible
future use. **No function assigned.** See ADR-0005.

## H4 — OLED Display

1.3-inch, 128×64, **I²C**, SH1106- or SSD1306-compatible.

- SDA → GPIO21 (proposed)
- SCL → GPIO22 (proposed)

## H5 — Dial Illumination

- 5 V warm-white lighting.
- Driven through a **logic-level N-channel MOSFET**; ESP32 drives the gate.
- **PWM** controlled by the ESP32 (proposed **GPIO25**, LEDC).
- ESP32 and lighting grounds are **common**.

Expected behaviours: fade up, fade down, configurable idle brightness, safe boot
state.

## Power Distribution

- Rails: 5 V and 3.3 V (see Hardware Architecture for the budget).
- The ESP32 carries **control and UI only**. It does **not** process or carry
  audio.

## Diagrams

Point-to-point harness diagrams are held in `hardware/Wiring/`.
