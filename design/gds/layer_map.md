# Layer map: trap_die_v4 (A30 / B60 / NODET), snspd_die_v4, run_R1_ONE, test_die_v4 (not in R1_ONE), wafer_v4

> **Claude-authored.** Generated alongside `make_chip.py`, `make_test_die.py` and `make_wafer.py`.
> - Units are µm; the GDS database unit is 1 nm.
> - Top cells: `TRAP_DIE_V4_A30`, `TRAP_DIE_V4_B60`, `TRAP_DIE_V4_NODET`, `TEST_DIE_V4`, `TEST_DIE_V4_TRAP`, `SNSPD_DIE_V4` (the SNSPD-only die, new 2026-11-12) and `WAFER_V4`. The run file `RUN_R1_ONE` (the next run) is listed below [verify the top cell name in the file].
> - **v4 (2026-11-08, DESIGN_LOG step 25): local-mirror architecture** (team decision; `notes/decisions.md`). No die-wide Al, no 10 µm D2, no gap etch. The Au electrodes sit on Si / 1.0 µm thermal SiO₂ / 238 nm PECVD SiO₂ spacer / 110 nm PECVD SiO₂ cap (160 ± 10 nm over the wires, with the HSQ). The Al is a raised 100 nm local mirror under the centre DC (decision 2026-11-12; was inlaid). Off the wires the SiO₂ between Au and Al is 348 nm. The SNSPD leads are Au in a slot along the centre DC. A30 and B60 (60 × 30 µm window) both kept.
> - `TRAP_DIE_V4_NODET` (`make_chip.py --nodet`, the R1_TRAP die) uses only layers 1 and 50, plus 100/101: Au on thermal SiO₂ over high-resistivity Si.
> - **The test dies are v4** (`test_die_v4`, `test_die_v4_TRAP`; DESIGN_LOG step 35): the same thin stack, each meander on its own local Al mirror. They are **not in R1_ONE** (files kept). The v3 test dies are in `archive_v3_baseline/`.
> - R&D run layouts: `RUN_R1_ONE` (`make_run.py R1_ONE`; the next run, one wafer of nine dies, decision 2026-11-12) and the superseded `RUN_R1_TRAP` and `RUN_R1_FULL` (kept), which reference these die cells. The SNSPD-only die `SNSPD_DIE_V4` is written by `make_snspd_die.py`.
> - Earlier versions are archived: v1 square die in `archive_v1_square/`, v2 narrow die in `archive_v2_narrow/`, v3 baseline (die-wide Al + 10 µm D2) in `archive_v3_baseline/`.

## Fab layers (v4 trap dies)

| GDS layer | Name | Material / process | Write tool | Drawn = | Aligns to | Notes |
|---|---|---|---|---|---|---|
| 1 | MARK | Al marks, written with layer 10 (one exposure, one lift-off); no Si etch | MLA150 | Al kept where drawn | wafer flat (first layer) | Crosses at 4 sites per die, at (±4300, ±4830) µm. Written in Al, not etched Si (decision 2026-11-12). |
| 10 | M1 | Evaporated Al **100 nm, raised** on the thermal SiO₂ (team decision 2026-11-12; was inlaid from 2026-11-09, 450 nm before that, and 150 nm in v3), **local mirror** (A30, B60, SNSPD-only) | MLA150; one resist for the Al evaporation and the lift-off, exposed together with layer 1; no SiO₂ recess etch | Al kept where drawn | 1 | \|y\| ≤ 20 µm under the centre DC, x = −2240 … +268 (B60: +284.5, 10 µm past the NbN); branch to y = 230 at x = −2240 … −2040 under the Au fill for the ground via. Never under the RF rails (checked). 0.142 mm² per A30 die, 0.143 mm² per B60 die (`measured_v4.md`). |
| 20 | NBN | NbN meander + contact tabs (+ test bars) | EBL (HSQ) | NbN kept | 22 crosses | v3.1 (DESIGN_LOG step 24): 130 nm wires, 200 nm pitch, 160 lines, 36 × 32 µm; tabs at x = 175 … 215 (B60: lines 69 µm, tabs 158.5 … 198.5), \|y\| ≈ 13 … 16, under the solid centre DC. Datatypes 1–7 = dose array on the SNSPD-only die's cells D1–D8 (datatypes 1, 2, 3, 5, 6, 7 used; 4 unused). The T8 dose array on the test dies (not in R1_ONE) is the same idea. |
| 22 | LEAD | Ti 5 nm / Au 50 nm contacts + EBL crosses (lift-off; was Ti 10 / Au 350 nm) | MLA150 | metal | 1 | Before the nanowire etch, as in v3. **v4: no buried leads.** Each contact covers the −x half of an NbN tab and steps into the slot to a 27 × 7 µm pad at x = 143 … 170 (B60: 126.5 … 153.5), y = ±(1.5 … 8.5). |
| 24, 30, 31 | *retired in v3* | – | – | – | – | ITO / via layers of v2. Must stay empty (checked). |
| 40 | OPEN | Openings through the cap (SNSPD contacts, 110 nm, landing on the Ti/Au pads) and cap + spacer (mirror via, 348 nm, landing on Al) | MLA150 + RIE | SiO₂ removed | 1 | Contacts: 18 × 3 µm at x = 148 … 166 (B60: 131.5 … 149.5), y = ±(3.5 … 6.5), ≥ 1 µm inside the Au lead and the Ti/Au pad. Mirror via: 100 × 100 µm at (−2140, 130), enclosed ≥ 25 µm by the Au fill and the Al. Also crosses at the marks. |
| 45 | PROTECT | *retired in v4* | – | – | – | – | No gap etch without D2. Must stay empty (checked). |
| 50 | AU | Electrode Au: E2 6 µm plated or E1 0.35 µm lift-off (**open**) | MLA150 | Au | 1 / 40 crosses | Electrodes, ground fill, pads and (v4) the SNSPD leads. **gds2itvg simulates this layer** (`*_sim.json`). |
| 100 | NOTE | Text | – | – | – | Not fabricated. |
| 101 | CHIP | Die outline / wafer outline | – | – | – | Not written. |

## Process order (v4, A30)

Base SiO₂ (1.0 µm thermal, D1) → 10 + 1 (Al mirror and marks, one exposure, first after the base SiO₂; no Si etch) → SiO₂ spacer 238 nm → NbN 7 nm → 22 (Ti 5 / Au 50 nm) → 20 (e-beam HSQ, CF₄ etch of the NbN) → SiO₂ cap 110 nm → 40 → electrode Au 50 (E1: lift-off; E2: seed, mold, plate, seed removal) → test → dice.

NODET on R1_ONE (shared wafer): base SiO₂ → 1 (Al marks only; no layer 10) → SiO₂ spacer → NbN (blanket, removed by the step-7 etch) → SiO₂ cap (blanket) → 50 → test → dice. [verify the step-7 etch clears the NbN and stops on the spacer]

Optional second wafer (layer 50 only, base SiO₂ only): base SiO₂ → 50 → test → dice. Details: [run sheet](../fab/RUNSHEET_R1_TRAP.md) and `design/fab/variants/LOCAL_MIRROR.md` H.2. Full step list: [traveler](../fab/TRAVELER.md).

## Trap die v4 key coordinates

GDS µm, die centre (0, 0), die 10 × 10 mm.

| Feature | Location |
|---|---|
| Trap axis | y = 0 |
| Readout zone (SNSPD) | (240, 0); window 30 × 30 µm (A30) or 60 × 30 µm (B60, axial × radial) |
| Loading zone | (−240, 0); zones 480 µm apart (step 28), outer DC segments at 120 µm pitch, centres −840 … +840 |
| RF U | rails x = −2000…2000, U bar x = 2000…2060; RF pad (4700, 0) |
| Centre DC | \|y\| ≤ 20. Slot \|y\| < 12.5 from the left end to x = 175 (A30) / 158.5 (B60), 20 µm left of the NbN tabs, so the centre DC is two 7.5 µm halves joined right of the slot; lead to its pad along the top half, turning up at x = −3600 |
| SNSPD leads (A30, B60) | Au 5 µm, centre y = ±5, from x = 170 (B60: 153.5) to x = −4400, then to their pads |
| Centre DC pad | (−4650, 450) |
| SNSPD pads (Au) | (−4750, ±100), 200 × 150 µm |
| Pad rows | top and bottom die edges, y = ±4720, \|x\| = 620…3500, 360 µm pitch (step 29; generated layout validated, team adoption pending beam-access review). `TL1…TL8`, `TR1…TR9`, `BL1…BL8`, `BR1…BR9` in `*_pads.csv` |
| GND bond spots | (±4700, ±1500), side edges |
| Mirror ground via (A30, B60) | (−2140, 130), 100 × 100 µm, just past the RF open end (step 28) |
| L1 / L40 marks | (±4300, ±4830) |
| L22 EBL crosses | (−60, ±700), (540, ±700) |

Electrode numbers match `*_sim.json` and `*_pads.csv`:
- 1 = RF
- 2 = centre DC
- 3–17 = top segments (left → right), 18–32 = bottom segments
- 33/34 = top caps (L/R), 35/36 = bottom caps (L/R)
- grounds: 99 = Au fill; A30 also 97/98 = SNSPD signal/return leads, 96 = window floor (simulation only)

## SNSPD-only die key coordinates (`snspd_die_v4`, R1_ONE)

GDS µm, die centre (0, 0), die 10 × 10 mm. Source: the die specification of 2026-11-12, as built by `make_snspd_die.py`. Pad positions: [snspd_die_v4_pads.csv](snspd_die_v4_pads.csv).

| Feature | Location |
|---|---|
| Detector cells D1–D8 (centre xc, yc) | x = −2700, −900, +900, +2700; y = +1200 (D1–D4), −1200 (D5–D8) |
| Cell direction (dir) | +1 for D1–D4 (leads to the top edge), −1 for D5–D8 (leads to the bottom edge) |
| Layer-20 datatype (dose factor) | D1 1 (0.80), D2 2 (0.87), D3 3 (0.93), D4 0 (1.00), D5 0 (1.00), D6 5 (1.07), D7 6 (1.13), D8 7 (1.20) |
| Readout window (L40 hole in Au) | 30 × 30 µm, centred on (xc, yc) of each cell |
| NbN meander | `meander(xc, yc, 36.0, 32.0, 0.130, 0.200)`; tab points at x = xc − 45 |
| Contact openings (L40) | x = xc − 92 … xc − 74; y = yc + sy·3.5 … yc + sy·6.5 (sy = +1 signal, −1 return) |
| Ti/Au pads (L22) | x = xc − 97 … xc − 70; y = yc + sy·1.5 … yc + sy·8.5 |
| Au leads (L50, 5 µm) | from (xc − 70, yc ± 5) to x = xc − 400 (inner) or xc − 760 (outer), then to the pad row |
| Bond pads (L50, 120 × 200 µm) | 16 pads at y = ±4720 µm; for example D1_S (−3100, +4720), D1_G (−3460, +4720), D8_G (+2300, −4720) |
| Al mirror (L10) per cell | strip x = xc − 370 … xc + 28, y = yc ± 20; branch x = xc − 370 … xc − 170, y = yc − dir·230 … yc + dir·20 |
| Mirror ground via (L40, 100 × 100 µm) | centred (xc − 270, yc − dir·130) |
| E-beam crosses (L22), four per cell | (xc ± 300, yc ± 700) µm; each cross 20 × 2 and 2 × 20 µm |
| T3 NbN four-wire bar (L20, datatype 0) | origin (−3000, −250); keep-out (no Au) x −3400 … −2600, y −310 … +230 |
| T11 Au-to-Al via chain | Al islands (L10) x −500 … −100 and +100 … +500, y ±75; Au pieces (L50) x −625 … −350, −250 … +250, +350 … +625, y ±75; openings (L40) 100 × 100 at x = −425, −175, +175, +425; keep-out x −650 … +650, y ±100 |
| Mark sites (L1, L40, L20/L22 squares, L22 cross) | (±4300, ±4830) µm |
| Au ground-fill bond spots (labels, layer 100) | GND at (±4700, ±1500) |
