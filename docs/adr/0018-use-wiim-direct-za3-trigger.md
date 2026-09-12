# ADR-0018: Use the WiiM Pro trigger output for the ZA3

## Status
Accepted

## Context
ADR-0010 correctly locked the WiiM Pro, Fosi Audio ZA3 and continuously powered
system architecture, but assumed that the ESP32 needed to generate the ZA3
12 V trigger through a custom driver. The acquired WiiM Pro itself provides a
12 V trigger output, while the ZA3 provides a trigger input. Keeping the ESP32
in this electrical path would add a driver, GPIO, 12 V source and failure mode
without improving the user behaviour.

## Decision
- Connect the WiiM Pro trigger output directly to the Fosi Audio ZA3 trigger
  input with the correct 2.5 mm-to-3.5 mm trigger lead/adaptor.
- The ESP32 does not connect electrically to, source or sense the 12 V trigger.
- The WiiM remains continuously powered. Its playback/standby behaviour controls
  the ZA3 operating state through the direct trigger connection.
- Prove RCA audio manually before adding the trigger, then bench-verify polarity,
  wake, standby and silence before final installation.

## Consequences
- The custom ESP32 trigger driver, separate 12 V trigger source and trigger GPIO
  are removed from the BOM and wiring design.
- The front-panel OFF command stops WiiM playback. WiiM automatic standby and
  trigger behaviour then place the ZA3 into standby; the exact delay is accepted
  by physical test rather than assumed in firmware.
- ADR-0010 remains accepted for amplifier choice, signal path and system-state
  architecture, but its custom-trigger-driver clauses are superseded by this ADR.
