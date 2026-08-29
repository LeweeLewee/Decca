# ADR-0012: Use authenticated local-network ArduinoOTA

## Status
Accepted

## Date
2026-08-29

## Context
The ESP32 is about to be mounted inside the Decca while firmware integration is
still active, making routine USB access inconvenient.

## Decision
Use ArduinoOTA with station-mode home Wi-Fi, hostname `decca`, mandatory
password authentication, gitignored `src/secrets.h`, non-blocking reconnect,
PlatformIO `espota`, and the standard dual-application partition layout. The
service is local-network only. The first flash remains USB.

## Consequences
- Routine updates no longer require opening the cabinet.
- Interrupted or rejected transfers retain the running application.
- The uploader password is supplied locally via `DECCA_OTA_PASSWORD`.
- USB-to-OTA acceptance is mandatory before enclosure.
- Automatic rollback after a fully received image fails to boot remains
  FR-ADV-04 / Phase 3.
