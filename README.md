# Decca music-centre restoration

ESP32 firmware, hardware and mechanical design for restoring a 1960s Decca
music centre while preserving its original controls and appearance.

The ESP32 provides control and user interface only. Audio remains outside it:
the locked Phase 2 path is **WiiM Pro → Fosi Audio ZA3 → passive speakers**.

## Current state

- Installed firmware is **v0.28.0** from source commit `d06e357`, deployed by
  authenticated OTA. WiiM-only source, metadata, volume, standby/resume and
  network-recovery acceptance passed; audio, channel, noise and trigger gates
  remain deferred until the ZA3 is connected.
- Safe board initialisation and authenticated local-network OTA are implemented.
- Four analogue controls and the SH1106 OLED are bench-verified.
- The reliable VHF contact is the sole source input:
  VHF latched = Digital Streamer; every other selector position = Vinyl.
- GPIO25/D25 is assigned to the Stereo/Mono contact as a lighting request:
  Stereo open = lights on immediately; Mono closed = lights off immediately
  after the 25 ms debounce. Firmware logic is correct,
  but the retained physical switch is faulty and remains open as HW-SW-01.
- The display, buttons, pots, settings, lighting and logical power modules are
  implemented and independently tested.
- The Phase 2 WiiM module is implemented as a background HTTPS worker for source,
  direct absolute volume over a reusable connection, power-state and metadata
  coordination. Live source,
  volume, active TIDAL metadata, logical-power and outage-recovery checks pass.
- Production coordinates power, all four pots, the VHF-derived source state and
  the accepted OLED views, and 85% Stereo/off Mono dial lighting while
  continuously servicing authenticated OTA.
- USB-to-OTA, GPIO14 power, GPIO26 VHF source selection and the fitted display
  are complete. The DFR0457 replacement stage is installed and its initial
  steady-light test resolved the flicker. Firmware v0.28.0 retains immediate
  lighting transitions. Physical transition verification after HW-SW-01, WAGO
  distribution, pot stability, temperature and current remain open as
  HW-LGT-01. Normal Stereo lighting is 85%; Mono and logical standby request off.
- v0.27.4 removes the fade engine: Stereo/Mono and logical power changes now
  apply the required LED duty immediately.
- ESP32 controller housing Rev C was printed, fitted, wired and installed as a
  prototype on 2026-09-07. Its CAD/mesh gates pass; seven prototype and two
  installation gates remain before production release.
- IEC C14 mounting plate Rev B is the active corrected-profile design. Its
  15/15 CAD checks pass and the owner confirmed the profile drawing; physical
  fit remains pending. Rev A is rejected.
- The completed 2026-09-06 ADC/PWM noise report and its 12,000-row raw capture
  are retained under `diagnostics/` as historical v0.27.1 evidence.

Read [Development Handover](docs/Development%20Handover.md) before continuing
firmware work, then check [Open Issues](docs/Open%20Issues.md).

## Locked controller map

| Function | ESP32 | Status |
|---|---:|---|
| Volume | GPIO32/D32 | Bench-verified |
| Bass | GPIO33/D33 | Bench-verified |
| Treble | GPIO34/D34 | Bench-verified |
| Balance | GPIO35/D35 | Bench-verified |
| VHF source contact | GPIO26/D26 | Physically verified |
| OLED SDA | GPIO21/D21 | Bench-verified |
| OLED SCL | GPIO22/D22 | Bench-verified |
| On/off | GPIO14/D14 | Physically verified |
| Stereo/Mono lighting request | GPIO25/D25 | Firmware logic verified; physical switch fault open under HW-SW-01 |
| Dial lighting PWM | GPIO18/D18 | DFR0457 installed and operating; final checks open under HW-LGT-01 |

Final OLED loom: Brown GND, Red 3V3/VCC, Orange SCL and Yellow SDA.

## Repository guide

- [Specification](docs/Specification.md)
- [Firmware architecture](docs/Firmware%20Architecture.md)
- [Hardware architecture](docs/Hardware%20Architecture.md)
- [Authoritative wiring](docs/Wiring.md)
- [Build and commissioning guide](docs/Build%20Guide.md)
- [Parts list](docs/Parts%20List.md)
- [Decision records](docs/adr/)
- [Development handover](docs/Development%20Handover.md)
- [Open issues](docs/Open%20Issues.md)
- [Branch disposition register](docs/Branch%20Disposition.md)
- `src/`: firmware modules
- `test/`: PlatformIO suites
- `hardware/`: BOM, wiring and electrical design
- `mechanical/`: CAD, drawings and print files
- `diagnostics/`: completed diagnostic evidence; not production firmware

## Windows build tools

If `pio` is not recognised in PowerShell, use the executable installed by the
PlatformIO VS Code extension:

```powershell
$pio = "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe"
& $pio --version
& $pio run -e esp32dev
& $pio test -e esp32dev
```

The first OTA bootstrap and commissioning procedure is in the
[Build Guide](docs/Build%20Guide.md). Never commit `src/secrets.h`.

## Engineering rules

Firmware modules remain independent and are coordinated in `main.cpp`. Update
paths must be non-blocking, persisted state belongs in `settings`, and hardware
changes must be reconciled across the pin map, wiring, BOM and revision history.

See [CONTRIBUTING.md](CONTRIBUTING.md) for code and commit conventions.
