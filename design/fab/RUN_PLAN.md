> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Run sequence and die maps

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

The work is organised as a series of short, cheap runs with the layout updated between them, not as one production wafer. Each run is a full 100 mm wafer with only a central block written (`gds/make_run.py`, [mask list](mask_list.md)). The MLA is maskless, so changing the GDS between runs costs nothing.

| Run | Layout | Process | Main questions | Feeds the next run |
|---|---|---|---|---|
| **0: short loops** | pieces or spare wafers | [qualification loops](QUALIFICATION.md) | NbN on the real stack; HSQ dose; D2 stress and the full D2-to-dicing rehearsal (W3); plating | Recipes, dose, etch times |
| **1a: trap only** (`run_R1_TRAP`, [run sheet](RUNSHEET_R1_TRAP.md)) | 6 NODET + 2 trap-only test dies (T1, T2, T6) | Steps 0–3, 9, 11–19. Skip 4–8 and the L20/L22 jobs. No EBL. | Plating, gap etch, leakage and breakdown (`test_plan.md` a1–a5), trapping, transport, heating rate | Trap process frozen; NODET becomes the reference die |
| **1b: full stack** (`run_R1_FULL`) | 2 A30, 2 B60, 2 NODET, 2 TEST | All steps | T8 dose array → nominal dose; T3/T4/T4b Tc, Isw and efficiency; SNSPD with RF on; ion over the window compared with NODET | Dose, spacer and cap thicknesses, die mix for run 2 |
| **2+** | edit `RUNS` in `make_run.py` | All steps | Whatever 1a/1b leave open, plus any [simplifications](../SIMPLIFICATIONS.md) variant worth trying | – |

**The team chose 1a first (2026-11-02).** [R1_TRAP run sheet](RUNSHEET_R1_TRAP.md) is the streamlined sheet for it.

## Layout files

| Layout | Map | Preview |
|---|---|---|
| [R1_TRAP](../gds/run_R1_TRAP.gds) | [Die IDs/coordinates](../gds/run_R1_TRAP_map.csv) | [Placement](../gds/run_R1_TRAP_map.png) |
| [R1_FULL](../gds/run_R1_FULL.gds) | [Die IDs/coordinates](../gds/run_R1_FULL_map.csv) | [Placement](../gds/run_R1_FULL_map.png) |
| [Full wafer](../gds/wafer_v3.gds) | [Die IDs/coordinates](../gds/wafer_v3_map.csv) | [Placement](../gds/wafer_v3_map.png) |

Each R1 block has eight dies in 20.2 × 33.1 mm. Columns share row heights for straight saw cuts. The full-wafer reference has 56 dies, not the historical v2 count of 184. Use one run map for every exposure, test record and dicing operation.

Before booking, complete [facility confirmations](QUALIFICATION.md#facility-confirmations). Before R1_FULL, complete [detector reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts).
