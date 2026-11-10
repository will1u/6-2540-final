> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Fabrication variants

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!note] The local mirror is the process; the v3 baseline is superseded
> The v4 local-mirror architecture is the fabrication process. The die-wide Al ground plane under 10 µm of SiO₂ (D2) is the superseded v3 baseline. Its GDS is archived in [gds/archive_v3_baseline/](../gds/archive_v3_baseline/), and it is not for fabrication. The substrate alternatives remain separate variants ([SUBSTRATES](variants/SUBSTRATES.md)).

There are four separate choices: **run**, **die type**, **detector revision**, and **process architecture**. A30 and B60 are detector-window sizes within the v4 architecture. R1_TRAP and R1_FULL are wafer runs.

## Runs

| Run | Die mix | Process | Status |
|---|---|---|---|
| R1_TRAP / 1a | 6 NODET + 2 TEST_TRAP | Steps 0–2, 12–15 (branch E1 or E2), 17–19. No Al, no NbN, no EBL | **Selected first**; [run sheet](RUNSHEET_R1_TRAP.md) |
| R1_FULL / 1b | 2 A30 + 2 B60 + 2 NODET + 2 TEST | Full v4 stack, steps 0–19; adds the Al mirror, NbN, EBL and layer 22 and 40 jobs | Planned after trap-process qualification |
| Full-wafer reference | 25 A30 + 14 B60 + 17 TEST | Same v4 architecture, more dies (`wafer_v4`) | Reference; not the first run |

Both R1 blocks are 20.2 × 33.1 mm at the centre of a 100 mm wafer. See [run plan and maps](RUN_PLAN.md).

## Die types

| Type | Au window, axial × radial | Detector | Purpose |
|---|---|---|---|
| A30 | 30 × 30 µm | NbN under the SiO₂ cap, over a 100 nm inlaid local Al mirror; no D2 | Primary detector size |
| B60 | 60 × 30 µm | Same stack, longer meander | Larger-aperture comparison |
| NODET | None; solid centre DC | None; no Al | Trap-only run (R1_TRAP) and full-stack reference |
| TEST | Not a trap | T1, T2v, T3, T4, T4b, T6, T8–T12 (v4, drawn and checked 2026-11-09) | Process, dose and geometry comparisons |
| TEST_TRAP | Not a trap | No NbN, no Al; T1 and T6 on layers 1 and 50 | Trap-process qualification |
| UNIFORM | None | Simulation reference only | Equal-depth DC segments, no leads; **never fabricate** |

NODET on R1_TRAP has no Al and no spacer, NbN or cap, so its Au sits on thermal SiO₂. Whether NODET on R1_FULL receives steps 4–8 is not stated in the sources [verify]. Die type alone does not determine the deposited stack.

The runs use the test dies `test_die_v4` and `test_die_v4_TRAP`; `make_run.py` writes the v4 TRAP die (checked 2026-11-09).

## A30 and B60 operating differences

Values from the v4 trap model (DESIGN_LOG steps 25–28) for the Au windows as drawn. The v3 values (recess −1.38 and −2.50 µm; 13.2 and 15.2 V at 10° tilt) are superseded.

| Quantity | A30 | B60 |
|---|---|---|
| Ion drop over the window (recess from the grounded floor), E2 (6 µm Au) | −1.19 µm | −2.04 µm |
| Ion drop over the window, E1 (0.35 µm Au) | ≤ −0.37 µm | ≤ −0.55 µm |
| Maximum DC at 10° readout tilt, 480 µm zones | 6.3 V | 2.2 V |
| Largest transport change per 10 µm step, centre DC held at 0 V | 1.708 V | 1.708 V |

The readout ion height is 49.98 µm before the window recess (planar model). The 10° readout tilt is still to be confirmed by the team ([open decisions](OPEN_DECISIONS.md)).

## Detector revision

v4 trap GDS files are named `trap_die_v4_*`. The current generators call their detector geometry **v3.1**. Record the generator revision with each file.

| Item | Earlier recipe | Current v3.1 generator |
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

| Architecture | Al beneath RF | Al under the detector | SiO₂ above the detector | Au electrodes | Status |
|---|---|---|---|---|---|
| **v4 local mirror** | None | Local mirror, 100 nm evaporated Al, inlaid, under the detector and its leads only | Spacer 238 nm; cap 160 ± 10 nm over the wires; no D2 | E1: 0.35 µm lift-off; E2: 6 µm plated (open) | **Adopted 2026-11-08**; mirror 100 nm inlaid from 2026-11-09; implemented in the v4 GDS; [traveler](TRAVELER.md) |
| Superseded: v3 baseline | Die-wide plane, 150 nm, inverted layer 10 | Same die-wide plane | Cap + 10 µm D2 | 6 µm plated | Superseded 2026-11-08; archived GDS only ([archive](../gds/archive_v3_baseline/)) |

The electrode Au (E1 or E2) is still open ([open decisions](OPEN_DECISIONS.md)). Both branches remove D2 and its deep gap etch. E1 has no plating; E2 keeps 6 µm plating. See the [local mirror](variants/LOCAL_MIRROR.md) page.

## Other alternatives and history

[Sapphire and fused silica](variants/SUBSTRATES.md) are substrate alternatives. [Simplifications](../SIMPLIFICATIONS.md) contains historical v2 candidate studies, labelled accordingly. The v1 corner layout, the v2 narrow two-ITO layout and the v3 baseline are archived.
