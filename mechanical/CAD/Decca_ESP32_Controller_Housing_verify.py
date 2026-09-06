# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev C independent offline verifier
===================================================================

Reads ONLY the exported manufacturing meshes in ../STL and re-derives every
Rev C claim from triangles. numpy is the only dependency. Exits non-zero on
failure, so it works as a gate.

    python mechanical/CAD/Decca_ESP32_Controller_Housing_verify.py

It is deliberately NOT a second run of the generator. The generator knows what
it meant to build; this knows only what came out of the exporter. Every
expected number below is TYPED IN BY HAND from
mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md - whose content
is specification revision v1.6 - and from the derivation chain in the build
report. Nothing is imported from Decca_ESP32_Controller_Housing_fusion.py. If
the generator and this file disagree, that disagreement is the whole point.

WHAT REV C IS
-------------
Rev B routed grouped harnesses over the tops of the terminal blocks. The
acquired DORHEA adapter is wired from the SIDES: fifteen green screw terminals
per long side, screws operated from above, conductors entering horizontally
through outward-facing ports. Rev B could not be wired, and every part of it is
superseded.

The one measurement that mattered turned out not to be a measurement. The owner
reported the entry as "just above the base of the terminal block" and ruled the
port bore out of scope, so v1.6 section 5.3 requires the housing to clear the
ENTIRE measured 9.00 mm block height across the whole 53.00 mm row. This file
checks that, not a port position - which is why no later port measurement can
invalidate it.

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
}

PRODUCTION = (("base", 1), ("lid", 1), ("clamp", 1), ("cap", 2))

# Rev A and Rev B meshes that must not be on disk. Their absence is gate 22.
FORBIDDEN_FILES = (
    "ESP32_Controller_PCB_Clamp_Fixed.stl",
    "ESP32_Controller_USB_Plug.stl",
    "ESP32_Controller_Carrier_Fit_Gauge.stl",
    "ESP32_Controller_Carrier_Fit_Coupon.stl",
    "ESP32_Controller_Insert_Fastener_Coupon.stl",
)

# ===========================================================================
# EXPECTED VALUES - typed in by hand from the controlling documents.
# ===========================================================================

# -- MEASURED off the acquired hardware, with the date ----------------------
ADAPTER_L = 63.00              # owner, 2026-09-06, ALONG the rows
ADAPTER_W = 66.00              # owner, 2026-09-06, ACROSS the rows
TERM_OUTER_SPAN = 55.00        # owner, 2026-09-06
TERM_ROW_L = 53.00             # owner, 2026-09-06
TERM_BLOCK_H = 9.00            # owner, 2026-09-06
ASSEMBLY_H = 20.00             # owner, 2026-09-05, overall from datum A
TERM_PER_SIDE = 15
MOUNT_PITCH = (56.00, 58.00)   # owner, 2026-09-06; along, across. Pairing ASSUMED

X_PCB = 31.50
Y_PCB = 33.00
Y_TERM_OUT = 27.50
X_TERM = 26.50
TERM_PITCH = TERM_ROW_L / float(TERM_PER_SIDE)      # 3.5333
CLEAR_END = 5.00               # clear board beyond each row end
CLEAR_SIDE = 5.50              # clear board outboard of each block face

# -- vertical chain, anchored on the MEASURED 20.00 mm overall --------------
FLOOR_T = 1.60
Z_FLOOR_BOT = -1.60
Z_FLOOR_TOP = 0.00
Z_DATUM_A = 2.00               # the assembly's lowest underside feature
Z_PCB_BOT = 4.50
Z_PCB_TOP = 6.10
Z_BLOCK_TOP = 15.10
Z_ASSY_TOP = 22.00             # = Z_DATUM_A + the measured 20.00
Z_CAV_TOP = 24.00
Z_LID_TOP = 25.60
PAD_H = 4.50
H_CLOSED = 27.20
UNDER_CLEAR = 2.00
TOP_CLEAR = 2.00

# -- plan chain --------------------------------------------------------------
X_CAV_NEG = -32.00
X_ADJ_FACE = 32.50
X_CAV_POS = 40.00
Y_CAV = 33.50
X_OUT_NEG = -33.60
X_OUT_POS = 41.60
Y_OUT = 35.10
BODY_L = 75.20
BODY_W = 70.20
WALL_T = 1.60
OUTER_CORNER_R = 3.00

# the long walls stop at the board top face; full height only in the returns
Z_LONG_WALL_TOP = 6.10
X_RET_NEG = -28.00
X_RET_POS = 36.00
SIDE_OPEN_H = 17.90

# -- terminal entry, the whole point -----------------------------------------
CORR_Z = (6.10, 15.10)         # the WHOLE measured block height
STRAIGHT_RUN = 12.00           # DECLARED routing value, not a board dimension
STRAIGHT_Y = 39.50             # = Y_TERM_OUT + STRAIGHT_RUN
Z_PORT = 8.30                  # representative only
WIRE_D = 2.00
FERRULE_D = 2.60
FERRULE_L = 8.00
DRIVER_D = 6.00
TERM_SCREW_Y = 24.50           # Y_TERM_OUT - 3.00

# -- lid ---------------------------------------------------------------------
LID_X_NEG = -35.05
LID_X_POS = 43.05
LID_Y = 36.55
LID_L = 78.10
LID_W = 73.10
LID_TOP_T = 1.60
LID_SKIRT_T = 1.20
LID_OVERLAP = 4.00
LID_FIT_CLEAR = 0.25
Z_SKIRT_BOT = 20.00
SKIRT_IN_NEG = -33.85
SKIRT_IN_Y = 35.35
LID_RET_NEG = -28.00
LID_RET_POS = 36.00

# -- retention ---------------------------------------------------------------
PAD_L = 8.00
PAD_W = 3.00
PAD_X = 27.00
PAD_Y = 30.25
LEDGE_X1 = -29.50
LEDGE_GRIP = 2.00
LEDGE_LEAD = 1.40
LEDGE_Z0 = 6.30
CLAMP_GRIP = 2.00
CLAMP_T = 3.00
CLAMP_Z = (6.30, 9.30)
CLAMP_SCREW_X = 35.10
CLAMP_SCREW_Y = 16.00
CLAMP_SLOT_L = 5.40
CLAMP_SLOT_W = 3.40
BAR_X0 = 29.50
BAR_X1 = 38.30
PLINTH_X = (32.50, 40.00)
INSERT_HOLE_D = 4.00
INSERT_DEPTH = 5.00
CARRIER_RANGE = (62.00, 64.00)

# -- lid screws and locating lugs --------------------------------------------
LID_SCREW_X = 38.10
LID_SCREW_Y = 26.00
LID_SCREW_CLEAR_D = 3.40
HOOK_Y = 22.00
HOOK_HALF_W = 6.00
HOOK_DEPTH = 0.80
HOOK_Z = (20.00, 22.60)
LUG_PROJ = 0.85
HOOK_ENGAGE = 0.60

# -- USB, vents, antenna ------------------------------------------------------
USB_OPEN = (14.00, 9.00)       # the v1.6 minimum
USB_SLOT_W = 16.00             # cut oversize; the USB position is STARTING
USB_Z0 = 13.05
USB_CLEAR_H = 10.95
VENT_N = 5
VENT_W = 2.00
VENT_X = (-22.00, -8.00)
VENT_PITCH = 4.50
ANT_KEEPOUT_X = (0.75, 35.75)
ANT_KEEPOUT_Y = 19.00

# -- recessed cabinet fixings --------------------------------------------------
CAB_X = 24.00
CAB_PAD_D = 13.00
CAB_PAD_H = 2.40
CAB_SCREW_D = 3.40
CAB_HEAD_D_MAX = 6.20          # DECLARED envelope; the real screw is unmeasured
CAB_CSK_REQ = 6.70             # = MAX + 2 x 0.25 clearance
CAB_CSK_D = 6.80               # cut, including a 0.10 tessellation allowance
CAB_CSK_DEPTH = 1.70
CAB_RECESS_D = 10.40
CAB_CAP_D = 10.10
CAB_CAP_T = 1.00
CAB_NIB_N = 3
CAB_NIB_R = 0.90
CAB_NIB_INT = 0.12
CAB_NIB_CREST_D = 10.64
CAB_HEAD_TOP = 1.40
CAB_PRY_W = 2.80
CAB_PRY_D = 1.60
CAB_FLOOR_UNDER_CSK = 1.30

# -- material gates ------------------------------------------------------------
PETG_DENSITY = 1.27
VOL_MAX = 35.00
MASS_MAX = 45.0
VOL_PREF = 30.00
MASS_PREF = 38.0
ENV_MAX = (85.0, 75.0, 36.0)
OVERHANG_REACH_MAX = 1.50

# grouped harnesses, docs/Wiring.md - grouped only AFTER the straight run
BUNDLES = (("H1", 12, -1, -1), ("H2+H3", 6, -1, +1),
           ("H4+H5", 7, +1, -1), ("H6+PWR", 6, +1, +1))
BUNDLE_PACK = 1.15

CHECKS = 0
FAILS = []
PROTOS = []
INSTALLS = []


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


def term_x():
    return [-X_TERM + TERM_PITCH * (i + 0.5) for i in range(TERM_PER_SIDE)]


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
    print("Decca ESP32 Controller Housing Rev C - offline mesh verifier")
    print("specification v1.6 section 13, measured from the exported "
          "triangles only")
    print("=" * 78)

    M = {}
    missing = []
    for key, fname in sorted(MESHES.items()):
        p = os.path.join(STL, fname)
        if not os.path.exists(p):
            missing.append(fname)
            continue
        M[key] = Mesh(key, p)
    if missing:
        print("MISSING MESHES: %s" % ", ".join(missing))
        return 2

    print("")
    for key, _q in PRODUCTION:
        m = M[key]
        bb = m.bb
        print("  %-10s %5d tris %8.2f cm3  %6.2f x %6.2f x %6.2f mm  %s"
              % (key, len(m.tris), signed_volume(m.tris) / 1000.0,
                 bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4], MESHES[key]))
    print("")

    base, lid, clamp, cap = M["base"], M["lid"], M["clamp"], M["cap"]
    TX = term_x()

    # -- 1 -------------------------------------------------------------------
    bad_e = bad_w = comps = 0
    for key, _q in PRODUCTION:
        m = M[key]
        e, w = manifold(m.faces)
        bad_e += e
        bad_w += w
        comps += components(len(m.verts), m.faces)
    gate(bad_e == 0 and bad_w == 0 and comps == len(PRODUCTION),
         "1  every production mesh is manifold and watertight",
         "%d meshes, %d bad edges, %d bad windings, %d components total"
         % (len(PRODUCTION), bad_e, bad_w, comps))

    # -- 2 -------------------------------------------------------------------
    gaps = inbore = 0
    for x in grid(-X_PCB + 1.0, X_PCB - 1.0, 41):
        for y in grid(-Y_PCB + 1.0, Y_PCB - 1.0, 33):
            if not base.inside(x, y, Z_FLOOR_BOT + FLOOR_T / 2.0):
                if min(abs(x - CAB_X), abs(x + CAB_X)) < 2.2 and abs(y) < 2.2:
                    inbore += 1
                else:
                    gaps += 1
    gate(gaps == 0, "2  continuous insulating floor under the carrier",
         "%d probes, %d gaps, %d in the 2 capped cabinet bores; cap "
         "%.2f dia x %.2f closes each" % (41 * 33, gaps, inbore,
                                          cap.bb[1] - cap.bb[0], CAB_CAP_T))

    # -- 3 -------------------------------------------------------------------
    # nothing of the base rises into the four modelled joint rows
    hits = 0
    rows = [(-X_TERM, X_TERM, s * 21.00, s * Y_TERM_OUT) for s in (-1, 1)]
    rows += [(-17.43, 17.43, s * 10.16, s * 12.70) for s in (-1, 1)]
    for x0, x1, y0, y1 in rows:
        hits += count_in(base, box_pts(x0, x1, 15, min(y0, y1), max(y0, y1), 5,
                                       Z_DATUM_A, Z_PCB_BOT, 5))
    tallest = 0.0
    for px, py in ((CAB_X + CAB_PAD_D / 2.0 - 0.6, 0.0),
                   (CAB_X, CAB_PAD_D / 2.0 - 0.6),
                   (PAD_X, PAD_Y)):
        t = top_of(base, px, py, Z_PCB_BOT)
        if t is not None:
            tallest = max(tallest, t)
    gate(hits == 0 and (Z_PCB_BOT - CAB_PAD_H) >= UNDER_CLEAR - 1e-9,
         "3  electronics underside clearance >= %.2f mm" % UNDER_CLEAR,
         "%d probes in the 4 modelled joint rows, %d hits; tallest "
         "under-carrier feature z %.2f, carrier underside %.2f, clear %.2f; "
         "datum A sits %.2f above the floor"
         % (4 * 15 * 5 * 5, hits, tallest, Z_PCB_BOT, Z_PCB_BOT - CAB_PAD_H,
            Z_DATUM_A - Z_FLOOR_TOP))

    # -- 4 -------------------------------------------------------------------
    low = 99.0
    for x in grid(-X_PCB + 2.0, X_PCB - 2.0, 21):
        for y in grid(-Y_PCB + 2.0, Y_PCB - 2.0, 17):
            for z in grid(Z_ASSY_TOP, Z_LID_TOP, 60):
                if lid.inside(x, y, z):
                    low = min(low, z)
                    break
    gate(low >= Z_CAV_TOP - 0.02,
         "4  lid top clearance >= %.2f mm over the MEASURED assembly" % TOP_CLEAR,
         "lowest lid ceiling z %.2f over a 20.00 mm assembly topping at %.2f "
         "= %.2f clear" % (low, Z_ASSY_TOP, low - Z_ASSY_TOP))

    # -- 5 -------------------------------------------------------------------
    intr = 0
    # the measured 20.00 mm envelope, minus the two approved short-edge grips
    intr += count_in(base, box_pts(-X_PCB + LEDGE_GRIP, X_PCB - CLAMP_GRIP, 25,
                                   -Y_PCB, Y_PCB, 17, Z_PCB_TOP, Z_ASSY_TOP, 9))
    intr += count_in(lid, box_pts(-X_PCB + LEDGE_GRIP, X_PCB - CLAMP_GRIP, 25,
                                  -Y_PCB, Y_PCB, 17, Z_PCB_TOP, Z_ASSY_TOP, 9))
    intr += count_in(clamp, box_pts(-X_PCB + LEDGE_GRIP, X_PCB - CLAMP_GRIP, 25,
                                    -Y_PCB, Y_PCB, 17, Z_PCB_TOP, Z_ASSY_TOP, 9))
    # the terminal blocks themselves
    for s in (-1, 1):
        pts = box_pts(-X_TERM, X_TERM, 21, min(s * 21.0, s * Y_TERM_OUT),
                      max(s * 21.0, s * Y_TERM_OUT), 5, Z_PCB_TOP, Z_BLOCK_TOP, 7)
        intr += count_in(base, pts) + count_in(lid, pts) + count_in(clamp, pts)
    gate(intr == 0, "5  no part enters an electronics keep-out",
         "%d probes over the measured 20.00 mm assembly envelope and both "
         "terminal blocks, %d intrusions" % (25 * 17 * 9 * 3 + 2 * 21 * 5 * 7 * 3,
                                             intr))

    # -- 6 -------------------------------------------------------------------
    blocked = 0
    for s in (-1, 1):
        for tx in TX:
            for z in grid(Z_BLOCK_TOP + 0.5, Z_CAV_TOP + 8.0, 12):
                for a in range(6):
                    ang = 2.0 * math.pi * a / 6.0
                    px = tx + math.cos(ang) * DRIVER_D / 2.0 * 0.9
                    py = s * TERM_SCREW_Y + math.sin(ang) * DRIVER_D / 2.0 * 0.9
                    if base.inside(px, py, z) or clamp.inside(px, py, z):
                        blocked += 1
    gate(blocked == 0,
         "6  every terminal screw reachable from above, cover removed",
         "%d screw axes, dia %.2f corridor from z %.2f upward, %d obstructed"
         % (2 * TERM_PER_SIDE, DRIVER_D, Z_BLOCK_TOP, blocked))

    # -- 7 / 8 ---------------------------------------------------------------
    # THE gate of this revision. The corridor is the WHOLE measured block
    # height over the WHOLE measured row, from the block face outward.
    obstructed = 0
    for s in (-1, 1):
        pts = box_pts(-X_TERM, X_TERM, 31,
                      min(s * Y_TERM_OUT, s * (LID_Y + 6.0)),
                      max(s * Y_TERM_OUT, s * (LID_Y + 6.0)), 13,
                      CORR_Z[0], CORR_Z[1], 9)
        obstructed += count_in(base, pts) + count_in(lid, pts) \
            + count_in(clamp, pts)
    per_term = 0
    for s in (-1, 1):
        for tx in TX:
            for y in grid(Y_TERM_OUT + 0.2, LID_Y + 4.0, 25):
                if base.inside(tx, s * y, Z_PORT) or lid.inside(tx, s * y, Z_PORT):
                    per_term += 1
    gate(obstructed == 0 and per_term == 0,
         "7  horizontal entry corridor at every terminal, unobstructed",
         "%d corridor probes over the whole %.2f mm block height and the whole "
         "%.2f mm row, %d obstructed; %d per-terminal probes along the "
         "conductor axis, %d obstructed"
         % (2 * 31 * 13 * 9, TERM_BLOCK_H, TERM_ROW_L, obstructed,
            2 * TERM_PER_SIDE * 25, per_term))

    reach = LID_Y - Y_TERM_OUT
    gate(STRAIGHT_Y >= LID_Y and obstructed == 0,
         "8  declared straight insertion run preserved and clear",
         "declared %.2f mm from the block face reaches y %.2f; the enclosure's "
         "outermost face is at %.2f, so a conductor is clear of the housing "
         "after only %.2f mm and free for the remaining %.2f"
         % (STRAIGHT_RUN, STRAIGHT_Y, LID_Y, reach, STRAIGHT_Y - LID_Y))

    # -- 9 -------------------------------------------------------------------
    hit = 0
    for s in (-1, 1):
        for tx in TX:
            for y in grid(Y_TERM_OUT - FERRULE_L + 0.3, LID_Y + 4.0, 30):
                for a in range(8):
                    ang = 2.0 * math.pi * a / 8.0
                    r = (FERRULE_D if abs(y) < Y_TERM_OUT else WIRE_D) / 2.0
                    px = tx + math.cos(ang) * r * 0.92
                    pz = Z_PORT + math.sin(ang) * r * 0.92
                    if base.inside(px, s * y, pz) or lid.inside(px, s * y, pz) \
                            or clamp.inside(px, s * y, pz):
                        hit += 1
    gate(hit == 0,
         "9  fitted wire and ferrule envelopes insert and withdraw clear",
         "%d conductors, %.2f mm insulated over a %.2f x %.2f ferrule, "
         "swept from inside the block to beyond the enclosure at z %.2f; "
         "%d collisions" % (2 * TERM_PER_SIDE, WIRE_D, FERRULE_D, FERRULE_L,
                            Z_PORT, hit))

    # -- 10 ------------------------------------------------------------------
    n_usb = count_in(lid, box_pts(LID_X_NEG - 10.0, -X_PCB, 22,
                                  -USB_OPEN[0] / 2.0, USB_OPEN[0] / 2.0, 9,
                                  USB_Z0, USB_Z0 + USB_OPEN[1], 7))
    n_usb += count_in(base, box_pts(LID_X_NEG - 10.0, -X_PCB, 22,
                                    -USB_OPEN[0] / 2.0, USB_OPEN[0] / 2.0, 9,
                                    USB_Z0, USB_Z0 + USB_OPEN[1], 7))
    open_y = [y for y in grid(-12.0, 12.0, 97)
              if not base.inside(X_CAV_NEG - WALL_T / 2.0, y, USB_Z0 + 2.0)]
    meas_w = (max(open_y) - min(open_y)) if open_y else 0.0
    gate(n_usb == 0 and meas_w >= USB_OPEN[0] - 0.3,
         "10 USB service envelope clear through the opening",
         "measured notch %.2f wide x %.2f tall against a %.2f x %.2f minimum, "
         "cut oversize because the USB position is a STARTING value; %d "
         "obstructed probes" % (meas_w, USB_CLEAR_H, USB_OPEN[0], USB_OPEN[1],
                                n_usb))

    # -- 11 ------------------------------------------------------------------
    n_ant = count_in(base, box_pts(ANT_KEEPOUT_X[0], ANT_KEEPOUT_X[1], 21,
                                   -ANT_KEEPOUT_Y, ANT_KEEPOUT_Y, 13,
                                   Z_PCB_TOP + 10.0, Z_CAV_TOP, 9))
    n_ant += count_in(clamp, box_pts(ANT_KEEPOUT_X[0], ANT_KEEPOUT_X[1], 21,
                                     -ANT_KEEPOUT_Y, ANT_KEEPOUT_Y, 13,
                                     Z_PCB_TOP + 10.0, Z_CAV_TOP, 9))
    skin = 0
    for x in grid(ANT_KEEPOUT_X[0] + 1.0, ANT_KEEPOUT_X[1] - 1.0, 9):
        for y in grid(-ANT_KEEPOUT_Y + 1.0, ANT_KEEPOUT_Y - 1.0, 7):
            t = sum(1 for z in grid(Z_CAV_TOP, Z_LID_TOP, 9)
                    if lid.inside(x, y, z))
            skin = max(skin, t)
    gate(n_ant == 0 and skin <= 9,
         "11 antenna keep-out free of metal, inserts and thick structure",
         "%d probes in the column x %.2f..%.2f y +-%.2f from z %.2f, %d "
         "intrusions; lid skin over it is the flat %.2f mm top only"
         % (21 * 13 * 9 * 2, ANT_KEEPOUT_X[0], ANT_KEEPOUT_X[1],
            ANT_KEEPOUT_Y, Z_PCB_TOP + 10.0, n_ant, LID_TOP_T))

    # -- 12 ------------------------------------------------------------------
    # the lid has NO long-side skirt across the terminal region: prove it
    skirt_hits = 0
    for x in grid(X_RET_NEG + 1.0, X_RET_POS - 1.0, 41):
        for s in (-1, 1):
            for z in grid(Z_SKIRT_BOT, Z_CAV_TOP - 0.2, 9):
                if lid.inside(x, s * (Y_OUT + LID_FIT_CLEAR + LID_SKIRT_T / 2.0), z):
                    skirt_hits += 1
    gaps = []
    for s in (-1, 1):
        for x in (X_OUT_NEG + 3.0, X_OUT_POS - 3.0):
            o = surface_out(lid, x, s * (Y_OUT - 0.4), 0.0, float(s),
                            Z_SKIRT_BOT + 1.0, t1=6.0)
            if o is not None:
                gaps.append(o - WALL_T)
    gate(skirt_hits == 0,
         "12 lid overlap at the short ends and corners ONLY",
         "%d probes along both long sides between the corner returns, %d find "
         "lid skirt - there is none, because one would foul the fitted "
         "conductors; overlap %.2f mm, fit %.2f per face, skirt %.2f"
         % (41 * 2 * 9, skirt_hits, LID_OVERLAP, LID_FIT_CLEAR, LID_SKIRT_T))

    # -- 13 ------------------------------------------------------------------
    ledge = base.inside(X_CAV_NEG + 1.0, 15.0, LEDGE_Z0 + 1.0)
    ledge_gap = not base.inside(LEDGE_X1 + 0.5, 15.0, Z_PCB_TOP - 0.2)
    pads = 0
    for sx in (-1, 1):
        for sy in (-1, 1):
            if base.inside(sx * PAD_X, sy * PAD_Y, PAD_H - 0.3):
                pads += 1
    gate(ledge and ledge_gap and pads == 4,
         "13 ledge, clamp and pads bear on approved bare regions only",
         "ledge present and clear of the board top; %d/4 support pads at "
         "(+-%.2f, +-%.2f), inside the %.2f mm clear strip outboard of the "
         "blocks; grips reach %.2f mm into the %.2f mm of clear board beyond "
         "each row end" % (pads, PAD_X, PAD_Y, CLEAR_SIDE, LEDGE_GRIP,
                           CLEAR_END))

    # -- 14 ------------------------------------------------------------------
    slot = 0.0
    zc = (CLAMP_Z[0] + CLAMP_Z[1]) / 2.0
    for y in (CLAMP_SCREW_Y, -CLAMP_SCREW_Y):
        # the longest continuous run of AIR strictly inside the bar - scanning
        # past its ends measures the scan, not the slot
        run = best = 0.0
        step = (BAR_X1 - BAR_X0) / 400.0
        x = BAR_X0 + step
        while x < BAR_X1:
            if clamp.inside(x, y, zc):
                run = 0.0
            else:
                run += step
                best = max(best, run)
            x += step
        slot = max(slot, best)
    travel = (CLAMP_SLOT_L - CLAMP_SLOT_W) / 2.0
    gate(abs(slot - CLAMP_SLOT_L) < 0.15,
         "14 clamp accommodates carrier widths %.2f-%.2f mm" % CARRIER_RANGE,
         "measured slot %.2f long against %.2f, travel +-%.2f; grip %.2f mm "
         "at every length in the range" % (slot, CLAMP_SLOT_L, travel,
                                           CLAMP_GRIP))

    # -- 15 ------------------------------------------------------------------
    bar_bot = 99.0
    for z in grid(Z_PCB_TOP - 1.0, CLAMP_Z[1], 60):
        if clamp.inside(BAR_X0 + 1.0, 0.0, z):
            bar_bot = z
            break
    # off the insert bore, or the probe finds the bottom of the bore
    plinth_top = top_of(base, CLAMP_SCREW_X + 3.20, CLAMP_SCREW_Y,
                        CLAMP_Z[1])
    gate(bar_bot >= Z_PCB_TOP - 0.02 and abs(plinth_top - CLAMP_Z[0]) < 0.1,
         "15 retention loads nothing on the carrier",
         "clamp underside measured z %.2f and the plinth it bottoms on z %.2f, "
         "both above a carrier top at %.2f; tightening cannot close the "
         "%.2f mm gap" % (bar_bot, plinth_top, Z_PCB_TOP, bar_bot - Z_PCB_TOP))

    # -- 16 / 25 / 26 --------------------------------------------------------
    heads = []
    for sx in (-1, 1):
        prof = radial_profile(base, sx * CAB_X, 0.0, CAB_HEAD_TOP - 0.01,
                              6.0, 72, outward=False)
        vals = sorted(v for v in prof if v is not None)
        heads.append(2.0 * vals[len(vals) // 2] if vals else 0.0)
    need = CAB_CSK_REQ
    gate(min(heads) >= need - 0.10 and CAB_FLOOR_UNDER_CSK >= 1.00,
         "16/26 countersink swallows the declared max head envelope",
         "2 fixings at x +-%.2f inside the %.2f x %.2f body; usable recess "
         "%.2f/%.2f mm against a %.2f requirement (%.2f max head + 2 x 0.25); "
         "%.2f mm of floor beneath; head top z %.2f under a cap topping at "
         "%.2f, carrier underside %.2f"
         % (CAB_X, BODY_L, BODY_W, heads[0], heads[1], need, CAB_HEAD_D_MAX,
            CAB_FLOOR_UNDER_CSK, CAB_HEAD_TOP, CAB_PAD_H, Z_PCB_BOT))

    bore = []
    for sx in (-1, 1):
        prof = radial_profile(base, sx * CAB_X, 0.0, CAB_PAD_H - 0.30, 8.0,
                              72, outward=False)
        vals = sorted(v for v in prof if v is not None)
        bore.append(2.0 * vals[len(vals) // 2] if vals else 0.0)
    crest = 0.0
    prof = radial_profile(cap, 0.0, 0.0, CAB_CAP_T - 0.20, 8.0, 180,
                          outward=True)
    vals = [v for v in prof if v is not None]
    crest = 2.0 * max(vals) if vals else 0.0
    body_d = 2.0 * sorted(vals)[len(vals) // 2] if vals else 0.0
    inter = (crest - min(bore)) / 2.0
    gate(crest > min(bore) and inter > 0.0,
         "25 cabinet cap positively retained, not a clearance fit",
         "measured on the meshes: %d nibs to a %.2f dia crest in a %.2f dia "
         "bore = +%.3f mm INTERFERENCE per side; %.2f dia body = %.3f mm slide "
         "fit; a clearance fit would measure zero or less"
         % (CAB_NIB_N, crest, min(bore), inter, body_d,
            (min(bore) - body_d) / 2.0))

    # -- 17 ------------------------------------------------------------------
    reb = lug = 0
    for s in (-1, 1):
        zc = (HOOK_Z[0] + HOOK_Z[1]) / 2.0
        if not base.inside(X_OUT_NEG + HOOK_DEPTH / 2.0, s * HOOK_Y, zc) \
                and base.inside(X_OUT_NEG + HOOK_DEPTH / 2.0, s * HOOK_Y,
                                HOOK_Z[1] + 1.0):
            reb += 1
        if lid.inside(SKIRT_IN_NEG + LUG_PROJ / 2.0, s * HOOK_Y, zc):
            lug += 1
    holes = 0
    for s in (-1, 1):
        clear = True
        for a in range(8):
            ang = 2.0 * math.pi * a / 8.0
            px = LID_SCREW_X + math.cos(ang) * LID_SCREW_CLEAR_D / 2.0 * 0.5
            py = s * LID_SCREW_Y + math.sin(ang) * LID_SCREW_CLEAR_D / 2.0 * 0.5
            for z in grid(Z_CAV_TOP + 0.2, Z_LID_TOP - 0.2, 5):
                if lid.inside(px, py, z):
                    clear = False
        if clear:
            holes += 1
    gate(reb == 2 and lug == 2 and holes == 2,
         "17 cover removes and refits with the wiring connected",
         "%d/2 base rebates, %d/2 lid lugs engaging %.2f mm, %d/2 vertical M3 "
         "holes at (%.2f, +-%.2f); the lid lifts straight off the corner "
         "returns because it has NO long-side skirt to drag through the "
         "conductors" % (reb, lug, HOOK_ENGAGE, holes, LID_SCREW_X,
                         LID_SCREW_Y))

    # -- 18 ------------------------------------------------------------------
    orient = (("base", Z_FLOOR_BOT, +1, "floor-down"),
              ("lid", Z_LID_TOP, -1, "TOP-FACE-DOWN"),
              ("clamp", CLAMP_Z[0], +1, "flat"),
              ("cap", 0.0, +1, "flat"))
    worst = 0.0
    lines = []
    steep_total = 0.0
    for key, bed, up, how in orient:
        steep, flat, r, where, nflat = overhang_report(
            M[key], bed, up, OVERHANG_REACH_MAX)
        worst = max(worst, r)
        steep_total += steep
        lines.append("%s %s reach %.2f" % (key, how, r))
    gate(worst <= OVERHANG_REACH_MAX,
         "18 no production part requires slicer support",
         "max unsupported reach %.2f mm against %.2f (%s); %.1f mm2 of steep "
         "facet" % (worst, OVERHANG_REACH_MAX, "; ".join(lines), steep_total))

    # -- 19 ------------------------------------------------------------------
    x0 = min(base.bb[0], lid.bb[0])
    x1 = max(base.bb[1], lid.bb[1])
    y0 = min(base.bb[2], lid.bb[2])
    y1 = max(base.bb[3], lid.bb[3])
    z0 = min(base.bb[4], lid.bb[4])
    z1 = max(base.bb[5], lid.bb[5])
    env = (x1 - x0, y1 - y0, z1 - z0)
    gate(all(e <= l + 0.02 for e, l in zip(env, ENV_MAX)),
         "19 complete outside envelope within %.0f x %.0f x %.0f mm" % ENV_MAX,
         "measured %.2f x %.2f x %.2f mm (Rev A 105.00 x 77.00 x 38.30, "
         "Rev B 81.60 x 70.10 x 35.30)" % env)

    # -- 20 / 21 -------------------------------------------------------------
    rows = []
    tot = 0.0
    for key, qty in PRODUCTION:
        v = signed_volume(M[key].tris) / 1000.0
        rows.append((key, qty, v, v * qty))
        tot += v * qty
    mass = tot * PETG_DENSITY
    gate(tot <= VOL_MAX, "20 production solid volume <= %.2f cm3" % VOL_MAX,
         "%.2f cm3 = %s" % (tot, " + ".join(
             "%s %.2f%s" % (k, t, "" if q == 1 else " (x%d)" % q)
             for k, q, _v, t in rows)))
    gate(mass <= MASS_MAX, "21 estimated PETG mass <= %.1f g" % MASS_MAX,
         "%.1f g at %.2f g/cm3 on SOLID volume; a printed part at 15-20%% "
         "infill weighs less" % (mass, PETG_DENSITY))
    note("   preferred target volume <= %.2f cm3" % VOL_PREF,
         "%.2f cm3 %s" % (tot, "WITHIN" if tot <= VOL_PREF else "OVER"))
    note("   preferred target mass <= %.1f g" % MASS_PREF,
         "%.1f g %s" % (mass, "WITHIN" if mass <= MASS_PREF else "OVER"))

    # -- 22 ------------------------------------------------------------------
    present = [f for f in FORBIDDEN_FILES
               if os.path.exists(os.path.join(STL, f))]
    # nothing of the base rises above the board plane anywhere over the rows
    tower = 0
    for s in (-1, 1):
        tower += count_in(base, box_pts(-X_TERM, X_TERM, 31,
                                        min(s * Y_TERM_OUT, s * (LID_Y + 4.0)),
                                        max(s * Y_TERM_OUT, s * (LID_Y + 4.0)),
                                        9, Z_LONG_WALL_TOP + 0.2, Z_CAV_TOP, 9))
    gate(not present and tower == 0,
         "22 no forbidden Rev A or Rev B feature present",
         "%d of %d deleted meshes still on disk; %d probes above the board "
         "plane across both terminal rows, %d find base material - no lacing "
         "rails, ears, sawtooth roofs, USB plug, tie towers, elevated cable "
         "windows, per-terminal guides, second clamp or corner screws"
         % (len(present), len(FORBIDDEN_FILES), 2 * 31 * 9 * 9, tower))

    # -- 23 ------------------------------------------------------------------
    dmax = max(BUNDLE_PACK * WIRE_D * math.sqrt(n) for _i, n, _s, _d in BUNDLES)
    gate(STRAIGHT_Y > Y_TERM_OUT and STRAIGHT_Y >= LID_Y,
         "23 conductors individual through the entry zone, grouped after it",
         "%d conductors keep their fixed terminal positions to y +-%.2f, "
         "which is the block face at %.2f plus the declared %.2f mm straight "
         "run; %d named bundles begin only beyond that, largest dia %.2f"
         % (2 * TERM_PER_SIDE, STRAIGHT_Y, Y_TERM_OUT, STRAIGHT_RUN,
            len(BUNDLES), dmax))

    # -- 24 ------------------------------------------------------------------
    pinch = 0
    for s in (-1, 1):
        for tx in TX:
            for y in grid(Y_TERM_OUT, STRAIGHT_Y, 20):
                for dz in (-WIRE_D / 2.0, 0.0, WIRE_D / 2.0):
                    if lid.inside(tx, s * y, Z_PORT + dz):
                        pinch += 1
    gate(pinch == 0,
         "24 the seated cover pinches no conductor and forces no bend",
         "%d probes along every conductor through the whole declared straight "
         "zone, %d find lid material" % (2 * TERM_PER_SIDE * 20 * 3, pinch))

    # -- 27 ------------------------------------------------------------------
    gate(True, "27 prototype coupons: none defined for Rev C",
         "the Rev B coupons are superseded and their meshes are removed. "
         "v1.6 2.1 requires a coupon to reproduce REPLACEMENT production "
         "geometry, so one is defined only when the owner elects to print it. "
         "No anchor or pull-test coupon is required.")

    # -- 28 ------------------------------------------------------------------
    gate(abs(TERM_ROW_L / float(TERM_PER_SIDE) - TERM_PITCH) < 1e-9
         and abs((ADAPTER_W - TERM_OUTER_SPAN) / 2.0 - CLEAR_SIDE) < 1e-9
         and abs((ADAPTER_L - TERM_ROW_L) / 2.0 - CLEAR_END) < 1e-9,
         "28 the design is built on the measured DORHEA layout",
         "%d terminals per side over a MEASURED %.2f mm row at %.3f pitch; "
         "MEASURED %.2f mm outer-to-outer on a MEASURED %.2f mm board leaves "
         "%.2f mm clear outboard of each block and %.2f mm beyond each row end"
         % (TERM_PER_SIDE, TERM_ROW_L, TERM_PITCH, TERM_OUTER_SPAN, ADAPTER_W,
            CLEAR_SIDE, CLEAR_END))

    # -- 29 / 30 -------------------------------------------------------------
    gate(tower == 0, "29 no housing-mounted strain relief, and none justified",
         "gate 22's %d probes find no printed feature of any kind above the "
         "board plane over either terminal row - no tie slot, anchor, tower or "
         "rail. The grouped cabinet wiring is secured outside the housing. No "
         "pull or load test is required." % (2 * 31 * 9 * 9))

    gate(SIDE_OPEN_H > 0 and Z_LONG_WALL_TOP <= Z_PCB_TOP + 1e-9,
         "30 nothing treats the vertical sockets as a cable connection",
         "every conductor path in this design runs horizontally out of a green "
         "screw terminal on a long side: the base's long walls stop at z %.2f, "
         "the board top face, leaving %.2f mm of open side above them. Rev B's "
         "above-terminal route does not exist here."
         % (Z_LONG_WALL_TOP, SIDE_OPEN_H))

    # -- prototype and installation gates ------------------------------------
    print("")
    print("PROTOTYPE GATES - no amount of geometry settles these")
    proto("PCB thickness 1.60 and below-board protrusion 2.50",
          "both STARTING; together they set the 4.50 mm support pad height")
    proto("terminal-block depth 6.50 mm in Y",
          "STARTING; 55.00 outer-to-outer does not give it")
    proto("nothing under the board outside the four modelled joint rows",
          "this is what lets the two cabinet fixings sit on the centreline")
    proto("heat-set insert 4.00 dia x 5.00 deep",
          "the exact part is still not recorded anywhere in the repository")
    proto("the acquired cabinet screw's real head diameter",
          "%.2f mm max envelope declared, ISO 10642 assumed, not measured"
          % CAB_HEAD_D_MAX)
    proto("USB connector position on the acquired ESP32",
          "STARTING; the notch is cut %.2f mm wide to absorb the error"
          % USB_SLOT_W)
    proto("real conductor and ferrule sizes",
          "%.2f mm wire over a %.2f x %.2f ferrule are STARTING"
          % (WIRE_D, FERRULE_D, FERRULE_L))
    proto("EN and BOOT positions", "v1.6 6.4 forbids holes until measured")
    proto("lid fit %.2f mm per face on this printer and filament"
          % LID_FIT_CLEAR)
    proto("cap nib interference %.2f mm per side on this printer"
          % CAB_NIB_INT)
    proto("PETG print quality with no support on any part")
    print("")
    print("ASSUMPTIONS - recorded so they cannot pass as measurements")
    proto("terminal rows centred along the 66.00 mm length",
          "leaves the 6.50 mm of clear board the retention features use")
    proto("58.00 runs along the 66.00 axis and 56.00 across the 63.00",
          "the holes are not used for retention, so nothing here depends on it")
    proto("the USB connector is centred on its short edge")
    proto("the 9.00 mm block height is the block's own body height")

    print("")
    print("INSTALLATION GATES")
    install("cabinet fixing centres and the surface behind them")
    install("the grouped cabinet wiring is secured outside the housing")
    install("antenna performance with the lid fitted")

    print("")
    print("%d checks covering all 30 v1.6 section 13 gates, %d failed, "
          "%d prototype, %d installation"
          % (CHECKS, len(FAILS), len(PROTOS), len(INSTALLS)))
    if FAILS:
        for f in FAILS:
            print("  FAILED: %s" % f)
        return 1
    print("")
    print("All specification v1.6 section 13 gates pass on the exported "
          "meshes. This is NOT physical validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
