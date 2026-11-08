> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Die layout and alignment

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

Earlier layouts are archived: v1 (square die, trap in a corner) in `gds/archive_v1_square/`, v2 (narrow 10 × 2.5 mm die, two-ITO window) in `gds/archive_v2_narrow/`. Use v3 files for the current runs.

**Trap die floorplan** (`gds/make_chip.py`; `check_chip.py` passes on all three v3 dies, 2026-11-07). GDS µm, die centre at (0, 0):

| Feature | Location |
|---|---|
| Die (L101) | 10 × 10 mm: x = ±5000, y = ±5000 |
| Trap axis | die centre line, y = 0 |
| RF rails | x = −2000 … +2000, U closed at the right (+x) end; RF pad (4700, 0) on the right die edge |
| Zones | loading x = −300, readout (SNSPD, window) x = +300 |
| Segments | 15 + 15 at 100 µm pitch, centres x = −700 … +700; outer DC depth 200 µm |
| Edge pads | 120 × 200 µm Au, four rows along the top and bottom die edges at y = ±4720 (moved in 60 µm in step 21 so a 50 µm fill strip runs outboard of the rows): TL1–TL8 at x = −3500 … −2240, TR1–TR9 at x = +3500 … +2060 (same x for BL / BR) |
| Left die edge | centre-DC pad C (−4650, 0); SNSPD pads SNS (−4750, +260) and SNG (−4750, −260) |
| Ground | Au ground-fill bond spots GND-1…4 at (±4700, ±1500); M1 bond openings M1-1…4 at (±4700, ±2000), on the left/right die edges; eight 150 × 150 µm fill-to-M1 ground vias (L40 under the Au fill) at (±4700, ±1000) and (±1000, ±2500) (DESIGN_LOG step 22) |
| Alignment marks | L1 at (±4300, ±4830), in edge notches of the Au ground fill |
| Full pad list | [trap_die_v3_A30_pads.csv](../gds/trap_die_v3_A30_pads.csv) (`_B60_pads.csv` is identical) |

**Beam clearance** (`sim/11_beam_clearance.py`, full 10 mm chip) [team calc]: with the trap on the centre line of a 10 × 10 mm die, about **1.7 × 10⁻² of a 493 nm beam** (3.2 × 10⁻² at 650 nm, 9.6 × 10⁻³ at 405 nm) hits the surface, vs 1.1 × 10⁻⁵ on the v2 2.5 mm die. Team decision 2026-11-07 (DESIGN_LOG step 18). The 45° beams through the zones leave the die at the top/bottom edges near \|x\| ≈ 4.7 mm and the side edges near \|y\| ≈ 4.7 mm; no pad sits in the corners \|x\|, \|y\| > 4 mm (`check_chip.py`).

**Test structures** are not on the trap die. The list below describes the earlier v3 test die; the current generator adds **T9** and uses v3.1 meanders for T4/T4b/T8 (see [Variants](VARIANTS.md#detector-revision)). They are on `gds/test_die_v3.gds` (`make_test_die.py`, 10 × 2.5 mm, same layer stack): T1 Au comb (5 µm gap), T2 Au/D2/M1 capacitor 0.8 × 0.8 mm + M1 pad, T3 NbN 4-wire bar, T4 spare SNSPD 30 × 30 and T4b spare SNSPD 60 × 30 (under SiO₂ cap + D2 only), T6 Au continuity loop, T8 EBL dose array (T5 and T7 were ITO tests and are gone in v3) (seven 30 × 30 µm meanders on L20 datatypes 1–7, factors 0.80–1.20 × nominal; [EBL job](mask_list.md#2-ebl-job-for-layer-20-nbn)). Each run layout has two test dies.

**Plain trap die, no SNSPD** (`gds/trap_die_v3_NODET.gds`, `make_chip.py --nodet`, DESIGN_LOG step 14):

- Same electrodes, pads, marks and M1 bond openings as A30. It has no window (solid centre DC) and nothing on L20 or L22.
- It is in both run layouts (`run_R1_TRAP`, `run_R1_FULL`) but not on `wafer_v3.gds`. On a mixed wafer it simply receives no features in those layers' steps.
- **Trap-only wafer:** run steps 0–3, 9, 11–19 and skip steps 4–8. D2 (step 9) then goes directly on M1. Keep it 10 µm, which is the `ground_depth` the simulation assumes.
- Step 11 opens the four M1 bond openings, eight fill-to-M1 ground vias and the L50 alignment crosses.
- Step 17 drops the SNSPD tests.

**Wafer jobs** use the run GDS, `gds/run_<name>.gds`: one MLA job per layer and one EBL job for L20, writing only the run's block at the wafer centre ([run plan](RUN_PLAN.md)).

### A.1 Resolved in the GDS (v2, carried into v3)

| # | Was | Now in the GDS |
|---|---|---|
| A1 | L1 marks under M1 Al | 300 × 300 µm M1 cut-outs at every mark site (trap die: edge notches at (±4300, ±4830); test die: (−1700, ±1080), (4300, ±1080)) |
| A2 | No EBL marks on L22 | 20 µm L22 crosses (2 µm arms) at (0, ±700) and (600, ±700) around the readout zone, plus one at every mark site |
| A3 | No protect layer for the gap etch | L45 PROTECT is drawn: every bond/probe D2 opening + 10 µm, readout window + 2.5 µm, SNSPD-lead branch region at the left end (x = −4835 … −4430, \|y\| ≤ 330). On the test die also the T3 and T4/T4b areas. Used in step 16a. **In v3 the window patch is essential**: with no ITO, nothing else stops the gap etch going down through the window SiO₂ toward the NbN |
| A4 | Ground fill had no bond pad, and no link to M1 | GND-1…4 bond spots on the fill, listed in `*_pads.csv`. **Step 22 (v3, 2026-11-08):** eight L40 vias under the fill tie it to M1 on chip, as Hampel 2023 grounds its mirror. M1 no longer depends on a bond wire to stay grounded; the M1-1…4 openings remain as a backup |
| A5 | No probe-able buried-ITO → Al test | Moot in v3 (no ITO); T7 removed |
| A6 | Top-ITO radial edges flush with the centre-DC Au edge | Moot in v3 (no ITO) |
| A7 | Single die only | Full-wafer reference `gds/make_wafer.py` → `wafer_v3.gds` (56 dies); R&D run layouts `gds/make_run.py` → `run_R1_TRAP.gds`, `run_R1_FULL.gds` (8 dies each, [run plan](RUN_PLAN.md)) |

## Alignment coordinates used by the recipes

Trap L1 marks: **(±4300, ±4830) µm**. L40 cross centres: **(±4300, ±4758) µm**, 72 µm inward along y. Test L1 sites: (−1700, ±1080) and (4300, ±1080) µm; their L40 centres are offset +72 µm in y. Add the run-map die centre for wafer coordinates. These positions follow the working generators; (±2150, ±1080) were the old v2 trap marks.

See the [exposure checklist](mask_list.md#4-export-checklist-per-job) for polarity and overlay, and [detector reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts) for the current T9/test-die changes.
