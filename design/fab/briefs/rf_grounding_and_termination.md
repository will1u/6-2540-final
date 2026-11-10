> **Claude-authored.** Decision brief: RF grounding and filters. Numbers and sources only; the choice is the team's. 2026-11-10.

# How are the DC electrodes and the SNSPD leads grounded at RF?

[Open decisions](../OPEN_DECISIONS.md) · [Glossary](../../GLOSSARY.md) · [Team decision log](../../../notes/decisions.md)

**Status:** Open; more important on v4 ([OPEN_DECISIONS](../OPEN_DECISIONS.md), "RF grounding / filters"). Not a team decision yet.

## The options

| Option | What it is, in one line |
| --- | --- |
| Centre-DC filtering | A capacitor from the centre DC (electrode 2) to ground; numbers in Part 1 |
| Carrier grounds | Ground connections made on the carrier and bond wires; no carrier design is in the repo ([04_PACKAGING](../process/04_PACKAGING.md), "SNSPD RF termination: open") |
| Symmetric detector termination or cancellation | The same termination on both SNSPD leads, or a cancellation tone; numbers in Part 2 |
| RF bypass at both SNSPD lead pads (v4) | A capacitor or termination at SNS and SNG; the matched rows in Part 2 |

Part 1 covers the DC electrodes. Part 2 covers the two SNSPD leads. The two parts are kept apart because they use different sources and models.

## What is already fixed

- 2026-11-08 · Architecture: local mirror, no 10 µm D2 ([decisions](../../../notes/decisions.md)). The Al mirror sits under the SNSPD and its leads only.
- 2026-11-08 · Local-mirror lead routing: slot along the centre DC ([decisions](../../../notes/decisions.md)). The SNSPD leads are in the electrode Au, in a slot along the centre DC.
- 2026-11-08 · On-chip vias from the Au ground fill to the Al ([decisions](../../../notes/decisions.md)). The mirror is tied to the ground fill on chip, not only by bond wires.
- 2026-11-09 · Local mirror: 100 nm Al, inlaid (replaces the 450 nm of 2026-11-08) ([decisions](../../../notes/decisions.md)).
- 2026-11-07 · No ITO anywhere ([decisions](../../../notes/decisions.md)).
- 2026-11-08 · Zone spacing 480 µm ([decisions](../../../notes/decisions.md)). Zones at x = ±240 µm.

`notes/decisions.md` records no decision on filter values, the termination of the leads, or the carrier. Those are open.

## Numbers side by side

### Part 1: filter capacitors on the DC electrodes

Source: [sim 23 summary](../../sim/out/23_dc_rf_coupling/summary.json) and [table.md](../../sim/out/23_dc_rf_coupling/table.md) (2026-11-10; script [23_dc_rf_coupling.py](../../sim/23_dc_rf_coupling.py)). C_c is the coupling from the rails to the electrode, C_g the capacitance to ground, C_f the filter capacitor. V_el = 53 V × C_c / (C_c + C_g + C_f), at 28 MHz. The null shift is the readout-zone shift from the gds2itvg unit potentials (`null_shifts`, `centre_abs_nm`; outer row: `top5_abs_nm`, the top segment alone). All values are [team calc].

| Electrode | Au | C_c (pF) | C_g (pF) | of C_g, to the Al mirror (pF) | V_el, C_f = 0 (V) | V_el, 100 pF (V) | V_el, 1 nF (V) | V_el, 10 nF (V) | Null shift, C_f = 0 (nm) | 100 pF (nm) | 1 nF (nm) | 10 nF (nm) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Centre DC, A30 | E2 | 0.4143 | 3.2056 | 3.0927 | 6.067 | 0.2119 | 0.02188 | 0.002195 | 2758 | 96.35 | 9.948 | 0.9981 |
| Centre DC, A30 | E1 | 0.3290 | 3.1422 | 3.0750 | 5.023 | 0.1685 | 0.01737 | 0.001743 | 2284 | 76.61 | 7.899 | 0.7924 |
| Centre DC, NODET | E2 | 0.7396 | 0.1219 | - | 45.5 | 0.3886 | 0.03916 | 0.003919 | not computed (A30 layout only) | not computed | not computed | not computed |
| Centre DC, NODET | E1 | 0.6567 | 0.1217 | - | 44.71 | 0.3453 | 0.03478 | 0.00348 | not computed | not computed | not computed | not computed |
| Outer DC segment, 120 µm | E2 | 0.01495 | 0.401 (5 mm lead) / 0.581 (8 mm) | - | 1.905 (1.329 with 8 mm) | 0.00789 | 0.000792 | 0.0000792 | 180.4 | 0.7474 | 0.07502 | 0.007505 |
| Outer DC segment, 120 µm | E1 | 0.01371 | 0.401 / 0.581 | - | 1.752 (1.222 with 8 mm) | 0.00724 | 0.000726 | 0.0000727 | 166.0 | 0.6856 | 0.06881 | 0.006884 |

- Sim 23 field solve (2-D), `per_electrode` block of the summary; the outer row's C_g is taken from [pad_electrical_effects.md](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/pad_electrical_effects.md) lines 29–31 (10 µm SiO₂ over a buried Al plane, not the v4 stack) [verify for this stack].
- The C_f = 0 column is a limit: no capacitor at all. No option in the repo proposes it.
- Outer-row null shift is the top segment alone (nearest segment at readout: electrode 12), from `null_shifts`, `top5_abs_nm`.
- RF current through the filter capacitor, I = ωC_f V_el ([table.md](../../sim/out/23_dc_rf_coupling/table.md), "Divider and RF"): A30 E2 3728 µA (100 pF), 3850 µA (1 nF), 3862 µA (10 nF); A30 E1 2964 / 3057 / 3066 µA; NODET E2 6837 / 6890 / 6895 µA; NODET E1 6076 / 6118 / 6122 µA; outer segment, 5 mm lead, E2 138.8 / 139.3 / 139.4 µA; E1 127.3 / 127.8 / 127.8 µA.
- Limits in the sim docstring: 2-D, ideal conductors, no segment ends. Bond-wire and lead inductance between electrode and capacitor are ignored [inference].

Filter values the repo already quotes, with their sources:

- 1 kΩ / 1 nF, about 160 kHz roll-off, citing Chiaverini Sec. 6: [fivewire_design_rules.md](../../research/research_notes/Trap%20integrated%20SNSPD%20design/fivewire_design_rules.md), line 18.
- 35 kΩ / 220 pF RC array on the PCB next to the trap (Guise et al., via Romaszko 2020); 60 pF on-chip from 1 mm² plates (Doret 2012, Sec. 2.3); 820 pF wire-bonded capacitors (Sterling 2014): [pad_electrical_effects.md](../../research/research_notes/Bond%20pad%20sizing%20for%20ion%20traps/pad_electrical_effects.md), lines 89–110.
- First-order RC, 5 kHz corner, Dietl et al. Sec. 4.2, page 9 (read from the PDF): [T1 note](../../research/research_notes/Test%20setup%202026-11/T1_dietl_2025.md).

Trade against transport speed. Sim 21 ([summary](../../sim/out/21_transport_waveform/trap_die_v4_A30_V2zero/summary.json), `nbar_scan`) tried two filter corners, f = 50 kHz and 200 kHz (`F_FILT`). The key reads T (move time), F (DAC update rate) and f (filter corner). Motional quanta left in the ion, classical model, A30 layout with centre DC at 0 V:

| Move time T | Update rate F | n̄, f = 50 kHz | n̄, f = 200 kHz |
| --- | --- | --- | --- |
| 100 µs | 1 MHz | 3.56e-5 | 5.39e-4 |
| 300 µs | 1 MHz | 5.40e-9 | 8.21e-8 |
| 1 ms | 1 MHz | 3.51e-13 | 5.39e-12 |
| 100 µs, 300 µs, 1 ms | 100 kHz | 4.89e6 (all three) | 7.40e7 (all three) |

Sim 20 ([summary](../../sim/out/20_transport_timing/summary.json), `part2_nbar_by_steps`, `480` steps, `part2_T_s` = 100 µs, 300 µs, 1 ms, 3 ms): 10 kHz filter 1.62e-9 / 1.85e-10 / 1.82e-11 / 1.96e5; 50 kHz 4.26e-8 / 5.38e-9 / 7.40e-10 / 4.89e6; 200 kHz 7.78e-7 / 1.40e-7 / 4.82e-8 / 7.40e7. The values are not monotonic in T.

### Part 2: termination of the two SNSPD leads

Source: [sim 19 summary](../../sim/out/19_lead_termination/summary.json), die A30, R pair 0 Ω (`I_nw_uA`, `pct_of_8uA`, `pulse_note`). Script and model: [19_lead_termination.py](../../sim/19_lead_termination.py) (docstring). Its E2 input is 44.5 µA; its E1 input is 28.3 µA, while [sim 10c](../../sim/out/10c_mirror_thickness/summary.json) (`al100_inlaid.E1.slot.I_lead_in_trap_uA`) gives 28.61 µA for the current stack. The % column is of the 8 µA reference the sim uses. Lumped model, one frequency (28 MHz), upper bound.

| Termination (signal lead / return lead) | Nanowire RF current, E2 (µA) | % of 8 µA | Nanowire RF current, E1 (µA) | % of 8 µA | Pulse note (sim 19) |
| --- | --- | --- | --- | --- | --- |
| 50 Ω line / short | 4.058 | 50.7 | 2.580 | 32.3 | no added filter |
| 50 Ω ∥ 0.1 nF / short | 3.200 | 40.0 | 2.035 | 25.4 | A-side low-pass corner 31.8 MHz |
| 50 Ω ∥ 1 nF / short | 0.465 | 5.8 | 0.296 | 3.7 | A-side low-pass corner 3.18 MHz |
| 50 Ω ∥ 10 nF / short | 0.0464 | 0.58 | 0.0295 | 0.37 | A-side low-pass corner 0.318 MHz |
| 50 Ω ∥ 1 nF / 1 nF, 0 % mismatch | 0.0534 | 0.67 | 0.0340 | 0.42 | A-side low-pass corner 3.18 MHz |
| same, 5 % mismatch | 0.0556 | 0.69 | 0.0353 | 0.44 | A-side low-pass corner 3.18 MHz |
| same, 10 % mismatch | 0.0646 | 0.81 | 0.0411 | 0.51 | A-side low-pass corner 3.18 MHz |
| same, 20 % mismatch | 0.0899 | 1.12 | 0.0572 | 0.71 | A-side low-pass corner 3.18 MHz |
| 50 Ω ∥ 10 nF / 10 nF, 0 % mismatch | 0.0005 | 0.01 | 0.0003 | 0.00 | A-side low-pass corner 0.318 MHz |
| same, 5 % mismatch | 0.0023 | 0.03 | 0.0014 | 0.02 | A-side low-pass corner 0.318 MHz |
| same, 10 % mismatch | 0.0042 | 0.05 | 0.0027 | 0.03 | A-side low-pass corner 0.318 MHz |
| same, 20 % mismatch | 0.0077 | 0.10 | 0.0049 | 0.06 | A-side low-pass corner 0.318 MHz |
| 50 Ω ∥ series L-C trap (100 pF, 0.5 Ω) at 28 MHz, nominal | 0.0403 | 0.50 | 0.0257 | 0.32 | \|Z_trap\| 524 Ω at 3 MHz, 139 Ω at 10 MHz, 0.5 Ω at 28 MHz |
| same, L −5 % | 0.2336 | 2.92 | 0.1486 | 1.86 | \|Z_trap\| 2.9 Ω at 28 MHz |
| same, L +5 % | 0.2313 | 2.89 | 0.1471 | 1.84 | \|Z_trap\| 2.9 Ω at 28 MHz |
| 50 Ω / 50 Ω (differential), 0 % mismatch | 0.0 | 0.0 | 0.0 | 0.0 | no added filter |
| 50 Ω / 50 Ω, 5 % mismatch | 0.2002 | 2.5 | 0.1273 | 1.59 | no added filter |
| 50 Ω / 50 Ω, 10 % mismatch | 0.4001 | 5.0 | 0.2545 | 3.18 | no added filter |

- Switching current in the repo, two estimates. Sim 19 uses an 8 µA reference and a bracket of 8–20 µA (`I_LO`, `I_HI`; task spec, DESIGN_LOG step 26). [02_CRYOGENIC](../tests/02_CRYOGENIC.md), expected-numbers table: I_sw at about 5 K ≈ 8–9 µA (100 nm wire, scaled from Sedykh 2025; geometry audit). The same file flags the 8–20 µA range as [verify] and says the two ranges do not agree.
- Nanowire pickup from the 2-D model, [sim 10c](../../sim/out/10c_mirror_thickness/summary.json), `al100_inlaid`: direct pickup `E2.window.I_pk_uA` 0.959 µA, `E1.window.I_pk_uA` 1.915 µA. Extra through the mirror path, `E2.rho.3e-08.i_wire_upper_uA` 0.729 and `E2.rho.4e-08` 0.972 µA; `E1` 0.743 and 0.990 µA (rho keys as written in the file).
- Common-mode current collected by each slot lead, `E2.slot.I_lead_in_trap_uA` 44.53 µA and `E1` 28.61 µA.
- Lead-pair resistance up to 140 Ω changes the sim 19 currents by less than 6 % (DESIGN_LOG step 33).
- Bond-wire inductance 2 nH is [verify] in sim 19 (`L_BOND`). The trap L-C values (100 pF, 0.5 Ω) are task-spec [verify] (`C_TRAP`, `R_TRAP`).

## What each option changes elsewhere

- Carrier and bond diagram: [04_PACKAGING](../process/04_PACKAGING.md), "SNSPD RF termination: open" (line 79). The termination at SNS and SNG is the open item.
- Readout chain: [03_READOUT](../tests/03_READOUT.md), row "RF grounding / termination" (line 25). Its low-pass and notch filter rows are not chosen.
- Cold test b6 records the termination used for each run, and compares the switching current against RF amplitude: [02_CRYOGENIC](../tests/02_CRYOGENIC.md), b6 (line 35). Each lead termination in the table above would be a separate b6 condition.
- Transport waveform: a filter slows the move and changes n̄. [DESIGN_LOG step 34](../../DESIGN_LOG.md) (line 1416) and [step 40](../../DESIGN_LOG.md) (line 1615). Step 40 names the 100 kHz update rate as the commensurate case with the 0.8 MHz axial frequency.
- Centre-DC capacitor and the null: the Part 1 table. Adding a capacitor changes the readout null by the amounts in the table; no other file records a null shift with a filter.

## Not known

- Filter component values: none chosen. No filter decision is in `notes/decisions.md`.
- The lab's existing filter boards and DAC: unknown. [00_SETUP](../tests/00_SETUP.md), section 6, questions 2 and 4 (DC lines, filtering, amplifiers and notch filters); the DAC row of the equipment table.
- Bond-wire and lead inductance between each electrode and its capacitor: ignored in sim 23 [inference]. The 10 nF column is most affected.
- The 2-D models have no lead tips or segment ends (sim 19, sim 23, sim 10c limits).
- 3-D lead pickup on the SNSPD leads is not modelled: [OPEN_DECISIONS](../OPEN_DECISIONS.md), "Source and model checks".
- The switching current is an estimate: 8–9 µA is a team calculation, and 8–20 µA is [verify] ([02_CRYOGENIC](../tests/02_CRYOGENIC.md)).
- The outer-segment C_g is from an older stack's pad estimate, with 5 mm and 8 mm lead lengths as a bracket that is not measured from the GDS [verify].

## What would settle it

- Cold test b6: switching current against RF amplitude (0 to 70 V, 28 MHz), with the termination recorded for each run ([02_CRYOGENIC](../tests/02_CRYOGENIC.md), b6).
- Cold test b7: detector clicks with bias off, RF on and off ([02_CRYOGENIC](../tests/02_CRYOGENIC.md), b7).
- The bond diagram against the real carrier ([04_PACKAGING](../process/04_PACKAGING.md), "SNSPD RF termination: open").
- The answers to the lab questions in [00_SETUP](../tests/00_SETUP.md), section 6.

## Where to read

- [DESIGN_LOG step 42](../../DESIGN_LOG.md) (line 1668): sim 23, the Part 1 numbers and their limits.
- [DESIGN_LOG step 33](../../DESIGN_LOG.md) (line 1392): the lead-termination table and its model.
- [DESIGN_LOG step 34](../../DESIGN_LOG.md) (line 1416) and [step 40](../../DESIGN_LOG.md) (line 1615): the transport timing and the waveform numbers.
- [sim 23 docstring](../../sim/23_dc_rf_coupling.py) and [sim 19 docstring](../../sim/19_lead_termination.py): model, inputs and limits.
- [Primer section 5](../../primers/RF_PRIMER.md#5-capacitive-pickup), [section 6](../../primers/RF_PRIMER.md#6-filters-on-the-dc-lines), [section 7](../../primers/RF_PRIMER.md#7-the-snspd-as-a-circuit-and-its-readout-chain) and [section 8](../../primers/RF_PRIMER.md#8-grounding-and-return-current): the circuit ideas.
- [T2 bench-test note](../../research/research_notes/Test%20setup%202026-11/T2_snspd_bench_tests.md), section "Checked against the PDFs": Slichter 2017 Fig. 4 (the circuit figure with couplers for the cancellation tones); Hampel 2023 pages 2–3 (grounded mirror, low-pass and notch filtering).
- [03_READOUT](../tests/03_READOUT.md), "RF grounding / termination" row.
