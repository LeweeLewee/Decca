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
| `buttons`  | Debounced on/off, sole VHF source selector and Stereo/Mono lighting request | `hardware`  |
| `pots`     | Filtered ADC1 reads of the four position pots (Balance, Treble, Bass, Volume) | `hardware` |
| `display`  | OLED rendering and idle pixel protection          | `hardware`, `settings`|
| `lighting` | Warm dial illumination (PWM via MOSFET, fades)   | `hardware`, `settings`|
| `power`    | Pure logical on/standby state handling           | —                     |
| WiiM iface | WiiM Pro local-API control *(Phase 2)*           | `settings`, Wi-Fi     |
| `ota`      | Authenticated Wi-Fi firmware update service      | Wi-Fi                 |

> The WiiM interface remains a later Phase 2 module. `power` and `ota` are
> implemented in `src/` and active in the production runtime.

### Module notes (confirmed Phase 1 build)

- **`buttons`** reads the retained on/off switch and sole active-low VHF contact
  with 25 ms software debounce. It exposes the stable VHF-derived source mode:
  closed = Digital Streamer; open = Vinyl. Press events do not repeat while held.
  The other interlocked positions release VHF and therefore select Vinyl
  (ADR-0013).
- **`pots`** treats the four pots as **position sensors only** (not in the audio
  path). It applies calibration, smoothing, deadband, and optional inversion, and
  emits values suitable for stable display updates (FR-POT-01..05). Sampling is
  fixed at 100 Hz; an integer low-pass filter precedes normalisation and output
  deadband so `update()` remains deterministic and non-blocking.
- **`lighting`** drives the warm dial illumination only (dial, not cabinet) via a
  logic-level N-channel MOSFET under PWM, with fade up/down, configurable idle
  brightness, and a safe boot state. It starts at duty 0, reads its initial
  target from `settings`, and advances one PWM count every 10 ms without
  blocking. `main` selects normal or standby targets; `lighting` does not read
  buttons or power state directly.
- **`display`** drives the purchased 1.3-inch 128×64 SH1106 panel at I²C
  address 0x3C. Its presentation contract is defined by ADR-0007: a short
  non-blocking monochrome Decca-logo startup animation; standby; transient
  control views; diagnostics; and an explicit SW unavailable message. The
  production coordinator supplies all four pot values and persistent source
  state. Volume is presented as 0–100%; Bass/Treble use centred −50..0..+50;
  Balance uses L50..0..R50; each transient includes a compact monochrome icon.
  In Phase
  2 the default on-state view prioritises now-playing metadata, falls back to
  the mapped logical function, and omits legacy fascia labels from user-facing
  views under ADR-0009. The display consumes coherent state supplied by `main`;
  it does not call input or WiiM modules. It redraws only when its semantic
  frame changes, an animation frame advances, or a transient expires. Mapped
  names and metadata use fixed-size copied text fields, so Phase 2 can supply
  them without allocation or changing the display interface. The installed
  panel is rendered at Adafruit GFX rotation 2 (180 degrees) and contrast 0x80.
  Physical calibration established viewport X4–123/Y10–61; production content
  uses Y24–60 to avoid the upper viewing-angle/parallax zone. The accepted UI
  presents one priority at a time: identity/standby, a control value and bar,
  source confirmation, status, or title/artist metadata. A small bottom-right
  triangle or two-bar glyph communicates playing or paused without repeating a
  text label. To limit OLED uneven ageing, activity runs at contrast 0x80, the
  panel dims to 0x20 after 60 seconds, and its pixels turn off after five minutes
  without activity. Standby is shown for ten seconds before pixels turn off.
  State, control, status and metadata activity wake it immediately. The
  non-blocking full-canvas calibration frame remains available as a service
  diagnostic and is subject to the same protection timer.
- **`power`** owns only the requested logical state. It converts the debounced
  on/off request supplied by `main` into On or Standby and reports transitions;
  it owns no GPIO and does not call display, lighting or network modules.

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
  `display`, `lighting`; authenticated `ota` is brought forward before enclosure.
- **Phase 2 (WiiM):** add the WiiM interface module; VHF selects digital playback,
  released VHF selects Line-In for Vinyl, and the phone controls digital
  content. Volume and metadata route through `settings`.
- **Phase 3 (Advanced):** configuration menus, automatic post-boot OTA rollback
  validation, richer UI and additional legacy controls.

## Evolving Toward `lib/`

Modules currently live in `src/`. As interfaces stabilise, self-contained
modules may migrate to `lib/` as PlatformIO libraries with their own unit tests
under `test/`, further enforcing independence. This is an intended path, not a
requirement for Phase 1.
