> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Fabrication variants

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

There are four separate choices: **run**, **die type**, **detector revision**, and **process architecture**. A30 and B60 are detector-window sizes within the same architecture; R1_TRAP and R1_FULL are wafer runs.

## Runs

| Run | Die mix | Process | Status |
|---|---|---|---|
| R1_TRAP / 1a | 6 NODET + 2 TEST_TRAP | Steps 0–3, 9, 11–19, including 16a; five MLA jobs, no EBL | **Selected first**; [run sheet](RUNSHEET_R1_TRAP.md) |
| R1_FULL / 1b | 2 A30 + 2 B60 + 2 NODET + 2 TEST | Full stack; adds detector deposition and L20/L22 jobs | Planned after trap-process qualification |
| Full-wafer reference | 25 A30 + 14 B60 + 17 TEST | Same architecture, more dies | Reference; not the first run |

Both R1 blocks are 20.2 × 33.1 mm at the centre of a 100 mm wafer. See [run plan and maps](RUN_PLAN.md).

## Die types

| Type | Au window, axial × radial | Detector | Purpose |
|---|---|---|---|
| A30 | 30 × 30 µm | NbN below cap + 10 µm D2 SiO₂ | Primary detector size |
| B60 | 60 × 30 µm | Same stack, longer meander | Larger-aperture comparison |
| NODET | None; solid centre DC | None | Trap-only run and full-stack reference |
| TEST | Not a trap | T1–T4b, T6, T8; current generator adds T9 | Process, dose and geometry comparisons |
| TEST_TRAP | Not a trap | No NbN; T1, T2, T6 only | Trap-process qualification |
| UNIFORM | None | Simulation reference only | Equal-depth DC segments, no leads; **never fabricate** |

**NODET on R1_FULL receives blanket spacer/cap depositions.** NODET on R1_TRAP skips them, so D2 goes directly on Al. Die type alone does not determine the deposited stack.

## A30 and B60 operating differences

Recorded v3 trap-model results from design-log steps 17 and 19; these describe the unchanged Au windows, not a cold-detector measurement.

| Quantity | A30 | B60 |
|---|---|---|
| Bare-SiO₂ recess correction [team calc, upper bound] | −1.38 µm | −2.50 µm |
| Readout ion height with that correction | ~48.7 µm | ~47.6 µm |
| Maximum DC at 10° readout tilt | 13.2 V, beyond ±10 V | 15.2 V, beyond ±10 V |
| Maximum DC with zero readout tilt | 6.6 V | 3.4 V |
| Largest transport change per 10 µm step | ~1.6 V | Up to ~4.5 V near window |

## Detector revision

GDS filenames still contain `v3`; the current generators call their detector geometry **v3.1**. Record the generator revision with the filename.

| Item | Earlier v3 recipe | Current v3.1 generator |
|---|---|---|
| NbN film | 7 nm | 7 nm recipe retained |
| Width / pitch | 100 / 200 nm; 50 % fill | 130 / 200 nm; 65 % fill |
| A30 line region | 30 × 30 µm, 150 lines | 36 × 32 µm, 160 lines |
| B60 line region | 60 × 30 µm, 150 lines | 69 × 32 µm, 160 lines |
| Turns / tabs | Square / abrupt | Rounded slots in end blocks / tapered |
| Au windows | 30 × 30 or 60 × 30 µm | Unchanged |
| Test comparison | T8 dose array | T8 plus T9 geometry array |

Turns and tabs extend beyond the line region. Sources: [trap generator](../gds/make_chip.py), [test generator](../gds/make_test_die.py), [shared geometry](../gds/snspd_geom.py). The [geometry audit](../research/reports/SNSPD%20geometry%20audit.md) explains the changes but describes the older drawing in its opening audit. **Exposure areas and detector predictions need reconciliation**; see [the checklist](OPEN_DECISIONS.md#detector-documents-and-generated-layouts).

## Process architecture

| Architecture | Al beneath RF | SiO₂ above detector | Au electrodes | Status |
|---|---|---|---|---|
| **Baseline** | Die-wide plane | Cap + 10 µm D2 | 6 µm plated | Implemented architecture; [traveler](TRAVELER.md) |
| **Local mirror E1** | None; Al local to detector/leads | Cap only | ~0.35 µm lift-off | Proposed; no GDS |
| **Local mirror E2** | None; Al local to detector/leads | Cap only | 6 µm plated | Proposed; no GDS |

**E1 removes plating as well as D2. E2 retains plating.** Both remove the deep D2 gap etch, and need a lead-routing decision and new stack simulations. See [local-mirror proposal](variants/LOCAL_MIRROR.md).

## Other alternatives and history

[Sapphire and fused silica](variants/SUBSTRATES.md) are substrate alternatives. [Simplifications](../SIMPLIFICATIONS.md) contains historical v2 candidate studies, labelled accordingly. The v1 corner layout and v2 narrow, two-ITO layout are archived.
