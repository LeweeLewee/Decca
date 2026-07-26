# Parts List

> **Status:** active. Human-readable summary; the formal BOM lives in
> `hardware/BOM/`. Reflects the confirmed Phase 1 build.

## Electronics (Phase 1)

| Item                  | Qty | Spec / Notes                                              | Source |
|-----------------------|-----|-----------------------------------------------------------|--------|
| ESP32 DevKit          | 1   | Dual-core, Wi-Fi, ADC1, LEDC PWM. Control/UI only, no audio. | _TBD_ |
| Potentiometer, 10 kΩ linear | 4 | Position sensors (Balance, Treble, Bass, Volume). Not in audio path. | _TBD_ |
| OLED display          | 1   | 1.3-inch, 128×64, I²C, SH1106/SSD1306-compatible          | _TBD_  |
| N-channel MOSFET      | 1   | Logic-level; switches 5 V dial lighting under ESP32 PWM   | _TBD_  |
| Warm-white LED lighting | 1 set | 5 V; dial illumination                                  | _TBD_  |
| Power supply / rails  | 1   | 5 V rail; 3.3 V from board regulator                      | _TBD_  |

## Reused Original Components (Phase 1)

| Item                    | Notes                                                        |
|-------------------------|-------------------------------------------------------------|
| Original on/off switch  | Retained with original solder joints and cable. Low-voltage logic input only (Red/Green). Not switching mains. |
| Original selector PCB   | **Retained** as mechanical carrier for the interlocked selector (ADR-0001). Not disposable. |
| Original source buttons | VHF, MW, LW, Gram wired as inputs; **SW deferred / no function** (ADR-0004). |
| Original Stereo/Mono control | Retained mechanically, **unwired**, decorative in Phase 1 (ADR-0005). |
| Original Decca knobs    | Retained via mechanical adaptor strategy (see `mechanical/Knob Adaptors/`). |

## Streamer (Phase 2)

| Item      | Qty | Notes                                              | Source |
|-----------|-----|----------------------------------------------------|--------|
| WiiM Pro  | 1   | Networked source; local API (source, volume, metadata) | _TBD_ |

## Mechanical / Fasteners

- Knob adaptors (printed — see `mechanical/Knob Adaptors/`)
- Display mount / bezel
- Standoffs, screws, brackets

## Consumables / Harness

- Wire per the colour standard in `docs/Wiring.md` (Brown GND, Red 3.3 V, Orange 5 V, White signal)
- Removable connectors at the controller end (harnesses H1–H5)
- Heat-shrink, solder, strain-relief materials
