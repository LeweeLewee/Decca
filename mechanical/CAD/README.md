# CAD

Source (editable, parametric) mechanical design files.

**Intended contents**
- Fusion 360 archives (`.f3d`) and/or OpenSCAD (`.scad`) source.
- Neutral exchange formats (STEP `.step`) for interop.

**Conventions**
- Keep source here; export print-ready meshes to `../STL/`.
- Parametric source is preferred so parts can be re-derived if dimensions change.
- Record revisions in `docs/Revision History.md`.

## Display mount — current revision: **P — OPEN, NOT RELEASED**

Rev P.2 is the corrected **flush-side-insertion** architecture, and it **passed**
its physical OLED-retention and Perspex-fit tests. **Rev P.3** amends only the
radio-side interface: the lighting-unit clearance cut and the original Decca
bolt / captive-nut interface that replaces the deleted M2 heat-set inserts. The
`.f3d` is the source of truth; the STEPs and the STL are derived exports.

| File | Role |
|---|---|
| `Decca_Display_Mount_revP.f3d` | **editable source of truth** — fully parametric, 101 named user parameters |
| `Decca_Display_Mount_revP_fusion.py` | the generator that builds the `.f3d`; single source of truth for every dimension |
| `Decca_Display_Mount_revP_verify.py` | independent offline verification of the exported STL (numpy only) |
| `Rear_Display_Carrier_revP.step` | the one structural part |
| `Decca_Display_Mount_revP_assembly.step` | carrier + Perspex + OLED + bezel + **original nuts / bolt envelope + lighting-unit keep-out** references |
| `Hex_Pocket_Fit_Coupon_revP.step` | five-station captive-nut pocket fit coupon — print this **before** the carrier |
| `Front_Bezel_revN.step` | cosmetic bezel — **unchanged, still the file of record for Rev P** |

Rev N files are retained as the last front-loaded design:
`Decca_Display_Mount_revN.f3d`, `Decca_Display_Mount_revN_assembly.step`,
`Rear_Display_Carrier_revN.step`, `Retainer_Bar_revN.step`. The Rev P
architecture deletes the retainer bar, so `Retainer_Bar_*` has no Rev P
equivalent.

### Rebuilding

Inside Fusion (Utilities → Add-Ins → Scripts), point `OUT_DIR` at this clone's
`mechanical` folder and run `main()`, `validate()`, `import_bezel()`,
`snapshots()`, `export()`, and `coupon()`. `main()` creates its own new document
and never modifies the Rev N or Rev O files; `snapshots()` regenerates the five
Drawings PNGs from the live model; `coupon()` builds and exports the hex-pocket
fit coupon in its own document. Then, offline:

```bash
python mechanical/CAD/Decca_Display_Mount_revP_verify.py
```

It reads only the exported STL and exits non-zero on failure, so it works as a
gate. See `../Drawings/Decca_OLED_Display_Mount_CAD_Build_revP.md` §13 for why
it is deliberately not a second run of the same recipe — and for the silent
Fusion `createTorus` failure it caught.

> **Rev P is OPEN.** The Rev P.2 OLED retention and Perspex fit are physically
> validated. Outstanding for the Rev P.3 amendment: measure the glass envelope
> (§9), the original nut across flats **and** across corners and the original
> bolt length (§21.6), print the hex-pocket fit coupon (§21.7), then prove
> installed lighting-unit clearance, rack/twist and the captive-nut behaviour on
> a real part.
