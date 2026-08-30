# test

On-target unit tests using [Unity](https://docs.platformio.org/en/latest/plus/unit-testing.html),
PlatformIO's default framework. One suite per module, exercising the public
interface declared in each module's header.

## Layout

```
test/
├── unity_runner.h          shared setup()/loop() runner (included by each suite)
├── test_hardware/          hardware::init()
├── test_settings/          state defaults + RAM/NVS round-trips
├── test_buttons/           active-low debounce, state + event queue
├── test_pots/              ADC mapping, smoothing, calibration + deadband
├── test_display/           SH1106 frames, timing, refresh + physical bring-up
├── test_lighting/          PWM safe-off, target and fade behaviour
├── test_power/             pure logical on/standby transitions
└── test_ota/               non-blocking authenticated OTA lifecycle
```

## Running

```
pio test                       # all suites
pio test -f test_settings      # a single suite
pio test -e esp32dev-debug     # against the debug build
```

These are **on-target** tests: they build for the ESP32 and run on a connected
board. `pio test` builds them without hardware, but running the suites needs a
board attached.

## How the build is wired

- `test_build_src = yes` (in `platformio.ini`) compiles the modules in `src/`
  alongside each test runner, so tests call the real module code.
- `main.cpp` is wrapped in `#ifndef PIO_UNIT_TESTING` so its `setup()`/`loop()`
  don't collide with the runner each suite provides via `unity_runner.h`.

## Status

Phase 1 is in progress. The settings suite exercises real NVS persistence using
a test-only namespace. The pots suite injects deterministic ADC samples to
exercise mapping, normalisation, smoothing, calibration, inversion and deadband.
The buttons suite injects digital levels to exercise active-low debounce, bounce
rejection, stable latching state, re-arming and fixed-queue ordering. The pots
and buttons suites also report physical snapshots through Unity for bench
verification. The lighting suite exercises a real low-duty fade for physical
bring-up and injects its clock and PWM writer for deterministic safe-off,
fade-up, fade-down, target-clamping and invalid-zone coverage. The display suite
injects its clock, panel initialiser and semantic frame writer to exercise the
five-frame startup animation, standby/source dashboards, persistent mapped
function identity,
copied now-playing metadata and fallback, all four control values, two-second
control overlays, function confirmation, change-only refresh, diagnostics,
SW-unavailable presentation and safe initialisation failure. It also performs a
real SH1106 address/frame snapshot for H4 bench verification and covers the
persistent 180-degree fitted-aperture calibration frame, inactivity dimming,
pixel-off sleep and activity wake. The power suite covers initial state and
one-shot transitions independently of GPIO ownership. Keeping one suite
per module reinforces the low-coupling design in
`docs/Firmware Architecture.md`.

## Future: native tests

Logic with no hardware dependency can move to a faster `native` environment
(no board required) once modules are decoupled from `Arduino.h` — for example
by testing extracted libraries under `lib/`. Not required for Phase 1.

## OTA suite

`pio test -e esp32dev -f test_ota` covers disabled operation, non-blocking connection, timed retry, service start/handling and Wi-Fi-loss recovery. Physical acceptance is one USB bootstrap flash followed by one authenticated wireless upload.

USB-to-OTA physical acceptance passed on 2026-08-30: the authenticated
`esp32dev-ota` upload succeeded and, after reboot, serial reported
`[OTA] ready at 192.168.1.79 (decca.local)`. Interrupted-transfer acceptance
remains a separate outstanding check.

Full on-target result (2026-08-30): the `esp32dev` release build passed cleanly
and all seven suites passed on the physical ESP32 — buttons 9/9, display 10/10,
hardware 3/3, lighting 7/7, OTA 5/5, pots 6/6 and settings 3/3 (43/43 total).
The production safe-bootstrap image was restored by USB after testing and serial
reconfirmed `[OTA] ready at 192.168.1.79 (decca.local)`.

Display-refinement increment (2026-08-30): the persistent 180-degree calibration
frame, calibrated viewport contract, safe content band and retained paused
metadata expanded `test_display` to 12/12. Physical photographs were used to
accept the final fitted-Perspex layouts, including the corner play/pause glyph.
The calibration frame remains available as a service diagnostic; production
startup returns to the accepted standby view while OTA remains continuously
serviced. The final release build passed and the complete physical run passed
45/45: buttons 9/9, display 12/12, hardware 3/3, lighting 7/7, OTA 5/5, pots 6/6
and settings 3/3. Production was restored by USB and serial reconfirmed
`[OTA] ready at 192.168.1.79 (decca.local)`.

Power/protection increment (2026-08-30): GPIO19 was physically accepted in both
positions and the production coordinator now maps the debounced switch to ON or
STANDBY display state. The OLED dims after 60 seconds, turns pixels off after
five minutes, and blanks standby after ten seconds; relevant activity wakes it.
The release build passed and all eight physical suites passed 52/52: buttons
9/9, display 14/14, hardware 3/3, lighting 7/7, OTA 5/5, pots 6/6, power 5/5 and
settings 3/3. Production was restored over COM3; serial reported
`[POWER] state=ON` and `[OTA] ready at 192.168.1.79 (decca.local)`.

Controls/source refinement (2026-08-30): production now samples all four pots
and the sole VHF state. VHF closed maps to Digital Streamer; VHF open maps to
Vinyl. The mapped source remains on the normal dashboard until metadata takes
priority. Control overlays use Volume 0–100%, Bass/Treble −50..0..+50 and
Balance L50..0..R50 with centred bars and monochrome icons; balance readings
that round to centre display plain `0`. Physical interaction and fitted-screen
appearance were accepted. The release build passed and all eight suites passed
53/53: buttons 9/9, display 15/15, hardware 3/3, lighting 7/7, OTA 5/5, pots 6/6,
power 5/5 and settings 3/3. Production was restored over COM3.

Stereo/Mono assignment (2026-08-30): TX2/GPIO17 is now included in the buttons
suite as a pulled-up lighting request. Stereo open/high maps to on; Mono
closed/low maps to off. The release firmware builds successfully (RAM 49,880 bytes / 15.2%; flash
836,337 bytes / 63.8%) and all eight test suites compile without uploading. The
expanded buttons suite passed 11/11 on target in both physical positions:
`stereo_mono_contact=0 lights=on` in Stereo and
`stereo_mono_contact=1 lights=off` in Mono.
The final release build passed and the complete physical run passed 55/55:
buttons 11/11, display 15/15, hardware 3/3, lighting 7/7, OTA 5/5, pots 6/6,
power 5/5 and settings 3/3.
