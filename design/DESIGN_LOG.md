# Design log: five-wire Ba⁺ trap with integrated NbN SNSPD

> **Claude-authored.** This is Claude's working log of design steps, numbers and choices. It does not replace William's own `notes/decisions.md`.
>
> Every entry gives: the script and its parameters, the key numbers, the decision taken, and the literature it rests on. Citation keys refer to `design/references_design.bib`. Scripts live in `design/sim/` and run with `./run.sh <script>.py`, which uses the `electrode` conda env.

---

## 2026-11-02: Step 0, scope and fixed inputs

**Fixed inputs** (from William's request and "Notes for 6.2540"):

| Item | Value |
|---|---|
| Ion | ¹³⁸Ba⁺; detection on 493 nm fluorescence |
| Cryostat | ~5 K |
| Chip | 1 cm × 1 cm |
| Substrate | high-resistivity Si (William's choice 2026-11-02), with sapphire and fused silica deltas |
| Ground plane | Al |
| Electrodes | plated Au |
| SNSPD | NbN, written with e-beam |
| SNSPD shield | SiO₂ plus a grounded ITO window |

**Zones:**
- A loading zone.
- A readout zone placed directly above the SNSPD.

**Working hypothesis (William):** Todaro et al. report a lower ion height above the detector. We attribute this to the electrode metal missing over the detector (an electrostatic boundary condition), not to any field the SNSPD itself makes. The hypothesis is checked in steps 3–4 below.

**Height policy (William):** the ion height does not have to be uniform from zone to zone. What matters is:
- confinement at both zones,
- transport between them that can actually be done,
- micromotion at readout that can be compensated.

---

## 2026-11-02: Step 1, analytic five-wire at h = 50 µm (`sim/01_analytic_fivewire.py`)

**Model.** Gapless, infinitely long strips in a grounded plane (House 2008, Wesenberg 2008). The RF null of a symmetric five-wire sits at h = √(x₁x₂), where x₁ and x₂ are the inner and outer midlines of the RF-rail gaps.

**Run parameters:**

| Parameter | Value |
|---|---|
| gap g | 5 µm |
| RF drive | 28 MHz |
| RF-only radial frequency (target) | 3 MHz |
| Mathieu q | 0.30 at this drive and radial target |

**Collection vs height.** Fraction of photons landing on a square detector centred below the ion, for a σ dipole with the quantisation axis along z. Script output; figure `out/01_analytic_fivewire/height_tradeoff.png`.

| Detector side | h = 40 µm | h = 50 µm | h = 70 µm |
|---|---|---|---|
| 20 µm | 2.8 % | 1.8 % | 0.95 % |
| 30 µm | 5.7 % | 3.8 % | 2.1 % |
| 40 µm | 9.0 % | 6.3 % | 3.5 % |
| 60 µm | 15.7 % | 11.7 % | 7.1 % |

**Heating.** Heating scales roughly as d⁻⁴ (Brownnutt 2015). Relative to 50 µm:
- 40 µm heats 2.4× faster.
- 70 µm heats 0.26× as fast.

At a fixed detector size, the collection gain from going lower is roughly ∝ h⁻², so heating rises faster than collection does.

**Decision: keep h = 50 µm** (William's choice). Detector size, not height, is the cheaper lever for collection. This is quantified later in the window study (step 4).

**Geometry family at h = 50 µm** (c = centre-DC width, a = RF-rail width, V_RF for 3 MHz radial at 28 MHz). Figure `out/01_analytic_fivewire/geometry_sweep.png`.

| c (µm) | a (µm) | V_RF (V) | depth (meV) |
|---|---|---|---|
| 20 | 182 | 63 | 73 |
| 30 | 120 | 54 | 60 |
| 40 | 84 | 53 | 52 |
| 50 | 58 | 58 | 47 |
| 60 | 39 | 71 | 43 |
| 70 | 24 | 98 | 41 |

**Interpretation:**
- Trap depth at fixed radial frequency falls as the centre electrode widens.
- The centre electrode must be wide enough to hold the SNSPD window (step 4). That pulls toward c ≈ 40–60 µm.
- The minimum RF voltage is near c ≈ 35–40 µm.

**Provisional baseline: c = 40 µm, a = 84 µm, g = 5 µm, V_RF ≈ 53 V at 28 MHz, depth ≈ 52 meV.** To be revisited once the detector and window size is fixed in step 4.

---

## 2026-11-02: Step 2, baseline in gds2itvg (`sim/02_baseline_gds2itvg.py`)

**Geometry.** `trapgeom.BASE`: c = 40, a = 84, g = 5 µm. Outer DC: 16 + 16 segments, 95 µm wide on a 100 µm pitch and 400 µm deep. Rails ±2.5 mm. Ground frame all round.

**Models compared:**
- **gapless "midline"**
- **device stack "profile":** 6 µm Au, SiO₂ with ε_r = 3.9, Al ground 10 µm below.

**Drive:** V_RF = 53 V at 28 MHz.

| | Analytic (step 1) | midline | profile |
|---|---|---|---|
| null height (µm) | 50.0 | 50.05 | 50.09 |
| RF-only radial (MHz) | 3.00 | 2.99 / 2.99 | 2.98 / 2.98 |
| q | 0.30 | 0.303 | 0.301 |
| depth (meV) | 51.9 | 52.0 | 51.9 |

- The null height is flat along the axis from −1500 to +1000 µm. Figure: `out/02_baseline/null_height.png`.
- The analytic sanity check passes. Gaps and the buried ground change the height by less than 0.1 µm, which matches the electrode repo's RESULTS.md (five-wire: 67.2 vs 67.0 µm).

**Decision.** Use the device-stack `profile` model for all later runs, with g = 5 µm, 6 µm Au and ground 10 µm down. These match the planned fab stack (thick PECVD SiO₂ over Al: Romaszko 2020 Fig. 3.1, Stick 2010).

---

## 2026-11-02: Step 3, outer DC segment pitch (`sim/03_segment_pitch.py`)

**Setup:**
- Ion above the middle segment; 9 segments per side.
- All DC electrodes active: segments, centre DC and end caps.
- Midline model, V_RF = 53 V at 28 MHz.

Max |V| from the minimum-norm solution:

| pitch (µm) | 1 MHz axial | shim x / y / z @100 V/m | 10° radial tilt | σ_min/σ_max |
|---|---|---|---|---|
| 50 | 11.5 V | 0.45 / 0.13 / 0.02 V | 12.2 V | 0.087 |
| 75 | 12.4 | 0.51 / 0.15 / 0.02 | 0.36 | 0.076 |
| 100 | 11.3 | 0.45 / 0.16 / 0.02 | 1.7 | 0.075 |
| 150 | 9.3 | 0.32 / 0.17 / 0.02 | 2.8 | 0.071 |
| 200 | 9.0 | 0.38 / 0.19 / 0.02 | 7.0 | 0.059 |

**What the numbers show:**
- A 1 MHz axial frequency costs roughly 9–12 V for the heavy ¹³⁸Ba⁺ at every pitch. Voltage scales as f_ax², so 0.7 MHz needs about 5.5 V.
- The shims are cheap at every pitch.
- Conditioning is similar across the sweep and degrades slowly above 150 µm.
- The 50 µm pitch is the odd one out for tilt. Narrow segments couple weakly to the ion at h = 50 µm, so the solve has to use large, opposing voltages.

**Decision:**
- **Pitch 100 µm (95 µm segments plus a 5 µm gap), i.e. 2h.** Moderate voltages, good tilt control, and the chip needs half the segments (and pads) of a 50 µm pitch.
- Axial target **0.7–1 MHz**, so the DACs need **±10 V or more**.

Literature check on segment pitch versus height is pending; see `research/report.md`.

---

## 2026-11-02: Step 4, laser beam clearance (`sim/11_beam_clearance.py`)

**Model.** A Gaussian beam focused at the ion (h = 50 µm), running parallel to the surface at 45° to the trap axis. The waist is chosen to minimise the beam radius at the chip edge. The quantity reported is the fraction of power striking the surface: ½ erfc(√2 h / w_max).

| λ | full 10 mm chip (axis on centre line) | widest crossing for < 1e-6 | widest crossing for < 1e-4 |
|---|---|---|---|
| 493 nm | 1.7e-2 | 2.0 mm | 3.2 mm |
| 650 nm | 3.2e-2 | 1.5 mm | 2.5 mm |
| 405 nm | 9.6e-3 | 2.4 mm | 4.0 mm |

**Problem.** On a plain 1 cm square chip, 1–3 % of every beam hits the surface. Light scattered near the readout zone goes straight into the SNSPD, so this is not acceptable. William's notes flag the same issue, citing Todaro's 1.8 mm bowtie isthmus.

**Decision: bowtie chip.**
- **Isthmus:** ≤ 1.4 mm wide across the zone region, limited by the 650 nm repump.
- **Envelope:** stays 10 × 10 mm.
- **Flanks:** open at less than 45° to the axis (30° chosen), so 45° beams leave without crossing silicon.
- **Making the outline:** a saw cannot stop mid-wafer, so the notches need a through-wafer DRIE etch (Si: SPTS Pegasus at MIT.nano).
- **Bond pads:** go on the two short ends of the bowtie, away from the beam paths. Wire-bond loops (~150–250 µm high) then never sit under a beam.

Implemented in `gds/make_chip.py` (step 8).

---

## 2026-11-02: Step 5, what the literature says about the readout window (`research/reports/Trap integrated SNSPD design.md`)

**What Todaro et al. actually built** (Todaro thesis Sec. 4.2.1.2, Figs. 4.8–4.9; PRL Fig. 1(b)):
- The SNSPD (22 × 20 µm MoSi) sits in a pocket cut into the **centre DC electrodes**, between the RF rails.
- No metal covers it, and it is recessed 6 µm below the top of the 6 µm plated Au.
- The RF rails **end about 83 µm past the detector**.
- The ion sits about 39 µm up away from the detector and about 29 µm over it (PRL p. 2), "by design".

**Why the height drops.** The thesis (Sec. 6.3, Fig. 6.3) gives two reasons:
- RF end effects (named first);
- the planar model breaking down over the deep recess.

No source attributes the drop to a field from the SNSPD itself. That supports half of William's hypothesis. The "missing metal" half needs a qualifier: in a flat model, a grounded hole inside an RF-grounded electrode does not move the RF null. What matters is depth and RF boundaries, which is tested next.

**Other literature constraints for the window:**
- Todaro Supp. "Trap fabrication" and Hampel 2023 (published version, after Fig. 2): any dielectric over the detector needs a **grounded conducting film or mesh on top**, both against surface charging and to screen the field kick from each click (0.009 quanta/click, PRL p. 4).

---

## 2026-11-02: Step 6, window electrostatics (`sim/05_window_variants.py`, `sim/04_window_validation.py`, `sim/04b_window_3d_fd.py`)

### 05: planar model (gds2itvg)

Readout at x = 0; window 30 µm long; V_RF = 53 V; f_ax = 0.8 MHz.

| Variant | Model | h(0) (µm) | axial Ψ barrier (meV) | RF-only f (MHz) | DC \|V\|max |
|---|---|---|---|---|---|
| V0, no window | profile | 50.03 | 0 | 2.99 / 2.99 | 7.2 |
| V1, 30 µm hole inside 40 µm centre DC | profile | 50.03 | 0 | 2.99 / 2.99 | 0.86 |
| V1w, centre DC cut across its full width | profile | **36.1** | **14.0** | 3.74 / 6.36 | 4.2 |
| V1r, cut also into the RF rails | profile | 46.9 | 0.67 | 3.17 / 3.49 | 1.2 |
| V1w | drawn (opening at 0 V) | 52.1 (= V0) | 0 | 2.72 / 2.72 | 0.6 |

**Observations:**
- A hole **inside** the centre DC electrode leaves the RF null untouched in the planar model.
- A cut across the whole centre electrode lets the RF fringe into the opening, through the "profile" model's dielectric opening. That is a 14 µm height drop and a 14 meV axial barrier, which would break transport.
- The DC solution changes too: the hole makes the centre-DC potential dip along the axis. So the window itself provides axial confinement: 0.73 V on the centre DC alone gives most of a 0.8 MHz well, against ±7 V without the window.

### 04 / 04b: independent finite-difference checks (no planar assumption)

Real stack: 6 µm Au on 10 µm SiO₂ over a grounded plane at −16 µm.

**2-D cross-section, infinitely long window (worst case):**

| Case | RF null height (µm) |
|---|---|
| no window | 47.8 |
| 30 µm pocket inside the centre DC, etched to the floor | 44.0 |
| centre cut, oxide left | 33.6 |
| centre cut, etched | 27.6 |

**3-D, finite window.** Truncated box: ion at 37 µm, so these shifts are a conservative upper bound at 50 µm. Each row is the change in h at the window centre:
- 30 × 30 µm etched to grounded floor: **−1.5 µm**
- 30 × 30 µm oxide floor: −1.4 µm
- **30 × 30 µm ITO-on-D2 floor (ITO tied to centre DC, 6 µm recess): −1.2 µm**
- 30 × 60 µm ITO-on-D2: −2.0 µm

The axial RF gradient on the null line peaks at 1.35e-4 /µm per volt (30 × 30). At 53 V that is a pseudopotential of about 0.3 meV, and it is zero at the window centre by symmetry.

**RF-rail termination (04, part B).** Ending the RF rails 80 µm past the readout point lowers h from 49.4 to 43.9 µm there, and to 41.3 µm at +40 µm. This is the Todaro mechanism, reproduced.

**Conclusion on the hypothesis.** Missing metal *does* lower the ion, but only through the RF boundary condition:
- If the opening is enclosed by RF-ground metal (a pocket inside the centre DC), the effect is small, ~1 µm, coming from the recess depth.
- If the opening spans the full centre electrode, so the RF rails "see" a deep floor, the effect is large: up to 14–20 µm, plus an axial barrier.
- Ending the RF rails near the window adds ~5 µm more.

The SNSPD's own field plays no part in any of this.

### Decisions

1. **Window entirely inside the centre DC electrode: 30 µm radial (5 µm Au rims), 30 µm axial.** Never cut across the centre electrode or into the RF rails.
2. **RF rails run ≥ 1.6 mm past the readout zone.** No termination effect, so the readout height stays ~49 µm instead of following Todaro's deliberate drop.
   - **Why:** the ion is heavy and the solid angle is already set by the window aperture.
   - **Consequence (Todaro trade-off):** h(y) stays nearly uniform between zones, and transport sees no barrier.
3. **Window variant "ITO on D2."**
   - **What it is:** a 30 + 2×5 µm ITO patch deposited on top of D2 before the Au seed. It overlaps the centre-DC Au by 5 µm, so it is electrically the centre electrode.
   - **Why:** the ion sees only conductors (Au walls, ITO floor), with no exposed dielectric (Todaro Supp.; Hampel 2023). The pocket is only 6 µm deep (smallest Δh = −1.2 µm), and the ITO screens click kicks and RF from above. The 10 µm D2 stays over the detector.
   - **Fab benefit:** the Au-masked D2 etch never opens over the detector, because the ITO patch protects it.
   - **Rejected alternative:** etching D2 down to a buried ITO. That leaves 10 µm SiO₂ sidewalls in line of sight, a deeper pocket, and it exposes the cap/ITO to the D2 RIE and BOE.

---

## 2026-11-02: Step 7, detector and window size (`sim/06_detector_size.py`)

**Model.** The window is the optical aperture. It sits 6 µm below the electrode top, and the ion-to-aperture distance is h − 1.2 + 6 µm. The 10 µm SiO₂ below spreads the light footprint by only about 2 µm per side, so the detector is matched to the window.

**Wire assumptions** (research report, Toomey 2018 / Medeiros 2019 film data):
- 100 nm wires on a 200 nm pitch
- Lk ≈ 105 pH/sq
- reset time τ = L / 50 Ω

| Window = detector (axial × radial) | Geometric collection | Wire length | L | τ | Δh (04b) |
|---|---|---|---|---|---|
| 20 × 20 µm | 1.46 % | 2.0 mm | 2.1 µH | 42 ns | – |
| **30 × 30 µm** | **3.25 %** | 4.5 mm | 4.7 µH | 94 ns | −1.2 µm |
| 45 × 30 µm | 4.46 % | 6.8 mm | 7.1 µH | 142 ns | – |
| 60 × 30 µm | 5.92 % | 9.0 mm | 9.4 µH | 189 ns | −2.0 µm |

**Reference point.** Todaro reported 2.0 % geometric collection with a 22 × 20 µm detector at 35 µm (PRL p. 2).

**What limits each direction:**
- **Radial size:** capped at 30 µm by the centre electrode (step 6, decision 1).
- **Axial size:** the free lever. A longer window costs a larger Δh and axial RF gradient, a longer reset, and lower yield, since constrictions scale with wire length.

**Decision.**
- **Chip A (primary):** 30 × 30 µm window and detector, 150 lines.
- **Chip B (wafer variant):** 60 × 30 µm (axial × radial).

Both come from the same `make_chip.py`, using the `--det60` flag.

---

## 2026-11-02: Step 8, full-chip layout on a plain square die (`gds/make_chip.py`, `gds/check_chip.py`)

**Change of plan (William):** no bowtie; use a regular diced 10 × 10 mm chip. This replaces the bowtie decision in step 4.

**Consequence.** Beam clearance was recomputed in `sim/11_beam_clearance.py` (corner section). With the trap on the chip centre line, 1–3 % of each beam would hit the surface. Instead the trap runs **parallel to the top edge, 800 µm from it**, with both zones close to the **top-right corner**. Beams at 45° to the axis then only cut across that corner:

| zone | distance to top / right edge | fraction of beam hitting the surface |
|---|---|---|
| readout | 800 / 800 µm | 5.6e-8 (493 nm), 1.9e-6 (650 nm), 2.4e-9 (405 nm) |
| loading | 800 / 1400 µm | 3.0e-5 (493 nm), 2.4e-4 (650 nm), 4.8e-6 (405 nm) |

**Layout decisions:**

| Item | Choice | Reason |
|---|---|---|
| Readout zone | GDS (4200, 4200) | Corner placement above |
| Loading zone | (3600, 4200), 600 µm = 12 h from readout | 2.3× Todaro's 264 µm (PRL p. 3), still close enough to the corner |
| Segments | 15 + 15 at 100 µm pitch, centres 3100–4500 | Both zones sit on a segment centre with ≥ 3 segments on each side |
| Segment radial depth | 150 µm (was 200–400 in sims) | Room for the lead bus above them |
| RF electrode | "U" closed on the right, 500 µm past the readout zone | RF pad on the right edge at y = 2400, well below where the beams leave (y ≈ 3400) |
| Centre DC | Leaves through the open left end of the U | Single-layer topology |
| Outer DC leads | Each segment continues as a full-width finger to its own track, then runs left | No floating ground islands between risers |
| Pad column | One column on the left edge, x = −4750, 180 µm pitch, 38 pads | Nested L's: higher track turns closer to the column and lands on a higher pad, so nothing crosses |
| SNSPD leads | Layer 22, 4 µm Ti/Au, under the centre-DC electrode and its 40 µm lead | Never under an RF rail (Todaro Supp. "Trap fabrication": route away from RF). Al plane below, centre DC above |
| Ground | Top Au fills everything else; only the main connected region is kept | Strips trapped between parallel leads are left as bare oxide over grounded Al (far from the ion) |
| M1 (Al) | Whole die, 150 µm from the dicing edge | Cut-outs under SNSPD and test pads so a bond cannot short through thin oxide to the Al |
| Wafer variants | A30 (30 × 30 µm detector) and B60 (60 × 30 µm) | Step 7 |

The **test structures** sit in the empty lower half and are probed, not bonded:
- T1: Au comb, 5 µm gaps
- T2: 1 mm² Au/D2/M1 capacitor plus an M1 contact
- T3: NbN 4-wire bar
- T4: spare SNSPD with an ITO patch
- T5: ITO 4-wire bar with Au contacts
- T6: Au continuity loop

These follow Dietl 2025 and Stick 2010.

**Check results.** `check_chip.py` passes on both variants:
- single top cell
- every seed on its own conductor (no shorts)
- every electrode reaches a pad
- minimum Au spacing ≥ 5 µm
- no Au narrower than 4.9 µm
- no text on fab layers
- SNSPD leads within 19 µm of the axis inside the trap
- electrode Au ≥ 20 µm from every D2 opening
- all metal ≥ 90 µm from the dicing edge
- no pad on the ground fill
- no floating Au islands

Preview images: `gds/trap_chip_v1_preview_*.png`.

---

## 2026-11-02: Step 9, NbN optical stack at 493 nm (`sim/09_optical_stack_tmm.py`)

**Model.** Plain transfer matrix (coherent thin layers). The meander is a uniaxial effective medium:
- E along the wires (and along z) sees ε_∥ = fε_NbN + (1−f)ε_SiO₂.
- E across the wires sees 1/ε_⊥ = f/ε_NbN + (1−f)/ε_SiO₂.

These are the Wiener bounds, which are the exact zeroth-order limit of a lamellar grating.

Oblique incidence is solved exactly in the two principal planes (s and p); other azimuths use cos²/sin² interpolation. The cone average weights a 30 µm square detector by cos³θ for an unpolarised isotropic emitter. Two ion distances are used: 50 µm (θ ≤ 23°) and 66 µm (= 50 + 6 Au + 10 D2, θ ≤ 18°).

The script's sanity checks: bulk-Al Fresnel R, the Brewster angle, and zero absorption in lossless films.

**Inputs** (room temperature; no cryogenic n,k found):

| Material | n + ik at 493 nm | Source |
|---|---|---|
| NbN (5 nm sputtered) | 2.11 + 2.00i | Banerjee 2018, Glasgow dataset DOI 10.5525/gla.researchdata.637 |
| NbN (alt) | 2.50 + 2.51i | Medeiros 2019 (arXiv:1812.05559) Table 1, interpolated |
| Al | 0.61 + 5.25i | McPeak 2015 |
| SiO₂ | 1.463 | Malitson 1965 |
| ITO | 1.965 + 0.003i (alt 1.844 + 0.011i; hypothetical k = 0.03) | Moerland 2016; Minenkov 2024 |
| Si | 4.33 + 0.048i | Green 2008 |

Fixed layers: NbN 7 nm with fill 0.5 (100/200 nm), and Al 150 nm over 1 µm thermal SiO₂ on Si. Search limits: cap ≥ 30 nm, spacer ≥ 40 nm, ITO 20–130 nm.

Two tolerance measures are reported, both with spacer, cap and ITO each off by up to ±10 nm:
- **box mean:** the mean absorption, for uniform, independent errors;
- **worst:** the worst corner of that box.

**Etched window** (vacuum / ITO / cap / NbN / spacer / Al), normal incidence, unpolarised:

| Stack | spacer / cap / ITO (nm) | A_NbN | box mean ±10 nm | worst ±10 nm |
|---|---|---|---|---|
| **Design, 1st order** | **66 / 78 / 65** | **0.630** | **0.580** | 0.385 |
| Design, 2nd order | 234 / 78 / 65 | 0.631 | 0.58 | 0.38 |
| No ITO (re-optimised) | 66 / 158 / 0 | 0.502 | 0.490 | 0.397 |
| No mirror, Si below (re-optimised, ITO 0 or 50) | – | 0.28 | – | – |
| Design thicknesses, Al removed | 66 / 78 / 65 | 0.20 | – | – |

- **One thickness at a time ±10 nm:** spacer 0.577 / 0.573, cap 0.589 / 0.585, ITO 0.598 / 0.591.
- **ITO thickness:**
  - ITO 60 nm with an 82 nm cap gives the same 0.631.
  - The plateau is ITO 45–80 nm (A ≥ 0.62 with the cap re-tuned).
  - ITO near 125 nm (half wave) is the worst choice (0.50).
- **Polarisation:** E along the wires 0.87, across 0.40.
- **Cone average:** 0.627 (50 µm) and 0.630 (66 µm). The angle spread costs < 1 %.
- **Mirror gain:** 0.63 / 0.28 = 2.2×. This matches Hampel's RCWA "factor of two" (Hampel 2023, optical-stack paragraph after Fig. 1).

**Sensitivity at the design point:**

| Change | A_NbN |
|---|---|
| Medeiros NbN constants | 0.61 (re-optimised 0.61) |
| NbN 5 / 8 / 10 nm | 0.54 / 0.66 / 0.69 |
| fill 0.4 / 0.6 | 0.54 / 0.73 |
| ITO k = 0.011 / 0.03 | 0.59 (ITO absorbs 3.5 %) / 0.59 (9.5 %) |

**Stray-light wavelengths** at the 493 nm design:
- 614 nm: 0.25 (Medeiros 0.28).
- 650 nm: 0.21 (Medeiros 0.25).

That is ~3× rejection of the repump relative to 493 nm. Without ITO the stack rejects less (614 nm: 0.31, 650 nm: 0.27).

**"ITO on D2" window** (the coordinator's front-runner, step 6 decision 3). The stack is vacuum / ITO / 10 µm D2 / NbN / spacer / Al. The cap merges into D2, so only the spacer and the ITO matter. Absorption is averaged over one fringe of the 10 µm thickness (equal to the incoherent result); the coherent min–max is shown alongside.

| ITO on D2 (nm) | best spacer | A fringe-avg | coherent range, normal | coherent, cone-averaged | A_ITO |
|---|---|---|---|---|---|
| 0 | 66 | 0.40 | 0.32–0.50 | 0.39–0.41 | 0 |
| 50 | 66 | **0.36** | 0.21–0.62 | 0.33–0.38 | 0.5 % |
| 100 | 66 | 0.38 | 0.26–0.57 | – | 1.0 % |
| 125 (half wave) | 66 | **0.40** | 0.32–0.50 | 0.385–0.41 | 1.5 % |

- **Thickness choice.** On top of D2 the ITO (n ≈ 1.96) sits between vacuum and SiO₂, so it can only add reflection. 50–60 nm is close to a quarter wave, which makes it the worst thickness. If this variant is kept, use ~125 nm (λ/2n), where the ITO is optically absent.
- **Fringes.** The ion's cone (θ up to ~20°) washes out most of the coherent fringe of the 10 µm layer. At 50 nm ITO, the normal-incidence range of 0.21–0.62 shrinks to 0.33–0.38.
- **Cost of keeping D2 over the detector.** A = 0.40 vs 0.63, i.e. about 37 % fewer detected photons than the etched window with buried ITO. A dielectric AR layer on top of the ITO could recover part of this (not modelled).
- **Stray light.** At 614 / 650 nm (ITO 125 nm) A = 0.34 / 0.32, so there is almost no rejection.

**Validation against Hampel 2023.** Their stack: NbTiN 10 nm (90/180 nm), 130 nm cap, 50 nm Al, at 395 nm (fabrication and SDE paragraphs). NbTiN is taken as 2.04 + 1.41i from the Banerjee dataset.
- **Cavity phase.** The model's optimum bottom oxide is **179 nm**. Hampel's is 186 nm, "optimized … for theoretically maximum SDE". So the model gets the cavity phase right.
- **Absorption level.** At 186 nm the model gives A = **0.61** with vacuum incidence (0.51 if the fibre is index-matched); the measured SDE is **0.68**.
  - SDE ≤ absorption, so the model is **at least 0.07 low** for the mirror stack.
  - Two possible causes: the effective medium underestimates absorption (the 180 nm pitch is only marginally sub-wavelength), or NIST's NbTiN absorbs more than the Glasgow film.
  - Treat the model as ~10 % pessimistic.
- **No mirror.** For an assumed 130 / NbTiN / 336 nm SiO₂ on Si the model gives 0.40; the measured value is 0.40. Their no-mirror stack is not specified, so this agreement may be coincidental.
- **Trap stack (212 nm).** The model gives 0.32 at 395 nm. Their stack was tuned for 397 nm with vacuum above, and the model may simply be off here. Not resolved.

**Recommendation (etched window with buried ITO).** Stack, bottom to top:
- Al ≥ 100 nm (150 nm)
- SiO₂ spacer 66 ± 10 nm (or 234 nm, second order)
- NbN 7 nm, 100/200 nm wires
- SiO₂ cap 80 ± 10 nm
- ITO 60 ± 10 nm

Predicted A ≈ 0.63, or 0.58 expected with ±10 nm errors. For comparison: 0.50 without ITO, 0.28 without the mirror.

The second-order spacer gives the same absorption with more oxide between Al hillocks and the wire (research report, implication 14). The price is a slightly weaker RF shield (step 10).

If the "ITO on D2" window is chosen instead, use ITO ≈ 125 nm and spacer 66 nm, and expect A ≈ 0.40.

**Limitations:**
- Effective medium, not RCWA/FDTD (Hampel and Todaro used RCWA).
- Room-temperature n,k. The two NbN datasets differ by ~20 %, so we should measure our own film (Medeiros 2019).
- Unpolarised isotropic source instead of the ion's dipole pattern.
- Absorption only, not internal detection efficiency.
- The model under-predicts Hampel's measured SDE by ≥ 0.07.

---

## 2026-11-02: Step 10, RF pickup in the nanowire (`sim/10_rf_pickup_2d.py`)

**Model.** 2-D finite-volume electrostatics in the x–z cross-section through the readout zone. The window is infinitely long along the axis (worst case), and only half the domain is solved, by symmetry.
- **Grid:** non-uniform. 3.5 nm steps across the NbN, 25 nm across the window (so every wire is resolved), 25 µm at the far boundary.
- **Boundary conditions:** RF rails at 1 V. All DC electrodes, the Al and grounded ITO at 0 V.
- **Induced current:** follows Todaro's circuit picture (Todaro Supp. "SNSPD pulses and induced rf currents", Fig. S4, Eq. S1).
  - The wires are held at RF ground; the charge on them gives C_RN per µm, and C_RN = C′_RN × 30 µm.
  - **I_pk = ω V_RF C_RN** at 53 V, 28 MHz. This is an upper bound on the peak current, since it assumes all the current leaves through one end.
- **Convergence:** halving every grid spacing changes E and C_RN by < 0.5 %.

**Geometry (µm).**
- Centre DC |x| ≤ 20 with a 30 µm window; RF rails 25–109; outer DC ≥ 114.
- 6 µm Au on 10 µm D2 (ε 3.9).
- Stack from step 9: ITO 60 nm / cap 80 nm / NbN 7 nm / spacer 234 nm / Al.
- In cases a–d, D2 is etched over the window down to the ITO or cap.

| Case | E_max at NbN plane, \|x\| ≤ 15 (V/m per V) | at 53 V (V/m) | C_RN (fF) | I_pk (µA) | I at Todaro's 8.8 V, 67 MHz (µA) |
|---|---|---|---|---|---|
| a: no Al, ground plane 1 µm below wire | 1.5e4 | 7.8e5 | 0.106 | 0.99 | 0.39 |
| a2: no Al, Si substrate (ε 11.7), back side grounded | 1.8e4 | 9.5e5 | 2.44 | **22.7** | 9.0 |
| b: Al only | 1.1e4 | 5.9e5 | 0.078 | **0.72** | 0.29 |
| c1: Al + grounded buried ITO, \|x\| ≤ 25 | ~0 | ~0 | ~0 (1e-44) | **~0** | ~0 |
| c2: Al + grounded ITO also under RF | ~0 | ~0 | ~0 | ~0 | ~0 |
| d: Al + buried ITO floating (\|x\| ≤ 25) | 1.6e4 | 8.6e5 | 0.71 | **6.6** | 2.6 |
| e: Al + ITO on D2 (D2 not etched) | 9.0e3 | 4.8e5 | 0.070 | **0.66** | 0.26 |

- **Thinner spacer (66 nm instead of 234 nm):** b 0.63 µA, e 0.56 µA, c1 ~0.
- **Floating ITO (d):** rides at 0.52 % of V_RF (0.28 V at 53 V).

**Comparisons:**
- **Calibration against Todaro.**
  - Model: the Todaro-like case a2 (no ground plane, Si below) at Todaro's 8.8 V and 67 MHz gives an upper bound of 9 µA.
  - Measured (Todaro Supp. Fig. S4 fit): I1 = 3.5(2) µA spatially varying, plus 0.9 µA uniform.
  - The geometry differs (22 × 20 µm MoSi on Si, no 10 µm oxide), so this is an order-of-magnitude check. It passes.
- **Switching current.** The estimated NbN Isw is 15–20 µA (research notes, nbn_process Q5, scaled from Najafi 2015).
  - Al alone (b) or ITO on D2 (e) keeps the upper bound at **~4 % of Isw**.
  - No mirror (a2) exceeds Isw.
  - A floating ITO (d) brings the wire up to ~1/3 of Isw. That is **9× worse than no ITO at all**, because the floating sheet couples RF into the wire from 80 nm away. Hampel's floating mirror taught the same lesson (Hampel 2023 Fig. 3(a) vs 3(b)).
- **Grounded buried ITO plus Al (c1, c2).**
  - Together they form a closed sandwich around the wire. The fringe field enters only from the ITO edge and decays as exp(−πx/0.3 µm), so the 2-D pickup is numerically zero.
  - The real floor is set by the SNSPD leads, the ITO openings and the window ends, none of which this model contains.
  - Hampel simulated the same configuration (Fig. 2(d)) but gave no number.
- **ITO on D2 (e) vs etched window with buried grounded ITO (c1).**
  - The ITO on D2 sits 10 µm above the wire. The D2 under the centre-DC rims and in the gaps stays open to the RF fringe.
  - Relative to Al alone it reduces C_RN by only 10 % (0.070 vs 0.078 fF).
  - The field at x = 0 drops from 2.0e3 to 2.2e2 V/m per V, but the window edge still sees ~1e4.
  - So for RF pickup, the ITO-on-D2 patch is roughly equivalent to "Al only". Its value lies in surface-charge and click-kick screening (step 6), not in shielding the wire.

**RF capacitance** (per rail, per mm along the axis; both rails assume 5 mm rails as in step 2):

| | per rail (pF/mm) | both rails, 5 mm (pF) | ωCV at 53 V, 28 MHz (mA) |
|---|---|---|---|
| Al ground plane 10 µm below the Au | 0.360 | 3.6 | 34 |
| No Al (Si substrate, back side grounded) | 0.162 | 1.6 | 15 |
| ITO extended under the rails (c2) | 0.371 (+0.010) | – | – |

- **Where the charge goes.** Extending the ITO under the RF rails barely changes the total capacitance (+3 %). But **0.30 pF/mm (84 %) of the rail's charge then ends on the ITO instead of the Al**. That displacement current must flow sideways through the ITO to its ground contacts (assumed at the centre-DC vias).
- **Loss in that ITO.** At 53 V and 28 MHz, the I²R loss (both rails) is:
  - **0.010 mW per mm of ITO length at 40 Ω/sq;**
  - **0.10 mW/mm at 400 Ω/sq.**
- **Validity check.** The distributed-RC length √(1/ωR_s c) ≈ 360 µm at 400 Ω/sq is much longer than the 84 µm rail width. So the ITO stays near ground and the estimate holds.
- **Small patch.** For the c1 patch (|x| ≤ 25 µm) the loss is 7e-6 mW/mm, which is negligible.
- **Why the loss matters.** Hampel identifies local RF heating as the residual limit once induced currents are gone (Hampel 2023, discussion of Fig. 3(b,c) and Fig. 4(b); published version). ITO under the RF rails therefore adds dissipation and gives no shielding benefit.
- **Not compared** with Dietl 2025 Table 2, whose values are not in our notes.

**Decision / recommendation:**
1. **Ground every conductor near the wire.**
   - The Al mirror is grounded through vias (Hampel fabrication paragraph).
   - Any ITO, buried or on D2, is tied to ground or to the centre DC with a low-inductance via ring.
   - A floating ITO is worse than none.
2. **Al alone already keeps the RF pickup bound at ~0.7 µA (~4 % of the estimated NbN Isw)** in this geometry. That is an order of magnitude below the no-mirror case.
3. **Stop the ITO short of the RF rails (|x| ≤ 25 µm or less).** Extending it under the rails adds dissipation (up to 0.1 mW/mm at 400 Ω/sq) and buys nothing.
4. **The window choice is an optics-versus-surface trade, not an RF one:**

   | Window | A_NbN | 2-D pickup | Surface and pocket |
   |---|---|---|---|
   | Etched, buried grounded ITO | ≈ 0.63 | ≈ 0 | 10 µm SiO₂ sidewalls exposed; pocket 16 µm deep |
   | ITO on D2 | ≈ 0.36 (50 nm ITO) or 0.40 (125 nm) | ≈ 0.66 µA (≈ Al only) | ion sees only conductors; pocket 6 µm deep (step 6) |

   Either way, **keep the SNSPD leads under the centre DC and over the Al** (step 8). In the shielded cases, the leads, not the meander, set the real pickup.

**Limitations:**
- 2-D with an infinitely long window: no leads, no window ends, no ITO openings.
- Ideal conductors.
- The ground plane in case a is a crude stand-in.
- I_pk is an upper bound. How the current splits between the two ends depends on the termination (Todaro Supp. Fig. S4).
- The NbN Isw is an estimate, not a measurement on our film.
- Open item: a 3-D model of the lead exit through the ITO/Al sandwich.

---

## 2026-11-02: Step 9b, recovering absorption for the ITO-on-D2 window (`sim/09b_itoD2_matching.py`)

**Problem from step 9.** The ITO-on-D2 window (step 6, decision 3) leaves 10 µm of SiO₂ above the cap. The cap/ITO then can no longer impedance-match the NbN, and absorption falls from 0.63 (etched window) to about 0.40.

**Fix tested.** A high-index layer goes back directly on the cap, **under** D2. Stack: vacuum / top ITO 125 nm (half wave) / D2 / high-index layer / cap / NbN / spacer / Al. The D2 thickness is averaged over one fringe.

| buried layer | best A (NbN) | spacer / cap / layer (nm) | worst ±10 nm corner |
|---|---|---|---|
| none | 0.40 | 64 / 160 / – | 0.38 |
| **ITO, grounded** | **0.53** | **238 / 80 / 60** | 0.41 |
| PECVD SiN (n ≈ 2.05, [verify]) | 0.55 | 64 / 80 / 60 | 0.40 |

**Decision: two ITO layers.**
- **Buried ITO** (layer 31): 60 nm on an 80 nm cap, where HSQ plus PECVD cap totals 80 nm over the wires.
  - Grounded to M1 through a 10 × 10 µm via (layer 24) through the cap and spacer, 60 µm on the +x side of the detector.
  - Kept within |y| ≤ 18 µm of the axis, so never under the RF rails.
  - It is the optical matching layer, *and* step 10 shows a grounded ITO directly over the wire gives the best RF shielding (≈ 0 induced current in 2-D, vs 0.72 µA for the Al mirror alone). This is Hampel 2023 Fig. 2(d) with a ground connection added.
- **Top ITO** (layer 30): 125 nm on D2, tied to the centre DC (step 6), so the ion sees only conductors.
- **Spacer:** second order, 238 nm. It is optically equal to the first order (64 nm) but puts more oxide between Al hillocks and the wire, and lowers lead capacitance to M1.

**Why grounded and not SiN.** SiN is marginally better optically but cannot be grounded. Step 10 found that a floating ITO *raises* pickup to 6.6 µA.

**Model caveat.** The model reads about 10 % pessimistic against Hampel's measurement (step 9). The final numbers need an RCWA/FDTD check and a witness stack.

---

## 2026-11-02: Step 11, final check on the fabrication GDS (`sim/12_final_chip_check.py`)

**What was simulated.** gds2itvg read layer 50 of `gds/trap_chip_v1.gds` directly, using the device-stack "profile" model. The ITO-on-D2 window enters as a fill of the centre DC; its 6 µm recess is added from step 6 (−1.2 µm).

**Drive and limits:** V_RF = 53 V at 28 MHz, f_ax = 0.8 MHz, DAC limit ±10 V. Radial axes rotated 10° at the zones, so in-plane 45° beams cool both radial modes.

| | loading (−600 µm) | readout (0) |
|---|---|---|
| RF null height | 50.06 µm | 50.02 µm (≈ 48.8 µm including the recess) |
| RF-only radial frequencies, q | 2.99 / 2.99 MHz, 0.30 | 3.00 / 3.00 MHz, 0.30 |
| with DC: axial / radial | 0.80 / 2.90, 2.97 MHz | 0.80 / 2.89, 2.99 MHz |
| radial-axis tilt | 10.7° | 10.3° |
| max \|V\| (14 nearest electrodes) | 8.7 V | 9.2 V |

**Null height along the axis** (RF "U" open at −2200, closed at +500):

| position (µm) | −2100 | −1500 | −1000 to +100 | +300 | +400 | +450 |
|---|---|---|---|---|---|---|
| null height (µm) | 44.9 | 49.8 | 50.0 ± 0.05 | 49.9 | 49.8 | 48.6 |

The readout zone sits 500 µm from the closed end and sees no termination effect. In this design the height is flat between the zones *by choice* (step 6, decision 2). Todaro instead used rail termination on purpose to bring the ion closer to the detector.

**Transport, loading → readout.**
- Method: 61 positions on a 10 µm step, minimum-norm solve over a **fixed** set of all 35 DC electrodes, with no tilt while moving.
- Result: max |V| 7.4 V; at most 1.6 V change per 10 µm step; smooth waveforms (`out/12_final_chip/trap_chip_v1/transport.png`, `waveforms.csv`); axial frequency held at 0.800 MHz; height 50.02–50.07 µm.
- The window's axial pseudopotential bump (≤ 0.3 meV, step 6) is two orders of magnitude below the 0.8 MHz well depth over ±50 µm. Transport needs no special treatment at the window.

An earlier run that let the active set change with position gave jumps of 3.2 V per step and hit the voltage limit, so a fixed set is required.

**Not covered.** The waveforms are quasi-static. Adiabatic timing and the ramp into the tilt set at the readout zone are left for the experiment (see Todaro thesis Ch. 7 on transport).

---

## 2026-11-02: Step 12, floorplan redone as a narrow 10 × 2.5 mm die (`gds/make_chip.py` v2, `make_test_die.py`, `make_wafer.py`)

**Why.** William reviewed the square-die layout from step 8 (trap in the top-right corner):
- only the corner held the trap;
- every lead ran 7–9 mm to one pad column;
- about three quarters of the die was empty ground with scattered test structures.

That layout was lopsided and wasteful. Long leads add capacitance and defect area, and the bonding is awkward. William chose a narrow die (offered options: two traps on the square die; a tidier single corner trap).

**Beam clearance** (`sim/11_beam_clearance.py`, narrow section). Trap on the die centre line, beams at 45° crossing only the width:

| die width | 493 nm | 650 nm | 405 nm |
|---|---|---|---|
| 2.0 mm | 1.0e-6 | 1.8e-5 | 8.2e-8 |
| **2.5 mm (chosen)** | **1.1e-5** | **1.1e-4** | **1.4e-6** |
| 3.0 mm | 5.3e-5 | 3.7e-4 | 9.5e-6 |

Clipping happens at the die edges, about 1.8 mm from the detector. It is worse than the corner placement (2e-6) but acceptable. A 2.0 mm die would be about 10× better if needed.

**New trap die** (`trap_die_v2_A30.gds`, `trap_die_v2_B60.gds`):

| Item | Choice |
|---|---|
| Trap core | Unchanged (c = 40, a = 84, g = 5 µm, 15 + 15 segments at 100 µm pitch, outer DC depth 200 µm), centred on the die |
| Zones | Loading x = −300, readout x = +300 (600 µm = 12 h) |
| RF electrode | U from −2000 to +2000, closed on the right |
| Outer DC leads | Each electrode continues at full width as a "staircase" finger to its own track (no floating islands); the track runs along the die and turns out to its pad |
| Pad rows | 4 rows on the long edges at \|x\| = 2.45–4.7 mm, outside the beam exits; the electrode farthest from its row takes the outer track and the pad nearest the trap |
| End pads | RF on the right short end; centre DC + 2 SNSPD pads on the left short end, SNSPD leads under the centre DC lead |
| Max lead length | ≈ 4.5 mm (was 9 mm) |

**Fixes from the traveler review now in the GDS:**

| Item | Fix |
|---|---|
| A1 | M1 cut-outs at the L1 marks |
| A2 | L22 EBL crosses around the readout zone |
| A3 | L45 PROTECT layer drawn |
| A4 | GND bond spots |
| A6 | Top-ITO radial edges 2 µm inside the centre-DC Au |

**Test die** (`test_die_v2.gds`) carries T1–T7, including the new T7 ITO→Al via chain (A5) and a 60 µm spare SNSPD (T4b).

**Wafer** (`wafer_v2.gds`, A7):
- 10 × 10.8 mm tiles of [A30, B60, A30, TEST], with 200 µm streets.
- 184 dies on 100 mm: 92 A30, 46 B60, 46 TEST.
- So the original 1 cm² footprint now holds two A30 traps, a B60 and a test die.

**Checks.** `check_chip.py` (rewritten to read die size and marks from the layout JSON) passes on both trap dies. The final simulation of the v2 GDS is in step 13.

The square-die files are archived in `gds/archive_v1_square/`.

---

## 2026-11-02: Step 13, final check on the v2 fabrication GDS (`sim/12_final_chip_check.py`)

**What was simulated.** Same method as step 11, rerun on layer 50 of `gds/trap_die_v2_A30.gds` and `trap_die_v2_B60.gds` (via their `*_sim.json`). Same drive: 53 V at 28 MHz, 0.8 MHz axial, ±10 V. The simulator frame is shifted 300 µm from GDS x: readout (GDS x = +300) is sim y = 0, and loading (GDS x = −300) is sim y = −600.

**A30 die:**

| | loading | readout |
|---|---|---|
| RF null height | 50.08 µm | 50.09 µm (48.90 µm including the 6 µm window recess) |
| q | 0.302 | 0.301 |
| with DC: axial / radial | 0.80 / 2.89, 2.97 MHz | 0.80 / 2.88, 2.98 MHz |
| radial-axis tilt | 10.7° | 9.4° |
| max \|V\| | 9.05 V | 9.05 V |
| residual field at the null | < 1e-16 V/µm | < 1e-16 V/µm |

**Null height along the axis** (positions measured from the readout zone):
- The RF U is open at −2300 (GDS −2000) and closed at +1700 (GDS +2000).

| position (µm) | −2200 | −2000 | −1500 | −1000 … +500 | +1000 | +1400 | +1600 |
|---|---|---|---|---|---|---|---|
| null height (µm) | 45.1 | 49.2 | 49.9 | 50.0–50.09 | 49.9 | 49.5 | 48.9 |

Both zones sit on the flat part. Each is ≥ 1.7 mm from either rail end, which is the margin chosen in step 6.

**Transport (A30), loading → readout:**
- 61 steps, fixed set of all DC electrodes.
- max |V| 7.33 V; at most 1.59 V per 10 µm step; no step at the voltage limit.
- Axial frequency 0.800 MHz throughout; height 50.08–50.09 µm.
- Waveforms are smooth and periodic at the 100 µm segment pitch: `out/12_final_chip/trap_die_v2_A30/transport.png`, `waveforms.csv`.

These numbers agree with the v1 run (step 11) to within 0.07 µm and 0.2 V. The narrow-die rerouting of the leads did not change the trap.

**B60 die.**
- Same numbers to every printed digit at both zones and in transport. This is expected: B60 differs only below the Au, in the SNSPD, the ITO size and the via.
- The planar model treats the top ITO as part of the centre DC, so it cannot see the window.
- For the 30 × 60 µm window, the 3-D recess correction from step 6 is −2.0 µm, which puts the readout ion at about 48.1 µm (vs 48.9 µm for A30).

**Status.** Both v2 trap dies pass `check_chip.py` and this simulation, so they are ready for review before tape-out. Still open:
- witness wafers (TRAVELER section E);
- adiabatic transport timing.

---

## 2026-11-02: Step 14, plain trap die without an SNSPD (`gds/make_chip.py --nodet`)

**Request.** William asked for a trap-only die with no SNSPD.

**What `--nodet` changes** relative to A30. Everything else is identical: electrodes, leads, pads, ground fill, marks, M1 bond openings.

| Item | A30 | NODET |
|---|---|---|
| Centre DC at the readout zone | 30 × 30 µm window, filled by top ITO | solid Au |
| Layers 20, 22, 24, 30, 31 | meander, leads, via, two ITOs, EBL crosses, mark overlay squares | empty |
| SNSPD pads SNS/SNG, their D2 openings and M1 cut-outs | present | removed; ground fill closes the gap |
| L45 protect | D2 openings, window, lead branch | M1 bond openings only |
| Signal pads | 38 | 36 |

**Checks.** `check_chip.py` passes. It now skips the SNSPD rules when layer 20 is empty, and instead checks that layers 20–31 are empty and the centre DC is solid at the readout zone. A30 and B60 were rebuilt and still pass.

**Simulation** (`out/12_log_v2_NODET.txt`):
- Identical to A30 to every printed digit: 50.08 / 50.09 µm at loading / readout, 0.80 MHz axial, max |V| 9.05 V, transport max 7.33 V.
- This is expected: the planar model already treated the A30 window as part of the centre DC.
- Physically, the NODET die has **no recess correction**, so the readout ion sits at 50.09 µm, vs ≈ 48.9 µm over the A30 window.

**Uses.**
- A control die: trapping, transport and heating rate without the window, ITO or nanowire. It isolates any effect the detector stack has on the ion.
- A trap-only wafer, which skips traveler steps 4–8b and 10 and needs no EBL (TRAVELER section A).

**Wafer.** NODET is not placed on `wafer_v2.gds`. Adding it, and in what ratio, is William's call.

---

## 2026-11-02: Step 15, R&D run layouts and an EBL dose array (`gds/make_run.py`, `gds/make_test_die.py`)

**Context.** William will fabricate at MIT.nano as an R&D workflow, not as one production wafer. So:
- Each run is a full 100 mm wafer with only a small central block written. Spin coating, PECVD and plating then behave as on a full wafer; small pieces are kept for short loops.
- The MLA150 is maskless, so the die mix and designs can change between runs at no mask cost.

**`make_run.py`** writes `run_<name>.gds`, a map CSV and a PNG:
- Blocks of dies on the `wafer_v2` pitch (10.2 × 2.7 mm), centred on the wafer.
- Presets:

| Run | Dies | Block | EBL (layer 20) |
|---|---|---|---|
| `R1_TRAP` | 6 NODET + 2 TEST | 20.4 × 10.8 mm | none (trap-only process; L20–L31 skipped) |
| `R1_FULL` | 2 A30 + 2 B60 + 2 NODET + 2 TEST | 20.4 × 10.8 mm | 0.030 mm², ~6–18 min at 1 nA [team calc] vs hours for the full wafer |

**T8 dose array** on the test die:
- Seven copies of the 30 × 30 µm trap meander, without ITO, on L20 datatypes 1–7.
- They get 0.80, 0.87, 0.93, 1.00, 1.07, 1.13 and 1.20 × the nominal dose (datatype 0).
- Each has two probe pads. The plan is SEM after step 7, then room-temperature R (test_plan a12), then cold Isw. The result sets the next run's nominal dose.

**Bug found and fixed in the test die.** The four T3 Ti/Au leads ended 5 µm short of their pads (lead end at y0 + 300, pad edge at y0 + 305), so the NbN 4-wire bar could not have been probed. The leads now end inside the pads. A connectivity check shows every NbN structure touches exactly its own leads (T3: 4; T4, T4b, T8 D1–D7: 2 each).

**Checks.**
- All three trap dies were rebuilt and pass `check_chip.py`.
- The test die keeps 9 Au conductors with ≥ 5.0 µm spacing.
- `wafer_v2.gds` and both run layouts were regenerated.

**Docs:**
- TRAVELER section A.3: run plan (run 0 short loops, run 1a trap-only, run 1b full stack) and the facility questions for MIT.nano staff.
- `mask_list.md` section 3 rewritten for runs; per-die areas updated for NODET and the larger test die.
- T8 rows added to `process_checks.md` and `test_plan.md`.

---

## 2026-11-02: Step 16, first run set to trap-only R1_TRAP (`fab/RUNSHEET_R1_TRAP.md`)

**Decision (William):** run 1a, the trap-only process, comes first (`SIMPLIFICATIONS.md` S2; TRAVELER A.3).

**Layout change.** The full test die would put D2 openings over SNSPD-pad areas with no metal under them; on a trap-only run those etches would land on bare D1 oxide. So `make_test_die.py --trap-only` writes `test_die_v2_TRAP.gds` with only T1 (Au comb), T2 (Au/D2/M1 capacitor + M1 pad) and T6 (Au loop).
- 5 Au conductors, ≥ 5.0 µm spacing.
- Its one bond-size D2 opening sits on Al.

`run_R1_TRAP` now uses it, so the run GDS contains only layers 1, 10, 40, 45 and 50 (plus 100/101): **five MLA jobs and no EBL**.

**Run-1a numbers** (gdstk on `run_R1_TRAP.gds`):
- plated Au 1.65 cm²;
- Al kept on 1.69 cm²;
- L40 openings 0.74 mm²;
- L45 patches 0.92 mm².

**Process changes from the full traveler** (D2 directly on Al):
- L40 etch ~10.0 µm;
- gap etch ~9.25 µm to stop 0.75 µm above Al;
- the ground plane sits 10.0 µm below the Au, matching the simulation's `ground_depth`.

**Run sheet.** `fab/RUNSHEET_R1_TRAP.md` covers:
- the die list;
- the five lithography jobs;
- the three short loops that matter (D2 stress, gap-etch rate, W5 plating);
- steps 0–3, 9, 11–19 with sign-off lines;
- the tests that apply (a1–a5, a10);
- the expected trapping numbers from step 14;
- what carries over to run 1b.
