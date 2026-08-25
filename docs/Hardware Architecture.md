# Hardware Architecture

> **Status:** active. Reflects the confirmed Phase 1 physical build plus the
> locked Phase 2 audio architecture. Pot inputs GPIO32–35 are bench-verified;
> remaining ESP32 assignments are **(proposed)** or unassigned. See
> `docs/Wiring.md` for the authoritative controller interconnect detail and
> ADR-0008 for the streamer/amplifier decision boundary.

Describes the electrical system: the boards, how power flows, and how the ESP32
connects to the front panel, display, lighting, streamer and external audio path.

## Scope Boundary

The ESP32 is a **control and user-interface system only**. It **must not process
or carry audio**. All potentiometers are position sensors read by the ADC; the
audio signal path is separate from the controller.

## System Block Diagram

```
                 ┌──────────────────────────────────────────┐
                 │                ESP32 DevKit               │
                 │        (control + UI only, no audio)      │
                 └───┬───────┬───────┬────────┬───────┬──────┘
       ADC1 (H1) │       │ H2    │ H3     │ H4    │ H5 (PWM)
        4× 10k   │       │ on/off│ source │ I²C   │ MOSFET gate
     ┌───────────┴──┐ ┌──┴───┐ ┌─┴─────┐ ┌┴─────┐ ┌┴──────────┐
     │ Balance/Treble│ │orig. │ │VHF MW │ │ OLED │ │ 5V warm   │
     │ Bass/Volume   │ │switch│ │LW Gram│ │128x64│ │ dial LEDs │
     │ (position)    │ │Red/Grn│ │(SW n/f)│ │ SH1106│ │ (N-ch FET)│
     └───────────────┘ └──────┘ └───────┘ └──────┘ └───────────┘

                  local network control / metadata
                 ESP32  <-------------------->  WiiM Pro
                                                   │
                                                   │ line-level audio
                                                   ▼
                                      Separate stereo power amp
                                                   │
                                                   ▼
                                           Passive speakers
```

## Locked Audio Architecture

The audio-path architecture is locked by ADR-0008 as:

`WiiM Pro -> separate stereo power amplifier -> passive speakers`

- **Streamer:** WiiM Pro, specifically. This is a locked model decision.
- **Power amplification:** separate from the WiiM Pro. This architecture is locked.
- **Power-amplifier model:** intentionally **open** pending final selection.
  Fosi V3 remains a candidate; used conventional stereo amplification also remains
  valid for assessment.
- **Dual monoblocks:** rejected for the current build unless requirements change.
- **Integrated WiiM amplifier variants:** WiiM Amp / Amp Pro are not substitutes
  for the selected architecture without a new ADR.
- **Cabinet thermal constraint:** none for normal hi-fi amplifier selection. The
  Decca cabinet has ample rear ventilation, so thermal performance is not a
  differentiating selection criterion beyond the amplifier's normal operating
  requirements.
- The ESP32 communicates with the WiiM Pro only for control and metadata. It never
  sits in the audio signal path.

## Power

- Rails: **5 V** (lighting, board input) and **3.3 V** (ESP32, pot references,
  logic). 3.3 V is taken from the board regulator.
- ESP32 and dial-lighting **grounds are common**.
- No mains switching by the ESP32 (see Controller / on-off below).
- Streamer and power-amplifier mains/power arrangements are part of the separate
  audio subsystem and will be finalised alongside the amplifier model and physical
  installation. The cabinet's existing rear ventilation is adequate and imposes
  no additional thermal-design restriction.

## Controller

- **ESP32 DevKit** (dual-core, Wi-Fi, LEDC PWM, ADC).
- **ADC1 is used for all analogue inputs** because Wi-Fi is enabled in Phase 2
  and **ADC2 is unavailable while Wi-Fi is active** (Specification `HW-02`).
- Strapping pins (0, 2, 5, 12, 15) are avoided for driven/reset-sensitive lines
  (`HW-03`). GPIO34–39 are input-only with no internal pull-ups (`HW-04`).

## Inputs

### Potentiometers (H1)
Four **10 kΩ linear** pots (Balance, Treble, Bass, Volume) wired GND / wiper /
3.3 V (Brown / White / Red). Wipers read on ADC1. Firmware applies calibration,
smoothing, deadband, and optional inversion (see Firmware Architecture).
Bench-verified pins: Volume GPIO32, Bass GPIO33, Treble GPIO34, Balance GPIO35.
Each channel measured 0 anticlockwise, approximately 2047 at centre, and 4095
clockwise on 2026-08-24, so the default 0–4095 calibration remains applicable.

### On/off switch (H2)
Retained original switch and cable, active conductors **Red** and **Green**. A
simple open/close contact read as a **low-voltage digital input** with the ESP32
**internal pull-up** enabled (proposed GPIO19). **Not a mains switch.** Optional
firmware inversion after bench testing.

### Source button bank (H3)
Original interlocked selector on its **original PCB**, which is retained as the
**mechanical carrier** for the mechanism (ADR-0001). Four working contact pairs
(VHF, MW, LW, Gram) are read as low-voltage digital inputs with internal pull-ups
and software debounce. **SW has no unique contact and is deferred (no function in
Phase 1).** Inputs are VHF GPIO16, MW GPIO17, LW GPIO18 and Gram GPIO23; all
avoid strapping pins. GPIO16, GPIO17 and GPIO23 are bench-verified. GPIO18
remains proposed pending repair and retest of the LW Yellow/Orange contact pair.
The Stereo/Mono control is retained but **unwired** (ADR-0005).

## Outputs

### OLED display (H4)
Purchased Pi Hut 1.3-inch white 128×64 SH1106 I²C panel (SKU 105630), powered
from 3.3 V at address 0x3C. Proposed SDA GPIO21 / SCL GPIO22 remain unverified.

### Dial lighting (H5)
5 V warm-white LEDs driven via a **logic-level N-channel MOSFET**, gate driven by
ESP32 **PWM (LEDC)**, proposed GPIO25. Common ground with the ESP32. Behaviours:
fade up/down, configurable idle brightness, safe boot state.

## Networking (Phase 2)

Wi-Fi is used only in Phase 2 for **WiiM Pro local API** integration (source
selection, volume, metadata/playback state). This is the reason ADC1 is mandated
for all analogue inputs. See Firmware Architecture → WiiM interface, ADR-0006
and ADR-0008.

## Revisions

Track board/electrical revisions in [Revision History](Revision History.md).
