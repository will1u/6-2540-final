# Surface ion trap fabrication (Al ground plane / thick SiO2 / Au electrodes) and electrical test protocols

Scope: recipe details for Si -> thermal oxide (D1) -> sputtered Al ground plane (M1) -> ~10 um PECVD SiO2 (D2) -> Ti/Au seed -> resist mold -> electroplated Au (M2, ~5-6 um) -> seed removal -> SiO2 RIE masked by Au -> isotropic undercut -> D2 openings to M1 -> dicing/packaging, plus electrical test protocols. All numbers carry a source pointer. Items not found in a primary source are listed under Gaps or flagged "(inference)" / "(unverified)".

## Q1. Romaszko et al. 2020 (Nat. Rev. Phys.), Sec. 3 / Fig. 3.1: what the "conventional" flow specifies

### Takeaway
Romaszko et al. is a generic, qualitative description. It gives D1 = 1-2 um SiO2/SiNx (PECVD or thermal), M1 = 1-2 um sputtered or evaporated metal (Au, Al, Cu), D2 on the order of 10 um PECVD SiO2/SiNx (called the hardest step), and M2 by electroplating, sputtering or evaporation, patterned by dry etch. D2 is then RIE-etched using the electrode pattern as the mask and undercut isotropically (wet or vapour). It gives no tool settings, etch rates or temperatures, and the arXiv version has no materials table.

### Cited Findings
- Bibliographic: Z. D. Romaszko, S. Hong, M. Siegele, R. K. Puddy, F. R. Lebrun-Gallagher, S. Weidt, W. K. Hensinger, "Engineering of microfabricated ion traps and integration of advanced on-chip features", Nat. Rev. Phys. 2, 285-299 (June 2020), DOI 10.1038/s42254-020-0182-8; arXiv:1908.00267 — [arXiv PDF](https://arxiv.org/pdf/1908.00267); [Sussex accepted version](https://sussex.figshare.com/articles/journal_contribution/Engineering_of_microfabricated_ion_traps_and_integration_of_advanced_on-chip_features/23307977)
- Sec. 3.2: mid-resistivity Si (1e2-1e4 Ohm cm) is very lossy at RF. The "simplest and most widely used" fix is a ground plane M1 between the RF electrode and the substrate (Fig. 3.1(a)). The alternative is very high- or very low-resistivity Si, keeping in mind that Si can become insulating at cryogenic temperature — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- Sec. 3.3 layer stack: ground layer M1, electrode layer M2, dielectrics D1 and D2. "A 1-2 um layer of either SiO2 or SiNx" (PECVD or thermal oxide) forms D1. M1 is "commonly a 1-2 um layer, either sputtered or evaporated", in any UHV-compatible conductor (Au, Al, Cu) — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- D2 thickness is "generally on the order of 10 um" to maximise the breakdown voltage between RF and ground. Its deposition and etch are "usually ... the most difficult steps", because such thicknesses fall outside conventional semiconductor processing, which limits the material to PECVD SiO2 or SiNx (or a spin-on polymer, ref. [103] = Bautista-Salvador) — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- M2 can be deposited by electroplating, sputtering or evaporation (Fig. 3.1(c)) and patterned by plasma dry etch (Fig. 3.1(d)). Au is the most widely used top metal (it barely oxidises). Because Au is incompatible with many conventional processes, a thin Au layer can instead be put on Al electrodes as a final step (ref. [104]) — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- Fig. 3.1(e)-(f): "vertical etching of the thick dielectric layer ... uses the electrode pattern as a mask, and reactive ion etch", "followed by isotropic wet or gas etching of the dielectric sidewalls" to reduce exposed dielectric — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- Fig. 3.1 caption (a-f): ground plane and insulator; thick (~um's) dielectric; metal layer; metal etch to define electrodes; thick dielectric etch; isotropic etch of the dielectric pillars from the sidewalls — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- Sec. 3.1 design rules: electrodes must sustain the species-appropriate RF voltage; RF coupling into the substrate should be minimised; exposed dielectric in line of sight of the ion should be minimised (UV-induced charging); all materials must survive UHV bake and cryogenic temperatures; wire bonds must not block optical paths; low roughness reduces laser scatter — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)

### Inferences
- "Fig. 3.1" is a schematic flow that the requested MIT.nano flow matches step for step (Al M1, ~10 um PECVD D2, electroplated Au M2, Au-masked D2 RIE, isotropic undercut). The numeric recipe has to come from Hong et al. (JoVE 2017, Q3), Stick et al. (Q2), Siegele-Brown et al. 2022 (Q5) and Bautista-Salvador (Q4). The Sussex 2022 paper shares authors with Romaszko (Hong, Weidt, Hensinger) and is effectively that group's documented Au-on-thick-SiO2 recipe.

### Gaps
- No materials table appears in the arXiv v3 text. The published NRP version may differ (possibly a table of substrate, dielectric and metal properties), but I could not access it, so I could not verify a "materials table".

## Q2. Stick et al. 2010 (Sandia): Al ground plane, PECVD SiO2 pillars, overhang; packaging and shorts test

### Takeaway
arXiv:1008.0990 is confirmed as Stick et al., Sandia National Laboratories. The device is Si, an Al M1 ground plane, 9 um multilayer PECVD SiO2 pillars (9-14 um possible), and Al M2 electrodes overhanging the pillars by 5 um with 7 um gaps, packaged in a 100-pin Kyocera CPGA with Au ribbon bonds to M1-level pads. Every trap was tested for shorts and showed none below 100 MOhm.

### Cited Findings
- D. Stick, K. M. Fortier, R. Haltli, C. Highstrete, D. L. Moehring, C. Tigges, M. G. Blain, Sandia National Laboratories, Albuquerque; arXiv:1008.0990 (v2, 16 Nov 2010) — [arXiv](https://arxiv.org/abs/1008.0990)
- Stack: Si substrate, SiO2 insulators, Al electrodes. PECVD SiO2 pillars separate the overhung Al electrodes from the Al ground plane — [arXiv:1008.0990](https://arxiv.org/abs/1008.0990)
- Pillars are "grown through multiple layers of plasma enhanced chemical vapor deposition" and are 9-14 um thick (9 um in the reported traps). The 5 um overhang is set by "vertical etch stops around the pillars" (Fig. 1). The lateral gap between top-metal electrodes is 7 um — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- The overhang allows vertical (line-of-sight) deposition of extra metal on top of the Al electrode layer without shorting electrodes, the same idea as an Au cap on Al — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- The chip back is Au-evaporated at a small off-normal angle to coat the exposed Si sidewalls and the platform, grounding the backside to prevent charge-up — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- Packaging: Kyocera 100-pin CPGA. The chip is attached with conductive cyanate-ester adhesive (Johnson Matthey JM7000) to a 1.5 mm ceramic spacer that raises the trap surface above the package. Package and chip backside are Au-coated and grounded — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- Bonding: Au ribbons (12.5 um x 75 um) are wedge-bonded to I/O pads on M1, 9 um below the M2 trap plane, and pulled taut to keep their profile low. M1 "serves primarily as a ground plane to prevent RF coupling into the lossy silicon substrate" — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- Electrical test: "Each trap is electrically tested for shorts between any trap electrodes (DC, RF, and grounds, including the ground plane)". No shorts below 100 MOhm were observed in either trap — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- RF: 30 MHz drive at 2 W through a Q = 150 resonator. Total RF-to-ground capacitance (trap + CPGA) is 7 pF. DC electrodes are capacitively grounded outside vacuum with 3 kHz or 200 kHz low-pass filters (the 200 kHz filters are used for shuttling) — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)

### Inferences
- Putting bond pads on M1 under openings in D2 (Stick) is a direct precedent for the requested "D2 openings to reach the Al ground plane for bonding". It also shows that ribbon or wire bonds can land 9 um below the top surface if the openings are large enough for the bond tool.

### Gaps
- The arXiv text does not give PECVD temperature, rate or per-layer thickness, the etch-stop material (likely metal "vertical etch stops" but not specified in the text read), or a journal reference. Publication venue unverified.

## Q3. JoVE 2017 (Hong et al.): full recipe incl. both-side oxide, Al/Cu, BOE undercut, packaging

### Takeaway
The JoVE protocol (Hong, Lee, Kwon, Cho, Kim; DOI 10.3791/56060; Seoul National University group, not ETRI) is the most complete numeric recipe found. Key numbers: 1.5 um sputtered Al-1%Cu ground plane, 14 um PECVD SiO2 deposited on both wafer sides at 350 C and about 300 nm/min, CHF3/CF4/Ar oxide RIE at about 360 nm/min, and a 60 s 6:1 BOE undercut after dicing. Electrodes are Al/Cu, not Au.

### Cited Findings
- S. Hong, M. Lee, Y.-D. Kwon, D. D. Cho, T. Kim, "Experimental Methods for Trapping Ions Using Microfabricated Surface Ion Traps", J. Vis. Exp., published 17 Aug 2017, DOI 10.3791/56060 — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface). The page as fetched did not show the volume or issue, so "126, e56060" is unverified. Romaszko attributes the related low-dielectric-exposure trap to "Seoul National University – Hong et al." — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- Substrate: 500-525 um (100) Si, 100 mm, piranha clean 15 min — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- D1: wet oxidation at 900 C for 4.5 h (O2 6500 / N2 5000 / H2 7000 sccm) gives 0.5 um SiO2 on both sides. Then LPCVD 0.2 um Si3N4 on both sides at 785 C and 200 mTorr (DCS 30 / NH3 100 sccm), about 40 A/min — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- M1: sputter 1.5 um Al-1%Cu at 2 mTorr and 300 W RF with 40 sccm Ar, about 130 A/min. The 1% Cu "prevents whisker formation during bakeout". Pattern with 2 um positive resist and ICP-etch with BCl3 20 / Cl2 30 sccm at 5 mTorr and 750 W, about 3600 A/min. O2 ash 150 sccm, 0.75 mTorr, 300 W — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- D2: PECVD 14 um SiO2 on both sides at 350 C and 1.9 Torr (SiH4 540 sccm, 750 W RF), about 3000 A/min (~300 nm/min) — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- Via holes to M1: 6 um resist (900 mJ/cm2, 10 min develop), then front SiO2 RIE with CHF3 25 / CF4 5 / Ar 50 sccm at 130 mTorr and 600 W, about 3600 A/min. Strip with hot solvent or sonication plus O2 ash — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- M2: sputter 1.5 um Al/Cu, then PECVD 1 um SiO2 as a hard mask. Pattern with 2 um resist and ICP-etch Al/Cu plus the 1 um SiO2. The 14 um oxide pillars are then RIE-patterned with 6 um resist (separate litho), followed by a loading-slot RIE through SiO2/Si3N4 — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- Backside DRIE to 450-470 um depth. Each loop is C4F8 deposition 5 s / C4F8 etch 3 s / Si etch 5 s at 825 W and 23 mTorr, about 1 um per loop — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- Dice into 10 x 10 mm dies, then remove dicing tape with acetone (5 min), DI rinse 10 min, IPA 2 min, and bake 110 C 2 min. Undercut with BOE (NH4F:HF = 6:1) for 60 s to form the overhangs, then DI 10 min, IPA 2 min, 110 C 2 min. The front DRIE through-slot is opened last — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- Packaging: Au wire bonds to a ceramic chip carrier (NTK IPKX0F1-8180BA). EPO-TEK 353ND is listed in the materials table. Bake at 200 C for about 2 weeks. A 240 V RF amplitude was withstood across an 8 um lateral gap at 1e-11 Torr. No pre-installation electrical test is described — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)

### Inferences
- Depositing 14 um PECVD SiO2 on both sides is the paper's stress-management strategy, balancing wafer bow. For MIT.nano, ~10 um on both sides, or a backside compensating film checked on the FLX2320 stress tool, is the analogous approach (inference).
- 300 nm/min PECVD means about 33 min of deposition for 10 um. At 360 nm/min, the D2 RIE takes about 28 min plus overetch. The resist (6 um) and the Au mask must withstand that (inference).
- The 60 s BOE undercut is short because PECVD oxide etches fast in BOE. JoVE does not state the undercut distance or rate. For comparison, Sussex measured a 3(1) um undercut from a partial-thickness BOE finish (Q5).

### Gaps
- The user's recollection of "3.5 um alternating SiO2 depositions on both wafer sides" is not confirmed by the fetched protocol text, which says 14 um on both sides with no sub-layer sequence. It may be in the video or the Supplementary Document (14 = 4 x 3.5 is suggestive but unverified).
- The packaging and wire-bond details are only in the JoVE Supplementary Document, which I did not access.

## Q4. Leibrandt et al. 2009 (Bell Labs/MIT) layer stack and packaging

### Takeaway
The Bell Labs VLSI trap (QIC 9, 901 (2009); arXiv:0904.2599) uses: 0.018 Ohm cm doped Si / 1 um Al ground plane (0.027 Ohm/sq) / 0.4 um SiN / Al DC layer / 10 um stress-balanced PETEOS SiO2 deposited in 1-2 um increments with thermal-equilibration pauses / 1 um Al RF layer, all processed below 400 C. It was packaged in a 100-pin CPGA with an alumina spacer; Au/Sn solder was found to be the best die attach.

### Cited Findings
- D. R. Leibrandt, J. Labaziewicz, R. J. Clark, I. L. Chuang (MIT) with Michigan, NIST and Bell Labs/Alcatel-Lucent (C.-S. Pai, Y. Low, R. Frahm) coauthors; arXiv:0904.2599. The journal ref QIC 9, 901 (2009) is as cited by Stick et al. — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599); [Stick ref. 21](https://arxiv.org/pdf/1008.0990)
- Substrate is highly doped Si (0.018 Ohm cm, 700 um), which is lossy at RF. All processing is below 400 C, so the flow is CMOS back-end compatible — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- Ground plane: 1 um Al at 0.027 Ohm/sq. DC layer: Al on 0.4 um SiN (k = 7.5). Some traps omit the ground plane — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- D2: 10 um PETEOS ("stress balanced SiO2", k = 4), made as thick as possible to cut capacitance and raise breakdown. It "must be deposited with carefully controlled temperature, e.g. deposition of a micron or two and then a pause for thermal equilibration". The paper warns this may leave micro-voids that slowly outgas. The RF layer is 1 um Al — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- The high DC-to-ground capacitance through thin SiN acts as a capacitive divider that RF-grounds pickup on the DC electrodes (DC-RF capacitance is about 1/50 of that). Additional capacitors sit in filters outside vacuum — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- Package: 100-pin CPGA (Global Chip Materials PGA10047002), with 300 x 300 um2 Al pads wire-bonded at the chip edge. The spacer is 1.27 mm 96% alumina with a 2 x 10 mm laser-cut slot. Die attach options compared: EPO-TEK 353 (outgassing and bake concerns, cannot be solvent-cleaned), ceramic paste (poor adhesion, chips detached during bonding), and 80/20 Au/Sn solder at about 285 C between Au-coated surfaces ("strong and clean", re-cleanable). Au/Sn was judged best — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- Without the Al ground plane, Q was about 100 because of RF loss in Si. With the ground plane it was about 150 — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- One NIST chip attached with EPO-TEK 353 reached only 6.7e-8 Pa base pressure — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)

### Inferences
- The "1-2 um then pause" PETEOS practice is the best published hint for managing heat and stress in a 10 um PECVD stack. At MIT.nano that would mean splitting the D2 deposition into several runs, with optional stress checks between them (inference).

### Gaps
- No PETEOS temperature, rate or stress value is given.

## Q5. Au electrode processing: Bautista-Salvador (PTB, NJP 2019 and thesis), Tanaka 2021, and Sussex 2022 (closest Au/thick-SiO2 flow)

### Takeaway
The PTB recipe is: Ti 15 nm / Au 50 nm evaporated seed, 16-25 um resist mold by contact litho, Au electroplated in a sulphite (cyanide-free) bath, resist stripped with NMP/solvent plus O2 and F plasma, Au seed removed by Ar etch (~50 nm/min) and Ti by F-plasma (~10 nm/min). This gives Rrms = 8.3(5) nm, about 100x smoother than aqua-regia wet seed removal. Sussex (Siegele-Brown et al. 2022) is the closest analogue to the requested flow: 8 um PECVD SiO2 under a Cr/Au top layer, oxide dry-etched with the same resist mask to about 750 nm short of the ground plane, then a BOE finish that forms a 3(1) um undercut.

### Cited Findings
- A. Bautista-Salvador et al., "Multilayer ion trap technology for scalable quantum computing and quantum simulation", New J. Phys. 21, 043011 (2019); arXiv:1812.01829 (PTB / Leibniz Univ. Hannover) — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829); [DOAJ](https://doaj.org/article/7435053dc3f84d4e87d16c71ea19abd8)
- Seed: "Ti adhesion layer (15 nm thin) and an Au seed layer (50 nm thin)" by resistive evaporation — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829)
- Mold: "a 25-um-thick positive or 16-um-thick negative resist is spin coated", contact-litho exposed, developed, and the openings "filled to a desired thickness by electrodeposition of Au in a sulphite-based bath" — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829)
- After plating: chemical resist removal, O2 plasma clean, then a fluorine plasma "to further remove possible resist debris". Then the Au seed is removed "via Ar etching" and the Ti by fluorine plasma. Etch rates are 50 nm/min for Au and 10 nm/min for Ti, with "minimal change of the surface quality" — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829)
- Results: features 5 um wide, 2 um gaps, gap aspect ratio up to 14:1. Rrms = 8.3(5) nm by AFM over 25 x 25 um, "a two-order of magnitude improvement when compared to a wet etching process using aqua regia" — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829)
- Other details: 3-inch HiR Si (>1e4 Ohm cm) with 2 um PECVD Si3N4 (blocks Au diffusion into Si and raises flashover). Vias use a >12 um negative resist mold. Polymer dielectric is spin-coated, cured and CMP-planarised. The final step is a F-plasma etch of the polymer in the gaps down to Si3N4. The chip is glued to a Cu block and wire-bonded to a filter PCB; RF is 2pi x 176.5 MHz at 100 V, DC within +/-25 V — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829)
- Thesis (A. Bautista-Salvador, Univ. Ulm 2015, "Integrated Electromagnets and Radiofrequency Spectroscopy in a Planar Paul Trap"): uses a cyanide-free electrolyte (pH 7.5) of gold sulfite complex, "Microfab Au 100-B" (Enthone). AZ nLOF 2070 negative resist was chosen for adhesion and chemical stability at pH > 8. Seed is Cr 5-6 nm / Au 50 nm evaporated at 1 A/s — [Thesis PDF](https://www.quantenbit.physik.uni-mainz.de/files/2015/11/PhDThesis_Bautista_Online.pdf)
- Thesis: resist strip in NMP 1 h plus O2 RIE 20 min (an earlier 36 h NMP soak left residues). Wet Au seed etch with KI/I2 runs at 16 nm/min (1:1), but it degraded roughness. Diluting 1:2 with H2O gives 4 nm/min. The thesis also notes that Ti etchant (HF) attacks SiO2, so Ti must be handled with care on oxide — [Thesis PDF](https://www.quantenbit.physik.uni-mainz.de/files/2015/11/PhDThesis_Bautista_Online.pdf)
- Tanaka et al. 2021 (PTB-fabricated trap, arXiv:2101.00459): 16 um positive resist by contact litho, sulphite-based Au bath, "gold with a thickness of up to 20 um". Resist removed in acetone/IPA plus O2 plasma; Au seed and Ti removed "by means of Ar reactive ion etching" — [arXiv:2101.00459](https://arxiv.org/pdf/2101.00459)
- Sussex 2022 (M. Siegele-Brown, S. Hong, F. R. Lebrun-Gallagher, S. J. Hile, S. Weidt, W. K. Hensinger, Quantum Sci. Technol., DOI 10.1088/2058-9565/ac66fc; arXiv:2202.02313): PECVD 0.5-1 um SiO2 is opened with BOE (HF:NH4F = 1:7). The ground plane is Cr/Au/Cr 10/1000/10 nm, sputtered and ion-beam-etched. "Next, an 8 um-thick SiO2 layer and 10/1000-3000 nm-thick Cr/Au layer are deposited", and "these two layers are dry etched sequentially using the same photoresist mask" — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313); [IOP](https://iopscience.iop.org/article/10.1088/2058-9565/ac66fc)
- Sussex 2022: "The good uniformity (4(1)%) of the deep oxide etching process allows stopping 750(250) nm before reaching the Cr/Au/Cr layer, in order not to expose the gold to the oxide etching chemistry". BOE removes the remainder and "also etches the sidewalls of the oxide pillar", giving a 3(1) um undercut. The exposed Cr over the Au ground plane is then wet-etched. The backside gets 10/500 nm Cr/Au for indium bonding — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)
- Sussex 2022 redeposition: after ion-beam etching, "every surface in the line of sight of the ion beam impact is covered with some redeposited material, which is unavoidable" (seen in the FIB cross-section) — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)
- Sussex 2022 RF: 8 um oxide between the RF electrode and ground plane gave a measured flashover above 250 V_amp at 15 MHz on a test-structure chip — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)
- Sussex 2022 Al ground plane: the trapping chip actually used an Al ground plane (an earlier version). The group switched the ground plane to Au "to avoid an aluminium electrode, as such an electrode could potentially form a very thin oxide layer and charge up", but "did not observe any adverse effects because of the aluminium ground plane". Ions were trapped for 7-16 h — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)
- Sussex 2022 tests: resistance between Cu tracks and the other conductors exceeded the 10 MOhm measurement limit, and no unintended shorts were found between electrodes. CCW resistance was measured four-terminal at 100 mA. Bonding used ten 25 x 125 um Al ribbon bonds per high-current pad — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)

### Inferences
- Au-as-mask oxide RIE: Sussex dry-etches the oxide with the same resist mask still on top of the Au, so the Au is not the sole mask, and stops short of the ground plane. Both practices limit Au sputtering and redeposition onto the pillar sidewalls, which could short the electrodes to M1 across the gap. For the requested flow (Au as the D2 mask), a reasonable mitigation is to leave the plating resist or a thin hard mask on during the D2 RIE, or at least keep ion energy moderate. The undercut BOE also lifts off thin redeposited films on the sidewalls (inference).
- With an Al M1 (instead of Au), stopping the RIE early and finishing in BOE protects the Al, because BOE attacks Al. The finish therefore needs to be short, or the M1 surface covered (e.g., by a thin SiNx or Al2O3 etch-stop between M1 and D2), or a BOE with Al-compatible additives used (inference; no source found on Al attack rate in BOE).
- Ti adhesion under Au: HF/BOE etches Ti (thesis). During the undercut BOE, the Ti under the Au edges is exposed at the pillar sidewall. A long BOE will undercut the Ti itself and can lift the Au. Options are Cr adhesion (Sussex uses Cr, which is HF-resistant) or keeping the BOE time short (60 s in JoVE) (inference).
- Seed removal: Ar ion-beam/RIE (PTB) gives the best roughness. At MIT.nano, "Clean-Ar-Plasma" or an Ar recipe on one of the RIE tools could approximate it (unverified). Wet KI/I2 (diluted, ~4 nm/min) is a fallback, at the cost of roughness.

### Gaps
- No current density, temperature or plating rate was found in the NJP paper, Tanaka, or the thesis text searched.
- No source was found on AZ 40XT, AZ 9260 or KMPR specifically for ion-trap Au molds. PTB used 25 um positive / 16 um negative resist, and the thesis used AZ nLOF 2070. A mold for 5-6 um Au would need resist of at least about 7-8 um (inference).

## Q6. Thick PECVD SiO2 stress, D2 etch chemistry and rate, BOE undercut, Al hillocks

### Takeaway
Concrete published numbers: PECVD SiO2 at 350 C, about 300 nm/min, 14 um deposited on both sides (JoVE); CHF3/CF4/Ar RIE at about 360 nm/min (JoVE); 1-2 um increments with thermal pauses (Leibrandt); 6:1 BOE for 60 s (JoVE); 1:7 BOE finish giving a 3 um undercut (Sussex); 1% Cu in Al to suppress whiskers and hillocks during bake (JoVE). No quantitative stress value (MPa) or wafer-bow number for 10 um PECVD oxide was found in the trap literature.

### Cited Findings
- PECVD SiO2: 14 um on both sides, 350 C, 1.9 Torr, SiH4 540 sccm, 750 W, about 3000 A/min — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- PETEOS, 10 um, "stress balanced": deposit 1-2 um, then pause for thermal equilibration. Possible micro-voids may outgas — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- Stick: pillars grown "through multiple layers" of PECVD — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- Oxide RIE: CHF3 25 / CF4 5 / Ar 50 sccm, 130 mTorr, 600 W, about 3600 A/min — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- Deep oxide etch uniformity of 4(1)% allows stopping 750(250) nm above the ground plane — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)
- Al-1%Cu prevents whisker formation during bakeout — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- MIT.nano has a Tencor FLX-2320 film stress tool ("Filmstress-Tencor-FLX2320") for measuring bow and stress — [MIT.nano Fab.nano tool list (Jul 2025)](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)

### Inferences
- A 10 um PECVD stack on a single side of a 500 um wafer will bow noticeably (typical PECVD oxide is slightly compressive). Following JoVE and depositing the same thickness on the backside, or tuning toward near-zero stress and checking with the FLX2320 between runs, is the prudent approach (inference; no MPa value sourced).
- Hillocks on a pure-Al M1 at 300-350 C PECVD could poke through or thin D2 locally and lower breakdown. Al-1%Cu (or Al-Si-Cu) sputtered M1 is the sourced mitigation (JoVE), and limiting the D2 temperature helps (inference).
- With Au on top, the M1 opening (D2 via) should be etched before Au plating, as in JoVE where the vias are opened before M2. Otherwise a separate resist-masked RIE step on a topography of 10 um oxide plus 5 um Au is needed (inference).

### Gaps
- No quantitative BOE etch rate for PECVD SiO2 was found in these sources. It is tool- and film-dependent; calibrate on witness wafers.
- No source measured Al-in-BOE attack or the Ti undercut rate during the trap undercut.
- No published data were found on Au sputter redeposition specifically during Au-masked SiO2 RIE in ion traps. Only the Sussex IBE-redeposition remark was found.

## Q7. Dietl et al. 2025: wafer-level electrical test protocol (and other test practice)

### Takeaway
Dietl et al. (arXiv:2505.21284; Adv. Quantum Technol. 2025) runs a room-temperature, 120-needle probe-card test per chip before dicing. It covers continuity (1 mA forced, pass at 0-100 mV), DC leakage (50 V, pass at <=100 nA), RF leakage (300 V DC, pass at <=100 nA), and resistance (5 mV forced, pass at 0-50 Ohm). Each DC electrode is laid out as a "loop electrode" with two pads, so continuity can be checked. Yield was 54% (258/477).

### Cited Findings
- "Test and characterization of multilayer ion traps on fused silica", M. Dietl et al., arXiv:2505.21284 (May 2025). The search result reports it as also in Advanced Quantum Technologies (2025, vol. 8, no. 11, e00412); the venue is from the search summary, not verified on the publisher page — [arXiv HTML](https://arxiv.org/html/2505.21284)
- Stack: 725 um fused silica on 200 mm wafers (temporary 2 um backside poly-Si for handling). Three Al layers: M1 and M2 at 1 um, M3 at 2 um. Two PECVD SiOx layers of 1 um and 2 um (+/-10%). Vias get an in-situ Ar mill before M2 deposition. Made at Infineon Villach in 104 steps with 365 nm lithography — [arXiv:2505.21284](https://arxiv.org/html/2505.21284)
- Test design: each DC electrode is a loop with two bond pads joined through the electrode. 480 steps per chip take about 7.8 s, and testing stops at the first failure — [arXiv:2505.21284](https://arxiv.org/html/2505.21284)
- Continuity: force 1 mA, pass if V = 0-100 mV (about 100 Ohm loop) and I = 0.8-1.3 mA — [arXiv:2505.21284](https://arxiv.org/html/2505.21284)
- DC leakage: 50 V applied against all other DC electrodes and GND, pass if <=100 nA and sensed V within +/-100 mV. RF leakage: 300 V DC on the RF electrode, same limits, chosen to stay below air breakdown between neighbours. Leakage tests are run twice to catch breakdown-induced shorts — [arXiv:2505.21284](https://arxiv.org/html/2505.21284)
- Resistance: force 5 mV, pass at 0-50 Ohm for DC and RF lines. The temperature sensors (Al meanders, 1-2 um wide, 70-94 cm long, four-wire at 5 mA) have kOhm-range windows. The paper's text and Table 2 appear to swap the TS1/TS2 labels — [arXiv:2505.21284](https://arxiv.org/html/2505.21284)
- Equipment: 120 probe needles with 40 um tips, SMUs, at atmosphere and 295 K. Failures were continuity 15.5% (mostly wafer edge) and leakage 29.8% (including DC-to-GND leakage with a 3x reticle periodicity). The room-temperature-only test is a stated limitation for cryogenic operation — [arXiv:2505.21284](https://arxiv.org/html/2505.21284)
- Other protocols: Stick tests every electrode pair including the ground plane and requires no shorts below 100 MOhm — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990). Sussex reports >10 MOhm (instrument limit) between conductors and four-terminal resistance at 100 mA — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313). Leibrandt uses in-situ Q (about 150) and RF/DC capacitance checks as a health metric — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599). Stick reports 7 pF RF-to-ground (trap plus CPGA) — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- MIT.nano lists "ProbeStation-Summit-11000" (Cascade Summit 11000 class probe station) and a 4-point probe — [MIT.nano tool list](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)

### Inferences
- Test structures for an MIT.nano run (adapted from Dietl and Stick, inference):
  - Two-pad loop DC electrodes for continuity.
  - An M2-to-M1 parallel-plate capacitor and leakage/breakdown structure (large pad over D2) to measure leakage at 50-300 V DC and C per area (expected ~3.5 pF/mm2 for 10 um SiO2 with k = 3.9).
  - Interdigitated M2 combs with the design gap (e.g., 5-7 um) for lateral leakage and redeposition-short detection.
  - A via chain or Kelvin structure through the D2 opening to M1 to check bondability and contact.
  - Au and Al sheet-resistance van der Pauw structures.
- RF flashover qualification: Sussex measured >250 V_amp at 15 MHz on a dedicated test-structure chip with 8 um oxide. A similar sacrificial test chip is advisable before committing to the RF amplitude (inference).

### Gaps
- Pfeifer 2026 fused-silica fabrication methods: not searched or found within the tool budget. Unverified.

## Q8. MIT.nano tool names (verified from the Fab.nano tool charge list, July 2025)

### Takeaway
Tool names confirmed in MIT.nano's Fab.nano tool charge list (July 2025): MLA150 direct-write, MA6 mask aligner, Elionix HS50 EBL, AJA sputter, Oxford TEOS PECVD and Samco PD220 PECVD, Samco and PlasmaTherm RIEs, SPTS Pegasus DRIE, HF/BOE wet bench, a plating tank (Plating-U04), DAD3240 dicing saw, wedge/ball wire bonders, FLX2320 stress tool, Dektak profilometers and a Summit 11000 probe station. Process capabilities (rates, recipes, bath chemistry) are not given in that list.

### Cited Findings
- Lithography: "DirectWrite-MLA150-AirAF", "DirectWrite-MLA150-OptAF", "DirectWrite-Raith-PicoMaster", "MaskAlign-MA6", "EBL-Elionix-HS50", spinners incl. "Spinner-SU8", "Spinner-Resist-U12"/"-L10", hotplates — [MIT.nano tool list](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)
- Deposition: "Sputter-AJA-ChamberLoad", "Sputter-AJA-LL", "Sputter-4Chamber-AMAT-Endura", "Sputter-Balzer-Au", "EBeam-AJA", "EBeam-Temescal-FC2800", "EBeam-Temescal-LL", "PECVD-Oxford-TEOS", "PECVD-Samco-PD220", "PECVD-STS-MMPLEX", "PECVD-2Chamber-AMAT-Centura", "ALD-Plasma-Arradiance-*" — [MIT.nano tool list](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)
- Furnaces: "Ox-Tube-Lindberg", "Tube-OxAnneal-Expertech-CTR200", "Anneal-Tube", "Anneal-Box" — [MIT.nano tool list](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)
- Etch: "RIE-F-Samco-230iP", "RIE-Mixed-Samco-230iP", "RIE-Cl2-SAMCO-200iP", "RIE-PlasmaTherm-210RL-A/-B", "RIE-2Chamber-AMAT-P5000", "DRIE-SPTS-Pegasus", "DRIE-STS-MMPLEX", "OxideEtch-HF-BOE-L06", "Acid-Etch-General-*", "Clean-Ar-Plasma", ashers ("Asher-TergeoPro-Strip", "Asher-Barrel-Thierry", etc.) — [MIT.nano tool list](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)
- Plating: "Plating-U04" ($637.5/full tank) — [MIT.nano tool list](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)
- Back-end and metrology: "Diesaw-DAD3240", "Scribe-Frontside/Backside", "Wirebond-Wedge", "Wirebond-Ball-MEI", "Wirebond-Ball-Westbond", "Wirebond-Auto", "DieBonder-PickAndPlace", "Filmstress-Tencor-FLX2320", "Dektak-150", "Dektak-XT", "4_Point_Probe", "ProbeStation-Summit-11000" — [MIT.nano tool list](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)
- The Elionix HS50 EBL and Temescal FC-2800 e-beam evaporator were added to the MIT.nano cleanroom (news item) — [MIT campus planning news](https://campusplanning.mit.edu/highlights-and-initiatives/mit-nano-adds-new-instruments-to-create-and-analyze-at-the-nanoscale/)

### Inferences
- Mapping the flow to tools (inference, not verified recipes):

| Step | Tool |
|---|---|
| Thermal oxide (D1) | Ox-Tube-Lindberg / Expertech |
| Al(-Cu) M1 | AJA sputter (check target availability) |
| 10 um D2 | Oxford TEOS PECVD or Samco PD220, multiple runs, FLX2320 stress check |
| D2 via etch | Samco 230iP fluorine RIE or PlasmaTherm |
| Ti/Au seed | AJA e-beam or sputter |
| Mold litho | MLA150 for thick resist; MA6 alternative |
| Au plating | Plating-U04 (bath chemistry unknown) |
| Seed removal | Ar plasma / IBE-like RIE, or wet KI/I2 |
| D2 RIE | Samco/PlasmaTherm fluorine |
| Undercut | OxideEtch-HF-BOE-L06 |
| Dicing | DAD3240 |
| Bonding | Wirebond-Wedge / Ball |
| Electrical test | Summit 11000 probe station |

### Gaps
- I could not verify the plating bath type (sulfite vs cyanide Au) in Plating-U04, or whether it is a gold tank at all. Its chemistry must be confirmed with MIT.nano staff.
- No MIT.nano recipe pages (rates, stress) were accessed. The nanousers.mit.edu tool pages were not opened.

## Q9. Wire bonding to Au pads and the Al ground plane; chip carrier and RF filtering

### Takeaway
Published practice uses 100-pin CPGAs with a raised spacer, Au ribbon or wire wedge bonds, and DC-line RC/capacitive filtering close to the chip. Examples: Stick used 12.5 x 75 um Au ribbon wedge-bonded down to M1 pads 9 um below the surface. Graham et al. used 20 nF 0805 ceramic capacitors about 1 cm from the chip on an in-vacuum Rogers PCB with a ZIF socket for the CPGA. Leibrandt found Au/Sn solder (about 285 C) the cleanest die attach.

### Cited Findings
- Stick: Kyocera 100-pin CPGA, JM7000 conductive cyanate ester, 1.5 mm ceramic spacer, Au ribbon wedge bonds to M1-level pads, chip backside Au-coated and grounded. DC filters at 3 kHz or 200 kHz outside vacuum — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990)
- Leibrandt: 100-pin CPGA (Global Chip Materials PGA10047002), Al pads 300 x 300 um, 1.27 mm alumina spacer. Au/Sn 80/20 solder at about 285 C between Au-coated surfaces; epoxy and ceramic paste were problematic — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- Graham et al., "A system for trapping barium ions in a microfabricated surface trap", arXiv:1305.2224 (2013; R. D. Graham, S.-P. Chen, T. Sakrejda, J. Wright, Z. Zhou, B. B. Blinov, University of Washington). Uses Sandia/GTRI 100-pin traps (Sandia "Y" trap) and a standard 100-pin ceramic PGA (33.5 mm square) in a ZIF socket (Tactic 100-4680-001A) on an in-vacuum Rogers RT/duroid 6002 PCB (1.52 mm, 35 um Cu). DC pins are filtered with 20 nF 0805 all-ceramic capacitors about 1 cm from the chip. A helical copper resonator drives the RF. Lead-free Sn/Ag/Cu solder was used — [ar5iv 1305.2224](https://ar5iv.labs.arxiv.org/html/1305.2224). The full author list comes from the search summary; the published venue was not verified.
- JoVE: Au wire bonds to an NTK ceramic carrier; EPO-TEK 353ND listed — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- PTB: chip glued to a Cu block and wire-bonded to a custom filter PCB — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829)
- Sussex: indium solder to a Cu block (backside 10/500 nm Cr/Au for In wetting); Al ribbon bonds — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)

### Inferences
- Bonding to Al M1 through D2 openings: an Al or Au wedge bond onto Al pads is standard (Leibrandt bonded to Al pads). The 10 um oxide step means the openings should be wide (e.g., >=150-300 um, Leibrandt's pads were 300 um) so the wedge tool clears the sidewall. Optionally the M1 pad can be capped with Ti/Au during seed deposition to give an Au bonding surface (inference).
- Au wire on Al pads can form Au-Al intermetallics during a 200 C bake ("purple plague"). Al wire on the Al ground pad and Au wire on Au electrodes avoids this. Not sourced in the trap papers read; general packaging knowledge (inference).

### Gaps
- Bond parameters (force, ultrasonic power) for electroplated Au trap pads were not found.

## Q10. Synthesized step-by-step flow for MIT.nano (all values traced to sources; adaptations flagged)

### Takeaway
A composite recipe is feasible from the sources: JoVE for the substrate, M1 and D2 numbers; PTB for the Au plating and seed removal; Sussex for the D2 etch-stop-plus-BOE undercut; Stick, Leibrandt and Dietl for packaging and test. The main open risks are D2 stress, Al attack during the BOE finish, Ti undercut under the Au, and Au redeposition during the D2 RIE.

### Cited Findings
- 1) Si (100) wafer, piranha 15 min — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- 2) D1: wet oxide 0.5 um at 900 C, 4.5 h (JoVE adds 0.2 um LPCVD SiN) — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface). Romaszko gives 1-2 um as typical — [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- 3) M1: sputter 1-1.5 um Al-1%Cu (about 13 nm/min at 300 W RF, 2 mTorr). Pattern M1 (pads, ground) with BCl3/Cl2 ICP at about 360 nm/min — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface); Leibrandt used 1 um Al — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- 4) D2: PECVD SiO2 ~10 um at 350 C (~300 nm/min), built up in increments with pauses, with backside compensation — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface); [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)
- 5) D2 bond-pad openings to M1: 6 um resist, CHF3/CF4/Ar RIE at about 360 nm/min — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)
- 6) Seed: Ti 15 nm / Au 50 nm (PTB), or Cr 10 nm / Au as in Sussex — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829); [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)
- 7) Mold: thick resist (PTB used 16-25 um; thesis used AZ nLOF 2070). 8) Electroplate Au in a sulphite bath to 5-6 um (PTB plated up to 20 um) — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829); [arXiv:2101.00459](https://arxiv.org/pdf/2101.00459); [Thesis](https://www.quantenbit.physik.uni-mainz.de/files/2015/11/PhDThesis_Bautista_Online.pdf)
- 9) Strip the mold (NMP/solvent, then O2 plus F plasma). Remove the seed with Ar etch (Au ~50 nm/min) and F-plasma (Ti ~10 nm/min) — [arXiv:1812.01829](https://arxiv.org/pdf/1812.01829)
- 10) D2 RIE using the electrodes (plus resist, in Sussex) as the mask. Stop about 0.75 um above the ground plane — [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313); [arXiv:1908.00267](https://arxiv.org/pdf/1908.00267)
- 11) Dice, clean, then BOE undercut (6:1 for 60 s in JoVE; 1:7 BOE finish giving a 3(1) um undercut in Sussex) — [JoVE](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface); [arXiv:2202.02313](https://arxiv.org/pdf/2202.02313)
- 12) Electrical test: shorts >100 MOhm between all electrodes and the ground plane (Stick); Dietl-style continuity at 1 mA and leakage at 50 V / 300 V with <=100 nA — [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990); [arXiv:2505.21284](https://arxiv.org/html/2505.21284)
- 13) Package: 100-pin CPGA plus spacer, Au/Sn or conductive die attach, wedge bonds, DC filter capacitors near the chip — [arXiv:0904.2599](https://arxiv.org/pdf/0904.2599); [arXiv:1008.0990](https://arxiv.org/pdf/1008.0990); [ar5iv 1305.2224](https://ar5iv.labs.arxiv.org/html/1305.2224)

### Inferences
- Ordering note: JoVE dices before the BOE undercut so the fragile overhangs survive dicing. Dicing tape is removed in acetone first. Adopt the same order (inference drawn from the JoVE sequence).
- If Au is the sole D2 RIE mask, 5-6 um Au gives ample selectivity. The concern is sputtered Au landing on the sidewalls (Sussex observed line-of-sight redeposition after IBE). Keep the resist on during the D2 RIE, as Sussex does (inference).

### Gaps
- No single source documents exactly "Al M1 + 10 um PECVD + electroplated Au M2 + Au-masked RIE". The recipe is a composite and every combination step needs witness-wafer calibration (BOE rate on this specific PECVD oxide, Ti/Al attack, stress).
