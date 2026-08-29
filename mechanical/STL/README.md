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
| `Hex_Pocket_Fit_Coupon_revP.stl` | **Print this FIRST.** PETG, rear face flat on the bed, no supports. Five captive-nut pockets at 0.10/0.15/0.20/0.25/0.30 mm fit allowance, notch-numbered. Sets `nut_pocket_fit_allowance` from a physical part. 4.570 cm³. |
| `Rear_Display_Carrier_revP.stl` | PETG. **Rear face flat on the bed, building forward.** No supports. 4+ top layers or ironing on the Perspex seating face. Print the Ø2.80 split locating posts slowly — they stand 5.50 mm tall. 4.472 cm³ ≈ 5.7 g. |
| `Front_Bezel_revN.stl` | PETG, matt/satin black. **Unchanged for Rev P** — no revP-named file exists. |

> ## Rev P is NOT released — do not print the carrier yet
>
> The **Rev P.2** print **passed** its OLED retention and Perspex-fit tests. This
> mesh is **Rev P.3**, which keeps that architecture untouched and amends only
> the radio-side interface: the lighting-unit-side end rail and cable-tie
> projection are deleted, and the M2 heat-set inserts are replaced by captive
> pockets for the original Decca nuts.
>
> **Four measurements gate this print**, and all four are in
> `../Drawings/Decca_OLED_Display_Mount_CAD_Build_revP.md`:
>
> 1. the OLED glass envelope at the two header-side mounting holes — at least
>    2.10 mm from each hole centre to the nearest bonded-glass edge (§9);
> 2. the original nut **across flats and across corners** — 3.80 mm is modelled
>    as across flats (§21.6);
> 3. the original bolt length under the head — between 5.00 and 15.00 mm (§21.6);
> 4. the **hex-pocket fit coupon**, printed first (§21.7).
>
> Then the carrier may be printed as an integration prototype. Release still
> needs installed clearance against the lighting unit, a rack/twist check on the
> open frame, and the captive-nut and bolt tests.
>
> **One mandatory assembly-preparation step:** nothing on the OLED's display-side
> face may stand more than **1.00 mm** proud. The budget is
> `optical gap 0.30 + glass proud 0.80 = 1.10 mm`; 1.10 is the hard ceiling, aim
> for 1.00 or less. Preferred method — remove the pin header and solder the leads
> from the rear with the front-side joints dressed flush. This is a module
> preparation step, not a carrier issue: the carrier clears the tips at any
> length. See the build review §11.

Hardware is the **two original Decca bolts and their two original matching
nuts**. There are no heat-set inserts, no replacement screws and no adhesive.

Rev N meshes (`Rear_Display_Carrier_revN.stl`, `Retainer_Bar_revN.stl`) are
retained as the last front-loaded design. Rev P has no retainer bar.
