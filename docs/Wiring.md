# Wiring

> **Status:** placeholder. This is the authoritative interconnect reference.

Records every physical connection so the build is reproducible and the firmware
pin map (`src/hardware.h`) always matches reality.

## Pin Map

Keep this table in sync with `src/hardware.h`. If they disagree, this document
and the header must be reconciled before any build.

| Signal            | ESP32 Pin | Type      | Notes                     |
|-------------------|-----------|-----------|---------------------------|
| _Power button_    | _TBD_     | Digital in| Pull-up, debounced        |
| _Source button_   | _TBD_     | Digital in| Pull-up, debounced        |
| _Volume pot_      | _TBD_     | ADC       | Confirm ADC1 channel      |
| _Tone pot_        | _TBD_     | ADC       | Confirm ADC1 channel      |
| _Dial LEDs_       | _TBD_     | PWM       | LEDC channel              |
| _Cabinet LEDs_    | _TBD_     | PWM       | LEDC channel              |
| _OLED SDA_        | _TBD_     | I²C       |                           |
| _OLED SCL_        | _TBD_     | I²C       |                           |

## Harnesses
- Connector pinouts
- Wire gauge and colour coding
- Strain relief and routing inside the cabinet

## Power Distribution
- Rails and where each is tapped
- Fusing / protection

## Diagrams
- Source diagrams in `hardware/Wiring/`.
