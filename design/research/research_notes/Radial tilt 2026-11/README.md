> **Claude-authored.** Reading pointers for the radial-tilt question (beams parallel to the chip, tilted radial principal axes, per-mode Doppler cooling, vertical micromotion). Pointers only, no summaries. Sections and equations are as printed in the PDF pages I opened; anything not checked is tagged [verify].

# Radial tilt: reading pointers

**Status (2026-11-10):** written by a delegated agent from the pages it opened. The orchestrator checked Allcock 2010 pp. 2–5 against the PDF; every other number here is still [verify]. Itano & Wineland 1982 (the per-mode Doppler formula) was not opened.

## Questions

1. How large a principal-axis tilt do real surface traps use, and how is it made (DC voltages, or asymmetric RF electrodes)?
2. What is the Doppler cooling rate and Doppler limit for a beam at an angle to a mode?
3. Why must the radial modes be non-degenerate?
4. With every beam parallel to the surface, how do surface-trap groups detect and compensate vertical (out-of-plane) excess micromotion?

## Where to read

| Source | Link | Where to read (as printed) | What it answers |
|---|---|---|---|
| Allcock et al. 2010, NJP 12 053026 (arXiv:0909.3272) | https://arxiv.org/abs/0909.3272 | Sec. I.A p.1 (split centre axial electrode rotates the modes); Sec. I.B p.2 and Fig. 2 (tilt basis, tilt angle 45° with degeneracy lifted, est. 42°), Table II p.2; Table III p.5 (tilt factor vs modelled angle); Sec. IV p.6 (Eq. 4; out-of-plane repumper; Fig. 9) and Sec. IV.A p.6-7 | Q1 (split-centre DC tilt, numbers), Q3 (degeneracy broken by tilt), Q4 (repumper-based out-of-plane micromotion compensation) |
| Romaszko et al. 2019, technical review (arXiv:1908.00267) | https://arxiv.org/abs/1908.00267 | Box 2 p.4 (laser parallel to surface at 45°); Sec. 2.2 "Rotation of principle axes" p.5 and Fig. 2.1 (RF-width and DC-rotation methods; 45° out-of-plane angle) | Q1 (both methods, 45° claim as a review statement) |
| Labaziewicz et al. 2007, arXiv:0706.3763v2 | https://arxiv.org/abs/0706.3763 | Fig. 1 caption p.2 (notch tilts principal axes 6° to 20°); text p.2 (DC voltage ratio) | Q1 (cryogenic example of a small tilt); no 37.5° value found |
| Zhang, Mehta, Home 2022, NJP 24 073030 (arXiv:2201.12579) | https://arxiv.org/abs/2201.12579 | Intro p.2 (SE traps lack mirror/rotation symmetry perpendicular to surface); Sec. 2 outline only (2.2-2.4) | Q3 background only; the degeneracy-vs-rotation passage was not read |
| Chiaverini et al. 2005, QIC 5, 419 (arXiv:quant-ph/0501147) | https://arxiv.org/abs/quant-ph/0501147 | Sec. 1-2 pp.419-421 only | No axis-rotation or surface-beam cooling content found in those pages; rest not read |
| Niedermayr et al. 2014, NJP 16 113068 (arXiv:1403.5208) | https://arxiv.org/abs/1403.5208 | Abstract page only | Not opened (see below) |
| Wineland et al. 1998, J. Res. NIST 103, 259 (arXiv:quant-ph/9710025) | https://arxiv.org/abs/quant-ph/9710025 | Sec. 2.1-2.3 pp.3-17 (pseudopotential, motional states); Sec. 3.1 not reached | Q2 not answered: the cooling-rate equation was not located |
| Berkeland et al. 1998, J. Appl. Phys. 83, 5025 (DOI 10.1063/1.367318) | https://doi.org/10.1063/1.367318 | Title page; Sec. II pp.5025-5026, Eq. 13 p.5026 (Doppler limit T_D = ħγ/2k_B for secular motion in one direction) | Q2 (Doppler limit per direction); the "micromotion detected only along k" statement was not located on pp.5025-5026 |
| An et al. 2018, arXiv:1807.06043v1 | https://arxiv.org/abs/1807.06043 | Abstract p.1; Sec. II p.2 (rf-null axis, tilt of the vertical mode into the plane, ion height via fluorescence) | Q1, Q3, Q4 (vertical micromotion in a surface trap; tilt used to couple the near-vertical mode) |
| Arnold et al. 2019, arXiv:1905.06523v3 | https://arxiv.org/abs/1905.06523 | Abstract p.1 (branching p, lifetime tau); Introduction p.1; Sec. II p.2 (beam geometry, p=0.267979(21)); Fig. 1 p.1 (493 nm and 650 nm levels) | Q2 input: 6P1/2 lifetime and branching for the linewidth |

Derived values (run in a script, not quoted from a paper): see the Arnold note.

## Not opened, or only seen as a search excerpt

- **Itano & Wineland 1982, Phys. Rev. A 25, 35** (DOI 10.1103/PhysRevA.25.35, from the search result only). Not opened. The Zenodo link returned by search (`zenodo.org/records/1282096`) is a different paper: Itano et al., "Time and frequency standards based on charged particle trapping", IEEE Trans. Nucl. Sci. NS-30 no. 2, p.1521 (1983). Do not cite that record for the 1982 paper. No per-mode cooling-rate equation was found. Q2 is still open.
- **Niedermayr et al. 2014, arXiv:1403.5208.** Only the abstract page was read. The body was too large for the fetch tool. The unequal-RF-width statement (item 4) was not verified. A search excerpt claimed a tilt of about 20°; unverified.
- **37.5° cryogenic tilt paper (item 6).** Not found after two searches. Search excerpts mention other angles, none of them opened: arXiv:1901.11250 (double wells with axes at ±35°, not stated as cryogenic); arXiv:1906.06489 (5° tilt, 397 nm beam); arXiv:0812.3907 (review, axes not perpendicular to surface); a 2025-era APS PRA paper (DOI 10.1103/mghd-1ffl) giving 45-50° optimal cooling angle in higher-dimensional crystals. All of these are search excerpts only.
- **Leibfried et al. 2003, Rev. Mod. Phys. 75, 281.** Not opened; not searched in this pass.
- **Berkeland "micromotion detection only along k".** Not located on pp.5025-5026; the Doppler-shift detection section was not read.
- **Chiaverini 2005 and Zhang/Home 2022**: only the pages listed above were read.
- **Ba+ 493 nm linewidth (item 11).** The search excerpt "Gamma/2pi = 15.3 MHz" was not confirmed. The primary-source lifetime from Arnold et al. gives a different derived number; see the Arnold note.
- **Allcock 2010, Sec. IV micromotion table and figure beyond p.7**: read, not every figure.
