> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Steps 17 to 19 test dice and package

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

Use die IDs from the run map. Detector measurements apply only where present. [Electrical tests](../tests/01_ELECTRICAL.md) precede dicing and repeat after packaging.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 17. Room-temperature wafer-level electrical test (before dicing)

- Protocol in [electrical protocol](../tests/01_ELECTRICAL.md): Dietl 2025 limits, Stick > 100 MΩ.
- Record pass/fail per die against the die IDs in `gds/run_<name>_map.csv`. Test dies (T1–T4b, T6, T8 and current T9) stand in for the trap dies of their run. Dies that fail go to destructive tests: T1 flashover, cross-sections.
- [ ] Done — date: ____ operator: ____ yield: ____ notes: ____

## 18. Protect, dice (10 × 10 mm trap dies, 10 × 2.5 mm test dies), strip

- **Recipe:**
  - Protective resist ≥ 8 µm (covers the 6 µm Au).
  - Diesaw-DAD3240 with a Si blade, on the L101 outlines [verify blade / recipe with staff]. x streets on a 10.2 mm pitch run straight through. The y streets follow the stacked column (10 mm trap dies and 2.5 mm test dies, `make_run.py` / `make_wafer.py`); all columns use the same stack, so the y cuts also run straight through. Streets are 200 µm wide. The kerf plus chipping must fit in the 200 µm street [verify blade width].
  - Remove the tape in acetone (JoVE), then acetone/IPA strip.
  - **No ultrasonic** [inference].
- **Inspect:** chipping < 50 µm [verify] (the Au is pulled back 100 µm and M1 150 µm from the die edge); meander R₄.
- **Hazards:** ESD from the saw spray. Use the saw's standard CO₂-bubbled DI [inference, verify].
- [ ] Done — date: ____ operator: ____ notes: ____

## 19. Package

- **Carrier:** choice remains open between a PGA84L-like 84-pin package, a 100-pin CPGA, and the lab's carrier [verify cryostat fit; see open decisions]. Step 29 checks the nominal PGA84L finger geometry. Spacer proposal: ≥ approximately 0.6 mm thick, die-sized (10 × 10 mm) or larger, with Si suggested [verify actual package stack].
- **v4 bond-map update (step 29):** the coordinates below describe the current generated v4 dies. The 360 µm pitch has passed layout and simulation checks; team adoption is pending review of future perpendicular beam access. The broader traveler rewrite still waits on E1/E2.
- **Die attach:**
  - Cryo-compatible epoxy cured ≤ 150 °C [verify product/cure], e.g. EPO-TEK 353ND as listed by JoVE.
  - Au/Sn (Leibrandt) needs a metallised backside, and ours is SiO₂.
- **Wire bonds:**
  - Au wire on the Au pads (Wirebond-Wedge or -Ball).
  - The v4 Au pads are 120 × 200 µm on the top/bottom edges, 200 × 200 µm for RF and C, and 200 × 150 µm for SNS/SNG. Au ground fill stays ≥ 30 µm from signal pads. The v3 recessed SNSPD and Al M1 bond openings do not apply to this v4 bond map; qualify the actual Au option and bonder on W7 [verify].
  - **Wedge-bond the SNSPD pads; no ball bonding there** (the ball bonder's flame-off spark is a risk to electrically sensitive devices: EPFL CMi HB10 guidelines) [inference for NbN].
  - **RF pad: 2–4 wires** in parallel (Sandia Phoenix/Peregrine bonds RF with 7 wires, arXiv:2009.02398 Sec. 5.3; `research/reports/Bond pad sizing for ion traps.md`).
  - **Probe at one end of each 200 µm pad and bond at the other** (step 17 probe marks can hide pad damage) [inference].
  - Plated Au must be wire-bond grade (soft, ≈ ≤ 90 Knoop, vendor figure) [verify with MIT.nano for the bath, or test-bond W5 coupons with and without an anneal].
  - **Bond the Au ground fill to carrier ground at GND-1…4, ≥ 2 of them (A4).** On v4 A30/B60, the local Al mirror is tied to this fill through its on-chip via; verify that link in [ground-link test a13](../tests/01_ELECTRICAL.md). NODET contains no Al. The v4 die has no separate M1 bond pads.
  - Bond off the top/bottom edges for the four pad rows, off the right edge for RF (4700, 0), and off the left edge for C and the SNSPD pads. Pads stay at \|x\| ≤ 3.5 mm on the top/bottom edges and near y = 0 on the side edges, away from the beam exits near the corners (\|x\| or \|y\| ≈ 4.7 mm). Keep the loops low anyway.
  - Bond the SNSPD pads last, wearing a strap. Short the carrier SNSPD pins until installation [inference].
- **Bond map** (from [trap_die_v4_A30_pads.csv](../../gds/trap_die_v4_A30_pads.csv), identical positions and electrode numbers for B60; [NODET CSV](../../gds/trap_die_v4_NODET_pads.csv) omits SNS/SNG). Rows run along y = +4720 (T) and y = −4720 (B) at **360 µm pitch**: TL1 … TL8 at x = −3500 … −980, TR1 … TR9 at x = +3500 … +620 (same x for BL / BR). The [centre-to-centre fan-out table](../../sim/out/16_pad_pitch_check/fanout.csv) and [diagram](../../sim/out/16_pad_pitch_check/fanout.png) use nominal pad/finger centres and local finger IDs; fill in actual carrier pins after choosing the package. The table represents one connection per chip pad; extra RF wires remain part of the final bond plan.

| Chip pad | Electrode | Role | Layer | Wire | Carrier pin |
|---|---|---|---|---|---|
| TL1 | 33 | top cap left | 50 | Au | |
| TL2–TL8 | 3 → 9 | top segments, −1080 … −360 µm from readout | 50 | Au | |
| TR1 | 34 | top cap right | 50 | Au | |
| TR2–TR9 | 17 → 10 | top segments, +600 … −240 µm from readout | 50 | Au | |
| BL1 | 35 | bottom cap left | 50 | Au | |
| BL2–BL8 | 18 → 24 | bottom segments, −1080 … −360 µm from readout | 50 | Au | |
| BR1 | 36 | bottom cap right | 50 | Au | |
| BR2–BR9 | 32 → 25 | bottom segments, +600 … −240 µm from readout | 50 | Au | |
| C | 2 | centre DC, (−4650, +450) | 50 | Au | |
| SNS | SNSPD_S | SNSPD signal, (−4750, +100) | 50 | Au | |
| SNG | SNSPD_G | SNSPD return, (−4750, −100) | 50 | Au | |
| RF | 1 | RF, (4700, 0) | 50 | Au | |
| GND-1…4 | Au ground fill | (±4700, ±1500); ≥ 2 bonds | 50 | Au | |

- **After packaging:** repeat the pad-to-pad isolation through the carrier pins, plus meander R₅.
- [ ] Done — date: ____ operator: ____ carrier: ____ notes: ____

Continue: [next stage](../test_plan.md).
