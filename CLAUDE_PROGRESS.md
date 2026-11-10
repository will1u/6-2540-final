# Claude progress: five-wire Ba⁺ trap with an integrated NbN SNSPD

> **Claude-authored running status.** Last update: 2026-11-09 (loose-ends pass: DESIGN_LOG steps 30–36; fab pages, test dies and figures are now v4; 50 µm height and E1 vs E2 assessed). Before that: 2026-11-08 (v4 local-mirror architecture, slot leads, A30 + B60; 360 µm pad layout validated, team adoption pending).
> - Full detail with numbers and citations for every step: [design log](design/DESIGN_LOG.md) (numbered design steps and documentation updates).
> - New team member? Set up the `electrode` repo first: `design/CLAUDE.md`, "Setting up the electrode repo".
> - Folder index and how to run: `design/README.md`.

**2026-11-09, loose-ends pass (DESIGN_LOG steps 30–36).** Written by delegated agents from a specification; every number below was rerun before logging. One team decision came out of it: keep the 50 µm ion height (logged in `notes/decisions.md`). The rest are assessments, not decisions.
- **Ion height (step 30, `sim/17`; team decision 2026-11-09: keep 50 µm):** 50 µm is adequate. Going to 40 µm with the same 30 µm window gives 1.44× the light for 2.4× the heating (h⁻⁴) and 2.6× the clipped beam power; shrinking the whole trap loses light. The same gain is available at 50 µm from the 160 nm cap, B60, E1 or a wider centre DC.
- **E1 vs E2 (step 31, `sim/18`):** identical as traps. E2 screens charge on the SiO₂ gap floor about 35× better and its SNSPD leads are 4 Ω instead of 69 Ω each (room temperature). E1 collects 1.18× more light and perturbs the RF null about three times less. The choice is still the team's.
- **Collection on v4 (step 32, `sim/15b`):** A30 on E2 collects 2.22 % and absorbs 1.47 % of all emitted 493 nm photons with the 160 nm cap; B60 4.16 % and 2.71 %.
- **SNSPD lead termination (step 33, `sim/19`):** a plain 50 Ω line with the return grounded puts about 4.1 µA of 28 MHz current through the A30 nanowire on E2 (switching current 8–20 µA). A 28 MHz L-C trap or a differential readout brings it below 0.3 µA; a 1 nF bypass also low-passes the pulse at 3.2 MHz.
- **Transport timing (step 34, `sim/20`):** smooth ramps are easy (minimum-jerk: < 0.1 quanta above 44 µs). The 10 µm voltage table is not a waveform: it must be interpolated well below 1 µm per DAC update.
- **Layouts (step 35):** v4 test dies `test_die_v4` / `test_die_v4_TRAP` with an independent checker; the cap is 160 nm in `make_chip.py` and the sim metadata; `gds/measured_v4.md` holds areas, squares and hashes measured from the released files.
- **Raised or misaligned mirror (step 39, `sim/10d`; open):** a 100 nm raised mirror only lifts the RF null by 0.13–0.16 µm, uniformly, with q changed by under 0.5 %, so for the ion raised and inlaid are equivalent. The larger effect is misalignment of the mirror on E1: 2 µm off centre moves the null 0.5 µm sideways (5 µm: 1.05 µm), against 15–30 nm on E2, because the mirror edge is drawn on the centre-DC edge and a shifted mirror reaches under the gap. The shift is static and the DC electrodes compensate it (about 18 V/m per µm; untrimmed, the ion still follows the null to within about 4 %), so it is not a problem. Optional proposal: narrow the mirror to |y| ≤ 18 µm (layer 10 only) and hold the layer-10 overlay to about 1 µm.
- **Al mirror: 100 nm, inlaid (step 38; team decision 2026-11-09, `notes/decisions.md`).** Step 3 is now resist, a 100 nm recess in the thermal SiO₂, Al evaporation and lift-off with one resist, so the SiO₂ cap and all the Au are at one level. `sim/10c`: 3.2 mA goes along the strip to ground; the extra nanowire current is at most 0.73–0.97 µA (E2); the strip dissipates 34–45 µW; T10 is expected at 18.8–25.1 Ω. Every fab page and both figures are updated. Unproven until witness loop W8 passes; fallback is the same mirror without the recess.
- **Al mirror thickness, the analysis behind it (step 37, `sim/10c`):** the 450 nm mirror stands 0.45 µm proud of the SiO₂ beside it, so the centre DC and slot leads sit 0.45 µm above the RF rails. Its pickup goes to ground (about 3.1 mA along the strip); the part that can reach the nanowire is ≤ 0.2 µA at 450 nm, ≤ 1.0 µA at 100 nm and ≤ 1.9 µA at 50 nm, next to a direct pickup of 0.96–1.92 µA. The ion does not notice. A thin mirror costs heat: 65–87 µW in a 50 nm strip against 7–10 µW at 450 nm. The team chose 100 nm, inlaid (step 38).
- **Fab pages (step 36):** every page in `design/fab/` is v4, with E1 and E2 written as equal branches; two new figures, `fab/figures/stack_v4.svg` and `process_flow_v4.svg`.

**2026-11-08, v4 SNSPD overhang audit:** completed the requested GDS, ray-footprint, optical-stack and straight-wire inductance checks for A30/B60, E1/E2 and 80/160 nm SiO₂ caps; see the final audit entry in `design/DESIGN_LOG.md`. Centred overhang causes no ray-envelope collection loss; its main quantified cost is about 14/22 ns of extra straight-section current-recovery time constant. Radial alignment margin is about 0.93 µm at 160 nm cap. The generator metadata and the process pages say 160 nm since step 35. No layout or design choice changed; actual switching current, internal efficiency and recovery still require qualification.

## Fabrication review

Start with [open decisions](design/fab/OPEN_DECISIONS.md) and the [team's decision log](notes/decisions.md). **The architecture changed to v4 on 2026-11-08** (local mirror, no D2; leads in a slot along the centre DC; A30 + B60 retained; R1_TRAP on the no-Al stack). The trap-die GDS is v4 and passes `check_chip.py`. Since 2026-11-09 the traveler, run sheet, mask list, test plan and test dies are v4 as well, with the electrode step written as two branches (E1 and E2) until the team chooses. Figures: [stack](design/fab/figures/stack_v4.svg), [process flow](design/fab/figures/process_flow_v4.svg).

## Goal

Synthesise design files and fab procedures for a basic **five-wire surface trap**, so that the team's fabrication is as streamlined as possible. Fixed parameters:

| Item | Choice |
|---|---|
| Ion | ¹³⁸Ba⁺, detected at 493 nm |
| Ion height | 50 µm |
| Substrate | High-resistivity Si (sapphire and fused-silica deltas covered) |
| Metals | Local Al mirror under the SNSPD and its leads (v4); Au electrodes, E1 0.35 µm lift-off or E2 6 µm plated (open) |
| Detector | NbN SNSPD under the readout zone, under SiO₂ only (no ITO since v3) |
| Electrodes | Segmented outer DC electrodes |
| Zones | Loading zone, plus a readout zone directly above the SNSPD |
| Die | **10 × 10 mm, trap centred, pads at the die edges** (team decision, 2026-11-07; was 10 × 2.5 mm in v2) |

Every design choice is referenced to the literature.

Ground rules agreed with the team:
- Claude-written docs live in `design/` and are labelled Claude-authored.
- Claude does not touch `proposal/*.tex`. Claude logs the team's decisions in `notes/decisions.md` (team change, 2026-11-08).

## Current deliverables (v4)

| What | File |
|---|---|
| Trap dies (10 × 10 mm) | `design/gds/trap_die_v4_A30.gds` (30 × 30 µm SNSPD, local mirror, slot leads), `trap_die_v4_B60.gds` (60 × 30 µm), `trap_die_v4_NODET.gds` (plain trap, no SNSPD, no Al). v3 (incl. B60) in `gds/archive_v3_baseline/` |
| Test die (10 × 2.5 mm) | `design/gds/test_die_v4.gds`: T1 Au comb, T2v Au / SiO₂ / Al capacitor, T3 NbN bar, T4/T4b spare SNSPDs on local Al mirrors, T6 Au loop, T8 EBL dose array, T9 geometry array, T10 Al mirror strip (four-point), T11 Au-to-Al via chain, T12 twin Au leads over Al. `test_die_v4_TRAP.gds`: T1 and T6 only. Both pass `check_test_die.py`. v3 test dies in `gds/archive_v3_baseline/` |
| R&D runs | `design/gds/run_R1_TRAP.gds` (6 NODET + 2 trap-only test dies; **run 1a, chosen first**; sheet `design/fab/RUNSHEET_R1_TRAP.md`) and `run_R1_FULL.gds` (2 A30 + 2 B60 + 2 NODET + 2 TEST): 8 dies, 20.2 × 33.1 mm block at the centre of a 100 mm wafer (`make_run.py`) |
| Full wafer (reference) | `design/gds/wafer_v4.gds` + `wafer_v4_map.csv/png`: 56 dies, columns of [A30, B60, A30, TEST] |
| Pad lists | `design/gds/*_pads.csv` |
| Layer map | `design/gds/layer_map.md` |
| Simulation layouts | `design/gds/*_sim.json` (read by gds2itvg) |
| Generators / checks | `make_chip.py`, `make_test_die.py`, `make_run.py`, `make_wafer.py`; `check_chip.py` (DRC + connectivity + fab consistency + no ITO + no pads in the beam-exit corners; **all pass** on v4 A30, B60 and NODET); `check_test_die.py` (written from the specification, independent of the generator); `measure_dies.py` → `measured_v4.md` (areas, meander squares, file hashes) |
| Simulations | `design/sim/01…20_*.py` (outputs in `design/sim/out/`). New 2026-11-09: `15b` collection on v4, `17` height trade-off, `18` E1 vs E2, `19` lead termination, `20` transport timing |
| Literature | `design/research/reports/Trap integrated SNSPD design.md`, `design/references_design.bib`; pointers from 2026-11-09 in `design/research/research_notes/Loose ends 2026-11/` |
| Fab | `design/fab/TRAVELER.md` (v4 index), `process/01…04`, `RUNSHEET_R1_TRAP.md`, `mask_list.md`, `process_checks.md`, `test_plan.md`, `figures/stack_v4.svg`, `figures/process_flow_v4.svg`; `check_links.py` checks the links between them |

## Key design numbers

| Item | Value |
|---|---|
| Geometry | Centre DC 40 µm (A30: 25 µm lead slot), RF rails 84 µm, gaps 5 µm; Au (E1 0.35 / E2 6 µm, open) on ~1.3 µm SiO₂ over HR Si; local Al mirror, no ground plane (v4) |
| RF drive | 53 V at 28 MHz → radial 3.0 MHz, q 0.30, depth ≈ 52 meV |
| Outer segments | 15 + 15 at 120 µm pitch (100 µm before step 28) |
| Zone spacing | Loading ↔ readout 480 µm (team decision 2026-11-08, laser setup; was 600 µm) |
| Readout window | 30 µm opening inside the centre DC; floor = the 160 nm SiO₂ cap, over the NbN and the grounded local mirror (v4) |
| Window effect on height | v4: −1.19 µm (E2) / ≤ −0.37 µm (E1), grounded floor (3-D FD). v3: −1.38 µm over bare SiO₂. |
| NbN absorption | v4: 0.66 with a 160 nm cap, 0.44 with the drawn 80 nm (sim 09c, step 26); v3.1: 0.54 (f 0.65, EMT) |
| Geometric collection | v4 (sim 15b, step 32), isotropic Ba⁺ emission: 2.22 % (A30, E2), 4.16 % (B60, E2); absorbed in NbN 1.47 % / 2.71 % of all emitted photons with the 160 nm cap. Todaro: 2.0 % geometric. |
| Beam clipping (10 × 10 mm die) | ≈ 1.7e-2 at 493 nm, 3.2e-2 at 650 nm (was 1.1e-5 / 1.1e-4 on the 2.5 mm die) |
| RF pickup bound (2-D) | v4 (sim 10c, steps 37–38): nanowire 0.96 µA (E2) / 1.92 µA (E1), plus at most 0.73–0.97 µA through the mirror path; each slot lead collects 44.5 µA (E2) / 28.6 µA (E1) of common-mode current. v3 was 1.4 µA with no ITO |
| Simulated on the v3 fab GDS | Null height 50.08 µm (loading), 50.09 µm (readout); with the window recess ≈ 48.7 µm (A30) or ≈ 47.6 µm (B60). Loading zone and NODET: axial 0.8 MHz, radial 2.89 / 2.97 MHz, 10° tilt, max \|V\| 9.05 V. **A30/B60 readout: the open window splits the radial modes, so the 10° tilt needs 13.2 / 15.2 V (over ±10 V); no tilt needs 6.6 / 3.4 V.** Transport max 7.33 V; ≤ 1.6 V per 10 µm step (A30), up to 4.5 V near the B60 window. |
| Simulated on the v4 fab GDS | Null 49.97 / 49.98 µm; readout incl. recess ≈ 48.8 µm (E2). 10° tilt (480 µm zones, steps 28–29): loading 7.5 V, **readout 6.3 V** (A30) / 2.2 V (B60) (fits ±10 V; v3 needed 13.2 V). NODET 7.9 V. Transport with the centre DC held at 0 V: max 6.6 V, ≤ 1.71 V per 10 µm step (7.6–8.0 V steps if the centre DC is used, because of the slot end and window). |

## Done ✅ (chronological)

1. **Read the inputs:** notes PDF, the electrode repo (gds2itvg) and the bib. Questions to the team settled authorship, the Si substrate and e-beam access.
2. **Literature:** 5 parallel research threads, combined into one report with 28 design implications. Main finding: Todaro's pocket sits inside the centre DC, and the height drop comes from RF-rail termination plus the recess.
3. **Sims 01–03:** analytic five-wire at h = 50 µm; gds2itvg baseline matches it; 100 µm segment pitch.
4. **Sims 04/04b/05:** the window study (planar, 2-D and 3-D finite differences). Missing metal lowers the ion only through the RF boundary condition. Decisions: the window stays inside the centre DC, and the RF rails run well past the readout zone.
5. **Sim 06:** detector size → A30 primary, B60 variant.
6. **Sims 09/09b/10:** optics and RF pickup → the two-ITO window stack; every ITO grounded.
7. **Sim 11:** beam clearance. First a bowtie, then a square die with the zones in a corner, then (now) the narrow die.
8. **GDS v1:** square die, then checker fixes, then the traveler review's items A1–A7.
9. **GDS v2 after your feedback** that the corner layout was lopsided:
   - narrow 10 × 2.5 mm die, trap centred;
   - pads in four rows on the long edges;
   - leads ≤ 4.5 mm;
   - test structures on their own die;
   - wafer layout;
   - A1–A7 built in.
10. **Final simulation of the v2 GDS** (DESIGN_LOG step 13): both dies match v1 to within 0.07 µm, and the zones sit on the flat part of h(y), ≥ 1.7 mm from the rail ends.
11. **Fab docs** written: traveler steps 0–19, witness wafers, thermal budget, mask list, checks, test plan. Reconciled to v2: v2 coordinates, the bond map from `trap_die_v2_A30_pads.csv`, per-die mask areas, wafer and quarter-wafer jobs, and TRAVELER section A marked resolved.
12. **Plain trap die** `trap_die_v2_NODET` (`make_chip.py --nodet`, DESIGN_LOG step 14): no SNSPD, no window. Passes the checks; simulation identical to A30 but with no recess drop. Traveler notes say which steps a trap-only wafer skips.
13. **Simplifications plan** (`design/SIMPLIFICATIONS.md`): wafer and run-size options plus 14 simplifications, each with sim and bench tests. Nothing run yet.
14. **R&D workflow for MIT.nano** (DESIGN_LOG step 15): small run layouts via `make_run.py`; T8 dose array on the test die; T3 lead-to-pad gap fixed; [facility questions](design/fab/QUALIFICATION.md#facility-confirmations) run plan and facility questions; mask list reworked for runs.
15. **First run set to trap-only R1_TRAP** (DESIGN_LOG step 16): trap-only test die (`--trap-only`); R1_TRAP uses only 5 MLA layers and no EBL; streamlined `fab/RUNSHEET_R1_TRAP.md`.
16. **v3: no ITO** (DESIGN_LOG step 17): L24/L30/L31 removed from every die; window floor is bare SiO₂; L45 window patch now essential. Reran 04b (bare-SiO₂ floor: −1.38 µm A30, −2.50 µm B60), 09b (absorption 0.40), 10 (pickup 1.42 µA). T5/T7 removed from the test die.
17. **v3: 10 × 10 mm die, pads at the edges** (DESIGN_LOG step 18): pad rows on the top/bottom edges at |x| ≤ 3.5 mm, ground/M1 spots on the side edges, nothing in the beam-exit corners. Runs and wafer stack mixed die heights; run columns share row heights so the saw cuts run straight. v2 archived in `gds/archive_v2_narrow/`.
18. **A30 vs B60 and DC height tuning** (DESIGN_LOG step 19, sims 12 and 13): drop −1.38 vs −2.50 µm; the open window splits the readout radial modes, so the 10° tilt needs 13.2 / 15.2 V. DC can push the ion back up (6.8 V A30, 2.8 V B60 without tilt) but cannot move the RF null: 200 / 350 nm excess micromotion.
19. **Team-neutral docs:** names and personal paths removed; `run.sh` finds the env on any machine; electrode setup steps in `design/CLAUDE.md`.
20. **Staircase check** (DESIGN_LOG step 20, sim 14): the staircase fingers + leads make each outer DC electrode 6–10 % stronger at the ion than a plain 200 µm rectangle (∂φ/∂z up to +13 %), and neighbours differ by up to 2 %. Final-chip sims already use the real GDS; an idealized model would be off by ≤ 1.3 V per electrode at the zones.
21. **Bond pads** (DESIGN_LOG step 21, research report `design/research/reports/Bond pad sizing for ion traps.md`): pad size is fine; fill keep-out around pads 10 → 30 µm, pad rows moved to y = ±4720, SNSPD openings 120 × 90 → 150 × 120 µm. Traveler: wedge-bond SNSPD, RF on 2–4 wires, W7 bond-and-leak short loop.

22. **On-chip ground vias** (DESIGN_LOG step 22, after comparing the team's FabuBlox flow with Hampel 2023): eight 150 µm L40 vias tie the Au ground fill to the Al mirror on chip, as Hampel grounds its mirror. L50 unchanged, so no re-simulation. Traveler: Ar pre-clean before the seed; new test a13 (GND ↔ M1 < 10 Ω); M1 bonds become a backup.

23. **SNSPD geometry v3.1** (DESIGN_LOG step 24, report `design/research/reports/SNSPD geometry audit.md`): 130/200 nm meander, lines past the window (3 / 4.5 µm axially, 1 µm radially per the sim 10 RF scan), rounded end blocks and tapered tabs outside the light footprint; shared `gds/snspd_geom.py`; new NbN checks; T9 geometry array on the test die; sims 06, 10, 15 updated. All dies pass `check_chip.py`.

24. **Decision log handed to Claude** (team change, 2026-11-08): rule updated in root and `design/` CLAUDE/AGENTS files; `notes/decisions.md` created, with the earlier team decisions backfilled.

25. **v4: local-mirror architecture** (DESIGN_LOG step 25, team decisions): `make_chip.py` v4 (local Al mirror + ground via, Au leads in a centre-DC slot as Hampel 2023, no D2/L45, NODET without Al); `check_chip.py` rewritten, all pass on A30 and NODET; runs and wafer regenerated; v3 archived. Sims 04b (grounded window floor), 12 and 13 rerun: readout tilt now fits (6.1 V); transport needs the centre DC held at 0 V. Fab pages for the v3 process carry a banner until the E1/E2 choice.

26. **360 µm pad-layout validation** (DESIGN_LOG step 29): measured all 84 PGA84L finger centres and mapped all 42 A30 pads without crossings; worst top/bottom angle 20.03°, side angles ≤ 8.58°. A30/B60/NODET pass `check_chip.py` (5.00 µm spacing, no floating Au or corner pads). All seven sim 12 runs pass: regular zone maxima ≤ 7.93 V; centre-zero transport 1.708 V per 10 µm; planar null heights unchanged, 49.96–49.98 µm at the confirmed two-decimal precision. A 0.117 V diagnostic readout-set change triggered sim 13; needed height-tuning voltages changed by ≤ 0.0041 V. Old outputs are archived. Layer map and v4 packaging map updated. **Pitch adoption, future perpendicular beam access, carrier choice and spacer remain open; `notes/decisions.md` unchanged.**

## In progress ⏳

- Fabrication notes reorganized into linked modules. Qualification and detector reconciliation remain open; see [checklist](design/fab/OPEN_DECISIONS.md).

## Open items / decisions for the team

- [ ] Ground vias (step 22): add the via contact check to W3 (with / without Ar pre-clean, sidewall cross-section); confirm the AJA substrate RF etch.
- [ ] **v3.1 SNSPD geometry** (step 24) is Claude's design call, not a team decision (team, 2026-11-08), so it stays out of `notes/decisions.md` until the team adopts it. Open from it: centre-DC filter capacitor, Al RF potential under the leads, Isw at 5 K (maybe 8–9 µA), measured NbN thickness, RCWA check of absorption, Suleimen 2026 full text, isotropy derivation check.
- [ ] **v4 follow-ups** (step 25): choose E1 vs E2; rewrite traveler / R1_TRAP sheet / mask list / stack for v4; rework the test dies (no D2, no die-wide Al); set the cap to 160 nm in the rewritten traveler (09c, step 26); RF bypass / symmetric termination for the slot leads (sim 10c: 44.5 µA common-mode per lead on E2); mirror ground path: via moved; Al 450 nm on 2026-11-08, then 100 nm inlaid on 2026-11-09 (steps 37–38; at most +0.97 µA), measured on T10 instead of a probe opening; order Si with ρ > 20 kΩ·cm; measure resonator Q with a die mounted.
- [ ] Bond pads (step 21): run W7 bond-and-leak before R1; get MIT.nano bonder and tool part numbers; draw the bond diagram against the carrier; field-solve DC-to-RF coupling.
- [ ] **Pad pitch / package (step 29):** adopt or revise the validated 360 µm layout after reviewing future perpendicular beam access near the zones; choose 84-pin vs 100-pin/lab carrier and complete its electrical pin map. Spacer proposal: ≥ approximately 0.6 mm thick, die-sized or larger, Si suggested; not adopted.
- [ ] Not yet team decisions (Claude's layout calls or open): readout radial tilt (v4 A30 fits 10° at 6.3 V; team to confirm), 0.8 MHz axial with ±10 V DACs.
- [ ] Reasons the team still owes `notes/decisions.md` (asked 2026-11-08): A30/B60 detector variants; and "not recorded" on Ba⁺/project scope, NODET die, R1_TRAP first. (Si substrate, no ITO and the 10 × 10 mm die were answered 2026-11-08; the 50 µm ion height on 2026-11-09.)
- [ ] Before tape-out, run the witness wafers in [qualification](design/fab/QUALIFICATION.md). Also confirm:
  - the Plating-U04 bath;
  - the Dane NbN recipe (Berggren group);
- [ ] Before R1_TRAP (v4): no D2 stress or gap-etch loops any more; W5 plating only if E2; W7 bond-and-leak on the v4 stack.
- [ ] Ask MIT.nano staff the facility questions in [facility questions](design/fab/QUALIFICATION.md#facility-confirmations): which tools accept Au, NbN sputter access, gold plating tank.
- [ ] Check whether T4/T4b on the test die can be wire-bonded for the cold SNSPD test (marked [verify] in `test_plan.md` (b)).
- [ ] Not modelled yet:
  - RCWA/FDTD of the meander (TMM reads about 10 % low);
  - 3-D lead pickup;
  - adiabatic transport timing.

## Decisions reversed along the way

| Was | Replaced by | Why |
|---|---|---|
| Bowtie chip | Square die with zones in a corner | Team: simpler fab |
| Square die with corner zones | Narrow 10 × 2.5 mm die | Team: lopsided layout, long leads |
| D2 etched down to a buried ITO | ITO on D2 + buried grounded ITO | The ion sees no dielectric, and absorption is recovered |
| ITO on D2 + buried grounded ITO | No ITO, bare SiO₂ window floor | Team decision 2026-11-07 |
| Narrow 10 × 2.5 mm die | 10 × 10 mm die, trap centred, pads at the edges | Team decision 2026-11-07 |
| Die-wide Al ground plane under 10 µm D2 (v3) | Local Al mirror, no D2, leads in a centre-DC slot (v4) | Team decision 2026-11-08: better optics with vacuum above the cap; NIST traps without a plane on HR Si |
| A30 + B60 | A30 only, then A30 + B60 again | Team decisions 2026-11-08 (B60 kept after the v4 numbers) |
