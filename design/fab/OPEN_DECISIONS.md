> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Open design decisions and run requirements

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

The first section concerns design choices; the next sections prepare each run. An unchecked item does not reverse an adopted choice. Recipe values tagged **[verify]** remain provisional.

## Design choices

| Decision | Choices | What resolves it | Scope |
|---|---|---|---|
| Architecture | Die-wide Al + D2, or local mirror | Compare qualification effort with the [proposal's](variants/LOCAL_MIRROR.md) routing/simulation work | Baseline currently retained |
| Local-mirror routing | Slot along centre DC, or thicker local SiO₂ over buried leads | Implement routing, check isolation, rerun trap fields | Local mirror only |
| Local-mirror Au | E1: ~0.35 µm lift-off; E2: 6 µm plated | Gap-charge shielding, resonator tests and process trade-off | Local mirror only |
| Readout radial tilt | Smaller tilt, zero tilt, or wider DAC range | Recorded 10° solutions need 13.2 V A30 / 15.2 V B60, beyond ±10 V; zero tilt needs 6.6 / 3.4 V [team calc, step 19] | Detector readout; NODET/load-zone solution fits |
| Detector allocation | Keep A30/B60, or change next-run mix | Compare yield, collection and B60 transport | R1_FULL currently contains both |
| RF grounding / filters | Centre-DC filtering, carrier grounds, symmetric detector termination or cancellation | Bond diagram, DC-to-RF coupling calculation, RF-on/off tests | Full-stack operation |

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
- [ ] W3: qualify D2 stress/backside compensation and chuck bow limit; calibrate L40 and gap etches.
- [ ] W3: compare fill-to-Al contact with/without Ar pre-clean; confirm AJA substrate RF etch and seed continuity down via walls.
- [ ] W5: calibrate plating current on the R1_TRAP pattern; check thickness, gaps and bondability.
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

R1_TRAP first (2026-11-02); no ITO and 10 × 10 mm edge-pad dies (2026-11-07); on-chip Au-fill-to-Al vias (2026-11-08). Current layout retains 600 µm zone spacing and 0.8 MHz axial confinement. The team should record adopted choices in `notes/decisions.md`; that team-owned file is unchanged.
