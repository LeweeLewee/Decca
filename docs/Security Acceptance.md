# ESP32 security acceptance

Status: OPEN. First review and live authentication check: 2026-09-21.
This gate supplements functional commissioning; successful OTA uploads and
passing lifecycle tests do not establish security acceptance.

## Scope and acceptance rule

Protect firmware integrity, Wi-Fi/OTA credentials, controller availability,
and predictable power/source/volume behaviour against another LAN client or
an impersonated WiiM endpoint. Include physical flash access as a separate
risk decision. The controller is control/UI only and does not process audio.

Close this gate only when the required tests below have recorded evidence and
remaining design risks have explicit owner acceptance. An unrun test, timeout,
compile-only result, or documentation statement is not a pass. Do not use the
installed music centre for flood, power-cut or corrupt-image tests: use a spare
ESP32 with representative firmware and a verified USB recovery route.

## Evidence recorded in this pass

- Baseline: main commit `02eee2c`; installed version recorded as v0.28.5 in the
  handover. Work is isolated on `fix/security-acceptance`; no firmware uploaded.
- Live `python security/ota_auth_probe.py decca-esp32.local`: PASS.
  The controller sent an AUTH challenge for an unauthenticated invitation,
  then explicitly returned Authentication Failed for an invalid proof.
  Exactly two small UDP datagrams were sent; no TCP firmware server or payload
  was provided. This tests one rejection, not rate limiting or replay safety.
- After the probe, `decca-esp32.local` answered 3/3 pings. This proves limited
  network reachability only, not unchanged uptime or physical control response.
- Probe regression suite: 5/5 passed locally, including false-pass protection
  for timeouts, unexpected replies and unauthenticated acceptance.
- Tracked-file inventory contains only `src/secrets.example.h`, no secrets.h,
  .env, .bin or .elf. Local `git log --all` for secrets.h paths returned no
  commits. This is a filename/history check, not a content-based secret scan
  or proof about remote/deleted history and previously distributed binaries.
- Release build: PASS, 50,168 bytes RAM and 842,209 bytes flash (without
  local credentials). WiiM suite compilation: PASS. Security suite compilation:
  PASS after correcting a Unity assertion name. Six security assertions were
  compiled, not executed on hardware; PlatformIO reports zero executed cases.
- That initial pass made no firmware release/version change, upload, merge or eFuse operation. The continuation below prepares a candidate but still performs no upload.

## Findings and required checks

| ID | Priority | Finding / test | Acceptance evidence required | Status |
|---|---|---|---|---|
| SEC-01 | High | OTA authentication | Missing credentials require challenge; incorrect proof rejected; correct-password update still works on candidate firmware | Positive deployment and post-update invalid-proof rejection PASS on 0.28.6-s1 |
| SEC-02 | High | WiiM peer identity | Reject an impersonated peer using a trusted certificate/pin provisioned through an independently verified channel; prove genuine WiiM reconnect after restart/update | OPEN: `client.setInsecure()` remains in wiim.cpp |
| SEC-03 | High | Oversized HTTP bodies | Reject declared and streamed overflow without heap growth proportional to body size, partial JSON acceptance or unsafe control changes | Bounded body sink and transport guard implemented; native guard tests pass; ESP32 integration execution pending |
| SEC-04 | High | Malformed/stalled responses | Malformed, deeply nested, huge, chunked, missing-length and slow/trickled bodies plus long HTTP headers; bounded request duration, heap recovery and local controls responsive | Ten native guard cases pass, including stalls/trickle/rollover; real TLS/HTTP adversarial integration pending |
| SEC-05 | Medium | OTA abuse / recovery | Repeated failed auth, stale proof and interrupted/corrupt transfer cannot install an image; continued physical controls and later valid update work | OPEN; run bounded tests on spare board |
| SEC-06 | Medium | Network boundary | Inventory listening services from trusted and guest segments; confirm guest/WAN cannot reach OTA; inspect router forwarding and IPv6 rules | OPEN; no port inventory or router evidence yet |
| SEC-07 | Medium | Credential lifecycle | Content-based history/artifact/log scan, unique strong password, controlled firmware distribution and rotation procedure | Known current passwords absent from 3,088 Git objects and 207 nonignored files; general secret detection/rotation review OPEN |
| SEC-08 | Medium | Firmware authenticity / physical access | Inventory chip revision/eFuse state; decide signed OTA, secure boot, flash/NVS encryption and debug access policy with recovery implications | OPEN; no eFuses changed |
| SEC-09 | Medium | Dependencies | Record exact toolchain/framework/library versions; check applicable vendor advisories and disposition each finding | Platform pinned; IDF 4.4.7 EOL confirmed; initial advisory triage below, migration/full review OPEN |
| SEC-10 | Medium | Failed-boot recovery | Prove fallback after a fully received but non-booting image, or explicitly accept USB recovery | Deferred Phase 3 under ADR-0012; not a security pass |

## Response-size change and its limits

`src/bounded_response.h` writes decoded HTTP body bytes into the existing
3072-byte response buffer, leaving one byte for NUL. A known length exceeding
3071 bytes is rejected before body reading. Unknown-length or chunked bodies
use the same cumulative cap. Overflow remains a failure even if HTTPClient
retries a write; the response is cleared and the connection is closed.
No body-sized String is allocated by the WiiM request path anymore.

The continuation adds `GuardedClient` around the actual TLS client. Each
request has an 8192-byte decrypted HTTP receive budget (headers, body and chunk
framing combined) and a six-second elapsed budget; reaching either budget closes
the connection and marks the request failed. The HTTP body cap remains 3071.
The guard is checked by virtual read/available/connected calls used by HTTPClient,
including its stalled-body loop and Stream header/chunk-line reads. A final
requestOk check prevents HTTPClient's partial-success return from hiding an abort.
Successful requests retain connection reuse; the next request resets the budget.

This is not a hard real-time six-second completion promise. A TLS/socket call
already in progress or Stream timedRead may finish after that point; socket and
TLS handshake timeouts are explicitly three seconds. Real ESP32/TLS scheduling,
heap use and physical controls still need post-upload/bench evidence. Native
mock-transport tests prove the production guard logic, not the whole network stack.

Certificate verification remains disabled pending a viable, verified trust
provisioning method for the actual WiiM device. Do not capture a certificate
from an unverified network connection and call that identity verification.

## Repeatable checks

From the repository root:

```powershell
python -m unittest discover -s security -p test_ota_auth_probe.py -v
python security/ota_auth_probe.py decca-esp32.local
$pio = "$env:USERPROFILE/.platformio/penv/Scripts/platformio.exe"
& $pio run -e esp32dev
& $pio test -e esp32dev -f test_security -f test_wiim --without-uploading --without-testing
```

The first command tests probe classification with mocked responses. The second
contacts the named controller, requires no credentials and never sends firmware.
A timeout is INCONCLUSIVE. Do not loop the probe as a flood test.
If an invitation is unexpectedly accepted without authentication, the device
may enter its update path before failing to connect to the absent server;
check recovery and stop. This is a negative test, not a guaranteed no-effect ping.

`test_security` contains six on-target cases: exact capacity/NUL termination,
overflow/canary protection/sticky failure, cumulative chunk overflow, invalid
destination handling, malformed JSON preserving state and excessive nesting.
Compile-only does not execute any of these assertions. Run it on a spare ESP32
via USB, then run existing WiiM tests and representative live transport cases.
No secrets are needed for the unit tests. A deployment build must separately
use local credentials and a new firmware version before release.

For SEC-03/04 bench integration, serve responses of 0, 3071, 3072 and much
larger body sizes; split at different chunk boundaries, omit Content-Length,
truncate a declared body, stall and trickle bytes, and send oversized headers.
Record minimum free heap, request completion time, reboot reason/uptime and
physical power/source/volume responsiveness. Verify genuine WiiM metadata,
source, volume and reconnect behaviour after each failure.

## Dependency baseline and references

Observed build: PlatformIO Espressif32 7.0.1, Arduino framework package
3.20017.241212+sha.dcc1105b (Arduino-ESP32 2.0.17), Xtensa GCC 8.4.0,
ArduinoJson 6.21.5, SH110X 2.1.14, GFX 1.12.6, BusIO 1.17.4.
This inventory is not a finding that those versions are vulnerability-free.

- [Espressif ArduinoOTA implementation](https://github.com/espressif/arduino-esp32/blob/2.0.17/libraries/ArduinoOTA/src/ArduinoOTA.cpp)
- [Espressif HTTPClient implementation](https://github.com/espressif/arduino-esp32/blob/2.0.17/libraries/HTTPClient/src/HTTPClient.cpp)
- [ESP32 secure boot guidance](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/security/secure-boot-v2.html)

## Continuation: 0.28.6-s1 (deployed; owner physical acceptance passed 2026-09-22)

The initial long prerelease label was shortened to fit the existing OLED startup
buffer. No display layout change is required. Changes are confined to WiiM HTTP
resource bounds, timeout configuration, version, platform pin and security checks.
The separate health trial is excluded from this candidate.

Executed local evidence:

- Ten native C++ security cases PASS using the actual `BoundedResponse` and
  `GuardedClient` headers, a minimal Stream shim and deterministic fake client.
  Coverage: capacity/canaries/NUL, cumulative overflow and retry, invalid buffers,
  receive budget, stalled peer, trickle deadline, millis rollover, reuse, recovery
  after failure, and a fragmentation sweep. This is not ESP32/TLS emulation.
- Five Python probe regression cases PASS again.
- Exact current Wi-Fi/OTA password scan: 3,088 reachable local Git objects and
  207 nonignored files examined, zero matches. No values printed. This does not
  cover unknown old passwords, transformed secrets, remote unreachable history,
  ignored logs or previously distributed firmware. Credential-bearing binaries
  and src/secrets.h remain ignored and local.
- UPnP audio discovery identified the device named Decca as a WiiM Pro Receiver.
  Read-only getPlayerStatus/getMetaInfo requests returned HTTP 200 and valid JSON:
  236 and 208 body bytes respectively, with Content-Length and approximately
  120 header bytes each. No playback/source/volume command was issued. TLS was
  unverified, matching current behaviour; discovery is not cryptographic identity.
- Selected TCP ports 22, 23, 80, 443, 1883, 3232, 8080 and 8883 all timed out on
  the controller. This is inconclusive, not proof that those ports are closed.
  Guest/WAN/IPv6 exposure was not checked.

Run native checks with `python security/run_host_tests.py` where a C++ compiler
is available, or pass `--zig <path-to-zig.exe>` on this host. CI now executes these
checks and the probe regressions, and compiles every ESP32 suite. For a private
known-secret scan run `python security/scan_known_secrets.py` with local secrets.h.

### Dependency disposition

The installed build headers identify ESP-IDF 4.4.7. Espressif declares the 4.4
branch end-of-life from July 2024. Pinning PlatformIO espressif32 7.0.1 reproduces
the tested baseline; it does not fix the unsupported SDK. A supported-framework
migration needs its own hardware regression pass and remains SEC-09.

Initial triage of the current Espressif advisory index: Bluetooth profiles and
provisioning, WPS, ESP-NOW, ESPTouch, HTTP/WebSocket server and SoftAP DHCP server
are not enabled by Decca's station-mode application; ESP32-P4 JPEG/ESP-TEE issues
are outside this board/application. These are source-based reachability
observations, not a claim that all linked libraries or their configurations are
vulnerability-free. Bootloader/physical-access protections remain unresolved.
The Arduino advisory CVE-2024-45798 concerns upstream privileged GitHub workflow
injection, not an ArduinoOTA runtime exploit. Decca's workflow uses read-only
repository permissions and no upstream artifact-processing workflow.

- [Espressif IDF 4.4 end-of-life advisory](https://documentation.espressif.com/AR2024-008%20End-of-Life%20Advisory%20for%20ESP-IDF%20v4.4%20Release%20Branch%20EN.html)
- [Espressif vulnerability index](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/security/vulnerabilities.html)
- [Arduino upstream workflow advisory](https://github.com/espressif/arduino-esp32/security/advisories/GHSA-h52q-xhg2-6jw8)

### OTA approval boundary

See [OTA Candidate](OTA%20Candidate.md) for the final image/hash and build evidence.
Approval to upload the candidate is a controlled integration trial, not closure
of this security gate. Peer certificate verification, supported-SDK migration,
physical protections, router isolation and destructive recovery/abuse tests stay
open. No eFuse or firmware-signing migration is included.

### Upload attempt blocked (2026-09-21 20:27 BST)

Owner-authorised upload was rejected at authentication before transfer. At that point the device
remained on v0.28.5 and the candidate required credential recovery
and a rebuild; candidate presence checks establish inclusion, not credential
validity. See OTA Candidate for the failed-attempt record.

### Deployment completed (2026-09-21 21:03 BST)

The saved credential was recovered from the prior successful deployment folder.
Only that private configuration changed; candidate/recovery images were rebuilt.
The corrected credential scan found zero matches in 3,126 Git objects and 208
nonignored files. After two interrupted authenticated transfers, a TCP_NODELAY
sender retry reached 100%, returned exit 0 and fresh discovery confirmed 0.28.6-s1.
The post-update invalid-proof rejection test passed. WiiM remained stopped at
47%, unmuted. No hardware test-suite execution is claimed. Physical acceptance
was subsequently confirmed by the owner on 2026-09-22 (see below).
See OTA Candidate for corrected hashes and full deployment evidence. SEC-01 has
positive and negative OTA evidence on the new image; the security gate stays open.

### Owner acceptance (2026-09-22)

The owner confirmed the requested display, standby/wake, source-selection and
physical-volume checks passed on installed v0.28.6-s1, and authorised updating
and merging the repository. This is owner-reported functional acceptance, not
execution of the ESP32 security suites or adversarial TLS/recovery tests.
FW-SEC-01 and FW-WIFI-01 remain open. No additional firmware upload is required.
