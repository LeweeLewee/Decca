# ADR-0014: Use TX2 Stereo/Mono as the dial-lighting command

## Status
Accepted

## Context
The original Stereo/Mono control is visible, mechanically useful and no longer
needs to represent audio processing because the ESP32 does not carry audio. A
simple period-appropriate lighting control gives it a clear function. GPIO5 was
rejected because it is an ESP32 strapping pin. TX2/GPIO17 is available and
supports an internal pull-up.

## Decision
Connect the isolated Stereo/Mono contact between TX2/GPIO17 and GND. Configure
GPIO17 as `INPUT_PULLUP` and debounce it with the other retained controls.
The installed contact is open/HIGH in Stereo and closed/LOW in Mono. Stereo
requests dial lights on; Mono requests them off. Expose the stable request from the buttons module without directly calling
the lighting module.

## Consequences
- ADR-0005 is superseded.
- No 3.3 V or 5 V wire is used at the switch.
- GPIO17 is no longer available for other functions.
- This decision assigns and implements the input only. GPIO25, the MOSFET and
  the lamp load remain disabled until their separate commissioning procedure.
- Wiring polarity and both stable states require physical acceptance before the
  input is marked bench-verified.
