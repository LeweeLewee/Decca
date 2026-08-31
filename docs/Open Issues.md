# Open Issues

This is the canonical short list of unresolved integration issues. Read it with
`docs/Development Handover.md` before continuing work. Historical test passes in
the revision history remain valid records of what was tested at the time, but do
not close a later issue listed here.

## HW-LGT-01 — Final dial-lighting stage flickers and disturbs pot UI

**Status:** OPEN — blocked on purchase of the selected replacement hardware.

**Observed:** the previous MOSFET/module path produced visible lamp flicker. With
that path energised, electrical disturbance also caused the display to jump
between pot overlays. The pot behaviour settled after the lighting path was
turned off and discharged. Driving the three lamps directly from the same 5 V
supply produced no visible flicker, isolating the fault to the switching path
rather than the lamps or supply. At a temporary 100% firmware target the pot/UI
disturbance stopped, but lamp flicker remained.

**Selected remedy:**

- Buy and install one DFRobot Gravity MOSFET Power Controller, **DFR0457**.
- Buy the Pi Hut pack of three **WAGO 221-415** five-way lever connectors; use
  one for the +5 V star point, one for common GND and retain one spare.
- Keep the single regulated 5 V supply and common-ground architecture.
- Before connecting DFR0457, change
  `decca::hardware::kDialLightingPwmFrequencyHz` from 5 kHz to no more than the
  controller's specified 1 kHz limit. Start at 1 kHz and adjust only if physical
  testing requires it.

**Locked behaviour:** GPIO25/D25 remains the lighting PWM output. Stereo
open/high requests lights on at the owner-approved 90% / duty 230; Mono
closed/low and logical standby request off. Preserve fades and safe-off boot.

**Device-state warning:** GitHub `main` is the firmware source of truth and holds
the approved 90% target. The last known image installed during diagnosis used a
temporary 100% target. Do not treat the installed image as a release: rebuild
from current `main` after the PWM-frequency change and upload the verified image.

**Acceptance required to close:**

1. Confirm safe-off at boot before the lamps can energise.
2. Confirm Stereo fades to 90%, Mono fades fully off, and standby remains off.
3. Observe no lamp flicker at steady state or through fades.
4. Exercise and then release all four pots; confirm the OLED does not chatter
   between control overlays while the lamps are on.
5. Confirm no abnormal module or wiring temperature and measure the installed
   three-lamp current.
6. Record the physical result, update the BOM/status documents and restore a
   release build over OTA before closing this issue.

**Procurement records:** `hardware/BOM/phase1.csv` and `docs/Parts List.md`.
**Wiring:** `docs/Wiring.md`, H5 and Power Distribution.

