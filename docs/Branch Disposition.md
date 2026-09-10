# Branch disposition register

> Current baseline: `main` at or after `5688321`, firmware v0.27.4. This register
> records the content review completed on 2026-09-10 before branch cleanup.
> Topic branches listed here must not be merged into current main: several carry
> superseded firmware, pin maps, mechanical revisions or procurement states.

| Remote branch | Disposition on current main |
|---|---|
| `claude/decca-display-bezel-revq` | Fully represented by the later, signed-off Rev Q package already on main. Branch is an ancestor and has no unique commit. |
| `claude/decca-display-mount-revo-swui8k` | Rev O is superseded by the released, installed and physically tested Rev P.5 carrier. Its branch-only intermediate artifacts are intentionally not current deliverables. |
| `claude/decca-display-mount-revp` | Fully represented by the released Rev P.5 package on main. Branch is an ancestor and has no unique commit. |
| `codex/spec-display-bezel-revq` | Its requirements are represented by the later signed-off Rev Q specification, source, exports and physical evidence on main. The two branch commits are superseded intermediate specification work. |
| `diagnostic/adc-pwm-noise` | The completed report, device summary and 12,000-row raw capture are retained under `diagnostics/`. Diagnostic-only source hooks are intentionally excluded because they depend on the v0.27.1 fade API and former GPIO25 lighting route; they are not production firmware. |
| `docs/reconcile-open-components` | Current parts, wiring, architecture and BOM documents now reflect later procurement and installation evidence. The branch's earlier open-component snapshot is superseded. |
| `docs/reconcile-selected-components-20260829` | Later selected-component states are represented in current parts/BOM documents. The branch snapshot is superseded. |
| `docs/record-amazon-dc-socket-20260829` | Purchase history is retained, while current documents record that the TopHomer socket became obsolete after the Phihong low-voltage lead was soldered directly into the Decca wiring. |
| `docs/select-phihong-5v-supply` | The Phihong PSA15R-050P selection is retained and current documents record its installed direct-solder shared-rail state. |
| `feat/esp32-controller-housing-cad` | Rev C source, F3D/STEP/STL exports, specification v1.7, Rev B/Rev C reports and all Rev C renders were selectively copied to main. Main records the owner's 2026-09-07 print, fit, wiring and installation, plus the remaining prototype/installation gates. No branch firmware was merged. |
| `feat/iec-c14-mounting-plate` | Rev A rejection evidence and the full active Rev B source, STEP/STL, specification, report and drawings were selectively copied to main. Rev B is 15/15 CAD-passed and profile-confirmed, with physical fit pending. |
| `feature/reassign-control-gpios` | Superseded by the final GPIO14 on/off, GPIO26 VHF, GPIO25 Stereo/Mono and GPIO18 lighting mapping and by v0.27.4 immediate lighting transitions. Its older firmware must not be merged. |
| `fix/esp32-pin-reassignment-d26-d14` | Fully represented in current main; branch is an ancestor and has no unique commit. |

Remote branch deletion does not authorise discarding uncommitted files in local
worktrees. Local worktrees must be reviewed separately and only removed after
their exact dirty paths are explicitly accepted for discard or preservation.
