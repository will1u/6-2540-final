> **Claude-authored.** Literature pointers, 2026-11-09. Verify before citing.

# L1: 493 nm emission from Ba⁺ and detection performance (literature pointers)

Scope: Q1 to Q5 from the L1 brief. Pointers only. Each source is marked:
- **OPENED (read the relevant part)**: the page was fetched and the stated part was read;
- **SEARCH EXCERPT ONLY (could not open)**: seen only in a search snippet.

**Read this first.** Every number and quote below came through a fetch tool that summarises the page. The quoted sentences are as the fetch returned them. Check each one against the arXiv HTML or the PDF before it goes into a report. Where a PDF could not be read as text, that is said below.

Items marked **[team calc]** are arithmetic on the numbers in the sources. Items marked **[inference]** are reasoning, not a reported result.

---

## Q1. Angular distribution of 493 nm emission from J = 1/2

**Answer in brief.** No textbook passage was opened. The closest opened source is Auzinsh, Budker and Rochester (arXiv:0908.2666). It says that a J_e = 1/2 upper level can carry only orientation (rank κ = 1), not alignment, so no alignment-dependent effect can show up in fluorescence. That supports "no alignment". It does not state that the intensity is isotropic.

1. **Auzinsh, Budker, Rochester, "Light-induced polarization effects in atoms with partially resolved hyperfine structure and applications to absorption, fluorescence, and nonlinear magneto-optical rotation," arXiv:0908.2666.** Journal and year: not confirmed. Authors as read: M. Auzinsh, D. Budker, S. M. Rochester.
   Link: https://ar5iv.arxiv.org/html/0908.2666 (abstract page: https://arxiv.org/abs/0908.2666)
   **OPENED (read the relevant part; first 100000 of 189298 characters).**
   - Sec. I: for J_g = 1/2 with unresolved hyperfine structure, "the highest rank multipole moment that can be supported by the ground state is orientation (κ = 2J = 1)", and "effects depending on atomic ground-state alignment will not be apparent".
   - Sec. II.4 (Fluorescence): "only the electronic excited-state polarization of rank κ ≤ 2J_e can be observed". For J_e = 1/2 this gives κ ≤ 1.
   - Table 1, fluorescence row: κ ≤ 2J_e.
   - **Caveat.** This is a rank argument about which moments can be observed. It does not say that the emitted intensity is isotropic for every m_J population. The rank-1 (orientation) term can still give a polarisation effect (see caveat below).

2. **Auzinsh, Budker, Rochester, *Optically Polarized Atoms: Understanding Light-Atom Interactions*, Oxford University Press, 2010.** Not opened. The title and publisher come from a search listing and a PDF mirror. The ISBN in that listing is 0199565120. Not confirmed against the publisher. Section on fluorescence angular distributions: not found.
   **SEARCH EXCERPT ONLY (could not open).**

3. **Budker, Kimball, DeMille, *Atomic Physics*** (2nd ed.) and **Foot, *Atomic Physics*.** Not opened. No section was located. **Not checked.** Suggested place to look: the chapter on fluorescence polarisation and angular momentum of the excited state. Confirm the section by reading the book.

**Clebsch check, for the team to verify [team calc].** For a single m_J = +1/2 sublevel of a J = 1/2 upper level decaying to a J = 1/2 lower level, the branching weights are 1/3 for π (q = 0, pattern (3/8π) sin²θ) and 2/3 for σ (q = ±1, pattern (3/16π)(1 + cos²θ)). Summing the two gives (1/8π)(sin²θ + 1 + cos²θ) = 1/(4π). The total emission from one m_J sublevel is therefore isotropic, which agrees with the design's claim. The same weights are the 1/3 and 2/3 used in the design. This is an algebra check, not a source.

**Caveat on polarisation [inference].** Isotropic intensity does not mean isotropic polarisation. An orientation (rank-1) population can give partially polarised light whose degree depends on direction. Todaro et al. (Q5 below) report that the SNSPD quantum efficiency depends on photon incidence angle and on polarisation. So a polarisation-dependent detector can see an angular effect even when the total intensity is isotropic.

---

## Q2. Ba⁺ 6P₁/₂ numbers

1. **Arnold, Chanu, Kaewuam, Tan, Yeo, Zhang, Safronova, Barrett, "Measurements of the branching ratios for 6P₁/₂ decays in ¹³⁸Ba⁺," Phys. Rev. A 100, 032503 (2019), arXiv:1905.06523.**
   Link: https://arxiv.org/abs/1905.06523 and https://arxiv.org/html/1905.06523v3
   **OPENED (read the relevant part; abstract, Sec. II, Sec. III, Sec. V, Table 2).**
   - Branching ratio to 5D₃/₂: "p = 0.268177 ± (37)_stat − (20)_sys" (abstract; repeated in Sec. II and Sec. V).
   - Table 2, "Recommended" column: p(theory) = 0.268177(57).
   - Lifetime: "τ = 7.855(10) ns" for the 6P₁/₂ level (abstract). Sec. III: "we obtain an estimate of τ = 7.855(10) ns for the P₁/₂ lifetime". The paper obtains this by combining p with earlier experimental data.
   - **6P₁/₂ → 6S₁/₂ branch:** not given as a separate number in the paper.
     **[inference]** The 6P₁/₂ decays go only to 6S₁/₂ and 5D₃/₂ (the 5D₅/₂ channel is forbidden from J = 1/2). So the 6S₁/₂ branch is 1 − p = 0.731823. Not a reported value.
   - Natural linewidth: **[team calc]** Γ = 1/τ = 1/(7.855 ns) = 1.2730 × 10⁸ s⁻¹; Γ/2π = 20.26 MHz.

2. **De Munshi, Dutta, Rebhi, Mukherjee, "Precision measurement of branching fractions of ¹³⁸Ba⁺: Testing many body theories below one percent level," Phys. Rev. A 91, 040501(R) (2015), arXiv:1411.5041.**
   Link: https://arxiv.org/abs/1411.5041
   **OPENED (abstract only).** The abstract claims a precision of 0.05 % on the branching fractions. It gives no branching values in the abstract. It gives the dipole matrix elements 3.306 ± 0.014 (S–P) and 3.036 ± 0.016 (P–D), and mentions "the known value of the upper state life-time" without a number. Use this as a second, independent branching measurement. Its branching values were not read.

3. **Lifetime, independent check.** Not found in an opened source beyond Arnold et al. Arnold et al. report that the value combines their p with earlier lifetime data, so it is not a fully independent check.

---

## Q3. Realistic 493 nm photon rate for a single ¹³⁸Ba⁺ ion

1. **Zhukas, Svihra, Nomerotski, Blinov, "High-Fidelity Simultaneous Detection of Trapped Ion Qubit Register," arXiv:2006.12801.** Journal and year not confirmed (arXiv 2006 number). Link: https://ar5iv.labs.arxiv.org/html/2006.12801
   **OPENED (read the relevant part).**
   - "when in the 6S₁/₂ state, the ion scatters ∼10⁷ photons/s" (setup section, four-ion chain and cooling/qubit lasers).
   - "the average time between photons is approximately 0.5 ms for the bright state" (data-analysis section). This implies about 2 kHz detected counts, but the paper does not state that rate directly.
   - **[team calc]** Comparing the two: 2 kHz / 10⁷ s⁻¹ = 2 × 10⁻⁴ overall. The paper's collection is about 1.3 % (point 2 below), so the detector and filter chain in that paper would have to pass roughly 1.5 % of the collected light. The source does not state the detection efficiency applied to the 0.5 ms figure. Check this before using either number alone.

2. **Collection in the same paper.** NA 0.20 objective ("50 mm Nikon lens with numerical aperture 0.20"), collection efficiency "approximately 1.3%" (experimental setup, optical system). Source as above; OPENED.

3. **Scattering limit from the lifetime [team calc].** For a two-level-like system, the maximum excited-state fraction is 1/2 and the maximum decay rate is Γ/2 = 6.37 × 10⁷ s⁻¹. The branch to 6S₁/₂ is 0.7318 (Q2). So the ceiling on 493 nm photons emitted is 0.7318 × 6.37 × 10⁷ = 4.66 × 10⁷ s⁻¹. The 650 nm repumper and the D-state dark-state pumping lower the real excited fraction, so this is a ceiling, not an expected rate.

4. **Lambda-system pumping and dark state.** Search excerpts only (SEARCH EXCERPT ONLY): 493 nm drives S₁/₂–P₁/₂, 650 nm drives D₃/₂–P₁/₂; scattering into D₅/₂ gives a dark state lasting about 30 s. Not used for any number here. Source not opened.

5. **Saturation intensity or measured scattering rate versus intensity for Ba⁺ 493 nm.** Not found in any opened source.

---

## Q4. Ba⁺ state-detection performance

1. **Zhukas et al., arXiv:2006.12801** (Q3 above). OPENED.
   - Detector: intensified time-stamping camera (Tpx3Cam, Timepix3 readout).
   - NA 0.20, collection about 1.3 %.
   - Abstract: "average single qubit detection error of 4.2(1.5) ppm and a 4-qubit state detection error of 17(2) ppm".
   - Summary: "a 30 ms detection time" for a single ion.
   - Note: this is a 4-ion register result with a per-ion detection time of 30 ms, not a short-time result.

2. **Duke group, Rev. Sci. Instrum. 95, 033201 (2024), "experimentoverview" PDF (iontrap.duke.edu).** Title and author list not confirmed. Source is a PDF the tool could not read as text.
   **SEARCH EXCERPT ONLY (could not open).** Excerpt: two aspheric lenses with NA 0.8; "Ideally they collect about 40% of the 493 nm photons", "measured net collection was about 36%" in the fibre-coupling setup; "coupling 10(1)% of the 493 nm photons into single-mode fibers". Detection time and fidelity: not in the excerpt.
   Link: https://iontrap.duke.edu/files/2025/03/033201_1_5.0180732.pdf

3. **O'Reilly, Toh, Goetting, Saha, Shalaev, Carter, Risinger, Kalakuntla, Li, Verma, Monroe, "Fast photon-mediated entanglement of continuously-cooled trapped ions for quantum networking," arXiv:2404.16167.** Journal: PRL, with a volume given as both 113 and 133 in the fetched metadata. Not confirmed. Link: https://arxiv.org/abs/2404.16167
   **OPENED (abstract page).** Two barium ion qubits, 0.8 NA in-vacuo objectives, entanglement fidelity lower bound "F > 94%". This is entanglement fidelity, not single-ion state detection, so it is not a detection benchmark. Use only as context for NA 0.8 collection in Ba⁺.

4. **Ba⁺ detection using a PMT** (single-ion fidelity 0.99971(3)), noted in a search excerpt as "133Ba⁺", which is probably a typo. **SEARCH EXCERPT ONLY.** Source not identified.

**Gap.** No opened source gives a Ba⁺ detection time and fidelity with an SNSPD at NA 0.4 or above. The Duke excerpt has NA 0.8 but no detection time in the excerpt.

---

## Q5. Todaro et al. 2021 (⁹Be⁺, trap-integrated SNSPD)

**Todaro, McCormick, Verma, Allcock, Mirin, Wineland, Nam, Wilson, Leibfried, Slichter, "State Readout of a Trapped Ion Qubit Using a Trap-Integrated Superconducting Photon Detector," Phys. Rev. Lett. 126, 010501 (2021), arXiv:2008.00065.**
Link: https://arxiv.org/abs/2008.00065 and https://ar5iv.labs.arxiv.org/html/2008.00065
**OPENED (read the relevant part).** Authors and journal reference confirmed on the abstract page.

- **Readout fidelity and time:** "achieving qubit state readout with fidelity 0.9991(1) in an average of 46 μs using an adaptive Bayesian readout scheme" (Introduction). "The corresponding maximum readout fidelities are 0.9988(1) and 0.9991(1) for the thresholding and Bayesian methods, respectively" (main text, readout-fidelity section).
- **Detection efficiency (SDE):** "Using this technique, we extract an SDE of 48(2) % with the trap rf on and Ib = 4 μA" (main text, SDE calibration paragraph). "this would correspond to a maximum SDE of 65(5) % without rf". "This number is slightly lower than the theoretical design SDE of 72 % based on nanowire geometry."
- **Count rates:** Section I.4 (readout fidelity): "We measure γb = 162.50(3) ms⁻¹, γd = 5.095(5) ms⁻¹, γdp = 0.020(3) ms⁻¹, and γrp = 0.0120(7) ms⁻¹." Here γb and γd are the bright and dark photon count rates. **The units are printed as ms⁻¹. Check whether the source means per ms or per s before using this number.** Dark counts per detection: "remain below 10⁻²" (main text).
- **Numerical aperture:** "When the ion is in zone D, this gives an effective NA of 0.32 for the SNSPD" (main text, trap configuration). Separate refractive objective for the EMCCD and PMT: "NA = 0.38" (Sec. I.2).
- **Detector material:** Mo₀.₇₅Si₀.₂₅ (amorphous), T_c = 5.2 K; from a search excerpt. **SEARCH EXCERPT ONLY.**

---

## Hampel et al. 2023 (for context on SNSPD detection efficiency)

**Hampel, Slichter, Leibfried, Mirin, Nam, Verma, "Trap-Integrated Superconducting Nanowire Single-Photon Detectors with Improved RF Tolerance for Trapped-Ion Qubit State Readout," Appl. Phys. Lett. 122, 174001 (2023), arXiv:2302.01462.** Link: https://arxiv.org/abs/2302.01462
**OPENED (abstract page).** "with a maximum system detection efficiency of 68 %"; shielded SNSPDs operated "at applied rf trapping potentials of up to 54 V_peak at 70 MHz and temperatures of up to 6 K".
Not confirmed from the opened page: the ion species and wavelength. A search excerpt says Ca⁺ at 397 nm. **Not confirmed for Ba⁺ or for this paper's species.** Dark count rates: not on the abstract page. The PDF was not readable.

---

## Numbers for the design

| Quantity | Value | Source |
|---|---|---|
| 6P₁/₂ lifetime τ | 7.855(10) ns | Arnold et al. 2019, abstract and Sec. III (OPENED) |
| 6P₁/₂ natural linewidth Γ/2π | 20.26 MHz | [team calc] from τ above |
| 493 nm branch (6P₁/₂ → 6S₁/₂) | 0.7318 | [inference] 1 − p, with p = 0.268177(37)(20) from Arnold et al. 2019, Table 2 and abstract (OPENED). Cross-check: De Munshi et al. 2015 claim 0.05 % precision (abstract only). |
| 650 nm branch (6P₁/₂ → 5D₃/₂) | 0.268177(37)_stat (20)_sys | Arnold et al. 2019 (OPENED) |
| 493 nm photon rate, measured | about 10⁷ s⁻¹ (bright 6S₁/₂ state, single ion in a chain) | Zhukas et al. (arXiv:2006.12801), OPENED. One source, not a dedicated scattering-rate measurement. |
| 493 nm photon rate, ceiling | 4.66 × 10⁷ s⁻¹ | [team calc]: 0.7318 × Γ/2 with Γ = 1/τ. An upper bound, not a prediction. |
| **Defensible range** | **10⁶ to 10⁷ s⁻¹** | Lower end is a judgment, not a sourced number. Upper end from Zhukas et al. Ceiling is 4.7 × 10⁷ s⁻¹. |

**[team calc] expected detected counts per 100 µs** if 1.47 % of all emitted 493 nm photons are absorbed in the detector:

counts = R × t × η, with t = 100 µs = 1.00 × 10⁻⁴ s and η = 0.0147.

- R = 10⁶ s⁻¹: 10⁶ × 1.00 × 10⁻⁴ × 0.0147 = **1.5 counts**
- R = 10⁷ s⁻¹: 10⁷ × 1.00 × 10⁻⁴ × 0.0147 = **14.7 counts**
- R = 4.66 × 10⁷ s⁻¹ (ceiling): 4.66 × 10⁷ × 1.00 × 10⁻⁴ × 0.0147 = **68.5 counts**

The 1.47 % value is the team's, not from these sources. Note that the Zhukas per-ion detection-time figure (30 ms) and the 2 kHz detected count rate are not on the same footing as this calculation.

---

## Proposed BibTeX (OPENED sources only; not added to `references_design.bib`)

```bibtex
@article{Arnold2019,
  author  = {Arnold, K. J. and Chanu, S. R. and Kaewuam, R. and Tan, T. R. and Yeo, L. and Zhang, Zhiqiang and Safronova, M. S. and Barrett, M. D.},
  title   = {Measurements of the branching ratios for $6P_{1/2}$ decays in $^{138}$Ba$^+$},
  journal = {Phys. Rev. A}, volume = {100}, pages = {032503}, year = {2019},
  eprint  = {1905.06523}, archivePrefix = {arXiv},
  note    = {Journal fields as read from the fetched arXiv page; verify against the DOI record}}

@article{DeMunshi2015,
  author  = {De Munshi, D. and Dutta, T. and Rebhi, R. and Mukherjee, M.},
  title   = {Precision measurement of branching fractions of $^{138}$Ba$^{+}$: Testing many body theories below one percent level},
  journal = {Phys. Rev. A}, volume = {91}, pages = {040501(R)}, year = {2015},
  eprint  = {1411.5041}, archivePrefix = {arXiv},
  note    = {Abstract read only; branching values not read}}

@misc{Zhukas2020,
  author = {Zhukas, L. A. and Svihra, P. and Nomerotski, A. and Blinov, B. B.},
  title  = {High-Fidelity Simultaneous Detection of Trapped Ion Qubit Register},
  year   = {2020}, eprint = {2006.12801}, archivePrefix = {arXiv},
  note   = {Journal not confirmed; year taken from arXiv number}}

@misc{Auzinsh2009,
  author = {Auzinsh, M. and Budker, D. and Rochester, S. M.},
  title  = {Light-induced polarization effects in atoms with partially resolved hyperfine structure and applications to absorption, fluorescence, and nonlinear magneto-optical rotation},
  year   = {2009}, eprint = {0908.2666}, archivePrefix = {arXiv},
  note   = {Journal not confirmed; Sec. I and II.4 read}}

@misc{OReilly2024,
  author = {O'Reilly, J. and Toh, G. and Goetting, I. and Saha, S. and Shalaev, M. and Carter, A. and Risinger, A. and Kalakuntla, A. and Li, T. and Verma, A. and Monroe, C.},
  title  = {Fast photon-mediated entanglement of continuously-cooled trapped ions for quantum networking},
  year   = {2024}, eprint = {2404.16167}, archivePrefix = {arXiv},
  note   = {Journal volume conflicting in fetched metadata (113 vs 133); abstract read only}}
```

Already in `references_design.bib` and checked against the opened abstract page: `Todaro2021` (arXiv:2008.00065, authors, journal and volume match) and `Hampel2023` (arXiv:2302.01462, journal and volume match). The Hampel ion species is **not confirmed** (see above). Not edited here.

---

## Not found / gaps

- A textbook passage stating that J = 1/2 fluorescence is isotropic in intensity. Not opened: Budker/Kimball/DeMille, Foot, and the Auzinsh/Budker/Rochester book (excerpt only).
- A direct Ba⁺ 493 nm scattering-rate or saturation measurement. Only the ~10⁷ s⁻¹ figure in Zhukas et al.
- An opened Ba⁺ SNSPD detection-time and fidelity result. Only the Duke excerpt (NA 0.8, 36 % collection).
- Journal details for Zhukas et al. (arXiv:2006.12801) and Auzinsh et al. (arXiv:0908.2666).
- Hampel et al. ion species (Ca⁺ per excerpt only).
