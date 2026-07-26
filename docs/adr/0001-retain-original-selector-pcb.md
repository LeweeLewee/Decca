# ADR-0001: Retain the original selector PCB as mechanical carrier

## Status
Accepted

## Context
The radio/source button bank uses an interlocked mechanical selector. The
original PCB is the physical carrier and alignment structure for that interlock
mechanism, not merely an electrical board. Removing or replacing it would mean
re-engineering the interlock itself.

## Decision
Retain the original selector PCB in place as the mechanical carrier for the
interlocked selector mechanism. It is not treated as disposable and is not
removed or replaced in Phase 1.

## Consequences
- The interlocked feel and fascia behaviour are preserved.
- Wiring taps existing contact pairs on the retained PCB (see ADR-0004).
- Available contacts are constrained by the original design, which directly
  causes the SW limitation recorded in ADR-0004.
