> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Local mirror without D2

[Variants](../VARIANTS.md) · [Open decisions](../OPEN_DECISIONS.md) · [Baseline](../TRAVELER.md)

> [!warning] Proposed architecture
> **No GDS implementation.** Dimensions below were proposed against the earlier detector. Recheck the mirror outline, tabs and clearance against v3.1. Routing, Au thickness, optics and RF remain open in [Open decisions](../OPEN_DECISIONS.md).

Team request, 2026-11-08 (DESIGN_LOG step 23). This is an **alternative** to the [baseline traveler](../TRAVELER.md), kept here so the two can be compared. The baseline stays the die-wide M1 ground plane under 10 µm D2. Nothing in the GDS implements this variant yet (H.5).

**Idea.** Follow Hampel 2023: the Al sits only under the SNSPD and along its leads, never under the RF rails. The electrodes sit on the thin optical stack. Both options remove 10 µm D2 and its deep gap etch. **E1 removes plating; E2 retains 6 µm plating.** A die-wide Al plane under electrodes on that thin stack would give C_RF–ground ≈ 127 pF instead of 2.9 pF (DESIGN_LOG step 22) [team calc]. That is why the mirror has to be local.

## H.0 Why the baseline has a thick D2: ground plane and mirror together

The Al does two jobs, and each one depends on a different distance:

- **Mirror:** the Al-to-nanowire distance. This is the 238 nm SiO₂ spacer, fixed by the 493 nm cavity phase (DESIGN_LOG steps 9 and 9b).
- **RF ground plane:** the Al-to-electrode distance. The RF Au and the Al form a parallel-plate capacitor, C = ε·A/d. The rail area is fixed (0.877 mm² on A30), so d is the only free parameter. A thicker D2 also raises the RF breakdown voltage.

| Stack | Ground plane under the RF | SNSPD mirror | C_RF–ground; RF current at 53 V, 28 MHz [team calc] | Cost |
|---|---|---|---|---|
| **Baseline: thick D2** (the [baseline traveler](../TRAVELER.md)) | Yes | Yes | 2.9 pF (10.3 µm SiO₂); ≈ 27 mA | 10 µm D2, plating, gap etch. The detector sits under a 6 µm-deep window; the ion drops 1.38 µm (A30) over the window (step 17). The window floor is bare SiO₂ |
| Thin stack, die-wide Al (FabuBlox flow as drawn) | Yes, but too close | Yes | 127 pF (238 nm SiO₂); ≈ 1.2 A | The RF resonator cannot drive it; loss and breakdown in the SiO₂ |
| **Thin stack, local mirror** (this section) | No | Yes | Only the rail-to-Si capacitance, not computed | Needs Si with ρ > 20 kΩ·cm; the RF over that Si is NIST practice (Todaro, Hampel). Exposed SiO₂ in every gap unless the electrodes are plated thick, as Todaro's 6 µm were (H.4, option E2). Simpler process |

The choice is therefore between process complexity and the ground plane. A thick D2 gives both the plane and the mirror; a thin stack keeps the mirror only by removing the Al from under the RF rails. On Si with ρ > 20 kΩ·cm, dropping the plane is what NIST does (Todaro, Hampel). The 10 µm D2 is the standard surface-trap ground-plane stack (Romaszko 2020 Fig. 3.1; JoVE; Stick 2010; Leibrandt 2009; Sterling 2014 with 10 µm of buried SiO₂).

The thickness of the SiO₂ under the electrodes changes the load on the RF drive and the field inside that SiO₂. It does not change the trapping field at the ion, which the electrode widths set.

## H.1 Mirror size

Hampel gives no dimensions. Measured from Hampel Fig. 1 (arXiv v1, p. 2) against its 20 µm and 100 µm scale bars [team calc]. The 20 × 30 µm SNSPD outline measures 20 × 30.5 µm, which checks the scale.

| | Hampel, small mirror | Hampel, large mirror | **This variant (proposal)** |
|---|---|---|---|
| Along the leads | ≈ 64 µm: 13 µm behind the active area, 20 µm forward under the lead start | ≥ 270 µm along the lead channel; runs ≈ 160 µm past the RF-rail ends | Small part: x = 265 … 328 (X_READ = 300; the meander tabs end at x = 245). Large part: continues under the leads to x ≈ −2400, i.e. ≈ 400 µm past the RF open end at x = −2000 |
| Across | 37–49 µm (visible edge to the black RF gaps) | ≈ 35–50 µm | **\|y\| ≤ 20 µm (40 µm)**: under the centre DC only. Our RF rails start at \|y\| = 25, so 50 µm is the hard limit |
| Margin around the detector | 8–15 µm on the long sides | – | **5 µm** on the long sides (detector \|y\| ≤ 15). Narrower than Hampel's because our channel is 50 µm wide |
| Under the RF rails | No | No | No, by construction |
| Ground | CHF₃ vias + 20 nm Au, "via the trap electrodes" | same | Widen the far end (x ≈ −2500 … −2300) to reach under the Au ground fill and put the via there (H.2 step 11v). Exact spot to be checked in the GDS: the fill must enclose it ≥ 25 µm, as in step 22 |

Capacitance the mirror adds to the centre DC (electrode 2), which sits 318 nm above it (spacer + HSQ/cap): 40 µm × ≈ 2.73 mm ≈ **12 pF** [team calc, ε_r 3.9]. That is harmless on a filtered DC line [inference].

## H.2 Steps (changes against the [baseline recipes](../TRAVELER.md#f-steps))

| Step | Baseline | Variant |
|---|---|---|
| 0–2 | Prep, L1 marks, 1 µm thermal SiO₂ (D1) | Same |
| **3v** | L10 inverted: die-wide plane | **L10 drawn: local mirror only**. Al-1%Cu 150 nm (opaque; Hampel used 50 nm e-beam Al). Either the step-3 etch with the job not inverted, or lift-off as Hampel did. No mark cut-outs needed |
| 4–8 | Spacer 238 nm, NbN, L22 leads, L20 nanowire, HSQ + cap | Same order: leads before the nanowire, cap straight after. **The cap is now the top surface over the detector (vacuum above)**, so its thickness matters optically again: rerun 09b before fixing it (H.4) |
| 9, 10 | 10 µm D2 | **Skipped** |
| **11v** | L40 through ≈ 10.4 µm D2 | **L40 through the thin stack only.** Mirror ground via: HSQ/cap + spacer ≈ 0.32 µm down to the Al. SNSPD pads: ≈ 80 nm down to the L22 Au. Thin positive resist (~1.3 µm); same CHF₃/CF₄/Ar chemistry, ≈ 1 min [verify]. Stops on Al and Au. Add a small Al probe opening on the mirror so it can be checked electrically (H.5) |
| **12v–15v** | Seed, nLOF mold, 6 µm plating, seed removal | **Ti/Au lift-off electrodes, L50 drawn**: LOR + positive resist, MLA. In-situ Ar pre-clean before the Ti (AlF₃ on the via floor; step 22). Ti 10 nm / Au 350 nm (Hampel 350 nm) [verify thickness]. Lift-off in NMP. Option E2: keep steps 12–15 as written and plate 6 µm on the thin stack; the cap protects the NbN under the plating resist (Todaro's damage step) [inference] |
| 16a, 16 | L45 protect, gap etch | **Skipped** (no D2 to clear) |
| 17–19 | Test, dice, package | Same, except: no M1 bond openings (the mirror is grounded through the fill); test fill ↔ mirror probe pad < 10 Ω; check that 350 nm evaporated Au wedge-bonds [verify] |

Thermal budget: no D2, so the long 300 °C exposure goes away.

## H.3 Cross-section under the readout window (variant)

HR Si / 1 µm thermal SiO₂ / 150 nm Al (local mirror) / 238 nm PECVD SiO₂ / 7 nm NbN / 80 nm HSQ + PECVD SiO₂ cap / **vacuum**. For E1/A30 the window is a 30 × 30 µm hole in 0.35 µm Au; E2 retains 6 µm Au. The ion sees the cap directly. Away from the detector the electrodes sit on spacer + cap over D1, with no Al under them.

## H.4 What the variant changes in the physics (each needs a rerun or a test)

- **RF over thin SiO₂ on HR Si, with no ground plane.** This is proven NIST practice, not an open risk. Todaro trapped on 6 µm plated Au over 134 nm PECVD SiO₂ on intrinsic Si, ρ > 20 kΩ·cm, with no ground plane, and reached days-long lifetimes and F = 0.9991. Hampel used the same kind of substrate. The ground plane in the baseline comes from the Romaszko/JoVE flow (Romaszko 2020 Sec. 3.2; Leibrandt 2009: Q 100 → 150 with the plane), which guards against substrate loss. **Condition: order Si with ρ > 20 kΩ·cm, as NIST did.** The baseline step 0 asks only for > 10⁴ Ω·cm. Measuring the resonator Q with the die mounted is still worth doing.
- **Exposed SiO₂ in every gap.** 0.35 µm Au over 5 µm gaps gives a depth-to-width ratio of 0.07, against ≥ 1 recommended (Bautista-Salvador 2019). The ion sees SiO₂ along the whole trap, not only at the window. Todaro trapped on the same NIST design with 6 µm electrodes; Hampel's paper reports no trapping. Option E2 (plated 6 µm) raises the ratio to 1.2.
- **Optics (09b).** Rerun with vacuum above the cap instead of 10 µm SiO₂.
- **Ion height and recess (04b, 12).** Set `metal_thickness` to 0.35 (or 6 for E2) and `ground_depth: null` (no buried ground) in the `_sim.json`. The window recess shrinks from 6 µm to 0.35 µm, so the 1.4 µm height drop over the window should shrink as well [inference; rerun 04b].
- **RF pickup (10).** Rerun with a local mirror, no D2, and the rail 5 µm laterally from the mirror edge.

## H.5 GDS changes needed (not made)

A `--localmirror` flag in `make_chip.py` would need:

- L10 = the H.1 mirror shape, not the die-wide plane;
- L40 = the mirror ground via + SNSPD pad openings + a mirror probe opening only (no M1 bond openings, no fill-to-M1 vias);
- no L45;
- `_sim.json` stack per H.4;
- **a lead-routing decision.** The L22 leads now run under the centre DC with only ≈ 80 nm of HSQ/cap between them and the Au, over ≈ 2.3 mm inside the trap and ≈ 2.6 mm under the centre lead. A pinhole anywhere shorts the SNSPD to electrode 2. Either (a) move the leads into the electrode layer, in a slot cut along the centre DC (Hampel's Fig. 1 layout; a GDS change and a new five-wire geometry to simulate), or (b) keep them buried and thicken the SiO₂ over the leads only [inference; adds a step].
- `check_chip.py` rules for the above.
