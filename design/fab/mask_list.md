> **Claude-authored.** Exposure list for the v4 dies: 10 × 10 mm trap dies `gds/trap_die_v4_A30.gds` (A30), `gds/trap_die_v4_B60.gds` (B60) and `gds/trap_die_v4_NODET.gds` (NODET, plain trap); the 10 × 10 mm SNSPD-only die `gds/snspd_die_v4.gds` (SNSPD); and the 10 × 2.5 mm test dies `gds/test_die_v4.gds` (TEST) and `gds/test_die_v4_TRAP.gds` (TEST_TRAP), which are not in R1_ONE. Each run writes a block of dies from `gds/run_<name>.gds` (`make_run.py`, section 3). The run for the one wafer is R1_ONE, `gds/run_R1_ONE.gds` (decision 2026-11-12). Layers 24, 30, 31 and 45 are retired and must be empty. Areas come from [measured_v4.md](../gds/measured_v4.md), which carries the file hashes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Mask / exposure list

[Fab overview](README.md) · [Traveler](TRAVELER.md) · [Open decisions](OPEN_DECISIONS.md)

**Electrode Au is open.** Two exposure jobs for layer 50 have equal standing: **E1** (Ti 10 nm / Au 350 nm lift-off, layer 50 exposed drawn in positive resist over LOR) and **E2** (6 µm plated Au, layer 50 exposed inverted in AZ nLOF 2070 as the plating mold). Both are written below. The 360 µm pad pitch is generated and validated, and its adoption by the team is pending ([open decisions](OPEN_DECISIONS.md#design-choices)).

The MLA150 is maskless, so "polarity" here means **which area the tool exposes**:

- **drawn**: expose the GDS polygons.
- **inverted**: expose everything in the job field except the polygons. This is the MLA job "invert" option [verify the option name, and that on a wafer job it inverts over the whole wafer rather than the design bounding box].
- **Field**: the exposed area per die (trap die 10 × 10 mm = 100 mm²; test die 10 × 2.5 mm = 25 mm²).

**Runs, not production.** At MIT.nano each run is a full 100 mm wafer with only a small central block written (section 3). R1_ONE has 9 dies in one 3 × 3 block. The MLA is maskless, so the die mix can change from run to run at no mask cost.

NODET dies have nothing on layers 10, 20, 22 and 40. On layer 50 they match A30 with the SNSPD leads and pads removed from the window area; the pads and the ground fill are on every trap die. In R1_ONE the NODET dies carry layers 1 and 50 only. They receive the blanket films of steps 4, 5 and 8 (spacer, NbN, cap), which have no mask job; see [run plan](RUN_PLAN.md#can-all-dies-share-one-wafer).

## Main table

### Exposure setup

Listed in process order. "Runs" gives the runs that use each job.

| Order | Layer | Name | Step | Tool | Resist | Expose | Runs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 + 10 | MARK + M1 (Al local mirror and marks), one job | 3 | DirectWrite-MLA150 | LOR + positive, one resist for the Al lift-off [verify thicknesses] | drawn | R1_ONE (all dies; NODET: layer 1 only) |
| 2 | 10 | M1 (Al local mirror, raised), same exposure as order 1; no recess etch | 3 | MLA150 | as order 1 | drawn | R1_ONE (A30, B60, SNSPD-only) |
| 3 | 22 | Ti 5 nm / Au 50 nm contacts and EBL marks (was Ti 10 / Au 350 nm) | 6 | MLA150 (or EBL with PMMA bilayer, no TMAH) | LOR + positive (bilayer lift-off), ~0.5 + 1.3 µm | drawn | R1_ONE (A30, B60, SNSPD-only) |
| 4 | 20 | NBN | 7 | EBL-Elionix-HS50 | **HSQ, negative**, 50–70 nm | drawn (datatype 0); datatypes 1–7 = dose array on the SNSPD-only die's cells D1–D8 | R1_ONE |
| 5 | 40 | openings: 110 nm SiO₂ (contacts) and 348 nm SiO₂ (mirror via) | 11 | MLA150 + RIE | thin positive, ~1.3 µm [verify] | drawn | R1_ONE |
| 6a | 50 | AU, branch E1 (lift-off) | 12–14 (E1) | MLA150 | LOR + positive [verify thicknesses] | **drawn** | R1_ONE; optional second wafer (layer 50 only) |
| 6b | 50 | AU, branch E2 (plating mold) | 12–14 (E2) | MLA150 | **AZ nLOF 2070, negative, ≥ 8 µm** | **inverted** | R1_ONE; optional second wafer (layer 50 only) |
| – | 101 | CHIP | 18 | Diesaw-DAD3240 | – | – | dicing map |
| – | 100 | NOTE | – | not fabricated | – | exclude from every job |

Jobs 6a and 6b are alternatives. Run one branch only.

Retired layers, no job: 24 (M1 via), 30 (top ITO), 31 (buried ITO), 45 (protect). There is no layer-45 protect job and no thick-resist 10 µm opening job in v4.

### Dimensions and alignment

| Layer | Align to | Critical dimension | Overlay |
| --- | --- | --- | --- |
| 1 | wafer flat (first layer) | crosses 100 µm long, 4 µm arms (trap and SNSPD-only dies at (±4300, ±4830)); written in Al with layer 10 | – |
| 10 | L1 | Al strip 40 µm wide at x = 0, 200 µm at the mirror-via branch (measured_v4 §7 gives 250 µm at the via: see contradictions in the report) [verify]; |y| ≤ 20 µm under the centre DC; no Al under the RF rails; 100 nm, raised | ±5 µm [verify] |
| 22 | Al marks, seen through the SiO₂ [verify on the MLA150] | contact pads 27 × 7 µm at x = 143 … 170 µm (A30); B60 at x = 126.5 … 153.5 µm | **±1 µm** (sets the overlay of the layer-40 openings on these pads) |
| 20 | L22 EBL crosses at (−60, ±700) and (540, ±700) µm on the A30/B60 dies; at (xc ± 300, yc ± 700) µm per cell on the SNSPD-only die [verify]; fallback L1 | **130 nm lines / 70 nm spaces** (v3.1, unchanged in v4); tolerance from W2 [verify]; T9 also has 100/100, 140/60 and 300/300 nm | ±2 µm |
| 40 | Al marks, seen through the SiO₂ [verify on the MLA150] | mirror via 100 × 100 µm, through 348 nm; SNSPD contacts 18 × 3 µm through 110 nm (A30 x = 148 … 166 µm, B60 131.5 … 149.5 µm); L40 crosses 60 × 24 µm | **≤ 1 µm** to layer 22, because the contact openings have 1 µm of drawn margin inside the Ti/Au pad and the Au lead [verify the overlay on the MLA150]. Replaces the ±5 µm carried from v3 |
| 50 | R1_ONE: Al marks (layer 1) seen through the SiO₂ [verify]. E1: L1 marks [verify]; E2: L40 crosses seen through the seed on the detector dies [verify], L1 on R1_TRAP (no L40 there) | 5 µm gaps (E2: record the bottom width; nLOF is re-entrant); 5 µm SNSPD leads in the slot at \|y\| = 5 µm; 120 × 200 µm edge pads at 360 µm pitch | ±1 µm to the L22 leads and the window [verify] |
| 101 | L1 / saw camera | 10 × 10 mm trap dies, 10 × 2.5 mm test dies, 200 µm streets | ±25 µm [verify] |
| 100 | – | – | – |

### Area estimates and export names

Runs (R1_ONE is the run; the others are superseded 2026-11-12 and kept for history):

| Run or die | Au, layer 50 (cm²) | Layer 20 (mm²) | Status |
| --- | --- | --- | --- |
| R1_ONE (one wafer, 9 dies) | 8.27 (8.2685) [from `check_run.py` output, FACTS; not yet in measured_v4.md] | 0.0372 [verify merged; datatype split not measured] | Next run |
| SNSPD-only die, per die (`snspd_die_v4`) | 0.937 | 0.013724 | New 2026-11-12 |
| R1_TRAP (6 NODET + 2 TEST_TRAP) | 5.9166 | none | Superseded 2026-11-12 by R1_ONE |
| R1_FULL (2 A30 + 2 B60 + 2 NODET + 2 TEST) | 5.7355 | 0.04963 | Superseded 2026-11-12 by R1_ONE |

Layers 1, 10, 22 and 40 for R1_ONE are not yet in [measured_v4.md](../gds/measured_v4.md). Rerun `measure_dies.py` before quoting them [verify].

Values are copied from [measured_v4.md](../gds/measured_v4.md) (sections 2, 3, 4, 7 and 8). Its section 1 lists the SHA-256 prefixes (first 16 hex digits) of each GDS. On 2026-11-09 the `test_die_v4.gds` row showed `d7c25bd035d00e36`, as expected. Prefixes for the files used here: A30 `1d4abbf88105ec23`, B60 `89e4dc808d2ceabd`, NODET `d5b32c23924d7d58`, TEST `d7c25bd035d00e36`, TEST_TRAP `b1247c80ce2b16c4`, R1_TRAP `281f6222285178c6`, R1_FULL `d71022c494349eb1`.

| Layer | Trap die A30 / B60 / NODET | Test die TEST / TEST_TRAP | Run R1_TRAP / R1_FULL (superseded 2026-11-12 by R1_ONE) | Export job |
| --- | --- | --- | --- | --- |
| 1 | 0.0031 mm² / 0.0031 mm² / 0.0031 mm² | 0.0031 mm² / 0.0031 mm² | 0.0251 mm² / 0.0251 mm² | `L01_MARK` → MLA wafer job |
| 10 | 0.1423 mm² / 0.1430 mm² / none | 0.7108 mm² / none | none / 1.9922 mm² | `L10_M1` → MLA wafer job, drawn |
| 20 | 1928.1 µm² / 2614.5 µm² / none (datatype 0, merged) | 13074.0 µm² (datatype 0); 1028.1 µm² each for datatypes 1–7 / none | none / 35233.1 µm² (datatype 0); 2056.1 µm² each for datatypes 1–7 | `L20_NBN` → EBL job (section 2) |
| 22 | 0.0021 mm² / 0.0021 mm² / none | 1.0119 mm² / none | none / 2.0322 mm² | `L22_LEAD` (Ti/Au contacts) → MLA wafer job, drawn |
| 40 | 0.0114 mm² / 0.0114 mm² / none | 0.6526 mm² / none | none / 1.3507 mm² | `L40_OPEN` → MLA wafer job, drawn |
| 50 | 91.3138 mm² (0.91314 cm²) / 91.3132 mm² (0.91313 cm²) / 91.4720 mm² (0.91472 cm²) | 12.6739 mm² (0.12674 cm²) / 21.4139 mm² (0.21414 cm²) | 591.6597 mm² (5.9166 cm²) / 573.5457 mm² (5.7355 cm²) | `L50_AU` E1 drawn or E2 inverted |
| 50, E2 exposed area (inverted) | 0.0869 cm² / 0.0869 cm² / 0.0853 cm² (complement in the 1.0 cm² die outline) | 0.1233 cm² / 0.0359 cm² (complement in the 0.25 cm² outline) | 94.0760 cm² / 94.2571 cm² (complement in the 100 cm² bounding square; see note) | E2 mold job, inverted |
| 45 | retired (empty) | – | – | none |
| 101 | – | – | – | dicing map |
| 100 | – | – | – | **exclude from every job** |

The run complement is taken in the 100 mm square bounding box, not in the wafer disc (the layer-101 disc is 78.53 cm²). Whether the inverted job covers the disc, the square or the job field is [verify with the MLA].

**Plated area (E2).** The Au written on layer 50 is the plated area: 0.913 cm² per A30 or B60 die, 0.915 cm² per NODET, 0.127 cm² per TEST and 0.214 cm² per TEST_TRAP. Per run: 5.917 cm² for R1_TRAP (6 NODET + 2 TEST_TRAP) and 5.735 cm² for R1_FULL (2 A30 + 2 B60 + 2 NODET + 2 TEST). These sums match measured_v4.md, section 3. For R1_ONE the plated area is 8.27 cm² (run table above); the two superseded sums are kept for history.

Percentages and totals in the earlier v3 estimates are superseded by the table above.

## 1. Notes per layer

- **Alignment strategy.**
  - Align L10, L22 and L40 to the **L1 marks** (the wafer job's marks). The L1 marks are now Al, written with layer 10 (see "L1 visibility"), so on the wafer they are seen through the SiO₂ [verify on the MLA150].
  - L20 aligns to the L22 EBL crosses at (−60, ±700) and (540, ±700) µm (A30 and B60) and to the four crosses per cell on the SNSPD-only die [verify]; it falls back to L1.
  - L50 on R1_ONE aligns to the Al marks (layer 1, seen through the SiO₂) [verify]. On the detector dies, E2 may also use the L40 crosses seen through the seed [verify on the v4 crosses]; E1 uses L1 and the L40 crosses [verify overlay].
  - Overlay chain: L22 → L1 → L40 → L50. The SNSPD leads run in the centre-DC slot at \|y\| = 5 µm and end at the layer-22 contact pads. Their position is checked by `check_chip.py` (SNSPD leads inside the slot, L40 contacts inside the leads).
  - Budget: MLA overlay ~±0.5–1 µm per layer [verify tool spec].
- **L1 visibility.** The Al local mirror is drawn only under the detector and its leads (|y| ≤ 20 µm, x = −2240 … +268 µm for A30). The L1 marks themselves are written in Al with layer 10 (one exposure, one lift-off), so they are Al crosses on the wafer, not etched Si. No layer-10 mirror polygon sits at a mark site on a trap die [verify].
- **L10 used once.** Layer 10 is exposed once, with layer 1, as the resist for the lift-off of the raised Al. There is no SiO₂ recess etch. There is no second exposure. No dicing-street clearing is needed.
- **L22 developer.** The positive-resist developers are TMAH-based, and the NbN is bare at this step. Use the shortest develop and a ≥ 3 min running DI rinse (Toomey 2018), or PMMA bilayer by EBL with MIBK:IPA (no TMAH) [team inference].
- **L22 marks.** 20 µm crosses with 2 µm arms: on the A30 and B60 dies at (−60, ±700) and (540, ±700) µm around the readout zone; on the SNSPD-only die, four per cell at (xc ± 300, yc ± 700) µm [verify]; on each test die one cross at each mark site (90 µm −x of the L1 cross), plus the 15 µm overlay squares at the mark sites (make_chip.py, SNSPD layers).
- **L50 plating area and cathode.** Plated area (E2): see the table above. Keep the wafer-edge cathode contacts free of resist: with an inverted job the edge would otherwise be exposed and the negative nLOF would stay there, so leave those spots out of the job or clear them by hand [verify].
- **L50 E1 and E2 are alternatives.** Both draw the same layer 50 polygons. E1 exposes them drawn, so the Au lands where they are drawn. E2 exposes everything except them, so the mold is open where the Au plates. Neither is recommended here; the choice is open ([open decisions](OPEN_DECISIONS.md)).
- **L40 openings.** Drawn. Two classes: SNSPD contacts (through the 110 nm SiO₂ cap, onto the Ti/Au contact pads on layer 22) and the mirror ground via (through the 110 nm cap and the 238 nm spacer, 348 nm in total, onto the Al). Over the wires the cap is 160 ± 10 nm, with the HSQ; the contact openings are off the wires, so they cross 110 nm only. The mark crosses on L40 are also drawn. No layer-45 patch is needed: there is no gap etch in v4.
- **Mixed die types on one wafer.** A run GDS places all its die types, so every MLA layer is a single job. In R1_ONE the NODET dies carry layers 1 and 50 only, and every layer job still covers the whole wafer. The optional second wafer exposes layer 50 only ([run plan](RUN_PLAN.md)).

## 2. EBL job for layer 20 (NbN)

### Source

**Setting:** Layer 20 of the run GDS. For `run_R1_ONE.gds` (see section 3 for the dies): 4 A30 and 1 B60 trap meanders, and 16 meanders on the two SNSPD-only dies (8 cells each, D1–D8). That is 21 meanders on 7 dies. The NODET dies have nothing on layer 20. The SNSPD-only cells carry the **dose array** on datatypes 1–7 (see the dose section).

**Boolean-OR the polygons within each datatype first.** Datatype 0 is the nominal dose; datatypes 1–7 are the dose array on the SNSPD-only dies (datatype 4 is unused).

Layer-20 areas by datatype for the dies and runs measured in measured_v4.md (section 4 and section 8). The R1_ONE split by datatype is not measured yet [verify].

| Die or run | Datatype 0 (merged, µm²) | Datatypes 1–7 (merged, µm² each) | Layer 20, all datatypes (merged, mm²) |
| --- | --- | --- | --- |
| A30 (329 polygons) | 1928.1 | – | 0.0019 |
| B60 (329 polygons) | 2614.5 | – | 0.0026 |
| TEST (`test_die_v4`, 2241 polygons on datatype 0) | 13074.0 | 1028.1 | 0.0203 |
| R1_FULL (2 A30 + 2 B60 + 2 NODET + 2 TEST) | 35233.1 | 2056.1 | 0.04963 |
| R1_ONE (4 A30, 1 B60, 2 SNSPD-only, 2 NODET) | [verify: not measured by datatype] | [verify: not measured by datatype] | 0.0372 [verify merged] |
| wafer_v4 (reference) | 307062.0 | 17476.9 | 0.4294 |

Merged polygons avoid double exposure at shared edges. Fracture the semicircles finely (they are 70 nm across); the written radius will not match the drawn one, which is fine.

The meander is v3.1: 130 nm wires, 200 nm pitch, 160 lines, lines 36 µm (A30) or 69 µm (B60) long with rounded end blocks and tapered tabs (`gds/snspd_geom.py`).

### Conversion

**Setting:** Elionix pattern format (WecasConverter, or BEAMER if licensed [verify]).

### Field

**Setting:** Centre one write field on each meander so it is never split across fields. Extent: A30 meander + tabs ≈ 84 × 32 µm; B60 ≈ 117 × 32 µm [team calc, from the earlier v3.1 estimate; recheck against the v4 lines]. Use a 150–300 µm field [verify].

### Beam

**Setting:** Low current / fine step for the meanders (≤ 5 nm beam step [verify]); a coarser, faster setting for the tabs, T3 bars and overlay squares.

### Dose

**Setting:** Najafi 2015: 70 nm HSQ at 30 keV, 700–850 µC/cm² (Raith 150). Dose scales roughly with kV [inference]: ~1.2–1.4 mC/cm² at 50 kV, ~2.3–3.5 mC/cm² at 100–125 kV. **Confirm the HS50's kV.**

W2 matrix: 0.6–4 mC/cm² in 10 % steps, plus line-width variants 100 / 120 / 130 / 140 nm on a 200 nm pitch (v3.1 target 130 / 70 nm).

**On the device wafer**, set datatype 0 to the dose W2 picks. On the SNSPD-only dies, the cells use these factors on that dose: D1 datatype 1 = **0.80**, D2 datatype 2 = **0.87**, D3 datatype 3 = **0.93**, D4 and D5 datatype 0 = **1.00**, D6 datatype 5 = **1.07**, D7 datatype 6 = **1.13**, D8 datatype 7 = **1.20**. Datatype 4 is unused. The factor values are those of `DOSE_FACTORS` in `make_test_die.py` [verify the SNSPD-only die uses the same list]. Measure the cells after step 7 (SEM linewidth, then 2-wire R and cold Isw). The next run's nominal dose comes from this array.

### Proximity

**Setting:** The meander is a 65 %-fill block in an empty field, so the outer few lines get less backscatter dose and come out narrower [inference]. Fix with BEAMER PEC, or a dose ramp on the outer ~10 lines. Dummy NbN would sit under the window in v4, so prefer PEC. In v3.1 the outermost 5 lines on each side (1 µm) and the end blocks lie outside the light footprint, so a narrower outer line costs no light, only switching-current margin.

### Exposure time

**Setting:** `run_R1_ONE` layer-20 area 0.0372 mm² [verify merged]. At 1.2–3.5 mC/cm² the total charge is about 0.45–1.3 µC, i.e. **~7–22 min at 1 nA** with the fine beam, plus per-die registration (9 dies) and stage moves [team calc; beam current verify]. The `wafer_v4` layer-20 area is 0.4294 mm².

### Registration

**Setting:** Per die, on the L22 crosses. Trap dies (A30, B60) use the crosses at (−60, ±700) and (540, ±700) µm around the readout zone. The SNSPD-only dies use the four crosses of each cell, at (xc ± 300, yc ± 700) µm [verify]. Test dies (not in R1_ONE) use the L22 crosses at each mark site [verify which two are used for the T4 and T4b meanders].

### Development

**Setting:** Salty NaOH/NaCl, ≥ 3 min running DI rinse ([step 7](process/02_DETECTOR.md)).

## 3. R&D runs (`make_run.py`) and the full-wafer reference

- **Run layouts.** `gds/make_run.py` writes `run_<name>.gds` (top cell `RUN_<NAME>`), `run_<name>_map.csv` and a PNG. Each one is a block of dies at the centre of a 100 mm wafer, with 200 µm streets. Each column stacks its dies at their own heights (10 mm dies; the superseded runs also had 2.5 mm test dies).

  | Run | Dies (die IDs in `run_<name>_map.csv`) | Block | Layers used | Use |
  | --- | --- | --- | --- | --- |
  | `R1_ONE` | 4 A30 (R1_ONE-01, -03, -05, -07), 1 B60 (-09), 2 SNSPD-only (-02, -08), 2 NODET (-04, -06) | 30.4 × 30.4 mm | all: 1, 10, 20, 22, 40, 50 (NODET: 1 and 50) | The one-wafer run (decision 2026-11-12). Map: `run_R1_ONE_map.csv`. |
  | `R1_TRAP` (superseded 2026-11-12 by R1_ONE) | 6 NODET (R1_TRAP-01, -03, -04, -05, -07, -08) + 2 TEST_TRAP (R1_TRAP-02, -06; T1 and T6 only) | 20.2 × 33.1 mm | **1 and 50 only**; no EBL | Superseded. Was run 1a, chosen first. Sheet: [R1_TRAP](RUNSHEET_R1_TRAP.md) (now the optional second wafer). |
  | `R1_FULL` (superseded 2026-11-12 by R1_ONE) | 2 A30 (R1_FULL-01, -07) + 2 B60 (-03, -08) + 2 NODET (-04, -05) + 2 TEST (-02, -06) | 20.2 × 33.1 mm | all six: 1, 10, 20, 22, 40, 50 | Superseded. Full stack with every variant and the dose array. |

- **Why a full wafer with a small block rather than a piece:**
  - The ≥ 8 µm plating mold and the resist build edge beads on small pieces.
  - Plating needs cathode contact at the wafer edge.
  - Use pieces only for short loops ([qualification](QUALIFICATION.md)).
- **Orientation.** Trap axis = wafer x. Align it to the primary flat so the streets follow the Si cleave directions [verify what the MLA and saw expect].
- **Die IDs.** `run_<name>_map.csv` lists `die, type, x_centre_um, y_centre_um, row, col`. Use the same IDs in every log (process checks, test plan).
- **Changing the next run.** Edit the die generators, re-run `make_chip.py` (A30, `--det60`, `--nodet`) and `make_test_die.py` (and `--trap-only`), then `make_run.py`. Rerun `measure_dies.py` so the numbers here match. Record the run name and the generator versions in the traveler header.
- **Full-wafer reference.** `gds/wafer_v4.gds` (`make_wafer.py`) places 56 dies (25 A30, 14 B60, 17 TEST). It is only needed if a later run goes to many dies.

## 4. Export checklist (per job)

- [ ] Layer isolated; NOTE (100) and CHIP / wafer outline (101) excluded from every MLA and EBL job.
- [ ] Layers 24, 30, 31 and 45 are empty in the exported run GDS (checked by `check_chip.py`, `check_test_die.py` and `measure_dies.py`).
- [ ] On R1_ONE exports: the NODET dies have nothing on layers 10, 20, 22 and 40 [verify that `check_run.py` checks it].
- [ ] Polarity / invert set per the main table (L50 E1 drawn, or E2 inverted; choose one branch).
- [ ] Run GDS chosen (`run_<name>.gds`) and the same die set used for every layer, the EBL job and the dicing map. Die IDs from `gds/run_<name>_map.csv`.
- [ ] Alignment mark coordinates entered (die coordinates plus the die centre from the run map):
  - trap dies: L1 crosses at (±4300, ±4830) µm; L40 crosses at (±4300, ±4758) µm (72 µm inward in y);
  - SNSPD-only die: L1 crosses at (±4300, ±4830) µm; e-beam crosses at (xc ± 300, yc ± 700) µm per cell;
  - test dies (not in R1_ONE): L1 crosses at (−1700, ±1080) and (4300, ±1080) µm; L40 crosses 72 µm in +y from each of those;
  - full detail in [coordinates](LAYOUT.md#alignment-coordinates-used-by-the-recipes).
  - For global alignment use marks on two dies far apart in the chosen set [verify the MLA procedure].
- [ ] Overlay verniers / check squares (15 µm squares, one per layer at each mark site) inspected after develop.
- [ ] Design checks pass on the released files:
  - `cd design/sim && ./run.sh ../gds/check_chip.py trap_die_v4_A30` (and `_B60`, `_NODET`) prints `ALL CHECKS PASS`;
  - `cd design/sim && ./run.sh ../gds/check_test_die.py test_die_v4` (and `test_die_v4_TRAP`) prints `ALL CHECKS PASS`.
  - `cd design/sim && ./run.sh ../gds/check_snspd_die.py` prints `ALL CHECKS PASS`;
  - `cd design/sim && ./run.sh ../gds/check_run.py R1_ONE` prints `ALL CHECKS PASS`.
- [ ] Hash check: the SHA-256 of each GDS used for export matches the table in [measured_v4.md](../gds/measured_v4.md), section 1, first 16 hex digits. If it does not match, the table is stale: rerun `measure_dies.py` before using any number from it. `run_R1_ONE` and `snspd_die_v4` are not in that table yet, so their hashes are not checked there [verify].
