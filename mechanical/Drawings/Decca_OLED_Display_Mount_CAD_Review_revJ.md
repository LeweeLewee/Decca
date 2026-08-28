# Decca OLED Display Mount — CAD Build Review (Rev J)

Supersedes Rev I. Retaining lip completed with a lead-in ramp; end walls restored to full height.
Platform: Autodesk Fusion 360, script-generated parametric build.

---

## 1. Solder pin interference — solved by removing the question

Three revisions have now been spent arguing about *which end* the header sits on, and two
prints lost to getting it wrong. Rev I stops arguing.

**Both ends now have a full through cut-out**, 16.00 mm wide, full depth through the
2.30 mm front plate. The shallow 0.60 mm recess is gone entirely — there is no longer a
"wrong end" to get wrong, and the board fits either way up.

**This costs almost nothing.** A 0.60 mm recess already sits clear of the PCB face, so it
was contributing **zero** bearing. Converting it to a through cut-out is free; the only
real cost is widening it from 12.00 to 16.00 mm to match the other end, which is
**6.4 mm² of bearing** (99.4 → 93.0).

Rearward pin clearance is cut through **both** tray walls to match, so a projecting header
and its cable have a clear exit whichever end they land at.

Verified by modelling solder tips 2.00 mm proud at **both** PCB edges simultaneously:
**both CLEAR**.

---

## 2. Retention

### 2.1 Thicker nose on the sprung pegs

| | Rev G | **Rev H** |
|---|---:|---:|
| Barb Ø | 3.20 | **3.35** |
| Radial hook | 0.100 | **0.175 mm** |
| Peak bending strain | 1.64% | **2.87%** |

75% more grip, still comfortably inside PETG. Room to go further to Ø3.40 (0.20 mm hook,
3.3% strain) if it still feels light.

### 2.2 All four sprung is not possible — here is why

I tried. The two holes at the narrow end sit **0.70 mm** from the display window edge.

A durable sprung peg needs the Ø4.80 counterbore relief that lets its root fillet sit
*forward* of the PCB datum — without it, a root fillet lifts the board off its datum (the
Rev C fault) and pushes the glass into the Perspex. That relief needs 2.40 mm of radius
around the hole. There is 0.70 mm.

Building the peg without the relief gives a **short, unfilleted** peg:

| | Wide-end peg | Narrow-end peg (no relief) |
|---|---:|---:|
| Free flex length | 3.10 mm | **2.10 mm** |
| Peak strain at 0.175 hook | 2.87% | **6.25%** |

6.25% is past PETG yield. That is the Rev B geometry that snapped, and it would snap
again. So the answer is not four identical pegs.

### 2.0 End walls restored to full height (Rev J)

Rev I cut a notch through both outside tray walls for rearward pin clearance. It was never
needed: the header sits ~0.50 mm *inside* the cavity, and its pins project straight back
past a tray only 5.80 mm deep, so they clear the walls entirely. Both notches removed —
**both end walls are now full height**, verified at the rear face.

### 2.3 What replaces it — a sprung retaining lip

**Yes — the bar is a retainer, and it is there instead of four sprung pegs**, for the
reason in §2.2. Rev J finishes it properly.

**What was missing: a lead-in ramp.** As built in Rev H/I the lip presented a square face
to the incoming board — it had nothing to cam it open, so it would have fought insertion
rather than snapping. The lip now tapers **28.1° over 1.50 mm**, going from full overlap
at the PCB rear plane to zero at the tip, while the **retaining face stays square** so it
still holds once seated.

Measured off the finished solid rather than assumed:

| Depth behind the PCB rear plane | Lip overlap onto the board |
|---|---:|
| 0.05 mm (retaining face) | **0.77 mm** |
| 0.75 mm (mid ramp) | 0.40 mm |
| 1.45 mm (tip) | **0.03 mm** |

That is a proper cam: the board meets almost nothing at the tip and progressively pushes
the lip aside as it seats. Insertion-corridor volume drops 32.31 → **16.67 mm³** as a
direct result.

Also completed: the lip is now embedded 0.35 mm into its legs rather than 0.15 mm, giving
a solid joint and removing the last sub-0.15 mm edges.

**Spring behaviour**, from the finished section (1.45 × 1.50 mm, 26 mm span):

| | |
|---|---:|
| Peak strain at full deflection | **1.03%** |
| Centre-load spring force (PETG, E≈2000 MPa) | **≈6.7 N** |

To release the board, push the lip outward with a small screwdriver — there is 3.10 mm of
flex gap behind it.

A single leaf spring across the narrow end, retaining the board where a peg cannot:

| | |
|---|---:|
| Span | 26.00 mm |
| Section | 1.20 mm thick × 1.50 mm |
| Overlap onto the PCB rear face | 0.80 mm |
| Flex gap behind it | 3.30 mm |
| Peak strain at full deflection | **0.85%** |

**Why this does not repeat the Rev C failure.** In Rev C the spring's anchor legs sat
rigidly behind the PCB's corners, inside the insertion path, and the board could not go in
at all. Here the legs sit at y +13.05…+16.50 against a PCB edge at +12.75 — **entirely
outside the PCB footprint**. Only the sprung lip itself overlaps, and it is meant to
deflect.

Verified with the insertion-corridor sweep: the PCB's solid area swept in, mounting holes
excluded, meets **32.31 mm³** of carrier — the two snap noses and the sprung lip, and
nothing else. Every obstruction in the path is a spring.

**Result: retention at both ends** — two sprung pegs with a thicker nose at the header
end, one sprung lip at the far end, plus the two plain posts still locating.

---

## 3. Validation

| Pair | Result |
|---|---|
| Carrier × glass / active area / PCB / solder tips / header / Perspex / bezel | **all CLEAR** |

| Check | Result |
|---|---:|
| Glass → Perspex | 0.300 mm |
| PCB datum bearing | 93.0 mm² |
| Insertion corridor | sprung features only |
| Both cable-tie paths | CLEAR |
| Seats on the Perspex plane | yes |
| Carrier | 56.50 × 48.35 × 6.20 mm, 3.836 cm³, solid |

**Sliver audit:** the 0.05 and 0.10 mm crescents from the stadium clamp and the flange
blend are gone. Four 0.1500 mm edges remain — these are the *deliberate* 0.15 mm merge
overlap where the lip enters its legs, not boolean artifacts, and they sit below one
extrusion width so they will not print.

---

## 4. Still open

1. **`oled_active_off_y` = 4.00 mm is still assumed.** Light the display and report how
   many mm high or low the lit area sits.
2. **Firmware must mask 2 pixel rows top and bottom.**
3. **Bezel retention is adhesive** — mechanical clipping is blocked by the glass. Recessed
   pads are provided. The alternative is clamping the bezel under the M2 bolt heads, which
   breaks §4 and §12.
4. **Snap force** — if the 0.175 mm hook still feels light, `snap_barb_d` goes to 3.40.
5. **Lip force** — if the lip is too stiff to fit the board past, drop `lip_overlap` from
   0.80; if too weak, raise `lip_t` from 1.20.

---

## 5. Print guidance

PETG / PETG-HF. Carrier: Perspex seating face down, no supports. Bezel: cosmetic face down.
0.2 mm layers, 4 perimeters, ~40% infill.

Hardware: 2 × M2 heat-set insert (Ø3.2 × 4.0), 2 × M2 × 8 bolt, 1–2 cable ties, thin
removable double-sided strip for the bezel.
