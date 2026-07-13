# Build Guide

> **Status:** placeholder. Populate as the physical build progresses.

Step-by-step guide to reproducing the decca build, from bare cabinet to working
music centre. This document should let a competent maker rebuild the project
from parts.

## 1. Before You Start
- Tools required
- Skills assumed (soldering, basic CAD/printing, PlatformIO)
- Safety notes (mains, dust, original finish)

## 2. Preparing the Cabinet
- Assessment and restoration of the original piece
- What is preserved vs. replaced
- Cleaning and refinishing notes

## 3. Electronics Assembly
- ESP32 and peripheral mounting
- Wiring the front-panel controls
- Power supply and rails
- Cross-references: [Wiring](Wiring.md), [Parts List](Parts List.md)

## 4. Mechanical Fit-Out
- Display mounting behind the dial glass
- Knob adaptors (see `mechanical/Knob Adaptors/`)
- Lighting placement

## 5. Firmware Flashing
- Installing PlatformIO
- First build and upload
- Cross-reference: `README.md` → Development Workflow

## 6. First Power-On
- Bring-up checklist
- Smoke-test procedure
- Common issues

## 7. Commissioning
- Calibrating pots and brightness
- Verifying each control
