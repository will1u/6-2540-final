> **Claude-authored** run sheet for run 1a, `gds/run_R1_TRAP.gds`. The team chose to run the trap-only process first on 2026-11-02; log that decision in `notes/decisions.md`.
> - This file lists only the steps this run uses, with the changes from the full traveler.
> - Full recipes: [foundation](process/01_FOUNDATION.md), [D2 and Au](process/03_ELECTRODES.md), [packaging](process/04_PACKAGING.md). Original step numbers are retained.
> - **[verify]** marks values not yet checked on the MIT.nano tool.

# Run sheet: R1_TRAP (plain five-wire trap, no SNSPD)

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!important] Before the device wafer
> Complete W3 stress/etch/via qualification, W5 plating and **W7 bond-and-leak**, and confirm facility access. See [Qualification](QUALIFICATION.md). The detector revision adds no EBL work to this trap-only run.

Wafer ID: ________ Start date: ________ Operator: ________ GDS generated (date / `make_run.py` version): ________

## 1. What this run is

- **Wafer:** one 100 mm HR float-zone Si wafer. Only an 8-die block at the centre (20.2 × 33.1 mm; v3 10 × 10 mm trap dies and 10 × 2.5 mm test dies) is written. Dies ([run_R1_TRAP_map.csv](../gds/run_R1_TRAP_map.csv), die-centre coordinates in µm):

  | Die | Type | Centre (x, y) |
  |---|---|---|
  | R1_TRAP-01, -03, -04, -05, -07, -08 | NODET trap die (`trap_die_v3_NODET`, 10 × 10 mm) | (±5100, −11550 / 1350 / 11550) |
  | R1_TRAP-02, -06 | Trap-only test die (`test_die_v3_TRAP`, 10 × 2.5 mm): T1 Au comb, T2 Au/D2/M1 capacitor + M1 pad, T6 Au loop | (±5100, −5100) |

- **Goal:** qualify the trap process (thick SiO₂, plating, gap etch, dicing, packaging) and trap ions on a die with no detector stack. The resulting NODET die becomes the reference for the SNSPD dies in run 1b ([staged-run rationale](../SIMPLIFICATIONS.md#s2-staged-runs-a-plain-trap-run-first-snspd-later)).
- **Stack (bottom to top):**
  - Si;
  - thermal SiO₂ 1.0 µm (both sides);
  - Al-1%Cu 150 nm;
  - PECVD SiO₂ D2, 10.0 µm, directly on the Al;
  - Ti/Au seed;
  - 6 µm plated Au.
  - Gaps are etched to ~0.75 µm above the Al.
  - The ground plane sits 10.0 µm below the Au, which is the `ground_depth` used in every simulation.
- **Skip detector steps 4–8** (spacer, NbN, leads, e-beam, cap). Steps 8a, 8b and 10 are retired in all v3 runs. **No e-beam.** The NbN thermal-budget rules no longer apply, but the Al rule does: ≤ 300 °C after step 3.

### Lithography jobs (MLA150, all on `run_R1_TRAP.gds`)

| Order | Step | Layer | Expose | Resist | Written area (whole run) | Align to |
|---|---|---|---|---|---|---|
| 1 | 1 | L1 MARK | drawn | positive ~1.3 µm | 0.03 mm² | wafer flat |
| 2 | 3 | L10 M1 | **inverted** | positive 1.3–2 µm | Al kept on 6.06 cm²; the edge ring and mark cut-outs are exposed | L1 (±5 µm) |
| 3 | 11 | L40 D2OPEN | drawn | thick positive ≥ 8 µm | 1.82 mm² (M1 bond openings, fill-to-M1 ground vias, T2 M1 pad, L50 alignment crosses) | L1 (±5 µm) |
| 4 | 13 | L50 AU mold | **inverted** | AZ nLOF 2070 ≥ 8 µm | Au plated on 5.93 cm² | L40 crosses (±1 µm) |
| 5 | 16a | L45 PROTECT | **inverted** | thick positive ≥ 10 µm | resist kept on 0.92 mm² (M1 openings + 10 µm) | L40/L50 (±2 µm) |

Export each layer alone. Exclude layers 100 (notes) and 101 (outlines). Enter the mark coordinates as die coordinates plus the die centres above (`mask_list.md` section 4).

## 2. Before the run (short loops on dummy wafers)

Complete these [qualification loops](QUALIFICATION.md) for R1_TRAP:

| Loop | What | Why |
|---|---|---|
| **D2 stress** (part of W3) | 10 µm PECVD SiO₂ in 1–2 µm increments on a dummy Si/D1/Al wafer, with backside compensation; bow after each increment | Bow must stay ≤ 50 µm for the MLA chuck [verify limit] |
| **Gap-etch rate** (part of W3) | The step-16 recipe on that D2 dummy | Etch rate and uniformity, so the stop lands ~0.75 µm above Al |
| **W7 bond-and-leak** | Planned bonds on W3 T2 and plated Au pads | Leakage before/after bonding; pull/shear and tool fit [verify] |
| **W5 plating** | Seed + the real L50 job from `run_R1_TRAP.gds` on a bare-SiO₂ dummy, plated to 6 µm | Current for this 5.93 cm² plated area, thickness map, gap profile |

Facility questions to settle first ([full list](QUALIFICATION.md#facility-confirmations)):

- which tools accept wafers with Au on them (steps 15–19 come after plating);
- whether a gold plating tank exists, its chemistry, and its minimum area;
- the order of tool trainings.

NbN questions can wait for run 1b.

## 3. Steps

Step numbers match the [full traveler](TRAVELER.md#f-steps). Only the changes for this run are spelled out.

### 0. Wafer prep and clean

[Full recipe](process/01_FOUNDATION.md#0-wafer-prep-and-clean)

- Piranha, DI rinse. RCA if the furnace requires it [verify]. Scribe the wafer ID.
- Set aside ≥ 2 dummy wafers for the short loops.
- [ ] Done — date: ____ operator: ____

### 1. L1 marks, Si RIE ~1 µm

[Full recipe](process/01_FOUNDATION.md#1-l1-alignment-marks-si-rie-1-µm)

- As in the traveler. Four crosses per die at the mark sites: NODET dies (±4300, ±4830); test dies (−1700, ±1080) and (4300, ±1080), all die coordinates.
- [ ] Done — date: ____ depth: ____

### 2. Thermal oxide D1, 1.0 µm, both sides

[Full recipe](process/01_FOUNDATION.md#2-thermal-oxide-d1-1-µm-both-sides)

- As in the traveler.
- [ ] Done — date: ____ t_ox (5 pts): ____

### 3. M1 Al-1%Cu, 150 nm (L10)

[Full recipe](process/01_FOUNDATION.md#3-m1-al-1cu-ground-plane--mirror-l10)

- As in the traveler: sputter, MLA **inverted**, BCl₃/Cl₂ etch, DI rinse right after.
- **Cut-outs on this run:** only the 300 × 300 µm openings at the mark sites. NODET and the trap-only test die have no SNSPD-pad cut-outs.
- Purpose here is RF ground only; there is no mirror role in this run.
- From now on: **≤ 300 °C**.
- [ ] Done — date: ____ t_Al: ____ Rsq (witness): ____

### 9. D2, 10.0 µm PECVD SiO₂, stress-balanced

[Full recipe](process/03_ELECTRODES.md#9-d2-10-µm-pecvd-sio₂-in-increments-stress-balanced)

- **Change:** D2 goes **directly on M1**; there is no spacer or cap.
- Same increments and backside interleave as in the traveler, with the bow plan taken from the D2 short loop.
- **Target:** 10.0 ± 0.5 µm; |bow| ≤ 50 µm [verify]; no cracks.
- [ ] Done — date: ____ increments: ____ bow log: ____ t_D2: ____

### 11. L40 D2 openings

[Full recipe](process/03_ELECTRODES.md#11-l40-d2-openings-pads-m1-bond-openings-fill-to-m1-ground-vias-l50-alignment-crosses)

- **Change:** etch depth is ~10.0 µm over M1 (no cap or spacer), so ~28 min at 360 nm/min plus 10–15 % over-etch, in ≤ 5 min segments [verify rate].
- Openings:
  - the four M1 bond openings per NODET die;
  - the eight 150 × 150 µm fill-to-M1 ground vias per NODET die (DESIGN_LOG step 22); the Au ground fill plates over them in step 14;
  - the T2 M1 pad on the test dies;
  - the L50 alignment crosses at the mark sites.
- The crosses sit over the M1 cut-outs, so the over-etch continues into D1 there. That only deepens the alignment topography, which is fine.
- **Inspect:** Dektak depth; bright Al at each bond opening and each ground via.
- [ ] Done — date: ____ etch time: ____ depth: ____

### 12. Plating seed Ti 15 nm / Au 50 nm

[Full recipe](process/03_ELECTRODES.md#12-plating-seed-ti-15-nm--au-50-nm-ptb)

- As in the traveler, **including the in-situ Ar pre-clean** of the Al at the via floors and the sidewall-coverage note. No SNSPD pads to worry about.
- [ ] Done — date: ____

### 13. L50 plating mold (nLOF ≥ 8 µm, inverted)

[Full recipe](process/03_ELECTRODES.md#13-l50-plating-mold-negative--8-µm)

- As in the traveler. Align to the L40 crosses (±1 µm). Leave the cathode contact points at the wafer edge free of resist.
- **Inspect:** 5 µm gap lines clean down to the seed; record the gap width at the bottom.
- [ ] Done — date: ____ t_resist: ____ overlay: ____

### 14. Au electroplating, 6.0 µm

[Full recipe](process/03_ELECTRODES.md#14-au-electroplating-6-µm)

- **Plated area:** 5.93 cm² for the whole run (6 NODET at ~0.92 cm² + 2 test dies at ~0.21 cm²) plus any open edge contact. Use the current calibrated on W5 [verify the bath's minimum area].
- Plate in two halves and measure between them.
- **Target:** 6.0 ± 0.5 µm; no nodules.
- [ ] Done — date: ____ I / t: ____ thickness: ____

### 15. Strip, descum, seed removal

[Full recipe](process/03_ELECTRODES.md#15-strip-descum-seed-removal)

- As in the traveler: NMP strip, O₂ + F descum, Ar ion etch of the Au seed, F-plasma etch of the Ti.
- **Inspect:**
  - every electrode isolated: > 100 MΩ to its neighbours at 10 V, probing the pad rows;
  - Au roughness (AFM).
- [ ] Done — date: ____ Ar time: ____ F time: ____ isolation: ____

### 16a. Protect resist (L45, inverted)

[Full recipe](process/03_ELECTRODES.md#16a-protect-resist-l45)

- **Covers only the M1 bond openings + 10 µm** on the NODET dies and the T2 M1 pad on the test dies. T1, T2 and T6 stay open on purpose.
- [ ] Done — date: ____

### 16. Au-masked D2 gap etch

[Full recipe](process/03_ELECTRODES.md#16-au-masked-d2-gap-etch)

- **Change:** target the stop at ~0.75 µm above M1, so etch ~9.25 µm (~26 min at 360 nm/min [verify on the short loop]).
- Etch in segments and check depth in the T1 comb gaps.
- No BOE undercut.
- **Inspect:** SEM on a sacrificial die or the dummy: gaps cleared, no Au redeposition bridges. Strip the 16a resist.
- [ ] Done — date: ____ etch time: ____ depth: ____

### 17. Room-temperature wafer-level test

[Full recipe](process/04_PACKAGING.md#17-room-temperature-wafer-level-electrical-test-before-dicing)

- [electrical protocol](tests/01_ELECTRICAL.md). Only these apply:
  - **a1:** RF leakage, 300 V;
  - **a2:** DC leakage, 50 V, > 100 MΩ;
  - **a3:** T6 continuity;
  - **a4:** T2 capacitor;
  - **a5:** T1 comb;
  - **a13:** ground link, GND-n ↔ M1-n < 10 Ω (step 22 vias).
- Detector tests a6–a8 and a12 do not apply. a9/a11 are retired ITO tests. The “Dietl 2025” attribution of draft leakage limits remains **[verify]** ([source check](OPEN_DECISIONS.md#source-and-model-checks)).
- Record per die ID.
- [ ] Done — date: ____ yield: ____

### 18. Protect, dice, strip

[Full recipe](process/04_PACKAGING.md#18-protect-dice-10--10-mm-trap-dies-10--25-mm-test-dies-strip)

- As in the traveler. Only the 8-die block needs cutting: 3 x-cuts (x = −10 200, 0, +10 200 µm ± street) and 5 y-cuts at the block edges and between the stacked dies (the trap-die / test-die row heights are the same in both columns, so every cut runs straight through; positions from [run_R1_TRAP_map.csv](../gds/run_R1_TRAP_map.csv)).
- [ ] Done — date: ____ chipping: ____

### 19. Package

[Full recipe](process/04_PACKAGING.md#19-package)

- As in the traveler, without the SNSPD pads.
- Bond map: [trap_die_v3_NODET_pads.csv](../gds/trap_die_v3_NODET_pads.csv) — 36 signal pads (RF, C, TL1–8, TR1–9, BL1–8, BR1–9), plus GND-1…4 on the Au fill and M1-1…4 on the Al (Al wedge wire).
- **Bond ≥ 2 GND spots to carrier ground.** The eight ground vias tie the Au fill to the Al on chip (step 22). Bond ≥ 1 M1 opening as well, as a backup; if step 17 found the fill-to-M1 link open, the M1 bond is required.
- RF capacitance (a10) after packaging.
- [ ] Done — date: ____ die used: ____ carrier: ____

## 4. First trapping on a NODET die: expected values

From DESIGN_LOG steps 14 and 19 (`sim/out/12_log_v3_NODET.txt`, waveforms in `sim/out/12_final_chip/trap_die_v3_NODET/`; identical to the v2 numbers):

- **Drive:** 53 V at 28 MHz → radial ~2.98 MHz RF-only, q ≈ 0.30, depth ≈ 52 meV.
- **Loading zone,** GDS (−300, 0): height 50.08 µm; axial 0.80 MHz; radial 2.89 / 2.97 MHz; radial axes tilted ~10°; max |V| 9.05 V.
- **Readout zone,** GDS (300, 0): height 50.09 µm. There is no window on this die, so no recess correction.
- **Transport between them:** 61 steps; max |V| 7.33 V; ≤ 1.59 V per 10 µm step.
- **Measurements that become the run-1b reference:**
  - secular frequencies against these numbers;
  - micromotion compensation at both zones and its drift;
  - heating rate at both zones;
  - transport.

## 5. What carries over to run 1b

Record these as the starting calibration for run 1b:

- D2 recipe and bow plan;
- L40 calibration (adjust depth for spacer/cap on R1_FULL);
- plating current;
- seed-removal times;
- gap-etch calibration and stop height (adjust time for full-stack thickness);
- dicing settings;
- the leakage numbers.

Run 1b adds **steps 4–8 and the e-beam**, with current T8 dose and T9 geometry arrays. Steps 8a, 8b and 10 remain retired. Complete [detector reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts) before export.
