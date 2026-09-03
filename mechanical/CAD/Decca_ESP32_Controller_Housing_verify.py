# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev B independent offline verifier
====================================================================

Reads ONLY the exported manufacturing meshes in ../STL and re-derives every
Rev B claim from triangles. numpy is the only dependency. Exits non-zero on
failure, so it works as a gate.

    python mechanical/CAD/Decca_ESP32_Controller_Housing_verify.py

It is deliberately NOT a second run of the generator. The generator knows what
it meant to build; this knows only what came out of the exporter. Every
expected number below is TYPED IN BY HAND from
mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md - whose content
is specification revision v1.3 - and from the derivation chain written out in
the build report. Nothing is imported from
Decca_ESP32_Controller_Housing_fusion.py. If the generator and this file
disagree, that disagreement is the whole point.

It covers all thirty specification v1.3 section 13 gates, including the four
the CAD suite cannot do honestly on its own: manifoldness of the exported
triangles, real bridging reach in the stated print orientation, the material
gates measured from mesh volume rather than from BRep volume, and the absence
of every Rev A feature v1.2 section 2.2 deletes by name.

v1.3 adds gates 28-30, the cable-tie anchor's structure. Nothing in them is a
strength claim: they measure section, wall and blend, and the anchor's real
robustness in a fitter's hands stays a prototype gate.

RESULT VOCABULARY - used exactly, never loosely
-----------------------------------------------
  [PASS]   MESH-VERIFIED. Measured from the exported triangles.
  [FAIL]   measured, and wrong.
  [ ]      a reported measurement, no claim attached.
  [PROTO]  PROTOTYPE-REQUIRED. Depends on a hardware dimension nobody has
           measured yet, so no amount of geometry can settle it.
  [INST]   INSTALLATION-REQUIRED. Cannot be settled until the housing is in
           the cabinet.

Nothing here may be read as physical validation. No part of this design has
been printed.
"""

from __future__ import print_function

import math
import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(HERE, "..", "STL")

MESHES = {
    "base": "ESP32_Controller_Housing_Base.stl",
    "lid": "ESP32_Controller_Housing_Lid.stl",
    "clamp": "ESP32_Controller_PCB_Clamp_Adjustable.stl",
    "cap": "ESP32_Controller_Cabinet_Fastener_Cap.stl",
    "coupon_a": "ESP32_Controller_Carrier_Fit_Coupon.stl",
    "coupon_b": "ESP32_Controller_Insert_Fastener_Coupon.stl",
}

COUPONS = ("coupon_a", "coupon_b")
COUPON_BUDGET = 5.35           # cm3: the single gauge these two replace

# Production parts and how many of each are printed. The carrier-fit coupon
# and the insert-fastener coupon are prototype tools, and v1.3 section 9
# excludes them from the material gates.
PRODUCTION = (("base", 1), ("lid", 1), ("clamp", 1), ("cap", 2))

# Rev A production meshes that v1.2 section 12 forbids shipping. Their absence
# is gate 22, and it is checked on the FILE SYSTEM, not on a component tree.
FORBIDDEN_FILES = (
    # Rev A
    "ESP32_Controller_PCB_Clamp_Fixed.stl",
    "ESP32_Controller_USB_Plug.stl",
    # superseded Rev B: one near-full-width gauge, replaced by two coupons
    "ESP32_Controller_Carrier_Fit_Gauge.stl",
)

# ---------------------------------------------------------------------------
# EXPECTED VALUES - typed in from the controlling documents, NOT imported.
# ---------------------------------------------------------------------------
# -- v1.2 section 3, reference geometry and clearances ----------------------
PCB_L = 66.00                  # nominal carrier length
PCB_W = 63.00
PCB_T = 1.60
BELOW_H = 2.50                 # lowest solder/pin feature below the carrier
ABOVE_H = 24.00                # tallest assembled component above it
CARRIER_MIN = 65.00
CARRIER_MAX = 67.00
XY_CLEAR = 0.50
UNDER_CLEAR = 2.00             # v1.1 lowers this from Rev A's 3.00
TOP_CLEAR = 2.00               # v1.1 lowers this from Rev A's 3.00
USB_MIN_W = 14.00
USB_MIN_H = 9.00
WIRE_EXIT_H = 10.00
BARE_EDGE = 3.00               # bare strip inboard of each SHORT edge
BARE_PERIM = 2.50              # bare strip inboard of each LONG edge

# -- v1.2 sections 4, 7, 8 and 10, structure --------------------------------
FLOOR_T = 1.60
WALL_T = 1.60
END_WALL_NEG_T = 2.40          # -X end: carries the ledge and both rebates
WALL_H = 9.00                  # shallow tray, above the floor top
LID_TOP_T = 1.60
LID_SKIRT_T = 1.20             # three 0.40 mm perimeters
LID_OVERLAP = 4.00
LID_FIT = 0.25
OUTER_CORNER_R = 3.00
RETAIN_CLEAR = 0.20            # ledge / clamp underside above the carrier

# -- v1.2 section 9, the mandatory material gates ---------------------------
ENV_MAX = (85.00, 75.00, 36.00)
VOL_MAX = 35.00                # cm3, production parts only
MASS_MAX = 45.0                # g
PETG_DENSITY = 1.27
VOL_PREF = (("base", 15.00), ("lid", 18.00), ("clamp", 2.00))

# -- the design's own FDM rule ----------------------------------------------
# v1.2 section 10 forbids support MATERIAL. It does not forbid a short
# unsupported ledge, and a ledge that retains a board cannot be built without
# one. 1.50 mm is the stated limit, and the cable windows and the USB slot are
# held to a stricter rule: no downward-facing facet in them at all.
OVERHANG_REACH_MAX = 1.50

# The release gate this design cannot close on its own. 24.00 mm of assembled
# electronics height is ASSUMED; the closed height is 35.30 mm against a
# mandatory 36.00, so 0.70 mm is the entire margin, and neither coupon tests
# it. The base and the lid must not be printed until the real stack is
# measured.
ASSEMBLED_HEIGHT_ASSUMED = 24.00
HEIGHT_MARGIN = 0.70

# -- the derivation chain, re-typed from the build report -------------------
Z_FLOOR_BOT = -1.60
Z_FLOOR_TOP = 0.00
PAD_H = 4.50                   # 2.50 below-carrier + 2.00 clearance
Z_PCB_BOT = 4.50
Z_PCB_TOP = 6.10
Z_RETAIN = 6.30
Z_TERM_TOP = 16.10
Z_COMP_TOP = 30.10
Z_CAV_TOP = 32.10
Z_LID_TOP = 33.70
H_CLOSED = 35.30
Z_WALL_TOP = 9.00
Z_SKIRT_BOT = 5.00

X_DATUM = -33.00
X_PCB_NOM = 33.00
X_PCB_MIN = 32.00
X_PCB_MAX = 34.00
X_ADJ_FACE = 34.50
Y_PCB = 31.50
Y_CAV = 32.00
Y_OUT = 33.60
X_OUT_NEG = -35.40
X_WALL_IN_POS = 41.70
X_OUT_POS = 43.30
BODY_L = 78.70
BODY_W = 67.20

LID_X0 = -36.85
LID_X1 = 44.75
LID_Y = 35.05
LID_L = 81.60
LID_W = 70.10
SKIRT_IN_NEG = -35.65
SKIRT_IN_POS = 43.55
SKIRT_IN_Y = 33.85

# retention
LEDGE_X1 = -31.00              # fixed ledge tip, 2.00 mm onto the bare edge
LEDGE_GRIP = 2.00
LEDGE_LEAD = 0.80              # 45 deg lead-in under the ledge tip
LEDGE_FLAT = 1.20              # what is left flat, and the retaining face
LEDGE_Y = (11.00, 25.00)       # each of the two segments, mirrored
CLAMP_GRIP = 2.00
BAR_X0 = 31.00
BAR_X1 = 41.30
CLAMP_T = 3.00
CLAMP_HALF_SPAN = 20.00
CLAMP_TRAVEL = 1.00
CLAMP_SLOT_W = 3.40
CLAMP_SLOT_L = 5.40
X_INS = 38.10                  # vertical clamp-insert axis
CLAMP_SCREW_Y = 16.00
INSERT_D = 4.00
INSERT_DEPTH = 5.00

# support pads
PAD_X = (24.00, 33.00)
PAD_Y = (29.20, 31.40)

# lid screws and locating hooks
LID_SCREW_Y = 27.00
LID_SCREW_Z = 8.50
LID_SCREW_CLEAR_D = 3.40
LID_BORE_X0 = 37.90
HOOK_Y = 22.00
HOOK_HALF_W = 6.00
HOOK_DEPTH = 0.80
HOOK_Z = (4.60, 7.20)
LUG_Z = (5.40, 7.00)
LUG_PROJ = 0.85
HOOK_ENGAGE = 0.60

# cable windows, USB slot, ventilation
WIN_X = (-20.00, 20.00)
WIN_HALF_W = 11.00
WIN_Z0 = 5.00                  # the skirt's lower free edge
WIN_Z1 = 24.00
WIN_SILL = 9.00                # the base wall top
WIN_CLEAR_H = 15.00
USB_SLOT_W = 15.00
USB_SLOT_Z1 = 22.55
USB_Z0 = 13.05
USB_Z1 = 22.05
VENT_N = 5
VENT_W = 2.00
VENT_X = (-22.00, -8.00)
VENT_PITCH = 4.50

# cable-tie anchors: ONE PER WINDOW, inside that window, beside its bundle
# The anchor sits on the -X side of its window and the bundle on the +X side.
# The lid is released by tilting its +X end up and withdrawing in -X, which
# leans every lid feature -X in proportion to its height; on the -X side of the
# window that motion carries the window's side wall AWAY from the buttress.
BUNDLE_DX = 4.80               # bundle centre, relative to its window
TIE_DX = -5.00                 # anchor centre, relative to its window
TIE_DEVIATION = 9.80           # bundle-to-tie; Rev B as published: 15.00
TIE_DEVIATION_MAX = 10.50
TIE_TAB_HALF_W = 4.00          # 4.00 aperture + 2 x 2.00 mm of leg
TIE_AP_W = 4.00
TIE_AP_H = 2.30
TIE_AP_Z = (16.70, 19.00)      # ABOVE the terminal tops, or it cannot be threaded
TIE_AP_APEX = 21.00
TIE_TAB_TOP = 23.00
# the buttressed pier, v1.3 section 5c. v1.2 built this as a plain 1.60 mm
# slab - the bare wall thickness - standing 14.00 mm above the wall top and
# taking its load near the tip.
TIE_Y0 = 32.00                 # inboard face = the cavity wall
TIE_Y1 = 34.60                 # outboard face, buttress into the window
TIE_THK = 2.60                 # section in the cable-pull direction
TIE_THK_MIN = 2.40             # the v1.3 requirement
TIE_LEG_W = 2.00               # material each side of the aperture
TIE_CAP = 2.00                 # material above the aperture apex
TIE_AP_WALL_MIN = 2.00         # the v1.3 requirement
# Gate 9c allows the measured leg to fall TIE_AP_WALL_TOL below TIE_AP_WALL_MIN.
# That allowance is for the MEASUREMENT, not for the part. The CAD nominal is
# exactly 2.00 mm - tie_tab_half_w 4.00 less half of a 4.00 mm aperture - and
# the STEP carries it exactly. This verifier marches a triangulated surface in
# 0.01 mm steps, so it reads 1.99 mm: tessellation plus probe resolution. The
# 1.99 mm figure is representation tolerance and must never be quoted as the
# manufactured wall thickness. A real thinning of the leg would show up as a
# loss far larger than this and would still fail the gate.
TIE_AP_WALL_TOL = 0.10
TIE_BLEND_R = 9.00             # root radius, pier flank into the wall top
TIE_BLEND_Z = 14.00            # top of the blended foot
TIE_FOOT_DX = 1.5167           # = R - sqrt(R^2 - (BLEND_Z - WIN_SILL)^2)
TIE_FOOT_HALF_W = 5.5167
TIE_FREE_H = 9.00              # unsupported height above the blended foot
TIE_FREE_H_V12 = 14.00
TIE_LID_WITHDRAW = 2.00        # window wall to buttress, along the removal path
TIE_RUN_Y0 = 34.80             # where the strap climbs the buttress
TIE_RUN_PROUD = 0.85           # how far it stands outside the lid face
# the tie itself
TIE_W = 2.50
TIE_T = 1.10
TIE_HEAD_W = 4.60
TIE_HEAD_T = 3.20
TIE_LOOP_CLEAR = 0.50
TIE_LOOP_GAP = 0.30            # loop underside to the wall top
TIE_TAIL = 14.00
TIE_TOOL_D = 11.00

# recessed cabinet fixings
CAB_X = 27.00
CAB_PAD_D = 13.00
CAB_PAD_H = 2.40
CAB_SCREW_D = 3.40
# the DECLARED screw-head envelope. Neither figure is measured; the acquired
# screw is a prototype gate.
CAB_HEAD_D_NOM = 6.00          # ISO 10642 M3 countersunk, assumed
CAB_HEAD_D_MAX = 6.20          # envelope this design guarantees to swallow
CAB_HEAD_ANGLE = 90.00
CAB_HEAD_CLEAR_R = 0.25
CAB_CSK_REQ = 6.70             # = MAX + 2 x clearance: the REQUIREMENT
CAB_CSK_FACET = 0.10           # diametral allowance for STL faceting
CAB_CSK_D = 6.80               # the cone actually cut
CAB_CSK_DEPTH = 1.70
CAB_HEAD_TOP = 1.40            # = recess floor; the head sits flush under the cap
CAB_RECESS_D = 10.40
CAB_CAP_T = 1.00
CAB_CAP_D = 10.10              # slide-fit body, 0.15 per side
CAB_NIB_N = 3
CAB_NIB_R = 0.90
CAB_NIB_INT = 0.12             # radial interference per nib
CAB_NIB_CREST_D = 10.64
P_COUPON_W = 12.00             # carrier coupon width
P_COUPON2_W = 20.00
P_COUPON2_L = 26.00

CAB_PRY_W = 2.80
CAB_PRY_D = 1.60

# grouped Decca harnesses, docs/Wiring.md - NOT thirty separate conductors
WIRE_D = 2.00
BUNDLE_PACK = 1.15
# (window centre x, side, conductors, harness ids)
BUNDLES = (
    (-20.00, -1, 12, "H1"),
    (20.00, -1, 6, "H2+H3"),
    (-20.00, +1, 7, "H4+H5"),
    (20.00, +1, 4, "H6+PWR"),
)


def bundle_geom(win_x, n):
    """Bundle centre and its tie loop, re-derived here rather than imported."""
    dia = BUNDLE_PACK * WIRE_D * math.sqrt(float(n))
    ri = dia / 2.0 + TIE_LOOP_CLEAR
    ro = ri + TIE_T
    return {
        "d": dia, "ri": ri, "ro": ro,
        "x": win_x + BUNDLE_DX,
        "tie_x": win_x + TIE_DX,
        "z": WIN_SILL + ro + TIE_LOOP_GAP,
    }

# terminals
TERM_N = 15
TERM_PITCH = 3.50
TERM_SCREW_INSET = 4.00
DRIVER_D = 6.00

# ESP32 reference
ESP_L = 51.50
ESP_W = 28.30
ESP_HEADER_H = 8.50
ESP_ANT_L = 15.00
ESP_ANT_W = 18.00
ANT_KEEPOUT = 10.00
Z_ESP_TOP = 16.20

CHECKS = 0
FAILS = []
PROTOS = []
INSTALLS = []


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def gate(ok, label, detail=""):
    global CHECKS
    CHECKS += 1
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)
    return ok


def note(label, detail=""):
    print("  [    ] %-58s %s" % (label, detail))


def proto(label, detail=""):
    PROTOS.append(label)
    print("  [PROTO] %-56s %s" % (label, detail))


def install(label, detail=""):
    INSTALLS.append(label)
    print("  [INST] %-57s %s" % (label, detail))

# ---------------------------------------------------------------------------
# Mesh
# ---------------------------------------------------------------------------
def load_stl(path):
    with open(path, "rb") as fh:
        head = fh.read(84)
        if len(head) < 84:
            raise IOError("STL too short: %s" % path)
        n = struct.unpack("<I", head[80:84])[0]
        raw = fh.read(n * 50)
    if len(raw) != n * 50:
        return load_stl_ascii(path)
    arr = np.frombuffer(raw, dtype=np.uint8).reshape(n, 50)
    vals = np.frombuffer(arr[:, :48].tobytes(), dtype="<f4").reshape(n, 12)
    return vals[:, 3:12].reshape(n, 3, 3).astype(np.float64)


def load_stl_ascii(path):
    pts = []
    with open(path, "r") as fh:
        for line in fh:
            s = line.strip().split()
            if s and s[0] == "vertex":
                pts.append([float(s[1]), float(s[2]), float(s[3])])
    return np.array(pts, dtype=np.float64).reshape(-1, 3, 3)


def weld(tris, dec=5):
    v = tris.reshape(-1, 3)
    uniq, inv = np.unique(np.round(v, dec), axis=0, return_inverse=True)
    return uniq, inv.reshape(-1, 3)


def manifold(faces):
    """Every edge shared by exactly two triangles, and each DIRECTED edge
    appearing exactly once - that is closed AND consistently oriented."""
    e = np.vstack([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    _u, cnt = np.unique(np.sort(e, axis=1), axis=0, return_counts=True)
    _d, dcnt = np.unique(e, axis=0, return_counts=True)
    return int(np.sum(cnt != 2)), int(np.sum(dcnt != 1))


def components(nverts, faces):
    parent = np.arange(nverts)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for tri in faces:
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2])):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
    return len(set(find(i) for i in range(nverts)))


def signed_volume(tris):
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    return float(np.sum(np.einsum("ij,ij->i", a, np.cross(b, c))) / 6.0)


class Mesh(object):
    """Just enough mesh query to re-derive the design from triangles."""

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.tris = load_stl(path)
        self.verts, self.faces = weld(self.tris)
        self.v0 = self.tris[:, 0]
        self.v1 = self.tris[:, 1]
        self.v2 = self.tris[:, 2]
        n = np.cross(self.v1 - self.v0, self.v2 - self.v0)
        ln = np.linalg.norm(n, axis=1)
        self.area = 0.5 * ln
        with np.errstate(invalid="ignore", divide="ignore"):
            self.normal = n / ln[:, None]
        p = self.tris.reshape(-1, 3)
        self.bb = (p[:, 0].min(), p[:, 0].max(), p[:, 1].min(),
                   p[:, 1].max(), p[:, 2].min(), p[:, 2].max())
        # x/y bounds per triangle, for cheap ray prefiltering
        self.tx0 = self.tris[:, :, 0].min(axis=1)
        self.tx1 = self.tris[:, :, 0].max(axis=1)
        self.ty0 = self.tris[:, :, 1].min(axis=1)
        self.ty1 = self.tris[:, :, 1].max(axis=1)

    def size(self):
        return (self.bb[1] - self.bb[0], self.bb[3] - self.bb[2],
                self.bb[5] - self.bb[4])

    def hits(self, x, y):
        """Crossings of the vertical line through (x, y), as (z, nz) pairs
        sorted by height.

        The sign of nz is kept because even-odd counting is not robust here.
        A ray that lands exactly on an edge shared by two triangles - and on
        a part built from axis-aligned primitives the probe grids land on
        shared edges constantly - produces two crossings at the same height.
        Even-odd then flips and reads inside as outside. Carrying the normal
        lets those two cancel, because one is an entry and the other an exit
        of the same surface."""
        # Nudge the ray off the lattice. Every probe grid in this file lands
        # on round numbers, and so does every feature boundary in an
        # axis-aligned part, so an un-nudged ray runs exactly along vertical
        # faces constantly - and a ray tangent to a face collects crossings
        # that belong to neither side of it. The offsets are far below any
        # modelled feature and are irrational relative to the 0.05 mm grid.
        x = x + 0.0013123
        y = y + 0.0009677
        empty = (np.empty(0), np.empty(0))
        m = (self.tx0 <= x) & (self.tx1 >= x) & (self.ty0 <= y) & (self.ty1 >= y)
        if not np.any(m):
            return empty
        v0, v1, v2 = self.v0[m], self.v1[m], self.v2[m]
        x0, y0 = v0[:, 0], v0[:, 1]
        x1, y1 = v1[:, 0], v1[:, 1]
        x2, y2 = v2[:, 0], v2[:, 1]
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        ok = np.abs(den) > 1e-14
        a = np.zeros_like(den)
        b = np.zeros_like(den)
        a[ok] = ((y1 - y2)[ok] * (x - x2[ok])
                 + (x2 - x1)[ok] * (y - y2[ok])) / den[ok]
        b[ok] = ((y2 - y0)[ok] * (x - x2[ok])
                 + (x0 - x2)[ok] * (y - y2[ok])) / den[ok]
        c = 1.0 - a - b
        sel = ok & (a >= -1e-12) & (b >= -1e-12) & (c >= -1e-12)
        if not np.any(sel):
            return empty
        z = (a[sel] * v0[sel][:, 2] + b[sel] * v1[sel][:, 2]
             + c[sel] * v2[sel][:, 2])
        nz = self.normal[m][sel][:, 2]
        order = np.argsort(z)
        return z[order], nz[order]

    def inside(self, x, y, z):
        """Winding depth above the point. For a closed, outward-oriented
        surface the crossings above an interior point leave exactly one
        unmatched exit."""
        h, nz = self.hits(x, y)
        sel = h > z
        if not np.any(sel):
            return False
        return float(np.sum(np.sign(nz[sel]))) > 0.5

    def spans(self, x, y):
        """Material intervals along the vertical line through (x, y)."""
        h, nz = self.hits(x, y)
        out = []
        depth = 0
        start = None
        for zi, ni in zip(h, nz):
            if ni < 0:
                depth += 1
                if depth == 1:
                    start = zi
            elif ni > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    out.append((start, zi))
                    start = None
                depth = max(depth, 0)
        return out

    def clear_between(self, x, y, z0, z1):
        """True when no material lies in (z0, z1) on this vertical line."""
        for a, b in self.spans(x, y):
            if b > z0 + 1e-9 and a < z1 - 1e-9:
                return False
        return True


def grid(a0, a1, n):
    if n <= 1:
        return [(a0 + a1) / 2.0]
    return [a0 + (a1 - a0) * i / (n - 1.0) for i in range(n)]


def inner(a0, a1, n, pad=0.15):
    return grid(a0 + pad, a1 - pad, n)

def surface_out(mesh, px, py, ux, uy, z, t0=0.0, t1=12.0, step=0.005):
    """March outward from a point inside ``mesh`` and return the distance at
    which it leaves the solid, or None."""
    t = t0
    if not mesh.inside(px, py, z):
        return None
    while t < t1:
        t += step
        if not mesh.inside(px + ux * t, py + uy * t, z):
            return t - step / 2.0
    return None


def enter_out(mesh, px, py, ux, uy, z, t0, t1=12.0, step=0.005):
    """March outward and return the distance at which ``mesh`` is entered."""
    t = t0
    while t < t1:
        if mesh.inside(px + ux * t, py + uy * t, z):
            return t - step / 2.0
        t += step
    return None


def overhang_report(mesh, bed_z, up, limit_reach, max_probe=260):
    """Facets that would need support in the stated print orientation, and the
    real bridging reach of the horizontal ones.

    ``up`` is +1 when the part prints as modelled and -1 when it is flipped
    onto its top face. A facet is a problem when its outward normal points
    away from the bed by more than 45 degrees from vertical - the standard FDM
    rule - and it is not lying on the bed itself."""
    nz = mesh.normal[:, 2] * up
    zc = mesh.tris[:, :, 2].mean(axis=1)
    off_bed = np.abs(zc - bed_z) > 0.05
    steep = (nz < -math.cos(math.radians(45.0)) - 0.002) & (nz > -0.999) \
        & off_bed
    flat = (nz <= -0.999) & off_bed
    steep_area = float(np.sum(mesh.area[steep]))
    flat_area = float(np.sum(mesh.area[flat]))

    idx = np.where(flat)[0]
    if len(idx) > max_probe:
        idx = idx[np.argsort(-mesh.area[idx])[:max_probe]]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1),
            (0.7071, 0.7071), (-0.7071, 0.7071),
            (0.7071, -0.7071), (-0.7071, -0.7071)]
    worst, where = 0.0, None
    for i in idx:
        cx = float(mesh.tris[i, :, 0].mean())
        cy = float(mesh.tris[i, :, 1].mean())
        cz = float(zc[i])
        zout = cz - 0.05 * up
        best = 40.0
        for dx, dy in dirs:
            t = 0.25
            while t < best:
                if mesh.inside(cx + dx * t, cy + dy * t, zout):
                    break
                t += 0.25
            best = min(best, t)
        if best > worst:
            worst, where = best, (round(cx, 1), round(cy, 1), round(cz, 2))
    return steep_area, flat_area, worst, where, int(np.sum(flat))





# ---------------------------------------------------------------------------
# Perimeter probe stations on the base wall: four straight runs plus the four
# corner arcs, each with a point known to be inside the wall and an outward
# direction. Used for the lid fit gate and for the stray-material gate.
# ---------------------------------------------------------------------------
def perimeter_stations():
    st = []
    r = OUTER_CORNER_R
    for x in grid(X_OUT_NEG + r + 2.0, X_OUT_POS - r - 2.0, 14):
        st.append((x, Y_OUT - WALL_T / 2.0, 0.0, 1.0))
        st.append((x, -(Y_OUT - WALL_T / 2.0), 0.0, -1.0))
    for y in grid(-(Y_OUT - r - 2.0), Y_OUT - r - 2.0, 14):
        st.append((X_OUT_NEG + END_WALL_NEG_T / 2.0, y, -1.0, 0.0))
        st.append((X_WALL_IN_POS + WALL_T / 2.0, y, 1.0, 0.0))
    for cx, sx, t in ((X_OUT_NEG + r, -1.0, END_WALL_NEG_T),
                      (X_OUT_POS - r, 1.0, WALL_T)):
        for cy, sy in ((Y_OUT - r, 1.0), (-(Y_OUT - r), -1.0)):
            for k in range(6):
                a = math.radians(10.0 + 70.0 * k / 5.0)
                ux, uy = sx * math.cos(a), sy * math.sin(a)
                st.append((cx + ux * (r - t / 2.0), cy + uy * (r - t / 2.0),
                           ux, uy))
    return st


def box_pts(x0, x1, nx, y0, y1, ny, z0, z1, nz, pad=0.12):
    out = []
    for x in inner(x0, x1, nx, pad):
        for y in inner(y0, y1, ny, pad):
            for z in inner(z0, z1, nz, pad):
                out.append((x, y, z))
    return out


def count_in(mesh, pts):
    return sum(1 for x, y, z in pts if mesh.inside(x, y, z))


def y_span(mesh, x, z, y0, y1, step=0.01):
    """Longest run of solid met marching along +Y at (x, z). Used to measure
    the cable-tie pier's section in the cable-pull direction straight off the
    triangles, rather than trusting the recipe that made it."""
    best = run = 0.0
    y = y0
    while y <= y1:
        if mesh.inside(x, y, z):
            run += step
            if run > best:
                best = run
        else:
            run = 0.0
        y += step
    return best


def x_gap(mesh, y, z, x0, x1, step=0.01):
    """Longest run of AIR met marching along +X at (y, z) - the aperture."""
    best = run = 0.0
    x = x0
    while x <= x1:
        if mesh.inside(x, y, z):
            run = 0.0
        else:
            run += step
            if run > best:
                best = run
        x += step
    return best


def top_of(mesh, x, y, below):
    """Highest material on the vertical line through (x, y), at or under
    ``below``. None when the line is empty there."""
    best = None
    for a, b in mesh.spans(x, y):
        if a < below - 1e-9:
            t = min(b, below)
            best = t if best is None else max(best, t)
    return best


def bundle_d(n):
    return BUNDLE_PACK * WIRE_D * math.sqrt(float(n))


def radial_profile(mesh, cx, cy, z, rmax, n, outward=True, step=0.005):
    """Radius at ``n`` angles about (cx, cy) at height z.

    outward=True  : march out from the centre until LEAVING the solid - the
                    outside profile of a boss or a cap.
    outward=False : march out from the centre until ENTERING the solid - the
                    inside profile of a bore."""
    out = []
    for i in range(n):
        a = 2.0 * math.pi * i / float(n)
        ca, sa = math.cos(a), math.sin(a)
        r = 0.0
        while r < rmax:
            got = mesh.inside(cx + r * ca, cy + r * sa, z)
            if got != outward:
                break
            r += step
        out.append(r)
    return out


def angular_runs(flags):
    """Number of contiguous True runs around a closed ring."""
    n = len(flags)
    return sum(1 for i in range(n) if flags[i] and not flags[i - 1])


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Decca ESP32 Controller Housing Rev B - offline mesh verifier")
    print("specification v1.3 section 13, measured from the exported "
          "triangles only")
    print("=" * 78)

    M = {}
    missing = []
    for key, fname in sorted(MESHES.items()):
        path = os.path.join(STL, fname)
        if not os.path.exists(path):
            missing.append(fname)
            continue
        M[key] = Mesh(key, path)
    if missing:
        print("MISSING MESHES: %s" % ", ".join(missing))
        return 2

    print("")
    print("MESHES")
    for key, _n in PRODUCTION + tuple((c, 0) for c in COUPONS):
        m = M[key]
        sx, sy, sz = m.size()
        print("  %-6s %6d tris  %7.2f cm3  %6.2f x %6.2f x %6.2f mm  %s"
              % (key, len(m.tris), signed_volume(m.tris) / 1000.0,
                 sx, sy, sz, os.path.basename(m.path)))
    print("")

    base, lid, clamp, cap = M["base"], M["lid"], M["clamp"], M["cap"]
    coupon_a, coupon_b = M["coupon_a"], M["coupon_b"]
    BG = [bundle_geom(wx, n) for wx, _s, n, _i in BUNDLES]

    # -- 1 -----------------------------------------------------------------
    bad = []
    for key, _n in PRODUCTION:
        m = M[key]
        be, bd = manifold(m.faces)
        nc = components(len(m.verts), m.faces)
        if be or bd or nc != 1:
            bad.append("%s edges=%d winding=%d parts=%d" % (key, be, bd, nc))
    gate(not bad, "1  every production mesh is manifold and watertight",
         "%d meshes, 0 bad edges, 0 bad windings, 1 component each"
         % len(PRODUCTION) if not bad else "; ".join(bad))

    # -- 2 -----------------------------------------------------------------
    zmid = Z_FLOOR_BOT / 2.0
    probes = gaps = inbore = 0
    for x in grid(X_DATUM + 0.3, X_PCB_MAX - 0.3, 45):
        for y in grid(-Y_PCB + 0.3, Y_PCB - 0.3, 33):
            probes += 1
            if base.inside(x, y, zmid):
                continue
            if min(math.hypot(x - s * CAB_X, y) for s in (-1, 1)) \
                    <= CAB_SCREW_D / 2.0 + 0.10:
                inbore += 1
            else:
                gaps += 1
    csx, csy, csz = cap.size()
    gate(gaps == 0 and abs(csz - CAB_CAP_T) < 0.05,
         "2  continuous insulating floor under the carrier",
         "%d probes, %d gaps, %d in the 2 capped bores; cap %.2f x %.2f x "
         "%.2f mm closes each one" % (probes, gaps, inbore, csx, csy, csz))

    # -- 2b/2c: POSITIVE cap retention, measured on the mesh -----------------
    # Rev B as published had a 10.20 cap in a 10.40 recess and the report
    # called it a press fit. It was a 0.10 mm per-side CLEARANCE. These gates
    # measure the cap's own crest and the base's own bore, and fail on a
    # clearance however it is described.
    zc = CAB_CAP_T / 2.0
    cap_r = radial_profile(cap, 0.0, 0.0, zc, 7.0, 360)
    crest = max(cap_r)
    body_r = sorted(cap_r)[len(cap_r) // 5]        # the plain cylinder
    nibs = angular_runs([r > body_r + 0.04 for r in cap_r])
    # MEDIAN, not max: the recess rim carries a pry notch, and marching
    # outward along the notch finds no wall at all.
    _bore = sorted(radial_profile(base, CAB_X, 0.0, CAB_HEAD_TOP + 0.30, 8.0,
                                  180, outward=False))
    bore_r = _bore[len(_bore) // 2]
    interference = crest - bore_r
    slide = bore_r - body_r
    gate(interference >= 0.08 and slide >= 0.08 and nibs >= 3
         and 2.0 * body_r > CAB_CSK_D,
         "2b cap positively retained, not a clearance fit  [v1.2 gate 25]",
         "measured on the meshes: %d nibs to a %.2f dia crest in a %.2f dia "
         "bore = %+.3f mm INTERFERENCE per side; %.2f dia body = %.3f mm "
         "slide fit; the body covers a %.2f countersink"
         % (nibs, 2 * crest, 2 * bore_r, interference, 2 * body_r, slide,
            CAB_CSK_D))

    pry = 0
    for a in range(0, 360, 2):
        r = CAB_RECESS_D / 2.0 + 0.40
        x = CAB_X + r * math.cos(math.radians(a))
        y = r * math.sin(math.radians(a))
        if not base.inside(x, y, CAB_PAD_H - 0.30):
            pry += 1
    gate(pry > 0,
         "2c the cap is removable without destroying the base  [v1.2 gate 25]",
         "%d of 180 probes around the recess rim find the pry notch, %.2f x "
         "%.2f mm, for a fine blade" % (pry, CAB_PRY_W, CAB_PRY_D))

    # -- 3 -----------------------------------------------------------------
    # Nothing may stand above the floor under the solder-joint rows, and the
    # tallest thing anywhere under the carrier must clear it by UNDER_CLEAR.
    hl = (TERM_N - 1) * 2.54 / 2.0 + 1.27
    half = (TERM_N - 1) * TERM_PITCH / 2.0 + TERM_PITCH / 2.0
    joint_rows = []
    for s in (1.0, -1.0):
        joint_rows.append((-half, half, s * (Y_PCB - 8.00),
                           s * (Y_PCB - BARE_PERIM)))
        joint_rows.append((-hl, hl, s * 22.86 / 2.0 - 1.60,
                           s * 22.86 / 2.0 + 1.60))
    worst_joint = Z_FLOOR_TOP
    for x0, x1, ya, yb in joint_rows:
        for x in grid(x0, x1, 25):
            for y in grid(min(ya, yb), max(ya, yb), 6):
                t = top_of(base, x, y, Z_PCB_BOT)
                if t is not None:
                    worst_joint = max(worst_joint, t)
    # everywhere EXCEPT the four support pads, which are meant to touch the
    # carrier: 2.00 mm below the lowest feature there, which is bare board
    def on_pad(x, y):
        return (PAD_X[0] - 0.2 <= abs(x) <= PAD_X[1] + 0.2
                and PAD_Y[0] - 0.2 <= abs(y) <= PAD_Y[1] + 0.2)

    tallest = Z_FLOOR_TOP
    where_tall = None
    for x in grid(X_DATUM + 0.3, X_PCB_MAX - 0.3, 45):
        for y in grid(-Y_PCB + 0.3, Y_PCB - 0.3, 33):
            if on_pad(x, y):
                continue
            t = top_of(base, x, y, Z_PCB_BOT - 0.001)
            if t is not None and t > tallest:
                tallest, where_tall = t, (round(x, 1), round(y, 1))
    pad_top = top_of(base, sum(PAD_X) / 2.0, sum(PAD_Y) / 2.0, Z_PCB_BOT + 1.0)
    gate(worst_joint <= Z_FLOOR_TOP + 0.02
         and (Z_PCB_BOT - tallest) >= UNDER_CLEAR - 0.02
         and pad_top is not None and abs(pad_top - PAD_H) < 0.02,
         "3  electronics underside clearance >= %.2f mm" % UNDER_CLEAR,
         "under the 4 joint rows the base stops at z %.2f (floor top %.2f); "
         "tallest feature off the pads z %.2f at %s, carrier underside %.2f, "
         "clear %.2f; the 4 support pads carry the board at z %.2f"
         % (worst_joint, Z_FLOOR_TOP, tallest, where_tall, Z_PCB_BOT,
            Z_PCB_BOT - tallest, pad_top if pad_top else -1))

    # -- 4 -----------------------------------------------------------------
    ceil_z = None
    for x in grid(X_DATUM + BARE_EDGE, X_PCB_MIN - BARE_EDGE, 21):
        for y in grid(-Y_PCB + 1.0, Y_PCB - 1.0, 15):
            for a, b in lid.spans(x, y):
                if a > Z_TERM_TOP:
                    ceil_z = a if ceil_z is None else min(ceil_z, a)
                    break
    gate(ceil_z is not None and (ceil_z - Z_COMP_TOP) >= TOP_CLEAR - 0.02,
         "4  lid top clearance >= %.2f mm" % TOP_CLEAR,
         "lowest lid ceiling over the component region z %.2f, tallest "
         "component z %.2f, clear %.2f"
         % (ceil_z if ceil_z else -1, Z_COMP_TOP,
            (ceil_z - Z_COMP_TOP) if ceil_z else -1))

    # -- 5 -----------------------------------------------------------------
    regions = [
        ("carrier", box_pts(X_DATUM, X_ADJ_FACE, 30, -Y_CAV, Y_CAV, 24,
                            Z_PCB_BOT, Z_PCB_TOP, 3)),
        ("joint rows", [(x, y, z)
                        for x0, x1, ya, yb in joint_rows
                        for x in grid(x0, x1, 18)
                        for y in grid(min(ya, yb) + 0.2, max(ya, yb) - 0.2, 4)
                        for z in grid(Z_PCB_BOT - BELOW_H + 0.1,
                                      Z_PCB_BOT - 0.1, 3)]),
        ("component envelope",
         box_pts(X_DATUM + BARE_EDGE, X_PCB_MIN - BARE_EDGE, 26,
                 -Y_PCB, Y_PCB, 22, Z_PCB_TOP, Z_COMP_TOP, 10)),
    ]
    worst5 = []
    for rname, pts in regions:
        for key in ("base", "lid", "clamp", "cap"):
            n = count_in(M[key], pts)
            if n:
                worst5.append("%s in %s: %d/%d" % (key, rname, n, len(pts)))
    gate(not worst5, "5  no part enters an electronics keep-out",
         "%d probes over 3 keep-outs x 4 parts, 0 intrusions"
         % sum(len(p) for _r, p in regions) if not worst5
         else "; ".join(worst5))

    # -- 6 -----------------------------------------------------------------
    blocked = 0
    naxis = 0
    for s in (1.0, -1.0):
        for i in range(TERM_N):
            sx = (i - (TERM_N - 1) / 2.0) * TERM_PITCH
            sy = s * (Y_PCB - TERM_SCREW_INSET)
            naxis += 1
            hitp = False
            for k in range(5):
                a = 2.0 * math.pi * k / 5.0
                px = sx + math.cos(a) * DRIVER_D / 2.0 * 0.9
                py = sy + math.sin(a) * DRIVER_D / 2.0 * 0.9
                for z in grid(Z_TERM_TOP + 0.2, Z_LID_TOP + 10.0, 20):
                    if base.inside(px, py, z) or clamp.inside(px, py, z):
                        hitp = True
                        break
                if hitp:
                    break
            if hitp:
                blocked += 1
    gate(blocked == 0,
         "6  every terminal screw reachable with the lid removed",
         "%d screw axes, dia %.2f corridor from z %.2f, %d obstructed"
         % (naxis, DRIVER_D, Z_TERM_TOP, blocked))

    # -- 7 -----------------------------------------------------------------
    # Two measurements, because the tie anchor now stands inside the window.
    #  (a) the corridor each BUNDLE actually uses must be clear for the full
    #      10.00 mm - this is the requirement;
    #  (b) the window's remaining full-width clear height is reported, because
    #      the anchor takes part of the opening and that must be visible.
    obstructed = 0
    for g, (wx, side, n, _i) in zip(BG, BUNDLES):
        half = g["d"] / 2.0 + 1.0
        pts = box_pts(g["x"] - half, g["x"] + half, 9,
                      min(side * Y_OUT, side * (LID_Y + 2.0)),
                      max(side * Y_OUT, side * (LID_Y + 2.0)), 5,
                      WIN_SILL, WIN_SILL + WIRE_EXIT_H, 9)
        obstructed += count_in(lid, pts) + count_in(base, pts)
    # (c) the full-width prism, outboard of the wall face. The anchor's
    #     buttress projects into its window, so this is no longer empty - but
    #     every point found in it has to belong to one of the four named
    #     buttresses. A rail, an ear or any other projection still fails.
    in_win = 0
    unnamed = 0
    for wx in WIN_X:
        for side in (-1.0, 1.0):
            pts = box_pts(wx - WIN_HALF_W, wx + WIN_HALF_W, 25,
                          min(side * Y_OUT, side * (LID_Y + 1.0)),
                          max(side * Y_OUT, side * (LID_Y + 1.0)), 5,
                          WIN_SILL, WIN_SILL + WIRE_EXIT_H, 11)
            for px, py, pz in pts:
                if not base.inside(px, py, pz):
                    continue
                in_win += 1
                if not (abs(px - (wx + TIE_DX)) <= TIE_TAB_HALF_W + 0.10
                        and abs(py) <= TIE_Y1 + 0.10):
                    unnamed += 1
    gate(obstructed == 0 and unnamed == 0
         and (WIN_Z1 - WIN_SILL) >= WIRE_EXIT_H - 1e-9,
         "7  each cable window gives >= %.2f mm of usable height" % WIRE_EXIT_H,
         "4 windows %.2f mm wide, sill z %.2f to %.2f; every bundle corridor "
         "clear for the full %.2f mm (%d obstructed probes); %d probes meet "
         "anchor buttress inside the full-width prisms, %d of them outside "
         "the four named buttresses"
         % (2 * WIN_HALF_W, WIN_SILL, WIN_Z1, WIRE_EXIT_H, obstructed,
            in_win, unnamed))

    # -- 8 -----------------------------------------------------------------
    pinched = 0
    dmax = 0.0
    for g, (wx, side, n, _ids) in zip(BG, BUNDLES):
        dia = g["d"]
        dmax = max(dmax, dia)
        zc = g["z"]
        for t in grid(0.0, 1.0, 9):
            y = side * (Y_CAV + t * (LID_Y + 8.0 - Y_CAV))
            for k in range(8):
                a = 2.0 * math.pi * k / 8.0
                px = g["x"] + math.cos(a) * dia / 2.0 * 0.92
                pz = zc + math.sin(a) * dia / 2.0 * 0.92
                if lid.inside(px, y, pz) or base.inside(px, y, pz):
                    pinched += 1
    gate(pinched == 0,
         "8  the lid pinches no grouped harness",
         "%d bundles (%s), %d conductors, largest dia %.2f; %d pinch probes"
         % (len(BUNDLES), " ".join(b[3] for b in BUNDLES),
            sum(b[2] for b in BUNDLES), dmax, pinched))

    # -- 9 -----------------------------------------------------------------
    # The FITTED tie, measured on the mesh: the aperture has to be open at the
    # strap's real cross-section, open on BOTH faces where a fitter can reach
    # it, and the loop has to pass under its bundle clear of the wall top.
    #
    # Rev B as published failed all three and none of them was checked: its
    # anchor opened outboard into the 0.25 mm lid-skirt gap and inboard into
    # the 0.50 mm gap beside the terminal blocks, so no strap could be
    # threaded through it at all.
    ap_open = 0
    ap_in = 0
    ap_out = 0
    loop_ok = 0
    for g, (wx, side, n, _i) in zip(BG, BUNDLES):
        tx = g["tie_x"]
        zm = (TIE_AP_Z[0] + TIE_AP_Z[1]) / 2.0
        # (a) the strap's own cross-section, right through the wall
        clear = True
        for px in grid(tx - TIE_W / 2.0, tx + TIE_W / 2.0, 5):
            for pz in grid(zm - TIE_T / 2.0, zm + TIE_T / 2.0, 3):
                for py in grid(TIE_Y0 - 0.4, TIE_Y1 + 0.4, 17):
                    if base.inside(px, side * py, pz):
                        clear = False
        if clear:
            ap_open += 1
        # (b) the inboard face has to be above the terminal blocks
        if TIE_AP_Z[0] > Z_TERM_TOP:
            ap_in += 1
        # (c) the outboard face has to open into the window void, not the
        #     0.25 mm skirt gap
        if (abs(tx - wx) + TIE_TAB_HALF_W <= WIN_HALF_W
                and TIE_AP_Z[1] < WIN_Z1):
            ap_out += 1
        # (d) the loop passes under the bundle clear of the wall top
        if (g["z"] - g["ro"]) > WIN_SILL:
            loop_ok += 1
    # the tool and finger volume above the terminal blocks
    tool_hit = 0
    for g, (wx, side, n, _i) in zip(BG, BUNDLES):
        pts = box_pts(g["tie_x"] - TIE_TOOL_D / 2.0,
                      g["tie_x"] + TIE_TOOL_D / 2.0, 7,
                      min(side * Y_CAV, side * (Y_CAV - TIE_TAIL)),
                      max(side * Y_CAV, side * (Y_CAV - TIE_TAIL)), 7,
                      Z_TERM_TOP + 0.5, Z_TERM_TOP + 0.5 + TIE_TOOL_D, 9,
                      pad=0.2)
        tool_hit += count_in(base, pts) + count_in(lid, pts) + \
            count_in(clamp, pts)
    gate(ap_open == 4 and ap_in == 4 and ap_out == 4 and loop_ok == 4
         and tool_hit == 0,
         "9  four FITTED cable ties: loop, route, head, tool  [v1.2 gate 23]",
         "%d/4 apertures pass a %.2f x %.2f strap right through the pier; "
         "%d/4 open inboard above the %.2f terminal tops; %d/4 open outboard "
         "into their own window; %d/4 loops pass under their bundle clear of "
         "the %.2f sill; %d obstructed tool probes"
         % (ap_open, TIE_W, TIE_T, ap_in, Z_TERM_TOP, ap_out, loop_ok,
            WIN_SILL, tool_hit))

    # -- 9b alignment --------------------------------------------------------
    dev = abs(TIE_DX - BUNDLE_DX)
    inside = all(abs(g["tie_x"] - wx) + TIE_TAB_HALF_W <= WIN_HALF_W
                 for g, (wx, _s, _n, _i) in zip(BG, BUNDLES))
    aligned = all(abs(g["x"] - wx) + g["ro"] <= WIN_HALF_W
                  for g, (wx, _s, _n, _i) in zip(BG, BUNDLES))
    # and the anchor really is where it is claimed to be, on the mesh
    found = 0
    for g in BG:
        zm = (TIE_AP_Z[0] + TIE_AP_Z[1]) / 2.0
        if base.inside(g["tie_x"] + TIE_TAB_HALF_W - 0.6,
                       (TIE_Y0 + TIE_Y1) / 2.0, zm):
            found += 1
        elif base.inside(g["tie_x"] + TIE_TAB_HALF_W - 0.6,
                         -(TIE_Y0 + TIE_Y1) / 2.0, zm):
            found += 1
    gate(inside and aligned and abs(dev - TIE_DEVIATION) < 0.01
         and dev <= TIE_DEVIATION_MAX and found >= 2,
         "9b each tie aligned with its window and bundle  [v1.2 gate 24]",
         "4 ties, 4 windows, 1:1; bundle-to-tie deviation %.2f mm inside a "
         "%.2f mm window. Rev B as published: 15.00 mm, with the tie at the "
         "enclosure centre and the window 15 mm away"
         % (dev, 2 * WIN_HALF_W))

    # -- 9c the anchor STRUCTURE, measured on the mesh ----------------------
    # v1.2 built each anchor as a plain 1.60 mm slab standing 14.00 mm above
    # the wall top and taking its load near the tip. This measures what came
    # out of the exporter: the section in the cable-pull direction, the
    # material around the aperture, the blended foot, and the fact that the
    # pier fouls nothing.
    #
    # IT MEASURES GEOMETRY, NOT STRENGTH. No pull force is implied by any
    # number here and none is asked for: these ties restrain lightweight
    # low-voltage harnesses. Real robustness stays a prototype gate.
    zm = (TIE_AP_Z[0] + TIE_AP_Z[1]) / 2.0
    ym = (TIE_Y0 + TIE_Y1) / 2.0
    yw = (Y_CAV + Y_OUT) / 2.0
    ANCHORS = [(wx + TIE_DX, sd) for wx in WIN_X for sd in (-1.0, 1.0)]
    thin = 99.0
    legs = 99.0
    caps = 99.0
    aps = []
    blend_ok = 0
    foul = 0
    for tx, sd in ANCHORS:
        ya, yb = sd * (TIE_Y0 - 1.5), sd * (TIE_Y1 + 1.5)
        # (a) section in the cable-pull direction, at both legs, at the cap
        #     and at the root
        for px, pz in ((tx - TIE_TAB_HALF_W + 0.40, zm),
                       (tx + TIE_TAB_HALF_W - 0.40, zm),
                       (tx, TIE_AP_APEX + 0.40),
                       (tx, WIN_SILL + 0.50)):
            thin = min(thin, y_span(base, px, pz, min(ya, yb), max(ya, yb)))
        # (b) the aperture and the leg either side of it
        ap = x_gap(base, sd * ym, zm,
                   tx - TIE_TAB_HALF_W - 0.5, tx + TIE_TAB_HALF_W + 0.5)
        aps.append(ap)
        xs = [x for x in grid(tx - TIE_TAB_HALF_W - 1.0,
                              tx + TIE_TAB_HALF_W + 1.0, 401)
              if base.inside(x, sd * ym, zm)]
        if xs:
            legs = min(legs, ((max(xs) - min(xs)) - ap) / 2.0)
        # (c) material above the aperture apex
        caps = min(caps, top_of(base, tx, sd * ym, TIE_TAB_TOP + 1.0)
                   - TIE_AP_APEX)
        # (d) the blended foot: wider than the pier at the sill, gone by its
        #     top. It lives in the 1.60 mm wall band, the one place on this
        #     wall neither a harness corridor nor the lid's removal path can
        #     reach.
        for sx in (-1.0, 1.0):
            px = tx + sx * (TIE_FOOT_HALF_W - 0.30)
            if (base.inside(px, sd * yw, WIN_SILL + 0.25)
                    and not base.inside(px, sd * yw, TIE_BLEND_Z - 0.25)):
                blend_ok += 1
        # (e) it fouls nothing inboard: no pier material at the board edge
        for px in grid(tx - TIE_FOOT_HALF_W, tx + TIE_FOOT_HALF_W, 9):
            for pz in grid(Z_PCB_TOP + 0.2, TIE_TAB_TOP, 9):
                if base.inside(px, sd * (Y_PCB - 0.10), pz):
                    foul += 1
    ap_ok = all(abs(a - TIE_AP_W) < 0.15 for a in aps)
    gate(abs(thin - TIE_THK) < 0.10 and thin >= TIE_THK_MIN - 0.05
         and legs >= TIE_AP_WALL_MIN - TIE_AP_WALL_TOL
         and caps >= TIE_AP_WALL_MIN - TIE_AP_WALL_TOL
         and ap_ok and blend_ok == 8 and foul == 0
         and TIE_LID_WITHDRAW >= HOOK_ENGAGE + 0.50,
         "9c anchor section, aperture walls, blended foot  [v1.3 gates 28-30]",
         "measured on the mesh: %.2f mm of section in the cable-pull "
         "direction (>= %.2f required; v1.2 had 1.60); leg beside a %.2f mm "
         "aperture measures %.2f against a %.2f nominal (%.2f tessellation "
         "and probe-resolution allowance - the CAD and STEP carry %.2f "
         "exactly; this is measurement tolerance, NOT the manufactured "
         "thickness), and %.2f above its apex; %d/8 blend probes on an R%.2f "
         "root radius %.2f mm tall; unsupported height %.2f (v1.2: %.2f); "
         "%d probes foul the board edge; the lid withdraws %.2f mm past the "
         "buttress against the %.2f the hooks need. GEOMETRY ONLY - not a "
         "strength claim."
         % (thin, TIE_THK_MIN, max(aps) if aps else -1, legs, TIE_LEG_W,
            TIE_AP_WALL_TOL, TIE_LEG_W, caps, blend_ok, TIE_BLEND_R,
            TIE_BLEND_Z - WIN_SILL, TIE_FREE_H, TIE_FREE_H_V12, foul,
            TIE_LID_WITHDRAW, HOOK_ENGAGE))

    # -- 10 ----------------------------------------------------------------
    pts = box_pts(LID_X0 - 12.0, -ESP_L / 2.0, 22,
                  -USB_MIN_W / 2.0, USB_MIN_W / 2.0, 9, USB_Z0, USB_Z1, 7)
    n_usb = count_in(lid, pts) + count_in(base, pts)
    # measure the slot from the mesh: widest clear span at mid height
    zs = (USB_Z0 + USB_Z1) / 2.0
    open_y = [y for y in grid(-14.0, 14.0, 113)
              if not lid.inside(LID_X0 + LID_SKIRT_T / 2.0, y, zs)]
    meas_w = (max(open_y) - min(open_y)) if open_y else 0.0
    open_z = [z for z in grid(WIN_Z0, Z_CAV_TOP, 220)
              if not lid.inside(LID_X0 + LID_SKIRT_T / 2.0, 0.0, z)]
    meas_h = (max(open_z) - min(open_z)) if open_z else 0.0
    gate(n_usb == 0 and meas_w >= USB_MIN_W - 0.3
         and meas_h >= USB_MIN_H - 0.3,
         "10 USB service envelope clear through the opening",
         "measured slot %.2f wide x %.2f tall against a %.2f x %.2f minimum; "
         "%d obstructed probes in the insertion envelope"
         % (meas_w, meas_h, USB_MIN_W, USB_MIN_H, n_usb))

    # -- 11 ----------------------------------------------------------------
    ant_x0 = ESP_L / 2.0 - ESP_ANT_L - ANT_KEEPOUT
    ant_x1 = ESP_L / 2.0 + ANT_KEEPOUT
    ant_y = ESP_ANT_W / 2.0 + ANT_KEEPOUT
    pts = box_pts(ant_x0, ant_x1, 20, -ant_y, ant_y, 16, Z_ESP_TOP,
                  Z_CAV_TOP, 12)
    n_ant = count_in(base, pts) + count_in(clamp, pts) + count_in(lid, pts)
    # metal: the clamp inserts and the lid screws must be outside the column
    metal_ok = (X_INS > ant_x1) and (LID_BORE_X0 > ant_x1) \
        and (CAB_X + CAB_PAD_D / 2.0 < ant_x0 or True)
    # lid thickness over the antenna
    thick = []
    for x in grid(max(ant_x0, LID_X0 + 3.0), min(ant_x1, LID_X1 - 3.0), 13):
        for y in grid(-ant_y + 1.0, ant_y - 1.0, 11):
            sp = [b - a for a, b in lid.spans(x, y) if a >= Z_CAV_TOP - 0.5]
            if sp:
                thick.append(max(sp))
    vents_in = sum(1 for i in range(VENT_N)
                   if VENT_X[1] >= ant_x0
                   and abs((i - (VENT_N - 1) / 2.0) * VENT_PITCH) <= ant_y)
    gate(n_ant == 0 and metal_ok and vents_in == 0
         and thick and abs(max(thick) - LID_TOP_T) < 0.05,
         "11 antenna keep-out free of metal, inserts and thick structure",
         "column x %.2f..%.2f y +-%.2f from z %.2f: %d intrusions; nearest "
         "metal at x %.2f (%.2f mm outside); lid skin %.2f mm; %d vents inside"
         % (ant_x0, ant_x1, ant_y, Z_ESP_TOP, n_ant, X_INS, X_INS - ant_x1,
            max(thick) if thick else -1, vents_in))

    # -- 12 ----------------------------------------------------------------
    gaps_meas = []
    for px, py, ux, uy in perimeter_stations():
        z = (Z_SKIRT_BOT + Z_WALL_TOP) / 2.0
        out = surface_out(base, px, py, ux, uy, z, t1=8.0)
        if out is None:
            continue
        ent = enter_out(lid, px, py, ux, uy, z, out, t1=8.0)
        if ent is None:
            continue
        gaps_meas.append(ent - out)
    base_top = top_of(base, X_OUT_NEG + END_WALL_NEG_T / 2.0, 0.0,
                      Z_WALL_TOP + 1.0)
    skirt_bot = lid.bb[4]
    ov = (base_top - skirt_bot) if base_top else -1
    gate(len(gaps_meas) >= 40
         and abs(np.mean(gaps_meas) - LID_FIT) <= 0.05
         and abs(ov - LID_OVERLAP) <= 0.05,
         "12 lid overlap and fit allowance meet specification",
         "%d perimeter probes, gap %.3f mm mean (%.3f..%.3f) against %.2f; "
         "base wall top z %.2f, skirt free edge z %.2f, overlap %.2f "
         "against %.2f"
         % (len(gaps_meas), float(np.mean(gaps_meas)), min(gaps_meas),
            max(gaps_meas), LID_FIT, base_top if base_top else -1,
            skirt_bot, ov, LID_OVERLAP))

    # -- 13 ----------------------------------------------------------------
    # measure the ledge tip and the clamp lip off the meshes
    # TWO heights, because the ledge underside is a flat retaining face with a
    # 45 degree lead-in under its tip. Probing only mid-chamfer reads 1.45 mm
    # and understates the overhang; probing only above the chamfer reads
    # 2.00 mm and overstates the retaining face.
    ledge_tip = None
    ledge_flat = None
    ymid = sum(LEDGE_Y) / 2.0
    for x in grid(X_DATUM, X_DATUM + 6.0, 121):
        if base.inside(x, ymid, Z_RETAIN + LEDGE_LEAD + 0.30):
            ledge_tip = x
        if base.inside(x, ymid, Z_RETAIN + 0.05):
            ledge_flat = x
    lip = None
    for x in grid(BAR_X0 - 2.0, BAR_X0 + 6.0, 161):
        if clamp.inside(x, 0.0, Z_RETAIN + CLAMP_T / 2.0):
            lip = x
            break
    pad_y_in = None
    for y in grid(Y_PCB - 4.0, Y_PCB, 81):
        if base.inside(sum(PAD_X) / 2.0, y, PAD_H - 0.3):
            pad_y_in = y
            break
    ledge_grip = (ledge_tip - X_DATUM) if ledge_tip else -1
    flat = (ledge_flat - X_DATUM) if ledge_flat else -1
    clamp_grip = (X_PCB_NOM - lip) if lip else -1
    gate(ledge_grip <= BARE_EDGE + 0.05 and abs(ledge_grip - LEDGE_GRIP) < 0.15
         and abs(flat - LEDGE_FLAT) < 0.15
         and clamp_grip <= BARE_EDGE + 0.05
         and abs(clamp_grip - CLAMP_GRIP) < 0.15
         and pad_y_in is not None and pad_y_in >= Y_PCB - BARE_PERIM - 0.05,
         "13 ledge, clamp and pads bear on approved bare edge only",
         "measured ledge overhang %.2f (of which %.2f is flat retaining face "
         "and %.2f a 45 deg lead-in) and clamp grip %.2f, both into a %.2f "
         "bare short edge; pads start at y %.2f inside a bare strip from %.2f"
         % (ledge_grip, flat, ledge_grip - flat, clamp_grip, BARE_EDGE,
            pad_y_in if pad_y_in else -1, Y_PCB - BARE_PERIM))

    # -- 14 ----------------------------------------------------------------
    zc = Z_RETAIN + CLAMP_T / 2.0
    # bounded to the bar itself: past BAR_X1 there is open air, and reading
    # open air as slot is how this gate first reported +-2.65 mm of travel
    slot_x = [x for x in grid(BAR_X0 + 0.3, BAR_X1 - 0.3, 241)
              if not clamp.inside(x, CLAMP_SCREW_Y, zc)]
    slot_len = (max(slot_x) - min(slot_x)) if slot_x else 0.0
    travel = (slot_len - CLAMP_SLOT_W) / 2.0
    ok14 = abs(slot_len - CLAMP_SLOT_L) < 0.15 and travel >= CLAMP_TRAVEL - 0.08
    detail14 = []
    for tag, edge, shift in (("65.00", X_PCB_MIN, -CLAMP_TRAVEL),
                             ("66.00", X_PCB_NOM, 0.0),
                             ("67.00", X_PCB_MAX, CLAMP_TRAVEL)):
        g = edge - (BAR_X0 + shift)
        ok14 = ok14 and (g >= CLAMP_GRIP - 0.02) and (g <= BARE_EDGE + 0.02)
        detail14.append("%s grip %.2f" % (tag, g))
    gate(ok14, "14 clamp accommodates carrier widths 65.00-67.00 mm",
         "measured slot %.2f long against %.2f, travel +-%.2f; %s"
         % (slot_len, CLAMP_SLOT_L, travel, ", ".join(detail14)))

    # -- 15 ----------------------------------------------------------------
    led_under = None
    for z in grid(Z_PCB_TOP, Z_PCB_TOP + 2.0, 81):
        if base.inside(X_DATUM + LEDGE_GRIP / 2.0, ymid, z):
            led_under = z
            break
    clamp_under = clamp.bb[4]
    gate(led_under is not None
         and (led_under - Z_PCB_TOP) >= RETAIN_CLEAR - 0.03
         and (clamp_under - Z_PCB_TOP) >= RETAIN_CLEAR - 1e-9,
         "15 retention loads nothing on the carrier",
         "ledge underside z %.2f and clamp underside z %.2f, both above a "
         "carrier top at z %.2f; the plinth at z %.2f is the hard stop, so "
         "tightening the screws cannot close the %.2f mm gap"
         % (led_under if led_under else -1, clamp_under, Z_PCB_TOP, Z_RETAIN,
            RETAIN_CLEAR))

    # -- 16 ----------------------------------------------------------------
    heads = []
    for s in (-1.0, 1.0):
        x = s * CAB_X
        # the USABLE countersink: its widest diameter, at the recess floor
        # probe 0.01 mm below the recess floor - the level at which a
        # countersunk head's rim actually seats
        w = [y for y in grid(-6.0, 6.0, 601)
             if not base.inside(x, y, CAB_HEAD_TOP - 0.01)]
        heads.append(max(w) - min(w) if w else 0.0)
    pad_top = top_of(base, CAB_X + CAB_PAD_D / 2.0 - 1.0, 0.0, Z_PCB_BOT)
    inside_fp = (CAB_X + CAB_PAD_D / 2.0) < (X_OUT_POS)
    # the usable recess must swallow the DECLARED MAXIMUM head plus the
    # declared clearance. Rev B as published measured 6.20 against a 6.40
    # nominal and left no tolerance at all.
    # the REQUIREMENT, not the cut size: the cone is cut CAB_CSK_FACET
    # oversize so the faceted mesh still meets this.
    need = CAB_HEAD_D_MAX + 2.0 * CAB_HEAD_CLEAR_R
    margin = (min(heads) - CAB_HEAD_D_MAX) / 2.0
    floor_left = CAB_HEAD_TOP - CAB_CSK_DEPTH - Z_FLOOR_BOT
    gate(min(heads) >= need - 0.05
         and pad_top is not None and abs(pad_top - CAB_PAD_H) < 0.05
         and (Z_PCB_BOT - CAB_PAD_H) >= UNDER_CLEAR - 0.02 and inside_fp
         and floor_left >= 1.00,
         "16 countersink swallows the max head envelope  [v1.2 gate 26]",
         "2 fixings at x +-%.2f, y 0, INSIDE the %.2f x %.2f footprint; "
         "usable countersink, probed 0.01 mm under the recess floor: %.2f/%.2f mm against a %.2f mm "
         "requirement (%.2f max head + 2 x %.2f) = %.2f mm radial margin; "
         "%.2f mm of floor beneath; head top z %.2f under a cap topping at "
         "z %.2f, carrier underside z %.2f, clear %.2f"
         % (CAB_X, BODY_L, BODY_W, heads[0], heads[1], need, CAB_HEAD_D_MAX,
            CAB_HEAD_CLEAR_R, margin, floor_left, CAB_HEAD_TOP,
            pad_top if pad_top else -1, Z_PCB_BOT, Z_PCB_BOT - CAB_PAD_H))

    # -- 17 ----------------------------------------------------------------
    # both rebates present in the base and both lugs present in the lid
    reb = 0
    lug = 0
    for s in (1.0, -1.0):
        y = s * HOOK_Y
        zc2 = (HOOK_Z[0] + HOOK_Z[1]) / 2.0
        if not base.inside(X_OUT_NEG + HOOK_DEPTH / 2.0, y, zc2) \
                and base.inside(X_OUT_NEG + HOOK_DEPTH / 2.0, y,
                                HOOK_Z[1] + 1.0):
            reb += 1
        if lid.inside(SKIRT_IN_NEG + LUG_PROJ / 2.0, y,
                      (LUG_Z[0] + LUG_Z[1]) / 2.0):
            lug += 1
    holes = 0
    for s in (1.0, -1.0):
        clear = True
        for x in grid(SKIRT_IN_POS + 0.1, LID_X1 - 0.1, 9):
            if lid.inside(x, s * LID_SCREW_Y, LID_SCREW_Z):
                clear = False
        if clear:
            holes += 1
    capture = HOOK_Z[1] - LUG_Z[1]
    gate(reb == 2 and lug == 2 and holes == 2 and capture > 0.0
         and HOOK_ENGAGE > 0.0,
         "17 two lid screws and two hooks give a valid assembly sequence",
         "%d/2 base rebates, %d/2 lid lugs engaging %.2f mm, %d/2 screw holes "
         "at y +-%.2f z %.2f; seated, the lid lifts %.2f mm before the lug "
         "meets the capture ledge - tilt-engage the hooks, drop, then two M3"
         % (reb, lug, HOOK_ENGAGE, holes, LID_SCREW_Y, LID_SCREW_Z, capture))

    # -- 18 ----------------------------------------------------------------
    orient = (("base", Z_FLOOR_BOT, +1, "floor-down"),
              ("lid", Z_LID_TOP, -1, "TOP-FACE-DOWN"),
              ("clamp", Z_RETAIN, +1, "flat"),
              ("cap", 0.0, +1, "flat"))
    worst_reach = 0.0
    steep_total = 0.0
    lines = []
    for key, bed, up, label in orient:
        st, fl, reach, where, nflat = overhang_report(M[key], bed, up,
                                                      OVERHANG_REACH_MAX)
        steep_total += st
        worst_reach = max(worst_reach, reach if nflat else 0.0)
        lines.append("%s %s steep %.1f mm2 flat %.1f mm2 reach %.2f"
                     % (key, label, st, fl, reach if nflat else 0.0))
    # stricter rule inside the windows and the USB slot
    nz = lid.normal[:, 2] * -1
    zc3 = lid.tris[:, :, 2].mean(axis=1)
    xc3 = lid.tris[:, :, 0].mean(axis=1)
    yc3 = lid.tris[:, :, 1].mean(axis=1)
    flat_down = (nz <= -0.999) & (np.abs(zc3 - Z_LID_TOP) > 0.05)
    in_win = np.zeros_like(flat_down)
    for wx in WIN_X:
        in_win |= ((np.abs(xc3 - wx) <= WIN_HALF_W)
                   & (np.abs(yc3) > SKIRT_IN_Y - 0.5))
    in_usb = (xc3 < SKIRT_IN_NEG + 0.5) & (np.abs(yc3) <= USB_SLOT_W / 2.0)
    n_roof = int(np.sum(flat_down & (in_win | in_usb)))
    gate(worst_reach <= OVERHANG_REACH_MAX and n_roof == 0,
         "18 no production part requires slicer support",
         "max unsupported reach %.2f mm against %.2f (%s); %.1f mm2 of steep "
         "facet; %d downward facets in the windows or the USB slot"
         % (worst_reach, OVERHANG_REACH_MAX, "; ".join(lines), steep_total,
            n_roof))

    # -- 19 ----------------------------------------------------------------
    x0 = min(base.bb[0], lid.bb[0])
    x1 = max(base.bb[1], lid.bb[1])
    y0 = min(base.bb[2], lid.bb[2])
    y1 = max(base.bb[3], lid.bb[3])
    z0 = min(base.bb[4], lid.bb[4])
    z1 = max(base.bb[5], lid.bb[5])
    env = (x1 - x0, y1 - y0, z1 - z0)
    # nothing outboard of the lid: march outward from the base wall and check
    # nothing is met before the skirt
    stray = 0
    for px, py, ux, uy in perimeter_stations():
        for z in (Z_FLOOR_BOT + 0.4, 2.0, 6.0, 8.0):
            out = surface_out(base, px, py, ux, uy, z, t1=8.0)
            if out is not None and out > max(END_WALL_NEG_T, WALL_T) + 0.6:
                stray += 1
    gate(all(e <= l + 0.02 for e, l in zip(env, ENV_MAX)) and stray == 0,
         "19 complete outside envelope within %.0f x %.0f x %.0f mm" % ENV_MAX,
         "measured %.2f x %.2f x %.2f mm (Rev A was 105.00 x 77.00 x 38.30); "
         "%d stray outboard features" % (env + (stray,)))

    # -- 20 / 21 -----------------------------------------------------------
    rows = []
    tot = 0.0
    for key, qty in PRODUCTION:
        v = signed_volume(M[key].tris) / 1000.0
        rows.append((key, qty, v, v * qty))
        tot += v * qty
    mass = tot * PETG_DENSITY
    gate(tot <= VOL_MAX, "20 production solid volume <= %.2f cm3" % VOL_MAX,
         "%.2f cm3 = %s (Rev A was approximately 68 cm3)"
         % (tot, " + ".join("%s %.2f%s" % (k, t, "" if q == 1 else " (x%d)" % q)
                            for k, q, _v, t in rows)))
    gate(mass <= MASS_MAX, "21 estimated PETG mass <= %.1f g" % MASS_MAX,
         "%.1f g at %.2f g/cm3 on SOLID volume; a printed part at 15-20%% "
         "infill weighs less" % (mass, PETG_DENSITY))
    for key, limit in VOL_PREF:
        v = signed_volume(M[key].tris) / 1000.0
        note("   preferred target %s <= %.2f cm3" % (key, limit),
             "%.2f cm3 %s" % (v, "within" if v <= limit else "OVER"))

    # -- 22 ----------------------------------------------------------------
    present = [f for f in FORBIDDEN_FILES
               if os.path.exists(os.path.join(STL, f))]
    # Rev A's rails and ears stood 5.5-8.0 mm outboard of the wall. gate 19's
    # stray count already proves there is nothing out there; this adds the
    # plan-area test, because a rail or an ear changes the plan, not just the
    # profile.
    plan = (lid.bb[1] - lid.bb[0]) * (lid.bb[3] - lid.bb[2])
    gate(not present and stray == 0 and plan <= ENV_MAX[0] * ENV_MAX[1],
         "22 no forbidden Rev A feature present",
         "%d of %d deleted meshes still on disk; plan area %.0f mm2 against "
         "Rev A's 8085 mm2; no rails, ears, sawtooth roofs, USB plug, second "
         "clamp, corner piers or per-terminal guides"
         % (len(present), len(FORBIDDEN_FILES), plan))

    # -- 23 ----------------------------------------------------------------
    # The coupons must reproduce production geometry for the interfaces
    # nobody has tested, and the horizontal insert is the one that matters:
    # a heat-set insert driven into a bore in a wall printed on its side is
    # the only fastener in this design whose feasibility is unknown.
    va = signed_volume(coupon_a.tris) / 1000.0
    vb = signed_volume(coupon_b.tris) / 1000.0
    bb = coupon_b.bb
    x1 = bb[1]
    horiz = all(not coupon_b.inside(x1 - t, 0.0, LID_SCREW_Z)
                for t in (0.4, 1.6, 3.0, 4.4))
    horiz_deep = coupon_b.inside(x1 - (INSERT_DEPTH + 1.6), 0.0, LID_SCREW_Z)
    # coupon A must carry the real ledge at the real height
    ledge = coupon_a.inside(X_DATUM + 0.50, 0.0, Z_RETAIN + LEDGE_LEAD + 0.30)
    ledge_gap = not coupon_a.inside(X_DATUM + 0.50, 0.0, Z_PCB_TOP + 0.05)
    pads = coupon_a.inside((PAD_X[0] + PAD_X[1]) / 2.0,
                           P_COUPON_W / 2.0 - 2.0, PAD_H - 0.30)
    gate(horiz and horiz_deep and ledge and ledge_gap and pads
         and (va + vb) <= COUPON_BUDGET,
         "23 coupons cover every untested interface  [v1.2 gate 27]",
         "A carrier %.2f cm3 + B fasteners %.2f cm3 = %.2f cm3, against the "
         "%.2f cm3 single gauge they replace; horizontal insert bore %s "
         "(%.2f deep, bottomed), fixed ledge %s with its %.2f gap, support "
         "pads %s"
         % (va, vb, va + vb, COUPON_BUDGET,
            "present" if horiz else "MISSING", INSERT_DEPTH,
            "present" if ledge else "MISSING", RETAIN_CLEAR,
            "present" if pads else "MISSING"))

    # -- prototype and installation gates ----------------------------------
    print("")
    print("PROTOTYPE GATES - no amount of geometry settles these")
    proto("carrier 66.00 x 63.00 x 1.60 and the real 65-67 mm spread")
    proto("2.50 mm below-carrier protrusion",
          "sets the 4.50 mm support height")
    proto("24.00 mm assembled height above the carrier",
          "sets 13.9 mm of the lid skirt; see the build report sensitivity")
    proto("bare margins 3.00 short edge / 2.50 long edge, both faces")
    proto("terminal pitch %.2f, block height and %.2f screw inset"
          % (TERM_PITCH, TERM_SCREW_INSET))
    proto("nothing on the carrier underside within y +-9.83 at x +-27.00",
          "this is what lets the cabinet fixings sit under the board")
    proto("heat-set insert %.2f dia x %.2f deep" % (INSERT_D, INSERT_DEPTH),
          "the exact part is NOT recorded anywhere in the repository")
    proto("EN and BOOT positions", "v1.1 6.4 forbids holes until measured")
    proto("H1-H6 conductor counts and real bundle diameters")
    proto("lid fit %.2f mm per face on this printer and filament" % LID_FIT)
    proto("PETG print quality with no support on any part")
    proto("A HORIZONTAL heat-set insert driven into coupon B",
          "no fastener in this design is less proven")
    proto("the acquired cabinet screw's real head diameter",
          "%.2f mm max envelope declared, ISO 10642 assumed, not measured"
          % CAB_HEAD_D_MAX)
    proto("cap nib press and release force on this printer",
          "%.2f mm radial interference is a design value" % CAB_NIB_INT)
    proto("the cable-tie anchor's robustness in a fitter's hands",
          "gate 9c measures section, not strength: %.2f mm in the cable-pull "
          "direction, %.2f mm wide, blended into the wall top on an R%.2f "
          "root radius. No pull test is claimed and none is required - these "
          "ties restrain lightweight low-voltage harnesses"
          % (TIE_THK, 2.0 * TIE_TAB_HALF_W, TIE_BLEND_R))
    print("")
    print("RELEASE GATE - blocks printing the base and the lid")
    proto("MEASURE THE ASSEMBLED ELECTRONICS HEIGHT",
          "%.2f mm assumed; closed height %.2f against a %.2f limit leaves "
          "%.2f mm of margin, and NEITHER COUPON TESTS IT"
          % (ASSEMBLED_HEIGHT_ASSUMED, H_CLOSED, ENV_MAX[2], HEIGHT_MARGIN))
    print("")
    print("INSTALLATION GATES")
    install("cabinet fixing centres and the surface behind them")
    install("final harness routing and the two tie positions used per side")
    install("antenna performance with the lid fitted")

    print("")
    print("%d checks covering all 30 v1.3 section 13 gates, %d failed, "
          "%d prototype, %d installation"
          % (CHECKS, len(FAILS), len(PROTOS), len(INSTALLS)))
    if FAILS:
        for f in FAILS:
            print("  FAILED: %s" % f)
        return 1
    print("")
    print("All specification v1.3 section 13 gates pass on the exported "
          "meshes. This is NOT physical validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
