> Claude-authored research notes (design/research). Not a substitute for reading the cited sections and figures.

# RF tolerance and RF pickup of trap-integrated SNSPDs: mechanisms, geometry, and an audit of the A30/B60 detector

Scope: goes beyond the earlier report (`reports/Trap integrated SNSPD design.md`) and the notes in `research_notes/Trap integrated SNSPD design/`. Those already cover the Todaro 2021 circuit model (I0 / I1 split), Slichter 2017 (cancellation tone), the Hampel 2023 stack, and Eltony 2013 ITO. They are not repeated here except where a new number or figure reading is needed.

Tags: **[team calc]** = computed for these notes; **[team reading]** = value read off a published plot by eye, about ±2 µA or ±10%; **[inference]** = reasoning, not data.

Sources opened in full for these notes:
- Hampel et al., arXiv:2302.01462v1, all 6 pages, including the Fig. 3 / Fig. 4 plots.
- Hampel et al., SPIE Proc. 13025, 1302506 (2024), doi 10.1117/12.3014455, all 5 pages (NIST PDF tf.nist.gov/general/pdf/3290.pdf).
- Sedykh et al., Zh. Tekh. Fiz. 95(9), 1673–1680 (2025), doi 10.61011/JTF.2025.09.61227.80-25, all 8 pages (in Russian; the translations are mine).
- Reens et al., arXiv:2202.01715v1, pp. 1–3.

Sources seen only as an abstract or a search excerpt are flagged where they are used.

---

## Q1. What RF amplitude and frequency did each trap-integrated SNSPD tolerate, and with what wire, area, shielding and lead routing?

### Takeaway
Only two groups have published RF-tolerance data for SNSPDs in trap-like electrode geometries:
- **NIST Boulder:** Slichter 2017, Todaro 2021, Hampel 2023/2024.
- **Russian Quantum Center / HSE / MISIS / MSPU (Gol'tsman, Lakhmanskiy):** Sedykh 2023, Sedykh 2025, Suleimen 2026.

The largest demonstrated drive is **54 V peak at 70 MHz** (Hampel, NbTiN, grounded Al mirror). It costs about 40% of the switching current, and that loss is attributed to RF heating, not induced current. The Moscow devices were tested only at **≤ 2 V** (5–35 MHz) on model electrodes. Their sensitivity scales as amplitude × frequency, which is the signature of capacitive pickup. No published device used a differential, balanced or centre-tapped meander.

### Cited Findings

**Comparison table** (from the sources below; Isw = switching current):

| Device | Material / wire | Area, L_k | Shield | RF tested | Isw rf-off → at max rf | Source |
|---|---|---|---|---|---|---|
| Slichter 2017, ring trap | 7 nm MoSi + 2 nm a-Si; 140 nm / 230 nm pitch | ≤30 × 30 µm; 550 nH | none; meander recessed inside a square rf electrode | 25 V, 46.23 MHz, 3.8 K | 11.5 → 7.6 µA (8.7 µA with cancellation tone) | [Slichter Sec. 4, Figs. 5–6](https://arxiv.org/abs/1611.09949) |
| Todaro 2021, linear trap | 8 nm MoSi; 110 / 170 nm | 22 × 20 µm; 2.2 µH | none; in a pocket of a DC electrode between the rf rails, 6 µm recess | 8.8 V, 67 MHz, 3.45 K | 8.9 → I_m ≈ 5.3 µA | [Todaro PRL p. 3, Supp. Fig. S4](https://arxiv.org/abs/2008.00065) |
| Hampel 2023, same trap layout as Todaro | 10 nm NbTiN; 90 / 180 nm | 20 × 30 µm; 1.3 µH | 50 nm Al mirror 212 nm below the NbTiN, grounded; "large" mirror also under the leads for several hundred µm | 18–54 V, 68–72 MHz, 4.5 and 6 K | ≈61 → ≈35 µA at 54 V, 4.5 K; ≈47 → ≈22 µA at 54 V, 6 K [team reading] | [arXiv Fig. 3](https://arxiv.org/abs/2302.01462); [SPIE Fig. 3](https://tf.nist.gov/general/pdf/3290.pdf) |
| Sedykh 2025, trap model | 5–7 nm NbN; 100 nm strip, j_c ≈ 5 MA/cm², Tc 7.5 K | 15 × 15 µm | 80 nm Au mirror under 100 nm Si3N4; 300 nm SiO2 + 300 nm ITO on top, ITO grounded | 0.01–2 V, 5–35 MHz, 2.2 K | ≈15 µA; Ic 14.94 → 14.05 µA (5 MHz) and 14.84 → 12.84 µA (35 MHz) over the amplitude sweep | [Sedykh 2025, Fig. 1, Fig. 3, p. 1676](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng) |
| Suleimen 2026 (abstract only) | NbN, 100 nm vs 300 nm wide | — | ITO shield | 2π × 25 MHz; amplitudes not in abstract | active cancellation recovers 92% of unperturbed Ic | [PR Applied 25, 044091](https://journals.aps.org/prapplied/abstract/10.1103/771x-57wg) |

**Hampel 2023, Fig. 3 per-panel readings** (4.5 K unless noted) [team reading]:
- (a) Large mirror, floating. Isw falls from ≈59 µA (0 V) to ≈51 (18 V), ≈44 (29 V), ≈37 (36 V) and ≈29 µA (44 V). At 44 V the plateau has gone: the maximum BCR is ≈80 of 200 kcps. DCR appears near 15 µA at 54 V.
- (b) Large mirror, grounded. Isw ≈61 → ≈56 / ≈52 / ≈51 / ≈45 / ≈36 µA for 18 / 29 / 36 / 44 / 54 V. The full 200 kcps plateau survives up to 44 V.
- (c) Small mirror, grounded. Isw ≈61 → ≈56 / ≈49 / ≈40 / ≈28 / ≈14 µA for 18 / 29 / 36 / 44 / 54 V. At 54 V it is about 2.5× worse than (b).
- (d) Large mirror, grounded, 6 K. Isw ≈47 → ≈22 µA at 54 V.
- [Hampel arXiv Fig. 3](https://arxiv.org/abs/2302.01462)

**Hampel 2023, interpretation in the text:**
- **Floating mirror.** The flattening of BCR(I_b) fits the Todaro induced-current model (Fig. 4(a)).
- **Grounded mirrors.** The model "does not fit well" for any grounded-mirror device. The response "is similar to their response to increasing temperature" (Fig. 4(b)), so the authors posit on-chip rf dissipation. They measured a temperature rise of about 0.5 K within about 10 µs of switching off 45 V rf.
- **Thin electrodes.** The 350 nm Au electrodes (versus ~6 µm in ion-trapping devices) may exaggerate the heating.
- [Hampel arXiv p. 4](https://arxiv.org/abs/2302.01462)

**Hampel geometry: where the SNSPD sits.**
- SPIE Fig. 1 is a clear SEM. The SNSPD sits in the channel between the two rf electrodes, at the **end** of the rf rails.
- The leads run along the trap axis between the rails and then out. The Al mirror (green outline) covers the SNSPD and runs under the leads for several hundred µm.
- Wire: 90 nm on a 180 nm pitch, 20 × 30 µm active area.
- Electrodes and leads are a single 350 nm Au lift-off. The mirror is contacted through CHF3-etched vias plus 20 nm Au "to prevent oxidation of the aluminum".
- [SPIE Sec. 2–3, Fig. 1](https://tf.nist.gov/general/pdf/3290.pdf)

**Pickup in the Hampel readout (SPIE Fig. 2 inset).**
- At 44 V peak, the unfiltered output carries an rf sine of roughly the same amplitude as the SNSPD pulse.
- Without the notch at f_rf plus a low-pass, "the counter can be triggered multiple times by a single SNSPD output". The cause is the rising edges at the rf frequency.
- [SPIE Sec. 4](https://tf.nist.gov/general/pdf/3290.pdf)

**Hampel scope claim.** The improvement is "an order of magnitude increase in tolerance to applied trapping rf potential" plus at least 2.5 K higher operating temperature, with the same electrode geometry as Todaro. The devices are said to be usable down to q/m ≈ 0.01 e/u. [Hampel arXiv p. 5](https://arxiv.org/abs/2302.01462)

**Sedykh 2025: stack, ITO, and the earlier unshielded paper.**
- **Stack (Fig. 1b), bottom to top:** sapphire 400 µm / Au1 80 nm (mirror) / Si3N4 100 nm / NbN 5 nm / Au2 300 nm (contacts) / SiO2 300 nm / ITO 300 nm.
- **ITO:** DC magnetron, 150 W, 1 sccm Ar, 1.5 × 10⁻³ mbar, 25 nm/min. Sheet resistance 428 / 160 / 82 Ω/sq for 20 / 50 / 100 nm (on sapphire). The ITO was grounded during the measurements.
- **Why the mirror is Au:** chosen for reflectivity at 397 nm (Ca+).
- **Earlier paper (Sedykh 2023, their ref. 12):** an unshielded NbN device reached a maximum field amplitude of only **800 mV at 5 MHz**. With ITO the range rose to **2000 mV at 5 MHz**.
- [Sedykh 2025, pp. 1674–1677](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)
- The 2023 paper is Sedykh et al., Zh. Tekh. Fiz. 93(7), 974 (2023), doi 10.21883/JTF.2023.07.55756.88-23 / Tech. Phys. 68(7), 908, as listed in the 2025 reference list. **I did not open its text**; the abstract (search excerpt) gives 10–800 mV, 5–20 MHz, 4 K.

**Sedykh 2025: efficiency fit (Fig. 4(b), table p. 1678).**
- Efficiency is fitted to η(A) = η0 / (1 + (A/A_3dB)ⁿ), where A_3dB is the amplitude that halves efficiency.
- A_3dB = 1392 / 726 / 526 / 365 / 296 / 348 / 776 mV at 5 / 10 / 15 / 20 / 25 / 30 / 35 MHz.
- The authors say the 30 and 35 MHz values are unreliable because data were insufficient.
- [Sedykh 2025, Fig. 4, table](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)

**Sedykh 2025: the two causes they give for the Ic drop (p. 1676).**
1. Additional induced rf currents.
2. "Additional charging of capacitors in the readout circuit", which raises the bias current.

They also note that the trap geometry in their model is not given numerically. Fig. 1a shows GND, "+RF" electrodes and a "Signal" pad around the ITO-covered SNSPD.

### Inferences
- **The amplitude × frequency product is constant for 5–25 MHz [team calc].** From Sedykh's table: 5 × 1.392 = 6.96, 10 × 0.726 = 7.26, 15 × 0.526 = 7.89, 20 × 0.365 = 7.30, 25 × 0.296 = 7.40 V·MHz, all within ±7%. This is what a displacement current I = 2πf·C·V adding to the bias predicts. It is the cleanest published evidence that the degradation scales as V·f. Their electrode geometry is unpublished, so the absolute number (A_3dB ≈ 0.26 V at 28 MHz extrapolated) does **not** transfer to a real trap.
- **V·f is the right figure of merit for comparing drives [team calc]:**

  | Drive | V·f |
  |---|---|
  | Todaro: 8.8 V × 67 MHz | 590 V·MHz |
  | Slichter: 25 × 46 | 1160 V·MHz |
  | **This project: 53 V × 28 MHz** | **1484 V·MHz** |
  | Hampel max: 54 × 70 | 3780 V·MHz |
  | Hampel Ca+ operating point: 40 × 70 | 2800 V·MHz |

  By this metric the project's drive sits **inside Hampel's demonstrated envelope**, even though 138Ba+ (0.0072 e/u) is below Hampel's stated q/m range. Coupling capacitance (geometry) is the other factor, and it differs, so this is a necessary but not sufficient comparison.
- **Hampel's "order of magnitude" is about rf amplitude, not fractional Isw.** At their maximum drive, Todaro lost about 40% of Isw (8.9 → 5.3 µA at 8.8 V) and Hampel also lost about 40% (61 → 35 µA at 54 V). The gains came from three factors together:
  - about 7× higher Isw (NbTiN versus MoSi);
  - a grounded mirror that removed the induced-current signature;
  - running at a higher drive.
  The residual loss in Hampel is a different mechanism (heating).
- **Mirror size mattered as much as grounding at high drive.** At 54 V, the small grounded mirror gave Isw ≈14 µA and the large one ≈36 µA. Hampel attributes this to thermal and dissipative paths. A mirror that also lies under the leads may additionally cut lead pickup [inference].

### Gaps
- **Suleimen 2026** (Phys. Rev. Applied 25, 044091, doi 10.1103/771x-57wg; received 30 Oct 2025, published 30 Apr 2026): only the abstract was readable. Not retrieved: amplitudes, the 300 nm versus 100 nm Ic-ratio curves, ITO thickness, and the cancellation method. No arXiv version was found. **Read this paper first.** It is the only published study that varies wire width for RF tolerance.
- Hampel's switching currents are figure readings; the numeric data are in the NIST data set [doi 10.18434/mds2-3216](https://data.nist.gov/pdr/lps/ark:/88434/mds2-3216/pdr:v/1.0.0) (listed, not opened).
- Sedykh's model-trap electrode dimensions and detector-to-RF distance are not given, so their V numbers cannot be scaled to a real trap.
- No trap-integrated SNSPD has been tested at the project's combination of 138Ba+, 493 nm, 28 MHz and ~50 V. No published device sits under 10 µm of SiO2 with an Au electrode opening above it.

---

## Q2. Mechanisms by which trap RF degrades an SNSPD, and quantitative tolerances

### Takeaway
There are four distinct mechanisms, and they need different fixes:
1. **Capacitive displacement current adds to the dc bias in the wire.** It lowers the usable bias and, if spatially varying, flattens the efficiency plateau. Fix: shield or reduce the coupling.
2. **RF pickup on the readout line.** It produces false or multiple triggers. Fix: notch plus low-pass, or a differential readout.
3. **RF dissipation heats the chip and lowers Ic.** This is the residual limit once shielded.
4. **RF-enabled clicks with the bias off.**

Latching is only indirectly related: rf current pushes I_b + I_rf over Isw, and the wire then has to reset through the load.

### Cited Findings
- **Induced current reduces the usable bias and flattens the plateau (Hampel).** The flattening is "believed to arise from induced rf currents flowing in the SNSPD". The floating-mirror data fit the induced-current model. The model "indicates that induced rf currents always flatten the slope of the BCR vs. I_b curve", which distinguishes them from heating, which shifts the curve without flattening it. — [Hampel arXiv p. 3–4, Fig. 4(a)](https://arxiv.org/abs/2302.01462)
- **Spatially varying versus uniform components (Todaro).** The fit gives I0 = 0.9 µA uniform (lead capacitance with asymmetric termination) and I1 = 3.5 µA spatially varying (direct rf-to-meander capacitance). Only the uniform part can be cancelled by a single tone. — [Todaro Supp. Fig. S4, Eq. S1](https://arxiv.org/abs/2008.00065) (already in the earlier notes; restated because it frames everything below).
- **Heating signature (Hampel).** The BCR curves shift to lower I_b without flattening, mirroring the temperature series of Fig. 4(b). The measured rise was about 0.5 K after 45 V. Fig. 4(b) gives the scale: Isw falls from ≈58 µA at 3 K to ≈47 µA at 6 K and ≈10 µA at 9 K [team reading]. — [Hampel arXiv Fig. 4(b), p. 4](https://arxiv.org/abs/2302.01462)
- **Readout-line pickup and false triggers.** See Hampel SPIE Fig. 2 inset (rf sine about as large as the pulse at 44 V) and the multi-trigger remark. Todaro: pickup "several times larger" than the pulses; a 40 dB notch plus 25 MHz low-pass was needed. — [SPIE Sec. 4](https://tf.nist.gov/general/pdf/3290.pdf); [Todaro Supp.](https://arxiv.org/abs/2008.00065)
- **Readout-circuit charging (Sedykh).** Sedykh attributes part of the Ic drop to rf charging capacitors in the readout chain, which raises the effective bias. This is a bias-network mechanism separate from on-chip coupling. — [Sedykh 2025 p. 1676](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)
- **Dark counts versus rf.** DCR "does not strongly increase" with external field amplitude when compared at fixed offset from Ic. DCR stays near 1 s⁻¹ in their Fig. 3 well below Ic. — [Sedykh 2025 p. 1676–1677, Fig. 3](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)
  - Hampel: DCR below 1 cps until within "a few µA of the switching current", then exponential, "both with and without applied rf". — [Hampel arXiv p. 3](https://arxiv.org/abs/2302.01462)
  - So RF does not create a separate dark-count floor. It moves the point where the exponential rise begins.
- **Clicks with the bias off.** "Even when the bias current is off, the SNSPD will occasionally pulse in response to photons when the trap rf is on." — [Todaro PRL p. 4](https://arxiv.org/abs/2008.00065) (in the earlier notes; listed for completeness as an rf mechanism).
- **Latching physics.** The negative electrothermal feedback through the load must be *unstable* for normal operation. If the electrical response is sped up (lower L_k / R_L), the feedback becomes stable and the wire latches. — [Kerman et al., PRB 79, 100509 (2009), arXiv:0812.0290 abstract](https://arxiv.org/abs/0812.0290)
  - I read only the abstract, which gives no quantitative L_k–R_L threshold.
  - Todaro thickened the leads with 350 nm Au specifically "to avoid latching" (lower series resistance). — [Todaro Supp.](https://arxiv.org/abs/2008.00065)

### Inferences
- **Tolerance budget [inference from the Todaro and Hampel models].**
  - Peak induced current must stay below Isw − I_plateau-onset, i.e. the bias range between where the SDE plateau starts and Isw.
  - With a flat plateau (Hampel grounded, 4.5 K: plateau starts about 10 µA below Isw), several µA of uniform induced current cost nothing in SDE.
  - With a narrow or absent plateau (Todaro MoSi), every µA costs efficiency.
  - **For NbN at 493 nm, how wide the plateau is at the operating temperature matters as much as the absolute Isw.**
- **NbN Isw at the project's temperature is probably lower than the 15–20 µA often quoted [team calc, rough].**
  - Sedykh's 100 nm, 5–7 nm NbN gives ≈15 µA at 2.2 K, with Tc 7.5 K.
  - With the common Ic ∝ (1 − (T/Tc)²)^{3/2} scaling, at 4.5–5 K and Tc ≈ 7.8 K this becomes about 8–10 µA.
  - The team's 1.4 µA pickup bound would then be about 15% of Isw, not about 4–8%. Measure Isw(T) on the T8 test structures before trusting the margin.
- **Heating is probably much smaller here than in Hampel [team calc, order of magnitude].**
  - Conductor loss scales as (V·f)²·R. Relative to Hampel's 45 V / 70 MHz: (53·28 / 45·70)² ≈ 0.22, and 6 µm Au versus 350 nm Au cuts the electrode R about 17×. The project's conductor heating should therefore be about 1% of Hampel's per unit C.
  - Unlike Hampel, the project has an Al ground plane under the whole RF rail through 10 µm SiO2. That adds rail-to-ground C (DESIGN_LOG step 21: ≥3.4 pF on-chip RF) and a return current of about ωCV ≈ 30 mA in the Al.
  - Dissipation in the Al-1%Cu return path and in the PECVD SiO2 (loss tangent unknown at 4 K) is the term to estimate. It is not covered by any trap-SNSPD source.

### Gaps
- No source measures RF-induced dark counts or latching in a trap SNSPD as a function of L_k. The only lead is Kerman's general model; the full text was not read.
- No cryogenic loss-tangent data for PECVD SiO2 at tens of MHz were retrieved.
- No measurement separates on-chip induced current from bias-network charging (Sedykh's second mechanism).

---

## Q3. Which geometry changes have been shown or modelled to raise RF tolerance? Is a balanced, differential or centre-tapped layout used anywhere in traps?

### Takeaway
**Demonstrated:**
1. A grounded conductor between the nanowire and the substrate, close to the wire (Hampel: Al 212 nm below; Sedykh: Au under 100 nm Si3N4).
2. That ground extended under the leads ("large mirror").
3. Higher-Ic material (NbTiN, about 7–10× MoSi).
4. A grounded transparent top layer (Sedykh ITO: 800 mV → 2000 mV at 5 MHz).
5. **Wider wire (300 nm versus 100 nm NbN; Suleimen 2026, abstract only).**

**Modelled only:**
- grounded Au mesh or ITO over the mirror (Hampel Fig. 2(c,d));
- the mirror plus ITO combination, said to cut the field effect by about 10³ (Sedykh conference abstract, search excerpt).

**Recommended in text but never built:** symmetric termination, narrow leads, higher inductance (Todaro, Slichter). **No trap paper uses a differential, bifilar or centre-tapped meander.** Differential SNSPDs exist outside traps (JPL/MIT impedance-matched devices) for timing, not rf immunity.

### Cited Findings
- **Changes credited by Hampel over Todaro.** "The trap electrode design is identical", with two major changes:
  1. NbTiN instead of MoSi, "increasing the SNSPD critical currents by roughly a factor of 10 and enabling operation at higher temperatures of up to 7 K";
  2. a grounded Al mirror.
  Both "reduce the sensitivity of the SNSPD performance to the applied trap rf potentials".
  Wire geometry changed only slightly (110/170 → 90/180 nm; 22 × 20 → 20 × 30 µm). — [Hampel arXiv p. 1](https://arxiv.org/abs/2302.01462)
- **Simulated field reduction (Hampel Fig. 2).** Colour maps at 100 V peak, 70 MHz, on a log scale from about 10³ to 10⁶ V/m.
  - (a) Unshielded: about 10⁵–10⁶ V/m at the wire.
  - (b) Grounded Al below: "roughly an order of magnitude" lower.
  - (c) Au mesh on top and (d) ITO on top "further improve" the shielding. No number is given; visually the field drops to about 10³ V/m in (d).
  - [Hampel arXiv Fig. 2](https://arxiv.org/abs/2302.01462)
- **Floating versus grounded, small versus large mirror.** See the Q1 Fig. 3 readings. A floating mirror leaves the induced-current signature. A grounded small mirror is markedly worse at 54 V than a grounded large mirror (≈14 versus ≈36 µA). — [Hampel arXiv Fig. 3](https://arxiv.org/abs/2302.01462)
- **ITO top shield, measured (Sedykh 2025).**
  - Operating range rose from 800 mV (unshielded, 2023) to 2000 mV (ITO, 2025) at 5 MHz.
  - The authors note limits from ITO conductivity and "skin depth". They plan a superconducting mesh with transmission above 90%.
  - They also plan **microstrip detectors 1–10 µm wide with critical currents of 600–700 µA**, to improve resilience to trap fields.
  - They float a planar Penning trap (static fields only) as an alternative that would "significantly reduce induced currents".
  - [Sedykh 2025, p. 1675, Conclusion p. 1679](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)
  - **Caution:** the 2023 and 2025 devices differ in more than the ITO (stack, temperature 4 K versus 2.2 K, frequency range), so the 2.5× is not a clean ITO-only comparison.
- **Wire width (Suleimen 2026, abstract only).** "a 300-nm-wide nanowire exhibits greater resilience to rf fields compared to a 100-nm-wide device". It keeps a higher relative critical current at larger rf amplitudes. Phase-coherent active cancellation recovered 92% of the unperturbed Ic at 2π × 25 MHz. — [PR Applied 25, 044091 (2026)](https://journals.aps.org/prapplied/abstract/10.1103/771x-57wg)
- **Recommended but not built (Todaro).** Reduce C_RN by capacitive shielding; reduce the uniform term by "symmetric terminations", lower C_RL and higher SNSPD inductance. — [Todaro Supp. Fig. S4 text](https://arxiv.org/abs/2008.00065)
- **Recommended but not built (Slichter).** "longer, thinner meanders" (more inductance) and identical termination of both leads. — [Slichter App. A](https://arxiv.org/abs/1611.09949)
- **Leads.** Todaro made leads "much narrower than typical SNSPD leads … to minimize capacitive coupling to the trap rf electrodes". — [Todaro Supp. "Trap fabrication"](https://arxiv.org/abs/2008.00065)
- **Differential SNSPDs outside traps.** Colangelo et al., "Impedance-matched differential superconducting nanowire detectors", arXiv:2108.07962 (NbN; transmission-line engineering plus differential readout). The abstract makes no common-mode-rejection or pickup claim. — [arXiv abstract](https://arxiv.org/abs/2108.07962)
  - A Caltech/JPL APS March Meeting 2020 abstract reports that a balanced cryogenic differential bias tee reduced EM-noise coupling and gave lower DCR than a ground-referenced device. — [APS abstract B11.6, search excerpt only](https://archive.aps.org/mar/2020/b11/6)
- **Two-ITO aperture shielding in a trap, for a SPAD (MIT-LL).** Reens et al. place SPADs directly under trap sites between the rf rails, with the same overall stack idea as this project:
  - Nb ground plane on 2 µm SiO2, with apertures over the SPADs;
  - 10 µm SiO2 above it;
  - Nb trap electrodes on top;
  - 30 µm clear aperture; ion at 50 µm; rf ~50 V.
  - "Two layers of ITO were used, one over the SPAD aperture in the ground plane and one over the similar aperture in the trap metal, to shield the ion from SPAD pulses and to shield the SPAD from trap radio frequency (RF) voltage."
  - [Reens arXiv:2202.01715, p. 1–2, Fig. 1(b,c)](https://arxiv.org/abs/2202.01715)

### Inferences
- **Why a centre tap or symmetric termination would help, and how much [inference from the Todaro distributed model].**
  - The meander's inductive impedance is about 10⁻⁶ of |Z_CRN| (Todaro Supp.). The wire therefore behaves as a near-equipotential conductor fed by distributed current sources, and the injected displacement current drains to whichever ends are low-impedance at f_rf.
  - With one end open (high-Z), the peak current is the whole ∑ωC_RN·V.
  - With both ends low-Z, it is about half.
  - With a grounded centre tap and both ends low-Z, it is about a quarter.
  - Generalisation: N sub-meanders, each low-Z at both ends, give peak ∝ 1/(2N) of the total.
  - This is the same logic as Todaro's "symmetric terminations". A centre-tapped device becomes two half-length detectors, which halves L_k per half and is a latching consideration.
- **Differential readout is not the same as rf immunity.**
  - The two rails of a five-wire trap carry the same rf phase, so pickup on a symmetric pair of leads is mostly common-mode. A differential amplifier or balun would reject it at the **output**, attacking the false-trigger problem.
  - It does **not** remove the displacement current flowing **in** the nanowire, which is what lowers Isw. Only reducing ω·C·V into the wire, or splitting the wire's drain paths, does that.
- **Wire orientation and hairpins [inference].** Current crowding at sharp 180° turns lowers the switching current of the whole meander (see Gaps for the source). Put the hairpins where the rf field is weakest:
  - Lines parallel to the trap axis put the hairpins at the axial ends of the window, under the continuing centre-DC Au, away from the rails. Only the 1–2 outermost lines run close to the window edges facing the rails.
  - Lines perpendicular to the axis put **every** hairpin at the window edge nearest an rf rail.
- **Wider wire [inference].**
  - At fixed fill factor, a 3× wider wire carries about 3× Ic. Displacement current per unit area is about unchanged, so I_rf/Isw drops about 3×.
  - L_k at fixed area drops about 9× (3× fewer lines, 3× fewer squares per unit length). For A30 that is about 4.7 µH → about 0.5 µH, a reset of about 10 ns into 50 Ω, which moves toward the latching regime.
  - Whether 300 nm, 5–7 nm NbN still has a saturated internal efficiency at 493 nm (2.5 eV) is the question to check in Suleimen 2026.

### Gaps
- **Current crowding at bends.** The standard reference is J. R. Clem and K. K. Berggren, "Geometry-dependent critical currents in superconducting nanocircuits", PRB 84, 174510 (2011). It was **not opened in this session**; the authors and title are from memory and must be verified before citing. A 2024 arXiv paper on current-crowding-free SNSPDs (arXiv:2407.14171) was seen only as a search excerpt.
- **Sedykh conference abstract** claiming that mirror plus ITO reduce the field effect by about 3 orders of magnitude in modelling: search excerpt only. The 2025 journal text says the "combination of a metal mirror under the detector and an ITO screening coating … reduce the influence … by 3 orders" when describing **Hampel's** modelling (p. 1674). Hampel's own text gives no such number. **Treat "10³" as unsourced.**
- **Bifilar or centre-tapped meanders:** no trap-SNSPD paper found.

---

## Q4. How does pickup scale with wire length, area and position relative to the RF rails? Does a grounded layer above or below matter more than wire geometry?

### Takeaway
To first order, induced current = 2πf · V_rf · C_coupling. C_coupling has two parts:
- **C_RN:** proportional to the meander area exposed to field lines that are not intercepted by a nearer ground.
- **C_RL:** proportional to lead area exposed to rf.

**The grounded layer matters more than wire geometry.** Hampel's 10× field reduction from a grounded mirror at 212 nm, plus the floating-versus-grounded contrast at fixed wire geometry, is the strongest evidence. Wire width and length then set how much Isw headroom and inductance you have.

In this project's stack the meander already sits 238 nm above grounded Al, so the residual pickup is set by:
1. lateral fringing through the 30 µm Au opening;
2. the leads;
3. **any lead or centre-DC rf voltage**, not the meander wire geometry.

### Cited Findings
- **V·f scaling, measured.** Sedykh's A_3dB × f is constant within ±7% over 5–25 MHz (Q1 inference, from the Sedykh 2025 table). — [Sedykh 2025 table p. 1678](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)
- **Proximity of the rf electrodes (Hampel SPIE).** "the close proximity of the rf electrodes can impair the function of the SNSPDs significantly. The high rf fields … will induce rf currents in the SNSPD nanowires and bias leads." — [SPIE Sec. 2](https://tf.nist.gov/general/pdf/3290.pdf)
- **Coupling grew from Slichter to Todaro.** The direct meander coupling rose between the devices. The thesis attributes the switch from lead-dominated to meander-dominated pickup to "increased coupling between the RF electrode and the SNSPD meander" (Todaro thesis p. 118, via the earlier notes). — [Todaro thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Required rf scales with frequency (Hampel).** Lowering the rf frequency lowers the required amplitude proportionally at fixed confinement (Hampel p. 3). — [Hampel arXiv](https://arxiv.org/abs/2302.01462)
- **Project's own 2-D model.** Step 10 and case f: with the Al mirror alone and 10 µm SiO2 kept over the window, the pickup bound is ~1.4 µA at 53 V / 28 MHz. The log already notes that "In the shielded cases, the leads, not the meander, set the real pickup". — `design/DESIGN_LOG.md`, Step 10 and the case-f entry (lines ~440–520, ~812)

### Inferences
- **Scaling rules [team calc / inference]:**
  - **Frequency and amplitude:** I ∝ f·V. At fixed q and secular frequency, V ∝ m·Ω²·h², so I ∝ m·Ω³·h². For a given trap, a heavy ion at low Ω (28 MHz here) is not worse than Ca+ at 70 MHz: the V·f numbers in Q1 put this project at about 0.4× Hampel's maximum.
  - **Area:** I1 ∝ C_RN ∝ the exposed area. B60 (60 × 30 µm) has about 2× the area of A30 at the same lateral distance to the rails, so expect about 2× I1. The team's case-f bound should be rerun for B60 if it was run only for A30.
  - **Length at fixed area** (finer pitch, more squares): C_RN is roughly unchanged. L_k rises (∝ squares), which reduces the *uniform* (lead-driven) term through a current divider: I0 ≈ I_lead · Z_term / |Z_term + jωL|.
    - At 28 MHz, ωL ≈ 830 Ω for 4.7 µH (A30) versus 50 Ω. Only about 6% of a lead's displacement current is diverted through the meander when one end is the 50 Ω line and the other is ground.
    - Longer wire also lowers Isw per unit of uniformity defects and slows reset.
  - **Position:** field lines from an rf rail edge terminate on the nearest grounded conductor. With grounded Al 0.238 µm under the NbN, and the rail edge about 10 µm laterally plus about 10 µm vertically away, only the outermost lines within a few spacer-thicknesses of the opening's edge see significant field. Inward of the edge, the fringe field decays roughly as exp(−πx/t_spacer). The team's own sim found this form for the ITO sandwich (DESIGN_LOG step 10).
  - **Inset the meander from the window edge.** Keeping the outermost wire ≳1–2 µm inside the projected Au opening edge should cut the lateral fringe contribution strongly. This is a geometry lever that costs only a little collection area.
- **Lead coupling where a lead lies under an rf-carrying conductor [team calc].**
  - Parallel-plate C through 10 µm SiO2 (ε_r ≈ 3.9) is ≈3.45 aF/µm².
  - At 53 V, 28 MHz: I = 2π·28 MHz·53 V·C ≈ **9.3 µA per fF**, which is **≈3.2 µA per 100 µm² of lead overlap**.
  - A grounded Al plane *below* the lead does not shield it from a conductor *above* it.
  - The layout rule "SNSPD leads under the centre DC, never under an RF rail" (DESIGN_LOG step 8 table) is therefore the key protection.
- **Centre-DC electrode as an rf source [team calc, check].**
  - The leads run about 10 µm under the 40 µm centre-DC electrode and its lead, which run alongside the rails over long distances. Any residual rf on the centre DC couples straight into the leads.
  - Example: 4 µm lead × 2 mm under the centre DC ≈ 8000 µm² ≈ 28 fF. At 28 MHz that is ≈ **4.9 µA per volt of rf on the centre-DC electrode**.
  - The centre DC needs to be rf-grounded through a low-impedance filter capacitor close to the chip:
    - rf on DC ≈ V_rf × C_rail–DC / C_filter;
    - e.g. 53 V × ~0.5 pF / 1 nF ≈ 26 mV gives ≈0.13 µA.
  - The capacitor value, its distance and the bond inductance set this. It is not in the 2-D window model.
- **Grounding of the Al plane.** Hampel's floating mirror was the bad case. Check that the v3 Al plane is tied to ground through enough D2 openings and bonds that its rf impedance is small compared with 1/(ωC_rail-to-Al):
  - layer 24 (M1 via) is retired in v3;
  - D2 openings to M1 exist per `gds/layer_map.md`.
  - At ≈30 mA rf return current, 1 nH of ground-bond inductance gives ≈5 mV of ground bounce under the SNSPD [team calc].

### Gaps
- No published measurement isolates pickup versus meander area or lateral distance to the rails. The scaling above is from the circuit model plus the team's 2-D sim.
- No published 3-D model of an SNSPD in an Au-electrode window over a buried ground plane. Hampel's and the team's models are 2-D cross-sections, which cannot capture lead, window-end or centre-DC coupling.

---

## Q5. Other groups' trap-integrated SNSPD or superconducting detector work (2017–2026)

### Takeaway
Trap-integrated **SNSPDs** with published rf data come only from NIST Boulder and the Moscow consortium (RQC/HSE/MISIS/MSPU). MIT-LL (Reens, Chiaverini, McConnell) and Sandia (Setzer) integrated **SPADs**, not SNSPDs. MIT-LL's two-ITO-aperture stack is the closest architectural analogue to this project. No trap-SNSPD paper was found from Oxford, PSI/ETH, Innsbruck, Duke or Quantinuum. Duke (Kim group) used *external* SNSPDs (Crain 2019, cited by Hampel; not opened). No trap-integrated SMSPD has been demonstrated; Sedykh 2025 only proposes one.

### Cited Findings
- **NIST.**
  - Slichter 2017 (Opt. Express 25, 8705).
  - Todaro 2021 (PRL 126, 010501).
  - Hampel 2023 (APL 122, 174001).
  - Hampel 2024 SPIE (Proc. SPIE 13025, 1302506). Invited; the same devices as the APL paper, adding the Fig. 2 pulse/pickup inset and Fig. 3 data at 4.5 / 6 K for 0 / 18 / 36 / 54 V. The conclusion's next steps are optical-stack optimisation and fabrication "for tests with real ions", so **no ion readout with the shielded NbTiN devices was published as of that paper**.
  - [SPIE PDF](https://tf.nist.gov/general/pdf/3290.pdf); [CLEO 2022 STu4F.6 abstract](https://opg.optica.org/abstract.cfm?URI=CLEO_SI-2022-STu4F.6)
- **RQC / HSE / MISIS / MSPU (Moscow).**
  - Sedykh 2023 (JTF 93(7) 974; unshielded NbN, ≤800 mV, 5–20 MHz, 4 K; abstract only).
  - Sedykh 2025 (JTF 95(9) 1673; ITO-shielded, ≤2 V, 5–35 MHz, 2.2 K; read).
  - Suleimen 2026 (PR Applied 25, 044091; wire width and active cancellation; abstract only).
  - The target is 40Ca+ (397 nm); the efficiency tests were at 729 nm.
  - Sedykh estimates that a 25 × 25 µm detector with ~60% SDE at 397 nm, 30 µm from the ion, could read out in under 10 µs (p. 1679).
  - [Sedykh 2025](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng); [Suleimen 2026](https://journals.aps.org/prapplied/abstract/10.1103/771x-57wg)
- **MIT Lincoln Laboratory (SPAD, room temperature, 88Sr+ at 422 nm).**
  - Nb ground plane plus Nb electrodes, two ITO layers over the apertures, rf ~50 V.
  - 99.92(1)% fidelity in 450 µs.
  - SPADs on a 240 µm pitch under seven trap sites.
  - [Reens PRL 129, 100502 (2022), arXiv:2202.01715 Fig. 1](https://arxiv.org/abs/2202.01715)
  - Hampel's intro notes that trap-integrated SPADs "suffer from the same rf pickup effects" and have higher DCR and lower QE than SNSPDs. — [Hampel arXiv p. 1](https://arxiv.org/abs/2302.01462)
- **Sandia (SPAD).** Setzer et al., APL 119, 154002 (2021), arXiv:2105.01235. Per the abstract, fidelity was limited by laser scatter, dark counts and "heating that prevents holding the ion directly above the SPAD". No rf-pickup numbers were in the abstract; the full text was not read. — [arXiv abstract](https://arxiv.org/abs/2105.01235)
- **Superconducting traps.** Wang et al., "Superconducting microfabricated ion traps" (MIT Chuang group with MIT-LL; Nb and NbN electrodes; 88Sr+), APL 97, 244102 (2010), arXiv:1010.6108. The venue and the "lasers have no effect on the measured critical current" statement come from search excerpts only; not opened. It is relevant only if NbN trap electrodes or a superconducting ground plane are considered.
- **Planar Penning trap as an rf-free alternative.** Sedykh cites Jain et al., Nature 627, 510 (2024) (ETH Home group), as a route that "should significantly reduce induced currents". — [Sedykh 2025 Conclusion and ref. 18](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)

### Inferences
- Reens's ground-plane-aperture-plus-ITO architecture is what this project's archived v2 "two-ITO window" resembled. That architecture was demonstrated to trap stably at ~50 V rf with a detector under a 30 µm aperture (for a SPAD, which is far less current-sensitive than an SNSPD).

### Gaps
- No 2024–2026 trap-integrated SNSPD paper was found at 370, 422 or 493 nm, and no trap-integrated SMSPD.
- The search did not reach DAMOP 2024–2026 abstracts specifically. Searching the APS meeting archive for "SNSPD" plus "trap" is worth doing.
- Crain et al., Commun. Phys. 2, 97 (2019) (external SNSPDs for 171Yb+) is cited by Hampel; not opened here.

---

## Q6. What is a good target geometry that is RF resistant yet easy to fabricate, and how does the current A30/B60 detector compare?

### Takeaway
The current detector already has the single most effective, literature-backed feature: a **grounded Al plane 238 nm under the NbN, extending under the leads** (Hampel's "large grounded mirror"). The remaining levers, in rough order of expected payoff per unit of fabrication effort:
1. confirm the Al and centre-DC grounding at rf;
2. keep the leads out from under anything carrying rf, and terminate them symmetrically;
3. inset the meander from the window edge, with hairpins at the axial ends;
4. round the hairpins;
5. widen the wire if Suleimen's data support it at 493 nm;
6. only then consider a top ITO or a centre tap.

Use RF notch plus low-pass filtering regardless.

### Cited Findings
- **Large grounded mirror under the leads beats a small one at high drive** (≈36 versus ≈14 µA Isw at 54 V). — [Hampel arXiv Fig. 3(b,c)](https://arxiv.org/abs/2302.01462)
- **Readout filtering** at f_rf plus a low-pass is needed for reproducible counting. — [Hampel SPIE Sec. 4](https://tf.nist.gov/general/pdf/3290.pdf); [Todaro Supp.](https://arxiv.org/abs/2008.00065)
- **Symmetric termination, narrow leads, higher inductance.** — [Todaro Supp.](https://arxiv.org/abs/2008.00065); [Slichter App. A](https://arxiv.org/abs/1611.09949)
- **300 nm NbN wires are more rf-resilient than 100 nm** (abstract only). — [Suleimen 2026](https://journals.aps.org/prapplied/abstract/10.1103/771x-57wg)
- **Top ITO** extends the tolerated range about 2.5× (with confounds); its value for the ion (surface charge, click kicks) is separate. — [Sedykh 2025](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng); [Hampel APL published version, via the earlier notes](https://tf.nist.gov/general/pdf/3223.pdf)

### Inferences (audit of the current design; checks to run, not verdicts)

**1. Meander numbers [team calc].**

| Variant | Wire length | Squares | L_k at ≈105 pH/sq | τ = L/50 Ω |
|---|---|---|---|---|
| A30: 150 lines × 30 µm | 4.5 mm | 45,000 (100 nm) | ≈4.7 µH | ≈95 ns |
| B60, if 300 lines of 30 µm or 150 of 60 µm | 9 mm | 90,000 | ≈9.5 µH | ≈190 ns |

For comparison: Todaro had about 2.2 µH and Hampel 1.3 µH. The large L_k is good for latching margin and for suppressing the lead-driven uniform term. It is slow but irrelevant at ion count rates.

**2. Hairpins.**
- Sharp 180° turns at 100 nm width and 100 nm gap concentrate current at the inner corner. They lower Isw for the whole device, and so lower the headroom against induced current.
- Rounded or optimally tapered turns are a pure EBL-layout change with no extra process step.
- Check the expected Isw penalty against the Clem–Berggren geometry (to be verified; see Q3 Gaps).

**3. Orientation.** Run the lines parallel to the trap axis, so the hairpins sit under the continuing centre-DC Au at the window's axial ends, not at the edges facing the rails. If the current layout has lines perpendicular to the axis, this is a free change.

**4. Window-edge inset.**
- Keep the outermost wire and all hairpins a few spacer thicknesses, ≳1–2 µm, inside the edge of the projected Au opening. The lateral fringe field is concentrated there.
- Rerun sim 10 case f with the meander extent as the variable, and for B60.

**5. Leads.**
- The design keeps them under the centre DC and never under an RF rail (DESIGN_LOG step 8). Keep both leads identical in width and overlap so their coupling is common-mode, and make both terminations low-Z at f_rf.
- The current single-ended scheme (signal pad to 50 Ω, return pad to ground) is the asymmetric case Todaro modelled.
- A cheap improvement is to bond the return pad to an on-board ground right at the chip, or to make the return path a matched 50 Ω line too.
- Estimate the centre-DC rf voltage, which depends on its filter capacitor, and multiply by ≈4.9 µA/V (per 2 mm of 4 µm lead).

**6. Grounding.** Confirm that the Al plane (L10) is contacted through enough D2 openings and ground bonds. Hampel shows that a floating plane is the failure mode, and v3 retired the M1-via layer.

**7. Isw headroom.**
- Measure NbN Isw(T) at the expected trap temperature on the T8 structures. If it is ~8–10 µA at 4.5–5 K, the 1.4 µA bound is ~15%, comparable to Hampel's grounded devices at about 18–29 V.
- Widening to 200–300 nm (about 2–3× Isw) is the simplest single geometry change that raises headroom.
- It lowers L_k by about 4–9×. Check the latching margin and the 493 nm internal efficiency first (Suleimen 2026 full text).

**8. Centre tap or differential readout.**
- A centre-grounded meander with two end readouts would cut the peak induced current about 2× relative to two low-Z ends (inference above).
- It needs a third contact and a second readout chain.
- Differential readout of the two leads helps the output pickup, not the in-wire current.
- Neither has trap precedent. Treat both as second-run options.

**9. Top ITO.** Removed in v3. Sedykh shows it helps the detector somewhat, and Hampel and Todaro say a top conductor is needed for the ion (surface charge on exposed SiO2, click kicks). It was not adopted in v3. The team's step 10 found that, with Al below, top ITO mostly helps the ion, not the wire.

**A fabrication-friendly target [inference]:**
- NbN 5–7 nm, ~150–200 nm wide at 50% fill;
- lines parallel to the axis, with rounded or tapered hairpins;
- meander inset ≥2 µm from the window edge;
- grounded Al 238 nm below, extending under both identical leads, which run only under the centre DC;
- both lead ends low-Z at f_rf;
- an RF notch at 28 MHz plus a ~25 MHz low-pass in the readout.

This is a one-mask (EBL) change from the present design.

### Gaps
- No published trap-SNSPD Isw-versus-rf data for NbN at 4–5 K, or for wires wider than 110 nm, beyond Suleimen's abstract.
- No published measurement of the hairpin or inset effect on rf pickup.
- Whether the v3 A30 meander lines run parallel or perpendicular to the trap axis was not checked for these notes (look at `gds/make_chip.py` / layer 20).

---

### Read these yourself (specific locations)
1. **Hampel arXiv:2302.01462.**
   - Fig. 2(a)–(d): field maps; compare panel (b) with your stack.
   - Fig. 3(a) versus (b): floating versus grounded; (b) versus (c): large versus small mirror.
   - Fig. 4(a)/(b) with p. 4: the induced-current versus heating argument.
2. **Hampel SPIE 13025 (tf.nist.gov/general/pdf/3290.pdf).**
   - Fig. 1: lead and mirror routing.
   - Fig. 2 inset: pickup versus pulse at 44 V.
   - Sec. 4: filtering.
3. **Sedykh JTF 2025 (mathnet.ru link above).**
   - Fig. 1b: stack.
   - Fig. 3 and p. 1676: Ic versus amplitude and frequency.
   - Fig. 4 and the table on p. 1678: the A_3dB(f) data behind the V·f scaling.
   - Conclusion p. 1679: mesh and microstrip plans.
4. **Suleimen PR Applied 25, 044091 (2026).** The full text: width comparison and cancellation. Not yet read by anyone on the team.
5. **Reens arXiv:2202.01715.** Fig. 1(b,c) and p. 1–2: the two-ITO aperture stack under a 50 µm ion.
6. **Todaro Supp. Fig. S4 / Eq. S1.** Re-read with the centre-tap and symmetric-termination question in mind.
