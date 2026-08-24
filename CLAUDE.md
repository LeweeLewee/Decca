# CLAUDE.md

Context for AI-assisted development in this repository. Read this first.

## What this is
ESP32 firmware + hardware/mechanical design for a restored 1960s Decca music
centre. See `README.md` for the full overview and `docs/Firmware Architecture.md`
for the design that governs all firmware changes.

## Build / test
- Build: `pio run`
- Upload: `pio run --target upload`
- Monitor: `pio device monitor`
- Test: `pio test`
- Debug build: `pio run -e esp32dev-debug`

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

## Working style
- Edit one module at a time; keep its header stable.
- Match the conventions in `CONTRIBUTING.md` (C++17, naming, commit style).
- When changing pins/parts, update `src/hardware.h`, `docs/Wiring.md`, the BOM,
  and `docs/Revision History.md` in the same change.
- Follow Conventional Commits (see `CONTRIBUTING.md`).

## Status
Phase 1 hardware-layer work is in progress. The proposed pin map and confirmed
control contracts are reconciled, board initialisation is implemented for all
assigned pins, `settings` implements NVS persistence, and `pots` implements
filtered/calibrated four-channel ADC1 reads. `buttons` implements active-low,
25 ms debounced stable state and press events. `lighting` implements safe-off
PWM control and non-blocking dial fades. `display` implements SH1106 startup,
standby/dashboard, transient status and diagnostic rendering with change-only
refreshes. Pot GPIO32–35 and source-button GPIO16,
GPIO17 and GPIO23 are bench-verified; GPIO18 awaits an LW harness repair. The
on/off switch, lighting GPIO25, OLED GPIO21/22 and remaining assigned pins stay
proposed until their documented bench tests.
