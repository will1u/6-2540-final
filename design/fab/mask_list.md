> **Claude-authored.** Exposure list for the v3 dies: 10 × 10 mm trap dies `gds/trap_die_v3_A30.gds` (A30), `gds/trap_die_v3_B60.gds` (B60), `gds/trap_die_v3_NODET.gds` (plain trap, NODET) and the 10 × 2.5 mm test die `gds/test_die_v3.gds` (TEST). v3 has no indium tin oxide (ITO): layers 24, 30 and 31 are retired. Each R&D run writes a small block of dies from `gds/run_<name>.gds` (`make_run.py`, section 3); `gds/wafer_v3.gds` is the full-wafer reference layout. One row per GDS layer. The layer meanings are in `gds/layer_map.md`; steps are in `TRAVELER.md`. Exposed areas were measured from the v3 GDS with gdstk on 2026-11-07. Resist products and tool settings are **[verify]** against what MIT.nano stocks.

# Mask / exposure list

The MLA150 is maskless, so "polarity" here means **which area the tool exposes**:
- **drawn**: expose the GDS polygons.
- **inverted**: expose everything in the job field except the polygons. This is the MLA job "invert" option [verify the option name, and that on a wafer job it inverts over the whole wafer rather than the design bounding box].
- **Field**: the exposed area per die (trap die 10 × 10 mm = 100 mm²; test die 10 × 2.5 mm = 25 mm²), given as A30 / B60 / TEST where they differ. "Dark field" means only a small area is exposed.

**Runs, not production.** At MIT.nano each run is a full 100 mm wafer with only a small central block written (section 3), e.g. 8 dies. The MLA is maskless, so the die mix and the designs can change from run to run at no mask cost.

NODET dies have nothing on L20 and L22. On L10, L40, L45 and L50 they match A30, minus the SNSPD pad features.

## Main table

| GDS layer | Name | Step | Write tool | Resist (tone, thickness) | Expose | Field (exposed area per die) | Align to | Critical dimension | Overlay tolerance | Export job |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MARK | 1 | DirectWrite-MLA150 | positive, ~1.3 µm (S1813-class) | drawn | dark field (3 136 µm², all dies) | wafer flat | 4 µm cross arms | – | `L01_MARK` → MLA wafer job |
| 10 | M1 | 3 | MLA150 | positive, 1.3–2 µm; then etch | inverted | 6.2 % (6.22 mm²) A30/B60, 6.1 % NODET / 21.7 % (5.43 mm²) TEST: edge ring + cut-outs | L1 | ≥ 150 µm (pull-back); cut-outs 290 × 250 µm (SNSPD pads), 300 × 300 µm (mark sites) | ±5 µm | `L10_M1` → MLA wafer job, invert |
| 22 | LEAD | 6 | MLA150 (or EBL with PMMA bilayer, no TMAH) | LOR + positive (bilayer lift-off), ~0.5 + 1.3 µm | drawn | dark field (0.079 mm² trap / 0.533 mm² TEST) | L1 | 4 µm lead width; 2 µm EBL-cross arms | **±1 µm** (sets the L22↔L50 overlay; see notes) | `L22_LEAD` → MLA wafer job |
| 20 | NBN | 7 | EBL-Elionix-HS50 | **HSQ, negative**, 50–70 nm | drawn | 1 603 / 2 053 / 11 070 µm² (A30 / B60 / TEST; trap figures include 900 µm² of overlay squares; TEST includes the T8 dose array) | L22 EBL crosses, fallback L1 | **100 nm lines / 100 nm spaces**, ±10 nm | ±2 µm (tab/lead overlap is 20 µm; meander-to-lead gap is 20 µm) | `L20_NBN` → EBL job (section 2) |
| 40 | D2OPEN | 11 | MLA150 | **thick positive ≥ 8 µm** (AZ 10XT / 4620-class) | drawn | 0.333 mm² A30/B60, 0.297 mm² NODET (incl. eight 150 µm fill-to-M1 ground vias, step 22) / 0.287 mm² TEST | L1 | 4 µm cross arms (L50 marks); openings 90–170 µm | ±5 µm (openings have a ≥ 15 µm rim; Au keep-out is 20 µm) | `L40_D2OPEN` → MLA wafer job (thick-resist mode) |
| 50 | AU (mold) | 13 | MLA150 | **AZ nLOF 2070, negative, ≥ 8 µm** | **inverted** | 8.4 % A30/B60/NODET (Au fraction 0.916) / 31.1 % TEST (0.689) | **L40 crosses** (topography through the seed) | **5 µm gaps** (record the bottom width; nLOF is re-entrant); 6 µm leads at 12 µm pitch; 5 µm window rim | **±1 µm** to the meander/window and to the L22 leads | `L50_AU` → MLA wafer job, invert |
| 45 | PROTECT | 16a | MLA150 | thick positive ≥ 10 µm over 6 µm topography | **inverted** (resist stays on the drawn patches) | ~99.6 % A30/B60 (patches 0.357 mm²), ~99.9 % NODET (0.144 mm²) / ~83 % TEST (patches 4.14 mm²) | L40 / L50 | 2.5 µm landing on the 5 µm window rim | ±2 µm | `L45_PROTECT` → MLA wafer job, invert |
| 101 | CHIP | 18 | Diesaw-DAD3240 | – | – | – | L1 / saw camera | 10 × 10 mm trap dies, 10 × 2.5 mm test dies, 200 µm streets | ±25 µm [verify] | dicing map |
| 100 | NOTE | – | not fabricated | – | – | – | – | – | – | **exclude from every job** |

## 1. Notes per layer

- **Alignment strategy.**
  - Align L22 and L40 to the **same L1 marks**; align L50 to the L40 crosses.
  - The critical stack-up is L22 → L1 → L40 → L50. The SNSPD leads run 1.5–1.7 µm inside the centre-DC Au edge near the readout zone [GDS check]. If they end up under the 5 µm gap, the gap etch removes the D2 above them.
  - Budget: MLA overlay ~±0.5–1 µm per layer [verify tool spec], about √3 × that in total.
- **L1 visibility (TRAVELER A1, resolved).** M1 has 300 × 300 µm cut-outs at every mark site, so the L1 crosses are not covered by Al.
- **L10 etch vs lift-off.** Etch (JoVE BCl₃/Cl₂) is preferred for sputtered Al-1%Cu. Hampel lifted off e-beam Al. The inverted wafer job also clears Al from the dicing streets.
- **L22 developer.** The positive-resist developers are TMAH-based, and the NbN is bare at this step. Use the shortest develop and a ≥ 3 min running DI rinse (Toomey 2018), or PMMA bilayer by EBL with MIBK:IPA (no TMAH) [team inference].
- **L22 marks (TRAVELER A2, resolved).** 20 µm crosses with 2 µm arms: on trap dies at (0, ±700) and (600, ±700) around the readout zone, and on every die one cross at each mark site (90 µm −x of the L1 cross). Plus the 15 µm overlay squares at the mark sites.
- **L50 plating area.** Keep the wafer-edge cathode contacts free of resist: with an inverted job the edge would otherwise be exposed and the negative nLOF would stay there, so leave those spots out of the job or clear them by hand [verify]. Plated area ≈ 0.92 cm² per trap die and ≈ 0.17 cm² per test die, ≈ 5.9 cm² per 8-die run [team calc].
- **L45 PROTECT (TRAVELER A3, now drawn in the GDS by `make_chip.py` and `make_test_die.py`).** GDS polarity: drawn = resist kept. Positive resist, so the MLA exposes everything except the patches (**inverted**). Contents:
  ```
  trap die:  offset(M1 bond openings, +10 µm)
           ∪ SNSPD-lead branch region at the left end, x = −4835 … −4430, |y| ≤ 330
             (SNSPD pads, their D2 openings, and where the L22 leads leave the centre-DC lead)
           ∪ offset(readout window, +2.5 µm)   ← essential in v3: no ITO, so this is all that keeps the gap etch out of the window SiO₂
  test die:  offset(every D2 opening, +10 µm) ∪ T3, T4, T4b, T8 boxes
  ```
  The L40 alignment crosses and the mark sites are not protected: they are not needed after step 13. The fill-to-M1 ground vias (step 22) need no L45 either: the plated Au ground fill covers them, so the Au itself masks the gap etch there. T1, T2 and T6 are left open so they see the gap etch.
- **Mixed die types on one wafer.** A run GDS (or `wafer_v3.gds`) places all its die types, so every MLA layer is a single job. The die types differ in L20, L22, L40, L45 and L50. On a trap-only run (`R1_TRAP`), skip the L20 and L22 jobs entirely (TRAVELER section A).

## 2. EBL job for layer 20 (NBN)

| Item | Setting |
|---|---|
| Source | Layer 20 of the run GDS. For `run_R1_FULL.gds`: 2 A30 + 2 B60 trap meanders; on each of the 2 test dies T4, T4b, the T3 bar and the **T8 dose array** (7 meanders); plus the 15 µm overlay squares at the mark sites. **Boolean-OR the polygons within each datatype first** (datatype 0 = nominal dose; T8 uses datatypes 1–7, see Dose). Each meander is 301 abutting rectangles (150 lines, 149 turn-arounds, 2 tabs); merged polygons avoid double exposure at shared edges |
| Conversion | Elionix pattern format (WecasConverter, or BEAMER if licensed [verify]) |
| Field | Centre one write field on each meander so it is never split across fields. Extent: A30 meander + tabs ≈ 70 × 36 µm; B60 ≈ 100 × 36 µm. Use a 100–300 µm field [verify] |
| Beam | Low current / fine step for the meanders (≤ 5 nm beam step [verify]); a coarser, faster setting for the tabs, T3 bars and overlay squares |
| Dose | Najafi 2015: 70 nm HSQ at 30 keV, 700–850 µC/cm² (Raith 150). Dose scales roughly with kV [inference]: ~1.2–1.4 mC/cm² at 50 kV, ~2.3–3.5 mC/cm² at 100–125 kV. **Confirm the HS50's kV.** W2 matrix: 0.6–4 mC/cm² in 10 % steps, plus line-width variants 80 / 90 / 100 / 110 nm. **On the device wafer**, set datatype 0 to the dose W2 picks and give T8 datatypes 1–7 the factors 0.80 / 0.87 / 0.93 / 1.00 / 1.07 / 1.13 / 1.20 × that dose (`DOSE_FACTORS` in `make_test_die.py`). SEM T8 after step 7, then compare 2-wire R and cold Isw. The next run's nominal dose comes from this array. |
| Proximity | The meander is a 50 %-fill block in an empty field, so the outer few lines get less backscatter dose and come out narrower [inference]. Fix with BEAMER PEC, or a dose ramp on the outer ~10 lines. Najafi used dummy lines outside the detector, but here dummy NbN would sit under the window; prefer PEC |
| Exposure time | `run_R1_FULL`: 0.030 mm² in total. At 1.2–3.5 mC/cm² that is 0.36–1.05 µC, i.e. **~6–18 min at 1 nA** with the fine beam, plus per-die registration (8 dies) and stage moves [team calc; beam current verify]. The full `wafer_v3` is smaller (39 trap dies with SNSPDs), still ~0.3 mm², i.e. about an hour or more. |
| Registration | Per die, on the L22 crosses: trap dies use the four crosses at (0, ±700), (600, ±700) around the readout zone; test dies use the four mark-site crosses (T4/T4b are 1–2 mm from them) |
| Development | Salty NaOH/NaCl, ≥ 3 min running DI rinse (TRAVELER step 7) |

## 3. R&D runs (`make_run.py`) and the full-wafer reference

- **Run layouts.** `gds/make_run.py` writes `run_<name>.gds` (top cell `RUN_<NAME>`), `run_<name>_map.csv` and a PNG. Each one is a small block of dies at the centre of a 100 mm wafer, with 200 µm streets; each column stacks its dies at their own heights (10 mm trap dies, 2.5 mm test dies), as in `wafer_v3`. Presets (edit `RUNS` in the script for others):

  | Run | Dies | Block | Use |
  |---|---|---|---|
  | `R1_TRAP` | 6 NODET + 2 TEST_TRAP (T1, T2, T6 only; `make_test_die.py --trap-only`) | 20.2 × 33.1 mm | Run 1a, chosen first. Uses only L1, L10, L40, L50 and L45; no EBL. Jobs and areas are in `RUNSHEET_R1_TRAP.md`. |
  | `R1_FULL` | 2 A30 + 2 B60 + 2 NODET + 2 TEST | 20.2 × 33.1 mm | Full stack with every variant and a dose array. ~6–18 min of EBL. |

- **Why a full wafer with a small block rather than a piece:**
  - The ≥ 8 µm plating mold and ≥ 10 µm protect resist build edge beads on small pieces.
  - Plating needs cathode contact at the wafer edge.
  - Use pieces only for short loops (TRAVELER section E).
- **Orientation.** Trap axis = wafer x. Align it to the primary flat so the streets follow the Si cleave directions; that keeps scribe-and-cleave possible as an alternative to the saw for a few dies [verify what the MLA and saw expect].
- **Die IDs.** `run_<name>_map.csv` lists `die, type, x_centre_um, y_centre_um, row, col`, with IDs like `R1_FULL-03`. Use the same IDs in every log (process checks, test plan).
- **Changing the next run.** Edit the die generators, re-run `make_chip.py` (`--det60`, `--nodet`) and `make_test_die.py`, then `make_run.py`. Record the run name and the generator versions in the traveler header.
- **Full-wafer reference.** `gds/wafer_v3.gds` (`make_wafer.py`) places 56 dies (25 A30, 14 B60, 17 TEST) inside a 45 mm radius, each column repeating [A30, B60, A30, TEST]. It is only needed if a later run goes to many dies. To crop it, keep the cell references for chosen rows and columns of `wafer_v3_map.csv` at unchanged coordinates.

## 4. Export checklist (per job)

- [ ] Layer isolated; NOTE (100) and CHIP / wafer outline (101) excluded
- [ ] Polarity / invert set per the main table
- [ ] Run GDS chosen (`run_<name>.gds`) and the same die set used for every layer, the EBL job and the dicing map
- [ ] Alignment mark coordinates entered (die coordinates, add the die centre from `run_<name>_map.csv`): L1 crosses on trap dies at (±2150, ±1080), on test dies at (−1700, ±1080) and (4300, ±1080) µm. L40 crosses 60–84 µm from each L1 cross: toward the die centre line on trap dies, +y on test dies. For global alignment use marks on two dies far apart in the chosen set [verify the MLA procedure]
- [ ] Overlay verniers / check squares (15 µm squares, one per layer at each mark site) inspected after develop
