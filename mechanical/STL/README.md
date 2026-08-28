# STL

Print-ready meshes exported from the CAD sources.

**Intended contents**
- `.stl` (or `.3mf`) files ready to slice and print.
- Optional print notes (orientation, supports, material) alongside each part.

**Conventions**
- STLs are derived artefacts — the editable source lives in `../CAD/`.
- Name files to match their CAD source and revision.

## Display mount — current revision: **P**

| File | Print notes |
|---|---|
| `Rear_Display_Carrier_revP.stl` | PETG. **Rear face flat on the bed, building forward.** No supports. 4+ top layers or ironing on the Perspex seating face. Print the 0.75 mm snap fingers slowly. 7.151 cm³ ≈ 9.1 g. |
| `Front_Bezel_revN.stl` | PETG, matt/satin black. **Unchanged for Rev P** — no revP-named file exists. |

> **Rev P is NOT yet released for print.** One of the mandatory validations
> fails: at the brief's 1.50 mm the OLED's trimmed front-side solder tips strike
> the original Perspex by 0.40 mm. No carrier geometry can fix that — the carrier
> is not in the path. Resolve it before printing, either by preparing the module
> to ≤ 1.00 mm front-side protrusion (the carrier is then correct unchanged) or
> by setting `oled_perspex_gap = 0.80` and rebuilding. See
> `../Drawings/Decca_OLED_Display_Mount_CAD_Build_revP.md` §8.

Rev N meshes (`Rear_Display_Carrier_revN.stl`, `Retainer_Bar_revN.stl`) are
retained as the last front-loaded design. Rev P has no retainer bar.
