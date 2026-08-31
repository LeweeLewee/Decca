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
| DFRobot Gravity MOSFET Power Controller | 1 | **OPEN — BUY** | DFR0457; selected for final dial-lamp switching. Accepts the 5 V lamp rail and 3.3 V control, with a specified switching range of 0–1 kHz. After installation, set firmware PWM to no more than 1 kHz and repeat safe-off, brightness, flicker, pot-stability and current tests. | The Pi Hut |
| ShuoHui E10 warm-white LED lamps | Pack of 10; 3 required | **THREE-LAMP ELECTRICAL LOAD VERIFIED / FIT CHECK** | ASIN B0CFTLZFGT; E10, AC/DC 6 V, 0.2 W, 3000 K. Three parallel lamps passed even 5 V PWM illumination on 2026-08-31. Physical holder fit, final brightness and total bank current remain open. | Amazon / ShuoHui |
| 5 V regulated control supply | 1 | **CONNECTED — SHARED RAIL / USB REMOVED** | Phihong PSA15R-050P switching adapter; 5.0 V DC at 3.0 A (15 W). Now feeds the ESP32 at VIN/5V and the lighting rail; USB was removed before external power was connected. Previously powered the accepted three-lamp PWM test on 2026-08-31. | Existing stock |
| TopHomer panel-mount DC input sockets | Pack of 5; 1 required | **PURCHASED — DELIVERY / FIT / POLARITY CHECK** | ASIN B08HGXYS4J; female two-terminal threaded-nut sockets, 5.5 mm OD × 2.1 mm ID, rated 3 A. Use one only after confirming the actual Phihong plug fit and centre-positive polarity before drilling or wiring. | Amazon / TopHomer |
| Low-voltage inline fuse holder | 1 | **OPEN — BUY** | Installed in the +5 V conductor immediately after the panel socket and before distribution. | _TBD_ |
| 2 A fuse | 2 | **OPEN — BUY** | One fitted and one spare; type must match the selected holder. Final rating to be rechecked against measured lamp current during bench commissioning. | _TBD_ |
| WAGO 221-415 five-way distribution connectors | Pack of 3; 2 required | **OPEN — BUY** | Pi Hut SKU 104130. Use one connector as the +5 V star point and one as the common-GND star point; retain the third as a spare. Each five-way connector makes every port common and accepts the selected 22–24 AWG wiring. | The Pi Hut |
| Lyeteung JST-XH 4-pin harness set | 15 pairs | **PURCHASED — CHECK PHYSICAL STOCK** | ASIN B0CBWX98NF; 2.54 mm male/female connectors with 150 mm 22 AWG leads. Use where a four-way removable low-voltage harness is suitable. | Amazon / Lyeteung |
| 22–24 AWG stranded power wire and ferrules | 1 lot | **CHECK STOCK** | Orange for +5 V and Brown for GND; ferrules sized for the ESP32 terminal adapter and distribution connectors. | Existing stock / _TBD_ |

## Reused Original Components (Phase 1)

| Item                    | Notes                                                        |
|-------------------------|-------------------------------------------------------------|
| Original on/off switch  | Retained with original solder joints and cable. Low-voltage logic input only (Red/Green). Not switching mains. |
| Original selector PCB   | **Retained** as mechanical carrier for the interlocked selector (ADR-0001). Not disposable. |
| Original source buttons | Original mechanism retained. Only VHF has a reliable electrical state: closed = Digital Streamer, open = Vinyl. SW/MW/LW/Gram mechanically release VHF and have no individual GPIO; replacement panel deferred (ADR-0013). |
| Original Stereo/Mono control | Retained and physically verified on TX2/GPIO17: open Stereo requests lights on; closed Mono requests lights off (ADR-0014). |
| Original Decca knobs    | Retained via mechanical adaptor strategy (see `mechanical/Knob Adaptors/`). |

## Audio Path / Phase 2

| Item | Qty | Decision / procurement status | Notes | Source |
|------|-----|-------------------------------|-------|--------|
| WiiM Pro | 1 | **LOCKED — NOT ACQUIRED** | Selected networked streamer/source. ESP32 restores the digital path when VHF is latched and selects Line-In for Vinyl when VHF is released; phone controls digital content. Continuously powered with automatic standby. Do not substitute WiiM Amp / Amp Pro without a new ADR. New-unit price watch threshold: £149 or below. | _Price watch active_ |
| Fosi Audio ZA3 | 1 | **LOCKED — NOT ACQUIRED** | Selected stereo power amplifier. WiiM Pro line output feeds the ZA3; its gain/volume becomes a commissioning ceiling and its operating state is controlled by the 12 V trigger. New-unit price watch threshold: £129 or below. | _Price watch active_ |
| B&W DM601 S3 speakers | 2 | **PRIMARY TARGET — NOT ACQUIRED / FIT VERIFY** | Primary used-speaker target, not yet a locked purchase. Approx. 365 H × 204 W × 228 D mm; verify the actual pair including terminals against the hard per-bay limit of 400 H × 270 W × 245 D mm. Front-ported. Target ≤£150, exceptional ≤£130; reject damaged/dented tweeters. | _Used-speaker watch active_ |
| ZA3 12 V trigger driver and source | 1 | **OPEN — DESIGN / SELECT** | ESP32-controlled transistor/MOSFET or isolated interface plus suitable 12 V source. Exact circuit and GPIO require selection and bench verification. | _TBD_ |
| ZA3 trigger plug / lead | 1 | **OPEN — SELECT WITH DRIVER** | Match the ZA3 trigger connector and confirmed polarity; length follows final equipment placement. | _TBD_ |
| Stereo RCA interconnect | 1 | **OPEN — BUY LATER** | WiiM Pro line output to ZA3 input; choose length after internal placement is fixed. | _TBD_ |
| 2 × 2.5 mm² OFC speaker cable / internal harness | 1 set | **SPEC SELECTED — LENGTH / TERMINATIONS OPEN** | ZA3 to passive speakers; exact brand, length and terminations follow final placement and speaker selection. | _TBD_ |
| Monoblock power amplifiers | 2 | **REJECTED** | Added cost and complexity are not justified for the current build. | n/a |

**Locked signal architecture:** `WiiM Pro -> Fosi Audio ZA3 -> passive speakers`.

See ADR-0008 and ADR-0010 for the locked streamer, amplifier and system-power
decisions.

## Whole-system mains boundary

The Phihong 5 V adapter is treated as an **external enclosed adapter** by default;
only its isolated 5 V output enters the cabinet. The current design therefore
does not add a 230 V socket merely for the controller rail.

A future one-mains-lead arrangement for the WiiM, ZA3 and controller would require
a separate fused mains-inlet/distribution design. That remains an **open system
design decision**, not an approved component purchase.

## Mechanical / Fasteners

- Knob adaptors (printed — see `mechanical/Knob Adaptors/`)
- Display mount / bezel
- Standoffs, screws, brackets

## Consumables / Harness

- Wire per the colour standard in `docs/Wiring.md` (Brown GND, Red 3.3 V, Orange 5 V, White signal), except the installed H4 OLED loom: Orange = SCL and Yellow = SDA; both are signals and must never be connected to 5 V
- Removable connectors at the controller end (harnesses H1–H6), including the purchased Lyeteung JST-XH 4-pin set where appropriate
- Heat-shrink, solder, ferrules and strain-relief materials
