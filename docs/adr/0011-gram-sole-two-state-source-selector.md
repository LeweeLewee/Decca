# ADR-0011: Use Gram as the sole two-state source selector

## Status
Accepted

## Date
2026-08-29

## Context
Repeated soldering onto the original selector PCB is proving unreliable. The
Gram contact pair has already passed bench verification, while depending on the
other old-board contacts adds disproportionate build risk. The interlocked
mechanism still reliably releases Gram when another fascia button is pressed.

## Decision
Use only the verified right-hand Gram dry-contact pair as an ESP32 input on
GPIO23 with the internal pull-up and software debounce.

- Gram closed/latched = **Vinyl**; Phase 2 selects WiiM Line-In.
- Gram open/released = **Digital Streamer**; digital service, station, playlist
  and track selection remain controlled from the phone/WiiM app.
- VHF, SW, MW and LW have no individual electrical or software function. They
  may mechanically release Gram through the retained interlock.
- GPIO16, GPIO17 and GPIO18 are released and the corresponding old-board
  conductors are disconnected and insulated.
- The original PCB remains as the mechanical carrier under ADR-0001.
- A purpose-built replacement button panel is deferred as a fallback.

This decision supersedes ADR-0004.

## Consequences
- The front panel provides simple, reliable Vinyl/Digital selection.
- The former LW solder repair is no longer required.
- Digital content choice is intentionally delegated to the phone.
- Source is derived from the physical Gram state at boot and is not persisted.
- Further front-panel presets require a new button panel and a new decision.
