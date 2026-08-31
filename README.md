# Decca music-centre restoration

ESP32 firmware, hardware and mechanical design for restoring a 1960s Decca
music centre while preserving its original controls and appearance.

The ESP32 provides control and user interface only. Audio remains outside it:
the locked Phase 2 path is **WiiM Pro → Fosi Audio ZA3 → passive speakers**.

## Current state

- Safe board initialisation and authenticated local-network OTA are implemented.
- Four analogue controls and the SH1106 OLED are bench-verified.
- The reliable VHF contact is the sole source input:
  VHF latched = Digital Streamer; every other selector position = Vinyl.
- TX2/GPIO17 is assigned to the Stereo/Mono contact as a lighting request:
  Stereo open = lights on; Mono closed = lights off. Both positions are physically verified.
- The display, buttons, pots, settings, lighting and logical power modules are
  implemented and independently tested.
- Production coordinates power, all four pots, the VHF-derived source state and
  the accepted OLED views, and 90% Stereo/off Mono dial lighting while
  continuously servicing authenticated OTA.
- USB-to-OTA, GPIO19 power, controls, source selection, fitted display and
  GPIO25/MOSFET/lamp electrical acceptance are complete. Normal Stereo lighting
  is locked at 90%; Mono and logical standby are off.

Read [Development Handover](docs/Development%20Handover.md) before continuing
firmware work.

## Locked controller map

| Function | ESP32 | Status |
|---|---:|---|
| Volume | GPIO32/D32 | Bench-verified |
| Bass | GPIO33/D33 | Bench-verified |
| Treble | GPIO34/D34 | Bench-verified |
| Balance | GPIO35/D35 | Bench-verified |
| VHF source contact | GPIO23/D23 | Physically accepted |
| OLED SDA | GPIO21/D21 | Bench-verified |
| OLED SCL | GPIO22/D22 | Bench-verified |
| On/off | GPIO19/D19 | Bench-verified |
| Stereo/Mono lighting request | GPIO17/TX2 | Physically accepted |
| Dial lighting PWM | GPIO25/D25 | Physically accepted with MOSFET/lamp bank |

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
- `src/`: firmware modules
- `test/`: PlatformIO suites
- `hardware/`: BOM, wiring and electrical design
- `mechanical/`: CAD, drawings and print files

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
