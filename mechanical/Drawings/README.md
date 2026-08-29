# Drawings

Dimensioned engineering drawings for fabrication, measurement, and reference.

**Intended contents**
- PDF drawings with critical dimensions and tolerances.
- Reference sketches for cabinet fit and mounting.

## Active OLED mount design direction

`Decca_OLED_Display_Mount_CAD_Review_revO.md` is the authoritative carrier
architecture brief. It includes the 2026-08-29 Rev P physical-retention
correction: flush-side insertion onto fixed rear PCB datums, positive sprung-post
handling retention, and no release until the corrected print passes physical
retention tests.

## Display mount

| File | Role |
|---|---|
| `Decca_OLED_Display_Mount_Spec_v1.0.md` | approved specification, **now at v1.1** (the filename keeps `v1.0` for link stability). §2 holds the **measured and locked** Decca interface geometry: opening 35.20 × 15.30, M2 pitch **49.00 mm**. Other design-intent values in it are superseded by later revisions — the build reviews are authoritative there. |
| `Decca_OLED_Display_Mount_CAD_Review_revN.md` | last front-loaded build (Rev N) |
| `Decca_OLED_Display_Mount_CAD_Review_revO.md` | **the governing brief**, as amended 2026-08-29 by the Rev P physical-retention correction |
| `Decca_OLED_Display_Mount_Topology_revP.md` | Rev P pre-CAD topology gate: side section, plan, load path, Z-chain, retention, corridors. **Rev P.2 corrected topology** — flush-side insertion, fixed rear datum pads, plain and sprung locating posts |
| `Decca_OLED_Display_Mount_CAD_Build_revP.md` | **Rev P build review and validation record** — start here |
| `Decca_OLED_Display_Mount_revP_views.png` | Rev P front three-quarter, carrier + module |
| `Decca_OLED_Display_Mount_revP_rear.png` | Rev P rear three-quarter — the rear pocket, posts and flange |
| `Decca_OLED_Display_Mount_revP_sections.png` | Rev P section through a sprung locating post, with the Perspex, bezel, glass and PCB |

Current mechanical revision: **P — OPEN**. The first Rev P print **failed its
physical retention test**: the OLED fell forward out of the loose carrier.
Corrective work is in progress. Rev P is **not released**; the retention finding
stays open until a corrected print passes the physical inversion and
gentle-shake handling test. Module preparation is unchanged — front-side solder
protrusion ≤ 1.00 mm; see the Rev P build review §8.
