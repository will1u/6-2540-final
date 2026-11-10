> **Claude-authored.** Glossary of the short labels used in `design/` (dies, runs, layers, electrodes, tests, tools, acronyms, physics symbols), each with a link to its defining file, 2026-11-10.

# Glossary

How to use this page: find the label in its section, read the one-line meaning, and follow the link for the authoritative definition. Where two repo files disagree, the entry says so and the value is tagged `[verify]`. Paths in the last column are relative to `design/`.

## Dies and runs

| Term | Meaning | Defined in |
|---|---|---|
| A30 | Trap die with a 30 × 30 µm Au readout window over the NbN detector (v4). | [VARIANTS](fab/VARIANTS.md) |
| B60 | Trap die with a 60 × 30 µm Au window over the same v4 detector stack; longer meander. | [VARIANTS](fab/VARIANTS.md) |
| NODET | Trap die with no SNSPD, no window (solid centre DC) and no Al. The R1_TRAP die. | [CLAUDE](CLAUDE.md) (line 79); [LAYOUT](fab/LAYOUT.md) |
| UNIFORM | Equal-depth DC segments with no leads. Simulation reference only; never fabricate. | [VARIANTS](fab/VARIANTS.md) |
| TEST | Test die (10 × 2.5 mm, not a trap) with T1 to T12 structures for process, dose and geometry comparisons. The current files are `test_die_v4.gds` and `test_die_v4_TRAP.gds` (DESIGN_LOG step 35). | [VARIANTS](fab/VARIANTS.md); [LAYOUT](fab/LAYOUT.md) |
| TEST_TRAP | Test die with only T1 and T6, on layers 1 and 50. No NbN and no Al. | [VARIANTS](fab/VARIANTS.md) |
| R1_TRAP | First run (run 1a): 6 NODET and 2 TEST_TRAP dies, trap only, no Al, NbN or EBL. | [VARIANTS](fab/VARIANTS.md) |
| R1_FULL | Second run (run 1b): 2 A30, 2 B60, 2 NODET and 2 TEST dies on the full v4 stack. Planned after trap-process qualification. | [VARIANTS](fab/VARIANTS.md) |

## Electrode options and versions

| Term | Meaning | Defined in |
|---|---|---|
| E1 | Electrode Au option: Ti 10 nm / Au 350 nm, evaporated and lifted off (0.35 µm). Not yet chosen by the team. | [TRAVELER](fab/TRAVELER.md) (line 8); [QUALIFICATION](fab/QUALIFICATION.md) (line 8) |
| E2 | Electrode Au option: 6 µm plated Au on a Ti/Au seed. Not yet chosen by the team. | [TRAVELER](fab/TRAVELER.md) (line 8); [QUALIFICATION](fab/QUALIFICATION.md) (line 8) |
| v1 | Square die with the zones in the corners. Archived in `gds/archive_v1_square/`. Do not use. | [CLAUDE](CLAUDE.md) (line 89) |
| v2 | Narrow 10 × 2.5 mm die with the two-ITO window. Archived in `gds/archive_v2_narrow/`. Do not use. | [CLAUDE](CLAUDE.md) (line 89) |
| v3 | 10 × 10 mm die with no ITO, a die-wide Al plane under 10 µm of D2. Superseded 2026-11-08; archived in `gds/archive_v3_baseline/`; not for fab. | [CLAUDE](CLAUDE.md) (line 80); [VARIANTS](fab/VARIANTS.md) (line 8) |
| v3.1 | Detector geometry revision: 130 nm wires, 200 nm pitch NbN meander, 160 lines. Used in both v3 and v4 generators. | [VARIANTS](fab/VARIANTS.md) (Detector revision); [CLAUDE](CLAUDE.md) (line 168) |
| v4 | Current local-mirror architecture (team decision 2026-11-08): Au electrodes on thin SiO₂ over high-resistivity Si, Al mirror only under the detector and its leads, no D2. The SiO₂ cap over the wires is 160 ± 10 nm (DESIGN_LOG steps 26 and 35; it was 80 nm before). | [CLAUDE](CLAUDE.md) (line 12); [VARIANTS](fab/VARIANTS.md) |

## File-name suffixes

| Term | Meaning | Defined in |
|---|---|---|
| _V2zero | Output of sim 12 run with `--centre-dc-zero`: centre DC (electrode 2) held at 0 V in every solve. | [12_final_chip_check.py](sim/12_final_chip_check.py) |
| _E1 | Au option E1 (0.35 µm). Files with this suffix are E1; the unsuffixed files are E2. Example: `trap_die_v4_A30_E1_sim.json`. | [CLAUDE](CLAUDE.md) (line 79) |
| _simfloor | Simulation-only GDS: layer 50 plus the grounded window floor. Never for fab. | [CLAUDE](CLAUDE.md) (line 79); [make_chip.py](gds/make_chip.py) |
| _pad180 | Sim 12 output folder for the 180 µm pad-pitch baseline, kept for comparison with the 360 µm layout. The unsuffixed folders are the current 360 µm runs (`sim/16_pad_pitch_check.py` compares the two). | [16_pad_pitch_check.py](sim/16_pad_pitch_check.py) (header) |
| _600um | Log files of v4 runs made before the zone spacing changed from 600 to 480 µm (DESIGN_LOG step 28). They are in `sim/out/archive/`. | [archive README](sim/out/archive/README.md); [CLAUDE](CLAUDE.md) (Conventions, zones) |
| _sim.json | gds2itvg simulation layout for a die: electrode seeds, die size and marks. Unsuffixed is E2. | [CLAUDE](CLAUDE.md) (line 79) |
| _pads.csv | Pad list for a die: pad names, coordinates and electrode numbers. | [CLAUDE](CLAUDE.md) (line 79) |

## Layers

| Term               | Meaning                                                                                                            | Defined in                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| 1 (MARK)           | Si alignment marks, about 1 µm etch.                                                                               | [CLAUDE](CLAUDE.md) (Layers table); [layer_map](gds/layer_map.md)          |
| 10 (M1)            | Evaporated Al, 100 nm, inlaid in the thermal SiO₂: the local mirror under the detector (A30, B60).                 | [CLAUDE](CLAUDE.md) (Layers table); [layer_map](gds/layer_map.md)          |
| 20 (NbN)           | NbN meander and contact tabs. Datatype 0 is the nominal dose; datatypes 1–7 are the T8 dose array.                 | [CLAUDE](CLAUDE.md) (Layers table)                                         |
| 22 (Ti/Au)         | Ti/Au contacts from the NbN tabs into the slot, and EBL marks. Called LEAD in [layer_map](gds/layer_map.md).       | [CLAUDE](CLAUDE.md) (Layers table); [layer_map](gds/layer_map.md)          |
| 24                 | M1 via layer of v2. Retired in v3; must stay empty.                                                                | [CLAUDE](CLAUDE.md) (Layers table)                                         |
| 30                 | Top ITO layer. Retired in v3; must stay empty.                                                                     | [CLAUDE](CLAUDE.md) (Layers table)                                         |
| 31                 | Buried ITO layer. Retired in v3; must stay empty.                                                                  | [CLAUDE](CLAUDE.md) (Layers table)                                         |
| 40                 | Openings through the SiO₂: SNSPD contacts and the mirror ground via. Called OPEN in [layer_map](gds/layer_map.md). | [CLAUDE](CLAUDE.md) (Layers table); [layer_map](gds/layer_map.md)          |
| 45                 | PROTECT layer of v3 (gap-etch patch). Retired in v4; must stay empty.                                              | [CLAUDE](CLAUDE.md) (Layers table); [LAYOUT](fab/LAYOUT.md)                |
| 50 (Au)            | Electrodes, ground fill, pads and the SNSPD leads in the slot. The layer gds2itvg simulates.                       | [CLAUDE](CLAUDE.md) (Layers table)                                         |
| 100                | Notes (text). Not fabricated.                                                                                      | [CLAUDE](CLAUDE.md) (Layers table)                                         |
| 101                | Die and wafer outlines. Not fabricated.                                                                            | [CLAUDE](CLAUDE.md) (Layers table)                                         |
| M1                 | Name of layer 10.                                                                                                  | [CLAUDE](CLAUDE.md) (Names)                                                |
| L22, L40, L45, L50 | Short names for layers 22, 40, 45 and 50 used in the fab pages.                                                    | [LAYOUT](fab/LAYOUT.md)                                                    |
| D1                 | Thermal SiO₂, 1.0 µm, on both sides (traveler step 2).                                                             | [TRAVELER](fab/TRAVELER.md) (step 2)                                       |
| D2                 | 10 µm deposited SiO₂ of v3. Gone in v4 (no 10 µm SiO₂).                                                            | [fab README](fab/README.md) (line 8); [VARIANTS](fab/VARIANTS.md) (line 8) |

## Electrode and pad numbers

| Term | Meaning | Defined in |
|---|---|---|
| 1 | RF electrode (the RF rails). RF pad at (4700, 0) µm. | [LAYOUT](fab/LAYOUT.md) (line 41); [CLAUDE](CLAUDE.md) (line 130) |
| 2 | Centre DC electrode. Pad C at (−4650, 450) µm. | [LAYOUT](fab/LAYOUT.md) (line 41); [CLAUDE](CLAUDE.md) (line 131) |
| 3–17 | Top outer DC segments, left to right. | [CLAUDE](CLAUDE.md) (line 132) |
| 18–32 | Bottom outer DC segments. | [CLAUDE](CLAUDE.md) (line 132) |
| 33, 34 | Top caps, left (L) and right (R). Pads TL1 = 33 and TR1 = 34. | [LAYOUT](fab/LAYOUT.md) (line 41); [CLAUDE](CLAUDE.md) (line 133) |
| 35, 36 | Bottom caps, left (L) and right (R). Pads BL1 = 35 and BR1 = 36. | [LAYOUT](fab/LAYOUT.md) (line 41); [CLAUDE](CLAUDE.md) (line 133) |
| 96 | Window floor. Simulation only (`_simfloor.gds`). | [CLAUDE](CLAUDE.md) (line 134) |
| 97, 98 | SNSPD signal and return leads, held at about 0 V in simulation (A30). | [CLAUDE](CLAUDE.md) (line 134) |
| 99 | Ground seed (the Au ground fill). | [CLAUDE](CLAUDE.md) (line 134) |
| TL, TR, BL, BR | Pad rows: top-left, top-right, bottom-left, bottom-right (TL1 … TL8, TR1 … TR9, BL1 … BL8, BR1 … BR9). | [LAYOUT](fab/LAYOUT.md) (line 33–38) |
| SNS | SNSPD signal pad at (−4750, +100) µm, Au. Also the SNSPD_S pad in the test rules. | [LAYOUT](fab/LAYOUT.md) (line 24); [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| SNG | SNSPD return (ground) pad at (−4750, −100) µm, Au. Also SNSPD_G. | [LAYOUT](fab/LAYOUT.md) (line 24); [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| GND-1 … GND-4 | Au ground-fill bond spots at (±4700, ±1500) µm. | [LAYOUT](fab/LAYOUT.md) (line 25) |

## Zones and coordinate frames

| Term | Meaning | Defined in |
|---|---|---|
| Loading zone | Zone at GDS (−240, 0) µm. In the ITVG frame it is at y = −480. | [CLAUDE](CLAUDE.md) (lines 127–128) |
| Readout zone | Zone at GDS (+240, 0) µm, directly above the SNSPD. Origin of the ITVG frame. | [CLAUDE](CLAUDE.md) (lines 127–128) |
| GDS frame | Die centre at (0, 0), trap axis y = 0 running along x, units µm, database unit 1 nm. Trap die 10 × 10 mm. | [CLAUDE](CLAUDE.md) (line 126) |
| ITVG frame | Simulation frame (`*_sim.json`): origin at the readout zone, `quarter_turns: 1`, so ITVG y = GDS x − 240. | [CLAUDE](CLAUDE.md) (line 128) |

## Test structures (T)

| Term | Meaning | Defined in |
|---|---|---|
| T1 | Au comb with 5 µm gaps: DC leakage and flashover across the trap gap. On TEST and TEST_TRAP. | [LAYOUT](fab/LAYOUT.md) (line 71) |
| T2 | Retired: the v3 Au / D2 / Al capacitor. Replaced by T2v. | [OPEN_DECISIONS](fab/OPEN_DECISIONS.md) (line 30) |
| T2v | Au / 0.40 µm SiO₂ / Al capacitor: 200 µm Au plate over a 240 µm Al plate. About 3.5 pF [team calc]. | [LAYOUT](fab/LAYOUT.md) (line 72) |
| T3 | NbN 4-wire bar: Rsq and Tc of the patterned NbN film. | [LAYOUT](fab/LAYOUT.md) (line 73) |
| T4 | Spare SNSPD with the A30 meander on its own local Al mirror, with a mirror probe pad. | [LAYOUT](fab/LAYOUT.md) (line 74) |
| T4b | Spare SNSPD with the B60 meander on its own local Al mirror. | [LAYOUT](fab/LAYOUT.md) (line 75) |
| T5 | Retired; removed from the test die. | [CLAUDE_PROGRESS](../CLAUDE_PROGRESS.md) (line 103) |
| T6 | Au continuity loop, 6 µm line, two pads. On TEST and TEST_TRAP. | [LAYOUT](fab/LAYOUT.md) (line 76) |
| T7 | Retired; removed from the test die. | [CLAUDE_PROGRESS](../CLAUDE_PROGRESS.md) (line 103) |
| T8 | EBL dose array: seven A30 meanders on NbN datatypes 1–7, dose factors 0.80 to 1.20 × nominal. | [LAYOUT](fab/LAYOUT.md) (line 77) |
| T9 | Geometry array: wire width and pitch variants, turn shape, length series, straight references. | [LAYOUT](fab/LAYOUT.md) (line 78) |
| T10 | Al mirror strip, four-point, over 2510 µm. Expected 18.8–25.1 Ω at 100 nm Al [team calc]. | [LAYOUT](fab/LAYOUT.md) (line 79) |
| T11 | Au-to-Al via chain: four vias in series. | [LAYOUT](fab/LAYOUT.md) (line 80) |
| T12 | Two 5 µm Au leads 5 µm apart over an Al strip, modelling the SNSPD leads in the slot. | [LAYOUT](fab/LAYOUT.md) (line 81) |

## Tests (a, b)

The a-tests are room-temperature electrical tests. The b-tests are cryogenic detector tests.

### a-tests (room temperature)

| ID | What it measures | Defined in |
|---|---|---|
| a1 | RF leakage: RF to ground fill, centre DC and caps. 300 V `[verify]`, pass ≤ 100 nA. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a2 | DC leakage: each DC pad to its neighbours and the ground fill. 50 V `[verify]`, pass ≤ 100 nA. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a3 | Continuity of the T6 loop at 1 mA. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a4 | Retired in v4 (old T2 dielectric test). See a15. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a5 | Gap leakage and redeposition across the T1 comb. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a6 | NbN Rsq on the T3 4-wire bar, within 10 % of the step-7 value. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a7 | Meander resistance, SNS to SNG on trap dies and T4 / T4b on test dies. ΔR/R₀ ≤ 10 %. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a8 | SNSPD isolation to the ground fill or the mirror probe pad. Pass > 1 GΩ `[verify]`. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a9 | Retired (v3 ITO test). | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) (Run applicability) |
| a10 | RF capacitance, packaged dies only (LCR at 1 MHz). No v4 pass value. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a11 | Retired (v3 ITO test). | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) (Run applicability) |
| a12 | Dose array on T8: resistance against dose factor. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a13 | Ground link from the mirror to the fill, checked on T10 and T11 (test die). Limit `[verify]`. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a14 | Geometry array on T9: resistance against squares × Rsq, within 10 %. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a15 | Dielectric capacitor on T2v: capacitance and leakage at 50 V `[verify]`. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a16 | Al mirror strip resistance on T10, four-point. Limit `[verify]`. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a17 | Au-to-Al via-chain resistance on T11. Limit `[verify]`. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a18 | Lead continuity over the Al edge and lead-to-lead leakage on T12. Limits `[verify]`. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| a19 | SNSPD-lead leakage to the centre DC (C). Pass > 1 GΩ `[verify]`. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |

### b-tests (cryogenic)

| ID | What it measures | Defined in |
|---|---|---|
| b1 | R(T) through Tc on the meander and T3. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b2 | I–V curve, I_sw and latching current with RF off, base to 7 K. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b3 | Pulse shape after the amplifier; fitted τ, hence L_k. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b4 | Count rate against bias under a 493 nm flood, RF off (plateau?). | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b5 | Dark count rate (DCR) against bias, light off. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b6 | RF on and off at 28 MHz, V_RF 0 to 70 V (53 V is the operating amplitude). I_sw against V_RF. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b7 | Clicks with bias off, RF on, light on and off. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b8 | RF heating: I_sw read ≤ 10 µs after RF switches off. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b9 | Bias gating with 10 µs ramps. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| b10 | T9 geometry array: I_sw ratios and whether 130 nm keeps a saturated plateau at 493 nm and 5 K. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |

## Witness loops (W)

| Term | Meaning | Defined in |
|---|---|---|
| W1 | NbN on the spacer over the 100 nm Al: Rsq, Tc and hillocks on the real stack. | [QUALIFICATION](fab/QUALIFICATION.md) (W1 heading) |
| W2 | HSQ dose, develop and CF₄ etch on the real stack; mark recognition and overlay. | [QUALIFICATION](fab/QUALIFICATION.md) (W2 heading) |
| W3 | Layer-40 openings, Au-to-Al contact and electrode rehearsal, with no NbN. | [QUALIFICATION](fab/QUALIFICATION.md) (W3 heading) |
| W5 | Plating calibration for the 6 µm Au. E2 only. | [QUALIFICATION](fab/QUALIFICATION.md) (W5 heading) |
| W7 | Bond-and-leak test on dummy pads. R1_TRAP and R1_FULL, both options. | [QUALIFICATION](fab/QUALIFICATION.md) (W7 heading) |
| W8 | Inlaid 100 nm Al mirror on a dummy wafer: recess, lift-off, planar surface. | [QUALIFICATION](fab/QUALIFICATION.md) (W8 heading) |
| E1 lift-off loop | Lift-off of 0.35 µm Au over 5 µm gaps, and wedge bonding. E1 only. | [QUALIFICATION](fab/QUALIFICATION.md) (E1 lift-off heading) |
| W4, W6 | Do not exist in the current v4 plan. There is no W4 or W6 heading in QUALIFICATION. | [QUALIFICATION](fab/QUALIFICATION.md) |

## Step numbers

Two numbering schemes both use the word "step". They are different things.

| Term | Meaning | Defined in |
|---|---|---|
| Process step 0–19 | Row number in the fabrication traveler, for example process step 3 = inlaid Al local mirror. Tables such as "R1_TRAP uses steps 0, 1, 2, 12–15, 17, 18 and 19" use these. | [TRAVELER](fab/TRAVELER.md) |
| Design-log step | Numbered entry in the design log, headed "Step N, …", for example "Step 3, outer DC segment pitch". Notes cite it as "DESIGN_LOG step 25" or "(step 36)". | [DESIGN_LOG](DESIGN_LOG.md) |
| How to tell them apart | If the text says "traveler", "process" or lists runs and dies, the number is a process step. If it says "DESIGN_LOG", "sim/" or sits next to a simulation, it is a design-log step. The design log starts at step 0 and new steps are appended at the end; process steps stop at 19. | [TRAVELER](fab/TRAVELER.md); [DESIGN_LOG](DESIGN_LOG.md) |

## Doc tags

| Term | Meaning | Defined in |
|---|---|---|
| [verify] | Not yet checked on the tool or against the source. | [CLAUDE](CLAUDE.md) (lines 28–31) |
| [team calc] | Computed for this project. | [CLAUDE](CLAUDE.md) (lines 28–31) |
| [inference] | Reasoning, not data. | [CLAUDE](CLAUDE.md) (lines 28–31) |

## Tools and files

| Term | Meaning | Defined in |
|---|---|---|
| gds2itvg | Simulation tool in the `electrode` repo. Reads a GDSII layout, writes unit-potential grid files for ITVG, and can find the RF null. | [root CLAUDE](../CLAUDE.md) (Tooling) |
| electrode repo | Clone of the gds2itvg repo, sibling to this repo, with its own conda env `electrode`. Not NIST's `electrode` package. | [root CLAUDE](../CLAUDE.md) (Tooling); [CLAUDE](CLAUDE.md) (Setting up) |
| ITVG | The `VoltageGenerator` program that gds2itvg writes its grid files for. | [root CLAUDE](../CLAUDE.md) (Tooling) |
| run.sh | Runs a design script in the `electrode` conda env from Git Bash: `cd design/sim && ./run.sh <script>`. | [CLAUDE](CLAUDE.md) (Environment); [run.sh](sim/run.sh) |
| check_chip.py | DRC, connectivity and fab-consistency checks on a trap die. A pass prints `ALL CHECKS PASS`. | [check_chip.py](gds/check_chip.py); [CLAUDE](CLAUDE.md) (line 87) |
| summary.json | Results file written by a sim script into `sim/out/<script>/`. Sim 12 writes one. | [12_final_chip_check.py](sim/12_final_chip_check.py) |

## Acronyms

| Term | Meaning | Defined in |
|---|---|---|
| SNSPD | Superconducting nanowire single-photon detector. | [CLAUDE](CLAUDE.md) (line 9) |
| NbN | Niobium nitride, the superconducting film of the detector. | [CLAUDE](CLAUDE.md) (line 12) |
| HSQ | Hydrogen silsesquioxane, an e-beam resist used on the NbN before etching. | [TRAVELER](fab/TRAVELER.md) (step 7) |
| EBL | Electron-beam lithography. | [TRAVELER](fab/TRAVELER.md) (step 7) |
| MLA | Maskless aligner (laser writer) used for optical patterning, for example MLA150. | [TRAVELER](fab/TRAVELER.md) (step 6) |
| PECVD | Plasma-enhanced chemical vapour deposition, used for SiO₂ spacer and cap. | [TRAVELER](fab/TRAVELER.md) (step 4) |
| RIE | Reactive-ion etching. | [TRAVELER](fab/TRAVELER.md) (step 3) |
| TMM | Transfer-matrix method, the thin-film optics model. | [CLAUDE_PROGRESS](../CLAUDE_PROGRESS.md) (line 140) |
| EMT | Effective-medium theory, the model for NbN absorption. | [CLAUDE](CLAUDE.md) (line 168) |
| RCWA | Rigorous coupled-wave analysis, an optics method. Not yet applied to the meander. | [CLAUDE_PROGRESS](../CLAUDE_PROGRESS.md) (line 140) |
| FDTD | Finite-difference time-domain, an electromagnetic simulation method. Not yet applied to the meander. | [CLAUDE_PROGRESS](../CLAUDE_PROGRESS.md) (line 140) |
| QCCD | Quantum charge-coupled device, the shuttling architecture the project targets. | [root CLAUDE](../CLAUDE.md) (line 3) |
| PGA / CPGA | Pin grid array package; CPGA is the ceramic version. Carrier options are PGA84L-like or CPGA. | [OPEN_DECISIONS](fab/OPEN_DECISIONS.md) (Carrier row); [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) (a10) |
| SMU | Source-measure unit, the instrument used for the probe tests. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| LCR | LCR meter (inductance, capacitance, resistance), used for a10 at 1 MHz. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) (a10) |
| DAC | Digital-to-analog converter that drives the electrode voltages (±10 V in this design). | [CLAUDE](CLAUDE.md) (Key design numbers) |
| ARTIQ | Control system for trapped-ion experiments. Its TTL input counts the photon edges in the readout. | [03_READOUT](fab/tests/03_READOUT.md) |
| DRC | Design-rule check. | [CLAUDE](CLAUDE.md) (line 87) |
| HR Si | High-resistivity silicon (ρ > 20 kΩ·cm), the substrate. | [CLAUDE](CLAUDE.md) (line 12) |
| RRR | Residual resistance ratio of the Au, an unverified cold-resistance assumption. | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) (a7) |
| DCR | Dark count rate. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) (b5) |

## Physics terms

Values come from the Key design numbers section of [CLAUDE](CLAUDE.md) or from [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md). A term with no value in those two sources says so.

| Term | Meaning and value | Defined in |
|---|---|---|
| RF null | Point where the RF field vanishes, where the ion is held. Ion height at the null: 49.97 µm (loading) and 49.98 µm (readout), planar model. | [CLAUDE](CLAUDE.md) (Key design numbers) |
| Pseudopotential depth | Trap depth from the RF pseudopotential: ≈ 52 meV at 53 V, 28 MHz. | [CLAUDE](CLAUDE.md) (Key design numbers) |
| Mathieu q | Stability parameter of the radial RF motion: 0.30 at 53 V, 28 MHz. | [CLAUDE](CLAUDE.md) (Key design numbers) |
| Secular frequency | Ion oscillation frequency in the pseudopotential. Radial ≈ 3.0 MHz; see axial below. | [CLAUDE](CLAUDE.md) (Key design numbers) |
| Radial frequency | Secular frequency across the trap (radial): ≈ 3.0 MHz. | [CLAUDE](CLAUDE.md) (Key design numbers) |
| Axial frequency | Secular frequency along the trap axis: 0.8 MHz. | [CLAUDE](CLAUDE.md) (Key design numbers) |
| Micromotion | Ion motion at the RF frequency, which grows when the ion sits off the RF null. Over the readout window the ion sits off the null when DC fields push it back up; sim 13 reports the resulting amplitude (`sim/out/13_dc_height_tuning_v4/summary.json`, key `a_mm_nm`). | [DESIGN_LOG](DESIGN_LOG.md) |
| Radial tilt | Tilt of the DC confining field in the radial plane: 10° in the zones. | [CLAUDE](CLAUDE.md) (Key design numbers) |
| I_sw | NbN switching current: ≈ 8–9 µA for a 100 nm wire at about 5 K [team calc, rough]. [sim 19](sim/19_lead_termination.py) uses 8–20 µA `[verify]`. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| L_k | Kinetic inductance: ≈ 3.3 µH for the v3.1 A30 meander at 70 pH/sq (7 nm NbN); τ = L/50 Ω ≈ 66 ns. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| R_sq | Sheet resistance of a thin film, in Ω per square. No value in the two designated sources; the value used in the tests is in [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) (a7). | [01_ELECTRICAL](fab/tests/01_ELECTRICAL.md) |
| Tc | Superconducting critical temperature of the NbN: ≈ 7.8–8 K. | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
| C_RN | RF-to-wire capacitance used in the sim 10 pickup model. The letters are not expanded in the repo. No value in the two designated sources. | [DESIGN_LOG](DESIGN_LOG.md) (step 10) |
| Common-mode current | RF current that flows the same way in both SNSPD leads. Each slot lead collects ≈ 44.5 µA (E2) and ≈ 28.6 µA (E1) at 28 MHz over the 2.24 mm of lead between the RF rails (`sim/out/10c_mirror_thickness/summary.json`, `al100_inlaid`; 2-D upper bound). | [02_CRYOGENIC](fab/tests/02_CRYOGENIC.md) |
