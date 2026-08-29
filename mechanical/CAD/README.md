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
its physical OLED-retention and Perspex-fit tests. **Rev P.3** amended only the
radio-side interface: the lighting-unit clearance cut and the original Decca
bolt / captive-nut interface that replaces the deleted M2 heat-set inserts.
**Rev P.4** makes two bounded corrections on top of that:

- the **synthetic lighting-unit keepout is deleted** — component, body,
  generator function, derived geometry, intersection checks and exports. Its
  boundary was asserted from the carrier's own pedestals, not measured off the
  radio, so it proved nothing and misrepresented the assembly. Nothing replaces
  it, and the physical rail cut it was invented to justify is kept exactly as
  printed. **Installed clearance is proven by physical test only** — see the
  build review §20.6;
- the **rear of the OLED bay is closed** by a 1.20 mm integral opaque light
  shield, part of the carrier, with a single local four-pin/header opening —
  build review §24.

The `.f3d` is the source of truth; the STEPs and the STL are derived exports.

| File | Role |
|---|---|
| `Decca_Display_Mount_revP.f3d` | **editable source of truth** — fully parametric, 130 named user parameters |
| `Decca_Display_Mount_revP_fusion.py` | the generator that builds the `.f3d`; single source of truth for every dimension |
| `Decca_Display_Mount_revP_verify.py` | independent offline verification of the exported STL (numpy only) |
| `Rear_Display_Carrier_revP.step` | the one structural part |
| `Decca_Display_Mount_revP_assembly.step` | carrier + Perspex + OLED + bezel + **original nuts / bolt envelope** references. **No lighting-unit keepout proxy** — Rev P.4 deleted it, and both tools assert its absence |
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
> validated. Outstanding: measure the glass envelope (§9), the original nut
> across flats **and** across corners and the original bolt length (§21.6),
> print the hex-pocket fit coupon (§21.7), then prove on a real part —
> **printed in opaque black** — installed lighting-unit clearance (§14.14),
> rack/twist, the captive-nut behaviour, and the **powered light-leak test**
> (§14.22).
>
> **No CAD result in this folder proves lighting-unit clearance or freedom from
> light leakage.** There is no measured lighting-unit geometry and no LED
> measurement anywhere in the project. Both are physical tests.
