> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Fabrication overview

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!note] v4 is the adopted process; the electrode Au is still open
> The adopted architecture is the v4 local mirror: Au electrodes on a thin SiO₂ stack over high-resistivity Si, with an Al mirror only under the detector and its leads. There is no 10 µm SiO₂ (D2) and no ITO ([decisions](../../notes/decisions.md), 2026-11-08). The electrode Au is open: **E1** (Ti/Au lift-off, 0.35 µm) or **E2** (6 µm plated Au). The process pages give both branches. Do not fabricate a branch until the team chooses one.

The next run is **R1_ONE** (team decision 2026-11-12): one 100 mm wafer with a 3 × 3 block of nine dies, in five lithography layers (1 + 10, 22, 20, 40, 50). It carries four chip types: the **SNSPD-only die** (eight detector cells, no trap), the **A30** die (SNSPD and trap; the team's choice for the chips it needs), a **B60** die as the spare, and the **NODET** die (trap only). The test dies are not in this run. R1_TRAP and R1_FULL are superseded by R1_ONE and kept.

> [!important] Current readiness
> The v4 generator (`gds/make_chip.py`) implements the local-mirror stack. A30, B60 and NODET pass `check_chip.py` (DESIGN_LOG step 29). The detector generators use the v3.1 meander, and some recipe estimates still describe the earlier v3 detector. The v4 test dies are drawn and checked (2026-11-09) but are not in R1_ONE. Reconcile the detector files before the R1_ONE export: see [the reconciliation checklist](OPEN_DECISIONS.md#detector-documents-and-generated-layouts). The process still needs witness-wafer qualification and facility confirmation.

## Start with your task

| I want to… | Open |
|---|---|
| Compare runs, die sizes and process options | [Variants](VARIANTS.md) |
| See the adopted architecture | [Local mirror (adopted v4)](variants/LOCAL_MIRROR.md) |
| See undecided choices and run requirements | [Open decisions](OPEN_DECISIONS.md) |
| Plan the one-wafer run R1_ONE: which chip serves which test, the die map | [Run plan](RUN_PLAN.md) |
| Prepare the optional second wafer (layer 50 only) | [R1_TRAP run sheet](RUNSHEET_R1_TRAP.md) (superseded as the first run) |
| Follow the full-stack process, steps 0–19 | [Traveler](TRAVELER.md), then the [process pages](process/01_FOUNDATION.md) |
| Check pads, marks and die layout | [Layout](LAYOUT.md) |
| Compare stacks and temperature limits | [Stack and thermal budget](STACK.md) |
| Plan dummy wafers and tool checks | [Qualification](QUALIFICATION.md) |
| Prepare exposures | [Mask list](mask_list.md) |
| Record in-process measurements | [Process checks](process_checks.md) |
| Test finished devices | [Test plan](test_plan.md) |
| Deciding an open design choice | [Open decisions](OPEN_DECISIONS.md) and the decision briefs ([E1 vs E2](briefs/E1_vs_E2.md), [readout tilt](briefs/readout_tilt.md), [pad pitch](briefs/pad_pitch.md), [carrier and spacer](briefs/carrier_and_spacer.md), [mirror](briefs/mirror_raised_vs_inlaid.md)) |
| Setting up a test bench or asking the lab what it has | [Test setup](tests/00_SETUP.md) |
| Asking whether a simpler test would do | [Simpler testing](tests/05_SIMPLER_TESTING.md) |
| New to the labels | [Glossary](../GLOSSARY.md) |

[Layout](LAYOUT.md), [mask list](mask_list.md), [qualification](QUALIFICATION.md), [process checks](process_checks.md) and [test plan](test_plan.md) were rewritten for v4 on 2026-11-09 (DESIGN_LOG step 36).

## Project progress

| Area | Progress | Next requirement |
|---|---|---|
| Trap layout (v4) | `trap_die_v4_A30`, `_B60` and `_NODET`; 36 signal pads at 360 µm pitch (team adoption pending); mirror ground via at (−2140, 130) µm; A30, B60 and NODET pass `check_chip.py` (DESIGN_LOG step 29) | Team adoption of the pad pitch |
| Trap simulations (v4) | 04b, 12 and 13 rerun on v4; 09c optics and 10b RF pickup done for v4; pad-pitch check (16) done; collection at the v4 heights done (`sim/15b_collection_v4.py`, step 32); transport waveform (sim 21): done, DESIGN_LOG step 40; chip RF capacitance (sim 22): done, step 41; DC-to-RF coupling (sim 23): done, step 42; RCWA of the meander (sim 24): done, step 43 | See the [simulation index](../sim/INDEX.md), "Not modelled yet" |
| Detector | v3.1 meander (130 / 200 nm) under the v4 stack; absorption 0.66 with a 160 nm cap (effective-medium model, 09c) | Reconcile generated files, masks and detector predictions |
| SNSPD-only die | `snspd_die_v4` (2026-11-12): eight A30-type detector cells, 16 Au bond pads, T3 and T11; `check_snspd_die.py` ALL CHECKS PASS | Process checks on the R1_ONE wafer |
| One-wafer run | `run_R1_ONE` (2026-11-12): nine dies in a 3 × 3 block; `check_run.py R1_ONE` ALL CHECKS PASS | Choose E1 or E2; facility confirmations |
| Fabrication | Process pages rewritten for v4; electrode Au (E1 or E2) open | Choose E1 or E2; facility confirmations; W5 and W7 [qualification](QUALIFICATION.md) |
| First run | R1_ONE chosen 2026-11-12 (one wafer for all four chips). R1_TRAP, selected 2026-11-02, is superseded | Choose E1 or E2; facility confirmations |
| Local mirror | Adopted 2026-11-08 as the v4 architecture; 100 nm Al, raised, from 2026-11-12 (was inlaid); implemented in the v4 GDS | Electrode Au choice; no mirror probe opening on the trap dies (none planned; the mirror is measured on the test dies) |

## Reading in Obsidian

Read in this order:
1. This page, for the v4 overview.
2. The [traveler](TRAVELER.md), the index of steps 0–19.
3. The process pages in order: [01 foundation](process/01_FOUNDATION.md), [02 detector](process/02_DETECTOR.md), [03 electrodes](process/03_ELECTRODES.md), [04 packaging](process/04_PACKAGING.md).
4. For the first run, the [R1_TRAP sheet](RUNSHEET_R1_TRAP.md) and the [layer stack](STACK.md).

Relative Markdown links connect notes and individual process steps. Each recipe stage links to the next.

## Status labels and sources

- **Current layout:** implemented in the working generator; qualification is a separate status.
- **Selected:** already recorded as the team's choice. **Open:** still needs a decision or check. **Proposed:** an alternative to the adopted process.
- **[verify]:** not checked on the tool or against the source. **[team calc]:** calculated for this project. **[inference]:** reasoning rather than data.

Recipe shorthand: JoVE = Hong 2017; PTB = Bautista-Salvador 2019 and thesis 2015; Sussex = Siegele-Brown 2022; Todaro = Todaro 2021 and supplement; Hampel = Hampel 2023. See [references](../references_design.bib), [literature report](../research/reports/Trap%20integrated%20SNSPD%20design.md) and [design log](../DESIGN_LOG.md). “Dietl 2025” is arXiv:2505.21284; reading pointers are in the [Dietl note](../research/research_notes/Test%20setup%202026-11/T1_dietl_2025.md).
