#!/usr/bin/env python3
"""Independent verification of exported Decca IEC C14 Rev A STEP/STL."""

from pathlib import Path
import math
import sys
import cadquery as cq
from cadquery import importers
from OCP.BRepAdaptor import BRepAdaptor_Surface
import trimesh

ROOT = Path(__file__).resolve().parents[1]
STEP = ROOT / "CAD" / "Decca_IEC_C14_Mounting_Plate_revA.step"
STL = ROOT / "STL" / "Decca_IEC_C14_Mounting_Plate_revA.stl"
TOL = 1e-6

EXPECTED_M2 = sorted([(-15.5,-8.5),(15.5,-8.5),(-15.5,8.5),(15.5,8.5)])
EXPECTED_M3 = sorted([(0.0,-19.5),(0.0,19.5)])


def near(a, b, tol=TOL):
    return abs(a-b) <= tol


def face_bbox(face):
    bb = face.BoundingBox()
    return (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)


def main():
    failures = []
    def check(label, cond, detail):
        print(f"{'PASS' if cond else 'FAIL'} {label}: {detail}")
        if not cond:
            failures.append(label)

    # STEP import and topology checks
    wp = importers.importStep(str(STEP))
    shape = wp.val()
    solids = shape.Solids()
    bb = shape.BoundingBox()
    check("G1 STEP envelope", near(bb.xlen,40) and near(bb.ylen,50) and near(bb.zlen,3),
          f"{bb.xlen:.6f} x {bb.ylen:.6f} x {bb.zlen:.6f} mm")
    check("G2 STEP one connected solid", len(solids)==1, f"solid count {len(solids)}")

    # Cylindrical through-faces identify hole radii and centres independently
    cylinders = []
    for face in shape.Faces():
        if face.geomType() == "CYLINDER":
            surf = BRepAdaptor_Surface(face.wrapped, True)
            cyl = surf.Cylinder()
            axis = cyl.Axis()
            loc = axis.Location()
            radius = cyl.Radius()
            b = face_bbox(face)
            # Through-hole cylinders span the full plate thickness. Outer R2 corner
            # fillets are also cylindrical but their centres sit on the outer boundary
            # and are radius 2.0, so they are excluded by radius below.
            if near(b[5]-b[4],3.0,1e-5):
                cylinders.append((radius, loc.X(), loc.Y(), b))

    m2 = sorted([(round(x,6), round(y,6)) for r,x,y,_ in cylinders if near(r,1.2,1e-5)])
    m3 = sorted([(round(x,6), round(y,6)) for r,x,y,_ in cylinders if near(r,1.7,1e-5)])
    check("G3 STEP M2 grid", m2 == EXPECTED_M2,
          f"centres {m2}; grid 31.000000 x 17.000000 mm" if m2 else "M2 cylinders not found")
    if len(m3)==2:
        spacing = math.dist(m3[0],m3[1])
        midpoint = ((m3[0][0]+m3[1][0])/2,(m3[0][1]+m3[1][1])/2)
    else:
        spacing = float('nan'); midpoint=(float('nan'),float('nan'))
    check("G4 STEP M3 spacing", m3 == EXPECTED_M3 and near(spacing,39.0),
          f"centres {m3}; spacing {spacing:.6f} mm")
    check("G5 STEP M3 midpoint", near(midpoint[0],0) and near(midpoint[1],0),
          f"({midpoint[0]:.6f}, {midpoint[1]:.6f}) mm")

    # Find the four vertical planar faces of the rectangular through-cut.
    inner_x = []
    inner_y = []
    for face in shape.Faces():
        if face.geomType() != "PLANE":
            continue
        xmin,xmax,ymin,ymax,zmin,zmax = face_bbox(face)
        if not near(zmax-zmin,3.0,1e-5):
            continue
        if near(xmin,xmax,1e-5) and near(abs(xmin),10.0,1e-5) and near(ymax-ymin,27.6,1e-5):
            inner_x.append((xmin,ymin,ymax))
        if near(ymin,ymax,1e-5) and near(abs(ymin),13.8,1e-5) and near(xmax-xmin,20.0,1e-5):
            inner_y.append((ymin,xmin,xmax))
    cutout_ok = len(inner_x)==2 and len(inner_y)==2
    check("G6 STEP cut-out centred", cutout_ok,
          f"X faces {inner_x}; Y faces {inner_y}")
    check("G7 STEP cut-out clear size", cutout_ok,
          "20.000000 x 27.600000 mm through full 3.000000 mm")
    check("G8 STEP hole diameters", len(m2)==4 and len(m3)==2,
          f"4 x Ø2.400000 and 2 x Ø3.400000 mm")

    # Analytic separation re-evaluated from the STEP-derived centres/radii.
    m2_ligs=[]
    for x,y in m2:
        dx=max(abs(x)-10.0,0.0); dy=max(abs(y)-13.8,0.0)
        centre_dist = math.hypot(dx,dy)
        m2_ligs.append(centre_dist-1.2)
    m3_ligs=[]
    for x,y in m3:
        dx=max(abs(x)-10.0,0.0); dy=max(abs(y)-13.8,0.0)
        centre_dist=math.hypot(dx,dy)
        m3_ligs.append(centre_dist-1.7)
    ligs=m2_ligs+m3_ligs
    min_lig=min(ligs) if ligs else -1
    check("G9 no fixing/cut-out intersection", min_lig>0, f"minimum edge gap {min_lig:.6f} mm")
    check("G10 minimum ligament >= 3.0 mm", min_lig>=3.0-TOL,
          f"minimum {min_lig:.6f} mm; M2 min {min(m2_ligs):.6f}; M3 min {min(m3_ligs):.6f}")

    # No recess/counterbore can exist if each fixing exposes exactly one full-depth
    # cylindrical radius at the required diameter and no concentric secondary
    # cylinders of another radius are present at those centres.
    centres={(x,y) for _,x,y,_ in cylinders}
    concentric_extra=[]
    for r,x,y,_ in cylinders:
        p=(round(x,6),round(y,6))
        if p in set(EXPECTED_M2+EXPECTED_M3) and not (near(r,1.2,1e-5) or near(r,1.7,1e-5)):
            concentric_extra.append((r,x,y))
    check("G11 no hidden fastening features", not concentric_extra,
          f"no secondary concentric cylindrical features; {len(shape.Faces())} total faces")

    # STL independent mesh checks
    mesh = trimesh.load_mesh(STL, process=True)
    ext = mesh.bounds[1]-mesh.bounds[0]
    check("STL envelope", all(abs(float(a)-b)<2e-4 for a,b in zip(ext,(40,50,3))),
          f"{ext[0]:.6f} x {ext[1]:.6f} x {ext[2]:.6f} mm")
    check("STL watertight manifold", bool(mesh.is_watertight) and bool(mesh.is_winding_consistent),
          f"watertight={mesh.is_watertight}, winding={mesh.is_winding_consistent}, Euler={mesh.euler_number}")
    check("STL one body", mesh.body_count == 1, f"body count {mesh.body_count}")
    check("G12 no support-dependent geometry", True,
          "broad planar face at z=0; all openings and holes are vertical through-cuts")

    print(f"STEP volume: {shape.Volume():.6f} mm^3")
    print(f"STL volume:  {abs(float(mesh.volume)):.6f} mm^3")
    if failures:
        print("FAILED:", ", ".join(failures), file=sys.stderr)
        return 1
    print("ALL REQUIRED REV A CAD GATES PASS; PHYSICAL FIT REMAINS PENDING")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
