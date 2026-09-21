# Architecture Decision Records (ADRs)

Short, immutable records of significant decisions. Each ADR captures the context,
the decision, and its consequences at the time it was made. Supersede rather than
rewrite: if a decision changes, add a new ADR and mark the old one `Superseded`.

Format: lightweight (Nygard). Status is one of `Proposed`, `Accepted`,
`Superseded`, `Deprecated`.

| ADR  | Title                                                       | Status   |
|------|-------------------------------------------------------------|----------|
| 0001 | Retain the original selector PCB as mechanical carrier      | Accepted |
| 0002 | Use four 10k analogue potentiometers as position sensors    | Accepted |
| 0003 | Reuse the original on/off switch and cable as a low-voltage input | Accepted |
| 0004 | Reuse VHF, MW, LW and Gram; defer SW                        | Superseded |
| 0005 | Leave Stereo/Mono unwired in Phase 1                        | Superseded |
| 0006 | Keep WiiM Pro integration in Phase 2                        | Accepted |
| 0007 | Present logical function and now-playing context            | Accepted |
| 0008 | Lock WiiM Pro with separate power amplification             | Accepted |
| 0009 | Omit legacy button labels from user-facing display views    | Accepted |
| 0010 | Lock Fosi ZA3 and system power-control architecture         | Accepted; lighting transitions superseded by 0017 and trigger implementation by 0018 |
| 0011 | Use Gram as the sole two-state source selector               | Superseded |
| 0012 | Use authenticated local-network ArduinoOTA                   | Accepted |
| 0013 | Use VHF as the authoritative two-state source selector       | Superseded |
| 0014 | Use TX2 Stereo/Mono as the dial-lighting command              | Superseded |
| 0015 | Reassign dry-contact inputs for terminal-adapter routing      | Superseded |
| 0016 | Finalise controller GPIO routing                              | Accepted |
| 0017 | Remove dial-lighting fades                                    | Accepted |
| 0018 | Use the WiiM Pro trigger output for the ZA3                    | Accepted |
