> **Claude-authored.** Rewritten for v4 2026-11-09. The v3 page was reorganized 2026-11-08 from the project fabrication notes.

# Steps 9 to 16 SiO₂ and Au electrodes

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

This page follows the v4 local-mirror stack ([variant H](../variants/LOCAL_MIRROR.md), adopted 2026-11-08). Steps 9, 10, 16a and 16 are removed in v4. Step 11 is common to both electrode options. The electrode Au is still open: **E1** (Ti/Au lift-off, 0.35 µm) and **E2** (plated Au, 6 µm) are two complete, parallel sequences with equal standing. Use one of them; the comparison table at the end gives process facts only.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## Changed from v3

- **Step 9** (10 µm PECVD SiO₂ D2, stress-balanced, backside SiO₂): removed. Heading renamed to "Removed in v4".
- **Step 10**: still empty; v3 ITO is gone and v4 has no D2. Heading renamed.
- **Step 11**: now layer 40 openings through the thin stack only. Mirror ground via and SNSPD contact openings. The v3 D2 openings, fill-to-Al ground vias, Al bond openings and L50 alignment-cross openings are gone.
- **Steps 12 to 15** are now two sections, E1 and E2. Each step is numbered and labelled with its option. The v3 text of steps 12 to 15 is carried into E2.
- **Steps 16a and 16**: removed in v4 (no D2, layer 45 retired).
- **Added:** the E1 section, the E2 section, the inspection list shared by both, and the "E1 vs E2 at a glance" table.
- **Architecture link** to [variant H](../variants/LOCAL_MIRROR.md) added.

## 9. Removed in v4

This was the 10 µm PECVD SiO₂ D2 with stress balancing and backside SiO₂. v4 has no thick SiO₂, so there is no stress balancing and no backside deposition.

## 10. Removed in v3 and v4

This was the top ITO on D2 (removed in v3). v4 has no ITO and no D2, so this step stays empty. Go from step 8 (cap) straight to step 11.

## 11. Layer 40 openings through the thin stack

- **Purpose:** open the SiO₂ cap and spacer over the mirror ground via, down to the Al; open the SiO₂ cap over the SNSPD contacts, down to the layer-22 Au pads.
- **Openings:**
  - (a) **Mirror ground via:** one 100 × 100 µm opening per detector die, centred at (−2140, 130) µm, through the SiO₂ cap and spacer (about 0.40 µm) down to the Al. It is enclosed ≥ 25 µm by the Au fill and the Al.
  - (b) **SNSPD contact openings:** 18 × 3 µm, at x = 148 … 166 µm (B60: 131.5 … 149.5 µm), |y| = 3.5 … 6.5 µm, through the SiO₂ cap down to the layer-22 Au pad. Each opening sits ≥ 1 µm inside the Au lead and the Ti/Au pad.
  - (c) **No mirror probe opening.** LOCAL_MIRROR H.2 and H.5 asked for a small Al probe opening; none is in the v4 GDS and none is planned. The mirror is checked on the test dies instead: T10 for the strip, T11 for the Au-to-Al via contact, and the mirror probe pads on T4/T4b.
- **Not in v4:** no Al bond openings, no fill-to-Al vias at the die edge, no 150 µm ground-via openings, no layer 45 patch.
- **NODET dies and R1_TRAP** have no layer 40 and skip this step.
- **Tool:** MLA150; RIE-F-Samco-230iP or RIE-PlasmaTherm-210RL (as in v3).
- **Resist:** thin positive resist, about 1.3 µm [verify].
- **Recipe:**
  - CHF₃ 25 / CF₄ 5 / Ar 50 sccm, 130 mTorr, 600 W (JoVE flows, carried from v3 step 11) [verify on our tool].
  - Etch about 1 min [verify] (LOCAL_MIRROR H.2). At the v3 rate of ~360 nm/min, 0.40 µm needs about 1.1 min [team calc]; the over-etch is set on W3 [verify].
  - Stops on Al (mirror via) and on Au (SNSPD contacts).
- **Cap thickness:** 160 ± 10 nm total SiO₂ over the NbN is the step-26 target. The GDS generator and the simulation metadata now state 160 nm (corrected 2026-11-09; geometry unchanged). [verify: confirm the deposited cap thickness before the etch time is set]
- **Layer / align:** L40 → L1 (±5 µm, carried from v3). [verify: the contact opening lands on a 27 × 7 µm Au pad and has only the ≥ 1 µm margin drawn; check the overlay budget against it]
- **Inspect:**
  - Dektak or equivalent depth at the mirror via; clean Al at the via floor and clean Au at every contact floor.
  - SNSPD pads (both tied together) to the Al at ≤ 1 V must read **> 1 GΩ** (no short through the spacer). [verify: threshold carried from the v3 M1 check]
  - First probe access to the meander: the v4 test dies are drawn and checked (2026-11-09), so this check can use the T4/T4b probe pads.
- **Hazards:** the v3 long etch and its heat exposure no longer apply; the etch is about 1 min [inference].
- [ ] Done — date: ____ operator: ____ etch time: ____ via depth: ____ SNSPD–Al: ____ notes: ____

## Electrodes, layer 50: E1 and E2

Layer 50 is the electrode Au, the ground fill, the pads, and in v4 the SNSPD leads in the slot along the centre DC. Both options draw the same layer 50. They differ only in how the Au is deposited. Run one option, then the inspection in its step 15.

---

## E1: Ti/Au lift-off, 0.35 µm

- **Purpose:** electrode, ground fill, pads and SNSPD leads in one Ti/Au layer, deposited by evaporation and lifted off. No plating.
- **Tools:** MLA150 (layer 50 drawn); evaporator EBeam-Temescal-FC2800 (the traveler's Ti/Au lift-off tool, step 6) [verify 350 nm Au and the Ti run]; in-situ Ar clean before the Ti [verify tool and whether it is available on that evaporator]; NMP lift-off bath [verify].
- **Layer / align:** L50 → L1 and L40 crosses [verify overlay].

### 12 (E1). LOR and positive resist, layer 50 exposure

- **Recipe:**
  - LOR + positive resist [verify thickness and spin for the 0.35 µm Au and the 0.40 µm via step].
  - MLA exposure of layer 50 **drawn**. With positive resist, exposed areas are removed, so the Au lands where layer 50 is drawn [verify dose and develop].
- **Inspect:** resist opening at the 5 µm gaps and at the slot; undercut for lift-off [verify].
- [ ] Done — date: ____ operator: ____ LOR t: ____ resist t: ____ overlay: ____ notes: ____

### 13 (E1). In-situ Ar pre-clean, Ti 10 nm / Au 350 nm

- **Ar pre-clean first:** in-situ, before the Ti, to remove the AlF₃ on the mirror-via floor (DESIGN_LOG step 22) [verify time and power]. On dies without a mirror via (NODET, R1_TRAP) whether the pre-clean is needed is [verify].
- **Ti 10 nm, then Au 350 nm,** evaporated [verify thicknesses; Hampel used 350 nm Au].
- Notes: the Au must cover the 0.40 µm via step and the mirror edge (checked in step 15).
- [ ] Done — date: ____ operator: ____ Ar pre-clean: ____ Ti t: ____ Au t: ____ notes: ____

### 14 (E1). Lift-off in NMP

- **Recipe:** lift-off in NMP [verify time, temperature and whether agitation is used].
- [ ] Done — date: ____ operator: ____ lift-off time: ____ notes: ____

### 15 (E1). Inspect

- **Inspect (both options, same list):**
  - all 5 µm gaps open everywhere;
  - SNSPD leads continuous in the slot (5 µm lines, 5 µm gaps);
  - mirror via covered by the ground fill (≥ 25 µm enclosure);
  - Au continuous over the 0.40 µm via step and over the mirror edge [verify];
  - electrodes isolated (neighbours > 100 MΩ at 10 V) [verify, carried from v3 step 15];
  - **fill-to-mirror resistance** at the test die: the old < 10 Ω limit does not apply as drawn (the Al strip is about 5 Ω at 450 nm [team calc]; DESIGN_LOG step 28 addendum), plus the contacts. [verify: replacement limit]
  - wire bond on 350 nm evaporated Au [verify].
- **Checks for this option (not a verdict):**
  - gap depth-to-width 0.07 (0.35 µm Au over 5 µm gaps), so SiO₂ is exposed in every gap, as the ion sees it;
  - Au coverage of the 0.40 µm via step and the mirror edge with 0.35 µm Au;
  - wedge-bondability of 350 nm evaporated Au [verify].
- [ ] Done — date: ____ operator: ____ gap check: ____ fill–mirror R: ____ bond test: ____ notes: ____

---

## E2: plated Au, 6 µm

Steps 12 to 15 are the v3 plating steps, carried onto the thin stack. Changes from v3 are noted in each step.

- **Purpose:** 6 µm plated Au for the electrodes, ground fill, pads and SNSPD leads. The plated thickness is the only change in the electrode layer.
- **Tools:** Sputter-AJA-* (seed); MLA150 (mold); Plating-U04 [chemistry unverified]; Asher-*, Clean-Ar-Plasma [verify it can mill], RIE-F (strip, seed removal).

### 12 (E2). Plating seed Ti 15 nm / Au 50 nm (PTB)

- **Tool:** Sputter-AJA-* (sputter for step coverage; PTB evaporated).
- **Ar pre-clean first:** an in-situ RF Ar sputter clean before the Ti, to remove the AlF₃ and native Al₂O₃ on the mirror-via floor (DESIGN_LOG step 22). Without it the Au to Al contact may be open. [verify the AJA has a substrate RF etch, and its time, on W3]
- **Sidewall coverage:** the v3 check was seed continuity down a 10.4 µm via wall. In v4 the mirror via is about 0.40 µm deep (step 11), so the wall is that deep. Check by cross-section on W3 [verify].
- **Note:** the seed shorts every electrode and both SNSPD pads together. That is ESD-safe, but no electrical checks are possible until step 15.
- **Note:** the seed coats the window floor, which is the SiO₂ cap over the NbN. It is removed in step 15.
- [ ] Done — date: ____ operator: ____ notes: ____

### 13 (E2). Layer 50 plating mold (negative, ≥ 8 µm)

- **Tool:** MLA150.
- **Recipe:**
  - AZ nLOF 2070 at ≥ 8 µm (PTB thesis used nLOF 2070; spin curve [verify]). Mold ≥ 1.3 × the plating thickness [inference].
  - MLA expose layer 50 **inverted** (resist stays where there is no Au). PEB and develop per datasheet.
  - Short O₂ descum.
  - Leave the cathode contact points at the wafer edge free of resist.
- **Layer / align:** L50 → layer-40 crosses seen through the seed (±1 µm, critical) [verify on v4 crosses].
- **Note:** the step at the mirror via is about 0.40 µm (step 11), not 10 µm as in v3. Check the nLOF profile at that step [verify].
- **Inspect:**
  - Window opening registered to the meander.
  - 5 µm gap lines clean down to the seed.
  - nLOF profile (re-entrant): record the gap width at the bottom.
- [ ] Done — date: ____ operator: ____ t_resist: ____ overlay (µm): ____ notes: ____

### 14 (E2). Au electroplating, 6 µm

- **Tool:** Plating-U04. **Whether it is a gold tank, and its chemistry, are not verified.** PTB used a sulfite bath (Enthone Microfab Au 100-B, pH 7.5, compatible with nLOF).
- **Recipe:**
  - Plated area, measured from the v4 GDS ([measured table](../../gds/measured_v4.md)): 0.913 cm² per A30 or B60 die, 0.915 cm² per NODET die, 5.917 cm² for `run_R1_TRAP` and 5.735 cm² for `run_R1_FULL`. Such a small plated area needs a low, well-calibrated current; confirm the tank's minimum [verify].
  - Current density per bath datasheet [verify]. At 3 mA/cm² and 100 % efficiency, Au(I) deposits ~0.19 µm/min, so ~32 min for 6 µm [team calc, Faraday].
  - Plate in two halves and measure in between.
- **Notes:** the SiO₂ cap over the NbN is the only layer between the NbN and the plating resist over the detector [inference: protects the NbN under the plating resist, Todaro's damage step].
- **Target:** 6.0 ± 0.5 µm (DESIGN_LOG step 2); ≤ 10 % across the wafer [verify]; no nodules.
- [ ] Done — date: ____ operator: ____ I / t: ____ thickness map: ____ notes: ____

### 15 (E2). Strip, descum, seed removal

- **Recipe:**
  1. Strip nLOF in hot NMP / Remover PG. Then O₂ plasma + F plasma for resist debris (PTB).
  2. **Ar ion etch of the Au seed** at ~50 nm/min (PTB): ~1 min + ~20 % over [verify that Clean-Ar-Plasma, or an Ar RIE recipe, actually mills].
  3. **F-plasma etch of the Ti** at ~10 nm/min (PTB): ~1.5 min + over.
- **Exposure notes:**
  - The window floor is the SiO₂ cap (160 nm target, see step 11). The F plasma and the end of the Ar etch can thin it. The cap is the optical matching layer (DESIGN_LOG step 26), so a loss of a few nm would shift the optics [inference; measure the cap after this step].
  - The SNSPD Au pads lose a few nm of Au.
  - Line-of-sight redeposition is unavoidable (Sussex).
- **Inspect (both options, same list as E1 step 15):**
  - all electrodes isolated (neighbours > 100 MΩ at 10 V) [verify];
  - 5 µm gaps open; SNSPD leads continuous in the slot;
  - mirror via covered by the ground fill;
  - fill-to-mirror resistance [verify: replacement limit];
  - meander R₂ (test die T4/T4b; the v4 test die is drawn and checked, 2026-11-09);
  - window floor optically clean (no Au film);
  - AFM: Au roughness ~8 nm rms (PTB 8.3(5) nm).
- **Checks for this option (not a verdict):**
  - gap depth-to-width 1.2 (6 µm Au over 5 µm gaps);
  - seed continuity over the 0.40 µm via step, since the plating needs it;
  - the cap over the NbN under the plating resist [inference].
- [ ] Done — date: ____ operator: ____ Ar time: ____ F time: ____ cap t: ____ R₂: ____ notes: ____

---

## E1 vs E2 at a glance (process facts only)

| Item | E1: Ti/Au lift-off, 0.35 µm | E2: plated Au, 6 µm |
|---|---|---|
| Numbered steps on this page | 12 (E1) to 15 (E1); 15 is inspection | 12 (E2) to 15 (E2); 15 includes strip and seed removal |
| Tools named on this page | MLA150; EBeam-Temescal-FC2800 [verify]; in-situ Ar clean [verify]; NMP lift-off [verify] | Sputter-AJA-*; MLA150; Plating-U04 [chemistry unverified]; Asher-*; Clean-Ar-Plasma [verify]; RIE-F |
| Au thickness | 0.35 µm (Ti 10 nm under) [verify] | 6.0 µm plated, on a Ti 15 nm / Au 50 nm seed (seed removed in step 15) |
| Layer 50 resist | LOR + positive resist [verify thickness] | AZ nLOF 2070, ≥ 8 µm |
| Gap depth-to-width ratio (5 µm gaps) | 0.07 | 1.2 |
| Must be verified | Au coverage of the 0.40 µm via step; wedge bond on 350 nm Au; in-situ Ar clean on the evaporator; LOR thickness and undercut; lift-off time; fill-to-mirror R | Plating tank minimum against the measured 5.7–5.9 cm² per run; seed continuity on the 0.40 µm via; cap thickness after step 15; Ar pre-clean on the AJA |
| Shared with the other option | Steps 9 to 11 (step 9 and 10 removed); inspection list in step 15 | Same |

## 16a. Removed in v4

There is no thick SiO₂ to clear from the gaps, and layer 45 is retired in v4 (it must stay empty). Nothing to do in this step.

## 16. Removed in v4

The Au-masked SiO₂ gap etch clears D2, which v4 does not have. The thin SiO₂ stack stays in the gaps under both options; see the gap checks in E1 and E2.

Continue: [next stage](04_PACKAGING.md).
