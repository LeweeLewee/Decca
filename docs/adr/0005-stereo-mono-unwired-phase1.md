# ADR-0005: Leave Stereo/Mono unwired in Phase 1

## Status
Accepted

## Context
The Stereo/Mono control is present on the fascia. It has no confirmed Phase 1
role, and the ESP32 does not handle audio, so any stereo/mono behaviour would be
a downstream or future concern.

## Decision
Retain the Stereo/Mono control **mechanically** but leave it **unwired** and
**decorative** in Phase 1. No function is assigned. Possible future use is
deferred.

## Consequences
- No GPIO or ADC resource is allocated to it in Phase 1.
- Assigning a function later requires wiring, a pin allocation, and a new ADR.
