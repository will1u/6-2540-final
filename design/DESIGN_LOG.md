# Design log: five-wire Ba⁺ trap with integrated NbN SNSPD

> **Claude-authored.** This is Claude's working log of design steps, numbers and choices. It does not replace the team's own `notes/decisions.md`.
>
> Every entry gives: the script and its parameters, the key numbers, the decision taken, and the literature it rests on. Citation keys refer to `design/references_design.bib`. Scripts live in `design/sim/` and run with `./run.sh <script>.py`, which uses the `electrode` conda env.

---

## 2026-11-02: Step 0, scope and fixed inputs

**Fixed inputs** (from the team's request and "Notes for 6.2540"):

| Item | Value |
|---|---|
| Ion | ¹³⁸Ba⁺; detection on 493 nm fluorescence |
| Cryostat | ~5 K |
| Chip | 1 cm × 1 cm |
| Substrate | high-resistivity Si (team choice 2026-11-02), with sapphire and fused silica deltas |
| Ground plane | Al |
| Electrodes | plated Au |
| SNSPD | NbN, written with e-beam |
| SNSPD shield | SiO₂ plus a grounded ITO window |

**Zones:**
- A loading zone.
- A readout zone placed directly above the SNSPD.

**Working hypothesis (team):** Todaro et al. report a lower ion height above the detector. We attribute this to the electrode metal missing over the detector (an electrostatic boundary condition), not to any field the SNSPD itself makes. The hypothesis is checked in steps 3–4 below.

**Height policy (team):** the ion height does not have to be uniform from zone to zone. What matters is:
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

**Decision: keep h = 50 µm** (team choice). Detector size, not height, is the cheaper lever for collection. This is quantified later in the window study (step 4).

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

**Problem.** On a plain 1 cm square chip, 1–3 % of every beam hits the surface. Light scattered near the readout zone goes straight into the SNSPD, so this is not acceptable. The team's notes flag the same issue, citing Todaro's 1.8 mm bowtie isthmus.

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

No source attributes the drop to a field from the SNSPD itself. That supports half of the team's hypothesis. The "missing metal" half needs a qualifier: in a flat model, a grounded hole inside an RF-grounded electrode does not move the RF null. What matters is depth and RF boundaries, which is tested next.

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

**Change of plan (team):** no bowtie; use a regular diced 10 × 10 mm chip. This replaces the bowtie decision in step 4.

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

**Why.** The team reviewed the square-die layout from step 8 (trap in the top-right corner):
- only the corner held the trap;
- every lead ran 7–9 mm to one pad column;
- about three quarters of the die was empty ground with scattered test structures.

That layout was lopsided and wasteful. Long leads add capacitance and defect area, and the bonding is awkward. The team chose a narrow die (offered options: two traps on the square die; a tidier single corner trap).

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

**Request.** The team asked for a trap-only die with no SNSPD.

**What `--nodet` changes** relative to A30. Everything else is identical: electrodes, leads, pads, ground fill, marks, M1 bond openings.

| Item | A30 | NODET |
|---|---|---|
| Centre DC at the readout zone | 30 × 30 µm window, filled by top ITO | solid Au |
| Layers 20, 22, 24, 30, 31 | meander, leads, via, two ITOs, EBL crosses, mark overlay squares | empty |
| SNSPD pads SNS/SNG, their D2 openings and M1 cut-outs | present | removed; ground fill closes the gap |
| L45 protect | D2 openings, window, lead branch | M1 bond openings only |
| Signal pads | 38 | 36 |

**Checks.** `check_chip.py` passes. It now skips the SNSPD rules when layer 20 is empty, and instead checks that layers 20–31 are empty and the centre DC is solid at the readout zone. A30 and B60 were rebuilt and still pass.

**Simulation** (`out/archive/12_log_v2_NODET.txt`):
- Identical to A30 to every printed digit: 50.08 / 50.09 µm at loading / readout, 0.80 MHz axial, max |V| 9.05 V, transport max 7.33 V.
- This is expected: the planar model already treated the A30 window as part of the centre DC.
- Physically, the NODET die has **no recess correction**, so the readout ion sits at 50.09 µm, vs ≈ 48.9 µm over the A30 window.

**Uses.**
- A control die: trapping, transport and heating rate without the window, ITO or nanowire. It isolates any effect the detector stack has on the ion.
- A trap-only wafer, which skips traveler steps 4–8b and 10 and needs no EBL (TRAVELER section A).

**Wafer.** NODET is not placed on `wafer_v2.gds`. Adding it, and in what ratio, is the team's call.

---

## 2026-11-02: Step 15, R&D run layouts and an EBL dose array (`gds/make_run.py`, `gds/make_test_die.py`)

**Context.** The team will fabricate at MIT.nano as an R&D workflow, not as one production wafer. So:
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

**Decision (team):** run 1a, the trap-only process, comes first (`SIMPLIFICATIONS.md` S2; TRAVELER A.3).

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

---

## 2026-11-07: Step 17, no ITO: readout window over bare SiO₂ (`gds/make_chip.py` v3; `sim/04b`, `09b`, `10`, `12`)

**Decision (team, 2026-11-07).** Remove both indium tin oxide (ITO) layers: the top ITO on the D2 SiO₂ (L30, tied to the centre DC) and the buried ITO on the cap (L31, grounded through the L24 via). The detector now sits under SiO₂ only. The buried ITO was not a mirror (the Al M1 plane is the mirror); it was an optical matching layer and an RF shield above the wire, and it has to be transparent, so Al cannot replace it.

**Layout.** L24, L30 and L31 are empty on every die (`check_chip.py` checks this). The readout window is a 30 µm opening in the centre-DC Au; its floor, 6 µm below the Au top, is the bare top surface of the 10 µm D2 SiO₂. The L45 protect patch over the window (+2.5 µm) is now essential: nothing else keeps the Au-masked gap etch out of the window SiO₂. Test die: T5 (ITO bar) and T7 (ITO→Al via chain) removed; T4/T4b have no ITO.

**Simulation layout.** `*_sim.json` no longer fills the window with electrode 2; `max_gap` is 20 µm (was 30), so the 30 µm hole fringes over the dielectric instead of being split at its midline. A `_window` entry gives the size; `12_final_chip_check.py` now looks up the 3-D recess correction for that size (it previously applied the A30 value to B60 as well).

**3-D window drop, bare-SiO₂ floor** (`04b_window_3d_fd.py oxide`; box puts the ion at ~37 µm, so Δh is a conservative upper bound at 50 µm):

| Window (radial × axial) | floor | Δh at the window centre | half of the drop at | \|Δh\| < 0.1 µm beyond | peak axial RF gradient (per V) | axial pseudopotential at that point, 53 V |
|---|---|---|---|---|---|---|
| 30 × 30 (A30) | bare SiO₂ | **−1.38 µm** | 25 µm | 45 µm | 1.55e-4 /µm | 0.38 meV |
| 30 × 60 (B60) | bare SiO₂ | **−2.50 µm** | 30 µm | 60 µm | 2.93e-4 /µm | 1.37 meV |
| 30 × 30 (v2) | ITO on SiO₂ | −1.19 µm | 25 µm | 45 µm | 1.35e-4 /µm | 0.29 meV |
| 30 × 60 (v2) | ITO on SiO₂ | −2.04 µm | 30 µm | 60 µm | 2.45e-4 /µm | 0.95 meV |

The 30 × 30 bare-SiO₂ case reproduces the step-6 run exactly (−1.38 µm). Removing the ITO deepens the drop by 0.2 µm (A30) and 0.5 µm (B60). The model treats the SiO₂ as an ideal dielectric with no surface charge; any charging of the exposed SiO₂ comes on top and is not modelled.

**Optics** (`09b_itoD2_matching.py`, no-ITO section; `out/09b_itoD2_matching/summary_noito.json`):

| Stack | NbN absorption at 493 nm | worst ±10 nm corner |
|---|---|---|
| no ITO, 1st-order spacer 66 nm | 0.402 | 0.392 |
| no ITO, 2nd-order spacer 234 nm | 0.402 | 0.391 |
| no ITO, v2 thicknesses (spacer 238, cap 80 nm) | 0.401 | – |
| v2 two-ITO stack (step 9b) | 0.532 | 0.408 |

With no ITO the SiO₂ cap merges optically with the 10 µm D2 SiO₂ (same material), so the cap thickness hardly matters; the spacer and cap are kept at 238 / 80 nm. Absorption drops by about 25 % relative (0.53 → 0.40).

**RF pickup** (`10_rf_pickup_2d.py`, new case f: Al mirror only, 10 µm SiO₂ kept over the window, no ITO; 2-D upper bound at 53 V, 28 MHz):

| Case | C_RN | I_pk |
|---|---|---|
| f, v3 stack | 0.152 fF | **1.42 µA** |
| b, Al only, window SiO₂ etched | 0.078 fF | 0.72 µA |
| e, v2 top ITO on SiO₂ | 0.070 fF | 0.66 µA |
| c1, v2 grounded buried ITO | ~0 | ~0 |

About 7–9 % of the estimated NbN switching current (15–20 µA). Twice case b because the SiO₂ (ε 3.9) left in the window pulls more RF field toward the wire.

**Planar simulation of the v3 dies** (`12_final_chip_check.py`, `out/12_log_v3_*.txt`): see step 19; with the hole now in the model, A30 and B60 no longer match NODET at the readout zone.

---

## 2026-11-07: Step 18, 10 × 10 mm trap die with pads at the die edges (`gds/make_chip.py`, `make_run.py`, `make_wafer.py`)

**Decision (team, 2026-11-07).** Go back to a 1 cm × 1 cm trap die with the trap centred and the bond pads at the die edges. Cost (sim 11, full-chip row, step 4): about **1.7 × 10⁻² of the 493 nm beam** (3.2 × 10⁻² at 650 nm, 9.6 × 10⁻³ at 405 nm) hits the surface, vs 1.1 × 10⁻⁵ on the 2.5 mm die. Light scattered near the readout zone reaches the SNSPD.

**Layout** (trap core, electrodes and lead topology unchanged):

| Item | v3 |
|---|---|
| Die | 10 × 10 mm (`CX = CY = 5000`) |
| Segment and cap pads | four rows on the top/bottom die edges, y = ±4780; TL1–8 at x = −3500 … −2240, TR1–9 at x = +3500 … +2060 (same for BL/BR); leads rise ~4.4 mm to them |
| Beam exits | 45° beams through the zones leave at the top/bottom edges near \|x\| ≈ 4.7 mm and the side edges near \|y\| ≈ 4.7 mm; `check_chip.py` now checks that no pad sits in the corners \|x\|, \|y\| > 4 mm |
| RF, centre DC, SNSPD pads | unchanged, already on the side edges: RF (4700, 0); C (−4650, 0); SNS/SNG (−4750, ±260) |
| GND spots / M1 openings | moved to the side edges: (±4700, ±1500) / (±4700, ±2000) |
| L1 / L40 marks | (±4300, ±4830) |
| Plated Au | 0.92 cm² per trap die (fraction 0.916) |

**Checks.** `check_chip.py` prints ALL CHECKS PASS on A30, B60 and NODET. Test die (`test_die_v3`, still 10 × 2.5 mm): 5 Au conductors, ≥ 5.00 µm spacing, every NbN structure touches exactly its own leads, nothing on L24/L30/L31.

**Runs and wafer.** `make_run.py` and `make_wafer.py` now stack each column at each die's own height. Every column of a run must stack the same heights so the saw's y cuts run straight across (asserted); `R1_TRAP` and `R1_FULL` were reordered so the test dies share a row. Runs are 20.2 × 33.1 mm blocks (8 dies). `wafer_v3.gds`: 56 dies (25 A30, 14 B60, 17 TEST).

**Archive.** v2 outputs and generators are in `gds/archive_v2_narrow/`.

---

## 2026-11-07: Step 19, A30 vs B60 over the bare-SiO₂ window, and DC height tuning (`sim/12_final_chip_check.py`, `sim/13_dc_height_tuning.py`)

### A30 vs B60 (v3 GDS; planar model + 3-D recess correction from step 17)

| | NODET | A30 (30 × 30 µm window) | B60 (60 × 30 µm window) |
|---|---|---|---|
| RF null, readout (planar) | 50.09 µm | 50.09 µm | 50.09 µm |
| 3-D window drop (bare SiO₂) | 0 | −1.38 µm | −2.50 µm |
| Readout height with the drop | 50.09 µm | ≈ 48.7 µm | ≈ 47.6 µm |
| Drop footprint (half / < 0.1 µm) | – | ±25 / ±45 µm | ±30 / ±60 µm |
| Peak axial RF pseudopotential at 53 V | 0 | 0.38 meV | 1.37 meV |
| Readout radial modes, no tilt (planar DC) | 2.89 / 2.97 MHz | 2.76 / 3.09 MHz | 2.55 / 3.27 MHz |
| Readout DC, no tilt | 7.33 V | 6.64 V | 3.38 V |
| Readout DC, 10° tilt | 9.05 V | **13.2 V** | **15.2 V** |
| Transport, max change per 10 µm step | 1.59 V | 1.61 V | **4.47 V** |
| Geometric collection (step 7) | – | 3.25 % | 5.9 % |
| Meander reset time τ (step 7) | – | 94 ns | 189 ns |

- With the ITO fill gone, the planar model sees the window hole in the centre DC. The hole gives the centre DC its own axial curvature; Laplace's equation then forces the two radial curvatures apart, which splits the radial modes. Rotating the radial axes by a fixed 10° costs an x–z curvature proportional to that split, so the tilt set goes over the ±10 V DACs. Without tilt both windows are cheap. (`12_final_chip_check.py` clips at 10 V, so its A30/B60 readout rows show a bounded, slightly off solution: axial 0.796 / 0.753 MHz.)
- The larger B60 window also makes the transport waveforms jump near it (4.47 V per step vs 1.6 V).
- The window drop and the axial bump both grow with the window's axial length: B60 has 1.8× the drop and 3.6× the axial pseudopotential of A30, for 1.8× the collection.

### Can the DC electrodes put the ion back at 50 µm? (`13_dc_height_tuning.py`)

The RF null is set by the RF electrodes; a DC field cannot move it. A vertical DC field pushes the ion off the null like a spring, so the ion then sits in a non-zero RF field and has excess micromotion. The script solves for the DC set (0.8 MHz axial, 14 nearest electrodes, no voltage clip) that gives the needed upward push, checks the real equilibrium by minimising the full energy, and reads the cost off at the shift actually reached:

| | A30, 0° | A30, 10° | B60, 0° | B60, 10° |
|---|---|---|---|---|
| Upward shift needed | 1.38 µm | 1.38 µm | 2.50 µm | 2.50 µm |
| max \|V\| | 6.77 V | 13.43 V | 2.81 V | 15.51 V |
| Vertical DC field | 542 V/m | 537 V/m | 1287 V/m | 1287 V/m |
| RF field amplitude left at the ion | 8.8 kV/m | 8.8 kV/m | 15.5 kV/m | 15.5 kV/m |
| Excess micromotion amplitude (along z) | 200 nm | 200 nm | 350 nm | 350 nm |
| Modulation index β at 493 nm, k along z | 2.5 | 2.5 | 4.5 | 4.5 |

- **Possible in voltage terms:** without tilt the push fits easily in ±10 V. With the 10° tilt the tilt set itself is the problem, not the push.
- **Cost:** the ion is no longer at the RF null. 200–350 nm of vertical micromotion, β ≈ 2.5–4.5 for a beam with k along z. In-plane beams (k_z = 0) barely see vertical micromotion, so it would also be hard to detect and compensate with the current beam geometry.
- **Checks:** zero push reproduces the diagnostic voltages (A30 6.64 / 13.19 V, B60 3.38 / 15.24 V). The micromotion matches (q/2)·Δz (0.15 × 1.38 µm ≈ 207 nm vs 200 nm). The real shift runs ahead of the linear spring estimate (target 2.50 µm gives 3.36 µm on A30) because the pseudopotential softens above the null.
- **Limits:** planar model for the trap fields; the drop itself is from the 3-D box (ion at ~37 µm, an upper bound); no charging of the bare SiO₂.

Outputs: `out/12_final_chip/trap_die_v3_*`, `out/archive/12_log_v3_*.txt`, `out/13_dc_height_tuning/` (`summary.json`, `dc_height.png`), `out/archive/13_log.txt`.

---

## 2026-11-08: Step 20, do the staircase fingers change the DC electrodes? (`sim/14_staircase_check.py`, `gds/make_chip.py --uniform`)

**Question (team).** On the real die every outer DC electrode continues as a full-width finger to its own lead track, so finger tops step by 12 µm (340–424 µm from the axis) and 6 µm tracks run along the axis above them. Did this ever show up as a difference from a plain five-wire? Earlier final-chip checks (steps 11–19) only compared RF quantities, which cannot see it: for the RF solution every DC electrode is ground.

**Layouts compared** (same device-stack model as step 11; unit potentials evaluated at the RF null):

| | Layout | Outer DC electrodes |
|---|---|---|
| FW | `electrode/examples/fivewire` (the electrode repo's reference example) | five identical 120 µm fingers per side, equal-depth rectangles, guard ring |
| U | `trap_die_v3_UNIFORM` (`make_chip.py --uniform`, simulation reference only, not for fab) | our trap, every outer DC electrode a plain 200 µm deep rectangle (y = 114–314 µm), no leads, ground fill around it |
| S | `trap_die_v3_NODET` (the real die) | staircase fingers + lead tracks |

**Sanity and symmetry checks:**

| | FW | U | S |
|---|---|---|---|
| RF null height | 67.19 µm (electrode RESULTS.md: 67.2) | 50.09 µm | 50.09 µm |
| translation mismatch, neighbouring interior segments (max / median, relative to peak) | 4.3e-5 / 3.0e-5 | 6.6e-5 / 5e-12 | **2.4e-2 / 4.9e-3** |
| top/bottom mirror mismatch (relative to peak) | 1.5e-4 | 2.5e-4 | 5.5e-5 |

FW and U both reproduce identical segments to < 1e-4; the FW mirror value is ≈ 5e-6 V per V absolute, matching RESULTS.md. S breaks translation symmetry at the 2 % level. Top/bottom stays symmetric because the two staircases are mirror images.

**S vs U, per top segment, at its own centre** (S/U − 1): unit potential +6.4 % (end segments 3, 17) rising to **+10.1 %** (segment 10, the tallest finger); vertical field ∂φ/∂z +8.5 % to **+13.3 %**; axial curvature ∂²φ/∂y² −0.8 % to −1.8 %. The profile follows the finger heights exactly (tallest at segments 9–11, where the two pad groups meet). The S − U difference is broad: still ≈ 7 % of the peak 300 µm from the segment centre, and skewed toward each electrode's pad side, i.e. it includes the lead track running along the axis. Plot: `out/14_staircase_check/profiles.png`.

**Effect on the zone solves and transport** (`12_final_chip_check.py`, U vs S, same settings as step 19):

| | U | S |
|---|---|---|
| loading / readout DC freqs (MHz) | 0.80 / 2.905, 2.956 · 0.80 / 2.904, 2.954 | 0.80 / 2.887, 2.974 · 0.80 / 2.881, 2.977 |
| max \|V\| at a zone, 10° tilt | 8.40 V | 9.05 V |
| largest single-electrode voltage difference, U vs S | – | 1.14 V (loading), 1.27 V (readout) |
| transport max \|V\| / max step | 7.43 / 1.625 V | 7.33 / 1.589 V |
| largest transport waveform difference | – | 0.20 V |

The NODET rerun reproduces the step-19 summary exactly.

**Reading.** The staircase is visible: segments are up to 10 % stronger at the ion than plain rectangles, by different amounts, so neighbouring segments are no longer interchangeable. All final-chip numbers since step 11 were computed on the real GDS, so they already include it; voltage sets computed from an idealized uniform-segment model would be off by up to ≈ 1.3 V per electrode at the zones and 0.2 V in transport. No layout change made.

**Limits.** Planar device-stack model; far geometry simplified with a tolerance ≤ 1 µm (well below the 12 µm steps); fingers and tracks were not separated.

Outputs: `out/14_staircase_check/` (`summary.json`, `profiles.png`), `out/14_log.txt`, `out/12_final_chip/trap_die_v3_UNIFORM/`, `out/archive/12_log_v3_UNIFORM.txt`, `out/archive/12_log_v3_NODET_rerun.txt`.

---

## 2026-11-08: Step 21, bond pads from the literature (`research/reports/Bond pad sizing for ion traps.md`; `gds/make_chip.py`)

**Question (team).** What does the literature say about bond pad size, does it matter, and what should change on our die?

**Findings** (full report and sources in `research/reports/Bond pad sizing for ion traps.md`; none of its citations are in `references_design.bib` yet):
- **Size is not the constraint.** Our 120 × 200 µm pads at 180 µm pitch are about twice the verified minimums: EPFL CMi standard 100 × 100 µm with 100 µm spacing (60 µm floor); Europractice > 55 µm opening at > 65 µm pitch for 25 µm Au ball bonds. A 25 µm Au ball is ~75 µm across. Published traps: Sandia Phoenix/Peregrine 95 µm pads at 100 µm pitch, RF on 7 bonds (arXiv:2009.02398 Sec. 5.3); Leibrandt 2009 300 × 300 µm Al pads.
- **Electrically, pads are the smallest parasitic** [team calc]: RF pad ~0.17 pF of ≥ 3.4 pF on-chip RF; DC pad 0.11 pF vs 0.32–0.51 pF per lead; SNSPD leads ~3.4 pF each, so pad size does not affect reset or latching. Pad area is ~100× too small to act as an RF filter on the DC lines.
- **What did matter here:** the Au ground fill came to 10.0 µm from every pad (`GAP_FAR`), leaving 40 µm fill fingers between pads and a 10 µm strip outboard of each row; a bond 33 µm off centre would short the pad to ground. The SNSPD openings (120 × 90 µm wells, 10 µm deep, over thin Ti/Au) were tight for a wedge foot (≤ 75 × 125 µm).

**Layout changes (v3, all three dies):**

| Item | Before | After |
|---|---|---|
| Au fill keep-out around bond pads (`PAD_GAP`) | 10 µm (`GAP_FAR`) | **30 µm**; no fill between neighbouring pads |
| Pad rows | y = ±4780 (outer edge 120 µm from the die edge) | **y = ±4720**: moved in 60 µm so a 50 µm fill strip runs outboard of the rows and the fill stays one piece |
| SNSPD D2 openings (L40) | 120 × 90 µm | **150 × 120 µm** |
| SNSPD Ti/Au pads (L22) | 150 × 120 µm | **180 × 150 µm** |
| Al cut-outs under the SNSPD pads (M1) | 260 × 220 µm | **290 × 250 µm** |

Unchanged: pad sizes (120 × 200 µm rows, 200 × 200 µm RF and C) and pitch; Al under the Au pads.

**Checks.** `check_chip.py`: ALL CHECKS PASS on A30, B60 and NODET. Measured on `trap_die_v3_A30.gds`: every Au pad is 30.0 µm from the fill. Test dies, wafer and runs regenerated. `12_final_chip_check.py` rerun on all three: loading/readout heights, DC sets and transport identical to step 19 (max |V| 9.05 → 9.06 V from rounding; the clipped A30 readout radial modes move 2.219 → 2.209 MHz, within the clipped solve's noise). The pad region is ≥ 4.4 mm from the zones.

**Fab doc changes** (`fab/TRAVELER.md`): wedge-bond the SNSPD pads (no ball-bond spark); RF pad on 2–4 wires; probe and bond at opposite ends of each pad; confirm wire-bond-grade (soft) plated Au; new short loop **W7 bond-and-leak** on the test-die T2 stack before R1 (pad-to-M1 leakage before/after bonding; if it leaks, cut the Al out under the DC pads next revision). Mask list and layer map updated.

**Open:** MIT.nano bonder model and wedge/capillary part numbers (to draw against the 10 µm wells); bond diagram against the real carrier; DC-to-RF coupling capacitances (field solve) to decide on filter capacitors.

---

## 2026-11-08: Step 22, on-chip ground vias from the Au fill to M1 (`gds/make_chip.py`, `gds/check_chip.py`)

**Question (team).** A team member drafted an SNSPD process flow in FabuBlox (`SNSPD_integrated_Ion_Trap.pdf`), based on Hampel 2023. Compared with that flow and with Hampel's fabrication paragraph (arXiv:2302.01462 v1), what should change in our GDS and traveler?

**Comparison.**
- Hampel's stack: Si / 150 nm PECVD SiO₂ / 50 nm e-beam Al mirror (lift-off, only under the SNSPD and its leads) / 212 nm SiO₂ / 10 nm NbTiN (SF₆ RIE) / 130 nm PECVD SiO₂ cap (CHF₃-patterned to cover the SNSPD only) / CHF₃ vias to the Al + 20 nm Au / 350 nm Au electrodes and leads by lift-off. The mirror is **grounded through those vias via the trap electrodes**.
- Our flow already covers Hampel's other lessons: cap right after the nanowire etch, leads over Al, spacer set for 493 nm (step 9b). Our lead-first order and blanket cap are deliberate (step-7 EBL marks on L22; the cap stays under D2) and stay as they are.
- **Gap:** our M1 was grounded only by Al wedge bonds at M1-1…4 (traveler A4: "no on-chip link"). A missing or lifted bond leaves the mirror floating, which is the worst case for pickup (Hampel Fig. 3(a); step 10: floating conductor 9× worse than none).
- The FabuBlox flow as drawn puts the evaporated Au electrodes ~240 nm above a blanket Al plane. From the A30 GDS the RF Au area is 0.877 mm², so C_RF–ground ≈ 127 pF on 238 nm SiO₂ vs 2.9 pF on our 10.3 µm [team calc, ε_r 3.9, parallel plate]. Hampel avoided this because the mirror was local and the chips were RF test structures. No change to our D2 follows; reported to the team only.

**Decision (team, 2026-11-08): add on-chip fill-to-M1 vias.**
- Eight 150 × 150 µm L40 openings at (±4700, ±1000) and (±1000, ±2500), each enclosed ≥ 25 µm by the Au ground fill and by M1 (asserted in `make_chip.py`, checked in `check_chip.py`). Same L40 job as the bond openings; the seed and the plated fill land on the Al. No L45: the Au masks them in the gap etch.
- Kept out of `d2_open`, so they create no fill keep-out. M1-1…4 bond openings stay as a backup.

**Checks.** `check_chip.py`: ALL CHECKS PASS on A30, B60 and NODET (new: ≥ 4 vias inside the fill; each enclosed ≥ 25 µm by Au and Al; the L45 rule now applies to bond/probe openings only). Layer diff against the step-21 GDS: only L40 (+0.180 mm² per die) and L100 labels changed; **L50 is identical, so `12_final_chip_check.py` was not rerun**. L40 area: A30/B60 0.333 mm², NODET 0.297 mm²; `run_R1_TRAP` 1.82 mm² and `run_R1_FULL` 2.50 mm², 48 vias in each block. Test dies, wafer and runs regenerated. Test die unchanged.

**Fab doc changes.**
- Traveler step 11: the vias. Step 12: an in-situ Ar pre-clean before the Ti, because the fluorine etch leaves AlF₃ / Al₂O₃ that a sputtered seed will not break through (wire bonds do) [inference]. Step 12 also notes seed sidewall coverage down the ~10.4 µm wall. Step 19: M1 bond now a backup, required if a13 fails. W3: via contact resistance with and without the pre-clean, plus a sidewall cross-section.
- `test_plan.md` a13: GND-n ↔ M1-n < 10 Ω 2-wire; expect ≲ 1 Ω (about one Al square at ~0.3 Ω/sq plus the contacts) [team calc; contact resistance unknown]. `process_checks.md` row 17 changed from "> 100 MΩ, separate nets" to that continuity test. Run sheet, mask list and layer map updated.

**Open:** whether the AJA has a substrate RF etch for the pre-clean; seed continuity on the via wall (W3 cross-section); Au–Al behaviour at the bake-out with 15 nm Ti between them [verify].

---

## 2026-11-08: Step 23, Hampel-style local mirror written up as a traveler variant (`fab/TRAVELER.md` section H; no GDS)

**Question (team).** How big is Hampel's local mirror? Write it into our flow as a variant (team choice, 2026-11-08: a variant section, not a replacement of M1).

**Measured from Hampel 2023 Fig. 1** (arXiv:2302.01462 v1, p. 2; the paper gives no dimensions) [team calc]. Scale check: the 20 × 30 µm SNSPD outline measures 20 × 30.5 µm against the 20 µm bar (13.2 px/µm at 600 dpi).
- Small mirror ≈ 64 µm along the leads × 37–49 µm across. The light-blue mirror shows in the gaps; its edge lies under the Au before the black gaps next to the RF rails.
- Large mirror ≥ 270 µm along the lead channel, ≈ 35–50 µm wide, running ≈ 160 µm past the RF-rail ends (2.70 px/µm against the 100 µm bar).
- Neither goes under the RF rails.
- Fab order from the p. 3 paragraph: nanowire → CHF₃ vias + 20 nm Au → 350 nm Au electrodes and leads by lift-off → **cap last** (blanket PECVD, then CHF₃-patterned to the SNSPD only). This corrects an earlier chat remark that Hampel capped straight after the etch. Cap-last works for them because their later steps are thin lift-offs, with no plating.

**Variant as written (traveler H).**
- Local L10 mirror at |y| ≤ 20 µm (our RF rails start at |y| = 25), from x = 328 along the leads to ≈ −2400. It is grounded through a via under the Au fill at the far end.
- No D2; 350 nm Ti/Au lift-off electrodes (option E2: 6 µm plated on the thin stack).
- Mirror ↔ centre DC ≈ 12 pF [team calc].

**Not done / open:**
- no GDS;
- lead routing under the centre DC with only ≈ 80 nm SiO₂ (slot in the centre DC vs a thicker local SiO₂);
- reruns of 09b (vacuum above the cap), 04b and 12 (`metal_thickness` 0.35, `ground_depth: null`) and 10;
- RF loss over bare HR Si;
- exposed SiO₂ in every 5 µm gap (aspect ratio 0.07).

Baseline unchanged.

**Addendum (2026-11-08): trade-off written down.** Traveler section H.0 now records why the baseline keeps a thick D2. The Al's mirror job depends on the Al-to-NbN distance (238 nm), and its ground-plane job on the Al-to-Au distance (10.3 µm), so the D2 lets one layer do both. C_RF–ground is 2.9 pF (≈ 27 mA at 53 V, 28 MHz) on 10.3 µm, against 127 pF (≈ 1.2 A) on 238 nm [team calc]. A thin stack keeps the mirror only by giving up the plane under the RF rails. Section C points to H.0.

**Correction (2026-11-08).** Traveler H.0 and H.4 had listed "RF over bare HR Si" as a risk of the variant. That is how NIST builds its chips. Todaro trapped on 6 µm plated Au over 134 nm PECVD SiO₂ on intrinsic Si (ρ > 20 kΩ·cm) with no ground plane; Hampel used the same kind of substrate (`research/research_notes/Trap integrated SNSPD design/todaro_slichter.md`). The real condition is the resistivity: ρ > 20 kΩ·cm, against the > 10⁴ Ω·cm in traveler step 0. Todaro credits the 6 µm electrodes with shielding the ion from substrate charge, so option E2 (plated 6 µm on the thin stack) is the Todaro + Hampel combination.


---

## 2026-11-08: Fabrication documentation reorganized for Obsidian

**Request.** Checkpoint existing fab docs, improve readability, split into linked modules, and highlight variants and open decisions. Checkpoint: `50a444d` (five fab files only; other pre-existing work retained).

**Changes.** Added fab overview, variants, open decisions, layout/run/stack/qualification notes, four process stages, separate local-mirror/substrate notes and four test modules. Original traveler/test-plan filenames remain indexes with old section headings. Step numbers, test IDs, uncertainty tags and source pointers retained. Exposure and record tables narrowed.

**Reconciliation.** Working generators specify v3.1: 130/200 nm, rounded turns, 36 × 32 µm A30 / 69 × 32 µm B60 line regions; T9 added. Earlier fab sheets describe 100 nm wires and no T9. Mixed detector revisions in areas, resistance/optics estimates and EBL times are labelled pending reconciliation; current v3.1 figures already present in the mask note are preserved. Simplifications catalog labelled historical v2.

**Corrections against local files.** Trap L1 marks (±4300, ±4830) µm; NODET step 11 includes eight ground vias; R1_TRAP includes W7 bonding; run 1b adds 4–8 while 8a/8b/10 remain retired; local-mirror E1 removes plating, E2 retains it. “Dietl 2025” flagged unresolved as already reported by the bond-pad audit.

**Inputs / sources.** Existing fab docs; working `make_chip.py`, `make_test_die.py`, `snspd_geom.py`; run-map CSVs; steps 17–23; SNSPD-geometry and bond-pad research reports. No new external source claims or design decisions. No generator or simulation was changed; no new physics or fabrication qualification run. Documentation links and content coverage checked separately.

---

## 2026-11-08: Step 24, SNSPD geometry v3.1 from the literature audit (`gds/snspd_geom.py`, `make_chip.py`, `make_test_die.py`, `check_chip.py`; `sim/15`, `sim/10`, `sim/06`)

**Question (team).** Audit the v3 meander against the SNSPD-geometry literature, starting from Suleimen et al., Phys. Rev. Applied 25, 044091 (2026) (doi 10.1103/771x-57wg; abstract only, paywalled) and Clem & Berggren, PRB 84, 174510 (2011). Goal: RF resistant, high collection, easy to fabricate. Report: `research/reports/SNSPD geometry audit.md`; notes in `research/research_notes/SNSPD geometry audit/`.

**Findings that changed the layout** (all [team calc], `sim/15_snspd_geometry.py`):
- **Collection model.** Ba⁺ 493 nm (P₁/₂ → S₁/₂) emission is isotropic: (1/3)(3/8π)sin²θ + (2/3)(3/16π)(1+cos²θ) = 1/4π for any J = ½ state. `sim/06` used the σ pattern. Geometric collection is **2.23 % (A30) / 4.20 % (B60)**, not 3.25 % / 5.9 %. Check against an atomic-physics text.
- **Refraction footprint.** Rays through the bottom of the 6 µm Au window spread 2.57 µm (A30) / 3.91 µm (B60) outward in 10.08 µm of SiO₂. A window-sized meander catches only **80.4 % / 82.0 %** of the photons through the window. Step 7's "spreads only ~2 µm, so a window-sized detector catches all light" was wrong.
- **Absorption vs fill factor** (EMT, oblique incidence, cone-averaged, 7 nm NbN): f 0.5 → 0.40, 0.65 → **0.54**, 0.7 → 0.60. The E-across-wires channel limits it (0.20 at f 0.5). Spacer and cap re-optimisation gains < 0.01. EMT is the zero-pitch limit; RCWA or FDTD needed before sign-off.
- **Turn crowding.** Clem & Berggren Eq. 100 gives R = 0.54 / 0.58 / 0.65 (ξ = 4 / 5 / 7 nm) for the v3 sharp hairpin. The crowding-free turn needs a 2W gap (f ≤ 1/3), which cannot fit in an interleaved meander at useful fill. At a fixed 200 nm pitch, widening to 130 nm lowers R to ~0.50 but raises W × R 1.12× (absolute turn-limited current).
- **Inductance.** 7 nm NbN at 400 Ω/sq, Tc 7.9 K gives 70 pH/sq (dirty BCS), not the 105 pH/sq (5 nm) in `sim/06`.

**RF scan** (`sim/10`, new v3.1 section, case f, 5 nm grid; baseline cases unchanged to 5 digits). C_RN vs the 100 nm / ±15 µm reference (0.151 fF):

| Wire / radial half-extent | C_RN | I_pk (53 V, 28 MHz) |
|---|---|---|
| 100 nm / 15 µm (v3) | 1.00× | 1.41 µA |
| 130 nm / 15 µm | 1.02× | 1.44 µA |
| **130 nm / 16 µm** | **1.19×** | **1.67 µA** |
| 130 nm / 17 µm | 1.40× | 1.97 µA |
| 130 nm / 15 µm, centre DC at 1 % of the RF | 1.11× | 1.56 µA |

Wire width barely matters; lines under the centre-DC rim do. Rule set in the plan: largest radial overhang with C_RN ≤ 1.2×, so **1 µm**. The 2-D model has no axial line extension (those ends are under centre-DC Au) and no leads.

**Decision (Claude, under the `design/` exception; the team should log it in `notes/decisions.md` if it adopts it): v3.1 meander.**
- 130 nm lines on a 200 nm pitch (f 0.65, 70 nm gaps), along the trap axis as before.
- Lines run 3 µm (A30) / 4.5 µm (B60) past each axial window edge (36 / 69 µm long), and 1 µm past each radial edge (160 lines over 32 µm).
- Turns: solid 0.5 µm end blocks, slot ends closed by a semicircle (diameter = gap), all outside the light footprint under the Au.
- The outer lines run past the end blocks and flare smoothly into the 40 × 3 µm tabs (edge y = w + (H − w)(s/L)², 6 µm; no re-entrant corner), on the side towards the axis. NbN max \|y\| = 15.96 µm.
- Predicted geometric × landing × absorption: **A30 0.71 % → 1.15 %, B60 1.37 % → 2.2 %** (internal efficiency 1). L = 3.1 / 5.9 µH, τ = 62 / 119 ns.
- Shared code in `gds/snspd_geom.py` (`meander()`, `straight()`), used by both generators; `turn="sharp"` reproduces v3 for the control.

**Test die.** T4 / T4b / T8 use the v3.1 meander. New **T9 geometry array** (8 slots, compared as ratios between neighbours): 100/200 sharp (v3 control), 100/200 rounded, 130/200 rounded, 140/200 rounded, 300/600 rounded (Suleimen width comparison), a short 130/200 meander (18 × 17 µm, length series), and straight Ic references at 100 / 130 / 140 / 300 nm. Test plan: a14 (RT resistance and SEM), b10 (Isw ratios, 493 nm plateau vs width at 2 K and 5 K).

**Checks.** `check_chip.py` has new NbN rules: \|y\| ≤ 17 µm, all NbN under centre-DC Au or the window, gaps ≥ 60 nm (morphological closing), no turn or tab inside the footprint (window + refraction spread). It fails the v3 sharp layout and passes v3.1: **ALL CHECKS PASS** on A30, B60, NODET. Test die: 5 Au conductors, ≥ 5.00 µm spacing, every NbN structure touches exactly its own leads. L50 is unchanged, so `sim/12` was not rerun. L20 areas 1 928 / 2 614 / 20 270 µm² (A30 / B60 / TEST); `run_R1_FULL` EBL area 0.050 mm². R1_TRAP unaffected (no L20).

**Open (not geometry):**
- Isw at 5 K may be only ≈ 8–9 µA (Sedykh 2025 scaled), so the 1.67 µA bound is ≈ 20 % of it (≈ 10 % with symmetric drain).
- Filter capacitor on the centre DC (each lead couples ≈ 11 µA per volt of RF on it).
- Al RF potential under the 4.7 mm of lead (≈ 2.7 pF per lead).
- Measured NbN thickness used in every model.
- Whether 130 nm, 7 nm NbN keeps a saturated 493 nm plateau at 5 K (T9 b10).
- Suleimen 2026 full text.

---

## 2026-11-08: Step 25, v4 local-mirror dies, slot leads, A30 only (`gds/make_chip.py` v4, `check_chip.py`, `make_run.py`, `make_wafer.py`; `sim/04b`, `12`, `13`)

**Decisions (team, 2026-11-08; logged in `notes/decisions.md`).**
- Architecture: local mirror, no 10 µm D2 (LOCAL_MIRROR.md, adopted).
- Lead routing: SNSPD leads in the electrode Au, in a slot along the centre DC, as Hampel 2023. Checked against the paper: arXiv:2302.01462 v1 fabrication paragraph, leads "patterned, together with the SNSPD leads, in a lift-off process" in 350 nm Au, capped only over the SNSPD; SPIE Proc. 13025 (tf.nist.gov/general/pdf/3290.pdf) Fig. 1 shows the leads as thin Au lines between the RF electrodes, over the mirror. Hampel trapped no ions in that paper.
- R1_TRAP on the same no-Al stack.
- Detector allocation: A30 only, B60 dropped.
- Still open: electrode Au, E1 (0.35 µm lift-off) vs E2 (6 µm plated).

**Layout (v4).** v3 files moved to `gds/archive_v3_baseline/`.
- Slot \|y\| < 12.5 from the left end of the centre DC to x = 235 (50 µm before the window): DC half / gap / lead / gap / lead / gap / DC half = 7.5 / 5 / 5 / 5 / 5 / 5 / 7.5 µm. Right of x = 235 the centre DC is solid, so electrode 2 is a U around the slot. Its lead runs along the top half and turns up to the C pad (−4650, 450) only at x = −3600, outboard of the left pad-row tracks (|y| ≥ 334 out to x = −3500). A first draft turned at x = −2300 and would have crossed them.
- Au leads 5 µm at y = ±5, x = 230 → −4400, then to Au pads (−4750, ±100), 200 × 150 µm. No layer-22 leads in the trap.
- Contacts: layer 22 covers the −x half of each NbN tab (under the solid centre DC), steps into the slot and ends in a 27 × 7 µm pad at x = 203 … 230; an 18 × 3 µm layer-40 cap opening sits ≥ 1 µm inside the Au lead and the pad.
- Local mirror (layer 10): \|y\| ≤ 20, x = −2550 … +328, plus a branch to y = 230 at x = −2550 … −2350 under the Au fill; 100 µm ground via at (−2450, 130), enclosed ≥ 25 µm by fill and Al. 0.157 mm². No layer 45; no M1 pads or fill-to-M1 vias.
- NODET: layers 1 and 50 only (solid centre DC, no Al). Pad map: C pad moved to (−4650, 450) on every variant.
- Simulation files: `_sim.json` = E2 (6 µm), `_E1_sim.json` = 0.35 µm; `ground_depth: null`; grounds 97/98 = the leads (~0 V), 96 = the window floor. `_simfloor.gds` (A30, sim only) adds a ground conductor 1 µm inside the window, because the floor is the cap 0.32 µm above the grounded mirror; without it gds2itvg treats the 30 µm hole as floating dielectric.

**Checks.** `check_chip.py` rewritten for v4 (leads inside the slot, no buried Ti/Au in the trap, contacts inside lead and pad, mirror never under the RF rails and ≥ 3 µm around all detector NbN, mirror via enclosure, layers 24/30/31/45 empty; NbN rules of step 24 with the v4 footprint = window + 0.02 µm, since only the 80 nm cap lies between the floor and the NbN). **ALL CHECKS PASS** on A30 and NODET. Layer areas per A30 die: L10 0.157, L20 0.0019, L22 0.0024, L40 0.0115 mm². Runs: `run_R1_TRAP` 6 NODET + 2 TEST_TRAP; `run_R1_FULL` 4 A30 + 2 NODET + 2 TEST (EBL area 0.049 mm²); `wafer_v4` 39 A30 + 17 TEST. **The test dies are still v3** (die-wide Al, D2 openings, L45).

**3-D window recess (`04b … mirror_t6`, `mirror_t1`).** Grounded floor at the bottom of the Au pocket, ~1.3 µm SiO₂ then Si (ε 11.7) below, box bottom 40 µm under the Au:
- E2 (6 µm pocket): Δh = **−1.19 µm** (v3 bare SiO₂ floor: −1.38; v2 `ito6` gave the same −1.19).
- E1: the 0.35 µm pocket is below the 1 µm grid; a 1 µm pocket gives **−0.37 µm**, an upper bound.

**Final-chip simulation (`12`, 53 V / 28 MHz, 0.8 MHz axial, 10° tilt in the zones).**

| Die | Null height load / read (planar) | Read incl. recess | Loading \|V\|max | Readout \|V\|max | Transport max \|V\| / max step |
|---|---|---|---|---|---|
| v3 A30 (step 19) | 50.08 / 50.09 | 48.7 | 9.06 | 10.00, clipped (13.2 needed) | 7.33 / 1.61 V |
| **v4 A30 E2** | 49.97 / 49.98 | **48.79** | 8.14 | **6.09** | 7.26 / **7.96 V** |
| **v4 A30 E1** | 49.96 / 49.96 | ≥ 49.59 | 8.13 | 6.08 | 7.26 / 7.96 V |
| v4 NODET | 49.97 / 49.98 | – | 9.10 | 9.10 | 7.34 / 1.59 V |
| **v4 A30 E2, centre DC at 0 V** | 49.97 / 49.98 | 48.79 | 10.00, clipped (0.76 MHz) | 10.00, clipped (0.76 MHz) | 6.41 / **1.67 V** |

- RF-only radial 3.00 MHz, q 0.30 on every v4 die. Without a ground plane the null sits ~0.1 µm lower than v3.
- **The readout tilt problem of step 19 is gone on v4:** with the floor grounded through the mirror, the 10° tilt at the A30 readout needs 6.1 V (v3: 13.2 V). Readout DC radial modes 2.80 / 3.08 MHz.
- **New: rough transport on A30.** The 7.96 V step sits between ITVG y = −200 and 0 (GDS x = 100 … 300), around the slot end (y = −65) and the window. Diagnosis (scratch script, gds2itvg unit potentials on the RF null): the constraint matrix is well conditioned (≈ 14–20, same as NODET), but electrode 2's axial curvature d²φ₂/dy² swings from +4.2 × 10⁻⁵ to −3.5 × 10⁻⁵ µm⁻² there (NODET: ~10⁻¹⁰), comparable to the whole 0.8 MHz axial curvature per volt (≈ 3.6 × 10⁻⁵ V/µm²). Any voltage on the centre DC makes axial bumps, and the minimum-norm single-position solve swings to cancel them. The slot also lowers φ₂ at the ion from 0.27 to 0.15.
- **Fix in the solve, not the layout:** hold the centre DC at 0 V during transport (`12_final_chip_check.py --centre-dc-zero`): max step 1.67 V, max \|V\| 6.41 V. With electrode 2 at 0 V, the zones cannot reach 0.8 MHz with the 10° tilt inside ±10 V, so the tilt set (which uses the centre DC) is ramped in once the ion sits in a zone, as sim 12 already assumes. E1 and E2 give the same voltages to 0.01 V; the V2 = 0 transport was run on E2 only.

**DC height tuning (`13`, out/13_dc_height_tuning_v4/).** Undoing the window drop by pushing the ion off the RF null: E2 (−1.19 µm) needs 1.4 V without tilt / 6.0 V with 10°, leaving 173 nm micromotion (β ≈ 2.2 at 493 nm with k along it); E1 (≤ −0.37 µm) needs 1.6 / 6.0 V and leaves ≤ 55 nm (β ≤ 0.7). v3 A30 needed 6.8 V for 200 nm.

**Mirror ground path [team calc].** The strip is 2.75 mm from the detector to the via, 40 µm wide: ≈ 69 squares of 150 nm Al-1%Cu at 0.20–0.27 Ω/sq (ρ 3–4 µΩ·cm), so ≈ 14–18 Ω. The < 10 Ω acceptance carried over from H.2 / a13 cannot pass as drawn; whether ~15 Ω matters for RF pickup needs sim 10.

**Not rerun / open:** 09b (vacuum above the cap; sets the cap thickness), 10 (RF pickup with the slot leads 17.5 µm from the RF rail edge and the local mirror), 15 (collection at the new heights). gds2itvg's single-stack gap model omits the local Al under the slot gaps and the window (`ground_depth: null` everywhere). Traveler, R1_TRAP sheet, mask list, stack and qualification docs still describe v3 and carry a banner; their rewrite waits on E1 vs E2. Test dies need a v4 rework.

---

## 2026-11-08: Step 26, v4 optics and RF pickup; B60 window on the v4 stack (`sim/09c_localmirror_optics.py`, `sim/10b_rf_pickup_v4.py`, `sim/04b`)

**Optics (`09c`, new; 09b's transfer matrix, EMT, f 0.65, normal incidence, unpolarised).** Vacuum now sits on the cap, so the cap is a matching layer again.

| Stack | Spacer / cap (nm) | A_NbN | ±10 nm box mean | worst corner |
|---|---|---|---|---|
| v3.1 baseline, 10 µm D2 above (fringe avg) | 238 / 80 | 0.540 | 0.534 | 0.517 |
| **v4 as drawn** | 238 / 80 | **0.440** | 0.440 | 0.419 |
| **v4, cap re-optimised** | 238 / **159** | **0.662** | 0.645 | 0.596 |
| v4 best, 1st-order spacer | 64 / 164 | 0.665 | 0.648 | 0.605 |
| v4 best, 2nd-order spacer | 232 / 166 | 0.665 | 0.648 | 0.609 |

- **The 80 nm cap is now a bad thickness** (0.44, below the v3.1 0.54). With the 238 nm spacer kept, a ~160 nm cap gives 0.66, +22 % over v3.1 and +50 % over the v4 drawing. Re-optimising the spacer gains nothing (0.665). A cap of 146–172 nm stays within 0.02 of the best; the response repeats every λ/2n = 168 nm (243 nm gives 0.44 again, 327 nm 0.66).
- **Decision (Claude, under the `design/` exception; reported to the team): total SiO₂ (HSQ + PECVD cap) over the wires 160 ± 10 nm** for v4, spacer unchanged. Side effects: twice the dielectric between the NbN/Ti-Au contacts and the centre-DC Au (better pinhole margin); the L40 contact etch becomes ~160 nm and the mirror via ~0.40 µm. The 2-D pickup and gds2itvg runs used 80 nm; at 160 nm the wires sit 80 nm further from the Au, a small change [inference].
- Hampel check (09): the model reads ~10 % low against Hampel's measured SDE.

**RF pickup (`10b`, new; 10's solver, 2-D, 53 V / 28 MHz, HR Si insulating at 4–6 K).**

| | E2 (6 µm Au) | E1 (0.35 µm Au) | v3.1 baseline |
|---|---|---|---|
| Nanowire C_RN (30 µm) / I_pk | 0.103 fF / **0.96 µA** | 0.206 fF / **1.92 µA** | 0.180 fF / 1.67 µA |
| Wires ↔ mirror | 137 fF | 137 fF | – |
| RF rail → mirror strip | 0.151 fF/µm | 0.154 fF/µm | – |
| Mirror detector end, ~15 Ω path (R_s 0.20–0.27) | 26–35 mV → +0.62–0.84 µA | 26–36 mV → +0.64–0.86 µA | – |
| RF rail → each slot lead | 2.13 aF/µm → **20 µA/mm, 46 µA over 2.3 mm** | 1.36 aF/µm → 13 µA/mm, 29 µA | buried, not modelled |

- **Nanowire:** E2 is better than v3.1 (the 6 µm walls and the grounded mirror 0.32 µm below); E1 is 1.15× v3.1.
- **Mirror ground path matters:** the ~15 Ω strip lets the mirror's detector end swing ~30 mV, adding up to ~0.6–0.9 µA (comparable to the direct pickup on E2). Lowering it needs a lower-resistance strip (thicker Al: 300 nm halves it), a shorter path, or less rail coupling (narrower mirror away from the detector) [inference].
- **Slot leads are a new, large pickup path.** Each lead collects ~46 µA (E2) of RF displacement current over its 2.3 mm between the rails, against an NbN switching current estimated at 8–20 µA. The two leads see the same coupling (common mode), so with identical terminations no current crosses the nanowire; any termination asymmetry sends a fraction through it [inference; Todaro Supp. Fig. S4 model]. This ties the routing to the open **RF grounding / filters** decision: a low-impedance-at-28 MHz capacitor to ground at both lead pads (e.g. 1 nF ≈ 6 Ω), a symmetric termination, or a differential readout [inference]. In v3 the leads were buried under the centre DC over the Al plane and were not modelled (3-D lead pickup was open).
- Limits: 2-D (no window ends, slot end or lead tips); ideal conductors; ω V C is an upper bound.

**B60 on the v4 stack (`04b mirror_t6` / `mirror_t1`, 30 × 60 case added).**

| Window | v3 bare-SiO₂ floor | v4 E2 (6 µm) | v4 E1 (≤, 1 µm pocket) |
|---|---|---|---|
| A30 (30 × 30) | −1.38 µm | −1.19 µm | −0.37 µm |
| B60 (30 × 60) | −2.50 µm | −2.04 µm | −0.55 µm |

The A30 numbers are unchanged from step 25. The B60 v4 die is not drawn (it needs the slot end moved left of its longer tabs).

---

## 2026-11-08: Step 27, B60 kept on v4 (`gds/make_chip.py --det60`, `make_run.py`, `make_wafer.py`; `sim/12`, `13`)

**Decision (team, 2026-11-08; `notes/decisions.md`):** keep B60, reversing the A30-only call after the step-26 numbers.

**Layout.** `make_chip.py --det60` writes `trap_die_v4_B60`: 60 × 30 µm window, 69 µm lines (OVH_X 4.5). The slot end now follows the tabs: X_TAB = X_READ − DET_WX/2 − 27 (asserted against `snspd_geom`), slot end = X_TAB − 20 (A30 235, B60 218.5), contacts 186.5 … 213.5 on B60; mirror to X_READ + DET_WX/2 + 10 (A30 328, B60 344.5). A30 is unchanged (layer areas identical). **ALL CHECKS PASS** on A30, B60, NODET. Runs back to `run_R1_FULL` 2 A30 + 2 B60 + 2 NODET + 2 TEST (EBL 0.050 mm²); `wafer_v4` tile A30/B60/A30/TEST (25 A30, 14 B60, 17 TEST).

**Simulation (`12`, `13`; window drop from step 26).**

| Die | Read incl. recess | Loading \|V\|max | Readout \|V\|max (10°) | Transport max step: centre DC free / at 0 V |
|---|---|---|---|---|
| v4 A30 E2 | 48.79 µm | 8.14 V | 6.09 V | 7.96 / 1.67 V |
| **v4 B60 E2** | **47.94 µm** | 8.14 V | **2.25 V** | 8.01 / **1.67 V** |
| v4 B60 E1 | ≥ 49.41 µm | 8.13 V | 2.24 V | 8.01 V / – |
| v3 B60 (step 19) | 47.6 µm | 9.06 V | 10.00 V clipped (15.2 needed) | up to 4.5 V |

- B60 readout radial modes 2.90 / 2.99 MHz. The 10° tilt now fits easily on both detector dies.
- Same transport behaviour as A30: hold the centre DC at 0 V while moving.
- DC height tuning (`13`, `out/13_dc_height_tuning_v4/`): undoing the B60 drop needs 0.7 V (no tilt) / 1.9 V (10°) on E2 and leaves 291 nm micromotion (β ≈ 3.7 at 493 nm, k along it); on E1, ≤ 0.55 µm needs 0.7 / 2.1 V and leaves ≤ 81 nm (β ≤ 1.0).

---

## 2026-11-08: Step 28, zones 480 µm apart, 120 µm segment pitch, mirror via moved (`gds/make_chip.py`; `sim/12`, `13`, `10b`)

**Decision (team, 2026-11-08; `notes/decisions.md`):** loading and readout zones 480 µm apart, to match the team's laser setup. Zones at x = −240 / +240 (were ±300).

**Layout calls (Claude, `design/` exception).**
- Outer DC segments at **120 µm pitch** (115 µm + 5 µm gap), still 15 per side, centres −840 … +840, so both zones sit on segment centres (four pitches apart). Step 3 found 75–150 µm pitches equivalent (1 MHz axial 9–12 V, tilt ≤ 2.8 V). A 96 µm pitch would need 16 segments and renumbered electrodes; 100 µm would put a zone over a gap. Electrode numbers and pad rows are unchanged.
- Detector, slot, contacts and mirror move with X_READ (A30 slot end 175, B60 158.5; mirror right end 268 / 284.5).
- **Mirror via moved from (−2450, 130) to (−2140, 130)**, just past the RF open end; the strip now starts at x = −2240 (2.51 mm on A30, was 2.88).
- `check_chip.py`: **ALL CHECKS PASS** on A30, B60, NODET. Runs and wafer regenerated (same die mix). The 600 µm logs are kept as `sim/out/*_600um.txt`.

**Simulation (`12`, 53 V / 28 MHz, 0.8 MHz axial, 10° tilt in the zones).**

| Die | Loading \|V\|max | Readout \|V\|max | Transport max \|V\| / max step: centre DC free | … centre DC at 0 V |
|---|---|---|---|---|
| A30 E2 (600 µm, step 25) | 8.14 | 6.09 | 7.26 / 7.96 V | 6.41 / 1.67 V |
| **A30 E2** | **7.45** | **6.28** | 7.27 / 7.59 V | **6.64 / 1.71 V** |
| A30 E1 | 7.45 | 6.27 | 7.27 / 7.59 V | – |
| **B60 E2** | 7.46 | **2.24** | 7.13 / 8.00 V | **6.64 / 1.71 V** |
| B60 E1 | 7.45 | 2.24 | 7.13 / 8.00 V | – |
| NODET | 7.92 | 7.87 | 7.20 / 1.66 V | – |

- Null heights 49.96–49.98 µm; RF-only radial 3.00 MHz, q 0.30; 49 transport steps of 10 µm.
- With the centre DC held at 0 V the zone solves still clip at ±10 V (0.795 MHz axial), so the tilt is ramped in at the zone as before.
- `13` (window drops from step 26 unchanged): undoing the drop needs A30 1.3 / 6.1 V and B60 0.7 / 1.9 V (no tilt / 10°) on E2, with the same micromotion as step 27 (A30 173 nm, B60 291 nm on E2; ≤ 55 / 81 nm on E1).

**Mirror ground path (`10b`, L = 2240 µm between the rails, 140 µm to the via).**

| Al | Detector-end swing | Extra wire current (E2) |
|---|---|---|
| 150 nm, via at −2450 (step 26) | 26–35 mV | 0.62–0.84 µA |
| 150 nm, via at −2140 | 20–27 mV | 0.48–0.65 µA |
| **450 nm, via at −2140** (proposed) | **6.7–8.8 mV** | **0.16–0.21 µA** |

- The Al thickness is a traveler parameter, not GDS; 450 nm is a proposal for the v4 traveler rewrite (step-L10 sputter time; watch hillocks after the spacer deposition, ≤ 300 °C).
- Slot-lead pickup: 44.5 µA per lead over 2.24 mm (E2), 28.3 µA (E1). Unchanged physics; the RF grounding decision stays open.

**Addendum (team, 2026-11-08): Al 450 nm adopted** (`notes/decisions.md`). The local mirror is 450 nm Al-1%Cu: detector-end swing 6.7–8.8 mV, extra wire current 0.16–0.21 µA on E2. GDS unchanged. To carry into the v4 traveler: L10 sputter time, strip acceptance ≈ 5 Ω, a mirror probe opening, and a hillock check after the spacer deposition.

---

## 2026-11-08: v4 SNSPD overhang audit (read-only calculations; no design decision)

**Inputs and method.** Actual `trap_die_v4_A30.gds` / `trap_die_v4_B60.gds`; existing gds2itvg nulls and window-drop estimates in `sim/out/13_dc_height_tuning_v4/summary.json`; optical functions from `sim/15_snspd_geometry.py`, evaluated inline through `sim/run.sh` without executing that script's v3 study. Stack: 493 nm, 7 nm NbN, fill 0.65, 238 nm SiO₂ spacer, 450 nm Al mirror, 80 / 160 nm SiO₂ cap, E2 6 µm / E1 0.35 µm Au. E1 heights are bracketed between the planar null and the existing 1 µm-pocket drop; they are not a new simulation of a 0.35 µm pocket. All numbers below are [team calc], not measured detector performance.

- **GDS:** both meanders are connected; 160 lines, 130 nm / 200 nm pitch, actual radial span 31.93 µm. Straight lengths 36 / 69 µm; windows 30 × 30 / 60 × 30 µm. Fill inside each window is 0.65. All local detector NbN outside the window lies under Au (alignment marks excluded).
- **Collection and absorption:** centred isotropic collection through the window floor is A30 E2 2.221%, E1 2.601–2.636%; B60 E2 4.158%, E1 4.674–4.760%. The finite Au pocket is included in the source-to-floor distance. Using the existing angular effective-medium approximation, fractions of all emitted 493 nm photons absorbed in NbN are A30 E2 0.980 / 1.470%, E1 1.149–1.164 / 1.720–1.743%; B60 E2 1.838 / 2.709%, E1 2.067–2.105 / 3.029–3.082% (80 / 160 nm cap). These exclude internal detection efficiency and recovery losses; the fill factor is already included in absorption.
- **Ray footprint:** maximum spreading in the cap is A30 20–22 / 41–44 nm and B60 31–33 / 62–66 nm (80 / 160 nm cap, across Au options and E1 height brackets). Current centred detector envelopes contain every aperture ray. With 160 nm cap, full-envelope radial alignment margin is about 0.93 µm; 1 / 2 µm radial misalignment misses about 0.20 / 3.3% of aperture rays. These are continuous-envelope estimates, not wire-resolved electromagnetic efficiencies. A 2 µm axial offset remains contained. A hypothetical exactly window-sized envelope, perfectly centred, loses only about 0.32–0.39% of window rays through cap spreading at 160 nm; it is not a connected, fabrication-qualified replacement design.
- **Electrical cost:** covered straight wire is 21.875 / 18.478% of total straight length (5.76 / 11.04 mm). With the existing dirty-BCS assumptions (400 Ω/square, Tc 7.9 K), straight-section kinetic inductance is 3.10 / 5.94 µH and L/50 Ω is 62.0 / 118.8 ns, excluding turns, tapers and connections. An ideal 150-line window-sized straight-section count gives 48.4 / 96.8 ns; the extra straight length therefore adds 13.6 / 22.0 ns. These are current recovery constants, not measured detection dead times. Kerman2006 Fig. 3 relates efficiency recovery to both inductance and the efficiency-versus-bias curve.
- **Bends:** the drawn inner slot radius is 35 nm (70 nm gap / 2), with 0.5 µm end blocks. Au coverage does not remove the series switching-current constraint. ClemBerggren2011 Sec. VII.4 / Figs. 8–9 explain geometry-dependent current crowding. The sharp-turn factor in sim/15 is not a quantitative prediction for these rounded GDS turns; no switching-current factor is assigned here.
- **Cap discrepancy:** step 26 specifies the current design target of 160 ± 10 nm total SiO₂ over NbN, but `make_chip.py` and the generated simulation metadata still state 80 nm, as do older process notes. GDS does not encode this deposited thickness. Both cases were evaluated; no fabrication recipe, metadata, or layout was changed by this audit.

**Verification and limits.** Exact rectangular solid angle agrees with the existing numerical integral to < 2e-7 absolute fraction. Optical spatial-grid refinement (120 → 240 per axis) changes absorption by < 5e-5 absolute fraction; ray angular-grid refinement (16384 → 32768) changes no-margin capture by < 1e-5 absolute fraction. These checks establish numerical consistency only. Diffraction, arbitrary-azimuth grating response, actual NbN optical constants, internal efficiency, bias dependence, RF response and measured recovery remain unqualified. No reduction in overhang was adopted. Sources read: [Kerman2006, Fig. 3](https://qnn-rle.mit.edu/documents/kerman-published-version-2006.pdf), [ClemBerggren2011, Sec. VII.4](https://arxiv.org/html/1109.4881), [Hampel2023, Figs. 3–4](https://tf.nist.gov/general/pdf/3223.pdf).

---

## 2026-11-08: Step 29, validate the generated 360 µm pad rows (`gds/check_package_fanout.py`; `sim/16_pad_pitch_check.py`, `12`, `13`)

**Status.** The current generated layout passes the checks below. **Team adoption of the pitch is pending** review of future perpendicular beam access near the zones. `notes/decisions.md` is unchanged. Record for the proposed decision: 360 µm pitch; rejected alternatives listed with the proposal: 180, 240, 300, 400 µm; the team's only supplied reason is to keep wire angles below 45° for a PGA84L-like package. Carrier and spacer choices remain open in `fab/OPEN_DECISIONS.md`.

**Layout.** `make_chip.py`: PAD_P 180 → 360 µm, X_ROW_IN 2000 → 600 µm. Actual pad centres from `trap_die_v4_A30_pads.csv`: TL/BL at x = −3500…−980, TR/BR at +3500…+620, y = ±4720 µm. Side pads: RF (4700, 0), C (−4650, 450), SNS/SNG (−4750, ±100), GND spots (±4700, ±1500). B60 shares these positions; NODET omits SNS/SNG. Staircase finger heights are unchanged; horizontal track lengths and riser positions changed. The supplied regenerated A30/B60/NODET/UNIFORM dies, wafer and run layouts were retained; this validation did not regenerate them. Test dies and archived v3 files were not changed.

**Package measurement and mapping [team calc].** Source `PGA84L1993`: [local cavity drawing](<pkg-pga84l-char (1).pdf>), extract page 2 / printed p. 4-24, dated 1993-05-14. Author/publisher are not identified in the supplied drawing. Cavity J = K = 0.470 in = 11.938 mm. Its vector bounds are (127.44, 169.77)…(486.11, 535.24) PDF points, giving independent x/y scale factors 33.284077 / 32.664788 µm per PDF point. Each finger centre is the average of the midpoints of its two long vector edges. All 84 measured centres were visually checked on the drawing. Rotate 90° counterclockwise as labelled, then mirror x to convert the bottom view to the die-facing view; centre the die on the cavity. These are approximate drawing-derived positions, not a manufacturing-tolerance specification.

| Die-facing edge | Fingers | Measured x range (mm) | Measured y range (mm) |
|---|---:|---|---|
| Top | 21 | −5.592…+5.536 | +6.690 |
| Bottom | 21 | −5.596…+5.540 | −6.590…−6.579 |
| Left | 21 | −6.648…−6.635 | −5.481…+5.656 |
| Right | 21 | +6.588…+6.600 | −5.486…+5.651 |

Full measured positions, including original PDF coordinates: [package_fingers.csv](sim/out/16_pad_pitch_check/package_fingers.csv). Local IDs T/B01…21 run left to right, L/R01…21 bottom to top; **these are not electrical package pin numbers**. `check_package_fanout.py` enumerates ordered, one-to-one mappings on each edge, minimizing the worst angle and then total projected wire length. Angles are atan(|tangential displacement| / |normal displacement|), measured from the die-edge normal. Wires join chip-pad centres to package-finger centres. The earlier 0.25 mm landing assumption and ±0.15 mm sweep were dropped at the user's request.

| Edge | Wires | Worst pad → finger | Worst angle | Longest projected wire |
|---|---:|---|---:|---:|
| Top | 17 | TL1 → T03 | 18.93° | 2.082 mm |
| Bottom | 17 | BL1 → B03 | 20.03° | 1.979 mm |
| Left | 5 | SNG → L10 | 8.58° | 1.988 mm |
| Right | 3 | GND-4 → R08 | 4.97° | 1.900 mm |

All 42 connections have distinct package fingers and no crossings. Top/bottom angles are below 45°; side angles are below the expected approximately 20°. Full pad/finger endpoints, electrode names, lengths and angles: [fanout.csv](sim/out/16_pad_pitch_check/fanout.csv); [diagram](sim/out/16_pad_pitch_check/fanout.png), [SVG](sim/out/16_pad_pitch_check/fanout.svg), [source hash and geometry summary](sim/out/16_pad_pitch_check/fanout_summary.json). This nominal plan represents one connection per chip pad; additional RF wires and electrical pin assignments await the carrier-specific bond plan.

**Layout checks.** `check_chip.py` rerun on current A30, B60 and NODET: **ALL CHECKS PASS** on each; minimum conductor spacing 5.00 µm, zero floating Au islands, and no pads in the beam-exit corners. [Checker inputs and logs](sim/out/16_pad_pitch_check/checks_manifest.json) are fingerprinted so these results can be tied to the checked files.

**Sim 12 comparison [team calc].** Seven cases run sequentially through the `electrode` launcher, using the unchanged sim 12 and solver source: 53 V RF, 28 MHz, 0.8 MHz axial; regular static zones use 10° tilt and ±10 V limits, transport uses zero tilt and a fixed electrode set. The queue script archives old summaries, waveforms and plots in `sim/out/12_final_chip/pad180/` before overwriting outputs; the seven `_pad180.txt` logs remain intact. Current canonical logs now correspond to the 360 µm layout. Exported zone voltages have 1 mV precision; waveform exports have 10 µV precision.

| Case | Loading max V, old → new | Readout max V, old → new | Largest readout electrode change | Transport max step, old → new (V per 10 µm) |
|---|---:|---:|---:|---:|
| A30 E2 | 7.45 → 7.45 | 6.28 → 6.29 | 0.018 V | 7.589287 → 7.590069 |
| A30 E1 | 7.45 → 7.45 | 6.27 → 6.28 | 0.018 V | 7.590345 → 7.591113 |
| A30 E2, centre DC = 0 | 10.00 → 10.00 † | 10.00 → 10.00 † | 0.117 V † | **1.710110 → 1.708356** |
| B60 E2 | 7.46 → 7.45 | 2.24 → 2.25 | 0.006 V | 8.001455 → 8.002177 |
| B60 E1 | 7.45 → 7.45 | 2.24 → 2.24 | 0.006 V | 8.001464 → 8.002183 |
| B60 E2, centre DC = 0 | 10.00 → 10.00 † | 10.00 → 10.00 † | 0.117 V † | **1.710110 → 1.708356** |
| NODET | 7.92 → 7.93 | 7.87 → 7.89 | 0.021 V | 1.661964 → 1.662091 |

† The centre-zero **static** zone solves remain bounded at 10 V and achieve approximately 0.794–0.795 MHz. They are diagnostic, as in steps 25/28; regular zone sets supply the stationary 10° tilt. The centre-zero **transport** solves achieve 0.800 MHz without clipping.

All five regular zone cases meet the ±10 V / 0.8 MHz requirement; both centre-zero transport runs are below the user-confirmed 1.75 V per 10 µm limit. Each transport sweep contains 49 positions (48 transitions) over 480 µm. Every saved 77-point RF-null scan is identical to its pad180 baseline. Transport planar height ranges are E2/NODET 49.970817…49.976975 µm and E1 49.957822…49.963980 µm. The user confirmed applying the 49.96–49.98 µm criterion at **two-decimal reporting precision**, with raw values retained. Recess-corrected readout heights are separate quantities and were not used for this planar-height criterion. Across all waveform electrodes and positions, the largest voltage change is 0.01284 V.

Data: [comparison.json](sim/out/16_pad_pitch_check/comparison.json), [per-electrode zone comparison](sim/out/16_pad_pitch_check/zone_voltage_comparison.csv), [per-electrode waveform comparison](sim/out/16_pad_pitch_check/transport_voltage_comparison.csv). Operating readout sets change by at most 0.021 V; the 0.117 V diagnostic change triggered the optional sim 13 rerun.

**Sim 13 rerun [team calc].** All four A30/B60, E2/E1 cases rerun. Old outputs are in `sim/out/13_dc_height_tuning_v4_pad180/` (also preserving the existing inputs to the separate overhang audit). At the achieved upward displacement needed to undo the existing window correction:

| Case | Required max V, no tilt: old → new | Required max V, 10°: old → new | Micromotion at 10°, new |
|---|---:|---:|---:|
| A30 E2 | 1.3377 → 1.3355 | 6.0641 → 6.0681 | 173.36 nm |
| A30 E1 | 1.5190 → 1.5164 | 6.1991 → 6.2027 | 54.88 nm |
| B60 E2 | 0.6639 → 0.6639 | 1.9086 → 1.9117 | 290.83 nm |
| B60 E1 | 0.6741 → 0.6740 | 2.1363 → 2.1390 | 81.46 nm |

The largest required-voltage change is 0.00403 V; sim 13 null heights and window-drop inputs are unchanged. E1 still uses the existing 1 µm-pocket upper-bound window correction. Full [height-tuning comparison](sim/out/16_pad_pitch_check/13_comparison.json) and [run log](sim/out/16_pad_pitch_check/13_log_pad360.txt).

---

> **Steps 30–36 (2026-11-09) close the v4 loose ends.** The scripts, layouts and pages were written by delegated agents from a written specification. Every acceptance number quoted below was rerun independently before it was logged. None of these steps is a team decision; `notes/decisions.md` is unchanged.

## 2026-11-09: Step 30, is 50 µm the right ion height? (`sim/17_height_tradeoff.py`)

**Question (team).** A higher ion is more stable but collects less light. Keep 50 µm, or redesign lower?

**Model.** The gapless five-wire model of step 1 (`trapcalc.fivewire_rf_phi`), which matched gds2itvg to 0.1 µm at 50 µm (step 2). For each height the RF rail width is set so the null sits there. Collection is for an isotropic emitter through the E2 aperture (ion height + 6 µm). Beam clipping is the formula of sim 11 (10 mm die, 45°). [team calc]

**A. Centre DC kept at 40 µm, so the 30 µm window stays.**

| h (µm) | RF rail (µm) | Depth at 3 MHz radial, 28 MHz (meV) | Drive that keeps 52 meV at q 0.30 | Collection A30 / B60, E2 (%) | Heating, h⁻⁴ (h⁻²·⁶) | 493 nm clipped |
|---|---|---|---|---|---|---|
| 30 | 12.5 | 14.9 | 123 V, 52 MHz | 4.73 / 7.92 | 7.7× (3.8×) | 10 % |
| 35 | 26.9 | 21.3 | 83 V, 44 MHz | 3.77 / 6.50 | 4.2× (2.5×) | 6.9 % |
| 40 | 43.6 | 29.5 | 67 V, 37 MHz | 3.06 / 5.42 | 2.4× (1.8×) | 4.5 % |
| **50** | **83.6** | **51.9** | **53 V, 28 MHz** | **2.13 / 3.90** | **1×** | **1.7 %** |
| 60 | 132.5 | 83.2 | 48 V, 22 MHz | 1.56 / 2.92 | 0.48× (0.62×) | 0.54 % |
| 70 | 190.3 | 124.2 | 46 V, 18 MHz | 1.19 / 2.26 | 0.26× (0.42×) | 0.15 % |

**B. Whole trap scaled with h (c = 0.8 h, window = c − 10 µm).** Collection falls when the trap shrinks, because the 5 µm rims and gaps do not shrink: 2.13 % at 50 µm, 1.72 % at 40 µm, 1.16 % at 30 µm (E2). Lower h raises collection only if the window keeps its size.

**C. Height kept at 50 µm, wider centre DC (window = c − 10 µm radially, 30 µm axially).** c = 50 µm: 2.77 %, 58 V, 46.6 meV. c = 60 µm: 3.36 %, 71 V, 43.3 meV. c = 70 µm: 3.90 %, 98 V, 41.3 meV.

**Reading.**
- Going from 50 to 40 µm with the same window gives 1.44× the light. It costs 2.4× the heating at h⁻⁴ (1.8× at h⁻²·⁶), 2.6× the clipped beam power, a 44 µm RF rail, and a window that is 0.75 h wide instead of 0.6 h (larger null drop and mode splitting: steps 6, 19).
- The same or a larger gain is available at 50 µm without those costs: the 160 nm cap (absorption 0.44 → 0.66, step 26), the B60 window (1.83×, drawn), E1 Au (1.22×, the aperture sits 5.65 µm closer) or a wider centre DC (1.3× at c = 50 µm).
- Absolute level: A30 on E2 absorbs 1.47 % of all emitted 493 nm photons (step 32). At about 10⁷ photons/s from a bright ion (Zhukas et al., arXiv:2006.12801, one source, read through a summarising tool) that is about 15 counts per 100 µs before the internal detection efficiency. [team calc]

**Decision (team, 2026-11-09; `notes/decisions.md`): keep 50 µm.** The team adopted the assessment below as its reason.

**Assessment (Claude, `design/` exception).** 50 µm is adequate; a lower trap is not worth a redesign. Height is the most expensive lever for collection in this design, and beam clipping on the 10 mm die (1.7 %) already argues against going lower.

**Limits.** Gapless, infinitely long model; no window perturbation in the collection column. The heating exponent is not universal: Sedlacek 2018 measured 3.9(2) at 295 K and 4.0(2) at 5 K over 29–83 µm; An 2019 reports 2.6 for electric-field noise over 50–300 µm (abstract only). Pointers: `research/research_notes/Loose ends 2026-11/`.

---

## 2026-11-09: Step 31, do E1 and E2 differ functionally? (`sim/18_e1_vs_e2.py`)

**Question (team).** E1 is 0.35 µm lift-off Au, E2 is 6 µm plated Au. Is there a functional difference beyond the process?

**Already simulated.** Zone and transport voltages agree to 0.01 V and null heights to 0.02 µm (steps 25, 28). As traps, the two are the same.

| Quantity | E1, 0.35 µm | E2, 6 µm | Source |
|---|---|---|---|
| Au sheet resistance at room temperature, bulk ρ 2.44 µΩ·cm | 0.070 Ω/sq | 0.0041 Ω/sq | [team calc]; thinner than the 14.9 µm skin depth at 28 MHz, so the DC value applies |
| One SNSPD slot lead (5 µm wide, 995 squares as drawn) | 69 Ω | 4.0 Ω | [team calc], room temperature |
| Lead pair in series with the 50 Ω line, cold | 14–69 Ω (RRR 10–2) | 0.8–4 Ω | RRR is an assumption [verify]; no measured value found for either film |
| Pulse amplitude and reset-time factor 50 / (50 + R pair), RRR 5 | 0.64 | 0.97 | [team calc] |
| Centre DC lead (7.5 µm wide, 394 squares) | 27 Ω | 1.6 Ω | [team calc], room temperature |
| RF dissipation, C_RF 1–2 pF, RRR 5 | 31–126 µW | 1.8–7.4 µW | upper bound; C_RF not computed [verify] |
| Screening of charge on the SiO₂ gap floor, exp(−π t / g), 5 µm gaps | 0.80 | 0.023 | [inference]: lowest slot mode, not a field solve |
| Same for the 30 µm window | 0.96 | 0.53 | [inference] |
| SiO₂ gap depth-to-width | 0.07 | 1.2 | LOCAL_MIRROR H.4 |
| Window null drop, A30 / B60 | ≤ 0.37 / ≤ 0.55 µm | 1.19 / 2.04 µm | steps 25, 26 |
| Micromotion after retuning the height, 10° tilt, A30 / B60 | 55 / 81 nm | 173 / 291 nm | step 29 |
| Geometric collection, A30 | 2.60–2.64 % | 2.22 % | step 32 |
| RF pickup: nanowire / each slot lead | 1.92 / 28.3 µA | 0.96 / 44.5 µA | steps 26, 28 |

**Reading.** Four differences matter:
1. **Charge on the SiO₂ in the gaps.** E2's 6 µm walls screen the gap floor about 35× better. With E1 the ion sees SiO₂ along the whole trap. Todaro trapped on 6 µm Au; Hampel (350 nm) reports no trapping.
2. **SNSPD lead resistance.** With E1 the two slot leads add tens of ohms in series with the 50 Ω readout line, which lowers the pulse amplitude and shortens the reset. With E2 the leads are negligible.
3. **Light and the window.** E1 collects 1.18× more and perturbs the RF null about three times less.
4. **RF heating.** Tens to hundreds of µW on E1, 17× less on E2; small either way, but it scales with C_RF², which is not known.

Process differences (plating bath, step coverage over the 0.40 µm via, wedge bonding on 350 nm Au) are in `fab/process/03_ELECTRODES.md`. **The choice stays the team's**; no option is recommended here.

**Literature (L2 note).** No measured resistivity at 4 K was found for 0.35 µm evaporated or 6 µm plated Au; a witness measurement would settle the RRR bracket. No source quantifying stray field from a charged trench floor against metal thickness was found.

---

## 2026-11-09: Step 32, collection and absorption on the v4 stack (`sim/15b_collection_v4.py`)

Closes "rerun 15 at the v4 heights". Parts A–C of sim 15 on the v4 stack: vacuum / SiO₂ cap 160 nm (and 80 nm) / NbN 7 nm, fill 0.65 / SiO₂ spacer 238 nm / Al 450 nm / SiO₂ 1 µm / Si. No D2 layer, so no fringe average. Heights from `sim/out/13_dc_height_tuning_v4/summary.json`; E1 is bracketed between the planar null and the 1 µm-pocket drop. [team calc]

| Case | Ion height (µm) | Geometric collection (%) | Absorbed of all emitted, 80 / 160 nm cap (%) |
|---|---|---|---|
| A30 E2 | 48.79 | 2.221 | 0.981 / 1.470 |
| A30 E1 | 49.60–49.96 | 2.601–2.636 | 1.149–1.164 / 1.720–1.743 |
| B60 E2 | 47.93 | 4.158 | 1.838 / 2.709 |
| B60 E1 | 49.42–49.96 | 4.674–4.760 | 2.067–2.105 / 3.029–3.082 |

- Normal-incidence unpolarised absorption 0.662 (160 nm) and 0.440 (80 nm), as sim 09c.
- Ray spread in the cap is at most 0.044 µm (A30) and 0.066 µm (B60) at 160 nm, so the meander envelope catches every window ray.
- All rows reproduce the overhang audit to the digits it printed. Internal detection efficiency, polarisation dependence of the meander and RCWA are still not included.

---

## 2026-11-09: Step 33, RF current through the nanowire against the lead termination (`sim/19_lead_termination.py`)

**Why.** Each slot lead collects 44.5 µA (E2) or 28.3 µA (E1) of common-mode 28 MHz current (step 28). Only an asymmetry between the two leads' paths to ground drives it through the nanowire.

**Model [inference].** Two nodes (the pad ends of the leads), equal injected currents, each node to ground through a 2 nH bond wire [verify] and its termination, and the nanowire as jωL_k plus the lead-pair resistance between them. L_k 3.10 µH (A30) and 5.94 µH (B60). Lumping the distributed pickup at the pads makes it an upper bound.

| Termination (signal lead / return lead) | Nanowire current, A30 E2 (µA) | A30 E1 (µA) | Effect on the detector pulse |
|---|---|---|---|
| 50 Ω line / short to ground | 4.06 | 2.58 | none |
| 50 Ω ∥ 100 pF / short | 3.20 | 2.04 | low-pass at 31.8 MHz |
| 50 Ω ∥ 1 nF / short | 0.47 | 0.30 | low-pass at 3.18 MHz |
| 50 Ω ∥ 10 nF / short | 0.046 | 0.029 | low-pass at 0.32 MHz |
| 50 Ω ∥ 1 nF / 1 nF, 0–20 % mismatch | 0.053–0.090 | 0.034–0.057 | low-pass at 3.18 MHz |
| 50 Ω ∥ series L-C trap at 28 MHz (100 pF, 0.5 Ω) / short | 0.040 | 0.026 | trap is 524 Ω at 3 MHz, 139 Ω at 10 MHz |
| same, L off by ±5 % | 0.23 | — | — |
| 50 Ω / 50 Ω (differential), 0 / 5 / 10 % mismatch | 0 / 0.20 / 0.40 | 0 / 0.13 / 0.25 | none |

- Reference: the switching current is estimated at 8–20 µA (step 26). A plain 50 Ω line with the return grounded puts half of the 8 µA lower bound through the A30 nanowire on E2.
- The pulse decays in L_k / 50 Ω = 62 ns (A30) or 119 ns (B60), a spectral corner of 2.6 or 1.3 MHz. A 1 nF bypass, the value suggested in step 26, puts its corner at 3.2 MHz, right on the pulse.
- A lead-pair resistance up to 140 Ω changes these currents by less than 6 %.
- This feeds the open **RF grounding / filters** decision. No termination is chosen here.

---

## 2026-11-09: Step 34, how fast can the ion be moved? (`sim/20_transport_timing.py`)

Closes "adiabatic transport timing" at the level of a first estimate. Input: `sim/out/12_final_chip/trap_die_v4_A30_V2zero/waveforms.csv` (centre DC at 0 V, 49 positions, 10 µm apart).

**Model [inference].** A classical ion in a 0.8 MHz axial well whose centre s(t) moves 480 µm in a time T. Residual motion n̄ = (m / 2ħω)·|∫ s̈ e^{iωt} dt|². Zero-point size 6.77 nm. The well centre is assumed to follow the filtered voltages linearly.

**Smooth ramps.** A minimum-jerk position ramp stays below 0.1 quanta for every T above 44 µs; a sin² ramp above 207 µs. A linear ramp never settles (envelope 2 × 10⁴ quanta at 100 µs).

**The DAC staircase is the limit.** One sudden 10 µm step leaves 5.5 × 10⁵ quanta; 1 µm leaves 5.5 × 10³; 0.1 µm leaves 55.

| Staircase, 10 kHz first-order filter | T = 100 µs | 300 µs | 1 ms | 3 ms |
|---|---|---|---|---|
| 48 steps of 10 µm | 76 | 1.4 × 10⁵ | 76 | 1.4 × 10⁵ |
| 480 steps of 1 µm | 2.2 | 0.56 | 0.75 | 1.4 × 10⁵ |
| 4800 steps of 0.1 µm | 2.0 | 0.23 | 0.022 | 0.0056 |

(n̄ with T shifted by 0.3 axial periods off the commensurate values; at exactly commensurate T the sum is either zero or the coherent maximum.)

- Whenever the step interval is a whole number of axial periods, the kicks add coherently (the 10⁵ entries). A finer staircase moves that resonance to longer T; it does not remove it.
- With 48 steps the update rate is far below the axial frequency (48 kHz at T = 1 ms against 800 kHz), so every step is a separate kick and only the filter attenuates it.
- **Consequence:** the 10 µm table from sim 12 is a set of static solutions, not a waveform. It has to be interpolated to steps well under 1 µm, with a DAC update rate above the axial frequency or a filter of higher order, before it is played.
- DAC numbers for 48 steps: largest step 1.708 V (electrode 11, GDS x from 50 to 60 µm), largest voltage 6.64 V, slew 0.082 V/µs at T = 1 ms.

**Limits.** One dimension, classical, harmonic, constant frequency along the path, no heating during the move, first-order filter only.

---

## 2026-11-09: Step 35, v4 test dies, cap metadata, measured layout numbers (`gds/make_test_die.py`, `check_test_die.py`, `measure_dies.py`, `make_chip.py`)

**Cap metadata.** `make_chip.py` and every `_sim.json` now state the 160 nm cap of step 26 (`t_sio2_above_nbn` 0.08 → 0.16; "0.32 µm" → "0.40 µm" in two comments). A per-layer XOR against the previous dies is zero on A30, B60, NODET and UNIFORM, so layer 50 is unchanged and sim 12 was not rerun. `check_chip.py`: **ALL CHECKS PASS** on A30, B60, NODET; the light footprint moves from the window + 0.02 µm to + 0.05 µm (A30) / + 0.07 µm (B60).

**Test dies for v4 (Claude's layout calls, `design/` exception).** `test_die_v4` and `test_die_v4_TRAP` replace the v3 files, which moved to `gds/archive_v3_baseline/`.
- Removed: T2 (Au / D2 / Al capacitor), layer 45, the die-wide Al and its cut-outs.
- Kept: T1, T3, T6, T8, T9, T4 / T4b. Every meander now has a local Al mirror (the drawn NbN + 4 µm, running 160 µm under its leads) with a mirror probe pad.
- New: **T2v** Au / 0.40 µm SiO₂ / Al capacitor, 200 × 200 µm, about 3.5 pF. **T10** Al strip 40 µm wide with voltage taps 2510 µm apart (62.75 squares; 4.2–5.6 Ω at 450 nm for ρ 3–4 µΩ·cm), the stand-in for the trap's mirror ground path. **T11** chain of four 100 µm Au-to-Al vias. **T12** two 5 µm Au lines 5 µm apart, 2.7 mm long, across a 2.3 mm Al strip (the slot leads, including the step over the Al edge).
- `--trap-only`: T1 and T6 on layers 1 and 50 only.
- **No mirror probe opening is added to the trap dies.** T10 and T11 measure the same path on the test die, so layer 50 near the trap stays untouched.
- On the test structures the 4 µm layer-22 leads cross the edge of the 450 nm Al under the spacer. The trap die has no such crossing. [inference: a possible weak point of the test structures only]

**Checks.** `check_test_die.py` was written from the specification, not from the generator. It found one fault the generator's own self-check missed: the mirror under the sharp-turn T9 control had a 1 µm margin, because that meander is drawn 36 µm tall for a nominal 30 µm. Three further faults were found by review and fixed: T10 end pads not touching the strip (an error in the specification), T12 lines meeting their pads along a 2.5 µm edge, and two T1 comb fingers left as separate conductors by an edge-only contact (inherited from v3). Final state: **ALL CHECKS PASS** on both dies; 30 Au conductors, all ≥ 5 µm apart. `run_R1_TRAP`, `run_R1_FULL` and `wafer_v4` regenerated.

**Measured from the released GDS (`gds/measured_v4.md`, with file hashes).**

| | A30 | B60 | NODET | TEST | TEST_TRAP |
|---|---|---|---|---|---|
| Layer 10 Al (mm²) | 0.142 | 0.143 | 0 | 0.710 | 0 |
| Layer 20 NbN (µm²) | 1928 | 2615 | 0 | 20 270 | 0 |
| Layer 22 Ti/Au (mm²) | 0.0021 | 0.0021 | 0 | 1.012 | 0 |
| Layer 40 openings (mm²) | 0.0114 | 0.0114 | 0 | 0.653 | 0 |
| Layer 50 Au (cm²) | 0.9131 | 0.9131 | 0.9147 | 0.1267 | 0.2141 |

- Meanders: 160 lines, 0.130 µm wide on a 0.200 µm pitch, 36 / 69 µm long; straight length 5.760 / 11.040 mm; 3.10 / 5.94 µH and 62.0 / 118.8 ns at 69.95 pH/sq (turns, tapers and tabs excluded).
- Runs: Au 5.917 cm² (`run_R1_TRAP`) and 5.735 cm² (`run_R1_FULL`); EBL area of `run_R1_FULL` 0.0496 mm² merged (0.0502 mm² as a raw sum).
- These replace the mixed v3 estimates in the mask list (plated area, EBL charge).

---

## 2026-11-09: Step 36, fabrication pages rewritten for v4; stack and process-flow figures (`fab/`)

**Team instruction (2026-11-09):** rewrite the fab pages for v4 now, with E1 and E2 both written out, without waiting for the electrode choice.

- **Rewritten:** `STACK.md`, `process/01_FOUNDATION.md` … `04_PACKAGING.md`, `RUNSHEET_R1_TRAP.md`, `QUALIFICATION.md`, `process_checks.md`, `test_plan.md`, `tests/01` … `04`, `TRAVELER.md`, `README.md`, `VARIANTS.md`, `RUN_PLAN.md`, `mask_list.md`, `LAYOUT.md`. The v3 banners are gone.
- **Step numbers are kept:** 0–3 foundation (step 3 = local Al mirror, detector dies only), 4–8 detector, 9 and 10 removed, 11 layer-40 openings through the thin stack, 12–15 electrodes as branch E1 or branch E2, 16a and 16 removed, 17–19 test, dice, package. R1_TRAP uses 0–2, 12–15 and 17–19.
- **Rule the writers worked under:** values are carried from the v3 pages, `LOCAL_MIRROR.md` and steps 25–29; nothing new is invented; anything no source gives is tagged `[verify]`. No page recommends E1 or E2.
- **New test identifiers:** a15 (T2v), a16 (T10), a17 (T11), a18 (T12), a19 (SNSPD leads to the centre DC). a4 is retired. a13 (ground link) no longer uses the < 10 Ω limit, because the Al strip alone is about 5 Ω.
- **Figures:** `fab/figures/stack_v4.svg` (five cross-section panels, E1 solid and E2 dashed) and `fab/figures/process_flow_v4.svg` (one composite cross-section per step, written by `make_process_flow.py`). Both are drawn flat, with the Al mirror embedded and the NbN inset under a level SiO₂ cap (the stack figure was corrected to this on 2026-11-09; it first showed the layers over the Al raised). Neither draws the real 0.45 µm step at the mirror edge, |y| = 20 µm; the stack figure and `fab/STACK.md` state it in words.
- **Link checker:** `fab/check_links.py` checks every relative link and heading anchor under `design/fab`.
- **Sources resolved:** "Dietl 2025" is M. Dietl et al., "Test and characterization of multilayer ion traps on fused silica", arXiv:2505.21284. Its Table 2 gives the 50 V DC / 300 V RF, 0–100 nA leakage limits and the 1 mA, 0–100 mV continuity test used in a1–a3. Those traps have Al electrodes on fused silica; no comb structure or flashover measurement was found in it, so the T1 limits remain `[verify]`. Suleimen 2026 is Phys. Rev. Applied 25, 044091; only the abstract is open.
- **Opened by the rewrite, for the team:** whether R1_TRAP also deposits the 398 nm of PECVD SiO₂ so its electrodes sit on the same surface as the detector dies; whether NODET dies on R1_FULL get steps 4–8; the T10 acceptance limit; no v4 witness covers the 300 °C cap deposition on NbN now that W1-b is gone.

**Reproducibility.** `sim/run_cached_geometry.py` reuses exact unions of identical immutable Shapely polygon pairs only inside the solver's gap-splitting routine (bounded cache, restored afterward); no coordinates, precision, solver source or physical model were changed. Repeated union results were checked byte-for-byte on overlapping polygon pairs. The compiler cache was placed in a writable ignored directory. Solver revision, package versions and input hashes are recorded in [environment.json](sim/out/16_pad_pitch_check/environment.json) and the comparison files. Re-run sim 12 with `cd design/sim` then `./run.sh 16_pad_pitch_check.py`; `--resume` rechecks completed cases only when simulation inputs match. The fan-out script requires Python with `pdfplumber` (the bundled document runtime was used here). Sim 13 used `./run.sh run_cached_geometry.py 13_dc_height_tuning.py` with a writable NUMBA_CACHE_DIR.

**Still open.** Confirm future perpendicular beam clearance before adopting the inward rows; choose 84-pin vs 100-pin/lab carrier and its electrical pin map; qualify the proposed ≥ approximately 0.6 mm, die-sized-or-larger spacer (Si suggested). The planned 45° beam arrangement remains the stated use case; no future-beam clearance was approved in this step.

---

## 2026-11-09: Step 37, what the Al mirror thickness buys, and the step it leaves (`sim/10c_mirror_thickness.py`)

**Question (team, 2026-11-09).** The stack figure showed the detector raised over the mirror; the process-flow figure showed it flat. Which is built, and is the 450 nm Al (team decision 2026-11-08, step 28) worth the step it causes?

**The step is real.** Step 3 leaves the Al standing on the thermal SiO₂ at |y| ≤ 20 µm and no later step planarizes, so the SiO₂ spacer, NbN, SiO₂ cap and Au over the mirror sit one Al thickness above the same layers beside it: 0.45 µm today. The mirror edge is also the centre-DC edge. With E1 the 0.35 µm evaporated Au has to climb that step wherever it leaves the mirror. All simulations assume coplanar electrodes.

**Hampel 2023 (arXiv:2302.01462 v1, read in full).** No mention of planarization, a recess or the step. Their mirror is 50 nm e-beam evaporated Al by lift-off on 150 nm PECVD SiO₂, left raised, under a 350 nm evaporated Au lift-off (Au 7× the step). NbTiN was co-sputtered at 500 °C over that Al. With the mirror grounded they report no induced-current signature up to 54 V at 70 MHz and attribute the remainder to RF heating. Those devices did not trap an ion. The published APL version was not re-opened.

**Simulation (`10c`, same 2-D solver as `10b`; 53 V, 28 MHz; SiO₂ cap 160 nm; ρ(Al) 3–4 µΩ·cm, room temperature).** The reference case reproduces `10b` exactly. Values are for E2; E1 is within 3 % except the direct pickup.

| Al mirror | Step | T10 strip | Current to the via | Swing at the detector | Extra wire current (upper bound) | Strip dissipation | Lead common mode from the mirror | Micromotion, A30 / B60 |
|---|---|---|---|---|---|---|---|---|
| 50 nm, raised | 50 nm | 38–50 Ω | 3.13 mA | 59–79 mV | 1.43–1.91 µA | 65–87 µW | 8.0–10.7 µA | ≤ 4.1 / 8.2 nm |
| 100 nm, raised | 100 nm | 19–25 Ω | 3.14 mA | 30–40 mV | 0.72–0.95 µA | 33–44 µW | 4.0–5.4 µA | ≤ 2.1 / 4.1 nm |
| 150 nm, raised | 150 nm | 13–17 Ω | 3.14 mA | 20–26 mV | 0.48–0.64 µA | 22–29 µW | 2.7–3.6 µA | ≤ 1.4 / 2.7 nm |
| 450 nm, raised (today) | 450 nm | 4.2–5.6 Ω | 3.15 mA | 6.6–8.8 mV | 0.16–0.21 µA | 7.4–9.8 µW | 0.9–1.2 µA | ≤ 0.5 / 0.9 nm |
| 450 nm, inlaid 0.45 µm into the thermal SiO₂ | 0 | 4.2–5.6 Ω | 3.42 mA | 7.2–9.6 mV | 0.17–0.23 µA | 8.7–11.5 µW | 1.0–1.3 µA | ≤ 0.5 / 1.0 nm |

For comparison: direct rail-to-wire pickup 0.96 µA (E2) / 1.90–1.92 µA (E1); direct lead pickup 44.5 µA (E2) / 28.5 µA (E1) per lead; switching current 8–20 µA; window micromotion 173 nm (A30 E2), ≤ 55 nm (E1) (step 27); RF rail dissipation 1.8–7.4 µW (E2), 31–126 µW (E1) (step 31, which assumed RRR 5 for the Au).

**Reading (Claude's assessment, not a team decision).**
1. The mirror's pickup goes to ground: about 3.1 mA flows along the strip to the via at every thickness. What can reach the nanowire is a second-order term, the swing of the strip's detector end coupled through the 137 fF between mirror and meander. It is under 0.1 % of the strip current.
2. For the SNSPD that term is small at every thickness. At 50 nm it is at most the size of the direct pickup on E1 and twice it on E2; at 100 nm it is at most equal to the direct pickup on E2. All are below the 4 µA that an unmatched lead termination can add (step 33). The 450 nm choice bought 0.3–0.45 µA relative to 150 nm.
3. For the ion it does not matter: the mirror swing seen through the window gives at most a few nm of micromotion (small-patch estimate), against 55–173 nm from the window itself.
4. The cost of a thin mirror is heat, not induced current. A 50 nm strip dissipates 65–87 µW, which makes the mirror the largest RF dissipator on an E2 chip and comparable to the rails on E1. Hampel names RF heating as their residual limit. These numbers use room-temperature resistivity, so they overstate the cold value; there is no thermal model.
5. The mirror swing adds 2–4 % (450 nm) to 18–38 % (50 nm) to the common-mode pickup on each slot lead. It reaches the nanowire only through a termination mismatch, as in step 33.
6. Inlaying the 450 nm mirror removes the step and costs about 9 % more strip current, because the Si is 0.45 µm closer to the rails. It needs a 450 nm Al lift-off into a recess, which no source read so far covers.

**Options for the team.** (a) A thin raised mirror by evaporation and lift-off, as Hampel built: 100 nm leaves a 0.10 µm step under 0.35 µm Au and halves the 50 nm penalties; 50 nm is the fully sourced case. This reverses the 450 nm decision. (b) Keep 450 nm and inlay it: flat, but a new process with its own witness loop. (c) Keep 450 nm raised and rely on step 15 and T12 to show the E1 Au crosses the step. Claude's recommendation was (a) at 100 nm. **Decided the same day: 100 nm, inlaid (step 38).**

**Limits.** 2-D model; ideal conductors; ω V C upper bounds; room-temperature Al resistivity; no thermal model; the micromotion figure is a small-patch estimate; the raised cases are solved with coplanar electrodes, so the step itself is not in the field model.

**Figures.** `fab/figures/stack_v4.svg` was redrawn flat on 2026-11-09 to match the process-flow figure, with the true step stated under panel (a) and in `fab/STACK.md`.

---

## 2026-11-09: Step 38, the Al mirror becomes 100 nm, inlaid (`sim/10c_mirror_thickness.py`; `fab/`)

**Team decision (2026-11-09; `notes/decisions.md`).** The local Al mirror is 100 nm of evaporated Al, inlaid in the thermal SiO₂. It replaces the 450 nm mirror of 2026-11-08. The team's reasons: the built electrodes should be the coplanar geometry that was simulated; E1's 0.35 µm Au should not climb a 0.45 µm step; and step 37 showed the reason for 450 nm was weak, because the mirror's pickup goes to ground.

**Process (Claude's design call under the `design/` exception).** Step 3 keeps its number and becomes four sub-steps with one resist and the existing layer-10 data:

| Sub-step | What | Where the recipe comes from |
|---|---|---|
| 3a | LOR + positive resist, layer 10 drawn (open where the mirror goes) | old step 3 lift-off route |
| 3b | RIE a 100 nm recess into the 1.0 µm thermal SiO₂ | CHF₃ / CF₄ / Ar of step 11 |
| 3c | e-beam evaporate Al to the measured recess depth, 100 nm nominal | evaporator of E1; Hampel 2023 for evaporated Al |
| 3d | lift-off; the Al top is level with the SiO₂ | as step 6 / E1 |

- 0.9 µm of thermal SiO₂ remains under the mirror.
- Planarity limit: residual step and any lip or groove at the mirror edge ≤ 20 nm (a design call, to be checked).
- Fallback: skip 3b, which gives a 100 nm raised mirror with the same mask.
- New witness loop W8: recess depth and RIE rate with the lift-off resist on the wafer, lift-off after the fluorine etch, residual step and edge profile, hillocks on evaporated Al after 300 °C.
- No GDS change; nothing was regenerated.

**Simulation (`10c`, new case `al100_inlaid`: Al 100 nm over 0.90 µm thermal SiO₂; 53 V, 28 MHz; ρ(Al) 3–4 µΩ·cm at room temperature).** Reran; the ten acceptance checks pass and the earlier rows are unchanged.

| | E2 | E1 |
|---|---|---|
| Sheet resistance; T10 strip | 0.30–0.40 Ω/sq; 18.8–25.1 Ω | same |
| Current along the strip to the via | 3.19 mA | 3.25 mA |
| Swing at the detector end | 30.2–40.3 mV | 30.8–41.0 mV |
| Extra nanowire current, upper bound | 0.73–0.97 µA | 0.74–0.99 µA |
| Direct rail-to-wire pickup, for comparison | 0.96 µA | 1.92 µA |
| Dissipation in the strip | 34–45 µW | 35–47 µW |
| Common mode added to each slot lead (direct) | 4.1–5.5 µA (44.5) | 4.1–5.5 µA (28.6) |
| Micromotion from the mirror swing, A30 / B60 | ≤ 2.1 / 4.2 nm | ≤ 2.1 / 4.3 nm |

Inlaying costs 2 % in strip current against the 100 nm raised case (3.19 against 3.14 mA on E2), because the Si is 0.1 µm closer; the 450 nm inlay cost 9 %.

**What this accepts.** The strip dissipates about four times what the 450 nm strip did (34–45 against 7–10 µW), on room-temperature resistivity and with no thermal model; Hampel names RF heating as their residual limit, so the cold RF test should watch the switching current against RF amplitude. The mirror is evaporated Al without Cu. No source read so far covers a recess-and-lift-off inlay, lift-off after a fluorine etch, or hillocks on 100 nm evaporated Al (`research/research_notes/Loose ends 2026-11/L3_inlaid_mirror.md`), so W8 carries that risk.

**Pages and figures.** Rewritten for the 100 nm inlaid mirror, each citing `sim/10c` and step 37 where it states the thickness or a pickup number: `fab/STACK.md`, `process/01_FOUNDATION.md` (step 3 as 3a–3d with the fallback), `02_DETECTOR.md`, `03_ELECTRODES.md`, `04_PACKAGING.md`, `QUALIFICATION.md` (W8), `process_checks.md`, `tests/01_ELECTRICAL.md` (T10 expected 18.8–25.1 Ω), `tests/02_CRYOGENIC.md`, `tests/03_READOUT.md`, `test_plan.md`, `TRAVELER.md`, `mask_list.md`, `RUN_PLAN.md`, `README.md`, `VARIANTS.md`, `LAYOUT.md`, `variants/LOCAL_MIRROR.md` (row 3v and the stack line only). `fab/figures/stack_v4.svg` and `process_flow_v4.svg` draw the Al inside the top of the thermal SiO₂; the process flow has three panels for step 3 (18 panels). The Al labels in `architecture_crosssection.svg` and `open_decisions_map.svg` were updated. `gds/layer_map.md` row 10 and the test-die docstring were updated as text only. A consistency pass over all the pages followed; the direct lead pickup on E1 now reads 28.6 µA (160 nm cap, `10c`) where pages had 28.3 µA (80 nm cap, `10b`).

**Still open.** W8 before a device wafer; an Al source on the E1 evaporator; the SiO₂ RIE rate on our tool; over-etch into the 100 nm Al at the mirror via; the T10 acceptance limit; a thermal estimate for the strip.

---

## 2026-11-09: Step 39, what a raised mirror and a misaligned mirror do to the RF null (`sim/10d_mirror_step.py`)

**Question (team).** Even a 100 nm raised mirror should not matter much; can the worst case be simulated?

**Model.** The 2-D finite-volume solver of `10b` / `10c` on the full cross-section through the lead slot (both signs of x), with the real heights: the SiO₂ and the Au over the mirror drawn `s` higher than beside it, and the mirror shifted sideways by `d`. RF rails at 1 V, everything else at RF ground. The null is found from a linear fit of the field around its minimum. Cases: `s` = 0 (inlaid 100 nm), 100 nm, 450 nm; `d` = 0, 2, 5 µm (5 µm is the overlay the mask list carries for layer 10, marked [verify]; the tool budget on the same page is 0.5–1 µm per layer); E2 and E1. Reference: inlaid, `d` = 0. 53 V, 28 MHz, ¹³⁸Ba⁺.

**Checks.** Left-right symmetry holds to under 1 nm at `d` = 0. The micromotion figure equals (q/2) × displacement in every case. The null shift is linear in the step on E2 (ratio 4.51 for 4.5). On E1 the ratio is 5.35; it is not checked there, because a 450 nm step is taller than the 0.35 µm Au. The absolute values of this boxed 2-D model are off against `gds2itvg`: null 47.4–47.8 µm above the Au instead of 49.97 µm, q 0.347 instead of 0.30. The cause was not tracked down (grounded lid and walls at 400 µm, real gaps), so only differences between cases are used.

**Results: shift of the RF null against the reference, and the micromotion if the DC set is not re-tuned.**

| Mirror | `d` (µm) | E2: sideways / height (nm) | E2: Δq | E2: micromotion (nm) | E1: sideways / height (nm) | E1: Δq | E1: micromotion (nm) |
|---|---|---|---|---|---|---|---|
| inlaid | 0 | 0 / 0 | 0 | 0 | 0 / 0 | 0 | 0 |
| inlaid | 2 | 15 / 10 | 0.01 % | 3 | 496 / 332 | −2.4 % | 101 |
| inlaid | 5 | 30 / 23 | 0.03 % | 7 | 1052 / 785 | −4.6 % | 217 |
| raised 100 nm | 0 | 0 / 163 | +0.47 % | 28 | 0 / 130 | +0.42 % | 23 |
| raised 100 nm | 2 | 45 / 143 | +0.42 % | 26 | 529 / 458 | −2.0 % | 119 |
| raised 100 nm | 5 | 60 / 132 | +0.39 % | 25 | 1108 / 911 | −4.2 % | 238 |
| raised 450 nm | 0 | 0 / 734 | −0.9 % | 126 | 0 / 694 | −3.8 % | 116 |
| raised 450 nm | 2 | 142 / 623 | −1.1 % | 110 | 653 / 959 | −3.5 % | 194 |
| raised 450 nm | 5 | 129 / 505 | −1.3 % | 89 | 1244 / 1336 | −5.8 % | 298 |

**Reading (Claude's assessment, not a team decision).**
1. **The step itself is harmless.** A 100 nm raised mirror lifts the null by 0.13–0.16 µm and changes q by under 0.5 %. The lift is the same wherever the mirror runs, and it runs under both zones, so the ion simply sits at the new null. Left uncorrected it would be 23–28 nm of micromotion, which ordinary micromotion compensation removes; the window already costs 55–173 nm (step 27). The hand estimate before the run was 70 nm; the simulation gives about twice that.
2. **The 450 nm mirror was not harmless in the same way:** 0.7 µm of lift and 116–126 nm if uncorrected. Going to 100 nm removed most of it, inlaid or not.
3. **Misalignment of the mirror matters far more than the step, on E1.** Inlaid and with no step at all, a mirror 2 µm off centre moves the null 0.5 µm sideways on E1 and 5 µm off moves it 1.05 µm, about 0.2–0.25 µm per µm of misalignment. On E2 the same errors move it 15–30 nm. Cause [inference]: the mirror edge is drawn on the centre-DC edge, so a shifted mirror reaches into the 5 µm gap next to one RF rail, 0.4 µm under the surface, and pulls the gap floor to ground there. With 0.35 µm Au the field above sees that; with 6 µm Au the gap is a deep trench and the field above does not.
4. The step adds only 30–55 nm sideways to that on top of the misalignment.
5. A sideways shift is also uniform along the mirror and is compensated like any stray field, but 0.5–1 µm is of the size of the window drop and changes the DC set needed.

**What follows.**
- For the ion, 100 nm raised and 100 nm inlaid are equivalent. The inlay now rests only on the fab argument (0.35 µm Au over a 0.10 µm step, which Hampel's 350 nm over 50 nm suggests is fine) and on keeping the build identical to the drawings. The raised mirror is the simpler process and is already the named fallback.
- **Proposal (not done; it changes layer 10 of the A30 and B60 dies):** pull the mirror edge in from the centre-DC edge, from |y| ≤ 20 µm to |y| ≤ 18 µm. The NbN reaches |y| = 16 µm, so that leaves 2 µm on each side: 2 µm of mirror beyond the NbN and 2 µm of Au beyond the mirror. A mirror misaligned by up to 2 µm then stays under the centre-DC Au and never reaches the gap. `check_chip.py` requires the mirror to cover the NbN by 3 µm today; that rule would become 2 µm. Layer 50 does not change, so the trap simulations stand.
- Whatever the outline, the layer-10 to layer-50 overlay should be held to about 1 µm, not the 5 µm carried on the mask list, when the electrodes are E1.

**Addendum, same day: these shifts are compensated by the DC electrodes, and the micromotion column overstates the uncorrected case.** [hand estimate, not simulated]
- A shifted null is a static offset, the same along the whole mirror. The ion sits on the RF null whenever the DC field there is zero, so the DC set only has to be trimmed for where the null really is. That is ordinary micromotion compensation.
- The trim is small. The DC field needed to move the DC zero-field point is m(ω_ax²/2)Δ/e ≈ 18 V/m per µm of null shift at 0.8 MHz axial, so about 19 V/m for the worst case here (1.05 µm sideways).
- The micromotion column assumed the ion stays at the old null. It does not: the RF confinement (3 MHz) is much stiffer than the radial DC curvature (ω_ax²/2, about 0.57 MHz equivalent), so with no trim at all the ion follows the null to within ω_ax²/(2ω_r²) ≈ 4 % of the shift. For the worst case that is about 50 nm off the null and about 8 nm of micromotion, not 217 nm. The DC quadrupole that sets the 10° tilt can raise this to roughly 10 % of the shift.
- What compensation does not undo: q lower by 2–5 % on E1 at 2–5 µm misalignment, and the ion up to 1 µm off the centre of the 30 µm window. Neither is a problem.
- So the mirror-outline proposal above is a convenience, not a requirement. It would make the DC set computed from the drawn layout correct without a trim.

**Limits.** 2-D cross-section through the lead slot: no window and no mirror end. The mirror ends 28 µm past the readout-zone centre, where a raised mirror gives an axial change in null height of 0.13–0.16 µm that this model cannot resolve. Ideal conductors; SiO₂ drawn with vertical steps; leads and DC electrodes at RF ground; absolute height and q biased as noted above.

---

## 2026-11-10: Step 40, a transport waveform that a DAC could play (`sim/21_transport_waveform.py`)

Closes the "10 µm table is not a waveform" item of step 34 as far as a model can. Written by a delegated agent from a specification; the acceptance numbers below were read back from the three `summary.json` files before logging.

**Method.** The static solve of sim 12 (fixed electrode set, zero tilt, centre DC at 0 V on A30 and B60, free on NODET) repeated every 2 µm between loading and readout (5 µm on B60, the script's fallback when the machine was loaded); a cubic spline per electrode; a minimum-jerk position against time; samples at a DAC update rate; 16-bit quantisation over ±10 V; a first-order filter. At each zone the transport set is blended linearly into the regular 10° zone set. Defaults: 1 ms move, 100 µs per tilt ramp, 1 MHz updates. The DAC and filter values are **[verify]**: the lab's hardware is not known.

| Check | A30 | B60 | NODET |
|---|---|---|---|
| Largest difference from the sim 12 table on its 10 µm grid | 5.0 µV | 5.0 µV | 5.0 µV |
| Largest \|V\| while moving / largest change per 10 µm | 6.64 V / 1.708 V | 6.64 V / 1.708 V | 7.20 V / 1.662 V |
| Well position error at the midpoints, with interpolated voltages | 0.007 nm | 0.29 nm (5 µm grid) | 0.006 nm |
| Axial frequency deviation at the midpoints | 3 × 10⁻⁷ | 1 × 10⁻⁵ | 2 × 10⁻⁷ |
| Zone sets against sim 12 (loading / readout) | 7.45 / 6.29 V | 7.45 / 2.25 V | 7.93 / 7.89 V |

- **Interpolation is not the limit.** The static solutions vary so smoothly with position that a spline through 2 µm points puts the well within 0.01 nm of where it should be (zero-point size 6.77 nm).
- **The tilt hand-off is safe by construction.** Both end sets have zero field at the same point, so every blend between them does too (largest residual 10⁻¹¹ V/m). Along the blend the radial axes turn from 0° to 10°, the radial frequencies stay between 2.76 and 3.12 MHz (A30), all curvatures stay positive, and the largest voltage never exceeds the larger of the two end sets.
- **DAC, A30, 1 ms move at 1 MHz:** 1001 updates, at most 0.154 V and 0.9 µm per update. At 100 kHz the same move takes 9 µm and 1.5 V steps.
- **Resolution.** One 16-bit step on the most sensitive electrode moves the well 1.0 nm; all electrodes together, 2.3 nm root-sum-square.
- **Motion left after the move (classical model of step 34):** below 10⁻³ quanta for every case at 1 MHz updates (3.6 × 10⁻⁵ at 100 µs with a 50 kHz filter).
- **A rate to avoid.** At 100 kHz updates the model leaves 5 × 10⁶ quanta whatever the move time. 100 kHz divides the 0.8 MHz axial frequency exactly, so every update kicks the ion at the same phase and the kicks add up to one jump of the full 480 µm, reduced only by the filter. This is the commensurate case of step 34. An update rate that is not a sub-multiple of the axial frequency, or a different axial frequency, avoids it; that case was not scanned here.

**Outputs.** `sim/out/21_transport_waveform/<die>/waveform.csv` (time, phase, position, V2 to V36), `static_fine.csv`, `summary.json`, plots.

**Limits.** The model of step 34: classical, one dimension, the well follows the filtered voltages linearly, no heating during the move. Quantisation noise and DAC glitches are not modelled. The radial modes during the move are not examined.

---

## 2026-11-10: Step 41, chip RF capacitance, loss and the resonator (`sim/22_rf_capacitance.py`)

Closes "chip RF capacitance is not computed". Written by a delegated agent from a specification; rerun before logging, with the same `summary.json`.

**Method.** The 2-D solver of `10c`, one cross-section per stretch of the RF net measured on the released A30 layout, times the length of the stretch: rails beside the lead slot and mirror (2240 µm), plain rails (1760 µm), the U bar (75 µm), the 60 µm feed line with 10 µm gaps to the Au ground fill (2525 µm), the pad with 30 µm gaps (200 µm). Ends and corners are neglected [inference]. B60 is taken equal to A30.

| | Rails, slot | Rails, plain | Feed | U bar + pad | **Chip** |
|---|---|---|---|---|---|
| A30, E2 (pF) | 1.12 | 0.86 | 0.53 | 0.07 | **2.59** |
| A30, E1 (pF) | 1.03 | 0.79 | 0.50 | 0.07 | **2.39** |

NODET: 2.57 pF (E2) and 2.37 pF (E1) with the full SiO₂ stack; 2.68 and 2.48 pF with thermal SiO₂ only.

- **RF current into the chip** at 53 V, 28 MHz: 24.2 mA (E2), 22.3 mA (E1).
- **Where the field energy is:** 63 % in the Si and 20 % in the SiO₂ (A30, E2).
- **Loss, first-order estimate [inference].** Si at the 20 kΩ·cm lower spec has tan δ = 0.27 at 28 MHz at room temperature. With 63 % of the energy in it, the chip alone has Q ≈ 6 at room temperature; inside a resonator with other, lossless capacitance the limit is (C_total / C_chip) times that, about 21 for 9.6 pF in total. 0.27 is not small, so this is an order of magnitude. Cold, with the carriers frozen out, only the SiO₂ counts: Q of the chip 490 to 49 000 for tan δ of 10⁻² to 10⁻⁴ **[verify]** (no loss tangent has been measured for these films). **A resonator Q measured at room temperature with a die mounted will not predict the cold value.** Dietl 2025 (Sec. 2.2) reports more heating than modelled where RF reaches bare low-resistivity Si.
- **RF heating in the Au (the bound of step 31, at the computed capacitance):** 0.031 mW (E2) and 0.45 mW (E1) with bulk resistivity and RRR 2. The ratio is 14.6, not the 17 of step 31, because E1 has less capacitance.
- **Resonator, A30 on E2:** with 3, 7 or 17 pF of other capacitance (values other groups report for a die, a package and a whole system; sources in `table.md`) the inductance for 28 MHz is 5.8, 3.4 or 1.7 µH, and the drive power at a loaded Q of 100 is 14, 24 or 48 mW. One pF of error moves the resonance by 9, 5 or 3 %.
- **Electrical test a10** (capacitance at 1 MHz, room temperature): the Si conducts at 1 MHz, so the reading is not the chip capacitance above. It lies between 2.6 pF (Si as a dielectric) and 23 pF (Si as a grounded conductor under the SiO₂) for A30, plus the carrier. A single reading cannot be compared with one expected value.

**Checks.** Reproduces `10b` (0.2486 pF/mm per rail) and `10c` (0.1529 fF/µm rail to mirror, 2.132 aF/µm rail to lead); halving the grid changes the capacitance per length by under 0.5 %; the feed section is 0.88 of the textbook coplanar-waveguide value; reproduces the 1 pF row of sim 18.

**Limits.** 2-D sections; ideal conductors; the ground fill beside the feed treated as solid; Si depth as in `10c`; package, bond wires and resonator not included.

---

## 2026-11-10: Step 42, RF coupling onto the DC electrodes and what a filter capacitor does (`sim/23_dc_rf_coupling.py`)

Closes "DC-to-RF coupling capacitances (field solve) to decide on filter capacitors" at the level of a 2-D model. It does not choose a capacitor. Written by a delegated agent from a specification; rerun before logging, with the same `summary.json`.

**Method.** The 2-D solver of `10c` with the current stack. Each conductor of the cross-section (RF rails, centre DC, slot lead, Al mirror, outer conductor) is set to 1 V in turn and the charge on every conductor is integrated: a capacitance matrix per unit length, for the lead-slot section and the plain section, for E1 and E2. Lengths: 2240 µm of slot section and 1760 µm of plain section for the centre DC; 120 µm for one outer segment. The RF voltage left on an electrode is the divider 53 V × C_c / (C_c + C_g + C_f). The null shift comes from the gds2itvg unit potentials of that electrode and the RF Hessian at the zone.

| Electrode | Coupling to the rails, C_c | To ground, C_g | RF voltage with no capacitor | with 1 nF | with 10 nF |
|---|---|---|---|---|---|
| Centre DC, A30, E2 | 0.41 pF | 3.2 pF (3.1 pF of it to the Al mirror) | 6.1 V | 22 mV | 2.2 mV |
| Centre DC, A30, E1 | 0.33 pF | 3.1 pF | 5.0 V | 17 mV | 1.7 mV |
| Centre DC, NODET, E2 | 0.74 pF | 0.12 pF | 45.5 V | 39 mV | 3.9 mV |
| One outer segment, E2 | 0.015 pF | 0.4–0.6 pF (pad and lead track, an estimate from the bond-pad notes) | 1.3–1.9 V | 0.8 mV | 0.08 mV |

- **The centre DC is the electrode that matters.** It runs the full length between the rails. On NODET it has almost no capacitance to ground of its own, so with nothing attached it would follow the rails at 45.5 V. On A30 the grounded mirror under it takes most of that away, and it would still carry 6 V. This column is a limit, not a proposal: it says the centre DC cannot be left without an RF ground.
- **Null shift at the readout zone, A30 on E2,** from the RF voltage on the centre DC: 2.8 µm with no capacitor, 96 nm with 100 pF, 10 nm with 1 nF, 1.0 nm with 10 nF. From the nearest top and bottom segments together: 0.10 nm with 1 nF.
- **Current through the capacitor on the centre DC:** 3.9 mA (A30, E2), 6.9 mA (NODET, E2). It returns through the bond wire and the carrier ground.
- The 0.41 pF agrees with the 0.5 pF estimated in the SNSPD geometry audit.
- **Mirror to centre DC: 3.1 pF,** not the "about 12 pF" of `fab/variants/LOCAL_MIRROR.md`. That estimate took the full 40 µm width; with the lead slot only 15 µm of centre DC lies over the mirror.

**Checks.** Reproduces `10c` (rail to lead 2.1322 aF/µm on E2 and 1.3698 on E1; rail to mirror 0.15294 fF/µm; lead to mirror 0.4888 fF/µm); the matrix is symmetric to 10⁻¹⁴; the charges sum to zero.

**Limits.** 2-D: no segment ends, no lead tracks near the rails. The inductance of the bond wire and of the lead between the electrode and the capacitor is ignored [inference], which matters most for the 10 nF column. The outer segment's capacitance to ground is taken from estimates made for an older stack. The 3-D pickup on the SNSPD leads is still not modelled: gds2itvg builds its electrode model for the ion's region and cannot be evaluated at the chip surface, so a planar charge integral was not attempted.

---

## 2026-11-10: Step 43, RCWA of the NbN meander (`sim/24_rcwa_meander.py`)

Closes "RCWA of the meander" for normal incidence. Written by a delegated agent from a specification; rerun before logging; the convergence rule was then tightened (see below) and the script rerun.

**Method.** Rigorous coupled-wave analysis with the `grcwa` package (0.1.2, in a separate conda env `rcwa`; setup in the script's docstring), 493 nm, normal incidence, the stack of `09c`: vacuum / SiO₂ cap / 7 nm grating of NbN lines 130 nm wide on a 200 nm pitch with SiO₂ between / 238 nm SiO₂ spacer / Al. Absorption in the NbN layer only, from the power flux above and below the grating layer. Indices as `09c`.

| SiO₂ cap | Field | Effective medium (`09c`, `15b`) | RCWA | RCWA / effective medium |
|---|---|---|---|---|
| 160 nm | along the wires | 0.830 | 0.822 | 0.99 |
| 160 nm | across the wires | 0.494 | 0.833 | 1.69 |
| 160 nm | unpolarised | 0.662 | 0.827 | 1.25 |
| 80 nm | unpolarised | 0.440 | 0.583 | 1.32 |

- **Along the wires the two models agree to 1 %.** Across the wires they do not: the effective-medium model mixes NbN and SiO₂ in series, which is right for a grating much thicker than its pitch. These lines are 7 nm thick and 130 nm wide, so nearly all of each line sees the field unscreened, and the rigorous result is almost independent of polarisation [inference for the explanation; the numbers are the solver's].
- **The 160 nm cap is still at the maximum:** the RCWA cap scan peaks at 0.829 near 170 nm and is within 0.02 of that from 150 to 180 nm.
- **What this would change, if adopted:** the absorbed fraction of all emitted photons scales with the unpolarised absorption, so the 1.47 % (A30, E2) and 2.71 % (B60, E2) of step 32 would become about 1.84 % and 3.4 % at normal incidence [team calc: ratio 1.25 applied; the emission-cone average of step 32 was not redone]. The key-number tables keep the effective-medium values, labelled as such, and quote this result beside them.

**Checks.** A uniform NbN film reproduces the transfer-matrix result exactly; the in-script effective-medium calculation reproduces the stored `15b` values to 10⁻⁹; reflected, transmitted and absorbed power sum to 1. Convergence: along the wires the value is steady at 0.8217 from 11 to 199 harmonics; across the wires it drifts from 0.839 at 7 harmonics to 0.8325 at 199. The script first stopped at a change of 0.005 (5 harmonics); it now stops at 0.001, which gives 0.833 at 99 harmonics.

**Limits.** Normal incidence only; the cone of angles from the ion is not averaged. The NbN index is the literature value of `09`, not a measurement of the team's film. A second lattice period of 1 nm is used to make the problem one-dimensional. No other RCWA code was run as a cross-check.

---

## 2026-11-10: Step 44, readability pass (documentation; no design change)

No layout, no GDS and no team decision changed in this step. Done by delegated agents from written specifications, with each package checked before it was committed.

**New pages.** `START_HERE.md` (entry page), `GLOSSARY.md`, `sim/INDEX.md`, `primers/RF_PRIMER.md` with `primer_numbers.py`, `fab/tests/00_SETUP.md` and `05_SIMPLER_TESTING.md`, six briefs in `fab/briefs/`, `figures/` (one plot style, a die map, eight report plots with no captions), and three source notes in `research/research_notes/Test setup 2026-11/`.

**Numbers kept honest.** `check_numbers.py` reads each key number from the sim outputs through the pointers in `facts_now.json`, checks that the current-state pages quote it, and flags known stale strings. It found 30 stale lines (the 80 nm cap, v3 pickup and collection, step-25 voltages, "46 µA" from the 600 µm-zone run, v3 test dies, the Dietl statements); all are fixed and it now reports none. `fab/check_links.py ..` covers all of `design/`: 0 broken links.

**Sources re-read.** Dietl 2025 was read from the arXiv PDF (pages 4–12). The 120 probe needles and the Table 2 limits are in the paper; two earlier notes here said the needles were not. Hampel 2023 (pages 2–3) and Slichter 2017 (pages 9–11) were read from their PDFs for the test pages: both tested detectors on trap chips with LED flood light and no ion.

**Housekeeping.** 26 superseded log files moved to `sim/out/archive/` (none is read by a script); stale docstrings fixed in sims 05, 12 and `trapgeom.py`; `CLAUDE_PROGRESS.md` reordered so the current state comes first.

**Found and not fixed.**
- `sim/16_pad_pitch_check.py --resume` refuses to run. Its stored input hashes date from step 29; the die files were regenerated in step 35. It needs a full rerun to be usable again. Its input files are all present.
- The switching-current estimates still disagree (8–9 µA against 8–20 µA; `fab/tests/02_CRYOGENIC.md`).
- `fab/LAYOUT.md` says the test dies have no bond pads while `fab/tests/02_CRYOGENIC.md` says to bond T4 and T4b.
- The journal reference of the Siverns helical-resonator paper differs between the arXiv page and an earlier note here.

---

## 2026-11-10: Step 45, radial tilt up to 45° (`sim/25_radial_tilt_sweep.py`)

**Why.** The 10° radial tilt in the zones came from step 11 ("in-plane 45° beams cool both radial modes") with no source and no other angle tried. Every beam runs parallel to the surface at 45° to the trap axis, k̂ = (1, 1, 0)/√2 in the ITVG frame. A Doppler beam cools mode i at a rate proportional to (k̂·êᵢ)², so with the radial axes exactly in the plane and vertical the vertical mode is not cooled. With the axes tilted by θ, the near-vertical mode gets ½ sin²θ: 0.015 at 10°, 0.058 at 20°, 0.125 at 30° and 0.25 at 45°, against 0.5 for the axial mode [team calc]. Allcock et al. 2010 (arXiv:0909.3272, read from the PDF) tilt the axes of a symmetric surface trap with a DC "tilt" quadrupole and note that the tilt would be 45° as soon as the radial degeneracy is lifted (p. 2); Table III (p. 5) gives 42° at 2.90 / 3.34 MHz. The question from the team: can this trap reach 45°?

**Method.** Two ways of setting the tilt, on the v4 dies A30, B60 and NODET (E2), at both zones:
- *natural split* (the sim 12 rule): keep the radial split the trap has and set tan 2θ = 2K_xz/ΔK. It cannot reach 45°.
- *fixed split*: choose the split Δf_r and the angle; the DC supplies the two free radial curvatures (K_xx − K_zz and K_xz; their sum is fixed by Laplace and the axial row). θ is the angle of the higher-frequency mode from the in-plane axis and runs 0–90°, because which mode is naturally higher differs between zones.

The voltages are minimum-norm solves over the 14 nearest electrodes (as sim 12) and over all 35. A Gaussian error of 10 mV on every voltage (200 draws) gives the scatter of the angle. Natural split at 10° reproduces sim 12 on every die (A30 7.45 / 6.29 V, B60 readout 2.25 V, NODET 7.93 / 7.89 V).

**45°, fixed split 0.1 MHz, all DC electrodes, largest |V| without the ±10 V clip:**

| Zone | 0.8 MHz axial | 0.6 MHz axial |
|---|---|---|
| Loading (A30, B60) | 11.30 V | 8.41 V |
| Loading (NODET) | 11.04 V | 8.27 V |
| Readout A30 | 13.27 V | 9.51 V |
| Readout B60 | **6.81 V** | 5.88 V |
| Readout NODET | 11.01 V | 8.23 V |

- At 0.8 MHz axial and ±10 V, 45° fits only at the B60 readout. The largest tilt that fits at 0.1 MHz split is 25–27° at the loading zones and the NODET readout, and 23° at the A30 readout.
- Each further 0.1 MHz of split costs about 4.6–4.9 V at 45° (A30 loading: 15.9 V at 0.2 MHz, 20.5 V at 0.3 MHz).
- **What costs the voltage** (scratch decomposition of the minimum-norm solve, A30 and NODET): about 6.4–6.7 V for the 0.8 MHz axial curvature with the radial split held at zero (8.7–10.3 V at the A30 readout), plus about 4.9–5.0 V per 0.1 MHz for K_xz. The K_xz part is carried by top/bottom segment pairs driven in opposition (24/9, 22/8, 23/7 at loading; 26/11, 12/27, 13/28 at readout). At 50 µm the outer segments are weak at making K_xz.
- **Robustness at 45°, 0.1 MHz:** 10 mV errors give an angle scatter of 0.8–1.4° (std). The stray curvature the trap will see is not known.
- **A split centre DC** (the arrangement Allcock used) would be far stronger: a 2-D estimate with gapless strips (`trapcalc.strip_phi`) gives about 0.15 V per 0.1 MHz once the x-field is cancelled with an outer pair, against about 5 V now [team calc, 2-D, not run on the GDS]. It is a layout change.

**Assessment (Claude's, not a team decision).** 45° at 0.8 MHz needs a larger DC range (the Sinara 5633 HV amplifier, 5× to ±50 V, step 46) or a split centre DC. Without either, 45° at 0.1 MHz split fits at 0.6 MHz axial, with the A30 readout at 9.5 V. The cooling benefit has not been turned into rates or temperatures: the per-mode formula (Itano & Wineland 1982) was not opened.

**Also found.** The readout window lowers the ion vertically, so the excess micromotion it leaves is vertical. A beam in the plane has no component along it at any tilt, so RF-photon correlation with the in-plane beams (04_TRAPPING step 9) does not measure it. Allcock 2010 added a beam reflected off the trap surface for micromotion compensation (p. 5); the method itself was not read in detail.

**Outputs.** `sim/out/25_radial_tilt_sweep/<die>/` and `<die>_fax0.6/` (`summary.json`, `vmax_vs_theta.png`, `projection_vs_theta.png`). Literature pointers: `research/research_notes/Radial tilt 2026-11/` (written by a delegated agent; checked against the PDF only for Allcock pp. 2–5).

---

## 2026-11-10: Step 46, the lab's DAC and the DC channel count (`sim/26_dc_channel_count.py`)

**Input from the team.** The lab's DC DAC is a Sinara Zotino. From the Sinara wiki and the ARTIQ driver docs ([T4 note](research/research_notes/Test%20setup%202026-11/T4_zotino_dac.md)): 32 channels, ±10 V, 16 bit, 1 MSPS shared between the channels, a 3rd-order Butterworth output filter at 75 kHz; output noise is not published. The ±10 V the sims used is therefore the real limit. Two consequences:
- The v4 dies have **35 DC electrodes** (2, 3–32, 33–36), three more than one Zotino.
- Sim 21 assumed 1 MHz updates on every channel and a first-order filter. With 35 channels changing, a full update takes at least 35 µs (at most about 28.6 kHz before SPI and RTIO overhead [verify]), and 800 kHz / 28.57 kHz = 28 exactly, the commensurate case of step 40. Sim 21 needs a rerun with the Zotino rate and filter.

**Question.** Can the trap run on fewer channels, by grounding electrodes or tying top/bottom pairs at the carrier, with no layout change?

**Method.** A tied pair is one channel whose unit potential is the sum of both electrodes'; grounded electrodes leave the solve. Zone solves as sim 12 (14 nearest channels, 10°), the 45° fixed-split solve of step 45 (0.1 MHz, all channels), and transport from loading to readout on a 10 µm step with a fixed set of all channels and zero tilt (centre DC at 0 V on A30 and B60, free on NODET, as sim 12). "all35" reproduces sim 12 on all three dies (A30 7.45 / 6.29 V, transport 6.64 V and 1.708 V per step; NODET transport 7.20 V and 1.662 V).

| Configuration | Channels | A30 zones at 10° (loading / readout) | A30 transport: max \|V\| / max step | NODET transport: max \|V\| / max step | 45° readout A30 at 0.8 / 0.6 MHz |
|---|---|---|---|---|---|
| all35 | 35 | 7.45 / 6.29 V | 6.64 / 1.708 V | 7.20 / 1.662 V | 13.27 / 9.51 V |
| caps grounded (33–36) | 31 | 7.45 / 6.29 V | 6.66 / 1.709 V | 7.20 / 1.662 V | 13.60 / 9.70 V |
| caps grounded, pairs 3+18, 4+19, 16+31, 17+32 tied | 27 | 7.43 / 6.32 V | 6.63 / 1.708 V | 7.20 / 1.662 V | 13.31 / 9.54 V |
| caps and 3, 18 grounded | 29 | 7.45 / 6.29 V | 6.66 / 1.709 V | 7.20 / 1.662 V | 13.61 / 9.70 V |
| also 4, 19, 17, 32 grounded | 25 | 7.45 / 6.29 V | 6.69 / 1.709 V | 7.20 / 1.662 V | 13.70 / 9.75 V |
| also 5, 20, 16, 31 grounded | 21 | 7.39 / 6.29 V | 6.82 / 1.712 V | 7.21 / 1.662 V | 13.95 / 9.90 V |

No configuration has a clipped step in transport, and the axial frequency stays at 0.800 MHz. B60 behaves like A30 (readout 2.25 V at 10° in every configuration).

**Assessment (Claude's, not a team decision).** One Zotino is enough. Grounding the four end caps (31 channels) changes nothing that matters, and going down to 21 channels costs at most 0.18 V in transport and 0.7 V in the 45° readout solve. Fewer channels also shorten each full update (1 MSPS / 21 ≈ 48 kHz at most). The 45° tilt at 0.8 MHz still needs more than ±10 V in every configuration except at the B60 readout. The grounding is done at the carrier or the breakout, so the choice can wait until bonding. Not checked: anything beyond the two zones and the transport between them (for example loading at another position), and the role of the end caps if the zones ever move outward.

**Outputs.** `sim/out/26_dc_channel_count/<die>/` (`summary.json`, `transport_maxV.png`).
