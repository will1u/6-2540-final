# Electrical effects of bond pad size over a buried Al ground plane (RF trap electrodes, DC electrodes, NbN SNSPD readout)

> **Claude-authored** research notes (raw; the citations here are not yet entered in `references_design.bib`).

Stack assumed throughout (from the task brief and the repo fab docs): 6 um plated Au pads/leads on 10 um PECVD SiO2 (D2), eps_r 3.9-4.5, over a continuous Al ground plane (M1), on high-resistivity Si. RF: 53 V amplitude, 28 MHz, one RF electrode with a 200 x 200 um pad and a ~2.7 mm x 60 um lead. About 36 DC electrodes, each with a 120 x 200 um pad and a 6 um x 5-8 mm lead. NbN SNSPD (30 x 30 um meander, 100 nm wire, 7 nm NbN) with two Ti/Au pads (~150 x 120 um, D2 opened over 120 x 90 um). From `design/fab/TRAVELER.md` and `mask_list.md`: the SNSPD leads are 4 um wide Ti/Au (10/350 nm) on a 238 nm PECVD SiO2 spacer over the Al, run ~4.5 mm under the centre DC electrode, and the Al has 260 x 220 um cut-outs under the SNSPD pads.

Labels: **[team calc]** = calculation done for these notes (not from a source; method and inputs given inline). Everything else has an inline source.

---

## 1. Pad capacitance to the buried ground plane vs leads vs electrodes

### Takeaway
A 200 x 200 um pad over 10 um SiO2 is ~0.15 pF parallel-plate, or ~0.17 pF with fringe. That is about a quarter of the RF lead's ~0.74 pF and ~5% of the >= 3.4 pF on-chip RF total (the 84 um rails alone are >= 2.5 pF). It is small next to the ~17-20 pF that a full trap, vacuum feedthrough and wiring load typically puts on the resonator. For DC electrodes the 6 um x 5-8 mm leads (0.3-0.5 pF) give 3-5x the capacitance of the 120 x 200 um pads (~0.1 pF). For the SNSPD, the 4 um leads on the 238 nm spacer over Al (~3.4 pF each) dominate completely. The pads sit over Al cut-outs and add almost nothing.

### Cited Findings
- Parallel-plate relation used for trap dielectrics: eps' = C d / (eps0 A), with loss conductance G = omega C tan(delta). — [Hughes et al. 2011, "Microfabricated ion traps", Sec. V.2](https://ar5iv.arxiv.org/html/1101.3207)
- Microstrip quasi-static formulas (Hammerstad 1975) used below for fringe-inclusive capacitance per length: for w/h <= 1, Z = Z0/(2 pi sqrt(eps_eff)) ln(8h/w + w/4h); for w/h >= 1, Z = Z0/(sqrt(eps_eff)[w/h + 1.393 + 0.667 ln(w/h + 1.444)]); eps_eff = (eps_r+1)/2 + (eps_r-1)/2 F, with F = (1+12h/w)^-1/2 (+0.04(1-w/h)^2 for w/h <= 1). Capacitance per length C' = sqrt(eps_eff)/(c Z). The page attributes these to Hammerstad, 1975 European Microwave Conf., pp. 268-272, and Garg, Bahl & Bozzi, *Microstrip Lines and Slotlines* (2013), and says to check exact forms against the primary texts. — [Wikipedia, "Microstrip"](https://en.wikipedia.org/wiki/Microstrip)
- Literature anchor for this exact stack: GTRI's trap uses a 1 um Al ground plane under 10 um low-stress PECVD SiO2, with RF/DC electrodes, leads, capacitor plates and wire bond pads all in the Al layer above. "10 um is adequate to reduce the RF-electrode capacitance to [~]1 pF". A glyph before "1" was lost in PDF extraction, so read it as approximately 1 pF. RF rails are 30 and 50 um wide. — [Doret et al. 2012, NJP 14, 073012, Secs. 2 and 3](https://arxiv.org/pdf/1204.4147)
- A whole-system RF load reference: an ion trap plus vacuum system measured at 17 +/- 2 pF and ~0.1 ohm. Siverns et al. built and tested resonators for trap loads of C_T = 2-85 pF and R_T = 0.1-10 ohm. — [Siverns et al. 2012, Appl. Phys. B 107, 921, Sec. V and Conclusion](https://arxiv.org/pdf/1106.5013.pdf)
- Sussex 2D-lattice chip (10 um buried SiO2, SOI): "The chip capacitance was measured to be 19 +/- 1 pF." — [Sterling et al. 2014, Nat. Commun. 5, 3637](https://ar5iv.arxiv.org/html/1302.3781)

**[team calc] Capacitance table** (h = 10 um D2. Pads use parallel-plate plus an edge fringe of 0.029 pF/mm of perimeter at eps_r = 4.2, taken from a 200 um-wide Hammerstad microstrip minus its parallel-plate part and divided by two edges. Leads use Hammerstad microstrip with air above. The table ignores lateral capacitance to neighbouring electrodes and grounded fill across 5-10 um gaps, which adds more):

| Element | eps_r = 3.9 | 4.2 | 4.5 | Note |
|---|---|---|---|---|
| RF pad 200 x 200 um | 0.160 pF | 0.172 pF | 0.184 pF | PP only 0.138-0.159 pF |
| RF lead 60 um x 2.7 mm | 0.69 pF | 0.74 pF | 0.79 pF | 0.27 pF/mm; Z0 ~23 ohm; PP only 0.60 pF |
| DC pad 120 x 200 um | 0.101 pF | 0.108 pF | 0.115 pF | PP only 0.089 pF at 4.2 |
| DC lead 6 um x 5 mm | 0.30 pF | 0.32 pF | 0.34 pF | 0.063 pF/mm; w/h = 0.6, so fringe ~ 2x PP; Z0 ~91 ohm |
| DC lead 6 um x 8 mm | 0.48 pF | 0.51 pF | 0.54 pF | |
| SNSPD pad 150 x 120 um *if* it sat over Al through 10 um | 0.077 pF | 0.083 pF | 0.088 pF | In the actual design the Al is cut out under it (see below) |
| SNSPD lead 4 um x 4.5 mm on 238 nm SiO2 over Al | 3.1 pF | 3.4 pF | 3.6 pF | 0.75 pF/mm; Z0 ~9 ohm; fully embedded in SiO2, so eps_r is used directly |

### Inferences
- [team calc] Fringe matters most for narrow features. For the 6 um DC leads (w/h = 0.6) the true capacitance is ~2.8x the parallel-plate value. For the 200 um pad, fringe adds only ~15%.
- [team calc] The RF electrode network on chip is pad (0.17 pF) + lead (0.74 pF) + the RF rails. `design/CLAUDE.md` gives two 84 um-wide RF rails that run >= 1.7 mm past both zones (zones 600 um apart), so each rail is >= ~4.0 mm long. Parallel-plate only, that is 2 x 84 um x 4.0 mm x eps0 x 4.2 / 10 um ~ 2.5 pF (a lower bound: no fringe, no lateral capacitance to the DC electrodes across the 5 um gaps). Total on-chip RF capacitance is therefore >= ~3.4 pF, about 3x Doret's ~1 pF (Doret's rails are narrower, 30 and 50 um). The RF pad is ~5% of the on-chip RF capacitance and <1% of a ~20 pF system load.
- [team calc] Scaling: pad C goes as area. Halving the RF pad to 100 x 100 um saves ~0.11 pF. Shortening or narrowing the RF lead gives comparable or bigger savings per unit of layout change.
- The SNSPD pads sit over Al cut-outs (260 x 220 um, per TRAVELER), so their capacitance is to the Si substrate through ~1 um thermal SiO2. At 4 K the high-resistivity Si is expected to be insulating ([Romaszko 2020 Sec. 3.2](https://arxiv.org/pdf/1908.00267v3) notes Si "can even act as an insulator" at cryogenic temperatures), so this capacitance is small and floating. The lead-to-Al capacitance (~3.4 pF per lead) is what the SNSPD circuit sees.

### Gaps
- The exact RF rail length and the rail-to-DC lateral capacitance were not extracted from the GDS, so the >= 3.4 pF total is a lower bound. Running the GDS through `gds2itvg`/a capacitance extractor (or simple area x eps/h per polygon) would close this.
- Lateral (coplanar) capacitance from each pad to grounded fill across 5-10 um gaps is not included. With 6 um-thick Au and 5-10 um gaps the sidewall term is not negligible; it needs a 2D/3D field solve.
- No source found giving measured RT eps_r for the team's specific PECVD recipe; 3.9-4.5 is the brief's range.

---

## 2. RF electrode: resonator loading, dielectric loss, and chip heating

### Takeaway
Total RF capacitance sets the helical-resonator frequency (omega0 = 1/sqrt(L sum C)) and, through kappa = (L/C)^1/4 and Q, the voltage reached per watt. The RF pad's ~0.17 pF shifts a ~20 pF system by ~0.4% in frequency and ~0.2% in kappa, which is negligible. Dielectric loss P = 1/2 omega C V^2 tan(delta) at 53 V and 28 MHz is ~0.25 mW per pF at tan(delta) = 1e-3 and ~2.5 mW per pF at 1e-2. For the pad alone that is 0.04-0.4 mW. That is small in absolute terms, but at tan(delta) ~ 1e-2 the on-chip dielectric can pull the loaded Q down by 10-30%, and the leads and rails contribute 5-10x more than the pad.

### Cited Findings
- Helical resonator model: resonant frequency omega0 = 1/sqrt((C_s + C_t + C_w + C_c) L_c), with C_s the shield capacitance, C_t the trap, C_w the wires and C_c the coil self-capacitance (Eq. 21). Q = X_Lc / R_ESR (Eq. 22), with R_ESR ~ R_j + R_c + R_s + gamma^2 R_t (Eq. 24) and gamma = a/(a+1), a = C_t/(C_s + C_w). High Q comes from maximising coil inductance and minimising system capacitance, and stray capacitances "can be on the same order of magnitude as the ion trap capacitance". — [Siverns et al. 2012, Sec. III.B](https://arxiv.org/pdf/1106.5013.pdf)
- Output voltage: V_rms = kappa sqrt(P Q), kappa = (L/C)^1/4. Measured example: a 17 +/- 2 pF trap + vacuum system gave omega0 = 2 pi x 21.895 MHz and Q = 477 +/- 28. 1.0 W gave 400 +/- 20 V (from secular-frequency BEM fit), so kappa = 12.9 +/- 1.4. — [Siverns et al. 2012, Sec. V](https://arxiv.org/pdf/1106.5013.pdf)
- Power dissipation in trap structures: P_d = 1/2 V0^2 Omega^2 C^2 R (series-resistance limit), full form P_d = V0^2 Omega^2 C^2 R (1+tan^2 delta)^2 / [2(1 + Omega^2 C^2 R^2 (1+tan^2 delta)^2)]. Loss conductance G = omega C tan(delta), and tan(delta) ~ eps''/eps'. High dissipation "can result in heating and destruction of trap structures". Typical drive 10-80 MHz. — [Hughes et al. 2011, Sec. V.2](https://ar5iv.arxiv.org/html/1101.3207)
- Measured loss tangents at 1 MHz for MOS-type stacks (these include the doped-Si substrate, so they are upper bounds for a stack screened by a ground plane): Au/SiO2/n-Si ~0.05; Au/Si3N4/p-Si ~0.025; Cr/SiO1.4/Au ~0.09; Rogers PCB 0.0031. — [Hughes et al. 2011, Secs. V.2, VI.1](https://ar5iv.arxiv.org/html/1101.3207)
- Low-temperature, low-power microwave loss tangents: PECVD SiO2 2.7-2.9 x 10^-3; thermal SiO2 0.30-0.33 x 10^-3 (below 100 mK, near single-photon excitation, with TLS loss unsaturated). — [O'Connell et al. 2008, APL 92, 112903](https://arxiv.org/pdf/0802.2404)
- The ground plane is there for loss: mid-resistivity Si (10^2-10^4 ohm cm) is very lossy at RF. A metal ground plane between the RF electrode and the substrate "almost guarantees the successful shielding of the substrate from RF dissipation". — [Romaszko et al. 2020, Nat. Rev. Phys. 2, 285, Sec. 3.2 (arXiv:1908.00267)](https://arxiv.org/pdf/1908.00267v3)
- GTRI: the 10 um PECVD SiO2 "limits the capacitance and power dissipation of the RF electrodes", and the RF rail widths were chosen partly to keep "power dissipation low". — [Doret et al. 2012, Sec. 2](https://arxiv.org/pdf/1204.4147)
- Observed on-chip RF heating at 4 K: NIST trap-integrated NbTiN SNSPDs warmed by ~0.5 K, inferred from switching current, with 45 V peak at ~70 MHz on 350 nm-thick Au electrodes. The authors attribute this to on-chip RF dissipation and expect less with 6 um Au. — [Hampel et al. 2023, APL 122, 174001](https://arxiv.org/pdf/2302.01462)
- At high power, Sussex applied "up to 30 W of rf power" to a 19 pF chip during flashover tests, mostly dissipated on chip. — [Sterling et al. 2014](https://ar5iv.arxiv.org/html/1302.3781)

### Inferences
- [team calc] RF current into capacitance: I = omega C V = 9.3 mA per pF at 53 V, 28 MHz. Au skin depth at 28 MHz is ~15 um (rho = 2.44e-8 ohm m), so 6 um Au carries current through its full thickness. R_sheet ~ 4 mohm/sq at room temperature, and the 2.7 mm x 60 um lead is ~45 squares = 0.18 ohm. Joule loss in the lead for a 1 pF load is ~8 uW, i.e. negligible next to dielectric loss unless tan(delta) < ~1e-5.
- [team calc] Dielectric loss P = 1/2 omega C V^2 tan(delta), V = 53 V, f = 28 MHz:

| C on chip | tan(delta) = 1e-3 | tan(delta) = 1e-2 |
|---|---|---|
| 0.15 pF (RF pad alone) | 0.037 mW | 0.37 mW |
| 0.6 pF (RF lead alone, PP) | 0.15 mW | 1.5 mW |
| 1 pF | 0.25 mW | 2.5 mW |
| 2 pF | 0.49 mW | 4.9 mW |

- [team calc] Resonator loading. Adding dC to C_tot shifts f0 by ~ -dC/(2 C_tot) and kappa by ~ -dC/(4 C_tot). For C_tot = 20 pF, the RF pad (0.15 pF) gives -0.37% in f0 and -0.19% in kappa. A full 1 pF of on-chip RF metal gives -2.4% and -1.2%. For C_tot = 10 pF the shifts double.
- [team calc] Q degradation from on-chip dielectric loss: Q_diel = C_tot/(C_chip tan(delta)), combined as 1/Q = 1/Q0 + 1/Q_diel. With Q0 = 477 (Siverns example) and C_tot = 20 pF: C_chip = 1 pF at tan(delta) = 1e-2 gives Q = 385 (V down 10%); at 1e-3 it gives Q = 466 (V down 1%). The pad alone at 1e-2 gives Q = 461 (V down 2%). With C_tot = 10 pF and C_chip = 2 pF at 1e-2, Q drops to 244 (V down 28%).
- [team calc] Applied to this die's >= 3.4 pF on-chip RF capacitance (Section 1): dielectric loss is >= 0.84 mW at tan(delta) = 1e-3 and >= 8.4 mW at 1e-2. With C_tot = 20 pF and Q0 = 477, Q falls to ~441 (V down 4%) at 1e-3 and ~263 (V down 26%) at 1e-2. The pad's share of either number is ~5%.
- [team calc] Power budget check: with Siverns' kappa = 12.9 and Q = 477, 53 V amplitude (37.5 V rms) needs P = (V_rms/kappa)^2 / Q ~ 18 mW of input. On-chip dielectric loss of 0.25-2.5 mW per pF is therefore a significant fraction of the total budget if tan(delta) is near 1e-2. The pad's share stays sub-mW.
- At 4 K with 53 V across 10 um (~5 V/um), two-level-system loss in PECVD SiO2 is expected to be power-saturated, so O'Connell's low-power 2.8e-3 is probably an upper bound for the cryogenic case. This is an inference from TLS physics and was not measured at these fields in any source found.
- Heating: a few mW dissipated in D2 under the leads and rails is the scale to compare against the 4 K stage's cooling budget and against Hampel's observed ~0.5 K SNSPD warming. The pad is not the main heater; leads and rails near the SNSPD matter more because of proximity.

### Gaps
- No primary measurement of RT tan(delta) for PECVD SiO2 at ~28 MHz in a metal/SiO2/metal (ground-plane-screened) stack was found. The brief's 1e-3 to 1e-2 range is not verified. Hughes' 0.025-0.09 values include doped-Si substrate loss.
- Wilpers 2012 (NPL monolithic 3D trap), Stick 2010 (Sandia), and Kumph/Hensinger RF-loss papers were not retrieved in this pass. Their RF capacitance and dissipation numbers are unverified here.
- No source found giving a measured chip temperature rise vs RF dissipation for a ground-plane trap at 4 K.

---

## 3. DC electrodes: RF pickup and the role of pad/lead capacitance and filter capacitors

### Takeaway
RF pickup on a DC electrode is set by the capacitive divider C_coupling/(C_coupling + C_to_ground), as long as the off-chip filter is "far away" electrically. The intrinsic pad + lead capacitance to the buried Al (~0.4-0.6 pF per DC electrode) does act as a small built-in shunt, and a bigger DC pad helps slightly. But it is ~100x smaller than the dedicated on-chip capacitors used in practice (60 pF in Doret 2012), so pad area is not a useful filter knob.

### Cited Findings
- GTRI on-chip capacitors: 1 mm^2 plates in the DC leads (middle Al layer vs top-level ground over 1 um SiO2) give 60 pF to ground. With the DC-to-RF stray capacitance of ~1.4 x 10^-3 pF, the divider suppresses RF pickup by ~4.3 x 10^4. Capacitors must sit close to the trap, because their effectiveness "is impaired by any intervening resistance or inductance, such as that of a lead between the trap and a vacuum feedthrough". Such capacitors are "an essential element for reducing RF pickup on these control electrodes". — [Doret et al. 2012, Sec. 2.3](https://arxiv.org/pdf/1204.4147)
- Sussex 2D lattice: "820 pF capacitors were wire bonded to the static electrodes" for RF grounding. — [Sterling et al. 2014](https://ar5iv.arxiv.org/html/1302.3781)
- Guise et al. mounted a bare-die RC filter array (35 kohm, 220 pF) on the PCB next to the trap. On-chip meander resistors (Seidelin et al.) have also been integrated as part of DC filters. — [Romaszko et al. 2020, Sec. on integrated passives](https://arxiv.org/pdf/1908.00267v3); [Hughes et al. 2011, Sec. VI.2](https://ar5iv.arxiv.org/html/1101.3207)

### Inferences
- [team calc] Divider estimate with only the intrinsic capacitance (53 V RF): for C_coupling = 1.4 fF (Doret's value; ours must be computed from our geometry), C_gnd = 0.5 pF gives ~150 mV of RF on the DC electrode, and C_gnd = 1 pF gives ~74 mV. With a 60 pF on-chip capacitor it drops to ~1.2 mV. For C_coupling = 10 fF (e.g. a DC lead running alongside the RF lead), it is ~0.5-1 V with intrinsic C only and ~9 mV with 60 pF.
- [team calc] Increasing a DC pad from 120 x 200 um (0.108 pF) to, say, 200 x 200 um (0.17 pF) raises C_gnd by ~0.06 pF on a ~0.4-0.6 pF total, i.e. ~10-15% less pickup. Real but minor. A dedicated capacitor, or a top-ground MIM plate as in Doret, is ~100x more effective per unit area: a thin dielectric gives C/A = eps/d, so 1 um SiO2 is 10x denser than the 10 um D2.
- The intrinsic DC-to-ground capacitance through D2 is distributed along the lead, right at the electrode, so it is free of bond-wire inductance. That is its one advantage over a carrier-mounted capacitor (consistent with Doret's placement argument).
- DC pad capacitance is irrelevant for the DC voltages themselves. For fast shuttling waveforms it adds to the load the DAC/filter drives, but 0.1 pF is negligible next to typical 100s-of-pF filter capacitors (Romaszko/Guise 220 pF).

### Gaps
- Our actual DC-to-RF coupling capacitances (electrode-to-rail and lead-to-lead) were not computed. They need a field solve of the layout. The pickup figures above are illustrative.
- No verified source found for a typical bond-wire inductance per mm (often quoted as ~1 nH/mm) to quantify how much a carrier capacitor loses to the bond wire at 28 MHz.

---

## 4. SNSPD: pad/lead parasitics, reset time, latching, RF pickup, readout bandwidth

### Takeaway
SNSPD reset is set by L_k/R_L (~50-70 ns expected for this 4.5 mm-long, 100 nm-wide NbN meander into 50 ohm). The ~3.4 pF lead-to-Al capacitance gives an R_L C of only ~0.15 ns and leaves the circuit ~100x overdamped, so pad and lead capacitance do not affect reset or latching. RF pickup is the real issue. The induced current scales as omega C V, which is ~9 uA per fF of nanowire/lead-to-RF coupling at 53 V and 28 MHz, comparable to NbN switching currents. Grounded metal under the detector and leads (here the Al plane), narrow leads, and keeping the leads away from RF electrodes are the measures demonstrated in the literature. Pad size is secondary unless the pads are near RF.

### Cited Findings
- Reset time is limited by kinetic inductance: devices of usable size and high efficiency have reset times "orders of magnitude longer than their intrinsic photoresponse time". L_k was measured from the phase of a reflected microwave signal. — [Kerman et al. 2006, APL 88, 111116 (arXiv physics/0510238)](https://arxiv.org/abs/physics/0510238)
- tau_r = L_K/R_L. Full reset ~3 tau_r. Reset can be sped up by increasing R_L or decreasing L_K, but if tau_r is too small the device latches into a finite-voltage state. Latching happens if the hotspot cools too slowly relative to L_K/R_L, and the hotspot heating is set by the inductive energy ~1/2 L_K I_b^2. "We can therefore eliminate latching in any device by sufficiently reducing R_L." NbN latches less than Nb because of its shorter electron-phonon time. Example values: L_K = 15-235 nH (including ~10 nH of measurement leads), R_L = 15-50 ohm. — [Annunziata et al. 2010, JAP 108, 084507 (arXiv:1008.0895)](https://arxiv.org/pdf/1008.0895)
- Annunziata's latching pulse shows slow decay from the AC coupling of the amplifier, so the readout's low-frequency cutoff shapes the observed pulse. — [Annunziata et al. 2010, Fig. 2 discussion](https://arxiv.org/pdf/1008.0895)
- NIST trap-integrated MoSi SNSPD (Todaro): SNSPD leads were made "much narrower than typical SNSPD leads, a design choice made to minimize capacitive coupling to the trap rf electrodes". 350 nm Au was added on the leads "to reduce their series resistance and thus prevent SNSPD latching". Total nanowire inductance was 2.2 uH. One terminal was grounded near the chip, the other went via 50 ohm coax through a bias tee. The amplifier chain gives 46 dB over 1 MHz-1 GHz, with a 25 MHz LPF and a 67 MHz notch. Bias pulses were ramped over 11 us to avoid bias-tee ringing. RF pickup at the trap frequency was "several times larger" than the SNSPD pulses. Trap RF reduced the maximum usable bias current (I_m ~5.3 uA vs switching current ~8.9 uA). — [Todaro et al. 2021, PRL 126, 010501 (arXiv:2008.00065), main text and Supplement](https://www.arxiv.org/pdf/2008.00065)
- Todaro's induced-RF-current circuit model: the nanowire is an LC transmission line with capacitance C_RN per segment to the RF electrode. The leads have capacitance C_RL to the RF electrode plus series L_L ~5 nH and R_L ~5 ohm. The spatially uniform induced current "increases with C_RL and with the asymmetry in termination impedances and decreases linearly with the total nanowire inductance". Direct nanowire coupling C_RN adds a spatially varying current, 90 degrees out of phase. — [Todaro et al. 2021 Supplement, Fig. S4](https://www.arxiv.org/pdf/2008.00065)
- Hampel (NIST, NbTiN): a grounded Al mirror under the SNSPD reduces the simulated RF field at the nanowire by ~10x. A large mirror covered the leads "for several hundred um away from the rf electrode". A floating mirror performed worse (switching-current reduction and BCR flattening) than a grounded one. Devices ran at up to 54 V peak at 70 MHz and up to 6 K: ~10x more RF tolerance than Todaro and >= 2.5 K higher temperature. NbTiN switching currents are ~10x MoSi. Pulse decay was 25 ns (L_k = 1.3 uH, for a 20 x 30 um, 90 nm-wide meander). Bias went through a 10 kohm series resistor and bias tee, and output was notch filtered to remove RF pickup. With grounded mirrors, the residual RF effect looks like heating rather than induced current. — [Hampel et al. 2023, APL 122, 174001 (arXiv:2302.01462)](https://arxiv.org/pdf/2302.01462)

### Inferences
- [team calc] Kinetic inductance of our meander: 150 lines x 30 um = 4.5 mm of 100 nm wire = 45,000 squares. Using the dirty-limit BCS relation L_k,sq = hbar R_sq/(pi Delta), Delta = 1.76 k_B T_c, with R_sq ~ 400 ohm/sq (team estimate in TRAVELER) and T_c = 7.5-9 K: L_k,sq ~ 60-75 pH/sq, so L_k ~ 2.8-3.3 uH and tau = L_k/50 ohm ~ 55-66 ns. This is consistent in scale with Todaro's 2.2 uH and Hampel's 1.3 uH. (The BCS relation is standard but was not re-verified from a primary source in this pass.)
- [team calc] Lead capacitance effect. The circuit is L_k in series with (R_L || C_par), with C_par ~ 3.4 pF per lead. R_L C_par = 0.15 ns (pole near 1 GHz). The characteristic equation L R C s^2 + L s + R = 0 is overdamped when L > 4 R^2 C; here L/(4R^2C) ~ 100. So there is no ringing, the reset time is unchanged, and latching (set by L_k/R_L vs hotspot cooling) is unaffected. Parasitic C only matters if it approaches L_k/(4 R_L^2) ~ 300 pF, or if the amplifier is >~1 GHz bandwidth and the rising edge (timing jitter) matters.
- [team calc] Pad capacitance (~0.08 pF if over Al; less over the cut-out) is ~40x smaller than the lead capacitance, so pad size is electrically irrelevant for reset, latching and pulse shape. Pad size is a bonding/yield choice for the SNSPD.
- [team calc] RF pickup scale: I = omega C V = 9.3 uA per fF of capacitance to the RF electrode at 53 V, 28 MHz. That is comparable to Todaro's ~9 uA switching current. So even a few fF of uncompensated coupling (unequal on the two leads, per Todaro's model) can matter. NbN with ~10x higher I_sw (by analogy with Hampel's NbTiN) has more margin.
- In this layout the SNSPD pads are at the left die edge (x ~ -4750 um) while the RF pad is at the right edge (x ~ +4700 um), so pad-to-RF coupling is negligible. The coupling that matters is near the readout zone, where the meander and leads are close to the RF rails. The leads run under the grounded/DC-biased centre electrode and over grounded Al, which is the Hampel-style configuration. The ~3.4 pF lead-to-Al capacitance is a low impedance at 28 MHz (~1.7 kohm), next to a fF-level coupling impedance (~6 Mohm per fF), so it shunts RF coupled onto the leads to the local ground. That works only if the Al plane is well grounded at RF; a floating mirror was worse in Hampel.
- Readout bandwidth: SNSPD pulses have ~sub-ns rise and ~50-70 ns decay. A 4.5 mm lead is ~lambda/30 at 1 GHz in SiO2, so it is electrically short and its ~9 ohm characteristic impedance does not need matching for MHz-to-~1 GHz readout. Pad RF/microwave impedance does not limit bandwidth. The 28 MHz trap RF sits inside the pulse spectrum, so it has to be notched as Todaro and Hampel did.
- Because L_k/R_L sets latching, adding series resistance in the leads (thin Ti/Au) raises R_L slightly. Todaro thickened leads to 350 nm Au for exactly this reason, and the team's 10/350 nm Ti/Au matches.

### Gaps
- Natarajan, Tanner & Hadfield 2012 (SNSPD review) and Kerman 2009 (electrothermal feedback, PRB) were not retrieved, so their pad/readout recommendations are not cited here.
- No source found giving explicit recommended SNSPD bond pad sizes. Literature pads are chosen for wire bonding, and no source treats pad size as an electrical parameter.
- Our actual C_RN/C_RL (meander and leads to RF rails) are not computed. They need a field solve like Todaro's.
- Setzer 2021 (trap-integrated SPAD, Sandia) was not retrieved. Hampel notes SPADs "suffer from the same rf pickup effects".

---

## 5. Dielectric breakdown, flashover and charging at high-voltage pads

### Takeaway
At 53 V the 10 um PECVD SiO2 is far from bulk breakdown: even 1 MV/cm gives ~1 kV, and thin-film PECVD values are 4-12 MV/cm. Surface flashover across 5-10 um gaps is the real limit. Measured microfabricated-trap flashover is in the hundreds of volts to ~1 kV range, with RF ~20% below static. A buried conductor (ground plane or Si) under the gap lowers flashover by ~30%. Pad size itself does not change breakdown; the gap to grounded fill and the edge quality do.

### Cited Findings
- Bulk breakdown V_c = d E_c, with E_c proportional to d^-n, n ~ 0.5-1, so thinner dielectrics do not raise breakdown voltage proportionally. Surface flashover V_b proportional to d^alpha, alpha ~ 0.5. The surface breakdown field is ~2.5x lower than bulk breakdown of the same material (dielectric 1-3.9 um, lengths 5-600 um). — [Hughes et al. 2011, Sec. V.1](https://ar5iv.arxiv.org/html/1101.3207)
- Sterling 2013 tested Au electrodes (500 nm, on Cr) on quartz with 3-15 um gaps, static and RF (22 MHz), at ~5 x 10^-4 Pa. RF flashover erodes the closest electrode edge along its whole length. Flashover lowers resonator Q, which can quench and then re-strike the discharge. With PECVD a-SiO on a Si substrate (a conductor under the surface), flashover dropped ~30% vs a-SiO on quartz, because field lines concentrate at the triple point. PECVD SiN raised flashover ~3.6x vs a-SiO. Process changes "more than double the flashover voltage". — [Sterling et al. 2013, APL 103, 143504 (arXiv:1208.5672)](https://www.arxiv.org/pdf/1208.5672)
- Sussex 2D lattice with an undercut (60 um into a 10 um buried SiO2) to lengthen the flashover path from 10 um to up to 120 um: mean flashover 1300 +/- 80 V static and 1061 +/- 10 V RF. Trapped at 455 V and 32.2 MHz. — [Sterling et al. 2014](https://ar5iv.arxiv.org/html/1302.3781)
- GTRI: gaps of 4 um near the ion, "expanding to 10 um under the top-level ground to reduce the probability of unintended shorts or RF breakdown". — [Doret et al. 2012, Sec. 2](https://arxiv.org/pdf/1204.4147)
- D2 is made ~10 um thick "to maximise the voltage at which electrical breakdown occurs" between electrodes and ground plane. It is usually the hardest fabrication step and is limited to PECVD SiO2 or SiNx. — [Romaszko et al. 2020, Sec. 3.3](https://arxiv.org/pdf/1908.00267v3)
- Exposed dielectric near ions charges and causes time-dependent stray fields, motivating small gaps or shielded dielectric. — [Sterling et al. 2013 intro](https://www.arxiv.org/pdf/1208.5672); [Romaszko et al. 2020, Sec. 3.1](https://arxiv.org/pdf/1908.00267v3)
- Thin-film PECVD SiO2 breakdown fields of roughly 4.7-12 MV/cm are reported across several studies (search-result snippets of MOS-capacitor papers; values depend on defect density, area and ramp rate; no multi-micron PECVD dataset found). — [Low-temperature PECVD SiO2 on Si and SiC (Univ. at Buffalo record)](https://researchconnect.buffalo.edu/en/publications/low-temperature-pecvd-siosub2sub-on-si-and-sic/) (snippet-level; not read in full)

### Inferences
- [team calc] Field across a 5 um gap at 53 V is ~10 V/um (100 kV/cm), and ~5 V/um across 10 um. Flashover scales roughly as gap^0.5 (Hughes), and measured values are hundreds of V for single-digit-um gaps (Sterling 2013 Fig. 2; exact values not extracted). So 53 V probably has a margin of several times, though the ~30% penalty from the buried Al under the gaps applies to this stack.
- The RF pad is the largest-perimeter high-voltage feature, with the most gap length to grounded fill. Flashover probability scales with the length of exposed gap at high field and with edge defects, so a smaller RF pad (shorter perimeter) slightly reduces risk. This is an inference; no source quantifies flashover vs gap length.
- Bulk breakdown through 10 um D2 is not a concern at 53 V. It would matter only at a crack or pinhole, which links to Section 6.

### Gaps
- Numeric flashover vs gap values from Sterling 2013 Fig. 2 are in the figure, not the text. The figure needs to be read directly.
- No source found for recommended pad-to-fill spacing specifically for RF pads (as opposed to trap-region gaps).

---

## 6. Bonding through thin dielectric onto a buried ground plane: shorting risk and ground-plane cut-outs

### Takeaway
In IC practice, bond pads over thin SiO2 above a continuous metal sheet are the configuration most prone to SiO2 cracking. Slotting or holing the metal beneath the pad improves robustness, and cracks can become leakage paths between nodes. Ion-trap literature (GTRI) bonds to pads in the electrode layer over 10 um PECVD SiO2 over an Al ground plane that appears to be continuous. The team's design already removes the Al under the SNSPD pads (cut-outs) and bonds to M1 Al directly for ground.

### Cited Findings
- Al/SiO2 IC bond pads: "The presence of a full sheet of metal in a pad sub-layer will dominate the top SiO2 cracking performance in the pad." Slots or holes in the metal beneath the pad greatly improve crack robustness (reducing metal-top-minus-one pattern density gives a "dramatic improvement"). In circuit-under-pad designs "a crack can become an electrical leakage" path between nodes. — [Hunter et al., onsemi, "Use of Harsh Wafer Probing to Evaluate Various Bond Pad Structures"](https://www.onsemi.com/site/pdf/UseofHarshWaferProbingtoEvaluateVariousBondPadStructures.pdf)
- Thin pad metal cracks more readily; thicker top metal (> 1 um) reduces cracking. — [Hunter, SWTW 2011 (search-snippet level, not read in full)](https://www.swtest.org/swtw_library/2011proc/PDF/S01_01_Hunter_SWTW2011.pdf)
- Cratering (fracture of Si/SiO2 under pads) often shows up only in cross-section, because a crater can sit under an apparently sound bond. — [Incure Lab, "Bond Pad Damage During Sensor Packaging"](https://incurelab.com/wp/bond-pad-damage-during-sensor-packaging-and-how-to-prevent-it) (vendor blog; low-authority)
- GTRI trap: wire bond pads are in the middle Al layer over 10 um PECVD SiO2. The bottom Al ground plane is patterned only for the loading slot and alignment marks, implying it is continuous under the pads. — [Doret et al. 2012, Sec. 3](https://arxiv.org/pdf/1204.4147)
- Sussex used Au ribbon wire from electrodes to carrier pads. — [Sterling et al. 2014](https://ar5iv.arxiv.org/html/1302.3781)

### Inferences
- The onsemi work concerns ~1 um inter-level SiO2 under thin (< 1-2 um) Al pads. Our stack has 10 um PECVD SiO2 under 6 um plated Au, which spreads the bond load far better on both counts. So the cracking risk is lower than the IC case, but it is not zero; PECVD SiO2 at 10 um is also highly stressed (the TRAVELER bow plan). This is an inference by analogy.
- A pad-to-ground short is an RF short on the RF pad (resonator would not ring up) and a DC short on a DC electrode. That is detectable before cooldown by a DC resistance check, pad to M1 at <= 1 V, as the TRAVELER already does for the SNSPD pads (> 1 Gohm).
- A ground-plane cut-out under a pad removes the shorting risk and most of the pad's capacitance. The pad then couples to the high-resistivity Si, which is lossy at RT in the mid-resistivity range (Romaszko Sec. 3.2). For the RF pad at RT a cut-out would trade a small capacitance reduction (~0.17 pF) for some substrate loss under the pad. For DC and SNSPD pads this loss is irrelevant.
- Electrically, pad size scales the capacitance linearly (Section 1). Mechanically, a larger pad gives more placement tolerance but more area over which a crack can short. The pads are small next to the leads electrically, so pad size can be chosen for bonding yield.

### Gaps
- No ion-trap paper found that explicitly discusses ground-plane cut-outs under bond pads or reports pad-to-ground-plane shorts from bonding through thick PECVD SiO2.
- No bond-force/ultrasonic-power data found for Au wedge/ball bonding onto 6 um Au over 10 um PECVD SiO2. A bond pull/shear plus pad-to-M1 leakage test on the test die (the TRAVELER W3 rehearsal already lists Al pad bondability) would be the direct check.
