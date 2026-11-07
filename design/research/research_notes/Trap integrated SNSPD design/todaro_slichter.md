# Todaro et al. 2021 (PRL 126, 010501) trap-integrated SNSPD and Slichter et al. 2017 (Opt. Express 25, 8705): design extraction

**Sources read in full (verified IDs):**
- [T-PRL] S. L. Todaro, V. B. Verma, K. C. McCormick, D. T. C. Allcock, R. P. Mirin, D. J. Wineland, S. W. Nam, A. C. Wilson, D. Leibfried, D. H. Slichter, "State readout of a trapped ion qubit using a trap-integrated superconducting photon detector," Phys. Rev. Lett. 126, 010501 (2021). DOI 10.1103/PhysRevLett.126.010501 (checked on Crossref). arXiv:2008.00065. arXiv has only v1 (31 Jul 2020), and that PDF includes the full Supplemental Material on pp. 8–15. PRL dates: received 3 Aug 2020, published 6 Jan 2021. — [arXiv](https://arxiv.org/abs/2008.00065), [PRL](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.126.010501). I read the arXiv v1 text. I could see the PRL abstract page but not the published body text. The abstract numbers (F = 0.9991(1), 46 µs) are the same in both.
- [T-Thesis] S. L. Todaro, *Improved State Detection and Transport of Trapped Ion Qubits for Scalable Quantum Computing*, Ph.D. thesis, Univ. of Colorado Boulder (2020). This is ref. [43] of the PRL. — [NIST PDF](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- [S-2017] D. H. Slichter, V. B. Verma, D. Leibfried, R. P. Mirin, S. W. Nam, D. J. Wineland, "UV-sensitive superconducting nanowire single photon detectors for integration in an ion trap," Opt. Express 25, 8705 (2017). DOI 10.1364/OE.25.008705 (checked on Crossref). arXiv:1611.09949 (I read v2, 10 Apr 2017). — [arXiv](https://arxiv.org/abs/1611.09949)

Notation: "Supp." means the PRL Supplemental Material (arXiv v1 pp. 8–15). Page numbers for the thesis are its printed page numbers.

---

## 1. Electrode layout around the detector (window/opening, sizes, recess)

### Takeaway
The SNSPD does not sit under the rf electrodes or under a gap in them. It sits in a rectangular recessed pocket (an opening) in the **central DC electrode region between the two rf rails**. That pocket is bounded by two center-right DC electrodes, **CUR and CLR**, which sit just past the end of the two center-left DC/microwave electrodes (CUL, CLL). The pocket is about 83 µm before the rf rails terminate. The meander is **22 µm × 20 µm** (110 nm wires on a 170 nm pitch, wires parallel to the trap axis). It lies on the substrate floor, recessed **6 µm** below the top of the 6 µm electroplated Au electrodes.

### Cited Findings
- **Electrodes named in the thesis layout.** Thesis Fig. 4.8 (p. 61) names the electrodes:
  - DC1–DC9 on the top side and DC10–DC18 on the bottom side are the outer segmented DC electrodes (blue).
  - Two red rf rails.
  - Two purple center electrodes, "CUL/µwave1" and "CLL/µwave2", fill the central strip between the rf rails, left of the detector.
  - Two blue center electrodes, "CUR" and "CLR", flank the SNSPD pocket and the lead channel on the right.
  - SNSPD in green, leads in yellow. — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Electrode count and gaps.** The "detector trap" has 24 electroplated Au electrodes, 6 µm thick, with 3–4 µm gaps between them, on a 350 µm thick intrinsic Si substrate. The thesis says the high aspect ratio shields the ion from stray charge on the substrate (Sec. 4.2.1.2, p. 60). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Trap type.** It is a "five-wire" linear surface trap. RF on the two rf electrodes makes an rf null about 39 µm above the surface along the x axis. The blue and purple electrodes provide axial DC confinement, stray-field compensation and secular-mode tuning. Either purple electrode can act as a microwave antenna (non-resonant and double-ended, with DC wirebonded to one end and microwave to the other) (Sec. 4.2.1.2, pp. 61–62, Fig. 4.10). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Electrode roles in the PRL.** The rf electrodes (pink) give transverse confinement. The surrounding segmented electrodes (grey) hold the ion at adjustable positions along the rf null. An "integrated current-carrying electrode" between the rf electrodes makes microwave magnetic fields for qubit control (PRL p. 2, Fig. 1). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **What the SEM shows.** Thesis Fig. 4.9(a) (p. 62) is a false-color SEM. It shows the green SNSPD on the floor of a pocket whose walls are the blue electroplated DC electrodes (CUR/CLR), with yellow leads around the active area. The purple CUL/CLL electrodes are on one side and pink rf rails on both sides. Caption: "ion is trapped 35(1) µm above the detector surface," "effective numerical aperture (NA) of 0.32." — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Meander and recess.** Supp. "Trap fabrication": the meander covers "an active area of 22 µm × 20 µm, with nanowires of 110 nm width on a 170 nm pitch, aligned with the trap axis." The PRL main text (p. 2) says the SNSPD is "recessed another 6 µm below this plane," meaning below the top surface of the electrodes. The thesis writes the area as "20 × 22 µm" (p. 62 and p. 107). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Electrode and lead thicknesses.** The trap electrodes are 6 µm thick electroplated Au. The SNSPD contacts and leads are 5 nm Ti + 50 nm Au, plus another 350 nm Au on the leads only (Supp. "Trap fabrication"). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Narrow leads.** The SNSPD leads are "much narrower than typical SNSPD leads." This was chosen "to minimize capacitive coupling to the trap rf electrodes." The extra 350 nm Au lowers series resistance to prevent latching (Supp. "Trap fabrication"). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Lead routing.** In PRL Fig. 1(b), the yellow leads leave the pocket toward the trap end (away from zones A–C), along the trap axis, in the central channel between the rf rails. In the thesis they run between CUR and CLR (Fig. 4.8). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Previous-generation meander.** Thesis Fig. 4.9(b) (from S-2017) shows the meander floor. It is framed by a thin evaporated Ti/Au contact layer, with the much taller electroplated electrodes next to it. — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Detectorless "transport trap".** It is identical except that "an evaporated gold electrode" (50 nm thick) replaces the SNSPD. That electrode is named "det" and is grounded when the detector-trap voltage sets are reused (Sec. 4.2.1.3, Fig. 4.11; App. B; Sec. 5.3.1). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)

### Inferences
- **Dimensions measured from figures.** The numbers below are my pixel measurements of PRL Fig. 1(b), which the caption calls a "top view scale diagram." I calibrated with the 100 µm scale bar and checked against the stated 264 µm A–D distance, which comes out at 265 µm. Thesis Fig. 4.8 (2.97 px/µm) gives the same numbers to within a few µm. Expect about ±2–3 µm error, and the drawn gaps may be exaggerated.
  - **RF rail width:** about 47 µm (both figures: 46.5–47 µm).
  - **Center channel at zones A–C:** about 57–58 µm between rf inner edges. In thesis Fig. 4.8 the purple CUL+CLL block is about 50 µm wide, with about 2–4 µm gaps to the rf.
  - **Center channel past the detector:** the rf inner edges step inward, so the channel narrows to about 44–45 µm. The rf rails widen to about 51–53 µm there.
  - **RF termination:** the rf rails end about 83–85 µm past the detector center (thesis Fig. 4.8: 83 µm; PRL Fig. 1(b): about 85 µm). Large end DC electrodes (DC9/DC18) lie beyond them.
  - **Pocket (opening in CUR/CLR):** about 50 µm along the axis by about 42 µm transverse (PRL Fig. 1(b)). A rim of DC electrode about 3.5–5 µm wide surrounds it inside the channel.
  - **Green rectangle as drawn:** about 34 µm along the axis by about 24 µm transverse. This is larger than the 22 × 20 µm active area, so the drawing probably shows the MoSi rectangle plus margin rather than the meander. Treat it as approximate.
  - **Leads:** two leads, each about 2–3 µm wide, about 4–5 µm center to center.
  - **Gap between CUL/CLL and CUR/CLR:** the microwave electrodes end about 33–35 µm before the detector center, and a single gap separates them from the CUR/CLR rim.
- **Answer to "which electrode sits around or over the SNSPD":** no electrode metal is over the detector. The SNSPD is in an opening of the grounded/DC center electrodes (CUR/CLR), not under or between the rf electrodes. The rf rails pass alongside at about 47 µm width and terminate about 83 µm downstream.
- **Wire orientation.** Thesis Table B.1 lists separate DC voltages for CUR and CLR, so they are DC-biased electrodes. The paper calls the nanowires "aligned with the trap axis," and Supp. Fig. S6 says they are "parallel to the trap axis." So the 22 µm side is probably along the axis, but no source states this.

### Gaps
- None of the sources gives an exact GDS-level dimension for the pocket opening, the CUR/CLR rim width, the rf rail widths, the gap widths, or the DC segment widths. Every number above comes from figure measurement.
- No source states the potential applied to CUR/CLR during readout. Table B.1 gives zone-8 values only to two decimals, and the unlabeled last row is ambiguous.
- No source says whether the 22 µm or the 20 µm side lies along the axis.

---

## 2. Ion height: nominal vs over the detector, and what causes the drop

### Takeaway
The ion height is ≈39 µm above the electrode top plane away from the detector and ≈29 µm when centered over it, which is 35 µm above the recessed SNSPD. The PRL says only that it drops "by design." The thesis attributes the drop to rf-electrode end effects plus the breakdown of the planar (2D) approximation over the recess. Neither source attributes it to any field from the SNSPD. Your hypothesis is therefore **partly supported**. The boundary-geometry (recess) part is one of the two stated causes, but the thesis names rf end effects first.

### Cited Findings
- **PRL main text (p. 2).** The ion is held "≈ 39 µm above the top surface plane of the trap electrodes, dropping by design to a smaller distance of ≈ 29 µm above this plane when centered over the SNSPD." It then says the SNSPD "is recessed another 6 µm below this plane." PRL Fig. 1(a) labels "39 µm" at the far zone and "35 µm" from the ion over the SNSPD down to the detector. — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Thesis Sec. 4.2.1.2 (p. 62).** The rf null "is not uniformly 39 µm from the trap." Paraphrase: because of end effects, it curves about 10 µm closer to the surface toward the right-hand end, which is the detector end. — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Thesis Sec. 6.3 (p. 113).** The ion drops "to 29 µm above the electroplated gold when centered over the detector" (35 µm from the SNSPD). Stated cause: "a combination of end-effects from the end of the RF electrodes" together with failure of the Biot–Savart (planar) analog. That analog assumes all electrodes lie in one 2D plane. The thesis says it fails over the detector, where the electrode height difference is large on the scale of the ion height. — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Thesis Fig. 6.3 caption (p. 114).** The ion moves "∽10 µm closer to the trap surface over the detector" because of the end of the RF electrode and because the 2D-surface approximation breaks down. — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **How height was measured (Supp. "Experimental apparatus").** Ion height and lateral distance were measured at each ion position by scanning the readout beam with motorized lenses, both parallel and perpendicular to the surface. The surface plane was found from a Gaussian fit to the light scattered off the trap. Uncertainty is about 1 µm in height and about 3 µm laterally, and the electrode surface roughness is about 100 nm peak-to-peak. — [T-PRL](https://arxiv.org/abs/2008.00065)
- **SNSPD bias timing.** The bias current "is applied only during readout and is off at other times" (PRL p. 3). With the trap rf on, rf-induced currents flow in the nanowire regardless. — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Earlier ring-trap design.** S-2017's ring-shaped test trap puts the rf pseudopotential well "48 µm above the center of the MoSi rectangle" (S-2017 Sec. 3 and Fig. 2 caption). — [S-2017](https://arxiv.org/abs/1611.09949)

### Inferences
- **Hypothesis test.** "The drop is caused by the absence of electrode metal over the detector, not by any field from the SNSPD."
  - Not-SNSPD-field: **consistent with the sources.** No source mentions an SNSPD-generated DC field as a cause. The thesis explanation is purely electrode geometry.
  - Absence-of-metal / recess: **partially consistent.** The thesis's second cause is the non-planar recess (the 2D model fails because the 6 µm step is large compared with the ion height). Its first cause is the rf rails terminating (end effects).
- **Likely third contributor (my inference, not stated):** the rf inner edges step inward right of the detector (channel about 57 → about 45 µm). A narrower rf gap lowers the rf-null height in a five-wire trap.
- "By design" suggests the designers expected and modeled the drop. No source gives the design rationale beyond the height and NA numbers.
- **Geometry check (my calculation).** A 20 × 22 µm rectangle seen from 35 µm above its center subtends Ω ≈ 0.33 sr. That equals a cone of NA ≈ 0.32, so the PRL's "NA 0.32" and the thesis's "0.32 steradians" (p. 107) agree numerically.

### Gaps
- **No h(x) plot or table** appears in the PRL, the Supp., or the thesis. Only the end points (39 and 29 µm) are given. The Fig. 1(a) rendering shows the trend qualitatively. The per-position measured heights used for Fig. 4 are not tabulated.
- No simulation separating the end-effect and recess contributions is given.

---

## 3. Trap zones, transport, DC segmentation, rf drive, secular frequencies, species, lasers

### Takeaway
The PRL labels four zones, **A–D**: A is the load zone, 264 µm from the SNSPD center, and D is directly over the SNSPD. The thesis labels seven zones, **2–8**, on about a 44 µm pitch; zone 2 is the load zone and zone 8 is over the detector. Ions of 9Be+ are loaded far from the detector and transported with time-varying potentials on the segmented outer DC electrodes. The rf is 8.8 V peak at 67.03 MHz. Secular frequencies are about 2 MHz axial and 5–10 MHz radial.

### Cited Findings
- **Zone positions.** Zones run "from directly over the SNSPD (zone D) to 264 µm away from the SNSPD center (zone A)" (PRL p. 2). "Ion loading occurs in trap zone A, 264 µm from the SNSPD center." The ion is transported to zone D "using time-varying potentials on the segmented outer electrodes" (PRL p. 3). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Thesis zone numbering.** Ions are loaded in "Zone 2 or 3, as labelled on Figure 4.8" (Sec. 5.3.1, p. 101). The thesis says ions are loaded at the end farthest from the SNSPD, with "no line-of-sight to the detector" (Sec. 6.3, p. 113). The Doppler-cooled lifetime is "days" both in the load zone and over the detector. — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Voltage sets.** Thesis App. B, Table B.1, gives DC voltage sets for a 2.0 MHz axial well in each of zones 2–8, using electrodes DC1–DC18, CUL, CLL, CUR, CLR plus one unlabeled row (simulated with the Biot–Savart method). Loading RF power is typically 6.0–9.0 dBm. — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Laser geometry.** All laser beams and B0 "lie in the plane of the trap at 45° angles to the trap axis." Beams can be translated horizontally to follow the ion between zones. Fig. 1(b) shows the "cooling/readout" beam and two Raman beams aimed at zone D (PRL Fig. 1 caption). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Species and transitions.** 9Be+. B0 = 0.56 mT, in plane at 45° to the axis, with no discernible effect on the SNSPD. The qubit is |F=2,mF=−2⟩ and |F=1,mF=−1⟩, ω0/2π ≈ 1.260 GHz. Optical pumping and readout use 2S1/2–2P3/2 at 313 nm; readout uses the cycling transition to |2P3/2, F=3, mF=−3⟩. Shelving to |F=1,mF=1⟩ is done with microwave pulses on the trap-integrated microwave electrode. Raman beams are detuned 80 GHz blue of 2S1/2–2P1/2 at 313 nm (PRL pp. 2–3). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Motional frequencies and rf drive.** Typical motional frequencies are "∼2 MHz" axial and "5 MHz to 10 MHz" radial. RF peak amplitude is 8.8 V at 67.03 MHz (PRL p. 2). Over the detector the heating measurement used a 5.3 MHz axial mode (5.34 MHz in thesis p. 127). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **RF resonator.** A critically coupled cryogenic LC resonator with a 315 nH PCB toroidal inductor. Loaded Q is 169 at 4 K, step-up is 18.5, and drive power is about 3 mW (Supp. "Experimental apparatus"). The thesis adds that trap capacitance is 6 pF, the coupling capacitor 1.5 pF, the shunt 12 pF, and total C 18 pF. Z = 132 Ω, f ≈ 67 MHz, and 7.4–11.6 V amplitude is reachable (Sec. 4.2.6.1, pp. 73–74). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Loading.** Resonance-enhanced two-photon photoionization at 235 nm (a frequency-quadrupled cw Ti:sapphire) from a thermal Be flux. All 313 nm beams come from frequency-doubled, sum-frequency IR fiber lasers (Supp.). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Cryogenics.** A closed-cycle cryostat at ≈3.5 K. Base trap temperature was as low as 3.45 K and drifted to 3.57 K over months (Supp.). The thesis says the trap runs 0.45 K above the cold head (Fig. 4.6). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Chip shape.** DRIE-patterned "bowtie" substrate, with the active trap area on a 1.8 mm-wide central isthmus, so focused beams are not clipped (Supp., Fig. S1). — [T-PRL](https://arxiv.org/abs/2008.00065)

### Inferences
- **DC segment pitch.** From PRL Fig. 1(b) and thesis Fig. 4.8 the outer DC segment pitch is about 44 µm, and the thesis zone pitch is about 44 µm (zones 2 → 8 = 265 µm ≈ 6 × 44 µm). So thesis zone 2 corresponds to PRL zone A and zone 8 to zone D. There are 9 outer DC electrodes per side (DC1–9, DC10–18). The end ones (DC9/DC18) are large electrodes past the rf termination.
- **Positions of B and C.** The marker positions in PRL Fig. 1(b) put B about 176 µm and C about 74 µm from D, but these look schematic, so I can't map them reliably to the thesis zones. The thesis measures zone-3 heating, while the PRL reports zone-B heating.
- **Where cooling and Raman operations happen.** Doppler cooling and readout are done at zone D. Raman sideband cooling was not achievable over the detector (Section 4), so Raman operations are best done in zones A–C. The PRL suggests this for a large-scale processor (p. 4).

### Gaps
- No transport waveform details (durations, speeds) for the detector trap are given in the PRL. The thesis transport chapter (Ch. 7) uses the detectorless "transport trap," which I did not extract.
- No exact DC segment widths or gap counts are given in text. Total segments: the thesis says 24 electrodes total.
- No well depth for the linear trap is given.

---

## 4. Micromotion/stray fields at the detector; effects of SNSPD bias and clicks on the ion

### Takeaway
Neither source reports a detector-specific micromotion or stray-field number. Generic compensation methods and typical stray fields are given in the thesis. The SNSPD does affect the ion in three ways:
- **Heating rate:** the axial heating rate over the SNSPD is 113(14) q/s at 5.3 MHz, versus 63(6) q/s at 2 MHz in zone B. That is about 6× the scaled field noise.
- **Click kicks:** each click gives an impulsive "kick" of about 0.009–0.010 quanta per click.
- **Clicks with bias off:** stray-light clicks still occur with the bias off when rf is on. This blocked Raman sideband cooling over the detector.

### Cited Findings
- **Heating rates.** Zone B: 63(6) quanta/s at ω/2π = 2 MHz, scaling as ω^−1.7(7). Zone D, over the SNSPD: 113(14) quanta/s at 5.3 MHz. Assuming d^−4 scaling, the scaled E-field noise over the SNSPD is "roughly 6 times higher" than over the gold. The cause is unclear: the wideband bias line, SNSPD materials, or something else (PRL p. 4). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Thesis heating values.** 108(14) quanta/s over the detector. S_E(ω) = 1.56 × 10^−5 V²/m² (as printed; units probably V²/m²/Hz). The ion was Doppler cooled to n̄ ≈ 2 at ω_ax = 5.34 MHz (Sec. 6.6, p. 127). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Click kick mechanism.** During a pulse, part of the nanowire stays at ground while the rest tracks the output voltage. This gives an impulsive electric-field "kick" to the ion. During readout this is negligible next to laser scattering. During Raman operations, stray-light SNSPD pulses can dominate heating (PRL p. 4). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Clicks with bias off.** "Even when the bias current is off, the SNSPD will occasionally pulse in response to photons when the trap rf is on." Measured: 0.009(5) quanta per SNSPD count on the 5.3 MHz axial mode in zone D. This limited Raman sideband cooling over the SNSPD (PRL p. 4). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Thesis heating-per-click measurement.** 0.010(4) quanta per click (Fig. 6.12). The most intense off-resonant Raman beam tested gave 21 clicks/ms, yet that was 300–1000× below the normal sideband-cooling power. The thesis estimates 3–10 quanta/ms during sideband pulses. Its 25 × 10 µs pulses would add 0.75–2.5 quanta (Sec. 6.6, pp. 127–128). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Why bias is gated.** The bias is gated only to readout because "detector pulses may introduce electric field noise at the ion." It is ramped on and off over 11 µs to limit bias-tee ringing and capacitive coupling to other electrodes (thesis Sec. 6.3.1, p. 114; Supp.). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis), [T-PRL](https://arxiv.org/abs/2008.00065)
- **Stray fields and compensation (generic, not detector-specific).** Typical stray fields were |E_s,x|, |E_s,y| ≈ 300 V/m and |E_z| ≈ 750 V/m. Radial micromotion in the plane is minimized by scanning a y shim to maximize fluorescence. Out-of-plane (z) micromotion is minimized using microwave micromotion sidebands from the microwave-antenna field gradient. Axial stray field is found by checking for position shifts under curvature changes. Stray fields drift over 12–24 h after loading, attributed to 235 nm light and loading charge (Sec. 5.3.2, pp. 101–103). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Fidelity limit related to rf.** Readout fidelity is partly limited by "trap-rf-induced state mixing" of the cycling transition (PRL p. 4). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Exposed dielectric.** A large exposed-dielectric area tends to accumulate stray charge, so a transparent shielding electrode (film or mesh) would be needed over any dielectric coat (Supp. "Trap fabrication"). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **a-Si cap.** S-2017: the 2 nm a-Si cap is thin enough that stray charge should tunnel to the MoSi, so it does not charge up (Sec. 3). — [S-2017](https://arxiv.org/abs/1611.09949)
- **Cancellation tone and the ion.** S-2017: the rf voltage across the SNSPD from a cancellation tone is about 10^5 times smaller than on the rf electrode, so no significant effect on the ion is expected (Sec. 4). — [S-2017](https://arxiv.org/abs/1611.09949)

### Inferences
- The SNSPD floor is an unshielded area of MoSi, a-Si, and SiO2 at 6 µm depth. Its stray-charge behavior was evidently tolerable: lifetimes of days and readout F = 0.9991. No micromotion penalty at zone D is reported.

### Gaps
- No measured micromotion amplitude, compensation-field values or stray field specifically at zone D appear in the PRL, Supp. or thesis.
- No measurement of a DC field or ion displacement when the bias is switched on or off.

---

## 5. SNSPD material, fabrication, RF pickup and filtering, proposed fixes

### Takeaway
The detector is 8 nm amorphous Mo0.75Si0.25 with a 2 nm a-Si cap (Tc = 5.2 K) on 134 nm SiO2 on Si. The nanowire was patterned **before** the 6 µm Au electroplating.
- **RF effect:** the trap rf cuts the usable bias I_m from the 8.9 µA switching current by about 3.6 µA, to 5.3 or 4.8 µA. Peak bright counts drop 17%.
- **Dominant pickup:** spatially varying current from direct rf-to-meander capacitance. A single cancellation tone cannot remove it.
- **Proposed fix:** an SiO2 overcoat plus a transparent conducting shield.

### Cited Findings
- **Fabrication sequence (Supp. "Trap fabrication"):**
  1. Intrinsic Si substrate (ρ > 20 kΩ·cm).
  2. 134 nm PECVD SiO2.
  3. 5 nm Ti / 50 nm Au by liftoff (SNSPD contacts and plating seed).
  4. An additional 350 nm Au liftoff on the SNSPD leads only.
  5. 8 nm amorphous Mo0.75Si0.25 capped with 2 nm a-Si, by DC magnetron sputtering.
  6. Optical plus e-beam lithography and ICP-RIE in SF6 to form the meander.
  7. 6 µm Au electroplating (commercial gold sulfite bath at 60 °C) through a 10 µm resist mask. The nanowire and leads are protected by resist.
  8. Ar ion milling of the seed in the gaps, with the nanowire protected.
  9. DRIE bowtie etch, with the whole chip under resist.
  10. Strips in acetone, with an additional NMP strip for the liftoffs.

  The SiO2 thickness and wire dimensions were chosen by RCWA for normal-incidence 313 nm absorption. The maximum SDE estimate is 72%. — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Yield and resistance.** Room-temperature resistance was 6–11 MΩ for working SNSPDs. It "increased by roughly 12 % to 30 %" over later fabrication steps. Larger increases correlated with lower switching current or failure to superconduct at 3.6 K. Most of the increase came between applying and stripping the electroplating resist, the step where electroplating happens. Resist apply/strip without plating did not cause it. DRIE heating was negligible. One month unprotected in air gave about 2.5% (Supp.). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Proposed fix.** Coat the nanowire with transparent SiO2 immediately after patterning, as an AR coat and for robustness. Because exposed dielectric charges, add a transparent shielding electrode on top, "either a continuous conducting film or a conducting mesh." The same layer would also cut induced rf currents, the click "kick," and electric-field noise (Supp.). The PRL main text (p. 4) also proposes "optically transparent SNSPD shielding electrodes." The thesis (Sec. 8.1.1, pp. 147–148) suggests a grounded transparent conductive film "such as ITO or similar," plus higher-Tc materials. — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Caution on ITO.** S-2017 says standard transparent conductive coatings such as ITO "may not be usable" because of poor transmission at many ion readout wavelengths (Sec. 2). — [S-2017](https://arxiv.org/abs/1611.09949)
- **Material and temperatures.** Tc = 5.2 K (PRL p. 2). The PRL says Tc should be ≳25% above the trap-surface temperature. The device operates with rf up to a trap temperature of 3.65 K (Supp.; thesis p. 62). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Switching current and RF on/off (PRL p. 3, Fig. 2; Supp.).**
  - Switching current ≈ 8.9 µA with rf off, at 3.45 K.
  - The rf reduces the maximum usable bias I_m by ≈3.6 µA. I_m ≈ 5.3 µA for the Fig. 2 data and ≈4.8 µA for the later SDE calibration, after the temperature drift.
  - Maximum bright counts with rf on are only 17% below rf off.
  - Mean dark counts per 200 µs detection stay below 10^−2 for I_b at least 1 µA below I_m.
  - With rf on and I_b = 0, bright counts are about 1 per 200 µs window (read from Fig. 2).
  - Thesis Fig. 6.6 caption: at RF amplitudes above the trapping value, the detector "did not operate at all." The operating point gives about 1 dark count per detection, with bright counts 83% of the no-RF maximum (thesis p. 118). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Circuit model (Supp. "SNSPD pulses and induced rf currents," Fig. S4, Eq. S1).**
  - Total nanowire inductance is 2.2 µH. The lead parasitics are L_L ≈ 5 nH and R_L ≈ 5 Ω.
  - One lead is grounded on chip and the other sees 50 Ω.
  - Two pickup paths exist. Lead capacitance C_RL with asymmetric termination drives a uniform current in phase with the rf. Direct capacitance C_RN to the meander drives a current that varies linearly along the wire and is 90° out of phase, zero at the midpoint.
  - The fit gives I0 = 0.9(1) µA uniform and I1 = 3.5(2) µA spatially varying, with K = 40. The C_RN required is about 1.5× the FEM value.
  - The spatially varying term dominates, which is why the S-2017 cancellation tone failed here.
  - Proposed remedies: reduce C_RN by capacitive shielding; use symmetric terminations; reduce C_RL; raise SNSPD inductance; widen the SDE plateau. — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Readout chain (Supp. Fig. S2; thesis Fig. 6.4).**
  - Bias: an AWG pulse attenuated 20 dB, through 10 kΩ, into the DC port of a bias tee (100 mV → 1.05 µA), ramped over 11 µs.
  - Amplifiers: two stages of 23 dB (46 dB total, 1 MHz–1 GHz).
  - The rf pickup is "several times larger" than the SNSPD pulses. Pulses are about 250 µV peak before amplification (thesis p. 115).
  - Filters: a 7th-order Bessel notch at the trap rf, 40 dB, 3 dB bandwidth 14 MHz; then a dissipative Gaussian low-pass, f_3dB = 25 MHz, adding 18 dB at the rf.
  - Detection: a Schmitt-trigger comparator, with ARTIQ timestamps at 1 ns.
  - Pulse shape: 1 ns rise with rf off and unfiltered, 10 ns rise when filtered. Pulse heights vary up to ×3 with rf on because of induced currents (Fig. S3). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Oxidation.** FEM shows that oxidizing the top 4 nm of MoSi would lower normal-incidence absorption from 72% to 65% (Supp. end). — [T-PRL](https://arxiv.org/abs/2008.00065)

### Inferences
- For a copy design, the main lever is lowering the direct C_RN from rf to meander. Options include moving the meander farther from the rf rails, shielding it, or using a symmetric bias/readout (for example a differential readout). Higher-Tc material would add margin. All are the authors' own recommendations; how to combine them is my reading.

### Gaps
- No measured C_RN or C_RL values are given beyond relative statements. No lead length or exact lead width is given. No chip-level map of lead routing to the bond pads is given.

---

## 6. Collection, efficiency, readout fidelity and time, count rate vs displacement

### Takeaway
At zone D the effective NA is 0.32. The fraction of emitted photons hitting the active area is 2.0(1)%, including the σ dipole pattern. The SDE is 48(2)% with rf on, an estimated 65(5)% without rf, against a 72% design value. Readout reaches F = 0.9991(1) in a mean of 46 µs (Bayesian) or 0.9988(1) at 125 µs (threshold). The count rate falls to about 3–4% of peak at about 82 µm lateral offset.

### Cited Findings
- **Collection.** Effective NA is 0.32 in zone D. Accounting for the dipole pattern, "2.0(1) % of the emitted photons will strike the SNSPD active region" (PRL p. 2). The fraction comes from Eq. S6, integrating (3/16π)(1 + cos²θ_q)·IDE·AP over the detector solid angle on a 1 µm × 1 µm grid, with uncertainty dominated by the ion height (Supp.). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Efficiency.** SDE is 48(2)% with rf on and I_b = 4 µA. The estimated maximum without rf is 65(5)%; the design value is 72% (RCWA, normal incidence, polarization-averaged). Absorption probability depends on angle and polarization (FEM in COMSOL, Supp. Figs. S6–S7). The SNSPD bright (dark) rate was about 2.5× (about 1.3×) the PMT's behind an NA 0.38 objective (PRL p. 3; Supp.). The thesis reports a QE of 0.44(2) "at our operating RF level of 9.1 V" (p. 120). — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Readout protocol.** The readout laser is applied for 500 µs. The first 50 µs are a heralding period: 0 counts marks "dark" and ≥8 counts marks "bright." The thresholding error minimum is 1.2(1) × 10^−3 at 125 µs (F = 0.9988(1)). The adaptive Bayesian method uses 1 µs bins and confidence levels from 0.9 to 0.9999. It reaches a minimum error of 9(1) × 10^−4 at a 46 µs mean duration (F = 0.9991(1)). The bright state takes 25 µs (ε_b = 6.1 × 10^−4) and the dark state 67 µs (ε_d = 11.9 × 10^−4). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Calibration rates.** λ_b = 162.50(3) ms^−1, λ_d = 5.095(5) ms^−1 (dark rate dominated by stray laser light), Γ_dp = 0.020(3) ms^−1, Γ_rp = 0.0120(7) ms^−1 (Supp. "Readout fidelity"). Fidelity is limited by off-resonant pumping out of |aux⟩, polarization impurity and rf-induced mixing (PRL p. 4). — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Count rate vs displacement (Fig. 4).** The normalized count rate along the axis is measured from about 6 to about 82 µm. It falls faster than the constant-SDE solid-angle model and agrees with the angle-dependent SDE model. The PRL calls this the first experimental measure of SNSPD SDE versus incidence angle (PRL pp. 4–5). The Supp. notes that the recess would eventually hide the detector at larger offsets, but not over the Fig. 4 range. — [T-PRL](https://arxiv.org/abs/2008.00065)
- **Thesis crosstalk statement.** "An ion 80 µm from the center of the detector … counts photons at less than 2% of the rate" of a centered ion (Sec. 6.4.3, p. 120; Fig. 6.9). — [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Other detector properties.** Photon antibunching was seen in SNSPD–PMT g(2), with the minimum at 28 ns because of chain delay (Supp. Fig. S5). With metastable shelving states, 40Ca+ could reach about 2 × 10^−5 error at the same detection efficiency (Supp.). — [T-PRL](https://arxiv.org/abs/2008.00065)

### Inferences
- Reading PRL Fig. 4 by eye (log axis): normalized rate is about 0.5 at 24 µm, about 0.2 at 44 µm, about 0.08 at 60 µm, and about 0.035 at 82 µm. That reading **conflicts slightly** with the thesis's "<2% at 80 µm." The thesis may use a different normalization or dataset. Treat about 2–4% at about 80 µm as the range.
- In Fig. 3(a), the optimal threshold sits between 5 and 6 counts per 125 µs. The bright mean is about 20 counts, consistent with λ_b × 125 µs ≈ 20.3.

### Gaps
- No tabulated Fig. 4 data. No count-rate measurement transverse to the axis.

---

## 7. Slichter et al. 2017: test-structure geometry, RF on/off, dark counts, temperature

### Takeaway
S-2017 built a **ring/point-trap test structure**: a square rf electrode completely surrounding a recessed 30 × 30 µm-capable MoSi rectangle, giving an rf well 48 µm above it. It showed 76 ± 4% SDE at 315 nm and 3.2 K for a stand-alone fiber-coupled device, with background counts below 1 cps. At 3.8 K with 25 V, 46.23 MHz rf, the switching current fell from 11.5 to 7.6 µA and the maximum count rate to 65%. A cancellation tone restored it to 91%. The background count rate did not increase.

### Cited Findings
- **Test-trap geometry (Fig. 2, Sec. 3).** "The rf electrode (red) surrounds the SNSPD." Grey electrodes outside are DC shim electrodes, grounded in these tests. The pseudopotential well sits 48 µm above the MoSi rectangle center. The active area could be up to 30 × 30 µm; the Fig. 2 device was 30 × 30 µm. Electrodes were 7 µm electroplated Au on a Ti/Au seed, ion-milled, with the SNSPD resist-protected. The substrate was 76.2 mm intrinsic Si wafers with 65 nm PECVD SiO2 (RCWA-chosen) and 5 nm Ti / 50 nm Au contacts. — [S-2017](https://arxiv.org/abs/1611.09949)
- **Calculated trap parameters.** At V_pk = 25 V, Ω_rf/2π = 46.23 MHz (half-wave coax resonator, Q = 27, about +23 dBm input): well depth 12 meV for 9Be+. Secular frequencies are about 5 and 9 MHz in plane and 14 MHz normal. The tested detector subtends 0.9% of the solid angle (NA 0.19). A 30 × 30 µm detector would subtend 2.8% (NA 0.33) (Sec. 4). — [S-2017](https://arxiv.org/abs/1611.09949)
- **Design rules from Sec. 2–4.**
  - The largest possible integrated-detector solid angle is set by the inside dimension of the rf electrode, or the rf–rf spacing in a linear trap, usually 1–2 ion heights. Including shields, gaps and thickness, an integrated SNSPD can subtend 3–8% (NA 0.35–0.55).
  - Detectors spaced 3 ion heights apart see 3–4% crosstalk. Recessing the detectors below the electrode tops reduces crosstalk and low-angle laser scatter.
  - Typical ion heights in current designs are 30–75 µm.
  - Array-size estimate: with a beam waist of 0.4 × the ion height at 313 nm, roughly 15–40 detection zones fit per readout beam.
  - Proposed architectures (Fig. 1): (a) detectors in the trap plane, with tall electrodes as optional shields; (b) flip-chip with SNSPDs on a separate wafer. — [S-2017](https://arxiv.org/abs/1611.09949)
- **Stand-alone detector (Sec. 4, Fig. 3).** 16 × 16 µm; 90 nm lines on a 190 nm pitch; 12 nm MoSi with no cap; fiber-coupled; LED at 315 nm. SDE plateau 76 ± 4% at 3.2 K, against an RCWA prediction of 69%. I_sw = 4.5 µA at 3.2 K, and 14.6 µA at 250 mK with a 75 ± 4% plateau. BCR < 1 cps for I_b ≤ 3.8 µA, where SDE is already 74 ± 4%. The comparison PMT gives 38 ± 2% at 315 nm with about 100 cps BCR. — [S-2017](https://arxiv.org/abs/1611.09949)
- **Trap-integrated detector (Sec. 4, Figs. 5–6).** 7 nm MoSi with a 2 nm a-Si cap; 140 nm lines on a 230 nm pitch; Tc = 5.6 K.
  - At 4.3 K, rf off: I_sw = 6.9 µA, BCR about 1 cps.
  - At 3.8 K, rf off: I_sw = 11.5 µA, plateau for I_b ≳ 9 µA, BCR < 1 cps below 10.5 µA. The 1/e pulse decay is 11 ± 1 ns, giving L_k = 550 ± 50 nH (70 ± 7 pH/square).
  - At 3.8 K, rf on: I_sw falls to 7.6 µA, the plateau disappears, and the maximum count rate is 65% of rf-off. BCR stays < 1 cps for I_b < 6.4 µA.
  - With the cancellation tone: I_sw rises to 8.7 µA and the maximum count rate to 91% of rf-off.
  - RF pickup at the output was similar in amplitude to the pulses and was cancelled with a phase-coherent tone before the counter.
  - The device was held at 3.8 ± 0.05 K at every rf setting, with an ADR heater. — [S-2017](https://arxiv.org/abs/1611.09949)
- **RF-current model (Sec. 4, Eq. 1, App. A).** The fit model is I_b(t) = I_dc + I_rf sin(Ω_rf t). It gives I_rf about 3 µA without cancellation and 1.3 µA with it. The fitted I_dc is about 750 nA above the applied value. Simulations (AWR Microwave Office, 8-inductor model) give I_rf of 3.5–6.5 µA, against a measured I_sw reduction of 3.9 µA. The amplitude is about 1.2 µA larger at the grounded end, and the phase varies 40–60° along the wire. The paper concluded that the **lead-capacitance + asymmetric-termination** term dominated in that device. Recommended fixes: reduce lead–rf capacitance, terminate both leads identically, and use longer, thinner meanders, which have more inductance. — [S-2017](https://arxiv.org/abs/1611.09949)
- **Bias switching.** Since SNSPDs turn on and off quickly via the bias and show no afterpulsing, exposure to other beams outside the readout window "should not compromise" performance (Sec. 2). Todaro et al. later found that with rf on the detector cannot be fully turned off (Section 4 above). — [S-2017](https://arxiv.org/abs/1611.09949), [T-PRL](https://arxiv.org/abs/2008.00065)

### Inferences
- **Evolution from S-2017 to Todaro 2021:**
  - Ring/point rf trap → linear five-wire trap with the detector in a DC electrode pocket near the rf end.
  - SiO2 65 → 134 nm; MoSi 7 → 8 nm; wire 140/230 → 110/170 nm; Au 7 → 6 µm; Tc 5.6 → 5.2 K; rf 25 V at 46 MHz → 8.8 V at 67 MHz.
  - Dominant pickup mechanism: lead/uniform (S-2017) → direct meander/spatially varying (Todaro). The thesis (p. 118) attributes this to "increased coupling between the RF electrode and the SNSPD meander."
- **Internal inconsistency in S-2017:** the Fig. 2 caption says the active area was 30 × 30 µm, while Sec. 4 says the tested detector subtended only 0.9% (NA 0.19), much smaller than the stated 2.8% for 30 × 30 µm. The tested rf-trap device probably had a smaller meander inside the 30 × 30 µm MoSi rectangle.

### Gaps
- S-2017 gives no ion trapping; the well height and frequencies are calculated only. No rf electrode dimensions are given in text. The leads' path across the rf ring is visible only in the SEM.

---

### Cross-source discrepancies to flag (all cited above)
- **RF amplitude and SDE:** the PRL gives 8.8 V peak and SDE 48(2)%. The thesis gives an "operating RF level of 9.1 V" and QE 0.44(2), and its Fig. 6.6 caption treats 9.1 V as the trapping level. — [T-PRL](https://arxiv.org/abs/2008.00065), [T-Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis)
- **Heating values:** the PRL gives 113(14) q/s at 5.3 MHz and 0.009(5) q/click. The thesis gives 108(14) q/s at 5.34 MHz and 0.010(4) q/click. — same sources.
- **Crosstalk at about 80 µm:** the thesis says <2%. The PRL Fig. 4 shows about 3.5% at about 82 µm (my reading of the plot). — same sources.
- **Active area orientation:** the PRL Supp. says "22 µm × 20 µm" and the thesis "20 × 22 µm." Neither says which side lies along the axis. — same sources.
