> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Steps 4 to 8 detector stack

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

Full stack only; R1_TRAP skips this stage. Current generators use v3.1 geometry: [reconcile estimates](../OPEN_DECISIONS.md#detector-documents-and-generated-layouts) before R1_FULL. Step numbers 8a/8b are retired.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 4. PECVD SiO₂ spacer (238 nm)

- **Purpose:** sets the cavity phase. Second order is chosen for hillock clearance (DESIGN_LOG step 9b).
- **Tool:** PECVD-Samco-PD220 or PECVD-Oxford-TEOS, ≤ 300 °C [verify the tool's settable T].
- **Target:** **238 ± 10 nm**. ±10 nm costs ≤ ~0.05 absorption [team calc, DESIGN_LOG step 9]. Never 140–160 nm (node).
- **Measure:**
  - Ellipsometry on the device wafer, with an Al substrate model.
  - A co-loaded bare-Si piece to cross-check the rate and index.
  - AFM roughness on a dummy die area, to compare with W1-a.
- **Go / no-go:** 228–248 nm; no visible hillocks.
- **Hazards:** first heating of the Al.
- [ ] Done — date: ____ operator: ____ t_sp (5 pts): ____ n: ____ notes: ____

## 5. NbN 7 nm, room-temperature RF-bias reactive sputter

- **Purpose:** detector film.
- **Tool:** the Berggren-group AJA Orion (Medeiros 2019), or a MIT.nano AJA if it has **RF substrate bias** [verify; not confirmed in the report].
- **Recipe:**
  - Unheated reactive DC magnetron with **50 W RF substrate bias** (Dane 2017).
  - **Flows, power and pressure were not retrieved** (the DSpace PDF was rate-limited). Get the recipe from the group or from Dane APL 111, 122601 / DSpace 1721.1/126227.
  - Rate ~0.04 nm/s (Medeiros: 200 s → 8 nm), so ~175 s for 7 nm [verify].
- **Witnesses in the same run:**
  - (a) a thermal-SiO₂/Si chip, for ellipsometry with the Medeiros model and for Rsq;
  - (b) a spacer-over-Al chip from step 4 (Tc on the real stack).
- **Target:** 7.0 ± 0.5 nm; Rsq ≈ 400 Ω/sq (5 nm: ≈ 600 Ω/sq) [team calc from Medeiros' fit ρ = 245 µΩ·cm with a 0.88 nm intercept; Toomey 2018 gives 600 Ω/sq at ~5 nm]; Tc ≈ 7.8–8 K (Dane 2017; Toomey 2018).
- **Go / no-go:** Tc ≥ 7.5 K, which leaves Todaro's ≥ 25 % margin above a ≤ 6 K surface (Todaro PRL p. 2) [verify].
- **Hazards:**
  - **Minimise air exposure.** Start step 6 within 24 h and store in an N₂ box (Medeiros oxidation law).
  - The RF bias couples to the floating Al plane under 238 nm of oxide. Arcing or charging risk is unknown [inference]; watch the bias trace.
- [ ] Done — date: ____ operator: ____ t (ellips.): ____ Rsq: ____ Tc (witness): ____ notes: ____

## 6. Ti/Au SNSPD leads by lift-off (L22), BEFORE the nanowire etch

- **Purpose:** leads, pads and the EBL alignment crosses for step 7 (20 µm crosses, 2 µm arms: on trap dies at (0, ±700) and (600, ±700) around the readout zone, and one at every mark site on both die types). The Au protects the NbN contact region during the CF₄ etch. Todaro thickened his leads with 350 nm Au to avoid latching (Todaro Supp. "Trap fabrication").
- **Tool:** MLA150; EBeam-Temescal-FC2800.
- **Recipe:**
  - Litho: LOR + S1813-class bilayer, MLA expose L22 **drawn** [verify resist stock].
  - **Developer hazard:** CD-26 / AZ 300 MIF is 2.38 % TMAH. 25 % TMAH thins NbN by ~0.25 nm per minute and leaves an etch-blocking residue (Toomey 2018). Use the **shortest develop** that clears the LOR, then a **≥ 3 min running DI rinse** (standing DI does not work, Toomey Expt. 1), then IPA.
  - No-TMAH alternative: a PMMA bilayer written on the EBL and developed in MIBK:IPA [team inference].
  - Deposition: if the evaporator has an in-situ Ar ion clean, use a short one to remove NbOx at the contact [inference, verify]. Then Ti 10 nm / Au 350 nm (Todaro: 350 nm Au).
  - Lift-off: NMP or Remover PG at 60–80 °C. Short sonication is acceptable (Najafi 2015 sonicated 2 min).
- **Layer / align:** L22 → L1 (±1 µm; this sets the L22↔L50 overlay, see [mask list](../mask_list.md)).
- **Inspect:** lift-off complete; no Au flags; leads continuous. Expected lead RT resistance ~0.1–0.3 kΩ per lead [team calc], negligible next to the meander.
- **Hazards:** TMAH (above). Bare NbN is exposed during the litho.
- [ ] Done — date: ____ operator: ____ develop time: ____ rinse: ____ t_Au: ____ notes: ____

## 7. EBL nanowire (L20): HSQ, salty develop, CF₄ RIE; HSQ left on

- **Purpose:** the meander and tabs (trap dies); the T3 bar and the T4/T4b meanders (test dies). Job contents, including T8 and T9, in the [EBL job](../mask_list.md#2-ebl-job-for-layer-20-nbn).
- **Tool:** EBL-Elionix-HS50; RIE-PlasmaTherm-210RL (Toomey used a Plasma-Therm; that this is the same tool or recipe is [verify]).
- **Recipe:**
  1. HSQ spun to **50–70 nm**. Najafi 2015 used 70 nm. Because HSQ + cap must total 80 nm, a thinner HSQ (~50 nm) leaves room for a ≥ 30 nm PECVD cap. Bake per the HSQ datasheet [verify].
  2. Expose L20 **drawn**.
     - Najafi: 700–850 µC/cm² at 30 keV (Raith 150).
     - **Redo the dose test on the Elionix at its actual kV.** HS50 suggests 50 kV; if a 100/125 kV Elionix is used, the dose rises further. Expect roughly kV-proportional scaling [inference].
     - Matrix and PEC notes are in [mask list](../mask_list.md). Align to the L22 EBL crosses (A2, resolved).
  3. Develop in **salty developer (NaOH/NaCl)**, preferred over 25 % TMAH (proposed in Toomey 2018; its effect on NbN is not reported. Formulation and time [verify]). Then a ≥ 3 min running DI rinse, IPA, N₂ dry.
  4. CF₄ RIE at 50 W, 10 mTorr, ~2.5 min (Toomey 2018 for 5 nm). For 7 nm, use 2.5–3.0 min, set from W2 [verify].
  5. **Leave the HSQ on.** **No O₂ plasma** (it oxidises the NbN sidewalls).
- **Current v3.1 target:** 130 nm wires / 70 nm spaces, 160 lines. Calibrate dose and separately inspect T9 controls. Use square counts from the released GDS for resistance acceptance.
- **Inspect:**
  - SEM: linewidth on T4/T4b (test dies); no bridges or breaks.
  - Room-temperature R at probe ≤ 1 V: main SNSPD (trap-die pads SNS/SNG), T4/T4b, and T3 4-wire (Rsq).
  - Expected meander R = N_sq × Rsq. Use the current [a7 estimate and acceptance](../tests/01_ELECTRICAL.md#a7-meander-r), with square counts checked against the released GDS. Earlier v3 values were ~18 / 36 MΩ at 400 Ω/sq.
  - Record R₀ (baseline for tracking). Also measure the remaining HSQ thickness on the W2 witness.
- **Go / no-go:** R / R_expected 0.8–1.3 [verify]. Open → die rejected. A low R means unetched bridges.
- **Hazards:** ESD on the open meander. Wear a grounded strap, probe with the SMU at 0 V, compliance ≤ 1 V / ≤ 100 nA [inference].
- [ ] Done — date: ____ operator: ____ dose: ____ etch time: ____ R₀ (A30 dies): ____ notes: ____

## 8. SiO₂ cap, PECVD, same day as step 7

- **Purpose:** protect and passivate the nanowire. This is the Todaro Supp. fix for 12–30 % R rises; Hampel used a 130 nm cap. Here it also sets the matching-layer phase.
- **Target:** cap = 80 nm − measured HSQ remaining, **≥ 30 nm** for sidewall coverage [inference]. HSQ + cap = 80 ± 10 nm. With no ITO the cap touches the D2 SiO₂, so its thickness barely matters optically (earlier v3 absorption ≈ 0.40; DESIGN_LOG step 17; reconcile for 65 % fill).
- **Tool:** PECVD at ≤ 300 °C. Measure the cap on a co-loaded Si piece (ellipsometry).
- **Hazards:**
  - The oxidising plasma meets the NbN sidewalls first. Hampel deposited PECVD directly on bare NbTiN without problems; there are no NbN data [inference].
  - From here until step 11 the pads are covered: **no electrical check is possible during steps 8–9**. Use the W1-b witness instead.
- [ ] Done — date: ____ operator: ____ t_cap: ____ HSQ (witness): ____ notes: ____

## 8a, 8b. Removed in v3

These were the L24 via to M1 and the L31 buried ITO. v3 has no ITO (DESIGN_LOG step 17); go from step 8 straight to step 9.

Continue: [next stage](03_ELECTRODES.md).
