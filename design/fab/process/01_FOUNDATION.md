> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

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

- **Purpose:** isolation of the Al local mirror and the Au electrodes from the Si. The backside SiO₂ also starts the stress balance. Step 3 etches a 100 nm recess into this SiO₂ for the mirror, so 0.9 µm remains under the mirror.
- **Tool:** Ox-Tube-Lindberg or Tube-OxAnneal-Expertech-CTR200.
- **Recipe:** wet oxidation to 1.0 µm [verify time/T on the tool chart]. JoVE used 0.5 µm at 900 °C for 4.5 h plus 0.2 µm LPCVD SiN. Romaszko gives 1–2 µm as typical for D1.
- **Target:** 1.00 ± 0.05 µm, by ellipsometry on 5 points.
- **Inspect:** marks still visible as topography.
- **Hazards:** none.
- [ ] Done — date: ____ operator: ____ t_SiO₂ (5 pts): ____ notes: ____

## 3. M1 inlaid Al local mirror (L10)

- **Purpose:** SNSPD mirror (238 nm PECVD SiO₂ spacer below the NbN; DESIGN_LOG steps 9, 26) and the ground of that mirror, tied to the Au ground fill through the mirror via (step 11). This is not an RF ground plane: v4 has no Al under the RF rails. The mirror is inlaid, so the surface under the spacer, NbN, cap and Au stays flat.
- **Thickness:** **100 nm**, inlaid: the Al top is level with the SiO₂ beside it (recess depth 100 nm in step 3b, Al 100 nm nominal in step 3c). History: 150 nm (v3) → 450 nm (2026-11-08) → 100 nm, inlaid (team decision 2026-11-09, [decisions](../../../notes/decisions.md)). Reason: the 450 nm mirror left a 0.45 µm step under the centre DC and the slot leads, and the simulation showed that the mirror's pickup goes to ground and that the thickness changes the nanowire current by under 2 µA (`sim/10c`, DESIGN_LOG step 37). 100 nm is opaque (≥ 100 nm is opaque; 50 nm transmits 0.12 %). Expected: sheet resistance 0.30–0.40 Ω/sq; T10 strip 18.8–25.1 Ω (`sim/10c`, DESIGN_LOG step 37).
- **Shape (drawn, not inverted):** |y| ≤ 20 µm from x = −2240 µm to just past the detector (x = +268 µm on A30; +284.5 µm on B60), plus a branch under the Au ground fill to the mirror ground via at (−2140, 130) µm. Nothing under the RF rails.
- **Tool:** MLA150; the SiO₂ RIE tool of step 3b (RIE-F-Samco-230iP or RIE-PlasmaTherm-210RL); EBeam-Temescal-FC2800 [verify Al source]; lift-off bath [verify].
- **Recipe:**
  - **3a Resist.** LOR + positive resist [verify thicknesses]. MLA150; expose layer 10 **drawn** (the resist is open where the mirror goes). Layer 10 data and alignment (L10 → L1, ±5 µm) are unchanged.
  - **3b Recess.** RIE a 100 nm recess into the thermal SiO₂ through that resist. Same chemistry as the step-11 layer-40 etch: CHF₃ 25 / CF₄ 5 / Ar 50 sccm, 130 mTorr, 600 W (JoVE flows, as carried in `process/03_ELECTRODES.md` step 11) [verify on our tool; verify etch rate]. Tool as step 11. Target depth 100 ± 10 nm [design call; verify]. The depth is known by calibrating the etch rate on a dummy thermal-SiO₂ piece the same day (witness loop W8), then timing the etch [verify].
  - **3c Al.** E-beam evaporate Al through the same resist. Set the Al thickness to the measured recess depth from 3b, 100 nm nominal. Tool: EBeam-Temescal-FC2800, the evaporator already named for E1 [verify that it has an Al source].
  - **3d Lift-off.** As step 6 and E1: NMP or Remover PG [verify]. After lift-off the Al top is level with the SiO₂ beside it.
  - The Al deposition and lift-off follow Hampel 2023 (arXiv:2302.01462), which made a 50 nm e-beam evaporated Al mirror by lift-off. The recess is this design's addition, not in Hampel, and is unproven until witness loop W8 passes.
- **Fallback:** if W8 fails, skip 3b. The result is a 100 nm raised mirror, a 0.10 µm step under the Au, with the same mask and the same later steps. The planarity limits under Inspect then do not apply; step 15 and test structure T12 must show that the Au crosses the 0.10 µm step.
- **Layer / align:** L10 → L1 (±5 µm).
- **Inspect:**
  - Recess depth: target 100 ± 10 nm, from the same-day rate calibration on the dummy piece. On the device wafer the resist is still on after 3b, so the depth error shows up as the residual step after lift-off.
  - Residual step and edge lip or groove after lift-off (≤ 20 nm each) by profilometer or AFM across the T10 strip and one trap mirror [design call; verify].
  - Lift-off complete; no Al flags or residue.
  - Rsq by 4-pt on a co-deposited witness: expected 0.30–0.40 Ω/sq [team calc, ρ 3–4 µΩ·cm] [verify].
  - Darkfield for hillocks / whiskers before the spacer, and again after the spacer deposition (step 4).
  - Mirror shape against the drawing, including the branch to the ground via.
  - Mirror strip resistance: measured on test die T10 (four-point, taps 2510 µm apart, 62.75 squares; 18.8–25.1 Ω expected [`sim/10c`, DESIGN_LOG step 37]). There is no mirror probe opening on the trap dies. Acceptance limit not set [verify].
  - Cut-outs: none in v4 (no Al under the SNSPD pads or the mark sites).
- **Hazards:** from here on the **≤ 300 °C rule** applies.
- [ ] Done — date: ____ operator: ____ recess depth: ____ t_Al: ____ residual step: ____ Rsq: ____ notes: ____

Continue: [next stage](02_DETECTOR.md).
