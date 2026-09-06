#!/usr/bin/env python3
"""Independent STEP/STL verification for Decca IEC C14 mounting plate Rev B."""
from pathlib import Path
import math, sys
from cadquery import importers
import trimesh

ROOT=Path(__file__).resolve().parents[1]
STEP=ROOT/'CAD'/'Decca_IEC_C14_Mounting_Plate_revB.step'
STL=ROOT/'STL'/'Decca_IEC_C14_Mounting_Plate_revB.stl'
TOL=1e-5

def near(a,b,tol=TOL): return abs(a-b)<=tol

def main():
    fail=[]
    def check(name,ok,detail):
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
        if not ok: fail.append(name)

    shape=importers.importStep(str(STEP)).val(); bb=shape.BoundingBox()
    check('B1 envelope',near(bb.xlen,40) and near(bb.ylen,50) and near(bb.zlen,3),f'{bb.xlen:.6f} x {bb.ylen:.6f} x {bb.zlen:.6f} mm')
    check('B2 one STEP solid',len(shape.Solids())==1,f'{len(shape.Solids())} solid')

    top=None
    for f in shape.Faces():
        b=f.BoundingBox()
        if b.zlen<TOL and near(b.zmin,3) and f.Area()>1000: top=f; break
    check('B3 top face found',top is not None,'top planar face')
    if top is None: return 1

    cut=None; holes=[]
    for w in top.Wires():
        b=w.BoundingBox()
        if 19.9 < b.xlen < 20.1 and 27.5 < b.ylen < 27.8: cut=w
        elif b.xlen < 4 and b.ylen < 4: holes.append(w)
    check('B4 six-sided profile cutout found',cut is not None,'20.00 x 27.64 mm rotated clear envelope')
    if cut is None: return 1

    lines=[e for e in cut.Edges() if e.geomType()=='LINE']
    arcs=[e for e in cut.Edges() if e.geomType()=='CIRCLE']
    radii=sorted(round(e.radius(),6) for e in arcs)
    check('B5 profile topology',len(lines)==6 and len(arcs)==6,f'{len(lines)} lines + {len(arcs)} arcs')
    check('B6 profile corner radii',radii==[0.65,0.65,0.65,0.65,2.25,2.25],f'cut radii {radii} mm')

    diag=[]
    for e in lines:
        if 7.0 < e.Length() < 8.0:
            p=e.Vertices(); a=p[0].toTuple(); b=p[1].toTuple()
            angle=math.degrees(math.atan2(abs(b[1]-a[1]),abs(b[0]-a[0])))
            diag.append(angle)
    check('B7 two diagonal segments',len(diag)==2,f'angles after 90° rotation {diag}')
    expected_rot=90-math.degrees(math.atan2(5.5,5.57))
    check('B8 diagonal angle',len(diag)==2 and all(abs(a-expected_rot)<1e-6 for a in diag),f'{diag[0]:.6f}° rotated; native 44.637701°' if diag else 'not found')

    m2=[]; m3=[]
    for w in holes:
        b=w.BoundingBox(); c=w.Center()
        if near(b.xlen,2.4,1e-4): m2.append((round(c.x,6),round(c.y,6),w))
        elif near(b.xlen,3.4,1e-4): m3.append((round(c.x,6),round(c.y,6),w))
    m2c=sorted((x,y) for x,y,_ in m2); m3c=sorted((x,y) for x,y,_ in m3)
    exp2=sorted([(-15.5,-8.5),(15.5,-8.5),(-15.5,8.5),(15.5,8.5)])
    exp3=sorted([(0,-19.5),(0,19.5)])
    check('B9 M2 pattern',m2c==exp2,f'{m2c}')
    check('B10 M3 pattern',m3c==exp3,f'{m3c}; pitch 39.00 mm')

    gaps=[cut.distance(w) for _,_,w in m2+m3]
    m2g=[cut.distance(w) for _,_,w in m2]; m3g=[cut.distance(w) for _,_,w in m3]
    check('B11 no intersections',min(gaps)>0,f'min edge gap {min(gaps):.6f} mm')
    check('B12 ligament >=3 mm',min(gaps)>=3,f'M2 min {min(m2g):.6f}; M3 min {min(m3g):.6f} mm')

    mesh=trimesh.load_mesh(STL,process=True); ext=mesh.bounds[1]-mesh.bounds[0]
    check('B13 STL envelope',all(abs(float(a)-b)<2e-4 for a,b in zip(ext,(40,50,3))),f'{ext[0]:.6f} x {ext[1]:.6f} x {ext[2]:.6f}')
    check('B14 STL manifold',bool(mesh.is_watertight) and bool(mesh.is_winding_consistent),f'watertight={mesh.is_watertight}; winding={mesh.is_winding_consistent}')
    check('B15 STL one body',mesh.body_count==1,f'body count {mesh.body_count}')

    print(f'STEP volume {shape.Volume():.6f} mm^3; STL volume {abs(float(mesh.volume)):.6f} mm^3')
    if fail:
        print('FAILED: '+', '.join(fail),file=sys.stderr); return 1
    print('REV B CAD PASS — physical profile fit still required')
    return 0

if __name__=='__main__': raise SystemExit(main())
