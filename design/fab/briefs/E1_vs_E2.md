> **Claude-authored.** Decision brief: electrode Au, E1 (0.35 µm lift-off) against E2 (6 µm plated). Numbers and sources only; the choice is the team's. 2026-11-10.

# Electrode Au: 0.35 µm lift-off (E1) or 6 µm plated (E2)?

[Open decisions](../OPEN_DECISIONS.md) · [Glossary](../../GLOSSARY.md) · [Team decision log](../../../notes/decisions.md)

**Status:** Open. Not a team decision yet. [OPEN_DECISIONS](../OPEN_DECISIONS.md), "Electrode Au (v4)", reads: "**Open.** No longer blocks the fab pages: both branches are written out (step 36)".

## The options

| Option | What it is, in one line |
| --- | --- |
| E1 | Au 0.35 µm, Ti 10 nm under it, evaporated and lifted off (branch E1 of [03_ELECTRODES](../process/03_ELECTRODES.md)) |
| E2 | Au 6 µm, plated on a Ti 15 nm / Au 50 nm seed; the seed is removed in step 15 (branch E2 of [03_ELECTRODES](../process/03_ELECTRODES.md)) |

Both branches share steps 9 to 11 ([03_ELECTRODES](../process/03_ELECTRODES.md), table "E1 vs E2 at a glance").

## What is already fixed

- 2026-11-08 · Architecture: local mirror, no 10 µm D2 ([decisions](../../../notes/decisions.md)). The entry reads: "Electrode Au thickness (E1 0.35 µm lift-off vs E2 6 µm plated) is still open."
- 2026-11-08 · Local-mirror lead routing: slot along the centre DC ([decisions](../../../notes/decisions.md)). The entry makes the SNSPD leads "in the electrode Au, in the same step as the electrodes". Both options therefore carry the leads.
- 2026-11-02 · Process: ground-plane flow, plated Au electrodes ([decisions](../../../notes/decisions.md)). Status in the entry: superseded 2026-11-08 by the local-mirror architecture. Its plated-Au choice is not the current electrode decision.
- 2026-11-09 · Keep the 50 µm ion height ([decisions](../../../notes/decisions.md)). The push in [sim 13](../../sim/13_dc_height_tuning.py) is computed from this height.
- 2026-11-12 · One wafer for all four chips (run `R1_ONE`). The electrode choice is wafer-wide: E1 and E2 cannot both be built on one wafer ([decisions](../../../notes/decisions.md)). The Al mirror is raised, 100 nm, so the electrode Au crosses its 100 nm step on both branches.

## Numbers side by side

| Quantity | E1 (0.35 µm) | E2 (6 µm) | Source |
| --- | --- | --- | --- |
| Au thickness | 0.35 µm | 6 µm | [OPEN_DECISIONS](../OPEN_DECISIONS.md), "Electrode Au (v4)"; [03_ELECTRODES](../process/03_ELECTRODES.md), "E1 vs E2 at a glance" |
| Scope of the choice | The whole shared wafer of run `R1_ONE`: every die gets the same electrode step | Same | [decisions](../../../notes/decisions.md), 2026-11-12 |
| Sheet resistance, room temperature, bulk ρ 2.44 µΩ·cm | 0.0697 Ω/sq | 0.0041 Ω/sq | [sim 18](../../sim/out/18_e1_vs_e2/compare.md), row "Rs, room temperature, bulk rho" (ρ [verify]) |
| Resistance of one SNSPD slot lead, room temperature, bulk ρ | 69.33 Ω | 4.04 Ω | [sim 18](../../sim/out/18_e1_vs_e2/compare.md), row "one lead R, room temperature, bulk rho" (drawn path, 994.5 sq on E2 squares) |
| Chip RF capacitance, A30, Si lossless (cold case) | 2.395 pF | 2.590 pF | [sim 22](../../sim/out/22_rf_capacitance/summary.json), `configs.A30_E1.chip.C_chip_pF`, `configs.A30_E2.chip.C_chip_pF`. With Si as a grounded conductor (not the cold case): 22.41 pF and 22.63 pF, `C_chip_groundSi_pF` |
| RF current into the chip, 53 V, 28 MHz | 22.33 mA | 24.15 mA | [sim 22](../../sim/out/22_rf_capacitance/summary.json), `heating.A30_E1.bulk_RRR2.I_mA`, `heating.A30_E2.bulk_RRR2.I_mA` (ωCV; the same for every RRR) |
| RF heating bound at the computed capacitance, bulk ρ, RRR 2 [verify] | 0.451 mW | 0.0308 mW | [sim 22](../../sim/out/22_rf_capacitance/summary.json), `heating.A30_E1.bulk_RRR2.P18_mW`, `heating.A30_E2.bulk_RRR2.P18_mW`; upper bound, sim 18 formula |
| RF heating bound, film ρ, RRR 2 [verify] | 0.740 mW | 0.0505 mW | [sim 22](../../sim/out/22_rf_capacitance/summary.json), `heating.*.film_RRR2.P18_mW` |
| Direct nanowire pickup, RF (2-D) | 1.92 µA | 0.96 µA | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), case `al100_cap110` (the decided stack), `E1.window.I_pk_uA`, `E2.window.I_pk_uA` (inlaid stack: 1.915 / 0.959 µA) |
| Common-mode RF current per slot lead, direct | 28.4 µA | 44.5 µA | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), case `al100_cap110` (the decided stack), `E1.slot.I_lead_in_trap_uA`, `E2.slot.I_lead_in_trap_uA` (inlaid stack: 28.61 / 44.53 µA) |
| Nanowire current, A30, plain 50 Ω line (return grounded), R pair 0 | 2.58 µA | 4.06 µA | [sim 19](../../sim/out/19_lead_termination/summary.json), case "1 50 ohm line / short", `I_nw_uA` |
| Geometric collection, A30 | 2.636 % | 2.221 % | [sim 15b](../../sim/out/15b_collection_v4/summary.json), `cases.A30_E1_null+drop.collection_pct`, `cases.A30_E2_null+drop.collection_pct` |
| Geometric collection, B60 | 4.760 % | 4.158 % | [sim 15b](../../sim/out/15b_collection_v4/summary.json), `cases.B60_E1_null+drop.collection_pct`, `cases.B60_E2_null+drop.collection_pct` |
| Absorbed fraction of all emitted photons, A30, 160 nm cap | 1.743 % | 1.470 % | [sim 15b](../../sim/out/15b_collection_v4/summary.json), `cases.A30_*_null+drop.caps.160.absorbed_of_emitted_pct` |
| Absorbed fraction of all emitted photons, B60, 160 nm cap | 3.082 % | 2.709 % | [sim 15b](../../sim/out/15b_collection_v4/summary.json), `cases.B60_*_null+drop.caps.160.absorbed_of_emitted_pct` |
| Null drop over the A30 window | ≤ 0.37 µm (upper bound) | 1.19 µm | [sim 12 E1](../../sim/out/12_final_chip/trap_die_v4_A30_E1/summary.json), `readout.dh_recess` = −0.368; [sim 12 E2](../../sim/out/12_final_chip/trap_die_v4_A30/summary.json), `readout.dh_recess` = −1.188. The E1 bound is from [DESIGN_LOG step 25](../../DESIGN_LOG.md) |
| Micromotion after DC height correction, A30, 10° tilt | 54.88 nm | 173.36 nm | [sim 13](../../sim/out/13_dc_height_tuning_v4/summary.json), `A30_E1.tilt_10deg.at_needed_shift.a_mm_nm`, `A30_E2.tilt_10deg.at_needed_shift.a_mm_nm` |
| Null sideways shift for a 2 µm mirror misalignment, raised 100 nm | 529 nm | 45 nm | [sim 10d](../../sim/out/10d_mirror_step/summary.json), `cases["E1|s=0.10|d=2.0"].dx_nm`, `cases["E2|s=0.10|d=2.0"].dx_nm` (inlaid, for the record: 496 nm / 14.8 nm, `s=0.00`) |
| Screening of charge on the SiO₂ gap floor, exp(−π t / g), g = 5 µm [inference] | 0.803 | 0.0230 | [sim 18](../../sim/out/18_e1_vs_e2/compare.md), row "exp(-pi t/g), g = 5 um"; lowest-mode estimate, not a field solve |
| Zone voltages: readout max \|V\|, A30 / loading max \|V\| | 6.28 V / 7.45 V | 6.29 V / 7.45 V | [sim 12 E1](../../sim/out/12_final_chip/trap_die_v4_A30_E1/summary.json), `readout.vmax`, `loading.vmax`; [sim 12 E2](../../sim/out/12_final_chip/trap_die_v4_A30/summary.json) (same keys) |
| Transport max \|V\| / max step change, 10 µm steps | 7.265 V / 7.591 V | 7.264 V / 7.590 V | [sim 12 E1](../../sim/out/12_final_chip/trap_die_v4_A30_E1/summary.json) and [sim 12 E2](../../sim/out/12_final_chip/trap_die_v4_A30/summary.json), `transport.max_abs_V`, `transport.max_step_change_V` |

The zone and transport voltages are equal to 0.01 V at the precision shown, as [DESIGN_LOG step 31](../../DESIGN_LOG.md) states. Both values are given above. The transport block in each sim 12 summary does not name its centre-DC setting [verify]. The sim 22 chip totals are 2-D, with ideal conductors, end effects neglected, B60 taken equal to A30 [inference], and Si lossless, as sim 10b treats it at 5 K. The sim 18 resistances use bulk ρ, with RRR 2 to 10 at 4 K, all [verify].

## What each option changes elsewhere

- Both branches share the contact layer, Ti 5 nm / Au 50 nm on layer 22 (final stack, decided 2026-11-12), which is separate from the electrode Au. Both branches also share the 100 nm raised Al mirror, so the electrode Au crosses its edge step on both. Whether that crossing holds on each branch is a check ([verify]), not a difference between them.
- Fab steps 12 to 15 are written twice, one branch per option ([03_ELECTRODES](../process/03_ELECTRODES.md), headings "E1" and "E2"). Step 13 on E1 is a Ti 10 nm / Au 350 nm evaporation; step 13 on E2 is the plating mold (≥ 8 µm); step 14 on E2 is the 6 µm plating.
- Layer 50 resist: LOR plus positive resist on E1 ([03_ELECTRODES](../process/03_ELECTRODES.md), E1 step 12); AZ nLOF 2070, ≥ 8 µm, on E2 (E2 step 13).
- Tools named in the branches: E1 uses the EBeam-Temescal-FC2800 evaporator and NMP lift-off, both [verify]; E2 uses the plating tool Plating-U04, [chemistry unverified] ([03_ELECTRODES](../process/03_ELECTRODES.md), table "E1 vs E2 at a glance").
- Qualification: W5 plating calibration applies to E2 only ([QUALIFICATION](../QUALIFICATION.md), W5). The E1 lift-off loop applies to E1 only ([QUALIFICATION](../QUALIFICATION.md), "E1 lift-off loop").
- Bonding: [04_PACKAGING](../process/04_PACKAGING.md) gives a wire-bond-grade figure of ≤ 90 Knoop for plated Au [verify] for E2, and marks wedge bonding onto 0.35 µm evaporated Au as [verify] for E1.
- Simulation files: the `_E1` suffix marks the E1 layouts, for example `trap_die_v4_A30_E1_sim.json`; unsuffixed files are E2 ([glossary](../../GLOSSARY.md)).

## Not known

- Resistivity of either Au film at 4 K. No measured value was found for 0.35 µm evaporated or 6 µm plated Au; the RRR is a bracket of 2 to 10 [verify] ([DESIGN_LOG step 31](../../DESIGN_LOG.md), literature note).
- Charge build-up on the SiO₂ gap floor against metal thickness. No source quantifying a stray field from a charged trench floor was found ([DESIGN_LOG step 31](../../DESIGN_LOG.md)). The screening row is an estimate, tagged [inference].
- Wedge bonding onto 350 nm evaporated Au [verify], and the hardness of the plated Au on E2 (vendor figure, [verify]).
- Plating tank minimum area against the 8.27 cm² of Au on run R1_ONE ([OPEN_DECISIONS](../OPEN_DECISIONS.md), "Before R1_ONE"), and step coverage over the 348 nm of SiO₂ at the mirror ground via for both branches ([03_ELECTRODES](../process/03_ELECTRODES.md)).
- Chip RF capacitance with the package and the pads: sim 22 gives the chip alone [inference]. Other capacitances in the literature are cited in [sim 22](../../sim/out/22_rf_capacitance/table.md) per row and are not computed here.
- Todaro 2021 used 6 µm electroplated Au; the bench-test note marks this [verify] ([T2 note](../../research/research_notes/Test%20setup%202026-11/T2_snspd_bench_tests.md), Todaro table, row 1). Hampel 2023 used one 350 nm evaporated Au layer for electrodes and leads; the same note records it as read from the PDF, pages 2–3.

## What would settle it

- A witness measurement of Au sheet resistance and RRR at 4 K on an E1 evaporated film and an E2 plated film ([OPEN_DECISIONS](../OPEN_DECISIONS.md), "Measure the Au film resistivity at 4 K").
- The W5 plating calibration on E2 and the E1 lift-off loop, with the W7 bond-and-leak test for both ([QUALIFICATION](../QUALIFICATION.md)).
- The RF-off and RF-on switching-current test on a cold die, and a nanowire current measurement with the planned lead termination ([sim 19](../../sim/out/19_lead_termination/summary.json)).
- Micromotion at readout, against the predicted 173 nm (E2) and 55 nm (E1) for A30 ([04_TRAPPING](../tests/04_TRAPPING.md), step 9).

## Where to read

- [DESIGN_LOG step 31](../../DESIGN_LOG.md) (line 1341): the functional comparison table and the four differences it names.
- [DESIGN_LOG step 32](../../DESIGN_LOG.md) (line 1375): collection and absorption on v4.
- [DESIGN_LOG step 33](../../DESIGN_LOG.md) (line 1392): the lead termination numbers.
- [DESIGN_LOG step 25](../../DESIGN_LOG.md) (line 1082): the E1 null-drop upper bound.
- [sim 18 script](../../sim/18_e1_vs_e2.py): the resistance, skin depth and screening formulas.
- [sim 22 script](../../sim/22_rf_capacitance.py): the chip capacitance and the resonator table.
- [03_ELECTRODES](../process/03_ELECTRODES.md): the two branches and the table "E1 vs E2 at a glance".
