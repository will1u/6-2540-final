> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Die layout and alignment

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

Current files are v4, for the one-wafer run R1_ONE (decision 2026-11-12): trap dies `gds/trap_die_v4_A30.gds`, `gds/trap_die_v4_B60.gds` and `gds/trap_die_v4_NODET.gds`; SNSPD-only die `gds/snspd_die_v4.gds`; run `gds/run_R1_ONE.gds`; full-wafer reference `gds/wafer_v4.gds`. The test dies `gds/test_die_v4.gds` and `gds/test_die_v4_TRAP.gds` are kept but are **not in R1_ONE**. The runs `gds/run_R1_TRAP.gds` and `gds/run_R1_FULL.gds` are superseded by R1_ONE and kept. Earlier layouts are archived: v1 (square die) in `gds/archive_v1_square/`, v2 (narrow die) in `gds/archive_v2_narrow/`, v3 (die-wide Al plane, 10 µm D2) in `gds/archive_v3_baseline/`. Do not use the archives for fabrication.

Numbers below are GDS µm with the die centre at (0, 0), unless noted. Areas and line counts are from [measured_v4.md](../gds/measured_v4.md).

## Trap die floorplan (v4)

Generator: `gds/make_chip.py` (`--det60` for B60, `--nodet` for NODET). `check_chip.py` passes on A30, B60 and NODET (`ALL CHECKS PASS`).

| Feature | Location |
|---|---|
| Die (L101) | 10 × 10 mm: x = ±5000, y = ±5000 |
| Trap axis | die centre line, y = 0 |
| RF rails | x = −2000 … +2000, U closed at the right (+x) end (U bar x = 2000 … 2060); RF pad (4700, 0), 200 × 200 µm, on the right die edge |
| Zones | loading zone (−240, 0); readout zone (+240, 0) with the SNSPD and window; 480 µm apart (step 28) |
| Centre DC | \|y\| ≤ 20 µm. Centre DC pad C (−4650, 450) on the left edge |
| Segments | 15 + 15 at 120 µm pitch, centres −840 … +840 µm; electrode numbers in the section below |
| Edge pads | Au, 120 (x) × 200 (y) µm, pitch 360 µm, two rows at y = ±4720 µm on the top and bottom die edges. Top and bottom rows at \|x\| = 620 … 3500 µm (right) and −3500 … −980 µm (left). Full list: `*_pads.csv`. The 360 µm pitch is generated and validated; team adoption is pending ([open decisions](OPEN_DECISIONS.md#design-choices)) |
| Left die edge | SNSPD pads SNS (−4750, +100) and SNG (−4750, −100), 200 × 150 µm, Au |
| Ground | Au ground-fill bond spots GND-1 … GND-4 at (±4700, ±1500). Au fill keeps ≥ 30 µm from every signal pad |
| Mirror ground via (A30, B60) | 100 × 100 µm at (−2140, 130) µm, through the cap and spacer to the Al (layer 40). Replaces the v3 fill-to-M1 vias and bond openings |
| Alignment marks | L1 crosses at (±4300, ±4830) µm, 100 × 4 µm arms, in edge notches of the Au ground fill. L40 crosses at (±4300, ±4758) µm, 60 × 24 µm |
| EBL alignment crosses | layer 22, 20 µm crosses with 2 µm arms, at (−60, ±700) and (540, ±700) µm around the readout zone |
| Full pad list | [trap_die_v4_A30_pads.csv](../gds/trap_die_v4_A30_pads.csv), [trap_die_v4_B60_pads.csv](../gds/trap_die_v4_B60_pads.csv), [trap_die_v4_NODET_pads.csv](../gds/trap_die_v4_NODET_pads.csv) |

Pad rows, electrode numbers (from the pads files):

| Row | Pads | Electrodes |
|---|---|---|
| Top-left | TL1 … TL8 at x = −3500 … −980 | TL1 = 33 (top cap L); TL2 … TL8 = 3 … 9 |
| Top-right | TR1 … TR9 at x = 620 … 3500 | TR1 = 34 (top cap R); TR2 … TR9 = 17 … 10 |
| Bottom-left | BL1 … BL8 at x = −3500 … −980 | BL1 = 35 (bottom cap L); BL2 … BL8 = 18 … 24 |
| Bottom-right | BR1 … BR9 at x = 620 … 3500 | BR1 = 36 (bottom cap R); BR2 … BR9 = 32 … 25 |
| Other | RF (4700, 0) = 1; C (−4650, 450) = 2; SNS / SNG = SNSPD leads (A30, B60); GND-1 … 4 = ground fill | |

Electrode numbers match `*_sim.json` and `*_pads.csv`: 1 = RF, 2 = centre DC, 3–17 top segments (left → right), 18–32 bottom segments, 33/34 top caps, 35/36 bottom caps.

**Beam clearance** (`sim/11_beam_clearance.py`, full 10 mm chip) [team calc]: with the trap on the centre line of a 10 × 10 mm die, about **1.7 × 10⁻² of a 493 nm beam** (3.2 × 10⁻² at 650 nm, 9.6 × 10⁻³ at 405 nm) hits the surface. Team decision 2026-11-07 (DESIGN_LOG step 18). The 45° beams through the zones leave the die at the top/bottom edges near \|x\| ≈ 4.7 mm and the side edges near \|y\| ≈ 4.7 mm; no pad sits in the corners \|x\|, \|y\| > 4 mm (`check_chip.py`).

## Readout zone: slot, leads, contacts, mirror, window (A30 and B60)

| Feature | A30 | B60 | Source |
|---|---|---|---|
| Slot in the centre DC | \|y\| < 12.5 µm, from the left end to x = 175 µm; the centre DC is two 7.5 µm halves joined to the right of the slot | to x = 158.5 µm | layer map |
| SNSPD leads (Au, L50) | 5 µm wide, centre y = ±5 µm, from the tip at x = 170 µm to x = −4400 µm, then to SNS / SNG | tip at x = 153.5 µm | layer map; `make_chip.py` |
| L22 Ti/Au contact pads | 27 × 7 µm, x = 143 … 170 µm, y = ±(1.5 … 8.5) µm; each covers the −x half of an NbN tab | x = 126.5 … 153.5 µm | layer map |
| L40 SNSPD contact openings | 18 × 3 µm, centred (157, ±5) µm, x = 148 … 166 µm, y = ±(3.5 … 6.5) µm | centred (140.5, ±5) µm, x = 131.5 … 149.5 µm | `measured_v4.md` §6 |
| Local Al mirror (L10), 100 nm, raised on the thermal SiO₂ (decision 2026-11-12; was inlaid) | strip \|y\| ≤ 20 µm, x = −2240 … +268 µm; 40 µm wide at x = 0, 200 µm wide at the via branch (x = −2240 … −2040 µm) | x to +284.5 µm | `measured_v4.md` §7 |
| Mirror branch | to y = 230 µm at x = −2240 … −2040 µm, under the Au fill | same | layer map |
| Mirror path, Al end to via | 2538.0 µm | 2554.5 µm | `measured_v4.md` §7 |
| Readout window (open in Au) | 30 × 30 µm, axial × radial | 60 × 30 µm | layer map |
| NbN meander (L20) | 160 lines, 130 nm wire, 200 nm pitch, lines 36 µm long, radial span 31.93 µm | lines 69 µm long | `measured_v4.md` §5 |

Mirror and via checks: the mirror stays under the readout zone and the centre DC only, never under the RF rails (`check_chip.py`). The mirror ground via is enclosed ≥ 25 µm by the Au fill and the Al. Ion height, window recess and stack are in [STACK](STACK.md#readout-cross-section).

## Plain trap die (NODET)

`gds/trap_die_v4_NODET.gds` (`make_chip.py --nodet`, the R1_TRAP die; in R1_ONE, two NODET dies): same electrodes, pads, ground fill and marks as A30. It has no window (solid centre DC), no Al, and nothing on layers 10, 20, 22 or 40. Layers 1 and 50 only, plus the notes and outline layers (100, 101). On the shared R1_ONE wafer the NODET dies also receive the blanket films (spacer, NbN, cap); see [RUN_PLAN](RUN_PLAN.md#can-all-dies-share-one-wafer).

## SNSPD-only die (`snspd_die_v4`, in R1_ONE)

Generator: `gds/make_snspd_die.py`. Independent checker: `gds/check_snspd_die.py`, written from the specification and not from the generator. Preview: `gds/snspd_die_v4_preview.png`. Pads: `gds/snspd_die_v4_pads.csv`. Top cell `SNSPD_DIE_V4`.

| Feature | Value |
|---|---|
| Die | 10 × 10 mm, centre (0, 0) |
| Detector cells | 8 (D1–D8) at x = −2700, −900, +900, +2700 µm; y = +1200 (D1–D4) and −1200 (D5–D8) µm |
| Cell content | The A30 detector with the A30 contact chain: NbN tab → Ti/Au strip and pad → opening in the SiO₂ cap → Au lead → Au bond pad. A 30 × 30 µm Au window; its own Al mirror and mirror ground via; four e-beam crosses at (±300, ±700) µm from the cell centre |
| Layer-20 dose datatype and factor | D1 1 (0.80), D2 2 (0.87), D3 3 (0.93), D4 0 (1.00); D5 0 (1.00), D6 5 (1.07), D7 6 (1.13), D8 7 (1.20). Datatype 4 is not used |
| Bond pads | 16 Au pads, 120 × 200 µm, at y = ±4720 µm (the signal lead is the inner lead on the top row; the return lead is the inner lead on the bottom row). Positions in the pads CSV |
| Ground | Au ground fill with four bond spots GND-1 … 4 at (±4700, ±1500) µm (labels only, on layer 100) |
| Process monitors (probe station only, not wire bonded) | T3 NbN four-wire bar at (−3000, −250) µm. T11 Au-to-Al via chain at the die centre |
| Marks | Four sites at (±4300, ±4830) µm, as on the trap dies |
| Areas | Au (layer 50) 0.937 cm²; layer 20 13 724 µm² |
| Checks | `check_snspd_die.py`: ALL CHECKS PASS. Each cell's layers 20, 22, 40 and 50 near the detector equal the A30 die translated. `check_run.py R1_ONE`: ALL CHECKS PASS |

The meander is never mirrored or rotated: its lines run along x in every cell. Each cell is the A30 detector translated, so the A30 and SNSPD-only dies share the same detector geometry (layers 20, 22, 40 and 50 near the detector).

Bond pads: the SNSPD-only die's cells have Au bond pads. The test dies do not (below).

## Test structures

**Not in R1_ONE.** The test dies (`test_die_v4`, `test_die_v4_TRAP`) are kept as files, and their structures are kept as listed below, but R1_ONE does not contain them. The two process monitors that R1_ONE does keep (T3 and T11) are on the SNSPD-only die.

Generator: `gds/make_test_die.py` (10 × 2.5 mm; `--trap-only` for TEST_TRAP). Checker: `gds/check_test_die.py` (`ALL CHECKS PASS`). Test-die L1 marks at (−1700, ±1080) and (4300, ±1080) µm. Test dies have no bond pads. The SNSPD-only die's cells do have Au bond pads.

| Structure | Where (x, y) µm | What it is for |
|---|---|---|
| T1 Au comb, 5 µm gap | (−4300, 350) | DC leakage and flashover across the trap gap (Dietl 2025, Sterling 2013). In TEST_TRAP |
| T2v Au / SiO₂ / Al capacitor | (−2700, 400) | Au top plate 200 µm over an Al plate 240 µm, dielectric = 238 nm spacer + 160 nm cap. Expected ≈ 3.5 pF [team calc] |
| T3 NbN 4-wire bar | (−1000, 250) | R_sq and Tc of the patterned NbN film. 200 × 10 µm with Ti/Au pads |
| T4 spare SNSPD (A30 meander) | (600, 450) | A30 geometry on its own local Al mirror, with a mirror probe pad |
| T4b spare SNSPD (B60 meander) | (2300, 450) | B60 geometry on its own local Al mirror |
| T6 Au continuity loop, 6 µm line | (3500, 300) | Two-pad continuity loop (Dietl 2025). In TEST_TRAP |
| T8 EBL dose array | (−1000, −650), 600 µm pitch | Seven A30 meanders on L20 datatypes 1–7; dose factors 0.80 … 1.20 × the nominal (`DOSE_FACTORS`). SEM linewidth, then 2-wire R at room temperature and cold |
| T9 geometry array | seven slots at y = −650 (x = −4380 … −2000, and 3160 and 3760 for the straight pairs), plus one meander at (−100, 450) | Wire width and pitch variants, turn shape, length series, straight Ic references (DESIGN_LOG step 24). Compared as ratios between neighbours |
| T10 Al mirror strip, four-point | y = −100, current pads at x = −4570 and −1920; taps at x = −4455 and −1945 | Mirror strip resistance over 2510 µm, the trap's mirror ground path. Full test die only (not in TEST_TRAP) |
| T11 Au-to-Al via chain | y = −100, x = 1700 … 2950 | Four vias in series: Au pad, Al island, Au strap, Al island, Au pad |
| T12 twin Au leads over Al | y = −100, x = −1600 … 1100 | Two 5 µm Au leads 5 µm apart over an Al strip, modelling the SNSPD leads in the trap's slot |

Test-die notes:
- T4 and T4b keep the meander's 32 µm radial span (`DET_WY`); the module docstring says 34 µm, which the code does not use.
- Probe access, as drawn in `make_test_die.py`:
  - each meander has two Ti/Au (L22) probe pads on its left, opened through the cap (L40);
  - each meander's local mirror has its own Al contact on the right, opened through the cap and spacer (L40) and covered by a 100 µm Au pad (L50);
  - T2v, T10 and the other Al probe pads use the same pattern: Al pad (L10), 70 µm opening (L40), Au probe pad (L50).

## Protections checked by check_chip.py

`check_chip.py` checks each trap die. The list is its module docstring: a pass means `ALL CHECKS PASS`.

| Group | What is checked |
|---|---|
| Conductors | every electrode and SNSPD lead seed is on its own Au conductor (no shorts); each reaches a pad near the die edge; no floating Au; minimum spacing ≥ 5 µm; no Au narrower than 4.9 µm |
| Layers | one top cell; no text on fab layers; all metal ≥ 90 µm from the dicing edge; layers 24, 30, 31 and 45 empty |
| SNSPD | leads inside the centre-DC slot and inside the trap; no Ti/Au (L22) inside the trap except the contacts by the detector (no buried leads); each L40 contact ≥ 1 µm inside its Au lead and its Ti/Au pad; the readout window is open in the Au; NbN rules (|y| ≤ 17 µm, all NbN under Au or the window, gaps ≥ 60 nm, no turn or tab in the light footprint) |
| Mirror | Al (L10) never under the RF rails; covers all NbN by ≥ 5 µm; at least one ground via inside the Au fill, enclosed ≥ 25 µm by fill Au and Al |
| Plain die | nothing on layers 10, 20, 22, 40; solid centre DC at the readout zone |
| Pads | no pad in the die corners (\|x\|, \|y\| > 4 mm); signal pads not on ground; GND spots on ground |
| Marks | L1 marks not under Al |

`make_test_die.py` has its own self-check (keep-out boxes do not overlap, all keep-outs inside the die, layers 24, 30, 31, 45 empty; in `--trap-only` also layers 10, 20, 22, 40 empty). `check_test_die.py` is written from the specification, not from the generator.

## Resolved items (v2, carried into v3, changed in v4)

### A.1 Resolved in the GDS (v2, carried into v3)

| # | Was | Now in the GDS (v4) |
|---|---|---|
| A1 | L1 marks under the die-wide M1 Al | No layer-10 polygon at any mark site (the Al is only the local mirror under the detector), so no cut-outs. Test-die L1 marks at (−1700, ±1080) and (4300, ±1080) |
| A2 | No EBL marks on L22 | Trap dies: L22 crosses at (−60, ±700) and (540, ±700) µm (moved from (0, ±700) and (600, ±700) in v3). Test dies: one L22 cross at each mark site, 90 µm −x of the L1 cross |
| A3 | Protect layer for the gap etch | Retired in v4. Layer 45 is empty, there is no gap etch and no 10 µm SiO₂ (D2), so there is no window protect patch |
| A4 | Ground fill had no link to M1 | Ground fill bond spots GND-1 … GND-4 at (±4700, ±1500). The v3 fill-to-M1 vias and M1 bond openings are gone; one mirror ground via at (−2140, 130) µm ties the local mirror to the fill (100 × 100 µm, enclosed ≥ 25 µm) |
| A5, A6 | ITO test and flush radial ITO edges | Moot: no ITO since v3, none in v4 |
| A7 | Single die only | R&D runs `run_R1_TRAP.gds` and `run_R1_FULL.gds` (8 dies each; both superseded 2026-11-12 by `run_R1_ONE.gds`, 9 dies; [mask list, section 3](mask_list.md#3-rd-runs-make_runpy-and-the-full-wafer-reference)); full-wafer reference `wafer_v4.gds` (56 dies) |

## Alignment coordinates used by the recipes

Trap L1 marks: **(±4300, ±4830) µm**. Trap L40 crosses: **(±4300, ±4758) µm**, 72 µm inward along y. Trap L22 EBL crosses: **(−60, ±700) and (540, ±700) µm**. Test L1 sites: **(−1700, ±1080) and (4300, ±1080) µm**; their L40 crosses are 72 µm further in +y. Add the run-map die centre for wafer coordinates (`run_<name>_map.csv`).

SNSPD-only die: L1 marks at (±4300, ±4830) µm, as on the trap dies. Its e-beam crosses are four per cell, at (xc ± 300, yc ± 700) µm from each cell centre (about 760 µm from the meander) [verify the alignment procedure].

The positions follow the v4 generators. The v3 trap marks at (±2150, ±1080) and the v3 EBL crosses at (0, ±700) and (600, ±700) are gone.

## Regenerate and check (current files)

Run from `design/sim`. Order matters: runs import the die files.

```bash
./run.sh ../gds/make_chip.py && ./run.sh ../gds/make_chip.py --det60 && ./run.sh ../gds/make_chip.py --nodet
./run.sh ../gds/make_snspd_die.py                # writes snspd_die_v4.gds, pads CSV, preview PNG [verify arguments]
./run.sh ../gds/check_snspd_die.py               # must print ALL CHECKS PASS [verify arguments]
./run.sh ../gds/make_run.py R1_ONE               # writes run_R1_ONE.gds, _map.csv, _map.png (the old runs are superseded; do not regenerate them)
./run.sh ../gds/check_run.py R1_ONE              # must print ALL CHECKS PASS
for v in A30 B60 NODET; do ./run.sh ../gds/check_chip.py trap_die_v4_$v; done
```

`measure_dies.py` does not list `run_R1_ONE` or `snspd_die_v4` yet, so the R1_ONE layer areas on the other pages are [verify] until it is rerun.

See the [exposure checklist](mask_list.md#4-export-checklist-per-job) for polarity and overlay, and [detector reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts) for the open T9 and test-die items.
