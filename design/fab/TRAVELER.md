> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Fabrication traveler

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

Baseline architecture: die-wide Al, SiO₂ spacer, NbN, SiO₂ cap, 10 µm D2 and 6 µm plated Au. For the selected first run, use the shorter [R1_TRAP sheet](RUNSHEET_R1_TRAP.md).

> [!important] Before starting
> Complete [qualification](QUALIFICATION.md) and review [open decisions](OPEN_DECISIONS.md). Current generators use v3.1 detectors; older estimates are marked in the detailed notes. This is a proposed process, not a qualified recipe.

Wafer ID: ________ Run: ________ Generator revision/date: ________ Start date: ________ Operator: ________

## A. Die layout (v3) and tape-out status

[Layout, marks, pads and protections](LAYOUT.md).

### A.1 Resolved in the GDS (v2, carried into v3)

[Layout protections A1–A7](LAYOUT.md#a1-resolved-in-the-gds-v2-carried-into-v3).

### A.2 Still open

[Design decisions and run requirements](OPEN_DECISIONS.md).

### A.3 R&D run plan at MIT.nano

[Run sequence and maps](RUN_PLAN.md).

## B. One-screen process summary

| # | Step | GDS layer | Material | Target thickness | Tool (MIT.nano name where verified in the report) |
|---|---|---|---|---|---|
| 0 | Wafer prep, clean | – | HR FZ Si, 100 mm | 500–525 µm [verify] | Acid-Etch-General-* (piranha) |
| 1 | Alignment marks | 1 | Si etch | ~1 µm deep | DirectWrite-MLA150-*; RIE-F-Samco-230iP |
| 2 | Thermal oxide D1, both sides | – | SiO₂ | 1.0 µm | Ox-Tube-Lindberg / Tube-OxAnneal-Expertech-CTR200 |
| 3 | M1 ground plane + mirror | 10 | Al-1%Cu | 150 nm | Sputter-AJA-*; MLA150; RIE-Cl2-SAMCO-200iP |
| 4 | Spacer | – | PECVD SiO₂ | 238 nm | PECVD-Samco-PD220 or PECVD-Oxford-TEOS |
| 5 | NbN film | – | NbN | 7 nm | Berggren-group AJA (RF substrate bias) [verify access] |
| 6 | SNSPD leads + EBL marks (lift-off) | 22 | Ti/Au | 10 / 350 nm | MLA150; EBeam-Temescal-FC2800 |
| 7 | Nanowire EBL + CF₄ etch | 20 | HSQ on NbN | HSQ 50–70 nm spun | EBL-Elionix-HS50; RIE-PlasmaTherm-210RL |
| 8 | Cap | – | PECVD SiO₂ | HSQ + cap = 80 nm over the wires | PECVD (as step 4) |
| 8a, 8b | *removed in v3* (were the M1 via and buried ITO) | – | – | – | – |
| 9 | D2 | – | PECVD SiO₂ | 10.0 µm front + backside compensation | PECVD; Filmstress-Tencor-FLX2320 |
| 10 | *removed in v3* (was the top ITO) | – | – | – | – |
| 11 | D2 openings | 40 | – | etch ~10.3 µm | MLA150; RIE-F-Samco-230iP / RIE-PlasmaTherm-210RL |
| 12 | Plating seed | – | Ti/Au | 15 / 50 nm | Sputter-AJA-* |
| 13 | Plating mold | 50 | AZ nLOF 2070 | ≥ 8 µm | MLA150 |
| 14 | Au electroplating | 50 | Au | 6.0 µm | Plating-U04 [chemistry unverified] |
| 15 | Strip, seed removal | – | – | Au 50 nm, Ti 15 nm removed | Asher-*; Clean-Ar-Plasma [verify it can ion-mill]; RIE-F |
| 16a | Protect resist | 45 | thick positive resist | ≥ 10 µm | MLA150 |
| 16 | Au-masked D2 gap etch | – (L50 is the mask) | – | etch ~9.6 µm, stop 0.75 µm above M1 | RIE-F-Samco-230iP |
| 17 | RT wafer-level electrical test | – | – | – | ProbeStation-Summit-11000 |
| 18 | Protect, dice | 101 | – | 10 × 10 mm trap dies, 10 × 2.5 mm test dies, 200 µm streets | Diesaw-DAD3240 |
| 19 | Package, wire bond | – | Au / Al wire | – | Wirebond-Wedge / Wirebond-Ball-MEI |

## C. Final cross-section under the readout window (bottom to top)

[Layer stack](STACK.md#readout-cross-section). R1_TRAP omits spacer/NbN/cap.

## D. Thermal budget

[Temperature limits](STACK.md#thermal-budget): ≤ 300 °C after Al deposition.

## E. Witness wafers and short loops to run first

[Qualification W1–W7 and facility questions](QUALIFICATION.md).

## F. Steps

| Stage | Recipes | R1_TRAP |
|---|---|---|
| 0–3 | [Substrate, marks, D1, Al](process/01_FOUNDATION.md) | Required |
| 4–8 | [Spacer, NbN, leads, nanowire, cap](process/02_DETECTOR.md) | Skip |
| 9–16 | [D2, vias, plating, protection, gap etch](process/03_ELECTRODES.md) | Required with run-sheet changes |
| 17–19 | [Test, dice, package](process/04_PACKAGING.md) | Required; omit detector tests |

Original step numbers are retained. **8a, 8b and 10 are retired** with ITO. **16a comes before 16.**

## G. Substrate deltas (sapphire, fused silica)

[Substrate alternatives](variants/SUBSTRATES.md).

## H. Variant: Hampel-style local mirror, no D2 (not the baseline; no GDS yet)

[Local-mirror proposal E1/E2](variants/LOCAL_MIRROR.md).

## Companion checks

[Masks](mask_list.md) · [Process checks](process_checks.md) · [Tests](test_plan.md) · [Variants](VARIANTS.md).
