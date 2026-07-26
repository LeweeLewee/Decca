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

The four GPIO assignments remain **proposed** until this procedure passes.
Keep the Decca disconnected from mains; power only the ESP32 and the low-voltage
pot harness by USB during this test.

1. With the harness disconnected, measure each 10 kΩ linear pot:
   - resistance between the two outside lugs should remain approximately 10 kΩ;
   - resistance from centre wiper to each outside lug should change smoothly
     and in opposite directions through the full travel.
2. Viewed from the rear of each installed pot, connect left lug to GND (Brown),
   centre wiper to its proposed ADC1 pin (White), and right lug to 3.3 V (Red):

   | Control | Proposed wiper pin |
   |---------|--------------------|
   | Volume  | GPIO32             |
   | Bass    | GPIO33             |
   | Treble  | GPIO34             |
   | Balance | GPIO35             |

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
ESP32 in any audio path. Do not relabel the proposed GPIOs as verified until the
channel-identity checks above pass.

### 7.2 Remaining commissioning

- Calibrating dial brightness
- Verifying source and on/off controls
