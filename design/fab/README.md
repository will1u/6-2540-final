> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Fabrication overview

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!note] v4 is the adopted process; the electrode Au is still open
> The adopted architecture is the v4 local mirror: Au electrodes on a thin SiO₂ stack over high-resistivity Si, with an Al mirror only under the detector and its leads. There is no 10 µm SiO₂ (D2) and no ITO ([decisions](../../notes/decisions.md), 2026-11-08). The electrode Au is open: **E1** (Ti/Au lift-off, 0.35 µm) or **E2** (6 µm plated Au). The process pages give both branches. Do not fabricate a branch until the team chooses one.

The first run is **R1_TRAP**: 6 NODET and 2 TEST_TRAP dies, trap only, with no Al and no detector. **R1_FULL** adds 2 A30 and 2 B60 detector dies, plus 2 NODET and 2 TEST dies, on the same v4 stack.

> [!important] Current readiness
> The v4 generator (`gds/make_chip.py`) implements the local-mirror stack. A30 and NODET pass `check_chip.py`. The detector generators use the v3.1 meander, and some recipe estimates still describe the earlier v3 detector. The v4 test dies are drawn and checked (2026-11-09). Reconcile the detector files before R1_FULL export: see [the reconciliation checklist](OPEN_DECISIONS.md#detector-documents-and-generated-layouts). The process still needs witness-wafer qualification and facility confirmation.

## Start with your task

| I want to… | Open |
|---|---|
| Compare runs, die sizes and process options | [Variants](VARIANTS.md) |
| See the adopted architecture | [Local mirror (adopted v4)](variants/LOCAL_MIRROR.md) |
| See undecided choices and run requirements | [Open decisions](OPEN_DECISIONS.md) |
| Prepare the first trap-only run | [R1_TRAP run sheet](RUNSHEET_R1_TRAP.md) |
| Follow the full-stack process, steps 0–19 | [Traveler](TRAVELER.md), then the [process pages](process/01_FOUNDATION.md) |
| Check pads, marks and die layout | [Layout](LAYOUT.md) |
| Compare stacks and temperature limits | [Stack and thermal budget](STACK.md) |
| Plan dummy wafers and tool checks | [Qualification](QUALIFICATION.md) |
| Prepare exposures | [Mask list](mask_list.md) |
| Record in-process measurements | [Process checks](process_checks.md) |
| Test finished devices | [Test plan](test_plan.md) |

[Layout](LAYOUT.md), [mask list](mask_list.md), [qualification](QUALIFICATION.md), [process checks](process_checks.md) and [test plan](test_plan.md) are not rewritten for v4 in this pass. Check them against the v4 files before use.

## Project progress

| Area | Progress | Next requirement |
|---|---|---|
| Trap layout (v4) | `trap_die_v4_A30`, `_B60` and `_NODET`; 36 signal pads at 360 µm pitch (team adoption pending); mirror ground via at (−2140, 130) µm; A30 and NODET pass `check_chip.py` | Record the B60 check result [verify]; team adoption of the pad pitch |
| Trap simulations (v4) | 04b, 12 and 13 rerun on v4; 09c optics and 10b RF pickup done for v4; pad-pitch check (16) done | Collection at the v4 heights: `sim/15b_collection_v4.py` exists; rerun 15 still to be checked |
| Detector | v3.1 meander (130 / 200 nm) under the v4 stack; absorption 0.66 with a 160 nm cap (effective-medium model, 09c) | Reconcile generated files, masks and detector predictions |
| Fabrication | Process pages rewritten for v4; electrode Au (E1 or E2) open | Choose E1 or E2; facility confirmations; W5, W7 and W8 (inlaid mirror) [qualification](QUALIFICATION.md) |
| First run | R1_TRAP selected on 2026-11-02; on the no-Al stack since 2026-11-08 | Choose E1 or E2; finish its qualification checklist |
| Local mirror | Adopted 2026-11-08 as the v4 architecture; implemented in the v4 GDS | Electrode Au choice; no mirror probe opening on the trap dies (none planned; the mirror is measured on the test dies) |

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

Recipe shorthand: JoVE = Hong 2017; PTB = Bautista-Salvador 2019 and thesis 2015; Sussex = Siegele-Brown 2022; Todaro = Todaro 2021 and supplement; Hampel = Hampel 2023. See [references](../references_design.bib), [literature report](../research/reports/Trap%20integrated%20SNSPD%20design.md) and [design log](../DESIGN_LOG.md). The unresolved “Dietl 2025” attribution is flagged in [Open decisions](OPEN_DECISIONS.md#source-and-model-checks).
