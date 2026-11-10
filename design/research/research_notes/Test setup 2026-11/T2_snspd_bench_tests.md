> **Claude-authored.** Reading pointers for how other groups tested trap-integrated SNSPDs (bench and RF tests), 2026-11-10.

# T2: how trap-integrated SNSPDs were tested

**What was opened.** Each source below was read through a summarising tool (WebFetch on the arXiv HTML page, `https://arxiv.org/html/<id>`, and the arXiv abstract page for identifiers). None of the text was read directly, so every number from these fetches is tagged `[verify]`. Section, figure and page labels are as the summary gave them; check them in the PDF. The Todaro supplement is inside the arXiv v1 PDF (`arXiv:2008.00065`, pp. 8–15); its labels are "Supp." as the summary gave them.

**Repo notes used as a starting point (not checked against the source here):** [`todaro_slichter.md`](../Trap%20integrated%20SNSPD%20design/todaro_slichter.md), [`rf_tolerance.md`](../SNSPD%20geometry%20audit/rf_tolerance.md), [`02_CRYOGENIC.md`](../../../fab/tests/02_CRYOGENIC.md), [`03_READOUT.md`](../../../fab/tests/03_READOUT.md).

**Identifiers, all checked on the arXiv abstract page in this session:**

| Key | Identifier confirmed | Title and authors as shown |
|---|---|---|
| `Slichter2017` | arXiv:1611.09949 (v2); Opt. Express 25, 8705–8720 (2017); DOI 10.1364/OE.25.008705 (listed as related) | "UV-sensitive superconducting nanowire single photon detectors for integration in an ion trap"; D. H. Slichter, V. B. Verma, D. Leibfried, R. P. Mirin, S. W. Nam, D. J. Wineland |
| `Todaro2021` | arXiv:2008.00065 (v1); PRL 126, 010501 (2021); DOI 10.1103/PhysRevLett.126.010501 | "State readout of a trapped ion qubit using a trap-integrated superconducting photon detector"; S. L. Todaro et al. (10 authors, as in the bib) |
| `Hampel2023` | arXiv:2302.01462; APL 122, 174001 (2023); DOI 10.1063/5.0145077 | "Trap-integrated superconducting nanowire single-photon detectors with improved RF tolerance for trapped-ion qubit state readout"; B. Hampel, D. H. Slichter, D. Leibfried, R. P. Mirin, S. W. Nam, V. B. Verma. The abstract says the detector is **NbTiN**, not NbN. |

The Todaro thesis (`TodaroThesis2020`) was not opened in this session.

## Checked against the PDFs (2026-11-10)

Two of the three papers were then read directly from the arXiv PDF, on the pages named. For the items below the `[verify]` tag in the tables no longer applies. Everything else in this note is still as the summarising tool gave it.

| Source and pages read | Confirmed on the page | Correction to the tables below |
|---|---|---|
| Hampel 2023, arXiv:2302.01462, pages 2–3 | Variable-temperature cryostat, base 2.6 K. Cryogenic 395 nm LEDs flood the samples; no ion. RF through resonators with a step-up of 20 at 68–72 MHz. Bias from a low-noise voltage source and a 10 kΩ series resistor through the low-frequency port of a bias tee; output amplified, low-pass and notch filtered, to an oscilloscope or counter. Decay about 25 ns, 1.3 µH. Fig. 3 holds the count rates against bias for the mirror cases. | None. Useful extra facts on the same pages: the detector is 10 nm NbTiN; the electrodes and the SNSPD leads are one 350 nm evaporated Au layer made by lift-off; the substrate is Si above 20 kΩ·cm; the mirror is 50 nm evaporated Al. |
| Slichter 2017, arXiv:1611.09949, pages 9–11 | Stand-alone detector on an ADR, fibre-coupled 315 nm LED, room-temperature bias tee, amplifier chain with 51 dB total gain, pulse counter or oscilloscope (Sec. 4, Fig. 3). Trap-electrode device at 3.8 K with a free-space LED on the 3 K stage 36 mm away, because a fibre ferrule would disturb the RF field; half-wave coaxial resonator at 46.23 MHz with Q = 27; 25 V peak; no ion. | **Fig. 4 is the circuit figure** for the RF test (LED, bias tee, amplifier, couplers for the cancellation tones, resonator, power meter). The table row that says there is no circuit figure is wrong. The detectors in this paper are MoSi, not NbN. |

Not checked against a PDF: every Todaro 2021 entry, and the Slichter figure numbers above Fig. 4.

---

## Slichter 2017 (`Slichter2017`)

**Opened:** arXiv HTML `https://arxiv.org/html/1611.09949` through a summarising tool; abstract page for identifiers. Section headings as the summary gave them: 1 Introduction; 2 Integrating an SNSPD with a surface electrode ion trap; 3 Design and fabrication; 4 Experimental results; 5 Conclusion; Appendix A (induced rf currents). Figure numbers as the summary gave them. **Readable: text and figure labels, no numbers read off plots.**

| Question | Where in the source | What is there |
|---|---|---|
| 1. Device tested | Sec. 4, Fig. 3 (stand-alone); Sec. 4, Figs. 4–7 (trap-integrated) | Stand-alone: fibre-coupled SNSPD [verify]. Trap-integrated: SNSPD on a trap chip, tested with LED light [verify]. No trapped ion was measured. The ion is only modelled ("assuming a single 9Be+ ion") [verify]. |
| 2. Cryostat and light | Sec. 4 (stand-alone: "between 250 mK and 3.2 K", ADR) | Adiabatic demagnetization refrigerator (ADR). Stand-alone: UV LED at room temperature, 315 nm, FWHM 10 nm, butt-coupled to a single-mode fibre [verify]. Trap-integrated: free-space LED on the 3 K stage about 36 mm away, 308 nm at 3.8 K, FWHM 6 nm; a fibre was not used because the ferrule "would distort the rf fields" [verify]. Device held at 3.8 ± 0.05 K (Sec. 4) [verify]. |
| 3. Bias and readout chain | Sec. 4 (text on the stand-alone and trap-integrated set-ups) | Bias through a room-temperature bias tee. Output to a low-noise amplifier chain with "a total gain of 51 dB" (stand-alone set-up) [verify]. Two 20 dB directional couplers, one before the bias tee and one after the amplifiers, for cancellation tones [verify]. Bias source, bias resistor, filter corners and amplifier bandwidth are **not stated** in the summary. Output to a pulse counter or oscilloscope. No circuit figure. |
| 4. RF applied and count-rate or switching-current figure | Sec. 4, Fig. 6 | rf electrode connected to a half-wave coaxial resonator; 46.23 MHz, resonator Q = 27; V_pk = 25 V at the electrode, about +23 dBm at the resonator input [verify]. Fig. 6 gives count rate and background vs bias with rf off, rf on and rf on with cancellation. Text: I_sw 11.5 µA (rf off), 7.6 µA (rf on), 8.7 µA (cancellation); see the same section [verify]. Fig. 5 is the 4.3 K, rf-off count rate [verify]. Fig. 7 is a schematic, not data [verify]. |
| 5. Measurements and figures | Sec. 4, Figs. 5–6 | I–V / switching current: Fig. 6 and text (Sec. 4). Count rate and background vs bias: Fig. 6 (rf off, rf on, cancellation) and Fig. 5 (4.3 K, rf off) [verify]. Dark-count figure, timing jitter and efficiency calibration: not stated in the fetched summary; check the PDF. |
| 6. Without a trapped ion, or simpler structure | Sec. 3 (first sentence on the stand-alone detector); Sec. 4 | Yes. The stand-alone detector was built first "for calibrated tests of detector SDE and dark count performance" (Sec. 3) [verify]. All trap-integrated data were taken with the LED and no ion (Sec. 4) [verify]. Well depth and frequencies are calculated for an ion only (Sec. 4) [verify]. |

---

## Todaro 2021 (`Todaro2021`), PRL body and Supplemental Material

**Opened:** arXiv HTML `https://arxiv.org/html/2008.00065` through a summarising tool; abstract page for identifiers. The PRL body and the Supplement are both in the arXiv v1 PDF. I did not open the published PRL page, so PRL page numbers are as the summary gave them. **Readable: text and figure labels only.** Supplement labels as the summary gave them: §I.1 "Trap fabrication", §I.2 "Experimental apparatus" and readout, §I.3, §I.5, §I.6 (Eq. S6). Repo notes also cite Supp. Figs. S1–S7 and Eq. S1.

| Question | Where in the source | What is there |
|---|---|---|
| 1. Device tested | Main text p. 2 ("Trap configuration"); Supp. §I.1, Fig. S1 | Trap-integrated SNSPD on a linear five-wire trap with a 9Be+ ion. The readout data are from trapped ions [verify]. Fig. S1 is a photograph of the chip (134 nm SiO₂; 8 nm Mo₀.₇₅Si₀.₂₅ capped with 2 nm Si; 110 nm wires on a 170 nm pitch; 22 µm × 20 µm active area; 6 µm electroplated Au; "bowtie" substrate) [verify]. |
| 2. Cryostat and light | Main text p. 2 ("Trap configuration"); Supp. §I.2 | Closed-cycle ultra-high-vacuum cryostat at ≈ 3.5 K; nominal 3.45 K, drifting to 3.57 K over months [verify]. Trap rf at 3.65 K max [verify]. Light is free space: 313 nm beams in the trap plane at 45° to the axis (main text p. 2, Fig. 1(b)) [verify]. "No intervening optical elements between the ion and the detector" (abstract) [verify]. A separate NA = 0.38 objective feeds an EMCCD or PMT, not the SNSPD (Supp. §I.2) [verify]. |
| 3. Bias and readout chain | Supp. §I.2 and Fig. S2; main text, SNSPD readout paragraph after Fig. 2 | Bias: an AWG pulse, attenuated, into the DC port of a bias tee, ramped over 11 µs (Supp. §I.2, Fig. S2) [verify]. The bias resistor is **not stated** in the fetched text. The repo note `todaro_slichter.md` gives a 10 kΩ series resistor and 100 mV → 1.05 µA; that is not confirmed here [verify]. Amplifiers: 46 dB gain, 1 MHz–1 GHz (Supp. §I.2, Fig. S2) [verify]. Filters: 7th-order Bessel notch, 40 dB at the trap rf, 3 dB bandwidth 14 MHz; then a Gaussian low-pass, f₃dB = 25 MHz, adding 18 dB at the rf (Supp. §I.2, Fig. S2) [verify]. Comparator: Schmitt trigger; counted by ARTIQ; timestamps at 1 ns (main text, SNSPD readout paragraph after Fig. 2) [verify]. Circuit figure: Supp. Fig. S2. |
| 4. RF applied; switching-current figure | Main text p. 2 ("Trap configuration"); main text p. 3, Fig. 2 | Trap rf: 8.8 V peak at 67.03 MHz (main text p. 2) [verify]. Fig. 2 and its text: switching current ≈ 8.9 µA with rf off at 3.45 K; the rf lowers the maximum usable bias I_m, which is ≈ 5.3 µA in the Fig. 2 data; maximum bright counts with rf on are 17 % lower (main text p. 3, Fig. 2) [verify]. §I.3: rf-induced reduction of I_m ≈ 3.6 µA [verify]. Count rate vs bias with rf on: Fig. 2 (main text p. 3) [verify]. |
| 5. Measurements and figures | Main text p. 3 Fig. 2; calibration paragraph after Fig. 2; Supp. Figs. S3, S5; main text p. 4 | I–V and I_sw: Fig. 2, Supp. §I.2 [verify]. Count rate vs bias: Fig. 2 [verify]. Dark counts: below 10⁻² per detection for I_b at least about 1 µA below I_m (Fig. 2 discussion) [verify]. Timing: rise time about 1 ns rf off and about 10 ns with filters; pulse heights vary up to ×3 with rf (Supp. Fig. S3) [verify]; g⁽²⁾ minimum at 28 ns (Supp. Fig. S5) [verify]. Efficiency calibration: calibration paragraph after Fig. 2; SDE 48(2) % with rf on, I_b = 4 µA; maximum without rf 65(5) % vs design 72 % (calibration paragraph after Fig. 2) [verify]. Collection fraction 2.0(1) %, Eq. S6 and main text p. 2 [verify]. Count rate vs lateral displacement: Fig. 4 (main text pp. 4–5); the figure number is named in the fetched text, the content is from the repo note [verify]. |
| 6. Without a trapped ion, or simpler structure | Main text, Fig. 2 discussion; Supp. §I.2 (ion-height calibration) | Dark counts were taken with the laser off (Fig. 2 discussion) [verify]. Laser scatter stands in for ion fluorescence for the bright counts (Fig. 2 discussion) [verify]. Beam scatter off the trap surface is used to calibrate ion height (Supp. §I.2) [verify]. The "detector with an ion" data are all with an ion; no separate test chip is described in the fetched text. |

**Discrepancy to check in the PDF.** The summary gives the bias resistor as "not stated". The repo note gives 10 kΩ. This is the only source of that value in the repo (`todaro_slichter.md`).

---

## Hampel 2023 (`Hampel2023`)

**Opened:** arXiv HTML `https://arxiv.org/html/2302.01462` through a summarising tool; abstract page for identifiers. Figure numbers as the summary gave them. **Readable: text and figure labels only. Figure values are not read off plots here.** The SPIE 2024 companion (Proc. SPIE 13025, 1302506, doi 10.1117/12.3014455) is not in the bib and was not opened in this session.

| Question | Where in the source | What is there |
|---|---|---|
| 1. Device tested | Measurements section; Fig. 1 (photomicrograph); Fig. 2(b) | Trap-integrated NbTiN SNSPD over a grounded Al mirror on a linear surface-electrode trap (Fig. 1) [verify]. Stand-alone fibre-coupled SNSPD with a 186 nm bottom SiO₂ layer, described only in text near the end of the results (no figure) [verify]. No measurement in the text is made with a trapped ion; ion statements are predictions from Ref. 7 [verify]. |
| 2. Cryostat and light | Measurements section (text, no figure) | Variable-temperature cryostat, base 2.6 K (measurements section) [verify]. Trap data at 4.5 K (Fig. 3(a)–(c)) and 6 K (Fig. 3(d)) [verify]. Trap devices: "Cryogenically-operated LEDs with a peak wavelength of 395 nm provided flood illumination" (measurements section, no figure) [verify]. Stand-alone: 395 nm LED, fibre butt-coupled at cryogenic temperature (text, no figure) [verify]. |
| 3. Bias and readout chain | Measurements section (text); Fig. 1 (bias current I_b marked) | Bias: "a low-noise voltage source and a 10 kΩ series resistor through the low-frequency port of a bias tee" (text, no figure) [verify]. Output from the high-frequency port of the bias tee, "amplified, lowpass-filtered and notch filtered", then to an oscilloscope or counter (text) [verify]. Amplifier gain, bandwidth and filter corners are **not stated** in the summary. Decay time ~25 ns and kinetic inductance 1.3 µH (text) [verify]. No figure shows the readout circuit. |
| 4. RF applied; switching-current figure | Measurements section (text); Fig. 2 (simulation); Fig. 3 | RF on the rf electrodes (red in Fig. 1) through resonators with step-up 20 and resonance 68–72 MHz, driven by an amplified generator (text) [verify]. Simulation: 100 V at 70 MHz (Fig. 2) [verify]. Measured amplitudes appear only in the Fig. 3 labels; the text uses 45 V for the heating test and the abstract gives "up to 54 V" at 70 MHz [verify]. Switching current and BCR vs rf: Fig. 3(a)–(d). |
| 5. Measurements and figures | Fig. 2; Fig. 3(a)–(d); Fig. 4(a), (b); text on heating | Fig. 3(a) floating large mirror, 4.5 K; Fig. 3(b) grounded large mirror, 4.5 K; Fig. 3(c) grounded small mirror, 4.5 K; Fig. 3(d) grounded large mirror, 6 K [verify]. Fig. 4(a): induced-current model fit to Fig. 3(a) [verify]. Fig. 4(b): BCR and DCR vs bias with no rf, several temperatures [verify]. Heating test: after 45 V rf is switched off, the switching current over ~10 µs gives a rise of about 0.5 K (text, no figure) [verify]. Stand-alone SDE: 68 % with the Al mirror and 40 % without, both at 2.5 K (text, no figure) [verify]. Timing jitter and dark-count numbers: not in the summary. |
| 6. Without a trapped ion, or simpler structure | Measurements section; Fig. 2 (2-D FEM) | Yes. The trap-chip RF tests (Figs. 3–4) use LED light on trap chips with no ion [verify]. Stand-alone SNSPDs with no trap are used for calibrated SDE [verify]. Fig. 2 is a 2-D finite-element field map for unshielded, Al-mirror, Au-mesh and ITO cases; the text says the field is reduced "roughly an order of magnitude" by the mirror [verify]. |

---

## Minimum equipment each measurement needs

Built only from the tables above. An empty cell means the source does not state it. Each cell carries its pointer. `[verify]` as above.

| Measurement | Cryostat and temperature | Light source and path | Bias source, bias resistor and bias tee | Amplifier and filter | Counter or comparator | RF drive |
|---|---|---|---|---|---|---|
| I–V, I_sw, stand-alone, no ion | ADR, 250 mK–3.2 K (Slichter Sec. 4) | 315 nm LED, fibre butt-coupled (Slichter Sec. 4, Fig. 3) | Room-temperature bias tee (Slichter Sec. 4). Bias resistor not stated | Total gain 51 dB (Slichter Sec. 4). Filters not stated | Pulse counter or oscilloscope (Slichter Sec. 4) | None |
| I_sw and count rate vs bias, with rf off and on, with an ion absent | ADR, 3.8 K (Slichter Sec. 4, Fig. 6) | Free-space 308 nm LED on the 3 K stage, about 36 mm away; no fibre (Slichter Sec. 4) | Bias tee (Slichter Sec. 4). Bias resistor not stated | Total gain 51 dB (Slichter Sec. 4) | Pulse counter (Slichter Sec. 4) | 46.23 MHz, V_pk 25 V, resonator Q 27 (Slichter Sec. 4, Fig. 6) |
| Trap chip with rf, LED flood, no ion | Variable-temperature cryostat, base 2.6 K; 4.5 K and 6 K data (Hampel, measurements section, Fig. 3) | Cryogenic 395 nm LEDs, flood illumination (Hampel, measurements section) | Low-noise voltage source, 10 kΩ series resistor, bias tee (Hampel, measurements section) | Amplified, low-pass and notch filtered; gain not stated (Hampel, measurements section) | Oscilloscope or counter (Hampel, measurements section) | 68–72 MHz, step-up 20, up to 54 V peak (Hampel, measurements section, Fig. 3, abstract) |
| Count rate and dark counts with a trapped ion | About 3.5 K closed-cycle cryostat (Todaro, main text p. 2, Supp. §I.2) | 313 nm free-space beams in the trap plane at 45° (Todaro, main text p. 2, Fig. 1(b)) | AWG pulse, attenuated, into bias-tee DC port, ramped over 11 µs (Todaro, Supp. §I.2, Fig. S2). Resistor per the repo note only [verify] | 46 dB, 1 MHz–1 GHz; 7th-order Bessel notch at the rf; 25 MHz Gaussian low-pass (Todaro, Supp. §I.2, Fig. S2) | Schmitt-trigger comparator, ARTIQ timestamps at 1 ns (Todaro, main text after Fig. 2) | 8.8 V peak at 67.03 MHz (Todaro, main text p. 2) |
| SDE calibration | Stand-alone at 2.5 K, 68 % and 40 % with and without Al (Hampel, text, no figure) | 395 nm LED fibre, calibrated with a PMT at room temperature (Hampel, text) | Not stated | Not stated | PMT for flux calibration (Hampel, text) | None |
| Efficiency calibration, trap chip | Not stated | Not stated | Not stated | Not stated | Not stated | Not stated |

---

## Open items in this note

- The Todaro bias resistor is 10 kΩ in the repo note and "not stated" in the fetched summary. Check the PDF Supp. §I.2 before relying on it.
- Hampel's amplifier gain, filter corners and counter type are not given in the fetched text. The SPIE companion (`doi 10.1117/12.3014455`) may have them; not opened.
- Slichter's Fig. 6 numbers are as the summary reported them. They should be read off the figure.
