# design/: five-wire ¹³⁸Ba⁺ trap with an integrated NbN SNSPD

> **Claude-authored** working folder, set up at William's request on 2026-11-02. It holds the design files, simulations and fab procedures. Design decisions here are Claude's proposals; record the ones you adopt in your own `notes/decisions.md`.

## Where things are

| Path | What it is |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | Identical context files for AI agents working in this folder: rules, environment, conventions, current state. |
| `DESIGN_LOG.md` | Chronological log of every design step: script, inputs, numbers, decision, citation. **Start here.** |
| `research/reports/Trap integrated SNSPD design.md` | Literature report with section/figure pointers and a "Read these sections yourself" list. |
| `research/research_notes/…` | Raw research notes behind the report. |
| `sim/` | Simulation scripts, numbered in the order they were run. Outputs go to `sim/out/<script>/`. |
| `SIMPLIFICATIONS.md` | Wafer layout and run-size options; possible design simplifications and the tests that would check each one (a plan; nothing run). |
| `gds/make_chip.py` | Generates the 10 × 2.5 mm trap dies: `trap_die_v2_A30.gds` and `trap_die_v2_B60.gds` (`--det60`). `--nodet` builds a plain trap die without an SNSPD (`trap_die_v2_NODET.gds`). It also writes the simulation layout (`*_sim.json`) and the pad list (`*_pads.csv`). |
| `gds/make_test_die.py` | Test-structure die (`test_die_v2.gds`), T1–T8. T8 is the EBL dose array. `--trap-only` writes `test_die_v2_TRAP.gds` (T1, T2, T6) for trap-only runs. |
| `gds/make_run.py` | Small R&D run layouts for MIT.nano: `run_R1_TRAP.gds`, `run_R1_FULL.gds` (8 dies at the wafer centre, map CSV/PNG). |
| `gds/make_wafer.py` | Full-wafer reference layout (`wafer_v2.gds`, 184 dies, map CSV/PNG). |
| `gds/archive_v1_square/` | The superseded square-die version (DESIGN_LOG step 8). |
| `gds/check_chip.py` | DRC, connectivity and short checks on a generated GDS, plus preview PNGs. |
| `gds/layer_map.md` | GDS layers, process order, coordinates. |
| `fab/` | `TRAVELER.md` (full process), `RUNSHEET_R1_TRAP.md` (streamlined sheet for the first, trap-only run), `mask_list.md`, `process_checks.md`, `test_plan.md`. |

## Running

Everything uses the `electrode` conda env, which has gds2itvg, gdstk, shapely and numba. In Git Bash, run from `design/sim`:

```bash
./run.sh 01_analytic_fivewire.py
```

```bash
./run.sh ../gds/make_chip.py && ./run.sh ../gds/check_chip.py trap_die_v2_A30
```

```bash
./run.sh 12_final_chip_check.py ../gds/trap_die_v2_A30_sim.json
```

`run.sh` puts the env's DLL folders on PATH. Without it, numpy/matplotlib crash with `0xc06d007f` when the env isn't activated.

## Scripts

| Script | Question it answers |
|---|---|
| `trapcalc.py` | Shared physics: pseudopotential, secular frequencies, DC solve, detector solid angle. Lifted from `electrode/workflow.ipynb`. |
| `trapgeom.py` | Parametric five-wire geometry used by the sims in steps 2–6. |
| `01_analytic_fivewire.py` | Collection vs heating vs height; geometry family at h = 50 µm (House/Wesenberg gapless model). |
| `02_baseline_gds2itvg.py` | Baseline in gds2itvg vs the analytic model. |
| `03_segment_pitch.py` | Outer-segment pitch vs DC voltages and conditioning. |
| `04_window_validation.py` | 2-D finite-difference cross-section of window variants; RF-rail termination (Todaro mechanism). |
| `04b_window_3d_fd.py` | 3-D finite-difference check of the finite readout window (height shift, axial RF field). |
| `05_window_variants.py` | Window variants in the planar gds2itvg model (RF null, barrier, DC). |
| `06_detector_size.py` | Detector/window size vs collection, nanowire length, reset time. |
| `09_optical_stack_tmm.py` | NbN absorption at 493 nm vs spacer/cap/ITO thickness (transfer matrix). |
| `10_rf_pickup_2d.py` | RF field at the nanowire with/without the Al mirror and ITO; RF capacitance. |
| `11_beam_clearance.py` | Laser clipping on the chip; corner placement of the zones. |
| `12_final_chip_check.py` | Simulates the **fabrication GDS itself**: RF null along the axis, DC sets at both zones, transport waveforms. |
