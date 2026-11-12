> **Claude-authored.** Which electrical tests could replace the wafer-level test for these dies, what each one catches and misses, 2026-11-10. Updated 2026-11-12 for run R1_ONE (the T-structures named below are not drawn in R1_ONE unless marked otherwise).

[Test plan](../test_plan.md) · [Setup](00_SETUP.md) · [Electrical tests](01_ELECTRICAL.md) · [Open decisions](../OPEN_DECISIONS.md)

# Can the testing be simpler than a wafer-level test?

## 1. Short answer

> **Yes for the trap-only die; partly for the detector dies.**
> - Dietl et al. built their wafer test for traps with buried routing, made 477 to a wafer: 120 needles, and every electrode a loop between two bond pads (Sec. 3, pages 6 to 8). The same section says optical inspection is enough for a single-layer trap. NODET is a single-layer trap.
> - Their continuity test cannot be copied: these dies have one pad per electrode, so no pad-to-pad measurement finds a broken trace (section 3.3). What carries over is the limits in their Table 2, which a1 to a3 already use as draft [verify] values.
> - For 8 dies, what probing every die before dicing buys is finding a short before a die is diced and bonded. Measuring pin to pin through the carrier finds the same shorts one packaging step later, without a probe station and without needle marks on the pads (section 4).
> - A30 and B60 have buried Al, buried NbN and a via. Those are checked by the SNS-to-SNG resistance on the trap die and by the test die's structures, so the test die still needs a probe station.
> - With only the trap cryostat, the detector can be tested with flood light and no ion, as Slichter 2017 and Hampel 2023 did (section 5).
> - No tier covers cold behaviour or breakdown margin. The page describes the tiers and does not choose one.

## 2. What the Dietl test is, and what transfers

Source for the Dietl column: [T1 note](../../research/research_notes/Test%20setup%202026-11/T1_dietl_2025.md) (read from the PDF). Pages and sections are as the note gives them.

| Feature | Dietl 2025 | This project | Carries over? |
|---|---|---|---|
| Electrical rather than optical testing | Optical inspection sees only the top metal layer, which is enough for single-layer traps. Electrical testing is preferred for multilayer traps because lower-layer defects are hidden (Sec. 3, page 6). | NODET has one Au layer, so optical inspection sees the whole electrode layer. A30 and B60 have buried Al, buried NbN and vias ([STACK.md](../STACK.md)). | Partly. The reasoning applies to A30 and B60, not to NODET. |
| Loop electrodes | Each electrode is a loop between two bond pads. Continuity is measured pad to pad through the electrode (Sec. 3, page 7; Fig. 2(a)). | One pad per electrode ([trap_die_v4_A30_pads.csv](../../gds/trap_die_v4_A30_pads.csv); [01_ELECTRICAL.md](01_ELECTRICAL.md), a14 text). | No |
| Needle damage | A needle dents the metal, so needles never touch an electrode (Sec. 3, page 7). | Trap pads are probed at step 17. The repo's rule is to probe one end of each pad and bond at the other ([04_PACKAGING.md](../process/04_PACKAGING.md) step 19). | No, as written. The repo probes pads that are bonded later. |
| Probe hardware | 120 probe needles with 40 µm tips, one per bond pad, at ambient pressure and 295 K (Sec. 3, page 6). | Manual probing planned ([RUNSHEET_R1_TRAP.md](../RUNSHEET_R1_TRAP.md) step 17, [verify]); probe station ProbeStation-Summit-11000 with SMUs ([01_ELECTRICAL.md](01_ELECTRICAL.md)). | No |
| Number of chips | 477 chips on a 200 mm wafer; 258 pass, 54 % (Sec. 3, pages 7 to 8). | R1_ONE: 9 dies in a 3 × 3 block (4 A30, 1 B60 spare, 2 SNSPD-only, 2 NODET) on one wafer. Earlier runs had 8 dies ([RUN_PLAN.md](../RUN_PLAN.md)). The full-wafer reference has 56 dies ([LAYOUT.md](../LAYOUT.md), resolved items A7). | No. Section 6 says what this changes. |
| Limits | Table 2, page 7: continuity 1 mA, pass 0 to 100 mV; DC leakage 50 V, pass 0 to 100 nA; RF leakage 300 V, pass 0 to 100 nA. | a1 (300 V), a2 (50 V) and a3 (1 mA, 0 to 100 mV) use the same values, marked [verify] ([01_ELECTRICAL.md](01_ELECTRICAL.md)). | Yes, as values. Their use for this project is [verify]. |
| Temperature | Room temperature only. The traps run cold (Sec. 5, page 10). | The trap runs cold, at about 5 K (team report, 2026-11-10) [verify]. | Yes. No room-temperature test covers cold behaviour. |
| A failure the wafer test did not prevent | After three cooldowns, two trapping sites stopped working. The cause was not assigned to the trap or the setup (Sec. 4.2, page 10). | Cold tests b1 to b10 ([02_CRYOGENIC.md](02_CRYOGENIC.md)) and trapping steps 2 to 12 ([04_TRAPPING.md](04_TRAPPING.md)). | Yes. This is a cold failure, outside what a room-temperature test covers. |
| DC filters | First-order RC filters with a 5 kHz corner, used when trapping (Sec. 4.2, page 9). | No filter chosen ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md), RF grounding and filters). | Not applicable. There is no filter to compare yet. |
| RF-to-DC coupling at crossings | 14 fF without a ground layer between the RF and DC lines, 0.6 fF with one (Sec. 2.1, page 4). | No ground plane under the RF rails in v4 ([CLAUDE.md](../../CLAUDE.md), local-mirror architecture). | Partly [inference]: the no-plane case is the 14 fF case. |

## 3. What can hide on these dies

### 3.1 Which features optical inspection can see

Layer order from [STACK.md](../STACK.md), section (a) to (c).

| Die | Visible under optical inspection (top) | Buried, not visible | Source |
|---|---|---|---|
| NODET (R1_TRAP) | Everything: one Au layer on thermal SiO₂ over high-resistivity Si. Electrodes, gaps, pads, ground fill and marks. | The Ti adhesion layer under the Au, and the SiO₂ below. The Au thickness shows only as a step [inference]. | [STACK.md](../STACK.md), section (c) |
| A30 and B60 | Au electrodes and pads; SNSPD leads in the slot; the window opening in the Au (30 × 30 µm on A30, 60 × 30 µm on B60). The NbN may show through the 160 nm cap inside the window [inference]. | The 100 nm Al mirror (raised, R1_ONE), under the 238 nm SiO₂ spacer; the NbN meander under the 160 nm cap outside the window; the Ti/Au contacts (L22) under the lead; the mirror ground via, which the Au ground fill covers. | [STACK.md](../STACK.md), sections (a) and (b); [LAYOUT.md](../LAYOUT.md), readout-zone table and its line on the mirror via |

### 3.2 Each buried feature and the electrical check for it

| Buried feature | Electrical check | What it covers | What it does not cover [inference] |
|---|---|---|---|
| Al mirror (100 nm, raised) | R1_ONE: four-point Al sheet on a co-loaded piece (T10 is not drawn); a13 through T11 on the SNSPD-only die; a8 on every detector (SNSPD pad to GND through the SiO₂) | Sheet resistance, and the link to the fill through T11 and the detectors | The trap die has no mirror probe pad ([01_ELECTRICAL.md](01_ELECTRICAL.md), a13). Its ground path is reached only through the fill pads GND-1 to 4, and a2 checks the fill, not the mirror. |
| Mirror ground via (layer 40) | a17 (T11 via chain) and a13, on the SNSPD-only die | The via contact of the SNSPD-only die | The trap die's own via. |
| NbN meander under the 160 nm cap | a7 (SNS to SNG on the trap die; each of the 8 cells on the SNSPD-only die), a6 (T3 bar), a12 (the 8 cells as the dose array). a14 (T9) is not in R1_ONE | Resistance and continuity of the meander path | A pinhole in the cap that shorts the NbN to the fill, the mirror or electrode 2. a8 (isolation to the fill or mirror pad, > 1 GΩ [verify]) and a19 (leads to C, > 1 GΩ [verify]) test that. |
| Ti/Au contacts (L22), Ti 5 / Au 50 nm in R1_ONE | a7 (the meander path runs through them). a18 (T12) is not in R1_ONE | Resistance of the path, in total | The contacts alone. a7 gives one total value. |
| SNSPD leads in the slot (Au, on top) | a7 (lead correction in [01_ELECTRICAL.md](01_ELECTRICAL.md)), a8 (SNSPD pad to GND, every detector) and a19 (leads to C) | Lead isolation over the SiO₂ to the fill and the mirror, on every detector. Lead-to-lead on T12 is not in R1_ONE | Lead-to-lead on the trap die. The two leads are in parallel with the meander there ([01_ELECTRICAL.md](01_ELECTRICAL.md), a19 text). |
| Spacer and cap dielectric | a8 (isolation of every detector through the SiO₂), and ellipsometry of the SiO₂ on Si pieces co-loaded in each PECVD run [verify]. a15 (T2v) is not in R1_ONE | The dielectric stack thickness and isolation at each detector | The dielectric on the trap die itself, beyond the detector pads. |

### 3.3 One pad per electrode

With one pad per electrode, a broken trace between a pad and its electrode cannot be found by a pad-to-pad measurement. The repo says the same for the trap dies: continuity is not tested directly there, and "a broken lead shows up later as a missing DC response" ([01_ELECTRICAL.md](01_ELECTRICAL.md), a14 text).

Two other points follow [inference]:
- a2 finds shorts between a pad and its neighbours or the fill. It does not find an open trace.
- Checks that could find an open trace: optical inspection of the trace on the top metal, which tier 0 uses; and, in the trap, the ion's response to that electrode (trapping steps 6 and 7 in [04_TRAPPING.md](04_TRAPPING.md)).

## 4. Tiers, least equipment first

Each tier is described. The page does not rank them or choose one.

| Tier | What you do | Equipment | Tests covered (IDs) | Catches | Misses | Risk to the die |
|---|---|---|---|---|---|---|
| 0 | Optical inspection of every die: top metal, pads, gaps and marks | Optical microscope; darkfield for Al hillocks ([process_checks.md](../process_checks.md), rows 0 and 3) | None | Defects visible in the top Au: bridges across gaps, missing metal, and chipping after dicing ([04_PACKAGING.md](../process/04_PACKAGING.md) step 18) | Anything under the top metal: the buried mirror, the meander, the contacts. No electrical result. Dietl makes the same point for single-layer traps (Sec. 3, page 6). | None beyond handling. |
| 1 | Package first (step 19), then measure pin to pin through the carrier at room temperature | A carrier that can be measured at room temperature (carrier open, [OPEN_DECISIONS.md](../OPEN_DECISIONS.md)); SMU; LCR for a10 | a1 and a2 (leakage through the carrier pins), a7 (meander resistance, R5), a10 (RF capacitance at 1 MHz). [04_PACKAGING.md](../process/04_PACKAGING.md) step 19 asks for pad-to-pad isolation and meander resistance; the IDs are matched to that wording [inference]. [01_ELECTRICAL.md](01_ELECTRICAL.md) line 10 says the test repeats after packaging but does not list the IDs. | Leakage between each electrode and the others, through the bond wires; meander resistance; RF capacitance | Any electrode without a carrier pin; the test structures unless they are also packaged (section 6, question 8 of [00_SETUP.md](00_SETUP.md)); all cold behaviour | The die is diced and bonded before the test. A die that fails costs a packaging cycle [inference]. |
| 2 | Probe station on the SNSPD-only die and its test structures only: T3, T11 and the 8 detector cells. Trap dies get tier 0 or tier 1. (R1_ONE. T1, T6, T10, T2v and T12 are not drawn; see the stand-ins in [01_ELECTRICAL.md](01_ELECTRICAL.md).) | Probe station and SMU | a6 (T3), a7 and a8 (cells), a12 (cells), a13 and a17 (T11) | Continuity and leakage of the structures that stand in for the trap's stack: NbN sheet resistance, Al strip resistance, the via chain, the dielectric capacitor and lead continuity over Al | Trap electrodes (not probed in this tier); the trap die's meander; the isolation of the trap die's SNSPD leads; cold behaviour. The cells' isolation (a8) is on the same die and is not in this tier's list. | Probe marks only on the SNSPD-only die. The trap dies carry none in this tier [inference]. |
| 3 | The current plan: probe every die before dicing | Probe station and SMU; LCR not needed in R1_ONE | a1, a2, a5 (as the NODET neighbour leakage), a6, a7, a8, a12, a13, a17, a19 and the a20 open-field check on the dies of R1_ONE ([01 Run applicability](01_ELECTRICAL.md#run-applicability)); a10 after packaging. a3, a14, a15, a16 and a18 are not in R1_ONE. [RUNSHEET_R1_TRAP.md](../RUNSHEET_R1_TRAP.md) step 17 applies a1, a2, a3 and a5 only. | Shorts and leakage between electrodes, pads and the fill at the wafer; meander resistance and isolation; test-structure values | Cold behaviour ([Dietl Sec. 5](../../research/research_notes/Test%20setup%202026-11/T1_dietl_2025.md), page 10); breakdown margin at operating RF; one open pad-to-electrode trace (section 3.3); buried defects beyond the test structures | Probe marks on every trap pad. [04_PACKAGING.md](../process/04_PACKAGING.md) step 19 says to probe one end and bond the other, because step 17 probe marks can hide pad damage [inference]. SNSPD: never more than 1 V or 100 nA across the meander ([01_ELECTRICAL.md](01_ELECTRICAL.md), safety rules). a1 at 300 V; a5 at 300 V only on sacrificial dies. A bad die found only after dicing and bonding costs a packaging cycle [inference]. |

## 5. SNSPD checks with only the trap cryostat

Ordered from least to most equipment. Every test ID is from [01_ELECTRICAL.md](01_ELECTRICAL.md) or [02_CRYOGENIC.md](02_CRYOGENIC.md).

| Check | Test ID | Needs | What it tells you | What it does not tell you | Source |
|---|---|---|---|---|---|
| Room-temperature meander resistance | a7 | SMU at ≤ 1 V and ≤ 100 nA; probe station (test die) or carrier (packaged) | The meander is continuous, and its resistance is near the team's estimate (≈ 18 MΩ on A30, 34 MΩ on B60 at 400 Ω/sq, [verify]); ΔR/R₀ against the room-temperature value, limit ≤ 10 % | Whether the detector switches cold. The T3 note found no readable source in which room-temperature resistance screens NbN meanders or predicts the cold switching current at 4 to 5 K. It names this as an open gap, not a finding ([T3 note](../../research/research_notes/Test%20setup%202026-11/T3_electrical_screening.md), Sec. 2). | [01_ELECTRICAL.md](01_ELECTRICAL.md), a7 |
| Resistance through Tc during cooldown | b1 | Two DC lines and a thermometer in the trap cryostat | Tc of the meander and of T3. The repo expects Tc ≈ 7.8 to 8 K ([02_CRYOGENIC.md](02_CRYOGENIC.md), expected numbers). | The switching current or the usable bias. A wire that goes superconducting at the expected Tc may still not switch at the expected current [inference]. | [02_CRYOGENIC.md](02_CRYOGENIC.md), b1 |
| I–V and switching current, RF off | b2 | Bias through the bias tee's DC port (readout chain); thermometer | I_sw against temperature from base to 7 K; latching current | Count rate, efficiency, and the RF effect (b6). Slichter 2017 (Sec. 4, Fig. 6) and Todaro 2021 (Fig. 2) are the pointers for this measurement ([T2 note](../../research/research_notes/Test%20setup%202026-11/T2_snspd_bench_tests.md), [verify]). | [02_CRYOGENIC.md](02_CRYOGENIC.md), b2 |
| Pulses and count rate under flood light, with no ion; dark counts with light off | b3, b4, b5 | Readout chain; oscilloscope after the amplifier (b3); 493 nm flood through a window or fibre (b4); no light (b5) | Pulse shape and τ, hence L_k (b3); the bias plateau under light (b4); the dark-count rate (b5) | The ion's photon rate or crosstalk. Two groups tested detectors on trap chips this way, with LED flood light and no ion: Slichter 2017 (308 nm LED on the cold stage; Sec. 4 and Fig. 4) and Hampel 2023 (cryogenic 395 nm LEDs; pages 2 to 3). Both were checked against the PDF. Todaro 2021 used 313 nm beams with an ion [verify]. None used 493 nm. | [02_CRYOGENIC.md](02_CRYOGENIC.md), b3 to b5; [T2 note](../../research/research_notes/Test%20setup%202026-11/T2_snspd_bench_tests.md) (Slichter 2017 Sec. 4; Hampel 2023 measurements section, Fig. 3; Todaro 2021 Fig. 2) |
| RF on and off | b6, b7, b8 | RF generator and resonator; light for the b4 and b6 curves; DC lines and thermometer for b8 | I_sw against V_RF (0 to 70 V at 28 MHz); clicks with bias off; ΔT from the I_sw recovery | Breakdown margin; the effect of the termination at SNS and SNG, which is an open decision ([OPEN_DECISIONS.md](../OPEN_DECISIONS.md)); the RF voltage at the ion | [02_CRYOGENIC.md](02_CRYOGENIC.md), b6 to b8; Todaro 2021 Fig. 3 and Supp. Fig. S4; Hampel 2023 Figs. 3 to 4 ([T2 note](../../research/research_notes/Test%20setup%202026-11/T2_snspd_bench_tests.md), [verify]) |
| With an ion | Trapping checklist, steps 5 to 12 | Everything above, plus the trapping lasers | Counts with the ion; crosstalk along the axis (step 8); micromotion (step 9); heating (step 12) | Anything that needs no ion. The rows above come first. | [04_TRAPPING.md](04_TRAPPING.md) |

## 6. What a simpler plan gives up

- **Statistics over many dies.** R1_ONE has 9 dies on one wafer; earlier runs had 8 ([RUN_PLAN.md](../RUN_PLAN.md)). Dietl's yield and failure-pattern figures come from 477 chips (T1 note, Sec. 3, pages 7 to 8). A tier with fewer tests gives fewer numbers per die [inference].
- **Finding a leak before spending a package.** Tier 2 does not test trap electrodes. A leak between two trap electrodes is found only in tier 3 (before dicing) or tier 1 (after packaging and bonding) [inference].
- **Cold behaviour.** No tier here tests cold behaviour. This is true of every tier at room temperature (Dietl Sec. 5, page 10). Dietl also reports a failure after three cooldowns that the wafer test did not prevent (Sec. 4.2, page 10).
- **Breakdown margin at the operating RF voltage.** No tier measures it. The operating amplitude is 53 V at 28 MHz, and b6 sweeps to 70 V ([02_CRYOGENIC.md](02_CRYOGENIC.md)). The only RF-voltage test is a1 at 300 V, which Dietl chose to stay below breakdown through air (T1 note, Sec. 3, page 7). That is a pass criterion, not a margin. In R1_ONE the T1 comb is not drawn; the 5 µm gaps are checked pad to pad on the finished NODET die (a2, the a5 stand-in). The T3 note says the flashover data it found (Sterling 2013, gold on quartz in vacuum, gaps of 3 to 15 µm [verify]) does not cover this geometry.
- **Opens between a pad and its electrode.** Pad-to-pad measurements do not find them (section 3.3).
- **Switching current from room temperature.** A room-temperature meander value does not predict the cold switching current in any source the repo has read (section 5; [T3 note](../../research/research_notes/Test%20setup%202026-11/T3_electrical_screening.md), Sec. 2).

## 7. Where to read

- [T1 note: Dietl 2025, what the wafer test is](../../research/research_notes/Test%20setup%202026-11/T1_dietl_2025.md), read from the PDF.
- [T2 note: how trap-integrated SNSPDs were tested](../../research/research_notes/Test%20setup%202026-11/T2_snspd_bench_tests.md). Read through a summarising tool; every number is [verify].
- [T3 note: electrical checks on traps and screening SNSPDs](../../research/research_notes/Test%20setup%202026-11/T3_electrical_screening.md). Read through a summarising tool; every number is [verify].
- [01_ELECTRICAL.md](01_ELECTRICAL.md): the tests, their limits and the run applicability.
- [00_SETUP.md](00_SETUP.md): the equipment and wiring for each device.
