# ADR-0003: Reuse the original on/off switch and cable as a low-voltage input

## Status
Accepted

## Context
The original Decca on/off switch, its original solder joints, and its original
cable are in good order and part of the authentic user experience. It is a simple
open/close switch with active conductors Red and Green.

## Decision
Reuse the original switch and cable as a **low-voltage logic input** to the ESP32.
Proposed interface: Red → ESP32 GPIO19 input with **internal pull-up enabled**;
Green → GND. Logical inversion may be applied in firmware after bench testing.

## Consequences
- The switch **must not** switch 230 V mains; it is logic-level only.
- The original Red/Green conductors are documented as an **exception** to the
  general wiring colour standard and are not recoloured (see docs/Wiring.md).
- GPIO19 assignment remains **proposed** until bench-verified.
