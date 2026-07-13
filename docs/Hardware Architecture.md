# Hardware Architecture

> **Status:** placeholder. Populate as the electrical design firms up.

Describes the electrical system: what the boards are, how power flows, and how
the ESP32 connects to the front panel, display, and lighting.

## System Block Diagram
_Insert a block diagram (source in `hardware/Schematics/`)._

## Power
- Input and rails (mains → PSU → 5 V → 3.3 V)
- Current budget per rail
- Standby behaviour

## Controller
- ESP32 DevKit: role, why chosen
- Reserved / strapping pins to avoid
- Reference: pin map in `src/hardware.h`

## Inputs
- Buttons: circuit, pull-ups, debounce approach
- Potentiometers: ADC connection, dividers, filtering

## Outputs
- OLED display interface (I²C / SPI)
- Lighting: LED driver / PWM approach

## Networking (Phase 2)
- Wi-Fi usage and WiiM Pro connectivity
- Reference: [Firmware Architecture](Firmware Architecture.md) → WiiM interface

## Revisions
- Track board/electrical revisions in [Revision History](Revision History.md).
