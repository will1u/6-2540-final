> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Steps 0 to 3 substrate and Al ground plane

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

Both runs. After Al deposition, keep subsequent steps at or below 300 °C.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 0. Wafer prep and clean

- **Purpose:** clean HR FZ Si start (ρ > 10⁴ Ω·cm [verify spec sheet]).
- **Tool:** Acid-Etch-General-* hood.
- **Recipe:**
  - Scribe the ID on the backside edge.
  - Piranha 15 min (JoVE substrate step).
  - DI rinse, spin dry. RCA clean if the furnace rules require it before step 2 [verify MIT.nano furnace cleanliness rules].
- **Inspect:** particles under a darkfield microscope.
- **Also:** set aside **≥ 3 dummy Si wafers** for W1/W3/W5.
- [ ] Done — date: ____ operator: ____ notes: ____

## 1. L1 alignment marks (Si RIE ~1 µm)

- **Purpose:** permanent marks for every later layer.
- **Tool:** DirectWrite-MLA150 + RIE-F-Samco-230iP (SF₆/O₂ or a Si recipe [verify recipe name]).
- **Recipe:**
  - HMDS; positive resist ~1.3 µm (S1813-class [verify stocked resist]).
  - MLA expose L1 **drawn** (wafer job on the run GDS, `run_<name>.gds`); develop (TMAH developer is fine here); etch Si ~1 µm.
  - Strip in solvent + O₂ ash.
- **Target:** 1.0 ± 0.2 µm, by Dektak.
- **Layer / align:** L1; first layer, aligned to the wafer flat. Four crosses per die: trap dies (±4300, ±4830), test dies (−1700, ±1080) and (4300, ±1080), die coordinates; die centres in `run_<name>_map.csv`.
- **Inspect:** crosses sharp, depth recorded.
- **Hazards:** none (no metal yet). M1 is cut out 300 × 300 µm at every mark site (A1, resolved), so the marks stay visible through the oxides.
- [ ] Done — date: ____ operator: ____ depth: ____ notes: ____

## 2. Thermal oxide D1, ~1 µm, both sides

- **Purpose:** isolation under M1. The backside oxide also starts the stress balance.
- **Tool:** Ox-Tube-Lindberg or Tube-OxAnneal-Expertech-CTR200.
- **Recipe:** wet oxidation to 1.0 µm [verify time/T on the tool chart]. JoVE used 0.5 µm at 900 °C for 4.5 h plus 0.2 µm LPCVD SiN. Romaszko gives 1–2 µm as typical for D1.
- **Target:** 1.00 ± 0.05 µm, by ellipsometry on 5 points.
- **Inspect:** marks still visible as topography.
- **Hazards:** none.
- [ ] Done — date: ____ operator: ____ t_ox (5 pts): ____ notes: ____

## 3. M1 Al-1%Cu ground plane + mirror (L10)

- **Purpose:** RF ground and SNSPD mirror (×2.2 absorption; DESIGN_LOG step 9).
- **Thickness:** **150 nm** (DESIGN_LOG step 9; ≥ 100 nm is opaque). Thicker Al gives more hillock material, so there is no gain from going above ~200 nm [inference].
- **Tool:** Sputter-AJA-* (Al-1%Cu target [verify availability]); MLA150; RIE-Cl2-SAMCO-200iP.
- **Recipe:**
  - Deposition: JoVE sputtered Al-1%Cu at 300 W RF, 2 mTorr, 40 sccm Ar, ~13 nm/min, so ~12 min for 150 nm [verify rate on the AJA].
  - Litho: positive resist ~1.3–2 µm; MLA expose L10 **inverted** (the pull-back ring and cut-outs).
  - Etch: BCl₃/Cl₂ ICP. JoVE: BCl₃ 20 / Cl₂ 30 sccm, 5 mTorr, 750 W, ~360 nm/min. DI rinse right after the Cl etch to avoid Al-Cu corrosion [inference]. A wet Al etchant is an alternative for these ≥ 150 µm features [verify availability].
  - Strip: solvent + O₂ ash.
- **Layer / align:** L10 → L1 (±5 µm).
- **Inspect:**
  - Rsq by 4-pt on a co-deposited Si witness [verify expected ~0.2–0.3 Ω/sq].
  - Darkfield for hillocks / whiskers.
  - Cut-outs open: trap dies, under the SNSPD pads (290 × 250 µm) and at the 4 mark sites (300 × 300 µm); test dies, the T3/T4/T4b pad areas and the mark sites.
- **Hazards:** from here on the **≤ 300 °C rule** applies.
- [ ] Done — date: ____ operator: ____ t_Al: ____ Rsq: ____ notes: ____

Continue: [next stage](02_DETECTOR.md).
