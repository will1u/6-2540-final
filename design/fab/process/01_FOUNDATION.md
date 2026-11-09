> **Claude-authored.** Rewritten for v4 2026-11-09.

# Steps 0 to 3 substrate and Al local mirror

[Traveler](../TRAVELER.md) · [R1_TRAP](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

Which dies: A30 and B60 dies do steps 0 to 3. NODET dies and the R1_TRAP run skip step 3 (no Al at all). The v4 test dies (drawn and checked 2026-11-09) have no die-wide Al; their Al is in the local structures T2v, T4/T4b, T10, T11 and T12, which this page does not cover. After Al deposition, keep subsequent steps at or below 300 °C.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 0. Wafer prep and clean

- **Purpose:** clean HR FZ Si start, ρ > 20 kΩ·cm [verify spec sheet] (was > 10⁴ Ω·cm). The RF runs over thin SiO₂ on this Si with no ground plane (LOCAL_MIRROR H.4).
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
- **Hazards:** none (no Al or Au yet). No L10 cut-outs are needed at the mark sites, because the v4 mirror sits in the trap centre (LOCAL_MIRROR H.2, step 3v) [verify against the run map].
- [ ] Done — date: ____ operator: ____ depth: ____ notes: ____

## 2. Thermal SiO₂ D1, ~1 µm, both sides

- **Purpose:** isolation of the Al local mirror and the Au electrodes from the Si. The backside SiO₂ also starts the stress balance.
- **Tool:** Ox-Tube-Lindberg or Tube-OxAnneal-Expertech-CTR200.
- **Recipe:** wet oxidation to 1.0 µm [verify time/T on the tool chart]. JoVE used 0.5 µm at 900 °C for 4.5 h plus 0.2 µm LPCVD SiN. Romaszko gives 1–2 µm as typical for D1.
- **Target:** 1.00 ± 0.05 µm, by ellipsometry on 5 points.
- **Inspect:** marks still visible as topography.
- **Hazards:** none.
- [ ] Done — date: ____ operator: ____ t_SiO₂ (5 pts): ____ notes: ____

## 3. M1 Al-1%Cu local mirror (L10)

- **Purpose:** SNSPD mirror (238 nm PECVD SiO₂ spacer below the NbN; DESIGN_LOG steps 9, 26) and the ground of that mirror, tied to the Au ground fill through the mirror via (step 11). This is not an RF ground plane: v4 has no Al under the RF rails.
- **Thickness:** **450 nm** (team decision 2026-11-08; was 150 nm). The thicker strip lowers the mirror-to-ground resistance (about 5 Ω expected on T10; acceptance limit [verify], see Inspect). ≥ 100 nm is opaque (TMM: 50 nm transmits 0.12 %).
- **Shape (drawn, not inverted):** |y| ≤ 20 µm from x = −2240 µm to just past the detector (x = +268 µm on A30; +284.5 µm on B60), plus a branch under the Au ground fill to the mirror ground via at (−2140, 130) µm. Nothing under the RF rails.
- **Tool:** Sputter-AJA-* (Al-1%Cu target [verify availability]); MLA150; RIE-Cl2-SAMCO-200iP (route A only).
- **Recipe:** choose one route. LOCAL_MIRROR H.2 step 3v leaves the choice open, so both are written out here.
  - **Route A, etch (drawn L10 with the job not inverted):**
    - Deposit Al-1%Cu: JoVE sputtered at 300 W RF, 2 mTorr, 40 sccm Ar, ~13 nm/min. 450 nm therefore needs ≈ 35 min [team calc; verify rate on the AJA].
    - Litho: positive resist ~1.3–2 µm; MLA expose L10 **drawn**.
    - Etch: BCl₃/Cl₂ ICP. JoVE: BCl₃ 20 / Cl₂ 30 sccm, 5 mTorr, 750 W, ~360 nm/min, so ≈ 75 s for 450 nm [team calc; verify over-etch]. DI rinse right after the Cl etch to avoid Al-Cu corrosion [inference]. A wet Al etchant is an alternative [verify availability and suitability for the 40 µm strip].
    - Strip: solvent + O₂ ash.
  - **Route B, lift-off (as Hampel 2023):**
    - Litho first: LOR + positive resist [verify thickness for 450 nm]; MLA expose L10 **drawn**.
    - Deposit Al-1%Cu as in route A (≈ 35 min at the JoVE rate [team calc]). Hampel used 50 nm e-beam Al, so a 450 nm lift-off is not covered by that source [verify process].
    - Lift off [verify solvent and process].
- **Layer / align:** L10 → L1 (±5 µm).
- **Inspect:**
  - Rsq by 4-pt on a co-deposited Si witness: expect one third of the 150 nm value. At 150 nm the sheet resistance is 0.20–0.27 Ω/sq (DESIGN_LOG step 26), so at 450 nm it is 0.067–0.089 Ω/sq [team calc, ρ 3–4 µΩ·cm] [verify].
  - Darkfield for hillocks / whiskers before the spacer, and again after the spacer deposition (step 4).
  - Mirror shape against the drawing, including the branch to the ground via.
  - Mirror strip resistance: measured on test die T10 (four-point, taps 2510 µm apart, 62.75 squares; 4.2–5.6 Ω at 450 nm [team calc]); there is no mirror probe opening on the trap dies. Acceptance limit not set [verify].
  - Cut-outs: none in v4 (no Al under the SNSPD pads or the mark sites).
- **Hazards:** from here on the **≤ 300 °C rule** applies.
- [ ] Done — date: ____ operator: ____ route (A/B): ____ t_Al: ____ Rsq: ____ notes: ____

Continue: [next stage](02_DETECTOR.md).
