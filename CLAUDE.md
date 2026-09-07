# CLAUDE.md

Context for AI-assisted development in this repository. Read this first.

## What this is
ESP32 firmware + hardware/mechanical design for a restored 1960s Decca music
centre. See `README.md` for the full overview and `docs/Firmware Architecture.md`
for the design that governs all firmware changes.

## Start here

Read `docs/Development Handover.md` and `docs/Open Issues.md` before changing
firmware. They record the current physical evidence and open work.

## Build / test
- Build: `pio run`
- Upload: `pio run --target upload`
- Monitor: `pio device monitor`
- Test: `pio test`
- Debug build: `pio run -e esp32dev-debug`
- Windows fallback when `pio` is not on PATH:
  `$pio = "$env:USERPROFILE\\.platformio\\penv\\Scripts\\platformio.exe"`,
  then invoke commands as `& $pio run ...`.

## Source layout
- `src/` — firmware modules + `main.cpp` (entry point / scheduler)
- `lib/` — future extracted, self-contained modules
- `test/` — PlatformIO unit tests
- `docs/` — architecture, wiring, build, parts, revisions
- `hardware/`, `mechanical/`, `assets/` — design and media

## Invariants (do not break)
1. **Modules are independent.** No module calls another module. Input modules
   (`buttons`, `pots`) never call output modules (`display`, `lighting`).
2. **Coordinate in `main`; share state via `settings`.** No lateral coupling.
3. **Depend downward only.** Modules may use `hardware` and `settings`; those
   two depend on nothing.
4. **Non-blocking.** No `delay()` in `loop()`/`update()`; use `millis()` timing.
5. **The header is the contract.** Keep public interfaces stable and documented.
6. **Persist only through `settings`** (NVS). No direct NVS writes elsewhere.
7. **Version once.** Update `src/version.h` for every firmware release; the
   startup screen and serial boot report consume that same value.

## Working style
- Edit one module at a time; keep its header stable.
- Match the conventions in `CONTRIBUTING.md` (C++17, naming, commit style).
- When changing pins/parts, update `src/hardware.h`, `docs/Wiring.md`, the BOM,
  and `docs/Revision History.md` in the same change.
- Follow Conventional Commits (see `CONTRIBUTING.md`).

## Status

Phase 1 module implementation is in progress. `hardware`, `settings`, `pots`,
`buttons`, `lighting`, `display`, `power` and authenticated `ota` exist. Pot
GPIO32–35, sole VHF source input GPIO23 and OLED GPIO21/22 are physically
verified. On/off GPIO19 and lighting PWM GPIO25 retain prior physical evidence;
firmware v0.28.0 reassigns them to physically verified GPIO26 and GPIO18
respectively. DFRobot DFR0457 is
installed as the final MOSFET stage;
its initial steady-light test resolved the flicker. Firmware uses 1 kHz PWM and
85% / duty 217. That image was uploaded successfully by authenticated OTA and
returned at `decca.local`. The owner physically approved the v0.27.1
startup/version timing and both approximately 4.34-second fade directions, with
no flicker reported. WAGO distribution installation plus pot-stability,
temperature and current checks remain open under HW-LGT-01. Mono and logical
standby are off.

Stereo/Mono is assigned to TX2/GPIO17 with the internal pull-up. The contact is
closed/LOW in Mono and open/HIGH in Stereo; Stereo requests lights on and Mono
requests lights off. Both input positions are physically accepted. The previous
GPIO25 assignment and lamp bank passed safe-off and smooth-fade testing through
full duty; GPIO18 is the new unverified output. The current production target
remains 85% / duty 217.

Source selection follows ADR-0013: closed/latched VHF = Digital Streamer;
every other selector position = Vinyl. GPIO16/17/18 remain released from the
source selector and the sole source input remains GPIO23; GPIO17 is separately
allocated to Stereo/Mono under ADR-0014 and GPIO18 is allocated to dial-light
PWM.

The production `main.cpp` coordinates power, pots, VHF source, display,
Stereo/Mono lighting and OTA in one non-blocking loop. USB-to-OTA is physically
accepted. Automatic rollback after a fully received but boot-invalid image
remains Phase 3.

The final H4 OLED loom is Brown GND, Red 3V3/VCC, Orange SCL GPIO22 and Yellow
SDA GPIO21. Rev Q bezel PR #7 is merged, complete and owner-approved.

GitHub `main` remains unchanged; the current feature source is
`feature/reassign-control-gpios`. The ESP32's last-known installed image is
firmware v0.28.0 from commit `283d40a`: authenticated OTA succeeded, the device
returned at `decca.local`, and the owner confirmed the D26/D18 wiring works
correctly. Its version hold is 2.2 seconds and the
0–85% lighting transition is approximately 4.34 seconds in either direction.
Complete the remaining HW-LGT-01 WAGO installation, pot-stability, temperature
and current checks.
