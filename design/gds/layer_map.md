# Layer map: trap_die_v3 (A30 / B60 / NODET), test_die_v3, wafer_v3

> **Claude-authored.** Generated alongside `make_chip.py`, `make_test_die.py` and `make_wafer.py`.
> - Units are µm; the GDS database unit is 1 nm.
> - Top cells: `TRAP_DIE_V3_A30`, `TRAP_DIE_V3_B60`, `TRAP_DIE_V3_NODET`, `TEST_DIE_V3`, `TEST_DIE_V3_TRAP` and `WAFER_V3`.
- **v3 (2026-11-07, DESIGN_LOG steps 17–18): no indium tin oxide (ITO) at all, and a 10 × 10 mm trap die.** Layers 24, 30 and 31 are retired; the readout window is an opening in the centre-DC Au over bare SiO₂ (D2).
> - R&D run layouts `RUN_R1_TRAP` and `RUN_R1_FULL` (`make_run.py`) reference these die cells; see `fab/mask_list.md` section 3.
> - `TRAP_DIE_V3_NODET` (`make_chip.py --nodet`) is the plain trap without an SNSPD. It uses only layers 1, 10, 40, 45 and 50, plus 100/101.
> - Earlier versions are archived: square die with corner zones in `archive_v1_square/`, narrow 10 × 2.5 mm die with the two-ITO window in `archive_v2_narrow/`.

## Fab layers

| GDS layer | Name | Material / process | Write tool | Drawn = | Aligns to | Notes |
|---|---|---|---|---|---|---|
| 1 | MARK | ~1 µm Si etch | MLA150 | etched | first layer | Crosses at 4 edge notches per die. M1 is cut out around them, so they stay visible. |
| 10 | M1 | Al-1%Cu ground plane + SNSPD mirror | MLA150 | Al kept | 1 | 150 µm from the dicing edge. Cut-outs under the SNSPD pads and at the marks. |
| 20 | NBN | NbN meander + contact tabs (+ test bars) | EBL (HSQ) | NbN kept | 22 crosses | v3.1 (DESIGN_LOG step 24, `gds/snspd_geom.py`): 130 nm wires, 200 nm pitch, 160 lines over 32 µm radially (1 µm past each radial window edge; 2 µm would raise RF pickup 1.40×, sim/10); lines 36 µm (A30) / 69 µm (B60) long, i.e. 3 / 4.5 µm past each axial window edge. Turns are 0.5 µm end blocks with rounded slot ends, outside the light footprint; the outer lines flare smoothly into 40 × 3 µm tabs. All NbN within \|y\| ≤ 17 µm (checked). Datatype 0 = nominal dose; datatypes 1–7 = T8 dose array on the test die; T9 = geometry array. |
| 22 | LEAD | Ti/Au SNSPD leads, pads, EBL crosses (lift-off) | MLA150 | metal | 1 | Done **before** the nanowire etch. Leads run under the centre DC and its lead. |
| 24 | VIA_M1 | *retired in v3* | – | – | – | – | Was part of the two-ITO window (v2). Must stay empty; `check_chip.py` checks this. |
| 31 | ITO_BURIED | *retired in v3* | – | – | – | – | Was part of the two-ITO window (v2). Must stay empty; `check_chip.py` checks this. |
| 30 | ITO_TOP | *retired in v3* | – | – | – | – | Was part of the two-ITO window (v2). Must stay empty; `check_chip.py` checks this. |
| 40 | D2OPEN | Openings through 10 µm D2 (+ cap) to M1 and to the SNSPD/test pads; fill-to-M1 ground vias; crosses for aligning L50 | MLA150 + RIE | SiO₂ removed | 1 | Ground vias (step 22): 150 µm squares under the Au ground fill, enclosed ≥ 25 µm by Au and by M1; plated over, so no L45. |
| 45 | PROTECT | Resist kept on during the Au-masked D2 gap etch | MLA150 | resist kept | 40 / 50 | Covers every bond/probe D2 opening (+10 µm), the readout window (+2.5 µm), the SNSPD lead branch and the test areas. |
| 50 | AU | Electroplated Au: electrodes, leads, pads, ground fill | MLA150, negative mold | Au plated | 40 crosses | **gds2itvg simulates this layer** (`*_sim.json`). |
| 100 | NOTE | Text | – | – | – | Not fabricated. |
| 101 | CHIP | Die outline / wafer outline | – | – | – | Not written. |

## Process order

1 → thermal SiO₂ (D1) → 10 → SiO₂ spacer → NbN → 22 → 20 → SiO₂ cap → D2 (10 µm SiO₂) → 40 → seed → 50 → plate → seed removal → 45 → Au-masked D2 gap etch → test → dice (10 × 10 mm trap dies, 10 × 2.5 mm test dies).

Details are in `design/fab/TRAVELER.md`.

## Trap die v3 key coordinates

GDS µm, die centre (0, 0), die 10 × 10 mm.

| Feature | Location |
|---|---|
| Trap axis | y = 0 |
| Readout zone (SNSPD) | (300, 0) |
| Loading zone | (−300, 0) |
| RF U | rails x = −2000…2000, U bar x = 2000…2060; RF pad (4700, 0) |
| Centre DC pad | (−4650, 0) |
| SNSPD pads | (−4750, ±260) |
| Pad rows | top and bottom die edges, y = ±4720, \|x\| = 2060…3500, 180 µm pitch (kept out of the beam-exit corners \|x\|, \|y\| > 4 mm). `TL1…TL8`, `TR1…TR9`, `BL1…BL8`, `BR1…BR9` in `*_pads.csv` |
| GND bond spots | (±4700, ±1500), side edges |
| M1 bond openings | (±4700, ±2000), side edges |
| Fill-to-M1 ground vias (L40 under the Au fill, step 22) | (±4700, ±1000), (±1000, ±2500); 150 × 150 µm |
| L1 / L40 marks | (±4300, ±4830) |
| L22 EBL crosses | (0, ±700), (600, ±700) |

Electrode numbers match `*_sim.json` and `*_pads.csv`:
- 1 = RF
- 2 = centre DC
- 3–17 = top segments (left → right), 18–32 = bottom segments
- 33/34 = top caps (L/R), 35/36 = bottom caps (L/R)
