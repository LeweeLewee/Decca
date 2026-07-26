# ADR-0002: Use four 10k analogue potentiometers as position sensors

## Status
Accepted

## Context
The music centre has four rotary controls (Balance, Treble, Bass, Volume). The
ESP32 provides user-interface control only and must not carry or process audio.
The original knobs are to be retained.

## Decision
Use four modern **10 kΩ linear** potentiometers as **position sensors** read by
the ESP32 ADC. Original Decca knobs are retained via a mechanical adaptor
strategy. Pots are wired GND / wiper / 3.3 V (Brown / White / Red) and read on
**ADC1** (Wi-Fi in Phase 2 makes ADC2 unavailable). Firmware provides
calibration, smoothing, deadband, optional inversion, and stable display updates.

## Consequences
- Pots are out of the audio path entirely; audio remains fully analogue.
- ADC1 pin choice is constrained by the Wi-Fi requirement (Specification HW-02).
- Proposed pins (Volume GPIO32, Bass GPIO33, Treble GPIO34, Balance GPIO35)
  remain **proposed** until bench-verified.
