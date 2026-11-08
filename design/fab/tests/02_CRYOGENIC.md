> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Cryogenic detector tests

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

> [!note] Provisional expectations
> Inductance/reset and switching-current ranges below were drafted for earlier v3 geometry. The [geometry audit](../../research/reports/SNSPD%20geometry%20audit.md) questions the margin near 5 K. Reconcile v3.1 and measure the plateau before sign-off.

**Order:**
1. **Test die**: T4 (A30 meander) or T4b (B60 meander) spare SNSPD, under SiO₂ cap + D2 only (same stack as the trap-die detectors). Bond the T4/T4b pads (150 µm L22 pads at the bottom of 10 µm D2 wells, 110 × 110 µm openings; the test die was laid out for probing, so check the bond fits [verify]) and test in a dipstick or the trap cryostat [verify available cryostat].
2. **Trap die** in the trap cryostat with the RF resonator connected.

**Expected numbers** [team calc unless noted]:

| Quantity | Value |
|---|---|
| Tc | ≈ 7.8–8 K (Dane 2017; Toomey 2018) |
| L_k | ≈ 3.3 µH for the v3.1 A30 meander at 70 pH/sq (7 nm NbN, dirty BCS; sim/15), so τ = L/50 Ω ≈ 66 ns (B60 ≈ 6.3 µH, 126 ns) |
| I_sw at ~5 K | **≈ 8–9 µA** for a 100 nm wire (Sedykh 2025's ≈ 15 µA at 2.2 K, Tc 7.5 K, scaled to 5 K; geometry audit), ≈ 1.1× that for the 130 nm wire with turn crowding [team calc, rough]. The older 15–25 µA came from heated NbN (Tc ≈ 10.9 K) and is optimistic |
| Pulse height | ≈ 50 Ω × I_b ≈ 0.75–1.25 mV |
| RF pickup bound | ≈ 1.4 µA (Al mirror only, 10 µm SiO₂ kept over the window, no ITO; 2-D upper bound, DESIGN_LOG step 17; v3.1 geometry in step 24), ≈ 16 % of an 8–9 µA switching current (≈ 8 % if both ends drain symmetrically) |

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
| b10 | **T9 geometry array** (step 24) | RF off; b2 at 2 K and 5 K, then b4/b5 on the meanders | I_sw ratios: rounded/sharp 100 nm (turn effect), 130/100 nm meanders, each meander / its straight reference (crowding factor R), long/short 130 nm (length or defects); 493 nm plateau vs width | Clem & Berggren 2011 Eq. 100 (R ≈ 0.5–0.65 predicted for sharp turns); Akhlaghi 2012 Fig. 2; Lusche 2013 Fig. 5. **Decides whether 130 nm keeps a saturated plateau at 493 nm and 5 K** |
| b9 | Bias gating | 10 µs bias ramps (Todaro thesis Sec. 6.3.1: 11 µs) | Count rate and DCR during and after the ramp | – |

Ba⁺ (q/m ≈ 0.0072 e/u) lies below Hampel's stated range of q/m ≥ 0.01 e/u. b6 is the direct test of that envelope at our 53–70 V and 28 MHz (research report implication 8).

**Go to trapping if** [verify all]:

- I_sw(53 V RF) ≥ 0.8 × I_sw(RF off);
- a usable bias exists where the b4 counts are ≥ 80 % of the plateau (or of the maximum) and DCR ≤ 100 cps with RF on;
- no latching at the operating bias.
