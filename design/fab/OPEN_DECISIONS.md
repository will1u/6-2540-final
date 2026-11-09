> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Open design decisions and run requirements

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

The first section concerns design choices; the next sections prepare each run. An unchecked item does not reverse an adopted choice. Recipe values tagged **[verify]** remain provisional.

## Design choices

![Map of open design decisions](figures/open_decisions_map.svg)

The two architectures in cross-section: [architecture comparison](figures/architecture_crosssection.svg) (also in [Local mirror H.0](variants/LOCAL_MIRROR.md#h0-why-the-baseline-has-a-thick-d2-ground-plane-and-mirror-together)).

| Decision | Choices | What resolves it | Status |
| --- | --- | --- | --- |
| Electrode Au (v4) | E1: 0.35 µm lift-off (no plating); E2: 6 µm plated (as Todaro) | SiO₂ exposed in every 5 µm gap (E1 depth/width 0.07, E2 1.2), plating effort, resonator tests. Sims 12/13 barely distinguish them (same voltages; window drop −1.19 µm E2 vs ≤ −0.37 µm E1) | **Open.** Blocks the v4 traveler rewrite |
| Readout radial tilt | Keep 10°, smaller tilt, zero tilt, or wider DAC range | v3 needed 13.2 V (A30) / 15.2 V (B60). **v4 needs 6.3 V (A30) / 2.2 V (B60) for 10°** (loading 7.5 V; 480 µm zones) [team calc, steps 25, 27, 28] | Over-range problem gone on v4; team to confirm 10° |
| RF grounding / filters | Centre-DC filtering, carrier grounds, symmetric detector termination or cancellation; for v4 also an RF bypass at both SNSPD lead pads | v4 slot leads each collect ≈ 46 µA (E2) / 29 µA (E1) of common-mode RF over 2.3 mm; only termination asymmetry sends it through the nanowire (step 26). Bond diagram, coupling calculation, RF-on/off tests | **Open; more important on v4** |

**Resolved 2026-11-08** ([decisions](../../notes/decisions.md)): architecture → local mirror, no D2; lead routing → Au leads in a slot along the centre DC; detector allocation → keep A30 and B60 (B60 was dropped, then kept); R1_TRAP → the same no-Al stack.

### Before any v4 run

- [ ] Choose E1 vs E2, then rewrite the traveler, R1_TRAP run sheet, mask list, stack and qualification pages for v4 (they carry a banner). Basis: [Local mirror H.2](variants/LOCAL_MIRROR.md).
- [ ] Rework the test dies for v4. T2 (Au/D2/M1 capacitor) and the D2 probe openings no longer exist; TEST_TRAP must carry no Al for R1_TRAP.
- [x] Mirror ground path: via moved to just past the RF open end (step 28) and **Al 450 nm** (team decision 2026-11-08): swing 6.7–8.8 mV, +0.16–0.21 µA. Still to do: put 450 nm in the v4 traveler, set the strip-resistance acceptance (≈ 5 Ω), add a mirror probe opening, check hillocks on a witness wafer.
- [x] 09c optics (step 26): **set the SiO₂ over the wires (HSQ + cap) to 160 ± 10 nm**: A 0.44 → 0.66 (v3.1: 0.54). The traveler and stack pages still say 80 nm.
- [x] 10b RF pickup (step 26): nanowire 0.96 µA (E2) / 1.92 µA (E1) vs 1.67 µA (v3.1); slot-lead pickup feeds the RF grounding decision above.
- [ ] Rerun 15 (collection at the v4 heights).
- [ ] Transport: hold the centre DC at 0 V while moving and ramp the tilt in at each zone (`12_final_chip_check.py --centre-dc-zero`: 1.67 V per 10 µm step vs 7.96 V with the centre DC free; step 25).
- [ ] Order Si with ρ > 20 kΩ·cm; measure the RF resonator Q with a die mounted.

### Detector documents and generated layouts

> [!warning] Reconcile before R1_FULL exposure export
> Current generators specify v3.1 detectors and T9; the checkpointed sheets described 100 nm wires and no T9. GDS filenames are reused. Passing checks recorded for an earlier revision do not establish that current files match the recipes.

- [ ] Record the generator revision for trap dies, test die and run GDS; verify the generated files match the 130/200 nm rounded-turn geometry.
- [ ] Check detector/test-die geometry, contact connectivity and clearances, including T9. Confirm run maps use the intended dies.
- [ ] Re-measure L20/L22/L40/L45/L50 areas and EBL time/charge for the full-stack run. The [mask list](mask_list.md) already has revised L20/T9 figures; other areas still mix revisions. Confirm all values against the same generated run.
- [ ] Calibrate the 130/70 nm SEM target on W2. Validate the separate T9 screening criteria in electrical test a14.
- [ ] Verify square count, resistance, inductance and reset time against the released GDS. Electrical a7 now has a revised resistance estimate; remaining historical values are not a sign-off for v3.1.
- [x] `sim/15_snspd_geometry.py` and the GDS both use the 32 µm radial extent (DESIGN_LOG step 24: OVH_Y = 1 µm after the sim/10 v3.1 RF scan).
- [ ] Reconcile absorption and RF pickup for the changed fill factor/footprint. Do not carry earlier 0.40 absorption or pickup-to-switching-current ratios forward without checking assumptions.

Sources: [trap generator](../gds/make_chip.py), [test generator](../gds/make_test_die.py), [geometry study](../sim/15_snspd_geometry.py), [geometry audit](../research/reports/SNSPD%20geometry%20audit.md).

## Before R1_TRAP

- [ ] Confirm Au-compatible tools, gold bath/minimum area, holders and training order with MIT.nano.
- [ ] ~~W3: qualify D2 stress/backside compensation and chuck bow limit; calibrate L40 and gap etches.~~ Not needed for v4 (no D2, no gap etch). The A30 L40 cap/spacer etch (~0.32 µm) still needs a short calibration before R1_FULL.
- [ ] Before R1_FULL (v4 A30/B60): compare Au-to-Al contact at the mirror via with/without Ar pre-clean; confirm the AJA substrate RF etch. R1_TRAP has no Al.
- [ ] W5 (only if E2): calibrate plating current on the R1_TRAP pattern; check thickness, gaps and bondability. If E1: lift-off of 0.35 µm Au over 5 µm gaps and wedge bonding on evaporated Au instead.
- [ ] W7: bond-and-leak loop; confirm bonder/wedge dimensions and carrier bond diagram.
- [ ] Verify mark coordinates, polarity and die IDs against [layout](LAYOUT.md) and [exposure checklist](mask_list.md#4-export-checklist-per-job).

See [Qualification](QUALIFICATION.md). No completed witness-wafer measurements are recorded in the reviewed progress notes.

## Before R1_FULL

- [ ] Finish detector reconciliation above.
- [ ] Obtain the full NbN recipe and sputter access; W1-a/b qualify the real stack and thermal history.
- [ ] W2: set HSQ dose/development/etch on the actual EBL tool; confirm mark recognition and L22-to-L50 overlay.
- [ ] Confirm test-die detector pads can be bonded for cold tests.
- [ ] Measure switching current and count plateau at operating temperature with RF off/on. The geometry audit questions the earlier 15–25 µA estimate; cold-test acceptance remains provisional.
- [ ] Compare charging drift and click-induced heating over bare SiO₂ with NODET.

## Source and model checks

- [ ] Resolve “Dietl 2025.” The [bond-pad report](../research/reports/Bond%20pad%20sizing%20for%20ion%20traps.md) could not locate it. Numerical test limits are retained as draft **[verify]** values.
- [ ] Resolve the Ba⁺ angular-emission model: older collection values use a σ-dipole; the geometry audit proposes isotropic emission and asks for an atomic-physics source check. Keep assumptions labelled.
- [ ] RCWA/FDTD, 3-D lead pickup and adiabatic transport timing remain open in the progress notes.
- [ ] Reconcile the full-stack physical Al-to-Au separation (~10.3 µm) with the current model's 10.0 µm ground-depth parameter.

## Choices already recorded as the team's

Project scope and fixed inputs, separate loading zone, high-resistivity Si, 50 µm height and the height policy, no bowtie, the narrow die (superseded), NODET die, R&D runs at MIT.nano, R1_TRAP first (all 2026-11-02, backfilled); no ITO and 10 × 10 mm edge-pad dies (2026-11-07); on-chip Au-fill-to-Al via (2026-11-08); local-mirror architecture, slot leads, A30 only, R1_TRAP on the v4 stack (2026-11-08). All are logged in [`notes/decisions.md`](../../notes/decisions.md), which Claude now writes for the team. Current layout retains 600 µm zone spacing and 0.8 MHz axial confinement.
