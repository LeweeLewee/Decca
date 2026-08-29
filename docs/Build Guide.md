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

## 5. Firmware Flashing and OTA Bootstrap

Complete both tests before mounting the ESP32 where USB access is difficult.

1. Create the private configuration:
   ```powershell
   Copy-Item src\secrets.example.h src\secrets.h
   ```
2. Replace the placeholders with the Wi-Fi details and a long unique OTA
   password. Never commit `src/secrets.h`; it is gitignored.
3. Flash once by USB:
   ```powershell
   pio run -e esp32dev -t upload --upload-port COM_PORT
   ```
4. Run `pio device monitor -b 115200` and wait for `[OTA] ready`.
5. Set the same password for PlatformIO:
   ```powershell
   $env:DECCA_OTA_PASSWORD = "YOUR_SAME_OTA_PASSWORD"
   ```
6. Prove a wireless upload:
   ```powershell
   pio run -e esp32dev-ota -t upload
   ```
   If mDNS fails, add `--upload-port 192.168.x.x` using the displayed IP.

The computer and Decca must be on the same local network. Guest-network
isolation or a VPN may block OTA. Do not expose the OTA service to the internet.

The dual application slots protect against interrupted or rejected transfers.
Automatic rollback after a fully received image fails to boot remains a Phase 3
hardening item, so retain recovery access until it is implemented.

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
   centre wiper to its ADC1 pin (White), and right lug to 3.3 V (Red). On the
   30-pin ESP32 DevKit used in this build, the terminal adapter exposes the same
   printed labels as the board. Use the **printed board label** shown below when
   locating each ADC terminal:

   | Control | Bench-verified GPIO | Printed board label |
   |---------|---------------------|---------------------|
   | Volume  | GPIO32              | **D32**             |
   | Bass    | GPIO33              | **D33**             |
   | Treble  | GPIO34              | **D34**             |
   | Balance | GPIO35              | **D35**             |

   Therefore the four White wiper wires connect to **D32, D33, D34 and D35**
   respectively. The Red wires go to 3V3 and the Brown wires go to GND.
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

| Control | GPIO | Board label | Anticlockwise | Approx. centre | Clockwise | Direction |
|---------|------|-------------|---------------|----------------|-----------|-----------|
| Volume  | 32   | D32         | 0             | 2047           | 4095      | Increasing clockwise |
| Bass    | 33   | D33         | 0             | 2047           | 4095      | Increasing clockwise |
| Treble  | 34   | D34         | 0             | 2047           | 4095      | Increasing clockwise |
| Balance | 35   | D35         | 0             | 2047           | 4095      | Increasing clockwise |

All six `test_pots` cases passed. Midpoint variation is expected because the
controls have no centre detent. The default 0–4095 calibration is retained with
no inversion.

### 7.2 Gram two-state source verification

Only the verified right-hand Gram Green/Yellow pair is used. Keep the Decca
disconnected from mains and power only the ESP32 by USB.

1. Connect one conductor of the right-hand Gram pair to GPIO23 / board label
   D23 and the other to GND. Current termination is Green → GPIO23 and
   Yellow → GND; the dry-contact pair may be swapped.
2. Leave VHF, SW, MW and LW conductors disconnected and individually insulated.
   Do not connect them to GPIO16, GPIO17 or GPIO18.
3. Run:

   ```powershell
   pio test -e esp32dev -f test_buttons
   ```

4. With Gram latched, expect:

   ```text
   BUTTON_SNAPSHOT pressed onoff=<0-or-1> gram=1 source=vinyl
   ```

5. Press any other fascia source button to release Gram and rerun. Expect
   `gram=0 source=digital`.

Pass criteria:

- Gram closed reports Vinyl;
- Gram open reports Digital Streamer;
- all nine behavioural tests pass;
- VHF, SW, MW and LW have no individual reported input.

The former LW solder repair is no longer required. If the Gram contact itself
later becomes unreliable, the deferred fallback is a purpose-built replacement
button panel.

### 7.3 OLED bench verification

This procedure passed on 2026-08-25, confirming GPIO21 and GPIO22. Keep it as
the commissioning method after any display, harness or controller replacement.
Keep the Decca disconnected from mains and power only the ESP32 by USB.

1. Read the labels printed beside the delivered OLED header. Do not infer its
   physical pin order from another module or online photograph.
2. Connect the purchased Pi Hut SH1106 panel:
   - OLED GND → ESP32 GND (Brown);
   - OLED VCC → ESP32 3V3 (Red), never 5 V for this build;
   - OLED SDA → GPIO21 / board label D21 (Orange);
   - OLED SCL → GPIO22 / board label D22 (Yellow).

   H4 is a documented colour-standard exception: its Orange conductor is SDA,
   not 5 V. Never connect that Orange wire to the 5 V rail.
3. In the PlatformIO terminal run:

   ```powershell
   git pull origin main
   pio test -e esp32dev -f test_display
   ```

4. Confirm the OLED reveals the `DECCA` wordmark from left to right over roughly
   1 s, then shows `VINYL` prominently without a legacy button label and a local
   dashboard with Volume 75% and the other three controls at 50%.
5. Confirm the output contains:

   ```text
   DISPLAY_SNAPSHOT controller=SH1106 address=0x3C ready=1
   ```

Pass criteria:

- the panel is detected at 0x3C;
- all five startup frames and the dashboard are upright, complete and not
  offset;
- white pixels are clear with no persistent noise or clipped columns;
- all ten display tests pass.

Recorded result (2026-08-25): the purchased SH1106 panel was detected at 0x3C,
all ten `test_display` cases passed, and the animated startup and revised
dashboard were upright, complete, unclipped and free of persistent display
artefacts. GPIO21 (SDA) and GPIO22 (SCL) are bench-verified.

If the panel is blank, disconnect USB before checking VCC/GND order and the
SDA/SCL labels.

### 7.4 Dial-lighting bench verification

GPIO25 remains proposed until this procedure passes. Keep the Decca disconnected
from mains. Use only the isolated low-voltage 5 V lighting supply and USB power
for the ESP32.

1. Check the MOSFET stage before applying power:
   - GPIO25 / board label D25 connects only to the logic-level N-channel MOSFET gate;
   - the MOSFET source connects to GND;
   - the dial-light negative lead connects to the MOSFET drain;
   - the dial-light positive lead connects to 5 V;
   - the ESP32 and 5 V lighting supply share GND.
2. Confirm there is no direct connection from the dial-light load to GPIO25 and
   no connection to the Decca mains wiring.
3. Connect the ESP32 by USB and run:

   ```powershell
   pio test -e esp32dev -f test_lighting
   ```

4. Observe the dial lighting. It should fade gently from off to a low test duty
   and back to off, without flashing at full brightness.
5. Confirm the output contains `LIGHTING_SNAPSHOT duty=32` and all seven tests
   pass.

Pass criteria:

- the light starts and finishes fully off;
- brightness changes smoothly in both directions;
- no full-brightness flash occurs at reset or test start;
- the MOSFET and wiring remain cool;
- all seven behavioural tests pass.

### 7.5 Remaining commissioning

- Selecting the final normal and standby dial brightness
- Verifying the on/off control
