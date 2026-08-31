# decca — Project Specification

## Document Control

| Field    | Value                                             |
|----------|---------------------------------------------------|
| Project  | decca — ESP32 music centre restoration            |
| Status   | Draft. USB-to-OTA, fitted-display, GPIO19 logical-power, four-pot UI, VHF source and TX2 Stereo/Mono acceptance are complete. GPIO25 is accepted, but final lighting-stage acceptance is reopened as HW-LGT-01 pending DFR0457 installation and <=1 kHz verification. Normal Stereo lighting remains 90%; Mono and standby are off. Eight on-target suites last passed 55/55. WiiM integration remains outstanding. |
| Version  | 0.26                                              |
| Owner    | LeweeLewee                                        |
| Related  | `README.md`, `docs/Development Handover.md`, `docs/Firmware Architecture.md`, `docs/Hardware Architecture.md`, `docs/Wiring.md`, `docs/adr/` |

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
glass and the warm dial illumination, and persists user state. The ESP32 handles
**control and user interface only and does not process or carry audio**. From
Phase 2 it also controls a WiiM Pro streamer over its local API. The firmware is
built from independent modules coordinated by a top-level scheduler, as defined
in `docs/Firmware Architecture.md`.

Confirmed Phase 1 front-panel controls:

- Four rotary controls as 10 kΩ position sensors: **Balance, Treble, Bass, Volume**.
- Retained original **on/off switch** (low-voltage logic input).
- Original **source button bank** retained mechanically. Only **VHF** provides a reliable electrical state: VHF latched = **Digital Streamer**; every other selector position = **Vinyl**.
- Original **Stereo/Mono** contact on TX2/GPIO17: Stereo open requests lights on; Mono closed requests lights off. Both positions are physically verified.
- **OLED** display and **warm dial illumination**.

See `docs/Wiring.md` and the ADRs in `docs/adr/` for the confirmed detail.

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
| FR-SYS-03 | Local hardware controls shall remain usable without a network; digital content and track selection are delegated to the WiiM app. | 1 |
| FR-SYS-04 | The system shall restore its last persisted state on boot.                   | 1     |
| FR-SYS-05 | The system shall degrade gracefully if the streamer is unavailable.          | 2     |

### 5.2 Buttons

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-BTN-01 | The system shall debounce the retained on/off switch and the sole VHF source contact. | 1 |
| FR-BTN-02 | The system shall expose the stable VHF state continuously and emit one event per confirmed press without hold repeats. | 1 |
| FR-BTN-03 | Closed/latched VHF shall select Digital Streamer; open/released VHF shall select Vinyl. | 1 |
| FR-BTN-04 | SW, MW, LW and Gram shall have no individual ESP32 input; their authoritative effect is to release VHF and select Vinyl through the original interlock. A replacement button panel is a deferred fallback only. | 1 |
| FR-BTN-05 | The system shall debounce the Stereo/Mono contact on GPIO17 and expose its stable lighting request continuously: Stereo open/high = on; Mono closed/low = off. | 1 |

> Digital service, station, playlist and track selection remain in the WiiM app.
> In Phase 2 the ESP32 maps Vinyl to WiiM Line-In and Digital Streamer to the
> phone-controlled network playback path (ADR-0013).

### 5.3 Potentiometers

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-POT-01 | The system shall read the four rotary controls (Balance, Treble, Bass, Volume) as position sensors via ADC1. | 1 |
| FR-POT-02 | Pot readings shall be filtered (smoothing) so a settled knob yields a stable value. | 1 |
| FR-POT-03 | Pot values shall be exposed on a normalised scale (0–1000).                  | 1     |
| FR-POT-04 | The system shall support per-pot calibration, deadband, and optional inversion. | 1 |
| FR-POT-05 | Pot changes shall produce stable display updates without flicker or jitter.  | 1     |

> The potentiometers are **position sensors only** and are **not in the audio
> path** (ADR-0002).

### 5.4 Display

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-DSP-01 | The system shall render system on/off state and the four control values (volume, bass, treble, balance). | 1 |
| FR-DSP-02 | The system shall show a transient control view for approximately 2 s when a pot is adjusted. Volume uses 0–100%; Bass and Treble use a centred −50..0..+50 scale; Balance uses L50..0..R50. Each view includes a control icon and bar. Source/function changes shall receive transient confirmation and diagnostic messages shall remain available. | 1 |
| FR-DSP-03 | While a streaming source is playing, the default on-state view shall show available now-playing information, including mapped function/source, title and artist. If metadata is absent, it shall fall back to the mapped function rather than a blank or stale now-playing view. | 2 |
| FR-DSP-04 | The display shall render configuration menus.                                | 3     |
| FR-DSP-05 | The display shall present SW as **unavailable / no function**, not as a working selector. | 1 |
| FR-DSP-06 | Startup shall show a short, non-blocking monochrome Decca-logo animation lasting approximately 1 s. | 1 |
| FR-DSP-07 | The display shall identify the mapped logical function prominently. Legacy fascia button labels shall not consume space in normal, now-playing or function-confirmation views. | 2 |
| FR-DSP-08 | The OLED shall reduce uneven ageing by dimming after inactivity, turning pixels off after extended inactivity and while logically off, and waking immediately on relevant activity. | 1 |

### 5.5 Lighting

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-LGT-01 | The system shall drive the warm dial illumination via PWM through a logic-level N-channel MOSFET. | 1 |
| FR-LGT-02 | Lighting shall support configurable idle brightness and standby dimming.     | 1     |
| FR-LGT-03 | Lighting transitions shall fade (up/down) rather than switch abruptly.       | 1     |
| FR-LGT-04 | Lighting shall adopt a defined safe state at boot.                           | 1     |
| FR-LGT-05 | While logically on, Stereo shall fade the dial lighting to the stored normal level and Mono shall fade it off. Logical standby shall force lighting off. | 1 |

> Confirmed Phase 1 lighting is the **dial illumination** only. Cabinet lighting
> is not part of the confirmed Phase 1 build.

### 5.6 Settings

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-SET-01 | The system shall persist volume and brightness to NVS. Source shall be derived from the physical VHF state and shall not be persisted. | 1 |
| FR-SET-02 | Settings shall be the single point through which modules exchange state.     | 1     |
| FR-SET-03 | Persistence shall be write-limited to protect flash endurance.               | 1     |

### 5.7 Streamer Integration (WiiM)

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-WIM-01 | The system shall connect to the WiiM Pro over the local network.             | 2     |
| FR-WIM-02 | VHF shall select the phone-controlled digital playback path; every other selector position shall select WiiM Line-In for Vinyl. | 2 |
| FR-WIM-03 | Front-panel volume and streamer volume shall be synchronised.                | 2     |
| FR-WIM-04 | The system shall retrieve and display now-playing metadata.                  | 2     |

### 5.8 Advanced (Phase 3)

| ID        | Requirement                                                                 | Phase |
|-----------|------------------------------------------------------------------------------|-------|
| FR-ADV-01 | The system shall provide on-device configuration menus.                      | 3     |
| FR-ADV-02 | The system shall support authenticated local-network OTA firmware updates. Interrupted or rejected transfers shall leave the running firmware bootable. | 1 |
| FR-ADV-03 | The system shall support reuse of additional original controls.             | 3     |
| FR-ADV-04 | The system shall automatically roll back after a fully received firmware image fails post-update boot validation. | 3 |

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
| HW-09  | The retained on/off switch shall be interfaced as a **low-voltage logic input only** (internal pull-up). It shall **not** switch 230 V mains. |
| HW-10  | The original source-selector **PCB shall be retained** as the mechanical carrier for the interlocked selector mechanism (ADR-0001); it shall not be discarded. |
| HW-11  | Proposed GPIO assignments (see `docs/Wiring.md`) shall be treated as **proposed** until bench-verified, and `src/hardware.h` reconciled to them (HW-06). |
| HW-12  | Dial lighting shall be switched by a logic-level N-channel MOSFET under ESP32 PWM, with ESP32 and lighting grounds common. |

---

## 8. External Interfaces

| ID     | Interface                                                                       |
|--------|---------------------------------------------------------------------------------|
| IF-01  | **Front panel:** four 10 kΩ pots on ADC1; retained on/off switch; sole debounced VHF source contact on GPIO23; pulled-up Stereo/Mono lighting-request contact on GPIO17/TX2. VHF closed = Digital Streamer; VHF open = Vinyl. Stereo open/high = lights requested on; Mono closed/low = off. |
| IF-02  | **Display:** purchased Pi Hut 1.3-inch white 128×64 **SH1106** OLED over **I²C** at address 0x3C, powered from 3.3 V and mounted behind the dial glass. |
| IF-03  | **Lighting:** PWM-driven warm dial illumination via logic-level N-channel MOSFET (dial only in Phase 1). |
| IF-04  | **WiiM Pro local API (Phase 2):** two-state Line-In/digital-path switching, volume control, and metadata/playback-state feedback. Digital content selection remains in the WiiM app. |
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
- FR-SYS-01..04, all FR-BTN, FR-POT, FR-DSP-01/02/05/06/08, FR-LGT, FR-SET satisfied.
- Local controls and vinyl selection remain available without a network; digital content selection requires the WiiM app/network.
- **Confirmed 2026-08-30:** all eight `esp32dev` on-target suites passed, 53/53 tests after power, controls, VHF source integration and OLED protection.
- **Confirmed 2026-08-30:** after TX2 Stereo/Mono integration, the release build
  passed and all eight on-target suites passed 55/55 (buttons 11, display 15,
  hardware 3, lighting 7, OTA 5, pots 6, power 5, settings 3).
- **Confirmed 2026-08-30:** one USB bootstrap flash and one authenticated OTA upload both succeeded; after reboot serial reported `[OTA] ready at 192.168.1.79 (decca.local)`.
- Interrupted-transfer behaviour is verified to retain the previous bootable firmware.
- **Confirmed 2026-08-30:** the final `esp32dev` release build passed cleanly (RAM 49,760 bytes / 15.2%; flash 833,321 bytes / 63.6%).

### Phase 2 — WiiM Integration
- FR-WIM-01..04 and FR-DSP-03/07 satisfied.
- VHF-to-digital and released-VHF-to-Line-In switching, volume sync and metadata are verified against a live WiiM Pro.
- Loss of the streamer does not impair local control (FR-SYS-05, NFR-09).

### Phase 3 — Advanced Features
- FR-ADV-01, FR-ADV-03, FR-ADV-04 and FR-DSP-04 satisfied.
- OTA update demonstrated with a successful rollback.

---

## 12. Traceability

- **Requirements → design:** `docs/Firmware Architecture.md` (modules, phase map).
- **Key decisions:** `docs/adr/` (ADR-0001 retained PCB, 0002 pots as sensors, 0003 on/off input, 0004 superseded multi-button plan, 0005 superseded Stereo/Mono deferral, 0006 WiiM Phase 2, 0007 display presentation, 0008 streamer/separate-amplifier architecture, 0009 function-only display hierarchy, 0010 Fosi ZA3 and system power, 0011 superseded Gram-only source selection, 0012 authenticated local OTA, 0013 VHF-authoritative two-state selection, 0014 TX2 Stereo/Mono lighting command).
- **Requirements → hardware:** `docs/Hardware Architecture.md`, `docs/Wiring.md`.
- **Requirements → verification:** test suites under `test/`, one per module.
- **Change history:** `docs/Revision History.md`.

Requirement IDs should be cited in commit messages and pull requests when work
implements or verifies them (e.g. `feat(pots): filtered ADC reads [FR-POT-02]`).
