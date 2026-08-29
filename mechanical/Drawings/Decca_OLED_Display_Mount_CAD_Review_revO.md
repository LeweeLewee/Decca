# Decca OLED Display Mount — CAD Redesign Specification (Rev O / Rev P correction)

Supersedes Rev N as the active design direction for the OLED carrier.

Amended 2026-08-29 after the physical Rev P prototype failed loose-carrier
retention. Rev P remains an open prototype revision; this correction supersedes
the rear-insertion and friction-retention clauses below as originally issued.

Platform: Autodesk Fusion 360. Manufacture: FDM 3D print.

## 1. Reason for redesign

Physical print-and-fit iterations of Rev N showed that the front-loaded architecture had become constrained by OLED depth. Rev O changes the topology rather than further tuning the Rev N front plate and retainer arrangement.

The governing design objective is to place the OLED glass close to the inside face of the original Perspex while keeping all M2 screw preload out of the OLED glass and PCB.

The subsequent Rev P prototype exposed a second architectural error. Rev P
inserted the OLED from the rear towards the Perspex, but placed its nominal PCB
datum shoulders behind the PCB rear face. Those shoulders restrained withdrawal
in the opposite direction; forward handling retention relied only on four
0.10 mm edge-friction contacts. The physical screen passed through the loose
carrier. This physical result invalidates the analytical friction-hold release
claim and is the governing evidence for the correction in this document.

## 2. Corrected Rev P architecture — mandatory topology

The OLED module shall load into the loose carrier from its
**flush/Perspex-contact side**, moving rearwards onto fixed PCB datum pads.

The carrier shall sit behind the OLED PCB. The OLED glass/display projects forwards towards the inside face of the Perspex.

**No carrier front plate, seating land, shoulder, lip or other structural load
feature may occupy the space between the front face of the OLED PCB and the
Perspex.** This continues to reject the failed Rev O implementation that
recreated the Rev N 1.10 mm forward retention plane as short seating lands.

A narrowly controlled exception is permitted only for local sprung-post noses
inside verified PCB mounting-hole keep-outs. A snap nose may cross the PCB front
plane only as far as required for positive handling retention and only when its
clearance to the OLED glass, solder joints, Perspex and full assembly path is
demonstrated. It shall not establish OLED depth or carry M2 preload.

The loose carrier shall positively constrain the PCB in both axial directions:

1. fixed, non-spring datum pads acting on rear-safe PCB areas stop rearward
   insertion and establish OLED Z position; and
2. sprung locating-post noses provide positive forward retention after seating,
   with deliberate axial clearance so they retain rather than clamp the PCB.

Friction, gravity or the assumed elastic modulus of printed material shall not
be used as the primary proof of axial retention. The Perspex remains redundant
final containment after assembly, but the OLED must not fall through or fall
away from the loose carrier during handling.

The carrier/Perspex assembly therefore performs two independent functions:

1. **Structural load path:** M2 screw → carrier structural bosses / hard stops → Perspex.
2. **OLED location and capture:** fixed rear PCB datum pads establish depth;
   locating posts establish X/Y; sprung post noses retain the loose module;
   Perspex provides redundant forward containment after assembly.

The glass must never be the structural compression stop.

## 3. Existing Decca interface — measured values are authoritative

Use the measured and print-confirmed dimensions already recorded in the repository, not the superseded Spec v1.0 values:

- Original Perspex thickness: 3.00 mm.
- Existing aperture: **35.20 mm W × 15.30 mm H**.
- Existing M2 fixing-hole pitch: **49.00 mm horizontal**.
- Fixing-hole centreline: vertically centred on the display aperture.
- No additional holes, cutting or irreversible modification to the original Perspex.
- M2 screws enter from the front of the Perspex and fasten into the rear carrier.

If any later physical measurement contradicts these values, the physical measurement wins and the parameter is updated explicitly.

## 4. Front bezel

The front bezel remains a separate cosmetic trim around the aperture only.

It must not include the M2 fixing holes and must not carry structural load. Retain the validated Rev N bezel unless physical testing identifies a specific reason to change it.

## 5. OLED loading, datum and retention

### 5.1 Flush-side loading

The OLED PCB shall insert from the carrier's flush/Perspex-contact side by a
controlled rearward translation. The glass enters the central clearance first;
the PCB rear face then seats on fixed rear datum pads. The carrier shall retain
open rear access around the header and solder joints after seating.

### 5.2 Fixed positive OLED Z datum from behind

OLED fore/aft position shall be established by **rear PCB support lands / shoulders acting on the rear face or rear-safe areas of the PCB**.

These support features shall be rigid parts of the carrier body, not faces on a
moving spring. They stop rearward insertion, locate the PCB in Z and must not
project ahead of the PCB front face.

The intended section is therefore:

```text
Perspex
  |
small controlled optical gap
  |
OLED glass
  |
OLED PCB
  ^
rear PCB support lands / datum
  |
rear carrier
```

Separate carrier structural bosses / hard stops shall contact the Perspex directly outside the OLED module envelope and carry the M2 preload.

### 5.3 Locating and retaining posts

Use a conservative Rev D / Rev K hybrid as the starting arrangement:

- two plain locating posts at the narrow, glass-sensitive hole pair; and
- two split sprung locating posts at the wider/header-side hole pair.

Candidate starting geometry from the earlier printed-post development is a
2.80 mm sprung shaft, 0.70 mm split slot, 3.20 mm initial barb diameter,
R0.80 root fillet and approximately 1.00 mm root relief where the real glass
envelope permits. Plain posts may start at 2.70 mm. These values are prototype
inputs, not automatic acceptance values.

Do not use four sprung posts unless the actual glass-to-hole clearances prove the
narrow pair safe. Rev K's narrow pair depended on only 0.20 mm assumed glass
clearance; that dependency shall not be carried forward without measurement.

Design intent:

- locate the PCB consistently in X/Y;
- prevent the loose OLED falling away during handling and installation;
- prevent the seated OLED translating forwards through the loose carrier by
  positive geometric overlap, not edge friction;
- avoid significant PCB bending or insertion force;
- keep sprung noses inside verified mounting-hole keep-outs and clear of bonded
  glass throughout insertion, seating and removal;
- provide axial clearance between each engaged nose and the PCB so the post does
  not clamp the module; and
- provide an identified, accessible release method after the carrier is removed
  from the Perspex.

A full swept insertion/removal corridor check is mandatory before print release.

### 5.4 Retainer bar

Delete the separate retainer bar from Rev O and retain a two-printed-part system:
carrier plus the existing bezel.

The post-and-datum system provides positive loose-carrier retention. The
assembled Perspex provides redundant final containment without becoming the OLED
depth datum or applying preload to the glass.

## 6. Optical depth and glass protection

Target nominal glass-to-Perspex gap: **0.15–0.30 mm**.

Select the final nominal from measured OLED geometry and realistic FDM tolerance. A nominal around 0.30 mm is acceptable if required for robustness.

Critical requirements:

- the OLED glass must not become the structural stop when the M2 screws are tightened;
- tightening the M2 screws must not alter OLED depth;
- there shall be no carrier material between the OLED PCB front face and Perspex used to establish this gap.

## 7. Solder-tip constraint — resolved by module preparation

The physical OLED solder tips project more than 2 mm from the PCB front face. The
Rev P depth chain proved that the earlier 1.50 mm preparation limit is
incompatible with the 0.30 mm optical gap. Prepare all display-side protrusions
to a **maximum of 1.00 mm proud**.

This is an accepted assembly preparation step and shall be treated as the design input for the corrected Rev P prototype.

Accordingly:

- model `oled_tip_proud = 1.00 mm maximum`;
- provide sufficient local carrier clearance around the solder joints and header;
- do not redesign the carrier topology merely to accommodate untrimmed >2 mm tips;
- verify that the prepared 1.00 mm tips do not interfere with the Perspex or any carrier feature in the final assembly or insertion path.

The hard geometric ceiling is the measured glass proud plus the selected optical
gap. Preserve at least 0.10 mm clearance to the Perspex rather than aiming at the
zero-clearance ceiling.

## 8. Carrier structural design

Rev O should restore sensible FDM section thicknesses behind and around the OLED module.

Guidance:

- approximately 2.0–3.0 mm structural wall thickness where geometry allows;
- reinforce M2 boss regions appropriately;
- use direct carrier-to-Perspex hard stops outside the OLED module envelope;
- avoid unnecessary thin membranes around the display window;
- leave rear access around the header and solder joints;
- maintain cable/header clearance and serviceability;
- minimise part count and avoid a separate retainer.

## 9. Required corrective CAD changes for open Rev P

1. Replace rear insertion with flush/Perspex-side insertion moving rearwards.
2. Replace the moving Rev P edge-finger shoulders with fixed, non-spring rear
   PCB datum pads.
3. Delete the four PCB-edge friction fingers, their tongues, shoulders and
   radial prise holes.
4. Add plain and sprung locating posts as specified in §5.3, providing positive
   forward retention after the PCB seats.
5. Keep all structural PCB datum geometry behind the PCB front face; permit only
   verified local snap noses to cross that plane inside mounting-hole keep-outs.
6. Provide a clear path for the OLED glass with no forward PCB seating lands.
7. Retain separate positive carrier-to-Perspex hard-stop geometry to carry M2 preload.
8. Delete the separate retainer bar.
9. Model display-side protrusions at 1.00 mm maximum after preparation.
10. Use the measured 49.00 mm M2 pitch and 35.20 × 15.30 mm aperture.
11. Retain the existing bezel unless new test evidence requires a change.
12. Preserve active-area centring relative to the original Decca aperture.
13. Keep the design fully parametric in Fusion 360.
14. Keep Rev P open and remove all release claims until corrected physical
    retention has passed prototype testing.

## 10. Mandatory CAD validation gate

Before the corrected Rev P geometry is accepted for a prototype print, verify all of the following on the actual generated geometry:

- carrier × Perspex: clear except intended structural seating faces;
- no structural carrier geometry ahead of the OLED PCB front face within the
  OLED module envelope, except verified local snap noses in mounting-hole keep-outs;
- rear PCB support contacts only intended PCB support areas;
- carrier × OLED glass: clear throughout insertion, seating and removal;
- carrier × OLED PCB: correct fixed rear datum, X/Y location and controlled
  positive snap overlap;
- carrier × header and prepared 1.00 mm solder joints: clear;
- prepared solder joints × Perspex: at least 0.10 mm clear;
- OLED glass × Perspex: 0.15–0.30 mm nominal gap;
- M2 load path terminates through carrier hard stops into Perspex, not OLED glass or PCB;
- snap features locate and positively retain the PCB without excessive strain,
  bending or axial preload;
- rearward PCB translation stops on fixed datums and forward PCB translation is
  blocked by positive snap geometry without relying on friction;
- OLED can be inserted from the flush side and removed through an identified
  release path without bonded glass sweeping through a rigid barb/post envelope;
- carrier seats flat against Perspex;
- screen active area remains centred behind the bezel/aperture;
- no unprintable thin slivers or unsupported critical features;
- normal FDM wall thickness is restored in structural areas.

**A static final-position interference check is insufficient. Swept insertion
and removal checks, plus a directionally correct positive-retention check, are
mandatory. A friction-versus-module-weight calculation cannot satisfy the
positive-retention requirement.**

## 11. Design-review gate before Fusion build

Before generating the next Fusion model, produce and review a simple side-section / topology diagram showing:

- Perspex;
- optical gap;
- OLED glass;
- PCB;
- rear PCB support datum;
- structural carrier hard stops to Perspex;
- M2 load path;
- plain and sprung locating posts;
- local positive snap overlap on the PCB front face; and
- the flush-side insertion direction.

The CAD build must not proceed unless the section shows positive stops in both
axial directions: fixed rear datum pads stopping insertion and sprung noses
stopping forward escape. It must contain no carrier land, plate or structural
shoulder between the PCB front face and Perspex. Only the controlled local snap
nose exception in §2 is permitted.

## 12. Prototype acceptance tests

The next corrected Rev P print is a geometry-and-retention prototype. Check in
this order:

1. flush-side rearward insertion of the OLED without glass or component contact;
2. PCB rear face seats consistently on every fixed datum pad;
3. sprung posts engage with visible positive overlap and no PCB bow;
4. the loose carrier retains the OLED when inverted in every axis and during a
   gentle handling shake, with no fall-through or fall-away;
5. the stated release method removes the OLED without damaging posts or PCB;
6. carrier seats flat against Perspex;
7. actual OLED-to-Perspex gap;
8. active-area centring when powered;
9. bezel alignment;
10. M2 tightening does not change OLED depth or stress the module;
11. prepared solder joints and header clear the Perspex and carrier;
12. no rattle when assembled; and
13. no separate retainer is required.

CAD and mesh checks may release this prototype print, but they shall not close
the retention finding. Physical tests 1–5 are mandatory before Rev P can regain
a release recommendation.

## 13. Design decision

Rev N should receive no further architecture-level iteration.

The failed first Rev O implementation is rejected because it recreated the critical Rev N geometry as **1.10 mm forward PCB seating lands** and attempted to capture the OLED within the carrier alone.

The first Rev P implementation is also rejected for retention because rear
insertion passed the OLED beyond the only positive shoulder and left forward
handling retention to assumed edge friction. Its M2 hard-stop architecture,
optical chain and open rear access remain useful.

The approved corrective direction is: **flush-side OLED insertion onto fixed
rear PCB datum pads; plain and sprung mounting-hole posts providing X/Y location
and positive loose-carrier retention; a controlled local exception for verified
snap noses only; separate carrier-to-Perspex structural hard stops; prepared
front-side protrusion no more than 1.00 mm; no separate retainer bar; and physical
retention testing before release.**
