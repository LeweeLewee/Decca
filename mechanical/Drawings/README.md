# Drawings

Dimensioned engineering drawings for fabrication, measurement, and reference.

**Intended contents**
- PDF drawings with critical dimensions and tolerances.
- Reference sketches for cabinet fit and mounting.

## ESP32 controller housing — Rev B, **PROTOTYPE CAD, not physically validated**

| File | Contents |
|---|---|
| `Decca_ESP32_Controller_Housing_Spec_v1.0.md` | The controlling specification. Its content is revision **v1.1**; the filename is kept for link stability. Authority for the architecture. |
| `Decca_ESP32_Controller_Housing_Build_Report_revB.md` | Rev B build report: the Rev A before/after, derived dimensions, both verification suites and what they caught, the material arithmetic, every open prototype gate, print orientations and the recommended first print. |
| `Decca_ESP32_Controller_Housing_revB_01_closed.png` | Closed housing. |
| `..._02_lid_removed.png` | Lid removed, controller and breakout in place. |
| `..._03_exploded.png` | Exploded assembly. |
| `..._04_plan.png` / `..._05_elevation.png` | Overall plan and elevation. |
| `..._06_section.png` / `..._06b_section_oblique.png` | Longitudinal section on y = 0: floor, support height, carrier, ledge, clamp, lid overlap and cavity headroom in one view. |
| `..._07_terminal_access.png` | All thirty screwdriver corridors as solids, lid removed. |
| `..._08_cable_windows.png` | The four open-bottom cable windows with the grouped H1-H6 bundles passing through them. |
| `..._09_strain_relief.png` | The four internal cable-tie tabs, with ties and bundles. |
| `..._10_usb_access.png` | USB service envelope swept to the connector. |
| `..._11_cabinet_fixings.png` | The two recessed cabinet fixings, from below, against the underside-joint envelope. |
| `..._12_antenna_keepout.png` | Wi-Fi antenna keep-out. |
| `..._13_retention.png` | Fixed ledge and adjustable clamp against the no-contact envelope. |
| `..._14_locating_hooks.png` | The two locating hooks on the -X end. |
| `..._15_fit_gauge.png` | The fit gauge — print this one first. |

Every image is regenerated from the model by `images()`; none is posed by hand.
Keep-out volumes are drawn as translucent yellow solids and acquired hardware
as green, so a reader can tell manufacturing geometry from a dimensional
assumption without opening the browser.

The sixteen `..._revA_*.png` renders and the Rev A build report are removed:
they show lacing rails, mounting ears, sawtooth window roofs and a USB plug,
none of which exists any more. The useful historical finding — that Rev A was
rejected for bulk despite passing all eighteen of its gates — is carried
forward in sections 1 and 6.1 of the Rev B report.


## Active OLED mount design direction

`Decca_OLED_Display_Mount_CAD_Review_revO.md` is the authoritative carrier
architecture brief. It includes the 2026-08-29 Rev P physical-retention
correction: flush-side insertion onto fixed rear PCB datums, positive sprung-post
handling retention, and no release until the corrected print passes physical
retention tests. The 2026-08-29 integration amendment additionally makes the
original Decca lighting unit a mandatory physical clearance interface and
deletes the continuous carrier end rail / cable-tie projection below the
sprung-post pair as installed.
The same open Rev P correction now also deletes the M2 heat-set inserts and
replacement M2 screws: the original non-standard-thread Decca front bolts and
their matching six-sided captive nuts are reused at the unchanged 49.00 mm pitch.
The Rev P.3 follow-up rejects the unmeasured synthetic lighting-unit keepout
component and requires an integral opaque rear wall over the OLED bay, with only
a local four-pin/header opening, to prevent cabinet-light contamination.
The Rev P.5 packaging correction reduces carrier depth from 8.00 to 6.00 mm,
enlarges the finished pin opening by 25% in both axes to 14.00 × 4.19 mm, adds
two internal side light blocks within the back-plate envelope, places the
four-pin side at the bottom and moves both carrier fixing points 7.00 mm toward
that bottom relative to the OLED group. The original Perspex holes remain fixed
at 49.00 mm pitch, so this raises the screen 7.00 mm relative to the earlier
bottom-edge-aligned datum.
The same Rev P.5 amendment converts the two remaining plain locating posts to
sprung retaining posts, giving four sprung posts subject to measured glass
clearance, combined-force, PCB-bow and deliberate-release validation.

The released Rev P.5 carrier is now frozen. The active follow-on work is the
**Rev Q bezel-only amendment** in
`Decca_OLED_Display_Bezel_CAD_Brief_revQ.md`: replace the Rev N side-only
locating rails with a continuous inset masking wall around the complete Perspex
opening. A brief amendment and four owner changes have since re-scoped it — to
an interference fit with rounded corners and a larger visible opening, to a wall
carrying **at least two continuous 0.40 mm loops per side** rather than the
single loop the original 0.40 mm wall produced, and finally to an aperture that
is **flush with the skirt on all four sides**. Rev Q must not change the
carrier.

## Display bezel — Rev Q, **COMPLETE — signed off 2026-08-31**

**Rev Q is built, modelled, validated, printed, fitted and signed off by the
owner on 2026-08-31.** Built to brief commit `7b107f2` ("require two-loop
inset wall") plus four owner changes made on the model. The bezel is one
connected manifold solid: the Rev N face, envelope and external radii are
carried over, and the two Rev N side rails are replaced by a single continuous
inset masking wall, 2.30 mm deep, around all four sides and all four corners.
The wall is **1.25 mm on the sides** — thick enough for its inner face to sit
flush with the face opening, with no set-back — and **0.80 mm top and bottom**.
The bezel face opening is flush with the skirt on all four sides, so the
aperture is a straight bore with no taper. The two Rev N recessed adhesive pads
are deleted at owner instruction, so the underside is one unbroken seating face.

> **The opening has been measured, and it was not what the project believed.**
> 36.74 × 16.45, not the 35.20 × 15.30 carried from Rev C — which no released part
> had ever checked. The skirt is now **36.94 × 16.60**, derived from that
> measurement plus 0.100 mm per side across and 0.075 mm per side up. Treat the
> reading as ±0.2 mm; a further iteration is expected. Build report §3.10.
>
> **It fits, and it is signed off.** Confirmed on printed parts: the fit, the
> opening corner and the opening dimensions. A 2.30 mm depth was tried and
> reverted — the bottoming-out was a printing issue, not the geometry. The slicer
> two-loop preview and the powered test were not run as checks and are recorded
> as not-run rather than passed. Build report §3.11–§3.12.

| File | Role |
|---|---|
| `Decca_OLED_Display_Bezel_CAD_Brief_revQ.md` | **governing Rev Q brief** — the controlled requirement |
| `Decca_OLED_Display_Bezel_revQ_Build_Report.md` | **Rev Q build report and validation record — start here** |
| `Decca_OLED_Display_Bezel_revQ_front.png` | front view |
| `Decca_OLED_Display_Bezel_revQ_rear.png` | rear view |
| `Decca_OLED_Display_Bezel_revQ_oblique.png` | oblique |
| `Decca_OLED_Display_Bezel_revQ_lip_oblique.png` | rear three-quarter — the wall as a continuous closed ring |
| `Decca_OLED_Display_Bezel_revQ_assembly.png` | seated on the measured Perspex, clear of both fixing holes |
| `Decca_OLED_Display_Bezel_revQ_section.png` | section on x = 0 |
| `Decca_OLED_Display_Bezel_revQ_section_detail.png` | **the wall masking the Perspex cut edge** |
| `Decca_OLED_Display_Bezel_revQ_optical.png` | the lit OLED area behind the aperture, to scale |

The eight PNGs are generated by `snapshots()` in the Rev Q generator, so they
document the geometry that is actually in `Decca_Display_Bezel_revQ.f3d`.

Validation: **52/52 gates PASS** in Fusion and **47/47 PASS** in the independent
offline mesh verifier. One shell, one lump, zero slivers, no degenerate
triangles. Continuity is proved by **cross-section area**, which matches the
analytic value to four decimals at three depths and in every region including
the four R4.25 corners — a stronger proof than point sampling, since any gap or
thin spot anywhere removes area.

| | mm |
|---|---:|
| Bezel face opening, at the front face | **34.440 × 15.000**, R3.000 |
| Inset-wall outer / inner envelope | **36.940 × 16.600** / 34.440 × 15.000 (flush, all four sides) |
| Wall / corner radii | **1.250 sides / 0.800 top+bottom** / R4.250 outer, R3.000 inner |
| Insert depth | **2.800** — 2.300 tried and reverted, the cause was a print issue |
| Aperture | a straight bore — taper 0.00° |
| Fit | **0.100 interference** per horizontal side, **0.075 interference** per vertical side |
| **Effective clear optical opening** | **34.440 × 15.000** |

> **Three things the prototype must settle, and CAD cannot.**
>
> 1. **The fit.** 0.100 / 0.075 mm per side is ordinary on paper, but acrylic
>    stores stress rather than deforming, the 1.25 mm side wall is about **31×
>    stiffer in bending** than the original 0.40 mm, and **print tolerance is the
>    same size as the fit**. Print `Bezel_Fit_Gauge_revQ` first; it is mandatory,
>    not advisable. Build report §8.1.
> 2. **The opening measurement**, at ±0.2 mm — twice the interference it sets.
>    The gauge sweep brackets it, so one print resolves both. The opening
>    **corner** is largely closed: the owner's offer-up found R4.25 a good match,
>    and at R4.25 the flanks set the fit for every plausible corner. Build report
>    §8.3, §8.4.
> 3. **The optical result.** The clear opening is 32.90 × 13.85, the lit band
>    goes 8.100 → **8.150 mm** — above Rev N for the first time. Judge the
>    noticeably slimmer black border instead. A powered-test decision. Build
>    report §5.

> **A forced modelling decision, since designed out.** While the face opening
> was taller than the whole wall, a straight-walled aperture would have left the
> top and bottom wall runs detached from the bezel face, so the aperture tapered
> in Y. Making the face opening flush with the skirt on all four sides removed
> the condition: the aperture is now a straight bore, and the generator refuses
> to build if the two drift apart. Build report §3.3.

> **Eight owner changes on top of the brief, each recorded and each reversible.**
> The adhesive pads **deleted**; the outer corner **R2.00 → R3.00**; the aperture
> made **flush on the left and right** with the loop rule clarified to **at
> least** two per side; the **interference-fit refinement**; the **pull-back**;
> the corner **reverted to R3.00** on the render; **the opening measured** —
> which restored R4.25 on physical evidence and made the insert derive from
> the measurement; the **depth cut 2.80 → 2.30 mm** after a printed part fitted
> but bottomed out; and that cut **reverted** when the cause proved to be a
> printing issue, followed by **sign-off**. Build report §3.5 to §3.12.

## Display mount

| File | Role |
|---|---|
| `Decca_OLED_Display_Mount_Spec_v1.0.md` | approved specification, **now at v1.2** (the filename keeps `v1.0` for link stability). §2 holds the **measured and locked** Decca interface geometry: opening 35.20 × 15.30, fixing pitch **49.00 mm**. §4 opens the Rev Q bezel-only amendment. |
| `Decca_OLED_Display_Bezel_CAD_Brief_revQ.md` | **governing Rev Q bezel brief** — continuous thin masking lip around the complete Perspex opening; Rev P.5 carrier frozen |
| `Decca_OLED_Display_Mount_CAD_Review_revN.md` | last front-loaded build (Rev N) |
| `Decca_OLED_Display_Mount_CAD_Review_revO.md` | **the governing brief**, as amended 2026-08-29 by the Rev P physical-retention correction |
| `Decca_OLED_Display_Mount_Topology_revP.md` | Rev P pre-CAD topology gate. **Rev P.2 corrected topology** — flush-side insertion, fixed rear datum pads, positive stops in both axial directions; §13 the Rev P.4 rear light shield; §14–§16 the Rev P.5 four-post conversion, 180° datum and 6.00 mm depth |
| `Decca_OLED_Display_Mount_CAD_Build_revP.md` | **Rev P.5 build review and validation record** — start here |
| `Decca_OLED_Display_Mount_revP_posts.png` | **Rev P.5 carrier from the front — FOUR split sprung posts, one in every PCB mounting hole. Connector at the bottom; the two light blocks flank the four-pin opening and run out into the bottom pedestals** |
| `Decca_OLED_Display_Mount_revP_views.png` | **Rev P.5 assembly, straight on through the Perspex — where the active area actually sits in the opening after the 7.00 mm mounting correction. Rendered with appearances so it can be read: green active area, translucent fascia** |
| `Decca_OLED_Display_Mount_revP_rear.png` | **Rev P.5 rear three-quarter — the continuous integral light shield, the four post relief bores, the enlarged 14.00 × 4.19 mm four-pin opening at the bottom, and the two fixing bosses sitting LOW relative to the connector-side carrier after the 7.00 mm correction. No lighting keepout component is present** |
| `Decca_OLED_Display_Mount_revP_sections.png` | Rev P.5 section at x = +15, through a sprung locating post, with the Perspex, glass and PCB |
| `Decca_OLED_Display_Mount_revP_nut.png` | Rev P.5 half-section through a fixing centre — the bolt bore, hex head seat, retaining ridge and the original nut |

The five PNGs are generated by `snapshots()` in the Rev P generator, so they
always document the geometry that is actually in the `.f3d`.

Current mechanical revision: **P.5 — RELEASED**.

**The carrier has been manufactured, installed and physically tested, and every
test passed:**

| Test | Result |
|---|---|
| Perspex fit and tolerances | **PASS** |
| OLED front insertion and removal | **PASS** |
| All four sprung posts, retention | **PASS** |
| No collision with the original Decca lighting unit | **PASS** |
| Bottom / open connector-side clearance | **PASS** |
| Reduced 6.00 mm carrier thickness | **PASS** |
| Enlarged 14.00 × 4.19 mm four-pin connector opening | **PASS** |
| Rear closure and light-blocking features | **PASS** |
| Original fasteners and captive nuts | **PASS** |
| Horizontal mounting-hole pitch 49.00 mm | **PASS** |
| Mounting points 7.00 mm lower — required OLED position | **PASS** |
| Installed fit, screen position, stiffness, retention, clearance | **PASS** |
| Powered operation | **PASS** |

Everything below is the design and validation trail that got here. Where it
describes a check as open, blocked or awaiting a test, **that item is closed by
the prototype** — build review §29.

**Rev P.2 passed physically** for OLED retention and Perspex fit. That
architecture — flush-side insertion, fixed rear datum pads, plain and sprung
locating posts, the snap retention and release, the OLED Z position and 0.30 mm
gap, active-area centring, the 35.20 × 15.30 aperture, the exact 49.00 mm pitch,
the carrier-to-Perspex hard stops and the existing bezel — is carried forward
**unchanged**.

**Rev P.3** was a bounded amendment to the radio-side interface only:

1. the continuous end rail below the sprung-post pair and its integral cable-tie
   projection collided with the retained original Decca lighting unit, and are
   **deleted** — the carrier is now an open-ended frame (build review §20);
2. the original front bolts have a **non-standard thread**, so the M2 heat-set
   insert architecture is **deleted** and the original bolts and their matching
   nuts are reused in captive hex pockets (build review §21).

**Rev P.4** corrects two things in Rev P.3, again without touching the validated
OLED architecture:

3. the **synthetic lighting-unit keepout is deleted** — `build_light_keepout()`,
   `REF_Lighting_Keepout`, `LIGHTING_UNIT_KEEPOUT`, the derived geometry that
   placed it, its intersection checks, the fastener checks against it and every
   mention in the drawings and exports. Its boundary was asserted from the
   carrier's own pedestals rather than measured off the radio, so it could never
   fail and it misrepresented the assembly. Nothing replaces it; the proven rail
   cut is kept exactly as printed (build review §20.6);
4. the **rear of the OLED bay is closed** by a 1.20 mm integral opaque light
   shield, part of the carrier, with a single local 11.20 × 3.35 mm
   four-pin/header opening and no other penetration (build review §24).

**Rev P.5** is a mandatory amendment, and unlike its predecessors it changes
load-bearing numbers:

5. both **plain locating posts are deleted** and replaced by sprung
   locating-and-retaining posts — **four sprung posts**, one per PCB mounting
   hole (build review §25);
6. the module is rotated **180° in plane**: connector at the **bottom**,
   panel-fixed holes unmoved. The carrier's open lighting-unit end travelled
   with it, +Y → −Y (§26);
7. the carrier drops to **6.00 mm**, the finished rear opening grows 25 % to
   **14.00 × 4.19 mm**, and two integral **light-block** baffles are added
   beside it (§27).

The depth reduction shortens every cantilever, so the split slot goes
0.70 → 1.20 mm and the root relief 3.20 → 2.00 mm; worst-case post strain rises
to 2.42 % against a 3.00 % limit and combined insertion force is 28.6 N.

8. both carrier fixing centres then move **7.00 mm toward that bottom**
   relative to the OLED group (`carrier_fix_y_from_previous = -7.00 mm`). The
   Perspex holes are untouched, so the equivalent — and the only implementation
   that lands the carrier holes *on* them — is to raise the OLED bay
   **+7.00 mm**. This **supersedes** the active-area-bottom-to-opening-bottom
   rule and every PASS based on it (§28).

**The screen is not fully visible, by design.** Only **8.30 mm** of the
14.70 mm active height falls inside the Perspex opening; about **6.40 mm —
44 %** — sits behind the fascia above it, and the lowest 7.00 mm of the opening
shows unlit board. Both tools report that geometry and neither passes a check on
it. **The powered fit test confirmed the resulting position is the required
one** and that the intended screen information is visible (§28.3).

*These were the gates before the build; all are now closed by the prototype.*
The powered fit and screen-position test (§28.3), the
bonded-glass boundary at all four holes (§25.4), the
nut across flats **and** across corners (§21.6), the original bolt length
(§21.6), and the hex-pocket fit coupon (§21.7). Gating release: installed
lighting-unit clearance (a **re-test**, not a regression check), rack/twist of
the open frame, the captive-nut and bolt tests, the four-post
seat/retain/release test, and the **powered light-leak test** with the carrier
printed in opaque black (§14.22).

**Neither CAD nor the mesh verifier proves the bonded-glass boundary,
lighting-unit clearance or freedom from light leakage.** None of the three was
ever measured — and all three were settled by the physical prototype instead,
which is what both tools always said would be required.

> **Modelling caveat, not a blocker.** The bonded-glass envelope and the
> original bolt length remain unmeasured placeholders in the parameter table.
> The built part works; the model does not describe those two. Measure before
> regenerating any post, nose or glass keep-out.
>
> The nut across-flats figure of **3.80 mm was confirmed on 2026-08-30** and is
> no longer a caveat.

Module preparation is unchanged — front-side solder protrusion ≤ 1.00 mm.
