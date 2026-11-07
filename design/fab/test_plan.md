> **Claude-authored.** Test plan from finished wafer to first trapped-ion readout, for the v2 dies `trap_die_v2_A30` (A30) and `trap_die_v2_B60` (B60); all test structures (T1–T7) are on the separate test die `test_die_v2` (one per 10 × 10.8 mm wafer tile). Numbers marked [team calc] were computed for this project. [verify] marks values to confirm against the source figure, the instrument or the lab. Pass criteria are starting points.

# Test plan

## (a) Room-temperature electrical test

**When:** step 17 (wafer, before dicing) and again after packaging (step 19, through the carrier pins).
**Tool:** ProbeStation-Summit-11000 + SMUs.
**Reference:** Dietl 2025 used a 120-needle card; we probe manually, so the tests are prioritised.
**Pads:** trap-die pad names and coordinates from `gds/trap_die_v2_A30_pads.csv` (TL/TR/BL/BR rows, RF, C, SNS, SNG, GND-n, M1-n). Test-die structures are probed on their own pads; the test dies stand in for the trap dies of their run.

**Safety rules for the SNSPD**
- Never put more than 1 V or 100 nA across the meander.
- During every high-voltage test, keep **SNSPD_S and SNSPD_G (pads SNS, SNG) tied together and grounded** [inference].
- Wear a grounded strap. Touch down with the SMU at 0 V.

| # | Test | Pads | Stimulus | Pass | Source |
|---|---|---|---|---|---|
| a1 | RF leakage | RF ↔ M1 (any M1-n), RF ↔ Au ground fill (GND-n), RF ↔ C (centre DC), RF ↔ caps 33–36 (TL1, TR1, BL1, BR1) and the segments nearest the closed end of the RF U (17, 32: TR2, BR2) | **300 V DC** | **≤ 100 nA; run twice** (catches breakdown-induced shorts) | Dietl 2025 |
| a2 | DC leakage | each DC pad ↔ both neighbours in its pad row, ↔ M1, ↔ ground fill | **50 V** | **≤ 100 nA**; and **> 100 MΩ between every pair including the ground plane** | Dietl 2025; Stick 2010 |
| a3 | Continuity | T6 loop (test die, two pads) | **1 mA** | **0–100 mV** (expect ~3 Ω, so ~3 mV [team calc]) | Dietl 2025 two-pad loop |
| a4 | Dielectric | T2 Au/D2/M1 capacitor (test die, 0.8 × 0.8 mm Au plate ↔ M1 pad) | C at 1 MHz [verify LCR availability]; leakage at 50 V | C ≈ 2.1 pF [team calc]; ≤ 100 nA | Stick 2010; research report implication 28 |
| a5 | Gap leakage / redeposition | T1 comb (test die, 5 µm gaps) | 50 V (then 300 V on sacrificial dies only) | ≤ 100 nA | Dietl 2025; Sussex 2022 (redeposition) |
| a6 | NbN Rsq | T3 4-wire (test die) | ≤ 1 µA | Matches the step-7 value within 10 % | – |
| a7 | **Meander R** | trap die SNS ↔ SNG; test die T4 (A30 meander) and T4b (B60 meander) | ≤ 1 V, ≤ 100 nA | ≈ 18 MΩ (A30) / 36 MΩ (B60) [team calc]; **ΔR/R₀ ≤ 10 %** (Todaro saw 12–30 % rises) | Todaro Supp. "Trap fabrication" |
| a8 | SNSPD isolation | SNS + SNG tied ↔ M1; ↔ C | ≤ 1 V to M1; ≤ 10 V to C [verify] | > 1 GΩ | – |
| a9 | Top ITO | T5 4-wire (test die); T5 outer finger ↔ M1 | ≤ 1 mA; 50 V | Rsq within 30 % of the witness; isolation ≤ 100 nA | – |
| a10 | RF capacitance (packaged only) | RF pin ↔ ground pins | LCR at 1 MHz | A few pF from the chip [team calc from DESIGN_LOG step 10: 0.36 pF/mm per rail], plus the carrier. Record it to predict the resonator frequency | Stick 2010 (7 pF trap + CPGA) |
| a11 | Buried-ITO grounding | T7 via chain (test die), end M1 pads | ≤ 100 µA [verify] | ITO links ≈ 4–7 kΩ + 14 × R_via; R_via ≤ 1 kΩ [team calc; verify] (`process_checks.md` section 3) | DESIGN_LOG step 10 (a floating buried ITO is 9× worse than none) |
| a12 | Dose array | T8 D1–D7 (test die), each meander's two pads | ≤ 1 V, ≤ 100 nA | R vs dose factor: R ∝ 1/width. Breaks (open) or bridges (low R) mark the usable dose window [team inference] | `mask_list.md` section 2 |

The trap's DC electrodes have one pad each (no Dietl loop), so continuity is only tested on T6 (test die). A broken lead shows up later as a missing DC response.

**Order per die:** trap die a7 → a8 → a2 → a1 (a10 after packaging); test die a7 → a12 → a6 → a3 → a11 → a9 → a4 → a5. Low-voltage SNSPD tests come first.

**Record:** pass/fail per die ID of `gds/run_<name>_map.csv`, per-die ΔR/R₀, leakage values.

## (b) Cryogenic SNSPD characterisation before trapping

**Order:**
1. **Test die**: T4 (A30 meander) or T4b (B60 meander) spare SNSPD, both with buried ITO + via + top ITO. Bond the T4/T4b pads (150 µm L22 pads at the bottom of 10 µm D2 wells, 110 × 110 µm openings; the test die was laid out for probing, so check the bond fits [verify]) and test in a dipstick or the trap cryostat [verify available cryostat].
2. **Trap die** in the trap cryostat with the RF resonator connected.

**Expected numbers** [team calc unless noted]:

| Quantity | Value |
|---|---|
| Tc | ≈ 7.8–8 K (Dane 2017; Toomey 2018) |
| L_k | ≈ 3.2–4.7 µH for A30 (70–105 pH/sq), so τ = L/50 Ω ≈ 64–94 ns (B60 ≈ 2×) |
| I_sw at ~5 K | ~15–25 µA (scaled from Najafi 2015 for ~5 nm; 7 nm may be higher) |
| Pulse height | ≈ 50 Ω × I_b ≈ 0.75–1.25 mV |
| RF pickup bound | ≈ 0 with grounded buried ITO (2-D); 0.72 µA if the ITO ground is ineffective (Al only); 6.6 µA if the buried ITO floats (DESIGN_LOG step 10) |

| # | Measurement | Conditions | Plot | Compare with |
|---|---|---|---|---|
| b1 | R(T) through Tc (meander and T3) | cooldown | R vs T | Witness Tc |
| b2 | I–V, I_sw, latching current | RF off; T = base … 7 K | I_sw vs T | Hampel Fig. 3(d) (6 K operation) |
| b3 | Pulse shape | scope after the amplifier | Mean pulse; fitted τ, hence L_k | Hampel: 25 ns, 1.3 µH |
| b4 | **Count rate vs bias, 493 nm flood** (LED/laser through a fibre or window, attenuated) | RF off | Count rate vs I_b/I_sw (plateau?) | Todaro PRL Fig. 2; Hampel Fig. 3 |
| b5 | **Dark counts vs bias** | light off, shutters closed | DCR vs I_b | – |
| b6 | **RF on / off** | 28 MHz at V_RF = 0, 20, 40, **53, 60, 70 V** | I_sw vs V_RF; b4 and b5 curves per V_RF on one plot | **Todaro Fig. 3 / Supp. Fig. S4** (8.9 → 5.3 µA with RF; flattening means induced current); **Hampel Figs. 3–4** (grounded mirror: shift without flattening means heating); **Slichter 2017** Sec. 4 / App. A (lead-dominated pickup; cancellation tone) |
| b7 | Clicks with bias off | RF on, light on and off | Rate vs V_RF | Todaro PRL p. 4 (detector pulses with RF on and bias off) |
| b8 | RF heating | I_sw measured ≤ 10 µs after the RF switches off, against the b2 I_sw(T) calibration | ΔT vs V_RF | Hampel: ~0.5 K after 45 V at 70 MHz. Expect less at 28 MHz [inference: dissipation ∝ (ωV)²] |
| b9 | Bias gating | 10 µs bias ramps (Todaro thesis Sec. 6.3.1: 11 µs) | Count rate and DCR during and after the ramp | – |

Ba⁺ (q/m ≈ 0.0072 e/u) lies below Hampel's stated range of q/m ≥ 0.01 e/u. b6 is the direct test of that envelope at our 53–70 V and 28 MHz (research report implication 8).

**Go to trapping if** [verify all]:
- I_sw(53 V RF) ≥ 0.8 × I_sw(RF off);
- a usable bias exists where the b4 counts are ≥ 80 % of the plateau (or of the maximum) and DCR ≤ 100 cps with RF on;
- no latching at the operating bias.

## (c) Readout electronics chain

The structure follows Todaro Supp. Fig. S2 (Fig. S3 [verify which figure shows the full chain]).

```
SNSPD_S ─ on-chip lead ─ bond ─ cryo coax ─┬─ bias tee ─ RF port ─ amplifiers (~46 dB total [verify gain in Todaro Supp. Fig. S2/S3])
                                           │                     ─ notch at f_rf = 28 MHz (≥ 40 dB)
                                           │                     ─ low-pass
                                           │                     ─ comparator ─ LVTTL ─ ARTIQ TTL input (edge counter / timestamps)
                                           └─ DC port ─ series R (Hampel: 10 kΩ) ─ isolated low-noise voltage source,
                                                         gated by ARTIQ (DAC or switch, ~10 µs ramps)
SNSPD_G ─ bond ─ ground (or a matched 50 Ω for symmetric termination, see below)
```

| Element | Choice | Reason / source |
|---|---|---|
| Notch | ≥ 40 dB at 28 MHz | Todaro: 7th-order Bessel notch, 40 dB at f_rf, 14 MHz 3 dB bandwidth, because RF pickup was "several times larger" than the ~250 µV pulses (Supp. Fig. S2) |
| Low-pass | Todaro used a 25 MHz Gaussian LPF, which gave 18 dB more at **67 MHz**. **At our 28 MHz a 25 MHz LPF adds almost nothing.** Use a lower corner (~10–15 MHz) and/or a steeper notch [inference] | Our pulses are slow (τ ≈ 60–190 ns), so a ~10 MHz bandwidth keeps the rising edge (~30 ns) [inference] |
| Gain | ~46 dB [verify]: 1 mV pulses become ~200 mV at the comparator | – |
| Comparator threshold | ~50 % of the mean pulse height; tune on the b4 pulse-height histogram | Pulse heights vary up to 3× with RF-modulated bias (Todaro Supp.) |
| Termination | Consider symmetric (both leads into 50 Ω) to cancel the uniform induced current I₀ | Todaro Supp. Fig. S4 remedies; Slichter App. A |
| Bias gate | Bias on only during readout. Bias off during loading, photoionisation and Raman / sideband work | Todaro thesis Sec. 6.3.1; PRL p. 4 (stray-light clicks blocked sideband cooling over the detector) |

**ARTIQ:** the comparator output goes to a TTL input. Count in the readout gate and also time-tag the edges: the same timestamps give RF-photon correlation for micromotion (section d).

## (d) First trapping checklist

1. **Pre-cool**
   - Pad isolation through the feedthroughs (repeat a1, a2, a7).
   - RF resonator frequency and Q with the chip installed (Leibrandt: ground plane raised Q from ≈ 100 to ≈ 150).
   - RF pick-off divider calibrated.
2. **Cold**
   - Short repeat of b2, b4 and b6 on the trap die.
   - Set the bias gate to off.
3. **RF:** 28 MHz, ramp to **53 V** (q ≈ 0.30, radial ≈ 3 MHz, depth ≈ 52 meV; DESIGN_LOG steps 1–2).
4. **DC: load-zone set**
   - The first row of `sim/out/12_final_chip/trap_die_v2_A30/waveforms.csv` (`sim/12_final_chip_check.py`; numbers in `summary.json` and `transport.png` in the same folder).
   - Loading zone: GDS (−300, 0), ITVG y = −600 µm (readout zone GDS (300, 0) is the ITVG origin). Expected (DESIGN_LOG step 13, v2 GDS): null height 50.08 µm, axial 0.80 MHz, radial 2.89 / 2.97 MHz, radial axes tilted 10.7°, max |V| 9.05 V (`summary.json` → `loading`).
5. **Load at the loading zone.**
   - 493 + 650 nm cooling; photoionisation (791 + 337/450 nm or 553/554 + 405 nm per the lab; Graham 2014, Shi 2023); oven with shutter, or ablation.
   - **SNSPD bias off**, because the PI beams scatter (DESIGN_LOG step 9: no stray-light rejection in the stack).
   - Beam clipping on the narrow die (`sim/11_beam_clearance.py`) [team calc]: fraction of beam power hitting the surface 1.1 × 10⁻⁵ (493 nm), 1.1 × 10⁻⁴ (650 nm), 1.4 × 10⁻⁶ (405 nm). Bond wires at |x| ≥ 2.4 mm are outside the beam paths.
   - Detect with the external imaging system.
6. **Micromotion at the loading zone**
   - Shim with the DC solution sets. Shim cost ≈ 0.45 / 0.16 / 0.02 V per 100 V/m in x / y / z (DESIGN_LOG step 3).
   - Generic stray fields in Todaro's trap were ≈ 300 V/m in-plane and 750 V/m vertical (thesis Sec. 5.3.2).
7. **Shuttle to readout**
   - Step through `waveforms.csv`: 61 positions on 10 µm steps from GDS x = −300 to +300, a fixed set of all 35 DC electrodes, max |V| 7.33 V, ≤ 1.59 V change per step, axial 0.800 MHz and height 50.08–50.09 µm throughout (DESIGN_LOG step 13; `summary.json` → `transport`).
   - Go slowly at first (~1 ms per step [verify]); the waveforms are quasi-static, with no adiabatic timing designed.
   - Ramp into the 10° tilt set at the readout zone after arrival.
   - Readout-zone beams on; confirm the ion arrives on the camera.
8. **Readout zone**
   - Bias on (gated). Count rate vs ion axial position (±100 µm scan) gives the crosstalk profile. Todaro: < 2 % at 80 µm (thesis Sec. 6.4.3).
   - Expected rate [team calc, rough]: geometric 3.25 % (DESIGN_LOG step 7) × absorption ~0.5 × internal efficiency [unknown] ≈ 1–1.5 % of scattered photons.
9. **Micromotion at readout**
   - RF-photon correlation from the SNSPD timestamps.
   - Compare the compensation fields with the loading zone and with the window electrostatics. Predicted Δh ≈ −1.2 µm from the window recess for A30, ≈ −2.0 µm for B60 (DESIGN_LOG step 6), so h ≈ 48.9 µm (A30) / 48.1 µm (B60) against the planar 50.09 µm (`summary.json` → `readout.null_z_with_recess`).
10. **Ion height at readout:** vertical beam scan, against the ≈ 48.9 µm (A30) / 48.1 µm (B60) prediction (planar 50.08 / 50.09 µm at loading / readout; DESIGN_LOG step 13).
11. **Readout fidelity**
    - Prepare bright (S₁/₂) and dark (shelved to D₅/₂, method per the lab; 614 nm deshelve).
    - Compare threshold and adaptive analysis against Todaro (F = 0.9991 in a mean of 46 µs, adaptive; 0.9988 at 125 µs, threshold; PRL p. 4).
12. **Heating:** sideband or Doppler-recooling heating rate at the loading zone vs the readout zone, bias off and on. Click-kick heating vs click rate (Todaro: 0.009(5) quanta/click unshielded). Expect less with the grounded top ITO; there is no published shielded number.

### Plots to make

| # | Plot | From |
|---|---|---|
| 1 | Meander R₀…R₅ per die, and the wafer map | (a), process_checks |
| 2 | I_sw vs T; R vs T | b1, b2 |
| 3 | Count rate and DCR vs I_b, one curve per V_RF | b4–b6 |
| 4 | I_sw vs V_RF, with Todaro and Hampel points (normalised) | b6 |
| 5 | ΔT (from I_sw recovery) vs V_RF | b8 |
| 6 | Count rate vs ion axial position (crosstalk) | d8 |
| 7 | Micromotion-compensation fields at both zones | d6, d9 |
| 8 | Bright / dark count histograms; fidelity vs readout time (threshold and adaptive) | d11 |
| 9 | Heating rate at both zones; heating vs click rate | d12 |
| 10 | Measured ion height vs prediction along the axis | d10, `sim/out/12_final_chip/trap_die_v2_A30/summary.json` (`null_along_axis`) |
