> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Steps 17 to 19 test dice and package

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md) · [Test plan](../test_plan.md) · [Local mirror (v4)](../variants/LOCAL_MIRROR.md)

Use die IDs from the run map. Detector measurements apply only where present. [Electrical tests](../test_plan.md) precede dicing and repeat after packaging.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## Changed from v3

This page follows the v4 local-mirror architecture ([Local mirror H.2, steps 17–19](../variants/LOCAL_MIRROR.md); DESIGN_LOG steps 25–29).

- **No Al bond openings and no Al wedge bonds.** The local Al mirror (layer 10) is grounded on chip through one via under the Au ground fill. Ground is reached through the four Au ground-fill spots at (±4700, ±1500).
- **All pads are Au (layer 50).** SNS and SNG are Au pads (200 × 150 µm) on the Au leads in the centre-DC slot. In v3 they were Ti/Au under SiO₂ openings.
- **Pad pitch 360 µm** on the outer DC rows. The layout is generated and validated; team adoption is pending.
- **Test structures** in step 17 are the v4 set. The v4 test-die layout is drawn and checked (2026-11-09).
- **Electrode Au** (E1 or E2) is still open. Both options are written out where they differ.
- **Removed for v4:** the 10 µm D2 and its openings, the protect resist, the M1 bond and probe pads, and the recessed SNSPD openings. Steps keep their numbers.

## 17. Room-temperature wafer-level electrical test (before dicing)

- Limits and protocol: [test plan](../test_plan.md). Its values are draft **[verify]**. The "Dietl 2025" source for them is identified (see the [literature note](../../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md)); the limits themselves are still **[verify]**.
- Test structures on the v4 test dies:

  | Structure | Description |
  |---|---|
  | T1 | Au comb, 5 µm gaps |
  | T6 | Au continuity loop |
  | T2v | Au / SiO₂ / Al capacitor |
  | T10 | Al mirror strip, four-point; expected 18.8–25.1 Ω at 100 nm Al (`sim/10c`, DESIGN_LOG step 37) [team calc]. Acceptance not yet set **[verify]** |
  | T11 | Au-to-Al via chain |
  | T12 | Twin Au leads over the inlaid Al strip, across its planar edge |
  | T3 | NbN bar |
  | T4, T4b | Spare SNSPDs |
  | T8 | EBL dose array |
  | T9 | SNSPD geometry array |

  The v4 test dies are drawn and checked (`gds/test_die_v4.gds`, 2026-11-09), and the table above is that set.
- Ground link: fill to mirror through the on-chip via ([test plan](../test_plan.md); the < 10 Ω figure there is the v3 limit, see [step 15](03_ELECTRODES.md#15-e2-strip-descum-seed-removal) **[verify: replacement limit]**). There is no mirror probe opening on the trap die. The check is made on the test die: T11 for the via contact, T10 for the strip, and the mirror probe pads on T4/T4b.
- R1_TRAP has no Al. Its trap die (NODET) has no mirror, so the Al checks above apply only to A30 and B60 runs.
- Record pass/fail per die against the die IDs in `gds/run_<name>_map.csv`. Dies that fail go to destructive tests: T1 flashover, cross-sections.
- [ ] Done — date: ____ operator: ____ yield: ____ notes: ____

## 18. Protect, dice (10 × 10 mm trap dies, 10 × 2.5 mm test dies), strip

- **Recipe:**
  - Protective resist ≥ 8 µm, which covers the 6 µm Au (option E2). For E1 (0.35 µm Au) the same thickness is kept **[verify]**.
  - Diesaw-DAD3240 with a Si blade, **[verify blade / recipe with staff]**. Dice on the die outlines from `gds/make_run.py` and `gds/make_wafer.py`. Layer 101 (outlines) is not written in the v4 GDS ([layer map](../../gds/layer_map.md)) **[verify]**.
  - x streets on a 10.2 mm pitch run straight through. The y streets follow the stacked column (10 mm trap dies and 2.5 mm test dies, `make_run.py` / `make_wafer.py`); all columns use the same stack, so the y cuts also run straight through. Streets are 200 µm wide. The kerf plus chipping must fit in the 200 µm street **[verify blade width]**.
  - Remove the tape in acetone (JoVE), then acetone/IPA strip.
  - **No ultrasonic** [inference].
- **Inspect:**
  - Chipping < 50 µm **[verify]**.
  - Au and Al are kept ≥ 90 µm from the dicing edge (`check_chip.py`, [DESIGN_LOG step 8](../../DESIGN_LOG.md)). Check chipping against that margin.
  - Meander R₄.
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
  - **Bond the Au ground fill to carrier ground at GND-1…4, at least 2 of them.** The Al mirror reaches this fill through its on-chip via. The v4 dies have no separate M1 bond pads, and NODET has no Al. The ground-link check is in step 17. The electrical protocol still names M1 pads in its a13 wording, so that check needs a v4 rewrite **[verify]**.
  - Bond off the top and bottom edges for the four pad rows, off the right edge for RF (4700, 0), and off the left edge for C and the SNSPD pads. Pads stay at |x| ≤ 3.5 mm on the top and bottom edges and near y = 0 on the side edges, away from the beam exits near the corners (|x| or |y| ≈ 4.7 mm). Keep the loops low anyway.
  - Bond the SNSPD pads last, wearing a strap. Short the carrier SNSPD pins until installation [inference].
- **SNSPD RF termination: open.** The SNSPD leads are Au in the centre-DC slot. Each collects about 46 µA (E2) or 29 µA (E1) of common-mode RF (DESIGN_LOG step 26; `sim/10c`, DESIGN_LOG step 37, gives 44.5 / 28.6 µA on the 2.24 mm lead). Whether the nanowire sees this depends on the termination at SNS and SNG. This belongs to the open **RF grounding / filters** decision in [open decisions](../OPEN_DECISIONS.md). Its options there are centre-DC filtering, carrier grounds, symmetric detector termination or cancellation, and for v4 an RF bypass at both SNSPD lead pads.
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
- [x] **Test dies for v4:** the T2v, T10, T11 and T12 structures are drawn and checked (`gds/test_die_v4.gds`, `gds/check_test_die.py`); done 2026-11-09. TEST_TRAP has no Al (T1 and T6 only, on layers 1 and 50).
- [ ] **Mirror strip:** acceptance for the T10 strip resistance (18.8–25.1 Ω at 100 nm Al, `sim/10c`, DESIGN_LOG step 37) is not set [verify]. There is no mirror probe opening on the trap dies and none is planned; the mirror is measured on T10, T11 and the T4/T4b probe pads.
- [ ] **Bonding:** W7 bond-and-leak on the final stack, and wedge bonding on E1 evaporated Au **[verify]**.
- [ ] **Ground-link check:** rewrite the a13 wording for v4 pads (no M1 bond pads) **[verify]**.
- [ ] **Dicing outlines:** layer 101 is not written in v4; confirm the street outlines with staff **[verify]**.

Continue: [next stage](../test_plan.md).
