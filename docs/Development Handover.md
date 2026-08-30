# Development Handover

> **Close-out date:** 2026-08-30  
> **Repository:** `LeweeLewee/Decca`  
> **Authoritative branch:** `main`

This document is the durable handover for firmware development and maintenance.
Read it before relying on chat history.

## Read first

1. `CLAUDE.md`
2. `docs/Specification.md`
3. `docs/Firmware Architecture.md`
4. `docs/Hardware Architecture.md`
5. `docs/Wiring.md`
6. `docs/Build Guide.md`
7. Relevant ADRs under `docs/adr/`

Always inspect the live `main` branch before changing code. Historical chat
messages and old revision-history entries may describe superseded hardware.

## Current firmware state

The production `src/main.cpp` is intentionally a **safe bootstrap runtime**.
It initialises safe board pins and continuously services authenticated ArduinoOTA.
It does **not yet** orchestrate settings, buttons, pots, display, lighting, power
or WiiM control during normal operation.

Implemented modules:

| Module | State |
|---|---|
| `hardware` | Pin map and safe initialisation implemented |
| `settings` | NVS persistence implemented, schema version 2 |
| `buttons` | On/off plus sole Gram contact, 25 ms non-blocking debounce |
| `pots` | Four filtered/calibrated ADC1 inputs |
| `display` | SH1106 UI plus active fitted-aperture calibration pattern; output rotated 180 degrees |
| `lighting` | Safe-off non-blocking PWM fades |
| `ota` | Authenticated LAN OTA, reconnect handling, dual-app partitions |
| `power` | Planned, not implemented |
| WiiM interface | Phase 2, not implemented |
| Main orchestration | Not implemented beyond the OTA bootstrap |

The ESP32 is control/UI only. It never carries or processes audio.

## Locked source logic

The original selector PCB remains as a mechanical carrier, but only the Gram
contact is used electrically:

| Gram contact | Logical source | Future WiiM action |
|---|---|---|
| Closed / latched | Vinyl | Select Line-In |
| Open / released | Digital Streamer | Restore phone-controlled digital playback |

GPIO23/D23 is the only source input. The verified Gram pair is Green to GPIO23
and Yellow to GND, although the two dry-contact wires may be swapped. GPIO16,
GPIO17 and GPIO18 are released. VHF, SW, MW and LW have no individual firmware
function. A replacement button panel is deferred.

## Confirmed controller wiring

| Function | ESP32 | Physical status |
|---|---:|---|
| Volume | GPIO32/D32 | Bench-verified, 0 / about 2047 / 4095 |
| Bass | GPIO33/D33 | Bench-verified, 0 / about 2047 / 4095 |
| Treble | GPIO34/D34 | Bench-verified, 0 / about 2047 / 4095 |
| Balance | GPIO35/D35 | Bench-verified, 0 / about 2047 / 4095 |
| Gram | GPIO23/D23 | Bench-verified contact |
| OLED SDA | GPIO21/D21 | Bench-verified |
| OLED SCL | GPIO22/D22 | Bench-verified |
| On/off | GPIO19/D19 | Proposed, physical test pending |
| Dial-light PWM | GPIO25/D25 | Proposed, load test pending |

Final H4 OLED loom, physically confirmed 2026-08-30:

| Wire | OLED | ESP32 |
|---|---|---|
| Brown | GND | GND |
| Red | VCC | 3V3 |
| Orange | SCL | GPIO22/D22 |
| Yellow | SDA | GPIO21/D21 |

Orange and Yellow are signal wires in H4. Neither is a 5 V conductor.

## Completed evidence

- Four pots passed on target with full 0–4095 travel and clockwise increase.
- Pi Hut 1.3-inch 128×64 white SH1106 OLED was electrically verified at address
  0x3C. After final Perspex installation exposed a restricted visible area, the
  output was rotated 180 degrees and an 8-pixel fitted-aperture calibration
  pattern passed its expanded 11/11 display suite on 2026-08-30. Straight-on
  photo analysis and final safe-viewport layout remain pending.
- Gram GPIO23 contact was physically verified before the firmware was simplified
  to its final two-state model.
- Revised button logic passed strict host compilation and its nine-case harness.
- Lighting logic passed strict host compilation and its seven-case harness.
- OTA logic passed strict host compilation and its five-case harness.
- USB-to-OTA physical acceptance passed on 2026-08-30: the authenticated
  `esp32dev-ota` upload succeeded and the rebooted ESP32 reported
  `[OTA] ready at 192.168.1.79 (decca.local)`.
- The full `esp32dev` release build passed and all seven on-target suites passed
  43/43 tests on 2026-08-30. Production firmware was restored afterward and
  OTA readiness was reconfirmed.
- Display mount Rev P.5 is released and physically validated.
- Root documentation and the final OLED loom colours were reconciled at chat
  close-out.

Do not convert host validation into an on-target claim. Record future physical
results explicitly.

## Completed gate before mounting the ESP32

USB-to-OTA physical acceptance **passed on 2026-08-30**. The authenticated
`esp32dev-ota` upload succeeded and, after reboot, serial reported
`[OTA] ready at 192.168.1.79 (decca.local)`. The procedure is retained below for
future controller replacement or recovery.

On the user's Windows machine, `pio` is not currently on PATH. Use the
PlatformIO executable directly:

```powershell
$pio = "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe"
& $pio --version
& $pio device list
```

Never type the literal placeholder `COM_PORT`. Set the actual port reported by
`device list`, for example:

```powershell
$port = "COM5"
& $pio test -e esp32dev -f test_ota
& $pio run -e esp32dev -t upload --upload-port $port
& $pio device monitor --port $port -b 115200
```

Expected serial message:

```text
[OTA] ready at 192.168.x.x (decca.local)
```

Then exit the monitor with Ctrl+C and prove wireless upload:

```powershell
$env:DECCA_OTA_PASSWORD = "THE SAME PRIVATE PASSWORD USED IN src\secrets.h"
& $pio run -e esp32dev-ota -t upload
Remove-Item Env:DECCA_OTA_PASSWORD
```

If mDNS fails, repeat the OTA command with
`--upload-port 192.168.x.x` using the address printed by the ESP32.

`src/secrets.h` is local and gitignored. Never request, display, log or commit
the user's Wi-Fi or OTA passwords.

## Recommended firmware sequence

1. **Complete (2026-08-30):** USB-to-OTA acceptance before enclosure.
2. **Complete (2026-08-30):** full PlatformIO `esp32dev` release build and all
   seven on-target suites, 43/43 tests passed.
3. **Current:** photograph the active fitted-aperture calibration pattern
   straight-on, derive the visible pixel bounds, then redesign and verify every
   display view inside the calibrated safe viewport.
4. Implement the planned `power` module and bench-test GPIO19.
5. Reconcile `main.cpp` from safe bootstrap into the non-blocking Phase 1
   scheduler, initialising and coordinating all existing modules while
   continuously servicing OTA.
6. Bench-test the MOSFET/lamp bank and verify GPIO25 safe-off/fade behaviour.
7. Commission normal and standby lighting levels.
8. **Deferred control reuse:** wire and implement the original Stereo/Mono switch
   so Stereo commands the dial lights on and Mono commands them off. It remains
   unwired in the current Phase 1 build; assign and bench-verify a safe GPIO
   before implementation.
9. Add WiiM Pro integration only in Phase 2, after the hardware is available and
   the live local API is verified.
10. Keep automatic failed-boot OTA rollback as Phase 3 unless separately brought
   forward.

## Open procurement and electrical work

Consult `docs/Parts List.md` and the CSV BOMs for current detail. Principal open
items are the inline fuse holder and matching fuses, 5 V/GND distribution
connectors, final lighting load verification, the ZA3 12 V trigger interface,
WiiM Pro, Fosi ZA3, speakers and final audio interconnects.

## Open mechanical work

Draft PR [#7](https://github.com/LeweeLewee/Decca/pull/7) contains the Rev Q
display bezel prototype. It is deliberately **not ready to merge**. Keep it
draft until its corner gauge, dry fit, lip quality, cut-edge masking, carrier
independence and powered readability tests pass. Do not alter the released Rev
P.5 carrier to make Rev Q fit.

## Engineering guardrails

- Preserve module independence; coordinate only in `main`.
- Keep all update paths non-blocking; no `delay()` in steady-state control.
- Avoid dynamic allocation in steady state.
- Persist only through `settings`.
- Keep analogue inputs on ADC1 because Wi-Fi is active.
- Treat proposed pins as unverified until a physical test is recorded.
- Update wiring, BOM, architecture and revision history with relevant changes.
- Use Conventional Commits and do not overwrite unrelated work.
- Do not merge draft mechanical work merely to make `main` look complete.

## New-chat handover prompt

```text
Continue development and maintenance of the Decca ESP32 restoration firmware in
https://github.com/LeweeLewee/Decca.

Before acting, read docs/Development Handover.md in full, then CLAUDE.md,
docs/Specification.md, docs/Firmware Architecture.md, docs/Hardware
Architecture.md, docs/Wiring.md, docs/Build Guide.md and the relevant ADRs.
Treat the live main branch and those documents as authoritative over chat memory.

Immediate priority: use a straight-on photograph of the fitted OLED's active
8-pixel calibration grid to derive the visible pixel bounds, then redesign all
display views inside that calibrated safe viewport. Output is already rotated
180 degrees and the production safe-bootstrap runtime is holding the pattern
while continuously servicing OTA. The expanded display suite passed 11/11.

After the fitted-display refinement, implement the planned `power` module and
bench-test GPIO19 one step at a time. Earlier gates passed on 2026-08-30:
authenticated USB-to-OTA physical acceptance, a clean `esp32dev` release build
and all seven
on-target suites (43/43 tests). Production firmware was restored afterward and
serial reconfirmed `[OTA] ready at 192.168.1.79 (decca.local)`.

After power/GPIO19 verification, continue with non-blocking Phase 1 main-loop
orchestration, then GPIO25 lighting commissioning. Keep the deferred Stereo/Mono
lighting mapping on the later development list: Stereo = lights on; Mono = lights
off. Preserve the locked Gram-only
source logic: Gram closed = Vinyl/Line-In; Gram open = Digital Streamer controlled
by phone; GPIO16/17/18 remain unused. Preserve the final OLED loom: Brown GND,
Red 3V3 VCC, Orange SCL GPIO22, Yellow SDA GPIO21.

Keep the ESP32 control/UI-only, preserve module independence, update all affected
docs/BOM/status references with each change, verify before committing, and push
logical changes to main. Draft PR #7 is separate Rev Q bezel work and must not be
merged until its recorded physical gates pass.
```
