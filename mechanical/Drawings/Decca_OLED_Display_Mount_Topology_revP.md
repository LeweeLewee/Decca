# Decca OLED Display Mount — Rev P Topology Review (pre-CAD gate)

Stage 1 deliverable required by `Decca_OLED_Display_Mount_CAD_Review_revO.md` §11.
No Fusion geometry may be generated until this section is clean.

> **Rev P.2 — CORRECTED 2026-08-29 after a physical retention failure.**
> The printed Rev P.1 carrier failed its retention test: the OLED falls forward
> through the loose carrier. The failure is **architectural, not a tolerance
> adjustment**. §0 records it; §1–§10 are the corrected topology and supersede
> the Rev P.1 text entirely.
>
> **Rev P.2 then PASSED physically** for OLED retention and Perspex tolerance.
> §1–§10 therefore describe validated hardware and are carried forward
> unchanged.
>
> **Rev P.3 — BOUNDED AMENDMENT 2026-08-29.** Two integration failures against
> the radio, neither touching the validated OLED architecture:
>
> - **§11** the continuous end rail and its cable-tie projection collide with
>   the retained original Decca lighting unit and are deleted;
> - **§12** the original front bolts have a non-standard thread, so the whole M2
>   heat-set-insert architecture is deleted and the original bolts and their
>   matching nuts are reused with a captive hex pocket.

Baseline: `main` @ `53071ff`, whose §8.1, §8.2, §9, §10 and §12 are
authoritative over anything written on this branch before them.

---

## 0. The Rev P.1 retention failure — what actually went wrong

Rev P.1 inserted the OLED **from the rear**, moving forwards towards the
Perspex. Its four snap-finger shoulders sat at the **PCB rear plane** (z = −2.70)
and stopped motion in the **opposite** direction — rearward, back out of the
pocket. Once the board passed those shoulders there was **no positive feature of
any kind** preventing further forward travel.

The only thing holding the module in a loose carrier was four 0.10 mm edge-grip
tongues pressing on the PCB **edge**, relying on an assumed PETG friction
coefficient. The Rev P.1 gate checked:

- that the rear shoulders exist — **they do, and they restrain the wrong way**;
- that the tongues stop behind the PCB front plane — **they do, which is exactly
  why they cannot stop forward travel**;
- that computed friction (0.55 N) exceeds module weight (0.039 N) — **a
  calculation, not a geometric stop**.

Nowhere did it demonstrate a positive geometric stop against forward movement,
because there was not one to demonstrate. The physical print settled it: the
screen falls out forwards.

**Conclusion.** Friction between a printed tongue and a PCB edge is not
retention. The gate must require *geometry that physically blocks the motion*,
and the module must be inserted from the side it is restrained on.

The following are **not** acceptable fixes and are not attempted: increasing
`finger_grip`, revising the assumed friction coefficient, increasing spring
force, or adding another rear-loaded edge finger. All four leave the
architectural defect in place.

### What survives from Rev P.1

The structural half of Rev P.1 was sound and is retained unchanged: the M2 load
path in parallel with the module, the direct carrier-to-Perspex hard stop, the
0.30 mm optical chain, the ≤ 1.00 mm front-side protrusion budget, the open
rear, active-area centring, the single printed carrier plus the Rev N bezel, and
the invariant-based way of proving that nothing structural sits in front of the
PCB.

### What is deleted

The four PCB-edge friction fingers, their shoulders, their 0.10 mm tongues,
their four Ø2.20 mm radial prise holes, and the friction-versus-weight
acceptance gate. None of them appears anywhere in Rev P.2.

---

## 1. Side section — insertion direction, both axial stops, the load path

Section on the plane x = +15.00 (through a sprung locating post), looking
along −X. `+Z` is forward, out of the fascia. `z = 0` is the rear face of the
Perspex. **The module is inserted from the FRONT, moving rearward (−Z).**

```text
                        FRONT (viewer)  —  INSERTION SIDE
   ═══════════════════════════════════════════════════════════   z = +3.00
     ORIGINAL bolt head bears here          ORIGINAL PERSPEX 3.00 mm
   ═════════════╤═══════════════════════════════════════╤═════   z =  0.00  <- DATUM A
                |                                       |           carrier hard stop
                |         v  v  v  MODULE INSERTED      |           (seating plane)
                |         v  v  v  FROM THIS SIDE       |
                |                                       |
                |        <- optical gap 0.30 mm ->      |       z = −0.30  glass front
                |   ┌────────────────────────┐    /^\   |       z = −0.40  nose tip
   ┌────────────┤   |       OLED GLASS       |   /   \  |       (Ø2.60, 0.40 clear
   |            |   |   (0.80 proud of PCB)  |  | Ø3.2| |        of the Perspex)
   |  CARRIER   |   |                        |  ├─────┤ |       z = −0.75  land
   |    RIM     |   ├────────────────────────┤  ├█████┤ |       z = −1.00  <- SNAP HOOK
   |  (3.00)    |   |        OLED PCB        |  |     | |        retaining face, square,
   |            |   |        1.60 mm         |  |     | |        0.10 mm axial clearance
   |            |█  |                        |  |Ø2.80| |       z = −1.10  PCB front face
   |            |█  |                        |  |shaft| |       z = −1.20  fwd material
   |            |█  └────────────────────────┘  |     | |                  limit (rim)
   |            |█══════════════╤═══════════════╪═════╪═|       z = −2.70  <- DATUM B
   |            |█  ███████████ | FIXED DATUM   |     | |        PCB REAR FACE seats on
   |            |█  ██pedestal█ | PAD Ø6.0/Ø4.8 |     | |        FIXED, RIGID pads
   |            |█  ███████████ └───────────────┤     | |       z = −3.00  pedestal top
   |            |█  ██████████  Ø4.80 root  ████|     | |
   |            |█  ██████████     relief   ████|     | |        (the relief is now
   |  M2 boss   |█  ██████████  (3.20 deep) ████|  \_/| |         BEHIND the PCB — the
   |  + insert  |█  ████████████████████████████ \___/  |         glass cannot constrain
   |            |█  ██████████████ R0.80 fillet ────────┘         its depth any more)
   |            |█  ████████████████████████████████████  z = −5.90  post root
   |            |█  ████████████████████████████████████
   └────────────┴──█████████████████████████████████████         z = −8.00  carrier rear
                        REAR (cabinet)  —  OPEN                  z = −10.80 header extent

   █ = rigid carrier body (pocket wall / pedestal).
   The ONLY sprung element anywhere in the carrier is the split post nose.
```

### The two positive axial stops

| Direction | Stopped by | Nature |
|---|---|---|
| **Rearward** (−Z, the insertion direction) | four **fixed datum pads** at z = −2.70, rigid parts of the carrier body, concentric with the four PCB mounting holes | rigid solid-to-solid seat, no spring anywhere in the path |
| **Forward** (+Z, the direction Rev P.1 failed in) | two **sprung post hooks**, Ø3.20 barb over a Ø3.00 hole = **0.10 mm radial geometric overlap**, square retaining face at z = −1.00 | positive geometric interference — the retaining face is square and cannot cam, so an axial pull cannot release it |

Neither stop touches the glass:

- the rearward stop acts on the PCB **rear** face, 1.60 mm behind the glass;
- the forward stop acts on the PCB **front** face **inside the Ø3.00 mounting
  hole**, which is a keep-out on both faces of the board by definition;
- the glass front face is at z = −0.30 and nothing but air is in front of it.

**Neither stop is friction.** Friction plays no part in Rev P.2 retention and no
friction calculation appears in the acceptance gate.

### M2 load path — unchanged from Rev P.1

```text
ORIGINAL bolt head -> Perspex front face -> Perspex (3.00) -> Perspex rear
                   -> carrier seating rim + boss pad  (z = 0, DATUM A)
                   -> captive ORIGINAL nut -> original bolt thread

(Rev P.3: the M2 heat-set insert this line used to name is deleted - see 12)
```

The forward-most carrier material anywhere is z = 0. The forward-most module
material is the glass front face at z = −0.30. The carrier bottoms out on the
Perspex 0.30 mm before anything can reach the glass and 1.10 mm before anything
can reach the PCB. Carrier and module are in **parallel**, never in series, so
**M2 torque cannot reach the module** — it cannot alter OLED depth, preload the
glass or preload the PCB.

The snap hooks are not in the load path either: their tips stop at z = −0.40,
0.40 mm short of the Perspex, so tightening the screws never touches them.

---

## 2. Plan view — locating posts, datum pads, rear access

Rear view (looking forward, −Z). Dimensions in the aperture-centre frame.

```text
                    y = +30.60  ┌───────────────────────────────┐
                                |   cable-tie flange   ▭    ▭   |  tie slots x ±10.50
                    y = +24.60  ├───────┬───────────────┬───────┤
                                |       | wire notch    |       |  13.0 x 1.5 rear-open
                    y = +21.60  |   ┌───┴───────────────┴───┐   |  <- aperture edge
                    y = +21.00  |   |                       |   |  <- pocket wall
                    y = +20.75  |   ├───────────────────────┤   |  <- PCB top edge
                                |   |  ╭─╮   ┌───────┐  ╭─╮ |   |
                    y = +18.25  |   |  |S|   | header|  |S| |   |  <- SPRUNG POSTS
                                |   |  ╰─╯   └───────┘  ╰─╯ |   |     x ±15.00
                                |   |   ^ Ø8.6 pedestal ^   |   |
                                |   |                       |   |
   ●  M2 x = −24.50             |   |      OLED  PCB        |   |         M2 x = +24.50 ●
   y = 0 ──────────────────────-|   |     35.40 x 33.50     |   |-────────────────── y = 0
                                |   |   centre y = +4.00    |   |
                                |   |  ┌─────────────────┐  |   |
                                |   |  |  ACTIVE  AREA   |  |   |  29.42 x 14.70
                                |   |  |  centred (0,0)  |  |   |  <- OPTICAL DATUM
                                |   |  └─────────────────┘  |   |
                                |   |  ╭─╮           ╭─╮    |   |
                    y = −10.25  |   |  |P|           |P|    |   |  <- PLAIN POSTS
                                |   |  ╰─╯           ╰─╯    |   |     x ±15.00
                    y = −12.75  |   ├───────────────────────┤   |  <- PCB bottom edge
                    y = −13.00  |   |                       |   |
                    y = −13.60  |   └───────────────────────┘   |
                    y = −16.60  └───────────────────────────────┘
                                x = −21.55                x = +21.55
                                    (carrier rim, ±28.30 over the M2 ears)

   S = split SPRUNG locating post, Ø2.80 shaft / 0.70 slot / Ø3.20 barb
   P = PLAIN locating post, Ø2.70, top at z = −1.20 — never crosses the PCB
       front plane, so it is unconditionally clear of the glass
   Each post stands in a Ø4.80 root relief, on a Ø8.00 pedestal, ringed by a
   Ø6.00/Ø4.80 fixed datum pad at z = −2.70.
   Open rear window x −11.00 … +11.00, full height: header, cable, and the
   push-out path used for removal.
```

### Why the sprung pair is on the header side and the plain pair is not

The brief's default arrangement, and the reason for it, is this design's single
remaining risk:

| Hole pair | y | Modelled glass edge | Margin to a Ø3.20 nose | Post type |
|---|---:|---:|---:|---|
| Header side ("wide") | +18.25 | +13.95 | **+2.70 mm** | **sprung** |
| Display side ("narrow") | −10.25 | −9.05 | **−0.40 mm (fouls)** | **plain** |

On the modelled envelope the glass **overhangs the display-side mounting holes**.
That pair therefore gets **plain posts that stop at z = −1.20**, 0.10 mm behind
the PCB front plane. Nothing there ever crosses into glass territory, whatever
the real envelope turns out to be — the risk is removed by geometry, not by a
number.

Rev K put sprung pegs in the narrow pair on **0.20 mm of assumed glass
clearance** and called it validated. That unmeasured dependency is **not**
recreated here.

---

## 3. Locating and retaining posts — geometry and the Rev D/K inheritance

Starting values taken from the printed Rev D / Rev K post development, then
**recalculated from the finished Rev P.2 geometry** as the brief requires.

### 3.1 Sprung locating posts — x = ±15.00, y = +18.25

| z range | feature | Ø | note |
|---|---|---:|---|
| −5.90 … −5.10 | R0.80 root fillet | 2.80 → 4.40 | inside the Ø4.80 relief, top 2.40 mm behind DATUM B |
| −5.90 … −1.00 | split shaft | **2.80** | 0.10 mm radial clearance in the Ø3.00 hole |
| −1.10 … −1.00 | axial clearance zone | 2.80 | **0.10 mm** — the hook does not clamp the PCB |
| **z = −1.00** | **retaining face — square, rearward-facing** | 2.80 → **3.20** | **0.10 mm radial overlap = the forward stop** |
| −1.00 … −0.75 | full-diameter land | 3.20 | 0.25 mm, thicker than a print layer |
| −0.75 … −0.40 | insertion lead-in cone | 3.20 → 2.60 | 40.6° from the axis |
| slot | full height, 0.70 mm wide, normal to Y | | halves deflect **inward**, never outward |

### 3.2 Plain locating posts — x = ±15.00, y = −10.25

| z range | feature | Ø |
|---|---|---:|
| −3.70 … −2.90 | R0.80 root fillet | 2.70 → 4.30 |
| −3.70 … −1.65 | shaft | **2.70** (0.15 mm radial clearance) |
| −1.65 … −1.35 | entry chamfer | 2.70 → 2.10 |

Top face at z = −1.35 — **0.25 mm behind the PCB front plane**, so the plain
posts satisfy the original prohibition without needing the controlled exception
at all. 0.10 mm (the generic `forward_setback`) is too thin to trust on an FDM
post top when the modelled glass overhangs these holes; 0.25 mm costs nothing
and still engages 1.35 mm of the 1.60 mm board.

### 3.3 Reused, changed, and why

| Rev D / Rev K value | Rev P.2 | Change and reason |
|---|---|---|
| sprung shaft Ø2.80 | **Ø2.80** | reused unchanged — printed and fit-tested at Rev D |
| split slot 0.70 | **0.70** | reused unchanged |
| barb Ø3.20, 0.10 mm radial hook | **Ø3.20, 0.10 mm** | reused unchanged — the brief's starting value |
| R0.80 root fillet | **R0.80** | reused unchanged |
| plain post Ø2.70 | **Ø2.70** | reused unchanged |
| root relief ≈ 1.00 mm | **3.20 mm (sprung) / 1.00 mm (plain)** | **changed.** In Rev D/K the relief sat *in front of* the PCB, so its depth was capped by the glass — that is exactly what forced Rev K's narrow pair down to a 0.40 mm relief on 0.20 mm of assumed clearance. In Rev P.2 the relief is **behind** the PCB, where the glass cannot constrain it at all, so its depth is set by strain instead. |
| hook land (Rev D: under one print layer) | **0.25 mm** | **changed.** A retaining face thinner than a layer is not a retaining face. |
| Rev D peak strain 1.64 % (a = 3.10) | **0.83 %** (a = 4.35) | consequence of the deeper relief |
| Rev K narrow pair on 0.20 mm assumed glass clearance | **deleted** | replaced by plain posts — the dependency is removed, not re-estimated |

### 3.4 Recalculated mechanics

Cantilever half-post, fixed at the top of the root fillet (z = −5.10), loaded at
the full-diameter land (z = −0.75): free length **a = 4.35 mm**, half-section
thickness t = (2.80 − 0.70)/2 = **1.05 mm**, PETG E = 2000 MPa.

| Quantity | Value |
|---|---:|
| Deflection to pass the barb, per half | 0.10 mm |
| **Peak strain, hole centred** | **0.83 %** |
| Deflection worst case, board hard to one side | 0.20 mm on one half |
| **Peak strain, worst case** | **1.66 %** |
| Strain limit | 3.00 % |
| Radial spring force per post at 0.10 mm | ≈ 3.9 N |
| Insertion force (40.6° cam, µ 0.30) | ≈ 6.1 N per post → **≈ 12.3 N total** |
| Seated deflection | **0.00 mm — the barb clears the PCB entirely** |
| Seated radial preload on the PCB | **zero** (0.10 mm shaft clearance in the hole) |
| Seated axial preload on the PCB | **zero** (0.10 mm clearance under the hook) |
| PCB bending from retention | **none** |
| Forward retention mechanism | **positive geometric overlap**, square face, cannot cam |
| Bearing area of the two hooks | ≈ 3 mm² → far beyond a 0.039 N module |

The seated state is the important line. Once the board is home, **every spring
in the carrier is fully relaxed**. The hooks stand clear of the PCB by 0.10 mm
and the shafts clear the holes by 0.10 mm radially, so the module is held by
four rigid pads at its rear and blocked by two relaxed hooks at its front, with
nothing squeezing, bending or preloading it.

---

## 4. Fixed rear datum pads

Four annular pads, **rigid parts of the carrier body**, top face at z = −2.70:

| | |
|---|---:|
| Position | concentric with the four Ø3.00 PCB mounting holes, x ±15.00, y +18.25 / −10.25 |
| Outer Ø / inner Ø | 6.00 / 4.80 |
| Nominal annulus area | 10.18 mm² each |
| Area actually on the PCB (clipped by the 35.40 x 33.50 outline) | ≈ 8.6 mm² each, **≈ 34 mm² total** |
| Supported by | Ø8.00 pedestals, z −8.00 … −3.00, merged into the pocket walls |
| Spring content | **none** — solid carrier body throughout |

Why these four locations and no others: they sit **inside the PCB's own
mounting-hole keep-outs**, which are component-free on both faces by
construction. Every earlier revision took its PCB datum from the board edge
band, which is an assumption about where components are not. This one is not an
assumption.

They span a 30.00 x 28.50 rectangle — the widest stable four-point pattern the
board offers — so the seated board cannot rock. Loading is the ≈ 12 N insertion
push only; nothing pushes the module rearward in service. 34 mm² at 12 N is
0.35 MPa.

---

## 5. Invariant P1′ — the controlled exception, stated as geometry

Rev P.1's invariant P1 said the aperture prism is empty forward of the PCB face.
Rev P.2 needs positive forward retention, so the invariant is **tightened to name
its own exception** rather than relaxed:

> **Invariant P1′.** Let `A` be the module-aperture prism
> `{ |x| ≤ 18.55, −13.60 ≤ y ≤ +21.60 }` and let `N` be the two nose envelopes
> `{ (x ∓ 15.00)² + (y − 18.25)² ≤ 1.60², −1.20 < z ≤ −0.40 }`. Then
>
> `Carrier ∩ A ∩ { z > −1.20 }  ⊆  N`
>
> and `N` lies strictly inside the two Ø3.00 PCB mounting-hole corridors.

Everything else satisfies the original prohibition unchanged:

| Carrier feature | z extent | satisfies P1′ because |
|---|---|---|
| Seating rim / frame | 0 … −8.00 | outside `A` |
| M2 bosses + ears | 0 … −8.00 | \|x\| ≥ 20.50, outside `A` |
| Cable-tie flange | 0 … −8.00 | y ≥ +24.60, outside `A` |
| PCB pocket walls | −1.20 … −8.00 | z ≤ −1.20 |
| Post pedestals, datum pads, root reliefs | −2.70 … −8.00 | z ≤ −1.20 |
| Plain post shafts and chamfers | −1.20 … −3.70 | z ≤ −1.20 |
| Sprung post shafts | −1.00 … −5.70 | cross z = −1.20 only inside `N` |
| **Sprung post noses** | **−1.20 … −0.40** | **the declared exception `N`** |

There is still **no carrier plate, seating land, structural shoulder or other
load-bearing feature** between the PCB front face and the Perspex. `N` carries no
load, sets no datum, and touches the PCB only when the module is being pulled
forwards out of the carrier.

### What `N` must be proven clear of

| `N` vs | Result | Basis |
|---|---|---|
| the Perspex | **0.40 mm clear** — nose tip z = −0.40, Perspex z ≥ 0 | modelled from the measured 3.00 mm panel |
| the Rev N bezel | **clear** — the bezel lip lies inside \|x\| ≤ 17.45, \|y\| ≤ 7.50; `N` is at y ≈ +18.25 | Rev N geometry, unchanged |
| the active display area | **9.30 mm clear** in Y | active area 29.42 x 14.70 on (0,0) |
| solder joints / tips | **8.49 mm clear** in X | tips at x −3.91 … +4.91 |
| the insertion and removal corridor | **clear** — the corridor is a pure ±Z translation and `N` sits inside the hole corridor it is meant to occupy | §6 |
| **the OLED glass** | **NOT DEMONSTRATED — see §7** | the glass X/Y envelope has never been measured |

---

## 6. Insertion and removal

Pure ±Z translation. No tilt, no rotation, no lateral shift — the only motion
whose swept envelope is exactly the module cross-section extruded along Z.

**Insertion** (carrier off the panel, **seating face towards you**):

1. Offer the module to the **front** of the carrier, glass towards the carrier,
   header at the top. The glass enters the open module aperture, which is
   0.85 mm larger than the PCB all round.
2. The two sprung barb tips (Ø2.60 at z = −0.40) enter the two header-side
   mounting holes first and align the board.
3. The PCB rear face enters the pocket at z = −1.20 (0.25 mm clearance).
4. The barbs cam inward 0.10 mm per half against the hole walls; the plain posts
   enter the display-side holes.
5. The PCB rear face lands on the **four fixed datum pads at z = −2.70**. Motion
   stops there — on rigid carrier body, not on a spring.
6. As the PCB front face passes z = −1.00 the two barbs snap fully clear and
   relax to zero deflection, standing 0.10 mm ahead of the PCB front face.
   Their tips reach z = −0.40, so 0.70 mm of nose stands proud of the board.

Only the two intended sprung noses deflect at any point in that sequence.
Everything else the module touches is rigid.

**Removal** (identified tool path):

1. Remove the two original bolts and lift the carrier off the Perspex.
2. From the front, squeeze each barb inward with fine-nose tweezers or snipe
   pliers — 0.10 mm per half. The barbs stand 0.70 mm proud of the PCB front
   face and are completely exposed, because nothing at all sits in front of the
   PCB.
3. With a barb pinched, lift that corner clear; or push the PCB forward from the
   **open rear window** (x −11.00 … +11.00, full board height) with a fingertip
   or spudger.
4. The plain posts then slide straight out.

No prise holes, no special tool, and no rigid feature anywhere in the corridor.

**Swept corridor expectations** (verified numerically in Stage 2):

| Swept body, ±Z | vs carrier | why |
|---|---|---|
| OLED glass | must be **CLEAR** | the aperture is empty forward of z = −1.20 except `N`; `N` is at y +18.25 |
| Solder tips @ 1.00 mm | must be **CLEAR** | tips at x −3.91 … +4.91, `N` at x ±13.40 … ±16.60 |
| Header body | must be **CLEAR** | pedestals at \|x\| 11.00 … 19.00; header at x ±5.00 |
| OLED PCB | **HIT expected**, at the two barbs only | the designed 0.10 mm snap deflection and nothing else |
| Four mounting-hole corridors | **HIT expected**, posts only | the posts are meant to be there |

---

## 7. The one blocking measurement — reported, not assumed

The brief is explicit: *if the real glass envelope cannot be demonstrated clear,
stop and report the missing measurement rather than assuming it.*

**It cannot be demonstrated. It is reported here, and it is not assumed away.**

| | |
|---|---|
| Missing dimension | the OLED glass X/Y envelope relative to the two **header-side** Ø3.00 mounting holes at (±15.00, +18.25) |
| Status in this repository | **never measured.** `oled_glass_w`, `oled_glass_h` and `oled_glass_off_y` are flagged NOT MEASURED in every revision since Rev B. The only measured glass dimension is `oled_glass_proud` = 0.80 mm. |
| Modelled value | glass top edge at y = +13.95 → **2.70 mm clear** of a Ø3.20 nose |
| Acceptance criterion | **the glass must not extend above y = +16.15** — it must stay clear of Ø4.20 circles centred on the two header-side mounting holes (nose Ø3.20 + 0.50 mm margin all round) |
| How to measure | with the module in hand, digital calipers: distance from each header-side mounting-hole centre to the nearest bonded-glass edge. One number, both ends. It must be **≥ 2.10 mm**. |
| Consequence if it fails | the sprung noses foul the glass. The design does **not** proceed to a print on an assumption. |

Evidence that is *suggestive* but is deliberately **not** treated as proof: the
front-face solder pads sit at y ≈ +17.95 … +19.15, and bonded glass cannot cover
solder pads, which bounds a rectangular glass panel below y ≈ +17.95. That bound
is 1.80 mm short of what the nose needs, and it rests on the pad position rather
than on the glass itself. It is not sufficient.

Note also what the modelled envelope implies: it puts the glass **0.40 mm over
the display-side mounting holes**, which would make the module unmountable with
any screw. The modelled numbers are therefore known to be untrustworthy in
exactly this region — a further reason not to lean on them.

**Gate: no corrected Rev P print until this single number is taken.** Everything
else in Rev P.2 is complete and validated; this is the one item standing between
the CAD and the printer.

Contingency if the measurement fails: move the sprung pair outboard along X
within the keep-out, or fall back to a non-hole forward stop bearing on the PCB
**corners** outside the glass footprint. Both are small changes to the generator;
neither is designed until the number exists.

### The other unmeasured inputs, unchanged in status

| # | Item | Blocks CAD? | Blocks print? |
|---|---|---|---|
| 1 | `oled_glass_proud` = 0.80, single measured sample | no | no |
| 2 | **Glass envelope vs the header-side holes** | **no** | **YES — §7** |
| 3 | `oled_pcb_off_y` = 4.00 assumed — affects centring only | no | no |
| 4 | Front-side protrusion ≤ 1.00 mm | no | no — assembly preparation |
| 5 | Anything on the PCB front face other than glass and tips | no | flag at the fit test |

---

## 8. Resulting nominal Z-chain

| z (mm) | Feature |
|---:|---|
| +3.000 | Perspex front face — M2 heads bear here |
| **0.000** | Perspex rear face = **carrier structural hard stop (DATUM A)** |
| −0.300 | OLED glass front face — `oled_perspex_gap` |
| −0.400 | sprung post nose tip — 0.400 mm clear of the Perspex |
| −0.750 | barb full-diameter land begins |
| **−1.000** | **snap-hook retaining face — the forward stop** |
| −1.100 | OLED PCB front face — `+ oled_glass_proud 0.80`; **0.100 mm under the hook** |
| −1.200 | forward limit of all carrier material inside the aperture, `N` excepted |
| −1.350 | plain post tops |
| **−2.700** | OLED PCB rear face = **fixed datum pads (DATUM B)** — `+ oled_pcb_t 1.60` |
| −2.900 | plain-post root fillet top |
| −3.000 | post pedestal top |
| −3.700 | plain-post root relief floor |
| −5.100 | sprung-post root fillet top |
| −5.900 | sprung-post root relief floor |
| −8.000 | carrier rear face |
| −10.800 | header rear extent — clear of the carrier |

```text
oled_perspex_gap 0.30  +  oled_glass_proud 0.80  +  oled_pcb_t 1.60  =  2.70
```

Carrier: **56.60 W x 47.20 H x 8.00 deep**. The 9.60 mm depth of Rev P.1 existed
only to give its 8.40 mm cantilever fingers room; with the fingers deleted the
depth falls out of the M2 insert stack and the post reliefs instead.

Optical: active area 29.42 x 14.70 centred on (0, 0); aperture margin x 2.89,
y 0.30 — firmware must still mask 2 pixel rows top and bottom, unchanged since
Rev C.

---

## 9. Print orientation

**Carrier rear face flat on the bed, building forward (+Z). No supports.**

| Feature | In this orientation |
|---|---|
| Post pedestals | grow from the bed, fully supported columns |
| Root reliefs | upward-opening blind pockets — need nothing |
| Post roots | start on the solid relief floor, supported |
| Datum pads at z = −2.70 | upward-facing faces on a layer boundary — layer-count accurate |
| Aperture step at z = −1.20 | upward-facing ledge |
| Barb retaining face at z = −1.00 | a **0.20 mm** downward-facing annular ledge, the step from the Ø2.80 shaft to the Ø3.20 barb (the retention overlap against the Ø3.00 hole is a different 0.10 mm) — the Rev D / Rev K hook class, both of which printed |
| Barb lead-in cone | 40.6° from the axis, 49° from horizontal — self-supporting |
| Seating face at z = 0 | becomes a top surface — use 4+ top layers or ironing, as Rev P.1 |

No unsupported critical barb: the only overhang in the retention system is the
0.20 mm hook ledge, and it is short, small in area, and printed on top of a
solidly rooted column.

DATUM A (z = 0) and DATUM B (z = −2.70) lie in the same Z stack, so the 2.70 mm
between them is layer-count accurate.

---

## 10. Pre-CAD gate — self-review verdict

The brief forbids building CAD until this section demonstrates four things.

| Required demonstration | Shown | Where |
|---|---|---|
| **Rearward motion stops on fixed datum pads** | four rigid annular pads at z = −2.70 on Ø8.00 pedestals; no spring in the path | §1, §4 |
| **Forward motion stops on positive snap-hook overlap** | 0.10 mm radial barb-over-hole interference, square retaining face that cannot cam; no friction term anywhere | §1, §3 |
| **Neither stop loads the glass** | the rear stop acts on the PCB rear face 1.60 mm behind the glass; the forward stop acts inside a mounting-hole keep-out; both are relaxed when seated, zero preload | §1, §3.4 |
| **M2 torque cannot reach the module** | the carrier bottoms on the Perspex at z = 0, the module is forward-most at z = −0.30; parallel, not series | §1 |

| Other gate | Result |
|---|---|
| Insertion from the flush/Perspex side by a straight controlled motion | PASS — pure −Z, §6 |
| Only intended sprung noses deflect during insertion | PASS — two split posts; everything else rigid, §6 |
| Retention by positive geometry, not friction | PASS — no friction term in the design or the gate, §3.4 |
| Hooks retain without clamping or bending the PCB | PASS — 0.10 mm axial clearance, 0.10 mm radial clearance, zero seated preload |
| Plain and sprung posts locate X/Y | PASS — four posts in four holes, §2 |
| No carrier plate / land / structural shoulder ahead of the PCB face | PASS — invariant P1′ with a single declared, bounded exception, §5 |
| Carrier-to-Perspex hard stop carries all M2 preload | PASS — DATUM A, §1 |
| No separate retainer bar | PASS — two printed parts, carrier + unchanged Rev N bezel |
| Removal possible with an identified tool path | PASS — §6 |
| Print orientation supports the roots, no unsupported critical barb | PASS — §9 |
| **Glass clearance for the two snap noses** | **NOT DEMONSTRATED — blocks the print, not the CAD, §7** |

**Topology approved for CAD**, with §7 recorded as the one blocking item that
must be measured before a corrected carrier is printed. The physical retention
finding from Rev P.1 remains **OPEN** and can only be closed by a real inversion
and gentle-shake handling test on a printed part.


---

# Rev P.3 amendment — the radio-side interface

Everything above is validated hardware and is unchanged. The two sections below
are the only design changes.

---

## 11. Original Decca lighting-unit keep-out (brief §8.1)

### 11.1 What collided

The lighting unit is original, retained and cannot be removed. The Rev P.2
carrier put a **continuous transverse rail** across the two side uprights on
that side (y +21.60 … +24.60, full 43.10 mm width) and stood a **cable-tie
flange** on top of it reaching y +30.60, with a rear relief and two tie slots.
The rail and that projection foul the lighting unit.

### 11.2 What is deleted

- the complete continuous end rail on the lighting-unit side;
- its central integral cable-tie / strain-relief projection;
- both tie slots and the flange rear relief;
- the rear-open wire notch that passed through the flange root.

Nothing is put back inside the keep-out. Parameters `top_flange`, `flange_w`,
`wire_notch_w`, `wire_notch_depth`, `tie_relief_w`, `tie_relief_h`,
`tie_relief_depth`, `tie_slot_x`, `tie_slot_w`, `tie_slot_h` and `tie_slot_z`
are gone from the generator, and the cable-tie path check is gone from the
validation gate.

### 11.3 What is retained

| Retained | Evidence |
|---|---|
| both sprung posts, full Ø8.60 pedestals, Ø6.00 datum pads, Ø4.80 reliefs, R0.80 root fillets | probed intact at both posts, in both tools |
| the local pedestal-to-side-upright connections | solid at the upright inner face on both sides |
| both vertical side uprights | terminated and capped, §11.4 |
| both 49.00 mm fixing-boss load paths | pitch measured 49.00000 mm exactly |
| the opposite transverse rail | untouched, y −16.60 … −13.60 |
| the OLED insertion, removal and wiring corridors | all corridors re-run CLEAR |

### 11.4 Where the carrier now ends, and how

```text
                    y = +22.55  ╭───╮           ╭───╮      <- pedestal tangent
                                │ S │           │ S │         = ASSERTED keep-out
                    y = +20.50  ├───┤           ├───┤      <- upright cap, R1.80
                                │   │  N O T H I N G  │
   ●  fixing        ┌───────────┘   │   B E T W E E N │
      x = −24.50    │  upright      │    T H E M      │
   ────────────────-┤               │                 ├──  ● fixing x = +24.50
                    │      OLED pocket, open at this end   │
                    │   ╭───╮                   ╭───╮      │
        y = −10.25  │   │ P │                   │ P │      │
                    │   ╰───╯                   ╰───╯      │
        y = −13.60  ├───────────────────────────────────────┤
        y = −16.60  └────────── bottom transverse rail ─────┘
```

The two side uprights stop at **y = +20.50**, half a millimetre short of the PCB
pocket wall line, and each is capped with a **half-round of its own 3.60 mm
width (R1.80)**. That radius lands directly alongside the retained sprung-post
pedestal root, which the pedestal ties into over a 6.26 mm long lens up to
1.35 mm deep — a real overlap, not a tangent touch.

Above y = +20.50 the only carrier material anywhere is the two Ø8.60 pedestal
towers. Between them, over x −10.70 … +10.70, there is nothing at all.

| | Rev P.2 | **Rev P.3** |
|---|---:|---:|
| Carrier extent on the lighting-unit side | y +30.60 | **y +22.55** |
| Projection returned | — | **8.05 mm** |
| Continuous bridge across the uprights | full width | **none** |
| Carrier height | 47.20 mm | **39.15 mm** |
| Carrier volume | 6.928 cm³ | **4.472 cm³** |
| Connected solids | 1 | **1** |

### 11.5 The keep-out boundary is asserted, not measured

The lighting unit's position has **never been measured**. What is known is that
the rail and the tie projection fouled it. The brief mandates retaining the full
sprung-post pedestals, so the keep-out solid used in CAD is placed at the
**pedestal tangent, y = +22.55** — the carrier's own new maximum extent.

That is an assertion. It is confirmed or refuted by the installed clearance test
(brief §12.14). If the two pedestal towers still foul, the next correction is to
reduce `pedestal_d` on the sprung pair, which is a one-parameter change; the
towers project only 2.05 mm past the upright caps.

### 11.6 Strain relief

The integral cable tie is gone and is **not replaced**. The brief permits a
replacement only outside the keep-out and only with separately demonstrated
radio-side clearance, which does not exist. With the rail deleted the header and
loom now leave through a fully open end rather than a notch. Strain relief is an
open item.

### 11.7 Rack and twist

A closed frame has become an open one, so this is a real question. What carries
it: a 3.00 × 8.00 mm bottom transverse rail across the full width, two 3.00 ×
8.00 mm side uprights 37.10 mm long, both fixing arms and bosses, a 637.7 mm²
rear face, and the two pedestals tying the uprights into the module pocket. The
seated OLED itself also spans between the uprights. CAD can only report the
sections — **brief §12.15 is the actual test**.

---

## 12. Original Decca bolt and captive-nut interface (brief §8.2)

### 12.1 What is deleted

The original front bolts have a **non-standard thread**. The entire M2 heat-set
insert architecture is removed from the generator, the geometry and the
manufacturing pack:

| Deleted | Was |
|---|---|
| `m2_insert_d` | 3.20 |
| `m2_insert_depth` | 4.00 |
| `m2_insert_recess` | 0.50 |
| `m2_bore_chamfer` | 0.40 |
| cylindrical heat-set insert bores | 2 blind bores |
| insert backing calculation | `carrier_depth + z_insert_bore` |
| M2 heat-set insert BOM entry | 2 × Ø3.2 × 4.0 |
| replacement M2 screw BOM entry | 2 × M2×6 |

`m2_boss_d` and `m2_arm_h` are renamed `fix_boss_d` and `fix_arm_h`: they are
now structural boss and arm dimensions with no thread implication.

### 12.2 The measured nut, and the interpretation on record

| Named parameter | Value | Status |
|---|---:|---|
| `original_nut_hex_width` | **3.80 mm** | **ASSUMED to be ACROSS FLATS** — see §12.6 |
| `original_nut_head_seat_depth` | 1.40 mm | measured axial head seat |
| `original_nut_total_length` | 10.00 mm | measured, must be cleared in full |
| `nut_pocket_fit_allowance` | 0.20 mm | **printer/material fit**, coupon-validated |
| `nut_body_allowance` | 0.20 mm | clearance bore beyond the head across-corners |
| `nut_seat_depth` | 2.00 mm | solid carrier ahead of the seating shoulder |
| `nut_retain_lip` | 0.25 mm | captive retaining ridge |
| `bolt_clear_d` | 2.60 mm | original bolt shank clearance (panel hole 2.40) |

**Nothing here is derived from an M2, BA, UNC, metric or other catalogue nut.**
The pocket fit allowance is a print-process fit; it is not permission to alter
the 3.80 mm physical measurement.

### 12.3 The pocket, front to rear

```text
   z =  0.00   carrier seating face on the Perspex          DATUM A
               ┌──────────────┐
               │  Ø2.60 bolt  │   solid carrier ring, 2.00 mm, carries the
               │  clearance   │   clamp load in pure compression
   z = -2.00   ├──┬────────┬──┤   ◄── SEATING SHOULDER, 8.55 mm² annulus
               │  │ 4.00af │  │   regular-hex HEAD SEAT, anti-rotation,
               │  │  hex   │  │   exactly the 1.40 mm measured head seat
   z = -3.40   │  ├─┬────┬─┤  │   ◄── step: this is what makes 1.40 positive
               │  │ │3.55│ │  │   RETAINING RIDGE, 0.125 mm per flat
   z = -3.70   │  ├─┴────┴─┤  │
               │  │ \    / │  │   self-supporting lead-in, aligns the hex
   z = -4.10   │  ├────────┤  │
               │  │ Ø4.82  │  │   clearance bore for the rest of the nut
               │  │  bore  │  │
   z = -8.00   └──┴────────┴──┘   carrier rear face — pocket opens here
                     │    │
                     │    │       the last 4.00 mm of the 10.00 mm nut sits
   z =-12.00         └────┘       behind the carrier in free air
```

Boss Ø7.60 around it, minimum continuous wall **1.391 mm** at the clearance-bore
diameter, measured 1.388 mm off the exported mesh.

### 12.4 What each requirement is met by

| Requirement | Met by | Evidence |
|---|---|---|
| rear-accessible regular-hex anti-rotation pocket | 4.00 mm across-flats hex, opening at the rear face | measured 4.000 af / 4.619 ac off the mesh at both centres; the same nut rotated 30° interferes by 1.02 mm³ |
| positive axial seating shoulder | annulus at z = −2.00 | 8.55 mm², backed by 2.00 mm of solid carrier |
| defined 1.40 mm head-seat depth | hex head seat ended by a step to the ridge | not dependent on the nut crushing into plastic |
| clearance for the full 10.00 mm nut and engaged bolt | hex + Ø4.82 bore through to the rear | nut and bolt envelopes CLEAR of glass, PCB, header, Perspex and lighting keep-out |
| sufficient continuous boss wall | Ø7.60 boss | **1.391 mm** minimum, continuous |
| serviceable captive retention | 0.25 mm retaining ridge, 0.125 mm per flat | pushed past on assembly; **no adhesive**; a 2.2 mm pin through the bolt bore pushes it back out |

The nut is modelled at its full 3.80 mm across flats over the whole 10.00 mm —
the most pessimistic reading — and the **only** carrier/nut interference
anywhere is the declared retaining ridge. That is the same discipline used for
the OLED snap noses: interference is permitted only where it is the point.

### 12.5 Load path

```text
original bolt head → Perspex → carrier seating face / hard stop
                   → captive original nut → original bolt thread
```

No part of it passes through the OLED glass or the PCB: the glass is 0.300 mm
behind the seating plane and the PCB 1.100 mm behind it, and the bolt envelope
is CLEAR of both. The bolt never touches the carrier — it only pulls the nut
onto the shoulder.

### 12.6 Measurements that gate the print

| # | Item | Why it matters |
|---|---|---|
| 1 | **nut across flats AND across corners** | 3.80 mm is modelled as across flats. If it is across corners, the true across-flats is 3.29 mm and this pocket is 0.51 mm oversize. Change the one parameter and regenerate. |
| 2 | **original bolt length under the head** | must exceed the 5.00 mm grip (Perspex 3.00 + carrier 2.00) to engage at all, and stay under 15.00 mm to remain inside the nut. Neither end is measured. |
| 3 | **hex-pocket fit coupon** | `nut_pocket_fit_allowance` 0.20 and `nut_retain_lip` 0.25 are not yet demonstrated on this printer/material. `Hex_Pocket_Fit_Coupon_revP.stl` carries the same pocket at 0.10/0.15/0.20/0.25/0.30, notch-numbered. Print it first. |

---

## 13. Rev P.3 pre-CAD gate — self-review verdict

| Required demonstration | Result |
|---|---|
| Rev P.2 OLED architecture preserved unchanged | PASS — insertion, datum pads, posts, retention, release, Z position, gap, centring, aperture, pitch, hard stops and bezel all re-validated identical |
| Complete lighting-unit-side end rail deleted | PASS — nothing in its old y +21.60 … +24.60 band |
| Cable-tie projection and slots deleted | PASS — nothing in its old y +24.60 … +30.60 band |
| No bridge between the side uprights in the keep-out | PASS — only the two pedestal towers, residual EMPTY |
| Nothing put back inside the keep-out | PASS — no replacement strain relief added |
| Sprung posts, pedestals, pads, reliefs, root fillets retained | PASS — full Ø8.60 / Ø6.00 / Ø4.80 at both |
| Side uprights, fixing arms/bosses, opposite rail retained | PASS |
| Uprights terminated with deliberate printable radii | PASS — R1.80 half-round caps |
| One connected open-ended solid | PASS — 1 lump in Fusion, 1 connected component on the mesh |
| M2 heat-set architecture completely removed | PASS — no bore, depth, recess, chamfer, backing or BOM entry |
| Named original-nut parameters created | PASS — §12.2 |
| 3.80 mm across-flats interpretation recorded | PASS — §12.2, §12.6, and in the generator source |
| Hex pocket, seat, head-seat depth, envelope, boss wall, captive retention | PASS — §12.4 |
| Original load path, no clamp through glass or PCB | PASS — §12.5 |
| 49.00 mm pitch unchanged | PASS — 49.00000 mm exactly |
| **Lighting-unit position** | **ASSERTED, NOT MEASURED — §11.5** |
| **Nut across-corners, bolt length, pocket fit** | **NOT MEASURED — §12.6** |

**Amendment approved for CAD**, with four items that gate the print and the
brief §12 tests that gate release.
