# CAD

Source (editable, parametric) mechanical design files.

**Intended contents**
- Fusion 360 archives (`.f3d`) and/or OpenSCAD (`.scad`) source.
- Neutral exchange formats (STEP `.step`) for interop.

**Conventions**
- Keep source here; export print-ready meshes to `../STL/`.
- Parametric source is preferred so parts can be re-derived if dimensions change.
- Record revisions in `docs/Revision History.md`.

## Display mount — current revision: **P.5 — RELEASED**

**The Rev P.5 carrier has been manufactured, installed and physically tested,
and every test passed:** Perspex fit and tolerances; OLED front insertion and
removal; all four sprung posts and retention; no collision with the original
Decca lighting unit; bottom / open connector-side clearance; the reduced
6.00 mm thickness; the enlarged 14.00 × 4.19 mm connector opening; the rear
closure and light-blocking features; the original fasteners and captive nuts;
49.00 mm horizontal pitch; the mounting points 7.00 mm lower giving the
required OLED position; and installed fit, screen position, stiffness,
retention, clearance and powered operation.

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

**Rev P.5** is a mandatory amendment that changes load-bearing numbers:

- both **plain locating posts are deleted** and replaced by sprung
  locating-and-retaining posts — all four PCB mounting holes now hold a split
  sprung post, and no plain-post parameter, body, branch or probe survives;
- the complete OLED reference is rotated **180° in plane**, so the four-pin
  connector is at the **bottom**. The panel-fixed holes do not move. **The open
  lighting-unit end of the carrier travelled with the module, +Y → −Y**;
- both carrier fixing centres then move **7.00 mm toward that bottom** relative
  to the OLED group (`carrier_fix_y_from_previous = -7.00 mm`). The Perspex
  holes are untouched, so the equivalent — and the only implementation that
  lands the carrier holes *on* them — is to raise the OLED bay **+7.00 mm**.
  This **supersedes** the earlier active-area-bottom-to-opening-bottom rule and
  every PASS based on it;
- the carrier drops to **6.00 mm** deep, the finished rear opening grows 25 % to
  **14.00 × 4.19 mm**, and two integral **light-block** baffles are added
  beside it, running out into the sprung pedestals.

Nothing numeric is inherited: the depth reduction shortens every cantilever, so
the split slot goes 0.70 → 1.20 mm and the root relief 3.20 → 2.00 mm. Build
review §25.3 has the recalculation.

> **The screen is no longer fully visible.** Only **8.30 mm** of the 14.70 mm
> active height falls inside the Perspex opening; about **6.40 mm — 44 % —**
> sits behind the fascia above it, and the lowest 7.00 mm of the opening shows
> unlit board. Both tools **report** this and neither passes a check on it.
> Whether the intended screen information is still readable is a question only
> the powered fit test can answer. Build review §28.3.

> **The bonded-glass boundary is now THE print gate.** The two converted posts
> put a nose ahead of the PCB at holes the plain posts never reached, and the
> modelled glass envelope — which has never been measured, and which puts the
> glass over the mounting holes — says it fouls by 0.40 mm. Both tools report
> those checks as **BLOCKED**, not passed and not failed. Measure the boundary,
> enter it, set `oled_glass_measured` / `GLASS_MEASURED`, and they become
> ordinary hard gates. Build review §25.4.

The `.f3d` is the source of truth; the STEPs and the STL are derived exports.

| File | Role |
|---|---|
| `Decca_Display_Mount_revP.f3d` | **editable source of truth** — fully parametric, 192 named user parameters |
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

> **Rev P.5 is RELEASED.** Every item that was outstanding here — the
> bonded-glass clearance, the original nut and bolt fit, the hex-pocket
> allowance, installed lighting-unit clearance, the light-leak test and the
> powered fit — was closed by the built and tested prototype. Both tools record
> them as `[TEST]`, and neither check was changed to get there.

> **What is still a modelling caveat, and is not a blocker.** Three inputs in
> the parameter table were never measured, and the prototype passing does not
> measure them:
>
> - `oled_glass_w` / `_h` / `_off_y` — the bonded-glass envelope is still the
>   placeholder that puts glass over the mounting holes. The built part clears
>   the real glass; the **model** does not describe it. `oled_glass_measured`
>   stays `False`;
> - `original_nut_hex_width` — 3.80 mm is still interpreted as **across
>   flats**. The real nuts fit the printed pocket, so the interpretation held,
>   but no across-corners figure was taken;
> - the original bolt length under the head. The bolts engage and clamp; the
>   length itself was not recorded.
>
> These matter only if the geometry is regenerated with changed dimensions. As
> built, the part is proven. Anyone changing a post, a nose, the glass keep-out
> or the nut pocket must measure first.
