> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Steps 9 to 16 SiO₂ and Au electrodes

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

Both runs, with depth/coverage changes in [R1_TRAP](../RUNSHEET_R1_TRAP.md). Step 10 is retired. **Apply 16a before 16.** Keep the readout-window patch on detector dies.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 9. D2: 10 µm PECVD SiO₂ in increments, stress-balanced

- **Purpose:** RF-to-ground dielectric. V_b ≈ 503 V at 10 µm by Sterling's model [team calc]. Sussex measured > 250 V_amp at 8 µm.
- **Tool:** PECVD-Oxford-TEOS or PECVD-Samco-PD220 at **≤ 300 °C**; Filmstress-Tencor-FLX2320.
- **Recipe:**
  - Deposit in **1–2 µm increments with cool-down pauses** (Leibrandt 2009). JoVE ran ~300 nm/min at 350 °C [verify our rate at 300 °C].
  - **Interleave backside oxide** (JoVE put 14 µm on both sides). Example: front 2 µm → bow → back 2 µm → bow … to front 10 µm, back ~8–10 µm (tune from W3).
  - Do face-down runs only after ≥ 2 µm is on the front, with a clean platen [verify whether the tool allows face-down].
- **Why balance:** a 10 µm film at −200 MPa [assumed, verify] on 525 µm Si bows a 100 mm wafer by ~300 µm (Stoney) [team calc], which is too much for the MLA and EBL chucks.
- **Target:** front 10.0 ± 0.5 µm (reflectometer / ellipsometer [tool name not verified]); \|bow\| ≤ 50 µm [verify chuck limit]; no cracks or crazing.
- **Hazards:** heat on the Al (hillocks) and on the capped NbN. Micro-voids may outgas (Leibrandt).
- [ ] Done — date: ____ operator: ____ increments: ____ bow log: ____ t_D2: ____ notes: ____

## 10. Removed in v3

This was the L30 top ITO on D2. v3 has no ITO; go from step 9 straight to step 11.

## 11. L40 D2 openings (pads, M1 bond openings, fill-to-M1 ground vias, L50 alignment crosses)

- **Ground vias (step 22):** eight 150 × 150 µm openings per trap die, at (±4700, ±1000) and (±1000, ±2500), etched with everything else in this job. The plated Au ground fill covers them in step 14 (≥ 25 µm overlap all round), which ties the fill to M1 on chip. They need no L45 patch.
- **Tool:** MLA150; RIE-F-Samco-230iP or RIE-PlasmaTherm-210RL.
- **Recipe:**
  - Thick positive resist **≥ 8 µm** (AZ 10XT / AZ 4620-class [verify stock]). JoVE used 6 µm. Expose L40 **drawn**.
  - Etch with CHF₃ 25 / CF₄ 5 / Ar 50 sccm, 130 mTorr, 600 W, ~360 nm/min (JoVE) [verify on our tool].
  - Depth: ~10.36 µm over M1 (D2 + cap + spacer) and ~10.1 µm over the L22 pads, so ~29 min + 10–15 % over-etch. Run in ≤ 5 min segments with cool-down to save the resist [inference].
  - Stops on Al (AlF₃) and on Au.
- **Layer / align:** L40 → L1 (±5 µm).
- **Inspect:**
  - Dektak depth; clean metal at every opening floor, including all eight ground vias.
  - **First probe access since step 7:** meander R₁ (SNS/SNG) and T3/T4/T4b on the test dies.
  - SNSPD pads (both tied together) to M1 (any M1-n opening) at ≤ 1 V must read **> 1 GΩ** (no short through the spacer to the Al).
- **Hazards:** heat in the long etch. The window area is under resist here.
- [ ] Done — date: ____ operator: ____ etch time: ____ R₁: ____ SNSPD–M1: ____ notes: ____

## 12. Plating seed Ti 15 nm / Au 50 nm (PTB)

- **Tool:** Sputter-AJA-* (sputter for step coverage; PTB evaporated).
- **Ar pre-clean first (step 22):** an in-situ RF Ar sputter clean before the Ti, to remove the AlF₃ and native Al₂O₃ that the step-11 fluorine etch leaves on the Al at the ground-via floors. Without it the fill-to-M1 contact may be open. Wire bonds at M1-n break through this film; a sputtered seed does not [inference; verify the AJA has a substrate RF etch, and the time, on W3].
- **Sidewall coverage (step 22):** the seed must run continuously down the ~10.4 µm via wall, or the via floor is never plated and never connected. Sputtering with substrate rotation coats the wall thinly; the 15 nm Ti also sits between the Al and the Au, which slows Au–Al intermetallic growth [inference; verify by cross-section on W3].
- **Note:** the seed shorts every electrode and both SNSPD pads together. That is ESD-safe, but no electrical checks are possible until step 15.
- **Note:** the seed coats the window floor (SiO₂); it is removed in step 15.
- [ ] Done — date: ____ operator: ____ notes: ____

## 13. L50 plating mold (negative, ≥ 8 µm)

- **Tool:** MLA150.
- **Recipe:**
  - AZ nLOF 2070 at ≥ 8 µm (PTB thesis used nLOF 2070; spin curve [verify]). Mold ≥ 1.3 × the plating thickness [inference].
  - MLA expose L50 **inverted** (resist stays where there is no Au). PEB and develop per datasheet.
  - Short O₂ descum.
  - Leave the cathode contact points at the wafer edge free of resist.
- **Layer / align:** L50 → **L40 topography crosses** seen through the seed (±1 µm, critical).
- **Inspect:**
  - Window opening registered to the meander.
  - 5 µm gap lines clean down to the seed.
  - nLOF profile (re-entrant): record the gap width at the bottom.
- [ ] Done — date: ____ operator: ____ t_resist: ____ overlay (µm): ____ notes: ____

## 14. Au electroplating, 6 µm

- **Tool:** Plating-U04. **Whether it is a gold tank, and its chemistry, are not verified.** PTB used a sulfite bath (Enthone Microfab Au 100-B, pH 7.5, compatible with nLOF).
- **Recipe:**
  - Plated area ≈ 0.92 cm² per 10 × 10 mm trap die (Au fraction 0.916) and ≈ 0.17 cm² per test die (0.69 with T8; 0.21 cm² for the trap-only test die), so ≈ 5.9 cm² for `run_R1_TRAP` and ≈ 5.8 cm² for `run_R1_FULL` (8 dies each) [team calc from GDS]. Such a small plated area on a 100 mm wafer needs a low, well-calibrated current; confirm the tank's minimum on W5 with the same run layout [verify].
  - Current density per bath datasheet [verify]. At 3 mA/cm² and 100 % efficiency, Au(I) deposits ~0.19 µm/min, so ~32 min for 6 µm [team calc, Faraday].
  - Plate in two halves and measure in between.
- **Target:** 6.0 ± 0.5 µm (DESIGN_LOG step 2); ≤ 10 % across the wafer [verify]; no nodules.
- [ ] Done — date: ____ operator: ____ I / t: ____ thickness map: ____ notes: ____

## 15. Strip, descum, seed removal

- **Recipe:**
  1. Strip nLOF in hot NMP / Remover PG. Then O₂ plasma + F plasma for resist debris (PTB).
  2. **Ar ion etch of the Au seed** at ~50 nm/min (PTB): ~1 min + ~20 % over [verify that Clean-Ar-Plasma, or an Ar RIE recipe, actually mills].
  3. **F-plasma etch of the Ti** at ~10 nm/min (PTB): ~1.5 min + over.
- **Exposure notes:**
  - The bare SiO₂ window floor sees the F plasma and the end of the Ar etch; expect a few nm of SiO₂ loss there [inference].
  - The SNSPD L22 pads lose a few nm of Au.
  - Line-of-sight redeposition is unavoidable (Sussex).
- **Inspect:**
  - All electrodes isolated (neighbours > 100 MΩ at 10 V).
  - Meander R₂.
  - Window floor optically clean (no Au film).
  - AFM: Au roughness ~8 nm rms (PTB 8.3(5) nm).
- [ ] Done — date: ____ operator: ____ Ar time: ____ F time: ____ R₂: ____ notes: ____

## 16a. Protect resist L45

- Thick positive resist ≥ 10 µm over the 6 µm topography. MLA expose **inverted** (resist stays on the L45 patches), aligned to L40/L50 (±2 µm).
- Covers, on trap dies: the four M1 openings + 10 µm; the SNSPD-lead branch region at the left end (x = −4835 … −4430, \|y\| ≤ 330: SNSPD pads, their D2 openings, and where the L22 leads leave the centre-DC lead); the readout window + 2.5 µm (onto the 5 µm Au rim).
- On test dies: every D2 opening + 10 µm; the T3, T4, T4b, T8 and T9 boxes in the current test-die layout. T1, T2 and T6 are left open on purpose so they see the gap etch.
- **The window patch must not be dropped in v3.** With no ITO, the window is a hole in the Au etch mask, and the gap etch would go down through the 10 µm SiO₂ toward the NbN.
- [ ] Done — date: ____ operator: ____ notes: ____

## 16. Au-masked D2 gap etch

- **Purpose:** remove D2 from the electrode gaps so the ion does not see oxide; aspect ratio > 1 (Bautista-Salvador 2019).
- **Recipe:**
  - Same CHF₃/CF₄/Ar recipe as step 11.
  - Etch ~9.6 µm, stopping **~0.75 µm above M1** (Sussex: 750(250) nm, 4(1) % uniformity), so ~27 min at 360 nm/min [verify on W3].
  - Etch in segments; check depth on the T1 comb gaps (test dies) by Dektak / optical interferometry.
- **Exposure notes:**
  - The window is protected only by the 16a resist patch (no ITO in v3).
  - The L22 leads cross a 10 µm Au gap in two spots, where they leave the centre-DC lead at x ≈ −4455, \|y\| ≈ 20–30. Both spots are inside the L45 branch patch. Checked with gdstk: the only L22 not covered by Au, L40 or L45 are the EBL crosses and overlay squares at the mark sites, which are no longer needed. **If 16a is skipped**, the lead top at those spots is ~0.6 µm above M1, with ~0.15 µm of oxide left over it or none [team calc]; then stop at ≥ 0.9 µm.
- **Optional BOE undercut: NOT in run 1.**
  - BOE attacks Al and the Ti adhesion layer under the Au (W6).
  - Near the readout the SNSPD leads are only **1.5–1.7 µm inside the centre-DC Au edge** [GDS check]. A Sussex-style 3 µm undercut would reach them.
  - If it is ever used: dice first (JoVE), keep all windows and pads under resist, and keep the undercut < 1 µm.
- **Inspect:**
  - SEM on a sacrificial die or W3: gap cleared to target; no Au redeposition bridges on the sidewalls.
  - Strip the 16a resist (solvent + O₂ ash; NbN is buried).
  - Meander R₃.
- [ ] Done — date: ____ operator: ____ etch time: ____ depth: ____ R₃: ____ notes: ____

Continue: [next stage](04_PACKAGING.md).
