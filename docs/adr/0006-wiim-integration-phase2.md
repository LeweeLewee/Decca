# ADR-0006: Keep WiiM Pro integration in Phase 2

## Status
Accepted

## Context
The system must be fully usable locally with no network (Specification FR-SYS-03).
Networked audio via a WiiM Pro adds source selection, volume control, and
metadata/playback-state feedback, but introduces Wi-Fi and network dependencies.

## Decision
Keep **WiiM Pro local API integration in Phase 2**. Phase 1 delivers complete
local control and diagnostics with no network. Phase 2 adds source-selection
commands, volume control, and metadata/playback-state feedback over the WiiM
local API.

## Consequences
- Wi-Fi is a Phase 2 concern, which is the reason all analogue inputs use ADC1
  (ADR-0002, Specification HW-02).
- Loss of the streamer must not impair local control (FR-SYS-05, NFR-09).
- Source-button-to-WiiM mappings are configurable in software (ADR-0004).
