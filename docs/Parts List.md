# Parts List

> **Status:** active. Human-readable summary; the formal BOM lives in
> `hardware/BOM/`. Reflects the confirmed build decisions. Where a component
> model is not yet selected, that is stated explicitly rather than inferred.

## Electronics (Phase 1)

| Item                  | Qty | Spec / Notes                                              | Source |
|-----------------------|-----|-----------------------------------------------------------|--------|
| ESP32 DevKit          | 1   | Dual-core, Wi-Fi, ADC1, LEDC PWM. Control/UI only, no audio. | _TBD_ |
| Potentiometer, 10 kΩ linear | 4 | Position sensors (Balance, Treble, Bass, Volume). Not in audio path. | _TBD_ |
| OLED display          | 1   | **Purchased:** Pi Hut SKU 105630; 1.3-inch white 128×64 SH1106, four-pin I²C, 3.3 V | The Pi Hut |
| N-channel MOSFET      | 1   | Logic-level; switches 5 V dial lighting under ESP32 PWM   | _TBD_  |
| E10 warm-white LED lamps | 1 set | **5 V, E10 screw-base LED lamps** for the original dial-lighting positions; warm-white output; switched/dimmed together from the 5 V lighting rail via the MOSFET PWM stage. Exact lamp count to follow physical socket count. | _TBD_  |
| Power supply / rails  | 1   | 5 V rail; 3.3 V from board regulator                      | _TBD_  |

## Reused Original Components (Phase 1)

| Item                    | Notes                                                        |
|-------------------------|-------------------------------------------------------------|
| Original on/off switch  | Retained with original solder joints and cable. Low-voltage logic input only (Red/Green). Not switching mains. |
| Original selector PCB   | **Retained** as mechanical carrier for the interlocked selector (ADR-0001). Not disposable. |
| Original source buttons | VHF, MW, LW, Gram wired as inputs; **SW deferred / no function** (ADR-0004). |
| Original Stereo/Mono control | Retained mechanically, **unwired**, decorative in Phase 1 (ADR-0005). |
| Original Decca knobs    | Retained via mechanical adaptor strategy (see `mechanical/Knob Adaptors/`). |

## Audio Path / Phase 2

| Item | Qty | Decision status | Notes | Source |
|------|-----|-----------------|-------|--------|
| WiiM Pro | 1 | **LOCKED** | Networked streamer/source. ESP32 integration via local API for source selection, volume and metadata. **Do not substitute WiiM Amp / Amp Pro without a new ADR.** | _TBD / price watch active_ |
| Separate stereo power amplifier | 1 | **ARCHITECTURE LOCKED; MODEL OPEN** | WiiM Pro line output feeds a separate analogue power amplifier, then passive speakers. Exact amp model is intentionally not yet locked. Fosi V3 was the initial recommendation; used conventional hi-fi amplification was subsequently reopened for comparison. | _TBD_ |
| Monoblock power amplifiers | 2 | **REJECTED for current build** | Considered, but added cost/complexity was not justified for the expected audible benefit in this installation. Revisit only if speaker/amp requirements materially change. | n/a |
| Passive speakers | 2 | **Separate selection** | Driven only by the power amplifier. Speaker selection is outside ESP32 firmware control. | _TBD_ |

**Locked signal architecture:** `WiiM Pro -> separate power amplifier -> passive speakers`.

See ADR-0008 for the decision boundary between the locked architecture and the
still-open amplifier model selection.

## Mechanical / Fasteners

- Knob adaptors (printed — see `mechanical/Knob Adaptors/`)
- Display mount / bezel
- Standoffs, screws, brackets

## Consumables / Harness

- Wire per the colour standard in `docs/Wiring.md` (Brown GND, Red 3.3 V, Orange 5 V, White signal)
- Removable connectors at the controller end (harnesses H1–H5)
- Heat-shrink, solder, strain-relief materials
