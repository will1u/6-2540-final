> **Claude-authored.** Literature pointers, 2026-11-09. Verify before citing.

# L2: open sources (items I1 to I5)

Status tags used below:
- **OPENED (section/figure)**: the text was fetched and the relevant part read (through a web-fetch tool; for PDFs that were unreadable, the arXiv HTML or ar5iv render was used instead).
- **OPENED (abstract only)**: only the abstract page was read.
- **SEARCH EXCERPT ONLY (could not open)**: seen only in search results.
- **not confirmed**: a detail I could not verify.

Caveat for all numbers: they came through a summarising fetch tool, not by reading the typeset page. Check each quoted number against the PDF before it goes into the report.

---

## I1. "Dietl 2025": FOUND, with a corrected title

**Confirmed citation.** M. Dietl, M. Valentini, F. Anmasser, A. Zesar, S. Auchter, M. van Mourik, T. Monz, R. Blatt, C. Rössler, P. Schindler, "Test and characterization of multilayer ion traps on fused silica", arXiv:2505.21284 (submitted 27 May 2025; v2 revised 12 Aug 2025). The arXiv page lists DOI 10.1002/qute.202500412 but does not name the journal; **journal not confirmed**.

**The bib entry is wrong on the title.** `references_design.bib` has "Wafer-level electrical testing of multilayer fused-silica ion traps". The wafer test is one section of the paper, not its title. Do not change the .bib file without a team decision; the correct title is above.

**Opened:** arXiv HTML, https://arxiv.org/html/2505.21284 (OPENED, sections 3, 4.2, 5 and Tables 2 and 3). The HTML is 104,533 characters; the last 4,533 were not read.

Where to read:
- **Section 3, Figure 2a**: each electrode is connected to two bond pads, forming a "loop electrode" that lets the probe test connectivity. This is the two-pad loop structure the report cites.
- **Section 3, Table 2 (Leakage Test DC and RF)**: DC test at 50 V forced; RF test at 300 V forced; pass if the current at the tested electrode does not exceed 100 nA. The DC test also has a voltage pass window of −100 to 100 mV.
- **Section 3 (yield)**: 29.8 % of traps on the wafer failed the leakage tests. The full test for one trap "consists of 480 steps", taking "roughly 7.8 seconds".
- **Section 3**: the 300 V RF test is "sufficiently low to prevent breakdown events through air between neighboring electrodes". No breakdown or flashover voltage is given.
- **Section 4.2, Figure 4a**: heating-rate frequency scaling at 10 K, power-law exponent α = 2.0(9).
- **Section 4.2, Figure 4b**: stray field over 1.2 mm at 60 µm resolution; changes "in the range of 0.1 V", peak at 200 µm.
- **Section 5 (conclusion)**: about 3 quanta/s at ω = 2π × 1.2 MHz, rising to about 60 quanta/s at 2π × 0.45 MHz.
- **Appendix D, Table 3**: site 10 at 0.42 MHz gives 65.9 (8) quanta/s; site 4 at 1.47 MHz gives 3.7 (3).

Not found in the paper (as far as the read covered):
- a **comb** or meander test structure on the wafer (the meander in Section 4.1, Figure 3a is the temperature sensor);
- a **120-needle probe card** (the claim in `fab/test_plan.md`);
- an insulation resistance in ohms;
- a breakdown or flashover voltage threshold.

Discrepancy to flag: the bond-pad report quotes "540 measurements per chip" from a conference abstract. The paper's Section 3 says **480 steps**. Use the paper's number, or cite the conference abstract separately.

Materials caveat: a search excerpt said the Dietl electrodes are aluminium. That was not confirmed in the text I read. Do not use the paper as a gold-electrode reference until this is checked.

---

## I2. "Suleimen 2026": FOUND (abstract), full text NOT opened

**Confirmed citation.** Y. Suleimen, P. P. An, K. O. Sedykh, A. Podlesnyy, S. Yu. Zarutskiy, S. S. Svyatodukh, A. D. Golikov, M. Makhlouf, I. N. Florya, V. V. Kovalyuk, K. E. Lakhmanskiy, G. N. Goltsman, "Mitigation of rf-induced critical-current shifts in NbN superconducting nanowire single-photon detectors for trapped-ion readout", Phys. Rev. Applied 25, 044091 (2026), DOI 10.1103/771x-57wg, published 30 April 2026. The author list and DOI match `references_design.bib`.

**Opened:** https://journals.aps.org/prapplied/abstract/10.1103/771x-57wg (OPENED, abstract only). The page shows "Access by MIT Libraries", so the full text may be readable through the MIT library. I could not open it.

From the abstract (OPENED): a 300 nm wide NbN nanowire keeps a higher relative critical current at higher rf amplitude than a 100 nm wide device; phase-coherent active rf cancellation recovers 92 % of the unperturbed critical current under a 2π × 25 MHz rf field; the device pairs an optically transparent ITO shield with the NbN wire.

**Width-comparison figure: not read.** The figure of critical current versus rf amplitude for the 100 nm and 300 nm wires was not accessible. Read the Results section and that figure in the full text before the test die relies on it.

Status: **SEARCH EXCERPT ONLY for the body; abstract opened.** Not found: any trap-based demonstration, and whether a trap or a model electrode was used.

---

## I3. Au resistivity and RRR: NOT FOUND for the two film types

No source I opened gives a measured room-temperature resistivity and RRR for either film type. Search excerpts only, with the reasons for the gaps:

| Source | Status | What it gives |
|---|---|---|
| Matula, J. Phys. Chem. Ref. Data 8, 1147 (1979) | not opened; cited from the reference list of the knowledgedoor page | probable origin of the 293 K bulk value below |
| https://www.knowledgedoor.com/2/elements_handbook/gold.html | OPENED | ρ(Au, 293 K) = 2.214 × 10⁻⁸ Ω·m (= 2.21 µΩ·cm); no 4 K value or RRR listed |
| https://hypertextbook.com/facts/2004/JennelleBaptiste.shtml | SEARCH EXCERPT ONLY | 2.44 × 10⁻⁸ Ω·m at about 20 °C (secondary citation, not the CRC table) |
| https://arxiv.org/abs/2409.07971 (Müller, Zühlke, Kempf, "Advanced fabrication process for particle absorbers of highly pure electroplated gold for microcalorimeter applications") | OPENED (abstract only) | free-standing, two stacked electroplated Au layers: RRR "above 40"; film thickness, plating bath and current density not stated |
| https://publiweb.femto-st.fr/... (400 nm sputtered Au, 7 to 300 K) | SEARCH EXCERPT ONLY | deposition angle raises residual resistivity; context only (sputtered, oblique) |
| https://pubs.rsc.org/en/content/articlepdf/2018/ra/c8ra01699b | could not open (HTTP 403) | not read |
| https://ui.adsabs.harvard.edu/abs/2004APS..MARS33011M/abstract (Au films on mica, 4 to 300 K) | could not open (HTTP 405) | not read; the search excerpt says thicknesses are "several" and gives no numbers |
| 2015 companion paper on room-temperature-grown Au on mica (Mayadas–Shatzkes, 8 to 100 nm, 4 K) | SEARCH EXCERPT ONLY | no RRR number in the excerpt |
| arXiv cond-mat/9907210 (thin-film metals, Au) | SEARCH EXCERPT ONLY | RRR about 1.6 for roughly 10 nm films (too thin to transfer) |
| PMC5856833, Fig. 2 (ρ300/ρ10 versus thickness, SiO₂ and sapphire) | SEARCH EXCERPT ONLY | figure exists; values not read |

Notes:
- The only opened RRR number is for free-standing electroplated Au with high-purity plating (> 40). It is not a measurement of 6 µm trap electrodes on SiO₂.
- The "about 10⁴" gold RRR that appeared in my own search query is **not confirmed**. Do not use it.
- The 0.35 µm evaporated and 6 µm electroplated Au films have no opened RRR. The honest route is a witness measurement: room-temperature and 4 K resistance on a witness of each process, on the same wafer. That was not in my remit to decide.

---

## I4. Distance scaling of heating (noise) with ion-surface distance d: FOUND

### (a) Sedlacek et al. 2018
- **Confirmed citation.** J. A. Sedlacek, A. Greene, J. Stuart, R. McConnell, C. D. Bruzewicz, J. M. Sage, J. Chiaverini, "Distance scaling of electric-field noise in a surface-electrode ion trap", Phys. Rev. A 97, 020302(R) (2018), arXiv:1712.00188. **Not Nature Physics**, as the search that I ran for "Nature Physics" showed.
- **Opened:** https://ar5iv.labs.arxiv.org/html/1712.00188 (OPENED, abstract and Sec. I/II; the fetch summary cited Figure 2).
- **Exponent:** "We find a scaling of approximately d⁻⁴ regardless of whether the electrodes are at room temperature or cryogenic temperature". Main text: β = 3.9(2) at room temperature and β = 4.0(2) at cryogenic temperature.
- **Distance range:** five zones at 83, 64, 49, 38 and 29 µm.
- **Temperatures:** 295 K and 5 K.
- **Figure:** Figure 2 (heating rate versus ion-electrode distance at both temperatures; single-ion axial mode at 850 kHz).

### (b) An et al. 2019 (arXiv:1906.06489)
- **Confirmed citation.** Da An, Clemens Matthiesen, Erik Urban, Hartmut Häffner, "Distance scaling and polarization of electric-field noise in a surface ion trap", Phys. Rev. A 100, 063405 (2019). The arXiv number is confirmed on the arXiv page.
- **Opened:** https://arxiv.org/abs/1906.06489 (OPENED, abstract only).
- **Exponent:** "We find the noise distance dependence to scale as d⁻²·⁶ in our trap."
- **Distance range:** 50 to 300 µm. **Temperature:** not stated in the abstract. **Figure:** not identified; full text not read.
- Note: this measures **electric-field noise**, not heating rate directly.

### (c) Brownnutt et al. 2015 review
- **Confirmed citation.** M. Brownnutt, M. Kumph, P. Rabl, R. Blatt, "Ion-trap measurements of electric-field noise near surfaces", Rev. Mod. Phys. 87, 1419 (2015), DOI 10.1103/RevModPhys.87.1419, arXiv:1409.6572.
- **Opened:** the arXiv HTML, https://arxiv.org/html/1409.6572, Section 3.2 "Distance scaling" (OPENED, via a summarising fetch of the rendered text; the section numbers and figure numbers should be checked on the typeset PDF). The journal abstract page is paywalled.
- **Exponents quoted in Section 3.2:**
  - Turchette et al. 2000, Fig. 5: two ring traps at 125 and 280 µm; β = 3.8(6) assuming α = 0 (β ≈ 5 if α = 1.5).
  - Deslauriers et al. 2006, Fig. 7: needle trap, 38 to 216 µm, room temperature (one point near 150 K); β = 3.5(1).
  - Deslauriers et al. 2004, Fig. 6: compiled traps over 80 to 600 µm, with a 1/d⁴ patch-potential line plotted for comparison.
  - Fig. 8: room-temperature compiled data with shaded d⁻⁴ and dotted d⁻² envelopes. The authors state the full set cannot support a general d⁻⁴ law.
  - Fig. 12: cryogenic traps (about 6 K), 30 to 230 µm. Median noise 40 × 10⁻¹² V²/(m²·Hz) at room temperature and 0.2 × 10⁻¹² V²/(m²·Hz) at cryogenic temperature over the same range. These are **noise spectral densities, not exponents**.
- The review's general range: distance enters as d^(−β), and a single mechanism can scale between d⁰ and d⁻⁶ depending on length scale (Section 1).

### Summary of exponents (heating or noise, surface or planar traps)
- 2.6 (An 2019, noise, 50 to 300 µm)
- 3.5 (Deslauriers 2006, room temperature, 38 to 216 µm; quoted in Brownnutt 2015)
- 3.8 (Turchette 2000, two rings, assumes α = 0; quoted in Brownnutt 2015)
- 3.9 and 4.0 (Sedlacek 2018, 295 K and 5 K, 29 to 83 µm)

---

## I5. Electrode thickness and exposed dielectric: FOUND, but no quantitative stray-field number

### Todaro et al. 2021 (arXiv:2008.00065)
- **Confirmed citation.** S. L. Todaro, V. B. Verma, K. C. McCormick, D. T. C. Allcock, R. P. Mirin, D. J. Wineland, S. W. Nam, A. C. Wilson, D. Leibfried, D. H. Slichter, "State readout of a trapped ion qubit using a trap-integrated superconducting photon detector", Phys. Rev. Lett. 126, 010501 (2021).
- **Opened:** https://arxiv.org/html/2008.00065v1 (OPENED, Sec. I.1 and the main text; supplement is included in the same document).
- **Electrode thickness:** "6 μm-thick Au trap electrodes are deposited by electroplating" with a 10 μm photoresist mask (Sec. I.1). **No rationale for the thickness is given.**
- **Dielectric:** the only passage on exposed dielectric concerns the SNSPD coating, not the gaps: "such a large area of exposed dielectric is often undesirable due to its tendency to accumulate stray charge" (Sec. I.1). It notes a transparent shielding electrode "would need to be fabricated on top of the dielectric".
- Gaps: the Ti/Au seed layer in the gaps is removed by Ar ion milling (Sec. I.1). **Gap width not given.**
- Dielectric under the electrodes: 134 nm SiO₂ by PECVD on intrinsic Si (Sec. I.1).
- Electric-field noise over the SNSPD is "roughly 6 times higher than that over the gold electrodes" (main text, a noise comparison, not a thickness dependence).
- **Not found:** any stray-field number versus electrode thickness or gap aspect ratio.

### Hampel et al. 2023 (arXiv:2302.01462)
- **Confirmed citation.** B. Hampel, D. H. Slichter, D. Leibfried, R. P. Mirin, S. W. Nam, V. B. Verma, "Trap-integrated superconducting nanowire single-photon detectors with improved RF tolerance for trapped-ion qubit state readout", Appl. Phys. Lett. 122, 174001 (2023), DOI 10.1063/5.0145077.
- **Opened:** https://arxiv.org/html/2302.01462v1 (OPENED, main text and Fig. 2).
- **Au film:** "a 350 nm evaporated gold layer" in a lift-off process. The text says these are "350 nm thick, as opposed to the ∼6 µm thickness in devices that would be used for ion trapping", and it speculates the thin traces may raise resistance and local heating. No thickness rationale beyond this.
- **Dielectric and charging:** no discussion of charging of exposed dielectric in gaps.
- **Fig. 2:** simulated rf field at 100 V, 70 MHz, with no shield and with a grounded aluminium mirror. Text: the rf field around the nanowire cross-sections "is reduced by roughly an order of magnitude".
- **Material note:** the detector is **NbTiN**, not NbN. Our design is NbN.
- Abstract (from the fetch): shielded devices operated to 54 V_peak at 70 MHz and up to 6 K.

### Bautista-Salvador et al. 2019 (arXiv:1812.01829)
- **Opened:** the arXiv PDF (OPENED, Sec. 1, Sec. 2.1, Sec. 2.2, Figs. 1 and 2 captions).
- **Journal:** New J. Phys. (2019), DOI 10.1088/1367-2630/ab0e46 (from a core.ac.uk excerpt; the journal page was not opened). **Author list and volume not confirmed**, so no BibTeX entry is proposed below.
- **Aspect-ratio recommendation:** Sec. 1: "the electrode interspacings should have at least a width equal to its height", or "electrode gaps of an aspect ratio higher than 1:1".
- **Figure 1(a)** caption: Au structures about 2 µm apart, "with a high aspect ratio of 5:1". **Figure 1(b)** caption: "a gap with an aspect ratio of 14:1".
- **Figure 3(a)** caption: "electrode gaps of about 5 µm" (no aspect ratio for this trap).
- **Dielectric in gaps:** Sec. 1: "Often one is concerned about shielding the ion(s) from patch potentials due to exposed dielectrics". Fig. 2 caption, step (f): exposed dielectric between electrodes is etched down to the Si₃N₄ layer, "to hide possible patch potentials built on the exposed insulator".
- **Not found:** a numerical electrode thickness for the final metal, a trap-level gap aspect ratio for the Fig. 3 device, and any measured or modelled charging or patch-potential magnitude.

### Quantitative stray field from charged dielectric versus metal thickness: NOT FOUND
Searched for, not found in any opened source. The Todaro, Hampel and Bautista-Salvador passages all state the motivation without a number. The Brownnutt review's patch-potential line (1/d⁴) is the closest quantitative model, but it is a distance scaling, not a thickness scaling.

---

## Numbers for the design

**Au resistivity and RRR (defend only these):**
- Bulk Au at 293 K: 2.21 µΩ·cm (2.214 × 10⁻⁸ Ω·m, knowledgedoor, citing Matula 1979). Matula not opened; open it before quoting. The 2.44 µΩ·cm value in other textbooks is a 20 °C value and disagrees by about 10 %.
- 0.35 µm evaporated Au: no opened measured resistivity or RRR. **Do not defend a number.** Measure a witness.
- 6 µm electroplated Au: no opened RRR for this geometry. The only opened RRR is > 40 for free-standing, high-purity electroplated Au (Müller et al., abstract). **Use it only as a purity target, not a value for the trap.**

**Heating-rate and noise distance exponents (defend with these sources):**
- β ≈ 4.0 (3.9(2) room temperature, 4.0(2) at 5 K; 29 to 83 µm; Sedlacek 2018, Fig. 2).
- 3.5(1) room temperature, 38 to 216 µm (Deslauriers 2006 via Brownnutt 2015, Fig. 7).
- 3.8(6) (Turchette 2000 via Brownnutt 2015, Fig. 5; assumes α = 0).
- 2.6 (noise, not heating rate; 50 to 300 µm; An 2019, abstract).
- Range to quote: **about 2.6 to 4.0**, with the note that the 2.6 value is a noise exponent and the others are heating-rate exponents, and that Brownnutt 2015 states a single d⁻⁴ law is not supported by the full dataset.

---

## Proposed BibTeX (OPENED sources only; do not paste into the .bib without the team's OK)

```bibtex
% Corrected title for Dietl2025 (replaces the title in references_design.bib). Journal not confirmed.
@misc{Dietl2025,
  author  = {Dietl, M. and Valentini, M. and Anmasser, F. and Zesar, A. and Auchter, S. and van Mourik, M. and Monz, T. and Blatt, R. and R{\"o}ssler, C. and Schindler, P.},
  title   = {Test and characterization of multilayer ion traps on fused silica},
  year    = {2025},
  eprint  = {2505.21284}, archivePrefix = {arXiv},
  doi     = {10.1002/qute.202500412},
  note    = {arXiv v2 (Aug 2025); DOI from the arXiv page, journal not confirmed}}

@article{Sedlacek2018,
  author  = {Sedlacek, J. A. and Greene, A. and Stuart, J. and McConnell, R. and Bruzewicz, C. D. and Sage, J. M. and Chiaverini, J.},
  title   = {Distance scaling of electric-field noise in a surface-electrode ion trap},
  journal = {Phys. Rev. A}, volume = {97}, pages = {020302(R)}, year = {2018},
  eprint  = {1712.00188}, archivePrefix = {arXiv}}

@article{An2019,
  author  = {An, D. and Matthiesen, C. and Urban, E. and H{\"a}ffner, H.},
  title   = {Distance scaling and polarization of electric-field noise in a surface ion trap},
  journal = {Phys. Rev. A}, volume = {100}, pages = {063405}, year = {2019},
  eprint  = {1906.06489}, archivePrefix = {arXiv}}

@article{Brownnutt2015,
  author  = {Brownnutt, M. and Kumph, M. and Rabl, P. and Blatt, R.},
  title   = {Ion-trap measurements of electric-field noise near surfaces},
  journal = {Rev. Mod. Phys.}, volume = {87}, pages = {1419}, year = {2015},
  doi     = {10.1103/RevModPhys.87.1419}, eprint = {1409.6572}, archivePrefix = {arXiv}}

@article{Todaro2021,
  author  = {Todaro, S. L. and Verma, V. B. and McCormick, K. C. and Allcock, D. T. C. and Mirin, R. P. and Wineland, D. J. and Nam, S. W. and Wilson, A. C. and Leibfried, D. and Slichter, D. H.},
  title   = {State readout of a trapped ion qubit using a trap-integrated superconducting photon detector},
  journal = {Phys. Rev. Lett.}, volume = {126}, pages = {010501}, year = {2021},
  doi     = {10.1103/PhysRevLett.126.010501}, eprint = {2008.00065}, archivePrefix = {arXiv}}

@article{Hampel2023,
  author  = {Hampel, B. and Slichter, D. H. and Leibfried, D. and Mirin, R. P. and Nam, S. W. and Verma, V. B.},
  title   = {Trap-integrated superconducting nanowire single-photon detectors with improved RF tolerance for trapped-ion qubit state readout},
  journal = {Appl. Phys. Lett.}, volume = {122}, pages = {174001}, year = {2023},
  doi     = {10.1063/5.0145077}, eprint = {2302.01462}, archivePrefix = {arXiv}}
```

Not proposed, for the reasons in the text: **Suleimen2026** (the existing bib entry already matches the abstract page; the full text is unread); **Bautista-Salvador 2019** (author list not confirmed); **Müller et al.** (abstract only, not cited in the design).

---

## Could not find or could not open (for the team's list)
- Full text of Suleimen 2026 (paywalled; try the MIT library).
- Full text of An 2019 (abstract only; the temperature and figure for d⁻²·⁶ are unread).
- Full text of Matula 1979 (bulk Au resistivity reference).
- RSC 2018 thin-Au paper (HTTP 403); 2004 APS Au-on-mica abstract (HTTP 405); Mayadas–Shatzkes mica papers (search excerpt only).
- Thickness and gap width in the Todaro and Hampel devices.
- Any measured charging-versus-thickness number for dielectric in trench gaps.
