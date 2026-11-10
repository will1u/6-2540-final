> **Claude-authored.** Reading pointers for electrical checks on single-layer traps and for screening SNSPDs before cooldown, 2026-11-10.

# T3: electrical checks on traps and screening SNSPDs before cooldown

**What was opened.** Stick 2010 and Sterling 2013 were read through a summarising tool (WebFetch on the arXiv HTML at ar5iv, and on the arXiv and AIP pages). None of the text was read directly, so every number from these fetches is tagged `[verify]`. The Kerman 2007 text was read the same way (ar5iv). The rest is listed under "Not opened". Identifiers below were checked on the arXiv or publisher page shown.

**Repo notes used as a starting point (not checked against the source here):** [`nbn_process.md`](../Trap%20integrated%20SNSPD%20design/nbn_process.md), [`rf_tolerance.md`](../SNSPD%20geometry%20audit/rf_tolerance.md).

**Identifiers checked in this session:**

| Key | Identifier checked | Where checked |
|---|---|---|
| `Stick2010` | arXiv:1008.0990 (v2, revised 16 Nov 2010); "Demonstration of a microfabricated surface electrode ion trap"; D. Stick, K. M. Fortier, R. Haltli, C. Highstrete, D. L. Moehring, C. Tigges, M. G. Blain. Journal not shown on the page. The bib entry's author list ("Stick, D. and others") and "journal venue unverified" note stand. | arXiv abstract page |
| `Sterling2013` | APL 103, 143504 (2013), issue 14; DOI 10.1063/1.4824012; authors R. C. Sterling, M. D. Hughes, C. J. Mellor, W. K. Hensinger. Preprint arXiv:1208.5672 (v3, 25 Apr 2014), **arXiv id not in the bib**. | AIP article page (pubs.aip.org, via the DOI redirect) and arXiv listing from search |
| `Kerman2007` | arXiv:physics/0611260 (v2, 22 Jan 2007); "Constriction-limited detection efficiency of superconducting nanowire single-photon detectors"; A. J. Kerman, E. A. Dauler, J. K. W. Yang, K. M. Rosfjord, V. Anant, K. K. Berggren, G. Gol'tsman, B. Voronov. Journal ref not shown on the arXiv page. The bib (APL 90, 101110, 2007) is **not confirmed here**. The arXiv page also lists a related DOI 10.1063/1.2696926, which is **not in the bib**. | arXiv abstract page; the same DOI appears in the link annotations of `https://qnn-rle.mit.edu/documents/kerman-2007.pdf` (binary, not readable) |
| `Kerman2009` | arXiv:0812.0290; PRB 79, 100509 (2009); DOI 10.1103/PhysRevB.79.100509; Kerman, Yang, Molnar, Dauler, Berggren | arXiv abstract page (metadata only; text not read) |
| `Medeiros2019` (bib key; arXiv listed as 2018) | arXiv:1812.05559 (v3, 23 Apr 2019); "Measuring thickness in thin NbN films for superconducting devices"; O. Medeiros, M. Colangelo, I. Charaev, K. K. Berggren. Journal not shown. | arXiv abstract page (abstract only) |
| `Dane2017` | APL 111, 122601 (2017); DOI 10.1063/1.4990066; "Bias sputtered NbN and superconducting nanowire devices"; A. E. Dane, A. N. McCaughan, D. Zhu, Q. Zhao, C.-S. Kim, N. Calandri, A. Agarwal, F. Bellei, K. K. Berggren | AIP article page (full text reported on the page; a sign-in prompt appears) |
| Not in bib | arXiv:2501.07780 (v3); J. Vac. Sci. Technol. A 43, 042701 (2025); DOI 10.1116/6.0004539 (related); S. Margiotta et al. Title: "Thermal Annealing and Radiation Effects on Structural and Electrical Properties of NbN/GaN Superconductor/Semiconductor Junction." Not an SNSPD film. | arXiv abstract page |
| Not in bib | arXiv:1910.07010 (v2, 26 Nov 2019); journal ref not shown; related DOI 10.1063/1.5131664 (listed); R. Cheng, S. Wang, H. X. Tang. "Superconducting nanowire single-photon detectors fabricated from atomic-layer-deposited NbN." | arXiv abstract page (abstract only) |
| Not in bib | arXiv:1511.07081 (submitted 22 Nov 2015); C. Schuck, X. Guo, L. Fan, X.-S. Ma, M. Poot, H. X. Tang. "Quantum interference in heterogeneous superconducting-photonic circuits on a silicon chip." | arXiv abstract page (abstract only; PDF text not readable) |
| Not in bib | arXiv:1906.09969 (21 Jun 2019); R. Gourgues et al. "High performance superconducting nanowire single photon detectors operating at temperature from 4 to 7 K"; related DOI 10.1364/OE.27.024601 (listed) | arXiv abstract page (abstract only; PDF text not readable) |

---

## 1. Electrical checks on trap chips (`Stick2010`, `Sterling2013`)

### Stick 2010 (`Stick2010`)

**Opened:** arXiv HTML at `https://ar5iv.arxiv.org/html/1008.0990` through a summarising tool, and the PDF `https://arxiv.org/pdf/1008.0990` (returned as binary, so the ar5iv copy was used). Section and figure labels as the summary gave them. **Readable: text and figure labels, no page numbers.**

| Question | Where in the source | What is there |
|---|---|---|
| Continuity, leakage or shorts on trap chips | Sec. II, "Fabrication" | Each trap was "electrically tested for shorts between any trap electrodes (DC, RF, and grounds, including the ground plane)" [verify]. For the two traps reported, no shorts below 100 MΩ were observed [verify]. Reported as a resistance threshold, not as a leakage current. |
| Breakdown or flashover voltage | Sec. II; no separate section found | None reported in the fetched text [verify]. |
| In air or in vacuum | Not stated in the fetched text | Not found [verify]. |
| Test structure | Sec. II; Figs. 2–3 | No separate test structure. Tests were on the trap electrodes themselves. Fig. 2 is a cross-section and overhead schematic; Fig. 3 is the electrode layout. Neither is a test structure [verify]. |
| Other electrical measurement | Sec. II, "Fabrication" | RF capacitance from the RF electrodes to ground (trap plus package) measured as 7 pF, with a 30 MHz, 2 W drive through a resonator with Q = 150 [verify]. |

The abstract describes a silicon substrate, SiO₂ and Al electrodes (arXiv abstract) [verify].
### Sterling 2013 (`Sterling2013`)

**Opened:** the full text on `https://pubs.aip.org/apl/article/103/14/143504/936631/Increased-surface-flashover-voltage-in` (summary said the page holds full text, with a subscriber prompt); the arXiv HTML at `https://ar5iv.arxiv.org/html/1208.5672` (the PDF was binary). Figure labels as the summary gave them. **Readable: text and figure labels, through a summarising tool.** Paragraph names below are the summary's.

| Question | Where in the source | What is there |
|---|---|---|
| Flashover data vs gap (the main data) | Fig. 2(a) (rf) and Fig. 2(b) (static); the caption of Fig. 2 | Fig. 2(a): mean rf flashover voltage vs gap, with standard-deviation bars, and a fit of Eq. 1 with φ_rf = 4.6 × 10¹⁸ eV m⁻² [verify]. Fig. 2(b): static flashover, fit φ_dc = 4.9 × 10¹⁸ eV m⁻² [verify]. Lift-off-electrode data are shown in Fig. 2(a) as open triangles [verify]. |
| Test structure | Paragraph "In order to set a base line", after Eq. 1 and before Fig. 1 | Gold electrodes on quartz, with gaps from 3 to 15 µm in 2 µm steps [verify]. |
| Air or vacuum | Same paragraph | Vacuum, about 5 × 10⁻⁴ Pa [verify]. |
| Process change that raised flashover | Fig. 3(b); paragraph "In order to increase the voltage", and paragraph "In multilayer fabrication processes" | Surface layer of aSiN (80 nm) on a layered dielectric over Si, in place of aSiO, gave about a 3.6-fold improvement (φ = 18.1 × 10¹⁸ eV m⁻²) [verify]. The abstract says "more than double" [verify]. |
| Continuity or leakage | None | No continuity or leakage test found [verify]. Voltage calibration is given as ±10 mV monitor error, and Fig. 1 shows visual damage inspection [verify]. |

Note: the abstract's "more than double" and the body's 3.6-fold figure refer to different comparisons. Check the PDF Fig. 3(b) before quoting either.

---

## 2. Screening SNSPDs before cooldown with room-temperature resistance

**Result of the search:** no source was opened in this session that reports screening of NbN nanowire meanders by room-temperature resistance before cooldown. Candidates and what each one showed:

| Candidate | Opened? | What the source shows | Qualifies? |
|---|---|---|---|
| `https://arxiv.org/abs/1511.07081` (Schuck et al.) | Abstract only. The PDF text is binary and was not readable. | Abstract: an on-chip photon-pair interference experiment with two integrated detectors, "97% interference visibility". The abstract does not mention room-temperature resistance or screening [verify]. | **No.** The abstract does not show the claim. A search excerpt says the paper measures room-temperature resistance of every wire on a chip, but that text was not read and is not used here. |
| `Kerman2007` (`physics/0611260`) | Yes, through ar5iv (summary) | Room-temperature resistance enters the normalisation of constriction efficiency: the product I_C^obs · R_n is used, with the figure "Figure 2b–c" [verify]. A kinetic-inductance measurement at low temperature gives the absolute constriction factor C (paragraph on kinetic inductance, "Figure 3a") [verify]. | **Partly.** It uses R_n as an input to the constriction model. It does not describe a pre-cooldown screen. |
| `Cheng2019` (`arXiv:1910.07010`) | Abstract only | The abstract attributes "near-unity throughput yield" to film homogeneity, citing "Statistical analyses on hundreds of fabricated devices" [verify]. No room-temperature resistance measurement in the abstract. | No (abstract only). |
| `Medeiros2019` (`arXiv:1812.05559`) | Abstract only | Ellipsometer used for "quickly measuring the thickness of NbN thin films" [verify]. Not a device screen. | No. |
| `Gourgues2019` (`arXiv:1906.09969`) | Abstract only | The abstract covers detectors at 4–7 K; it does not describe room-temperature resistance screening [verify]. | No (abstract only). |

What the sources say about the limit of the method (from `Kerman2007`, the only opened source with a room-temperature resistance term):

| Question | Where | What is there |
|---|---|---|
| What is measured | Paragraph on normalisation, Fig. 2(b–c) | R_n at room temperature, combined with I_C^obs, to normalise the constriction effect [verify]. |
| What it can predict | Paragraph before Fig. 3(b–d) | "Electrical C values can be used to predict detection efficiency", suggested as a screen [verify]. The C values in that paragraph come from the low-temperature kinetic inductance measurement, not from a room-temperature reading [verify]. |
| What it cannot predict | Final paragraph before the Conclusion | The cause of the constrictions is not identified; SEM found no lithographic error; "Further work is ongoing" [verify]. |

**Status of (a):** no readable source shows a room-temperature resistance screen of NbN meanders before cooldown. Two more candidate papers would be needed. This is an open gap, not a finding.

---

## 3. Constrictions that limit the switching current (start: `Kerman2006`, `Kerman2009`, `Kerman2007`)

| Source | Opened? | Where | What is there |
|---|---|---|---|
| `Kerman2007` (`physics/0611260`) | Yes (ar5iv summary) | Introduction (paragraph after the array-application paragraph); Fig. 1 caption and paragraph after Fig. 1; Fig. 2 caption and text after it; Fig. 3(a)–(d) | Constrictions are defined in the paragraph after Fig. 1. They reduce the observed critical current by a factor C [verify]. The wire width comparison (54 nm and 90 nm wires, a 54 nm constriction in a 90 nm wire) is in the Fig. 2 caption [verify]. The SEM found no lithographic error in the constriction region (Fig. 2a discussion) [verify]. The absolute C is set by the kinetic inductance L_k(I_bias), measured with a network analyser (paragraph on kinetic inductance and Fig. 3a) [verify]. |
| `Kerman2009` (`0812.0290`) | Metadata only | Abstract page | Not read as text. Electrothermal feedback, PRB 79, 100509 (2009). **Do not use for the constriction question without reading the text.** |
| `Kerman2006` (DOI 10.1063/1.2183810) | No | Repo bib entry links `https://qnn-rle.mit.edu/documents/kerman-published-version-2006.pdf` | Not attempted in this session. |

---

## 4. How the film is checked cold, with little equipment (NbN sheet resistance, Tc, RRR)

| Quantity | Source (opened) | Where | What is there |
|---|---|---|---|
| Tc of unpatterned NbN film, bias-sputtered at room temperature | `Dane2017` | Abstract; Fig. 2 (bottom) | Abstract: Tc of 7.8 K for the optimised 5 nm film [verify]. Fig. 2 (bottom) shows Tc for the 5 nm films under different deposition conditions [verify]. The text says bias raised Tc by 25 % to 73 % [verify]. |
| Resistivity (and sheet resistance) | `Dane2017` | Abstract; Fig. 2 (top); four-point probe method in the text | Abstract: resistivity 253 µΩ·cm for the same film [verify]. Fig. 2 (top) shows room-temperature resistivity [verify]. The text says sheet resistance was measured by four-point probe and multiplied by the film thickness [verify]. **No sheet resistance value is reported.** |
| RRR | `Dane2017` | Not reported on the page | **Not found.** |
| Tc, RRR, and their change with heat (NbN on GaN, not an SNSPD film) | `arXiv:2501.07780` (not in bib) | Abstract | As-deposited Tc 12.82 K [verify]. Tc stable after a 500 °C anneal; at 950 °C, Tc about 8 K and the "residual resistivity ratio" falls from 0.85 to 0.29 after 30 min [verify]. The abstract uses the term "residual resistivity ratio". This is a GaN junction study, so the values do not transfer directly. |

The repo note `nbn_process.md` lists further values from `Toomey2018` (sheet resistance 90 Ω/sq at about 20 nm; 600 Ω/sq at 5 nm; Tc change with TMAH time) and from `Najafi2015` (515 Ω/sq, Tc 10.9 K). **These were not opened in this session.** They are listed under "Not opened" and are not used here.

---

## Not opened

| Source | What was tried |
|---|---|
| Toomey et al. 2018 (`Toomey2018`, DOI 10.1116/1.5047427) | Not attempted in this session. Repo note `nbn_process.md` cites it. |
| Najafi et al. 2015 (`Najafi2015`, DOI 10.1038/ncomms6873) | Not attempted in this session. Repo note `nbn_process.md` cites it. |
| Kerman et al. 2006 (`Kerman2006`, DOI 10.1063/1.2183810) | Not attempted in this session. The repo URL `https://qnn-rle.mit.edu/documents/kerman-published-version-2006.pdf` was not fetched. |
| Kerman et al. 2009 (`Kerman2009`) | Abstract metadata only. Text not read. |
| Kerman 2007 published version (APL 90, 101110) | The arXiv version was read; the published journal page was not opened. The bib journal entry is unconfirmed. The qnn PDF (`https://qnn-rle.mit.edu/documents/kerman-2007.pdf`) returned binary, not text. |
| Stick 2010 PDF | Returned binary. Read through ar5iv only. |
| Sterling 2013 PDF | Returned binary. Read through the AIP page and ar5iv only. |
| Medeiros 2019 full text | Abstract only. The repo note's statement that resistance is unreliable for thickness is not checked here. |
| Cheng 2019 (`arXiv:1910.07010`), Gourgues 2019 (`arXiv:1906.09969`), Schuck 2015 (`arXiv:1511.07081`) | Abstracts only. PDFs binary or not read. |
| Search excerpts for NbTiN room-temperature screening and for a 300 mm TaN wafer study | Not opened. Not used. |
| Todaro thesis (`TodaroThesis2020`) | Not opened in this session (not needed for T3). |

---

## Open questions these sources do not answer

- No readable source here reports a room-temperature resistance screen of NbN meanders, its yield, or how well it predicts the switching current at 4–5 K.
- Stick 2010 does not state whether its shorts test was in air or vacuum, or what voltage it used. Sterling 2013 gives flashover data but not for the electrode geometry of the team's stack.
- Dane 2017 gives Tc and resistivity but not sheet resistance or RRR for a 5 nm film [verify with the PDF].
- The Kerman 2007 journal and DOI are unconfirmed on the arXiv page (the bib gives APL 90, 101110; the arXiv link annotation gives DOI 10.1063/1.2696926).
- Whether the room-temperature resistance of a patterned meander follows the unpatterned film values in `Dane2017` (Fig. 2) is not shown by any source opened here.
