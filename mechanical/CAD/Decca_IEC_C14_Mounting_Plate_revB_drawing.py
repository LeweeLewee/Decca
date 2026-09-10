#!/usr/bin/env python3
from pathlib import Path
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from cadquery import importers

ROOT=Path(__file__).resolve().parents[1]
STEP=ROOT/'CAD'/'Decca_IEC_C14_Mounting_Plate_revB.step'
OUT=ROOT/'Drawings'/'Decca_IEC_C14_Mounting_Plate_revB_views.png'
shape=importers.importStep(str(STEP)).val()

top=None
for f in shape.Faces():
    b=f.BoundingBox()
    if b.zlen<1e-6 and abs(b.zmin-3)<1e-6 and f.Area()>1000: top=f; break
cut=None
for w in top.Wires():
    b=w.BoundingBox()
    if 19.9<b.xlen<20.1 and 27.5<b.ylen<27.8: cut=w; break

fig=plt.figure(figsize=(12,8),dpi=180)
ax=fig.add_axes([0.05,0.08,0.56,0.84]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-26,26); ax.set_ylim(-31,31)
ax.add_patch(FancyBboxPatch((-20,-25),40,50,boxstyle='round,pad=0,rounding_size=2',fill=False,linewidth=1.8))
for e in cut.Edges():
    pts,_=e.sample(60 if e.geomType()=='CIRCLE' else 2)
    ax.plot([p.x for p in pts],[p.y for p in pts],linewidth=1.8)
for x,y in [(-15.5,-8.5),(15.5,-8.5),(-15.5,8.5),(15.5,8.5)]: ax.add_patch(Circle((x,y),1.2,fill=False,linewidth=1.1))
for x,y in [(0,-19.5),(0,19.5)]: ax.add_patch(Circle((x,y),1.7,fill=False,linewidth=1.1))
ax.axhline(0,linewidth=.5,linestyle='--'); ax.axvline(0,linewidth=.5,linestyle='--')
ax.text(0,29,'REV B — INSTALLED PLATE VIEW',ha='center',weight='bold',fontsize=11)
ax.text(0,27.2,'40 × 50 × 3 mm | C14 profile rotated 90° | 0.25 mm profile clearance',ha='center',fontsize=8)
ax.text(-11.0,0,'LONG FLAT',rotation=90,va='center',ha='center',fontsize=8)
ax.text(11.3,0,'SHORT FLAT',rotation=90,va='center',ha='center',fontsize=8)
ax.text(0,-28.6,'M2 grid 31.00 × 17.00 mm     •     M3 pitch 39.00 mm',ha='center',fontsize=8)

bx=fig.add_axes([0.65,0.12,0.31,0.76]); bx.set_aspect('equal'); bx.axis('off'); bx.set_xlim(-18,18); bx.set_ylim(-15,15)
W,H,SIDE,SHORT=27.14,19.50,14.00,16.00
w=W/2; h=H/2; s=SHORT/2; yd=h-SIDE
verts=[(-w,h),(w,h),(w,yd),(s,-h),(-s,-h),(-w,yd),(-w,h)]
bx.plot([p[0] for p in verts],[p[1] for p in verts],linewidth=1.8)
bx.text(0,13.4,'MEASURED NATIVE C14 PROFILE',ha='center',weight='bold',fontsize=10)
bx.text(0,11.8,'before 90° plate rotation',ha='center',fontsize=8)
bx.annotate('',xy=(-w,10.6),xytext=(w,10.6),arrowprops=dict(arrowstyle='<->',lw=.8)); bx.text(0,11,'27.14 overall / long flat',ha='center',fontsize=8)
bx.annotate('',xy=(10.6,-h),xytext=(10.6,h),arrowprops=dict(arrowstyle='<->',lw=.8)); bx.text(11.2,0,'19.50',rotation=90,va='center',fontsize=8)
bx.annotate('',xy=(-s,-11.1),xytext=(s,-11.1),arrowprops=dict(arrowstyle='<->',lw=.8)); bx.text(0,-12.1,'16.00 short flat',ha='center',fontsize=8)
bx.annotate('',xy=(15.0,yd),xytext=(15.0,h),arrowprops=dict(arrowstyle='<->',lw=.8)); bx.text(15.6,(yd+h)/2,'14.00 side',rotation=90,va='center',fontsize=8)
run=(W-SHORT)/2; rise=H-SIDE; angle=math.degrees(math.atan2(rise,run)); length=math.hypot(run,rise)
bx.text(0,-14.2,f'Derived each side: run {run:.2f} | rise {rise:.2f} | length {length:.2f} | angle {angle:.2f}°',ha='center',fontsize=8)
bx.text(0,-1.0,'R2.0 at the two long-flat corners\nR0.4 at the other four corners',ha='center',fontsize=8)

fig.suptitle('Decca IEC C14 Mounting Plate — Rev B',fontsize=14,weight='bold',y=.98)
fig.savefig(OUT,bbox_inches='tight',pad_inches=.15)
print(OUT)
