> **Claude-authored.** Decision brief: carrier and package spacer. Numbers and sources only; the choice is the team's. 2026-11-10.

# Which chip carrier, and what spacer under the die?

[Open decisions](../OPEN_DECISIONS.md) · [Glossary](../../GLOSSARY.md) · [Team decision log](../../../notes/decisions.md)

**Status:** Carrier: **Open.** Local finger IDs in the fan-out table are not package pin numbers. Package spacer: **Open proposal [verify]**, not an adopted material or thickness. Not a team decision yet.

## The options

| Option | What it is, in one line |
| --- | --- |
| PGA84L-like 84-pin package | 84 fingers, 21 per edge; the fan-out uses its cavity drawing (1993) |
| 100-pin CPGA | 100-pin ceramic pin-grid carrier; named in the decision row, no geometry in the repo |
| Lab carrier | The lab's own carrier; not described anywhere in the repo |
| Spacer (proposal) | Under the die, at least approximately 0.6 mm thick, die-sized (10 × 10 mm) or larger, Si suggested. No alternative spacer is listed |

## What is already fixed

- 2026-11-07 · 10 × 10 mm trap die, trap centred, pads at the die edges ([decisions](../../../notes/decisions.md)). The die the carrier receives.
- 2026-11-02 · First run is trap-only (R1_TRAP) ([decisions](../../../notes/decisions.md)), and 2026-11-08 · R1_TRAP follows the new architecture ([decisions](../../../notes/decisions.md)). R1_TRAP was built from 6 NODET and 2 TEST_TRAP dies ([design/CLAUDE.md](../../CLAUDE.md), run list). It is replaced by `R1_ONE` (2026-11-12): one wafer with 4 A30, 1 B60, 2 SNSPD-only and 2 NODET dies. The NODET die has no Al apart from four small corner crosses.
- 2026-11-02 · Ion height 50 µm; height may differ between zones, and 2026-11-09 · Keep the 50 µm ion height ([decisions](../../../notes/decisions.md)). The height the beams are aimed at.
- 2026-11-12 · The SNSPD-only die of `R1_ONE` also has 16 Au edge pads, 120 × 200 µm, at y = ±4720 µm ([make_snspd_die.py](../../gds/make_snspd_die.py)). The carrier and spacer rows below are about the trap die; whether the fan-out covers this die is not checked [verify].

## Numbers side by side

| Quantity | PGA84L-like 84-pin | 100-pin CPGA | Lab carrier | Spacer (proposal) | Source |
| --- | --- | --- | --- | --- | --- |
| Worst top / bottom wire angle, nominal (°) | 20.03 (bottom); 18.93 (top) | not computed | not computed | not computed | [fanout_summary.json](../../sim/out/16_pad_pitch_check/fanout_summary.json), `edges.B.worst_angle_deg`, `edges.T.worst_angle_deg` |
| Side wire angles, left / right (°) | 8.58 / 4.97 | not computed | not computed | not computed | fanout_summary.json, `edges.L`, `edges.R` |
| Wires in the nominal plan | 42 (T 17, B 17, L 5, R 3) | not computed | not computed | not computed | fanout_summary.json, `edges.*.wires` |
| Cavity dimension J = K (mm) | 11.938 (J = K = 0.470 in) | not computed | not computed | not computed | [DESIGN_LOG step 29](../../DESIGN_LOG.md), line 1246 |
| Thickness (mm) | not computed | not computed (other groups: 1.5 mm, see note) | not computed | ≥ approximately 0.6 (proposal) | [OPEN_DECISIONS.md](../OPEN_DECISIONS.md), row "Package spacer" |
| RF-to-ground capacitance of the carrier (pF) | not computed | 4 ± 1 (another group's Phoenix package, not our part) | not computed | not computed | [literature note](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/ion_trap_pad_literature.md), line 93 |

The 1.5 mm entry in the 100-pin CPGA column is a spacer used by other groups (Tabakov et al.; Stick et al.), not one of our options: [literature note](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/ion_trap_pad_literature.md), lines 21 and 69. The beam clipping figure is not in this table, because it has no carrier or spacer term: 493 nm, full 10 mm die, 1.69 × 10⁻² of the beam power strikes the surface ([summary.json](../../sim/out/11_beam_clearance/summary.json), key `493 nm (cool/detect)` → `full_chip_10mm`; [DESIGN_LOG step 4](../../DESIGN_LOG.md), line 142).

## What each option changes elsewhere

- The carrier sets the bond map. The carrier pin column in [04_PACKAGING.md](../process/04_PACKAGING.md) step 19 is blank until the carrier is chosen. A new carrier drawing means a new fan-out run ([check_package_fanout.py](../../gds/check_package_fanout.py)).
- The electrical pin map is carrier-specific ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), carrier row).
- The spacer changes the height of the die above the carrier. The repo states no value for that height in the layout, and the beam-clearance model (sim 11) has no spacer term.
- Die attach: [04_PACKAGING.md](../process/04_PACKAGING.md) step 19 says Au/Sn attach needs a Au backside, and the die backside is SiO₂, so that attach does not apply as written. The spacer also sits against the die backside.
- After packaging: repeat pad-to-pad isolation through the carrier pins and meander R₅ ([04_PACKAGING.md](../process/04_PACKAGING.md), "After packaging").
- Bond wires: [04_PACKAGING.md](../process/04_PACKAGING.md) step 19 ("Wire bonds") gives the bond edges for each pad row. The bond-pad report (row 8) asks for loops kept low along the 45° beam exits.

## Not known

- The lab's own carrier: not in the repo. [OPEN_DECISIONS.md](../OPEN_DECISIONS.md) lists it as an option only.
- Cryostat fit of any carrier: marked [verify] in [04_PACKAGING.md](../process/04_PACKAGING.md), step 19.
- The reason for the 0.6 mm spacer value. The decision row, [DESIGN_LOG step 29](../../DESIGN_LOG.md) and step 19 of the packaging page state the proposal without a reason. The literature note records another group's reason for a spacer (Leibrandt et al.: to raise the chip for laser access), at its line 72.
- Whether the proposed spacer clears the beams: [OPEN_DECISIONS.md](../OPEN_DECISIONS.md) says verify the actual carrier, die and spacer stack and beam clearance. No file computes it.
- MIT.nano bonder model and wedge or capillary part numbers: open in [DESIGN_LOG step 21](../../DESIGN_LOG.md) (line 939).
- Full wire span from trap to package: no source in the literature note gives one (note, line 77).
- The 84-pin finger positions come from a drawing and are approximate ([DESIGN_LOG step 29](../../DESIGN_LOG.md), line 1246).

## What would settle it

- The team's carrier choice, followed by a cryostat fit and a carrier-specific pin map ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), carrier row).
- A bond diagram drawn against the real carrier, with the bond-pad report's checks: wire angle below 45°, wire length, die-to-package gap, package pad size ([report](../../research/reports/Bond%20pad%20sizing%20for%20ion%20traps.md), table row 8).
- The spacer check named in [OPEN_DECISIONS.md](../OPEN_DECISIONS.md): actual carrier, die and spacer stack, and beam clearance.
- The W7 bond-and-leak loop, which confirms the bonder and wedge dimensions and the carrier bond diagram ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), "Before R1_ONE").

## Where to read

- [DESIGN_LOG step 29](../../DESIGN_LOG.md) (line 1246): PGA84L finger measurement, fan-out angles, and the cavity drawing reference.
- [DESIGN_LOG step 4](../../DESIGN_LOG.md) (line 142): beam clipping on a plain 10 mm die (1–3 % of each beam strikes the surface, before the layout change in step 8).
- [DESIGN_LOG step 21](../../DESIGN_LOG.md) (line 939): bond-pad sizing and the open bonder questions.
- [Packaging page](../process/04_PACKAGING.md), step 19 (line 61) and "Open before packaging" (line 96).
- [Literature note](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/ion_trap_pad_literature.md): lines 21 (CPGA on a 1.5 mm spacer), 66 (package RF trace 3.7 pF, updated 2.9 pF, a custom AlN CPGA), 69 (1.5 mm ceramic spacer), 72 (spacer for laser access, solder attach), 93 (RF budget: CPGA 4 ± 1 pF).
- [sim/out/11_beam_clearance/summary.json](../../sim/out/11_beam_clearance/summary.json) and [sim/11_beam_clearance.py](../../sim/11_beam_clearance.py): the clipping model.
- [fanout.png](../../sim/out/16_pad_pitch_check/fanout.png) and [package_fingers.csv](../../sim/out/16_pad_pitch_check/package_fingers.csv): the nominal PGA84L-like fan-out.
