> **Claude-authored.** Decision brief: Al local mirror, inlaid in the SiO₂ or raised on it. Numbers and sources only; the choice is the team's. 2026-11-10.

# Al mirror: inlaid in the SiO₂, or raised?

[Open decisions](../OPEN_DECISIONS.md) · [Glossary](../../GLOSSARY.md) · [Team decision log](../../../notes/decisions.md)

**Status:** The team decided on 2026-11-09 that the mirror is 100 nm of Al, inlaid ([decisions](../../../notes/decisions.md), last entry). Still open in [OPEN_DECISIONS](../OPEN_DECISIONS.md), "Before any v4 run": whether to keep the inlay or fall back to the raised mirror if witness loop W8 fails, and an optional narrowing of the mirror. The "Raised or inlaid" row there reads: "for the ion the two are equivalent at 100 nm (step 39). The inlay is kept on the pages; the raised mirror is the simpler process and is the named fallback. The team may swap them."

## The options

| Option | What it is, in one line |
| --- | --- |
| Inlaid, 100 nm (decided 2026-11-09) | 100 nm evaporated Al in a 100 nm recess in the thermal SiO₂, level with the SiO₂ beside it (steps 3a to 3d of [01_FOUNDATION](../process/01_FOUNDATION.md)) |
| Raised, 100 nm (named fallback) | The same 100 nm Al on the SiO₂, with the recess etch (step 3b) skipped; a 0.10 µm step under the Au ([01_FOUNDATION](../process/01_FOUNDATION.md), fallback) |
| Raised, 450 nm (2026-11-08, replaced) | 450 nm Al standing on the SiO₂; replaced by the 100 nm inlaid mirror on 2026-11-09 |
| Narrowed mirror, optional (Claude's proposal, not adopted) | [OPEN_DECISIONS](../OPEN_DECISIONS.md), "Mirror edge on the centre-DC edge", reads: "Proposal: narrow the mirror to \|y\| ≤ 18 µm (layer 10 of A30 and B60 only; 2 µm beyond the NbN, 2 µm inside the Au), and hold the layer-10 overlay to about 1 µm instead of the ±5 µm on the [mask list](../mask_list.md). Not done: it changes the released dies." |

## What is already fixed

- 2026-11-08 · Architecture: local mirror, no 10 µm D2 ([decisions](../../../notes/decisions.md)). The Al is a local mirror under the SNSPD and its leads, never under the RF rails.
- 2026-11-08 · On-chip vias from the Au ground fill to the Al ([decisions](../../../notes/decisions.md)). The mirror is grounded on chip through a via under the Au ground fill.
- 2026-11-08 · Local mirror Al 450 nm thick ([decisions](../../../notes/decisions.md)). Superseded: the entry's header reads "Replaced on 2026-11-09: the mirror is now 100 nm, inlaid."
- 2026-11-09 · Local mirror: 100 nm Al, inlaid (replaces the 450 nm of 2026-11-08) ([decisions](../../../notes/decisions.md)). This is the decision the Status line describes.
- 2026-11-09 · Keep the 50 µm ion height ([decisions](../../../notes/decisions.md)). The mirror numbers below are computed at this height.

## Numbers side by side

Columns are the three mirror cases in the sim 10c and 10d tables. Ranges are the two Al resistivities used (3 and 4 µΩ·cm, room temperature), as in [sim 10c](../../sim/out/10c_mirror_thickness/summary.json). Values are for E2 unless a row says E1.

| Quantity | Raised 450 nm (replaced) | Raised 100 nm (fallback) | Inlaid 100 nm (decided) | Source |
| --- | --- | --- | --- | --- |
| Step at the mirror edge | 450 nm | 100 nm | 0 | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `al450.step_nm`, `al100.step_nm`, `al100_inlaid.step_nm` |
| Strip resistance, T10 (four-point) | 4.2–5.6 Ω | 18.8–25.1 Ω | 18.8–25.1 Ω | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.rho.*.t10_ohm` (table in [table.md](../../sim/out/10c_mirror_thickness/table.md)) |
| Current along the strip to the via | 3.153 mA | 3.137 mA | 3.194 mA | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.rho.3e-08.i_mirror_mA` for each case |
| Swing at the detector end | 6.62–8.83 mV | 29.65–39.53 mV | 30.19–40.25 mV | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.rho.*.v_m_mV` |
| Extra nanowire current, upper bound | 0.160–0.213 µA | 0.716–0.954 µA | 0.729–0.972 µA | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.rho.*.i_wire_upper_uA` |
| Direct nanowire pickup, for comparison | 0.959 µA | 0.959 µA | 0.959 µA (E1: 1.915 µA) | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.window.I_pk_uA` in each case |
| Strip dissipation, room-temperature ρ | 7.35–9.80 µW | 32.73–43.63 µW | 33.93–45.23 µW | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.rho.*.p_uW` |
| Common mode from the mirror, per slot lead | 0.898–1.2 µA | 4.02–5.36 µA | 4.09–5.46 µA | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.rho.*.i_lead_mirror_uA` |
| Null height change against inlaid, no misalignment, E2 / E1 | 734 nm / 694 nm | 163 nm / 130 nm | 0 / 0 | [sim 10d](../../sim/out/10d_mirror_step/summary.json), `cases["E2|s=0.45|d=0.0"]`, `cases["E2|s=0.10|d=0.0"]` and `cases["E1|…"]` (`dz_nm`); [table](../../sim/out/10d_mirror_step/table.md) |
| Micromotion if nothing is re-tuned, A30 | 126.2 nm (E2) / 115.6 nm (E1) | 28.3 nm (E2) / 22.6 nm (E1) | 0 | [sim 10d](../../sim/out/10d_mirror_step/summary.json) table, column "micromotion if nothing is re-tuned" |
| Micromotion from the mirror swing, A30 / B60 | 0.34–0.46 nm / 0.69–0.91 nm | 1.53–2.05 nm / 3.07–4.09 nm | 1.56–2.08 nm / 3.13–4.17 nm | [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `E2.rho.*.micromotion_A30_nm`, `micromotion_B60_nm` |
| Sideways null shift, 2 µm misalignment, E2 / E1 | 142 nm / 653 nm | 45 nm / 529 nm | 15 nm / 496 nm | [sim 10d](../../sim/out/10d_mirror_step/summary.json), `cases["E2|s=0.45|d=2.0"]`, `cases["E2|s=0.10|d=2.0"]`, `cases["E2|s=0.00|d=2.0"]` (`dx_nm`); E1 keys alike |
| Narrowed mirror, \|y\| ≤ 18 µm | not computed | not computed | not computed | No simulation of the narrowing in the repo; sim 10d tests misalignment only |

The sim 10c raised cases are solved with coplanar electrodes, so the step itself is not in that field model ([DESIGN_LOG step 37](../../DESIGN_LOG.md), limits). The sim 10d cases do include the step height. The 10c micromotion column is a small-patch estimate. The 10d values come from a 2-D cross-section through the lead slot, with absolute null heights off against gds2itvg (about 47.4 µm against 49.97 µm); only the differences between cases are used ([DESIGN_LOG step 39](../../DESIGN_LOG.md)).

## What each option changes elsewhere

- Step 3 of [01_FOUNDATION](../process/01_FOUNDATION.md) is written as 3a to 3d for the inlaid mirror (resist, 100 nm recess, Al evaporation, lift-off). The fallback skips 3b and keeps the same mask ([01_FOUNDATION](../process/01_FOUNDATION.md), step 3).
- Witness loop W8 covers the inlaid recess and lift-off ([QUALIFICATION](../QUALIFICATION.md), "W8 Inlaid Al mirror"). The fallback names step 15 and test structure T12 as the check that the Au crosses the 0.10 µm step ([01_FOUNDATION](../process/01_FOUNDATION.md), fallback).
- T10 expected resistance is 18.8–25.1 Ω for both 100 nm options, and 4.2–5.6 Ω for the replaced 450 nm mirror ([tests/01_ELECTRICAL](../tests/01_ELECTRICAL.md); [LAYOUT](../LAYOUT.md)). The T10 acceptance limit is not set [verify].
- No GDS change was made for the 100 nm inlay: [DESIGN_LOG step 38](../../DESIGN_LOG.md) states "No GDS change; nothing was regenerated." The optional narrowing would change layer 10 in the released A30 and B60 dies ([OPEN_DECISIONS](../OPEN_DECISIONS.md), "Mirror edge on the centre-DC edge").
- The Au over the mirror edge is the check that differs by option: "no lip or groove at the mirror edge" is listed for both electrode branches ([03_ELECTRODES](../process/03_ELECTRODES.md), "E1 vs E2 at a glance").
- The stack and process-flow figures show the inlaid mirror ([DESIGN_LOG step 38](../../DESIGN_LOG.md), "Pages and figures").

## Not known

- Recess depth and RIE rate with the lift-off resist on the wafer, and lift-off after the fluorine etch. No source read covers the recess-and-lift-off step ([L3 note](../../research/research_notes/Loose%20ends%202026-11/L3_inlaid_mirror.md), section A and "What we could not find").
- Whether a fluorine-etched, crosslinked top resist changes the lift-off outcome; the UMN source could not be opened (L3 note, section B).
- Hillocks in 100 nm evaporated Al after the ≤ 300 °C steps. The hillock sources in the L3 note are sputtered films or abstract-only ([DESIGN_LOG step 38](../../DESIGN_LOG.md), "What this accepts").
- Residual step and edge profile after lift-off. The ≤ 20 nm limit is a design call, to be checked ([DESIGN_LOG step 38](../../DESIGN_LOG.md), "Planarity limit").
- Heating of the strip: the 34–45 µW figure uses room-temperature resistivity and no thermal model ([DESIGN_LOG step 38](../../DESIGN_LOG.md)).
- Resistivity of evaporated Al at 4 K for a 100 nm film. No value was found in the L3 note's sources.
- Whether Hampel 2023 planarized its mirror. Its mirror is 50 nm evaporated Al, raised, with no mention of a step or recess ([DESIGN_LOG step 37](../../DESIGN_LOG.md); [L3 note](../../research/research_notes/Loose%20ends%202026-11/L3_inlaid_mirror.md), section D).

## What would settle it

- Witness loop W8 on a dummy thermal-SiO₂ wafer: recess depth, Al thickness, residual step and edge profile after lift-off and after the 238 nm spacer, lift-off quality, and hillocks after 300 °C ([QUALIFICATION](../QUALIFICATION.md), W8).
- The T10 four-point strip resistance on the test die, against 18.8–25.1 Ω ([LAYOUT](../LAYOUT.md); [01_FOUNDATION](../process/01_FOUNDATION.md), step 3 measurement).
- The cold RF test: the SNSPD switching current against RF amplitude, to watch for the strip heating ([OPEN_DECISIONS](../OPEN_DECISIONS.md), "Mirror strip heating").
- The layer-10 overlay on the mask set, against the 5 µm and 1 µm figures in [OPEN_DECISIONS](../OPEN_DECISIONS.md), "Mirror edge on the centre-DC edge", and the [mask list](../mask_list.md).
- The team's choice between keeping the inlay and falling back to the raised mirror, which the team has not yet made ([OPEN_DECISIONS](../OPEN_DECISIONS.md), "Raised or inlaid").

## Where to read

- [DESIGN_LOG step 37](../../DESIGN_LOG.md) (line 1492): the thickness comparison and the step it leaves.
- [DESIGN_LOG step 38](../../DESIGN_LOG.md) (line 1528): the 100 nm inlaid case, its process, and what it accepts.
- [DESIGN_LOG step 39](../../DESIGN_LOG.md) (line 1570): the raised and misaligned mirror on the RF null.
- [notes/decisions.md](../../../notes/decisions.md): the entries "Local mirror Al 450 nm thick" (2026-11-08, replaced) and "Local mirror: 100 nm Al, inlaid" (2026-11-09).
- [sim 10c script](../../sim/10c_mirror_thickness.py) and [sim 10d script](../../sim/10d_mirror_step.py).
- [01_FOUNDATION](../process/01_FOUNDATION.md), step 3: the inlay process and the fallback.
- [QUALIFICATION](../QUALIFICATION.md), W8: the witness loop for the inlay.
- [L3 note](../../research/research_notes/Loose%20ends%202026-11/L3_inlaid_mirror.md): what the literature search found and did not find.
