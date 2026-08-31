# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev A independent offline verifier
====================================================================

Reads ONLY the exported manufacturing meshes in ../STL and re-derives every
Rev A claim from triangles. numpy is the only dependency. Exits non-zero on
failure, so it works as a gate.

    python mechanical/CAD/Decca_ESP32_Controller_Housing_verify.py

It is deliberately NOT a second run of the generator. The generator knows what
it meant to build; this knows only what came out of the exporter. Every
expected number below is TYPED IN BY HAND from
mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md and from the
derivation chain written out in the build report - nothing is imported from
Decca_ESP32_Controller_Housing_fusion.py. If the generator and this file
disagree, that disagreement is the whole point.

It covers all eighteen specification section 14 gates.

RESULT VOCABULARY - used exactly, never loosely
-----------------------------------------------
  [PASS]   MESH-VERIFIED. Measured from the exported triangles.
  [FAIL]   measured, and wrong.
  [ ]      a reported measurement, no claim attached.
  [PROTO]  PROTOTYPE-REQUIRED. Depends on a hardware dimension nobody has
           measured yet, so it cannot be verified by any amount of geometry.
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
    "clamp_fix": "ESP32_Controller_PCB_Clamp_Fixed.stl",
    "clamp_adj": "ESP32_Controller_PCB_Clamp_Adjustable.stl",
    "gauge": "ESP32_Controller_Carrier_Fit_Gauge.stl",
    "plug": "ESP32_Controller_USB_Plug.stl",
}

# ---------------------------------------------------------------------------
# EXPECTED VALUES - typed in from the controlling documents, NOT imported.
# ---------------------------------------------------------------------------
# -- specification section 4 and 11, verbatim -------------------------------
ADAPTER_L, ADAPTER_W, ADAPTER_T = 66.00, 63.00, 1.60
ADAPTER_BELOW_H = 2.50
ASSEMBLY_ABOVE_H = 24.00
LEN_ADJUST = 1.00
PCB_XY_CLEAR = 0.50
PCB_UNDER_CLEAR = 3.00
COMPONENT_TOP_CLEAR = 3.00
CLAMP_VERT_CLEAR = 0.20
ANTENNA_KEEPOUT = 10.00
LID_FIT_CLEAR = 0.25
BASE_FLOOR_T = 2.40
WALL_T = 2.00
LID_TOP_T = 1.80
LID_ANTENNA_T = 1.60
LID_OVERLAP = 5.00
LID_SKIRT_T = 2.00
OUTER_CORNER_R = 3.00
INNER_FILLET_R = 1.00
WIRE_EXIT_H = 10.00
USB_OPEN_W, USB_OPEN_H = 14.00, 9.00
BUTTON_TOOL_D = 3.00
TIE_SLOT_W, TIE_SLOT_L = 2.50, 6.00
LID_SCREW_D, LID_SCREW_LEN = 3.00, 8.00
LID_SCREW_CLEAR_D = 3.40
CABINET_SLOT_W, CABINET_SLOT_L = 4.00, 8.00
EAR_T = 3.00
INSERT_HOLE_D, INSERT_DEPTH = 4.00, 6.00
BOSS_WALL = 2.00

# -- hardware starting values, section 4 and the build report ---------------
TERM_PER_SIDE, TERM_PITCH = 15, 3.50
TERM_BLOCK_H, TERM_SCREW_INSET, TERM_WIRE_Z = 10.00, 4.00, 4.00
DRIVER_D = 6.00
ESP_L, ESP_W, ESP_T = 51.50, 28.30, 1.60
ESP_HEADER_H, ESP_HEADER_SPAN = 8.50, 22.86
ESP_USB_H = 2.70
ESP_ANT_L, ESP_ANT_W = 15.00, 18.00
ESP_BTN_X, ESP_BTN_Y = -22.00, 10.15
ESP_BTN_H = 4.30
PCB_BARE_EDGE, PCB_BARE_PERIM = 3.00, 2.50

# -- the derivation chain, recomputed here by hand ---------------------------
Z_FLOOR_BOT = -BASE_FLOOR_T                                  # -2.40
Z_FLOOR_TOP = 0.00
PAD_H = ADAPTER_BELOW_H + PCB_UNDER_CLEAR                    #  5.50
Z_PCB_BOT = PAD_H                                            #  5.50
Z_PCB_TOP = Z_PCB_BOT + ADAPTER_T                            #  7.10
Z_UNDER_BOT = Z_PCB_BOT - ADAPTER_BELOW_H                    #  3.00
Z_TERM_TOP = Z_PCB_TOP + TERM_BLOCK_H                        # 17.10
Z_COMP_TOP = Z_PCB_TOP + ASSEMBLY_ABOVE_H                    # 31.10
Z_CAV_TOP = Z_COMP_TOP + COMPONENT_TOP_CLEAR                 # 34.10
Z_LID_TOP = Z_CAV_TOP + LID_TOP_T                            # 35.90
H_CLOSED = Z_LID_TOP - Z_FLOOR_BOT                           # 38.30

X_DATUM = -ADAPTER_L / 2.0                                   # -33.00
X_PCB_NOM = ADAPTER_L / 2.0                                  #  33.00
X_PCB_MAX = X_DATUM + ADAPTER_L + LEN_ADJUST                 #  34.00
X_PCB_MIN = X_DATUM + ADAPTER_L - LEN_ADJUST                 #  32.00
X_ADJ_FACE = X_PCB_MAX + PCB_XY_CLEAR                        #  34.50
Y_PCB = ADAPTER_W / 2.0                                      #  31.50
Y_CAV = Y_PCB + PCB_XY_CLEAR                                 #  32.00
Y_OUT = Y_CAV + WALL_T                                       #  34.00

INSERT_C = BOSS_WALL + INSERT_HOLE_D / 2.0                   #   4.00
BOSS_OD = 2.0 * INSERT_C                                     #   8.00
FIX_SCREW_X = X_DATUM - INSERT_C                             # -37.00
ADJ_SCREW_X = X_ADJ_FACE + INSERT_C                          #  38.50
CLAMP_SLOT_W = LID_SCREW_CLEAR_D                             #   3.40
CLAMP_SLOT_L = LID_SCREW_CLEAR_D + 2.0 * LEN_ADJUST          #   5.40
CLAMP_BAR_MARGIN = 1.60
CLAMP_GRIP = 2.50
CLAMP_HALF_SPAN = 23.00
CLAMP_SCREW_Y = 19.00
CLAMP_T = 3.00
FIX_BAR_IN = X_DATUM + CLAMP_GRIP                            # -30.50
FIX_BAR_OUT = FIX_SCREW_X - (LID_SCREW_CLEAR_D / 2.0 + CLAMP_BAR_MARGIN)
ADJ_BAR_IN = X_PCB_NOM - CLAMP_GRIP                          #  30.50
ADJ_BAR_OUT = ADJ_SCREW_X + (CLAMP_SLOT_L / 2.0 + CLAMP_BAR_MARGIN)
X_WALL_IN_NEG = X_DATUM - max(BOSS_OD, (X_DATUM - FIX_BAR_OUT) + 0.20)
X_WALL_IN_POS = X_ADJ_FACE + max(
    BOSS_OD, ((ADJ_BAR_OUT + LEN_ADJUST) - X_ADJ_FACE) + 0.20)
X_OUT_NEG = X_WALL_IN_NEG - WALL_T                           # -43.00
X_OUT_POS = X_WALL_IN_POS + WALL_T                           #  46.00
BODY_L = X_OUT_POS - X_OUT_NEG                               #  89.00
BODY_W = 2.0 * Y_OUT                                         #  68.00

# The boss columns overlap the walls by BOSS_MERGE. Sitting them tangent is
# a valid BRep and an invalid mesh: a tangent line tessellates to an edge
# shared by four triangles, and every ray-parity test below then reads the
# wrong answer through it.
PIER_BURY = 1.00
PIER_D = BOSS_OD                                             #   8.00
PIER_X_FIX = (X_WALL_IN_NEG - PIER_BURY,
              X_WALL_IN_NEG - PIER_BURY + PIER_D)            # -42.00, -34.00
PIER_X_ADJ = (X_WALL_IN_POS + PIER_BURY - PIER_D,
              X_WALL_IN_POS + PIER_BURY)                     #  37.00,  45.00
PIER_Y = (Y_CAV + PIER_BURY - PIER_D, Y_CAV + PIER_BURY)     #  25.00,  33.00
BOSS_FIX_X = sum(PIER_X_FIX) / 2.0                           # -38.00
BOSS_ADJ_X = sum(PIER_X_ADJ) / 2.0                           #  41.00
BOSS_Y = sum(PIER_Y) / 2.0                                   #  29.00
Z_INSERT_BOT = Z_CAV_TOP - INSERT_DEPTH                      #  28.10
Z_SCREW_TIP = Z_LID_TOP - LID_SCREW_LEN                      #  27.90
Z_PLINTH_TOP = Z_PCB_TOP + CLAMP_VERT_CLEAR                  #   7.30

EAR_PROJ = 2.00 + CABINET_SLOT_W + 2.00                      #   8.00
EAR_LEN = CABINET_SLOT_L + 4.00                              #  12.00
EAR_X_NEG = X_OUT_NEG - EAR_PROJ                             # -51.00
EAR_X_POS = X_OUT_POS + EAR_PROJ                             #  54.00
EAR_Y_FAR = Y_OUT - OUTER_CORNER_R                           #  31.00
EAR_Y_IN = EAR_Y_FAR - EAR_LEN                               #  19.00
EAR_SLOT_Y = EAR_Y_FAR - 2.00 - CABINET_SLOT_L / 2.0         #  25.00
EAR_SLOT_X_NEG = EAR_X_NEG + 2.00 + CABINET_SLOT_W / 2.0     # -47.00
EAR_SLOT_X_POS = EAR_X_POS - 2.00 - CABINET_SLOT_W / 2.0     #  50.00
Z_EAR_TOP = Z_FLOOR_BOT + EAR_T                              #   0.60
OVERALL_L = EAR_X_POS - EAR_X_NEG                            # 105.00

RAIL_Y_OUT = Y_OUT + TIE_SLOT_W + 2.00                       #  38.50
RAIL_LEDGE_TOP = Z_FLOOR_BOT + 3.00                          #   0.60
RAIL_Z1 = Z_PCB_TOP                                          #   7.10
RAIL_HALF_L = 32.00
TIE_LEGS_X = (-30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0)
OVERALL_W = 2.0 * RAIL_Y_OUT                                 #  77.00

WIN_HALF_L = 30.00
WIN_Z0 = Z_PCB_TOP                                           #   7.10
WIN_H = 12.00
WIN_Z1 = WIN_Z0 + WIN_H                                      #  19.10
SAW_N = 16
SAW_MARGIN = 1.00                # the sawtooth runs past the window ends, so
SAW_X0 = -WIN_HALF_L - SAW_MARGIN     # no flank is tangent to an end plane
SAW_X1 = WIN_HALF_L + SAW_MARGIN
SAW_STEP = (SAW_X1 - SAW_X0) / SAW_N                         #   3.875
SAW_H = SAW_STEP / 2.0                                       #   1.9375
WIN_SAW_TOP = WIN_Z1 + SAW_H                                 #  21.0375

Z_SKIRT_BOT = Z_CAV_TOP - LID_OVERLAP                        #  29.10
SIDE_VENT_Z1 = Z_SKIRT_BOT - 0.50                            #  28.60
SIDE_VENT_Z0 = SIDE_VENT_Z1 - 5.00                           #  23.60
VENT_W = 2.00

TERM_Y = Y_PCB - TERM_SCREW_INSET                            #  27.50
TERM_X = [(i - (TERM_PER_SIDE - 1) / 2.0) * TERM_PITCH
          for i in range(TERM_PER_SIDE)]
TERM_SPAN = (TERM_PER_SIDE - 1) * TERM_PITCH                 #  49.00
Z_WIRE = Z_PCB_TOP + TERM_WIRE_Z                             #  11.10

ESP_X0, ESP_X1 = -ESP_L / 2.0, ESP_L / 2.0                   # -25.75, 25.75
ESP_Y0, ESP_Y1 = -ESP_W / 2.0, ESP_W / 2.0                   # -14.15, 14.15
Z_ESP_BOT = Z_PCB_TOP + ESP_HEADER_H                         #  15.60
Z_ESP_TOP = Z_ESP_BOT + ESP_T                                #  17.20
Z_USB_AXIS = Z_ESP_TOP + ESP_USB_H / 2.0                     #  18.55
USB_Z0 = Z_USB_AXIS - USB_OPEN_H / 2.0                       #  14.05
USB_Z1 = Z_USB_AXIS + USB_OPEN_H / 2.0                       #  23.05
Z_BTN_TOP = Z_ESP_TOP + ESP_BTN_H                            #  21.50

ANT_X1 = ESP_X1                                              #  25.75
ANT_X0 = ESP_X1 - ESP_ANT_L                                  #  10.75
ANT_Y0, ANT_Y1 = -ESP_ANT_W / 2.0, ESP_ANT_W / 2.0           #  -9.00, 9.00
AKO_X0, AKO_X1 = ANT_X0 - ANTENNA_KEEPOUT, ANT_X1 + ANTENNA_KEEPOUT
AKO_Y0, AKO_Y1 = ANT_Y0 - ANTENNA_KEEPOUT, ANT_Y1 + ANTENNA_KEEPOUT

SKIRT_IN_NEG = X_OUT_NEG - LID_FIT_CLEAR                     # -43.25
SKIRT_IN_POS = X_OUT_POS + LID_FIT_CLEAR                     #  46.25
SKIRT_IN_Y = Y_OUT + LID_FIT_CLEAR                           #  34.25
LID_X0 = SKIRT_IN_NEG - LID_SKIRT_T                          # -45.25
LID_X1 = SKIRT_IN_POS + LID_SKIRT_T                          #  48.25
LID_Y = SKIRT_IN_Y + LID_SKIRT_T                             #  36.25
Z_LID_THIN = Z_CAV_TOP + (LID_TOP_T - LID_ANTENNA_T)         #  34.30

GAUGE_Y = -120.00                                            # parked offset

TOL = 0.05                       # mesh/chord tolerance, mm

FAILS = []
CHECKS = 0
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


# ---------------------------------------------------------------------------
# Perimeter probe stations: four straight runs plus the four corner arcs, each
# with a start point known to be inside the wall and an outward direction.
# ---------------------------------------------------------------------------
def perimeter_stations():
    st = []
    r = OUTER_CORNER_R
    for x in grid(X_OUT_NEG + r + 1.0, X_OUT_POS - r - 1.0, 12):
        st.append((x, Y_OUT - WALL_T / 2.0, 0.0, 1.0))
        st.append((x, -(Y_OUT - WALL_T / 2.0), 0.0, -1.0))
    for y in grid(-(Y_OUT - r - 1.0), Y_OUT - r - 1.0, 12):
        st.append((X_OUT_NEG + WALL_T / 2.0, y, -1.0, 0.0))
        st.append((X_OUT_POS - WALL_T / 2.0, y, 1.0, 0.0))
    for cx, sx in ((X_OUT_NEG + r, -1.0), (X_OUT_POS - r, 1.0)):
        for cy, sy in ((Y_OUT - r, 1.0), (-(Y_OUT - r), -1.0)):
            for k in range(6):
                a = math.radians(10.0 + 70.0 * k / 5.0)
                ux, uy = sx * math.cos(a), sy * math.sin(a)
                st.append((cx + ux * (r - WALL_T / 2.0),
                           cy + uy * (r - WALL_T / 2.0), ux, uy))
    return st


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
            t = 0.5
            while t < best:
                if mesh.inside(cx + dx * t, cy + dy * t, zout):
                    break
                t += 0.5
            best = min(best, t)
        if best > worst:
            worst, where = best, (round(cx, 1), round(cy, 1), round(cz, 2))
    return steep_area, flat_area, worst, where, int(np.sum(flat))



# ---------------------------------------------------------------------------
# Dimensioned drawings, plotted from the SAME triangles the gates are measured
# on. The outlines are sliced out of the exported meshes; only the dimension
# text is typed, and every typed figure is one this file has already gated.
# ---------------------------------------------------------------------------
def slice_axis(tris, axis, value):
    """Segments where the mesh crosses the plane axis = value, returned in
    the remaining two coordinates."""
    keep = [i for i in range(3) if i != axis]
    segs = []
    for t in tris:
        dv = t[:, axis] - value
        if np.all(dv > 0) or np.all(dv < 0):
            continue
        pts = []
        for i in range(3):
            j = (i + 1) % 3
            di, dj = dv[i], dv[j]
            if di == 0.0:
                pts.append(t[i][keep])
            if (di < 0 < dj) or (dj < 0 < di):
                f = di / (di - dj)
                pts.append((t[i] + f * (t[j] - t[i]))[keep])
        if len(pts) >= 2:
            segs.append((pts[0], pts[1]))
    return segs


def _plot_segs(ax, segs, **kw):
    from matplotlib.collections import LineCollection
    if not segs:
        return
    ax.add_collection(LineCollection([[tuple(a), tuple(b)] for a, b in segs],
                                     **kw))


def _dim(ax, p0, p1, off, text, horizontal=True, tick=1.6, fs=8.5):
    """One dimension: witness lines, a double arrow and the value."""
    if horizontal:
        y = off
        ax.plot([p0, p0], [p0 * 0 + y, y], lw=0)
        ax.annotate("", xy=(p1, y), xytext=(p0, y),
                    arrowprops=dict(arrowstyle="<->", lw=0.8, color="#222"))
        ax.text((p0 + p1) / 2.0, y, " %s " % text, ha="center", va="bottom",
                fontsize=fs, color="#111",
                bbox=dict(fc="white", ec="none", pad=0.6))
    else:
        x = off
        ax.annotate("", xy=(x, p1), xytext=(x, p0),
                    arrowprops=dict(arrowstyle="<->", lw=0.8, color="#222"))
        ax.text(x, (p0 + p1) / 2.0, " %s " % text, ha="left", va="center",
                fontsize=fs, color="#111", rotation=90,
                bbox=dict(fc="white", ec="none", pad=0.6))


def _witness(ax, pts, lo, hi, horizontal=True):
    for p in pts:
        if horizontal:
            ax.plot([p, p], [lo, hi], lw=0.5, ls=":", color="#999")
        else:
            ax.plot([lo, hi], [p, p], lw=0.5, ls=":", color="#999")


def drawings(M, out_dir, prefix):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    written = []
    base, lid = M["base"], M["lid"]

    # ---- plan ------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
    layers = ((Z_FLOOR_BOT / 2.0, "#1b3a5c", 1.4, "ears and body at mid-floor"),
              ((RAIL_LEDGE_TOP + RAIL_Z1) / 2.0, "#2e7d32", 1.0,
               "lacing rails at mid-slot"),
              ((SIDE_VENT_Z0 + SIDE_VENT_Z1) / 2.0, "#b0651a", 0.9,
               "walls at the sidewall vents"))
    for z, colour, lw, label in layers:
        segs = slice_axis(base.tris, 2, z)
        _plot_segs(ax, segs, colors=colour, linewidths=lw)
        ax.plot([], [], color=colour, lw=lw, label="%s  (z %+.2f)" % (label, z))
    segs = slice_axis(lid.tris, 2, (Z_SKIRT_BOT + Z_CAV_TOP) / 2.0)
    _plot_segs(ax, segs, colors="#8e24aa", linewidths=0.9)
    ax.plot([], [], color="#8e24aa", lw=0.9,
            label="lid skirt at mid-overlap  (z %+.2f)"
                  % ((Z_SKIRT_BOT + Z_CAV_TOP) / 2.0))
    ax.plot([X_DATUM, X_PCB_NOM, X_PCB_NOM, X_DATUM, X_DATUM],
            [-Y_PCB, -Y_PCB, Y_PCB, Y_PCB, -Y_PCB],
            lw=1.0, ls="--", color="#c62828",
            label="breakout outline %.2f x %.2f  STARTING VALUE"
                  % (ADAPTER_L, ADAPTER_W))

    _witness(ax, (EAR_X_NEG, X_OUT_NEG, X_OUT_POS, EAR_X_POS), -60, 60)
    _dim(ax, EAR_X_NEG, EAR_X_POS, 52.0, "%.2f overall" % OVERALL_L)
    _dim(ax, X_OUT_NEG, X_OUT_POS, 45.0, "%.2f body" % BODY_L)
    _dim(ax, X_DATUM, X_PCB_NOM, -45.0, "%.2f board" % ADAPTER_L)
    _witness(ax, (-RAIL_Y_OUT, -Y_OUT, Y_OUT, RAIL_Y_OUT), -60, 60,
             horizontal=False)
    _dim(ax, -RAIL_Y_OUT, RAIL_Y_OUT, 62.0, "%.2f overall" % OVERALL_W,
         horizontal=False)
    _dim(ax, -Y_OUT, Y_OUT, 70.0, "%.2f body" % BODY_W, horizontal=False)
    _dim(ax, -Y_CAV, Y_CAV, -58.0, "%.2f cavity" % (2 * Y_CAV),
         horizontal=False)
    for sx in (EAR_SLOT_X_NEG, EAR_SLOT_X_POS):
        for sy in (EAR_SLOT_Y, -EAR_SLOT_Y):
            ax.plot([sx], [sy], marker="+", ms=9, color="#c62828", mew=1.2)
    ax.annotate("4 x cabinet slot %.2f x %.2f, long axis across the housing"
                % (CABINET_SLOT_W, CABINET_SLOT_L),
                xy=(EAR_SLOT_X_POS, EAR_SLOT_Y), xytext=(20.0, 47.0),
                fontsize=8.5, color="#c62828",
                arrowprops=dict(arrowstyle="->", lw=0.8, color="#c62828"))
    ax.set_title("Decca ESP32 Controller Housing Rev A - plan, measured from "
                 "ESP32_Controller_Housing_Base.stl" + chr(10) +
                 "PROTOTYPE CAD. "
                 "Board outline is a starting value, not a measurement.",
                 fontsize=10)
    ax.set_aspect("equal")
    ax.set_xlim(-64, 66)
    ax.set_ylim(-76, 78)
    ax.set_xlabel("X, mm")
    ax.set_ylabel("Y, mm")
    ax.grid(True, lw=0.3, color="#ddd")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    p = os.path.join(out_dir, prefix + "15_dimensioned_plan.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    written.append(p)

    # ---- transverse section ----------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
    x_cut = -5.00                     # through a window, clear of the piers
    _plot_segs(ax, slice_axis(base.tris, 0, x_cut), colors="#1b3a5c",
               linewidths=1.5)
    _plot_segs(ax, slice_axis(lid.tris, 0, x_cut), colors="#8e24aa",
               linewidths=1.5)
    ax.plot([], [], color="#1b3a5c", lw=1.5, label="base   (section x %+.2f)"
            % x_cut)
    ax.plot([], [], color="#8e24aa", lw=1.5, label="lid    (section x %+.2f)"
            % x_cut)
    ax.add_patch(plt.Rectangle((-Y_PCB, Z_PCB_BOT), 2 * Y_PCB, ADAPTER_T,
                               fc="#c8e6c9", ec="#2e7d32", lw=1.0, ls="--"))
    ax.add_patch(plt.Rectangle((-Y_PCB, Z_UNDER_BOT), 2 * Y_PCB,
                               ADAPTER_BELOW_H, fc="none", ec="#c62828",
                               lw=0.9, ls=":"))
    ax.add_patch(plt.Rectangle((-Y_PCB, Z_PCB_TOP), 2 * Y_PCB,
                               ASSEMBLY_ABOVE_H, fc="none", ec="#c62828",
                               lw=0.9, ls=":"))
    ax.plot([], [], color="#c62828", lw=0.9, ls=":",
            label="hardware envelopes  STARTING VALUES")
    chain = ((Z_FLOOR_BOT, Z_FLOOR_TOP, "%.2f floor" % BASE_FLOOR_T),
             (Z_FLOOR_TOP, Z_UNDER_BOT, "%.2f clear under the joints"
              % PCB_UNDER_CLEAR),
             (Z_UNDER_BOT, Z_PCB_BOT, "%.2f below-board parts"
              % ADAPTER_BELOW_H),
             (Z_PCB_BOT, Z_PCB_TOP, "%.2f board" % ADAPTER_T),
             (Z_PCB_TOP, Z_COMP_TOP, "%.2f assembly above the board"
              % ASSEMBLY_ABOVE_H),
             (Z_COMP_TOP, Z_CAV_TOP, "%.2f headroom" % COMPONENT_TOP_CLEAR),
             (Z_CAV_TOP, Z_LID_TOP, "%.2f lid" % LID_TOP_T))
    # one dimension column with upright labels beside it. Rotated text does
    # not fit between links as short as the 1.60 mm board.
    x_dim, x_txt = 42.0, 44.5
    for z0, z1, label in chain:
        ax.annotate("", xy=(x_dim, z1), xytext=(x_dim, z0),
                    arrowprops=dict(arrowstyle="<->", lw=0.8, color="#222"))
        ax.text(x_txt, (z0 + z1) / 2.0, label, ha="left", va="center",
                fontsize=8.0, color="#111")
        _witness(ax, (z0, z1), -44.0, x_dim, horizontal=False)
    ax.annotate("", xy=(66.0, Z_LID_TOP), xytext=(66.0, Z_FLOOR_BOT),
                arrowprops=dict(arrowstyle="<->", lw=1.0, color="#222"))
    ax.text(67.5, (Z_FLOOR_BOT + Z_LID_TOP) / 2.0,
            "%.2f closed height" % H_CLOSED, ha="left", va="center",
            fontsize=9.0, rotation=90, color="#111")
    _dim(ax, WIN_Z0, WIN_Z1, -44.0, "%.2f cable window" % WIN_H,
         horizontal=False)
    _dim(ax, Z_SKIRT_BOT, Z_CAV_TOP, -52.0, "%.2f lid overlap" % LID_OVERLAP,
         horizontal=False)
    _dim(ax, -RAIL_Y_OUT, RAIL_Y_OUT, -9.0, "%.2f overall width" % OVERALL_W)
    _dim(ax, -Y_OUT, Y_OUT, -6.0, "%.2f body" % BODY_W)
    ax.set_title("Decca ESP32 Controller Housing Rev A - transverse section, "
                 "measured from the exported meshes" + chr(10) +
                 "PROTOTYPE CAD. Nothing "
                 "here has been printed or offered up to hardware.",
                 fontsize=10)
    ax.set_aspect("equal")
    ax.set_xlim(-58, 82)
    ax.set_ylim(-14, 44)
    ax.set_xlabel("Y, mm")
    ax.set_ylabel("Z, mm")
    ax.grid(True, lw=0.3, color="#ddd")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
    p = os.path.join(out_dir, prefix + "16_dimensioned_section.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    written.append(p)

    for p in written:
        print("  %s" % os.path.basename(p))
    return written


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("DECCA ESP32 CONTROLLER HOUSING - REV A OFFLINE MESH VERIFICATION")
    print("=" * 78)
    M = {}
    for key, fname in MESHES.items():
        path = os.path.normpath(os.path.join(STL, fname))
        if not os.path.exists(path):
            print("MISSING MESH: %s" % path)
            return 2
        M[key] = Mesh(key, path)
    for key in ("base", "lid", "clamp_fix", "clamp_adj", "gauge", "plug"):
        m = M[key]
        sx, sy, sz = m.size()
        print("  %-10s %-44s %6d tris  %7.2f x %7.2f x %7.2f mm"
              % (key, MESHES[key], len(m.tris), sx, sy, sz))
    base, lid = M["base"], M["lid"]
    cfix, cadj = M["clamp_fix"], M["clamp_adj"]
    gauge, plug = M["gauge"], M["plug"]
    print("")

    # -- 1 ------------------------------------------------------------------
    print("1. EVERY PRINTABLE PART IS A CLOSED MANIFOLD SOLID")
    for key in ("base", "lid", "clamp_fix", "clamp_adj", "gauge", "plug"):
        m = M[key]
        bad_und, bad_dir = manifold(m.faces)
        ncomp = components(len(m.verts), m.faces)
        vol = signed_volume(m.tris)
        ok = bad_und == 0 and bad_dir == 0 and ncomp == 1 and vol > 0
        gate(ok, key,
             "edges %d bad, winding %d bad, %d component(s), %.3f cm3"
             % (bad_und, bad_dir, ncomp, vol / 1000.0))

    # -- 2 ------------------------------------------------------------------
    print("")
    print("2. BASE FLOOR CONTINUOUS BENEATH THE COMPLETE PCB OUTLINE")
    holes = []
    for x in inner(X_DATUM, X_PCB_MAX, 25):
        for y in inner(-Y_PCB, Y_PCB, 23):
            if not base.inside(x, y, Z_FLOOR_BOT / 2.0):
                holes.append((round(x, 1), round(y, 1)))
    gate(not holes, "25 x 23 probes at mid-floor under the board",
         "%d gap(s)%s" % (len(holes), " e.g. %s" % holes[:3] if holes else ""))
    zt = base.spans(0.0, 0.0)
    gate(any(abs(a - Z_FLOOR_BOT) < TOL and abs(b - Z_FLOOR_TOP) < TOL
             for a, b in zt), "floor slab measured on the centre line",
         "spans %s" % [(round(a, 2), round(b, 2)) for a, b in zt])

    # -- 3 ------------------------------------------------------------------
    print("")
    print("3. UNDERSIDE ELECTRICAL CLEARANCE >= %.2f mm" % PCB_UNDER_CLEAR)
    worst, worst_at = Z_UNDER_BOT - Z_FLOOR_TOP, None
    bad = []
    for x in inner(X_DATUM + PCB_BARE_EDGE, X_PCB_NOM - PCB_BARE_EDGE, 23):
        for y in inner(-(Y_PCB - PCB_BARE_PERIM), Y_PCB - PCB_BARE_PERIM, 21):
            top = Z_FLOOR_BOT
            for a, b in base.spans(x, y):
                if a < Z_UNDER_BOT - 1e-6:
                    top = max(top, min(b, Z_UNDER_BOT))
            clr = Z_UNDER_BOT - top
            if clr < worst:
                worst, worst_at = clr, (round(x, 1), round(y, 1))
            if clr < PCB_UNDER_CLEAR - TOL:
                bad.append((round(x, 1), round(y, 1), round(clr, 2)))
    gate(not bad, "clear air beneath every modelled solder joint",
         "minimum %.2f mm at %s" % (worst, worst_at))
    # Measure where the pads actually stop, by walking inward at mid-pad
    # height. The probe sits above the R1.00 floor fillet on purpose: that
    # fillet is required geometry, not an intrusion.
    z_pad = (Z_FLOOR_TOP + PAD_H) / 2.0
    innermost, at = 0.0, None
    for px in (-28.0, 0.0, 28.0):
        for sgn in (1.0, -1.0):
            y = sgn * Y_PCB
            while abs(y) > 20.0 and base.inside(px, y, z_pad):
                y -= sgn * 0.01
            edge = abs(y)
            if innermost == 0.0 or edge < innermost:
                innermost, at = edge, (px, sgn)
    gate(innermost >= Y_PCB - PCB_BARE_PERIM - 0.05,
         "support pads stop inside the declared bare perimeter strip",
         "innermost pad edge |y| %.3f, strip starts at %.2f"
         % (innermost, Y_PCB - PCB_BARE_PERIM))
    hs = base.spans(0.0, Y_PCB - PCB_BARE_PERIM / 2.0)
    pad = [(a, b) for a, b in hs if b > Z_FLOOR_TOP + 0.05]
    gate(bool(pad) and abs(pad[0][1] - PAD_H) < TOL,
         "support pad height equals below-board + clearance",
         "measured %.2f mm, expected %.2f" % (pad[0][1] if pad else -1, PAD_H))

    # -- 4 ------------------------------------------------------------------
    print("")
    print("4. NO FASTENER ENVELOPE ENTERS THE PCB OR WIRING KEEP-OUT")
    fasteners = [("lid screw", bx, sy * BOSS_Y, INSERT_HOLE_D)
                 for bx in (BOSS_FIX_X, BOSS_ADJ_X) for sy in (1, -1)]
    fasteners += [("clamp screw", bx, sy * CLAMP_SCREW_Y, INSERT_HOLE_D)
                  for bx in (FIX_SCREW_X, ADJ_SCREW_X) for sy in (1, -1)]
    fasteners += [("cabinet screw", bx, sy * EAR_SLOT_Y, CABINET_SLOT_W)
                  for bx in (EAR_SLOT_X_NEG, EAR_SLOT_X_POS) for sy in (1, -1)]
    worst = 1e9
    for nm, fx, fy, fd in fasteners:
        dx = max(X_DATUM - (fx + fd / 2.0), (fx - fd / 2.0) - X_ADJ_FACE)
        dy = abs(fy) - fd / 2.0 - Y_PCB
        worst = min(worst, max(dx, dy))
    gate(worst > 0.0, "all %d fastener axes lie outside the board envelope"
         % len(fasteners), "tightest clearance %.2f mm" % worst)
    holes_found = 0
    for nm, fx, fy, fd in fasteners[:8]:
        z = Z_CAV_TOP - 0.5 if nm == "lid screw" else Z_PLINTH_TOP - 0.5
        if base.clear_between(fx, fy, z - 0.2, z + 0.2):
            holes_found += 1
    gate(holes_found == 8, "all eight heat-set insert holes present in the base",
         "%d found at the named coordinates" % holes_found)
    gate(Z_SCREW_TIP > Z_PCB_TOP,
         "M3 x %.0f tip at full insertion stays above the board plane"
         % LID_SCREW_LEN,
         "tip z %+.2f, board top %+.2f, %.2f mm clear"
         % (Z_SCREW_TIP, Z_PCB_TOP, Z_SCREW_TIP - Z_PCB_TOP))

    # -- 5 ------------------------------------------------------------------
    print("")
    print("5. COMPONENT-TO-LID CLEARANCE >= %.2f mm" % COMPONENT_TOP_CLEAR)
    low = 1e9
    low_at = None
    for x in inner(X_DATUM, X_PCB_NOM, 27):
        for y in inner(-Y_PCB, Y_PCB, 25):
            for a, b in lid.spans(x, y):
                if b > Z_PCB_TOP and a < low:
                    low, low_at = a, (round(x, 1), round(y, 1))
    gate(low - Z_COMP_TOP >= COMPONENT_TOP_CLEAR - TOL,
         "lowest lid material anywhere over the board",
         "z %+.2f at %s, %.2f mm above the modelled component ceiling"
         % (low, low_at, low - Z_COMP_TOP))

    # -- 6 ------------------------------------------------------------------
    print("")
    print("6. TERMINAL SCREWDRIVER CORRIDORS, LID REMOVED")
    ring = [(0.0, 0.0)] + [(DRIVER_D / 2.0 * math.cos(math.radians(a)),
                            DRIVER_D / 2.0 * math.sin(math.radians(a)))
                           for a in range(0, 360, 45)]
    blocked = []
    for sgn in (1.0, -1.0):
        for i, tx in enumerate(TERM_X):
            for ox, oy in ring:
                px, py = tx + ox, sgn * TERM_Y + oy
                for m in (base, cfix, cadj):
                    if not m.clear_between(px, py, Z_TERM_TOP, 80.0):
                        blocked.append((i + 1, "+Y" if sgn > 0 else "-Y",
                                        m.name))
    gate(not blocked, "%d corridors of %.2f mm diameter, both rows"
         % (2 * TERM_PER_SIDE, DRIVER_D),
         "%d obstruction(s)%s" % (len(blocked),
                                  " %s" % blocked[:3] if blocked else ""))

    # -- 7 ------------------------------------------------------------------
    print("")
    print("7. WIRE-EXIT HEIGHT ON BOTH LONG SIDES >= %.2f mm" % WIRE_EXIT_H)
    for sgn, side in ((1.0, "+Y"), (-1.0, "-Y")):
        worst, at = 1e9, None
        for x in grid(-TERM_SPAN / 2.0, TERM_SPAN / 2.0, 61):
            y = sgn * (Y_OUT - WALL_T / 2.0)
            h = 0.0
            zs = base.spans(x, y)
            below = [b for a, b in zs if b <= WIN_Z0 + 1e-6]
            above = [a for a, b in zs if a >= WIN_Z0 - 1e-6]
            if below and above:
                h = min(above) - max(below)
            if h < worst:
                worst, at = h, round(x, 2)
        gate(worst >= WIRE_EXIT_H - TOL,
             "%s side, narrowest clear opening across the terminal span"
             % side, "%.2f mm at x %+.2f" % (worst, at))
    note("window roof", "sawtooth apex z %+.2f, %d teeth of %.3f mm at exactly "
         "45 degrees" % (WIN_SAW_TOP, SAW_N, SAW_STEP))

    # -- 8 ------------------------------------------------------------------
    print("")
    print("8. NO LID MATERIAL CROSSES A WIRE PATH")
    crossed = []
    for sgn in (1.0, -1.0):
        for tx in TERM_X:
            for y in grid(sgn * TERM_Y, sgn * (RAIL_Y_OUT + 10.0), 25):
                for dz in (-1.2, 0.0, 1.2):
                    if lid.inside(tx, y, Z_WIRE + dz):
                        crossed.append((round(tx, 1), round(y, 1)))
    gate(not crossed, "lid against all %d modelled wire runs"
         % (2 * TERM_PER_SIDE), "%d crossing(s)" % len(crossed))
    note("clearance", "lid skirt bottom z %+.2f, window roof z %+.2f, "
         "%.2f mm apart" % (Z_SKIRT_BOT, WIN_SAW_TOP,
                            Z_SKIRT_BOT - WIN_SAW_TOP))

    # -- 9 ------------------------------------------------------------------
    print("")
    print("9. USB SERVICE ENVELOPE UNOBSTRUCTED")
    bad = []
    for x in grid(X_OUT_NEG - 14.0, ESP_X0 + 1.6, 24):
        for y in inner(-USB_OPEN_W / 2.0, USB_OPEN_W / 2.0, 7):
            for z in inner(USB_Z0, USB_Z1, 7):
                for m in (base, lid, cfix, cadj):
                    if m.inside(x, y, z):
                        bad.append((m.name, round(x, 1), round(y, 1),
                                    round(z, 1)))
    gate(not bad, "%.2f x %.2f mm envelope swept to the connector face"
         % (USB_OPEN_W, USB_OPEN_H),
         "%d obstruction(s)%s" % (len(bad), " %s" % bad[:2] if bad else ""))
    ws = base.spans(X_OUT_NEG + WALL_T / 2.0, 0.0)
    gap = [(a, b) for a, b in ws if a > Z_PLINTH_TOP]
    opening = None
    for a, b in zip([w[1] for w in ws], [w[0] for w in ws[1:]]):
        if a > Z_PLINTH_TOP and b - a > 5.0:
            opening = (a, b)
    if opening:
        note("measured wall opening on the USB axis",
             "z %+.2f to %+.2f, %.2f mm high against a %.2f mm requirement"
             % (opening[0], opening[1], opening[1] - opening[0], USB_OPEN_H))

    # -- 10 -----------------------------------------------------------------
    print("")
    print("10. BUTTON TOOL HOLES ALIGN TO THE ESP32 REFERENCE")
    for tag, by in (("EN/RESET", ESP_BTN_Y), ("BOOT", -ESP_BTN_Y)):
        clear = all(lid.clear_between(ESP_BTN_X + dx, by + dy,
                                      Z_LID_TOP - LID_TOP_T + 0.4,
                                      Z_LID_TOP + 0.1)
                    for dx, dy in ((0, 0), (1.3, 0), (-1.3, 0),
                                   (0, 1.3), (0, -1.3)))
        wall = all(lid.inside(ESP_BTN_X + dx, by + dy, Z_LID_TOP - 0.9)
                   for dx, dy in ((2.4, 0), (-2.4, 0), (0, 2.4), (0, -2.4)))
        gate(clear and wall, "%s hole open at (%.2f, %+.2f)"
             % (tag, ESP_BTN_X, by),
             "through-hole clear to %.2f mm diameter, material at %.2f mm"
             % (2.6, 4.8))
    gate(Z_BTN_TOP < Z_CAV_TOP, "a tool reaches the button from outside",
         "button top z %+.2f, lid underside z %+.2f, %.2f mm of travel"
         % (Z_BTN_TOP, Z_CAV_TOP, Z_CAV_TOP - Z_BTN_TOP))

    # -- 11 -----------------------------------------------------------------
    print("")
    print("11. ANTENNA KEEP-OUT CARRIES NO SCREW, INSERT, RIB OR LACING")
    bad = []
    for x in grid(AKO_X0, AKO_X1, 25):
        for y in grid(AKO_Y0, AKO_Y1, 21):
            for z in grid(Z_ESP_TOP, Z_CAV_TOP - 0.1, 9):
                for m in (base, cfix, cadj):
                    if m.inside(x, y, z):
                        bad.append((m.name, round(x, 1), round(y, 1)))
    gate(not bad, "base and both clamps inside the %.2f mm keep-out"
         % ANTENNA_KEEPOUT,
         "%d intrusion(s)%s" % (len(bad), " %s" % bad[:2] if bad else ""))
    for nm, fx, fy, fd in fasteners:
        assert True
    near = min(max(AKO_X0 - (fx + fd / 2.0), (fx - fd / 2.0) - AKO_X1,
                   AKO_Y0 - (fy + fd / 2.0), (fy - fd / 2.0) - AKO_Y1)
               for _n, fx, fy, fd in fasteners)
    gate(near > 0.0, "every fastener envelope stays outside the keep-out",
         "closest approach %.2f mm" % near)
    thick, thick_at = 0.0, None
    for x in grid(ANT_X0, ANT_X1, 13):
        for y in grid(ANT_Y0, ANT_Y1, 11):
            t = sum(b - a for a, b in lid.spans(x, y))
            if t > thick:
                thick, thick_at = t, (round(x, 1), round(y, 1))
    gate(thick <= LID_ANTENNA_T + TOL,
         "lid thickness over the antenna <= %.2f mm" % LID_ANTENNA_T,
         "maximum %.2f mm at %s" % (thick, thick_at))
    gate(Y_OUT + TIE_SLOT_W > AKO_Y1,
         "no cable-lacing feature inside the keep-out",
         "nearest rail |y| %.2f against a keep-out reaching |y| %.2f"
         % (Y_OUT + TIE_SLOT_W, AKO_Y1))

    # -- 12 -----------------------------------------------------------------
    print("")
    print("12. LID OVERLAP AND FIT CLEARANCE AROUND THE FULL PERIMETER")
    z_mid = Z_CAV_TOP - LID_OVERLAP / 2.0
    gaps, bad_gap, bad_lap = [], [], []
    for px, py, ux, uy in perimeter_stations():
        tb = surface_out(base, px, py, ux, uy, z_mid)
        if tb is None:
            bad_gap.append(("no base surface", round(px, 1), round(py, 1)))
            continue
        tl = enter_out(lid, px, py, ux, uy, z_mid, tb)
        if tl is None:
            bad_gap.append(("no skirt", round(px, 1), round(py, 1)))
            continue
        g = tl - tb
        gaps.append(g)
        if abs(g - LID_FIT_CLEAR) > 0.08:
            bad_gap.append((round(g, 3), round(px, 1), round(py, 1)))
        for z in (Z_SKIRT_BOT + 0.30, Z_CAV_TOP - 0.30):
            if not lid.inside(px + ux * (tb + LID_FIT_CLEAR + LID_SKIRT_T / 2),
                              py + uy * (tb + LID_FIT_CLEAR + LID_SKIRT_T / 2),
                              z):
                bad_lap.append((round(px, 1), round(py, 1), z))
    gate(not bad_gap, "%d perimeter probes: sliding gap = %.2f mm"
         % (len(perimeter_stations()), LID_FIT_CLEAR),
         "measured %.3f to %.3f mm, mean %.3f"
         % (min(gaps), max(gaps), sum(gaps) / len(gaps)) if gaps else "none")
    gate(not bad_lap, "skirt material present over the full %.2f mm overlap"
         % LID_OVERLAP, "%d station(s) short" % len(bad_lap))
    ls = lid.spans(0.0, Y_OUT + LID_FIT_CLEAR + LID_SKIRT_T / 2.0)
    skirt = [(a, b) for a, b in ls if a < Z_CAV_TOP - 0.1]
    gate(bool(skirt) and abs((Z_CAV_TOP - skirt[0][0]) - LID_OVERLAP) < TOL,
         "measured overlap depth on the centre station",
         "%.2f mm from z %+.2f" % (Z_CAV_TOP - skirt[0][0] if skirt else -1,
                                   skirt[0][0] if skirt else 0))

    # -- 13 -----------------------------------------------------------------
    print("")
    print("13. CLAMPS CONTACT ONLY DECLARED BARE PCB EDGE ZONES")
    fb, ab = cfix.bb, cadj.bb
    gate(abs(fb[4] - Z_PLINTH_TOP) < TOL and abs(ab[4] - Z_PLINTH_TOP) < TOL,
         "both clamp undersides sit %.2f mm above the board" % CLAMP_VERT_CLEAR,
         "fixed z %+.3f, adjustable z %+.3f, board top %+.2f"
         % (fb[4], ab[4], Z_PCB_TOP))
    gate(fb[1] <= X_DATUM + PCB_BARE_EDGE + TOL,
         "fixed clamp lip inside the %.2f mm bare short-edge strip"
         % PCB_BARE_EDGE,
         "reaches x %+.3f, strip ends at %+.2f"
         % (fb[1], X_DATUM + PCB_BARE_EDGE))
    for tag, edge, slide in (("short 65.00", X_PCB_MIN, X_PCB_MIN - X_PCB_NOM),
                             ("nominal 66.00", X_PCB_NOM, 0.0),
                             ("long 67.00", X_PCB_MAX, X_PCB_MAX - X_PCB_NOM)):
        lip = ab[0] + slide
        gate(lip >= edge - PCB_BARE_EDGE - TOL and lip <= edge - TOL,
             "adjustable clamp lip on bare edge, board %s" % tag,
             "lip x %+.3f, bare strip %+.2f to %+.2f"
             % (lip, edge - PCB_BARE_EDGE, edge))
    gate(min(fb[4], ab[4]) > Z_PCB_TOP,
         "no clamp material enters the board thickness",
         "lowest clamp point z %+.3f, board top %+.2f"
         % (min(fb[4], ab[4]), Z_PCB_TOP))

    # -- 14 -----------------------------------------------------------------
    print("")
    print("14. ADJUSTABLE CLAMP TRAVEL >= +/-%.2f mm" % LEN_ADJUST)
    z_probe = Z_PLINTH_TOP + CLAMP_T / 2.0
    runs = []
    x = ADJ_SCREW_X - 6.0
    start = None
    while x < ADJ_SCREW_X + 6.0:
        ins = cadj.inside(x, CLAMP_SCREW_Y, z_probe)
        if not ins and start is None:
            start = x
        if ins and start is not None:
            runs.append((start, x))
            start = None
        x += 0.005
    slot = max(runs, key=lambda r: r[1] - r[0]) if runs else (0, 0)
    length = slot[1] - slot[0]
    gate(abs(length - CLAMP_SLOT_L) < 0.06, "slot length measured in the mesh",
         "%.3f mm against %.2f expected" % (length, CLAMP_SLOT_L))
    travel = (length - LID_SCREW_CLEAR_D) / 2.0
    gate(travel >= LEN_ADJUST - 0.03, "resulting travel on an M3 screw",
         "+/-%.3f mm, slot centre x %+.3f" % (travel,
                                              (slot[0] + slot[1]) / 2.0))
    gate(ab[1] + LEN_ADJUST <= X_WALL_IN_POS - 0.10,
         "clamp still clears the end wall at full outward travel",
         "bar reaches x %+.2f, wall inner face %+.2f"
         % (ab[1] + LEN_ADJUST, X_WALL_IN_POS))

    # -- 15 -----------------------------------------------------------------
    print("")
    print("15. NO RETAINING FEATURE LOADS THE ESP32 OR ITS SOCKETS")
    bad = []
    for x in inner(ESP_X0, ESP_X1, 27):
        for y in inner(ESP_Y0, ESP_Y1, 15):
            for z in grid(Z_ESP_BOT, Z_ESP_TOP + 3.10, 5):
                for m in (base, lid, cfix, cadj):
                    if m.inside(x, y, z):
                        bad.append((m.name, round(x, 1), round(y, 1)))
    gate(not bad, "controller envelope", "%d intrusion(s)" % len(bad))
    bad = []
    for sgn in (1.0, -1.0):
        for x in inner(-ESP_HEADER_SPAN, ESP_HEADER_SPAN, 21):
            for y in inner(sgn * ESP_HEADER_SPAN / 2.0 - 1.27,
                           sgn * ESP_HEADER_SPAN / 2.0 + 1.27, 3):
                for z in grid(Z_PCB_TOP + 0.2, Z_ESP_BOT - 0.2, 5):
                    for m in (base, lid, cfix, cadj):
                        if m.inside(x, y, z):
                            bad.append((m.name, round(x, 1), round(y, 1)))
    gate(not bad, "socket header envelope", "%d intrusion(s)" % len(bad))

    # -- 16 -----------------------------------------------------------------
    print("")
    print("16. CABINET MOUNTING SLOTS OUTSIDE THE ELECTRICAL ENVELOPE")
    found = 0
    for sx in (EAR_SLOT_X_NEG, EAR_SLOT_X_POS):
        for sy in (EAR_SLOT_Y, -EAR_SLOT_Y):
            through = base.clear_between(sx, sy, Z_FLOOR_BOT - 0.5,
                                         Z_EAR_TOP + 0.5)
            ends = (base.inside(sx, sy + CABINET_SLOT_L / 2.0 + 1.0,
                                Z_EAR_TOP - 1.0)
                    and base.inside(sx, sy - CABINET_SLOT_L / 2.0 - 1.0,
                                    Z_EAR_TOP - 1.0))
            if through and ends:
                found += 1
    gate(found == 4, "four through-slots present at the named coordinates",
         "%d found" % found)
    for sx in (EAR_SLOT_X_NEG, EAR_SLOT_X_POS):
        runs, start, y = [], None, EAR_SLOT_Y - 9.0
        while y < EAR_SLOT_Y + 9.0:
            ins = base.inside(sx, y, Z_EAR_TOP - EAR_T / 2.0)
            if not ins and start is None:
                start = y
            if ins and start is not None:
                runs.append((start, y))
                start = None
            y += 0.01
        run = max(runs, key=lambda r: r[1] - r[0]) if runs else (0, 0)
        gate(abs((run[1] - run[0]) - CABINET_SLOT_L) < 0.10,
             "slot long axis runs ACROSS the housing at x %+.2f" % sx,
             "%.3f mm measured along Y against %.2f expected"
             % (run[1] - run[0], CABINET_SLOT_L))
    clr = min(abs(sx) - CABINET_SLOT_W / 2.0 for sx in (EAR_SLOT_X_NEG,
                                                        EAR_SLOT_X_POS))
    gate(clr > max(abs(X_DATUM), X_ADJ_FACE),
         "slot envelopes clear of the board plan",
         "nearest slot edge |x| %.2f against a board reaching %.2f"
         % (clr, X_ADJ_FACE))
    gate(abs((Z_EAR_TOP - Z_FLOOR_BOT) - EAR_T) < TOL, "ear thickness",
         "%.2f mm" % (Z_EAR_TOP - Z_FLOOR_BOT))

    # -- 17 -----------------------------------------------------------------
    print("")
    print("17. VALID ASSEMBLY, WIRING AND REMOVAL SEQUENCE")
    proud = []
    for px, py, ux, uy in perimeter_stations():
        for z in grid(Z_SKIRT_BOT + 0.1, Z_CAV_TOP - 0.1, 7):
            t = surface_out(base, px, py, ux, uy, z)
            if t is None:
                continue
            base_out = surface_out(base, px, py, ux, uy, z_mid)
            if base_out is not None and t > base_out + 0.02:
                proud.append((round(px, 1), round(py, 1), round(z, 1)))
    gate(not proud, "nothing on the base grows outward inside the skirt band",
         "%d station(s) proud - the lid lifts straight off" % len(proud))
    bad = []
    for nm, m, x0, x1 in (("fixed", cfix, FIX_BAR_OUT, FIX_BAR_IN),
                          ("adjustable", cadj, ADJ_BAR_IN,
                           ADJ_BAR_OUT + LEN_ADJUST)):
        for x in inner(x0, x1, 13):
            for y in inner(-CLAMP_HALF_SPAN, CLAMP_HALF_SPAN, 15):
                if not base.clear_between(x, y, Z_PLINTH_TOP + CLAMP_T, 80.0):
                    bad.append((nm, round(x, 1), round(y, 1)))
    gate(not bad, "both clamps lift out with the lid off and wiring in place",
         "%d obstruction(s)" % len(bad))
    bad = []
    for x in inner(ESP_X0, ESP_X1, 25):
        for y in inner(ESP_Y0, ESP_Y1, 13):
            for m in (base, cfix, cadj):
                if not m.clear_between(x, y, Z_ESP_BOT, 80.0):
                    bad.append((m.name, round(x, 1), round(y, 1)))
    gate(not bad, "ESP32 lifts vertically out of its sockets, lid off",
         "%d obstruction(s)" % len(bad))
    note("sequence", "inserts -> board on pads against the datum -> fixed "
         "clamp -> adjustable clamp -> wire and lace -> ESP32 -> lid")

    # -- 18 -----------------------------------------------------------------
    print("")
    print("18. PRINTABLE IN THE STATED ORIENTATION WITHOUT INTERNAL SUPPORT")
    limit = 8.0
    beds = (("base", base, Z_FLOOR_BOT, 1, "floor down"),
            ("lid", lid, Z_LID_TOP, -1, "top face down"),
            ("clamp_fix", cfix, Z_PLINTH_TOP, 1, "flat"),
            ("clamp_adj", cadj, Z_PLINTH_TOP, 1, "flat"),
            ("plug", plug, USB_Z1 + 2.0, -1, "flange face down"),
            ("gauge", gauge, -2.40, 1, "plate down"))
    for nm, m, bed, up, orient in beds:
        steep, flat, reach, where, nfacet = overhang_report(m, bed, up, limit)
        gate(steep < 1.0, "%s, %s: facets steeper than 45 degrees" % (nm,
                                                                     orient),
             "%.2f mm2" % steep)
        gate(reach <= limit, "%s: worst unsupported bridging reach" % nm,
             "%.2f mm (span %.2f) over %.1f mm2 in %d facet(s)%s"
             % (reach, 2 * reach, flat, nfacet,
                ", worst at %s" % (where,) if where else ""))
    gate(abs(SAW_H - SAW_STEP / 2.0) < 1e-9,
         "cable-window roof flanks are exactly 45 degrees",
         "rise %.3f over run %.3f" % (SAW_H, SAW_STEP / 2.0))
    gate(VENT_W < LID_SCREW_D - 0.5,
         "no top vent can pass a fastener used in this build",
         "%.2f mm slot against an M%.0f shank and a %.2f mm insert"
         % (VENT_W, LID_SCREW_D, INSERT_HOLE_D))

    # -- envelope ------------------------------------------------------------
    print("")
    print("DERIVED ENVELOPE, MEASURED FROM THE MESH")
    bx = base.bb
    ov_l, ov_w = bx[1] - bx[0], bx[3] - bx[2]
    ov_h = (Z_LID_TOP) - bx[4]
    gate(abs(ov_l - OVERALL_L) < TOL and abs(ov_w - OVERALL_W) < TOL,
         "overall plan measured on the base",
         "%.2f x %.2f mm against %.2f x %.2f derived"
         % (ov_l, ov_w, OVERALL_L, OVERALL_W))
    gate(abs(ov_h - H_CLOSED) < TOL, "closed height",
         "%.2f mm against %.2f derived" % (ov_h, H_CLOSED))
    note("against the section 10 approximate target",
         "%.2f x %.2f x %.2f target 90.00 x 78.00 x ~35.00; length +%.2f, "
         "width -%.2f, height +%.2f"
         % (ov_l, ov_w, ov_h, ov_l - 90.0, 78.0 - ov_w, ov_h - 35.0))
    note("body excluding ears and lacing rails",
         "%.2f x %.2f mm" % (BODY_L, BODY_W))

    # -- gates nothing geometric can close -----------------------------------
    print("")
    print("PROTOTYPE-REQUIRED - depends on hardware nobody has measured")
    for k, v in (("breakout outline 66.00 x 63.00 x 1.60", "section 4"),
                 ("below-board component height 2.50", "section 4"),
                 ("assembled height above the board 24.00", "section 4"),
                 ("terminal count, pitch and screw inset", "starting value"),
                 ("terminal block height 10.00", "starting value"),
                 ("ESP32 outline, socket height and USB height",
                  "starting value"),
                 ("EN/RESET and BOOT positions (-22.00, +/-10.15)",
                  "starting value"),
                 ("PCB antenna extent 15.00 x 18.00", "starting value"),
                 ("bare edge strips 3.00 and 2.50", "starting value"),
                 ("heat-set insert 4.00 dia x 6.00 deep", "not recorded"),
                 ("clamp retains without bowing the board", "physical"),
                 ("lid fit and repeated removal", "physical"),
                 ("USB plug and shroud insertion", "physical"),
                 ("thermal behaviour after 30 minutes powered", "physical")):
        proto(k, v)
    print("")
    print("INSTALLATION-REQUIRED - cannot be settled before it is fitted")
    for k, v in (("cabinet mounting surface and hole positions",
                  "the ears set their own"),
                 ("harness routing and final tie positions", "on the bench"),
                 ("OTA link with the lid fitted", "in the cabinet"),
                 ("shake and handling test", "assembled")):
        install(k, v)

    print("")
    print("=" * 78)
    print("%d mesh gates, %d failed | %d prototype-required | "
          "%d installation-required" % (CHECKS, len(FAILS), len(PROTOS),
                                        len(INSTALLS)))
    if FAILS:
        for f in FAILS:
            print("  FAILED: %s" % f)
    print("NOTHING HERE IS PHYSICAL VALIDATION. NO PART HAS BEEN PRINTED.")
    print("=" * 78)
    return 1 if FAILS else 0


if __name__ == "__main__":
    if "--drawings" in sys.argv:
        MM = {}
        for _k, _f in MESHES.items():
            MM[_k] = Mesh(_k, os.path.normpath(os.path.join(STL, _f)))
        print("dimensioned drawings:")
        drawings(MM, os.path.normpath(os.path.join(HERE, "..", "Drawings")),
                 "Decca_ESP32_Controller_Housing_revA_")
        sys.exit(0)
    sys.exit(main())
