> **Claude-authored.** In-line measurements and acceptance windows for [traveler](TRAVELER.md) (v3 dies: `trap_die_v3_A30/B60/NODET.gds` and the test die `test_die_v3.gds`, which carries the test structures T1–T4b, T6, T8 and current T9). v3 has no indium tin oxide (ITO). Targets come from DESIGN_LOG steps 2, 9, 9b, 10 and 17 and the research report. Windows marked **[verify]** are first guesses to tighten after the witness wafers ([qualification](QUALIFICATION.md)).

# Process checks

[Fab overview](README.md) · [Qualification](QUALIFICATION.md) · [Test plan](test_plan.md)

> [!important] Use the correct run and detector revision
> R1_TRAP omits steps 4–8 and detector checks; its L40 depth is ~10.0 µm and gap-etch depth ~9.25 µm. Full-stack depths below include spacer/cap. Earlier v3 resistance/absorption estimates need [reconciliation](OPEN_DECISIONS.md#detector-documents-and-generated-layouts). “Dietl 2025” is unresolved; its draft limits are **[verify]**.

## 1. Film thickness and wafer shape

| After step | Quantity | Method / where | Target | Accept | If out of window |
|---|---|---|---|---|---|
| 1 | Mark depth | Dektak, 4 marks | 1.0 µm | 0.8–1.2 µm | Re-etch, or accept if the marks are visible |
| 2 | Thermal SiO₂ | Ellipsometry, 5 points, front + back | 1.00 µm | ±5 % | – |
| 3 | Al-1%Cu | Dektak step on the etched edge; 4-pt Rsq on a co-deposited Si witness | 150 nm | 135–175 nm; Rsq record [verify ~0.2–0.3 Ω/sq] | < 100 nm: not opaque, so re-deposit |
| 3, 4, 9 | Hillocks / whiskers on Al | Darkfield microscope; AFM on the W1-a witness | none | no features > 100 nm on the spacer surface [verify] | Lower the PECVD T, or add a Ti cap on the Al in the next run (SINTEF) |
| 4 | Spacer | Ellipsometry (Al substrate model) + co-loaded Si | 238 nm | **228–248 nm**; never 140–160 nm (node) | Strip-and-redo is not possible over Al. With no ITO the absorption is flat in cap thickness (~0.40), so only the spacer phase matters; re-run 09b with the measured value |
| 5 | NbN | Ellipsometry on the thermal-SiO₂ witness (Medeiros 2019 model; agrees with XRR within 0.5 nm above ~4 nm) | 7.0 nm | 6.5–7.5 nm | Re-deposit on a new wafer |
| 7 | HSQ remaining after CF₄ | Ellipsometry / AFM step on the W2 witness | – | record it; it sets the cap thickness | – |
| 8 | Cap (PECVD part) | Co-loaded Si, ellipsometry | 80 nm − HSQ | ≥ 30 nm; HSQ + cap 70–90 nm | – |
| 9 | D2 front / back | Reflectometer or ellipsometer [tool name not verified]; record per increment | 10.0 µm front | 9.5–10.5 µm; non-uniformity ≤ 4 % [verify] | Add an increment |
| 9 | **Wafer bow** | Filmstress-Tencor-FLX2320, after every increment | 0 | \|bow\| ≤ 50 µm [verify against MLA / EBL chuck limits] | Next increment on the other side |
| 11 | L40 depth | Dektak in a large opening | 10.3–10.4 µm (to metal) | Metal visible at every floor | Extend the etch in 2 min steps |
| 13 | Mold thickness / overlay | Dektak; overlay verniers | ≥ 8 µm; ±1 µm | Overlay > 1 µm: strip and redo | – |
| 14 | **Plated Au** | Dektak on 5 die positions and at the mid-point check | 6.0 µm | 5.5–6.5 µm, ≤ 10 % across the wafer [verify] | Plate more (before strip only) |
| 15 | **Au roughness** | AFM, 25 × 25 µm, on an electrode top | – | ~8 nm rms (PTB 8.3(5) nm after Ar seed removal) | – |
| 16 | **Gap-etch depth** | Dektak / optical profilometer in the T1 comb gaps (test dies) and a wide ground gap | stop 0.75 µm above M1 (Sussex 750(250) nm) | remaining oxide over M1 0.5–1.0 µm | Etch more in 1 min steps; never into Al |

## 2. Superconducting film and nanowire

| After step | Quantity | Method | Expected | Accept |
|---|---|---|---|---|
| 5 | **NbN Rsq** | 4-pt on the thermal-SiO₂ witness | ≈ 400 Ω/sq at 7 nm (≈ 600 at 5 nm) [team calc from the Medeiros fit; Toomey 2018] | ±15 % [verify] |
| 5 | **NbN Tc** | Dipstick / PPMS on both witnesses (thermal SiO₂ and spacer-over-Al) [verify access] | 7.8–8 K (Dane 2017; Toomey 2018) | ≥ 7.5 K (Todaro: Tc ≳ 1.25 × T_surface, so T_surface ≲ 6 K) |
| 7, 11, 15 | T3 4-wire bar Rsq (test dies) | 4-wire on T3 pads: inner taps 80 µm apart, w = 10 µm, so ~8 squares (±12 % from the 10 µm tap width) | ≈ 3.2 kΩ at 400 Ω/sq [team calc] | Within ±10 % of the step-7 value |
| 7 | Line width | SEM on T4 / T4b | v3.1: 130 nm wires / 70 nm spaces | Calibrate tolerance on W2 [verify]; no bridges/breaks. T9 controls have separate widths |
| 7 | **Dose array** | SEM on T8 D1–D7 (test dies), before the cap; later 2-wire R at room temperature ([dose-array test a12](tests/01_ELECTRICAL.md)) | Width vs dose factor 0.80–1.20 | Record width and breaks per D-element. The best element sets the next run's nominal dose (`mask_list.md` section 2) |
| W1-b | NbN after thermal history (5 × 300 °C PECVD) | Rsq, Tc on witness | – | ΔTc ≤ 0.3 K, ΔRsq ≤ 10 % [verify] |

### Meander room-temperature resistance tracking

- **Expected R = N_sq × Rsq.** Use the current [electrical test a7](tests/01_ELECTRICAL.md#a7-meander-r) and the released GDS square counts. Earlier v3 estimates were ~18 / 36 MΩ at 400 Ω/sq.
- **Where:** trap dies between pads SNS and SNG; test dies on T4 (same meander as A30) and T4b (same as B60).
- **Measurement rules.** Probe at ≤ 1 V and ≤ 100 nA compliance. Touch down at 0 V and wear a grounded strap. ESD on the open meander is the main handling risk [inference].
- **Flag:** **> 10 % rise** from R₀ at any checkpoint. Todaro saw 12–30 % rises (mostly while the plating resist was applied and stripped), and the large rises correlated with low switching current or no superconductivity (Todaro Supp. "Trap fabrication").

| Checkpoint | After step | Note |
|---|---|---|
| R₀ | 7 | Baseline. Also R / R_expected: accept 0.8–1.3 [verify] |
| – | 8 – 9 | **No access** (pads under the cap/D2). Covered by witness W1-b |
| R₁ | 11 | First access through the L40 openings |
| – | 12 – 14 | Seed shorts everything |
| R₂ | 15 | After the plating resist and seed removal: the Todaro-sensitive step |
| R₃ | 16 | After the gap etch |
| R₄ | 18 | After dicing |
| R₅ | 19 | Through the carrier pins (include the bond/lead R) |

- **Log, per die:** die ID from `gds/run_<name>_map.csv`, R₀ … R₅, ΔR/R₀, and the variant (A30 / B60, or T4 / T4b on test dies).
- **Use:** pick the dies with the smallest drift for packaging.

## 3. Readout window (bare SiO₂ floor, v3)

| After step | Quantity | Method | Expected | Accept |
|---|---|---|---|---|
| 15 | Window floor | Optical / SEM | bare SiO₂, no Au or Ti film or residue | Any visible film: extra F-plasma [verify]; record it |
| 16 | Window floor after the gap etch | Optical / profilometer | unchanged (protected by the L45 patch) | Any etch into the window SiO₂ means the 16a patch failed: reject the die |

(The v2 ITO checks, T5 and T7, were removed with the ITO.)

## 4. Isolation, shorts and dielectric

| After step | Test | Accept |
|---|---|---|
| 11 | SNSPD pads (tied together) ↔ M1 at ≤ 1 V. Checks for a short through the spacer to the Al | > 1 GΩ [verify] |
| 15 | Every electrode pad ↔ its neighbours at 10 V (seed fully removed) | > 100 MΩ (Stick 2010) |
| 16, 17 | Full Dietl 2025 set ([electrical tests](tests/01_ELECTRICAL.md)) | DC 50 V ≤ 100 nA; RF 300 V DC ≤ 100 nA, run twice |
| 16 | T1 comb leakage (test dies) at 50 V: detects Au redeposition bridges from the gap etch (Sussex) | ≤ 100 nA; ideally < 1 nA [verify] |
| 16 | T2 Au/D2/M1 capacitor (test dies; Au plate ↔ its M1 pad) | C ≈ 2.1 pF (ε_r 3.9, 0.8 × 0.8 mm = 0.64 mm², 10.3 µm) [team calc]; leakage at 50 V ≤ 100 nA |
| 16 | **Gap clearing** | SEM top view on 3 dies (plus a cross-section on W3 / sacrificial die): gaps open to the target depth, no sidewall films bridging Au to the floor, no Au stringers |
| 17 | Au ground fill (GND-n) ↔ M1 (M1-n opening): continuity through the eight fill-to-M1 vias (DESIGN_LOG step 22; [ground-link test a13](tests/01_ELECTRICAL.md)) | < 10 Ω 2-wire. Open: the die needs an M1 bond in step 19; log it, and check the via floors on W3 |

## 5. Records per die

Use the run-map die ID in both records. NODET has no R₀–R₅ entries. Record T9 structure identity separately.

### Detector resistance history

| Die ID / structure | R₀ | R₁ | R₂ | R₃ | R₄ | R₅ | Max ΔR/R₀ |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

### Electrical disposition

| Die ID | Variant | SNSPD–M1 | Ground link a13 | Leakage pass [verify] | Package? |
|---|---|---|---|---|---|
| | | | | | |
