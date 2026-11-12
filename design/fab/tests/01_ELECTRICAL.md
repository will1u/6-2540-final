> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09; run R1_ONE, raised mirror, and the new a20 check 2026-11-12 (the inlaid mirror and the R1_TRAP / R1_FULL test dies are superseded).

# Room temperature electrical tests

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

> [!warning] Draft limits and unresolved source
> The numerical limits below are draft **[verify]** values. “Dietl 2025” is M. Dietl et al., arXiv:2505.21284. Its Table 2 gives the 100 nA leakage pass limit at 50 V DC and 300 V (labelled RF in the paper). The paper's test uses 120 probe needles on loop electrodes with two bond pads each (its Sec. 3, page 6); an Au comb structure was not found in it, and no breakdown or flashover voltage is given. Reading pointers: [Dietl note](../../research/research_notes/Test%20setup%202026-11/T1_dietl_2025.md). The source of the limits is identified; see the [L2 source note](../../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md) (item I1). The limits themselves remain **[verify]**.

**When:** step 17 (wafer, before dicing) and again after packaging (step 19, through the carrier pins).
**Tool:** ProbeStation-Summit-11000 + SMUs.
**Pads:** trap-die pad names and coordinates from [trap_die_v4_A30_pads.csv](../../gds/trap_die_v4_A30_pads.csv) (TL/TR/BL/BR rows, RF, C, SNS, SNG, GND-1…4). The v4 trap dies have no M1 bond or probe pads. **R1_ONE:** there is no TEST or TEST_TRAP die. The SNSPD-only die (`snspd_die_v4`) carries the structures that remain (T3, T11 and the 8 detector cells D1 to D8), probed on its own pads; each cell has two Au bond pads (120 × 200 µm). Structures not drawn in R1_ONE are marked "not in R1_ONE" below, with what stands in for them.

**Safety rules for the SNSPD**

- Never put more than 1 V or 100 nA across the meander.
- During every high-voltage test, keep **SNSPD_S and SNSPD_G (pads SNS, SNG) tied together and grounded** [inference].
- Wear a grounded strap. Touch down with the SMU at 0 V.

## Run applicability

- **R1_ONE** (current run, 2026-11-12: one wafer, 3 × 3 block: 4 A30, 1 B60 spare, 2 SNSPD-only, 2 NODET; optional layer-50-only backup wafer):
  - **Trap dies (NODET, A30; B60 spare):** a1 and a2 on every trap die; a7 (SNS to SNG) and a8 and a19 on the A30 and B60 dies; a10 after packaging.
  - **NODET, extra:** a2 includes neighbouring-electrode leakage (the 5 µm gaps, the stand-in for a5); a20 on the wafer after the NbN etch.
  - **SNSPD-only die:** a6 (T3), a7 and a8 on each of D1 to D8, a12 (D1 to D8 as the dose array), a13 (on T11), a17 (T11).
  - **Not in R1_ONE:** a3 (T6), a5 (T1, stand-in above), a14 (T9), a15 (T2v), a16 (T10), a18 (T12). For each, the text below says what stands in for it.
- **R1_TRAP** (superseded by R1_ONE; no Al, no SNSPD): kept for the record. 6 NODET trap dies + 2 TEST_TRAP; a1 and a2 on the NODET dies; a3 (T6) and a5 (T1) on TEST_TRAP; a10 after packaging. a7, a8, a13, a15–a19 do not apply.
- **R1_FULL** (superseded by R1_ONE; 2 A30 + 2 B60 + 2 NODET + 2 TEST): a1, a2 and a10 (after packaging) on every trap die; a3 and a5 on the T6 and T1 structures of every die that carries them; a6, a12, a14 and a15–a18 on the test dies; a7 (T4 / T4b on test dies; SNS ↔ SNG on A30 and B60), a8 and a19 on A30 and B60 trap dies; a13 on the test dies (T10 / T11).
- a4 is retired in v4. a9 and a11 were retired earlier (v3 ITO tests).
- Current T9 controls use a14 and need individual resistance and cold switching-current records (T9 is not in R1_ONE); validation is part of [detector reconciliation](../OPEN_DECISIONS.md#detector-documents-and-generated-layouts).

## a1 RF leakage

**R1_ONE:** the A30, B60 and NODET trap dies only. The SNSPD-only die has no RF electrode.

**Pads:** RF ↔ Au ground fill (GND-1…4), RF ↔ C (centre DC), RF ↔ caps 33–36 (TL1, TR1, BL1, BR1), and the segments nearest the closed end of the RF U (17, 32: TR2, BR2). There is no RF ↔ mirror pad: the Al mirror lies under the centre window, not under the RF rails.

**Stimulus:** **300 V** [verify]. Dietl's Table 2 labels this test RF; the earlier version of this page wrote DC. Confirm the waveform and the instrument setting before the test.

**Pass:** **≤ 100 nA; run twice** (catches breakdown-induced shorts) [verify]

**Source:** Dietl 2025 (Table 2) [verify]

## a2 DC leakage

**Pads:** each DC pad ↔ both neighbours in its pad row, ↔ Au ground fill (GND-1…4). The mirror is not probed on trap dies; it is reached only through the fill and its on-chip via.

**R1_ONE:** on every finished NODET die, pad-to-pad leakage between neighbouring electrodes (the 5 µm gaps). This is the stand-in for a5 (T1 comb), which is not drawn in R1_ONE. Adjacent DC electrodes are measured pad to pad; the RF pad to a GND pad is measured as well. The pass limits below are still [verify].

**Stimulus:** **50 V** [verify]

**Pass:** **≤ 100 nA** [verify]; and **> 100 MΩ between every pair including the Au ground fill** [verify]. Note: at 50 V a pair at exactly 100 MΩ draws 0.5 µA, so the two limits cannot both be applied at 50 V. Confirm the voltage for the > 100 MΩ check before the test.

**Source:** Dietl 2025; Stick 2010

## a3 Continuity

**R1_ONE: not in R1_ONE** (T6 loop not drawn; it was on the retired TEST dies). No stand-in in R1_ONE: the trap electrodes have one pad each, so no pad-to-pad continuity is measured ([05_SIMPLER_TESTING.md](05_SIMPLER_TESTING.md) section 3.3). The old pads were:

**Pads:** T6 loop (test die, two pads; also on TEST_TRAP)

**Stimulus:** **1 mA**

**Pass:** **0–100 mV** (expect ~3 Ω, so ~3 mV [team calc])

**Source:** Dietl 2025 two-pad loop

## a4 Dielectric

**Retired in v4.** The v3 T2 Au / D2 / Al capacitor (0.8 × 0.8 mm Au plate on the 10 µm D2) no longer exists: there is no D2 in v4. Its replacement is [a15](#a15-dielectric-capacitor-t2v).

## a5 Gap leakage / redeposition

**R1_ONE: not drawn** (T1 Au comb). The stand-in is the pad-to-pad leakage on each finished NODET die, in [a2](#a2-dc-leakage). Limits below are [verify] and were written for the comb.

**Pads (old, R1_TRAP / R1_FULL):** T1 comb (test die, 5 µm gaps; also on TEST_TRAP)

**Stimulus:** 50 V (then 300 V on sacrificial dies only) [verify]

**Pass:** ≤ 100 nA [verify]

**Source:** Dietl 2025 (the comb itself is not in the paper, see the warning above); Sussex 2022 (redeposition)

## a6 NbN Rsq

**Pads:** T3 4-wire (test die)

**Stimulus:** ≤ 1 µA

**Pass:** Matches the step-7 value within 10 %

**Source:** –

## a7 Meander R

**Pads:** trap die SNS ↔ SNG (A30; B60 spare). **R1_ONE:** SNS ↔ SNG on each of the 8 cells D1 to D8 of the SNSPD-only die (pads D1_S … D8_G, probe station or wire bonded). The cells are the A30 detector, so the A30 value applies to each.

**Old (R1_FULL):** test die T4 (A30 meander) and T4b (B60 meander)

**Stimulus:** ≤ 1 V, ≤ 100 nA

**Pass:** ≈ 18 MΩ (A30) / 34 MΩ (B60) for the v3.1 130 nm meander at 400 Ω/sq [team calc, step 24; verify against the released layout]; **ΔR/R₀ ≤ 10 %** (Todaro saw 12–30 % rises)

**Lead correction (v4):** the SNSPD leads are now Au in the slot, so each lead adds series resistance that depends on the electrode option. Room temperature, bulk Au: one lead ≈ 69 Ω (E1) or ≈ 4 Ω (E2); the two leads in series ≈ 139 Ω (E1) or ≈ 8 Ω (E2) [team calc, sim 18]. Cold values depend on an unverified residual resistance ratio [verify]. Subtract the pair value from a 2-wire reading, or state it. Against 18 MΩ the pair is below 0.001 % (E1), so it does not change the pass/fail, but record which option the die has.

**Source:** Todaro Supp. "Trap fabrication"

## a8 SNSPD isolation

**Pads:** trap die: SNS + SNG tied ↔ GND-1…4 (Au ground fill). **R1_ONE, SNSPD-only die:** each SNSPD pad (D1_S … D8_G) ↔ GND, which measures the Au leads over the Al mirror through the SiO₂: 238 nm spacer plus 110 nm cap, 348 nm off the wires, and 160 ± 10 nm over the wires (HSQ 50 nm plus cap 110 nm). This check runs on every detector, so it also covers the twin-lead isolation that T12 measured. The leakage to the centre DC is [a19](#a19-snspd-lead-leakage-to-the-centre-dc).

**Old (R1_FULL):** test die (T4 / T4b): SNS + SNG tied ↔ the mirror probe pad, through the 238 nm SiO₂ spacer and 160 nm SiO₂ cap to the Al mirror.

**Stimulus:** ≤ 1 V

**Pass:** > 1 GΩ [verify for the v4 spacer and cap]

**Source:** – (the v3 check was to M1; the threshold is carried over)

## a10 RF capacitance (packaged only)

**R1_ONE:** the NODET and A30 dies, after packaging.

**Pads:** RF pin ↔ ground pins

**Stimulus:** LCR at 1 MHz

**Pass:** No single pass value. `sim/22` (DESIGN_LOG step 41) gives the chip alone as 2.59 pF (A30, E2) or 2.39 pF (A30, E1) when the Si acts as a dielectric, which is the cold case at 28 MHz. At 1 MHz and room temperature the Si conducts, so the reading lies between that value and about 23 pF (the Si taken as a grounded conductor under the SiO₂), plus the carrier [team calc, first-order]. Record the measured value and the frequency; a reading at a higher frequency, or cold, is the one that predicts the resonator frequency.

**Source:** Stick 2010 (7 pF trap + CPGA)

## a13 Ground link (step 22)

**Pads:** The v4 trap dies have no M1 bond pads, so the mirror cannot be probed directly on a trap die. The check is:
- **R1_ONE:** on the **SNSPD-only die**, through the T11 Au-to-Al via chain ([a17](#a17-au-to-al-via-chain-t11)). T10 (the four-point Al strip, [a16](#a16-al-mirror-strip-resistance-t10)) is not drawn; Al sheet resistance is measured by four-point on a co-loaded piece instead [verify which piece];
- (old, R1_FULL) on the **test die**, through the T10 strip (four-point) and the T11 Au-to-Al via chain;
- on a **trap die**, only indirectly, through the Au ground fill pads GND-1…4 and the fill-to-carrier bonds in step 19.

**Stimulus:** 10 mA, 2-wire (4-wire if two probes fit per pad) [carried from v3; verify for T11 and the co-loaded Al piece]

**Pass:** **[verify]**. The old **< 10 Ω** limit cannot be applied as written: the Al strip alone is **18.8–25.1 Ω** at 100 nm Al (`sim/10c`, DESIGN_LOG step 37) [team calc], before the via and probe contacts. That figure is a calculation for the T10 strip, which is not drawn in R1_ONE; it is not a measurement. Set the acceptance separately for the co-loaded Al sheet and the T11 chain.

If T11 reads open, or much higher than the expected chain, the candidates are AlF₃ or native Al₂O₃ left at the via floor, or a broken seed on the via sidewall [inference]. The Ar pre-clean in [process step 12 (E2)](../process/03_ELECTRODES.md) is the step that addresses the via floor.

**Source:** Hampel 2023 (mirror grounded through vias)

## a12 Dose array

**R1_ONE:** the 8 detector cells D1 to D8 on the SNSPD-only die, each cell's two pads (D1_S/D1_G … D8_S/D8_G). Layer-20 datatypes 1, 2, 3, 0 (D1 to D4) and 0, 5, 6, 7 (D5 to D8) give dose factors 0.80, 0.87, 0.93, 1.00, 1.00, 1.07, 1.13, 1.20. The trap dies use datatype 0 (nominal). Old: T8 D1–D7 (test die), each meander's two pads.

**Stimulus:** ≤ 1 V, ≤ 100 nA

**Pass:** R vs dose factor: R ∝ 1/width. Breaks (open) or bridges (low R) mark the usable dose window [team inference]

**Source:** [EBL job](../mask_list.md#2-ebl-job-for-layer-20-nbn)

## a14 Geometry array (step 24)

**R1_ONE: not in R1_ONE** (the T9 geometry array is a later run). No stand-in in R1_ONE; the cell-to-cell comparison is a12 (dose only).

**Pads (old, R1_FULL):** T9 slots (test die): each meander's two pads; each straight wire's two pads

**Stimulus:** ≤ 1 V, ≤ 100 nA

**Pass:** R matches squares × R_sq within 10 % (squares from the GDS). Open = break; low R = a bridge across a 60–70 nm gap. SEM the 130/200 and 140/200 slots and the turn ends [team inference]

**Source:** `gds/make_test_die.py` (T9 list)

The trap's DC electrodes have one pad each, so continuity on the trap dies is not tested directly. In R1_ONE, T6 and T12 are not drawn: the lead continuity stand-in is a8 on every detector, and the Al strip is four-point on a co-loaded piece. A broken lead shows up later as a missing DC response.

The v4 trap dies have no M1 pads. The Au ground fill is grounded to the Al mirror through the mirror via, so a fill probe in a1 and a2 checks the fill and its bonds, not the mirror itself.

## a15 Dielectric capacitor (T2v)

**R1_ONE: not drawn** (T2v capacitor). The isolation between the Au leads and the Al mirror through the SiO₂ is measured on every detector by [a8](#a8-snspd-isolation). The SiO₂ thickness is measured by ellipsometry on Si pieces co-loaded in each PECVD run [verify]. Off the wires that SiO₂ is 238 + 110 = 348 nm. The entries below are the old design, kept for the record.

**Pads (old):** T2v Au top plate (200 × 200 µm) and the T2v Au pad, as laid out in `test_die_v4.gds`. The 200 × 200 µm Au plate at (−2700, 400) is the top electrode; the 150 µm Au pad at (−2400, 400) reaches the Al bottom plate through a 100 µm layer-40 opening

**Dielectric (old, R1_FULL):** 238 nm PECVD SiO₂ spacer + 160 nm SiO₂ cap, about 0.40 µm total [team calc, sim 15b and step 26 values]. R1_ONE: 238 + 110 = 348 nm off the wires; 160 ± 10 nm over the wires.

**Stimulus:** C at 1 MHz [verify LCR availability]; leakage at 50 V [verify]

**Pass:** C ≈ 3.5 pF [team calc, for the 200 × 200 µm plate]; the value depends on the SiO₂ permittivity and the actual thickness, both [verify]. Leakage ≤ 100 nA [verify]

**Source:** Stick 2010; research report implication 28 (dielectric check, carried from the retired a4)

## a16 Al mirror strip resistance (T10)

**R1_ONE: not drawn** (T10 strip). Al sheet resistance is measured by four-point on a co-loaded piece [verify which piece]. The 18.8–25.1 Ω below is a calculated value for the old strip, not a measurement in R1_ONE.

**Pads (old):** T10 four-point on the Al mirror strip (40 µm wide, 2510 µm long; test die)

**Stimulus:** [verify] (four-point current not set in the notes)

**Pass:** **[verify].** Expected **18.8–25.1 Ω** at 100 nm Al (62.75 squares at 0.30–0.40 Ω/sq) [team calc] (`sim/10c`, DESIGN_LOG step 37). No acceptance is set. A higher value than expected points to a thin or discontinuous Al film or an over-etched via.

**Source:** DESIGN_LOG step 25 (mirror path); [STACK](../STACK.md) (v4 changes)

## a17 Au-to-Al via chain (T11)

**R1_ONE:** T11 is kept, at the centre of each SNSPD-only die, probed at the probe station. Its four openings are 100 × 100 µm (spec). **Pads:** T11 P1 ↔ P2 (Au pads), through four 100 µm Au-to-Al vias in series, with two Al segments and an Au strap between them (test die)

**Stimulus:** [verify]

**Pass:** **[verify].** No expected value is in the notes. Record the chain resistance and, once the witness is measured, the per-via contribution [verify].

**Source:** Hampel 2023 (mirror grounded through vias); [process step 12 (E2)](../process/03_ELECTRODES.md) (Ar pre-clean before the seed)

## a18 Lead continuity over the Al edge and lead-to-lead (T12)

**R1_ONE: not drawn** (T12). The stand-in is [a8](#a8-snspd-isolation) on every detector (SNSPD pad to GND through the SiO₂). Lead-to-lead and lead-to-Al leakage are not measured in R1_ONE.

**Pads (old):** T12 is two 5 µm Au lines, 5 µm apart, laid over an Al strip (test die). The lines are 2.7 mm long and run over a 2.3 mm Al strip, extending about 200 µm beyond each end of the strip. The Al is inlaid, so it is level with the SiO₂ beside it: the lines cross the planar edge of the strip, and there is no step to climb. Probe each line at both ends (continuity across the planar Al edge), line to line (lead-to-lead), and line to the Al strip (lead-to-Al).

**Stimulus:** [verify]. The a2 DC values (50 V, ≤ 100 nA) are a starting point only [verify].

**Pass:** **[verify]** for continuity, lead-to-lead leakage and lead-to-Al leakage.

**Source:** `gds/make_test_die.py` (T12 models the SNSPD leads in the trap's slot)

## a19 SNSPD-lead leakage to the centre DC

**R1_ONE:** the A30 dies (and the B60 spare). The lead-to-lead check on the trap die is not possible in R1_ONE, because the leads are in parallel with the meander there and T12 is not drawn.

**Pads:** SNS + SNG tied ↔ C (centre DC, electrode 2) on A30 and B60 trap dies. The leads are Au in the slot along the centre DC, so the leakage path is lateral over the SiO₂ cap [inference]. The other SNSPD leakage checks are [a8](#a8-snspd-isolation) (to the Au ground fill and the mirror) and [a18](#a18-lead-continuity-over-the-al-edge-and-lead-to-lead-t12) (lead-to-lead and lead-to-Al, on the test die). On the trap die the two SNSPD leads are in parallel with the meander, so the lead-to-lead check is only possible on the test die.

**Stimulus:** ≤ 10 V to C [verify]; ≤ 1 V on the SNSPD side

**Pass:** > 1 GΩ [verify; carried from the C leg of the v3 a8]

**Source:** – (new in v4)

### a20 NbN residue after the etch (step 7)

**When:** on the wafer, after the NbN etch (step 7), before the cap (step 8).

**Pads:** an open field of the wafer (no NbN drawn there), and a trap-only die position. Two probes, on the NbN layer, at the open field and at the trap-only die position.

**Why:** NbN left behind on the open field would sit under every electrode, and the electrodes would then short through it.

**Stimulus:** [verify] (the probe station's own voltage or current setting).

**Pass:** open circuit between the two probes at both positions. Numeric limit not set [verify].

**Source:** team rule, 2026-11-12 (new in R1_ONE).

**Order per die (R1_ONE):**
- A30 die, and the B60 spare: a7 → a8 → a19 → a2 → a1 (a10 after packaging).
- NODET die: a2 → a1 (a10 after packaging), with a20 on the wafer at step 7.
- SNSPD-only die: a6 → a7 → a12 → a8 → a13 → a17.

a3, a5, a14, a15, a16 and a18 are not in R1_ONE. Low-voltage SNSPD tests come first on every die.

**Record:** pass/fail per die ID of `gds/run_R1_ONE_map.csv` (the die map for this run: check the file exists before citing it [verify]), per-die ΔR/R₀, leakage values, the lead option (E1 or E2) of the die, the SNSPD-only die cells D1 to D8 with their dose factors, the T11 chain resistance, and the co-loaded Al sheet and SiO₂ thickness values.
