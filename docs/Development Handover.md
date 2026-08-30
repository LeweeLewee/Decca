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

The production `src/main.cpp` now initialises the safe board state, buttons,
logical power, display and authenticated ArduinoOTA. It continuously services
the original on/off switch, display and OTA without blocking. Full settings,
pots, source, lighting and WiiM coordination is not yet implemented.

Implemented modules:

| Module | State |
|---|---|
| `hardware` | Pin map and safe initialisation implemented |
| `settings` | NVS persistence implemented, schema version 2 |
| `buttons` | On/off plus sole Gram contact, 25 ms non-blocking debounce |
| `pots` | Four filtered/calibrated ADC1 inputs |
| `display` | Fitted-Perspex SH1106 UI physically accepted; calibrated views plus idle dim/display-off protection |
| `lighting` | Safe-off non-blocking PWM fades |
| `ota` | Authenticated LAN OTA, reconnect handling, dual-app partitions |
| `power` | GPIO-independent logical on/standby state implemented and tested |
| WiiM interface | Phase 2, not implemented |
| Main orchestration | GPIO19 power/display/OTA slice implemented; remaining Phase 1 coordination open |

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
| On/off | GPIO19/D19 | Bench-verified, closed = on / open = standby |
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
  0x3C and physically accepted behind the final Perspex on 2026-08-30. Output is
  rotated 180 degrees; the measured viewport is X4–123/Y10–61 and normal content
  is restricted to Y24–60 for viewing-angle readability. Contrast 0x80 and the
  focused identity, control, source, metadata, play/pause and standby layouts
  were accepted from physical photographs. The calibration pattern remains a
  service diagnostic.
- Gram GPIO23 contact was physically verified before the firmware was simplified
  to its final two-state model.
- GPIO19/D19 was physically verified with the retained H2 Red/Green switch.
  Closed selects logical ON and open selects STANDBY; both transitions were
  accepted on the production firmware.
- Revised button logic passed strict host compilation and its nine-case harness.
- Lighting logic passed strict host compilation and its seven-case harness.
- OTA logic passed strict host compilation and its five-case harness.
- USB-to-OTA physical acceptance passed on 2026-08-30: the authenticated
  `esp32dev-ota` upload succeeded and the rebooted ESP32 reported
  `[OTA] ready at 192.168.1.79 (decca.local)`.
- The power/display-protection `esp32dev` release build passed and all eight
  on-target suites passed 52/52 tests on 2026-08-30 (buttons 9, display 14,
  hardware 3, lighting 7, OTA 5, pots 6, power 5 and settings 3). Production
  firmware was restored by USB; serial reported `[POWER] state=ON` and
  `[OTA] ready at 192.168.1.79 (decca.local)`.
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
   eight on-target suites; latest accepted run passed 52/52 tests.
3. **Complete (2026-08-30):** fitted-Perspex display calibration, visual design
   cycle and physical acceptance.
4. **Complete (2026-08-30):** implement the logical `power` module, bench-test
   GPIO19 and integrate on/standby display coordination in production.
5. **Current:** extend `main.cpp` into the complete non-blocking Phase 1
   scheduler, coordinating pots, Gram source and lighting while continuously
   servicing OTA.
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

Immediate priority: extend the production coordinator with the remaining Phase
1 pots, Gram source and lighting behaviour, one step at a time. The preceding
gates passed on 2026-08-30: authenticated USB-to-OTA acceptance, fitted-Perspex
display acceptance, GPIO19 on/off acceptance and all 52 on-target tests.
Production coordinates logical power/display state while continuously servicing
OTA; its OLED dims after 60 s, turns pixels off after 5 min, and blanks standby
after 10 s, waking immediately on activity.

Continue with non-blocking Phase 1 main-loop orchestration, then GPIO25 lighting
commissioning. Keep the deferred Stereo/Mono
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
