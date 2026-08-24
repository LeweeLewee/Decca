# Hardware Architecture

> **Status:** active. Reflects the confirmed Phase 1 physical build. Pot inputs
> GPIO32–35 are bench-verified; remaining ESP32 assignments are **(proposed)**
> or unassigned. See `docs/Wiring.md` for the authoritative interconnect detail.

Describes the electrical system: the boards, how power flows, and how the ESP32
connects to the front panel, display, and lighting.

## Scope Boundary

The ESP32 is a **control and user-interface system only**. It **must not process
or carry audio**. All potentiometers are position sensors read by the ADC; the
analogue audio path is entirely separate and outside the controller.

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
```

## Power

- Rails: **5 V** (lighting, board input) and **3.3 V** (ESP32, pot references,
  logic). 3.3 V is taken from the board regulator.
- ESP32 and dial-lighting **grounds are common**.
- No mains switching by the ESP32 (see Controller / on-off below).

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
1.3-inch 128×64 I²C panel (SH1106/SSD1306-compatible), proposed SDA GPIO21 /
SCL GPIO22.

### Dial lighting (H5)
5 V warm-white LEDs driven via a **logic-level N-channel MOSFET**, gate driven by
ESP32 **PWM (LEDC)**, proposed GPIO25. Common ground with the ESP32. Behaviours:
fade up/down, configurable idle brightness, safe boot state.

## Networking (Phase 2)

Wi-Fi is used only in Phase 2 for **WiiM Pro local API** integration (source
selection, volume, metadata/playback state). This is the reason ADC1 is mandated
for all analogue inputs. See Firmware Architecture → WiiM interface and ADR-0006.

## Revisions

Track board/electrical revisions in [Revision History](Revision History.md).
