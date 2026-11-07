# Layer map: trap_die_v2 (A30 / B60), test_die_v2, wafer_v2

> **Claude-authored.** Generated alongside `make_chip.py`, `make_test_die.py` and `make_wafer.py`.
> - Units are µm; the GDS database unit is 1 nm.
> - Top cells: `TRAP_DIE_V2_A30`, `TRAP_DIE_V2_B60`, `TRAP_DIE_V2_NODET`, `TEST_DIE_V2` and `WAFER_V2`.
> - R&D run layouts `RUN_R1_TRAP` and `RUN_R1_FULL` (`make_run.py`) reference these die cells; see `fab/mask_list.md` section 3.
> - `TRAP_DIE_V2_NODET` (`make_chip.py --nodet`) is the plain trap without an SNSPD. It uses only layers 1, 10, 40, 45 and 50, plus 100/101.
> - The square-die version is archived in `archive_v1_square/`.

## Fab layers

| GDS layer | Name | Material / process | Write tool | Drawn = | Aligns to | Notes |
|---|---|---|---|---|---|---|
| 1 | MARK | ~1 µm Si etch | MLA150 | etched | first layer | Crosses at 4 edge notches per die. M1 is cut out around them, so they stay visible. |
| 10 | M1 | Al-1%Cu ground plane + SNSPD mirror | MLA150 | Al kept | 1 | 150 µm from the dicing edge. Cut-outs under the SNSPD pads and at the marks. |
| 20 | NBN | NbN meander + contact tabs (+ test bars) | EBL (HSQ) | NbN kept | 22 crosses | 100 nm wires, 200 nm pitch, 150 lines; 40 × 3 µm tabs. Datatype 0 = nominal dose; datatypes 1–7 = T8 dose array on the test die. |
| 22 | LEAD | Ti/Au SNSPD leads, pads, EBL crosses (lift-off) | MLA150 | metal | 1 | Done **before** the nanowire etch. Leads run under the centre DC and its lead. |
| 24 | VIA_M1 | 10 × 10 µm via through cap + spacer to Al | MLA150 + CHF₃ RIE | oxide removed | 1 | Grounds the buried ITO; 45 µm on the +x side of the meander. |
| 31 | ITO_BURIED | 60 nm ITO on the 80 nm cap, under D2 | MLA150 lift-off | ITO | 1 | Within 18 µm of the axis, never under RF. Optical matching + RF shield. |
| 30 | ITO_TOP | ~125 nm ITO on D2 (+10–15 nm margin) | MLA150 lift-off | ITO | 1 | Readout window + 5 µm overlap axially, 2 µm inside the Au edge radially. Tied to the centre DC. |
| 40 | D2OPEN | Openings through 10 µm D2 (+ cap) to M1 and to the SNSPD/test pads; crosses for aligning L50 | MLA150 + RIE | oxide removed | 1 | |
| 45 | PROTECT | Resist kept on during the Au-masked D2 gap etch | MLA150 | resist kept | 40 / 50 | Covers every bond/probe D2 opening (+10 µm), the readout window (+2.5 µm), the SNSPD lead branch and the test areas. |
| 50 | AU | Electroplated Au: electrodes, leads, pads, ground fill | MLA150, negative mold | Au plated | 40 crosses | **gds2itvg simulates this layer** (`*_sim.json`). |
| 100 | NOTE | Text | – | – | – | Not fabricated. |
| 101 | CHIP | Die outline / wafer outline | – | – | – | Not written. |

## Process order

1 → thermal oxide → 10 → spacer → NbN → 22 → 20 → cap → 24 → 31 → D2 → 30 → 40 → seed → 50 → plate → seed removal → 45 → Au-masked D2 gap etch → test → dice.

Details are in `design/fab/TRAVELER.md`.

## Trap die v2 key coordinates

GDS µm, die centre (0, 0), die 10 × 2.5 mm.

| Feature | Location |
|---|---|
| Trap axis | y = 0 |
| Readout zone (SNSPD) | (300, 0) |
| Loading zone | (−300, 0) |
| RF U | rails x = −2000…2000, U bar x = 2000…2060; RF pad (4700, 0) |
| Centre DC pad | (−4650, 0) |
| SNSPD pads | (−4750, ±260) |
| Pad rows | y = ±1030, \|x\| = 2450…4700, 180 µm pitch. `TL1…TL8`, `TR1…TR9`, `BL1…BL8`, `BR1…BR9` in `*_pads.csv` |
| GND bond spots | (±2500, ±820) |
| M1 bond openings | (±2900, ±820) |
| L1 / L40 marks | (±2150, ±1080) |
| L22 EBL crosses | (0, ±700), (600, ±700) |

Electrode numbers match `*_sim.json` and `*_pads.csv`:
- 1 = RF
- 2 = centre DC
- 3–17 = top segments (left → right), 18–32 = bottom segments
- 33/34 = top caps (L/R), 35/36 = bottom caps (L/R)
