# ADR-0004: Reuse VHF, MW, LW and Gram; defer SW

## Status
Superseded by ADR-0011 on 2026-08-29

## Context
The fascia selector order is VHF, SW, MW, LW, Gram. Bench investigation of the
retained selector PCB (ADR-0001) found usable contact pairs for VHF, MW, LW and
Gram. A **unique SW-only** contact pair could not be found: the pair that closed
for SW also switched with Gram.

## Decision
Wire and use **VHF, MW, LW and Gram** as four independent low-voltage GPIO inputs
(internal pull-ups, software debounce). **SW is intentionally NO FUNCTION** in the
first pass. No microswitch workaround is added in the current design. Final
Phase 2 WiiM source mappings remain configurable in software.

Current intended mapping direction (Phase 2, not binding):
- VHF → streaming / internet radio
- Gram → vinyl / WiiM Line-In
- MW, LW → presets or alternative streaming functions
- SW → deferred

## Consequences
- Only four of five buttons are electrically available in Phase 1.
- Documentation must not claim all five buttons work, nor that SW has a Phase 1
  function.
- Revisiting SW later would require a hardware change and a new ADR.

> Historical record only. The four-input decision was superseded after the old
> PCB proved unreliable for repeated soldering and connection.
