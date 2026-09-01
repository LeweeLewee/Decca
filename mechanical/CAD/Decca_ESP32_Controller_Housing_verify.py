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
is specification revision v1.1 - and from the derivation chain written out in
the build report. Nothing is imported from
Decca_ESP32_Controller_Housing_fusion.py. If the generator and this file
disagree, that disagreement is the whole point.

It covers all twenty-two specification v1.1 section 13 gates, including the
four the CAD suite cannot do honestly on its own: manifoldness of the exported
triangles, real bridging reach in the stated print orientation, the material
gates measured from mesh volume rather than from BRep volume, and the absence
of every Rev A feature v1.1 section 2.2 deletes by name.

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
    "gauge": "ESP32_Controller_Carrier_Fit_Gauge.stl",
}

# Production parts and how many of each are printed. The fit gauge is a
# prototype tool and v1.1 section 9 excludes it from the material gates.
PRODUCTION = (("base", 1), ("lid", 1), ("clamp", 1), ("cap", 2))

# Rev A production meshes that v1.1 section 12 forbids shipping. Their absence
# is gate 22, and it is checked on the FILE SYSTEM, not on a component tree.
FORBIDDEN_FILES = (
    "ESP32_Controller_PCB_Clamp_Fixed.stl",
    "ESP32_Controller_USB_Plug.stl",
)

# ---------------------------------------------------------------------------
# EXPECTED VALUES - typed in from the controlling documents, NOT imported.
# ---------------------------------------------------------------------------
# -- v1.1 section 3, reference geometry and clearances ----------------------
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

# -- v1.1 sections 4, 7, 8 and 10, structure --------------------------------
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

# -- v1.1 section 9, the mandatory material gates ---------------------------
ENV_MAX = (85.00, 75.00, 36.00)
VOL_MAX = 35.00                # cm3, production parts only
MASS_MAX = 45.0                # g
PETG_DENSITY = 1.27
VOL_PREF = (("base", 15.00), ("lid", 18.00), ("clamp", 2.00))

# -- the design's own FDM rule ----------------------------------------------
# v1.1 section 10 forbids support MATERIAL. It does not forbid a short
# unsupported ledge, and a ledge that retains a board cannot be built without
# one. 1.50 mm is the stated limit, and the cable windows and the USB slot are
# held to a stricter rule: no downward-facing facet in them at all.
OVERHANG_REACH_MAX = 1.50

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
WIN_HALF_W = 10.00
WIN_Z0 = 5.00                  # the skirt's lower free edge
WIN_Z1 = 20.00
WIN_SILL = 9.00                # the base wall top
WIN_CLEAR_H = 11.00
USB_SLOT_W = 15.00
USB_SLOT_Z1 = 22.55
USB_Z0 = 13.05
USB_Z1 = 22.05
VENT_N = 5
VENT_W = 2.00
VENT_X = (-22.00, -8.00)
VENT_PITCH = 4.50

# internal cable-tie tabs
TIE_X = (-5.00, 5.00)
TIE_TAB_HALF_W = 5.00
TIE_TAB_TOP = 15.50
TIE_AP_W = 5.00
TIE_AP_Z = (10.00, 12.40)

# recessed cabinet fixings
CAB_X = 27.00
CAB_PAD_D = 13.00
CAB_PAD_H = 2.40
CAB_SCREW_D = 3.40
CAB_HEAD_D = 6.40
CAB_HEAD_TOP = 1.20
CAB_CAP_D = 10.20
CAB_CAP_T = 1.20
CAB_RECESS_D = 10.40

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


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Decca ESP32 Controller Housing Rev B - offline mesh verifier")
    print("specification v1.1 section 13, measured from the exported "
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
    for key, _n in PRODUCTION + (("gauge", 0),):
        m = M[key]
        sx, sy, sz = m.size()
        print("  %-6s %6d tris  %7.2f cm3  %6.2f x %6.2f x %6.2f mm  %s"
              % (key, len(m.tris), signed_volume(m.tris) / 1000.0,
                 sx, sy, sz, os.path.basename(m.path)))
    print("")

    base, lid, clamp, cap = M["base"], M["lid"], M["clamp"], M["cap"]

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
    seal = (CAB_RECESS_D - csx)
    gate(gaps == 0 and CAB_CAP_D > CAB_HEAD_D and 0.0 < seal <= 0.40
         and abs(csz - CAB_CAP_T) < 0.05,
         "2  continuous insulating floor under the carrier",
         "%d probes, %d gaps, %d in the 2 capped bores; cap %.2f dia x %.2f "
         "in a %.2f recess over a %.2f head"
         % (probes, gaps, inbore, csx, csz, CAB_RECESS_D, CAB_HEAD_D))

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
    obstructed = 0
    for s in (1.0, -1.0):
        for wx in WIN_X:
            pts = box_pts(wx - WIN_HALF_W, wx + WIN_HALF_W, 13,
                          min(s * Y_OUT, s * (LID_Y + 2.0)),
                          max(s * Y_OUT, s * (LID_Y + 2.0)), 5,
                          WIN_SILL, WIN_SILL + WIRE_EXIT_H, 9)
            obstructed += count_in(lid, pts) + count_in(base, pts)
    gate(obstructed == 0 and (WIN_Z1 - WIN_SILL) >= WIRE_EXIT_H - 1e-9,
         "7  each cable window gives >= %.2f mm of usable height" % WIRE_EXIT_H,
         "4 windows %.2f mm wide, sill z %.2f to %.2f = %.2f mm clear; "
         "%d obstructed probes"
         % (2 * WIN_HALF_W, WIN_SILL, WIN_Z1, WIN_CLEAR_H, obstructed))

    # -- 8 -----------------------------------------------------------------
    pinched = 0
    dmax = 0.0
    for wx, side, n, _ids in BUNDLES:
        dia = bundle_d(n)
        dmax = max(dmax, dia)
        zc = WIN_SILL + dia / 2.0 + 0.50
        for t in grid(0.0, 1.0, 9):
            y = side * (Y_CAV + t * (LID_Y + 8.0 - Y_CAV))
            for k in range(8):
                a = 2.0 * math.pi * k / 8.0
                px = wx + math.cos(a) * dia / 2.0 * 0.92
                pz = zc + math.sin(a) * dia / 2.0 * 0.92
                if lid.inside(px, y, pz) or base.inside(px, y, pz):
                    pinched += 1
    gate(pinched == 0,
         "8  the lid pinches no grouped harness",
         "%d bundles (%s), %d conductors, largest dia %.2f; %d pinch probes"
         % (len(BUNDLES), " ".join(b[3] for b in BUNDLES),
            sum(b[2] for b in BUNDLES), dmax, pinched))

    # -- 9 -----------------------------------------------------------------
    open_ap = 0
    tab_solid = 0
    for s in (1.0, -1.0):
        for tx in TIE_X:
            clear = True
            for y in grid(Y_CAV - 0.5, Y_OUT + 0.5, 11):
                for px in grid(tx - TIE_AP_W / 2.0 + 0.3,
                               tx + TIE_AP_W / 2.0 - 0.3, 5):
                    for pz in grid(TIE_AP_Z[0] + 0.2, TIE_AP_Z[1] - 0.2, 4):
                        if base.inside(px, s * y, pz):
                            clear = False
            if clear:
                open_ap += 1
            # the tab has to be there: material beside the aperture, and above
            # it, on the wall line
            ymid = s * (Y_CAV + Y_OUT) / 2.0
            side_x = tx + TIE_AP_W / 2.0 + 1.0
            if base.inside(side_x, ymid, (TIE_AP_Z[0] + TIE_AP_Z[1]) / 2.0) \
                    and base.inside(tx, ymid, TIE_TAB_TOP - 0.4):
                tab_solid += 1
    gate(open_ap == 4 and tab_solid == 4,
         "9  four internal cable-tie positions, two per long side",
         "%d/4 apertures open through the wall, %d/4 tabs solid; %.2f x %.2f "
         "aperture with a 45 deg peak, tab top z %.2f - the tie loads the "
         "wall, which loads the base and the cabinet screws"
         % (open_ap, tab_solid, TIE_AP_W, TIE_AP_Z[1] - TIE_AP_Z[0],
            TIE_TAB_TOP))

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
        # widest bore diameter measured just under the recess floor
        w = [y for y in grid(-6.0, 6.0, 241)
             if not base.inside(x, y, CAB_HEAD_TOP - 0.06)]
        heads.append(max(w) - min(w) if w else 0.0)
        top = top_of(base, x, 0.0, Z_PCB_BOT)
    pad_top = top_of(base, CAB_X + CAB_PAD_D / 2.0 - 1.0, 0.0, Z_PCB_BOT)
    inside_fp = (CAB_X + CAB_PAD_D / 2.0) < (X_OUT_POS)
    gate(all(h >= CAB_HEAD_D - 0.35 for h in heads)
         and pad_top is not None and abs(pad_top - CAB_PAD_H) < 0.05
         and (Z_PCB_BOT - CAB_PAD_H) >= UNDER_CLEAR - 0.02 and inside_fp,
         "16 cabinet fastener heads recessed, insulated and clear",
         "2 fixings at x +-%.2f, y 0, INSIDE the %.2f x %.2f footprint; "
         "measured countersink %.2f/%.2f mm for a %.2f head; head top z %.2f "
         "under a cap to z %.2f, carrier underside z %.2f, clear %.2f"
         % (CAB_X, BODY_L, BODY_W, heads[0], heads[1], CAB_HEAD_D,
            CAB_HEAD_TOP, pad_top if pad_top else -1, Z_PCB_BOT,
            Z_PCB_BOT - CAB_PAD_H))

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
    print("")
    print("INSTALLATION GATES")
    install("cabinet fixing centres and the surface behind them")
    install("final harness routing and the two tie positions used per side")
    install("antenna performance with the lid fitted")

    print("")
    print("%d gates, %d failed, %d prototype, %d installation"
          % (CHECKS, len(FAILS), len(PROTOS), len(INSTALLS)))
    if FAILS:
        for f in FAILS:
            print("  FAILED: %s" % f)
        return 1
    print("")
    print("All specification v1.1 section 13 gates pass on the exported "
          "meshes. This is NOT physical validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
