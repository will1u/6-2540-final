> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Cryogenic detector tests

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

> [!note] Provisional expectations
> Values below are v4 where the v4 layout or simulations give one. The inductance and switching-current ranges use the v3.1 meander, which the v4 layout keeps (130 / 200 nm lines and pitch, 160 lines). The [geometry audit](../../research/reports/SNSPD%20geometry%20audit.md) questions the margin near 5 K. Reconcile against the released GDS and measure the plateau before sign-off.

**Order:**
1. **Test die**: T4 (A30 meander) or T4b (B60 meander) spare SNSPD, under the v4 detector stack (local Al mirror, 238 nm SiO₂ spacer, NbN, HSQ + SiO₂ cap at 160 ± 10 nm), the same stack as the trap-die detectors. Each has its own mirror probe pad. Bond the SNSPD pads and the mirror probe pad as laid out in `test_die_v4.gds` [verify pad sizes and bond fit], and test in a dipstick or the trap cryostat [verify available cryostat].
2. **Trap die** in the trap cryostat with the RF resonator connected.

**Expected numbers** [team calc unless noted]:

| Quantity | Value |
|---|---|
| Tc | ≈ 7.8–8 K (Dane 2017; Toomey 2018) |
| L_k | ≈ 3.3 µH for the v3.1 A30 meander at 70 pH/sq (7 nm NbN, dirty BCS; sim/15), so τ = L/50 Ω ≈ 66 ns (B60 ≈ 6.3 µH, 126 ns) |
| I_sw at ~5 K | **≈ 8–9 µA** for a 100 nm wire (Sedykh 2025's ≈ 15 µA at 2.2 K, Tc 7.5 K, scaled to 5 K; geometry audit), ≈ 1.1× that for the 130 nm wire with turn crowding [team calc, rough]. The older 15–25 µA came from heated NbN (Tc ≈ 10.9 K) and is optimistic |
| Pulse height | ≈ 50 Ω × I_b ≈ 0.75–1.25 mV |
| RF pickup, nanowire | v4 simulations (sim 10b, DESIGN_LOG step 26): **0.96 µA (E2) / 1.92 µA (E1)** in the nanowire, 2-D. The mirror path adds at most 0.73–0.97 µA on E2 and 0.74–0.99 µA on E1 with the 100 nm inlaid Al (`sim/10c`, DESIGN_LOG step 37). About 3.2 mA of RF current flows along the mirror strip to ground and dissipates 34–47 µW in it at room-temperature resistivity; no thermal model, so watch the switching current against RF amplitude as the sign of heating |
| RF pickup, lead model | Sim 19, lumped: a plain 50 Ω line on the signal lead with the return grounded gives **≈ 4.1 µA (E2) / 2.6 µA (E1)** through the A30 nanowire (upper bound). Each slot lead collects ≈ 44.5 µA (E2) / 28.6 µA (E1) of common-mode 28 MHz current over its 2.24 mm length (`sim/10c`, DESIGN_LOG step 37; sim 18 / step 28 gave 28.3 µA for E1) |
| Reference for the RF comparison | sim 19 expresses its results as a percentage of an 8 µA switching current; its notes give 8–20 µA as the range [team calc, upper bound]. The I_sw row above is 8–9 µA, so the two ranges do not agree [verify] |

The termination at SNS and SNG is an **open decision** ([OPEN_DECISIONS](../OPEN_DECISIONS.md), RF grounding / filters). The lumped figures above assume the plain 50 Ω case; they are not a choice of termination. Record the termination used for each b6 run.

| # | Measurement | Conditions | Plot | Compare with |
|---|---|---|---|---|
| b1 | R(T) through Tc (meander and T3) | cooldown | R vs T | Witness Tc |
| b2 | I–V, I_sw, latching current | RF off; T = base … 7 K | I_sw vs T | Hampel Fig. 3(d) (6 K operation) |
| b3 | Pulse shape | scope after the amplifier | Mean pulse; fitted τ, hence L_k | Hampel: 25 ns, 1.3 µH |
| b4 | **Count rate vs bias, 493 nm flood** (LED/laser through a fibre or window, attenuated) | RF off | Count rate vs I_b/I_sw (plateau?) | Todaro PRL Fig. 2; Hampel Fig. 3 |
| b5 | **Dark counts vs bias** | light off, shutters closed | DCR vs I_b | – |
| b6 | **RF on / off** | 28 MHz at V_RF = 0, 20, 40, **53, 60, 70 V** (53 V is the v4 operating amplitude); termination at SNS and SNG recorded for each run | I_sw vs V_RF; b4 and b5 curves per V_RF on one plot | **Compare I_sw(V_RF) with I_sw(RF off) from b2 at the same temperature.** Scale the shift against the pickup values above and the 8–20 µA reference. **Todaro Fig. 3 / Supp. Fig. S4** (8.9 → 5.3 µA with RF; flattening means induced current); **Hampel Figs. 3–4** (grounded mirror: shift without flattening means heating); **Slichter 2017** Sec. 4 / App. A (lead-dominated pickup; cancellation tone) |
| b7 | Clicks with bias off | RF on, light on and off | Rate vs V_RF | Todaro PRL p. 4 (detector pulses with RF on and bias off) |
| b8 | RF heating | I_sw measured ≤ 10 µs after the RF switches off, against the b2 I_sw(T) calibration | ΔT vs V_RF | Hampel: ~0.5 K after 45 V at 70 MHz. Expect less at 28 MHz [inference: dissipation ∝ (ωV)²] |
| b9 | Bias gating | 10 µs bias ramps (Todaro thesis Sec. 6.3.1: 11 µs) | Count rate and DCR during and after the ramp | – |
| b10 | **T9 geometry array** (step 24) | RF off; b2 at 2 K and 5 K, then b4/b5 on the meanders | I_sw ratios: rounded/sharp 100 nm (turn effect), 130/100 nm meanders, each meander / its straight reference (crowding factor R), long/short 130 nm (length or defects); 493 nm plateau vs width | Clem & Berggren 2011 Eq. 100 (R ≈ 0.5–0.65 predicted for sharp turns); Akhlaghi 2012 Fig. 2; Lusche 2013 Fig. 5. **Decides whether 130 nm keeps a saturated plateau at 493 nm and 5 K** |

Ba⁺ (q/m ≈ 0.0072 e/u) lies below Hampel's stated range of q/m ≥ 0.01 e/u. b6 is the direct test of that envelope at our 53–70 V and 28 MHz (research report implication 8).

**Go to trapping if** [verify all]:

- I_sw(53 V RF) ≥ 0.8 × I_sw(RF off);
- a usable bias exists where the b4 counts are ≥ 80 % of the plateau (or of the maximum) and DCR ≤ 100 cps with RF on;
- no latching at the operating bias.
