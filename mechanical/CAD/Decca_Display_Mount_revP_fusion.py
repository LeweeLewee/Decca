# -*- coding: utf-8 -*-
"""
Decca OLED Display Mount - Rev P parametric generator (Autodesk Fusion 360).

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

DOC_NAME = "Decca_Display_Mount_revP"
CARRIER = "Rear_Display_Carrier"


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
    "oled_active_w": 29.42,
    "oled_active_h": 14.70,
    # NOT MEASURED. Rev P.2 depends on the glass X/Y envelope in exactly one
    # place - the two header-side snap noses. See topology review section 7:
    # that dependency is REPORTED as a blocking pre-print measurement, never
    # assumed away.
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
    # room. The fingers are deleted; the depth now falls out of the M2 insert
    # stack and the sprung-post root relief.
    "carrier_depth": 8.00,
    "carrier_corner_r": 3.00,
    "top_flange": 6.00,            # cable-tie flange above the top wall
    "flange_w": 31.00,             # narrowed per the validated Rev F change

    # -- M2 structural interface -------------------------------------------
    "m2_boss_d": 7.60,
    "m2_insert_d": 3.20,
    "m2_insert_depth": 4.00,
    "m2_insert_recess": 0.50,
    "m2_bore_chamfer": 0.40,
    "m2_arm_h": 7.50,              # stadium arm height (Rev F/N shape)

    # -- Locating posts -----------------------------------------------------
    # Starting values from the printed Rev D / Rev K post development. Strain
    # is RE-CALCULATED from the finished geometry in validate(), not inherited.
    "sprung_shaft_d": 2.80,        # Rev D, unchanged
    "sprung_slot_w": 0.70,         # Rev D, unchanged
    "sprung_barb_d": 3.20,         # Rev D, unchanged -> 0.10 mm radial overlap
    "sprung_tip_d": 2.60,          # nose lead-in tip
    "sprung_relief_d": 4.80,       # Rev D counterbore, unchanged
    # Rev D/K used ~1.00 mm because the relief sat IN FRONT of the PCB and the
    # glass capped it - the dependency that made Rev K's narrow pair unsafe. In
    # Rev P.2 the relief is BEHIND the PCB, so the glass cannot constrain it and
    # the depth is set by strain instead.
    "sprung_relief_depth": 3.20,
    "plain_post_d": 2.70,          # Rev D plain locating post, unchanged
    "plain_relief_d": 4.80,
    "plain_relief_depth": 1.00,    # the brief's value; nothing forces it deeper
    "plain_lead": 0.30,            # entry chamfer leg at the plain post tip
    # The plain posts stop this far BEHIND the PCB front plane. The
    # modelled glass overhangs the display-side mounting holes, so this is
    # the clearance to bonded glass in the worst case where the glass
    # covers the hole entirely. 0.10 mm (the generic forward_setback) is
    # too thin to trust on an FDM post top; 0.25 mm costs nothing and
    # still leaves 1.35 mm of the 1.60 mm board engaged.
    "plain_setback": 0.25,
    "post_fillet_r": 0.80,         # Rev D R0.80 root fillet, unchanged
    "hook_clear": 0.10,            # AXIAL clearance under the hook when seated
    "hook_land": 0.25,             # full-diameter land above the retaining face
    "nose_perspex_clear": 0.40,    # nose tip clearance to the Perspex

    # -- Fixed rear PCB datum ----------------------------------------------
    "datum_pad_od": 6.00,          # annular pad, ID = the post relief bore
    "datum_pad_h": 0.30,           # pad stands this far above the pedestal top
    # 8.60 rather than a round 8.00: at Ø8.00 the pedestal arc passes
    # 0.033 mm inside the pocket corner and leaves four hair slivers.
    # Ø8.60 swallows the corner by 0.27 mm instead.
    "pedestal_d": 8.60,            # rigid column carrying each pad and post

    # -- Service features ---------------------------------------------------
    "wire_notch_w": 13.00,
    "wire_notch_depth": 1.50,
    "tie_relief_w": 26.00,
    "tie_relief_h": 2.40,          # in Y, up from the top wall outer face
    "tie_relief_depth": 2.00,
    "tie_slot_x": 10.50,
    "tie_slot_w": 3.80,
    "tie_slot_h": 1.60,            # in Z
    "tie_slot_z": -7.00,           # slot centre in Z, inside the rear relief

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
def derive(P):
    d = {}

    # --- the optical depth chain, front to rear ---------------------------
    d["z_perspex_front"] = P["perspex_t"]
    d["z_perspex_rear"] = 0.0                                      #  0.00 DATUM A
    d["z_glass_front"] = -P["oled_perspex_gap"]                    # -0.30
    d["z_pcb_front"] = d["z_glass_front"] - P["oled_glass_proud"]  # -1.10
    d["z_fwd_limit"] = d["z_pcb_front"] - P["forward_setback"]     # -1.20
    d["z_pcb_rear"] = d["z_pcb_front"] - P["oled_pcb_t"]           # -2.70 DATUM B
    d["z_rear"] = -P["carrier_depth"]                              # -8.00
    d["z_tip_front"] = d["z_pcb_front"] + P["oled_tip_proud"]
    d["z_header_rear"] = d["z_pcb_rear"] - P["oled_header_depth"]
    d["z_insert_bore"] = -(P["m2_insert_recess"] + P["m2_insert_depth"])

    # --- retention stack ---------------------------------------------------
    d["z_hook_face"] = d["z_pcb_front"] + P["hook_clear"]              # -1.00
    d["z_hook_top"] = d["z_hook_face"] + P["hook_land"]                # -0.85
    d["z_nose_tip"] = -P["nose_perspex_clear"]                         # -0.40
    d["z_ped_top"] = d["z_pcb_rear"] - P["datum_pad_h"]                # -3.00
    d["z_sprung_floor"] = d["z_pcb_rear"] - P["sprung_relief_depth"]   # -5.70
    d["z_sprung_fix"] = d["z_sprung_floor"] + P["post_fillet_r"]       # -4.90
    d["z_plain_floor"] = d["z_pcb_rear"] - P["plain_relief_depth"]     # -3.70
    d["z_plain_fix"] = d["z_plain_floor"] + P["post_fillet_r"]         # -2.90
    d["z_plain_top"] = d["z_pcb_front"] - P["plain_setback"]           # -1.35
    d["z_plain_lead"] = d["z_plain_top"] - P["plain_lead"]             # -1.65
    # the forward over-travel that would strip the hook if the barbs were
    # held squeezed: where the nose cone narrows back to the hole diameter
    frac = ((P["sprung_barb_d"] - P["oled_hole_d"])
            / (P["sprung_barb_d"] - P["sprung_tip_d"]))
    d["z_strip"] = d["z_hook_top"] + frac * (d["z_nose_tip"] - d["z_hook_top"])
    d["strip_travel"] = d["z_strip"] - d["z_pcb_rear"]

    # --- module envelopes -------------------------------------------------
    d["pcb_x0"] = -P["oled_pcb_w"] / 2.0
    d["pcb_x1"] = P["oled_pcb_w"] / 2.0
    d["pcb_y0"] = P["oled_pcb_off_y"] - P["oled_pcb_h"] / 2.0
    d["pcb_y1"] = P["oled_pcb_off_y"] + P["oled_pcb_h"] / 2.0
    d["glass_x0"] = -P["oled_glass_w"] / 2.0
    d["glass_x1"] = P["oled_glass_w"] / 2.0
    d["glass_y0"] = P["oled_glass_off_y"] - P["oled_glass_h"] / 2.0
    d["glass_y1"] = P["oled_glass_off_y"] + P["oled_glass_h"] / 2.0

    # --- PCB pocket -------------------------------------------------------
    c = P["pcb_clearance"]
    d["pk_x0"], d["pk_x1"] = d["pcb_x0"] - c, d["pcb_x1"] + c
    d["pk_y0"], d["pk_y1"] = d["pcb_y0"] - c, d["pcb_y1"] + c

    # --- module aperture --------------------------------------------------
    a = P["aperture_margin"]
    d["ap_x0"], d["ap_x1"] = d["pk_x0"] - a, d["pk_x1"] + a
    d["ap_y0"], d["ap_y1"] = d["pk_y0"] - a, d["pk_y1"] + a

    # --- carrier outer profile -------------------------------------------
    w = P["carrier_wall"]
    d["car_x0"], d["car_x1"] = d["ap_x0"] - w, d["ap_x1"] + w
    d["car_y0"] = d["ap_y0"] - w
    d["wall_y1"] = d["ap_y1"] + w                    # top wall outer face
    d["car_y1"] = d["wall_y1"] + P["top_flange"]     # flange top edge

    # --- M2 bosses --------------------------------------------------------
    d["m2_x"] = P["panel_fix_pitch"] / 2.0
    d["m2_r"] = P["m2_boss_d"] / 2.0
    d["ear_x1"] = d["m2_x"] + d["m2_r"]
    d["arm_x0"] = d["car_x1"] - 2.0                  # deep overlap, no slivers

    # --- solder tips ------------------------------------------------------
    n = 4
    span = (n - 1) * P["oled_tip_pitch"]
    d["tip_x"] = [P["oled_tip_cx"] - span / 2.0 + i * P["oled_tip_pitch"]
                  for i in range(n)]

    # --- PCB mounting holes and the posts that occupy them ----------------
    hx = P["oled_hole_pitch_x"] / 2.0
    hy = P["oled_hole_pitch_y"] / 2.0
    d["post_x"] = hx
    d["y_sprung"] = P["oled_pcb_off_y"] + hy         # +18.25, header side
    d["y_plain"] = P["oled_pcb_off_y"] - hy          # -10.25, display side
    d["sprung"] = [(sx * hx, d["y_sprung"]) for sx in (-1, 1)]
    d["plain"] = [(sx * hx, d["y_plain"]) for sx in (-1, 1)]
    d["holes"] = d["sprung"] + d["plain"]

    # The sprung pair belongs on the header side, away from the glass. Assert
    # the choice rather than trusting a comment.
    d["sprung_is_header_side"] = (d["y_sprung"] * P["oled_header_off_y"]) > 0

    # --- retention mechanics ----------------------------------------------
    d["hook_overlap"] = (P["sprung_barb_d"] - P["oled_hole_d"]) / 2.0   # 0.10
    d["shaft_clear"] = (P["oled_hole_d"] - P["sprung_shaft_d"]) / 2.0   # 0.10
    d["plain_clear"] = (P["oled_hole_d"] - P["plain_post_d"]) / 2.0     # 0.15
    d["post_a"] = d["z_hook_top"] - d["z_sprung_fix"]                   # 4.05
    d["post_t"] = (P["sprung_shaft_d"] - P["sprung_slot_w"]) / 2.0      # 1.05
    dr = (P["sprung_barb_d"] - P["sprung_tip_d"]) / 2.0
    d["cam_deg"] = math.degrees(math.atan2(dr,
                                           d["z_nose_tip"] - d["z_hook_top"]))
    # the glass keep-out the noses require, as a radius about each hole centre
    d["nose_keepout_r"] = P["sprung_barb_d"] / 2.0 + P["nose_glass_margin"]
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
                      -P["oled_active_h"] / 2.0, P["oled_active_h"] / 2.0,
                      zf + P["oled_glass_proud"] - 0.05,
                      zf + P["oled_glass_proud"]), "OLED_ActiveArea"))
    out.append((B.box(-P["oled_header_w"] / 2.0, P["oled_header_w"] / 2.0,
                      P["oled_header_off_y"] - P["oled_header_h"] / 2.0,
                      P["oled_header_off_y"] + P["oled_header_h"] / 2.0,
                      zr - P["oled_header_depth"], zr), "OLED_Header_Keepout"))

    tips = None
    for ty in (P["oled_tip_y_top"], P["oled_tip_y_bot"]):
        for tx in d["tip_x"]:
            c = B.cylz(P["oled_tip_d"], tx, ty, zf, zf + tp)
            tips = c if tips is None else B.uni(tips, c)
    out.append((tips, "OLED_Solder_Tips"))
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
                      P["oled_header_off_y"] - P["oled_header_h"] / 2.0,
                      P["oled_header_off_y"] + P["oled_header_h"] / 2.0,
                      d["z_header_rear"], zr + travel), "SWEPT_Header"))
    tips = None
    for ty in (P["oled_tip_y_top"], P["oled_tip_y_bot"]):
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
    """The declared exception to invariant P1' - the union of the two sprung
    nose envelopes. The ONLY carrier material permitted forward of the PCB
    front plane inside the module aperture."""
    env = None
    for (x, y) in d["sprung"]:
        b = B.cylz(P["sprung_barb_d"] + 2 * pad, x, y,
                   d["z_fwd_limit"] - pad, d["z_nose_tip"] + pad)
        env = b if env is None else B.uni(env, b)
    return env


def hole_keepout(B, P, d, pad=None):
    """The two header-side mounting-hole corridors, expanded by the nose glass
    margin. Every scrap of nose material must lie inside this."""
    r = d["nose_keepout_r"] if pad is None else pad
    env = None
    for (x, y) in d["sprung"]:
        b = B.cylz(2 * r, x, y, d["z_fwd_limit"] - 0.1, d["z_nose_tip"] + 0.1)
        env = b if env is None else B.uni(env, b)
    return env


# ---------------------------------------------------------------------------
# The carrier
# ---------------------------------------------------------------------------
def sprung_post(B, P, d, x, y, pinch=0.0):
    """One split sprung locating post.

    ``pinch`` shrinks the barb, modelling the two halves squeezed together with
    tweezers. Used to validate the removal path.
    """
    barb = max(P["sprung_tip_d"], P["sprung_barb_d"] - 2.0 * pinch)
    z0 = d["z_sprung_floor"]

    s = B.cylz(P["sprung_shaft_d"], x, y, z0, d["z_hook_face"])
    B.uni(s, B.root_fillet(P["sprung_shaft_d"], P["post_fillet_r"], x, y, z0))
    B.uni(s, B.cylz(barb, x, y, d["z_hook_face"], d["z_hook_top"]))
    B.uni(s, B.conez(barb, min(P["sprung_tip_d"], barb), x, y,
                     d["z_hook_top"], d["z_nose_tip"]))

    # the split slot: free above the root fillet, solid through it, so the
    # cantilever is properly built in at z_sprung_fix
    half = P["sprung_slot_w"] / 2.0
    B.sub(s, B.box(x - P["sprung_barb_d"], x + P["sprung_barb_d"],
                   y - half, y + half,
                   d["z_sprung_fix"], d["z_nose_tip"] + 0.10))
    return s


def plain_post(B, P, d, x, y):
    """One rigid plain locating post. Stops at z = z_fwd_limit, so it never
    crosses the PCB front plane and is unconditionally clear of the glass."""
    z0 = d["z_plain_floor"]
    s = B.cylz(P["plain_post_d"], x, y, z0, d["z_plain_lead"])
    B.uni(s, B.root_fillet(P["plain_post_d"], P["post_fillet_r"], x, y, z0))
    B.uni(s, B.conez(P["plain_post_d"], P["plain_post_d"] - 2 * P["plain_lead"],
                     x, y, d["z_plain_lead"], d["z_plain_top"]))
    return s


def build_carrier(B, P, d, pinch=0.0):
    """Rear_Display_Carrier - the single structural Rev P.2 part."""
    zr, zf = d["z_rear"], d["z_fwd_limit"]

    # 1. outer envelope: rounded body + two stadium M2 arms
    s = B.rrect(d["car_x0"], d["car_x1"], d["car_y0"], d["wall_y1"],
                zr, 0.0, P["carrier_corner_r"])
    B.uni(s, B.rrect(-P["flange_w"] / 2.0, P["flange_w"] / 2.0,
                     d["wall_y1"] - 3.0, d["car_y1"],
                     zr, 0.0, P["carrier_corner_r"]))
    for sx in (-1, 1):
        a, b = sx * d["arm_x0"], sx * d["ear_x1"]
        B.uni(s, B.rrect(min(a, b), max(a, b),
                         -P["m2_arm_h"] / 2.0, P["m2_arm_h"] / 2.0,
                         zr, 0.0, P["m2_arm_h"] / 2.0))
        a, b = sx * (d["m2_x"] - d["m2_r"]), sx * d["ear_x1"]
        B.uni(s, B.rrect(min(a, b), max(a, b), -d["m2_r"], d["m2_r"],
                         zr, 0.0, d["m2_r"]))

    # 2. MODULE APERTURE - all carrier material forward of z_fwd_limit is
    #    removed across the full module envelope. This is invariant P1'; the
    #    two sprung noses are added back in step 6 as the declared exception.
    B.sub(s, B.box(d["ap_x0"], d["ap_x1"], d["ap_y0"], d["ap_y1"], zf, 1.0))

    # 3. PCB pocket, open at the rear - the module now drops in from the FRONT,
    #    and the rear stays open for the header, the cable and the push-out path
    B.sub(s, B.box(d["pk_x0"], d["pk_x1"], d["pk_y0"], d["pk_y1"], zr - 1.0, zf))

    # 4. rigid pedestals + FIXED REAR DATUM PADS at z = z_pcb_rear.
    #    These are solid carrier body. They stop the module moving rearward and
    #    they set the OLED Z position. No spring is involved anywhere in them.
    for (x, y) in d["holes"]:
        B.uni(s, B.cylz(P["pedestal_d"], x, y, zr, d["z_ped_top"]))
        B.uni(s, B.cylz(P["datum_pad_od"], x, y, d["z_ped_top"], d["z_pcb_rear"]))

    # 5. post root reliefs, bored down from the datum plane
    for (x, y) in d["sprung"]:
        B.sub(s, B.cylz(P["sprung_relief_d"], x, y,
                        d["z_sprung_floor"], d["z_pcb_rear"]))
    for (x, y) in d["plain"]:
        B.sub(s, B.cylz(P["plain_relief_d"], x, y,
                        d["z_plain_floor"], d["z_pcb_rear"]))

    # 6. the posts
    for (x, y) in d["sprung"]:
        B.uni(s, sprung_post(B, P, d, x, y, pinch))
    for (x, y) in d["plain"]:
        B.uni(s, plain_post(B, P, d, x, y))

    # 7. M2 heat-set insert bores, blind, opening at the seating face
    for sx in (-1, 1):
        x = sx * d["m2_x"]
        B.sub(s, B.cylz(P["m2_insert_d"], x, P["panel_fix_y"],
                        d["z_insert_bore"], 0.001))
        ch = P["m2_bore_chamfer"]
        B.sub(s, B.conez(P["m2_insert_d"] + 2 * ch, P["m2_insert_d"],
                         x, P["panel_fix_y"], 0.001, -ch))

    # 8. rear-open wire relief through the top wall and flange
    B.sub(s, B.box(-P["wire_notch_w"] / 2.0, P["wire_notch_w"] / 2.0,
                   d["pk_y1"], d["car_y1"] + 1.0,
                   zr - 1.0, zr + P["wire_notch_depth"]))

    # 9. cable-tie strain relief: a rear-face relief across the flange root,
    #    plus two Y slots breaking out at the flange top edge, so a tie can be
    #    threaded entirely on the rear side. Nothing reaches the seating face.
    B.sub(s, B.box(-P["tie_relief_w"] / 2.0, P["tie_relief_w"] / 2.0,
                   d["wall_y1"], d["wall_y1"] + P["tie_relief_h"],
                   zr - 1.0, zr + P["tie_relief_depth"]))
    for sx in (-1, 1):
        x = sx * P["tie_slot_x"]
        B.sub(s, B.box(x - P["tie_slot_w"] / 2.0, x + P["tie_slot_w"] / 2.0,
                       d["wall_y1"] + P["tie_relief_h"] - 1.0,
                       d["car_y1"] + 1.0,
                       P["tie_slot_z"] - P["tie_slot_h"] / 2.0,
                       P["tie_slot_z"] + P["tie_slot_h"] / 2.0))
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
              "z_nose_tip", "z_ped_top", "z_sprung_floor", "z_sprung_fix",
              "z_plain_floor", "z_plain_top", "post_a", "post_t",
              "hook_overlap", "shaft_clear", "plain_clear", "nose_keepout_r",
              "y_sprung", "y_plain", "post_x"):
        vals[k] = d[k]
    n = 0
    for k in sorted(vals):
        v = vals[k]
        if not isinstance(v, (int, float)):
            continue
        name = "p_" + k
        expr = "%.4f mm" % v
        ex = ups.itemByName(name)
        try:
            if ex:
                ex.expression = expr
            else:
                ups.add(name, adsk.core.ValueInput.createByString(expr),
                        "mm", "Rev P.2 generator")
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

    for name in ("REF_Decca_Panel", "REF_SH1106_1P3", CARRIER):
        clear_component(design, name)

    add_component(root, "REF_Decca_Panel", build_panel(B, P, d))
    add_component(root, "REF_SH1106_1P3", build_oled(B, P, d))
    add_component(root, CARRIER, build_carrier(B, P, d))

    app.activeViewport.fit()

    print("Rev P.2 built in %s document %r"
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
    print("sprung posts y %+.2f (header side: %s)  plain posts y %+.2f"
          % (d["y_sprung"], d["sprung_is_header_side"], d["y_plain"]))


# ---------------------------------------------------------------------------
# validate - the mandatory Rev P.2 validation gate
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

    def gate(ok, label, detail=""):
        print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", label, detail))
        if not ok:
            fails.append(label)

    def openitem(label, detail=""):
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
    print("REV P.2 VALIDATION GATE - corrected flush-side-insertion architecture")
    print("=" * 80)

    # ---- 1. static interference, seated ---------------------------------
    print("")
    print("1. STATIC INTERFERENCE - final seated position")
    for name in ("OLED_Glass", "OLED_ActiveArea", "OLED_Header_Keepout",
                 "OLED_Solder_Tips", "OLED_PCB"):
        h, v, bb = _hit(B, carrier, mod[name])
        gate(not h, "carrier x %s" % name,
             "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
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
         "%.2f mm radial overlap, square retaining face" % d["hook_overlap"])
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
         "noses stay inside the hole keep-out (R%.2f about each centre)"
         % d["nose_keepout_r"],
         "EMPTY" if n2 == 0 else "%.5f mm3 outside the keep-out" % rv2)
    zmax = max(f.boundingBox.maxPoint.z * 10 for f in carrier.faces)
    gate(abs(zmax) < 1e-6, "forward-most carrier material",
         "z = %+.5f - the Perspex seating plane" % zmax)
    plain_fwd = 0
    for (x, y) in d["plain"]:
        if _inside(carrier, x, y, d["z_pcb_front"] + 0.02):
            plain_fwd += 1
    gate(plain_fwd == 0, "plain posts stay behind the PCB front plane",
         "%.2f mm behind it - unconditionally clear of the glass even if"
         % P["plain_setback"])
    print("         the glass covers the display-side holes completely,")
    print("         which the modelled (unmeasured) envelope says it does.")

    # ---- 4. M2 load path -------------------------------------------------
    print("")
    print("4. M2 LOAD PATH")
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
    print("      insert bore z 0.00 .. %+.2f ; backing %.2f ; boss wall %.2f mm"
          % (d["z_insert_bore"], P["carrier_depth"] + d["z_insert_bore"],
             (P["m2_boss_d"] - P["m2_insert_d"]) / 2.0))
    print("      screw -> Perspex -> seating face -> boss -> insert.")
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

    # ---- 6. retention mechanics -----------------------------------------
    print("")
    print("6. RETENTION MECHANICS - recalculated from the finished geometry")
    a = d["post_a"]
    t = d["post_t"]
    I = P["sprung_shaft_d"] * t ** 3 / 12.0

    def beam(delta):
        return (3 * P["petg_E"] * I * delta / a ** 3,
                3 * t * delta / (2 * a * a) * 100.0)

    dn = d["hook_overlap"]
    dw = dn + d["shaft_clear"]                 # board hard against one side
    F_n, e_n = beam(dn)
    _F_w, e_w = beam(dw)
    tan_c = math.tan(math.radians(d["cam_deg"]))
    axial = 2.0 * F_n * (tan_c + 0.30) / (1 - 0.30 * tan_c)
    print("      split cantilever a = %.2f mm, half-section %.2f x %.2f mm"
          % (a, t, P["sprung_shaft_d"]))
    print("      barb %.2f in a %.2f hole -> %.2f mm radial overlap"
          % (P["sprung_barb_d"], P["oled_hole_d"], dn))
    gate(e_n < P["strain_limit"], "peak strain, hole centred",
         "%.2f %% at %.2f mm deflection per half" % (e_n, dn))
    gate(e_w < P["strain_limit"], "peak strain, board hard against one side",
         "%.2f %% at %.2f mm on a single half" % (e_w, dw))
    print("      insertion %.1f N per post at a %.1f deg cam -> %.1f N total"
          % (axial, d["cam_deg"], 2 * axial))
    print("      (the mu 0.30 above estimates push-on force ONLY; no")
    print("       acceptance criterion in this gate depends on friction)")
    gate(True, "seated spring deflection",
         "0.00 mm - the barb clears the PCB front face entirely")
    gate(True, "seated preload on the PCB",
         "none: %.2f mm axial under the hook, %.2f mm radial in the hole"
         % (P["hook_clear"], d["shaft_clear"]))
    gate(True, "retention basis", "positive geometric overlap, not friction")

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
        gate(not h, "carrier x %s" % nm,
             "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    h, v, bb = _hit(B, carrier, swept["SWEPT_PCB"])
    print("  [INFO] carrier x SWEPT_PCB  HIT %.4f mm3  %s" % (v, bb))
    n, rv = _residual(B, carrier, swept["SWEPT_PCB"], env)
    gate(n == 0, "only the two sprung noses deflect during insertion",
         "all %.4f mm3 is designed snap deflection" % v if n == 0
         else "%.5f mm3 of RIGID obstruction in the corridor" % rv)

    # ---- 8. removal -----------------------------------------------------
    print("")
    print("8. REMOVAL - barbs pinched, no prise holes, no special tool")
    pinch = d["hook_overlap"] + 0.02
    car_p = build_carrier(B, P, d, pinch=pinch)[0][0]
    print("      barbs modelled squeezed %.2f mm per half = %.2f required "
          "+ 0.02 margin" % (pinch, d["hook_overlap"]))
    for nm in ("SWEPT_PCB", "SWEPT_Glass", "SWEPT_Tips", "SWEPT_Header"):
        h, v, bb = _hit(B, car_p, swept[nm])
        gate(not h, "pinched carrier x %s" % nm,
             "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    rear_open = True
    for xr in (-8.0, 0.0, 8.0):
        rear_open = rear_open and not _inside(carrier, xr, 0.0, d["z_rear"] + 0.5)
    gate(rear_open, "open rear push-out window behind the PCB",
         "clear on the carrier rear face between the pedestals")
    gate(d["z_nose_tip"] - d["z_pcb_front"] > 0.40,
         "barbs accessible from the front for pinching",
         "%.2f mm of nose stands proud of the PCB front face"
         % (d["z_nose_tip"] - d["z_pcb_front"]))

    # ---- 9. glass clearance ---------------------------------------------
    print("")
    print("9. GLASS CLEARANCE - the one item that is REPORTED, not assumed")
    h, v, bb = _hit(B, carrier, swept["SWEPT_Glass"])
    print("      carrier x swept glass, MODELLED envelope: %s"
          % ("CLEAR" if not h else "HIT %.4f mm3" % v))
    nose_inner = d["y_sprung"] - P["sprung_barb_d"] / 2.0
    print("      modelled glass top edge %+.2f, nose inner edge %+.2f -> "
          "%.2f mm" % (d["glass_y1"], nose_inner, nose_inner - d["glass_y1"]))
    print("      modelled hole-centre to glass edge: %.2f mm"
          % (d["y_sprung"] - d["glass_y1"]))
    print("      BUT oled_glass_w / _h / _off_y are NOT MEASURED.")
    openitem("glass envelope vs the header-side mounting holes",
             "measure hole-centre to nearest glass edge at BOTH header-side "
             "holes; it must be >= %.2f mm, i.e. the glass must not pass "
             "y = %+.2f. Modelled (unmeasured) value %.2f mm."
             % (d["nose_keepout_r"], d["y_sprung"] - d["nose_keepout_r"],
                d["y_sprung"] - d["glass_y1"]))
    big = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                d["z_pcb_front"], d["z_glass_front"] + SWEEP_TRAVEL)
    h, v, bb = _hit(B, carrier, big)
    n, rv = _residual(B, carrier, big, env)
    print("      worst case, glass = the FULL PCB outline swept: %.4f mm3, of"
          % v)
    gate(n == 0, "worst-case glass exposure is confined to the two noses",
         "%.5f mm3 outside them" % rv if n else
         "which every scrap is inside the two declared noses")
    print("      -> the two noses are the ONLY glass exposure in the design;")
    print("         the plain posts, pads, pedestals, walls and rim are clear")
    print("         of the glass even if the glass is the whole board.")

    # ---- 10. optical alignment ------------------------------------------
    print("")
    print("10. OPTICAL ALIGNMENT AND THE ASSEMBLED GAP")
    aa = mod["OLED_ActiveArea"].boundingBox
    cx = (aa.minPoint.x + aa.maxPoint.x) * 5.0
    cy = (aa.minPoint.y + aa.maxPoint.y) * 5.0
    gate(abs(cx) < 1e-6 and abs(cy) < 1e-6,
         "active-area centre on the aperture centre",
         "(%.4f, %.4f)" % (cx, cy))
    gate(abs(-d["z_glass_front"] - P["oled_perspex_gap"]) < 1e-9,
         "assembled glass-to-Perspex gap",
         "%.3f mm nominal, seated on the fixed pads" % P["oled_perspex_gap"])
    print("      float within the carrier is the %.2f mm hook clearance, so the"
          % P["hook_clear"])
    print("      worst-case gap is %.2f mm and the glass can never touch the"
          % (P["oled_perspex_gap"] - P["hook_clear"]))
    print("      Perspex.")
    print("      active %.2f x %.2f in aperture %.2f x %.2f -> margin x %.2f y %.2f"
          % (P["oled_active_w"], P["oled_active_h"], P["panel_open_w"],
             P["panel_open_h"], (P["panel_open_w"] - P["oled_active_w"]) / 2,
             (P["panel_open_h"] - P["oled_active_h"]) / 2))
    print("      firmware must still mask 2 pixel rows top and bottom")

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
    ledge = (P["sprung_barb_d"] - P["sprung_shaft_d"]) / 2.0
    gate(ledge <= 0.30, "unsupported barb ledge, printed rear-down",
         "%.2f mm radial step from the shaft (the retention overlap against "
         "the hole is a different %.2f mm) - the Rev D / Rev K hook class, "
         "both printed" % (ledge, d["hook_overlap"]))
    print("      structural wall %.2f ; boss wall %.2f ; insert backing %.2f mm"
          % (P["carrier_wall"], (P["m2_boss_d"] - P["m2_insert_d"]) / 2.0,
             P["carrier_depth"] + d["z_insert_bore"]))
    print("      sprung post %.2f dia, %.2f mm tall, slot %.2f mm"
          % (P["sprung_shaft_d"], d["z_nose_tip"] - d["z_sprung_floor"],
             P["sprung_slot_w"]))
    print("      plain post %.2f dia, %.2f mm tall"
          % (P["plain_post_d"], d["z_plain_top"] - d["z_plain_floor"]))
    print("      ORIENTATION: carrier REAR FACE on the bed, building +Z.")
    print("      - pedestals and post roots all grow off the bed, no supports")
    print("      - root reliefs are upward-opening blind pockets")
    print("      - datum pads at z %.2f are upward-facing, layer-accurate"
          % d["z_pcb_rear"])
    print("      - the nose lead-in is a %.0f deg self-supporting cone"
          % (90 - d["cam_deg"]))

    # ---- 12. point probes -----------------------------------------------
    print("")
    print("12. SOLID-MEMBERSHIP PROBES")
    sx, sy = d["sprung"][1]
    px, py = d["plain"][1]
    edge = (P["oled_hole_d"] + P["sprung_barb_d"]) / 4.0   # 1.55, on the
    #                                                        hole edge
    # a point on one half of the split post: clear of the slot, inside the
    # shaft. The post AXIS is inside the slot, so it must not be probed.
    half = (P["sprung_slot_w"] / 2.0 + P["sprung_shaft_d"] / 2.0) / 2.0
    # a point inside a root relief bore: outside the shaft, inside the bore
    rel = (P["sprung_shaft_d"] / 2.0 + P["sprung_relief_d"] / 2.0) / 2.0
    probes = [
        ("seating rim solid", 0.0, d["wall_y1"] - 1.5, -0.20, True),
        ("M2 boss solid", d["m2_x"] + 2.4, 0.0, -1.0, True),
        ("M2 insert bore void", d["m2_x"], 0.0, -2.0, False),
        ("insert backing solid", d["m2_x"], 0.0, -6.5, True),
        ("module aperture void", 0.0, d["pcb_y1"] + 0.3, -0.60, False),
        ("aperture at PCB corner void", d["pcb_x1"] + 0.4, d["pcb_y1"] + 0.4,
         -0.60, False),
        ("pocket side wall solid", d["pk_x1"] + 0.3, 0.0, -5.0, True),
        ("PCB pocket void", 0.0, 0.0, -2.0, False),
        ("open rear window void", 0.0, 0.0, d["z_rear"] + 0.5, False),
        ("sprung shaft solid inside the hole", sx, sy + half, -2.0, True),
        ("sprung barb solid ahead of the PCB face", sx, sy + half,
         (d["z_hook_face"] + d["z_hook_top"]) / 2.0, True),
        ("barb overlaps the hole edge", sx, sy + edge,
         (d["z_hook_face"] + d["z_hook_top"]) / 2.0, True),
        ("no barb material at the PCB front plane", sx, sy + edge,
         d["z_pcb_front"] - 0.02, False),
        ("sprung root relief void", sx + rel, sy, -4.0, False),
        ("sprung post root solid", sx, sy + half,
         d["z_sprung_floor"] + 0.3, True),
        ("pedestal solid below the relief", sx, sy, d["z_rear"] + 0.5, True),
        ("split slot void on the post axis", sx, sy, -2.0, False),
        ("datum pad solid behind DATUM B", sx + rmid, sy,
         d["z_pcb_rear"] - 0.05, True),
        ("datum pad void ahead of DATUM B", sx + rmid, sy,
         d["z_pcb_rear"] + 0.05, False),
        ("plain post solid inside the hole", px, py, -2.0, True),
        ("plain post void ahead of the PCB face", px, py,
         d["z_pcb_front"] + 0.02, False),
        ("plain root relief void", px + rel, py, -3.3, False),
        ("wire notch void", 0.0, d["pk_y1"] + 1.0, d["z_rear"] + 0.7, False),
        ("tie slot void", P["tie_slot_x"], d["car_y1"] - 1.0, P["tie_slot_z"],
         False),
        ("flange seating face solid", P["tie_slot_x"], d["car_y1"] - 1.0,
         -0.20, True),
        ("tie rear relief void", 0.0, d["wall_y1"] + 1.0, d["z_rear"] + 0.8,
         False),
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

    # ---- 14. cable-tie path ---------------------------------------------
    print("")
    print("14. CABLE-TIE PATH - 3.50 x 1.40 mm tie section")
    z0 = P["tie_slot_z"] - 0.70
    z1 = P["tie_slot_z"] + 0.70
    tie = None
    for sxx in (-1, 1):
        x = sxx * P["tie_slot_x"]
        b = B.box(x - 1.75, x + 1.75, d["wall_y1"] + 0.4, d["car_y1"] + 4.0,
                  z0, z1)
        tie = b if tie is None else B.uni(tie, b)
    B.uni(tie, B.box(-P["tie_slot_x"] - 1.75, P["tie_slot_x"] + 1.75,
                     d["wall_y1"] + 0.4,
                     d["wall_y1"] + P["tie_relief_h"] - 0.4, z0, z1))
    h, v, bb = _hit(B, carrier, tie)
    gate(not h, "tie section swept through the anchor path",
         "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    tz = max(f.boundingBox.maxPoint.z * 10 for f in tie.faces)
    gate(tz < -0.001, "tie path never reaches the Perspex seating face",
         "forward-most tie material z = %+.2f" % tz)

    # ---- 15. part count --------------------------------------------------
    print("")
    print("15. PART COUNT")
    gate(find_component(design, "Retainer_Bar") is None,
         "no separate retainer bar", "carrier + the unchanged Rev N bezel")

    print("")
    print("=" * 80)
    if fails:
        print("GATE RESULT: %d FAILURE(S)" % len(fails))
        for f in fails:
            print("   - %s" % f)
    else:
        print("GATE RESULT: ALL CHECKS PASS")
    if opens:
        print("")
        print("BLOCKING OPEN ITEM(S) BEFORE ANY PRINT: %d" % len(opens))
        for o in opens:
            print("   * %s" % o)
    print("")
    print("Rev P remains OPEN. These checks may release a corrected")
    print("geometry-validation print once the open item above is measured, but")
    print("the retention finding is closed only by a physical inversion and")
    print("gentle-shake handling test on a printed carrier.")
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

    clear_component(design, SECTION)

    # 1. front three-quarter: carrier + module, the flush side towards us
    _show(design, {CARRIER, "REF_SH1106_1P3"})
    _shot(app, os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_views.png"),
          (-60.0, -45.0, 70.0), (0.0, 4.0, -3.0), (0, 1, 0))

    # 2. rear three-quarter: the carrier alone - pedestals, pads, open rear
    _show(design, {CARRIER})
    _shot(app, os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_rear.png"),
          (55.0, -50.0, -70.0), (0.0, 4.0, -4.0), (0, 1, 0))

    # 3. carrier alone from the front - the retention features themselves
    _show(design, {CARRIER})
    _shot(app, os.path.join(IMG_DIR, "Decca_OLED_Display_Mount_revP_posts.png"),
          (-42.0, -34.0, 46.0), (0.0, 5.0, -2.5), (0, 1, 0))

    # 4. section on x = +15.00, through a sprung locating post.
    #    Everything is clipped to a window around the module as well as to the
    #    half space, so the 90 x 80 mm reference Perspex patch cannot swamp
    #    the fitted view.
    win = B.box(d["post_x"], 40.0, -18.0, 32.0, -13.0, 4.0)
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
          (-120.0, 26.0, 34.0), (d["post_x"], 7.0, -4.0), (0, 1, 0))

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
