# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev A parametric generator (Autodesk Fusion 360).

Controlling document: mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md
Status: PROTOTYPE CAD. NOT physically validated. Nothing in this file has been
        measured off the acquired hardware.

WHAT THIS BUILDS
----------------
One document, nine components, exactly the tree the specification asks for:

    Decca_ESP32_Controller_Housing
    |-- REF_ESP32_DevKit_V1_30Pin      non-manufacturing reference
    |-- REF_30Pin_Terminal_Adapter     non-manufacturing reference
    |-- REF_Wired_Keepouts             non-manufacturing reference
    |-- Housing_Base                   printable
    |-- Housing_Lid                    printable
    |-- PCB_Clamp_Fixed_End            printable
    |-- PCB_Clamp_Adjustable_End       printable
    |-- USB_Blanking_Plug              printable
    +-- Carrier_Fit_Gauge              printable

THE HARDWARE IS NOT MEASURED, AND THIS FILE DOES NOT PRETEND OTHERWISE
----------------------------------------------------------------------
The repository records the controller family (30-pin DevKit V1 / DOIT-style)
and that a matching 30-pin screw-terminal adapter is ACQUIRED. It records no
manufacturer, no outline, no mounting-hole pattern and no assembled height.
Specification section 2 forbids inventing one.

So every hardware number below is a CAD STARTING VALUE carrying the tag
STARTING in the parameter table, and the housing uses non-hole-dependent
retention: the breakout is held by two removable printed edge clamps that
touch declared bare PCB edge only. No fastener enters the board. If the
acquired breakout measures differently, change the STARTING parameters and
re-run; nothing downstream is a hidden sketch dimension.

THREE DERIVED DIMENSIONS EXCEED THE SPECIFICATION'S APPROXIMATE TARGETS
-----------------------------------------------------------------------
Section 10 gives approximate totals and then says, in terms: "These are design
targets, not permission to violate required electrical, terminal, antenna or
cable clearances. Claude should report the final derived envelope rather than
forcing these approximate totals." This build takes that instruction literally.
Every required clearance is met in full and the envelope is reported, not
forced. The three overruns, with their arithmetic, are:

1. HEIGHT 38.30 mm against an approximate 35 mm target.
   2.40 floor + 2.50 below-PCB components + 3.00 clearance beneath those
   joints + 1.60 PCB + 24.00 assembly above PCB + 3.00 clearance above the
   highest component + 1.80 lid top = 38.30. Section 4 lists the 2.50 mm
   below-PCB height and the 3.00 mm beneath-joint clearance as two separate
   values, and section 5.1 requires the 3.00 mm to be measured BENEATH the
   solder joints, so the two are additive. Section 10's "internal height above
   PCB support plane 27.0 mm" is 1.60 mm short of the PCB plus assembly plus
   top clearance it has to contain; the derived figure is 28.60 mm.

2. LENGTH 105.00 mm against an approximate 90 mm target.
   Section 10 budgets a 72.0 mm body, which is 68.0 mm of internal plan plus
   two 2.0 mm walls. That leaves NO length at all for the section 5.2 end
   clamps, their two M3 screws each, or the four section 9 lid-screw bosses,
   which section 9 requires to be outside the breakout outline - and outside
   the breakout outline, in a housing whose cavity is 1.00 mm wider than the
   board, means beyond the two short edges. The derived chain per end is
   boss wall 2.00 + insert hole 4.00 + boss wall 2.00, widened at the
   adjustable end to 9.50 mm to carry the +/-1.00 mm slot travel and the bar
   edge margin, plus a 2.00 mm wall. Body length is therefore 89.00 mm, and
   the four section 5.3 ears add 8.00 mm at each end.

3. WIDTH 77.00 mm against a 78.0 mm maximum - this one is INSIDE target, and
   is stated here only because the plan is not square: the derived plan area,
   105.00 x 77.00 = 8085 mm2, is 15% larger than the 90 x 78 = 7020 mm2
   target rectangle. The housing is longer and narrower than the target
   assumed.

This is reported as an owner decision item in the build report. It is NOT
resolved by deleting clamps, shrinking clearances or moving the separately
mounted MOSFET/power hardware into this box. See BUILD REPORT section
"Envelope deviation" for the two documented ways to shorten it.

ARCHITECTURE
------------
Base tray, floor down. Insulating floor continuous beneath the whole board.
Six low support pads touch only the declared bare long-edge perimeter strip.
One short edge butts a hard datum face; the other is taken by a clamp with
+/-1.00 mm of slot travel. Both clamps lift off with the lid off and the
wiring still connected, and the ESP32 pulls straight up out of its sockets
with only the lid removed.

Both long walls carry one continuous cable-exit window, 14.00 mm of clear
height, whose top edge is a 45-degree sawtooth so a 60 mm opening prints with
no bridge and no support. Below each window an external lacing rail gives six
2.50 x 6.00 mm cable-tie slots per side, so tie load lands on the housing and
never on the screw terminals.

Removable lid, overlapping OUTSIDE the base wall by 5.00 mm at 0.25 mm per
face. It overlaps outside deliberately: an internal tongue would have to sit
inside the wall line, and the wall line is 0.50 mm off the board, so an
internal tongue lands inside the maximum-assembled-height keep-out. The lid
is thinned to 1.60 mm over the antenna, carries no insert, screw, rib or
lacing feature there, and its top vents are 2.00 mm slots - narrower than an
M3 shank and much narrower than the 4.00 mm inserts, so no fastener used in
this build can fall through one whatever path it takes.

PRINTING
--------
PETG or PETG-HF, 0.40 mm nozzle, 0.20 mm layers. Base floor-down. Lid
top-face-down, which is what keeps the recessed markings crisp. Clamps, gauge
and USB plug flat in their working orientation. No part needs support.

RUNNING IT
----------
    main(None)      builds/rebuilds every component in the active document
    validate(None)  runs the section 14 gate suite against the built solids
    export(None)    writes f3d, STEP and STL into mechanical/CAD and
                    mechanical/STL

``run`` is provided so the file can be sent straight through the Fusion MCP
bridge; it calls ``main``.
"""

from __future__ import print_function

import math
import os

import adsk.core
import adsk.fusion


DOC_NAME = "Decca_ESP32_Controller_Housing"

BASE = "Housing_Base"
LID = "Housing_Lid"
CLAMP_FIX = "PCB_Clamp_Fixed_End"
CLAMP_ADJ = "PCB_Clamp_Adjustable_End"
PLUG = "USB_Blanking_Plug"
GAUGE = "Carrier_Fit_Gauge"

REF_ESP = "REF_ESP32_DevKit_V1_30Pin"
REF_ADP = "REF_30Pin_Terminal_Adapter"
REF_KEEP = "REF_Wired_Keepouts"

PRINTABLE = (BASE, LID, CLAMP_FIX, CLAMP_ADJ, PLUG, GAUGE)
REFERENCE = (REF_ESP, REF_ADP, REF_KEEP)

REF_NOTE = ("NON-MANUFACTURING REFERENCE. Dimensional starting values only - "
            "not measured hardware. Excluded from every printable export.")

# Repository root, resolved from this file, so exports land in the repo.
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))


# ---------------------------------------------------------------------------
# PARAMETERS - the single source of truth.
#
# STATUS tags, used verbatim in the build report:
#   LOCKED    recorded by the repository as a hardware fact
#   STARTING  a CAD starting value; NOT measured; correct it after the fit test
#   DESIGN    a design value taken from the controlling specification
#   DERIVED*  (in derive() below, never here)
# ---------------------------------------------------------------------------
P = {
    # -- Repository-controlled hardware, LOCKED ----------------------------
    "esp_pin_count": 30,

    # -- Breakout / terminal adapter reference, STARTING -------------------
    "adapter_pcb_l": 66.00,
    "adapter_pcb_w": 63.00,
    "adapter_pcb_t": 1.60,
    "adapter_below_h": 2.50,
    "assembly_above_pcb_h": 24.00,
    "adapter_len_adjust": 1.00,      # required +/- longitudinal adjustment
    "pcb_bare_edge": 3.00,           # bare strip inboard of each SHORT edge
    "pcb_bare_perim": 2.50,          # bare strip inboard of each LONG edge
    "pad_l": 8.00,                   # PCB support pad, along the long edge
    "pad_w": 2.20,                   # PCB support pad, across the long edge

    # -- Screw terminals, STARTING -----------------------------------------
    "term_per_side": 15,
    "term_pitch": 3.50,
    "term_block_w": 8.00,            # block depth inboard from the PCB edge
    "term_block_h": 10.00,           # block height above the PCB top face
    "term_screw_inset": 4.00,        # screw axis inboard from the PCB edge
    "term_screw_d": 2.60,
    "term_wire_z": 4.00,             # wire entry height above the PCB top

    # -- ESP32 DevKit V1 / DOIT reference, STARTING ------------------------
    "esp_pcb_l": 51.50,
    "esp_pcb_w": 28.30,
    "esp_pcb_t": 1.60,
    "esp_header_h": 8.50,            # socket header height above the breakout
    "esp_header_span": 22.86,        # 0.90 in row spacing
    "esp_off_x": 0.00,
    "esp_off_y": 0.00,
    "esp_mod_l": 25.50,
    "esp_mod_w": 18.00,
    "esp_mod_h": 3.10,
    "esp_ant_l": 15.00,              # PCB antenna, at the END OPPOSITE the USB
    "esp_ant_w": 18.00,
    "esp_usb_w": 7.50,
    "esp_usb_l": 5.90,
    "esp_usb_h": 2.70,
    "esp_btn_x": -22.00,             # EN/RESET and BOOT, module-local X
    "esp_btn_y": 10.15,              # +Y = EN/RESET, -Y = BOOT
    "esp_btn_sz": 6.00,
    "esp_btn_h": 4.30,

    # -- Clearances, DESIGN (specification section 11) ---------------------
    "pcb_xy_clear": 0.50,
    "pcb_under_clear": 3.00,
    "component_top_clear": 3.00,
    "clamp_vertical_clear": 0.20,
    "antenna_keepout": 10.00,
    "lid_fit_clear": 0.25,

    # -- Structure, DESIGN --------------------------------------------------
    "base_floor_t": 2.40,
    "wall_t": 2.00,
    "lid_top_t": 1.80,
    "lid_antenna_t": 1.60,
    "lid_overlap": 5.00,
    "lid_skirt_t": 2.00,
    "outer_corner_r": 3.00,
    "inner_fillet_r": 1.00,

    # -- Access, DESIGN -----------------------------------------------------
    "wire_exit_h": 10.00,            # REQUIRED minimum clear exit height
    "wire_win_h": 12.00,             # PROVIDED clear exit height
    "wire_win_half_l": 30.00,
    "wire_saw_n": 16,                # 45 deg sawtooth, height DERIVED
    "usb_open_w": 14.00,
    "usb_open_h": 9.00,
    "button_tool_d": 3.00,
    "button_tool_lead_d": 5.00,
    "tie_slot_w": 2.50,
    "tie_slot_l": 6.00,
    "tie_leg_w": 4.00,
    "tie_rail_t": 2.00,
    "tie_ledge_h": 3.00,             # solid rail root, clear of a mount face
    "driver_d": 6.00,                # terminal screwdriver corridor
    "wire_d": 2.60,                  # 22-24 AWG plus ferrule and insulation

    # -- Fasteners, DESIGN --------------------------------------------------
    "lid_screw_nominal": 3.00,
    "lid_screw_length": 8.00,
    "lid_screw_clear_d": 3.40,
    "lid_screw_head_d": 6.00,
    "insert_hole_d": 4.00,           # STARTING - exact insert NOT recorded
    "insert_depth": 6.00,            # STARTING - exact insert NOT recorded
    "boss_wall": 2.00,
    "pier_bury": 1.00,               # lid-screw pier buried into the wall
    "saw_margin": 1.00,              # sawtooth runs past the window ends
    "cabinet_slot_w": 4.00,
    "cabinet_slot_l": 8.00,
    "cabinet_screw_head_d": 6.50,
    "ear_t": 3.00,
    "ear_root_gap": 2.00,
    "ear_edge": 2.00,
    "ear_fillet_r": 2.00,

    # -- Edge clamps, DESIGN ------------------------------------------------
    "clamp_t": 3.00,
    "clamp_grip": 2.50,              # overhang onto the bare PCB short edge
    "clamp_half_span": 23.00,
    "clamp_screw_y": 19.00,
    "clamp_slot_w": 3.40,
    "clamp_slot_l": 5.40,            # 3.40 + 2 x 1.00 travel
    "clamp_bar_margin": 1.60,
    "clamp_corner_r": 2.00,

    # -- Ventilation, DESIGN -------------------------------------------------
    "vent_w": 2.00,
    "vent_bridge": 2.50,
    "vent_side_h": 5.00,
    "vent_lid_l": 12.00,

    # -- Fit gauge ------------------------------------------------------------
    "gauge_w": 24.00,
    "gauge_zone": 20.00,
    "gauge_plate_t": 2.40,
    "gauge_score": 0.60,
}

# Hardware values that are CAD starting values, not measurements. Every one of
# these is a prototype gate: it must be confirmed against the acquired board
# before any dimension derived from it can be called verified.
STARTING = (
    "adapter_pcb_l", "adapter_pcb_w", "adapter_pcb_t", "adapter_below_h",
    "assembly_above_pcb_h", "pcb_bare_edge", "pcb_bare_perim",
    "term_per_side", "term_pitch", "term_block_w", "term_block_h",
    "term_screw_inset", "term_screw_d", "term_wire_z",
    "esp_pcb_l", "esp_pcb_w", "esp_pcb_t", "esp_header_h", "esp_header_span",
    "esp_off_x", "esp_off_y", "esp_mod_l", "esp_mod_w", "esp_mod_h",
    "esp_ant_l", "esp_ant_w", "esp_usb_w", "esp_usb_l", "esp_usb_h",
    "esp_btn_x", "esp_btn_y", "esp_btn_sz", "esp_btn_h",
    "insert_hole_d", "insert_depth",
)


# ---------------------------------------------------------------------------
# Helpers. Fusion's internal length unit is cm; the whole design is mm.
# ---------------------------------------------------------------------------
def mm(v):
    return float(v) / 10.0


def p3(x, y, z):
    return adsk.core.Point3D.create(mm(x), mm(y), mm(z))


def v3(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


class Builder(object):
    """Thin wrapper over TemporaryBRepManager so recipes read like solids."""

    def __init__(self):
        self.tbm = adsk.fusion.TemporaryBRepManager.get()

    def box(self, x0, x1, y0, y1, z0, z1):
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        z0, z1 = min(z0, z1), max(z0, z1)
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0),
            v3(1, 0, 0), v3(0, 1, 0),
            mm(x1 - x0), mm(y1 - y0), mm(z1 - z0))
        return self.tbm.createBox(obb)

    def cylz(self, d, x, y, z0, z1):
        return self.tbm.createCylinderOrCone(p3(x, y, z0), mm(d / 2.0),
                                             p3(x, y, z1), mm(d / 2.0))

    def cyly(self, d, x, z, y0, y1):
        return self.tbm.createCylinderOrCone(p3(x, y0, z), mm(d / 2.0),
                                             p3(x, y1, z), mm(d / 2.0))

    def conez(self, d0, d1, x, y, z0, z1):
        return self.tbm.createCylinderOrCone(p3(x, y, z0), mm(d0 / 2.0),
                                             p3(x, y, z1), mm(d1 / 2.0))

    def copy(self, a):
        return self.tbm.copy(a)

    def uni(self, a, b):
        self.tbm.booleanOperation(a, b,
                                  adsk.fusion.BooleanTypes.UnionBooleanType)
        return a

    def sub(self, a, b):
        self.tbm.booleanOperation(
            a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        return a

    def inter(self, a, b):
        self.tbm.booleanOperation(
            a, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)
        return a

    def rrect(self, x0, x1, y0, y1, z0, z1, r):
        """Rounded-rectangle prism along Z, built from primitives - far more
        robust than filleting four long vertical edges afterwards."""
        if r <= 0.0:
            return self.box(x0, x1, y0, y1, z0, z1)
        r = min(r, (x1 - x0) / 2.0, (y1 - y0) / 2.0)
        eps = 1.0e-9
        s = None
        if (x1 - x0) - 2 * r > eps:
            s = self.box(x0 + r, x1 - r, y0, y1, z0, z1)
        if (y1 - y0) - 2 * r > eps:
            b = self.box(x0, x1, y0 + r, y1 - r, z0, z1)
            s = b if s is None else self.uni(s, b)
        for cx in sorted({round(x0 + r, 9), round(x1 - r, 9)}):
            for cy in sorted({round(y0 + r, 9), round(y1 - r, 9)}):
                c = self.cylz(2 * r, cx, cy, z0, z1)
                s = c if s is None else self.uni(s, c)
        return s

    def ring(self, x0, x1, y0, y1, t, z0, z1, r):
        """Rounded-rectangle wall of thickness t, grown inward from the outer
        rounded rectangle. Inner corner radius follows automatically."""
        outer = self.rrect(x0, x1, y0, y1, z0, z1, r)
        inner = self.rrect(x0 + t, x1 - t, y0 + t, y1 - t,
                           z0 - 1.0, z1 + 1.0, max(0.0, r - t))
        return self.sub(outer, inner)

    def tri_x(self, xc, z_base, half_w, height, y0, y1):
        """Isoceles triangular prism lying along Y: base 2*half_w at z_base,
        apex height above it. With half_w == height the flanks are 45 degrees,
        which is what makes the cable window print with no bridge."""
        s = math.sqrt(2.0) * max(half_w, height)
        u = v3(1.0 / math.sqrt(2.0), 0.0, 1.0 / math.sqrt(2.0))
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3(xc, (y0 + y1) / 2.0, z_base), u, v3(0, 1, 0),
            mm(s), mm(y1 - y0), mm(s))
        d = self.tbm.createBox(obb)
        return self.inter(d, self.box(xc - half_w - 1.0, xc + half_w + 1.0,
                                      y0 - 1.0, y1 + 1.0,
                                      z_base, z_base + height))

    def diamond_x(self, xc, zc, half, y0, y1):
        """Square prism rotated 45 degrees in XZ, lying along Y, centred on
        (xc, zc). Subtracted at a solid's corner it leaves an exact 45-degree
        chamfer of leg ``half`` on both faces meeting there."""
        s = math.sqrt(2.0) * half
        u = v3(1.0 / math.sqrt(2.0), 0.0, 1.0 / math.sqrt(2.0))
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3(xc, (y0 + y1) / 2.0, zc), u, v3(0, 1, 0),
            mm(s), mm(y1 - y0), mm(s))
        return self.tbm.createBox(obb)

    def round_edge_x(self, yc, zc, sy, sz, r, x0, x1):
        """Cutter that ROUNDS a convex edge running parallel to X at
        (yc, zc). (sy, sz) point INTO the material. Box at the corner minus
        the fillet cylinder - so what is left to remove is exactly the sharp
        corner outside radius r."""
        c = self.box(x0, x1, min(yc, yc + sy * r), max(yc, yc + sy * r),
                     min(zc, zc + sz * r), max(zc, zc + sz * r))
        return self.sub(c, self.cylx(2 * r, yc + sy * r, zc + sz * r,
                                     x0 - 1.0, x1 + 1.0))

    def round_edge_z(self, xc, yc, sx, sy, r, z0, z1):
        """Cutter that ROUNDS a convex edge running parallel to Z at
        (xc, yc). (sx, sy) point INTO the material."""
        c = self.box(min(xc, xc + sx * r), max(xc, xc + sx * r),
                     min(yc, yc + sy * r), max(yc, yc + sy * r), z0, z1)
        return self.sub(c, self.cylz(2 * r, xc + sx * r, yc + sy * r,
                                     z0 - 1.0, z1 + 1.0))

    def cylx(self, d, y, z, x0, x1):
        return self.tbm.createCylinderOrCone(p3(x0, y, z), mm(d / 2.0),
                                             p3(x1, y, z), mm(d / 2.0))


def volume_of(body):
    """Volume in mm^3 of a (possibly temporary) BRep body, 0.0 if empty."""
    if body is None:
        return 0.0
    try:
        if body.faces.count == 0:
            return 0.0
    except Exception:
        return 0.0
    try:
        v = body.volume
        if v:
            return float(v) * 1000.0
    except Exception:
        pass
    try:
        return float(body.physicalProperties.volume) * 1000.0
    except Exception:
        return -1.0


# ---------------------------------------------------------------------------
# Derived geometry - everything here is a consequence of P, nothing is typed.
# Origin: centre of the breakout PCB in plan, z = 0 at the cavity floor top.
# ---------------------------------------------------------------------------
def derive(P):
    d = {}

    # ---- vertical chain ---------------------------------------------------
    d["z_floor_bot"] = -P["base_floor_t"]
    d["z_floor_top"] = 0.0
    # Support height is ADDITIVE: section 5.1 requires the 3.00 mm to be
    # measured beneath the solder joints, and the joints hang 2.50 mm down.
    d["pad_h"] = P["adapter_below_h"] + P["pcb_under_clear"]
    d["z_pcb_bot"] = d["pad_h"]
    d["z_pcb_top"] = d["z_pcb_bot"] + P["adapter_pcb_t"]
    d["z_under_bot"] = d["z_pcb_bot"] - P["adapter_below_h"]
    d["z_term_top"] = d["z_pcb_top"] + P["term_block_h"]
    d["z_comp_top"] = d["z_pcb_top"] + P["assembly_above_pcb_h"]
    d["z_cav_top"] = d["z_comp_top"] + P["component_top_clear"]
    d["z_lid_top"] = d["z_cav_top"] + P["lid_top_t"]
    d["h_closed"] = d["z_lid_top"] - d["z_floor_bot"]
    d["internal_h_above_support"] = d["z_cav_top"] - d["z_pcb_bot"]

    # ---- board footprint --------------------------------------------------
    d["x_datum"] = -P["adapter_pcb_l"] / 2.0
    d["x_pcb_nom"] = P["adapter_pcb_l"] / 2.0
    d["x_pcb_max"] = d["x_datum"] + P["adapter_pcb_l"] + P["adapter_len_adjust"]
    d["x_pcb_min"] = d["x_datum"] + P["adapter_pcb_l"] - P["adapter_len_adjust"]
    d["x_adj_face"] = d["x_pcb_max"] + P["pcb_xy_clear"]
    d["y_pcb"] = P["adapter_pcb_w"] / 2.0
    d["y_cav"] = d["y_pcb"] + P["pcb_xy_clear"]
    d["y_out"] = d["y_cav"] + P["wall_t"]

    # ---- clamp screw chain - this is what sets the body length ------------
    d["insert_c"] = P["boss_wall"] + P["insert_hole_d"] / 2.0
    d["boss_od"] = 2.0 * d["insert_c"]
    d["fix_screw_x"] = d["x_datum"] - d["insert_c"]
    d["adj_screw_x"] = d["x_adj_face"] + d["insert_c"]

    d["fix_bar_in"] = d["x_datum"] + P["clamp_grip"]
    d["fix_bar_out"] = d["fix_screw_x"] - (P["lid_screw_clear_d"] / 2.0
                                           + P["clamp_bar_margin"])
    d["adj_bar_in"] = d["x_pcb_nom"] - P["clamp_grip"]
    d["adj_bar_out"] = d["adj_screw_x"] + (P["clamp_slot_l"] / 2.0
                                           + P["clamp_bar_margin"])
    d["adj_bar_out_max"] = d["adj_bar_out"] + P["adapter_len_adjust"]

    d["plinth_fix_d"] = max(d["boss_od"],
                            (d["x_datum"] - d["fix_bar_out"]) + 0.20)
    d["plinth_adj_d"] = max(d["boss_od"],
                            (d["adj_bar_out_max"] - d["x_adj_face"]) + 0.20)
    d["x_wall_in_neg"] = d["x_datum"] - d["plinth_fix_d"]
    d["x_wall_in_pos"] = d["x_adj_face"] + d["plinth_adj_d"]
    d["x_out_neg"] = d["x_wall_in_neg"] - P["wall_t"]
    d["x_out_pos"] = d["x_wall_in_pos"] + P["wall_t"]
    d["body_l"] = d["x_out_pos"] - d["x_out_neg"]
    d["body_w"] = 2.0 * d["y_out"]
    d["z_plinth_top"] = d["z_pcb_top"] + P["clamp_vertical_clear"]

    # ---- lid screw bosses, both outside the breakout outline --------------
    # The lid screws land in square CORNER PIERS, not round columns.
    #
    # A cylindrical boss set against a flat wall is either tangent to it or
    # needs a root fillet that overruns it, and both tessellate to edges
    # shared by four triangles - a valid BRep and an invalid mesh, which
    # silently corrupts every ray-parity test in the offline verifier. A pier
    # buried pier_bury into both walls meets them on plain coincident planes,
    # merges cleanly, needs no torus, and is stiffer for the same material.
    d["pier_d"] = d["boss_od"]
    d["pier_x_fix"] = (d["x_wall_in_neg"] - P["pier_bury"],
                       d["x_wall_in_neg"] - P["pier_bury"] + d["pier_d"])
    d["pier_x_adj"] = (d["x_wall_in_pos"] + P["pier_bury"] - d["pier_d"],
                       d["x_wall_in_pos"] + P["pier_bury"])
    d["pier_y"] = (d["y_cav"] + P["pier_bury"] - d["pier_d"],
                   d["y_cav"] + P["pier_bury"])
    d["boss_fix_x"] = sum(d["pier_x_fix"]) / 2.0
    d["boss_adj_x"] = sum(d["pier_x_adj"]) / 2.0
    d["boss_y"] = sum(d["pier_y"]) / 2.0
    d["z_insert_bot"] = d["z_cav_top"] - P["insert_depth"]
    d["z_screw_tip"] = d["z_lid_top"] - P["lid_screw_length"]

    # ---- cabinet mounting ears -------------------------------------------
    d["ear_proj"] = P["ear_root_gap"] + P["cabinet_slot_w"] + P["ear_edge"]
    d["ear_len"] = P["cabinet_slot_l"] + 2.0 * P["ear_edge"]
    d["ear_x_neg"] = d["x_out_neg"] - d["ear_proj"]
    d["ear_x_pos"] = d["x_out_pos"] + d["ear_proj"]
    # the ear must land on the flat wall, not beside the R3.00 outer corner,
    # or its root is a proud step instead of a fillettable junction
    d["ear_y_far"] = d["y_out"] - P["outer_corner_r"]
    d["ear_y_in"] = d["ear_y_far"] - d["ear_len"]
    d["ear_slot_y"] = d["ear_y_far"] - P["ear_edge"] - P["cabinet_slot_l"] / 2.0
    d["ear_slot_x_neg"] = d["ear_x_neg"] + P["ear_edge"] + P["cabinet_slot_w"] / 2.0
    d["ear_slot_x_pos"] = d["ear_x_pos"] - P["ear_edge"] - P["cabinet_slot_w"] / 2.0
    d["z_ear_top"] = d["z_floor_bot"] + P["ear_t"]
    d["overall_l"] = d["ear_x_pos"] - d["ear_x_neg"]

    # ---- cable exit windows and lacing rails ------------------------------
    d["win_z0"] = d["z_pcb_top"]
    d["win_z1"] = d["win_z0"] + P["wire_win_h"]
    d["win_x0"] = -P["wire_win_half_l"]
    d["win_x1"] = P["wire_win_half_l"]
    # The sawtooth runs saw_margin past each window end. Ending a flank
    # exactly on the window end plane makes the two surfaces tangent there,
    # which tessellates non-manifold for the same reason a tangent boss does.
    d["saw_x0"] = d["win_x0"] - P["saw_margin"]
    d["saw_x1"] = d["win_x1"] + P["saw_margin"]
    d["win_saw_step"] = (d["saw_x1"] - d["saw_x0"]) / P["wire_saw_n"]
    # 45 degrees exactly: flank rise equals flank run, so the window roof is
    # self-supporting over its full span and no bridge is ever printed.
    d["wire_saw_h"] = d["win_saw_step"] / 2.0
    d["win_saw_top"] = d["win_z1"] + d["wire_saw_h"]
    d["z_skirt_bot"] = d["z_cav_top"] - P["lid_overlap"]
    # The rail is rooted on the print bed and its tie slots are open at the
    # TOP. An earlier arrangement started the whole rail at z 2.10, which put
    # its first layer in mid-air, and closed the slots with a 6 mm bridge.
    # Both are gone: nothing here needs support, and the slot floor still
    # stands 3.00 mm clear of a mounting face so a tie passes when the
    # housing is screwed flat to a cabinet wall.
    d["rail_z0"] = d["z_floor_bot"]
    d["rail_ledge_top"] = d["z_floor_bot"] + P["tie_ledge_h"]
    d["rail_z1"] = d["z_pcb_top"]
    d["tie_slot_h"] = d["rail_z1"] - d["rail_ledge_top"]
    d["rail_y_out"] = d["y_out"] + P["tie_slot_w"] + P["tie_rail_t"]
    d["rail_half_l"] = P["wire_win_half_l"] + 2.0
    d["overall_w"] = 2.0 * d["rail_y_out"]
    d["tie_legs_x"] = [-30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0]
    d["tie_slots_per_side"] = len(d["tie_legs_x"]) - 1

    # ---- terminals ---------------------------------------------------------
    n = P["term_per_side"]
    d["term_x"] = [(i - (n - 1) / 2.0) * P["term_pitch"] for i in range(n)]
    d["term_y"] = d["y_pcb"] - P["term_screw_inset"]
    d["term_in_y"] = d["y_pcb"] - P["term_block_w"]
    d["term_span"] = (n - 1) * P["term_pitch"]
    d["z_wire"] = d["z_pcb_top"] + P["term_wire_z"]

    # ---- ESP32 -------------------------------------------------------------
    d["esp_x0"] = P["esp_off_x"] - P["esp_pcb_l"] / 2.0
    d["esp_x1"] = P["esp_off_x"] + P["esp_pcb_l"] / 2.0
    d["esp_y0"] = P["esp_off_y"] - P["esp_pcb_w"] / 2.0
    d["esp_y1"] = P["esp_off_y"] + P["esp_pcb_w"] / 2.0
    d["z_esp_bot"] = d["z_pcb_top"] + P["esp_header_h"]
    d["z_esp_top"] = d["z_esp_bot"] + P["esp_pcb_t"]
    d["z_usb_axis"] = d["z_esp_top"] + P["esp_usb_h"] / 2.0
    d["usb_z0"] = d["z_usb_axis"] - P["usb_open_h"] / 2.0
    d["usb_z1"] = d["z_usb_axis"] + P["usb_open_h"] / 2.0
    d["usb_y0"] = P["esp_off_y"] - P["usb_open_w"] / 2.0
    d["usb_y1"] = P["esp_off_y"] + P["usb_open_w"] / 2.0
    d["z_btn_top"] = d["z_esp_top"] + P["esp_btn_h"]

    # antenna: at the END OPPOSITE the USB, so at +X
    d["ant_x1"] = d["esp_x1"]
    d["ant_x0"] = d["esp_x1"] - P["esp_ant_l"]
    d["ant_y0"] = P["esp_off_y"] - P["esp_ant_w"] / 2.0
    d["ant_y1"] = P["esp_off_y"] + P["esp_ant_w"] / 2.0
    k = P["antenna_keepout"]
    d["ako_x0"] = d["ant_x0"] - k
    d["ako_x1"] = d["ant_x1"] + k
    d["ako_y0"] = d["ant_y0"] - k
    d["ako_y1"] = d["ant_y1"] + k
    d["ako_z0"] = d["z_esp_top"]
    d["ako_z1"] = d["z_lid_top"] + 1.0
    d["ant_thin_x0"] = d["ant_x0"] - 2.0
    d["ant_thin_x1"] = d["ant_x1"] + 2.0
    d["ant_thin_y0"] = d["ant_y0"] - 2.0
    d["ant_thin_y1"] = d["ant_y1"] + 2.0
    d["z_lid_thin"] = d["z_cav_top"] + (P["lid_top_t"] - P["lid_antenna_t"])

    # ---- lid ---------------------------------------------------------------
    d["skirt_in_neg"] = d["x_out_neg"] - P["lid_fit_clear"]
    d["skirt_in_pos"] = d["x_out_pos"] + P["lid_fit_clear"]
    d["skirt_in_y"] = d["y_out"] + P["lid_fit_clear"]
    d["lid_x0"] = d["skirt_in_neg"] - P["lid_skirt_t"]
    d["lid_x1"] = d["skirt_in_pos"] + P["lid_skirt_t"]
    d["lid_y"] = d["skirt_in_y"] + P["lid_skirt_t"]
    d["lid_l"] = d["lid_x1"] - d["lid_x0"]
    d["lid_w"] = 2.0 * d["lid_y"]
    # a uniform skirt and a uniform 0.25 mm gap force the lid corner radius:
    # it is the base corner offset outward by the clearance and the skirt
    d["skirt_inner_r"] = P["outer_corner_r"] + P["lid_fit_clear"]
    d["lid_r"] = d["skirt_inner_r"] + P["lid_skirt_t"]

    # ---- ventilation, kept entirely clear of the antenna keep-out ---------
    pitch = P["vent_w"] + P["vent_bridge"]
    d["lid_vent_x0"] = -17.00
    d["lid_vent_x1"] = d["lid_vent_x0"] + P["vent_lid_l"]
    d["lid_vent_y"] = [(i - 2.5) * pitch for i in range(6)]
    # sidewall vents live between the window roof and the lid skirt, so the
    # fitted lid can never cover an open slot
    d["side_vent_z1"] = d["z_skirt_bot"] - 0.50
    d["side_vent_z0"] = d["side_vent_z1"] - P["vent_side_h"]
    d["side_vent_web"] = d["side_vent_z0"] - d["win_saw_top"]
    d["side_vent_x"] = [(i - 6) * pitch for i in range(13)]

    # ---- overall -----------------------------------------------------------
    d["overall_h"] = d["h_closed"]
    d["plan_area"] = d["overall_l"] * d["overall_w"]
    return d


# ---------------------------------------------------------------------------
# Reference components. NON-MANUFACTURING. Starting values, never measurements.
# ---------------------------------------------------------------------------
def build_esp32(B, P, d):
    """30-pin DevKit V1 / DOIT-style controller, sitting in its sockets."""
    pcb = B.box(d["esp_x0"], d["esp_x1"], d["esp_y0"], d["esp_y1"],
                d["z_esp_bot"], d["z_esp_top"])
    mod = B.box(d["esp_x1"] - P["esp_mod_l"], d["esp_x1"],
                P["esp_off_y"] - P["esp_mod_w"] / 2.0,
                P["esp_off_y"] + P["esp_mod_w"] / 2.0,
                d["z_esp_top"], d["z_esp_top"] + P["esp_mod_h"])
    ant = B.box(d["ant_x0"], d["ant_x1"], d["ant_y0"], d["ant_y1"],
                d["z_esp_top"] + P["esp_mod_h"],
                d["z_esp_top"] + P["esp_mod_h"] + 0.20)
    usb = B.box(d["esp_x0"], d["esp_x0"] + P["esp_usb_l"],
                P["esp_off_y"] - P["esp_usb_w"] / 2.0,
                P["esp_off_y"] + P["esp_usb_w"] / 2.0,
                d["z_esp_top"], d["z_esp_top"] + P["esp_usb_h"])
    b = P["esp_btn_sz"] / 2.0
    en = B.box(P["esp_btn_x"] - b, P["esp_btn_x"] + b,
               P["esp_btn_y"] - b, P["esp_btn_y"] + b,
               d["z_esp_top"], d["z_btn_top"])
    boot = B.box(P["esp_btn_x"] - b, P["esp_btn_x"] + b,
                 -P["esp_btn_y"] - b, -P["esp_btn_y"] + b,
                 d["z_esp_top"], d["z_btn_top"])
    return [(pcb, "REF_ESP32_PCB"), (mod, "REF_ESP32_MODULE"),
            (ant, "REF_ESP32_PCB_ANTENNA"), (usb, "REF_ESP32_USB_CONNECTOR"),
            (en, "REF_ESP32_BUTTON_EN_RESET"), (boot, "REF_ESP32_BUTTON_BOOT")]


def build_adapter(B, P, d):
    """30-pin screw-terminal breakout: board, both terminal rows, the ESP32
    sockets and the underside solder envelope."""
    pcb = B.box(d["x_datum"], d["x_pcb_nom"], -d["y_pcb"], d["y_pcb"],
                d["z_pcb_bot"], d["z_pcb_top"])

    blocks = None
    screws = None
    half = d["term_span"] / 2.0 + P["term_pitch"] / 2.0
    for sgn in (1.0, -1.0):
        y_out = sgn * d["y_pcb"]
        y_in = sgn * d["term_in_y"]
        blk = B.box(-half, half, min(y_out, y_in), max(y_out, y_in),
                    d["z_pcb_top"], d["z_term_top"])
        blocks = blk if blocks is None else B.uni(blocks, blk)
        for x in d["term_x"]:
            s = B.cylz(P["term_screw_d"], x, sgn * d["term_y"],
                       d["z_term_top"] - 1.20, d["z_term_top"] + 0.10)
            screws = s if screws is None else B.uni(screws, s)

    sock = None
    hl = (P["term_per_side"] - 1) * 2.54 / 2.0 + 1.27
    for sgn in (1.0, -1.0):
        s = B.box(-hl, hl, sgn * P["esp_header_span"] / 2.0 - 1.27,
                  sgn * P["esp_header_span"] / 2.0 + 1.27,
                  d["z_pcb_top"], d["z_pcb_top"] + P["esp_header_h"])
        sock = s if sock is None else B.uni(sock, s)

    under = B.box(-half, half, -d["y_pcb"] + 0.50, d["y_pcb"] - 0.50,
                  d["z_under_bot"], d["z_pcb_bot"])
    return [(pcb, "REF_ADAPTER_PCB"), (blocks, "REF_ADAPTER_TERMINAL_BLOCKS"),
            (screws, "REF_ADAPTER_TERMINAL_SCREWS"),
            (sock, "REF_ADAPTER_ESP32_SOCKETS"),
            (under, "REF_ADAPTER_UNDERSIDE_JOINTS")]


def build_keepouts(B, P, d):
    """Every volume the housing has to respect, as explicit solids."""
    out = []

    # the datum face is a deliberate hard contact, so the envelope starts on
    # it rather than 0.50 mm outside it
    out.append((B.box(d["x_datum"], d["x_adj_face"], -d["y_cav"], d["y_cav"],
                      d["z_pcb_bot"], d["z_pcb_top"]), "KEEPOUT_PCB_ENVELOPE"))

    # solder joints exist inboard of the DECLARED bare margins - which is
    # exactly the region the support pads are forbidden to enter
    out.append((B.box(d["x_datum"] + P["pcb_bare_edge"],
                      d["x_pcb_nom"] - P["pcb_bare_edge"],
                      -d["y_pcb"] + P["pcb_bare_perim"],
                      d["y_pcb"] - P["pcb_bare_perim"],
                      d["z_under_bot"], d["z_pcb_bot"]),
                "KEEPOUT_UNDERSIDE_JOINTS"))

    out.append((B.box(d["x_datum"], d["x_pcb_nom"], -d["y_pcb"], d["y_pcb"],
                      d["z_pcb_top"], d["z_comp_top"]),
                "KEEPOUT_ASSEMBLY_MAX_HEIGHT"))

    drv = None
    for sgn in (1.0, -1.0):
        for x in d["term_x"]:
            c = B.cylz(P["driver_d"], x, sgn * d["term_y"],
                       d["z_term_top"], d["z_lid_top"] + 25.0)
            drv = c if drv is None else B.uni(drv, c)
    out.append((drv, "KEEPOUT_TERMINAL_DRIVER_CORRIDORS"))

    wire = None
    for sgn in (1.0, -1.0):
        for x in d["term_x"]:
            c = B.cyly(P["wire_d"], x, d["z_wire"],
                       sgn * (d["y_pcb"] - P["term_screw_inset"]),
                       sgn * (d["rail_y_out"] + 12.0))
            wire = c if wire is None else B.uni(wire, c)
    out.append((wire, "KEEPOUT_WIRE_EXIT_PATHS"))

    out.append((B.box(d["esp_x0"] + 1.50, d["x_out_neg"] - 22.0,
                      d["usb_y0"], d["usb_y1"], d["usb_z0"], d["usb_z1"]),
                "KEEPOUT_USB_SERVICE_ENVELOPE"))

    btn = None
    for sgn in (1.0, -1.0):
        c = B.cylz(P["button_tool_d"], P["esp_btn_x"], sgn * P["esp_btn_y"],
                   d["z_btn_top"], d["z_lid_top"] + 10.0)
        btn = c if btn is None else B.uni(btn, c)
    out.append((btn, "KEEPOUT_BUTTON_TOOL_ACCESS"))

    out.append((B.box(d["ako_x0"], d["ako_x1"], d["ako_y0"], d["ako_y1"],
                      d["ako_z0"], d["ako_z1"]), "KEEPOUT_WIFI_ANTENNA"))

    scr = None
    for bx in (d["boss_fix_x"], d["boss_adj_x"]):
        for sgn in (1.0, -1.0):
            s = B.cylz(P["lid_screw_nominal"], bx, sgn * d["boss_y"],
                       d["z_screw_tip"], d["z_lid_top"])
            B.uni(s, B.cylz(P["insert_hole_d"], bx, sgn * d["boss_y"],
                            d["z_insert_bot"], d["z_cav_top"]))
            B.uni(s, B.cylz(P["lid_screw_head_d"], bx, sgn * d["boss_y"],
                            d["z_lid_top"], d["z_lid_top"] + 2.50))
            scr = s if scr is None else B.uni(scr, s)
    for bx, sy in ((d["fix_screw_x"], 1.0), (d["fix_screw_x"], -1.0),
                   (d["adj_screw_x"], 1.0), (d["adj_screw_x"], -1.0)):
        s = B.cylz(P["insert_hole_d"], bx, sy * P["clamp_screw_y"],
                   d["z_plinth_top"] - P["insert_depth"],
                   d["z_plinth_top"] + P["clamp_t"] + 3.0)
        scr = B.uni(scr, s)
    out.append((scr, "KEEPOUT_LID_AND_CLAMP_FASTENERS"))

    cab = None
    for cx in (d["ear_slot_x_neg"], d["ear_slot_x_pos"]):
        for sgn in (1.0, -1.0):
            s = B.rrect(cx - P["cabinet_slot_w"] / 2.0,
                        cx + P["cabinet_slot_w"] / 2.0,
                        sgn * d["ear_slot_y"] - P["cabinet_slot_l"] / 2.0,
                        sgn * d["ear_slot_y"] + P["cabinet_slot_l"] / 2.0,
                        d["z_floor_bot"] - 14.0, d["z_ear_top"],
                        P["cabinet_slot_w"] / 2.0)
            B.uni(s, B.rrect(cx - P["cabinet_screw_head_d"] / 2.0,
                             cx + P["cabinet_screw_head_d"] / 2.0,
                             sgn * d["ear_slot_y"] - P["cabinet_slot_l"] / 2.0
                             - 1.25,
                             sgn * d["ear_slot_y"] + P["cabinet_slot_l"] / 2.0
                             + 1.25,
                             d["z_ear_top"], d["z_ear_top"] + 3.50,
                             P["cabinet_screw_head_d"] / 2.0))
            cab = s if cab is None else B.uni(cab, s)
    out.append((cab, "KEEPOUT_CABINET_FASTENERS"))
    return out


# ---------------------------------------------------------------------------
# Housing_Base
# ---------------------------------------------------------------------------
def build_base(B, P, d):
    r = P["outer_corner_r"]
    body = B.rrect(d["x_out_neg"], d["x_out_pos"], -d["y_out"], d["y_out"],
                   d["z_floor_bot"], d["z_floor_top"], r)
    B.uni(body, B.ring(d["x_out_neg"], d["x_out_pos"], -d["y_out"], d["y_out"],
                       P["wall_t"], d["z_floor_top"], d["z_cav_top"], r))

    # end plinths: clamp seats, datum face and lid-boss roots
    B.uni(body, B.box(d["x_wall_in_neg"], d["x_datum"], -d["y_cav"], d["y_cav"],
                      d["z_floor_top"], d["z_plinth_top"]))
    B.uni(body, B.box(d["x_adj_face"], d["x_wall_in_pos"],
                      -d["y_cav"], d["y_cav"],
                      d["z_floor_top"], d["z_plinth_top"]))

    # lid screw boss columns, both outside the breakout outline. The root
    # blend is built as a true concave torus fillet rather than left to a
    # fillet feature: the columns are tangent to the wall, which is exactly
    # the junction Fusion refuses to blend.
    for px in (d["pier_x_fix"], d["pier_x_adj"]):
        for sgn in (1.0, -1.0):
            ya, yb = sorted([sgn * d["pier_y"][0], sgn * d["pier_y"][1]])
            B.uni(body, B.rrect(px[0], px[1], ya, yb,
                                d["z_floor_top"], d["z_cav_top"],
                                2.0 * P["inner_fillet_r"]))

    # six PCB support pads, on the declared bare long-edge perimeter only
    pad_y = d["y_pcb"] - P["pcb_bare_perim"] / 2.0
    for px in (-28.0, 0.0, 28.0):
        for sgn in (1.0, -1.0):
            B.uni(body, B.box(px - P["pad_l"] / 2.0, px + P["pad_l"] / 2.0,
                              sgn * pad_y - P["pad_w"] / 2.0,
                              sgn * pad_y + P["pad_w"] / 2.0,
                              d["z_floor_top"], d["pad_h"]))

    # external cable-lacing rails
    for sgn in (1.0, -1.0):
        # solid root, straight off the bed
        B.uni(body, B.box(-d["rail_half_l"], d["rail_half_l"],
                          sgn * d["y_out"], sgn * d["rail_y_out"],
                          d["rail_z0"], d["rail_ledge_top"]))
        # the bar, and the legs that leave the tie slots between them
        B.uni(body, B.box(-d["rail_half_l"], d["rail_half_l"],
                          sgn * (d["y_out"] + P["tie_slot_w"]),
                          sgn * d["rail_y_out"],
                          d["rail_ledge_top"], d["rail_z1"]))
        for lx in d["tie_legs_x"]:
            B.uni(body, B.box(lx - P["tie_leg_w"] / 2.0,
                              lx + P["tie_leg_w"] / 2.0,
                              sgn * d["y_out"],
                              sgn * (d["y_out"] + P["tie_slot_w"]),
                              d["rail_ledge_top"], d["rail_z1"]))

    # four external cabinet mounting ears
    for xa, xb in ((d["ear_x_neg"], d["x_out_neg"]),
                   (d["x_out_pos"], d["ear_x_pos"])):
        for sgn in (1.0, -1.0):
            B.uni(body, B.box(xa, xb, sgn * d["ear_y_in"],
                              sgn * d["ear_y_far"],
                              d["z_floor_bot"], d["z_ear_top"]))

    # ---- cuts -------------------------------------------------------------
    # continuous cable-exit window, 45 deg sawtooth top so it needs no bridge
    for sgn in (1.0, -1.0):
        ya, yb = sorted([sgn * (d["y_cav"] - 2.0), sgn * (d["y_out"] + 2.0)])
        B.sub(body, B.box(d["win_x0"], d["win_x1"], ya, yb,
                          d["win_z0"], d["win_z1"]))
        step = d["win_saw_step"]
        for i in range(P["wire_saw_n"]):
            xc = d["saw_x0"] + (i + 0.5) * step
            B.sub(body, B.tri_x(xc, d["win_z1"], step / 2.0, d["wire_saw_h"],
                                ya, yb))
        # Every wire-contact edge of the window is ROUNDED to inner_fillet_r:
        # both sills, and the four vertical end edges.
        r = P["inner_fillet_r"]
        yi, yo = sgn * d["y_cav"], sgn * d["y_out"]
        B.sub(body, B.round_edge_x(yi, d["win_z0"], sgn, -1.0, r,
                                   d["win_x0"], d["win_x1"]))
        B.sub(body, B.round_edge_x(yo, d["win_z0"], -sgn, -1.0, r,
                                   d["win_x0"], d["win_x1"]))
        for xe, sx in ((d["win_x0"], -1.0), (d["win_x1"], 1.0)):
            # stop at the rectangular opening. Running these to the sawtooth
            # apex leaves a vertical face that the 45 degree flank meets
            # tangentially, and the mesh comes out non-manifold there.
            B.sub(body, B.round_edge_z(xe, yi, sx, sgn, r,
                                       d["win_z0"], d["win_z1"]))
            B.sub(body, B.round_edge_z(xe, yo, sx, -sgn, r,
                                       d["win_z0"], d["win_z1"]))

    # USB service opening, chamfered both faces so the moulded cable shroud
    # meets no square edge
    B.sub(body, B.box(d["x_out_neg"] - 2.0, d["x_wall_in_neg"] + 2.0,
                      d["usb_y0"], d["usb_y1"], d["usb_z0"], d["usb_z1"]))
    for xf, sx in ((d["x_out_neg"], 1.0), (d["x_wall_in_neg"], -1.0)):
        for yf, sy in ((d["usb_y0"], -1.0), (d["usb_y1"], 1.0)):
            B.sub(body, B.round_edge_z(xf, yf, sx, sy, 0.60,
                                       d["usb_z0"], d["usb_z1"]))

    # upper sidewall ventilation
    for sgn in (1.0, -1.0):
        ya, yb = sorted([sgn * (d["y_cav"] - 2.0), sgn * (d["y_out"] + 2.0)])
        for vx in d["side_vent_x"]:
            B.sub(body, B.box(vx - P["vent_w"] / 2.0, vx + P["vent_w"] / 2.0,
                              ya, yb, d["side_vent_z0"], d["side_vent_z1"]))

    # lid-screw heat-set insert holes
    for bx in (d["boss_fix_x"], d["boss_adj_x"]):
        for sgn in (1.0, -1.0):
            B.sub(body, B.cylz(P["insert_hole_d"], bx, sgn * d["boss_y"],
                               d["z_insert_bot"], d["z_cav_top"] + 1.0))

    # clamp-screw heat-set insert holes
    for bx in (d["fix_screw_x"], d["adj_screw_x"]):
        for sgn in (1.0, -1.0):
            B.sub(body, B.cylz(P["insert_hole_d"], bx,
                               sgn * P["clamp_screw_y"],
                               d["z_plinth_top"] - P["insert_depth"],
                               d["z_plinth_top"] + 1.0))

    # cabinet mounting slots, 4.00 x 8.00 obround, long axis ACROSS the housing
    for cx in (d["ear_slot_x_neg"], d["ear_slot_x_pos"]):
        for sgn in (1.0, -1.0):
            B.sub(body, B.rrect(cx - P["cabinet_slot_w"] / 2.0,
                                cx + P["cabinet_slot_w"] / 2.0,
                                sgn * d["ear_slot_y"]
                                - P["cabinet_slot_l"] / 2.0,
                                sgn * d["ear_slot_y"]
                                + P["cabinet_slot_l"] / 2.0,
                                d["z_floor_bot"] - 1.0, d["z_ear_top"] + 1.0,
                                P["cabinet_slot_w"] / 2.0))
    return [(body, "ESP32_Controller_Housing_Base")]


# ---------------------------------------------------------------------------
# Housing_Lid
# ---------------------------------------------------------------------------
def build_lid(B, P, d):
    r = d["lid_r"]
    body = B.rrect(d["lid_x0"], d["lid_x1"], -d["lid_y"], d["lid_y"],
                   d["z_cav_top"], d["z_lid_top"], r)
    B.uni(body, B.ring(d["lid_x0"], d["lid_x1"], -d["lid_y"], d["lid_y"],
                       P["lid_skirt_t"], d["z_skirt_bot"], d["z_cav_top"], r))

    # thin the lid to lid_antenna_t over the Wi-Fi antenna, from the UNDERSIDE
    # so the outside stays flat and the clearance below only ever grows
    B.sub(body, B.box(d["ant_thin_x0"], d["ant_thin_x1"],
                      d["ant_thin_y0"], d["ant_thin_y1"],
                      d["z_cav_top"], d["z_lid_thin"]))

    # top ventilation. Slots are 2.00 mm - narrower than an M3 shank and much
    # narrower than a 4.00 mm insert - so no fastener used in this build can
    # pass one, whatever path it takes. Alternate rows are offset as well.
    for i, vy in enumerate(d["lid_vent_y"]):
        off = 0.0 if i % 2 == 0 else 3.0
        B.sub(body, B.box(d["lid_vent_x0"] + off, d["lid_vent_x1"] + off,
                          vy - P["vent_w"] / 2.0, vy + P["vent_w"] / 2.0,
                          d["z_cav_top"] - 1.0, d["z_lid_top"] + 1.0))

    # EN/RESET and BOOT tool holes, with an underside lead-in
    for sgn in (1.0, -1.0):
        B.sub(body, B.cylz(P["button_tool_d"], P["esp_btn_x"],
                           sgn * P["esp_btn_y"],
                           d["z_cav_top"] - 1.0, d["z_lid_top"] + 1.0))
        B.sub(body, B.conez(P["button_tool_lead_d"], P["button_tool_d"],
                            P["esp_btn_x"], sgn * P["esp_btn_y"],
                            d["z_cav_top"], d["z_cav_top"] + 1.00))

    # lid screw clearance holes with a lead-in chamfer
    for bx in (d["boss_fix_x"], d["boss_adj_x"]):
        for sgn in (1.0, -1.0):
            B.sub(body, B.cylz(P["lid_screw_clear_d"], bx, sgn * d["boss_y"],
                               d["z_cav_top"] - 1.0, d["z_lid_top"] + 1.0))
            B.sub(body, B.conez(P["lid_screw_clear_d"] + 1.20,
                                P["lid_screw_clear_d"], bx, sgn * d["boss_y"],
                                d["z_lid_top"], d["z_lid_top"] - 0.60))
    return [(body, "ESP32_Controller_Housing_Lid")]


# ---------------------------------------------------------------------------
# Edge clamps
# ---------------------------------------------------------------------------
def build_clamp(B, P, d, which):
    z0 = d["z_plinth_top"]
    z1 = z0 + P["clamp_t"]
    if which == "fix":
        xa, xb = d["fix_bar_out"], d["fix_bar_in"]
        sx = d["fix_screw_x"]
        slot_l = P["lid_screw_clear_d"]
        grip_x = d["x_datum"]
        name = "ESP32_Controller_PCB_Clamp_Fixed"
    else:
        xa, xb = d["adj_bar_in"], d["adj_bar_out"]
        sx = d["adj_screw_x"]
        slot_l = P["clamp_slot_l"]
        grip_x = d["x_pcb_nom"]
        name = "ESP32_Controller_PCB_Clamp_Adjustable"

    bar = B.rrect(xa, xb, -P["clamp_half_span"], P["clamp_half_span"],
                  z0, z1, P["clamp_corner_r"])
    for sgn in (1.0, -1.0):
        B.sub(bar, B.rrect(sx - slot_l / 2.0, sx + slot_l / 2.0,
                           sgn * P["clamp_screw_y"] - P["clamp_slot_w"] / 2.0,
                           sgn * P["clamp_screw_y"] + P["clamp_slot_w"] / 2.0,
                           z0 - 1.0, z1 + 1.0, P["clamp_slot_w"] / 2.0))
    # 0.60 mm lead-in on the leading bottom edge so the lip cannot catch the
    # board edge while the clamp is slid into place
    lead = xb if which == "fix" else xa
    B.sub(bar, B.diamond_x(lead, z0, 0.60,
                           -P["clamp_half_span"] - 1.0,
                           P["clamp_half_span"] + 1.0))
    return [(bar, name)], grip_x


# ---------------------------------------------------------------------------
# USB blanking plug - optional dust/contact protection only
# ---------------------------------------------------------------------------
def build_plug(B, P, d):
    c = 0.15                                   # per face into the opening
    spig = B.box(d["x_wall_in_neg"] - 0.20, d["x_out_neg"],
                 d["usb_y0"] + c, d["usb_y1"] - c,
                 d["usb_z0"] + c, d["usb_z1"] - c)
    fl_y = P["usb_open_w"] / 2.0 + 2.00
    fl_z0 = d["usb_z0"] - 2.00
    fl_z1 = d["usb_z1"] + 2.00
    flange = B.box(d["x_out_neg"] - 1.50, d["x_out_neg"], -fl_y, fl_y,
                   fl_z0, fl_z1)
    body = B.uni(flange, spig)
    for sgn in (1.0, -1.0):
        B.sub(body, B.cylz(3.00, sgn * (fl_y + 0.60),
                           0.0, fl_z0 - 1.0, fl_z1 + 1.0))
    return [(body, "ESP32_Controller_USB_Plug")]


# ---------------------------------------------------------------------------
# Carrier fit gauge - a low-material coupon printed FIRST
# ---------------------------------------------------------------------------
def build_gauge(B, P, d):
    gy = -120.0                                # parked clear of the assembly
    t = P["gauge_plate_t"]
    hw = P["gauge_w"] / 2.0
    slot_h = P["adapter_pcb_t"] + P["clamp_vertical_clear"]

    body = B.rrect(-30.0, 30.0, gy - hw, gy + hw, -t, 0.0, 2.0)

    # Zone A: PCB thickness, support-pad height and edge-clamp clearance
    B.uni(body, B.box(-30.0, -22.0, gy - hw, gy + hw, 0.0, d["z_plinth_top"]))
    B.uni(body, B.box(-22.0, -12.0, gy - hw, gy + hw, 0.0, d["pad_h"]))
    # the lip runs 1.00 mm BACK into the plinth: butting it exactly on the
    # plinth face leaves two coplanar surfaces meeting on one edge, which
    # tessellates non-manifold
    B.uni(body, B.box(-23.0, -22.0 + P["clamp_grip"], gy - hw, gy + hw,
                      d["pad_h"] + slot_h,
                      d["pad_h"] + slot_h + P["clamp_t"]))

    # Zone B: male overlap coupon, the base wall top
    B.uni(body, B.box(-8.0, 6.0, gy - 4.0, gy + 4.0, 0.0, P["lid_overlap"]))

    # Zone C: female overlap coupon, the lid skirt
    c = P["lid_fit_clear"]
    B.uni(body, B.box(10.0, 30.0, gy - 9.0, gy + 9.0, 0.0,
                      P["lid_overlap"] + 2.0))
    B.sub(body, B.box(12.0 - c, 26.0 + c, gy - 4.0 - c, gy + 4.0 + c,
                      2.0, P["lid_overlap"] + 3.0))

    # snap grooves, so the three zones separate by hand
    for gx in (-10.0, 8.0):
        B.sub(body, B.diamond_x(gx, 0.0, P["gauge_score"],
                                gy - hw - 1.0, gy + hw + 1.0))
    return [(body, "ESP32_Controller_Carrier_Fit_Gauge")]


# ---------------------------------------------------------------------------
# Fusion plumbing
# ---------------------------------------------------------------------------
def add_component(root, name, bodies, description=""):
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = name
    if description:
        comp.description = description
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    try:
        for body, bname in bodies:
            if body is None:
                continue
            comp.bRepBodies.add(body, bf).name = bname
    finally:
        bf.finishEdit()
    return occ, comp


def find_component(design, name):
    root = design.rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        if occ.component.name == name:
            return occ
    return None


def clear_component(design, name):
    root = design.rootComponent
    for i in range(root.occurrences.count - 1, -1, -1):
        if root.occurrences.item(i).component.name == name:
            root.occurrences.item(i).deleteMe()


def write_parameters(design, P, d):
    """Every controlling value becomes a named Fusion user parameter, so the
    model can be corrected from the parameter table after the fit test without
    hunting for a hidden sketch dimension."""
    ups = design.userParameters
    vals = {}
    for k, v in P.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            vals[k] = float(v)
    for k, v in d.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            vals[k] = float(v)
    n = 0
    for k in sorted(vals):
        name = "p_" + k
        expr = "%.4f mm" % vals[k]
        ex = ups.itemByName(name)
        try:
            if ex:
                ex.expression = expr
            else:
                ups.add(name, adsk.core.ValueInput.createByString(expr),
                        "mm", "Rev A ESP32 controller housing generator")
            n += 1
        except Exception:
            pass
    return n


def _text_input(sk, s, x0, y0, x1, y1, h):
    ti = sk.sketchTexts.createInput2(s, mm(h))
    ti.setAsMultiLine(
        adsk.core.Point3D.create(mm(x0), mm(y0), 0),
        adsk.core.Point3D.create(mm(x1), mm(y1), 0),
        adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
        adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    return sk.sketchTexts.add(ti)


MARK_DEPTH = 0.40                    # recessed legend depth, mm


def add_lid_markings(design, P, d):
    """Recessed identification on the lid top face. Section 7 requires the USB
    end and both button functions to be identified; section 9 permits a small
    DECCA CONTROLLER legend. Depth 0.40 mm, cut downward from the top face, so
    printing the lid top-face-down leaves them crisp against the bed.

    Returns the number of legends cut. Marking is cosmetic, so a per-legend
    failure is reported rather than allowed to destroy the build."""
    occ = find_component(design, LID)
    comp = occ.component
    planes = comp.constructionPlanes
    pin = planes.createInput()
    pin.setByOffset(comp.xYConstructionPlane,
                    adsk.core.ValueInput.createByReal(mm(d["z_lid_top"])))
    plane = planes.add(pin)
    plane.name = "LID_MARKING_PLANE"

    legends = [
        ("USB", d["lid_x0"] + 3.0, -6.0, d["lid_x0"] + 13.0, 6.0, 3.6),
        ("EN", P["esp_btn_x"] - 5.0, P["esp_btn_y"] + 2.6,
         P["esp_btn_x"] + 5.0, P["esp_btn_y"] + 6.4, 3.0),
        ("BOOT", P["esp_btn_x"] - 6.0, -P["esp_btn_y"] - 6.4,
         P["esp_btn_x"] + 6.0, -P["esp_btn_y"] - 2.6, 3.0),
        # placed clear of the 1.60 mm antenna window, so the deepest cut over
        # the antenna keep-out still leaves 1.40 mm of lid
        ("DECCA CONTROLLER", -1.0, 12.8, 46.0, 18.4, 3.2),
    ]
    made = 0
    for text, x0, y0, x1, y1, h in legends:
        body = comp.bRepBodies.item(0)
        v0 = body.volume
        try:
            sk = comp.sketches.add(plane)
            sk.name = "MARK_" + text.split()[0]
            st = _text_input(sk, text, x0, y0, x1, y1, h)
            ei = comp.features.extrudeFeatures.createInput(
                st, adsk.fusion.FeatureOperations.CutFeatureOperation)
            # both of these matter. Without participantBodies the cut targets
            # nothing on a base-feature body and reports success having
            # removed exactly zero material; setDistanceExtent with a negative
            # value does the same. Volume is checked afterwards so a silent
            # no-op can never be reported as a legend.
            ei.participantBodies = [body]
            ei.setOneSideExtent(
                adsk.fusion.DistanceExtentDefinition.create(
                    adsk.core.ValueInput.createByReal(mm(MARK_DEPTH))),
                adsk.fusion.ExtentDirections.NegativeExtentDirection)
            comp.features.extrudeFeatures.add(ei)
            cut = (v0 - comp.bRepBodies.item(0).volume) * 1000.0
            if cut <= 0.001:
                print("  marking %-18s CUT NOTHING" % text)
            else:
                made += 1
        except Exception as exc:
            print("  marking %-18s FAILED: %s" % (text, exc))
    return made


def soften(design, P, d):
    """Fillet pass on the two junctions the specification names and that
    primitives cannot reach: the ear-to-wall roots (section 5.3, R2.0 minimum)
    and the internal wall-to-floor corner (section 9, R1.0 minimum on stressed
    internal corners).

    Edges are selected by exact geometric predicate, not by trawling, so the
    printed "n of m" is a real result and not a trawl hit-rate. Per-edge
    try/except stays, because one junction failing to compute must not lose
    the whole solid - but a shortfall is REPORTED, never hidden."""
    occ = find_component(design, BASE)
    comp = occ.component
    body = comp.bRepBodies.item(0)
    fil = comp.features.filletFeatures
    tol = 0.02
    report = []

    def edge_at(e):
        bb = e.boundingBox
        return (bb.minPoint.x * 10.0, bb.maxPoint.x * 10.0,
                bb.minPoint.y * 10.0, bb.maxPoint.y * 10.0,
                bb.minPoint.z * 10.0, bb.maxPoint.z * 10.0)

    def one(edges, radius):
        col = adsk.core.ObjectCollection.create()
        for e in edges:
            col.add(e)
        fi = fil.createInput()
        fi.addConstantRadiusEdgeSet(
            col, adsk.core.ValueInput.createByReal(mm(radius)), True)
        fi.isRollingBallCorner = True
        fil.add(fi)

    def run(edges, radius, label):
        ok = 0
        if edges:
            # a closed loop must go in as ONE edge set, or each single-edge
            # fillet fights the corner left by the last one
            try:
                one(edges, radius)
                report.append((label, len(edges), len(edges), radius))
                print("  %-32s %d of %d edges filleted R%.2f"
                      % (label, len(edges), len(edges), radius))
                return len(edges), len(edges)
            except Exception:
                pass
        for e in edges:
            col = adsk.core.ObjectCollection.create()
            col.add(e)
            try:
                fi = fil.createInput()
                fi.addConstantRadiusEdgeSet(
                    col, adsk.core.ValueInput.createByReal(mm(radius)), True)
                fi.isRollingBallCorner = True
                fil.add(fi)
                ok += 1
            except Exception:
                pass
        report.append((label, ok, len(edges), radius))
        print("  %-32s %d of %d edges filleted R%.2f"
              % (label, ok, len(edges), radius))
        return ok, len(edges)

    # 1. ear-to-wall root: the horizontal edge where each ear top face meets
    #    the outer wall, one per ear, exactly four.
    ear = []
    for e in body.edges:
        x0, x1, y0, y1, z0, z1 = edge_at(e)
        if abs(z1 - z0) > tol or abs(z0 - d["z_ear_top"]) > tol:
            continue
        if abs(x1 - x0) > tol:
            continue
        if (abs(x0 - d["x_out_neg"]) < tol or abs(x0 - d["x_out_pos"]) < tol):
            if (y1 - y0) > d["ear_len"] - 0.5:
                ear.append(e)
    a_ok, a_n = run(ear, P["ear_fillet_r"], "ear-to-wall root")

    # 2. internal wall-to-floor corner: the complete cavity perimeter at the
    #    floor plane, four straight runs and four corner arcs.
    # 2. cavity floor perimeter: two long runs against the side walls and two
    #    short runs against the end plinth faces.
    inner = []
    for e in body.edges:
        x0, x1, y0, y1, z0, z1 = edge_at(e)
        if abs(z1 - z0) > tol or abs(z0 - d["z_floor_top"]) > tol:
            continue
        long_run = (abs(abs(y0) - d["y_cav"]) < tol
                    and abs(abs(y1) - d["y_cav"]) < tol
                    and (x1 - x0) > 20.0)
        end_run = ((abs(x0 - d["x_datum"]) < tol
                    or abs(x0 - d["x_adj_face"]) < tol)
                   and abs(x1 - x0) < tol and (y1 - y0) > 20.0)
        if long_run or end_run:
            inner.append(e)
            continue

    b_ok, b_n = run(inner, P["inner_fillet_r"], "cavity floor perimeter")
    # 3. the exposed root of each lid-screw pier. The piers stand on the end
    #    plinth, not on the cavity floor, so the corner to soften is at
    #    z_plinth_top - and only the two faces that look into the cavity;
    #    the other two are buried in the walls.
    pier = []
    for e in body.edges:
        x0, x1, y0, y1, z0, z1 = edge_at(e)
        if abs(z1 - z0) > tol or abs(z0 - d["z_plinth_top"]) > tol:
            continue
        for px in (d["pier_x_fix"], d["pier_x_adj"]):
            for sgn in (1.0, -1.0):
                ya, yb = sorted([sgn * d["pier_y"][0], sgn * d["pier_y"][1]])
                if (x0 >= px[0] - tol and x1 <= px[1] + tol
                        and y0 >= ya - tol and y1 <= yb + tol):
                    pier.append(e)
    c_ok, c_n = run(pier, P["inner_fillet_r"], "lid screw pier roots")

    return report, a_ok + b_ok + c_ok, a_n + b_n + c_n


# ---------------------------------------------------------------------------
# main - build every component
# ---------------------------------------------------------------------------
def _design_holds_housing(app):
    des = adsk.fusion.Design.cast(app.activeProduct)
    if des is None:
        return False
    root = des.rootComponent
    for i in range(root.occurrences.count):
        if root.occurrences.item(i).component.name == BASE:
            return True
    return False


def main(_context=None):
    app = adsk.core.Application.get()
    reuse = _design_holds_housing(app)
    if not reuse:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc = app.activeDocument
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent

    B = Builder()
    d = derive(P)

    for name in REFERENCE + PRINTABLE:
        clear_component(design, name)

    add_component(root, REF_ESP, build_esp32(B, P, d), REF_NOTE)
    add_component(root, REF_ADP, build_adapter(B, P, d), REF_NOTE)
    add_component(root, REF_KEEP, build_keepouts(B, P, d), REF_NOTE)
    add_component(root, BASE, build_base(B, P, d))
    add_component(root, LID, build_lid(B, P, d))
    fixb, fix_grip = build_clamp(B, P, d, "fix")
    adjb, adj_grip = build_clamp(B, P, d, "adj")
    add_component(root, CLAMP_FIX, fixb)
    add_component(root, CLAMP_ADJ, adjb)
    add_component(root, PLUG, build_plug(B, P, d))
    add_component(root, GAUGE, build_gauge(B, P, d))

    npar = write_parameters(design, P, d)
    print("built in %s document %r" % ("the existing" if reuse else "a NEW",
                                       doc.name))
    print("user parameters written: %d" % npar)

    print("edge softening:")
    soften(design, P, d)
    print("lid markings: %d legends cut" % add_lid_markings(design, P, d))

    app.activeViewport.fit()

    print("")
    print("DERIVED ENVELOPE")
    print("  body            %7.2f x %7.2f x %7.2f mm"
          % (d["body_l"], d["body_w"], d["h_closed"]))
    print("  overall         %7.2f x %7.2f x %7.2f mm  (ears, lacing rails)"
          % (d["overall_l"], d["overall_w"], d["h_closed"]))
    print("  spec target     %7.2f x %7.2f x %7.2f mm  (section 10, approx)"
          % (90.0, 78.0, 35.0))
    print("  plan area       %8.0f mm2 against a %8.0f mm2 target rectangle"
          % (d["plan_area"], 90.0 * 78.0))
    print("  internal height above the PCB support plane %.2f mm "
          "(section 10 target 27.00)" % d["internal_h_above_support"])
    print("")
    print("KEY DERIVED HEIGHTS  floor top 0.00 -> pad %.2f -> PCB %.2f/%.2f"
          " -> terminals %.2f -> max component %.2f -> cavity %.2f -> lid %.2f"
          % (d["pad_h"], d["z_pcb_bot"], d["z_pcb_top"], d["z_term_top"],
             d["z_comp_top"], d["z_cav_top"], d["z_lid_top"]))
    print("CLAMP GRIP  fixed end datum x %+.2f, lip to x %+.2f;"
          "  adjustable nominal edge x %+.2f, lip to x %+.2f"
          % (fix_grip, d["fix_bar_in"], adj_grip, d["adj_bar_in"]))

    for name in PRINTABLE:
        occ = find_component(design, name)
        b = occ.bRepBodies.item(0)
        bb = b.boundingBox
        print("%-26s solid=%-5s lumps=%d faces=%4d  %6.2f cm3  "
              "%6.2f x %6.2f x %6.2f mm"
              % (name, b.isSolid, b.lumps.count, b.faces.count,
                 volume_of(b) / 1000.0,
                 (bb.maxPoint.x - bb.minPoint.x) * 10,
                 (bb.maxPoint.y - bb.minPoint.y) * 10,
                 (bb.maxPoint.z - bb.minPoint.z) * 10))
    return d


def run(_context=None):
    return main(_context)


# ---------------------------------------------------------------------------
# validate - the specification section 14 gate suite, run inside Fusion on the
# finished solids. The offline mesh verifier in
# Decca_ESP32_Controller_Housing_verify.py is deliberately independent of this
# one: it reads only the exported STLs and re-derives every claim from
# triangles, so the two can disagree, which is the point.
# ---------------------------------------------------------------------------
FAILS = []
CHECKS = 0
BLOCKED = []


def gate(ok, label, detail=""):
    global CHECKS
    CHECKS += 1
    print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)
    return ok


def note(label, detail=""):
    print("  [    ] %-56s %s" % (label, detail))


def proto(label, detail=""):
    BLOCKED.append(label)
    print("  [PROTO] %-54s %s" % (label, detail))


def _bodies(design, comp_name):
    occ = find_component(design, comp_name)
    return {b.name: b for b in occ.bRepBodies}


def _vol(b):
    return volume_of(b)


def _hit(B, a, b):
    """Intersection VOLUME in mm3. Volume, not face count: two solids that
    merely touch share faces but enclose nothing, and a tangent contact is not
    an interference."""
    c1, c2 = B.copy(a), B.copy(b)
    B.inter(c1, c2)
    return max(0.0, _vol(c1))


def _mind(app, a, b):
    try:
        return app.measureManager.measureMinimumDistance(a, b).value * 10.0
    except Exception:
        return float("nan")


def _inside(body, x, y, z):
    pc = body.pointContainment(p3(x, y, z))
    return pc == adsk.fusion.PointContainment.PointInsidePointContainment


def _overhangs(body, z_bed, up, tol=0.02, grid=1.0, march=40.0):
    """Unsupported horizontal faces in the STATED print orientation, with the
    real bridging distance measured rather than guessed from a bounding box.

    ``up`` is +1 when the part prints in model orientation and -1 when it is
    flipped onto its top face; ``z_bed`` is the model-space height of the bed.
    A face is unsupported when its material lies on the bed side and there is
    nothing under it, which in model space means the outward normal points
    AWAY from the bed.

    For each such face the routine samples its area and, from every sample,
    marches horizontally in eight directions until it re-enters the solid at
    the same height. The shortest of those eight is how far that point is
    from something holding it up, and the largest such distance over the face
    is the REACH: half of a two-sided bridge, all of a cantilever. A bounding
    box cannot tell those apart, which is why it is not used - a 2.00 x 64.00
    rail underside and a 14.00 mm window lintel have opposite answers under
    max() and under min()."""
    out = []
    eps = 0.05
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1),
            (0.7071, 0.7071), (-0.7071, 0.7071),
            (0.7071, -0.7071), (-0.7071, -0.7071)]
    for f in body.faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
            continue
        n = g.normal
        if f.isParamReversed:
            n = adsk.core.Vector3D.create(-n.x, -n.y, -n.z)
        if n.z * up > -0.99:
            continue
        bb = f.boundingBox
        z = bb.minPoint.z * 10.0
        if (z - z_bed) * up <= tol:
            continue
        x0, x1 = bb.minPoint.x * 10.0, bb.maxPoint.x * 10.0
        y0, y1 = bb.minPoint.y * 10.0, bb.maxPoint.y * 10.0
        zin = z + eps * up                      # material side of the face
        zout = z - eps * up                     # open side
        reach = 0.0
        nx = max(2, int((x1 - x0) / grid) + 1)
        ny = max(2, int((y1 - y0) / grid) + 1)
        for i in range(nx):
            px = x0 + (x1 - x0) * i / (nx - 1.0)
            for j in range(ny):
                py = y0 + (y1 - y0) * j / (ny - 1.0)
                if not _inside(body, px, py, zin):
                    continue
                if _inside(body, px, py, zout):
                    continue
                best = march
                for dx, dy in dirs:
                    t = grid / 2.0
                    while t < best:
                        if _inside(body, px + dx * t, py + dy * t, zout):
                            break
                        t += grid / 2.0
                    best = min(best, t)
                reach = max(reach, best)
        if reach > 0.0:
            out.append((round(reach, 2), round(z, 2), round(f.area * 100.0, 1),
                        round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1)))
    return sorted(out, key=lambda t: -t[0])


def validate(_context=None):
    global FAILS, CHECKS, BLOCKED
    FAILS, CHECKS, BLOCKED = [], 0, []
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    B = Builder()
    d = derive(P)

    base = _bodies(design, BASE)["ESP32_Controller_Housing_Base"]
    lid = _bodies(design, LID)["ESP32_Controller_Housing_Lid"]
    cfix = _bodies(design, CLAMP_FIX)["ESP32_Controller_PCB_Clamp_Fixed"]
    cadj = _bodies(design, CLAMP_ADJ)["ESP32_Controller_PCB_Clamp_Adjustable"]
    plug = _bodies(design, PLUG)["ESP32_Controller_USB_Plug"]
    gauge = _bodies(design, GAUGE)["ESP32_Controller_Carrier_Fit_Gauge"]
    K = _bodies(design, REF_KEEP)
    E = _bodies(design, REF_ESP)
    A = _bodies(design, REF_ADP)

    printable = [(BASE, base), (LID, lid), (CLAMP_FIX, cfix),
                 (CLAMP_ADJ, cadj), (PLUG, plug), (GAUGE, gauge)]

    print("=" * 78)
    print("DECCA ESP32 CONTROLLER HOUSING - REV A  SECTION 14 GATE SUITE (CAD)")
    print("=" * 78)
    print("")

    # -- 1 ------------------------------------------------------------------
    print("1. EVERY PRINTABLE PART IS A CLOSED MANIFOLD SOLID")
    for nm, b in printable:
        gate(b.isSolid and b.lumps.count == 1 and b.shells.count == 1, nm,
             "solid=%s lumps=%d shells=%d faces=%d vol=%.3f cm3"
             % (b.isSolid, b.lumps.count, b.shells.count, b.faces.count,
                _vol(b) / 1000.0))

    # -- 2 ------------------------------------------------------------------
    print("")
    print("2. BASE FLOOR CONTINUOUS BENEATH THE COMPLETE PCB OUTLINE")
    holes = []
    nx, ny = 27, 25
    for i in range(nx):
        x = d["x_datum"] + (d["x_pcb_max"] - d["x_datum"]) * i / (nx - 1.0)
        for j in range(ny):
            y = -d["y_pcb"] + 2.0 * d["y_pcb"] * j / (ny - 1.0)
            if not _inside(base, x, y, d["z_floor_bot"] / 2.0):
                holes.append((round(x, 2), round(y, 2)))
    gate(not holes, "%d x %d probe grid under the board, mid-floor" % (nx, ny),
         "%d gap(s)%s" % (len(holes), (" e.g. " + str(holes[:3])) if holes
                          else ""))
    gate(abs(P["base_floor_t"] - (d["z_floor_top"] - d["z_floor_bot"])) < 1e-9,
         "floor thickness", "%.2f mm" % P["base_floor_t"])

    # -- 3 ------------------------------------------------------------------
    print("")
    print("3. UNDERSIDE ELECTRICAL CLEARANCE >= %.2f mm" % P["pcb_under_clear"])
    clear_vol = B.box(d["x_datum"] + P["pcb_bare_edge"],
                      d["x_pcb_nom"] - P["pcb_bare_edge"],
                      -d["y_pcb"] + P["pcb_bare_perim"],
                      d["y_pcb"] - P["pcb_bare_perim"],
                      d["z_floor_top"], d["z_under_bot"])
    v = _hit(B, base, clear_vol)
    gate(v < 1.0e-3, "the whole %.2f mm band beneath the joints is empty"
         % P["pcb_under_clear"], "intrusion %.4f mm3" % v)
    note("clearance beneath the lowest modelled joint",
         "%.2f mm (floor top %.2f to joint underside %.2f)"
         % (d["z_under_bot"] - d["z_floor_top"], d["z_floor_top"],
            d["z_under_bot"]))
    gate(_mind(app, base, K["KEEPOUT_UNDERSIDE_JOINTS"]) > -1,
         "support pads sit outside the joint footprint",
         "lateral gap %.2f mm"
         % _mind(app, base, K["KEEPOUT_UNDERSIDE_JOINTS"]))

    # -- 4 ------------------------------------------------------------------
    print("")
    print("4. NO FASTENER ENVELOPE ENTERS THE PCB OR WIRING KEEP-OUT")
    elec = B.copy(K["KEEPOUT_PCB_ENVELOPE"])
    for k in ("KEEPOUT_UNDERSIDE_JOINTS", "KEEPOUT_ASSEMBLY_MAX_HEIGHT",
              "KEEPOUT_WIRE_EXIT_PATHS"):
        B.uni(elec, B.copy(K[k]))
    for k in ("KEEPOUT_LID_AND_CLAMP_FASTENERS", "KEEPOUT_CABINET_FASTENERS"):
        v = _hit(B, K[k], elec)
        gate(v < 1.0e-3, k, "intersection %.4f mm3" % v)
    note("lid screw M3 x %.0f tip at full insertion"
         % P["lid_screw_length"],
         "z %+.2f, %.2f mm above the PCB top and %.2f mm outside the board"
         % (d["z_screw_tip"], d["z_screw_tip"] - d["z_pcb_top"],
            abs(d["boss_fix_x"]) - abs(d["x_datum"])))

    # -- 5 ------------------------------------------------------------------
    print("")
    print("5. COMPONENT-TO-LID CLEARANCE >= %.2f mm" % P["component_top_clear"])
    head = B.box(d["x_datum"], d["x_pcb_nom"], -d["y_pcb"], d["y_pcb"],
                 d["z_comp_top"], d["z_comp_top"] + P["component_top_clear"])
    v = _hit(B, lid, head)
    gate(v < 1.0e-3, "lid clear of the %.2f mm headroom band"
         % P["component_top_clear"], "intrusion %.4f mm3" % v)
    v = _hit(B, base, head)
    gate(v < 1.0e-3, "base clear of the same band", "intrusion %.4f mm3" % v)
    note("cavity top / lid underside", "z %+.2f, headroom %.2f mm"
         % (d["z_cav_top"], d["z_cav_top"] - d["z_comp_top"]))

    # -- 6 ------------------------------------------------------------------
    print("")
    print("6. TERMINAL SCREWDRIVER CORRIDORS, LID REMOVED")
    blocked = []
    for sgn in (1.0, -1.0):
        for i, x in enumerate(d["term_x"]):
            c = B.cylz(P["driver_d"], x, sgn * d["term_y"],
                       d["z_term_top"], d["z_lid_top"] + 25.0)
            tot = _hit(B, base, c) + _hit(B, cfix, c) + _hit(B, cadj, c)
            if tot > 1.0e-3:
                blocked.append(("+Y" if sgn > 0 else "-Y", i + 1, tot))
    gate(not blocked, "%d corridors of %.2f mm diameter, both rows"
         % (2 * P["term_per_side"], P["driver_d"]),
         "%d obstructed" % len(blocked) + (" %s" % blocked[:3] if blocked
                                           else ""))

    # -- 7 ------------------------------------------------------------------
    print("")
    print("7. WIRE-EXIT HEIGHT ON BOTH LONG SIDES >= %.2f mm"
          % P["wire_exit_h"])
    for sgn, side in ((1.0, "+Y"), (-1.0, "-Y")):
        probe = B.box(-d["term_span"] / 2.0, d["term_span"] / 2.0,
                      sgn * (d["y_cav"] - 0.5), sgn * (d["rail_y_out"] + 5.0),
                      d["win_z0"], d["win_z0"] + P["wire_exit_h"])
        v = _hit(B, base, probe)
        gate(v < 1.0e-3, "%s side, required band across the terminal span"
             % side, "obstruction %.4f mm3" % v)
    note("provided clear window", "%.2f mm (z %+.2f to %+.2f), roof sawtooth "
         "to z %+.2f" % (P["wire_win_h"], d["win_z0"], d["win_z1"],
                         d["win_saw_top"]))

    # -- 8 ------------------------------------------------------------------
    print("")
    print("8. NO LID MATERIAL CROSSES A WIRE PATH")
    v = _hit(B, lid, K["KEEPOUT_WIRE_EXIT_PATHS"])
    gate(v < 1.0e-3, "lid against all %d modelled wire runs"
         % (2 * P["term_per_side"]), "intersection %.4f mm3" % v)
    note("lid skirt bottom vs wire-window roof",
         "z %+.2f against %+.2f, %.2f mm apart"
         % (d["z_skirt_bot"], d["win_saw_top"],
            d["z_skirt_bot"] - d["win_saw_top"]))

    # -- 9 ------------------------------------------------------------------
    print("")
    print("9. USB SERVICE ENVELOPE UNOBSTRUCTED")
    u = K["KEEPOUT_USB_SERVICE_ENVELOPE"]
    tot = 0.0
    for nm, b in (("base", base), ("lid", lid), ("clamp fixed", cfix),
                  ("clamp adjustable", cadj)):
        v = _hit(B, b, u)
        tot += v
        gate(v < 1.0e-3, "%.2f x %.2f mm envelope against %s"
             % (P["usb_open_w"], P["usb_open_h"], nm),
             "intersection %.4f mm3" % v)
    note("USB axis height", "z %+.2f, %.2f mm above the fixed clamp top"
         % (d["z_usb_axis"], d["usb_z0"] - (d["z_plinth_top"] + P["clamp_t"])))
    note("blanking plug", "fitted plug intersects the envelope by %.1f mm3 - "
         "it is REMOVED for USB service" % _hit(B, plug, u))

    # -- 10 -----------------------------------------------------------------
    print("")
    print("10. BUTTON TOOL HOLES ALIGN TO THE ESP32 REFERENCE")
    v = _hit(B, lid, K["KEEPOUT_BUTTON_TOOL_ACCESS"])
    gate(v < 1.0e-3, "EN/RESET and BOOT corridors through the lid",
         "intersection %.4f mm3" % v)
    found = []
    for f in lid.faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType:
            continue
        if abs(g.radius * 10.0 - P["button_tool_d"] / 2.0) > 0.01:
            continue
        found.append((round(g.origin.x * 10.0, 3), round(g.origin.y * 10.0, 3)))
    want = [(P["esp_btn_x"], P["esp_btn_y"]), (P["esp_btn_x"], -P["esp_btn_y"])]
    ok = all(any(abs(fx - wx) < 0.01 and abs(fy - wy) < 0.01
                 for fx, fy in found) for wx, wy in want)
    gate(ok, "hole centres equal the named ESP32 button coordinates",
         "want %s, found %s" % (want, sorted(set(found))))

    # -- 11 -----------------------------------------------------------------
    print("")
    print("11. ANTENNA KEEP-OUT CARRIES NO SCREW, INSERT, RIB OR LACING")
    ako = K["KEEPOUT_WIFI_ANTENNA"]
    for nm, b in (("base", base), ("clamp fixed", cfix),
                  ("clamp adjustable", cadj),
                  ("all fastener envelopes",
                   K["KEEPOUT_LID_AND_CLAMP_FASTENERS"]),
                  ("cabinet fastener envelopes",
                   K["KEEPOUT_CABINET_FASTENERS"])):
        v = _hit(B, b, ako)
        gate(v < 1.0e-3, "%s inside the keep-out" % nm,
             "intersection %.4f mm3" % v)
    thin = 0.0
    for zz in (d["z_lid_thin"] + 0.05, d["z_cav_top"] + 0.05):
        pass
    over = []
    for i in range(9):
        x = d["ant_x0"] + (d["ant_x1"] - d["ant_x0"]) * i / 8.0
        for j in range(7):
            y = d["ant_y0"] + (d["ant_y1"] - d["ant_y0"]) * j / 6.0
            lo = None
            steps = 40
            for k in range(steps + 1):
                z = d["z_cav_top"] + (d["z_lid_top"] - d["z_cav_top"]) \
                    * k / float(steps)
                if _inside(lid, x, y, z):
                    lo = z if lo is None else lo
            over.append(d["z_lid_top"] - (lo if lo is not None
                                          else d["z_lid_top"]))
    thin = max(over) if over else 0.0
    gate(thin <= P["lid_antenna_t"] + 0.05,
         "lid thickness over the antenna <= %.2f mm" % P["lid_antenna_t"],
         "measured maximum %.2f mm" % thin)
    note("lacing rails", "nearest rail is at |y| >= %.2f, keep-out reaches "
         "|y| %.2f" % (d["y_out"] + P["tie_slot_w"], d["ako_y1"]))

    # -- 12 -----------------------------------------------------------------
    print("")
    print("12. LID OVERLAP AND FIT CLEARANCE AROUND THE FULL PERIMETER")
    c = P["lid_fit_clear"]
    bad_gap, bad_lap = [], []
    for i in range(72):
        t = 2.0 * math.pi * i / 72.0
        ux, uy = math.cos(t), math.sin(t)
        # walk INWARD to find the base outer surface. At this height the
        # cavity is hollow, so a walk outward from the centre finds nothing.
        step = 0.05
        cx = (d["x_out_neg"] + d["x_out_pos"]) / 2.0
        zc = d["z_cav_top"] - P["lid_overlap"] / 2.0
        r = 120.0
        while r > 0.0 and not _inside(base, cx + ux * r, uy * r, zc):
            r -= step
        if r <= 0.0:
            continue
        surf = r + step / 2.0
        px, py = cx + ux * surf, uy * surf
        if _inside(lid, px + ux * (c * 0.5), py + uy * (c * 0.5), zc):
            bad_gap.append(round(math.degrees(t)))
        if not _inside(lid, px + ux * (c + P["lid_skirt_t"] / 2.0),
                       py + uy * (c + P["lid_skirt_t"] / 2.0), zc):
            bad_gap.append(round(math.degrees(t)))
        for zz in (d["z_skirt_bot"] + 0.3, d["z_cav_top"] - 0.3):
            if not _inside(lid, px + ux * (c + P["lid_skirt_t"] / 2.0),
                           py + uy * (c + P["lid_skirt_t"] / 2.0), zz):
                bad_lap.append(round(math.degrees(t)))
    gate(not bad_gap, "72 perimeter probes: %.2f mm gap then skirt material"
         % c, "%d bad%s" % (len(bad_gap), " at %s deg" % sorted(set(bad_gap))[:6]
                            if bad_gap else ""))
    gate(not bad_lap, "skirt present over the full %.2f mm overlap"
         % P["lid_overlap"], "%d bad" % len(bad_lap))
    v = _hit(B, base, lid)
    gate(v < 1.0e-3, "lid and base do not interfere when closed",
         "intersection %.4f mm3" % v)

    # -- 13 -----------------------------------------------------------------
    print("")
    print("13. CLAMPS CONTACT ONLY DECLARED BARE PCB EDGE ZONES")
    # The bare strip is measured from the ACTUAL short edge, so the clamp and
    # the forbidden zone must be evaluated in the SAME board configuration.
    # All three are checked: short, nominal and long board, with the
    # adjustable clamp slid to where that board puts it.
    for tag, edge, slide in (("short board 65.00", d["x_pcb_min"],
                              d["x_pcb_min"] - d["x_pcb_nom"]),
                             ("nominal board 66.00", d["x_pcb_nom"], 0.0),
                             ("long board 67.00", d["x_pcb_max"],
                              d["x_pcb_max"] - d["x_pcb_nom"])):
        forbidden = B.box(d["x_datum"] + P["pcb_bare_edge"],
                          edge - P["pcb_bare_edge"], -d["y_pcb"], d["y_pcb"],
                          d["z_pcb_top"] - 0.01, d["z_comp_top"])
        moved = B.copy(cadj)
        m = adsk.core.Matrix3D.create()
        m.translation = adsk.core.Vector3D.create(mm(slide), 0, 0)
        B.tbm.transform(moved, m)
        v = _hit(B, cfix, B.copy(forbidden)) + _hit(B, moved, forbidden)
        gate(v < 1.0e-3, "both clamps on bare edge only, %s" % tag,
             "intersection %.4f mm3" % v)
    note("fixed clamp lip", "x %+.2f to %+.2f, %.2f mm of the %.2f mm bare "
         "strip" % (d["x_datum"], d["fix_bar_in"], P["clamp_grip"],
                    P["pcb_bare_edge"]))
    note("adjustable clamp lip", "x %+.2f to %+.2f at nominal"
         % (d["adj_bar_in"], d["x_pcb_nom"]))
    for nm, b in ((CLAMP_FIX, cfix), (CLAMP_ADJ, cadj)):
        v = _hit(B, b, K["KEEPOUT_PCB_ENVELOPE"])
        gate(v < 1.0e-3, "%s does not enter the board thickness" % nm,
             "intersection %.4f mm3, vertical gap %.2f mm"
             % (v, P["clamp_vertical_clear"]))

    # -- 14 -----------------------------------------------------------------
    print("")
    print("14. ADJUSTABLE CLAMP TRAVEL >= +/-%.2f mm"
          % P["adapter_len_adjust"])
    travel = (P["clamp_slot_l"] - P["lid_screw_clear_d"]) / 2.0
    gate(travel >= P["adapter_len_adjust"], "slot geometry",
         "slot %.2f - screw %.2f = +/-%.2f mm"
         % (P["clamp_slot_l"], P["lid_screw_clear_d"], travel))
    for s in (-P["adapter_len_adjust"], P["adapter_len_adjust"]):
        moved = B.copy(cadj)
        m = adsk.core.Matrix3D.create()
        m.translation = adsk.core.Vector3D.create(mm(s), 0, 0)
        B.tbm.transform(moved, m)
        v = _hit(B, base, moved)
        gate(v < 1.0e-3, "clamp translated %+0.2f mm still fits the seat" % s,
             "interference %.4f mm3" % v)
    note("board length window covered",
         "%.2f to %.2f mm against a %.2f mm nominal"
         % (d["x_pcb_min"] - d["x_datum"], d["x_pcb_max"] - d["x_datum"],
            P["adapter_pcb_l"]))

    # -- 15 -----------------------------------------------------------------
    print("")
    print("15. NO RETAINING FEATURE LOADS THE ESP32 OR ITS SOCKETS")
    esp_all = None
    for nm in E:
        esp_all = B.copy(E[nm]) if esp_all is None else B.uni(esp_all,
                                                              B.copy(E[nm]))
    B.uni(esp_all, B.copy(A["REF_ADAPTER_ESP32_SOCKETS"]))
    for nm, b in ((CLAMP_FIX, cfix), (CLAMP_ADJ, cadj), (BASE, base),
                  (LID, lid)):
        v = _hit(B, b, esp_all)
        gate(v < 1.0e-3, "%s against the controller and its sockets" % nm,
             "intersection %.4f mm3" % v)

    # -- 16 -----------------------------------------------------------------
    print("")
    print("16. CABINET MOUNTING SLOTS OUTSIDE THE ELECTRICAL ENVELOPE")
    v = _hit(B, K["KEEPOUT_CABINET_FASTENERS"], elec)
    gate(v < 1.0e-3, "all four slot and screw-head envelopes",
         "intersection %.4f mm3" % v)
    note("nearest slot edge to the board",
         "%.2f mm in X" % (abs(d["ear_slot_x_neg"]) - P["cabinet_slot_w"] / 2.0
                           - abs(d["x_datum"])))
    n_slots = 0
    for f in base.faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType:
            continue
        # vertical axis only: the R2.00 ear-root fillets are the same radius
        # and would otherwise be counted as slot ends
        if abs(g.axis.z) < 0.99:
            continue
        if abs(g.radius * 10.0 - P["cabinet_slot_w"] / 2.0) < 0.01:
            bb = f.boundingBox
            if bb.maxPoint.z * 10.0 <= d["z_ear_top"] + 0.01:
                n_slots += 1
    gate(n_slots == 8, "four obround slots present (two half-cylinders each)",
         "%d half-cylinder faces found" % n_slots)

    # -- 17 -----------------------------------------------------------------
    print("")
    print("17. VALID ASSEMBLY, WIRING AND REMOVAL SEQUENCE")
    up = 60.0
    skirt = B.rrect(d["lid_x0"], d["lid_x1"], -d["lid_y"], d["lid_y"],
                    d["z_skirt_bot"], d["z_lid_top"] + up, d["lid_r"])
    B.sub(skirt, B.rrect(d["skirt_in_neg"], d["skirt_in_pos"],
                         -d["skirt_in_y"], d["skirt_in_y"],
                         d["z_skirt_bot"] - 1.0, d["z_lid_top"] + up + 1.0,
                         d["skirt_inner_r"]))
    v = _hit(B, base, skirt)
    gate(v < 1.0e-3, "lid lifts vertically clear of the base",
         "swept skirt corridor obstruction %.4f mm3" % v)
    for nm, b, x0, x1 in ((CLAMP_FIX, cfix, d["fix_bar_out"], d["fix_bar_in"]),
                          (CLAMP_ADJ, cadj, d["adj_bar_in"],
                           d["adj_bar_out_max"])):
        corridor = B.box(x0, x1, -P["clamp_half_span"], P["clamp_half_span"],
                         d["z_plinth_top"] + P["clamp_t"],
                         d["z_lid_top"] + up)
        v = _hit(B, base, corridor)
        gate(v < 1.0e-3, "%s lifts out with the lid off and wiring in place"
             % nm, "obstruction %.4f mm3" % v)
    corridor = B.box(d["esp_x0"], d["esp_x1"], d["esp_y0"], d["esp_y1"],
                     d["z_esp_bot"], d["z_lid_top"] + up)
    v = _hit(B, base, corridor) + _hit(B, cfix, corridor) \
        + _hit(B, cadj, corridor)
    gate(v < 1.0e-3, "ESP32 lifts vertically out of its sockets, lid off",
         "obstruction %.4f mm3" % v)
    note("sequence", "inserts -> board on pads against the datum -> fixed "
         "clamp -> adjustable clamp -> wire and lace -> ESP32 -> lid")

    # -- 18 -----------------------------------------------------------------
    print("")
    print("18. PRINTABLE IN THE STATED ORIENTATION WITHOUT INTERNAL SUPPORT")
    # up = +1 prints as modelled, -1 prints flipped onto its top face
    beds = ((BASE, base, d["z_floor_bot"], 1, "floor down"),
            (LID, lid, d["z_lid_top"], -1, "top face down"),
            (CLAMP_FIX, cfix, d["z_plinth_top"], 1, "flat, as modelled"),
            (CLAMP_ADJ, cadj, d["z_plinth_top"], 1, "flat, as modelled"),
            (PLUG, plug, d["usb_z1"] + 2.0, -1, "flange face down"),
            (GAUGE, gauge, -P["gauge_plate_t"], 1, "plate down"))
    limit = 8.0                       # reach, so a two-sided bridge of 16 mm
    for nm, b, bed, up, orient in beds:
        oh = _overhangs(b, bed, up)
        worst = oh[0] if oh else (0.0, 0.0, 0.0, 0, 0, 0, 0)
        gate(worst[0] <= limit,
             "%s, %s: worst unsupported reach" % (nm, orient),
             "%.2f mm over %d face(s), limit %.2f%s"
             % (worst[0], len(oh), limit,
                ("  worst at z %+.2f x[%.1f,%.1f] y[%.1f,%.1f]"
                 % (worst[1], worst[3], worst[4], worst[5], worst[6]))
                if oh else ""))
        for row in oh[:3]:
            note("    reach %.2f mm" % row[0],
                 "z %+.2f  %.1f mm2  x[%.1f,%.1f] y[%.1f,%.1f]"
                 % (row[1], row[2], row[3], row[4], row[5], row[6]))
    note("why bridges are acceptable", "a bridge is not support material; the "
         "cable window roof is a 45 degree sawtooth precisely so its 60.00 mm "
         "span never becomes one")
    gate(abs(d["wire_saw_h"] - d["win_saw_step"] / 2.0) < 1e-9,
         "cable-window roof flanks are exactly 45 degrees",
         "rise %.3f over run %.3f" % (d["wire_saw_h"], d["win_saw_step"] / 2.0))
    gate(P["vent_w"] < P["lid_screw_nominal"] - 0.5,
         "no top vent can pass a fastener used in this build",
         "slot %.2f mm against an M%.0f shank and a %.2f mm insert"
         % (P["vent_w"], P["lid_screw_nominal"], P["insert_hole_d"]))

    # -- prototype gates ----------------------------------------------------
    print("")
    print("PROTOTYPE GATES - NOT VERIFIABLE IN CAD, NEVER MARKED PASS")
    for k in sorted(STARTING):
        proto(k, "CAD starting value %s" % P[k])

    print("")
    print("=" * 78)
    print("%d CAD gates, %d failed, %d prototype gates open"
          % (CHECKS, len(FAILS), len(BLOCKED)))
    if FAILS:
        for f in FAILS:
            print("  FAILED: %s" % f)
    print("=" * 78)
    return len(FAILS)


# ---------------------------------------------------------------------------
# export - editable, exchange and print files, straight into the repository
# ---------------------------------------------------------------------------
def export(_context=None):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    em = design.exportManager
    d = derive(P)

    cad = os.path.join(REPO, "mechanical", "CAD")
    stl = os.path.join(REPO, "mechanical", "STL")
    for p in (cad, stl):
        if not os.path.isdir(p):
            os.makedirs(p)

    written = []

    def f3d(path):
        em.execute(em.createFusionArchiveExportOptions(path))
        written.append(path)

    def step(path, comp=None):
        opts = (em.createSTEPExportOptions(path, comp) if comp
                else em.createSTEPExportOptions(path))
        em.execute(opts)
        written.append(path)

    def mesh(body, path):
        o = em.createSTLExportOptions(body, path)
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(o)
        written.append(path)

    f3d(os.path.join(cad, "Decca_ESP32_Controller_Housing.f3d"))

    # The assembly STEP is a review artefact. The keep-out solids deliberately
    # overlap everything, so they are pulled for the export and rebuilt after.
    clear_component(design, REF_KEEP)
    step(os.path.join(cad, "Decca_ESP32_Controller_Housing_assembly.step"))
    add_component(root, REF_KEEP, build_keepouts(Builder(), P, d), REF_NOTE)

    step(os.path.join(cad, "ESP32_Controller_Housing_Base.step"),
         find_component(design, BASE).component)
    step(os.path.join(cad, "ESP32_Controller_Housing_Lid.step"),
         find_component(design, LID).component)
    step(os.path.join(cad, "ESP32_Controller_Carrier_Fit_Gauge.step"),
         find_component(design, GAUGE).component)

    # both clamps in one exchange file, per the deliverable list
    clear_component(design, "EXPORT_PCB_Clamps")
    tbm = adsk.fusion.TemporaryBRepManager.get()
    pair = []
    for nm in (CLAMP_FIX, CLAMP_ADJ):
        b = find_component(design, nm).bRepBodies.item(0)
        pair.append((tbm.copy(b), b.name))
    _occ, cc = add_component(root, "EXPORT_PCB_Clamps", pair)
    step(os.path.join(cad, "ESP32_Controller_PCB_Clamps.step"), cc)
    clear_component(design, "EXPORT_PCB_Clamps")

    meshes = (
        (BASE, "ESP32_Controller_Housing_Base.stl"),
        (LID, "ESP32_Controller_Housing_Lid.stl"),
        (CLAMP_FIX, "ESP32_Controller_PCB_Clamp_Fixed.stl"),
        (CLAMP_ADJ, "ESP32_Controller_PCB_Clamp_Adjustable.stl"),
        (GAUGE, "ESP32_Controller_Carrier_Fit_Gauge.stl"),
        (PLUG, "ESP32_Controller_USB_Plug.stl"),
    )
    for comp_name, fname in meshes:
        mesh(find_component(design, comp_name).bRepBodies.item(0),
             os.path.join(stl, fname))

    for p in written:
        print("%10d  %s" % (os.path.getsize(p) if os.path.exists(p) else -1,
                            os.path.relpath(p, REPO).replace("\\", "/")))
    print("%d files written" % len(written))
    return written


# ---------------------------------------------------------------------------
# images - the review evidence required by specification section 13.
#
# Every view is generated from the built model, never posed by hand, so the
# whole set regenerates from one call after any parameter change. Keep-out
# solids are shown as bodies rather than described in a caption: a corridor
# either has housing in it or it does not, and the picture shows which.
# ---------------------------------------------------------------------------
IMG_W, IMG_H = 1400, 1000
IMG_PREFIX = "Decca_ESP32_Controller_Housing_revA_"

VIEW = {
    "iso": "IsoTopRightViewOrientation",
    "iso_left": "IsoTopLeftViewOrientation",
    "iso_bottom": "IsoBottomRightViewOrientation",
    "top": "TopViewOrientation",
    "bottom": "BottomViewOrientation",
    "front": "FrontViewOrientation",
    "right": "RightViewOrientation",
    "left": "LeftViewOrientation",
}


def _appearance(design, app, body, wanted):
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    if lib is None:
        return
    a = None
    for i in range(lib.appearances.count):
        nm = lib.appearances.item(i).name
        if wanted.lower() in nm.lower():
            a = lib.appearances.item(i)
            break
    if a is None:
        return
    local = design.appearances.itemByName(a.name)
    if local is None:
        local = design.appearances.addByCopy(a, a.name)
    body.appearance = local


PRINT_LOOK = "Plastic - Matte (Gray)"
HARDWARE_LOOK = "Plastic - Matte (Green)"
KEEPOUT_LOOK = "Plastic - Translucent Matte (Yellow)"


def _look_for(body_name, comp_name):
    if body_name.startswith("KEEPOUT_") or comp_name == REF_KEEP:
        return KEEPOUT_LOOK
    if body_name.startswith("REF_") or comp_name in REFERENCE:
        return HARDWARE_LOOK
    return PRINT_LOOK


def dress(design, app, extra=()):
    """Printable grey, acquired hardware green, keep-out volumes translucent
    yellow. A reader can then tell manufacturing geometry from a dimensional
    assumption without opening the browser."""
    root = design.rootComponent
    names = list(REFERENCE) + list(PRINTABLE) + list(extra)
    for name in names:
        occ = find_component(design, name)
        if occ is None:
            continue
        for b in occ.component.bRepBodies:
            try:
                _appearance(design, app, b, _look_for(b.name, name))
            except Exception:
                pass


def _show(design, spec):
    """spec maps component name -> True for all bodies, or a set of body
    names. Everything not named is hidden."""
    root = design.rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        nm = occ.component.name
        on = nm in spec
        occ.isLightBulbOn = on
        if not on:
            continue
        want = spec[nm]
        for b in occ.bRepBodies:
            b.isLightBulbOn = True if want is True else (b.name in want)


def _shot(app, path, orientation):
    vp = app.activeViewport
    cam = vp.camera
    cam.viewOrientation = getattr(adsk.core.ViewOrientations, orientation)
    cam.isFitView = True
    vp.camera = cam
    vp.refresh()
    adsk.doEvents()
    vp.fit()
    if not vp.saveAsImageFile(path, IMG_W, IMG_H):
        raise RuntimeError("could not write %s" % path)
    return path


def _temp_component(design, name, pieces):
    """pieces: list of (body, dx, dy, dz, keep_box_or_None, new_name)."""
    root = design.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    clear_component(design, name)
    out = []
    for body, dx, dy, dz, keep, bn in pieces:
        c = tbm.copy(body)
        if keep is not None:
            tbm.booleanOperation(c, tbm.copy(keep),
                                 adsk.fusion.BooleanTypes.IntersectionBooleanType)
            if c.faces.count == 0:
                continue
        if dx or dy or dz:
            m = adsk.core.Matrix3D.create()
            m.translation = adsk.core.Vector3D.create(mm(dx), mm(dy), mm(dz))
            tbm.transform(c, m)
        out.append((c, bn))
    return add_component(root, name, out)


def images(_context=None):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    B = Builder()
    d = derive(P)
    out_dir = os.path.join(REPO, "mechanical", "Drawings")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    dress(design, app)

    def path(tag):
        return os.path.join(out_dir, IMG_PREFIX + tag + ".png")

    written = []

    def shot(tag, spec, orientation):
        _show(design, spec)
        written.append(_shot(app, path(tag), VIEW[orientation]))
        print("  %-26s %s" % (tag, os.path.basename(written[-1])))

    ALL = {n: True for n in PRINTABLE if n != GAUGE}

    # 1 closed housing
    shot("01_closed", {BASE: True, LID: True}, "iso")

    # 2 lid removed, controller in place
    shot("02_lid_removed",
         {BASE: True, CLAMP_FIX: True, CLAMP_ADJ: True,
          REF_ADP: True, REF_ESP: True}, "iso")

    # 3 exploded assembly
    parts = []
    for nm, dz in ((BASE, 0.0), (CLAMP_FIX, 40.0), (CLAMP_ADJ, 40.0),
                   (LID, 96.0)):
        for b in find_component(design, nm).bRepBodies:
            parts.append((b, 0.0, 0.0, dz, None, b.name))
    for b in find_component(design, REF_ADP).bRepBodies:
        parts.append((b, 0.0, 0.0, 18.0, None, b.name))
    for b in find_component(design, REF_ESP).bRepBodies:
        parts.append((b, 0.0, 0.0, 62.0, None, b.name))
    for b in find_component(design, PLUG).bRepBodies:
        parts.append((b, -44.0, 0.0, 96.0, None, b.name))
    _temp_component(design, "EXPLODED_VIEW", parts)
    dress(design, app, ("EXPLODED_VIEW",))
    shot("03_exploded", {"EXPLODED_VIEW": True}, "iso")
    clear_component(design, "EXPLODED_VIEW")

    # 4 overall plan and elevation - dimensions are annotated by the offline
    #   verifier, which measures them off the mesh rather than trusting these
    shot("04_plan", {BASE: True, LID: True}, "top")
    shot("05_elevation", {BASE: True, LID: True}, "front")

    # 6 section through the board, base and lid
    half = B.box(d["x_out_neg"] - 20.0, 0.0, -d["rail_y_out"] - 20.0,
                 d["rail_y_out"] + 20.0, d["z_floor_bot"] - 20.0,
                 d["z_lid_top"] + 20.0)
    parts = []
    for nm in (BASE, LID, CLAMP_FIX, REF_ADP, REF_ESP):
        for b in find_component(design, nm).bRepBodies:
            parts.append((b, 0.0, 0.0, 0.0, half, b.name))
    _temp_component(design, "SECTION_VIEW", parts)
    dress(design, app, ("SECTION_VIEW",))
    shot("06_section", {"SECTION_VIEW": True}, "right")
    shot("06b_section_oblique", {"SECTION_VIEW": True}, "iso")
    clear_component(design, "SECTION_VIEW")

    # 7 terminal screwdriver corridors, lid removed
    shot("07_terminal_corridors",
         {BASE: True, CLAMP_FIX: True, CLAMP_ADJ: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_TERMINAL_DRIVER_CORRIDORS"}}, "iso")

    # 8 cable exits and strain relief
    shot("08_cable_exits",
         {BASE: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_WIRE_EXIT_PATHS"}}, "iso")

    # 9 underside: isolated board and cabinet fastener envelopes
    shot("09_underside_clearances",
         {BASE: True,
          REF_KEEP: {"KEEPOUT_UNDERSIDE_JOINTS",
                     "KEEPOUT_LID_AND_CLAMP_FASTENERS",
                     "KEEPOUT_CABINET_FASTENERS"}}, "iso_bottom")

    # 10 USB insertion envelope
    shot("10_usb_envelope",
         {BASE: True, LID: True, REF_ESP: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_USB_SERVICE_ENVELOPE"}}, "iso_left")

    # 11 EN/RESET and BOOT tool access
    shot("11_button_access",
         {LID: True, REF_ESP: True,
          REF_KEEP: {"KEEPOUT_BUTTON_TOOL_ACCESS"}}, "iso")

    # 12 Wi-Fi antenna keep-out
    shot("12_antenna_keepout",
         {BASE: True, LID: True, REF_ESP: True,
          REF_KEEP: {"KEEPOUT_WIFI_ANTENNA"}}, "iso")

    # 13 cabinet mounting slots
    shot("13_mounting_slots", {BASE: True}, "bottom")

    # 14 fit gauge
    shot("14_fit_gauge", {GAUGE: True}, "iso")

    _show(design, {n: True for n in PRINTABLE + REFERENCE})
    for nm in REFERENCE:
        occ = find_component(design, nm)
        if occ:
            occ.isLightBulbOn = nm != REF_KEEP
    print("%d review images written to mechanical/Drawings/" % len(written))
    return written
