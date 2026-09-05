# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev B parametric generator (Autodesk Fusion).

Controlling document: mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md
                      (its content is specification revision v1.3)
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
                        buttressed cable-tie piers, one per cable window;
                        two recessed, capped cabinet fixings under the board.
    Housing_Lid         deep cover carrying most of the side protection; four
                        open-bottom cable windows; one open-bottom USB service
                        slot; five top vent slots; two locating lugs.
    PCB_Clamp_Adjustable   one flat bar, two slotted M3 screws, +/-1.00 mm of
                        travel, bottoming on the plinths so the board is never
                        loaded.
    Cabinet_Fastener_Caps  two insulating discs over the recessed M3 heads.
    Carrier_Fit_Coupon  non-production prototype coupon for the 65-67 mm range.
    Insert_Fastener_Coupon  non-production prototype coupon for the
                        horizontal and vertical inserts, the countersink
                        and the retained cap.

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
    validate(None)  the specification v1.3 section 13 gate suite
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
COUPON_A = "Carrier_Fit_Coupon"
COUPON_B = "Insert_Fastener_Coupon"

REF_ESP = "REF_ESP32_DevKit_V1_30Pin"
REF_ADP = "REF_30Pin_Terminal_Adapter"
REF_KEEP = "REF_Wired_Keepouts"

# Parts that are printed and shipped. The carrier-fit coupon and the
# insert-fastener coupon are prototype tools and are excluded from the
# section 9 material gates; the caps are mandatory because a recessed metal
# screw head under the board cannot be insulated any other way.
PRODUCTION = (BASE, LID, CLAMP, CAPS)
COUPONS = (COUPON_A, COUPON_B)
PRINTABLE = PRODUCTION + COUPONS
REFERENCE = (REF_ESP, REF_ADP, REF_KEEP)

REF_NOTE = ("NON-MANUFACTURING REFERENCE. Dimensional starting values only - "
            "not measured hardware. Excluded from every printable export.")

PETG_DENSITY = 1.27                  # g/cm3, specification section 9

# Slicer evidence, Bambu Studio CLI, recorded in the build report. The
# full-solid figure above remains the conservative design gate; this is what
# the spool actually loses.
SLICER_PROFILE = ("Bambu Lab P1S, PETG-HF, 0.40 mm nozzle, 0.20 mm layers, "
                  "3 walls, 15% infill, no supports, textured PEI plate")

# The one FDM rule this design states for itself. v1.2 section 10 forbids
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
#   DESIGN    a design value taken from specification v1.2
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
    "carrier_len_min": 65.00,        # specification v1.2 section 3
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

    # -- Clearances, DESIGN (specification v1.2 section 3) -----------------
    "pcb_xy_clear": 0.50,
    "pcb_under_clear": 2.00,         # v1.1 lowers this from 3.00
    "component_top_clear": 2.00,     # v1.1 lowers this from 3.00
    "clamp_vertical_clear": 0.20,
    "antenna_keepout": 10.00,
    "lid_fit_clear": 0.25,

    # -- Structure, DESIGN --------------------------------------------------
    "base_floor_t": 1.60,            # v1.2 section 4.1
    "base_wall_t": 1.60,
    "base_wall_h": 9.00,             # shallow tray: wall top above floor top
    "lid_top_t": 1.60,               # v1.2 sections 7.4 and 8.1
    "lid_skirt_t": 1.20,             # three 0.40 mm perimeters
    "lid_overlap": 4.00,             # v1.2 section 8.3
    "outer_corner_r": 3.00,
    "cav_corner_r": 0.00,            # SQUARE internal corners: a filleted
                                     # cavity corner eats into the corner
                                     # of a square-routed carrier
    "boss_wall": 1.60,

    # -- Access, DESIGN -----------------------------------------------------
    "wire_exit_h": 10.00,            # REQUIRED clear window height
    "win_half_w": 11.00,             # half width of each cable window
    "win_x_centre": 20.00,           # +/- centres of the two windows per side
    "win_top": 24.00,                # window top, above the floor top
    "bundle_dx": 4.80,              # bundle centre, relative to its window
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

    # -- Cable-tie anchors, DESIGN ------------------------------------------
    # ONE anchor per cable window, inside that window, beside its own bundle.
    #
    # v1.2 built each anchor as a plain 1.60 mm slab - the bare wall thickness
    # - standing 13.90 mm above the wall top and taking its load near the tip.
    # It is now a BUTTRESSED PIER: the same 8.00 mm of wall carried up from the
    # floor, thickened to 2.60 mm in the cable-pull direction by a buttress
    # that projects into its own cable window, blended into the wall top on
    # both flanks by a generous R9.00 root radius, and with 2.00 mm of material
    # on every side of the aperture instead of 1.60.
    #
    # OUTBOARD IS THE ONLY DIRECTION WITH ROOM. The usable band on this wall is
    # the component keep-out at y 31.50 to the lid's outer face at y 35.05 -
    # 3.55 mm - and the strap has to climb the pier's outboard face inside the
    # window on its way to the loop. Thickening inboard is blocked by the
    # terminal blocks up to z 16.10 and by the assembly keep-out above them.
    # That is also why there is no inboard triangular gusset: below the
    # terminal tops there is 0.50 mm of space, and above them there is nothing
    # for a gusset to stand on. The blended foot does that job in the plane
    # that is actually free, which is what section 5c asks for.
    # The anchor sits on the -X side of its window and the bundle on the +X
    # side. That is not arbitrary: the lid is released by tilting its +X end up
    # about the locating hooks and withdrawing in -X, which leans every lid
    # feature -X in proportion to its height. With the anchor on the +X side of
    # its window the window's side wall walks into the buttress; on the -X side
    # the same motion carries it away. Gate 17 found this the hard way.
    "tie_dx": -5.00,                 # anchor centre, relative to its window
    "tie_tab_half_w": 4.00,          # 4.00 aperture + 2 x 2.00 mm of leg
    "tie_ap_w": 4.00,                # aperture width, X
    "tie_ap_h": 2.30,                # aperture straight height, Z
    "tie_ap_rise": 0.60,             # aperture floor above the terminal tops
    "tie_tab_cap": 2.00,             # pier material above the aperture apex
    "tie_boss_t": 1.00,              # outboard buttress -> 2.60 mm section
    "tie_blend_r": 9.00,             # root radius, pier flank into the sill
    "tie_blend_z": 14.00,            # top of the blended foot
    "tie_thk_min": 2.40,             # GATE: local thickness, pull direction
    "tie_ap_wall_min": 2.00,         # GATE: material around the aperture

    # -- Cable tie reference geometry, STARTING ------------------------------
    # A standard small nylon tie: 2.50 x 1.10 mm strap, 4.60 mm square head
    # 3.20 mm deep. Modelled so the gate can check the real loop, the real
    # insertion route and real tool access, not just that a hole exists.
    "tie_w": 2.50,                   # strap width
    "tie_t": 1.10,                   # strap thickness
    "tie_head_w": 4.60,              # locking head, across
    "tie_head_t": 3.20,              # locking head, along the strap
    "tie_loop_clear": 0.50,          # loop inner clearance on the bundle
    "tie_loop_gap": 0.30,            # loop underside to the window sill
    "tie_tail": 14.00,               # cut-tail clearance beyond the head
    "tie_tool_d": 11.00,             # tensioning-tool and finger access

    # -- Recessed cabinet fixings, DESIGN ----------------------------------
    "cab_x": 27.00,                  # +/- fixing centres, on the centreline
    "cab_screw_d": 3.40,             # M3 clearance
    # The screw-head envelope is now declared explicitly instead of a single
    # "head diameter" that the countersink only reached at its very top face.
    # NOMINAL is the ISO 10642 M3 countersunk head; MAX is the envelope this
    # design guarantees to swallow, including tolerance, plating and burr.
    # NEITHER IS MEASURED: the acquired screw is a prototype gate.
    "cab_head_d_nom": 6.00,          # STARTING - ISO 10642 M3, not measured
    "cab_head_d_max": 6.20,          # declared maximum head envelope
    "cab_head_angle": 90.00,         # included angle
    "cab_head_clear_r": 0.25,        # radial clearance on the max envelope
    # A cone exported to STL is a faceted polygon, and its across-flats is
    # smaller than the ideal circle - the offline verifier measured 6.64 on
    # a nominal 6.70. The manufacturing geometry IS the mesh, so the cone is
    # cut oversize by this much to guarantee the faceted part still swallows
    # the declared head plus its clearance.
    "cab_csk_facet": 0.10,           # diametral tessellation allowance
    "cab_pad_d": 13.00,
    "cab_pad_h": 2.40,               # pad top - stays 2.10 below the PCB
    "cab_recess_d": 10.40,           # cap recess, the controlling dimension
    "cab_cap_t": 1.00,
    "cab_cap_clear_r": 0.15,         # cap body, radial, a slide fit
    # Positive retention: three compliant nibs on the cap rim, each standing
    # cab_nib_int proud of the recess so the cap has to be pressed in.
    "cab_nib_n": 3,
    "cab_nib_r": 0.90,               # nib radius, 4.5 extrusion widths
    "cab_nib_int": 0.12,             # radial interference per nib
    "cab_pry_w": 2.80,               # pry notch in the pad rim, for removal
    "cab_pry_d": 1.60,

    # -- Ventilation, DESIGN -------------------------------------------------
    "vent_w": 2.00,
    "vent_l": 14.00,
    "vent_pitch": 4.50,
    "vent_n": 5,
    "vent_x": -15.00,                # centre, kept clear of the antenna

    # -- Prototype coupons (tools, excluded from the material gates) --------
    "coupon_w": 12.00,               # carrier coupon width
    "coupon_t": 1.60,
    "coupon2_w": 20.00,              # insert/fastener coupon width
    "coupon2_l": 26.00,
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

# The actual Decca harnesses, docs/Wiring.md. Specification v1.2 section 5.1
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
    # Additive, and deliberately so: v1.2 section 4.3 measures its 2.00 mm
    # BENEATH the lowest solder feature, and that feature hangs 2.50 mm below
    # the board. v1.2 lowers both clearances from Rev A's 3.00 mm, which is
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

    # window and bundle X positions, needed by the tie anchors below
    d["win_x"] = [-P["win_x_centre"], P["win_x_centre"]]
    d["bundle_x"] = [w + P["bundle_dx"] for w in d["win_x"]]

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

    # ---- four cable-tie anchors, ONE PER CABLE WINDOW ---------------------
    # Rev B as first published put the anchors at x +/-5.00 and the windows at
    # x +/-20.00, so every bundle had to run 15 mm inboard to its tie and 15 mm
    # back out to its window. Worse, the anchor aperture opened OUTBOARD into
    # the 0.25 mm lid-skirt gap and INBOARD into the 0.50 mm gap between the
    # wall and the terminal blocks, so no strap could actually be threaded
    # through it. Both are fixed here:
    #
    #   * one anchor per window, inside that window, beside its own bundle;
    #   * the aperture's OUTBOARD face opens into the window void, where the
    #     strap, the locking head and a finger all have room;
    #   * the aperture's INBOARD face sits ABOVE the terminal blocks, which is
    #     the only height at which the inboard side of the wall is open.
    #
    # The anchor cannot be coaxial with its bundle. A closed slot for a
    # 2.50 mm strap wrapping a Y-running bundle needs the strap's WIDTH across
    # the wall - about 4.4 mm with usable walls - and the band between the
    # component keep-out at y 31.50 and the lid's outer face at y 35.05 is only
    # 3.55 mm. The residual offset below is therefore a geometric minimum, not
    # a convenience.
    d["tie_x"] = [w + P["tie_dx"] for w in d["win_x"]]
    d["tie_ap_z0"] = d["z_term_top"] + P["tie_ap_rise"]
    d["tie_ap_z1"] = d["tie_ap_z0"] + P["tie_ap_h"]
    d["tie_ap_peak"] = P["tie_ap_w"] / 2.0
    d["tie_ap_apex"] = d["tie_ap_z1"] + d["tie_ap_peak"]
    d["tie_tab_top"] = d["tie_ap_apex"] + P["tie_tab_cap"]
    d["tie_ap_mid"] = (d["tie_ap_z0"] + d["tie_ap_z1"]) / 2.0
    # tensioning-tool and finger volume, above the terminal blocks
    d["tie_tool_z0"] = d["z_term_top"] + 0.50
    d["tie_tool_z1"] = d["tie_tool_z0"] + P["tie_tool_d"]
    # the number the review asked to minimise
    d["tie_deviation"] = abs(P["tie_dx"] - P["bundle_dx"])

    # ---- two recessed cabinet fixings, under the carrier ------------------
    # The countersink is now sized from a DECLARED MAXIMUM head envelope plus
    # a radial clearance, not from a single nominal diameter that the cone only
    # reached at its very top face. The usable recess is what the verifier
    # measures, and it must swallow cab_head_d_max + 2 x cab_head_clear_r.
    d["cab_csk_req"] = P["cab_head_d_max"] + 2.0 * P["cab_head_clear_r"]
    d["cab_csk_d"] = d["cab_csk_req"] + P["cab_csk_facet"]
    d["cab_csk_depth"] = ((d["cab_csk_d"] - P["cab_screw_d"]) / 2.0
                          / math.tan(math.radians(P["cab_head_angle"] / 2.0)))
    d["cab_recess_z1"] = P["cab_pad_h"]
    d["cab_recess_z0"] = P["cab_pad_h"] - P["cab_cap_t"]
    d["cab_csk_z0"] = d["cab_recess_z0"] - d["cab_csk_depth"]
    d["cab_head_top"] = d["cab_recess_z0"]          # head sits flush, under the cap
    d["cab_head_to_pcb"] = d["z_pcb_bot"] - P["cab_pad_h"]
    d["cab_floor_under_csk"] = d["cab_csk_z0"] - d["z_floor_bot"]
    # cap: a slide-fit body carrying cab_nib_n compliant nibs that stand proud
    # of the recess, so it presses in and stays in
    d["cab_cap_d"] = P["cab_recess_d"] - 2.0 * P["cab_cap_clear_r"]
    d["cab_nib_crest_d"] = P["cab_recess_d"] + 2.0 * P["cab_nib_int"]
    d["cab_nib_c"] = (d["cab_nib_crest_d"] / 2.0) - P["cab_nib_r"]
    d["cab_cap_wall"] = (P["cab_pad_d"] - P["cab_recess_d"]) / 2.0

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
    # reason v1.2 could delete Rev A's sixteen-tooth window roofs.
    d["win_z0"] = d["z_skirt_bot"]
    d["win_z1"] = P["win_top"]
    d["win_sill"] = d["z_wall_top"]
    d["win_clear_h"] = d["win_z1"] - d["win_sill"]

    # ---- the buttressed pier ----------------------------------------------
    # The pier spans tie_y0 (the cavity wall face) to tie_y1 (its buttress,
    # projecting tie_boss_t into the cable window). Everything below follows.
    d["tie_y0"] = d["y_cav"]
    d["tie_y1"] = d["y_out"] + P["tie_boss_t"]
    d["tie_thk"] = d["tie_y1"] - d["tie_y0"]
    d["tie_leg_w"] = P["tie_tab_half_w"] - P["tie_ap_w"] / 2.0
    d["tie_to_lid"] = d["lid_y"] - d["tie_y1"]
    d["tie_to_win_top"] = d["win_z1"] - d["tie_tab_top"]
    # The flank blend is one R tie_blend_r arc, tangent to the pier face at
    # z = tie_blend_z and running out to the wall top, so the foot width is a
    # consequence of the radius and the blend height rather than a second
    # number that could drift away from it.
    d["tie_blend_h"] = P["tie_blend_z"] - d["win_sill"]
    d["tie_foot_dx"] = (P["tie_blend_r"]
                        - math.sqrt(max(0.0, P["tie_blend_r"] ** 2
                                        - d["tie_blend_h"] ** 2)))
    d["tie_foot_half_w"] = P["tie_tab_half_w"] + d["tie_foot_dx"]
    d["tie_foot_to_window"] = (P["win_half_w"] - abs(P["tie_dx"])
                               - d["tie_foot_half_w"])
    # The blend is carried through the WALL BAND only, not through the
    # buttress. Two independent reasons, both measured by gates:
    #   * the harness corridor of gate 7 is defined outboard of the wall face,
    #     and a full-width blend reached 0.70 mm into H1's;
    #   * the lid's window side wall has to travel -X past the buttress to
    #     release the locating hooks, and a full-width blend left 0.48 mm.
    # Inboard of y_out the lid can never reach, and neither can a bundle.
    d["tie_blend_y1"] = d["y_out"]
    # what the lid has to be able to withdraw past the buttress, and what the
    # hooks actually need - gate 17
    d["tie_lid_withdraw"] = (P["win_half_w"] - abs(P["tie_dx"])
                             - P["tie_tab_half_w"])
    # unsupported height: from the top of the blended foot to the cap
    d["tie_free_h"] = d["tie_tab_top"] - P["tie_blend_z"]
    d["tie_free_h_v12"] = d["tie_tab_top"] - d["win_sill"]
    # where the strap climbs, just outboard of the buttress
    d["tie_run_y0"] = d["tie_y1"] + 0.20
    d["tie_run_y1"] = d["tie_run_y0"] + P["tie_t"]
    d["tie_run_proud"] = d["tie_run_y1"] - d["lid_y"]
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
        # The bundle rides high enough that its TIE LOOP passes under it
        # clear of the base wall top. Sizing this from the bundle alone put
        # the loop 1.10 mm inside the wall, which gate 9 caught.
        ro = dia / 2.0 + P["tie_loop_clear"] + P["tie_t"]
        z = d["win_sill"] + ro + P["tie_loop_gap"]
        bundles.append({
            "ids": "+".join(g["ids"]), "n": g["n"], "d": dia,
            "side": side, "win": win,
            "x": d["bundle_x"][win],           # off-centre, so its tie fits
            "tie_x": d["tie_x"][win],          # the anchor that restrains it
            "win_x": d["win_x"][win],
            "z": z,
            # the tie loop that actually wraps this bundle
            "loop_ri": dia / 2.0 + P["tie_loop_clear"],
            "loop_ro": dia / 2.0 + P["tie_loop_clear"] + P["tie_t"],
        })
    d["bundles"] = bundles
    d["bundle_d_max"] = max(b["d"] for b in bundles)
    d["bundle_top_max"] = max(b["z"] + b["d"] / 2.0 for b in bundles)
    d["loop_ro_max"] = max(b["loop_ro"] for b in bundles)
    # every loop must pass clear of the wall top it sits over
    d["loop_to_sill"] = min(b["z"] - b["loop_ro"] - d["win_sill"]
                            for b in bundles)
    d["loop_top_max"] = max(b["z"] + b["loop_ro"] for b in bundles)
    # the loop must not foul its own anchor
    # (side-agnostic: the anchor may sit either side of its bundle)
    d["loop_to_tab"] = min(abs(b["tie_x"] - b["x"]) - P["tie_tab_half_w"]
                           - b["loop_ro"] for b in bundles)
    # nor run outside its window
    d["loop_in_window"] = min(
        P["win_half_w"] - (abs(b["x"] - b["win_x"]) + b["loop_ro"])
        for b in bundles)

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

    v1.2 section 6.4 forbids EN/BOOT access holes until the buttons have been
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
    mounting features on external ears. v1.2 section 4.8 requires the fixings
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


def _one_tie(B, P, d, b, acc):
    """One FITTED cable tie, as the solids a fitter actually has to route.

    Order of assembly:
      1. feed the tail inboard-to-outboard through the anchor aperture. The
         inboard face sits above the terminal blocks, which is the only height
         at which that side of the wall is open at all;
      2. take it up the outboard face of the wall, inside the window void;
      3. across to the bundle at the top of the loop;
      4. round the bundle - the loop passes UNDER it, clear of the wall top,
         which is what sets the bundle's ride height;
      5. back to the locking head, which sits inboard above the terminal
         blocks where a tensioning tool can reach it;
      6. cut the tail.

    The strap turns through 90 degrees between the anchor and the loop. That
    is what a tie does at any tie-down point, and it is unavoidable here: the
    loop must lie in XZ to wrap a Y-running bundle, while a closed anchor slot
    for a 2.50 mm strap in that plane would need about 4.4 mm across the wall
    and only 3.55 mm exists between the component keep-out and the lid."""
    sgn = float(b["side"])
    w2 = P["tie_w"] / 2.0
    t2 = P["tie_t"] / 2.0
    zm = d["tie_ap_mid"]
    z_top = b["z"] + b["loop_ro"]                  # top of the loop
    y_run0 = sgn * d["tie_run_y0"]                 # outboard face of the pier
    y_run1 = sgn * d["tie_run_y1"]
    y_loop = sgn * (d["y_cav"] + 1.20)             # clear of the terminals

    def bx(x0, x1, y0, y1, z0, z1):
        return B.box(min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1),
                     min(z0, z1), max(z0, z1))

    # 1 - strap through the anchor aperture
    body = bx(b["tie_x"] - w2, b["tie_x"] + w2,
              sgn * (d["tie_y0"] - 1.00), sgn * (d["tie_y1"] + 1.20),
              zm - t2, zm + t2)

    # 2 - up the outboard face of the wall, inside the window
    body = B.uni(body, bx(b["tie_x"] - w2, b["tie_x"] + w2,
                          y_run0, y_run1, zm - t2, z_top + t2))

    # 3 - across to the bundle, at the top of the loop
    body = B.uni(body, bx(b["tie_x"], b["x"], y_run0, y_run1,
                          z_top - t2, z_top + t2))

    # 3b - and inboard onto the loop plane
    body = B.uni(body, bx(b["x"] - w2, b["x"] + w2, y_loop, y_run1,
                          z_top - t2, z_top + t2))

    # 4 - the loop itself, in the XZ plane around the bundle
    ring = B.cyly(2.0 * b["loop_ro"], b["x"], b["z"],
                  y_loop - w2, y_loop + w2)
    ring = B.sub(ring, B.cyly(2.0 * b["loop_ri"], b["x"], b["z"],
                              y_loop - w2 - 1.0, y_loop + w2 + 1.0))
    body = B.uni(body, ring)

    # 5 - locking head, inboard of the anchor and above the terminal blocks
    hw = P["tie_head_w"] / 2.0
    ya = sgn * (d["y_cav"] - 1.00)
    yb = sgn * (d["y_cav"] - 1.00 - P["tie_head_t"])
    body = B.uni(body, bx(b["tie_x"] - hw, b["tie_x"] + hw, ya, yb,
                          zm - hw, zm + hw))

    # 6 - cut tail, pulled inboard
    yc = sgn * (d["y_cav"] - 1.00 - P["tie_head_t"] - P["tie_tail"])
    body = B.uni(body, bx(b["tie_x"] - w2, b["tie_x"] + w2, yb, yc,
                          zm - t2, zm + t2))
    return body if acc is None else B.uni(acc, body)


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
    # retention system is forbidden to touch (v1.2 sections 4.7 and 13.15)
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

    # GROUPED harnesses, one solid per bundle per window. v1.2 section 5.1:
    # six named Decca harnesses, not thirty independent conductors.
    bun = None
    for b in d["bundles"]:
        sgn = float(b["side"])
        c = B.cyly(b["d"], b["x"], b["z"],
                   sgn * d["y_cav"], sgn * (d["lid_y"] + 8.0))
        bun = c if bun is None else B.uni(bun, c)
    out.append((bun, "KEEPOUT_GROUPED_HARNESS_BUNDLES"))

    # A REAL cable tie at each of the four positions, not a placeholder slot.
    # Rev B as first published modelled the tie as a 2.50 x 2.20 box sitting in
    # the aperture, which proved only that a hole existed. This models the
    # whole fitted tie - the loop that wraps the bundle, the strap through the
    # anchor, the locking head, the cut tail - so the gate can check the route
    # a fitter actually has to take.
    tie = None
    for b in d["bundles"]:
        tie = _one_tie(B, P, d, b, tie)
    out.append((tie, "KEEPOUT_CABLE_TIES"))

    # the volume a tensioning tool and two fingers need at each head
    tool = None
    for b in d["bundles"]:
        sgn = float(b["side"])
        ya = sgn * d["y_cav"]
        yb = sgn * (d["y_cav"] - P["tie_tail"])
        t = B.box(b["tie_x"] - P["tie_tool_d"] / 2.0,
                  b["tie_x"] + P["tie_tool_d"] / 2.0,
                  min(ya, yb), max(ya, yb),
                  d["tie_tool_z0"], d["tie_tool_z1"])
        tool = t if tool is None else B.uni(tool, t)
    out.append((tool, "KEEPOUT_TIE_TOOL_ACCESS"))

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
        # the DECLARED MAXIMUM head, not a nominal one: this is the envelope
        # the countersink has to swallow, and the gate measures against it
        cab = B.uni(cab, B.conez(P["cab_screw_d"], P["cab_head_d_max"],
                                 sx * P["cab_x"], 0.0,
                                 d["cab_head_top"] - (P["cab_head_d_max"]
                                                      - P["cab_screw_d"]) / 2.0,
                                 d["cab_head_top"]))
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
#   7  four buttressed cable-tie piers             gates 9, 9b, 9c
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

    # 7 - four cable-tie anchors, ONE PER CABLE WINDOW, standing in the wall
    #     plane inside their own window so no bundle has to detour to reach
    #     one. The aperture's outboard face opens into the window void and its
    #     inboard face sits above the terminal blocks; those are the only two
    #     places on this wall where a strap can actually be got at. The roof
    #     is a 45 degree peak, so it prints with no bridge.
    #
    #     Each one is a BUTTRESSED PIER rather than the 1.60 mm upright v1.2
    #     published. Three solids per anchor:
    #       a) the pier, carried from the print bed to the top of the cap,
    #          8.00 mm wide and tie_thk (2.60 mm) thick in the pull direction;
    #       b) the foot, the same section widened to tie_foot_half_w for the
    #          full depth of the base wall, so the blend lands on solid
    #          material and the buttress is supported off the bed;
    #       c) the root blend on each flank - a block with an R tie_blend_r
    #          disc taken out of it, tangent to the pier face at tie_blend_z
    #          and running out to the wall top. One radius, both jobs: the
    #          broad blended foot and the generous root radius.
    #     Both flanks are blended, including the bundle side: the tie loop is
    #     at its widest at the aperture, not at the sill, so there is room
    #     down there and gate 9 measures what is left.
    for sy in (-1.0, 1.0):
        for tx in d["tie_x"]:
            hw = P["tie_tab_half_w"]
            fw = d["tie_foot_half_w"]
            y0, y1 = sy * d["tie_y0"], sy * d["tie_y1"]
            body = B.uni(body, B.box(tx - hw, tx + hw, y0, y1,
                                     d["z_floor_bot"], d["tie_tab_top"]))
            body = B.uni(body, B.box(tx - fw, tx + fw, y0,
                                     sy * d["tie_blend_y1"],
                                     d["z_floor_bot"], d["win_sill"]))
            for sx in (-1.0, 1.0):
                # overlap the pier and the foot by 0.20 so no boolean in this
                # stack is ever asked to union two exactly coincident faces
                blk = B.box(tx + sx * (hw - 0.20), tx + sx * fw, y0,
                            sy * d["tie_blend_y1"],
                            d["win_sill"] - 0.20, P["tie_blend_z"])
                blk = B.sub(blk, B.cyly(
                    2.0 * P["tie_blend_r"],
                    tx + sx * (hw + P["tie_blend_r"]), P["tie_blend_z"],
                    min(y0, y1) - 1.0, max(y0, y1) + 1.0))
                body = B.uni(body, blk)
    for sy in (-1.0, 1.0):
        for tx in d["tie_x"]:
            ya = sy * (d["tie_y0"] - 1.0)
            yb = sy * (d["tie_y1"] + 1.0)
            ap = B.box(tx - P["tie_ap_w"] / 2.0, tx + P["tie_ap_w"] / 2.0,
                       min(ya, yb), max(ya, yb),
                       d["tie_ap_z0"], d["tie_ap_z1"])
            ap = B.uni(ap, B.wedge_y(tx, d["tie_ap_z1"], d["tie_ap_peak"],
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
        body = B.sub(body, B.cylz(P["cab_recess_d"], x, 0.0,
                                  d["cab_recess_z0"], P["cab_pad_h"] + 1.0))
        # the countersink is sized from the DECLARED MAXIMUM head envelope
        # plus a radial clearance, so the head lands fully below the cap with
        # tolerance to spare rather than only kissing the top face
        body = B.sub(body, B.conez(P["cab_screw_d"], d["cab_csk_d"], x, 0.0,
                                   d["cab_csk_z0"], d["cab_recess_z0"] + 0.001))
        body = B.sub(body, B.cylz(P["cab_screw_d"], x, 0.0,
                                  d["z_floor_bot"] - 1.0,
                                  d["cab_csk_z0"] + 0.001))
        # a pry notch through the recess rim, so the cap comes out with a
        # fine blade and the base survives it
        body = B.sub(body, B.box(
            x - P["cab_pry_w"] / 2.0, x + P["cab_pry_w"] / 2.0,
            P["cab_recess_d"] / 2.0 - P["cab_pry_d"],
            P["cab_pad_d"] / 2.0 + 1.0,
            d["cab_recess_z0"], P["cab_pad_h"] + 1.0))

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
    #     no support. This is the feature v1.2 section 5.4 asks for and the
    #     one that let Rev A's sixteen-tooth window roofs be deleted.
    for sy in (-1.0, 1.0):
        for wx in d["win_x"]:
            ya = sy * (d["skirt_in_y"] - 2.0)
            yb = sy * (d["lid_y"] + 2.0)
            body = B.sub(body, B.box(wx - P["win_half_w"],
                                     wx + P["win_half_w"],
                                     min(ya, yb), max(ya, yb),
                                     d["win_z0"] - 5.0, d["win_z1"]))

    # 3 - the USB service slot, the same trick on the -X end. v1.2 section 6.2
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
# has to be installed after the base is printed; v1.2 section 4.10 therefore
# makes this a mandatory production part and it counts in the material gates.
# ---------------------------------------------------------------------------
CAP_QTY = 2


def build_cap(B, P, d):
    """Positively retained insulating cap.

    Rev B as first published had a 10.20 cap in a 10.40 recess and the report
    called it a press fit. It was a 0.20 mm CLEARANCE fit: the cap would fall
    out of a base mounted vertically. This is the fix, and it is the simplest
    arrangement that prints on a 0.4 mm nozzle without support:

      * the cap BODY is a slide fit, cab_cap_clear_r under the recess, so it
        enters square and does not shave a ring of swarf onto the screw head;
      * cab_nib_n compliant nibs on the rim stand cab_nib_int proud of the
        recess, so seating it takes a deliberate push and lifting it takes a
        deliberate pull;
      * a 0.30 mm lead-in cone starts the nibs into the bore;
      * the nibs are r0.90 - four and a half extrusion widths - not a thin
        cantilever snap, because a 0.4 mm nozzle cannot make a reliable one;
      * a pry notch in the base rim gets a blade under the cap for service.

    Nothing here is adhesive, and after assembly the carrier sits 2.10 mm above
    the cap, so it is captive whatever the enclosure's attitude."""
    body = B.conez(d["cab_cap_d"] - 0.60, d["cab_cap_d"], 0.0, 0.0, 0.0, 0.30)
    body = B.uni(body, B.cylz(d["cab_cap_d"], 0.0, 0.0, 0.30, P["cab_cap_t"]))
    for i in range(int(P["cab_nib_n"])):
        a = 2.0 * math.pi * i / float(P["cab_nib_n"])
        nx = d["cab_nib_c"] * math.cos(a)
        ny = d["cab_nib_c"] * math.sin(a)
        nib = B.cylz(2.0 * P["cab_nib_r"], nx, ny, 0.30, P["cab_cap_t"])
        # taper the nib's leading end so it starts into the recess
        nib = B.uni(nib, B.conez(2.0 * P["cab_nib_r"] - 0.60,
                                 2.0 * P["cab_nib_r"], nx, ny, 0.0, 0.30))
        body = B.uni(body, nib)
    return [(body, "ESP32_Controller_Cabinet_Fastener_Cap")]


# ---------------------------------------------------------------------------
# Prototype coupons. These are TOOLS, not production parts, and v1.2 section 9
# excludes them from the material gates.
#
# The Rev B fit gauge was 78.70 x 18.00 mm and 5.35 cm3 - a near-full-width
# representation of the enclosure that tested only the carrier interface and
# the VERTICAL clamp insert. The two lid screws use HORIZONTAL heat-set
# inserts, which is the harder and completely untested case, and the cabinet
# countersink and the retained cap were untested too. Two narrow coupons cover
# all six interfaces for less filament than the one gauge did.
# ---------------------------------------------------------------------------
def build_coupon_a(B, P, d):
    """Coupon A - the carrier interface, at 1:1 over the full carrier length.

    Tests: the fixed ledge and its lead-in, the 4.50 mm support height, the
    0.20 mm retention gap, the clamp plinth and its VERTICAL insert, and where
    the free short edge really lands in the 65.00-67.00 mm window.

    It has to span the carrier, so its length is not negotiable; its width is,
    and 12.00 mm keeps both support rails inside the clear strip the
    underside-joint model leaves on the carrier centreline."""
    hw = P["coupon_w"] / 2.0
    body = B.box(d["x_out_neg"], d["x_wall_in_pos"], -hw, hw,
                 d["z_floor_bot"], d["z_floor_top"])

    # the real -X end wall and the real fixed ledge, chamfer and all
    body = B.uni(body, B.box(d["x_out_neg"], d["x_datum"], -hw, hw,
                             d["z_floor_top"], d["z_wall_top"]))
    seg = B.box(d["x_datum"], d["ledge_x1"], -hw + 1.0, hw - 1.0,
                d["ledge_z0"], d["z_wall_top"])
    seg = B.inter(seg, B.keep_above_chamfer(
        d["ledge_x1"], d["ledge_z0"], -1.0, 1.0, P["ledge_lead"],
        -hw - 2.0, hw + 2.0))
    body = B.uni(body, seg)

    # FOUR local support pads at the real pad height, in the same
    # arrangement as the base. Two full-length rails would cost 1.10 cm3 more
    # and would test a support scheme the housing does not have.
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            body = B.uni(body, B.box(
                sx * d["pad_x0"], sx * d["pad_x1"],
                sy * (hw - 3.20), sy * (hw - 1.00),
                d["z_floor_top"], d["z_pcb_bot"]))

    # three read-off steps at 65.00 / 66.00 / 67.00, standing BELOW the carrier
    # so they never obstruct it: sight down and read which one the free edge
    # lands on
    band = (P["coupon_w"] - 2.4) / 3.0
    for i, xs in enumerate((d["x_pcb_min"], d["x_pcb_nom"], d["x_pcb_max"])):
        y0 = -hw + 1.20 + i * band
        body = B.uni(body, B.box(xs, xs + 1.60, y0, y0 + band - 0.80,
                                 d["z_floor_top"], d["z_pcb_bot"] - 0.20))

    # the real clamp plinth and its vertical insert
    body = B.uni(body, B.box(d["x_adj_face"], d["x_wall_in_pos"], -hw, hw,
                             d["z_floor_top"], d["z_retain"]))
    body = B.sub(body, B.cylz(P["insert_hole_d"], d["x_ins"], 0.0,
                              d["z_ins_bot"], d["z_retain"] + 1.0))
    return [(body, "ESP32_Controller_Carrier_Fit_Coupon")]


def build_coupon_b(B, P, d):
    """Coupon B - the fastener interfaces, all at production geometry.

    Tests: one HORIZONTAL lid-screw boss identical to the base's, one vertical
    clamp insert, the cabinet countersink against the real screw, and the
    positively retained cap including its pry notch.

    The horizontal insert is the point of this coupon. A heat-set insert driven
    into a horizontal bore in a wall printed on its side is the one fastener in
    this design whose feasibility nobody has demonstrated, and it is cheaper to
    find out on 2 cm3 of PETG than on the base."""
    hw = P["coupon2_w"] / 2.0
    ln = P["coupon2_l"]

    # a plate to stand it all on, with the base's own floor thickness
    body = B.box(0.0, ln, -hw, hw, d["z_floor_bot"], d["z_floor_top"])

    # -- horizontal lid-screw boss, production geometry, on its own end wall
    bx1 = ln
    bx0 = bx1 - (d["x_out_pos"] - (d["lid_bore_x0"] - P["boss_wall"]))
    body = B.uni(body, B.box(bx0, bx1,
                             -P["lid_boss_half_w"], P["lid_boss_half_w"],
                             d["z_floor_top"], P["lid_boss_h"]))
    body = B.sub(body, B.cylx(P["insert_hole_d"], 0.0, P["lid_screw_z"],
                              bx1 - (P["insert_depth"] + 0.40), bx1 + 1.0))

    # -- vertical clamp insert boss, production geometry
    vx = 8.00
    body = B.uni(body, B.box(vx - 4.50, vx + 4.50, hw - 9.00, hw,
                             d["z_floor_top"], d["z_retain"]))
    body = B.sub(body, B.cylz(P["insert_hole_d"], vx, hw - 4.50,
                              d["z_ins_bot"], d["z_retain"] + 1.0))

    # -- cabinet countersink, cap recess and pry notch, production geometry
    cx = 8.00
    cy = -hw + P["cab_pad_d"] / 2.0 + 0.50
    body = B.uni(body, B.cylz(P["cab_pad_d"], cx, cy,
                              d["z_floor_top"], P["cab_pad_h"]))
    body = B.sub(body, B.cylz(P["cab_recess_d"], cx, cy,
                              d["cab_recess_z0"], P["cab_pad_h"] + 1.0))
    body = B.sub(body, B.conez(P["cab_screw_d"], d["cab_csk_d"], cx, cy,
                               d["cab_csk_z0"], d["cab_recess_z0"] + 0.001))
    body = B.sub(body, B.cylz(P["cab_screw_d"], cx, cy,
                              d["z_floor_bot"] - 1.0, d["cab_csk_z0"] + 0.001))
    body = B.sub(body, B.box(cx - P["cab_pry_w"] / 2.0,
                             cx + P["cab_pry_w"] / 2.0,
                             cy - P["cab_pad_d"] / 2.0 - 1.0,
                             cy - P["cab_recess_d"] / 2.0 + P["cab_pry_d"],
                             d["cab_recess_z0"], P["cab_pad_h"] + 1.0))
    return [(body, "ESP32_Controller_Insert_Fastener_Coupon")]


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
    """The one legend v1.2 permits: an optional recessed USB / DISCONNECT 5V
    note on the lid top, over the USB end. Cut 0.40 mm downward from the top
    face, which prints crisp because the lid goes on the bed top-face-down.

    Rev A's four legends, including the DECCA CONTROLLER banner, are gone.
    EN and BOOT are not marked because v1.2 section 6.4 forbids their access
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
                    "Carrier_Fit_Gauge",
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
    add_component(root, COUPON_A, build_coupon_a(B, P, d),
                  "PROTOTYPE TOOL. Not a production part; excluded from the "
                  "specification section 9 material gates.")
    add_component(root, COUPON_B, build_coupon_b(B, P, d),
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
    print("  v1.3 limit       %7.2f x %7.2f x %7.2f mm"
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
    print("TIE ALIGNMENT  windows %s | bundles %s | anchors %s"
          % ([round(v, 2) for v in d["win_x"]],
             [round(v, 2) for v in d["bundle_x"]],
             [round(v, 2) for v in d["tie_x"]]))
    print("  bundle-to-tie deviation %.2f mm (Rev B as published: 15.00); "
          "aperture z %.2f-%.2f, %.2f above the terminal tops, apex %.2f, "
          "tab top %.2f inside a window top of %.2f"
          % (d["tie_deviation"], d["tie_ap_z0"], d["tie_ap_z1"],
             d["tie_ap_z0"] - d["z_term_top"], d["tie_ap_apex"],
             d["tie_tab_top"], d["win_z1"]))
    print("  ANCHOR: buttressed pier %.2f wide x %.2f thick in the pull "
          "direction, %.2f mm legs, %.2f mm cap, R%.2f flank blend to a foot "
          "%.2f wider each side at the sill; unsupported height %.2f "
          "(v1.2 slab: 1.60 thick, %.2f free)"
          % (2.0 * P["tie_tab_half_w"], d["tie_thk"], d["tie_leg_w"],
             P["tie_tab_cap"], P["tie_blend_r"], d["tie_foot_dx"],
             d["tie_free_h"], d["tie_free_h_v12"]))
    print("CAP RETENTION  recess %.2f, cap body %.2f (%.2f/side slide fit), "
          "%d nibs to a %.2f crest = %.2f mm interference each; pry notch "
          "%.2f x %.2f"
          % (P["cab_recess_d"], d["cab_cap_d"], P["cab_cap_clear_r"],
             int(P["cab_nib_n"]), d["cab_nib_crest_d"], P["cab_nib_int"],
             P["cab_pry_w"], P["cab_pry_d"]))
    print("CABINET CSK   head max %.2f + 2 x %.2f clearance = %.2f dia x "
          "%.2f deep; %.2f mm of floor beneath it; head top z %.2f, cap top "
          "z %.2f, carrier underside z %.2f"
          % (P["cab_head_d_max"], P["cab_head_clear_r"], d["cab_csk_d"],
             d["cab_csk_depth"], d["cab_floor_under_csk"], d["cab_head_top"],
             P["cab_pad_h"], d["z_pcb_bot"]))
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
          % ("v1.3 section 9 limit", "", 35.0, 45.0))
    for cn in COUPONS:
        g = find_component(design, cn)
        if g:
            gv = sum(volume_of(b) for b in g.bRepBodies) / 1000.0
            print("  %-24s      %-18s %6.2f cm3  %6.1f g   (EXCLUDED, "
                  "prototype tool)" % (cn, "", gv, gv * PETG_DENSITY))

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
# validate - the specification v1.3 section 13 gate suite, run inside Fusion on
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

# Rev A features v1.2 section 2.2 deletes by name. Each is checked as an
# absent COMPONENT and, where it was geometry rather than a part, as absent
# material in the region it used to occupy.
FORBIDDEN_COMPONENTS = ("PCB_Clamp_Fixed_End", "USB_Blanking_Plug",
                        "PCB_Clamp_Fixed", "Cable_Lacing_Rail",
                        "Cabinet_Mounting_Ears")


def _buttress_env(B, P, d, pad=0.02):
    """The four cable-tie buttresses, as one solid, slightly grown.

    Gates 7 and 22 use it to say exactly what is allowed to stand outboard of
    the base wall face: these four named structures inside their own cable
    windows, and nothing else anywhere on the part."""
    env = None
    for sy in (-1.0, 1.0):
        for tx in d["tie_x"]:
            e = B.box(tx - d["tie_foot_half_w"] - pad,
                      tx + d["tie_foot_half_w"] + pad,
                      sy * (d["y_out"] - 1.00), sy * (d["tie_y1"] + pad),
                      d["z_floor_bot"] - 1.00, d["tie_tab_top"] + pad)
            env = e if env is None else B.uni(env, e)
    return env


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
    print("Decca ESP32 Controller Housing Rev B - specification v1.3 "
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
    # The cap must COVER the head, sit on a slide-fit body, and be held by
    # real interference. Rev B as published had a 10.20 cap in a 10.40 recess -
    # a 0.10 mm per-side CLEARANCE that the report called a press fit. This
    # gate now measures the nib interference itself, and fails on a clearance.
    body_fit = (P["cab_recess_d"] - d["cab_cap_d"]) / 2.0
    interference = (d["cab_nib_crest_d"] - P["cab_recess_d"]) / 2.0
    covers = d["cab_cap_d"] > d["cab_csk_d"]
    nib_printable = P["cab_nib_r"] >= 0.80          # >= 4 extrusion widths
    gate(covers and interference >= 0.08 and body_fit >= 0.10
         and int(P["cab_nib_n"]) >= 3 and nib_printable
         and P["cab_pry_w"] >= 2.00,
         "2b cap positively retained, not a clearance fit  [v1.2 gate 25]",
         "cap body %.2f in a %.2f recess = %.2f per side slide fit; %d nibs "
         "r%.2f to a %.2f crest = %+.2f mm INTERFERENCE per side; cap covers "
         "a %.2f countersink; %.2f x %.2f pry notch for removal"
         % (d["cab_cap_d"], P["cab_recess_d"], body_fit, int(P["cab_nib_n"]),
            P["cab_nib_r"], d["cab_nib_crest_d"], interference, d["cab_csk_d"],
            P["cab_pry_w"], P["cab_pry_d"]))

    # 2c the cap physically interferes with the recess bore. Proved by
    #    intersecting the cap solid with a cylinder of the recess bore: a
    #    clearance fit gives zero, an interference fit gives the nib volume.
    bore = B.cylz(P["cab_recess_d"], 0.0, 0.0, -1.0, P["cab_cap_t"] + 1.0)
    shell = B.box(-20.0, 20.0, -20.0, 20.0, -1.0, P["cab_cap_t"] + 1.0)
    B.sub(shell, bore)
    grip = _hit(B, cap, shell)
    # ANY material outside the bore is interference; a clearance fit gives
    # exactly zero. The magnitude is small by design - three r0.90 nibs
    # standing 0.12 mm proud is about 0.15 mm3 of PETG that has to deflect -
    # and the number that matters is the interference itself, gated above.
    gate(grip > 0.02,
         "2c the cap has to be pressed in and pulled out  [v1.2 gate 25]",
         "%.2f mm3 of cap stands outside the %.2f recess bore and must "
         "deflect to enter; a clearance fit would measure exactly 0.00"
         % (grip, P["cab_recess_d"]))

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
    # Two measurements, matching the offline verifier, because the cable-tie
    # anchor stands inside its window and its buttress now projects into it.
    #  (a) THE REQUIREMENT: the corridor each grouped bundle actually uses is
    #      clear for the full wire_exit_h, from the wall face outward.
    #  (b) THE FULL-WIDTH PRISM: still measured, and everything found in it
    #      must lie inside the four named anchor buttresses. A rail, an ear or
    #      any other projection anywhere in a window still fails.
    worst_c = 0.0
    nwin = 0
    for b in d["bundles"]:
        sgn = float(b["side"])
        half = b["d"] / 2.0 + 1.00
        ya, yb = sgn * d["y_out"], sgn * (d["lid_y"] + 2.0)
        corr = B.box(b["x"] - half, b["x"] + half, min(ya, yb), max(ya, yb),
                     d["win_sill"], d["win_sill"] + P["wire_exit_h"])
        worst_c = max(worst_c, _hit(B, lid, corr), _hit(B, base, corr))
    env = _buttress_env(B, P, d)
    in_win = 0.0
    unnamed = 0.0
    for sgn in (-1.0, 1.0):
        for wx in d["win_x"]:
            nwin += 1
            ya, yb = sgn * d["y_out"], sgn * (d["lid_y"] + 2.0)
            prism = B.box(wx - P["win_half_w"], wx + P["win_half_w"],
                          min(ya, yb), max(ya, yb),
                          d["win_sill"], d["win_sill"] + P["wire_exit_h"])
            got = B.inter(B.copy(base), B.copy(prism))
            in_win += max(0.0, volume_of(got))
            unnamed += max(0.0, volume_of(B.sub(got, B.copy(env))))
            worst_c = max(worst_c, _hit(B, lid, prism))
    gate(worst_c <= 0.001 and unnamed <= 0.05
         and d["win_clear_h"] >= P["wire_exit_h"],
         "7  each cable window gives >= %.2f mm of usable height"
         % P["wire_exit_h"],
         "%d windows, %.2f mm wide, sill %.2f to %.2f = %.2f mm clear; every "
         "bundle corridor clear (%.3f mm3); %.1f mm3 of anchor buttress "
         "inside the full-width prisms, %.3f mm3 of it unaccounted for"
         % (nwin, d["win_w"], d["win_sill"], d["win_z1"], d["win_clear_h"],
            worst_c, in_win, unnamed))

    # -- 8 -----------------------------------------------------------------
    bun = K["KEEPOUT_GROUPED_HARNESS_BUNDLES"]
    hb, hl = _hit(B, base, bun), _hit(B, lid, bun)
    gate(hb <= 0.001 and hl <= 0.001,
         "8  the lid does not pinch any grouped harness",
         "%d bundles, %d conductors, largest dia %.2f; base %.3f lid %.3f mm3"
         % (len(d["bundles"]), sum(b["n"] for b in d["bundles"]),
            d["bundle_d_max"], hb, hl))

    # -- 9 -----------------------------------------------------------------
    # This gate now checks the FITTED TIE, not just that an aperture exists.
    # It failed the first time it was written, which is how the published Rev B
    # anchor was found to be unusable: its aperture opened outboard into the
    # 0.25 mm lid-skirt gap and inboard into the 0.50 mm gap beside the
    # terminal blocks, so no strap could be threaded through it at all.
    tie = K["KEEPOUT_CABLE_TIES"]
    tool = K["KEEPOUT_TIE_TOOL_ACCESS"]
    ht = _hit(B, base, tie) + _hit(B, lid, tie) + _hit(B, clamp, tie)
    htool = _hit(B, base, tool) + _hit(B, lid, tool) + _hit(B, clamp, tool)
    # the loop must actually encircle its bundle, not sit beside it
    bun = K["KEEPOUT_GROUPED_HARNESS_BUNDLES"]
    wraps = _hit(B, tie, bun)
    # and it must not foul its own anchor or run outside its window
    encircles = all(b["loop_ri"] >= b["d"] / 2.0 + 1e-9 for b in d["bundles"])
    gate(ht <= 0.001 and htool <= 0.001 and wraps <= 0.001 and encircles
         and d["loop_to_tab"] > 0.0 and d["loop_in_window"] > 0.0
         and d["loop_to_sill"] > 0.0,
         "9  four FITTED cable ties: loop, route, head, tool  [v1.2 gate 23]",
         "one per window; strap %.2f x %.2f through a %.2f x %.2f aperture "
         "%.2f above the terminal tops, %.2f mm deep through the buttressed "
         "pier; loop clears its bundle by %.2f, its own anchor by %.2f and "
         "the wall top by %.2f; the strap climbs the buttress face at y %.2f "
         "and stands %.2f proud of the lid face inside the window; "
         "obstruction tie %.3f tool %.3f mm3"
         % (P["tie_w"], P["tie_t"], P["tie_ap_w"], P["tie_ap_h"],
            d["tie_ap_z0"] - d["z_term_top"], d["tie_thk"],
            P["tie_loop_clear"], d["loop_to_tab"], d["loop_to_sill"],
            d["tie_run_y0"], d["tie_run_proud"], ht, htool))

    # 9b alignment: every tie sits inside the window it serves, and the
    #    bundle-to-tie deviation is reported so it cannot drift back.
    # the FOOT, not just the pier, has to stay inside its window and clear of
    # the window's side wall by at least the lid fit clearance
    inside = all(abs(b["tie_x"] - b["win_x"]) + d["tie_foot_half_w"]
                 <= P["win_half_w"] - P["lid_fit_clear"] for b in d["bundles"])
    aligned = all(abs(b["x"] - b["win_x"]) + b["loop_ro"] <= P["win_half_w"]
                  for b in d["bundles"])
    gate(inside and aligned and d["tie_deviation"] <= 10.50,
         "9b each tie aligned with its window and bundle  [v1.2 gate 24]",
         "4 ties, 4 windows, 1:1; bundle-to-tie deviation %.2f mm, both "
         "inside a %.2f mm window (Rev B as published: 15.00 mm, and the tie "
         "was not in the window at all)"
         % (d["tie_deviation"], 2.0 * P["win_half_w"]))

    # -- 9c ----------------------------------------------------------------
    # The anchor STRUCTURE. v1.2 built it as a 1.60 mm slab standing 13.90 mm
    # above the wall top and taking its load near the tip. This gate holds the
    # section in the pull direction, the material around the aperture, the
    # blended foot and the fact that the pier fouls nothing.
    #
    # IT IS A GEOMETRIC GATE. It measures section, not strength. Nothing here
    # proves a pull force, and no pull test is claimed or implied.
    ko = 0.0
    for nm in ("KEEPOUT_PCB_ENVELOPE", "KEEPOUT_ASSEMBLY_MAX_HEIGHT",
               "KEEPOUT_NO_CONTACT_COMPONENTS",
               "KEEPOUT_TERMINAL_DRIVER_CORRIDORS",
               "KEEPOUT_GROUPED_HARNESS_BUNDLES", "KEEPOUT_CABLE_TIES",
               "KEEPOUT_TIE_TOOL_ACCESS"):
        ko += _hit(B, base, K[nm])
    hw, fw = P["tie_tab_half_w"], d["tie_foot_half_w"]
    # (a) the pier really is solid right through, at four heights and both legs
    solid = 0
    want = 0
    for tx in d["tie_x"]:
        for sy in (-1.0, 1.0):
            for zz in (d["win_sill"] + 0.50, d["tie_ap_z0"] - 0.40,
                       d["tie_ap_mid"], d["tie_ap_apex"] + 0.40,
                       d["tie_tab_top"] - 0.40):
                for xx in (tx - hw + 0.30, tx + hw - 0.30):
                    for t in (0.10, 0.50, 0.90):
                        want += 1
                        yy = d["tie_y0"] + t * d["tie_thk"]
                        if _inside(base, xx, sy * yy, zz):
                            solid += 1
    # (b) the blended foot: wider than the pier at the sill, gone by its top
    blend = 0
    for tx in d["tie_x"]:
        for sy in (-1.0, 1.0):
            for sx in (-1.0, 1.0):
                px = tx + sx * (fw - 0.30)
                py = sy * (d["tie_y0"] + d["tie_thk"] / 2.0)
                if (_inside(base, px, py, d["win_sill"] + 0.25)
                        and not _inside(base, px, py,
                                        P["tie_blend_z"] - 0.25)):
                    blend += 1
    gate(ko <= 0.001 and solid == want and blend == 8
         and d["tie_thk"] >= P["tie_thk_min"] - 1e-9
         and d["tie_leg_w"] >= P["tie_ap_wall_min"] - 1e-9
         and P["tie_tab_cap"] >= P["tie_ap_wall_min"] - 1e-9
         and d["tie_foot_to_window"] >= P["lid_fit_clear"]
         and d["tie_lid_withdraw"] >= d["hook_engage"] + 0.50
         and d["tie_to_lid"] > 0.0 and d["tie_to_win_top"] > 0.0,
         "9c anchor section, aperture walls, blended foot  [v1.3 gates 28-30]",
         "pier %.2f wide x %.2f thick in the pull direction (>= %.2f), "
         "%.2f mm of leg each side of the aperture and %.2f above its apex "
         "(>= %.2f); R%.2f flank blend %.2f tall leaves a foot %.2f wider "
         "each side at the sill, %.2f clear of the window wall; unsupported "
         "height %.2f (v1.2: %.2f); %.2f to the lid face, %.2f to the window "
         "head; keep-out intrusion %.3f mm3; %d/%d section probes solid, "
         "%d/8 blend probes; the lid can withdraw %.2f past the buttress "
         "against the %.2f the hooks need. GEOMETRY ONLY - not a strength "
         "claim."
         % (2.0 * hw, d["tie_thk"], P["tie_thk_min"], d["tie_leg_w"],
            P["tie_tab_cap"], P["tie_ap_wall_min"], P["tie_blend_r"],
            d["tie_blend_h"], d["tie_foot_dx"], d["tie_foot_to_window"],
            d["tie_free_h"], d["tie_free_h_v12"], d["tie_to_lid"],
            d["tie_to_win_top"], ko, solid, want, blend,
            d["tie_lid_withdraw"], d["hook_engage"]))

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
    # the modelled MAXIMUM head must fit inside the countersink with the
    # declared clearance still to spare, and must land below the cap
    head = K["KEEPOUT_CABINET_FASTENERS"]
    head_hit = _hit(B, base, head)
    margin = (d["cab_csk_req"] - P["cab_head_d_max"]) / 2.0
    gate(d["cab_head_top"] < d["z_pcb_bot"] and below >= P["pcb_under_clear"]
         and inside_fp and pad_clear <= 0.001 and head_hit <= 0.001
         and margin >= P["cab_head_clear_r"] - 1e-9
         and d["cab_floor_under_csk"] >= 1.00,
         "16 countersink swallows the max head envelope  [v1.2 gate 26]",
         "countersink cut %.2f dia (%.2f required + %.2f tessellation "
         "allowance) x %.2f deep for a %.2f max head = %.2f mm radial "
         "margin; %.3f mm3 of head/base interference; %.2f mm of floor "
         "left beneath; head top z %.2f under a cap topping at z %.2f, "
         "carrier underside z %.2f (%.2f clear)"
         % (d["cab_csk_d"], d["cab_csk_req"], P["cab_csk_facet"],
            d["cab_csk_depth"], P["cab_head_d_max"], margin,
            head_hit, d["cab_floor_under_csk"], d["cab_head_top"],
            P["cab_pad_h"], d["z_pcb_bot"], d["cab_head_to_pcb"]))

    # -- 17 ----------------------------------------------------------------
    # (a) seated, the lid cannot lift: the lug meets the capture ledge.
    lifted = _moved(B, lid, 0.0, 0.0, P["hook_z1"] - P["lug_z1"] + 0.30)
    captured = _hit(B, lifted, base)
    # (b) it comes off. v1.2 tilted the lid 12 degrees and shoved it 3.00 mm
    #     in -X - a number with nothing behind it. The withdrawal is now
    #     DERIVED from the hook that has to be released (hook_engage, plus a
    #     0.50 mm margin), and the test is in two stages instead of one:
    #       b1  tilt, then withdraw exactly far enough to free the lug;
    #       b2  from there, lift the lid 30 mm clear - a stage v1.2 never ran.
    #     This matters now because the cable-tie buttresses stand in the cable
    #     windows, so the lid's window side walls travel past them on the way
    #     out. That clearance is measured here and gated in 9c.
    withdraw = d["hook_engage"] + 0.50
    pivot = adsk.core.Point3D.create(mm(d["x_out_neg"]), 0.0,
                                     mm(P["lug_z1"]))
    freed = _rotated(B, lid, -12.0, v3(0, 1, 0), pivot)
    freed = _moved(B, freed, -withdraw, 0.0, 2.0)
    escape = _hit(B, freed, base)
    away = _rotated(B, lid, -12.0, v3(0, 1, 0), pivot)
    away = _moved(B, away, -withdraw, 0.0, 30.0)
    escape += _hit(B, away, base)
    screws = 2
    hooks = 2
    gate(captured > 0.001 and escape <= 0.001 and screws == 2 and hooks == 2,
         "17 two screws + two hooks give a valid assembly sequence",
         "lift %.2f mm -> %.1f mm3 of lug/ledge capture; tilt 12 deg "
         "about the hook line, withdraw %.2f mm (engagement %.2f + 0.50) and "
         "then lift 30 mm clear -> %.3f mm3 over both stages; the lid's "
         "window walls pass the cable-tie buttresses with %.2f mm to spare"
         % (P["hook_z1"] - P["lug_z1"] + 0.30, captured, withdraw,
            d["hook_engage"], escape,
            d["tie_lid_withdraw"] - withdraw))

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
    # Two geometric tests, tightened for v1.3 because the cable-tie buttresses
    # project past the base wall face into their own cable windows:
    #   (i)  NOTHING on the base stands outside the closed enclosure's own
    #        outer envelope - the lid outline. This is the real limit on an
    #        external projection and it is checked here for the first time.
    #   (ii) The only base material outboard of the base wall rectangle is the
    #        four named cable-tie buttresses. Anything else - a rail, an ear,
    #        a foot, a guide - fails, wherever it is.
    lid_env = B.rrect(d["lid_x0"] - 0.02, d["lid_x1"] + 0.02,
                      -d["lid_y"] - 0.02, d["lid_y"] + 0.02,
                      d["z_floor_bot"] - 1.0, d["z_lid_top"] + 1.0,
                      d["lid_r"] + 0.02)
    out_lid = max(0.0, volume_of(B.sub(B.copy(base), lid_env)))
    shell = B.rrect(d["x_out_neg"] - 0.02, d["x_out_pos"] + 0.02,
                    -d["y_out"] - 0.02, d["y_out"] + 0.02,
                    d["z_floor_bot"] - 1.0, d["z_lid_top"] + 1.0,
                    P["outer_corner_r"] + 0.02)
    stray = B.sub(B.copy(base), shell)
    stray_v = max(0.0, volume_of(B.copy(stray)))
    unnamed = max(0.0, volume_of(B.sub(stray, _buttress_env(B, P, d))))
    gate(not present and out_lid <= 0.05 and unnamed <= 0.05,
         "22 no forbidden Rev A feature present",
         "0 of %d deleted components; %.3f mm3 of base outside the closed "
         "enclosure envelope; %.1f mm3 outboard of the base wall, all of it "
         "in the four named cable-tie buttresses (%.3f mm3 unaccounted). No "
         "rails, ears, sawtooth roofs, plug, second clamp, corner piers or "
         "per-terminal guides."
         % (len(FORBIDDEN_COMPONENTS), out_lid, stray_v, unnamed))

    # -- 23 ----------------------------------------------------------------
    # The coupons have to test the HORIZONTAL insert, which is the one
    # fastener in this design nobody has ever driven, and they have to do it
    # on production geometry.
    ca = _one(design, COUPON_A)
    cb = _one(design, COUPON_B)
    cav = sum(volume_of(x) for x in (ca, cb) if x is not None) / 1000.0
    horiz = 0
    if cb is not None:
        bb = cb.boundingBox
        x1 = bb.maxPoint.x * 10.0
        zc = P["lid_screw_z"]
        # a clear bore of insert depth at the production axis height
        clear = all(not _inside(cb, x1 - t, 0.0, zc)
                    for t in (0.5, 2.0, 3.5, 5.0))
        horiz = 1 if clear else 0
    vert = 0
    if cb is not None:
        vert = 1 if not _inside(cb, 8.00, P["coupon2_w"] / 2.0 - 4.50,
                                d["z_retain"] - 2.0) else 0
    csk = 0
    if cb is not None:
        cy = -P["coupon2_w"] / 2.0 + P["cab_pad_d"] / 2.0 + 0.50
        csk = 1 if not _inside(cb, 8.00, cy, d["cab_recess_z0"] - 0.30) else 0
    ledge = 0
    if ca is not None:
        ledge = 1 if _inside(ca, d["x_datum"] + 0.50, 0.0,
                             d["ledge_z0"] + 1.00) else 0
    gate(ca is not None and cb is not None and horiz and vert and csk
         and ledge and cav <= 5.35,
         "23 coupons cover every untested interface  [v1.2 gate 27]",
         "A carrier %.2f cm3 + B fasteners %.2f cm3 = %.2f cm3, against the "
         "5.35 cm3 single gauge they replace; horizontal insert bore %s, "
         "vertical insert bore %s, countersink %s, fixed ledge %s"
         % (volume_of(ca) / 1000.0 if ca else -1,
            volume_of(cb) / 1000.0 if cb else -1, cav,
            "present" if horiz else "MISSING",
            "present" if vert else "MISSING",
            "present" if csk else "MISSING",
            "present" if ledge else "MISSING"))

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
    proto("EN and BOOT positions - v1.2 6.4 forbids holes until measured")
    proto("H1-H6 conductor counts and real bundle diameters")
    proto("lid_fit_clear 0.25 on this printer, filament and flow")
    proto("antenna performance with the lid fitted")
    proto("MEASURE THE ASSEMBLED STACK BEFORE PRINTING THE BASE OR LID",
          "24.00 mm assumed; the closed height is 35.30 against a 36.00 "
          "limit, so 0.70 mm is all the margin there is, and no coupon "
          "tests it")
    proto("the acquired cabinet screw's real head diameter",
          "6.20 mm max envelope declared, ISO 10642 assumed, not measured")
    proto("a horizontal heat-set insert driven into coupon B")
    proto("cap nib interference on this printer and filament",
          "0.12 mm per side is a design value, not a measured press force")
    proto("the cable-tie anchor's real handling robustness",
          "gate 9c measures section, not strength: 2.60 mm in the pull "
          "direction, 8.00 mm wide, blended into the wall on an R9.00 root "
          "radius. No pull test is claimed and none is asked for - these "
          "ties restrain lightweight low-voltage harnesses")

    print("")
    print("%d checks covering all 30 v1.3 section 13 gates, %d failed, "
          "%d prototype gates open" % (CHECKS, len(FAILS), len(BLOCKED)))
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
    (CAPS, "ESP32_Controller_Cabinet_Fastener_Cap.step"),
    (COUPON_A, "ESP32_Controller_Carrier_Fit_Coupon.step"),
    (COUPON_B, "ESP32_Controller_Insert_Fastener_Coupon.step"),
)

STL_FILES = (
    (BASE, "ESP32_Controller_Housing_Base.stl"),
    (LID, "ESP32_Controller_Housing_Lid.stl"),
    (CLAMP, "ESP32_Controller_PCB_Clamp_Adjustable.stl"),
    (CAPS, "ESP32_Controller_Cabinet_Fastener_Cap.stl"),
    (COUPON_A, "ESP32_Controller_Carrier_Fit_Coupon.stl"),
    (COUPON_B, "ESP32_Controller_Insert_Fastener_Coupon.stl"),
)

# Rev A production artefacts that would be mistaken for current deliverables.
# v1.2 section 12: do not ship a fixed-clamp STL or a USB-plug STL.
OBSOLETE = (
    # Rev A
    ("STL", "ESP32_Controller_PCB_Clamp_Fixed.stl"),
    ("STL", "ESP32_Controller_USB_Plug.stl"),
    ("CAD", "ESP32_Controller_PCB_Clamps.step"),
    # superseded Rev B: the one near-full-width gauge, replaced by two coupons
    ("STL", "ESP32_Controller_Carrier_Fit_Gauge.stl"),
    ("CAD", "ESP32_Controller_Carrier_Fit_Gauge.step"),
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
# images - the review evidence v1.2 section 12 requires.
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

# Renders from an earlier Rev B run whose subject no longer exists. Left
# on disk they would read as current review evidence.
SUPERSEDED_IMAGES = (
    "Decca_ESP32_Controller_Housing_revB_15_fit_gauge.png",
    # first cut of the v1.3 anchor close-up, replaced by 09d + 09e
    "Decca_ESP32_Controller_Housing_revB_09e_anchor_detail_outboard.png",
)


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

    # 9 internal strain relief: all four ties CLOSED on their bundles
    shot("09_strain_relief",
         {BASE: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_CABLE_TIES",
                     "KEEPOUT_GROUPED_HARNESS_BUNDLES"}}, "iso")

    # 9b each harness from its terminals, through its aligned tie, to its
    #    own window - the alignment the review asked for, in one picture
    shot("09b_tie_alignment",
         {BASE: True, LID: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_CABLE_TIES",
                     "KEEPOUT_GROUPED_HARNESS_BUNDLES"}}, "top")

    # 9c locking heads and the tightening pull, from inboard
    shot("09c_tie_heads_and_tool",
         {BASE: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_CABLE_TIES", "KEEPOUT_TIE_TOOL_ACCESS",
                     "KEEPOUT_GROUPED_HARNESS_BUNDLES"}}, "iso_left")

    # 9d THE REVISED ANCHOR, close up, with its tie fitted and NO tool volume
    #    in the way: pier, outboard buttress, R blend into the wall top,
    #    aperture, peaked roof and cap, all in one uncluttered picture
    tx0 = d["tie_x"][0]
    win = B.box(tx0 - 8.0, tx0 + 16.0, -d["lid_y"] - 5.0, -d["y_cav"] + 3.0,
                d["z_floor_bot"] - 1.0, d["tie_tab_top"] + 5.0)
    bare = []
    for bb in find_component(design, BASE).bRepBodies:
        bare.append((bb, 0.0, 0.0, 0.0, win, bb.name))
    _temp_component(design, "ANCHOR_DETAIL", bare)
    dress(design, app, ("ANCHOR_DETAIL",))
    shot("09d_anchor_detail", {"ANCHOR_DETAIL": True}, "iso")
    clear_component(design, "ANCHOR_DETAIL")
    # 9e the same anchor with its tie fitted, in elevation: strap through the
    #    aperture, loop closed on the bundle, locking head. Still no tool
    #    volume - nothing orange in either picture is a clearance block.
    fitted = list(bare)
    for bb in find_component(design, REF_KEEP).bRepBodies:
        if bb.name in ("KEEPOUT_CABLE_TIES",
                       "KEEPOUT_GROUPED_HARNESS_BUNDLES"):
            fitted.append((bb, 0.0, 0.0, 0.0, win, bb.name))
    _temp_component(design, "ANCHOR_DETAIL", fitted)
    dress(design, app, ("ANCHOR_DETAIL",))
    shot("09e_anchor_and_tie", {"ANCHOR_DETAIL": True}, "front")
    clear_component(design, "ANCHOR_DETAIL")

    # 10 USB service access
    shot("10_usb_access",
         {BASE: True, LID: True, REF_ESP: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_USB_SERVICE_ENVELOPE"}}, "iso_left")

    # 11 the two recessed cabinet fixings, from below and from inside
    shot("11_cabinet_fixings",
         {BASE: True, CAPS: True,
          REF_KEEP: {"KEEPOUT_CABINET_FASTENERS",
                     "KEEPOUT_UNDERSIDE_JOINTS"}}, "iso_bottom")

    # 11b screw, countersink, retained cap and carrier clearance, in section
    cut = B.box(P["cab_x"] - 12.0, P["cab_x"] + 12.0,
                -d["lid_y"] - 5.0, 0.0, d["z_floor_bot"] - 3.0, d["z_pcb_top"] + 3.0)
    parts = []
    for nm in (BASE, CAPS, REF_ADP):
        for bb in find_component(design, nm).bRepBodies:
            parts.append((bb, 0.0, 0.0, 0.0, cut, bb.name))
    for bb in find_component(design, REF_KEEP).bRepBodies:
        if bb.name == "KEEPOUT_CABINET_FASTENERS":
            parts.append((bb, 0.0, 0.0, 0.0, cut, bb.name))
    _temp_component(design, "CAB_SECTION", parts)
    dress(design, app, ("CAB_SECTION",))
    shot("11b_cabinet_fixing_section", {"CAB_SECTION": True}, "back")
    clear_component(design, "CAB_SECTION")

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

    # 15 the two prototype coupons
    shot("15_coupon_a_carrier", {COUPON_A: True}, "iso")
    shot("16_coupon_b_inserts", {COUPON_B: True}, "iso")

    # 17 both insert test features together, with the metal that goes in them
    shot("17_insert_test_features",
         {BASE: True, REF_KEEP: {"KEEPOUT_LID_AND_CLAMP_FASTENERS"}}, "iso")

    # retire the Rev A renders - v1.2 section 12
    removed = []
    for f in sorted(os.listdir(out_dir)):
        if f.startswith(OLD_IMAGES) or f in SUPERSEDED_IMAGES:
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
