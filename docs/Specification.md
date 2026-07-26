# decca — Project Specification

## Document Control

| Field    | Value                                             |
|----------|---------------------------------------------------|
| Project  | decca — ESP32 music centre restoration            |
| Status   | Draft (foundation stage — no firmware implemented) |
| Version  | 0.1                                               |
| Owner    | LeweeLewee                                        |
| Related  | `README.md`, `docs/Firmware Architecture.md`, `docs/Hardware Architecture.md`, `docs/Wiring.md` |

Requirements are identified as `FR-*` (functional), `NFR-*` (non-functional),
`HW-*` (hardware), and `IF-*` (interface). IDs are stable once assigned so they
can be referenced from issues, commits, and tests.

---

## 1. Purpose

Define what the decca system must do, the constraints it must respect, and the
criteria by which each build phase is judged complete. This specification is the
agreed scope against which design, implementation, and testing are measured.

## 2. Scope

decca converts a restored 1960s Decca music centre into a modern, network-capable
audio appliance while preserving the original cabinet, controls, and dial. The
system covers the ESP32 firmware, the supporting electronics, and the mechanical
integration. It does **not** cover the audio amplification path or speakers,
which remain analogue and outside the controller's responsibility except where a
networked source is introduced in Phase 2.

## 3. System Overview

An ESP32 reads the restored front-panel controls, drives an OLED behind the dial
glass and the dial/cabinet lighting, and persists user state. From Phase 2 it
also controls a WiiM Pro streamer over its local HTTP API. The firmware is built
from independent modules coordinated by a top-level scheduler, as defined in
`docs/Firmware Architecture.md`.

## 4. Definitions

| Term        | Meaning                                                        |
|-------------|----------------------------------------------------------------|
| Module      | A self-contained firmware unit with one responsibility         |
| Front panel | The original, restored physical controls of the music centre   |
| Streamer    | WiiM Pro networked audio source (Phase 2+)                      |
| NVS         | ESP32 non-volatile storage used for persisted settings         |
| Local-first | Full core function without any network or companion device     |

---

## 5. Functional Requirements

### 5.1 Core / System

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-SYS-01 | The system shall initialise all modules in dependency order at power-on.     | 1     |
| FR-SYS-02 | The system shall run a non-blocking main loop; no operation may stall it.    | 1     |
| FR-SYS-03 | The system shall be fully operable from the front panel with no network.     | 1     |
| FR-SYS-04 | The system shall restore its last persisted state on boot.                   | 1     |
| FR-SYS-05 | The system shall degrade gracefully if the streamer is unavailable.          | 2     |

### 5.2 Buttons

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-BTN-01 | The system shall read all front-panel buttons and debounce them.             | 1     |
| FR-BTN-02 | The system shall emit a discrete event per confirmed press.                  | 1     |
| FR-BTN-03 | Buttons shall control power/standby, source selection, and transport.        | 1     |

### 5.3 Potentiometers

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-POT-01 | The system shall read the volume and tone potentiometers.                    | 1     |
| FR-POT-02 | Pot readings shall be filtered so a settled knob yields a stable value.      | 1     |
| FR-POT-03 | Pot values shall be exposed on a normalised scale (0–1000).                  | 1     |

### 5.4 Display

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-DSP-01 | The system shall render an idle/now-playing screen on the OLED.              | 1     |
| FR-DSP-02 | The system shall show transient status for volume and source changes.        | 1     |
| FR-DSP-03 | The display shall show streamer metadata (title/artist/source) when present. | 2     |
| FR-DSP-04 | The display shall render configuration menus.                                | 3     |

### 5.5 Lighting

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-LGT-01 | The system shall drive dial and cabinet illumination via PWM.                | 1     |
| FR-LGT-02 | Lighting shall support brightness control and standby dimming.               | 1     |
| FR-LGT-03 | Lighting transitions shall fade rather than switch abruptly.                 | 1     |

### 5.6 Settings

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-SET-01 | The system shall persist user state (source, volume, brightness) to NVS.     | 1     |
| FR-SET-02 | Settings shall be the single point through which modules exchange state.     | 1     |
| FR-SET-03 | Persistence shall be write-limited to protect flash endurance.               | 1     |

### 5.7 Streamer Integration (WiiM)

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-WIM-01 | The system shall connect to the WiiM Pro over the local network.             | 2     |
| FR-WIM-02 | The system shall select the streamer source from the front panel.            | 2     |
| FR-WIM-03 | Front-panel volume and streamer volume shall be synchronised.                | 2     |
| FR-WIM-04 | The system shall retrieve and display now-playing metadata.                  | 2     |

### 5.8 Advanced (Phase 3)

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-ADV-01 | The system shall provide on-device configuration menus.                      | 3     |
| FR-ADV-02 | The system shall support OTA firmware updates with rollback safety.          | 3     |
| FR-ADV-03 | The system shall support reuse of additional original controls.             | 3     |

---

## 6. Non-Functional Requirements

| ID       | Requirement                                                                  |
|----------|-------------------------------------------------------------------------------|
| NFR-01   | Main loop responsiveness: a button press shall register within 50 ms.         |
| NFR-02   | The firmware shall use no dynamic allocation in the steady state.             |
| NFR-03   | Modules shall have no lateral coupling (see `docs/Firmware Architecture.md`). |
| NFR-04   | The codebase shall build with `pio run` with no errors or warnings.          |
| NFR-05   | Each module shall have a unit-test suite exercising its public interface.     |
| NFR-06   | Builds shall be reproducible via the pinned PlatformIO toolchain.            |
| NFR-07   | Public interfaces shall be documented in their headers.                      |
| NFR-08   | The device shall reach an operable state within 3 s of power-on (Phase 1).   |
| NFR-09   | Network features shall never block core local control.                       |
| NFR-10   | No secrets (Wi-Fi credentials, tokens) shall be committed to the repository. |

---

## 7. Hardware Requirements & Constraints

| ID     | Requirement                                                                    |
|--------|---------------------------------------------------------------------------------|
| HW-01  | Controller shall be an ESP32 DevKit (dual-core, Wi-Fi, ≥ 4 MB flash).           |
| HW-02  | **All potentiometers shall be wired to ADC1 pins (GPIO 32–39).** ADC2 is unavailable while Wi-Fi is active and must not be used for analogue inputs. |
| HW-03  | Buttons and any pin driven at reset shall avoid ESP32 strapping pins (0, 2, 5, 12, 15). |
| HW-04  | Input-only pins (GPIO 34–39) shall be used only for inputs and require external pull-ups where needed. |
| HW-05  | Lighting outputs shall use LEDC (hardware PWM) channels.                        |
| HW-06  | The pin map in `src/hardware.h` shall match `docs/Wiring.md` at all times.      |
| HW-07  | Power supply shall provide stable 5 V and 3.3 V rails sized to the load budget. |
| HW-08  | Original controls shall be preserved and reused; modifications shall be reversible where practical. |

---

## 8. External Interfaces

| ID     | Interface                                                                       |
|--------|---------------------------------------------------------------------------------|
| IF-01  | **Front panel:** buttons (digital, debounced) and potentiometers (ADC1).        |
| IF-02  | **Display:** OLED over I²C (or SPI), mounted behind the dial glass.             |
| IF-03  | **Lighting:** PWM-driven LED zones (dial, cabinet).                             |
| IF-04  | **WiiM Pro HTTP API (Phase 2):** local-network HTTP control for source, volume, and metadata. Endpoint and command set to be documented in `docs/Hardware Architecture.md` / a dedicated interface note when implemented. |
| IF-05  | **Serial console:** 115200 baud for diagnostics and bring-up.                   |

---

## 9. Constraints & Assumptions

- The original cabinet, dial, and controls are available and restorable.
- The WiiM Pro exposes a stable local HTTP API on the same LAN as the ESP32.
- Wi-Fi credentials are provisioned locally and never committed (see NFR-10).
- The amplifier and speaker path remain analogue and outside firmware control.
- One ESP32 handles all responsibilities; no secondary microcontroller is assumed.

## 10. Out of Scope

- Audio DSP, equalisation, or amplification within the firmware.
- Cloud services, remote/off-LAN control, or mobile applications.
- Multi-unit / multi-room orchestration (may be revisited post-Phase 3).

---

## 11. Acceptance Criteria

### Phase 1 — Local Control
- FR-SYS-01..04, all FR-BTN, FR-POT, FR-DSP-01/02, FR-LGT, FR-SET satisfied.
- Device is fully usable with no network connected.
- All Phase 1 module test suites pass (`pio test`).
- Build is clean per NFR-04.

### Phase 2 — WiiM Integration
- FR-WIM-01..04 and FR-DSP-03 satisfied.
- Source selection, volume sync, and metadata verified against a live WiiM Pro.
- Loss of the streamer does not impair local control (FR-SYS-05, NFR-09).

### Phase 3 — Advanced Features
- FR-ADV-01..03 and FR-DSP-04 satisfied.
- OTA update demonstrated with a successful rollback.

---

## 12. Traceability

- **Requirements → design:** `docs/Firmware Architecture.md` (modules, phase map).
- **Requirements → hardware:** `docs/Hardware Architecture.md`, `docs/Wiring.md`.
- **Requirements → verification:** test suites under `test/`, one per module.
- **Change history:** `docs/Revision History.md`.

Requirement IDs should be cited in commit messages and pull requests when work
implements or verifies them (e.g. `feat(pots): filtered ADC reads [FR-POT-02]`).
