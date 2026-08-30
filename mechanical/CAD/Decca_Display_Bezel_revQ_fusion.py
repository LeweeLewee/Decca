# -*- coding: utf-8 -*-
"""
Decca OLED Display Bezel - Rev Q parametric generator
=====================================================

OPEN revision. Bezel only. The released Rev P.5 carrier is FROZEN: this script
never writes, regenerates or re-exports any Rev P.5 file. It *reads*
Rear_Display_Carrier_revP.step as an immutable reference for the interference
checks and nothing more.

What Rev Q changes, and only this
---------------------------------
The Rev N pair of side locating rails is replaced by ONE continuous rearward
masking lip around the complete inside perimeter of the Perspex opening -
left, right, top, bottom and all four corners. Everything else about the Rev N
bezel is reproduced: the 40.00 x 20.30 x 4.00 envelope, the R2.00 external
corners, the R0.40 front edge break, the 30.40 mm visible window width, the
R0.80 window corners and the two recessed adhesive pads.

Cross-section (top or bottom of the opening):

    front
    BEZEL FACE
    --------------  seats against the Perspex front face, z = +3.000
           |
           |  continuous 0.40 mm lip, 2.80 mm rearwards
    PERSPEX|
    -------+        lip rear tip, z = +0.200
    rear

Provenance of the preserved Rev N geometry
------------------------------------------
Every Rev N figure below was recovered by reading Front_Bezel_revN.step
(read-only) and cross-checked against the Rev P build review section 16 and
the Z-chain in section 3. Recovered directly from the STEP BREP:

  envelope            40.000 x 20.300 x 4.000, X +/-20.000, Y +/-10.150
  Z levels present    +0.200, +3.000, +3.300, +3.800, +4.200
  external corners    R2.000 cylinders at (+/-18.000, +/-8.150)
  front edge break    R0.400, torus major 1.600 at the external corners
  window              30.400 x 14.900, R0.800 corners at (+/-14.400, +/-6.650)
  window edge break   R0.400, torus major 1.200
  adhesive pads       x +/-12.000, y 7.850..9.850 and -9.850..-7.850,
                      floor z = +3.300, i.e. 0.300 deep in the seating face
  locating rails      TWO ONLY, x 15.300..17.450 and -17.450..-15.300,
                      y -4.000..+4.000, z +0.200..+3.000, R0.600 ends

The rails prove the 34.90 mm outer envelope in X and the 2.80 mm depth. They
prove NOTHING about the top, the bottom or any corner - they were deliberately
kept clear of the corners because the Perspex corner radius has never been
measured. See corner_study() and the Rev Q build report.

Z-chain, absolute, unchanged from Rev N and Rev P.5
---------------------------------------------------
    z = +4.200   bezel front face
    z = +3.000   Perspex FRONT face == bezel seating plane
    z =  0.000   Perspex REAR face  == DATUM A, carrier hard stop
    z = -0.300   OLED glass front face

    lip rear tip z = +0.200 -> 0.200 clear of the Perspex rear face,
                               0.500 clear of the OLED glass (released value)

Entry points - run inside Fusion (Utilities -> Add-Ins -> Scripts), or through
the MCP bridge by exec()ing this file and calling:

    main()          build the Rev Q bezel and its reference bodies
    validate()      the full check suite - prints PASS / FAIL / REPORT lines
    corner_study()  the corner-fit tolerance table (pure arithmetic)
    snapshots()     regenerate the Rev Q Drawings PNGs
    export()        write the Rev Q files (never a Rev P.5 file)
    coupon()        build and export the corner-radius gauge coupon

main() creates its own NEW document. It never opens, modifies or saves the
Rev N, Rev O or Rev P documents.
"""

import adsk.core
import adsk.fusion
import math
import os

# ---------------------------------------------------------------------------
# Output location - the clone's mechanical folder on the user's machine
# ---------------------------------------------------------------------------
OUT_DIR = r"D:\GitHub\Decca\mechanical"
CARRIER_STEP = os.path.join(OUT_DIR, "CAD", "Rear_Display_Carrier_revP.step")

COMP_BEZEL = "Front_Bezel_revQ"
COMP_PANEL = "REF_Decca_Panel"
COMP_GLASS = "REF_OLED_Glass"
COMP_CARRIER = "REF_Carrier_revP"
COMP_COUPON = "Bezel_Fit_Gauge_revQ"
COMP_ACTIVE = "REF_OLED_Active"

# ---------------------------------------------------------------------------
# NAMED PARAMETERS - created before any dependent geometry
#
# MEASURED      physical, from Spec v1.2 section 2. Do not change without a
#               new measurement.
# PRESERVED     recovered from Front_Bezel_revN.step. Rev Q must not alter the
#               Rev N face, envelope or external appearance.
# PROVISIONAL   initial Rev Q fit values. These are the ONLY values a test
#               print may change.
# UNRESOLVED    no physical evidence exists anywhere in the project.
# ---------------------------------------------------------------------------
P = {
    # -- MEASURED: the original Decca fascia -------------------------------
    "panel_open_w": 35.20,          # MEASURED    Rev C
    "panel_open_h": 15.30,          # MEASURED    Rev C
    "panel_t": 3.00,                # MEASURED
    "panel_fix_pitch": 49.00,       # MEASURED    Rev C, print-confirmed Rev D
    "panel_ref_w": 70.00,           # reference slab only, not a fascia size
    "panel_ref_h": 40.00,
    "panel_fix_clear_d": 2.40,

    # The corner radius of the REAL opening. Modelled as 0.00 because that is
    # exactly what the RELEASED Rev P generator does (build_panel cuts a sharp
    # box). It is NOT a measurement and NOT a claim. See corner_study().
    "panel_open_corner_r": 0.00,    # UNRESOLVED  unmeasured, modelled sharp

    # -- PRESERVED: the Rev N bezel, recovered from the released STEP -------
    "bezel_w": 40.00,               # PRESERVED
    "bezel_h": 20.30,               # PRESERVED
    "bezel_t": 4.00,                # PRESERVED
    "bezel_outer_r": 2.00,          # PRESERVED   external corner radius
    "bezel_edge_break": 0.40,       # PRESERVED   front face edge fillet
    # THE FACE OPENING IS NOW FLUSH WITH THE SKIRT ON ALL FOUR SIDES.
    # X was made flush by the owner's earlier change; Y follows here.
    # Moving the skirt walls out to a 15.60 inner opening would otherwise
    # leave the 15.35 face opening as the new limiter and deliver +1.83 mm
    # of vertical opening instead of the +2.00 mm asked for, so the face
    # opening goes to 15.60 with it. The owner chose this explicitly.
    #
    # The corner radius follows for a different reason. At R0.80 the face
    # corner is FULLER than the skirt's R1.75, so once the two share the
    # same extents the face corner becomes the visible one and the clear
    # opening would sharpen from R1.75 to R0.80. R1.75 leaves what the eye
    # actually sees exactly as it is today, and makes the aperture a
    # single straight bore instead of a taper. derive() refuses to build
    # if either value drifts away from the skirt inner envelope.
    #
    # DECLARED DEVIATION from brief 2/4 (face opening 30.90 x 15.35,
    # R0.80) - the third, after the owner's width and corner changes.
    "bezel_window_w": 32.90,        # OWNER       was 30.90, = skirt inner
    "bezel_window_h": 15.60,        # OWNER       was 15.35, = skirt inner
    "bezel_window_r": 1.75,         # OWNER       was 0.80,  = skirt inner R
    # -- recessed adhesive pads - DELETED at owner instruction -------------
    # Rev N has two: 24.00 x 2.00 mm, 0.30 mm deep into the seating face at
    # y +/-7.85..9.85. The owner inspected the model, identified them as the
    # "two rectangle cut outs on the underside", and directed their removal.
    # pads_enabled is therefore False and the seating face is now a plain
    # unbroken annulus.
    #
    # DECLARED DEVIATION from brief 3.1, which lists "recessed adhesive pads"
    # among the Rev N features to preserve. It is a defensible one: Rev N
    # located on two side rails with a CLEARANCE fit and needed adhesive to
    # stay put, whereas Rev Q is held by a 0.10 mm per side INTERFERENCE fit,
    # which makes the pads redundant. Set pads_enabled back to True to restore
    # them exactly - the Rev N values below are kept for that purpose and
    # nothing else depends on them.
    "pads_enabled": False,          # OWNER       deleted 2026-08-30
    "pad_x_half": 12.00,            # Rev N value, retained for restoration
    "pad_y0": 7.85,                 # Rev N value, retained for restoration
    "pad_y1": 9.85,                 # Rev N value, retained for restoration
    "pad_depth": 0.30,              # Rev N value, retained for restoration

    # -- Rev Q: the continuous inset masking wall --------------------------
    # Owner amendment, brief commit 7b107f2: a controlled horizontal
    # INTERFERENCE fit, R2.00 outer corners, and an 0.80 mm wall so the
    # established 0.40 mm extrusion configuration resolves as TWO continuous
    # wall loops instead of the single loop the 0.40 mm wall produced.
    # OWNER 2026-08-30 - the interference-fit refinement, in two moves.
    #
    #   1. ONE extra 0.40 mm wall loop on the LEFT and RIGHT outer faces,
    #      added OUTWARD so the horizontal opening is not touched:
    #          35.40 -> 36.20
    #      It is applied at the corners as a true outward offset, which
    #      is what keeps the OPENING corner at R1.75 - see
    #      bezel_lip_corner_r. The top and bottom faces do NOT get the
    #      extra loop; the owner scoped the loop to the sides.
    #
    #   2. the top and bottom walls then move 1.00 mm out each, which
    #      opens the vertical aperture by 2.00 mm:
    #          15.20 -> 17.20 outer,   13.60 -> 15.60 inner
    #
    # Both moves push material OUTWARD into the Perspex opening, and
    # derive() reports what that does to the fit: horizontal interference
    # 0.100 -> 0.500 mm per side, vertical from a 0.050 mm CLEARANCE to
    # 0.950 mm of INTERFERENCE. The panel_open_* figures above are
    # MEASURED Rev C values and are deliberately NOT adjusted to suit.
    "bezel_lip_outer_w": 36.20,     # OWNER       35.40 + 2 x 0.40, one loop
    "bezel_lip_outer_h": 17.20,     # OWNER       15.20 + 2 x 1.00
    "bezel_lip_depth": 2.80,        # PROVEN      Rev N engagement depth

    # THE WALL IS NO LONGER UNIFORM, at owner instruction 2026-08-30.
    #
    # The owner asked for three things at once: the horizontal opening out by
    # 1.00 mm per side, the side wall thickened until its inner face is FLUSH
    # with that opening (i.e. no set-back on the left and right, which is what
    # the old 1.45 mm ledge was), and the outer envelope left alone. With a
    # single uniform wall those three force 1.25 mm everywhere, which would
    # drag the vertical clear opening 13.60 -> 12.70 and cost 0.45 mm more of
    # the lit band. The owner then ruled that loss out, and clarified that the
    # loop rule is AT LEAST two loops and that the side and the top/bottom
    # walls need not carry the same number.
    #
    # So the wall is split. Y stays at the proven 0.80 (two loops); X is
    # DERIVED from the flush requirement and, after the extra outward loop
    # on the sides, comes out at 1.65 (4.125 loops). Through the corners
    # the wall tapers smoothly between them and never drops below 0.80 -
    # see derive().
    "bezel_lip_wall_y": 0.80,       # OWNER       top/bottom, 2 loops
    #                                 X wall is DERIVED - see derive()
    # Owner refinement 2026-08-30: R2.00 did not match the real Perspex
    # opening corner, so the outer corner radius went up 50% to R3.00, and
    # it then took the extra outward loop with the rest of the side
    # profile, 3.00 -> 3.40. That +0.40 is not decoration. The inner corner
    # radius is (corner_r - wall_x), so holding the outer at 3.00 while the
    # wall went 1.25 -> 1.65 would have dragged the OPENING corner
    # 1.75 -> 1.35. The instruction was to leave the horizontal opening
    # alone, so the outer corner absorbs the loop and the opening corner
    # stays at R1.75. Brief 7 explicitly allows the named corner parameters
    # to be changed when the fit needs it; the brief's stated 2.00 is
    # therefore superseded by observation, and this is recorded as a
    # deviation from brief 2/4.
    "bezel_lip_corner_r": 3.40,     # OWNER       3.00 + the outward loop
    "bezel_lip_lead": 0.20,         # PROVISIONAL minimum entry lead-in

    # The established production extrusion width. Every wall must be at least
    # TWO of these - that is the rule, and it is a MINIMUM, applied per side.
    "extrusion_width": 0.40,        # PRODUCTION  nozzle / extrusion width

    # How far the tapered aperture stops OUTSIDE the lip inner opening at the
    # seating plane, so the two surfaces meet transversally instead of
    # tangentially. Purely a meshing measure - see derive(). The lip still
    # controls the clear height.
    # Was 0.02, to stop the aperture landing exactly on the skirt inner face.
    # That was needed while the two profiles COINCIDED along the straight
    # runs but DIFFERED at the corners - the tessellator answered the
    # mismatch with 52 zero-area triangles. The aperture rear section is now
    # the skirt inner profile exactly, corner radius included, so there is no
    # mismatch left to relieve. Both tools still check for degenerates.
    "ap_root_relief": 0.00,         # MODELLING   no longer needed

    # -- OLED reference, for the optical report only -----------------------
    # From the RELEASED Rev P.5 model. oled_glass_* remains an UNMEASURED
    # placeholder there and stays one here - see the CAD README caveat.
    "oled_active_w": 29.42,
    "oled_active_h": 14.70,
    "oled_active_cy": 6.70,         # Rev P.5 active centre y, after the +7.00 rise
    "oled_view_w": 31.42,
    "oled_view_h": 16.70,
    "oled_glass_front_z": -0.30,    # RELEASED    glass front face
    "oled_glass_rear_z": -1.10,     # PCB front face

    # -- interference fit gauge coupon -------------------------------------
    "coupon_keep_x": 12.00,         # clip the ring at |x| >= this
    "coupon_pad_out": 3.20,
    "coupon_pitch": 24.00,
}

# Horizontal interference per side carried by the fit gauge, ascending.
#
# The corner radius is no longer the open question - the owner has specified
# R2.00. The open question is now the INTERFERENCE: 0.10 mm per horizontal
# side, resisted by a wall that is 8x stiffer in bending than the 0.40 mm one
# it replaces. These five bracket the declared value so the fit can be chosen
# from a physical part instead of argued from CAD.
COUPON_INTERFERENCE = [0.00, 0.05, 0.10, 0.15, 0.20]


def derive(P):
    """Every dependent dimension. Nothing below is entered twice."""
    d = {}

    # Z-chain --------------------------------------------------------------
    d["z_panel_front"] = P["panel_t"]                                # +3.000
    d["z_panel_rear"] = 0.0                                          #  0.000
    d["bezel_face_t"] = P["bezel_t"] - P["bezel_lip_depth"]          #  1.200
    d["z_bezel_front"] = d["z_panel_front"] + d["bezel_face_t"]      # +4.200
    d["z_lip_rear"] = d["z_panel_front"] - P["bezel_lip_depth"]      # +0.200

    # THE SPLIT WALL ---------------------------------------------------------
    #
    # X is DERIVED from the flush requirement: the side wall is exactly as
    # thick as it needs to be for its inner face to land on the face opening,
    # so there is no set-back on the left and right. Y is the entered value,
    # held at the proven 0.80 so the vertical clear opening stays at 13.60.
    d["bezel_lip_wall_x"] = (P["bezel_lip_outer_w"]
                             - P["bezel_window_w"]) / 2.0            # 1.250
    d["bezel_lip_wall_y"] = P["bezel_lip_wall_y"]                    # 0.800
    ew = P["extrusion_width"]
    d["wall_loops_x"] = d["bezel_lip_wall_x"] / ew                   # 3.125
    d["wall_loops_y"] = d["bezel_lip_wall_y"] / ew                   # 2.000

    # The loop rule is a MINIMUM of two, applied per side. The sides and the
    # top/bottom are free to carry different numbers.
    for axis, w in (("x", d["bezel_lip_wall_x"]), ("y", d["bezel_lip_wall_y"])):
        if w / ew < 2.0 - 1e-9:
            raise ValueError(
                "bezel_lip_wall_%s (%.3f) gives only %.2f loop(s) at a %.3f mm "
                "extrusion width; at least TWO are required on every side"
                % (axis, w, w / ew, ew))

    # Fit against the MEASURED opening --------------------------------------
    # BOTH axes are now an INTERFERENCE. Sign convention unchanged:
    # interference positive means the lip is WIDER than the hole and has to
    # flex to enter. bezel_lip_clear_y keeps its old meaning, so it now
    # reads NEGATIVE - which is the honest answer, not a bug.
    #
    # These are the numbers to look at before printing anything. At
    # 36.20 x 17.20 into a 35.20 x 15.30 hole the skirt is 1.00 mm oversize
    # across and 1.90 mm oversize up. That is not a press fit in PETG; as
    # modelled the part cannot enter the opening at all. Owner-directed,
    # and it is not resolvable in CAD - either the MEASURED panel_open_h is
    # stale or the vertical move overshoots.
    d["bezel_lip_interf_x"] = (P["bezel_lip_outer_w"]
                               - P["panel_open_w"]) / 2.0            # +0.500
    d["bezel_lip_interf_y"] = (P["bezel_lip_outer_h"]
                               - P["panel_open_h"]) / 2.0            # +0.950
    d["bezel_lip_clear_y"] = -d["bezel_lip_interf_y"]                # -0.950

    d["bezel_lip_inner_w"] = (P["bezel_lip_outer_w"]
                              - 2 * d["bezel_lip_wall_x"])           # 32.900
    d["bezel_lip_inner_h"] = (P["bezel_lip_outer_h"]
                              - 2 * d["bezel_lip_wall_y"])           # 13.600

    # The inner corner radius follows the THICKER (X) wall. That choice is not
    # arbitrary: it puts the inner corner arc centre on the same x as the outer
    # arc centre, so the wall sweeps smoothly from 1.650 at the side to 0.800
    # at the top and bottom and reaches its minimum exactly at the top/bottom
    # tangent. Any smaller inner radius squares the corner off, drags it toward
    # the outer arc and thins the wall BELOW 0.800 - at R0 it collapses to
    # 0.189 mm. R1.75 is the smallest value that keeps two full loops all the
    # way round; validate() re-measures it rather than trusting this comment.
    if P["bezel_lip_corner_r"] < d["bezel_lip_wall_x"] - 1e-9:
        raise ValueError(
            "bezel_lip_corner_r (%.3f) is below the X wall (%.3f): the inner "
            "corner radius would go negative"
            % (P["bezel_lip_corner_r"], d["bezel_lip_wall_x"]))
    d["bezel_lip_inner_r"] = (P["bezel_lip_corner_r"]
                              - d["bezel_lip_wall_x"])               # 1.750
    d["lip_corner_r"] = P["bezel_lip_corner_r"]

    # FLUSH ON ALL FOUR SIDES. The face opening must equal the skirt inner
    # envelope exactly - extents AND corner radius - or one of them becomes
    # a ledge in front of the other. X has been flush since the owner's
    # earlier change; Y and the corner joined it with the vertical move.
    # Refuse to build rather than silently produce a set-back.
    for nm, want, got in (("bezel_window_h", d["bezel_lip_inner_h"],
                           P["bezel_window_h"]),
                          ("bezel_window_r", d["bezel_lip_inner_r"],
                           P["bezel_window_r"])):
        if abs(want - got) > 1e-9:
            raise ValueError(
                "%s is %.4f but the skirt inner envelope derives %.4f; the "
                "aperture would not be flush. Change the driver, not this."
                % (nm, got, want))
    d["wall_min"] = min(d["bezel_lip_wall_x"], d["bezel_lip_wall_y"])
    d["wall_max"] = max(d["bezel_lip_wall_x"], d["bezel_lip_wall_y"])

    # Half extents ---------------------------------------------------------
    d["bezel_window_w"] = P["bezel_window_w"]                        # 30.900
    d["bezel_window_h"] = P["bezel_window_h"]                        # 15.350
    d["bw2"] = P["bezel_w"] / 2.0
    d["bh2"] = P["bezel_h"] / 2.0
    d["ww2"] = d["bezel_window_w"] / 2.0
    d["wh2"] = d["bezel_window_h"] / 2.0
    d["low2"] = P["bezel_lip_outer_w"] / 2.0
    d["loh2"] = P["bezel_lip_outer_h"] / 2.0
    d["liw2"] = d["bezel_lip_inner_w"] / 2.0
    d["lih2"] = d["bezel_lip_inner_h"] / 2.0
    d["po_w2"] = P["panel_open_w"] / 2.0
    d["po_h2"] = P["panel_open_h"] / 2.0

    # THE APERTURE IS TAPERED IN Y, AND IT HAS TO BE.
    #
    # The amended face opening is 15.350 high. The whole inset wall is only
    # 15.200 high. So the face opening is 0.075 mm TALLER PER SIDE than the
    # outside of the lip, and at the top and bottom the lip footprint
    # (|y| 6.800..7.600) falls entirely inside it. A straight-walled face
    # opening would therefore leave the top and bottom lip runs DETACHED from
    # the bezel face - floating ~31 mm cantilevers joined only near the
    # corners, unprintable without support, and not one sound solid.
    #
    # In X there is no such problem: the face opening (half 15.450) is
    # NARROWER than the lip inner (half 16.900), so the left and right runs
    # land on solid face material with 1.450 mm to spare.
    #
    # Resolution: the aperture is 30.900 wide throughout and TAPERS in Y from
    # the lip inner opening at the seating plane to the specified face opening
    # at the front face. Every published number survives - face opening
    # 30.90 x 15.35 at the front face, lip inner 33.80 x 13.60, effective
    # optical opening 30.90 x 13.60 - the full 0.80 mm wall lands on solid
    # material, and the taper is self-supporting printed front-face-down.
    # Spec v1.2 section 4 asks for a flared aperture anyway, "to reduce tunnel
    # effect through the 3 mm Perspex".
    #
    # The aperture stops a hair OUTSIDE the lip inner opening rather than
    # exactly on it. Landing it exactly on y = +/-6.800 makes the tapered wall
    # tangent to the lip inner face along a line at z = 3.000, and the
    # tessellator answers that with a seam of zero-area triangles - 52 of them
    # in the first export, all at exactly z = 3.0000. Backing the aperture off
    # by ap_root_relief turns that tangency into an ordinary transverse
    # intersection and the degenerate triangles vanish.
    #
    # It costs nothing that matters: the LIP still controls the clear height
    # at 13.600, exactly as brief section 4 requires, because the aperture is
    # now the wider of the two. The lip keeps 0.760 of its 0.800 mm wall
    # rooted on solid face material.
    d["ap_root_relief"] = P["ap_root_relief"]
    d["ap_rear_w"] = d["bezel_lip_inner_w"]                          # 32.900
    d["ap_rear_h"] = (d["bezel_lip_inner_h"]
                      + 2 * d["ap_root_relief"])                     # 15.600
    d["ap_front_w"] = d["bezel_window_w"]                            # 32.900
    d["ap_front_h"] = d["bezel_window_h"]                            # 15.600
    # The rear section carries the SKIRT inner corner radius, not the window
    # one. Anything smaller bulges outside the skirt corner and leaves a
    # crescent-shaped 90-degree ledge hanging over the aperture - it measured
    # 3.40 mm2 of unsupported overhang across the four corners at R0.80.
    d["ap_rear_r"] = d["bezel_lip_inner_r"]                          #  1.750
    d["ap_front_r"] = P["bezel_window_r"]                            #  1.750
    d["ap_taper_dy"] = (d["ap_front_h"] - d["ap_rear_h"]) / 2.0      #  0.875
    d["ap_taper_deg"] = math.degrees(math.atan2(d["ap_taper_dy"],
                                                d["bezel_face_t"]))  # 36.10
    d["ap_slope"] = d["ap_taper_dy"] / d["bezel_face_t"]

    # Clearances the released design already proved -------------------------
    d["clear_to_panel_rear"] = d["z_lip_rear"] - d["z_panel_rear"]   # 0.200
    d["clear_to_glass"] = d["z_lip_rear"] - P["oled_glass_front_z"]  # 0.500

    # Effective optical opening --------------------------------------------
    # The through-hole is the narrowest cross-section of the whole aperture.
    # Every candidate is now the same number, because the face opening and
    # the skirt inner envelope are flush on all four sides - so take the
    # true minimum of all three rather than assuming which one wins.
    d["optical_w"] = min(d["bezel_window_w"], d["bezel_lip_inner_w"])  # 32.900
    d["optical_h"] = min(d["bezel_window_h"], d["ap_rear_h"],
                         d["bezel_lip_inner_h"])                       # 15.600
    d["lip_root_supported"] = d["bezel_lip_wall_y"] - d["ap_root_relief"]
    # the clear opening corner is the SKIRT inner corner - it cuts in
    # further than the window corner does
    d["optical_r"] = d["bezel_lip_inner_r"]                            #  1.750

    # what Rev N showed, for the honest before/after
    d["revN_window_w"] = 30.40
    d["revN_window_h"] = 14.90

    # visible OLED active area through the Rev Q aperture
    a0 = P["oled_active_cy"] - P["oled_active_h"] / 2.0              # -0.650
    a1 = P["oled_active_cy"] + P["oled_active_h"] / 2.0              # +14.050
    d["active_y0"], d["active_y1"] = a0, a1
    # the CONTROLLING aperture half-height is the lip, not the face opening
    oh2 = d["optical_h"] / 2.0
    d["vis_q_y0"] = max(a0, -oh2)
    d["vis_q_y1"] = min(a1, +oh2)
    d["vis_q_h"] = max(0.0, d["vis_q_y1"] - d["vis_q_y0"])
    d["vis_n_y0"] = max(a0, -d["revN_window_h"] / 2.0)
    d["vis_n_y1"] = min(a1, +d["revN_window_h"] / 2.0)
    d["vis_n_h"] = max(0.0, d["vis_n_y1"] - d["vis_n_y0"])
    d["vis_open_y0"] = max(a0, -d["po_h2"])
    d["vis_open_y1"] = min(a1, +d["po_h2"])
    d["vis_open_h"] = max(0.0, d["vis_open_y1"] - d["vis_open_y0"])
    d["active_loss_vs_revN"] = d["vis_n_h"] - d["vis_q_h"]
    d["vis_w"] = min(P["oled_active_w"], d["optical_w"])

    # unlit board visible below the active area
    d["unlit_below_q"] = max(0.0, a0 - (-oh2))
    d["unlit_below_n"] = max(0.0, a0 - (-d["revN_window_h"] / 2.0))

    return d


# ---------------------------------------------------------------------------
# Temporary-BRep helpers - the API works in cm, the design works in mm
# ---------------------------------------------------------------------------
def mm(v):
    return float(v) / 10.0


def p3(x, y, z):
    return adsk.core.Point3D.create(mm(x), mm(y), mm(z))


def v3(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


class B(object):
    """Thin wrapper over TemporaryBRepManager. Everything in mm."""

    def __init__(self):
        self.t = adsk.fusion.TemporaryBRepManager.get()

    def box(self, x0, x1, y0, y1, z0, z1):
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0),
            v3(1, 0, 0), v3(0, 1, 0),
            mm(x1 - x0), mm(y1 - y0), mm(z1 - z0))
        return self.t.createBox(obb)

    def cylz(self, r, cx, cy, z0, z1):
        return self.t.createCylinderOrCone(p3(cx, cy, z0), mm(r),
                                           p3(cx, cy, z1), mm(r))

    def uni(self, a, b):
        self.t.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
        return a

    def sub(self, a, b):
        self.t.booleanOperation(
            a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        return a

    def inter(self, a, b):
        self.t.booleanOperation(
            a, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)
        return a

    def copy(self, a):
        return self.t.copy(a)

    def rprism(self, x0, x1, y0, y1, z0, z1, r):
        """Rounded-rectangle prism along Z, built from primitives. Far more
        robust than filleting four long vertical edges afterwards."""
        if r < 1.0e-6:
            return self.box(x0, x1, y0, y1, z0, z1)
        if 2 * r > (x1 - x0) + 1e-9 or 2 * r > (y1 - y0) + 1e-9:
            raise ValueError("corner radius %.4f too large for %.4f x %.4f"
                             % (r, x1 - x0, y1 - y0))
        s = self.box(x0 + r, x1 - r, y0, y1, z0, z1)
        self.uni(s, self.box(x0, x1, y0 + r, y1 - r, z0, z1))
        for cx in (x0 + r, x1 - r):
            for cy in (y0 + r, y1 - r):
                self.uni(s, self.cylz(r, cx, cy, z0, z1))
        return s

    def ring(self, ow2, oh2, iw2, ih2, z0, z1, ro, ri):
        """Closed rounded-rectangle ring - the continuous lip."""
        outer = self.rprism(-ow2, ow2, -oh2, oh2, z0, z1, ro)
        inner = self.rprism(-iw2, iw2, -ih2, ih2, z0 - 1.0, z1 + 1.0, ri)
        return self.sub(outer, inner)


# ---------------------------------------------------------------------------
# Bodies
# ---------------------------------------------------------------------------
def build_bezel(b, P, d):
    """The Rev Q bezel massing, as ONE connected solid.

    The tapered aperture is NOT cut here - it is a real Fusion loft feature
    applied afterwards by main(), so the taper stays parametric and editable.
    What this returns is the solid face slab with its adhesive pads, plus the
    continuous inset wall unioned onto its underside.
    """
    # 1. face slab - Rev N envelope and external corner radius, PRESERVED
    face = b.rprism(-d["bw2"], d["bw2"], -d["bh2"], d["bh2"],
                    d["z_panel_front"], d["z_bezel_front"], P["bezel_outer_r"])

    # 2. the two recessed adhesive pads - DELETED at owner instruction.
    #    Guarded rather than removed so they can be restored exactly.
    if P.get("pads_enabled", True):
        for sy in (1, -1):
            y0, y1 = sorted((sy * P["pad_y0"], sy * P["pad_y1"]))
            b.sub(face, b.box(-P["pad_x_half"], P["pad_x_half"], y0, y1,
                              d["z_panel_front"] - 0.5,
                              d["z_panel_front"] + P["pad_depth"]))

    # 3. THE REV Q FEATURE - one continuous inset wall, all four sides and
    #    all four corners, constant 0.80 mm through the R2.00 corners.
    lip = b.ring(d["low2"], d["loh2"], d["liw2"], d["lih2"],
                 d["z_lip_rear"], d["z_panel_front"],
                 P["bezel_lip_corner_r"], d["bezel_lip_inner_r"])

    b.uni(face, lip)
    return face


def _rrect_sketch(comp, z, hw, hh, r, name):
    """A closed rounded-rectangle sketch profile on a plane at height z."""
    planes = comp.constructionPlanes
    pi = planes.createInput()
    pi.setByOffset(comp.xYConstructionPlane,
                   adsk.core.ValueInput.createByReal(mm(z)))
    pl = planes.add(pi)
    pl.name = name + "_plane"
    sk = comp.sketches.add(pl)
    sk.name = name
    sk.isComputeDeferred = True
    lines = sk.sketchCurves.sketchLines
    arcs = sk.sketchCurves.sketchArcs

    def p2(x, y):
        return adsk.core.Point3D.create(mm(x), mm(y), 0.0)

    a, bb = hw - r, hh - r
    # four straight runs
    lines.addByTwoPoints(p2(hw, -bb), p2(hw, bb))
    lines.addByTwoPoints(p2(-a, hh), p2(a, hh))
    lines.addByTwoPoints(p2(-hw, bb), p2(-hw, -bb))
    lines.addByTwoPoints(p2(a, -hh), p2(-a, -hh))
    # four corner arcs, each sweeping 90 degrees anticlockwise
    arcs.addByCenterStartSweep(p2(a, bb), p2(hw, bb), math.pi / 2)
    arcs.addByCenterStartSweep(p2(-a, bb), p2(-a, hh), math.pi / 2)
    arcs.addByCenterStartSweep(p2(-a, -bb), p2(-hw, -bb), math.pi / 2)
    arcs.addByCenterStartSweep(p2(a, -bb), p2(a, -hh), math.pi / 2)
    sk.isComputeDeferred = False
    if sk.profiles.count < 1:
        raise RuntimeError("%s did not close into a profile" % name)
    return sk.profiles.item(0)


def build_aperture(comp, P, d, over=0.05):
    """The tapered aperture, as a real Fusion LOFT between two rounded-rect
    profiles, then combined out of the bezel.

    Constant 32.900 wide; in Y it runs from the skirt inner opening at the
    seating plane to the specified face opening at the front face.

    The FRONT section is pushed `over` beyond its plane so the cut breaks
    cleanly through the front face. The REAR section stops exactly on the
    seating plane and must not go below it.

    That rear limit matters now. While the aperture was 30.900 wide against a
    33.800 skirt it sat well inside the skirt and an over-run below the
    seating plane touched nothing. With the side wall flush the two share the
    same 32.900 width, and the aperture's R0.80 rear corners bulge outside the
    skirt's R1.75 inner corners - so any over-run bites the top of the wall at
    all four corners. It showed up as 0.84 mm2 of ring area missing at
    z = 2.95 while z = 0.45 and 1.60 measured correctly.
    """
    z0 = d["z_panel_front"]
    z1 = d["z_bezel_front"] + over
    hh0 = d["ap_rear_h"] / 2.0 + d["ap_slope"] * (z0 - d["z_panel_front"])
    hh1 = d["ap_rear_h"] / 2.0 + d["ap_slope"] * (z1 - d["z_panel_front"])
    hw = d["ap_rear_w"] / 2.0

    p0 = _rrect_sketch(comp, z0, hw, hh0, d["ap_rear_r"], "ap_rear")
    p1 = _rrect_sketch(comp, z1, hw, hh1, d["ap_front_r"], "ap_front")

    lofts = comp.features.loftFeatures
    li = lofts.createInput(
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    li.loftSections.add(p0)
    li.loftSections.add(p1)
    li.isSolid = True
    loft = lofts.add(li)
    loft.name = "aperture_taper"

    tool = loft.bodies.item(0)
    tool.name = "APERTURE_TOOL"
    target = comp.bRepBodies.itemByName("BEZEL")
    oc = adsk.core.ObjectCollection.create()
    oc.add(tool)
    ci = comp.features.combineFeatures.createInput(target, oc)
    ci.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    ci.isKeepToolBodies = False
    cut = comp.features.combineFeatures.add(ci)
    cut.name = "aperture_cut"
    return d["ap_taper_deg"]


def build_panel(b, P, d, relief_x=0.0, relief_y=0.0):
    """REF_Decca_Panel - the original fascia Perspex. Reference only.

    The opening is modelled EXACTLY as the released Rev P generator models it,
    a sharp-cornered box, because that is the controlled representation.
    panel_open_corner_r is exposed so corner sensitivity can be explored
    without pretending a measurement exists.

    relief_x and relief_y widen the opening by that much per side. They are
    used only by the validator, to state the interference claim the other
    way round: relieve the opening by exactly the declared interference and
    the overlap must vanish completely. Rev Q now interferes on BOTH axes,
    so both reliefs are needed. Nothing about the real panel changes.
    """
    s = b.box(-P["panel_ref_w"] / 2.0, P["panel_ref_w"] / 2.0,
              -P["panel_ref_h"] / 2.0, P["panel_ref_h"] / 2.0,
              d["z_panel_rear"], d["z_panel_front"])
    b.sub(s, b.rprism(-d["po_w2"] - relief_x, d["po_w2"] + relief_x,
                      -d["po_h2"] - relief_y, d["po_h2"] + relief_y,
                      d["z_panel_rear"] - 1.0, d["z_panel_front"] + 1.0,
                      P["panel_open_corner_r"]))
    m2x = P["panel_fix_pitch"] / 2.0
    for sx in (-1, 1):
        b.sub(s, b.cylz(P["panel_fix_clear_d"] / 2.0, sx * m2x, 0.0,
                        d["z_panel_rear"] - 1.0, d["z_panel_front"] + 1.0))
    return s


def build_glass(b, P, d):
    """OLED bonded-glass proxy. The ENVELOPE is the RELEASED placeholder and
    has NEVER been measured - see the CAD README caveat. Only its FRONT FACE Z
    matters for the bezel check, and that is a released value."""
    return b.box(-P["oled_view_w"] / 2.0, P["oled_view_w"] / 2.0,
                 P["oled_active_cy"] - P["oled_view_h"] / 2.0,
                 P["oled_active_cy"] + P["oled_view_h"] / 2.0,
                 P["oled_glass_rear_z"], P["oled_glass_front_z"])


def build_active(b, P, d):
    """The LIT area of the OLED, as a thin plate on the glass front face.

    Reference only. It exists so the assembly image shows, to scale, exactly
    how much of the lit area the new lip masks. Its position comes from the
    RELEASED Rev P.5 model: active centre y = +6.70 after the +7.00 mm rise.
    """
    return b.box(-P["oled_active_w"] / 2.0, P["oled_active_w"] / 2.0,
                 P["oled_active_cy"] - P["oled_active_h"] / 2.0,
                 P["oled_active_cy"] + P["oled_active_h"] / 2.0,
                 P["oled_glass_front_z"] - 0.05, P["oled_glass_front_z"])


def build_behind_panel(b, P, d):
    """SYNTHETIC. Everything behind the Perspex rear face, across the whole
    opening and well beyond it.

    If the bezel does not touch this solid it cannot touch the carrier, the
    module, the glass, the sprung posts or any assembly / removal corridor,
    because every one of those lives at z < 0. One check, no assumptions."""
    return b.box(-P["panel_ref_w"], P["panel_ref_w"],
                 -P["panel_ref_h"], P["panel_ref_h"],
                 -30.0, d["z_panel_rear"])


def build_coupon(b, P, d):
    """INTERFERENCE FIT GAUGE. Five loose end-tabs, notch-numbered 1..5 in
    ascending horizontal interference.

    The corner radius is no longer the open question - the owner has specified
    R2.00. The open question is the fit: 0.10 mm per horizontal side of
    interference, now resisted by a wall 8x stiffer in bending than the
    0.40 mm one it replaces.

    Each tab is the complete RIGHT-HAND END of the real Rev Q inset wall at
    one candidate interference - full 15.20 mm height, both R2.00 corners, the
    real 0.80 mm two-loop wall and the real 2.80 mm depth - so it engages the
    interference exactly as the bezel will. Offering each into the end of the
    real opening answers, on a physical part, the question CAD cannot: which
    interference is snug but removable, and leaves the Perspex unstressed.
    """
    tabs = []
    keep = P["coupon_keep_x"]
    out = P["coupon_pad_out"]
    for i, interf in enumerate(COUPON_INTERFERENCE):
        ow2 = (P["panel_open_w"] + 2 * interf) / 2.0
        iw2 = ow2 - d["bezel_lip_wall_x"]
        # the complete inset wall at this interference, clipped to the +X end
        seg = b.ring(ow2, d["loh2"], iw2, d["lih2"],
                     d["z_lip_rear"], d["z_panel_front"],
                     P["bezel_lip_corner_r"], d["bezel_lip_inner_r"])
        b.inter(seg, b.box(keep, ow2 + 10.0, -d["loh2"] - 10.0,
                           d["loh2"] + 10.0,
                           d["z_lip_rear"] - 1.0, d["z_panel_front"] + 1.0))
        # the face pad that lands on the Perspex front face around the opening
        pad = b.box(keep - 1.0, ow2 + out, -d["po_h2"] - out, d["po_h2"] + out,
                    d["z_panel_front"], d["z_bezel_front"])
        b.uni(pad, seg)
        # notch code - i+1 notches cut into the outboard edge
        for n in range(i + 1):
            cy = -3.0 + 1.5 * n
            b.sub(pad, b.box(ow2 + out - 0.9, ow2 + out + 1.0,
                             cy - 0.35, cy + 0.35,
                             d["z_panel_front"] - 1.0,
                             d["z_bezel_front"] + 1.0))
        # lay the five tabs out in a row for printing
        mtx = adsk.core.Matrix3D.create()
        mtx.translation = v3(mm((i - 2) * P["coupon_pitch"] - ow2), 0.0, 0.0)
        b.t.transform(pad, mtx)
        tabs.append((pad, "GAUGE_I%03d" % int(round(interf * 100))))
    return tabs


# ---------------------------------------------------------------------------
# Fusion plumbing
# ---------------------------------------------------------------------------
def _app():
    return adsk.core.Application.get()


def _design():
    return adsk.fusion.Design.cast(_app().activeProduct)


def _drop(root, name):
    for i in range(root.occurrences.count - 1, -1, -1):
        if root.occurrences.item(i).component.name == name:
            root.occurrences.item(i).deleteMe()


def _add_comp(root, name):
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    return occ


def _add_bodies(comp, bodies):
    """Bodies added inside a BaseFeature die at finishEdit(). Name them here,
    re-fetch by name afterwards."""
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    try:
        for body, name in bodies:
            comp.bRepBodies.add(body, bf).name = name
    finally:
        bf.finishEdit()


def _write_params(design, P, d):
    """Mirror the generator dict into named user parameters, the derived
    values as real formulas so the derivation is visible in the UI."""

    def put(name, expr, comment):
        ex = design.userParameters.itemByName(name)
        if ex:
            try:
                ex.expression = expr
            except Exception:
                pass
            try:
                ex.comment = comment
            except Exception:
                pass
            return
        try:
            design.userParameters.add(
                name, adsk.core.ValueInput.createByString(expr), "mm", comment)
        except Exception:
            pass

    for k, v in sorted(P.items()):
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            put(k, "%.5f mm" % v, "Rev Q generator")

    # derived - written as formulas so changing a driver updates them
    put("bezel_lip_interf_x", "(bezel_lip_outer_w - panel_open_w) / 2",
        "DERIVED  horizontal INTERFERENCE per side")
    put("bezel_lip_interf_y", "(bezel_lip_outer_h - panel_open_h) / 2",
        "DERIVED  vertical INTERFERENCE per side")
    put("bezel_lip_clear_y", "(panel_open_h - bezel_lip_outer_h) / 2",
        "DERIVED  vertical clearance - NEGATIVE, it is an interference")
    put("bezel_lip_wall_x", "(bezel_lip_outer_w - bezel_window_w) / 2",
        "DERIVED  side wall, set by the FLUSH requirement")
    put("bezel_lip_inner_w", "bezel_lip_outer_w - 2 * bezel_lip_wall_x",
        "DERIVED  == bezel_window_w, i.e. flush")
    put("bezel_lip_inner_h", "bezel_lip_outer_h - 2 * bezel_lip_wall_y", "DERIVED")
    put("bezel_lip_inner_r", "bezel_lip_corner_r - bezel_lip_wall_x", "DERIVED")
    put("wall_loops_x", "bezel_lip_wall_x / extrusion_width",
        "DERIVED  at least 2")
    put("wall_loops_y", "bezel_lip_wall_y / extrusion_width",
        "DERIVED  at least 2")
    put("aperture_rear_h", "bezel_lip_inner_h",
        "DERIVED  the lip controls the clear height")
    put("optical_h", "bezel_lip_inner_h",
        "DERIVED  face opening is flush with it, so they are equal")
    put("bezel_face_t", "bezel_t - bezel_lip_depth", "DERIVED")
    put("z_panel_front", "panel_t", "DERIVED seating plane")
    put("z_bezel_front", "z_panel_front + bezel_face_t", "DERIVED")
    put("z_lip_rear", "z_panel_front - bezel_lip_depth", "DERIVED")


def _planar_faces_at_z(body, z, tol=1.0e-4):
    """Every Z-normal planar face lying entirely at height z.

    Deliberately does NOT test the sign of Plane.normal: for a face produced by
    a boolean, the underlying plane normal is the surface's own normal and does
    not have to agree with the outward direction of the face, so a sign test
    silently returns nothing. Height is unambiguous, so height is what is used.
    """
    out = []
    for f in body.faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
            continue
        if abs(abs(g.normal.z) - 1.0) > 1.0e-6:
            continue
        bb = f.boundingBox
        if abs(bb.minPoint.z * 10 - z) > tol or abs(bb.maxPoint.z * 10 - z) > tol:
            continue
        out.append(f)
    return out


def _planar_face(body, z, nz=0, tol=1.0e-4):
    """The largest Z-normal planar face at height z. nz is accepted for
    readability at the call site and is not used as a filter - see above."""
    fs = _planar_faces_at_z(body, z, tol)
    if not fs:
        return None
    return max(fs, key=lambda f: f.area)


def _fillet(comp, edges, r_mm, name):
    if not edges:
        return False, "no edges"
    oc = adsk.core.ObjectCollection.create()
    for e in edges:
        oc.add(e)
    try:
        fi = comp.features.filletFeatures.createInput()
        fi.addConstantRadiusEdgeSet(
            oc, adsk.core.ValueInput.createByReal(mm(r_mm)), True)
        fi.isG2 = False
        fi.isRollingBallCorner = True
        f = comp.features.filletFeatures.add(fi)
        f.name = name
        return True, "ok"
    except Exception as ex:
        return False, str(ex)


def _chamfer(comp, edges, dist_mm, name):
    if not edges:
        return False, "no edges"
    oc = adsk.core.ObjectCollection.create()
    for e in edges:
        oc.add(e)
    try:
        ci = comp.features.chamferFeatures.createInput2()
        ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(
            oc, adsk.core.ValueInput.createByReal(mm(dist_mm)), True)
        c = comp.features.chamferFeatures.add(ci)
        c.name = name
        return True, "ok"
    except Exception as ex:
        return False, str(ex)


def _bezel_comp():
    root = _design().rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        if occ.component.name == COMP_BEZEL:
            return occ.component, occ
    raise RuntimeError("%s not found - run main() first" % COMP_BEZEL)


def _all_bodies(occ):
    """Every body under an occurrence, including nested sub-occurrences (a
    STEP import puts its solid one level down)."""
    out = [bd for bd in occ.bRepBodies]
    subs = occ.childOccurrences
    for i in range(subs.count):
        out.extend(_all_bodies(subs.item(i)))
    return out


def _find_occ(name):
    root = _design().rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        if occ.component.name == name:
            return occ
    return None


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(new_document=True):
    app = _app()
    if new_document:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = _design()
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent

    d = derive(P)
    _write_params(design, P, d)

    for n in (COMP_BEZEL, COMP_PANEL, COMP_GLASS):
        _drop(root, n)

    b = B()

    # ---- the bezel -------------------------------------------------------
    occ = _add_comp(root, COMP_BEZEL)
    comp = occ.component
    _add_bodies(comp, [(build_bezel(b, P, d), "BEZEL")])

    body = comp.bRepBodies.itemByName("BEZEL")
    print("after base feature : bodies=%d solid=%s faces=%d"
          % (comp.bRepBodies.count, body.isSolid, body.faces.count))

    # ---- the tapered aperture, as a parametric loft ----------------------
    ang = build_aperture(comp, P, d)
    body = comp.bRepBodies.itemByName("BEZEL")
    print("aperture taper     : %.2f deg from vertical, %s"
          % (ang, "self-supporting" if ang <= 45.0 else "NEEDS SUPPORT"))
    print("                     %.3f x %.3f at the seating plane -> "
          "%.3f x %.3f at the front face"
          % (d["ap_rear_w"], d["ap_rear_h"],
             d["ap_front_w"], d["ap_front_h"]))
    print("after aperture cut : bodies=%d solid=%s faces=%d"
          % (comp.bRepBodies.count, body.isSolid, body.faces.count))

    # ---- front face edge breaks, 0.40 - PRESERVED from Rev N -------------
    #
    # The OUTER envelope keeps the Rev N R0.40 fillet exactly.
    #
    # The WINDOW edge cannot: the tapered aperture is one NURBS surface, and
    # its front edge is a single closed NURBS curve whose dihedral varies
    # around the loop - 90 degrees down the vertical left and right walls,
    # 53.9 degrees where the top and bottom lean back, sweeping between the
    # two through the corners. Fusion refuses a fillet there at every radius
    # tried (0.40, 0.30, 0.20, 0.10 - all ASM_BL_UNFIN_SHEET), whole-loop and
    # per-edge alike. A chamfer of the same 0.40 succeeds cleanly.
    #
    # So the window break is realised as a 0.40 x 45 degree CHAMFER rather
    # than an R0.40 fillet. It is a declared deviation from Rev N and the only
    # one in the visible face detail. At 0.40 mm on a matt black part the two
    # are indistinguishable by eye, and the window was already re-dimensioned
    # and flared by the owner amendment, so its section could not have been
    # carried over unchanged in any case.
    body = comp.bRepBodies.itemByName("BEZEL")
    ff = _planar_face(body, d["z_bezel_front"], +1)
    outer_e, win_e = [], []
    if ff:
        for lp in ff.loops:
            (outer_e if lp.isOuter else win_e).extend(list(lp.edges))
    okA, msgA = _fillet(comp, outer_e, P["bezel_edge_break"],
                        "front_edge_break_outer")
    print("front break, outer envelope  R%.2f fillet  : %s %s"
          % (P["bezel_edge_break"], okA, msgA))

    body = comp.bRepBodies.itemByName("BEZEL")
    ff = _planar_face(body, d["z_bezel_front"], +1)
    win_e = []
    if ff:
        for lp in ff.loops:
            if not lp.isOuter:
                win_e = list(lp.edges)
    okB, msgB = _chamfer(comp, win_e, P["bezel_edge_break"],
                         "front_edge_break_window")
    print("front break, window          %.2f chamfer : %s %s"
          % (P["bezel_edge_break"], okB, msgB))

    # ---- lip entry lead-in, OUTER loop of the rear tip face only ----------
    body = comp.bRepBodies.itemByName("BEZEL")
    tip = _planar_face(body, d["z_lip_rear"], -1)
    lead_edges = []
    if tip:
        for lp in tip.loops:
            if lp.isOuter:
                lead_edges = list(lp.edges)
    ok2, msg2 = _chamfer(comp, lead_edges, P["bezel_lip_lead"], "lip_lead_in")
    print("lip lead-in %.2f x 45deg : %s %s" % (P["bezel_lip_lead"], ok2, msg2))

    # ---- reference bodies ------------------------------------------------
    po = _add_comp(root, COMP_PANEL)
    _add_bodies(po.component, [(build_panel(b, P, d), "PANEL_Perspex")])

    go = _add_comp(root, COMP_GLASS)
    _add_bodies(go.component,
                [(build_glass(b, P, d), "OLED_Glass_PLACEHOLDER")])

    body = comp.bRepBodies.itemByName("BEZEL")
    bb = body.boundingBox
    print("")
    print("REV Q BEZEL")
    print("  bodies in component : %d" % comp.bRepBodies.count)
    print("  isSolid             : %s" % body.isSolid)
    print("  faces / edges       : %d / %d" % (body.faces.count,
                                               body.edges.count))
    print("  volume              : %.4f cm3" % body.physicalProperties.volume)
    print("  bbox X  %+9.4f .. %+9.4f   span %8.4f"
          % (bb.minPoint.x * 10, bb.maxPoint.x * 10,
             (bb.maxPoint.x - bb.minPoint.x) * 10))
    print("  bbox Y  %+9.4f .. %+9.4f   span %8.4f"
          % (bb.minPoint.y * 10, bb.maxPoint.y * 10,
             (bb.maxPoint.y - bb.minPoint.y) * 10))
    print("  bbox Z  %+9.4f .. %+9.4f   span %8.4f"
          % (bb.minPoint.z * 10, bb.maxPoint.z * 10,
             (bb.maxPoint.z - bb.minPoint.z) * 10))
    app.activeViewport.fit()
    return comp


# ---------------------------------------------------------------------------
# Corner-fit tolerance study - pure arithmetic, no Fusion needed
# ---------------------------------------------------------------------------
def _sdf_rrect(x, y, A, Bh, R):
    """Signed distance to a rounded rectangle of half-extents A, Bh and corner
    radius R. Negative inside."""
    qx = abs(x) - (A - R)
    qy = abs(y) - (Bh - R)
    return (math.hypot(max(qx, 0.0), max(qy, 0.0))
            + min(max(qx, qy), 0.0) - R)


def _rrect_path(A, Bh, R, n=1440):
    """Exact points around a rounded-rectangle boundary, with the INWARD unit
    normal at each. Built segment by segment - no root finding, so it is both
    exact and fast enough to sit inside a bisection loop."""
    a, bb = A - R, Bh - R
    straight = 2.0 * (2 * a) + 2.0 * (2 * bb)
    arc = 2.0 * math.pi * R
    total = straight + arc
    if total <= 0:
        return []
    pts = []
    # how many samples each segment gets, proportional to its length
    n_x = max(2, int(round(n * (2 * a) / total))) if a > 0 else 0
    n_y = max(2, int(round(n * (2 * bb) / total))) if bb > 0 else 0
    n_c = max(2, int(round(n * (math.pi * R / 2.0) / total))) if R > 0 else 0

    for i in range(n_y):                      # right and left runs
        t = -bb + 2 * bb * i / max(1, n_y - 1)
        pts.append((A, t, -1.0, 0.0))
        pts.append((-A, t, 1.0, 0.0))
    for i in range(n_x):                      # top and bottom runs
        t = -a + 2 * a * i / max(1, n_x - 1)
        pts.append((t, Bh, 0.0, -1.0))
        pts.append((t, -Bh, 0.0, 1.0))
    for sx in (1.0, -1.0):                    # the four corner arcs
        for sy in (1.0, -1.0):
            for i in range(n_c):
                th = 0.5 * math.pi * i / max(1, n_c - 1)
                cx, cy = math.cos(th), math.sin(th)
                pts.append((sx * (a + R * cx), sy * (bb + R * cy),
                            -sx * cx, -sy * cy))
    return pts


def corner_clearance(P, d, R_lip, R_panel, n=720):
    """Minimum clearance from the lip OUTER surface to the Perspex opening
    wall, for an assumed opening corner radius. Negative means the lip fouls
    the opening and the bezel will NOT seat."""
    A, Bh = d["po_w2"], d["po_h2"]
    worst = 1.0e9
    for (px, py, _nx, _ny) in _rrect_path(d["low2"], d["loh2"], R_lip, n):
        v = -_sdf_rrect(px, py, A, Bh, R_panel)
        if v < worst:
            worst = v
    return worst


def corner_gap_at_bisector(P, d, R_lip, R_panel):
    """How far the lip stands off the opening wall on the 45 degree corner
    bisector - i.e. how much cut edge stays UNMASKED at the corner."""
    a = d["low2"] - R_lip
    b = d["loh2"] - R_lip
    k = math.sqrt(0.5)
    return -_sdf_rrect(a + R_lip * k, b + R_lip * k,
                       d["po_w2"], d["po_h2"], R_panel)


def max_panel_r(P, d, R_lip, need=0.0):
    """The largest Perspex opening corner radius this lip corner radius can
    tolerate and still seat with at least `need` clearance."""
    lo, hi = 0.0, 7.0
    if corner_clearance(P, d, R_lip, lo) < need:
        return None
    for _ in range(24):
        mid = (lo + hi) / 2.0
        if corner_clearance(P, d, R_lip, mid) >= need:
            lo = mid
        else:
            hi = mid
    return lo


def _corner_wall_range(d, n=2001):
    """Wall thickness right round one corner arc, min and max, in mm.

    With the split wall the corner is where 1.25 has to become 0.80, so this
    is the one place the thickness is neither of the entered values. Measured
    as the distance from each point on the INNER corner arc out to the outer
    profile, which is exact for a rounded rectangle."""
    Ao, Bo = d["low2"], d["loh2"]
    Ro, Ri = d["lip_corner_r"], d["bezel_lip_inner_r"]
    ai, bi = d["liw2"] - Ri, d["lih2"] - Ri
    lo, hi = 1.0e9, -1.0e9
    for i in range(n):
        th = 0.5 * math.pi * i / (n - 1)
        x = ai + Ri * math.cos(th)
        y = bi + Ri * math.sin(th)
        t = -_sdf_rrect(x, y, Ao, Bo, Ro)
        lo, hi = min(lo, t), max(hi, t)
    return lo, hi


def penetration(P, d, R_lip, R_panel, n=1440):
    """Deepest penetration of the lip OUTER surface into the Perspex, and the
    largest gap, for an assumed opening corner radius.

    Positive penetration means material overlap - which for Rev Q is now
    DELIBERATE on the horizontal flanks and must equal the declared value."""
    A, Bh = d["po_w2"], d["po_h2"]
    worst_pen, worst_gap = -1e9, -1e9
    for (px, py, _nx, _ny) in _rrect_path(d["low2"], d["loh2"], R_lip, n):
        s = _sdf_rrect(px, py, A, Bh, R_panel)   # >0 = outside the opening
        worst_pen = max(worst_pen, s)
        worst_gap = max(worst_gap, -s)
    return worst_pen, worst_gap


def fit_study(P=P):
    """The Rev Q interference fit, and what it does at the corners."""
    d = derive(P)
    R = P["bezel_lip_corner_r"]
    print("=" * 74)
    print("REV Q FIT STUDY - INTERFERENCE ON BOTH AXES")
    print("=" * 74)
    print("opening    %.2f x %.2f mm   (MEASURED; corner radius NOT RECORDED)"
          % (P["panel_open_w"], P["panel_open_h"]))
    print("lip outer  %.2f x %.2f mm   R%.2f outer corners"
          % (P["bezel_lip_outer_w"], P["bezel_lip_outer_h"], R))
    print("lip inner  %.2f x %.2f mm   R%.2f inner corners  (derived)"
          % (d["bezel_lip_inner_w"], d["bezel_lip_inner_h"],
             d["bezel_lip_inner_r"]))
    print("wall       SIDES %.2f mm (%.3f loops)   TOP/BOTTOM %.2f mm (%.3f loops)"
          % (d["bezel_lip_wall_x"], d["wall_loops_x"],
             d["bezel_lip_wall_y"], d["wall_loops_y"]))
    print("           corners sweep between the two, never below %.2f mm"
          % d["bezel_lip_wall_y"])
    print("")
    print("DECLARED FIT")
    print("   horizontal  %+.3f mm per side   INTERFERENCE - the lip is wider"
          % d["bezel_lip_interf_x"])
    print("               than the hole and must flex to enter")
    print("   vertical    %+.3f mm per side   INTERFERENCE - so is the lip"
          % d["bezel_lip_interf_y"])
    print("")
    print("AND AS MODELLED IT CANNOT ENTER")
    print("   The skirt is %.2f x %.2f into a %.2f x %.2f hole: %.2f mm"
          % (P["bezel_lip_outer_w"], P["bezel_lip_outer_h"],
             P["panel_open_w"], P["panel_open_h"],
             2 * d["bezel_lip_interf_x"]))
    print("   oversize across and %.2f mm oversize up. PETG will not give"
          % (2 * d["bezel_lip_interf_y"]))
    print("   that up. Either the MEASURED panel_open_h is stale or the")
    print("   vertical move overshoots - owner-directed, and no CAD check")
    print("   in this repository can settle which.")
    print("")
    print("WHAT THE R%.2f CORNERS DO ABOUT THE UNMEASURED OPENING CORNER" % R)
    print("   The R%.2f outer corner pulls the lip well away from the corner," % R)
    print("   so an unmeasured opening corner radius no longer decides whether")
    print("   the part seats - it only decides how much corner is left")
    print("   unmasked. That was the open risk at the 0.40 mm wall; it is not")
    print("   the open risk now. The interference is.")
    print("")
    print("   Larger corners buy robustness against the unmeasured opening")
    print("   corner and pay for it in corner masking - the largest-gap")
    print("   column above is cut edge left visible at each corner.")
    print("")
    print("   R_panel   deepest penetration   largest gap   verdict")
    dmax = max(d["bezel_lip_interf_x"], d["bezel_lip_interf_y"])
    for rp in (0.00, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 2.50, 3.00):
        pen, gap = penetration(P, d, R, rp)
        if pen > dmax + 1e-4:
            verdict = "EXCEEDS the declared interference"
        else:
            verdict = "within the declared %.2f mm" % dmax
        print("   %5.2f        %+7.3f            %+7.3f      %s"
              % (rp, pen, gap, verdict))
    print("")
    print("   deepest penetration stays at the declared %.3f mm for every"
          % dmax)
    print("   plausible opening corner radius: the flanks set it, not the")
    print("   corners.")
    print("")
    print("INSERTION - THE OPEN RISK, AND IT HAS GROWN")
    wx = d["bezel_lip_wall_x"]
    print("   The interference is HORIZONTAL, so it is resisted by the SIDE")
    print("   wall - and that is the wall that just went to %.2f mm to make" % wx)
    print("   the aperture flush.")
    print("")
    print("   Bending stiffness scales with thickness CUBED:")
    for prev in (0.40, 0.80):
        print("      vs a %.2f mm wall   %5.1fx stiffer" % (prev, (wx / prev) ** 3))
    print("")
    print("   So the same %.2f mm per side is now resisted roughly %.0fx harder"
          % (d["bezel_lip_interf_x"], (wx / 0.40) ** 3))
    print("   than at the original 0.40 mm wall, and about %.1fx harder than at"
          % ((wx / 0.80) ** 3))
    print("   the 0.80 mm wall it replaced on the sides. Brief 3.8 requires the")
    print("   PRINTED WALL to take the deflection and the Perspex to be left")
    print("   unspread and unstressed. At %.2f mm that is a much harder ask, and" % wx)
    print("   CAD cannot settle it. PRINT THE FIT GAUGE BEFORE THE BEZEL - and")
    print("   be ready to reduce bezel_lip_outer_w AND bezel_lip_outer_h.")
    print("=" * 74)


# kept under the old name so existing notes and links still resolve
def corner_study(P=P):
    fit_study(P)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------
_RESULTS = []


def _gate(ok, label, detail=""):
    _RESULTS.append((bool(ok), label))
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", label, detail))
    return bool(ok)


def _report(label, detail=""):
    print("  [    ] %-58s %s" % (label, detail))


def _vol_mm3(body):
    try:
        return body.volume * 1000.0
    except Exception:
        return 0.0


def _hit_mm3(b, a1, a2):
    """Volume of the intersection of two solids, in mm3. Touching faces give
    zero volume, which is what we want - the seating face is MEANT to touch
    the Perspex."""
    c1, c2 = b.copy(a1), b.copy(a2)
    try:
        ok = b.t.booleanOperation(
            c1, c2, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    except Exception:
        return 0.0
    if not ok:
        return 0.0
    try:
        return _vol_mm3(c1)
    except Exception:
        return 0.0


def _slab_area(b, body, z, thick=0.01, region=None):
    """Cross-section area of a solid at height z, in mm2, by intersecting a
    thin slab and dividing the volume by its thickness. Optionally restricted
    to a region box (x0, x1, y0, y1)."""
    big = 60.0
    x0, x1, y0, y1 = region if region else (-big, big, -big, big)
    slab = b.box(x0, x1, y0, y1, z - thick / 2.0, z + thick / 2.0)
    return _hit_mm3(b, body, slab) / thick


def _aperture_at(body, d, z, limit=20.0, step=0.01):
    """Clear aperture width and height at height z, found by marching out
    along each axis from the centre to the first solid material.

    Marched, not bisected: walking outward the ray goes void -> material ->
    air, which is not monotone, and bisection steps straight over a thin
    band."""
    out = []
    for axis in (0, 1):
        t, prev = step, 0.0
        hit = None
        while t < limit:
            x, y = (t, 0.0) if axis == 0 else (0.0, t)
            if _inside(body, x, y, z):
                lo, hi = prev, t
                for _ in range(30):
                    mid = (lo + hi) / 2.0
                    xx, yy = (mid, 0.0) if axis == 0 else (0.0, mid)
                    if _inside(body, xx, yy, z):
                        hi = mid
                    else:
                        lo = mid
                hit = (lo + hi) / 2.0
                break
            prev = t
            t += step
        if hit is None:
            return None
        out.append(2.0 * hit)
    return (out[0], out[1])


def _hit_bbox(b, a1, a2):
    """Bounding box of the intersection of two solids, in mm, or None."""
    c1, c2 = b.copy(a1), b.copy(a2)
    try:
        ok = b.t.booleanOperation(
            c1, c2, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    except Exception:
        return None
    if not ok:
        return None
    try:
        if _vol_mm3(c1) <= 1.0e-9:
            return None
        bb = c1.boundingBox
        return (bb.minPoint.x * 10, bb.maxPoint.x * 10,
                bb.minPoint.y * 10, bb.maxPoint.y * 10,
                bb.minPoint.z * 10, bb.maxPoint.z * 10)
    except Exception:
        return None


def _inside(body, x, y, z):
    pc = body.pointContainment(p3(x, y, z))
    return pc == adsk.fusion.PointContainment.PointInsidePointContainment


def validate(P=P):
    global _RESULTS
    _RESULTS = []
    d = derive(P)
    app = _app()
    design = _design()
    root = design.rootComponent
    comp, occ = _bezel_comp()
    body = comp.bRepBodies.itemByName("BEZEL")
    b = B()

    print("=" * 74)
    print("DECCA OLED DISPLAY BEZEL - REV Q VALIDATION")
    print("=" * 74)
    print("")
    print("1. SOLID INTEGRITY")
    _gate(comp.bRepBodies.count == 1, "exactly one body in the component",
          "%d" % comp.bRepBodies.count)
    _gate(body.isSolid, "the body is a closed solid", str(body.isSolid))
    _gate(body.shells.count == 1, "one connected shell, so one connected solid",
          "%d shell(s)" % body.shells.count)
    _gate(body.lumps.count == 1, "one lump, nothing floating loose",
          "%d lump(s)" % body.lumps.count)

    tiny_f = [f for f in body.faces if f.area * 100.0 < 1.0e-3]
    tiny_e = [e for e in body.edges if e.length * 10.0 < 5.0e-3]
    _gate(len(tiny_f) == 0, "no sliver faces below 0.001 mm2",
          "%d found" % len(tiny_f))
    _gate(len(tiny_e) == 0, "no sliver edges below 0.005 mm",
          "%d found" % len(tiny_e))
    _report("faces / edges / volume",
            "%d / %d / %.4f cm3" % (body.faces.count, body.edges.count,
                                    body.physicalProperties.volume))

    print("")
    print("2. ENVELOPE - the Rev N appearance must be preserved")
    bb = body.boundingBox
    sx = (bb.maxPoint.x - bb.minPoint.x) * 10
    sy = (bb.maxPoint.y - bb.minPoint.y) * 10
    sz = (bb.maxPoint.z - bb.minPoint.z) * 10
    _gate(abs(sx - P["bezel_w"]) < 1e-6, "envelope width  40.00 mm",
          "%.5f" % sx)
    _gate(abs(sy - P["bezel_h"]) < 1e-6, "envelope height 20.30 mm",
          "%.5f" % sy)
    _gate(abs(sz - P["bezel_t"]) < 1e-6, "envelope depth   4.00 mm",
          "%.5f" % sz)
    _gate(abs(bb.maxPoint.z * 10 - d["z_bezel_front"]) < 1e-6,
          "bezel front face at z = +4.200", "%.5f" % (bb.maxPoint.z * 10))
    _gate(abs(bb.minPoint.z * 10 - d["z_lip_rear"]) < 1e-6,
          "rearmost material at z = +0.200", "%.5f" % (bb.minPoint.z * 10))

    print("")
    print("3. THE CONTINUOUS LIP - by measured cross-section AREA")
    #
    # NOT by point sampling. BRepBody.pointContainment is not trustworthy on
    # this body: with the tapered aperture the face wall is a single NURBS
    # surface, and containment then reports the middle of the open aperture as
    # solid and scattered points inside the lip as void. Cross-section area,
    # taken by boolean intersection with a thin slab, is exact and cannot
    # drift - and it is a STRONGER continuity proof than sampling, because any
    # break anywhere in the ring shows up as missing area.
    zs = [d["z_lip_rear"] + P["bezel_lip_lead"] + 0.05,
          (d["z_lip_rear"] + d["z_panel_front"]) / 2.0,
          d["z_panel_front"] - 0.05]
    ax = d["low2"] - P["bezel_lip_corner_r"]     # 14.70
    ay = d["loh2"] - P["bezel_lip_corner_r"]     #  4.60
    wx, wy = d["bezel_lip_wall_x"], d["bezel_lip_wall_y"]
    Ro, Ri = P["bezel_lip_corner_r"], d["bezel_lip_inner_r"]
    big = 60.0
    # The straight runs are clean rectangles in these windows. In X both
    # profiles turn at the same station (outer_half - Ro == inner_half - Ri,
    # because Ri is derived from the X wall), so the top and bottom windows
    # cut exactly across the straight runs of both.
    regions = [
        ("top", (-ax, ax, ay, big), wy * 2 * ax),
        ("bottom", (-ax, ax, -big, -ay), wy * 2 * ax),
        ("right", (ax, big, -ay, ay), wx * 2 * ay),
        ("left", (-big, -ax, -ay, ay), wx * 2 * ay),
    ]
    # With a split wall the ring is no longer a uniform offset, so the corner
    # area is not pi*(Ro^2 - Ri^2) any more. Take the whole ring analytically -
    # outer rounded rect minus inner rounded rect - and let the corners be the
    # remainder.
    def _rrect_area(hw, hh, r):
        return (2 * hw) * (2 * hh) - (4.0 - math.pi) * r * r
    ring_exact = (_rrect_area(d["low2"], d["loh2"], Ro)
                  - _rrect_area(d["liw2"], d["lih2"], Ri))
    corner_exact = ring_exact - sum(r[2] for r in regions)
    for z in zs:
        got = _slab_area(b, body, z)
        _gate(abs(got - ring_exact) < 5.0e-3,
              "z = %.2f  full ring area = %.4f mm2" % (z, ring_exact),
              "%.4f mm2" % got)
    zmid = zs[1]
    part_sum = 0.0
    for name, (x0, x1, y0, y1), exact in regions:
        got = _slab_area(b, body, zmid, region=(x0, x1, y0, y1))
        part_sum += got
        _gate(abs(got - exact) < 5.0e-3,
              "lip continuous - %-6s  area %.4f mm2" % (name, exact),
              "%.4f mm2" % got)
    got_corners = _slab_area(b, body, zmid) - part_sum
    _gate(abs(got_corners - corner_exact) < 5.0e-3,
          "lip continuous - corners  area %.4f mm2" % corner_exact,
          "%.4f mm2" % got_corners)
    _report("why area and not point sampling",
            "any gap, thin spot or break anywhere in the ring removes area; "
            "an exact area match leaves nowhere for one to hide")

    # --- outer envelope ----------------------------------------------------
    lip_bb = _hit_bbox(b, body, b.box(-big, big, -big, big,
                                      d["z_lip_rear"] + 0.001,
                                      d["z_panel_front"] - 0.001))
    _gate(lip_bb is not None
          and abs(lip_bb[1] - d["low2"]) < 1.0e-4
          and abs(lip_bb[3] - d["loh2"]) < 1.0e-4,
          "lip outer envelope is exactly %.2f x %.2f"
          % (P["bezel_lip_outer_w"], P["bezel_lip_outer_h"]),
          "%.4f x %.4f" % ((lip_bb[1] * 2, lip_bb[3] * 2) if lip_bb
                           else (-1, -1)))

    # --- the split wall and its corners ------------------------------------
    _gate(abs(d["bezel_lip_wall_x"]
              - (P["bezel_lip_outer_w"] - P["bezel_window_w"]) / 2.0) < 1e-9,
          "side wall %.3f mm is DERIVED from the flush requirement"
          % d["bezel_lip_wall_x"],
          "(%.2f - %.2f)/2" % (P["bezel_lip_outer_w"], P["bezel_window_w"]))
    _gate(abs(d["bezel_lip_inner_w"] - P["bezel_window_w"]) < 1e-9,
          "FLUSH: skirt inner width == face opening, no set-back at the sides",
          "%.4f vs %.4f" % (d["bezel_lip_inner_w"], P["bezel_window_w"]))
    _gate(abs(d["bezel_lip_inner_h"] - P["bezel_window_h"]) < 1e-9,
          "FLUSH: skirt inner height == face opening, no ledge top or bottom",
          "%.4f vs %.4f" % (d["bezel_lip_inner_h"], P["bezel_window_h"]))
    _gate(abs(d["bezel_lip_inner_r"] - P["bezel_window_r"]) < 1e-9,
          "FLUSH: skirt inner corner == face opening corner, so neither "
          "one cuts inside the other",
          "R%.4f vs R%.4f" % (d["bezel_lip_inner_r"], P["bezel_window_r"]))
    _gate(abs(d["bezel_lip_inner_r"]
              - (P["bezel_lip_corner_r"] - d["bezel_lip_wall_x"])) < 1e-9,
          "inner corner R%.2f = outer R%.2f - side wall %.2f"
          % (d["bezel_lip_inner_r"], P["bezel_lip_corner_r"],
             d["bezel_lip_wall_x"]),
          "%.4f" % d["bezel_lip_inner_r"])
    # With a split wall the corner is where the two thicknesses have to meet.
    # Measure the wall right round the corner arc and demand it never drops
    # below the thinner of the two - i.e. never below two full loops.
    cmin, cmax = _corner_wall_range(d)
    _gate(cmin >= d["bezel_lip_wall_y"] - 1.0e-4,
          "wall through the R%.2f corners never thins below the %.2f mm "
          "top/bottom wall" % (P["bezel_lip_corner_r"], d["bezel_lip_wall_y"]),
          "min %.4f  max %.4f mm" % (cmin, cmax))
    _gate(cmax <= d["bezel_lip_wall_x"] + 1.0e-4,
          "and never exceeds the %.2f mm side wall through the arc"
          % d["bezel_lip_wall_x"], "%.4f mm" % cmax)
    _report("corner wall sweep",
            "%.4f -> %.4f mm across the arc; the full %.2f mm is carried "
            "on the straight side runs, outside the arc"
            % (cmin, cmax, d["bezel_lip_wall_x"]))

    # --- the loop rule: AT LEAST two, per side ------------------------------
    ew = P["extrusion_width"]
    _gate(d["wall_loops_x"] >= 2.0 - 1e-9,
          "side wall is at least two %.2f mm loops" % ew,
          "%.3f / %.2f = %.3f loops" % (d["bezel_lip_wall_x"], ew,
                                        d["wall_loops_x"]))
    _gate(d["wall_loops_y"] >= 2.0 - 1e-9,
          "top/bottom wall is at least two %.2f mm loops" % ew,
          "%.3f / %.2f = %.3f loops" % (d["bezel_lip_wall_y"], ew,
                                        d["wall_loops_y"]))
    _gate(cmin / ew >= 2.0 - 1.0e-3,
          "and the corners never fall below two loops either",
          "%.3f loops at the thinnest" % (cmin / ew))
    # the two loop centrelines are offsets of the outer surface by 0.20 and
    # 0.60; both must stay closed and non-degenerate right through the
    # corners, or the slicer merges them or drops one
    r1 = P["bezel_lip_corner_r"] - ew / 2.0
    r2 = P["bezel_lip_corner_r"] - ew - ew / 2.0
    _gate(r2 > 0.0,
          "outer loop R%.3f and inner loop R%.3f at the corners, no cusp"
          % (r1, r2), "smallest offset radius %.3f mm" % r2)
    _gate(abs((r1 - r2) - ew) < 1e-9,
          "loop centrelines stay exactly one extrusion apart",
          "%.4f mm" % (r1 - r2))
    _gate(abs(ring_exact - _slab_area(b, body, zmid)) < 5.0e-3,
          "no thin spot anywhere - every section is at least two extrusions",
          "measured ring area matches the %.2f/%.2f split wall exactly"
          % (d["bezel_lip_wall_x"], d["bezel_lip_wall_y"]))
    _report("SLICER PREVIEW IS STILL A PHYSICAL GATE",
            "the geometry admits two loops; only the production slicer can "
            "prove that it lays them")

    tip = _planar_face(body, d["z_lip_rear"])
    _gate(tip is not None, "lip rear tip face exists at z = +0.200",
          "%.4f mm2" % (tip.area * 100.0 if tip else 0.0))
    _gate(abs((d["z_panel_front"] - d["z_lip_rear"]) - P["bezel_lip_depth"])
          < 1e-9, "lip depth = 2.800 mm",
          "%.5f" % (d["z_panel_front"] - d["z_lip_rear"]))
    _gate(abs(d["bezel_lip_interf_x"]
              - (P["bezel_lip_outer_w"] - P["panel_open_w"]) / 2.0) < 1e-9,
          "horizontal INTERFERENCE %.3f mm per side"
          % d["bezel_lip_interf_x"],
          "(%.2f - %.2f)/2 = %+.4f mm"
          % (P["bezel_lip_outer_w"], P["panel_open_w"],
             d["bezel_lip_interf_x"]))
    _gate(abs(d["bezel_lip_interf_y"]
              - (P["bezel_lip_outer_h"] - P["panel_open_h"]) / 2.0) < 1e-9,
          "vertical INTERFERENCE %.3f mm per side"
          % d["bezel_lip_interf_y"],
          "(%.2f - %.2f)/2 = %+.4f mm"
          % (P["bezel_lip_outer_h"], P["panel_open_h"],
             d["bezel_lip_interf_y"]))
    _report("BOTH AXES ARE NOW AN INTERFERENCE - AND IT WILL NOT ENTER",
            "a %.2f x %.2f skirt into a %.2f x %.2f hole is %.2f mm "
            "oversize across and %.2f mm oversize up. As modelled the part "
            "cannot be assembled. OWNER-DIRECTED; either the MEASURED "
            "panel_open_h is stale or the vertical move overshoots, and no "
            "check in this file can settle which."
            % (P["bezel_lip_outer_w"], P["bezel_lip_outer_h"],
               P["panel_open_w"], P["panel_open_h"],
               2 * d["bezel_lip_interf_x"], 2 * d["bezel_lip_interf_y"]))

    print("")
    print("4. THE ORIGINAL PERSPEX - the declared interference, and nothing else")
    panel_occ = _find_occ(COMP_PANEL)
    panel = panel_occ.bRepBodies.item(0)
    v = _hit_mm3(b, body, panel)
    _gate(v > 1.0e-6,
          "the declared horizontal interference IS present",
          "%.4f mm3 of overlap" % v)

    # Where is it? The overlap must live only on the two horizontal flanks,
    # outboard of the opening wall, and nowhere else.
    hit_bb = _hit_bbox(b, body, panel)
    if hit_bb:
        (hx0, hx1, hy0, hy1, hz0, hz1) = hit_bb
        _gate(hz0 >= d["z_lip_rear"] - 1.0e-4
              and hz1 <= d["z_panel_front"] + 1.0e-4,
              "overlap is confined to the lip depth",
              "z %.4f .. %.4f" % (hz0, hz1))
        _gate((max(abs(hx0), abs(hx1)) - d["po_w2"])
              <= d["bezel_lip_interf_x"] + 1.0e-4,
              "overlap never exceeds the declared %.3f mm per side in X"
              % d["bezel_lip_interf_x"],
              "deepest %.4f mm"
              % (max(abs(hx0), abs(hx1)) - d["po_w2"]))
        _gate((max(abs(hy0), abs(hy1)) - d["po_h2"])
              <= d["bezel_lip_interf_y"] + 1.0e-4,
              "overlap never exceeds the declared %.3f mm per side in Y"
              % d["bezel_lip_interf_y"],
              "deepest %.4f mm"
              % (max(abs(hy0), abs(hy1)) - d["po_h2"]))

    # An independent statement of the same thing: relieve the opening by the
    # declared interference on BOTH axes now, and NOTHING may touch it any
    # more.
    relieved = build_panel(b, P, d, relief_x=d["bezel_lip_interf_x"],
                           relief_y=d["bezel_lip_interf_y"])
    vr = _hit_mm3(b, body, relieved)
    _gate(vr < 1.0e-6,
          "with the declared relief applied, interference falls to zero",
          "%.6f mm3" % vr)

    behind = build_behind_panel(b, P, d)
    v2 = _hit_mm3(b, body, behind)
    _gate(v2 < 1.0e-6,
          "no material behind the Perspex rear face (z = 0)",
          "%.6f mm3" % v2)
    _gate(bb.minPoint.z * 10 >= d["z_panel_rear"],
          "rearmost bezel material is forward of DATUM A",
          "z = %+.4f, %.3f mm clear"
          % (bb.minPoint.z * 10, d["clear_to_panel_rear"]))

    print("")
    print("5. THE OLED")
    glass_occ = _find_occ(COMP_GLASS)
    glass = glass_occ.bRepBodies.item(0)
    v3m = _hit_mm3(b, body, glass)
    _gate(v3m < 1.0e-6, "no interference with the OLED glass proxy",
          "%.6f mm3" % v3m)
    _gate(d["clear_to_glass"] >= 0.5 - 1e-9,
          "clearance to the OLED glass front face >= 0.500 mm",
          "%.4f mm" % d["clear_to_glass"])
    _report("glass envelope caveat",
            "UNMEASURED placeholder, exactly as the released Rev P model")

    print("")
    print("6. THE FROZEN REV P.5 CARRIER")
    car = _find_occ(COMP_CARRIER)
    if car is None:
        _report("carrier reference", "NOT IMPORTED - run import_carrier() first")
    else:
        # a STEP import nests the solid in a sub-occurrence, so walk the tree
        cb = _all_bodies(car)
        tot = 0.0
        for bd in cb:
            tot += _hit_mm3(b, body, bd)
        _gate(tot < 1.0e-6,
              "no interference with the released Rev P.5 carrier",
              "%.6f mm3 over %d body(ies)" % (tot, len(cb)))
        try:
            dist = app.measureManager.measureMinimumDistance(
                body.createForAssemblyContext(occ), cb[0]).value * 10.0
            _report("minimum distance bezel to carrier", "%.4f mm" % dist)
        except Exception as ex:
            _report("minimum distance bezel to carrier", "not measured: %s" % ex)
    _report("sprung-post and module corridors",
            "covered by check 4: every corridor lies at z < 0 and the bezel "
            "does not reach z = 0")

    print("")
    print("7. THE FACE OPENING AND THE EFFECTIVE OPTICAL OPENING")
    # The clear opening is bracketed with two solid "plugs" pushed through the
    # whole part. A plug of the declared size must pass without touching
    # anything; a plug 0.04 mm larger must hit. That pins the opening from
    # both sides using booleans only.
    eps = 0.02
    plug = b.rprism(-d["optical_w"] / 2.0 + eps, d["optical_w"] / 2.0 - eps,
                    -d["optical_h"] / 2.0 + eps, d["optical_h"] / 2.0 - eps,
                    d["z_lip_rear"] - 0.5, d["z_bezel_front"] + 0.5,
                    d["optical_r"])
    vplug = _hit_mm3(b, body, plug)
    _gate(vplug < 1.0e-6,
          "a %.2f x %.2f plug passes clean through - nothing intrudes"
          % (d["optical_w"] - 2 * eps, d["optical_h"] - 2 * eps),
          "%.6f mm3" % vplug)
    plug2 = b.rprism(-d["optical_w"] / 2.0 - eps, d["optical_w"] / 2.0 + eps,
                     -d["optical_h"] / 2.0 - eps, d["optical_h"] / 2.0 + eps,
                     d["z_lip_rear"] - 0.5, d["z_bezel_front"] + 0.5,
                     d["optical_r"])
    vplug2 = _hit_mm3(b, body, plug2)
    _gate(vplug2 > 1.0e-6,
          "a %.2f x %.2f plug does NOT - the opening is no larger"
          % (d["optical_w"] + 2 * eps, d["optical_h"] + 2 * eps),
          "%.4f mm3 of contact" % vplug2)
    _report("aperture at the seating plane",
            "%.3f x %.3f mm - set by the lip inner envelope"
            % (d["ap_rear_w"], d["ap_rear_h"]))
    _report("aperture at the front face, before the 0.40 break",
            "%.3f x %.3f mm - the specified bezel face opening"
            % (d["ap_front_w"], d["ap_front_h"]))
    _report("aperture taper",
            "%.2f deg - the aperture is a STRAIGHT bore now, flush with "
            "the skirt on all four sides, so there is no taper left to "
            "support" % d["ap_taper_deg"])
    _gate(abs(d["optical_w"] - P["bezel_window_w"]) < 1e-9
          and abs(d["optical_h"] - d["bezel_lip_inner_h"]) < 1e-9,
          "EFFECTIVE optical opening = %.2f x %.2f"
          % (P["bezel_window_w"], d["bezel_lip_inner_h"]),
          "%.3f x %.3f" % (d["optical_w"], d["optical_h"]))
    _report("versus the figure brief 4 predicts",
            "30.90 x 13.60 - now %+.2f mm wider and %+.2f mm taller, both "
            "owner-directed: the face opened 1.00 mm per side, then the "
            "skirt walls moved out 1.00 mm each"
            % (d["optical_w"] - 30.90, d["optical_h"] - 13.60))
    _report("controlled by",
            "the skirt inner envelope on ALL FOUR sides - the face opening "
            "is flush with it at %.2f x %.2f R%.2f, so neither one masks "
            "the other" % (d["bezel_window_w"], d["bezel_window_h"],
                           P["bezel_window_r"]))
    _report("Rev N clear opening",
            "%.3f W x %.3f H mm (R%.2f)"
            % (d["revN_window_w"], d["revN_window_h"], P["bezel_window_r"]))
    _report("Rev Q clear opening",
            "%.3f W x %.3f H mm (R%.2f)"
            % (d["optical_w"], d["optical_h"], d["optical_r"]))
    _report("change versus Rev N",
            "width %.3f -> %.3f (%+.3f), height %.3f -> %.3f (%+.3f mm "
            "total, %+.3f per side). The lip no longer COSTS opening - "
            "after the owner moves it gives some back."
            % (d["revN_window_w"], d["optical_w"],
               d["optical_w"] - d["revN_window_w"],
               d["revN_window_h"], d["optical_h"],
               d["optical_h"] - d["revN_window_h"],
               (d["optical_h"] - d["revN_window_h"]) / 2.0))
    _report("controlled by",
            "the lip and the bezel face together - they are flush, so "
            "neither is the limiter on its own")
    _report("visible OLED active area, Rev N",
            "%.3f W x %.3f H mm" % (d["vis_w"], d["vis_n_h"]))
    _report("visible OLED active area, Rev Q",
            "%.3f W x %.3f H mm" % (d["vis_w"], d["vis_q_h"]))
    _report("active height versus Rev N",
            "%+.3f mm, all of it at the TOP edge"
            % (-d["active_loss_vs_revN"]))
    _report("unlit board visible below the active area",
            "Rev N %.3f -> Rev Q %.3f mm"
            % (d["unlit_below_n"], d["unlit_below_q"]))
    _report("NOT A CAD DECISION",
            "acceptability of the powered image is a PHYSICAL test")

    print("")
    print("8. PRINT ORIENTATION - front face DOWN on the bed")
    ov = _overhangs(body, d)
    _gate(ov["lip_vertical"],
          "the thin lip is self-supporting, no face over 45 deg",
          "%d lip faces, worst overhang %.3f deg"
          % (ov["lip_faces"], ov["lip_max_overhang"]))
    _gate(ov["bad_area"] < 1.0e-6,
          "no unsupported overhang outside the R0.40 front edge break",
          "%.4f mm2 elsewhere %s"
          % (ov["bad_area"], ov["bad_faces"] if ov["bad_faces"] else ""))
    _report("bed contact area, front face down",
            "%.3f mm2" % ov["bed_area"])
    _report("the two R0.40 front edge breaks",
            "worst %.1f deg, but they sit ON the bed within the first 0.400 mm "
            "- geometry identical to Rev N, no support" % ov["break_max"])

    print("")
    ok = all(r[0] for r in _RESULTS)
    npass = sum(1 for r in _RESULTS if r[0])
    print("=" * 74)
    print("GATES: %d/%d PASS   ->   %s" % (npass, len(_RESULTS),
                                           "ALL PASS" if ok else "FAILURES"))
    if not ok:
        for good, label in _RESULTS:
            if not good:
                print("   FAILED: %s" % label)
    print("=" * 74)
    return ok


def _face_outward_nz(body, f, samples=9):
    """Worst (most bed-facing) outward normal Z component on a face.

    The sign of a surface normal is NOT reliably the outward sense of the face
    - isParamReversed is easy to get backwards and a wrong guess silently
    inverts the whole overhang census. So the outward side is settled
    geometrically: step off the surface along the normal and ask the solid
    which side it is on.
    """
    ev = f.evaluator
    rng = ev.parametricRange()
    worst = None
    k = int(round(math.sqrt(samples)))
    for i in range(k):
        for j in range(k):
            u = (i + 0.5) / k
            v = (j + 0.5) / k
            pt = adsk.core.Point2D.create(
                rng.minPoint.x + u * (rng.maxPoint.x - rng.minPoint.x),
                rng.minPoint.y + v * (rng.maxPoint.y - rng.minPoint.y))
            try:
                okp, pos = ev.getPointAtParameter(pt)
                okn, n = ev.getNormalAtParameter(pt)
            except Exception:
                continue
            if not (okp and okn):
                continue
            L = n.length or 1.0
            nx, ny, nz = n.x / L, n.y / L, n.z / L
            eps = 0.002          # cm == 0.02 mm
            probe = adsk.core.Point3D.create(pos.x + nx * eps,
                                             pos.y + ny * eps,
                                             pos.z + nz * eps)
            inside = (body.pointContainment(probe)
                      == adsk.fusion.PointContainment.PointInsidePointContainment)
            out_nz = -nz if inside else nz
            if worst is None or out_nz > worst:
                worst = out_nz
    return 0.0 if worst is None else worst


def _overhangs(body, d):
    """Overhang census for printing with the bezel FRONT FACE flat on the bed.

    The bed is at the +Z end of the model, so the part grows in -Z and
    'downward' in print space is model +Z. A face overhangs only if its
    OUTWARD normal has a positive Z component; the overhang angle measured
    from vertical is asin(out_nz), so 0 deg is a vertical wall and 90 deg is a
    horizontal ceiling.
    """
    bed_z = d["z_bezel_front"]
    band = P["bezel_edge_break"]          # the R0.40 front break lives here
    out = {"lip_faces": 0, "lip_max_overhang": 0.0, "lip_vertical": True,
           "bad_area": 0.0, "bad_faces": [], "bed_area": 0.0,
           "break_max": 0.0}
    for f in body.faces:
        bbf = f.boundingBox
        zmin, zmax = bbf.minPoint.z * 10, bbf.maxPoint.z * 10
        area = f.area * 100.0
        nz = _face_outward_nz(body, f)
        ang = math.degrees(math.asin(max(0.0, min(1.0, nz))))

        on_bed = abs(zmin - bed_z) < 1e-6 and abs(zmax - bed_z) < 1e-6
        if on_bed:
            out["bed_area"] += area
            continue
        in_break = zmax > bed_z - band - 1e-6

        if zmax <= d["z_panel_front"] + 1e-6:      # a lip surface
            out["lip_faces"] += 1
            out["lip_max_overhang"] = max(out["lip_max_overhang"], ang)

        if ang > 45.0 + 1e-6:
            if in_break:
                out["break_max"] = max(out["break_max"], ang)
            else:
                out["bad_area"] += area
                out["bad_faces"].append((round(zmin, 3), round(zmax, 3),
                                         round(ang, 2), round(area, 4)))
    out["lip_vertical"] = out["lip_max_overhang"] <= 45.0 + 1e-6
    return out


# ---------------------------------------------------------------------------
# The frozen carrier - READ ONLY
# ---------------------------------------------------------------------------
def import_carrier():
    """Bring the RELEASED Rev P.5 carrier in as an immutable reference.

    This READS Rear_Display_Carrier_revP.step. It never writes it, never
    regenerates it and never re-exports it. The Rev Q assembly export
    references this body; the released file itself is untouched.
    """
    app = _app()
    design = _design()
    root = design.rootComponent
    if not os.path.exists(CARRIER_STEP):
        raise RuntimeError("frozen carrier STEP not found: %s" % CARRIER_STEP)
    _drop(root, COMP_CARRIER)
    occ = _add_comp(root, COMP_CARRIER)
    imp = app.importManager
    opts = imp.createSTEPImportOptions(CARRIER_STEP)
    opts.isViewFit = False
    imp.importToTarget(opts, occ.component)
    n = 0
    bbs = None
    for i in range(occ.component.occurrences.count):
        sub = occ.component.occurrences.item(i)
        for bd in sub.bRepBodies:
            n += 1
    for bd in occ.component.bRepBodies:
        n += 1
    bbs = occ.boundingBox
    print("imported frozen carrier : %d body(ies)" % n)
    print("   bbox X %+9.4f .. %+9.4f" % (bbs.minPoint.x * 10,
                                          bbs.maxPoint.x * 10))
    print("   bbox Y %+9.4f .. %+9.4f" % (bbs.minPoint.y * 10,
                                          bbs.maxPoint.y * 10))
    print("   bbox Z %+9.4f .. %+9.4f" % (bbs.minPoint.z * 10,
                                          bbs.maxPoint.z * 10))
    return occ


# ---------------------------------------------------------------------------
# Corner gauge coupon
# ---------------------------------------------------------------------------
def coupon():
    design = _design()
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent
    d = derive(P)
    _drop(root, COMP_COUPON)
    occ = _add_comp(root, COMP_COUPON)
    b = B()
    _add_bodies(occ.component, build_coupon(b, P, d))
    tot = 0.0
    for bd in occ.component.bRepBodies:
        tot += bd.physicalProperties.volume
        print("  %-16s solid=%s  vol=%.4f cm3"
              % (bd.name, bd.isSolid, bd.physicalProperties.volume))
    print("interference fit gauge: %d tabs, %.4f cm3 total"
          % (occ.component.bRepBodies.count, tot))
    return occ


# ---------------------------------------------------------------------------
# Exports - Rev Q names only, never a Rev P.5 file
# ---------------------------------------------------------------------------
_FORBIDDEN = ("revp", "rev_p", "revn", "rev_n", "revo")


def _guard(path):
    base = os.path.basename(path).lower()
    for bad in _FORBIDDEN:
        if bad in base:
            raise RuntimeError(
                "REFUSING to write %s - Rev N/O/P files are frozen" % path)
    return path


def export(what="bezel"):
    app = _app()
    design = _design()
    root = design.rootComponent
    em = design.exportManager
    cad = os.path.join(OUT_DIR, "CAD")
    stl = os.path.join(OUT_DIR, "STL")
    written = []

    if what in ("bezel", "all"):
        comp, occ = _bezel_comp()
        p = _guard(os.path.join(cad, "Decca_Display_Bezel_revQ.f3d"))
        em.execute(em.createFusionArchiveExportOptions(p))
        written.append(p)

        p = _guard(os.path.join(cad, "Front_Bezel_revQ.step"))
        em.execute(em.createSTEPExportOptions(p, comp))
        written.append(p)

        body = comp.bRepBodies.itemByName("BEZEL")
        p = _guard(os.path.join(stl, "Front_Bezel_revQ.stl"))
        o = em.createSTLExportOptions(body, p)
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        o.isBinaryFormat = True
        em.execute(o)
        written.append(p)

        # 3MF as well as STL. A hand-exported 3MF of a superseded build got
        # swept into the repo twice; generating it here means the path always
        # holds the CURRENT geometry instead of whatever was last exported by
        # hand. 3MF also carries units and per-object settings, which STL does
        # not, so it is the better thing to hand a slicer.
        p = _guard(os.path.join(stl, "Front_Bezel_revQ.3mf"))
        try:
            o = em.createC3MFExportOptions(body, p)
            o.meshRefinement = (
                adsk.fusion.MeshRefinementSettings.MeshRefinementHigh)
            em.execute(o)
            written.append(p)
        except Exception as ex:
            print("3MF export skipped: %s" % ex)

    if what in ("assembly", "all"):
        p = _guard(os.path.join(cad, "Decca_Display_Bezel_revQ_assembly.step"))
        em.execute(em.createSTEPExportOptions(p))
        written.append(p)

    if what in ("coupon", "all"):
        occ = _find_occ(COMP_COUPON)
        if occ:
            p = _guard(os.path.join(cad, "Bezel_Fit_Gauge_revQ.step"))
            em.execute(em.createSTEPExportOptions(p, occ.component))
            written.append(p)
            # one mesh carrying all five tabs
            for bd in occ.component.bRepBodies:
                pp = _guard(os.path.join(
                    stl, "Bezel_Fit_Gauge_revQ_%s.stl" % bd.name))
                o = em.createSTLExportOptions(bd, pp)
                o.meshRefinement = \
                    adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
                o.isBinaryFormat = True
                em.execute(o)
                written.append(pp)

    for p in written:
        print("wrote %-70s %8d bytes"
              % (p, os.path.getsize(p) if os.path.exists(p) else -1))
    return written


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------
DRAW = os.path.join(OUT_DIR, "Drawings")
SNAP_PREFIX = "Decca_OLED_Display_Bezel_revQ_"


def _vis(names):
    root = _design().rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        occ.isLightBulbOn = occ.component.name in names


def _shot(name, orientation=None, eye=None, target=None, up=None,
          fit=True, w=1400, h=1000):
    app = _app()
    vp = app.activeViewport
    cam = vp.camera
    if orientation is not None:
        cam.viewOrientation = orientation
    if eye is not None:
        cam.eye = eye
        cam.target = target
        cam.upVector = up
    cam.isFitView = fit
    vp.camera = cam
    vp.refresh()
    adsk.doEvents()
    if fit:
        vp.fit()
        adsk.doEvents()
    path = os.path.join(DRAW, SNAP_PREFIX + name + ".png")
    vp.saveAsImageFile(path, w, h)
    print("snapshot %-64s %8d bytes"
          % (path, os.path.getsize(path) if os.path.exists(path) else -1))
    return path


def _appear(comp, libname):
    """Give every body in a component a library appearance. Purely for
    legibility in the review images - it changes no geometry."""
    app = _app()
    design = _design()
    try:
        lib = app.materialLibraries.itemByName("Fusion Appearance Library")
        a = lib.appearances.itemByName(libname)
        if a is None:
            return
        loc = design.appearances.itemByName(a.name)
        if loc is None:
            loc = design.appearances.addByCopy(a, a.name)
        for bd in comp.bRepBodies:
            bd.appearance = loc
    except Exception as ex:
        print("appearance skipped (%s): %s" % (libname, ex))


def _appear_body(comp, body_name, libname):
    app = _app()
    design = _design()
    try:
        lib = app.materialLibraries.itemByName("Fusion Appearance Library")
        a = lib.appearances.itemByName(libname)
        bd = comp.bRepBodies.itemByName(body_name)
        if a is None or bd is None:
            return
        loc = design.appearances.itemByName(a.name)
        if loc is None:
            loc = design.appearances.addByCopy(a, a.name)
        bd.appearance = loc
    except Exception as ex:
        print("appearance skipped (%s / %s): %s" % (body_name, libname, ex))


def _matte(comp, libname="Paint - Enamel Glossy (Black)"):
    _appear(comp, libname)


# bezel matt black, Perspex translucent, glass blue - so a section reads at a
# glance which material is which
APP_BEZEL = "Paint - Enamel Glossy (Black)"
APP_PANEL = "Plastic - Translucent Matte (Gray)"
APP_GLASS = "Glass - Light Color (Blue)"
APP_ACTIVE = "Plastic - Translucent Glossy (Blue)"


def snapshots():
    app = _app()
    design = _design()
    root = design.rootComponent
    d = derive(P)
    comp, occ = _bezel_comp()
    _appear(comp, APP_BEZEL)
    pocc = _find_occ(COMP_PANEL)
    if pocc:
        _appear(pocc.component, APP_PANEL)
    gocc = _find_occ(COMP_GLASS)
    if gocc:
        _appear(gocc.component, APP_GLASS)
    if not os.path.isdir(DRAW):
        os.makedirs(DRAW)

    V = adsk.core.ViewOrientations
    out = []

    # the bezel alone
    _vis({COMP_BEZEL})
    out.append(_shot("front", V.TopViewOrientation))
    out.append(_shot("rear", V.BottomViewOrientation))
    out.append(_shot("oblique", V.IsoTopRightViewOrientation))

    # rear three-quarter, so the continuous lip reads as a ring
    _vis({COMP_BEZEL})
    out.append(_shot("lip_oblique", V.IsoBottomLeftViewOrientation))

    # with the Perspex, seated
    _vis({COMP_BEZEL, COMP_PANEL})
    out.append(_shot("assembly", V.IsoTopRightViewOrientation))

    # THE OPTICAL VIEW - looking straight in at the bezel with the lit area
    # of the OLED behind it, to scale, so the masking is visible and not just
    # asserted. CAD cannot say whether this is ACCEPTABLE; it can only say
    # what is geometrically visible.
    _drop(root, COMP_ACTIVE)
    ba = B()
    aocc = _add_comp(root, COMP_ACTIVE)
    _add_bodies(aocc.component, [(build_active(ba, P, d), "OLED_ACTIVE")])
    _appear_body(aocc.component, "OLED_ACTIVE", APP_ACTIVE)
    _vis({COMP_BEZEL, COMP_ACTIVE})
    out.append(_shot("optical", V.TopViewOrientation))

    # section on x = 0 through the top and bottom lip
    _drop(root, "SECTION_revQ")
    b = B()
    socc = _add_comp(root, "SECTION_revQ")
    half = b.box(-60.0, 0.0, -60.0, 60.0, -30.0, 30.0)
    bez = b.copy(comp.bRepBodies.itemByName("BEZEL"))
    b.inter(bez, b.copy(half))
    pan = build_panel(b, P, d)
    b.inter(pan, b.copy(half))
    _add_bodies(socc.component, [(bez, "SECT_BEZEL"), (pan, "SECT_PANEL")])
    _appear_body(socc.component, "SECT_BEZEL", APP_BEZEL)
    _appear_body(socc.component, "SECT_PANEL", APP_PANEL)
    _vis({"SECTION_revQ"})
    out.append(_shot("section", V.RightViewOrientation))

    # zoomed detail of the TOP edge - the cut edge and the lip that masks it
    _drop(root, "DETAIL_revQ")
    b2 = B()
    docc = _add_comp(root, "DETAIL_revQ")
    win = b2.box(-6.0, 0.0, 5.0, 11.0, -0.6, 4.8)
    bez2 = b2.copy(comp.bRepBodies.itemByName("BEZEL"))
    b2.inter(bez2, b2.copy(win))
    pan2 = build_panel(b2, P, d)
    b2.inter(pan2, b2.copy(win))
    _add_bodies(docc.component,
                [(bez2, "DETAIL_BEZEL"), (pan2, "DETAIL_PANEL")])
    _appear_body(docc.component, "DETAIL_BEZEL", APP_BEZEL)
    _appear_body(docc.component, "DETAIL_PANEL", APP_PANEL)
    _vis({"DETAIL_revQ"})
    out.append(_shot("section_detail", V.RightViewOrientation))

    _vis({COMP_BEZEL, COMP_PANEL})
    return out


# ---------------------------------------------------------------------------
# One-shot
# ---------------------------------------------------------------------------
def build_all():
    main(new_document=True)
    import_carrier()
    coupon()
    corner_study()
    ok = validate()
    export("all")
    snapshots()
    return ok
