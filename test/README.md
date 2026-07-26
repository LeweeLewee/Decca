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
├── test_buttons/           idle event queue
├── test_pots/              value range
├── test_display/           interface smoke
└── test_lighting/          brightness interface
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
a test-only namespace; the remaining suites are interface / smoke tests pending
their module implementations. Each file notes how to grow it into a behavioural
test as the module gains logic. Keeping one suite per module reinforces the
low-coupling design in `docs/Firmware Architecture.md`.

## Future: native tests

Logic with no hardware dependency can move to a faster `native` environment
(no board required) once modules are decoupled from `Arduino.h` — for example
by testing extracted libraries under `lib/`. Not required for Phase 1.
