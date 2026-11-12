> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Steps 4 to 8 detector stack

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

Full stack only (A30 and B60 dies). R1_TRAP and NODET dies skip this stage. Current generators use the v4 local-mirror stack with the v3.1 meander: [reconcile estimates](../OPEN_DECISIONS.md#detector-documents-and-generated-layouts) before R1_FULL. Step numbers 8a/8b are retired.

**Changed from v3 on this page**
- Mirror: the Al under the spacer is the 100 nm inlaid local mirror, evaporated into a 100 nm recess in the thermal SiO₂ (step 3). History: 150 nm (v3), 450 nm (2026-11-08), then 100 nm inlaid (team decision 2026-11-09, [`notes/decisions.md`](../../../notes/decisions.md)). The 450 nm mirror left a 0.45 µm step under the centre DC and the slot leads. `sim/10c` showed the mirror's pickup goes to ground, and the thickness changes the nanowire current by under 2 µA (`sim/10c`, DESIGN_LOG step 37).
- Step 4: spacer unchanged (238 nm). It is deposited on a flat surface: after step 3 the Al top is level with the SiO₂ beside it.
- Step 5: NbN unchanged. The Al under it is the 100 nm evaporated local mirror, which is not grounded until the layer-40 mirror via (step 11v).
- Step 6: Ti/Au is contacts only: a strip from each NbN tab into the slot, ending in a 27 × 7 µm pad, plus the EBL marks. No long buried Ti/Au leads. The long SNSPD leads are electrode Au (layer 50), made later.
- Step 7: meander geometry unchanged (v3.1). Cap target moves with step 8.
- Step 8: total SiO₂ over the wires (HSQ + cap) is **160 ± 10 nm** (was 80 nm). It is the top surface over the detector, with vacuum above.
- Step 9: the 10 µm SiO₂ (D2) is removed in v4 (kept as a numbered entry at the end of this page).

> **Layer 22 is contacts only.** The long SNSPD leads are not buried. They are Au in the electrode layer (layer 50) and land on the step-6 pads through the layer-40 openings.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 4. PECVD SiO₂ spacer (238 nm)

- **Purpose:** sets the cavity phase between the Al mirror and the NbN. Second order is chosen for hillock clearance (DESIGN_LOG step 9b).
- **Tool:** PECVD-Samco-PD220 or PECVD-Oxford-TEOS, ≤ 300 °C [verify the tool's settable T].
- **Target:** **238 ± 10 nm**. ±10 nm costs ≤ ~0.05 absorption [team calc, DESIGN_LOG step 9]. Never 140–160 nm (node).
- **Measure:**
  - Ellipsometry on the device wafer, with an Al substrate model [verify which device-wafer area carries the 100 nm local mirror under the spacer].
  - A co-loaded bare-Si piece to cross-check the rate and index.
  - AFM roughness on a dummy die area, to compare with W1-a.
- **Go / no-go:** 228–248 nm; no visible hillocks.
- **Hazards:**
  - First heating of the Al.
  - The mirror is 100 nm evaporated Al, inlaid (was 150 nm in v3). It is evaporated Al with no Cu, not Al-1%Cu, so check for hillocks after the spacer deposition (DESIGN_LOG step 28 addendum; ≤ 300 °C). Witness W8 repeats the hillock check after a 300 °C cycle.
- [ ] Done — date: ____ operator: ____ t_sp (5 pts): ____ n: ____ notes: ____

## 5. NbN 7 nm, room-temperature RF-bias reactive sputter

- **Purpose:** detector film. Unchanged in v4.
- **Tool:** the Berggren-group AJA Orion (Medeiros 2019), or a MIT.nano AJA if it has **RF substrate bias** [verify; not confirmed in the report].
- **Recipe:**
  - Unheated reactive DC magnetron with **50 W RF substrate bias** (Dane 2017).
  - **Flows, power and pressure were not retrieved** (the DSpace PDF was rate-limited). Get the recipe from the group or from Dane APL 111, 122601 / DSpace 1721.1/126227.
  - Rate ~0.04 nm/s (Medeiros: 200 s → 8 nm), so ~175 s for 7 nm [verify].
- **Witnesses in the same run:**
  - (a) a thermal-SiO₂/Si chip, for ellipsometry with the Medeiros model and for Rsq;
  - (b) a spacer-over-Al chip from step 4 (Tc on the real stack). Its Al is the 100 nm evaporated, inlaid local-mirror film, as in the W1 stack of [QUALIFICATION](../QUALIFICATION.md) (pieces from W8).
- **Target:** 7.0 ± 0.5 nm; Rsq ≈ 400 Ω/sq (5 nm: ≈ 600 Ω/sq) [team calc from Medeiros' fit ρ = 245 µΩ·cm with a 0.88 nm intercept; Toomey 2018 gives 600 Ω/sq at ~5 nm]; Tc ≈ 7.8–8 K (Dane 2017; Toomey 2018).
- **Go / no-go:** Tc over 7 K, the team's threshold for a 5 K trap (decisions, 2026-11-02: "anything over 7K"; [decisions](../../../notes/decisions.md)). Todaro's ≥ 25 % margin above a ≤ 6 K surface would ask for 7.5 K (Todaro PRL p. 2) [verify].
- **Hazards:**
  - **Minimise air exposure.** Start step 6 within 24 h and store in an N₂ box (Medeiros oxidation law).
  - The RF bias couples to the local Al mirror under 238 nm of SiO₂. The mirror is not grounded until the layer-40 mirror via (step 11v), so it floats during this step. Arcing or charging risk is unknown [inference]; watch the bias trace.
- [ ] Done — date: ____ operator: ____ t (ellips.): ____ Rsq: ____ Tc (witness): ____ notes: ____

## 6. Ti/Au NbN contacts by lift-off (L22), BEFORE the nanowire etch

- **Purpose:** v4 contacts only.
  - Each contact covers the −x half of one NbN tab and runs into the slot, ending in a 27 × 7 µm pad. A30 pads at x = 143 … 170 µm; B60 at x = 126.5 … 153.5 µm; y = ±(1.5 … 8.5) µm.
  - The layer-40 openings (step 11v) and the long Au leads (layer 50) land on these pads.
  - EBL alignment crosses for step 7: 20 µm crosses, 2 µm arms [verify size], at (−60, ±700) and (540, ±700) µm (v4 layer map; v3 had (0, ±700) and (600, ±700)). [verify] whether crosses at the other mark sites are still needed.
  - The Au protects the NbN contact region during the CF₄ etch. Todaro thickened his leads with 350 nm Au to avoid latching (Todaro Supp. "Trap fabrication").
- **Tool:** MLA150; EBeam-Temescal-FC2800.
- **Recipe:**
  - Litho: LOR + S1813-class bilayer, MLA expose L22 **drawn** [verify resist stock].
  - **Developer hazard:** CD-26 / AZ 300 MIF is 2.38 % TMAH. 25 % TMAH thins NbN by ~0.25 nm per minute and leaves an etch-blocking residue (Toomey 2018). Use the **shortest develop** that clears the LOR, then a **≥ 3 min running DI rinse** (standing DI does not work, Toomey Expt. 1), then IPA.
  - No-TMAH alternative: a PMMA bilayer written on the EBL and developed in MIBK:IPA [team inference].
  - Deposition: if the evaporator has an in-situ Ar ion clean, use a short one to remove native NbOₓ at the contact [inference, verify]. Then Ti 10 nm / Au 350 nm (Todaro: 350 nm Au).
  - Lift-off: NMP or Remover PG at 60–80 °C. Short sonication is acceptable (Najafi 2015 sonicated 2 min).
- **Layer / align:** L22 → L1 (±1 µm; this sets the overlay of the layer-40 openings on these pads, see [mask list](../mask_list.md)).
- **Inspect:**
  - Lift-off complete; no Au flags; each contact continuous from its NbN tab to its pad.
  - **Contact pads cover the NbN tabs:** each 27 × 7 µm pad sits in the slot, and each contact covers the −x half of its tab (SEM or optical, on a trap die).
  - Lead resistance: [verify] method and target. The v3 figure (~0.1–0.3 kΩ per lead) was for the long buried leads and does not apply to the short v4 contacts; it has not been recomputed.
- **Hazards:** TMAH (above). Bare NbN is exposed during the litho.
- [ ] Done — date: ____ operator: ____ develop time: ____ rinse: ____ t_Au: ____ notes: ____

## 7. EBL nanowire (L20): HSQ, salty develop, CF₄ RIE; HSQ left on

- **Purpose:** the meander and tabs (trap dies); the T3 bar and the T4/T4b meanders (test dies). Job contents, including T8 and T9, in the [EBL job](../mask_list.md#2-ebl-job-for-layer-20-nbn).
- **Tool:** EBL-Elionix-HS50; RIE-PlasmaTherm-210RL (Toomey used a Plasma-Therm; that this is the same tool or recipe is [verify]).
- **Recipe:**
  1. HSQ spun to **50–70 nm**. Najafi 2015 used 70 nm. HSQ + cap must total 160 ± 10 nm (step 8), so the cap is 160 nm minus the HSQ left, i.e. ≈ 90–110 nm for 50–70 nm HSQ [team calc]. Bake per the HSQ datasheet [verify].
  2. Expose L20 **drawn**.
     - Najafi: 700–850 µC/cm² at 30 keV (Raith 150).
     - **Redo the dose test on the Elionix at its actual kV.** HS50 suggests 50 kV; if a 100/125 kV Elionix is used, the dose rises further. Expect roughly kV-proportional scaling [inference].
     - Matrix and PEC notes are in [mask list](../mask_list.md). Align to the L22 EBL crosses (A2, resolved).
  3. Develop in **salty developer (NaOH/NaCl)**, preferred over 25 % TMAH (proposed in Toomey 2018; its effect on NbN is not reported. Formulation and time [verify]). Then a ≥ 3 min running DI rinse, IPA, N₂ dry.
  4. CF₄ RIE at 50 W, 10 mTorr, ~2.5 min (Toomey 2018 for 5 nm). For 7 nm, use 2.5–3.0 min, set from W2 [verify].
  5. **Leave the HSQ on.** **No O₂ plasma** (it oxidises the NbN sidewalls).
- **Current v4 target (meander geometry v3.1, unchanged):** 130 nm wires on a 200 nm pitch (70 nm gaps, fill 0.65), 160 lines over a 32 µm radial extent. Lines 36 µm (A30) or 69 µm (B60) long; rounded end blocks and tapered tabs; NbN gaps ≥ 60 nm. Calibrate dose and separately inspect T9 controls. Use square counts from the released GDS for resistance acceptance.
- **Inspect:**
  - SEM: **linewidth target 130 nm wire / 70 nm gap** on T4/T4b (test dies; v4 test die, drawn and checked 2026-11-09; meander geometry v3.1); no bridges or breaks.
  - Room-temperature R at probe ≤ 1 V: main SNSPD (trap-die pads SNS/SNG), T4/T4b, and T3 4-wire (Rsq).
  - Expected meander R = N_sq × Rsq. Use the current [a7 estimate and acceptance](../tests/01_ELECTRICAL.md#a7-meander-r), with square counts checked against the released GDS. Earlier v3 values were ~18 / 36 MΩ at 400 Ω/sq.
  - Record R₀ (baseline for tracking). Also measure the remaining HSQ thickness on the W2 witness (it sets the cap in step 8).
- **Go / no-go:** R / R_expected 0.8–1.3 [verify]. Open → die rejected. A low R means unetched bridges.
- **Hazards:** ESD on the open meander. Wear a grounded strap, probe with the SMU at 0 V, compliance ≤ 1 V / ≤ 100 nA [inference].
- [ ] Done — date: ____ operator: ____ dose: ____ etch time: ____ R₀ (A30 dies): ____ HSQ left (W2): ____ notes: ____

## 8. SiO₂ cap, PECVD, same day as step 7

- **Purpose:** protect and passivate the nanowire. This is the Todaro Supp. fix for 12–30 % R rises; Hampel used a 130 nm cap. In v4 the total SiO₂ over the wires is the top surface over the detector, with vacuum above, so its thickness sets the absorption.
- **Target:**
  - **HSQ + cap = 160 ± 10 nm** (was 80 nm; DESIGN_LOG step 26). Cap = 160 nm − measured HSQ remaining, **≥ 30 nm** for sidewall coverage [inference].
  - Absorption (EMT, sim 09c, 238 nm spacer) [team calc]: 0.66 at 160 nm, 0.44 at 80 nm. A total of 146–172 nm stays within 0.02 of the best.
- **Tool:** PECVD at ≤ 300 °C. Measure the total SiO₂ (HSQ + cap) by ellipsometry on a co-loaded Si piece.
- **Hazards:**
  - The oxidising plasma meets the NbN sidewalls first. Hampel deposited PECVD directly on bare NbTiN without problems; there are no NbN data [inference].
  - Until the layer-40 openings (step 11v) the contacts are covered: **no electrical check is possible during step 8**. Use the W1-b witness instead.
  - Step 11v etches ~160 nm of SiO₂ over the contacts and ~0.40 µm (cap + spacer) over the mirror via [team calc, DESIGN_LOG step 26].
- [ ] Done — date: ____ operator: ____ t_cap (cap alone): ____ t_total (HSQ + cap, Si witness): ____ HSQ (witness): ____ notes: ____

## 8a, 8b. Removed in v3

These were the L24 via to M1 and the L31 buried ITO. v3 and v4 have no ITO (DESIGN_LOG step 17). Go from step 8 to the layer-40 openings (step 11v, [local-mirror variant H.2](../variants/LOCAL_MIRROR.md)).

## 9. Removed in v4

The 10 µm SiO₂ (D2) is not deposited in v4: there is no ground-plane D2 and no long 300 °C exposure after the NbN, and the step-8 cap is the top surface over the detector. Step 10 stays retired (top ITO, v3).

Continue: [next stage](03_ELECTRODES.md).
