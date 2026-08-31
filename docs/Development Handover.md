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
| `settings` | NVS persistence implemented, schema version 3 |
| `buttons` | On/off, sole VHF contact and TX2 Stereo/Mono lighting request, 25 ms non-blocking debounce |
| `pots` | Four filtered/calibrated ADC1 inputs |
| `display` | Fitted-Perspex SH1106 UI physically accepted; calibrated views plus idle dim/display-off protection |
| `lighting` | Safe-off non-blocking PWM fades |
| `ota` | Authenticated LAN OTA, reconnect handling, dual-app partitions |
| `power` | GPIO-independent logical on/standby state implemented and tested |
| WiiM interface | Phase 2, not implemented |
| Main orchestration | Power, pots, VHF source, fitted display and OTA integrated; lighting commissioning open |

The ESP32 is control/UI only. It never carries or processes audio.

## Accepted source logic

The original selector PCB remains as a mechanical carrier, but only the VHF
state is reliable electrically:

| VHF contact | Logical source | Future WiiM action |
|---|---|---|
| Closed / latched | Digital Streamer | Restore phone-controlled digital playback |
| Open / released | Vinyl | Select Line-In |

GPIO23/D23 is the only source input. The accepted VHF-derived pair is Green to
GPIO23 and Yellow to GND, although the two dry-contact wires may be swapped.
GPIO16 and GPIO18 are released. GPIO17 is released from the source bank and
assigned to the separate Stereo/Mono contact. SW, MW, LW and Gram have no individual
firmware function; their interlocked release of VHF selects Vinyl. A replacement
button panel is deferred.

## Confirmed controller wiring

| Function | ESP32 | Physical status |
|---|---:|---|
| Volume | GPIO32/D32 | Bench-verified, 0 / about 2047 / 4095 |
| Bass | GPIO33/D33 | Bench-verified, 0 / about 2047 / 4095 |
| Treble | GPIO34/D34 | Bench-verified, 0 / about 2047 / 4095 |
| Balance | GPIO35/D35 | Bench-verified, 0 / about 2047 / 4095 |
| VHF source contact | GPIO23/D23 | Physically accepted |
| OLED SDA | GPIO21/D21 | Bench-verified |
| OLED SCL | GPIO22/D22 | Bench-verified |
| On/off | GPIO19/D19 | Bench-verified, closed = on / open = standby |
| Stereo/Mono lighting request | GPIO17/TX2 | Physically accepted, open Stereo = on / closed Mono = off |
| Dial-light PWM | GPIO25/D25 | Electrically accepted with MOSFET/three-lamp load |

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
- VHF on GPIO23 was physically accepted as the only reliable active selector;
  every other interlocked position releases it and selects Vinyl.
- GPIO19/D19 was physically verified with the retained H2 Red/Green switch.
  Closed selects logical ON and open selects STANDBY; both transitions were
  accepted on the production firmware.
- Revised button logic passed strict host compilation and its nine-case harness.
- Lighting logic passed strict host compilation and its seven-case harness.
- OTA logic passed strict host compilation and its five-case harness.
- USB-to-OTA physical acceptance passed on 2026-08-30: the authenticated
  `esp32dev-ota` upload succeeded and the rebooted ESP32 reported
  `[OTA] ready at 192.168.1.79 (decca.local)`.
- The accepted controls/source/display `esp32dev` release build passed and all
  eight on-target suites passed 53/53 tests on 2026-08-30 (buttons 9, display 15,
  hardware 3, lighting 7, OTA 5, pots 6, power 5 and settings 3). Production
  firmware was restored by USB; serial reported `[POWER] state=ON` and
  `[OTA] ready at 192.168.1.79 (decca.local)`.
- After TX2 Stereo/Mono integration, the release build passed and all eight
  on-target suites passed 55/55 (buttons 11, display 15, hardware 3, lighting 7,
  OTA 5, pots 6, power 5 and settings 3).
- After production lighting coordination and settings schema v3, the
  credential-enabled release build passed (RAM 49,936 bytes / 15.2%; flash
  839,253 bytes / 64.0%) and all eight on-target suites again passed 55/55.
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
   eight on-target suites; latest accepted run passed 55/55 tests.
3. **Complete (2026-08-30):** fitted-Perspex display calibration, visual design
   cycle and physical acceptance.
4. **Complete (2026-08-30):** implement the logical `power` module, bench-test
   GPIO19 and integrate on/standby display coordination in production.
5. **Complete:** production coordinates pots, persistent VHF-derived source,
   logical power, fitted display and OTA in one non-blocking loop.
6. **Complete (2026-08-31):** GPIO25/MOSFET/three-lamp electrical test passed:
   safe off, smooth fades through full duty, even illumination and fade fully off.
7. **Complete (2026-08-31):** normal Stereo lighting approved at 90% / duty
   230 and integrated in production; Mono and logical standby fade to off.
8. **Complete (2026-08-30):** original Stereo/Mono switch wired to TX2/GPIO17
   and GND. Physical snapshots confirmed Stereo open requests dial lights on and
   Mono closed requests them off. GPIO25 load remained disabled during testing.
9. Add WiiM Pro integration only in Phase 2, after the hardware is available and
   the live local API is verified.
10. Keep automatic failed-boot OTA rollback as Phase 3 unless separately brought
   forward.

## Open procurement and electrical work

Consult `docs/Parts List.md` and the CSV BOMs for current detail. Principal open
items are the inline fuse holder and matching fuses, 5 V/GND distribution
connectors, final lighting level/current/holder checks, the ZA3 12 V trigger interface,
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

Immediate priority: complete final lamp-holder fit and current measurement,
then proceed to Phase 2 WiiM integration when its hardware is available.
Production now coordinates all four pots,
VHF-derived source, logical power and display while
continuously servicing OTA. The OLED dims after 60 s, turns pixels off after
5 min, and blanks standby after 10 s, waking immediately on activity. The
accepted control overlays use Volume 0–100%, Bass/Treble −50..0..+50 and Balance
L50..0..R50 with centred bars and monochrome icons.

TX2/GPIO17 and the GPIO25/MOSFET/three-lamp electrical path are physically
accepted. Stereo fades to 90%; Mono and standby fade off. Preserve the accepted
VHF-only source logic: VHF closed = Digital
Streamer; VHF open = Vinyl/Line-In;
GPIO16 and GPIO18 remain unused. Preserve the final OLED loom: Brown GND,
Red 3V3 VCC, Orange SCL GPIO22, Yellow SDA GPIO21.

Keep the ESP32 control/UI-only, preserve module independence, update all affected
docs/BOM/status references with each change, verify before committing, and push
logical changes to main. Draft PR #7 is separate Rev Q bezel work and must not be
merged until its recorded physical gates pass.
```
