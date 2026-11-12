# Design decisions

The team's decision log. The decisions and the reasons are the team's. Since 2026-11-08, Claude writes the entries at the team's request (root `CLAUDE.md`, Decision log). Open choices live in `design/fab/OPEN_DECISIONS.md`; design steps and numbers live in `design/DESIGN_LOG.md`.

Format: date · decision · options rejected · reason · consequences.

---

## 2026-11-02 · Project scope and fixed inputs

*Backfilled 2026-11-08 from DESIGN_LOG step 0 and the team's "Notes for 6.2540".*

- **Decision:** a five-wire surface trap for ¹³⁸Ba⁺ (detection on the 493 nm fluorescence) with an NbN SNSPD written by e-beam under the readout zone, segmented outer DC electrodes, plated Au electrodes and an Al ground plane, for a cryostat at about 5 K.
- **Rejected:** for the process family, a pure single-layer trap and a full multilayer process (Bautista-Salvador 2018). Otherwise not recorded.
- **Reason:** not recorded for the ion or the substrate. The team's notes give reasons for three parts:
  - Ground plane + thick SiO₂ + top electrodes (Romaszko 2020 Fig. 3.1): "a simpler design we could go for, as a in between difficulty of a pure single layer trap vs actual multilayering" (Notes, Romaszko section).
  - Detector shield: "just SiO2 shield on top, Al ground plane, optional ITO window", because "clearly it worked for Hampel" (Notes, Integrated SNSPD section).
  - Electrodes: plated Au first, with sputtered Al (JoVE 2017) to "fall back to … if gold doesn't work out" (Notes, JoVE section).
- **Requirement on the detector film (team notes, Todaro section):** Tc more than 25 % above the trap surface, so "anything over 7K" for a 5 K trap.
- **Superseded in part:** the die-wide Al ground plane became a local mirror (2026-11-08, below); the planned grounded ITO window was dropped (2026-11-07).

## 2026-11-02 · Separate loading zone

*Backfilled 2026-11-08.*

- **Decision:** two zones: a loading zone, plus a readout zone directly above the SNSPD. The ion is shuttled between them with the outer DC segments.
- **Rejected:** loading directly over the detector.
- **Reason (team notes, Todaro section):** "not sure if it is safe to blast the SNSPD with a bunch of atoms." The notes also record that Todaro needed a separate zone for cooling, because cooling above the detector was hard.
- **Details:** zones were 600 µm apart (DESIGN_LOG step 8); the team set 480 µm on 2026-11-08 (below).

## 2026-11-02 · High-resistivity Si substrate

*Backfilled 2026-11-08.*

- **Decision:** high-resistivity float-zone Si, with sapphire and fused silica kept as written-up alternatives.
- **Rejected:** sapphire and fused silica as the primary substrate.
- **Reason (team, given 2026-11-08):** low RF loss, and it is NIST practice.
- **Later change:** the local-mirror architecture (2026-11-08) tightened the order to ρ > 20 kΩ·cm.
- **Details:** DESIGN_LOG step 0; `design/fab/TRAVELER.md` section G (substrate deltas).

## 2026-11-02 · Ion height 50 µm; height may differ between zones

*Backfilled 2026-11-08.*

- **Decision:**
  - Target ion height h = 50 µm.
  - Height policy: the ion height does not have to be the same in every zone. What matters is confinement at both zones, transport between them that can actually be done, and micromotion at readout that can be compensated.
- **Rejected:** the other heights in the step-1 table (40 and 70 µm).
- **Reason:**
  - Height policy: the electrode cut-out over the SNSPD lowers the ion there (team notes 11/7). The notes list ways to live with it: a different beam height per zone, a beam wide enough for both heights, or different waveforms per zone.
  - 50 µm: not recorded at the time (asked 2026-11-08). The team gave its reason on 2026-11-09; see the entry "Keep the 50 µm ion height" below. DESIGN_LOG step 1 has the first analysis: heating scales roughly as h⁻⁴ while collection gains only about h⁻², so detector size is the cheaper lever.
- **Details:** DESIGN_LOG steps 0–1.

## 2026-11-02 · Plain diced square chip, no bowtie

*Backfilled 2026-11-08.*

- **Decision:** a regular diced 10 × 10 mm chip.
- **Rejected:** the bowtie chip (1.4 mm isthmus cut by through-wafer DRIE) proposed in DESIGN_LOG step 4.
- **Reason:** simpler fab.
- **Superseded:** by the narrow die (below), then the 10 × 10 mm centred die (2026-11-07).
- **Details:** DESIGN_LOG step 8.

## 2026-11-02 · Narrow 10 × 2.5 mm die

*Backfilled 2026-11-08.*

- **Decision:** a narrow 10 × 2.5 mm die with the trap on its centre line.
- **Rejected:**
  - the square die with the trap in one corner;
  - two traps on the square die;
  - a tidier single corner trap.
- **Reason:** the corner layout was lopsided and wasteful. Only the corner held the trap; every lead ran 7–9 mm to one pad column; about three quarters of the die was empty.
- **Superseded:** by the 10 × 10 mm centred die (2026-11-07).
- **Details:** DESIGN_LOG step 12.

## 2026-11-02 · A plain trap die without an SNSPD (NODET)

*Backfilled 2026-11-08.*

- **Decision:** add a trap-only die: same electrodes and pads, no SNSPD, solid centre DC.
- **Rejected:** not recorded.
- **Reason:** not recorded. It later became the R1_TRAP die and the reference for the SNSPD dies.
- **Details:** DESIGN_LOG step 14.

## 2026-11-02 · Fabricate as small R&D runs at MIT.nano

*Backfilled 2026-11-08.*

- **Decision:** fabricate as a series of short runs, each a full 100 mm wafer with only a small central block of dies written. Change the layout between runs.
- **Rejected:** a single production wafer.
- **Reason (team notes 11/7):** make several chips at a time to speed up fabrication ("make 3 at one time").
- **Details:** DESIGN_LOG step 15; `make_run.py`.

## 2026-11-02 · Process: ground-plane flow, plated Au electrodes

*Backfilled 2026-11-08 from `design/DESIGN_LOG.md` and the team's "Notes for 6.2540".*

- **Decision:** follow Romaszko 2020 Fig. 3.1: an Al ground plane, a thick (~10 µm) PECVD SiO₂ layer, and plated Au electrodes on top (substrate: entry above).
- **Rejected:** a pure single-layer trap, and a full multilayer process (Bautista-Salvador 2018).
- **Reason (team notes):** "a simpler design we could go for, as a in between difficulty of a pure single layer trap vs actual multilayering".
- **Fallback:** sputtered Al electrodes (JoVE 2017) "if gold doesn't work out"; the team flagged checking whether Au is allowed in the tools.
- **Status:** superseded 2026-11-08 by the local-mirror architecture (below).
- **Details:** DESIGN_LOG step 0.

## 2026-11-02 · SNSPD material: NbN, patterned by e-beam

*Backfilled 2026-11-08 from `design/DESIGN_LOG.md` and the team's "Notes for 6.2540".*

- **Decision:** NbN nanowire detector written with e-beam lithography.
- **Rejected:** not recorded. The references used MoSi (Todaro 2021) and NbTiN (Hampel 2023).
- **Reason (team notes):** the detector needs a T_c well above the ~5 K operating temperature ("anything over 7K"), and NbN is the film the team has deposition access to (Berggren-group recipe).
- **Details:** DESIGN_LOG step 0.

## 2026-11-02 · SNSPD protection: SiO₂ cap, Al ground plane, grounded ITO window

*Backfilled 2026-11-08 from `design/DESIGN_LOG.md` and the team's "Notes for 6.2540".*

- **Decision:** cover the detector with SiO₂, put the Al ground plane under it, and add a grounded ITO window.
- **Reason (team notes):** against laser scatter, RF pickup and dielectric charging, "the short answer is just SiO2 shield on top, Al ground plane, optional ITO window". ITO was also meant to screen the field kick from an SNSPD click.
- **Status:** ITO removed 2026-11-07; die-wide Al replaced by a local mirror 2026-11-08 (both below).

## 2026-11-02 · First run is trap-only (R1_TRAP)

*Backfilled 2026-11-08 from the design docs; the reason was not written down at the time.*

- **Decision:** run the trap-only process first (R1_TRAP: no NbN, no EBL), then the full stack (R1_FULL).
- **Rejected:** a full-stack first run.
- **Reason:** not recorded. The run sheet states the goal: qualify the trap process and trap ions on a die without a detector, and use that NODET die as the reference for the SNSPD dies.
- **Status:** superseded 2026-11-12 by the one-wafer run (entry "One wafer for all four chips" below).
- **Details:** DESIGN_LOG step 16; `design/SIMPLIFICATIONS.md` S2.

## 2026-11-07 · Detector variants: 30 µm and 60 µm windows, plus a die without a detector

*Backfilled 2026-11-08 from `design/DESIGN_LOG.md` and the team's "Notes for 6.2540".*

- **Decision:** make an A30 die (30 × 30 µm detector window), a B60 die (60 µm along the axis) and the NODET die.
- **Reason:** not recorded (asked 2026-11-08).
- **Status:** B60 dropped and then kept again on 2026-11-08 (below).
- **Details:** DESIGN_LOG steps 7 and 19.

## 2026-11-07 · No ITO anywhere

*Backfilled 2026-11-08.*

- **Decision:** remove both ITO layers (top ITO on D2, buried ITO on the cap). The NbN sits under SiO₂ only.
- **Rejected:**
  - the v2 two-ITO window;
  - keeping only the buried, grounded ITO (absorption ≈ 0.53 and RF pickup ≈ 0 in 2-D, but ITO sputtering stays in the process);
  - replacing the buried ITO with Al. The team asked for this if the buried ITO was the mirror. It was dropped once it was clear the buried ITO sits above the nanowire, in the light path, as a matching layer and RF shield; the Al M1 below is already the mirror, and Al there would block the light.
- **Reason (team, given 2026-11-08):** switch to an Al mirror to implement the Hampel design. The team's notes had listed the window as "SiO2 shield on top, Al ground plane, optional ITO window".
- **Costs accepted:** absorption 0.53 → ≈ 0.40; RF pickup bound ≈ 0 → 1.42 µA; the ion sees bare SiO₂ in the window (no screening of charging or click kicks); the L45 protect patch over the window becomes essential.
- **Details:** DESIGN_LOG step 17.

## 2026-11-07 · 10 × 10 mm trap die, trap centred, pads at the die edges

*Backfilled 2026-11-08.*

- **Decision:** 1 cm × 1 cm die instead of the v2 10 × 2.5 mm die, trap on the centre line, bond pads moved to the die edges.
- **Rejected:**
  - keeping the narrow 10 × 2.5 mm die;
  - a 10 × 10 mm die with the trap near one edge (as in v1).
- **Reason (team, given 2026-11-08):** to fit the lab's form factor. The beam-clipping cost was stated when the option was chosen: ~1.7 × 10⁻² of the 493 nm beam clips the surface (vs 1.1 × 10⁻⁵ on the narrow die).
- **Details:** DESIGN_LOG step 18.

## 2026-11-08 · On-chip vias from the Au ground fill to the Al

*Backfilled 2026-11-08.*

- **Decision:** tie the Al to the Au ground fill with vias on chip, as Hampel 2023 grounds its mirror, instead of relying on bond wires. Came out of comparing the team's FabuBlox SNSPD flow (based on Hampel 2023) with the traveler.
- **Rejected:** grounding the Al only through Al wedge bonds at the M1 bond openings (those stay as a backup).
- **Reason:** a mirror left floating by a missing bond is the worst case for RF pickup (Hampel Fig. 3(a); DESIGN_LOG step 10). Claude proposed this reasoning; the team accepted the change.
- **Note:** this was decided for the die-wide Al. With the local-mirror architecture (below), the same idea grounds the local mirror strip.
- **How the mirror reaches ground (clarified 2026-11-12, at the team's request):**
  - The via is **not wire bonded**. It is a 100 × 100 µm opening through the 348 nm of SiO₂ (cap + spacer) at (−2140, 130) µm, under the Au ground fill. When the electrode Au is deposited, the fill's Au fills the opening and lands on the Al. That Au-on-Al contact is the whole connection.
  - Path to ground: carrier ground → wire bonds → GND-1…4 at (±4700, ±1500) µm → Au ground fill (one continuous sheet) → via → Al mirror. The mirror is grounded by the fill's own bonds, at least two of the four.
  - The only bonds that matter for the mirror are therefore the GND bonds; no separate mirror bond exists on the v4 dies.
  - The via's position is a layout call (DESIGN_LOG step 28), not part of this decision: just past the RF open end, to keep the mirror path short. It is on the left because the mirror runs along the SNSPD leads, which leave through the open end; the right end is closed by the RF U-bar and feed, so the Al cannot reach ground fill there without running under RF.
  - Cross-section: `design/fab/figures/stack_v4.svg`, panel (d) "Mirror ground via (detail)".
- **Details:** DESIGN_LOG step 22.

## 2026-11-08 · Hampel's local mirror as a variant first

*Backfilled 2026-11-08.*

- **Decision:** write Hampel's local Al mirror into the flow as a variant section, not as a replacement for the die-wide Al (DESIGN_LOG step 23).
- **Reason:** not recorded.
- **Superseded** the same day: the team adopted the local mirror as the architecture (next entry).

## 2026-11-08 · Architecture: local mirror, no 10 µm D2

- **Decision:** follow Hampel 2023. The Al is a local mirror under the SNSPD and along its leads, never under the RF rails. The electrodes sit on the thin optical stack; there is no 10 µm D2 and no deep gap etch.
- **Rejected:** die-wide Al ground plane under 10 µm of PECVD SiO₂ (the v3 baseline).
- **Reason:**
  - Optics: with vacuum directly above the cap, the cap can be tuned as a matching layer. Under 10 µm of SiO₂ it can't. Absorption is ~0.50 vs ~0.40 at 50 % fill (DESIGN_LOG step 9).
  - The ground plane mainly guards against RF loss in the substrate. NIST traps without one on Si with ρ > 20 kΩ·cm (Todaro 2021, Hampel 2023), so the team accepts dropping it.
- **Consequences:**
  - Order Si with ρ > 20 kΩ·cm (was > 10⁴ Ω·cm).
  - Measure the RF resonator Q with a die mounted.
  - Electrode Au thickness (E1 0.35 µm lift-off vs E2 6 µm plated) is still open.
- **Details:** `design/fab/variants/LOCAL_MIRROR.md`; `design/fab/figures/architecture_crosssection.svg`.

## 2026-11-08 · Local-mirror lead routing: slot along the centre DC

- **Decision:** make the SNSPD leads in the electrode Au, in the same step as the electrodes, in a slot along the centre DC, as Hampel 2023 does. Hampel's leads are made "together with the SNSPD leads, in a lift-off process" in 350 nm Au, and run between the RF electrodes over the mirror (SPIE Proc. 13025, Fig. 1).
- **Rejected:** keeping the leads buried under the centre DC and adding a thicker local SiO₂ over them.
- **Reason:** it matches Hampel and puts the leads in a step the process already has.
- **Consequences:** the centre DC splits around the slot, so the trap geometry changes and needs new simulations. The leads sit uncapped in the electrode plane, where the ion sees them.

## 2026-11-08 · R1_TRAP follows the new architecture

- **Decision:** R1_TRAP uses the local-mirror process. The NODET dies have no Al and no D2, and the Au electrodes sit on SiO₂ over high-resistivity Si (as Todaro did).
- **Rejected:** running the baseline D2 process first anyway.
- **Reason:** R1_TRAP should qualify the process the SNSPD dies will use.

## 2026-11-08 · Detector allocation: A30 only, drop B60

- **Decision:** keep only the A30 detector (30 × 30 µm window). B60 leaves the next full-stack run.
- **Rejected:** keeping both A30 and B60 in R1_FULL.
- **Reason:**
  - The 60 µm window lowers the ion more: v3 gave −2.50 µm for B60 against −1.38 µm for A30 (DESIGN_LOG step 19).
  - A larger exposed window floor has more area to become contaminated.
- **Status:** reversed the same day (next entry).

## 2026-11-08 · Detector allocation: keep B60 (reverses the entry above)

- **Decision:** keep both detector dies, A30 and B60, in the v4 design and in R1_FULL.
- **Rejected:** A30 only.
- **Reason:** the team reconsidered after the v4 numbers (DESIGN_LOG step 26), which change both earlier concerns:
  - Height: the B60 window lowers the ion by −2.04 µm with E2 and ≤ −0.55 µm with E1, against −2.50 µm in v3.
  - Exposed area: B60 adds 900 µm² of window floor. The slot's exposed SiO₂ gaps under the transport path are about 20× larger, and the floor now sits 0.3 µm above the grounded mirror.
  - B60 collects about 1.9× the light of A30 (4.2 % vs 2.2 % geometric).
  The team did not say which of these points decided it.
- **Later change:** on 2026-11-12 the team put A30 on the chips it needs and kept B60 only as a spare position (entry "Detector for the integrated chips" below).

## 2026-11-08 · Zone spacing 480 µm

- **Decision:** put the loading and readout zones 480 µm apart (x = −240 and +240 µm), instead of 600 µm.
- **Rejected:** the 600 µm spacing of the earlier layouts, which was a layout choice, not a recorded team decision.
- **Reason:** 480 µm matches the laser setup the team has in its system now.
- **Consequences (Claude's layout calls, DESIGN_LOG step 28):** the outer DC segment pitch goes from 100 to 120 µm, keeping 15 segments per side, so both zones sit on segment centres; step 3 found pitches from 75 to 150 µm equivalent. The detector, slot and mirror move with the readout zone.

## 2026-11-08 · Local mirror Al 450 nm thick

> Replaced on 2026-11-09: the mirror is now 100 nm, inlaid. See "Local mirror: 100 nm Al, inlaid" below.

- **Decision:** make the local Al mirror (layer 10, Al-1%Cu) 450 nm thick instead of 150 nm.
- **Rejected:** keeping 150 nm.
- **Reason:** lower the resistance of the mirror's path to ground. The RF rails drive current into the 2.5 mm strip, and at 150 nm (≈ 15 Ω) the detector end swings 20–27 mV and adds up to 0.65 µA of nanowire pickup. At 450 nm it is 7–9 mV and ≤ 0.21 µA (DESIGN_LOG step 28).
- **Consequences:** a longer Al sputter in the v4 traveler; no layout change. Check hillocks on a witness wafer after the spacer deposition (≤ 300 °C after the Al step).

## 2026-11-09 · Keep the 50 µm ion height

- **Decision:** keep the target ion height at 50 µm. No redesign for a lower trap.
- **Rejected:** redesigning for a lower ion to collect more light. The case worked through was 40 µm with the centre DC and the 30 µm window unchanged; 30 and 35 µm are in the same table.
- **Reason:** the team asked whether 50 µm should stay, given that a higher ion is more stable but collects less light, and adopted the analysis of DESIGN_LOG step 30 (`design/sim/17_height_tradeoff.py`) as its reason:
  - Going to 40 µm with the same window gives 1.44× the light. It costs 2.4× the heating (h⁻⁴ scaling; 1.8× at h⁻²·⁶) and 2.6× the laser power clipped on the 10 mm die, which is 1.7 % at 493 nm already.
  - Shrinking the whole trap with the height loses light, because the 5 µm rims and gaps do not shrink: 2.13 % at 50 µm against 1.72 % at 40 µm.
  - The same gain is available at 50 µm without those costs: the 160 nm SiO₂ cap (absorption 0.44 → 0.66), the B60 window (1.83×), E1 Au (1.22×) or a wider centre DC (1.3× at 50 µm).
  - The level reached is enough to work with: the A30 detector on E2 absorbs 1.47 % of all emitted 493 nm photons.
- **Limits the team accepted with it:** the analysis uses a gapless, infinitely long five-wire model; the heating exponent is not universal; the photon rate behind the count estimate comes from one paper.
- **Consequences:** no layout change. The height policy of 2026-11-02 (the height may differ between zones) stands.
- **Details:** DESIGN_LOG step 30.

## 2026-11-09 · Local mirror: 100 nm Al, inlaid (replaces the 450 nm of 2026-11-08)

> Changed on 2026-11-12: the mirror stays 100 nm but is raised, not inlaid. See "Local mirror: 100 nm Al, raised" below.

- **Decision:** the local Al mirror (layer 10) is 100 nm of evaporated Al, inlaid in the thermal SiO₂ so that its top is level with the SiO₂ beside it. Step 3 etches a 100 nm recess, evaporates the Al and lifts it off, all with one resist.
- **Rejected:**
  - 450 nm standing on the SiO₂ (the 2026-11-08 choice): it leaves a 0.45 µm step under the centre DC and the slot leads.
  - 450 nm inlaid: flat, but it needs a 450 nm Al lift-off into a recess that no source we have read covers.
  - 50 nm standing on the SiO₂, as Hampel 2023 built: about twice the strip heating and twice the extra nanowire current of 100 nm, and still a step.
  - 100 nm standing on the SiO₂: kept only as the fallback if the recess gives trouble (skip the recess etch; same mask).
- **Reason:**
  - We want the built electrodes to be the flat, coplanar geometry that every simulation assumes.
  - With E1, 0.35 µm of evaporated Au should not have to climb a 0.45 µm step where it leaves the mirror.
  - The reason for 450 nm did not hold up. We doubted that the mirror's extra pickup ends up in the SNSPD, since the mirror is grounded, and had it simulated (`design/sim/10c_mirror_thickness.py`, DESIGN_LOG step 37). About 3.2 mA of RF current flows along the strip to the ground via at any thickness. What can reach the nanowire is at most 0.16–0.21 µA at 450 nm and 0.73–0.97 µA at 100 nm inlaid (E2), next to 0.96 µA (E2) or 1.92 µA (E1) of direct pickup and a switching current of 8–20 µA. The ion is not affected: at most about 2 nm of micromotion on A30, against 55–173 nm from the window.
  - 100 nm rather than 50 nm: half the heating in the strip and half the extra nanowire current.
- **What we accept with it:**
  - More heat in the mirror strip: 34–45 µW at 100 nm inlaid against 7–10 µW at 450 nm (room-temperature resistivity, no thermal model). Hampel names RF heating as their remaining limit.
  - The mirror is evaporated Al, not Al-1%Cu, so hillocks after the ≤ 300 °C steps have to be checked.
  - The recess-and-lift-off step is not in any source we have read. It needs a witness wafer (W8) before a device wafer.
  - The simulation is 2-D with ideal conductors and gives upper bounds.
- **Consequences:** no layout change. Step 3 of the traveler is rewritten; the expected T10 strip resistance becomes 18.8–25.1 Ω instead of about 5 Ω; 0.9 µm of thermal SiO₂ remains under the mirror; new witness loop W8; the stack and process-flow figures show the inlaid mirror.
- **Details:** DESIGN_LOG steps 37 and 38.

## 2026-11-12 · One wafer for all four chips (run R1_ONE)

- **Decision:** fabricate the four chips the team's test plan needs on one wafer, in one run:
  - one chip with only SNSPDs;
  - two chips with an SNSPD integrated in the trap;
  - one chip with only the trap.
  The wafer carries a 3 × 3 block of 10 × 10 mm dies with spares: 4 A30, 1 B60, 2 SNSPD-only, 2 trap-only (NODET).
- **Rejected:**
  - the two-run sequence R1_TRAP then R1_FULL (2026-11-02);
  - a 2 × 2 block with exactly four dies and no spares;
  - a 4 × 4 block.
- **Reason:**
  - The chips follow the tests in the team's plan (teammate notes, `design/fab/`): the SNSPD alone and the SNSPD with trap RF at the SNSPD test setup; the trap alone and the SNSPD in the trap chamber.
  - The team has about one week of fab and wants the run "as easily fabricated as possible, with the least ways for complications to arise".
  - Spares: Claude proposed the 3 × 3 block because the tools write directly, so copies add write time but no process steps, and one bad die then does not cost a test. The team accepted.
- **Checked before deciding:** Claude went through every process step against every die type and found no step that harms a die that does not need it (DESIGN_LOG step 45). The trap-only die receives the blanket SiO₂ spacer, NbN (etched off again) and SiO₂ cap, so its electrodes sit on the same SiO₂ as the detector dies.
- **What the team accepts with it:** one wafer is a single point of failure; the trap-only chip waits for the detector steps; E1 or E2 applies to the whole wafer. Claude recommends a second wafer with only the electrode layer exposed as a backup; the team has not decided on it.
- **Consequences:** a new SNSPD-only die (`design/gds/make_snspd_die.py`); a new run preset `R1_ONE`; the separate test dies leave the run.

## 2026-11-12 · Detector for the integrated chips: A30, with B60 as a spare

- **Decision:** the two SNSPD + trap chips the team needs are A30 (30 × 30 µm window). One spare position on the wafer carries B60.
- **Rejected:** A30 on every integrated position; one A30 and one B60 as the two needed chips.
- **Reason:** A30 "is closer to the chip designed by Hampel" (team). The reason for keeping one B60 as a spare was not given.
- **Confirmed:** asked directly at the end of the session whether A30 is final for the two integrated chips, with one B60 die as a spare, the team answered yes.
- **Numbers the team had in front of it** (repo values, 6 µm Au): Hampel's detector is 20 × 30 µm; A30 absorbs 1.47 % of the emitted photons with 5.76 mm of nanowire and lowers the RF null 1.19 µm over the window; B60 absorbs 2.71 % with 11.04 mm and lowers it 2.04 µm.
- **Details:** DESIGN_LOG step 45.

## 2026-11-12 · Local mirror: 100 nm Al, raised (replaces "inlaid" of 2026-11-09)

- **Decision:** the local Al mirror is 100 nm of evaporated Al standing on the SiO₂, made by lift-off. There is no recess etch.
- **Rejected:** the inlaid mirror of 2026-11-09 (100 nm recess etched into the SiO₂ before the Al).
- **Reason:** about one week of fab, and the team wants the fewest ways for the run to go wrong. Claude pointed out that no source we have read covers the recess-and-lift-off step and that it needs a witness wafer first, and proposed the raised mirror, which was already the named fallback and uses the same mask. The team accepted.
- **What we accept with it:** a 100 nm step under the centre DC and the slot leads, so the electrodes are no longer exactly flat. `design/sim/10d_mirror_step.py` (DESIGN_LOG step 39) puts the effect at 0.13–0.16 µm of extra RF-null height.
- **Consequences:** no layout change. Step 3 loses its etch; witness loop W8 is no longer needed for the recess.

## 2026-11-12 · Alignment marks in Al, written with the mirror layer

- **Decision:** the alignment-mark shapes (GDS layer 1) are exposed together with the mirror layer and made in the same Al lift-off. The step that etched marks into the Si before the SiO₂ is dropped.
- **Rejected:** keeping the Si-etched marks; leaving the choice to the teammate writing the process flow.
- **Reason:** Claude proposed it as one lithography and one etch fewer, and so that wafers that already carry SiO₂ can be used as they are. The team accepted.
- **Consequences:** no layout change. The trap-only dies get four small Al crosses at their corners, 4.5 mm from the trap; they still have no Al under the electrodes. Later layers align to Al marks seen through the SiO₂ [verify on the tool]; the e-beam still aligns to its own Au crosses.

## 2026-11-12 · SNSPD leads stay Au in the slot; contacts thinned

- **Decision:** keep the SNSPD leads as Au strips in the centre-DC slot (2026-11-08). The short Ti/Au contact strips from the NbN tabs to the slot stay where they are.
- **Rejected for this run:**
  - NbN from each tab into the slot, with Ti/Au only as a pad in the slot;
  - NbN leads along the whole slot under the SiO₂ cap, with the Au strips as grounded shields.
- **Reason:** a team member was told that SNSPD leads can also be made of NbN, and the team asked what that would change. After the options were laid out, the team chose to keep the Au leads. The grounds Claude gave for that option: no layout change to the dies that are already checked, and the gain of the short NbN version is small once the contacts are thin.
- **Contact thickness:** the option the team chose was "keep Au leads, thin contacts", which sets the Ti/Au contact layer to Ti 5 / Au 50 nm instead of 10 / 350 nm. Claude proposed the value; see the entry "Final layer stack" below.
- **Details:** DESIGN_LOG step 45.

## 2026-11-12 · Final layer stack

- **Decision:** the layer thicknesses for run R1_ONE, bottom to top:
  - Si: high-resistivity float-zone, ρ > 20 kΩ·cm, thickness as supplied.
  - Base SiO₂: 1.0 µm thermal nominal; 0.5–2.0 µm accepted as supplied; a PECVD SiO₂ base if the wafers are bare.
  - Al mirror and alignment marks: 100 ± 10 nm evaporated Al, raised, lift-off (entries above).
  - SiO₂ spacer: 238 ± 10 nm PECVD SiO₂.
  - NbN: 7.0 ± 0.5 nm.
  - Ti/Au contacts and e-beam crosses: Ti 5 / Au 50 nm.
  - HSQ: 50 nm after develop, left on the wires only.
  - SiO₂ cap: 110 nm PECVD SiO₂ everywhere, which gives 160 ± 10 nm of SiO₂ over the wires.
  - Openings: 110 nm at the contacts, 348 nm at the mirror ground via, in one etch.
  - Test structures in this run: the 16 detector cells of the SNSPD-only dies, T3 and T11 only.
- **How it was decided:** the team asked Claude to finalize the layer thicknesses, paying attention specifically to the SiO₂ layers, and to plan any simulations itself. Claude proposed this table in its plan and the team approved the plan. The team also chose two of the items explicitly: the raised mirror, and "keep Au leads, thin contacts".
- **Confirmed:** asked directly at the end of the session whether the stack is final as logged, the team answered yes.
- **Rejected:**
  - Ti 10 / Au 350 nm contacts (the value carried from v3, when that layer was the leads).
  - Reading "160 nm" as the thickness of the PECVD SiO₂ cap itself; it is the total over the wires.
  - Moving the spacer to 240 nm, the best nominal of the RCWA scan (it gains 0.011 at the worst tolerance corner).
  - Thinning the base SiO₂ to the 150 nm and 134 nm of the reference devices.
- **Reason:** the reasons are Claude's analysis, which the team accepted with the plan; the team gave none of its own beyond wanting the stack final and as easy to fabricate as possible.
  - The HSQ stays on the wires only, so the cap that covers everything is 160 nm minus the HSQ. Off the wires 348 nm of SiO₂ lies between the Au and the Al, not 398 nm.
  - About 20 µm of each contact strip lies under the centre-DC Au with only that cap between, so the contacts have to be thin.
  - RCWA (`design/sim/24b_rcwa_stack_scan.py`): 0.828 absorbed at 238 nm / 160 nm; 0.753 at the worst ±10 nm corner.
  - Base SiO₂ (`design/sim/22b_base_sio2_sweep.py`): cold, the chip capacitance moves only from 2.88 to 2.38 pF over 0.15–2.0 µm; with the Si conducting it goes from 57.5 to 13.6 pF, so thinner than 0.5 µm is not accepted without need.
- **Not part of this decision, still open:**
  - Electrode Au, E1 (Ti 10 / Au 350 nm, lift-off) or E2 (seed + 6 µm plated). The team left it open on 2026-11-12; the thickness of each option is fixed.
  - What the team's wafers are (resistivity, SiO₂ already on them, thickness).
  - ITO: not in the stack (2026-11-07). The same scan shows an ITO layer on top would need a thinner SiO₂ cap (120 nm with 20 nm of ITO, 90 nm with 50 nm), so it cannot be added afterwards.
  - To verify on the tools: e-beam mark contrast on 50 nm Au; Au lost in the opening over-etch; layer-40 overlay ≤ 1 µm.
- **Details:** DESIGN_LOG step 45; `design/fab/STACK.md`.
