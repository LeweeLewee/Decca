# -*- coding: utf-8 -*-
"""
Decca OLED Display Mount - Rev O parametric generator (Autodesk Fusion 360)

Run this INSIDE Fusion 360 (Utilities > Add-Ins > Scripts) to build the Rev O
design as a BRAND-NEW Fusion document and export
    mechanical/CAD/Decca_Display_Mount_revO.f3d
plus STEP and STL.

Rev O is a clean redesign, not a Rev N derivative:
  * the OLED PCB loads into the carrier from the REAR;
  * the OLED glass projects FORWARD through the carrier window;
  * the M2 load path is  screw -> carrier -> seating face -> Perspex,
    and never  screw -> carrier -> PCB -> glass -> Perspex;
  * there is no separate retainer bar and no full-area thin front plate.

Nothing from the Rev N feature tree is reused. The only Rev N artefact carried
forward is the cosmetic Front_Bezel, which is unchanged and is imported as a
STEP body (see BEZEL_STEP below) because it is already validated.

Coordinate frame (identical to Rev N, which was validated on real prints):
    origin  = centre of the original Decca display aperture
            = centre of the OLED active area  (primary optical datum)
    +X      = to the viewer's right
    +Y      = up
    +Z      = forward, out of the fascia towards the viewer
    z =  0.00  rear face of the original 3 mm Perspex == carrier seating plane
    z = +3.00  front face of the Perspex
    z <  0     rearward, into the carrier

Author: generated for the Decca restoration project.
"""

import os
import math
import traceback

import adsk.core
import adsk.fusion


# ---------------------------------------------------------------------------
# PARAMETERS - single source of truth.
# Every value is mm. The offline verifier
# (Decca_Display_Mount_revO_verify.py) parses this literal, so keep it a plain
# dict of plain numbers.
# ---------------------------------------------------------------------------
P = {
    # -- Original Decca panel: MEASURED off the real fascia ----------------
    # These are the physically measured values, taken at Rev C and confirmed
    # on a print at Rev D ("fixing pitch 49.00 confirmed correct on the
    # print"), and used unchanged by the Rev N model that was prototyped.
    #
    # They deviate from the figures quoted in the Rev O redesign brief
    # (48.00 pitch, 35.50 x 15.80 aperture), which are the ORIGINAL Spec v1.0
    # numbers that physical measurement superseded. Building at 48.00 would
    # put each M2 screw 0.50 mm off its hole - far more than the 0.20 mm
    # radial slop an M2 screw has in a 2.40 mm clearance hole - so the
    # carrier simply would not bolt on.  See the Rev O build review, s.2.
    # If the 48.00 figure is ever re-confirmed on the real panel, change
    # panel_fix_pitch here and rebuild; nothing else needs touching.
    "perspex_t": 3.00,            # original Perspex thickness
    "panel_open_w": 35.20,        # existing display aperture width  (measured)
    "panel_open_h": 15.30,        # existing display aperture height (measured)
    "panel_fix_pitch": 49.00,     # existing M2 fixing pitch          (measured)
    "panel_fix_y": 0.00,          # fixing centreline is centred on the aperture
    "panel_fix_clear_d": 2.40,    # M2 clearance hole in the Perspex
    "panel_ref_w": 90.00,         # size of the modelled Perspex patch (ref only)
    "panel_ref_h": 44.00,

    # -- OLED module: measured, carried over from the validated Rev N ref ---
    "oled_pcb_w": 35.40,
    "oled_pcb_h": 33.50,
    "oled_pcb_t": 1.60,
    "oled_pcb_off_y": 4.00,       # PCB centre sits this far ABOVE the active centre
    "oled_active_w": 29.42,
    "oled_active_h": 14.70,
    "oled_view_w": 31.42,
    "oled_view_h": 16.70,
    "oled_glass_w": 34.50,
    "oled_glass_h": 23.00,
    "oled_glass_off_y": 2.45,     # glass centre above the active centre
    "oled_glass_proud": 0.80,     # glass front face proud of the PCB front face
    "oled_hole_d": 3.00,
    "oled_hole_pitch_x": 30.00,
    "oled_hole_pitch_y": 28.50,
    "oled_header_w": 10.00,       # rear header/connector keep-out
    "oled_header_h": 3.00,
    "oled_header_off_y": 19.25,   # keep-out centre, y 17.75 .. 20.75
    "oled_header_depth": 8.10,    # projects rearward from the PCB rear face
    "oled_tip_proud": 2.00,       # solder tips proud of the PCB FRONT face - MEASURE
    "oled_tip_d": 1.20,
    "oled_tip_pitch": 2.54,
    "oled_tip_cx": 0.50,          # centre of the 4-way tip group
    "oled_tip_y_top": 18.55,
    "oled_tip_y_bot": -10.55,

    # -- Rev O carrier -----------------------------------------------------
    "oled_perspex_gap": 0.30,     # CHOSEN nominal glass-to-Perspex gap
    "pcb_seat_depth": 1.10,       # = oled_glass_proud + oled_perspex_gap  (derived)
    "carrier_stop_depth": 1.10,   # hard-stop plane to PCB datum plane (== pcb_seat_depth)
    "pcb_clearance": 0.25,        # X/Y clearance around the PCB in the pocket
    "glass_clearance": 0.30,      # X/Y clearance around the glass in the window
    "carrier_wall": 2.60,         # structural wall
    "carrier_depth": 5.60,        # seating plane to rear face
    "carrier_corner_r": 3.00,
    "carrier_top_flange": 3.00,   # cable-tie flange above the top wall
    "tip_relief_cx": 0.50,        # solder-tip / header relief window, centre
    "tip_relief_w": 14.00,        # ... and width

    # -- Locating snap posts (adapted from the Rev N snap-pin concept) ------
    "locating_pin_d": 2.70,
    "locating_pin_clearance": 0.30,   # = oled_hole_d - locating_pin_d
    "pin_barb": 0.35,             # radial barb on the split head
    "pin_float": 0.10,            # PCB free play under the barb shoulder
    "pin_head_h": 1.70,           # barb cone height
    "pin_tip_d": 2.20,            # lead-in diameter at the post tip
    "pin_slot_w": 1.20,           # splitting slot -> two 0.75 mm legs

    # -- M2 structural interface -------------------------------------------
    "m2_boss_d": 7.60,           # keeps the carrier inside the proven Rev N envelope
    "m2_insert_d": 3.20,          # heat-set insert bore
    "m2_insert_depth": 4.00,
    "m2_insert_recess": 0.50,     # insert installed this far below the seating face
    "m2_bore_chamfer": 0.40,      # relief for insert flash at the seating face

    # -- Service features ---------------------------------------------------
    "wire_notch_w": 14.00,
    "wire_notch_depth": 1.50,
    "tie_slot_w": 2.50,
    "tie_slot_h": 1.50,
    "tie_slot_x": 10.50,
    "tie_slot_z": -3.85,          # slot centre, rearward of the seating plane
}

# Where to write the outputs. Point this at your clone of the repo.
OUT_DIR = r"D:\GitHub\Decca\mechanical"
# Validated Rev N bezel, imported unchanged. Leave as None to skip the bezel.
BEZEL_STEP = os.path.join(OUT_DIR, "CAD", "Front_Bezel_revN.step")


# ---------------------------------------------------------------------------
# Helpers. Fusion works in cm; every design value here is mm.
# ---------------------------------------------------------------------------
def mm(v):
    return float(v) / 10.0


def p3(x, y, z):
    return adsk.core.Point3D.create(mm(x), mm(y), mm(z))


def v3(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


class Builder(object):
    """Thin wrapper over TemporaryBRepManager so the recipes read like solids."""

    def __init__(self):
        self.tbm = adsk.fusion.TemporaryBRepManager.get()

    def box(self, x0, x1, y0, y1, z0, z1):
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0),
            v3(1, 0, 0), v3(0, 1, 0),
            mm(x1 - x0), mm(y1 - y0), mm(z1 - z0))
        return self.tbm.createBox(obb)

    def cyl(self, d, x, y, z0, z1):
        return self.tbm.createCylinderOrCone(p3(x, y, z0), mm(d / 2.0),
                                             p3(x, y, z1), mm(d / 2.0))

    def cone(self, d0, d1, x, y, z0, z1):
        return self.tbm.createCylinderOrCone(p3(x, y, z0), mm(d0 / 2.0),
                                             p3(x, y, z1), mm(d1 / 2.0))

    def uni(self, a, b):
        self.tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
        return a

    def sub(self, a, b):
        self.tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        return a

    def rrect(self, x0, x1, y0, y1, z0, z1, r):
        """Rounded-rectangle prism along Z, built from primitives.

        Far more robust than filleting long vertical edges afterwards.
        Degenerate cases (a side exactly 2r, i.e. an obround) are handled, so
        the M2 boss ears can be written as a rounded prism of width 2r.
        """
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
                c = self.cyl(2 * r, cx, cy, z0, z1)
                s = c if s is None else self.uni(s, c)
        return s


# ---------------------------------------------------------------------------
# Derived geometry. Everything below is a consequence of P.
# ---------------------------------------------------------------------------
def derive(P):
    d = {}

    # --- the depth chain, front to rear -----------------------------------
    # This IS the Rev O design. Read it top to bottom.
    d["z_perspex_rear"] = 0.0
    d["z_glass_front"] = -P["oled_perspex_gap"]
    d["z_pcb_front"] = d["z_glass_front"] - P["oled_glass_proud"]     # -1.10
    d["z_pcb_rear"] = d["z_pcb_front"] - P["oled_pcb_t"]              # -2.70
    d["z_carrier_rear"] = -P["carrier_depth"]                         # -5.60
    d["z_barb_shoulder"] = d["z_pcb_rear"] - P["pin_float"]           # -2.80
    d["z_pin_tip"] = d["z_barb_shoulder"] - P["pin_head_h"]           # -4.50

    # --- PCB envelope ------------------------------------------------------
    d["pcb_x0"] = -P["oled_pcb_w"] / 2.0
    d["pcb_x1"] = P["oled_pcb_w"] / 2.0
    d["pcb_y0"] = P["oled_pcb_off_y"] - P["oled_pcb_h"] / 2.0         # -12.75
    d["pcb_y1"] = P["oled_pcb_off_y"] + P["oled_pcb_h"] / 2.0         # +20.75

    # --- glass envelope ----------------------------------------------------
    d["glass_x0"] = -P["oled_glass_w"] / 2.0
    d["glass_x1"] = P["oled_glass_w"] / 2.0
    d["glass_y0"] = P["oled_glass_off_y"] - P["oled_glass_h"] / 2.0   # -9.05
    d["glass_y1"] = P["oled_glass_off_y"] + P["oled_glass_h"] / 2.0   # +13.95

    # --- rear-entry PCB pocket --------------------------------------------
    c = P["pcb_clearance"]
    d["pocket_x0"] = d["pcb_x0"] - c
    d["pocket_x1"] = d["pcb_x1"] + c
    d["pocket_y0"] = d["pcb_y0"] - c
    d["pocket_y1"] = d["pcb_y1"] + c

    # --- forward glass window through the seating lands -------------------
    g = P["glass_clearance"]
    d["win_x0"] = d["glass_x0"] - g
    d["win_x1"] = d["glass_x1"] + g
    d["win_y0"] = d["glass_y0"] - g
    d["win_y1"] = d["glass_y1"] + g

    # --- carrier outer profile --------------------------------------------
    w = P["carrier_wall"]
    d["car_x0"] = d["pocket_x0"] - w
    d["car_x1"] = d["pocket_x1"] + w
    d["car_y0"] = d["pocket_y0"] - w
    d["car_y1"] = d["pocket_y1"] + w + P["carrier_top_flange"]
    d["wall_y1"] = d["pocket_y1"] + w                                 # top wall outer

    # --- M2 bosses ---------------------------------------------------------
    d["m2_x"] = P["panel_fix_pitch"] / 2.0
    d["m2_r"] = P["m2_boss_d"] / 2.0
    d["ear_x1"] = d["m2_x"] + d["m2_r"]
    d["ear_x0"] = d["car_x1"] - 3.5   # deep overlap: no tangent slivers

    # --- solder-tip / header relief ---------------------------------------
    d["relief_x0"] = P["tip_relief_cx"] - P["tip_relief_w"] / 2.0
    d["relief_x1"] = P["tip_relief_cx"] + P["tip_relief_w"] / 2.0

    # --- locating post positions (the four PCB holes) ---------------------
    hx = P["oled_hole_pitch_x"] / 2.0
    hy = P["oled_hole_pitch_y"] / 2.0
    d["pins"] = [(sx * hx, P["oled_pcb_off_y"] + sy * hy)
                 for sx in (-1, 1) for sy in (-1, 1)]

    # --- solder tip positions ---------------------------------------------
    n = 4
    span = (n - 1) * P["oled_tip_pitch"]
    d["tip_x"] = [P["oled_tip_cx"] - span / 2.0 + i * P["oled_tip_pitch"]
                  for i in range(n)]
    return d


# ---------------------------------------------------------------------------
# Bodies
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
        B.sub(s, B.cyl(P["panel_fix_clear_d"], sx * d["m2_x"], P["panel_fix_y"],
                       -1.0, t + 1.0))
    return [(s, "PANEL_Perspex")]


def build_oled(B, P, d):
    """REF_SH1106_1P3 - the OLED module, as separately checkable bodies."""
    out = []
    pcb = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                d["z_pcb_rear"], d["z_pcb_front"])
    for (px, py) in d["pins"]:
        B.sub(pcb, B.cyl(P["oled_hole_d"], px, py,
                         d["z_pcb_rear"] - 1.0, d["z_pcb_front"] + 1.0))
    out.append((pcb, "OLED_PCB"))
    out.append((B.box(d["glass_x0"], d["glass_x1"], d["glass_y0"], d["glass_y1"],
                      d["z_pcb_front"], d["z_glass_front"]), "OLED_Glass"))
    out.append((B.box(-P["oled_active_w"] / 2.0, P["oled_active_w"] / 2.0,
                      -P["oled_active_h"] / 2.0, P["oled_active_h"] / 2.0,
                      d["z_glass_front"] - 0.05, d["z_glass_front"]),
                "OLED_ActiveArea"))
    out.append((B.box(-P["oled_header_w"] / 2.0, P["oled_header_w"] / 2.0,
                      P["oled_header_off_y"] - P["oled_header_h"] / 2.0,
                      P["oled_header_off_y"] + P["oled_header_h"] / 2.0,
                      d["z_pcb_rear"] - P["oled_header_depth"], d["z_pcb_rear"]),
                "OLED_Header_Keepout"))
    tips = None
    z1 = d["z_pcb_front"] + P["oled_tip_proud"]
    for ty in (P["oled_tip_y_top"], P["oled_tip_y_bot"]):
        for tx in d["tip_x"]:
            c = B.cyl(P["oled_tip_d"], tx, ty, d["z_pcb_front"], z1)
            tips = c if tips is None else B.uni(tips, c)
    out.append((tips, "OLED_Solder_Tips"))
    return out


def build_carrier(B, P, d):
    """Rear_Display_Carrier - the Rev O structural part."""
    zr = d["z_carrier_rear"]
    zs = d["z_pcb_front"]           # seating-land face, -1.10

    # 1. outer envelope: rounded body + two M2 boss ears
    s = B.rrect(d["car_x0"], d["car_x1"], d["car_y0"], d["car_y1"],
                zr, 0.0, P["carrier_corner_r"])
    for sx in (-1, 1):
        x0, x1 = sx * d["ear_x0"], sx * d["ear_x1"]
        B.uni(s, B.rrect(min(x0, x1), max(x0, x1), -d["m2_r"], d["m2_r"],
                         zr, 0.0, d["m2_r"]))

    # 2. rear-entry PCB pocket, open at the rear
    B.sub(s, B.box(d["pocket_x0"], d["pocket_x1"], d["pocket_y0"], d["pocket_y1"],
                   zr - 1.0, zs))

    # 3. forward glass window through the seating lands
    B.sub(s, B.box(d["win_x0"], d["win_x1"], d["win_y0"], d["win_y1"],
                   zs, 1.0))

    # 4. solder-tip / header relief: full-height slot through the lands, so the
    #    carrier never touches a solder joint or a header pin.
    B.sub(s, B.box(d["relief_x0"], d["relief_x1"],
                   d["pocket_y0"], d["pocket_y1"], zs, 1.0))

    # 5. M2 heat-set insert bores, blind, opening at the seating face
    depth = P["m2_insert_recess"] + P["m2_insert_depth"]
    for sx in (-1, 1):
        x = sx * d["m2_x"]
        B.sub(s, B.cyl(P["m2_insert_d"], x, P["panel_fix_y"], -depth, 0.001))
        ch = P["m2_bore_chamfer"]
        B.sub(s, B.cone(P["m2_insert_d"] + 2 * ch, P["m2_insert_d"],
                        x, P["panel_fix_y"], 0.001, -ch))

    # 6. rear-open wire relief notch in the top wall
    B.sub(s, B.box(-P["wire_notch_w"] / 2.0, P["wire_notch_w"] / 2.0,
                   d["pocket_y1"], d["car_y1"] + 1.0,
                   zr - 1.0, zr + P["wire_notch_depth"]))

    # 7. cable-tie slots through the top flange (strain relief)
    for sx in (-1, 1):
        x = sx * P["tie_slot_x"]
        B.sub(s, B.box(x - P["tie_slot_w"] / 2.0, x + P["tie_slot_w"] / 2.0,
                       d["wall_y1"] - 1.0, d["car_y1"] + 1.0,
                       P["tie_slot_z"] - P["tie_slot_h"] / 2.0,
                       P["tie_slot_z"] + P["tie_slot_h"] / 2.0))

    # 8. four locating snap posts, rising rearward from the seating lands
    pd = P["locating_pin_d"]
    head_d = pd + 2 * P["pin_barb"]
    for (px, py) in d["pins"]:
        post = B.cyl(pd, px, py, d["z_barb_shoulder"], zs)
        B.uni(post, B.cone(head_d, P["pin_tip_d"], px, py,
                           d["z_barb_shoulder"], d["z_pin_tip"]))
        # split it so the legs can flex; slot runs through in Y
        B.sub(post, B.box(px - P["pin_slot_w"] / 2.0, px + P["pin_slot_w"] / 2.0,
                          py - head_d, py + head_d,
                          d["z_pin_tip"] - 0.5, zs + 0.001))
        B.uni(s, post)

    return [(s, "Rear_Display_Carrier")]


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
    vals["z_glass_front"] = d["z_glass_front"]
    vals["z_pcb_front"] = d["z_pcb_front"]
    vals["z_pcb_rear"] = d["z_pcb_rear"]
    for k in sorted(vals):
        v = vals[k]
        if not isinstance(v, (int, float)):
            continue
        expr = "{0} mm".format(v)
        try:
            ex = ups.itemByName(k)
            if ex:
                ex.expression = expr
            else:
                ups.add(k, adsk.core.ValueInput.createByString(expr), "mm",
                        "Rev O generator")
        except Exception as e:
            print("parameter %s rejected (%s) - geometry is unaffected" % (k, e))


def import_bezel(app, root, path):
    """Bring the unchanged, validated Rev N bezel in as a reference body.

    Strictly non-fatal and strictly non-disruptive. The bezel is cosmetic
    reference geometry, so it must never be able to take the build down with
    it -- and it must never switch the active document, because everything
    after this point holds references into the document we created.
    """
    if not path or not os.path.exists(path):
        print("bezel: %s not found - skipped" % path)
        return None
    before = set()
    for i in range(root.occurrences.count):
        before.add(root.occurrences.item(i).entityToken)
    try:
        opts = app.importManager.createSTEPImportOptions(path)
        app.importManager.importToTarget(opts, root)
    except Exception as e:
        # Do NOT fall back to importToNewDocument: it makes the imported file
        # the active document and every reference held here goes stale.
        print("bezel: import failed (%s) - continuing without it" % e)
        return None
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        if occ.entityToken not in before:
            print("bezel: imported as %r" % occ.name)
            return occ
    print("bezel: import reported success but added no occurrence")
    return None


# ---------------------------------------------------------------------------
# Validation - run before believing anything
# ---------------------------------------------------------------------------
def volume_of_intersection(tbm, a, b):
    ca, cb = tbm.copy(a), tbm.copy(b)
    try:
        tbm.booleanOperation(ca, cb, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    except Exception:
        return 0.0
    if ca.faces.count == 0:
        return 0.0
    return ca.volume * 1000.0        # cm3 -> mm3


def check_insertion(P, d, carrier):
    """Sweep the module forward onto its seat and look for solid carrier.

    Rev O reverses the load direction, which makes the insertion path a NEW
    failure mode. Every other check in this file is static, on the final
    seated position - and a part can be perfectly clear where it ends up
    while having no way to get there. Revs H/J/K carried this check for the
    front-loaded design; it must exist for the rear-loaded one too.
    """
    tbm = adsk.fusion.TemporaryBRepManager.get()
    B = Builder()
    rear = d["z_carrier_rear"] - 20.0

    glass = B.box(d["glass_x0"], d["glass_x1"], d["glass_y0"], d["glass_y1"],
                  rear, d["z_glass_front"])
    pcb = B.box(d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"],
                rear, d["z_pcb_front"])
    for (px, py) in d["pins"]:
        B.sub(pcb, B.cyl(P["oled_hole_d"], px, py, rear - 1.0, 1.0))
    tips = None
    for ty in (P["oled_tip_y_top"], P["oled_tip_y_bot"]):
        for tx in d["tip_x"]:
            c = B.cyl(P["oled_tip_d"], tx, ty, rear,
                      d["z_pcb_front"] + P["oled_tip_proud"])
            tips = c if tips is None else B.uni(tips, c)
    header = B.box(-P["oled_header_w"] / 2.0, P["oled_header_w"] / 2.0,
                   P["oled_header_off_y"] - P["oled_header_h"] / 2.0,
                   P["oled_header_off_y"] + P["oled_header_h"] / 2.0,
                   rear, d["z_pcb_rear"])

    print("")
    print("--- insertion corridor (module swept forward onto its seat) ---")
    blocked = []
    for name, body in (("OLED glass", glass), ("solder tips", tips),
                       ("header body", header)):
        v = volume_of_intersection(tbm, body, carrier)
        print("  %-12s swept x carrier   %s"
              % (name, "CLEAR" if v < 1e-6 else "** HIT %.4f mm3 **" % v))
        if v >= 1e-6:
            blocked.append((name, v))

    v = volume_of_intersection(tbm, pcb, carrier)
    defl = (P["locating_pin_d"] + 2 * P["pin_barb"] - P["oled_hole_d"]) / 2.0
    print("  %-12s swept x carrier   %s"
          % ("OLED PCB", "CLEAR" if v < 1e-6 else "HIT %.4f mm3" % v))
    print("               ^ barb interference fit, %.3f mm deflection per leg,"
          % defl)
    print("                 by design - the legs are sprung, the glass is not")

    if blocked:
        print("")
        print("  ** THE MODULE CANNOT REACH ITS SEAT **")
        for (px, py) in d["pins"]:
            loc = B.box(px - 3.5, px + 3.5, py - 3.5, py + 3.5, rear, 0.0)
            near = tbm.copy(carrier)
            tbm.booleanOperation(
                near, loc, adsk.fusion.BooleanTypes.IntersectionBooleanType)
            vv = (volume_of_intersection(tbm, glass, near)
                  if near.faces.count else 0.0)
            print("     glass x post (%+6.2f, %+6.2f)   %s"
                  % (px, py, "clear" if vv < 1e-6 else "FOUL %.4f mm3" % vv))
        head_r = (P["locating_pin_d"] + 2 * P["pin_barb"]) / 2.0
        for (px, py) in d["pins"]:
            if py < d["glass_y0"] < py + head_r:
                print("")
                print("     barb head at y %+.3f reaches y %+.3f; the glass lower"
                      % (py, py + head_r))
                print("     edge is at y %+.3f - they overlap by %.3f mm. The glass"
                      % (d["glass_y0"], py + head_r - d["glass_y0"]))
                print("     is rigid, and its rear face is coplanar with the PCB")
                print("     front face, so it meets the barb BEFORE the PCB hole")
                print("     does: the barb is at full diameter when they touch.")
                print("     Root cause is the reference module - the glass envelope")
                print("     overlaps the two bottom mounting holes. MEASURE IT.")
                break
    return blocked


def validate(app, design, comps, P, d):
    print("")
    print("--- Rev O interference matrix (mm3 of overlap) ---")
    carrier = comps["carrier"]
    others = [(n, b) for n, b in comps["ref"]]
    tbm = adsk.fusion.TemporaryBRepManager.get()
    for name, body in others:
        v = volume_of_intersection(tbm, carrier, body)
        print("  carrier x %-22s %s" % (name, "CLEAR" if v < 1e-6 else "HIT %.3f" % v))
    mm_ = app.measureManager
    print("")
    print("--- key clearances (mm) ---")
    for a_name, a_body, b_name, b_body in comps["pairs"]:
        try:
            r = mm_.measureMinimumDistance(a_body, b_body)
            print("  %-24s -> %-22s %.3f" % (a_name, b_name, r.value * 10.0))
        except Exception as e:
            print("  %-24s -> %-22s FAILED (%s)" % (a_name, b_name, e))
    return check_insertion(P, d, comps["carrier"])


# ---------------------------------------------------------------------------
def run(_context):
    app = adsk.core.Application.get()
    try:
        d = derive(P)

        # Check the output path first. A throw at export time rolls the whole
        # transaction back and you lose the build, so fail here instead.
        if not os.path.isdir(OUT_DIR):
            raise RuntimeError(
                "OUT_DIR does not exist: %s\n"
                "Edit OUT_DIR at the top of this script to point at your "
                "clone of the repo (the 'mechanical' folder)." % OUT_DIR)

        # A BRAND-NEW document. Rev O is not a Save-As of Rev N.
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent
        try:
            root.name = "Decca_Display_Mount_revO"
        except Exception:
            # The root component of an unsaved document often cannot be
            # renamed. Cosmetic only - do not lose the build over it.
            pass

        write_parameters(design, P, d)

        B = Builder()
        panel_occ, _ = add_component(root, "REF_Decca_Panel", build_panel(B, P, d))
        oled_occ, _ = add_component(root, "REF_SH1106_1P3", build_oled(B, P, d))
        car_occ, car_comp = add_component(root, "Rear_Display_Carrier",
                                          build_carrier(B, P, d))
        import_bezel(app, root, BEZEL_STEP)

        carrier = car_occ.bRepBodies.item(0)
        ref = [(b.name, b) for b in list(panel_occ.bRepBodies) + list(oled_occ.bRepBodies)]
        by = dict(ref)
        pairs = []
        if "OLED_Glass" in by and "PANEL_Perspex" in by:
            pairs.append(("OLED_Glass", by["OLED_Glass"],
                          "PANEL_Perspex", by["PANEL_Perspex"]))
        if "OLED_Glass" in by:
            pairs.append(("OLED_Glass", by["OLED_Glass"],
                          "Rear_Display_Carrier", carrier))
        if "OLED_Solder_Tips" in by:
            pairs.append(("OLED_Solder_Tips", by["OLED_Solder_Tips"],
                          "Rear_Display_Carrier", carrier))
        blocked = validate(app, design,
                           {"carrier": carrier, "ref": ref, "pairs": pairs},
                           P, d)

        # Exports
        cad = os.path.join(OUT_DIR, "CAD")
        stl = os.path.join(OUT_DIR, "STL")
        os.makedirs(cad, exist_ok=True)
        os.makedirs(stl, exist_ok=True)
        em = design.exportManager
        em.execute(em.createFusionArchiveExportOptions(
            os.path.join(cad, "Decca_Display_Mount_revO.f3d")))
        em.execute(em.createSTEPExportOptions(
            os.path.join(cad, "Rear_Display_Carrier_revO.step"), car_comp))
        em.execute(em.createSTEPExportOptions(
            os.path.join(cad, "Decca_Display_Mount_revO_assembly.step")))
        o = em.createSTLExportOptions(carrier,
                                      os.path.join(stl, "Rear_Display_Carrier_revO.stl"))
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(o)

        app.activeViewport.fit()
        print("")
        print("Rev O built and exported to %s" % OUT_DIR)
        print("Chosen glass-to-Perspex gap: %.2f mm" % P["oled_perspex_gap"])
        print("Solder-tip trim threshold  : %.2f mm proud of the PCB front face"
              % (P["oled_glass_proud"] + P["oled_perspex_gap"]))
        if blocked:
            print("")
            print("BLOCKING: the module cannot be inserted -")
            for n, v in blocked:
                print("  %s fouls the carrier through %.4f mm3 of its travel"
                      % (n, v))
            print("Rev O is NOT ready to print. See the build review, s.6a.")
    except Exception:
        # Print rather than messageBox: a modal dialog blocks Fusion and
        # hangs any non-interactive (MCP) run. The re-raise still gives the
        # Scripts UI its own error dialog when the script is run by hand.
        print("Rev O build failed:")
        print(traceback.format_exc())
        raise
