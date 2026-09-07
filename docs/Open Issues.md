# Open Issues

This is the canonical short list of unresolved integration issues. Read it with
`docs/Development Handover.md` before continuing work. Historical test passes in
the revision history remain valid records of what was tested at the time, but do
not close a later issue listed here.

## HW-LGT-01 — Final dial-lighting integration acceptance

**Status:** OPEN — DFR0457 installed; flicker, v0.28.0 GPIO18 operation and 85%
fade behaviour physically accepted. WAGO installation, pot-stability,
temperature and current remain.

**Observed:** the previous MOSFET/module path produced visible lamp flicker. With
that path energised, electrical disturbance also caused the display to jump
between pot overlays. The pot behaviour settled after the lighting path was
turned off and discharged. Driving the three lamps directly from the same 5 V
supply produced no visible flicker, isolating the fault to the switching path
rather than the lamps or supply. At a temporary 100% firmware target the pot/UI
disturbance stopped, but lamp flicker remained.

**Selected remedy and current progress:**

- **Complete:** install one DFRobot Gravity MOSFET Power Controller,
  **DFR0457**. The owner reports that the lighting flicker is resolved.
- **Ordered:** Pi Hut pack of three **WAGO 221-415** five-way lever connectors.
  On delivery, use one for the +5 V star point, one for common GND and retain
  one spare.
- Keep the single regulated 5 V supply and common-ground architecture.
- **Complete:** set `decca::hardware::kDialLightingPwmFrequencyHz` to the
  controller's specified 1 kHz limit and restore the existing non-blocking soft
  fade engine. Commit `c6cb9a6` uploaded by authenticated OTA and the ESP32
  returned at `decca.local` after reboot.
- **Complete (2026-09-05):** deploy v0.27.1 at commit `d0b1d3c`. The owner
  approved the 2.2-second firmware-version hold and both approximately
  4.34-second lighting fades, with no flicker reported.

**Locked behaviour:** firmware v0.28.0 reassigns the lighting PWM output from the
previously accepted GPIO25/D25 to the now physically accepted GPIO18/D18. Stereo
open/high requests lights on at the owner-approved
85% / duty 217; Mono closed/low and logical standby request off. Preserve 1 kHz
and the 20 ms/count fades. Firmware drives D18 LOW at the earliest opportunity,
but the owner has deferred the recommended external pull-down; reset-time
safe-off before `setup()` is therefore not guaranteed and needs observation.

**Device state:** the last-known installed image is firmware v0.28.0 from commit
`283d40a`, using 1 kHz PWM and an 85% / duty 217 target with approximately
4.34-second fades. Its authenticated OTA upload succeeded and the device
returned at `decca.local` / 192.168.1.79.

**GPIO transition state:** complete 2026-09-06. Authenticated OTA installed
v0.28.0 with the signal wires disconnected; after confirmed power-off the owner
moved the on/off signal to D26 and DFR0457 PWM to D18, then confirmed correct
operation. D19/D25 remain historical assignments.

**Acceptance required to close:**

1. **Passed:** cold startup showed no unwanted lamp flash before the controlled
   fade.
2. **Passed:** Stereo softly fades to 85% and Mono softly fades fully off in
   approximately 4.34 seconds.
3. **Passed:** no lamp flicker was reported at steady state or through fades.
4. **Open:** install the ordered WAGO 221-415 +5 V and common-GND star points.
5. **Open:** exercise and then release all four pots; confirm the OLED does not
   chatter between control overlays while the lamps are on.
6. **Open:** confirm no abnormal module or wiring temperature and measure the
   installed three-lamp current.
7. **Complete:** physical results are recorded and release v0.28.0 is installed
   by authenticated OTA on the accepted D26/D18 assignments. Close only after
   items 4–6 pass.

**Procurement records:** `hardware/BOM/phase1.csv` and `docs/Parts List.md`.
**Wiring:** `docs/Wiring.md`, H5 and Power Distribution.
