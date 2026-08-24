# Build Guide

> **Status:** placeholder. Populate as the physical build progresses.

Step-by-step guide to reproducing the decca build, from bare cabinet to working
music centre. This document should let a competent maker rebuild the project
from parts.

## 1. Before You Start
- Tools required
- Skills assumed (soldering, basic CAD/printing, PlatformIO)
- Safety notes (mains, dust, original finish)

## 2. Preparing the Cabinet
- Assessment and restoration of the original piece
- What is preserved vs. replaced
- Cleaning and refinishing notes

## 3. Electronics Assembly
- ESP32 and peripheral mounting
- Wiring the front-panel controls
- Power supply and rails
- Cross-references: [Wiring](Wiring.md), [Parts List](Parts List.md)

## 4. Mechanical Fit-Out
- Display mounting behind the dial glass
- Knob adaptors (see `mechanical/Knob Adaptors/`)
- Lighting placement

## 5. Firmware Flashing
- Installing PlatformIO
- First build and upload
- Cross-reference: `README.md` → Development Workflow

## 6. First Power-On
- Bring-up checklist
- Smoke-test procedure
- Common issues

## 7. Commissioning

### 7.1 Potentiometer bench verification

This procedure passed on 2026-08-24, confirming the four GPIO assignments. Keep
it as the commissioning method after any harness rework or controller
replacement. Keep the Decca disconnected from mains; power only the ESP32 and
the low-voltage pot harness by USB during this test.

1. With the harness disconnected, measure each 10 kΩ linear pot:
   - resistance between the two outside lugs should remain approximately 10 kΩ;
   - resistance from centre wiper to each outside lug should change smoothly
     and in opposite directions through the full travel.
2. Viewed from the rear of each installed pot, connect left lug to GND (Brown),
   centre wiper to its ADC1 pin (White), and right lug to 3.3 V (Red):

   | Control | Bench-verified wiper pin |
   |---------|---------------------------|
   | Volume  | GPIO32                    |
   | Bass    | GPIO33                    |
   | Treble  | GPIO34                    |
   | Balance | GPIO35                    |

3. Set all four controls fully anticlockwise, connect the ESP32 by USB, and run:

   ```powershell
   pio test -e esp32dev -f test_pots
   ```

4. Record the four raw readings from the line beginning `POT_SNAPSHOT`.
5. Repeat with all four controls centred, then fully clockwise.
6. Verify direction and channel identity with four more runs: set one control
   fully clockwise and the other three fully anticlockwise, changing the
   clockwise control each run.

Pass criteria:

- each named reading responds only to its matching physical control;
- readings change monotonically through the travel without large discontinuities;
- each control reaches at least below 250 and above 3800 raw counts;
- the midpoint is broadly central (typically 1600–2500 raw counts);
- the physical snapshot test and all five deterministic behavioural tests in
  the suite pass on the ESP32.

Record the observed low/high endpoints before applying per-pot calibration.
If a control is electrically sound but its value falls as it turns clockwise,
use the firmware's per-pot `inverted` calibration option rather than placing the
ESP32 in any audio path.

Recorded result (2026-08-24):

| Control | GPIO | Anticlockwise | Approx. centre | Clockwise | Direction |
|---------|------|---------------|----------------|-----------|-----------|
| Volume  | 32   | 0             | 2047           | 4095      | Increasing clockwise |
| Bass    | 33   | 0             | 2047           | 4095      | Increasing clockwise |
| Treble  | 34   | 0             | 2047           | 4095      | Increasing clockwise |
| Balance | 35   | 0             | 2047           | 4095      | Increasing clockwise |

All six `test_pots` cases passed. Midpoint variation is expected because the
controls have no centre detent. The default 0–4095 calibration is retained with
no inversion.

### 7.2 Source-button bench verification

The proposed H3 inputs are active-low and use the ESP32's internal pull-ups.
Keep the Decca disconnected from mains and power only the ESP32 by USB.

| Physical order | Proposed button | Contact pair | Proposed test termination |
|----------------|-----------------|--------------|-----------------------------|
| Leftmost / top | VHF             | Yellow + Green (left-hand pair) | Yellow → GPIO16 / RX2; Green → GND |
| —              | SW              | No unique isolated pair | Leave disconnected |
| Second working pair | MW         | Purple + Blue | Purple → GPIO17 / TX2; Blue → GND |
| Third working pair | LW          | Orange + Red | Orange → GPIO18 / D18; Red → GND |
| Rightmost / bottom | Gram        | Green + Yellow (right-hand pair) | Green → GPIO23 / D23; Yellow → GND |

1. Identify the four pairs by their physical left-to-right order. Distinguish
   the left-hand and right-hand Green/Yellow pairs before connecting either.
2. Test only one pair at a time. Connect one conductor to its proposed GPIO and
   the other conductor from the same pair to GND as shown. Each pair has its own
   return; H3 has no common-return wire. Do not connect any contact to 3.3 V or
   5 V. Because these are dry contacts, swapping the two conductors within one
   pair does not affect the result.
3. Connect the ESP32 by USB and run:

   ```powershell
   pio test -e esp32dev -f test_buttons
   ```

4. Record the line beginning `BUTTON_SNAPSHOT`. A selected source is shown as
   `1`; an open contact is shown as `0`.
5. Repeat with the proposed VHF, MW, LW and Gram pairs in turn, disconnecting
   the previous pair before connecting the next. Ignore `onoff` unless the H2
   harness is also connected.

Pass criteria:

- each selection sets only its matching named value to `1`;
- changing selection returns the previous contact to `0`;
- all nine behavioural tests pass;
- SW remains unwired and has no reported input.

If a pair responds to a different physical button, stop and amend the pair
assignment from the observed result rather than moving GPIO definitions.

On the pictured ESP32 board, GPIO16 and GPIO17 are printed as RX2 and TX2;
GPIO18 and GPIO23 are printed as D18 and D23. Keep GPIO16/17/18/23 labelled
proposed until these checks pass.

### 7.3 Remaining commissioning

- Calibrating dial brightness
- Verifying the on/off control
