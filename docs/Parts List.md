# Parts List

> **Status:** active. Human-readable summary; the formal BOM lives in
> `hardware/BOM/`. Reflects the confirmed build decisions. Where a component
> model is not yet selected, that is stated explicitly rather than inferred.

## Electronics (Phase 1)

Status meanings: **OPEN** = purchase or selection still required; **CHECK STOCK** =
may already be available but has not been confirmed.

| Item | Qty | Status | Spec / Notes | Source |
|------|-----|--------|--------------|--------|
| ESP32 DevKit | 1 | **ACQUIRED** | 30-pin DevKit V1 / DOIT-style board; dual-core, Wi-Fi, ADC1 and LEDC PWM. Control/UI only, no audio. | Existing stock |
| ESP32 screw-terminal adapter | 1 | **ACQUIRED** | Matching 30-pin terminal adapter used for the installed controller. | Existing stock |
| Potentiometer, 10 kΩ linear | 4 | **INSTALLED / VERIFIED** | Position sensors for Balance, Treble, Bass and Volume. Not in the audio path. | Existing stock |
| OLED display | 1 | **INSTALLED / VERIFIED** | Pi Hut SKU 105630; 1.3-inch white 128×64 SH1106, four-pin I²C, 3.3 V. | The Pi Hut |
| Logic-level N-channel MOSFET stage | 1 | **OPEN — SELECT** | 3.3 V gate-compatible, PWM-capable low-side stage for the complete 5 V lamp bank. Minimum 3 A rating; include a gate pulldown, either on the module or externally. | _TBD_ |
| E10 warm-white LED lamps | 3 | **OPEN — BUY** | E10/MES, approximately 24 mm overall length, preferably 2200–3000 K; nominal 5 V or an operating range explicitly including 5 V; identical and wired in parallel. | _TBD_ |
| 5 V regulated control supply | 1 | **ACQUIRED — OUTPUT CHECK REQUIRED** | Phihong PSA15R-050P switching adapter; 5.0 V DC at 3.0 A (15 W). Confirm the actual DC plug dimensions and centre polarity with a multimeter before connection. | Existing stock |
| Panel-mount DC input socket | 1 | **OPEN — VERIFY THEN BUY** | Female socket matching the Phihong plug, rated at least 5 V / 3 A. Provisional expectation is 5.5 mm OD × 2.1 mm ID, centre positive; do not order until the actual plug is checked. | _TBD_ |
| Low-voltage inline fuse holder | 1 | **OPEN — BUY** | Installed in the +5 V conductor immediately after the panel socket and before distribution. | _TBD_ |
| 2 A fuse | 2 | **OPEN — BUY** | One fitted and one spare; type must match the selected holder. Final rating to be rechecked against measured lamp current during bench commissioning. | _TBD_ |
| 5 V / GND distribution connectors | 2 | **OPEN — BUY** | Two three-way lever connectors, preferred Wago 221-413 or equivalent: one for +5 V and one for GND. | _TBD_ |
| 22–24 AWG stranded power wire and ferrules | 1 lot | **CHECK STOCK** | Orange for +5 V and Brown for GND; ferrules sized for the ESP32 terminal adapter and distribution connectors. | Existing stock / _TBD_ |

## Reused Original Components (Phase 1)

| Item                    | Notes                                                        |
|-------------------------|-------------------------------------------------------------|
| Original on/off switch  | Retained with original solder joints and cable. Low-voltage logic input only (Red/Green). Not switching mains. |
| Original selector PCB   | **Retained** as mechanical carrier for the interlocked selector (ADR-0001). Not disposable. |
| Original source buttons | VHF, MW, LW, Gram wired as inputs; **SW deferred / no function** (ADR-0004). |
| Original Stereo/Mono control | Retained mechanically, **unwired**, decorative in Phase 1 (ADR-0005). |
| Original Decca knobs    | Retained via mechanical adaptor strategy (see `mechanical/Knob Adaptors/`). |

## Audio Path / Phase 2

| Item | Qty | Decision / procurement status | Notes | Source |
|------|-----|-------------------------------|-------|--------|
| WiiM Pro | 1 | **LOCKED — NOT ACQUIRED** | Networked streamer/source. ESP32 local-API integration for source selection, volume and metadata. Continuously powered with automatic standby. Do not substitute WiiM Amp / Amp Pro without a new ADR. | _TBD / price watch active_ |
| Fosi Audio ZA3 | 1 | **LOCKED — NOT ACQUIRED** | Stereo power amplifier. WiiM Pro line output feeds the ZA3; its gain/volume becomes a commissioning ceiling and its operating state is controlled by the 12 V trigger. | _TBD / price watch active_ |
| Passive speakers | 2 | **OPEN — SELECTION TRACKED SEPARATELY** | Driven by the ZA3. Final choice must meet the cabinet fit and condition limits. | _TBD_ |
| ZA3 12 V trigger driver and source | 1 | **OPEN — DESIGN / SELECT** | ESP32-controlled transistor/MOSFET or isolated interface plus suitable 12 V source. Exact circuit and GPIO require selection and bench verification. | _TBD_ |
| ZA3 trigger plug / lead | 1 | **OPEN — SELECT WITH DRIVER** | Match the ZA3 trigger connector and confirmed polarity; length follows final equipment placement. | _TBD_ |
| Stereo RCA interconnect | 1 | **OPEN — BUY LATER** | WiiM Pro line output to ZA3 input; choose length after internal placement is fixed. | _TBD_ |
| Speaker cable / internal harness | 1 set | **OPEN — BUY LATER** | ZA3 to passive speakers; conductor size, length and terminations follow final placement and speaker selection. | _TBD_ |
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

- Wire per the colour standard in `docs/Wiring.md` (Brown GND, Red 3.3 V, Orange 5 V, White signal), except the installed H4 OLED loom: Orange = SDA and Yellow = SCL; H4 Orange must never be connected to 5 V
- Removable connectors at the controller end (harnesses H1–H6)
- Heat-shrink, solder, ferrules and strain-relief materials
