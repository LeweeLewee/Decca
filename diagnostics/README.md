# Diagnostics archive

## ADC/PWM noise capture — 2026-09-06

The report, device summary and 12,000-row raw capture preserve the completed
controlled comparison between 85%/1 kHz PWM and constant-high operation. The
test ran diagnostic firmware v0.27.1 on the former GPIO25 lighting route.

The result is historical evidence, not current firmware: PWM switching was a
modest contributor to raw ADC noise, while the normal filter/deadband path
produced no UI-sized filtered excursions in either phase. No brightness or
production-filter change was justified by the result.

Current production firmware is v0.27.4, lighting PWM is on GPIO18, and all fade
logic has been removed. The diagnostic-only firmware hooks were intentionally
not copied into production because they depend on the superseded fade API and
old GPIO route. The report and raw data are the authoritative retained record.
