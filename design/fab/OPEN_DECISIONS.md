> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Updated 2026-11-12 for the one-wafer run `R1_ONE` and the team decisions of that day.

# Open design decisions and run requirements

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

The first section concerns design choices; the next sections prepare the run. An unchecked item does not reverse an adopted choice. Recipe values tagged **[verify]** remain provisional. Rows marked **final stack** hold the layer values that Claude proposed and the team approved with the plan on 2026-11-12 ([`notes/decisions.md`](../../notes/decisions.md), entry "Final layer stack"); they are listed here because each still carries items to verify on the tools. The map shows the design choices only; the checklists below carry the rest.

## Design choices

![Map of open design decisions](figures/open_decisions_map.svg)

The two architectures in cross-section: [architecture comparison](figures/architecture_crosssection.svg) (also in [Local mirror H.0](variants/LOCAL_MIRROR.md#h0-why-the-baseline-has-a-thick-d2-ground-plane-and-mirror-together)).

| Decision | Choices | What resolves it | Status |
| --- | --- | --- | --- |
| Electrode Au (v4) | E1: 0.35 µm lift-off (no plating); E2: 6 µm plated (as Todaro) | As traps they are the same (voltages equal to 0.01 V). They differ in four ways (DESIGN_LOG step 31, `sim/18`): screening of charge on the SiO₂ gap floor (0.80 for E1 against 0.023 for E2 [inference]); SNSPD lead resistance (69 Ω against 4 Ω per lead at room temperature); light and window perturbation (E1 collects 1.18× more; null drop ≤ 0.37 against 1.19 µm); RF heating (17× lower on E2 at equal capacitance; 14.6× at the computed chip capacitance of 2.39 pF for E1 and 2.59 pF for E2, `sim/22`, step 41). Common-mode RF current per SNSPD slot lead: 44.5 µA (E2) / 28.4 µA (E1) (`sim/10c`, case `al100_cap110`). Plus plating effort, step coverage and bondability | **Open.** No longer blocks the fab pages: both branches are written out (step 36). **Wafer-wide:** the choice applies to every die on the shared wafer of `R1_ONE`, so trying both E1 and E2 needs two wafers |
| Readout radial tilt | Keep 10°, smaller tilt, zero tilt, or wider DAC range | v3 needed 13.2 V (A30) / 15.2 V (B60). **v4 needs 6.3 V (A30) / 2.2 V (B60) for 10°** (loading 7.5 V; 480 µm zones) [team calc, steps 25, 27, 28] | Over-range problem gone on v4; team to confirm 10° |
| RF grounding / filters | Centre-DC filtering, carrier grounds, symmetric detector termination or cancellation; for v4 also an RF bypass at both SNSPD lead pads | v4 slot leads each collect 44.5 µA (E2) / 28.4 µA (E1) of common-mode RF over 2.24 mm (`sim/10c`, case `al100_cap110`); only termination asymmetry sends it through the nanowire (step 26). Lumped model (step 33, `sim/19`, upper bound): a plain 50 Ω line with the return lead grounded puts 4.1 µA (E2) / 2.6 µA (E1) through the A30 nanowire, against a switching current of 8–20 µA. These `sim/19` numbers are **not re-run**: they were computed with the earlier lead currents 44.5 / 28.6 µA, and the script's E1 input is 28.3 µA [verify]. A 1 nF bypass cuts it to 0.47 µA but low-passes the pulse at 3.2 MHz; a series L-C trap at 28 MHz gives 0.04 µA (0.23 µA if detuned 5 %); a differential 50 Ω / 50 Ω readout gives 0.20 µA per 5 % mismatch. DC-to-RF coupling (step 42, `sim/23`, 2-D): the centre DC couples to the rails through 0.41 pF (A30, E2); with 1 nF to ground it carries 22 mV of RF and moves the null 10 nm, with 10 nF 2.2 mV and 1.0 nm; left with no RF ground it would carry 6 V (45.5 V on NODET). An outer segment couples through 0.015 pF. Still needed: bond diagram, the filter values, RF-on/off tests | **Open; more important on v4** |
| Pad pitch / beam access | Current generated layout: 360 µm; alternatives recorded for the proposed choice: 180, 240, 300, 400 µm | Centre-to-centre PGA84L fan-out passes (worst 20.03°; step 29), as do all seven sim 12 cases. Closest top/bottom pads are at x = +0.62 / −0.98 mm; confirm clearance for a future perpendicular beam near the zones | **Team adoption pending.** Proposed reason: keep wire angles below 45° for a PGA84L-like package; no additional reason supplied |
| Carrier | PGA84L-like 84-pin package, 100-pin CPGA, or the lab carrier | Cryostat fit and a carrier-specific electrical pin map; step 29 checks nominal PGA84L geometry only. Local finger IDs in the fan-out table are not package pin numbers | **Open.** |
| Package spacer | Proposed thickness ≥ approximately 0.6 mm; die-sized (10 × 10 mm) or larger; Si suggested | Verify the actual carrier, die and spacer stack and beam clearance | **Open proposal [verify]**, not an adopted material or thickness |
| ITO cap over the detector (raised in the team notes as a possibility) | No ITO (adopted 2026-11-07, [decisions](../../notes/decisions.md)); ITO cap over the detector. The teammate notes of this week again raise an ITO cap. Sim 24b (`sim/24b_rcwa_stack_scan.py`) computes what a top ITO layer does to the optics; its result (DESIGN_LOG step 45): on the stack as specified (160 nm of SiO₂ over the wires) ITO lowers the NbN absorption from 0.83 to 0.68 (20 nm of ITO) or 0.42 (50 nm); re-tuned, the best SiO₂ over the wires becomes 120 nm (0.87) or 90 nm (0.91). So ITO has to be chosen before the SiO₂ cap is deposited | The team reopening the 2026-11-07 decision "No ITO anywhere" ([decisions](../../notes/decisions.md)) | **Possibility, not adopted.** Conflicts with the 2026-11-07 decision "No ITO anywhere"; it stands only if the team reopens that decision |
| Base SiO₂ (final stack, 2026-11-12) | 1.0 µm thermal SiO₂ nominal; accept 0.5–2.0 µm as supplied. If the wafers arrive bare: thermal oxidation, or a PECVD SiO₂ base (Hampel 2023 used 150 nm PECVD SiO₂, Todaro 2021 134 nm [verify]) | Cold chip capacitance moves only from 2.88 to 2.38 pF (E2) across 0.15–2.0 µm (`sim/22b`). Warm, the capacitance to the conducting Si goes roughly as 1 / thickness: 22.8 pF at 1.0 µm (room-temperature limit, E2). Whether the team's wafers already carry SiO₂ (see the wafer row below) | **Decided 2026-11-12** with the final stack ([decisions](../../notes/decisions.md)); proposed by Claude, approved by the team with the plan. The [verify] items stay open |
| Ti/Au contacts, layer 22 (final stack, 2026-11-12) | Ti 5 nm / Au 50 nm (was 10 / 350 nm). Contacts from the NbN tabs into the slot, and e-beam crosses only | Thin on purpose. The Au is the etch stop for the opening etch: the fluorine plasma that opens the SiO₂ also etches NbN, and 7 nm cannot stop it. About 20 µm of each contact strip lies under the centre-DC Au with only the 110 nm cap between, so it must be thin. 350 nm has no job in v4. [verify] e-beam mark contrast on 50 nm Au; [verify] the Au lost in the opening over-etch | **Decided 2026-11-12** with the final stack ([decisions](../../notes/decisions.md)); proposed by Claude, approved by the team with the plan. The [verify] items stay open |
| HSQ and SiO₂ cap (final stack, 2026-11-12) | HSQ 50 nm after develop, on the NbN wires only (target, measured on the wafer). One blanket PECVD SiO₂ cap of 110 nm | HSQ plus cap give **160 ± 10 nm** of SiO₂ over the wires (the window stack of `sim/09c` and `sim/15b`). Off the wires the SiO₂ between Au and Al is 238 + 110 = **348 nm** (mirror ground via). Openings (layer 40) are one etch: 110 nm at the contact pads, 348 nm at the mirror via | **Decided 2026-11-12** with the final stack ([decisions](../../notes/decisions.md)); proposed by Claude, approved by the team with the plan. The [verify] items stay open |
| SiO₂ spacer (final stack, 2026-11-12) | 238 ± 10 nm PECVD SiO₂, ≤ 300 °C, between the Al mirror and the NbN; kept from the earlier pass | Sim 24b (RCWA, DESIGN_LOG step 45): 0.828 absorbed at 238 nm spacer / 160 nm over the wires; ±10 nm box mean 0.803, worst corner 0.753; the best nominal on the grid (240 / 160 nm) has a worst corner only 0.011 higher, so 238 nm is kept | **Decided 2026-11-12** with the final stack ([decisions](../../notes/decisions.md)); proposed by Claude, approved by the team with the plan. The [verify] items stay open |
| Test structures in `R1_ONE` (final stack, 2026-11-12) | Kept: the 16 detector cells on the two SNSPD-only dies, T3 (NbN four-wire bar) and T11 (Au-to-Al via chain). Dropped from this run: TEST and TEST_TRAP dies, T1, T2v, T4, T4b, T6, T8, T9, T10, T12 | Where the measurements are done in `R1_ONE`: the detector cells and T3 / T11 on the SNSPD-only dies, T3 and T11 probe-station only. The layer-20 dose datatypes on the SNSPD-only dies (dose factors 0.80–1.20) stand in for the T8 dose array [inference]. No other stand-in is named in the repo [verify]. The mirror strip (T10) is not measured in this run | **Decided 2026-11-12** with the final stack ([decisions](../../notes/decisions.md)); proposed by Claude, approved by the team with the plan. The [verify] items stay open |
| Team's wafers (new, 2026-11-12) | Resistivity of the Si, SiO₂ on the wafers, and its thickness | Not known yet. [verify on the wafer box]. Decides whether step 2 (base SiO₂) is run, and whether the base SiO₂ row above is needed | **Open** |
| Second wafer with only layer 50 exposed (new, 2026-11-12) | (a) one wafer, `R1_ONE` only; (b) plus a second wafer with ONLY layer 50 exposed, from the same run file (no new layout) | Trap-only backup if the one wafer fails; also the trial of the electrode step and of wire bonding. Claude recommends (b); the team has not decided. It is also the only way to try both E1 and E2 | **Open; recommended, not decided** |
| Tool limits for one wafer (new, 2026-11-12) | The NbN sputter tool and the e-beam holder must take a 100 mm wafer; the e-beam, the CF₄ etcher and the PECVD must accept a wafer that already carries the Au contacts from step 6 | [verify] on the tools; the process steps were checked against each die type, the tools were not | **Open [verify]** |
| NbN leads for a later run (new, 2026-11-12) | (a) Au leads in the slot (chosen for `R1_ONE`); (b) NbN from the tab into the slot, with Ti/Au only as a pad in the slot; (c) NbN along the whole slot under the SiO₂ cap, with the Au strips as grounded shields | Not in this run (decided 2026-11-12). Options written up in [variants/LOCAL_MIRROR.md](variants/LOCAL_MIRROR.md), section "NbN leads (considered 2026-11-12, not built)" | **Later run only; not built** |

**One-page briefs** (numbers and sources side by side; no recommendation): [E1 vs E2](briefs/E1_vs_E2.md) · [readout tilt](briefs/readout_tilt.md) · [RF grounding and lead termination](briefs/rf_grounding_and_termination.md) · [pad pitch](briefs/pad_pitch.md) · [carrier and spacer](briefs/carrier_and_spacer.md) · [mirror, raised or inlaid](briefs/mirror_raised_vs_inlaid.md).

**Resolved 2026-11-08** ([decisions](../../notes/decisions.md)): architecture → local mirror, no D2; lead routing → Au leads in a slot along the centre DC; detector allocation → keep A30 and B60 (B60 was dropped, then kept); R1_TRAP → the same no-Al stack.

**Resolved 2026-11-12 (decisions)** ([decisions](../../notes/decisions.md)): one wafer for all four chips (run `R1_ONE`, 3 × 3); A30 on the chips the team needs, B60 as one spare; Al mirror 100 nm raised; alignment marks in Al with the mirror layer; SNSPD leads stay Au in the slot; the final layer stack (proposed by Claude, approved with the plan).

## Checklists

The run that is planned now is `R1_ONE`. Its checklist is first. The earlier checklists (for `R1_TRAP` and `R1_FULL`) are kept below as history; items that the 2026-11-12 decisions closed are struck through and marked.

### Before R1_ONE

The chips: 4 A30, 1 B60 (spare), 2 SNSPD-only, 2 NODET; see [`design/gds/run_R1_ONE_map.csv`](../gds/run_R1_ONE_map.csv) for the die IDs.

- [ ] Choose E1 vs E2. It is wafer-wide: trying both needs two wafers. The fab pages carry both branches until then.
- [ ] Decide on the optional second wafer with ONLY layer 50 exposed (recommended by Claude, not decided by the team).
- [ ] The team's wafers: Si resistivity (ρ > 20 kΩ·cm), the SiO₂ on them, and its thickness [verify on the wafer box]. Decides whether step 2 (base SiO₂) is run.
- [ ] Tool limits for one wafer [verify]: the NbN sputter tool and the e-beam holder must take a 100 mm wafer; the e-beam, the CF₄ etcher and the PECVD must accept a wafer that already carries the Au contacts from step 6.
- [ ] Schedule: the trap-only die (NODET) needs only the electrode module, but it waits for every detector step.
- [ ] Au tools at MIT.nano: Au-compatible tools, the gold plating tank and its minimum area (if E2), the Ti/Au evaporator (E1), holders and training order.
- [x] **Al mirror: 100 nm Al, raised, lift-off, no recess** (team decision 2026-11-12). *Closed 2026-11-12: mirror raised.* The recess witness, the raised-or-inlaid choice, and the recess facility items (an Al source, the SiO₂ RIE recipe, the over-etch into Al) are closed with it.
- [ ] Witness W8 "Al mirror, raised (step 3)" ([QUALIFICATION](QUALIFICATION.md#w8-al-mirror-raised-step-3)): residual step and edge profile after lift-off; hillocks in evaporated Al after the ≤ 300 °C steps [verify].
- [ ] Mirror edge: the 100 nm step now lies on the centre-DC edge (raised mirror). The Au crosses that step on both branches; check for a break at the edge [verify]. Narrowing the mirror to \|y\| ≤ 18 µm stays an optional proposal, not done: it changes layer 10 of the released A30 and B60 dies.
- [ ] Mirror ground via: the via now crosses 348 nm of SiO₂ to the Al (step 11). Compare the Au-to-Al contact at the via with and without the Ar pre-clean; confirm the AJA substrate RF etch. T11 measures the via chain on the SNSPD-only dies.
- [ ] Mirror strip heating: 32.9–43.9 µW (E2) / 34.2–45.6 µW (E1) in the Al strip at 53 V, 28 MHz (room-temperature resistivity; no thermal model). In the cold RF test, watch the SNSPD switching current against RF amplitude.
- [ ] Layer-40 overlay to layer 22 must be ≤ 1 µm: the contact openings have 1 µm of drawn margin. (The page used ±5 µm before.)
- [ ] e-beam cross distance: the e-beam crosses on the trap die sit about 760 µm from the meander, outside one write field [verify the alignment procedure].
- [ ] e-beam mark contrast on 50 nm Au [verify]: the layer-22 crosses are 50 nm Au.
- [ ] Alignment: layer 1 (marks) is written in Al with layer 10, in one exposure and one lift-off. Layers 22, 40 and 50 align to the Al marks seen through the SiO₂ [verify on the MLA150]; the e-beam aligns layer 20 to the layer-22 Au crosses.
- [ ] After the NbN etch (step 7), an open field must read open circuit between two probes.
- [ ] On a finished trap die, pad-to-pad leakage between neighbouring electrodes.
- [ ] Check the four Al crosses at the corners of each NODET die (4.5 mm from the trap). They are the only Al on that die.
- [ ] Bond pads: confirm the 16 Au bond pads of the SNSPD-only die (120 × 200 µm) can be bonded for cold tests; the W7 bond-and-leak loop covers the trap dies ([QUALIFICATION](QUALIFICATION.md)).
- [ ] Test structures: set the acceptance limits for T3 (NbN bar) and T11 (Au-to-Al via chain). T10 is not in `R1_ONE`; decide whether a mirror-strip measurement is still wanted (team).
- [ ] Measure the Au film resistivity at 4 K on a witness (E1 evaporated, E2 plated). No value was found in the literature, and the SNSPD lead resistance on E1 depends on it (step 31).
- [ ] Measure the switching current and the count plateau at operating temperature with RF off and on.
- [ ] Compare charging drift and click-induced heating over bare SiO₂ with NODET.
- [ ] Verify mark coordinates, polarity and die IDs against [layout](LAYOUT.md) and [exposure checklist](mask_list.md#4-export-checklist-per-job). No fabricated layer carries a die label, so identify dies by the run map.
- [ ] Facility questions for MIT.nano staff listed in [05_SIMPLER_TESTING](tests/05_SIMPLER_TESTING.md) and [00_SETUP](tests/00_SETUP.md), where they apply to this run.

**Questions the 2026-11-12 pass answered** (from the page rewrite of 2026-11-09):

- [x] *Does the trap-only run also deposit the 238 nm spacer and the 110 nm cap, so its electrodes sit on the same surface as the detector dies?* Answer for `R1_ONE`: yes. Every die gets the blanket films. The NODET die's Au sits on base SiO₂ + spacer + cap, the same surface as A30. (`R1_TRAP` is no longer run.)
- [x] *Do NODET dies get steps 4–8?* Answer for `R1_ONE`: they get the blanket steps 2 (if the wafer is bare), 4, 5 and 8. Step 5 deposits NbN, and the step 7 CF₄ etch removes it again; no HSQ or Ti/Au is drawn on them (step 6 is written only where drawn). Their only Al is the four corner crosses from step 3. [verify] on the tool.
- [x] *Which witness covers the 300 °C cap deposition on NbN?* Answer: none is named in the repo. On the shared wafer, a co-loaded NbN piece goes through the cap deposition [verify].

### Other open items (not tied to one run)

- [ ] Transport hardware: the DAC update rate, resolution and filter corner used in `sim/21` are **[verify]** (lab hardware not known). Avoid an update rate that divides the axial frequency exactly: at 100 kHz and 0.8 MHz the model leaves 5 × 10⁶ quanta whatever the move time (step 40).
- [ ] Order Si with ρ > 20 kΩ·cm; measure the RF resonator Q with a die mounted. Measure it cold: at room temperature about 63 % of the RF field energy is in Si with a loss tangent near 0.27 at 28 MHz, so the warm Q is low and does not predict the cold value (step 41, first-order estimate).

### Detector documents and generated layouts

> [!note] Reconciled 2026-11-09 against the released files
> [`gds/measured_v4.md`](../gds/measured_v4.md) is written by `gds/measure_dies.py` from the GDS files themselves and records each file's hash. The pages now cite it. Regenerate it after any layout change and before an exposure export; a hash that differs from the table means the numbers are stale.

- [x] Record the generator revision for trap dies, test die and run GDS; verify the generated files match the 130/200 nm rounded-turn geometry. Measured: 160 lines, 0.130 µm wide on a 0.200 µm pitch, 36 µm (A30) / 69 µm (B60) long (step 35).
- [x] Check detector/test-die geometry, contact connectivity and clearances, including T9. `gds/check_test_die.py` passes: 20 NbN pieces, each on its own leads; every meander on its own Al mirror. The run maps use the v4 dies.
- [x] Re-measure the layer areas for both runs: in `gds/measured_v4.md` (Au 5.917 cm² for R1_TRAP, 5.735 cm² for R1_FULL; EBL 0.0496 mm² for R1_FULL). EBL time and charge still depend on the dose from W2.
- [x] 2026-11-12, `R1_ONE`: Au (layer 50) 8.27 cm²; layer 20 (e-beam) 0.0372 mm² on 7 of the 9 dies, 21 meanders (4 A30, 1 B60, 16 on the two SNSPD-only dies). Source: `gds/check_run.py R1_ONE`, which reports ALL CHECKS PASS.
- [ ] Calibrate the 130/70 nm SEM target on W2. Validate the separate T9 screening criteria in electrical test a14.
- [x] Verify square count, inductance and reset time against the released GDS: straight sections 5.760 / 11.040 mm, 3.10 / 5.94 µH, 62.0 / 118.8 ns (turns, tapers and tabs excluded). The resistance acceptance in a7 still needs the measured sheet resistance.
- [x] `sim/15_snspd_geometry.py` and the GDS both use the 32 µm radial extent (DESIGN_LOG step 24: OVH_Y = 1 µm after the sim/10 v3.1 RF scan).
- [x] Reconcile absorption and RF pickup for the changed fill factor/footprint: absorption in steps 26 and 32 (0.66 with the 160 nm cap), pickup in steps 26, 28 and 33. Switching current itself is still an estimate (8–20 µA) until the cold test.

Sources: [trap generator](../gds/make_chip.py), [test generator](../gds/make_test_die.py), [geometry study](../sim/15_snspd_geometry.py), [geometry audit](../research/reports/SNSPD%20geometry%20audit.md).

### Earlier checklists (history)

> Superseded as the run plan by `R1_ONE` (2026-11-12). Kept so the record is complete. Struck items were closed by the 2026-11-12 decisions or moved into "Before R1_ONE".

#### Before any v4 run

- [ ] Choose E1 vs E2. The fab pages no longer wait for it. (Still open; see "Before R1_ONE".)
- [x] Rewrite the traveler, R1_TRAP run sheet, mask list, stack and qualification pages for v4: done 2026-11-09 with E1 and E2 as parallel branches (DESIGN_LOG step 36). When the team chooses, delete the other branch.
- [x] Rework the test dies for v4: done 2026-11-09 (`gds/test_die_v4`, `test_die_v4_TRAP`; step 35). T2 is replaced by T2v; T10, T11 and T12 are new; TEST_TRAP carries T1 and T6 only, with no Al. Both pass `gds/check_test_die.py`. Not in `R1_ONE` (2026-11-12); the files are kept.
- [x] **Al mirror: 100 nm, inlaid** (team decision 2026-11-09, [decisions](../../notes/decisions.md); DESIGN_LOG steps 37 and 38). It replaced the 450 nm mirror, which left a 0.45 µm step under the centre DC and the slot leads. *Closed 2026-11-12: mirror raised (100 nm standing on the SiO₂, no recess).* The inlaid process (resist, 100 nm SiO₂ recess, Al evaporation, lift-off) is kept only as the comparison in the [mirror brief](briefs/mirror_raised_vs_inlaid.md).
- [ ] **Mirror edge on the centre-DC edge (DESIGN_LOG step 39, `sim/10d`).** With E1, a mirror 2 µm off centre moves the RF null 0.5 µm sideways, and 5 µm off moves it 1.05 µm; with E2 it is 15–30 nm. The step of a raised 100 nm mirror is small by comparison (null 0.13–0.16 µm higher, uniform). Proposal: narrow the mirror to \|y\| ≤ 18 µm (layer 10 of A30 and B60 only; 2 µm beyond the NbN, 2 µm inside the Au), and hold the layer-10 overlay to about 1 µm instead of the ±5 µm on the [mask list](mask_list.md). Not done: it changes the released dies. Optional: the shift is static and the DC electrodes compensate it (about 18 V/m per µm of shift; with no trim the ion still follows the null to within about 4 %), so this only saves a trim (step 39 addendum).
- [x] ~~**Raised or inlaid**~~ *Closed 2026-11-12: raised* (team decision, [decisions](../../notes/decisions.md)). For the ion the two are equivalent at 100 nm (step 39).
- [x] ~~**Inlaid mirror, to prove before a device wafer:** witness loop W8, recess depth and RIE rate~~ *Closed 2026-11-12: mirror raised, no recess.* The W8 witness is now "W8 Al mirror, raised (step 3)" ([QUALIFICATION](QUALIFICATION.md#w8-al-mirror-raised-step-3)); its open parts are in "Before R1_ONE".
- [x] ~~**Inlaid mirror, facility:** an Al source on the E1 evaporator; the SiO₂ RIE recipe and rate on our tool; over-etch into the 100 nm Al at the mirror via (step 11).~~ *Closed 2026-11-12: mirror raised.* The over-etch into Al at the via remains in "Before R1_ONE".
- [ ] **Mirror strip heating:** 32.9–43.9 µW (E2) / 34.2–45.6 µW (E1) in the strip at 53 V, 28 MHz (room-temperature resistivity; no thermal model). In the cold RF test, watch the SNSPD switching current against RF amplitude.
- [x] Mirror ground path: via moved to just past the RF open end (step 28). The Al was 450 nm from 2026-11-08, then 100 nm inlaid from 2026-11-09, and is **100 nm raised** from 2026-11-12: swing 29.7–39.6 mV, at most +0.72–0.96 µA (E2) (`sim/10c`, case `al100_cap110`; DESIGN_LOG step 37). The strip is measured on test structure T10 (62.75 squares, 18.8–25.1 Ω expected) in the old test die, and the via contact on T11. T10 is not in `R1_ONE`. The hillock check moved to "Before R1_ONE" (W8).
- [x] 09c optics (step 26): **set the SiO₂ over the wires (HSQ + cap) to 160 ± 10 nm**: A 0.44 → 0.66 (v3.1: 0.54). The pages, `make_chip.py` and the `_sim.json` files now all say 160 nm (step 35).
- [x] 10b RF pickup (step 26): nanowire 0.96 µA (E2) / 1.92 µA (E1) vs 1.67 µA (v3.1); slot-lead pickup feeds the RF grounding decision above.
- [x] Rerun 15 at the v4 heights: done as `sim/15b_collection_v4.py` (step 32). A30 E2 collects 2.22 % and absorbs 1.47 % of all emitted photons with the 160 nm cap; B60 E2 4.16 % and 2.71 %.
- [x] Transport: hold the centre DC at 0 V while moving and ramp the tilt in at each zone (`12_final_chip_check.py --centre-dc-zero`: **1.708 V per 10 µm step** on A30/B60 with the 480 µm zone spacing and 360 µm pad pitch; free-centre transport 7.590 / 8.002 V, step 29). The constrained static 10° zone solves remain diagnostic; use the regular zone sets once stationary.
- [x] Transport waveform (steps 34 and 40, `sim/20`, `sim/21`): `sim/out/21_transport_waveform/<die>/waveform.csv` holds voltages against time for a 1 ms minimum-jerk move with the tilt ramped out and in, sampled at 1 MHz and quantised to 16 bit. It reproduces the sim 12 table to 5 µV; interpolation puts the well within 0.01 nm of its target (0.29 nm on B60, solved on a 5 µm grid); at 1 MHz updates the classical model leaves under 10⁻³ quanta.
- [ ] Transport hardware: moved to "Other open items".
- [ ] Order Si with ρ > 20 kΩ·cm; measure the RF resonator Q with a die mounted: moved to "Other open items".
- [x] New from the page rewrite (step 36): the three questions (trap-only spacer and cap; NODET steps 4–8; witness for the 300 °C cap on NbN) are answered under "Before R1_ONE".
- [ ] Measure the Au film resistivity at 4 K: moved to "Before R1_ONE".

#### Before R1_TRAP

- [ ] Confirm Au-compatible tools, gold bath/minimum area, holders and training order with MIT.nano. (Moved to "Before R1_ONE".)
- [x] ~~W3: qualify D2 stress/backside compensation and chuck bow limit; calibrate L40 and gap etches.~~ Not needed for v4 (no D2, no gap etch). The L40 cap + spacer etch (≈ 0.40 µm, stopping on the 100 nm Al) still needs a short calibration before R1_FULL. *Superseded 2026-11-12: the via now crosses 348 nm of SiO₂, not 0.40 µm; see "Before R1_ONE".*
- [ ] Before R1_FULL (v4 A30/B60): compare Au-to-Al contact at the mirror via with/without Ar pre-clean; confirm the AJA substrate RF etch. R1_TRAP has no Al. (Moved to "Before R1_ONE".)
- [ ] W5 (only if E2): calibrate plating current on the R1_TRAP pattern; check thickness, gaps and bondability. If E1: lift-off of 0.35 µm Au over 5 µm gaps and wedge bonding on evaporated Au instead.
- [ ] W7: bond-and-leak loop; confirm bonder/wedge dimensions and carrier bond diagram.
- [ ] Verify mark coordinates, polarity and die IDs against [layout](LAYOUT.md) and [exposure checklist](mask_list.md#4-export-checklist-per-job).

See [Qualification](QUALIFICATION.md). No completed witness-wafer measurements are recorded in the reviewed progress notes.

#### Before R1_FULL

- [x] Finish detector reconciliation above. *R1_FULL is superseded by R1_ONE (2026-11-12).*
- [ ] Obtain the full NbN recipe and sputter access; W1-a/b qualify the real stack and thermal history.
- [ ] W2: set HSQ dose/development/etch on the actual EBL tool; confirm mark recognition and L22-to-L50 overlay.
- [ ] Confirm test-die detector pads can be bonded for cold tests. In `R1_ONE` this is the SNSPD-only die's bond pads (see "Before R1_ONE").
- [ ] Measure switching current and count plateau at operating temperature with RF off/on. The geometry audit questions the earlier 15–25 µA estimate; cold-test acceptance remains provisional.
- [ ] Compare charging drift and click-induced heating over bare SiO₂ with NODET.

## Source and model checks

- [x] Resolve "Dietl 2025": M. Dietl et al., "Test and characterization of multilayer ion traps on fused silica", arXiv:2505.21284 ([literature note](../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md)). Its Table 2 gives the 50 V DC / 300 V RF, 0–100 nA leakage limits and the 1 mA, 0–100 mV continuity test. Those traps have Al electrodes on fused silica. No comb structure or flashover measurement was found in it, so the T1 limits stay **[verify]**. The paper was read through a summarising tool: check the table against the PDF.
- [ ] Ba⁺ angular-emission model, partly resolved: the π and σ patterns of a J = 1/2 upper level sum to 1/(4π) (algebra, [team calc]), and Auzinsh, Budker and Rochester (arXiv:0908.2666, Sec. II.4) state that fluorescence shows excited-state polarization of rank at most 2J_e, so J_e = 1/2 carries no alignment ([literature note](../research/research_notes/Loose%20ends%202026-11/L1_ba_emission_and_detection.md)). No textbook passage stating the isotropy outright was opened. The polarisation is not isotropic, and the meander absorbs the two polarisations differently.
- [ ] Suleimen 2026 is Phys. Rev. Applied 25, 044091; only the abstract is open. Read the full text before using its width comparison (T9).
- [x] RCWA of the meander at normal incidence (step 43, `sim/24`): 0.83 unpolarised with the 160 nm cap, against 0.66 from the effective-medium model; the difference is in the polarisation across the wires. The key-number tables still quote the effective-medium value.
- [ ] Still open: RCWA averaged over the ion's emission cone (or FDTD); the 3-D pickup on the SNSPD leads (step 42 says why the planned method was not attempted); a second RCWA code as a cross-check.
- [x] Chip RF capacitance (step 41, `sim/22`): 2.59 pF (A30, E2), 2.39 pF (A30, E1), from 2-D sections of the RF net; 24.2 / 22.3 mA at 53 V, 28 MHz.
- [ ] Not measured: the loss tangent of the PECVD and thermal SiO₂ (sets the cold Q of the chip, step 41).
- [x] ~~Reconcile the full-stack physical Al-to-Au separation (~10.3 µm) with the model's 10.0 µm ground-depth parameter.~~ v3 only: v4 has no ground plane (`ground_depth: null`).

## Choices already recorded as the team's

Project scope and fixed inputs, separate loading zone, high-resistivity Si, 50 µm height and the height policy, no bowtie, the narrow die (superseded), NODET die, R&D runs at MIT.nano, R1_TRAP first (all 2026-11-02, backfilled); no ITO and 10 × 10 mm edge-pad dies (2026-11-07); on-chip Au-fill-to-Al via (2026-11-08); local-mirror architecture, slot leads, A30 only then A30 + B60 retained, R1_TRAP on the v4 stack (2026-11-08). 2026-11-12: one wafer for all four chips (run `R1_ONE`, which replaces the R1_TRAP-then-R1_FULL plan); A30 on the chips the team needs, with B60 as one spare; Al mirror 100 nm raised; alignment marks in Al with the mirror layer; SNSPD leads stay Au in the slot; the final layer stack (proposed by Claude, approved with the plan). All are logged in [`notes/decisions.md`](../../notes/decisions.md), which Claude now writes for the team. Current layout uses 480 µm zone spacing and 0.8 MHz axial confinement. The generated 360 µm pad pitch remains pending team adoption (step 29).

The 50 µm height was checked again on 2026-11-09 (DESIGN_LOG step 30, `sim/17`): going to 40 µm with the same window gives 1.44× the light for 2.4× the heating and 2.6× the clipped beam power, and the same gain is available at 50 µm from the 160 nm cap, B60, E1 or a wider centre DC. The team adopted this as its reason for keeping 50 µm on 2026-11-09 ([decisions](../../notes/decisions.md)).
