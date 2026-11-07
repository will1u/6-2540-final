# Five-wire surface-electrode Paul trap design rules for 138Ba+ at about 50 um ion height (1 cm x 1 cm chip, loading zone and separate readout zone)

Notation used in these notes: a = centre (RF-ground) electrode width, b = width of each RF rail (symmetric case), h (= d = z0) = ion height above electrode plane, V = RF amplitude (zero-to-peak), Omega = 2*pi*f_RF, Q = e, M = ion mass (138Ba+: 137.905 amu). "Gapless" means the gapless-plane approximation (electrodes tile an infinite plane, gaps -> 0).

Method note: several key PDFs (Chiaverini 2005, Wesenberg 2008, Sterling 2013, Shi 2023, Todaro 2021, Bautista-Salvador 2019) were downloaded and text-extracted with pdftotext; equation and figure pointers below come from that text. House 2008 (PRA 78, 033402) full text was NOT accessible (paywalled, no arXiv preprint found), so its equation numbers are not given. Numbers labelled "computed" were calculated by me in this session from the gapless analytic model (pure-Python script, arctan strip potentials) and cross-checked against Wesenberg's published example values.

## 1. Analytic five-wire model: ion height, trap depth, q, optimal width ratios

### Takeaway
For a gapless symmetric five-wire trap, the RF null sits at h = (1/2)*sqrt(a(a+2b)) (asymmetric rails b, c: h = sqrt(a*b*c*(a+b+c))/(b+c)); the depth is kappa*U0 with U0 = Q^2 V^2 / (4 M Omega^2 h^2), and kappa peaks at 0.0091 when b/a ~ 3.7, while the RF curvature (hence q and secular frequency) peaks near b/a ~ 2.5. Five-wire depth is only ~1% of an equivalent two-layer quadrupole (Chiaverini Fig. 4c). For 138Ba+ at h = 50 um, the formulas map the parameter space as follows (computed table under Inferences): a ~ 35-58 um and b ~ 58-127 um set the height, and f_RF ~ 30-50 MHz with V ~ 100-200 V spans q ~ 0.15-0.5, radial ~ 3-7 MHz and gapless RF depth ~ 0.04-0.4 eV. Picking a point in this space is a project design decision.

### Cited Findings
- Chiaverini et al., "Surface-electrode architecture for ion-trap quantum information processing", Quantum Inf. Comput. 5, 419 (2005), arXiv:quant-ph/0501147 (verified on arXiv; listing says QIC Vol. 5, No. 6; the extracted PDF page headers run 424-432, consistent with a first page of 419). The five-wire design keeps centre and outer electrodes at RF ground with two RF rails, and the trap axis sits above the centre electrode (Sec. 4, Fig. 4c) — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Chiaverini Fig. 4 caption: normalised to a two-layer quadrupole with aspect ratio 1 (same drive frequency, RF amplitude, ion mass, same ion-to-nearest-electrode distance d, electrode thickness 0.10d), the five-wire surface trap has secular frequency fi = 0.30 and trap depth umax = 0.010, so its depth is ~1% of that quadrupole. The four-wire planar trap has fi = 0.34 and umax = 0.017 — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Chiaverini Sec. 5: surface-trap radial frequencies are ~1/6 to 1/3 of a four-rod quadrupole of similar size. The depth is set by a pseudopotential local maximum above the trap axis at a distance of order d, and is smaller by a factor ~30-200 than a standard quadrupole depending on electrode shape. The static (DC) axial-confinement potential and principal-axis rotation can deepen the trap by a factor of about 2 — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Chiaverini Appendix A (thin-wire model): trap minimum at y = sqrt(3)/2 (wire spacing units), radial secular frequency ~0.29 of the standard quadrupole, depth lower by 3(12+7*sqrt(3)) ~ 72. With finite-diameter (0.2) electrodes the frequency factor is ~0.16 and the depth factor ~200 — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Chiaverini Sec. 6 design example: calculations suggest trapping ~50 um from the chip surface with secular frequencies ~10 MHz for 100 V RF at 100 MHz, and control voltages of a few volts giving axial frequencies of a few MHz. Note the ion species is not stated in that sentence; NIST used light ions (Be+/Mg+), so this does not transfer directly to Ba+ (138 amu) — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Chiaverini Sec. 6, RF dissipation: P = I_rms^2 (R_lead + R_ESR) = (C*Omega*V_rms)^2 (R_lead + tan(delta)/(Omega*C)). For 100 V at 100 MHz, 1 ohm leads, 3 pF and tan(delta) = 4e-4 (fused silica), this gives ~20 mW. DC filters ~1 kOhm / 1 nF (~160 kHz roll-off) — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Chiaverini Sec. 6, dielectric constant: comparing substrate epsilon = 1 vs epsilon = 10, for gaps as large as 1/4 of the electrode-segment width the field change near the trap is at the ~1% level — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Wesenberg, "Electrostatics of surface-electrode ion traps", arXiv:0808.1623 (v2, Dec 2008). The published version is, I believe, Phys. Rev. A 78, 063410 (2008), but I did not verify this in this session. Sec. II A: the gapless-plane approximation needs gaps << d, total trap extent >> d, and other conductors at distance >> d. Corrections from nearby conductors are first order in (electrode extent)/(distance to the conductors) — [arXiv:0808.1623](https://arxiv.org/abs/0808.1623)
- Wesenberg Eq. (9): q0 = 4 Q V_rf / (M Omega^2 d^2). Eq. (12): depth scale U0 = Q^2 V_rf^2 / (4 M Omega^2 d^2). With the example parameters of Eq. (11) (Omega = 2*pi*100 MHz, V_rf = 100 V, M = 10 amu, d = 100 um) the paper gives q0 = 0.98 and U0 = 6.1 eV. I recomputed both and they match these formulas — [arXiv:0808.1623](https://arxiv.org/abs/0808.1623)
- Wesenberg Sec. IV, Eq. (25): the quadrupole q equals a geometric strength factor times q0, and the strongest surface-electrode multipole is weaker than the strongest 3D multipole at the same d. For the Eq. (11) parameters the maximum secular frequency is 5.5 MHz, which implies q_max ~ q0/(2*pi) ~ 0.16. That ratio is my inference from the stated numbers, because the extracted equation text was garbled — [arXiv:0808.1623](https://arxiv.org/abs/0808.1623)
- Wesenberg Sec. V A, Eqs. (28)-(30): there is a maximal intrinsic (no DC field) depth for surface quadrupoles, reached along a one-parameter family of geometries (Eq. 28), and for the Eq. (11) parameters it is U*_s(2) = 55.8 meV. 55.8 meV / 6.1 eV = 0.0091, consistent with Eq. (30) U*_s(2) = (5*sqrt(5) - 11)/(2*pi^2) * U0 ~ 0.0091 U0. I reconstructed that expression from garbled text plus the numeric check — [arXiv:0808.1623](https://arxiv.org/abs/0808.1623)
- Wesenberg Sec. V B: a DC bias applied to the RF electrodes can increase depth by a geometry-only factor (up to 9.8x in his example, at a/q^2 = 0.14). Stability requires q < 0.7 and |a/q^2| < 0.5 — [arXiv:0808.1623](https://arxiv.org/abs/0808.1623)
- House, "Analytic model for electrostatic fields in surface-electrode ion traps", Phys. Rev. A 78, 033402 (2008), DOI 10.1103/PhysRevA.78.033402 (DOI resolves). It gives analytic potentials for planar electrodes and uses them to derive ion position, trap depth and stability parameters. I could not access the full text or its equation numbers — [APS](https://link.aps.org/doi/10.1103/PhysRevA.78.033402)
- Shi et al. 2023 (APL 122, 264002), Eq. (2): RF trap depth E_max = q^2 V_rf^2 / (pi^2 m Omega_rf^2 z0^2) * kappa(a,b), with kappa a dimensionless geometry factor for a five-wire trap (RF rails of width b separated by a; their Fig. 2a). DC voltages reduce the true depth below this "RF trap depth" — [Shi et al. 2023, OSTI copy](https://www.osti.gov/pages/servlets/purl/2425574)

### Inferences
- **Computed gapless five-wire relations** (my derivation, consistent with the cited formalisms). The potential of a strip is phi = (V/pi)[atan((x2-x)/y) - atan((x1-x)/y)]. Setting dphi/dy = 0 on axis gives h = sqrt((a/2)(a/2+b)) = (1/2)sqrt(a(a+2b)), and for unequal rails b, c, h = sqrt(abc(a+b+c))/(b+c). Near the null |E| ~ k V r / h^2. It follows that:
  - radial secular frequency: omega_r = Q V k / (sqrt(2) M Omega h^2)
  - Mathieu q: q = 2 Q V k / (M Omega^2 h^2) = (k/2) q0
  - depth: U = kappa * U0
- **Computed geometry factors** (normalised to fixed h, gapless):

  | b/a | h/a | escape-point height / h | kappa (depth / U0) | k (gradient) |
  |---|---|---|---|---|
  | 1.0 | 0.866 | 1.82 | 0.0055 | 0.275 |
  | 2.5 | 1.225 | 1.96 | 0.0088 | 0.318 (max ~ 1/pi) |
  | 3.68 | 1.446 | 2.06 | 0.0091 (max; matches Wesenberg Eq. 30) | 0.309 |
  | 6 | 1.80 | 2.21 | 0.0086 | 0.281 |

  So "depth-optimal" b/a ~ 3.7 and "strength-optimal" b/a ~ 2.5. The optimum is flat: kappa stays within 5% of maximum for b/a between ~2.5 and ~6. The escape point sits ~2h above the surface, along the vertical, which matters for loading and for any overhead structure.
- **Computed 138Ba+ numbers at h = 50 um** (gapless; pseudopotential approximation, reliable only for q below ~0.4):
  - b/a = 3.68 (a = 34.6 um, b = 127 um):
    - f = 41.1 MHz, V = 150 V: q = 0.39, f_r = 5.6 MHz, depth 216 meV
    - f = 50 MHz, V = 200 V: q = 0.35, f_r = 6.2 MHz, depth 259 meV
    - f = 30 MHz, V = 100 V: q = 0.49, f_r = 5.2 MHz, depth 180 meV
  - b/a = 1 (a = b = 57.7 um):
    - f = 41.1 MHz, V = 150 V: q = 0.35, f_r = 5.0 MHz, depth 129 meV
- **Constraints that bound the choice** (the choice itself is left to the project team):
  - Pseudopotential validity: the formulas above are trustworthy for q up to about 0.4. Wesenberg's stability limit is q < 0.7.
  - Gapless-model validity: Wesenberg requires gaps << d. A gap/h of about 0.1 or less is my reading of that condition, to be checked with gds2itvg/BEM.
  - Real depth versus the table: with DC axial confinement, finite gaps and finite electrode extent the depth will differ from the gapless value. Chiaverini notes DC can deepen it by about 2x for suitable principal axes, and Shi 2023 notes DC generally reduces it below the "RF trap depth".
  - Literature anchor: the MIT LL 50 um trap running Ba+ at 41.1 MHz with 1.9-3.3 MHz radial frequencies (Q4) implies roughly V ~ 60-100 V for the geometries tabulated above. This is my back-calculation; that paper does not state V.
  - Upper bound on V: RF flashover (Q8).
- **Sanity checks worth running on any chosen geometry:** compare the gds2itvg RF-null height to sqrt(a(a+2b))/2, and compare the simulated q to 2QVk/(M Omega^2 h^2).
- Since depth scales as V^2/(Omega^2 h^2) and q as V/(Omega^2 h^2), at fixed q the depth scales as q * V. Raising V and Omega together at fixed q increases depth linearly in V, and the ceiling is RF breakdown (Q8).

### Gaps
- House 2008 equation numbers and his explicit asymmetric-rail depth formula: full text not accessed. The h formula for asymmetric rails above is my derivation (it reduces to the symmetric case) and should be checked against House.
- Schmied 2010 (finite-electrode / optimal surface-electrode designs) was not retrieved, so no finite-gap correction factor is cited. Quantitative gap-induced reduction in q and depth for 5 um gaps at h = 50 um needs a BEM/FEM check.
- Wesenberg's PRA journal reference (78, 063410) is from memory, not verified here.

## 2. Outer DC segment width/pitch and count per zone

### Takeaway
Segment width should be of order the ion height: the axial curvature per volt is maximised at W/h ~ 0.8, and falls off significantly below W/h ~ 0.5, while splitting and separation favour wider segments (up to ~3.7 times the RF-rail separation). For h = 50 um this means segment widths ~40-100 um (pitch ~45-105 um with 5 um gaps). Each functional zone needs enough independent DC degrees of freedom to null all three stray-field components and to set axial curvature and principal-axis tilt, so in practice at least 5-7 electrodes per zone.

### Cited Findings
- "Transport dynamics of single ions in segmented microstructured Paul trap arrays" ("railway track" model; I believe the authors are Huber et al., NJP 2006, but did not verify authorship in this session), with segment width normalised to ion-electrode distance (W^ = W/d): the axial potential has a maximum at W^ ~ 0.78 and decreases significantly only for W^ < 0.5 — [arXiv:quant-ph/0606237](https://arxiv.org/pdf/quant-ph/0606237) (as quoted in search-result snippet; full text not re-read)
- Optimisation of segmented electrodes for fast ion separation in surface traps: the quartic coefficient is maximised for segment width W ~ 3.66a for one design and W ~ a for another, where a is the RF electrode separation, and larger widths are needed at larger ion-electrode distance (Fig. 5) — [arXiv:1007.3542](https://arxiv.org/pdf/1007.3542). I believe this is Nizamani and Hensinger (Appl. Phys. B, 2012), but the attribution was not verified in this session.
- A later trapped-ion/superconducting-qubit system design adopted w_outer ~ 3.66a = 66 um for its outer segmented electrodes — [arXiv:1510.07298](https://arxiv.org/pdf/1510.07298)
- Doret et al., NJP 14, 073012 (2012), arXiv:1204.4147 (GTRI): a CMOS-compatible linear surface trap with 44 independently controlled DC electrodes used for anharmonic wells, shuttling, splitting and merging, and tuning secular frequencies and trap-axis orientation. On-chip capacitors on the DC electrodes suppress RF pickup, a top ground layer simplifies modelling, and a localised substrate aperture is used for loading. Measuring and cancelling spatially varying stray fields produced nearly equally spaced chains — [arXiv:1204.4147](https://arxiv.org/abs/1204.4147)
- Todaro et al. 2021 (NIST): segmented outer electrodes move the ion along the RF null between zones, from over the SNSPD (zone D) to 264 um away (zone A), with the ion transported by time-varying potentials on the segmented outer electrodes — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)
- Chiaverini 2005 Sec. 4 suggests segmenting the centre electrode to help ion separation and notes that DC control of principal-axis angles changes depth. Fig. 6/7 discussion: separation electrodes whose field is cancelled elsewhere — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Chiaverini Sec. 6: typical DC RC filters (1 kOhm, 1 nF, ~160 kHz) allow transport in tens of microseconds — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)

### Inferences
- For h = 50 um, a segment width W ~ 50 um (W/h ~ 1) with 5 um gaps (pitch ~55 um) is close to the curvature optimum and also adequate for transport. Widening to ~100 um helps if splitting chains is needed.
- **Degrees of freedom per zone.** Each zone needs at least 5 linearly independent DC knobs: E_x (in-plane radial), E_y (vertical), E_z (axial position), axial curvature, and one cross-curvature term to tilt the radial principal axes (needed so the Doppler-cooling beam projects onto both radial modes).
  - With segmented outer DC on both sides and a single (unsegmented) centre electrode, the vertical field is weakly controlled. Use a split centre electrode or the RF-rail DC bias (Wesenberg Sec. V B) for vertical compensation.
  - A practical layout is 3 segments per side per zone (6) plus a centre electrode (or split centre) = 7-8 electrodes per zone.
- **Electrode count for this chip.** For a loading zone plus a readout zone separated by a transport region of length L at pitch p, count roughly 2*(L/p) + ~14 electrodes. For example, L = 500 um at p = 55 um gives ~32 DC electrodes, well within a 44-pin-class design (Doret).

### Gaps
- Amini et al. 2010 (NJP 12, 033031) and Blakestad 2011 (X-junction) segment pitches were not retrieved. A specific published "minimum number of segments for full 3D micromotion compensation" rule was not found; the 5-DOF count above is my inference.
- Moehring 2011 segment dimensions not retrieved.

## 3. Heating-rate scaling with ion-electrode distance, cryogenic rates near 50 um

### Takeaway
Surface-trap electric-field noise scales approximately as d^-4 (Sedlacek 2018, unchanged between room temperature and cryogenic), while needle-trap data give d^-3.5(1) and some planar data give shallower exponents (~2.6). The exponent is not universal. Cryogenic operation lowers rates by ~100x. A NIST trap-integrated-SNSPD trap at 3.5 K saw tens to ~100 quanta/s for 9Be+ at 29-39 um.

### Cited Findings
- Sedlacek, Greene, Stuart, McConnell, Bruzewicz, Sage, Chiaverini, "Distance scaling of electric-field noise in a surface-electrode ion trap", Phys. Rev. A 97, 020302(R) (2018), arXiv:1712.00188. Ions were held at five ion-electrode distances in one multizone surface trap. Noise scales approximately as d^-4 at both room temperature and cryogenic temperature, and cryogenic rates are about two orders of magnitude smaller. The noise is close to 1/f at both temperatures — [arXiv:1712.00188](https://arxiv.org/abs/1712.00188)
- Deslauriers et al. 2006 (needle trap, tungsten electrodes): heating scales as d^-3.5(1) — [as summarised in Brownnutt et al. review, arXiv:1409.6572](https://arxiv.org/pdf/1409.6572)
- Brownnutt, Kumph, Rabl, Blatt, "Ion-trap measurements of electric-field noise near surfaces", arXiv:1409.6572 (Rev. Mod. Phys. 87, 1419 (2015); journal reference from my own knowledge, consistent with the task prompt). The review cautions that compiled cross-experiment plots cannot establish a general d^-4 law — [arXiv:1409.6572](https://arxiv.org/pdf/1409.6572)
- A later planar-trap measurement reports a distance-scaling exponent beta ~ 2.6 over ion-surface distances of 50-300 um — [arXiv:1906.06489](https://ar5iv.labs.arxiv.org/html/1906.06489)
- A second Sedlacek 2018 paper (PRA 98, 063430) found the d-scaling unchanged by ion milling, while the temperature dependence changed from power-law to Arrhenius — [NIST/PRA 98, 063430](https://link.aps.org/accepted/10.1103/PhysRevA.98.063430)
- Todaro 2021 (9Be+, trap at ~3.5 K, ion 39 um above electrodes, 29 um over the recessed SNSPD): axial heating 63(6) quanta/s at 2 MHz in zone B (frequency scaling omega^-1.7(7)), and 113(14) quanta/s at 5.3 MHz over the SNSPD. Stray-light-induced SNSPD clicks added 0.009(5) quanta per count — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)
- Chiaverini 2005 Sec. 7: Johnson noise gives d^-3 (d >> skin depth) or d^-2. Patch potentials smaller than d give d^-4 — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- dc-tunable-height surface trap: ion lifetimes fall from several hours at 110 um height to several minutes at 50 um at the same secular frequencies, attributed partly to reduced harmonicity/depth at low height — [arXiv:1807.06043](https://arxiv.org/pdf/1807.06043)

### Inferences
- For mass scaling, heating rate n_dot = q^2 S_E / (4 m hbar omega). A 138Ba+ ion sees ~15x lower n_dot than 9Be+ at the same S_E and omega. Combined with d^-4 from 39 to 50 um (factor ~0.37), a Todaro-like cryogenic surface would give ~a few quanta/s for Ba+ at ~2 MHz axial at 50 um. This is an order-of-magnitude extrapolation, not a measurement.
- At d^-4, going from 50 um to 70 um cuts noise ~3.8x but costs ~2x in depth at fixed V and Omega (depth ~ 1/h^2). 50 um is a reasonable compromise for cryogenic operation.
- Over an integrated SNSPD (dielectric or recessed nanowire), expect locally higher heating (Todaro saw ~2x at a higher frequency and lower height), plus RF pickup on the detector.

### Gaps
- Absolute S_E values or heating rates for Ba+ in cryogenic surface traps at ~50 um were not found in the sources retrieved (the MIT LL Nb trap Ba+ heating rate was not reported in Shi 2023).
- Turchette 2000 was not retrieved directly.

## 4. Ba+ surface-trap operating parameters, wavelengths and loading method

### Takeaway
The closest direct precedent is the MIT/MIT-LL cryogenic Nb-on-sapphire surface trap with 138Ba+ at h = 50 um, f_RF = 41.1 MHz, radial 1.9-3.3 MHz and axial 0.5-0.6 MHz, loaded by ablation plus 554/405 nm photoionization. The UW (Blinov) Sandia Y-trap ran Ba+ at 24.9 MHz, ~96-100 V, with secular frequencies 0.75/1.5/2.1 MHz and ~44 meV depth. Ba+ uses 493 nm cooling/detection, 650 nm repump and 614 nm deshelving; photoionization uses 791 + 337/450 nm or 553/554 + <418 nm (e.g. 405 nm).

### Cited Findings
- Shi, Todaro, Mintzer, Bruzewicz, Chiaverini, Chuang, "Ablation loading of barium ions into a surface-electrode trap", Appl. Phys. Lett. 122, 264002 (2023), DOI 10.1063/5.0149778.
  - Microfabricated sputtered-Nb-on-sapphire trap (cryogenic): ion height 50 um, f_RF = 41.1 MHz, Ba+ radial 1.9-3.3 MHz, axial 500-600 kHz.
  - PCB trap ("Bastille"): 730 um height, 7.1 MHz drive, radial 165-295 kHz, axial ~100 kHz.
  - Photoionization of ablated Ba used 554 nm + 405 nm. Detection is at 493 nm (Ba+) and 422 nm (Sr+).
  - Cooling, repump and detection beams were overlapped at 45 degrees to the trap axis.

  — [Shi et al. 2023, OSTI](https://www.osti.gov/pages/servlets/purl/2425574)
- Shi 2023: ablation used 1064 nm, 5-7 ns pulses, 100 um waist, 1 J/cm^2, from a Ba-metal target 11.4 mm from trap centre. Higher fluence raises per-pulse loading but also contamination with particles that scatter beams or charge up, so they used low fluence at 10-15 Hz.
  - Loading probability turns on above a threshold RF depth and drops at high depth in the 50 um trap because micromotion shrinks the stable volume.
  - Their model gives an optimal RF trap depth of roughly ~0.1 eV for ablated Ba (Eq. 3 and Fig. 3; the extracted numerals were partly garbled).
  - Loading rate in the 50 um trap was lower than in the 730 um trap (stable trapping volume ~150x smaller), and they suggest a high-volume loading zone plus a transition region.

  — [Shi et al. 2023](https://doi.org/10.1063/5.0149778)
- Shi 2023: Ba+ D5/2 lifetime is more than 30 s. Non-radioactive Ba is usually loaded from an oven, but ovens produce excess flux that coats the apparatus, and ablation deposits less excess material — [Shi et al. 2023](https://doi.org/10.1063/5.0149778)
- Graham, Chen, Sakrejda, Wright, Zhou, Blinov, "A system for trapping barium ions in a microfabricated surface trap", AIP Advances 4, 057124 (2014), DOI 10.1063/1.4879817.
  - Trap and drive: Sandia "Y" junction surface trap, 24.9 MHz resonator (30 pF load, Q ~ 200), ~100 V (96 V from secular-frequency fit) at ~120 mW.
  - Measured: secular frequencies 0.75, 1.5 and 2.1 MHz; depth ~44 meV at the loading region; dark lifetime 20 +/- 4.9 s over the loading slot and 31.6 +/- 3.4 s mid-arm.
  - Lasers: cooling 493 nm (doubled 986), repump 650 nm, deshelve 614 nm (doubled 1228). Photoionization used 791 nm + 450 nm (avoiding far UV); the traditional route is 791 + 337 nm (N2 laser or flash lamp), and a 553 nm + <418 nm route is also mentioned.

  — [Graham et al. 2014](https://pubs.aip.org/aip/adv/article/4/5/057124/20382/A-system-for-trapping-barium-ions-in-a)
- Sandia Phoenix/Peregrine traps (HOA bowtie platform; Phoenix has a through-substrate slot for perpendicular beams, NA 0.25; six-rail design with segmented inner and outer DC) are used in Ba-133 work reported at DAMOP 2023 — [Revelle, arXiv:2009.02398](https://arxiv.org/abs/2009.02398); [DAMOP 2023 abstract](https://meetings-archive.aps.org/damop/2023/v01/79)

### Inferences
- For our 50 um Ba+ design, operating near the MIT-LL point (~40 MHz) is well precedented. The higher V in Q1's starting point (~150 V) would raise radial frequencies to ~5 MHz and depth to ~0.2 eV (gapless). That is useful for oven loading (thermal Ba), but keep it within the Shi optimum (~0.1 eV RF depth) if ablation-loading, or plan a separate loading-optimised RF/DC setting.
- Because 493/650 nm are visible and less charging-prone than UV, the only short-wavelength beam is photoionization (337/405/450 nm). Keep the PI beam confined to the loading zone and away from the SNSPD region (stray light caused SNSPD clicks and heating in Todaro).

### Gaps
- No Ba+-specific RF amplitude was given in Shi 2023 for the 50 um trap. Quantinuum, IonQ and Duke Ba+ surface-trap operating parameters were not found in open sources during this search.

## 5. Loading-zone separation from sensitive features (detector, readout zone)

### Takeaway
The NIST trap-integrated SNSPD work loaded 264 um from the SNSPD centre and shuttled to the detector. GTRI and Sandia traps use backside loading slots, and UW added an oven shutter because oxidised Ba and clusters can clog loading apertures. For a 1 cm chip, a loading zone a few hundred um to ~1 mm from the readout zone, with the atomic beam entering from the backside through a slot, is well within precedent.

### Cited Findings
- Todaro 2021: ion loading occurs in zone A, 264 um from the SNSPD centre. The ion is transported to the detector (zone D) using the segmented outer electrodes. Neutral Be atoms come from a thermal flux, photoionised at 235 nm. The trap operates at ~3.5 K with RF 8.8 V peak at 67.03 MHz (9Be+, ~2 MHz axial, 5-10 MHz radial) — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)
- Todaro 2021: the SNSPD Tc should be at least ~25% above the trap surface temperature (typically 4 K). Parasitic RF coupling to the SNSPD output was several times the pulse amplitude and needed a 67 MHz notch (40 dB) plus a 25 MHz low-pass filter — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)
- Doret 2012: "a localized substrate aperture" allows deterministic loading from an oven via species-selective photoionization — [arXiv:1204.4147](https://arxiv.org/abs/1204.4147)
- Graham 2014: a bimetal shutter blocks the Ba oven during bake-out and initial operation to protect the chip from excess flux and indium, since oxidised barium and clusters can block the chip's loading apertures. Ion lifetime was lower over the loading region than mid-arm (20 s vs 31.6 s) — [Graham et al. 2014](https://pubs.aip.org/aip/adv/article/4/5/057124/20382/A-system-for-trapping-barium-ions-in-a)
- Shi 2023: ablation target 11.4 mm from trap centre. Higher fluence increases contamination by particles that scatter beams or charge up. They recommend a high-volume loading zone plus a transition region for small traps — [Shi et al. 2023](https://doi.org/10.1063/5.0149778)
- Chiaverini 2005 Sec. 5: proposes integrating a larger load/reservoir trap and shuttling ions into the surface trap — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)

### Inferences
- **Backside loading slot.** Put a slot under the loading zone and a mechanical shield or collimator below the chip so that no line of sight exists from the oven to the SNSPD/readout zone. Place the loading zone >= ~300 um along the axis from the readout zone (Todaro precedent); ~0.5-1 mm is cheap on a 1 cm chip.
- **Slot as an electrode feature.** The slot is a large exposed-dielectric/aperture feature that perturbs the RF null. Leave a few ion heights (>= ~3h = 150 um) of normal electrode structure between the slot edge and the readout zone. This is my estimate, by analogy with the gapless-model condition that features be << d or far away.
- **Surface loading alternative.** If surface loading (oven beam grazing the chip) is used instead, Ba coats electrodes downstream, so the beam direction should point away from the readout zone.

### Gaps
- No quantitative study of Ba deposition footprint vs distance on a chip was found. The numeric separations above beyond Todaro's 264 um are my recommendations.

## 6. Gap aspect ratio and dielectric shielding

### Takeaway
To hide exposed dielectric from the ion, make the gap depth (electrode height and/or trench) at least equal to, and preferably a few times, the gap width (aspect ratio >= 1). Typical gaps are 2-10 um, with 5 um common.

### Cited Findings
- Bautista-Salvador et al., "Multilayer ion trap technology for scalable quantum computing and quantum simulation", New J. Phys. 21, 043011 (2019), arXiv:1812.01829.
  - On top-level electrode gaps: interspacings should have a height at least equal to their width, "electrode gaps of an aspect ratio higher than 1" (citing their Ref. 18).
  - They demonstrate gaps as narrow as 2 um and a 14:1 aspect-ratio gold gap.
  - Their trap's upper metal level has ~5 um gaps, with a 9Be+ ion at 35 um.

  — [arXiv:1812.01829](https://arxiv.org/abs/1812.01829)
- Chiaverini 2005 Sec. 6: trenches undercutting the metal with depth more than a few times the gap width suppress charged-insulator effects. Electroplating electrodes to a height more than a few times the gap is an alternative — [arXiv:quant-ph/0501147](https://arxiv.org/abs/quant-ph/0501147)
- Wesenberg 2008 Sec. II A: surface-electrode traps use small gaps because exposed substrate picks up static charge, and the gapless model needs gaps << d — [arXiv:0808.1623](https://arxiv.org/abs/0808.1623)
- Sterling 2013: wide electrode spacing for high voltage creates exposed dielectric, so electrodes are normally separated by several-um gaps — [Sterling et al. 2013](https://www.sussex.ac.uk/physics/iqt/APPLAB_103_14_143504_1.pdf)

### Inferences
- **Gap and plating.** For h = 50 um use 4-5 um gaps with >= 5-10 um electroplated Au, or a 5 um gap with an undercut trench of >= 10 um (aspect ratio >= 2). Gap/h ~ 0.1 keeps the field within a few percent of the gapless model.
- **SNSPD shielding.** For an integrated SNSPD, the detector itself is exposed dielectric or superconductor under the ion. Todaro recessed it 6 um below the electrode plane, and the ion height dropped from 39 to 29 um over it by design. Budget for local RF-null and stray-field perturbation over the detector and compensate with local DC segments.

### Gaps
- Bautista-Salvador's Ref. 18 was not identified. No quantitative curve of stray-field vs aspect ratio was retrieved.

## 7. Beam clipping, chip geometry and wirebonds

### Takeaway
At 50 um height, a beam that skims the full 1 cm chip cannot be kept much smaller than the ion height. A Gaussian at 493 nm optimised over a +/-5 mm path has w ~ 40 um at the chip edges (~0.8h), so it scatters strongly. Reducing the over-chip path to ~+/-1 mm (notched or bowtie chip, or zones near an edge) allows w0 ~ 12-15 um with w <= 20 um everywhere (h/w >= 2.5). Precedent beam geometry is diagonal, at 45 degrees to the trap axis.

### Cited Findings
- Graham 2014: beams travel ~1 cm close to the chip surface. UV-induced surface charging motivates well-focused, low-divergence beams at the longest practical wavelengths, and low background needs "tight focusing of beams and precise leveling" relative to the chip surface. Beam 1/e^2 radii at the ion were 61 um (493), 80 um (650), 76 um (614), 55 um (450) and 97 um (791), with lasers "just 70 um above the whole surface of the chip". A wire-mesh ground shield sat over the carrier — [Graham et al. 2014](https://pubs.aip.org/aip/adv/article/4/5/057124/20382/A-system-for-trapping-barium-ions-in-a)
- Shi 2023: cooling, repump and detection beams overlap at the ion at 45 degrees to the trap axis. The ablation beam is tilted in the y-z plane to avoid scattering off the trap surface — [Shi et al. 2023](https://doi.org/10.1063/5.0149778)
- Todaro 2021: the magnetic field is in-plane at 45 degrees to the trap axis. Ion height is calibrated by scanning the beam toward the surface and fitting scatter (~1 um uncertainty) — [arXiv:2008.00065](https://arxiv.org/abs/2008.00065)
- Sandia HOA/Phoenix: "bowtie-shaped" chip platform (narrow central region for beam access), and Phoenix adds a through-substrate slot for beams perpendicular to the surface — [arXiv:2009.02398](https://arxiv.org/abs/2009.02398)

### Inferences
- **Gaussian-beam budget (computed).** For a beam parallel to the surface at height h, the smallest worst-case radius over a path +/-z is achieved with w0 = sqrt(lambda*z/pi), giving w(z) = sqrt(2)*w0.

  | Wavelength | Path +/-5 mm: w0 / w_edge | Path +/-1 mm: w0 / w_edge |
  |---|---|---|
  | 493 nm | 28 / 40 um | 12.5 / 18 um |
  | 650 nm | 32 / 46 um | 14.4 / 20 um |
  | 405 nm | 25 / 36 um | 11 / 16 um |

  - Over +/-5 mm at 493 nm, w_edge/h = 0.8 and the surface (h = 50 um) sits at ~4% of peak intensity, so scatter is strong. Over +/-1 mm the surface is at exp(-2(h/w)^2) ~ 1e-7 of peak.
  - So on a 1 cm x 1 cm chip either place the zones within ~1 mm of a chip edge along the beam path, or notch or bowtie the chip so the beam crosses <= ~2 mm of chip.
  - A 45-degree beam crossing a square chip's centre traverses ~14 mm, which is impractical at 50 um height without notching.
- **Wirebonds.** Wirebond loops typically rise ~100-300 um, which is not sourced here. Keep pads on the two chip edges parallel to the beam direction (not on the beam entry/exit edges), at least several mm from the beam line, or use a bowtie with pads only on the wide ends.
- **Mesh shield.** A mesh ground shield over the carrier (Graham) must leave a clear aperture along the beam path.

### Gaps
- No source found for the exact width of Todaro's or the Sandia isthmus ("1.8 mm" in the prompt is unverified). Sandia HOA bowtie dimensions were not retrieved. Typical wirebond loop heights are not sourced.

## 8. RF voltage limits and breakdown across 5-10 um gaps

### Takeaway
Surface flashover sets the RF ceiling. Sterling 2013's fit is V_b = sqrt(u*e*d/eps0). With u = 4.6e18 eV/m^2 (Au on quartz, RF) this gives ~645 V at 5 um and ~910 V at 10 um. PECVD SiO2 on Si is ~30% worse than quartz (u = 1.4e18 eV/m^2), while a SiN surface layer is ~3.6x better than SiO2. RF and DC flashover are statistically indistinguishable. For a 50 um Ba+ trap needing ~100-200 V, 5 um gaps on quartz or sapphire have ~3x margin, but SiO2-over-silicon multilayers have less (~360 V at 5 um).

### Cited Findings
- Sterling, Hughes, Mellor, Hensinger, "Increased surface flashover voltage in microfabricated devices", Appl. Phys. Lett. 103, 143504 (2013), DOI 10.1063/1.4824012.
  - Setup: Au electrodes (500 nm, Cr seed) on quartz, gaps 3-15 um in 2 um steps, ~5e-4 Pa, RF at 22.0 MHz.
  - Eq. (1) SEEA model fit: u_rf ~ 4.6e18 eV m^-2 and u_dc ~ 4.9e18 eV m^-2 (~5% difference, not significant; Fig. 2).
  - Damage modes: RF flashover erodes the closest electrode edges along the full length; DC flashover destroys large electrode areas (Fig. 1).

  — [Sterling et al. 2013](https://www.sussex.ac.uk/physics/iqt/APPLAB_103_14_143504_1.pdf)
- Sterling 2013, Fig. 3:
  - Layered PECVD aSiO/aSiN surface on quartz: flashover similar to quartz within error.
  - aSiO on a silicon substrate: ~30% lower (u ~ 1.4e18 eV m^-2), attributed to field concentration from the conductive substrate.
  - 80 nm aSiN surface layer: u ~ 18.1e18 eV m^-2 (~3.6x aSiO); up to 29.9e18 eV m^-2 on 0.5 um aSiN on quartz, with large spread.
  - LPCVD SiO2 with an O2 plasma clean from prior work: u ~ 16e18 eV m^-2, suggesting surface cleaning matters.

  — [Sterling et al. 2013](https://www.sussex.ac.uk/physics/iqt/APPLAB_103_14_143504_1.pdf)
- Sandia: RF breakdown is a major limit on the maximum RF voltage of microfabricated surface traps, and slow voltage ramping on new traps is used to detect breakdown — [DAMOP 2022 abstract](https://meetings-archive.aps.org/damop/2022/m09/5)
- Shi 2023 notes RF breakdown in microfabricated traps can limit achievable depth — [Shi et al. 2023](https://doi.org/10.1063/5.0149778)

### Inferences
- **Computed from Sterling Eq. (1)** (units check: u*e in J/m^2, times d/eps0 gives V^2). Whether these are peak or rms for RF is not stated in the extracted text; treat them as amplitude magnitudes.

  | Surface | 3 um | 5 um | 7 um | 10 um | 15 um |
  |---|---|---|---|---|---|
  | Au on quartz | 500 V | 645 V | 763 V | 912 V | 1117 V |
  | SiO2 on Si | 276 V | 356 V | 421 V | 503 V | — |
  | SiN-surface on Si | 991 V | 1280 V | 1514 V | 1810 V | — |

- **Derating.** Derate to <= ~50% of V_b for long-term operation (my engineering margin, not sourced). With 5 um gaps on sapphire or quartz the safe ceiling is ~300 V, comfortably above the ~100-200 V needed for Q1's design point.
- **Buried layers.** If the SNSPD process puts SiO2 over a conducting layer or Si near the RF rails, the margin falls to ~180 V. Use SiN as the top dielectric or widen the RF-to-ground gaps near buried conductors.
- **Bias-line spacing.** RF pickup on SNSPD bias lines (Todaro) argues for keeping SNSPD leads away from RF rails as well, independent of breakdown.

### Gaps
- Stick et al. 2010 (Sandia) breakdown data across ~10 um SiO2 (bulk breakdown between levels) was not retrieved, so no number for vertical breakdown through inter-level dielectric. Cryogenic flashover data were not found.
