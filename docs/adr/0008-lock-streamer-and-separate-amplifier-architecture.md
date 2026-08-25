# ADR-0008: Lock WiiM Pro with separate power amplification

## Status
Accepted

## Context
The Decca restoration needs a networked streamer that the ESP32 can control while
keeping all audio processing and amplification outside the controller. Earlier
project work considered a WiiM Pro feeding a separate stereo amplifier, including
a Fosi V3 and later used conventional hi-fi amplifiers. Dual-mono/monoblock
amplification was also considered.

A later discussion incorrectly conflated the selected WiiM Pro with the integrated
WiiM Amp Pro. This ADR removes that ambiguity from the repository.

## Decision
- The network streamer is **WiiM Pro**.
- The WiiM Pro is a source/streamer only in this build. It feeds a **separate
  analogue power amplifier** via its line-level output.
- The power amplifier then drives the passive speakers.
- The exact power-amplifier model is **not yet locked** and must remain explicitly
  open until a model is selected on the basis of speaker load, available cabinet
  space, thermal behaviour, noise, power requirements and value.
- **Fosi V3** remains a previously recommended candidate, not a final selection.
- A suitable **used conventional stereo amplifier** remains an allowed candidate.
- **Dual monoblocks are rejected for the current build** because their added
  cost, packaging and complexity are not justified by the likely audible benefit.
- WiiM Amp, WiiM Amp Pro, or another integrated streaming amplifier must **not**
  be substituted for the WiiM Pro + separate-amp architecture without a new ADR.

## Locked signal path

`WiiM Pro -> separate stereo power amplifier -> passive speakers`

The ESP32 communicates with the WiiM Pro over the local network for control and
metadata only. It does not carry or process audio.

## Consequences
- Documentation and BOMs must name **WiiM Pro** specifically.
- The amplifier BOM line must remain `model open` until a separate amplifier
  selection is explicitly accepted.
- Firmware can target the WiiM Pro local API without depending on the eventual
  power-amplifier model.
- Physical layout and power design must reserve for separate streamer and
  amplifier hardware rather than assuming an integrated WiiM amplifier.
