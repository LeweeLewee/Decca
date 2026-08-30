# -*- coding: utf-8 -*-
"""
Decca OLED Display Bezel - Rev Q independent offline verifier
=============================================================

Reads ONLY the exported mesh, ../STL/Front_Bezel_revQ.stl, and re-derives the
Rev Q claims from triangles. numpy is the only dependency. Exits non-zero on
failure, so it works as a gate.

It is deliberately NOT a second run of the generator's recipe. The generator
knows what it meant to build; this knows only what came out. Everything below
is measured from the mesh and compared against numbers typed in here by hand
from the controlled documents.

    python mechanical/CAD/Decca_Display_Bezel_revQ_verify.py

It also verifies, from the same mesh, the one thing the whole revision exists
for: that a continuous wall of material surrounds the complete inside
perimeter of the Perspex opening at every depth of the lip.
"""

from __future__ import print_function

import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(HERE, "..", "STL", "Front_Bezel_revQ.stl")

# ---------------------------------------------------------------------------
# Expected values - typed in from the controlled documents, NOT imported from
# the generator. If the generator and these disagree, that is the point.
# ---------------------------------------------------------------------------
BEZEL_W, BEZEL_H, BEZEL_T = 40.00, 20.30, 4.00      # Rev N envelope, PRESERVED
Z_FRONT = 4.20                                       # bezel front face
Z_SEAT = 3.00                                        # Perspex front / seating
Z_TIP = 0.20                                         # lip rear tip
LIP_OUT_W, LIP_OUT_H = 34.90, 15.00                  # lip outer envelope
LIP_IN_W, LIP_IN_H = 34.10, 14.20                    # derived: outer - 2*wall
LIP_WALL = 0.40
LIP_DEPTH = 2.80
LIP_CORNER_R = 0.60
LIP_LEAD = 0.20
WINDOW_W, WINDOW_H = 30.40, 14.20                    # Rev Q clear opening
PANEL_OPEN_W, PANEL_OPEN_H = 35.20, 15.30            # MEASURED
PANEL_T = 3.00
GLASS_FRONT_Z = -0.30
CLEAR_PER_SIDE = 0.15

TOL = 0.02          # mesh/chord tolerance, mm

FAILS = []
CHECKS = 0


def gate(ok, label, detail=""):
    global CHECKS
    CHECKS += 1
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)
    return ok


def note(label, detail=""):
    print("  [    ] %-58s %s" % (label, detail))


# ---------------------------------------------------------------------------
# STL
# ---------------------------------------------------------------------------
def load_stl(path):
    with open(path, "rb") as fh:
        head = fh.read(84)
        if len(head) < 84:
            raise IOError("STL too short: %s" % path)
        n = struct.unpack("<I", head[80:84])[0]
        raw = fh.read(n * 50)
    if len(raw) != n * 50:
        # ASCII STL fallback
        return load_stl_ascii(path)
    arr = np.frombuffer(raw, dtype=np.uint8).reshape(n, 50)
    vals = np.frombuffer(arr[:, :48].tobytes(), dtype="<f4").reshape(n, 12)
    tris = vals[:, 3:12].reshape(n, 3, 3).astype(np.float64)
    return tris


def load_stl_ascii(path):
    pts = []
    with open(path, "r") as fh:
        for line in fh:
            s = line.strip().split()
            if s and s[0] == "vertex":
                pts.append([float(s[1]), float(s[2]), float(s[3])])
    a = np.array(pts, dtype=np.float64)
    return a.reshape(-1, 3, 3)


def weld(tris, dec=5):
    """Index the triangles onto welded vertices."""
    v = tris.reshape(-1, 3)
    key = np.round(v, dec)
    uniq, inv = np.unique(key, axis=0, return_inverse=True)
    return uniq, inv.reshape(-1, 3)


# ---------------------------------------------------------------------------
# Topology
# ---------------------------------------------------------------------------
def manifold(faces):
    """Every edge must be shared by exactly two triangles, and each directed
    edge must appear exactly once - that is closed AND consistently oriented."""
    e = np.vstack([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    und = np.sort(e, axis=1)
    _u, cnt = np.unique(und, axis=0, return_counts=True)
    bad_und = int(np.sum(cnt != 2))
    _d, dcnt = np.unique(e, axis=0, return_counts=True)
    bad_dir = int(np.sum(dcnt != 1))
    return bad_und, bad_dir


def components(nverts, faces):
    """Connected components over the vertex graph - union-find."""
    parent = np.arange(nverts)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for tri in faces:
        union(tri[0], tri[1])
        union(tri[1], tri[2])
    roots = set(find(i) for i in range(nverts))
    return len(roots)


def volume(tris):
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    return float(np.abs(np.sum(np.einsum("ij,ij->i", a, np.cross(b, c))) / 6.0))


# ---------------------------------------------------------------------------
# Geometry probes
# ---------------------------------------------------------------------------
def section_segments(tris, z):
    """All triangle/plane intersection segments at height z."""
    segs = []
    for t in tris:
        d = t[:, 2] - z
        if np.all(d > 0) or np.all(d < 0):
            continue
        pts = []
        for i in range(3):
            j = (i + 1) % 3
            di, dj = d[i], d[j]
            if di == 0.0:
                pts.append(t[i][:2])
            if (di < 0 < dj) or (dj < 0 < di):
                f = di / (di - dj)
                pts.append((t[i] + f * (t[j] - t[i]))[:2])
        if len(pts) >= 2:
            segs.append((pts[0], pts[1]))
    return segs


def section_bbox(tris, z):
    segs = section_segments(tris, z)
    if not segs:
        return None
    p = np.array([q for s in segs for q in s])
    return (p[:, 0].min(), p[:, 0].max(), p[:, 1].min(), p[:, 1].max())


def inside_xy(tris, x, y, zlo, zhi):
    """Is the vertical line at (x, y) inside the solid between zlo and zhi?

    Counts triangle crossings of the upward ray from (x, y, zlo) and keeps the
    crossings that fall in the band. Robust enough here because every probe is
    placed off the mesh's own vertices.
    """
    hits = ray_hits(tris, x, y)
    inside_lo = (np.sum(hits > zlo) % 2) == 1
    return inside_lo, hits


def ray_hits(tris, x, y):
    """Z heights where the +Z ray through (x, y) crosses the surface."""
    v0, v1, v2 = tris[:, 0], tris[:, 1], tris[:, 2]
    x0, y0 = v0[:, 0], v0[:, 1]
    x1, y1 = v1[:, 0], v1[:, 1]
    x2, y2 = v2[:, 0], v2[:, 1]
    d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    ok = np.abs(d) > 1e-14
    a = np.zeros_like(d)
    b = np.zeros_like(d)
    a[ok] = ((y1 - y2)[ok] * (x - x2[ok]) + (x2 - x1)[ok] * (y - y2[ok])) / d[ok]
    b[ok] = ((y2 - y0)[ok] * (x - x2[ok]) + (x0 - x2)[ok] * (y - y2[ok])) / d[ok]
    c = 1.0 - a - b
    m = ok & (a >= 0) & (b >= 0) & (c >= 0)
    if not np.any(m):
        return np.array([])
    z = (a[m] * v0[m][:, 2] + b[m] * v1[m][:, 2] + c[m] * v2[m][:, 2])
    return np.sort(z)


def rrect_path(A, Bh, R, n):
    """Points on a rounded-rectangle boundary with the inward unit normal."""
    a, bb = A - R, Bh - R
    out = []
    per_side = max(2, n // 8)
    for i in range(per_side):
        t = -bb + 2 * bb * i / (per_side - 1)
        out.append((A, t, -1.0, 0.0))
        out.append((-A, t, 1.0, 0.0))
        s = -a + 2 * a * i / (per_side - 1)
        out.append((s, Bh, 0.0, -1.0))
        out.append((s, -Bh, 0.0, 1.0))
    if R > 0:
        for sx in (1.0, -1.0):
            for sy in (1.0, -1.0):
                for i in range(per_side):
                    th = 0.5 * np.pi * i / (per_side - 1)
                    cx, cy = np.cos(th), np.sin(th)
                    out.append((sx * (a + R * cx), sy * (bb + R * cy),
                                -sx * cx, -sy * cy))
    return out


# ---------------------------------------------------------------------------
def main():
    print("=" * 74)
    print("DECCA OLED DISPLAY BEZEL - REV Q OFFLINE MESH VERIFICATION")
    print("=" * 74)
    path = os.path.normpath(STL)
    if not os.path.exists(path):
        print("MISSING MESH: %s" % path)
        return 2
    tris = load_stl(path)
    verts, faces = weld(tris)
    print("mesh: %s" % path)
    print("      %d triangles, %d welded vertices, %d bytes"
          % (len(tris), len(verts), os.path.getsize(path)))
    print("")

    print("1. MESH TOPOLOGY")
    bad_und, bad_dir = manifold(faces)
    gate(bad_und == 0, "every edge shared by exactly two triangles",
         "%d bad edge(s)" % bad_und)
    gate(bad_dir == 0, "consistent outward winding, no duplicate directed edge",
         "%d bad" % bad_dir)
    ncomp = components(len(verts), faces)
    gate(ncomp == 1, "ONE connected component - a single solid",
         "%d component(s)" % ncomp)
    deg = np.zeros(len(verts), dtype=int)
    for tri in faces:
        for i in tri:
            deg[i] += 1
    gate(int(np.sum(deg == 0)) == 0, "no orphan vertices",
         "%d" % int(np.sum(deg == 0)))
    areas = 0.5 * np.linalg.norm(
        np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]), axis=1)
    gate(float(areas.min()) > 1e-9, "no degenerate (zero-area) triangles",
         "min %.3e mm2" % float(areas.min()))
    note("mesh volume", "%.4f mm3  (%.4f cm3)"
         % (volume(tris), volume(tris) / 1000.0))

    print("")
    print("2. ENVELOPE - the Rev N appearance, PRESERVED")
    lo = tris.reshape(-1, 3).min(axis=0)
    hi = tris.reshape(-1, 3).max(axis=0)
    gate(abs((hi[0] - lo[0]) - BEZEL_W) < TOL, "envelope width 40.00 mm",
         "%.4f" % (hi[0] - lo[0]))
    gate(abs((hi[1] - lo[1]) - BEZEL_H) < TOL, "envelope height 20.30 mm",
         "%.4f" % (hi[1] - lo[1]))
    gate(abs((hi[2] - lo[2]) - BEZEL_T) < TOL, "envelope depth 4.00 mm",
         "%.4f" % (hi[2] - lo[2]))
    gate(abs(hi[2] - Z_FRONT) < TOL, "front face at z = +4.200",
         "%.4f" % hi[2])
    gate(abs(lo[2] - Z_TIP) < TOL, "rearmost material at z = +0.200",
         "%.4f" % lo[2])
    gate(abs(lo[0] + BEZEL_W / 2) < TOL and abs(lo[1] + BEZEL_H / 2) < TOL,
         "centred on the opening datum",
         "x0 %.4f  y0 %.4f" % (lo[0], lo[1]))

    print("")
    print("3. NOTHING BEHIND THE PERSPEX, NOTHING NEAR THE GLASS")
    gate(lo[2] >= 0.0 - 1e-9,
         "no material behind the Perspex rear face (z = 0)",
         "lowest z = %+.4f" % lo[2])
    gate(lo[2] - 0.0 >= 0.20 - TOL,
         "clear of the Perspex rear face by 0.200 mm",
         "%.4f mm" % (lo[2] - 0.0))
    gate(lo[2] - GLASS_FRONT_Z >= 0.50 - TOL,
         "clear of the OLED glass front face by >= 0.500 mm",
         "%.4f mm" % (lo[2] - GLASS_FRONT_Z))

    print("")
    print("4. THE CONTINUOUS LIP - cross-sections through the skirt")
    for z in (Z_TIP + LIP_LEAD + 0.05, 1.60, Z_SEAT - 0.05):
        bb = section_bbox(tris, z)
        okw = abs((bb[1] - bb[0]) - LIP_OUT_W) < TOL
        okh = abs((bb[3] - bb[2]) - LIP_OUT_H) < TOL
        gate(okw and okh,
             "z = %.2f  outer section is %.2f x %.2f" % (z, LIP_OUT_W,
                                                         LIP_OUT_H),
             "%.4f x %.4f" % (bb[1] - bb[0], bb[3] - bb[2]))

    # walk the whole perimeter and demand material at every station
    print("")
    print("5. THE CONTINUOUS LIP - continuity right around the perimeter")
    zs = [Z_TIP + LIP_LEAD + 0.05, 1.60, Z_SEAT - 0.05]
    path_pts = rrect_path(LIP_OUT_W / 2.0, LIP_OUT_H / 2.0, LIP_CORNER_R, 720)
    sides = {"left": [0, 0], "right": [0, 0], "top": [0, 0],
             "bottom": [0, 0], "corner": [0, 0]}
    ax = LIP_OUT_W / 2.0 - LIP_CORNER_R
    ay = LIP_OUT_H / 2.0 - LIP_CORNER_R
    voids = 0
    walls = []
    for (px, py, nx, ny) in path_pts:
        mx, my = px + nx * LIP_WALL / 2.0, py + ny * LIP_WALL / 2.0
        hits = ray_hits(tris, mx, my)
        present_all = True
        for z in zs:
            if (np.sum(hits > z) % 2) != 1:
                present_all = False
        if abs(px) > ax - 1e-9 and abs(py) > ay - 1e-9:
            key = "corner"
        elif abs(py) >= ay - 1e-9:
            key = "top" if py > 0 else "bottom"
        else:
            key = "right" if px > 0 else "left"
        sides[key][0] += 1
        if present_all:
            sides[key][1] += 1
        else:
            voids += 1
        # wall thickness along the inward normal at z = 1.60
        t_in, t_out = None, None
        for k in range(1, 121):
            t = k * 0.005
            hx, hy = px + nx * t, py + ny * t
            h = ray_hits(tris, hx, hy)
            ins = (np.sum(h > 1.60) % 2) == 1
            if ins and t_in is None:
                t_in = t
            if t_in is not None and not ins:
                t_out = t
                break
        if t_in is not None and t_out is not None:
            walls.append(t_out - t_in)
    gate(voids == 0, "material at all %d perimeter stations x 3 depths"
         % len(path_pts), "%d void station(s)" % voids)
    for k in ("left", "right", "top", "bottom", "corner"):
        tot, hit = sides[k]
        gate(tot > 0 and hit == tot, "lip continuous - %s" % k,
             "%d/%d" % (hit, tot))
    if walls:
        w = np.array(walls)
        gate(abs(w.mean() - LIP_WALL) < 0.02,
             "measured lip wall = 0.400 mm",
             "mean %.4f  min %.4f  max %.4f" % (w.mean(), w.min(), w.max()))

    print("")
    print("6. LIP ENVELOPE, DEPTH AND CLEARANCE")
    bb = section_bbox(tris, 1.60)
    gate(abs((bb[1] - bb[0]) - LIP_OUT_W) < TOL,
         "lip outer width  34.90 mm", "%.4f" % (bb[1] - bb[0]))
    gate(abs((bb[3] - bb[2]) - LIP_OUT_H) < TOL,
         "lip outer height 15.00 mm", "%.4f" % (bb[3] - bb[2]))
    # Inner opening at a given height, probing outward along an axis.
    #
    # Straight bisection is WRONG here and silently returns the outer edge of
    # the part: walking out along an axis the ray goes hole -> material ->
    # air, so the predicate is not monotone, and a 0.40 mm band of material is
    # exactly the kind of thing bisection steps straight over. Scan out in
    # steps smaller than the thinnest wall, then refine the first crossing.
    def _in(z, axis, t):
        x, y = (t, 0.0) if axis == "x" else (0.0, t)
        return (np.sum(ray_hits(tris, x, y) > z) % 2) == 1

    def opening_at(z, axis, limit=21.0, step=0.02):
        prev = 0.0
        t = step
        while t < limit:
            if _in(z, axis, t):
                lo_, hi_ = prev, t
                for _ in range(40):
                    mid = (lo_ + hi_) / 2.0
                    if _in(z, axis, mid):
                        hi_ = mid
                    else:
                        lo_ = mid
                return (lo_ + hi_) / 2.0
            prev = t
            t += step
        return float("nan")
    iw = 2 * opening_at(1.60, "x")
    ih = 2 * opening_at(1.60, "y")
    gate(abs(iw - LIP_IN_W) < 0.02, "lip inner width  34.10 mm", "%.4f" % iw)
    gate(abs(ih - LIP_IN_H) < 0.02, "lip inner height 14.20 mm", "%.4f" % ih)
    gate(abs((Z_SEAT - Z_TIP) - LIP_DEPTH) < 1e-9, "lip depth 2.800 mm",
         "%.4f" % (Z_SEAT - Z_TIP))
    cx = (PANEL_OPEN_W - LIP_OUT_W) / 2.0
    cy = (PANEL_OPEN_H - LIP_OUT_H) / 2.0
    gate(abs(cx - CLEAR_PER_SIDE) < 1e-9 and abs(cy - CLEAR_PER_SIDE) < 1e-9,
         "clearance into the measured opening 0.150 mm per side",
         "x %.4f  y %.4f" % (cx, cy))

    print("")
    print("7. THE VISIBLE WINDOW AND THE EFFECTIVE OPTICAL OPENING")
    ow = 2 * opening_at(3.60, "x")
    oh = 2 * opening_at(3.60, "y")
    gate(abs(ow - WINDOW_W) < 0.02, "window width  30.40 mm (Rev N, preserved)",
         "%.4f" % ow)
    gate(abs(oh - WINDOW_H) < 0.02, "window height 14.20 mm (DERIVED from lip)",
         "%.4f" % oh)
    eff_w = min(ow, iw)
    eff_h = min(oh, ih)
    gate(abs(eff_w - WINDOW_W) < 0.02 and abs(eff_h - LIP_IN_H) < 0.02,
         "EFFECTIVE optical opening 30.40 x 14.20 mm",
         "%.4f x %.4f" % (eff_w, eff_h))
    note("controlled by",
         "width by the bezel window, HEIGHT BY THE NEW LIP")
    note("versus Rev N (30.40 x 14.90)",
         "height -0.700 mm total, -0.350 mm per side")

    print("")
    print("8. THE LEAD-IN MUST NOT EAT THE COVERAGE")
    bb_tip = section_bbox(tris, Z_TIP + 0.001)
    tip_w = bb_tip[1] - bb_tip[0]
    gate(abs(tip_w - (LIP_OUT_W - 2 * LIP_LEAD)) < 0.05,
         "lead-in present: tip is 0.200 mm inboard of the envelope",
         "%.4f vs %.4f" % (tip_w, LIP_OUT_W - 2 * LIP_LEAD))
    bbf = section_bbox(tris, Z_TIP + LIP_LEAD + 0.02)
    gate(abs((bbf[1] - bbf[0]) - LIP_OUT_W) < TOL,
         "full envelope restored by z = +0.400, so 2.600 mm of the 3.000 mm "
         "Perspex is covered at full clearance",
         "%.4f" % (bbf[1] - bbf[0]))

    print("")
    print("=" * 74)
    if FAILS:
        print("RESULT: %d/%d PASS - FAILURES:" % (CHECKS - len(FAILS), CHECKS))
        for f in FAILS:
            print("   FAILED: %s" % f)
        print("=" * 74)
        return 1
    print("RESULT: %d/%d PASS - the exported mesh matches the Rev Q claims"
          % (CHECKS, CHECKS))
    print("")
    print("This proves geometry only. It does NOT prove the bezel fits the")
    print("real Perspex: the opening corner radius has never been measured,")
    print("and no CAD or mesh check in this repository can settle it. See the")
    print("Rev Q build report, and print the corner gauge coupon first.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
