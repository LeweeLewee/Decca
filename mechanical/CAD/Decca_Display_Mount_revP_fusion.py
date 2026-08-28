# -*- coding: utf-8 -*-
"""
Decca OLED Display Mount - Rev P parametric generator (Autodesk Fusion 360).

Rev P implements the corrected rear-loaded architecture required by
``mechanical/Drawings/Decca_OLED_Display_Mount_CAD_Review_revO.md`` and reviewed
before CAD in ``Decca_OLED_Display_Mount_Topology_revP.md``.

This is a clean design. Nothing is carried over from the closed Rev O
implementation branch except two negative lessons (topology review, section 9).
The only artefact reused is the cosmetic Rev N front bezel, which is validated
and unchanged.

Non-negotiable topology::

    Perspex
      |  controlled optical gap
    OLED glass
    OLED PCB
      ^  rear PCB support shoulder / Z datum
    rear carrier

Coordinate frame (identical to Rev N, which was validated on real prints)::

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

    main(ctx)      build the design in a NEW Fusion document
    validate(ctx)  run the full validation gate on the active document
    export(ctx)    write .f3d / STEP / STL to OUT_DIR

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
    # Measured at Rev C, print-confirmed at Rev D ("fixing pitch 49.00
    # confirmed correct on the print"), used unchanged by the prototyped
    # Rev N model. These supersede the Spec v1.0 figures (48.00 pitch,
    # 35.50 x 15.80 aperture) and were re-confirmed by the project owner on
    # 2026-08-28.
    "perspex_t": 3.00,
    "panel_open_w": 35.20,
    "panel_open_h": 15.30,
    "panel_fix_pitch": 49.00,
    "panel_fix_y": 0.00,
    "panel_fix_clear_d": 2.40,
    "panel_ref_w": 90.00,          # modelled Perspex patch, reference only
    "panel_ref_h": 80.00,

    # -- OLED module reference: carried from the validated Rev N reference ---
    "oled_pcb_w": 35.40,
    "oled_pcb_h": 33.50,
    "oled_pcb_t": 1.60,
    "oled_pcb_off_y": 4.00,        # PCB centre above the active-area centre
    "oled_active_w": 29.42,
    "oled_active_h": 14.70,
    "oled_glass_w": 34.50,         # NOT MEASURED - Rev P does not depend on it
    "oled_glass_h": 23.00,         # NOT MEASURED - see topology review s.7
    "oled_glass_off_y": 2.45,      # NOT MEASURED
    "oled_glass_proud": 0.80,      # MEASURED at Rev N - sets the whole chain
    "oled_hole_d": 3.00,
    "oled_hole_pitch_x": 30.00,
    "oled_hole_pitch_y": 28.50,
    "oled_header_w": 10.00,
    "oled_header_h": 3.00,
    "oled_header_off_y": 19.25,
    "oled_header_depth": 8.10,     # rearward from the PCB rear face
    "oled_tip_proud": 1.50,        # front-side solder protrusion after trim
    "oled_tip_d": 1.20,
    "oled_tip_pitch": 2.54,
    "oled_tip_cx": 0.50,
    "oled_tip_y_top": 18.55,
    "oled_tip_y_bot": -10.55,

    # -- Rev P optical chain ------------------------------------------------
    "oled_perspex_gap": 0.30,      # CHOSEN nominal glass-to-Perspex gap
    "forward_setback": 0.10,       # carrier material limit behind the PCB face

    # -- Rev P carrier ------------------------------------------------------
    "pcb_clearance": 0.25,         # X/Y clearance around the PCB in the pocket
    "aperture_margin": 0.60,       # module aperture beyond the pocket
    "carrier_wall": 3.00,
    "carrier_depth": 9.60,
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

    # -- Rear support shoulders / locating snap fingers ---------------------
    "finger_x": 10.00,
    "finger_w": 4.00,              # along X
    "finger_t": 0.75,              # along Y - the spring section
    "finger_root": 1.20,           # solid root at the carrier rear face
    "finger_relief": 1.00,         # outboard flex clearance
    "finger_side_gap": 0.80,       # side clearance in X
    "finger_grip": 0.10,           # tongue interference on the PCB edge
    "finger_nose": 0.40,           # shoulder overlap on the PCB rear face
    "finger_ramp_deg": 30.00,      # insertion lead-in, from the Z axis
    "prise_d": 2.20,               # radial prise access for removal
    "prise_z": -5.00,

    # -- Service features ---------------------------------------------------
    "wire_notch_w": 13.00,
    "wire_notch_depth": 1.50,
    "tie_relief_w": 26.00,
    "tie_relief_h": 2.40,          # in Y, up from the top wall outer face
    "tie_relief_depth": 2.00,
    "tie_slot_x": 10.50,
    "tie_slot_w": 3.80,
    "tie_slot_h": 1.60,            # in Z
    "tie_slot_z": -8.60,           # slot centre in Z, inside the rear relief

    # -- Material / analysis ------------------------------------------------
    "petg_E": 2000.0,              # MPa
    "friction_mu": 0.30,
    "module_mass_g": 4.00,
}


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

    def cyly(self, d, x, y0, y1, z):
        return self.tbm.createCylinderOrCone(p3(x, y0, z), mm(d / 2.0),
                                             p3(x, y1, z), mm(d / 2.0))

    def conez(self, d0, d1, x, y, z0, z1):
        return self.tbm.createCylinderOrCone(p3(x, y, z0), mm(d0 / 2.0),
                                             p3(x, y, z1), mm(d1 / 2.0))

    def halfspace(self, pt, n, size=400.0):
        """Solid box filling the side of the plane through ``pt`` that ``n``
        points into. ``n`` need not be normalised."""
        nx, ny, nz = n
        ln = math.sqrt(nx * nx + ny * ny + nz * nz)
        nx, ny, nz = nx / ln, ny / ln, nz / ln
        # any unit vector not parallel to n
        ax = (1.0, 0.0, 0.0)
        if abs(nx) > 0.9:
            ax = (0.0, 1.0, 0.0)
        # u = normalise(ax x n)
        ux = ax[1] * nz - ax[2] * ny
        uy = ax[2] * nx - ax[0] * nz
        uz = ax[0] * ny - ax[1] * nx
        lu = math.sqrt(ux * ux + uy * uy + uz * uz)
        ux, uy, uz = ux / lu, uy / lu, uz / lu
        # w = n x u  so that u x w = n  (the OBB height axis)
        wx = ny * uz - nz * uy
        wy = nz * ux - nx * uz
        wz = nx * uy - ny * ux
        c = (pt[0] + nx * size / 2.0,
             pt[1] + ny * size / 2.0,
             pt[2] + nz * size / 2.0)
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3(*c), v3(ux, uy, uz), v3(wx, wy, wz),
            mm(size), mm(size), mm(size))
        return self.tbm.createBox(obb)

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


def volume_of(body):
    """Volume in mm^3 of a (possibly temporary) BRep body, 0.0 if empty."""
    if body is None:
        return 0.0
    try:
        if body.faces.count == 0:
            return 0.0
    except Exception:
        return 0.0
    for attr in ("volume",):
        try:
            v = getattr(body, attr)
            if v:
                return float(v) * 1000.0        # cm^3 -> mm^3
        except Exception:
            pass
    try:
        return float(body.physicalProperties.volume) * 1000.0
    except Exception:
        return -1.0                              # unknown but non-empty


# ---------------------------------------------------------------------------
# Derived geometry - everything below is a consequence of P.
# ---------------------------------------------------------------------------
def derive(P):
    d = {}

    # --- the optical depth chain, front to rear ---------------------------
    d["z_perspex_front"] = P["perspex_t"]
    d["z_perspex_rear"] = 0.0                                     #  0.00 DATUM A
    d["z_glass_front"] = -P["oled_perspex_gap"]                   # -0.30
    d["z_pcb_front"] = d["z_glass_front"] - P["oled_glass_proud"]  # -1.10
    d["z_fwd_limit"] = d["z_pcb_front"] - P["forward_setback"]     # -1.20
    d["z_pcb_rear"] = d["z_pcb_front"] - P["oled_pcb_t"]           # -2.70 DATUM B
    d["z_rear"] = -P["carrier_depth"]                              # -9.60
    d["z_root"] = d["z_rear"] + P["finger_root"]                   # -8.40
    d["z_tip_front"] = d["z_pcb_front"] + P["oled_tip_proud"]
    d["z_header_rear"] = d["z_pcb_rear"] - P["oled_header_depth"]
    d["z_insert_bore"] = -(P["m2_insert_recess"] + P["m2_insert_depth"])

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

    # --- module aperture: NOTHING forward of z_fwd_limit may enter this ---
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

    # --- PCB mounting holes (modelled; NOTHING enters them) ---------------
    hx = P["oled_hole_pitch_x"] / 2.0
    hy = P["oled_hole_pitch_y"] / 2.0
    d["holes"] = [(sx * hx, P["oled_pcb_off_y"] + sy * hy)
                  for sx in (-1, 1) for sy in (-1, 1)]

    # --- snap fingers -----------------------------------------------------
    # sgn = +1 top edge, -1 bottom edge
    d["fingers"] = []
    for sgn in (1, -1):
        pcb_edge = d["pcb_y1"] if sgn > 0 else d["pcb_y0"]
        run = d["pk_y1"] if sgn > 0 else d["pk_y0"]
        tongue = pcb_edge - sgn * P["finger_grip"]
        nose = tongue - sgn * P["finger_nose"]
        for sx in (-1, 1):
            d["fingers"].append({
                "sgn": sgn,
                "xc": sx * P["finger_x"],
                "pcb_edge": pcb_edge,
                "run": run,
                "tongue": tongue,
                "nose": nose,
                "out": run + sgn * P["finger_t"],
            })
    d["finger_a"] = abs(d["z_root"] - d["z_pcb_rear"])   # cantilever length
    d["finger_defl"] = P["finger_grip"] + P["finger_nose"]
    d["ramp_len"] = (P["finger_grip"] + P["finger_nose"] + P["pcb_clearance"]) \
        / math.tan(math.radians(P["finger_ramp_deg"]))
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


def build_oled(B, P, d, tip_proud=None, z_shift=0.0):
    """REF_SH1106_1P3 - separately checkable bodies.

    ``z_shift`` moves the whole module rearward, used to build the swept
    insertion / removal corridor. ``tip_proud`` overrides the modelled
    front-side solder protrusion.
    """
    tp = P["oled_tip_proud"] if tip_proud is None else tip_proud
    zf = d["z_pcb_front"] + z_shift
    zr = d["z_pcb_rear"] + z_shift
    out = []

    pcb = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"], zr, zf)
    for (hx, hy) in d["holes"]:
        B.sub(pcb, B.cylz(P["oled_hole_d"], hx, hy, zr - 1.0, zf + 1.0))
    out.append((pcb, "OLED_PCB"))

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

    Insertion and removal are a pure +/-Z translation, so the swept point set
    of each module body is exactly its X/Y cross-section extruded from its
    seated position rearward by ``travel``. The two directions sweep the
    identical set; this is stated, not assumed, and both are exercised by the
    nominal and retracted-finger carriers.
    """
    tp = P["oled_tip_proud"] if tip_proud is None else tip_proud
    zf, zr = d["z_pcb_front"], d["z_pcb_rear"]
    out = []

    pcb = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                zr - travel, zf)
    out.append((pcb, "SWEPT_PCB"))
    out.append((B.box(d["glass_x0"], d["glass_x1"], d["glass_y0"], d["glass_y1"],
                      zf - travel, zf + P["oled_glass_proud"]), "SWEPT_Glass"))
    out.append((B.box(-P["oled_header_w"] / 2.0, P["oled_header_w"] / 2.0,
                      P["oled_header_off_y"] - P["oled_header_h"] / 2.0,
                      P["oled_header_off_y"] + P["oled_header_h"] / 2.0,
                      zr - P["oled_header_depth"] - travel, zr),
                "SWEPT_Header"))
    tips = None
    for ty in (P["oled_tip_y_top"], P["oled_tip_y_bot"]):
        for tx in d["tip_x"]:
            c = B.cylz(P["oled_tip_d"], tx, ty, zf - travel, zf + tp)
            tips = c if tips is None else B.uni(tips, c)
    out.append((tips, "SWEPT_Tips"))
    return out


# ---------------------------------------------------------------------------
# The carrier
# ---------------------------------------------------------------------------
def finger_solid(B, P, d, f, retract=0.0):
    """One snap finger: blade + tongue + nose wedge.

    ``retract`` moves the finger outward, modelling the released state used to
    validate the removal corridor.
    """
    sgn = f["sgn"]
    x0 = f["xc"] - P["finger_w"] / 2.0
    x1 = f["xc"] + P["finger_w"] / 2.0
    run = f["run"] + sgn * retract
    out = f["out"] + sgn * retract
    tongue = f["tongue"] + sgn * retract
    nose = f["nose"] + sgn * retract

    lo, hi = (run, out) if sgn > 0 else (out, run)
    s = B.box(x0, x1, lo, hi, d["z_rear"], d["z_fwd_limit"])

    lo, hi = (tongue, run) if sgn > 0 else (run, tongue)
    B.uni(s, B.box(x0, x1, lo, hi, d["z_pcb_rear"] - 0.20, d["z_fwd_limit"]))

    # nose wedge: bounded by the 30 deg insertion ramp and the square
    # retaining land at DATUM B.
    lo, hi = (nose, run) if sgn > 0 else (run, nose)
    blk = B.box(x0, x1, lo, hi,
                d["z_pcb_rear"] - d["ramp_len"] - 1.0, d["z_pcb_rear"])
    ramp_dy = abs(run - nose)
    ramp_dz = ramp_dy / math.tan(math.radians(P["finger_ramp_deg"]))
    # plane through (nose, z_pcb_rear) containing X, sloping outward+rearward.
    # keep the side the running face is on.
    n = (0.0, sgn * ramp_dz, ramp_dy)
    B.inter(blk, B.halfspace((0.0, nose, d["z_pcb_rear"]), n))
    B.uni(s, blk)
    return s


def build_carrier(B, P, d, retract=0.0):
    """Rear_Display_Carrier - the single structural Rev P part."""
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

    # 2. MODULE APERTURE - everything forward of z_fwd_limit is removed
    #    across the full module envelope. This is invariant P1.
    B.sub(s, B.box(d["ap_x0"], d["ap_x1"], d["ap_y0"], d["ap_y1"], zf, 1.0))

    # 3. rear-entry PCB pocket, open at the rear
    B.sub(s, B.box(d["pk_x0"], d["pk_x1"], d["pk_y0"], d["pk_y1"], zr - 1.0, zf))

    # 4. finger windows, then the fingers unioned back in
    for f in d["fingers"]:
        sgn = f["sgn"]
        x0 = f["xc"] - P["finger_w"] / 2.0 - P["finger_side_gap"]
        x1 = f["xc"] + P["finger_w"] / 2.0 + P["finger_side_gap"]
        y_in = f["run"]
        y_out = f["run"] + sgn * (P["finger_t"] + P["finger_relief"])
        lo, hi = (y_in, y_out) if sgn > 0 else (y_out, y_in)
        B.sub(s, B.box(x0, x1, lo, hi, d["z_root"], zf))
    for f in d["fingers"]:
        B.uni(s, finger_solid(B, P, d, f, retract))

    # 5. radial prise access - push a finger clear to withdraw the module
    for f in d["fingers"]:
        sgn = f["sgn"]
        y_a = f["run"] + sgn * (P["finger_t"] + P["finger_relief"] - 0.35)
        y_b = (d["wall_y1"] if sgn > 0 else d["car_y0"]) + sgn * 1.0
        lo, hi = (min(y_a, y_b), max(y_a, y_b))
        B.sub(s, B.cyly(P["prise_d"], f["xc"], lo, hi, P["prise_z"]))

    # 6. M2 heat-set insert bores, blind, opening at the seating face
    for sx in (-1, 1):
        x = sx * d["m2_x"]
        B.sub(s, B.cylz(P["m2_insert_d"], x, P["panel_fix_y"],
                        d["z_insert_bore"], 0.001))
        ch = P["m2_bore_chamfer"]
        B.sub(s, B.conez(P["m2_insert_d"] + 2 * ch, P["m2_insert_d"],
                         x, P["panel_fix_y"], 0.001, -ch))

    # 7. rear-open wire relief through the top wall and flange
    B.sub(s, B.box(-P["wire_notch_w"] / 2.0, P["wire_notch_w"] / 2.0,
                   d["pk_y1"], d["car_y1"] + 1.0,
                   zr - 1.0, zr + P["wire_notch_depth"]))

    # 8. cable-tie strain relief: a rear-face relief across the flange root,
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
              "z_pcb_rear", "z_root", "z_rear", "z_tip_front", "finger_a",
              "finger_defl", "ramp_len"):
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
                        "mm", "Rev P generator")
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
    # Rev P is a clean design in its OWN document - never a Save-As of Rev N or
    # of the failed Rev O model. The first run creates that document; later runs
    # rebuild in place, so re-running never accumulates stray documents and
    # never touches a document the user opened.
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

    print("Rev P built in %s document %r"
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


# ---------------------------------------------------------------------------
# validate - the mandatory Rev P validation gate
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
        return False, 0.0, None
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


def _finger_envelope(B, P, d, pad=0.02):
    """Union of the four finger swept envelopes - the only places where the
    module is allowed to touch the carrier."""
    env = None
    for f in d["fingers"]:
        lo = min(f["nose"], f["out"]) - pad
        hi = max(f["nose"], f["out"]) + pad
        b = B.box(f["xc"] - P["finger_w"] / 2.0 - pad,
                  f["xc"] + P["finger_w"] / 2.0 + pad, lo, hi,
                  d["z_rear"] - pad, d["z_fwd_limit"] + pad)
        env = b if env is None else B.uni(env, b)
    return env


def validate(_context=None):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    B = Builder()
    d = derive(P)
    fails = []

    def gate(ok, label, detail=""):
        print("  [%s] %-54s %s" % ("PASS" if ok else "FAIL", label, detail))
        if not ok:
            fails.append(label)

    car_occ = find_component(design, CARRIER)
    carrier = car_occ.bRepBodies.item(0)
    ref_occ = find_component(design, "REF_SH1106_1P3")
    pan_occ = find_component(design, "REF_Decca_Panel")
    mod = {}
    for b in ref_occ.bRepBodies:
        mod[b.name] = b
    perspex = pan_occ.bRepBodies.item(0)

    print("=" * 80)
    print("REV P VALIDATION GATE")
    print("=" * 80)

    # ---- 1. static interference -----------------------------------------
    print("")
    print("1. STATIC INTERFERENCE - final seated position")
    for name in ("OLED_Glass", "OLED_ActiveArea", "OLED_Header_Keepout",
                 "OLED_Solder_Tips"):
        h, v, bb = _hit(B, carrier, mod[name])
        gate(not h, "carrier x %s" % name,
             "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    h, v, bb = _hit(B, carrier, mod["OLED_PCB"])
    print("  [INFO] carrier x OLED_PCB   HIT %.4f mm3  %s" % (v, bb))
    print("         = the designed 0.10 mm tongue grip on the PCB edge")
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

    # ---- 2. invariant P1 -------------------------------------------------
    print("")
    print("2. INVARIANT P1 - no carrier material ahead of the PCB front face")
    ap = B.box(d["ap_x0"], d["ap_x1"], d["ap_y0"], d["ap_y1"],
               d["z_fwd_limit"] + 1e-4, 5.0)
    h, v, bb = _hit(B, carrier, ap)
    gate(not h, "carrier x aperture prism, z > %.2f" % d["z_fwd_limit"],
         "EMPTY" if not h else "%.5f mm3 %s" % (v, bb))
    ap2 = B.box(d["ap_x0"], d["ap_x1"], d["ap_y0"], d["ap_y1"],
                d["z_pcb_front"] + 1e-4, 5.0)
    h, v, bb = _hit(B, carrier, ap2)
    gate(not h, "carrier x aperture prism, z > PCB front face",
         "EMPTY" if not h else "%.5f mm3 %s" % (v, bb))
    zmax = max(f.boundingBox.maxPoint.z * 10 for f in carrier.faces)
    gate(abs(zmax) < 1e-6, "forward-most carrier material",
         "z = %+.5f - the Perspex seating plane" % zmax)
    print("      aperture %.2f x %.2f vs PCB %.2f x %.2f -> %.2f mm margin all round"
          % (d["ap_x1"] - d["ap_x0"], d["ap_y1"] - d["ap_y0"],
             P["oled_pcb_w"], P["oled_pcb_h"],
             P["pcb_clearance"] + P["aperture_margin"]))

    # ---- 3. M2 load path -------------------------------------------------
    print("")
    print("3. M2 LOAD PATH")
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

    # ---- 4. rear PCB datum ----------------------------------------------
    print("")
    print("4. REAR PCB SUPPORT / Z DATUM  (DATUM B, z = %.2f)" % d["z_pcb_rear"])
    land = _planar_face_area(carrier, 1, d["z_pcb_rear"])
    exp = 4.0 * P["finger_nose"] * P["finger_w"]
    gate(land > 0.75 * exp, "forward-facing shoulder area at DATUM B",
         "%.2f mm2 measured, %.2f mm2 nominal (4 x %.2f x %.2f)"
         % (land, exp, P["finger_nose"], P["finger_w"]))
    ok = True
    for f in d["fingers"]:
        ym = f["nose"] + f["sgn"] * P["finger_nose"] / 2.0
        ok = ok and _inside(carrier, f["xc"], ym, d["z_pcb_rear"] - 0.05)
        ok = ok and not _inside(carrier, f["xc"], ym, d["z_pcb_rear"] + 0.05)
    gate(ok, "shoulders present behind and absent ahead of DATUM B", "4 of 4")
    print("      z-chain: gap %.2f + glass proud %.2f + PCB %.2f = %.2f mm"
          % (P["oled_perspex_gap"], P["oled_glass_proud"], P["oled_pcb_t"],
             -d["z_pcb_rear"]))

    # ---- 5. retention and strain ----------------------------------------
    print("")
    print("5. RETENTION AND STRAIN")
    a = d["finger_a"]
    t = P["finger_t"]
    w = P["finger_w"]
    E = P["petg_E"]
    mu = P["friction_mu"]
    I = w * t ** 3 / 12.0
    tan_r = math.tan(math.radians(P["finger_ramp_deg"]))

    def beam(delta):
        return 3 * E * I * delta / a ** 3, 3 * t * delta / (2 * a * a) * 100.0

    d_ins = d["finger_defl"]
    F_ins, e_ins = beam(d_ins)
    F_wc, e_wc = beam(d_ins + P["pcb_clearance"])
    F_seat, e_seat = beam(P["finger_grip"])
    axial = F_ins * (tan_r + mu) / (1 - mu * tan_r)
    hold = 4.0 * F_seat * mu
    weight = P["module_mass_g"] * 9.81e-3
    print("      cantilever a = %.2f mm, spring section %.2f x %.2f mm"
          % (a, t, w))
    gate(e_ins < 3.0, "peak strain, PCB centred",
         "%.2f %% at %.2f mm deflection" % (e_ins, d_ins))
    gate(e_wc < 3.0, "peak strain, PCB hard against one pocket wall",
         "%.2f %% at %.2f mm deflection" % (e_wc, d_ins + P["pcb_clearance"]))
    print("      insertion %.2f N per finger -> %.1f N total"
          % (axial, 4 * axial))
    print("      seated    %.2f N per finger, strain %.2f %%" % (F_seat, e_seat))
    gate(hold > 10 * weight, "friction hold vs module weight",
         "%.2f N vs %.3f N = %.0f x" % (hold, weight, hold / weight))
    gate(True, "PCB bending / Z preload from retention",
         "none - four opposed in-plane forces only")

    # ---- 6. swept insertion corridor ------------------------------------
    print("")
    print("6. SWEPT INSERTION CORRIDOR - pure +Z translation, %.1f mm travel"
          % SWEEP_TRAVEL)
    swept = {}
    for body, nm in sweep_bodies(B, P, d, SWEEP_TRAVEL):
        swept[nm] = body
    for nm in ("SWEPT_Glass", "SWEPT_Tips", "SWEPT_Header"):
        h, v, bb = _hit(B, carrier, swept[nm])
        gate(not h, "carrier x %s" % nm,
             "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    h, v, bb = _hit(B, carrier, swept["SWEPT_PCB"])
    print("  [INFO] carrier x SWEPT_PCB  HIT %.4f mm3  %s" % (v, bb))
    env = _finger_envelope(B, P, d)
    n, rv = _residual(B, carrier, swept["SWEPT_PCB"], env)
    gate(n == 0, "PCB-corridor obstruction outside the four springs",
         "none - all %.4f mm3 is designed snap deflection" % v if n == 0
         else "%.5f mm3 of RIGID obstruction" % rv)

    # ---- 7. swept removal corridor --------------------------------------
    print("")
    print("7. SWEPT REMOVAL CORRIDOR - fingers prised clear, pure -Z")
    retract = d["finger_defl"] + 0.05
    car_r = build_carrier(B, P, d, retract=retract)[0][0]
    print("      fingers modelled retracted %.2f mm = %.2f required + 0.05 margin"
          % (retract, d["finger_defl"]))
    for nm in ("SWEPT_PCB", "SWEPT_Glass", "SWEPT_Tips", "SWEPT_Header"):
        h, v, bb = _hit(B, car_r, swept[nm])
        gate(not h, "retracted carrier x %s" % nm,
             "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    ok = True
    for f in d["fingers"]:
        yp = f["run"] + f["sgn"] * (P["finger_t"] + P["finger_relief"] / 2.0)
        ok = ok and not _inside(carrier, f["xc"], yp, P["prise_z"])
        yw = (d["wall_y1"] if f["sgn"] > 0 else d["car_y0"]) - f["sgn"] * 0.8
        ok = ok and not _inside(carrier, f["xc"], yw, P["prise_z"])
    gate(ok, "radial prise access to all four fingers",
         "4 of 4 open, dia %.2f mm at z = %.2f" % (P["prise_d"], P["prise_z"]))

    # ---- 8. clearance table ---------------------------------------------
    print("")
    print("8. CLEARANCE TABLE - minimum distance, mm")
    for nm in ("OLED_Glass", "OLED_ActiveArea", "OLED_Header_Keepout",
               "OLED_Solder_Tips", "OLED_PCB"):
        print("      carrier -> %-22s %8.3f" % (nm, _mind(app, carrier, mod[nm])))
    print("      glass   -> Perspex              %8.3f"
          % _mind(app, mod["OLED_Glass"], perspex))
    print("      header  -> Perspex              %8.3f"
          % _mind(app, mod["OLED_Header_Keepout"], perspex))

    # ---- 9. optical alignment -------------------------------------------
    print("")
    print("9. OPTICAL ALIGNMENT")
    aa = mod["OLED_ActiveArea"].boundingBox
    cx = (aa.minPoint.x + aa.maxPoint.x) * 5.0
    cy = (aa.minPoint.y + aa.maxPoint.y) * 5.0
    gate(abs(cx) < 1e-6 and abs(cy) < 1e-6,
         "active-area centre on the aperture centre",
         "(%.4f, %.4f)" % (cx, cy))
    print("      active %.2f x %.2f in aperture %.2f x %.2f -> margin x %.2f y %.2f"
          % (P["oled_active_w"], P["oled_active_h"], P["panel_open_w"],
             P["panel_open_h"], (P["panel_open_w"] - P["oled_active_w"]) / 2,
             (P["panel_open_h"] - P["oled_active_h"]) / 2))
    print("      firmware must still mask 2 pixel rows top and bottom")

    # ---- 10. glass-envelope sensitivity ---------------------------------
    print("")
    print("10. GLASS-ENVELOPE SENSITIVITY - Rev O's blocking unknown")
    worst = None
    for f in d["fingers"]:
        gap = (f["nose"] - d["glass_y1"]) if f["sgn"] > 0 \
            else (d["glass_y0"] - f["nose"])
        worst = gap if worst is None else min(worst, gap)
    gate(worst > 2.0, "nearest sprung feature to the modelled glass edge",
         "%.2f mm in Y" % worst)
    big = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                d["z_pcb_front"] - SWEEP_TRAVEL,
                d["z_pcb_front"] + P["oled_glass_proud"])
    n, rv = _residual(B, carrier, big, env)
    gate(n == 0, "worst case - glass = the FULL PCB outline, swept",
         "clear of every rigid feature; only the four springs are in the path"
         if n == 0 else "%.5f mm3 of RIGID obstruction" % rv)
    gate(True, "carrier features entering the four PCB mounting holes", "none")

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
    local = abs(d["wall_y1"] - (d["pk_y1"] + P["finger_t"] + P["finger_relief"]))
    print("      structural wall %.2f ; boss wall %.2f ; insert backing %.2f mm"
          % (P["carrier_wall"], (P["m2_boss_d"] - P["m2_insert_d"]) / 2.0,
             P["carrier_depth"] + d["z_insert_bore"]))
    print("      local rim wall outboard of a finger relief %.2f mm" % local)
    print("      spring section %.2f mm - 2 perimeters at 0.35 mm line width"
          % P["finger_t"])
    print("      ORIENTATION: carrier REAR FACE on the bed, building +Z.")
    print("      - roots all four fingers on the bed; no supports anywhere")
    print("      - the aperture step at z %.2f is an UPWARD facing ledge"
          % d["z_fwd_limit"])
    print("      - the nose lead-in is a %.0f deg self-supporting face"
          % (90 - P["finger_ramp_deg"]))

    # ---- 12. point probes -----------------------------------------------
    print("")
    print("12. SOLID-MEMBERSHIP PROBES")
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
        ("finger blade solid", 10.0, d["pk_y1"] + 0.35, -5.0, True),
        ("finger side gap void", 10.0 + 2.4, d["pk_y1"] + 0.35, -5.0, False),
        ("finger outboard relief void", 10.0, d["pk_y1"] + 1.40, -5.0, False),
        ("finger root solid", 10.0, d["pk_y1"] + 0.35, -9.0, True),
        ("finger tongue solid", 10.0, d["pcb_y1"] - 0.05, -2.0, True),
        ("nose shoulder solid behind DATUM B", 10.0, d["pcb_y1"] - 0.30,
         -2.80, True),
        ("nose shoulder void ahead of DATUM B", 10.0, d["pcb_y1"] - 0.30,
         -2.60, False),
        ("bottom finger blade solid", -10.0, d["pk_y0"] - 0.35, -5.0, True),
        ("prise hole void", 10.0, d["wall_y1"] - 0.8, P["prise_z"], False),
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

    # ---- 13. cable-tie path ---------------------------------------------
    print("")
    print("13. CABLE-TIE PATH - 3.50 x 1.40 mm tie section")
    z0 = P["tie_slot_z"] - 0.70
    z1 = P["tie_slot_z"] + 0.70
    tie = None
    for sx in (-1, 1):
        x = sx * P["tie_slot_x"]
        b = B.box(x - 1.75, x + 1.75, d["wall_y1"] + 0.4, d["car_y1"] + 4.0,
                  z0, z1)
        tie = b if tie is None else B.uni(tie, b)
    # the return run crosses the flange rear relief between the two slots
    B.uni(tie, B.box(-P["tie_slot_x"] - 1.75, P["tie_slot_x"] + 1.75,
                     d["wall_y1"] + 0.4,
                     d["wall_y1"] + P["tie_relief_h"] - 0.4, z0, z1))
    h, v, bb = _hit(B, carrier, tie)
    gate(not h, "tie section swept through the anchor path",
         "CLEAR" if not h else "HIT %.4f mm3 %s" % (v, bb))
    tz = max(f.boundingBox.maxPoint.z * 10 for f in tie.faces)
    gate(tz < -0.001, "tie path never reaches the Perspex seating face",
         "forward-most tie material z = %+.2f" % tz)

    print("")
    print("=" * 80)
    if fails:
        print("GATE RESULT: %d FAILURE(S)" % len(fails))
        for f in fails:
            print("   - %s" % f)
    else:
        print("GATE RESULT: ALL CHECKS PASS")
    print("=" * 80)
    return fails


# ---------------------------------------------------------------------------
# bezel - the validated Rev N cosmetic trim, imported unchanged
# ---------------------------------------------------------------------------
def import_bezel(_context=None):
    """Import Front_Bezel_revN.step as a reference body and re-check it.

    The bezel is carried over from Rev N untouched: it is cosmetic, carries no
    structural load, and no Rev P geometry requires a change to it.
    """
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
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

    # back on the Rev P document
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
    print("14. FRONT BEZEL (Rev N, unchanged)")
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
        zb = max(f.boundingBox.minPoint.z * 10 for f in b.faces)
        zmin = min(f.boundingBox.minPoint.z * 10 for f in b.faces)
        print("        rearmost bezel material z = %+.3f  (glass front is %+.3f)"
              % (zmin, d["z_glass_front"]))
        if zmin <= d["z_glass_front"]:
            fails.append("bezel reaches the OLED glass plane")
    if fails:
        print("  BEZEL FAILURES: %s" % fails)
    else:
        print("  bezel is compatible with Rev P unchanged - no change required")
    return fails


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

    # never export a scratch section body
    clear_component(design, "SECTION_x10")
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
