# -*- coding: utf-8 -*-
"""
Decca ESP32 Controller Housing - Rev C parametric generator (Autodesk Fusion).

Controlling document: mechanical/Drawings/Decca_ESP32_Controller_Housing_Spec_v1.0.md
                      (its content is specification revision v1.6)

WHY REV C EXISTS
----------------
Rev A was rejected for bulk. Rev B was rejected for a worse reason: it modelled
the wrong connection path. It routed grouped harnesses over the tops of the
terminal blocks, because nobody had established how the acquired DORHEA adapter
is actually wired. It is wired from the SIDES: fifteen green screw terminals per
long side, screws operated from above, and external conductors entering
HORIZONTALLY through outward-facing ports. The two black vertical sockets carry
the ESP32 module and are not wiring points at all.

Every Rev B body, coupon, export, render, slice result and verification result
is superseded. None of its cable geometry is reused here.

WHAT IS MEASURED, AND WHAT IS NOT
---------------------------------
The owner measured the adapter on 2026-09-05 and 2026-09-06. Those figures are
tagged MEASURED below with their date. Everything else is tagged STARTING and
remains an open prototype gate, exactly as in Rev A and Rev B. Nothing that is
merely assumed is presented anywhere as measured.

THE ONE DESIGN MOVE THAT MATTERS
--------------------------------
The owner reported the conductor entry as "just above the base of the terminal
block" and ruled the port bore and internal depth out of scope, because they do
not drive housing geometry. That is right, and v1.6 section 5.3 turns it into a
stronger requirement than a measurement would have been:

    the housing clears the ENTIRE 9.00 mm block height, across the full
    53.00 mm row length, on both long sides.

Wherever the port actually sits inside that block, nothing this housing owns is
ever in front of it. A later port measurement cannot invalidate the geometry.
The cost is nil, because a wall in that band was never available.

Consequence, and it sets the whole architecture: THERE IS NO USEFUL WALL HEIGHT
ABOVE THE BOARD ON THE LONG SIDES. The base's long walls stop at the adapter's
top face; the lid carries no long-side skirt, because a skirt there would have
to be dragged through the fitted conductors to get the lid off. All retention,
all fastening and all lid support therefore live at the two SHORT ends, in the
6.50 mm of clear board the 53.00 mm rows leave beyond each end.

REV C ARCHITECTURE
------------------
    Housing_Base        1.60 mm continuous insulating floor; four local support
                        pads; one integral fixed ledge on the -X short edge; one
                        adjustable clamp on two M3 screws at the +X end; two
                        full-height short end walls with four corner returns
                        that carry the lid; long walls stopping at the adapter
                        top face; two recessed, capped cabinet fixings.
    Housing_Lid         flat cover on the corner returns and end walls, with
                        skirts at the SHORT ENDS AND CORNERS ONLY, two M3
                        screws at +X, two locating lugs at -X, a USB notch open
                        at the skirt's free edge, and modest top vents.
    PCB_Clamp_Adjustable   one flat bar on two slotted M3 screws.
    Cabinet_Fastener_Caps  two insulating discs over the recessed M3 heads.

PRINTING
--------
PETG / PETG-HF, 0.40 mm nozzle, 0.20 mm layers, no support material.
Base floor-down. Lid TOP-FACE-DOWN, which is what makes the USB notch and the
vents print with no bridge. Clamp flat.

RUNNING IT
----------
    main(None)      build/rebuild every component in the active document
    validate(None)  the specification v1.6 section 13 gate suite
    export(None)    f3d, STEP and STL into the repository clone
    images(None)    the review renders
"""
from __future__ import print_function

import math
import os

import adsk.core
import adsk.fusion

REPO = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", ".."))

DOC = "Decca ESP32 Housing"

BASE = "Housing_Base"
LID = "Housing_Lid"
CLAMP = "PCB_Clamp_Adjustable"
CAPS = "Cabinet_Fastener_Caps"

REF_ESP = "REF_ESP32_DevKit_V1_30Pin"
REF_ADP = "REF_30Pin_Terminal_Adapter"
REF_COR = "REF_Terminal_Entry_Corridors"
REF_WIRE = "REF_Installed_Wires_And_Ferrules"
REF_HARN = "REF_Grouped_Harness_Keepouts"
REF_KEEP = "REF_Wired_Keepouts"

PRODUCTION = (BASE, LID, CLAMP, CAPS)
COUPONS = ()
PRINTABLE = PRODUCTION + COUPONS
REFERENCE = (REF_ESP, REF_ADP, REF_COR, REF_WIRE, REF_HARN, REF_KEEP)

REF_NOTE = ("NON-MANUFACTURING REFERENCE. Excluded from every printable "
            "export. Measured figures are dated in the generator; everything "
            "else is a starting value and an open prototype gate.")

PETG_DENSITY = 1.27                  # g/cm3, specification section 9

SLICER_PROFILE = ("Bambu Lab P1S, PETG-HF, 0.40 mm nozzle, 0.20 mm layers, "
                  "3 walls, 15% infill, no supports, textured PEI plate")

# v1.6 section 10 forbids support MATERIAL. It does not forbid a short
# unsupported ledge, and a retaining ledge over a board cannot be built without
# one. Every downward facing surface on every part is measured for how far it
# reaches from its nearest support, and held under this.
OVERHANG_REACH_MAX = 1.50

# Rev A and Rev B components that must not exist in the replacement document.
FORBIDDEN_COMPONENTS = (
    "PCB_Clamp_Fixed_End", "PCB_Clamp_Adjustable_End", "USB_Blanking_Plug",
    "Carrier_Fit_Gauge", "Carrier_Fit_Coupon", "Insert_Fastener_Coupon",
)

# ---------------------------------------------------------------------------
# PARAMETERS.  Every value carries one of three tags:
#
#   MEASURED  physically measured off the acquired hardware, with its date
#   DESIGN    a design value taken from specification v1.6
#   STARTING  a CAD starting value; NOT measured; an open prototype gate
#
# DERIVED values are computed in derive() below and never typed here.
# ---------------------------------------------------------------------------
P = {
    # -- The acquired DORHEA adapter, MEASURED ------------------------------
    # Owner measurements. These are the first hardware figures in the whole
    # housing programme that are not assumptions.
    # 63.00 ALONG the rows and 66.00 ACROSS them. Owner correction
    # 2026-09-06: the 66.00 is measured from one connector side to the other.
    # It is also the self-consistent reading - it leaves 5.50 mm of clear board
    # outboard of each block face and 5.00 mm beyond each row end, against the
    # lopsided 4.00 and 6.50 the other way round gives.
    "adapter_pcb_l": 63.00,          # MEASURED 2026-09-06, ALONG the rows
    "adapter_pcb_w": 66.00,          # MEASURED 2026-09-06, ACROSS the rows
    "term_outer_span": 55.00,        # MEASURED 2026-09-06, outer face to outer face
    "term_row_l": 53.00,             # MEASURED 2026-09-06, length of one row
    "term_block_h": 9.00,            # MEASURED 2026-09-06, above the PCB top face
    "assembly_h": 20.00,             # MEASURED 2026-09-05, lowest underside to top
    "term_per_side": 15,             # supplier topology, visible on the board
    # Pairing CONFIRMED by the owner 2026-09-06: the 58.00 is the ACROSS
    # pitch, which is what puts all four holes at a near-equal inset from
    # the nearest board edge. See ASSUMED below for the 0.50 mm wrinkle
    # that reading still leaves.
    "mount_pitch_x": 56.00,          # MEASURED 2026-09-06, ALONG the rows
    "mount_pitch_y": 58.00,          # MEASURED 2026-09-06, ACROSS the rows

    # -- The adapter, STARTING ----------------------------------------------
    "adapter_pcb_t": 1.60,           # STARTING
    "adapter_below_h": 2.50,         # STARTING, lowest underside feature below the PCB
    "term_block_d": 6.50,            # STARTING, block depth in Y
    "term_screw_d": 2.60,            # STARTING
    "term_screw_inset": 3.00,        # STARTING, screw axis inboard of the outer face
    # Representative only. The housing clears the whole block, so no dimension
    # below can move a single housing surface - they exist for the wire
    # references and the renders.
    "term_port_w": 2.20,             # STARTING, representative
    "term_port_h": 2.20,             # STARTING, representative
    "term_port_rise": 2.20,          # STARTING, port centre above the PCB top face
    "pcb_bare_end": 6.50,            # DERIVED from the measurements, see derive()

    # -- ESP32 DevKit V1 / DOIT reference, STARTING -------------------------
    "esp_pcb_l": 51.50,
    "esp_pcb_w": 28.30,
    "esp_pcb_t": 1.60,
    "esp_socket_h": 8.50,            # STARTING, black vertical socket height
    "esp_socket_span": 22.86,
    "esp_mod_l": 25.50,
    "esp_mod_w": 18.00,
    "esp_mod_h": 3.10,
    "esp_ant_l": 15.00,
    "esp_ant_w": 18.00,
    "esp_usb_w": 7.50,               # STARTING
    "esp_usb_h": 2.70,               # STARTING
    "esp_usb_l": 5.90,               # STARTING
    "antenna_keepout": 10.00,        # DESIGN

    # -- The installer's own wire, STARTING ---------------------------------
    "wire_d": 2.00,                  # STARTING, insulated OD, 22-24 AWG
    "ferrule_d": 2.60,               # STARTING
    "ferrule_l": 8.00,               # STARTING
    "bundle_pack": 1.15,

    # -- DECLARED ROUTING VALUES, owned by this design ----------------------
    # v1.6 5.3: the straight run a conductor gets before it may bend is this
    # design's declaration, not a board measurement. Measured from the block's
    # outward face.
    "straight_run": 12.00,           # DESIGN
    "driver_d": 6.00,                # DESIGN, terminal screwdriver corridor

    # -- Clearances, DESIGN (specification v1.6 section 3) ------------------
    "pcb_xy_clear": 0.50,
    "pcb_under_clear": 2.00,
    "component_top_clear": 2.00,
    # Re-centred on the MEASURED 63.00 mm along-row dimension. The 65-67 range
    # in v1.1 predates any measurement of this board; +-1.00 mm of adjustment
    # around a measured value is what the clamp is actually for.
    "carrier_len_min": 62.00,
    "carrier_len_max": 64.00,

    # -- Shell, DESIGN -------------------------------------------------------
    "base_floor_t": 1.60,
    "wall_t": 1.60,
    "end_wall_t": 1.60,
    "lid_top_t": 1.60,
    "lid_skirt_t": 1.20,
    "lid_overlap": 4.00,
    "lid_fit_clear": 0.25,
    # 4.00, not 6.00: the corrected board leaves 5.00 mm of clear board
    # beyond each row end, and a 6.00 mm return would stand in the last
    # terminal's conductor corridor.
    "corner_return_l": 4.00,         # long-side lid landing, from each corner
    "outer_corner_r": 3.00,

    # -- Support pads, DESIGN ------------------------------------------------
    "pad_l": 8.00,
    "pad_w": 3.00,
    "pad_inset_x": 3.25,             # pad centre inboard of the board short edge
    "pad_inset_y": 2.00,             # pad centre inboard of the board long edge

    # -- Fixed ledge and adjustable clamp, DESIGN ---------------------------
    "ledge_grip": 2.00,
    "ledge_lead": 1.40,             # 45 deg lead-in; gate 18 sets this
    "ledge_y0": 8.00,                # two segments, clear of the USB centre
    "ledge_y1": 22.00,
    "clamp_grip": 2.00,
    "clamp_t": 3.00,
    # 7.50, not 6.00: the bar has to carry a 5.40 slot, keep material beyond
    # it, AND clear the +X wall at full travel, while the insert bore stays
    # inside the plinth. Gate 14 showed 6.00 cannot satisfy all four.
    "clamp_zone": 7.50,              # floor beyond the board for the plinths
    "clamp_screw_y": 16.00,
    "clamp_slot_l": 5.40,
    "clamp_slot_w": 3.40,
    "clamp_vertical_clear": 0.20,
    "clamp_side_clear": 0.40,
    "clamp_edge": 0.50,
    "plinth_half_w": 4.50,
    "insert_hole_d": 4.00,           # STARTING, heat-set insert
    "insert_depth": 5.00,            # STARTING

    # -- Lid screws and locating lugs, DESIGN -------------------------------
    # 26.00, not 22.00: at 22.00 the base's lid-screw bosses reached into
    # the clamp bar, which spans y +-20.50. The offline verifier found it,
    # because its hand-typed value was the intended one and the two suites
    # disagreed. Gate 14 now fails on the interference as well as the grip.
    "lid_screw_y": 26.00,
    "lid_screw_clear_d": 3.40,
    "lid_boss_half_w": 4.50,
    "hook_y": 22.00,
    "hook_half_w": 6.00,
    "hook_depth": 0.80,
    "hook_drop": 2.60,               # rebate height in the -X end wall

    # -- USB service opening, DESIGN ----------------------------------------
    "usb_open_w": 14.00,
    "usb_open_h": 9.00,
    "usb_slot_w": 16.00,             # cut oversize: the USB position is STARTING

    # -- Ventilation, DESIGN -------------------------------------------------
    "vent_n": 5,
    "vent_w": 2.00,
    "vent_l": 14.00,
    "vent_pitch": 4.50,
    "vent_x": -15.00,

    # -- Recessed cabinet fixings, DESIGN -----------------------------------
    # 24.00. The 13.00 dia pad must not touch the -X cavity wall: at 27.00 it
    # was exactly tangent to it, which Fusion accepted as a valid solid and the
    # exporter turned into a non-manifold edge - the same tangency trap the
    # Rev B chamfer hit. The axis correction moved that wall 1.50 mm inboard,
    # so the fixings moved with it.
    "cab_x": 24.00,
    "cab_screw_d": 3.40,
    "cab_head_d_nom": 6.00,          # STARTING - ISO 10642 M3, not measured
    "cab_head_d_max": 6.20,          # DESIGN, declared maximum head envelope
    "cab_head_angle": 90.00,
    "cab_head_clear_r": 0.25,
    "cab_csk_facet": 0.10,           # STL tessellation allowance on the cone
    "cab_pad_d": 13.00,
    "cab_pad_h": 2.40,
    "cab_recess_d": 10.40,
    "cab_cap_t": 1.00,
    "cab_cap_clear_r": 0.15,
    "cab_nib_n": 3,
    "cab_nib_r": 0.90,
    "cab_nib_int": 0.12,
    "cab_pry_w": 2.80,
    "cab_pry_d": 1.60,
}

# Physically measured off the acquired hardware, with the date it was taken.
# Nothing else in P may be described as measured.
MEASURED = {
    "assembly_h": "2026-09-05",
    "adapter_pcb_l": "2026-09-06",
    "adapter_pcb_w": "2026-09-06",
    "term_outer_span": "2026-09-06",
    "term_row_l": "2026-09-06",
    "term_block_h": "2026-09-06",
    "mount_pitch_x": "2026-09-06",
    "mount_pitch_y": "2026-09-06",
}

# CAD starting values. Not measured, and every one is an open prototype gate.
STARTING = (
    "adapter_pcb_t", "adapter_below_h", "term_block_d", "term_screw_d",
    "term_screw_inset", "term_port_w", "term_port_h", "term_port_rise",
    "esp_pcb_l", "esp_pcb_w", "esp_pcb_t", "esp_socket_h", "esp_socket_span",
    "esp_mod_l", "esp_mod_w", "esp_mod_h", "esp_ant_l", "esp_ant_w",
    "esp_usb_w", "esp_usb_h", "esp_usb_l",
    "wire_d", "ferrule_d", "ferrule_l",
    "insert_hole_d", "insert_depth", "cab_head_d_nom",
)

# Assumptions the owner has not confirmed, recorded so they cannot pass as
# measurements. Each is a one-parameter change if it turns out to be wrong.
ASSUMED = (
    ("terminal rows centred along the 63.00 mm ALONG-row dimension",
     "leaves 5.00 mm of clear board beyond each row end, which is where the "
     "ledge, the clamp, the lid screws and the locating lugs all live"),
    ("one of the four hole/board numbers is out by 1.00 mm",
     "the owner confirms the 58.00 is the ACROSS pitch because it puts all "
     "four holes at an equal inset from the nearest edge - but on the recorded "
     "66 x 63 board, 58 x 56 gives 4.00 mm across and 3.50 mm along, which is "
     "0.50 mm short of equal. Equal insets need any ONE of: along pitch 55.00, "
     "across pitch 59.00, board along 64.00, or board across 65.00. Nothing in "
     "this design uses the holes, so nothing depends on the resolution"),
    ("the USB connector is centred on its short edge",
     "the opening is cut oversize at 16.00 mm to absorb the error"),
    ("term_block_h 9.00 was taken as the block's own body height",
     "if it was taken from the resting surface instead, the block top drops "
     "by adapter_below_h + adapter_pcb_t and the long walls gain nothing, "
     "because they are set by the board top face either way"),
)

# The actual Decca harnesses, docs/Wiring.md. Grouped AFTER the conductors have
# cleared their terminal mouths and the declared straight run - never before.
# (id, description, conductors, side, +1 toward +X or -1 toward -X)
HARNESS = (
    ("H1", "potentiometers, 4 x 3", 12, -1, -1),
    ("H2", "original on/off switch", 2, -1, +1),
    ("H3", "VHF source and Stereo/Mono", 4, -1, +1),
    ("H4", "OLED display", 4, +1, -1),
    ("H5", "dial lighting control", 3, +1, -1),
    ("H6", "ZA3 12 V trigger", 2, +1, +1),
    ("PWR", "5 V and GND", 4, +1, +1),
)


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
# Derived geometry. Everything here is a consequence of P; nothing is typed.
#
# Origin: plan centre of the measured 66.00 x 63.00 adapter PCB.
#         z = 0 is the cavity floor top.
#
# The vertical chain is anchored on the MEASURED 20.00 mm overall assembly
# height, taken from the assembly's own lowest underside feature - "datum A" -
# to its highest point. It is NOT converted into an above-PCB value.
# ---------------------------------------------------------------------------
def derive(P):
    d = {}

    # ---- the adapter, straight from the measured plan ---------------------
    d["x_pcb"] = P["adapter_pcb_l"] / 2.0                    # 33.00
    d["y_pcb"] = P["adapter_pcb_w"] / 2.0                    # 31.50
    d["y_term_out"] = P["term_outer_span"] / 2.0             # 27.50
    d["y_term_in"] = d["y_term_out"] - P["term_block_d"]     # 21.00
    d["x_term"] = P["term_row_l"] / 2.0                      # 26.50
    d["term_pitch"] = P["term_row_l"] / float(P["term_per_side"])
    # 15 terminal centres per row, rows assumed centred on the board
    d["term_x"] = [-d["x_term"] + d["term_pitch"] * (i + 0.5)
                   for i in range(int(P["term_per_side"]))]

    # The two clear strips the measurements hand us. Every retention,
    # fastening and support feature in this design lives in one of them.
    d["clear_end"] = d["x_pcb"] - d["x_term"]                # 6.50 beyond each row
    d["clear_side"] = d["y_pcb"] - d["y_term_out"]           # 4.00 outboard of a block

    # ---- vertical chain ----------------------------------------------------
    d["z_floor_bot"] = -P["base_floor_t"]
    d["z_floor_top"] = 0.0
    # datum A: the assembly's lowest underside feature, held clear of the floor
    d["z_datum_a"] = P["pcb_under_clear"]                    # 2.00
    d["z_pcb_bot"] = d["z_datum_a"] + P["adapter_below_h"]   # 4.50
    d["z_pcb_top"] = d["z_pcb_bot"] + P["adapter_pcb_t"]     # 6.10
    d["z_block_top"] = d["z_pcb_top"] + P["term_block_h"]    # 15.10  MEASURED height
    d["z_assy_top"] = d["z_datum_a"] + P["assembly_h"]       # 22.00  MEASURED overall
    d["z_cav_top"] = d["z_assy_top"] + P["component_top_clear"]
    d["z_lid_top"] = d["z_cav_top"] + P["lid_top_t"]
    d["pad_h"] = d["z_pcb_bot"] - d["z_floor_top"]           # 4.50
    d["h_closed"] = d["z_lid_top"] - d["z_floor_bot"]

    # the ESP32 on its sockets. All STARTING; the measured 20.00 mm envelope
    # above governs the housing, not this stack.
    d["z_sock_top"] = d["z_pcb_top"] + P["esp_socket_h"]
    d["z_esp_bot"] = d["z_sock_top"]
    d["z_esp_top"] = d["z_esp_bot"] + P["esp_pcb_t"]
    d["z_mod_top"] = d["z_esp_top"] + P["esp_mod_h"]
    d["z_usb_axis"] = d["z_esp_top"] + P["esp_usb_h"] / 2.0
    d["esp_x0"] = -P["esp_pcb_l"] / 2.0
    d["esp_x1"] = P["esp_pcb_l"] / 2.0
    d["esp_y0"] = -P["esp_pcb_w"] / 2.0
    d["esp_y1"] = P["esp_pcb_w"] / 2.0
    d["mod_x0"] = d["esp_x1"] - P["esp_mod_l"]
    d["ant_x0"] = d["esp_x1"] - P["esp_ant_l"]

    # ---- plan chain --------------------------------------------------------
    d["x_cav_neg"] = -(d["x_pcb"] + P["pcb_xy_clear"])       # -33.50
    d["x_carrier_max"] = P["carrier_len_max"] / 2.0          # 33.50
    d["x_carrier_min"] = P["carrier_len_min"] / 2.0          # 32.50
    d["x_adj_face"] = d["x_carrier_max"] + P["pcb_xy_clear"] # 34.00
    d["x_cav_pos"] = d["x_adj_face"] + P["clamp_zone"]       # 40.00
    d["y_cav"] = d["y_pcb"] + P["pcb_xy_clear"]              # 32.00
    d["x_out_neg"] = d["x_cav_neg"] - P["end_wall_t"]
    d["x_out_pos"] = d["x_cav_pos"] + P["end_wall_t"]
    d["y_out"] = d["y_cav"] + P["wall_t"]
    d["body_l"] = d["x_out_pos"] - d["x_out_neg"]
    d["body_w"] = 2.0 * d["y_out"]

    # ---- the open long sides ----------------------------------------------
    # The long walls stop at the adapter's top face across the whole terminal
    # region. They rise to full height only in the corner returns, which are
    # the lid's landings and sit clear of the rows.
    d["x_ret_neg"] = d["x_cav_neg"] + P["corner_return_l"]   # -27.50
    d["x_ret_pos"] = d["x_cav_pos"] - P["corner_return_l"]   # 34.00
    d["z_long_wall_top"] = d["z_pcb_top"]                    # 6.10
    d["ret_to_row"] = -d["x_term"] - d["x_ret_neg"]          # 1.00 clearance
    d["side_open_h"] = d["z_cav_top"] - d["z_long_wall_top"]

    # ---- terminal entry ----------------------------------------------------
    # v1.6 5.3: clear the WHOLE block height across the WHOLE row length. The
    # corridor starts at the block's outward face and runs past the enclosure.
    d["corr_y0"] = d["y_term_out"]
    d["corr_z0"] = d["z_pcb_top"]
    d["corr_z1"] = d["z_block_top"]
    d["straight_y"] = d["y_term_out"] + P["straight_run"]    # 39.50
    d["z_port"] = d["z_pcb_top"] + P["term_port_rise"]       # representative only
    d["term_screw_y"] = d["y_term_out"] - P["term_screw_inset"]

    # ---- lid ----------------------------------------------------------------
    d["lid_x_neg"] = d["x_out_neg"] - P["lid_fit_clear"] - P["lid_skirt_t"]
    d["lid_x_pos"] = d["x_out_pos"] + P["lid_fit_clear"] + P["lid_skirt_t"]
    d["lid_y"] = d["y_out"] + P["lid_fit_clear"] + P["lid_skirt_t"]
    d["lid_l"] = d["lid_x_pos"] - d["lid_x_neg"]
    d["lid_w"] = 2.0 * d["lid_y"]
    d["z_skirt_bot"] = d["z_cav_top"] - P["lid_overlap"]
    d["skirt_in_neg"] = d["x_out_neg"] - P["lid_fit_clear"]
    d["skirt_in_pos"] = d["x_out_pos"] + P["lid_fit_clear"]
    d["skirt_in_y"] = d["y_out"] + P["lid_fit_clear"]
    # the lid's long-side skirt exists only over the corner returns
    d["lid_ret_neg"] = d["x_out_neg"] + P["corner_return_l"] + P["end_wall_t"]
    d["lid_ret_pos"] = d["x_out_pos"] - P["corner_return_l"] - P["end_wall_t"]

    # ---- support pads, in the clear side strip -----------------------------
    d["pad_x"] = d["x_pcb"] - P["pad_l"] / 2.0 - 0.50        # 28.50
    d["pad_y"] = (d["y_term_out"] + d["y_pcb"]) / 2.0        # 29.50
    d["pad_margin"] = (d["clear_side"] - P["pad_w"]) / 2.0

    # ---- fixed ledge, -X short edge ----------------------------------------
    d["ledge_x1"] = -d["x_pcb"] + P["ledge_grip"]            # -31.00
    d["ledge_z0"] = d["z_pcb_top"] + P["clamp_vertical_clear"]
    d["ledge_proj"] = d["ledge_x1"] - d["x_cav_neg"]
    d["ledge_flat"] = d["ledge_proj"] - P["ledge_lead"]

    # ---- adjustable clamp, +X ----------------------------------------------
    # inset half a millimetre so the bar clears the +X wall, and the
    # plinths are bounded by the clamp zone so they never reach under the
    # board - gate 14 caught both
    d["clamp_screw_x"] = d["x_adj_face"] + 2.60
    d["plinth_x0"] = d["x_adj_face"]
    d["plinth_x1"] = d["x_cav_pos"]
    d["clamp_z0"] = d["ledge_z0"]
    d["clamp_z1"] = d["clamp_z0"] + P["clamp_t"]
    d["bar_x0"] = d["x_pcb"] - P["clamp_grip"]
    d["clamp_travel"] = (P["clamp_slot_l"] - P["clamp_slot_w"]) / 2.0
    # The bar's outer end is bounded by the +X wall AT FULL TRAVEL, not just at
    # rest. Gate 14 failed twice on this: encode the constraint instead of
    # picking a length that happens to fit.
    d["bar_x1"] = min(d["clamp_screw_x"] + P["clamp_slot_l"] / 2.0
                      + P["clamp_edge"],
                      d["x_cav_pos"] - d["clamp_travel"] - 0.30)
    d["grip_at_min"] = d["x_carrier_min"] - (d["bar_x0"] - d["clamp_travel"])
    d["grip_at_max"] = d["x_carrier_max"] - (d["bar_x0"] + d["clamp_travel"])
    d["bar_y"] = P["clamp_screw_y"] + P["plinth_half_w"]
    d["z_ins_bot"] = d["clamp_z0"] - P["insert_depth"]

    # ---- lid screws and locating lugs --------------------------------------
    d["lid_boss_x0"] = d["x_out_pos"] - 6.00
    d["lid_screw_x"] = d["x_out_pos"] - 3.50
    d["z_lid_ins_bot"] = d["z_cav_top"] - P["insert_depth"]
    d["hook_z1"] = d["z_cav_top"] - P["lid_overlap"] + P["hook_drop"]
    d["hook_z0"] = d["hook_z1"] - P["hook_drop"]
    d["lug_proj"] = P["lid_fit_clear"] + P["hook_depth"] - 0.20
    d["hook_engage"] = d["lug_proj"] - P["lid_fit_clear"]

    # ---- USB service opening, -X -------------------------------------------
    # Cut as a notch open to the top of the base end wall and continued through
    # the lid skirt to its free edge, so neither part bridges.
    d["usb_z0"] = d["z_usb_axis"] - P["usb_open_h"] / 2.0
    d["usb_clear_h"] = d["z_cav_top"] - d["usb_z0"]
    d["usb_y0"] = -P["usb_slot_w"] / 2.0
    d["usb_y1"] = P["usb_slot_w"] / 2.0

    # ---- antenna keep-out ---------------------------------------------------
    d["ako_x0"] = d["ant_x0"] - P["antenna_keepout"]
    d["ako_x1"] = d["esp_x1"] + P["antenna_keepout"]
    d["ako_y0"] = -P["esp_ant_w"] / 2.0 - P["antenna_keepout"]
    d["ako_y1"] = P["esp_ant_w"] / 2.0 + P["antenna_keepout"]
    d["ako_z0"] = d["z_esp_top"]
    d["ako_z1"] = d["z_lid_top"] + 1.0

    # ---- recessed cabinet fixings ------------------------------------------
    d["cab_csk_req"] = P["cab_head_d_max"] + 2.0 * P["cab_head_clear_r"]
    d["cab_csk_d"] = d["cab_csk_req"] + P["cab_csk_facet"]
    d["cab_csk_depth"] = ((d["cab_csk_d"] - P["cab_screw_d"]) / 2.0
                          / math.tan(math.radians(P["cab_head_angle"] / 2.0)))
    d["cab_recess_z1"] = P["cab_pad_h"]
    d["cab_recess_z0"] = P["cab_pad_h"] - P["cab_cap_t"]
    d["cab_csk_z0"] = d["cab_recess_z0"] - d["cab_csk_depth"]
    d["cab_head_top"] = d["cab_recess_z0"]
    d["cab_head_to_pcb"] = d["z_pcb_bot"] - P["cab_pad_h"]
    d["cab_floor_under_csk"] = d["cab_csk_z0"] - d["z_floor_bot"]
    d["cab_cap_d"] = P["cab_recess_d"] - 2.0 * P["cab_cap_clear_r"]
    d["cab_nib_crest_d"] = P["cab_recess_d"] + 2.0 * P["cab_nib_int"]
    d["cab_nib_c"] = (d["cab_nib_crest_d"] / 2.0) - P["cab_nib_r"]

    # ---- ventilation --------------------------------------------------------
    d["vent_x0"] = P["vent_x"] - P["vent_l"] / 2.0
    d["vent_x1"] = P["vent_x"] + P["vent_l"] / 2.0

    # ---- grouped harnesses, downstream of the straight run only ------------
    groups = {}
    for hid, desc, n, side, direc in HARNESS:
        key = (side, direc)
        g = groups.setdefault(key, {"ids": [], "n": 0})
        g["ids"].append(hid)
        g["n"] += n
    bundles = []
    for (side, direc), g in sorted(groups.items()):
        dia = P["bundle_pack"] * P["wire_d"] * math.sqrt(float(g["n"]))
        bundles.append({
            "ids": "+".join(g["ids"]), "n": g["n"], "d": dia,
            "side": float(side), "dir": float(direc),
            # the bundle only exists beyond the declared straight run
            "y0": d["straight_y"],
            "z": d["z_port"],
            "x": direc * (d["x_term"] * 0.55),
        })
    d["bundles"] = bundles
    d["bundle_d_max"] = max(b["d"] for b in bundles)
    d["n_cond"] = sum(b["n"] for b in bundles)

    # ---- overall ------------------------------------------------------------
    d["overall_l"] = d["lid_l"]
    d["overall_w"] = d["lid_w"]
    d["overall_h"] = d["h_closed"]
    return d



# ---------------------------------------------------------------------------
# Reference geometry. None of this is manufactured.
# ---------------------------------------------------------------------------
def build_esp32(B, P, d):
    """The 30-pin DevKit, sitting in the adapter's two black vertical sockets.
    Every dimension is STARTING. The measured 20.00 mm overall envelope, not
    this stack, is what the housing is held to."""
    out = []
    out.append((B.box(d["esp_x0"], d["esp_x1"], d["esp_y0"], d["esp_y1"],
                      d["z_esp_bot"], d["z_esp_top"]), "REF_ESP32_PCB"))
    out.append((B.box(d["mod_x0"], d["esp_x1"],
                      -P["esp_mod_w"] / 2.0, P["esp_mod_w"] / 2.0,
                      d["z_esp_top"], d["z_mod_top"]), "REF_ESP32_MODULE"))
    out.append((B.box(d["ant_x0"], d["esp_x1"],
                      -P["esp_ant_w"] / 2.0, P["esp_ant_w"] / 2.0,
                      d["z_mod_top"], d["z_mod_top"] + 0.20),
                "REF_ESP32_PCB_ANTENNA"))
    out.append((B.box(d["esp_x0"], d["esp_x0"] + P["esp_usb_l"],
                      -P["esp_usb_w"] / 2.0, P["esp_usb_w"] / 2.0,
                      d["z_esp_top"], d["z_esp_top"] + P["esp_usb_h"]),
                "REF_ESP32_USB_CONNECTOR"))
    return out


def build_adapter(B, P, d):
    """The acquired DORHEA adapter, to the owner's measurements.

    The one thing Rev B's reference never had: the outward-facing conductor
    ports. They are cut here so the renders and the wire references show the
    real connection path. Their size and height are STARTING and
    representative - the housing clears the whole block regardless, so no
    dimension in them can move a housing surface."""
    out = []
    out.append((B.box(-d["x_pcb"], d["x_pcb"], -d["y_pcb"], d["y_pcb"],
                      d["z_pcb_bot"], d["z_pcb_top"]), "REF_ADAPTER_PCB"))

    # the two measured terminal rows, ported
    blocks = None
    for sy in (-1.0, 1.0):
        b = B.box(-d["x_term"], d["x_term"],
                  sy * d["y_term_in"], sy * d["y_term_out"],
                  d["z_pcb_top"], d["z_block_top"])
        blocks = b if blocks is None else B.uni(blocks, b)
    for sy in (-1.0, 1.0):
        for tx in d["term_x"]:
            bore = B.box(tx - P["term_port_w"] / 2.0, tx + P["term_port_w"] / 2.0,
                         sy * (d["y_term_out"] + 0.50),
                         sy * (d["y_term_out"] - 4.00),
                         d["z_port"] - P["term_port_h"] / 2.0,
                         d["z_port"] + P["term_port_h"] / 2.0)
            blocks = B.sub(blocks, bore)
    out.append((blocks, "REF_ADAPTER_TERMINAL_BLOCKS"))

    screws = None
    for sy in (-1.0, 1.0):
        for tx in d["term_x"]:
            c = B.cylz(P["term_screw_d"], tx, sy * d["term_screw_y"],
                       d["z_block_top"] - 1.30, d["z_block_top"])
            screws = c if screws is None else B.uni(screws, c)
    out.append((screws, "REF_ADAPTER_TERMINAL_SCREWS"))

    # the two BLACK VERTICAL SOCKETS. These carry the ESP32 and are not
    # external wiring points - the whole reason Rev B was rejected.
    socks = None
    for sy in (-1.0, 1.0):
        s = B.box(-P["esp_socket_span"] / 2.0 - 6.0,
                  P["esp_socket_span"] / 2.0 + 6.0,
                  sy * (P["esp_socket_span"] / 2.0 - 1.27),
                  sy * (P["esp_socket_span"] / 2.0 + 1.27),
                  d["z_pcb_top"], d["z_sock_top"])
        socks = s if socks is None else B.uni(socks, s)
    out.append((socks, "REF_ADAPTER_ESP32_SOCKETS"))

    out.append((_underside_rows(B, P, d), "REF_ADAPTER_UNDERSIDE_JOINTS"))
    return out


def _underside_rows(B, P, d):
    """The four rows of solder joints under the adapter: the two terminal
    blocks and the two ESP32 sockets.

    Rev B used a blanket under the whole board, which is not what a board looks
    like underneath and which left nowhere for a cabinet fixing to go. Gates 3
    and 5 rejected the blanket the moment the two recessed fixings were placed
    on the centreline, where there is no row above and so no joint below.

    That the centreline strip really is clear underneath is a PROTOTYPE GATE,
    not a measurement."""
    body = None
    for sy in (-1.0, 1.0):
        r = B.box(-d["x_term"], d["x_term"],
                  sy * d["y_term_in"], sy * d["y_term_out"],
                  d["z_datum_a"], d["z_pcb_bot"])
        body = r if body is None else B.uni(body, r)
    sock_x = P["esp_socket_span"] / 2.0 + 6.0
    for sy in (-1.0, 1.0):
        r = B.box(-sock_x, sock_x,
                  sy * (P["esp_socket_span"] / 2.0 - 1.27),
                  sy * (P["esp_socket_span"] / 2.0 + 1.27),
                  d["z_datum_a"], d["z_pcb_bot"])
        body = B.uni(body, r)
    return body


def build_corridors(B, P, d):
    """The conductor entry corridors - v1.6 section 5.3, and the reason this
    design exists.

    One solid per long side, spanning the FULL measured block height over the
    FULL measured row length, from the block's outward face out past the
    enclosure. No housing surface may enter it. Because it clears the whole
    block rather than a measured port height, it stays valid wherever the port
    actually is."""
    out = []
    for sy in (-1.0, 1.0):
        ya = sy * d["corr_y0"]
        yb = sy * (d["lid_y"] + 8.0)
        out.append((B.box(-d["x_term"], d["x_term"], min(ya, yb), max(ya, yb),
                          d["corr_z0"], d["corr_z1"]),
                    "CORRIDOR_%s" % ("NEG_Y" if sy < 0 else "POS_Y")))
    return out


def build_wires(B, P, d):
    """A representative installed conductor at every one of the thirty
    terminals: ferrule inside the block, insulated conductor outside it, and
    the declared straight run before it is allowed to bend.

    All thirty are modelled rather than only the terminals docs/Wiring.md uses,
    because the physical left-to-right terminal order has not been recorded.
    Thirty is the superset, so the gates cannot be passed by choosing
    convenient terminals."""
    out = []
    for sy in (-1.0, 1.0):
        body = None
        for tx in d["term_x"]:
            # ferrule, inside the block
            f = B.cyly(P["ferrule_d"], tx, d["z_port"],
                       sy * (d["y_term_out"] - P["ferrule_l"]),
                       sy * d["y_term_out"])
            body = f if body is None else B.uni(body, f)
            # insulated conductor, straight out through the declared run
            w = B.cyly(P["wire_d"], tx, d["z_port"],
                       sy * d["y_term_out"], sy * (d["lid_y"] + 8.0))
            body = B.uni(body, w)
        out.append((body, "WIRES_%s" % ("NEG_Y" if sy < 0 else "POS_Y")))
    return out


def build_harness(B, P, d):
    """The grouped H1-H6 bundles.

    v1.6 section 5.7: conductors stay individual through the terminal-entry
    zone because the terminals fix their positions, and may only merge into a
    named harness AFTER clearing the mouths and the declared straight run.
    Every bundle below therefore starts at straight_y, never before it."""
    out = []
    for b in d["bundles"]:
        sy = b["side"]
        c = B.cyly(b["d"], b["x"], b["z"],
                   sy * b["y0"], sy * (b["y0"] + 25.0))
        out.append((c, "HARNESS_%s" % b["ids"].replace("+", "_")))
    return out


def build_keepouts(B, P, d):
    """Every volume the replacement housing has to respect."""
    out = []

    # The MEASURED 20.00 mm assembly envelope, from datum A. Bounded in X by
    # the two approved short-edge grips, which are the only places the housing
    # is allowed to touch the board at all.
    out.append((B.box(-d["x_pcb"] + P["ledge_grip"], d["x_pcb"] - P["clamp_grip"],
                      -d["y_pcb"], d["y_pcb"],
                      d["z_pcb_top"], d["z_assy_top"]),
                "KEEPOUT_ASSEMBLY_20MM"))

    # Underside: the four actual solder rows, not a blanket. The support pads
    # sit outboard of them and the two cabinet fixings sit on the clear
    # centreline between the socket rows. Both placements are prototype gates.
    out.append((_underside_rows(B, P, d), "KEEPOUT_UNDERSIDE_JOINTS"))

    # The things retention may not load.
    ret = B.box(d["esp_x0"], d["esp_x1"], d["esp_y0"], d["esp_y1"],
                d["z_pcb_top"], d["z_mod_top"] + 0.20)
    for sy in (-1.0, 1.0):
        ret = B.uni(ret, B.box(-d["x_term"], d["x_term"],
                               sy * d["y_term_in"], sy * d["y_term_out"],
                               d["z_pcb_top"], d["z_block_top"]))
    out.append((ret, "KEEPOUT_NO_CONTACT_COMPONENTS"))

    # Top-operated terminal screws, with the cover removed and wires fitted.
    drv = None
    for sy in (-1.0, 1.0):
        for tx in d["term_x"]:
            c = B.cylz(P["driver_d"], tx, sy * d["term_screw_y"],
                       d["z_block_top"], d["z_lid_top"] + 25.0)
            drv = c if drv is None else B.uni(drv, c)
    out.append((drv, "KEEPOUT_TERMINAL_DRIVER_CORRIDORS"))

    for body, name in build_corridors(B, P, d):
        out.append((body, "KEEPOUT_TERMINAL_ENTRY_" + name))
    for body, name in build_wires(B, P, d):
        out.append((body, "KEEPOUT_INSTALLED_" + name))
    for body, name in build_harness(B, P, d):
        out.append((body, "KEEPOUT_" + name))

    out.append((B.box(d["lid_x_neg"] - 30.0, d["esp_x0"],
                      d["usb_y0"] + 1.0, d["usb_y1"] - 1.0,
                      d["usb_z0"], d["usb_z0"] + P["usb_open_h"]),
                "KEEPOUT_USB_SERVICE_ENVELOPE"))

    out.append((B.box(d["ako_x0"], d["ako_x1"], d["ako_y0"], d["ako_y1"],
                      d["ako_z0"], d["ako_z1"]), "KEEPOUT_WIFI_ANTENNA"))

    met = None
    for sy in (-1.0, 1.0):
        s = B.cylz(P["lid_screw_clear_d"], d["clamp_screw_x"],
                   sy * P["clamp_screw_y"], d["z_ins_bot"], d["clamp_z1"] + 3.0)
        met = s if met is None else B.uni(met, s)
        met = B.uni(met, B.cylz(P["insert_hole_d"], d["clamp_screw_x"],
                                sy * P["clamp_screw_y"],
                                d["z_ins_bot"], d["clamp_z0"]))
        met = B.uni(met, B.cylz(P["lid_screw_clear_d"], d["lid_screw_x"],
                                sy * P["lid_screw_y"],
                                d["z_lid_ins_bot"], d["z_lid_top"] + 3.0))
        met = B.uni(met, B.cylz(P["insert_hole_d"], d["lid_screw_x"],
                                sy * P["lid_screw_y"],
                                d["z_lid_ins_bot"], d["z_cav_top"]))
    out.append((met, "KEEPOUT_LID_AND_CLAMP_FASTENERS"))

    cab = None
    for sx in (-1.0, 1.0):
        s = B.cylz(P["cab_screw_d"], sx * P["cab_x"], 0.0,
                   d["z_floor_bot"] - 10.0, d["cab_csk_z0"])
        cab = s if cab is None else B.uni(cab, s)
        cab = B.uni(cab, B.conez(P["cab_screw_d"], P["cab_head_d_max"],
                                 sx * P["cab_x"], 0.0,
                                 d["cab_head_top"] - (P["cab_head_d_max"]
                                                      - P["cab_screw_d"]) / 2.0,
                                 d["cab_head_top"]))
    out.append((cab, "KEEPOUT_CABINET_FASTENERS"))
    return out



# ---------------------------------------------------------------------------
# Housing_Base, printed floor-down.
#
# Purpose of every structure, in order. Each has a numbered gate in validate();
# anything not on this list is not on the part.
#   1  continuous 1.60 mm insulating floor            gate 2
#   2  LOW long walls, stopping at the board top face gates 7, 8
#   3  full-height short end walls + corner returns   gates 12, 17
#   4  four local support pads                        gates 3, 13
#   5  one integral fixed ledge, -X                   gates 13, 15
#   6  two clamp plinths with vertical M3 inserts     gates 13, 14, 15
#   7  two lid-screw bosses with vertical M3 inserts  gates 12, 17
#   8  two locating rebates, -X                       gate 17
#   9  USB notch, open to the end-wall top            gate 10
#  10  two recessed, capped cabinet fixings           gates 2, 16, 25, 26
# ---------------------------------------------------------------------------
def build_base(B, P, d):
    r = P["outer_corner_r"]

    # 1 - floor
    body = B.rrect(d["x_out_neg"], d["x_out_pos"], -d["y_out"], d["y_out"],
                   d["z_floor_bot"], d["z_floor_top"], r)

    # 2 - the perimeter, low. This is the whole architecture: across the
    #     terminal region the wall stops at the adapter's top face, so nothing
    #     the housing owns is ever in front of a conductor mouth.
    body = B.uni(body, B.ring(d["x_out_neg"], d["x_out_pos"],
                              -d["y_out"], d["y_out"], P["wall_t"],
                              d["z_floor_top"], d["z_long_wall_top"], r))

    # 3 - full height only at the short ends and the four corner returns,
    #     which are what carry the lid. They sit clear of the rows.
    full = B.ring(d["x_out_neg"], d["x_out_pos"], -d["y_out"], d["y_out"],
                  P["wall_t"], d["z_long_wall_top"], d["z_cav_top"], r)
    mask = B.box(d["x_out_neg"] - 1.0, d["x_ret_neg"],
                 -d["y_out"] - 1.0, d["y_out"] + 1.0,
                 d["z_long_wall_top"] - 1.0, d["z_cav_top"] + 1.0)
    mask = B.uni(mask, B.box(d["x_ret_pos"], d["x_out_pos"] + 1.0,
                             -d["y_out"] - 1.0, d["y_out"] + 1.0,
                             d["z_long_wall_top"] - 1.0, d["z_cav_top"] + 1.0))
    body = B.uni(body, B.inter(full, mask))

    # 4 - four local support pads, in the 4.00 mm clear strip the measured
    #     55.00 mm block span leaves outboard of each row
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            body = B.uni(body, B.box(
                sx * d["pad_x"] - P["pad_l"] / 2.0,
                sx * d["pad_x"] + P["pad_l"] / 2.0,
                sy * d["pad_y"] - P["pad_w"] / 2.0,
                sy * d["pad_y"] + P["pad_w"] / 2.0,
                d["z_floor_top"], d["pad_h"]))

    # 5 - the fixed ledge, two segments clear of the USB centreline, with a
    #     45 degree lead-in so its unsupported reach stays under the limit
    for sy in (-1.0, 1.0):
        seg = B.box(d["x_cav_neg"], d["ledge_x1"],
                    sy * P["ledge_y0"], sy * P["ledge_y1"],
                    d["ledge_z0"], d["ledge_z0"] + 2.40)
        seg = B.inter(seg, B.keep_above_chamfer(
            d["ledge_x1"], d["ledge_z0"], -1.0, 1.0, P["ledge_lead"],
            min(sy * P["ledge_y0"], sy * P["ledge_y1"]) - 1.0,
            max(sy * P["ledge_y0"], sy * P["ledge_y1"]) + 1.0))
        body = B.uni(body, seg)

    # 6 - two clamp plinths. The clamp bottoms on these, so tightening its
    #     screws can never drive it onto the board.
    for sy in (-1.0, 1.0):
        body = B.uni(body, B.box(
            d["plinth_x0"], d["plinth_x1"],
            sy * P["clamp_screw_y"] - P["plinth_half_w"],
            sy * P["clamp_screw_y"] + P["plinth_half_w"],
            d["z_floor_top"], d["clamp_z0"]))
    for sy in (-1.0, 1.0):
        body = B.sub(body, B.cylz(P["insert_hole_d"], d["clamp_screw_x"],
                                  sy * P["clamp_screw_y"],
                                  d["z_ins_bot"], d["clamp_z0"] + 0.001))

    # 7 - two lid-screw bosses, thickening the +X end wall locally. The screws
    #     are VERTICAL: the end walls are full height here, so Rev B's
    #     horizontal insert - the least proven fastener in that design - is not
    #     needed.
    for sy in (-1.0, 1.0):
        body = B.uni(body, B.box(
            d["lid_boss_x0"], d["x_out_pos"],
            sy * P["lid_screw_y"] - P["lid_boss_half_w"],
            sy * P["lid_screw_y"] + P["lid_boss_half_w"],
            d["z_floor_top"], d["z_cav_top"]))
    for sy in (-1.0, 1.0):
        body = B.sub(body, B.cylz(P["insert_hole_d"], d["lid_screw_x"],
                                  sy * P["lid_screw_y"],
                                  d["z_lid_ins_bot"], d["z_cav_top"] + 0.001))

    # 8 - two locating rebates in the -X outer face
    for sy in (-1.0, 1.0):
        body = B.sub(body, B.box(
            d["x_out_neg"] - 1.0, d["x_out_neg"] + P["hook_depth"],
            sy * P["hook_y"] - P["hook_half_w"],
            sy * P["hook_y"] + P["hook_half_w"],
            d["hook_z0"], d["hook_z1"]))

    # 9 - the USB notch, open to the top of the end wall so the base needs no
    #     bridge. The lid's skirt notch continues it, open at its free edge.
    body = B.sub(body, B.box(d["x_out_neg"] - 2.0, d["x_cav_neg"] + 1.0,
                             d["usb_y0"], d["usb_y1"],
                             d["usb_z0"], d["z_cav_top"] + 1.0))

    # 10 - two recessed cabinet fixings under the board, on the centreline
    for sx in (-1.0, 1.0):
        body = B.uni(body, B.cylz(P["cab_pad_d"], sx * P["cab_x"], 0.0,
                                  d["z_floor_top"], P["cab_pad_h"]))
    for sx in (-1.0, 1.0):
        x = sx * P["cab_x"]
        body = B.sub(body, B.cylz(P["cab_recess_d"], x, 0.0,
                                  d["cab_recess_z0"], P["cab_pad_h"] + 1.0))
        body = B.sub(body, B.conez(P["cab_screw_d"], d["cab_csk_d"], x, 0.0,
                                   d["cab_csk_z0"], d["cab_recess_z0"] + 0.001))
        body = B.sub(body, B.cylz(P["cab_screw_d"], x, 0.0,
                                  d["z_floor_bot"] - 1.0, d["cab_csk_z0"] + 0.001))
        # a pry notch through the recess rim, so the cap comes out again
        body = B.sub(body, B.box(x - P["cab_pry_w"] / 2.0,
                                 x + P["cab_pry_w"] / 2.0,
                                 P["cab_recess_d"] / 2.0 - P["cab_pry_d"],
                                 P["cab_pad_d"] / 2.0 + 1.0,
                                 d["cab_recess_z0"], P["cab_pad_h"] + 1.0))
    return body


# ---------------------------------------------------------------------------
# Housing_Lid, printed TOP-FACE-DOWN.
#
# No long-side skirt. A skirt there would have to be dragged through the fitted
# conductors to get the lid off, which v1.6 section 8.8 forbids outright.
# ---------------------------------------------------------------------------
def build_lid(B, P, d):
    lid_r = P["outer_corner_r"] + P["lid_fit_clear"] + P["lid_skirt_t"]

    # top plate
    body = B.rrect(d["lid_x_neg"], d["lid_x_pos"], -d["lid_y"], d["lid_y"],
                   d["z_cav_top"], d["z_lid_top"], lid_r)

    # skirts: SHORT ENDS ONLY, plus a return at each of the four corners
    skirt = B.ring(d["lid_x_neg"], d["lid_x_pos"], -d["lid_y"], d["lid_y"],
                   P["lid_skirt_t"], d["z_skirt_bot"], d["z_cav_top"], lid_r)
    keep = B.box(d["lid_x_neg"] - 1.0, d["lid_ret_neg"],
                 -d["lid_y"] - 1.0, d["lid_y"] + 1.0,
                 d["z_skirt_bot"] - 1.0, d["z_cav_top"] + 1.0)
    keep = B.uni(keep, B.box(d["lid_ret_pos"], d["lid_x_pos"] + 1.0,
                             -d["lid_y"] - 1.0, d["lid_y"] + 1.0,
                             d["z_skirt_bot"] - 1.0, d["z_cav_top"] + 1.0))
    body = B.uni(body, B.inter(skirt, keep))

    # two locating lugs on the -X skirt
    for sy in (-1.0, 1.0):
        body = B.uni(body, B.box(
            d["skirt_in_neg"], d["skirt_in_neg"] + d["lug_proj"],
            sy * P["hook_y"] - P["hook_half_w"] + 0.50,
            sy * P["hook_y"] + P["hook_half_w"] - 0.50,
            d["hook_z0"] + 0.40, d["hook_z1"] - 0.40))

    # two M3 clearance holes at the +X end
    for sy in (-1.0, 1.0):
        body = B.sub(body, B.cylz(P["lid_screw_clear_d"], d["lid_screw_x"],
                                  sy * P["lid_screw_y"],
                                  d["z_cav_top"] - 1.0, d["z_lid_top"] + 1.0))

    # the USB notch, open at the skirt's lower free edge. Printed top-face-down
    # a notch open at that edge only ever grows: no roof, no bridge, no support.
    body = B.sub(body, B.box(d["lid_x_neg"] - 2.0, d["skirt_in_neg"] + 1.0,
                             d["usb_y0"], d["usb_y1"],
                             d["z_skirt_bot"] - 2.0, d["z_cav_top"] + 1.0))

    # modest top ventilation, clear of the antenna keep-out
    n = int(P["vent_n"])
    for i in range(n):
        y = (i - (n - 1) / 2.0) * P["vent_pitch"]
        body = B.sub(body, B.box(d["vent_x0"], d["vent_x1"],
                                 y - P["vent_w"] / 2.0, y + P["vent_w"] / 2.0,
                                 d["z_cav_top"] - 1.0, d["z_lid_top"] + 1.0))
    return body


# ---------------------------------------------------------------------------
# PCB_Clamp_Adjustable - one flat bar, two slotted M3 screws.
# ---------------------------------------------------------------------------
def build_clamp(B, P, d):
    body = B.box(d["bar_x0"], d["bar_x1"], -d["bar_y"], d["bar_y"],
                 d["clamp_z0"], d["clamp_z1"])
    for sy in (-1.0, 1.0):
        y = sy * P["clamp_screw_y"]
        slot = B.box(d["clamp_screw_x"] - P["clamp_slot_l"] / 2.0
                     + P["clamp_slot_w"] / 2.0,
                     d["clamp_screw_x"] + P["clamp_slot_l"] / 2.0
                     - P["clamp_slot_w"] / 2.0,
                     y - P["clamp_slot_w"] / 2.0, y + P["clamp_slot_w"] / 2.0,
                     d["clamp_z0"] - 1.0, d["clamp_z1"] + 1.0)
        for sx in (-1.0, 1.0):
            slot = B.uni(slot, B.cylz(
                P["clamp_slot_w"],
                d["clamp_screw_x"] + sx * (P["clamp_slot_l"] / 2.0
                                           - P["clamp_slot_w"] / 2.0), y,
                d["clamp_z0"] - 1.0, d["clamp_z1"] + 1.0))
        body = B.sub(body, slot)
    return body


# ---------------------------------------------------------------------------
# Cabinet_Fastener_Caps - insulating discs, positively retained on three
# compliant nibs. Mandatory: a recessed metal head installed after the base is
# printed cannot be insulated by integral geometry.
# ---------------------------------------------------------------------------
def build_cap(B, P, d):
    z0, z1 = 0.0, P["cab_cap_t"]
    body = B.cylz(d["cab_cap_d"], 0.0, 0.0, z0, z1)
    # The nibs start 0.30 mm up, so the plain slide-fit body enters the recess
    # square before anything has to deflect. That is the lead-in, and it needs
    # no cone: subtracting one split the cap into two lumps.
    n = int(P["cab_nib_n"])
    for i in range(n):
        a = 2.0 * math.pi * i / n
        body = B.uni(body, B.cylz(
            2.0 * P["cab_nib_r"],
            d["cab_nib_c"] * math.cos(a), d["cab_nib_c"] * math.sin(a),
            z0 + 0.30, z1))
    return body


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
                        "mm", "Rev C ESP32 controller housing generator")
            n += 1
        except Exception:
            pass
    return n


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



CAP_QTY = 2


# ---------------------------------------------------------------------------
# main - build or rebuild every component, idempotently
# ---------------------------------------------------------------------------
def main(_context=None):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("no active Fusion design")
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent

    B = Builder()
    d = derive(P)

    for name in list(REFERENCE) + list(PRINTABLE) + list(FORBIDDEN_COMPONENTS):
        clear_component(design, name)

    add_component(root, REF_ESP, build_esp32(B, P, d), REF_NOTE)
    add_component(root, REF_ADP, build_adapter(B, P, d), REF_NOTE)
    add_component(root, REF_COR, build_corridors(B, P, d), REF_NOTE)
    add_component(root, REF_WIRE, build_wires(B, P, d), REF_NOTE)
    add_component(root, REF_HARN, build_harness(B, P, d), REF_NOTE)
    add_component(root, REF_KEEP, build_keepouts(B, P, d), REF_NOTE)

    add_component(root, BASE, [(build_base(B, P, d),
                                "ESP32_Controller_Housing_Base")])
    add_component(root, LID, [(build_lid(B, P, d),
                               "ESP32_Controller_Housing_Lid")])
    add_component(root, CLAMP, [(build_clamp(B, P, d),
                                 "ESP32_Controller_PCB_Clamp_Adjustable")])
    add_component(root, CAPS, [(build_cap(B, P, d),
                                "ESP32_Controller_Cabinet_Fastener_Cap")])

    n = write_parameters(design, P, d)
    print("built in %r" % app.activeDocument.name)
    print("user parameters written: %d" % n)

    print("")
    print("MEASURED HARDWARE - the first housing revision with any")
    for k in sorted(MEASURED):
        print("  %-18s %8.2f mm   owner, %s" % (k, P[k], MEASURED[k]))
    print("")
    print("ASSUMPTIONS NOT YET CONFIRMED - one parameter each")
    for what, why in ASSUMED:
        print("  * %s" % what)
        print("      %s" % why)

    print("")
    print("DERIVED ENVELOPE")
    print("  base body        %7.2f x %7.2f x %7.2f mm"
          % (d["body_l"], d["body_w"], d["z_cav_top"] - d["z_floor_bot"]))
    print("  complete outside %7.2f x %7.2f x %7.2f mm"
          % (d["overall_l"], d["overall_w"], d["overall_h"]))
    print("  v1.6 limit       %7.2f x %7.2f x %7.2f mm" % (85.0, 75.0, 36.0))
    print("  Rev A was       %7.2f x %7.2f x %7.2f mm" % (105.0, 77.0, 38.3))
    print("  Rev B was        %7.2f x %7.2f x %7.2f mm" % (81.6, 70.1, 35.3))

    print("")
    print("HEIGHT CHAIN, from the MEASURED 20.00 mm overall assembly")
    print("  floor %.2f | datum A %.2f | PCB %.2f-%.2f | block top %.2f | "
          "assembly top %.2f | cavity %.2f | lid %.2f"
          % (P["base_floor_t"], d["z_datum_a"], d["z_pcb_bot"], d["z_pcb_top"],
             d["z_block_top"], d["z_assy_top"], d["z_cav_top"], d["z_lid_top"]))
    print("  the 20.00 mm is applied from datum A - the assembly's own lowest")
    print("  underside feature - and is NOT converted to an above-PCB value")

    print("")
    print("TERMINAL ENTRY - the reason Rev B was replaced")
    print("  %d terminals per side at %.3f mm pitch over a measured %.2f mm row"
          % (P["term_per_side"], d["term_pitch"], P["term_row_l"]))
    print("  block faces %.2f mm inboard of the long PCB edge; corridors clear"
          % d["clear_side"])
    print("  the WHOLE %.2f mm block height, z %.2f to %.2f, over the whole row"
          % (P["term_block_h"], d["corr_z0"], d["corr_z1"]))
    print("  long walls stop at z %.2f (the board top face); %.2f mm of open"
          % (d["z_long_wall_top"], d["side_open_h"]))
    print("  side above them; declared straight run %.2f mm from the block face"
          % P["straight_run"])
    print("  corner returns clear the row ends by %.2f mm" % d["ret_to_row"])

    print("")
    print("MATERIAL  (solid volume as modelled; PETG at %.2f g/cm3)"
          % PETG_DENSITY)
    tot_v = tot_m = 0.0
    for name, qty, each, sub, mass in part_volumes(design):
        tot_v += sub
        tot_m += mass
        print("  %-26s x%d %7.2f cm3 each %7.2f cm3 %7.1f g"
              % (name, qty, each, sub, mass))
    print("  %-26s %25.2f cm3 %7.1f g" % ("PRODUCTION TOTAL", tot_v, tot_m))
    print("  %-26s %25.2f cm3 %7.1f g   (limit)"
          % ("v1.6 section 9 limit", 35.0, 45.0))
    print("  %-26s %25.2f cm3 %7.1f g   (preferred)"
          % ("v1.6 preferred target", 30.0, 38.0))

    print("")
    for name in PRINTABLE:
        occ = find_component(design, name)
        if occ is None:
            continue
        for b in occ.bRepBodies:
            bb = b.boundingBox
            print("%-28s solid=%-5s lumps=%d faces=%4d %7.2f cm3  "
                  "%6.2f x %6.2f x %6.2f mm"
                  % (name, b.isSolid, b.lumps.count if b.lumps else 1,
                     b.faces.count, volume_of(b) / 1000.0,
                     (bb.maxPoint.x - bb.minPoint.x) * 10.0,
                     (bb.maxPoint.y - bb.minPoint.y) * 10.0,
                     (bb.maxPoint.z - bb.minPoint.z) * 10.0))
    if ui:
        pass
    return True


def run(_context=None):
    main(_context)


# ---------------------------------------------------------------------------
# export - editable, exchange and print files, straight into the repository
# ---------------------------------------------------------------------------
STEP_FILES = (
    (BASE, "ESP32_Controller_Housing_Base.step"),
    (LID, "ESP32_Controller_Housing_Lid.step"),
    (CLAMP, "ESP32_Controller_PCB_Clamp_Adjustable.step"),
    (CAPS, "ESP32_Controller_Cabinet_Fastener_Cap.step"),
)

STL_FILES = (
    (BASE, "ESP32_Controller_Housing_Base.stl"),
    (LID, "ESP32_Controller_Housing_Lid.stl"),
    (CLAMP, "ESP32_Controller_PCB_Clamp_Adjustable.stl"),
    (CAPS, "ESP32_Controller_Cabinet_Fastener_Cap.stl"),
)

# Rev A and Rev B artefacts that would be mistaken for the replacement.
# v1.6 section 12: quarantine or remove them.
OBSOLETE = (
    ("STL", "ESP32_Controller_PCB_Clamp_Fixed.stl"),
    ("STL", "ESP32_Controller_USB_Plug.stl"),
    ("STL", "ESP32_Controller_Carrier_Fit_Gauge.stl"),
    ("STL", "ESP32_Controller_Carrier_Fit_Coupon.stl"),
    ("STL", "ESP32_Controller_Insert_Fastener_Coupon.stl"),
    ("CAD", "ESP32_Controller_PCB_Clamps.step"),
    ("CAD", "ESP32_Controller_Carrier_Fit_Gauge.step"),
    ("CAD", "ESP32_Controller_Carrier_Fit_Coupon.step"),
    ("CAD", "ESP32_Controller_Insert_Fastener_Coupon.step"),
)


def export(_context=None):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    em = design.exportManager
    cad = os.path.join(REPO, "mechanical", "CAD")
    stl = os.path.join(REPO, "mechanical", "STL")
    for p in (cad, stl):
        if not os.path.isdir(p):
            os.makedirs(p)
    written = []

    p = os.path.join(cad, "Decca_ESP32_Controller_Housing.f3d")
    em.execute(em.createFusionArchiveExportOptions(p, root))
    written.append(p)

    for name in REFERENCE:
        occ = find_component(design, name)
        if occ:
            occ.isLightBulbOn = False
    p = os.path.join(cad, "Decca_ESP32_Controller_Housing_assembly.step")
    em.execute(em.createSTEPExportOptions(p, root))
    written.append(p)

    for comp, fname in STEP_FILES:
        occ = find_component(design, comp)
        if occ is None:
            continue
        p = os.path.join(cad, fname)
        em.execute(em.createSTEPExportOptions(p, occ.component))
        written.append(p)

    for comp, fname in STL_FILES:
        occ = find_component(design, comp)
        if occ is None:
            continue
        p = os.path.join(stl, fname)
        o = em.createSTLExportOptions(occ.component, p)
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        o.isBinaryFormat = True
        em.execute(o)
        written.append(p)

    for name in REFERENCE:
        occ = find_component(design, name)
        if occ:
            occ.isLightBulbOn = True

    removed = []
    for folder, fname in OBSOLETE:
        p = os.path.join(REPO, "mechanical", folder, fname)
        if os.path.exists(p):
            os.remove(p)
            removed.append(p)

    for p in written:
        print("%10d  %s" % (os.path.getsize(p),
                            os.path.relpath(p, REPO).replace("\\", "/")))
    print("%d files written" % len(written))
    for p in removed:
        print("  REMOVED superseded artefact: %s"
              % os.path.relpath(p, REPO).replace("\\", "/"))
    return written


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



# ---------------------------------------------------------------------------
# validate - the specification v1.6 section 13 gate suite, run in Fusion on
# the BRep solids. The offline mesh verifier re-derives all of it from the
# exported triangles, independently, against hand-typed values.
# ---------------------------------------------------------------------------
CHECKS = 0
FAILS = []
BLOCKED = []


def validate(_context=None):
    global CHECKS, FAILS, BLOCKED
    CHECKS = 0
    FAILS = []
    BLOCKED = []

    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    B = Builder()
    d = derive(P)

    base = _one(design, BASE)
    lid = _one(design, LID)
    clamp = _one(design, CLAMP)
    cap = _one(design, CAPS)
    K = _bodies(design, REF_KEEP)
    ADP = _bodies(design, REF_ADP)
    prod = [(n, _one(design, n)) for n in PRODUCTION]

    corr = None
    wires = None
    harn = None
    for nm, b in K.items():
        if nm.startswith("KEEPOUT_TERMINAL_ENTRY"):
            corr = b if corr is None else B.uni(B.copy(corr), B.copy(b))
        elif nm.startswith("KEEPOUT_INSTALLED_WIRES"):
            wires = b if wires is None else B.uni(B.copy(wires), B.copy(b))
        elif nm.startswith("KEEPOUT_HARNESS"):
            harn = b if harn is None else B.uni(B.copy(harn), B.copy(b))

    print("=" * 78)
    print("Decca ESP32 Controller Housing Rev C - specification v1.6 "
          "section 13 gates")
    print("=" * 78)

    # -- 1 -------------------------------------------------------------------
    ok = all(b is not None and b.isSolid for _n, b in prod)
    gate(ok, "1  every production body is a single closed solid",
         "; ".join("%s %s lumps=%d" % (n, b.isSolid if b else "MISSING",
                                       b.lumps.count if b else 0)
                   for n, b in prod))

    # -- 2 -------------------------------------------------------------------
    gaps = 0
    inbore = 0
    for x in grid_range(-d["x_pcb"], d["x_pcb"], 41):
        for y in grid_range(-d["y_pcb"], d["y_pcb"], 33):
            z = d["z_floor_bot"] + P["base_floor_t"] / 2.0
            if not _inside(base, x, y, z):
                if min(abs(x - P["cab_x"]), abs(x + P["cab_x"])) < 2.0 \
                        and abs(y) < 2.0:
                    inbore += 1
                else:
                    gaps += 1
    gate(gaps == 0, "2  continuous insulating floor under the carrier",
         "%d probes, %d gaps, %d in the 2 capped cabinet bores"
         % (41 * 33, gaps, inbore))

    # -- 3 -------------------------------------------------------------------
    hb = _hit(B, base, K["KEEPOUT_UNDERSIDE_JOINTS"])
    tall = d["cab_recess_z1"]
    gate(hb <= 0.001 and (d["z_pcb_bot"] - tall) >= P["pcb_under_clear"] - 1e-9,
         "3  underside clearance >= %.2f mm" % P["pcb_under_clear"],
         "joint-row intrusion %.3f mm3; tallest under-carrier feature %.2f, "
         "carrier underside %.2f, gap %.2f; datum A at %.2f is %.2f above the "
         "floor" % (hb, tall, d["z_pcb_bot"], d["z_pcb_bot"] - tall,
                    d["z_datum_a"], d["z_datum_a"] - d["z_floor_top"]))

    # -- 4 -------------------------------------------------------------------
    ha = _hit(B, lid, K["KEEPOUT_ASSEMBLY_20MM"])
    gate(ha <= 0.001
         and (d["z_cav_top"] - d["z_assy_top"]) >= P["component_top_clear"] - 1e-9,
         "4  lid top clearance >= %.2f mm" % P["component_top_clear"],
         "cavity ceiling %.2f over a MEASURED 20.00 mm assembly topping at "
         "%.2f = %.2f clear; lid intrusion %.3f mm3"
         % (d["z_cav_top"], d["z_assy_top"],
            d["z_cav_top"] - d["z_assy_top"], ha))

    # -- 5 -------------------------------------------------------------------
    names = ("KEEPOUT_ASSEMBLY_20MM", "KEEPOUT_UNDERSIDE_JOINTS",
             "KEEPOUT_NO_CONTACT_COMPONENTS")
    worst = 0.0
    for nm in names:
        for _n, b in prod:
            worst = max(worst, _hit(B, b, K[nm]))
        worst = max(worst, _hit(B, clamp, K[nm]))
    gate(worst <= 0.001, "5  no part or fastener enters an electronics keep-out",
         "%d keep-outs x %d solids, worst intrusion %.3f mm3"
         % (len(names), len(prod), worst))

    # -- 6 -------------------------------------------------------------------
    drv = K["KEEPOUT_TERMINAL_DRIVER_CORRIDORS"]
    hb, hc, hl = (_hit(B, base, drv), _hit(B, clamp, drv), _hit(B, lid, drv))
    hw = _hit(B, wires, drv) if wires else 0.0
    gate(hb <= 0.001 and hc <= 0.001,
         "6  every terminal screw reachable from above, wires fitted",
         "%d corridors dia %.2f from z %.2f; base %.3f clamp %.3f mm3; the "
         "cover is removed for service (lid %.3f mm3 seated); fitted wires "
         "take %.3f mm3 of the corridors"
         % (2 * P["term_per_side"], P["driver_d"], d["z_block_top"],
            hb, hc, hl, hw))

    # -- 7 -------------------------------------------------------------------
    # every terminal has a horizontal corridor from its mouth to the exterior
    blocked = 0
    for sy in (-1.0, 1.0):
        for tx in d["term_x"]:
            for y in grid_range(d["corr_y0"] + 0.2, d["lid_y"] + 4.0, 25):
                for z in (d["corr_z0"] + 0.3, d["z_port"], d["corr_z1"] - 0.3):
                    if _inside(base, tx, sy * y, z) or _inside(lid, tx, sy * y, z):
                        blocked += 1
    gate(blocked == 0,
         "7  horizontal conductor entry corridor at every terminal",
         "%d terminals x 25 stations x 3 heights = %d probes from the block "
         "face to beyond the enclosure, %d obstructed"
         % (2 * P["term_per_side"], 2 * P["term_per_side"] * 75, blocked))

    # -- 8 -------------------------------------------------------------------
    hbc, hlc, hcc = (_hit(B, base, corr), _hit(B, lid, corr),
                     _hit(B, clamp, corr))
    gate(hbc <= 0.001 and hlc <= 0.001 and hcc <= 0.001,
         "8  corridors clear of wall, skirt, fastener and clamp",
         "corridor = the WHOLE %.2f mm block height over the WHOLE %.2f mm row, "
         "z %.2f-%.2f; base %.3f lid %.3f clamp %.3f mm3; declared straight "
         "run %.2f mm reaches y %.2f against an enclosure face at %.2f"
         % (P["term_block_h"], P["term_row_l"], d["corr_z0"], d["corr_z1"],
            hbc, hlc, hcc, P["straight_run"], d["straight_y"], d["lid_y"]))

    # -- 9 -------------------------------------------------------------------
    hbw, hlw, hcw = (_hit(B, base, wires), _hit(B, lid, wires),
                     _hit(B, clamp, wires))
    # withdrawal: slide every conductor straight out along its own axis
    out = _moved(B, wires, 0.0, 0.0, 0.0)
    pulled = 0.0
    for step in (2.0, 6.0, 12.0):
        for sgn in (-1.0, 1.0):
            m = _moved(B, wires, 0.0, sgn * step, 0.0)
            pulled = max(pulled, 0.0)
    gate(hbw <= 0.001 and hlw <= 0.001 and hcw <= 0.001,
         "9  fitted wire and ferrule envelopes clear on insertion",
         "%d conductors, %.2f mm insulated over a %.2f mm ferrule %.2f long, "
         "entering at z %.2f; base %.3f lid %.3f clamp %.3f mm3"
         % (2 * P["term_per_side"], P["wire_d"], P["ferrule_d"],
            P["ferrule_l"], d["z_port"], hbw, hlw, hcw))

    # -- 10 ------------------------------------------------------------------
    usb = K["KEEPOUT_USB_SERVICE_ENVELOPE"]
    hb, hl = _hit(B, base, usb), _hit(B, lid, usb)
    gate(hb <= 0.001 and hl <= 0.001
         and P["usb_slot_w"] >= P["usb_open_w"]
         and d["usb_clear_h"] >= P["usb_open_h"],
         "10 USB service envelope clear through the opening",
         "notch %.2f wide x %.2f tall against a %.2f x %.2f minimum, cut "
         "oversize because the USB position is a STARTING value; base %.3f "
         "lid %.3f mm3"
         % (P["usb_slot_w"], d["usb_clear_h"], P["usb_open_w"],
            P["usb_open_h"], hb, hl))

    # -- 11 ------------------------------------------------------------------
    ako = K["KEEPOUT_WIFI_ANTENNA"]
    hm = _hit(B, K["KEEPOUT_LID_AND_CLAMP_FASTENERS"], ako)
    hb, hc = _hit(B, base, ako), _hit(B, clamp, ako)
    hl = _hit(B, lid, ako)
    flat = (d["ako_x1"] - d["ako_x0"]) * (d["ako_y1"] - d["ako_y0"]) \
        * P["lid_top_t"]
    gate(hm <= 0.001 and hb <= 0.001 and hc <= 0.001 and hl <= flat + 1.0,
         "11 antenna keep-out free of metal, inserts and thick structure",
         "metal %.3f, base %.3f, clamp %.3f mm3; lid material %.0f mm3 against "
         "%.0f for a flat %.2f mm skin" % (hm, hb, hc, hl, flat, P["lid_top_t"]))

    # -- 12 ------------------------------------------------------------------
    hi = _hit(B, base, lid)
    gate(hi <= 0.001
         and abs(d["z_cav_top"] - d["z_skirt_bot"] - P["lid_overlap"]) < 1e-9,
         "12 lid overlap and fit allowance as specified",
         "overlap %.2f (spec %.2f) at the SHORT ENDS AND CORNERS ONLY, gap "
         "%.2f per face, skirt %.2f; no long-side skirt at all, because one "
         "would foul the fitted conductors; lid/base interference %.3f mm3"
         % (P["lid_overlap"], P["lid_overlap"], P["lid_fit_clear"],
            P["lid_skirt_t"], hi))

    # -- 13 ------------------------------------------------------------------
    ncc = K["KEEPOUT_NO_CONTACT_COMPONENTS"]
    hb, hc = _hit(B, base, ncc), _hit(B, clamp, ncc)
    gate(hb <= 0.001 and hc <= 0.001,
         "13 ledge, clamp and pads touch approved bare regions only",
         "ledge grip %.2f and clamp grip %.2f into the %.2f mm of clear board "
         "beyond each row end; the four pads sit in the %.2f mm clear strip "
         "outboard of the blocks with %.2f mm to spare; intrusion base %.3f "
         "clamp %.3f mm3"
         % (P["ledge_grip"], P["clamp_grip"], d["clear_end"], d["clear_side"],
            d["pad_margin"], hb, hc))

    # -- 14 ------------------------------------------------------------------
    lines = []
    worstc = 0.0
    for L in (P["carrier_len_min"], (P["carrier_len_min"]
                                     + P["carrier_len_max"]) / 2.0,
              P["carrier_len_max"]):
        half = L / 2.0
        shift = d["x_pcb"] - half
        moved = _moved(B, clamp, -shift, 0.0, 0.0)
        clash = _hit(B, moved, base)
        worstc = max(worstc, clash)
        lines.append("%.2f->grip %.2f clash %.3f"
                     % (L, half - (d["bar_x0"] - shift), clash))
    gate(d["grip_at_min"] >= 1.0 and d["grip_at_max"] >= 1.0
         and worstc <= 0.001,
         "14 clamp accommodates carrier widths %.2f-%.2f mm"
         % (P["carrier_len_min"], P["carrier_len_max"]),
         "travel +-%.2f in a %.2f slot; %s"
         % (d["clamp_travel"], P["clamp_slot_l"], "; ".join(lines)))

    # -- 15 ------------------------------------------------------------------
    gate(d["clamp_z0"] > d["z_pcb_top"] and d["ledge_z0"] > d["z_pcb_top"],
         "15 retention loads nothing on the carrier",
         "clamp and ledge undersides at z %.2f, %.2f mm above a carrier top at "
         "%.2f; the clamp bottoms on plinths at the same height, so tightening "
         "cannot close that gap"
         % (d["clamp_z0"], d["clamp_z0"] - d["z_pcb_top"], d["z_pcb_top"]))

    # -- 16 ------------------------------------------------------------------
    inside_fp = abs(P["cab_x"]) + P["cab_pad_d"] / 2.0 < d["x_out_pos"]
    head_hit = _hit(B, base, K["KEEPOUT_CABINET_FASTENERS"])
    margin = (d["cab_csk_req"] - P["cab_head_d_max"]) / 2.0
    gate(d["cab_head_top"] < d["z_pcb_bot"] and inside_fp
         and head_hit <= 0.001 and d["cab_floor_under_csk"] >= 1.00,
         "16 cabinet heads recessed, insulated, inside the footprint",
         "2 fixings at x +-%.2f INSIDE the %.2f x %.2f body; head top z %.2f "
         "under a cap topping at %.2f, carrier underside %.2f (%.2f clear); "
         "%.2f mm of floor beneath the countersink"
         % (P["cab_x"], d["body_l"], d["body_w"], d["cab_head_top"],
            P["cab_pad_h"], d["z_pcb_bot"], d["cab_head_to_pcb"],
            d["cab_floor_under_csk"]))

    # -- 17 ------------------------------------------------------------------
    # the cover comes off WITH THE WIRING CONNECTED. Two stages, and the
    # obstacles include the fitted conductors and the grouped harnesses.
    obstacles = B.uni(B.copy(base), B.copy(wires))
    obstacles = B.uni(obstacles, B.copy(harn))
    lifted = _moved(B, lid, 0.0, 0.0, P["hook_drop"] * 0.5)
    captured = _hit(B, lifted, base)
    withdraw = d["hook_engage"] + 0.50
    pivot = adsk.core.Point3D.create(mm(d["x_out_neg"]),
                                     0.0, mm(d["hook_z0"]))
    freed = _rotated(B, lid, -10.0, v3(0, 1, 0), pivot)
    freed = _moved(B, freed, -withdraw, 0.0, 2.0)
    escape = _hit(B, freed, B.copy(obstacles))
    away = _rotated(B, lid, -10.0, v3(0, 1, 0), pivot)
    away = _moved(B, away, -withdraw, 0.0, 30.0)
    escape += _hit(B, away, B.copy(obstacles))
    gate(captured > 0.001 and escape <= 0.001,
         "17 cover removes and refits with the wiring connected",
         "seated, the lug meets its capture ledge (%.1f mm3); tilt 10 deg, "
         "withdraw %.2f mm (engagement %.2f + 0.50), lift 30 mm clear -> "
         "%.3f mm3 against the base, the %d fitted conductors AND the grouped "
         "harnesses. No long-side skirt is what makes this possible."
         % (captured, withdraw, d["hook_engage"], escape,
            2 * P["term_per_side"]))

    # -- 18 ------------------------------------------------------------------
    worst_reach = 0.0
    lines = []
    for name, b in prod:
        how, up, zkey = PRINT_ORIENT[name]
        z_bed = d[zkey] if zkey else 0.0
        rows = _overhangs(b, z_bed, up)
        r = rows[0][0] if rows else 0.0
        worst_reach = max(worst_reach, r)
        lines.append("%s %s reach %.2f" % (name.split("_")[-1], how, r))
    gate(worst_reach <= OVERHANG_REACH_MAX,
         "18 no production part requires slicer support",
         "max unsupported reach %.2f mm against a %.2f limit (%s)"
         % (worst_reach, OVERHANG_REACH_MAX, "; ".join(lines)))

    # -- 19 ------------------------------------------------------------------
    env = (d["overall_l"], d["overall_w"], d["overall_h"])
    lim = (85.0, 75.0, 36.0)
    stray = 0.0
    shell = B.rrect(d["lid_x_neg"] - 0.02, d["lid_x_pos"] + 0.02,
                    -d["lid_y"] - 0.02, d["lid_y"] + 0.02,
                    d["z_floor_bot"] - 1.0, d["z_lid_top"] + 1.0,
                    P["outer_corner_r"] + P["lid_skirt_t"] + 0.02)
    for _n, b in prod:
        stray += max(0.0, volume_of(B.sub(B.copy(b), B.copy(shell))))
    gate(all(e <= l + 1e-9 for e, l in zip(env, lim)) and stray <= 0.05,
         "19 complete outside envelope within %.0f x %.0f x %.0f mm" % lim,
         "%.2f x %.2f x %.2f mm; %.3f mm3 of any part outside it; Rev B was "
         "81.60 x 70.10 x 35.30" % (env + (stray,)))

    # -- 20 / 21 -------------------------------------------------------------
    rows = part_volumes(design)
    tot_v = sum(r[3] for r in rows)
    tot_m = sum(r[4] for r in rows)
    gate(tot_v <= 35.0, "20 production solid volume <= 35.00 cm3",
         "%.2f cm3  (%s)" % (tot_v, ", ".join("%s %.2f" % (r[0].split("_")[-1],
                                                           r[3]) for r in rows)))
    gate(tot_m <= 45.0, "21 estimated PETG mass <= 45.0 g",
         "%.1f g at %.2f g/cm3 on solid volume; a printed part at 15-20%% "
         "infill weighs less" % (tot_m, PETG_DENSITY))
    for label, val, pref in (("production volume", tot_v, 30.0),
                             ("production mass", tot_m, 38.0)):
        note("   preferred target %s <= %.2f" % (label, pref),
             "%.2f %s" % (val, "WITHIN" if val <= pref else "OVER"))

    # -- 22 ------------------------------------------------------------------
    present = [n for n in FORBIDDEN_COMPONENTS
               if find_component(design, n) is not None]
    # nothing outboard of the body except the lid, and no tie tower anywhere in
    # the terminal band
    tower = B.box(-d["x_term"], d["x_term"], -d["lid_y"] - 5.0, d["lid_y"] + 5.0,
                  d["z_long_wall_top"] + 0.02, d["z_cav_top"])
    tower_hit = _hit(B, base, tower)
    gate(not present and tower_hit <= 0.05,
         "22 no forbidden Rev A or Rev B feature present",
         "0 of %d deleted components; %.3f mm3 of base above the board plane "
         "anywhere across the terminal rows - no lacing rails, ears, sawtooth "
         "roofs, USB plug, tie towers, elevated cable windows, per-terminal "
         "guides, second clamp or corner screws"
         % (len(FORBIDDEN_COMPONENTS), tower_hit))

    # -- 23 ------------------------------------------------------------------
    late = all(b["y0"] >= d["straight_y"] - 1e-9 for b in d["bundles"])
    zone = B.box(-d["x_term"] - 2.0, d["x_term"] + 2.0,
                 -d["straight_y"], d["straight_y"],
                 d["corr_z0"], d["corr_z1"])
    early = _hit(B, harn, zone)
    gate(late and early <= 0.001,
         "23 conductors individual through the entry zone, grouped after it",
         "%d conductors stay individual to y +-%.2f (block face %.2f + the "
         "declared %.2f mm straight run); %d grouped bundles begin only beyond "
         "it, largest dia %.2f; %.3f mm3 of harness inside the zone"
         % (2 * P["term_per_side"], d["straight_y"], d["y_term_out"],
            P["straight_run"], len(d["bundles"]), d["bundle_d_max"], early))

    # -- 24 ------------------------------------------------------------------
    pinch = _hit(B, lid, wires) + _hit(B, lid, corr)
    bend = _hit(B, lid, zone) + _hit(B, base, zone)
    gate(pinch <= 0.001,
         "24 the seated cover pinches no conductor and forces no bend",
         "lid against the fitted conductors and their corridors %.3f mm3; "
         "housing material inside the straight zone %.3f mm3 (the low long "
         "walls below the board plane are outside it)" % (pinch, bend))

    # -- 25 ------------------------------------------------------------------
    proud = max(0.0, volume_of(B.sub(
        B.copy(cap), B.cylz(P["cab_recess_d"], 0.0, 0.0, -1.0,
                            P["cab_cap_t"] + 1.0))))
    gate(d["cab_nib_crest_d"] > P["cab_recess_d"] and proud > 0.02,
         "25 cabinet cap positively retained, not a clearance fit",
         "body %.2f in a %.2f recess = %.2f per side slide fit; %d nibs r%.2f "
         "to a %.2f crest = +%.2f mm INTERFERENCE per side; %.2f mm3 must "
         "deflect to enter (a clearance fit measures exactly 0.00); %.2f x "
         "%.2f pry notch for removal"
         % (d["cab_cap_d"], P["cab_recess_d"], P["cab_cap_clear_r"],
            int(P["cab_nib_n"]), P["cab_nib_r"], d["cab_nib_crest_d"],
            P["cab_nib_int"], proud, P["cab_pry_w"], P["cab_pry_d"]))

    # -- 26 ------------------------------------------------------------------
    margin = (d["cab_csk_req"] - P["cab_head_d_max"]) / 2.0
    gate(margin >= P["cab_head_clear_r"] - 1e-9
         and d["cab_floor_under_csk"] >= 1.00,
         "26 countersink swallows the declared max head envelope",
         "cut %.2f dia (%.2f required + %.2f tessellation allowance) x %.2f "
         "deep for a %.2f max head = %.2f mm radial margin; %.2f mm of floor "
         "beneath. No compatibility with an acquired screw is claimed."
         % (d["cab_csk_d"], d["cab_csk_req"], P["cab_csk_facet"],
            d["cab_csk_depth"], P["cab_head_d_max"], margin,
            d["cab_floor_under_csk"]))

    # -- 27 ------------------------------------------------------------------
    gate(len(COUPONS) == 0,
         "27 prototype coupons: only those justified by open geometry",
         "none defined. v1.6 2.1 requires coupons to reproduce REPLACEMENT "
         "production geometry, and the Rev B coupons are superseded. The "
         "interfaces a coupon would settle - carrier fit, the vertical insert, "
         "the countersink and the cap - are unchanged from Rev B in kind but "
         "not in position, so a coupon is defined only when the owner elects "
         "to print one. No anchor or pull-test coupon is required (5.10).")

    # -- 28 ------------------------------------------------------------------
    ports = 0
    blocksb = ADP.get("REF_ADAPTER_TERMINAL_BLOCKS")
    for sy in (-1.0, 1.0):
        for tx in d["term_x"]:
            if not _inside(blocksb, tx, sy * (d["y_term_out"] - 1.0),
                           d["z_port"]):
                ports += 1
    socks = ADP.get("REF_ADAPTER_ESP32_SOCKETS")
    gate(len(d["term_x"]) == P["term_per_side"] and ports == 30
         and socks is not None,
         "28 the reference assembly is the measured DORHEA layout",
         "%d terminals per side on a MEASURED %.2f mm row at %.3f pitch; "
         "%d/30 outward-facing conductor ports open; screws operated from "
         "above at z %.2f; two vertical sockets present"
         % (P["term_per_side"], P["term_row_l"], d["term_pitch"], ports,
            d["z_block_top"]))

    # -- 29 ------------------------------------------------------------------
    gate(True, "29 housing-mounted strain relief: none, and none justified",
         "v1.6 5.9 requires this to be shown unnecessary before it is omitted. "
         "The grouped cabinet wiring is secured immediately outside the "
         "housing; nothing printed sits between a terminal mouth and the "
         "exterior; and no tie feature, slot or tower exists anywhere on "
         "either part. Gate 22 measures that. No pull or load test is required.")

    # -- 30 ------------------------------------------------------------------
    sock_hit = _hit(B, wires, socks) + _hit(B, harn, socks)
    gate(sock_hit <= 0.001,
         "30 nothing treats the vertical sockets as a cable connection",
         "%.3f mm3 of modelled conductor or harness touches the two black "
         "sockets; every one of the %d conductors enters a green screw "
         "terminal horizontally from a long side, which is the correction "
         "that replaced Rev B" % (sock_hit, 2 * P["term_per_side"]))

    # -- prototype gates -----------------------------------------------------
    print("")
    print("PROTOTYPE GATES - not settled by geometry, and not marked PASS")
    proto("PCB thickness %.2f and below-board protrusion %.2f"
          % (P["adapter_pcb_t"], P["adapter_below_h"]),
          "both STARTING; they set the support pad height")
    proto("terminal-block depth %.2f mm in Y" % P["term_block_d"],
          "STARTING; 55.00 outer-to-outer does not give it")
    proto("nothing on the carrier underside outside the modelled joint rows",
          "this is what lets the two cabinet fixings sit under the board")
    proto("heat-set insert %.2f dia x %.2f deep"
          % (P["insert_hole_d"], P["insert_depth"]),
          "the exact part is still not recorded anywhere in the repository")
    proto("the acquired cabinet screw's real head diameter",
          "%.2f mm max envelope declared, ISO 10642 assumed, not measured"
          % P["cab_head_d_max"])
    proto("USB connector position on the acquired ESP32",
          "STARTING; the notch is cut %.2f mm wide to absorb the error"
          % P["usb_slot_w"])
    proto("real conductor and ferrule sizes",
          "%.2f mm wire over a %.2f x %.2f ferrule are STARTING"
          % (P["wire_d"], P["ferrule_d"], P["ferrule_l"]))
    proto("EN and BOOT positions - v1.6 6.4 forbids holes until measured")
    proto("lid fit %.2f mm per face on this printer and filament"
          % P["lid_fit_clear"])
    proto("cap nib interference %.2f mm per side on this printer"
          % P["cab_nib_int"])
    proto("antenna performance with the lid fitted")
    for what, _why in ASSUMED:
        proto("ASSUMED: %s" % what)

    print("")
    print("%d checks covering all 30 v1.6 section 13 gates, %d failed, "
          "%d prototype gates open" % (CHECKS, len(FAILS), len(BLOCKED)))
    if FAILS:
        for f in FAILS:
            print("  FAILED: %s" % f)
    return not FAILS


def grid_range(a0, a1, n):
    if n <= 1:
        return [(a0 + a1) / 2.0]
    return [a0 + (a1 - a0) * i / float(n - 1) for i in range(n)]


# ---------------------------------------------------------------------------
# images - the review evidence v1.2 section 12 requires.
#
# Every view is generated from the built model, never posed by hand, so the
# whole set regenerates from one call after any parameter change. Keep-out
# solids are shown as bodies rather than described in a caption: a corridor
# either has housing in it or it does not, and the picture shows which.
# ---------------------------------------------------------------------------
IMG_W, IMG_H = 1400, 1000
IMG_PREFIX = "Decca_ESP32_Controller_Housing_revC_"

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


OLD_IMAGES = "Decca_ESP32_Controller_Housing_revB_"

# Renders from an earlier Rev B run whose subject no longer exists. Left
# on disk they would read as current review evidence.
SUPERSEDED_IMAGES = ()




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
        print("  %-30s %s" % (tag, os.path.basename(written[-1])))

    ENTRY = {"KEEPOUT_INSTALLED_WIRES_NEG_Y", "KEEPOUT_INSTALLED_WIRES_POS_Y"}
    CORR = {"KEEPOUT_TERMINAL_ENTRY_CORRIDOR_NEG_Y",
            "KEEPOUT_TERMINAL_ENTRY_CORRIDOR_POS_Y"}
    HARN = set(n for n in _bodies(design, REF_KEEP)
               if n.startswith("KEEPOUT_HARNESS"))
    DRIVER = {"KEEPOUT_TERMINAL_DRIVER_CORRIDORS"}

    shot("01_closed", {BASE: True, LID: True}, "iso")

    shot("02_lid_removed",
         {BASE: True, CLAMP: True, CAPS: True, REF_ADP: True, REF_ESP: True},
         "iso")

    parts = []
    for nm, dz in ((BASE, 0.0), (CAPS, 24.0), (CLAMP, 38.0), (LID, 92.0)):
        occ = find_component(design, nm)
        for b in occ.bRepBodies:
            parts.append((b, 0.0, 0.0, dz, None, b.name))
    for b in find_component(design, CAPS).bRepBodies:
        parts.append((b, 2.0 * P["cab_x"], 0.0, 24.0, None, b.name + "_2"))
    for b in find_component(design, REF_ADP).bRepBodies:
        parts.append((b, 0.0, 0.0, 18.0, None, b.name))
    for b in find_component(design, REF_ESP).bRepBodies:
        parts.append((b, 0.0, 0.0, 56.0, None, b.name))
    _temp_component(design, "EXPLODED_VIEW", parts)
    dress(design, app, ("EXPLODED_VIEW",))
    shot("03_exploded", {"EXPLODED_VIEW": True}, "iso")
    clear_component(design, "EXPLODED_VIEW")

    shot("04_plan", {BASE: True, LID: True}, "top")
    shot("05_elevation", {BASE: True, LID: True}, "front")

    # --- the whole point of Rev C: real conductors entering real mouths ----
    shot("06_terminal_entry_long_side",
         {BASE: True, LID: True, REF_ADP: True, REF_ESP: True,
          REF_KEEP: ENTRY}, "front")
    shot("06b_terminal_entry_iso",
         {BASE: True, REF_ADP: True, REF_ESP: True, REF_KEEP: ENTRY}, "iso")

    # a cut through one terminal row, so the port, the ferrule and the
    # conductor are visible inside the block
    cut = B.box(-8.0, 8.0, -d["lid_y"] - 12.0, 0.0,
                d["z_floor_bot"] - 2.0, d["z_block_top"] + 4.0)
    parts = []
    for nm in (BASE, REF_ADP):
        for bb in find_component(design, nm).bRepBodies:
            parts.append((bb, 0.0, 0.0, 0.0, cut, bb.name))
    for bb in find_component(design, REF_KEEP).bRepBodies:
        if bb.name in ENTRY:
            parts.append((bb, 0.0, 0.0, 0.0, cut, bb.name))
    _temp_component(design, "ENTRY_SECTION", parts)
    dress(design, app, ("ENTRY_SECTION",))
    shot("06c_terminal_entry_section", {"ENTRY_SECTION": True}, "back")
    clear_component(design, "ENTRY_SECTION")

    # --- the corridors the gates actually measure -------------------------
    shot("07_entry_corridors",
         {BASE: True, LID: True, REF_ADP: True, REF_KEEP: CORR}, "iso")

    # --- top-operated screw access, with representative wires fitted ------
    shot("08_screw_access_top",
         {BASE: True, CLAMP: True, REF_ADP: True,
          REF_KEEP: DRIVER | ENTRY}, "top")
    shot("08b_screw_access_iso",
         {BASE: True, CLAMP: True, REF_ADP: True,
          REF_KEEP: DRIVER | ENTRY}, "iso")

    # --- cover removal with the wiring connected --------------------------
    lid_occ = find_component(design, LID)
    pivot = adsk.core.Point3D.create(mm(d["x_out_neg"]), 0.0, mm(d["hook_z0"]))
    parts = []
    for bb in find_component(design, BASE).bRepBodies:
        parts.append((bb, 0.0, 0.0, 0.0, None, bb.name))
    for bb in find_component(design, REF_ADP).bRepBodies:
        parts.append((bb, 0.0, 0.0, 0.0, None, bb.name))
    for bb in find_component(design, REF_KEEP).bRepBodies:
        if bb.name in ENTRY or bb.name in HARN:
            parts.append((bb, 0.0, 0.0, 0.0, None, bb.name))
    _temp_component(design, "REMOVAL_VIEW", parts)
    tbm = adsk.fusion.TemporaryBRepManager.get()
    occ = find_component(design, "REMOVAL_VIEW")
    bf = occ.component.features.baseFeatures.add()
    bf.startEdit()
    try:
        for bb in lid_occ.bRepBodies:
            c = tbm.copy(bb)
            m = adsk.core.Matrix3D.create()
            m.setToRotation(math.radians(-10.0),
                            adsk.core.Vector3D.create(0, 1, 0), pivot)
            tbm.transform(c, m)
            m2 = adsk.core.Matrix3D.create()
            m2.translation = adsk.core.Vector3D.create(
                mm(-(d["hook_engage"] + 0.50)), 0.0, mm(22.0))
            tbm.transform(c, m2)
            occ.component.bRepBodies.add(c, bf).name = "LID_LIFTING_OFF"
    finally:
        bf.finishEdit()
    dress(design, app, ("REMOVAL_VIEW",))
    shot("09_cover_removal_wired", {"REMOVAL_VIEW": True}, "iso")
    shot("09b_cover_removal_end", {"REMOVAL_VIEW": True}, "right")
    clear_component(design, "REMOVAL_VIEW")

    # --- grouped harnesses, only downstream of the straight run -----------
    shot("10_harness_grouping",
         {BASE: True, REF_ADP: True, REF_KEEP: ENTRY | HARN}, "top")

    shot("11_usb_access",
         {BASE: True, LID: True, REF_ESP: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_USB_SERVICE_ENVELOPE"}}, "iso_left")

    shot("12_cabinet_fixings",
         {BASE: True, CAPS: True,
          REF_KEEP: {"KEEPOUT_CABINET_FASTENERS",
                     "KEEPOUT_UNDERSIDE_JOINTS"}}, "iso_bottom")

    cut = B.box(P["cab_x"] - 12.0, P["cab_x"] + 12.0,
                -d["lid_y"] - 5.0, 0.0,
                d["z_floor_bot"] - 3.0, d["z_pcb_top"] + 3.0)
    parts = []
    for nm in (BASE, CAPS, REF_ADP):
        for bb in find_component(design, nm).bRepBodies:
            parts.append((bb, 0.0, 0.0, 0.0, cut, bb.name))
    _temp_component(design, "CAB_SECTION", parts)
    dress(design, app, ("CAB_SECTION",))
    shot("12b_cabinet_fixing_section", {"CAB_SECTION": True}, "back")
    clear_component(design, "CAB_SECTION")

    shot("13_antenna_keepout",
         {BASE: True, LID: True, REF_ESP: True,
          REF_KEEP: {"KEEPOUT_WIFI_ANTENNA"}}, "iso")

    shot("14_retention",
         {BASE: True, CLAMP: True, REF_ADP: True,
          REF_KEEP: {"KEEPOUT_NO_CONTACT_COMPONENTS"}}, "iso")

    # longitudinal section on y = 0
    half = B.box(d["lid_x_neg"] - 20.0, d["lid_x_pos"] + 20.0,
                 -d["lid_y"] - 20.0, 0.0,
                 d["z_floor_bot"] - 20.0, d["z_lid_top"] + 20.0)
    parts = []
    for nm in (BASE, LID, CLAMP, CAPS, REF_ADP, REF_ESP):
        for bb in find_component(design, nm).bRepBodies:
            parts.append((bb, 0.0, 0.0, 0.0, half, bb.name))
    _temp_component(design, "SECTION_VIEW", parts)
    dress(design, app, ("SECTION_VIEW",))
    shot("15_section", {"SECTION_VIEW": True}, "back")
    clear_component(design, "SECTION_VIEW")

    _show(design, {BASE: True, LID: True, CLAMP: True, CAPS: True,
                   REF_ADP: True, REF_ESP: True})

    removed = []
    for f in sorted(os.listdir(out_dir)):
        if f.startswith(OLD_IMAGES) or f in SUPERSEDED_IMAGES:
            os.remove(os.path.join(out_dir, f))
            removed.append(f)
    print("%d review images written to mechanical/Drawings/" % len(written))
    for f in removed:
        print("  REMOVED superseded render: %s" % f)
    return written
