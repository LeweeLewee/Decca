# Decca OLED Display Mount — Rev P Topology Review (pre-CAD gate)

Stage 1 deliverable required by `Decca_OLED_Display_Mount_CAD_Review_revO.md` §11.
No Fusion geometry may be generated until this section is clean.

Baseline: `main` @ `525c257`. Rev N is the last validated CAD. The closed Rev O
implementation branch contributes **no geometry and no design decision** — only
two negative lessons, recorded in §9.

---

## 1. Side section — the load path and the optical chain

Section on the plane x = +10.00 (through a snap finger), looking along −X.
`+Z` is forward, out of the fascia. `z = 0` is the rear face of the Perspex.

```text
                        FRONT (viewer)
   ═══════════════════════════════════════════════════════   z = +3.00
        M2 screw head bears here          ORIGINAL PERSPEX 3.00 mm
   ═════════════╤═════════════════════════════════╤═══════   z =  0.00   ◄── DATUM A
                │                                 │              carrier hard stop
                │      ← controlled optical gap →  │              (seating plane)
                │            0.30 mm              │
                │   ┌───────────────────────┐     │
                │   │      OLED GLASS       │     │           z = −0.30  glass front
   ┌────────────┤   │   (0.80 proud of PCB) │     ├────────┐
   │  CARRIER   │   ├───────────────────────┤     │CARRIER │  z = −1.10  PCB front face
   │    RIM     │   │       OLED PCB        │     │  RIM   │  z = −1.20  fwd material limit
   │  (3.00)    │   │        1.60 mm        │     │ (3.00) │  pocket wall from −1.20
   │            │▐  └───────────────────────┘  ▌  │        │
   │            │▐══════════════════════════════▌ │        │  z = −2.70  ◄── DATUM B
   │            │▐   snap-finger shoulders      ▌ │        │   REAR SUPPORT / Z DATUM
   │            │▐      (0.40 overlap)         ▌ │        │
   │            │ ▐  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐    ▌  │        │
   │            │ ▐  │  header + wiring  │    ▌  │        │   open rear access
   │            │ ▐  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘    ▌  │        │
   │  M2 boss   │  ▐ cantilever root  ▌         │        │   z = −8.40  finger root
   │  + insert  │                                │        │
   └────────────┴────────────────────────────────┴────────┘   z = −9.60  carrier rear
                        REAR (cabinet)                        z = −10.80 header extent

   ▐▌ = the four sprung snap fingers.  They lie ENTIRELY at z ≤ −1.20.
```

**M2 load path** — one path, and it never touches the module:

```text
M2 screw head → Perspex front face → Perspex (3.00) → Perspex rear face
              → carrier seating rim + annular boss pad  (z = 0, DATUM A)
              → M2 boss → heat-set insert → screw thread
```

The forward-most carrier material anywhere is z = 0. The forward-most module
material is the glass front face at z = −0.30. **The carrier bottoms out on the
Perspex 0.30 mm before anything can reach the glass, and 1.10 mm before anything
can reach the PCB.** Screw torque therefore cannot alter OLED depth, cannot
preload the glass and cannot preload the PCB. There is no series path
screw → carrier → PCB → glass → Perspex, because the carrier and the module are
in *parallel*, not in series.

---

## 2. Plan view — how the PCB is located in X/Y

Rear view (looking forward, −Z), so +X is to the left of the page as drawn from
behind. Dimensions are the model's, in the aperture-centre frame.

```text
                    y = +30.60  ┌───────────────────────────────┐
                                │   cable-tie flange  ▭     ▭   │  tie slots x ±10.50
                    y = +24.60  ├───────┬───────────────┬───────┤
                                │       │ wire notch    │       │  14.0 × 1.5 rear-open
                    y = +21.60  │   ┌───┴───────────────┴───┐   │  ◄ aperture edge
                    y = +21.00  │   │ ▐▌            ▐▌      │   │  ◄ pocket wall
                                │   │  ▲ finger      ▲      │   │    fingers x ±10.00
                    y = +20.75  │   ├──┴─────────────┴──────┤   │  ◄ PCB top edge
                                │   │   ┌───────────────┐   │   │
                                │   │   │  header body  │   │   │  x ±5.00
                                │   │   └───────────────┘   │   │
                                │   │                       │   │
   ●  M2 x = −24.50             │   │      OLED  PCB        │   │             M2 x = +24.50  ●
   y = 0 ────────────────────────   │     35.40 × 33.50     │   ────────────────────── y = 0
                                │   │   centre y = +4.00    │   │
                                │   │  ┌─────────────────┐  │   │
                                │   │  │  ACTIVE  AREA   │  │   │  29.42 × 14.70
                                │   │  │  centred (0,0)  │  │   │  ◄ OPTICAL DATUM
                                │   │  └─────────────────┘  │   │
                    y = −12.75  │   ├──┬─────────────┬──────┤   │  ◄ PCB bottom edge
                    y = −13.00  │   │ ▐▌            ▐▌      │   │
                    y = −13.60  │   └───────────────────────┘   │
                    y = −16.60  └───────────────────────────────┘
                                x = −21.55                x = +21.55
                                    (carrier rim, ±28.30 over the M2 ears)
```

**X/Y location is by the rigid pocket walls, not by the snaps.**

| | x0 | x1 | y0 | y1 |
|---|---:|---:|---:|---:|
| OLED PCB | −17.70 | +17.70 | −12.75 | +20.75 |
| PCB pocket (0.25 clearance) | −17.95 | +17.95 | −13.00 | +21.00 |
| **Module aperture** | **−18.55** | **+18.55** | **−13.60** | **+21.60** |
| Carrier rim outer | −21.55 | +21.55 | −16.60 | +24.60 |

The pocket walls engage the PCB edge over z −1.20 … −2.70 (1.50 mm of the
1.60 mm board thickness). Nothing enters the four Ø3.00 mm PCB mounting holes.

---

## 3. Retention / light-locating mechanism

Four identical sprung cantilever fingers, x = ±10.00, at the PCB top and bottom
edges. Section 0.75 mm (Y) × 4.00 mm (X). Rooted at the carrier **rear** frame
(z = −8.40) and reaching **forward** — so the whole finger, root included, lies
behind the PCB front plane.

Finger inner-face profile, at rest (top finger; bottom mirrors about the PCB edge):

| z range | inner face y | function |
|---|---:|---|
| −9.60 … −8.40 | +21.00 | rigid root, flush with the pocket wall |
| −8.40 … −3.83 | +21.00 | free cantilever length, 0.25 clear of the PCB |
| −3.83 … −2.70 | +21.00 → +20.25 | 30° insertion lead-in ramp |
| **z = −2.70** | +20.25 → +20.65 | **retaining shoulder — the rear Z datum**, 0.40 mm wide, square |
| −2.70 … −1.20 | +20.65 | tongue: 0.10 mm interference on the PCB edge → friction hold |

| Quantity | Value |
|---|---:|
| Effective cantilever length *a* | 5.70 mm |
| Deflection to pass the nose | 0.50 mm |
| Peak strain, PCB centred | **1.73 %** |
| Peak strain, PCB hard against one pocket wall (+0.25 mm) | **2.60 %** |
| Seated deflection | 0.10 mm (0.35 % strain) |
| Seated shoulder overlap on the PCB rear face | 0.40 mm |
| Insertion force (30° ramp, µ 0.30) | 2.42 N/finger → **9.7 N total** |
| Removal | press the four fingers 0.50 mm clear through the radial prise holes |
| Seated friction hold | **0.55 N** vs 0.039 N module weight → **14×** |
| PCB bending load | **none** — all four forces are in-plane and opposed |

The fingers do three things and only three things: locate Y (four opposed
springs, self-centring), hold the loose module against the rear datum by
friction, and stop it falling out of the open window while the carrier is
offered up. They are not the final retention system — §4.

---

## 4. Insertion / removal path

Pure ±Z translation. No tilt, no rotation, no lateral shift. Chosen
deliberately: Rev O died on an unchecked insertion corridor, and a pure
translation is the only motion whose swept envelope is exactly the module
cross-section extruded along Z, which makes the corridor check trivial to state
and impossible to fudge.

**Insertion** (carrier off the panel, rear face toward you):

1. Offer the PCB to the rear opening, glass forward, header at the top.
2. Push forward. The PCB front face meets the four 30° ramps at z ≈ −3.83 and
   deflects each finger 0.50 mm.
3. At z(PCB front) = −1.10 the PCB rear face clears z = −2.70; all four
   shoulders snap in behind it. The fingers relax to 0.10 mm deflection, their
   tongues gripping the PCB edge.
4. The module now rests on the four shoulders. Axial float forward = 0.30 mm,
   held closed by 0.55 N of friction against a 0.039 N module weight.

**Removal**: the retaining shoulder is square, not tapered. A release taper on a
µ = 0.30 interface is self-locking below about 17°, so any taper shallow enough
to keep a crisp Z datum would not release, and any taper steep enough to release
would spoil the datum. Instead the carrier carries four **Ø2.20 mm radial prise
holes** at z = −5.00, one per finger, opening on the outside of the rim. A 2 mm
pin pushes each finger the 0.50 mm it needs; with all four clear the module
withdraws rearward along the corridor it entered. Validated with the fingers
modelled retracted 0.55 mm.

**Final axial capture** happens only at installation: bolting the carrier to the
Perspex closes the front of the pocket. The module is then trapped between the
rear shoulders (DATUM B) and the Perspex, 0.30 mm apart, with **no preload path
in any position within that float**. This is the architecture the brief
mandates: the carrier alone does not capture the OLED.

**Swept corridor, by construction** (verified numerically in Stage 2):

| Swept body | vs carrier | why |
|---|---|---|
| OLED glass | must be CLEAR | nose tips are 6.30 mm (top) / 3.20 mm (bottom) clear of the glass in Y; pocket walls 0.70 mm clear in X |
| Solder tips | CLEAR by construction | tips lie forward of the PCB front face, where the carrier has no material inside the aperture (§5) |
| Header body | must be CLEAR | fingers are 3.00 mm clear of the header in X; pocket wall 0.25 mm clear in Y |
| OLED PCB | HIT expected | the designed 0.50 mm finger deflection, and nothing else |

---

## 5. Proof: no carrier material for retention or Z datum lies ahead of the PCB front face

Stated as a geometric invariant rather than an inspection.

> **Invariant P1.** Let `A` be the module-aperture prism
> `{ |x| ≤ 18.55, −13.60 ≤ y ≤ +21.60 }`. Then
> `Carrier ∩ A ∩ { z > −1.20 } = ∅`.

Every carrier feature satisfies P1 by construction:

| Carrier feature | z extent | X/Y position | satisfies P1 because |
|---|---|---|---|
| Seating rim / frame | 0 … −9.60 | outside `A` | never inside `A` |
| M2 bosses + ears | 0 … −9.60 | \|x\| ≥ 20.50 | outside `A` |
| Cable-tie flange | 0 … −9.60 | y ≥ +24.60 | outside `A` |
| PCB pocket walls | −1.20 … −9.60 | inside `A` | z ≤ −1.20 |
| Snap fingers, tongues, noses, shoulders | −1.20 … −9.60 | inside `A` | z ≤ −1.20 |
| Wire notch, tie slots | −8.10 … −9.60 / −4.75 … −6.25 | outside `A` | outside `A` |

> **Invariant P2.** The OLED module envelope lies strictly inside `A`:

| Module feature | −x margin | +x margin | −y margin | +y margin |
|---|---:|---:|---:|---:|
| OLED PCB | 0.85 | 0.85 | 0.85 | 0.85 |
| OLED glass | 1.30 | 1.30 | 4.55 | 7.65 |
| Solder tips (either edge) | 13.64 | 14.64 | 2.45 | 2.45 |
| Header body | 13.55 | 13.55 | 0.85 | 31.35 |

P1 ∧ P2 ⟹ **no carrier material of any kind — plate, land, lip, shoulder, snap
or datum — exists between the OLED PCB front face and the Perspex within the
OLED module envelope**, with a 0.10 mm margin. The PCB's forward datum is the
Perspex itself; its rearward datum is DATUM B at z = −2.70. Nothing else.

A corollary worth stating: because the carrier has no material forward of
z = −1.20 inside `A`, **carrier × solder-tip interference is impossible at any
tip length**. Rev N needed a relief slot for this; Rev P gets it from the
topology.

---

## 6. Resulting nominal Z-chain

| z (mm) | Feature |
|---:|---|
| +3.000 | Perspex front face — M2 heads bear here |
| **0.000** | Perspex rear face = **carrier structural hard stop (DATUM A)** |
| −0.300 | OLED glass front face — `oled_perspex_gap` |
| −1.100 | OLED PCB front face — `+ oled_glass_proud 0.80` |
| −1.200 | forward limit of all carrier material inside the aperture |
| −1.200 | pocket wall reaches full section — no chamfer needed, see the build review |
| **−2.700** | OLED PCB rear face = **rear support shoulder (DATUM B)** — `+ oled_pcb_t 1.60` |
| −8.400 | snap-finger cantilever root |
| −9.600 | carrier rear face |
| −10.800 | header rear extent (clear of the carrier) |

```text
oled_perspex_gap 0.30  +  oled_glass_proud 0.80  +  oled_pcb_t 1.60  =  2.70
```

Carrier: **56.60 W × 47.20 H × 9.60 deep**, structural wall 3.00 mm, 7.151 cm³
(9.1 g in PETG). Cable-tie flange 6.00 mm tall × 31.00 mm wide, narrowed per the
validated Rev F change.
Optical: active area 29.42 × 14.70 centred on (0, 0); aperture margin x 2.89,
y 0.30 — firmware must still mask 2 pixel rows top and bottom, unchanged from
Rev N.

---

## 7. Physical measurements — does anything block CAD?

**Nothing blocks CAD.** One item blocks *assembly*, and it is a decision, not a
measurement (§8).

| # | Item | Status | Blocks CAD? | Blocks print? |
|---|---|---|---|---|
| 1 | `oled_glass_proud` = 0.80 | measured, single sample (Rev N) | no | no — sets the chain; a second sample is 10 minutes well spent |
| 2 | Glass envelope vs the four PCB holes | **never measured** | **no — designed out** | **no** |
| 3 | `oled_active_off_y` = 4.00 | assumed | no | no — affects centring only, correctable in one parameter |
| 4 | Front-side solder protrusion | see §8 | no | **yes** |
| 5 | Anything else on the PCB front face besides glass and solder tips | assumed: nothing | no | flag for the fit test |

Item 2 was Rev O's blocking failure. Rev P removes it as a dependency: nothing
enters the PCB mounting holes, and the nearest sprung feature to the glass is
3.20 mm away in Y. The glass envelope would have to be wrong by more than
3.20 mm before it mattered. **This measurement is no longer required.**

---

## 8. The one real conflict: 1.50 mm solder tips cannot coexist with a 0.30 mm gap

This is arithmetic, not architecture, and no carrier topology can change it.

Anything standing on the PCB's front face has a budget of exactly

```text
oled_perspex_gap (0.30)  +  oled_glass_proud (0.80)  =  1.10 mm
```

before it reaches z = 0 and strikes the Perspex. Modelled at the brief's
1.50 mm, the tips reach **z = +0.40 — 0.40 mm inside the Perspex**.

| Tip proud of PCB face | Clearance to Perspex at gap 0.30 | Verdict |
|---:|---:|---|
| 0.40 | +0.70 | PASS |
| 0.80 | +0.30 | PASS |
| **1.00** | **+0.10** | **PASS — the release limit** |
| 1.10 | 0.00 | marginal, zero margin |
| 1.20 | −0.10 | FAIL |
| **1.50** | **−0.40** | **FAIL** |
| 2.00 | −0.90 | FAIL |

Reversing the load direction moved the *carrier* out of the tips' way — that part
Rev P does deliver, and unconditionally (§5 corollary). It cannot move the
Perspex.

**Three resolutions, and the one Rev P builds:**

1. **Remove the pin header; solder the four leads to the pads from the rear and
   dress the front-side joints below 1.00 mm proud.** Rev P leaves the entire
   rear of the board open, so this is easy. Optical gap stays at 0.30 mm.
   ← **built as the default**
2. Keep the header, trim the front-side pins and solder below 1.00 mm proud.
   Same geometry, same result, tighter trim than 1.50 mm.
3. Accept 1.50 mm tips and open `oled_perspex_gap` to **0.80 mm**. One parameter,
   rebuild, no topology change — but 2.7× the approved 0.15–0.30 band, and the
   screen sits visibly deeper behind the fascia.

Rev P is built at gap 0.30 with a stated assembly-preparation limit of 1.00 mm,
because the brief's governing objective is to place the glass *close* to the
Perspex. The model is validated at **both** 1.50 mm (the brief's worst case,
which fails) and 1.00 mm (the release limit, which passes), and the tip length
is a single user parameter either way.

---

## 9. What the closed Rev O branch contributes

Two negative lessons. No geometry.

1. **Do not recreate a forward retention plane.** Rev O's "short seating lands"
   at z = −1.10 were the Rev N front plate in disguise. Rev P answers this with
   invariant P1 (§5), a machine-checkable statement rather than an intention.
2. **A static final-position matrix proves nothing about assembly.** Rev O's
   19-point probe, load path, clearance table and screenshots were all clean
   while the module could not physically be inserted. Rev P checks the swept
   corridor in both directions, and — more importantly — is *designed* so the
   corridor is clear by construction (§4, §5).

A third, structural lesson: Rev O put barbs through the PCB mounting holes,
which made an unmeasured glass-envelope dimension load-bearing on the whole
design. Rev P takes no feature into those holes at all.

---

## 10. Self-review verdict

| Gate | Result |
|---|---|
| Rear-loaded, carrier behind the PCB | PASS |
| No front plate / land / lip / shoulder / PCB datum forward of the PCB face | PASS — invariant P1, 0.10 mm margin |
| OLED Z position from rear PCB support | PASS — DATUM B, z = −2.70 |
| Separate carrier-to-Perspex hard stops carrying all M2 preload | PASS — DATUM A, z = 0, outside the module envelope |
| Not captured by the carrier alone | PASS — 0.30 mm float; the Perspex closes the pocket |
| Snaps locate and lightly retain only | PASS — 0.55 N friction hold, 0.40 mm shoulder |
| Glass never sweeps a rigid post or barb | PASS — 3.20 mm minimum clearance, no feature in any PCB hole |
| No separate retainer bar | PASS — deleted |
| Sections 2–3 mm where geometry allows | PASS — 3.00 mm wall; 0.75 mm fingers are springs by intent |
| Blocking measurement gap | NONE |
| Blocking conflict | ONE — §8, front-side solder protrusion |

**Topology approved for CAD.** Proceed to the Fusion 360 build.
