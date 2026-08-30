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
└── test_lighting/          PWM safe-off, target and fade behaviour
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
five-frame startup animation, standby/local dashboards, mapped function and
source identity retained in state but omitted from the user-facing layout,
copied now-playing metadata and fallback, all four control values, two-second
control overlays, function confirmation, change-only refresh, diagnostics,
SW-unavailable presentation and safe initialisation failure. It also performs a
real SH1106 address/frame snapshot for H4 bench verification and covers the
persistent 180-degree fitted-aperture calibration frame. Keeping one suite
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

Display-calibration increment (2026-08-30): the release build passed and the
expanded `test_display` suite passed 11/11 on the physical SH1106. The production
safe-bootstrap image was then installed with the 180-degree, 8-pixel calibration
pattern active; OTA readiness remained available. Final visible-boundary photo
analysis is pending and is not yet a layout-acceptance claim.
