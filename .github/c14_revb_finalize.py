#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re


def insert_after_title(path: str, marker: str, block: str) -> None:
    p = Path(path)
    text = p.read_text()
    if marker in text:
        return
    i = text.find('\n\n')
    if i < 0:
        raise RuntimeError(f'Cannot locate title break in {path}')
    p.write_text(text[:i+2] + block.rstrip() + '\n\n' + text[i+2:])


cad_block = '''## IEC C14 mounting plate — Rev B — ACTIVE PROTOTYPE / PHYSICAL FIT PENDING

**Rev A is rejected.** Rev B replaces the rectangular opening with the measured six-sided C14 profile.

| File | Role |
|---|---|
| `Decca_IEC_C14_Mounting_Plate_revB_cadquery.py` | controlling parametric Rev B source |
| `Decca_IEC_C14_Mounting_Plate_revB_verify.py` | independent exported STEP/STL verifier |
| `Decca_IEC_C14_Mounting_Plate_revB_drawing.py` | dimensioned profile drawing generator |
| `Decca_IEC_C14_Mounting_Plate_revB.step` | neutral Rev B CAD export |

Measured native profile: **27.14 × 19.50 mm**, **16.00 mm short flat**, **14.00 mm straight side**, with each angled section derived as **5.57 mm run × 5.50 mm rise = 44.638°**. Nominal inlet corners are **R2.00** at the two long-flat corners and **R0.40** at the other four. Production opening uses **0.25 mm normal clearance** and is rotated 90° in the plate.

**15/15 Rev B exported-geometry checks PASS.** Physical fit remains mandatory before release.

### Rev A — REJECTED

The Rev A source and exports are retained for traceability only. Its 20.00 × 27.60 mm rectangular opening does **not** properly enclose the physical C14 profile and must not be printed or installed.'''

stl_block = '''## IEC C14 mounting plate — Rev B — ACTIVE PROTOTYPE

| File | Print notes |
|---|---|
| `Decca_IEC_C14_Mounting_Plate_revB.stl` | **Use this prototype; do not use Rev A.** PETG minimum; 0.20 mm layers; 4+ perimeters; 100% infill; broad face on bed; no supports. The opening follows the measured six-sided C14 profile with 0.25 mm normal clearance. |

Status is **CAD PASS / physical fit pending**. Confirm socket-profile enclosure, M3/M2 alignment, flat clamping and rear-terminal/wire clearance before release.

### Rev A — REJECTED

`Decca_IEC_C14_Mounting_Plate_revA.stl` is retained only as the failed prototype record and must not be printed for installation.'''

drawings_block = '''## IEC C14 mounting plate — Rev B — ACTIVE / PHYSICAL FIT PENDING

**Rev A is rejected following physical review. Rev B is the active design.**

| File | Role |
|---|---|
| `Decca_IEC_C14_Mounting_Plate_Spec_revB.md` | controlling corrected-profile specification |
| `Decca_IEC_C14_Mounting_Plate_revB_Build_Report.md` | Rev B exported-geometry validation record |
| `Decca_IEC_C14_Mounting_Plate_revB_views.png` | dimensioned measured-profile and installed-orientation view |
| `Decca_IEC_C14_Mounting_Plate_revA_Build_Report.md` | rejected Rev A physical-failure record retained for traceability |

Rev B uses the complete six-sided inlet profile defined by 27.14, 19.50, 16.00 and 14.00 mm measured datums, calculated **44.638°** angled sides, R2.00 long-flat corners and R0.40 remaining corners. **15/15 CAD checks PASS; prototype fit is still required.**'''

revision_block = '''## 2026-09-06 — IEC C14 mounting plate Rev B corrects rejected Rev A

- Owner physical review **rejected Rev A**: the rectangular opening passed the written CAD gates but did not properly enclose the actual IEC C14 shape.
- Corrected the specification error by making the previously supplied **16.00 mm** and **14.00 mm** measurements governing profile datums alongside the **27.14 × 19.50 mm** overall measurements.
- Derived each angled section as **5.57 mm run × 5.50 mm rise = 7.828 mm at 44.638°**; nominal corners are **R2.00** at the two long-flat corners and **R0.40** at the other four.
- Built Rev B with **0.25 mm normal profile clearance**, retaining the exact 31 × 17 mm Decca grid and 39 mm C14 fixing pitch. Exported STEP/STL pass **15/15** checks; minimum fixing-to-opening ligament is **3.98 mm**.
- Status: **Rev A rejected; Rev B CAD PASS / physical prototype fit pending**.'''

insert_after_title('mechanical/CAD/README.md', '## IEC C14 mounting plate — Rev B — ACTIVE PROTOTYPE / PHYSICAL FIT PENDING', cad_block)
insert_after_title('mechanical/STL/README.md', '## IEC C14 mounting plate — Rev B — ACTIVE PROTOTYPE', stl_block)
insert_after_title('mechanical/Drawings/README.md', '## IEC C14 mounting plate — Rev B — ACTIVE / PHYSICAL FIT PENDING', drawings_block)
insert_after_title('docs/Revision History.md', '## 2026-09-06 — IEC C14 mounting plate Rev B corrects rejected Rev A', revision_block)

# Mark the superseded Rev A spec clearly without deleting the historical inputs.
p = Path('mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_Spec_revA.md')
text = p.read_text()
warning = '> **REJECTED 2026-09-06:** Physical review showed that the rectangular Rev A opening does not properly enclose the IEC C14 profile. **Do not build or install Rev A.** The controlling design is now `Decca_IEC_C14_Mounting_Plate_Spec_revB.md`.\n\n'
if warning not in text:
    i = text.find('\n\n')
    p.write_text(text[:i+2] + warning + text[i+2:])

# Replace hashes in the Rev B report with the clean GitHub build outputs.
report = Path('mechanical/Drawings/Decca_IEC_C14_Mounting_Plate_revB_Build_Report.md')
text = report.read_text()
for label, path in {
    'CadQuery source': Path('mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revB_cadquery.py'),
    'STEP': Path('mechanical/CAD/Decca_IEC_C14_Mounting_Plate_revB.step'),
    'STL': Path('mechanical/STL/Decca_IEC_C14_Mounting_Plate_revB.stl'),
}.items():
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    text = re.sub(rf'^- {re.escape(label)}: `[^`]+`$', f'- {label}: `{digest}`', text, flags=re.M)
report.write_text(text)
