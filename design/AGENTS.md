# design/: five-wire ¹³⁸Ba⁺ surface trap with an integrated NbN SNSPD

> **Claude-authored.** Context for AI agents (Claude Code, Codex and others) working in `design/`.
> - `CLAUDE.md` and `AGENTS.md` in this folder are identical. Edit both together.
> - The repo-root `CLAUDE.md` / `AGENTS.md` rules still apply; this file adds what is specific to `design/`.

## What this folder is

A fabrication-ready design package for a five-wire surface trap:
- segmented outer DC electrodes;
- a loading zone, plus a readout zone directly above an integrated NbN SNSPD;
- Au electrodes on a thin SiO₂ stack over high-resistivity Si (ρ > 20 kΩ·cm), with no ground plane: **v4 local-mirror architecture** (team decision, 2026-11-08). The Al is a local mirror under the SNSPD and its leads only, as in Hampel 2023;
- the SNSPD under SiO₂ only (no indium tin oxide, ITO, since v3); its leads are Au in a slot along the centre DC.

It holds GDS generators, simulations, a literature report, and fab documents for MIT.nano. The package is run as small R&D runs, not a production wafer.

## Rules for this folder (agreed with the team, 2026-11-02)

- **Agreed exception to the root rules:** in `design/`, Claude makes design calls and flags problems honestly. The team asked for this package.
- **Authorship:** every Claude-written doc lives in `design/` (or `../CLAUDE_PROGRESS.md`) and starts with a **"Claude-authored"** line.
- **Off limits:** never touch `proposal/*.tex`.
- **Decisions:** when a team member makes a decision, log it in `../notes/decisions.md` in the same session (root `CLAUDE.md`, Decision log; team change, 2026-11-08).
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
| `DESIGN_LOG.md` | Every design step from step 0 on, with numbers and citations. **Read the latest steps first.** |
| `START_HERE.md` | One-page entry: the chip, the die map and stack, the defining numbers, the team's decisions, open items, tests, and where to go next. **New readers start here.** |
| `GLOSSARY.md` | Every short label (dies, runs, E1/E2, layers, electrodes, T/W/a/b IDs, suffixes, symbols) with a link to its definition |
| `check_numbers.py`, `facts_now.json` | Prints each key number from the sim outputs, checks that the current-state pages quote it, and flags known stale strings. `facts_now.json` holds pointers (file and key), not values. Run it after any doc or sim change |
| `README.md` | Folder index and script list |
| `SIMPLIFICATIONS.md` | Wafer and run options; 14 possible simplifications, each with tests (a plan; nothing run) |
| `research/reports/Trap integrated SNSPD design.md` | Literature report (28 design implications); raw notes in `research/research_notes/` |
| `research/reports/SNSPD geometry audit.md` | Audit of the v3 meander against the SNSPD-geometry literature (Clem & Berggren, Suleimen 2026, Hampel); basis of step 24 |
| `research/reports/Bond pad sizing for ion traps.md` | Bond pad size, spacing and bonding rules; basis of step 21 |
| `references_design.bib` | Verified references |
| `sim/` | `trapcalc.py` (shared physics), `trapgeom.py` (parametric geometry), numbered studies `01`–`24`, indexed in `sim/INDEX.md` with the question, headline number and validity of each (13 = DC height tuning, 14 = staircase vs uniform segments, 15 = SNSPD geometry budget on v3, 15b = collection and absorption on v4, 16 = pad pitch, 17 = ion height trade-off, 18 = E1 vs E2, 19 = SNSPD lead termination, 20 = transport timing, 21 = transport waveform, 22 = chip RF capacitance, 23 = DC-to-RF coupling, 24 = RCWA of the meander, which runs in a separate `rcwa` conda env: see its docstring). Superseded loose logs are in `sim/out/archive/` |
| `gds/make_chip.py` | v4 10 × 10 mm trap dies: `trap_die_v4_A30` (default), `_B60` (`--det60`), `_NODET` (`--nodet`: no SNSPD, no Al; the R1_TRAP die), `_UNIFORM` (`--uniform`, simulation reference only; never for fab). Writes `.gds`, `_pads.csv`, `_sim.json` (electrode option E2, 6 µm Au) and, for A30/B60, `_E1_sim.json` (0.35 µm Au) plus `_simfloor.gds` (simulation only: layer 50 + the grounded window floor; never for fab). |
| `gds/archive_v3_baseline/` | v3 dies (die-wide Al + 10 µm D2, A30/B60/NODET/UNIFORM), runs and wafer. Superseded 2026-11-08; sim 14 still reads its NODET/UNIFORM files. |
| `gds/make_test_die.py` | 10 × 2.5 mm `test_die_v4` for the v4 stack (step 35): T1 Au comb, T2v Au / 0.40 µm SiO₂ / Al capacitor, T3 NbN bar, T4/T4b spare SNSPDs, T6 Au loop, T8 EBL dose array, T9 SNSPD geometry array, T10 Al mirror strip four-point (taps 2510 µm apart), T11 Au-to-Al via chain, T12 twin Au leads over Al. Every meander sits on its own local Al mirror with a probe pad. `--trap-only` → `test_die_v4_TRAP` (T1 and T6; layers 1 and 50 only). The script ends with a self-check and writes a preview PNG. v3 test dies are in `gds/archive_v3_baseline/`. |
| `gds/check_test_die.py` | Independent checker for the test dies, written from the specification (not from the generator): Au spacing, NbN on its own leads, every opening on Al or Ti/Au and covered by Au, a mirror under every meander, T1/T2v/T6/T10/T11/T12 connectivity. |
| `gds/measure_dies.py` | Read-only measurement of the released GDS files → `gds/measured_v4.md` / `.json`: area per layer, Au area per run, meander line count, squares, inductance, file hashes. The fab pages cite it. Rerun it after any layout change. |
| `gds/snspd_geom.py` | `meander()` and `straight()`: the NbN geometry shared by `make_chip.py` and `make_test_die.py` (step 24) |
| `gds/make_run.py` | R&D run layouts: `run_R1_TRAP` (6 NODET + 2 TEST_TRAP), `run_R1_FULL` (2 A30 + 2 B60 + 2 NODET + 2 TEST), 8 dies at the wafer centre. Edit `RUNS` to add a run; every column must stack the same die heights so the saw cuts run straight (asserted). |
| `gds/make_wafer.py` | Full-wafer reference, `wafer_v4` (56 dies: 25 A30 + 14 B60 + 17 TEST) |
| `gds/check_chip.py` | DRC, connectivity and fab-consistency checks, plus preview PNGs |
| `gds/layer_map.md` | Layers, process order, key coordinates |
| `gds/archive_v1_square/`, `gds/archive_v2_narrow/` | Superseded layouts (v1 square die with corner zones; v2 narrow 10 × 2.5 mm die with the two-ITO window). Do not use. |
| `fab/README.md`, `fab/VARIANTS.md`, `fab/OPEN_DECISIONS.md` | Human-facing fab overview, variant comparison and unresolved decisions / qualification checklist |
| `fab/TRAVELER.md` | Index of steps 0–19 in `fab/process/`, **v4 since 2026-11-09** (step 36). Steps 9, 10, 16a and 16 are removed; steps 12–15 are written twice, as branch E1 and branch E2, until the team chooses. `fab/QUALIFICATION.md` for witnesses; `fab/variants/LOCAL_MIRROR.md` for the argument behind the architecture |
| `fab/figures/` | `stack_v4.svg` (cross-sections of the final stack), `process_flow_v4.svg` (one composite cross-section per step; written by `make_process_flow.py`), `architecture_crosssection.svg` (v3 against v4) |
| `fab/check_links.py` | Checks every relative link and heading anchor under `design/fab`. Run it after editing any fab page |
| `fab/RUNSHEET_R1_TRAP.md` | Streamlined sheet for the first run (trap only, no EBL) |
| `fab/mask_list.md`, `process_checks.md`, `test_plan.md` | Exposure jobs; go/no-go checks; electrical, cryogenic and trapping tests |
| `fab/tests/00_SETUP.md`, `05_SIMPLER_TESTING.md` | What each test needs on the bench (signal chains, equipment, questions for the lab); what could replace the wafer-level test and what each option misses |
| `fab/briefs/` | One page per open design choice: options, numbers side by side with their sources, what is not known. No recommendation; the choice is the team's |
| `primers/RF_PRIMER.md`, `primer_numbers.py` | Basics of RF drive, loss, pickup, filters and SNSPD readout, worked on this chip; the script prints every number in the page |
| `figures/` | `plotstyle.py` (one plot style), `make_die_map.py`, `make_report_figures.py` → `figures/report/` (plots for the team's report: axis labels and legends only, no captions) |
| `research/research_notes/Test setup 2026-11/` | Reading pointers for testing: Dietl 2025 (from the PDF), SNSPD bench tests, electrical screening |

## Regenerating and checking

Order matters: runs and the wafer import the die GDS files.

```bash
cd design/sim
./run.sh ../gds/make_chip.py && ./run.sh ../gds/make_chip.py --det60 && ./run.sh ../gds/make_chip.py --nodet && ./run.sh ../gds/make_chip.py --uniform
./run.sh ../gds/make_test_die.py && ./run.sh ../gds/make_test_die.py --trap-only
./run.sh ../gds/make_wafer.py && ./run.sh ../gds/make_run.py
for v in A30 B60 NODET; do ./run.sh ../gds/check_chip.py trap_die_v4_$v; done
```

```bash
cd design/sim && ./run.sh 12_final_chip_check.py ../gds/trap_die_v4_A30_sim.json      # also _E1_sim.json, NODET
```

The simulation takes about 3 minutes per die; run it in the background.

After any change to a die:
- `check_chip.py` must print `ALL CHECKS PASS`;
- if layer 50 changed, re-run `12_final_chip_check.py`;
- then log the step.

After any change to a test die: `make_test_die.py` must print `SELF-CHECK PASS`, and `./run.sh ../gds/check_test_die.py test_die_v4` (and `test_die_v4_TRAP`) must print `ALL CHECKS PASS`. Then rerun `make_wafer.py`, `make_run.py` and `measure_dies.py`.

After editing any page under `design/`: `./run.sh ../fab/check_links.py ..` must report 0 broken links, and `./run.sh ../check_numbers.py` must end with `ALL NUMBERS CONSISTENT`. When a key number changes, change the pointer or the expected pages in `facts_now.json`, not the checker.

## Conventions

- **Units and die:** µm, GDS database unit 1 nm. Trap die 10 × 10 mm (test die 10 × 2.5 mm), centre (0, 0). Trap axis is GDS y = 0, running along x. Pads on the top/bottom die edges at |x| ≤ 3.5 mm and near y = 0 on the side edges; none in the beam-exit corners.
- **Zones:** loading (−240, 0); readout/SNSPD (+240, 0); 480 µm apart (team decision 2026-11-08: the team's laser setup; v3 and earlier: ±300, 600 µm).
- **Simulation frame** (`*_sim.json`): origin at the readout zone, `quarter_turns: 1`, so **ITVG y = GDS x − 240**. Loading is at ITVG y = −480.
- **Electrode numbers** (match `_sim.json` and `_pads.csv`):
  - 1 = RF;
  - 2 = centre DC (on A30 a U around the lead slot; seed on its top half);
  - 3–17 = top segments (left → right), 18–32 = bottom segments;
  - 33/34 = top caps (L/R), 35/36 = bottom caps;
  - ground seed = `99`; on A30 also `97` / `98` = the SNSPD signal / return leads (held at ~0 V) and `96` = the window floor (sim-only, in `_simfloor.gds`).
  - gds2itvg needs exactly one seed per conductor.
- **Layers:**

  | Layer | Name | Note |
  |---|---|---|
  | 1 | MARK | |
  | 10 | M1 | Al: v4 local mirror (A30, B60) |
  | 20 | NbN | datatype 0 = nominal dose, 1–7 = T8 dose array |
  | 22 | Ti/Au | v4: contacts from the NbN tabs into the slot + EBL marks only |
  | 24 | M1 via | retired in v3 (must stay empty) |
  | 30 | top ITO | retired in v3 (must stay empty) |
  | 31 | buried ITO | retired in v3 (must stay empty) |
  | 40 | openings | v4: cap openings for the SNSPD contacts, mirror ground via |
  | 45 | protect | retired in v4 (no gap etch; must stay empty) |
  | 50 | Au | electrodes, ground fill and (v4) the SNSPD leads; **the layer gds2itvg simulates** |
  | 100 | notes | not fabricated |
  | 101 | outlines | not fabricated |

  Details in `gds/layer_map.md`.
- **Names:**
  - die variants: A30, B60, NODET (v3 files archived);
  - test dies: TEST, TEST_TRAP;
  - runs: R1_TRAP, R1_FULL;
  - die IDs come from `gds/run_<name>_map.csv`.

## Key design numbers

| Item | Value |
|---|---|
| Geometry | centre DC 40 µm (A30: split by a 25 µm lead slot up to 20 µm before the NbN tabs), RF rails 84 µm, gaps 5 µm; Au (E2 6 µm or E1 0.35 µm, open) on ~1.3 µm SiO₂ over HR Si, no ground plane; local Al mirror \|y\| ≤ 20 µm, 100 nm thick, inlaid in the thermal SiO₂ (was 450 nm until 2026-11-09); 15 + 15 segments at 120 µm pitch (100 µm before step 28) |
| RF drive | 53 V at 28 MHz → radial ~3.0 MHz, q 0.30, depth ≈ 52 meV |
| Ion height | v4: 49.97 / 49.98 µm (loading / readout, planar model); over the window the grounded-floor recess lowers it by 1.19 µm (E2, ≈ 48.8 µm) or ≤ 0.37 µm (E1) (sim 04b `mirror_t6` / `mirror_t1`) |
| DC | axial 0.8 MHz, ±10 V DACs (the lab's Sinara Zotino: 32 channels for 35 DC electrodes, 16 bit, 1 MSPS shared between channels, 75 kHz 3rd-order output filter; `research/research_notes/Test setup 2026-11/T4_zotino_dac.md`), 10° radial tilt in the zones. v4 (480 µm zones, step 28): loading 7.5 V, readout 6.3 V (A30) / 2.2 V (B60) (v3 needed 13.2 / 15.2 V); NODET 7.9 V. **Transport on A30/B60: hold the centre DC at 0 V** (`12 --centre-dc-zero`: max 6.6 V, ≤ 1.71 V per 10 µm step); with it free, the slot end and window give 8 V steps (DESIGN_LOG step 25). Ramp the tilt in at the zone. Voltages against time for a 1 ms minimum-jerk move with the tilt ramped out and in are in `sim/out/21_transport_waveform/` (step 40; it assumed 1 MHz updates on every channel and a first-order filter, which the Zotino does not give, so it needs a rerun) |
| Detector | A30 and B60 (B60 dropped and kept again 2026-11-08). v3.1 (step 24): NbN meander 130 nm / 200 nm pitch (f 0.65), 160 lines over 32 µm, lines 36 µm (A30) / 69 µm (B60), rounded end blocks and tapered tabs under Au (`gds/snspd_geom.py`). Geometric collection on v4 (isotropic Ba⁺ 493 nm emission, sim 15b, step 32): A30 2.22 % (E2) / 2.60–2.64 % (E1), B60 4.16 % / 4.67–4.76 %; absorbed in NbN of all emitted photons with the 160 nm cap: A30 E2 1.47 %, B60 E2 2.71 %; absorption (EMT) **0.66 on v4 with a 160 nm cap** (0.44 with the drawn 80 nm; v3.1: 0.54; sim 09c); RCWA at normal incidence gives 0.83 unpolarised (sim 24, step 43), and the collection numbers in this row still use the EMT value. RF pickup bound (sim 10b, 2-D): nanowire 0.96 µA (E2) / 1.92 µA (E1), plus at most 0.73–0.97 µA from the mirror path with the 100 nm inlaid Al (`sim/10c`, steps 37–38; it was 0.16–0.21 µA with the 450 nm Al of step 28); each slot lead collects 44.5 µA (E2) / 28.6 µA (E1) of common-mode RF over 2.24 mm (`sim/10c`) (needs an RF trap or a symmetric termination at the pads: sim 19, step 33; a plain 1 nF bypass low-passes the pulse at 3.2 MHz) |
| Window stack | v4: local Al mirror / SiO₂ spacer 238 nm / NbN / SiO₂ (HSQ + cap) **160 ± 10 nm** (step 26; was 80) / vacuum; the ion sees the cap in the 30 µm Au opening |
| Die / beams | 10 × 10 mm die, trap on the centre line: ~1.7e-2 of the 493 nm beam clips the surface (sim 11) |
| RF circuit | Chip RF capacitance 2.59 pF (A30, E2) / 2.39 pF (A30, E1), so 24.2 / 22.3 mA at 53 V, 28 MHz; 63 % of the field energy is in the Si, so the room-temperature Q is low and does not predict the cold one (sim 22, step 41). The centre DC couples to the rails through 0.41 pF (A30, E2): with 1 nF to ground it carries 22 mV of RF and moves the null 10 nm (sim 23, step 42) |

## Physics decisions not to undo without a reason

- **Window placement:** keep the readout window *inside* the centre DC electrode. Never cut across it or into the RF rails; that gives a 14–20 µm height drop and an axial barrier (DESIGN_LOG step 6).
- **RF rail ends:** the rails run ≥ 1.7 mm past both zones, so the ends have no termination effect on the zones. Todaro's lower ion over the detector came from rail termination plus the recess, not from any SNSPD field.
- **If ITO ever comes back:** every ITO must be grounded or tied to an electrode. A floating ITO raised RF pickup 9× (step 10).
- **Keep the mirror ground via** (DESIGN_LOG steps 22, 25). It ties the local Al mirror to the Au ground fill on chip, as Hampel 2023 does. A floating mirror is the worst case for RF pickup (Hampel Fig. 3(a); step 10).
- **Never put Al under the RF rails** (v4). On the thin stack, a die-wide plane would give C_RF–ground ≈ 127 pF (step 22). `check_chip.py` checks the mirror stays at |y| ≤ 20 µm inside the trap.
- **No buried SNSPD leads under the centre DC** (v4). With only the 160 nm cap between them and the Au, a pinhole would short the SNSPD to electrode 2; the leads are Au in the slot (team decision). Layer 22 is contacts only.
- **SNSPD turns stay outside the light footprint** (DESIGN_LOG step 24). The NbN lines run past the window (3 µm axially, 1 µm radially) with the end blocks and tabs beyond, under Au. In v3 light refracted 2.6–3.9 µm outward in the 10 µm SiO₂; in v4 only the 160 nm cap lies between the window floor and the NbN, so the footprint is essentially the window (+0.05 µm on A30, +0.07 µm on B60) and the overhang is margin. `check_chip.py` checks it, plus NbN gaps ≥ 60 nm and \|y\| ≤ 17 µm.
- **Collection uses an isotropic emitter** for Ba⁺ 493 nm (`collection_fraction(..., "iso")`), not "sigma" (step 24).
- **Transport solves:** use a fixed electrode set with zero tilt. Letting the active set change gives 3 V jumps per step (step 11).
- **Give the centre DC an RF ground** (step 42). With no capacitor to ground it would follow the RF rails: 6 V on A30, 45.5 V on NODET in the 2-D model. The value and place of the capacitor are open (`fab/briefs/rf_grounding_and_termination.md`).
- **Do not update the DACs at a sub-multiple of the axial frequency** (step 40). At 100 kHz updates and 0.8 MHz axial, every step kicks the ion at the same phase.

## Current state (2026-11-10)

- **v4: local-mirror architecture** (team decisions in `../notes/decisions.md`; DESIGN_LOG step 25). A30 and NODET pass `check_chip.py`; sims 04b, 12 and 13 rerun on v4.
- **First run: R1_TRAP**, trap-only, now on the no-Al stack (Au on SiO₂ over HR Si).
- **Loose-ends pass, 2026-11-09 (DESIGN_LOG steps 30–36).** The fab pages, test dies and figures are v4. New sims 15b and 17–20. Team decision 2026-11-09: keep the 50 µm ion height (step 30; `../notes/decisions.md`). Assessment (Claude's, not a team decision): E1 and E2 trap the same but differ in gap screening, SNSPD lead resistance, light and RF heating (step 31). Team decision 2026-11-09 (steps 37–38, `sim/10c_mirror_thickness.py`; `../notes/decisions.md`): the Al mirror is 100 nm of evaporated Al, inlaid in the thermal SiO₂ (step 3 = resist, 100 nm SiO₂ recess, Al evaporation, lift-off), so the electrodes are flat. It replaces the 450 nm mirror, which left a 0.45 µm step. The mirror's pickup goes to ground (3.2 mA); the extra nanowire current is at most 0.73–0.97 µA and the strip dissipates 34–45 µW. T10 is expected at 18.8–25.1 Ω. Unproven until witness loop W8 passes. Step 39 (`sim/10d_mirror_step.py`): a 100 nm raised mirror would only lift the null 0.13–0.16 µm, so raised and inlaid are equivalent for the ion; the larger sensitivity is a sideways-misaligned mirror on E1 (0.5 µm of null shift for 2 µm), because the mirror edge is drawn on the centre-DC edge. The DC electrodes compensate it (about 18 V/m per µm), so it is not a problem. Optional proposal: mirror \|y\| ≤ 18 µm and about 1 µm overlay on layer 10.
- **Readability pass and four new sims, 2026-11-10 (DESIGN_LOG steps 40–43).** New pages: `START_HERE.md`, `GLOSSARY.md`, `sim/INDEX.md`, `primers/RF_PRIMER.md`, `fab/briefs/`, `fab/tests/00_SETUP.md` and `05_SIMPLER_TESTING.md`, `figures/`. New sims: 21 (transport waveform; reproduces the sim 12 table to 5 µV), 22 (chip RF capacitance 2.59 pF on E2), 23 (DC-to-RF coupling and filter capacitors), 24 (RCWA: absorption 0.83 against 0.66 from the effective-medium model). No team decision came out of this pass, and no layout changed.
- Still open before any run:
  - electrode Au, E1 vs E2 (the fab pages carry both branches; delete one when the team chooses);
  - SNSPD lead termination (step 33): a plain 50 Ω line with the return grounded puts about 4 µA of RF through the nanowire; and the filter capacitors on the DC lines, the centre DC first (step 42);
  - the transport waveform exists (step 40), but it assumed 1 MHz updates on every channel and a first-order filter; the lab's Zotino shares 1 MSPS between channels and has a 75 kHz 3rd-order filter, so sim 21 needs a rerun with those values;
  - DAC channels: one Zotino has 32, the die has 35 DC electrodes (sim 26, step 46);
  - pad pitch adoption, carrier, spacer, T10 acceptance limit, whether R1_TRAP gets the 398 nm PECVD SiO₂;
  - facility questions for MIT.nano staff: which tools accept Au, the gold plating tank (if E2), an evaporator for Ti/Au (if E1), training order.
- Full list of open items: `../CLAUDE_PROGRESS.md` and `fab/OPEN_DECISIONS.md`.

## Gotchas

- `check_chip.py` previews fail to write if the PNG is open in a viewer; it catches the error and continues.
- In gdstk, `Polygon.area()` is a method, not a property.
- `make_chip.py` keeps only the largest ground-fill piece, so enclosed fill islands vanish silently. `check_chip.py` reports floating Au.
