# ADR-0015: Reassign dry-contact inputs for terminal-adapter routing

## Status
Superseded by ADR-0016

## Date
2026-09-08

## Supersedes
ADR-0013 and ADR-0014; their behaviours are retained and only the GPIO routing
changes

## Context

The VHF/source-selector and Stereo/Mono dry contacts were physically accepted
on GPIO23/D23 and GPIO17/TX2 respectively. Their positions on the ESP32 terminal
adapter make the installed wiring unnecessarily difficult to route. GPIO26/D26
and GPIO14/D14 are available ordinary digital inputs with internal pull-ups.
They avoid the excluded strapping pins GPIO0, GPIO2, GPIO5, GPIO12 and GPIO15
and do not conflict with the ADC1 pots, OLED, on/off input or dial-lighting PWM.

## Decision

- Reassign the sole VHF/source-selector input from GPIO23/D23 to GPIO26/D26.
- Reassign the Stereo/Mono input from GPIO17/TX2 to GPIO14/D14.
- Retain active-low operation, internal pull-ups and 25 ms software debounce.
  VHF closed/latched remains Digital Streamer and VHF open/released remains
  Vinyl. Stereo open/high continues to request lights on and Mono closed/low
  continues to request lights off.
- Leave the ZA3 trigger GPIO open/TBD.

The firmware pin map used these assignments as an interim routing proposal.

## Consequences

- GPIO17 and GPIO23 were released by this proposal.
- GPIO26 and GPIO14 were unavailable for other functions while this decision
  was active.
- Historical physical results for the switches remained evidence of their
  behaviour, not verification of the proposed GPIO routing.
- ADR-0016 supersedes this interim route with the physically reconciled map.
