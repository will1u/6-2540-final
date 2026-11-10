> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Room temperature electrical tests

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

> [!warning] Draft limits and unresolved source
> The numerical limits below are draft **[verify]** values. “Dietl 2025” is M. Dietl et al., arXiv:2505.21284. Its Table 2 gives the 100 nA leakage pass limit at 50 V DC and 300 V (labelled RF in the paper). The paper's test uses 120 probe needles on loop electrodes with two bond pads each (its Sec. 3, page 6); an Au comb structure was not found in it, and no breakdown or flashover voltage is given. Reading pointers: [Dietl note](../../research/research_notes/Test%20setup%202026-11/T1_dietl_2025.md). The source of the limits is identified; see the [L2 source note](../../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md) (item I1). The limits themselves remain **[verify]**.

**When:** step 17 (wafer, before dicing) and again after packaging (step 19, through the carrier pins).
**Tool:** ProbeStation-Summit-11000 + SMUs.
**Pads:** trap-die pad names and coordinates from [trap_die_v4_A30_pads.csv](../../gds/trap_die_v4_A30_pads.csv) (TL/TR/BL/BR rows, RF, C, SNS, SNG, GND-1…4). The v4 trap dies have no M1 bond or probe pads. Test-die structures are probed on their own pads; the test dies stand in for the trap dies of their run. TEST_TRAP carries T1 and T6 only.

**Safety rules for the SNSPD**

- Never put more than 1 V or 100 nA across the meander.
- During every high-voltage test, keep **SNSPD_S and SNSPD_G (pads SNS, SNG) tied together and grounded** [inference].
- Wear a grounded strap. Touch down with the SMU at 0 V.

## Run applicability

- **R1_TRAP** (6 NODET trap dies + 2 TEST_TRAP; no Al, no SNSPD): a1 and a2 on the NODET dies; a3 (T6) and a5 (T1) on TEST_TRAP; a10 after packaging. a7, a8, a13, a15–a19 do not apply (no Al, no SNSPD leads on the NODET dies, no T2v/T10–T12 on TEST_TRAP).
- **R1_FULL** (2 A30 + 2 B60 + 2 NODET + 2 TEST): a1, a2 and a10 (after packaging) on every trap die; a3 and a5 on the T6 and T1 structures of every die that carries them; a6, a12, a14 and a15–a18 on the test dies; a7 (T4 / T4b on test dies; SNS ↔ SNG on A30 and B60), a8 and a19 on A30 and B60 trap dies; a13 on the test dies (T10 / T11).
- a4 is retired in v4. a9 and a11 were retired earlier (v3 ITO tests).
- Current T9 controls use a14 and need individual resistance and cold switching-current records; validation is part of [detector reconciliation](../OPEN_DECISIONS.md#detector-documents-and-generated-layouts).

## a1 RF leakage

**Pads:** RF ↔ Au ground fill (GND-1…4), RF ↔ C (centre DC), RF ↔ caps 33–36 (TL1, TR1, BL1, BR1), and the segments nearest the closed end of the RF U (17, 32: TR2, BR2). There is no RF ↔ mirror pad: the Al mirror lies under the centre window, not under the RF rails.

**Stimulus:** **300 V** [verify]. Dietl's Table 2 labels this test RF; the earlier version of this page wrote DC. Confirm the waveform and the instrument setting before the test.

**Pass:** **≤ 100 nA; run twice** (catches breakdown-induced shorts) [verify]

**Source:** Dietl 2025 (Table 2) [verify]

## a2 DC leakage

**Pads:** each DC pad ↔ both neighbours in its pad row, ↔ Au ground fill (GND-1…4). The mirror is not probed on trap dies; it is reached only through the fill and its on-chip via.

**Stimulus:** **50 V** [verify]

**Pass:** **≤ 100 nA** [verify]; and **> 100 MΩ between every pair including the Au ground fill** [verify]. Note: at 50 V a pair at exactly 100 MΩ draws 0.5 µA, so the two limits cannot both be applied at 50 V. Confirm the voltage for the > 100 MΩ check before the test.

**Source:** Dietl 2025; Stick 2010

## a3 Continuity

**Pads:** T6 loop (test die, two pads; also on TEST_TRAP)

**Stimulus:** **1 mA**

**Pass:** **0–100 mV** (expect ~3 Ω, so ~3 mV [team calc])

**Source:** Dietl 2025 two-pad loop

## a4 Dielectric

**Retired in v4.** The v3 T2 Au / D2 / Al capacitor (0.8 × 0.8 mm Au plate on the 10 µm D2) no longer exists: there is no D2 in v4. Its replacement is [a15](#a15-dielectric-capacitor-t2v).

## a5 Gap leakage / redeposition

**Pads:** T1 comb (test die, 5 µm gaps; also on TEST_TRAP)

**Stimulus:** 50 V (then 300 V on sacrificial dies only) [verify]

**Pass:** ≤ 100 nA [verify]

**Source:** Dietl 2025 (the comb itself is not in the paper, see the warning above); Sussex 2022 (redeposition)

## a6 NbN Rsq

**Pads:** T3 4-wire (test die)

**Stimulus:** ≤ 1 µA

**Pass:** Matches the step-7 value within 10 %

**Source:** –

## a7 Meander R

**Pads:** trap die SNS ↔ SNG; test die T4 (A30 meander) and T4b (B60 meander)

**Stimulus:** ≤ 1 V, ≤ 100 nA

**Pass:** ≈ 18 MΩ (A30) / 34 MΩ (B60) for the v3.1 130 nm meander at 400 Ω/sq [team calc, step 24; verify against the released layout]; **ΔR/R₀ ≤ 10 %** (Todaro saw 12–30 % rises)

**Lead correction (v4):** the SNSPD leads are now Au in the slot, so each lead adds series resistance that depends on the electrode option. Room temperature, bulk Au: one lead ≈ 69 Ω (E1) or ≈ 4 Ω (E2); the two leads in series ≈ 139 Ω (E1) or ≈ 8 Ω (E2) [team calc, sim 18]. Cold values depend on an unverified residual resistance ratio [verify]. Subtract the pair value from a 2-wire reading, or state it. Against 18 MΩ the pair is below 0.001 % (E1), so it does not change the pass/fail, but record which option the die has.

**Source:** Todaro Supp. "Trap fabrication"

## a8 SNSPD isolation

**Pads:** trap die: SNS + SNG tied ↔ GND-1…4 (Au ground fill). Test die (T4 / T4b): SNS + SNG tied ↔ the mirror probe pad, through the 238 nm SiO₂ spacer and 160 nm SiO₂ cap to the Al mirror. The leakage to the centre DC is [a19](#a19-snspd-lead-leakage-to-the-centre-dc).

**Stimulus:** ≤ 1 V

**Pass:** > 1 GΩ [verify for the v4 spacer and cap]

**Source:** – (the v3 check was to M1; the threshold is carried over)

## a10 RF capacitance (packaged only)

**Pads:** RF pin ↔ ground pins

**Stimulus:** LCR at 1 MHz

**Pass:** No single pass value. `sim/22` (DESIGN_LOG step 41) gives the chip alone as 2.59 pF (A30, E2) or 2.39 pF (A30, E1) when the Si acts as a dielectric, which is the cold case at 28 MHz. At 1 MHz and room temperature the Si conducts, so the reading lies between that value and about 23 pF (the Si taken as a grounded conductor under the SiO₂), plus the carrier [team calc, first-order]. Record the measured value and the frequency; a reading at a higher frequency, or cold, is the one that predicts the resonator frequency.

**Source:** Stick 2010 (7 pF trap + CPGA)

## a13 Ground link (step 22)

**Pads:** The v4 trap dies have no M1 bond pads, so the mirror cannot be probed directly on a trap die. The check is:
- on the **test die**, through the T10 strip (four-point) and the T11 Au-to-Al via chain; see [a16](#a16-al-mirror-strip-resistance-t10) and [a17](#a17-au-to-al-via-chain-t11);
- on a **trap die**, only indirectly, through the Au ground fill pads GND-1…4 and the fill-to-carrier bonds in step 19.

**Stimulus:** 10 mA, 2-wire (4-wire if two probes fit per pad) [carried from v3; verify for T10]

**Pass:** **[verify]**. The old **< 10 Ω** limit cannot be applied as written: the Al strip alone is **18.8–25.1 Ω** at 100 nm Al (`sim/10c`, DESIGN_LOG step 37) [team calc], before the via and probe contacts. Set the acceptance separately for the T10 strip and the T11 chain.

If T11 reads open, or much higher than the expected chain, the candidates are AlF₃ or native Al₂O₃ left at the via floor, or a broken seed on the via sidewall [inference]. The Ar pre-clean in [process step 12 (E2)](../process/03_ELECTRODES.md) is the step that addresses the via floor.

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

The trap's DC electrodes have one pad each, so continuity on the trap dies is not tested directly. Continuity is tested on T6 (test die), and the lead and Al-strip continuity on T11 and T12. A broken lead shows up later as a missing DC response.

The v4 trap dies have no M1 pads. The Au ground fill is grounded to the Al mirror through the mirror via, so a fill probe in a1 and a2 checks the fill and its bonds, not the mirror itself.

## a15 Dielectric capacitor (T2v)

**Pads:** T2v Au top plate (200 × 200 µm) and the T2v Au pad, as laid out in `test_die_v4.gds`. The 200 × 200 µm Au plate at (−2700, 400) is the top electrode; the 150 µm Au pad at (−2400, 400) reaches the Al bottom plate through a 100 µm layer-40 opening

**Dielectric:** 238 nm PECVD SiO₂ spacer + 160 nm SiO₂ cap, about 0.40 µm total [team calc, sim 15b and step 26 values]

**Stimulus:** C at 1 MHz [verify LCR availability]; leakage at 50 V [verify]

**Pass:** C ≈ 3.5 pF [team calc, for the 200 × 200 µm plate]; the value depends on the SiO₂ permittivity and the actual thickness, both [verify]. Leakage ≤ 100 nA [verify]

**Source:** Stick 2010; research report implication 28 (dielectric check, carried from the retired a4)

## a16 Al mirror strip resistance (T10)

**Pads:** T10 four-point on the Al mirror strip (40 µm wide, 2510 µm long; test die)

**Stimulus:** [verify] (four-point current not set in the notes)

**Pass:** **[verify].** Expected **18.8–25.1 Ω** at 100 nm Al (62.75 squares at 0.30–0.40 Ω/sq) [team calc] (`sim/10c`, DESIGN_LOG step 37). No acceptance is set. A higher value than expected points to a thin or discontinuous Al film or an over-etched via.

**Source:** DESIGN_LOG step 25 (mirror path); [STACK](../STACK.md) (v4 changes)

## a17 Au-to-Al via chain (T11)

**Pads:** T11 P1 ↔ P2 (Au pads), through four 100 µm Au-to-Al vias in series, with two Al segments and an Au strap between them (test die)

**Stimulus:** [verify]

**Pass:** **[verify].** No expected value is in the notes. Record the chain resistance and, once the witness is measured, the per-via contribution [verify].

**Source:** Hampel 2023 (mirror grounded through vias); [process step 12 (E2)](../process/03_ELECTRODES.md) (Ar pre-clean before the seed)

## a18 Lead continuity over the Al edge and lead-to-lead (T12)

**Pads:** T12 is two 5 µm Au lines, 5 µm apart, laid over an Al strip (test die). The lines are 2.7 mm long and run over a 2.3 mm Al strip, extending about 200 µm beyond each end of the strip. The Al is inlaid, so it is level with the SiO₂ beside it: the lines cross the planar edge of the strip, and there is no step to climb. Probe each line at both ends (continuity across the planar Al edge), line to line (lead-to-lead), and line to the Al strip (lead-to-Al).

**Stimulus:** [verify]. The a2 DC values (50 V, ≤ 100 nA) are a starting point only [verify].

**Pass:** **[verify]** for continuity, lead-to-lead leakage and lead-to-Al leakage.

**Source:** `gds/make_test_die.py` (T12 models the SNSPD leads in the trap's slot)

## a19 SNSPD-lead leakage to the centre DC

**Pads:** SNS + SNG tied ↔ C (centre DC, electrode 2) on A30 and B60 trap dies. The leads are Au in the slot along the centre DC, so the leakage path is lateral over the SiO₂ cap [inference]. The other SNSPD leakage checks are [a8](#a8-snspd-isolation) (to the Au ground fill and the mirror) and [a18](#a18-lead-continuity-over-the-al-edge-and-lead-to-lead-t12) (lead-to-lead and lead-to-Al, on the test die). On the trap die the two SNSPD leads are in parallel with the meander, so the lead-to-lead check is only possible on the test die.

**Stimulus:** ≤ 10 V to C [verify]; ≤ 1 V on the SNSPD side

**Pass:** > 1 GΩ [verify; carried from the C leg of the v3 a8]

**Source:** – (new in v4)

**Order per die:**
- Trap die: a7 → a8 → a19 → a2 → a1 (a10 after packaging).
- Test die: a7 → a12 → a14 → a6 → a3 → a16 → a17 → a13 → a18 → a15 → a5.

Low-voltage SNSPD tests come first on every die.

**Record:** pass/fail per die ID of `gds/run_<name>_map.csv`, per-die ΔR/R₀, leakage values, the lead option (E1 or E2) of the die, and the measured resistances of T10 and T11.
