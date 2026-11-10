> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Fabrication traveler

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!note] v4 index; electrode Au still open
> This page indexes steps 0–19 of the adopted v4 local-mirror process ([decisions](../../notes/decisions.md); [local mirror](variants/LOCAL_MIRROR.md)). The team has not chosen the electrode Au: **E1** (Ti 10 nm / Au 350 nm, lift-off) or **E2** (6 µm plated Au). Steps 12–15 are written for both branches. Do not fabricate a branch until the choice is recorded ([open decisions](OPEN_DECISIONS.md)).

Step recipes are on four process pages: [01 foundation](process/01_FOUNDATION.md) (steps 0–3), [02 detector](process/02_DETECTOR.md) (4–8), [03 electrodes](process/03_ELECTRODES.md) (9–16) and [04 packaging](process/04_PACKAGING.md) (17–19). For the first run, use the [R1_TRAP sheet](RUNSHEET_R1_TRAP.md).

The v3 baseline (die-wide Al plane, 10 µm D2) is superseded. Its GDS is archived in [gds/archive_v3_baseline/](../gds/archive_v3_baseline/) and is not for fabrication.

Wafer ID: ________ Run: ________ Generator revision/date: ________ Start date: ________ Operator: ________

> [!important] Before starting
> Complete [qualification](QUALIFICATION.md) and review [open decisions](OPEN_DECISIONS.md). Current generators use v3.1 detectors; older estimates are marked in the detailed notes. This is a proposed process, not a qualified recipe.

## A. Die layout (v4) and tape-out status

- Trap dies: `gds/trap_die_v4_A30`, `_B60` and `_NODET` (10 × 10 mm). Runs use the test dies `test_die_v4` and `test_die_v4_TRAP`, drawn and checked by `gds/check_test_die.py` (ALL CHECKS PASS, 2026-11-09); `make_run.py` and `make_wafer.py` use them.
- [Layout, marks, pads and protections](LAYOUT.md), rewritten for v4 on 2026-11-09. Areas and counts: [measured table](../gds/measured_v4.md).

### A.1 Resolved in the GDS (v2, carried into v3)

[Layout protections A1–A7](LAYOUT.md#a1-resolved-in-the-gds-v2-carried-into-v3).

### A.2 Still open

[Design decisions and run requirements](OPEN_DECISIONS.md).

### A.3 R&D run plan at MIT.nano

[Run sequence and maps](RUN_PLAN.md).

## B. One-screen process summary

![v4 process flow: one composite cross-section per step, with the E1 and E2 electrode branches](figures/process_flow_v4.svg)

The figure is written by `figures/make_process_flow.py`. It is a composite schematic, not to scale.

Step 3 has sub-steps 3a–3d (resist, 100 nm SiO₂ recess, Al evaporation, lift-off). The surface is flat after step 3. Decision: team decision 2026-11-09 ([decisions](../../notes/decisions.md)). Numbers: (`sim/10c`, DESIGN_LOG step 37).

"Used in" lists the runs that use each step. R1_TRAP uses steps 0, 1, 2, 12–15, 17, 18 and 19 only. R1_FULL uses the remaining steps.

| # | Step | GDS layer | Material | Target thickness | Tool (MIT.nano name where verified in the report) | Used in |
|---|---|---|---|---|---|---|
| 0 | Wafer prep, clean | – | HR FZ Si, 100 mm, ρ > 20 kΩ·cm | 500–525 µm [verify] | Acid-Etch-General-* (piranha) | R1_TRAP, R1_FULL |
| 1 | Alignment marks | 1 | Si etch | ~1 µm deep | DirectWrite-MLA150-*; RIE-F-Samco-230iP | R1_TRAP, R1_FULL |
| 2 | Thermal SiO₂ D1, both sides | – | SiO₂ | 1.0 µm | Ox-Tube-Lindberg / Tube-OxAnneal-Expertech-CTR200 | R1_TRAP, R1_FULL |
| 3 | Inlaid Al local mirror | 10 | evaporated Al, inlaid in the thermal SiO₂, under the detector and its leads only | 100 nm (was 450 nm; 150 nm in v3) | MLA150; SiO₂ RIE (as step 11); EBeam-Temescal-FC2800; lift-off | R1_FULL, A30 and B60 only |
| 4 | SiO₂ spacer | – | PECVD SiO₂ | 238 ± 10 nm | PECVD-Samco-PD220 or PECVD-Oxford-TEOS | R1_FULL |
| 5 | NbN film | – | NbN | 7 nm | Berggren-group AJA (RF substrate bias) [verify access] | R1_FULL |
| 6 | Ti/Au NbN contacts and EBL marks (lift-off) | 22 | Ti/Au | 10 / 350 nm [verify] | MLA150; EBeam-Temescal-FC2800 | R1_FULL |
| 7 | Nanowire EBL + CF₄ etch; HSQ left on | 20 | HSQ on NbN | HSQ 50–70 nm | EBL-Elionix-HS50; RIE-PlasmaTherm-210RL | R1_FULL |
| 8 | SiO₂ cap | – | HSQ + PECVD SiO₂ | HSQ + cap = 160 ± 10 nm over the wires | PECVD (as step 4) | R1_FULL |
| 9 | *removed in v4* (was the 10 µm SiO₂ D2) | – | – | – | – | – |
| 10 | *removed in v4* (was the top ITO) | – | – | – | – | – |
| 11 | Openings through the thin stack | 40 | – | Mirror via through ~0.40 µm (cap + spacer) to the Al; SNSPD contacts through ~160 nm of SiO₂ | MLA150; RIE-F-Samco-230iP / RIE-PlasmaTherm-210RL | R1_FULL |
| 12 | Electrode Au, step 12: E1 LOR + positive resist; E2 Ti/Au seed | 50 | E1 resist; E2 Ti 15 nm / Au 50 nm seed | – | MLA150; Sputter-AJA-* (E2 seed) | R1_TRAP, R1_FULL (E1 or E2) |
| 13 | Electrode Au, step 13: E1 Ti 10 nm / Au 350 nm evaporation; E2 nLOF mold ≥ 8 µm, inverted | 50 | E1 Ti/Au; E2 AZ nLOF 2070 | E1 Au 0.35 µm [verify]; E2 mold ≥ 8 µm | E1 evaporator [verify]; E2 MLA150 | R1_TRAP, R1_FULL (E1 or E2) |
| 14 | Electrode Au, step 14: E1 lift-off in NMP; E2 Au plating | 50 | Au | E1 0.35 µm; E2 6.0 µm | E1 NMP [verify]; E2 Plating-U04 [chemistry unverified] | R1_TRAP, R1_FULL (E1 or E2) |
| 15 | Inspection (both branches); E2 also strip and seed removal | – | E2: Au 50 nm and Ti 15 nm seed removed | – | E2: Asher-*, Clean-Ar-Plasma [verify it can mill], RIE-F | R1_TRAP, R1_FULL (E1 or E2) |
| 16a, 16 | *removed in v4* (were the layer-45 protect and the D2 gap etch) | – | – | – | – | – |
| 17 | Room-temperature wafer-level electrical test | – | – | – | ProbeStation-Summit-11000 | R1_TRAP, R1_FULL |
| 18 | Protect, dice | 101 | – | 10 × 10 mm trap dies, 10 × 2.5 mm test dies, 200 µm streets | Diesaw-DAD3240 | R1_TRAP, R1_FULL |
| 19 | Package, wire bond | – | Au wire on Au pads | – | Wirebond-Wedge / Wirebond-Ball-MEI; carrier open | R1_TRAP, R1_FULL |

NODET dies have no Al, so step 3 does not apply to them. Whether NODET dies on R1_FULL receive steps 4–8 is not stated in the sources [verify].

### Lithography layers (v4)

| Layer | Name | Use | Exposure | Used in |
|---|---|---|---|---|
| 1 | MARK | Si alignment marks | drawn | R1_TRAP, R1_FULL |
| 10 | M1 | Inlaid Al local mirror, 100 nm (A30, B60) | drawn, not inverted | R1_FULL |
| 20 | NbN | Nanowire, EBL (datatype 0 nominal dose; 1–7 T8 dose array) | e-beam | R1_FULL |
| 22 | Ti/Au | NbN contacts and EBL marks only | drawn | R1_FULL |
| 40 | openings | Mirror ground via and SNSPD contacts only (no mirror probe opening; the mirror is measured on the test die, T10, T11 and the T4/T4b probe pads) | – | R1_FULL |
| 50 | Au | Electrodes, ground fill, pads, SNSPD leads in the slot | E1 drawn; E2 inverted (plating mold) | R1_TRAP, R1_FULL |
| 24, 30, 31, 45 | retired | Must stay empty | – | – |
| 100, 101 | notes, outlines | Not fabricated | – | – |

## C. Final cross-section under the readout window (bottom to top)

[Layer stack](STACK.md#readout-cross-section), v4. R1_TRAP has no Al, spacer, NbN or cap: the electrode Au sits on 1.0 µm thermal SiO₂ on high-resistivity Si (STACK, section (c)).

## D. Thermal budget

[Temperature limits](STACK.md#thermal-budget). Rule: **≤ 300 °C for every step after step 3** (the Al deposition) on A30 and B60 runs. R1_TRAP has no Al, so the rule does not apply to it. The 10 µm SiO₂ D2 and its long 300 °C exposure are removed in v4.

## E. Witness wafers and short loops to run first

[Qualification W1–W8 and facility questions](QUALIFICATION.md). For R1_TRAP, the short loops are W7 bond-and-leak (both branches), W5 plating (E2 only) and the E1 lift-off test, as listed in the [R1_TRAP sheet](RUNSHEET_R1_TRAP.md). The D2 stress and gap-etch loops are not needed in v4 ([open decisions](OPEN_DECISIONS.md#before-r1_trap)).

## F. Steps

Original step numbers are retained. 8a and 8b (the v3 M1 via and buried ITO) and 10 (top ITO) are retired. Steps 9 (D2), 16a (protect) and 16 (gap etch) are removed in v4.

| Stage | Recipes | R1_TRAP |
|---|---|---|
| 0–2 | [Substrate, marks, D1](process/01_FOUNDATION.md) | Required |
| 3 | [Inlaid Al local mirror](process/01_FOUNDATION.md#3-m1-inlaid-al-local-mirror-l10) | No (no Al) |
| 4–8 | [Spacer, NbN, contacts, nanowire, cap](process/02_DETECTOR.md) | Skip |
| 9–11 | [Layer-40 openings (11)](process/03_ELECTRODES.md#11-layer-40-openings-through-the-thin-stack); 9 and 10 removed | Skip |
| 12–15 | [Electrodes, E1 or E2](process/03_ELECTRODES.md#electrodes-layer-50-e1-and-e2) | Required (choose E1 or E2) |
| 16a, 16 | [Removed in v4](process/03_ELECTRODES.md#16a-removed-in-v4) | No |
| 17–19 | [Test, dice, package](process/04_PACKAGING.md) | Required; omit detector tests |

## G. Substrate deltas (sapphire, fused silica)

[Substrate alternatives](variants/SUBSTRATES.md). The adopted v4 substrate is high-resistivity FZ Si with ρ > 20 kΩ·cm ([stack](STACK.md)).

## H. Local mirror: the adopted v4 process (no D2)

[Local mirror (adopted v4)](variants/LOCAL_MIRROR.md). Its H.2 table is the basis of the v4 steps in section B. The architecture decision is recorded in [decisions](../../notes/decisions.md) (2026-11-08). The die-wide Al plane under 10 µm of SiO₂ is the superseded v3 baseline.

## Companion checks

[Masks](mask_list.md) · [Process checks](process_checks.md) · [Tests](test_plan.md) · [Variants](VARIANTS.md).
