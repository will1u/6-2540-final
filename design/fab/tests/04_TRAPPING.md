> **Claude-authored.** Rewritten for v4 2026-11-09; run R1_ONE 2026-11-12 (the A30 die is team test 4; the NODET die is team test 3; the R1_TRAP and R1_FULL die lists are superseded).

# First trapping checklist

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

For the NODET die of R1_ONE (team test 3), use [R1_TRAP expected values](../RUNSHEET_R1_TRAP.md#4-first-trapping-on-a-nodet-die-expected-values) (the same trap design) and omit detector actions. The checklist below is for integrated-detector operation: the A30 die of R1_ONE (team test 4). The B60 die is a spare and is not in the R1_ONE plan.

1. **Pre-cool**
   - Pad isolation through the feedthroughs (repeat a1, a2, a7; a8 and a19 on the SNSPD pads of A30 and B60).
   - RF resonator frequency and Q with the chip installed. Leibrandt: a ground plane raised Q from ≈ 100 to ≈ 150. v4 has no die-wide plane, so that result is not a direct reference [inference]. Measure the v4 Q [verify].
   - RF pick-off divider calibrated.
2. **Cold**
   - Short repeat of b2, b4 and b6 on the trap die.
   - Set the bias gate to off.
3. **RF:** 28 MHz, ramp to **53 V** (q ≈ 0.30, radial ≈ 3.0 MHz, depth ≈ 52 meV; DESIGN_LOG steps 1–2, 28–29).
4. **DC: load-zone set**
   - The first row of the loading-zone set in `sim/out/12_final_chip/trap_die_v4_A30/waveforms.csv` (`sim/12_final_chip_check.py`; numbers in `summary.json` in the same folder). Use the `--centre-dc-zero` set for transport (step 7); the folder `trap_die_v4_A30_V2zero` is taken to be that run [verify]. The `pad180` subfolder holds the 180 µm pad-pitch variant; the top-level folder is taken as the current 360 µm layout [verify].
   - Loading zone: GDS (−240, 0), ITVG y = −480 µm (readout zone GDS (+240, 0) is the ITVG origin). Expected [team calc, DESIGN_LOG steps 25–29]: null height 49.97 µm (planar model), axial 0.80 MHz, radial ≈ 3.0 MHz, 10° radial tilt needs 7.5 V. Max \|V\| at loading: [verify; not in the notes].
5. **Load at the loading zone.**
   - 493 + 650 nm cooling; photoionisation (791 + 337/450 nm or 553/554 + 405 nm per the lab; Graham 2014, Shi 2023); oven with shutter, or ablation.
   - **SNSPD bias off**, because the PI beams scatter (DESIGN_LOG step 9: no stray-light rejection in the stack).
   - Beam clipping on the 10 × 10 mm die (`sim/11_beam_clearance.py`, full-chip row) [team calc]: about 1.7 × 10⁻² of the 493 nm beam (3.2 × 10⁻² at 650 nm, 9.6 × 10⁻³ at 405 nm) hits the surface. Expect much more scattered light than on the v2 narrow die. Bond wires stay out of the beam-exit corners.
   - Detect with the external imaging system.
6. **Micromotion at the loading zone**
   - Shim with the DC solution sets. Shim cost ≈ 0.45 / 0.16 / 0.02 V per 100 V/m in x / y / z (DESIGN_LOG step 3; an early value, recheck for v4 [verify]).
   - Generic stray fields in Todaro's trap were ≈ 300 V/m in-plane and 750 V/m vertical (thesis Sec. 5.3.2).
7. **Shuttle to readout**
   - Step through the transport set with the centre DC held at 0 V (the v4 transport setting; `12_final_chip_check.py --centre-dc-zero`, the folder in step 4). 10 µm steps from GDS x = −240 (loading) to +240 (readout) [verify the step count in `waveforms.csv`]. Expected [team calc, DESIGN_LOG steps 25, 29]: max \|V\| 6.6 V, ≤ 1.71 V change per step, axial 0.80 MHz.
   - With the centre DC free, the notes give max \|V\| 7.59 V (A30) / 8.00 V (B60), with larger steps (DESIGN_LOG steps 25, 29).
   - Go slowly at first (~1 ms per step [verify]); the waveforms are quasi-static. A transport timing model now exists (`sim/20_transport_timing.py`); its ramp timing is not used on this page [verify before use].
   - Ramp into the 10° tilt set at the readout zone after arrival.
   - Readout-zone beams on; confirm the ion arrives on the camera.
8. **Readout zone**
   - Bias on (gated). Count rate vs ion axial position (±100 µm scan) gives the crosstalk profile. Todaro: < 2 % at 80 µm (thesis Sec. 6.4.3).
   - Expected rate [team calc, rough]: the absorbed fraction of emitted 493 nm photons with the 160 nm cap (sim 15b) is A30 **1.47 %** (E2) / 1.72–1.74 % (E1) and B60 **2.71 %** (E2) / 3.03–3.08 % (E1). Collection is already included in these fractions. Multiply by the emission rate and the internal detection efficiency, which is not included [unknown]. At an emission rate of 10⁶–10⁷ s⁻¹ (the defensible range in the [L1 note](../../research/research_notes/Loose%20ends%202026-11/L1_ba_emission_and_detection.md), a judgment), A30 gives 1.5–15 counts per 100 µs before the internal efficiency [team calc].
9. **Micromotion at readout**
   - RF-photon correlation from the SNSPD timestamps.
   - Compare the compensation fields with the loading zone and with the window electrostatics. The window recess lowers the null over the window by **1.19 µm (A30, E2)** or **≤ 0.37 µm (E1)**; for B60, **2.04 µm (E2)** or **≤ 0.55 µm (E1)** (DESIGN_LOG steps 25–26; sim 15b). The null height over the window is then ≈ 48.8 µm (A30, E2), ≥ 49.6 µm (A30, E1), ≈ 47.9 µm (B60, E2), ≥ 49.4 µm (B60, E1) against the planar 49.98 µm at readout [team calc].
   - [verify for R1_ONE] The window and recess numbers above come from the sims run before the 2026-11-12 facts (the mirror is raised, and the SiO₂ off the wires is 348 nm). They were not re-run for R1_ONE.
   - Predicted residual micromotion after undoing the drop with a 10° tilt set [team calc, DESIGN_LOG step 29]: A30 ≈ 55 nm (E1) / 173 nm (E2); B60 ≈ 81 nm (E1) / 291 nm (E2).
10. **Ion height at readout:** vertical beam scan, against the predictions in step 9 (planar 49.97 / 49.98 µm at loading / readout; DESIGN_LOG steps 13, 25–29).
11. **Readout fidelity**
    - Prepare bright (S₁/₂) and dark (shelved to D₅/₂, method per the lab; 614 nm deshelve).
    - Compare threshold and adaptive analysis against Todaro (F = 0.9991 in a mean of 46 µs, adaptive; 0.9988 at 125 µs, threshold; PRL p. 4).
12. **Heating:** sideband or Doppler-recooling heating rate at the loading zone vs the readout zone, bias off and on. Click-kick heating vs click rate (Todaro: 0.009(5) quanta/click unshielded). v4 has no conducting film over the window: the window floor is 160 nm SiO₂ over the NbN wires (HSQ 50 nm plus PECVD cap 110 nm), and the Au window walls are 0.35 µm (E1) or 6 µm (E2) deep. Compare with Todaro's unshielded value and with NODET.

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
| 10 | Measured ion height vs prediction along the axis | d10, `sim/out/12_final_chip/trap_die_v4_A30/summary.json` (`null_along_axis`) |
