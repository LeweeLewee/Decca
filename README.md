# decca

Custom ESP32 firmware and hardware integration for a restored 1960s Decca music centre.

---

## Project Overview

**decca** brings a 1960s Decca radiogram / music centre back into daily use without
gutting its character. The original cabinet, controls, and dial are preserved and
restored, while the internals are re-engineered around a modern ESP32 microcontroller
that drives the front-panel controls, lighting, and (in later phases) a networked
audio streamer.

The goal is a piece that looks and feels period-correct but behaves like a modern,
maintainable, network-connected audio appliance. The original knobs, switches, and
dial illumination are reused as the primary interface; the ESP32 reads them, drives an
OLED display hidden behind the dial glass, controls cabinet and dial lighting, and
eventually talks to a WiiM Pro streamer over its local HTTP API.

This repository holds **only the firmware, hardware design, mechanical design, and
documentation**. It is structured to be maintained over years, not weekends.

---

## Goals

- **Preserve the original.** Reuse the cabinet, controls, and dial; no irreversible
  modifications where avoidable.
- **Modern internals.** ESP32-based control system with clean, testable firmware.
- **Local-first control.** The music centre must be fully usable from its own front
  panel with no phone, app, or network dependency.
- **Networked audio.** Integrate a WiiM Pro streamer for source selection, volume, and
  now-playing metadata.
- **Maintainability.** Modular firmware, documented hardware, and reproducible builds so
  the project can be picked up cold months later.
- **Professional discipline.** Treat a personal restoration to the same engineering
  standard as a production embedded product.

---

## Current Architecture

The system is organised as a set of **independent firmware modules** coordinated by
`main.cpp`. Each module owns one responsibility and exposes a small, explicit interface.
Modules do not reach into each other's internals; shared state flows through `settings`
and the top-level application loop.

```
                       ┌─────────────────────────────┐
                       │           main.cpp          │
                       │   (init, scheduler, glue)   │
                       └──────────────┬──────────────┘
                                      │
        ┌───────────────┬─────────────┼─────────────┬───────────────┐
        │               │             │             │               │
   ┌────┴────┐    ┌─────┴────┐   ┌────┴────┐   ┌────┴─────┐   ┌──────┴─────┐
   │ buttons │    │   pots   │   │ display │   │ lighting │   │  settings  │
   └────┬────┘    └─────┬────┘   └────┬────┘   └────┬─────┘   └──────┬─────┘
        │               │             │             │               │
        └───────────────┴─────────────┴─────────────┴───────────────┘
                                      │
                              ┌───────┴────────┐
                              │    hardware    │
                              │ (pins, board   │
                              │  abstraction)  │
                              └────────────────┘
```

- **hardware** — single source of truth for pin assignments and board-level setup.
- **buttons / pots** — debounced, filtered input from the front-panel controls.
- **display** — OLED rendering behind the dial glass.
- **lighting** — dial and cabinet illumination (PWM, effects, standby dimming).
- **settings** — persisted configuration and runtime state (NVS-backed).
- **WiiM interface** *(Phase 2)* — network control of the WiiM Pro streamer.

See [`docs/Firmware Architecture.md`](docs/Firmware%20Architecture.md) for the full design.

---

## Hardware Overview

| Element            | Role                                                                 |
|--------------------|----------------------------------------------------------------------|
| ESP32 DevKit       | Main controller (dual-core, Wi-Fi, PWM, ADC).                        |
| OLED display       | Small SPI/I²C OLED mounted behind the dial glass.                    |
| Front-panel buttons| Source / transport / power, read as debounced digital inputs.        |
| Potentiometers     | Volume / tone controls read via the ESP32 ADC.                       |
| Dial & cabinet LEDs| PWM-driven illumination replacing original lamps.                    |
| Power supply       | Regulated 5 V / 3.3 V rails feeding the ESP32 and peripherals.       |
| WiiM Pro *(Ph. 2)* | Networked audio streamer controlled over its local HTTP API.        |

Full electrical detail lives in [`docs/Hardware Architecture.md`](docs/Hardware%20Architecture.md),
[`docs/Wiring.md`](docs/Wiring.md), and the [`hardware/`](hardware/) tree.

---

## Development Philosophy

- **Modules stay independent.** Adding, replacing, or removing a peripheral should touch
  one module, not the whole codebase.
- **The front panel is the product.** Network features are additive; the device must
  never depend on a phone or cloud service to play music.
- **Document as you build.** Hardware revisions, wiring, and decisions are captured in
  `docs/` at the time they happen, not reconstructed later.
- **Small, explicit interfaces.** Prefer a handful of well-named functions over shared
  globals and hidden coupling.
- **Reproducible builds.** PlatformIO pins the toolchain and dependencies so a checkout
  builds identically on any machine.
- **Restore, don't replace.** Mechanical and electrical work respects the original piece.

---

## Repository Structure

```
decca/
├── src/                    Firmware source (modules + entry point)
├── lib/                    Self-contained libraries / future extracted modules
├── test/                   PlatformIO unit tests
├── docs/                   Build, hardware, firmware and wiring documentation
├── hardware/               Electrical design
│   ├── Schematics/         Circuit schematics
│   ├── PCB/                PCB layouts / fabrication files
│   ├── BOM/                Bills of materials
│   └── Wiring/             Harness and interconnect diagrams
├── mechanical/             Physical design
│   ├── CAD/                Source CAD (Fusion 360 etc.)
│   ├── STL/                Print-ready meshes
│   ├── Drawings/           Dimensioned drawings
│   └── Knob Adaptors/      Adaptors mating original knobs to modern shafts
├── assets/                 Project media
│   ├── Photos/             Build and reference photography
│   ├── Icons/              UI / display icons
│   └── Logos/              Branding
├── .github/                Issue and pull request templates
├── platformio.ini          Build configuration
├── CONTRIBUTING.md          Coding standards and workflow
├── LICENSE                  Licence (placeholder — see below)
└── README.md               This file
```

---

## Development Workflow

1. **Install [PlatformIO](https://platformio.org/)** (VS Code extension or the CLI).
2. **Clone** the repository and open the folder.
3. **Build:** `pio run`
4. **Upload:** `pio run --target upload`
5. **Serial monitor:** `pio device monitor`
6. **Run tests:** `pio test`

Work happens on feature branches and merges via pull request. Branch names, commit style,
and code conventions are defined in [`CONTRIBUTING.md`](CONTRIBUTING.md).

> **Working with Claude Code:** this repository is laid out so an AI assistant can navigate
> it without additional context. Module boundaries, responsibilities, and interfaces are
> documented in headers and in `docs/Firmware Architecture.md`. Prefer editing one module
> at a time and keeping interfaces stable.

---

## Build Phases

The project is delivered in three phases. Each phase is independently useful — the device
is fully functional at the end of Phase 1.

### Phase 1 — Local Control
- OLED display behind the dial glass
- Front-panel buttons
- Potentiometer inputs
- Dial and cabinet LED lighting
- Fully usable with no network

### Phase 2 — WiiM Pro Integration
- WiiM Pro HTTP API integration
- Source selection from the front panel
- Volume synchronisation between panel and streamer
- Now-playing metadata on the OLED

### Phase 3 — Advanced Features
- On-device configuration menus
- OTA (over-the-air) firmware updates
- Richer UI and display modes
- Additional legacy control features (e.g. reusing more original switches)

See [`docs/Firmware Architecture.md`](docs/Firmware%20Architecture.md) for how each phase
maps onto the module set.

---

## Future Roadmap

- **WiiM interface module** as a clean, testable network layer (Phase 2).
- **Configuration UI** driven by `settings` and rendered by `display` (Phase 3).
- **OTA update channel** with rollback safety (Phase 3).
- **Optional extras** under evaluation: presence/standby automation, multi-room grouping,
  additional analogue meters, or reinstating the original tuning dial as a soft control.

Roadmap items are tracked as GitHub issues and milestones.

---

## Contributing

This is a personal restoration project, but it is structured to accept contributions and
to be maintainable by others. Before opening a pull request, please read
[`CONTRIBUTING.md`](CONTRIBUTING.md), which covers the C++17 standard, naming conventions,
module responsibilities, documentation expectations, and commit message style.

Use the GitHub issue templates for bugs, features, and hardware issues, and the pull
request template when submitting changes.

---

## Licence

**Placeholder — licence to be confirmed.**

No licence has been finalised for this repository yet. Until a licence is chosen, all
rights are reserved by the author. See [`LICENSE`](LICENSE) for the current placeholder
text, which will be replaced once a licence is selected.
