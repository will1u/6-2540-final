# design/: five-wire ¹³⁸Ba⁺ surface trap with an integrated NbN SNSPD

> **Claude-authored.** Context for AI agents (Claude Code, Codex and others) working in `design/`.
> - `CLAUDE.md` and `AGENTS.md` in this folder are identical. Edit both together.
> - The repo-root `CLAUDE.md` / `AGENTS.md` rules still apply; this file adds what is specific to `design/`.

## What this folder is

A fabrication-ready design package for a five-wire surface trap:
- segmented outer DC electrodes;
- a loading zone, plus a readout zone directly above an integrated NbN SNSPD;
- Au electrodes over an Al ground plane, on high-resistivity Si;
- the SNSPD shielded by SiO₂ and ITO.

It holds GDS generators, simulations, a literature report, and fab documents for MIT.nano. The package is run as small R&D runs, not a production wafer.

## Rules for this folder (agreed with William, 2026-11-02)

- **Agreed exception to the root rules:** in `design/`, Claude makes design calls and flags problems honestly. William asked for this package.
- **Authorship:** every Claude-written doc lives in `design/` (or `../CLAUDE_PROGRESS.md`) and starts with a **"Claude-authored"** line.
- **Off limits:** never touch `proposal/*.tex` or `notes/decisions.md`. When William makes a decision, remind him to log it there himself.
- **Logging:**
  - After every design step, append an entry to `DESIGN_LOG.md`: date, script, inputs, key numbers, decision, citation.
  - Keep `../CLAUDE_PROGRESS.md` current: goal, deliverables, done list, open items. William reads it to pick up the work.
- **Citations:** only entries verified in `references_design.bib`; flag anything uncertain.
- **Tags in the fab docs:**
  - `[verify]`: not yet checked on the tool or against the source;
  - `[team calc]`: computed for this project;
  - `[inference]`: reasoning, not data.
- **Code style:** plain numbered scripts, few abstractions, matching the surrounding style. Simulation outputs go to `sim/out/<script>/`.
- **Don't edit the `electrode` repo** (`C:\Users\willi\Repos\6.2540\electrode`). A test pins the output of `examples/fivewire`.

## Environment

- Conda env **`electrode`** (Python 3.12: gds2itvg, gdstk, shapely, scipy, numba), at `C:/Users/willi/anaconda3/envs/electrode`. The course env (Python 3.9, gdspy) cannot run gds2itvg.
- **Always run through `sim/run.sh` from Git Bash:**

  ```bash
  cd design/sim && ./run.sh <script>.py
  ```

  For one-liners use `./run.sh -c "..."`.
- `run.sh` does three things:
  - puts the env's DLL folders on PATH (without this, numpy/matplotlib crash with `0xc06d007f`);
  - sets `PYTHONIOENCODING=utf-8`;
  - sets `MPLBACKEND=Agg`.
- `conda run` rejects multi-line `-c` code, so use `run.sh`.

## Where things are

| Path | Contents |
|---|---|
| `DESIGN_LOG.md` | Steps 0–16: every design step with numbers and citations. **Read the latest steps first.** |
| `README.md` | Folder index and script list |
| `SIMPLIFICATIONS.md` | Wafer and run options; 14 possible simplifications, each with tests (a plan; nothing run) |
| `research/reports/Trap integrated SNSPD design.md` | Literature report (28 design implications); raw notes in `research/research_notes/` |
| `references_design.bib` | Verified references |
| `sim/` | `trapcalc.py` (shared physics), `trapgeom.py` (parametric geometry), numbered studies `01`–`12` |
| `gds/make_chip.py` | Trap dies: `trap_die_v2_A30` (default), `_B60` (`--det60`), `_NODET` (`--nodet`, no SNSPD). Writes `.gds`, `_sim.json` (gds2itvg layout) and `_pads.csv`. |
| `gds/make_test_die.py` | `test_die_v2` (T1–T8; T8 = EBL dose array); `--trap-only` → `test_die_v2_TRAP` (T1, T2, T6) |
| `gds/make_run.py` | R&D run layouts: `run_R1_TRAP`, `run_R1_FULL` (8 dies at the wafer centre). Edit `RUNS` to add a run. |
| `gds/make_wafer.py` | Full-wafer reference, `wafer_v2` (184 dies) |
| `gds/check_chip.py` | DRC, connectivity and fab-consistency checks, plus preview PNGs |
| `gds/layer_map.md` | Layers, process order, key coordinates |
| `gds/archive_v1_square/` | Superseded square die. Do not use. |
| `fab/TRAVELER.md` | Full process, steps 0–19; witness/short loops in section E; R&D run plan in A.3 |
| `fab/RUNSHEET_R1_TRAP.md` | Streamlined sheet for the first run (trap only, no EBL) |
| `fab/mask_list.md`, `process_checks.md`, `test_plan.md` | Exposure jobs; go/no-go checks; electrical, cryogenic and trapping tests |

## Regenerating and checking

Order matters: runs and the wafer import the die GDS files.

```bash
cd design/sim
./run.sh ../gds/make_chip.py && ./run.sh ../gds/make_chip.py --det60 && ./run.sh ../gds/make_chip.py --nodet
./run.sh ../gds/make_test_die.py && ./run.sh ../gds/make_test_die.py --trap-only
./run.sh ../gds/make_wafer.py && ./run.sh ../gds/make_run.py
for v in A30 B60 NODET; do ./run.sh ../gds/check_chip.py trap_die_v2_$v; done
```

```bash
cd design/sim && ./run.sh 12_final_chip_check.py ../gds/trap_die_v2_A30_sim.json
```

The simulation takes about 3 minutes per die; run it in the background.

After any change to a die:
- `check_chip.py` must print `ALL CHECKS PASS`;
- if layer 50 changed, re-run `12_final_chip_check.py`;
- then log the step.

The test die has no checker script. Check it with a short gdstk/shapely snippet: Au conductor count, ≥ 5 µm spacing, and every NbN structure touching its own leads.

## Conventions

- **Units and die:** µm, GDS database unit 1 nm. Die 10 × 2.5 mm, centre (0, 0). Trap axis is GDS y = 0, running along x.
- **Zones:** loading (−300, 0); readout/SNSPD (+300, 0); 600 µm apart.
- **Simulation frame** (`*_sim.json`): origin at the readout zone, `quarter_turns: 1`, so **ITVG y = GDS x − 300**. Loading is at ITVG y = −600.
- **Electrode numbers** (match `_sim.json` and `_pads.csv`):
  - 1 = RF;
  - 2 = centre DC;
  - 3–17 = top segments (left → right), 18–32 = bottom segments;
  - 33/34 = top caps (L/R), 35/36 = bottom caps;
  - ground seed = `99`.
  - gds2itvg needs exactly one seed per conductor.
- **Layers:**

  | Layer | Name | Note |
  |---|---|---|
  | 1 | MARK | |
  | 10 | M1 | Al |
  | 20 | NbN | datatype 0 = nominal dose, 1–7 = T8 dose array |
  | 22 | Ti/Au leads | |
  | 24 | M1 via | |
  | 30 | top ITO | |
  | 31 | buried ITO | |
  | 40 | D2 openings | |
  | 45 | protect | |
  | 50 | Au | **the layer gds2itvg simulates** |
  | 100 | notes | not fabricated |
  | 101 | outlines | not fabricated |

  Details in `gds/layer_map.md`.
- **Names:**
  - die variants: A30, B60, NODET;
  - test dies: TEST, TEST_TRAP;
  - runs: R1_TRAP, R1_FULL;
  - die IDs come from `gds/run_<name>_map.csv`.

## Key design numbers

| Item | Value |
|---|---|
| Geometry | centre DC 40 µm, RF rails 84 µm, gaps 5 µm, 6 µm Au on 10 µm SiO₂ over Al; 15 + 15 segments at 100 µm pitch |
| RF drive | 53 V at 28 MHz → radial ~3.0 MHz, q 0.30, depth ≈ 52 meV |
| Ion height | 50.08 / 50.09 µm (loading / readout); ≈ 48.9 µm over the A30 window, ≈ 48.1 µm over B60 |
| DC | axial 0.8 MHz, ±10 V DACs: max 9.05 V at the zones; transport max 7.33 V, ≤ 1.59 V per 10 µm step |
| Detector | A30 30 × 30 µm (3.25 % collection), B60 60 × 30 µm (5.9 %); NbN absorption ≈ 0.53 at 493 nm |
| Window stack | Two ITO layers: buried 60 nm (grounded) and top ~125 nm (tied to the centre DC) |

## Physics decisions not to undo without a reason

- **Window placement:** keep the readout window *inside* the centre DC electrode. Never cut across it or into the RF rails; that gives a 14–20 µm height drop and an axial barrier (DESIGN_LOG step 6).
- **RF rail ends:** the rails run ≥ 1.7 mm past both zones, so the ends have no termination effect on the zones. Todaro's lower ion over the detector came from rail termination plus the recess, not from any SNSPD field.
- **ITO grounding:** every ITO must be grounded or tied to an electrode. A floating ITO raised RF pickup 9× (step 10).
- **Transport solves:** use a fixed electrode set with zero tilt. Letting the active set change gives 3 V jumps per step (step 11).

## Current state (2026-11-02)

- The v2 narrow-die design is complete. All dies pass `check_chip.py`, and the simulations are DESIGN_LOG steps 13–14.
- **First run: R1_TRAP**, trap-only (William's choice). Use `fab/RUNSHEET_R1_TRAP.md`.
- Still open before the run:
  - short loops: D2 stress, gap-etch rate, W5 plating;
  - facility questions for MIT.nano staff: which tools accept Au, the gold plating tank, training order.
- Full list of open items: `../CLAUDE_PROGRESS.md`.

## Gotchas

- `check_chip.py` previews fail to write if the PNG is open in a viewer; it catches the error and continues.
- In gdstk, `Polygon.area()` is a method, not a property.
- `make_chip.py` keeps only the largest ground-fill piece, so enclosed fill islands vanish silently. `check_chip.py` reports floating Au.
