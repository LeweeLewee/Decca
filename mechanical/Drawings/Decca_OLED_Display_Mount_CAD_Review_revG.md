# Decca OLED Display Mount — CAD Build Review (Rev G)

Supersedes Rev F. Mounting orientation corrected, bezel location and retention reworked,
boolean slivers removed.
Platform: Autodesk Fusion 360, script-generated parametric build.

---

## 1. Mounting orientation corrected — the layout is mirrored

Confirmed: with the Decca upright and the display reading the right way up, the four
header wires exit **above** the window. Every revision up to F had the header below it.

This is not a local fix. The header edge determines where the wide bare-PCB strip sits,
which in turn sets the cavity, the display window and the glass position. The whole
carrier mirrors.

Implemented by building in the old frame and rotating **180° about Z**. The part is
symmetric in X, so that is exactly a Y-mirror, and it guarantees every feature moves
together — no chance of one sign flip being missed.

| | Rev F | **Rev G** |
|---|---:|---:|
| PCB centre | y −4.00 | **y +4.00** |
| Header edge | y −20.75 | **y +20.75** |
| Active-area centre | 0.00 | **0.00** (unchanged — it is the datum) |
| Header through cut-out | lower strip | **upper strip, y +14.45…+21.25** |
| Shallow recess | upper | **lower, y −13.25…−9.55** |
| Tie flange + anchors | lower edge | **upper edge, beside the cable exit** |

The tie anchors moving to the header edge is a real gain — the strain relief is now
where the cable actually leaves the board, instead of 40 mm away at the far end.

**Header relief per your instruction:** the wide upper strip gets the full **through
cut-out** (16.00 mm wide); the lower strip reverts to a **0.60 mm shallow recess**
(12.00 mm wide). Verified: solder tips modelled 2.00 mm proud are **CLEAR** of the
carrier on the header side.

---

## 2. Bezel — location fixed, retention is adhesive by necessity

### 2.1 Why the lip would not enter

The four corner blocks sat exactly where the opening's corner radii are. Any radius at
all and they foul before the bezel is home.

**Replaced with two side rails**, x ±15.30…17.45 (2.15 mm wide), y ±4.00, 2.80 mm deep,
0.15 mm clearance per side. Nothing within **3.65 mm** of a corner, so the design
tolerates a corner radius up to R3.65.

Tested against modelled openings with **R1.5, R2.0 and R3.0** corners — bezel enters
clear in all three.

### 2.2 Retention — mechanical clip-in is not possible

Checked before falling back to adhesive. Anything that clips must reach *behind* the
Perspex, and the OLED glass sits **0.30 mm** behind the panel spanning ±17.25 of a
±17.60 opening:

- legs down the sides → hit the glass (0.35 mm of margin per side)
- a barb snapping behind the panel → hits the glass
- top and bottom → only 0.20 mm of margin

There is no path through the opening that clears the glass. Spec §4 anticipated exactly
this: *"removable/light adhesive may be used only if required after physical fit
testing."* We have now done that testing.

**Provided:** two recessed pads, 24.00 × 2.00 mm and 0.30 mm deep, in the fascia contact
ring top and bottom, for a thin removable double-sided strip. The recess keeps the glue
line off the fascia surface and the tape thickness out of the seating plane.

**The one positive mechanical alternative** is extending the bezel out under the M2 bolt
heads. It works, but it breaks §4 (*bezel independent of the structural fixing bolts*)
and §12 (*fixing bolts remain visually separate*). Not implemented — say the word.

---

## 3. Boolean slivers removed

Two causes, both mine:

1. The tie flange's rounded top corner meant the concave blend met a **curved** face
   where it assumed a flat one. Fixed by squaring the flange's buried top 4.00 mm.
2. The rounded-prism helper clamped the corner radius **0.05 mm short** of a true
   stadium, leaving hairline flats where the arm ends met the bosses. Fixed to handle
   `r == half-span` exactly.

Blend solids now also overlap their mating faces by 0.08 mm rather than meeting
coincidentally.

**Tiny-edge count (edges under 0.15 mm): 10 → 0.** Arm ends are a true R3.75 stadium
concentric with the Ø7.50 bosses.

---

## 4. Validation

| Pair | Result |
|---|---|
| Carrier × glass / active area / PCB / solder tips / header / Perspex / bezel | **all CLEAR** |
| Bezel × Perspex / glass | **CLEAR** |
| Bezel vs openings with R1.5 / R2.0 / R3.0 corners | **enters clear** |

| Check | Result |
|---|---:|
| Active-area centre | X +0.0000, Y +0.0000 |
| Header keep-out | y +17.75…+20.75 (above the window) ✓ |
| Glass → Perspex | 0.300 mm |
| Both cable-tie paths | CLEAR |
| Seats on the Perspex plane | yes |
| Tiny edges | 0 |
| Carrier | solid, 3.408 cm³ |

**PCB datum bearing 117.9 → 99.4 mm²** on the same measure, because the through cut-out
now falls on the wide strip rather than the narrow one. Still carried on both edges plus
the side ledges, and ample for a board this light — but it is the one number that got
worse in this revision, so it is worth a look on the print.

---

## 5. Still open

1. **`oled_active_off_y` = 4.00 mm is still assumed** (now applied as −4.00 in the
   mirrored frame). With this print, light the display and report how many mm high or
   low the lit area sits.
2. **Firmware must mask 2 pixel rows top and bottom.** The 15.30 mm opening leaves only
   0.60 mm total against a 14.70 mm active area.
3. **Solder tip length** — front plate is 2.30 mm and seats on the Perspex; tips longer
   than that reach the panel through the cut-out.
4. **Bezel corner radius** — worth measuring; the rails tolerate up to R3.65.

---

## 6. Print guidance

PETG / PETG-HF. Carrier: Perspex seating face down, no supports. Bezel: cosmetic face
down; the 2.80 mm rails print upward. 0.2 mm layers, 4 perimeters, ~40% infill.

Hardware: 2 × M2 heat-set insert (Ø3.2 × 4.0), 2 × M2 × 8 bolt, 1–2 cable ties,
and a thin removable double-sided strip for the bezel.
