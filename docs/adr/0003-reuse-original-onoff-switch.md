# ADR-0003: Reuse the original on/off switch and cable as a low-voltage input

## Status
Accepted

## Context
The original Decca on/off switch, its original solder joints, and its original
cable are in good order and part of the authentic user experience. It is a simple
open/close switch with active conductors Red and Green.

## Decision
Reuse the original switch and cable as a **low-voltage logic input** to the ESP32.
Confirmed interface: Red → ESP32 GPIO19 input with **internal pull-up enabled**;
Green → GND. Physical acceptance on 2026-08-30 established closed/active-low as
logical ON and open as logical STANDBY.

## Consequences
- The switch **must not** switch 230 V mains; it is logic-level only.
- The original Red/Green conductors are documented as an **exception** to the
  general wiring colour standard and are not recoloured (see docs/Wiring.md).
- GPIO19/D19 is bench-verified in both switch positions. The firmware's `power`
  module owns the logical state without owning the GPIO; `main` coordinates the
  debounced input with display and later power-sequence outputs.
