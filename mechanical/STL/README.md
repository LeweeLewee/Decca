# STL

Print-ready meshes exported from the CAD sources.

**Intended contents**
- `.stl` (or `.3mf`) files ready to slice and print.
- Optional print notes (orientation, supports, material) alongside each part.

**Conventions**
- STLs are derived artefacts — the editable source lives in `../CAD/`.
- Name files to match their CAD source and revision.

## Display mount

- `Rear_Display_Carrier_revO.stl` — current. Print seating face (the flat face
  with the two bolt bosses) **down** on the bed, no supports. PETG/PETG-HF.
- `Front_Bezel_revN.stl` — current. The bezel is unchanged at Rev O.
- `Rear_Display_Carrier_revN.stl`, `Retainer_Bar_revN.stl` — superseded by
  Rev O; the retainer bar no longer exists.
