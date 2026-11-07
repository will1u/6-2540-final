> Claude-authored literature report (design/research). Not a substitute for reading the cited sections.

# Recess and rail ends lower the readout ion

Todaro et al. 2021 put the SNSPD in a **recessed pocket cut into the grounded/DC centre electrodes between the two rf rails**, not under or between rf metal. The pocket sits about 83 µm before the rf rails terminate. The ion's height falls from **≈39 µm to ≈29 µm above the electrode plane** over the detector ([Todaro PRL p. 2](https://arxiv.org/abs/2008.00065)). The PRL calls the drop "by design" and gives no cause. The Todaro thesis gives two causes: **end effects from the rf-electrode termination** and the **failure of the planar (2D) model over the 6 µm recess** ([Todaro thesis Sec. 6.3, p. 113; Fig. 6.3 caption, p. 114](https://www.nist.gov/document/susanna-todaro-phd-thesis)). No source attributes the drop to fields from the SNSPD. Your hypothesis is therefore half right. "Not SNSPD fields" is consistent with every source. "Absence of electrode metal" is too coarse a framing: the thesis names the rf termination first, and figure measurements suggest a third, unstated contributor (the rf channel narrows past the detector). For the shield stack, Hampel et al. 2023 show that a **grounded Al mirror under the nanowire removes the rf-induced-current signature**, leaving rf heating as the residual limit. They simulated a grounded ITO top shield but did not fabricate one ([Hampel arXiv:2302.01462, Figs. 2–4](https://arxiv.org/abs/2302.01462)). Todaro's supplement and Hampel's published version both say exposed dielectric over the detector needs a transparent grounded electrode **on top** ([Todaro Supp. "Trap fabrication"](https://arxiv.org/abs/2008.00065); [Hampel APL version, paragraph after Fig. 2](https://tf.nist.gov/general/pdf/3223.pdf)). Four other parts of the literature bound the rest of your design. Room-temperature bias-sputtered NbN is the only MIT NbN recipe compatible with an Al ground plane. The five-wire analytic formulas bound the geometry for 138Ba+ at 50 µm. Flashover data for SiO2 over a conductor bound the rf amplitude. The process recipes are spread across JoVE/Hong 2017, PTB, Sussex 2022 and Dietl 2025, and no single paper documents your exact stack.

Notes on provenance. Numbers marked **[team calc]** were computed by the research team for these notes, not taken from a paper. They include figure pixel measurements, gapless five-wire calculations, a transfer-matrix (TMM) optical model and Sterling-formula evaluations. Treat them as starting points to re-derive, not as literature. The TMM scripts are in `C:\Users\willi\AppData\Local\Temp\claude\C--Users-willi-Repos-6-2540\2462feda-17d8-4bbb-b4c9-ed087db8a35f\scratchpad\` (tmm_stack.py, run1–3.py). "Supp." means the PRL Supplemental Material, pp. 8–15 of arXiv:2008.00065v1. Thesis page numbers are printed page numbers.

## The detector sits in a hole in the DC centre electrode, 83 µm before the rf rails end

**Layout.** Todaro's "detector trap" is a five-wire linear surface trap with **24 electroplated Au electrodes, 6 µm thick, with 3–4 µm gaps, on 350 µm intrinsic Si** ([thesis Sec. 4.2.1.2, p. 60](https://www.nist.gov/document/susanna-todaro-phd-thesis)). Thesis Fig. 4.8 (p. 61) names them:

- nine outer segmented DC electrodes per side (DC1–DC9, DC10–DC18);
- two rf rails;
- two centre electrodes, **CUL/µwave1 and CLL/µwave2**, filling the channel between the rails on the load side; either can act as a non-resonant microwave antenna (thesis pp. 61–62, Fig. 4.10);
- two centre electrodes, **CUR and CLR**, that flank the SNSPD pocket and the lead channel on the detector side.

The false-colour SEM (thesis Fig. 4.9(a), p. 62) shows the nanowire on the floor of a pocket whose walls are the electroplated CUR/CLR electrodes. The caption gives the ion **35(1) µm above the detector surface** and an effective **NA of 0.32**. Thesis Table B.1 lists separate voltages for CUR and CLR, so they are DC-biased electrodes (rf ground), not rf. **No electrode metal lies over the detector.**

**Detector.** The meander has a **22 µm × 20 µm active area, 110 nm wires on a 170 nm pitch, aligned with the trap axis** ([Supp. "Trap fabrication"](https://arxiv.org/abs/2008.00065)). The PRL says it is **"recessed another 6 µm"** below the electrode top plane ([PRL p. 2](https://arxiv.org/abs/2008.00065)). No source says whether the 22 µm or the 20 µm side runs along the axis. The leads were made **"much narrower than typical SNSPD leads … to minimize capacitive coupling to the trap rf electrodes"** and thickened with 350 nm Au to avoid latching ([Supp. "Trap fabrication"](https://arxiv.org/abs/2008.00065)). They leave the pocket along the axis, away from the load zone, in the centre channel (PRL Fig. 1(b); thesis Fig. 4.8).

**Dimensions measured from figures [team calc].** No GDS-level dimension is published for the pocket, rails, gaps or segments. Measured from PRL Fig. 1(b) and thesis Fig. 4.8, with roughly ±2–3 µm error:

| Feature | Approximate size |
|---|---|
| RF rail width | ≈47 µm |
| Centre channel at the load/transport zones | ≈57–58 µm |
| Centre channel past the detector | ≈44–45 µm (rails widen to ≈51–53 µm) |
| RF rails end, measured from detector centre | ≈83–85 µm downstream |
| Pocket opening | ≈50 µm along the axis × 42 µm across |
| DC-electrode rim around the pocket | ≈3.5–5 µm |
| Outer DC segment pitch | ≈44 µm |

**Comparison: Slichter 2017.** The earlier test structure used a different geometry. A square rf electrode completely surrounded the recessed MoSi rectangle (up to 30 × 30 µm), with the calculated pseudopotential well 48 µm above it ([Slichter 2017 Sec. 3, Fig. 2](https://arxiv.org/abs/1611.09949)). Todaro's design moves the detector off the rf electrode and into a DC-electrode pocket. Slichter's Sec. 2 also gives the general rule: the largest integrated-detector solid angle is set by the rf–rf spacing in a linear trap, usually 1–2 ion heights. Including shields and gaps, an integrated SNSPD can subtend **3–8% of the solid angle (NA 0.35–0.55)**.

## Rf-rail termination, the recess and channel narrowing all pull the null down

**What the sources state.** The PRL says the ion sits "≈ 39 µm above the top surface plane of the trap electrodes, dropping by design to a smaller distance of ≈ 29 µm above this plane when centered over the SNSPD" ([PRL p. 2, Fig. 1(a)](https://arxiv.org/abs/2008.00065)). The thesis explains the drop in three places:

- Sec. 4.2.1.2 (p. 62): the rf null "is not uniformly 39 µm from the trap" and curves about 10 µm toward the surface at the detector end because of end effects.
- Sec. 6.3 (p. 113): the drop is due to "a combination of end-effects from the end of the RF electrodes" together with the breakdown of the Biot–Savart (planar) analog, which assumes all electrodes lie in one plane and fails where the height step is large compared with the ion height.
- Fig. 6.3 caption (p. 114): repeats both causes.

[Thesis](https://www.nist.gov/document/susanna-todaro-phd-thesis). No source plots h(x), separates the two contributions, or mentions an SNSPD-generated field. Height was measured per position by scanning the readout beam, with about 1 µm uncertainty ([Supp. "Experimental apparatus"](https://arxiv.org/abs/2008.00065)).

**How to sharpen the hypothesis [team inference].** CUR/CLR are at rf ground, and the nanowire is tied to ground at one end with the other end on 50 Ω. So **in a planar (gapless) model the pocket floor and the surrounding centre electrode sit at the same rf potential, and the hole is invisible to the rf.** "Missing metal" changes the rf null only through the step: the floor is 6 µm below the plane while the ion is ≈29 µm above it, a ratio of about 0.2. The figure measurements also show the rf inner edges stepping inward past the detector (channel ≈57 → ≈45 µm). In the gapless formula h = ½√(a(a+2b)), narrowing the channel from 57 to 45 µm while widening the rails from 47 to 52 µm lowers h by about 12%. That would be roughly 5 µm of the 10 µm drop if the scaling held. This is a rough number from pixel-measured widths and an infinite-rail model.

The testable version of your hypothesis therefore has three candidate causes:

1. the rf-rail termination about 83 µm away;
2. the non-planar recess;
3. the channel narrowing.

A 3D BEM model that switches each one on in turn would separate them. That is a check to run, not a literature result.

**Consequence for your simulation workflow.** gds2itvg produces planar (2D-layout) solutions. Todaro's thesis states that the planar analog fails over a recess that is deep compared with the ion height. If your detector window is opened through ~10 µm of SiO2 plus the Au thickness, the window depth relative to a 50 µm ion height is worth computing before you trust planar results over the window.

## A readout zone 264 µm from the load zone, reached by shuttling

**Zones.** The PRL labels zones **A–D**, from directly over the SNSPD (D) to **264 µm away (A, the load zone)**. Ions are moved to D "using time-varying potentials on the segmented outer electrodes" ([PRL pp. 2–3](https://arxiv.org/abs/2008.00065)). The thesis numbers zones 2–8 on a ≈44 µm pitch. It loads in zone 2 or 3, at the end farthest from the detector with "no line-of-sight to the detector" ([thesis Sec. 5.3.1, p. 101; Sec. 6.3, p. 113](https://www.nist.gov/document/susanna-todaro-phd-thesis)). Table B.1 (App. B) gives full DC voltage sets for a 2.0 MHz axial well in each of zones 2–8 using DC1–DC18, CUL, CLL, CUR and CLR. It is the closest published example of a per-zone voltage set for this layout. No waveform durations or speeds are given for the detector trap. The thesis transport chapter (Ch. 7) uses a detectorless "transport trap" in which a 50 nm evaporated Au electrode ("det") replaces the SNSPD (Sec. 4.2.1.3, Fig. 4.11). The Doppler-cooled lifetime was **days** in both the load zone and over the detector (thesis Sec. 6.3).

**Operating point.** RF was **8.8 V peak at 67.03 MHz**. Motional frequencies were ≈2 MHz axial and 5–10 MHz radial for 9Be+ ([PRL p. 2](https://arxiv.org/abs/2008.00065)). All beams and B0 lay in the trap plane at 45° to the axis (PRL Fig. 1 caption). The chip was DRIE-cut to a "bowtie" with a **1.8 mm-wide central isthmus** so focused beams are not clipped ([Supp. Fig. S1](https://arxiv.org/abs/2008.00065)). The trap ran at ≈3.5 K, 0.45 K above the cold head (Supp.; thesis Fig. 4.6). The PRL suggests doing Raman operations away from detector zones, because sideband cooling over the detector was blocked by stray-light clicks (p. 4).

**What the detector does to the ion.**

- **Heating.** 113(14) quanta/s at 5.3 MHz over the SNSPD, versus 63(6) quanta/s at 2 MHz in zone B. After d⁻⁴ scaling, the field noise over the detector is about 6× higher ([PRL p. 4](https://arxiv.org/abs/2008.00065)). The thesis gives 108(14) quanta/s (Sec. 6.6, p. 127).
- **Click kicks.** Each click deposits **0.009(5) quanta**, because part of the wire stays grounded while the rest follows the output voltage (PRL p. 4). The thesis gives 0.010(4) quanta/click (Fig. 6.12).
- **Clicks with bias off.** "Even when the bias current is off, the SNSPD will occasionally pulse in response to photons when the trap rf is on" (PRL p. 4).
- **Bias gating.** Bias is applied only during readout and ramped over 11 µs ([thesis Sec. 6.3.1, p. 114](https://www.nist.gov/document/susanna-todaro-phd-thesis)).
- **Stray fields.** No detector-specific micromotion or stray-field value is published. Generic stray fields were ≈300 V/m in-plane and ≈750 V/m vertical (thesis Sec. 5.3.2, pp. 101–103).

**Collection, readout and crosstalk.** **2.0(1)% of emitted photons strike the active area**, including the dipole pattern. SDE was **48(2)% with rf on**, an estimated 65(5)% without rf, against a 72% design value ([PRL pp. 2–3; Supp. Eq. S6](https://arxiv.org/abs/2008.00065)). Readout reached **F = 0.9991(1) in a mean of 46 µs** (adaptive Bayesian) or 0.9988(1) at 125 µs (threshold) (PRL p. 4). An ion 80 µm from the detector centre counts at <2% of the centred rate ([thesis Sec. 6.4.3, p. 120](https://www.nist.gov/document/susanna-todaro-phd-thesis)). PRL Fig. 4 reads closer to ≈3.5% at ≈82 µm [team reading of the log plot]. Slichter puts crosstalk at 3–4% for detectors 3 ion heights apart and notes that recessing reduces it ([Slichter 2017 Sec. 2](https://arxiv.org/abs/1611.09949)).

## A grounded mirror below kills induced currents; the top shield is about charge and kicks

**Rf pickup in Todaro's device.** The trap rf cut the usable bias from the **8.9 µA switching current to I_m ≈ 5.3 µA** (4.8 µA after temperature drift). The fit splits the induced current into **I1 = 3.5(2) µA spatially varying**, from direct rf-to-meander capacitance C_RN, and I0 = 0.9(1) µA uniform, from lead capacitance with asymmetric termination ([Supp. "SNSPD pulses and induced rf currents", Fig. S4, Eq. S1](https://arxiv.org/abs/2008.00065)). A uniform cancellation tone cannot remove the spatially varying term. The authors' remedies are to reduce C_RN by capacitive shielding, use symmetric termination, lower C_RL, and raise inductance.

Slichter's earlier ring trap showed the opposite balance: lead coupling dominated, and a cancellation tone restored the count rate to 91% ([Slichter 2017 Sec. 4, Eq. 1, App. A](https://arxiv.org/abs/1611.09949)). Pickup at the output was **"several times larger"** than the ≈250 µV pulses. It needed a **40 dB, 7th-order Bessel notch at f_rf plus a 25 MHz low-pass** ([Supp. Fig. S2; thesis p. 115](https://arxiv.org/abs/2008.00065)).

**Hampel 2023 stack and result.** The stack, bottom to top, is:

- high-resistivity Si
- 150 nm PECVD SiO2
- **50 nm e-beam Al mirror**
- **212 nm SiO2**
- **10 nm NbTiN** (90 nm wires on a 180 nm pitch, 20 × 30 µm active area)
- **130 nm PECVD SiO2 cap**, patterned to cover only the SNSPD

The trap electrodes are 350 nm Au. The mirror is grounded through CHF3-etched vias plus 20 nm Au contacting the Au electrode layer ([Hampel arXiv:2302.01462, fabrication paragraph](https://arxiv.org/abs/2302.01462)). Note the material: **NbTiN, not NbN**.

With a **floating** mirror, the switching current fell and the count-rate curve flattened, the induced-current signature. With a **grounded** mirror, the model "suggests that almost no induced rf currents are present". The devices operated to **54 V peak at 70 MHz and up to 6 K** (Figs. 3–4). The residual effect looked like heating: the SNSPD was ≈0.5 K above steady state right after 45 V rf was switched off. The authors note that their 350 nm electrodes may exaggerate dissipation compared with 6 µm electrodes. The published version adds that a larger mirror may cool better ([NIST PDF of APL version](https://tf.nist.gov/general/pdf/3223.pdf)).

Two Hampel numbers matter directly for Ba+:

- **Charge-to-mass range.** Hampel states usability "for ions with charge-to-mass ratio ≥ 0.01 e/u". **138Ba+ is 1/138 ≈ 0.0072 e/u**, below that stated range.
- **RF scaling.** Ca+ needs 40 V at 70 MHz for ≈2/5 MHz secular frequencies, and "reducing the rf frequency will reduce the required rf amplitude proportionally" (final paragraphs).

**Simulated shielding.** The 2D FEM at 100 V and 70 MHz shows the grounded mirror cutting the rf field at the wire by **"roughly an order of magnitude"**. A grounded 50 nm Au mesh or 50 nm ITO on top improves it further, but no number is given (Fig. 2(a)–(d)). The fabricated devices had no top shield "for simplicity". The published version says a top layer "may be necessary … to protect the ion from accumulating surface charges on the insulating SiO2 layer and to reduce motional heating of the ion due to SNSPD pulses", but "might not be required" for rf shielding of the SNSPD ([NIST PDF](https://tf.nist.gov/general/pdf/3223.pdf)). Todaro's Supp. makes the same point: a dielectric overcoat needs "either a continuous conducting film or a conducting mesh" on top, and that layer also cuts the click kick and electric-field noise ([Supp. "Trap fabrication"](https://arxiv.org/abs/2008.00065)). The thesis suggests a grounded film "such as ITO or similar" ([thesis Sec. 8.1.1, pp. 147–148](https://www.nist.gov/document/susanna-todaro-phd-thesis)).

**Check worth running.** List, layer by layer, which material the ion sees directly above your SNSPD window. Compare that against these two passages.

**ITO evidence.** Eltony et al. built five-wire traps from **400 nm RF-sputtered ITO** (lift-off, no anneal mentioned):

- resistivity **1–2 × 10⁻⁵ Ω·m**;
- ≈60% transmission at 422 nm, including the quartz;
- held 88Sr+ for hours at a **≈6 K** trap surface;
- no measurable micromotion change after a 405/461 nm beam (≈5 mW/mm²) was crashed into the trap for 10 min.

([Eltony 2013, fabrication and results paragraphs](https://arxiv.org/abs/1212.1443)). Slichter cautions that ITO "may not be usable" at many UV readout wavelengths ([Slichter 2017 Sec. 2](https://arxiv.org/abs/1611.09949)). At 493 nm that concern is weak: good ITO has n ≈ 1.84–1.97 and k ≈ 0.003–0.011 ([refractiveindex.info, Moerland; König; Minenkov](https://refractiveindex.info/?shelf=other&book=In2O3-SnO2&page=Moerland)). ITO stays metallic-like down to liquid-helium temperature, with a small residual-resistance ratio and a weak log upturn below ~25 K ([Lin & Li review, arXiv:1702.07845](https://arxiv.org/abs/1702.07845)). The team took the upturn detail from abstracts, not full text. Sedykh et al. 2025 measured an ITO-shielded NbN SNSPD in a model trap at 2.2 K (0.01–2 V, 5–35 MHz). Only the abstract was read, so no shielding factor is available ([Ioffe page](https://journals.ioffe.ru/articles/61926)). **No fabricated ITO-shielded trap SNSPD with a published pickup reduction or kick-heating number was found.**

**Optical cavity at 493 nm [team calc, TMM with effective-medium meander, not RCWA].** Inputs:

| Material | n + ik at 493 nm | Source |
|---|---|---|
| Al | 0.61 + 5.25i | McPeak, DOI 10.1021/ph5004237 |
| SiO2 | 1.463 | Malitson |
| NbN | ≈2.11 + 2.00i | Banerjee 2018 Glasgow dataset, DOI 10.5525/gla.researchdata.637 |
| NbN | ≈2.50 + 2.51i | Medeiros 2019 Table I, interpolated |

The two NbN datasets differ by ~20%, so measure your own film. Results:

- **Spacer from Al to NbN.** Absorption is periodic in the spacer thickness t1 with period λ/2n ≈ 168 nm. Peaks are at **t1 ≈ 65 ± 15 nm** (A ≈ 0.40 for 7 nm NbN, no ITO) and ≈228–236 nm. There is a **node near 148 nm (A ≈ 0)**.
- **ITO layer.** A 40–60 nm ITO layer over an ≈88 nm cap acts as a high-index matching layer. It raises 7 nm NbN absorption to ≈0.53 while the ITO itself absorbs 0.7–3%, depending on k.
- **Thicker NbN.** 10 nm NbN gives ≈0.60–0.62 with ITO.
- **No mirror.** Without a mirror, absorption is only ≈0.20–0.33, consistent with Hampel's measured factor of ≈2 (68% vs 40% SDE at 395 nm).
- **Coherent fringes in the thick oxide.** Treated fully coherently, the 10 µm oxide swings absorption between ≈0.46 and 0.63 over a 168 nm thickness change.
- **Weak spectral selectivity.** 650 nm repump light is absorbed at ≈55% of the 493 nm efficiency, so the stack gives no meaningful stray-light rejection.
- **Calibration.** The model reproduces Hampel's mirror stack within about 10% (0.61 vs 0.68) but underestimates the no-mirror case. Sign-off needs RCWA or FDTD.

## The NbN process has to stay cold, TMAH-free and capped early

**Deposition.** Dane et al. showed that a **50 W RF substrate bias during unheated reactive DC magnetron sputtering raises NbN Tc by up to 73% (to ≈7.8 K) and smooths the film** enough for unconstricted nanowires ([Dane APL 111, 122601, abstract via MIT DSpace](https://dspace.mit.edu/handle/1721.1/126227)). The full recipe numbers (flows, power, pressure) were not retrieved because of DSpace rate-limiting. Two downstream MIT papers describe films from this recipe:

- Toomey: ≈5 nm films give **R_s ≈ 600 Ω/sq and Tc ≈ 7.9 K**, ρ ≈ 250 µΩ·cm ([Toomey 2018](https://doi.org/10.1116/1.5047427)).
- Medeiros: ran it in an AJA Orion system at ≈0.04 nm/s (200 s → 8 nm) ([Medeiros arXiv:1812.05559](https://arxiv.org/abs/1812.05559)).

The older MIT heated process (800 °C holder, Tc 10.9 K) ([Najafi 2015 Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)) is far above the Al melting point, so the unheated recipe is the Al-compatible one [team inference]. Combine this with Todaro's rule that **Tc should be ≳25% above the trap-surface temperature** ([PRL p. 2](https://arxiv.org/abs/2008.00065)): Tc ≈ 7.8 K implies a trap surface no warmer than about 6.2 K. Hampel's NbTiN worked to 6 K.

**Metrology and degradation.**

- **Thickness.** Medeiros measures thickness by four-wavelength ellipsometry. It agrees with XRR within 0.5 nm above ~4 nm.
- **Oxidation.** An 8 nm film lost **8.7% of its NbN in 100 days of air**. The oxide followed **d_ox = 0.78 t^0.17 nm** (t in days) ([Medeiros Sec. on oxidation](https://arxiv.org/abs/1812.05559)), i.e. ≈0.8 nm after one day [team calc].
- **TMAH.** Toomey found that **25% TMAH forms a soluble TMA-hexaniobate that thins NbN and blocks CF4 etching**. 60 s removed ≈0.25 nm and dropped Tc by 0.2 K. 25 h removed ≈57% and dropped Tc by ≈1.6 K. A ≥3 min *running* DI rinse removes the etch barrier but not the thinning ([Toomey JVST B 36, 06JC01, abstract and Expts. 1–2](https://doi.org/10.1116/1.5047427)).
- **Patterning precedent.** The MIT flow is 70 nm HSQ, Raith 150 at 30 keV, 700–850 µC/cm², TMAH develop, **CF4 RIE 50 W, 2.5 min**, then Ti/Au pads by bilayer lift-off ([Najafi 2015 Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)).

**Yield hazard from later processing.** In Todaro's device, MoSi room-temperature resistance **rose 12–30% during later fabrication, mostly between applying and stripping the electroplating resist** (the plating step). Larger rises correlated with low switching current or failure to superconduct ([Supp. "Trap fabrication"](https://arxiv.org/abs/2008.00065)). The proposed fix is an SiO2 cap right after patterning. Hampel's 130 nm PECVD SiO2 cap "to protect the nanowire during further processing and limit degradation due to oxidation" is the working precedent.

No primary data were found on NbN nanowires after O2 ashing, BOE/HF, ITO sputtering or anneal, or electroplating baths. Inert anneals to 500 °C preserve NbN Tc ([arXiv:2501.07780](https://arxiv.org/pdf/2501.07780)). Uncapped NbN loses Tc in oxygen anneals ([Ioffe paper](https://journals.ioffe.ru/articles/viewPDF/59210)).

**Al ground plane under the detector.** Sputtered or evaporated Al shows hillocks and voids after ~350 °C anneals. Ti or TiW caps suppress them ([SINTEF](https://www.sintef.no/publikasjoner/publikasjon/1155451/)), and JoVE uses **Al-1%Cu to "prevent whisker formation during bakeout"** ([Hong JoVE 2017, M1 step](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)). No hillock-height data for thin Al under PECVD oxide were found. In your stack, the 10 µm PECVD step (JoVE: 350 °C) happens *after* the nanowire sits a few tens of nm above the Al. The team flags hillock-induced constrictions as an unquantified yield risk [team inference].

**Device estimates [team calc].** Lk,sq ≈ 105 pH/sq (dirty-BCS from R_s = 600 Ω/sq, Tc = 7.9 K). A 20 × 20 µm, 100/200 nm meander would then have L ≈ 2 µH, a ≈40 ns reset into 50 Ω, and an estimated switching current of ~15–25 µA. Hampel's 10 nm NbTiN measured ≈55–60 µA at 4.5 K, 1.3 µH and 25 ns ([Hampel Fig. 3; readout paragraph](https://arxiv.org/abs/2302.01462)).

## Five-wire rules put 138Ba+ at 50 µm near 100–200 V and 30–50 MHz

**Height and depth formulas.** Wesenberg gives q0 = 4QV/(MΩ²d²) (Eq. 9) and the depth scale U0 = Q²V²/(4MΩ²d²) (Eq. 12). The maximal intrinsic surface-quadrupole depth is ≈0.0091 U0 (Eq. 30, reconstructed from garbled text plus his numeric example U*_s = 55.8 meV). Stability needs q < 0.7. A DC bias on the rf rails can deepen the trap (Sec. V B). The gapless model needs gaps ≪ d and other conductors far away (Sec. II A). ([Wesenberg arXiv:0808.1623](https://arxiv.org/abs/0808.1623).) Shi 2023 Eq. 2 writes the five-wire rf depth as q²V²/(π²mΩ²z0²)·κ(a,b) ([Shi APL 122, 264002](https://www.osti.gov/pages/servlets/purl/2425574)). Chiaverini Fig. 4 puts five-wire depth at ≈1% of a comparable two-layer quadrupole ([Chiaverini QIC 5, 419, Sec. 4–5](https://arxiv.org/abs/quant-ph/0501147)).

**Gapless results [team calc].** The null height is **h = ½√(a(a+2b))** (asymmetric rails: h = √(abc(a+b+c))/(b+c); check against House 2008, which the team could not access). κ peaks at 0.0091 for b/a ≈ 3.7, the rf gradient peaks near b/a ≈ 2.5, and the escape point sits ≈2h above the surface. For 138Ba+ at h = 50 µm:

| b/a | a | b | f_rf | V | q | f_r | Depth |
|---|---|---|---|---|---|---|---|
| 3.68 | 34.6 µm | 127 µm | 41.1 MHz | 150 V | 0.39 | 5.6 MHz | 216 meV |
| 3.68 | 34.6 µm | 127 µm | 30 MHz | 100 V | 0.49 | 5.2 MHz | 180 meV |
| 1 | 57.7 µm | 57.7 µm | 41.1 MHz | 150 V | 0.35 | 5.0 MHz | 129 meV |

**Ba+ precedents.**

- **MIT/MIT-LL** ran 138Ba+ in a cryogenic Nb-on-sapphire trap at **h = 50 µm, 41.1 MHz, radial 1.9–3.3 MHz, axial 0.5–0.6 MHz**, loaded by 1064 nm ablation plus **554 + 405 nm photoionisation**. Their model gives an **optimal rf depth of ~0.1 eV** for ablation loading (Eq. 3/Fig. 3, numerals partly garbled in extraction). They recommend a high-volume loading zone plus a transition region ([Shi 2023](https://doi.org/10.1063/5.0149778)). The rf amplitude is not stated; the team back-calculates ~60–100 V.
- **UW Blinov group** ran Ba+ at 24.9 MHz, ~96–100 V, 0.75/1.5/2.1 MHz, ~44 meV depth. Lasers were 493 nm cooling, 650 nm repump, 614 nm deshelve, and 791 + 450 nm photoionisation. They used an oven shutter because oxidised Ba clogs loading slots ([Graham 2014, AIP Adv. 4, 057124](https://pubs.aip.org/aip/adv/article/4/5/057124/20382/A-system-for-trapping-barium-ions-in-a)).

**Segment width.** The axial potential per volt peaks at **W/d ≈ 0.78** and drops significantly below W/d ≈ 0.5 ([arXiv:quant-ph/0606237](https://arxiv.org/pdf/quant-ph/0606237); authorship unverified, from a search snippet). For separation, the quartic coefficient favours W ≈ a to 3.66a, where a is the rf-electrode separation ([arXiv:1007.3542](https://arxiv.org/pdf/1007.3542), Fig. 5). Doret used 44 independent DC electrodes for shuttling, splitting and axis tuning, plus a localised loading aperture ([Doret NJP 14, 073012](https://arxiv.org/abs/1204.4147)). No published "minimum electrodes per zone" rule was found. The team's count is ≥5 independent DC degrees of freedom per zone: E_x, E_y, E_z, axial curvature and one tilt term.

**Heating.** Sedlacek found field noise scaling as **≈d⁻⁴ at both room and cryogenic temperature**, with cryogenic rates ≈100× lower ([Sedlacek PRA 97, 020302(R)](https://arxiv.org/abs/1712.00188)). Other data give d⁻³·⁵ (needle trap, via [Brownnutt review](https://arxiv.org/pdf/1409.6572)) and β ≈ 2.6 ([arXiv:1906.06489](https://ar5iv.labs.arxiv.org/html/1906.06489)), so the exponent is not universal. Scaling Todaro's 3.5 K surface to Ba+ at 50 µm suggests ~a few quanta/s at 2 MHz [team order-of-magnitude extrapolation].

**Gaps and breakdown.**

- **Gap aspect ratio.** Gaps should be at least as deep as they are wide (aspect ratio > 1) ([Bautista-Salvador NJP 21, 043011](https://arxiv.org/abs/1812.01829)). Chiaverini asks for trenches or plating more than a few times the gap width (Sec. 6).
- **Flashover model.** Sterling's model is **V_b = √(u·e·d/ε0)**. For Au on quartz, u_rf ≈ 4.6 × 10¹⁸ eV/m². **SiO2 on a Si substrate is ≈30% worse** (u ≈ 1.4 × 10¹⁸), attributed to the conductive substrate. An 80 nm SiN surface layer gives ≈3.6× SiO2 (u ≈ 18.1 × 10¹⁸) ([Sterling APL 103, 143504, Eq. 1, Figs. 2–3](https://www.sussex.ac.uk/physics/iqt/APPLAB_103_14_143504_1.pdf)).
- **Evaluated flashover voltages [team calc].** SiO2-on-Si: ≈356 V at 5 µm and ≈503 V at 10 µm. SiN-surface: ≈1280 V at 5 µm. Whether these are peak or rms is not stated in the extracted text.
- **Measured trap-stack precedents.** Sussex measured **>250 V_amp at 15 MHz** with 8 µm oxide over the ground plane ([Siegele-Brown 2022](https://arxiv.org/abs/2202.02313)). JoVE reports 240 V across an 8 µm gap.

**Beam clipping [team calc].** For a beam skimming the surface at height h over a path ±z, the best worst-case radius is √2·√(λz/π). At 493 nm that gives **w ≈ 40 µm over ±5 mm** (0.8h, strong surface scatter) but **≈18 µm over ±1 mm**. Precedents use beams at 45° to the axis and bowtie chips (Todaro 1.8 mm isthmus; Sandia HOA ([Revelle arXiv:2009.02398](https://arxiv.org/abs/2009.02398))). Graham's Ba+ beams ran ~70 µm above a whole chip with 55–97 µm radii.

## No paper documents this exact stack; four flows cover its pieces

**Romaszko et al.** give the generic ground-plane flow ([NRP 2, 285, Sec. 3.2–3.3, Fig. 3.1](https://arxiv.org/pdf/1908.00267)):

- D1: 1–2 µm SiO2/SiNx.
- M1: 1–2 µm Au/Al/Cu.
- D2: "on the order of 10 µm" PECVD, called the hardest step.
- M2: electroplated, sputtered or evaporated.
- D2 is then etched vertically using the electrode pattern as the mask, followed by an isotropic sidewall undercut.

They also note that mid-resistivity Si is lossy at rf and that Si can freeze out at cryogenic temperature. No numbers are given.

**Stick et al. (Sandia).** Al M1, **9 µm multilayer PECVD pillars**, Al M2 overhanging by 5 µm with 7 µm gaps, and the backside Au-coated to prevent charge-up. Packaged in a 100-pin CPGA on a 1.5 mm spacer, with **Au ribbon wedge bonds to M1 pads 9 µm below the surface**. **Every trap was tested for shorts between all electrode pairs including the ground plane: none below 100 MΩ** ([arXiv:1008.0990](https://arxiv.org/abs/1008.0990)).

**JoVE / Hong 2017** is the most numeric recipe ([JoVE 56060](https://www.jove.com/t/56060/experimental-methods-for-trapping-ions-using-microfabricated-surface)):

- 0.5 µm wet oxide plus 0.2 µm LPCVD SiN;
- **1.5 µm sputtered Al-1%Cu** M1, BCl3/Cl2 ICP;
- **14 µm PECVD SiO2 on both wafer sides at 350 °C, ~300 nm/min**;
- vias to M1 by **CHF3/CF4/Ar RIE at ~360 nm/min**;
- Al/Cu M2 (not Au);
- dicing to 10 × 10 mm, then a **6:1 BOE 60 s undercut after dicing**.

**Leibrandt et al.** deposited 10 µm stress-balanced PETEOS "a micron or two and then a pause for thermal equilibration", warning of micro-voids that outgas. They kept all steps below 400 °C. Adding the Al ground plane raised the loaded Q from ≈100 to ≈150. Au/Sn (≈285 °C) was the cleanest die attach they tested ([arXiv:0904.2599](https://arxiv.org/pdf/0904.2599)).

**Electroplated Au (PTB).** Ti 15 nm / Au 50 nm seed, 16–25 µm resist mold, **sulphite (cyanide-free) Au bath**, resist strip plus O2 and F plasma, then **Ar etch of the Au seed (~50 nm/min) and F-plasma etch of the Ti (~10 nm/min)**. Result: **R_rms = 8.3(5) nm, ~100× smoother than aqua-regia seed removal** ([Bautista-Salvador 2019](https://arxiv.org/abs/1812.01829)). The thesis used Enthone Microfab Au 100-B (pH 7.5) with AZ nLOF 2070 and warns that Ti etchant (HF) attacks SiO2 ([Bautista-Salvador thesis, Ulm 2015](https://www.quantenbit.physik.uni-mainz.de/files/2015/11/PhDThesis_Bautista_Online.pdf)).

**Sussex (closest analogue).** **8 µm PECVD SiO2 under Cr/Au**, both dry-etched with the same resist mask. The oxide etch (4(1)% uniformity) stops **750(250) nm short of the ground plane**, then BOE finishes the etch and forms a **3(1) µm undercut**. They saw line-of-sight redeposition after ion-beam etching. An Al-ground-plane version trapped ions for 7–16 h with no adverse effects observed, though they later switched to Au to avoid charging of Al oxide ([Siegele-Brown QST 2022](https://arxiv.org/abs/2202.02313)).

**Dietl 2025 test protocol.** A room-temperature 120-needle probe card, run before dicing:

- continuity: 1 mA forced, pass at 0–100 mV, using two-pad "loop" DC electrodes;
- DC leakage: 50 V, pass at ≤100 nA;
- rf leakage: 300 V DC, pass at ≤100 nA, run twice to catch breakdown;
- resistance: 5 mV forced, pass at 0–50 Ω.

Yield was 54% ([arXiv:2505.21284](https://arxiv.org/html/2505.21284)).

**MIT.nano tools.** All of these appear in the July 2025 Fab.nano charge list: EBL-Elionix-HS50, Sputter-AJA, EBeam-Temescal-FC2800, PECVD-Oxford-TEOS, PECVD-Samco-PD220, RIE-F-Samco-230iP, RIE-PlasmaTherm-210RL, DRIE-SPTS-Pegasus, OxideEtch-HF-BOE-L06, Plating-U04, Clean-Ar-Plasma, Diesaw-DAD3240, Wirebond-Wedge, Filmstress-Tencor-FLX2320 and ProbeStation-Summit-11000 ([MIT.nano tool list PDF](https://nanousers.mit.edu/sites/default/files/documents/Fab.nano_ToolsetPricingExternal_July2025.pdf)). Plating-U04's bath chemistry, and whether it is a gold tank at all, was not verified. Whether any MIT.nano sputter tool offers the RF substrate bias that the Dane recipe needs was not verified either.

**Open process interactions in the composite flow.** These are not sourced and need witness wafers:

- BOE attack on Al M1 during the undercut finish;
- Ti undercut beneath the Au during BOE (Cr, which Sussex uses, resists HF);
- Au redeposition on pillar sidewalls during an Au-masked D2 RIE;
- whether ITO and the SNSPD cap survive any D2 RIE or BOE that reaches the detector window.

## Conclusion

The most useful correction from this literature is to the hypothesis. In a planar model, a grounded hole in a grounded electrode does not move the rf null. What moves it is boundary geometry along the rf rails: the termination about 83 µm away, the 6 µm step that breaks the planar model, and (from figure measurements) a narrowed rf channel. Todaro's "by design" plausibly means the designers used these effects deliberately to bring the ion closer and raise NA from 39 µm to 29 µm. Your readout zone can therefore be modelled the same way: decide where the rf rails end relative to the window, and check how deep the window is compared with 50 µm, since that ratio decides whether planar gds2itvg results hold there.

On the detector side, the literature shows grounded-mirror shielding works and that rf heating then becomes the limit. It does not show a fabricated ITO top shield with measured benefit, NbN under 10 µm of PECVD oxide, or a demonstrated q/m as low as Ba+. Those three gaps are where your design is untested, and where test structures and witness wafers will teach the most.

## Design implications

1. **Detector placement.** Precedent puts the SNSPD in an opening of an rf-ground (DC) centre electrode between the rf rails, with no electrode metal over it, ≈83 µm before the rf rails terminate (Todaro thesis Fig. 4.8, Fig. 4.9(a); PRL Fig. 1(b)) [distances from figure measurement].
2. **Expect the null to drop over the readout zone** if rf rails terminate nearby, the window is recessed, or the rf channel narrows. Todaro saw −10 µm at a nominal 39 µm, about −25% (PRL p. 2; thesis Sec. 6.3, Fig. 6.3). Separate the three causes with a 3D model before fixing the layout. Planar (gds2itvg) results over a recess deep relative to h are flagged as unreliable by the thesis (Sec. 6.3, p. 113).
3. **Collection geometry.** Todaro: 22 × 20 µm at 35 µm gives NA 0.32 and 2.0% capture (PRL p. 2; Supp. Eq. S6). Holding NA fixed means scaling the active-area side with the ion-to-detector distance, roughly 22 µm × (distance/35 µm) [team calc]. The upper bound is the rf–rf spacing, giving 3–8% solid angle (Slichter Sec. 2).
4. **Load-to-readout separation.** Precedent is 264 µm (≈6.8 h at 39 µm) with no line of sight from the load zone to the detector (PRL p. 3; thesis Sec. 6.3). Crosstalk is <2–4% at ≈80 µm (thesis Sec. 6.4.3; PRL Fig. 4).
5. **DC segment width.** W/h ≈ 0.78 maximises axial curvature, and the potential falls off for W/h < 0.5 (arXiv:quant-ph/0606237). At h = 50 µm that is W ≈ 40 µm minimum and ≈40–100 µm practical. Todaro's pitch was ≈44 µm at h = 39 µm [figure measurement]. Plan ≥5 independent DC degrees of freedom per zone [team inference].
6. **Gapless five-wire design formulas** [team calc, check against House 2008]: h = ½√(a(a+2b)), depth = κ·Q²V²/(4MΩ²h²) with κ_max ≈ 0.0091 at b/a ≈ 3.7 (Wesenberg Eqs. 9, 12, 30). Stability: q < 0.7 (Wesenberg Sec. V B). Keep q ≲ 0.4 for pseudopotential validity.
7. **Ba+ operating window at h = 50 µm** [team calc, gapless]: 30–50 MHz and 100–200 V give q ≈ 0.35–0.5, f_r ≈ 5–6 MHz and depth ≈ 0.13–0.26 eV. The MIT-LL precedent ran 41.1 MHz at f_r 1.9–3.3 MHz (Shi 2023). For ablation loading the optimal rf depth is ~0.1 eV (Shi Eq. 3/Fig. 3).
8. **RF tolerance of the shielded SNSPD is undemonstrated for Ba+.** Hampel demonstrated 54 V peak at 70 MHz and claims usability for q/m ≥ 0.01 e/u (Hampel final paragraphs). 138Ba+ is 0.0072 e/u. Required rf amplitude scales with frequency at fixed secular frequency (Hampel). Compare your chosen V and Ω against this envelope explicitly.
9. **Ground the mirror.** A floating mirror leaves induced rf currents; a grounded one removes them (Hampel Figs. 3–4). Ground through vias to the trap ground layer. Extend the ground under the SNSPD leads for several hundred µm, as Hampel's "large" mirror did (Hampel fabrication paragraph, Fig. 1).
10. **Leads.** Narrow leads to minimise C_RL, routed away from rf (Todaro Supp. "Trap fabrication"). Terminate both ends symmetrically to suppress the uniform induced current (Todaro Supp. Fig. S4; Slichter App. A).
11. **Readout filtering.** Expect rf pickup larger than the pulses. Budget a ≥40 dB notch at f_rf plus a low-pass (Todaro Supp. Fig. S2). Gate the bias to readout windows with ≈10 µs ramps (thesis Sec. 6.3.1).
12. **Where a top shield is needed.** The literature recommends a grounded transparent conductor (film or mesh) **on top of** any dielectric over the detector, both to stop surface charging and to screen click kicks (≈0.009 quanta/click unshielded) (Todaro Supp.; Hampel published version after Fig. 2; PRL p. 4). Check which surface the ion sees over your window.
13. **ITO parameters.** 40–60 nm is the optical optimum in the team TMM: NbN absorption ≈0.53 for 7 nm NbN, with ITO loss of 0.7–3% depending on k [team calc]. Resistivity 1–2 × 10⁻⁵ Ω·m as-sputtered (Eltony). It remains conductive at 6 K (Eltony; Lin & Li). Shield RC ≪ 1/f_rf for 40–400 Ω/sq [team calc].
14. **Spacer between Al and NbN.** Use ≈65 ± 15 nm (first order) or ≈230 nm (second order). Avoid ≈148 nm, which is a node [team TMM]. The second-order choice also puts more oxide between Al hillocks and the wire [team inference].
15. **Cap thickness.** ≈88 nm under 50 nm ITO. ±10 nm on spacer or cap costs ≤0.07 absorption [team TMM]. Final numbers need RCWA or FDTD.
16. **Coherent thick oxide.** The 10 µm oxide over the detector can modulate absorption between ≈0.46 and 0.63 [team TMM]. Either remove it over the window or treat it as a design variable.
17. **No stray-light rejection from the stack.** 650 nm light is absorbed at ≈55% of 493 nm efficiency [team TMM]. Keep the photoionisation beam (405/450/337 nm) and the 650 nm repump scatter away from the detector (Todaro PRL p. 4 on stray-light clicks).
18. **NbN recipe.** Use room-temperature RF-bias-sputtered NbN: ≈5 nm, R_s ≈ 600 Ω/sq, Tc ≈ 7.8–7.9 K (Dane 2017; Toomey 2018). The trap surface must then stay ≲6.2 K (Todaro's ≥25% Tc margin, PRL p. 2). Hampel's NbTiN, co-sputtered at 500 °C, ran to 6 K.
19. **No TMAH on bare NbN.** Use short develops followed by a ≥3 min running DI rinse. Budget ≈0.25 nm and 0.2 K lost per minute of 25% TMAH (Toomey Expt. 2).
20. **Cap the nanowire right after patterning.** Precedent: 130 nm PECVD SiO2 (Hampel), with HSQ left on (Najafi; Cheng). Todaro saw 12–30% resistance rises during plating-resist steps on uncapped MoSi (Supp.). Air oxidation is ≈0.8 nm/day initially (Medeiros).
21. **Thermal budget after Al.** JoVE PECVD runs at 350 °C, and Al hillocks are reported at ~350 °C. Use Al-1%Cu or a Ti/TiN cap (JoVE M1 step; SINTEF). Keep ITO anneals ≲250–300 °C [team inference]. Inert anneals to 500 °C preserve NbN Tc (arXiv:2501.07780).
22. **Deposit D2 in increments with balanced stress.** JoVE puts 14 µm on both wafer sides at 350 °C; Leibrandt uses 1–2 µm increments with pauses. Measure bow on the FLX2320.
23. **Gaps.** Aspect ratio > 1 (Bautista-Salvador). With 4–5 µm gaps, use ≥5–10 µm Au or an undercut (Chiaverini Sec. 6). Gap/h ≈ 0.1 keeps the gapless model approximately valid [team inference from Wesenberg Sec. II A].
24. **Breakdown.** For SiO2 over a conductor: V_b ≈ 356 V at 5 µm and ≈503 V at 10 µm (Sterling Eq. 1 with u = 1.4 × 10¹⁸ eV/m²) [team calc]. Measured precedents: >250 V_amp at 15 MHz with 8 µm oxide (Sussex) and 240 V across an 8 µm gap (JoVE). A SiN surface layer raises u ≈ 3.6×. Qualify on a sacrificial test chip.
25. **Plated Au recipe.** Ti/Au (or Cr/Au) seed and a sulphite bath. Remove the seed by Ar etch (~50 nm/min) plus F-plasma for the Ti (PTB). Stop the D2 RIE ≈0.75 µm above the ground plane and finish with BOE, giving a ≈3 µm undercut (Sussex). Dice before the undercut (JoVE).
26. **Beam path over the chip.** Keep it ≲±1 mm at 50 µm height (493 nm w ≤ 18 µm) by bowtie/notch or zones near the edge. Todaro used a 1.8 mm isthmus (Supp. Fig. S1). Keep wirebond pads off the beam-entry and beam-exit edges [team calc and inference].
27. **Loading.** Use a backside slot or a shielded oven, with an oven shutter (Graham 2014). Keep the slot ≥ a few h from the readout zone [team inference]. Ba+ lasers: 493 nm, 650 nm, 614 nm, and photoionisation at 791 + 337/450 nm or 553/554 + 405 nm (Graham; Shi).
28. **Pre-package electrical test.** Require >100 MΩ between every electrode pair including the ground plane (Stick). Dietl-style checks: 1 mA continuity, 50 V DC leakage, 300 V rf-line leakage at ≤100 nA. Add M2–M1 capacitor, comb and via-chain test structures [team inference]; expect ≈3.5 pF/mm² for 10 µm SiO2.

## Read these sections yourself

1. **Todaro PRL (arXiv:2008.00065v1).** Read p. 2 (ion heights, recess, NA, capture), Fig. 1(a)/(b) (scale diagram), p. 4 (heating, click kicks, shield proposal), Fig. 4 (count rate vs offset), and in the Supp. "Trap fabrication", "Experimental apparatus", and "SNSPD pulses and induced rf currents" with Fig. S4 and Eq. S1. Also read Fig. S1 (bowtie).
2. **Todaro thesis.** Read Sec. 4.2.1.2 (pp. 60–62) with Figs. 4.8–4.10, Sec. 4.2.1.3 with Fig. 4.11 (transport trap), App. B Table B.1, Sec. 5.3.1–5.3.2 (pp. 101–103), Sec. 6.3 (p. 113) with Fig. 6.3 (p. 114), Sec. 6.3.1, Sec. 6.6 (pp. 127–128), Sec. 8.1.1 (pp. 147–148), and Ch. 7 (transport, not yet extracted).
3. **Slichter 2017.** Read Sec. 2 (solid-angle and crosstalk rules, ITO caution), Sec. 3 with Fig. 2 (ring geometry), Sec. 4 with Eq. 1, and App. A (rf-current model).
4. **Hampel 2023.** Read the fabrication paragraph, Fig. 2(a)–(d) (shielding FEM), Figs. 3–4, and the final paragraphs (q/m, rf scaling). Read both the arXiv and the NIST APL PDF, since the published version adds the surface-charge and heating sentences.
5. **Eltony 2013.** Read the fabrication, resistivity and charging paragraphs.
6. **Wesenberg 2008.** Read Sec. II A and Eqs. 9, 12, 25, 28–30, and Sec. V B. The extracted equation text was garbled, so check every reconstructed formula against the PDF.
7. **Chiaverini 2005.** Read Fig. 4, Secs. 4–6, and App. A.
8. **Shi 2023.** Read Eq. 2, Eq. 3 with Fig. 3 (optimal depth), and the trap-parameter paragraph.
9. **Sterling 2013.** Read Eq. 1 and Figs. 2–3.
10. **Toomey 2018.** Read Expts. 1–2 and Fig. 4. **Medeiros 2019:** Table I and the oxidation section. **Dane 2017:** the full recipe, which was not retrieved.
11. **Fabrication papers.** Read JoVE 56060 (full protocol, including the Supplementary Document, which was not accessed), Siegele-Brown 2022 (fabrication section), Bautista-Salvador 2019 (fabrication section), Leibrandt 2009 (stack and packaging), Stick 2010 (Fig. 1 and packaging), and Dietl 2025 (test protocol and Table 2).

## References

Verified means the ID was checked in the research notes (DOI on Crossref or a publisher page, or the arXiv listing opened).

| Ref | Status |
|---|---|
| S. L. Todaro et al., PRL 126, 010501 (2021), DOI 10.1103/PhysRevLett.126.010501, arXiv:2008.00065 | Verified |
| S. L. Todaro, Ph.D. thesis, Univ. Colorado Boulder (2020), [NIST PDF](https://www.nist.gov/document/susanna-todaro-phd-thesis) | Verified (no DOI) |
| D. H. Slichter et al., Opt. Express 25, 8705 (2017), DOI 10.1364/OE.25.008705, arXiv:1611.09949 | Verified |
| B. Hampel et al., APL 122, 174001 (2023), DOI 10.1063/5.0145077, arXiv:2302.01462 | Verified |
| A. M. Eltony et al., APL 102, 054106 (2013), DOI 10.1063/1.4790843, arXiv:1212.1443 | Verified |
| Sedykh et al., Tech. Phys. 2025 no. 9, p. 1577 ([Ioffe](https://journals.ioffe.ru/articles/61926)) | **DOI not retrieved; abstract only** |
| Jansson et al., arXiv:2411.10361 (related DOI 10.1364/AO.547471 listed on arXiv) | arXiv verified; journal DOI as listed |
| J. J. Lin & Z. Q. Li, JPCM 26, 343201 (2014), arXiv:1702.07845 | arXiv verified |
| K. M. McPeak et al., ACS Photonics 2, 326 (2015), DOI 10.1021/ph5004237 | Via refractiveindex.info |
| Banerjee et al., Opt. Mater. Express 8, 2072 (2018); dataset DOI 10.5525/gla.researchdata.637 | Dataset verified |
| O. Medeiros et al., arXiv:1812.05559 | **Journal version unverified** |
| A. E. Dane et al., APL 111, 122601 (2017), DOI 10.1063/1.4990066 | Verified via DSpace record; full text not read |
| M. Toomey et al., JVST B 36, 06JC01 (2018), DOI 10.1116/1.5047427 | Verified |
| F. Najafi et al., Nat. Commun. 6, 5873 (2015), DOI 10.1038/ncomms6873 | Verified |
| J. Chiaverini et al., QIC 5, 419 (2005), arXiv:quant-ph/0501147 | Verified (arXiv) |
| J. H. Wesenberg, arXiv:0808.1623 | arXiv verified; **PRA 78, 063410 unverified** |
| M. G. House, PRA 78, 033402 (2008), DOI 10.1103/PhysRevA.78.033402 | DOI resolves; full text not read |
| Y. Shi et al., APL 122, 264002 (2023), DOI 10.1063/5.0149778 | Verified |
| R. D. Graham et al., AIP Adv. 4, 057124 (2014), DOI 10.1063/1.4879817; arXiv:1305.2224 | Verified |
| arXiv:quant-ph/0606237 (railway-track transport model) | **Authorship (Huber et al.?) unverified** |
| arXiv:1007.3542 (segment optimisation for separation) | **Attribution (Nizamani & Hensinger?) unverified** |
| S. C. Doret et al., NJP 14, 073012 (2012), arXiv:1204.4147 | Verified |
| J. A. Sedlacek et al., PRA 97, 020302(R) (2018), arXiv:1712.00188 | Verified |
| M. Brownnutt et al., arXiv:1409.6572 | arXiv verified; **RMP 87, 1419 from memory** |
| arXiv:1906.06489 (β ≈ 2.6) | arXiv only; authors not recorded |
| A. Bautista-Salvador et al., NJP 21, 043011 (2019), arXiv:1812.01829 | Verified |
| A. Bautista-Salvador, Ph.D. thesis, Univ. Ulm (2015) | PDF opened |
| R. C. Sterling et al., APL 103, 143504 (2013), DOI 10.1063/1.4824012 | Verified |
| Z. D. Romaszko et al., Nat. Rev. Phys. 2, 285 (2020), DOI 10.1038/s42254-020-0182-8, arXiv:1908.00267 | Verified |
| D. Stick et al., arXiv:1008.0990 | arXiv verified; **journal venue unverified** |
| S. Hong et al., J. Vis. Exp. (2017), DOI 10.3791/56060 | DOI verified; **volume "126, e56060" unverified** |
| D. R. Leibrandt et al., QIC 9, 901 (2009), arXiv:0904.2599 | arXiv verified; journal ref as cited by Stick |
| M. Siegele-Brown et al., Quantum Sci. Technol. (2022), DOI 10.1088/2058-9565/ac66fc, arXiv:2202.02313 | Verified |
| T. Tanaka et al., arXiv:2101.00459 | arXiv verified |
| M. Dietl et al., arXiv:2505.21284 | arXiv verified; **Adv. Quantum Technol. 8, e00412 unverified** |
| M. C. Revelle, arXiv:2009.02398 | arXiv verified |
| Annealed-NbN Tc study, arXiv:2501.07780 | arXiv only |
| SINTEF Al hillock publication 1155451 | Web record only |
| MIT.nano Fab.nano Toolset Pricing (July 2025) PDF | Verified document |
