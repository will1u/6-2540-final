# 6.2540 Final Project: Surface-Electrode Ion Traps

> **Claude-authored** index page, written at the team's request on 2026-11-11. It says where things are and how to run them. It does not describe the project's motivation, methods or results; those are in the team's own documents.

Final project for MIT 6.2540: a microfabricated surface-electrode ion trap. The design package in [design/](design/README.md) is a five-wire ¹³⁸Ba⁺ surface trap with an integrated NbN superconducting nanowire single-photon detector (SNSPD).

## Where to start

| If you want | Read |
|---|---|
| A one-page map of the chip, its key numbers, decisions and open items | [design/START_HERE.md](design/START_HERE.md) |
| What the team has decided, and why | [notes/decisions.md](notes/decisions.md) |
| What is still open | [design/fab/OPEN_DECISIONS.md](design/fab/OPEN_DECISIONS.md) |
| Current status and the done list | [CLAUDE_PROGRESS.md](CLAUDE_PROGRESS.md) |
| The meaning of a label (A30, NODET, E1/E2, R1_ONE, ...) | [design/GLOSSARY.md](design/GLOSSARY.md) |
| Every simulation, with its question and headline number | [design/sim/INDEX.md](design/sim/INDEX.md) |
| The fabrication process | [design/fab/README.md](design/fab/README.md) |
| The full design history, latest steps first | [design/DESIGN_LOG.md](design/DESIGN_LOG.md) |

## Repo layout

| Path | What it is | Written by |
|---|---|---|
| `proposal/` | Project proposal: `main.tex` (REVTeX 4.2) and `references.bib` | Team |
| `notes/decisions.md` | Decision log: each design choice, the options rejected and the team's reason | Team's decisions; Claude writes the entries |
| `design/` | Design package: GDS generators, simulations, fab documents, literature report, primers. Index: [design/README.md](design/README.md) | Claude, at the team's request |
| `design/gds/` | Layout generators and checkers (`make_chip.py`, `check_chip.py`, `make_snspd_die.py`, `make_run.py`, `check_run.py`, ...) and the generated GDS files | |
| `design/sim/` | Numbered simulation scripts; outputs in `design/sim/out/<script>/` (tracked) | |
| `design/fab/` | Process pages, run sheet, test plan, decision briefs (linked Obsidian notes) | |
| `design/research/` | Literature report and the research notes behind it | |
| `design/primers/` | RF primer and the scripts that produce its numbers and circuit figures | |
| `design/figures/` | Plot style and the scripts that draw the report figures | |
| `CLAUDE_PROGRESS.md` | Running status of the design package | Claude |
| `CLAUDE.md`, `AGENTS.md` | Rules for AI agents working in this repo (identical files). `design/` has its own pair with folder-specific rules | Team |

## Setup

Every simulation runs on **gds2itvg** from the [`electrode`](https://github.com/felixknollmann/electrode) repo (not NIST's `electrode` package). Clone it next to this repo, so the two folders are siblings, and install its conda env once:

```bash
git clone https://github.com/felixknollmann/electrode
conda create -n electrode python=3.12
conda activate electrode
pip install -e "electrode[test,plot]"
cd 6-2540-final/design/sim && ./run.sh -c "import gds2itvg; print('ok')"
```

- `run.sh` finds the env through `$ELECTRODE_ENV`, or else `<conda base>/envs/electrode`.
- On Windows, run it from Git Bash. `run.sh` puts the env's DLL folders on PATH; without that, numpy and matplotlib crash when the env is not activated.
- The course env (Python 3.9, gdspy) cannot run gds2itvg.
- `24_rcwa_meander.py` needs a separate `rcwa` conda env; see its docstring.
- Do not edit the `electrode` repo.

Full setup notes: [design/CLAUDE.md](design/CLAUDE.md), "Setting up the electrode repo".

## Running

All scripts run through `design/sim/run.sh`:

```bash
cd design/sim
./run.sh 01_analytic_fivewire.py
./run.sh ../gds/make_chip.py && ./run.sh ../gds/check_chip.py trap_die_v4_A30
./run.sh 12_final_chip_check.py ../gds/trap_die_v4_A30_sim.json
```

The last one simulates the fabrication GDS and takes about 3 minutes per die. The order for regenerating every layout is in [design/CLAUDE.md](design/CLAUDE.md), "Regenerating and checking".

For the 2026-11-12 pass (the SNSPD-only die and the run R1_ONE):

```bash
cd design/sim
./run.sh ../gds/make_snspd_die.py
./run.sh ../gds/check_snspd_die.py
./run.sh ../gds/make_run.py R1_ONE
./run.sh ../gds/check_run.py R1_ONE
```

Sim 24b (`24b_rcwa_stack_scan.py`) needs the separate `rcwa` env, as sim 24 does.

## New files, 2026-11-12

| File | What it is |
|---|---|
| `design/gds/make_snspd_die.py` | Generates `snspd_die_v4.gds`, the SNSPD-only die: eight A30 detector cells D1–D8, T3, T11 |
| `design/gds/check_snspd_die.py` | Independent checker for that die |
| `design/gds/check_run.py` | Run-level checker, for `R1_ONE` |
| `design/gds/make_run.py` | Now takes a run name; `R1_ONE` is the next run (3 × 3 block, 9 dies) |
| `design/sim/22b_base_sio2_sweep.py` | Chip RF capacitance against base SiO₂ thickness |
| `design/sim/24b_rcwa_stack_scan.py` | RCWA scan of the spacer and cap (`rcwa` env) |
| `design/sim/10c_mirror_thickness.py`, case `al100_cap110` | Slot cross-section of the final stack |

## Checks before committing

| After changing | Run (from `design/sim`) | Must print |
|---|---|---|
| A trap die | `./run.sh ../gds/check_chip.py trap_die_v4_<variant>` | `ALL CHECKS PASS` |
| A test die | `./run.sh ../gds/make_test_die.py`, then `./run.sh ../gds/check_test_die.py test_die_v4` | `SELF-CHECK PASS`, `ALL CHECKS PASS` |
| The SNSPD-only die | `./run.sh ../gds/check_snspd_die.py` (from `design/sim`) | `ALL CHECKS PASS` |
| The run R1_ONE | `./run.sh ../gds/check_run.py R1_ONE` (from `design/sim`) | `ALL CHECKS PASS` |
| Any page under `design/` | `./run.sh ../fab/check_links.py ..` | 0 broken links |
| Any page or simulation output | `./run.sh ../check_numbers.py` | `ALL NUMBERS CONSISTENT` |

## Building the proposal

```bash
cd proposal && latexmk -pdf main
```

Or `pdflatex → bibtex → pdflatex → pdflatex`. A single `pdflatex` run leaves new citations undefined. PDFs and LaTeX auxiliary files are not tracked.

## Conventions

- Name materials explicitly: SiO₂, ITO, Al, NbN, Si₃N₄, never "oxide" or "metal".
- Every Claude-written page starts with a "Claude-authored" line. The proposal and the decisions are the team's.
- Team decisions go in `notes/decisions.md`; proposals and open options go in `design/fab/OPEN_DECISIONS.md` or `design/DESIGN_LOG.md`.
- Units are µm in layouts; coordinate frames, electrode numbers and GDS layers are in [design/CLAUDE.md](design/CLAUDE.md), "Conventions", and [design/gds/layer_map.md](design/gds/layer_map.md).
