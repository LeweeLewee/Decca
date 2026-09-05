# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev B slicer evidence harness
===============================================================

Slices the production set and the two prototype coupons with the Bambu Studio
CLI and reports REAL filament use and print time, so the build report can quote
predicted spool consumption instead of relabelling a solid-volume calculation.

    python mechanical/CAD/Decca_ESP32_Controller_Housing_slice.py

The full-solid figure in the build report remains the conservative DESIGN GATE.
This is the operational number, and the two are reported separately.

Three things had to be solved to drive the CLI headlessly, all recorded here so
the next person does not repeat them:

  1. `--slice` needs `--arrange 1` for a bare STL, or it reports
     "The input files to the slicer are not found" even though the file is
     there and `--export-3mf` reads it happily.
  2. Bambu's system presets use `inherits` chains that the CLI will not resolve
     from a bare file path, so they are FLATTENED here first. Nothing else
     about them is rewritten: touching setting_id, instantiation or
     compatible_printers makes the CLI reject the printer/process pairing.
  3. The P1S takes the X1C process presets - that is what its own machine
     preset names in `default_print_profile` - and PETG cannot use the Cool
     Plate, so `curr_bed_type` has to be declared or the slice is refused.

The lid is flipped 180 degrees about X before slicing, because its stated print
orientation is TOP-FACE-DOWN and that is the orientation the support-free claim
depends on.
"""
from __future__ import print_function

import io
import json
import math
import os
import re
import struct
import subprocess
import sys

# This harness drives a Windows-only GUI executable through its CLI
# entry point. Every prerequisite is resolved LAZILY and reported as
# plain english, so running it on Linux, in CI, or on a machine without
# Bambu Studio prints what is missing and exits 2. It never dies on a
# KeyError reading an environment variable only Windows sets.
EXE = r"C:\Program Files\Bambu Studio\bambu-studio.exe"
APPDATA = os.environ.get("APPDATA")
TEMPDIR = os.environ.get("TEMP") or os.environ.get("TMP")
PRE = (os.path.join(APPDATA, "BambuStudio", "ota", "presets", "BBL")
       if APPDATA else None)
REPO = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", ".."))
STL = os.path.join(REPO, "mechanical", "STL")
WORK = os.path.join(TEMPDIR, "claude", "slice_revb") if TEMPDIR else None


def unavailable():
    """What this machine is missing, as a list of plain-english reasons.

    Empty means the slicer can be driven here."""
    why = []
    if os.name != "nt":
        why.append("this is a Windows-only slicer harness (os.name=%r)"
                   % os.name)
    if not APPDATA:
        why.append("APPDATA is not set, so the Bambu preset library "
                   "cannot be located")
    if not TEMPDIR:
        why.append("neither TEMP nor TMP is set, so there is nowhere "
                   "to stage the slice")
    if not os.path.exists(EXE):
        why.append("Bambu Studio is not installed at %s" % EXE)
    elif PRE and not os.path.isdir(PRE):
        why.append("the Bambu system preset library is not at %s" % PRE)
    return why

MACHINE = "Bambu Lab P1S 0.4 nozzle"
PROCESS = "0.20mm Standard @BBL X1C"   # the P1S machine preset's own default_print_profile
FILAMENT = "Generic PETG HF @BBL P1S 0.4 nozzle"

# The declared profile, injected over the stock process preset.
OVERRIDES = {
    "wall_loops": "3",
    "sparse_infill_density": "15%",
    "enable_support": "0",
    "layer_height": "0.2",
    "initial_layer_print_height": "0.2",
    # PETG is not compatible with the Cool Plate, and the CLI refuses to slice
    # if the plate type and the filament disagree.
    "curr_bed_type": "Textured PEI Plate",
}

# part -> (stl name, quantity, print orientation)
#   "as-modelled"  the STL is already in its print orientation
#   "flip-x"       rotate 180 deg about X, i.e. top face down
PARTS = [
    ("Housing_Base", "ESP32_Controller_Housing_Base.stl", 1, "as-modelled"),
    ("Housing_Lid", "ESP32_Controller_Housing_Lid.stl", 1, "flip-x"),
    ("PCB_Clamp_Adjustable", "ESP32_Controller_PCB_Clamp_Adjustable.stl", 1,
     "as-modelled"),
    ("Cabinet_Fastener_Cap", "ESP32_Controller_Cabinet_Fastener_Cap.stl", 2,
     "as-modelled"),
]

GAUGES = [
    ("Carrier_Fit_Coupon", "ESP32_Controller_Carrier_Fit_Coupon.stl", 1,
     "as-modelled"),
    ("Insert_Fastener_Coupon", "ESP32_Controller_Insert_Fastener_Coupon.stl", 1,
     "as-modelled"),
]


# ---------------------------------------------------------------------------
def flatten(kind, name, seen=None):
    """Resolve a preset's `inherits` chain into one flat dict."""
    seen = seen or []
    if name in seen:
        raise RuntimeError("inherits loop at %s" % name)
    path = os.path.join(PRE, kind, name + ".json")
    if not os.path.exists(path):
        raise IOError("preset not found: %s" % path)
    d = json.load(io.open(path, encoding="utf-8"))
    parent = d.pop("inherits", None)
    if parent:
        base = flatten(kind, parent, seen + [name])
        base.update(d)
        d = base
    return d


def write_presets(out_dir):
    made = {}
    for kind, name, extra in (("machine", MACHINE, None),
                              ("process", PROCESS, OVERRIDES),
                              ("filament", FILAMENT, None)):
        # Flatten only. Every other field is left exactly as Bambu ships it -
        # rewriting setting_id, instantiation or compatible_printers is what
        # made the CLI reject the printer/process pairing.
        d = flatten(kind, name)
        d["name"] = name
        if extra:
            d.update(extra)
        p = os.path.join(out_dir, "%s.json" % kind)
        io.open(p, "w", encoding="utf-8").write(
            json.dumps(d, indent=2, ensure_ascii=False))
        made[kind] = p
    return made


# ---------------------------------------------------------------------------
def read_stl(path):
    with open(path, "rb") as fh:
        head = fh.read(84)
        n = struct.unpack("<I", head[80:84])[0]
        raw = fh.read(n * 50)
    tris = []
    for i in range(n):
        v = struct.unpack("<12f", raw[i * 50:i * 50 + 48])
        tris.append([v[3:6], v[6:9], v[9:12]])
    return tris


def write_stl(path, tris):
    with open(path, "wb") as fh:
        fh.write(b"\0" * 80)
        fh.write(struct.pack("<I", len(tris)))
        for t in tris:
            ax, ay, az = t[0]
            bx, by, bz = t[1]
            cx, cy, cz = t[2]
            ux, uy, uz = bx - ax, by - ay, bz - az
            vx, vy, vz = cx - ax, cy - ay, cz - az
            nx = uy * vz - uz * vy
            ny = uz * vx - ux * vz
            nz = ux * vy - uy * vx
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            fh.write(struct.pack("<12fH", nx / ln, ny / ln, nz / ln,
                                 ax, ay, az, bx, by, bz, cx, cy, cz, 0))


def orient(tris, how):
    if how == "flip-x":
        # 180 degrees about X, and reverse winding so normals stay outward
        tris = [[(v[0], -v[1], -v[2]) for v in reversed(t)] for t in tris]
    zs = [v[2] for t in tris for v in t]
    dz = -min(zs)
    return [[(v[0], v[1], v[2] + dz) for v in t] for t in tris]


# ---------------------------------------------------------------------------
GC_PATTERNS = {
    "grams": re.compile(r"^;\s*total filament weight \[g\]\s*:\s*([0-9.]+)", re.I),
    "grams2": re.compile(r"^;\s*filament used \[g\]\s*=\s*([0-9.]+)", re.I),
    "time": re.compile(r"^;\s*(?:estimated printing time.*?|model printing time)\s*[:=]\s*(.+)$", re.I),
    "total_time": re.compile(r"^;\s*total estimated time\s*[:=]\s*(.+)$", re.I),
    "support": re.compile(r"^;\s*enable_support\s*=\s*(\S+)", re.I),
    "walls": re.compile(r"^;\s*wall_loops\s*=\s*(\S+)", re.I),
    "infill": re.compile(r"^;\s*sparse_infill_density\s*=\s*(\S+)", re.I),
    "layer": re.compile(r"^;\s*layer_height\s*=\s*(\S+)", re.I),
    "nozzle": re.compile(r"^;\s*nozzle_diameter\s*=\s*(\S+)", re.I),
    "filament_type": re.compile(r"^;\s*filament_type\s*=\s*(\S+)", re.I),
}


def parse_gcode(path):
    got = {}
    with io.open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if not line.startswith(";"):
                continue
            for key, rx in GC_PATTERNS.items():
                if key in got:
                    continue
                m = rx.match(line)
                if m:
                    got[key] = m.group(1).strip()
    return got


def slice_one(tag, stl_name, how, presets, src_dir):
    d = os.path.join(WORK, tag)
    if not os.path.isdir(d):
        os.makedirs(d)
    src = os.path.join(src_dir, stl_name)
    if not os.path.exists(src):
        return {"error": "STL missing: %s" % stl_name}
    dst = os.path.join(d, "part.stl")
    write_stl(dst, orient(read_stl(src), how))
    gc = os.path.join(d, "plate_1.gcode")
    if os.path.exists(gc):
        os.remove(gc)
    cmd = [EXE, "--arrange", "1", "--slice", "0",
           "--load-settings", "%s;%s" % (presets["machine"], presets["process"]),
           "--load-filaments", presets["filament"],
           "--outputdir", d, dst]
    # cwd=d: the CLI drops a result.json into the WORKING directory as well as
    # into --outputdir, and it must not land in the repository.
    subprocess.call(cmd, cwd=d)
    res = {}
    rp = os.path.join(d, "result.json")
    if os.path.exists(rp):
        res = json.load(io.open(rp, encoding="utf-8"))
    if not os.path.exists(gc):
        return {"error": res.get("error_string", "no gcode"), "result": res}
    out = parse_gcode(gc)
    out["result"] = res
    return out


def main():
    why = unavailable()
    if why:
        print("SLICER EVIDENCE NOT AVAILABLE ON THIS MACHINE")
        for w in why:
            print("  - %s" % w)
        print("")
        print("No slicer figures are produced here. The build report's "
              "full-solid volume and mass remain the conservative design "
              "gate and are NOT a slicer estimate; the figures in section "
              "2.4 were recorded on a machine where this harness ran.")
        return 2
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    presets = write_presets(WORK)
    print("presets flattened:", ", ".join(os.path.basename(p)
                                          for p in presets.values()))
    print("")
    rows = []
    for tag, name, qty, how in PARTS + GAUGES:
        r = slice_one(tag, name, how, presets, STL)
        rows.append((tag, qty, how, r))
        if "error" in r:
            print("%-24s FAILED: %s" % (tag, r["error"]))
        else:
            g = r.get("grams") or r.get("grams2") or "?"
            print("%-24s x%d %-12s %8s g  %-18s walls=%s infill=%s "
                  "support=%s layer=%s nozzle=%s"
                  % (tag, qty, how, g, r.get("time", "?"), r.get("walls"),
                     r.get("infill"), r.get("support"), r.get("layer"),
                     r.get("nozzle")))
    json.dump([[t, q, h, r] for t, q, h, r in rows],
              io.open(os.path.join(WORK, "summary.json"), "w",
                      encoding="utf-8"), indent=1)
    print("")
    print("summary written to", os.path.join(WORK, "summary.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
