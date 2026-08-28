# CAD

Source (editable, parametric) mechanical design files.

**Intended contents**
- Fusion 360 archives (`.f3d`) and/or OpenSCAD (`.scad`) source.
- Neutral exchange formats (STEP `.step`) for interop.

**Conventions**
- Keep source here; export print-ready meshes to `../STL/`.
- Parametric source is preferred so parts can be re-derived if dimensions change.
- Record revisions in `docs/Revision History.md`.

---

## Display mount — Rev O (current)

Rev O is a clean redesign of the OLED carrier: the module loads from the rear,
the glass projects forward through a window, and there is no separate retainer
bar. See `../Drawings/Decca_OLED_Display_Mount_CAD_Build_revO.md`.

| File | What it is |
|---|---|
| `Decca_Display_Mount_revO_fusion.py` | **The model.** The parametric generator. Run it inside Fusion 360 to build Rev O as a brand-new design and write `Decca_Display_Mount_revO.f3d`. |
| `Decca_Display_Mount_revO_verify.py` | Offline validator and exporter. Parses the parameter table and the body recipes out of the generator and rebuilds them on OpenCascade, so the checks run against the same recipe Fusion will run. `pip install cadquery` first. |
| `Rear_Display_Carrier_revO.step` | The carrier, exported by the validator. |
| `Decca_Display_Mount_revO_assembly.step` | Carrier + panel + OLED reference + bezel. |

`Decca_Display_Mount_revO.f3d` is produced by running the generator in Fusion —
a `.f3d` is a Fusion archive and can only be written by Fusion itself. The
generator creates a **new** document; it never opens or Save-As-es the Rev N
file. Build instructions are in the build review, §11.

The front bezel is **unchanged** from Rev N. `Front_Bezel_revN.step` and
`../STL/Front_Bezel_revN.stl` remain the files of record for it.

## Display mount — Rev N (historical baseline)

Kept untouched as the tested prototype baseline. `Decca_Display_Mount_revN.f3d`,
`Decca_Display_Mount_revN_assembly.step`, `Rear_Display_Carrier_revN.step`,
`Front_Bezel_revN.step`, `Retainer_Bar_revN.step`. The Rev N retainer bar is not
used by Rev O.
