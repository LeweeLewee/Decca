# Hardware Architecture

> **Status:** active. Reflects the confirmed Phase 1 physical build plus the
> locked Phase 2 audio and power-control architecture. Pot inputs GPIO32–35 and
> OLED I²C GPIO21/22 are bench-verified; remaining ESP32 assignments are
> **(proposed)** or unassigned. See `docs/Wiring.md` for the authoritative
> controller interconnect detail and ADR-0008 / ADR-0010 for the streamer,
> amplifier and power-control decisions.

Describes the electrical system: the boards, how power flows, and how the ESP32
connects to the front panel, display, lighting, streamer and external audio path.

## Scope Boundary

The ESP32 is a **control and user-interface system only**. It **must not process
or carry audio**. All potentiometers are position sensors read by the ADC; the
audio signal path is separate from the controller.

## System Block Diagram

```
                 ┌──────────────────────────────────────────┐
                 │                ESP32 DevKit               │
                 │        (control + UI only, no audio)      │
                 └───┬───────┬───────┬────────┬───────┬──────┘
       ADC1 (H1) │       │ H2    │ H3     │ H4    │ H5 (PWM)
        4× 10k   │       │ on/off│ source │ I²C   │ MOSFET gate
     ┌───────────┴──┐ ┌──┴───┐ ┌─┴─────┐ ┌┴─────┐ ┌┴──────────┐
     │ Balance/Treble│ │orig. │ │ Gram  │ │ OLED │ │ 3× 5V     │
     │ Bass/Volume   │ │switch│ │contact│ │128x64│ │ E10 LEDs  │
     │ (position)    │ │Red/Grn│ │2-state│ │ SH1106│ │ (N-ch FET)│
     └───────────────┘ └──────┘ └───────┘ └──────┘ └───────────┘

                  local network control / metadata
                 ESP32  <-------------------->  WiiM Pro
                                                   │
                                                   │ line-level audio
                                                   ▼
                                             Fosi Audio ZA3
                                                   │
                                                   ▼
                                           Passive speakers

                 Decca on/off -> ESP32 -> 12 V trigger driver -> ZA3 trigger
```

## Locked Audio Architecture

The audio-path architecture is locked by ADR-0008 and ADR-0010 as:

`WiiM Pro -> Fosi Audio ZA3 -> passive speakers`

- **Streamer:** WiiM Pro, specifically. This is a locked model decision.
- **Power amplifier:** **Fosi Audio ZA3 stereo amplifier**, locked.
- **Dual monoblocks:** rejected for the current build unless requirements change.
- **Integrated WiiM amplifier variants:** WiiM Amp / Amp Pro are not substitutes
  for the selected architecture without a new ADR.
- **Cabinet thermal constraint:** none for normal hi-fi amplifier selection. The
  Decca cabinet has ample rear ventilation, so thermal performance is not a
  differentiating selection criterion beyond the amplifier's normal operating
  requirements.
- The ESP32 communicates with the WiiM Pro only for control and metadata. It never
  sits in the audio signal path.
- User volume is controlled by the original Decca volume potentiometer as an ESP32
  position input, with the ESP32 commanding WiiM output volume. The ZA3 volume/gain
  control is set during commissioning as a fixed hardware ceiling rather than used
  as the normal user volume control.

## Power

- Controller/lighting architecture is locked to a **single regulated 5 V control
  rail** plus **3.3 V** from the ESP32 board regulator for logic, ADC references
  and the OLED where applicable.
- The 5 V rail powers the ESP32 board input and the three dial-lighting lamps.
- The dial lighting does **not** receive a separate 6 V or 6.3 V rail. A dedicated
  lamp-only supply is explicitly rejected unless a later hardware constraint
  requires an ADR change.
- The 5 V supply is **selected and acquired**: **Phihong PSA15R-050P** switching
  adapter, rated **5.0 V DC at 3.0 A (15 W)**. This closes the 5 V PSU procurement
  item and provides adequate margin for the controller, OLED and all three lamps.
  Before connection, confirm the DC plug size and polarity with a multimeter; keep
  the adapter's enclosed mains side intact and route only its low-voltage output
  into the control-rail wiring.
- ESP32 and dial-lighting **grounds are common**.
- The original Decca on/off switch remains a **low-voltage ESP32 input only**; it
  does not carry 230 V mains.

### WiiM Pro power behaviour — locked

- The **WiiM Pro remains continuously powered** from its own supply in normal use.
- The WiiM is **not hard power-cycled** by the Decca front-panel on/off control.
- WiiM **automatic standby** is the preferred idle/off-state behaviour so that the
  unit remains network-aware and can wake without a full boot cycle.
- Turning the Decca on does not require mains switching of the WiiM. Playback or a
  supported WiiM/network control action may wake it from standby.
- The ESP32 may later issue a deterministic wake/control request if bench testing
  confirms a suitable supported local-API behaviour, but the hardware design does
  **not depend on that**.
- On Decca off, the ESP32 should stop playback or issue an appropriate supported
  control action where useful, then allow WiiM auto-standby to provide the normal
  idle state.

### Fosi Audio ZA3 power behaviour — locked

- The ZA3 is the locked stereo power amplifier for this build.
- The ZA3 is **not mains-switched by the original Decca switch**.
- Its PSU may remain energised; amplifier operating state is controlled through
  the ZA3's **12 V trigger input**.
- The ESP32 controls a dedicated low-voltage trigger-driver stage that generates
  or switches the required 12 V trigger signal. The exact transistor/MOSFET,
  12 V source and ESP32 GPIO remain open implementation details pending component
  selection and bench verification.
- No ESP32-controlled 230 V relay is required for the amplifier in the locked
  architecture.

### Front-panel power-state behaviour — locked

The original Decca on/off control is a **system-state command**, not a mains
switch.

**ON sequence**
1. Original switch closes and the ESP32 detects the active state.
2. ESP32 asserts the ZA3 12 V trigger through the trigger-driver stage.
3. ESP32 fades the three dial lamps up to their stored commissioning brightness.
4. ESP32 enables the OLED and runs the normal startup/dashboard sequence.
5. WiiM remains physically powered and wakes from automatic standby when playback
   or supported network/control activity requires it.

**OFF sequence**
1. ESP32 detects the original switch opening.
2. ESP32 stops playback / sends an appropriate WiiM control action where useful;
   WiiM then uses its own automatic standby behaviour.
3. ESP32 fades the dial lamps to zero.
4. ESP32 blanks the OLED.
5. ESP32 removes the 12 V trigger so the ZA3 enters its trigger-controlled off/
   standby state.
6. ESP32 and its 5 V control supply remain powered so the next switch-on can be
   detected immediately.

The cabinet's existing rear ventilation is adequate and imposes no additional
thermal-design restriction.

## Controller

- **ESP32 DevKit** (dual-core, Wi-Fi, LEDC PWM, ADC).
- The physical board used is the **30-pin DevKit V1 / DOIT-style layout** on a
  matching 30-pin screw-terminal adapter. Documentation therefore records both
  the logical GPIO number and the **silkscreen label printed on the board**.
- **ADC1 is used for all analogue inputs** because Wi-Fi is enabled in Phase 2
  and **ADC2 is unavailable while Wi-Fi is active** (Specification `HW-02`).
- Strapping pins (0, 2, 5, 12, 15) are avoided for driven/reset-sensitive lines
  (`HW-03`). GPIO34–39 are input-only with no internal pull-ups (`HW-04`).

## Inputs

### Potentiometers (H1)
Four installed **AB Elektronik / TT Electronics ABW1 10K linear** pots (CPC
order code **RE04644**) for Balance, Treble, Bass and Volume, wired GND / wiper /
3.3 V (Brown / White / Red). Wipers read on ADC1. Firmware applies calibration,
smoothing, deadband, and optional inversion (see Firmware Architecture).
Bench-verified assignments and board labels are:

| Control | GPIO | Printed board label |
|---------|------|---------------------|
| Volume  | GPIO32 | **D32** |
| Bass    | GPIO33 | **D33** |
| Treble  | GPIO34 | **D34** |
| Balance | GPIO35 | **D35** |

Each channel measured 0 anticlockwise, approximately 2047 at centre, and 4095
clockwise on 2026-08-24, so the default 0–4095 calibration remains applicable.

### On/off switch (H2)
Retained original switch and cable, active conductors **Red** and **Green**. A
simple open/close contact read as a **low-voltage digital input** with the ESP32
**internal pull-up** enabled (proposed GPIO19, board label **D19**). **Not a mains switch.** Optional
firmware inversion after bench testing. Its logical state drives the locked
system-power sequence documented above.

### Source button bank (H3)
The original selector PCB and interlocked mechanism are retained as the
mechanical carrier (ADR-0001), but unreliable soldering/contact behaviour makes
multi-button electrical reuse unsuitable.

Only the verified right-hand Gram Green/Yellow dry-contact pair is connected to
GPIO23 / D23 with the internal pull-up and software debounce. Closed Gram selects
Vinyl; open Gram selects Digital Streamer. VHF, SW, MW and LW are mechanically
retained but unwired at the ESP32; pressing them may release Gram through the
interlock. GPIO16, GPIO17 and GPIO18 are released. A new button panel is a
deferred fallback (ADR-0011). Stereo/Mono remains unwired (ADR-0005).

## Outputs

### OLED display (H4)
Purchased Pi Hut 1.3-inch white 128×64 SH1106 I²C panel (SKU 105630), powered
from 3.3 V at address 0x3C. SDA GPIO21 / board label **D21** and SCL GPIO22 /
board label **D22** were bench-verified on 2026-08-25 with the on-target display
suite and a visual layout inspection.

### Dial lighting (H5)
The purchased lamp set is **ShuoHui ASIN B0CFTLZFGT**: ten E10 miniature
screw LEDs rated 6 V AC/DC, 0.2 W and 3000 K; three are required. The lamps were
bench-confirmed functional at **5 V** on 2026-08-29, validating compatibility with
the locked 5 V lighting rail. Physical holder fit, final brightness and total
three-lamp current remain commissioning checks.

The selected switch candidate is one **DAOKAI 3.3 V / 5 V PWM MOSFET driver
module, ASIN B09YYH2BTF**, from the ordered pack of ten. Seller compatibility
claims do not replace verification: GPIO25 / board label **D25**, safe-off
behaviour, clean PWM switching and module temperature must pass at the measured
three-lamp load. The three validated lamps will be wired **in parallel** with
common ground to the ESP32.

Brightness is a commissioning/configuration value rather than a permanent front-
panel user control. Firmware stores the selected PWM level in non-volatile
settings and applies it at startup. The unused aerial control may be used as a
temporary commissioning input if convenient, but it is not reserved as a
permanent lighting control. Behaviours: fade up/down, configurable stored
brightness, safe boot state.

### ZA3 trigger output
The ESP32 controls a dedicated interface to the ZA3 **12 V trigger input**. The
ESP32 GPIO must not source 12 V directly. A suitable transistor/MOSFET or isolated
low-voltage driver and a 12 V source are required. Exact implementation and GPIO
remain **open/proposed** until the driver is selected and bench-tested.

## Networking (Phase 2)

Wi-Fi is used only in Phase 2 for **WiiM Pro local API** integration (Gram-driven
Line-In/digital-path switching, volume and metadata/playback state). Digital
service, station, playlist and track selection remain in the WiiM app. This is the reason ADC1 is mandated
for all analogue inputs. See Firmware Architecture → WiiM interface, ADR-0006,
ADR-0008 and ADR-0010.

## Revisions

Track board/electrical revisions in [Revision History](Revision History.md).
