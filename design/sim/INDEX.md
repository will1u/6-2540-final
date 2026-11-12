> **Claude-authored.** Index of the simulation scripts in `design/sim/`: what each asked, its headline number, whether it still applies, and which decision or page it fed, 2026-11-10.

Numbers 07 and 08 were never used: no script, output or commit exists for either.

1. **How to use this folder**
   - Run a script with `cd design/sim && ./run.sh <script>.py`. For the one-time `electrode` environment setup, see [design/CLAUDE.md](../CLAUDE.md) ("Setting up the electrode repo").
   - Sim 24 uses the separate `rcwa` conda env, not `electrode`; the setup is in its docstring (`24_rcwa_meander.py`).
   - Outputs go to `design/sim/out/<script stem>/`, each with a `summary.json`. A few scripts also write named extra files (for example `summary_wx30.json`).
   - Version tags: v1 = square die; v2 = narrow 10 × 2.5 mm die with indium tin oxide (ITO) in the window; v3 = die-wide Al plane under 10 µm SiO₂.
   - v3.1 = new NbN meander on v3 (step 24). v4 = local Al mirror under the SNSPD only, the current architecture.
   - Headline numbers below come from each `summary.json` (key path given). Where a folder has several summaries, the current-version one is used.

2. **Main table**

| Script | Question it asks | Headline result (summary.json key) | Applies to | DESIGN_LOG step | Fed which decision or page | Output folder |
|---|---|---|---|---|---|---|
| `01_analytic_fivewire.py` | Height vs collection vs heating, and a width sweep of the five-wire trap at h = 50 µm (analytic model) | `max_depth_design.depth_meV` = 73.38 meV (c = 20 µm design point; `c60_design.depth_meV` = 43.33 meV) | any version (analytic) | 1 | Inputs of the 50 µm height and 53 V RF used in later sims ([design/CLAUDE.md](../CLAUDE.md), key design numbers) | `out/01_analytic_fivewire/` |
| `02_baseline_gds2itvg.py` | Does the gds2itvg model of the baseline trap (no window) match the analytic model? | `profile.null_z` = 50.095 µm (device-stack profile; `midline.null_z` = 50.055 µm) | any version (baseline check; older 16-segment geometry) | 2 | Check that the solver is trusted before 03 to 05 | `out/02_baseline/` |
| `03_segment_pitch.py` | Which outer DC segment pitch gives control at h = 50 µm? | List of 5 rows, one per pitch. The 100 µm row: `[2].vmax_confine_1MHz` = 11.287 V, `[2].vmax_tilt_10deg` = 1.708 V | any version, but the pitch it chose (100 µm) became 120 µm in step 28 | 3 | Segment pitch, now 120 µm (step 28) | `out/03_segment_pitch/` |
| `04_window_validation.py` | Are the planar window results (05) right? 2-D finite-difference check | `full.null_z` = 47.783 µm (no window, 2-D model) | v2-era validation | 6 | Check on 05 (window inside the centre DC rule, step 6) | `out/04_validation/` |
| `04b_window_3d_fd.py` | How much does a finite window pocket lower the RF null? 3-D finite-difference check | `summary_mirror_t6.json`, `"30x30 mirror_t6".dh[0]` = −1.1877 µm (ion height change over the window centre; `mirror_t6` = 6 µm Au over the grounded Al mirror) | `mirror_t6` and `mirror_t1` cases: v4 (current); `mirror_t6` = 6 µm Au, `mirror_t1` = 1 µm Au, the upper bound for E1 (0.35 µm is below the 1 µm grid). Other cases, all v2/v3: `ito6` = window with the SiO₂ left in place and ITO on it at the floor, tied to the RF ground (`summary_ito6.json`, v2); `oxide` = window with the SiO₂ left in place and no ITO, so the floor is bare SiO₂ with a grounded plane 10 µm below (`summary_oxide.json`, v3); base `summary.json` = the no-window reference plus `etched` pockets (SiO₂ removed down to the grounded floor) | 6 (cases); 17, 25, 26 (v4) | Window drop used by 12 and 13; the 16 pad check. The v4 E2 value agrees with `13_dc_height_tuning_v4` (see row 13) | `out/04b_window_3d/` |
| `05_window_variants.py` | What does a missing patch of electrode metal (the window) do to the trap? | `summary_wx30.json`, `results["V1_wy30\|profile"].dc_vmax` = 0.860 V vs `results["V0\|profile"].dc_vmax` = 7.221 V (no window) | v2 only | 6 | Rule to keep the window inside the centre DC electrode ([design/CLAUDE.md](../CLAUDE.md), physics decisions; step 6) | `out/05_window/` |
| `06_detector_size.py` | Collection vs window size vs nanowire length | List of 4 rows keyed by window; `[0].collection_pct` = 0.9838 % (20 × 20 µm window) | v3 only | 7 | Window sizes A30 and B60 (steps 7 and 24) | `out/06_detector_size/` |
| `09_optical_stack_tmm.py` | NbN absorption at 493 nm with the ITO-stack transfer matrix | `etched_window.nominal_best.A_nominal` = 0.6306 (etched window, ITO 65 nm) | v2 only (ITO stack) | 9 | Input to 09b; the ITO retirement (step 17) | `out/09_optical_stack_tmm/` |
| `09b_itoD2_matching.py` | Can the ITO-on-D2 window (ITO on 10 µm SiO₂) get its absorption back with a buried matching layer? | `ITO.A` = 0.5315 (with buried matching ITO); `none.A` = 0.3968 (no matching layer) | v3 only, superseded by 09c | 9b | ITO retirement (step 17); superseded by 09c for v4 | `out/09b_itoD2_matching/` |
| `09c_localmirror_optics.py` | NbN absorption at 493 nm for the v4 local-mirror stack | `v4_current_238_80.A` = 0.4404 (current spacer 238 nm, cap 80 nm); `v4_best_cap_spacer238.A` = 0.6620 (cap 159 nm) | v4 (current) | 26 | Absorption 0.66 with a 160 nm cap ([design/CLAUDE.md](../CLAUDE.md), key design numbers) | `out/09c_localmirror_optics/` |
| `10_rf_pickup_2d.py` | RF pickup current in the NbN meander (2-D electrostatics) | `v3_f_noito_stack.I_pk_uA` = 1.417 µA (v3 stack with no ITO; the older cases a to f are under `cases`) | v2/v3 stack; it writes `summary_v31_scan.json`, which 10b reads | 10, 17 | Floating ITO raised pickup 9×, hence the "ground or tie every ITO" rule ([design/CLAUDE.md](../CLAUDE.md)) | `out/10_rf_pickup_2d/` |
| `10b_rf_pickup_v4.py` | RF pickup for the v4 local-mirror die | `E2_window.I_pk_uA` = 0.9615 µA (E2 window cut, 80 nm cap, 150 nm Al) | v4, older stack numbers (80 nm SiO₂ cap, 150 nm Al); superseded for numbers by 10c | 26 (and 28) | RF pickup bound quoted in [design/CLAUDE.md](../CLAUDE.md) | `out/10b_rf_pickup_v4/` |
| `10c_mirror_thickness.py` | Al mirror thickness; for the final stack, the slot cross-section with a raised 100 nm Al mirror under a 110 nm cap (case `al100_cap110`), and the direct nanowire pickup (case `al100`) | Case `al100_cap110`: `al100_cap110.E2.slot.I_lead_in_trap_uA` = 44.53 µA (common-mode per slot lead, E2); E1 28.4 µA (same case). Direct pickup, case `al100`: `al100.E2.window.I_pk_uA` = 0.96 µA (E2), `al100.E1.window.I_pk_uA` = 1.92 µA (E1). Quote `al100_cap110` for the mirror and the leads; `al100` for the direct pickup. Do not quote `al100_inlaid` as current | v4 (current). `al100_cap110` (2026-11-12): the slot cross-section of the final stack, raised 100 nm Al with 110 nm of SiO₂ over it under the leads. `al100` (2026-11-12): raised 100 nm Al with 160 nm over the wires | 37, 38, 45 | Final stack, raised mirror (team decision 2026-11-12, [notes/decisions.md](../../notes/decisions.md)). Superseded: the inlaid mirror of 2026-11-09 | `out/10c_mirror_thickness/` |
| `10d_mirror_step.py` | RF null shift from a raised step or a sideways misalignment of the mirror | `cases["E1\|s=0.00\|d=2.0"].dx_nm` = 495.95 nm (2 µm sideways misalignment, E1) | v4 (current) | 39 Raised 100 nm mirror chosen 2026-11-12 (step 39: it lifts the null by 0.13 to 0.16 µm). Open item on the mirror edge ([fab/OPEN_DECISIONS.md](../fab/OPEN_DECISIONS.md)) | `out/10d_mirror_step/` |
| `11_beam_clearance.py` | Laser beam clearance over the chip surface at h = 50 µm | `493 nm (cool/detect).full_chip_10mm` = 0.01689 (about 1.7e-2 of the beam clips the surface) | any version (die-level) | 4 | Beam clearance on the 10 × 10 mm die ([design/CLAUDE.md](../CLAUDE.md), key design numbers) | `out/11_beam_clearance/` |
| `12_final_chip_check.py` | Final check of the fabrication GDS (layer 50) by gds2itvg: null, DC solves, transport | `trap_die_v4_A30/summary.json`: `readout.null_z` = 49.977 µm; `transport.max_abs_V` = 7.264 V | v4 (current) for `trap_die_v4_*`. `trap_die_v2_*` and `trap_die_v3_*` folders are older | 11, 13, 19, 25, 28, 29 | Required re-run when layer 50 changes ([design/CLAUDE.md](../CLAUDE.md)); transport with the centre DC at 0 V (step 25) | `out/12_final_chip/` |
| `13_dc_height_tuning.py` | Can the DC electrodes put the ion back at 50 µm over the window? | `13_dc_height_tuning_v4/summary.json`: `A30_E2.window_drop_um` = −1.1877 µm | v4 (current) in `13_dc_height_tuning_v4`; `13_dc_height_tuning` is v3 only (`A30.window_drop_um` = −1.3810 µm) | 19 (v3); 25, 27, 28 (v4) | Read by 15b (row 15b) and used in the v4 die checks | `out/13_dc_height_tuning_v4/` (v3: `out/13_dc_height_tuning/`) |
| `14_staircase_check.py` | Do the staircase fingers and lead tracks change the DC electrodes? | `S_vs_U_profile_max_relative` = 0.1012 (real die vs uniform segments); `FW.null_z` = 67.192 µm (reference five-wire) | v3 only (by design; it reads the v3 folders) | 20 | Step 20 check of staircase fingers; no v4 rerun | `out/14_staircase_check/` |
| `15_snspd_geometry.py` | SNSPD geometry budget: collection, refraction footprint, absorption, turn crowding | `collection_pct.A30.iso` = 2.2280 % (v3 A30, isotropic emitter) | v3 only, superseded by 15b for collection | 24 | Basis of the v3.1 meander (step 24) | `out/15_snspd_geometry/` |
| `15b_collection_v4.py` | SNSPD collection and NbN absorption on the v4 stack | `cases["A30_E2_null+drop"].collection_pct` = 2.2213 % | v4 (current) | 32 (and the 2026-11-08 overhang audit) | Collection numbers in [design/CLAUDE.md](../CLAUDE.md), key design numbers | `out/15b_collection_v4/` |
| `16_pad_pitch_check.py` | Compares the current pad layout with the preserved 180 µm pad baseline | No `summary.json`. Outputs: `out/16_pad_pitch_check/comparison.json` and `checks_manifest.json`; no headline number taken. Its `--resume` option refuses to run: the die files were regenerated after step 29 (step 35, the 160 nm cap in the metadata), so the stored input hashes no longer match; a full rerun would refresh them | v4 (current) | 29 | Pad pitch adoption is an open item ([design/CLAUDE.md](../CLAUDE.md), current state) | `out/16_pad_pitch_check/` |
| `17_height_tradeoff.py` | Is 50 µm the right ion height, or should the trap be lower? | `reference.depth_meV` = 51.912 meV (h = 50 µm, c = 40 µm); tables A, B and C compare heights | v4 (current) | 30 | Team decision 2026-11-09: keep the 50 µm ion height ([notes/decisions.md](../../notes/decisions.md)) | `out/17_height_tradeoff/` |
| `18_e1_vs_e2.py` | E1 (0.35 µm lift-off Au) vs E2 (6 µm plated Au): one comparison table | `checks[0]`: "Rs(E1)/Rs(E2) = 17.14" (pass: true) | v4 (current) | 31 | Electrode Au choice E1 vs E2 is still open ([design/CLAUDE.md](../CLAUDE.md), open items) | `out/18_e1_vs_e2/` (`compare.md`, `summary.json`) |
| `19_lead_termination.py` | RF current through the SNSPD nanowire for several lead terminations | `summary.json` rows keyed by case and die: "1 50 ohm line / short", A30, E2: `I_nw_uA` = 4.0575 µA (list of 288 rows). The E1 input 28.3 µA (line 37) is the 10b value; 10c gives 28.6 µA | v4 (current) | 33 | Lead termination is an open item ([design/CLAUDE.md](../CLAUDE.md), open items) | `out/19_lead_termination/` |
| `20_transport_timing.py` | Classical axial heating of a 138Ba⁺ ion shuttled 480 µm | `part3_max_step_V` = 1.70836 V (largest step in the 10 µm transport waveform); `part3_max_abs_V` = 6.63909 V | v4 (current); reads `trap_die_v4_A30_V2zero/waveforms.csv` | 34 | The 10 µm table is not yet a playable waveform (open item, step 34) | `out/20_transport_timing/` |
| `21_transport_waveform.py` | Can the 10 µm static table of sim 12 become a voltage-versus-time waveform a DAC could play, and what motional energy does the move leave (classical)? | `checkA.max_abs_diff_V` = 4.99e-6 V (5.0 µV, largest difference from the sim 12 table, A30); `checkB.max_abs_dy_nm` = 0.0067 nm (interpolation position error at the midpoints, A30) | v4 (current) | 40 | Transport items in [fab/OPEN_DECISIONS.md](../fab/OPEN_DECISIONS.md); [readout tilt brief](../fab/briefs/readout_tilt.md) | `out/21_transport_waveform/<die>/` (A30, B60, NODET) |
| `22_rf_capacitance.py` | What RF capacitance does the chip have to ground, what loss does its dielectric allow, and what does that do to a resonator? | `configs.A30_E2.chip.C_chip_pF` = 2.590 pF (A30, E2); `configs.A30_E1.chip.C_chip_pF` = 2.395 pF (A30, E1) | v4 (current) | 41 | [E1 vs E2 brief](../fab/briefs/E1_vs_E2.md); [RF primer](../primers/RF_PRIMER.md); electrical test a10 ([process checks](../fab/process_checks.md)) | `out/22_rf_capacitance/` (`summary.json`, `table.md`, `sections.png`) |
| `22b_base_sio2_sweep.py` | How does the chip RF capacitance depend on the base SiO₂ thickness (0.15 to 2.0 µm), for the final stack? | Cold (Si lossless), case `E2`, base 0.15 to 2.0 µm: `cases[].C_chip_pF` from 2.878 to 2.383 pF (E2); the Si as a grounded conductor (room-temperature limit): `cases[].C_chip_groundSi_pF` from 57.5 to 13.6 pF. Table in `table.md`. Acceptance: `acceptance.E2.C_chip_pF` = 2.590 pF, `acceptance.E1.C_chip_pF` = 2.395 pF (the 1.0 µm base reproduces sim 22) | v4 final stack (2026-11-12); 2-D; imports sim 22 | 45 | Base SiO₂ thickness of the final stack (1.0 µm nominal; accept 0.5–2.0 µm as supplied); the pages keep 2.59 pF (E2) / 2.39 pF (E1) from sim 22 | `out/22b_base_sio2_sweep/` (`summary.json`, `table.md`, `sweep.png`) |
| `23_dc_rf_coupling.py` | How much of the 53 V RF on the rails couples onto each DC electrode, and what a filter capacitor does to that voltage and to the RF null? | `per_electrode.E2.centre_A30.C_c_pF` = 0.414 pF (centre DC to rails); `divider[2].V_el_V` = 0.02188 V (RF left on the A30 centre DC with 1 nF to ground, E2; `divider[2].C_f_pF` = 1000) | v4 (current) | 42 | [RF grounding and termination brief](../fab/briefs/rf_grounding_and_termination.md) (RF grounding and filters decision) | `out/23_dc_rf_coupling/` (`summary.json`, `table.md`) |
| `24_rcwa_meander.py` | How much 493 nm light does the NbN meander absorb, by rigorous RCWA, compared with the effective-medium value? (160 nm cap, unpolarised) | `table` row with `cap` = 160.0 and `polarisation` = "unpol": `rcwa` = 0.827 (RCWA); `emt` = 0.662 (effective medium, the value still quoted) | v4 (current) | 43 | Absorption key number (the effective-medium value is still quoted; see step 43) | `out/24_rcwa_meander/` (`summary.json`, `table.md`); run in the `rcwa` env (see the script docstring) |
| `24b_rcwa_stack_scan.py` | Are the 238 nm spacer and the 160 nm of SiO₂ over the wires at the RCWA optimum, with tolerance, NbN thickness, SiO₂ index and an optional ITO layer? | `table.md`: 0.828 at spacer 238 nm / 160 nm of SiO₂ over the wires; ±10 nm box mean 0.803, worst corner 0.753; best worst corner on the grid 0.764 at 240 / 160 nm. NbN 6 / 7 / 8 nm: 0.779 / 0.828 / 0.865. With 20 nm (50 nm) of ITO on top: 0.682 (0.417) at 160 nm, best 0.869 at 120 nm (0.909 at 90 nm) | v4 final stack (2026-11-12); RCWA, in the `rcwa` env like sim 24 | 45 | Spacer 238 nm and 160 nm over the wires kept; ITO would have to be chosen before the cap deposition | `out/24b_rcwa_stack_scan/` (`table.md`, not yet written) |

3. **Shared modules**
   - `trapcalc.py`: shared plain-numpy physics helpers: the analytic five-wire model, the pseudopotential and secular frequencies, finite-difference gradients of gds2itvg unit potentials, the DC voltage solve (`solve_dc`) and the geometric collection fraction.
   - `trapgeom.py`: parametric five-wire electrode geometry (`build(P)`); used by sims 02, 03, 04 and 05 only.
   - `run_cached_geometry.py`: runs an unchanged study with repeated Shapely unions cached. Usage: `./run.sh run_cached_geometry.py 12_final_chip_check.py <args>`.
   - `run.sh`: runs a script in the `electrode` conda env, with the DLL path, UTF-8 and Agg settings.
   - `../gds/snspd_geom.py`: NbN meander geometry `meander()` and `straight()`, shared by `make_chip.py` and `make_test_die.py` (step 24).

4. **Outputs read by other scripts (do not move these)**

   Checked by grep on the reading script; the line number is in the reader.

   | Output | Read by | Line |
   |---|---|---|
   | `out/10_rf_pickup_2d/summary_v31_scan.json` | `10b_rf_pickup_v4.py` | 182 |
   | `out/04b_window_3d/summary_<floor>.json` | `12_final_chip_check.py` | 56 |
   | `out/04b_window_3d/summary_<floor>.json` | `13_dc_height_tuning.py` | 62 |
   | `out/04b_window_3d/summary_<floor>.json` | `16_pad_pitch_check.py` | 70 |
   | `out/13_dc_height_tuning_v4/summary.json` | `15b_collection_v4.py` | 29 |
   | `out/12_final_chip/trap_die_v4_A30_V2zero/waveforms.csv` | `20_transport_timing.py` | 30 |
   | `out/12_final_chip/trap_die_v3_{UNIFORM,NODET}/summary.json` | `14_staircase_check.py` | 104 |
   | `gds/archive_v3_baseline/` (v3 `NODET` and `UNIFORM` GDS and `_sim.json`) | `14_staircase_check.py` | 39, 52, 54 |
   | `out/12_final_chip/pad180/` (folders) and `out/12_log_v4_*_pad180.txt` | `16_pad_pitch_check.py` | 21, 50, 58 |
   | `out/12_log_v4_*.txt` (current logs, not `_pad180`) | `16_pad_pitch_check.py` | 55, 88 |
   | `out/22_rf_capacitance/summary.json` | `primers/primer_numbers.py` | 72 |
   | `out/10c_mirror_thickness/summary.json` | `primers/primer_numbers.py` | 62 |
   | `out/18_e1_vs_e2/summary.json` | `primers/primer_numbers.py` | 63 |
   | `out/19_lead_termination/summary.json` | `primers/primer_numbers.py` | 53 |
   | `out/12_final_chip/trap_die_v4_A30_V2zero/waveforms.csv` | `21_transport_waveform.py` | 221 |
   | `out/12_final_chip/trap_die_v4_A30_V2zero/summary.json` | `21_transport_waveform.py` | 234 |
   | `out/12_final_chip/trap_die_v4_{A30,A30_E1,NODET}/summary.json` | `figures/make_report_figures.py` | 41, 42, 43 |
   | `out/12_final_chip/trap_die_v4_A30_V2zero/waveforms.csv` | `figures/make_report_figures.py` | 84 |
   | `out/17_height_tradeoff/summary.json` | `figures/make_report_figures.py` | 129 |
   | `out/19_lead_termination/summary.json` | `figures/make_report_figures.py` | 170 |
   | `out/21_transport_waveform/trap_die_v4_A30_V2zero/waveform.csv` | `figures/make_report_figures.py` | 237 |
   | `out/22_rf_capacitance/summary.json` | `figures/make_report_figures.py` | 291 |

   The `primers/` and `figures/` scripts sit in `design/`, not in `sim/`. Their paths are written relative to the script's own folder, as the reads are coded. Line numbers are from grep on each script.

   `06_detector_size.py` (line 33) and `15_snspd_geometry.py` (line 41) carry the 04b window numbers as constants or comments; they do not read the files.

5. **Older outputs still in place**

   The output folders below were not moved. Folders are not moved in this pass, and some are read by code (see section 4).

   | Folder | Version | Why it is still in place |
   |---|---|---|
   | `out/12_final_chip/trap_die_v2_A30`, `trap_die_v2_B60`, `trap_die_v2_NODET` | v2 | Output folders are not moved. No script reads them by name. |
   | `out/12_final_chip/trap_die_v3_A30`, `_B60`, `_NODET`, `_UNIFORM` | v3 | Sim 14 reads the `_UNIFORM` and `_NODET` summaries (line 104). |
   | `out/12_final_chip/pad180/` | v4, 180 µm pad rows | Sim 16 reads it as its baseline (lines 21, 58). |
   | `out/13_dc_height_tuning/` | v3 | Written by 13 for v3; not read by other code. |
   | `out/13_dc_height_tuning_v4_pad180/` | v4, 180 µm pad rows | The first v4 sim 13 outputs (same files as commit `c997cff`), copied here by commit `d53eb20` before the step 29 rerun on the 360 µm layout. No script writes or reads it. |
   | `out/05_window/` | v2 | Not read by code; the v2 window result. |
   | `out/06_detector_size/` | v3 | Not read by code. |
   | `out/09b_itoD2_matching/` | v3 | Not read by code; the ITO-on-D2 matching result. |
   | `out/15_snspd_geometry/` | v3 | Not read by code; v3 geometry budget (superseded for collection by 15b). |

6. **Not modelled yet**

   Copied from the open items in the source documents. Each item is open in its source.
   - [ ] Ba⁺ angular-emission model: partly resolved (see [fab/OPEN_DECISIONS.md](../fab/OPEN_DECISIONS.md), "Source and model checks").
   - [ ] Suleimen 2026 (Phys. Rev. Applied 25, 044091): only the abstract is open; read the full text before using its width comparison ([fab/OPEN_DECISIONS.md](../fab/OPEN_DECISIONS.md)).
   - [x] RCWA of the meander at normal incidence: done (step 43, [DESIGN_LOG](../DESIGN_LOG.md)). Not done: the average over the ion's emission cone, and FDTD ([fab/OPEN_DECISIONS.md](../fab/OPEN_DECISIONS.md), "Source and model checks").
   - [ ] 3-D pickup on the SNSPD leads: not modelled. Step 42 says why the planned method was not attempted ([DESIGN_LOG](../DESIGN_LOG.md)).
   - [x] Transport: a playable waveform is done (step 40, [DESIGN_LOG](../DESIGN_LOG.md)). The DAC and filter values in it are [verify]; the lab's hardware is not known.
   - [x] Chip RF capacitance: computed (step 41, [DESIGN_LOG](../DESIGN_LOG.md)); the RF heating in step 31 scales with its square.
   - [ ] Not measured: the loss tangent of the SiO₂ films (sets the cold Q of the chip, step 41), and the Au film resistivity at 4 K ([fab/OPEN_DECISIONS.md](../fab/OPEN_DECISIONS.md), "Design choices" and "Before any v4 run").

7. **Other files in `out/`**

   Loose files in `out/` that no table above lists. No code reads them.
   - `16_pad_pitch_check/13_comparison.json` and `16_pad_pitch_check/13_log_pad360.txt`: the sim 13 rerun on the 360 µm pad layout (step 29). No script in the tree writes them; commit `d53eb20` added them. `fab/briefs/pad_pitch.md` links to the JSON.
   - `09c_log.txt` and `10b_log.txt`: console logs of sim 09c and sim 10b (commit `ef35574`).
   - `13_log_v4.txt`: console log of the v4 run of sim 13 (commit `c997cff`).
   - `14_log.txt`: console log of sim 14, its FW and U lines (commit `ca1b6bd`).
   - `04b_mirror_t1_log.txt` and `04b_mirror_t6_log.txt`: console logs of `04b_window_3d_fd.py mirror_t1` and `mirror_t6` (commit `c997cff`).
   - `12_log_v4_*.txt`: listed in section 4 (read by sim 16).