# Revision History

Chronological log of meaningful changes across firmware, hardware, and
mechanical design. Firmware release detail belongs in Git tags/releases; this
document captures cross-cutting milestones and hardware/mechanical revisions
that source control alone does not express well.

## Format

`YYYY-MM-DD` — _Area_ — Summary (author)

- **Area** is one of: Firmware, Hardware, Mechanical, Docs, Project.
- Keep entries short; link to issues/PRs or `hardware/` revisions where useful.

## Log

| Date       | Area    | Summary                                  |
|------------|---------|------------------------------------------|
| _TBD_      | Project | Repository foundation created            |
| _TBD_      | Docs    | Specification baselined (v0.1)           |
| _TBD_      | Docs    | Phase 1 wiring facts documented; Wiring, Hardware Architecture, Parts List, Firmware Architecture, README and Specification (v0.2) updated; ADR-0001..0006 added. Proposed GPIOs labelled proposed. |
| 2026-07-26 | Firmware | Reconciled named firmware pin constants with the proposed Phase 1 wiring map; assignments remain unverified. |
| 2026-07-26 | Firmware | Reconciled source, button, lighting, and shared-state contracts with the confirmed Phase 1 controls. |
| 2026-07-26 | Firmware | Implemented versioned settings persistence and behavioural NVS round-trip coverage (Specification v0.3). |
| 2026-07-26 | Firmware | Implemented board initialisation for assigned Phase 1 inputs, ADC1, I²C and safe-off dial-lighting PWM (Specification v0.4); all GPIO assignments remain proposed. |

## Hardware Revisions

| Rev | Date  | Change                          | Notes |
|-----|-------|---------------------------------|-------|
| A   | _TBD_ | Initial design                  |       |

## Mechanical Revisions

| Rev | Date  | Part / Change                   | Notes |
|-----|-------|---------------------------------|-------|
| A   | _TBD_ | Initial knob adaptor design     |       |
