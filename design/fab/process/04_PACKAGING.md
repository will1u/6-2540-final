> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm 2026-11-09; final stack and R1_ONE 2026-11-12.

# Steps 17 to 19 test dice and package

[Traveler](../TRAVELER.md) · [R1_TRAP sheet (superseded for R1_ONE)](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md) · [Test plan](../test_plan.md) · [Local mirror (v4)](../variants/LOCAL_MIRROR.md)

Use die IDs from the run map (`gds/run_R1_ONE_map.csv`). Detector measurements apply only where present. [Electrical tests](../test_plan.md) precede dicing and repeat after packaging.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## Changed from v3

This page follows the v4 local-mirror architecture ([Local mirror H.2, steps 17–19](../variants/LOCAL_MIRROR.md); DESIGN_LOG steps 25–29, 45).

**Changed 2026-11-12 (R1_ONE)**
- **Run:** R1_ONE, one 3 × 3 wafer block: 4 A30, 1 B60 (spare), 2 SNSPD-only, 2 NODET. R1_TRAP and R1_FULL are superseded.
- **Dicing:** one 10.2 mm pitch in both directions; cuts at x and y = −15300, −5100, +5100, +15300 µm; 9 dies.
- **Test structures:** on R1_ONE the test dies are not used. Measurements are on the SNSPD-only die (T3, T11, the eight detector cells) and on the trap dies. See step 17.

**Changed in v4 (kept)**
- **No Al bond openings and no Al wedge bonds.** The local Al mirror (layer 10) is grounded on chip through one via under the Au ground fill. Ground is reached through the four Au ground-fill spots at (±4700, ±1500).
- **All pads are Au (layer 50).** SNS and SNG are Au pads (200 × 150 µm) on the Au leads in the centre-DC slot. In v3 they were Ti/Au under SiO₂ openings.
- **Pad pitch 360 µm** on the outer DC rows. The layout is generated and validated; team adoption is pending.
- **Electrode Au** (E1 or E2) is still open. Both options are written out where they differ.
- **Removed for v4:** the 10 µm D2 and its openings, the protect resist, the M1 bond and probe pads, and the recessed SNSPD openings. Steps keep their numbers.

## 17. Room-temperature wafer-level electrical test (before dicing)

- Limits and protocol: [test plan](../test_plan.md). Its values are draft **[verify]**. The "Dietl 2025" source for them is identified (see the [literature note](../../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md)); the limits themselves are still **[verify]**.
- Test structures on R1_ONE, by where the measurement is made:

  | Structure | Where on R1_ONE | Description |
  |---|---|---|
  | T3 | SNSPD-only die, probe station only | NbN four-wire bar (Rsq) |
  | T11 | SNSPD-only die, centre | Au-to-Al via chain (the mirror via contact) |
  | D1–D8 | SNSPD-only die, eight cells | The A30 detector with its contact chain, own Al mirror and ground via |
  | Trap dies | A30, B60 and NODET | Electrode leakage and pad-to-pad isolation through the pads |
  | Not in R1_ONE | – | T1, T2v, T4, T4b, T6, T8, T9, T10, T12, TEST, TEST_TRAP. The mirror strip (T10) is not measured on this run; 18.8–25.1 Ω at 100 nm Al is a calculated value (`sim/10c`, DESIGN_LOG step 37) [team calc] |

  The SNSPD-only die is `snspd_die_v4` (new; `gds/check_snspd_die.py` ALL CHECKS PASS).
- Ground link: fill to mirror through the on-chip via ([test plan](../test_plan.md); the < 10 Ω figure there is the v3 limit, see [step 15](03_ELECTRODES.md#15-e2-strip-descum-seed-removal) **[verify: replacement limit]**). On R1_ONE the via is checked by T11 on the SNSPD-only die. There is no mirror probe opening on the trap dies, and no mirror probe pad on the trap dies.
- R1_ONE NODET dies have no Al except the four corner marks. The Al checks above apply to A30, B60 and SNSPD-only dies.
- R1_ONE NODET dies have no detector entries. Use the die ID from the run map.
- Record pass/fail per die against the die IDs in `gds/run_R1_ONE_map.csv`. Dies that fail go to destructive tests on a rejected die or on the second wafer [verify].
- [ ] Done — date: ____ operator: ____ yield: ____ notes: ____

## 18. Protect, dice (10 × 10 mm trap dies, 10 × 2.5 mm test dies), strip

- **Recipe:**
  - Protective resist ≥ 8 µm, which covers the 6 µm Au (option E2). For E1 (0.35 µm Au) the same thickness is kept **[verify]**.
  - Diesaw-DAD3240 with a Si blade, **[verify blade / recipe with staff]**. Dice on the die outlines from `gds/make_run.py` (run `R1_ONE`) and `gds/make_wafer.py`. Layer 101 (outlines) is not written in the v4 GDS ([layer map](../../gds/layer_map.md)) **[verify]**.
  - **R1_ONE saw cuts:** x and y at −15300, −5100, +5100, +15300 µm: one 10.2 mm pitch both ways, 9 dies. The streets are 200 µm wide; every row and column is the same 10 mm die, so the cuts run straight through. The kerf plus chipping must fit in the 200 µm street **[verify blade width]**.
  - Remove the tape in acetone (JoVE), then acetone/IPA strip.
  - **No ultrasonic** [inference].
- **Inspect:**
  - Chipping < 50 µm **[verify]**.
  - Au and Al are kept ≥ 90 µm from the dicing edge (`check_chip.py`, [DESIGN_LOG step 8](../../DESIGN_LOG.md)). Check chipping against that margin.
  - Meander R₄ on the SNSPD-only dies and on the A30 and B60 dies.
- **Hazards:** ESD from the saw spray. Use the saw's standard CO₂-bubbled DI [inference, verify].
- [ ] Done — date: ____ operator: ____ notes: ____

## 19. Package

- **Carrier: open.** Choice between a PGA84L-like 84-pin package, a 100-pin CPGA, and the lab's carrier. Cryostat fit is **[verify]**. Step 29 checks the nominal PGA84L finger geometry only. The finger IDs in the fan-out table are local, not electrical pin numbers.
- **Package spacer: open, proposal only.** Proposed ≥ approximately 0.6 mm thick, die-sized (10 × 10 mm) or larger, Si suggested. Not adopted **[verify actual carrier, die and spacer stack]**.
- **Pad pitch: 360 µm, team adoption pending.** Generated and validated in step 29. Adoption waits on review of future perpendicular beam access near the zones. Alternatives recorded: 180, 240, 300, 400 µm. The only reason supplied is keeping wire angles below 45° for a PGA84L-like package. Worst wire angle is 20.03° (bottom edge, BL1 → B03; [team calc], nominal PGA84L cavity; [fan-out table](../../sim/out/16_pad_pitch_check/fanout.csv), [diagram](../../sim/out/16_pad_pitch_check/fanout.png)).
- **Die attach:**
  - Cryo-compatible epoxy cured ≤ 150 °C [verify product/cure], e.g. EPO-TEK 353ND as listed by JoVE.
  - Au/Sn (Leibrandt) needs a Au backside. Our backside is SiO₂ (D1 on both sides), so it does not apply as written.
- **Wire bonds:**
  - Au wire on Au pads (Wirebond-Wedge or -Ball).
  - Pad sizes: 120 × 200 µm on the top and bottom edges, 200 × 200 µm for RF and C, and 200 × 150 µm for SNS/SNG. The Au ground fill stays ≥ 30 µm from signal pads.
  - **Bonding surface depends on the electrode option.** E2 (6 µm plated Au): plated Au must be wire-bond grade (soft, ≈ ≤ 90 Knoop, vendor figure) [verify with MIT.nano for the bath, or test-bond W5 coupons with and without an anneal]. E1 (0.35 µm evaporated Au): wedge bonding onto it is **[verify]**; qualify it on W7 ([qualification](../QUALIFICATION.md)).
  - **Wedge-bond the SNSPD pads; no ball bonding there** (the ball bonder's flame-off spark is a risk to electrically sensitive devices: EPFL CMi HB10 guidelines) [inference for NbN].
  - **RF pad: 2–4 wires** in parallel (Sandia Phoenix/Peregrine bonds RF with 7 wires, arXiv:2009.02398 Sec. 5.3; `research/reports/Bond pad sizing for ion traps.md`).
  - **Probe at one end of each pad and bond at the other** (step 17 probe marks can hide pad damage) [inference].
  - **Bond the Au ground fill to carrier ground at GND-1…4, at least 2 of them.** The Al mirror reaches this fill through its on-chip via. The v4 dies have no separate M1 bond pads, and NODET has no Al mirror (only the four corner marks). The ground-link check is in step 17. The electrical protocol still names M1 pads in its a13 wording, so that check needs a v4 rewrite **[verify]**.
  - Bond off the top and bottom edges for the four pad rows, off the right edge for RF (4700, 0), and off the left edge for C and the SNSPD pads. Pads stay at |x| ≤ 3.5 mm on the top and bottom edges and near y = 0 on the side edges, away from the beam exits near the corners (|x| or |y| ≈ 4.7 mm). Keep the loops low anyway.
  - Bond the SNSPD pads last, wearing a strap. Short the carrier SNSPD pins until installation [inference].
- **SNSPD RF termination: open.** The SNSPD leads are Au in the centre-DC slot. Each collects 44.5 µA (E2) or 28.4 µA (E1) of common-mode RF on its 2.24 mm between the RF rails (`sim/10c`, DESIGN_LOG step 37). Whether the nanowire sees this depends on the termination at SNS and SNG. This belongs to the open **RF grounding / filters** decision in [open decisions](../OPEN_DECISIONS.md). Its options there are centre-DC filtering, carrier grounds, symmetric detector termination or cancellation, and for v4 an RF bypass at both SNSPD lead pads.
- **Bond map.** Pad positions and electrode numbers come from [trap_die_v4_A30_pads.csv](../../gds/trap_die_v4_A30_pads.csv). B60 has the same positions; the [NODET CSV](../../gds/trap_die_v4_NODET_pads.csv) omits SNS and SNG. Top and bottom rows run at y = ±4720 µm at 360 µm pitch.

  | Pad(s) | Electrode(s) | Role | Wire |
  |---|---|---|---|
  | TL1, TR1 / BL1, BR1 | 33, 34 / 35, 36 | top / bottom cap, left and right | Au |
  | TL2–TL8 / BL2–BL8 | 3 → 9 / 18 → 24 | top / bottom segments, left side of the readout zone | Au |
  | TR2–TR9 / BR2–BR9 | 17 → 10 / 32 → 25 | top / bottom segments, right side of the readout zone | Au |
  | C | 2 | centre DC, (−4650, 450) | Au |
  | SNS / SNG | SNSPD_S / SNSPD_G | SNSPD signal / return, (−4750, ±100) | Au |
  | RF | 1 | RF, (4700, 0) | Au |
  | GND-1…4 | Au ground fill | (±4700, ±1500); ≥ 2 bonds | Au |

  The carrier pin column is blank: the carrier is open. The [centre-to-centre fan-out table](../../sim/out/16_pad_pitch_check/fanout.csv) uses nominal pad and finger centres. Fill in actual carrier pins after the package is chosen. The table has one connection per chip pad; extra RF wires belong to the final bond plan.
- **After packaging:** repeat the pad-to-pad isolation through the carrier pins, plus meander R₅.
- [ ] Done — date: ____ operator: ____ carrier: ____ notes: ____

## Open before packaging

Mirrors the open decisions in [open decisions](../OPEN_DECISIONS.md). Items marked adopted are not open.

- [ ] **Electrode Au: E1 (0.35 µm lift-off) vs E2 (6 µm plated).** Blocks the v4 traveler rewrite. Changes the bonding surface (step 19) and the protective resist (step 18).
- [ ] **Pad pitch 360 µm:** team adoption, and clearance for a future perpendicular beam near the zones.
- [ ] **Carrier:** PGA84L-like 84-pin, 100-pin CPGA, or the lab carrier. Needs a cryostat fit and a carrier-specific electrical pin map.
- [ ] **Package spacer:** thickness, size and material (proposal ≥ approximately 0.6 mm, die-sized or larger, Si suggested) **[verify]**.
- [ ] **RF grounding / filters:** filtering, carrier grounds, symmetric or cancelled termination, and an RF bypass at the SNS and SNG pads.
- [x] **Test structures for R1_ONE:** the SNSPD-only die `snspd_die_v4` (T3, T11, eight cells) is drawn and checked by `gds/check_snspd_die.py`. The 2026-11-09 test dies (`test_die_v4`) are not in R1_ONE.
- [ ] **Mirror strip:** acceptance for the T10 strip resistance (18.8–25.1 Ω at 100 nm Al, `sim/10c`, DESIGN_LOG step 37) is not set [verify]. T10 is not on R1_ONE, so the strip is not measured in this run.
- [ ] **Bonding:** W7 bond-and-leak on the final stack, and wedge bonding on E1 evaporated Au **[verify]**.
- [ ] **Ground-link check:** rewrite the a13 wording for v4 pads (no M1 bond pads) **[verify]**.
- [ ] **Dicing outlines:** layer 101 is not written in v4; confirm the street outlines with staff **[verify]**.

Continue: [next stage](../test_plan.md).
