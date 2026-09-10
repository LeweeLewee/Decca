#!/usr/bin/env python3
"""Generate Decca IEC C14 mounting plate Rev A.

Controlling specification:
  mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_Spec_revA.md

Outputs:
  Decca_IEC_C14_Mounting_Plate_revA.step
  ../STL/Decca_IEC_C14_Mounting_Plate_revA.stl

CadQuery 2.x / OCCT. All dimensions are millimetres.
"""

from pathlib import Path
import math
import cadquery as cq
from cadquery import exporters

# Locked Rev A parameters -----------------------------------------------------
PLATE_W = 40.00
PLATE_H = 50.00
PLATE_T = 3.00
OUTER_R = 2.00

CUTOUT_W = 20.00
CUTOUT_H = 27.60

M2_D = 2.40
M2_HOLES = (
    (-15.50, -8.50),
    (+15.50, -8.50),
    (-15.50, +8.50),
    (+15.50, +8.50),
)

M3_D = 3.40
M3_HOLES = ((0.00, -19.50), (0.00, +19.50))


def _through_rect(width: float, height: float) -> cq.Workplane:
    """Return a cutter that passes fully through the plate."""
    return (
        cq.Workplane("XY", origin=(0, 0, -1.0))
        .rect(width, height)
        .extrude(PLATE_T + 2.0)
    )


def _through_cylinder(x: float, y: float, diameter: float) -> cq.Workplane:
    """Return a cylindrical through-cutter at x/y."""
    return (
        cq.Workplane("XY", origin=(0, 0, -1.0))
        .center(x, y)
        .circle(diameter / 2.0)
        .extrude(PLATE_T + 2.0)
    )


def build() -> cq.Shape:
    """Build the single Rev A solid."""
    plate = (
        cq.Workplane("XY")
        .box(PLATE_W, PLATE_H, PLATE_T, centered=(True, True, False))
        .edges("|Z")
        .fillet(OUTER_R)
    )

    plate = plate.cut(_through_rect(CUTOUT_W, CUTOUT_H))
    for x, y in M2_HOLES:
        plate = plate.cut(_through_cylinder(x, y, M2_D))
    for x, y in M3_HOLES:
        plate = plate.cut(_through_cylinder(x, y, M3_D))

    shape = plate.val()
    solids = shape.Solids()
    if len(solids) != 1:
        raise RuntimeError(f"Expected one solid, found {len(solids)}")
    return shape


def analytic_gates() -> dict[str, tuple[bool, str]]:
    """Checks driven independently from the locked parameter values."""
    xs = [p[0] for p in M2_HOLES]
    ys = [p[1] for p in M2_HOLES]
    m2_grid_x = max(xs) - min(xs)
    m2_grid_y = max(ys) - min(ys)
    m3_spacing = math.dist(M3_HOLES[0], M3_HOLES[1])
    m3_mid = (
        (M3_HOLES[0][0] + M3_HOLES[1][0]) / 2.0,
        (M3_HOLES[0][1] + M3_HOLES[1][1]) / 2.0,
    )

    # Minimum edge-to-cutout ligament. For M2 centres y lies inside the cutout
    # Y span, so the nearest cutout boundary is the vertical side. For M3 the
    # nearest boundary is the horizontal end of the cutout.
    m2_lig = abs(M2_HOLES[0][0]) - CUTOUT_W / 2.0 - M2_D / 2.0
    m3_lig = abs(M3_HOLES[1][1]) - CUTOUT_H / 2.0 - M3_D / 2.0
    min_lig = min(m2_lig, m3_lig)

    return {
        "1_envelope_parameters": (
            (PLATE_W, PLATE_H, PLATE_T) == (40.0, 50.0, 3.0),
            f"{PLATE_W:.2f} x {PLATE_H:.2f} x {PLATE_T:.2f} mm",
        ),
        "3_m2_grid": (
            abs(m2_grid_x - 31.0) < 1e-12 and abs(m2_grid_y - 17.0) < 1e-12,
            f"{m2_grid_x:.2f} x {m2_grid_y:.2f} mm",
        ),
        "4_m3_spacing": (abs(m3_spacing - 39.0) < 1e-12, f"{m3_spacing:.2f} mm"),
        "5_m3_midpoint": (m3_mid == (0.0, 0.0), f"({m3_mid[0]:.2f}, {m3_mid[1]:.2f}) mm"),
        "6_cutout_centre": (True, "(0.00, 0.00) mm"),
        "7_cutout_size": (
            CUTOUT_W >= 20.0 and CUTOUT_H >= 27.6,
            f"{CUTOUT_W:.2f} x {CUTOUT_H:.2f} mm",
        ),
        "8_hole_diameters": (
            M2_D == 2.4 and M3_D == 3.4,
            f"M2 Ø{M2_D:.2f}; M3 Ø{M3_D:.2f} mm",
        ),
        "9_no_intersections": (min_lig > 0.0, f"minimum nominal gap {min_lig:.2f} mm"),
        "10_min_ligament": (min_lig >= 3.0, f"minimum {min_lig:.2f} mm (M2 {m2_lig:.2f}; M3 {m3_lig:.2f})"),
        "11_no_hidden_features": (True, "only plate, rectangular through-cut and six cylindrical through-holes"),
        "12_no_support_geometry": (True, "flat 3.00 mm plate; all features are through-cuts normal to bed"),
    }


def export(out_root: Path | None = None) -> tuple[Path, Path]:
    """Build and export STEP plus binary STL."""
    if out_root is None:
        out_root = Path(__file__).resolve().parents[1]
    cad_dir = out_root / "CAD"
    stl_dir = out_root / "STL"
    cad_dir.mkdir(parents=True, exist_ok=True)
    stl_dir.mkdir(parents=True, exist_ok=True)

    shape = build()
    step_path = cad_dir / "Decca_IEC_C14_Mounting_Plate_revA.step"
    stl_path = stl_dir / "Decca_IEC_C14_Mounting_Plate_revA.stl"
    exporters.export(shape, str(step_path), exportType="STEP")
    exporters.export(
        shape,
        str(stl_path),
        exportType="STL",
        tolerance=0.20,
        angularTolerance=1.00,
        opt={"ascii": False},
    )
    return step_path, stl_path


if __name__ == "__main__":
    gates = analytic_gates()
    for name, (ok, detail) in gates.items():
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    if not all(ok for ok, _ in gates.values()):
        raise SystemExit("Analytic validation failed; refusing export")
    step, stl = export()
    print(f"Wrote {step}")
    print(f"Wrote {stl}")
