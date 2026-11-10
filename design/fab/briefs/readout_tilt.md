> **Claude-authored.** Decision brief: readout radial tilt. Numbers and sources only; the choice is the team's. 2026-11-10; updated the same day with sims 25 and 26 (DESIGN_LOG steps 45–46).

# Keep the 10° radial tilt in the zones?

[Open decisions](../OPEN_DECISIONS.md) · [Glossary](../../GLOSSARY.md) · [Team decision log](../../../notes/decisions.md)

**Status:** Over-range problem gone on v4; team to confirm 10°. Not a team decision yet.

## The options

| Option | What it is, in one line |
| --- | --- |
| Keep 10° | The radial axes rotated 10° in the loading and readout zone sets (current) |
| Smaller tilt | A tilt between 0° and 10° (sim 25) |
| Larger tilt, up to 45° | Rotate the radial axes further, so the in-plane beams reach the near-vertical mode more strongly (sim 25) |
| Zero tilt | No radial rotation; simulated only in sim 13's window-drop push, not as a zone set |
| Wider DAC range | Widen the ±10 V limit: the lab's Sinara Zotino is ±10 V; the Sinara 5633 HV amplifier gives 5× up to ±50 V [verify: M-Labs page only] |

## What is already fixed

- 2026-11-08 · Architecture: local mirror, no 10 µm D2 ([decisions](../../../notes/decisions.md)). The v4 dies the numbers below come from.
- 2026-11-08 · Zone spacing 480 µm ([decisions](../../../notes/decisions.md)). Zones at x = ±240 µm.
- 2026-11-08 · Detector allocation: keep B60 (reverses the entry above) ([decisions](../../../notes/decisions.md)). Both A30 and B60 are on the v4 tables.
- 2026-11-09 · Keep the 50 µm ion height ([decisions](../../../notes/decisions.md)). The push in sim 13 is computed from this height.

## Numbers side by side

| Quantity | Zero tilt (0°) | 10° (kept) | Smaller tilt | Wider DAC range | Source |
| --- | --- | --- | --- | --- | --- |
| Readout zone max \|V\|, A30 E2, zone set (V) | not computed (v3 only, see notes) | 6.29 | not computed | not computed | [12 summary](../../sim/out/12_final_chip/trap_die_v4_A30/summary.json), `readout.vmax` |
| Readout zone max \|V\|, B60 E2, zone set (V) | not computed (v3 only) | 2.25 | not computed | not computed | `trap_die_v4_B60/summary.json`, `readout.vmax` |
| Readout zone max \|V\|, NODET, zone set (V) | not computed | 7.89 | not computed | not computed | `trap_die_v4_NODET/summary.json`, `readout.vmax` |
| Loading zone max \|V\|, A30 E2, zone set (V) | not computed | 7.45 | not computed | not computed | `trap_die_v4_A30/summary.json`, `loading.vmax` |
| Window-drop push max \|V\|, A30 E2 (V) | 1.3355 | 6.0681 | not computed | not computed | [13 summary](../../sim/out/13_dc_height_tuning_v4/summary.json), `A30_E2.tilt_0deg` / `tilt_10deg` → `at_needed_shift.vmax` |
| Window-drop push max \|V\|, A30 E1 (V) | 1.5164 | 6.2027 | not computed | not computed | summary.json, `A30_E1` (same keys) |
| Window-drop push max \|V\|, B60 E2 (V) | 0.6639 | 1.9117 | not computed | not computed | summary.json, `B60_E2` (same keys) |
| Window-drop push max \|V\|, B60 E1 (V) | 0.6740 | 2.1390 | not computed | not computed | summary.json, `B60_E1` (same keys) |
| Micromotion at the reached shift, A30 E2 (nm) | 173.36 | 173.36 | not computed | not computed | summary.json, `A30_E2` → `at_needed_shift.a_mm_nm` |
| Micromotion at the reached shift, B60 E2 (nm) | 290.83 | 290.83 | not computed | not computed | summary.json, `B60_E2` → `at_needed_shift.a_mm_nm` |

The push rows are the DC set that moves the ion up by the window drop, solved without the ±10 V clip ([sim 13 docstring](../../sim/13_dc_height_tuning.py)). The window drop for A30 E2 is −1.19 µm (`window_drop_um`). The zone rows are the static zone solves in sim 12; the summaries mark them `bounded: false`, so the solve did not reach the ±10 V limit. The 0° and 10° micromotion values are equal to the printed precision.

## Larger tilts (sim 25, DESIGN_LOG step 45)

Why the angle matters: the beams run in the plane at 45° to the trap axis, and a Doppler beam cools a mode at a rate proportional to the square of its wavevector's projection on that mode. For the near-vertical radial mode that is ½ sin²θ [team calc]:

| Tilt θ | 0° | 10° | 20° | 30° | 45° |
| --- | --- | --- | --- | --- | --- |
| Projection on the near-vertical mode | 0 | 0.015 | 0.058 | 0.125 | 0.25 |

The axial mode gets 0.5 at every θ. Allcock 2010 (arXiv:0909.3272, p. 2 and Table III on p. 5) tilts a symmetric surface trap to about 42–45° with a DC quadrupole.

Largest |V| for a 45° tilt with the radial modes split by 0.1 MHz, all DC electrodes, without the ±10 V clip:

| Zone | 0.8 MHz axial | 0.6 MHz axial | Largest tilt within ±10 V at 0.8 MHz | Source |
| --- | --- | --- | --- | --- |
| Loading, A30 and B60 | 11.30 V | 8.41 V | 25° | [sim 25](../../sim/out/25_radial_tilt_sweep/trap_die_v4_A30/summary.json), `loading.records` (`fixed split`, `all`, 45, 0.1) and `loading.theta_max_fit`; `_fax0.6` folder |
| Readout, A30 | 13.27 V | 9.51 V | 23° | same file, `readout` |
| Readout, B60 | 6.81 V | 5.88 V | 45° | `trap_die_v4_B60/summary.json` |
| Loading / readout, NODET | 11.04 / 11.01 V | 8.27 / 8.23 V | 27° | `trap_die_v4_NODET/summary.json` |

- A larger split costs about 4.6–4.9 V more per 0.1 MHz at 45°.
- 10 mV errors on every voltage scatter the 45° axes by 0.8–1.4° (std).
- The voltage goes on top/bottom outer-segment pairs driven in opposition. A split centre DC would need about 0.15 V per 0.1 MHz in a 2-D estimate (step 45) [team calc, not run on the GDS]; it is a layout change.
- Grounding or tying electrodes to fit one 32-channel Zotino changes these numbers by at most 0.7 V (sim 26, step 46).

## What each option changes elsewhere

- Sim 12 zone sets use the 10° tilt ([DESIGN_LOG step 28](../../DESIGN_LOG.md), line 1201). Changing the tilt means rerunning [12_final_chip_check.py](../../sim/12_final_chip_check.py) on each die.
- Sim 13 is the only place the repo solves 0° and 10° side by side ([13_dc_height_tuning.py](../../sim/13_dc_height_tuning.py), docstring). Changing the tilt means rerunning it for the four die and electrode cases.
- Transport: the centre DC is held at 0 V while moving, and the tilt set (which uses the centre DC) is ramped in at each zone ([DESIGN_LOG step 25](../../DESIGN_LOG.md), line 1118; [OPEN_DECISIONS.md](../OPEN_DECISIONS.md), transport row).
- Trapping checklist: the loading-zone 10° set, the ramp-in at readout, and the micromotion predictions are in [04_TRAPPING.md](../tests/04_TRAPPING.md), steps 6, 7 and 9 (line 40).
- DAC: the ±10 V limit is cited in [DESIGN_LOG step 11](../../DESIGN_LOG.md) (line 561) and [design/CLAUDE.md](../../CLAUDE.md). No file names a DAC part or range.

## Not known

- Cooling rates and temperatures for each tilt: not computed. The per-mode formula (Itano & Wineland 1982) has not been opened ([radial tilt notes](../../research/research_notes/Radial%20tilt%202026-11/README.md)).
- Zero-tilt zone sets on v4: not computed. The only zero-tilt zone numbers are v3 values: readout DC without tilt 6.64 V (A30) and 3.38 V (B60) ([DESIGN_LOG step 19](../../DESIGN_LOG.md), table, line 862). The same step gives 13.2 V and 15.2 V at 10° on v3.
- Loading-zone |V| at 10°: [04_TRAPPING.md](../tests/04_TRAPPING.md), step 6, marks it "[verify; not in the notes]". The sim 12 summary gives 7.45 V for A30 E2 (`loading.vmax`).
- Micromotion: the planar model and the window-drop values are upper bounds for E1 (the file gives ≤ −0.37 µm). Micromotion with the ion following the null is estimated at about 4 % of the shift with no trim ([DESIGN_LOG step 39](../../DESIGN_LOG.md), addendum, line 1607), which the file says a 10° set can raise to about 10 %.
- `readout.radial_axis_angle_deg` in the sim 12 summaries reads 170.1° (A30, B60) and −99.6° (NODET). The file does not state its reference angle; check it before quoting.
- Electrode option: the push values differ between E1 and E2 (rows above). The option row is [OPEN_DECISIONS.md](../OPEN_DECISIONS.md), "Electrode Au".

## What would settle it

- The team confirming 10° ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), readout tilt row: "team to confirm 10°").
- Micromotion at readout, compared with the predicted 173 nm (E2) / 55 nm (E1) for A30 and 291 nm / 81 nm for B60 ([04_TRAPPING.md](../tests/04_TRAPPING.md), step 9). This micromotion is vertical, so RF-photon correlation with the in-plane beams does not see it at any tilt; it needs a beam with a vertical component (DESIGN_LOG step 45).
- The ramp-in check at the readout zone after arrival ([04_TRAPPING.md](../tests/04_TRAPPING.md), step 7).
- The shim and micromotion-compensation fields at both zones, compared with the window electrostatics ([04_TRAPPING.md](../tests/04_TRAPPING.md), steps 6 and 9).

## Where to read

- [DESIGN_LOG step 11](../../DESIGN_LOG.md) (line 557): the reason for the tilt, "in-plane 45° beams cool both radial modes" (line 561).
- [DESIGN_LOG step 19](../../DESIGN_LOG.md) (line 851): v3 readout DC table and the over-range cause (line 869).
- [DESIGN_LOG step 25](../../DESIGN_LOG.md) (line 1105), [step 27](../../DESIGN_LOG.md) (line 1170) and [step 28](../../DESIGN_LOG.md) (line 1191): v4 zone and push values.
- [DESIGN_LOG step 29](../../DESIGN_LOG.md) (line 1294): the sim 13 rerun table on the 360 µm layout (largest required-V change 0.00403 V).
- Readout radial frequencies from the sim 12 summaries (`readout.dc_freqs_MHz`): A30 2.796 / 3.083 MHz; B60 2.895 / 2.990 MHz; NODET 2.900 / 2.985 MHz.
- [sim/03_segment_pitch.py](../../sim/03_segment_pitch.py) (early tilt study, `vmax_tilt_10deg` in `sim/out/03_segment_pitch/summary.json`): 12.15 V at 50 µm pitch, 0.358 V at 75 µm, 1.708 V at 100 µm, 2.763 V at 150 µm, 7.039 V at 200 µm. This is a 1 MHz axial study on a gapless midline model, not the v4 die.
- [sim/13_dc_height_tuning.py](../../sim/13_dc_height_tuning.py), docstring: the method and what the 0° and 10° blocks mean.
