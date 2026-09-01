# ADR-0010: Lock Fosi ZA3 and system power-control architecture

## Status
Accepted

## Context
ADR-0008 locked the audio architecture as WiiM Pro feeding a separate stereo
power amplifier, but intentionally left the amplifier model open. Subsequent
review compared the Fosi V3, Fosi ZA3, Fosi V3 Mono pair and Topping alternatives
against price, sound quality, cabinet integration, ESP32 controllability and
standby/power-management behaviour.

The restoration also requires the original Decca on/off control to behave like a
single system power control without putting 230 V mains back through the original
switch.

## Decision
- The stereo power amplifier is **Fosi Audio ZA3**.
- The locked signal path is:

  `WiiM Pro -> Fosi Audio ZA3 -> passive speakers`

- The original Decca on/off switch remains a **low-voltage ESP32 input only**.
- The switch represents requested **system state**, not direct mains isolation.
- The **WiiM Pro remains continuously powered** and uses WiiM automatic standby;
  it is not hard power-cycled from the front-panel switch.
- The **Fosi ZA3 operating state is controlled by its 12 V trigger input**.
- The ESP32 commands that trigger through a dedicated low-voltage driver stage.
  The ESP32 must never source or receive the 12 V trigger directly.
- The exact trigger-driver device, 12 V source and ESP32 GPIO remain open until
  selected and bench-verified.
- No ESP32-controlled 230 V relay is required for the ZA3 under this architecture.
- The ESP32 remains powered when the Decca is logically OFF so it can detect the
  front-panel switch and orchestrate the next startup.
- The OLED is blanked and the dial lamps are faded to zero in the logical OFF
  state.
- User volume is controlled as:

  `Decca volume pot -> ESP32 ADC -> WiiM volume`

  The ZA3's own level control is set during commissioning as a fixed hardware
  ceiling and is not the normal user volume control.

## Locked power-state sequence

### ON
1. ESP32 detects the original Decca switch closing.
2. ESP32 asserts the ZA3 12 V trigger through the driver stage.
3. Dial lamps fade to the stored commissioning brightness.
4. OLED enables and runs the startup/dashboard sequence.
5. WiiM remains physically powered and wakes from automatic standby when playback
   or supported network/control activity requires it.

### OFF
1. ESP32 detects the original Decca switch opening.
2. ESP32 stops playback or sends an appropriate supported WiiM control action where
   useful; WiiM then returns to its own automatic standby behaviour.
3. Dial lamps fade to zero.
4. OLED is blanked.
5. ESP32 removes the ZA3 12 V trigger.
6. ESP32 remains powered awaiting the next switch-on.

## Consequences
- `hardware/BOM/phase2.csv` must name the **Fosi Audio ZA3** as locked.
- The previous Fosi V3 candidate and generic used-amplifier path are superseded for
  this build.
- The power design no longer requires an ESP32-controlled mains relay for the
  amplifier.
- A small 12 V trigger-driver subsystem is now a required hardware item.
- The exact **12 V trigger source, trigger driver and GPIO** remain open
  implementation/procurement decisions.
- The 5 V controller supply was subsequently selected and acquired as a **Phihong
  PSA15R-050P, 5.0 V DC, 3.0 A (15 W)**; current implementation status is tracked
  in `hardware/BOM/phase1.csv`, `docs/Parts List.md` and `docs/Hardware Architecture.md`.
- Firmware must treat the original switch as a system-state transition and
  coordinate ZA3 trigger, lighting, OLED and WiiM behaviour accordingly.
