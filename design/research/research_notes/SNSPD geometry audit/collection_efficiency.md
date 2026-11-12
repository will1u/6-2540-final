# SNSPD geometry and total collection efficiency at 493 nm (138Ba+), with 370/422 nm comparison

> **Superseded in part (2026-11-11).** The absorption tables and the refraction check (line 138) assume the v3 stack: an 80 nm SiO₂ cap over 10 µm of SiO₂, and a 150 nm Al layer (lines 9, 24 and 26). v4 has a 160 nm cap, no 10 µm SiO₂, and a 100 nm inlaid Al mirror, so these absorption and footprint values do not describe the current chip. Current: [layer stack](../../../fab/STACK.md).

> Claude-authored research notes (design/research). Not a substitute for reading the cited sections. Tags: **[team calc]** = computed for this project in this session, **[inference]** = reasoning, not data. "Read" means the full text (or the stated part) was opened; "excerpt only" means only a search snippet or abstract was seen.

Factorisation used throughout: η_total = (geometric fraction of photons that reach the active area) × (NbN absorption A for that light) × (internal detection efficiency, IDE). The previous report (`design/research/reports/Trap integrated SNSPD design.md`) already covers Todaro 2021 / Slichter 2017 / Hampel 2023 stacks, rf pickup and the team TMM; only new material is given here.

**Calculation provenance.** All [team calc] absorption numbers come from `emt_angle_fill.py` (the script was a scratch file and is not in the repo; copy it into `design/sim/` if you want to keep it). It is the transfer-matrix / zeroth-order effective-medium (EMT) model of `design/sim/09b_itoD2_matching.py`, extended to oblique incidence with an anisotropic wire layer (ε across wires = harmonic mean, ε along wires and normal = arithmetic mean), same n,k (NbN 2.109+1.997i, Al 0.605+5.245i, SiO2 1.463), same v3 stack (vacuum / 10 µm SiO2, fringe-averaged / 80 nm SiO2 cap / NbN / 238 nm SiO2 spacer / 150 nm Al / 1 µm SiO2 / Si). It reproduces 09b's 0.401 at normal incidence. EMT is the zero-pitch limit; at 200 nm pitch (≈0.6 λ/n_SiO2) it is only indicative. RCWA/FDTD is needed before sign-off.

---

## Q1. What fill factor and wire width maximise absorbed fraction at 493 nm in the mirror-backed stack, for unpolarised/dipole light over a ±30° cone?

### Takeaway
In the current stack the absorption is limited by the **TM (E across wires) channel**, not by the cavity or by angle: TE is already ≈0.61, TM only ≈0.20. Raising the fill factor is the dominant lever: in EMT, 7 nm NbN goes from A ≈ 0.40 (f = 0.5) to ≈0.49 (f = 0.6), ≈0.60 (f = 0.7) and ≈0.71 (f = 0.8), averaged over the real emission cone. Angle (0–32°) costs ≤ 0.01–0.03. Re-tuning spacer/cap gains < 0.01. f = 0.5 at 200 nm pitch is not optimal for unpolarised light. It is the classic 1550 nm compromise, and NIST's own ion-trap and UV devices used f ≈ 0.55–0.65.

### Cited Findings
- **Anant 2008, measured (1550 nm, NbN, front illumination, no cavity):** 200 nm pitch / f = 0.5 absorbed 21% for E parallel to the wires vs 10% perpendicular. 200 nm / f = 0.25 absorbed 14% vs 6%. In their model, A∥ depends **only on fill factor**, independent of pitch. A⊥ **falls as pitch decreases at constant fill factor**, because the field inside NbN drops at every air–NbN interface, so a fill-factor-only effective index fails for perpendicular polarisation. Read Fig. 1(c,d) (model vs f and pitch), Fig. 4 (five geometries), and Fig. 5 (DE vs absorptance). The paper does **not** study incidence angle or visible wavelengths. — [Anant et al., Opt. Express 16, 10750 (2008), arXiv:0806.3194](https://arxiv.org/abs/0806.3194)
- **Wollman 2017 (MoSi, UV):** 110 nm wide × 10 nm thick wires, pitch "below 200 nm" to avoid diffraction (so f > 0.55). RCWA gives ≈75% unpolarised MoSi absorption for the broadband Si-backed stack and **96% unpolarised** for the DBR stack near 370 nm, where TE and TM are equal. Measured SDE was 76 ± 4% (56 µm diameter, narrowband), 69 ± 4% (broadband) and 69 ± 4% (16 µm). Read Sec. 2 and Fig. 1(c) (TE/TM/unpolarised RCWA curves) and Table 1. — [Wollman et al., Opt. Express (2017), arXiv:1708.04231](https://arxiv.org/abs/1708.04231)
- **Todaro 2021 used f ≈ 0.65:** 110 nm wires on a 170 nm pitch, 72% design SDE (see previous report). — [Todaro PRL Supp. "Trap fabrication", arXiv:2008.00065](https://arxiv.org/abs/2008.00065)
- **SMSPD precedent for f ≈ 0.8:** a 1 µm wide NbN strip with "filling factor near 0.8" in a DBR cavity reached 92.2% SDE at 1550 nm and a polarisation extinction ratio of 1.03 (**excerpt only**, full text not read). — [Xu et al., Photonics Research 9, 958 (2021), arXiv:2101.05407](https://arxiv.org/abs/2101.05407)
- **Fractal precedent at low fill factor:** f = 0.31, 40 nm wide, 9 nm NbTiN, simulated 96% absorptance at 1550 nm in a cavity, "completely polarization-independent" (Fig. 1e–f). This shows that a strong cavity, not fill factor alone, drives absolute absorption at 1550 nm. — [Meng et al., arXiv:2012.06730](https://arxiv.org/abs/2012.06730)
- **Team baseline numbers** (current v3 stack): 7 nm NbN, f = 0.5, A ≈ 0.40 (`sim/09b`). The wire inductance estimate in `sim/06_detector_size.py` uses a **5 nm** film (Lk ≈ 105 pH/sq from R_s ≈ 600 Ω/sq). — project files `design/sim/09b_itoD2_matching.py`, `design/sim/06_detector_size.py`

**[team calc] EMT, normal incidence, v3 thicknesses (spacer 238 nm, cap 80 nm):**

| NbN t | f | TE (E ∥ wires) | TM (E ⊥ wires) | Unpolarised |
|---|---|---|---|---|
| 5 nm | 0.5 | 0.49 | 0.15 | **0.32** |
| 5 nm | 0.7 | 0.61 | 0.37 | 0.49 |
| 7 nm | 0.4 | 0.53 | 0.12 | 0.32 |
| 7 nm | 0.5 | 0.61 | 0.20 | **0.40** |
| 7 nm | 0.6 | 0.67 | 0.31 | 0.49 |
| 7 nm | 0.7 | 0.72 | 0.46 | **0.59** |
| 7 nm | 0.8 | 0.77 | 0.65 | 0.71 |
| 10 nm | 0.5 | 0.73 | 0.26 | 0.50 |
| 10 nm | 0.7 | 0.84 | 0.56 | 0.70 |

- **Re-optimising spacer (190–280 nm) and cap (20–300 nm)** for unpolarised light changes these by ≤ 0.01. The optimum spacer is 226–238 nm for all f and t, so the current 238 nm is already right [team calc].
- **Angle, 7 nm, f = 0.5 (vacuum angle):** unpolarised mean 0.401 (0°), 0.403 (17°), 0.396 (25°), 0.389 (32°), 0.367 (40°). The four polarisation/plane channels stay within ±0.05 of their normal-incidence values up to 32° [team calc].
- **Cone average** (isotropic, unpolarised emitter; aperture at 54.8 µm for A30 and 53.96 µm for B60, i.e. ion height + 6 µm Au, as in `sim/06`; wires along the trap axis):

| Case | A30 | B60 |
|---|---|---|
| f 0.5, 7 nm | 0.401 | 0.399 |
| f 0.6, 7 nm | 0.491 | 0.489 |
| f 0.7, 7 nm | 0.596 | 0.596 |
| f 0.5, 10 nm | 0.497 | 0.496 |

  The cone hardly matters for absorption [team calc].
- **Diffraction bound on pitch [team calc]:** no diffracted order propagates in the SiO2 above the wires if Λ < λ/(n(1 + sin θ_int)). At 493 nm that is 337 nm at normal incidence and ≈247 nm at the B60 corner ray (31.7° in vacuum → 21° in SiO2). 200 nm is safe. A wider wire at fixed f = 0.5 (e.g. 150 nm wire on 300 nm pitch) would cross this bound for part of the cone, and EMT would no longer apply. This is consistent with Wollman's "pitch < 200 nm" rule at 370 nm.

### Inferences
- **The best fill factor is the highest one lithography and IDE allow**, roughly 0.65–0.75 at 200 nm pitch (130–150 nm wires with 50–70 nm gaps) [inference from the table]. In EMT, TM absorption rises steeply with f, while TE saturates. The gain from 0.5 → 0.7 (×1.5) is larger than the gain from 5 → 7 nm or 7 → 10 nm NbN.
- **Two ways to raise f, with different costs** [inference, team calc using `sim/06` scaling L ∝ length/width]:
  - *Keep 200 nm pitch, widen the wire to 140 nm (f = 0.7).* Same wire length, ≈0.71× the squares, so L ≈ 3.4 µH and τ ≈ 67 ns for A30. Switching current rises about 1.4×. The risk is IDE (Q4).
  - *Keep 100 nm wires, shrink the pitch to 143 nm* (43 nm gaps). Wire length ×1.4, so L ≈ 6.6 µH and τ ≈ 131 ns for A30. More length means more constriction risk, and 43 nm HSQ gaps are harder. IDE is unchanged.
- **The thickness assumption is inconsistent across scripts.** The optical model uses 7 nm NbN (A = 0.40); the inductance model uses the 5 nm Dane/Toomey film (A would be 0.32 at f = 0.5). Pick one measured thickness and use it in both.
- **Pitch at fixed f is a second-order effect for TE** (Anant) and lowers TM at smaller pitch. EMT is the zero-pitch limit, so it probably *underestimates* TM at 200 nm pitch [inference from Anant Fig. 1(d)]. RCWA would settle the sign and size.

### Gaps
- No RCWA/FDTD at 493 nm for NbN gratings was found in the literature, and none has been run for this stack. EMT at Λ ≈ 0.6 λ/n is indicative only.
- NbN n,k for the team's room-temperature bias-sputtered film is not measured. The two literature datasets differ by ~20% (previous report).
- Hampel's NbTiN (90/180 nm, f = 0.5) and Slichter's MoSi stacks were not re-modelled at their own wavelengths with this oblique code.

---

## Q2. Does the wire direction (along the trap axis) relative to the ion's emission polarisation matter?

### Takeaway
**For 138Ba+ at 493 nm, no.** The S1/2–P1/2 emission is isotropic and, for any linear-dichroic detector, effectively unpolarised for *any* P1/2 state and any B-field direction. The same holds for Yb+ 370 nm (P1/2 F'=0) and Sr+ 422 nm (P1/2). So a meander along the axis absorbs exactly the unpolarised average, (TE+TM)/2, and spiral/fractal layouts only equalise TE and TM. They do not raise this average. The same physics changes the **geometric** term: the 3.25% / 5.92% in `DESIGN_LOG` step 7 assume a σ dipole with quantisation axis normal to the surface. For Ba+ 493 nm the isotropic values are **≈2.22% (A30) and ≈4.15% (B60)** [team calc].

### Cited Findings
- **Polarisation contrast is large in a meander.** 21% vs 10% (Anant, 1550 nm). 0.61 vs 0.20 in the team stack at 493 nm [team calc, Q1 table].
- **Spiral and fractal layouts remove the contrast.** Fractal (arced Peano, NbTiN): measured polarisation sensitivity 1.02 (+0.06/−0.02), SDE 84 ± 3% at 1575 nm (Fig. 2a–c). Simulated meander polarisation ratio grows with wavelength, while the fractal stays at 1 from 0.6 to 5 µm (Fig. 4). — [Meng et al., arXiv:2012.06730](https://arxiv.org/abs/2012.06730)
- **Earlier fractal:** polarisation sensitivity 1.1 at 1550 nm (**excerpt only**). — [Chi et al., Opt. Lett. 2018, KTH PDF](https://www.aphys.kth.se/polopoly_fs/1.849863.1600688358!/2018_OL_Fractal%20superconducting%20nanowire%20single-photon%20detectors%20with%20reduced%20polarization%20sensitivity.pdf)
- **Spiral (Dorenbos):** a spiral "reduced significantly" the polarisation sensitivity. Seen only as a citation in a review excerpt; **the Dorenbos paper was not opened**. — [review excerpt, arXiv:1807.09060](https://arxiv.org/pdf/1807.09060)
- **Wollman's DBR stack** makes TE and TM absorption equal near 370 nm (Fig. 1c). A cavity design can also remove the contrast for a meander. — [Wollman, arXiv:1708.04231](https://arxiv.org/abs/1708.04231)
- **Team collection model.** `trapcalc.collection_fraction(..., "sigma")` uses w = 3/(16π)(1+cos²θ) with θ from the surface normal ("dipole rotating in the surface plane, quantization axis along z"). `sim/06` calls it with "sigma". — project files `design/sim/trapcalc.py` lines 156–176, `design/sim/06_detector_size.py` line 34

**[team calc] derivation, worth checking by hand.**
- P1/2, m' = +1/2 decays by π to S1/2 m = +1/2 (branching 1/3) and by σ to m = −1/2 (2/3). With normalised patterns π: (3/8π) sin²θ and σ: (3/16π)(1+cos²θ), the sum is (1/8π) sin²θ + (1/8π)(1+cos²θ) = 1/(4π). The emission is **isotropic**.
- Polarisation, resolved on the (e_θ, e_φ) basis: π gives (1/3) sin²θ in e_θ. σ gives (1/3) cos²θ in e_θ and 1/3 in e_φ, with a 90° phase between them. Total: 1/3 in each. So the linear Stokes parameters Q = U = 0, and only a circular part V remains.
- Any J = 1/2 density matrix is a spin pointing somewhere, so the result holds for any population or coherence, and any B direction.
- Consequence: a non-chiral linear grating absorbs the unpolarised average, (TE+TM)/2.
- Corrected geometric fractions: the same integral with an isotropic pattern gives 2.22% (A30, aperture 54.8 µm) and 4.15% (B60, 53.96 µm), versus 3.25% / 5.92% with "sigma" [team calc, scratch script].

### Inferences
- **Wire direction is not a collection lever for Ba+ 493 nm** [inference from the derivation]. It can be chosen for other reasons: lead routing, rf coupling (Todaro aligned wires with the axis), and current-crowding at turns.
- **The "sigma" pattern is right only for a closed σ cycling line with B normal to the surface** (e.g. Be+ S1/2→P3/2 stretched states) [inference]. Todaro's Be+ had B in-plane at 45°, which favours *less* emission toward the surface.
- **Realistic Ba+ totals with IDE ≈ 1** [team calc]:

| Detector | f 0.5 | f 0.7 |
|---|---|---|
| A30 | 2.22% × 0.40 ≈ 0.9% | 2.22% × 0.60 ≈ 1.3% |
| B60 | 4.15% × 0.40 ≈ 1.7% | 4.15% × 0.60 ≈ 2.5% |

  The DESIGN_LOG implies ≈1.3% for A30 (3.25% × 0.40). For scale, Todaro achieved ≈2.0% × 48% ≈ 1.0%.
- **Small residual effect:** at oblique, off-axis azimuths a 1D grating can have a small circular-dichroism term that couples to V. It is expected to be negligible here [inference, not computed; the scratch model ignores azimuthal s–p mixing and interpolates A as cos²φ/sin²φ between the two principal planes].

### Gaps
- No literature source was opened that states the J=1/2→1/2 isotropy explicitly. Check it against an atomic-physics text (angular distribution of dipole radiation summed over final Zeeman states).
- Not checked: whether any planned 493 nm detection uses polarisation-selective optics or a cycling configuration that would break this.
- The ray-optics aperture model ignores the Au sidewall (6 µm) and refraction-induced footprint growth (Q3).

---

## Q3. What is the best realistic detector area, given the window-size penalty on trapping, and what have published trap-integrated detectors achieved?

### Takeaway
- **Collection** grows about linearly with the axial window length at fixed 30 µm radial width: isotropic 2.22% for 30 µm → 4.15% for 60 µm [team calc].
- **The trap penalty grows faster.** B60 has 1.8× the null drop, 3.6× the axial pseudopotential, and a 10° radial tilt needing 15.2 V, outside the ±10 V DACs (DESIGN_LOG).
- **Better levers:** with today's DACs, raising A from 0.40 to ≈0.6 via fill factor buys the same ×1.5 as going from A30 to ≈45 × 30 µm, with no trap penalty.
- **Published trap-integrated SNSPDs** reached SDE 48–76%, but only ≈1% total because of 2–3% solid angle. **Rf pickup and heating**, not optics, cut SDE in the trap.

### Cited Findings
- **Project window study** (planar + 3-D FD):

| Window | Geometric collection ("sigma" model) | L | Δh |
|---|---|---|---|
| 20 × 20 µm | 1.46% | 2.1 µH | – |
| 30 × 30 µm | 3.25% | 4.7 µH | −1.2 µm |
| 45 × 30 µm | 4.46% | 7.1 µH | – |
| 60 × 30 µm | 5.92% | 9.4 µH | −2.0 µm |

  - Radial width is capped at 30 µm by the 40 µm centre DC with 5 µm rims.
  - B60 has 1.8× the drop and 3.6× the axial pseudopotential of A30 for 1.8× the collection.
  - The 10° radial tilt needs 13.2 V (A30) and 15.2 V (B60), over the DAC range; with no tilt, 6.6 / 3.4 V.

  — project file `design/DESIGN_LOG.md` (steps 7 and 19; table at lines ~256–261, comparison at ~866–871); `design/CLAUDE.md` key numbers
- **Slichter 2017:** SDE 76 ± 4% at 315 nm and 3.2 K, background < 1 s⁻¹ at saturation. "Typical RF trapping fields reduce system detection efficiency by 9%" without raising background. Integrated test traps ran at 3.8 K. (Abstract read; geometry rule of 3–8% solid angle, NA 0.35–0.55, from Sec. 2 per previous report.) — [Slichter et al., Opt. Express 25, 8705 (2017), arXiv:1611.09949](https://arxiv.org/abs/1611.09949)
- **Todaro 2021:** 2.0(1)% of photons hit the 22 × 20 µm area (dipole pattern included). SDE 48(2)% with rf, ≈65(5)% estimated without rf, against a 72% design (previous report; PRL pp. 2–3, Supp. Eq. S6). — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)
- **Hampel 2023:** NbTiN, 90/180 nm, 20 × 30 µm. SDE ≈68% with an Al mirror vs ≈40% without at ≈395 nm (previous report's reading; Figs. 3–4). Remaining limit: rf heating once the mirror is grounded. — [arXiv:2302.01462](https://arxiv.org/abs/2302.01462)
- **Wollman 2017:** a 56 µm diameter MoSi detector kept 76% SDE. Large area does not by itself cost efficiency in amorphous films. — [arXiv:1708.04231](https://arxiv.org/abs/1708.04231)

### Inferences
- **Refraction check [team calc].** The 10 µm SiO2 between the aperture (bottom of the Au) and the NbN shifts edge rays outward by 10 µm × tan(θ_int). That is ≈2.5 µm at the A30 corner (21° in vacuum → 14° in SiO2) and ≈3.9 µm at the B60 corner (31.7° → 21°). A meander exactly the size of the window misses that rim. `sim/06` assumes "~2 µm per side" is caught. Worth checking that the NbN meander is ≥ window + ≈3–4 µm per side, or quantifying the loss.
- **"Best realistic area" [inference]:**
  - The radial size is fixed at 30 µm by the electrode.
  - Axially, the marginal collection per µm is constant, while the DC-tilt voltage and axial pseudopotential grow (A30 → B60: the tilt requirement exceeds the DACs in both).
  - Under the current DAC range, ≈30–45 µm axial plus a higher fill factor gives more collection per unit trap penalty than 60 µm at f = 0.5.
  - If the readout runs with zero tilt (6.6 / 3.4 V), B60's penalty is the 2.0 µm null drop and the axial bump, and its 4.15% × A wins outright.
- **Lowering the ion is the other lever** (collection ∝ h⁻² at fixed size, DESIGN_LOG step 1). The team already rejected it because heating rises faster.
- **What limits trap-integrated detectors is mostly not optics.** Todaro lost 72 → 48% to rf pickup; Slichter lost 9% to rf; Hampel's residual limit was rf heating [inference from previous report + Slichter abstract]. A 0.5 → 0.7 fill-factor change attacks the 0.40 absorption, which is the biggest *optical* loss in this design.

### Gaps
- Trap-integrated SPAD/APD alternatives (e.g. Setzer et al. 2021, Sandia; Reens et al. 2022, MIT-LL) were **not opened**; their efficiency numbers are not given here.
- No 3-D FD run exists for 45 × 30 µm. The DC-tilt voltage as a function of window length between 30 and 60 µm is not tabulated.
- The Slichter 2017 active area and Ion/SNSPD distance were not re-extracted in this session.

---

## Q4. Do wider wires (150–300 nm, or µm-wide SMSPDs) keep saturated IDE at 493 nm in NbN, and what do alternative layouts (spiral, fractal, SNAP/arrays, SMSPD) buy?

### Takeaway
- **Plateau is plausible for NbN up to ~130–180 nm wide at 400–500 nm**, but only measured for thin (3.6–4.8 nm), higher-Tc films. Lusche measured meanders 85–178 nm wide with a short-wavelength plateau and a near-IR cut-off that scales as 1/w (Fig. 3, Fig. 5).
- **Thicker films move the cut-off toward the blue** (Hofherr/Henrich, excerpt).
- **Micron-wide NbN bridges do detect 408 nm single photons**, but Korneeva **did not observe IDE saturation**. IDE reached only "tens of percent" near Ic, with j_det ≈ 0.5 j_dep at 408 nm. Saturated micron-wire detectors exist in WSi/MoSi (Chiles) and, reportedly, He-ion-irradiated NbN (Xu 2021); both are excerpt only.
- **So: 140 nm wires for f = 0.7 are a moderate, testable risk; 0.5–3 µm NbN strips in standard sputtered NbN are a high risk.**
- **Spirals and fractals** fix polarisation and current crowding, not unpolarised absorption.

### Cited Findings
- **Lusche 2013 (NbN on 250 nm SiO2 on Si, ~4 × 4 µm meanders):** Table I gives the NbN set, thickness / width / Tc:

  | Samples | Thickness | Width / Tc |
  |---|---|---|
  | NbN1–4 | 3.6 nm | 122 nm / 9.0 K, 130 / 9.2, 156 / 10.2, 178 / 10.0 |
  | NbN5–7 | 4.8 nm | 85 / 8.5, 98 / 8.7, 130 / 9.4 |

  - Bias in the spectra: 0.5–0.7 I_dep.
  - Fig. 3 shows the 130 nm NbN IDE spectrum, with a plateau at short wavelengths and a cut-off fitted by IDE₀/(1+(λ/λ₀)^n). Below 450 nm the monochromator error reaches 35%.
  - The reciprocal cut-off wavelength scales linearly with width, as the non-homogeneous hot-spot model predicts (efficiency factor 0.43 for NbN). "With increasing wire thickness the cut-off wavelength decreases."
  - Read Table I, Fig. 3, Fig. 5 (λ₀ vs 1/w; cut-off values must be read off the figure).

  — [Lusche et al., arXiv:1303.4546 (DOI 10.1063/1.4891105 as listed on arXiv)](https://arxiv.org/abs/1303.4546)
- **Korneeva 2018:**
  - 5.8 nm reactively sputtered NbN, bridge widths 0.53–5.15 µm, constriction geometry with edges as circle segments (R = 8.6 µm) to avoid current crowding (Fig. 1).
  - Single-photon response confirmed at 408, 829 and 1550 nm (Fig. 4, linear count vs photon number at 0.7 and 0.9 I/I_dep).
  - IDE "reaches value of tens of percents near the experimental critical current". "We also do not observe a saturation of IDE", attributed to the widening geometry (Fig. 6).
  - j_det ≈ 0.5 j_dep at 408 nm; experimental j_c ≈ 0.7 j_dep (Fig. 7).
  - Read Sec. IV, Fig. 6–7, App. C Fig. 11 (model: I_det^max/I_dep saturates for w ≳ 100ξ).

  — [Korneeva et al., Phys. Rev. Applied 9, 064037 (2018), arXiv:1802.02881](https://arxiv.org/abs/1802.02881)
- **Chiles 2020 (WSi microwires), excerpt only:** saturated IDE at 1.55 µm for 1–3 µm wide out-and-back wires (100 µm long) and for a 2 µm meander over ≈362 × 362 µm². Many devices reach Ic > 50% of depairing. — [Chiles et al., APL 2020, arXiv:2002.12858](https://arxiv.org/abs/2002.12858)
- **Luskin 2023, excerpt only:** 1 mm², 8-pixel, 1 µm WSi and MoSi arrays; saturated IDE at 1064 nm in 6/8 pixels for the best WSi device. — [arXiv:2303.10739](https://arxiv.org/abs/2303.10739v1)
- **Xu 2021 (NbN SMSPD), excerpt only:** 1 µm wide strip, f ≈ 0.8, NbN pre-irradiated with He ions, 92.2% SDE at 1550 nm and 0.84 K; >70% at 2.1 K. — [arXiv:2101.05407](https://arxiv.org/abs/2101.05407)
- **Wollman 2017:** 110 nm × 10 nm MoSi was "the largest" cross-section that still saturated at 370 nm while maximising operating temperature, with plateaus up to 4.2 K and from 250–373 nm (Fig. 2, Fig. 4a). No width sweep was published. — [arXiv:1708.04231](https://arxiv.org/abs/1708.04231)
- **Hofherr 2010, excerpt only:** NbN 4–12 nm thick, 400–2000 nm. Thinnest devices reach ≈70% IDE in the visible, and the thickness dependence supports a hot-spot red boundary. — DOI 10.1063/1.3437043 (search excerpt via [DLR elib](https://elib.dlr.de/67725/))
- **Henrich 2012 (spiral), abstract only:** 4 nm NbN on sapphire, widths 100–300 nm. The spiral is "less susceptible to the critical current reduction in sharp turns". At 100 nm it reaches 27.6% DE in the optical range, ≈1.5× the meander, and "more than doubled" in the IR. — [Henrich et al., arXiv:1210.3988](https://arxiv.org/abs/1210.3988)
- **Meng (arced fractal):** standard fractal turns cut the normalised switching current to 0.67; arced turns restore 0.81, vs 0.82 for a meander (Fig. 1d–e). Built as 16 cascaded 2-SNAPs (Fig. 1g). Estimated ceiling 93% SDE; the shortfall was attributed to misalignment and IDE < 1. — [arXiv:2012.06730](https://arxiv.org/abs/2012.06730)

### Inferences
- **Why widening the wire can help on two fronts [inference].** In the hot-spot picture the detectable width scales roughly with photon energy. 493 nm photons carry ≈3.1× the energy of 1550 nm photons, so the visible plateau should survive to wider wires than the ~100 nm IR rule (consistent with Lusche's 1/w scaling). The team's room-temperature NbN has lower Tc (≈7.8 K) and a smaller gap than Lusche's 9–10 K films, which also tends to help.
- **Why it can also hurt [inference].** The ≈5–7 nm thickness pushes the cut-off blueward. So 130–150 nm at 5–7 nm Dane-NbN is the regime to measure, not assume.
- **Hairpins matter more as fill factor rises [inference].** At 200 nm pitch and f = 0.7, the 60 nm gap makes the hairpin inner corner sharper relative to the width, so current crowding grows. Rounded/arced turns or bends placed outside the illuminated area keep the switching current near the straight-wire value (Meng Fig. 1e; Henrich abstract).
  - A spiral (Henrich) removes all but one central S-turn and is polarisation-insensitive. For Ba+ the polarisation property is irrelevant (Q2). The turn-loss property is the reason to consider it.
- **SNAP/parallel wires and arrays [inference].** They raise the output signal and allow larger area at fixed reset time (L/n²). They do not change absorption, which is set by local fill factor and the stack. For a 30 × 60 µm detector, L = 9.4 µH (τ ≈ 190 ns) is already acceptable for ion readout (~10–100 µs), so the main benefits would be signal amplitude against rf pickup and yield, not efficiency.
- **SMSPD (0.5–3 µm) at 493 nm in NbN [inference].**
  - Advantages: optically, f ≈ 0.8–0.9 is easy and absorption would rise toward the f = 0.8 row of the Q1 table (≈0.7 for 7 nm). Wide strips can use photolithography and are robust to constrictions.
  - Blockers: Korneeva's unsaturated IDE in standard NbN, plus the need for I_bias near ~0.5–0.7 I_dep, which leaves little margin for the 1–4 µA rf-induced currents seen in trap environments.
  - Pitch of ~1 µm puts the grating well into the diffractive regime at 493 nm, so EMT is invalid and RCWA is required.

### Gaps
- **No primary measurement was found of NbN IDE vs width specifically at 450–500 nm for 5–7 nm room-temperature bias-sputtered films.** The closest data are Lusche (3.6–4.8 nm, 9–10 K films; cut-off values only in Fig. 5, not extracted) and Korneeva (micron bridges, unsaturated).
- Not opened: Marsili/Verma WSi and MoSi width studies, Reddy/Marsili 98% papers, Vodolazov 2017 kinetic-equation theory (PR Applied), the Dorenbos and Chi fractal OL papers (excerpt only), Clem & Berggren 2011 current crowding, and SNAP papers (Ejrnaes/Marsili). Treat their claims here as unsourced.
- Xu 2021 and Chiles 2020 numbers come from search excerpts only.
- Whether the T8 EBL dose array on the test die spans enough width to measure the 100 → 150 nm IDE transition was not checked (project file not opened for this).
