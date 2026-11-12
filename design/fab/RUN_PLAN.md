> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09. Rewritten around the one-wafer run R1_ONE 2026-11-12 (team decision, [notes/decisions.md](../../notes/decisions.md)).

# Run sequence and die maps

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

The next run is **R1_ONE**: one 100 mm wafer with one 3 × 3 block of nine dies (team decision 2026-11-12, [notes/decisions.md](../../notes/decisions.md)). Each run is still a full 100 mm wafer with only a central block written (`gds/make_run.py`, [mask list](mask_list.md)). The MLA is maskless, so changing the GDS between runs costs nothing.

| Run | Layout | Process | Main questions | Feeds the next run |
|---|---|---|---|---|
| **R1_ONE (next run)** | `run_R1_ONE`: 4 A30, 1 B60 (spare), 2 SNSPD-only dies, 2 NODET; one wafer, 9 dies | Full v4 flow in five lithography layers (1 + 10, 22, 20, 40, 50); electrode branch E1 or E2, wafer-wide | Does the full v4 stack work on one wafer: the SNSPD cells (SNSPD-only dies), the trap with the detector (A30), the trap alone (NODET). See [which chip serves which test](#which-chip-serves-which-test) | Dose, spacer and cap calibration; die choice for the next run |
| **R1_ONE, second wafer** (optional, not decided by the team) | `run_R1_ONE.gds`, layer 50 only | Steps 0–2, 12–15 (E1 or E2), 17–19 | Electrode step on a real wafer; wire bonding; trap-only backup if the shared wafer fails | Electrode and bonding recipe frozen. See [optional second wafer](#optional-second-wafer) |
| **1a: trap only** (`run_R1_TRAP`, [run sheet](RUNSHEET_R1_TRAP.md)). Superseded 2026-11-12 by R1_ONE | 6 NODET + 2 TEST_TRAP (20.2 × 33.1 mm block) | Steps 0–2, 12–15 (E1 or E2), 17–19. No Al, no NbN, no EBL | Electrode quality, isolation, bonding; trapping, transport, heating rate | Not run. The run sheet now describes the optional second wafer |
| **1b: full stack** (`run_R1_FULL`). Superseded 2026-11-12 by R1_ONE | 2 A30, 2 B60, 2 NODET, 2 TEST (20.2 × 33.1 mm block) | Full v4 stack, steps 0–19 | T8 dose array; T3/T4/T4b Tc, Isw and efficiency; SNSPD with RF on | Not run. Its questions moved to R1_ONE |
| **0: short loops** | pieces or spare wafers | [qualification loops](QUALIFICATION.md) | E1 lift-off over 5 µm gaps and wedge bonding on evaporated Au; E2 plating current (W5); W7 bond-and-leak; NbN on the real stack and HSQ dose (W1, W2) | Electrode branch chosen; recipes and doses |
| **2+** | edit `RUNS` in `make_run.py` | All steps | Whatever R1_ONE leaves open, plus any [simplifications](../SIMPLIFICATIONS.md) variant worth trying | – |

**The team chose 1a first (2026-11-02). On 2026-11-12 it chose one wafer for all four chips (R1_ONE), which replaces 1a and 1b.** The [R1_TRAP run sheet](RUNSHEET_R1_TRAP.md) now describes only the optional second wafer.

## Which chip serves which test

The team's four tests and the die for each. Die IDs are from [run_R1_ONE_map.csv](../gds/run_R1_ONE_map.csv).

| Test | Where it is run | Die | Dies in R1_ONE |
|---|---|---|---|
| 1. The SNSPD alone | SNSPD test setup | SNSPD-only die (`snspd_die_v4`, 8 detector cells D1–D8) | R1_ONE-02, R1_ONE-08 |
| 2. The SNSPD with trap RF applied | SNSPD test setup | A30 die (SNSPD + trap) | R1_ONE-01, -03, -05, -07 |
| 3. The trap alone | Trap chamber | NODET die (trap, no detector) | R1_ONE-04, R1_ONE-06 |
| 4. The SNSPD in the trap chamber | Trap chamber | A30 die (SNSPD + trap) | R1_ONE-01, -03, -05, -07 |

Spares:
- **R1_ONE-09 (B60) is the spare.** The team put A30 on the chips it needs and kept B60 as a spare position (decision 2026-11-12).
- The team has not yet assigned individual A30 or NODET dies to a test [verify].

## Die map

Laid out as the wafer, top row first. Die centres in µm, in the wafer frame.

| | Left column (x = −10 200) | Middle column (x = 0) | Right column (x = +10 200) |
|---|---|---|---|
| **Top row** (y = +10 200) | R1_ONE-03, A30 | R1_ONE-06, NODET | R1_ONE-09, B60 (spare) |
| **Middle row** (y = 0) | R1_ONE-02, SNSPD-only | R1_ONE-05, A30 (wafer centre) | R1_ONE-08, SNSPD-only |
| **Bottom row** (y = −10 200) | R1_ONE-01, A30 | R1_ONE-04, NODET | R1_ONE-07, A30 |

- Die size: 10 × 10 mm, all nine dies.
- Pitch: 10.2 mm both ways (200 µm streets).
- Block: 30.4 × 30.4 mm, at the wafer centre. Largest die-corner radius 21.5 mm.
- Saw cuts: at x and y = −15 300, −5 100, +5 100 and +15 300 µm.
- Die IDs and centres: [run_R1_ONE_map.csv](../gds/run_R1_ONE_map.csv). Placement image: [run_R1_ONE_map.png](../gds/run_R1_ONE_map.png).
- Dies carry no label on a fabricated layer. Identify them by this map.

## Can all dies share one wafer?

Verdict: one wafer works. No step that one die needs harms a die that does not need it [inference, from the step analysis below; not yet checked on a tool]. This answers the earlier question of whether NODET dies receive steps 4–8: on the shared wafer they do, as blanket films.

| Step | SNSPD + trap dies (A30, B60, SNSPD-only) | Trap-only die (NODET), same wafer | Conflict? |
|---|---|---|---|
| 0, 2: clean; base SiO₂ | Base SiO₂ 1.0 µm nominal (thermal, or as supplied) | Same film | No |
| 1 + 3: Al mirror and marks (layers 10 and 1, one exposure, lift-off) | 100 nm raised Al mirror under the detector and its leads; marks on every die | Marks only (layer 1); no Al | No. The Al is drawn only where drawn |
| 4: SiO₂ spacer, 238 nm | Blanket | Blanket | No |
| 5: NbN, 7 nm | Blanket; patterned in step 7 | Blanket; removed by the step-7 etch | No, if the etch clears it [verify: CF₄ selectivity of NbN to SiO₂ is not in the sources] |
| 6: Ti 5 nm / Au 50 nm (layer 22) | Contacts and e-beam crosses | None (no layer 22 on NODET) | No |
| 7: e-beam HSQ (layer 20) and CF₄ etch | HSQ on the NbN wires only; CF₄ etch of the rest | No HSQ; CF₄ etch removes the NbN blanket | No, [verify] the etch stops on the spacer |
| 8: SiO₂ cap, 110 nm | Blanket; 160 ± 10 nm over the wires with the HSQ | Blanket, 110 nm | No |
| 11: openings (layer 40) | Contact openings (110 nm of SiO₂, landing on the Au of the contact pad); mirror ground via (348 nm, landing on Al) | None: no openings on NODET | No |
| 12–15: electrode Au (layer 50, E1 or E2) | Au on the cap | Au on base SiO₂ + 238 nm spacer + 110 nm cap | No. One step for all dies |
| 17–19: test, dice, package | As drawn | As drawn | No |

What could still force a second wafer:
1. Trying both E1 and E2. The electrode branch is a wafer-wide choice.
2. Tool limits [verify]: the NbN sputter tool and the e-beam holder must take a 100 mm wafer. The e-beam, the CF₄ etcher and the PECVD must accept a wafer that already carries Au from step 6.
3. Schedule: the trap-only die needs only the electrode module but waits for every detector step.

New checks because of the shared wafer:
- After the NbN etch (step 7), an open field must read open circuit between two probes.
- On a finished trap die, pad-to-pad leakage between neighbouring electrodes must be checked.

Still open on the mask list:
- The e-beam crosses on the detector dies sit about 760 µm from the meander, outside one write field [verify the alignment procedure].
- The contact openings have 1 µm of drawn margin, so the layer-40 overlay to layer 22 must be ≤ 1 µm.
- Dies carry no label on a fabricated layer. Identify them by the run map.

## Optional second wafer

Recommended, not yet decided by the team.

- Exposes **only layer 50** from the same file, `run_R1_ONE.gds`. No new layout.
- Purpose: the trap-only backup, and the trial of the electrode step and of wire bonding.
- Its dies sit on base SiO₂ only (no spacer, NbN or cap), so the Au lies on a different stack from the NODET die of the shared wafer.
- Run sheet: [RUNSHEET_R1_TRAP.md](RUNSHEET_R1_TRAP.md), which carries a banner with the two differences from the old sheet.

## What the run needs first

| Needs first (R1_ONE) | Where it is set out |
|---|---|
| **Electrode branch chosen (E1 or E2).** Wafer-wide. Plated area for E2: 8.27 cm² for R1_ONE [team calc from `run_R1_ONE.gds`; not yet in [measured table](../gds/measured_v4.md)] | [Open decisions](OPEN_DECISIONS.md#before-any-v4-run) |
| **The wafers.** High-resistivity float-zone Si, ρ > 20 kΩ·cm [verify on the wafer box]. Base SiO₂ 1.0 µm nominal, 0.5–2.0 µm accepted as supplied. Whether SiO₂ is already on the wafers is not known yet. If they are bare: thermal oxidation, or a PECVD SiO₂ base (Hampel 2023 used 150 nm, Todaro 2021 134 nm) | [Fab overview](README.md) and [Open decisions](OPEN_DECISIONS.md#before-any-v4-run) |
| **Facility, tools that accept a wafer carrying Au after step 6** (e-beam, CF₄ etcher, PECVD) [verify] | [Facility confirmations](QUALIFICATION.md#facility-confirmations) |
| **Facility, NbN sputter access and wafer size** (100 mm) [verify] | [Facility confirmations](QUALIFICATION.md#facility-confirmations) |
| **Facility, e-beam holder size** [verify] | [Facility confirmations](QUALIFICATION.md#facility-confirmations) |
| **Facility, evaporator for Al, Ti and Au** [verify] | [Facility confirmations](QUALIFICATION.md#facility-confirmations) |
| **Facility, plating tank and minimum area, if E2** | [Facility confirmations](QUALIFICATION.md#facility-confirmations) |
| **Co-loaded pieces instead of separate witness wafers.** Qualification pieces ride on the R1_ONE wafer where the process allows | [Qualification](QUALIFICATION.md) |
| **Carrier and pad pitch, before packaging.** Pad pitch 360 µm is generated; team adoption pending | [Open decisions](OPEN_DECISIONS.md#design-choices) |

## Layout files

| Layout | Map | Preview |
|---|---|---|
| [R1_ONE](../gds/run_R1_ONE.gds) (next run) | [Die IDs/coordinates](../gds/run_R1_ONE_map.csv) | [Placement](../gds/run_R1_ONE_map.png) |
| [snspd_die_v4](../gds/snspd_die_v4.gds) (SNSPD-only die, 10 × 10 mm) | [Bond pads](../gds/snspd_die_v4_pads.csv) | [Preview](../gds/snspd_die_v4_preview.png) |
| [R1_TRAP](../gds/run_R1_TRAP.gds). Superseded 2026-11-12 by R1_ONE | [Die IDs/coordinates](../gds/run_R1_TRAP_map.csv) | [Placement](../gds/run_R1_TRAP_map.png) |
| [R1_FULL](../gds/run_R1_FULL.gds). Superseded 2026-11-12 by R1_ONE | [Die IDs/coordinates](../gds/run_R1_FULL_map.csv) | [Placement](../gds/run_R1_FULL_map.png) |
| [Full wafer, v4](../gds/wafer_v4.gds) (reference) | [Die IDs/coordinates](../gds/wafer_v4_map.csv) | [Placement](../gds/wafer_v4_map.png) |

The v3 runs and wafer are archived in [gds/archive_v3_baseline/](../gds/archive_v3_baseline/). Do not use them.

R1_ONE is nine dies in a 30.4 × 30.4 mm block (3 × 3, all 10 × 10 mm). The superseded R1_TRAP and R1_FULL blocks were 20.2 × 33.1 mm with eight dies each.

Before exposing, complete [facility confirmations](QUALIFICATION.md#facility-confirmations). Check the [detector reconciliation checklist](OPEN_DECISIONS.md#detector-documents-and-generated-layouts) against the R1_ONE files [verify: the checklist was written for R1_FULL]. Use one run map for every exposure, test record and dicing operation.
