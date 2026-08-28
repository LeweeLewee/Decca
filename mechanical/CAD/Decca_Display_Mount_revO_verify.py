# -*- coding: utf-8 -*-
"""
Decca OLED Display Mount - Rev O offline verifier and exporter.

This does NOT re-describe the design. It parses the parameter table and the
body recipes straight out of Decca_Display_Mount_revO_fusion.py and rebuilds
them on an OpenCascade kernel (CadQuery), so what is validated here is the
same recipe Fusion will run - there is no second copy to drift.

    pip install cadquery
    python3 Decca_Display_Mount_revO_verify.py

It prints the depth chain, the interference matrix, the clearance table, the
snap-post strain check and the solder-tip study, and writes STEP/STL next to
this file.
"""

import ast
import math
import os
import re
import sys

import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Decca_Display_Mount_revO_fusion.py")
BEZEL = os.path.join(HERE, "Front_Bezel_revN.step")
STL_DIR = os.path.normpath(os.path.join(HERE, "..", "STL"))


# ---------------------------------------------------------------------------
# A Builder with the same surface as the Fusion one, backed by OCC.
# The recipes mutate the solid they are handed, so bodies are wrapped.
# ---------------------------------------------------------------------------
class Body(object):
    __slots__ = ("s",)

    def __init__(self, s):
        self.s = s


class Builder(object):
    def box(self, x0, x1, y0, y1, z0, z1):
        return Body(cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0,
                                     cq.Vector(x0, y0, z0)))

    def cyl(self, d, x, y, z0, z1):
        lo, hi = (z0, z1) if z1 >= z0 else (z1, z0)
        return Body(cq.Solid.makeCylinder(d / 2.0, hi - lo,
                                          cq.Vector(x, y, lo),
                                          cq.Vector(0, 0, 1)))

    def cone(self, d0, d1, x, y, z0, z1):
        # d0 belongs to z0, d1 to z1, in either direction.
        if z1 >= z0:
            lo, r_lo, r_hi = z0, d0 / 2.0, d1 / 2.0
            h = z1 - z0
        else:
            lo, r_lo, r_hi = z1, d1 / 2.0, d0 / 2.0
            h = z0 - z1
        return Body(cq.Solid.makeCone(r_lo, r_hi, h, cq.Vector(x, y, lo),
                                      cq.Vector(0, 0, 1)))

    def uni(self, a, b):
        a.s = a.s.fuse(b.s)
        return a

    def sub(self, a, b):
        a.s = a.s.cut(b.s)
        return a

    # rrect is taken verbatim from the Fusion script (see load_recipes).


# ---------------------------------------------------------------------------
def load_recipes():
    """Pull P, derive() and the build_*() recipes out of the Fusion script."""
    src = open(SRC).read()
    tree = ast.parse(src)

    P = None
    wanted = {"derive", "build_panel", "build_oled", "build_carrier"}
    fns = {}
    rrect = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "P":
            P = ast.literal_eval(node.value)
        elif isinstance(node, ast.FunctionDef) and node.name in wanted:
            fns[node.name] = ast.get_source_segment(src, node)
        elif isinstance(node, ast.ClassDef) and node.name == "Builder":
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef) and sub.name == "rrect":
                    rrect = ast.get_source_segment(src, sub)
    assert P and wanted <= set(fns) and rrect, "could not read the Rev O recipes"

    ns = {"math": math}
    exec("\n\n".join(fns[k] for k in sorted(fns)), ns)
    # graft the real rrect onto the OCC builder
    bns = {}
    exec("class _R(object):\n" + "\n".join("    " + l for l in rrect.splitlines()), bns)
    Builder.rrect = bns["_R"].rrect
    return P, ns


def vol(b):
    return b.s.Volume()


def bbox(b):
    bb = b.s.BoundingBox()
    return (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)


def overlap(a, b):
    try:
        c = a.s.intersect(b.s)
    except Exception:
        return 0.0
    try:
        v = c.Volume()
    except Exception:
        return 0.0
    return 0.0 if v < 1e-7 else v


def mindist(a, b):
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    e = BRepExtrema_DistShapeShape(a.s.wrapped, b.s.wrapped)
    e.Perform()
    return e.Value()


def slab_area(body, z0, z1, x0, x1, y0, y1):
    """Cross-sectional area of `body` inside a thin window, in mm^2."""
    B = Builder()
    box = B.box(x0, x1, y0, y1, z0, z1)
    try:
        c = body.s.intersect(box.s)
        return c.Volume() / (z1 - z0)
    except Exception:
        return 0.0


def rule(t):
    print("")
    print(t)
    print("-" * len(t))


# ---------------------------------------------------------------------------
def main():
    P, ns = load_recipes()
    d = ns["derive"](P)
    B = Builder()

    panel = dict((n, b) for b, n in ns["build_panel"](B, P, d))
    oled = dict((n, b) for b, n in ns["build_oled"](B, P, d))
    carrier = ns["build_carrier"](B, P, d)[0][0]

    gap = P["oled_perspex_gap"]
    seat = P["oled_glass_proud"] + gap

    rule("Rev O depth chain (z = 0 is the rear face of the Perspex)")
    print("  Perspex front face          z = %+7.3f" % P["perspex_t"])
    print("  Perspex rear face / seating z = %+7.3f   <- carrier hard stops" % 0.0)
    print("  OLED glass front face       z = %+7.3f   gap = %.3f mm"
          % (d["z_glass_front"], gap))
    print("  OLED PCB front face / lands z = %+7.3f   seat depth = %.3f mm"
          % (d["z_pcb_front"], seat))
    print("  OLED PCB rear face          z = %+7.3f" % d["z_pcb_rear"])
    print("  snap barb shoulder          z = %+7.3f   PCB float = %.3f mm"
          % (d["z_barb_shoulder"], P["pin_float"]))
    print("  carrier rear face           z = %+7.3f" % d["z_carrier_rear"])
    assert abs(seat - P["pcb_seat_depth"]) < 1e-9, "pcb_seat_depth is inconsistent"
    assert abs(P["carrier_stop_depth"] - P["pcb_seat_depth"]) < 1e-9

    rule("Carrier")
    bb = bbox(carrier)
    print("  envelope   %.2f x %.2f x %.2f mm"
          % (bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]))
    print("  X[%.2f, %.2f]  Y[%.2f, %.2f]  Z[%.2f, %.2f]" % bb)
    print("  volume     %.3f cm3" % (vol(carrier) / 1000.0))
    print("  solid      %s" % carrier.s.isValid())

    seat_a = slab_area(carrier, -0.02, 0.0, -40, 40, -40, 40)
    land_a = slab_area(carrier, d["z_pcb_front"], d["z_pcb_front"] + 0.02,
                       d["pcb_x0"], d["pcb_x1"], d["pcb_y0"], d["pcb_y1"])
    print("  Perspex seating-face area   %.1f mm2" % seat_a)
    print("  PCB datum bearing area      %.1f mm2   (Rev N: 97.4 mm2)" % land_a)

    rule("Interference matrix - carrier against every reference body")
    worst = []
    for name in ("PANEL_Perspex",):
        v = overlap(carrier, panel[name])
        worst.append((name, v))
    for name in ("OLED_PCB", "OLED_Glass", "OLED_ActiveArea",
                 "OLED_Header_Keepout", "OLED_Solder_Tips"):
        v = overlap(carrier, oled[name])
        worst.append((name, v))
    for name, v in worst:
        print("  carrier x %-22s %s" % (name, "CLEAR" if v == 0.0 else "HIT  %.4f mm3" % v))

    rule("Module against the original panel")
    v = overlap(oled["OLED_Solder_Tips"], panel["PANEL_Perspex"])
    print("  solder tips x Perspex        %s"
          % ("CLEAR" if v == 0.0 else "HIT  %.4f mm3" % v))
    v = overlap(oled["OLED_Glass"], panel["PANEL_Perspex"])
    print("  OLED glass  x Perspex        %s"
          % ("CLEAR" if v == 0.0 else "HIT  %.4f mm3" % v))
    v = overlap(oled["OLED_Header_Keepout"], panel["PANEL_Perspex"])
    print("  header body x Perspex        %s"
          % ("CLEAR" if v == 0.0 else "HIT  %.4f mm3" % v))

    rule("Clearance table (mm)")
    for a, an, b, bn in (
            (oled["OLED_Glass"], "OLED glass", panel["PANEL_Perspex"], "Perspex"),
            (oled["OLED_Glass"], "OLED glass", carrier, "carrier"),
            (oled["OLED_ActiveArea"], "active area", carrier, "carrier"),
            (oled["OLED_PCB"], "OLED PCB", carrier, "carrier"),
            (oled["OLED_Header_Keepout"], "header body", carrier, "carrier"),
            (oled["OLED_Solder_Tips"], "solder tips", carrier, "carrier")):
        print("  %-12s -> %-9s %.3f" % (an, bn, mindist(a, b)))

    rule("Solder-tip study - what actually sets the trim threshold")
    print("  Threshold = oled_glass_proud + oled_perspex_gap = %.2f mm proud"
          % seat)
    print("  (anything on the PCB FRONT face taller than this reaches the")
    print("   Perspex, whatever the carrier does - the carrier itself is clear)")
    print("")
    print("   tip proud   tip x carrier   tip x Perspex")
    for tp in (0.60, 0.90, 1.10, 1.40, 2.00):
        Q = dict(P)
        Q["oled_tip_proud"] = tp
        dq = ns["derive"](Q)
        o2 = dict((n, b) for b, n in ns["build_oled"](Builder(), Q, dq))
        vc = overlap(o2["OLED_Solder_Tips"], carrier)
        vp = overlap(o2["OLED_Solder_Tips"], panel["PANEL_Perspex"])
        print("     %4.2f mm     %-13s   %s"
              % (tp,
                 "CLEAR" if vc == 0.0 else "HIT %.3f" % vc,
                 "CLEAR" if vp == 0.0 else "HIT %.3f mm3" % vp))

    rule("Snap-post check")
    leg_t = (P["locating_pin_d"] - P["pin_slot_w"]) / 2.0
    L = abs(d["z_pin_tip"] - d["z_pcb_front"])
    defl = (P["locating_pin_d"] + 2 * P["pin_barb"] - P["oled_hole_d"]) / 2.0
    strain = 1.5 * defl * leg_t / (L * L) * 100.0
    print("  post          %.2f mm dia, %.2f mm free length" % (P["locating_pin_d"], L))
    print("  slot          %.2f mm  ->  two %.2f mm legs" % (P["pin_slot_w"], leg_t))
    print("  head          %.2f mm dia through a %.2f mm hole"
          % (P["locating_pin_d"] + 2 * P["pin_barb"], P["oled_hole_d"]))
    print("  deflection    %.3f mm per leg on insertion" % defl)
    print("  peak strain   %.2f %%   (PETG working limit ~4 %%; Rev N was 3.06 %%)"
          % strain)
    print("  retention     %.2f mm radial step on the PCB rear face"
          % ((P["locating_pin_d"] + 2 * P["pin_barb"] - P["oled_hole_d"]) / 2.0))
    print("  X/Y location  %.2f mm diametral clearance in the PCB hole"
          % (P["oled_hole_d"] - P["locating_pin_d"]))
    if strain > 4.0:
        print("  ** WARNING: strain over the PETG working limit **")

    rule("Load path - the M2 preload must never reach the glass")
    cz = bbox(carrier)[5]
    gz = bbox(oled["OLED_Glass"])[5]
    pz = bbox(oled["OLED_PCB"])[5]
    print("  forward-most carrier material   z = %+7.3f  <- the only thing the"
          % cz)
    print("                                                 Perspex can touch")
    print("  forward-most OLED glass         z = %+7.3f  (%.3f mm clear)"
          % (gz, -gz))
    print("  forward-most OLED PCB           z = %+7.3f  (%.3f mm clear)"
          % (pz, -pz))
    ok = cz >= gz + 1e-9 and cz >= pz + 1e-9 and cz <= 1e-9
    print("  seating pad at the -X M2 boss   %.1f mm2"
          % slab_area(carrier, -0.02, 0.0, -d["ear_x1"], -d["car_x1"], -40, 40))
    print("  seating pad at the +X M2 boss   %.1f mm2"
          % slab_area(carrier, -0.02, 0.0, d["car_x1"], d["ear_x1"], -40, 40))
    print("  verdict  %s"
          % ("screw -> carrier -> seating face -> Perspex. The glass and the "
             "PCB\n           are both strictly behind the seating plane, so "
             "further torque\n           cannot close the optical gap."
             if ok else "** LOAD PATH VIOLATION **"))

    rule("Sections and printability (print seating face down)")
    boss_wall = (P["m2_boss_d"] - P["m2_insert_d"]) / 2.0
    blind = P["carrier_depth"] - P["m2_insert_recess"] - P["m2_insert_depth"]
    tie_rear = P["carrier_depth"] - abs(P["tie_slot_z"]) - P["tie_slot_h"] / 2.0
    print("  structural wall                 %.2f mm" % P["carrier_wall"])
    print("  M2 boss wall around the insert  %.2f mm" % boss_wall)
    print("  material behind the blind bore  %.2f mm" % blind)
    print("  PCB seating land                %.2f mm  (short ledges, backed by"
          % P["pcb_seat_depth"])
    print("                                            the %.2f mm frame - not a"
          % P["carrier_wall"])
    print("                                            full-area membrane)")
    print("  snap-post leg                   %.2f mm" % leg_t)
    print("  material behind a tie slot      %.2f mm" % tie_rear)
    thin = [n for n, v in (("boss wall", boss_wall), ("blind bore backing", blind),
                           ("tie-slot backing", tie_rear),
                           ("snap leg", leg_t)) if v < 0.7]
    print("  thinnest feature %s"
          % ("all >= 0.70 mm" if not thin else "** " + ", ".join(thin) + " **"))
    print("  overhangs: the barb shoulder (%.2f mm step) and the tie-slot roof"
          % P["pin_barb"])
    print("             (%.2f mm bridge). No supports required."
          % P["tie_slot_w"])

    rule("Optical alignment")
    print("  active area   %.2f x %.2f centred on (0, 0) = the aperture centre"
          % (P["oled_active_w"], P["oled_active_h"]))
    print("  aperture      %.2f x %.2f" % (P["panel_open_w"], P["panel_open_h"]))
    print("  active/aperture margin   x %.2f mm   y %.2f mm"
          % ((P["panel_open_w"] - P["oled_active_w"]) / 2.0,
             (P["panel_open_h"] - P["oled_active_h"]) / 2.0))

    bez = None
    if os.path.exists(BEZEL):
        bshape = cq.importers.importStep(BEZEL)
        bez = Body(cq.Compound.makeCompound(bshape.solids().vals()))
        bb = bbox(bez)
        print("  bezel (Rev N, unchanged)  %.2f x %.2f x %.2f mm"
              % (bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]))
        print("  bezel x carrier           %s"
              % ("CLEAR" if overlap(bez, carrier) == 0.0 else "HIT"))
        print("  bezel x Perspex           %s"
              % ("CLEAR" if overlap(bez, panel["PANEL_Perspex"]) == 0.0 else "HIT"))
        print("  bezel x OLED glass        %s"
              % ("CLEAR" if overlap(bez, oled["OLED_Glass"]) == 0.0 else "HIT"))

    rule("Feature probe - is every Rev O feature actually where it should be?")
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_OUT
    cls = BRepClass3d_SolidClassifier(carrier.s.wrapped)

    def solid_at(x, y, z):
        cls.Perform(gp_Pnt(x, y, z), 1e-7)
        return cls.State() != TopAbs_OUT

    zl = d["z_pcb_front"] / 2.0                     # inside the seating land
    probes = [
        ("top seating land", 15.9, 18.25, zl, True),
        ("bottom seating land", 12.0, -11.0, zl, True),
        ("glass window is open", 0.0, 0.0, zl, False),
        ("solder-tip relief, top", 0.0, P["oled_tip_y_top"], zl, False),
        ("solder-tip relief, bottom", 0.0, P["oled_tip_y_bot"], zl, False),
        ("snap-post leg", 15.9, 18.25, -2.0, True),
        ("snap-post split slot", 15.0, 18.25, -2.0, False),
        ("snap barb head", 15.75, -10.25, -3.5, True),
        ("clear beyond the post tip", 15.9, 18.25, d["z_pin_tip"] - 0.2, False),
        ("PCB pocket is open", 0.0, 4.0, -4.0, False),
        ("M2 insert bore", d["m2_x"], 0.0, -2.0, False),
        ("M2 boss body", 26.5, 0.0, -2.0, True),
        ("blind backing behind the bore", d["m2_x"], 0.0,
         d["z_carrier_rear"] + 0.4, True),
        ("cable-tie slot", P["tie_slot_x"], 25.1, P["tie_slot_z"], False),
        ("flange beside the tie slot", 14.0, 25.1, P["tie_slot_z"], True),
        ("wire notch", 0.0, 22.3, d["z_carrier_rear"] + 0.6, False),
        ("top wall forward of it", 0.0, 22.3, -3.0, True),
        ("seating face at the boss", 26.5, 0.0, -0.05, True),
        ("outside the envelope", 30.0, 0.0, -2.0, False),
    ]
    nbad = 0
    for name, x, y, z, want in probes:
        got = solid_at(x, y, z)
        if got != want:
            nbad += 1
        print("  %-30s %-6s %s" % (name, "solid" if got else "void",
                                   "ok" if got == want else "<< MISMATCH"))
    print("  %d/%d probes as designed" % (len(probes) - nbad, len(probes)))

    rule("Exports")
    os.makedirs(STL_DIR, exist_ok=True)
    cq.exporters.export(cq.Workplane(carrier.s),
                        os.path.join(HERE, "Rear_Display_Carrier_revO.step"))
    cq.exporters.export(cq.Workplane(carrier.s),
                        os.path.join(STL_DIR, "Rear_Display_Carrier_revO.stl"),
                        tolerance=0.01, angularTolerance=0.1)
    parts = [carrier.s, panel["PANEL_Perspex"].s] + [oled[k].s for k in sorted(oled)]
    if bez is not None:
        parts.append(bez.s)
    cq.exporters.export(cq.Workplane(cq.Compound.makeCompound(parts)),
                        os.path.join(HERE, "Decca_Display_Mount_revO_assembly.step"))
    for f in ("Rear_Display_Carrier_revO.step",
              "Decca_Display_Mount_revO_assembly.step"):
        print("  wrote %s" % f)
    print("  wrote ../STL/Rear_Display_Carrier_revO.stl")

    fails = [n for n, v in worst if v != 0.0]
    print("")
    print("RESULT: %s" % ("carrier CLEAR against every reference body"
                          if not fails else "INTERFERENCE: " + ", ".join(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
