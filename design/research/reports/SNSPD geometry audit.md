> **Claude-authored** research report (design/research), 2026-11-08. It audits the v3 integrated NbN SNSPD geometry and proposes a new one. It does not replace the cited sections and figures: read them before acting. Tags: **[team calc]** = computed for this project (in the research notes or in this session), **[inference]** = reasoning, not data, **[verify]** = not yet checked against the source or on the tool. Raw notes: `design/research/research_notes/SNSPD geometry audit/` (four files), building on `research_notes/Trap integrated SNSPD design/`.

# Move the turnarounds out of the light

> **Superseded in part (2026-11-11).** The v3 values in lines 7 and 43 (100 nm wires, 150 lines, 150 nm Al, 80 nm cap, 10 µm D2, bare SiO₂ window floor) are replaced in v4 by 130 nm wires, 160 lines, a 100 nm inlaid Al mirror, and a 160 nm cap with no D2. The bond-level return fix (line 335) is superseded by the on-chip Au-fill-to-Al via on layer 40 (decision 2026-11-08). The ≈0.5 pF rail-to-centre estimate (line 314) is replaced by 0.414 pF from sim 23 (`design/sim/out/23_dc_rf_coupling/summary.json`, `per_electrode.E2.centre_A30.C_c_pF`). Current: [layer stack](../../fab/STACK.md).

**Bottom line.** The v3 meander is 7 nm NbN, 100 nm wires on a 200 nm pitch (fill factor f = 0.5), 150 lines along the trap axis, with square-cornered hairpins exactly at the edges of the Au window. Three things in this geometry cost efficiency and switching-current headroom, and each can be fixed in the layer-20 layout alone.

- **Footprint.** The meander is the same size as the window, but light that passes the window edge refracts outward through 10 µm of SiO₂ and lands 2.5 µm (A30) to 3.9 µm (B60) beyond it. **About 20 % of the photons that pass the window miss the NbN** [team calc].
- **Fill factor.** At f = 0.5 the NbN absorbs only **≈0.40** at 493 nm. The channel with E perpendicular to the wires absorbs 0.20 against 0.61 for E parallel [team calc, effective-medium model].
- **Hairpins.** Sharp hairpins limit the device switching current to **≈0.54–0.65 of a straight wire** ([Clem & Berggren Eq. 100](https://ar5iv.labs.arxiv.org/html/1109.4881) applied to this geometry [team calc]).

**Recommended geometry.** Keep the electron-beam-written (HSQ) NbN meander with lines along the axis. Make three changes:

1. Widen the wire to **130 nm on the same 200 nm pitch** (f ≈ 0.65).
2. Extend the lines **≈3 µm (A30) or ≈4.5 µm (B60) past each axial window edge**, so every turnaround sits under the Au outside the illuminated footprint. Extend the meander 1–2 µm radially, after one RF check.
3. Use **rounded-slot turnarounds with a solid end block**, and a tapered junction into the contact tabs.

Predicted geometric × absorption efficiency with internal efficiency set to 1 goes from **0.71 % to ≈1.2 % (A30)** and from **1.37 % to ≈2.2 % (B60)** [team calc].

**The turnaround-versus-absorption tension.** It cannot be resolved the way the notes first suggest. An interleaved meander at f ≥ 0.5 has no room to open a 2W gap at its turns. So Clem & Berggren's crowding-free turn (R = 1, which needs f = 1/3) is out of reach at any useful fill factor. The workable resolution is spatial: absorb at high fill factor where the light lands, put the turns where it does not, and buy back absolute switching current with width rather than chasing R = 1.

**RF.** Wire geometry is second-order. The first-order items are:

- whether the centre DC electrode is really at RF ground (its filter capacitor is still undecided);
- the Al plane's RF potential under the 4.7 mm of SNSPD lead that rides 238 nm above it;
- the switching current at the ~5 K cryostat temperature. It may be only ≈8–9 µA, which makes the 1.4 µA pickup bound ≈16 %, not the 7–9 % in `DESIGN_LOG.md`.

**Width and Suleimen et al.** The only paper that varies NbN width for RF tolerance, Suleimen et al. 2026, was **seen only as an abstract**. Its 300 nm wire belongs on the test die, not the first trap die.

**Collection numbers.** The 3.25 % / 5.92 % in `DESIGN_LOG.md` assume a σ-dipole pattern. Ba⁺ 493 nm emission is isotropic by a team derivation that no opened source confirms, which gives **2.22 % / 4.15 %** [team calc, to check].

**How the session numbers were computed.** The refraction-footprint, isotropic-collection, Clem–Berggren and inductance numbers were computed in this session with short inline scripts through `design/sim/run.sh -c`, using `trapcalc.collection_fraction`. They are not saved as files. The effective-medium absorption numbers come from the notes' scratchpad script (`emt_angle_fill.py` in the session scratchpad, a temporary path; it extends `design/sim/09b_itoD2_matching.py` to oblique incidence and reproduces its 0.401). Effective-medium theory is the zero-pitch limit and is only indicative at a 200 nm pitch. Rigorous coupled-wave analysis (RCWA) or FDTD is needed before sign-off.

## What the v3 detector actually is

Confirmed from `design/gds/make_chip.py` (the `meander()` function, lines ~165–208) and `design/gds/layer_map.md`:

- **Lines.** `WIRE_W = 0.100`, `WIRE_P = 0.200` µm, and `nlines = DET_WY / WIRE_P = 150`. Each line is a rectangle along GDS x, which is the trap axis, spanning exactly the window: `DET_WX = WIN_WX` = 30 µm on A30 (the 30 × 30 µm window die) and 60 µm on B60 (the 60 axial × 30 radial µm die).
- **Turnarounds.** Each is a 100 nm-wide rectangle 300 nm tall placed just outside the line ends. Inner and outer corners are square, so the end-bar width equals the wire width (W′ = W). The turnarounds sit on the axial window edges, under the edge of the Au rim.
- **Tabs.** The two ends of the meander enter **40 × 3 µm NbN tabs** at the −x window edge. Each junction is an abrupt step from 100 nm to 3.1 µm, with one flush edge and one re-entrant 90° corner.
- **Leads.** Ti/Au leads (layer 22), 4 µm wide, at y = ±6 µm. They run about 4.7 mm under the 40 µm centre DC electrode and its lead to pads at (−4750, ±260) µm.
- **Stack.** The meander sits on a 238 nm SiO₂ spacer over 150 nm Al-1%Cu (layer 10), under an 80 nm SiO₂ cap and 10 µm of D2 SiO₂. There is no ITO in v3. The window floor the ion sees is bare SiO₂.

**How the Al plane is grounded changed today.** Layer 24 (the M1 via) is retired. Until DESIGN_LOG step 22 (2026-11-08) the plane was grounded only by Al wedge bonds at the four M1 openings on the die's side edges (±4700, ±2000) µm. The traveler said explicitly that there was "no on-chip link" from the Au ground fill to the Al. Step 22 added eight 150 µm layer-40 openings that tie the plated Au fill to the Al on chip, at (±4700, ±1000) and (±1000, ±2500) µm. The bond openings remain as a backup. Test-plan item a13 now requires GND-to-M1 continuity below 10 Ω.

The geometry already gets two things right. Lines run along the axis, so the 149 hairpins sit at the axial window ends, under the continuing centre-DC Au and away from the RF rails. Todaro's MoSi device also aligned its wires with the trap axis ([Todaro Supp. "Trap fabrication"](https://arxiv.org/abs/2008.00065)). And a grounded Al plane lies 238 nm under the nanowire and its leads. That is the feature Hampel et al. credit with removing the induced-current signature ([Hampel arXiv:2302.01462, Figs. 3–4](https://arxiv.org/abs/2302.01462)).

**Model inconsistencies to fix:**

| What | Where | Value | Consistent value |
|---|---|---|---|
| NbN thickness, optics and RF pickup | `sim/09b`, `sim/10` | 7 nm | matches the traveler (7 nm, Rsq ≈ 400 Ω/sq) |
| NbN thickness, inductance | `sim/06` | 5 nm film (Rs ≈ 600 Ω/sq, Lk ≈ 105 pH/sq) | 7 nm gives Lk ≈ **70 pH/sq**, so A30 L ≈ 3.2 µH and τ ≈ 63 ns rather than 4.7 µH / 94 ns [team calc, dirty-BCS from Rsq 400 Ω/sq, Tc 7.9 K] |
| Docstring | `sim/06` | still describes the v2 ITO-on-SiO₂ window and an absorption of "~0.5" | v3: no ITO, absorption ≈0.40 |
| Footprint assumption | `sim/06`, `DESIGN_LOG.md` step 7 | the 10 µm SiO₂ "spreads the light footprint by only ~2 µm per side, so a detector the size of the window catches all light" | the spread is real, so a window-sized meander does *not* catch it (next section) |

The thickness choice also matters for absorption. At f = 0.5 the absorption is 0.32 for 5 nm NbN and 0.40 for 7 nm [team calc]. Pick one measured thickness (ellipsometry on witness W1-a) and use it in every script.

## Refraction and a 0.5 fill factor discard about 40 % of the catchable light

### The σ-dipole collection model overstates Ba⁺ collection by ≈1.45×

`trapcalc.collection_fraction(..., "sigma")` weights directions by 3/(16π)(1 + cos²θ). That is a σ dipole rotating in the surface plane, with the quantisation axis normal to the chip. `sim/06` calls it with "sigma", which gives the 3.25 % (A30) and 5.92 % (B60) quoted in `DESIGN_LOG.md` step 7 and in `design/CLAUDE.md`.

The collection notes derive that ¹³⁸Ba⁺ 493 nm emission is **isotropic** [team calc, no opened source]. The derivation:

1. A P₁/₂ state m′ = +½ decays by π (branching 1/3, pattern (3/8π) sin²θ) and by σ (2/3, pattern (3/16π)(1 + cos²θ)).
2. The two sum to 1/(4π).
3. Any J = ½ state is a spin pointing in some direction, so the result holds for any population, coherence or B-field direction.
4. The linear Stokes parameters vanish, so a linear grating absorbs the unpolarised average of its two polarisation channels.

A supporting argument [inference]: the total far-field intensity depends only on the excited-state density matrix summed over final ground states. Laser-driven coherences between S and P (the coherent part of the scattered light) therefore do not change the angular distribution of the total.

Redone isotropically at the same aperture heights (ion height plus 6 µm of Au, from `sim/06`), the fractions are **2.22 % (A30) and 4.15 % (B60)** [team calc, reproduced in this session]. **Check this against an atomic-physics text** (angular distribution of dipole radiation summed over final Zeeman sublevels) before the numbers in `DESIGN_LOG.md` and `design/CLAUDE.md` are replaced. Two consequences follow if it holds:

- Wire orientation is not an optical lever for Ba⁺. It can be chosen for RF and current-crowding reasons alone.
- Spiral and fractal layouts would equalise the two polarisation channels but would not raise their average.

### A window-sized meander misses the refracted rim

The limiting aperture is the bottom of the 6 µm Au window. A ray that passes the bottom edge heading outward travels another 10 µm through SiO₂ (n = 1.463) before reaching the NbN. At the A30 corner the ray is at 21° in vacuum and 14° in SiO₂, so it lands **2.5 µm** outside the window projection. At the B60 corner (31.7° → 21°) it lands **3.9 µm** outside.

Ray tracing every aperture point to the NbN plane for an isotropic emitter (geometric optics; the Fresnel number of the 30 µm window over 10 µm is ≈70) [team calc, this session]:

| Meander extent beyond the window (axial, radial per side) | A30: fraction of window photons landing on NbN | B60 |
|---|---|---|
| 0, 0 (v3 as drawn) | **80.5 %** | **82.2 %** |
| +4 µm, 0 | 89.7 % | 89.8 % |
| +4 µm, +1 µm | 95.4 % | 95.4 % |
| +2 µm, +2 µm | 100 % | 96.4 % |
| +4 µm, +2 µm | 100 % | 100 % |

The axial overhang is free. It lies along the axis under the continuing centre-DC Au and does not move any NbN toward an RF rail. The radial overhang is not free: it moves the outermost lines from |y| = 15 µm to 16–17 µm, closer to the centre-DC edge at |y| = 20 µm and its 5 µm gap to the RF rail. That trade is taken up under RF below. Pushing the meander outward has one more benefit [inference]. The outermost few lines, which proximity-effect dosing makes narrower (`fab/mask_list.md`, "Proximity"), and the turnarounds would then sit where no photons land, although they stay electrically in series.

### Fill factor is the biggest optical lever, and it hits the weak polarisation channel

In the v3 stack the absorption is limited by the E-perpendicular (TM) channel, not by the cavity. Effective-medium transfer-matrix results [team calc]:

| NbN t | f | TE (E ∥ wires) | TM (E ⊥ wires) | Unpolarised |
|---|---|---|---|---|
| 7 nm | 0.4 | 0.53 | 0.12 | 0.32 |
| 7 nm | 0.5 | 0.61 | 0.20 | **0.40** |
| 7 nm | 0.6 | 0.67 | 0.31 | 0.49 |
| 7 nm | 0.7 | 0.72 | 0.46 | **0.59** |
| 7 nm | 0.8 | 0.77 | 0.65 | 0.71 |
| 5 nm | 0.5 | 0.49 | 0.15 | 0.32 |

Other parts of the stack matter much less [team calc]:

- Re-optimising the spacer (190–280 nm) and cap (20–300 nm) changes these by ≤ 0.01. The present 238 nm spacer is already at the optimum.
- Averaging over the real emission cone costs ≤ 0.01 (A30) because the four polarisation and plane channels stay within ±0.05 up to 32°.

The polarisation contrast is a known meander property. Anant et al. measured 21 % versus 10 % absorption for the two polarisations in 200 nm-pitch, f = 0.5 NbN at 1550 nm. They showed that the E-parallel absorption depends only on fill factor, while the E-perpendicular absorption falls as pitch shrinks at fixed fill ([Anant et al., arXiv:0806.3194, Figs. 1(c,d), 4](https://arxiv.org/abs/0806.3194)). By that result the zero-pitch effective-medium model probably *underestimates* the E-perpendicular channel at 200 nm pitch [inference]. RCWA would settle the sign.

Trap and UV devices from NIST ran at higher fill than v3:

- Todaro: 110 nm on 170 nm, f ≈ 0.65 ([Todaro Supp.](https://arxiv.org/abs/2008.00065)).
- Wollman: 110 nm MoSi on a pitch "below 200 nm" to stay out of diffraction, with 76 ± 4 % system detection efficiency at UV wavelengths ([Wollman et al., arXiv:1708.04231, Sec. 2, Fig. 1(c)](https://arxiv.org/abs/1708.04231)).

The pitch has an upper limit [team calc]. No diffracted order propagates in the SiO₂ above the wires while Λ < λ / (n(1 + sin θ_int)). At 493 nm that is 337 nm at normal incidence and ≈247 nm at the B60 corner ray. The 200 nm pitch is safe, and any widening of the wire should happen at fixed pitch.

### Collection budget

[team calc; internal detection efficiency (IDE) = 1; absorption cone-averaged; recommended f = 0.65 interpolated between the f = 0.6 and 0.7 cone averages]

| Term | A30 v3 | A30 recommended | B60 v3 | B60 recommended |
|---|---|---|---|---|
| Geometric, σ-dipole model (as logged) | 3.25 % | – | 5.92 % | – |
| Geometric, isotropic | 2.22 % | 2.22 % | 4.15 % | 4.15 % |
| Lands on NbN after refraction | 80.5 % | 100 % | 82.2 % | 100 % |
| NbN absorption, 7 nm | 0.40 | ≈0.54 | 0.40 | ≈0.54 |
| **Product** | **0.71 %** | **≈1.20 %** | **1.37 %** | **≈2.24 %** |

For scale, Todaro's device reached ≈2.0 % geometric × 48 % system detection efficiency ≈ 1.0 % with RF on ([Todaro PRL pp. 2–3](https://arxiv.org/abs/2008.00065)). Trap-integrated detectors lost efficiency to RF more than to optics: Todaro went from a 72 % design to 48 % measured, and Slichter lost 9 % with "typical RF trapping fields" ([Slichter et al., arXiv:1611.09949, abstract](https://arxiv.org/abs/1611.09949)). The recommended geometry is worth the most if the RF items below are also handled.

## Sharp hairpins cap the switching current at 0.54–0.65 of a straight wire

### What Clem & Berggren predict for this exact geometry

Clem and Berggren's London-model criterion sets I_c where the vortex-entry barrier at the inner edge of a bend vanishes. For a rectangular 180° turn, a slot of width 2h cut into a film of total width 2a with arm width W = a − h, their Eq. (100) gives R = I_c,turn / I_c,straight = (3/2)(π α ξ / 2W)^(1/3), with α = √(1 − (W/a)²) ([Clem & Berggren, PRB 84, 174510 (2011), Sec. VII.5, Fig. 11, Eq. 100](https://ar5iv.labs.arxiv.org/html/1109.4881)).

For the v3 geometry (W = 100 nm, 2h = 100 nm, a = 150 nm, α = 0.745) this gives **R = 0.54, 0.58 and 0.65 for ξ = 4, 5 and 7 nm** [team calc, reproduced in this session]. A cross-check with their fill-factor form, Eq. (175), says the neighbouring line costs only ≈9 % on top of the isolated sharp hairpin at f = 0.5.

Two corrections pull in opposite directions [inference]. First, the v3 drawing may be *worse* than Eq. (100), an extrapolation that C&B do not compute: Fig. 11 continues as a full-width film beyond the slot end, while v3 ends in a 100 nm bar (W′ = W), and in C&B's rounded-turn calculation the narrow end bar is worse than the wide one (Fig. 9, solid versus dashed curves). Second, ξ(T) at the ~5 K operating point is larger than ξ(0) ≈ 5 nm, and because R scales as ξ^(1/3) that pushes R up somewhat.

**Caveat on the source.** The paper was read through ar5iv with a summarising tool. Equation numbers and values were consistent across three reads, but figure values were not seen directly. Which panel of Fig. 8 has W′ = W and which W′ = ∞ is unconfirmed [verify].

### Experiments are milder than the theory, but confirm it

Measured suppression is consistently weaker than the London prediction:

| Study | Sample | Measured | Predicted |
|---|---|---|---|
| [Hortensius et al., arXiv:1203.4253, Figs. 3–4](https://arxiv.org/abs/1203.4253) | 8 nm NbTiN, 1 µm wires, 4.2 K; sharp 90° corner (actual inner radius ≈60 nm) | R ≈ 0.51; optimally rounded corners indistinguishable from straight wires | 0.33 |
| [Henrich et al., PRB 86, 144504, Figs. 1–4](https://ar5iv.labs.arxiv.org/html/1204.0616) | 10.4 nm NbN, 250–300 nm wires | two sharp 90° bends gave ≈60 % of the straight-wire j_c at 4.2 K; bent/straight ≈0.65 at 0.3 Tc | below 0.5 |

Henrich et al. attribute the gap to film inhomogeneities that already limit the straight wire, which reached only ≈55 % of depairing.

Two related results add to this. Akhlaghi et al. found, in 100 nm NbTiN, that optimal bends cut dark counts "by orders of magnitude" at equal bias and efficiency. At 100 nm spacing, where no optimal shape fits, circular rounding still improved I_c "by a considerable factor". They also note that a meander's many turns in series make "at least one very sharp bend" likely ([Akhlaghi et al., arXiv:1205.4290, Figs. 2–3](https://arxiv.org/pdf/1205.4290)). The Hortensius stub result bears on the v3 tab junction: a sudden widening measured R ≈ 0.64 against 0.46 predicted, so **the two 100 nm → 3.1 µm tab junctions are crowding points of the same order as the hairpins**. C&B Sec. X.2 gives the crowding-free taper, which follows the S = −K_I W/4 streamline.

A realistic expectation for v3 is therefore R somewhere between 0.54–0.65 and roughly 0.7–0.8 [inference]. Both the Hortensius and Henrich samples were wider (larger W/ξ) than 100 nm, so neither is a direct test at this width.

### Why the 2W turnaround and a 0.6–0.7 fill factor cannot coexist in an interleaved meander

C&B's optimal 180° turnaround (Eqs. 58–59, Fig. 10) reaches R = 1, but only with a gap of 2W between the arms, which is f = 1/3. The paper says that raising f above 1/3 "must come at the expense of the critical current" (Sec. XIV). The notes proposed keeping f = 0.5 in the straight lines and flaring the gap to 2W only near each turn.

That flare does not fit in a meander [team calc, geometry]. At a given end of the meander the hairpin pairs repeat every 2p in y. A pair has two arms (2W), an inner gap g_t, and a clearance s to the next pair, so 2W + g_t + s = 2p, which gives g_t = 2g − s with g = p − W. Reaching g_t = 2W needs g ≥ W + s/2. With a 50 nm minimum clearance, that means f ≤ 0.44 even before any rounding. At f = 0.5 the flared arms of neighbouring pairs collide. At f = 0.65 the attainable turn gap is at most ≈70 nm.

Staggering alternate pairs in x frees room only for every second pair. Fanning the lines out to a larger pitch near the ends needs about 45 µm of radial width for 150 lines at a 300 nm pitch. The centre DC electrode is only 40 µm wide, and NbN outside it would sit next to an RF rail.

So R = 1 is not available at any fill factor that absorbs well. The useful question becomes how to maximise the *absolute* turn-limited current at high f, and where to put the turns. Three observations answer it:

- **The end region is free in x.** The solid block joining the two arms can be made long (a W′ of several hundred nm or more) without using any y space. That turns the v3 narrow-end-bar shape into C&B's Fig. 11 geometry, for which Eq. (100) applies.
- **The slot end can be rounded.** A semicircle of diameter equal to the gap moves the result toward C&B's rounded-turn curves (Sec. VII.4, Figs. 8–9). At f = 0.5 the two rounded shapes shown give R = 0.60 and 0.71. The f = 0.65 value must be read off Fig. 9 [verify].
- **The turns can sit outside the illuminated footprint**, so the local geometry at the turn costs no absorption.

### Width beats fill factor for the turn-limited current

[team calc, this session; sharp-slot R from Eq. 100 at ξ = 5 nm, a lower bound for the rounded version; "W × R" is the turn-limited device current relative to v3]

| Wire / pitch (nm) | f | Gap | Sharp R (ξ 4 / 5 / 7 nm) | W × R vs v3 | Absorption (7 nm) |
|---|---|---|---|---|---|
| 100 / 200 (v3) | 0.50 | 100 | 0.54 / 0.58 / 0.65 | 1.00 | 0.40 |
| 120 / 200 | 0.60 | 80 | 0.49 / 0.53 / 0.59 | 1.09 | 0.49 |
| **130 / 200** | **0.65** | **70** | **0.46 / 0.50 / 0.56** | **1.12** | **≈0.54** |
| 140 / 200 | 0.70 | 60 | 0.44 / 0.48 / 0.53 | 1.14 | 0.59 |
| 100 / 150 | 0.67 | 50 | 0.50 / 0.54 / 0.61 | 0.93 | ≈0.56 |
| 300 / 600 | 0.50 | 300 | 0.37 / 0.40 / 0.45 | 2.08 | outside effective-medium validity (diffractive) |

Raising f by widening the wire at a fixed 200 nm pitch *raises* the absolute turn-limited current, even though R itself falls. Raising f by shrinking the pitch lowers it, and also adds 1.4× the wire length and a 50 nm gap.

The fractional bias reachable in the absorbing straight sections, R, stays near the v3 value. That is the real open risk, and it is the same risk v3 already carries: whether 493 nm photons are detected with saturated internal efficiency at I_b ≈ 0.5–0.7 of the straight-wire I_c (next section).

## Width, not pitch, is the lever that serves absorption, crowding and RF together

### Saturation at 493 nm: plausible to ~180 nm, unmeasured for this film

**Lusche et al.** measured NbN meanders 85–178 nm wide, 3.6–4.8 nm thick, with Tc 8.5–10.2 K, on 250 nm SiO₂ ([Lusche et al., arXiv:1303.4546, Table I, Figs. 3 and 5](https://arxiv.org/abs/1303.4546)):

- a short-wavelength plateau in the spectra, biased at 0.5–0.7 of the depairing current;
- a near-IR cut-off whose inverse scales linearly with width;
- the statement that "with increasing wire thickness the cut-off wavelength decreases".

**Korneeva et al.**: 0.53–5.15 µm NbN bridges detect single 408 nm photons ([Korneeva et al., arXiv:1802.02881, Sec. IV, Figs. 6–7](https://arxiv.org/abs/1802.02881)):

- They "do not observe a saturation" of internal efficiency.
- The widest bridge lost the deterministic regime at 4.2 K.

**Wollman et al.** call 110 nm × 10 nm MoSi "the largest" cross-section that still saturated at 370 nm ([Wollman, Fig. 2, Fig. 4a](https://arxiv.org/abs/1708.04231)). That is a different material.

Taken together [inference]: a 493 nm photon (2.5 eV) carries ≈3× the energy of a 1550 nm photon, which favours detection in wider wires. The 7 nm film thickness pushes the other way, and the ~5 K cryostat (T/Tc ≈ 0.64 for Tc 7.8 K) is warmer than any of these measurements.

**Risk ranking for a trap-die wire** [inference]:

| Width | Risk |
|---|---|
| 130–140 nm | moderate, testable |
| 300 nm | unknown at 493 nm and 5 K |
| 1–3 µm microstrips | high |

The microstrip case: the NbN result that does saturate in the visible needed 0.85 K, a 2–6 Ω cold shunt against latching, and accepted fill 0.33 ([Xu et al., arXiv:2304.06921, Secs. 2–5](https://arxiv.org/pdf/2304.06921)).

### What Suleimen et al. 2026 does and does not settle

Suleimen et al., "Mitigation of rf-induced critical-current shifts in NbN superconducting nanowire single-photon detectors for trapped-ion readout", Phys. Rev. Applied 25, 044091 (2026), is the only paper that compares NbN width for RF tolerance in an ion-trap setting. **Only the abstract page was readable.** The full text is paywalled and no arXiv version was found. The abstract (paraphrased) reports three things ([APS abstract page](https://journals.aps.org/prapplied/abstract/10.1103/771x-57wg)):

- an optically transparent, conducting ITO shield;
- a **300 nm-wide NbN nanowire that keeps a higher relative critical current under stronger RF than a 100 nm-wide one**;
- phase-coherent active cancellation that recovers **92 % of the unperturbed I_c at 2π × 25 MHz**.

The group works with ⁴⁰Ca⁺ (397 nm), and their efficiency tests in the precursor paper were at 729 nm. So the abstract says nothing about saturation at 493 nm.

A plausible mechanism [inference, not from the text]: at fixed fill and area the displacement current per area is unchanged, while I_c scales with width, so I_rf / I_sw falls.

A 300 nm wire at f = 0.5 has three costs [team calc]:

- the pitch (600 nm) is well past the 247–337 nm diffraction bound, so the absorption model no longer applies;
- the sharp-turn R drops to ≈0.40;
- L falls about 9×, to ≈0.4 µH at 70 pH/sq, a ≈7 ns reset into 50 Ω.

The latching margin from that L is still positive. Kerman et al. ran ≈50 nH at 50 Ω without latching on sapphire ([Kerman et al., PRB 79, 100509, arXiv:0812.0290, Figs. 1–3](https://arxiv.org/pdf/0812.0290)). SiO₂ is a poorer phonon sink than sapphire, which narrows the margin [inference].

**Recommendation:** obtain the paper through MIT library access, read the width-comparison figures in Results and Discussion, and put a 300 nm meander on the test die. Do not put it on the trap die yet.

### Fabrication cost of the recommended change is one EBL layer

The recommendation stays inside the existing process: HSQ negative tone, CF₄ etch, an SiO₂ cap right after the etch (`fab/TRAVELER.md` steps 5–8). What changes:

- The line/space target in `fab/mask_list.md` goes from 100/100 ±10 nm to 130/70 nm. A 60 nm gap is the demonstrated trap precedent (Todaro, 110/170).
- High fill factor has a measured cost. Yang et al. saw I_c suppressed 35 % at 88 % fill relative to 40 %, more than linewidth error could explain. Their best detection efficiency came at 60 % fill ([Yang et al., IEEE TAS 19, 318 (2009), Fig. 4b](https://qnn-rle.mit.edu/documents/yang-6-2009-60.pdf)). The f = 0.65 point should sit near the benign end of that trend [inference]. Read Yang Fig. 4b for the value at 0.6–0.7.
- Write time is trivial: ≈9 nC for the v3 A30 wire area at ≈2 mC/cm² (≈9 s at 1 nA), and about twice that for the recommended area [team calc]. The meander still fits one EBL field.
- Curved slot ends become many small trapezoids, which is routine at this scale. The written radius will not match the drawn one. Akhlaghi saw an uncontrolled minimum of ≈35 nm, which is about half of the 70 nm gap anyway.

**The real fabrication cost is yield.** Kerman et al. found that 10 × 10 µm NbN meanders had lower average constriction factors than 3 × 3.3 µm ones, "qualitatively consistent with some fixed area density of constrictions". They expected the yield of high-efficiency devices of 10 × 10 µm or larger to be "quite low" ([Kerman et al., APL 90, 101110, arXiv:physics/0611260, Fig. 3c,d](https://arxiv.org/abs/physics/0611260)).

| Device | Wire length | NbN wire area |
|---|---|---|
| Kerman 10 × 10 µm | ≈0.5 mm | – |
| v3 A30 | 4.5 mm (≈9× Kerman) | 450 µm² |
| Recommended A30 (170 lines × 36 µm × 130 nm) | 6.1 mm | ≈800 µm² |

The square count barely changes: 45,000 → 47,000 for A30 and 90,000 → 90,000 for B60 [team calc]. But the wire *area* grows ×1.8. Under an area-density model, more A30s fail.

The run plan already carries the mitigation: two A30 and two B60 meanders in `run_R1_FULL`, two-point room-temperature resistance, then cold I_c × R_n screening, which Kerman shows is independent of cross-section. If yield proves limiting, the axial overhang can shrink to the minimum that keeps the turns outside the footprint (≈2.5 µm A30, ≈4 µm B60).

### Alternatives considered and set aside for this run

| Option | Why set aside [inference] |
|---|---|
| **Spiral** (Henrich et al. 2012) | Henrich reported a spiral "less susceptible to the critical current reduction in sharp turns", with ≈1.5× the meander efficiency at 100 nm width in the optical range ([Henrich et al., arXiv:1210.3988](https://arxiv.org/abs/1210.3988), **abstract only**). A spiral removes all but one central S-turn and is the natural second-run option. But for a square 30 µm window it needs rounded-square loops whose inner corners have radius comparable to W, the S-turn sits in the brightest part of the footprint, and its polarisation benefit does nothing for Ba⁺. |
| **Fractal layouts** | They mainly buy polarisation independence. Arced turns restore the normalised switching current only to ≈0.81, versus 0.82 for a meander ([Meng et al., arXiv:2012.06730, Fig. 1d–e](https://arxiv.org/abs/2012.06730)). |
| **Micron-wide NbN strips** | They would make lithography easy, but they need sub-1 K operation and a cold shunt (Xu 2023), and Korneeva saw no saturation at 4.2 K. |
| **SNAPs and parallel arrays** | They add lithography and series elements for benefits (signal amplitude, photon-number resolution) that a single ion-fluorescence pixel does not need (`layout_and_fab.md` Q2; the Marsili SNAP papers were seen only as search excerpts). |

## RF headroom depends more on grounding than on the meander

### The 1.4 µA bound is ≈16 % of a realistic 5 K switching current, not 7–9 %

`sim/10` case f is the v3 configuration: Al mirror only, 10 µm SiO₂ kept over the window, no ITO, 7 nm NbN. It gives C_RN = 0.152 fF and a peak induced current of **1.42 µA at 53 V, 28 MHz** (`DESIGN_LOG.md` step 17). This is an upper bound from a 2-D cross-section that assumes all the current leaves through one end. With both ends low-impedance compared with the meander's ωL (≈580–830 Ω at 28 MHz for 3.3–4.7 µH), the in-wire peak is roughly half, about 0.7 µA. That follows Todaro's distributed model and Slichter's symmetric-termination remark [inference] ([Todaro Supp. Fig. S4, Eq. S1](https://arxiv.org/abs/2008.00065); [Slichter App. A](https://arxiv.org/abs/1611.09949)).

**The switching-current figure the bound is compared against is optimistic.** `DESIGN_LOG.md` uses 15–20 µA, scaled from Najafi et al.'s heated-NbN wires (Tc ≈ 10.9 K, measured near 2.5 K) ([Najafi et al., Nat. Commun. 6, 5873, Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4354051)). The room-temperature, bias-sputtered NbN compatible with Al has Tc ≈ 7.8 K, and the cryostat runs at ~5 K (`DESIGN_LOG.md` step 0).

Sedykh et al.'s 100 nm, 5–7 nm NbN device (Tc 7.5 K) gave ≈15 µA at 2.2 K ([Sedykh et al., Zh. Tekh. Fiz. 95(9), 1673 (2025), Fig. 3, p. 1676](https://www.mathnet.ru/php/getFT.phtml?jrnid=jtf&paperid=8303&what=fullt&option_lang=eng)). Scaling it with (1 − (T/Tc)²)^(3/2) to 5 K gives **≈8–9 µA** [team calc, rough]. The 2-D bound is then ≈16 % of I_sw, or ≈8 % with symmetric drain.

Compare the two NIST devices:

- **Hampel**, grounded mirror at 4.5 K: the plateau starts about 10 µA below a 61 µA I_sw, roughly 16 %, and the full count-rate plateau survived to 44 V [team reading of the published plot] ([Hampel arXiv Fig. 3(b)](https://arxiv.org/abs/2302.01462)).
- **Todaro**, MoSi: induced currents of 3.5 µA (spatially varying) plus 0.9 µA (uniform) ate half of an 8.9 µA I_sw, and efficiency fell from ≈65 % to 48 %.

**What matters for NbN at 493 nm is the width of the plateau at the operating temperature, more than the absolute I_sw.** Measure I_sw(T) from 2 to 6 K on the T3 bar and the T4 / T4b spare meanders before trusting any of these ratios.

**By the V·f metric the drive is inside the demonstrated envelope.** Sedykh's 3 dB amplitude × frequency is constant within ±7 % over 5–25 MHz, which is the signature of capacitive pickup [team calc from the Sedykh 2025 table, p. 1678]. On that metric [team calc]:

| Drive | V·f |
|---|---|
| Todaro, 8.8 V × 67 MHz | 590 V·MHz |
| **This project, 53 V × 28 MHz** | **1484 V·MHz** |
| Hampel maximum, 54 V × 70 MHz | 3780 V·MHz |

The coupling geometry differs from Hampel's, so this is necessary but not sufficient.

### Ground the centre DC electrode at RF, or nothing else matters

Two pieces of the design assume the centre DC electrode is at RF ground:

- `sim/10` sets every DC electrode to RF ground "through their filter capacitors".
- The SNSPD leads are routed under that electrode for safety (`DESIGN_LOG.md` step 8).

But the filter capacitors are still open: step 21 lists "DC-to-RF coupling capacitances (field solve) to decide on filter capacitors" as unresolved.

Each lead is 4 µm × ≈4.7 mm under the centre DC electrode and its lead, through 10 µm of SiO₂. That is ≈65 fF per lead, or **≈11 µA of displacement current per volt of RF on the centre DC electrode** at 28 MHz [team calc, parallel plate, ε_r 3.9]. The two leads are matched, so this current is mostly common-mode and drains to the terminations. Only the fraction set by 50 Ω / ωL (≈6–9 %) crosses the meander. Any RF on the centre DC electrode would also sit on the Au rim around the window, a few µm from the outermost lines, which `sim/10` does not model.

An estimate from the notes [team calc, order of magnitude]: 53 V × ~0.5 pF of rail-to-centre coupling into a 1 nF filter gives ≈26 mV, or ≈0.3 µA of common-mode lead current. That is harmless. Without a nearby filter capacitor, the centre DC electrode would sit at a sizeable fraction of the RF amplitude, and the lead coupling would exceed I_sw.

**Recommendations:** compute the rail-to-centre-DC capacitance with the field solve already on the open list, put an nF-class capacitor to ground on the centre DC line at the carrier, and rerun `sim/10` with the centre DC electrode at a small RF fraction (for example 1 %) to bound the sensitivity.

### The Al plane is now tied on chip; check its RF potential under the leads

Hampel's floating mirror was the failure case. It lost the count-rate plateau by 44 V, while the same mirror grounded kept it, and a large grounded mirror under the leads beat a small one at 54 V (≈36 versus ≈14 µA I_sw) [team reading] ([Hampel arXiv Fig. 3(a–c)](https://arxiv.org/abs/2302.01462); [Hampel SPIE 13025, Fig. 1](https://tf.nist.gov/general/pdf/3290.pdf)). The v3 plane covers the whole die apart from a 150 µm edge band and cut-outs under the SNSPD pads and marks, so it is the "large mirror" case.

Since DESIGN_LOG step 22 the plane is tied to the Au fill through eight on-chip layer-40 vias, with the four Al bond openings as a backup. Two quantities are still unbudgeted:

- **Distance and return current.** The nearest via to the readout zone at (300, 0) µm is at (1000, ±2500) µm, about 2.6 mm away. The rail-to-Al capacitance (≈2.9 pF, step 22) returns about ωCV ≈ 27 mA through the 150 nm Al-1%Cu sheet [team calc].
- **Lead-to-Al coupling.** The SNSPD leads ride 238 nm above that sheet for ≈4.7 mm, which is **≈2.7 pF per lead**, or ≈0.5 µA per mV of RF potential between the Al under the leads and the SNSPD return bond [team calc].

The few-mV ground bounce the notes estimate for 1 nH of bond inductance would therefore put a few µA of common-mode current on the leads. That is not in the 2-D model, which treats the Al as ideal.

**Recommendations** [inference]:

- Estimate the Al plane's RF potential along the lead path (sheet resistance at 5 K times the return current density, plus the via and bond inductance).
- Bond the SNSPD return pad to the same carrier ground point as the nearest GND and M1 bonds, with short wires.
- Keep test a13 as a gate.

An on-chip tie from the return lead to the Al would need an opening through the spacer before layer 22, which is the retired layer-24 step, so a bond-level fix is the cheaper first move.

### Geometry levers that remain, in order

**The radial overhang is the one trade between optics and RF that has no number on the RF side.** Field lines leaking through the 5 µm centre-DC-to-rail gap into the Au–Al sandwich decay inward roughly as exp(−π x / t), with t ≈ 10 µm under the rim [inference]. Over the 3–4 µm between the centre-DC edge and an overhung line at |y| = 16–17 µm, that is not a strong suppression. Rerun `sim/10` case f with the wire region extended to |y| ≤ 15, 16 and 17 µm, and pick the largest overhang that keeps C_RN within ~10–20 % of the present value:

- +2 µm recovers the last 4.6 % of photons (A30);
- +1 µm already recovers 95.4 % (A30).

The same rerun should include f = 0.65, since more NbN coverage may intercept more charge.

**The remaining levers:**

1. Hairpins and tabs: rounded slot ends and long end blocks for the hairpins, tapered tab junctions. These move the switching point and dark counts away from defects (Akhlaghi).
2. Width: 130 nm raises the turn-limited current ≈1.1× even before rounding (table above).
3. Readout filtering, regardless of the above: a notch at f_rf plus a low-pass, as both NIST devices needed ([Hampel SPIE Sec. 4](https://tf.nist.gov/general/pdf/3290.pdf); [Todaro Supp. Fig. S2](https://arxiv.org/abs/2008.00065)).
4. Second-run options with no trap precedent: a grounded centre tap, which would roughly halve the in-wire peak again [inference from the distributed model], and active cancellation (Suleimen, abstract only).

## A one-mask change plus a test die that settles the unknowns

### Recommended trap-die geometry

[inference; all values to be confirmed by the test die and the reruns named]

| Parameter | v3 now | Recommended |
|---|---|---|
| NbN | 7 nm (traveler) | 7 nm, measured, used in every model (`sim/06`, `09b`, `10`) |
| Wire / pitch | 100 / 200 nm, f 0.50 | **130 / 200 nm, f ≈ 0.65** (70 nm gaps) |
| Orientation | lines along the trap axis | unchanged |
| Line length | = window (30 / 60 µm) | window + 2 × 3 µm (A30: 36 µm); window + 2 × 4.5 µm (B60: 69 µm) |
| Radial extent | 30 µm (150 lines) | 32–34 µm (160–170 lines), set by the `sim/10` overhang rerun |
| Turnarounds | 100 nm straight bar, square inner and outer corners, at the window edge | slot end rounded (diameter = gap); solid end block 2W + g tall and ≥ ~0.5 µm long; all outside the optical footprint, under the Au |
| Tab junctions | abrupt 100 nm → 3.1 µm with a re-entrant corner | C&B Sec. X.2 streamline taper |
| L, τ at 70 pH/sq | 3.2 µH, 63 ns (A30) | ≈3.3 µH, 66 ns (A30); ≈6.3 µH, 126 ns (B60), far from latching |
| Leads | 4 µm Ti/Au under the centre DC electrode, single-ended | unchanged geometry, plus a centre-DC filter capacitor and short common return bonding |

All of this is a change to `WIRE_W`, `DET_WX` / `DET_WY` relative to `WIN_WX` / `WIN_WY`, and the `meander()` polygon code in `make_chip.py`. `check_chip.py` and the tab-to-lead overlap rules (20 µm in `mask_list.md`) should be rechecked after the edit.

**Test-die matrix.** Add a geometry array next to the T8 dose array. A ±20 % dose step moves linewidth by far less than 100 → 130 nm [inference], so the dose array alone cannot answer the width question. Use paired devices a few µm apart, compared as ratios, as Akhlaghi did:

| Group | Devices |
|---|---|
| Meanders | 100/200 sharp (v3 control), 100/200 rounded with end block, 130/200 rounded, 140/200 rounded, and 300/600 rounded (the Suleimen comparison) |
| Straight wires | one at each width, as I_c references |
| Length series | two or three lengths at 130 nm, to measure I_c versus length on this film |

**Measurements, in order:**

1. Room-temperature resistance.
2. I_c × R_n against the straight references (Kerman 2007).
3. I_sw(T) from 2 to 6 K.
4. Dark count rate versus bias.
5. Detection efficiency versus bias at or near 493 nm.

The third and fifth results decide the two questions this report cannot settle from the literature: whether ≈0.5–0.7 I_c,straight sits on the 493 nm plateau at 5 K, and how much headroom remains against ≈0.7–1.4 µA of pickup.

### Where to read

| Source | Read |
|---|---|
| Suleimen et al. 2026 ([APS](https://journals.aps.org/prapplied/abstract/10.1103/771x-57wg), **abstract only so far**) | Experimental Methods (wire geometry, ITO stack, how the RF is applied); Results and Discussion (the 100 versus 300 nm I_c-versus-RF figures and the cancellation figure); Appendices (field simulations). Check whether an actual trap or a model electrode was used. |
| Clem & Berggren 2011 ([ar5iv](https://ar5iv.labs.arxiv.org/html/1109.4881)) | Secs. III–IV (criterion, Eqs. 12–15); Sec. VII.2 with Figs. 6a and 10 (optimal turn, Eqs. 58–59); Sec. VII.4 with Figs. 8–9 (R versus f for rounded turns: read the f = 0.65 value and which curve is W′ = W); Sec. VII.5 with Fig. 11 (Eqs. 96–101); Sec. X.2 (tab taper); Sec. XII (dark counts); Sec. XIII (Eqs. 175–176). |
| Hortensius 2012; Henrich 2012 | Hortensius Figs. 3–4 (I_c histograms; the corner as the defined weak link). Henrich Figs. 2–4 (rounded-bend recovery; temperature dependence). |
| Akhlaghi 2012 | Fig. 2 (I_c ratios for sharp, rounded and optimal pairs, not given in the text); Fig. 3 (dark counts at equal bias). |
| Yang 2009 | Fig. 4b (I_c versus fill factor at 90 nm width). |
| Anant 2008; Wollman 2017 | Anant Figs. 1(c,d) and 4 (polarisation and pitch); Wollman Sec. 2, Fig. 1(c), Table 1. |
| Lusche 2013; Korneeva 2018 | Lusche Table I, Figs. 3 and 5 (read the cut-off wavelength versus 1/w); Korneeva Figs. 6–7. |
| Hampel 2023 ([arXiv](https://arxiv.org/abs/2302.01462), [SPIE](https://tf.nist.gov/general/pdf/3290.pdf)) | arXiv Fig. 2(b) against this stack; Fig. 3(a–c) (floating versus grounded, small versus large mirror); Fig. 4 with p. 4 (induced current versus heating); SPIE Fig. 1 (lead and mirror routing), Sec. 4 (filtering). |
| Kerman 2007, 2009 | 2007 Figs. 2–3 (I_c × R_n screening; area dependence). 2009 Figs. 1–3 (latching boundary versus L and R_L). |

## Conclusion

The audit changes where the effort should go. The meander's own geometry is not the main efficiency loss. Two drawing choices are:

- making the NbN exactly window-sized, which ignores refraction in 10 µm of SiO₂;
- copying the 1550 nm-style 0.5 fill factor, which starves the E-perpendicular channel.

Both are fixed by extending and widening the wires. Once the turnarounds move outside the illuminated footprint, the fill-factor-versus-crowding conflict stops being a conflict about light. It becomes a question about bias: whether 493 nm photons are detected in 130 nm, 7 nm NbN at ≈0.5–0.7 of the straight-wire I_c at 5 K. The current design carries the same open question unacknowledged. The C&B optimal turn cannot be had in any interleaved meander that absorbs well, so the strategy is to maximise W × R, and width at a fixed 200 nm pitch does that.

The audit also moves the RF risk off the nanowire and onto the circuit around it. The geometry already has the literature's most effective feature, a large grounded mirror 238 nm below the wire. The remaining unknowns are all outside layer 20:

- a centre DC electrode whose RF grounding has not been designed;
- an Al sheet whose RF potential couples into 2.7 pF of lead;
- a switching current at 5 K that may be half the logged estimate.

The cheapest path is to settle those with one field solve, one capacitor and one cold measurement, before spending a second EBL iteration on wider wires or spirals. If the team adopts any of these geometry changes, record the choice and the reason in `notes/decisions.md`. The A30/B60 collection numbers in `DESIGN_LOG.md` and `design/CLAUDE.md` should be revisited once the isotropy derivation is checked.
