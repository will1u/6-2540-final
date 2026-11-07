# Claude progress: five-wire Ba⁺ trap with an integrated NbN SNSPD

> **Claude-authored running status.** Last update: 2026-11-02 (v2 narrow die simulated; fab docs reconciled).
> - Full detail with numbers and citations for every step: `design/DESIGN_LOG.md` (steps 0–16).
> - Folder index and how to run: `design/README.md`.

## Goal

Synthesise design files and fab procedures for a basic **five-wire surface trap**, so that William's fabrication is as streamlined as possible. Fixed parameters:

| Item | Choice |
|---|---|
| Ion | ¹³⁸Ba⁺, detected at 493 nm |
| Ion height | 50 µm |
| Substrate | High-resistivity Si (sapphire and fused-silica deltas covered) |
| Metals | Al ground plane, plated Au electrodes |
| Detector | NbN SNSPD under the readout zone, shielded by SiO₂ + ITO |
| Electrodes | Segmented outer DC electrodes |
| Zones | Loading zone, plus a readout zone directly above the SNSPD |
| Die | **Plain diced 10 × 2.5 mm** (William, 2026-11-02; four per original 1 cm²) |

Every design choice is referenced to the literature.

Ground rules agreed with William:
- Claude-written docs live in `design/` and are labelled Claude-authored.
- Claude does not touch `proposal/*.tex` or `notes/decisions.md`.

## Current deliverables (v2)

| What | File |
|---|---|
| Trap dies | `design/gds/trap_die_v2_A30.gds` (30 × 30 µm SNSPD), `trap_die_v2_B60.gds` (60 × 30 µm), `trap_die_v2_NODET.gds` (plain trap, no SNSPD) |
| Test die | `design/gds/test_die_v2.gds`: T1 Au comb, T2 D2 capacitor, T3 NbN bar, T4/T4b spare SNSPDs, T5 ITO bar, T6 Au loop, T7 ITO→Al via chain, T8 EBL dose array |
| R&D runs | `design/gds/run_R1_TRAP.gds` (6 NODET + 2 trap-only test dies; **run 1a, chosen first**; sheet `design/fab/RUNSHEET_R1_TRAP.md`) and `run_R1_FULL.gds` (2 A30 + 2 B60 + 2 NODET + 2 TEST): 8 dies at the centre of a 100 mm wafer (`make_run.py`) |
| Full wafer (reference) | `design/gds/wafer_v2.gds` + `wafer_v2_map.csv/png`: 184 dies in tiles of [A30, B60, A30, TEST] |
| Pad lists | `design/gds/*_pads.csv` |
| Layer map | `design/gds/layer_map.md` |
| Simulation layouts | `design/gds/*_sim.json` (read by gds2itvg) |
| Generators / checks | `make_chip.py`, `make_test_die.py`, `make_wafer.py`; `check_chip.py` (DRC + connectivity + fab consistency; **all pass** on A30 and B60) |
| Simulations | `design/sim/01…12_*.py` (outputs in `design/sim/out/`) |
| Literature | `design/research/reports/Trap integrated SNSPD design.md`, `design/references_design.bib` |
| Fab | `design/fab/TRAVELER.md`, `mask_list.md`, `process_checks.md`, `test_plan.md` |

## Key design numbers

| Item | Value |
|---|---|
| Geometry | Centre DC 40 µm, RF rails 84 µm, gaps 5 µm, 6 µm Au on 10 µm SiO₂ over Al |
| RF drive | 53 V at 28 MHz → radial 3.0 MHz, q 0.30, depth ≈ 52 meV |
| Outer segments | 15 + 15 at 100 µm pitch |
| Zone spacing | Loading ↔ readout 600 µm (12 h) |
| Readout window | 30 µm inside the centre DC; buried grounded ITO 60 nm + top ITO 125 nm tied to the centre DC |
| Window effect on height | −1.2 µm (3-D FD). The ion sees no bare dielectric. |
| NbN absorption | ≈ 0.53 at 493 nm (Al mirror, 238 nm spacer, 80 nm cap) |
| Geometric collection | 3.25 % (A30), 5.9 % (B60). Todaro: 2.0 %. |
| Beam clipping (2.5 mm die) | 1.1e-5 at 493 nm, 1.1e-4 at 650 nm |
| Simulated on the v2 fab GDS (A30 = B60) | Null height 50.08 µm (loading), 50.09 µm (readout); with the window recess about 48.9 µm (A30) or 48.1 µm (B60). Axial 0.8 MHz, radial 2.88 / 2.98 MHz, tilt about 10°, max \|V\| 9.05 V. Transport smooth: max 7.33 V, at most 1.59 V per 10 µm step. |

## Done ✅ (chronological)

1. **Read the inputs:** notes PDF, the electrode repo (gds2itvg) and the bib. Questions to William settled authorship, the Si substrate and e-beam access.
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
14. **R&D workflow for MIT.nano** (DESIGN_LOG step 15): small run layouts via `make_run.py`; T8 dose array on the test die; T3 lead-to-pad gap fixed; TRAVELER A.3 run plan and facility questions; mask list reworked for runs.
15. **First run set to trap-only R1_TRAP** (DESIGN_LOG step 16): trap-only test die (`--trap-only`); R1_TRAP uses only 5 MLA layers and no EBL; streamlined `fab/RUNSHEET_R1_TRAP.md`.

## In progress ⏳

- Nothing running. The v2 package is ready for your review.

## Open items / decisions for William

- [ ] Log in `notes/decisions.md` (your call):
  - die 10 × 2.5 mm, or 2.0 mm for about 10× less beam clipping;
  - two-ITO window stack (vs etched window: higher absorption, but exposed oxide);
  - A30/B60 split;
  - 600 µm zone spacing;
  - 0.8 MHz axial frequency with ±10 V DACs.
- [ ] Before tape-out, run the witness wafers in `TRAVELER.md` section E. Also confirm:
  - the Plating-U04 bath;
  - the Dane NbN recipe (Berggren group);
  - whether ITO survives the D2 RIE and the Ar seed mill.
- [ ] Log in `notes/decisions.md`: first run is trap-only R1_TRAP (William, 2026-11-02).
- [ ] Before R1_TRAP: D2 stress loop, gap-etch rate loop, W5 plating (RUNSHEET_R1_TRAP section 2).
- [ ] Ask MIT.nano staff the facility questions in TRAVELER A.3: which tools accept Au, NbN sputter access, gold plating tank, ITO source.
- [ ] Check whether T4/T4b on the test die can be wire-bonded for the cold SNSPD test (marked [verify] in `test_plan.md` (b)).
- [ ] Not modelled yet:
  - RCWA/FDTD of the meander (TMM reads about 10 % low);
  - 3-D lead pickup;
  - adiabatic transport timing.

## Decisions reversed along the way

| Was | Replaced by | Why |
|---|---|---|
| Bowtie chip | Square die with zones in a corner | William: simpler fab |
| Square die with corner zones | Narrow 10 × 2.5 mm die | William: lopsided layout, long leads |
| D2 etched down to a buried ITO | ITO on D2 + buried grounded ITO | The ion sees no dielectric, and absorption is recovered |
