# Parts List

> **Status:** active. Human-readable summary; the formal BOM lives in
> `hardware/BOM/`. Reflects the confirmed build decisions. A selected model that
> has not yet been bought is kept separate from a genuinely open selection.

## Electronics (Phase 1)

Status meanings: **OPEN** = selection or purchase is still required; **CHECK** =
the named item is already selected or purchased but a physical or electrical
validation remains.

| Item | Qty | Status | Spec / Notes | Source |
|------|-----|--------|--------------|--------|
| ESP32 DevKit | 1 | **ACQUIRED — USB→OTA VERIFIED** | 30-pin DevKit V1 / DOIT-style board. Authenticated `esp32dev-ota` upload and post-reboot readiness were physically verified on 2026-08-30; dual application partitions are in use. | Existing stock |
| ESP32 screw-terminal adapter | 1 | **ACQUIRED** | Matching 30-pin terminal adapter used for the installed controller. | Existing stock |
| ABW1 10K linear potentiometers | 4 | **INSTALLED / VERIFIED** | AB Elektronik / TT Electronics ABW1 10K, CPC order code RE04644. Position sensors for Balance, Treble, Bass and Volume; not in the audio path. | CPC |
| OLED display | 1 | **INSTALLED / VERIFIED** | Pi Hut SKU 105630; 1.3-inch white 128×64 SH1106, four-pin I²C, 3.3 V. | The Pi Hut |
| DAOKAI MOSFET driver modules | Pack of 10; 1 previously tested | **RETAINED TEST STOCK — SUPERSEDED** | ASIN B09YYH2BTF. One module passed the earlier GPIO25 bench test on 2026-08-31. Retain the pack as test stock; DFR0457 is selected for the final installation. | Amazon / DAOKAI |
| DFRobot Gravity MOSFET Power Controller | 1 | **INSTALLED — FLICKER PASS / IMMEDIATE SWITCH + FINAL CHECKS OPEN** | DFR0457; control input is on GPIO18/D18. Earlier v0.27.1 fade observations are superseded because the installed LEDs held brightness until a delayed final switch. v0.27.4 removes the fade engine. Mono/off re-verification after HW-SW-01, immediate power-transition verification, pot stability, temperature and current remain before closure. | The Pi Hut |
| ShuoHui E10 warm-white LED lamps | Pack of 10; 3 required | **THREE-LAMP ELECTRICAL LOAD VERIFIED / FIT CHECK** | ASIN B0CFTLZFGT; E10, AC/DC 6 V, 0.2 W, 3000 K. Three parallel lamps passed even 5 V PWM illumination on 2026-08-31. Physical holder fit, final brightness and total bank current remain open. | Amazon / ShuoHui |
| 5 V regulated control supply | 1 | **CONNECTED — SHARED RAIL / USB REMOVED** | Phihong PSA15R-050P switching adapter; 5.0 V DC at 3.0 A (15 W). Now feeds the ESP32 at VIN/5V and the lighting rail; USB was removed before external power was connected. Previously powered the accepted three-lamp PWM test on 2026-08-31. | Existing stock |
| TopHomer panel-mount DC input sockets | Pack of 5 | **PURCHASED — OBSOLETE / NOT REQUIRED** | ASIN B08HGXYS4J; previously intended for the Phihong input. The installed PSU output is soldered directly into the low-voltage wiring, so no panel DC socket is used. | Amazon / TopHomer |
| Low-voltage inline fuse holder | 1 | **REUSED / IMPLEMENTED** | Original Decca holder installed in the +5 V conductor immediately after the soldered PSU output connection and before distribution. | Original Decca hardware |
| 2 A fuse | 2 | **PURCHASED** | One fitted and one spare. Recheck the final rating against measured lamp current during commissioning. | Purchased |
| WAGO 221-415 five-way distribution connectors | Pack of 3; 2 required | **ORDERED — DELIVERY / INSTALLATION CHECK** | Pi Hut SKU 104130. Use one connector as the +5 V star point and one as the common-GND star point; retain the third as a spare. Each five-way connector makes every port common and accepts the selected 22–24 AWG wiring. | The Pi Hut |
| Lyeteung JST-XH 4-pin harness set | 15 pairs | **PURCHASED — CHECK PHYSICAL STOCK** | ASIN B0CBWX98NF; 2.54 mm male/female connectors with 150 mm 22 AWG leads. Use where a four-way removable low-voltage harness is suitable. | Amazon / Lyeteung |
| 22–24 AWG stranded power wire and ferrules | 1 lot | **CHECK STOCK** | Orange for +5 V and Brown for GND; ferrules sized for the ESP32 terminal adapter and distribution connectors. | Existing stock / _TBD_ |
| IEC C14 panel-mount mains inlet | 1 | **ACQUIRED / MEASURED — REV B FIT CHECK OPEN** | 250 V AC, 10 A class. The owner supplied the physical profile dimensions and confirmed the Rev B drawing; the corrected six-sided Rev B plate passes 15/15 CAD checks. Verify inlet fit, both fixing patterns, flat clamping and rear terminal/wire clearance before mains energisation. | Amazon |
| UK mains to IEC C13 lead | 1 | **ORDERED — DELIVERY CHECK** | Appropriately fused BS 1363 UK plug to IEC C13 female lead for the rear C14 inlet. | Amazon |
| Internal 4-gang mains distribution block | 1 | **ORDERED — INSTALLATION DESIGN OPEN** | Enclosed Masterplug four-socket extension block. Retain its enclosure and verify secure mounting, routing, earthing and the final C14 connection before energisation. | Amazon / Masterplug |

## Reused Original Components (Phase 1)

| Item                    | Notes                                                        |
|-------------------------|-------------------------------------------------------------|
| Original on/off switch  | Retained with original solder joints and cable. Low-voltage logic input only (Red/Green). Not switching mains. |
| Original selector PCB   | **Retained** as mechanical carrier for the interlocked selector (ADR-0001). Not disposable. |
| Original source buttons | Original mechanism retained. Only VHF has a reliable electrical state: closed = Digital Streamer, open = Vinyl. SW/MW/LW/Gram mechanically release VHF and have no individual GPIO; replacement panel deferred (ADR-0016). |
| Original Stereo/Mono control | Retained on GPIO25/D25. Open Stereo requests lights on; closed Mono requests lights off. Firmware logic is correct, but the physical switch contact is faulty and open under HW-SW-01 (ADR-0016). |
| Original Decca knobs    | Retained via mechanical adaptor strategy (see `mechanical/Knob Adaptors/`). |

## Audio Path / Phase 2

| Item | Qty | Decision / procurement status | Notes | Source |
|------|-----|-------------------------------|-------|--------|
| WiiM Pro | 1 | **LOCKED — ACQUIRED / NETWORK + METADATA VERIFIED** | Delivered and configured as Decca on 2026-09-11. Fixed local address is held only in installation configuration. Live HTTPS identity, idle player and active TIDAL metadata probes passed on firmware `Linkplay.4.8.827634`. WiiM Home commissioning configuration is Line Out, variable volume, 2 Vrms, EQ off, Auto Headroom on, stereo, centred balance and temporary 70% limit; control commands, OTA and audio remain open gates. Continuously powered with automatic standby. | _Acquired_ |
| Fosi Audio ZA3 | 1 | **LOCKED — NOT ACQUIRED** | Selected stereo power amplifier. WiiM Pro line output feeds the ZA3; its gain/volume becomes a commissioning ceiling and its operating state is controlled by the 12 V trigger. New-unit price watch threshold: £129 or below. | _Price watch active_ |
| B&W DM601 S3 speakers | 2 | **PRIMARY TARGET — NOT ACQUIRED / FIT VERIFY** | Primary used-speaker target, not yet a locked purchase. Approx. 365 H × 204 W × 228 D mm; verify the actual pair including terminals against the hard per-bay limit of 400 H × 270 W × 245 D mm. Front-ported. Target ≤£150, exceptional ≤£130; reject damaged/dented tweeters. | _Used-speaker watch active_ |
| ZA3 12 V trigger driver and source | 1 | **REMOVED — NOT REQUIRED** | Superseded by direct WiiM Pro trigger-out to ZA3 trigger-in connection under ADR-0018. The ESP32 is not electrically connected to the trigger. | n/a |
| WiiM-to-ZA3 trigger lead/adaptor | 1 | **REQUIRED — VERIFY SUPPLIED ADAPTOR** | Correct 2.5 mm-to-3.5 mm trigger connection from WiiM Pro output to ZA3 input. Verify supplied adaptor, polarity, wake and standby behaviour before installation. | _With WiiM / verify_ |
| Stereo RCA interconnect | 1 | **OPEN — BUY LATER** | WiiM Pro line output to ZA3 input; choose length after internal placement is fixed. | _TBD_ |
| 2 × 2.5 mm² OFC speaker cable / internal harness | 1 set | **SPEC SELECTED — LENGTH / TERMINATIONS OPEN** | ZA3 to passive speakers; exact brand, length and terminations follow final placement and speaker selection. | _TBD_ |
| Monoblock power amplifiers | 2 | **REJECTED** | Added cost and complexity are not justified for the current build. | n/a |

**Locked signal architecture:** `WiiM Pro -> Fosi Audio ZA3 -> passive speakers`.

See ADR-0008 and ADR-0010 for the locked streamer, amplifier and system-power
decisions.

## Whole-system mains boundary

The Phihong adapter's enclosed mains side remains intact. Its isolated 5 V output
lead is soldered directly into the Decca low-voltage wiring, through the reused
inline fuse holder; the purchased TopHomer panel DC socket is obsolete.

The whole-system one-mains-lead arrangement is now an active implementation:
an IEC C14 inlet, UK C13 lead and enclosed Masterplug four-gang distribution
block are ordered. The corrected Rev B C14 mounting plate has passed CAD checks
but remains physical-fit pending; mains wiring, earthing, secure mounting and
rear terminal clearance must be verified before energisation.

## Mechanical / Fasteners

- Knob adaptors (printed — see `mechanical/Knob Adaptors/`)
- Display mount / bezel
- ESP32 controller housing Rev C: printed, fitted, wired and installed as a
  prototype on 2026-09-07; it fitted first time. Seven prototype and two
  installation gates remain before production release.
- IEC C14 mounting plate Rev B: 15/15 CAD checks pass and the owner confirmed
  the corrected profile drawing; physical fit remains open. Rev A is rejected.
- Standoffs, screws, brackets

## Consumables / Harness

- Wire per the colour standard in `docs/Wiring.md` (Brown GND, Red 3.3 V, Orange 5 V, White signal), except the installed H4 OLED loom: Orange = SCL and Yellow = SDA; both are signals and must never be connected to 5 V
- Removable connectors at the controller end (harnesses H1–H6), including the purchased Lyeteung JST-XH 4-pin set where appropriate
- Heat-shrink, solder, ferrules and strain-relief materials
