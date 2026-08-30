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
| `display` | SH1106 UI, animation, mapped function, metadata-ready views |
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
- Pi Hut 1.3-inch 128×64 white SH1106 OLED passed 10/10 on target at address
  0x3C; display orientation and layout were visually accepted.
- Gram GPIO23 contact was physically verified before the firmware was simplified
  to its final two-state model.
- Revised button logic passed strict host compilation and its nine-case harness.
- Lighting logic passed strict host compilation and its seven-case harness.
- OTA logic passed strict host compilation and its five-case harness.
- Display mount Rev P.5 is released and physically validated.
- Root documentation and the final OLED loom colours were reconciled at chat
  close-out.

Do not convert host validation into an on-target claim. Record future physical
results explicitly.

## Immediate gate before mounting the ESP32

OTA is implemented but **USB-to-OTA physical acceptance is still pending**.
Do not treat OTA as commissioned until one USB bootstrap flash and one
authenticated wireless upload both succeed.

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

1. Complete and record USB-to-OTA acceptance before enclosure.
2. Run the full PlatformIO build and all suites on the actual toolchain.
3. Implement the planned `power` module and bench-test GPIO19.
4. Reconcile `main.cpp` from safe bootstrap into the non-blocking Phase 1
   scheduler, initialising and coordinating all existing modules while
   continuously servicing OTA.
5. Bench-test the MOSFET/lamp bank and verify GPIO25 safe-off/fade behaviour.
6. Commission normal and standby lighting levels.
7. Add WiiM Pro integration only in Phase 2, after the hardware is available and
   the live local API is verified.
8. Keep automatic failed-boot OTA rollback as Phase 3 unless separately brought
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

Immediate priority: complete the physical USB-to-OTA acceptance before the ESP32
is mounted. The Windows PowerShell command "pio" is not on PATH, so use:
$pio = "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe"
First confirm the PlatformIO version and actual COM port, then guide me one step
at a time through test_ota, the initial USB flash, serial confirmation of
"[OTA] ready", and one authenticated esp32dev-ota upload. Never ask me to paste
or reveal Wi-Fi or OTA passwords, and never commit src/secrets.h. Do not type or
tell me to type the literal placeholder COM_PORT.

Do not claim OTA commissioning until the physical wireless upload succeeds.
After that, continue the documented firmware sequence: full on-target
build/tests, power-module and GPIO19 verification, non-blocking Phase 1 main-loop
orchestration, then GPIO25 lighting commissioning. Preserve the locked Gram-only
source logic: Gram closed = Vinyl/Line-In; Gram open = Digital Streamer controlled
by phone; GPIO16/17/18 remain unused. Preserve the final OLED loom: Brown GND,
Red 3V3 VCC, Orange SCL GPIO22, Yellow SDA GPIO21.

Keep the ESP32 control/UI-only, preserve module independence, update all affected
docs/BOM/status references with each change, verify before committing, and push
logical changes to main. Draft PR #7 is separate Rev Q bezel work and must not be
merged until its recorded physical gates pass.
```
