# Wiring

Harness and interconnect diagrams — how modules physically connect inside the
cabinet.

**Intended contents**
- Point-to-point wiring diagrams and harness drawings for H1–H5.
- Connector pinout tables.

**Harnesses** (see `docs/Wiring.md` for the authoritative detail)
- H1 — potentiometer harness
- H2 — original on/off switch harness
- H3 — radio/source button harness
- H4 — OLED harness
- H5 — dial-lighting harness

**Conventions**
- The authoritative textual pin map and colour standard live in `docs/Wiring.md`
  and must be reconciled with `src/hardware.h` before any build. Diagrams here
  illustrate that map.
- Colour standard: Brown = GND, Red = 3.3 V, Orange = 5 V, White = signal. The
  original on/off switch keeps its original Red/Green conductors as a documented
  exception.
- H4 OLED loom exception: Orange = SDA (GPIO21) and Yellow = SCL (GPIO22).
  Never connect the H4 Orange conductor to 5 V.
