# ADR-0009: Omit legacy button labels from user-facing display views

## Status
Accepted

## Context
ADR-0007 established that the mapped logical function is the primary display
identity and the originating VHF, MW, LW or Gram label is secondary context.
Physical testing on the 128×64 SH1106 showed that the parenthesised legacy
label consumes a complete text row without adding enough value: the user has
just operated the physical button and the mapped function is the information
needed from the screen.

## Decision
- Do not render legacy fascia button labels in the normal dashboard,
  now-playing view or mapped-function confirmation.
- Use the reclaimed space for clearer separation of mapped function, metadata
  and control values.
- Retain physical source identity in the supplied state for coordination,
  testing and diagnostics; this decision changes presentation only.
- Retain every other ADR-0007 decision, including the mapped-function priority,
  metadata fallback, transient control view, startup animation and SW handling.

## Consequences
- The display communicates system function rather than repeating a control
  label already visible on the fascia.
- Future source-button mappings remain configurable and do not require display
  layout changes.
- ADR-0009 supersedes only ADR-0007's instruction to show the originating
  legacy button as secondary context. ADR-0007 otherwise remains accepted.
