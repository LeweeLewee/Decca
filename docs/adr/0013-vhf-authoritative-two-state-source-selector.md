# ADR-0013: Use VHF as the authoritative two-state source selector

## Status
Accepted

## Date
2026-08-30

## Supersedes
ADR-0011

## Context

Installed testing showed that the original selector mechanism does not provide
a dependable Gram-only state as assumed by ADR-0011. VHF is the only position
that produces a reliable active contact at the ESP32. The interlock reliably
releases VHF when any other source button is selected.

## Decision

Use the active-low contact on GPIO23 as the sole VHF state:

- VHF closed/latched = **Digital Streamer**.
- VHF open/released = **Vinyl**; SW, MW, LW and Gram all produce this state by
  releasing VHF and have no individual software identity.
- Source is derived from the physical VHF state at boot and is not persisted.
- Phase 2 maps VHF to phone-controlled digital playback and released VHF to the
  WiiM Line-In used by Vinyl.

GPIO16, GPIO17 and GPIO18 remain released. The selector PCB remains the original
mechanical carrier. A replacement button panel remains a deferred fallback.

## Verification

The fitted unit physically accepted both transitions. On-target button tests
cover debounce, bounce rejection, hold suppression, open/closed source mapping,
event ordering and boot state. Production serial reports the derived source and
the OLED retains it as the normal dashboard until metadata or a control overlay
takes priority.
