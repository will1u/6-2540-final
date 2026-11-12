> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm 2026-11-09; final stack 2026-11-12.

# Steps 4 to 8 detector stack

[Traveler](../TRAVELER.md) · [R1_TRAP sheet (superseded for R1_ONE)](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

On R1_ONE every die receives the blanket steps **4, 5 and 8, including NODET** (the trap-only die). The patterned steps (6, 7, 11) are done only where they are drawn: A30, B60 and SNSPD-only dies. On NODET the blanket NbN is etched off in step 7. Current generators use the v4 local-mirror stack with the v3.1 meander: [reconcile estimates](../OPEN_DECISIONS.md#detector-documents-and-generated-layouts) before the next run. Step numbers 8a/8b are retired.

**Changed on this page (2026-11-12)**
- **Step 3 (earlier page section):** the mirror is raised, 100 nm of Al on the base SiO₂, and there is no recess. The surface under the spacer is therefore stepped by 100 nm at each mirror edge, not flat.
- **Step 4:** spacer unchanged (238 nm). It is blanket: it goes on NODET too.
- **Step 5:** NbN unchanged. Blanket on all dies; etched off on NODET in step 7.
- **Step 6:** Ti 5 nm / Au 50 nm (was 10 / 350 nm). Contacts only: a strip from each NbN tab into the slot, ending in a 27 × 7 µm pad, plus the EBL marks. The long SNSPD leads are electrode Au (layer 50), made later.
- **Step 7:** HSQ target 50 nm after develop, left on the NbN wires only. New check: an open field reads open circuit after the etch.
- **Step 8:** the PECVD SiO₂ cap is one blanket number, 110 nm (= 160 nm − the HSQ left). Over the wires SiO₂ totals 160 ± 10 nm (HSQ + cap). Elsewhere the cap is 110 nm. It is blanket: it goes on NODET too.

**Changed from v3 on this page (kept)**
- Mirror: 100 nm Al, raised (2026-11-12). Earlier: 150 nm (v3), 450 nm (2026-11-08), 100 nm inlaid (2026-11-09, superseded). The 450 nm mirror left a 0.45 µm step under the centre DC and the slot leads. `sim/10c` showed the mirror's pickup goes to ground, and the thickness changes the nanowire current by under 2 µA (DESIGN_LOG step 37).
- Step 8: total SiO₂ over the wires is 160 ± 10 nm (was 80 nm). It is the top surface over the detector, with vacuum above.
- Step 9: the 10 µm SiO₂ (D2) is removed in v4 (kept as a numbered entry at the end of this page).

> **Layer 22 is contacts only.** The long SNSPD leads are not buried. They are Au in the electrode layer (layer 50) and land on the step-6 pads through the layer-40 openings.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 4. PECVD SiO₂ spacer (238 nm), blanket on all dies

- **Purpose:** sets the cavity phase between the Al mirror and the NbN. Second order is chosen for hillock clearance (DESIGN_LOG step 9b). Blanket: it covers the raised Al, the base SiO₂ and, on NODET, the electrode area.
- **Tool:** PECVD-Samco-PD220 or PECVD-Oxford-TEOS, ≤ 300 °C [verify the tool's settable T].
- **Target:** **238 ± 10 nm**. ±10 nm costs ≤ ~0.05 absorption [team calc, DESIGN_LOG step 9]. Never 140–160 nm (node).
- **Measure:**
  - Ellipsometry on the device wafer [verify which area carries the witness: the spacer goes over the raised 100 nm Al, so use a spacer-over-Al witness, see the W1 stack in [QUALIFICATION](../QUALIFICATION.md)].
  - A co-loaded bare-Si piece to cross-check the rate and index.
  - AFM roughness on a dummy die area, to compare with W1-a.
- **Go / no-go:** 228–248 nm; no visible hillocks.
- **Hazards:**
  - First heating of the Al.
  - The mirror is 100 nm evaporated Al, raised on the base SiO₂ (was 150 nm in v3). It is evaporated Al with no Cu, not Al-1%Cu, so check for hillocks after the spacer deposition (DESIGN_LOG step 28 addendum; ≤ 300 °C). Witness W8 repeats the hillock check after a 300 °C cycle.
  - The spacer goes over the 100 nm mirror edge, so it is thinner on the edge [verify with the AFM or cross-section on W1].
- [ ] Done — date: ____ operator: ____ t_sp (5 pts): ____ n: ____ notes: ____

## 5. NbN 7 nm, room-temperature RF-bias reactive sputter, blanket on all dies

- **Purpose:** detector film. Blanket on all dies; the NbN on NODET and the other areas outside the meanders is etched off in step 7.
- **Tool:** the Berggren-group AJA Orion (Medeiros 2019), or a MIT.nano AJA if it has **RF substrate bias** [verify; not confirmed in the report].
- **Recipe:**
  - Unheated reactive DC magnetron with **50 W RF substrate bias** (Dane 2017).
  - **Flows, power and pressure were not retrieved** (the DSpace PDF was rate-limited). Get the recipe from the group or from Dane APL 111, 122601 / DSpace 1721.1/126227.
  - Rate ~0.04 nm/s (Medeiros: 200 s → 8 nm), so ~175 s for 7 nm [verify].
- **Witnesses in the same run:**
  - (a) a thermal-SiO₂/Si chip, for ellipsometry with the Medeiros model and for Rsq;
  - (b) a spacer-over-Al chip from step 4 (Tc on the real stack). Its Al is the 100 nm evaporated, raised local-mirror film, as in the W1 stack of [QUALIFICATION](../QUALIFICATION.md) (pieces from W8).
- **Target:** 7.0 ± 0.5 nm; Rsq ≈ 400 Ω/sq (5 nm: ≈ 600 Ω/sq) [team calc from Medeiros' fit ρ = 245 µΩ·cm with a 0.88 nm intercept; Toomey 2018 gives 600 Ω/sq at ~5 nm]; Tc ≈ 7.8–8 K (Dane 2017; Toomey 2018).
- **Go / no-go:** Tc over 7 K, the team's threshold for a 5 K trap (decisions, 2026-11-02: "anything over 7K"; [decisions](../../../notes/decisions.md)). Todaro's ≥ 25 % margin above a ≤ 6 K surface would ask for 7.5 K (Todaro PRL p. 2) [verify].
- **Hazards:**
  - **Minimise air exposure.** Start step 6 within 24 h and store in an N₂ box (Medeiros oxidation law).
  - The RF bias couples to the local Al mirror under 238 nm of SiO₂. The mirror is not grounded until the layer-40 mirror via (step 11), so it floats during this step. Arcing or charging risk is unknown [inference]; watch the bias trace.
- [ ] Done — date: ____ operator: ____ t (ellips.): ____ Rsq: ____ Tc (witness): ____ notes: ____

## 6. Ti/Au NbN contacts by lift-off (L22), BEFORE the nanowire etch

- **Purpose:** v4 contacts only, Ti 5 nm / Au 50 nm.
  - Each contact covers the −x half of one NbN tab and runs into the slot, ending in a 27 × 7 µm pad. A30 pads at x = 143 … 170 µm; B60 at x = 126.5 … 153.5 µm; y = ±(1.5 … 8.5) µm.
  - The layer-40 openings (step 11) and the long Au leads (layer 50) land on these pads.
  - EBL alignment crosses for step 7: 20 µm crosses, 2 µm arms [verify size], at (−60, ±700) and (540, ±700) µm (v4 layer map; v3 had (0, ±700) and (600, ±700)). [verify] whether crosses at the other mark sites are still needed.
  - **Why thin:** it is the etch stop for the layer-40 opening etch (the fluorine plasma that opens SiO₂ also etches NbN, and 7 nm cannot stop it). It carries the e-beam crosses, which must exist before the nanowire is written. About 20 µm of each contact strip lies under the centre-DC Au with only the 110 nm cap between, so it must be thin. 350 nm was the v3 lead thickness and has no job in v4. Todaro used 350 nm Au on his leads (Todaro Supp. "Trap fabrication"); here the contact Au is 50 nm for the reason above.
  - [verify] e-beam mark contrast on 50 nm Au, and the Au lost in the opening over-etch (step 11).
- **Tool:** MLA150; EBeam-Temescal-FC2800.
- **Recipe:**
  - Litho: LOR + S1813-class bilayer, MLA expose L22 **drawn** [verify resist stock].
  - **Developer hazard:** CD-26 / AZ 300 MIF is 2.38 % TMAH. 25 % TMAH thins NbN by ~0.25 nm per minute and leaves an etch-blocking residue (Toomey 2018). Use the **shortest develop** that clears the LOR, then a **≥ 3 min running DI rinse** (standing DI does not work, Toomey Expt. 1), then IPA.
  - No-TMAH alternative: a PMMA bilayer written on the EBL and developed in MIBK:IPA [team inference].
  - Deposition: if the evaporator has an in-situ Ar ion clean, use a short one to remove native NbOₓ at the contact [inference, verify]. Then **Ti 5 nm / Au 50 nm** [verify thicknesses].
  - Lift-off: NMP or Remover PG at 60–80 °C. Short sonication is acceptable (Najafi 2015 sonicated 2 min).
- **Layer / align:** L22 → L1 (the Al marks, ±1 µm; this sets the overlay of the layer-40 openings on these pads, see [mask list](../mask_list.md)).
- **Inspect:**
  - Lift-off complete; no Au flags; each contact continuous from its NbN tab to its pad.
  - **Contact pads cover the NbN tabs:** each 27 × 7 µm pad sits in the slot, and each contact covers the −x half of its tab (SEM or optical, on a trap die or the SNSPD-only die).
  - Lead resistance: [verify] method and target. The v3 figure (~0.1–0.3 kΩ per lead) was for the long buried leads and does not apply to the short v4 contacts; it has not been recomputed.
- **Hazards:** TMAH (above). Bare NbN is exposed during the litho.
- [ ] Done — date: ____ operator: ____ develop time: ____ rinse: ____ t_Au (50 nm target): ____ notes: ____

## 7. EBL nanowire (L20): HSQ, salty develop, CF₄ RIE; HSQ left on the wires

- **Purpose:** the meander and tabs (A30, B60 and the SNSPD-only die cells). The NbN on the other dies, including NODET, is removed in this step (below).
- **Tool:** EBL-Elionix-HS50; RIE-PlasmaTherm-210RL (Toomey used a Plasma-Therm; that this is the same tool or recipe is [verify]).
- **Recipe:**
  1. HSQ spun to give **50 nm after develop** (target, measured on the W2 witness) [verify spin curve]. Najafi 2015 used 70 nm (citation only). The HSQ left sets the cap in step 8: cap = 160 nm − HSQ left, so **110 nm** for 50 nm HSQ. Bake per the HSQ datasheet [verify].
  2. Expose L20 **drawn**.
     - Najafi: 700–850 µC/cm² at 30 keV (Raith 150).
     - **Redo the dose test on the Elionix at its actual kV.** HS50 suggests 50 kV; if a 100/125 kV Elionix is used, the dose rises further. Expect roughly kV-proportional scaling [inference].
     - Matrix and PEC notes are in [mask list](../mask_list.md). Align to the L22 EBL crosses (A2, resolved).
  3. Develop in **salty developer (NaOH/NaCl)**, preferred over 25 % TMAH (proposed in Toomey 2018; its effect on NbN is not reported. Formulation and time [verify]). Then a ≥ 3 min running DI rinse, IPA, N₂ dry.
  4. CF₄ RIE at 50 W, 10 mTorr, ~2.5 min (Toomey 2018 for 5 nm). For 7 nm, use 2.5–3.0 min, set from W2 [verify].
  5. **Leave the HSQ on the wires.** **No O₂ plasma** (it oxidises the NbN sidewalls).
  6. **NODET and other areas without layer 20:** the blanket NbN is etched off by the same CF₄ etch, with no HSQ pattern. [verify: the etch time that clears the NbN over the whole die, and the NbN clearance check below]
- **Current v4 target (meander geometry v3.1, unchanged):** 130 nm wires on a 200 nm pitch (70 nm gaps, fill 0.65), 160 lines over a 32 µm radial extent. Lines 36 µm (A30) or 69 µm (B60) long; rounded end blocks and tapered tabs; NbN gaps ≥ 60 nm. Use square counts from the released GDS for resistance acceptance.
- **Inspect:**
  - SEM: **linewidth target 130 nm wire / 70 nm gap** on the detector cells of the SNSPD-only die (D1–D8) and on the W2 witness [verify]; no bridges or breaks. The dose array (T8) and the T4/T4b test meanders are not on R1_ONE; the dose test is on the W2 witness [verify].
  - **NbN cleared check (new, on R1_ONE):** on an open field, two probes read open circuit after the etch. Check it on a NODET position and on a trap die, not only on the detector cells.
  - Room-temperature R (R₀) cannot be read on the trap dies at this step: the SNSPD pads are electrode Au, and the contacts are covered by the cap. Early resistance readings come from T3 at step 11 on the SNSPD-only die, and from the finished cells. [verify]
  - Expected meander R = N_sq × Rsq. Use the current [a7 estimate and acceptance](../tests/01_ELECTRICAL.md#a7-meander-r), with square counts checked against the released GDS. Earlier v3 values were ~18 / 36 MΩ at 400 Ω/sq.
  - Measure the remaining HSQ thickness on the W2 witness (it sets the cap in step 8).
- **Go / no-go:** open meander → die rejected. A low R means unetched bridges. The NbN cleared check: an open field must read open circuit.
- **Hazards:** ESD on the open meander. Wear a grounded strap, probe with the SMU at 0 V, compliance ≤ 1 V / ≤ 100 nA [inference].
- [ ] Done — date: ____ operator: ____ dose: ____ etch time: ____ HSQ left (W2): ____ NbN cleared (open field): ____ notes: ____

## 8. SiO₂ cap, PECVD blanket, same day as step 7, on all dies

- **Purpose:** protect and passivate the nanowire. This is the Todaro Supp. fix for 12–30 % R rises; Hampel used a 130 nm cap. In v4 the SiO₂ over the wires is the top surface over the detector, with vacuum above, so its thickness sets the absorption.
- **Target:**
  - **One blanket number: 110 nm PECVD SiO₂**, adjusted to **160 nm minus the measured HSQ left** (110 nm for 50 nm HSQ).
  - **Over the wires the SiO₂ totals 160 ± 10 nm** (HSQ + cap). Elsewhere the cap is 110 nm.
  - Cap ≥ 30 nm over the wires for sidewall coverage [inference]. Met by 110 nm.
  - Absorption (EMT, sim 09c, 238 nm spacer) [team calc]: 0.66 at 160 nm, 0.44 at 80 nm. A total of 146–172 nm stays within 0.02 of the best.
- **Tool:** PECVD at ≤ 300 °C. Measure the cap by ellipsometry on a co-loaded Si piece, and the total (HSQ + cap) on the same piece.
- **Hazards:**
  - The oxidising plasma meets the NbN sidewalls first. Hampel deposited PECVD directly on bare NbTiN without problems; there are no NbN data [inference].
  - Until the layer-40 openings (step 11) the contacts are covered: **no electrical check is possible during step 8**. Use the W1-b witness instead.
  - Step 11 etches 110 nm of SiO₂ over the contacts and 348 nm (cap + spacer) over the mirror via [team calc, DESIGN_LOG step 26].
- [ ] Done — date: ____ operator: ____ t_cap (cap alone, 110 nm target): ____ t_total (HSQ + cap, Si witness, 160 ± 10 nm): ____ HSQ (witness): ____ notes: ____

## 8a, 8b. Removed in v3

These were the L24 via to M1 and the L31 buried ITO. v3 and v4 have no ITO (DESIGN_LOG step 17). Go from step 8 to the layer-40 openings (step 11, [local-mirror variant H.2](../variants/LOCAL_MIRROR.md)).

## 9. Removed in v4

The 10 µm SiO₂ (D2) is not deposited in v4: there is no ground-plane D2 and no long 300 °C exposure after the NbN. The step-8 cap is the top surface over the detector. Step 10 stays retired (top ITO, v3).

Continue: [next stage](03_ELECTRODES.md).
