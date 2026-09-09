# ADR-0016: Finalise controller GPIO routing

## Status
Accepted

## Date
2026-09-08

## Supersedes
The GPIO-routing portions of ADR-0003, ADR-0013, ADR-0014 and ADR-0015. Their
logical behaviours and historical physical evidence remain valid.

## Context

Physical reconciliation of the installed ESP32 terminal adapter established
that the DFR0457 lighting control is on GPIO18/D18, not the historical
GPIO25/D25 route described by the interim PR. The retained controls also need
to terminate on one accessible side of the adapter. GPIO14, GPIO25 and GPIO26
are ordinary digital inputs with internal pull-ups and avoid excluded strapping
pins GPIO0, GPIO2, GPIO5, GPIO12 and GPIO15.

## Decision

- On/off uses GPIO14/D14 with its internal pull-up: closed/LOW is ON and
  open/HIGH is STANDBY.
- VHF uses GPIO26/D26 with its internal pull-up: closed/LOW is Digital Streamer
  and open/HIGH is Vinyl.
- Stereo/Mono uses GPIO25/D25 with its internal pull-up: open/HIGH requests
  lights on and closed/LOW requests lights off.
- The installed DFR0457 dial-light PWM uses GPIO18/D18 at 1 kHz. Firmware takes
  GPIO18 low at the earliest setup opportunity before attaching LEDC at duty 0.
- GPIO13, GPIO17, GPIO19 and GPIO23 are released. The ZA3 trigger remains TBD.

Firmware v0.27.3 at commit `0a4d3bd` implements this map. The build and
authenticated OTA completed successfully, and the ESP32 returned at
`decca.local` / `192.168.1.79`. Owner testing accepted the routing and firmware
logic. The retained Stereo/Mono switch has a separate contact fault tracked as
HW-SW-01.

## Consequences

- GPIO14, GPIO18, GPIO25 and GPIO26 are reserved for their assigned functions.
- Historical D19 on/off, D23 VHF, TX2/D17 Stereo/Mono and D25 PWM results remain
  valid records for their earlier configurations.
- Repairing the physical Stereo/Mono switch is required before its end-to-end
  Mono/off transition can be accepted; no firmware polarity change is required.
