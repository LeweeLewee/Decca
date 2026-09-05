# Open Issues

This is the canonical short list of unresolved integration issues. Read it with
`docs/Development Handover.md` before continuing work. Historical test passes in
the revision history remain valid records of what was tested at the time, but do
not close a later issue listed here.

## HW-LGT-01 — Final dial-lighting stage flickers and disturbs pot UI

**Status:** OPEN — DFR0457 installed; initial steady-light flicker test passed;
85% soft-fade firmware deployed; physical integration acceptance in progress.

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
- Buy the Pi Hut pack of three **WAGO 221-415** five-way lever connectors; use
  one for the +5 V star point, one for common GND and retain one spare.
- Keep the single regulated 5 V supply and common-ground architecture.
- **Complete:** set `decca::hardware::kDialLightingPwmFrequencyHz` to the
  controller's specified 1 kHz limit and restore the existing non-blocking soft
  fade engine. Commit `c6cb9a6` uploaded by authenticated OTA and the ESP32
  returned at `decca.local` after reboot.

**Locked behaviour:** GPIO25/D25 remains the lighting PWM output. Stereo
open/high requests lights on at the owner-approved 85% / duty 217; Mono
closed/low and logical standby request off. Preserve fades and safe-off boot.

**Device state:** the last-known installed image is firmware v0.27.0 at commit
`1ae242e`, using 1 kHz PWM and an 85% / duty 217 target with soft fades. Its
authenticated OTA upload succeeded and the device returned at `decca.local`.
GitHub `main` remains the source of truth.

**Acceptance required to close:**

1. Confirm safe-off at boot before the lamps can energise.
2. Confirm Stereo softly fades to 85%, Mono softly fades fully off, and standby
   remains off.
3. Observe no lamp flicker at steady state or through fades.
4. Exercise and then release all four pots; confirm the OLED does not chatter
   between control overlays while the lamps are on.
5. Confirm no abnormal module or wiring temperature and measure the installed
   three-lamp current.
6. Record the physical result, update the BOM/status documents and restore a
   release build over OTA before closing this issue.

**Procurement records:** `hardware/BOM/phase1.csv` and `docs/Parts List.md`.
**Wiring:** `docs/Wiring.md`, H5 and Power Distribution.
