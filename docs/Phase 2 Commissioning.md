# Phase 2 commissioning record

Consolidated on 2026-09-21 from the complete text history of **Amp commissioning**,
PR #11 and the subsequent installed acceptance records. This record preserves
the project decisions and results; it is not a verbatim chat or photo archive.

## Installed architecture and setup

- WiiM Pro device name: **Decca**. Control is over the local HTTPS API; no data
  cable runs between the WiiM and ESP32. The ESP32 remains control/UI only.
- Audio: WiiM Pro RCA Line Out to Fosi Audio ZA3 RCA input, in stereo, then
  the installed B&W DM601 S3 speakers. The supplied WiiM RCA lead is accepted.
- Vinyl: Audio-Technica AT-LP120X, output switch set to LINE, into WiiM Line-In.
  The installed UGREEN interconnect and other purchase details are in the BOM.
- Trigger: WiiM Pro 12 V Trigger Out directly to ZA3 Trigger In using the
  correct 2.5 mm-to-3.5 mm connection. Never connect this line to the ESP32.
  ADR-0018 supersedes the former custom ESP32 trigger-driver proposal.
- Confirmed WiiM Home settings: Line Out, Fixed Volume Output off, 2 Vrms,
  EQ off, Auto Headroom on, stereo, centred balance, 70% commissioning volume
  limit. The ZA3 gain sets the maximum listening ceiling; everyday volume is
  controlled through Decca/WiiM. No exact final ZA3 knob position is recorded.
- TIDAL Connect is the accepted digital playback route: choose **Decca** in
  TIDAL's output picker. TIDAL Wi-Fi quality Max was recommended in the original
  setup guidance; it was not separately confirmed as an observed setting.
- Use a reserved WiiM address in private installation configuration. Addresses,
  MAC/device identifiers and passwords are intentionally excluded from Git.
  The controller's current hostname is `decca-esp32`; the older `decca` label
  collided with the streamer and is superseded.

## Evidence and final acceptance

- Initial WiiM API verification reported firmware `Linkplay.4.8.827634`.
  Active TIDAL returned Dolly Parton, Jolene, at 96 kHz, vendor Tidal and mode 10.
  Both hex player fields and structured metadata decoded correctly; regression
  fixtures are retained in `test/test_wiim/test_wiim.cpp`. Empty idle metadata
  and an empty audio-output-query response were observed; output was confirmed
  in WiiM Home instead. Do not depend solely on the older documented mode 32.
- The early cloud toolchain checksum problem was superseded by successful
  GitHub Actions build/test-suite compilation, including run 34623008714.
  The original v0.28.0 deployment prompt is historical, not a current action.
- Installed firmware is **v0.28.4**, source `3195c95`. The credential-enabled
  build passed at 52,336 bytes RAM and 1,018,373 bytes flash. Authenticated OTA
  and network return passed. The affected WiiM/display target suites compiled
  without execution; this is not a claim of fresh on-target unit-test execution.
- Digital and vinyl audio, left/right routing, metadata/play state, physical
  volume/app synchronisation, VHF digital/other-position vinyl selection and
  source return passed. Corrective firmware restored about one-second source
  response after the intermediate 30–60+ second regression.
- Logical standby/resume and network recovery passed. Standby stops playback;
  the accepted 30-second WiiM automatic standby removes the ZA3 trigger.
  Logical ON uses a volume activity pulse to wake the WiiM/ZA3 without starting
  playback. The OLED blanks after ten seconds and passive telemetry leaves it
  blank. See ADR-0018 and the revision history for the wake correction.
- On 2026-09-21 the owner confirmed all formal noise checks complete with
  **no issues**: no hum, buzz, clipping, switching thumps or OLED/control
  interference. This closes FW-WIM-01 and the final Phase 2 physical gate.
- The owner approved review and explicitly authorised merge of PR #11 on
  2026-09-21. No new firmware or OTA deployment was needed for this close-out.

## Continuing work and record retention

Separate retained-switch, lighting and mechanical acceptance items remain in
`docs/Open Issues.md`; Phase 2 completion does not close those items.
The commissioning shutdown target remains playback stopped and volume no higher
than 35%, with EQ off and the 70% limit retained. A read-only observation earlier
on 2026-09-21 found playback stopped at 49%; final volume reduction was requested
but not subsequently confirmed. Do not turn that into a verified final-state claim.

The project decisions, configuration, API evidence, corrected architecture,
deployment history, acceptance outcomes and outstanding work from **Amp
commissioning** are now represented in repository records. The chat is no longer
needed to continue the project. Its original screenshots, raw device identifiers
and conversational troubleshooting are not reproduced here; retain a personal
export if those original artifacts are wanted. No private credentials were
copied into this record.
