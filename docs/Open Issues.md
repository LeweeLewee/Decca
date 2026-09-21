# Open Issues

This is the canonical short list of unresolved integration issues. Read it with
`docs/Development Handover.md` before continuing work. Historical test passes in
the revision history remain valid records of what was tested at the time, but do
not close a later issue listed here.

## FW-WIFI-01 — Investigate Wi-Fi reliability / packet loss

**Status:** OPEN — retained after the owner-authorised v0.28.5 merge on
2026-09-21. The TX-power update is deployed; Wi-Fi reliability is not resolved.

**Observed:** authenticated OTA and subsequent discovery confirmed v0.28.5 at
`decca-esp32.local`, power saving disabled (`WIFI_PS_NONE`), and an effective
19.5 dBm TX ceiling despite the accepted 20 dBm request. Connection-time RSSI
was -48 dBm. Before-update numeric RSSI/TX readbacks were unavailable.
Post-update ping samples returned 28/30 and 26/30 replies: 6/60 lost (10%),
with latency up to 646 ms. The baseline was only four successful pings, so
these samples cannot establish improvement or regression. Fresh OTA discovery
remained available; serial boot/watchdog/power logs were unavailable remotely.

**Next diagnostics / acceptance:**

1. Correlate AP client retries, disconnect reasons and a longer simultaneous
   LAN latency observation; distinguish controller, AP and test-host effects.
2. If warranted, inspect antenna placement and interference. The -48 dBm
   snapshot alone does not establish weak signal as the cause.
3. Obtain boot/watchdog/power logs if resets or functional symptoms occur.
4. Record a sustained representative run with stable connectivity and no
   unexplained control/audio interruptions before closing this issue.

See `docs/Build Guide.md` for deployment evidence and telemetry limitations.

## HW-GPIO-01 — Verify final controller-side GPIO routing

**Status:** COMPLETE — owner testing on 2026-09-08 confirmed the final routing
and firmware logic: on/off GPIO14/D14, VHF GPIO26/D26, Stereo/Mono GPIO25/D25
and DFR0457 lighting PWM GPIO18/D18.

Firmware v0.27.3 at commit `0a4d3bd` was built for `esp32dev-ota`, uploaded by
authenticated OTA and returned at `decca.local` / its reserved address. The owner
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

**Device state:** the installed image is firmware v0.28.4 from source commit
`3195c95`. It retains GPIO18 PWM at 1 kHz and the 85% / duty 217 target.
Authenticated OTA and controller network return most recently passed on
2026-09-20.

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

**Status:** COMPLETE (owner confirmation 2026-09-21) — firmware v0.28.4 from source commit `3195c95` is installed by
authenticated OTA. Digital and vinyl audio, metadata, direct absolute
volume/app reflection, correct left/right channels, logical standby/resume,
source response, direct trigger and network recovery acceptance pass. The
controller now advertises the unique `decca-esp32` hostname. The owner confirmed all formal
noise/interference checks passed with no issues on 2026-09-21, closing Phase 2
physical acceptance. The owner approved PR #11 for review and explicitly authorised merge on 2026-09-21.

**WiiM Home configuration confirmed 2026-09-11:** analogue Line Out path,
Fixed Volume Output off, 2 Vrms line level, EQ off, Auto Headroom on, stereo,
balance centred and a temporary 70% commissioning volume limit.

**Acceptance required:**

1. **Passed:** captured live `getPlayerStatus` and `getMetaInfo` during active
   TIDAL playback; sanitised fixtures decode Jolene / Dolly Parton correctly.
2. **Passed:** final credential-enabled release built at 52,336 bytes RAM
   (16.0%) and 1,018,373 bytes flash (77.7%); the WiiM and display targets,
   including source-priority, retry-bypass, RSSI and standby-wake regressions,
   compiled successfully. These were compile-only hardware-target checks.
3. **Passed:** authenticated OTA installed v0.28.4 and the controller returned
   without USB intervention. Private configuration remained ignored/uncommitted.
4. **Passed:** VHF selected the Wi-Fi/digital path; released VHF selected Line-In;
   returning to VHF restored network control.
5. **Passed:** the Decca volume pot sends the mapped absolute 0–100 target to the
   WiiM over a reusable HTTPS connection. Exact 10%, 20% and 30% setpoints matched
   in WiiM Home; 20% to 30% completed in about 2.2 seconds total and the owner
   confirmed the final response was much more responsive. The rejected
   intermediate two-point slew had turned a ten-point move into five delayed
   steps and is not present in the installed build.
6. **Passed:** logical OFF stopped playback; ON restored the selected source and
   controls without restarting or reflashing the controller.
7. **Passed:** outage warning remained visible throughout the confirmed outage
   and cleared automatically after recovery. The controller has the unique
   `decca-esp32` hostname; the OLED now distinguishes `NO CONTROLLER WI-FI` from
   `WIIM NOT RESPONDING` and shows controller RSSI bars in the top-left header.
8. **Passed (2026-09-19):** TIDAL digital playback was clear through both B&W
   DM601 S3 speakers; an identifiable channel check confirmed correct left and
   right routing, and the owner reported that playback sounded excellent.
9. **Passed after correction `36d84d1`:** OFF stopped playback and the WiiM's
   30-second automatic standby removed the trigger, extinguishing the ZA3 power
   indicator. ON now sends a one-step downward volume wake pulse and immediately
   restores the requested value; the WiiM and ZA3 woke without app or physical
   volume interaction. The pulse never exceeds the selected volume except the
   silent 0-to-1 boundary needed to create activity.
10. **Passed (2026-09-20):** vinyl playback through WiiM Line-In was confirmed.
    An observed 30–60+ second source-selection regression was traced to forced
    TLS teardown plus retry scheduling; v0.28.4 restores connection reuse,
    prioritises physical source changes and reconciles WiiM Line-In state. The
    owner confirmed approximately one-second response after deployment.
11. **Passed (2026-09-20):** entering standby shows `DECCA STANDBY`, blanks after
    ten seconds and remains off. Passive RSSI/status updates no longer wake it.
12. **Passed (owner confirmation 2026-09-21):** all formal noise checks are
    complete, with no hum, buzz, clipping, switching thumps or OLED/control
    interference reported. This closes the final Phase 2 physical gate.

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
