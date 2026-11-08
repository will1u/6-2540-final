# Wafer layout, and possible simplifications with the tests that would check them

> **Claude-authored**, 2026-11-02, at the team's request.
> - Part 1 explains the wafer layout and run-size options.
> - Part 2 lists ways to simplify the design, each with the tests that would show the design still works.
> - **None of these tests have been run.** Where a number already exists from an earlier DESIGN_LOG step, it is quoted with its step; anything else is a test to do, not a result.
> - Each simplification is a decision for you. Log the ones you adopt in `notes/decisions.md`.

---

> [!warning] Historical planning assumptions
> This catalog was drafted for v2: narrow dies, 184-die wafer, ITO and the earlier detector. References to `wafer_v3` were renamed without updating those assumptions. Use [current variants](fab/VARIANTS.md), [run plan](fab/RUN_PLAN.md) and [open decisions](fab/OPEN_DECISIONS.md) for fabrication. Candidate tests below remain proposals, not current run instructions.

## Part 1. What the wafer layout is

`gds/wafer_v3.gds` (from `make_wafer.py`) is the *placement plan* for a 100 mm wafer.

**What the layout fixes:**
- **Tiles:** 10 × 10.8 mm. Each tile holds four 10 × 2.5 mm dies stacked with 200 µm dicing streets: A30, B60, A30, test die.
- **Count:** the tiles that fit inside a 45 mm radius give 184 dies (92 A30, 46 B60, 46 test).
- **Die IDs:** `wafer_v3_map.csv` gives every die an ID and a centre coordinate.

**How a wafer run works:**
- **Patterning.** Every step in `fab/TRAVELER.md` is done to the whole wafer at once:
  - Depositions (oxide, Al, NbN, ITO), etches and plating treat the full wafer surface.
  - Each lithography layer is one job on the MLA150 (maskless, so no physical masks) that writes the pattern at every die position.
  - The nanowire layer is one EBL job that visits every meander.
- **After step 16:** the wafer gets a quick room-temperature probe test (step 17). Then it is coated with protective resist and sawn along the streets into individual dies (step 18).
- **Packaging:** you pick the best dies from the probe results and package those (step 19).

So yes: as drawn, all the traps are made together on one wafer and then cut apart.

### Does it have to be like that? No.

The process steps are wafer-scale anyway: you can't sputter or plate "one die". What you choose is how much of the wafer you *pattern*, and what size of substrate you put in the tools.

| Option | What it means | For | Against |
|---|---|---|---|
| **Full wafer** (as drawn) | All 184 dies written | Most dies; the most test-die data on uniformity | Longest write times. The EBL job is ~0.53 mm² of nanowire, estimated at ~2–5 h at 1 nA (`fab/mask_list.md` section 2) [team calc]. A single mistake costs the whole run. |
| **Full wafer, small block written** | Process a whole 100 mm wafer but expose only a central block, e.g. 2–3 tiles = 8–12 dies, in every MLA/EBL job | Resist, PECVD and plating stay uniform because the substrate is still a full wafer, with no edge effects on small pieces. Write time drops roughly 15–20×. Easy handling. | Most of the wafer area is unused (a wafer is cheap next to tool time) |
| **Quarter wafer** | Cleave first, then process a quarter (`mask_list.md` section 3: e.g. 35 dies) | Saves wafers if you plan several runs | Need to check every tool takes a quarter piece [verify]. Resist edge bead and plating current distribution are worse near cleaved edges. |
| **Single-tile piece** (≈ 1–2 cm square) | Process one tile (2 A30 + B60 + test) or a few | Smallest material use | **Risky for this process:** the ≥ 8 µm plating mold and ≥ 10 µm protect resist build thick edge beads on small pieces, and a 2.5 mm-wide die is never far from an edge. It also needs a plating contact on a tiny piece and special holders on most tools [verify]. |

**My recommendation:** for the first run, use a full wafer but write only a small central block. This keeps the process conditions the traveler assumes while cutting write time and risk. This is now implemented: `gds/make_run.py` writes 8-die run layouts (`run_R1_TRAP`, `run_R1_FULL`), and TRAVELER A.3 lays out the run sequence (DESIGN_LOG step 15).

Dicing is still needed with any option to separate the dies. Cleaving along scribed lines is a possible alternative to sawing, but it is less controlled on 2.5 mm-wide dies.

---

## Part 2. Possible simplifications

### What "still works" means

For each simplification, check that the numbers below hold. They are the baseline from DESIGN_LOG steps 6, 9b, 10, 11 and 13; **[verify]** marks margins that are my suggestions, not literature limits.

| Quantity | Baseline (A30, v2) | Suggested pass criterion |
|---|---|---|
| RF-null height at both zones | 50.08 / 50.09 µm (48.9 µm over the window) | within ±2 µm of the intended height [verify] |
| Radial secular frequencies, q | 2.98 MHz, q ≈ 0.30 | q ≤ 0.4; frequencies within 10 % [verify] |
| Trap depth | ≈ 52 meV | ≥ 40 meV [verify] |
| DC solutions at the zones | max \|V\| 9.05 V, radial tilt ~10° | \|V\| ≤ 10 V (DAC limit), tilt ≥ 5° |
| Transport loading → readout | max 7.33 V, ≤ 1.59 V per 10 µm step | ≤ 10 V, ≤ 2 V per step, no step at the limit |
| Axial RF pseudopotential bump at the window | ≤ 0.3 meV | ≤ 1 meV [verify] |
| NbN absorption at 493 nm | 0.53 (model reads ~10 % low) | stated per option; the trade-off is your call |
| RF current induced in the nanowire | ≈ 0 with grounded buried ITO; 0.72 µA (≈ 4 % of Isw) with Al mirror only (step 10) | ≤ 10 % of Isw [verify] |
| Layout | `check_chip.py` ALL CHECKS PASS | same |

**Tools to reuse:**
- **Electrostatics on a real layout:** `sim/12_final_chip_check.py` on the rebuilt `*_sim.json`.
- **Parametric geometry** (gap, metal thickness, ground depth): `sim/02_baseline_gds2itvg.py` / `trapgeom.py`.
- **Window in 3-D and gap cross-sections with oxide vs etched floors:** `sim/04_window_validation.py` and `04b_window_3d_fd.py`. These already have "oxide left" vs "etched" cases.
- **Segment count:** `sim/03_segment_pitch.py`.
- **Optics:** `sim/09_optical_stack_tmm.py`, `09b_itoD2_matching.py`.
- **RF pickup:** `sim/10_rf_pickup_2d.py`.
- **Laser clipping:** `sim/11_beam_clearance.py`.

**Stray-charge sensitivity test** (used several times below; a new short script, not written yet):
- In gds2itvg, make the exposed-dielectric region (window floor or gap floor) its own "electrode" and set it to 1 V. That stands in for charge on the surface.
- Compute the field at the ion and the DC change needed to cancel it.
- Compare with the baseline, where that region is metal.
- This turns "the ion sees bare oxide" into a number: V/m per volt of surface charging.

---

### A. Scope simplifications (the device design doesn't change)

#### S1. Write a small block instead of the full wafer
- **Removes:** most of the MLA and EBL write time; the scale of the dicing map.
- **Risks:** fewer test dies, so less information on uniformity.
- **Tests:**
  - **Before tape-out:** crop `wafer_v3.gds` to the block. Check that each MLA job, the EBL job and the dicing map list the same die IDs (`mask_list.md` section 4 checklist).
  - **After fab:** the usual test-die measurements, at least one test die per tile (`test_plan.md` (a)).
- **My take:** recommended for run 1.

#### S2. Staged runs: a plain-trap run first, SNSPD later
- **Removes from run 1:**
  - every SNSPD-specific step (traveler steps 4–8b and 10);
  - the EBL;
  - the NbN thermal-budget constraints.
- **How:** use `trap_die_v3_NODET` (DESIGN_LOG step 14). In parallel, or next, run the detector stack alone on test dies (T3, T4, T4b, T5, T7) to qualify NbN, optics and ITO before they are combined with the 10 µm D2 and plating.
- **Risks:**
  - The combination is only tested in run 2.
  - The interaction effects stay untested until the combined run: thermal budget of D2 and plating on finished NbN, and whether ITO survives the D2 etch.
- **Tests:**
  - *Run 1 (trap):*
    - `test_plan.md` (a) a1–a5 on trap and test dies;
    - trap an ion in the loading zone;
    - measure secular frequencies against the step 14 values;
    - transport to the readout zone and back;
    - micromotion compensation;
    - heating rate. This becomes the reference for the SNSPD die.
  - *Detector run:*
    - T3 Tc and Rsq;
    - T4/T4b switching current, dark counts, and efficiency at 493 nm (`test_plan.md` (b));
    - T5 and T7 resistances.
  - *Combined run:* repeat both sets. Compare heating rate and micromotion over the window against the run-1 die. That separates "the detector stack disturbs the ion" from "the trap process is bad".
- **My take:** recommended. It is the biggest de-risking step available.

#### S3. One detector size (drop B60)
- **Removes:** the second EBL pattern and the per-variant bookkeeping. B60 costs no extra fab steps, so the saving is small.
- **Risks:** lose the yield-vs-collection comparison (5.9 % vs 3.25 % geometric collection, step 7).
- **Tests:** none for the trap. On the detector side, check T4 yield (fraction of meanders with a normal Isw) on the test dies.
- **My take:** optional. Only worth it if EBL time is tight.

---

### B. Trap-process simplifications

#### S4. Skip the Au-masked D2 gap etch (traveler steps 16a, 16; layer L45)
- **Removes:** one thick-resist lithography step, a ~27 min deep oxide etch with tight stop control, and the L45 layer.
- **Risks:** the 5 µm gaps keep oxide at the level of the Au bottom, 6 µm below the electrode top, instead of being etched down near M1. The ion then sees more dielectric through each gap (aspect ratio 6/5 = 1.2 instead of ~3).
- **Tests:**
  - **Sim:**
    - Rerun `04_window_validation.py`'s 2-D cross-section for an *electrode gap* with an oxide floor at −6 µm vs etched to −15.6 µm. Check the RF-null height and depth against the criteria.
    - Run the stray-charge sensitivity test with the gap floors as the charged region. Compare the V/m per volt with the etched case.
  - **Fab / bench:**
    - T1 comb leakage and breakdown (a5) with and without the etch: build one witness wafer each way, or leave the etch off half the wafer.
    - Surface leakage at 300 V RF-to-ground (a1).
  - **Ion:** micromotion-compensation drift over hours, with and without the 493/650 nm beams on.
- **My take:** a real candidate if the etch stop is hard to control. Decide from the stray-charge number and from a1/a5.

#### S5. Evaporated thin Au (≈ 1–2 µm, lift-off) instead of 6 µm plating
- **Removes:** traveler steps 12–15: seed layer, ≥ 8 µm plating mold, plating, seed etch.
  - This is the biggest single process saving for the trap.
  - It also removes the plating-bath uncertainty.
- **Risks:**
  - The gap aspect ratio falls below 1, so more exposed oxide is visible to the ion (Bautista-Salvador 2019 ties the aspect ratio to this).
  - The RF electrode's series resistance rises.
- **Tests:**
  - **Sim:**
    - `trapgeom.py` / `02` with `metal_thickness` 1–2 µm: height, depth, q.
    - The stray-charge sensitivity test on the gaps.
    - If combined with S4, the case where both apply.
  - **Calc:**
    - RF current I = ωCV from the packaged RF capacitance (a10), and its dissipation in the thinner rails and lead.
    - Compare with the baseline. Au skin depth at 28 MHz is ~15 µm at room temperature, so 6 µm Au is already thinner than the skin depth.
  - **Bench:**
    - T6 loop resistance (a3), scaled to the RF lead.
    - Resonator Q with the chip connected.
    - a1/a5 breakdown.
- **My take:** possible for a plain-trap first run (S2). Decide after the stray-charge test.

#### S6. Wider gaps (e.g. 8–10 µm instead of 5 µm)
- **Removes:** the tightest lithography and plating-mold rule (5 µm lines in an ≥ 8 µm mold), raising yield.
- **Risks:** more exposed oxide per gap; a slightly different null height and depth.
- **Tests:**
  - **Sim:**
    - `trapgeom.py` sweep g = 5, 8, 10 µm at fixed h = 50 µm (re-solve the rail widths with `01_analytic_fivewire.py`), then `02`. Height, depth, q.
    - Rebuild the die with `make_chip.py` (G parameter) and run `12_final_chip_check.py`: DC sets and transport.
    - `check_chip.py`.
    - Stray-charge test.
  - **Bench:** T1 comb at the new gap.
- **My take:** a cheap, low-risk option if the 5 µm mold is marginal on the MLA150.

#### S7. Use Al (M1) marks as the first layer instead of etched-Si marks (L1)
- **Removes:** one lithography step and one Si etch (traveler step 1).
- **Risks:** Al marks could be harder to see under 10 µm of oxide for the L50 alignment. The L40 crosses already exist for that, though.
- **Tests:** overlay verniers on every layer of the test die (`mask_list.md` checklist). MLA alignment-camera check through the full stack on a witness wafer before committing.
- **My take:** optional.

#### S8. Fewer DC segments (e.g. 8 + 8 instead of 15 + 15)
- **Removes:** about 14 pads, leads and wire bonds, and the matching DAC channels and filter boards.
- **Risks:** less control at each zone, higher voltages, or rougher transport.
- **Tests:**
  - **Sim:**
    - `03_segment_pitch.py` for the reduced count. Check conditioning and \|V\| at 0.8 MHz.
    - Rebuild with `make_chip.py` (N_SEG, segment width, and possibly zone spacing).
    - `12_final_chip_check.py`: both zones within ±10 V with ~10° tilt; transport ≤ 2 V per step, no step at the limit.
    - `check_chip.py`.
  - If the zones also move closer together (e.g. 300 µm), check the beam clearance again (`11_beam_clearance.py`).
- **My take:** reasonable. The sim tells you directly whether it works.

#### S9. A single zone (load directly at the readout zone)
- **Removes:** transport and the loading zone. Combined with S8, it allows very few segments.
- **Risks:**
  - Atom flux and photoionisation light land right on the window and detector.
  - The SNSPD sees the loading lasers.
  - Todaro kept loading in a separate zone (the report gives 264 µm).
- **Tests:**
  - **Bench (cold):** SNSPD count rate with the photoionisation/405 nm beams on and off, and with the oven or ablation on, using T4 on a test die in the trap cryostat.
  - **Window optics:** transmission or detection efficiency before and after many loading cycles.
  - **Sim:** none beyond a single-zone DC set (`12`).
- **My take:** avoid for the SNSPD die. Fine for a plain trap.

#### S10. Remove the Al ground plane (M1), or keep only a local patch under the detector
- **Removes:** M1 deposition and lithography, the Al hillock and thermal-budget concerns, and the M1 bond openings. A local patch still needs one lithography step.
- **Risks:**
  - The Al plane shields the substrate from RF and is the ground the simulation assumes (`ground_depth` 10 µm).
  - Under the detector it is also the optical mirror and RF shield. Known numbers:
    - absorption falls from 0.63 to 0.28 without the mirror (step 9);
    - RF pickup without the mirror exceeds Isw (step 10).
- **Tests:**
  - **Sim:**
    - gds2itvg with no ground plane (`outer_ground_depth`/`ground_depth` set to the substrate) for height, depth and q.
    - `09`/`10` must keep a mirror and ground under the detector, so only the patch version is viable for the SNSPD die.
  - **Bench:** RF loss on a no-M1 witness: a T2-style capacitor and resonator Q at 28 MHz, at room temperature and cold.
- **My take:** avoid on the SNSPD die. For a plain trap, it combines naturally with S11.

#### S11. Plain trap on sapphire or fused silica: Au directly on the substrate, no M1, no D2
- **Removes:** almost everything. It becomes a one-metal process: Au lift-off or plating on an insulating substrate.
- **Risks:**
  - The exposed substrate in the gaps can charge.
  - The electrostatic stack differs from the simulated one.
  - Not compatible with the SNSPD stack as designed.
- **Tests:**
  - **Sim:** gds2itvg with no buried ground (dielectric substrate) for height, depth, q; stray-charge test on the gaps.
  - **Bench:** resonator Q; a1 breakdown; Au adhesion (tape test).
  - **Ion:** compare micromotion drift and heating rate with the Si run.
- **My take:** a fast way to a working five-wire trap for learning to trap and transport. Not a path to the integrated detector.

#### S12. Ground the centre DC electrode
- **Removes:** one DC channel. The top ITO and buried ITO would then both sit at ground, so their electrical connection can't harm anything.
- **Risks:** a degree of freedom lost. Step 6 found the window gives the centre DC most of a 0.8 MHz well at 0.73 V; without it, the segments do all the work.
- **Tests (sim):** `12_final_chip_check.py` with electrode 2 forced to 0 V (removed from the solve set). Both zones and transport against the criteria, including the tilt.
- **My take:** a wiring simplification, not a fab one. Try it in simulation; it costs nothing.

---

### C. Detector-stack simplifications

#### S13. Drop the buried ITO and its via (layers L31, L24)
- **Removes:** two lithography layers, one ITO lift-off, the via etch, and the via-chain test (T7). It also removes the "does ITO survive" question for the buried layer.
- **Risks** (known numbers):
  - absorption falls from 0.53 to 0.40 after re-optimising the spacer and cap (step 9b);
  - RF pickup goes from ≈ 0 to the Al-mirror-only 0.72 µA, ≈ 4 % of Isw (step 10, 2-D).
- **Tests:**
  - **Sim:**
    - Rerun `09b` for the no-buried-layer stack and fix the new spacer and cap thicknesses (the table gives 64 / 160 nm); include the ±10 nm corners.
    - Rerun `10` for that stack at 53 V. This is a 2-D estimate; a 3-D lead-pickup estimate is still an open item.
  - **Bench (cold):** on the test die, add a T4 copy without L31/L24 next to the existing one. Measure Isw, dark counts and efficiency with RF on and off (`test_plan.md` (b)), and compare the two.
- **My take:** the most attractive detector-side simplification. It costs about a quarter of the absorption, and the bench comparison is cheap to include.

#### S14. Drop the top ITO, leaving an open window with the oxide floor exposed
- **Removes:** one lithography layer and ITO lift-off on D2, plus the W4 question (does ITO survive the gap etch).
- **Risks:**
  - The ion sees bare oxide 6 µm below it, right where the detection beam and scattered light are strongest.
  - Step 6 rejected this to keep the ion seeing only conductors (Todaro Supp.; Hampel 2023).
  - Known numbers: Δh is −1.4 µm with an oxide floor vs −1.2 µm with ITO (04b).
- **Tests:**
  - **Sim:** the stray-charge sensitivity test with the window floor as the charged region (V/m per volt and the compensation it needs); `09` optics without the top ITO; `10` RF pickup without it.
  - **Fab:** L45 must then cover the window during the gap etch; it is drawn already.
  - **Ion:** micromotion-compensation drift at the readout zone with the detection beam on, compared with the loading zone and with a NODET die.
- **My take:** avoid unless the ITO process fails. If it does, this is the fallback and the tests above are the ones to run.

---

## Suggested order

1. **Cheap simulation checks, all in the existing scripts plus one new stray-charge script:**
   - S12 (grounded centre);
   - S8 (fewer segments);
   - S6 (wider gaps);
   - S13 (no buried ITO, `09b`/`10`);
   - the stray-charge numbers for S4/S5/S14.
2. **Run-planning choices:** S1 (small block) and S2 (plain trap first).
3. **After a witness wafer or the first run:** S4, S5 and S7 based on the bench data; S13 based on the T4 comparison.
