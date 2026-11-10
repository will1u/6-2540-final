# design/: five-wire ¹³⁸Ba⁺ trap with an integrated NbN SNSPD

> **Claude-authored** working folder, set up at the team's request on 2026-11-02. It holds the design files, simulations and fab procedures. Design decisions here are Claude's proposals; record the ones you adopt in your own `notes/decisions.md`.

For fabrication review, start with [fab overview](fab/README.md), [variants](fab/VARIANTS.md) and [open decisions](fab/OPEN_DECISIONS.md).

## Where things are

| Path | What it is |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | Identical context files for AI agents working in this folder: rules, environment, conventions, current state. |
| `DESIGN_LOG.md` | Chronological log of every design step: script, inputs, numbers, decision, citation. **Start here.** |
| `research/reports/Trap integrated SNSPD design.md` | Literature report with section/figure pointers and a "Read these sections yourself" list. |
| `research/research_notes/…` | Raw research notes behind the report. |
| `sim/` | Simulation scripts, numbered in the order they were run. Outputs go to `sim/out/<script>/`. |
| `SIMPLIFICATIONS.md` | Wafer layout and run-size options; possible design simplifications and the tests that would check each one (a plan; nothing run). |
| `gds/make_chip.py` | Generates the v4 10 × 10 mm trap dies (local mirror, no D2; DESIGN_LOG step 25): `trap_die_v4_A30.gds`; `--nodet` builds the plain trap die without an SNSPD or Al (`trap_die_v4_NODET.gds`, the R1_TRAP die); `--uniform` builds `trap_die_v4_UNIFORM.gds`, a simulation-only reference (never for fab). It also writes the simulation layouts (`*_sim.json` for E2 6 µm Au, `*_E1_sim.json` for E1 0.35 µm Au, and `*_simfloor.gds`, sim only) and the pad list (`*_pads.csv`). The v3 baseline dies (incl. B60) are in `gds/archive_v3_baseline/`. |
| `gds/make_test_die.py` | 10 × 2.5 mm test-structure die for the v4 stack (`test_die_v4.gds`): T1, T2v, T3, T4/T4b, T6, T8 (EBL dose array), T9 (geometry array), T10 (Al mirror strip), T11 (Au-to-Al via chain), T12 (twin Au leads over Al). `--trap-only` writes `test_die_v4_TRAP.gds` (T1 and T6, no Al) for trap-only runs. The v3 test dies are in `gds/archive_v3_baseline/`. |
| `gds/check_test_die.py` | Independent checks on the test dies (spacing, connectivity, openings, mirrors), written from the specification and not from the generator. |
| `gds/measure_dies.py` | Read-only measurement of the released GDS files: area per layer, meander squares and inductance, file hashes. Writes `gds/measured_v4.md`, which the fab pages cite. |
| `gds/make_run.py` | Small R&D run layouts for MIT.nano: `run_R1_TRAP.gds`, `run_R1_FULL.gds` (8 dies at the wafer centre, map CSV/PNG). |
| `gds/make_wafer.py` | Full-wafer reference layout (`wafer_v4.gds`, 56 dies, map CSV/PNG). |
| `gds/archive_v1_square/`, `gds/archive_v2_narrow/` | Superseded layouts: v1 square die (DESIGN_LOG step 8), v2 narrow die with the two-ITO window (steps 12–16). |
| `gds/check_chip.py` | DRC, connectivity and short checks on a generated GDS, plus preview PNGs. |
| `gds/layer_map.md` | GDS layers, process order, coordinates. |
| [fab/](fab/README.md) | Linked Obsidian notes: variants, open decisions, qualification, process stages, first-run sheet, exposures and tests. [Traveler](fab/TRAVELER.md) is the full-process index. |

## Running

Everything uses the `electrode` conda env, which has gds2itvg, gdstk, shapely and numba. Set it up once first (steps in `CLAUDE.md`, "Setting up the electrode repo"). Then, in Git Bash (or any bash), run from `design/sim`:

```bash
./run.sh 01_analytic_fivewire.py
```

```bash
./run.sh ../gds/make_chip.py && ./run.sh ../gds/check_chip.py trap_die_v4_A30
```

```bash
./run.sh 12_final_chip_check.py ../gds/trap_die_v4_A30_sim.json
```

`run.sh` finds the env (`$ELECTRODE_ENV` or `<conda base>/envs/electrode`) and, on Windows, puts its DLL folders on PATH. Without that, numpy/matplotlib crash with `0xc06d007f` when the env isn't activated.

## Scripts

| Script | Question it answers |
|---|---|
| `trapcalc.py` | Shared physics: pseudopotential, secular frequencies, DC solve, detector solid angle. Lifted from `electrode/workflow.ipynb`. |
| `trapgeom.py` | Parametric five-wire geometry used by the sims in steps 2–6. |
| `01_analytic_fivewire.py` | Collection vs heating vs height; geometry family at h = 50 µm (House/Wesenberg gapless model). |
| `02_baseline_gds2itvg.py` | Baseline in gds2itvg vs the analytic model. |
| `03_segment_pitch.py` | Outer-segment pitch vs DC voltages and conditioning. |
| `04_window_validation.py` | 2-D finite-difference cross-section of window variants; RF-rail termination (Todaro mechanism). |
| `04b_window_3d_fd.py` | 3-D finite-difference check of the finite readout window (height shift, axial RF field). Window-floor cases: `etched` (SiO₂ removed to the ground plane), `oxide` (bare SiO₂ floor, the v3 design), `ito6` (ITO on the SiO₂, v2), `mirror_t6` / `mirror_t1` (v4: grounded floor over the local mirror at the bottom of a 6 / 1 µm Au pocket, Si below, no ground plane). |
| `05_window_variants.py` | Window variants in the planar gds2itvg model (RF null, barrier, DC). |
| `06_detector_size.py` | Detector/window size vs collection, nanowire length, reset time. |
| `09_optical_stack_tmm.py` | NbN absorption at 493 nm vs spacer/cap/ITO thickness (transfer matrix). |
| `10_rf_pickup_2d.py` | RF field at the nanowire with/without the Al mirror and ITO; RF capacitance. |
| `11_beam_clearance.py` | Laser clipping on the chip; corner placement of the zones. |
| `12_final_chip_check.py` | Simulates the **fabrication GDS itself**: RF null along the axis, DC sets at both zones, transport waveforms. |
| `13_dc_height_tuning.py` | Can DC voltages push the ion back up over the readout window? DC needed and excess micromotion vs upward shift, at 0° and 10° radial tilt. |
| `14_staircase_check.py` | Staircase fingers + leads vs plain equal-depth segments (`trap_die_v3_UNIFORM`, read from `gds/archive_v3_baseline/`) and the electrode repo's five-wire example: unit potentials, symmetry, zone voltages, transport. |
| `09c_localmirror_optics.py`, `10b_rf_pickup_v4.py` | v4 versions of 09 and 10: NbN absorption with vacuum above the cap (sets the 160 nm cap); RF pickup with the slot leads and the local mirror. |
| `10c_mirror_thickness.py` | 10b's solver over Al mirror thicknesses 50–450 nm and an inlaid mirror: strip current, swing, extra nanowire current, strip dissipation, lead common mode, micromotion estimate (step 37). |
| `10d_mirror_step.py` | The same solver on the full cross-section with a raised mirror (0, 100, 450 nm) and a sideways-misaligned mirror (0, 2, 5 µm): shift of the RF null, change in q, micromotion if not re-tuned (step 39). Options `--one`, `--au E1\|E2`. |
| `15_snspd_geometry.py` | SNSPD geometry budget on the v3 stack: collection, refraction footprint, absorption vs fill factor, turn crowding, kinetic inductance. |
| `15b_collection_v4.py` | Collection and NbN absorption on the v4 stack, for A30/B60 and both electrode options. |
| `16_pad_pitch_check.py` | Compares the 360 µm pad layout with the 180 µm one: wire fan-out to the PGA84L fingers, sim 12 and 13 differences. |
| `17_height_tradeoff.py` | Is 50 µm the right ion height? Collection, trap depth, heating and beam clipping from 30 to 70 µm. |
| `18_e1_vs_e2.py` | Do the two electrode options differ functionally? Au resistance, RF heating, SiO₂ gap screening, next to the already-simulated differences. |
| `19_lead_termination.py` | RF current through the nanowire for several terminations of the SNSPD leads, and what each does to the detector pulse. |
| `20_transport_timing.py` | How fast can the ion be moved? Residual motion for smooth ramps and for a DAC staircase through a filter. |
