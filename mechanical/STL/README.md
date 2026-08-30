# STL

Print-ready meshes exported from the CAD sources.

**Intended contents**
- `.stl` (or `.3mf`) files ready to slice and print.
- Optional print notes (orientation, supports, material) alongside each part.

**Conventions**
- STLs are derived artefacts — the editable source lives in `../CAD/`.
- Name files to match their CAD source and revision.

## Display bezel — current revision: **Q — OPEN, integration prototype**

**Rev Q is bezel-only. The Rev P.5 carrier mesh below is FROZEN and unchanged.**

| File | Print notes |
|---|---|
| `Bezel_Fit_Gauge_revQ_GAUGE_I{000,005,010,015,020}.stl` | **Print these FIRST, with the production profile.** PETG, front face flat on the bed, no supports. Five end-tabs, notch-numbered 1…5, at **0.00 / 0.05 / 0.10 / 0.15 / 0.20 mm horizontal interference per side**. Each is the complete right-hand end of the real Rev Q wall — full 15.20 mm height, both R2.00 corners, the real 0.80 mm two-loop wall, the real 2.80 mm depth — so it engages the interference exactly as the bezel will. ≈1.54 cm³ ≈ 2 g for all five. |
| `Front_Bezel_revQ.stl` | PETG, matt/satin **black**. **FRONT FACE FLAT ON THE BED, wall pointing up. No supports.** 40.00 × 20.30 × **4.00 mm**, 0.6056 cm³ ≈ 0.77 g. The 0.80 mm continuous inset wall must slice as **exactly two 0.40 mm loops** — see the print gate below. 4+ top/bottom layers or ironing on the bed face; it is the only surface anyone sees. |

> ### Rev Q print gate 1 — TWO CONTINUOUS WALL LOOPS
>
> This is why the wall is 0.80 mm. At 0.40 mm the slicer resolved it as a
> single loop, which is what the owner correction rejects.
>
> | Setting | Value |
> |---|---|
> | Nozzle / extrusion width | **0.40 mm** — the wall *is* two of these |
> | Layer height | 0.15–0.20 mm |
> | Perimeters in the wall | **2** — not "auto", not variable-width |
> | Thin-wall / gap fill | **OFF** if the slicer allows; a full 0.80 mm needs none |
> | Arachne / variable width | **prefer classic** — Arachne may merge 0.80 into ONE 0.8 mm-wide extrusion, which is a single loop and **fails** |
> | External perimeter speed | **≤ 25 mm/s** through the wall |
> | Cooling | 100 % |
> | Supports | **none** |
>
> **Step through every layer of the wall in the slicer preview before
> printing.** Confirm two continuous 0.40 mm loops around the complete
> perimeter — both straight runs, both ends, **and all four R2.00 corners**.
> **Reject** the profile on any of: a single variable-width wall, a missing
> second loop, gap fill substituted for a loop, or the two loops locally merged
> into one wide extrusion. Fix the slicer — do not thicken `bezel_lip_wall` to
> work around it without recording why.
>
> **If your extrusion width is not 0.40 mm**, set `bezel_lip_wall` to **two**
> *actual* extrusion widths and regenerate; the inner envelope, corner radii,
> aperture and optical opening are all derived and follow. The generator
> refuses to build a wall that is not a whole multiple of `extrusion_width`.

> ### Rev Q print gate 2 — THE INTERFERENCE FIT
>
> The wall is **0.10 mm per horizontal side WIDER than the hole** by design,
> and at 0.80 mm it is about **8× stiffer in bending** than the 0.40 mm wall it
> replaces — so it resists that interference roughly 8× harder. Brief §3.8
> requires the printed wall to take the deflection and the original Perspex to
> be left unspread and unstressed. **CAD cannot settle that.** Print the fit
> gauge first, find the largest interference that seats by hand and releases
> without marking or whitening the Perspex, and set `bezel_lip_outer_w` from
> the physical result before printing a bezel.

> ### What this print costs optically
>
> The clear opening is **30.90 × 13.60 mm** — width by the face opening, height
> by the wall — and the visible lit band drops from 8.100 to **7.450 mm**, all
> of it at the top. Only the powered test can say whether that is acceptable.
>
> Full detail, the fit study and the test procedure:
> `../Drawings/Decca_OLED_Display_Bezel_revQ_Build_Report.md`.

`Front_Bezel_revN.stl` remains the last **released** bezel mesh and is
unchanged. The first issue's `Bezel_Corner_Gauge_revQ_*` meshes are deleted —
the corner radius is now specified at R2.00, so the fit gauge replaces the
corner gauge.

---

## Display mount — current revision: **P.5 — RELEASED**

| File | Print notes |
|---|---|
| `Hex_Pocket_Fit_Coupon_revP.stl` | **Print this FIRST.** PETG, rear face flat on the bed, no supports. Five captive-nut pockets at 0.10/0.15/0.20/0.25/0.30 mm fit allowance, notch-numbered. Sets `nut_pocket_fit_allowance` from a physical part. 4.570 cm³. |
| `Rear_Display_Carrier_revP.stl` | PETG **in OPAQUE BLACK**. **Rear face flat on the bed, building forward.** No supports. 4+ top layers or ironing on the Perspex seating face. Print the **four** Ø2.80 split sprung posts slowly — they stand 4.40 mm tall on a 0.80 mm half-section (exactly two 0.40 mm perimeters). **Print the 1.20 mm rear light shield fully solid** — it is the first 6 layers, flat on the bed; solid perimeters, never sparse infill and never a single translucent skin. The two light blocks grow up off it. 56.60 × 39.15 × **6.00 mm**, 4.411 cm³ ≈ 5.6 g. |
| `Front_Bezel_revN.stl` | PETG, matt/satin black. **Unchanged for Rev P** — no revP-named file exists. This is the last **released** bezel mesh; the OPEN Rev Q above supersedes it for new work but is not yet released. |

> ## Rev P.5 is RELEASED — this mesh has been printed and tested
>
> The carrier printed from this mesh has been installed in the radio and passed
> every physical test: Perspex fit, OLED insertion and removal, four-post
> retention, lighting-unit clearance, connector-side clearance, the 6.00 mm
> thickness, the enlarged connector opening, the rear closure and light blocks,
> the original captive-nut fasteners, 49.00 mm pitch, the 7.00 mm lower
> mounting points and powered operation.
>
> Print it **in opaque black** with the rear light shield solid — that is a
> functional requirement, not a finish choice.
>
> <details><summary>The pre-build gates, retained for the record</summary>
>
> The **Rev P.2** print **passed** its OLED retention and Perspex-fit tests. This
> mesh is **Rev P.5**. Rev P.3 amended
> the radio-side interface — the lighting-unit-side end rail and cable-tie
> projection are deleted, and the M2 heat-set inserts are replaced by captive
> pockets for the original Decca nuts. Rev P.4 then deleted the synthetic
> lighting-unit keepout reference (it was asserted, never measured) and **closed
> the rear of the OLED bay** with a 1.20 mm integral opaque light shield,
> leaving only a local four-pin/header opening.
>
> **Rev P.5 then changed load-bearing numbers.** Both plain locating posts are
> deleted and replaced by sprung retaining posts — **four sprung posts now, one
> per mounting hole**. The module is rotated **180°**, putting the connector at
> the **bottom**, and both carrier fixing centres then move **7.00 mm toward
> that bottom** relative to the OLED group — which, with the Perspex holes
> untouched, raises the screen 7.00 mm in the assembly.
> The carrier drops to **6.00 mm**, the finished opening grows to
> **14.00 × 4.19 mm**, and two light blocks flank it. The shorter carrier forces
> the split slot to 1.20 mm and the root relief to 2.00 mm; worst-case post
> strain rises from 1.66 % to **2.42 %** against a 3.00 % limit, and combined
> insertion force is **28.6 N** across the four posts.
>
> **Four measurements gate this print**, and all four are in
> `../Drawings/Decca_OLED_Display_Mount_CAD_Build_revP.md`:
>
> 1. the OLED glass envelope at the two header-side mounting holes — at least
>    2.10 mm from each hole centre to the nearest bonded-glass edge (§9);
> 2. the original nut **across flats and across corners** — 3.80 mm is modelled
>    as across flats (§21.6);
> 3. the original bolt length under the head — between 5.00 and 15.00 mm (§21.6);
> 4. the **hex-pocket fit coupon**, printed first (§21.7);
> 5. **the powered fit and screen-position test (§28.3).** Install on the
>    original Perspex holes with the original bolts, confirm the open connector
>    side is at the bottom and both holes align without forcing or slotting,
>    power the OLED and **photograph** the visible active-area edges. Only
>    **8.30 mm** of the 14.70 mm active height falls inside the opening — about
>    **6.40 mm sits above it** and the lowest 7.00 mm of the opening shows
>    unlit board. CAD reports that; only the powered part can say whether it is
>    acceptable;
> 6. **the bonded-glass boundary at ALL FOUR holes (§25.4) — this one blocks the
>    print.** The two converted posts put a retaining nose ahead of the PCB at
>    holes the plain posts never reached. The modelled glass envelope says the
>    far pair fouls by 0.40 mm — and the same model puts the glass over the
>    mounting holes, which is impossible for a screw-mounted board. Measure hole
>    centre to nearest glass edge at all four holes, model it, and re-run both
>    tools. Until then the glass checks report **BLOCKED**, not passed.
>
> Then the carrier may be printed as an integration prototype — **in opaque
> black**, which is a functional requirement, not a finish choice: the rear
> light shield only works if the material does not transmit the cabinet
> lighting. If your nozzle or extrusion width is not 0.40 mm, raise
> `rear_light_shield_t` to at least three *actual* extrusion widths and
> regenerate before slicing.
>
> Release still needs, on a real part: installed clearance against the lighting
> unit — a **RE-TEST**, not a regression check, because the 180° transform moved
> the carrier's open end to the other side of the fixing bolts — a rack/twist
> check on the open frame, the captive-nut and bolt tests, the **four-post
> seat / retain / release test (§12.28)**, and the **powered light-leak test** — cabinet LEDs through their usable
> brightness range with the OLED showing black, dim and normal content, checking
> for rear glow, edge leakage, a bright patch at the pin opening, Perspex
> illumination around the aperture and any contrast loss.
>
> **No CAD or mesh check in this repository proves the bonded-glass boundary,
> lighting-unit clearance or freedom from light leakage.** None of the three has
> ever been measured; the synthetic keepout that implied otherwise was deleted
> at Rev P.4.
>
> </details>

**All six gates above are now closed by the built and tested part.** Both tools
record them as `[TEST]` and neither check was changed to get there.

> **What is still a modelling caveat, and is not a blocker.** The bonded-glass
> envelope and the original bolt length were never measured. The built part
> works; the **model** still carries placeholders for those two, and
> `oled_glass_measured` / `GLASS_MEASURED` stay `False`. Measure before
> regenerating any post, nose or glass keep-out.
>
> The nut across-flats figure of **3.80 mm was confirmed on 2026-08-30** and is
> no longer a caveat — the nut pocket can be regenerated as it stands.
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
