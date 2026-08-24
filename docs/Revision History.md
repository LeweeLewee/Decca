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
| 2026-07-26 | Firmware | Implemented four-channel ADC1 pot sampling, normalisation, smoothing, deadband, calibration/inversion and behavioural tests (Specification v0.5); added the bench-verification procedure. |
| 2026-08-24 | Firmware | Routed the physical pot snapshot through Unity diagnostics so PlatformIO retains the four raw ADC readings during bench verification. |
| 2026-08-24 | Hardware | Bench-verified Volume GPIO32, Bass GPIO33, Treble GPIO34 and Balance GPIO35 across the full 0–4095 ADC range; default calibration retained (Specification v0.6). |
| 2026-08-24 | Firmware | Assigned proposed active-low source inputs VHF GPIO16, MW GPIO17, LW GPIO18 and Gram GPIO23 with internal pull-ups (Specification v0.7); assignments remain unverified. |
| 2026-08-24 | Firmware | Implemented 25 ms active-low debounce, stable latching state, fixed press-event queue, behavioural coverage and source-button bench diagnostics (Specification v0.8). |
| 2026-08-24 | Docs | Recorded the locked H3 colour code and the controller board labels for the proposed source-button GPIOs (HW-06, ADR-0004). |
| 2026-08-24 | Docs | Corrected H3 from an unsupported common-return colour map to four photographed, isolated two-wire pairs in provisional physical order; bench verification remains required (HW-06, ADR-0004). |
| 2026-08-24 | Hardware | Bench-verified VHF Yellow/Green on GPIO16, MW Purple/Blue on GPIO17 and Gram Yellow/Green on GPIO23; corrected LW to Yellow/Orange and retained GPIO18 as proposed pending solder repair and retest (Specification v0.9, HW-06, ADR-0004). |
| 2026-08-24 | Firmware | Implemented safe-off dial PWM, persisted idle target, non-blocking 10 ms fade steps and behavioural/physical test coverage (Specification v0.10, FR-LGT-01..04, HW-05). GPIO25 remains proposed pending bench verification. |
| 2026-08-24 | Firmware | Locked the purchased Pi Hut SH1106 panel and implemented non-blocking startup, standby/dashboard, status, SW-unavailable and diagnostic frames with change-only refresh and behavioural/physical coverage (Specification v0.11, FR-DSP-01/02/05, IF-02). GPIO21/22 remain proposed pending bench verification. |
| 2026-08-24 | Docs | Locked the revised display presentation contract: animated Decca startup, transient control overlays, mapped function prioritised over legacy button label, and Phase 2 now-playing metadata with mapped-function fallback (Specification v0.12, ADR-0007, FR-DSP-02/03/06/07). |

## Hardware Revisions

| Rev | Date  | Change                          | Notes |
|-----|-------|---------------------------------|-------|
| A   | _TBD_ | Initial design                  |       |

## Mechanical Revisions

| Rev | Date  | Part / Change                   | Notes |
|-----|-------|---------------------------------|-------|
| A   | _TBD_ | Initial knob adaptor design     |       |
