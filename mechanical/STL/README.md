# STL

Print-ready meshes exported from the CAD sources.

**Intended contents**
- `.stl` (or `.3mf`) files ready to slice and print.
- Optional print notes (orientation, supports, material) alongside each part.

**Conventions**
- STLs are derived artefacts — the editable source lives in `../CAD/`.
- Name files to match their CAD source and revision.

## Display mount — current revision: **P — OPEN, NOT RELEASED**

| File | Print notes |
|---|---|
| `Rear_Display_Carrier_revP.stl` | PETG. **Rear face flat on the bed, building forward.** No supports. 4+ top layers or ironing on the Perspex seating face. Print the Ø2.80 split locating posts slowly — they stand 5.50 mm tall. 6.928 cm³ ≈ 8.8 g. |
| `Front_Bezel_revN.stl` | PETG, matt/satin black. **Unchanged for Rev P** — no revP-named file exists. |

> ## Rev P is NOT released — do not print this yet
>
> The first Rev P print **failed its physical retention test**: the OLED fell
> forward out of the loose carrier. This mesh is the corrected **Rev P.2**
> geometry — flush-side insertion onto four fixed rear datum pads, with forward
> escape blocked by two sprung post hooks rather than by friction. It passes
> every CAD and mesh check, but **one measurement is still outstanding and it
> gates the print**: the OLED glass envelope at the two header-side mounting
> holes, which must be at least 2.10 mm from each hole centre to the nearest
> bonded-glass edge. See `../Drawings/Decca_OLED_Display_Mount_CAD_Build_revP.md`
> §9.
>
> After that measurement this mesh may be printed as a
> **geometry-and-retention prototype**. The retention finding closes only when a
> printed carrier holds the module through an inversion and gentle-shake test —
> §14.
>
> **One mandatory assembly-preparation step:** nothing on the OLED's display-side
> face may stand more than **1.00 mm** proud. The budget is
> `optical gap 0.30 + glass proud 0.80 = 1.10 mm`; 1.10 is the hard ceiling, aim
> for 1.00 or less. Preferred method — remove the pin header and solder the leads
> from the rear with the front-side joints dressed flush. This is a module
> preparation step, not a carrier issue: the carrier clears the tips at any
> length. See the build review §11.

Rev N meshes (`Rear_Display_Carrier_revN.stl`, `Retainer_Bar_revN.stl`) are
retained as the last front-loaded design. Rev P has no retainer bar.
