# OTA candidate: Decca 0.28.6-s1

**BUILT AND REVIEWABLE; NOT UPLOADED. Owner approval required.**

Prepared 2026-09-21 on `fix/security-acceptance`, based on main `02eee2c`.
Installed firmware remains recorded as v0.28.5. This candidate excludes the
independent health-monitoring trial.

## Change

WiiM response bodies are capped at 3071 bytes without a body-sized String.
The transport guard caps the total decrypted HTTP receive bytes (including
headers/chunk framing) at 8192 and applies a six-second transaction budget.
In-flight TLS/socket/Stream operations can finish later; this is not a hard
real-time promise. Socket and TLS handshake timeouts are three seconds, with
the seconds/milliseconds mismatch corrected. Connection reuse is retained.
The tested PlatformIO platform is pinned to 7.0.1.

## Verification

- **10/10 native production-guard tests PASS**, using a fake client/clock.
- **5/5 Python OTA-probe regression tests PASS**.
- **All 10 ESP32 suites compiled**, including the six new security cases.
  They were not executed on hardware.
- Credential-enabled OTA build PASS: RAM **52,336 / 327,680 bytes (16.0%)**;
  flash **1,020,461 / 1,310,720 bytes (77.9%)**.
- Installed-controller probe required authentication and rejected an invalid
  proof. No firmware was sent. Read-only WiiM responses fit the new size limits.
- No current Wi-Fi/OTA password matches in 3,088 local Git objects or 207
  nonignored files at scan time. This is exact-known-secret coverage only.
- Both images contain the expected version and all four nonempty installation
  definitions. Values were not printed. Private configuration/images stay ignored.

## Frozen local images

These binaries contain credentials: keep them local. The ignored
`build/candidates/manifest.json` records image and source/configuration hashes.

| Image | File | File bytes | SHA-256 |
|---|---|---:|---|
| Candidate | `build/candidates/decca-0.28.6-s1.bin` | 1027040 | `42cccdf7aa5e7dcbf5e871848e0651df1f94c87acac96893c67169d3dba0cd6c` |
| Recovery | `build/candidates/decca-0.28.5-recovery.bin` | 1026704 | `767e8300b883dceec644d945744e7c33cbf29661da082e707caf3f5d94139238` |

Recovery was rebuilt from v0.28.5 source `02eee2c` with the same configuration;
it is not a readback of installed flash and has not been flashed in this session.
Recovery build PASS: RAM 52,336 bytes; flash 1,020,129 bytes. OTA recovery needs
a reachable service; a non-booting application may require USB. Automatic
failed-boot rollback remains unimplemented. A backup image is not proof of recovery.

## Risks still open

This is an incremental hardening trial, not security sign-off. WiiM certificate
verification is disabled; ESP-IDF 4.4.7 is end-of-life. SDK migration, router
isolation/guest/WAN/IPv6 exposure, firmware signing/physical protections,
real ESP32 adversarial TLS tests and destructive recovery/abuse tests remain open.
TCP probe timeouts were inconclusive. See [Security Acceptance](Security%20Acceptance.md).
The existing Wi-Fi reliability issue is also unresolved.

## Approval and post-upload checks

The next action is authenticated OTA upload of **the exact candidate hash above**
to `decca-esp32.local`, followed by reboot. The owner explicitly requested this
approval boundary; no upload may run until approval arrives. Recheck the target,
binary and source/configuration manifest first, using local credentials without
printing them. If firmware changes, rerun affected checks and request approval
for the new image.

After an approved upload, verify fresh discovery and advertised `0.28.6-s1`
version (not merely ping), authentication rejection, and read-only WiiM status.
The owner must verify display, standby/wake, source and physical volume response.
If there is a regression, stop and assess recovery with the owner. Do not run
flood/corrupt-image/power-cut/eFuse tests on the installed music centre.
