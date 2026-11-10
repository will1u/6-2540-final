> **Claude-authored.** Reading pointers, not summaries. 2026-11-09.

# L3: sources for the inlaid Al mirror

This note points to sources for one process. The process: a 100 nm recess is etched into thermal SiO₂ through a LOR plus positive resist mask by fluorine RIE (CHF₃ / CF₄ / Ar). Then 100 nm of e-beam evaporated Al goes through the same mask, and lift-off leaves the Al top level with the SiO₂ beside it. PECVD SiO₂ at 300 °C or below, NbN, and Au follow. The note helps us check four points: the inlaid method itself, resist behaviour after fluorine etching, hillocks in evaporated Al during heating, and whether any trap or SNSPD group has planarized a buried ground without CMP.

Status of every source: **opened** means I fetched it and read the part named. Fetch results were summarised by a tool, not read from the typeset page, so check each number against the PDF before it goes into the report. **Search excerpt only** means I saw only a search snippet.

## A. Self-aligned recess etch plus lift-off (inlaid or buried conductors)

- Patent US 4448800 ("Method for the manufacture of semiconductor device using refractory metal in a lift-off step"). It describes recessing SiO₂, lifting off a mask, and stripping the layers to get a flat buried SiO₂ surface. This is the closest method I found, though the buried layer there is not a conductor. Read the claims and the figure sequence. (search excerpt only)
- Patent US 4396458 A ("Method for forming planar metal/insulator structures"). The title matches question A. The body was not read. Read the claims for the etch-back step and any step-height figure. (search excerpt only)
- Patent US 4532002 ("Multilayer planarizing structure for lift-off technique"). It uses a planarizing layer under the resist for lift-off. Relevant only if we add a planarizing layer. Read the lift-off layer section. (search excerpt only)
- An unnamed microelectrode paper. A snippet says traces were recessed by RIE before evaporation and lift-off. Acetone plus sonication did not remove polymer residue, which stayed in thin bands beside the traces. No author, title or journal was visible, so I cannot cite it. Find it by searching for recessed-trench electrode arrays with lift-off. (search excerpt only, unidentified)
- No source I found reports the residual step height or the edge profile (ears, fences, trenches) for this method. Gap noted under "What we could not find".

## B. Lift-off after a fluorine etch that uses the same resist

- Kayaku FAQ page on PMGI and LOR resists, https://kayakuam.com/pmgi-and-lor-resists-faqs/. Read the remover statement. It says Remover PG strips PMGI, LOR, PMMA, KMPR 1000 and minimally cross-linked SU-8. The page says nothing about resist that has been etched by plasma. That gap is the question. (opened)
- UMN bilayer lift-off page, https://apps.mnc.umn.edu/archive/ebpgwiki/BilayerProcess.html. The snippet says PMGI can leave residue after develop, which can greatly reduce lift-off yield. It suggests a few seconds of oxygen plasma before evaporation. Read the PMGI residue paragraph. I could not open this page (connection refused). (search excerpt only)
- Kayaku LOR extended abstract, https://kayakuam.com/wp-content/uploads/2019/09/LOR-Extended-Abstract-Final.pdf. The link returned HTTP 404, so the file was not read. Look for it on the vendor site. (not opened)
- Patent US 6861177 ("Method of forming a read sensor using a lift-off mask having a hardmask layer and a release layer"). A snippet says CHF₃, C₃F₈ or CF₄ etching, with a hardmask, gives high selectivity over the PMGI release layer. The snippet does not cover the top resist being hardened. Read the etch step and the lift-off step. (search excerpt only)
- The search found no source on whether a fluorine-etched, crosslinked top resist changes the lift-off outcome. The plan to test it on a witness is ours. Nothing here settles it.

## C. Hillocks in evaporated Al during heating, and resistivity

- Cambridge MRS proceedings article "Diffusional hillock formation in Al thin films controlled by creep", https://www.cambridge.org/core/journals/mrs-online-proceedings-library-archive/article/diffusional-hillock-formation-in-al-thin-films-controlled-by-creep/5BFDF2AFF4284F4389862BBD501B10B1. The abstract page was opened. The abstract is about sputter-deposited Al with trace Ti, W and O. It links hillock growth to power-law creep in the overlying film. Read the model section. Film thicknesses, annealing temperatures and any cap are not on the page, and the full text is paywalled. (opened, abstract only)
- Patent US 6348403 ("Suppression of hillock formation in thin aluminum films"), https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6348403. A snippet says a TiN cap suppresses hillocks during later heating. Read the examples for film thickness and anneal temperature. (search excerpt only)
- A 1997 IEEE paper on hillock test structures. It uses vias through a low-temperature SiO₂ layer on the Al film, read after furnace annealing, to count hillocks. This is a test method we could copy for the T10 or witness step. No authors or DOI were seen. (search excerpt only)
- Resistivity: Mayadas et al. 1968, Journal of Applied Physics, abstract page at https://research.ibm.com/publications/intrinsic-resistivity-and-electron-mean-free-path-in-aluminum-films. The abstract says the measured resistivity at 296 K is about 60 % higher than the bulk value. It also gives a maximum mean free path of about 1 µm for UHV films. The page gives no 4.2 K value, no RRR and no film thickness. Read the body for the thickness-dependent 4.2 K and RRR data. (opened, abstract only)
- Author names for the 1968 paper differ between two listings on the search results. Check the journal before citing. (search excerpt only for the listing)
- A companion evaporated-films paper, "Resistivity and Structure of Evaporated Aluminum Films", https://scilit.com/publications/d030a27dea51e2bca7942714d3f32b82. A snippet says the intrinsic resistivity depends on film thickness through grain size, and gives RRR as a function of thickness. Read the thickness table in the full text. (search excerpt only)
- A search snippet gives a 4.2 K resistivity for a film near 100 nm. I did not open the source, so I have not used that number here. Read the source before quoting any value.

## D. Planarized or buried ground in ion-trap or SNSPD cavities without CMP

- Hampel et al., Appl. Phys. Lett. 122, 174001 (2023), arXiv:2302.01462, https://arxiv.org/html/2302.01462v1. Read the fabrication paragraph and the Fig. 2 discussion. The paper uses a 50 nm electron-beam evaporated Al mirror patterned by lift-off under SiO₂. It makes no mention of planarization or step height. Vias are etched through the SiO₂ with CHF₃ and covered with 20 nm Au, and the 350 nm Au electrode layer contacts the mirror there, which matches our mirror ground via. The NbTiN is co-sputtered at 500 °C on the SiO₂ over the Al, which bears on question C: a 50 nm evaporated Al film under SiO₂ went through a hotter step than our 300 °C. The Fig. 2 text says the rf field around the nanowire is reduced by about an order of magnitude with the grounded mirror. Read the Fig. 3 discussion for the grounded-mirror behaviour. (opened; the arXiv v1 text was also read in full on 2026-11-09 for DESIGN_LOG step 37. The page gives no section numbers, so use the paragraph names above)
- Todaro et al., Phys. Rev. Lett. 126, 010501 (2021), arXiv:2008.00065. Already opened in L2. Its electrodes are 6 µm electroplated Au on PECVD SiO₂. It does not describe a planarized or buried ground. (opened in L2, not re-read here)
- Bautista-Salvador et al. (2019), arXiv:1812.01829. Already opened in L2. It is useful for gap aspect ratio but does not describe a buried ground. (opened in L2, not re-read here)
- I found no trap or SNSPD source that describes a planarized buried ground made without CMP.

## What we could not find

- Step height or edge profile reported for any recessed-lift-off or inlaid thin-film method (question A).
- Any source on whether a fluorine-etched, crosslinked top resist changes lift-off (question B). The UMN bilayer page could not be opened.
- Hillock data for evaporated Al at about 100 nm, with or without a SiO₂ cap, at 300 °C or below (question C). The hillock sources above are sputtered films or abstract-only.
- A 4 K residual resistivity ratio for evaporated Al at about 100 nm (question C).
- A planarized buried ground in an ion-trap or SNSPD device without CMP (question D).
- Full text of the Cambridge hillock paper (paywalled) and of the Kayaku LOR abstract (HTTP 404).
- The unnamed microelectrode paper (question A). Its authors and year must be found before it can be cited.

## Where a source differs from the process described above

- No source contradicts the process directly. None of the sources reports an inlaid mirror, so none can confirm or refute it.
- Hampel's mirror is 50 nm, lift-off on flat SiO₂. Our process is 100 nm inlaid. The difference is in thickness and in the recess, not a conflict.
- Hampel's numbers that look inconsistent are not. The 150 nm PECVD SiO₂ is under the mirror and the 212 nm SiO₂ is between the mirror and the NbTiN. The 100 nm wire on a 160 nm pitch is the simulated geometry of Fig. 2; 90 nm on a 180 nm pitch is what they measured by SEM. (Corrected on review against the arXiv v1 text.)
- The Kayaku remover statement covers only minimally cross-linked SU-8. Our process etches the top resist, then lifts it off. No source covers that step, so the step is unverified, not contradicted.
- The hillock sources concern sputtered Al. Our film is evaporated, so they do not cover our case.

## Proposed bib entries

No new BibTeX entries are proposed this round. The sources I opened either lack fields I can confirm (the 1968 Mayadas paper has conflicting author listings, and the Cambridge page shows no authors), or are already in the bib (Hampel 2023, Todaro 2021). Hampel's author list and DOI come from L2, not from this session. Add the entries once the full texts are read.

## Source table

| Short name | Full citation as found | Link | Opened or excerpt only | What to read |
|---|---|---|---|---|
| Hampel 2023 | B. Hampel et al., Appl. Phys. Lett. 122, 174001 (2023); arXiv:2302.01462 | https://arxiv.org/html/2302.01462v1 | opened (summarising fetch) | Fabrication paragraph (50 nm Al lift-off, 20 nm Au via); Fig. 2 text; Fig. 3 grounded-mirror discussion |
| Kayaku FAQ | Kayaku Advanced Materials, "PMGI and LOR resists FAQs" | https://kayakuam.com/pmgi-and-lor-resists-faqs/ | opened | Remover statement (PMGI, LOR, PMMA, minimally cross-linked SU-8) |
| UMN bilayer | UMN Nanofabrication archive, "PMMA/PMGI Bilayer E-Beam Liftoff Process" | https://apps.mnc.umn.edu/archive/ebpgwiki/BilayerProcess.html | excerpt only (page refused) | PMGI residue paragraph; oxygen plasma before evaporation |
| Kayaku LOR abstract | Kayaku Advanced Materials, LOR extended abstract | https://kayakuam.com/wp-content/uploads/2019/09/LOR-Extended-Abstract-Final.pdf | not opened (HTTP 404) | Look for it on the vendor site |
| US 6861177 | "Method of forming a read sensor using a lift-off mask having a hardmask layer and a release layer" (US patent 6,861,177) | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6861177 | excerpt only | Fluorine etch step with hardmask over PMGI; lift-off steps |
| US 4448800 | "Method for the manufacture of semiconductor device using refractory metal in a lift-off step" (US patent 4,448,800) | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4448800 | excerpt only | Recess, lift-off mask and buried flat SiO₂ sequence; figures |
| US 4396458 A | "Method for forming planar metal/insulator structures" (US patent 4,396,458 A) | https://patents.google.com/patent/US4396458A/en | excerpt only | Claims for the etch-back step; step-height figure |
| US 4532002 | "Multilayer planarizing structure for lift-off technique" (US patent 4,532,002) | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4532002 | excerpt only | Lift-off layer and planarizing layer section |
| Microelectrode paper | Authors, title and year not seen | none | excerpt only, unidentified | RIE-recessed traces, lift-off residue; find first |
| Hillock, creep model | "Diffusional hillock formation in Al thin films controlled by creep", MRS Online Proceedings Library (authors and year not shown) | https://www.cambridge.org/core/journals/mrs-online-proceedings-library-archive/article/diffusional-hillock-formation-in-al-thin-films-controlled-by-creep/5BFDF2AFF4284F4389862BBD501B10B1 | opened (abstract only; paywalled) | Creep model section; thickness and anneal data in full text |
| US 6348403 | "Suppression of hillock formation in thin aluminum films" (US patent 6,348,403) | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6348403 | excerpt only | TiN cap examples; film thickness and anneal temperature |
| Mayadas 1968 (resistivity) | Mayadas et al., J. Appl. Phys., 1968; author names differ between listings | https://research.ibm.com/publications/intrinsic-resistivity-and-electron-mean-free-path-in-aluminum-films | opened (abstract only) | Body text for 4.2 K and RRR versus thickness |
| Evaporated Al films | "Resistivity and Structure of Evaporated Aluminum Films" (authors not shown in excerpt) | https://scilit.com/publications/d030a27dea51e2bca7942714d3f32b82 | excerpt only | Thickness table for RRR |
| Todaro 2021 | S. L. Todaro et al., Phys. Rev. Lett. 126, 010501 (2021); arXiv:2008.00065 | https://arxiv.org/html/2008.00065v1 | opened in L2 (not re-read) | Sec. I.1 electrode process; no buried ground |
| Bautista-Salvador 2019 | arXiv:1812.01829 | https://arxiv.org/pdf/1812.01829 | opened in L2 (not re-read) | Gap aspect ratio; no buried ground |
