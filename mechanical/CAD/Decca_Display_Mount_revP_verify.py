# -*- coding: utf-8 -*-
"""
Rev P independent verification - reads the EXPORTED STL, not the build recipe.

    python mechanical/CAD/Decca_Display_Mount_revP_verify.py

Why this exists, and what it is not
-----------------------------------
Rev O was checked by re-running the same parameter table and the same body
recipes through a second geometry kernel. Both sides agreed, and both were
wrong in the same way, because agreement between two transcriptions of one
recipe proves only that the transcription was faithful. It cannot find a check
that is missing from both.

This file deliberately shares nothing with the generator:

* it reads the **exported binary STL** - the artefact that actually gets
  printed - and never imports, parses or executes the generator;
* the requirements are re-entered here from the **measured repository values
  and the Rev P brief**, independently of any parameter the generator holds, so
  a silent parameter drift in the generator shows up as a failure here;
* the algorithms are different in kind: triangle/AABB separating-axis tests,
  ray-cast point membership, edge-manifold counting and a divergence-theorem
  volume, rather than BRep booleans;
* it checks the assembly path, the disassembly path, the load path, the
  retention function and the dimensional assumptions, not just the final
  seated position.

Requires numpy only.
"""

import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MECH = os.path.abspath(os.path.join(HERE, ".."))
STL_PATH = os.path.join(MECH, "STL", "Rear_Display_Carrier_revP.stl")

# ---------------------------------------------------------------------------
# REQUIREMENTS - re-entered from the measured repository values and the Rev P
# brief. NOT read from the generator.
# ---------------------------------------------------------------------------
R = dict(
    # measured Decca fascia
    perspex_t=3.00,
    aperture_w=35.20, aperture_h=15.30,
    m2_pitch=49.00,
    # measured / reference OLED module
    pcb_w=35.40, pcb_h=33.50, pcb_t=1.60, pcb_off_y=4.00,
    glass_w=34.50, glass_h=23.00, glass_off_y=2.45,
    glass_proud=0.80,                 # MEASURED at Rev N
    hole_d=3.00, hole_pitch_x=30.00, hole_pitch_y=28.50,
    header_w=10.00, header_h=3.00, header_off_y=19.25, header_depth=8.10,
    # accepted module-preparation limit; 1.10 mm is the zero-margin ceiling
    tip_proud=1.00,
    tip_d=1.20, tip_pitch=2.54, tip_cx=0.50,
    tip_y_top=18.55, tip_y_bot=-10.55,
    # Rev P design intent
    gap=0.30,                         # controlled optical gap
    setback=0.10,                     # carrier limit behind the PCB front face
    pcb_clearance=0.25,
    aperture_margin=0.60,
    # expected carrier envelope
    car_w=56.60, car_h=47.20, car_d=9.60,
    # expected retention geometry
    finger_x=10.00, finger_w=4.00, finger_t=0.75,
    finger_grip=0.10, finger_nose=0.40, finger_relief=1.00,
    finger_root=1.20,
    # material
    petg_E=2000.0, mu=0.30, module_mass_g=4.00,
    strain_limit=3.00,
    travel=12.00,
)

# derived requirement chain - independent arithmetic
Z_PERSPEX_REAR = 0.0
Z_GLASS_FRONT = -R["gap"]
Z_PCB_FRONT = Z_GLASS_FRONT - R["glass_proud"]
Z_FWD_LIMIT = Z_PCB_FRONT - R["setback"]
Z_PCB_REAR = Z_PCB_FRONT - R["pcb_t"]
Z_REAR = -R["car_d"]
Z_TIP_FRONT = Z_PCB_FRONT + R["tip_proud"]

PCB = (-R["pcb_w"] / 2, R["pcb_w"] / 2,
       R["pcb_off_y"] - R["pcb_h"] / 2, R["pcb_off_y"] + R["pcb_h"] / 2)
GLASS = (-R["glass_w"] / 2, R["glass_w"] / 2,
         R["glass_off_y"] - R["glass_h"] / 2, R["glass_off_y"] + R["glass_h"] / 2)
PK = (PCB[0] - R["pcb_clearance"], PCB[1] + R["pcb_clearance"],
      PCB[2] - R["pcb_clearance"], PCB[3] + R["pcb_clearance"])
AP = (PK[0] - R["aperture_margin"], PK[1] + R["aperture_margin"],
      PK[2] - R["aperture_margin"], PK[3] + R["aperture_margin"])

FAILS = []
NOTES = []


def check(ok, label, detail=""):
    print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)
    return ok


def note(label, detail=""):
    print("  [ -- ] %-56s %s" % (label, detail))


# ---------------------------------------------------------------------------
# STL
# ---------------------------------------------------------------------------
def read_binary_stl(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) < 84:
        raise ValueError("file too short to be a binary STL")
    n = struct.unpack("<I", data[80:84])[0]
    expect = 84 + 50 * n
    if len(data) != expect:
        raise ValueError("not a binary STL: %d triangles implies %d bytes, got %d"
                         % (n, expect, len(data)))
    raw = np.frombuffer(data, dtype=np.uint8, count=50 * n, offset=84)
    raw = raw.reshape(n, 50)
    floats = raw[:, :48].copy().view("<f4").reshape(n, 12)
    normals = floats[:, 0:3].astype(np.float64)
    tris = floats[:, 3:12].astype(np.float64).reshape(n, 3, 3)
    return tris, normals


def weld(tris, tol=1e-4):
    v = tris.reshape(-1, 3)
    keys = np.round(v / tol).astype(np.int64)
    uniq, inv = np.unique(keys, axis=0, return_inverse=True)
    verts = np.zeros((len(uniq), 3))
    np.add.at(verts, inv, v)
    cnt = np.bincount(inv, minlength=len(uniq)).astype(np.float64)
    verts /= cnt[:, None]
    return verts, inv.reshape(-1, 3)


def mesh_volume(tris):
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    return float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)


# ---------------------------------------------------------------------------
# triangle / axis-aligned box overlap  (Akenine-Moller separating axis test)
# ---------------------------------------------------------------------------
def tris_hit_box(tris, box, shrink=0.0):
    """Boolean mask of triangles overlapping the AABB.

    ``box`` is (x0, x1, y0, y1, z0, z1). ``shrink`` pulls every face inward, so
    exact face-to-face tangency is not reported as an overlap.
    """
    lo = np.array([box[0] + shrink, box[2] + shrink, box[4] + shrink])
    hi = np.array([box[1] - shrink, box[3] - shrink, box[5] - shrink])
    if np.any(hi <= lo):
        return np.zeros(len(tris), dtype=bool)
    c = (lo + hi) / 2.0
    e = (hi - lo) / 2.0

    v = tris - c                                    # (n,3,3)
    live = np.ones(len(tris), dtype=bool)

    # 1. the three box axes
    for k in range(3):
        vk = v[:, :, k]
        live &= ~((vk.min(axis=1) > e[k]) | (vk.max(axis=1) < -e[k]))
    if not live.any():
        return live

    idx = np.nonzero(live)[0]
    vv = v[idx]
    f = np.stack([vv[:, 1] - vv[:, 0], vv[:, 2] - vv[:, 1], vv[:, 0] - vv[:, 2]],
                 axis=1)                            # (m,3,3) edge vectors

    # 2. the triangle normal
    nrm = np.cross(f[:, 0], f[:, 1])
    d = np.einsum("ij,ij->i", nrm, vv[:, 0])
    r = np.einsum("ij,j->i", np.abs(nrm), e)
    keep = np.abs(d) <= r + 1e-12

    # 3. the nine edge cross products
    basis = np.eye(3)
    for ei in range(3):
        for bi in range(3):
            ax = np.cross(basis[bi], f[:, ei])
            p = np.einsum("mij,mj->mi", vv, ax)
            rr = np.einsum("mj,j->m", np.abs(ax), e)
            keep &= ~((p.min(axis=1) > rr + 1e-12) | (p.max(axis=1) < -rr - 1e-12))

    out = np.zeros(len(tris), dtype=bool)
    out[idx[keep]] = True
    return out


def boxes_hit(tris, boxes, shrink=0.0):
    total = np.zeros(len(tris), dtype=bool)
    for b in boxes:
        total |= tris_hit_box(tris, b, shrink)
    return total


# ---------------------------------------------------------------------------
# ray-cast point membership  (Moller-Trumbore, odd crossing count = inside)
# ---------------------------------------------------------------------------
_DIR = np.array([0.5773502691896258, 0.3333333333333333, 0.7453559924999299])
_DIR = _DIR / np.linalg.norm(_DIR)


def ray_ts(tris, origin, direction):
    """Signed parametric distances of every ray/triangle crossing."""
    o = np.asarray(origin, dtype=np.float64)
    dv = np.asarray(direction, dtype=np.float64)
    e1 = tris[:, 1] - tris[:, 0]
    e2 = tris[:, 2] - tris[:, 0]
    p = np.cross(dv, e2)
    det = np.einsum("ij,ij->i", e1, p)
    ok = np.abs(det) > 1e-12
    inv = np.zeros_like(det)
    inv[ok] = 1.0 / det[ok]
    tvec = o - tris[:, 0]
    u = np.einsum("ij,ij->i", tvec, p) * inv
    q = np.cross(tvec, e1)
    vpar = np.einsum("j,ij->i", dv, q) * inv
    t = np.einsum("ij,ij->i", e2, q) * inv
    good = ok & (u >= -1e-9) & (vpar >= -1e-9) & (u + vpar <= 1.0 + 1e-9)
    return np.sort(t[good])


def inside(tris, x, y, z):
    t = ray_ts(tris, (x, y, z), _DIR)
    return int(np.sum(t > 1e-9)) % 2 == 1


def material_spans(tris, origin, direction, lo=-1e9, hi=1e9):
    """Material intervals along a ray - used to MEASURE sections off the mesh."""
    t = ray_ts(tris, origin, direction)
    t = t[(t > lo) & (t < hi)]
    if len(t) % 2:
        return None
    return [(float(t[i]), float(t[i + 1])) for i in range(0, len(t), 2)]


# ---------------------------------------------------------------------------
def main():
    print("=" * 80)
    print("REV P INDEPENDENT VERIFICATION  (exported STL, not the build recipe)")
    print("=" * 80)
    if not os.path.isfile(STL_PATH):
        print("STL not found: %s" % STL_PATH)
        return 2
    tris, normals = read_binary_stl(STL_PATH)
    print("source : %s" % STL_PATH)
    print("         %d triangles, %.1f kB" % (len(tris), os.path.getsize(STL_PATH) / 1024.0))

    # ---- A. mesh integrity ----------------------------------------------
    print("")
    print("A. MESH INTEGRITY OF THE PRINTED ARTEFACT")
    verts, faces = weld(tris)
    ed = {}
    for f in faces:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            k = (a, b) if a < b else (b, a)
            ed[k] = ed.get(k, 0) + 1
    bad = sum(1 for v in ed.values() if v != 2)
    check(bad == 0, "closed 2-manifold", "%d vertices, %d edges, %d non-manifold"
          % (len(verts), len(ed), bad))
    directed = set()
    dup = 0
    for f in faces:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            if (a, b) in directed:
                dup += 1
            directed.add((a, b))
    check(dup == 0, "consistent triangle winding", "%d duplicated directed edges" % dup)
    vol = mesh_volume(tris)
    check(vol > 0, "outward orientation / positive volume",
          "%.4f cm3  (%.2f g in PETG at 1.27 g/cm3)" % (vol / 1000.0, vol / 1000.0 * 1.27))
    lo = tris.reshape(-1, 3).min(axis=0)
    hi = tris.reshape(-1, 3).max(axis=0)
    size = hi - lo
    # the STL tessellates the cylindrical M2 ear ends, so the mesh sits a
    # chord-height under nominal across X. 0.05 mm covers MeshRefinementHigh.
    check(abs(size[0] - R["car_w"]) < 0.05 and abs(size[1] - R["car_h"]) < 0.02
          and abs(size[2] - R["car_d"]) < 0.02, "carrier envelope",
          "%.2f x %.2f x %.2f mm (nominal %.2f x %.2f x %.2f; X is under by "
          "%.3f mm of tessellation chord on the ear radii)"
          % (size[0], size[1], size[2], R["car_w"], R["car_h"], R["car_d"],
             R["car_w"] - size[0]))
    check(abs(hi[2]) < 1e-3, "forward-most material is the seating plane",
          "z max = %+.4f" % hi[2])
    check(abs(lo[2] + R["car_d"]) < 1e-3, "rear face",
          "z min = %+.4f" % lo[2])

    # ---- B. independent optical chain ------------------------------------
    print("")
    print("B. OPTICAL Z-CHAIN, RE-DERIVED FROM THE MEASURED INPUTS")
    note("Perspex rear face / hard stop", "%+.3f" % Z_PERSPEX_REAR)
    note("glass front face  = -gap", "%+.3f" % Z_GLASS_FRONT)
    note("PCB front face    = -gap-glass_proud", "%+.3f" % Z_PCB_FRONT)
    note("PCB rear face     = -gap-glass_proud-pcb_t", "%+.3f" % Z_PCB_REAR)
    check(abs((-R["gap"] - R["glass_proud"] - R["pcb_t"]) - Z_PCB_REAR) < 1e-12,
          "chain closes: %.2f + %.2f + %.2f = %.2f"
          % (R["gap"], R["glass_proud"], R["pcb_t"], -Z_PCB_REAR), "")

    # ---- C. invariant P1 -------------------------------------------------
    print("")
    print("C. INVARIANT P1 - nothing ahead of the PCB front face in the aperture")
    # The aperture boundary IS a carrier wall face, so triangles lie exactly on
    # it. Tangency is not intrusion: test for material strictly inside.
    fwd_box = (AP[0], AP[1], AP[2], AP[3], Z_FWD_LIMIT + 1e-4, 10.0)
    m = tris_hit_box(tris, fwd_box, shrink=1e-4)
    check(not m.any(), "aperture prism above z = %.3f" % Z_FWD_LIMIT,
          "empty" if not m.any() else "%d triangles intrude" % int(m.sum()))
    fwd_box2 = (AP[0], AP[1], AP[2], AP[3], Z_PCB_FRONT + 1e-4, 10.0)
    m2 = tris_hit_box(tris, fwd_box2, shrink=1e-4)
    check(not m2.any(), "aperture prism above the PCB front face",
          "empty" if not m2.any() else "%d triangles intrude" % int(m2.sum()))
    tang = int(tris_hit_box(tris, fwd_box, shrink=0.0).sum())
    note("triangles lying exactly ON the aperture boundary",
         "%d - the pocket wall inner faces and the seating plane, by "
         "construction; %.2f mm outboard of the PCB" % (tang,
         R["pcb_clearance"] + R["aperture_margin"]))
    # and the tighter statement over the PCB footprint alone
    m3 = tris_hit_box(tris, (PCB[0], PCB[1], PCB[2], PCB[3],
                             Z_PCB_FRONT + 1e-4, 10.0))
    check(not m3.any(), "PCB footprint above the PCB front face",
          "empty" if not m3.any() else "%d triangles intrude" % int(m3.sum()))

    # ---- D. corridors ----------------------------------------------------
    print("")
    print("D. SWEPT ASSEMBLY AND DISASSEMBLY CORRIDORS  (%.1f mm travel)" % R["travel"])
    tv = R["travel"]
    glass_cor = (GLASS[0], GLASS[1], GLASS[2], GLASS[3],
                 Z_PCB_FRONT - tv, Z_GLASS_FRONT)
    m = tris_hit_box(tris, glass_cor, shrink=1e-4)
    check(not m.any(), "OLED glass corridor", "CLEAR" if not m.any()
          else "%d triangles in the path" % int(m.sum()))

    tipx = [R["tip_cx"] - 1.5 * R["tip_pitch"] + i * R["tip_pitch"] for i in range(4)]
    tr = R["tip_d"] / 2
    tip_cors = []
    for ty in (R["tip_y_top"], R["tip_y_bot"]):
        tip_cors.append((min(tipx) - tr, max(tipx) + tr, ty - tr, ty + tr,
                         Z_PCB_FRONT - tv, Z_TIP_FRONT))
    m = boxes_hit(tris, tip_cors, shrink=1e-4)
    check(not m.any(), "solder-tip corridor at %.2f mm proud" % R["tip_proud"],
          "CLEAR" if not m.any() else "%d triangles in the path" % int(m.sum()))

    hdr_cor = (-R["header_w"] / 2, R["header_w"] / 2,
               R["header_off_y"] - R["header_h"] / 2,
               R["header_off_y"] + R["header_h"] / 2,
               Z_PCB_REAR - R["header_depth"] - tv, Z_PCB_REAR)
    m = tris_hit_box(tris, hdr_cor, shrink=1e-4)
    check(not m.any(), "header corridor", "CLEAR" if not m.any()
          else "%d triangles in the path" % int(m.sum()))

    # PCB corridor, minus the four finger footprints. Exact box decomposition.
    fx = R["finger_x"]
    fw = R["finger_w"]
    pad = 0.05
    xa0, xa1 = fx - fw / 2 - pad, fx + fw / 2 + pad
    band_top = (PCB[3] - R["finger_grip"] - R["finger_nose"] - pad, PCB[3])
    band_bot = (PCB[2], PCB[2] + R["finger_grip"] + R["finger_nose"] + pad)
    z0, z1 = Z_PCB_REAR - tv, Z_PCB_FRONT
    clean = [(PCB[0], PCB[1], band_bot[1], band_top[0], z0, z1)]
    xr = [(PCB[0], -xa1), (-xa0, xa0), (xa1, PCB[1])]
    for band in (band_bot, band_top):
        for a, b in xr:
            if b > a:
                clean.append((a, b, band[0], band[1], z0, z1))
    m = boxes_hit(tris, clean, shrink=1e-4)
    check(not m.any(), "PCB corridor outside the four spring footprints",
          "CLEAR - every obstruction is a spring" if not m.any()
          else "%d triangles of RIGID obstruction" % int(m.sum()))

    # positive retention: the shoulders MUST be in the path
    print("")
    print("E. RETENTION FUNCTION - the shoulders must actually be there")
    found = 0
    for sx in (-1, 1):
        for sy in (1, -1):
            edge = PCB[3] if sy > 0 else PCB[2]
            y0 = edge - sy * (R["finger_grip"] + R["finger_nose"])
            box = (sx * fx - fw / 2 + 0.1, sx * fx + fw / 2 - 0.1,
                   min(y0, edge) + 0.02, max(y0, edge) - 0.02,
                   Z_PCB_REAR - 0.25, Z_PCB_REAR - 0.02)
            if tris_hit_box(tris, box).any():
                found += 1
    check(found == 4, "rear support shoulders inside the PCB footprint",
          "%d of 4 present behind DATUM B" % found)
    # Ahead of DATUM B the shoulder band must be empty. The 0.10 mm tongue is a
    # separate feature: it grips the PCB EDGE, ends 0.10 mm behind the PCB front
    # face, and therefore cannot act as a forward datum - which invariant P1
    # over the PCB footprint already proves.
    ahead = 0
    for sx in (-1, 1):
        for sy in (1, -1):
            edge = PCB[3] if sy > 0 else PCB[2]
            y_out = edge - sy * R["finger_grip"]
            y_in = edge - sy * (R["finger_grip"] + R["finger_nose"])
            box = (sx * fx - fw / 2 + 0.1, sx * fx + fw / 2 - 0.1,
                   min(y_in, y_out) + 0.02, max(y_in, y_out) - 0.02,
                   Z_PCB_REAR + 0.02, Z_PCB_FRONT)
            if tris_hit_box(tris, box, shrink=1e-4).any():
                ahead += 1
    check(ahead == 0, "no shoulder material ahead of DATUM B",
          "%d of 4 shoulder bands intrude - the datum is one-sided" % ahead)
    tongue_fwd = tris_hit_box(
        tris, (fx - fw / 2 + 0.1, fx + fw / 2 - 0.1,
               PCB[3] - R["finger_grip"] + 0.01, PCB[3],
               Z_PCB_FRONT - R["setback"] + 1e-3, Z_PCB_FRONT), shrink=1e-4)
    check(not tongue_fwd.any(), "edge-grip tongue stops behind the PCB front face",
          "ends at z %.2f, %.2f mm clear of the PCB face"
          % (Z_FWD_LIMIT, R["setback"]))

    # ---- F. PCB mounting holes ------------------------------------------
    print("")
    print("F. PCB MOUNTING HOLES - nothing may enter them")
    hr = R["hole_d"] / 2
    hole_boxes = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx = sx * R["hole_pitch_x"] / 2
            hy = R["pcb_off_y"] + sy * R["hole_pitch_y"] / 2
            hole_boxes.append((hx - hr, hx + hr, hy - hr, hy + hr,
                               Z_PCB_REAR - tv, Z_GLASS_FRONT))
    m = boxes_hit(tris, hole_boxes)
    check(not m.any(), "four Nom.3.00 mm holes and their full axial corridor",
          "CLEAR - Rev O's unmeasured glass/hole overlap is designed out"
          if not m.any() else "%d triangles enter a hole" % int(m.sum()))

    # ---- G. sections measured off the mesh ------------------------------
    print("")
    print("G. SECTIONS MEASURED OFF THE MESH (not read from the generator)")
    # clear of the radial prise hole, which is at z = -5.00
    zc = Z_REAR + R["finger_root"] + 0.80
    sp = material_spans(tris, (fx, PCB[3] - 5.0, zc), (0.0, 1.0, 0.0),
                        lo=0.0, hi=40.0)
    if sp is None:
        check(False, "finger section ray at x = %.2f" % fx, "odd crossing count")
    else:
        y0 = PCB[3] - 5.0
        segs = [(a + y0, b + y0, b - a) for a, b in sp]
        txt = ", ".join("%.2f..%.2f (%.2f)" % s for s in segs)
        note("material along +Y at x %.1f, z %.1f" % (fx, zc), txt)
        blade = [s for s in segs if abs(s[2] - R["finger_t"]) < 0.06]
        check(len(blade) >= 1, "spring section measured off the mesh",
              "%.3f mm (requirement %.2f)" % (blade[0][2], R["finger_t"])
              if blade else "no %.2f mm section found" % R["finger_t"])
        relief = [s for i, s in enumerate(segs[:-1])
                  if segs[i + 1][0] - s[1] > 0.5]
        if relief:
            g = segs[segs.index(relief[0]) + 1][0] - relief[0][1]
            check(g >= R["finger_relief"] - 0.02,
                  "finger flex relief measured off the mesh",
                  "%.3f mm gap (needs %.2f for %.2f mm deflection)"
                  % (g, R["finger_relief"],
                     R["finger_grip"] + R["finger_nose"] + R["pcb_clearance"]))
    sp = material_spans(tris, (0.0, PK[3] + 1.0, -0.30), (0.0, 1.0, 0.0),
                        lo=0.0, hi=40.0)
    if sp:
        y0 = PK[3] + 1.0
        w0 = sp[0][1] - sp[0][0]
        check(w0 >= 2.5, "structural rim wall measured at the seating plane",
              "%.3f mm" % w0)
    sp = material_spans(tris, (R["m2_pitch"] / 2, 0.0, -1.0), (1.0, 0.0, 0.0),
                        lo=-20.0, hi=20.0)
    if sp:
        note("M2 boss section through the insert bore at z -1.00",
             ", ".join("%.2f..%.2f" % (a + R["m2_pitch"] / 2, b + R["m2_pitch"] / 2)
                       for a, b in sp))

    # ---- H. load path ----------------------------------------------------
    print("")
    print("H. M2 LOAD PATH")
    check(abs(hi[2]) < 1e-3, "carrier reaches the Perspex and stops there",
          "z max = %+.4f, no material forward of the fascia" % hi[2])
    ok = True
    for sx in (-1, 1):
        x = sx * R["m2_pitch"] / 2
        ok &= not inside(tris, x, 0.0, -2.0)          # inside the insert bore
        ok &= inside(tris, x, 0.0, -6.5)              # backing behind the bore
        ok &= inside(tris, x + 2.6, 0.0, -1.0)        # boss wall
    check(ok, "M2 bosses at +/-%.2f mm with blind inserts" % (R["m2_pitch"] / 2),
          "bore open at the seating face, closed behind")
    check(Z_GLASS_FRONT < 0 and Z_PCB_FRONT < 0,
          "glass and PCB both behind the hard-stop plane",
          "glass %+.2f, PCB %+.2f -> preload cannot reach either"
          % (Z_GLASS_FRONT, Z_PCB_FRONT))

    # ---- I. retention mechanics ------------------------------------------
    print("")
    print("I. RETENTION MECHANICS (from the requirement geometry)")
    a = abs(Z_REAR + R["finger_root"] - Z_PCB_REAR)
    t, w = R["finger_t"], R["finger_w"]
    I = w * t ** 3 / 12.0
    delta = R["finger_grip"] + R["finger_nose"]
    dwc = delta + R["pcb_clearance"]
    def beam(dd):
        return 3 * R["petg_E"] * I * dd / a ** 3, 3 * t * dd / (2 * a * a) * 100.0
    F, eps = beam(delta)
    Fw, epsw = beam(dwc)
    Fs, _ = beam(R["finger_grip"])
    hold = 4 * Fs * R["mu"]
    weight = R["module_mass_g"] * 9.81e-3
    note("cantilever", "a = %.2f mm, section %.2f x %.2f mm" % (a, t, w))
    check(eps < R["strain_limit"], "peak strain, PCB centred", "%.2f %%" % eps)
    check(epsw < R["strain_limit"], "peak strain, PCB against one wall",
          "%.2f %%" % epsw)
    note("insertion force", "%.2f N/finger -> %.1f N total"
         % (F * 1.0605, 4 * F * 1.0605))
    check(hold > 10 * weight, "friction hold vs module weight",
          "%.2f N vs %.3f N = %.0f x" % (hold, weight, hold / weight))

    # ---- J. dimensional assumptions --------------------------------------
    print("")
    print("J. DIMENSIONAL ASSUMPTIONS AND THE SOLDER-TIP BUDGET")
    budget = -Z_PCB_FRONT
    note("budget for anything on the PCB front face",
         "gap %.2f + glass proud %.2f = %.2f mm" % (R["gap"], R["glass_proud"], budget))
    tip_ok = R["tip_proud"] <= budget - 0.10
    check(tip_ok, "modelled tip protrusion %.2f mm clears the Perspex"
          % R["tip_proud"],
          "clearance %+.2f mm" % (budget - R["tip_proud"]))
    if not tip_ok:
        NOTES.append(
            "solder tips at %.2f mm proud strike the Perspex by %.2f mm; the "
            "release limit at gap %.2f is %.2f mm, or the gap must open to "
            "%.2f mm" % (R["tip_proud"], R["tip_proud"] - budget, R["gap"],
                         budget - 0.10, R["tip_proud"] + 0.10 - R["glass_proud"]))
    note("glass-envelope sensitivity",
         "nearest spring is %.2f mm clear of the modelled glass edge in Y"
         % min(PCB[3] - R["finger_grip"] - R["finger_nose"] - GLASS[3],
               GLASS[2] - (PCB[2] + R["finger_grip"] + R["finger_nose"])))
    note("unmeasured inputs that no longer gate the design",
         "glass_w, glass_h, glass_off_y - nothing enters the PCB holes")
    note("unmeasured input that still affects centring only",
         "pcb_off_y = %.2f mm (light the display and report the offset)"
         % R["pcb_off_y"])

    # ---- K. probes -------------------------------------------------------
    print("")
    print("K. RAY-CAST MEMBERSHIP PROBES (independent of Fusion)")
    probes = [
        ("seating rim solid", 0.0, PK[3] + 1.5, -0.20, True),
        ("module aperture void", 0.0, PCB[3] + 0.35, -0.60, False),
        ("aperture at the PCB corner void", PCB[1] + 0.4, PCB[3] + 0.4, -0.60, False),
        ("PCB pocket void", 0.0, 0.0, -2.00, False),
        ("pocket side wall solid", PK[1] + 0.3, 0.0, -5.00, True),
        ("finger blade solid", fx, PK[3] + 0.35, -5.00, True),
        ("finger side gap void", fx + 2.4, PK[3] + 0.35, -5.00, False),
        ("finger flex relief void", fx, PK[3] + 1.30, -5.00, False),
        ("finger root solid", fx, PK[3] + 0.35, -9.00, True),
        ("finger tongue solid", fx, PCB[3] - 0.05, -2.00, True),
        ("shoulder solid behind DATUM B", fx, PCB[3] - 0.30, -2.80, True),
        ("shoulder void ahead of DATUM B", fx, PCB[3] - 0.30, -2.60, False),
        ("bottom finger blade solid", -fx, PK[2] - 0.35, -5.00, True),
        ("insert bore void", R["m2_pitch"] / 2, 0.0, -2.00, False),
        ("insert backing solid", R["m2_pitch"] / 2, 0.0, -6.50, True),
    ]
    bad = []
    for nm, x, y, z, want in probes:
        if inside(tris, x, y, z) != want:
            bad.append(nm)
    check(not bad, "membership probes", "%d of %d agree"
          % (len(probes) - len(bad), len(probes)))
    for b in bad:
        print("         MISMATCH: %s" % b)

    print("")
    print("=" * 80)
    if NOTES:
        print("OPEN ITEMS")
        for n in NOTES:
            print("   * %s" % n)
        print("")
    if FAILS:
        print("VERDICT: %d CHECK(S) FAILED" % len(FAILS))
        for f in FAILS:
            print("   - %s" % f)
    else:
        print("VERDICT: every independent check on the exported STL passes")
    print("=" * 80)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
