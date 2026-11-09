> **Claude-authored.** Run sheet for run 1a, `gds/run_R1_TRAP.gds`. Rewritten for v4 2026-11-09. The team chose the trap-only process first on 2026-11-02 ([decisions](../../notes/decisions.md)).
> - This sheet lists only the steps this run uses. Each heading keeps its traveler number in square brackets, `[trav N]`. The branch steps E1.x and E2.x have no traveler number.
> - Full recipes: [foundation](process/01_FOUNDATION.md), [Au electrodes](process/03_ELECTRODES.md) (E2 steps 12–15 only), [packaging](process/04_PACKAGING.md).
> - **[verify]** marks values not yet checked on the MIT.nano tool, or not given by any source.

# Run sheet: R1_TRAP (plain five-wire trap, no detector, v4)

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md) · [Local mirror (v4 basis)](variants/LOCAL_MIRROR.md) · [Qualification](QUALIFICATION.md)

> [!important] Before the device wafer
> Choose the electrode branch (E1 or E2, in section 3). Qualify the branch used, and run W7 bond-and-leak for both. Confirm facility access. Clear the [open items](#6-open-before-the-run) first.

Wafer ID: ________ Start date: ________ Operator: ________ Electrode branch used (E1 / E2): ________ GDS generated (date / `make_run.py` version): ________

## 1. What this run is

- **Goal:** qualify the v4 electrode process on the no-Al stack, dice and package it, and trap ions on a die with no detector. The NODET die becomes the reference for the SNSPD dies in run 1b ([staged-run rationale](../SIMPLIFICATIONS.md#s2-staged-runs-a-plain-trap-run-first-snspd-later)).
- **Stack, bottom to top** (team decision 2026-11-08, [decisions](../../notes/decisions.md)):
  - high-resistivity float-zone Si, ρ > 20 kΩ·cm;
  - thermal SiO₂ 1.0 µm, both sides;
  - Au electrodes directly on the SiO₂, by branch E1 (Ti 10 nm / Au 350 nm, lift-off) or E2 (Ti/Au seed, 6 µm plated Au).
- **Not in this run:** Al (no M1, no local mirror), the 10 µm D2, the SiO₂ spacer and cap, NbN, e-beam lithography, any ground plane, and layers 10, 20, 22, 24, 30, 31, 40 and 45.
- **Wafer:** one 100 mm wafer. Only an 8-die block at the centre (20.2 × 33.1 mm) is written. Dies ([run_R1_TRAP_map.csv](../gds/run_R1_TRAP_map.csv), die-centre coordinates in µm):

| Die | Type | Centre (x, y) |
|---|---|---|
| R1_TRAP-01, -03, -04, -05, -07, -08 | NODET trap die (`trap_die_v4_NODET`, 10 × 10 mm; layers 1 and 50 only) | (−5100 / +5100, −11550 / 1350 / 11550) |
| R1_TRAP-02, -06 | TEST_TRAP die (10 × 2.5 mm; T1 Au comb and T6 Au loop) | (±5100, −5100) |

The TEST_TRAP die is generated from the v4 file `test_die_v4_TRAP` (drawn and checked 2026-11-09; see [open item 3](#6-open-before-the-run)).

### Changed from v3

- **Stack:** thermal SiO₂ 1.0 µm, then Au directly on it. Removed: the 150 nm Al-1%Cu ground plane, the 10 µm D2 and the spacer and cap.
- **Substrate:** ρ > 20 kΩ·cm (was > 10⁴ Ω·cm).
- **Removed steps:** 3 (M1 Al), 9 (D2), 11 (L40 openings), 16a (L45 protect) and 16 (D2 gap etch). Steps 4–8 and 10 stay retired.
- **Removed rules and items:** the ≤ 300 °C limit after the Al step (no Al), the fill-to-M1 ground vias, the M1 bond openings and the mark cut-outs (no M1). The PECVD SiO₂ question is open ([open item 2](#6-open-before-the-run)).
- **Electrodes:** branch E1 added (lift-off, Ti 10 nm / Au 350 nm). Branch E2 kept (seed, mold, plating, seed removal), without D2.
- **Dies:** NODET from `trap_die_v4_NODET` (layers 1 and 50 only). The pad map has 36 signal pads at 360 µm pitch (pending adoption) and no SNS/SNG pads.
- **Electrical tests:** a4 (T2 capacitor) and a13 (ground link) do not apply. a1 and a2 lose their M1 pads.
- **Qualification:** the D2 stress loop, the gap-etch loop and W3 are removed. W5 applies to E2 only. W7 applies to both.

### Lithography jobs (MLA150, `run_R1_TRAP.gds`, layers 1 and 50 only)

| Order | Step | Layer | Expose | Resist | Written area | Align to |
|---|---|---|---|---|---|---|
| 1 | 1 | L1 MARK | drawn | positive ~1.3 µm | 0.025 mm² | wafer flat |
| 2a | E1.1 | L50 AU, branch E1 | drawn | LOR + positive resist [verify thicknesses] | 5.917 cm² of Au | L1 marks [verify overlay] |
| 2b | E2.2 | L50 AU, branch E2 | **inverted** | AZ nLOF 2070 ≥ 8 µm | the complement of 5.917 cm² of Au [verify the inverted area with the MLA] | L1 marks [verify overlay] |

Jobs 2a and 2b are alternatives. Use only the one for the branch chosen. Export each layer alone. Exclude layers 100 (notes) and 101 (outlines). Enter the mark coordinates as die coordinates plus the die centres above ([mask list](mask_list.md), section 4).

## 2. Before the run (short loops on dummy wafers)

Complete these [qualification loops](QUALIFICATION.md) for R1_TRAP:

| Loop | What | Applies to | Why |
|---|---|---|---|
| **W5 plating** | Seed + the real L50 job from `run_R1_TRAP.gds` on a bare-SiO₂ dummy, plated to 6 µm | Branch E2 only | Current for the plated area, thickness map and gap profile [verify plated area, open item 6] |
| **W7 bond-and-leak** | Planned bonds on the Au pads of a dummy die (plated for E2, evaporated for E1) | Both branches | Au-to-ground leakage before and after bonding; pull and shear; tool fit [verify]. The W3 T2 capacitor is retired in v4 ([open item 4](#6-open-before-the-run)) |
| **E1 lift-off test** | 0.35 µm Au lift-off over 5 µm gaps, then wedge bonding on the evaporated Au | Branch E1 only | Lift-off and bondability ([open decisions](OPEN_DECISIONS.md#before-any-v4-run), "If E1") |

Removed for v4: the D2 stress loop, the gap-etch rate loop and W3 (no D2, no gap etch). Dummy wafers: ≥ 2, as in the v3 sheet [verify count for the v4 loops].

Facility questions to settle first ([full list](QUALIFICATION.md#facility-confirmations)):

- which tools accept wafers with Au on them (the probe station and the dicing saw come after the electrodes);
- branch E2 only: whether a gold plating tank exists, its chemistry and its minimum plated area;
- branch E1 only: which evaporator accepts Au and Ti, and its lift-off compatibility [verify];
- the order of tool trainings.

NbN questions can wait for run 1b.

## 3. Steps

### Common part

#### 0. Wafer prep and clean [trav 0]

[Full recipe](process/01_FOUNDATION.md#0-wafer-prep-and-clean)

- **Tool:** Acid-Etch-General-* hood.
- **Recipe:**
  - Start with high-resistivity float-zone Si, **ρ > 20 kΩ·cm** (v4 decision; replaces the traveler's > 10⁴ Ω·cm) [verify on the spec sheet].
  - Scribe the wafer ID on the backside edge.
  - Piranha 15 min, DI rinse, spin dry. RCA if the furnace rules require it [verify].
  - Set aside ≥ 2 dummy Si wafers for the short loops [verify count].
- **Inspect:** particles under darkfield microscopy.
- [ ] Done — date: ____ operator: ____ ρ (spec sheet): ____ notes: ____

#### 1. L1 marks, Si RIE ~1 µm [trav 1]

[Full recipe](process/01_FOUNDATION.md#1-l1-alignment-marks-si-rie-1-µm)

- **Tool:** DirectWrite-MLA150 and RIE-F-Samco-230iP (SF₆/O₂ or a Si recipe [verify recipe name]).
- **Recipe:**
  - HMDS; positive resist ~1.3 µm (S1813-class [verify stocked resist]).
  - MLA expose L1 **drawn**. Develop (TMAH developer is fine here). Etch Si ~1 µm.
  - Strip in solvent, then O₂ ash.
- **Marks:** four crosses per die. NODET dies at (±4300, ±4830). Test dies at (−1700, ±1080) and (4300, ±1080), unchanged in v4.
- **Inspect:** crosses sharp; depth by Dektak, target 1.0 ± 0.2 µm.
- [ ] Done — date: ____ operator: ____ depth: ____ notes: ____

#### 2. Thermal SiO₂ D1, 1.0 µm, both sides [trav 2]

[Full recipe](process/01_FOUNDATION.md#2-thermal-sio₂-d1-1-µm-both-sides)

- **Tool:** Ox-Tube-Lindberg or Tube-OxAnneal-Expertech-CTR200.
- **Recipe:** wet oxidation to 1.0 µm [verify time and temperature on the tool chart]. This SiO₂ is the electrode substrate.
- **Target:** 1.00 ± 0.05 µm by ellipsometry at 5 points.
- **Inspect:** marks still visible as topography.
- [ ] Done — date: ____ operator: ____ t SiO₂ (5 pts): ____ notes: ____

**Continue with one branch only: E1 or E2 (section 3, below). Both branches have equal standing in this sheet; the choice is open ([open item 1](#6-open-before-the-run)).**

### Branch E1: lift-off Au, 0.35 µm (steps E1.1–E1.3)

#### E1.1 L50 lift-off resist and expose [new]

- **Tool:** DirectWrite-MLA150.
- **Recipe:**
  - LOR, then positive resist. Names and thicknesses [verify].
  - MLA expose L50 **drawn** (Au stays where the electrodes, pads and ground fill are) [H.2, steps 12v–15v]. Align to the L1 marks [verify overlay].
  - Develop per datasheet [verify].
- **Inspect:** the 5 µm gaps are open down to the SiO₂; undercut profile [verify].
- [ ] Done — date: ____ operator: ____ LOR and resist: ____ overlay: ____ notes: ____

#### E1.2 Evaporate Ti 10 nm / Au 350 nm [new]

- **Tool:** evaporator [verify; no evaporator is named in the sources].
- **Recipe:**
  - Ti 10 nm, then Au 350 nm [verify thicknesses; 350 nm as in Hampel 2023].
  - In-situ Ar pre-clean before the Ti: H.2 gives it for the AlF₃ on the via floor, which R1_TRAP does not have. Keep or drop ([open item 5](#6-open-before-the-run)).
- **Inspect:** Ti and Au thickness on a witness [verify].
- [ ] Done — date: ____ operator: ____ Ti: ____ Au: ____ notes: ____

#### E1.3 Lift-off in NMP [new]

- **Tool:** NMP lift-off [verify bench and time].
- **Recipe:** lift off in NMP [H.2, step 12v–15v; verify time and temperature].
- **Inspect:**
  - every electrode and pad separated; no Au across a 5 µm gap;
  - each electrode isolated: > 100 MΩ to its neighbours at 10 V, probing the pad rows (the E2.4 check, carried over) [verify for E1].
- [ ] Done — date: ____ operator: ____ isolation: ____ notes: ____

### Branch E2: plated Au, 6 µm (steps E2.1–E2.4)

#### E2.1 Plating seed Ti 15 nm / Au 50 nm (PTB) [trav 12]

[Full recipe](process/03_ELECTRODES.md#12-e2-plating-seed-ti-15-nm--au-50-nm-ptb)

- **Tool:** Sputter-AJA-* (sputter for step coverage; PTB evaporated).
- **Recipe:** Ti 15 nm, then Au 50 nm, as in the traveler. The in-situ Ar pre-clean was for the Al at the via floors; R1_TRAP has no Al ([open item 5](#6-open-before-the-run)).
- **Note:** the seed shorts every electrode and the pads together, so no electrical check is possible until E2.4.
- **Inspect:** Ti and Au thickness [verify].
- [ ] Done — date: ____ operator: ____ Ti / Au: ____ notes: ____

#### E2.2 L50 plating mold, nLOF ≥ 8 µm, inverted [trav 13]

[Full recipe](process/03_ELECTRODES.md#13-e2-layer-50-plating-mold-negative--8-µm)

- **Tool:** MLA150.
- **Recipe:**
  - AZ nLOF 2070 at ≥ 8 µm (PTB thesis; spin curve [verify]). The mold is ≥ 1.3 × the plating thickness [inference], so 8 µm covers the 6 µm plating.
  - MLA expose L50 **inverted** (resist stays where there is no Au). Align to the L1 marks [verify overlay; the traveler's ±1 µm was to L40 crosses, which this die does not have].
  - PEB and develop per datasheet. Short O₂ descum.
  - Leave the cathode contact points at the wafer edge free of resist.
- **Inspect:** 5 µm gap lines clean down to the seed. Record the gap width at the bottom (re-entrant profile).
- [ ] Done — date: ____ operator: ____ t_resist: ____ overlay: ____ gap bottom: ____ notes: ____

#### E2.3 Au electroplating, 6 µm [trav 14]

[Full recipe](process/03_ELECTRODES.md#14-e2-au-electroplating-6-µm)

- **Tool:** Plating-U04. Whether it is a gold tank, and its chemistry, are not verified [verify]. PTB used a sulfite bath (Enthone Microfab Au 100-B, pH 7.5, compatible with nLOF).
- **Recipe:**
  - Plated area: **5.917 cm²** for this run (0.915 cm² per NODET die, 0.214 cm² per TEST_TRAP die), measured from the v4 run GDS ([measured table](../gds/measured_v4.md)).
  - Current density per bath datasheet [verify]. Calibrate the current on W5 first. The minimum area of the bath is [verify].
  - At 3 mA/cm² and 100 % efficiency, Au(I) deposits ~0.19 µm/min, so ~32 min for 6 µm [team calc, Faraday].
  - Plate in two halves and measure in between.
- **Target:** 6.0 ± 0.5 µm (DESIGN_LOG step 2); ≤ 10 % across the wafer [verify]; no nodules.
- **Inspect:** thickness map; nodules.
- [ ] Done — date: ____ operator: ____ I / t: ____ thickness: ____ notes: ____

#### E2.4 Strip, descum, seed removal [trav 15]

[Full recipe](process/03_ELECTRODES.md#15-e2-strip-descum-seed-removal)

- **Tool:** NMP / Remover PG for the strip. Ar ion etch: Clean-Ar-Plasma or an Ar RIE recipe [verify that it mills]. F-plasma etch [verify tool].
- **Recipe:**
  1. Strip nLOF in hot NMP / Remover PG. Then O₂ plasma and F plasma for resist debris (PTB).
  2. Ar ion etch of the Au seed at ~50 nm/min (PTB): ~1 min + ~20 % over.
  3. F-plasma etch of the Ti at ~10 nm/min (PTB): ~1.5 min + over.
- **Note:** line-of-sight redeposition is unavoidable (Sussex).
- **Inspect:**
  - every electrode isolated: > 100 MΩ to its neighbours at 10 V, probing the pad rows;
  - Au roughness by AFM (PTB 8.3(5) nm rms; W5 target ~8 nm rms).
- [ ] Done — date: ____ operator: ____ Ar time: ____ F time: ____ isolation: ____ AFM: ____ notes: ____

### Common end (both branches)

#### 17. Room-temperature wafer-level electrical test [trav 17]

[Electrical protocol](tests/01_ELECTRICAL.md)

- **Tool:** ProbeStation-Summit-11000 with SMUs. Manual probing [verify].
- **Recipe:** apply these tests only:
  - **a2 DC leakage:** 50 V, ≤ 100 nA, and > 100 MΩ between every pair, including the Au ground fill [verify; the protocol says "ground plane"];
  - **a1 RF leakage:** 300 V, ≤ 100 nA, run twice (RF to the ground fill, to C, to caps 33–36 and to segments 17 and 32);
  - **a3 T6 continuity** on TEST_TRAP: 1 mA, 0–100 mV;
  - **a5 T1 comb leakage:** 50 V, ≤ 100 nA. 300 V only on sacrificial dies.
  - Order per die: a2, then a1 (low-voltage tests first).
  - Not applicable: a4, a6–a8, a12 and a13 (no Al, no M1). a10 applies after packaging only.
  - The "Dietl 2025" source of the limits is identified ([L2 note](../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md)); the limits remain [verify].
- **Record:** pass/fail per die ID from [run_R1_TRAP_map.csv](../gds/run_R1_TRAP_map.csv). Dies that fail go to destructive tests (T1 flashover, cross-sections).
- [ ] Done — date: ____ operator: ____ yield: ____ notes: ____

#### 18. Protect, dice (10 × 10 mm trap dies, 10 × 2.5 mm test dies), strip [trav 18]

[Full recipe](process/04_PACKAGING.md#18-protect-dice-10--10-mm-trap-dies-10--25-mm-test-dies-strip)

- **Tool:** Diesaw-DAD3240 with a Si blade [verify blade and recipe with staff].
- **Recipe:**
  - Protective resist: E2 ≥ 8 µm, covering the 6 µm Au [trav 18]. E1 [verify thickness for the 0.35 µm Au].
  - Cuts: 3 x-cuts at x = −10 200, 0 and +10 200 µm (± street). 5 y-cuts at y = −16 550, −6 450, −3 750, +6 450 and +16 550 µm; the outer two are the block edges, and the others sit between stacked dies [team calc from the run map].
  - Remove the tape in acetone; then acetone and IPA strip. No ultrasonic [inference].
- **Inspect:** chipping < 50 µm [verify].
- [ ] Done — date: ____ operator: ____ chipping: ____ notes: ____

#### 19. Package [trav 19]

[Full recipe](process/04_PACKAGING.md#19-package)

- **Tool:** cryo-compatible epoxy for die attach; wire bonder, Wirebond-Wedge or Wirebond-Ball [verify which].
- **Carrier:** open. PGA84L-like, 100-pin CPGA or the lab carrier [open item 8]. The package spacer is an open proposal [verify].
- **Die attach:** cryo-compatible epoxy, cured ≤ 150 °C [verify product and cure], for example EPO-TEK 353ND as listed by JoVE. Au/Sn would need a metallised back side. This die's back side is SiO₂.
- **Bond map:** [trap_die_v4_NODET_pads.csv](../gds/trap_die_v4_NODET_pads.csv). There are 36 signal pads (RF, C, TL1–8, TR1–9, BL1–8, BR1–9) on the Au electrodes, and GND-1…4 on the Au fill. The pitch is 360 µm (generated; team adoption pending). Top and bottom pad rows are at y = ±4720 µm, RF at (4700, 0) and C at (−4650, 450).
- **Wire:**
  - Au wire on the Au pads. Pads are 120 × 200 µm on the top and bottom edges, and 200 × 200 µm for RF and C.
  - Keep the Au ground fill ≥ 30 µm from the signal pads.
  - RF pad: 2–4 wires in parallel (Sandia, arXiv:2009.02398 Sec. 5.3).
  - Probe at one end of each pad and bond at the other [inference].
  - Plated Au (E2) must be wire-bond grade [verify; W5]. For E1, check that the 350 nm evaporated Au wedge-bonds [verify].
- **Ground:** bond ≥ 2 of GND-1…4 to carrier ground. There is no Al on this die, so there is no M1 backup bond.
- **Bond off** the top and bottom edges for the pad rows, the right edge for RF and the left edge for C.
- **After packaging:** a10 RF capacitance [verify carrier]; pad-to-pad isolation through the carrier pins.
- **Inspect:** bond pull and shear, per W7 [verify].
- [ ] Done — date: ____ die used: ____ carrier: ____ notes: ____

## 4. First trapping on a NODET die: expected values

From DESIGN_LOG step 25 (v4 NODET, `12_final_chip_check.py`, planar model, 53 V at 28 MHz, 0.8 MHz axial, 10° tilt in the zones) and step 2:

- **Drive:** 53 V at 28 MHz gives RF-only radial 3.00 MHz and q = 0.30 on every v4 die. Depth ≈ 52 meV from step 2, with no v4 value recorded [verify].
- **Loading zone** (GDS x = −240): ion height 49.97 µm; max |V| 9.10 V; axial 0.8 MHz target.
- **Readout zone** (GDS x = +240): ion height 49.98 µm; max |V| 9.10 V. There is no window on this die, so no recess correction.
- **Transport between zones:** max |V| 7.34 V; max step 1.59 V per 10 µm.
- **Radial frequencies and tilt at each zone:** not recorded for v4 NODET [verify]. The v3 values (2.89 / 2.97 MHz) do not apply.
- **Measurements that become the run-1b reference:**
  - secular frequencies against these numbers;
  - micromotion compensation at both zones and its drift;
  - heating rate at both zones;
  - transport.

## 5. What carries over to run 1b

Record these as the starting calibration for run 1b:

- the electrode branch used and its calibration: lift-off times (E1), or plating current and seed-removal times (E2);
- the thermal SiO₂ thickness result and the Si spec-sheet resistivity;
- the wire-bond and pull results from W7, and the bond map;
- the dicing settings;
- the leakage numbers (a1, a2, a5) and the RF capacitance (a10);
- the RF resonator Q with a die mounted, if measured [open item 9].

Run 1b adds the NbN steps, the spacer and cap, and the e-beam (current T8 dose and T9 geometry arrays). The A30 and B60 cap and spacer etch (about 0.40 µm: 238 nm spacer plus 160 nm cap) still needs its calibration before run 1b ([open decisions](OPEN_DECISIONS.md#before-r1_full)). Complete [detector reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts) before export.

## 6. Open before the run

- [ ] **1. Electrode Au, E1 or E2.** Open; it blocks the traveler rewrite. Both branches stay in this sheet until the team chooses ([open decisions](OPEN_DECISIONS.md)).
- [ ] **2. 398 nm PECVD SiO₂.** Whether R1_TRAP also deposits 398 nm of PECVD SiO₂ on the 1.0 µm thermal SiO₂, so that the electrode substrate matches the detector dies (1.0 µm thermal, 238 nm spacer and 160 nm cap, about 1.4 µm of SiO₂). The sources do not decide this. [verify with the team]
- [x] **3. TEST_TRAP for v4.** Done 2026-11-09: `make_run.py` writes `test_die_v4_TRAP` (T1 and T6 only, on layers 1 and 50), checked by `gds/check_test_die.py`; `run_R1_TRAP.gds` regenerated.
- [ ] **4. Substitute for the T2 capacitor.** T2 (a4, and the W7 bonding structure) is retired in v4. Its replacement T2v (Au / SiO₂ / Al capacitor) is on `test_die_v4` only, not on TEST_TRAP [verify the a4 and W7 use].
- [ ] **5. Ar pre-clean before the Au electrodes.** The traveler's reason (AlF₃ on the Al at via floors) does not apply without Al. Keep or drop the in-situ Ar pre-clean before the E1 Ti or the E2 seed. [verify with the team]
- [x] **6. Plated area (E2 only).** Done 2026-11-09: 5.917 cm² for `run_R1_TRAP`, measured from the v4 run GDS by `gds/measure_dies.py` ([measured table](../gds/measured_v4.md)). The older 5.93 and 1.65 cm² figures were for v3 layouts.
- [ ] **7. Pad pitch 360 µm.** Team adoption pending ([open decisions](OPEN_DECISIONS.md#design-choices)).
- [ ] **8. Carrier and package spacer.** Open: PGA84L-like, 100-pin CPGA or the lab carrier. The spacer is an open proposal ([open decisions](OPEN_DECISIONS.md#design-choices)).
- [ ] **9. Si and RF resonator.** Order Si with ρ > 20 kΩ·cm; measure the RF resonator Q with a die mounted ([open decisions](OPEN_DECISIONS.md#before-any-v4-run)).
- [ ] **10. Facility.** Au-compatible tools, the gold plating tank (E2), an evaporator with Au and Ti (E1), holders, training order and booking ([facility confirmations](QUALIFICATION.md#facility-confirmations)).
- [ ] **11. E1 details.** Names and thicknesses of the LOR and positive resist; protective resist thickness for dicing 0.35 µm Au; and the L50-to-L1 overlay tolerance (no L40 crosses on this die). [verify]
- [ ] **12. Dummy wafers and dicing.** The count of dummy wafers for the v4 loops [verify]. The team list does not include the dicing rehearsal, so decide whether any W3 item stays ([open decisions](OPEN_DECISIONS.md#before-r1_trap)).
- [ ] **13. Dietl 2025 limits.** The source of the a1, a2 and a5 limits is identified ([L2 note](../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md)); the limits remain [verify] ([source check](OPEN_DECISIONS.md#source-and-model-checks)).
