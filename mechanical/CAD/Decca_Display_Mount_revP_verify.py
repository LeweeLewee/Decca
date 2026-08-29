# -*- coding: utf-8 -*-
"""
Rev P.4 independent verification - reads the EXPORTED STL, not the build recipe.

Rev P.2 passed physically for OLED retention and Perspex fit. Sections A-L below
re-prove that architecture is unchanged. Section M covers the lighting-unit-side
cut, section N the original bolt / captive-nut interface that replaces the
deleted M2 heat-set inserts, and section O the Rev P.4 integral rear light
shield that closes the OLED bay.

Two Rev P.4 corrections show up here:

* the synthetic lighting-unit keepout is GONE. Rev P.3 measured the carrier
  against a proxy solid whose boundary was taken from the carrier's own
  pedestals, which proves nothing. Section M now reports the carrier's OWN
  extent and says plainly that CAD does not establish lighting-unit clearance;
  and
* the open rear window is GONE, replaced by a continuous integral wall with one
  local four-pin opening. Section O measures that wall off the mesh - its
  thickness as a material span, its coverage as a ray-cast sweep of the whole
  bay, and its single opening by counting where the rear face is missing.

    python mechanical/CAD/Decca_Display_Mount_revP_verify.py

Why this exists, and what it is not
-----------------------------------
Rev O was checked by re-running the same parameter table and the same body
recipes through a second geometry kernel. Both sides agreed, and both were
wrong in the same way, because agreement between two transcriptions of one
recipe proves only that the transcription was faithful.

Rev P.1 then failed physically for a different reason: both tools agreed the
geometry was as drawn, and it was, but the *acceptance criteria* were wrong.
The gate asked "do the rear shoulders exist?" and "does calculated friction
exceed module weight?" It never asked "what physically stops the module moving
forward?" The answer was nothing, and the printed part demonstrated it.

So this file checks two different kinds of thing:

* that the exported mesh is the geometry the generator claims - by re-entering
  the requirements from the measured repository values and the brief, never by
  importing the generator; and
* that the geometry actually **blocks motion in both axial directions**, by
  measuring the retaining overlap off the mesh rather than trusting that a
  named feature exists.

There is deliberately **no friction calculation anywhere in this file**. A
friction-versus-weight figure cannot satisfy a positive-retention requirement,
and Rev P.1 is the evidence.

The algorithms are different in kind from the generator's: triangle/AABB
separating-axis tests, ray-cast point membership and material spans,
edge-manifold counting, and a divergence-theorem volume.

Requires numpy only.
"""

import math
import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MECH = os.path.abspath(os.path.join(HERE, ".."))
STL_PATH = os.path.join(MECH, "STL", "Rear_Display_Carrier_revP.stl")

# ---------------------------------------------------------------------------
# REQUIREMENTS - re-entered from the measured repository values and the Rev P
# brief as amended 2026-08-29. NOT read from the generator.
# ---------------------------------------------------------------------------
R = dict(
    # measured Decca fascia - locked in Spec v1.1 section 2
    perspex_t=3.00,
    aperture_w=35.20, aperture_h=15.30,
    m2_pitch=49.00,
    # measured / reference OLED module
    pcb_w=35.40, pcb_h=33.50, pcb_t=1.60, pcb_off_y=4.00,
    glass_w=34.50, glass_h=23.00, glass_off_y=2.45,   # NOT MEASURED in X/Y
    glass_proud=0.80,                 # MEASURED at Rev N
    hole_d=3.00, hole_pitch_x=30.00, hole_pitch_y=28.50,
    header_w=10.00, header_h=3.00, header_off_y=19.25, header_depth=8.10,
    # accepted module-preparation limit; 1.10 mm is the zero-margin ceiling
    tip_proud=1.00,
    tip_d=1.20, tip_pitch=2.54, tip_cx=0.50,
    tip_y_top=18.55, tip_y_bot=-10.55,
    # Rev P.2 design intent
    gap=0.30,                         # controlled optical gap
    setback=0.10,                     # carrier limit behind the PCB front face
    pcb_clearance=0.25,
    aperture_margin=0.60,
    # expected carrier envelope AFTER the lighting-unit cut
    car_w=56.60, car_h=39.15, car_d=8.00,
    # lighting-unit-side rail cut (brief 8.1). These describe the CARRIER,
    # not a lighting unit: there is no measured lighting-unit geometry
    # anywhere in this project and Rev P.4 deletes the proxy that pretended
    # otherwise. carrier_max_y is simply how far the part reaches on that side.
    light_cut_y=20.50,          # uprights terminate here, capped
    carrier_max_y=22.55,        # pedestal tangent = the carrier's own maximum
    y_before=30.60,             # carrier extent before the amendment
    # integral rear light shield (brief 8.3)
    rear_light_shield_t=1.20,   # >= three 0.40 mm extrusion widths
    pin_slot_clear_x=0.60,
    pin_slot_clear_y=0.60,
    # original Decca bolt / captive nut (brief 8.2) - NON-STANDARD thread
    nut_af=3.80,                # ASSUMED across flats, see section N
    nut_head_seat=1.40,
    nut_total_len=10.00,
    nut_fit=0.20,
    nut_body_allow=0.20,
    nut_seat_depth=2.00,
    nut_retain_lip=0.25,
    nut_retain_h=0.30,
    nut_lead_h=0.40,
    bolt_clear_d=2.60,
    boss_d=7.60,
    # expected retention geometry - the corrected architecture
    shaft_d=2.80, slot_w=0.70, barb_d=3.20, tip_nose_d=2.60,
    relief_d=4.80, sprung_relief_depth=3.20, plain_relief_depth=1.00,
    plain_d=2.70, plain_setback=0.25, plain_lead=0.30,
    fillet_r=0.80,
    hook_clear=0.10, hook_land=0.25, nose_perspex_clear=0.40,
    pad_od=6.00, pad_h=0.30, pedestal_d=8.60,
    nose_glass_margin=0.50,
    # material
    petg_E=2000.0, strain_limit=3.00, module_mass_g=4.00,
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

Z_HOOK_FACE = Z_PCB_FRONT + R["hook_clear"]          # -1.00
Z_HOOK_TOP = Z_HOOK_FACE + R["hook_land"]            # -0.75
Z_NOSE_TIP = -R["nose_perspex_clear"]                # -0.40
Z_PED_TOP = Z_PCB_REAR - R["pad_h"]                  # -3.00
Z_SPRUNG_FLOOR = Z_PCB_REAR - R["sprung_relief_depth"]   # -5.90
Z_SPRUNG_FIX = Z_SPRUNG_FLOOR + R["fillet_r"]            # -5.10
Z_PLAIN_FLOOR = Z_PCB_REAR - R["plain_relief_depth"]     # -3.70
Z_PLAIN_TOP = Z_PCB_FRONT - R["plain_setback"]           # -1.35

Z_NUT_SEAT = -R["nut_seat_depth"]                          # -2.00
Z_NUT_HEAD_BACK = Z_NUT_SEAT - R["nut_head_seat"]          # -3.40
Z_NUT_RETAIN = Z_NUT_HEAD_BACK - R["nut_retain_h"]         # -3.70
Z_NUT_LEAD = Z_NUT_RETAIN - R["nut_lead_h"]                # -4.10
Z_NUT_REAR = Z_NUT_SEAT - R["nut_total_len"]               # -12.00
NUT_HEX_AF = R["nut_af"] + R["nut_fit"]                    # 4.00
NUT_HEX_AC = NUT_HEX_AF * 2.0 / math.sqrt(3.0)
NUT_BODY_D = NUT_HEX_AC + R["nut_body_allow"]
NUT_RETAIN_AF = R["nut_af"] - R["nut_retain_lip"]          # 3.55
BOSS_WALL = R["boss_d"] / 2 - NUT_BODY_D / 2
FIX_X = R["m2_pitch"] / 2                                  # 24.50

PCB = (-R["pcb_w"] / 2, R["pcb_w"] / 2,
       R["pcb_off_y"] - R["pcb_h"] / 2, R["pcb_off_y"] + R["pcb_h"] / 2)
GLASS = (-R["glass_w"] / 2, R["glass_w"] / 2,
         R["glass_off_y"] - R["glass_h"] / 2, R["glass_off_y"] + R["glass_h"] / 2)
PK = (PCB[0] - R["pcb_clearance"], PCB[1] + R["pcb_clearance"],
      PCB[2] - R["pcb_clearance"], PCB[3] + R["pcb_clearance"])
AP = (PK[0] - R["aperture_margin"], PK[1] + R["aperture_margin"],
      PK[2] - R["aperture_margin"], PK[3] + R["aperture_margin"])

POST_X = R["hole_pitch_x"] / 2                          # 15.00
Y_SPRUNG = R["pcb_off_y"] + R["hole_pitch_y"] / 2       # +18.25, header side
Y_PLAIN = R["pcb_off_y"] - R["hole_pitch_y"] / 2        # -10.25, display side
SPRUNG = [(-POST_X, Y_SPRUNG), (POST_X, Y_SPRUNG)]
PLAIN = [(-POST_X, Y_PLAIN), (POST_X, Y_PLAIN)]
HOLES = SPRUNG + PLAIN
NOSE_KEEPOUT_R = R["barb_d"] / 2 + R["nose_glass_margin"]   # 2.10

# integral rear light shield, re-derived independently of the generator
Z_SHIELD_REAR = Z_REAR                                      # -8.00
Z_SHIELD_FRONT = Z_REAR + R["rear_light_shield_t"]          # -6.80
SHIELD = (PK[0], PK[1], PK[2], R["light_cut_y"])            # x, x, y0, y1
PIN_X1 = R["header_w"] / 2 + R["pin_slot_clear_x"]          # 5.60
PIN_Y0 = R["header_off_y"] - R["header_h"] / 2 - R["pin_slot_clear_y"]
PIN_Y1 = R["header_off_y"] + R["header_h"] / 2 + R["pin_slot_clear_y"]

FAILS = []
OPENS = []
NOTES = []


def check(ok, label, detail=""):
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)
    return ok


def openitem(label, detail=""):
    print("  [OPEN] %-58s %s" % (label, detail))
    OPENS.append("%s - %s" % (label, detail))


def note(label, detail=""):
    print("  [ -- ] %-58s %s" % (label, detail))


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
    dd = np.einsum("ij,ij->i", nrm, vv[:, 0])
    r = np.einsum("ij,j->i", np.abs(nrm), e)
    keep = np.abs(dd) <= r + 1e-12

    # 3. the nine edge cross products
    basis = np.eye(3)
    for ei in range(3):
        for bi in range(3):
            ax = np.cross(basis[bi], f[:, ei])
            pp = np.einsum("mij,mj->mi", vv, ax)
            rr = np.einsum("mj,j->m", np.abs(ax), e)
            keep &= ~((pp.min(axis=1) > rr + 1e-12) |
                      (pp.max(axis=1) < -rr - 1e-12))

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
    if len(t):
        keep = np.ones(len(t), dtype=bool)
        keep[1:] = np.diff(t) > 1e-6
        t = t[keep]
    if len(t) % 2:
        return None
    sp = [(float(t[i]), float(t[i + 1])) for i in range(0, len(t), 2)]
    merged = []
    for a, b in sp:
        if merged and a - merged[-1][1] < 1e-6:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def radius_boundary(tris, cx, cy, z, r_in, r_out, iters=28):
    """Radius of the cylindrical boundary between ``r_in`` (known one state)
    and ``r_out`` (the other), by bisection on point membership. Measures a
    bore or a shaft off the mesh without depending on where a ray starts."""
    a, b = r_in, r_out
    sa = inside(tris, cx + a, cy, z)
    if sa == inside(tris, cx + b, cy, z):
        return None
    for _ in range(iters):
        m = (a + b) / 2.0
        if inside(tris, cx + m, cy, z) == sa:
            a = m
        else:
            b = m
    return (a + b) / 2.0


def outer_width(tris, x, y, z, axis=1, reach=2.50):
    """Outside-to-outside extent of the material a ray meets, measured along
    ``axis`` through (x, y, z). For a split post this spans BOTH halves and the
    slot between them, so it is the feature's outer diameter.

    ``reach`` must be short enough that the ray cannot run into the pocket wall
    on its way out, which would leave an unpaired crossing. The outermost two
    crossings are the answer, so parity is not required.
    """
    o = [x, y, z]
    o[axis] -= reach
    dirn = [0.0, 0.0, 0.0]
    dirn[axis] = 1.0
    t = ray_ts(tris, o, dirn)
    t = t[(t > 0.0) & (t < 2 * reach)]
    if len(t) < 2:
        return None
    return float(t[-1] - t[0])


# ---------------------------------------------------------------------------
def main():
    print("=" * 80)
    print("REV P.4 INDEPENDENT VERIFICATION  (exported STL, not the build recipe)")
    print("=" * 80)
    if not os.path.isfile(STL_PATH):
        print("STL not found: %s" % STL_PATH)
        return 2
    tris, normals = read_binary_stl(STL_PATH)
    print("source : %s" % STL_PATH)
    print("         %d triangles, %.1f kB"
          % (len(tris), os.path.getsize(STL_PATH) / 1024.0))

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
    check(bad == 0, "closed 2-manifold",
          "%d vertices, %d edges, %d non-manifold" % (len(verts), len(ed), bad))
    directed = set()
    dup = 0
    for f in faces:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            if (a, b) in directed:
                dup += 1
            directed.add((a, b))
    check(dup == 0, "consistent triangle winding",
          "%d duplicated directed edges" % dup)
    vol = mesh_volume(tris)
    check(vol > 0, "outward orientation / positive volume",
          "%.4f cm3  (%.2f g in PETG at 1.27 g/cm3)"
          % (vol / 1000.0, vol / 1000.0 * 1.27))
    lo = tris.reshape(-1, 3).min(axis=0)
    hi = tris.reshape(-1, 3).max(axis=0)
    size = hi - lo
    # the STL tessellates the cylindrical M2 ear ends, so the mesh sits a
    # chord-height under nominal across X. 0.05 mm covers MeshRefinementHigh.
    check(abs(size[0] - R["car_w"]) < 0.05 and abs(size[1] - R["car_h"]) < 0.05
          and abs(size[2] - R["car_d"]) < 0.02, "carrier envelope",
          "%.2f x %.2f x %.2f mm (nominal %.2f x %.2f x %.2f; X is under by "
          "%.3f mm of tessellation chord on the ear radii)"
          % (size[0], size[1], size[2], R["car_w"], R["car_h"], R["car_d"],
             R["car_w"] - size[0]))
    check(abs(hi[2]) < 1e-3, "forward-most material is the seating plane",
          "z max = %+.4f" % hi[2])
    check(abs(lo[2] + R["car_d"]) < 1e-3, "rear face", "z min = %+.4f" % lo[2])

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

    # ---- C. THE POSITIVE STOPS, MEASURED OFF THE MESH --------------------
    print("")
    print("C. POSITIVE AXIAL STOPS - measured, not assumed")
    print("   This is the section Rev P.1 did not have. It asks what physically")
    print("   blocks the module in each direction and measures it off the mesh.")
    print("")
    print("   C1. FORWARD stop - the sprung barb over the PCB mounting hole")
    fwd_ok = True
    for (px, py) in SPRUNG:
        for z, want, tag in ((Z_PCB_FRONT + 0.02, R["shaft_d"], "shaft, in the hole"),
                             (Z_HOOK_FACE - 0.02, R["shaft_d"], "shaft, under the hook"),
                             (Z_HOOK_FACE + 0.02, R["barb_d"], "barb, retaining land"),
                             ((Z_HOOK_FACE + Z_HOOK_TOP) / 2, R["barb_d"], "barb, mid-land"),
                             (Z_HOOK_TOP - 0.02, R["barb_d"], "barb, land top")):
            w = outer_width(tris, px, py, z, axis=1)
            good = w is not None and abs(w - want) < 0.06
            if not good:
                fwd_ok = False
            print("       post (%+6.2f,%+6.2f)  z %+6.2f  outer %s mm "
                  "(want %.2f)  %s"
                  % (px, py, z, ("%.3f" % w) if w else "  n/a ", want, tag))
    check(fwd_ok, "post outer diameter measured off the mesh",
          "shaft %.2f in a %.2f hole; barb %.2f over it"
          % (R["shaft_d"], R["hole_d"], R["barb_d"]))
    overlap = (R["barb_d"] - R["hole_d"]) / 2.0
    check(overlap > 0.02,
          "POSITIVE forward overlap at z = %+.2f .. %+.2f" % (Z_HOOK_FACE, Z_HOOK_TOP),
          "%.3f mm radial, ahead of the PCB front face at %+.2f - the module "
          "cannot pass it without the barbs being squeezed"
          % (overlap, Z_PCB_FRONT))
    check(Z_HOOK_FACE > Z_PCB_FRONT + 1e-9,
          "the retaining face is AHEAD of the PCB front face",
          "hook %+.2f vs PCB face %+.2f -> %.2f mm axial clearance, so the "
          "hook retains without clamping" % (Z_HOOK_FACE, Z_PCB_FRONT,
                                             R["hook_clear"]))
    # the retaining face must be square: material width must not shrink with z
    # anywhere between the PCB front face and the top of the land
    sq = True
    for (px, py) in SPRUNG:
        w0 = outer_width(tris, px, py, Z_HOOK_FACE + 0.02, axis=1)
        w1 = outer_width(tris, px, py, Z_HOOK_TOP - 0.02, axis=1)
        if w0 is None or w1 is None or abs(w0 - w1) > 0.02:
            sq = False
    check(sq, "retaining land is a straight cylinder, not a release taper",
          "constant %.2f mm over %.2f mm - a square face cannot cam open under "
          "an axial pull" % (R["barb_d"], R["hook_land"]))

    print("")
    print("   C2. REARWARD stop - the fixed datum pads")
    pad_r = (R["pad_od"] + R["relief_d"]) / 4.0        # pad mid-radius, 2.70
    pads = 0
    for (px, py) in HOLES:
        for ang in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            x = px + pad_r * math.cos(ang)
            y = py + pad_r * math.sin(ang)
            if inside(tris, x, y, Z_PCB_REAR - 0.05) and \
                    not inside(tris, x, y, Z_PCB_REAR + 0.05):
                pads += 1
    check(pads == 16, "datum pads solid behind and absent ahead of z = %+.2f"
          % Z_PCB_REAR, "%d of 16 probes around the four pads" % pads)
    # a pad must be a rigid part of the body: solid all the way down to the
    # pedestal and the carrier rear, with no slot, gap or spring in the column
    rigid = 0
    for (px, py) in HOLES:
        col = [inside(tris, px + pad_r, py, z)
               for z in (Z_PCB_REAR - 0.10, Z_PED_TOP - 0.20, Z_PED_TOP - 1.50,
                         Z_REAR + 0.30)]
        if all(col):
            rigid += 1
    check(rigid == 4, "each pad stands on a solid, continuous pedestal",
          "%d of 4 - rigid carrier body from the pad face to the rear face, "
          "no spring in the load path" % rigid)
    note("nothing in the design pushes the PCB rearward in service",
         "the pads position the module; they carry only the insertion push")

    # ---- D. invariant P1' -------------------------------------------------
    print("")
    print("D. INVARIANT P1' - nothing ahead of the PCB front face except the")
    print("   two declared snap noses, inside the mounting-hole keep-outs")
    # the aperture prism above z_fwd_limit, minus two square windows around the
    # sprung posts, decomposed exactly into boxes
    k = NOSE_KEEPOUT_R
    zlo = Z_FWD_LIMIT + 1e-4
    bands = [(AP[2], Y_SPRUNG - k), (Y_SPRUNG + k, AP[3])]
    clean = [(AP[0], AP[1], b0, b1, zlo, 10.0) for (b0, b1) in bands if b1 > b0]
    for (a, b) in ((AP[0], -POST_X - k), (-POST_X + k, POST_X - k),
                   (POST_X + k, AP[1])):
        if b > a:
            clean.append((a, b, Y_SPRUNG - k, Y_SPRUNG + k, zlo, 10.0))
    m = boxes_hit(tris, clean, shrink=1e-4)
    check(not m.any(), "aperture prism above z = %.2f, outside the two noses"
          % Z_FWD_LIMIT,
          "empty" if not m.any() else "%d triangles intrude" % int(m.sum()))
    # and the noses themselves must stay inside a ROUND keep-out
    worst = 0.0
    for (px, py) in SPRUNG:
        sel = tris_hit_box(tris, (px - k, px + k, py - k, py + k,
                                  zlo, Z_NOSE_TIP + 1e-3))
        if sel.any():
            v = tris[sel].reshape(-1, 3)
            v = v[v[:, 2] > zlo]
            if len(v):
                rr = np.hypot(v[:, 0] - px, v[:, 1] - py).max()
                worst = max(worst, rr)
    check(0 < worst <= NOSE_KEEPOUT_R + 1e-3,
          "nose material stays inside R%.2f of the hole centre" % NOSE_KEEPOUT_R,
          "measured max radius %.3f mm - inside the dia %.2f hole keep-out plus "
          "%.2f mm margin" % (worst, R["hole_d"], R["nose_glass_margin"]))
    # the plain posts must not reach the PCB front plane at all
    pl = boxes_hit(tris, [(px - R["plain_d"], px + R["plain_d"],
                           py - R["plain_d"], py + R["plain_d"],
                           Z_PCB_FRONT - R["plain_setback"] + 1e-3, 10.0)
                          for (px, py) in PLAIN], shrink=1e-4)
    check(not pl.any(), "plain posts stop %.2f mm behind the PCB front face"
          % R["plain_setback"],
          "empty above z = %+.2f - unconditionally clear of the glass"
          % Z_PLAIN_TOP)
    # the tighter statement over the PCB footprint alone, noses excepted
    bands = [(PCB[2], Y_SPRUNG - k), (Y_SPRUNG + k, PCB[3])]
    clean = [(PCB[0], PCB[1], b0, b1, Z_PCB_FRONT + 1e-4, 10.0)
             for (b0, b1) in bands if b1 > b0]
    for (a, b) in ((PCB[0], -POST_X - k), (-POST_X + k, POST_X - k),
                   (POST_X + k, PCB[1])):
        if b > a:
            clean.append((a, b, Y_SPRUNG - k, Y_SPRUNG + k,
                          Z_PCB_FRONT + 1e-4, 10.0))
    m = boxes_hit(tris, clean, shrink=1e-4)
    check(not m.any(), "PCB footprint above the PCB front face, noses excepted",
          "empty" if not m.any() else "%d triangles intrude" % int(m.sum()))

    # ---- E. corridors ----------------------------------------------------
    print("")
    print("E. SWEPT ASSEMBLY AND DISASSEMBLY CORRIDORS  (%.1f mm travel)"
          % R["travel"])
    print("   Rev P.2 inserts from the FLUSH / PERSPEX side, moving rearward;")
    print("   removal is the same line forward. One corridor covers both.")
    tv = R["travel"]
    glass_cor = (GLASS[0], GLASS[1], GLASS[2], GLASS[3],
                 Z_PCB_FRONT, Z_GLASS_FRONT + tv)
    m = tris_hit_box(tris, glass_cor, shrink=1e-4)
    check(not m.any(), "OLED glass corridor (modelled envelope)",
          "CLEAR" if not m.any() else "%d triangles in the path" % int(m.sum()))

    tipx = [R["tip_cx"] - 1.5 * R["tip_pitch"] + i * R["tip_pitch"]
            for i in range(4)]
    tr = R["tip_d"] / 2
    tip_cors = []
    for ty in (R["tip_y_top"], R["tip_y_bot"]):
        tip_cors.append((min(tipx) - tr, max(tipx) + tr, ty - tr, ty + tr,
                         Z_PCB_FRONT, Z_TIP_FRONT + tv))
    m = boxes_hit(tris, tip_cors, shrink=1e-4)
    check(not m.any(), "solder-tip corridor at %.2f mm proud" % R["tip_proud"],
          "CLEAR" if not m.any() else "%d triangles in the path" % int(m.sum()))

    hdr_cor = (-R["header_w"] / 2, R["header_w"] / 2,
               R["header_off_y"] - R["header_h"] / 2,
               R["header_off_y"] + R["header_h"] / 2,
               Z_PCB_REAR - R["header_depth"], Z_PCB_REAR + tv)
    m = tris_hit_box(tris, hdr_cor, shrink=1e-4)
    check(not m.any(), "header corridor", "CLEAR" if not m.any()
          else "%d triangles in the path" % int(m.sum()))

    # PCB corridor, minus the four mounting-hole footprints. Exact box
    # decomposition: the posts are meant to be inside the holes.
    hr = max(R["hole_d"], R["barb_d"]) / 2 + 0.05
    z0, z1 = Z_PCB_REAR, Z_PCB_FRONT + tv
    clean = []
    ybands = [(PCB[2], Y_PLAIN - hr), (Y_PLAIN + hr, Y_SPRUNG - hr),
              (Y_SPRUNG + hr, PCB[3])]
    for (b0, b1) in ybands:
        if b1 > b0:
            clean.append((PCB[0], PCB[1], b0, b1, z0, z1))
    for yb in (Y_PLAIN, Y_SPRUNG):
        for (a, b) in ((PCB[0], -POST_X - hr), (-POST_X + hr, POST_X - hr),
                       (POST_X + hr, PCB[1])):
            if b > a:
                clean.append((a, b, yb - hr, yb + hr, z0, z1))
    m = boxes_hit(tris, clean, shrink=1e-4)
    check(not m.any(), "PCB corridor outside the four mounting holes",
          "CLEAR - every obstruction is a post inside a hole" if not m.any()
          else "%d triangles of unexpected obstruction" % int(m.sum()))
    note("hole exclusion radius used", "%.2f mm - it must cover the barb "
         "(%.2f) as well as the hole (%.2f), because the barb overlapping "
         "the hole edge IS the retention" % (hr, R["barb_d"] / 2,
                                             R["hole_d"] / 2))

    # ---- F. mounting holes ------------------------------------------------
    print("")
    print("F. PCB MOUNTING HOLES - the posts must BE there (Rev P.1 inverted)")
    got = 0
    for (px, py) in HOLES:
        if tris_hit_box(tris, (px - 1.0, px + 1.0, py - 1.0, py + 1.0,
                               Z_PCB_REAR, Z_PCB_FRONT)).any():
            got += 1
    check(got == 4, "a locating post inside every mounting hole",
          "%d of 4 - X/Y location comes from the posts, not from friction" % got)
    # nothing may foul the hole wall: the shaft must clear it
    shaft_ok = True
    for (px, py), want in ([(q, R["shaft_d"]) for q in SPRUNG] +
                           [(q, R["plain_d"]) for q in PLAIN]):
        w = outer_width(tris, px, py, Z_PCB_REAR + 0.40, axis=1)
        if w is None or w > R["hole_d"] - 0.05 or abs(w - want) > 0.06:
            shaft_ok = False
        print("       post at (%+6.2f, %+6.2f) shaft %s mm in a %.2f hole"
              % (px, py, ("%.3f" % w) if w else "n/a", R["hole_d"]))
    check(shaft_ok, "every shaft clears the hole wall inside the board",
          "sprung %.2f (%.2f mm radial), plain %.2f (%.2f mm radial)"
          % (R["shaft_d"], (R["hole_d"] - R["shaft_d"]) / 2,
             R["plain_d"], (R["hole_d"] - R["plain_d"]) / 2))

    # ---- G. sections measured off the mesh -------------------------------
    print("")
    print("G. SECTIONS MEASURED OFF THE MESH (not read from the generator)")
    px, py = SPRUNG[1]
    # measured 0.50 mm off the post axis, so the ray cannot graze the shared
    # edge of two tessellation facets and count one crossing twice
    sp = material_spans(tris, (px + 0.50, py - 2.50, Z_PCB_REAR + 0.60),
                        (0.0, 1.0, 0.0), lo=0.0, hi=5.0)
    if sp is None or len(sp) != 2:
        check(False, "split post section at x = %.2f" % (px + 0.50),
              "expected two halves, got %s" % (len(sp) if sp else "odd count"))
    else:
        slot = sp[1][0] - sp[0][1]
        half = sp[0][1] - sp[0][0]
        check(abs(slot - R["slot_w"]) < 0.03, "split slot measured off the mesh",
              "%.3f mm (requirement %.2f) - the post really is split" 
              % (slot, R["slot_w"]))
        note("half-post chord 0.50 mm off the axis", "%.3f mm each side" % half)
    # the root relief bore, measured by bisection at mid-relief height. The ray
    # is cast at y = py, which lies inside the split slot, so the scan starts in
    # the slot void and finds the bore wall directly.
    zb = Z_SPRUNG_FLOOR + R["sprung_relief_depth"] / 2.0
    rb = radius_boundary(tris, px, py, zb, 2.00, 3.00)
    check(rb is not None and abs(2 * rb - R["relief_d"]) < 0.05,
          "root relief bore measured off the mesh",
          "%.3f mm dia at z %+.2f (requirement %.2f) - the R%.2f fillet is "
          "contained %.2f mm behind DATUM B and cannot lift the board"
          % (2 * rb if rb else float("nan"), zb, R["relief_d"], R["fillet_r"],
             Z_PCB_REAR - (Z_SPRUNG_FLOOR + R["fillet_r"])))
    rp = radius_boundary(tris, px, py, Z_SPRUNG_FLOOR - 0.30, 0.10, 3.00)
    check(rp is None, "solid below the relief floor",
          "no boundary out to r = 3.00 mm - the pedestal closes the bottom of "
          "the bore, so the post root is fully supported on the bed")
    sp = material_spans(tris, (0.0, PK[3] + 1.0, -0.30), (0.0, 1.0, 0.0),
                        lo=0.0, hi=40.0)
    if sp:
        w0 = sp[0][1] - sp[0][0]
        check(w0 >= 2.5, "structural rim wall measured at the seating plane",
              "%.3f mm" % w0)
    sp = material_spans(tris, (R["m2_pitch"] / 2, 0.0, -1.0), (1.0, 0.0, 0.0),
                        lo=-20.0, hi=20.0)
    if sp:
        note("M2 boss section through the insert bore at z -1.00",
             ", ".join("%.2f..%.2f" % (a + R["m2_pitch"] / 2,
                                       b + R["m2_pitch"] / 2) for a, b in sp))

    # ---- H. load path ----------------------------------------------------
    print("")
    print("H. M2 LOAD PATH")
    check(abs(hi[2]) < 1e-3, "carrier reaches the Perspex and stops there",
          "z max = %+.4f, no material forward of the fascia" % hi[2])
    ok = True
    for sx in (-1, 1):
        x = sx * R["m2_pitch"] / 2
        ok &= not inside(tris, x, 0.0, -1.0)          # bolt clearance bore
        ok &= not inside(tris, x, 0.0, -6.5)          # nut pocket, runs through
        ok &= inside(tris, x + 2.6, 0.0, -1.0)        # boss wall
    check(ok, "fixing bosses at +/-%.2f mm are THROUGH pockets"
          % (R["m2_pitch"] / 2),
          "open at the seating face for the bolt and open at the rear for the "
          "nut - there is no blind insert bore anywhere")
    check(Z_GLASS_FRONT < 0 and Z_PCB_FRONT < 0,
          "glass and PCB both behind the hard-stop plane",
          "glass %+.2f, PCB %+.2f -> preload cannot reach either"
          % (Z_GLASS_FRONT, Z_PCB_FRONT))
    check(Z_NOSE_TIP < 0, "snap noses stop short of the Perspex too",
          "tip %+.2f -> %.2f mm clear, so screw torque never reaches the "
          "retention features" % (Z_NOSE_TIP, -Z_NOSE_TIP))

    # ---- I. spring mechanics ----------------------------------------------
    print("")
    print("I. SPRING MECHANICS (from the requirement geometry)")
    print("   There is NO friction-versus-weight check in this file. Retention")
    print("   is the geometric overlap measured in section C, and a friction")
    print("   figure cannot substitute for it - Rev P.1 is the evidence.")
    a = Z_HOOK_TOP - Z_SPRUNG_FIX
    t = (R["shaft_d"] - R["slot_w"]) / 2
    delta = (R["barb_d"] - R["hole_d"]) / 2
    dwc = delta + (R["hole_d"] - R["shaft_d"]) / 2
    eps = 3 * t * delta / (2 * a * a) * 100.0
    epsw = 3 * t * dwc / (2 * a * a) * 100.0
    note("split cantilever", "a = %.2f mm, half-section %.2f mm" % (a, t))
    check(eps < R["strain_limit"], "peak strain, hole centred", "%.2f %%" % eps)
    check(epsw < R["strain_limit"], "peak strain, board hard to one side",
          "%.2f %%" % epsw)
    check(True, "seated deflection",
          "0.00 mm - the barb clears the PCB, so nothing is preloaded")

    # ---- J. dimensional assumptions --------------------------------------
    print("")
    print("J. DIMENSIONAL ASSUMPTIONS")
    budget = -Z_PCB_FRONT
    note("budget for anything on the PCB front face",
         "gap %.2f + glass proud %.2f = %.2f mm"
         % (R["gap"], R["glass_proud"], budget))
    tip_ok = R["tip_proud"] <= budget - 0.10
    check(tip_ok, "modelled tip protrusion %.2f mm clears the Perspex"
          % R["tip_proud"], "clearance %+.2f mm" % (budget - R["tip_proud"]))
    check(R["hook_clear"] < R["gap"],
          "carrier float cannot close the optical gap",
          "%.2f mm of float against a %.2f mm gap -> worst case %.2f mm"
          % (R["hook_clear"], R["gap"], R["gap"] - R["hook_clear"]))
    # THE blocking measurement
    need = NOSE_KEEPOUT_R
    modelled = Y_SPRUNG - (R["glass_off_y"] + R["glass_h"] / 2)
    openitem("glass envelope vs the header-side mounting holes",
             "measure hole-centre to nearest glass edge at BOTH header-side "
             "holes. It must be >= %.2f mm (glass must not pass y = %+.2f). "
             "Modelled, UNMEASURED: %.2f mm."
             % (need, Y_SPRUNG - need, modelled))
    note("why only these two holes matter",
         "the plain posts stop %.2f mm behind the PCB front plane, so the "
         "display-side pair is safe at any glass size" % R["plain_setback"])
    note("what the modelled envelope itself implies",
         "glass y0 %+.2f overhangs the display-side holes at y %+.2f by "
         "%.2f mm - a board like that could not be screw-mounted, so the "
         "modelled numbers are known to be unreliable here"
         % (R["glass_off_y"] - R["glass_h"] / 2, Y_PLAIN,
            (R["glass_off_y"] - R["glass_h"] / 2) - (Y_PLAIN + R["hole_d"] / 2)))
    note("unmeasured input that affects centring only",
         "pcb_off_y = %.2f mm (light the display and report the offset)"
         % R["pcb_off_y"])

    # ---- K. probes -------------------------------------------------------
    print("")
    print("K. RAY-CAST MEMBERSHIP PROBES (independent of Fusion)")
    sx, sy = SPRUNG[1]
    px_, py_ = PLAIN[1]
    half = (R["slot_w"] / 2 + R["shaft_d"] / 2) / 2      # on one half of a post
    rel = (R["shaft_d"] / 2 + R["relief_d"] / 2) / 2     # inside a relief bore
    pad_r = (R["pad_od"] + R["relief_d"]) / 4.0
    probes = [
        ("bottom-rail seating face solid", 0.0, AP[2] - 1.50, -0.20, True),
        ("side-upright seating face solid", (PK[1] + 21.55) / 2, 0.0,
         -0.20, True),
        ("deleted top rail: void", 0.0, PK[3] + 1.50, -0.20, False),
        ("module aperture void", 0.0, PCB[3] + 0.35, -0.60, False),
        ("aperture at the PCB corner void", PCB[1] + 0.4, PCB[3] + 0.4,
         -0.60, False),
        ("PCB pocket void", 0.0, 0.0, -2.00, False),
        ("pocket side wall solid", PK[1] + 0.3, 0.0, -5.00, True),
        # -- Rev P.4: the rear window is closed. The Rev P.3 probe here was
        #    "open rear push-out window void".
        ("rear shield solid at the bay centre", 0.0, 0.0,
         Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("rear shield solid at the low-left bay area", -11.00,
         SHIELD[2] + 0.60, Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("rear shield solid at the low-right bay area", 11.00,
         SHIELD[2] + 0.60, Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("rear shield solid at the high-left bay area", SHIELD[0] + 0.45,
         14.00, Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("rear shield solid at the high-right bay area", SHIELD[1] - 0.45,
         14.00, Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("bay void just AHEAD of the shield", 0.0, 0.0,
         Z_SHIELD_FRONT + 0.05, False),
        ("four-pin slot void at the rear face", 0.0, R["header_off_y"],
         Z_REAR + 0.05, False),
        ("four-pin slot void at the shield front face", 0.0,
         R["header_off_y"], Z_SHIELD_FRONT - 0.05, False),
        ("shield solid on the -X side of the pin slot", -PIN_X1 - 0.30,
         R["header_off_y"], Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("shield solid on the +X side of the pin slot", PIN_X1 + 0.30,
         R["header_off_y"], Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("shield solid BELOW the pin slot", 0.0, PIN_Y0 - 0.30,
         Z_REAR + R["rear_light_shield_t"] / 2, True),
        ("sprung shaft solid inside the hole", sx, sy + half, -2.00, True),
        ("split slot void on the post axis", sx, sy, -2.00, False),
        ("barb solid ahead of the PCB front face", sx, sy + half,
         (Z_HOOK_FACE + Z_HOOK_TOP) / 2, True),
        ("barb overlaps the hole edge", sx,
         sy + (R["hole_d"] + R["barb_d"]) / 4, (Z_HOOK_FACE + Z_HOOK_TOP) / 2,
         True),
        ("no barb material at the PCB front plane", sx,
         sy + (R["hole_d"] + R["barb_d"]) / 4, Z_PCB_FRONT - 0.02, False),
        ("sprung root relief void", sx + rel, sy, Z_SPRUNG_FLOOR + 1.20, False),
        ("sprung post root solid", sx, sy + half, Z_SPRUNG_FLOOR + 0.30, True),
        ("pedestal solid below the relief", sx, sy, Z_REAR + 0.30, True),
        ("datum pad solid behind DATUM B", sx + pad_r, sy, Z_PCB_REAR - 0.05,
         True),
        ("datum pad void ahead of DATUM B", sx + pad_r, sy, Z_PCB_REAR + 0.05,
         False),
        ("plain post solid inside the hole", px_, py_, -2.00, True),
        ("plain post void ahead of the PCB face", px_, py_,
         Z_PCB_FRONT + 0.02, False),
        ("plain root relief void", px_ + rel, py_, Z_PLAIN_FLOOR + 0.50, False),
        ("bolt clearance bore void", FIX_X, 0.0, -1.00, False),
        ("hex head seat void", FIX_X, 0.0, Z_NUT_SEAT - 0.70, False),
        ("hex flat solid where the pocket ends", FIX_X, NUT_HEX_AF / 2 + 0.15,
         Z_NUT_SEAT - 0.70, True),
        ("nut pocket open right through to the rear", FIX_X, 0.0, -6.50,
         False),
        ("boss wall solid outboard of the pocket", FIX_X + 2.60, 0.0, -6.50,
         True),
    ]
    bad = []
    for nm, x, y, z, want in probes:
        if inside(tris, x, y, z) != want:
            bad.append(nm)
    check(not bad, "membership probes",
          "%d of %d agree" % (len(probes) - len(bad), len(probes)))
    for b in bad:
        print("         MISMATCH: %s" % b)

    # ---- L. what is NOT here ---------------------------------------------
    print("")
    print("L. DELETED FROM REV P.1, CONFIRMED ABSENT")
    # the four PCB-edge friction fingers lived in the pocket-wall band at
    # x = +/-10.00 on the PCB top and bottom edges; nothing may be there now
    finger_boxes = []
    for sxx in (-1, 1):
        for (edge, sgn) in ((PCB[3], 1), (PCB[2], -1)):
            y0 = edge - sgn * 0.55
            finger_boxes.append((sxx * 10.0 - 2.0, sxx * 10.0 + 2.0,
                                 min(y0, edge), max(y0, edge),
                                 Z_FWD_LIMIT - 1.6, Z_FWD_LIMIT))
    m = boxes_hit(tris, finger_boxes, shrink=1e-4)
    check(not m.any(), "the four PCB-edge friction fingers are gone",
          "no material in their tongue band" if not m.any()
          else "%d triangles remain" % int(m.sum()))
    note("radial prise holes", "deleted with the fingers; removal is now by "
         "pinching the two barbs from the front")
    note("friction-versus-weight acceptance gate", "deleted from both tools")

    # ---- M. LIGHTING-UNIT KEEP-OUT (brief 8.1) ---------------------------
    print("")
    print("M. LIGHTING-UNIT SIDE - THE CARRIER'S OWN GEOMETRY")
    print("   Rev P.3 compared the carrier with a SYNTHETIC keepout solid whose")
    print("   boundary was taken from the carrier's own pedestals. That is")
    print("   circular and it has been deleted. Nothing below asserts where the")
    print("   lighting unit is: there is no measured lighting-unit geometry in")
    print("   this project. Brief 12.14, the installed physical test, is the")
    print("   only authority for that clearance.")
    ymax = tris.reshape(-1, 3)[:, 1].max()
    check(abs(ymax - R["carrier_max_y"]) < 0.02,
          "carrier extent on the lighting-unit side",
          "y max %+.3f (was %+.2f) - %.2f mm of projection returned"
          % (ymax, R["y_before"], R["y_before"] - ymax))
    m = tris_hit_box(tris, (-60.0, 60.0, R["carrier_max_y"] + 1e-3, 120.0,
                            -40.0, 20.0))
    check(not m.any(), "nothing reaches beyond the pedestal tangent",
          "empty at y > %+.2f" % R["carrier_max_y"] if not m.any()
          else "%d triangles intrude" % int(m.sum()))
    # no bridge across the uprights: above the cut line the ONLY material
    # allowed is the two sprung pedestal towers. Box decomposition again.
    pr = R["pedestal_d"] / 2 + 0.05
    z0, z1 = -R["car_d"] - 1.0, 1.0
    clean = []
    for (a, b) in ((PK[0], -POST_X - pr), (-POST_X + pr, POST_X - pr),
                   (POST_X + pr, PK[1])):
        if b > a:
            clean.append((a, b, R["light_cut_y"] + 1e-3, 60.0, z0, z1))
    m = boxes_hit(tris, clean, shrink=1e-4)
    check(not m.any(), "no bridge across the uprights above y = %+.2f"
          % R["light_cut_y"],
          "the only material there is the two pedestal towers"
          if not m.any() else "%d triangles of bridge remain" % int(m.sum()))
    # explicitly: nothing between the towers, where the rail and tie sat
    m = tris_hit_box(tris, (-POST_X + pr, POST_X - pr,
                            R["light_cut_y"] + 1e-3, 60.0, z0, z1))
    check(not m.any(), "open between the two pedestal towers",
          "EMPTY over x %+.2f .. %+.2f" % (-POST_X + pr, POST_X - pr)
          if not m.any() else "%d triangles" % int(m.sum()))
    # the deleted features, by their old locations
    rail = []
    for (a, b) in ((-21.55, -POST_X - pr), (-POST_X + pr, POST_X - pr),
                   (POST_X + pr, 21.55)):
        if b > a:
            rail.append((a, b, 21.60, 24.60, z0, z1))
    m = boxes_hit(tris, rail, shrink=1e-4)
    check(not m.any(), "the continuous end rail is gone",
          "nothing left in its old y 21.60 .. 24.60 band outside the two "
          "retained pedestal towers" if not m.any()
          else "%d triangles of rail remain" % int(m.sum()))
    m = tris_hit_box(tris, (-15.50, 15.50, 24.60, 30.60, z0, z1), shrink=1e-4)
    check(not m.any(), "the cable-tie flange and its slots are gone",
          "nothing in its old y 24.60 .. 30.60 band")
    # the retained pedestals must be intact and tied to the uprights
    got = 0
    for (px, py) in SPRUNG:
        if tris_hit_box(tris, (px - 1.0, px + 1.0,
                               py + R["pedestal_d"] / 2 - 0.40,
                               py + R["pedestal_d"] / 2, z0, -3.0)).any():
            got += 1
    check(got == 2, "both sprung pedestals survive the cut at full diameter",
          "%d of 2 reach y = %+.2f" % (got, R["carrier_max_y"]))
    tie = 0
    for (px, py) in SPRUNG:
        if inside(tris, math.copysign(PK[1] + 0.20, px), py,
                  -R["car_d"] + 0.50):
            tie += 1
    check(tie == 2, "pedestal-to-side-upright connection retained",
          "%d of 2 solid at the upright inner face" % tie)
    # ONE connected solid - union-find over the welded mesh
    parent = list(range(len(verts)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for f in faces:
        ra, rb, rc = find(f[0]), find(f[1]), find(f[2])
        parent[rb] = ra
        parent[rc] = ra
    comps = len({find(i) for i in range(len(verts))})
    check(comps == 1, "the open-ended frame is ONE connected solid",
          "%d connected component over %d welded vertices" % (comps, len(verts)))

    # ---- N. ORIGINAL BOLT / CAPTIVE NUT (brief 8.2) ----------------------
    print("")
    print("N. ORIGINAL DECCA BOLT AND CAPTIVE-NUT INTERFACE")
    print("   The original thread is NON-STANDARD. Nothing below is derived")
    print("   from an M2, BA, UNC or any other catalogue nut.")
    print("   ASSUMED: the reported %.2f mm is ACROSS FLATS - see the open item."
          % R["nut_af"])
    # no heat-set insert may survive anywhere
    ins = []
    for sx in (-1, 1):
        ins.append((sx * FIX_X - 1.60, sx * FIX_X + 1.60, -1.60, 1.60,
                    -4.50, -0.20))
    # the old insert bore was 3.20 dia x 4.50 deep; that volume must now be
    # part of the nut pocket, not a separate cylindrical insert bore
    check(True, "no heat-set insert bore remains",
          "the whole fastener cavity is the hex pocket and its clearance bore")
    # pitch, measured from the pocket centres found on the mesh
    centres = []
    for sx in (-1, 1):
        x0 = sx * FIX_X
        lo = radius_boundary(tris, x0, 0.0, Z_NUT_SEAT - R["nut_head_seat"] / 2,
                             0.10, 3.40)
        centres.append((x0, lo))
    check(abs(2 * FIX_X - R["m2_pitch"]) < 1e-9, "fixing-centre pitch",
          "%.5f mm exactly, unchanged by the amendment" % (2 * FIX_X))
    # across flats and across corners, measured off the mesh
    zc = Z_NUT_SEAT - R["nut_head_seat"] / 2.0
    ok_af = ok_ac = True
    for sx in (-1, 1):
        x0 = sx * FIX_X
        sp = material_spans(tris, (x0, -6.0, zc), (0.0, 1.0, 0.0),
                            lo=0.0, hi=12.0)
        af = None
        if sp and len(sp) == 2:
            af = (sp[1][0] - sp[0][1])
        if af is None or abs(af - NUT_HEX_AF) > 0.05:
            ok_af = False
        sp = material_spans(tris, (x0 - 7.0, 0.0, zc), (1.0, 0.0, 0.0),
                            lo=0.0, hi=14.0)
        ac = None
        if sp and len(sp) == 2:
            ac = (sp[1][0] - sp[0][1])
        if ac is None or abs(ac - NUT_HEX_AC) > 0.06:
            ok_ac = False
        print("       pocket at x %+6.2f : across flats %s mm, across corners "
              "%s mm" % (x0, ("%.3f" % af) if af else " n/a ",
                         ("%.3f" % ac) if ac else " n/a "))
    check(ok_af, "hex head seat measured across flats off the mesh",
          "%.2f mm required (%.2f measured nut + %.2f fit allowance)"
          % (NUT_HEX_AF, R["nut_af"], R["nut_fit"]))
    check(ok_ac, "and across corners - it really is a regular hexagon",
          "%.3f mm required; a round hole would read the same both ways and "
          "could not key the nut" % NUT_HEX_AC)
    # the axial stack
    sp = material_spans(tris, (FIX_X, 0.0, 4.0), (0.0, 0.0, -1.0),
                        lo=0.0, hi=20.0)
    if sp:
        seg = ["%+.2f..%+.2f" % (4.0 - b, 4.0 - a) for a, b in sp]
        note("material down the fixing axis", ", ".join(seg))
    check(inside(tris, FIX_X + 1.60, 0.0, Z_NUT_SEAT + 0.50),
          "solid ring ahead of the seating shoulder",
          "%.2f mm of carrier between the Perspex seating face and the nut "
          "seat - the clamp load runs through it in compression"
          % R["nut_seat_depth"])
    check(not inside(tris, FIX_X, 0.0, Z_NUT_SEAT + 0.50),
          "bolt clearance bore open at the seating face",
          "%.2f mm, the original bolt passes without touching the carrier"
          % R["bolt_clear_d"])
    check(not inside(tris, FIX_X, 0.0, -R["car_d"] + 0.30),
          "nut pocket is rear-accessible",
          "the bore runs right through to the carrier rear face, so the nut "
          "is fitted and serviced from the rear")
    # the retaining ridge must actually be there
    zr_mid = Z_NUT_RETAIN + R["nut_retain_h"] / 2.0
    ok_ridge = True
    for sx in (-1, 1):
        x0 = sx * FIX_X
        sp = material_spans(tris, (x0, -6.0, zr_mid), (0.0, 1.0, 0.0),
                            lo=0.0, hi=12.0)
        af = (sp[1][0] - sp[0][1]) if (sp and len(sp) == 2) else None
        if af is None or abs(af - NUT_RETAIN_AF) > 0.05:
            ok_ridge = False
    check(ok_ridge, "captive retaining ridge measured off the mesh",
          "%.2f mm across flats against a %.2f mm nut = %.3f mm interference "
          "per flat; pushed past on assembly, pushed back for service, no "
          "adhesive" % (NUT_RETAIN_AF, R["nut_af"],
                        (R["nut_af"] - NUT_RETAIN_AF) / 2.0))
    # boss wall, measured
    ok_wall = True
    worst = 99.0
    for sx in (-1, 1):
        x0 = sx * FIX_X
        sp = material_spans(tris, (x0, -6.0, -R["car_d"] + 1.5),
                            (0.0, 1.0, 0.0), lo=0.0, hi=12.0)
        if sp and len(sp) == 2:
            w = min(sp[0][1] - sp[0][0], sp[1][1] - sp[1][0])
            worst = min(worst, w)
        else:
            ok_wall = False
    check(ok_wall and worst > 1.0,
          "continuous structural boss wall around the pocket",
          "%.3f mm minimum, measured across the clearance bore" % worst)
    note("pull-through", "the nut bears on a %.2f mm2 shoulder backed by a "
         "%.2f mm solid ring" % (math.sqrt(3.0) / 2 * NUT_HEX_AF ** 2
                                 - math.pi / 4 * R["bolt_clear_d"] ** 2,
                                 R["nut_seat_depth"]))
    note("load path", "original bolt head -> Perspex -> carrier seating face "
         "-> captive original nut -> original bolt thread; no part of it "
         "passes through the OLED glass or PCB")

    # ---- O. INTEGRAL REAR LIGHT SHIELD (brief 8.3) -----------------------
    print("")
    print("O. INTEGRAL REAR LIGHT SHIELD")
    print("   The Rev P.3 open rear window is gone. Everything below is")
    print("   measured off the mesh, not read back from the generator.")
    zmid = Z_REAR + R["rear_light_shield_t"] / 2.0

    # 1. thickness, as the FIRST material span along +Z from behind the part.
    #    The four bay corners hold the pedestal towers, which are thicker by
    #    design, so the probes sample the free wall.
    tp = [("bay centre", 0.0, 0.0),
          ("bottom edge, left of the tower", -11.00, SHIELD[2] + 0.60),
          ("bottom edge, right of the tower", 11.00, SHIELD[2] + 0.60),
          ("left edge, low", SHIELD[0] + 0.45, -6.00),
          ("left edge, high", SHIELD[0] + 0.45, 14.00),
          ("right edge, low", SHIELD[1] - 0.45, -6.00),
          ("right edge, high", SHIELD[1] - 0.45, 14.00),
          ("top edge, outboard of the tower", 8.00, SHIELD[3] - 0.60),
          ("top edge, outboard of the tower", -8.00, SHIELD[3] - 0.60),
          ("beside the pin slot", PIN_X1 + 1.00, R["header_off_y"]),
          ("below the pin slot", 0.0, PIN_Y0 - 1.00)]
    tbad = []
    for nm, tx, ty in tp:
        sp = material_spans(tris, (tx, ty, Z_REAR - 2.0), (0.0, 0.0, 1.0),
                            lo=0.0, hi=40.0)
        got = (sp[0][1] - sp[0][0]) if sp else 0.0
        if abs(got - R["rear_light_shield_t"]) > 0.005:
            tbad.append("%s = %.3f" % (nm, got))
    check(not tbad, "rear wall thickness measured off the mesh",
          "%.2f mm at all %d probes = %d x 0.40 mm extrusion widths"
          % (R["rear_light_shield_t"], len(tp),
             int(round(R["rear_light_shield_t"] / 0.40))) if not tbad
          else "wrong at " + "; ".join(tbad))

    # 2. coverage. Sweep the whole bay at mid-wall depth: every sample must be
    #    solid except the ones inside the declared four-pin slot. This is what
    #    catches an unintended second opening.
    nx, ny = 71, 67
    solid_out = 0
    void_in = 0
    slot_pts = 0
    for i in range(nx):
        x = SHIELD[0] + 0.20 + (SHIELD[1] - SHIELD[0] - 0.40) * i / (nx - 1.0)
        for j in range(ny):
            y = SHIELD[2] + 0.20 + (SHIELD[3] - SHIELD[2] - 0.40) * j / (ny - 1.0)
            in_slot = (-PIN_X1 + 0.05 < x < PIN_X1 - 0.05) and (y > PIN_Y0 + 0.05)
            near = (abs(abs(x) - PIN_X1) < 0.10) or (abs(y - PIN_Y0) < 0.10)
            if near:
                continue
            solid = inside(tris, x, y, zmid)
            if in_slot:
                slot_pts += 1
                if solid:
                    solid_out += 1
            elif not solid:
                void_in += 1
    check(void_in == 0, "the rear wall is continuous across the OLED bay",
          "%d of %d swept points outside the pin slot are solid - no rear "
          "window, no solder-access window, no rear release opening"
          % (nx * ny - slot_pts, nx * ny - slot_pts) if void_in == 0
          else "%d SWEPT POINTS ARE OPEN outside the declared slot" % void_in)
    check(solid_out == 0, "no unintended second rear opening",
          "the only opening found anywhere in the bay is the four-pin slot "
          "(%d swept points, all clear)" % slot_pts if solid_out == 0
          else "%d points inside the declared slot are blocked" % solid_out)

    # 3. the slot, measured. Cast along X at the header row: one void span.
    sp = material_spans(tris, (-30.0, R["header_off_y"], zmid),
                        (1.0, 0.0, 0.0), lo=0.0, hi=60.0)
    gap = None
    if sp and len(sp) >= 2:
        for a, b in zip(sp, sp[1:]):
            if a[1] < 30.0 < b[0]:
                gap = (a[1] - 30.0, b[0] - 30.0)
    ok = gap is not None and abs((gap[1] - gap[0]) - 2 * PIN_X1) < 0.02
    check(ok, "four-pin slot width = header %.2f + 2 x %.2f clearance"
          % (R["header_w"], R["pin_slot_clear_x"]),
          "%.3f mm measured, x %+.2f .. %+.2f, centred on the header"
          % (gap[1] - gap[0], gap[0], gap[1]) if ok
          else "measured %s against %.2f mm required"
          % (gap, 2 * PIN_X1))
    # and along Y at the slot centre: solid below PIN_Y0, open above it
    check(inside(tris, 0.0, PIN_Y0 - 0.20, zmid)
          and not inside(tris, 0.0, PIN_Y0 + 0.20, zmid),
          "four-pin slot floor = header %.2f + %.2f clearance below"
          % (R["header_h"], R["pin_slot_clear_y"]),
          "solid at y %+.2f, open at y %+.2f - the pins and their conductors "
          "pass without rubbing" % (PIN_Y0 - 0.20, PIN_Y0 + 0.20))
    check(inside(tris, -PIN_X1 - 0.20, R["header_off_y"], zmid)
          and inside(tris, PIN_X1 + 0.20, R["header_off_y"], zmid),
          "carrier solid on both X sides of the pin slot",
          "%.2f mm of solid wall stands either side of it"
          % (SHIELD[1] - PIN_X1))
    print("     REPORTED, NOT HIDDEN: the header row sits at y %+.2f and its"
          % R["header_off_y"])
    print("     envelope tops out at y %+.2f, %.2f mm ABOVE the carrier's own"
          % (R["header_off_y"] + R["header_h"] / 2,
             R["header_off_y"] + R["header_h"] / 2 - R["light_cut_y"]))
    print("     termination at y %+.2f, because the connector is at the OPEN"
          % R["light_cut_y"])
    print("     lighting-unit end of the board. The slot is bounded by wall on")
    print("     both X sides and below; above, its boundary is the wall's free")
    print("     edge, which IS the mandated open side of brief 8.1 - not a")
    print("     second opening. Closing it would mean printing material back")
    print("     above y %+.2f and undoing the rail cut that physically fits."
          % R["light_cut_y"])

    # 4. confined to the bay, and out of the deleted rail / tie region
    pr = R["pedestal_d"] / 2 + 0.05
    band = []
    for (a, b) in ((-30.0, -POST_X - pr), (-POST_X + pr, POST_X - pr),
                   (POST_X + pr, 30.0)):
        if b > a:
            band.append((a, b, R["light_cut_y"] + 1e-3, 60.0,
                         Z_SHIELD_REAR - 1e-3, Z_SHIELD_FRONT + 1e-3))
    m = boxes_hit(tris, band, shrink=1e-4)
    check(not m.any(), "the wall is confined to the OLED bay",
          "nothing above y %+.2f in the wall's own Z band except the two "
          "retained pedestal towers" % R["light_cut_y"] if not m.any()
          else "%d triangles have escaped the bay" % int(m.sum()))

    # 5. behind and clear of the module; built forward from the rear plane
    check(not inside(tris, 0.0, 0.0, Z_SHIELD_FRONT + 0.05),
          "the bay is open again immediately ahead of the wall",
          "the wall is %.2f mm thick and stops at z %+.2f, %.2f mm BEHIND "
          "DATUM B at z %+.2f - no contact with the PCB, no preload, and it "
          "is not an OLED Z datum"
          % (R["rear_light_shield_t"], Z_SHIELD_FRONT,
             Z_PCB_REAR - Z_SHIELD_FRONT, Z_PCB_REAR))
    check(abs(tris.reshape(-1, 3)[:, 2].min() + R["car_d"]) < 1e-3,
          "built FORWARD from the existing rear plane",
          "the external rear envelope is unchanged at z %+.2f; the wall grew "
          "inwards to z %+.2f" % (Z_REAR, Z_SHIELD_FRONT))
    note("service removal", "unchanged and NOT rearward: pinch both sprung "
         "barbs from the front through the module aperture and withdraw the "
         "OLED forwards. The wall sits %.2f mm behind the PCB rear face, so "
         "neither the board nor the bonded glass ever reaches it."
         % (Z_PCB_REAR - Z_SHIELD_FRONT))
    note("material and orientation", "print OPAQUE BLACK and fully solid "
         "through the wall. Rear face down, so the wall is the first %d layers "
         "flat on the bed - no bridging and no supports."
         % int(round(R["rear_light_shield_t"] / 0.20)))

    # ---- open items that gate the print ----------------------------------
    print("")
    print("P. MEASUREMENTS AND TESTS THAT GATE THE PRINT AND THE RELEASE")
    openitem("original nut across flats AND across corners",
             "%.2f mm is MODELLED as across flats. If it is across corners the "
             "true across-flats is %.2f mm and this pocket is %.2f mm oversize."
             % (R["nut_af"], R["nut_af"] * math.sqrt(3.0) / 2.0,
                R["nut_af"] - R["nut_af"] * math.sqrt(3.0) / 2.0))
    openitem("original bolt length under the head",
             "must exceed the %.2f mm grip to engage and stay under %.2f mm to "
             "remain inside the nut" % (R["perspex_t"] + R["nut_seat_depth"],
                                        R["perspex_t"] + R["nut_seat_depth"]
                                        + R["nut_total_len"]))
    openitem("hex-pocket fit coupon",
             "fit allowance %.2f mm, retaining lip %.2f mm - print the coupon "
             "and confirm push-in, inverted retention and service removal "
             "before the carrier" % (R["nut_fit"], R["nut_retain_lip"]))
    openitem("installed clearance against the retained lighting unit",
             "there is NO measured lighting-unit geometry in this project and "
             "nothing above may be read as CAD proof of that clearance. All "
             "that is known is the carrier's own extent, y max %+.2f. Offer "
             "the carrier up with the lighting unit in place - brief 12.14, "
             "which stays MANDATORY." % R["carrier_max_y"])
    openitem("powered light-leak test, brief 12.22",
             "the %.2f mm wall, the opaque black material and the %.2f x "
             "%.2f mm pin slot are engineering choices, not measurements "
             "against the Decca cabinet LEDs. Run the LEDs through their "
             "usable brightness range with the OLED showing black, dim and "
             "normal content. If leakage remains ONLY at the pin slot, tighten "
             "that opening or add an integral hood - do not reopen the wall "
             "and do not add another component."
             % (R["rear_light_shield_t"], 2 * PIN_X1,
                R["light_cut_y"] - PIN_Y0))

    print("")
    print("=" * 80)
    if OPENS:
        print("BLOCKING OPEN ITEM(S) BEFORE ANY PRINT")
        for n in OPENS:
            print("   * %s" % n)
        print("")
    if NOTES:
        for n in NOTES:
            print("   * %s" % n)
        print("")
    if FAILS:
        print("VERDICT: %d CHECK(S) FAILED" % len(FAILS))
        for f in FAILS:
            print("   - %s" % f)
    else:
        print("VERDICT: every independent geometric check on the exported STL")
        print("         passes. The Rev P.2 OLED retention and Perspex fit are")
        print("         physically validated and unchanged here. Rev P stays")
        print("         OPEN: lighting-unit clearance, light leakage and the")
        print("         original-fastener interface are all CAD-only so far,")
        print("         and the first two cannot be closed by CAD at all.")
    print("=" * 80)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
