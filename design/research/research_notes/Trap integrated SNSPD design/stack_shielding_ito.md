# Trap-integrated SNSPD: layer stack, RF shielding, optical cavity design, and ITO transparent ground for 138Ba+ (493 nm) at ~5 K

Target stack (bottom to top): Si / thermal SiO2 / Al ground plane + mirror / SiO2 spacer (t1) / NbN nanowire (5-10 nm) / SiO2 cap (t2) / grounded ITO (t_ITO) / ~10 um PECVD SiO2 / Au electrodes.

Notation: "[TMM]" marks numbers I calculated for these notes with my own normal-incidence transfer-matrix script. The script uses the optical constants cited in Q3 and an effective-medium approximation for the meander. Treat these as design estimates, not published results. The script and its inputs are in the scratchpad (see the Q3 Gaps).

---

## Q1. Hampel et al. 2023: full stack, mirror, grounding, RF tolerance, efficiency, temperature, simulations

### Takeaway
Citation verified: B. Hampel, D. H. Slichter, D. Leibfried, R. P. Mirin, S. W. Nam, V. B. Verma, "Trap-Integrated Superconducting Nanowire Single-Photon Detectors with Improved RF Tolerance for Trapped-Ion Qubit State Readout," Appl. Phys. Lett. 122, 174001 (2023), DOI 10.1063/5.0145077, arXiv:2302.01462.

The fabricated stack, bottom to top, is: high-resistivity Si / 150 nm PECVD SiO2 / 50 nm e-beam Al mirror (lift-off) / 212 nm SiO2 / 10 nm NbTiN (90 nm wide on 180 nm pitch) / 130 nm PECVD SiO2 cap. The trap electrodes are 350 nm Au. The mirror is grounded through CHF3-etched vias plus 20 nm Au, which contact the Au trap electrode layer. The devices operated at up to 54 V peak at 70 MHz and up to 6 K. System detection efficiency (SDE) at 395 nm was 68% with the mirror and 40% without, on standalone fiber-coupled devices with a 186 nm bottom oxide. Grounded ITO and Au-mesh top shields were simulated (Fig. 2c,d) but not fabricated.

### Cited Findings
- **Verified IDs.** arXiv:2302.01462 (submitted 2 Feb 2023). Published as APL 122, 174001 (2023), DOI 10.1063/5.0145077. The published version is hosted by NIST at tf.nist.gov/general/pdf/3223.pdf. — [arXiv](https://arxiv.org/abs/2302.01462); [APL DOI](https://doi.org/10.1063/5.0145077); [NIST PDF](https://tf.nist.gov/general/pdf/3223.pdf)
- **Correction to the task's guesses.** The 212 nm SiO2 / 10 nm / 130 nm SiO2 numbers are correct, but the film is NbTiN, not NbN. ITO and the Au mesh appear only in simulations (Fig. 2c,d). The fabricated devices had no top shield "for simplicity." — [arXiv](https://arxiv.org/abs/2302.01462)
- **Fabrication sequence.**
  - Substrate: high-resistivity Si (>20 kΩ·cm) with 150 nm PECVD SiO2.
  - Mirror: 50 nm e-beam-evaporated Al, patterned by lift-off, covered by 212 nm SiO2.
  - Absorber: 10 nm NbTiN co-sputtered at 500 °C, patterned by optical + e-beam lithography and SF6 RIE.
  - Active area is 20 um x 30 um. Measured wire width is 90 nm on a 180 nm pitch (SEM).
  - Vias etched through the bottom SiO2 (CHF3 RIE), followed by 20 nm Au, connect to the buried Al mirror.
  - Trap rf and dc electrodes and the SNSPD leads come from a single 350 nm evaporated Au lift-off. This layer contacts the Al mirror where the vias were opened.
  - Finally, a 130 nm PECVD SiO2 cap is patterned (CHF3 RIE) to cover only the SNSPD. — [arXiv](https://arxiv.org/abs/2302.01462)
- **Simulation geometry (Fig. 2).** 2D finite-element cross-section through the SNSPD, along the white dashed line in Fig. 1, with 100 V peak at 70 MHz on the rf electrodes. Panels:
  - (a) No shielding: Si / 212 nm SiO2 / 10 nm-thick, 100 nm-wide NbTiN on 160 nm pitch / 130 nm SiO2 / vacuum.
  - (b) Grounded Al mirror between Si and the lower SiO2. The rf field around the nanowire drops by "roughly an order of magnitude."
  - (c) Plus a grounded 50 nm Au mesh on top, with width and pitch equal to the SNSPD gaps.
  - (d) Plus a grounded 50 nm ITO layer instead of the mesh.
  - Both top layers "further improve the shielding," but the text gives no number. The top layer also shields the ion from SNSPD pulse fields. — [arXiv](https://arxiv.org/abs/2302.01462); [NIST PDF](https://tf.nist.gov/general/pdf/3223.pdf)
- **Published version adds a sentence the arXiv v1 lacks.** A top shielding layer "may be necessary for future designs to protect the ion from accumulating surface charges on the insulating SiO2 layer and to reduce motional heating of the ion due to SNSPD pulses," but "might not be required" for shielding the SNSPD from rf. — [NIST PDF of APL version](https://tf.nist.gov/general/pdf/3223.pdf)
- **Mirror variants and grounding.** Two mirror sizes were tested:
  - "Small": under the SNSPD plus a small surrounding region (Fig. 1 inset).
  - "Large": also under the SNSPD leads for several hundred um away from the rf electrode.
  - Each was either electrically floating or grounded via the trap electrodes. — [arXiv](https://arxiv.org/abs/2302.01462)
- **RF tolerance (Fig. 3).** BCR/DCR vs. Ib at 4.5 K: (a) large floating mirror, (b) large grounded mirror, (c) small grounded mirror, (d) same device as (b) at 6 K.
  - Floating mirror: with increasing rf, the switching current drops and the BCR(Ib) curve flattens, consistent with induced rf currents. Fit to the induced-current model in Fig. 4(a).
  - Grounded mirror: the switching-current reduction is smaller, and the curve shifts to lower Ib without flattening. The maximum BCR is unaffected to much higher rf.
  - Operation up to 54 V peak at 70 MHz and up to 6 K. — [arXiv](https://arxiv.org/abs/2302.01462)
- **The residual rf effect with a grounded mirror is attributed to local heating, not induced current.**
  - After turning off the rf (45 V peak), the switching current measured within ~10 us implies the SNSPD was ~0.5 K above steady state.
  - The rf electrodes were only 350 nm Au, versus 6 um in real ion-trapping devices, so dissipation may be exaggerated.
  - The published version adds that the thin SiO2 under the mirror adds thermal resistance, and that a larger mirror may cool better, which could explain the difference between Fig. 3(b) and 3(c). — [arXiv](https://arxiv.org/abs/2302.01462); [NIST PDF](https://tf.nist.gov/general/pdf/3223.pdf)
- **Readout chain.**
  - Pulse decay time 25 ns, so kinetic inductance is 1.3 uH.
  - Bias through a 10 kΩ series resistor and bias tee. Output is amplified, low-pass filtered, and notch filtered to remove rf pickup.
  - rf resonators had 20x step-up at 68-72 MHz.
  - Cryostat base temperature 2.6 K. Illumination by 395 nm LEDs. — [arXiv](https://arxiv.org/abs/2302.01462)
- **Efficiency.**
  - RCWA: the Al mirror doubles normal-incidence absorption when the SiO2 thicknesses are chosen well. Al was chosen over Au for its better UV/blue reflectivity.
  - Standalone self-aligned fiber-coupled SNSPDs (same stack, bottom SiO2 optimized to 186 nm) reached a maximum SDE of 68% with the mirror and 40% without, at 395 nm and 2.5 K. — [arXiv](https://arxiv.org/abs/2302.01462)
- **Claimed improvement over Todaro 2021.** "An order of magnitude increase in tolerance to applied trapping rf potential" and "an increase of at least 2.5 K in operating temperature," with identical trap electrode geometry. Usable for ions with charge-to-mass ratio ≥ 0.01 e/u. NbTiN gives ~10x the critical current of MoSi and operation up to 7 K (their ref. 18). — [arXiv](https://arxiv.org/abs/2302.01462)
- **Required rf for 40Ca+.** 70 MHz at 40 V gives about 2 MHz axial and 5 MHz radial secular frequency. "Reducing the rf frequency will reduce the required rf amplitude proportionally." — [arXiv](https://arxiv.org/abs/2302.01462)

### Inferences
- **Check worth doing: compare 138Ba+ to Hampel's stated range.** Hampel claims usability down to q/m = 0.01 e/u (final summary paragraph) and gives the rf scaling rule for Ca+ (40 V at 70 MHz, with amplitude scaling proportionally to frequency). Secular frequency scales as ω_sec ∝ QV/(mΩ r0²). From this you can compute the rf amplitude Ba+ needs at your chosen Ω and compare it to the 54 V demonstrated.
- **Lower rf frequency also reduces induced currents and heating.** The capacitively induced current scales as I ∝ ΩCV. With V ∝ Ω, this gives I ∝ Ω², and resistive heating scales as P ∝ Ω⁴. Hampel identifies heating as the residual limit, so this is significant. This is my scaling argument, not a published measurement.
- **Grounding recipe to copy.** Open vias through the spacer to the Al and contact them with the same metal as the trap ground electrodes. Extend the mirror under the SNSPD leads, as the "large" mirror did. The large-vs-small comparison in Fig. 3(b,c) suggests a larger mirror also helps thermally.
- **The 212 nm bottom oxide was not optimal in my model.** In the trap device it was tuned for 397 nm with vacuum above the 130 nm cap. My TMM puts it far from the 395 nm optimum (A ≈ 0.32), versus A ≈ 0.61 for the 186 nm standalone stack. So the trap devices' in-situ efficiency was probably below the 68% standalone value, unless the effective-medium model misses something. [TMM; low confidence]

### Gaps
- **Switching-current numbers for the NbTiN devices** with and without rf appear only graphically in Fig. 3 and Fig. 4(b), not in the text. I could not read numeric values from the figures.
- **Field-reduction factors for the ITO and mesh cases (Fig. 2c,d)** are not quantified in the text. Only "roughly an order of magnitude" is given for the mirror alone.
- **Lead routing.** The text does not describe it beyond the large mirror running under the leads for several hundred um, and the leads being part of the 350 nm Au layer.
- **NbTiN Tc, PECVD deposition temperatures, and the exact via/contact layout** are not stated in the text.

---

## Q2. ITO in ion traps: Eltony 2013 and other uses; ITO optics at 493 nm; resistivity at 4 K; deposition and anneal; compatibility with NbN

### Takeaway
- Eltony et al. (MIT Chuang group) built surface traps with 400 nm room-temperature RF-sputtered ITO electrodes (lift-off, no anneal mentioned).
  - Transmission at 422 nm was ~60% (including the quartz substrate).
  - Resistivity was 1-2 x 10^-5 Ω·m (1-2 mΩ·cm).
  - They trapped 88Sr+ stably at about 6 K trap-surface temperature, with no measurable laser-induced charging.
- ITO stays metallic-like down to liquid-helium temperatures, with a small residual resistance ratio and a weak logarithmic upturn below ~25 K. So a grounded ITO film works as a shield at 5 K.
- At 493 nm, good ITO has n ≈ 1.84-1.97 and k ≈ 0.003-0.011, so a 20-80 nm film absorbs only ~0.3-3%.
- Room-temperature, as-deposited amorphous ITO is more absorbing and resistive. Crystallization needs roughly 200-250 °C.

### Cited Findings
**Eltony et al. 2013**
- **Verified citation.** A. M. Eltony, S. X. Wang, G. M. Akselrod, P. F. Herskind, I. L. Chuang, "Transparent ion trap with integrated photodetector," Appl. Phys. Lett. 102, 054106 (2013), DOI 10.1063/1.4790843, arXiv:1212.1443. — [arXiv](https://arxiv.org/abs/1212.1443)
- **Fabrication.**
  - Optical lithography (NR9-3000PY resist) on a quartz substrate.
  - ITO deposited by RF sputtering in argon at 0.5 Å/s, patterned by lift-off (RD6). The text mentions no anneal.
  - Transmission of ITO plus polished quartz, measured at 422 nm over 4 mm² at room temperature, averaged ~60%. That is "about 10% lower than expected for commercial films."
  - Resistivity was 1x10^-5 to 2x10^-5 Ω·m depending on the sputter run. The paper notes ITO resistivity is ~1000x that of trap metals. — [arXiv](https://arxiv.org/abs/1212.1443)
- **Thickness and Au overlay.** Both traps used 400 nm ITO for all electrodes.
  - ITO-4K: an extra 50 nm Au on the RF electrodes only, giving effective resistivity ~2x10^-8 Ω·m.
  - ITO-PD: only 5 nm Au on the RF electrodes, for ~60% transparency, giving ~3x10^-8 Ω·m.
  - Five-wire trap geometry, 35 MHz rf, 0.8-1.3 MHz secular frequencies, ~300 meV depth, ion 100 um above the surface. — [arXiv](https://arxiv.org/abs/1212.1443)
- **Cryogenic operation and charging.**
  - ITO-4K's trap surface was estimated at 6 K. Single 88Sr+ ions were held for several hours, comparable to metal traps.
  - Crashing a 405 nm or 461 nm beam (~5 mW/mm²) into the trap center for 10 min gave no significant change in micromotion amplitude. The authors conclude charging is not a major problem for cryogenic ITO traps.
  - The photodiode trap (ITO-PD) was run at 77 K because PIN photodiode responsivity drops from ~0.1 A/W to ~0.01 A/W at 4 K. — [arXiv](https://arxiv.org/abs/1212.1443)

**Other ion-trap and SNSPD ITO work**
- **Sedykh et al. 2025 (Technical Physics 2025, issue 9, p. 1577).** "Characteristics of a superconducting single-photon detector shielded by ITO under external electric field conditions." Groups: HSE, MISiS, Russian Quantum Center, Gol'tsman group.
  - Model surface ion trap with RF electrodes plus an ITO-shielded NbN SNSPD at 2.2 K.
  - rf of 0.01-2 V at 5-35 MHz.
  - Reports dark count rate and detection efficiency vs. induced RF field with the ITO shield. — [Ioffe journal page](https://journals.ioffe.ru/articles/61926)
- **Earlier Sedykh et al. paper**, cited in that reference list as Tech. Phys. 68(7), 908 (2023), DOI 10.61011/TP.2023.07.56637.88-23, on SNSPDs in an ion-trap model. — [Ioffe journal page (reference list)](https://journals.ioffe.ru/articles/61926)
- **Jansson et al. (PTB / Mehlstäubler group).** "Indium tin oxide combined with anti-reflective coatings with high transmittance for wavelengths < 400 nm," arXiv:2411.10361. The arXiv page lists the related DOI 10.1364/AO.547471 (Applied Optics).
  - Ion-beam sputtering below 150 °C.
  - ITO+AR system: sheet resistance 115 ± 5 Ω/sq, 80% transmittance at 370 nm, scattering 0.012 ± 0.002%.
  - The authors conclude these coatings are "suitable for ion trap experiments." — [arXiv](https://arxiv.org/abs/2411.10361)
- **Todaro et al. 2021 (Supplement)** recommends that a dielectric cap over the SNSPD be covered by a transparent shielding electrode, either a continuous film or a mesh. Exposed dielectric charges and perturbs the trap. The same layer would cut induced rf currents, the pulse "kick" to the ion, and electric-field noise from the meander and its circuitry. — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)

**ITO optical constants at 493 nm (refractiveindex.info datasets, interpolated by me from the database YAML files)**
- **Moerland & Hoogenboom**, Optica 3, 112 (2016): n = 1.965, k = 0.003 (n,k = 2.003, 0.005 at 450 nm; 1.925, 0.002 at 550 nm). — [refractiveindex.info Moerland](https://refractiveindex.info/?shelf=other&book=In2O3-SnO2&page=Moerland); [database](https://github.com/polyanskiy/refractiveindex.info-database)
- **König et al.**, ACS Nano 8, 6182 (2014), DOI 10.1021/nn501601e. Commercial 72 nm ITO on BK7, 15-25 Ω/sq: n = 1.921, k = 0.004. — [refractiveindex.info König](https://refractiveindex.info/?shelf=other&book=In2O3-SnO2&page=Konig)
- **Minenkov et al.**, ACS Appl. Mater. Interfaces (2024):
  - on glass: n = 1.915, k = 0.007
  - on Si, top: n = 1.949, k = 0.005
  - on Si, bottom: n = 1.844, k = 0.011
  - These are graded-film models. — [refractiveindex.info](https://refractiveindex.info/?shelf=other&book=In2O3-SnO2&page=Konig); [Minenkov et al. (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10895603/)

**ITO at cryogenic temperature**
- **Lin & Li review.** "Electronic conduction properties of indium tin oxide: single-particle and many-body transport," J. Phys.: Condens. Matter 26, 343201 (2014), arXiv:1702.07845. ITO is a "metallic-like" disordered conductor with a free-electron-like band and low carrier concentration. Slow electron-phonon relaxation gives a small residual resistance ratio. Transport is covered from 300 K to low T. — [arXiv](https://arxiv.org/abs/1702.07845)
- **Low-T upturn.** Sn-doped In2O3 films are metallic. Below ~25 K, resistivity rises slightly and logarithmically on cooling, from weak localization and electron-electron interaction. Inhomogeneous or granular films show different log-T behavior.
  - These statements come from search snippets of the Lin-group papers. I did not open the full texts.
  - One reactively sputtered film was reported to show a metal-insulator transition at ~110 K (arXiv:1610.08799). This is an outlier. — [arXiv 1202.1627](https://arxiv.org/pdf/1202.1627); [NYCU record](https://ir.lib.nycu.edu.tw/handle/11536/25635); [arXiv 1610.08799](https://arxiv.org/pdf/1610.08799)
- **Direct operational evidence.** Eltony's ITO electrodes held a trapped ion at about 6 K. — [arXiv](https://arxiv.org/abs/1212.1443)

**Low-temperature deposition and anneal**
- **Takayama (AVS 2002, TF-MoA9).** Room-temperature DC magnetron ITO, 260-280 nm, oxygen-annealed at 100-150 °C. Best resistivity 7x10^-4 Ω·cm after a 100 °C O2 anneal, with ~90% visible transmittance. These films were polycrystalline as deposited. — [AVS abstract](https://www2.avs.org/symposium2002/Papers/Paper_TF-MoA9.html)
- **Search-snippet trends (attribution to individual URLs uncertain; full texts not read).**
  - Room-temperature sputtered ITO is amorphous and becomes polycrystalline above ~200 °C, with lower resistivity and higher visible transmission.
  - In an air anneal, resistivity bottoms out at 6.0x10^-4 Ω·cm at 200 °C and then rises at higher temperature.
  - 300 °C anneals reach 2-3x10^-4 Ω·cm.
  - In-situ 200 °C deposition gave 24 Ω/sq crystalline films, while post-anneal needed ≥250 °C.
  - A patent reports 150 °C anneals (N2 or H2) do not improve transmittance, while 300-400 °C improve the short-wavelength side.
  - — [USQ record](https://research.usq.edu.au/item/q5x52/effect-of-different-thermo-treatment-at-relatively-low-temperatures-on-the-properties-of-indium-tin-oxide-thin-films); [NWPU record](https://pure.nwpu.edu.cn/en/publications/effects-of-air-annealing-on-the-structure-resistivity-infrared-em); [US patent 5808315](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5808315) (unverified attribution)

### Inferences
- **Sheet resistance estimates** (R_s = ρ/t):
  - Eltony's as-sputtered ITO (1-2 mΩ·cm): 400 nm gives 25-50 Ω/sq; 50 nm would give 200-400 Ω/sq.
  - Annealed ITO (~2-3x10^-4 Ω·cm): 50 nm gives about 40-60 Ω/sq.
  - Expect only a small change from 300 K to 5 K (small RRR, slight log upturn).
- **Absorption in the ITO layer** at 493 nm inside my optimized stack [TMM]:
  - 50 nm: ~0.7% with k = 0.003, ~2.5% with k = 0.011, ~6% with a hypothetical k = 0.03 (an assumed value for poorly oxidized room-temperature amorphous ITO), ~12% with k = 0.06.
  - So ITO stoichiometry matters more than thickness in the 20-60 nm range. Oxygen partial pressure during sputtering, or a 200-250 °C anneal, is the key lever.
- **ITO thickness choice: 40-60 nm.** In the optical design (Q3), a thin high-index ITO layer improves NbN absorption. A ~127 nm half-wave ITO (λ/2n) is optically "absent." 40-60 nm gives the best absorption [TMM] and roughly 40-400 Ω/sq.
- **Shielding needs low R_s only near the SNSPD.** The relevant time constant is the ITO-patch RC. For a 30x30 um patch over an 88 nm SiO2 cap, C ≈ 0.35 pF (ε_r = 3.9). With R ≈ 50-400 Ω this gives τ ≈ 20-140 ps. That is far shorter than 1/(70 MHz) and shorter than the ~1 ns SNSPD rise time, so the patch stays equipotential for both rf pickup and pulse-kick screening. [my estimate]
- **Useful numbers for deciding how far the ITO should extend** (my estimate). With 10 um PECVD SiO2 (ε_r ~ 4), the capacitance from an rf electrode to any ground plane beneath it is ≈ 3.5 fF/um².
  - Example: 2 x (100 um x 3 mm) of rf electrode is ≈ 2 pF. At 30 MHz and 100 V, that is ≈ 40 mA of displacement current returning through whichever ground layer lies underneath.
  - Dissipation is I²R, so compare the ITO sheet resistance (Q2: ~40-400 Ω/sq at 50 nm) with Al or Au.
  - Hampel identifies local rf heating as the residual limit (published version, discussion of Fig. 3b,c and Fig. 4b), so this I²R estimate is worth doing for the actual layout.
- **Compatibility with an underlying NbN film.** I found no direct study of ITO deposited on NbN SNSPDs. The precautions below are engineering judgment, not sourced results:
  - Keep the SiO2 cap continuous over the nanowire before ITO deposition. Todaro measured 12-30% MoSi resistance increases from later processing and recommended a cap.
  - Sputter at room temperature with modest O2 partial pressure.
  - Limit any anneal to ≤250-300 °C in N2/vacuum. NbN/NbTiN is deposited at ~500 °C (Hampel's NbTiN at 500 °C) and survives PECVD.
  - Re-check sheet resistance and switching current after the anneal.
- **Sanity check worth running on the target stack (per project CLAUDE.md, framed as a check, not a verdict).** List which material the ion "sees" directly above the SNSPD window, layer by layer. Compare that against the surface-charge remarks in the Hampel published version (paragraph after Fig. 2) and the Todaro Supplement (fabrication section, "transparent shielding electrode" paragraph). Also see the coherent-fringe result for the 10 um layer in Q3.

### Gaps
- **No primary ITO resistivity number at 4-5 K was extracted.** The Lin & Li full text was not opened. The qualitative conclusion (stays conductive, small RRR) is solid, and Eltony's 6 K operation confirms it.
- **No source gives n,k at 493 nm for room-temperature as-deposited amorphous ITO** versus annealed ITO. The k = 0.03 and 0.06 cases are hypothetical sensitivity cases.
- **Sedykh et al. 2025: quantitative results** (shielding factor, ITO thickness/resistance, efficiency change) and the article DOI were not retrieved. The Ioffe site has certificate errors, and only the abstract was read.
- **I found no Sandia or Clark-group paper using ITO trap electrodes.** Searches surfaced only Eltony (MIT), Jansson (PTB), and Sedykh (Russian Quantum Center). Mark any "Sandia ITO trap" claim as unverified.

---

## Q3. Optical constants at 493 nm and absorption-cavity design (TMM); typical NbN absorption with and without mirror

### Takeaway
At 493 nm:

| Material | n | k | Source |
|---|---|---|---|
| Al | 0.61 | 5.25 | McPeak (R ≈ 0.92 in vacuum) |
| Al | 0.79 | 5.97 | Rakić |
| Al | 0.47 | 4.72 | Cheng |
| SiO2 | 1.463 | 0 | Malitson |
| Si | 4.33 | 0.048 | Green 2008 |
| NbN | ≈ 2.11 | ≈ 2.00 | Banerjee 2018 |
| NbN | ≈ 2.50 | ≈ 2.51 | Medeiros 2019, interpolated |

My TMM design for 7 nm NbN at 50% fill factor gives the following polarization-averaged absorption:
- **Without ITO:** ≈ 40%, with spacer t1 ≈ 64-68 nm (first order) or ≈ 228-236 nm (second order).
- **With 50-60 nm ITO:** ≈ 53-54%, with cap t2 ≈ 80-90 nm or ≈ 250 nm.
- **Raising the fill factor** to 0.6 gives ≈ 63%. Going to 10 nm NbN gives ≈ 60%.
- **Without a mirror (Si below):** only ≈ 20-33%.

The literature anchor is Hampel's 68% vs 40% SDE at 395 nm with vs without an Al mirror.

### Cited Findings
- **Al.** McPeak et al., ACS Photonics 2, 326 (2015), DOI 10.1021/ph5004237: n = 0.605 + 5.245i at 493 nm. Rakić (refractiveindex.info "Rakic" Drude-Lorentz dataset): 0.787 + 5.966i. Cheng et al., ACS Nano 10, 9852 (2016), DOI 10.1021/acsnano.6b05556: 0.467 + 4.720i. — [refractiveindex.info Al McPeak](https://refractiveindex.info/?shelf=main&book=Al&page=McPeak); [database](https://github.com/polyanskiy/refractiveindex.info-database)
- **SiO2.** Malitson, JOSA 55, 1205 (1965), Sellmeier: n = 1.463 at 493 nm. Lemarchand thin-film data: 1.477. PECVD oxide is typically similar but should be measured. — [refractiveindex.info SiO2 Malitson](https://refractiveindex.info/?shelf=main&book=SiO2&page=Malitson)
- **Si.** Green, Sol. Energ. Mater. Sol. Cells 92, 1305 (2008): n = 4.333 + 0.048i at 493 nm. — [refractiveindex.info Si Green-2008](https://refractiveindex.info/?shelf=main&book=Si&page=Green-2008)
- **Au** (for an Au-mesh alternative). Johnson & Christy, PRB 6, 4370 (1972): n = 1.07 + 1.84i at 493 nm. Au is lossy in the blue, which is why Hampel chose Al. — [refractiveindex.info Au Johnson](https://refractiveindex.info/?shelf=main&book=Au&page=Johnson); [Hampel arXiv](https://arxiv.org/abs/2302.01462)
- **NbN, Banerjee et al.** "Optical properties of refractory metal based thin films," Opt. Mater. Express 8, 2072-2088 (2018). Open dataset at Glasgow, DOI 10.5525/gla.researchdata.637, file "optical constants_NbN_NbTiN_MoSi.xlsx." The sheet header says "5 nm thick, Sputtered."
  - NbN: n,k = 2.0997, 1.9832 at 490 nm and 2.1323, 2.0302 at 500 nm, so ≈ 2.11 + 2.00i at 493 nm.
  - NbN: 2.107 + 1.480i at 400 nm; 4.277 + 3.529i at 1550 nm.
  - NbTiN: ≈ 1.90 + 1.91i at 493 nm; ≈ 2.04 + 1.41i near 395 nm.
  - MoSi (no Si cap): ≈ 2.75 + 3.38i at 490 nm. — [Glasgow dataset](https://researchdata.gla.ac.uk/637); [eprint](https://eprints.gla.ac.uk/164939)
- **NbN, Medeiros et al. (MIT Berggren group).** "Measuring thickness in thin NbN films for superconducting devices," arXiv:1812.05559, Table 1, room-temperature reactive DC sputtered NbN:
  - 466 nm: n = 2.456, k = 2.487
  - 522 nm: n = 2.554, k = 2.536
  - 598 nm: n = 2.643, k = 3.047
  - 638 nm: n = 2.822, k = 3.197
  - Linear interpolation gives ≈ 2.50 + 2.51i at 493 nm.
  - The authors stress the constants are specific to their deposition conditions, and that n,k and thickness are strongly correlated in ellipsometry of absorbing films. — [ar5iv](https://ar5iv.labs.arxiv.org/html/1812.05559); [arXiv](https://arxiv.org/abs/1812.05559)
- **Mirror gain anchors.**
  - Hampel (NbTiN, 395 nm): RCWA predicts a factor-of-2 absorption enhancement from the Al mirror. Measured SDE is 68% with the mirror and 40% without. — [arXiv](https://arxiv.org/abs/2302.01462)
  - Todaro (MoSi 8 nm + 2 nm a-Si, 110/170 nm wire/pitch, 134 nm PECVD SiO2 on Si, no mirror): designed 72% average absorption at 313 nm by RCWA. Measured SDE was 48(2)% with rf on, extrapolated to 65(5)% without rf. Oxidation of the top 4 nm of MoSi would cut the absorption probability from 72% to 65%. — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)

### Inferences (my TMM)
Method:
- Normal incidence, coherent thin layers.
- The meander is modeled as a uniaxial effective medium:
  - TE (E parallel to wires): ε = fε_NbN + (1-f)ε_SiO2.
  - TM: 1/ε = f/ε_NbN + (1-f)/ε_SiO2.
  - Results are the TE/TM average.
- Light enters through the 10 um SiO2. The vacuum/SiO2 interface (R = 3.5%) is treated incoherently, with multiple bounces.
- The Al is 100 nm thick, effectively opaque: 50 nm transmits only 0.12%, so Hampel's 50 nm Al is already opaque.
- Inputs at 493 nm: NbN = Banerjee 2.11 + 2.00i unless noted; Al = McPeak; ITO = Moerland.

Results:
- **Validation against Hampel at 395 nm** (NbTiN 10 nm, f = 0.5):

  | Stack | TMM absorption |
  |---|---|
  | Standalone, mirror (186 nm bottom) | 0.61 |
  | No mirror (362 nm SiO2 on Si) | 0.21 |
  | Measured, for comparison | 0.68 (mirror) / 0.40 (no mirror) |

  The mirror-stack number is reasonable. No-mirror is underestimated, since their no-mirror stack is not specified and the effective-medium model is approximate. Use RCWA/FDTD for sign-off.
- **Spacer t1 (Al to NbN), no ITO, NbN 7 nm.** Absorption vs t1 is periodic with period λ/(2n) ≈ 168 nm:

  | t1 (nm) | A |
  |---|---|
  | 52 | 0.38 |
  | 68 | 0.40 |
  | 84 | 0.37 |
  | 148 | 0.003 (node: NbN at the standing-wave minimum) |
  | 228-244 | 0.39-0.40 |

  First-order t1 ≈ 65 ± 15 nm is the most tolerant choice.
- **Optimum absorption by NbN thickness and dataset** (f = 0.5, best t1/t2):

  | NbN | No ITO | 50 nm ITO |
  |---|---|---|
  | 5 nm | 0.32 | 0.44 |
  | 7 nm | 0.40 | 0.53 |
  | 10 nm | 0.50 | 0.62 |
  | 5 nm, Medeiros constants | 0.37 | 0.48 |
  | 7 nm, Medeiros constants | 0.45 | 0.55 |
  | 10 nm, Medeiros constants | 0.52 | 0.60 |

- **ITO thickness sweep** (NbN 7 nm, cap t2 re-optimized; A_NbN with ITO absorption in brackets):

  | ITO thickness | k = 0.003 (Moerland) | k = 0.011 (Minenkov) |
  |---|---|---|
  | 0 nm | 0.40 | 0.40 |
  | 20 nm | 0.47 [0.3%] | 0.45 [1.1%] |
  | 40 nm | 0.52 [0.6%] | 0.49 [2.2%] |
  | 50 nm | 0.53 [0.7%] | 0.50 [2.5%] |
  | 60 nm | 0.54 [0.8%] | 0.50 [3%] |
  | 80 nm | 0.53 [1.0%] | 0.50 [3.4%] |
  | 100 nm | 0.48 [1.2%] | 0.47 [4.2%] |
  | 127 nm (half-wave, "absent") | 0.40 [1.5%] | 0.40 [5.1%] |
  | 150 nm | 0.48 [2.0%] | 0.42 [6.5%] |

  The ITO acts as a high-index matching layer between the cap and the thick oxide. Hypothetical k = 0.03 with 50 nm gives A_NbN 0.51 and A_ITO 6%. k = 0.06 gives 0.49 and 12%.
- **Recommended design point:** Al ≥ 50 nm / SiO2 t1 ≈ 68 nm / NbN 7 nm (f ≈ 0.5-0.6) / SiO2 cap t2 ≈ 88 nm / ITO 50 nm / thick SiO2. Predicted A ≈ 0.53 at f = 0.5.
  - Tolerance: ±10 nm on t1 or t2 costs ≤ 0.07 absolute. For example, t1 = 68, t2 = 98 gives 0.51; t1 = 78, t2 = 88 gives 0.50; t1 = 58, t2 = 98 gives 0.53.
  - Polarization split at f = 0.5: TE 0.77, TM 0.30. At f = 0.4: 0.44 average. At f = 0.6: 0.63 average.
  - Ion dipole emission is polarization-structured, so the TE/TM average is only an approximation (Todaro measured angle and polarization dependence of SDE).
- **Coherence of the 10 um oxide.**
  - The ion's 493 nm emission is narrowband, so the 10 um PECVD layer can act coherently. Fringe period is Δλ ≈ λ²/(2nd) ≈ 8 nm, or a thickness change of λ/(2n) ≈ 168 nm.
  - Treated fully coherently, absorption swings between 0.455 and 0.625 (mean 0.53) as the oxide thickness varies over one fringe.
  - In practice, the angular spread of collected photons and ±1-5% PECVD thickness nonuniformity will partly wash this out. Better: remove the thick oxide over the SNSPD (see Q2), or add an AR coating.
- **Spectral selectivity is weak.** The cavity is low-Q. For the same 50 nm ITO design, A = 0.47 at 455 nm, 0.53 at 493 nm, 0.48 at 532 nm, 0.33 at 614 nm, 0.30 at 650 nm, and 0.27 at 700 nm.
  - So scattered 650 nm Ba+ repump light is absorbed at ~55% of the 493 nm efficiency. The optical stack provides only about 1.8x rejection, so stray-light control and filtering, if any, must come from elsewhere.
  - Without ITO, the ratio is closer to 1.2x (0.40 vs 0.34).
- **Mirror vs no mirror at 493 nm.** With Si below the thermal oxide instead of Al, the best absorption is 0.20 / 0.26 / 0.33 for 5 / 7 / 10 nm NbN. The Al mirror gives roughly 1.5-2x, consistent with Hampel's factor of ~2.
- **Low temperature.** The Al reflectivity and NbN n,k used here are room-temperature values. Al reflectivity typically improves slightly on cooling, and NbN optical constants at 493 nm are not expected to change much (photon energy ≫ gap). This is unverified.

### Gaps
- **No cryogenic n,k data at 493 nm** for NbN or Al were found.
- **The two NbN datasets differ by ~20% in n and k at 493 nm.** Ultrathin NbN optical constants depend on deposition (stoichiometry, thickness, substrate). Measure your own film by ellipsometry on a thickness series, as Medeiros recommends.
- **The effective-medium TMM is not RCWA.** With a pitch of 160-200 nm vs λ/n ≈ 337 nm, the meander is only marginally sub-wavelength. Final numbers should come from RCWA, as Hampel and Todaro did, or from FDTD.
- **Scripts and data** are in the session scratchpad:
  - Scripts: tmm_stack.py, run1.py, run2.py, run3.py in C:\Users\willi\AppData\Local\Temp\claude\C--Users-willi-Repos-6-2540\2462feda-17d8-4bbb-b4c9-ed087db8a35f\scratchpad\
  - NbN dataset: ...\scratchpad\gla\nbn.xlsx
  - refractiveindex.info files: ...\scratchpad\ri\db\

---

## Q4. RF pickup physics, switching-current suppression, mitigation by grounded planes, lead routing

### Takeaway
Trap rf couples capacitively to the nanowire, through C_RN (rf electrode to nanowire segment), and to the leads, through C_RL. This drives position-dependent rf currents that add to the dc bias. The maximum usable bias I_m drops by the peak induced current.

In Todaro 2021 (MoSi, 8.8 V peak at 67 MHz, 3.45 K), the switching current fell from ~8.9 uA to I_m ≈ 5.3 uA. The reduction of ~3.6 uA was mostly spatially varying induced current (I1 ≈ 3.5 uA, versus a uniform component I0 ≈ 0.9 uA).

Mitigations:
- Capacitively shield the wire, which reduces C_RN: grounded mirror below plus a grounded transparent layer above.
- Use symmetric termination, low C_RL, and higher kinetic inductance.
- Use higher-Ic material such as NbTiN or NbN.

Hampel's grounded Al mirror removed the induced-current signature. What remained was rf heating.

### Cited Findings
- **Todaro et al.** "State readout of a trapped ion qubit using a trap-integrated superconducting photon detector," PRL 126, 010501 (2021), DOI 10.1103/PhysRevLett.126.010501, arXiv:2008.00065 (verified). — [arXiv](https://arxiv.org/abs/2008.00065); [APS](https://link.aps.org/doi/10.1103/PhysRevLett.126.010501)
- **Switching current.**
  - Switching current ≈ 8.9 uA at 3.45 K. Trap rf was 8.8 V peak at 67.03 MHz.
  - With rf on, the maximum usable bias was I_m ≈ 5.3 uA for the Fig. 2 data, and ≈ 4.8 uA for the later SDE-calibration data taken at a higher cryostat temperature.
  - The reduction max|I_rf| ≈ 3.6 uA. Fit: I0 = 0.9(1) uA uniform, I1 = 3.5(2) uA spatially varying, K = 40 segments.
  - Max bright counts with rf on were only 17% lower than with rf off.
  - The SNSPD operated with rf up to a trap temperature of 3.65 K (Tc of MoSi is 5.2 K). — [arXiv (main text + Supplement Fig. S4, Eq. S1)](https://arxiv.org/abs/2008.00065)
- **Circuit model (Supplement Fig. S4).**
  - The nanowire is modeled as an LC transmission line (L_total = 2.2 uH from the pulse decay) with capacitance C_RN per segment to the rf electrode and C_NG to ground.
  - Leads have C_RL to rf, L_L ≈ 5 nH, and R_L ≈ 5 Ω. One lead is grounded off-chip; the other sees 50 Ω.
  - |Z_CRN| ≈ 10^6 |Z_LN| and |Z_CNG| ≈ 10^4 |Z_LN| at the rf frequency.
  - A spatially uniform "cancellation" tone cannot cancel the dominant spatially varying component.
  - Recommended fixes:
    - Reduce C_RN by capacitive shielding.
    - Reduce the uniform component with symmetric termination, lower C_RL, and higher SNSPD inductance.
    - Use materials with wider SDE plateaus. — [arXiv](https://arxiv.org/abs/2008.00065)
- **Lead design and readout.**
  - Leads were made "much narrower than typical SNSPD leads" to minimize capacitive coupling to the rf electrodes. They were then thickened with 350 nm Au to lower series resistance and avoid latching.
  - The rf pickup on the output was "several times larger" than the SNSPD pulses. It was removed by a 7th-order Bessel notch (40 dB at f_rf, 14 MHz 3 dB bandwidth) plus a 25 MHz Gaussian low-pass (18 dB more at f_rf).
  - Pulse heights varied up to 3x because of rf-modulated bias. — [arXiv Supplement](https://arxiv.org/abs/2008.00065)
- **Hampel 2023.**
  - Floating Al mirror: the switching current is reduced with rf and the BCR curve flattens, fitting the induced-current model (Fig. 4a).
  - Grounded mirror: smaller switching-current reduction and no flattening. The model "suggests that almost no induced rf currents are present."
  - The remaining shift is heating-like (Fig. 4b comparison with temperature).
  - Simulated rf field at the nanowire falls about 10x with a grounded mirror, and further with a top ITO or Au mesh (Fig. 2). — [arXiv](https://arxiv.org/abs/2302.01462); [NIST PDF](https://tf.nist.gov/general/pdf/3223.pdf)
- **Sedykh et al. 2025** measured dark count rate and detection efficiency of an ITO-shielded NbN SNSPD vs. induced RF field (0.01-2 V, 5-35 MHz, 2.2 K) in a trap model. Numbers not retrieved. — [Ioffe](https://journals.ioffe.ru/articles/61926)

### Inferences
- **Why a mirror-plus-ITO sandwich works.** With grounded conductors above (ITO) and below (Al) a ~150 nm-thick dielectric containing the nanowire, field lines from the rf electrode terminate on the grounds. C_RN collapses, and what is left is fringing through the gaps at the sandwich edge.
  - For pure capacitive (E-field) shielding, conductivity only needs to be high enough that the shield's RC ≪ 1/f_rf, which holds by orders of magnitude for 50-400 Ω/sq ITO (Q2).
  - Skin depth is irrelevant here: about 85 um for ITO at 70 MHz with ρ = 2x10^-6 Ω·m, versus 50 nm thickness. The shield does not block magnetic fields, but coupling is dominated by C_RN.
- **Routing rules derived from the model.**
  - (1) Run both leads as a tightly coupled pair, ideally coplanar or stacked, between the Al ground and a top ground, so the rf-induced common-mode is equal on both.
  - (2) Terminate symmetrically, for example a differential or balanced readout, or equal impedances. This suppresses the uniform component I0.
  - (3) Route leads perpendicular to and away from rf electrodes, crossing only over the Al ground.
  - (4) Extend the Al ground under the leads for hundreds of um, as Hampel's "large mirror" did.
  - (5) Keep the ITO and Al grounds tied together at many points around the SNSPD (via ring) to avoid slot-antenna or ground-loop paths.
  - These are design inferences from the Todaro and Hampel circuit models.
- **Material headroom.** NbN at 5 K should give a switching current of order tens of uA for ~100 nm wide, 5-7 nm films. Hampel cites ~10x MoSi for NbTiN. Any residual induced current of a few uA is then a much smaller fraction of Isw. I did not verify NbN Isw values at 5 K here.

### Gaps
- **No numeric pickup reduction** (dB or uA) has been published for a fabricated ITO top shield. Hampel's ITO case is simulation only. Sedykh's numbers were not retrieved.
- **The NbN switching current and Tc at 5 K for 5-7 nm films** were not researched here. They are probably covered by a parallel SNSPD-materials researcher.

---

## Q5. SNSPD clicks perturbing the ion (pulse "kick") and shielding by a grounded transparent layer

### Takeaway
Todaro measured 0.009(5) motional quanta per SNSPD count on a 5.3 MHz axial mode, for an ion over an unshielded MoSi SNSPD. This is negligible during fluorescence readout. It dominated heating during Raman operations, where stray light makes the SNSPD click; this blocked Raman sideband cooling over the detector. The SNSPD even clicks with bias off when rf is on.

Both Todaro and Hampel propose a grounded transparent top electrode (ITO or mesh) to screen the pulse fields. Hampel adds that it also prevents surface charging of the SiO2.

### Cited Findings
- **Mechanism and measurement.** During a pulse, part of the nanowire stays at ground while the rest follows the output voltage, giving an impulsive E-field "kick."
  - The measured heating was 0.009(5) quanta per count (5.3 MHz axial mode, zone D, over the SNSPD).
  - The detector "will occasionally pulse in response to photons" even with bias off when trap rf is on.
  - "The addition of optically transparent SNSPD shielding electrodes may permit operations with high-power Raman beams" in SNSPD zones. — [Todaro arXiv](https://arxiv.org/abs/2008.00065)
- **Motional heating over the detector.** 113(14) quanta/s at 5.3 MHz over the SNSPD, versus 63(6) quanta/s at 2 MHz in zone B over gold. Scaled, electric-field noise over the SNSPD was about 6x higher than over gold, but still state of the art. — [Todaro arXiv](https://arxiv.org/abs/2008.00065)
- **Supplement recommendation.** A top transparent conductor would reduce "the electric field 'kick' at the ion due to SNSPD pulses, and any electric field noise at the ion originating from the meander or its bias and readout circuitry." — [Todaro arXiv](https://arxiv.org/abs/2008.00065)
- **Hampel.** "The top electrical shielding layer both protects the SNSPD from trapping rf as well as shielding the ion from electric fields due to SNSPD pulses." SNSPD output pulses also heat the ion less than SPAD pulses because they are smaller. — [arXiv](https://arxiv.org/abs/2302.01462); [NIST PDF](https://tf.nist.gov/general/pdf/3223.pdf)
- **Pulse size.** Pulse height is the shunt impedance (50 Ω) times the instantaneous bias. Rise time is ~1 ns unfiltered. — [Todaro Supplement](https://arxiv.org/abs/2008.00065)

### Inferences
- **Pulse amplitude.** With I_b ~ 10-20 uA for NbN into 50 Ω, the pulse is ~0.5-1 mV, about 2x Todaro's MoSi pulses (~5 uA x 50 Ω ≈ 0.25 mV) for the same geometry. Unshielded kick heating per click scales roughly as V², so NbN without a shield could reach ~0.04 quanta per click. This is a scaling estimate.
- **Shield RC.** A grounded ITO patch with RC ~ 20-140 ps (Q2) is equipotential on the ns pulse timescale. It should therefore cut the dipole field at the ion by a large factor, limited by fringing at the patch edge and any ITO-to-ground inductance.
  - Ground the ITO with a low-inductance via ring, not a single thin trace.
  - Make the ITO patch extend past the meander and the lead region under the ion by more than the ion height. This is a design inference.
- **Bias gating.** Switching the bias off during Raman and other sensitive operations (as Todaro did) plus the shield are complementary. With rf on and bias off, clicks still occur, so the shield matters even with gated bias.

### Gaps
- **No published measurement of kick heating with an ITO or mesh shield** in place was found.
- **No calculation of the residual field at a typical ion height** (50-100 um) for a shielded geometry was found.
