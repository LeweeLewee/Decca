# OTA candidate: Decca 0.28.6-s1

**DEPLOYED: v0.28.6-s1 verified on Decca at 21:03 BST, 2026-09-21.**

Prepared 2026-09-21 on `fix/security-acceptance`, based on main `02eee2c`.
Installed firmware is now v0.28.6-s1. This image excludes the
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
  flash **1,020,493 / 1,310,720 bytes (77.9%)**.
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
| Candidate | `build/candidates/decca-0.28.6-s1.bin` | 1027072 | `6f2f6ebfdaba6ad00b6a7d97a2dbe6cd1f9c6e9e79328cdab5e4154f5e8ab9f6` |
| Recovery | `build/candidates/decca-0.28.5-recovery.bin` | 1026736 | `c72a41205329a2682e58a599952103caee7324a639113bc0d76692de5ceaab12` |

Recovery was rebuilt from v0.28.5 source `02eee2c` with the same configuration;
it is not a readback of installed flash and has not been flashed in this session.
Recovery build PASS: RAM 52,336 bytes; flash 1,020,161 bytes. OTA recovery needs
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

The owner authorised authenticated OTA upload of **the exact candidate hash above**
to `decca-esp32.local`, followed by reboot; it has completed. For future uploads, recheck the target,
binary and source/configuration manifest first, using local credentials without
printing them. If firmware changes again, rerun affected checks and confirm the new deployment scope.

After an approved upload, verify fresh discovery and advertised `0.28.6-s1`
version (not merely ping), authentication rejection, and read-only WiiM status.
The owner must verify display, standby/wake, source and physical volume response.
If there is a regression, stop and assess recovery with the owner. Do not run
flood/corrupt-image/power-cut/eFuse tests on the installed music centre.

## Authorised upload attempt: 2026-09-21 20:27 BST

The owner approved the update. The frozen SHA-256 and source/configuration
manifest matched; fresh discovery identified Decca v0.28.5 with authentication
required. The uploader received Authentication Failed and exited 1 before any
firmware transfer. No update or intentional reboot occurred.

The local saved OTA password is not accepted by the installed image; no newer
DECCA_OTA_PASSWORD environment value was available. Obtain the correct private
installation configuration from the owner. Correct src/secrets.h and rebuild
both candidate and recovery images before another attempt: merely using a newer
uploader password with the old candidate would install the stale password.
Recheck the relevant tests, known-secret scan, configuration presence and image
hashes. The hashes above identify the attempted candidate, not a future rebuild.

## Credential recovery and successful deployment

The current configuration was recovered from the local working copy used for
v0.28.5 on 2026-09-21 (`work-in-the-decca-restoration-repository/work/Decca`).
Only DECCA_OTA_PASSWORD differed from the stale shared configuration. The
recovered file is preserved in this checkout's ignored src/secrets.h and the
shared Decca folder's secrets.h. Do not recover credentials from Git or print
them. The original deployment folder remains an additional private copy.

Both candidate and recovery images were rebuilt to preserve that credential;
no firmware source changed. Candidate flash 1,020,493 bytes, recovery flash
1,020,161 bytes; RAM 52,336 bytes each. The image table now identifies these
corrected binaries. The repeated known-secret scan found zero matches in 3,126
Git objects and 208 nonignored files.

Authenticated transfer attempts using the standard sender and then 100 ms
pacing failed partway, with v0.28.5 still advertised afterward. The final retry
used the same corrected image and upstream espota protocol with TCP_NODELAY
set on the accepted sender socket; it reached 100% and uploader exit 0.
This is a successful retry, not proof that buffering caused earlier failures.

Fresh discovery at 2026-09-21 21:03:42 BST advertised firmware 0.28.6-s1,
auth_upload=yes, uptime_ms_at_connect=770, power_save=0, tx_power_qdbm=78
(19.5 dBm) and rssi_at_connect=-76 dBm. These are connection-time snapshots,
not continuous uptime/RSSI measurements. The invalid-proof OTA test passed.
Read-only WiiM status remained stopped, volume 47%, unmuted, mode 10.
No playback command was sent. Physical display/standby/source/volume acceptance
remains pending; SDK/certificate and wider security acceptance issues stay open.
