# ADR-0017: Remove dial-lighting fades

## Status
Accepted

## Context
The firmware ramped dial-light PWM by one count every 20 ms, taking about 4.34
seconds to move between off and the normal duty of 217. Installed observation
showed that the LEDs did not produce a useful visible ramp: they stayed at full
brightness and then switched off after the fade interval. This made the
Stereo/Mono and logical power controls appear unresponsive.

## Decision
Remove the lighting fade state machine and timer. Every changed lighting request
is written to PWM immediately:

- logical ON plus Stereo writes the stored normal duty;
- Mono writes duty 0;
- logical standby writes duty 0;
- logical power-on writes the applicable duty.

The existing 25 ms input debounce remains because it suppresses mechanical
contact chatter; it is not a visual transition delay. Safe-off initialization at
duty 0 and the stored commissioning brightness remain unchanged.

## Consequences
- `lighting::setBrightness()` is an immediate operation.
- `lighting::update()`, fade timing constants, target state and clock test hooks
  are removed.
- The lighting tests verify immediate on/off writes and safe initialization.
- The fade-related portions of ADR-0010 and ADR-0014 are superseded.
- Firmware v0.27.4 requires OTA deployment and physical verification.
