# PCB

PCB layouts and fabrication outputs for any **new** boards (e.g. a controller
carrier board), plus documentation of retained original boards.

> **Retained original selector PCB.** The original radio/source selector PCB is
> **retained in place as the mechanical carrier** for the interlocked selector
> mechanism (see ADR-0001 and `docs/Wiring.md`). It is **not disposable** and is
> not re-fabricated. Only its existing usable contact pairs are tapped.

**Intended contents (new boards only)**
- Source layout files (e.g. KiCad `.kicad_pcb`).
- Gerbers and drill files (zipped per revision) for fabrication.
- Optional 3D exports (STEP) for mechanical fit checks.

**Conventions**
- One subfolder or zip per fabrication revision; never overwrite a released set.
- Cross-reference the matching schematic revision.
