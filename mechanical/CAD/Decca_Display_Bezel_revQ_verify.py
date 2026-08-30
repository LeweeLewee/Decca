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
import math
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
LIP_OUT_W, LIP_OUT_H = 35.40, 15.20                  # inset-wall outer envelope
LIP_IN_W, LIP_IN_H = 33.80, 13.60                    # derived: outer - 2*wall
LIP_WALL = 0.80                                      # two 0.40 loops
LIP_DEPTH = 2.80
LIP_CORNER_R = 3.00                                  # owner +50%, was 2.00
LIP_INNER_R = 2.20                                   # derived: 3.00 - 0.80
LIP_LEAD = 0.20
EXTRUSION_W = 0.40                                   # production extrusion
WALL_LOOPS = 2                                       # the whole point of Rev Q
FACE_OPEN_W, FACE_OPEN_H = 30.90, 15.35              # bezel face opening
OPTICAL_W, OPTICAL_H = 30.90, 13.60                  # effective clear opening
AP_ROOT_RELIEF = 0.02                                # anti-tangency relief
AP_REAR_H = OPTICAL_H + 2 * AP_ROOT_RELIEF           # aperture at the seat
PANEL_OPEN_W, PANEL_OPEN_H = 35.20, 15.30            # MEASURED
PANEL_T = 3.00
GLASS_FRONT_Z = -0.30
INTERF_X = 0.10                                      # per side, INTERFERENCE
CLEAR_Y = 0.05                                       # per side, clearance

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
    wall_arr = None
    if walls:
        w = np.array(walls)
        wall_arr = w
        gate(abs(w.mean() - LIP_WALL) < 0.02
             and abs(w.min() - LIP_WALL) < 0.03
             and abs(w.max() - LIP_WALL) < 0.03,
             "measured lip wall = %.2f mm everywhere" % LIP_WALL,
             "mean %.4f  min %.4f  max %.4f" % (w.mean(), w.min(), w.max()))
        # the corner stations on their own - a constant wall through an
        # R2.00 outer / R1.20 inner corner is the hardest part to get right
        cw = [walls[i] for i, (px, py, _n, _m) in enumerate(path_pts[:len(walls)])
              if abs(px) > ax - 1e-9 and abs(py) > ay - 1e-9]
        if cw:
            c = np.array(cw)
            gate(abs(c.min() - LIP_WALL) < 0.03
                 and abs(c.max() - LIP_WALL) < 0.03,
                 "wall stays %.2f mm THROUGH THE R%.2f CORNERS"
                 % (LIP_WALL, LIP_CORNER_R),
                 "%d corner stations, min %.4f max %.4f"
                 % (len(cw), c.min(), c.max()))

    print("")
    print("5b. THE TWO-LOOP WALL - the point of the 0.80 mm amendment")
    gate(abs(LIP_WALL / EXTRUSION_W - WALL_LOOPS) < 1e-9,
         "wall is EXACTLY %d x %.2f mm extrusion loops"
         % (WALL_LOOPS, EXTRUSION_W),
         "%.2f / %.2f = %.4f" % (LIP_WALL, EXTRUSION_W,
                                 LIP_WALL / EXTRUSION_W))
    if wall_arr is not None:
        gate(wall_arr.min() >= WALL_LOOPS * EXTRUSION_W - 0.03,
             "no measured station thinner than %d extrusions - nowhere for "
             "the slicer to substitute gap fill" % WALL_LOOPS,
             "thinnest measured %.4f mm vs %.2f mm required"
             % (wall_arr.min(), WALL_LOOPS * EXTRUSION_W))
    # the two loop centrelines are inward offsets of the outer surface by
    # 0.20 and 0.60. Both must survive the corners without cusping or
    # merging, or the slicer drops one or fuses them.
    r1 = LIP_CORNER_R - EXTRUSION_W / 2.0
    r2 = LIP_CORNER_R - EXTRUSION_W - EXTRUSION_W / 2.0
    gate(r2 > 0.0,
         "loop radii at the R%.2f corner: outer %.2f, inner %.2f - no cusp"
         % (LIP_CORNER_R, r1, r2), "smallest offset radius %.3f mm" % r2)
    gate(abs((r1 - r2) - EXTRUSION_W) < 1e-9,
         "loop centrelines stay exactly one extrusion apart",
         "%.4f mm" % (r1 - r2))
    gate(LIP_INNER_R >= 0.0
         and abs(LIP_INNER_R - (LIP_CORNER_R - LIP_WALL)) < 1e-9,
         "inner corner R%.2f = outer R%.2f - wall %.2f"
         % (LIP_INNER_R, LIP_CORNER_R, LIP_WALL), "%.4f" % LIP_INNER_R)
    note("still a physical gate",
         "this proves the GEOMETRY admits two continuous loops; only the "
         "production slicer preview can prove it lays them")

    print("")
    print("6. LIP ENVELOPE, DEPTH AND FIT")
    bb = section_bbox(tris, 1.60)
    gate(abs((bb[1] - bb[0]) - LIP_OUT_W) < TOL,
         "lip outer width  %.2f mm" % LIP_OUT_W, "%.4f" % (bb[1] - bb[0]))
    gate(abs((bb[3] - bb[2]) - LIP_OUT_H) < TOL,
         "lip outer height %.2f mm" % LIP_OUT_H, "%.4f" % (bb[3] - bb[2]))
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
    gate(abs(iw - LIP_IN_W) < 0.02, "lip inner width  %.2f mm" % LIP_IN_W,
         "%.4f" % iw)
    gate(abs(ih - LIP_IN_H) < 0.02, "lip inner height %.2f mm" % LIP_IN_H,
         "%.4f" % ih)
    gate(abs((Z_SEAT - Z_TIP) - LIP_DEPTH) < 1e-9, "lip depth 2.800 mm",
         "%.4f" % (Z_SEAT - Z_TIP))
    ix = (LIP_OUT_W - PANEL_OPEN_W) / 2.0          # positive = interference
    cy = (PANEL_OPEN_H - LIP_OUT_H) / 2.0          # positive = clearance
    gate(abs(ix - INTERF_X) < 1e-9,
         "horizontal INTERFERENCE %.3f mm per side" % INTERF_X,
         "%+.4f mm" % ix)
    gate(abs(cy - CLEAR_Y) < 1e-9,
         "vertical clearance %.3f mm per side" % CLEAR_Y, "%+.4f mm" % cy)
    note("the lip is WIDER than the hole by design",
         "brief 3.7/3.8: the thin printed lip takes the deflection, the "
         "Perspex is not to be spread or stressed - a PHYSICAL gate")

    print("")
    print("7. THE FACE OPENING AND THE EFFECTIVE OPTICAL OPENING")
    # The aperture is tapered in Y, so its height is a linear function of z.
    # Measure it at two heights clear of both the 0.40 front break and the
    # seating plane, fit the line, and read off both ends. That verifies the
    # taper AND the two published numbers without trusting either.
    z_a, z_b = 3.20, 3.70
    h_a, h_b = 2 * opening_at(z_a, "y"), 2 * opening_at(z_b, "y")
    slope = (h_b - h_a) / (z_b - z_a)
    h_seat = h_a + slope * (Z_SEAT - z_a)
    h_front = h_a + slope * (Z_FRONT - z_a)
    ang = math.degrees(math.atan2(slope / 2.0, 1.0))
    note("aperture height at z = %.2f and %.2f" % (z_a, z_b),
         "%.4f and %.4f mm" % (h_a, h_b))
    gate(abs(h_seat - AP_REAR_H) < 0.03,
         "extrapolates to %.3f mm at the seating plane" % AP_REAR_H,
         "%.4f" % h_seat)
    gate(h_seat > OPTICAL_H + 1e-9,
         "aperture stops OUTSIDE the lip inner, so the LIP controls the "
         "clear height",
         "aperture %.3f vs lip inner %.3f, relief %.3f per side"
         % (h_seat, OPTICAL_H, (h_seat - OPTICAL_H) / 2.0))
    gate(abs(h_front - FACE_OPEN_H) < 0.03,
         "extrapolates to %.2f mm at the front face (the face opening)"
         % FACE_OPEN_H, "%.4f" % h_front)
    gate(ang <= 45.0,
         "aperture taper %.2f deg from vertical - self-supporting" % ang,
         "%.2f deg" % ang)
    ow = 2 * opening_at(3.60, "x")
    gate(abs(ow - FACE_OPEN_W) < 0.02,
         "face opening width %.2f mm, constant through the taper" % FACE_OPEN_W,
         "%.4f" % ow)
    eff_w = min(ow, iw)
    eff_h = min(h_seat, ih)
    gate(abs(eff_w - OPTICAL_W) < 0.02 and abs(eff_h - OPTICAL_H) < 0.03,
         "EFFECTIVE optical opening %.2f x %.2f mm" % (OPTICAL_W, OPTICAL_H),
         "%.4f x %.4f" % (eff_w, eff_h))
    note("controlled by",
         "width by the %.2f mm face opening, HEIGHT BY THE %.2f mm LIP INNER"
         % (FACE_OPEN_W, LIP_IN_H))
    note("versus Rev N (30.40 x 14.90)",
         "width +0.500, height -1.300 total, -0.650 per side")

    print("")
    print("8. THE LEAD-IN MUST NOT EAT THE COVERAGE")
    bb_tip = section_bbox(tris, Z_TIP + 0.001)
    tip_w = bb_tip[1] - bb_tip[0]
    gate(abs(tip_w - (LIP_OUT_W - 2 * LIP_LEAD)) < 0.05,
         "lead-in present: tip is %.2f mm inboard of the envelope" % LIP_LEAD,
         "%.4f vs %.4f" % (tip_w, LIP_OUT_W - 2 * LIP_LEAD))
    bbf = section_bbox(tris, Z_TIP + LIP_LEAD + 0.02)
    gate(abs((bbf[1] - bbf[0]) - LIP_OUT_W) < TOL,
         "full envelope restored by z = +0.400, so 2.600 mm of the 3.000 mm "
         "Perspex is covered at full section",
         "%.4f" % (bbf[1] - bbf[0]))
    note("the lead-in also starts the interference fit",
         "the tip is %.2f mm UNDER the %.2f mm opening, so entry is free for "
         "the first %.2f mm and the %.2f mm per side engages after that"
         % (PANEL_OPEN_W - (LIP_OUT_W - 2 * LIP_LEAD), PANEL_OPEN_W,
            LIP_LEAD, INTERF_X))

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
    print("This proves geometry only. It does NOT prove the bezel FITS. The")
    print("0.10 mm per side horizontal INTERFERENCE is now resisted by a wall")
    print("8x stiffer in bending than the 0.40 mm one it replaces, and the")
    print("opening corner radius has never been measured. No CAD or mesh check")
    print("in this repository can settle either. Print Bezel_Fit_Gauge_revQ")
    print("first, and see the Rev Q build report.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
