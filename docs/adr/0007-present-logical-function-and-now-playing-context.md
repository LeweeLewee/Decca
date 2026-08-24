# ADR-0007: Present logical function and now-playing context

## Status
Accepted

## Context
The retained source buttons are labelled VHF, MW, LW and Gram, but those fascia
labels identify physical controls rather than necessarily describing their
configured WiiM functions. Presenting only `VHF`, for example, would conceal a
mapping such as BBC Radio 2. The 128×64 monochrome OLED must also communicate
live control changes clearly without permanently displacing useful playback
information.

WiiM metadata and configurable source mappings remain Phase 2 capabilities
under ADR-0006. The ESP32 handles control and user interface only; it must not
receive, process or carry audio.

## Decision
- Display the mapped logical function prominently. Show the originating legacy
  fascia button only as secondary context in parentheses, for example
  `BBC RADIO 2` followed by `(VHF BUTTON)`.
- While a streaming source is playing, use available now-playing information as
  the default on-state view: mapped function/source, song title and artist. If
  metadata is absent, fall back to the mapped function and never retain stale
  track information.
- When a pot is adjusted, temporarily replace the default view for approximately
  2 s with the control name, a level bar and percentage. Confirm a newly selected
  mapped function transiently before returning to the default view.
- Replace the static startup frame with a short, approximately 1 s monochrome
  Decca-logo animation of 4–8 frames. It must remain non-blocking.
- Keep SW explicitly unavailable. It is not assigned a displayable function.
- Keep the `display` module independent. `main` supplies coherent display state;
  the display does not read buttons, pots or the WiiM interface directly.

## Consequences
- Phase 1 display work adds the startup animation and transient control
  presentation without introducing any network dependency.
- Mapped function names and now-playing metadata are activated only with the
  Phase 2 WiiM interface. The display contract may be prepared earlier, but it
  must not perform network requests itself.
- Source-button labels remain useful for orientation and diagnostics but are not
  the primary description of system function.
- Metadata loss or WiiM unavailability produces a deterministic mapped-function
  fallback, preserving local operation.
- The existing static startup/dashboard implementation must be revised and its
  behavioural tests updated before ADR-0007 is considered implemented.
