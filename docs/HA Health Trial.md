# Home Assistant health trial

Status: isolated development only; no firmware upload and no live HA installation.
Branch: `feat/ha-health-trial`.
Baseline main: `02eee2c24b9c3aa3f986b885837a86aa76e4b321`.
Installed firmware remains v0.28.5, as recorded in the development handover.
Trial builds identify as `0.28.6-h1`; normal builds retain v0.28.5.

## Scope and architecture

A read-only optional health module receives power/source/WiiM state from main.
It never calls another functional module, writes settings/NVS/GPIO, sends WiiM
commands or changes Wi-Fi settings. Default production environments compile out
the module and its coordinator calls. Separate trial environments opt in.

Local sampling is 1 Hz; summaries are sent every **five minutes**, selected by
the owner. The first summary follows a 60-second startup grace period.
Wi-Fi disconnections use Wi-Fi events rather than slow polling. WiiM fault
episodes count transitions into the existing worker's Error state, not every
failed HTTP request. Counters are cumulative since boot, with uptime/reset
reason showing the reset boundary. No extra probes of the WiiM are introduced.

A report includes current/minimum-window RSSI, current/minimum-since-boot free
heap, maximum coordinator loop gap in the window, sample count, Wi-Fi/MQTT
disconnect counts, WiiM fault episodes, firmware, reset reason, logical power,
requested source and reported WiiM worker status. A worker status of ready is
not proof of a fresh successful WiiM probe (especially in standby).

A fixed-size accumulator keeps minima and loop-gap maxima while offline.
Failed sends merge their window back without losing samples arriving during
the attempt. No unbounded historical queue exists. QoS 0 means a successful
socket write is not an end-to-end delivery guarantee: a report/minimum can be
lost in transit; cumulative fault counts may still be recovered next time.
Power loss discards unsent RAM data. Do not infer exact event timestamps from a
five-minute bucket or claim sub-second RSSI events are captured at 1 Hz.

MQTT is ESP-IDF's bundled client, not a new Arduino library. A low-priority
worker performs publish calls; the coordinator performs no MQTT/socket calls.
Reconnects are spaced by five minutes, network operations have a one-second
configured timeout, and packets are bounded to 1280 bytes. DNS is avoided by a
numeric broker address. MQTT keepalives still generate small packets between
summaries (120-second configured keepalive); five minutes is the data cadence,
not a promise of no intervening traffic. Network stack scheduling/timeouts
require measurement on a spare board.

The aggregator/JSON payload uses fixed-size storage and no application-level
steady-state allocation. ESP-MQTT and the network stack allocate internally;
strict system-wide NFR-02 compliance is **not established**. Heap trend,
fragmentation/stack headroom and responsiveness must be measured before any
deployment decision. This is a documented trial feasibility gate, not a claim
that an isolated task cannot affect the rest of the ESP32.

## Isolation and configuration

- No migration to ESPHome, partition changes, pin changes or production HA edits.
- Telemetry defaults off. Missing broker/user/password also leaves it inactive.
- Trial MQTT topics: `decca/trial/health/state` and
  `decca/trial/health/availability`.
- Separate HA device/entity IDs: `decca_health_trial`.
- One trial publisher only: fixed client ID `decca-health-trial`.
- Initial trial uses an isolated LAN test broker with TCP port 1883 and a
  dedicated publish-only account restricted to those two topics. Credentials
  are not encrypted on this transport. Do not use a shared administrator account
  or an untrusted network; TLS feasibility is outside this first build.
- All broker and Wi-Fi values belong in ignored `src/secrets.h`. Do not copy
  the existing workspace secrets into fixture builds.
- No command subscription, restart button or HA-controlled device function.
- Trial and fixture environments reject upload targets through
  `tools/block_trial_upload.py`.

For a later spare-board build, local secrets additionally define
`DECCA_HEALTH_BROKER`, `DECCA_HEALTH_USER`, `DECCA_HEALTH_PASSWORD`.
The compile fixture uses RFC 5737 addresses and fake credentials and must never
be flashed. The interval may be compiled between 5 and 30 minutes, but update
HA expiry to at least twice the interval plus 60 seconds if changing it.

## Dashboard package

Files under `home-assistant/` are JSON-form YAML (valid YAML), requiring no
custom cards or HACS. The package explicitly defines MQTT entities, avoiding
retained discovery records and discovery bursts. No discovery publisher is
needed. The dashboard uses entity and 24-hour history cards.

Use a **test HA instance first**:
1. Back up its configuration and confirm the MQTT integration reaches the test
   broker. Record the HA version and existing entity IDs.
2. Add `decca-health-package.yaml` as a named Home Assistant package under
   the existing `homeassistant: packages:` configuration. Merge into existing
   mappings; never replace the configuration file or duplicate top-level keys.
3. Run HA's configuration check before reloading/restarting the test instance.
4. Create a separate manual dashboard titled Decca Health Trial; use the
   dashboard file in its raw configuration editor.
5. Confirm the default entity IDs match. HA preserves custom IDs and may add a
   suffix on collisions; adjust dashboard references if necessary.
6. Replay the labelled fixture files only onto the test broker's state topic,
   non-retained, and publish online on the availability topic. Do not publish
   fixture data to the user's normal HA history.
7. Confirm numeric units, graphs, reset/counter behaviour, standby and source
   context. Withhold telemetry for 660 seconds: sensors must become unavailable
   even if a stale retained online availability message exists.
8. Exercise broker restart, HA restart and offline/recovery. State is deliberately
   not retained; HA may wait up to the next report after restart.
9. Confirm recorder includes these entities. Default retention may limit history;
   changes to global retention/storage are a separate reviewed choice.

The availability Last Will reports broker connection loss; it cannot distinguish
controller failure, Wi-Fi failure and broker failure. HA expiry is 660 seconds
for the selected five-minute cadence. Do not call MQTT availability a hardware
health diagnosis.

## Build and test gates

No command in this section uploads firmware.

```text
pio run -e esp32dev
pio run -e esp32dev-network-baseline -e esp32dev-health-compile
pio run -e esp32dev-health
pio test -e esp32dev --without-uploading --without-testing
python tools/test_health_contract.py
g++ -std=c++17 -Wall -Wextra -Werror tools/tests/health_model_test.cpp -o health-model-test
./health-model-test
```

The baseline and enabled fixture builds use identical inert Wi-Fi/WiiM settings
so link-time removal of unconfigured network code cannot produce a misleading
size comparison. Both compile all network paths. No credentials are required.
The credential-free default build alone is not comparable with the installed
credential-enabled image and is **not** a deployable rollback image.

CI runs the pure C++ accumulator tests, artifact contract checks, full-path
comparison builds and target test compilation. Offline checks do not establish
Home Assistant runtime validity, radio reliability, actual heap/stack safety or
physical control acceptance. Record measured results in the validation section.

### Spare-board acceptance before considering installed hardware

Use a separate ESP32, test broker and test HA, with no connection to the installed
controller or live audio path. An isolated WiiM fixture server is preferred.
Trial upload is intentionally blocked; enable a separately reviewed spare-board
upload target only after positively identifying its port/address and credentials.

- Baseline and enabled runs: at least 24 hours each, including on/standby.
- Confirm five-minute reporting and counter/minimum capture across short drops.
- Broker unavailable/wrong password/restart, Wi-Fi interruption and HA restart.
- No unexplained reset, heap decline or growing MQTT backlog.
- Quantify idle and worst-case free heap and both task stack high-water marks;
  static RAM size is not a substitute for runtime measurements.
- Controls remain within NFR-01 (50 ms); compare source/volume response, standby
  OLED behaviour and OTA service with telemetry disabled/enabled.
- Compare packet loss with a simultaneous control host/AP observation; do not
  close FW-WIFI-01 from MQTT availability alone.
- Rehearse restoring the exact baseline image over OTA and USB on the spare.
- Reject or redesign if overhead, responsiveness, recovery or integration fails.

## Reversal and deployment boundary

**A branch is not a firmware rollback mechanism.** The installed firmware lacks
automatic post-boot rollback. OTA recovery depends on the trial firmware booting
and staying reachable; otherwise physical USB recovery may be necessary.

Today reversal means remove the trial test dashboard/package/account and archive
the branch. The existing controller and production HA remain unchanged.

Before any separately authorised installed-device trial:
1. Retrieve or build the exact v0.28.5 baseline with the correct private settings
   and recorded toolchain. Preserve firmware/partition/bootloader artifacts
   locally, SHA-256 hashes, source SHA and build manifest. Never commit credential-
   enabled binaries. Confirm that the source matches the installed release.
2. Prove the baseline rollback and USB recovery on the spare board first.
3. Keep physical USB access available. If the user requires **zero risk** to the
   installed deployment, do not flash it; retain this as a spare-board experiment.
4. Keep HA configuration/dashboard backups. Use a separate additive dashboard.
5. On regression, restore the verified baseline application by the established
   authenticated OTA procedure if reachable, otherwise the verified USB route.
   Do not erase NVS or change partitions.
6. Verify version, Wi-Fi/OTA, physical controls, digital/vinyl, standby and display
   behaviour after rollback. Broker credential revocation stops publishing but
   does not remove firmware tasks and is not a full rollback.
7. Remove only the trial package/dashboard and its retained availability message;
   preserve existing D7 entities and historical data unless explicitly removing
   the trial history. There are no retained discovery messages to clean up.

No installed-device deployment, merge to main or changes to the user's live HA
are authorised by this build record.

## Validation record

Local Windows checks (2026-09-21):
- PlatformIO Core 6.1.19; Espressif32 7.0.1; Arduino framework
  3.20017.241212+sha.dcc1105b; Xtensa 8.4.0+2021r2-patch5.
- All four build configurations pass without compiler warnings after shortening
  the trial label to fit the existing OLED identity buffer.
- Default disabled: 50,168 bytes static RAM / 842,209 bytes flash, identical sizes
  to the untouched credential-free baseline.
- Full-network disabled fixture: 52,336 bytes static RAM / 1,020,137 bytes flash.
- Full-network enabled fixture: 52,452 bytes static RAM / 1,062,545 bytes flash
  (81.1% of the 1,310,720-byte application slot).
- Delta: 116 bytes static RAM and 42,408 bytes flash. Runtime allocations are
  additional: at least the 6 KiB publisher and 4 KiB MQTT task stacks, client
  buffers and TCP resources. Actual headroom remains unmeasured.
- Five offline Python tests pass: field coverage, dashboard entity references,
  expiry/isolation, recovery/reboot fixtures and upload-target rejection.
- C++ aggregation execution and all target-suite compilation are configured in
  the branch CI; consult the PR checks for their results.
- No production credentials copied, no firmware uploaded, no HA installation.

Physical/spare-board and live HA acceptance are NOT run. No rollback image
has been prepared or tested. This branch is a feasibility prototype, not a
deployment-ready release.
