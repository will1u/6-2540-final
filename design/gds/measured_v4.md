> **Claude-authored.** Written by gds/measure_dies.py; regenerate, do not edit.

Read-only measurement of the v4 GDS files (no GDS was written). Units are given in each header. Top cells are flattened before measuring. Areas are merged per layer (gdstk boolean OR).

## 1. Files

| File | SHA-256 (first 16) | Modified (local) | Bytes | Top cell | Outline bbox, um (source) |
|---|---|---|---:|---|---|
| trap_die_v4_A30.gds | 1d4abbf88105ec23 | 2026-11-10T11:33:21 | 57394 | TRAP_DIE_V4_A30 | (-5000, -5000) to (5000, 5000) (layer 101 polygons) |
| trap_die_v4_B60.gds | 89e4dc808d2ceabd | 2026-11-10T11:33:21 | 57466 | TRAP_DIE_V4_B60 | (-5000, -5000) to (5000, 5000) (layer 101 polygons) |
| trap_die_v4_NODET.gds | d5b32c23924d7d58 | 2026-11-10T11:33:21 | 20412 | TRAP_DIE_V4_NODET | (-5000, -5000) to (5000, 5000) (layer 101 polygons) |
| test_die_v4.gds | d7c25bd035d00e36 | 2026-11-09T16:33:22 | 520478 | TEST_DIE_V4 | (-5000, -1250) to (5000, 1250) (layer 101 polygons) |
| test_die_v4_TRAP.gds | b1247c80ce2b16c4 | 2026-11-09T16:33:22 | 9722 | TEST_DIE_V4_TRAP | (-5000, -1250) to (5000, 1250) (layer 101 polygons) |
| snspd_die_v4.gds | 919f68b823714376 | 2026-11-12T14:07:50 | 280582 | SNSPD_DIE_V4 | (-5000, -5000) to (5000, 5000) (layer 101 polygons) |
| run_R1_TRAP.gds | 281f6222285178c6 | 2026-11-09T16:11:50 | 35292 | RUN_R1_TRAP | (-49995, -49999) to (50000, 49999) (layer 101 polygons) |
| run_R1_FULL.gds | d71022c494349eb1 | 2026-11-09T16:11:51 | 660456 | RUN_R1_FULL | (-49995, -49999) to (50000, 49999) (layer 101 polygons) |
| run_R1_ONE.gds | 3a9619c5cc8acf0e | 2026-11-12T14:12:53 | 420694 | RUN_R1_ONE | (-49995, -49999) to (50000, 49999) (layer 101 polygons) |
| wafer_v4.gds | 996628a824690291 | 2026-11-09T16:11:43 | 643102 | WAFER_V4 | (-49995, -49999) to (50000, 49999) (layer 101 polygons) |

## 2. Merged area per layer

Cell = polygon count / merged area in mm^2.

| Layer | trap_die_v4_A30.gds | trap_die_v4_B60.gds | trap_die_v4_NODET.gds | test_die_v4.gds | test_die_v4_TRAP.gds | snspd_die_v4.gds | run_R1_TRAP.gds | run_R1_FULL.gds | run_R1_ONE.gds | wafer_v4.gds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 8 / 0.0031 | 8 / 0.0031 | 8 / 0.0031 | 8 / 0.0031 | 8 / 0.0031 | 8 / 0.0031 | 64 / 0.0251 | 64 / 0.0251 | 72 / 0.0282 | 448 / 0.1756 |
| 10 | 1 / 0.1423 | 1 / 0.1430 | 0 / 0.0000 | 43 / 0.7108 | 0 / 0.0000 | 10 / 0.5834 | 0 / 0.0000 | 90 / 1.9922 | 25 / 1.8790 | 770 / 17.6431 |
| 20 | 329 / 0.0019 | 329 / 0.0026 | 0 / 0.0000 | 4516 / 0.0203 | 0 / 0.0000 | 2609 / 0.0134 | 0 / 0.0000 | 10348 / 0.0496 | 6863 / 0.0372 | 89603 / 0.4294 |
| 22 | 24 / 0.0021 | 24 / 0.0021 | 0 / 0.0000 | 92 / 1.0119 | 0 / 0.0000 | 116 / 0.1059 | 0 / 0.0000 | 280 / 2.0322 | 352 / 0.2223 | 2500 / 17.2845 |
| 40 | 11 / 0.0114 | 11 / 0.0114 | 0 / 0.0000 | 74 / 0.6526 | 0 / 0.0000 | 40 / 0.1705 | 0 / 0.0000 | 192 / 1.3507 | 135 / 0.3980 | 1687 / 11.5380 |
| 50 | 74 / 91.3138 | 74 / 91.3132 | 72 / 91.4720 | 30 / 12.6739 | 4 / 21.4139 | 21 / 93.6672 | 440 / 591.6597 | 500 / 573.5457 | 556 / 826.8468 | 3396 / 3776.6856 |
| 100 | 74 / 0.0095 | 74 / 0.0095 | 53 / 0.0071 | 443 / 0.0438 | 50 / 0.0051 | 104 / 0.0111 | 436 / 1.5304 | 1306 / 1.5497 | 701 / 1.5112 | 10437 / 2.8491 |
| 101 | 1 / 100.0000 | 1 / 100.0000 | 1 / 100.0000 | 1 / 25.0000 | 1 / 25.0000 | 1 / 100.0000 | 10 / 7852.9425 | 10 / 7852.9425 | 11 / 7852.9425 | 58 / 7852.9425 |
| 24 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 |
| 30 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 |
| 31 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 |
| 45 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 | 0 / 0.0000 |

## 3. Au (layer 50) and the plating mold

E2 plated area = E1 evaporated area (same Au pattern). Complement = outline box minus Au, i.e. the area exposed in inverted-exposure plating-mold lithography.

| File | Au written, cm^2 | Complement in outline, cm^2 | Outline area, cm^2 |
|---|---:|---:|---:|
| trap_die_v4_A30.gds | 0.91314 | 0.0869 | 1.0000 |
| trap_die_v4_B60.gds | 0.91313 | 0.0869 | 1.0000 |
| trap_die_v4_NODET.gds | 0.91472 | 0.0853 | 1.0000 |
| test_die_v4.gds | 0.12674 | 0.1233 | 0.2500 |
| test_die_v4_TRAP.gds | 0.21414 | 0.0359 | 0.2500 |
| snspd_die_v4.gds | 0.93667 | 0.0633 | 1.0000 |
| run_R1_TRAP.gds | 5.91660 | 94.0760 | 99.9926 |
| run_R1_FULL.gds | 5.73546 | 94.2571 | 99.9926 |
| run_R1_ONE.gds | 8.26847 | 91.7241 | 99.9926 |
| wafer_v4.gds | 37.76686 | 62.2257 | 99.9926 |

## 4. Layer 20 (EBL) by datatype

| File | Datatype | Polygons | Merged area, um^2 |
|---|---:|---:|---:|
| trap_die_v4_A30.gds | 0 | 329 | 1928.1 |
| trap_die_v4_B60.gds | 0 | 329 | 2614.5 |
| test_die_v4.gds | 0 | 2241 | 13074.0 |
| test_die_v4.gds | 1 | 325 | 1028.1 |
| test_die_v4.gds | 2 | 325 | 1028.1 |
| test_die_v4.gds | 3 | 325 | 1028.1 |
| test_die_v4.gds | 4 | 325 | 1028.1 |
| test_die_v4.gds | 5 | 325 | 1028.1 |
| test_die_v4.gds | 6 | 325 | 1028.1 |
| test_die_v4.gds | 7 | 325 | 1028.1 |
| snspd_die_v4.gds | 0 | 659 | 7256.1 |
| snspd_die_v4.gds | 1 | 325 | 1028.1 |
| snspd_die_v4.gds | 2 | 325 | 1028.1 |
| snspd_die_v4.gds | 3 | 325 | 1028.1 |
| snspd_die_v4.gds | 5 | 325 | 1028.1 |
| snspd_die_v4.gds | 6 | 325 | 1028.1 |
| snspd_die_v4.gds | 7 | 325 | 1028.1 |
| run_R1_FULL.gds | 0 | 5798 | 35233.1 |
| run_R1_FULL.gds | 1 | 650 | 2056.1 |
| run_R1_FULL.gds | 2 | 650 | 2056.1 |
| run_R1_FULL.gds | 3 | 650 | 2056.1 |
| run_R1_FULL.gds | 4 | 650 | 2056.1 |
| run_R1_FULL.gds | 5 | 650 | 2056.1 |
| run_R1_FULL.gds | 6 | 650 | 2056.1 |
| run_R1_FULL.gds | 7 | 650 | 2056.1 |
| run_R1_ONE.gds | 0 | 2963 | 24838.9 |
| run_R1_ONE.gds | 1 | 650 | 2056.1 |
| run_R1_ONE.gds | 2 | 650 | 2056.1 |
| run_R1_ONE.gds | 3 | 650 | 2056.1 |
| run_R1_ONE.gds | 5 | 650 | 2056.1 |
| run_R1_ONE.gds | 6 | 650 | 2056.1 |
| run_R1_ONE.gds | 7 | 650 | 2056.1 |
| wafer_v4.gds | 0 | 50928 | 307062.0 |
| wafer_v4.gds | 1 | 5525 | 17476.9 |
| wafer_v4.gds | 2 | 5525 | 17476.9 |
| wafer_v4.gds | 3 | 5525 | 17476.9 |
| wafer_v4.gds | 4 | 5525 | 17476.9 |
| wafer_v4.gds | 5 | 5525 | 17476.9 |
| wafer_v4.gds | 6 | 5525 | 17476.9 |
| wafer_v4.gds | 7 | 5525 | 17476.9 |

## 5. Detector meander, trap_die_v4_A30.gds

| Quantity | Value |
|---|---:|
| Lines (polygons 0.125-0.135 um tall, >= 10 um long) | 160 |
| Lines that are plain rectangles | 160 |
| Cut check at x = 240 um: intervals | 160 |
| Lines inside the NbN piece nearest (240, 0) | 160 of 160 |
| Line length, um (min / max) | 36.000 / 36.000 |
| Wire width, um (median; min / max) | 0.130 (0.130 / 0.130) |
| Pitch, um (median; min / max) | 0.200 (0.200 / 0.200) |
| Radial span, um | 31.93 |
| Straight total, um / mm | 5760.0 / 5.7600 |
| Squares = total / width | 44307.7 |
| Lk, pH/sq | 69.95 |
| L, uH | 3.0991 |
| tau = L/50 ohm, ns | 61.98 |
| Room-temperature R of straight sections, ohm | 17723077 |

## 5. Detector meander, trap_die_v4_B60.gds

| Quantity | Value |
|---|---:|
| Lines (polygons 0.125-0.135 um tall, >= 10 um long) | 160 |
| Lines that are plain rectangles | 160 |
| Cut check at x = 240 um: intervals | 160 |
| Lines inside the NbN piece nearest (240, 0) | 160 of 160 |
| Line length, um (min / max) | 69.000 / 69.000 |
| Wire width, um (median; min / max) | 0.130 (0.130 / 0.130) |
| Pitch, um (median; min / max) | 0.200 (0.200 / 0.200) |
| Radial span, um | 31.93 |
| Straight total, um / mm | 11040.0 / 11.0400 |
| Squares = total / width | 84923.1 |
| Lk, pH/sq | 69.95 |
| L, uH | 5.9400 |
| tau = L/50 ohm, ns | 118.80 |
| Room-temperature R of straight sections, ohm | 33969231 |

Excluded from L and tau: turns, tapers, tabs and connections. Lk = hbar Rs / (pi 1.76 kB Tc) with hbar 1.0546e-34 J s, kB 1.3807e-23 J/K (sim/15_snspd_geometry.py part E), Rs 400 ohm/sq, Tc 7.9 K.

## 6. Layer 40 openings

| File | Class | Count |
|---|---|---:|
| trap_die_v4_A30.gds | SNSPD contact | 2 |
| trap_die_v4_A30.gds | mark cross | 4 |
| trap_die_v4_A30.gds | mirror ground via | 1 |
| trap_die_v4_B60.gds | SNSPD contact | 2 |
| trap_die_v4_B60.gds | mark cross | 4 |
| trap_die_v4_B60.gds | mirror ground via | 1 |
| test_die_v4.gds | mark cross | 4 |
| test_die_v4.gds | mirror ground via | 5 |
| test_die_v4.gds | unclassified | 61 |
| snspd_die_v4.gds | SNSPD contact | 1 |
| snspd_die_v4.gds | mark cross | 4 |
| snspd_die_v4.gds | mirror ground via | 11 |
| snspd_die_v4.gds | unclassified | 20 |
| run_R1_FULL.gds | mark cross | 24 |
| run_R1_FULL.gds | mirror ground via | 14 |
| run_R1_FULL.gds | unclassified | 130 |
| run_R1_ONE.gds | SNSPD contact | 2 |
| run_R1_ONE.gds | mark cross | 28 |
| run_R1_ONE.gds | mirror ground via | 29 |
| run_R1_ONE.gds | unclassified | 48 |
| wafer_v4.gds | mark cross | 224 |
| wafer_v4.gds | mirror ground via | 124 |
| wafer_v4.gds | unclassified | 1115 |

Detail for the detector dies (centre and size, um):

| File | Class | Centre | Size |
|---|---|---|---|
| trap_die_v4_A30.gds | mark cross | (-4300.0, -4758.0) | 60.0 x 24.0 |
| trap_die_v4_A30.gds | SNSPD contact | (157.0, 5.0) | 18.0 x 3.0 |
| trap_die_v4_A30.gds | mirror ground via | (-2140.0, 130.0) | 100.0 x 100.0 |
| trap_die_v4_A30.gds | mark cross | (-4300.0, 4758.0) | 60.0 x 24.0 |
| trap_die_v4_A30.gds | mark cross | (4300.0, -4758.0) | 60.0 x 24.0 |
| trap_die_v4_A30.gds | SNSPD contact | (157.0, -5.0) | 18.0 x 3.0 |
| trap_die_v4_A30.gds | mark cross | (4300.0, 4758.0) | 60.0 x 24.0 |
| trap_die_v4_B60.gds | mark cross | (-4300.0, -4758.0) | 60.0 x 24.0 |
| trap_die_v4_B60.gds | SNSPD contact | (140.5, 5.0) | 18.0 x 3.0 |
| trap_die_v4_B60.gds | mirror ground via | (-2140.0, 130.0) | 100.0 x 100.0 |
| trap_die_v4_B60.gds | mark cross | (-4300.0, 4758.0) | 60.0 x 24.0 |
| trap_die_v4_B60.gds | mark cross | (4300.0, -4758.0) | 60.0 x 24.0 |
| trap_die_v4_B60.gds | SNSPD contact | (140.5, -5.0) | 18.0 x 3.0 |
| trap_die_v4_B60.gds | mark cross | (4300.0, 4758.0) | 60.0 x 24.0 |

## 7. Local Al mirror (layer 10), detector dies

| Quantity | trap_die_v4_A30.gds | trap_die_v4_B60.gds |
|---|---:|---:|
| Bbox, um (x0, y0) to (x1, y1) | (-2240.0, -20.0) to (268.0, 230.0) | (-2240.0, -20.0) to (284.5, 230.0) |
| Strip width at x = 0, um | 40.00 | 40.00 |
| Strip width at the via, um | 250.00 | 250.00 |
| Ground via centre, um | [-2140.0, 130.0] | [-2140.0, 130.0] |
| Path, Al detector end to via, um | 2538.0 | 2554.5 |

Path = (x_end - x_via) + |y_via| along the strip centreline, with x_end the Al maximum x (detector end).

## 8. Runs and wafer: totals

| File | Direct references (die cell: count) | EBL layer 20, mm^2 (merged) | EBL, mm^2 (raw sum) | Au layer 50, cm^2 |
|---|---|---:|---:|---:|
| run_R1_TRAP.gds | {'TRAP_DIE_V4_NODET': 6, 'TEST_DIE_V4_TRAP': 2} | 0.00000 | 0.00000 | 5.9166 |
| run_R1_FULL.gds | {'TRAP_DIE_V4_A30': 2, 'TEST_DIE_V4': 2, 'TRAP_DIE_V4_B60': 2, 'TRAP_DIE_V4_NODET': 2} | 0.04963 | 0.05023 | 5.7355 |
| run_R1_ONE.gds | {'TRAP_DIE_V4_A30': 4, 'SNSPD_DIE_V4': 2, 'TRAP_DIE_V4_NODET': 2, 'TRAP_DIE_V4_B60': 1} | 0.03718 | 0.03778 | 8.2685 |
| wafer_v4.gds | {'TRAP_DIE_V4_B60': 14, 'TRAP_DIE_V4_A30': 25, 'TEST_DIE_V4': 17} | 0.4294 | - | 37.7669 |

make_run.py printed 0.0502 mm^2 for run_R1_FULL: the sum over die cells (raw, not merged) is compared above.

## 9. Acceptance

| Check | Expected | Measured | Pass |
|---|---|---|---|
| trap_die_v4_A30.gds: meander lines | 160 | 160 | PASS |
| trap_die_v4_A30.gds: meander cut at x = 240 um | 160 | 160 | PASS |
| trap_die_v4_A30.gds: total straight length (mm, 1 %) | 5.76 | 5.76 | PASS |
| trap_die_v4_A30.gds: L (uH, 1 %) | 3.1 | 3.0991 | PASS |
| trap_die_v4_A30.gds: tau (ns, 1 %) | 62.0 | 61.982 | PASS |
| trap_die_v4_B60.gds: meander lines | 160 | 160 | PASS |
| trap_die_v4_B60.gds: meander cut at x = 240 um | 160 | 160 | PASS |
| trap_die_v4_B60.gds: total straight length (mm, 1 %) | 11.04 | 11.04 | PASS |
| trap_die_v4_B60.gds: L (uH, 1 %) | 5.94 | 5.94 | PASS |
| trap_die_v4_B60.gds: tau (ns, 1 %) | 118.8 | 118.799 | PASS |
| run_R1_FULL EBL area (mm^2, 2 % of make_run 0.0502) | 0.0502 | 0.049626 | PASS |
| run_R1_ONE EBL area (mm^2, 2 % of make_run 0.0378) | 0.0378 | 0.037176 | PASS |
| trap_die_v4_A30.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| trap_die_v4_B60.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| trap_die_v4_NODET.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| test_die_v4.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| test_die_v4_TRAP.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| snspd_die_v4.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| run_R1_TRAP.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| run_R1_FULL.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| run_R1_ONE.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| wafer_v4.gds: layers 24, 30, 31, 45 empty | 0 polygons | 0 non-empty | PASS |
| trap_die_v4_NODET.gds: nothing on layers 10, 20, 22, 40 | 0 polygons | 0 non-empty | PASS |
| test_die_v4_TRAP.gds: nothing on layers 10, 20, 22, 40 | 0 polygons | 0 non-empty | PASS |
| run_R1_TRAP.gds: nothing on layers 10, 20, 22, 40 | 0 polygons | 0 non-empty | PASS |

## 10. SNSPD-only die (snspd_die_v4.gds)

Eight detector cells, no trap. Section 5 (single-meander analysis) does not apply to it.

| Quantity | Value |
|---|---:|
| Layer-20 datatypes present | 7 |
| Layer 20, datatype 0: merged area, um^2 (polygons) | 7256.1 (659) |
| Layer 20, datatype 1: merged area, um^2 (polygons) | 1028.1 (325) |
| Layer 20, datatype 2: merged area, um^2 (polygons) | 1028.1 (325) |
| Layer 20, datatype 3: merged area, um^2 (polygons) | 1028.1 (325) |
| Layer 20, datatype 5: merged area, um^2 (polygons) | 1028.1 (325) |
| Layer 20, datatype 6: merged area, um^2 (polygons) | 1028.1 (325) |
| Layer 20, datatype 7: merged area, um^2 (polygons) | 1028.1 (325) |
| Au (layer 50), cm^2 | 0.93667 |

Layer-40 openings by size (um):

| Size | Count |
|---|---:|
| 100.0 x 100.0 | 12 |
| 110.0 x 110.0 | 4 |
| 18.0 x 3.0 | 16 |
| 60.0 x 24.0 | 4 |

