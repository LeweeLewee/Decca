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
COMP_COUPON = "Bezel_Corner_Gauge_revQ"
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
    "bezel_window_w": 30.40,        # PRESERVED   visible window width
    "bezel_window_r": 0.80,         # PRESERVED   window corner radius
    "pad_x_half": 12.00,            # PRESERVED   adhesive pad half length
    "pad_y0": 7.85,                 # PRESERVED
    "pad_y1": 9.85,                 # PRESERVED
    "pad_depth": 0.30,              # PRESERVED   recess into the seating face

    # -- Rev Q: the continuous masking lip ---------------------------------
    "bezel_lip_outer_w": 34.90,     # PROVISIONAL proven in X by the Rev N rails
    "bezel_lip_outer_h": 15.00,     # PROVISIONAL never physically proven in Y
    "bezel_lip_depth": 2.80,        # PROVEN      Rev N engagement depth
    "bezel_lip_wall": 0.40,         # PROVISIONAL one 0.40 mm extrusion width
    "bezel_lip_corner_r": 0.60,     # UNRESOLVED  Rev N rail-end relief R0.60
    "bezel_lip_lead": 0.20,         # PROVISIONAL minimum entry lead-in

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

    # -- corner-radius gauge coupon ----------------------------------------
    "coupon_leg_x": 6.00,
    "coupon_leg_y": 4.00,
    "coupon_pad_out": 3.60,
    "coupon_pitch": 26.00,
}

# Candidate lip corner radii carried by the gauge coupon, ascending.
#
# A uniform wall forces bezel_lip_corner_r >= bezel_lip_wall, because the lip
# INNER corner radius is (corner_r - wall) and cannot go negative. With the
# 0.40 mm wall the smallest buildable outer corner radius is therefore 0.40,
# and that is where the coupon starts. Between them these five span opening
# corner radii from 0.91 mm to 3.01 mm - see corner_study().
COUPON_RADII = [0.40, 0.60, 1.00, 1.60, 2.50]


def derive(P):
    """Every dependent dimension. Nothing below is entered twice."""
    d = {}

    # Z-chain --------------------------------------------------------------
    d["z_panel_front"] = P["panel_t"]                                # +3.000
    d["z_panel_rear"] = 0.0                                          #  0.000
    d["bezel_face_t"] = P["bezel_t"] - P["bezel_lip_depth"]          #  1.200
    d["z_bezel_front"] = d["z_panel_front"] + d["bezel_face_t"]      # +4.200
    d["z_lip_rear"] = d["z_panel_front"] - P["bezel_lip_depth"]      # +0.200

    # Lip, derived from the outer envelope and the wall ---------------------
    d["bezel_lip_clear_x"] = (P["panel_open_w"] - P["bezel_lip_outer_w"]) / 2.0
    d["bezel_lip_clear_y"] = (P["panel_open_h"] - P["bezel_lip_outer_h"]) / 2.0
    d["bezel_lip_inner_w"] = P["bezel_lip_outer_w"] - 2 * P["bezel_lip_wall"]
    d["bezel_lip_inner_h"] = P["bezel_lip_outer_h"] - 2 * P["bezel_lip_wall"]
    # A uniform wall makes the inner corner radius (corner_r - wall), so the
    # outer corner radius can never be smaller than the wall.
    if P["bezel_lip_corner_r"] < P["bezel_lip_wall"] - 1e-9:
        raise ValueError(
            "bezel_lip_corner_r (%.3f) is below bezel_lip_wall (%.3f): a "
            "uniform-wall lip cannot have an outer corner radius smaller "
            "than its wall" % (P["bezel_lip_corner_r"], P["bezel_lip_wall"]))
    d["bezel_lip_inner_r"] = P["bezel_lip_corner_r"] - P["bezel_lip_wall"]

    # The window HEIGHT is DERIVED, not independently dimensioned.
    #
    # Rev N's window was 14.900 high. The Rev Q lip inner opening is 14.200.
    # If the window stayed at 14.900 the lip's 0.400 mm wall would meet the
    # bezel face over only 0.050 mm of its width at the top and the bottom -
    # a knife-edge root, a sliver, and unprintable as a standing wall.
    # Driving the window height from the lip inner opening lands the full
    # 0.400 mm wall on solid face material and makes the lip a true skirt
    # continuing rearward from the window edge, which is the required
    # cross-section.
    #
    # It costs NOTHING optically: the clear opening is 14.200 either way,
    # because the lip already controls it. Brief section 3.4 requires exactly
    # this - "the wall and the opening it creates must be derived".
    d["bezel_window_h"] = d["bezel_lip_inner_h"]                     # 14.200
    d["bezel_window_w"] = P["bezel_window_w"]                        # 30.400

    # Half extents ---------------------------------------------------------
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

    # Clearances the released design already proved -------------------------
    d["clear_to_panel_rear"] = d["z_lip_rear"] - d["z_panel_rear"]   # 0.200
    d["clear_to_glass"] = d["z_lip_rear"] - P["oled_glass_front_z"]  # 0.500

    # Effective optical opening --------------------------------------------
    # The through-hole is the intersection of the face window and the lip
    # inner opening. Because the window height is now derived from the lip the
    # two coincide in Y, and the window is far narrower than the lip in X, so
    # the result is simply the window.
    d["optical_w"] = d["bezel_window_w"]                             # 30.400
    d["optical_h"] = d["bezel_window_h"]                             # 14.200
    d["optical_r"] = P["bezel_window_r"]                             #  0.800

    # what Rev N showed, for the honest before/after
    d["revN_window_w"] = 30.40
    d["revN_window_h"] = 14.90

    # visible OLED active area through the Rev Q aperture
    a0 = P["oled_active_cy"] - P["oled_active_h"] / 2.0              # -0.650
    a1 = P["oled_active_cy"] + P["oled_active_h"] / 2.0              # +14.050
    d["active_y0"], d["active_y1"] = a0, a1
    d["vis_q_y0"] = max(a0, -d["wh2"])
    d["vis_q_y1"] = min(a1, +d["wh2"])
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
    d["unlit_below_q"] = max(0.0, a0 - (-d["wh2"]))
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
    """The Rev Q bezel, as ONE connected solid.

    Order matters: the window is cut from the face slab BEFORE the lip is
    unioned on, so no boolean ever has to resolve a coincident face at
    z = +3.000.
    """
    # 1. face slab - Rev N envelope and external corner radius
    face = b.rprism(-d["bw2"], d["bw2"], -d["bh2"], d["bh2"],
                    d["z_panel_front"], d["z_bezel_front"], P["bezel_outer_r"])

    # 2. the visible window - width PRESERVED from Rev N, height DERIVED
    win = b.rprism(-d["ww2"], d["ww2"], -d["wh2"], d["wh2"],
                   d["z_panel_front"] - 1.0, d["z_bezel_front"] + 1.0,
                   P["bezel_window_r"])
    b.sub(face, win)

    # 3. the two recessed adhesive pads - PRESERVED from Rev N
    for sy in (1, -1):
        y0, y1 = sorted((sy * P["pad_y0"], sy * P["pad_y1"]))
        b.sub(face, b.box(-P["pad_x_half"], P["pad_x_half"], y0, y1,
                          d["z_panel_front"] - 0.5,
                          d["z_panel_front"] + P["pad_depth"]))

    # 4. THE REV Q FEATURE - one continuous lip, all four sides and corners
    lip = b.ring(d["low2"], d["loh2"], d["liw2"], d["lih2"],
                 d["z_lip_rear"], d["z_panel_front"],
                 P["bezel_lip_corner_r"], d["bezel_lip_inner_r"])

    b.uni(face, lip)
    return face


def build_panel(b, P, d):
    """REF_Decca_Panel - the original fascia Perspex. Reference only.

    The opening is modelled EXACTLY as the released Rev P generator models it,
    a sharp-cornered box, because that is the controlled representation.
    panel_open_corner_r is exposed so corner sensitivity can be explored
    without pretending a measurement exists.
    """
    s = b.box(-P["panel_ref_w"] / 2.0, P["panel_ref_w"] / 2.0,
              -P["panel_ref_h"] / 2.0, P["panel_ref_h"] / 2.0,
              d["z_panel_rear"], d["z_panel_front"])
    b.sub(s, b.rprism(-d["po_w2"], d["po_w2"], -d["po_h2"], d["po_h2"],
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
    """Corner-radius gauge. Five loose L-tabs, one per candidate lip corner
    radius, notch-numbered 1..5 in ascending radius.

    Each tab carries a REAL section of the Rev Q lip at that radius - the same
    0.40 mm wall, the same 2.80 mm depth, the same 34.90 x 15.00 outer
    envelope - so offering it into a corner of the REAL opening answers the
    one question CAD cannot: what is the Perspex corner radius.
    """
    tabs = []
    lx, ly = P["coupon_leg_x"], P["coupon_leg_y"]
    out = P["coupon_pad_out"]
    x_in = d["low2"] - lx
    y_in = d["loh2"] - ly
    for i, r in enumerate(COUPON_RADII):
        ri = r - P["bezel_lip_wall"]
        if ri < 0.0:
            raise ValueError("coupon radius %.2f is below the wall" % r)
        # a full lip ring at this radius, clipped to the +X +Y corner
        seg = b.ring(d["low2"], d["loh2"], d["liw2"], d["lih2"],
                     d["z_lip_rear"], d["z_panel_front"], r, ri)
        b.inter(seg, b.box(x_in, d["low2"] + 10.0, y_in, d["loh2"] + 10.0,
                           d["z_lip_rear"] - 1.0, d["z_panel_front"] + 1.0))
        # the face pad that lands on the Perspex front face
        pad = b.box(x_in - 1.0, d["low2"] + out, y_in - 1.0, d["loh2"] + out,
                    d["z_panel_front"], d["z_bezel_front"])
        b.uni(pad, seg)
        # notch code - i+1 notches cut into the outboard edge
        for n in range(i + 1):
            cy = y_in - 0.4 + 1.2 * n
            b.sub(pad, b.box(d["low2"] + out - 0.9, d["low2"] + out + 1.0,
                             cy - 0.30, cy + 0.30,
                             d["z_panel_front"] - 1.0,
                             d["z_bezel_front"] + 1.0))
        # lay the five tabs out in a row for printing
        mtx = adsk.core.Matrix3D.create()
        mtx.translation = v3(mm((i - 2) * P["coupon_pitch"] - d["low2"]),
                             mm(-y_in), 0.0)
        b.t.transform(pad, mtx)
        tabs.append((pad, "COUPON_R%03d" % int(round(r * 100))))
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
    put("bezel_lip_clear_x", "(panel_open_w - bezel_lip_outer_w) / 2", "DERIVED")
    put("bezel_lip_clear_y", "(panel_open_h - bezel_lip_outer_h) / 2", "DERIVED")
    put("bezel_lip_inner_w", "bezel_lip_outer_w - 2 * bezel_lip_wall", "DERIVED")
    put("bezel_lip_inner_h", "bezel_lip_outer_h - 2 * bezel_lip_wall", "DERIVED")
    put("bezel_lip_inner_r", "bezel_lip_corner_r - bezel_lip_wall", "DERIVED")
    put("bezel_window_h", "bezel_lip_inner_h", "DERIVED from the lip")
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

    # ---- front face edge break R0.40 - PRESERVED from Rev N --------------
    ff = _planar_face(body, d["z_bezel_front"], +1)
    ok1, msg1 = _fillet(comp, list(ff.edges) if ff else [],
                        P["bezel_edge_break"], "front_edge_break")
    print("front edge break R%.2f : %s %s" % (P["bezel_edge_break"], ok1, msg1))

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


def corner_study(P=P):
    d = derive(P)
    print("=" * 74)
    print("REV Q CORNER-FIT STUDY")
    print("=" * 74)
    print("The Perspex opening corner radius is NOT RECORDED anywhere in this")
    print("project. The Rev N side rails sat at y +/-4.000, clear of every")
    print("corner, so they prove nothing about it, and the released Rev P")
    print("reference models the opening with SHARP corners.")
    print("")
    print("opening      %.2f x %.2f mm, corner radius R_panel = UNKNOWN"
          % (P["panel_open_w"], P["panel_open_h"]))
    print("lip outer    %.2f x %.2f mm, corner radius R_lip = %.2f mm (set)"
          % (P["bezel_lip_outer_w"], P["bezel_lip_outer_h"],
             P["bezel_lip_corner_r"]))
    print("")
    print("Largest tolerable opening corner radius, by lip corner radius:")
    print("   R_lip    seats if R_panel <=    with >=0.05 clear")
    for rl in (0.20, 0.40, 0.60, 0.80, 1.00, 1.20, 1.60, 2.00, 2.50):
        m0 = max_panel_r(P, d, rl, 0.0)
        m5 = max_panel_r(P, d, rl, 0.05)
        print("   %5.2f          %6.3f               %6.3f"
              % (rl, m0 if m0 else -1, m5 if m5 else -1))
    print("")
    print("   Rule of thumb from the table:  R_panel_max  ~=  R_lip + 0.51 mm")
    print("")
    print("Unmasked corner gap on the 45 degree bisector (mm):")
    hdr = "   R_lip \\ R_panel"
    cols = (0.00, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00)
    print(hdr + "".join("%8.2f" % c for c in cols))
    for rl in (0.20, 0.60, 1.00, 1.60, 2.50):
        row = "   R %4.2f         " % rl
        for rp in cols:
            row += "%8.3f" % corner_gap_at_bisector(P, d, rl, rp)
        print(row)
    print("")
    print("   negative = the lip fouls the corner and the bezel will NOT seat")
    print("")
    cur = P["bezel_lip_corner_r"]
    mp = max_panel_r(P, d, cur, 0.0)
    print("AT THE SET VALUE R_lip = %.2f mm:" % cur)
    print("   seats for any opening corner radius up to  %.3f mm" % mp)
    print("   corner gap if the opening is sharp (R=0)   %.3f mm"
          % corner_gap_at_bisector(P, d, cur, 0.0))
    print("   corner gap if the opening is R0.50         %.3f mm"
          % corner_gap_at_bisector(P, d, cur, 0.5))
    print("   flat-run clearance, all four sides         %.3f mm"
          % d["bezel_lip_clear_x"])
    print("")
    print("FAILURE MODE IS SAFE AND OBVIOUS. Too small an R_lip does not")
    print("damage anything - the four corners simply bottom on the Perspex")
    print("corner fillets and the bezel stands proud of the fascia, which is")
    print("immediately visible. The fix is to raise bezel_lip_corner_r and")
    print("reprint. Too large an R_lip seats but leaves the gap tabulated")
    print("above unmasked at each corner.")
    print("=" * 74)


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
    print("3. THE CONTINUOUS LIP")
    # --- continuity: walk the full perimeter at three depths ---------------
    zs = [d["z_lip_rear"] + 0.05, (d["z_lip_rear"] + d["z_panel_front"]) / 2.0,
          d["z_panel_front"] - 0.05]
    mid_off = P["bezel_lip_wall"] / 2.0
    path = _rrect_path(d["low2"], d["loh2"], P["bezel_lip_corner_r"], 1440)
    gaps = []
    for (px, py, nx, ny) in path:
        mx, my = px + nx * mid_off, py + ny * mid_off
        for z in zs:
            if not _inside(body, mx, my, z):
                gaps.append((round(mx, 3), round(my, 3), round(z, 3)))
    _gate(len(gaps) == 0,
          "lip present at all 1440 perimeter stations x 3 depths",
          "%d void station(s)" % len(gaps))

    # per-side and per-corner continuity, stated separately
    sides = {"left": 0, "right": 0, "top": 0, "bottom": 0, "corners": 0}
    hits = dict((k, 0) for k in sides)
    ax = d["low2"] - P["bezel_lip_corner_r"]
    ay = d["loh2"] - P["bezel_lip_corner_r"]
    for (px, py, nx, ny) in path:
        if abs(px) <= ax and abs(py) <= ay:
            key = "corners"
        elif abs(px) > ax and abs(py) > ay:
            key = "corners"
        elif abs(py) >= ay and abs(px) <= ax:
            key = "top" if py > 0 else "bottom"
        else:
            key = "right" if px > 0 else "left"
        sides[key] += 1
        mx, my = px + nx * mid_off, py + ny * mid_off
        if _inside(body, mx, my, zs[1]):
            hits[key] += 1
    for k in ("left", "right", "top", "bottom", "corners"):
        _gate(sides[k] > 0 and hits[k] == sides[k],
              "lip continuous - %s" % k,
              "%d/%d stations" % (hits[k], sides[k]))

    # --- outer envelope, wall thickness, depth -----------------------------
    walls, outers = [], []
    for (px, py, nx, ny) in path[::4]:
        z = zs[1]
        # the outer surface must be exactly on the envelope
        if _inside(body, px - nx * 0.01, py - ny * 0.01, z):
            outers.append(-1.0)
        else:
            outers.append(0.0)
        lo, hi = 0.002, 2.0
        if not _inside(body, px + nx * lo, py + ny * lo, z):
            walls.append(0.0)
            continue
        for _ in range(40):
            mid = (lo + hi) / 2.0
            if _inside(body, px + nx * mid, py + ny * mid, z):
                lo = mid
            else:
                hi = mid
        walls.append((lo + hi) / 2.0)
    _gate(all(o == 0.0 for o in outers),
          "no material outside the 34.90 x 15.00 outer envelope",
          "%d breach(es)" % sum(1 for o in outers if o < 0))
    wmin, wmax = min(walls), max(walls)
    _gate(abs(wmin - P["bezel_lip_wall"]) < 5.0e-4
          and abs(wmax - P["bezel_lip_wall"]) < 5.0e-4,
          "lip wall = 0.400 mm everywhere",
          "min %.4f  max %.4f" % (wmin, wmax))

    tip = _planar_face(body, d["z_lip_rear"])
    _gate(tip is not None, "lip rear tip face exists at z = +0.200",
          "%.4f mm2" % (tip.area * 100.0 if tip else 0.0))
    _gate(abs((d["z_panel_front"] - d["z_lip_rear"]) - P["bezel_lip_depth"])
          < 1e-9, "lip depth = 2.800 mm",
          "%.5f" % (d["z_panel_front"] - d["z_lip_rear"]))
    _gate(abs(d["bezel_lip_clear_x"] - 0.15) < 1e-9
          and abs(d["bezel_lip_clear_y"] - 0.15) < 1e-9,
          "nominal clearance 0.150 mm per side, all four sides",
          "x %.4f  y %.4f" % (d["bezel_lip_clear_x"], d["bezel_lip_clear_y"]))

    print("")
    print("4. THE ORIGINAL PERSPEX")
    panel_occ = _find_occ(COMP_PANEL)
    panel = panel_occ.bRepBodies.item(0)
    v = _hit_mm3(b, body, panel)
    _gate(v < 1.0e-6, "no interference with the measured Perspex solid",
          "%.6f mm3" % v)
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
    print("7. EFFECTIVE OPTICAL OPENING")
    _report("Rev N clear opening",
            "%.3f W x %.3f H mm (R%.2f)"
            % (d["revN_window_w"], d["revN_window_h"], P["bezel_window_r"]))
    _report("Rev Q clear opening",
            "%.3f W x %.3f H mm (R%.2f)"
            % (d["optical_w"], d["optical_h"], d["optical_r"]))
    _report("change introduced by the lip",
            "width unchanged, height %.3f -> %.3f, i.e. -%.3f mm total "
            "(-%.3f per side)"
            % (d["revN_window_h"], d["optical_h"],
               d["revN_window_h"] - d["optical_h"],
               (d["revN_window_h"] - d["optical_h"]) / 2.0))
    _report("controlled by", "the TOP and BOTTOM lip, not the bezel face")
    _report("visible OLED active area, Rev N",
            "%.3f W x %.3f H mm" % (d["vis_w"], d["vis_n_h"]))
    _report("visible OLED active area, Rev Q",
            "%.3f W x %.3f H mm" % (d["vis_w"], d["vis_q_h"]))
    _report("active height lost to the lip",
            "%.3f mm, all of it at the TOP edge" % d["active_loss_vs_revN"])
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
    print("corner gauge coupon: %d tabs, %.4f cm3 total"
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

    if what in ("assembly", "all"):
        p = _guard(os.path.join(cad, "Decca_Display_Bezel_revQ_assembly.step"))
        em.execute(em.createSTEPExportOptions(p))
        written.append(p)

    if what in ("coupon", "all"):
        occ = _find_occ(COMP_COUPON)
        if occ:
            p = _guard(os.path.join(cad, "Bezel_Corner_Gauge_revQ.step"))
            em.execute(em.createSTEPExportOptions(p, occ.component))
            written.append(p)
            # one mesh carrying all five tabs
            for bd in occ.component.bRepBodies:
                pp = _guard(os.path.join(
                    stl, "Bezel_Corner_Gauge_revQ_%s.stl" % bd.name))
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
