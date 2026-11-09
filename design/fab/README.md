> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Fabrication overview

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!warning] Architecture changed to v4 (2026-11-08)
> The team chose the local-mirror architecture (no die-wide Al, no 10 µm D2), leads in a slot along the centre DC, A30 and B60 detector dies (B60 briefly dropped, then kept), and the same no-Al stack for R1_TRAP ([decisions](../../notes/decisions.md); DESIGN_LOG step 25). The GDS is now v4 (`gds/trap_die_v4_*`). **This page still describes the v3 baseline process.** It must be rewritten before any run; the rewrite waits on the electrode Au choice (E1 lift-off vs E2 plated). Do not fabricate from it.

The first run is **R1_TRAP**, a plain trap without a detector. R1_FULL adds A30 and B60 detector dies. The local-mirror architecture is adopted and implemented in the v4 GDS; the process pages below still describe the v3 baseline (see the banner).

> [!important] Current readiness
> Generated v3 layouts have recorded passing checks through the ground-via revision. The process still needs witness-wafer qualification and facility confirmation. **The detector generators now specify v3.1 geometry, while several recipe estimates still describe the earlier v3 detector.** See [the reconciliation checklist](OPEN_DECISIONS.md#detector-documents-and-generated-layouts).

## Start with your task

| I want to… | Open |
|---|---|
| Compare runs, die sizes and process options | [Variants](VARIANTS.md) |
| See undecided choices and run requirements | [Open decisions](OPEN_DECISIONS.md) |
| Prepare the first trap-only run | [R1_TRAP run sheet](RUNSHEET_R1_TRAP.md) |
| Follow the full-stack process | [Traveler](TRAVELER.md) |
| Check pads, marks and die layout | [Layout](LAYOUT.md) |
| Compare stacks and temperature limits | [Stack and thermal budget](STACK.md) |
| Plan dummy wafers and tool checks | [Qualification](QUALIFICATION.md) |
| Prepare exposures | [Mask list](mask_list.md) |
| Record in-process measurements | [Process checks](process_checks.md) |
| Test finished devices | [Test plan](test_plan.md) |

## Project progress

| Area | Progress | Next requirement |
|---|---|---|
| Trap layout | 10 × 10 mm dies; 36 signal electrodes; eight Au-fill-to-Al vias; passing checks recorded in [step 22](../DESIGN_LOG.md) | Qualify via contact and sidewall coverage on W3 |
| Trap simulations | v3 zone/transport results, staircase and pad checks recorded | Choose a readout radial tilt that fits the DAC range |
| Detector | Current generators use 130/200 nm wires, rounded turns and an enlarged footprint; T9 compares geometries | Reconcile generated files, masks and detector predictions |
| Fabrication | Recipes and short loops planned | D2 stress, etch, plating and bonding qualification; facility access |
| First run | R1_TRAP selected on 2026-11-02 | Finish its qualification checklist |
| Local mirror | Process comparison written; no GDS | Decide whether to pursue it, then resolve routing and Au thickness |

## Reading in Obsidian

Start here within the project vault. Relative Markdown links connect notes and individual process steps. Each recipe stage links to the next. The original traveler, R1_TRAP sheet and test-plan filenames remain entry points.

## Status labels and sources

- **Current layout:** implemented in the working generator; qualification is a separate status.
- **Selected:** already recorded as the team's choice. **Open:** still needs a decision or check. **Proposed:** an alternative to the baseline.
- **[verify]:** not checked on the tool or against the source. **[team calc]:** calculated for this project. **[inference]:** reasoning rather than data.

Recipe shorthand: JoVE = Hong 2017; PTB = Bautista-Salvador 2019 and thesis 2015; Sussex = Siegele-Brown 2022; Todaro = Todaro 2021 and supplement; Hampel = Hampel 2023. See [references](../references_design.bib), [literature report](../research/reports/Trap%20integrated%20SNSPD%20design.md) and [design log](../DESIGN_LOG.md). The unresolved “Dietl 2025” attribution is flagged in [Open decisions](OPEN_DECISIONS.md#source-and-model-checks).
