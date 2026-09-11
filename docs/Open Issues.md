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
- **Historical (superseded):** commit `c6cb9a6` set the controller's 1 kHz limit
  while retaining the then-current soft fade; v0.27.1 at `d0b1d3c` was deployed
  on 2026-09-05. Installed observation later showed the LEDs held brightness
  until the delayed final switch, so ADR-0017 and v0.27.4 removed that engine.

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

## FW-WIM-01 — Accept Phase 2 WiiM integration

**Status:** OPEN — WiiM Pro acquired and network verified. Live HTTPS
`getStatusEx` and idle `getPlayerStatus` passed on 2026-09-11. The idle player
reported mode -1, status none, volume 35 and mute off. `getMetaInfo` returned an
empty body while idle. Firmware v0.28.0 implements the integration but is not
yet built, deployed or physically accepted.

**Acceptance required:**

1. Capture `getPlayerStatus` and `getMetaInfo` while TIDAL Connect is actively
   playing; retain sanitised fixtures and confirm title/artist rendering.
2. Build the release and all nine suites from a trusted toolchain; do not accept
   the checksum-failed PlatformIO package download observed in the Work session.
3. Add `DECCA_WIIM_HOST` to local `src/secrets.h`, build the credential-enabled
   OTA target and deploy v0.28.0.
4. Verify VHF selects the Wi-Fi/digital path and every released-VHF position
   selects WiiM Line-In.
5. Verify the Decca volume pot controls WiiM 0–100 smoothly without command
   chatter, including safe start level and application reflection.
6. Verify logical OFF stops playback while local lights/display still obey their
   existing behaviour, and ON restores source/volume without hard-cycling WiiM.
7. Disconnect/reconnect the network and confirm local controls remain responsive,
   the unavailable message appears once, and control recovers automatically.
8. After the ZA3 arrives, verify RCA left/right audio and the direct WiiM-to-ZA3
   trigger wake/standby behaviour under ADR-0018.

## MECH-HSG-01 — Complete ESP32 housing prototype acceptance

**Status:** OPEN — Rev C was printed, fitted, wired and installed on 2026-09-07
and passed every geometric mesh check. The fitted prototype closed twelve gates,
but specification v1.7 still records seven prototype and two installation gates.

Close only against the exact remaining measurements/observations in
`mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md` and its Rev C
build report. Do not infer unmeasured dimensions from the successful fit.

## MECH-C14-01 — Physically validate IEC C14 mounting plate Rev B

**Status:** OPEN — Rev A is rejected. Rev B passes 15/15 CAD checks and the owner
confirmed the corrected six-sided profile drawing, but no physical Rev B fit is
recorded.

Before release or mains energisation, confirm the inlet enters without forcing,
both M3 inlet fixings and all four Decca M2 holes align, the plate clamps flat,
and rear terminal/wire clearance plus insulation and earthing are acceptable.
