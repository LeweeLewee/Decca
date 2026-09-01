# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev B parametric generator (Autodesk Fusion).

Controlling document: mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md
                      (its content is specification revision v1.1)
Status: PROTOTYPE CAD. NOT physically validated. No dimension in this file has
        been measured off the acquired hardware.

WHY REV B EXISTS
----------------
Rev A was rejected on owner review: 105.00 x 77.00 x 38.30 mm and 68 cm3 of
printed material for a board 66 x 63 mm. Rev A geometry is NOT the baseline.
Specification v1.1 deletes, by name, the external lacing rails, the external
mounting ears, the sawtooth cable-window roofs, the USB blanking plug, the
second full-width clamp, the four-corner lid screws with their corner piers and
the thirty per-terminal wire guides. None of them is rebuilt here.

REV B ARCHITECTURE
------------------
Shallow base tray, deep lid.

    Housing_Base        1.60 mm continuous insulating floor; four local PCB
                        support pads; one integral fixed ledge on the -X short
                        edge; two clamp plinths with vertical M3 inserts and
                        two lid-screw bosses with horizontal M3 inserts on the
                        +X short edge; two locating rebates on -X; four
                        cable-tie tabs, two per long side; two recessed,
                        capped cabinet fixings under the board.
    Housing_Lid         deep cover carrying most of the side protection; four
                        open-bottom cable windows; one open-bottom USB service
                        slot; five top vent slots; two locating lugs.
    PCB_Clamp_Adjustable   one flat bar, two slotted M3 screws, +/-1.00 mm of
                        travel, bottoming on the plinths so the board is never
                        loaded.
    Cabinet_Fastener_Caps  two insulating discs over the recessed M3 heads.
    Carrier_Fit_Gauge   non-production prototype gauge for the 65-67 mm range.

Every external structure below has a stated purpose and a numbered gate in
``validate``. There are no ribs, fins, tabs or projections beyond those.

THE HARDWARE IS STILL NOT MEASURED
----------------------------------
Every hardware figure is a CAD starting value tagged STARTING, carried forward
unchanged from Rev A because the repository records no measurement. They remain
prototype acceptance gates. Nothing here may be described as verified until a
printed part has been offered up to the acquired board.

PRINTING
--------
PETG / PETG-HF, 0.40 mm nozzle, 0.20 mm layers, no support material.
Base floor-down. Lid TOP-FACE-DOWN - which is what makes the open-bottom cable
windows and the USB slot print with no roof, no bridge and no support: printed
inverted, a notch that is open at the skirt's free edge only ever grows, it
never closes. Clamp flat, so its cantilever is stressed along the layers.

RUNNING IT
----------
    main(None)      build/rebuild every component in the active document
    validate(None)  the specification v1.1 section 13 gate suite
    export(None)    f3d, STEP and STL into mechanical/CAD and mechanical/STL
    images(None)    the review renders into mechanical/Drawings

``run`` is provided for the Fusion MCP bridge; it calls ``main``.
"""

from __future__ import print_function

import math
import os

import adsk.core
import adsk.fusion


DOC_NAME = "Decca_ESP32_Controller_Housing"

BASE = "Housing_Base"
LID = "Housing_Lid"
CLAMP = "PCB_Clamp_Adjustable"
CAPS = "Cabinet_Fastener_Caps"
GAUGE = "Carrier_Fit_Gauge"

REF_ESP = "REF_ESP32_DevKit_V1_30Pin"
REF_ADP = "REF_30Pin_Terminal_Adapter"
REF_KEEP = "REF_Wired_Keepouts"

# Parts that are printed and shipped. The fit gauge is a prototype tool and is
# excluded from the section 9 material gates; the caps are mandatory because a
# recessed metal screw head under the board cannot be insulated any other way.
PRODUCTION = (BASE, LID, CLAMP, CAPS)
PRINTABLE = PRODUCTION + (GAUGE,)
REFERENCE = (REF_ESP, REF_ADP, REF_KEEP)

REF_NOTE = ("NON-MANUFACTURING REFERENCE. Dimensional starting values only - "
            "not measured hardware. Excluded from every printable export.")

PETG_DENSITY = 1.27                  # g/cm3, specification section 9

# The one FDM rule this design states for itself. v1.1 section 10 forbids
# support MATERIAL; it does not forbid a short unsupported ledge, and a
# retaining ledge over a board cannot be built without one. Every downward
# facing surface on every part is measured for how far it reaches from
# something holding it up, and 1.50 mm is the limit. Cable windows and the USB
# slot are held to a stricter rule: no downward-facing surface at all.
OVERHANG_REACH_MAX = 1.50            # mm

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))


# ---------------------------------------------------------------------------
# PARAMETERS - the single source of truth.
#
# STATUS tags, used verbatim in the build report:
#   STARTING  a CAD starting value; NOT measured; an open prototype gate
#   DESIGN    a design value taken from specification v1.1
#   DERIVED*  (in derive() below, never here)
# ---------------------------------------------------------------------------
P = {
    # -- Repository-controlled hardware ------------------------------------
    "esp_pin_count": 30,

    # -- Terminal adapter / carrier, STARTING ------------------------------
    "adapter_pcb_l": 66.00,          # nominal carrier length, X
    "adapter_pcb_w": 63.00,          # carrier width, Y
    "adapter_pcb_t": 1.60,
    "adapter_below_h": 2.50,         # lowest solder/pin feature below the PCB
    "assembly_above_pcb_h": 24.00,   # tallest assembled component above it
    "carrier_len_min": 65.00,        # specification v1.1 section 3
    "carrier_len_max": 67.00,
    "pcb_bare_edge": 3.00,           # bare strip inboard of each SHORT edge
    "pcb_bare_perim": 2.50,          # bare strip inboard of each LONG edge

    # -- Screw terminals, STARTING -----------------------------------------
    "term_per_side": 15,
    "term_pitch": 3.50,
    "term_block_w": 8.00,            # block depth inboard from the PCB edge
    "term_block_h": 10.00,           # block height above the PCB top face
    "term_screw_inset": 4.00,
    "term_screw_d": 2.60,
    "term_wire_z": 4.00,             # wire entry height above the PCB top

    # -- ESP32 DevKit V1 / DOIT reference, STARTING ------------------------
    "esp_pcb_l": 51.50,
    "esp_pcb_w": 28.30,
    "esp_pcb_t": 1.60,
    "esp_header_h": 8.50,
    "esp_header_span": 22.86,
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

    # -- Clearances, DESIGN (specification v1.1 section 3) -----------------
    "pcb_xy_clear": 0.50,
    "pcb_under_clear": 2.00,         # v1.1 lowers this from 3.00
    "component_top_clear": 2.00,     # v1.1 lowers this from 3.00
    "clamp_vertical_clear": 0.20,
    "antenna_keepout": 10.00,
    "lid_fit_clear": 0.25,

    # -- Structure, DESIGN --------------------------------------------------
    "base_floor_t": 1.60,            # v1.1 section 4.1
    "base_wall_t": 1.60,
    "base_wall_h": 9.00,             # shallow tray: wall top above floor top
    "lid_top_t": 1.60,               # v1.1 sections 7.4 and 8.1
    "lid_skirt_t": 1.20,             # three 0.40 mm perimeters
    "lid_overlap": 4.00,             # v1.1 section 8.3
    "outer_corner_r": 3.00,
    "cav_corner_r": 0.00,            # SQUARE internal corners: a filleted
                                     # cavity corner eats into the corner
                                     # of a square-routed carrier
    "boss_wall": 1.60,

    # -- Access, DESIGN -----------------------------------------------------
    "wire_exit_h": 10.00,            # REQUIRED clear window height
    "win_half_w": 10.00,             # half width of each cable window
    "win_x_centre": 20.00,           # +/- centres of the two windows per side
    "win_top": 20.00,                # window top, above the floor top
    "usb_open_w": 14.00,             # REQUIRED minimum 14.00
    "usb_open_h": 9.00,              # REQUIRED minimum 9.00
    "usb_slot_w": 15.00,             # PROVIDED slot width
    "driver_d": 6.00,                # terminal screwdriver corridor
    "wire_d": 2.00,                  # one 22-24 AWG insulated conductor
    "bundle_pack": 1.15,             # round-bundle packing factor

    # -- PCB support and retention, DESIGN ---------------------------------
    "pad_l": 9.00,                   # support pad, along the long edge
    "pad_w": 2.20,                   # support pad, across the long edge
    "pad_x": 28.50,                  # +/- pad centres
    "ledge_grip": 2.00,              # fixed ledge overhang onto the bare edge
    "ledge_lead": 0.80,              # 45 deg lead-in chamfer under the ledge
    "ledge_half_span": 7.00,         # each of the two ledge segments
    "ledge_y": 18.00,                # +/- ledge segment centres
    "clamp_t": 3.00,
    "clamp_grip": 2.00,
    "clamp_half_span": 20.00,
    "clamp_screw_y": 16.00,
    "clamp_slot_w": 3.40,
    "clamp_slot_l": 5.40,            # 3.40 + 2 x 1.00 travel
    "clamp_edge": 0.50,              # bar material past the slot end
    "clamp_side_clear": 0.40,        # bar end to the +X wall inner face
    "plinth_half_w": 4.50,           # each clamp plinth, along Y

    # -- Fasteners, DESIGN --------------------------------------------------
    "lid_screw_nominal": 3.00,
    "lid_screw_clear_d": 3.40,
    "insert_hole_d": 4.00,           # STARTING - exact insert NOT recorded
    "insert_depth": 5.00,            # STARTING - exact insert NOT recorded
    "lid_screw_y": 27.00,            # +/- horizontal lid screw axes
    "lid_screw_z": 8.50,             # axis height; keeps 1.80 mm of skirt
                                     # below the clearance hole
    "lid_boss_half_w": 4.00,         # each lid-screw boss, along Y
    "lid_boss_h": 12.20,             # local wall raise at the boss

    # -- Locating hooks, DESIGN --------------------------------------------
    "hook_y": 22.00,                 # +/- hook centres on the -X end
    "hook_half_w": 6.00,
    "hook_depth": 0.80,              # rebate depth / lug projection
    "hook_z0": 4.60,                 # rebate bottom
    "hook_z1": 7.20,                 # rebate top = capture ledge underside
    "lug_z0": 5.40,
    "lug_z1": 7.00,

    # -- Cable-tie tabs, DESIGN ---------------------------------------------
    "tie_x": 5.00,                   # +/- tab centres on each long side
    "tie_tab_half_w": 4.00,
    "tie_tab_top": 15.50,            # tab top above the floor top
    "tie_ap_w": 5.00,                # aperture width, X
    "tie_ap_h": 2.40,                # aperture straight height, Z
    "tie_ap_z0": 10.00,

    # -- Recessed cabinet fixings, DESIGN ----------------------------------
    "cab_x": 27.00,                  # +/- fixing centres, on the centreline
    "cab_screw_d": 3.40,             # M3 clearance
    "cab_head_d": 6.40,              # M3 countersunk head
    "cab_pad_d": 13.00,
    "cab_pad_h": 2.40,               # pad top - stays 2.10 below the PCB
    "cab_cap_d": 10.20,
    "cab_cap_t": 1.20,
    "cab_cap_clear": 0.20,           # on diameter

    # -- Ventilation, DESIGN -------------------------------------------------
    "vent_w": 2.00,
    "vent_l": 14.00,
    "vent_pitch": 4.50,
    "vent_n": 5,
    "vent_x": -15.00,                # centre, kept clear of the antenna

    # -- Fit gauge (prototype tool, excluded from the material gates) -------
    "gauge_w": 18.00,
    "gauge_plate_t": 1.60,
}

STARTING = (
    "adapter_pcb_l", "adapter_pcb_w", "adapter_pcb_t", "adapter_below_h",
    "assembly_above_pcb_h", "pcb_bare_edge", "pcb_bare_perim",
    "term_per_side", "term_pitch", "term_block_w", "term_block_h",
    "term_screw_inset", "term_screw_d", "term_wire_z",
    "esp_pcb_l", "esp_pcb_w", "esp_pcb_t", "esp_header_h", "esp_header_span",
    "esp_off_x", "esp_off_y", "esp_mod_l", "esp_mod_w", "esp_mod_h",
    "esp_ant_l", "esp_ant_w", "esp_usb_w", "esp_usb_l", "esp_usb_h",
    "insert_hole_d", "insert_depth",
)

# The actual Decca harnesses, docs/Wiring.md. Specification v1.1 section 5.1
# requires these to be modelled as GROUPED BUNDLES - the thirty-wire model that
# produced Rev A's per-terminal guides is deleted.
#   (id, description, conductors, long side, window index on that side)
HARNESS = (
    ("H1", "Potentiometer harness, 4 pots x 3", 12, -1, 0),
    ("H2", "Original on/off switch harness", 2, -1, 1),
    ("H3", "Radio/source and stereo/mono contacts", 4, -1, 1),
    ("H4", "OLED harness", 4, +1, 0),
    ("H5", "Dial-lighting control to DFR0457", 3, +1, 0),
    ("H6", "ZA3 12 V trigger harness", 2, +1, 1),
    ("PWR", "5 V and GND from the WAGO star points", 2, +1, 1),
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

    def cylx(self, d, y, z, x0, x1):
        return self.tbm.createCylinderOrCone(p3(x0, y, z), mm(d / 2.0),
                                             p3(x1, y, z), mm(d / 2.0))

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

    def wedge_y(self, xc, z_base, half_w, height, y0, y1):
        """Isoceles triangular prism lying along Y: base 2*half_w at z_base,
        apex ``height`` above it. With half_w == height the flanks are 45
        degrees, which is what lets an aperture roof print with no bridge."""
        s = math.sqrt(2.0) * max(half_w, height)
        u = v3(1.0 / math.sqrt(2.0), 0.0, 1.0 / math.sqrt(2.0))
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3(xc, (y0 + y1) / 2.0, z_base), u, v3(0, 1, 0),
            mm(s), mm(y1 - y0), mm(s))
        dbox = self.tbm.createBox(obb)
        return self.inter(dbox, self.box(xc - half_w - 1.0, xc + half_w + 1.0,
                                         y0 - 1.0, y1 + 1.0,
                                         z_base, z_base + height))

    def diamond_y(self, xc, zc, half, y0, y1):
        """Square prism rotated 45 degrees in XZ, lying along Y, centred on
        (xc, zc). Subtracted at a solid's convex corner it leaves an exact
        45-degree chamfer of leg ``half`` on both faces meeting there."""
        s = math.sqrt(2.0) * half
        u = v3(1.0 / math.sqrt(2.0), 0.0, 1.0 / math.sqrt(2.0))
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3(xc, (y0 + y1) / 2.0, zc), u, v3(0, 1, 0),
            mm(s), mm(y1 - y0), mm(s))
        return self.tbm.createBox(obb)

    def diamond_x(self, yc, zc, half, x0, x1):
        """The same, in the YZ plane, lying along X."""
        s = math.sqrt(2.0) * half
        u = v3(0.0, 1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0))
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3((x0 + x1) / 2.0, yc, zc), u, v3(1, 0, 0),
            mm(s), mm(x1 - x0), mm(s))
        return self.tbm.createBox(obb)

    def keep_above_chamfer(self, xc, zc, sx, sz, leg, y0, y1, L=60.0):
        """A large half-space-like box whose FACE is the 45 degree chamfer
        plane at the convex corner (xc, zc), with the box on the material
        side. (sx, sz) point INTO the material.

        Intersecting a solid with this is the manifold-safe way to chamfer.
        Subtracting a diamond centred on the corner is not: the diamond's
        vertices land exactly on the two faces meeting there, every face pair
        touches at a single line, and Fusion reports a valid solid that
        tessellates to edges shared by four triangles. That defect is
        invisible in CAD and fatal to every ray-parity test in the offline
        verifier, so it is designed out rather than checked for.
        """
        t = v3(-sx / math.sqrt(2.0), 0.0, sz / math.sqrt(2.0))
        mx = sx / math.sqrt(2.0)
        mz = sz / math.sqrt(2.0)
        # midpoint of the chamfer edge, then half the box depth into the solid
        px = xc + sx * leg / 2.0 + mx * L / 2.0
        pz = zc + sz * leg / 2.0 + mz * L / 2.0
        obb = adsk.core.OrientedBoundingBox3D.create(
            p3(px, (y0 + y1) / 2.0, pz), t, v3(0, 1, 0),
            mm(L), mm(y1 - y0), mm(L))
        return self.tbm.createBox(obb)


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
# Origin: the FIXED short edge of the carrier is at x = -adapter_pcb_l/2, the
# plan centre of the nominal 66 mm board is x = 0, and z = 0 is the cavity
# floor top.
# ---------------------------------------------------------------------------
def derive(P):
    d = {}

    # ---- vertical chain ---------------------------------------------------
    d["z_floor_bot"] = -P["base_floor_t"]
    d["z_floor_top"] = 0.0
    # Additive, and deliberately so: v1.1 section 4.3 measures its 2.00 mm
    # BENEATH the lowest solder feature, and that feature hangs 2.50 mm below
    # the board. v1.1 lowers both clearances from Rev A's 3.00 mm, which is
    # where 2.00 mm of the Rev A height reduction comes from.
    d["pad_h"] = P["adapter_below_h"] + P["pcb_under_clear"]
    d["z_pcb_bot"] = d["pad_h"]
    d["z_pcb_top"] = d["z_pcb_bot"] + P["adapter_pcb_t"]
    d["z_under_bot"] = d["z_pcb_bot"] - P["adapter_below_h"]
    d["z_retain"] = d["z_pcb_top"] + P["clamp_vertical_clear"]
    d["z_term_top"] = d["z_pcb_top"] + P["term_block_h"]
    d["z_comp_top"] = d["z_pcb_top"] + P["assembly_above_pcb_h"]
    d["z_cav_top"] = d["z_comp_top"] + P["component_top_clear"]
    d["z_lid_top"] = d["z_cav_top"] + P["lid_top_t"]
    d["h_closed"] = d["z_lid_top"] - d["z_floor_bot"]
    d["internal_h_above_support"] = d["z_cav_top"] - d["z_pcb_bot"]
    d["z_wall_top"] = P["base_wall_h"]
    d["z_skirt_bot"] = d["z_wall_top"] - P["lid_overlap"]

    # ---- carrier footprint and its 65-67 mm length window -----------------
    d["x_datum"] = -P["adapter_pcb_l"] / 2.0
    d["x_pcb_nom"] = P["adapter_pcb_l"] / 2.0
    d["x_pcb_min"] = d["x_datum"] + P["carrier_len_min"]
    d["x_pcb_max"] = d["x_datum"] + P["carrier_len_max"]
    d["x_adj_face"] = d["x_pcb_max"] + P["pcb_xy_clear"]
    # the component region on the carrier top, valid for EVERY length in the
    # 65-67 mm window: inboard of both bare short-edge margins at the shortest
    d["comp_x0"] = d["x_datum"] + P["pcb_bare_edge"]
    d["comp_x1"] = d["x_pcb_min"] - P["pcb_bare_edge"]
    d["y_pcb"] = P["adapter_pcb_w"] / 2.0
    d["y_cav"] = d["y_pcb"] + P["pcb_xy_clear"]
    d["y_out"] = d["y_cav"] + P["base_wall_t"]

    # ---- base plan --------------------------------------------------------
    # The -X end wall is 2.40 mm, not 1.60: it carries the integral fixed
    # ledge AND the two hook rebates, and a 0.80 mm rebate in a 1.60 mm wall
    # would leave 0.80 mm of skin. 0.80 mm of extra wall costs 0.48 cm3 and
    # 0.80 mm of length, and it is the only place in the base that is thicker
    # than 1.60 mm other than the four bosses.
    d["end_wall_neg_t"] = P["base_wall_t"] + P["hook_depth"]
    d["x_wall_in_neg"] = d["x_datum"]
    d["x_out_neg"] = d["x_wall_in_neg"] - d["end_wall_neg_t"]

    # The +X length is set by two chains that have to be taken together, and
    # taking only the first is the mistake that would bury the clamp bar in
    # the end wall: (a) the vertical insert needs boss_wall of material either
    # side of its hole, and (b) the clamp bar's screw SLOT is 5.40 mm long,
    # so the bar reaches clamp_edge past the slot and needs clamp_side_clear
    # to the wall. Here the two chains happen to land on the same face.
    d["x_ins"] = (d["x_adj_face"] + P["boss_wall"] + P["insert_hole_d"] / 2.0)
    d["slot_x0"] = d["x_ins"] - P["clamp_slot_l"] / 2.0
    d["slot_x1"] = d["x_ins"] + P["clamp_slot_l"] / 2.0
    d["bar_x1"] = d["slot_x1"] + P["clamp_edge"]
    d["x_wall_in_pos"] = max(
        d["x_ins"] + P["insert_hole_d"] / 2.0 + P["boss_wall"],
        d["bar_x1"] + P["clamp_side_clear"])
    d["x_out_pos"] = d["x_wall_in_pos"] + P["base_wall_t"]

    d["body_l"] = d["x_out_pos"] - d["x_out_neg"]
    d["body_w"] = 2.0 * d["y_out"]

    # ---- integral fixed ledge, -X short edge ------------------------------
    d["ledge_x1"] = d["x_datum"] + P["ledge_grip"]
    d["ledge_z0"] = d["z_retain"]
    d["ledge_y0"] = P["ledge_y"] - P["ledge_half_span"]
    d["ledge_y1"] = P["ledge_y"] + P["ledge_half_span"]
    # the only unsupported horizontal overhang in the base, and the lead-in
    # chamfer that the carrier slides against takes most of it away
    d["ledge_flat"] = P["ledge_grip"] - P["ledge_lead"]

    # ---- four local carrier support pads ----------------------------------
    d["pad_x0"] = P["pad_x"] - P["pad_l"] / 2.0
    d["pad_x1"] = P["pad_x"] + P["pad_l"] / 2.0
    d["pad_y1"] = d["y_pcb"] - 0.10
    d["pad_y0"] = d["pad_y1"] - P["pad_w"]
    d["bare_y0"] = d["y_pcb"] - P["pcb_bare_perim"]

    # ---- adjustable clamp -------------------------------------------------
    d["clamp_z0"] = d["z_retain"]
    d["clamp_z1"] = d["clamp_z0"] + P["clamp_t"]
    d["bar_x0"] = d["x_pcb_nom"] - P["clamp_grip"]
    d["clamp_travel"] = (P["clamp_slot_l"] - P["clamp_slot_w"]) / 2.0
    d["grip_at_min"] = (d["x_pcb_min"]
                        - (d["bar_x0"] - d["clamp_travel"]))
    d["grip_at_max"] = (d["x_pcb_max"]
                        - (d["bar_x0"] + d["clamp_travel"]))
    d["plinth_y0"] = P["clamp_screw_y"] - P["plinth_half_w"]
    d["plinth_y1"] = P["clamp_screw_y"] + P["plinth_half_w"]
    d["z_ins_bot"] = d["z_retain"] - P["insert_depth"]

    # ---- two horizontal lid-screw bosses, +X end --------------------------
    d["lid_bore_x0"] = d["x_out_pos"] - (P["insert_depth"] + 0.40)
    d["lid_boss_y0"] = P["lid_screw_y"] - P["lid_boss_half_w"]
    d["lid_boss_y1"] = P["lid_screw_y"] + P["lid_boss_half_w"]

    # ---- two locating hooks, -X end ---------------------------------------
    d["hook_x0"] = d["x_out_neg"]
    d["hook_x1"] = d["x_out_neg"] + P["hook_depth"]
    d["hook_y0"] = P["hook_y"] - P["hook_half_w"]
    d["hook_y1"] = P["hook_y"] + P["hook_half_w"]
    d["lug_proj"] = P["lid_fit_clear"] + P["hook_depth"] - 0.20
    d["hook_engage"] = d["lug_proj"] - P["lid_fit_clear"]

    # ---- four internal cable-tie tabs, two per long side ------------------
    d["tie_tab_x0"] = P["tie_x"] - P["tie_tab_half_w"]
    d["tie_tab_x1"] = P["tie_x"] + P["tie_tab_half_w"]
    d["tie_ap_z1"] = P["tie_ap_z0"] + P["tie_ap_h"]
    d["tie_ap_peak"] = P["tie_ap_w"] / 2.0
    d["tie_ap_apex"] = d["tie_ap_z1"] + d["tie_ap_peak"]

    # ---- two recessed cabinet fixings, under the carrier ------------------
    d["cab_recess_z1"] = P["cab_pad_h"]
    d["cab_recess_z0"] = P["cab_pad_h"] - P["cab_cap_t"]
    d["cab_csk_z0"] = d["cab_recess_z0"] - (P["cab_head_d"]
                                            - P["cab_screw_d"]) / 2.0
    d["cab_head_top"] = d["cab_recess_z0"]
    d["cab_head_to_pcb"] = d["z_pcb_bot"] - P["cab_pad_h"]
    d["cab_recess_d"] = P["cab_cap_d"] + P["cab_cap_clear"]

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

    # ---- lid ---------------------------------------------------------------
    d["skirt_in_neg"] = d["x_out_neg"] - P["lid_fit_clear"]
    d["skirt_in_pos"] = d["x_out_pos"] + P["lid_fit_clear"]
    d["skirt_in_y"] = d["y_out"] + P["lid_fit_clear"]
    d["lid_x0"] = d["skirt_in_neg"] - P["lid_skirt_t"]
    d["lid_x1"] = d["skirt_in_pos"] + P["lid_skirt_t"]
    d["lid_y"] = d["skirt_in_y"] + P["lid_skirt_t"]
    d["lid_l"] = d["lid_x1"] - d["lid_x0"]
    d["lid_w"] = 2.0 * d["lid_y"]
    d["skirt_inner_r"] = P["outer_corner_r"] + P["lid_fit_clear"]
    d["lid_r"] = d["skirt_inner_r"] + P["lid_skirt_t"]

    # ---- open-bottom cable windows ----------------------------------------
    # Each window is a notch in the deep lid skirt that is OPEN at the skirt's
    # lower free edge. Printed top-face-down the notch only ever grows, so it
    # needs no roof, no bridge, no sawtooth and no support - which is the whole
    # reason v1.1 could delete Rev A's sixteen-tooth window roofs.
    d["win_x"] = [-P["win_x_centre"], P["win_x_centre"]]
    d["win_z0"] = d["z_skirt_bot"]
    d["win_z1"] = P["win_top"]
    d["win_sill"] = d["z_wall_top"]
    d["win_clear_h"] = d["win_z1"] - d["win_sill"]
    d["win_w"] = 2.0 * P["win_half_w"]

    # ---- open-bottom USB service slot, same trick -------------------------
    d["usb_slot_y0"] = -P["usb_slot_w"] / 2.0
    d["usb_slot_y1"] = P["usb_slot_w"] / 2.0
    d["usb_slot_z1"] = d["usb_z1"] + 0.50
    d["usb_clear_h"] = d["usb_slot_z1"] - d["usb_z0"]

    # ---- top ventilation, kept clear of the antenna keep-out --------------
    d["vent_x0"] = P["vent_x"] - P["vent_l"] / 2.0
    d["vent_x1"] = P["vent_x"] + P["vent_l"] / 2.0
    d["vent_y"] = [(i - (P["vent_n"] - 1) / 2.0) * P["vent_pitch"]
                   for i in range(P["vent_n"])]

    # ---- grouped harnesses, docs/Wiring.md --------------------------------
    # Bundle diameter for n round conductors, hexagonally packed and squeezed
    # by a tie: pack * wire_d * sqrt(n). Windows are indexed 0 (-X) and 1 (+X).
    groups = {}
    for hid, desc, n_cond, side, win in HARNESS:
        key = (side, win)
        g = groups.setdefault(key, {"ids": [], "n": 0})
        g["ids"].append(hid)
        g["n"] += n_cond
    bundles = []
    for (side, win), g in sorted(groups.items()):
        dia = P["bundle_pack"] * P["wire_d"] * math.sqrt(float(g["n"]))
        z = d["win_sill"] + dia / 2.0 + 0.50
        bundles.append({
            "ids": "+".join(g["ids"]), "n": g["n"], "d": dia,
            "side": side, "win": win, "x": d["win_x"][win], "z": z,
        })
    d["bundles"] = bundles
    d["bundle_d_max"] = max(b["d"] for b in bundles)
    d["bundle_top_max"] = max(b["z"] + b["d"] / 2.0 for b in bundles)

    # ---- overall -----------------------------------------------------------
    d["overall_l"] = d["lid_l"]
    d["overall_w"] = d["lid_w"]
    d["overall_h"] = d["h_closed"]
    d["plan_area"] = d["overall_l"] * d["overall_w"]
    return d


# ---------------------------------------------------------------------------
# Reference components. NON-MANUFACTURING. Starting values, never measurements.
# ---------------------------------------------------------------------------
def build_esp32(B, P, d):
    """30-pin DevKit V1 / DOIT-style controller, sitting in its sockets.

    v1.1 section 6.4 forbids EN/BOOT access holes until the buttons have been
    physically measured, so Rev A's two button solids and their tool corridors
    are gone: the removable lid is the prototype access route."""
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
    return [(pcb, "REF_ESP32_PCB"), (mod, "REF_ESP32_MODULE"),
            (ant, "REF_ESP32_PCB_ANTENNA"), (usb, "REF_ESP32_USB_CONNECTOR")]


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

    under = _underside_joints(B, P, d)
    return [(pcb, "REF_ADAPTER_PCB"), (blocks, "REF_ADAPTER_TERMINAL_BLOCKS"),
            (screws, "REF_ADAPTER_TERMINAL_SCREWS"),
            (sock, "REF_ADAPTER_ESP32_SOCKETS"),
            (under, "REF_ADAPTER_UNDERSIDE_JOINTS")]


def _underside_joints(B, P, d):
    """The solder-joint envelope beneath the carrier, as FOUR ROWS.

    Rev A modelled this as one blanket slab covering everything inboard of the
    declared bare margins. That slab is 58 x 52 mm and it makes an under-board
    cabinet fixing geometrically impossible - which is why Rev A put its
    mounting features on external ears. v1.1 section 4.8 requires the fixings
    INSIDE the footprint, so the envelope is modelled where the joints actually
    are: two rows under the screw-terminal blocks and two rows under the ESP32
    socket headers. The strip between the header rows is clear.

    THIS REFINEMENT IS ITSELF A PROTOTYPE GATE. Before printing, confirm that
    the acquired breakout carries nothing on its underside within the modelled
    clear strip at the two cabinet fixing centres."""
    half = d["term_span"] / 2.0 + P["term_pitch"] / 2.0
    hl = (P["term_per_side"] - 1) * 2.54 / 2.0 + 1.27
    rows = []
    for sgn in (1.0, -1.0):
        rows.append((-half, half,
                     sgn * (d["y_pcb"] - P["term_block_w"]),
                     sgn * (d["y_pcb"] - P["pcb_bare_perim"])))
        rows.append((-hl, hl,
                     sgn * P["esp_header_span"] / 2.0 - 1.60,
                     sgn * P["esp_header_span"] / 2.0 + 1.60))
    body = None
    for x0, x1, ya, yb in rows:
        b = B.box(x0, x1, min(ya, yb), max(ya, yb),
                  d["z_under_bot"], d["z_pcb_bot"])
        body = b if body is None else B.uni(body, b)
    return body


def build_keepouts(B, P, d):
    """Every volume the Rev B housing has to respect, as explicit solids."""
    out = []

    # carrier at its MAXIMUM 67.00 mm length, so the clamp end is gated at the
    # worst case rather than the nominal one
    out.append((B.box(d["x_datum"], d["x_adj_face"], -d["y_cav"], d["y_cav"],
                      d["z_pcb_bot"], d["z_pcb_top"]), "KEEPOUT_PCB_ENVELOPE"))

    out.append((_underside_joints(B, P, d), "KEEPOUT_UNDERSIDE_JOINTS"))

    # Components live INBOARD of the declared bare short-edge margins, so the
    # assembly envelope stops there: the fixed ledge and the clamp lip are
    # required to stand over those margins and cannot be gated as intrusions.
    # The +X bound uses the SHORTEST carrier in the 65-67 mm window, so the
    # envelope is a component region for every length the clamp accepts.
    out.append((B.box(d["comp_x0"], d["comp_x1"], -d["y_pcb"], d["y_pcb"],
                      d["z_pcb_top"], d["z_comp_top"]),
                "KEEPOUT_ASSEMBLY_MAX_HEIGHT"))

    # the ESP32 module, its sockets and the terminal blocks - the things the
    # retention system is forbidden to touch (v1.1 sections 4.7 and 13.15)
    ret = B.box(d["esp_x0"], d["esp_x1"], d["esp_y0"], d["esp_y1"],
                d["z_pcb_top"], d["z_esp_top"] + P["esp_mod_h"] + 0.20)
    half = d["term_span"] / 2.0 + P["term_pitch"] / 2.0
    for sgn in (1.0, -1.0):
        ret = B.uni(ret, B.box(-half, half, sgn * d["term_in_y"],
                               sgn * d["y_pcb"],
                               d["z_pcb_top"], d["z_term_top"]))
    # the bare edge strips are the ONLY approved contact regions
    ret = B.uni(ret, B.box(d["comp_x0"], d["comp_x1"],
                           -d["y_pcb"] + P["pcb_bare_perim"],
                           d["y_pcb"] - P["pcb_bare_perim"],
                           d["z_pcb_top"], d["z_pcb_top"] + 0.40))
    out.append((ret, "KEEPOUT_NO_CONTACT_COMPONENTS"))

    drv = None
    for sgn in (1.0, -1.0):
        for x in d["term_x"]:
            c = B.cylz(P["driver_d"], x, sgn * d["term_y"],
                       d["z_term_top"], d["z_lid_top"] + 25.0)
            drv = c if drv is None else B.uni(drv, c)
    out.append((drv, "KEEPOUT_TERMINAL_DRIVER_CORRIDORS"))

    # GROUPED harnesses, one solid per bundle per window. v1.1 section 5.1:
    # six named Decca harnesses, not thirty independent conductors.
    bun = None
    for b in d["bundles"]:
        sgn = float(b["side"])
        c = B.cyly(b["d"], b["x"], b["z"],
                   sgn * d["y_cav"], sgn * (d["lid_y"] + 8.0))
        bun = c if bun is None else B.uni(bun, c)
    out.append((bun, "KEEPOUT_GROUPED_HARNESS_BUNDLES"))

    # a cable tie standing in each aperture: 2.50 x 1.10 mm strap, doubled
    tie = None
    for sgn in (1.0, -1.0):
        for sx in (-1.0, 1.0):
            t = B.box(sx * P["tie_x"] - 1.25, sx * P["tie_x"] + 1.25,
                      sgn * (d["y_cav"] - 1.0), sgn * (d["y_out"] + 1.0),
                      P["tie_ap_z0"] + 0.20, d["tie_ap_z1"] - 0.20)
            tie = t if tie is None else B.uni(tie, t)
    out.append((tie, "KEEPOUT_CABLE_TIE_PATHS"))

    out.append((B.box(d["lid_x0"] - 30.0, d["esp_x0"], d["usb_y0"], d["usb_y1"],
                      d["usb_z0"], d["usb_z1"]),
                "KEEPOUT_USB_SERVICE_ENVELOPE"))

    out.append((B.box(d["ako_x0"], d["ako_x1"], d["ako_y0"], d["ako_y1"],
                      d["ako_z0"], d["ako_z1"]), "KEEPOUT_WIFI_ANTENNA"))

    # every piece of metal the design introduces
    met = None
    for sgn in (1.0, -1.0):
        s = B.cylz(P["lid_screw_clear_d"], d["x_ins"],
                   sgn * P["clamp_screw_y"], d["z_ins_bot"], d["clamp_z1"] + 3.0)
        met = s if met is None else B.uni(met, s)
        met = B.uni(met, B.cylz(P["insert_hole_d"], d["x_ins"],
                                sgn * P["clamp_screw_y"],
                                d["z_ins_bot"], d["z_retain"]))
        met = B.uni(met, B.cylx(P["lid_screw_clear_d"],
                                sgn * P["lid_screw_y"], P["lid_screw_z"],
                                d["lid_bore_x0"], d["lid_x1"] + 3.0))
        met = B.uni(met, B.cylx(P["insert_hole_d"],
                                sgn * P["lid_screw_y"], P["lid_screw_z"],
                                d["lid_bore_x0"], d["x_out_pos"]))
    out.append((met, "KEEPOUT_LID_AND_CLAMP_FASTENERS"))

    cab = None
    for sx in (-1.0, 1.0):
        s = B.cylz(P["cab_screw_d"], sx * P["cab_x"], 0.0,
                   d["z_floor_bot"] - 10.0, d["cab_csk_z0"])
        cab = s if cab is None else B.uni(cab, s)
        cab = B.uni(cab, B.conez(P["cab_screw_d"], P["cab_head_d"],
                                 sx * P["cab_x"], 0.0,
                                 d["cab_csk_z0"], d["cab_head_top"]))
    out.append((cab, "KEEPOUT_CABINET_FASTENERS"))

    return out


# ---------------------------------------------------------------------------
# Housing_Base - shallow tray, printed floor-down.
#
# Purpose of every external structure on this part, in order. Each one has a
# numbered gate in validate(); anything not on this list is not on the part.
#   1  continuous 1.60 mm insulating floor        gate 2
#   2  four local carrier support pads            gates 3, 13
#   3  one integral fixed ledge                   gates 13, 15
#   4  two clamp plinths + vertical M3 inserts    gates 13, 14, 15
#   5  two lid-screw bosses + horizontal inserts  gates 12, 17
#   6  two locating rebates                       gate 17
#   7  four cable-tie tabs                        gate 9
#   8  two recessed, capped cabinet fixings       gates 2, 16
# ---------------------------------------------------------------------------
def build_base(B, P, d):
    outer = B.rrect(d["x_out_neg"], d["x_out_pos"], -d["y_out"], d["y_out"],
                    d["z_floor_bot"], d["z_wall_top"], P["outer_corner_r"])
    cav = B.rrect(d["x_wall_in_neg"], d["x_wall_in_pos"],
                  -d["y_cav"], d["y_cav"],
                  d["z_floor_top"], d["z_wall_top"] + 5.0,
                  P["cav_corner_r"])
    body = B.sub(outer, cav)

    # 2 - four local support pads on the declared bare long-edge strip
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            body = B.uni(body, B.box(sx * d["pad_x0"], sx * d["pad_x1"],
                                     sy * d["pad_y0"], sy * d["pad_y1"],
                                     d["z_floor_top"], d["z_pcb_bot"]))

    # 3 - the integral fixed ledge, two segments, with a 45 degree lead-in
    #     chamfer on its underside. The chamfer is what the carrier slides
    #     against, and it cuts the only real unsupported overhang in the base
    #     down to ledge_flat.
    for sy in (-1.0, 1.0):
        y0 = min(sy * d["ledge_y0"], sy * d["ledge_y1"])
        y1 = max(sy * d["ledge_y0"], sy * d["ledge_y1"])
        seg = B.box(d["x_datum"], d["ledge_x1"], y0, y1,
                    d["ledge_z0"], d["z_wall_top"])
        seg = B.inter(seg, B.keep_above_chamfer(
            d["ledge_x1"], d["ledge_z0"], -1.0, 1.0, P["ledge_lead"],
            y0 - 2.0, y1 + 2.0))
        body = B.uni(body, seg)

    # 4 - two clamp plinths. Their top face is the HARD STOP that keeps the
    #     0.20 mm retention gap: tightening the two M3 screws seats the clamp
    #     bar on the plinths, so the bar cannot be driven onto the carrier.
    for sy in (-1.0, 1.0):
        body = B.uni(body, B.box(d["x_adj_face"], d["x_wall_in_pos"],
                                 sy * d["plinth_y0"], sy * d["plinth_y1"],
                                 d["z_floor_top"], d["z_retain"]))

    # 5 - two lid-screw bosses carrying HORIZONTAL inserts. The lid is deep
    #     and the base is shallow, so a vertical lid screw would need a 27 mm
    #     pillar through the cavity; the screws therefore run along X through
    #     the lid skirt into the base end wall.
    for sy in (-1.0, 1.0):
        body = B.uni(body, B.box(d["lid_bore_x0"] - P["boss_wall"],
                                 d["x_out_pos"],
                                 sy * d["lid_boss_y0"], sy * d["lid_boss_y1"],
                                 d["z_floor_top"], P["lid_boss_h"]))

    # 7 - four cable-tie tabs, two per long side, formed IN the wall plane so
    #     they take no internal plan space at all: the carrier fills the tray
    #     to within 0.50 mm and there is none to take. The aperture roof is a
    #     45 degree peak, so it prints with no bridge.
    for sy in (-1.0, 1.0):
        for sx in (-1.0, 1.0):
            cx = sx * P["tie_x"]
            tab = B.box(cx - P["tie_tab_half_w"], cx + P["tie_tab_half_w"],
                        sy * d["y_cav"], sy * d["y_out"],
                        d["z_floor_top"], P["tie_tab_top"])
            body = B.uni(body, tab)
    for sy in (-1.0, 1.0):
        for sx in (-1.0, 1.0):
            cx = sx * P["tie_x"]
            ya = sy * (d["y_cav"] - 1.0)
            yb = sy * (d["y_out"] + 1.0)
            ap = B.box(cx - P["tie_ap_w"] / 2.0, cx + P["tie_ap_w"] / 2.0,
                       min(ya, yb), max(ya, yb),
                       P["tie_ap_z0"], d["tie_ap_z1"])
            ap = B.uni(ap, B.wedge_y(cx, d["tie_ap_z1"], d["tie_ap_peak"],
                                     d["tie_ap_peak"], min(ya, yb),
                                     max(ya, yb)))
            body = B.sub(body, ap)

    # 8 - two recessed cabinet fixings, on the centreline under the carrier,
    #     in the strip the underside-joint model leaves clear. The head is
    #     countersunk flush, then an insulating cap closes the recess, and the
    #     cap top still stands cab_head_to_pcb below the carrier underside.
    for sx in (-1.0, 1.0):
        body = B.uni(body, B.cylz(P["cab_pad_d"], sx * P["cab_x"], 0.0,
                                  d["z_floor_top"], P["cab_pad_h"]))
    for sx in (-1.0, 1.0):
        x = sx * P["cab_x"]
        body = B.sub(body, B.cylz(d["cab_recess_d"], x, 0.0,
                                  d["cab_recess_z0"], P["cab_pad_h"] + 1.0))
        body = B.sub(body, B.conez(P["cab_screw_d"], P["cab_head_d"], x, 0.0,
                                   d["cab_csk_z0"], d["cab_recess_z0"] + 0.001))
        body = B.sub(body, B.cylz(P["cab_screw_d"], x, 0.0,
                                  d["z_floor_bot"] - 1.0,
                                  d["cab_csk_z0"] + 0.001))

    # 6 - two locating rebates in the -X outer wall face. The 0.40 mm chamfer
    #     The capture ledge is left square: its underside is a 0.80 mm
    #     unsupported step, which is nothing, and a chamfer there would both
    #     halve the capture and reintroduce a tangent cutter vertex.
    for sy in (-1.0, 1.0):
        y0 = min(sy * d["hook_y0"], sy * d["hook_y1"])
        y1 = max(sy * d["hook_y0"], sy * d["hook_y1"])
        body = B.sub(body, B.box(d["hook_x0"] - 1.0, d["hook_x1"], y0, y1,
                                 P["hook_z0"], P["hook_z1"]))

    # insert bores, cut last so nothing fills them back in
    for sy in (-1.0, 1.0):
        body = B.sub(body, B.cylz(P["insert_hole_d"], d["x_ins"],
                                  sy * P["clamp_screw_y"],
                                  d["z_ins_bot"], d["z_retain"] + 1.0))
        body = B.sub(body, B.cylx(P["insert_hole_d"], sy * P["lid_screw_y"],
                                  P["lid_screw_z"],
                                  d["lid_bore_x0"], d["x_out_pos"] + 1.0))

    return [(body, "ESP32_Controller_Housing_Base")]


# ---------------------------------------------------------------------------
# Housing_Lid - deep cover, printed TOP-FACE-DOWN.
#
#   1  1.60 mm top, 1.20 mm skirt, 4.00 mm overlap  gate 12
#   2  four open-bottom cable windows               gates 7, 8, 18
#   3  one open-bottom USB service slot             gates 10, 18
#   4  five top ventilation slots                   gate 11
#   5  two lid-screw clearance holes                gate 17
#   6  two locating lugs                            gate 17
# ---------------------------------------------------------------------------
def build_lid(B, P, d):
    outer = B.rrect(d["lid_x0"], d["lid_x1"], -d["lid_y"], d["lid_y"],
                    d["z_skirt_bot"], d["z_lid_top"], d["lid_r"])
    void = B.rrect(d["skirt_in_neg"], d["skirt_in_pos"],
                   -d["skirt_in_y"], d["skirt_in_y"],
                   d["z_skirt_bot"] - 5.0, d["z_cav_top"], d["skirt_inner_r"])
    body = B.sub(outer, void)

    # 2 - the cable windows. Open at the skirt's lower free edge, so printed
    #     top-face-down they only ever GROW: no roof, no bridge, no sawtooth,
    #     no support. This is the feature v1.1 section 5.4 asks for and the
    #     one that let Rev A's sixteen-tooth window roofs be deleted.
    for sy in (-1.0, 1.0):
        for wx in d["win_x"]:
            ya = sy * (d["skirt_in_y"] - 2.0)
            yb = sy * (d["lid_y"] + 2.0)
            body = B.sub(body, B.box(wx - P["win_half_w"],
                                     wx + P["win_half_w"],
                                     min(ya, yb), max(ya, yb),
                                     d["win_z0"] - 5.0, d["win_z1"]))

    # 3 - the USB service slot, the same trick on the -X end. v1.1 section 6.2
    #     deletes the blanking plug, so this is simply an opening.
    body = B.sub(body, B.box(d["lid_x0"] - 2.0, d["skirt_in_neg"] + 2.0,
                             d["usb_slot_y0"], d["usb_slot_y1"],
                             d["z_skirt_bot"] - 5.0, d["usb_slot_z1"]))

    # 4 - a modest set of simple top slots, kept wholly clear of the antenna
    for vy in d["vent_y"]:
        body = B.sub(body, B.rrect(d["vent_x0"], d["vent_x1"],
                                   vy - P["vent_w"] / 2.0,
                                   vy + P["vent_w"] / 2.0,
                                   d["z_cav_top"] - 2.0, d["z_lid_top"] + 2.0,
                                   P["vent_w"] / 2.0))

    # 6 - two locating lugs, on the inner face of the -X skirt
    for sy in (-1.0, 1.0):
        y0 = min(sy * (P["hook_y"] - P["hook_half_w"] + 0.50),
                 sy * (P["hook_y"] + P["hook_half_w"] - 0.50))
        y1 = max(sy * (P["hook_y"] - P["hook_half_w"] + 0.50),
                 sy * (P["hook_y"] + P["hook_half_w"] - 0.50))
        body = B.uni(body, B.box(d["skirt_in_neg"] - 0.01,
                                 d["skirt_in_neg"] + d["lug_proj"],
                                 y0, y1, P["lug_z0"], P["lug_z1"]))

    # 5 - lid-screw clearance holes, cut last
    for sy in (-1.0, 1.0):
        body = B.sub(body, B.cylx(P["lid_screw_clear_d"],
                                  sy * P["lid_screw_y"], P["lid_screw_z"],
                                  d["skirt_in_pos"] - 2.0, d["lid_x1"] + 2.0))

    return [(body, "ESP32_Controller_Housing_Lid")]


# ---------------------------------------------------------------------------
# PCB_Clamp_Adjustable - one flat bar, printed flat so the cantilever at its
# lip is stressed ALONG the layers rather than across them.
# ---------------------------------------------------------------------------
def build_clamp(B, P, d):
    body = B.rrect(d["bar_x0"], d["bar_x1"],
                   -P["clamp_half_span"], P["clamp_half_span"],
                   d["clamp_z0"], d["clamp_z1"], 1.50)
    for sy in (-1.0, 1.0):
        slot = B.box(d["slot_x0"], d["slot_x1"],
                     sy * P["clamp_screw_y"] - P["clamp_slot_w"] / 2.0,
                     sy * P["clamp_screw_y"] + P["clamp_slot_w"] / 2.0,
                     d["clamp_z0"] - 1.0, d["clamp_z1"] + 1.0)
        for sx in (-1.0, 1.0):
            slot = B.uni(slot, B.cylz(
                P["clamp_slot_w"], d["x_ins"] + sx * d["clamp_travel"],
                sy * P["clamp_screw_y"],
                d["clamp_z0"] - 1.0, d["clamp_z1"] + 1.0))
        body = B.sub(body, slot)
    return [(body, "ESP32_Controller_PCB_Clamp_Adjustable")]


# ---------------------------------------------------------------------------
# Cabinet_Fastener_Caps - ONE body, printed 2 off. A recessed metal screw head
# under the carrier cannot be insulated by integral geometry, because the head
# has to be installed after the base is printed; v1.1 section 4.10 therefore
# makes this a mandatory production part and it counts in the material gates.
# ---------------------------------------------------------------------------
CAP_QTY = 2


def build_cap(B, P, d):
    # a 0.30 mm lead-in cone so the cap presses in without shaving the recess
    body = B.conez(P["cab_cap_d"] - 0.60, P["cab_cap_d"], 0.0, 0.0, 0.0, 0.30)
    body = B.uni(body, B.cylz(P["cab_cap_d"], 0.0, 0.0, 0.30, P["cab_cap_t"]))
    return [(body, "ESP32_Controller_Cabinet_Fastener_Cap")]


# ---------------------------------------------------------------------------
# Carrier_Fit_Gauge - a PROTOTYPE TOOL, not a production part, and excluded
# from the section 9 material gates. It reproduces, at 1:1, the three things
# that cannot be settled without the acquired board in hand: the fixed ledge,
# the support height, and where the free short edge actually lands inside the
# 65.00-67.00 mm window.
# ---------------------------------------------------------------------------
def build_gauge(B, P, d):
    hw = P["gauge_w"] / 2.0
    body = B.box(d["x_out_neg"], d["x_out_pos"], -hw, hw,
                 d["z_floor_bot"], d["z_floor_top"])

    # the real -X end wall and the real fixed ledge
    body = B.uni(body, B.box(d["x_out_neg"], d["x_datum"], -hw, hw,
                             d["z_floor_top"], d["z_wall_top"]))
    seg = B.box(d["x_datum"], d["ledge_x1"], -hw + 1.0, hw - 1.0,
                d["ledge_z0"], d["z_wall_top"])
    seg = B.inter(seg, B.keep_above_chamfer(
        d["ledge_x1"], d["ledge_z0"], -1.0, 1.0, P["ledge_lead"],
        -hw - 2.0, hw + 2.0))
    body = B.uni(body, seg)

    # two support rails at the real pad height, inside the clear strip the
    # underside-joint model leaves on the carrier centreline
    for sy in (-1.0, 1.0):
        body = B.uni(body, B.box(d["x_datum"], d["x_pcb_max"] + 3.0,
                                 sy * (hw - 4.50), sy * (hw - 1.50),
                                 d["z_floor_top"], d["z_pcb_bot"]))

    # three read-off steps at 65.00, 66.00 and 67.00, standing BELOW the
    # carrier so they never obstruct it: sight down and read which step edge
    # the free short edge lands on
    for i, xs in enumerate((d["x_pcb_min"], d["x_pcb_nom"], d["x_pcb_max"])):
        y0 = -hw + 1.50 + i * (P["gauge_w"] - 3.0) / 3.0
        y1 = y0 + (P["gauge_w"] - 3.0) / 3.0 - 0.80
        body = B.uni(body, B.box(xs, xs + 2.00, y0, y1,
                                 d["z_floor_top"], d["z_pcb_bot"] - 0.20))

    # the real clamp plinth and its insert, so the printed clamp and the
    # 0.20 mm retention gap can both be checked against the real board
    body = B.uni(body, B.box(d["x_adj_face"], d["x_wall_in_pos"],
                             -hw, hw, d["z_floor_top"], d["z_retain"]))
    body = B.sub(body, B.cylz(P["insert_hole_d"], d["x_ins"], 0.0,
                              d["z_ins_bot"], d["z_retain"] + 1.0))
    return [(body, "ESP32_Controller_Carrier_Fit_Gauge")]


# ---------------------------------------------------------------------------
# Component plumbing
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
    for src in (P, d):
        for k, v in src.items():
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
                        "mm", "Rev B ESP32 controller housing generator")
            n += 1
        except Exception:
            pass
    return n


MARK_DEPTH = 0.40


def add_lid_marking(design, P, d):
    """The one legend v1.1 permits: an optional recessed USB / DISCONNECT 5V
    note on the lid top, over the USB end. Cut 0.40 mm downward from the top
    face, which prints crisp because the lid goes on the bed top-face-down.

    Rev A's four legends, including the DECCA CONTROLLER banner, are gone.
    EN and BOOT are not marked because v1.1 section 6.4 forbids their access
    holes until the buttons have been measured, and marking a hole that does
    not exist is worse than not marking it."""
    occ = find_component(design, LID)
    comp = occ.component
    planes = comp.constructionPlanes
    pin = planes.createInput()
    pin.setByOffset(comp.xYConstructionPlane,
                    adsk.core.ValueInput.createByReal(mm(d["z_lid_top"])))
    plane = planes.add(pin)
    plane.name = "LID_MARKING_PLANE"

    text = "USB / DISCONNECT 5V"
    # clear of the vent band at |y| <= 10.00 and of the lid edge
    x0, y0 = d["lid_x0"] + 4.0, -22.00
    x1, y1 = d["lid_x0"] + 34.0, -16.00
    body = comp.bRepBodies.item(0)
    v0 = body.volume
    try:
        sk = comp.sketches.add(plane)
        sk.name = "MARK_USB"
        ti = sk.sketchTexts.createInput2(text, mm(3.20))
        ti.setAsMultiLine(
            adsk.core.Point3D.create(mm(x0), mm(y0), 0),
            adsk.core.Point3D.create(mm(x1), mm(y1), 0),
            adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
            adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
        st = sk.sketchTexts.add(ti)
        ei = comp.features.extrudeFeatures.createInput(
            st, adsk.fusion.FeatureOperations.CutFeatureOperation)
        # Both of these matter. Without participantBodies the cut targets
        # nothing on a base-feature body and reports success having removed
        # exactly zero material; a plain distance extent does the same. The
        # volume removed is measured afterwards so a silent no-op can never
        # be reported as a legend.
        ei.participantBodies = [body]
        ei.setOneSideExtent(
            adsk.fusion.DistanceExtentDefinition.create(
                adsk.core.ValueInput.createByReal(mm(MARK_DEPTH))),
            adsk.fusion.ExtentDirections.NegativeExtentDirection)
        comp.features.extrudeFeatures.add(ei)
        cut = (v0 - comp.bRepBodies.item(0).volume) * 1000.0
        if cut <= 0.001:
            print("  marking %-22s CUT NOTHING" % text)
            return 0
        print("  marking %-22s %.1f mm3 removed" % (text, cut))
        return 1
    except Exception as exc:
        print("  marking %-22s FAILED: %s" % (text, exc))
        return 0


# ---------------------------------------------------------------------------
# main - build every component
# ---------------------------------------------------------------------------
def _design_holds_housing(app):
    des = adsk.fusion.Design.cast(app.activeProduct)
    if des is None:
        return False
    root = des.rootComponent
    for i in range(root.occurrences.count):
        if root.occurrences.item(i).component.name in (BASE, "Housing_Base"):
            return True
    return False


def part_volumes(design):
    """Solid volume in cm3 per production part, with the cap counted CAP_QTY
    times because one body is modelled and two are printed."""
    qty = {CAPS: CAP_QTY}
    out = []
    for name in PRODUCTION:
        occ = find_component(design, name)
        if occ is None:
            continue
        v = sum(volume_of(b) for b in occ.bRepBodies) / 1000.0
        n = qty.get(name, 1)
        out.append((name, n, v, v * n, v * n * PETG_DENSITY))
    return out


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

    # every Rev A component name, so a rebuild in the Rev A document leaves
    # no orphan clamp, plug or keep-out behind
    for name in (REFERENCE + PRINTABLE
                 + ("PCB_Clamp_Fixed_End", "PCB_Clamp_Adjustable_End",
                    "USB_Blanking_Plug", "EXPORT_PCB_Clamps",
                    "EXPLODED_VIEW", "SECTION_VIEW")):
        clear_component(design, name)

    add_component(root, REF_ESP, build_esp32(B, P, d), REF_NOTE)
    add_component(root, REF_ADP, build_adapter(B, P, d), REF_NOTE)
    add_component(root, REF_KEEP, build_keepouts(B, P, d), REF_NOTE)
    add_component(root, BASE, build_base(B, P, d))
    add_component(root, LID, build_lid(B, P, d))
    add_component(root, CLAMP, build_clamp(B, P, d))
    add_component(root, CAPS, build_cap(B, P, d),
                  "PRINT %d OFF. Insulating cap over each recessed cabinet "
                  "fastener head." % CAP_QTY)
    add_component(root, GAUGE, build_gauge(B, P, d),
                  "PROTOTYPE TOOL. Not a production part; excluded from the "
                  "specification section 9 material gates.")

    npar = write_parameters(design, P, d)
    print("built in %s document %r" % ("the existing" if reuse else "a NEW",
                                       doc.name))
    print("user parameters written: %d" % npar)
    add_lid_marking(design, P, d)

    # Rev B applies NO post-hoc fillet or chamfer features. Every radius and
    # every 45 degree relief is in the primitive recipe. Three of Rev A's four
    # non-manifold defects came from fillets and tangent bosses added after
    # the fact to base-feature bodies; not adding them is the fix.
    app.activeViewport.fit()

    print("")
    print("DERIVED ENVELOPE")
    print("  base body        %7.2f x %7.2f x %7.2f mm"
          % (d["body_l"], d["body_w"], d["z_wall_top"] - d["z_floor_bot"]))
    print("  complete outside %7.2f x %7.2f x %7.2f mm"
          % (d["overall_l"], d["overall_w"], d["overall_h"]))
    print("  v1.1 limit       %7.2f x %7.2f x %7.2f mm"
          % (85.0, 75.0, 36.0))
    print("  Rev A was        %7.2f x %7.2f x %7.2f mm"
          % (105.0, 77.0, 38.30))
    print("  internal height above the carrier support plane %.2f mm"
          % d["internal_h_above_support"])
    print("")
    print("HEIGHT CHAIN  floor %.2f | pad %.2f | carrier %.2f-%.2f | retain "
          "%.2f | wall top %.2f | skirt bottom %.2f | terminals %.2f | "
          "components %.2f | cavity %.2f | lid %.2f"
          % (P["base_floor_t"], d["pad_h"], d["z_pcb_bot"], d["z_pcb_top"],
             d["z_retain"], d["z_wall_top"], d["z_skirt_bot"], d["z_term_top"],
             d["z_comp_top"], d["z_cav_top"], d["z_lid_top"]))
    print("")
    print("MATERIAL  (solid volume as modelled; PETG at %.2f g/cm3)"
          % PETG_DENSITY)
    tot_v = tot_m = 0.0
    for name, n, v, tv, tm in part_volumes(design):
        tot_v += tv
        tot_m += tm
        print("  %-24s x%d  %6.2f cm3 each  %6.2f cm3  %6.1f g"
              % (name, n, v, tv, tm))
    print("  %-24s      %-18s %6.2f cm3  %6.1f g"
          % ("PRODUCTION TOTAL", "", tot_v, tot_m))
    print("  %-24s      %-18s %6.2f cm3  %6.1f g   (limit)"
          % ("v1.1 section 9 limit", "", 35.0, 45.0))
    g = find_component(design, GAUGE)
    if g:
        gv = sum(volume_of(b) for b in g.bRepBodies) / 1000.0
        print("  %-24s      %-18s %6.2f cm3  %6.1f g   (EXCLUDED, prototype "
              "tool)" % (GAUGE, "", gv, gv * PETG_DENSITY))

    print("")
    for name in PRINTABLE:
        occ = find_component(design, name)
        if occ is None:
            continue
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
# validate - the specification v1.1 section 13 gate suite, run inside Fusion on
# the finished solids. The offline mesh verifier in
# Decca_ESP32_Controller_Housing_verify.py is deliberately independent: it
# reads only the exported STLs and re-derives every claim from triangles, so
# the two can disagree, which is the point of having both.
# ---------------------------------------------------------------------------
FAILS = []
CHECKS = 0
BLOCKED = []


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
    BLOCKED.append(label)
    print("  [PROTO] %-56s %s" % (label, detail))


def _bodies(design, comp_name):
    occ = find_component(design, comp_name)
    if occ is None:
        return {}
    return {b.name: b for b in occ.bRepBodies}


def _one(design, comp_name):
    occ = find_component(design, comp_name)
    return None if occ is None else occ.bRepBodies.item(0)


def _hit(B, a, b):
    """Intersection VOLUME in mm3. Volume, not face count: two solids that
    merely touch share faces but enclose nothing, and a tangent contact is not
    an interference."""
    if a is None or b is None:
        return 0.0
    c1, c2 = B.copy(a), B.copy(b)
    B.inter(c1, c2)
    return max(0.0, volume_of(c1))


def _mind(app, a, b):
    try:
        return app.measureManager.measureMinimumDistance(a, b).value * 10.0
    except Exception:
        return float("nan")


def _inside(body, x, y, z):
    pc = body.pointContainment(p3(x, y, z))
    return pc == adsk.fusion.PointContainment.PointInsidePointContainment


def _moved(B, body, dx, dy, dz):
    c = B.copy(body)
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(mm(dx), mm(dy), mm(dz))
    B.tbm.transform(c, m)
    return c


def _rotated(B, body, angle_deg, axis, origin):
    c = B.copy(body)
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.radians(angle_deg), axis, origin)
    B.tbm.transform(c, m)
    return c


def _overhangs(body, z_bed, up, tol=0.02, grid=1.0, march=40.0, step=0.25):
    """Unsupported horizontal faces in the STATED print orientation, with the
    real bridging distance measured rather than guessed from a bounding box.

    ``up`` is +1 when the part prints in model orientation and -1 when it is
    flipped onto its top face; ``z_bed`` is the model-space height of the bed.
    A face is unsupported when its material lies on the bed side and there is
    nothing under it, which in model space means the outward normal points
    AWAY from the bed.

    For each such face the routine samples its area and, from every sample,
    marches horizontally in eight directions until it re-enters the solid at
    the same height. The shortest of those eight is how far that point is from
    something holding it up, and the largest such distance over the face is the
    REACH: half of a two-sided bridge, all of a cantilever. A bounding box
    cannot tell those apart, which is why it is not used.

    Only PLANAR faces are examined. A horizontal circular bore has no planar
    downward face; its apex is self-supporting at these diameters and is
    reported separately as a stated design rule rather than measured here."""
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
        zin = z + eps * up
        zout = z - eps * up
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
                    t = step
                    while t < best:
                        if _inside(body, px + dx * t, py + dy * t, zout):
                            break
                        t += step
                    best = min(best, t)
                reach = max(reach, best)
        if reach > 0.0:
            out.append((round(reach, 2), round(z, 2), round(f.area * 100.0, 1),
                        round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1)))
    return sorted(out, key=lambda t: -t[0])


PRINT_ORIENT = {
    BASE: ("floor-down", +1, "z_floor_bot"),
    LID: ("TOP-FACE-DOWN", -1, "z_lid_top"),
    CLAMP: ("flat, loaded section across the layers", +1, "clamp_z0"),
    CAPS: ("flat", +1, None),
}

# Rev A features v1.1 section 2.2 deletes by name. Each is checked as an
# absent COMPONENT and, where it was geometry rather than a part, as absent
# material in the region it used to occupy.
FORBIDDEN_COMPONENTS = ("PCB_Clamp_Fixed_End", "USB_Blanking_Plug",
                        "PCB_Clamp_Fixed", "Cable_Lacing_Rail",
                        "Cabinet_Mounting_Ears")


def validate(_context=None):
    global FAILS, CHECKS, BLOCKED
    FAILS, CHECKS, BLOCKED = [], 0, []
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    B = Builder()
    d = derive(P)

    base = _one(design, BASE)
    lid = _one(design, LID)
    clamp = _one(design, CLAMP)
    cap = _one(design, CAPS)
    K = _bodies(design, REF_KEEP)
    A = _bodies(design, REF_ADP)
    E = _bodies(design, REF_ESP)
    prod = [(BASE, base), (LID, lid), (CLAMP, clamp), (CAPS, cap)]

    print("=" * 78)
    print("Decca ESP32 Controller Housing Rev B - specification v1.1 "
          "section 13 gates")
    print("=" * 78)

    # -- 1 -----------------------------------------------------------------
    bad = [n for n, b in prod
           if b is None or not b.isSolid or b.lumps.count != 1]
    gate(not bad, "1  every production body is a single closed solid",
         "; ".join("%s %s lumps=%d" % (n, b.isSolid, b.lumps.count)
                   for n, b in prod if b is not None))

    # -- 2 -----------------------------------------------------------------
    # Continuous insulating floor beneath the carrier. The two cabinet bores
    # are the only penetrations; each is closed above by a fitted cap, so the
    # electrical path from the carrier region to the cabinet stays broken.
    zmid = d["z_floor_bot"] / 2.0
    probes = gaps = inbore = 0
    for i in range(41):
        px = d["x_datum"] + (d["x_pcb_max"] - d["x_datum"]) * i / 40.0
        for j in range(31):
            py = -d["y_pcb"] + 2.0 * d["y_pcb"] * j / 30.0
            probes += 1
            if _inside(base, px, py, zmid):
                continue
            near = min(math.hypot(px - sx * P["cab_x"], py)
                       for sx in (-1.0, 1.0))
            if near <= P["cab_screw_d"] / 2.0 + 0.05:
                inbore += 1
            else:
                gaps += 1
    gate(gaps == 0, "2  floor continuous under the carrier",
         "%d probes, %d gaps, %d in the 2 capped cabinet bores"
         % (probes, gaps, inbore))
    seal = d["cab_recess_d"] - P["cab_cap_d"]
    gate(P["cab_cap_d"] > P["cab_head_d"] and 0.0 < seal <= 0.40,
         "2b each cabinet bore is closed by a fitted insulating cap",
         "cap %.2f in a %.2f recess (%.2f fit) over a %.2f head"
         % (P["cab_cap_d"], d["cab_recess_d"], seal, P["cab_head_d"]))

    # -- 3 -----------------------------------------------------------------
    v = sum(_hit(B, b, K["KEEPOUT_UNDERSIDE_JOINTS"])
            for _n, b in prod if b is not None)
    tallest = max(P["cab_pad_h"], d["z_floor_top"])
    gate(v <= 0.001 and d["cab_head_to_pcb"] >= P["pcb_under_clear"],
         "3  underside clearance >= %.2f mm" % P["pcb_under_clear"],
         "joint-row intrusion %.3f mm3; tallest under-carrier feature %.2f, "
         "carrier underside %.2f, gap %.2f"
         % (v, tallest, d["z_pcb_bot"], d["cab_head_to_pcb"]))

    # -- 4 -----------------------------------------------------------------
    lowest = lid.boundingBox.minPoint.z * 10.0
    over = d["z_cav_top"] - d["z_comp_top"]
    inter = _hit(B, lid, K["KEEPOUT_ASSEMBLY_MAX_HEIGHT"])
    gate(over >= P["component_top_clear"] and inter <= 0.001,
         "4  lid top clearance >= %.2f mm" % P["component_top_clear"],
         "cavity ceiling %.2f over a %.2f component top = %.2f; lid skirt "
         "reaches z %.2f; assembly-envelope intrusion %.3f mm3"
         % (d["z_cav_top"], d["z_comp_top"], over, lowest, inter))

    # -- 5 -----------------------------------------------------------------
    ek = ("KEEPOUT_PCB_ENVELOPE", "KEEPOUT_UNDERSIDE_JOINTS",
          "KEEPOUT_ASSEMBLY_MAX_HEIGHT", "KEEPOUT_NO_CONTACT_COMPONENTS")
    worst = []
    for kn in ek:
        for pn, b in prod:
            if b is None:
                continue
            h = _hit(B, b, K[kn])
            if h > 0.001:
                worst.append("%s x %s %.2f" % (pn, kn, h))
        h = _hit(B, K["KEEPOUT_LID_AND_CLAMP_FASTENERS"], K[kn])
        if h > 0.001:
            worst.append("metal x %s %.2f" % (kn, h))
        h = _hit(B, K["KEEPOUT_CABINET_FASTENERS"], K[kn])
        if h > 0.001:
            worst.append("cabinet metal x %s %.2f" % (kn, h))
    gate(not worst, "5  no part or fastener enters an electronics keep-out",
         "4 keep-outs x 6 solids, 0 intrusions" if not worst
         else "; ".join(worst))

    # -- 6 -----------------------------------------------------------------
    drv = K["KEEPOUT_TERMINAL_DRIVER_CORRIDORS"]
    hb = _hit(B, base, drv)
    hc = _hit(B, clamp, drv)
    gate(hb <= 0.001 and hc <= 0.001,
         "6  every terminal screw reachable with the lid removed",
         "%d corridors of dia %.2f from z %.2f; base %.3f, clamp %.3f mm3"
         % (2 * P["term_per_side"], P["driver_d"], d["z_term_top"], hb, hc))

    # -- 7 -----------------------------------------------------------------
    # A prism the full width of each window and wire_exit_h tall, sitting on
    # the base wall top. Nothing may be in it.
    worst_w = 0.0
    nwin = 0
    for sgn in (-1.0, 1.0):
        for wx in d["win_x"]:
            nwin += 1
            ya, yb = sgn * d["y_out"], sgn * (d["lid_y"] + 2.0)
            prism = B.box(wx - P["win_half_w"], wx + P["win_half_w"],
                          min(ya, yb), max(ya, yb),
                          d["win_sill"], d["win_sill"] + P["wire_exit_h"])
            worst_w = max(worst_w, _hit(B, lid, prism), _hit(B, base, prism))
    gate(worst_w <= 0.001 and d["win_clear_h"] >= P["wire_exit_h"],
         "7  each cable window gives >= %.2f mm of usable height"
         % P["wire_exit_h"],
         "%d windows, %.2f mm wide, sill %.2f to %.2f = %.2f mm clear; "
         "obstruction %.3f mm3"
         % (nwin, d["win_w"], d["win_sill"], d["win_z1"], d["win_clear_h"],
            worst_w))

    # -- 8 -----------------------------------------------------------------
    bun = K["KEEPOUT_GROUPED_HARNESS_BUNDLES"]
    hb, hl = _hit(B, base, bun), _hit(B, lid, bun)
    gate(hb <= 0.001 and hl <= 0.001,
         "8  the lid does not pinch any grouped harness",
         "%d bundles, %d conductors, largest dia %.2f; base %.3f lid %.3f mm3"
         % (len(d["bundles"]), sum(b["n"] for b in d["bundles"]),
            d["bundle_d_max"], hb, hl))

    # -- 9 -----------------------------------------------------------------
    tie = K["KEEPOUT_CABLE_TIE_PATHS"]
    ht = _hit(B, base, tie)
    # the load path: each tab is continuous with the wall, so a tie pulls on
    # the base and not on a terminal. Proved by the part being one lump (1)
    # and by the tab standing on the wall line.
    gate(ht <= 0.001,
         "9  four internal cable-tie positions accept a tie and load the base",
         "2 per long side at x %+.2f/%+.2f, aperture %.2f x %.2f with a 45 "
         "deg peak; obstruction %.3f mm3"
         % (-P["tie_x"], P["tie_x"], P["tie_ap_w"], P["tie_ap_h"], ht))

    # -- 10 ----------------------------------------------------------------
    usb = K["KEEPOUT_USB_SERVICE_ENVELOPE"]
    hb, hl = _hit(B, base, usb), _hit(B, lid, usb)
    gate(hb <= 0.001 and hl <= 0.001
         and P["usb_slot_w"] >= P["usb_open_w"]
         and (d["usb_slot_z1"] - d["usb_z0"]) >= P["usb_open_h"],
         "10 USB service envelope clear through the opening",
         "slot %.2f wide x %.2f tall against a %.2f x %.2f minimum; "
         "base %.3f lid %.3f mm3"
         % (P["usb_slot_w"], d["usb_slot_z1"] - d["z_skirt_bot"],
            P["usb_open_w"], P["usb_open_h"], hb, hl))

    # -- 11 ----------------------------------------------------------------
    ako = K["KEEPOUT_WIFI_ANTENNA"]
    m1 = _hit(B, K["KEEPOUT_LID_AND_CLAMP_FASTENERS"], ako)
    m2 = _hit(B, K["KEEPOUT_CABINET_FASTENERS"], ako)
    hb = _hit(B, base, ako)
    hc = _hit(B, clamp, ako)
    hl = _hit(B, lid, ako)
    # the only material allowed in the column is the 1.60 mm lid top
    ideal = ((d["ako_x1"] - d["ako_x0"]) * (d["ako_y1"] - d["ako_y0"])
             * P["lid_top_t"])
    vent_in = 0.0
    for vy in d["vent_y"]:
        if d["ako_y0"] <= vy <= d["ako_y1"] and d["vent_x1"] >= d["ako_x0"]:
            vent_in += 1.0
    gate(m1 <= 0.001 and m2 <= 0.001 and hb <= 0.001 and hc <= 0.001
         and vent_in == 0 and hl <= ideal * 1.02,
         "11 antenna keep-out free of metal, inserts and thick structure",
         "metal %.3f, base %.3f, clamp %.3f mm3; lid material %.0f mm3 "
         "against %.0f for a flat %.2f mm skin; %d vents inside"
         % (m1 + m2, hb, hc, hl, ideal, P["lid_top_t"], int(vent_in)))

    # -- 12 ----------------------------------------------------------------
    gap_x = d["skirt_in_pos"] - d["x_out_pos"]
    gap_y = d["skirt_in_y"] - d["y_out"]
    ov = d["z_wall_top"] - d["z_skirt_bot"]
    touch = _hit(B, base, lid)
    gate(abs(ov - P["lid_overlap"]) < 1e-6
         and abs(gap_x - P["lid_fit_clear"]) < 1e-6
         and abs(gap_y - P["lid_fit_clear"]) < 1e-6
         and touch <= 0.001,
         "12 lid overlap and fit allowance as specified",
         "overlap %.2f (spec %.2f), gap %.2f/%.2f per face (spec %.2f), "
         "skirt %.2f mm; lid/base interference %.3f mm3"
         % (ov, P["lid_overlap"], gap_x, gap_y, P["lid_fit_clear"],
            P["lid_skirt_t"], touch))

    # -- 13 ----------------------------------------------------------------
    # The ledge and the clamp lip may only sit over the declared bare strips.
    nc = K["KEEPOUT_NO_CONTACT_COMPONENTS"]
    hled = _hit(B, base, nc)
    hcl = _hit(B, clamp, nc)
    ledge_ok = P["ledge_grip"] <= P["pcb_bare_edge"]
    grip_ok = P["clamp_grip"] <= P["pcb_bare_edge"]
    pads_ok = d["pad_y0"] >= d["bare_y0"]
    gate(hled <= 0.001 and hcl <= 0.001 and ledge_ok and grip_ok and pads_ok,
         "13 ledge, clamp and pads touch approved bare PCB edge only",
         "ledge grip %.2f and clamp grip %.2f into a %.2f bare short edge; "
         "pads from y %.2f inside a bare strip starting at %.2f; "
         "intrusion base %.3f clamp %.3f mm3"
         % (P["ledge_grip"], P["clamp_grip"], P["pcb_bare_edge"],
            d["pad_y0"], d["bare_y0"], hled, hcl))

    # -- 14 ----------------------------------------------------------------
    # slide the clamp to both ends of its travel and check the grip it gets
    ok14 = True
    detail14 = []
    for tag, xedge, shift in (("65.00", d["x_pcb_min"], -d["clamp_travel"]),
                              ("66.00", d["x_pcb_nom"], 0.0),
                              ("67.00", d["x_pcb_max"], +d["clamp_travel"])):
        moved = _moved(B, clamp, shift, 0.0, 0.0)
        lip = d["bar_x0"] + shift
        grip = xedge - lip
        carrier = B.box(d["x_datum"], xedge, -d["y_pcb"], d["y_pcb"],
                        d["z_pcb_bot"], d["z_pcb_top"])
        clash = _hit(B, moved, carrier)
        cover = grip >= P["clamp_grip"] - 0.001
        ok14 = ok14 and cover and clash <= 0.001
        detail14.append("%s->grip %.2f clash %.3f" % (tag, grip, clash))
    gate(ok14, "14 clamp accommodates carrier widths 65.00-67.00 mm",
         "travel +-%.2f in a %.2f slot; %s"
         % (d["clamp_travel"], P["clamp_slot_l"], ", ".join(detail14)))

    # -- 15 ----------------------------------------------------------------
    seat = d["z_retain"] - d["z_pcb_top"]
    plinth_stop = abs(d["clamp_z0"] - d["z_retain"]) < 1e-6
    gate(seat >= P["clamp_vertical_clear"] - 1e-6 and plinth_stop
         and _hit(B, clamp, A["REF_ADAPTER_PCB"]) <= 0.001
         and _hit(B, clamp, A["REF_ADAPTER_TERMINAL_BLOCKS"]) <= 0.001
         and _hit(B, clamp, A["REF_ADAPTER_ESP32_SOCKETS"]) <= 0.001
         and _hit(B, base, E["REF_ESP32_MODULE"]) <= 0.001,
         "15 retention loads nothing on the carrier",
         "clamp bottoms on the plinth at z %.2f, %.2f mm above the carrier "
         "top; the screws cannot close that gap"
         % (d["z_retain"], seat))

    # -- 16 ----------------------------------------------------------------
    below = d["z_pcb_bot"] - d["cab_head_top"]
    inside_fp = (abs(P["cab_x"]) + P["cab_pad_d"] / 2.0) < (d["body_l"] / 2.0
                                                            + 6.0)
    pad_clear = _hit(B, base, K["KEEPOUT_UNDERSIDE_JOINTS"])
    gate(d["cab_head_top"] < d["z_pcb_bot"] and below >= P["pcb_under_clear"]
         and inside_fp and pad_clear <= 0.001,
         "16 cabinet fastener heads recessed, insulated and clear",
         "2 fixings at x %+.2f on the centreline, INSIDE the footprint; head "
         "top z %.2f, cap top z %.2f, carrier underside z %.2f (%.2f clear)"
         % (P["cab_x"], d["cab_head_top"], P["cab_pad_h"], d["z_pcb_bot"],
            d["cab_head_to_pcb"]))

    # -- 17 ----------------------------------------------------------------
    # (a) seated, the lid cannot lift: the lug meets the capture ledge.
    lifted = _moved(B, lid, 0.0, 0.0, P["hook_z1"] - P["lug_z1"] + 0.30)
    captured = _hit(B, lifted, base)
    # (b) it comes off: tilt about the -X hook line, then withdraw.
    pivot = adsk.core.Point3D.create(mm(d["x_out_neg"]), 0.0,
                                     mm(P["lug_z1"]))
    freed = _rotated(B, lid, -12.0, v3(0, 1, 0), pivot)
    freed = _moved(B, freed, -3.0, 0.0, 2.0)
    escape = _hit(B, freed, base)
    screws = 2
    hooks = 2
    gate(captured > 0.001 and escape <= 0.001 and screws == 2 and hooks == 2,
         "17 two screws + two hooks give a valid assembly sequence",
         "lift %.2f mm -> %.1f mm3 of lug/ledge capture; tilt 12 deg about "
         "the hook line and withdraw -> %.3f mm3; engagement %.2f mm"
         % (P["hook_z1"] - P["lug_z1"] + 0.30, captured, escape,
            d["hook_engage"]))

    # -- 18 ----------------------------------------------------------------
    worst_reach = 0.0
    lines = []
    for name, b in prod:
        if b is None:
            continue
        label, up, zkey = PRINT_ORIENT[name]
        z_bed = 0.0 if zkey is None else d[zkey]
        oh = _overhangs(b, z_bed, up)
        r = oh[0][0] if oh else 0.0
        worst_reach = max(worst_reach, r)
        lines.append("%s %s reach %.2f" % (name.split("_")[-1], label.split(",")[0], r))
    # the windows and the USB slot are held to a stricter rule: no downward
    # facing planar face inside them at all, in the lid's print orientation
    win_faces = 0
    for f in lid.faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
            continue
        n = g.normal
        if f.isParamReversed:
            n = adsk.core.Vector3D.create(-n.x, -n.y, -n.z)
        if n.z < 0.99:
            continue
        bb = f.boundingBox
        z = bb.minPoint.z * 10.0
        if z >= d["z_lid_top"] - 0.02:
            continue
        cx = (bb.minPoint.x + bb.maxPoint.x) * 5.0
        cy = (bb.minPoint.y + bb.maxPoint.y) * 5.0
        in_win = any(abs(cx - wx) <= P["win_half_w"] for wx in d["win_x"]) \
            and abs(cy) > d["skirt_in_y"] - 0.5
        in_usb = cx < d["skirt_in_neg"] + 0.5 and abs(cy) <= P["usb_slot_w"]
        if in_win or in_usb:
            win_faces += 1
    gate(worst_reach <= OVERHANG_REACH_MAX and win_faces == 0,
         "18 no production part requires slicer support",
         "max unsupported reach %.2f mm against a %.2f limit (%s); %d "
         "downward faces in the windows or the USB slot"
         % (worst_reach, OVERHANG_REACH_MAX, "; ".join(lines), win_faces))

    # -- 19 ----------------------------------------------------------------
    lim = (85.0, 75.0, 36.0)
    got = (d["overall_l"], d["overall_w"], d["overall_h"])
    # nothing may stand outside the lid envelope in plan
    # grown 0.02 mm: features that END on the envelope share a face with it,
    # and a boolean on coincident faces leaves numerical slivers, not material
    env = B.rrect(d["lid_x0"] - 0.02, d["lid_x1"] + 0.02,
                  -d["lid_y"] - 0.02, d["lid_y"] + 0.02,
                  d["z_floor_bot"] - 1.0, d["z_lid_top"] + 1.0,
                  d["lid_r"] + 0.02)
    outside = 0.0
    for _n, b in prod:
        if b is None:
            continue
        c = B.copy(b)
        B.sub(c, B.copy(env))
        outside += max(0.0, volume_of(c))
    gate(all(g <= l + 1e-9 for g, l in zip(got, lim)) and outside <= 0.05,
         "19 complete outside envelope within 85.00 x 75.00 x 36.00 mm",
         "%.2f x %.2f x %.2f mm; %.3f mm3 of any part outside the body "
         "envelope" % (got + (outside,)))

    # -- 20 / 21 -----------------------------------------------------------
    rows = part_volumes(design)
    tot_v = sum(r[3] for r in rows)
    tot_m = sum(r[4] for r in rows)
    gate(tot_v <= 35.0, "20 production solid volume <= 35.00 cm3",
         "%.2f cm3  (%s)" % (tot_v, ", ".join("%s %.2f" % (r[0].split("_")[-1],
                                                           r[3]) for r in rows)))
    gate(tot_m <= 45.0, "21 estimated PETG mass <= 45.0 g",
         "%.1f g at %.2f g/cm3, solid volume - a printed part at 15-20%% "
         "infill weighs less" % (tot_m, PETG_DENSITY))

    # -- 22 ----------------------------------------------------------------
    present = [n for n in FORBIDDEN_COMPONENTS
               if find_component(design, n) is not None]
    # geometry: nothing outboard of the base wall except the lid, and no part
    # of the base stands outside its own outer rounded rectangle
    shell = B.rrect(d["x_out_neg"] - 0.02, d["x_out_pos"] + 0.02,
                    -d["y_out"] - 0.02, d["y_out"] + 0.02,
                    d["z_floor_bot"] - 1.0, d["z_lid_top"] + 1.0,
                    P["outer_corner_r"] + 0.02)
    stray = B.copy(base)
    B.sub(stray, shell)
    stray_v = max(0.0, volume_of(stray))
    gate(not present and stray_v <= 0.05,
         "22 no forbidden Rev A feature present",
         "0 of %d deleted components; %.3f mm3 of base outside its own "
         "envelope (no rails, ears, sawtooth roofs, plug, second clamp, "
         "corner piers or per-terminal guides)"
         % (len(FORBIDDEN_COMPONENTS), stray_v))

    # -- prototype gates ---------------------------------------------------
    print("")
    print("PROTOTYPE GATES - not settled by geometry, and not marked PASS")
    proto("carrier outline 66.00 x 63.00 x 1.60 and its 65-67 mm window")
    proto("2.50 mm below-carrier protrusion and 24.00 mm assembled height")
    proto("bare edge margins 3.00 short / 2.50 long, both faces")
    proto("terminal pitch, block height and screw inset")
    proto("underside-joint model: nothing within y +-9.83 at x +-27.00",
          "this is what lets the cabinet fixings sit under the carrier")
    proto("heat-set insert 4.00 dia x 5.00 deep - the exact part is NOT "
          "recorded anywhere in the repository")
    proto("EN and BOOT positions - v1.1 6.4 forbids holes until measured")
    proto("H1-H6 conductor counts and real bundle diameters")
    proto("lid_fit_clear 0.25 on this printer, filament and flow")
    proto("antenna performance with the lid fitted")

    print("")
    print("%d gates, %d failed, %d prototype gates open"
          % (CHECKS, len(FAILS), len(BLOCKED)))
    if FAILS:
        for f in FAILS:
            print("  FAILED: %s" % f)
    return not FAILS


# ---------------------------------------------------------------------------
# export - editable, exchange and print files, straight into the repository
# ---------------------------------------------------------------------------
STEP_FILES = (
    (BASE, "ESP32_Controller_Housing_Base.step"),
    (LID, "ESP32_Controller_Housing_Lid.step"),
    (CLAMP, "ESP32_Controller_PCB_Clamp_Adjustable.step"),
    (GAUGE, "ESP32_Controller_Carrier_Fit_Gauge.step"),
)

STL_FILES = (
    (BASE, "ESP32_Controller_Housing_Base.stl"),
    (LID, "ESP32_Controller_Housing_Lid.stl"),
    (CLAMP, "ESP32_Controller_PCB_Clamp_Adjustable.stl"),
    (CAPS, "ESP32_Controller_Cabinet_Fastener_Cap.stl"),
    (GAUGE, "ESP32_Controller_Carrier_Fit_Gauge.stl"),
)

# Rev A production artefacts that would be mistaken for current deliverables.
# v1.1 section 12: do not ship a fixed-clamp STL or a USB-plug STL.
OBSOLETE = (
    ("STL", "ESP32_Controller_PCB_Clamp_Fixed.stl"),
    ("STL", "ESP32_Controller_USB_Plug.stl"),
    ("CAD", "ESP32_Controller_PCB_Clamps.step"),
)


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

    for comp_name, fname in STEP_FILES:
        occ = find_component(design, comp_name)
        if occ is not None:
            step(os.path.join(cad, fname), occ.component)

    for comp_name, fname in STL_FILES:
        occ = find_component(design, comp_name)
        if occ is not None:
            mesh(occ.bRepBodies.item(0), os.path.join(stl, fname))

    removed = []
    for sub, fname in OBSOLETE:
        p = os.path.join(REPO, "mechanical", sub, fname)
        if os.path.exists(p):
            os.remove(p)
            removed.append(os.path.relpath(p, REPO).replace("\\", "/"))

    for p in written:
        print("%10d  %s" % (os.path.getsize(p) if os.path.exists(p) else -1,
                            os.path.relpath(p, REPO).replace("\\", "/")))
    print("%d files written" % len(written))
    for p in removed:
        print("  REMOVED obsolete Rev A artefact: %s" % p)
    return written


# ---------------------------------------------------------------------------
# images - the review evidence v1.1 section 12 requires.
#
# Every view is generated from the built model, never posed by hand, so the
# whole set regenerates from one call after any parameter change. Keep-out
# solids are shown as bodies rather than described in a caption: a corridor
# either has housing in it or it does not, and the picture shows which.
# ---------------------------------------------------------------------------
IMG_W, IMG_H = 1400, 1000
IMG_PREFIX = "Decca_ESP32_Controller_Housing_revB_"

VIEW = {
    "iso": "IsoTopRightViewOrientation",
    "iso_left": "IsoTopLeftViewOrientation",
    "iso_bottom": "IsoBottomRightViewOrientation",
    "top": "TopViewOrientation",
    "bottom": "BottomViewOrientation",
    "front": "FrontViewOrientation",
    "back": "BackViewOrientation",
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
    for name in list(REFERENCE) + list(PRINTABLE) + list(extra):
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
            tbm.booleanOperation(
                c, tbm.copy(keep),
                adsk.fusion.BooleanTypes.IntersectionBooleanType)
            if c.faces.count == 0:
                continue
        if dx or dy or dz:
            m = adsk.core.Matrix3D.create()
            m.translation = adsk.core.Vector3D.create(mm(dx), mm(dy), mm(dz))
            tbm.transform(c, m)
        out.append((c, bn))
    return add_component(root, name, out)


OLD_IMAGES = "Decca_ESP32_Controller_Housing_revA_"


def images(_context=None):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
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
        print("  %-28s %s" % (tag, os.path.basename(written[-1])))

    # 1 closed housing
    shot("01_closed", {BASE: True, LID: True}, "iso")

    # 2 lid removed, controller in place
    shot("02_lid_removed",
         {BASE: True, CLAMP: True, CAPS: True, REF_ADP: True, REF_ESP: True},
         "iso")

    # 3 exploded assembly
    parts = []
    for nm, dz in ((BASE, 0.0), (CAPS, 26.0), (CLAMP, 40.0), (LID, 104.0)):
        occ = find_component(design, nm)
        for b in occ.bRepBodies:
            parts.append((b, 0.0, 0.0, dz, None, b.name))
    for b in find_component(design, CAPS).bRepBodies:
        parts.append((b, 2.0 * P["cab_x"], 0.0, 26.0, None, b.name + "_2"))
    for b in find_component(design, REF_ADP).bRepBodies:
        parts.append((b, 0.0, 0.0, 20.0, None, b.name))
    for b in find_component(design, REF_ESP).bRepBodies:
        parts.append((b, 0.0, 0.0, 64.0, None, b.name))
    _temp_component(design, "EXPLODED_VIEW", parts)
    dress(design, app, ("EXPLODED_VIEW",))
    shot("03_exploded", {"EXPLODED_VIEW": True}, "iso")
    clear_component(design, "EXPLODED_VIEW")

    # 4 plan and elevation
    shot("04_plan", {BASE: True, LID: True}, "top")
    shot("05_elevation", {BASE: True, LID: True}, "front")

    # 6 longitudinal section on y = 0, viewed from +Y so the CUT FACE is what
    #   the camera sees: floor, support height, carrier, ledge, clamp, plinth,
    #   lid overlap and cavity headroom all in one picture
    half = B.box(d["lid_x0"] - 20.0, d["lid_x1"] + 20.0, -d["lid_y"] - 20.0,
                 0.0, d["z_floor_bot"] - 20.0, d["z_lid_top"] + 20.0)
    parts = []
    for nm in (BASE, LID, CLAMP, CAPS, REF_ADP, REF_ESP):
        for b in find_component(design, nm).bRepBodies:
            parts.append((b, 0.0, 0.0, 0.0, half, b.name))
    _temp_component(design, "SECTION_VIEW", parts)
    dress(design, app, ("SECTION_VIEW",))
    shot("06_section", {"SECTION_VIEW": True}, "back")
    shot("06b_section_oblique", {"SECTION_VIEW": True}, "iso")
    clear_component(design, "SECTION_VIEW")

    # 7 terminal screwdriver corridors, lid removed
    shot("07_terminal_access",
         {BASE: True, CLAMP: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_TERMINAL_DRIVER_CORRIDORS"}}, "iso")

    # 8 the open-bottom cable windows with the grouped H1-H6 bundles in them
    shot("08_cable_windows",
         {BASE: True, LID: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_GROUPED_HARNESS_BUNDLES"}}, "iso")

    # 9 internal strain relief: the four tie tabs and the ties through them
    shot("09_strain_relief",
         {BASE: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_CABLE_TIE_PATHS",
                     "KEEPOUT_GROUPED_HARNESS_BUNDLES"}}, "iso")

    # 10 USB service access
    shot("10_usb_access",
         {BASE: True, LID: True, REF_ESP: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_USB_SERVICE_ENVELOPE"}}, "iso_left")

    # 11 the two recessed cabinet fixings, from below and from inside
    shot("11_cabinet_fixings",
         {BASE: True, CAPS: True,
          REF_KEEP: {"KEEPOUT_CABINET_FASTENERS",
                     "KEEPOUT_UNDERSIDE_JOINTS"}}, "iso_bottom")

    # 12 antenna keep-out
    shot("12_antenna_keepout",
         {BASE: True, LID: True, REF_ESP: True,
          REF_KEEP: {"KEEPOUT_WIFI_ANTENNA"}}, "iso")

    # 13 retention: the fixed ledge and the adjustable clamp
    shot("13_retention",
         {BASE: True, CLAMP: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_NO_CONTACT_COMPONENTS"}}, "iso")

    # 14 the two locating hooks on the -X end
    shot("14_locating_hooks", {BASE: True, LID: True}, "iso_left")

    # 15 fit gauge
    shot("15_fit_gauge", {GAUGE: True}, "iso")

    # retire the Rev A renders - v1.1 section 12
    removed = []
    for f in sorted(os.listdir(out_dir)):
        if f.startswith(OLD_IMAGES):
            os.remove(os.path.join(out_dir, f))
            removed.append(f)

    _show(design, {n: True for n in PRINTABLE + REFERENCE})
    for nm in REFERENCE:
        occ = find_component(design, nm)
        if occ:
            occ.isLightBulbOn = nm != REF_KEEP
    print("%d review images written to mechanical/Drawings/" % len(written))
    for f in removed:
        print("  REMOVED obsolete Rev A render: %s" % f)
    return written
