> **Claude-authored.** In-line measurements and acceptance windows for the v4 steps ([process pages](process/01_FOUNDATION.md), [R1_TRAP sheet](RUNSHEET_R1_TRAP.md)). Targets come from DESIGN_LOG steps 2, 9, 9b, 9c, 10, 17, 22 and 25–29 and the research report. Windows marked **[verify]** are first guesses to tighten after the witness wafers ([qualification](QUALIFICATION.md)). Rewritten for v4 2026-11-09; mirror 100 nm 2026-11-09; final stack and R1_ONE 2026-11-12.

# Process checks

[Fab overview](README.md) · [Qualification](QUALIFICATION.md) · [Test plan](test_plan.md)

> [!important] Use the correct run, detector and electrode branch
> - **R1_ONE** (the one-wafer run, 2026-11-12): every die does steps 0–3 (step 3 is the raised Al mirror and marks), and the blanket steps 4, 5 and 8. The patterned steps (6, 7, 11) are done only on the dies that draw them: A30, B60 and SNSPD-only. The NODET (trap-only) die gets the blanket NbN etched off in step 7 [verify], and no layer 40. Then one electrode branch (E1 or E2, still open), then steps 17–19.
> - **A30, B60 and SNSPD-only dies:** all steps.
> - **NODET dies:** steps 0–3 (corner marks only), 4, 5, 8, the NbN clearance check after step 7, 12–15, 17–19.
> - Rows marked **E1** or **E2** apply to that branch only. Unmarked rows apply to both.
> - Full-stack thicknesses include the spacer and cap. Earlier v3 resistance and absorption estimates need [reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts).
> - The test structures on R1_ONE are T3 and T11 on the SNSPD-only die, and the eight detector cells. T1, T2v, T4, T4b, T6, T8, T9, T10 and T12 are not on R1_ONE; the rows that named them point to where the measurement is made on this run, or to "not in R1_ONE".
> - **R₀ on trap dies cannot be read before the electrodes:** the SNSPD pads are electrode Au and the contacts are covered by the cap. The early resistance readings come from T3 at step 11 on the SNSPD-only die, and from the finished cells.

## 1. Substrate, marks and base SiO₂ (steps 0–2)

| Step | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|
| 0 | Substrate resistivity | Spec sheet | ρ > 20 kΩ·cm | > 20 kΩ·cm [verify spec sheet] | Do not start the run [inference] |
| 0 | Particles on the start wafer | Darkfield microscope | none seen | [verify] | Re-clean |
| 0 | Dummy Si wafers for the witness loops | Count | ≥ 3 ([foundation](process/01_FOUNDATION.md)) or ≥ 2 ([R1_TRAP sheet](RUNSHEET_R1_TRAP.md)) | [verify count] | – |
| 1 | Si marks | – | *removed 2026-11-12* (marks are Al, step 3) | – | – |
| 2 | Base SiO₂ (front and back, or the route used) | Ellipsometry, 5 points; or as supplied | 1.0 µm nominal | 0.5–2.0 µm accepted as supplied (sim 22b) | Record the thickness; re-run [sim 22b](STACK.md#base-sio₂-thickness-sim-22b) with it |

## 2. Al mirror and marks (step 3; A30, B60, SNSPD-only; NODET corner marks)

Thermal limit for this step and every later step: **≤ 300 °C**.

| Step | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|
| 3 | Al thickness (one evaporation) | Crystal monitor; witness by profilometer | 100 nm | 90–110 nm [design call; verify] | Re-evaporate or hold; reconcile with the sim |
| 3 | Lift-off complete | Optical | No Al flags or residue | No Al flags or residue [verify] | Re-do the lift-off [verify] |
| 3 | Mark crosses (layer 1, Al) | Optical or SEM | Sharp, sized as drawn | [verify] | Re-expose |
| 3 | Al sheet resistance | 4-pt on a co-loaded witness | 0.30–0.40 Ω/sq expected [team calc] | [verify] | Reconcile before accepting |
| 3 | Hillocks and whiskers on Al | Darkfield microscope | none | no features > 100 nm [verify] | Lower the deposition T, or a Ti cap on the Al in a later run (SINTEF; a proposed mitigation, not a team decision) |
| 3 | Mirror shape | Drawing vs as-built | \|y\| ≤ 20 µm, x = −2240 … +268 µm (A30); branch to the ground via at (−2140, 130) µm | Matches the drawing | Re-expose |
| 3 | Mirror strip resistance | Not measured on R1_ONE (no T10 on this run) | 18.8–25.1 Ω calculated at 100 nm (2.51 mm × 40 µm, 62.75 squares) (`sim/10c`, [DESIGN_LOG step 37](../DESIGN_LOG.md)) | [verify]: acceptance not set | – |

## 3. Detector stack (steps 4–8; blanket on all dies, patterned where drawn)

| Step | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|
| 4 | PECVD SiO₂ spacer | Ellipsometry (Al substrate model) on the device wafer, plus co-loaded bare Si | 238 nm | 228–248 nm | Strip is not possible over Al. Re-run 09c with the measured value |
| 4 | Hillocks after the spacer | Darkfield; AFM on a dummy die area | none | no features > 100 nm [verify] | As step 3 |
| 4 | Spacer temperature | Tool log | ≤ 300 °C | ≤ 300 °C [verify the tool's settable T] | – |
| 5 | NbN thickness | Ellipsometry on the thermal-SiO₂ witness (Medeiros 2019 model) | 7.0 nm | 6.5–7.5 nm | Re-deposit on a new wafer |
| 5 | **NbN Rsq** | 4-pt on the thermal-SiO₂ witness | ≈ 400 Ω/sq at 7 nm [team calc, Medeiros fit; Toomey 2018] | ±15 % [verify] | – |
| 5 | **NbN Tc** | Dipstick / PPMS, on both witnesses (thermal SiO₂ and spacer over Al) [verify access] | 7.8–8 K (Dane 2017; Toomey 2018) | Over 7 K (decisions, 2026-11-02) | – |
| 5 | Time from NbN to step 6 | Log | within 24 h, otherwise store in an N₂ box | ≤ 24 h [inference from the Medeiros oxidation law] | Record the Nb₂O₅ growth |
| 6 | Ti / Au contact thickness | Witness [verify] | **Ti 5 nm / Au 50 nm** | [verify] | – |
| 6 | NbN develop and rinse | Log | shortest develop that clears the LOR, then ≥ 3 min running DI rinse, then IPA | Done as written (Toomey) | Do not proceed with a standing DI rinse |
| 6 | Contact pads | SEM or optical, drawn die | 27 × 7 µm pads in the slot; each contact covers the −x half of its NbN tab | Matches the drawing | Re-expose |
| 6 | Lift-off | Optical | no Au flags; each contact continuous from tab to pad | – | Re-do the lift-off [verify] |
| 6 | Lead resistance | [verify method and target] | record | [verify]. The v3 per-lead figure (~0.1–0.3 kΩ, long buried leads) does not apply | – |
| 7 | HSQ after develop (wires) | Ellipsometry or AFM step on the W2 witness | 50 nm | [verify]; sets the cap in step 8 | – |
| 7 | Line width | SEM on the SNSPD-only die cells (D1–D8) and the W2 witness | 130 nm wires / 70 nm spaces | Calibrate tolerance on W2 [verify]; no bridges or breaks | – |
| 7 | Dose test | W2 witness only; T8 is not on R1_ONE | width vs dose factor 0.80–1.20 | record width and breaks per element | The best element sets the next run's nominal dose ([mask list](mask_list.md), section 2) |
| 7 | Detector geometry controls | SEM on the cells of the SNSPD-only die | as drawn | [verify]; T9 is not on R1_ONE | – |
| 7 | **NbN cleared, open field (new)** | Two probes on an open field, after the CF₄ etch, on a NODET position and on a trap die | open circuit between the probes | open circuit [verify] | Extend the etch [verify]; the NbN is still there |
| 7 | R₀ on trap dies | – | not possible before the electrodes (SNSPD pads are electrode Au; contacts under the cap) | – | Early readings from T3 at step 11 and the finished cells |
| 7 | Meander R (cells, if reachable) | Probe at ≤ 1 V, ≤ 100 nA | expected N_sq × Rsq ([a7](tests/01_ELECTRICAL.md#a7-meander-r)) | R / R_expected 0.8–1.3 [verify] | Open: die rejected. Low R: unetched bridges |
| 8 | **Total SiO₂ over the wires (HSQ + cap)** | Ellipsometry on a co-loaded Si piece | 160 nm | 150–170 nm (160 ± 10 nm) | Record. Absorption: 0.66 at 160 nm, 0.44 at 80 nm; 146–172 nm within 0.02 of the best [team calc, sim 09c] |
| 8 | **Cap (PECVD, blanket)** | Ellipsometry on a co-loaded Si piece | 110 nm (= 160 − HSQ 50 nm) | 110 ± 10 nm [verify]; ≥ 30 nm over the wires [inference, sidewall coverage] | – |
| 8 | Electrical access | – | none possible until step 11 (contacts covered) | – | Use the W1 witness pieces [verify] |

## 4. Layer-40 openings (step 11; A30, B60, SNSPD-only)

| Step | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|
| 11 | Mirror via depth | Dektak at the via | 348 nm (cap 110 + spacer 238), through to the Al | Clean Al at the floor | Extend the etch in short steps [verify] |
| 11 | SNSPD contact depth | Dektak or SEM | 110 nm through the cap, to the layer-22 Au (50 nm) | Clean Au at every floor | Extend in short steps [verify]; watch for Au loss |
| 11 | Au loss in the over-etch | Co-loaded piece, SEM or profile | the contacts stand on 50 nm Au for about 0.66 min more at the v3 rate [team calc] | Au survives [verify] | Shorten the over-etch on W3 |
| 11 | Etch time | Log | one etch; about 1 min [verify] (348 nm ≈ 0.97 min at the v3 rate of ~360 nm/min [team calc]) | Set on W3 | – |
| 11 | Contact-opening placement | SEM, top view | 18 × 3 µm openings at x = 148 … 166 µm (B60: 131.5 … 149.5 µm), \|y\| = 3.5 … 6.5 µm | Each opening ≥ 1 µm inside its 27 × 7 µm pad | Re-align or reject |
| 11 | Layer-40 overlay to layer 22 | Overlay measurement | ≤ 1 µm (1 µm drawn margin) [team calc] | ≤ 1 µm | Re-align or reject |
| 11 | Mirror via enclosure | Drawing | ≥ 25 µm enclosed by the Au ground fill and the Al | Matches the drawing | – |
| 11 | SNSPD pads (tied together) ↔ Al at ≤ 1 V | Probe | > 1 GΩ (no short through the spacer) | > 1 GΩ [verify; threshold carried from v3] | Reject die or investigate pinhole [verify] |
| 11 | Mirror via contact, first access | T11 on the SNSPD-only die, probe station | Au-to-Al via chain closed [verify] | [verify] | – |
| 11 | First access: R₀ (baseline) | T3 on the SNSPD-only die, probe station; detector cells through their pads | record R₀ | Record. R₀ is the baseline for the cells | – |

## 5. Electrodes, E1 and E2 (steps 12–15)

Both branches draw the same layer 50. Run one branch.

### Branch E1: Ti/Au lift-off, 0.35 µm

| Step | Branch | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|---|
| 12 | E1 | Resist opening (LOR + positive resist) | Optical or SEM | 5 µm gaps and slot open | Thicknesses [verify] | Re-expose |
| 13 | E1 | In-situ Ar pre-clean before the Ti | Log | time and power [verify] | Needed or not on this die [verify] | – |
| 13 | E1 | Ti and Au thickness | Witness | Ti 10 nm / Au 350 nm | [verify] | – |
| 14 | E1 | Lift-off in NMP | Optical | no Au across the 5 µm gaps; no flags | – | Re-do [verify] |
| 15 | E1 | Electrode isolation | Probe pad rows, 10 V | > 100 MΩ between neighbours | [verify; carried from v3 step 15] | – |
| 15 | E1 | Au over the 348 nm via step | SEM cross-section ([E1 lift-off loop](QUALIFICATION.md#e1-lift-off-loop-e1-only)) | continuous | [verify] | – |
| 15 | E1 | Au across the 100 nm mirror-edge step | Optical or SEM | continuous; no open or thin spot | [verify; the conformal SiO₂ softens the step, inference] | – |
| 15 | E1 | Gap depth-to-width (5 µm gaps, 0.35 µm Au) | Calculated | 0.07 [team calc]. Record; not a verdict | – | – |
| 15 | E1 | Wire bond on evaporated Au | Pull test ([W7](QUALIFICATION.md#w7-bond-and-leak-step-19)) | [verify] | [verify] | – |

### Branch E2: plated Au, 6 µm

| Step | Branch | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|---|
| 12 | E2 | Plating seed Ti 15 nm / Au 50 nm | Witness [verify] | 15 nm / 50 nm | [verify] | – |
| 12 | E2 | In-situ RF Ar clean before the seed, on the mirror via floor | Log, then T11 resistance (W3) | time [verify] | Au-to-Al contact closed (T11 [verify]) | – |
| 12 | E2 | Seed continuity down the 348 nm via wall | SEM cross-section, W3 | continuous | [verify] | – |
| 13 | E2 | Mold thickness (AZ nLOF 2070) | Dektak | ≥ 8 µm | ≥ 8 µm (mold ≥ 1.3 × plating [inference]) | – |
| 13 | E2 | Mold overlay to layer 40 crosses | Overlay | ±1 µm, critical | [verify on v4 crosses] | Strip and redo |
| 13 | E2 | Gap lines clean down to the seed; gap width at the bottom | SEM or profile | recorded | clean | – |
| 14 | E2 | Plated Au thickness | Dektak, 5 die positions and the midpoint | 6.0 µm | 5.5–6.5 µm; ≤ 10 % across the wafer [verify] | Plate more (before strip only) |
| 14 | E2 | Current calibration | W5 | from W5 | [verify] | – |
| 14 | E2 | Nodules | Optical | none | – | – |
| 15 | E2 | Au seed removal | Ar etch, ~50 nm/min (PTB) | ~1 min + ~20 % over | Milling confirmed [verify Clean-Ar-Plasma or Ar RIE recipe] | – |
| 15 | E2 | Ti seed removal | F-plasma, ~10 nm/min (PTB) | ~1.5 min + over | [verify] | – |
| 15 | E2 | Au roughness | AFM, 25 × 25 µm | ~8 nm rms (PTB 8.3(5) nm) | [verify] | – |
| 15 | E2 | Au across the 100 nm mirror-edge step | Optical or SEM | continuous | [verify] | – |
| 15 | E2 | Gap depth-to-width (5 µm gaps, 6 µm Au) | Calculated | 1.2 [team calc]. Record | – | – |

### Both branches (step 15 inspection)

| Step | Branch | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|---|
| 15 | Both | All 5 µm gaps open | Optical or SEM | open everywhere | – | Re-do the lift-off or the seed removal |
| 15 | Both | SNSPD leads continuous in the slot | Optical or SEM | 5 µm lines, 5 µm gaps | continuous | – |
| 15 | Both | Mirror via covered by the Au ground fill | Optical or SEM | ≥ 25 µm enclosure | covered | – |
| 15 | Both | Electrode isolation | Probe pad rows, 10 V | > 100 MΩ between neighbours | [verify] | – |
| 15 | Both | Pad-to-pad leakage between neighbouring electrodes, finished trap die (new) | Probe, 10 V | no leakage above the isolation limit | [verify] | – |
| 15 | Both | Fill-to-mirror resistance | Probe fill; not measured on R1_ONE (no T10). The calculated strip is 18.8–25.1 Ω at 100 nm, plus contacts [team calc] | calculated value only | [verify]: the old < 10 Ω test is not carried over as drawn | – |
| 15 | Both | Window floor (SiO₂ cap) | Optical; ellipsometry | no Au film or residue; cap thickness recorded | no visible film [verify]; thickness [verify] | Extra F-plasma [verify]; record |
| 15 | Both | R₂ on the SNSPD-only die (cells, T3) | Probe at ≤ 1 V, ≤ 100 nA | R / R₀ and the [meander tracking](#meander-resistance-tracking) | ΔR/R₀ ≤ 10 % [verify] | – |

## 6. Test, dice and package (steps 17–19)

### Step 17: electrical test, before dicing

Limits and protocol: [test plan](test_plan.md). The Dietl 2025 source for the limits is identified (see the [L2 note](../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md)); all limits are draft **[verify]**.

| Test | Quantity | Target | Accept | Applies to |
|---|---|---|---|---|
| a2 | DC leakage | 50 V | ≤ 100 nA; > 100 MΩ between pairs, including the Au ground fill [verify] | All dies |
| a1 | RF leakage | 300 V DC, run twice | ≤ 100 nA | All dies |
| a5 | Au comb leakage | 50 V | T1 is not on R1_ONE. Use the electrode-to-electrode leakage of step 15 on the trap dies [verify] | Trap dies |
| a3 | T6 Au continuity loop | – | not on R1_ONE | – |
| T2v | Au / SiO₂ / Al capacitor | – | not on R1_ONE | – |
| T10 | Al mirror strip, four-point | 18.8–25.1 Ω at 100 nm (calculated) | not on R1_ONE; not measured | – |
| T11 | Au-to-Al via chain | [verify] | [verify] | SNSPD-only die, centre |
| T12 | Twin Au leads over Al | – | not on R1_ONE | – |
| T3 | NbN four-wire bar Rsq | 4-wire, on the SNSPD-only die | within ±10 % of the step-7 value [verify] | SNSPD-only die, probe station |
| Ground link | Fill to mirror, through the on-chip via | [verify]: the old < 10 Ω was for the v3 M1 vias | [verify]; measured by T11 (via) on the SNSPD-only die; the strip is not measured on R1_ONE | A30, B60, SNSPD-only |
| a10 | RF capacitance | – | [verify] | After packaging |

- Order per die: a2, then a1 (low-voltage tests first).
- Dies that fail go to destructive tests on a rejected die or on the second wafer [verify].
- Record pass or fail per die ID from the run map (`gds/run_R1_ONE_map.csv`).

### Step 18: protect and dice

| Step | Branch | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|---|
| 18 | E2 | Protective resist | Thickness | ≥ 8 µm (covers 6 µm Au) | ≥ 8 µm | – |
| 18 | E1 | Protective resist | Thickness | [verify] for 0.35 µm Au | [verify] | – |
| 18 | Both | Dicing street | Layout, `make_run.py` (R1_ONE) and `make_wafer.py` | 200 µm street; saw cuts at x and y = −15300, −5100, +5100, +15300 µm (10.2 mm pitch) | Kerf plus chipping fits [verify blade width] | – |
| 18 | Both | Chipping | Optical | – | < 50 µm [verify] | – |
| 18 | Both | Au and Al clearance from the dicing edge | Layout check (`check_chip.py`; [DESIGN_LOG step 8](../DESIGN_LOG.md)) | ≥ 90 µm | ≥ 90 µm | – |
| 18 | A30, B60, SNSPD-only | Meander R₄ | Probe at ≤ 1 V | [R tracking](#meander-resistance-tracking) | R / R_expected 0.8–1.3 [verify] | – |

### Step 19: package

| Step | Branch | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|---|
| 19 | Both | Die attach epoxy cure | Product datasheet | ≤ 150 °C [verify product and cure] | ≤ 150 °C | – |
| 19 | Both | Bond map | [trap_die_v4_A30_pads.csv](../gds/trap_die_v4_A30_pads.csv); [NODET CSV](../gds/trap_die_v4_NODET_pads.csv) | pads as drawn; pitch 360 µm (team adoption pending) | Every pad bonded as in the map | – |
| 19 | Both | Worst wire angle | Fan-out check, nominal PGA84L-like cavity (step 29) | 20.03° [team calc] | Carrier not fixed [open] | – |
| 19 | Both | Ground bonds | GND-1…4 to carrier ground | ≥ 2 bonded | ≥ 2 | – |
| 19 | Both | Ground fill to signal pads | Layout | ≥ 30 µm | ≥ 30 µm | – |
| 19 | Both | RF pad wires | Bond plan | 2–4 wires in parallel | 2–4 | – |
| 19 | Both | SNSPD pads | Bond method | wedge-bonded; no ball bond on the SNSPD pads [inference] | as stated | – |
| 19 | E2 | Plated Au bondability | Test bond on W5 coupons, with and without an anneal | wire-bond grade [verify] | [verify] | – |
| 19 | E1 | Wedge bond on evaporated 350 nm Au | W7 and E1 loop | bonds pass pull [verify] | [verify] | – |
| 19 | Both | Wire bond pull and shear | W7 | – | [verify] | – |
| 19 | Both | Pad-to-pad isolation through the carrier pins | Carrier | after packaging | [verify] | – |
| 19 | A30, B60, SNSPD-only | Meander R₅ | Carrier pins | – | R / R_expected [verify] | – |

Open, not a check: the SNSPD RF termination (common-mode RF of ≈ 44.5 µA per lead on E2, 28.4 µA on E1 (`sim/10c`, DESIGN_LOG step 37); [open decisions](OPEN_DECISIONS.md#design-choices)).

## 7. Records per die

Use the run-map die ID in every record. NODET dies have no detector entries.

### Meander resistance tracking

- **Expected R = N_sq × Rsq.** Use [electrical test a7](tests/01_ELECTRICAL.md#a7-meander-r) and the released GDS square counts. Earlier v3 estimates were ~18 / 36 MΩ at 400 Ω/sq.
- **Where:** detector cells on the SNSPD-only dies (through their pads, from step 11); A30 and B60 dies between pads SNS and SNG after step 15.
- **Measurement rules.** Probe at ≤ 1 V and ≤ 100 nA compliance. Touch down at 0 V and wear a grounded strap. ESD on the open meander is the main handling risk [inference].
- **Flag:** **> 10 % rise** from R₀ at any checkpoint. Todaro saw 12–30 % rises (mostly while the plating resist was applied and stripped), and the large rises correlated with low switching current or no superconductivity (Todaro Supp. "Trap fabrication").

| Checkpoint | After step | Note |
|---|---|---|
| R₀ | 11 | Baseline, first access (T3 and the cells). Not possible at step 7 on trap dies. R / R_expected: accept 0.8–1.3 [verify] |
| – | 8 | **No access** (contacts covered by the cap). No witness loop in v4 covers this step [verify] |
| R₁ | – | Not used on R1_ONE: the first access is the R₀ point at step 11 |
| – | 12–14 | Seed or electrode Au shorts everything; no check possible (E2 seed, E1 Au) |
| R₂ | 15 | After the electrodes and seed removal (the Todaro-sensitive step) |
| R₃ | – | Removed in v4 (no gap etch). Number kept so the logs line up |
| R₄ | 18 | After dicing |
| R₅ | 19 | Through the carrier pins, including the bond and lead R |

- **Log, per die:** die ID from `gds/run_R1_ONE_map.csv`, R₀, R₂, R₄, R₅, ΔR/R₀, and the variant (A30 / B60 / SNSPD-only cell D1–D8).
- **Use:** pick the dies with the smallest drift for packaging.

### Detector resistance history

| Die ID / structure | R₀ | R₁ (not used on R1_ONE) | R₂ | R₄ | R₅ | Max ΔR/R₀ |
|---|---|---|---|---|---|---|
| | | | | | | |

### Electrical disposition

| Die ID | Variant | Electrode branch | SNSPD pads ↔ Al (step 11) | Mirror ground link (T11) | Leakage pass [verify] | Package? |
|---|---|---|---|---|---|---|
| | | | | | | |
