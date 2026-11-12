> **Claude-authored.** Decision brief: pad pitch. Numbers and sources only; the choice is the team's. 2026-11-10.

# Should the pad rows keep the generated 360 µm pitch?

[Open decisions](../OPEN_DECISIONS.md) · [Glossary](../../GLOSSARY.md) · [Team decision log](../../../notes/decisions.md)

**Status:** Team adoption pending. Proposed reason: keep wire angles below 45° for a PGA84L-like package; no additional reason supplied. Not a team decision yet.

## The options

| Option | What it is, in one line |
| --- | --- |
| 360 µm (current) | Centre-to-centre pitch of the outer DC pad rows in the generated layout |
| 180 µm | The earlier pitch; the layout was generated and simulated, then replaced by 360 µm in step 29 |
| 240 µm, 300 µm, 400 µm | Alternatives named in the decision row; no layout or simulation output in the repo |

## What is already fixed

- 2026-11-07 · 10 × 10 mm trap die, trap centred, pads at the die edges ([decisions](../../../notes/decisions.md)). Pads sit on the top and bottom edges and near y = 0 on the side edges.
- 2026-11-08 · Zone spacing 480 µm ([decisions](../../../notes/decisions.md)). Step 28 records that the electrode numbers and pad rows were unchanged by it; the zones and outer DC segments were moved.
- 2026-11-12 · The SNSPD-only die of run `R1_ONE` ([make_snspd_die.py](../../gds/make_snspd_die.py)) has 16 Au bond pads, 120 × 200 µm, at y = ±4720 µm. The two pads of a cell are 360 µm apart, and neighbouring cells' pads are 1440 µm apart (`gds/snspd_die_v4_pads.csv`). It is not a trap die; the pad rows in this brief describe the trap dies, and the package fan-out check of step 29 was not run for this die [verify before bonding it into the same carrier].

## Numbers side by side

| Quantity | 180 µm | 360 µm (current) | 240 µm | 300 µm | 400 µm | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Worst top / bottom wire angle, nominal PGA84L-like | not computed | 20.03° bottom (BL1 → B03); 18.93° top | not computed | not computed | not computed | [fanout_summary.json](../../sim/out/16_pad_pitch_check/fanout_summary.json), `edges.B.worst_angle_deg`, `edges.T.worst_angle_deg` |
| Longest projected top / bottom wire | not computed | 1.979 mm bottom; 2.082 mm top | not computed | not computed | not computed | fanout_summary.json, `edges.B.longest_projected_wire_um`, `edges.T.longest_projected_wire_um` |
| Side wire angles (left / right) | not computed | 8.58° / 4.97° | not computed | not computed | not computed | fanout_summary.json, `edges.L.worst_angle_deg`, `edges.R.worst_angle_deg` |
| Transport max step, A30 E2, centre DC free (V per 10 µm) | 7.589287 | 7.590069 | not computed | not computed | not computed | [comparison.json](../../sim/out/16_pad_pitch_check/comparison.json), case `A30_E2`: `old_transport` / `transport`, `max_step_change_V` |
| Transport max step, A30 E2, centre DC at 0 V (V per 10 µm) | 1.710110 | 1.708356 | not computed | not computed | not computed | comparison.json, case `A30_E2_V2zero` (same keys) |
| Readout max \|V\|, A30 E2, 10° zone set (V) | 6.28 | 6.29 | not computed | not computed | not computed | comparison.json, case `A30_E2`: `zones.readout.old_vmax` / `new_vmax` |
| Readout max \|V\|, B60 E2, 10° zone set (V) | 2.24 | 2.25 | not computed | not computed | not computed | comparison.json, case `B60_E2`: `zones.readout` |
| Largest readout electrode change, A30 E2 (V) | reference | 0.018 | not computed | not computed | not computed | comparison.json, case `A30_E2`: `zones.readout.max_electrode_delta_V` |
| Largest transport waveform electrode change, A30 E2 (V) | reference | 0.01284 | not computed | not computed | not computed | comparison.json, case `A30_E2`: `max_waveform_electrode_delta_V` |
| Sim 13 push, max \|V\| at 10°, A30 E2 (V) | 6.0641 | 6.0681 | not computed | not computed | not computed | [13_comparison.json](../../sim/out/16_pad_pitch_check/13_comparison.json), rows `A30_E2` / `tilt_10deg`: `old_vmax` / `new_vmax` |
| Pad-to-package wire count in the nominal plan | not computed | 42 (T 17, B 17, L 5, R 3) | not computed | not computed | not computed | fanout_summary.json, `edges.*.wires` |

Values in the 180 µm column are the archived run in `sim/out/12_final_chip/pad180/` ([folder](../../sim/out/12_final_chip/pad180/)), as step 29 records them. The 360 µm column is the current run. The 0.018 V and 0.01284 V rows are differences between the two layouts, so the 360 µm cell holds the change.

## What each option changes elsewhere

- Layout generator: `PAD_P` and `X_ROW_IN` in [make_chip.py](../../gds/make_chip.py) set the pitch (step 29 changed them from 180 to 360 µm and 2000 to 600 µm). A different pitch means regenerating the trap, test and run files in the order in [design/CLAUDE.md](../../CLAUDE.md).
- Pad positions: [LAYOUT.md](../LAYOUT.md) (edge pads row) and the pad files `gds/trap_die_v4_*_pads.csv` change with the pitch; the electrode numbers do not (step 29).
- Fan-out and bond map: [check_package_fanout.py](../../gds/check_package_fanout.py) produced the 360 µm fan-out; [04_PACKAGING.md](../process/04_PACKAGING.md) step 19 quotes the 360 µm pitch and the worst angle.
- Simulations: sim 12 and sim 13 were rerun for 360 µm (step 29). The 180 µm outputs were archived, not deleted.
- Layout checks: step 29 records `check_chip.py` ALL CHECKS PASS for the 360 µm A30, B60 and NODET dies, with no pads in the beam-exit corners.

## Not known

- Team adoption: pending, with the reason stated only as wire angles below 45° for a PGA84L-like package ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), row "Pad pitch / beam access"; [DESIGN_LOG step 29](../../DESIGN_LOG.md)).
- Clearance for a future perpendicular beam near the zones: not checked and not approved. Step 29 says no future-beam clearance was approved.
- Wire angles at 180, 240, 300 and 400 µm: no fan-out output in `sim/out/16_pad_pitch_check/`.
- Package geometry: the fan-out uses nominal finger centres from a 1993 cavity drawing, described in step 29 as approximate and not a tolerance specification.
- Finger IDs (T01…B21, L01…R21) are local, not electrical pin numbers (step 29).
- Wire span from trap to package: no source in the literature note gives one ([literature note](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/ion_trap_pad_literature.md), line 77).

## What would settle it

- A team review of perpendicular beam access near the zones, with the clearance written out for the chosen pitch ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), pad row; [DESIGN_LOG step 29](../../DESIGN_LOG.md)).
- The carrier-specific bond diagram, with the checks the bond-pad report lists: wire angle below 45°, wire length, die-to-package gap and package pad size ([report](../../research/reports/Bond%20pad%20sizing%20for%20ion%20traps.md), table row 8).
- The chosen carrier's pin map, which replaces the local finger IDs ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), carrier row).

## Where to read

- [DESIGN_LOG step 29](../../DESIGN_LOG.md) (line 1246): the 180 → 360 µm change, fan-out results, and the sim 12 and 13 comparison tables.
- [DESIGN_LOG step 21](../../DESIGN_LOG.md) (line 939): the 180 µm bond-pad sizing and the Au fill keep-out.
- [Bond pad sizing report](../../research/reports/Bond%20pad%20sizing%20for%20ion%20traps.md): bonding rules and the literature summary.
- [Literature note](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/ion_trap_pad_literature.md), Q1 table (lines 16–26): pad sizes and pitches used by other groups. Sandia Phoenix/Peregrine uses 95 µm pads at 100 µm pitch (note line 18; its source is arXiv:2009.02398, Sec. 5.3).
- [Pad electrical note](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/pad_electrical_effects.md), section 1 and the scaling line: pad capacitance scales with pad area [team calc].
- [fanout.png](../../sim/out/16_pad_pitch_check/fanout.png) and [package_fingers.csv](../../sim/out/16_pad_pitch_check/package_fingers.csv): the nominal fan-out and measured finger positions.
- [sim/16_pad_pitch_check.py](../../sim/16_pad_pitch_check.py): the comparison script.
