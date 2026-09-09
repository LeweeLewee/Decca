# Open Issues

This is the canonical short list of unresolved integration issues. Read it with
`docs/Development Handover.md` before continuing work. Historical test passes in
the revision history remain valid records of what was tested at the time, but do
not close a later issue listed here.

## HW-GPIO-01 — Verify final controller-side GPIO routing

**Status:** COMPLETE — owner testing on 2026-09-08 confirmed the final routing
and firmware logic: on/off GPIO14/D14, VHF GPIO26/D26, Stereo/Mono GPIO25/D25
and DFR0457 lighting PWM GPIO18/D18.

Firmware v0.27.3 at commit `0a4d3bd` was built for `esp32dev-ota`, uploaded by
authenticated OTA and returned at `decca.local` / `192.168.1.79`. The owner
confirmed the v0.27.3 startup screen, correct ON/STANDBY operation on GPIO14,
the VHF route on GPIO26, GPIO25 Stereo/Mono input logic, and D18 lighting output.
The retained Stereo/Mono switch itself is faulty and is tracked separately as
HW-SW-01; that mechanical/contact fault does not reopen the firmware pin map.

## HW-SW-01 — Repair retained Stereo/Mono switch

**Status:** OPEN — GPIO25/D25 input logic is correct, but the retained physical
switch does not currently produce the required closed/LOW Mono state.

**Observed (2026-09-08):** with v0.27.3 running and the unit logically ON, the
lamps reached fully on after the Stereo/open command. After moving the physical
control to Mono and waiting ten seconds, the lamps remained fully on. The owner
identified the retained switch as the fault and confirmed the firmware logic is
correct.

**Acceptance required:**

1. Repair or replace the isolated Stereo/Mono contact without connecting 3.3 V
   or 5 V to GPIO25.
2. Confirm Stereo is open/HIGH and requests lights on.
3. Confirm Mono is closed/LOW and requests lights off.
4. Confirm both transitions while logical power is ON, then record the result.

## HW-LGT-01 — Final dial-lighting integration acceptance

**Status:** OPEN — DFR0457 installed and steady-state flicker resolved. The
previous fade behavior is superseded because installed testing showed a delayed
final switch rather than a useful visible ramp. Immediate v0.27.4 behavior,
WAGO installation, pot-stability, temperature and current remain to be verified.

**Observed:** the previous MOSFET/module path produced visible lamp flicker. With
that path energised, electrical disturbance also caused the display to jump
between pot overlays. The pot behaviour settled after the lighting path was
turned off and discharged. Driving the three lamps directly from the same 5 V
supply produced no visible flicker, isolating the fault to the switching path
rather than the lamps or supply. At a temporary 100% firmware target the pot/UI
disturbance stopped, but lamp flicker remained.

**Selected remedy and current progress:**

- **Complete:** install one DFRobot Gravity MOSFET Power Controller,
  **DFR0457**. The owner reports that the lighting flicker is resolved.
- **Ordered:** Pi Hut pack of three **WAGO 221-415** five-way lever connectors.
  On delivery, use one for the +5 V star point, one for common GND and retain
  one spare.
- Keep the single regulated 5 V supply and common-ground architecture.
- **Complete:** set `decca::hardware::kDialLightingPwmFrequencyHz` to the
  controller's specified 1 kHz limit and restore the existing non-blocking soft
  fade engine. Commit `c6cb9a6` uploaded by authenticated OTA and the ESP32
  returned at `decca.local` after reboot.
- **Complete (2026-09-05):** deploy v0.27.1 at commit `d0b1d3c`. The owner
  approved the 2.2-second firmware-version hold and both approximately
  4.34-second lighting fades, with no flicker reported.

**Locked behaviour:** GPIO18/D18 is the lighting PWM output. After debounce,
Stereo open/high applies the owner-approved 85% / duty 217 immediately and Mono
closed/low applies duty 0 immediately. Logical power transitions are also
immediate. Preserve safe-off boot.

**Pending physical acceptance:** v0.27.4 removes the fade engine and makes every
lighting transition immediate. The release and credential-enabled OTA builds
pass, all eight on-target suites compile without upload or execution,
authenticated OTA succeeded and the device returned on the network. Physical
transition verification remains pending.

**Device state:** the installed image is firmware v0.27.4 built from commit
`19c16b6`, using GPIO18 PWM at 1 kHz and an 85% / duty 217 target. Its
authenticated OTA upload succeeded in 57.956 seconds and the device returned at
`decca.local` / `192.168.1.79`.

**Acceptance required to close:**

1. **Passed:** cold startup showed no unwanted lamp flash before firmware control.
2. **Partial:** the D18 path reached fully on during the 2026-09-08 check. The
   Mono/off transition is blocked by the retained switch fault in HW-SW-01.
3. **Passed:** no lamp flicker was reported at steady state. The old fade result
   is superseded by the v0.27.4 immediate-switch requirement.
4. **Open:** install the ordered WAGO 221-415 +5 V and common-GND star points.
5. **Open:** exercise and then release all four pots; confirm the OLED does not
   chatter between control overlays while the lamps are on.
6. **Open:** confirm no abnormal module or wiring temperature and measure the
   installed three-lamp current.
7. **Complete:** release v0.27.4 is installed by authenticated OTA and network
   return is confirmed. Close only after items 2 and 4–6 pass.

**Procurement records:** `hardware/BOM/phase1.csv` and `docs/Parts List.md`.
**Wiring:** `docs/Wiring.md`, H5 and Power Distribution.
