# Claude progress: five-wire Ba⁺ trap with an integrated NbN SNSPD

> **Claude-authored running status.** Last documentation update: 2026-11-08 (linked fab notes and reconciliation checklist).
> - Full detail with numbers and citations for every step: [design log](design/DESIGN_LOG.md) (numbered design steps and documentation updates).
> - New team member? Set up the `electrode` repo first: `design/CLAUDE.md`, "Setting up the electrode repo".
> - Folder index and how to run: `design/README.md`.

## Fabrication review

Start with [fab overview](design/fab/README.md), [variants](design/fab/VARIANTS.md) and [open decisions](design/fab/OPEN_DECISIONS.md). R1_TRAP remains the selected first run. Current generators specify v3.1 (130/200 nm, rounded turns, enlarged footprint, T9); older fab estimates need reconciliation before R1_FULL. No new layout checks, simulations or witness measurements were run during this cleanup.

## Goal

Synthesise design files and fab procedures for a basic **five-wire surface trap**, so that the team's fabrication is as streamlined as possible. Fixed parameters:

| Item | Choice |
|---|---|
| Ion | ¹³⁸Ba⁺, detected at 493 nm |
| Ion height | 50 µm |
| Substrate | High-resistivity Si (sapphire and fused-silica deltas covered) |
| Metals | Al ground plane, plated Au electrodes |
| Detector | NbN SNSPD under the readout zone, under SiO₂ only (no ITO since v3) |
| Electrodes | Segmented outer DC electrodes |
| Zones | Loading zone, plus a readout zone directly above the SNSPD |
| Die | **10 × 10 mm, trap centred, pads at the die edges** (team decision, 2026-11-07; was 10 × 2.5 mm in v2) |

Every design choice is referenced to the literature.

Ground rules agreed with the team:
- Claude-written docs live in `design/` and are labelled Claude-authored.
- Claude does not touch `proposal/*.tex` or `notes/decisions.md`.

## Current deliverables (v3)

| What | File |
|---|---|
| Trap dies (10 × 10 mm) | `design/gds/trap_die_v3_A30.gds` (30 × 30 µm SNSPD), `trap_die_v3_B60.gds` (60 × 30 µm), `trap_die_v3_NODET.gds` (plain trap, no SNSPD) |
| Test die (10 × 2.5 mm) | `design/gds/test_die_v3.gds`: T1 Au comb, T2 D2 capacitor, T3 NbN bar, T4/T4b spare SNSPDs, T6 Au loop, T8 EBL dose array (T5/T7 ITO tests removed) |
| R&D runs | `design/gds/run_R1_TRAP.gds` (6 NODET + 2 trap-only test dies; **run 1a, chosen first**; sheet `design/fab/RUNSHEET_R1_TRAP.md`) and `run_R1_FULL.gds` (2 A30 + 2 B60 + 2 NODET + 2 TEST): 8 dies, 20.2 × 33.1 mm block at the centre of a 100 mm wafer (`make_run.py`) |
| Full wafer (reference) | `design/gds/wafer_v3.gds` + `wafer_v3_map.csv/png`: 56 dies, columns of [A30, B60, A30, TEST] |
| Pad lists | `design/gds/*_pads.csv` |
| Layer map | `design/gds/layer_map.md` |
| Simulation layouts | `design/gds/*_sim.json` (read by gds2itvg) |
| Generators / checks | `make_chip.py`, `make_test_die.py`, `make_run.py`, `make_wafer.py`; `check_chip.py` (DRC + connectivity + fab consistency + no ITO + no pads in the beam-exit corners; **all pass** on A30, B60, NODET) |
| Simulations | `design/sim/01…13_*.py` (outputs in `design/sim/out/`) |
| Literature | `design/research/reports/Trap integrated SNSPD design.md`, `design/references_design.bib` |
| Fab | `design/fab/TRAVELER.md`, `mask_list.md`, `process_checks.md`, `test_plan.md` |

## Key design numbers

| Item | Value |
|---|---|
| Geometry | Centre DC 40 µm, RF rails 84 µm, gaps 5 µm, 6 µm Au on 10 µm SiO₂ over Al |
| RF drive | 53 V at 28 MHz → radial 3.0 MHz, q 0.30, depth ≈ 52 meV |
| Outer segments | 15 + 15 at 100 µm pitch |
| Zone spacing | Loading ↔ readout 600 µm (12 h) |
| Readout window | 30 µm opening inside the centre DC over bare SiO₂ (no ITO, v3); the L45 protect patch keeps the gap etch out of it |
| Window effect on height | −1.38 µm (A30) / −2.50 µm (B60) over bare SiO₂ (3-D FD, upper bound). The ion now sees bare SiO₂ in the window. |
| NbN absorption | ≈ 0.54 at 493 nm for the v3.1 meander (f 0.65; EMT, step 24); 0.40 at f 0.5 (v3) |
| Geometric collection | 2.23 % (A30), 4.20 % (B60) with isotropic Ba⁺ emission (step 24; the old 3.25 % / 5.9 % assumed a σ pattern). × 95 % landing × 0.54 ≈ 1.15 % / 2.2 %. Todaro: 2.0 % geometric. |
| Beam clipping (10 × 10 mm die) | ≈ 1.7e-2 at 493 nm, 3.2e-2 at 650 nm (was 1.1e-5 / 1.1e-4 on the 2.5 mm die) |
| RF pickup bound (2-D) | 1.42 µA with no ITO (was ≈ 0 with the grounded buried ITO); ~7–9 % of the estimated NbN switching current |
| Simulated on the v3 fab GDS | Null height 50.08 µm (loading), 50.09 µm (readout); with the window recess ≈ 48.7 µm (A30) or ≈ 47.6 µm (B60). Loading zone and NODET: axial 0.8 MHz, radial 2.89 / 2.97 MHz, 10° tilt, max \|V\| 9.05 V. **A30/B60 readout: the open window splits the radial modes, so the 10° tilt needs 13.2 / 15.2 V (over ±10 V); no tilt needs 6.6 / 3.4 V.** Transport max 7.33 V; ≤ 1.6 V per 10 µm step (A30), up to 4.5 V near the B60 window. |

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

## In progress ⏳

- Fabrication notes reorganized into linked modules. Qualification and detector reconciliation remain open; see [checklist](design/fab/OPEN_DECISIONS.md).

## Open items / decisions for the team

- [ ] Ground vias (step 22): add the via contact check to W3 (with / without Ar pre-clean, sidewall cross-section); confirm the AJA substrate RF etch.
- [ ] Log in `notes/decisions.md` (team's call): **on-chip fill-to-M1 ground vias** (2026-11-08).
- [ ] Log in `notes/decisions.md` (team's call): **v3.1 SNSPD geometry** (step 24). Open from it: centre-DC filter capacitor, Al RF potential under the leads, Isw at 5 K (maybe 8–9 µA), measured NbN thickness, RCWA check of absorption, Suleimen 2026 full text, isotropy derivation check.
- [ ] Local-mirror variant (step 23, [local-mirror proposal](design/fab/variants/LOCAL_MIRROR.md)): written up only, no GDS. To pursue it: choose the lead routing (slot in the centre DC vs a thicker local SiO₂), add `make_chip.py --localmirror`, rerun 09b / 04b / 12 / 10 with no D2; specify Si with ρ > 20 kΩ·cm (NIST practice, no ground plane needed); prefer option E2 (6 µm plated, as Todaro did). Log the choice in `notes/decisions.md` if the team picks it.
- [ ] Bond pads (step 21): run W7 bond-and-leak before R1; get MIT.nano bonder and tool part numbers; draw the bond diagram against the carrier; field-solve DC-to-RF coupling.
- [ ] Log in `notes/decisions.md` (team's call):
  - **no ITO** (2026-11-07): absorption 0.53 → 0.40, RF pickup bound ≈ 0 → 1.4 µA, bare SiO₂ under the ion (unscreened charging and click kicks);
  - **10 × 10 mm die with edge pads** (2026-11-07): ~1.7e-2 of the 493 nm beam clips the surface (vs 1e-5 on the 2.5 mm die);
  - readout radial tilt: 10° no longer fits ±10 V on A30/B60 (13.2 / 15.2 V); pick a smaller tilt, wider DACs, or no tilt;
  - A30/B60 split;
  - 600 µm zone spacing;
  - 0.8 MHz axial frequency with ±10 V DACs.
- [ ] Before tape-out, run the witness wafers in [qualification](design/fab/QUALIFICATION.md). Also confirm:
  - the Plating-U04 bath;
  - the Dane NbN recipe (Berggren group);
- [ ] Log in `notes/decisions.md`: first run is trap-only R1_TRAP (team decision, 2026-11-02).
- [ ] Before R1_TRAP: D2 stress loop, gap-etch rate loop, W5 plating (RUNSHEET_R1_TRAP section 2).
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
