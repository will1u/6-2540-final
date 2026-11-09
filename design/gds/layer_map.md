# Layer map: trap_die_v4 (A30 / B60 / NODET), test_die_v3, wafer_v4

> **Claude-authored.** Generated alongside `make_chip.py`, `make_test_die.py` and `make_wafer.py`.
> - Units are µm; the GDS database unit is 1 nm.
> - Top cells: `TRAP_DIE_V4_A30`, `TRAP_DIE_V4_B60`, `TRAP_DIE_V4_NODET`, `TEST_DIE_V3`, `TEST_DIE_V3_TRAP` and `WAFER_V4`.
> - **v4 (2026-11-08, DESIGN_LOG step 25): local-mirror architecture** (team decision; `notes/decisions.md`). No die-wide Al, no 10 µm D2, no gap etch. The Au electrodes sit on Si / 1 µm thermal SiO₂ / 238 nm spacer / 80 nm cap. The Al is a local mirror under the centre DC. The SNSPD leads are Au in a slot along the centre DC. A30 and B60 (60 × 30 µm window) both kept.
> - `TRAP_DIE_V4_NODET` (`make_chip.py --nodet`, the R1_TRAP die) uses only layers 1 and 50, plus 100/101: Au on thermal SiO₂ over high-resistivity Si.
> - **The test dies are still v3** (die-wide M1, D2 openings, L45). Their rework for v4 is open (`fab/OPEN_DECISIONS.md`).
> - R&D run layouts `RUN_R1_TRAP` and `RUN_R1_FULL` (`make_run.py`) reference these die cells.
> - Earlier versions are archived: v1 square die in `archive_v1_square/`, v2 narrow die in `archive_v2_narrow/`, v3 baseline (die-wide Al + 10 µm D2) in `archive_v3_baseline/`.

## Fab layers (v4 trap dies)

| GDS layer | Name | Material / process | Write tool | Drawn = | Aligns to | Notes |
|---|---|---|---|---|---|---|
| 1 | MARK | ~1 µm Si etch | MLA150 | etched | first layer | Crosses at 4 edge notches per die. |
| 10 | M1 | Al-1%Cu **450 nm** (team decision 2026-11-08; was 150), **local mirror** (A30, B60) | MLA150 | Al kept | 1 | \|y\| ≤ 20 µm under the centre DC, x = −2240 … +268 (B60: +284.5, 10 µm past the NbN); branch to y = 230 at x = −2240 … −2040 under the Au fill for the ground via. Never under the RF rails (checked). 0.157 mm² per die. |
| 20 | NBN | NbN meander + contact tabs (+ test bars) | EBL (HSQ) | NbN kept | 22 crosses | v3.1 (DESIGN_LOG step 24): 130 nm wires, 200 nm pitch, 160 lines, 36 × 32 µm; tabs at x = 175 … 215 (B60: lines 69 µm, tabs 158.5 … 198.5), \|y\| ≈ 13 … 16, under the solid centre DC. Datatypes 1–7 = T8 dose array (test die). |
| 22 | LEAD | Ti/Au contacts + EBL crosses (lift-off) | MLA150 | metal | 1 | Before the nanowire etch, as in v3. **v4: no buried leads.** Each contact covers the −x half of an NbN tab and steps into the slot to a 27 × 7 µm pad at x = 143 … 170 (B60: 126.5 … 153.5), y = ±(1.5 … 8.5). |
| 24, 30, 31 | *retired in v3* | – | – | – | – | ITO / via layers of v2. Must stay empty (checked). |
| 40 | OPEN | Openings through the cap (SNSPD contacts, ~80 nm) and cap + spacer (mirror via, ~0.32 µm), stopping on Ti/Au and Al | MLA150 + RIE | SiO₂ removed | 1 | Contacts: 18 × 3 µm at x = 148 … 166 (B60: 131.5 … 149.5), y = ±(3.5 … 6.5), ≥ 1 µm inside the Au lead and the Ti/Au pad. Mirror via: 100 × 100 µm at (−2140, 130), enclosed ≥ 25 µm by the Au fill and the Al. Also crosses at the marks. |
| 45 | PROTECT | *retired in v4* | – | – | – | – | No gap etch without D2. Must stay empty (checked). |
| 50 | AU | Electrode Au: E2 6 µm plated or E1 0.35 µm lift-off (**open**) | MLA150 | Au | 1 / 40 crosses | Electrodes, ground fill, pads and (v4) the SNSPD leads. **gds2itvg simulates this layer** (`*_sim.json`). |
| 100 | NOTE | Text | – | – | – | Not fabricated. |
| 101 | CHIP | Die outline / wafer outline | – | – | – | Not written. |

## Process order (v4, A30)

1 → thermal SiO₂ (D1) → 10 (local mirror) → SiO₂ spacer → NbN → 22 → 20 → SiO₂ cap → 40 → electrode Au 50 (E1: lift-off; E2: seed, mold, plate, seed removal) → test → dice.

NODET / R1_TRAP: 1 → thermal SiO₂ → 50 → test → dice. Details: `design/fab/variants/LOCAL_MIRROR.md` H.2 (the v4 traveler is not yet written).

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
| Pad rows | top and bottom die edges, y = ±4720, \|x\| = 2060…3500, 180 µm pitch. `TL1…TL8`, `TR1…TR9`, `BL1…BL8`, `BR1…BR9` in `*_pads.csv` |
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
