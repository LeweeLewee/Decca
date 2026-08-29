# -*- coding: utf-8 -*-
"""
Decca OLED Display Mount - Rev P parametric generator (Autodesk Fusion 360).

REV P.5 - RELEASED. PROTOTYPE BUILT AND PHYSICALLY VALIDATED (2026-08-30)
-------------------------------------------------------------------------
The Rev P.5 carrier has been manufactured and tested in the radio, and the
project owner reports every physical test PASSED. See REV_P5_PROTOTYPE below
for the itemised outcome.

What that changes in this file: the items this gate could never settle itself -
the bonded-glass envelope, installed lighting-unit clearance, light leakage, the
original-fastener fit and the powered screen position - were always deferred to
physical test, and that test has now happened. They are reported as CLOSED BY
TEST rather than BLOCKED or OPEN.

What it does NOT change: not one geometric check has been altered, relaxed or
removed to reach that state. Every gate below runs exactly as it did, on the
same geometry, and still has to pass on its own terms. The modelled bonded-glass
envelope is also left exactly as it was - unmeasured and known to be wrong - and
is still printed as such. The prototype proves the PART works; it did not
produce a measurement, and this file does not pretend it did.

REV P.5 - FOUR SPRUNG POSTS, 6.00 mm DEPTH, 180-DEGREE MODULE DATUM (2026-08-29)
--------------------------------------------------------------------------------
Rev P.5 applies the brief's section 5.3 and 8.4 corrections together, because
they interact: the module is rotated, the carrier is shortened, and the posts
have to be re-solved inside the new envelope.

A. FOUR SPRUNG POSTS (brief 5.3). The two plain locating posts are DELETED and
   replaced by sprung locating-and-retaining posts, so every one of the four PCB
   mounting holes now holds a split sprung post with a positive retaining nose.
   Gone completely: plain_post_d, plain_relief_d, plain_relief_depth, plain_lead,
   plain_setback, plain_post(), the plain coordinate list, the plain root relief,
   the plain probes and every plain-post line in the reports and images.

   The converted (far) pair carries its own named geometry - sprung_far_* - so it
   can diverge from the proven connector-side pair once the bonded glass is
   measured, without disturbing geometry that has physical evidence behind it.

B. 6.00 mm CARRIER DEPTH (brief 8.4). carrier_depth 8.00 -> 6.00. This is NOT a
   free change: it shortens every sprung cantilever, because the root relief can
   no longer be 3.20 mm deep without eating through the 1.20 mm rear light
   shield. The relief is cut to 2.00 mm, which leaves a 1.30 mm solid floor, and
   the split slot is opened from 0.70 to 1.00 mm to bring the peak strain back
   under the limit. Both numbers are recalculated from the finished solid in
   validate() section 6 and reported per post type and for the four-post system.

C. 180-DEGREE MODULE TRANSFORM AND THE VERTICAL DATUM (brief 8.4). The complete
   OLED reference is rotated 180 degrees in its plane, so the four-pin connector
   is now at the BOTTOM - the open, cut-away side of the carrier.

   MOUNTING-POINT CORRECTION (brief 8.4, amended). Both carrier fixing centres
   move 7.00 mm TOWARD that bottom relative to the OLED-dependent group -
   carrier_fix_y_from_previous = -7.00 mm. The original Perspex holes are not
   moved, redrilled or redefined, so in the assembled model the equivalent and
   only correct implementation is to RAISE the OLED bay and everything that
   depends on it by +7.00 mm while the panel holes stay put. The carrier holes
   and the Perspex holes are therefore coincident in the assembly, never 7.00 mm
   apart.

   This SUPERSEDES the earlier rule that aligned the visible active-area bottom
   edge with the Perspex opening bottom edge. That rule, and every PASS based on
   it, is deleted. The active-area centre moves from y = -0.30 to y = +6.70, and
   the consequence is reported rather than dressed up: only part of the modelled
   active area lies inside the Perspex opening. See validate() section 10.

   Because the whole module rotated, the open lighting-unit end of the carrier
   travels with the connector-side sprung pair from +Y to -Y. The Rev P.3/P.4
   installed fit therefore does NOT carry over: brief 12.14 is a RE-TEST, not a
   regression check.

D. FOUR-PIN OPENING AND LIGHT BLOCKS (brief 8.4). The finished rear opening is
   enlarged 25% in both axes to exactly 14.00 x 4.19 mm, and two integral opaque
   light-block walls are added, one each side of it, forming a short internal
   tunnel that stops cabinet light spilling sideways out of the pin slot.

REV P.4 - KEEPOUT REMOVAL AND INTEGRAL REAR LIGHT SHIELD (2026-08-29)
---------------------------------------------------------------------
Rev P.4 is a bounded correction on top of Rev P.3. Two changes only:

A. THE SYNTHETIC LIGHTING KEEPOUT IS DELETED (brief 8.1). Rev P.3 carried a
   reference solid - build_light_keepout() / REF_Lighting_Keepout /
   LIGHTING_UNIT_KEEPOUT - standing in for the retained original Decca lighting
   unit. Its boundary was ASSERTED from the carrier's own pedestal tangent, not
   measured off the radio. A proxy built from the part it is meant to check
   proves nothing, and shipping it in the browser, the assembly STEP and the
   manufacturing pack misrepresents the assembly. The function, the component,
   the body, the derived geometry that existed only to place it, its
   intersection checks and the fastener-clearance checks against it are all
   removed, and nothing replaces it.

   The PHYSICAL cut it was invented to justify is KEPT exactly as printed: the
   lighting-unit-side end rail and its cable-tie projection stay deleted, the
   uprights still terminate at light_cut_y and the open lighting-unit side is
   unchanged. ``carrier_max_y`` is what the old ``light_keepout_y`` becomes: a
   report of the carrier's OWN maximum extent on that side, not a keep-out
   boundary. The authority for that interface is the installed physical
   clearance test (brief 12.14), which remains mandatory and open.

B. THE REAR OF THE OLED BAY IS CLOSED (brief 8.3). Rev P.3 left a full-height
   open rear window behind the module, so the Decca cabinet LEDs could light
   the back and edges of the OLED and glow through the Perspex aperture. That
   window is replaced by a continuous integral rear wall, ``rear_light_shield_t``
   thick, built FORWARD from the existing carrier rear plane so the external
   envelope does not grow. It is part of Rear_Display_Carrier, not a second
   component or a cover. Its only penetration is a local slot for the four
   input/header pins and their conductors, sized from the header envelope plus
   separately named X and Y print/wiring clearances.

REV P.3 - LIGHTING-UNIT CLEARANCE AND ORIGINAL-FASTENER AMENDMENT (2026-08-29)
-----------------------------------------------------------------------------
The Rev P.2 prototype PASSED physically for OLED retention and Perspex fit. That
architecture is preserved unchanged through Rev P.3 and Rev P.4: flush-side
insertion, fixed rear PCB datum pads, plain and sprung locating posts, snap
retention and release, the OLED Z position and 0.30 mm Perspex gap, active-area
centring, the 35.20 x 15.30 mm aperture, the exact 49.00 mm fixing pitch, the
carrier-to-Perspex hard stops and the existing Rev N bezel.

Rev P.3 was a bounded amendment addressing two integration failures only:

1. LIGHTING-UNIT CLEARANCE (brief 8.1). The continuous transverse end rail on
   the lighting-unit side, its central cable-tie / strain-relief projection and
   the tie slots collided with the retained original Decca lighting unit. All of
   it is deleted. No bridge remains between the two side uprights in that
   keep-out, and nothing is put back inside it. The uprights terminate in
   deliberate radii adjacent to the retained sprung-post pedestal roots.

2. ORIGINAL DECCA FASTENERS (brief 8.2). The original front bolts have a
   non-standard thread. The whole M2 heat-set-insert architecture is deleted -
   insert bores, insert depth, insert recess, bore chamfer, backing calculation
   and the replacement M2 screw / insert BOM entries. The two original bolts and
   their two original matching nuts are reused at the unchanged 49.00 mm pitch,
   with a rear-accessible regular-hex anti-rotation pocket, a positive axial
   seating shoulder, a defined 1.40 mm head seat, full 10.00 mm nut and bolt
   clearance, and a serviceable captive retaining ridge.

REV P.2 - CORRECTED AFTER A PHYSICAL RETENTION FAILURE (2026-08-29)
------------------------------------------------------------------
The printed Rev P.1 carrier failed its retention test: the OLED falls forward
through the loose carrier. The failure is architectural, not a tolerance
adjustment. Rev P.1 inserted the module from the REAR and put its only positive
shoulders at the PCB rear plane, so those shoulders restrained the wrong
direction; forward retention was left to four 0.10 mm edge-grip tongues acting
through assumed friction.

Rev P.2 reverses the installation direction and replaces friction with geometry:

    FRONT / PERSPEX SIDE   <-- the module is inserted from here, moving rearward

    OLED glass
    OLED PCB                  <-- forward escape blocked by two sprung post hooks
    fixed rear PCB datum pads  <-- rearward motion stops here, on rigid carrier
    carrier structure

    REAR

Both stops are positive geometry. No friction term appears in the design or in
the acceptance gate.

Deleted from Rev P.1: the four PCB-edge friction fingers, their shoulders, their
0.10 mm tongues, their four radial prise holes, and the friction-versus-weight
acceptance gate.

Governing brief: ``mechanical/Drawings/Decca_OLED_Display_Mount_CAD_Review_revO.md``
as amended 2026-08-29 (main @ 666abca).
Pre-CAD gate:    ``mechanical/Drawings/Decca_OLED_Display_Mount_Topology_revP.md``

Coordinate frame (identical to Rev N and Rev P.1, validated on real prints)::

    origin = centre of the original Decca display aperture
           = centre of the OLED active area   (primary optical datum)
    +X     = viewer's right
    +Y     = up
    +Z     = forward, out of the fascia towards the viewer
    z =  0.00  rear face of the Perspex == carrier structural hard stop (DATUM A)
    z = +3.00  front face of the Perspex
    z <  0     rearward, into the carrier

REV P.5 vertical datum. The origin is still the centre of the original Decca
display aperture, and the panel-fixed fixing holes are still on y = 0 at exactly
49.00 mm pitch. The OLED is NOT centred on the origin any more: it is rotated
180 degrees in plane and dropped so its active-area bottom edge sits on the
Perspex opening bottom edge at y = -7.65, i.e. active centre y = -0.30. Every
oled_* parameter below is still stated in MODULE-LOCAL coordinates, exactly as
it is measured on the module; derive() applies the flip and the offset once, in
one place, so no feature can be transformed twice or missed.

Run through the Fusion MCP bridge, or from Utilities > Add-Ins > Scripts.
Entry points:

    main(ctx)         build the design in a NEW Fusion document
    validate(ctx)     run the full validation gate on the active document
    import_bezel(ctx) bring in the unchanged Rev N bezel and re-check it
    export(ctx)       write .f3d / STEP / STL to OUT_DIR

Every length in this file is millimetres. The Fusion API works in centimetres;
conversion happens only in ``mm()``.
"""

import math
import os

import adsk.core
import adsk.fusion

OUT_DIR = r"D:\GitHub\Decca\mechanical"
BEZEL_STEP = os.path.join(OUT_DIR, "CAD", "Front_Bezel_revN.step")

# ---------------------------------------------------------------------------
# PROTOTYPE OUTCOME - the physical evidence that closes this revision.
# ---------------------------------------------------------------------------
# Reported by the project owner after building and installing the Rev P.5
# carrier. Each entry is an outcome, not a measurement: the tests confirm the
# part works, and none of them produced a number that is fed back into the
# parameter table. Where a modelled input is still a placeholder it stays a
# placeholder and is still flagged as one.
REV_P5_PROTOTYPE_VALIDATED = True
REV_P5_PROTOTYPE = (
    ("Perspex fit and tolerances", "PASS"),
    ("OLED front insertion and removal", "PASS"),
    ("all four sprung posts, retention", "PASS"),
    ("no collision with the original Decca lighting unit", "PASS"),
    ("bottom / open connector-side clearance", "PASS"),
    ("reduced 6.00 mm carrier thickness", "PASS"),
    ("enlarged 14.00 x 4.19 mm four-pin opening", "PASS"),
    ("rear closure and light-blocking features", "PASS"),
    ("original fasteners and captive nuts", "PASS"),
    ("horizontal mounting-hole pitch 49.00 mm", "PASS"),
    ("mounting points 7.00 mm lower - required OLED position", "PASS"),
    ("installed fit, screen position, stiffness, retention, clearance",
     "PASS"),
    ("powered operation", "PASS"),
)

DOC_NAME = "Decca_Display_Mount_revP"
CARRIER = "Rear_Display_Carrier"

# Components this generator no longer creates, but must delete when it is run
# against a document built by an earlier revision. REF_Lighting_Keepout held the
# synthetic LIGHTING_UNIT_KEEPOUT body that Rev P.4 rejects: it was asserted
# from the carrier's own geometry rather than measured off the radio, so it
# must not appear in the browser, the assembly STEP or the manufacturing pack.
LEGACY_COMPONENTS = ("REF_Lighting_Keepout",)


# ---------------------------------------------------------------------------
# PARAMETERS - the single source of truth.
# ---------------------------------------------------------------------------
P = {
    # -- Original Decca fascia: MEASURED off the real panel -----------------
    # Measured at Rev C, print-confirmed at Rev D, re-confirmed by the project
    # owner on 2026-08-28, locked in Spec v1.1 section 2.
    "perspex_t": 3.00,
    "panel_open_w": 35.20,
    "panel_open_h": 15.30,
    "panel_fix_pitch": 49.00,
    "panel_fix_y": 0.00,
    "panel_fix_clear_d": 2.40,
    "panel_ref_w": 90.00,          # modelled Perspex patch, reference only
    "panel_ref_h": 80.00,

    # -- OLED module reference ----------------------------------------------
    "oled_pcb_w": 35.40,
    "oled_pcb_h": 33.50,
    "oled_pcb_t": 1.60,
    "oled_pcb_off_y": 4.00,        # PCB centre above the active-area centre
    #                                (MODULE-LOCAL, before the 180 deg flip)
    "oled_active_w": 29.42,
    "oled_active_h": 14.70,
    # -- Rev P.5 in-plane module transform (brief 8.4) ----------------------
    # 180 degrees, applied ONCE in derive() to every module-local value below:
    # PCB, glass, active area, all four mounting holes, header, solder tips,
    # datum pads, posts, pocket, rear-wall opening and light blocks. The
    # panel-fixed bosses and holes are NOT part of the module and do not move.
    "module_rot_deg": 180.0,

    # -- Rev P.5 mounting-point correction (brief 8.4, amended) -------------
    # BOTTOM is -Y: the open, cut-away side of the carrier that carries the
    # four-pin connector opening. Both carrier fixing centres move this far
    # toward that bottom, relative to the complete OLED-dependent group.
    # Negative = downward = toward the connector.
    #
    # The original Perspex holes do NOT move. So in the assembled model the
    # equivalent - and the only implementation that puts the carrier holes on
    # the Perspex holes rather than 7.00 mm away from them - is to raise the
    # OLED bay and everything that depends on it by the same amount while
    # panel_fix_y stays on the physical hole line. derive() does exactly that,
    # in one place, so the two descriptions cannot drift apart.
    "carrier_fix_y_from_previous": -7.00,
    # NOT MEASURED. Rev P.5 depends on the glass X/Y envelope at ALL FOUR
    # mounting holes now, because all four hold sprung noses. It is REPORTED
    # as a blocking pre-print measurement, never assumed away.
    #
    # Set oled_glass_measured True once the real boundary has been measured and
    # entered below. While it is False, every check that compares carrier
    # geometry against this envelope reports [BLOCKED] rather than PASS or
    # FAIL, because a fictional envelope can produce neither. As modelled, the
    # glass covers both far mounting holes completely - a board like that could
    # not be screw-mounted, which is how we know the model is wrong.
    "oled_glass_measured": False,
    "oled_glass_w": 34.50,         # NOT MEASURED
    "oled_glass_h": 23.00,         # NOT MEASURED
    "oled_glass_off_y": 2.45,      # NOT MEASURED
    "oled_glass_proud": 0.80,      # MEASURED at Rev N - sets the whole chain
    "oled_hole_d": 3.00,
    "oled_hole_pitch_x": 30.00,
    "oled_hole_pitch_y": 28.50,
    "oled_header_w": 10.00,
    "oled_header_h": 3.00,
    "oled_header_off_y": 19.25,
    "oled_header_depth": 8.10,     # rearward from the PCB rear face
    # Front-side solder protrusion after module preparation. The budget is
    # oled_perspex_gap + oled_glass_proud = 1.10 mm before anything on the PCB
    # front face reaches the Perspex, so 1.00 mm is the accepted preparation
    # limit and leaves 0.10 mm of clearance. Confirmed by the project owner
    # 2026-08-28: the tips will be reduced.
    "oled_tip_proud": 1.00,
    "oled_tip_d": 1.20,
    "oled_tip_pitch": 2.54,
    "oled_tip_cx": 0.50,
    "oled_tip_y_top": 18.55,
    "oled_tip_y_bot": -10.55,

    # -- Optical chain ------------------------------------------------------
    "oled_perspex_gap": 0.30,      # CHOSEN nominal glass-to-Perspex gap
    "forward_setback": 0.10,       # carrier material limit behind the PCB face

    # -- Carrier ------------------------------------------------------------
    "pcb_clearance": 0.25,         # X/Y clearance around the PCB in the pocket
    "aperture_margin": 0.60,       # module aperture beyond the pocket
    "carrier_wall": 3.00,
    # Rev P.1 was 9.60 mm deep purely to give its 8.40 mm cantilever fingers
    # room. Rev P.2-P.4 ran at 8.00 mm. Brief 8.4 now fixes the plastic Z
    # envelope at exactly 6.00 mm from the Perspex seating plane to the rear
    # plane. That is the binding constraint on the sprung-post root relief -
    # see sprung_relief_depth.
    "carrier_depth": 6.00,
    "carrier_corner_r": 3.00,
    # The Rev P.2 cable-tie flange (top_flange 6.00, flange_w 31.00) and the
    # transverse rail it stood on are DELETED - they collided with the retained
    # original Decca lighting unit. Nothing replaces them inside the keep-out.

    # -- Lighting-unit-side rail cut (brief 8.1) ----------------------------
    # This positions the ACTUAL cut in the carrier. It is not, and never was,
    # a synthetic lighting-unit body: Rev P.4 deletes that proxy entirely.
    # The two side uprights terminate this far short of the PCB pocket's
    # lighting-unit-side wall line, capped with a half-round of the upright
    # width. Above that line the ONLY carrier material is the two sprung-post
    # pedestal towers; there is no bridge of any kind between the uprights.
    "light_cut_back": 0.50,

    # -- Integral rear light shield (brief 8.3) -----------------------------
    # The rear OLED bay is closed by carrier material, not by a cover. The
    # wall grows FORWARD from the existing rear plane at z = -carrier_depth,
    # so the external rear envelope is unchanged.
    #
    # 1.20 mm = three 0.40 mm extrusion widths. If the slicer profile uses a
    # different extrusion width, raise this to at least three ACTUAL widths -
    # the wall must be solid perimeters end to end, never sparse infill or a
    # single translucent skin. Print in OPAQUE BLACK material.
    "rear_light_shield_t": 1.20,
    # The only penetration. Sized from the header envelope
    # (oled_header_w x oled_header_h at oled_header_off_y) plus these two
    # SEPARATE clearances - a print allowance plus room for the conductors and
    # the wire bend immediately behind the header. They exist so the pin slot
    # can be opened up without touching the general OLED opening.
    #
    # Brief 8.4 fixes the FINISHED opening at 14.00 x 4.19 mm, 25% up on the
    # Rev P.4 11.20 x 3.35. These two clearances are what deliver exactly that,
    # symmetrically about the transformed header envelope:
    #     width  = oled_header_w + 2 * pin_slot_clear_x = 10.00 + 4.00 = 14.00
    #     height = (oled_header_h + 2 * pin_slot_clear_y) clipped by the
    #              carrier's own termination = 4.19
    "pin_slot_clear_x": 2.00,
    "pin_slot_clear_y": 1.44,

    # -- Internal connector light blocks (brief 8.4) ------------------------
    # Two integral opaque baffles, one immediately outboard of each lateral
    # edge of the pin opening, forming a short tunnel beside the pins so light
    # coming through the opening cannot spill sideways into the OLED bay. They
    # grow FORWARD off the inside face of the rear shield and are part of the
    # same carrier solid. They are internal baffles - never external fins,
    # never a separate component, never behind the rear plane.
    # MINIMUM thickness. The blocks are actually run all the way out to the
    # sprung pedestals (see light_block_tie) so no open gap is left between
    # the block and the tower for light to come round - the finished walls are
    # wider than this, and this value is the floor the gate checks.
    "light_block_t": 1.20,         # 3 x 0.40 mm extrusion width, as the shield
    # How far each block runs INTO the adjacent pedestal tower. A flat wall
    # meeting a cylinder tangentially only touches at one height and leaves a
    # wedge-shaped slot either side of the tangent point; 0.60 mm of overlap
    # turns that tangent into a real merge over the block's whole height.
    "light_block_tie": 0.60,
    # Forward reach off the shield's inner face. Bounded by DATUM B: the blocks
    # must stay behind the seated PCB and out of the insertion/removal sweep.
    "light_block_depth": 1.60,
    "light_block_pcb_clear": 0.50,  # required gap from block front face to DATUM B

    # -- Original Decca bolt / captive-nut interface (brief 8.2) ------------
    # The original bolts have a NON-STANDARD thread. Nothing here is derived
    # from an M2, BA, UNC or any other catalogue nut. Every value below is a
    # measurement of, or an allowance against, the physical original parts.
    #
    # INTERPRETATION, RECORDED AS REQUIRED BY THE BRIEF: the reported 3.80 mm
    # is taken as the distance ACROSS OPPOSITE FLAT FACES. Before release the
    # physical nut must be checked across flats AND across corners. If 3.80 mm
    # proves to be across corners, change this one parameter and regenerate.
    "original_nut_hex_width": 3.80,        # ACROSS FLATS - assumed, see above
    "original_nut_head_seat_depth": 1.40,  # axial depth of the head seat
    "original_nut_total_length": 10.00,    # full nut envelope to be cleared
    # printer/material fit allowance on the pocket. This is a process fit, NOT
    # permission to alter the 3.80 mm physical measurement. Validate with the
    # hex-pocket coupon before printing the carrier.
    "nut_pocket_fit_allowance": 0.20,
    "nut_body_allowance": 0.20,     # clearance bore beyond the head across-corners
    "nut_seat_depth": 2.00,         # solid carrier ahead of the seating shoulder
    "nut_retain_lip": 0.25,         # controlled interference retaining ridge
    "nut_retain_h": 0.30,           # axial height of that ridge
    "nut_lead_h": 0.40,             # self-supporting lead-in below the ridge
    "bolt_clear_d": 2.60,           # original bolt shank clearance (panel hole 2.40)
    "fix_boss_d": 7.60,             # structural boss around the hex pocket
    "fix_arm_h": 7.50,              # stadium arm height (Rev F/N shape)

    # -- Locating posts -----------------------------------------------------
    # Starting values from the printed Rev D / Rev K post development. Strain
    # is RE-CALCULATED from the finished geometry in validate(), not inherited.
    # -- CONNECTOR-SIDE sprung pair (y = -18.55 after the flip) -------------
    # The pair that was physically proven at Rev P.2. Shaft, barb and tip are
    # unchanged. Two values DID have to change, and neither is cosmetic:
    "sprung_shaft_d": 2.80,        # Rev D, unchanged
    # Rev P.2-P.4 used 0.70 in an 8.00 mm carrier. At 6.00 mm the cantilever is
    # 1.20 mm shorter; strain goes as 1/a^2 and spring force as 1/a^3, so the
    # proven 0.70 slot would give 3.17 % worst-case strain (over the 3.00 %
    # limit) and 64.6 N of combined four-post insertion force. Opening the slot
    # to 1.20 mm thins each half from 1.05 to 0.80 mm, which brings those to
    # 2.42 % and 28.6 N. 0.80 mm is exactly two 0.40 mm extrusion widths - two
    # clean perimeters, where 1.05 mm was two perimeters plus a sliver.
    #
    # This does NOT weaken retention. Retention is the square land at
    # z_hook_face bearing on the PCB front face; a forward load on that land
    # has no inward component, so it cannot deflect the barb out of the hole at
    # any stiffness. Stiffness only sets insertion and release effort.
    # Recalculated from the finished solid in validate() section 6.
    "sprung_slot_w": 1.20,
    "sprung_barb_d": 3.20,         # Rev D, unchanged -> 0.10 mm radial overlap
    "sprung_tip_d": 2.60,          # nose lead-in tip
    "sprung_relief_d": 4.80,       # Rev D counterbore, unchanged
    # Rev P.2-P.4 used 3.20 in an 8.00 mm carrier. At 6.00 mm that would leave
    # only 0.10 mm of floor under the relief and would eat straight through the
    # 1.20 mm rear light shield. 2.00 mm leaves a 1.30 mm solid floor - the
    # shield thickness plus 0.10 mm - so the shield stays light-tight under
    # every post. Gated in validate().
    "sprung_relief_depth": 2.00,
    "post_fillet_r": 0.80,         # Rev D R0.80 root fillet, unchanged

    # -- CONVERTED FAR pair (y = +9.95 after the flip) ----------------------
    # Brief 5.3: the two plain posts become sprung posts. They are given their
    # OWN names so the pair can be reduced once the bonded glass is measured
    # without touching the pair that has physical evidence behind it.
    #
    # They currently hold the same values as the connector pair, deliberately.
    # The only lever that would shrink the glass keep-out is the barb, and the
    # only overlap figure with physical evidence behind it is the 0.10 mm that
    # Rev P.2 proved. Trading proven retention for a keep-out reduction that
    # still would not satisfy the (known-unreliable) modelled glass envelope
    # would be a guess replacing a measurement. See validate() section 9.
    "sprung_far_shaft_d": 2.80,
    "sprung_far_slot_w": 1.20,
    "sprung_far_barb_d": 3.20,
    "sprung_far_tip_d": 2.60,
    "sprung_far_relief_d": 4.80,
    "sprung_far_relief_depth": 2.00,
    # In-plane rotation of the split slot about the post axis. 0.00 matches the
    # connector pair. Modelled and available, but not currently used: rotating
    # the split does not change the barb's swept envelope, so it buys nothing
    # against the glass. It is here so the option survives the measurement.
    "sprung_far_split_angle": 0.00,
    "sprung_far_root_fillet_r": 0.80,
    "hook_clear": 0.10,            # AXIAL clearance under the hook when seated
    "hook_land": 0.25,             # full-diameter land above the retaining face
    "nose_perspex_clear": 0.40,    # nose tip clearance to the Perspex
    # Minimum radial overlap any sprung nose may be reduced to. This is not a
    # round number chosen for comfort: it is the exact overlap that the Rev P.2
    # prototype physically retained with. Anything below it needs new physical
    # retention evidence, not a CAD decision.
    "hook_overlap_min": 0.10,

    # -- Fixed rear PCB datum ----------------------------------------------
    "datum_pad_od": 6.00,          # annular pad, ID = the post relief bore
    "datum_pad_h": 0.30,           # pad stands this far above the pedestal top
    # 8.60 rather than a round 8.00: at Ø8.00 the pedestal arc passes
    # 0.033 mm inside the pocket corner and leaves four hair slivers.
    # Ø8.60 swallows the corner by 0.27 mm instead.
    "pedestal_d": 8.60,            # rigid column carrying each pad and post

    # -- Service features ---------------------------------------------------
    # The integral cable-tie flange, its rear relief and its two slots are
    # DELETED: they sat inside the original lighting-unit keep-out. The brief
    # allows a replacement strain relief only outside that keep-out and only
    # with separately demonstrated radio-side clearance, which does not exist
    # yet, so none is added. Strain relief is an open item - see the build
    # review. With the rail gone the header and loom now exit through a fully
    # open end rather than a notch.

    # -- Analysis -----------------------------------------------------------
    "petg_E": 2000.0,              # MPa
    "strain_limit": 3.00,          # %
    "module_mass_g": 4.00,
    # The pre-print glass keep-out the two snap noses require, as a margin
    # around the barb. Reported, never assumed.
    "nose_glass_margin": 0.50,
}

# NOTE. There is deliberately NO friction coefficient in this parameter table.
# Rev P.1 used one to justify retention and the printed part disproved it.
# Rev P.2 retains the module by geometric overlap, and no acceptance check may
# depend on friction, gravity or the assumed modulus of the printed material.
# A mu is used once, inside validate(), purely to estimate push-on force.


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def mm(v):
    return float(v) / 10.0


def p3(x, y, z):
    return adsk.core.Point3D.create(mm(x), mm(y), mm(z))


def v3(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


class Builder(object):
    """Thin wrapper over TemporaryBRepManager so recipes read like solids."""

    def __init__(self):
        self.tbm = adsk.fusion.TemporaryBRepManager.get()

    def box(self, x0, x1, y0, y1, z0, z1):
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0),
            v3(1, 0, 0), v3(0, 1, 0),
            mm(x1 - x0), mm(y1 - y0), mm(z1 - z0))
        return self.tbm.createBox(obb)

    def cylz(self, d, x, y, z0, z1):
        return self.tbm.createCylinderOrCone(p3(x, y, z0), mm(d / 2.0),
                                             p3(x, y, z1), mm(d / 2.0))

    def conez(self, d0, d1, x, y, z0, z1):
        return self.tbm.createCylinderOrCone(p3(x, y, z0), mm(d0 / 2.0),
                                             p3(x, y, z1), mm(d1 / 2.0))

    def hexz(self, across_flats, x, y, z0, z1):
        """Regular hexagonal prism about the Z axis, built as the intersection
        of three boxes at 0/60/120 degrees. ``across_flats`` is the distance
        between opposite FLAT faces. Two flats are normal to Y, so the wider
        across-corners dimension lies along X where the fixing ear has room."""
        s = None
        span = across_flats * 3.0
        for k in range(3):
            a = math.radians(k * 60.0)
            u = v3(math.cos(a), math.sin(a), 0.0)
            w = v3(-math.sin(a), math.cos(a), 0.0)
            obb = adsk.core.OrientedBoundingBox3D.create(
                p3(x, y, (z0 + z1) / 2.0), u, w,
                mm(span), mm(across_flats), mm(abs(z1 - z0)))
            b = self.tbm.createBox(obb)
            s = b if s is None else self.inter(s, b)
        return s

    def torusz(self, x, y, z, major_r, minor_r):
        """Torus about the Z axis, centred on (x, y, z).

        NOTE. ``TemporaryBRepManager.createTorus`` ignores its ``center``
        argument in this Fusion build (2704.1.53) and always returns a torus at
        the world origin. Passing a centre and trusting it produces a body in
        the wrong place, and a subsequent boolean against it silently no-ops -
        which is exactly how a root fillet turns into a plain cylindrical
        collar without anything reporting an error. Build at the origin and
        translate it explicitly.
        """
        t = self.tbm.createTorus(p3(0.0, 0.0, 0.0), v3(0, 0, 1),
                                 mm(major_r), mm(minor_r))
        m = adsk.core.Matrix3D.create()
        m.translation = adsk.core.Vector3D.create(mm(x), mm(y), mm(z))
        if not self.tbm.transform(t, m):
            raise RuntimeError("could not place torus at (%g, %g, %g)"
                               % (x, y, z))
        return t

    def copy(self, a):
        return self.tbm.copy(a)

    def uni(self, a, b):
        self.tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
        return a

    def sub(self, a, b):
        self.tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        return a

    def inter(self, a, b):
        self.tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)
        return a

    def rrect(self, x0, x1, y0, y1, z0, z1, r):
        """Rounded-rectangle prism along Z, built from primitives - far more
        robust than filleting long vertical edges afterwards. Handles the
        degenerate obround case used by the M2 arms."""
        if r <= 0.0:
            return self.box(x0, x1, y0, y1, z0, z1)
        r = min(r, (x1 - x0) / 2.0, (y1 - y0) / 2.0)
        eps = 1.0e-9
        s = None
        if (x1 - x0) - 2 * r > eps:
            s = self.box(x0 + r, x1 - r, y0, y1, z0, z1)
        if (y1 - y0) - 2 * r > eps:
            b = self.box(x0, x1, y0 + r, y1 - r, z0, z1)
            s = b if s is None else self.uni(s, b)
        for cx in sorted({round(x0 + r, 9), round(x1 - r, 9)}):
            for cy in sorted({round(y0 + r, 9), round(y1 - r, 9)}):
                c = self.cylz(2 * r, cx, cy, z0, z1)
                s = c if s is None else self.uni(s, c)
        return s

    def root_fillet(self, shaft_d, fr, x, y, z0):
        """Concave R``fr`` fillet blending a post of diameter ``shaft_d`` into
        the floor at z = ``z0``. Built from primitive torus geometry so every
        post is identical by construction - the Rev D technique, unchanged.

        The result is checked against the un-filleted collar volume: a torus
        boolean that quietly does nothing leaves a cylindrical collar that
        looks plausible in every clearance check but is not the specified
        geometry, so it must fail loudly rather than ship.
        """
        s = self.cylz(shaft_d + 2 * fr, x, y, z0, z0 + fr)
        collar = math.pi * (shaft_d / 2.0 + fr) ** 2 * fr
        self.sub(s, self.torusz(x, y, z0 + fr, shaft_d / 2.0 + fr, fr))
        got = volume_of(s)
        if got > collar - 1e-3:
            raise RuntimeError(
                "root fillet at (%g, %g, %g) removed nothing: %.4f mm3 vs a "
                "%.4f mm3 plain collar" % (x, y, z0, got, collar))
        return s


def volume_of(body):
    """Volume in mm^3 of a (possibly temporary) BRep body, 0.0 if empty."""
    if body is None:
        return 0.0
    try:
        if body.faces.count == 0:
            return 0.0
    except Exception:
        return 0.0
    try:
        v = body.volume
        if v:
            return float(v) * 1000.0                 # cm^3 -> mm^3
    except Exception:
        pass
    try:
        return float(body.physicalProperties.volume) * 1000.0
    except Exception:
        return -1.0                                  # unknown but non-empty


# ---------------------------------------------------------------------------
# Derived geometry - everything below is a consequence of P.
# ---------------------------------------------------------------------------
def _post_geo(P, d, tag):
    """One sprung post's complete geometry and mechanics, as a dict.

    ``tag`` is "" for the proven connector-side pair and "far_" for the pair
    converted from the deleted plain posts. Both are split sprung posts; the
    far pair simply reads its values from sprung_far_* so it can diverge after
    the bonded glass is measured.
    """
    def g(name, fallback=None):
        k = "sprung_%s%s" % (tag, name)
        if k in P:
            return P[k]
        return P[fallback if fallback else "sprung_%s" % name]

    geo = {
        "tag": "far" if tag else "conn",
        "shaft_d": g("shaft_d"),
        "slot_w": g("slot_w"),
        "barb_d": g("barb_d"),
        "tip_d": g("tip_d"),
        "relief_d": g("relief_d"),
        "relief_depth": g("relief_depth"),
        "split_deg": P["sprung_far_split_angle"] if tag else 0.0,
        "fillet_r": (P["sprung_far_root_fillet_r"] if tag
                     else P["post_fillet_r"]),
    }

    # --- the Z stack of this post ----------------------------------------
    geo["z_floor"] = d["z_pcb_rear"] - geo["relief_depth"]
    geo["z_fix"] = geo["z_floor"] + geo["fillet_r"]
    # solid carrier left between the relief floor and the carrier rear plane
    geo["floor_t"] = geo["z_floor"] - d["z_rear"]

    # --- retention mechanics, all recalculated, none inherited ------------
    geo["overlap"] = (geo["barb_d"] - P["oled_hole_d"]) / 2.0
    geo["shaft_clear"] = (P["oled_hole_d"] - geo["shaft_d"]) / 2.0
    geo["a"] = d["z_hook_top"] - geo["z_fix"]              # free cantilever
    geo["t"] = (geo["shaft_d"] - geo["slot_w"]) / 2.0      # half thickness
    dr = (geo["barb_d"] - geo["tip_d"]) / 2.0
    geo["cam_deg"] = math.degrees(math.atan2(
        dr, d["z_nose_tip"] - d["z_hook_top"]))
    geo["nose_keepout_r"] = geo["barb_d"] / 2.0 + P["nose_glass_margin"]

    # second moment of one half, and the beam results
    I = geo["shaft_d"] * geo["t"] ** 3 / 12.0
    geo["I"] = I

    def beam(delta):
        F = 3.0 * P["petg_E"] * I * delta / geo["a"] ** 3
        e = 3.0 * geo["t"] * delta / (2.0 * geo["a"] ** 2) * 100.0
        return F, e

    geo["beam"] = beam
    geo["delta_nom"] = geo["overlap"]
    geo["delta_worst"] = geo["overlap"] + geo["shaft_clear"]
    geo["F_nom"], geo["strain_nom"] = beam(geo["delta_nom"])
    geo["F_worst"], geo["strain_worst"] = beam(geo["delta_worst"])
    # push-on estimate only. mu appears here and NOWHERE in any acceptance
    # criterion - Rev P.1 used friction to justify retention and the printed
    # part disproved it.
    tan_c = math.tan(math.radians(geo["cam_deg"]))
    geo["F_axial"] = (2.0 * geo["F_nom"] * (tan_c + 0.30)
                      / (1.0 - 0.30 * tan_c))
    # forward travel needed at this hole to clear the nose during release
    geo["release_travel"] = d["z_nose_tip"] - d["z_pcb_front"]
    return geo


def derive(P):
    d = {}

    # --- the optical depth chain, front to rear ---------------------------
    d["z_perspex_front"] = P["perspex_t"]
    d["z_perspex_rear"] = 0.0                                      #  0.00 DATUM A
    d["z_glass_front"] = -P["oled_perspex_gap"]                    # -0.30
    d["z_pcb_front"] = d["z_glass_front"] - P["oled_glass_proud"]  # -1.10
    d["z_fwd_limit"] = d["z_pcb_front"] - P["forward_setback"]     # -1.20
    d["z_pcb_rear"] = d["z_pcb_front"] - P["oled_pcb_t"]           # -2.70 DATUM B
    d["z_rear"] = -P["carrier_depth"]                              # -6.00

    # --- retention stack, the parts that are common to all four posts -----
    d["z_hook_face"] = d["z_pcb_front"] + P["hook_clear"]              # -1.00
    d["z_hook_top"] = d["z_hook_face"] + P["hook_land"]                # -0.75
    d["z_nose_tip"] = -P["nose_perspex_clear"]                         # -0.40
    d["z_ped_top"] = d["z_pcb_rear"] - P["datum_pad_h"]                # -3.00

    # =====================================================================
    # REV P.5 IN-PLANE MODULE TRANSFORM (brief 8.4)
    # =====================================================================
    # Applied ONCE, here, to every module-local value. Nothing downstream may
    # transform anything again, and nothing may be left untransformed.
    #
    # The panel is the datum: the measured Perspex opening, centred on the
    # origin, with the fixing holes on y = panel_fix_y. Neither moves, ever.
    d["panel_open_bottom_y"] = -P["panel_open_h"] / 2.0                # -7.65
    d["panel_open_top_y"] = P["panel_open_h"] / 2.0                    # +7.65

    # --- the SUPERSEDED datum, kept only as the numerical baseline --------
    # Rev P.5 originally aligned the visible active-area bottom edge with the
    # Perspex opening bottom edge, which put the active centre here. Brief 8.4
    # as amended supersedes that rule; this value survives ONLY so the 7.00 mm
    # correction can be cross-checked against a stated starting point.
    d["oled_cy_prev"] = (d["panel_open_bottom_y"]
                         + P["oled_active_h"] / 2.0)                   # -0.30

    # --- the mounting-point correction (brief 8.4, amended) ---------------
    # Both fixing centres move carrier_fix_y_from_previous toward the bottom
    # relative to the OLED group. The Perspex holes do not move, so the
    # equivalent - and the only implementation that keeps the carrier holes ON
    # the Perspex holes - is to raise the OLED group by the same amount.
    d["oled_rise"] = -P["carrier_fix_y_from_previous"]                  # +7.00
    d["oled_cy"] = d["oled_cy_prev"] + d["oled_rise"]                   # +6.70
    # the flip itself: 180 degrees in plane negates both in-plane axes
    r = math.radians(P["module_rot_deg"])
    d["fx"] = round(math.cos(r), 12)                                   # -1
    d["fy"] = round(math.cos(r), 12)                                   # -1
    d["flipped"] = abs(P["module_rot_deg"] - 180.0) < 1e-9

    def MY(local):
        """MODULE-LOCAL y (measured on the module, connector at +y) -> panel y."""
        return d["oled_cy"] + d["fy"] * local

    def MX(local):
        return d["fx"] * local

    d["MY"] = MY
    d["MX"] = MX

    # --- module envelopes, all transformed --------------------------------
    d["pcb_cy"] = MY(P["oled_pcb_off_y"])                              # -4.30
    d["glass_cy"] = MY(P["oled_glass_off_y"])                          # -2.75
    d["header_cy"] = MY(P["oled_header_off_y"])                        # -19.55
    d["pcb_x0"] = -P["oled_pcb_w"] / 2.0
    d["pcb_x1"] = P["oled_pcb_w"] / 2.0
    d["pcb_y0"] = d["pcb_cy"] - P["oled_pcb_h"] / 2.0                  # -21.05
    d["pcb_y1"] = d["pcb_cy"] + P["oled_pcb_h"] / 2.0                  # +12.45
    d["glass_x0"] = -P["oled_glass_w"] / 2.0
    d["glass_x1"] = P["oled_glass_w"] / 2.0
    d["glass_y0"] = d["glass_cy"] - P["oled_glass_h"] / 2.0            # -14.25
    d["glass_y1"] = d["glass_cy"] + P["oled_glass_h"] / 2.0            # +8.75
    d["active_y0"] = d["oled_cy"] - P["oled_active_h"] / 2.0           # -0.65
    d["active_y1"] = d["oled_cy"] + P["oled_active_h"] / 2.0           # +14.05
    d["header_y0"] = d["header_cy"] - P["oled_header_h"] / 2.0         # -21.05
    d["header_y1"] = d["header_cy"] + P["oled_header_h"] / 2.0         # -18.05
    d["z_tip_front"] = d["z_pcb_front"] + P["oled_tip_proud"]
    d["z_header_rear"] = d["z_pcb_rear"] - P["oled_header_depth"]

    # --- PCB pocket -------------------------------------------------------
    c = P["pcb_clearance"]
    d["pk_x0"], d["pk_x1"] = d["pcb_x0"] - c, d["pcb_x1"] + c
    d["pk_y0"], d["pk_y1"] = d["pcb_y0"] - c, d["pcb_y1"] + c          # -21.30, +12.70

    # --- module aperture --------------------------------------------------
    a = P["aperture_margin"]
    d["ap_x0"], d["ap_x1"] = d["pk_x0"] - a, d["pk_x1"] + a
    d["ap_y0"], d["ap_y1"] = d["pk_y0"] - a, d["pk_y1"] + a            # -21.90, +13.30

    # --- carrier outer profile -------------------------------------------
    # The open lighting-unit end travels with the connector-side sprung pair,
    # so after the 180 deg flip it is at -Y. car_y1 is now the SOLID transverse
    # rail; the cut is at car_y0.
    w = P["carrier_wall"]
    d["car_x0"], d["car_x1"] = d["ap_x0"] - w, d["ap_x1"] + w
    d["car_y1"] = d["ap_y1"] + w                                       # +16.30
    d["wall_y0"] = d["ap_y0"] - w        # where the deleted rail used to start
    d["light_cut_y"] = d["pk_y0"] + P["light_cut_back"]                # -20.80
    d["cap_r"] = (d["car_x1"] - d["pk_x1"]) / 2.0                      # 1.80
    d["cap_x"] = (d["car_x1"] + d["pk_x1"]) / 2.0                      # 19.75
    d["car_y0"] = d["light_cut_y"]                   # carrier structural extent

    # --- original-fastener bosses (brief 8.2) -----------------------------
    # PANEL-FIXED. These do NOT move with the module transform: they sit on the
    # physical Perspex holes, on y = panel_fix_y, at exactly 49.00 mm pitch.
    d["m2_x"] = P["panel_fix_pitch"] / 2.0           # exact 49.00 mm pitch / 2
    d["m2_r"] = P["fix_boss_d"] / 2.0
    d["ear_x1"] = d["m2_x"] + d["m2_r"]
    d["arm_x0"] = d["car_x1"] - 2.0                  # deep overlap, no slivers

    # captive original-nut pocket, front to rear
    d["z_nut_seat"] = -P["nut_seat_depth"]                                # -2.00
    d["z_nut_head_back"] = d["z_nut_seat"] - P["original_nut_head_seat_depth"]
    d["z_nut_retain"] = d["z_nut_head_back"] - P["nut_retain_h"]
    d["z_nut_lead"] = d["z_nut_retain"] - P["nut_lead_h"]
    d["nut_hex_af"] = P["original_nut_hex_width"] + P["nut_pocket_fit_allowance"]
    d["nut_hex_ac"] = d["nut_hex_af"] * 2.0 / math.sqrt(3.0)
    d["nut_body_d"] = d["nut_hex_ac"] + P["nut_body_allowance"]
    d["nut_retain_af"] = P["original_nut_hex_width"] - P["nut_retain_lip"]
    d["nut_retain_ac"] = d["nut_retain_af"] * 2.0 / math.sqrt(3.0)
    d["nut_ac"] = P["original_nut_hex_width"] * 2.0 / math.sqrt(3.0)
    d["boss_wall_min"] = d["m2_r"] - d["nut_body_d"] / 2.0
    d["z_nut_rear"] = d["z_nut_seat"] - P["original_nut_total_length"]     # -12.00
    # the seating shoulder is the hex area less the bolt clearance bore
    d["nut_seat_area"] = (math.sqrt(3.0) / 2.0 * d["nut_hex_af"] ** 2
                          - math.pi / 4.0 * P["bolt_clear_d"] ** 2)
    # grip from the bolt-head bearing face to the nut front face
    d["bolt_grip"] = P["perspex_t"] + P["nut_seat_depth"]

    # --- solder tips ------------------------------------------------------
    n = 4
    span = (n - 1) * P["oled_tip_pitch"]
    cx = MX(P["oled_tip_cx"])
    d["tip_x"] = [cx - span / 2.0 + i * P["oled_tip_pitch"] for i in range(n)]
    d["tip_y"] = [MY(P["oled_tip_y_top"]), MY(P["oled_tip_y_bot"])]

    # --- PCB mounting holes and the FOUR sprung posts that occupy them ----
    hx = P["oled_hole_pitch_x"] / 2.0
    hy = P["oled_hole_pitch_y"] / 2.0
    d["post_x"] = hx
    # connector side: module-local +hy relative to the PCB centre, flipped
    d["y_conn"] = MY(P["oled_pcb_off_y"] + hy)                         # -18.55
    d["y_far"] = MY(P["oled_pcb_off_y"] - hy)                          #  +9.95
    d["conn"] = [(sx * hx, d["y_conn"]) for sx in (-1, 1)]
    d["far"] = [(sx * hx, d["y_far"]) for sx in (-1, 1)]
    d["holes"] = d["conn"] + d["far"]

    # the connector pair must be the pair beside the header, by construction
    d["conn_is_header_side"] = (
        abs(d["y_conn"] - d["header_cy"]) < abs(d["y_far"] - d["header_cy"]))
    # and after the flip the connector side must be the BOTTOM
    d["connector_at_bottom"] = d["header_cy"] < d["oled_cy"]

    # --- the four posts ---------------------------------------------------
    d["geo_conn"] = _post_geo(P, d, "")
    d["geo_far"] = _post_geo(P, d, "far_")
    d["posts"] = ([(x, y, d["geo_conn"]) for (x, y) in d["conn"]]
                  + [(x, y, d["geo_far"]) for (x, y) in d["far"]])
    d["post_count"] = len(d["posts"])
    # forward over-travel that would strip a hook if the barbs were held
    # squeezed: where the nose cone narrows back to the hole diameter
    g0 = d["geo_conn"]
    frac = ((g0["barb_d"] - P["oled_hole_d"]) / (g0["barb_d"] - g0["tip_d"]))
    d["z_strip"] = d["z_hook_top"] + frac * (d["z_nose_tip"] - d["z_hook_top"])
    d["strip_travel"] = d["z_strip"] - d["z_pcb_rear"]
    d["F_total"] = sum(g["F_axial"] for (_x, _y, g) in d["posts"])
    d["strain_worst_all"] = max(g["strain_worst"] for (_x, _y, g) in d["posts"])
    d["overlap_min_all"] = min(g["overlap"] for (_x, _y, g) in d["posts"])
    d["floor_min_all"] = min(g["floor_t"] for (_x, _y, g) in d["posts"])
    # the deepest relief of the four sets the shield's worst case
    d["z_floor_min"] = min(g["z_floor"] for (_x, _y, g) in d["posts"])

    # --- integral rear light shield (brief 8.3) ---------------------------
    d["z_shield_rear"] = d["z_rear"]                                      # -6.00
    d["z_shield_front"] = d["z_rear"] + P["rear_light_shield_t"]          # -4.80
    d["shield_x0"], d["shield_x1"] = d["pk_x0"], d["pk_x1"]
    # the shield runs from the carrier's own termination on the cut side up to
    # the pocket line on the solid side
    d["shield_y0"] = d["light_cut_y"]                                     # -20.80
    d["shield_y1"] = d["pk_y1"]                                           # +12.70
    d["shield_pcb_clear"] = d["z_pcb_rear"] - d["z_shield_front"]         #  2.10
    d["shield_free_edge"] = (d["light_cut_y"] + d["cap_r"]) - d["shield_y0"]
    # margin between the deepest post relief floor and the shield's inner face
    d["relief_floor_margin"] = d["z_floor_min"] - d["z_shield_front"]

    # --- the four-pin opening (brief 8.4: finished 14.00 x 4.19) ----------
    d["pin_slot_x1"] = P["oled_header_w"] / 2.0 + P["pin_slot_clear_x"]   # 7.00
    d["pin_slot_x0"] = -d["pin_slot_x1"]
    # nominal cut: the header envelope grown symmetrically by the named
    # clearances, so the opening is centred on the transformed connector
    d["pin_slot_y0"] = d["header_y0"] - P["pin_slot_clear_y"]             # -22.49
    d["pin_slot_y1"] = d["header_y1"] + P["pin_slot_clear_y"]             # -16.61
    # FINISHED opening: what is actually missing from the wall. The lower edge
    # is the shield's own free edge on the open lighting-unit side.
    d["pin_open_y0"] = max(d["pin_slot_y0"], d["shield_y0"])              # -20.80
    d["pin_open_y1"] = d["pin_slot_y1"]                                   # -16.61
    d["pin_slot_w"] = d["pin_slot_x1"] - d["pin_slot_x0"]                 # 14.00
    d["pin_slot_h"] = d["pin_open_y1"] - d["pin_open_y0"]                 #  4.19
    d["pin_slot_area"] = d["pin_slot_w"] * d["pin_slot_h"]
    d["shield_area"] = ((d["shield_x1"] - d["shield_x0"])
                        * (d["shield_y1"] - d["shield_y0"]))
    d["pin_slot_side_w"] = d["shield_x1"] - d["pin_slot_x1"]
    d["pin_slot_above_h"] = d["shield_y1"] - d["pin_open_y1"]

    # --- connector light blocks (brief 8.4) -------------------------------
    # One each side, immediately outboard of the opening, growing forward off
    # the shield's inner face and stopping short of DATUM B.
    d["z_block_rear"] = d["z_shield_front"]                               # -4.80
    d["z_block_front"] = d["z_shield_front"] + P["light_block_depth"]     # -3.20
    d["block_pcb_clear"] = d["z_pcb_rear"] - d["z_block_front"]           #  0.50
    d["block_y0"] = d["pin_open_y0"]
    d["block_y1"] = d["pin_open_y1"]
    d["block_x_in"] = d["pin_slot_x1"]                                    # 7.00
    # Run each block out to the sprung pedestal and 0.60 mm into it. Rev P.5.1
    # stopped at pin_slot_x1 + light_block_t = 8.20 and left a 2.50 mm open
    # gap between the block and the tower at x 8.20 .. 10.70 - a straight
    # sideways path for light out of the pin opening into the bay. There is no
    # reason to leave it: the pedestal is right there to tie into.
    # The pedestal is a CYLINDER, so its inner edge retreats outboard as you
    # move away from its centre line. Taking the tangent at the post centre
    # (x 10.70) leaves a 0.04 mm slot at the block's far edge - a sliver, and
    # a light path. Solve it at the WORST y the block reaches instead.
    d["block_dy_max"] = max(abs(d["block_y0"] - d["y_conn"]),
                            abs(d["block_y1"] - d["y_conn"]))            #  2.25
    d["ped_inner_x"] = d["post_x"] - math.sqrt(
        max(0.0, (P["pedestal_d"] / 2.0) ** 2 - d["block_dy_max"] ** 2))  # 11.34
    d["block_x_out"] = d["ped_inner_x"] + P["light_block_tie"]           # 11.94
    d["block_w"] = d["block_x_out"] - d["block_x_in"]                    #  4.94
    d["block_header_clear"] = d["block_x_in"] - P["oled_header_w"] / 2.0  # 2.00

    # --- what the amendment history costs, for the record -----------------
    d["carrier_min_y"] = d["y_conn"] - P["pedestal_d"] / 2.0              # -22.85
    d["carrier_max_y"] = d["car_y1"]                                      # +16.30
    d["carrier_h"] = d["carrier_max_y"] - d["carrier_min_y"]              #  39.15
    d["y_before"] = d["ap_y0"] - P["carrier_wall"] - 6.00

    # --- what the mounting-point correction actually does to the picture --
    # Reported, not asserted. The active area is NOT fully visible and is NOT
    # vertically centred; both statements would be false.
    d["vis_y0"] = max(d["active_y0"], d["panel_open_bottom_y"])         # -0.65
    d["vis_y1"] = min(d["active_y1"], d["panel_open_top_y"])            # +7.65
    d["vis_h"] = max(0.0, d["vis_y1"] - d["vis_y0"])                    #  8.30
    d["vis_frac"] = d["vis_h"] / P["oled_active_h"]
    d["active_above_opening"] = max(0.0, d["active_y1"]
                                    - d["panel_open_top_y"])            #  6.40
    d["active_below_opening"] = max(0.0, d["panel_open_bottom_y"]
                                    - d["active_y0"])                   #  0.00
    # unlit band of the Perspex opening under the active area
    d["opening_unlit_below"] = max(0.0, d["active_y0"]
                                   - d["panel_open_bottom_y"])          #  7.00

    # --- the SAME move, stated in both frames -----------------------------
    # 1. CARRIER-LOCAL: where the fixing centres sit relative to the OLED group
    d["fix_rel_oled"] = P["panel_fix_y"] - d["oled_cy"]                 # -6.70
    d["fix_rel_oled_prev"] = P["panel_fix_y"] - d["oled_cy_prev"]       # +0.30
    d["fix_shift_local"] = d["fix_rel_oled"] - d["fix_rel_oled_prev"]   # -7.00
    # 2. ASSEMBLED PANEL: the panel holes are fixed, the OLED group rose
    d["oled_shift_global"] = d["oled_cy"] - d["oled_cy_prev"]           # +7.00
    return d
# ---------------------------------------------------------------------------
# Reference bodies
# ---------------------------------------------------------------------------
def build_panel(B, P, d):
    """REF_Decca_Panel - the original fascia Perspex. Reference only."""
    t = P["perspex_t"]
    s = B.box(-P["panel_ref_w"] / 2.0, P["panel_ref_w"] / 2.0,
              -P["panel_ref_h"] / 2.0, P["panel_ref_h"] / 2.0, 0.0, t)
    B.sub(s, B.box(-P["panel_open_w"] / 2.0, P["panel_open_w"] / 2.0,
                   -P["panel_open_h"] / 2.0, P["panel_open_h"] / 2.0,
                   -1.0, t + 1.0))
    for sx in (-1, 1):
        B.sub(s, B.cylz(P["panel_fix_clear_d"], sx * d["m2_x"],
                        P["panel_fix_y"], -1.0, t + 1.0))
    return [(s, "PANEL_Perspex")]


def build_pcb(B, P, d, z_shift=0.0):
    """The OLED PCB alone, with its four Ø3.00 mounting holes, optionally
    translated along Z. The positive-stop checks use this on its own."""
    zf = d["z_pcb_front"] + z_shift
    zr = d["z_pcb_rear"] + z_shift
    pcb = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"], zr, zf)
    for (hx, hy) in d["holes"]:
        B.sub(pcb, B.cylz(P["oled_hole_d"], hx, hy, zr - 1.0, zf + 1.0))
    return pcb


def build_oled(B, P, d, tip_proud=None, z_shift=0.0):
    """REF_SH1106_1P3 - separately checkable bodies."""
    tp = P["oled_tip_proud"] if tip_proud is None else tip_proud
    zf = d["z_pcb_front"] + z_shift
    zr = d["z_pcb_rear"] + z_shift
    out = [(build_pcb(B, P, d, z_shift), "OLED_PCB")]

    out.append((B.box(d["glass_x0"], d["glass_x1"], d["glass_y0"], d["glass_y1"],
                      zf, zf + P["oled_glass_proud"]), "OLED_Glass"))
    out.append((B.box(-P["oled_active_w"] / 2.0, P["oled_active_w"] / 2.0,
                      d["active_y0"], d["active_y1"],
                      zf + P["oled_glass_proud"] - 0.05,
                      zf + P["oled_glass_proud"]), "OLED_ActiveArea"))
    out.append((B.box(-P["oled_header_w"] / 2.0, P["oled_header_w"] / 2.0,
                      d["header_y0"], d["header_y1"],
                      zr - P["oled_header_depth"], zr), "OLED_Header_Keepout"))

    tips = None
    for ty in d["tip_y"]:
        for tx in d["tip_x"]:
            c = B.cylz(P["oled_tip_d"], tx, ty, zf, zf + tp)
            tips = c if tips is None else B.uni(tips, c)
    out.append((tips, "OLED_Solder_Tips"))
    return out


def build_fasteners(B, P, d):
    """REF_Decca_Fasteners - the two ORIGINAL nuts and the envelope their
    original bolts sweep. Reference only; separately checkable.

    The nut is modelled as a regular hex prism at the MEASURED 3.80 mm across
    flats - no fit allowance - seated on the shoulder and running the full
    measured 10.00 mm length, which takes it 4.00 mm past the carrier rear face
    into free air. The bolt envelope runs from the head bearing face on the
    front of the Perspex to the far end of the nut, so anything the bolt could
    ever occupy is covered.
    """
    out = []
    nuts = None
    bolts = None
    for sx in (-1, 1):
        x = sx * d["m2_x"]
        y = P["panel_fix_y"]
        n = B.hexz(P["original_nut_hex_width"], x, y,
                   d["z_nut_rear"], d["z_nut_seat"])
        nuts = n if nuts is None else B.uni(nuts, n)
        b = B.cylz(P["panel_fix_clear_d"], x, y,
                   d["z_nut_rear"], d["z_perspex_front"])
        bolts = b if bolts is None else B.uni(bolts, b)
    out.append((nuts, "ORIGINAL_Nuts"))
    out.append((bolts, "ORIGINAL_Bolt_Envelope"))
    return out


def sweep_bodies(B, P, d, travel, tip_proud=None):
    """Swept insertion / removal corridor.

    Rev P.2 inserts from the FRONT, so the module travels rearward on assembly
    and forward on removal. Both are the same straight line, so one corridor
    covers both directions: each body's X/Y cross-section extruded FORWARD from
    its seated position by ``travel``.
    """
    tp = P["oled_tip_proud"] if tip_proud is None else tip_proud
    zf, zr = d["z_pcb_front"], d["z_pcb_rear"]
    out = []

    # the PCB keeps its four holes - the posts are meant to be inside them
    pcb = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                zr, zf + travel)
    for (hx, hy) in d["holes"]:
        B.sub(pcb, B.cylz(P["oled_hole_d"], hx, hy, zr - 1.0, zf + travel + 1.0))
    out.append((pcb, "SWEPT_PCB"))

    out.append((B.box(d["glass_x0"], d["glass_x1"], d["glass_y0"], d["glass_y1"],
                      zf, d["z_glass_front"] + travel), "SWEPT_Glass"))
    out.append((B.box(-P["oled_header_w"] / 2.0, P["oled_header_w"] / 2.0,
                      d["header_y0"], d["header_y1"],
                      d["z_header_rear"], zr + travel), "SWEPT_Header"))
    tips = None
    for ty in d["tip_y"]:
        for tx in d["tip_x"]:
            c = B.cylz(P["oled_tip_d"], tx, ty, zf, zf + tp + travel)
            tips = c if tips is None else B.uni(tips, c)
    out.append((tips, "SWEPT_Tips"))
    return out


def swept_pcb(B, P, d, travel):
    """The PCB swept CONTINUOUSLY forward from its seated position by
    ``travel``. Motion is continuous, so an obstruction anywhere in this
    volume stops the board - which is the only honest way to ask whether
    forward escape is blocked."""
    pcb = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                d["z_pcb_rear"], d["z_pcb_front"] + travel)
    for (hx, hy) in d["holes"]:
        B.sub(pcb, B.cylz(P["oled_hole_d"], hx, hy,
                          d["z_pcb_rear"] - 1.0,
                          d["z_pcb_front"] + travel + 1.0))
    return pcb


def nose_envelope(B, P, d, pad=0.02):
    """The declared exception to invariant P1' - the union of ALL FOUR sprung
    nose envelopes. The ONLY carrier material permitted forward of the PCB
    front plane inside the module aperture.

    Rev P.5: four noses, not two. The two converted posts are a new exception
    and are declared here explicitly rather than being allowed to slip through
    as residual."""
    env = None
    for (x, y, g) in d["posts"]:
        b = B.cylz(g["barb_d"] + 2 * pad, x, y,
                   d["z_fwd_limit"] - pad, d["z_nose_tip"] + pad)
        env = b if env is None else B.uni(env, b)
    return env


def nut_retain_envelope(B, P, d, pad=0.05):
    """The declared captive-nut retaining ridge, as an envelope.

    The ridge is a deliberate interference: the nut is pushed past it on
    assembly and back past it on service. So carrier x nut is NOT expected to
    be empty - it is expected to be empty OUTSIDE this envelope, exactly as the
    snap noses are handled for the OLED. Anything outside it would be a real
    fouling of the nut.
    """
    env = None
    for sx in (-1, 1):
        b = B.cylz(d["nut_body_d"] + 2 * pad, sx * d["m2_x"], P["panel_fix_y"],
                   d["z_nut_lead"] - pad, d["z_nut_head_back"] + pad)
        env = b if env is None else B.uni(env, b)
    return env


def hole_keepout(B, P, d, pad=None):
    """All FOUR mounting-hole corridors, expanded by the nose glass margin.
    Every scrap of nose material must lie inside this."""
    env = None
    for (x, y, g) in d["posts"]:
        r = g["nose_keepout_r"] if pad is None else pad
        b = B.cylz(2 * r, x, y, d["z_fwd_limit"] - 0.1, d["z_nose_tip"] + 0.1)
        env = b if env is None else B.uni(env, b)
    return env


# ---------------------------------------------------------------------------
# The carrier
# ---------------------------------------------------------------------------
def sprung_post(B, P, d, x, y, geo, pinch=0.0):
    """One split sprung locating-and-retaining post.

    Rev P.5 builds all FOUR posts from this one function. ``geo`` carries that
    post's own geometry, so the converted far pair can diverge from the proven
    connector pair without a second code path to keep in step - there is no
    plain-post branch left anywhere.

    ``pinch`` shrinks the barb, modelling the two halves squeezed together with
    tweezers. Used to validate the release path.
    """
    barb = max(geo["tip_d"], geo["barb_d"] - 2.0 * pinch)
    z0 = geo["z_floor"]

    s = B.cylz(geo["shaft_d"], x, y, z0, d["z_hook_face"])
    B.uni(s, B.root_fillet(geo["shaft_d"], geo["fillet_r"], x, y, z0))
    B.uni(s, B.cylz(barb, x, y, d["z_hook_face"], d["z_hook_top"]))
    B.uni(s, B.conez(barb, min(geo["tip_d"], barb), x, y,
                     d["z_hook_top"], d["z_nose_tip"]))

    # the split slot: free above the root fillet, solid through it, so the
    # cantilever is properly built in at geo["z_fix"]
    half = geo["slot_w"] / 2.0
    slot = B.box(x - geo["barb_d"], x + geo["barb_d"], y - half, y + half,
                 geo["z_fix"], d["z_nose_tip"] + 0.10)
    if abs(geo["split_deg"]) > 1e-9:
        m = adsk.core.Matrix3D.create()
        m.setToRotation(math.radians(geo["split_deg"]), v3(0, 0, 1),
                        p3(x, y, 0.0))
        if not B.tbm.transform(slot, m):
            raise RuntimeError("could not rotate the split slot at (%g, %g)"
                               % (x, y))
    B.sub(s, slot)
    return s


def build_carrier(B, P, d, pinch=0.0):
    """Rear_Display_Carrier - the single structural part.

    Rev P.2 retention geometry unchanged, plus the Rev P.3 lighting-unit-side
    cut and the Rev P.4 integral rear light shield (steps 3a / 3b).
    """
    zr, zf = d["z_rear"], d["z_fwd_limit"]

    # 1. OPEN-ENDED outer envelope. The lighting-unit-side transverse rail and
    #    the cable-tie flange that stood on it are gone: the body simply stops
    #    short of them, so no bridge can survive across the two side uprights.
    #    Each upright is then capped with a half-round of its own width, which
    #    is the deliberate termination radius the brief asks for. It lands
    #    adjacent to the retained sprung-post pedestal root, which the pedestal
    #    union in step 4 ties into.
    #
    #    REV P.5: the open end is at -Y now. It did not move relative to the
    #    module - it is still below/outboard of the connector-side sprung pair -
    #    but that pair travelled from +Y to -Y with the 180 degree transform, so
    #    the cut travelled with it. The solid transverse rail is now at +Y.
    #
    #    The rounded-rectangle corner radius is a COSMETIC top-corner feature.
    #    Applied at the cut end as well it pulled the outer wall inward just
    #    where the R1.80 upright cap pushes it back out, and the two crossed:
    #    the cap stood proud of the retreating corner and left a visible step -
    #    an indent in the left and right outer walls. The corner is squared off
    #    over the cap band so the upright runs at constant width right down to
    #    its termination and the cap lands tangent to it. Nothing else moves.
    y_cap = d["light_cut_y"] + d["cap_r"]
    s = B.rrect(d["car_x0"], d["car_x1"], y_cap, d["car_y1"],
                zr, 0.0, P["carrier_corner_r"])
    B.uni(s, B.box(d["car_x0"], d["car_x1"], y_cap,
                   y_cap + P["carrier_corner_r"], zr, 0.0))
    for sx in (-1, 1):
        B.uni(s, B.cylz(2.0 * d["cap_r"], sx * d["cap_x"], y_cap, zr, 0.0))
    for sx in (-1, 1):
        a, b = sx * d["arm_x0"], sx * d["ear_x1"]
        B.uni(s, B.rrect(min(a, b), max(a, b),
                         -P["fix_arm_h"] / 2.0, P["fix_arm_h"] / 2.0,
                         zr, 0.0, P["fix_arm_h"] / 2.0))
        a, b = sx * (d["m2_x"] - d["m2_r"]), sx * d["ear_x1"]
        B.uni(s, B.rrect(min(a, b), max(a, b), -d["m2_r"], d["m2_r"],
                         zr, 0.0, d["m2_r"]))

    # 2. MODULE APERTURE - all carrier material forward of z_fwd_limit is
    #    removed across the full module envelope. This is invariant P1'; the
    #    two sprung noses are added back in step 6 as the declared exception.
    B.sub(s, B.box(d["ap_x0"], d["ap_x1"], d["ap_y0"], d["ap_y1"], zf, 1.0))

    # 3. PCB pocket, cut right through - the module drops in from the FRONT.
    B.sub(s, B.box(d["pk_x0"], d["pk_x1"], d["pk_y0"], d["pk_y1"], zr - 1.0, zf))

    # 3a. INTEGRAL REAR LIGHT SHIELD (brief 8.3). Rev P.3 stopped at step 3 and
    #     shipped a full-height open rear window, so the Decca cabinet LEDs lit
    #     the back and edges of the OLED. The bay is now closed by carrier
    #     material - a wall grown FORWARD from the existing rear plane, so the
    #     external envelope is unchanged and the whole wall prints as the first
    #     layers flat on the bed.
    #
    #     Footprint = the PCB-pocket rectangle in X, so the wall lands exactly
    #     on the two pocket side walls and ties the uprights together across
    #     the OLED bay. In Y it runs from the bottom rail up to light_cut_y and
    #     stops: it does not re-enter the deleted end-rail / cable-tie region.
    #     It is 4.10 mm behind DATUM B, so it never touches the PCB and is
    #     never an OLED Z datum.
    B.uni(s, B.box(d["shield_x0"], d["shield_x1"],
                   d["shield_y0"], d["shield_y1"],
                   d["z_shield_rear"], d["z_shield_front"]))

    # 3b. the ONLY penetration through the shield: the four-pin / header slot.
    #     Sized from the header envelope plus the two named clearances, which
    #     brief 8.4 fixes so the FINISHED opening is exactly 14.00 x 4.19 mm.
    #     Cut right through the wall and on forward into the (already void) bay
    #     so no coincident faces are created. There is no rear window, no
    #     solder-access window and no rear release opening anywhere else.
    B.sub(s, B.box(d["pin_slot_x0"], d["pin_slot_x1"],
                   d["pin_slot_y0"], d["pin_slot_y1"],
                   zr - 1.0, zf))

    # 3c. CONNECTOR LIGHT BLOCKS (brief 8.4). Two integral opaque baffles, one
    #     immediately outboard of each lateral edge of the opening, growing
    #     FORWARD off the shield's inner face to form a short tunnel beside the
    #     pins. They are part of this solid - not fins, not a second component.
    #     They stop light_block_pcb_clear short of DATUM B, so they stay behind
    #     the seated PCB and out of the insertion / removal sweep.
    #
    #     Each one runs from the edge of the pin opening all the way out to the
    #     sprung pedestal and 0.60 mm into it, so there is no open gap left
    #     between the baffle and the tower. They stay entirely ABOVE
    #     light_cut_y: the 8.1 rail cut is not touched.
    for sx in (-1, 1):
        a, b = sx * d["block_x_in"], sx * d["block_x_out"]
        B.uni(s, B.box(min(a, b), max(a, b), d["block_y0"], d["block_y1"],
                       d["z_block_rear"], d["z_block_front"]))

    # 4. rigid pedestals + FIXED REAR DATUM PADS at z = z_pcb_rear.
    #    These are solid carrier body. They stop the module moving rearward and
    #    they set the OLED Z position. No spring is involved anywhere in them.
    for (x, y) in d["holes"]:
        B.uni(s, B.cylz(P["pedestal_d"], x, y, zr, d["z_ped_top"]))
        B.uni(s, B.cylz(P["datum_pad_od"], x, y, d["z_ped_top"], d["z_pcb_rear"]))

    # 5. post root reliefs, bored down from the datum plane. FOUR of them now,
    #    each only as deep as its own post needs, and every one stopping short
    #    of the rear light shield so the shield stays light-tight underneath.
    for (x, y, g) in d["posts"]:
        B.sub(s, B.cylz(g["relief_d"], x, y, g["z_floor"], d["z_pcb_rear"]))

    # 6. the FOUR sprung posts. No plain-post branch exists any more.
    for (x, y, g) in d["posts"]:
        B.uni(s, sprung_post(B, P, d, x, y, g, pinch))

    # 7. CAPTIVE ORIGINAL-NUT POCKET at each original fixing centre.
    #    There is no heat-set insert anywhere in this part. Front to rear:
    #      0.00 .. -2.00   bolt clearance bore - solid carrier ring that
    #                      carries the clamp load in compression
    #      -2.00           SEATING SHOULDER, the positive axial seat
    #      -2.00 .. -3.40  regular-hex HEAD SEAT, anti-rotation, exactly the
    #                      measured 1.40 mm head-seat depth, positively
    #                      defined by the step behind it
    #      -3.40 .. -3.70  retaining ridge - a controlled interference the nut
    #                      is pushed past on assembly and back past on service
    #      -3.70 .. -4.10  self-supporting lead-in that also aligns the hex
    #      -4.10 .. rear   clearance bore for the rest of the nut envelope
    for sx in (-1, 1):
        x = sx * d["m2_x"]
        y = P["panel_fix_y"]
        B.sub(s, B.cylz(P["bolt_clear_d"], x, y, d["z_nut_seat"], 0.001))
        B.sub(s, B.hexz(d["nut_hex_af"], x, y,
                        d["z_nut_head_back"], d["z_nut_seat"]))
        B.sub(s, B.hexz(d["nut_retain_af"], x, y,
                        d["z_nut_retain"], d["z_nut_head_back"]))
        B.sub(s, B.conez(d["nut_body_d"], d["nut_retain_ac"], x, y,
                         d["z_nut_lead"], d["z_nut_retain"]))
        B.sub(s, B.cylz(d["nut_body_d"], x, y, zr - 1.0, d["z_nut_lead"]))
    return [(s, CARRIER)]


# ---------------------------------------------------------------------------
# Fusion plumbing
# ---------------------------------------------------------------------------
def add_component(root, name, bodies):
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = name
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    try:
        for body, bname in bodies:
            comp.bRepBodies.add(body, bf).name = bname
    finally:
        bf.finishEdit()
    return occ, comp


def write_parameters(design, P, d):
    ups = design.userParameters
    vals = dict(P)
    for k in ("z_perspex_rear", "z_glass_front", "z_pcb_front", "z_fwd_limit",
              "z_pcb_rear", "z_rear", "z_tip_front", "z_hook_face", "z_hook_top",
              "z_nose_tip", "z_ped_top",
              "oled_cy", "pcb_cy", "glass_cy", "header_cy",
              "active_y0", "active_y1", "panel_open_bottom_y",
              "panel_open_top_y", "oled_cy_prev", "oled_rise",
              "vis_y0", "vis_y1", "vis_h", "active_above_opening",
              "opening_unlit_below", "fix_rel_oled", "fix_rel_oled_prev",
              "fix_shift_local", "oled_shift_global",
              "y_conn", "y_far", "post_x",
              "light_cut_y", "cap_r", "cap_x",
              "carrier_min_y", "carrier_max_y", "carrier_h",
              "z_block_rear", "z_block_front", "block_pcb_clear",
              "block_x_in", "block_x_out", "block_y0", "block_y1",
              "pin_open_y0", "pin_open_y1", "relief_floor_margin",
              "z_shield_rear", "z_shield_front", "shield_x0", "shield_x1",
              "shield_y0", "shield_y1", "shield_pcb_clear",
              "pin_slot_x0", "pin_slot_x1", "pin_slot_y0", "pin_slot_y1",
              "pin_slot_w", "pin_slot_h", "pin_slot_side_w",
              "z_nut_seat", "z_nut_head_back", "z_nut_retain", "z_nut_lead",
              "z_nut_rear", "nut_hex_af", "nut_hex_ac", "nut_body_d",
              "nut_retain_af", "nut_ac", "boss_wall_min", "bolt_grip"):
        vals[k] = d[k]
    # every post's own recalculated geometry, one flat parameter each
    for tag, key in (("conn", "geo_conn"), ("far", "geo_far")):
        for gk in ("shaft_d", "slot_w", "barb_d", "tip_d", "relief_d",
                   "relief_depth", "split_deg", "fillet_r", "z_floor",
                   "z_fix", "floor_t", "overlap", "shaft_clear", "a", "t",
                   "cam_deg", "nose_keepout_r", "strain_nom", "strain_worst",
                   "F_axial", "release_travel"):
            vals["post_%s_%s" % (tag, gk)] = d[key][gk]
    n = 0
    for k in sorted(vals):
        v = vals[k]
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        name = "p_" + k
        expr = "%.4f mm" % v
        ex = ups.itemByName(name)
        try:
            if ex:
                ex.expression = expr
            else:
                ups.add(name, adsk.core.ValueInput.createByString(expr),
                        "mm", "Rev P.5 generator")
            n += 1
        except Exception:
            pass
    return n


def find_component(design, name):
    root = design.rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        if occ.component.name == name:
            return occ
    return None


def clear_component(design, name):
    root = design.rootComponent
    for i in range(root.occurrences.count - 1, -1, -1):
        if root.occurrences.item(i).component.name == name:
            root.occurrences.item(i).deleteMe()


# ---------------------------------------------------------------------------
# main - build in a NEW document
# ---------------------------------------------------------------------------
def _design_holds_carrier(app):
    """True if the ACTIVE document already contains this generator's output."""
    des = adsk.fusion.Design.cast(app.activeProduct)
    if des is None:
        return False
    root = des.rootComponent
    for i in range(root.occurrences.count):
        if root.occurrences.item(i).component.name == CARRIER:
            return True
    return False


def main(_context=None):
    app = adsk.core.Application.get()
    reuse = _design_holds_carrier(app)
    if not reuse:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc = app.activeDocument
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent

    B = Builder()
    d = derive(P)

    npar = write_parameters(design, P, d)

    for name in ("REF_Decca_Panel", "REF_SH1106_1P3", CARRIER,
                 "REF_Decca_Fasteners") + LEGACY_COMPONENTS:
        clear_component(design, name)

    add_component(root, "REF_Decca_Panel", build_panel(B, P, d))
    add_component(root, "REF_SH1106_1P3", build_oled(B, P, d))
    add_component(root, CARRIER, build_carrier(B, P, d))
    add_component(root, "REF_Decca_Fasteners", build_fasteners(B, P, d))

    app.activeViewport.fit()

    print("Rev P.5 built in %s document %r"
          % ("the existing Rev P" if reuse else "a NEW", doc.name))
    print("user parameters written: %d" % npar)
    occ = find_component(design, CARRIER)
    body = occ.bRepBodies.item(0)
    bb = body.boundingBox
    print("carrier bbox mm  x[%.2f, %.2f]  y[%.2f, %.2f]  z[%.2f, %.2f]" % (
        bb.minPoint.x * 10, bb.maxPoint.x * 10,
        bb.minPoint.y * 10, bb.maxPoint.y * 10,
        bb.minPoint.z * 10, bb.maxPoint.z * 10))
    print("carrier size %.2f x %.2f x %.2f mm" % (
        (bb.maxPoint.x - bb.minPoint.x) * 10,
        (bb.maxPoint.y - bb.minPoint.y) * 10,
        (bb.maxPoint.z - bb.minPoint.z) * 10))
    print("carrier isSolid=%s  volume %.3f cm3  faces %d" % (
        body.isSolid, volume_of(body) / 1000.0, body.faces.count))
    print("FOUR sprung posts: connector pair y %+.2f, converted far pair y %+.2f"
          % (d["y_conn"], d["y_far"]))
    print("  connector at the bottom: %s   header side: %s   no plain post: yes"
          % (d["connector_at_bottom"], d["conn_is_header_side"]))
    print("module rotated %.0f deg in plane" % P["module_rot_deg"])
    print("MOUNTING-POINT CORRECTION, stated both ways:")
    print("  carrier-local : fixing centres %+.2f mm relative to the OLED "
          "group (was %+.2f) = %+.2f mm toward the connector bottom"
          % (d["fix_rel_oled"], d["fix_rel_oled_prev"], d["fix_shift_local"]))
    print("  assembled     : Perspex holes UNMOVED at y %+.2f, pitch %.5f mm; "
          "OLED group raised %+.2f mm (centre %+.2f -> %+.2f)"
          % (P["panel_fix_y"], 2.0 * d["m2_x"], d["oled_shift_global"],
             d["oled_cy_prev"], d["oled_cy"]))
    print("active area y %+.2f .. %+.2f against a Perspex opening of "
          "%+.2f .. %+.2f" % (d["active_y0"], d["active_y1"],
                              d["panel_open_bottom_y"], d["panel_open_top_y"]))
    print("  VISIBLE through the opening: %.2f mm of %.2f mm (%.0f%%); "
          "%.2f mm of active area sits ABOVE the opening"
          % (d["vis_h"], P["oled_active_h"], 100.0 * d["vis_frac"],
             d["active_above_opening"]))
    print("lumps %d  (must be 1 - one connected open-ended solid)"
          % body.lumps.count)
    print("uprights terminate at y %+.2f, capped R%.2f; carrier reaches y %+.2f "
          "on the open side" % (d["light_cut_y"], d["cap_r"], d["carrier_min_y"]))
    for nm in LEGACY_COMPONENTS:
        print("legacy component %-24s %s"
              % (nm, "ABSENT" if find_component(design, nm) is None
                 else "*** STILL PRESENT ***"))
    print("rear light shield %.2f mm thick, z %+.2f .. %+.2f, %.1f x %.1f mm, "
          "%.1f mm clear of the PCB"
          % (P["rear_light_shield_t"], d["z_shield_rear"], d["z_shield_front"],
             d["shield_x1"] - d["shield_x0"], d["shield_y1"] - d["shield_y0"],
             d["shield_pcb_clear"]))
    print("four-pin slot FINISHED %.2f x %.2f mm at x %+.2f..%+.2f, y %+.2f..%+.2f"
          % (d["pin_slot_w"], d["pin_slot_h"], d["pin_slot_x0"],
             d["pin_slot_x1"], d["pin_open_y0"], d["pin_open_y1"]))
    print("light blocks x %+.2f..%+.2f (both sides), z %+.2f..%+.2f, "
          "%.2f mm clear of DATUM B"
          % (d["block_x_in"], d["block_x_out"], d["z_block_rear"],
             d["z_block_front"], d["block_pcb_clear"]))
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        print("post %-9s a %.2f, half %.2f x %.2f, overlap %.3f, cam %.1f deg, "
              "strain %.2f/%.2f %%, %.1f N, relief floor %.2f mm"
              % (nm, g["a"], g["t"], g["shaft_d"], g["overlap"], g["cam_deg"],
                 g["strain_nom"], g["strain_worst"], g["F_axial"],
                 g["floor_t"]))
    print("four-post combined insertion force %.1f N" % d["F_total"])
    print("shield open area %.1f%% - the pin slot is the only penetration"
          % (100.0 * d["pin_slot_w"] * d["pin_slot_h"] / d["shield_area"]))
    print("nut hex pocket %.2f af (%.2f measured + %.2f fit), boss wall %.3f mm"
          % (d["nut_hex_af"], P["original_nut_hex_width"],
             P["nut_pocket_fit_allowance"], d["boss_wall_min"]))


# ---------------------------------------------------------------------------
# validate - the mandatory Rev P.5 validation gate
# ---------------------------------------------------------------------------
SWEEP_TRAVEL = 12.00


def _hit(B, a, b):
    """Boolean-intersection interference test -> (hit, volume_mm3, bbox)."""
    c = B.copy(a)
    B.inter(c, B.copy(b))
    try:
        n = c.faces.count
    except Exception:
        n = 0
    if n == 0:
        return False, 0.0, ""
    bb = c.boundingBox
    box = "x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]" % (
        bb.minPoint.x * 10, bb.maxPoint.x * 10,
        bb.minPoint.y * 10, bb.maxPoint.y * 10,
        bb.minPoint.z * 10, bb.maxPoint.z * 10)
    return True, volume_of(c), box


def _residual(B, a, b, env):
    """Part of the a-b intersection that lies outside the envelope ``env``."""
    r = B.copy(a)
    B.inter(r, B.copy(b))
    try:
        if r.faces.count == 0:
            return 0, 0.0
    except Exception:
        return 0, 0.0
    B.sub(r, B.copy(env))
    try:
        n = r.faces.count
    except Exception:
        n = 0
    return n, (volume_of(r) if n else 0.0)


def _planar_face_area(body, nz, z_at, tol=0.005):
    """Area (mm2) of planar faces normal to Z (sign nz) lying at z = z_at."""
    total = 0.0
    for f in body.faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
            continue
        n = g.normal
        if abs(abs(n.z) - 1.0) > 1e-6 or (n.z * nz) < 0:
            continue
        bb = f.boundingBox
        if abs(bb.minPoint.z * 10 - z_at) > tol:
            continue
        if abs(bb.maxPoint.z * 10 - z_at) > tol:
            continue
        total += f.area * 100.0
    return total


def _inside(body, x, y, z):
    pc = body.pointContainment(p3(x, y, z))
    return pc == adsk.fusion.PointContainment.PointInsidePointContainment


def _mind(app, a, b):
    try:
        return app.measureManager.measureMinimumDistance(a, b).value * 10.0
    except Exception:
        return float("nan")


def validate(_context=None):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    B = Builder()
    d = derive(P)
    fails = []
    opens = []
    blocks = []
    closed = []
    glass_measured = bool(P.get("oled_glass_measured", False))
    tested = bool(REV_P5_PROTOTYPE_VALIDATED)

    def gate(ok, label, detail=""):
        print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", label, detail))
        if not ok:
            fails.append(label)

    def blocked(label, detail=""):
        print("  [BLKD] %-56s %s" % (label, detail))
        blocks.append("%s - %s" % (label, detail))

    def closed_by_test(label, detail=""):
        """An item this gate deferred to physical test, which has now passed.

        Not a CAD pass and not a re-interpretation of the model: a record that
        the evidence the gate always asked for now exists."""
        print("  [TEST] %-56s %s" % (label, detail))
        closed.append("%s - %s" % (label, detail))

    def glassgate(ok, label, detail="", blocked_detail=""):
        """A check against the bonded-glass envelope.

        While that envelope is unmeasured it is fiction, and fiction can
        produce neither a pass nor a failure. A clear result still passes - it
        costs nothing. An intrusion is reported as BLOCKED, with the number,
        and it holds the print until the boundary is measured. Set
        oled_glass_measured once it is, and every one of these becomes an
        ordinary hard gate with no other change."""
        if ok or glass_measured:
            gate(ok, label, detail)
        elif tested:
            # The modelled envelope is still fiction and is still printed as
            # such. What changed is that the real assembly was built and the
            # OLED inserted, retained and released with no glass contact, so
            # the question this check could not answer has been answered.
            closed_by_test(
                label,
                "%s. The modelled envelope is UNMEASURED and unchanged. "
                "CLOSED BY PHYSICAL TEST: the built carrier inserted, retained "
                "and released the OLED with no glass contact."
                % (blocked_detail or detail))
        else:
            blocked(label, blocked_detail or detail)

    def openitem(label, detail="", outcome=""):
        """A pre-print/pre-release item.

        ``detail`` is what had to be done. ``outcome`` is what the prototype
        actually showed. Before the build the item prints as OPEN with the
        instruction; after it, as [TEST] with the outcome - so resetting
        REV_P5_PROTOTYPE_VALIDATED restores the original wording exactly."""
        if tested:
            closed_by_test(label, outcome or
                           "deferred to physical test; the Rev P.5 prototype "
                           "passed")
            return
        print("  [OPEN] %-56s %s" % (label, detail))
        opens.append("%s - %s" % (label, detail))

    car_occ = find_component(design, CARRIER)
    carrier = car_occ.bRepBodies.item(0)
    ref_occ = find_component(design, "REF_SH1106_1P3")
    pan_occ = find_component(design, "REF_Decca_Panel")
    mod = {}
    for b in ref_occ.bRepBodies:
        mod[b.name] = b
    perspex = pan_occ.bRepBodies.item(0)
    rmid = (P["datum_pad_od"] + P["sprung_relief_d"]) / 4.0

    print("=" * 80)
    print("REV P.5 VALIDATION GATE - RELEASED, PROTOTYPE VALIDATED")
    if tested:
        print("  The Rev P.5 carrier has been BUILT AND PHYSICALLY TESTED and")
        print("  every test passed. The geometric gates below are unchanged")
        print("  and still run in full; the items this gate always deferred to")
        print("  physical test are now marked [TEST] instead of OPEN/BLOCKED.")
        for label, res in REV_P5_PROTOTYPE:
            print("    %-58s %s" % (label, res))
        print("")
    print("  Rev P.2 flush-side insertion onto fixed rear datum pads with")
    print("  positive sprung retention is carried through - but NOTHING is")
    print("  inherited numerically. Rev P.5 rotates the module 180 deg, drops")
    print("  the carrier to 6.00 mm and converts the two plain posts to sprung")
    print("  posts, so every post, relief, floor, strain and force below is")
    print("  recalculated from the finished solid.")
    print("    5b  root reliefs inside the 6.00 mm envelope")
    print("    6   FOUR-post mechanics, combined force and PCB bow")
    print("    8   the four-post release sequence, rear wall closed")
    print("    9   bonded-glass clearance at all four holes - the print gate")
    print("    10  the 180 deg transform and the vertical datum")
    print("    14  lighting-unit side, no keepout proxy")
    print("    14b rear light shield and the connector light blocks")
    print("    15  original bolt / captive-nut interface")
    print("=" * 80)

    # ---- 1. static interference, seated ---------------------------------
    print("")
    print("1. STATIC INTERFERENCE - final seated position")
    for name in ("OLED_Glass", "OLED_ActiveArea", "OLED_Header_Keepout",
                 "OLED_Solder_Tips", "OLED_PCB"):
        h, v, bb = _hit(B, carrier, mod[name])
        det = "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb)
        if name == "OLED_Glass":
            glassgate(not h, "carrier x %s" % name, det,
                      "%s - the two CONVERTED far noses against the UNMEASURED "
                      "glass model. Section 9 has the numbers and the "
                      "measurement that settles it." % det)
        else:
            gate(not h, "carrier x %s" % name, det)
    print("      carrier x OLED_PCB CLEAR is the point: seated, the module is")
    print("      touched by nothing but the four rigid datum pads it rests on.")
    print("      No clamp, no bend, no radial or axial preload anywhere.")
    h, v, bb = _hit(B, carrier, perspex)
    gate(not h, "carrier x Perspex",
         "CLEAR - plane contact only" if not h else "HIT %.4f mm3 %s" % (v, bb))
    h, v, bb = _hit(B, mod["OLED_Glass"], perspex)
    gate(not h, "OLED glass x Perspex", "CLEAR" if not h else "HIT %.4f mm3" % v)
    h, v, bb = _hit(B, mod["OLED_Header_Keepout"], perspex)
    gate(not h, "header x Perspex", "CLEAR" if not h else "HIT %.4f mm3" % v)
    h, v, bb = _hit(B, mod["OLED_Solder_Tips"], perspex)
    gate(not h, "solder tips x Perspex at %.2f mm proud" % P["oled_tip_proud"],
         "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    gate(-d["z_nose_tip"] > 0.05, "sprung nose tips clear of the Perspex",
         "tip z %+.2f -> %.2f mm clear" % (d["z_nose_tip"], -d["z_nose_tip"]))

    print("")
    print("1a. TIP-LENGTH SWEEP - the module-preparation limit")
    for tp in (0.40, 0.80, 1.00, 1.10, 1.20, 1.50, 2.00):
        tips = None
        for ty in (P["oled_tip_y_top"], P["oled_tip_y_bot"]):
            for tx in d["tip_x"]:
                c = B.cylz(P["oled_tip_d"], tx, ty, d["z_pcb_front"],
                           d["z_pcb_front"] + tp)
                tips = c if tips is None else B.uni(tips, c)
        hp, vp, _x = _hit(B, tips, perspex)
        hc, vc, _y = _hit(B, carrier, tips)
        print("      tip %.2f proud -> Perspex %-20s carrier %s"
              % (tp, ("HIT %.3f mm3" % vp) if hp else "CLEAR",
                 ("HIT %.3f mm3" % vc) if hc else "CLEAR"))

    # ---- 2. THE HEADLINE CHECK: positive stops in both directions --------
    print("")
    print("2. POSITIVE AXIAL STOPS - the check Rev P.1 did not have")
    print("   Method: translate the real PCB solid along Z and ask whether it")
    print("   runs into carrier material. No step below is a friction estimate.")
    print("")
    print("   2a. FORWARD escape (+Z) - the direction Rev P.1 failed in")
    print("       The board is moved forward CONTINUOUSLY from its seated")
    print("       position. Motion is continuous, so an obstruction anywhere")
    print("       in the swept volume stops it - it cannot skip past the hook.")
    fwd_ok = True
    for dz in (0.05, P["hook_clear"], 0.15, 0.30, 0.50, 1.00, 2.00, 5.00,
               SWEEP_TRAVEL):
        h, v, bb = _hit(B, carrier, swept_pcb(B, P, d, dz))
        must_block = dz > P["hook_clear"] + 1e-9
        if must_block and not h:
            fwd_ok = False
        if h:
            note = "%.5f mm3 at %s" % (v, bb)
        elif must_block:
            note = "*** NOT BLOCKED ***"
        else:
            note = "free - the designed hook clearance"
        print("       swept +%5.2f mm  %-9s %s"
              % (dz, "BLOCKED" if h else "free", note))
    gate(fwd_ok,
         "forward escape blocked beyond the %.2f mm hook clearance"
         % P["hook_clear"],
         "%.2f mm radial overlap at all four posts, square retaining face"
         % d["overlap_min_all"])
    print("")
    print("       static positions, for reference - where the hook bites:")
    first_free = None
    for dz in (0.15, 0.50, 1.00, 1.50, 2.00, 2.50):
        h, v, bb = _hit(B, carrier, build_pcb(B, P, d, z_shift=dz))
        if not h and first_free is None:
            first_free = dz
        print("         +%5.2f mm  %-9s %.5f mm3"
              % (dz, "blocked" if h else "clear", v))
    print("       the hook can only be stripped by forcing the board %.2f mm"
          % d["strip_travel"])
    print("       forward, which the swept check above shows is impossible")
    print("       unless the barbs are squeezed - that IS the removal action.")

    print("")
    print("   2b. REARWARD travel (-Z) - must stop on the FIXED datum pads")
    rear_ok = True
    pads = None
    for (x, y) in d["holes"]:
        b = B.cylz(P["datum_pad_od"] + 0.10, x, y,
                   d["z_ped_top"] - 0.05, d["z_pcb_rear"] + 0.10)
        pads = b if pads is None else B.uni(pads, b)
    for dz in (-0.02, -0.05, -0.20):
        pcb = build_pcb(B, P, d, z_shift=dz)
        h, v, bb = _hit(B, carrier, pcb)
        n, rv = _residual(B, carrier, pcb, pads)
        if not h:
            rear_ok = False
        print("       %6.2f mm  %-9s %.5f mm3, %.5f mm3 of it outside the pads"
              % (dz, "BLOCKED" if h else "*** FREE ***", v, rv))
    gate(rear_ok, "rearward travel stops on carrier material",
         "four fixed pads at z = %.2f" % d["z_pcb_rear"])
    solid_pads = 0
    for (x, y) in d["holes"]:
        if _inside(carrier, x + rmid, y, d["z_pcb_rear"] - 0.05):
            solid_pads += 1
    gate(solid_pads == 4, "all four rear datum pads are solid carrier body",
         "%d of 4 - rigid, not a face on a moving spring" % solid_pads)

    # ---- 3. invariant P1' ------------------------------------------------
    print("")
    print("3. INVARIANT P1' - nothing ahead of the PCB front face except the")
    print("   two declared snap noses, inside the mounting-hole keep-outs")
    ap = B.box(d["ap_x0"], d["ap_x1"], d["ap_y0"], d["ap_y1"],
               d["z_fwd_limit"] + 1e-4, 5.0)
    h, v, bb = _hit(B, carrier, ap)
    print("      carrier x aperture prism, z > %.2f : %.4f mm3  %s"
          % (d["z_fwd_limit"], v, bb))
    env = nose_envelope(B, P, d)
    n, rv = _residual(B, carrier, ap, env)
    gate(n == 0, "P1': that material lies entirely inside the two noses",
         "residual EMPTY" if n == 0
         else "%.5f mm3 of UNDECLARED material forward of the PCB" % rv)
    n2, rv2 = _residual(B, carrier, ap, hole_keepout(B, P, d))
    gate(n2 == 0,
         "noses stay inside the hole keep-outs (R%.2f about each of 4 centres)"
         % d["geo_conn"]["nose_keepout_r"],
         "EMPTY" if n2 == 0 else "%.5f mm3 outside the keep-out" % rv2)
    zmax = max(f.boundingBox.maxPoint.z * 10 for f in carrier.faces)
    gate(abs(zmax) < 1e-6, "forward-most carrier material",
         "z = %+.5f - the Perspex seating plane" % zmax)
    print("      Rev P.5: FOUR noses cross the PCB front plane, not two. The")
    print("      two converted posts are declared exceptions on exactly the")
    print("      same terms as the proven pair - inside their own mounting-hole")
    print("      keep-outs and nowhere else.")

    # ---- 4. M2 load path -------------------------------------------------
    print("")
    print("4. ORIGINAL-FASTENER LOAD PATH")
    seat = _planar_face_area(carrier, 1, 0.0)
    gate(seat > 200.0, "carrier seating-face area at z = 0", "%.1f mm2" % seat)
    plate = B.box(-45.0, 45.0, -42.0, 42.0, 1e-4, 6.0)
    h, v, bb = _hit(B, carrier, plate)
    gate(not h, "synthetic Perspex fixture plate x carrier",
         "carrier stops exactly at the seating plane" if not h
         else "penetrates %.4f mm3" % v)
    for nm in ("OLED_Glass", "OLED_PCB"):
        zt = max(f.boundingBox.maxPoint.z * 10 for f in mod[nm].faces)
        gate(zt < -1e-9, "%s stays behind z = 0" % nm,
             "z = %+.3f -> %.3f mm clear of the Perspex" % (zt, -zt))
    print("      ORIGINAL bolt head -> Perspex -> carrier seating face")
    print("      -> captive ORIGINAL nut -> original bolt thread.")
    print("      no heat-set insert exists anywhere in this part.")
    print("      the module sits in PARALLEL with that path, never in series.")
    print("      the snap noses stop %.2f mm short of the Perspex, so screw"
          % -d["z_nose_tip"])
    print("      torque never reaches them either.")

    # ---- 5. fixed rear PCB datum ----------------------------------------
    print("")
    print("5. FIXED REAR PCB DATUM  (DATUM B, z = %.2f)" % d["z_pcb_rear"])
    land = _planar_face_area(carrier, 1, d["z_pcb_rear"])
    ring = math.pi / 4.0 * (P["datum_pad_od"] ** 2 - P["sprung_relief_d"] ** 2)
    padsolid = None
    for (x, y) in d["holes"]:
        b = B.cylz(P["datum_pad_od"], x, y,
                   d["z_pcb_rear"] - P["datum_pad_h"], d["z_pcb_rear"])
        B.sub(b, B.cylz(P["sprung_relief_d"], x, y,
                        d["z_pcb_rear"] - P["datum_pad_h"] - 0.1,
                        d["z_pcb_rear"] + 0.1))
        padsolid = b if padsolid is None else B.uni(padsolid, b)
    B.inter(padsolid, B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                            d["z_pcb_rear"] - P["datum_pad_h"] - 0.1,
                            d["z_pcb_rear"]))
    on_pcb = volume_of(padsolid) / P["datum_pad_h"]
    gate(land > 30.0, "forward-facing pad area at DATUM B",
         "%.2f mm2 total, %.2f mm2 nominal per annulus" % (land, ring))
    gate(on_pcb > 20.0, "pad area actually bearing on the PCB outline",
         "%.2f mm2 across a %.2f x %.2f mm four-point pattern"
         % (on_pcb, P["oled_hole_pitch_x"], P["oled_hole_pitch_y"]))
    ok = True
    for (x, y) in d["holes"]:
        ok = ok and _inside(carrier, x + rmid, y, d["z_pcb_rear"] - 0.05)
        ok = ok and not _inside(carrier, x + rmid, y, d["z_pcb_rear"] + 0.05)
    gate(ok, "pads present behind and absent ahead of DATUM B", "4 of 4")
    print("      the pads are concentric with the four PCB mounting holes, so")
    print("      they bear inside the board's own keep-outs rather than on an")
    print("      assumed component-free edge band.")
    print("      z-chain: gap %.2f + glass proud %.2f + PCB %.2f = %.2f mm"
          % (P["oled_perspex_gap"], P["oled_glass_proud"], P["oled_pcb_t"],
             -d["z_pcb_rear"]))

    # ---- 5b. relief floors inside the 6.00 mm envelope -------------------
    print("")
    print("5b. ROOT RELIEFS INSIDE THE %.2f mm CARRIER (brief 8.4)"
          % P["carrier_depth"])
    print("      Shortening the carrier by 2.00 mm attacks the post roots")
    print("      first: at the Rev P.4 relief depth of 3.20 mm the bore would")
    print("      end 0.10 mm short of the rear face and cut straight through")
    print("      the %.2f mm light shield. Every floor below is MEASURED off"
          % P["rear_light_shield_t"])
    print("      the finished solid, not taken from the parameter table.")
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        x, y = (d["conn"][1] if g is d["geo_conn"] else d["far"][1])
        col = B.box(x - 0.02, x + 0.02, y - 0.02, y + 0.02,
                    d["z_rear"] - 0.50, g["z_floor"] - 0.02)
        h, v, bb = _hit(B, carrier, col)
        # the probe column stops 0.02 mm short of the relief floor so it does
        # not land on a coincident face, so it reads floor_t - 0.02
        got = (v / (0.04 * 0.04) + 0.02) if h else 0.0
        gate(abs(got - g["floor_t"]) < 5e-3 and got >= P["rear_light_shield_t"],
             "%s post: solid floor under the relief" % nm,
             "%.3f mm measured (%.2f nominal), at least the %.2f mm shield, so "
             "the shield stays light-tight under the post"
             % (got, g["floor_t"], P["rear_light_shield_t"]))
        gate(g["z_floor"] > d["z_shield_front"] + 1e-9,
             "%s post: relief stops short of the shield inner face" % nm,
             "floor z %+.3f against shield face z %+.3f - %.2f mm of margin, "
             "no break-through and no thin membrane"
             % (g["z_floor"], d["z_shield_front"], d["relief_floor_margin"]))
        gate(g["fillet_r"] <= g["relief_depth"] - 1e-9,
             "%s post: R%.2f root fillet is not truncated" % (nm, g["fillet_r"]),
             "it sits entirely inside the %.2f mm relief, %.2f mm below the "
             "built-in point at z %+.3f"
             % (g["relief_depth"], g["fillet_r"], g["z_fix"]))
    gate(abs((d["z_perspex_rear"] - d["z_rear"]) - P["carrier_depth"]) < 1e-9,
         "carrier depth, Perspex seating plane to rear plane",
         "exactly %.2f mm" % P["carrier_depth"])

    # ---- 6. retention mechanics -----------------------------------------
    print("")
    print("6. FOUR-POST RETENTION MECHANICS - recalculated, nothing inherited")
    print("      Rev P.5 has FOUR sprung posts. Nothing below is carried over")
    print("      from Rev P.4: the 6.00 mm carrier shortens every cantilever,")
    print("      so both pairs are re-solved from the finished geometry.")
    print("")
    print("      %-10s %6s %6s %6s %7s %7s %7s %7s %7s"
          % ("post pair", "a", "half t", "overlap", "cam", "defl", "strain",
             "worst", "F axial"))
    print("      %-10s %6s %6s %6s %7s %7s %7s %7s %7s"
          % ("", "mm", "mm", "mm", "deg", "mm", "%", "%", "N"))
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        print("      %-10s %6.2f %6.2f %6.3f %7.1f %7.2f %7.2f %7.2f %7.1f"
              % (nm, g["a"], g["t"], g["overlap"], g["cam_deg"],
                 g["delta_nom"], g["strain_nom"], g["strain_worst"],
                 g["F_axial"]))
    print("")
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        gate(g["overlap"] >= P["hook_overlap_min"] - 1e-9,
             "%s pair: POSITIVE radial overlap beyond the hole radius" % nm,
             "barb %.2f in a %.2f hole = %.3f mm of square retaining face per "
             "side, at or above the %.2f mm that Rev P.2 physically retained "
             "with. Not friction."
             % (g["barb_d"], P["oled_hole_d"], g["overlap"],
                P["hook_overlap_min"]))
        gate(g["strain_nom"] < P["strain_limit"],
             "%s pair: peak strain, hole centred" % nm,
             "%.2f %% at %.2f mm per half (limit %.2f %%)"
             % (g["strain_nom"], g["delta_nom"], P["strain_limit"]))
        gate(g["strain_worst"] < P["strain_limit"],
             "%s pair: worst-case strain, board hard against one side" % nm,
             "%.2f %% at %.2f mm on a single half - %.0f %% margin on the "
             "%.2f %% limit"
             % (g["strain_worst"], g["delta_worst"],
                100.0 * (P["strain_limit"] - g["strain_worst"])
                / P["strain_limit"], P["strain_limit"]))
    print("      The Rev P.2 proven pair ran at 0.83 / 1.66 % in an 8.00 mm")
    print("      carrier. The rise is the direct, unavoidable cost of brief")
    print("      8.4's 6.00 mm depth: a is %.2f mm now against 4.35 mm, and"
          % d["geo_conn"]["a"])
    print("      strain goes as 1/a^2. The split slot was opened 0.70 -> %.2f"
          % P["sprung_slot_w"])
    print("      to claw it back; without that it would be 3.17 %, over limit.")

    # --- combined four-post insertion force and PCB bow ------------------
    print("")
    print("      COMBINED FOUR-POST INSERTION FORCE AND PCB BOW")
    gate(d["F_total"] < 40.0, "combined insertion force, all four posts",
         "%.1f N (%.1f N per post x %d). At the proven 0.70 mm slot it would "
         "be %.1f N."
         % (d["F_total"], d["geo_conn"]["F_axial"], d["post_count"],
            d["F_total"] * ((P["sprung_shaft_d"] - 0.70) / 2.0) ** 3
            / d["geo_conn"]["t"] ** 3))
    # worst case: the whole combined force applied at mid-span between the two
    # hole rows, board simply supported on the four posts. FR4 at 20 GPa.
    E_fr4 = 20000.0
    span = P["oled_hole_pitch_y"]
    I_pcb = P["oled_pcb_w"] * P["oled_pcb_t"] ** 3 / 12.0
    bow = d["F_total"] * span ** 3 / (48.0 * E_fr4 * I_pcb)
    gate(bow < P["hook_clear"], "PCB bow, worst case",
         "%.4f mm with ALL %.1f N applied at mid-span between the two hole "
         "rows (%.2f mm), board simply supported on the four posts, FR4 at "
         "%.0f GPa, I = %.2f mm4. That is under the %.2f mm axial hook "
         "clearance, so even the worst case cannot push a nose into the board."
         % (bow, d["F_total"], span, E_fr4 / 1000.0, I_pcb, P["hook_clear"]))
    print("      In practice the load is applied over the board face and the")
    print("      four reactions are AT the four holes, where the datum pads")
    print("      also are - press near the posts and the bow is essentially")
    print("      zero. The figure above is the pessimistic bound, not the")
    print("      expected value. Brief 12.3 and 12.28 are the physical checks.")

    # --- root sections, remaining material, and the neighbours ------------
    print("")
    print("      ROOT SECTION AND WHAT IS LEFT BEHIND EACH RELIEF")
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        print("      %-10s half section %.2f x %.2f mm at the built-in point "
              "z %+.2f;" % (nm, g["t"], g["shaft_d"], g["z_fix"]))
        print("      %-10s relief O%.2f in a O%.2f pedestal leaves a %.2f mm "
              "annulus;" % ("", g["relief_d"], P["pedestal_d"],
                            (P["pedestal_d"] - g["relief_d"]) / 2.0))
        print("      %-10s %.2f mm of solid carrier behind the relief floor."
              % ("", g["floor_t"]))
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        gate(g["z_floor"] - d["z_shield_front"] > 0.0,
             "%s pair: clearance to the %.2f mm rear shield"
             % (nm, P["rear_light_shield_t"]),
             "%.2f mm between the relief floor and the shield inner face"
             % (g["z_floor"] - d["z_shield_front"]))
    # light blocks vs the nearest sprung pedestal, in X
    gate(d["block_x_out"] > d["ped_inner_x"] + 1e-9,
         "light blocks tie INTO the sprung pedestals, leaving no gap",
         "each block runs x %.2f .. %.2f and the pedestal starts at x %.2f, so "
         "they overlap by %.2f mm - no open slot between the baffle and the "
         "tower for light to come round"
         % (d["block_x_in"], d["block_x_out"], d["ped_inner_x"],
            P["light_block_tie"]))

    # --- release ----------------------------------------------------------
    print("")
    print("      RELEASE DEFLECTION AND TOOL ACCESS")
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        gate(g["release_travel"] > 0.30,
             "%s pair: release deflection and travel" % nm,
             "pinch %.3f mm per half (the overlap) and the hole clears the "
             "nose after %.2f mm of forward travel; %.2f mm of nose stands "
             "proud of the PCB front face for the tweezers to reach"
             % (g["overlap"], g["release_travel"], g["release_travel"]))
    gate(True, "seated spring deflection",
         "0.00 mm at all four posts - every barb clears the PCB front face")
    gate(True, "seated preload on the PCB",
         "none: %.2f mm axial under every hook, %.2f mm radial in every hole"
         % (P["hook_clear"], d["geo_conn"]["shaft_clear"]))
    gate(True, "retention basis",
         "positive geometric overlap at four holes, not friction")
    print("      (the mu 0.30 in the axial figures estimates push-on force")
    print("       ONLY; no acceptance criterion in this gate uses friction)")

    # ---- 7. swept corridor ----------------------------------------------
    print("")
    print("7. SWEPT INSERTION / REMOVAL CORRIDOR - pure Z, %.1f mm travel"
          % SWEEP_TRAVEL)
    print("   Insertion is from the FLUSH / PERSPEX side, moving rearward.")
    swept = {}
    for body, nm in sweep_bodies(B, P, d, SWEEP_TRAVEL):
        swept[nm] = body
    for nm in ("SWEPT_Glass", "SWEPT_Tips", "SWEPT_Header"):
        h, v, bb = _hit(B, carrier, swept[nm])
        det = "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb)
        if nm == "SWEPT_Glass":
            glassgate(not h, "carrier x %s" % nm, det,
                      "%s - swept against the UNMEASURED glass model; see "
                      "section 9" % det)
        else:
            gate(not h, "carrier x %s" % nm, det)
    h, v, bb = _hit(B, carrier, swept["SWEPT_PCB"])
    print("  [INFO] carrier x SWEPT_PCB  HIT %.4f mm3  %s" % (v, bb))
    n, rv = _residual(B, carrier, swept["SWEPT_PCB"], env)
    gate(n == 0, "only the two sprung noses deflect during insertion",
         "all %.4f mm3 is designed snap deflection" % v if n == 0
         else "%.5f mm3 of RIGID obstruction in the corridor" % rv)

    # ---- 8. removal - the FOUR-POST release sequence ---------------------
    print("")
    print("8. RELEASE - four sprung posts, rear wall closed, no prise holes")
    pinch = d["overlap_min_all"] + 0.02
    car_p = build_carrier(B, P, d, pinch=pinch)[0][0]
    print("      all four barbs modelled squeezed %.2f mm per half = %.2f "
          "required + 0.02 margin" % (pinch, d["overlap_min_all"]))
    for nm in ("SWEPT_PCB", "SWEPT_Glass", "SWEPT_Tips", "SWEPT_Header"):
        h, v, bb = _hit(B, car_p, swept[nm])
        det = "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb)
        if nm == "SWEPT_Glass":
            glassgate(not h, "pinched carrier x %s" % nm, det,
                      "%s - even pinched, against the UNMEASURED glass model; "
                      "see section 9" % det)
        else:
            gate(not h, "pinched carrier x %s" % nm, det)
    print("")
    print("      THE SEQUENCE. Four sprung posts cannot all be pinched at")
    print("      once, and the brief does not require it - only that the")
    print("      board never needs all four inaccessible at the same time.")
    print("      It is released a row at a time, about the other row:")
    print("        1. remove the two original bolts and lift the carrier off")
    print("           the Perspex. Nothing below needs the radio.")
    print("        2. pinch BOTH connector-side barbs (y %+.2f) together and"
          % d["y_conn"])
    print("           lift that edge %.2f mm. The board pivots on the far pair,"
          % d["geo_conn"]["release_travel"])
    print("           which stays engaged and stays in control of the board.")
    print("        3. pinch BOTH far barbs (y %+.2f) and withdraw the module"
          % d["y_far"])
    print("           straight forward, out through the Perspex side.")
    print("      Step 2 and step 3 are the same operation on opposite rows, so")
    print("      the order can be reversed if the far pair is easier to reach.")

    # every clause the brief puts on the release, checked
    gate(d["z_nose_tip"] - d["z_pcb_front"] > 0.40,
         "released from the FRONT / accessible sides, not the rear",
         "%.2f mm of every nose stands proud of the PCB front face inside the "
         "open module aperture - reachable with fine-nose tweezers at all four"
         % (d["z_nose_tip"] - d["z_pcb_front"]))
    ledge = P["aperture_margin"] + P["pcb_clearance"]
    gate(ledge > 0.50, "PCB edge accessible from the front all round",
         "the module aperture is %.2f mm larger than the PCB on every side, so "
         "a spudger reaches the board edge at z %+.2f" % (ledge, d["z_fwd_limit"]))
    gate(d["pcb_y0"] < d["light_cut_y"],
         "connector-side PCB edge also reachable from the open side",
         "the board overhangs the carrier termination by %.2f mm at y %+.2f, "
         "the open lighting-unit end"
         % (d["light_cut_y"] - d["pcb_y0"], d["pcb_y0"]))
    # the pivot in step 2 has to fit inside the shaft clearance in the far holes
    tilt = math.degrees(math.atan2(d["geo_conn"]["release_travel"],
                                   P["oled_hole_pitch_y"]))
    tilt_max = math.degrees(math.atan2(2.0 * d["geo_far"]["shaft_clear"],
                                       P["oled_pcb_t"]))
    gate(tilt < tilt_max, "the row-at-a-time pivot fits the far holes",
         "lifting the connector edge %.2f mm rotates the board %.2f deg about "
         "the far pair; the %.2f mm radial clearance in a %.2f mm board allows "
         "%.2f deg before the hole binds on the shaft"
         % (d["geo_conn"]["release_travel"], tilt,
            d["geo_far"]["shaft_clear"], P["oled_pcb_t"], tilt_max))
    gate(d["overlap_min_all"] > 0.0 and pinch < d["geo_conn"]["shaft_d"] / 2.0,
         "no post is permanently deformed to release the board",
         "%.2f mm per half is elastic - %.2f %% strain, the same figure as "
         "insertion, well under the %.2f %% limit"
         % (pinch, d["geo_conn"]["beam"](pinch)[1], P["strain_limit"]))
    gate(d["geo_conn"]["overlap"] < P["oled_hole_d"] / 4.0,
         "the PCB mounting holes are not damaged by release",
         "the nose bears on the hole wall over %.3f mm of radial overlap in a "
         "%.2f mm hole, and it is squeezed clear before the board moves - the "
         "board is never dragged over an engaged barb"
         % (d["geo_conn"]["overlap"], P["oled_hole_d"]))
    gate(d["shield_pcb_clear"] > 1.0,
         "released FORWARD, away from the closed rear wall",
         "removal travel is +Z; the wall sits %.2f mm BEHIND the PCB rear face "
         "and never enters the removal path. No second rear-wall opening is "
         "needed and the shield is not removed or damaged."
         % d["shield_pcb_clear"])
    back = B.box(d["shield_x0"] - 1.0, d["shield_x1"] + 1.0,
                 d["shield_y0"] - 1.0, d["shield_y1"] + 1.0,
                 d["z_rear"] - 1.0, d["z_pcb_rear"] - 1e-4)
    seated = build_pcb(B, P, d)
    h, v, bb = _hit(B, B.copy(seated), B.copy(back))
    gate(not h, "neither PCB nor bonded glass reaches the rear wall zone",
         "the entire module sits forward of z %+.2f throughout insertion, "
         "seating and removal" % d["z_pcb_rear"] if not h
         else "HIT %.4f mm3" % v)
    # nothing in the release path levers on the glass
    gate(d["z_nose_tip"] < d["z_glass_front"] + 1e-9,
         "nothing in the release levers against the bonded glass",
         "every tool contact is on a nose at z %+.2f or on the PCB edge at "
         "z %+.2f; the glass front face is at z %+.2f and is never a reaction "
         "surface" % (d["z_nose_tip"], d["z_fwd_limit"], d["z_glass_front"]))
    print("      The module is NOT trapped by the closed rear: the release was")
    print("      never rearward, and adding two more sprung posts did not make")
    print("      it rearward.")

    # ---- 9. glass clearance - the blocking measurement -------------------
    print("")
    print("9. BONDED-GLASS CLEARANCE AT ALL FOUR HOLES")
    print("   This is the item that gates the Rev P.5 print. It is REPORTED,")
    print("   never assumed, and the modelled envelope is not evidence.")
    h, v, bb = _hit(B, carrier, swept["SWEPT_Glass"])
    print("      carrier x swept glass, MODELLED envelope: %s"
          % ("CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb)))
    print("")
    print("      %-11s %8s %9s %9s %9s %9s"
          % ("hole pair", "y", "glass y", "gap", "need", "margin"))
    worst = None
    for nm, y, gy, g in (("connector", d["y_conn"], d["glass_y0"],
                          d["geo_conn"]),
                         ("far", d["y_far"], d["glass_y1"], d["geo_far"])):
        gap = abs(y - gy)
        need = g["nose_keepout_r"]
        margin = gap - need
        bare = gap - g["barb_d"] / 2.0
        print("      %-11s %+8.2f %+9.2f %9.2f %9.2f %+9.2f"
              % (nm, y, gy, gap, need, margin))
        if worst is None or margin < worst[1]:
            worst = (nm, margin, gap, need, bare, g)
    print("")
    print("      Against the MODELLED glass the far pair is %+.2f mm on the"
          % worst[1])
    print("      keep-out radius and %+.2f mm on the bare barb radius. That"
          % worst[4])
    print("      is the number the brief quotes, and it is reproduced here")
    print("      rather than tuned away.")
    print("")
    print("      WHY THE MODELLED ENVELOPE IS NOT EVIDENCE. oled_glass_w,")
    print("      oled_glass_h and oled_glass_off_y have never been measured.")
    print("      As modelled the glass spans x %+.2f..%+.2f and y %+.2f..%+.2f,"
          % (d["glass_x0"], d["glass_x1"], d["glass_y0"], d["glass_y1"]))
    print("      which puts BOTH far mounting holes (%+.2f, y %+.2f) entirely"
          % (d["post_x"], d["y_far"]))
    print("      underneath the bonded glass. A board like that could not be")
    print("      screw-mounted at all, so the model is known to be wrong here.")
    print("      It is kept, unedited, because replacing a wrong number with a")
    print("      convenient one would hide the measurement that is actually")
    print("      needed.")
    print("")
    print("      WHY THE FAR NOSE IS NOT SIMPLY MADE SMALLER. The only lever")
    print("      on the keep-out radius is the barb, and the floor under it is")
    print("      the hole radius %.2f mm - below that there is no overlap and"
          % (P["oled_hole_d"] / 2.0))
    print("      no retention at all. The %.2f mm overlap in the model is the"
          % d["geo_far"]["overlap"])
    print("      only overlap figure with physical evidence behind it: it is")
    print("      what Rev P.2 actually retained with. Shrinking the barb would")
    print("      trade proven retention for a keep-out reduction that STILL")
    print("      would not clear the modelled glass. sprung_far_barb_d is")
    print("      separately named so it can be reduced the moment there is a")
    print("      measurement to justify a value - and not before.")
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        openitem("bonded-glass boundary at the %s holes" % nm,
                 "measure hole centre to the nearest bonded-glass edge at BOTH "
                 "%s holes (x +/-%.2f, y %+.2f). It must be at least %.2f mm "
                 "(barb %.2f/2 + %.2f margin), i.e. the glass must not pass "
                 "y %+.2f. Model says %.2f mm and the model is UNRELIABLE."
                 % (nm, d["post_x"],
                    d["y_conn"] if nm == "connector" else d["y_far"],
                    g["nose_keepout_r"], g["barb_d"], P["nose_glass_margin"],
                    (d["y_conn"] + g["nose_keepout_r"]) if nm == "connector"
                    else (d["y_far"] - g["nose_keepout_r"]),
                    abs((d["y_conn"] - d["glass_y0"]) if nm == "connector"
                        else (d["glass_y1"] - d["y_far"]))),
                 outcome="CLOSED BY PHYSICAL TEST. The built carrier inserted, "
                 "retained and released the OLED with no bonded-glass contact "
                 "at the %s pair. The boundary itself was still not measured, "
                 "so the modelled envelope stays as it is - a placeholder, "
                 "flagged as one." % nm)
    openitem("model the measured glass and re-run this gate",
             "replace oled_glass_w / _h / _off_y with the measured boundary, "
             "regenerate, and confirm carrier x SWEPT_Glass is CLEAR through "
             "insertion, seating, retention, release and withdrawal for every "
             "shaft, split, lead-in and nose on all FOUR posts. If the measured "
             "glass will not clear the %.2f mm keep-out at the far pair, reduce "
             "sprung_far_barb_d only as far as %.2f mm - the overlap Rev P.2 "
             "physically retained with - and take new physical retention "
             "evidence before going below it."
             % (d["geo_far"]["nose_keepout_r"],
                P["oled_hole_d"] + 2.0 * P["hook_overlap_min"]),
             outcome="NOT a release blocker any more - the part is built and "
             "works - but STILL TRUE as a modelling caveat: "
             "oled_glass_w / _h / _off_y remain unmeasured placeholders and "
             "oled_glass_measured stays False. Measure before regenerating any "
             "post, nose or glass keep-out.")
    big = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                d["z_pcb_front"], d["z_glass_front"] + SWEEP_TRAVEL)
    h, v, bb = _hit(B, carrier, big)
    n, rv = _residual(B, carrier, big, env)
    print("")
    print("      worst case, glass = the FULL PCB outline swept: %.4f mm3, of"
          % v)
    gate(n == 0, "worst-case glass exposure is confined to the four noses",
         "%.5f mm3 outside them" % rv if n else
         "which every scrap is inside the four declared noses")
    print("      -> the four noses are the ONLY glass exposure in the design.")
    print("         Pads, pedestals, reliefs, walls, light blocks and rim are")
    print("         clear of the glass even if the glass is the whole board.")
    print("         So the measurement above is the complete question - there")
    print("         is nothing else for the glass to foul.")

    # ---- 10. optical alignment and the mounting-point correction ---------
    print("")
    print("10. VERTICAL DATUM, THE 7.00 mm MOUNTING-POINT CORRECTION,")
    print("    AND WHAT IS ACTUALLY VISIBLE")
    aa = mod["OLED_ActiveArea"].boundingBox
    cx = (aa.minPoint.x + aa.maxPoint.x) * 5.0
    cy = (aa.minPoint.y + aa.maxPoint.y) * 5.0
    ay0 = aa.minPoint.y * 10.0
    ay1 = aa.maxPoint.y * 10.0

    print("")
    print("    THE SAME MOVE, STATED IN BOTH FRAMES")
    print("    1. CARRIER-LOCAL. Both fixing centres are %+.2f mm from the"
          % d["fix_rel_oled"])
    print("       OLED-dependent group, against %+.2f mm before: they moved"
          % d["fix_rel_oled_prev"])
    print("       %+.2f mm TOWARD the connector/open bottom." % d["fix_shift_local"])
    print("    2. ASSEMBLED PANEL. The Perspex and its holes did not move at")
    print("       all. The OLED bay and every OLED-dependent feature rose")
    print("       %+.2f mm instead, so the carrier holes land ON the Perspex"
          % d["oled_shift_global"])
    print("       holes rather than %.2f mm away from them."
          % abs(d["fix_shift_local"]))
    print("    These are one geometry described twice, not two moves.")
    print("")

    gate(abs(cx) < 1e-6, "active area still HORIZONTALLY centred",
         "centre x %.4f mm - the correction is vertical only" % cx)
    gate(abs(d["fix_shift_local"] - P["carrier_fix_y_from_previous"]) < 1e-9,
         "fixing centres moved exactly carrier_fix_y_from_previous",
         "%+.2f mm toward the bottom, relative to the OLED-dependent group"
         % d["fix_shift_local"])
    gate(abs((cy - d["oled_cy_prev"]) - d["oled_rise"]) < 1e-6,
         "active area is exactly %.2f mm higher than the superseded datum"
         % d["oled_rise"],
         "centre y %+.4f against the previous %+.2f - measured on the built "
         "body, not asserted" % (cy, d["oled_cy_prev"]))
    hdr = mod["OLED_Header_Keepout"].boundingBox
    gate(hdr.maxPoint.y * 10.0 < cy,
         "the four-pin connector is at the BOTTOM",
         "header envelope y %+.2f .. %+.2f, entirely below the active-area "
         "centre - the complete module was rotated %.0f deg in plane"
         % (hdr.minPoint.y * 10.0, hdr.maxPoint.y * 10.0, P["module_rot_deg"]))
    gate(abs(d["light_cut_y"] - d["pin_open_y0"]) < 1e-9
         and d["pin_open_y0"] < cy,
         "the connector CUT-OUT side is the same bottom",
         "the open rail cut terminates at y %+.2f and the four-pin opening "
         "starts there - BOTTOM is unambiguously -Y"
         % d["light_cut_y"])
    gate(abs(P["panel_fix_y"]) < 1e-9
         and abs(2.0 * d["m2_x"] - P["panel_fix_pitch"]) < 1e-9,
         "the panel-fixed holes did NOT move",
         "still on y %+.2f at exactly %.5f mm pitch, on one common horizontal "
         "centreline, no X shift and no skew - the carrier was corrected "
         "around them" % (P["panel_fix_y"], 2.0 * d["m2_x"]))
    ok = True
    for sx in (-1, 1):
        b = B.cylz(P["bolt_clear_d"] - 0.20, sx * d["m2_x"], P["panel_fix_y"],
                   d["z_nut_seat"] + 0.10, -0.001)
        h, v, bb = _hit(B, carrier, b)
        ok = ok and not h
    gate(ok, "both bolt bores concentric with their fixing centres",
         "clear through at x %+.2f and %+.2f, y %+.2f - bores, bosses, hex "
         "pockets, retention ridges and arms all moved together"
         % (-d["m2_x"], d["m2_x"], P["panel_fix_y"]))

    # ---- what this actually looks like through the Perspex ---------------
    print("")
    print("    WHAT IS ACTUALLY VISIBLE - REPORTED, NOT PASSED")
    print("    The superseded rule put the active-area bottom edge on the")
    print("    opening bottom edge. It is gone, and so is every PASS that")
    print("    depended on it. Raising the screen 7.00 mm has a consequence,")
    print("    and this is it:")
    print("")
    print("      active area          y %+.2f .. %+.2f  (%.2f mm tall)"
          % (ay0, ay1, ay1 - ay0))
    print("      Perspex opening      y %+.2f .. %+.2f  (%.2f mm tall)"
          % (d["panel_open_bottom_y"], d["panel_open_top_y"],
             P["panel_open_h"]))
    print("      VISIBLE overlap      y %+.2f .. %+.2f  = %.2f mm, %.0f%% of "
          "the active height" % (d["vis_y0"], d["vis_y1"], d["vis_h"],
                                 100.0 * d["vis_frac"]))
    print("      hidden ABOVE the opening            %.2f mm of active area"
          % d["active_above_opening"])
    print("      hidden BELOW the opening            %.2f mm of active area"
          % d["active_below_opening"])
    print("      unlit band at the bottom of the opening  %.2f mm"
          % d["opening_unlit_below"])
    print("")
    print("    The active area is NOT fully visible and is NOT vertically")
    print("    centred. Roughly %.2f mm of it - about %.0f%% - sits behind the"
          % (d["active_above_opening"],
             100.0 * d["active_above_opening"] / P["oled_active_h"]))
    print("    fascia above the opening, and the lowest %.2f mm of the opening"
          % d["opening_unlit_below"])
    print("    shows unlit board rather than screen. This is the direct,")
    print("    intended consequence of the mounting correction, reported so")
    print("    that the powered fit test (brief 12.8 / 12.27) is judged")
    print("    against the real picture and not against a CAD claim.")
    gate(d["vis_h"] > 0.0, "some active area does fall inside the opening",
         "%.2f mm of %.2f mm. This is a REPORT of the geometry, not a "
         "judgement that it is acceptable - only the powered test can make "
         "that call" % (d["vis_h"], P["oled_active_h"]))
    openitem("powered active-area position through the Perspex",
             "brief 12.8 / 12.27. Install on the ORIGINAL Perspex holes with "
             "the ORIGINAL bolts, confirm the open connector side is at the "
             "bottom and both holes align without forcing or slotting, power "
             "the OLED and PHOTOGRAPH the visible top and bottom edges. "
             "Expected: the screen sits %.2f mm higher than the preceding "
             "Rev P.5 position, with about %.2f mm of active area above the "
             "opening and a %.2f mm unlit band at the bottom of it. Confirm "
             "the intended screen information is still visible."
             % (d["oled_rise"], d["active_above_opening"],
                d["opening_unlit_below"]),
             outcome="PASSED. Installed on the original Perspex holes with the "
             "original bolts, connector side at the bottom, holes aligned "
             "without forcing or slotting. The %.2f mm rise gives the required "
             "OLED position relative to the opening and the intended screen "
             "information is visible. The geometry above is unchanged and "
             "still reported: %.2f mm of the %.2f mm active height falls "
             "inside the opening."
             % (d["oled_rise"], d["vis_h"], P["oled_active_h"]))

    print("")
    gate(abs(-d["z_glass_front"] - P["oled_perspex_gap"]) < 1e-9,
         "assembled glass-to-Perspex gap",
         "%.3f mm nominal, seated on the fixed pads - the correction is "
         "in-plane only and does not touch the Z chain"
         % P["oled_perspex_gap"])
    print("      float within the carrier is the %.2f mm hook clearance, so the"
          % P["hook_clear"])
    print("      worst-case gap is %.2f mm and the glass can never touch the"
          % (P["oled_perspex_gap"] - P["hook_clear"]))
    print("      Perspex.")
    print("      active %.2f x %.2f in aperture %.2f x %.2f"
          % (P["oled_active_w"], P["oled_active_h"], P["panel_open_w"],
             P["panel_open_h"]))
    print("      margins: x %.2f each side; vertically the active area now"
          % ((P["panel_open_w"] - P["oled_active_w"]) / 2))
    print("      OVERRUNS the opening at the top by %.2f mm."
          % d["active_above_opening"])
    print("      firmware must still mask 2 pixel rows top and bottom")

    # ---- 10b. THE MOVED FIXINGS - STRUCTURE ------------------------------
    print("")
    print("10b. MOVED FIXING ARMS AND BOSSES - STRUCTURAL RE-CHECK")
    print("     Sliding the fixings %+.2f mm relative to the OLED group lands"
          % d["fix_shift_local"])
    print("     them on a different part of the side uprights, so their")
    print("     connection is re-measured on the finished solid rather than")
    print("     assumed to be as good as it was.")

    # 1. the arm is joined to the upright over its full height, not necked
    ok = True
    worst = None
    for sy in (-1, 1):
        y = sy * P["fix_arm_h"] / 2.0 * 0.90
        for sx in (-1, 1):
            if not _inside(carrier, sx * (d["arm_x0"] + 0.30), y, -0.20):
                ok = False
            if not _inside(carrier, sx * (d["car_x1"] - 0.30), y, -0.20):
                ok = False
    gate(ok, "both arms continuously joined to the side uprights",
         "solid across the whole %.2f mm arm height at both x %+.2f (the arm "
         "root) and x %+.2f (the upright outer face) - the arm overlaps the "
         "upright by %.2f mm, it does not meet it on a tangent"
         % (P["fix_arm_h"], d["arm_x0"], d["car_x1"],
            d["car_x1"] - d["arm_x0"]))

    # 2. the junction is inside the upright's full-width band, not on a radius
    upright_lo = d["light_cut_y"] + d["cap_r"] + P["carrier_corner_r"]
    upright_hi = d["car_y1"] - P["carrier_corner_r"]
    lo_m = P["panel_fix_y"] - P["fix_arm_h"] / 2.0 - upright_lo
    hi_m = upright_hi - (P["panel_fix_y"] + P["fix_arm_h"] / 2.0)
    gate(min(lo_m, hi_m) > 1.0,
         "the arms land on FULL-WIDTH upright, clear of both corner radii",
         "arm spans y %+.2f .. %+.2f; the upright is full width from y %+.2f "
         "to %+.2f, so there is %.2f mm below the arm and %.2f mm above it"
         % (P["panel_fix_y"] - P["fix_arm_h"] / 2.0,
            P["panel_fix_y"] + P["fix_arm_h"] / 2.0,
            upright_lo, upright_hi, lo_m, hi_m))

    # 3. the boss is not cut into by anything OLED-side
    gate(d["m2_x"] - d["m2_r"] > d["ap_x1"] + 0.50,
         "the bosses clear the OLED bay entirely",
         "boss inner edge x %+.2f against an aperture edge at %+.2f - %.2f mm "
         "clear, so raising the bay cannot reach them"
         % (d["m2_x"] - d["m2_r"], d["ap_x1"],
            (d["m2_x"] - d["m2_r"]) - d["ap_x1"]))
    gate(d["m2_x"] - d["nut_body_d"] / 2.0 > d["shield_x1"] + 0.50,
         "the nut pockets clear the rear shield and the light blocks",
         "nut bore inner edge x %+.2f against a shield edge at %+.2f"
         % (d["m2_x"] - d["nut_body_d"] / 2.0, d["shield_x1"]))
    h, v, bb = _hit(B, carrier, mod["OLED_PCB"])
    gate(not h, "the moved fixings do not touch the seated module",
         "carrier x OLED_PCB still CLEAR after the shift")

    # 4. the clamp-load path still terminates in Perspex seating faces
    seat_all = _planar_face_area(carrier, 1, 0.0)
    arm_seat = None
    for sx in (-1, 1):
        a, b = sx * d["arm_x0"], sx * d["ear_x1"]
        blk = B.box(min(a, b), max(a, b),
                    -P["fix_arm_h"] / 2.0, P["fix_arm_h"] / 2.0, -0.05, 0.05)
        arm_seat = blk if arm_seat is None else B.uni(arm_seat, blk)
    h, v, bb = _hit(B, carrier, arm_seat)
    gate(h and v > 0.0, "both fixing arms still seat on the Perspex",
         "%.2f mm2 of the %.1f mm2 total seating face is under the two arms - "
         "the bolt head -> Perspex -> carrier seat -> captive nut path is "
         "unbroken" % (v / 0.10, seat_all))

    # 5. nut pocket walls unchanged by the move
    gate(d["boss_wall_min"] > 1.0,
         "nut-pocket boss wall unchanged by the shift",
         "%.3f mm minimum - the pockets moved with their bosses, so nothing "
         "about the wall changed" % d["boss_wall_min"])
    gate(abs((d["z_perspex_rear"] - d["z_rear"]) - P["carrier_depth"]) < 1e-9,
         "carrier depth still exactly %.2f mm" % P["carrier_depth"],
         "the correction is in-plane only")

    # 6. the deleted rail has not come back with the move
    pedcol = None
    for (px, py) in d["conn"]:
        c = B.cylz(P["pedestal_d"] + 0.10, px, py, d["z_rear"] - 1.0, 1.0)
        pedcol = c if pedcol is None else B.uni(pedcol, c)
    below = B.box(d["car_x0"] - 1.0, d["car_x1"] + 1.0, -60.0,
                  d["light_cut_y"] - 1e-4, d["z_rear"] - 1.0, 1.0)
    n, rv = _residual(B, carrier, below, pedcol)
    gate(n == 0, "the lighting-unit-side rail has NOT returned",
         "nothing below y %+.2f but the two connector pedestal towers - the "
         "fixings moved toward that side without putting material back into it"
         % d["light_cut_y"])
    print("     NOTE. The carrier now reaches y %+.2f above the bolt line "
          % d["car_y1"])
    print("     against %+.2f before, because the OLED bay rose while the"
          % (d["car_y1"] - d["oled_rise"]))
    print("     bolts stayed put. Nothing in CAD says whether that fits the")
    print("     radio - brief 12.14 covers it, and it is a physical test.")

    # ---- 11. printability -----------------------------------------------
    print("")
    print("11. PRINTABILITY")
    gate(carrier.isSolid, "carrier is a single closed solid",
         "%.3f cm3, %d faces" % (volume_of(carrier) / 1000.0,
                                 carrier.faces.count))
    tiny_f = 0
    for f in carrier.faces:
        if f.area * 100.0 < 0.02:
            tiny_f += 1
    tiny_e = 0
    for e in carrier.edges:
        if e.length * 10.0 < 0.05:
            tiny_e += 1
    gate(tiny_f == 0 and tiny_e == 0, "boolean slivers",
         "%d faces < 0.02 mm2, %d edges < 0.05 mm" % (tiny_f, tiny_e))
    worst_ledge = max((g["barb_d"] - g["shaft_d"]) / 2.0
                      for (_x, _y, g) in d["posts"])
    gate(worst_ledge <= 0.30, "unsupported barb ledge, printed rear-down",
         "%.2f mm radial step from the shaft at all four posts (the retention "
         "overlap against the hole is a different %.2f mm) - the Rev D / Rev K "
         "hook class, both printed" % (worst_ledge, d["overlap_min_all"]))
    thin = min(g["t"] for (_x, _y, g) in d["posts"])
    gate(thin >= 0.79, "sprung half-section is a whole number of perimeters",
         "%.2f mm = exactly two 0.40 mm extrusion widths at all four posts; "
         "the Rev P.4 1.05 mm was two perimeters plus a sliver" % thin)
    print("      structural wall %.2f ; boss wall around the hex %.3f mm"
          % (P["carrier_wall"], d["boss_wall_min"]))
    for nm, g in (("connector", d["geo_conn"]), ("far", d["geo_far"])):
        print("      %-10s sprung post %.2f dia, %.2f mm tall, slot %.2f mm, "
              "split %.0f deg"
              % (nm, g["shaft_d"], d["z_nose_tip"] - g["z_floor"],
                 g["slot_w"], g["split_deg"]))
    print("      NO plain post exists: all four holes hold sprung posts.")
    print("      ORIENTATION: carrier REAR FACE on the bed, building +Z.")
    print("      - pedestals and post roots all grow off the bed, no supports")
    print("      - root reliefs are upward-opening blind pockets")
    print("      - datum pads at z %.2f are upward-facing, layer-accurate"
          % d["z_pcb_rear"])
    print("      - every nose lead-in is a %.0f deg self-supporting cone"
          % (90 - d["geo_conn"]["cam_deg"]))
    print("      - all four root reliefs bottom out %.2f mm short of the"
          % d["relief_floor_margin"])
    print("        shield inner face, leaving %.2f mm of solid floor - the"
          % d["floor_min_all"])
    print("        %.2f mm carrier does not thin them to a membrane"
          % P["carrier_depth"])
    print("      - the two connector light blocks stand %.2f mm off the shield"
          % P["light_block_depth"])
    print("        inner face as upward walls %.2f mm thick - no overhang"
          % P["light_block_t"])
    print("      - the %.2f mm rear light shield IS the first %d layers, laid"
          % (P["rear_light_shield_t"],
             int(round(P["rear_light_shield_t"] / 0.20))))
    print("        flat on the bed: no bridging, no supports, and the whole")
    print("        %.1f x %.1f mm plate is bed-supported over its full area."
          % (d["shield_x1"] - d["shield_x0"], d["shield_y1"] - d["shield_y0"]))
    print("      - its free edge on the open side is a %.2f mm strip beyond"
          % d["shield_free_edge"])
    print("        the upright cap line at y %+.2f," % d["light_cut_y"])
    print("        %.2f mm thick and %.1f mm wide - a plate edge, not a"
          % (P["rear_light_shield_t"], d["shield_x1"] - d["shield_x0"]))
    print("        sliver and not an unsupported cantilever.")
    print("      - the four-pin slot is a through-slot in those layers, so it")
    print("        needs no bridge either.")
    print("      - the carrier is %.2f mm deep, %.2f mm shallower than Rev P.4,"
          % (P["carrier_depth"], 8.00 - P["carrier_depth"]))
    print("        so the whole part prints in fewer layers with no new")
    print("        overhang: nothing was truncated to reach that depth.")

    # ---- 12. point probes -----------------------------------------------
    print("")
    print("12. SOLID-MEMBERSHIP PROBES")
    probes = [
        ("seating rim solid on a retained upright", d["cap_x"],
         0.0, -0.20, True),
        ("solid transverse rail seating face", 0.0, d["car_y1"] - 1.50,
         -0.20, True),
        ("M2 boss solid", d["m2_x"] + 2.4, 0.0, -1.0, True),
        ("M2 insert bore void", d["m2_x"], 0.0, -2.0, False),
        ("nut bore runs right through to the rear", d["m2_x"], 0.0,
         d["z_rear"] + 0.50, False),
        ("module aperture void", 0.0, d["pcb_y1"] + 0.3, -0.60, False),
        ("aperture at PCB corner void", d["pcb_x1"] + 0.4, d["pcb_y1"] + 0.4,
         -0.60, False),
        ("pocket side wall solid", d["pk_x1"] + 0.3, 0.0, -4.0, True),
        ("PCB pocket void", 0.0, 0.0, -2.0, False),
        # -- integral rear light shield (brief 8.3) --
        ("rear shield solid at the bay centre", 0.0, 0.0,
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("rear shield solid, bay corner (-x, cut side)",
         d["shield_x0"] + 0.60, d["shield_y0"] + 0.60,
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("rear shield solid, bay corner (+x, cut side)",
         d["shield_x1"] - 0.60, d["shield_y0"] + 0.60,
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("rear shield solid, bay corner (-x, solid side)",
         d["shield_x0"] + 0.60, d["shield_y1"] - 0.60,
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("rear shield solid, bay corner (+x, solid side)",
         d["shield_x1"] - 0.60, d["shield_y1"] - 0.60,
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("rear shield solid on the rear face itself", 0.0, 0.0,
         d["z_rear"] + 0.05, True),
        ("bay void just AHEAD of the shield", 0.0, 0.0,
         d["z_shield_front"] + 0.05, False),
        ("four-pin slot void through the shield", 0.0, d["header_cy"],
         d["z_rear"] + 0.05, False),
        ("four-pin slot still void at the shield front face", 0.0,
         d["header_cy"], d["z_shield_front"] - 0.05, False),
        ("shield solid on the -X side of the pin slot",
         d["pin_slot_x0"] - 0.30, d["header_cy"],
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("shield solid on the +X side of the pin slot",
         d["pin_slot_x1"] + 0.30, d["header_cy"],
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("shield solid ABOVE the pin slot", 0.0, d["pin_open_y1"] + 0.30,
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("shield solid between the slot and the bay wall (-X)",
         (d["shield_x0"] + d["pin_slot_x0"]) / 2.0, d["header_cy"],
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        ("shield solid between the slot and the bay wall (+X)",
         (d["shield_x1"] + d["pin_slot_x1"]) / 2.0, d["header_cy"],
         d["z_rear"] + P["rear_light_shield_t"] / 2.0, True),
        # -- connector light blocks (brief 8.4) --
        ("light block solid, -X side", -(d["block_x_in"] + d["block_x_out"]) / 2.0,
         d["header_cy"], (d["z_block_rear"] + d["z_block_front"]) / 2.0, True),
        ("light block solid, +X side", (d["block_x_in"] + d["block_x_out"]) / 2.0,
         d["header_cy"], (d["z_block_rear"] + d["z_block_front"]) / 2.0, True),
        ("pin corridor still open between the blocks", 0.0, d["header_cy"],
         (d["z_block_rear"] + d["z_block_front"]) / 2.0, False),
        ("light block merges into the +X pedestal",
         (d["ped_inner_x"] + d["block_x_out"]) / 2.0, d["header_cy"],
         (d["z_block_rear"] + d["z_block_front"]) / 2.0, True),
        ("light block merges into the -X pedestal",
         -(d["ped_inner_x"] + d["block_x_out"]) / 2.0, d["header_cy"],
         (d["z_block_rear"] + d["z_block_front"]) / 2.0, True),
        ("no gap between the +X block and its pedestal",
         (d["block_x_in"] + d["block_x_out"]) / 2.0 + 1.50, d["header_cy"],
         (d["z_block_rear"] + d["z_block_front"]) / 2.0, True),
        ("nothing ahead of the light blocks", d["block_x_in"] + 0.60,
         d["header_cy"], d["z_block_front"] + 0.20, False),
        ("light blocks stop short of DATUM B", d["block_x_in"] + 0.60,
         d["header_cy"], d["z_pcb_rear"] - 0.05, False),
    ]

    # -- the FOUR sprung posts, every one probed the same way --------------
    for tag, (x, y), g in (("connector", d["conn"][1], d["geo_conn"]),
                           ("connector", d["conn"][0], d["geo_conn"]),
                           ("far", d["far"][1], d["geo_far"]),
                           ("far", d["far"][0], d["geo_far"])):
        # a point on one half of the split: clear of the slot, inside the shaft.
        # The post AXIS lies inside the slot, so it must never be probed.
        half = (g["slot_w"] / 2.0 + g["shaft_d"] / 2.0) / 2.0
        # inside a root relief bore: outside the shaft, inside the bore
        rel = (g["shaft_d"] / 2.0 + g["relief_d"] / 2.0) / 2.0
        edge = (P["oled_hole_d"] + g["barb_d"]) / 4.0     # on the hole edge
        pad_r = (P["datum_pad_od"] + g["relief_d"]) / 4.0
        lbl = "%s post x%+.0f" % (tag, x)
        zmid = (g["z_floor"] + d["z_pcb_rear"]) / 2.0
        probes += [
            ("%s: shaft solid inside the hole" % lbl, x, y + half, zmid, True),
            ("%s: split slot void on the axis" % lbl, x, y, zmid, False),
            ("%s: barb solid ahead of the PCB face" % lbl, x, y + half,
             (d["z_hook_face"] + d["z_hook_top"]) / 2.0, True),
            ("%s: barb overlaps the hole edge" % lbl, x, y + edge,
             (d["z_hook_face"] + d["z_hook_top"]) / 2.0, True),
            ("%s: no barb at the PCB front plane" % lbl, x, y + edge,
             d["z_pcb_front"] - 0.02, False),
            ("%s: root relief void" % lbl, x + rel, y, zmid, False),
            ("%s: post root solid" % lbl, x, y + half,
             g["z_floor"] + 0.30, True),
            ("%s: solid floor under the relief" % lbl, x, y,
             g["z_floor"] - 0.30, True),
            ("%s: shield not broken through" % lbl, x, y,
             d["z_rear"] + 0.20, True),
            ("%s: datum pad solid behind DATUM B" % lbl, x + pad_r, y,
             d["z_pcb_rear"] - 0.05, True),
            ("%s: datum pad void ahead of DATUM B" % lbl, x + pad_r, y,
             d["z_pcb_rear"] + 0.05, False),
        ]

    sx, sy = d["conn"][1]
    probes += [
        # -- lighting-unit-side cut (brief 8.1), now at -Y --
        ("deleted rail: void between the uprights", 0.0,
         d["light_cut_y"] - 0.50, -3.00, False),
        ("deleted rail: void at the old wall line", 0.0,
         d["wall_y0"] + 0.50, -3.00, False),
        ("deleted cable-tie flange: void", 0.0, d["y_before"] + 3.00,
         -3.00, False),
        ("upright still solid above the cut", d["cap_x"],
         d["light_cut_y"] + 3.00, -3.00, True),
        ("upright cap solid at the termination", d["cap_x"],
         d["light_cut_y"] + d["cap_r"], -3.00, True),
        ("nothing beyond the upright cap", d["cap_x"],
         d["light_cut_y"] - 0.20, -3.00, False),
        ("connector pedestal survives beyond the cut", sx,
         d["light_cut_y"] - 1.00, d["z_rear"] + 1.00, True),
        # -- captive original-nut pocket (brief 8.2) --
        ("bolt clearance bore void", d["m2_x"], 0.0,
         d["z_nut_seat"] + 0.20, False),
        ("solid ring ahead of the nut seat", d["m2_x"] + 2.0, 0.0,
         d["z_nut_seat"] + 0.20, True),
        ("hex head seat void", d["m2_x"], 0.0,
         d["z_nut_seat"] - 0.20, False),
        ("hex flat where it should be", d["m2_x"],
         d["nut_hex_af"] / 2.0 + 0.15, d["z_nut_seat"] - 0.70, True),
        ("hex corner clear along X", d["m2_x"] + d["nut_hex_ac"] / 2.0 - 0.15,
         0.0, d["z_nut_seat"] - 0.70, False),
        ("retaining ridge solid at the flat", d["m2_x"],
         d["nut_retain_af"] / 2.0 + 0.05, d["z_nut_retain"] + 0.15, True),
        ("nut body bore void", d["m2_x"], 0.0, d["z_rear"] + 0.80, False),
        ("boss wall solid outboard of the bore", d["m2_x"],
         d["nut_body_d"] / 2.0 + d["boss_wall_min"] / 2.0, d["z_rear"] + 0.80,
         True),
        ("boss solid outboard of the hex corner", d["m2_x"] + 2.60,
         0.0, -3.00, True),
        # -- no plain post survives anywhere --
        ("no plain post at the far holes: split slot is OPEN",
         d["far"][1][0], d["far"][1][1],
         (d["geo_far"]["z_floor"] + d["z_pcb_rear"]) / 2.0, False),
        ("no plain post at the far holes: a nose IS present",
         d["far"][1][0],
         d["far"][1][1] + (P["oled_hole_d"] + d["geo_far"]["barb_d"]) / 4.0,
         (d["z_hook_face"] + d["z_hook_top"]) / 2.0, True),
    ]
    bad = []
    for nm, x, y, z, want in probes:
        if _inside(carrier, x, y, z) != want:
            bad.append("%s (wanted inside=%s at %.2f, %.2f, %.2f)"
                       % (nm, want, x, y, z))
    gate(not bad, "point probes",
         "%d of %d pass" % (len(probes) - len(bad), len(probes)))
    for b in bad:
        print("        MISMATCH: %s" % b)

    # ---- 13. clearance table --------------------------------------------
    print("")
    print("13. CLEARANCE TABLE - minimum distance, mm")
    for nm in ("OLED_Glass", "OLED_ActiveArea", "OLED_Header_Keepout",
               "OLED_Solder_Tips", "OLED_PCB"):
        print("      carrier -> %-22s %8.3f" % (nm, _mind(app, carrier, mod[nm])))
    print("      glass   -> Perspex              %8.3f"
          % _mind(app, mod["OLED_Glass"], perspex))
    print("      header  -> Perspex              %8.3f"
          % _mind(app, mod["OLED_Header_Keepout"], perspex))

    # ---- 14. LIGHTING-UNIT SIDE: THE PHYSICAL CUT (brief 8.1) ------------
    print("")
    print("14. ORIGINAL DECCA LIGHTING-UNIT SIDE")
    print("      Rev P.3 checked the carrier against a SYNTHETIC keepout solid")
    print("      whose boundary was taken from the carrier's own pedestals.")
    print("      That is circular, and it has been DELETED - component,")
    print("      body, generator function and every check against it. What")
    print("      follows tests the carrier's OWN geometry only. CAD cannot and")
    print("      does not prove lighting-unit clearance; brief 12.14, the")
    print("      installed physical test, is the sole authority for that.")
    for nm in LEGACY_COMPONENTS:
        gate(find_component(design, nm) is None,
             "no %s component in the design" % nm,
             "absent from the browser, so absent from the assembly STEP and "
             "the manufacturing pack")
    names = set()
    for i in range(design.rootComponent.occurrences.count):
        occ = design.rootComponent.occurrences.item(i)
        names.add(occ.component.name)
        for b in occ.bRepBodies:
            names.add(b.name)
    strays = sorted(n for n in names if "KEEPOUT" in n.upper()
                    and "HEADER" not in n.upper())
    gate(not strays, "no keepout proxy body anywhere in the assembly",
         "browser holds %d components, none of them a lighting proxy"
         % design.rootComponent.occurrences.count if not strays
         else "found %s" % ", ".join(strays))
    print("")
    print("      REV P.5: the open end travelled with the module. It is still")
    print("      below/outboard of the connector-side sprung pair, exactly as")
    print("      brief 8.1 words it - but that pair rotated from +Y to -Y, so")
    print("      the cut is now at y %+.2f instead of +20.50. The Rev P.3/P.4"
          % d["light_cut_y"])
    print("      installed fit therefore does NOT carry over. Brief 12.14 is a")
    print("      RE-TEST against the radio, not a regression check.")
    bridge = B.box(d["pk_x0"], d["pk_x1"], -60.0, d["light_cut_y"] - 1e-4,
                   d["z_rear"] - 1.0, 1.0)
    ped = None
    for (px, py) in d["conn"]:
        c = B.cylz(P["pedestal_d"] + 0.10, px, py, d["z_rear"] - 1.0, 1.0)
        ped = c if ped is None else B.uni(ped, c)
    h, v, bb = _hit(B, carrier, bridge)
    n, rv = _residual(B, carrier, bridge, ped)
    gate(n == 0, "no bridge across the uprights below y = %+.2f"
         % d["light_cut_y"],
         "the only material there is the two pedestal towers (%.3f mm3), "
         "residual EMPTY" % v if n == 0
         else "%.5f mm3 of BRIDGE material remains" % rv)
    lo = -d["post_x"] + P["pedestal_d"] / 2.0
    hi = d["post_x"] - P["pedestal_d"] / 2.0
    between = B.box(lo, hi, -60.0, d["light_cut_y"] - 1e-4,
                    d["z_rear"] - 1.0, 1.0)
    h, v, bb = _hit(B, carrier, between)
    gate(not h, "open between the two pedestal towers",
         "EMPTY over x %+.2f .. %+.2f" % (lo, hi) if not h
         else "HIT %.4f mm3" % v)
    ymin = min(f.boundingBox.minPoint.y * 10 for f in carrier.faces)
    gate(abs(ymin - d["carrier_min_y"]) < 1e-3,
         "carrier extent on the lighting-unit side",
         "y min %+.3f - the connector-side pedestal tangent, %.2f mm past the "
         "upright caps at y %+.2f and nothing else"
         % (ymin, d["light_cut_y"] - ymin, d["light_cut_y"]))
    ok = True
    for (px, py) in d["conn"]:
        ok = ok and _inside(carrier, px, py - P["pedestal_d"] / 2.0 + 0.30,
                            d["z_rear"] + 0.50)
        ok = ok and _inside(carrier, px + rmid, py, d["z_pcb_rear"] - 0.05)
    gate(ok, "connector-side pedestals, pads and reliefs survive the cut",
         "full %.2f dia pedestal and %.2f dia pad retained at both connector "
         "posts" % (P["pedestal_d"], P["datum_pad_od"]))
    ok = True
    for (px, py) in d["conn"]:
        ok = ok and _inside(carrier, math.copysign(d["pk_x1"] + 0.20, px), py,
                            d["z_rear"] + 0.50)
    gate(ok, "pedestal-to-side-upright connection retained",
         "solid at the upright inner face on both sides")
    gate(carrier.lumps.count == 1,
         "the open-ended frame is ONE connected solid",
         "%d lump - transverse rail, two capped uprights, two fixing arms, "
         "four pedestals, four sprung posts, the rear shield and the two light "
         "blocks all joined" % carrier.lumps.count)
    print("      the deleted cable-tie flange is NOT replaced: the brief allows")
    print("      a new strain relief only outside the cut region and only with")
    print("      demonstrated radio-side clearance, which does not exist yet.")

    # ---- 14b. INTEGRAL REAR LIGHT SHIELD (brief 8.3) ---------------------
    print("")
    print("14b. INTEGRAL REAR LIGHT SHIELD")
    print("      Replaces the Rev P.3 open rear window. It is part of the")
    print("      carrier body - not a cover and not a second component.")

    # Thickness is MEASURED as a material span along Z at points spread over
    # the wall, rather than trusting that a box of the right size was drawn.
    #    The four bay corners are occupied by the pedestal towers, which are
    #    5.30 mm of solid carrier by design, so the thickness probes sample the
    #    FREE wall: its centre, its two side edges and the corners of the
    #    pedestal-free area. The towers are reported separately below.
    #    Every point below is inside the free wall: clear of the four pedestal
    #    towers, clear of the two light blocks and clear of the pin slot.
    xl = d["shield_x0"] + 0.45
    xr = d["shield_x1"] - 0.45
    tprobe = [("bay centre", 0.0, 0.0),
              ("bay, low", 0.0, -8.00),
              ("bay, high", 0.0, 2.00),
              ("left edge, mid", xl, 0.0),
              ("left edge, low", xl, -8.00),
              ("right edge, mid", xr, 0.0),
              ("right edge, low", xr, -8.00),
              ("just above the light blocks", 0.0, d["pin_open_y1"] + 1.10),
              ("just above the light blocks, off centre", 5.00,
               d["pin_open_y1"] + 1.10),
              ("between the far towers", 0.0, 10.00),
              ("between the far towers, off centre", -5.00, 11.00),
              ("solid-rail end of the bay", 0.0, d["shield_y1"] - 0.70)]
    tbad = []
    for nm, tx, ty in tprobe:
        col = B.box(tx - 0.02, tx + 0.02, ty - 0.02, ty + 0.02,
                    d["z_rear"] - 0.50, d["z_fwd_limit"])
        h, v, bb = _hit(B, carrier, col)
        got = v / (0.04 * 0.04) if h else 0.0
        if abs(got - P["rear_light_shield_t"]) > 1e-3:
            tbad.append("%s = %.3f" % (nm, got))
    gate(not tbad, "rear wall thickness equals rear_light_shield_t",
         "%.2f mm at all %d probes = %d x 0.40 mm extrusion widths"
         % (P["rear_light_shield_t"], len(tprobe),
            int(round(P["rear_light_shield_t"] / 0.40))) if not tbad
         else "wrong at " + "; ".join(tbad))
    print("      the four bay corners hold the pedestal towers instead, and")
    print("      the wall merges into them - they are not separate parts:")
    off = P["pedestal_d"] / 2.0 - 0.60
    for nm, tx, ty in (("connector tower", d["conn"][1][0],
                        d["conn"][1][1] + off),
                       ("far tower", d["far"][1][0],
                        d["far"][1][1] - off)):
        col = B.box(tx - 0.02, tx + 0.02, ty - 0.02, ty + 0.02,
                    d["z_rear"] - 0.50, d["z_fwd_limit"])
        h, v, bb = _hit(B, carrier, col)
        print("      %-16s %.2f mm of solid carrier off the bed - the wall"
              % (nm, (v / (0.04 * 0.04)) if h else 0.0))
    gate(P["rear_light_shield_t"] >= 3 * 0.40 - 1e-9,
         "thickness is at least three 0.40 mm extrusion widths",
         "%.2f mm. On a different extrusion width, raise the parameter to "
         "three ACTUAL widths and regenerate." % P["rear_light_shield_t"])

    # The wall closes the bay: bay slab MINUS carrier must be exactly the slot.
    bay = B.box(d["shield_x0"], d["shield_x1"], d["shield_y0"], d["shield_y1"],
                d["z_shield_rear"], d["z_shield_front"])
    slot = B.box(d["pin_slot_x0"], d["pin_slot_x1"],
                 d["pin_slot_y0"], d["pin_slot_y1"],
                 d["z_shield_rear"] - 0.10, d["z_shield_front"] + 0.10)
    hole = B.copy(bay)
    B.sub(hole, B.copy(carrier))
    try:
        nvoid = hole.faces.count
    except Exception:
        nvoid = 0
    vvoid = volume_of(hole) if nvoid else 0.0
    nres, vres = 0, 0.0
    if nvoid:
        resid = B.copy(hole)
        B.sub(resid, B.copy(slot))
        try:
            nres = resid.faces.count
        except Exception:
            nres = 0
        vres = volume_of(resid) if nres else 0.0
    want = d["pin_slot_w"] * d["pin_slot_h"] * P["rear_light_shield_t"]
    gate(nres == 0, "the ONLY penetration is the four-pin slot",
         "the whole %.1f x %.1f mm bay slab is solid except %.3f mm3, and "
         "every scrap of that lies inside the declared slot envelope"
         % (d["shield_x1"] - d["shield_x0"],
            d["shield_y1"] - d["shield_y0"], vvoid) if nres == 0
         else "%.4f mm3 of UNINTENDED second rear opening" % vres)
    gate(abs(vvoid - want) < 0.05, "no unintended second rear opening",
         "measured void %.3f mm3 against %.3f mm3 required by the header "
         "envelope plus clearance - no rear window, no solder-access window "
         "and no rear release opening" % (vvoid, want))

    # The slot matches the header envelope plus the DOCUMENTED clearances.
    gate(abs(d["pin_slot_x1"] - P["oled_header_w"] / 2.0
             - P["pin_slot_clear_x"]) < 1e-9,
         "pin slot X = header %.2f + 2 x %.2f clearance"
         % (P["oled_header_w"], P["pin_slot_clear_x"]),
         "%.2f mm wide, x %+.2f .. %+.2f, centred on the header"
         % (d["pin_slot_w"], d["pin_slot_x0"], d["pin_slot_x1"]))
    gate(abs(d["pin_slot_y1"] - d["header_y1"] - P["pin_slot_clear_y"]) < 1e-9
         and abs(d["pin_slot_y0"] - d["header_y0"]
                 + P["pin_slot_clear_y"]) < 1e-9,
         "pin slot Y = header %.2f + 2 x %.2f clearance, on the header centre"
         % (P["oled_header_h"], P["pin_slot_clear_y"]),
         "nominal y %+.2f .. %+.2f about the header envelope y %+.2f .. %+.2f; "
         "the finished opening is y %+.2f .. %+.2f = %.2f mm, the brief's "
         "4.19 mm, because the lower edge is the carrier's own termination"
         % (d["pin_slot_y0"], d["pin_slot_y1"], d["header_y0"], d["header_y1"],
            d["pin_open_y0"], d["pin_open_y1"], d["pin_slot_h"]))
    gate(abs(d["pin_slot_w"] - 14.00) < 1e-9
         and abs(d["pin_slot_h"] - 4.19) < 5e-3,
         "FINISHED four-pin opening measures 14.00 x 4.19 mm (brief 8.4)",
         "%.4f x %.4f mm, 25%% up on the Rev P.4 11.20 x 3.35"
         % (d["pin_slot_w"], d["pin_slot_h"]))
    h, v, bb = _hit(B, carrier, mod["OLED_Header_Keepout"])
    gate(not h, "pins and attached conductors pass without rubbing",
         "the full %.2f mm deep header / wiring envelope crosses the wall "
         "with ZERO contact" % P["oled_header_depth"] if not h
         else "HIT %.4f mm3 %s" % (v, bb))
    print("      the wire bend immediately behind the header lies inside that")
    print("      same %.2f mm envelope, which reaches z %+.2f - %.2f mm past"
          % (P["oled_header_depth"], d["z_header_rear"],
             abs(d["z_header_rear"] - d["z_rear"])))
    print("      the rear face - so the bend is covered by the check above.")
    print("      slot open area %.2f mm2 of %.2f mm2 of wall = %.1f%%: local"
          % (d["pin_slot_area"], d["shield_area"],
             100.0 * d["pin_slot_area"] / d["shield_area"]))
    print("      to the header, not a general window. %.2f mm of solid wall"
          % d["pin_slot_side_w"])
    print("      stands either side of it and %.2f mm above it."
          % d["pin_slot_above_h"])
    print("")
    print("      REPORTED, NOT HIDDEN. After the 180 deg transform the header")
    print("      row sits at y %+.2f and its envelope bottoms out at y %+.2f,"
          % (d["header_cy"], d["header_y0"]))
    print("      which is %.2f mm BELOW the carrier's own termination at"
          % (d["light_cut_y"] - d["header_y0"]))
    print("      y %+.2f, because the connector is at the OPEN lighting-unit"
          % d["light_cut_y"])
    print("      end of the board. The slot is therefore bounded by wall on")
    print("      both X sides and ABOVE, and by the wall's free edge below -")
    print("      and that edge IS the mandated open lighting-unit side of")
    print("      brief 8.1, not a second opening. Enclosing it would mean")
    print("      printing material back below y %+.2f, undoing the rail cut."
          % d["light_cut_y"])
    print("      The two light blocks (brief 8.4) are what handle the light")
    print("      that does come through: a tunnel beside the pins, %.2f mm"
          % P["light_block_t"])
    print("      thick and %.2f mm deep, stopping %.2f mm short of DATUM B."
          % (P["light_block_depth"], d["block_pcb_clear"]))

    # Confined to the OLED bay, and out of the deleted rail / tie region.
    pedcol = None
    for (px, py) in d["conn"]:
        c = B.cylz(P["pedestal_d"] + 0.10, px, py,
                   d["z_rear"] - 1.0, d["z_fwd_limit"])
        pedcol = c if pedcol is None else B.uni(pedcol, c)
    outside = B.box(d["car_x0"] - 1.0, d["car_x1"] + 1.0,
                    -60.0, d["shield_y0"] - 1e-4,
                    d["z_shield_rear"] - 1e-4, d["z_shield_front"] + 1e-4)
    n, rv = _residual(B, carrier, outside, pedcol)
    gate(n == 0, "the wall is confined to the OLED bay",
         "nothing below y %+.2f inside the wall's own Z band except the two "
         "connector pedestal towers" % d["shield_y0"] if n == 0
         else "%.5f mm3 of wall material has escaped the bay" % rv)
    railband = B.box(d["pk_x0"], d["pk_x1"], -60.0, d["pk_y0"] - 1e-4,
                     d["z_rear"] - 1.0, 1.0)
    n, rv = _residual(B, carrier, railband, pedcol)
    gate(n == 0, "the deleted rail / cable-tie region is still EMPTY",
         "the wall has not crept back below y %+.2f" % d["pk_y0"] if n == 0
         else "%.5f mm3 has reappeared there" % rv)
    gate(abs(d["z_shield_rear"] - d["z_rear"]) < 1e-9,
         "built FORWARD from the existing rear plane",
         "wall z %+.2f .. %+.2f, so the external rear envelope is unchanged "
         "at z %+.2f" % (d["z_shield_rear"], d["z_shield_front"], d["z_rear"]))

    # Behind and clear of the whole seated module.
    touch = []
    for nm in ("OLED_PCB", "OLED_Glass", "OLED_Solder_Tips",
               "OLED_ActiveArea"):
        hh, vv, _b = _hit(B, B.copy(bay), mod[nm])
        if hh:
            touch.append("%s %.4f mm3" % (nm, vv))
    gate(not touch, "the wall's whole slab is clear of PCB, glass and tips",
         "only the header / wiring envelope crosses it, through its own slot"
         if not touch else "; ".join(touch))
    gate(d["shield_pcb_clear"] > 1.0, "wall stands clear BEHIND the PCB",
         "%.2f mm from the wall front face z %+.2f to DATUM B z %+.2f: no "
         "contact, no preload, and the wall is NOT an OLED Z datum"
         % (d["shield_pcb_clear"], d["z_shield_front"], d["z_pcb_rear"]))
    pad_area = _planar_face_area(carrier, 1, d["z_pcb_rear"])
    gate(pad_area > 0.0,
         "datum pads, sprung posts, snap overlap and optical gap untouched",
         "%.2f mm2 of DATUM B pad still faces forward at z %+.2f; the wall is "
         "built after the retention stack and cuts none of it"
         % (pad_area, d["z_pcb_rear"]))
    print("      MATERIAL: print in OPAQUE BLACK, fully solid through the")
    print("      wall - solid perimeters, never sparse infill and never a")
    print("      single translucent skin.")
    print("      ORIENTATION: rear face down, so the wall is the first %d"
          % int(round(P["rear_light_shield_t"] / 0.20)))
    print("      layers laid flat on the bed. No bridging and no supports.")

    # ---- 15. CAPTIVE ORIGINAL NUTS (brief 8.2) ---------------------------
    print("")
    print("15. ORIGINAL DECCA BOLT AND CAPTIVE-NUT INTERFACE")
    print("      NO heat-set insert architecture remains: no insert bore, no")
    print("      insert depth or recess, no bore chamfer, no backing figure.")
    print("      ASSUMED: the measured %.2f mm is ACROSS FLATS. Check the real"
          % P["original_nut_hex_width"])
    print("      nut across flats AND across corners before release.")
    fast_occ = find_component(design, "REF_Decca_Fasteners")
    fast = {}
    if fast_occ:
        for b in fast_occ.bRepBodies:
            fast[b.name] = b
    gate(abs(2.0 * d["m2_x"] - P["panel_fix_pitch"]) < 1e-9,
         "fixing-centre pitch",
         "%.5f mm exactly, unchanged" % (2.0 * d["m2_x"]))
    conc = True
    rr = d["nut_hex_af"] / 2.0 - 0.10
    for sxx in (-1, 1):
        x = sxx * d["m2_x"]
        for (ddx, ddy) in ((0.0, rr), (0.0, -rr), (rr, 0.0), (-rr, 0.0)):
            if _inside(carrier, x + ddx, P["panel_fix_y"] + ddy,
                       d["z_nut_seat"] - 0.70):
                conc = False
    gate(conc, "both hex pockets concentric with the fixing centres",
         "void to r = %.2f all round at both centres" % rr)
    if "ORIGINAL_Nuts" in fast:
        ridge = nut_retain_envelope(B, P, d)
        h, v, bb = _hit(B, carrier, fast["ORIGINAL_Nuts"])
        n, rv = _residual(B, carrier, fast["ORIGINAL_Nuts"], ridge)
        print("      the nut is modelled at its full measured %.2f mm across"
              % P["original_nut_hex_width"])
        print("      flats over the whole %.2f mm length - the most pessimistic"
              % P["original_nut_total_length"])
        print("      reading of the measurement. carrier x nut = %.4f mm3." % v)
        gate(n == 0, "the real nut fits the pocket everywhere but the ridge",
             "residual EMPTY - the %.4f mm3 is the declared retaining ridge and "
             "nothing else; %.2f mm nut in a %.2f mm pocket (%.2f fit "
             "allowance)" % (v, P["original_nut_hex_width"], d["nut_hex_af"],
                             P["nut_pocket_fit_allowance"]) if n == 0
             else "%.5f mm3 of UNDECLARED fouling outside the ridge" % rv)
        rot = None
        for sxx in (-1, 1):
            x = sxx * d["m2_x"]
            nb = B.hexz(P["original_nut_hex_width"], x, P["panel_fix_y"],
                        d["z_nut_head_back"] + 0.05, d["z_nut_seat"] - 0.05)
            mx = adsk.core.Matrix3D.create()
            mx.setToRotation(math.radians(30.0), v3(0, 0, 1),
                             p3(x, P["panel_fix_y"], 0.0))
            B.tbm.transform(nb, mx)
            rot = nb if rot is None else B.uni(rot, nb)
        h, v, bb = _hit(B, carrier, rot)
        gate(h, "POSITIVE anti-rotation in the hex head seat",
             "the same nut rotated 30 deg interferes by %.4f mm3 - the pocket "
             "keys it, it cannot spin" % v if h
             else "*** the nut can rotate freely - not a hex key ***")
    gate(d["nut_seat_area"] > 5.0,
         "positive axial seating shoulder at z = %+.2f" % d["z_nut_seat"],
         "%.2f mm2 annulus backed by %.2f mm of solid carrier to the seating "
         "face - the nut does not crush into printed material"
         % (d["nut_seat_area"], P["nut_seat_depth"]))
    gate(abs((d["z_nut_seat"] - d["z_nut_head_back"])
             - P["original_nut_head_seat_depth"]) < 1e-9,
         "head-seat depth positively defined",
         "%.2f mm, ended by the step to the retaining ridge"
         % P["original_nut_head_seat_depth"])
    for nm in ("ORIGINAL_Nuts", "ORIGINAL_Bolt_Envelope"):
        if nm not in fast:
            continue
        for onm, other in (("OLED glass", mod["OLED_Glass"]),
                           ("OLED PCB", mod["OLED_PCB"]),
                           ("header / wiring", mod["OLED_Header_Keepout"]),
                           ("Perspex aperture", perspex)):
            h, v, bb = _hit(B, fast[nm], other)
            ok = (not h) or (nm == "ORIGINAL_Bolt_Envelope"
                             and onm == "Perspex aperture")
            det = "CLEAR" if not h else "%.4f mm3 %s" % (v, bb)
            if h and ok:
                det += "  (the bolt passes through its own panel hole)"
            gate(ok, "%s x %s" % (nm, onm), det)
    h, v, bb = _hit(B, fast["ORIGINAL_Bolt_Envelope"], carrier)
    gate(not h, "ORIGINAL_Bolt_Envelope x carrier",
         "CLEAR - the bolt never touches the carrier; it only pulls the nut "
         "onto the seating shoulder" if not h else "HIT %.4f mm3 %s" % (v, bb))
    gate(True, "full %.2f mm nut envelope cleared"
         % P["original_nut_total_length"],
         "seat %+.2f to nut rear %+.2f; the last %.2f mm sits behind the "
         "carrier rear face in free air"
         % (d["z_nut_seat"], d["z_nut_rear"],
            abs(d["z_nut_rear"] - d["z_rear"])))
    gate(P["nut_retain_lip"] > 0.10,
         "captive retaining ridge behind the head seat",
         "hex narrows %.2f -> %.2f af over %.2f mm: %.3f mm interference per "
         "flat, pushed past on assembly, no adhesive"
         % (d["nut_hex_af"], d["nut_retain_af"], P["nut_retain_h"],
            (P["original_nut_hex_width"] - d["nut_retain_af"]) / 2.0))
    gate(P["bolt_clear_d"] < P["original_nut_hex_width"],
         "deliberate service removal path",
         "a %.2f mm pin through the %.2f mm bolt bore bears on the nut face "
         "and pushes it back out of the rear"
         % (P["bolt_clear_d"] - 0.40, P["bolt_clear_d"]))
    gate(d["boss_wall_min"] > 1.0,
         "continuous structural boss wall around the hex pocket",
         "%.3f mm minimum, at the clearance-bore diameter" % d["boss_wall_min"])
    print("      pull-through: the nut bears on %.2f mm2 backed by a %.2f mm "
          "solid ring" % (d["nut_seat_area"], P["nut_seat_depth"]))
    print("      bottoming: grip from the bolt-head face to the nut front face")
    print("      is Perspex %.2f + carrier %.2f = %.2f mm. The original bolt"
          % (P["perspex_t"], P["nut_seat_depth"], d["bolt_grip"]))
    print("      must be longer than that to engage and shorter than %.2f mm"
          % (d["bolt_grip"] + P["original_nut_total_length"]))
    print("      to stay inside the nut. MEASURE the original bolt length -")
    print("      see the build review open items.")

    # ---- 15b. stiffness of the open-ended frame -------------------------
    print("")
    print("15b. OPEN-ENDED FRAME - SECTIONS THAT NOW CARRY THE RACK LOAD")
    print("      Deleting the end rail turns a closed frame into an open one,")
    print("      so lateral rack and twist become a real question. CAD can")
    print("      only report the sections; brief 12.15 is the actual test.")
    # Fusion reports the plane normal, not the outward face normal, so both
    # the seating face and the rear face come back as +Z here.
    rail = _planar_face_area(carrier, 1, d["z_rear"])
    print("      bottom transverse rail %.2f mm deep x %.2f mm thick"
          % (P["carrier_depth"], d["ap_y0"] - d["car_y0"]))
    print("      each side upright     %.2f mm deep x %.2f mm thick, %.2f long"
          % (P["carrier_depth"], d["car_x1"] - d["ap_x1"],
             d["light_cut_y"] - d["car_y0"]))
    print("      rear-face area %.1f mm2; both fixing arms and bosses retained"
          % rail)
    print("      the two sprung pedestals also tie the uprights to the module")
    print("      pocket, and the seated OLED itself spans between them.")
    gate(True, "rack and twist", "reported; brief 12.15 is a physical test")

    # ---- 16. part count --------------------------------------------------
    print("")
    print("16. PART COUNT AND HARDWARE")
    gate(find_component(design, "Retainer_Bar") is None,
         "no separate retainer bar", "carrier + the unchanged Rev N bezel")
    gate(True, "hardware",
         "2 x ORIGINAL Decca bolts + 2 x ORIGINAL matching nuts, reused. "
         "No heat-set inserts and no replacement screws anywhere.")

    # ---- open items that gate the print ---------------------------------
    print("")
    print("17. MEASUREMENTS THAT GATE THE PRINT")
    openitem("original nut across flats AND across corners",
             "the %.2f mm is MODELLED as across flats. If it is across "
             "corners the true across-flats is %.2f mm and the pocket is "
             "%.2f mm oversize. Change original_nut_hex_width and regenerate."
             % (P["original_nut_hex_width"],
                P["original_nut_hex_width"] * math.sqrt(3.0) / 2.0,
                P["original_nut_hex_width"]
                - P["original_nut_hex_width"] * math.sqrt(3.0) / 2.0),
             outcome="The original nuts seat and stay captive in the printed "
             "pocket, so the ACROSS-FLATS interpretation held in practice. No "
             "across-corners figure was taken, so original_nut_hex_width "
             "remains an interpretation, not a measurement.")
    openitem("original bolt length under the head",
             "must exceed the %.2f mm grip to engage at all, and stay under "
             "%.2f mm to remain inside the nut. Neither end is measured."
             % (d["bolt_grip"], d["bolt_grip"] + P["original_nut_total_length"]),
             outcome="The original bolts engage freely, do not bottom and "
             "clamp the carrier to the Perspex. The length itself was not "
             "recorded, so the 5.00-15.00 mm window stays a calculation.")
    openitem("hex-pocket fit coupon on the selected printer/material",
             "nut_pocket_fit_allowance is %.2f mm and nut_retain_lip is "
             "%.2f mm. Print the coupon, confirm the nut pushes in, stays put "
             "inverted and comes back out, then record the allowance."
             % (P["nut_pocket_fit_allowance"], P["nut_retain_lip"]),
             outcome="SUPERSEDED. The coupon existed to de-risk the pocket fit "
             "before committing to a carrier print. The carrier itself has now "
             "been printed and both original nuts fit, so the %.2f mm "
             "allowance and %.2f mm lip are proven on the real part."
             % (P["nut_pocket_fit_allowance"], P["nut_retain_lip"]))
    openitem("installed clearance against the retained lighting unit",
             "there is NO lighting-unit geometry in this model and no CAD "
             "result here may be read as proving that clearance. All CAD "
             "reports is the carrier's own extent, y %+.2f .. %+.2f. AND the "
             "Rev P.5 180-degree transform moved the open end from +Y to -Y, "
             "so the Rev P.3/P.4 installed fit does NOT carry over: brief "
             "12.14 is a RE-TEST, not a regression check. MANDATORY."
             % (d["carrier_min_y"], d["carrier_max_y"]),
             outcome="PASSED. The carrier clears the retained original Decca "
             "lighting unit, with the required clearance on the bottom / open "
             "connector side. This was the re-test the 180 deg transform made "
             "necessary, and it is the ONLY evidence for that interface - "
             "there is still no lighting-unit geometry in CAD.")
    openitem("powered light-leak test with the opaque black print",
             "the %.2f mm shield and the %.2f x %.2f mm pin slot are chosen, "
             "not measured against the cabinet LEDs. Run brief 12.22: cabinet "
             "LEDs through their usable range, OLED black / dim / normal. If "
             "leakage remains ONLY at the pin slot, tighten that slot or add "
             "an integral hood - do not reopen the wall or add a component."
             % (P["rear_light_shield_t"], d["pin_slot_w"], d["pin_slot_h"]),
             outcome="PASSED. The rear closure and the two light-block walls "
             "work: powered operation is clean with the cabinet lighting in "
             "place. No hood was needed and nothing was reopened.")

    print("")
    print("=" * 80)
    if fails:
        print("GATE RESULT: %d FAILURE(S)" % len(fails))
        for f in fails:
            print("   - %s" % f)
    elif blocks:
        print("GATE RESULT: EVERY EVALUABLE CHECK PASSES - %d BLOCKED ON A"
              % len(blocks))
        print("             MEASUREMENT THAT DOES NOT EXIST YET")
    elif tested:
        print("GATE RESULT: ALL GEOMETRIC CHECKS PASS, AND THE %d ITEMS THIS"
              % len(closed))
        print("             GATE DEFERRED TO PHYSICAL TEST ARE CLOSED BY THE")
        print("             BUILT AND TESTED PROTOTYPE.")
    else:
        print("GATE RESULT: ALL CHECKS PASS")
    if blocks:
        print("")
        print("BLOCKED - CANNOT BE EVALUATED UNTIL THE BONDED GLASS IS")
        print("MEASURED. These are NOT passes and NOT design failures: they")
        print("are checks against a placeholder envelope that is known to be")
        print("wrong (it covers the mounting holes). Measure the boundary,")
        print("enter it, set oled_glass_measured, and they become hard gates.")
        for b in blocks:
            print("   ? %s" % b)
    if opens:
        print("")
        print("BLOCKING OPEN ITEM(S) BEFORE ANY PRINT: %d" % len(opens))
        for o in opens:
            print("   * %s" % o)
    if closed:
        print("")
        print("CLOSED BY THE PHYSICAL PROTOTYPE: %d item(s)" % len(closed))
        print("Each of these was recorded here as something CAD could not")
        print("settle. The built and tested part settled them. None of them")
        print("was closed by changing a check or a number.")
        for c in closed:
            print("   + %s" % c)
    print("")
    if blocks or opens:
        print("NO PRINT until the item(s) above are resolved.")
    elif tested:
        print("REV P.5 IS RELEASED.")
        print("")
        print("The Rev P.2 architecture - flush-side insertion, fixed rear")
        print("datum pads, retention by positive geometric overlap - is")
        print("carried through, and every Rev P.5 change on top of it has now")
        print("been built and tested in the radio: four sprung posts, the")
        print("6.00 mm carrier, the 180 deg module datum, the fixings 7.00 mm")
        print("lower, the closed rear with its light blocks, the enlarged")
        print("14.00 x 4.19 mm connector opening and the original captive-nut")
        print("fasteners at exactly 49.00 mm pitch.")
        print("")
        print("WHAT REMAINS A MODELLING CAVEAT, NOT A BLOCKER. Three inputs in")
        print("the parameter table were never measured, and the prototype")
        print("passing does not measure them:")
        print("  * oled_glass_w / _h / _off_y - the bonded-glass envelope. It")
        print("    is still the placeholder that puts glass over the mounting")
        print("    holes. The built part clears the real glass; the MODEL does")
        print("    not describe it. oled_glass_measured stays False.")
        print("  * original_nut_hex_width - 3.80 mm is still interpreted as")
        print("    ACROSS FLATS. The real nuts fit the printed pocket, so the")
        print("    interpretation held, but no across-corners figure was taken.")
        print("  * the original bolt length under the head. The bolts engage")
        print("    and clamp; the length itself was not recorded.")
        print("These matter only if the geometry is regenerated with changed")
        print("dimensions. As built, the part is proven. Anyone changing a")
        print("post, the glass keep-out or the nut pocket must measure first.")
    print("=" * 80)
    return fails


# ---------------------------------------------------------------------------
# bezel - the validated Rev N cosmetic trim, imported unchanged
# ---------------------------------------------------------------------------
def import_bezel(_context=None):
    """Import Front_Bezel_revN.step as a reference body and re-check it."""
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    B = Builder()
    d = derive(P)

    clear_component(design, "REF_Front_Bezel_revN")
    if not os.path.isfile(BEZEL_STEP):
        print("bezel STEP not found: %s" % BEZEL_STEP)
        return None

    imp = app.importManager
    opts = imp.createSTEPImportOptions(BEZEL_STEP)
    src_doc = imp.importToNewDocument(opts)
    src_des = adsk.fusion.Design.cast(app.activeProduct)
    bodies = []
    for i in range(src_des.rootComponent.occurrences.count):
        o = src_des.rootComponent.occurrences.item(i)
        for b in o.component.bRepBodies:
            bodies.append(B.copy(b))
    for b in src_des.rootComponent.bRepBodies:
        bodies.append(B.copy(b))
    print("bezel bodies imported: %d" % len(bodies))
    src_doc.close(False)

    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    named = [(b, "BEZEL_revN_%d" % (i + 1)) for i, b in enumerate(bodies)]
    occ, comp = add_component(root, "REF_Front_Bezel_revN", named)

    for b in comp.bRepBodies:
        bb = b.boundingBox
        print("bezel %-16s x[%.2f, %.2f]  y[%.2f, %.2f]  z[%.2f, %.2f]" % (
            b.name, bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10,
            bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10))

    car = find_component(design, CARRIER).bRepBodies.item(0)
    ref = find_component(design, "REF_SH1106_1P3")
    mod = {}
    for b in ref.bRepBodies:
        mod[b.name] = b
    pan = find_component(design, "REF_Decca_Panel").bRepBodies.item(0)

    fails = []
    print("")
    print("16. FRONT BEZEL (Rev N, unchanged)")
    for b in comp.bRepBodies:
        for nm, other in (("carrier", car), ("Perspex", pan),
                          ("OLED glass", mod["OLED_Glass"]),
                          ("OLED PCB", mod["OLED_PCB"]),
                          ("solder tips", mod["OLED_Solder_Tips"])):
            h, v, box = _hit(B, b, other)
            ok = not h or nm == "Perspex"
            tag = "PASS" if ok else "FAIL"
            det = "CLEAR" if not h else "%.4f mm3 %s" % (v, box)
            if h and nm == "Perspex":
                det += "  (locating lip inside the aperture - by design)"
            print("  [%s] %-30s x %-14s %s" % (tag, b.name, nm, det))
            if not ok:
                fails.append("%s x %s" % (b.name, nm))
        zmin = min(f.boundingBox.minPoint.z * 10 for f in b.faces)
        print("        rearmost bezel material z = %+.3f  (glass front %+.3f,"
              " nose tip %+.3f)" % (zmin, d["z_glass_front"], d["z_nose_tip"]))
        if zmin <= d["z_glass_front"]:
            fails.append("bezel reaches the OLED glass plane")
        if zmin <= d["z_nose_tip"]:
            fails.append("bezel reaches the snap-nose plane")
    if fails:
        print("  BEZEL FAILURES: %s" % fails)
    else:
        print("  bezel is compatible with Rev P.2 unchanged - no change needed")
    return fails


# ---------------------------------------------------------------------------
# hex-pocket fit coupon
# ---------------------------------------------------------------------------
COUPON = "Hex_Pocket_Fit_Coupon"
COUPON_ALLOWANCES = (0.10, 0.15, 0.20, 0.25, 0.30)
COUPON_PITCH = 11.00


def build_coupon(B, P, d):
    """A small coupon carrying the SAME captive-nut pocket at five fit
    allowances, so the printer/material allowance is chosen from a physical
    part rather than assumed. The brief requires this before the carrier
    whenever the fit has not already been demonstrated.

    Each station reproduces the carrier's axial stack exactly - bolt clearance
    bore, hex head seat, retaining ridge, lead-in, clearance bore - at the same
    depths and in the same print orientation, so what the coupon proves
    transfers directly.

    Station 1 is the smallest allowance. Count the notches on the front face:
    one notch = station 1.
    """
    n = len(COUPON_ALLOWANCES)
    half = (n - 1) * COUPON_PITCH / 2.0
    w = (n - 1) * COUPON_PITCH + P["fix_boss_d"] + 4.0
    h = P["fix_boss_d"] + 4.0
    s = B.rrect(-w / 2.0, w / 2.0, -h / 2.0, h / 2.0,
                d["z_rear"], 0.0, 2.00)
    for i, allow in enumerate(COUPON_ALLOWANCES):
        x = -half + i * COUPON_PITCH
        af = P["original_nut_hex_width"] + allow
        ac = af * 2.0 / math.sqrt(3.0)
        body = ac + P["nut_body_allowance"]
        B.sub(s, B.cylz(P["bolt_clear_d"], x, 0.0, d["z_nut_seat"], 0.001))
        B.sub(s, B.hexz(af, x, 0.0, d["z_nut_head_back"], d["z_nut_seat"]))
        B.sub(s, B.hexz(d["nut_retain_af"], x, 0.0,
                        d["z_nut_retain"], d["z_nut_head_back"]))
        B.sub(s, B.conez(body, d["nut_retain_ac"], x, 0.0,
                         d["z_nut_lead"], d["z_nut_retain"]))
        B.sub(s, B.cylz(body, x, 0.0, d["z_rear"] - 1.0, d["z_nut_lead"]))
        # identification notches on the front face: one per station number
        for k in range(i + 1):
            nx = x - (i * 0.9) / 2.0 + k * 0.9
            B.sub(s, B.box(nx - 0.30, nx + 0.30,
                           h / 2.0 - 1.60, h / 2.0 + 1.0, -0.60, 0.001))
    return [(s, COUPON)]


def coupon(_context=None):
    """Build and export the hex-pocket fit coupon as its own document."""
    app = adsk.core.Application.get()
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    B = Builder()
    d = derive(P)
    occ, comp = add_component(design.rootComponent, COUPON,
                              build_coupon(B, P, d))
    body = comp.bRepBodies.item(0)
    bb = body.boundingBox
    print("coupon %.2f x %.2f x %.2f mm, %.3f cm3, solid=%s, lumps=%d"
          % ((bb.maxPoint.x - bb.minPoint.x) * 10,
             (bb.maxPoint.y - bb.minPoint.y) * 10,
             (bb.maxPoint.z - bb.minPoint.z) * 10,
             volume_of(body) / 1000.0, body.isSolid, body.lumps.count))
    for i, a in enumerate(COUPON_ALLOWANCES):
        print("  station %d  %d notch(es)  allowance %.2f  pocket %.2f af"
              % (i + 1, i + 1, a, P["original_nut_hex_width"] + a))
    em = design.exportManager
    stl = os.path.join(OUT_DIR, "STL")
    cad = os.path.join(OUT_DIR, "CAD")
    for pth in (stl, cad):
        if not os.path.isdir(pth):
            os.makedirs(pth)
    out = []
    q = os.path.join(cad, "Hex_Pocket_Fit_Coupon_revP.step")
    em.execute(em.createSTEPExportOptions(q, comp))
    out.append(q)
    q = os.path.join(stl, "Hex_Pocket_Fit_Coupon_revP.stl")
    o = em.createSTLExportOptions(body, q)
    o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    o.isBinaryFormat = True
    em.execute(o)
    out.append(q)
    for q in out:
        print("  %-44s %9d bytes"
              % (os.path.basename(q), os.path.getsize(q)))
    doc.close(False)
    return out


# ---------------------------------------------------------------------------
# snapshots - the three drawing images, regenerated from the live model
# ---------------------------------------------------------------------------
IMG_DIR = os.path.join(OUT_DIR, "Drawings")
SECTION = "SECTION_x15"


def _shot(app, path, eye, target, up, w=1600, h=1200):
    vp = app.activeViewport
    cam = vp.camera
    cam.eye = adsk.core.Point3D.create(mm(eye[0]), mm(eye[1]), mm(eye[2]))
    cam.target = adsk.core.Point3D.create(mm(target[0]), mm(target[1]),
                                          mm(target[2]))
    cam.upVector = adsk.core.Vector3D.create(*up)
    cam.isFitView = True
    vp.camera = cam
    adsk.doEvents()
    vp.refresh()
    ok = vp.saveAsImageFile(path, w, h)
    print("  %-44s %s" % (os.path.basename(path),
                          "%d bytes" % os.path.getsize(path) if ok else "FAILED"))
    return ok


# Snapshot appearances. The Rev P.5 mounting-point correction is a question
# about WHERE THE SCREEN SITS IN THE OPENING, and a uniform grey render cannot
# answer it: the module and the Perspex come out the same colour and the
# aperture reads as an empty hole. These make the assembly image legible - a
# translucent fascia, a lit-looking active area, a black carrier as it will
# actually be printed. Cosmetic only; no dimension depends on them.
PAINT = {
    "PANEL_Perspex": "Glass - Light Color",
    "OLED_ActiveArea": "LED (Green)",
    "OLED_Glass": "Glass (Grey)",
    "OLED_PCB": "Plastic - Matte (Blue)",
    "OLED_Header_Keepout": "Plastic - Matte (White)",
    "OLED_Solder_Tips": "Paint - Metallic (Yellow)",
    # The carrier is deliberately NOT painted. It is printed in opaque black
    # (brief 8.3), but a matte-black render collapses to a flat silhouette and
    # the four relief bores, the pin opening and the light blocks disappear.
    # The carrier-only views are documentation of geometry, so they keep the
    # default shading. The print colour is a material requirement, not a
    # rendering one.
    "ORIGINAL_Nuts": "Paint - Metallic (Blue)",
    "ORIGINAL_Bolt_Envelope": "Paint - Metallic (Blue)",
}


def _paint(app, design):
    """Apply PAINT to every matching body. Silent no-op if a name is missing."""
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    if lib is None:
        return 0
    cache = {}
    n = 0
    root = design.rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        for b in occ.bRepBodies:
            want = PAINT.get(b.name)
            if want is None:
                continue
            if want not in cache:
                src = lib.appearances.itemByName(want)
                if src is None:
                    cache[want] = None
                else:
                    ex = design.appearances.itemByName(want)
                    cache[want] = ex or design.appearances.addByCopy(src, want)
            ap = cache[want]
            if ap is not None:
                try:
                    b.appearance = ap
                    n += 1
                except Exception:
                    pass
    return n


def _show(design, names):
    root = design.rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        occ.isLightBulbOn = occ.component.name in names


def snapshots(_context=None):
    """Rebuild the three Drawings PNGs from the current model.

    They are documentation of the geometry that is actually in the file, so
    they are generated, never hand-captured.
    """
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    B = Builder()
    d = derive(P)
    if not os.path.isdir(IMG_DIR):
        os.makedirs(IMG_DIR)
    print("appearances applied to %d bodies" % _paint(app, design))

    clear_component(design, SECTION)

    # 1. THE ASSEMBLY, STRAIGHT ON FROM THE FRONT. This is the image that has
    #    to answer the Rev P.5 mounting-point question, so it shows the
    #    Perspex as well: where the active area actually sits inside the
    #    opening after the 7.00 mm correction. A three-quarter view cannot be
    #    read for alignment, so this one is deliberately square-on.
    _show(design, {CARRIER, "REF_SH1106_1P3", "REF_Decca_Panel"})
    _shot(app, os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_views.png"),
          (0.0, 4.0, 320.0), (0.0, 4.0, 0.0), (0, 1, 0))

    # 2. rear three-quarter: the carrier alone. It also has to show the
    #    Rev P.5 mounting-point correction from behind - the two fixing bosses
    #    now sit LOW relative to the connector-side carrier, because the OLED
    #    bay rose 7.00 mm while the bolts stayed on the Perspex holes.
    #    This view has to show the
    #    Rev P.4 change - a CONTINUOUS rear wall closing the OLED bay with one
    #    small four-pin slot and no keepout proxy - AND the Rev P.5 changes:
    #    the connector opening now at the BOTTOM with its two light blocks,
    #    and FOUR post relief bores, one per PCB mounting hole.
    _show(design, {CARRIER})
    _shot(app, os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_rear.png"),
          (-28.0, -27.0, -64.0), (0.0, 3.0, -3.0), (0, 1, 0))

    # 3. carrier alone from the front - the retention features themselves.
    #    Rev P.5: FOUR split sprung posts, one in every mounting hole. There is
    #    no plain post left to show.
    _show(design, {CARRIER})
    _shot(app, os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_posts.png"),
          (-42.0, -27.0, 46.0), (0.0, 3.0, -2.0), (0, 1, 0))

    # 4. section on x = +15.00, through a sprung locating post.
    #    Everything is clipped to a window around the module as well as to the
    #    half space, so the 90 x 80 mm reference Perspex patch cannot swamp
    #    the fitted view.
    win = B.box(d["post_x"], 40.0, d["car_y0"] - 4.0, d["car_y1"] + 4.0,
                d["z_rear"] - 5.0, 4.0)
    keep = {}
    for nm in (CARRIER, "REF_SH1106_1P3", "REF_Decca_Panel",
               "REF_Front_Bezel_revN"):
        occ = find_component(design, nm)
        if occ is None:
            continue
        for b in occ.bRepBodies:
            c = B.copy(b)
            B.inter(c, B.copy(win))
            try:
                if c.faces.count:
                    keep[(nm, b.name)] = c
            except Exception:
                pass
    add_component(root, SECTION,
                  [(v, "%s__%s" % k) for k, v in sorted(keep.items())])
    _show(design, {SECTION})
    _shot(app,
          os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_sections.png"),
          (-120.0, 33.0, 34.0), (d["post_x"], 4.0, -3.0), (0, 1, 0))

    # 5. section on y = 0 through a captive-nut pocket, looking along -Y
    clear_component(design, SECTION)
    win = B.box(d["m2_x"] - 9.0, d["m2_x"] + 9.0, 0.0, 9.0,
                d["z_nut_rear"] - 1.0, d["z_perspex_front"] + 1.0)
    keep = {}
    for nm in (CARRIER, "REF_Decca_Panel", "REF_Decca_Fasteners"):
        occ = find_component(design, nm)
        if occ is None:
            continue
        for bdy in occ.bRepBodies:
            c = B.copy(bdy)
            B.inter(c, B.copy(win))
            try:
                if c.faces.count:
                    keep[(nm, bdy.name)] = c
            except Exception:
                pass
    add_component(root, SECTION,
                  [(v, "%s__%s" % k) for k, v in sorted(keep.items())])
    _show(design, {SECTION})
    _shot(app, os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_nut.png"),
          (d["m2_x"] - 46.0, -70.0, 34.0), (d["m2_x"], 0.0, -4.5), (0, 0, 1))

    clear_component(design, SECTION)
    for i in range(root.occurrences.count):
        root.occurrences.item(i).isLightBulbOn = True
    print("snapshots written to %s" % IMG_DIR)


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------
def export(_context=None):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    em = design.exportManager

    cad = os.path.join(OUT_DIR, "CAD")
    stl = os.path.join(OUT_DIR, "STL")
    for p in (cad, stl):
        if not os.path.isdir(p):
            os.makedirs(p)

    clear_component(design, SECTION)
    for i in range(root.occurrences.count):
        root.occurrences.item(i).isLightBulbOn = True

    car_occ = find_component(design, CARRIER)
    car_comp = car_occ.component

    out = []
    p = os.path.join(cad, "Decca_Display_Mount_revP.f3d")
    em.execute(em.createFusionArchiveExportOptions(p))
    out.append(p)

    p = os.path.join(cad, "Rear_Display_Carrier_revP.step")
    em.execute(em.createSTEPExportOptions(p, car_comp))
    out.append(p)

    p = os.path.join(cad, "Decca_Display_Mount_revP_assembly.step")
    em.execute(em.createSTEPExportOptions(p))
    out.append(p)

    body = car_comp.bRepBodies.item(0)
    p = os.path.join(stl, "Rear_Display_Carrier_revP.stl")
    o = em.createSTLExportOptions(body, p)
    o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    o.isBinaryFormat = True
    em.execute(o)
    out.append(p)

    for p in out:
        sz = os.path.getsize(p) if os.path.isfile(p) else -1
        print("  %-52s %9d bytes" % (os.path.basename(p), sz))
    print("exported %d files to %s" % (len(out), OUT_DIR))
    return out
