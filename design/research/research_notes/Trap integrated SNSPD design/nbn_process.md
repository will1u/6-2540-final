# NbN SNSPD Fabrication (MIT Berggren-group style) and Compatibility with an Al-Ground-Plane Surface Ion-Trap Flow

Scope note: the primary MIT papers (Toomey 2018, Medeiros 2019, Najafi 2015) and the NIST trap-integrated SNSPD paper (Hampel 2023) were read in full or at the methods level. The Dane 2017 APL full text could NOT be retrieved (MIT DSpace returned HTTP 429 rate limiting on every attempt), so the exact Dane sputter recipe numbers (Ar/N2 flows, DC power/current, pressure) are listed as gaps. Everything marked "Inference" is my reasoning, not a sourced number.

## Q1. NbN deposition: Dane et al. 2017 room-temperature bias sputtering

### Takeaway
Dane et al. 2017 is verified as Appl. Phys. Lett. 111, 122601 (2017), DOI 10.1063/1.4990066 (no arXiv version found). The key process idea is reactive DC magnetron sputtering of NbN onto an unheated SiO2/Si substrate while applying a 50 W RF bias to the substrate holder, which raised Tc of unheated films by up to 73% (to ~7.8 K) and smoothed the films enough to make unconstricted nanowires. The MIT group later used this exact recipe (AJA Orion system) as their standard SNSPD film, with ~5 nm films giving Rs ~600 ohm/sq and Tc ~7.9 K.

### Cited Findings
- Citation: A. E. Dane, A. N. McCaughan, et al., "Bias sputtered NbN and superconducting nanowire devices," Appl. Phys. Lett. 111, 122601 (2017), DOI 10.1063/1.4990066; open-access copy on MIT DSpace handle 1721.1/126227. No arXiv listing was found. — [MIT DSpace record](https://dspace.mit.edu/handle/1721.1/126227); [DSpace PDF](https://dspace.mit.edu/bitstream/1721.1/126227/1/1.4990066.pdf)
- "By adding a 50 W RF bias to the substrate holder during sputtering, the Tc of the unheated NbN films was increased by up to 73%, and the roughness was substantially reduced." — [MIT DSpace abstract (via search result)](https://dspace.mit.edu/handle/1721.1/126227)
- Devices measured at 2.5 K with 1550 nm light; count rate saturated near the critical current (near-unity internal efficiency); single-ended timing jitter 38 ps. The same material was used for nanocryotrons and a large-area imager. — [MIT DSpace abstract](https://dspace.mit.edu/handle/1721.1/126227)
- AIP Scilight summary: biased films reached Tc = 7.8 K (73% higher than unbiased); deposition on unheated silicon dioxide; 10 deposition conditions explored; unbiased films were "too rough for fabricating unconstricted nanowires"; 5-nm-thick films were made for comparison. (The Scilight also says thicknesses "ranged from 46 nm to 23 nm", which looks garbled; treat as uncertain.) — [AIP Scilight](https://www.aip.org/scilights/new-method-for-making-superconducting-nbn-nanowires-could-make-single-photons-easy-prey)
- Substrate/system as used downstream in the group: NbN "bias sputtered at room temperature on a 4 in. Si wafer in an AJA sputtering system following the procedure described in [Dane 2017]"; ~20 nm film had Rs ~90 ohm/sq and Tc = 8.1 K; ~5 nm film had Rs = 600 ohm/sq; resistivity rho ~2.5 kOhm*nm (= 250 uOhm*cm) from XRR of a sister film, "consistent with the results for an ~5 nm film reported in prior work." — [Toomey et al., JVST B 36, 06JC01 (2018)](https://qnn-rle.mit.edu/wp-content/uploads/2018/10/1.5047427-1.pdf)
- Untreated ~5 nm (4.7 nm inferred) film Tc ~7.9 K (Fig. 4b starting point at 1 min TMAH ~7.9 K). — [Toomey 2018](https://doi.org/10.1116/1.5047427)
- Medeiros 2019 used the Dane conditions on 220 nm thermal SiO2 on Si(100), 1 cm x 1 cm pieces from 4 in wafers, room-temperature DC reactive magnetron sputtering in an AJA International Orion system, recipe automated in AJA Phase IIJ software; deposition time 20-200 s in 20 s steps plus 400 s and 600 s to produce 1-30 nm. Data: 200 s -> ~8 nm (stated "a 200 s deposition (8 nm)"), 400 s -> ~16 nm, 600 s -> ~24 nm, i.e. ~0.04 nm/s. — [Medeiros et al., arXiv:1812.05559v3](https://arxiv.org/pdf/1812.05559)
- Resistivity of these films from ellipsometry vs sheet-conductance fit: 245 uOhm*cm (linear fit, adj. R^2 = 0.9991), with a 0.88 nm intercept indicating resistivity increases at small thickness (inset shows rho rising steeply below ~3 nm). — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- Dane's S.M. thesis: "Reactive DC magnetron sputtering of ultrathin superconducting niobium nitride films," MIT EECS S.M. 2015, advisor K. K. Berggren, 101 pp.; per abstract, film Tc was improved "by changing the way the samples were heated during the deposition, by ex situ rapid thermal processing, and in some cases by the addition of an RF bias to the substrate holder." — [DSpace 1721.1/97257](https://dspace.mit.edu/handle/1721.1/97257)
- Contrast (heated deposition, older MIT process): Najafi 2015 used 4 nm NbN reactively sputtered onto PECVD SiNx at an 800 C substrate-holder temperature, Rs = 515 ohm/sq, Tc = 10.9 K. — [Najafi et al., Nat. Commun. 6, 5873 (2015), PMC4354051](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)

### Inferences
- For an Al-ground-plane trap wafer, the room-temperature bias-sputter recipe is the only option of the two MIT recipes that is compatible: 800 C heated deposition (Najafi) is far above Al's melting point (660 C) and hillock range, while the Dane process is unheated. Cost: Tc ~7.8-7.9 K instead of ~10.9 K, so detectors need operation well below ~4 K for good switching current margin (the group measures at 2.5 K).
- Process target for SNSPDs: ~5 nm (deposition ~120-130 s at the Medeiros rate), Rs ~550-650 ohm/sq at room temperature, Tc ~7.5-8 K. Use Rs from a 4-point probe on a witness piece as the first, fastest go/no-go check.
- RF substrate bias causes ion bombardment of the growing film; on a patterned trap wafer the substrate holder bias will couple through the dielectric to buried Al. Whether this matters (charging, arcing at Al features) was not addressed in any source.

### Gaps
- Exact Dane recipe numbers (Nb target size/purity, Ar and N2 sccm, chamber pressure, DC current/power, DC self-bias voltage, base pressure), the Tc-vs-thickness table and RMS roughness values could not be extracted because the DSpace PDF was rate-limited (HTTP 429) during this session. Retrieve directly from APL 111, 122601 or DSpace 1721.1/126227 / thesis 1721.1/97257.
- Whether the Dane paper used sapphire as well as SiO2/Si was not confirmed (sources found only mention SiO2).
- I did not verify whether the specific AJA Orion tool used by the group is in MIT.nano or in the QNN lab (RLE); a student should confirm tool access and whether a substrate RF bias option exists on the MIT.nano sputter tools.

## Q2. Thickness metrology and oxidation tracking (Medeiros et al. 2019)

### Takeaway
A fixed-angle, four-wavelength ellipsometer (Film Sense FS-1) with a multi-sample-derived NbN n,k model measures 1-30 nm NbN on thermal SiO2 in <30 s per sample and agrees with XRR to within 0.5 nm above ~4 nm thickness. Adding an Nb2O5 layer to the model tracks oxidation: NbN thickness dropped 8.7% over 100 days in air, with oxide following d_ox = 0.78 t^0.17 (nm, t in days).

### Cited Findings
- O. Medeiros, M. Colangelo, I. Charaev, K. K. Berggren, "Measuring thickness in thin NbN films for superconducting devices," arXiv:1812.05559 (v3 dated 23 Apr 2019). — [arXiv](https://arxiv.org/abs/1812.05559v1); [QNN news](https://qnn-rle.mit.edu/new-publication-measuring-thickness-in-thin-nbn-films-for-superconducting-devices)
- Tool: Film Sense FS-1 multi-wavelength (466, 522, 598, 638 nm), fixed angle; alignment within +/-0.01 deg, 1 s acquisition (longer did not improve accuracy); alignment + measurement < 30 s per sample. Model: NbN (n,k) on thermal SiO2 on Si; fitted with OpenFilters, Marquardt-Levenberg. — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- Multi-sample analysis: samples with identical optical properties and varying thickness are fit jointly; SiO2 fit as a single shared thickness; no oxide layer during multi-sample analysis. Fit MSE 0.055 (thinnest) to 0.0156 (thickest). — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- NbN optical constants (Table I): 466 nm n=2.456, k=2.487; 522 nm n=2.554, k=2.536; 598 nm n=2.643, k=3.047; 638 nm n=2.822, k=3.197 (specific to these deposition conditions). — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- Validation: XRR (Rigaku SmartLab, Cu 0.1541 nm, >40 min per sample) and 4-point probe. Above 100 s deposition, ellipsometer thickness within 0.5 nm of XRR; XRR deviated for thinner films (no interference fringes). — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- Oxidation: an 8 nm (200 s) film, transported in a reduced-atmosphere (~0.5 atm) box to minimize initial exposure, measured at increasing intervals while stored in air. After 100 days NbN thickness decreased by 8.7%; Nb2O5 thickness fit d_ox = 0.78 t^0.17 (sum sq. error 0.04), consistent with Deal-Grove-like diffusion-limited growth. Oxidation product assumed Nb2O5 (citing Gallagher et al.). — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- Rationale given in paper: Lk proportional to 1/d, so thickness is critical; resistance-based thickness is unreliable because it depends on deposition conditions and changes over time with oxide growth. — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)

### Inferences
- Process check usage: (1) after deposition, measure a witness chip on thermal SiO2 (same SiO2 thickness each run) and record thickness + Rs; (2) re-measure before EBL if the wafer waited >1 day, since d_ox = 0.78 t^0.17 gives ~0.78 nm oxide after 1 day and ~1.15 nm after 10 days, which is a large fraction of a 5 nm film; (3) use as a post-develop check for TMAH thinning (see Q4).
- On the trap wafer, NbN will sit on PECVD SiO2 over Al, not on thermal SiO2 over Si. The ellipsometer model must include the Al mirror and the actual SiO2 thickness, or measure a co-deposited witness on thermal SiO2/Si. The witness approach is simpler and is what the paper validated.

### Gaps
- Final journal citation (volume/page/DOI) for Medeiros 2019 was not verified in this session; the arXiv v3 PDF does not show it. Mark as "arXiv:1812.05559; journal version unverified."
- Whether MIT.nano has a Film Sense FS-1 (vs. a Woollam VASE) was not checked; a VASE can do the same multi-sample analysis but the paper's n,k values are tool-independent only for the same film recipe.

## Q3. Nanowire patterning (EBL), etch and contacts: Najafi et al. 2015 flow

### Takeaway
The verified Najafi 2015 paper is "On-chip detection of non-classical light by scalable integration of single-photon detectors," Nat. Commun. 6, 5873 (2015), DOI 10.1038/ncomms6873. Its flow: 70 nm HSQ, Raith 150 at 30 keV, 700-850 uC/cm^2, TMAH development 3 min at 27 C, CF4 RIE 2.5 min at 50 W, then Ti/Au (10/15 nm) contact pads by PMGI/S1813 bilayer liftoff. 82 nm wires, ~30% of 225 detectors were high performance; jitter 39-65 ps. The "80 nm, ~70% yield, 24 ps jitter" paper the assignment describes was not identified.

### Cited Findings
- Citation and authors: F. Najafi, J. Mower, N. C. Harris, F. Bellei, A. Dane, C. Lee, X. Hu, P. Kharel, F. Marsili, S. Assefa, K. K. Berggren, D. Englund, Nat. Commun. 6, 5873 (2015), DOI 10.1038/ncomms6873. — [PMC4354051](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)
- Film: 4 nm NbN on 200-300 nm PECVD SiNx on double-polished Si, 800 C holder, 515 ohm/sq, Tc 10.9 K. — [Najafi 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)
- EBL: HSQ 70 nm thick; Raith 150 at 30 keV; dose 700-850 uC/cm^2; dummy features exposed outside the hairpin detector for proximity/dose uniformity. Wire width 82 nm (Fig. 2a). — [Najafi 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)
- Develop: TMAH, 27 C, 3 min (concentration not stated in methods). — [Najafi 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)
- Etch: CF4 RIE, 2.5 min at 50 W. — [Najafi 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)
- Contacts: 700 nm PMGI under 1.5 um S1813, UV 13 s at 2,300 uW/cm^2, develop 24 s CD-26; evaporate Ti 10 nm / Au 15 nm; liftoff in acetone with 2 min sonication. — [Najafi 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)
- Yield/performance: 225 detectors fabricated, ~30% typically high-performance and selected for transfer; 10 detectors integrated on one circuit with 100% device yield (post-selection); Ic 15.2, 16.8, 16.4, 14.8 uA after undercut/transfer (~20% lower than before); jitter 42-65 ps (A/B channels), 39-57 ps for the ten-detector array; on-chip detection efficiency up to 52+/-6% at 1550 nm. — [Najafi 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051); [search summary of paper](https://www.rle.mit.edu/on-chip-detection-of-non-classical-light-by-scalable-integration-of-single-photon-detectors-nature-communications/)
- Group's standard CF4 etch used later (Toomey 2018): Plasma-Therm RIE, CF4, RF 50 W, 10 mTorr, 2.5 min (a ~20 nm film needed ~3.5+ min; a ~20 nm HSQ-patterned film took nearly twice as long as an unpatterned control because of TMAH residue, eroding the HSQ mask). — [Toomey 2018](https://doi.org/10.1116/1.5047427)
- HSQ is typically left on the nanowires after etch; a Cornell MBE-NbN SNSPD paper keeps HSQ on the wires as an oxidation barrier and uses CF4 at 50 W RF. — [Cheng et al. 2020 (search result)](https://djena.engineering.cornell.edu/papers-new/2020/cheng2020epitaxial.pdf)
- NIST trap-integrated alternative: NbTiN patterned "by optical and electron-beam lithography combined with reactive-ion etching with sulfur hexafluoride (SF6)"; 90 nm wire, 180 nm pitch, 20 um x 30 um active area. — [Hampel et al., arXiv:2302.01462](https://arxiv.org/pdf/2302.01462)

### Inferences
- Suggested MIT.nano-adapted flow (student version; parameters to be re-calibrated on the local EBL tool, which is likely a higher-voltage system than the 30 keV Raith 150, so dose will be several times higher): (1) NbN ~5 nm by bias sputtering; (2) ellipsometry + Rs check; (3) Ti/Au or Nb/Au alignment marks and contact pads first, by liftoff (pads-first avoids exposing finished wires to liftoff sonication); (4) HSQ ~50-70 nm spin, bake per manufacturer; (5) EBL meander with dummy fill around the meander edges; (6) develop (see Q4 for TMAH mitigation: salty developer or dilute TMAH plus a 3 min running DI rinse); (7) CF4 RIE 50 W, 10 mTorr, time from witness etch plus over-etch, verified by open-circuit test on a test structure; (8) leave HSQ on as the first passivation; (9) PECVD SiO2 cap.
- Ordering pads before nanowire EBL also lets the NbN-to-pad contact be made by HSQ overlapping onto the pad region; if pads go last, an Ar pre-clean of the NbN contact area is usually needed to remove Nb2O5 for ohmic contact (not sourced here; standard practice).

### Gaps
- The paper described in the assignment ("80 nm wires, ~70% yield, 24 ps jitter", Berggren-group optimized fab or "membrane-integrated") was not found in this session. The verified 2015 Najafi paper reports ~30% selection rate and 39-65 ps jitter. Faraz Najafi's PhD thesis (MIT 2015) likely has the fuller recipe but was not retrieved.
- HSQ product/dilution (e.g., XR-1541 2% vs 6%), pre-bake, TMAH concentration (25% vs 2.38%), and meander pitch for Najafi 2015 were not stated in the methods.

## Q4. TMAH damage to NbN (Toomey et al. 2018) and mitigation

### Takeaway
Toomey, Colangelo, Abedzadeh, Berggren, "Influence of tetramethylammonium hydroxide on niobium nitride thin films," J. Vac. Sci. Technol. B 36, 06JC01 (2018), DOI 10.1116/1.5047427 (verified). 25% TMAH reacts with NbN to form a water-soluble TMA-hexaniobate salt that blocks CF4 etching and consumes the film: 60 s of exposure removed ~0.25 nm (5%) and lowered Tc by 0.2 K; 25 h removed ~3 nm (57%) and lowered Tc by ~1.6 K. A vigorous 3 min running DI rinse removes the etch barrier but does not undo the thinning.

### Cited Findings
- Abstract: "25% TMAH developer damages niobium nitride (NbN) thin films by modifying the surface chemistry and creating an etch contaminant that slows reactive ion etching in CF4"; "processes using 25% TMAH as an adhesion promoter are not preferred for NbN films." — [Toomey 2018 PDF](https://qnn-rle.mit.edu/wp-content/uploads/2018/10/1.5047427-1.pdf)
- Experiment 1: ~20 nm NbN (90 ohm/sq, Tc 8.1 K); 25% TMAH for 0-90 s; DI rinse either 30 s (standard) or 3 min under running DI; brief IPA rinse; CF4 RIE 2.5 min at 50 W, 10 mTorr in a Plasma-Therm. 30 s-rinsed samples had 7-8 nm more remaining film than the control after etch (etch barrier); 3 min running-rinse samples were within 2 nm of control. Simply soaking in DI for 3-5 min did not help; flowing DI is needed. — [Toomey 2018](https://doi.org/10.1116/1.5047427)
- Experiment 2: 5 nm NbN (600 ohm/sq), 25% TMAH from 1 min to 25 h, then 3 min vigorous DI rinse. 60 s -> 0.25 nm (5%) thinner and Tc down 0.2 K; 25 h -> ~3 nm (~57%) thinner and Tc down ~1.6 K (from ~7.9 K to ~6.6 K in Fig. 4b). No saturation, so the reaction consumes the whole film, not just the 1-2 nm native oxide. — [Toomey 2018](https://doi.org/10.1116/1.5047427)
- Mechanism: ATR-FTIR peaks at 838, 692, 650 cm^-1 match TMA-hexaniobate [(CH3)4N]5[H3Nb6O19]*20H2O; water-soluble, forms clusters, likely forms a fluorocarbon-polymer etch stop in CF4 and consumes reactive F. — [Toomey 2018](https://doi.org/10.1116/1.5047427)
- Damage to sidewalls: HSQ protects the top during development but the sides of the pattern remain vulnerable. Prior literature: a 4 min 25% TMAH pretreatment (adhesion promoter) increased Rs and decreased Tc. — [Toomey 2018](https://doi.org/10.1116/1.5047427)
- Suggested mitigations (proposed, not tested in the paper): evaluate dilute TMAH developers (e.g., MF CD-26); salty developer (NaOH/NaCl) for HSQ, "but their influence on superconducting films has not yet been reported"; Ar ion milling or Cl2 RIE instead of CF4 to avoid needing the 3 min rinse; a protective layer between NbN and HSQ. — [Toomey 2018](https://doi.org/10.1116/1.5047427)
- Related: EIPBN 2018 abstract 1C-3 summarizes the same results. — [EIPBN 2018](https://eipbn.org/abstracts/2018/papers/1C-3.pdf)

### Inferences
- For a student flow: do not use a TMAH pre-dip as adhesion promoter; keep develop time as short as the HSQ allows; always finish with >=3 min running DI rinse before IPA; budget ~0.25-0.5 nm thickness loss and ~0.2-0.3 K Tc loss per minute-scale develop. A thin (~2 nm) SiO2 or Si adhesion/protection layer between NbN and HSQ is a plausible fix but is unvalidated here.
- Note that MF CD-26 (2.38% TMAH) is also the standard photoresist developer; any photolithography steps on exposed NbN (e.g., pad liftoff after nanowire patterning) also expose NbN to TMAH. Pads-first ordering or a cap over the wires avoids this.

### Gaps
- No quantitative data found on salty developer (NaOH/NaCl) or dilute 2.38% TMAH effects on NbN.

## Q5. Device-level numbers: switching current, kinetic inductance, reset time, size vs yield

### Takeaway
Representative values: MIT room-temp NbN ~5 nm, Rs ~600 ohm/sq, Tc ~7.9 K; 4 nm/82 nm heated-NbN wires gave Ic ~15-21 uA; NIST 10 nm/90 nm NbTiN gave Isw ~55-60 uA at 4.5 K with 20x30 um area, 1.3 uH, ~25 ns decay. For a ~20x20 um NbN meander of 100 nm wire at 200 nm pitch, estimated Lk ~2 uH and 1/e reset ~40 ns into 50 ohm.

### Cited Findings
- Najafi 2015: 82 nm wide, 4 nm NbN, Ic 14.8-16.8 uA post-transfer (~20% lower than pre-undercut). — [Najafi 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)
- Hampel 2023 (NIST, NbTiN on SiO2 over grounded Al mirror): 10 nm NbTiN, 90 nm width, 180 nm pitch (50% fill), active area 20 um x 30 um; pulse decay time constant ~25 ns, device kinetic inductance 1.3 uH; switching currents ~55-60 uA at 4.5 K with no rf (Fig. 3); operated at 2.6 K base up to 6 K; NbTiN increased critical currents ~10x vs MoSi; max system detection efficiency 68% (395 nm). — [Hampel et al., APL 122, 174001 (2023), arXiv:2302.01462](https://arxiv.org/pdf/2302.01462)
- Resistivity rises steeply below ~3 nm for MIT NbN (Medeiros Fig. 2 inset), and Lk scales as 1/d. — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- Rf heating in trap: with 45 V peak rf applied, SNSPD temperature rises ~0.5 K above steady state; grounded Al mirror reduces rf field at the nanowire by ~10x and makes Isw tolerant to up to 54 V peak at 70 MHz. — [Hampel 2023](https://arxiv.org/pdf/2302.01462)

### Inferences
- Lk per square estimate (BCS dirty limit, Lk,sq = hbar*Rs/(pi*Delta), Delta = 1.76 kB Tc): Rs = 600 ohm/sq, Tc = 7.9 K -> Delta ~1.2 meV -> Lk,sq ~105 pH/sq. (Calculated, not measured in any source here.)
- A 20 um x 20 um meander, 100 nm wire at 200 nm pitch: ~2,000 um of wire = ~20,000 squares -> Lk ~2.1 uH -> L/50 ohm ~42 ns 1/e recovery. A 50 x 50 um detector at the same geometry has ~6x more squares (~13 uH, ~250 ns): slower reset, and more length per device so lower yield from point defects/constrictions. Latching risk rises as L decreases (fast reset); with ~2 uH and 50 ohm load, latching is generally not an issue for NbN, but the margin should be checked if a series inductor is omitted.
- Switching current for 100 nm x 5 nm room-temp bias-sputtered NbN: scaling from Najafi (4 nm, 82 nm, heated, Tc 10.9 K, ~19-21 uA pre-transfer) by width and thickness, and down for lower Tc (~7.9 K), suggests roughly 15-25 uA at ~2.5 K. This is an estimate; the actual Dane 2017 device Ic was not retrieved.
- For ion-trap rf tolerance, Hampel's argument is that higher Isw (NbTiN ~10x MoSi) makes induced rf currents a smaller fraction of bias. Room-temp NbN at ~20 uA would be between MoSi and NbTiN, so a grounded Al mirror below is important.

### Gaps
- Tc on sapphire vs SiO2 for the room-temperature bias-sputter recipe: not found.
- Dane 2017 device switching current, wire width, and meander fill factor: not retrieved.
- Quantitative yield vs detector area data for the MIT process: not found.

## Q6. Thermal/chemical budget for finished NbN nanowires

### Takeaway
Direct, nanowire-specific data are sparse. What is sourced: TMAH (any concentration exposure on bare NbN) thins NbN (Q4); air oxidation consumes ~9% of an 8 nm film in 100 days (Q2); bulk NbN films keep Tc after 500 C anneals in inert conditions but lose Tc when annealed in oxygen unless capped; and NIST built SNSPDs inside a full trap flow with a 130 nm PECVD SiO2 cap and CHF3 RIE patterning, then evaporated Au electrodes, with working devices. No sourced data were found on O2-plasma ashing, BOE/HF, ITO sputtering, or electroplating bath effects on NbN.

### Cited Findings
- NIST trap flow over finished NbTiN nanowires: CHF3 RIE vias through SiO2, 20 nm Au, 350 nm evaporated Au electrode liftoff (in contact with Al mirror through vias), then "a 130 nm-thick SiO2 cap was deposited on top of the SNSPD to protect the nanowire during further processing and limit degradation due to oxidation," by PECVD across the whole wafer, patterned to cover only the SNSPD with CHF3 RIE. Devices worked after this flow. — [Hampel 2023](https://arxiv.org/pdf/2302.01462)
- NIST also simulated, but did not fabricate in this paper, top shielding of 50 nm Au mesh or 50 nm ITO over the SNSPD. — [Hampel 2023](https://arxiv.org/pdf/2302.01462)
- Sputtered NbN on GaN: Tc stable after 500 C anneal; 950 C (30 min) dropped Tc to 8.7 K and RRR from 0.85 to 0.29. — [arXiv:2501.07780](https://arxiv.org/pdf/2501.07780)
- Oxygen annealing of NbN on SiO2: Tc of uncapped NbN decreases as anneal temperature increases; NbN/ScN capped films show insignificant Tc change for anneals below 450 C. — [Ioffe journal paper](https://journals.ioffe.ru/articles/viewPDF/59210)
- NbN oxidizes in air to Nb2O5 (Medeiros, citing Gallagher); oxide growth d_ox = 0.78 t^0.17 nm (t in days). — [Medeiros 2019](https://arxiv.org/pdf/1812.05559)
- Toomey notes that oxidation of NbN surface is involved in TMAH reaction (TMA-hexaniobate is synthesized from Nb2O5 + TMAH), and that Ar ion milling or Cl2 RIE are alternative NbN etches. — [Toomey 2018](https://doi.org/10.1116/1.5047427)

### Inferences
- Likely-safe after encapsulation with HSQ + PECVD SiO2 (>=100 nm): photoresist bakes (<=120 C), solvent strips, Au evaporation/liftoff, CHF3/CF4 RIE of SiO2 away from the wires. PECVD SiO2 at ~300 C in an N2O/SiH4 plasma is likely acceptable because the NIST group did it directly on bare NbTiN; for NbN the first few nm of SiO2 deposit in an oxidizing plasma, so expect a small (~sub-nm) oxidation of the top surface; deposit a thicker HSQ remnant first if possible. Not directly sourced for NbN.
- Risky without data: O2 plasma ashing on bare NbN (oxidizes it; Nb2O5 forms readily), BOE/HF (attacks Nb2O5 and SiO2/HSQ cap; would strip HSQ and then contact NbN; avoid unless the cap is thick and timed), Ar ion milling with line-of-sight onto wires (physically removes nm-scale film), long TMAH or KOH-based developer contact, electroplating baths (alkaline/cyanide Au baths would contact sidewalls if cap has pinholes). Rule: never expose bare nanowires to any of these; do all such steps before NbN or with the SNSPD region capped.
- ITO sputtering on top of the SiO2 cap: sputter damage should be absorbed by the >=100 nm SiO2; ITO anneals at 300-400 C in air are a concern for the Al (Q7) more than the capped NbN.

### Gaps
- No primary data found for NbN nanowire Tc/Isw after O2 plasma, BOE, ITO deposition/anneal, or electroplating. The "Todaro proposal" referenced in the assignment was not located in this session (Todaro et al. 2021 PRL used MoSi SNSPDs; not verified here).
- Exact PECVD temperature in the Hampel flow is not stated in the pages read.

## Q7. Al ground plane thermal limits and SNSPDs above Al mirrors

### Takeaway
Hillocks in sputtered/evaporated Al form during anneals in the ~300-450 C range, with significant hillocking reported at 350 C; caps of Ti, TiW or TiN, Al-Si-Cu alloying, and strong (111) texture suppress them. The NIST trap-integrated SNSPD is a direct precedent for the stack: 50 nm e-beam Al mirror on 150 nm PECVD SiO2, covered by 212 nm PECVD SiO2, then 10 nm NbTiN co-sputtered at 500 C on top, with working detectors.

### Cited Findings
- Hampel 2023 stack: high-resistivity Si (>20 kOhm*cm) / 150 nm PECVD SiO2 / 50 nm e-beam-evaporated Al mirror (liftoff) / 212 nm SiO2 / 10 nm NbTiN co-sputtered at 500 C / nanowire / 130 nm PECVD SiO2 cap. Mirror is grounded through CHF3-etched vias + 20 nm Au + 350 nm Au electrodes. Al chosen over Au for higher UV/blue reflectivity; mirror doubles nanowire absorption with suitable SiO2 thickness (186 nm bottom SiO2 optimum for a standalone variant). Fabricated in NIST Boulder Microfabrication Facility. — [Hampel 2023](https://arxiv.org/pdf/2302.01462)
- Significant temperature-induced voiding and hillocking on Al after annealing at 350 C; sputtered Ti and TiW on top of the Al suppressed hillocks. — [SINTEF publication](https://www.sintef.no/publikasjoner/publikasjon/1155451/)
- TI study of AlSi(1%)Cu(0.5%): uncapped stacks showed hillock formation on heating and hillock/grain collapse on cooling; capped stacks showed reduced or suppressed hillocks. — [MRS Proc., stress phenomena in capped Al metallizations](https://www.cambridge.org/core/journals/mrs-online-proceedings-library-archive/article/stressrelated-phenomena-in-capped-aluminumbased-metallizations/9468E17DBFE8FE6E972A910ACEC2DBD3)
- Patent: AlxTiyNz cap acts as mechanical restraint suppressing hillocks when heated above ~300 C. — [US 6348403](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6348403)
- Strongly (111)-textured Al films resist hillocks/voids at 400 C for 1 h. — [MRS Proc., texture and hillocks](https://core-cms.cambridgecore.org/core/journals/mrs-online-proceedings-library-archive/article/effect-of-texture-on-hillock-formation-in-aluminum-films/2BA3E6F067027A2CB56C1DE13D0B5869)
- Al/TiN interface is metallurgically active, so some interfacial reaction expected. — [US 5747361](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5747361)

### Inferences
- The Hampel precedent shows a 50 nm Al film under ~212 nm PECVD SiO2 survived a 500 C NbTiN deposition well enough for working devices; it does not show hillock-free Al (not reported). The room-temperature NbN recipe (Q1) is far gentler (<~100 C from plasma heating, not sourced), so NbN over SiO2-over-Al is thermally the easy case. The hottest steps in the trap flow are likely PECVD SiO2 (~250-350 C) and any ITO anneal.
- Practical limits for the Al ground plane: keep all post-Al steps <=300 C where possible; if PECVD at 300-350 C is required, use Al-1%Si-0.5%Cu or a 10-20 nm Ti/TiN cap on the Al, and make the SiO2 over the Al thick enough (>=200 nm) that any hillocks (typically up to ~sub-um tall) do not reach the 5 nm NbN layer. Hillocks under the meander would cause thickness/width constrictions and are the main yield risk.
- Surface roughness of PECVD SiO2 over Al matters for 5 nm NbN; consider measuring AFM RMS on the SiO2 before NbN deposition; Dane 2017 emphasized roughness as the reason bias was needed.

### Gaps
- No quantitative hillock height vs temperature data for thin (50-200 nm) e-beam Al under PECVD SiO2 were found.
- No other cavity SNSPDs with Al mirrors (vs Au/Ag/DBR) were identified in this session; MIT-group NbN SNSPDs specifically on SiO2-over-Al were not found.
