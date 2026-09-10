#!/usr/bin/env python3
"""Generate the dimensioned Rev A orthographic drawing PNG."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

OUT = Path(__file__).resolve().parents[1] / 'Drawings' / 'Decca_IEC_C14_Mounting_Plate_revA_views.png'
OUT.parent.mkdir(parents=True, exist_ok=True)

W,H,T,R = 40.0,50.0,3.0,2.0
CUT_W,CUT_H = 20.0,27.6
M2=[(-15.5,-8.5),(15.5,-8.5),(-15.5,8.5),(15.5,8.5)]
M3=[(0,-19.5),(0,19.5)]

fig = plt.figure(figsize=(10,11), dpi=180)
ax = fig.add_axes([0.08,0.22,0.84,0.72])
ax.set_aspect('equal')
ax.set_xlim(-29,29); ax.set_ylim(-33,34); ax.axis('off')

# Plate outline and apertures
plate = FancyBboxPatch((-W/2,-H/2),W,H,boxstyle=f"round,pad=0,rounding_size={R}",fill=False,linewidth=1.8)
ax.add_patch(plate)
ax.add_patch(Rectangle((-CUT_W/2,-CUT_H/2),CUT_W,CUT_H,fill=False,linewidth=1.6))
for x,y in M2: ax.add_patch(Circle((x,y),1.2,fill=False,linewidth=1.2))
for x,y in M3: ax.add_patch(Circle((x,y),1.7,fill=False,linewidth=1.2))
ax.axhline(0,linewidth=0.6,linestyle='--',color='black'); ax.axvline(0,linewidth=0.6,linestyle='--',color='black')

# Labels
ax.text(0,29.8,'DECCA IEC C14 MOUNTING PLATE — REV A',ha='center',va='bottom',fontsize=12,weight='bold')
ax.text(0,27.8,'ALL DIMENSIONS mm   |   TOP VIEW   |   SCALE NTS',ha='center',va='bottom',fontsize=8)
ax.text(0,0,'20.00 × 27.60\nC14 CLEAR CUT-OUT',ha='center',va='center',fontsize=8)
ax.text(11.8,18.2,'2 × Ø3.40 THRU',fontsize=8)
ax.text(-28.2,10.5,'4 × Ø2.40 THRU',fontsize=8)
ax.text(17.0,-23.5,'R2.00\n4 CORNERS',fontsize=8,ha='left')

# Dimension helper

def dim_h(x1,x2,y,ref_y1,ref_y2,text):
    ax.plot([x1,x1],[ref_y1,y],linewidth=.7,color='black'); ax.plot([x2,x2],[ref_y2,y],linewidth=.7,color='black')
    ax.annotate('',xy=(x1,y),xytext=(x2,y),arrowprops=dict(arrowstyle='<->',linewidth=.8,color='black'))
    ax.text((x1+x2)/2,y+0.8,text,ha='center',va='bottom',fontsize=8)

def dim_v(y1,y2,x,ref_x1,ref_x2,text):
    ax.plot([ref_x1,x],[y1,y1],linewidth=.7,color='black'); ax.plot([ref_x2,x],[y2,y2],linewidth=.7,color='black')
    ax.annotate('',xy=(x,y1),xytext=(x,y2),arrowprops=dict(arrowstyle='<->',linewidth=.8,color='black'))
    ax.text(x+0.8,(y1+y2)/2,text,ha='left',va='center',fontsize=8,rotation=90)

# Overall
# top dimension beyond plate
dim_h(-20,20,26.4,25,25,'40.00')
dim_v(-25,25,22.4,20,20,'50.00')
# Cutout
dim_h(-10,10,-15.8,-13.8,-13.8,'20.00')
dim_v(-13.8,13.8,-12.4,-10,-10,'27.60')
# M2 grid
dim_h(-15.5,15.5,11.8,8.5,8.5,'31.00 M2 GRID')
dim_v(-8.5,8.5,-18.2,-15.5,-15.5,'17.00 M2 GRID')
# M3 spacing
dim_v(-19.5,19.5,4.2,0,0,'39.00 M3 PITCH')

# Coordinates note
notes=(
    'HOLE CENTRES FROM PLATE CENTRE (0,0)\n'
    'M2: (±15.50, ±8.50)   |   M3: (0.00, ±19.50)\n'
    'C14 cut-out centred at (0,0)   |   plate thickness 3.00'
)
ax.text(0,-30.2,notes,ha='center',va='top',fontsize=8)

# Side view
ax2=fig.add_axes([0.13,0.07,0.74,0.11])
ax2.set_xlim(-24,24); ax2.set_ylim(-2,8); ax2.axis('off')
ax2.add_patch(Rectangle((-20,1),40,T,fill=False,linewidth=1.5))
ax2.plot([-20,-20],[-0.3,5.8],linewidth=.7,color='black'); ax2.plot([20,20],[-0.3,5.8],linewidth=.7,color='black')
ax2.annotate('',xy=(-20,5.2),xytext=(20,5.2),arrowprops=dict(arrowstyle='<->',linewidth=.8,color='black'))
ax2.text(0,5.6,'40.00',ha='center',va='bottom',fontsize=8)
ax2.plot([21.2,22.8],[1,1],linewidth=.7,color='black'); ax2.plot([21.2,22.8],[4,4],linewidth=.7,color='black')
ax2.annotate('',xy=(22.2,1),xytext=(22.2,4),arrowprops=dict(arrowstyle='<->',linewidth=.8,color='black'))
ax2.text(23.0,2.5,'3.00',ha='left',va='center',fontsize=8,rotation=90)
ax2.text(-23.3,2.5,'SIDE VIEW',fontsize=8,rotation=90,va='center')

fig.savefig(OUT,bbox_inches='tight',pad_inches=0.12)
print(OUT)
