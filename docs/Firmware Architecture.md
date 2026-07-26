# Firmware Architecture

This document defines how the decca firmware is organised and the rules that
keep it maintainable. It is the reference for both human contributors and
AI-assisted editing.

## Design Principles

1. **Independent modules.** Each module owns one responsibility and exposes a
   small, explicit interface. A change to one peripheral touches one module.
2. **No lateral coupling.** Modules do not call each other. Input modules
   (`buttons`, `pots`) never talk to output modules (`display`, `lighting`)
   directly. Coordination happens in `main`; shared state lives in `settings`.
3. **Non-blocking.** Every `update()` returns quickly. No `delay()` in the main
   path; timing is handled with millis()-style scheduling.
4. **Local-first.** The device is fully functional with no network. Networked
   features are strictly additive.
5. **Documented interfaces.** The header is the contract. Behaviour and
   dependencies are described in each `.h` file.

## Module Set

| Module     | Responsibility                                   | Depends on            |
|------------|--------------------------------------------------|-----------------------|
| `hardware` | Pin map and board-level init                     | —                     |
| `settings` | Persisted config + shared runtime state (NVS)    | —                     |
| `buttons`  | Debounced on/off switch + source buttons (VHF, MW, LW, Gram) | `hardware`  |
| `pots`     | Filtered ADC1 reads of the four position pots (Balance, Treble, Bass, Volume) | `hardware` |
| `display`  | OLED rendering behind the dial glass              | `hardware`, `settings`|
| `lighting` | Warm dial illumination (PWM via MOSFET, fades)   | `hardware`, `settings`|
| `power`    | On/off state handling *(planned)*                | `hardware`, `settings`|
| WiiM iface | WiiM Pro local-API control *(Phase 2)*           | `settings`, Wi-Fi     |

> `power` and the WiiM interface are documented here as intended modules; they
> are added in later phases and are not yet present in `src/`.

### Module notes (confirmed Phase 1 build)

- **`buttons`** reads the retained on/off switch (low-voltage input, internal
  pull-up) and the four working source buttons with software debounce. **SW has
  no function in Phase 1** (no unique contact; ADR-0004). No transport controls
  exist in Phase 1.
- **`pots`** treats the four pots as **position sensors only** (not in the audio
  path). It applies calibration, smoothing, deadband, and optional inversion, and
  emits values suitable for stable display updates (FR-POT-01..05). Sampling is
  fixed at 100 Hz; an integer low-pass filter precedes normalisation and output
  deadband so `update()` remains deterministic and non-blocking.
- **`lighting`** drives the warm dial illumination only (dial, not cabinet) via a
  logic-level N-channel MOSFET under PWM, with fade up/down, configurable idle
  brightness, and a safe boot state.
- **`display`** presents on/off state, the selected working source, the four
  control values, and diagnostics, and shows SW as unavailable.

## Data Flow

```
buttons ─┐                         ┌─> display
pots ────┼─> main ──> settings ──> ┤
         │   (glue)   (shared      └─> lighting
         │            state)
         └─────────────────────────────┘
```

- Input modules produce events/values.
- `main` interprets them and updates `settings`.
- Output modules render from `settings` (and from values `main` passes them).
- `settings` persists state to NVS; no module writes NVS directly.

## Interface Convention

Every module lives in the `decca::<module>` namespace and exposes at least:

```cpp
void init();     // one-time setup; call from setup() in dependency order
void update();   // non-blocking; call once per loop()
```

Modules add a small number of typed accessors (e.g. `buttons::nextEvent()`,
`pots::value()`, `lighting::setBrightness()`). See the headers in `src/`.

## Initialisation Order

`hardware` → `settings` → input modules → output modules. Enforced in
`main.cpp::setup()`.

## Phase Mapping

- **Phase 1 (Local control):** `hardware`, `settings`, `buttons`, `pots`,
  `display`, `lighting`.
- **Phase 2 (WiiM):** add the WiiM interface module (network layer) and route
  source/volume/metadata through `settings`.
- **Phase 3 (Advanced):** configuration menus (`display` + `settings`), OTA
  update channel, richer UI, additional legacy controls.

## Evolving Toward `lib/`

Modules currently live in `src/`. As interfaces stabilise, self-contained
modules may migrate to `lib/` as PlatformIO libraries with their own unit tests
under `test/`, further enforcing independence. This is an intended path, not a
requirement for Phase 1.
