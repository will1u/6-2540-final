> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Room temperature electrical tests

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

> [!warning] Draft limits and detector revision
> “Dietl 2025” is an unresolved attribution; its numerical limits below are **[verify]**. The updated a7 and a14 values are v3.1 estimates to validate against the released GDS and witness measurements.

**When:** step 17 (wafer, before dicing) and again after packaging (step 19, through the carrier pins).
**Tool:** ProbeStation-Summit-11000 + SMUs.
**Draft reference [verify]:** the earlier sheet attributes a 120-needle card to “Dietl 2025”; that source remains unresolved. The tests here assume manual probing.
**Pads:** trap-die pad names and coordinates from [trap_die_v3_A30_pads.csv](../../gds/trap_die_v3_A30_pads.csv) (TL/TR/BL/BR rows, RF, C, SNS, SNG, GND-n, M1-n). Test-die structures are probed on their own pads; the test dies stand in for the trap dies of their run.

**Safety rules for the SNSPD**

- Never put more than 1 V or 100 nA across the meander.
- During every high-voltage test, keep **SNSPD_S and SNSPD_G (pads SNS, SNG) tied together and grounded** [inference].
- Wear a grounded strap. Touch down with the SMU at 0 V.

## Run applicability

R1_TRAP uses a1–a5 and a13, plus a10 after packaging. Detector dies add a6–a8/a12 where present. a9/a11 are retired ITO tests. Current T9 controls use a14 and need individual resistance and cold switching-current records; validation is part of [detector reconciliation](../OPEN_DECISIONS.md#detector-documents-and-generated-layouts).

## a1 RF leakage

**Pads:** RF ↔ M1 (any M1-n), RF ↔ Au ground fill (GND-n), RF ↔ C (centre DC), RF ↔ caps 33–36 (TL1, TR1, BL1, BR1) and the segments nearest the closed end of the RF U (17, 32: TR2, BR2)

**Stimulus:** **300 V DC**

**Pass:** **≤ 100 nA; run twice** (catches breakdown-induced shorts)

**Source:** Dietl 2025

## a2 DC leakage

**Pads:** each DC pad ↔ both neighbours in its pad row, ↔ M1, ↔ ground fill

**Stimulus:** **50 V**

**Pass:** **≤ 100 nA**; and **> 100 MΩ between every pair including the ground plane**

**Source:** Dietl 2025; Stick 2010

## a3 Continuity

**Pads:** T6 loop (test die, two pads)

**Stimulus:** **1 mA**

**Pass:** **0–100 mV** (expect ~3 Ω, so ~3 mV [team calc])

**Source:** Dietl 2025 two-pad loop

## a4 Dielectric

**Pads:** T2 Au/D2/M1 capacitor (test die, 0.8 × 0.8 mm Au plate ↔ M1 pad)

**Stimulus:** C at 1 MHz [verify LCR availability]; leakage at 50 V

**Pass:** C ≈ 2.1 pF [team calc]; ≤ 100 nA

**Source:** Stick 2010; research report implication 28

## a5 Gap leakage / redeposition

**Pads:** T1 comb (test die, 5 µm gaps)

**Stimulus:** 50 V (then 300 V on sacrificial dies only)

**Pass:** ≤ 100 nA

**Source:** Dietl 2025; Sussex 2022 (redeposition)

## a6 NbN Rsq

**Pads:** T3 4-wire (test die)

**Stimulus:** ≤ 1 µA

**Pass:** Matches the step-7 value within 10 %

**Source:** –

## a7 Meander R

**Pads:** trap die SNS ↔ SNG; test die T4 (A30 meander) and T4b (B60 meander)

**Stimulus:** ≤ 1 V, ≤ 100 nA

**Pass:** ≈ 18 MΩ (A30) / 34 MΩ (B60) for the v3.1 130 nm meander at 400 Ω/sq [team calc, step 24]; **ΔR/R₀ ≤ 10 %** (Todaro saw 12–30 % rises)

**Source:** Todaro Supp. "Trap fabrication"

## a8 SNSPD isolation

**Pads:** SNS + SNG tied ↔ M1; ↔ C

**Stimulus:** ≤ 1 V to M1; ≤ 10 V to C [verify]

**Pass:** > 1 GΩ

**Source:** –

## a10 RF capacitance (packaged only)

**Pads:** RF pin ↔ ground pins

**Stimulus:** LCR at 1 MHz

**Pass:** A few pF from the chip [team calc from DESIGN_LOG step 10: 0.36 pF/mm per rail], plus the carrier. Record it to predict the resonator frequency

**Source:** Stick 2010 (7 pF trap + CPGA)

## a13 Ground link (step 22)

**Pads:** each GND-n ↔ the nearest M1-n (trap die; the Au fill and M1 are one net through the eight fill-to-M1 vias)

**Stimulus:** 10 mA, 2-wire (4-wire if two probes fit per pad)

**Pass:** **< 10 Ω** 2-wire, probe contacts included. Expect ≲ 1 Ω: one Al square at ~0.3 Ω/sq plus the via contacts [team calc; contact resistance unknown, verify on W3]. Open or ≫ 10 Ω means AlF₃ / native oxide left at the via floor, or a broken seed on the via sidewall. The die is still usable with an M1 bond (step 19)

**Source:** Hampel 2023 (mirror grounded through vias)

## a12 Dose array

**Pads:** T8 D1–D7 (test die), each meander's two pads

**Stimulus:** ≤ 1 V, ≤ 100 nA

**Pass:** R vs dose factor: R ∝ 1/width. Breaks (open) or bridges (low R) mark the usable dose window [team inference]

**Source:** [EBL job](../mask_list.md#2-ebl-job-for-layer-20-nbn)

## a14 Geometry array (step 24)

**Pads:** T9 slots (test die): each meander's two pads; each straight wire's two pads

**Stimulus:** ≤ 1 V, ≤ 100 nA

**Pass:** R matches squares × R_sq within 10 % (squares from the GDS). Open = break; low R = a bridge across a 60–70 nm gap. SEM the 130/200 and 140/200 slots and the turn ends [team inference]

**Source:** `gds/make_test_die.py` (T9 list)

The trap's DC electrodes have one pad each (no Dietl loop), so continuity is only tested on T6 (test die). A broken lead shows up later as a missing DC response.

Since step 22, M1 and the Au ground fill are one net on chip, so in a1 and a2 "↔ M1" and "↔ ground fill" are the same measurement; probing both still checks the vias.

**Order per die:** trap die a7 → a8 → a13 → a2 → a1 (a10 after packaging); test die a7 → a12 → a14 → a6 → a3 → a4 → a5. Low-voltage SNSPD tests come first.

**Record:** pass/fail per die ID of `gds/run_<name>_map.csv`, per-die ΔR/R₀, leakage values.
