# design/: five-wire ¹³⁸Ba⁺ surface trap with an integrated NbN SNSPD

> **Claude-authored.** Context for AI agents (Claude Code, Codex and others) working in `design/`.
> - `CLAUDE.md` and `AGENTS.md` in this folder are identical. Edit both together.
> - The repo-root `CLAUDE.md` / `AGENTS.md` rules still apply; this file adds what is specific to `design/`.

## What this folder is

A fabrication-ready design package for a five-wire surface trap:
- segmented outer DC electrodes;
- a loading zone, plus a readout zone directly above an integrated NbN SNSPD;
- Au electrodes over an Al ground plane, on high-resistivity Si;
- the SNSPD under SiO₂ only (v3: no indium tin oxide, ITO).

It holds GDS generators, simulations, a literature report, and fab documents for MIT.nano. The package is run as small R&D runs, not a production wafer.

## Rules for this folder (agreed with the team, 2026-11-02)

- **Agreed exception to the root rules:** in `design/`, Claude makes design calls and flags problems honestly. The team asked for this package.
- **Authorship:** every Claude-written doc lives in `design/` (or `../CLAUDE_PROGRESS.md`) and starts with a **"Claude-authored"** line.
- **Off limits:** never touch `proposal/*.tex` or `notes/decisions.md`. When a team member makes a decision, remind them to log it there themselves.
- **Logging:**
  - After every design step, append an entry to `DESIGN_LOG.md`: date, script, inputs, key numbers, decision, citation.
  - Keep `../CLAUDE_PROGRESS.md` current: goal, deliverables, done list, open items. Team members read it to pick up the work.
- **Citations:** any source you have read, not only `references_design.bib`: papers and other sources you search for, and the team's "Notes for 6.2540" Google Doc (root `CLAUDE.md`, Literature review). Add sources a design doc cites to `references_design.bib`. Flag anything you could not open or only saw as a search excerpt.
- **Name materials explicitly** (team rule, 2026-11-07): write SiO₂, ITO, Al, NbN, Si₃N₄, never shorthand like "oxide" or "metal", and never a script's internal case label (e.g. 04b's `oxide` / `ito6`) without saying what it means ("bare-SiO₂ window floor"). Applies to chat and to docs.
- **Tags in the fab docs:**
  - `[verify]`: not yet checked on the tool or against the source;
  - `[team calc]`: computed for this project;
  - `[inference]`: reasoning, not data.
- **Code style:** plain numbered scripts, few abstractions, matching the surrounding style. Simulation outputs go to `sim/out/<script>/`.
- **Don't edit the `electrode` repo** (the sibling clone `../electrode`, see below). A test pins the output of `examples/fivewire`.

## Setting up the electrode repo (do this first)

Every simulation here runs on **gds2itvg** from the `electrode` repo ([felixknollmann/electrode](https://github.com/felixknollmann/electrode)). An AI agent can only check a layout change, rerun a study or answer a "will this work?" question when that repo and its conda env are installed. Without them, it can only edit files and guess at the physics. Each team member sets this up once:

```bash
# next to this repo, so the two folders are siblings: <parent>/6-2540-final and <parent>/electrode
git clone https://github.com/felixknollmann/electrode
conda create -n electrode python=3.12
conda activate electrode
pip install -e "electrode[test,plot]"    # gds2itvg + numba (fast kernel) + matplotlib
cd 6-2540-final/design/sim && ./run.sh -c "import gds2itvg; print('ok')"
```

- `run.sh` finds the env through `$ELECTRODE_ENV`, or else `<conda base>/envs/electrode`. Set `ELECTRODE_ENV` if the env lives somewhere else.
- The course env (Python 3.9, gdspy) cannot run gds2itvg.

## Environment

- Conda env **`electrode`** (Python 3.12: gds2itvg, gdstk, shapely, scipy, numba).
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
| `DESIGN_LOG.md` | Steps 0–24: every design step with numbers and citations. **Read the latest steps first.** |
| `README.md` | Folder index and script list |
| `SIMPLIFICATIONS.md` | Wafer and run options; 14 possible simplifications, each with tests (a plan; nothing run) |
| `research/reports/Trap integrated SNSPD design.md` | Literature report (28 design implications); raw notes in `research/research_notes/` |
| `research/reports/SNSPD geometry audit.md` | Audit of the v3 meander against the SNSPD-geometry literature (Clem & Berggren, Suleimen 2026, Hampel); basis of step 24 |
| `research/reports/Bond pad sizing for ion traps.md` | Bond pad size, spacing and bonding rules; basis of step 21 |
| `references_design.bib` | Verified references |
| `sim/` | `trapcalc.py` (shared physics), `trapgeom.py` (parametric geometry), numbered studies `01`–`15` (13 = DC height tuning, 14 = staircase vs uniform segments, 15 = SNSPD geometry budget) |
| `gds/make_chip.py` | 10 × 10 mm trap dies: `trap_die_v3_A30` (default), `_B60` (`--det60`), `_NODET` (`--nodet`, no SNSPD), `_UNIFORM` (`--uniform`, simulation reference only: equal-depth outer DC rectangles, no leads; never for fab). Writes `.gds`, `_sim.json` (gds2itvg layout) and `_pads.csv`. |
| `gds/make_test_die.py` | 10 × 2.5 mm `test_die_v3` (T1–T4b, T6, T8, T9; T8 = EBL dose array, T9 = SNSPD geometry array); `--trap-only` → `test_die_v3_TRAP` (T1, T2, T6) |
| `gds/snspd_geom.py` | `meander()` and `straight()`: the NbN geometry shared by `make_chip.py` and `make_test_die.py` (step 24) |
| `gds/make_run.py` | R&D run layouts: `run_R1_TRAP`, `run_R1_FULL` (8 dies at the wafer centre). Edit `RUNS` to add a run; every column must stack the same die heights so the saw cuts run straight (asserted). |
| `gds/make_wafer.py` | Full-wafer reference, `wafer_v3` (56 dies) |
| `gds/check_chip.py` | DRC, connectivity and fab-consistency checks, plus preview PNGs |
| `gds/layer_map.md` | Layers, process order, key coordinates |
| `gds/archive_v1_square/`, `gds/archive_v2_narrow/` | Superseded layouts (v1 square die with corner zones; v2 narrow 10 × 2.5 mm die with the two-ITO window). Do not use. |
| `fab/README.md`, `fab/VARIANTS.md`, `fab/OPEN_DECISIONS.md` | Human-facing fab overview, variant comparison and unresolved decisions / qualification checklist |
| `fab/TRAVELER.md` | Index of steps 0–19 in `fab/process/`; `fab/QUALIFICATION.md` for witnesses; `fab/variants/LOCAL_MIRROR.md` for the proposal |
| `fab/RUNSHEET_R1_TRAP.md` | Streamlined sheet for the first run (trap only, no EBL) |
| `fab/mask_list.md`, `process_checks.md`, `test_plan.md` | Exposure jobs; go/no-go checks; electrical, cryogenic and trapping tests |

## Regenerating and checking

Order matters: runs and the wafer import the die GDS files.

```bash
cd design/sim
./run.sh ../gds/make_chip.py && ./run.sh ../gds/make_chip.py --det60 && ./run.sh ../gds/make_chip.py --nodet
./run.sh ../gds/make_test_die.py && ./run.sh ../gds/make_test_die.py --trap-only
./run.sh ../gds/make_wafer.py && ./run.sh ../gds/make_run.py
for v in A30 B60 NODET; do ./run.sh ../gds/check_chip.py trap_die_v3_$v; done
```

```bash
cd design/sim && ./run.sh 12_final_chip_check.py ../gds/trap_die_v3_A30_sim.json
```

The simulation takes about 3 minutes per die; run it in the background.

After any change to a die:
- `check_chip.py` must print `ALL CHECKS PASS`;
- if layer 50 changed, re-run `12_final_chip_check.py`;
- then log the step.

The test die has no checker script. Check it with a short gdstk/shapely snippet: Au conductor count, ≥ 5 µm spacing, and every NbN structure touching its own leads.

## Conventions

- **Units and die:** µm, GDS database unit 1 nm. Trap die 10 × 10 mm (test die 10 × 2.5 mm), centre (0, 0). Trap axis is GDS y = 0, running along x. Pads on the top/bottom die edges at |x| ≤ 3.5 mm and near y = 0 on the side edges; none in the beam-exit corners.
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
  | 24 | M1 via | retired in v3 (must stay empty) |
  | 30 | top ITO | retired in v3 (must stay empty) |
  | 31 | buried ITO | retired in v3 (must stay empty) |
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
| Ion height | 50.08 / 50.09 µm (loading / readout, planar model); over the bare-SiO₂ window the 3-D recess lowers it by 1.38 µm (A30, ≈ 48.7 µm) or 2.50 µm (B60, ≈ 47.6 µm) (sim 04b, an upper bound) |
| DC | axial 0.8 MHz, ±10 V DACs. Loading zone and NODET readout: max 9.05 V with a 10° radial tilt. **A30/B60 readout (open window): the 10° tilt needs 13.2 / 15.2 V (over the DAC range); no tilt needs 6.6 / 3.4 V** (DESIGN_LOG step 19). Transport max 7.33 V; ≤ 1.6 V per 10 µm step (A30), up to 4.5 V per step near the B60 window |
| Detector | v3.1 (step 24): NbN meander 130 nm / 200 nm pitch (f 0.65), 160 lines over 32 µm, lines 36 µm (A30) / 69 µm (B60), rounded end blocks and tapered tabs outside the light footprint (`gds/snspd_geom.py`). Geometric collection (isotropic Ba⁺ 493 nm emission) 2.23 % (A30 window) / 4.20 % (B60); absorption ≈ 0.54 (EMT; v3 f 0.5: 0.40). 95 % of it lands on the NbN with the 1 µm radial overhang. Product ≈ 1.15 % / 2.2 % (sim 15). RF pickup bound 1.67 µA (1.19× v3; sim 10 v3.1 scan) |
| Window stack | No ITO (v3): Al mirror / SiO₂ spacer 238 nm / NbN / SiO₂ cap 80 nm / 10 µm D2 SiO₂; the ion sees bare SiO₂ in the 30 µm Au opening. RF pickup bound 1.4 µA (sim 10, case f) |
| Die / beams | 10 × 10 mm die, trap on the centre line: ~1.7e-2 of the 493 nm beam clips the surface (sim 11) |

## Physics decisions not to undo without a reason

- **Window placement:** keep the readout window *inside* the centre DC electrode. Never cut across it or into the RF rails; that gives a 14–20 µm height drop and an axial barrier (DESIGN_LOG step 6).
- **RF rail ends:** the rails run ≥ 1.7 mm past both zones, so the ends have no termination effect on the zones. Todaro's lower ion over the detector came from rail termination plus the recess, not from any SNSPD field.
- **If ITO ever comes back:** every ITO must be grounded or tied to an electrode. A floating ITO raised RF pickup 9× (step 10).
- **Keep the fill-to-M1 ground vias** (DESIGN_LOG step 22). They tie the Au ground fill to the Al mirror on chip, as Hampel 2023 does. Without them the mirror is grounded only by bond wires, and a floating mirror is the worst case for RF pickup (Hampel Fig. 3(a); step 10).
- **Keep the L45 protect patch over the readout window.** With no ITO, it is the only thing that stops the Au-masked gap etch going down through the window SiO₂ toward the NbN.
- **SNSPD turns stay outside the light footprint** (DESIGN_LOG step 24). The NbN lines run past the window (3 µm A30, 4.5 µm B60 axially; 1 µm radially, the most the RF budget allows) because light refracts 2.6–3.9 µm outward in the 10 µm SiO₂; the end blocks and tabs sit beyond that, under Au. `check_chip.py` checks it, plus NbN gaps ≥ 60 nm and \|y\| ≤ 17 µm. A meander the size of the window loses ~20 % of the light; the 1 µm radial overhang still loses ~5 %.
- **Collection uses an isotropic emitter** for Ba⁺ 493 nm (`collection_fraction(..., "iso")`), not "sigma" (step 24).
- **Transport solves:** use a fixed electrode set with zero tilt. Letting the active set change gives 3 V jumps per step (step 11).

## Current state (2026-11-07)

- **v3:** no ITO anywhere, 10 × 10 mm trap die with edge pads (DESIGN_LOG steps 17–19). All three trap dies pass `check_chip.py`; sims 04b, 09b, 10, 12 and 13 were rerun on v3.
- **First run: R1_TRAP**, trap-only (team decision). Use `fab/RUNSHEET_R1_TRAP.md`. It is unaffected by the ITO removal; only the die size and areas changed.
- Still open before the run:
  - short loops: D2 stress, gap-etch rate, W5 plating;
  - facility questions for MIT.nano staff: which tools accept Au, the gold plating tank, training order.
- Full list of open items: `../CLAUDE_PROGRESS.md`.

## Gotchas

- `check_chip.py` previews fail to write if the PNG is open in a viewer; it catches the error and continues.
- In gdstk, `Polygon.area()` is a method, not a property.
- `make_chip.py` keeps only the largest ground-fill piece, so enclosed fill islands vanish silently. `check_chip.py` reports floating Au.
