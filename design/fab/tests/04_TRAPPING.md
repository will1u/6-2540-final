> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# First trapping checklist

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

For NODET, use [R1_TRAP expected values](../RUNSHEET_R1_TRAP.md#4-first-trapping-on-a-nodet-die-expected-values) and omit detector actions. The checklist below is for integrated-detector operation.

1. **Pre-cool**
   - Pad isolation through the feedthroughs (repeat a1, a2, a7).
   - RF resonator frequency and Q with the chip installed (Leibrandt: ground plane raised Q from ≈ 100 to ≈ 150).
   - RF pick-off divider calibrated.
2. **Cold**
   - Short repeat of b2, b4 and b6 on the trap die.
   - Set the bias gate to off.
3. **RF:** 28 MHz, ramp to **53 V** (q ≈ 0.30, radial ≈ 3 MHz, depth ≈ 52 meV; DESIGN_LOG steps 1–2).
4. **DC: load-zone set**
   - The first row of `sim/out/12_final_chip/trap_die_v3_A30/waveforms.csv` (`sim/12_final_chip_check.py`; numbers in `summary.json` and `transport.png` in the same folder).
   - Loading zone: GDS (−300, 0), ITVG y = −600 µm (readout zone GDS (300, 0) is the ITVG origin). Expected (DESIGN_LOG step 19, v3 GDS; same as v2 at the loading zone): null height 50.08 µm, axial 0.80 MHz, radial 2.89 / 2.97 MHz, radial axes tilted 10.7°, max \|V\| 9.05 V (`summary.json` → `loading`).
5. **Load at the loading zone.**
   - 493 + 650 nm cooling; photoionisation (791 + 337/450 nm or 553/554 + 405 nm per the lab; Graham 2014, Shi 2023); oven with shutter, or ablation.
   - **SNSPD bias off**, because the PI beams scatter (DESIGN_LOG step 9: no stray-light rejection in the stack).
   - Beam clipping on the 10 × 10 mm die (`sim/11_beam_clearance.py`, full-chip row) [team calc]: about 1.7 × 10⁻² of the 493 nm beam (3.2 × 10⁻² at 650 nm, 9.6 × 10⁻³ at 405 nm) hits the surface. Expect much more scattered light than on the v2 narrow die. Bond wires stay out of the beam-exit corners.
   - Detect with the external imaging system.
6. **Micromotion at the loading zone**
   - Shim with the DC solution sets. Shim cost ≈ 0.45 / 0.16 / 0.02 V per 100 V/m in x / y / z (DESIGN_LOG step 3).
   - Generic stray fields in Todaro's trap were ≈ 300 V/m in-plane and 750 V/m vertical (thesis Sec. 5.3.2).
7. **Shuttle to readout**
   - Step through `waveforms.csv`: 61 positions on 10 µm steps from GDS x = −300 to +300, a fixed set of all 35 DC electrodes, max \|V\| 7.33 V, ≤ 1.59 V change per step, axial 0.800 MHz and height 50.08–50.09 µm throughout (DESIGN_LOG step 13; `summary.json` → `transport`).
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
12. **Heating:** sideband or Doppler-recooling heating rate at the loading zone vs the readout zone, bias off and on. Click-kick heating vs click rate (Todaro: 0.009(5) quanta/click unshielded). v3 has no conducting film over the window (bare SiO₂), so expect roughly Todaro's unshielded value; compare with NODET.

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
| 10 | Measured ion height vs prediction along the axis | d10, `sim/out/12_final_chip/trap_die_v3_A30/summary.json` (`null_along_axis`) |
