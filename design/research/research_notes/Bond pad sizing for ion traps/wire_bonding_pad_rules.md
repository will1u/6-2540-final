# Wire-bonding process requirements for bond pad size, pitch and metallization

> **Claude-authored** research notes (2026-11-08). Raw notes for the report writer; not verified against MIT.nano tools.

Scope: 10 x 10 mm surface-electrode ion-trap die, hand-bonded at a university facility (MIT.nano). Stack: high-resistivity Si / Al ground plane (M1) / 10 um PECVD SiO2 / 6 um electroplated Au (on a seed layer). Pads now: 120 x 200 um Au on a 180 um pitch (60 um gap); 200 x 200 um Au for RF and one DC; Al ground-plane openings 170 x 170 um at the bottom of 10 um-deep wells in the SiO2; two SNSPD pads on a few-hundred-nm Ti/Au layer, exposed through 120 x 90 um openings in the 10 um SiO2.

Source quality note: the two primary documents I read in full are the EPFL CMi "TPT HB10 wire bonder guidelines" (Dec. 2017) and the Europractice "ASIC Prototype Packaging Design Rules 2024". Other numbers come from search-result excerpts of pages I could not fully fetch (UC Davis CNM2 returned HTTP 403; a wedge-tool tech tip returned HTTP 401). These are marked "(excerpt only)". I did not get access to Harman's book, the MIL-STD-883 text, or any K&S / West Bond / Hesse / TPT / MEI design guide, so no numbers are quoted from them.

## 1. Bond size vs wire diameter, and recommended minimum pad size and pitch

### Takeaway
For 25 um (1 mil) Au wire, a ball bond is about 2-3x the wire diameter (about 50-75 um across), and a wedge foot is about 1.2-3x the wire diameter wide and 1.5-5x long. University bonding facilities ask for about 100 x 100 um pads as standard, with a hard floor of about 55-60 um. Industry fine-pitch minimums for 25 um Au ball bonding are 55 um pads on a 65 um pitch. Those are machine-placement numbers, not hand-bonding numbers.

### Cited Findings
**Ball size**
- Free-air ball (FAB) diameter is "generally 2-3 times of wire diameter" (academic capillary study; excerpt only) — [ProQuest record](https://www.proquest.com/docview/2474760246)
- UC Davis CNM2 (West Bond 7700E ball bonder, 1 mil Au wire): ball bond diameter about 75 um, "so ideally bond pads should be 100x100um square or larger"; gold should be at least 200 nm thick (excerpt only; page returned HTTP 403 when fetched) — [UC Davis CNM2 West Bond 7700E](https://cnm2.ucdavis.edu/equipment/west-bond-7700e-ball-bonder)
- Bond squash is about 2x wire diameter for ball bonding vs about 1.3x for wedge bonding (Circuits Assembly; excerpt only) — [Circuits Assembly article index](https://circuitsassembly.com/ca/editorial/menu-features/277-magazine-articles.html?start=366)

**Wedge foot size (visual-inspection reject limits)**
- An ESCC (European Space Components Coordination) internal-visual specification for SAW devices rejects wedge bonds with width < 1.2 or > 3 wire diameters, or length < 1.5 or > 5 wire diameters, and ball height < 1 or > 3 wire diameters (excerpt only) — [escies.org spec](https://escies.org/download/specdraftapppub?id=2884)
- For 25 um wire, that gives an acceptable wedge foot of about 30-75 um wide and about 38-125 um long (my arithmetic from the ESCC ratios).
- I could NOT verify the corresponding MIL-STD-883 numbers. Method 2017 is the hybrid/multichip internal visual; monolithic-device wire-bond visual criteria are in TM 2010 — [MIL-STD-883 TM 2017 copy, q-tech.com](https://q-tech.com/wp-content/uploads/STD-883-2017.pdf); [TM 2010 course description](https://passive-components.eu/event/mil-std-883-tm-2010/)

**Facility and foundry pad rules**
- EPFL CMi (TPT HB10, manual; Al wire 17.5 and 33 um wedge-wedge only; Au wire 20 and 25 um, wedge-wedge and ball-wedge): "Standard dimensions for the pads are 100umX100um with a 100um spacing. All these dimensions can be reduced to 60um for smaller pitch, but not more." Pads should be in a single line at the die edge, and the maximum distance from pads to the die edge is 500 um. Longer distances need higher loops, which their machine does not support, and longer wires are less rigid and more likely to short. Pads on the support/package must be Au. — [EPFL CMi HB10 guidelines (PDF)](https://www.epfl.ch/research/facilities/cmi/wp-content/uploads/2020/04/HB10_guidelines.pdf)
- EPFL CMi: the package/PCB bond pads should be at least 300 x 500 um, and the gap from die edge to package pads should be 500 um minimum and 2 mm maximum. — [EPFL CMi HB10 guidelines (PDF)](https://www.epfl.ch/research/facilities/cmi/wp-content/uploads/2020/04/HB10_guidelines.pdf)
- Europractice (25 um Au ball, standard service): bond pad opening > 55 x 55 um, pitch > 65 um, wire length 6 mm or less, bond wire angle < 45 deg, at most 2 wires per pad, die placement accuracy +/-100 um (manual placement). Table 2 (non-standard Au ball): 17.5 um wire: 40 um pad / 50 um pitch / 4.5 mm max length; 20 um: 46 / 56 / 5.0; 25 um: 55 / 65 / 6.0; 33 um: 70 / 80 / 7.0; minimum wire angle 45 deg. It also recommends leads into a pad be at least 20 um wide. — [Europractice ASIC Prototype Packaging Design Rules 2024 (PDF)](https://europractice-ic.com/wp-content/uploads/2020/06/ASIC_Prototype_Packaging_Design_Rules_2024.pdf)
- CERN Bond Lab: a 60 um bond pitch is possible with 25 um wire, but only with a double-side-relief wedge tool that limits loop height. "The minimum preferable in line distance between two bonds is 300um" (tool- and loop-dependent). Al wedge bonds call for a more rectangular pad, Au ball bonds a more square one. Make pads "as large as is realistically possible". — [CERN Bond Lab recommendations](https://bondlab.web.cern.ch/Recommendations.html)
- A patent notes ball bonding becomes difficult when pads are closer than about 100 um, because of the capillary diameter (excerpt only; patent context, older technology) — [US5544804A](https://patents.google.com/patent/US5544804)
- Industry blog sources give pad = 1.5-2x wire diameter, or ball pads of 60-120 um. These are secondary sources and are not used as primary numbers here. — [LCSC blog](https://www.lcsc.com/blog/?p=4177)

### Inferences
- Pad width needed for one bond, 25 um Au wire: ball ~75 um, wedge foot ~30-75 um wide x ~38-125 um long. A 100 um-wide pad gives about +/-12 um placement margin around a 75 um ball. A 120 um-wide pad gives about +/-22 um.
- The current 120 x 200 um signal pads on a 180 um pitch (60 um gap) exceed every minimum found (EPFL 60 x 60 um / 60 um gap; Europractice 55 um / 65 um pitch for 25 um Au ball) and match EPFL's 100 um "standard". The 200 um length is enough for about 2 wedge feet in a row (each up to ~125 um long at the ESCC upper limit) or 2 ball bonds (75 um each).
- The ratio "pad >= 2-3x bond foot" asked about in the brief was NOT found stated as a rule in any source I could verify. The closest verified guidance is facility minimums (55-60 um) vs standards (100 um) for 25 um wire, which is roughly 1.3-1.5x a 75 um ball.
- Sanity check worth running: lay out a bond diagram with the actual package/PCB pads. Check wire angle (< 45 deg from pad normal per Europractice), wire length (<= 6 mm for 25 um Au), and die-edge-to-pad distance (<= 500 um at EPFL; 500 um-2 mm to package pads).

### Gaps
- I could not access K&S, West Bond, Hesse, TPT, MEI/Marpet or Palomar design guides, or Harman's book, so there are no manufacturer numbers for capillary tip diameter, wedge foot length per tool part number, or bond placement accuracy.
- I found no published number for the placement accuracy of a manual bonder (operator + micromanipulator). Europractice's +/-100 um is die-placement accuracy, not bond placement.
- MIL-STD-883 TM 2010/2017 bond-dimension criteria are unverified (the text was not read).

## 2. Advantages of larger pads for manual bonding; common research-cleanroom practice

### Takeaway
University facilities set 100 x 100 um as the standard pad and treat about 60 um as the absolute floor. CERN explicitly advises making pads as large as practical. I found no source that quantifies how much rework or how many attempts an extra pad area buys.

### Cited Findings
- EPFL CMi: standard 100 x 100 um pads with 100 um spacing; 60 um is the minimum for both; smaller "will not be compatible with the CMi wire-bonding machine". — [EPFL CMi HB10 guidelines (PDF)](https://www.epfl.ch/research/facilities/cmi/wp-content/uploads/2020/04/HB10_guidelines.pdf)
- UC Davis CNM2: 100 x 100 um "or larger" for a ~75 um ball (excerpt only). — [UC Davis CNM2](https://cnm2.ucdavis.edu/equipment/west-bond-7700e-ball-bonder)
- CERN Bond Lab: "prudent to make the bond pad as large as is realistically possible"; consider bond-foot size and form in 3D. — [CERN Bond Lab recommendations](https://bondlab.web.cern.ch/Recommendations.html)
- Europractice allows at most 2 wires per pad (standard service), which implies room for 2 bond feet on a pad if doubling up. — [Europractice 2024 (PDF)](https://europractice-ic.com/wp-content/uploads/2020/06/ASIC_Prototype_Packaging_Design_Rules_2024.pdf)
- Probe marks can hide cracks at the bottom of the pad stack (bond-pad damage study, Al pads; excerpt only). This is relevant if pads are probed before bonding. — [SWTW 2016, Hunter](https://www.swtest.org/swtw_library/2016proc/PDF/T01_01_Hunter_SWTW2016.pdf)

### Inferences
- A pad long enough for 2+ bond footprints allows a re-bond next to a lifted or failed bond without landing on the residue. This matters most for students learning the tool. The 200 um-long pads allow that; the 120 um width allows a single row.
- If pads are to be probed before bonding, a separate probe area (or a pad long enough to keep probe marks off the bond area) avoids bonding onto a probe scrub. The Hunter paper's probe-crack finding is for Al pads on low-k stacks, so how far it transfers to thick Au is uncertain.

### Gaps
- No quantitative data found on yield vs pad size for manual bonding, or on how many re-bond attempts a given pad length supports.
- I found no published MIT.nano, Stanford SNF, Berkeley Marvell or Cornell CNF pad-size rule (searched, not found).

## 3. Metallization: Au thickness, electroplated Au, adhesion, bonding over thick SiO2 and a buried Al plane

### Takeaway
Facilities ask for at least 100-200 nm Au with a Ti or Cr adhesion layer. Electroplated Au for wire bonding should be soft, high-purity Au (about <= 90 Knoop; annealing softens it). Bonding over a soft or compliant layer under the pad reduces ultrasonic coupling and raises cratering risk, and a stiffer pad helps. I found no source that addresses a 10 um PECVD SiO2 layer over a buried Al plane specifically.

### Cited Findings
**Thickness and adhesion**
- EPFL CMi: standard pad materials are Au, Al or Pt "with specific titanium or chromium adhesion layers"; "The thickness of the pads cannot be less than 100nm"; "Mind the adhesion layer!!"; no guarantee for thinner pads or other materials. — [EPFL CMi HB10 guidelines (PDF)](https://www.epfl.ch/research/facilities/cmi/wp-content/uploads/2020/04/HB10_guidelines.pdf)
- UC Davis CNM2: Au at least 200 nm thick (excerpt only). — [UC Davis CNM2](https://cnm2.ucdavis.edu/equipment/west-bond-7700e-ball-bonder)

**Electroplated Au hardness**
- ASTM B488 (electrodeposited Au for engineering uses) classifies coatings by purity type and Knoop hardness code, and lists bondability as an application. — [ASTM B488 catalog page](https://standards.iteh.ai/catalog/standards/astm/cd877f37-2151-48d2-9883-32439fc575e8/astm-b488-012010e1)
- Plating vendor: hardness grade A (<= 90 Knoop) is the wire-bond grade; MIL-DTL-45204 is referenced for soft, high-purity Au for wire bonding (vendor source; excerpt only). — [Gleco Plating](https://glecoplating.com/?p=221)
- Vendor article: soft Au about 60-85 Knoop vs hard Au about 120-300 Knoop; wire bonding uses soft Au (secondary source). — [ALLPCB](https://www.allpcb.com/allelectrohub/hard-gold-vs-soft-gold-plating-choosing-the-right-finish-for-your-electronic-components)
- Patent family on bonding over active circuitry: annealing a Au layer at about 120-350 C gives about 150 down to 15 HV (Vickers); about 270 C gives about 50 HV; softer Au is preferred for bonding because it absorbs bonding stress; hardness should be < ~150 HV. These are Vickers values and do not convert directly to Knoop. — [US 8021976 (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8021976)

**Soft/thick dielectric under pad; cratering**
- IEEE abstract: Au thermosonic bonding to Al pads on thick polyimide improved when Ti was added, "attributed to the increased bond pad rigidity" (ultrasonic energy coupled better to the interface) (abstract only). — [infona.pl IEEE record](https://www.infona.pl/resource/bwmeta1.element.ieee-art-000000187617)
- Patent background: low-k (including organic) dielectrics "greatly aggravate" cratering, and thinner bond pads "cannot bear the mechanical impact" of bonding (patent background; excerpt only). — [US 8198737 (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8198737)
- Ultrasonic power and z-axis bond force are the most critical machine parameters for Si cratering, and a harder bond pad protects against cratering (Cu ball-bond study; excerpt only). — [DeepDyve: cratering on thermosonic Cu wire ball bonding](https://www.deepdyve.com/lp/springer-journals/cratering-on-thermosonic-copper-wire-ball-bonding-AdLtMnCiQl)
- Al pad thickness below about 1.0-1.2 um increases probe punch-through (Al pads, probing; excerpt only). — [SWTW 2000, McKnight](https://www.swtest.org/swtw_library/2000proc/PDF/S16_McKnight.pdf)

### Inferences
- The 6 um plated Au is far above the 100-200 nm facility minimums, so thickness alone is not the concern for the main pads. Hardness and surface cleanliness of the plated Au are open questions. Electroplated Au can be hard depending on bath and additives, and the sources say wire-bond-grade Au is soft (<= ~90 Knoop) and that annealing softens it.
- The sources point to pad stiffness and the compliance of what lies under it as what controls ultrasonic coupling and cratering. Whether 10 um PECVD SiO2 under 6 um Au behaves as "stiff" or "compliant" here is not answered by any source found. PECVD SiO2 is an inorganic glass, unlike the polyimide/low-k cases cited, so those results may not transfer.
- Sanity checks worth running (not predictions): (a) after bonding test pads, check DC continuity/isolation from each Au pad to the Al ground plane; (b) pull or shear tests on test pads of the same stack before bonding the real die; (c) confirm with the plating recipe or a hardness/anneal test whether the Au is soft-grade.

### Gaps
- No source found on Au wire bonding onto pads over thick (~10 um) PECVD SiO2 above a buried metal plane, or on dielectric cracking / pad-to-plane shorts in that geometry.
- No source found on the seed layer (Ti/Au or Cr/Au) under thick plated Au and its effect on pad peeling during bonding.
- Harman's chapters on bondability of plated Au were not accessed.

## 4. Bonding into recessed openings / wells (10 um deep, 90-170 um wide)

### Takeaway
I found no numeric clearance rule linking opening width and depth to capillary or wedge geometry. Recessed-pad wedge tools exist for pads 2-8 um below the passivation, and deep-access bonders (90 deg feed) are made for cavities. A 10 um recess is just beyond the patent's stated range.

### Cited Findings
- Wedge-tool patent: "pocket" and "open-notch" wedges for pads recessed about 2-8 um below a protective overcoat or passivation; pocket sidewalls can damage the overcoat on recessed pads, which the open-notch design avoids; the foot is designed so no other part of the wedge touches the surface. — [US7451905B2 (Google Patents)](https://patents.google.com/patent/US7451905)
- Deep-access applications may need a 90 deg wire-feed angle (wire fed through a hole in the shank); higher feed angles help deep access but give less consistent loops (tool-vendor guidance; excerpt only). — [smtnet wedge tool selection tech tip](https://dev.smtnet.com/library/files/upload/techtip2-2018.pdf)
- A double-relief vertical-hole shank gives maximum clearance from package walls (vendor listing; excerpt only). — [Jensen Tools / Small Precision Tools listing](https://jensentools.com/product/335IE4565-2004565)
- Facility bonders with deep access: Westbond 4KE is three-way convertible (45 deg wedge, 90 deg deep access, ball) — [TU Delft Kavli Nanolab](https://tudelft.nl/tnw/over-faculteit/afdelingen/quantum-nanoscience/kavli-nanolab-delft/equipment/miscellaneous/westbond-4ke); Westbond 747677E at Waterloo is convertible wedge/ball, usually set up for 1 mil Au ball — [Waterloo QNFCF](https://uwaterloo.ca/quantum-nano-fabrication-and-characterization-facility/qnc-lab-equipment-0/packaging-lab/wire-bonder-manual-wedgeball-westbond-wirebond1)

### Inferences
- For a ball bond, a capillary tip is usually wider than the ~75 um ball. In a 90 um-wide opening the capillary face may land on the surrounding SiO2 edge before the ball is fully deformed. In a 170 um opening it is less likely. This is reasoning from geometry, not a sourced number: the capillary tip diameter for the specific tool should be checked against each opening width.
- For wedge bonding, the foot (roughly 38-125 um long for 25 um wire) has to fit inside the opening along the wire direction, and the wedge heel/shank must clear the well wall.
- Sanity check worth running: get the exact capillary/wedge part number from MIT.nano staff, then draw the tool profile (tip diameter, face angle or foot length, back radius) to scale against a cross-section of each well (90 x 120 um and 170 x 170 um, 10 um deep).

### Gaps
- No verified numbers for capillary tip diameter, chamfer, or wedge foot length for the tools MIT.nano stocks.
- No source gives a rule like "opening >= X times tool tip" for recessed pads.

## 5. Bonding to thin (~200-350 nm) evaporated Ti/Au pads

### Takeaway
Facility rules accept Au pads as thin as 100 nm (EPFL) or 200 nm (UC Davis) with a Ti/Cr adhesion layer, so ~200-350 nm Ti/Au is within stated facility rules. Thinner or poorly adhered films are the main named risk, and the sources do not quantify a reliability difference.

### Cited Findings
- EPFL: minimum 100 nm pad thickness with Ti or Cr adhesion; results not guaranteed below that. — [EPFL CMi HB10 guidelines (PDF)](https://www.epfl.ch/research/facilities/cmi/wp-content/uploads/2020/04/HB10_guidelines.pdf)
- UC Davis: Au at least 200 nm (excerpt only). — [UC Davis CNM2](https://cnm2.ucdavis.edu/equipment/west-bond-7700e-ball-bonder)
- Thinner pads are more easily damaged by bonding impact (patent background, general). — [US 8198737](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8198737)
- EPFL warns that ball bonding uses an electronic flame-off spark, so "electrically sensitive samples should not be bonded with this technique". — [EPFL CMi HB10 guidelines (PDF)](https://www.epfl.ch/research/facilities/cmi/wp-content/uploads/2020/04/HB10_guidelines.pdf)

### Inferences
- The SNSPD pads (~200-350 nm Ti/Au) meet EPFL's 100 nm and UC Davis's 200 nm minimums. They sit 10 um down in 120 x 90 um openings, so the recess questions in section 4 also apply, and the 90 um dimension is the tighter one.
- The EPFL flame-off warning may matter for an SNSPD (an electrically sensitive nanowire). Wedge-wedge bonding has no spark. This is an inference from EPFL's general warning, not an SNSPD-specific source.

### Gaps
- No quantitative pull-strength or yield data found comparing ~100-350 nm evaporated Au with thick Au pads.

## 6. Cryogenic considerations (4 K)

### Takeaway
Au-Al intermetallic growth and Kirkendall voiding are driven by high temperatures (hundreds of C, or long times at about 150 C), so they are a concern for any heated bonding or bake steps, not at 4 K. I found no measured data on wire-bond fatigue under 300 K to 4 K cycling.

### Cited Findings
- Au-Al intermetallic compounds ("purple plague", AuAl2) and Kirkendall voids "have resulted in more documented wire-bond failures than any other" IC problem; voiding is faster at elevated temperature and with halides or moisture; reaction rate roughly doubles every 10-15 C (patent citing Harman). — [US 9824948 (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9824948)
- Classic void formation: bakes > 1 h at > 300 C (Au-rich side) or > 400 C (Al-rich side), or much longer at lower temperatures (patent; excerpt only). — [US 9711480 (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9711480)
- Harman, *Wire Bonding in Microelectronics*, 3rd ed. (McGraw-Hill, 2010): Au-Al intermetallics in Ch. 5 (pp. 131-153); thermal degradation of Au ball bonds on Al pads in App. 5B (pp. 170-173); extreme-temperature wire bonds in Ch. 9 (page numbers as cited in patent text; book not accessed). — [US 9935028 (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9935028)
- NIST (Josephson chips): press contacts degraded under repeated 4 K / room-temperature cycling; NIST moved to soldered flip-chip-on-flex and showed reliable cycling with 40 connections. This is not a wire-bond result. — [NIST](https://www.nist.gov/node/643911)
- Superconducting multi-chip module patents: contacts must survive 300 K / 4 K cycling, and brittle materials with mismatched thermal expansion should be avoided (applicant documents, not measurements). — [US 11121302 (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11121302)

### Inferences
- The ground-plane openings (Al M1) bonded with Au wire form an Au-Al interface. The sources say intermetallic growth is a high-temperature issue (heated thermosonic stage, any post-bond bake), so the thermal history above room temperature matters more than the 4 K operation.
- Au wire on Au pads (the main electrode pads) is monometallic and has no intermetallic issue.

### Gaps
- No measured data found on Au or Al wire-bond fatigue or pull strength after 300 K / 4 K cycling. A follow-up search could target superconducting-qubit packaging literature or the full NIST/IEEE paper (Burroughs et al., IEEE Trans. Appl. Supercond., vol. 15, no. 2; citation from search excerpt, not verified).

## 7. MIT.nano wire bonder specifics

### Takeaway
UNVERIFIED. I found no official MIT.nano page describing "Wirebond-Wedge" or "Wirebond-Ball-MEI" (model, wire diameters stocked, ball vs wedge).

### Cited Findings
- Searches for MIT.nano wire bonder pages returned no MIT.nano equipment page. One MIT MTL labnetwork mailing-list attachment appeared in results but was not checked for relevance. — [mtl.mit.edu labnetwork attachment](https://mtl.mit.edu/pipermail/labnetwork/attachments/20211214/ff4a5b57/attachment.html)
- For comparison, an MEI wedge bonder at Utah NANOFAB supports ultrasonic, thermosonic and thermocompression wedge bonding, and Al wire is most commonly used (excerpt only). — [Utah NANOFAB MEI Wedge Bonder SOP (PDF)](https://www.nanofab.utah.edu/wp-content/uploads/2023/02/MEI-Wedge-Bonder-SOP-3.pdf)
- USC's F&S Bondtec 53BDA page lists Au ball bonding with 18-25 um wire at 100-200 C stage and 20-50 g force, and Al wedge with 25-50 um wire. The page itself says it is LLM-generated and under human review, so treat these as unverified. — [USC Nanofab wiki](https://wiki.nanofab.usc.edu/index.php/Ball_%26_Wedge_bonder)

### Inferences
- The traveler's tool names suggest one wedge bonder and one MEI ball bonder. The MEI label is consistent with the Utah MEI wedge tool family, but this is not confirmed for MIT.nano.

### Gaps
- MIT.nano tool models, wire stocked (Au vs Al, 25 um vs other), tool part numbers (capillary tip diameter, wedge foot length), and stage heating limits: ask MIT.nano staff or check the internal LabRunr/Coral tool pages (login needed, not accessible here).
