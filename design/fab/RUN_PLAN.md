> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09.

# Run sequence and die maps

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

The work is organised as a series of short, cheap runs with the layout updated between them, not as one production wafer. Each run is a full 100 mm wafer with only a central block written (`gds/make_run.py`, [mask list](mask_list.md)). The MLA is maskless, so changing the GDS between runs costs nothing.

| Run | Layout | Process | Main questions | Feeds the next run |
|---|---|---|---|---|
| **0: short loops** | pieces or spare wafers | [qualification loops](QUALIFICATION.md) | E1 lift-off over 5 µm gaps and wedge bonding on evaporated Au; E2 plating current (W5); W7 bond-and-leak; NbN on the real stack and HSQ dose (W1, W2) | Electrode branch chosen; recipes and doses |
| **1a: trap only** (`run_R1_TRAP`, [run sheet](RUNSHEET_R1_TRAP.md)) | 6 NODET + 2 TEST_TRAP | Steps 0–2, 12–15 (branch E1 or E2), 17–19. Skip 3–11 and 16a/16. No Al, no NbN, no EBL | Electrode quality (lift-off or plating), isolation, bonding; trapping, transport, heating rate | Trap process frozen for the chosen branch; NODET becomes the reference die |
| **1b: full stack** (`run_R1_FULL`) | 2 A30, 2 B60, 2 NODET, 2 TEST | Full v4 stack, steps 0–19 | T8 dose array → nominal dose; T3/T4/T4b Tc, Isw and efficiency; SNSPD with RF on; ion over the window compared with NODET | Dose, spacer and cap thicknesses, die mix for run 2 |
| **2+** | edit `RUNS` in `make_run.py` | All steps | Whatever 1a/1b leave open, plus any [simplifications](../SIMPLIFICATIONS.md) variant worth trying | – |

**The team chose 1a first (2026-11-02).** [R1_TRAP run sheet](RUNSHEET_R1_TRAP.md) is the streamlined sheet for it.

## What each run needs first

| Run | Needs first | Where it is set out |
|---|---|---|
| **1a: R1_TRAP** | Electrode branch chosen (E1 or E2) | [Open decisions](OPEN_DECISIONS.md#before-any-v4-run) |
| | Facility: Au-compatible tools and holders; plating tank and minimum area (E2); evaporator for Au and Ti (E1); training order | [Facility confirmations](QUALIFICATION.md#facility-confirmations) |
| | W7 bond-and-leak on the chosen branch; W5 plating (E2) or the E1 lift-off test | [Run sheet, section 2](RUNSHEET_R1_TRAP.md) |
| | v4 TEST_TRAP die and run GDS: done 2026-11-09 (`make_run.py` writes `test_die_v4_TRAP`) | [Run sheet, open item 3](RUNSHEET_R1_TRAP.md#6-open-before-the-run) |
| | Si ordered with ρ > 20 kΩ·cm; RF resonator Q measured with a die mounted | [Open decisions](OPEN_DECISIONS.md#before-any-v4-run) |
| | Plated area for v4 layer 50 (E2): done, 5.917 cm² | [Measured table](../gds/measured_v4.md) |
| | Pad pitch (360 µm) adopted or changed, and carrier chosen, before packaging | [Open decisions](OPEN_DECISIONS.md#design-choices) |
| **1b: R1_FULL** | Detector reconciliation: generated files, the 130 / 200 nm recipe, T9, and L20 / L22 / L40 / L50 areas and EBL time | [Checklist](OPEN_DECISIONS.md#detector-documents-and-generated-layouts) |
| | NbN recipe and sputter access; W1-a and W1-b | [Open decisions](OPEN_DECISIONS.md#before-r1_full) |
| | W2: HSQ dose, develop and etch on the actual EBL tool; L22-to-L50 overlay | [Open decisions](OPEN_DECISIONS.md#before-r1_full) |
| | Cap and spacer etch (about 0.40 µm) calibration; Au-to-Al contact at the mirror via with and without Ar pre-clean; AJA substrate RF etch | [Open decisions](OPEN_DECISIONS.md#before-r1_full) |
| | v4 test dies: T2v, T10, T11 and T12 drawn and checked 2026-11-09. No mirror probe opening on the trap dies (none planned) | [Open decisions](OPEN_DECISIONS.md#before-any-v4-run) |
| | Switching current at operating temperature with RF off and on; charging drift against NODET | [Open decisions](OPEN_DECISIONS.md#before-r1_full) |
| | Collection at the v4 heights: `sim/15b_collection_v4.py` exists; rerun of sim 15 still to be checked | [Open decisions](OPEN_DECISIONS.md#before-any-v4-run) |
| **2+** | Whatever 1a and 1b leave open; edit `RUNS` in `make_run.py`. Every column must stack the same die heights so the saw cuts run straight (asserted in the script) | [Open decisions](OPEN_DECISIONS.md#before-r1_full) |

## Layout files

| Layout | Map | Preview |
|---|---|---|
| [R1_TRAP](../gds/run_R1_TRAP.gds) | [Die IDs/coordinates](../gds/run_R1_TRAP_map.csv) | [Placement](../gds/run_R1_TRAP_map.png) |
| [R1_FULL](../gds/run_R1_FULL.gds) | [Die IDs/coordinates](../gds/run_R1_FULL_map.csv) | [Placement](../gds/run_R1_FULL_map.png) |
| [Full wafer, v4](../gds/wafer_v4.gds) | [Die IDs/coordinates](../gds/wafer_v4_map.csv) | [Placement](../gds/wafer_v4_map.png) |

The v3 runs and wafer are archived in [gds/archive_v3_baseline/](../gds/archive_v3_baseline/). Do not use them.

Each R1 block has eight dies in 20.2 × 33.1 mm. Columns share row heights for straight saw cuts. The full-wafer reference has 56 dies, not the historical v2 count of 184. Use one run map for every exposure, test record and dicing operation.

Before booking, complete [facility confirmations](QUALIFICATION.md#facility-confirmations). Before R1_FULL, complete [detector reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts).
