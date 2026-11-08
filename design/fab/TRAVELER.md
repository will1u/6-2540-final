> **Claude-authored.** Run sheet (traveler) for the v3 10 × 10 mm trap dies `gds/trap_die_v3_A30.gds` (A30), `gds/trap_die_v3_B60.gds` (B60) and `gds/trap_die_v3_NODET.gds` (plain trap), and the 10 × 2.5 mm test die `gds/test_die_v3.gds`. **v3 has no indium tin oxide (ITO):** the readout window is an opening in the centre-DC Au over bare SiO₂ (DESIGN_LOG step 17), so steps 8a, 8b and 10 are removed (numbers kept so cross-references still work). Each R&D run writes a small block from `gds/run_<name>.gds` (section A.3); `gds/wafer_v3.gds` is the full-wafer reference. It turns DESIGN_LOG steps 0–10 and 9b plus the research report (`research/reports/Trap integrated SNSPD design.md`) into a step list. It is a starting recipe, not a qualified process: every number marked **[verify]** is an inference, a tool setting nobody has checked, or a value that needs a witness wafer. Companion files: `mask_list.md`, `process_checks.md`, `test_plan.md`.

# Traveler: Ba⁺ surface trap with integrated NbN SNSPD, 100 mm HR float-zone Si

Wafer ID: ________ Run layout: `run_________.gds` (R1_TRAP / R1_FULL / other) Generator versions / date: ________ Start date: ________ Operator: ________

Source shorthand: JoVE = Hong 2017 (JoVE 56060); PTB = Bautista-Salvador 2019 (NJP 21, 043011) and Bautista-Salvador thesis 2015; Sussex = Siegele-Brown 2022; Todaro = Todaro 2021 PRL + Supp.; Hampel = Hampel 2023 (APL 122, 174001). "[team calc]" = computed for this project, not from a paper.

---

## A. Die layout (v3) and tape-out status

Earlier layouts are archived: v1 (square die, trap in a corner) in `gds/archive_v1_square/`, v2 (narrow 10 × 2.5 mm die, two-ITO window) in `gds/archive_v2_narrow/`. Nothing in this traveler refers to them any more.

**Trap die floorplan** (`gds/make_chip.py`; `check_chip.py` passes on all three v3 dies, 2026-11-07). GDS µm, die centre at (0, 0):

| Feature | Location |
|---|---|
| Die (L101) | 10 × 10 mm: x = ±5000, y = ±5000 |
| Trap axis | die centre line, y = 0 |
| RF rails | x = −2000 … +2000, U closed at the right (+x) end; RF pad (4700, 0) on the right die edge |
| Zones | loading x = −300, readout (SNSPD, window) x = +300 |
| Segments | 15 + 15 at 100 µm pitch, centres x = −700 … +700; outer DC depth 200 µm |
| Edge pads | 120 × 200 µm Au, four rows along the top and bottom die edges at y = ±4720 (moved in 60 µm in step 21 so a 50 µm fill strip runs outboard of the rows): TL1–TL8 at x = −3500 … −2240, TR1–TR9 at x = +3500 … +2060 (same x for BL / BR) |
| Left die edge | centre-DC pad C (−4650, 0); SNSPD pads SNS (−4750, +260) and SNG (−4750, −260) |
| Ground | Au ground-fill bond spots GND-1…4 at (±4700, ±1500); M1 bond openings M1-1…4 at (±4700, ±2000), on the left/right die edges; eight 150 × 150 µm fill-to-M1 ground vias (L40 under the Au fill) at (±4700, ±1000) and (±1000, ±2500) (DESIGN_LOG step 22) |
| Alignment marks | L1 at (±4300, ±4830), in edge notches of the Au ground fill |
| Full pad list | `gds/trap_die_v3_A30_pads.csv` (`_B60_pads.csv` is identical) |

**Beam clearance** (`sim/11_beam_clearance.py`, full 10 mm chip) [team calc]: with the trap on the centre line of a 10 × 10 mm die, about **1.7 × 10⁻² of a 493 nm beam** (3.2 × 10⁻² at 650 nm, 9.6 × 10⁻³ at 405 nm) hits the surface, vs 1.1 × 10⁻⁵ on the v2 2.5 mm die. Team decision 2026-11-07 (DESIGN_LOG step 18). The 45° beams through the zones leave the die at the top/bottom edges near |x| ≈ 4.7 mm and the side edges near |y| ≈ 4.7 mm; no pad sits in the corners |x|, |y| > 4 mm (`check_chip.py`).

**Test structures** are not on the trap die. They are on `gds/test_die_v3.gds` (`make_test_die.py`, 10 × 2.5 mm, same layer stack): T1 Au comb (5 µm gap), T2 Au/D2/M1 capacitor 0.8 × 0.8 mm + M1 pad, T3 NbN 4-wire bar, T4 spare SNSPD 30 × 30 and T4b spare SNSPD 60 × 30 (under SiO₂ cap + D2 only), T6 Au continuity loop, T8 EBL dose array (T5 and T7 were ITO tests and are gone in v3) (seven 30 × 30 µm meanders on L20 datatypes 1–7, factors 0.80–1.20 × nominal; `mask_list.md` section 2). Each run layout has two test dies.

**Plain trap die, no SNSPD** (`gds/trap_die_v3_NODET.gds`, `make_chip.py --nodet`, DESIGN_LOG step 14):
- Same electrodes, pads, marks and M1 bond openings as A30. It has no window (solid centre DC) and nothing on L20 or L22.
- It is in both run layouts (`run_R1_TRAP`, `run_R1_FULL`) but not on `wafer_v3.gds`. On a mixed wafer it simply receives no features in those layers' steps.
- **Trap-only wafer:** run steps 0–3, 9, 11–19 and skip steps 4–8. D2 (step 9) then goes directly on M1. Keep it 10 µm, which is the `ground_depth` the simulation assumes.
- Step 11 opens only the four M1 bond openings and the L50 alignment crosses.
- Step 17 drops the SNSPD tests.

**Wafer jobs** use the run GDS, `gds/run_<name>.gds`: one MLA job per layer and one EBL job for L20, writing only the run's block at the wafer centre (`mask_list.md` section 3).

### A.1 Resolved in the GDS (v2, carried into v3)

| # | Was | Now in the GDS |
|---|---|---|
| A1 | L1 marks under M1 Al | 300 × 300 µm M1 cut-outs at every mark site (trap die: edge notches at (±4300, ±4830); test die: (−1700, ±1080), (4300, ±1080)) |
| A2 | No EBL marks on L22 | 20 µm L22 crosses (2 µm arms) at (0, ±700) and (600, ±700) around the readout zone, plus one at every mark site |
| A3 | No protect layer for the gap etch | L45 PROTECT is drawn: every bond/probe D2 opening + 10 µm, readout window + 2.5 µm, SNSPD-lead branch region at the left end (x = −4835 … −4430, \|y\| ≤ 330). On the test die also the T3 and T4/T4b areas. Used in step 16a. **In v3 the window patch is essential**: with no ITO, nothing else stops the gap etch going down through the window SiO₂ toward the NbN |
| A4 | Ground fill had no bond pad, and no link to M1 | GND-1…4 bond spots on the fill, listed in `*_pads.csv`. **Step 22 (v3, 2026-11-08):** eight L40 vias under the fill tie it to M1 on chip, as Hampel 2023 grounds its mirror. M1 no longer depends on a bond wire to stay grounded; the M1-1…4 openings remain as a backup |
| A5 | No probe-able buried-ITO → Al test | Moot in v3 (no ITO); T7 removed |
| A6 | Top-ITO radial edges flush with the centre-DC Au edge | Moot in v3 (no ITO) |
| A7 | Single die only | Full-wafer reference `gds/make_wafer.py` → `wafer_v3.gds` (56 dies); R&D run layouts `gds/make_run.py` → `run_R1_TRAP.gds`, `run_R1_FULL.gds` (8 dies each, section A.3) |

### A.2 Still open

| Item | Why it matters | Action |
|---|---|---|
| Witness wafers W1–W6 (section E) | Most [verify] values in steps 5–16 depend on them; W3 rehearses steps 9–18 | Run W1-a/b, W2 and W3 before the device wafer |
| NbN recipe and tool access (step 5) | Flows, power and pressure were not retrieved; RF-bias AJA access is unconfirmed | Get the Dane 2017 recipe from the Berggren group |
| Plating bath (step 14) | Whether Plating-U04 has a gold tank, and its chemistry, are unverified | Ask staff; W5 |
| BOE undercut (step 16) | Not in run 1: it attacks Al and Ti, and the SNSPD leads sit 1.5–1.7 µm inside the centre-DC Au edge | W6 only if an undercut is ever wanted |
| L22 ↔ L50 overlay | Near the readout the L22 leads are 1.5–1.7 µm inside the centre-DC Au edge, so the overlay must hold ±1 µm | Overlay check after step 13 |
| Bare SiO₂ under the ion (v3) | The window floor is exposed SiO₂: it can charge from scattered laser light and is not screened against SNSPD click kicks (Todaro Supp.; Hampel 2023; DESIGN_LOG step 5) | Compare stray-field drift over the window with NODET in run 1b |
| HS50 mark recognition | The L22 crosses are 20 µm with 2 µm arms; the HS50 auto-alignment may want another shape | Ask EBL staff [verify] |


### A.3 R&D run plan at MIT.nano

The work is organised as a series of short, cheap runs with the layout updated between them, not as one production wafer. Each run is a full 100 mm wafer with only a central block written (`gds/make_run.py`, `mask_list.md` section 3). The MLA is maskless, so changing the GDS between runs costs nothing.

| Run | Layout | Process | Main questions | Feeds the next run |
|---|---|---|---|---|
| **0: short loops** | pieces or spare wafers | section E (W1–W6) | NbN on the real stack; HSQ dose; D2 stress and the full D2-to-dicing rehearsal (W3); plating | Recipes, dose, etch times |
| **1a: trap only** (`run_R1_TRAP`, run sheet `RUNSHEET_R1_TRAP.md`) | 6 NODET + 2 trap-only test dies (T1, T2, T6) | Steps 0–3, 9, 11–19. Skip 4–8 and the L20/L22 jobs. No EBL. | Plating, gap etch, leakage and breakdown (`test_plan.md` a1–a5), trapping, transport, heating rate | Trap process frozen; NODET becomes the reference die |
| **1b: full stack** (`run_R1_FULL`) | 2 A30, 2 B60, 2 NODET, 2 TEST | All steps | T8 dose array → nominal dose; T3/T4/T4b Tc, Isw and efficiency; SNSPD with RF on; ion over the window compared with NODET | Dose, spacer and cap thicknesses, die mix for run 2 |
| **2+** | edit `RUNS` in `make_run.py` | All steps | Whatever 1a/1b leave open, plus any `SIMPLIFICATIONS.md` variant worth trying | – |

**The team chose 1a first (2026-11-02).** `RUNSHEET_R1_TRAP.md` is the streamlined sheet for it.

**Facility questions to settle with MIT.nano staff before run 1** (all [verify]):
- **Gold.** Which tools accept wafers carrying Au. The D2 gap etch (step 16), the L45 resist step, the probe station and the dicing saw all come *after* plating.
- **NbN.** Which sputter tool and recipe (Dane 2017 is a Berggren-group process), and whether access goes through that group.
- **Plating.** Whether a gold plating tank exists, its chemistry, and its minimum plated area.
- **Holders.** Piece holders for the short loops.
- **Training and booking.** The order in which tool trainings must be done.

---

## B. One-screen process summary

| # | Step | GDS layer | Material | Target thickness | Tool (MIT.nano name where verified in the report) |
|---|---|---|---|---|---|
| 0 | Wafer prep, clean | – | HR FZ Si, 100 mm | 500–525 µm [verify] | Acid-Etch-General-* (piranha) |
| 1 | Alignment marks | 1 | Si etch | ~1 µm deep | DirectWrite-MLA150-*; RIE-F-Samco-230iP |
| 2 | Thermal oxide D1, both sides | – | SiO₂ | 1.0 µm | Ox-Tube-Lindberg / Tube-OxAnneal-Expertech-CTR200 |
| 3 | M1 ground plane + mirror | 10 | Al-1%Cu | 150 nm | Sputter-AJA-*; MLA150; RIE-Cl2-SAMCO-200iP |
| 4 | Spacer | – | PECVD SiO₂ | 238 nm | PECVD-Samco-PD220 or PECVD-Oxford-TEOS |
| 5 | NbN film | – | NbN | 7 nm | Berggren-group AJA (RF substrate bias) [verify access] |
| 6 | SNSPD leads + EBL marks (lift-off) | 22 | Ti/Au | 10 / 350 nm | MLA150; EBeam-Temescal-FC2800 |
| 7 | Nanowire EBL + CF₄ etch | 20 | HSQ on NbN | HSQ 50–70 nm spun | EBL-Elionix-HS50; RIE-PlasmaTherm-210RL |
| 8 | Cap | – | PECVD SiO₂ | HSQ + cap = 80 nm over the wires | PECVD (as step 4) |
| 8a, 8b | *removed in v3* (were the M1 via and buried ITO) | – | – | – | – |
| 9 | D2 | – | PECVD SiO₂ | 10.0 µm front + backside compensation | PECVD; Filmstress-Tencor-FLX2320 |
| 10 | *removed in v3* (was the top ITO) | – | – | – | – |
| 11 | D2 openings | 40 | – | etch ~10.3 µm | MLA150; RIE-F-Samco-230iP / RIE-PlasmaTherm-210RL |
| 12 | Plating seed | – | Ti/Au | 15 / 50 nm | Sputter-AJA-* |
| 13 | Plating mold | 50 | AZ nLOF 2070 | ≥ 8 µm | MLA150 |
| 14 | Au electroplating | 50 | Au | 6.0 µm | Plating-U04 [chemistry unverified] |
| 15 | Strip, seed removal | – | – | Au 50 nm, Ti 15 nm removed | Asher-*; Clean-Ar-Plasma [verify it can ion-mill]; RIE-F |
| 16a | Protect resist | 45 | thick positive resist | ≥ 10 µm | MLA150 |
| 16 | Au-masked D2 gap etch | – (L50 is the mask) | – | etch ~9.6 µm, stop 0.75 µm above M1 | RIE-F-Samco-230iP |
| 17 | RT wafer-level electrical test | – | – | – | ProbeStation-Summit-11000 |
| 18 | Protect, dice | 101 | – | 10 × 10 mm trap dies, 10 × 2.5 mm test dies, 200 µm streets | Diesaw-DAD3240 |
| 19 | Package, wire bond | – | Au / Al wire | – | Wirebond-Wedge / Wirebond-Ball-MEI |

---

## C. Final cross-section under the readout window (bottom to top)

All values are DESIGN_LOG steps 2, 6, 9, 9b and 10.

| Layer | Thickness | Role / note |
|---|---|---|
| HR FZ Si | ~525 µm [verify] | RF substrate loss largely irrelevant under the Al plane (Romaszko 2020 Sec. 3.2; Leibrandt 2009) |
| Thermal SiO₂ (D1) | 1.0 µm | Isolation; also on the backside |
| Al-1%Cu (M1) | 150 nm | Ground plane and optical mirror; ≥ 100 nm is opaque (TMM: 50 nm transmits 0.12 %) |
| PECVD SiO₂ spacer | 238 ± 10 nm | Second-order cavity spacer. 64 nm (first order) is optically equal but sits closer to Al hillocks. **Avoid ≈ 148 nm** (absorption node) |
| NbN meander | 7 nm; 100 nm wires on 200 nm pitch | 150 lines, 30 × 30 µm (A30) or 60 × 30 µm (B60) |
| HSQ (on wires only) + PECVD cap | 80 ± 10 nm total over the wires | Cap thickness = 80 − measured remaining HSQ |
| PECVD SiO₂ (D2) | 10.0 µm | Stays over the detector. Its top surface is the window floor the ion sees (bare SiO₂) |
| Au walls (centre DC, 5 µm rims) | 6.0 µm | Window 30 × 30 µm (A30) or 60 × 30 µm (B60); pocket depth 6 µm |
| Vacuum; ion | h ≈ 50.1 µm above the Au top, minus the 3-D recess effect over the bare-SiO₂ window: −1.38 µm (A30), −2.50 µm (B60) (DESIGN_LOG step 17) | – |

Expected NbN absorption ≈ 0.40 (worst ±10 nm corner 0.39) with no ITO, vs 0.53 for the v2 two-ITO stack. The model reads ~10 % pessimistic against Hampel. These are TMM effective-medium numbers, not RCWA (DESIGN_LOG steps 9b and 17).

Under the trap electrodes elsewhere: Si / D1 / M1 / spacer / cap / D2 / Ti-Au seed / 6 µm Au. Ground is ~10.3 µm below the Au. The same Al is the SNSPD mirror (238 nm below the NbN) and the RF ground plane (10.3 µm below the Au). Section H.0 explains why both need the thick D2.

---

## D. Thermal budget

| Step | Max T | Time at T | Note |
|---|---|---|---|
| 2 Thermal oxide | ~1000–1100 °C [verify furnace recipe] | hours | Before Al and NbN, so no limit applies |
| 3 Al sputter | < 100 °C [verify] | min | – |
| 4 Spacer PECVD | ≤ 300 °C | ~5 min | First anneal of the Al |
| 5 NbN sputter | ~RT (unheated; plasma heating unquantified) | min | Dane 2017 recipe is unheated |
| 6, 7, 11, 13 resist bakes | ≤ 115 °C (HSQ bake per datasheet [verify]) | min | – |
| 8 Cap PECVD | ≤ 300 °C | min | – |
| 9 D2 PECVD (front + back) | ≤ 300 °C | cumulative ~1–2 h [verify rate] | Hottest long step after Al and NbN. JoVE ran 350 °C; we cap at 300 °C because of the Al |
| 14 Plating bath | ~50–65 °C [verify bath datasheet] | ~30–60 min | – |
| 19 Die attach / bake-out | ≤ 150–200 °C [verify adhesive] | hours–days | Au–Al intermetallics on bakes [inference] |

| Limit | Value | Source |
|---|---|---|
| Al hillocks / voids | significant at ~350 °C; Al-1%Cu or a Ti/TiW cap suppresses them | SINTEF; JoVE M1 step ("prevent whisker formation during bakeout") |
| **Rule for this run** | **≤ 300 °C for every step after step 3** | team inference from the two lines above |
| NbN, inert ambient | Tc stable to 500 °C | arXiv:2501.07780 |
| NbN, uncapped in O₂ | Tc drops | Ioffe paper (research report) |
| NbN in air | Nb₂O₅ grows as d_ox = 0.78 t^0.17 nm (t in days): ~0.8 nm after 1 day | Medeiros 2019 |

---

## E. Witness wafers and short loops to run first

Run these before committing the device wafers. W3 is the most valuable: it rehearses steps 9–18 with no NbN.

| ID | Short loop | Stack / steps | Measure | Go / no-go |
|---|---|---|---|---|
| W1-a | **NbN on spacer-over-Al** | Si / 1 µm ox / 150 nm Al-1%Cu / 238 nm spacer → NbN 7 nm, co-loaded with a thermal-SiO₂/Si chip (Medeiros ellipsometry model) | AFM on the spacer before NbN (hillocks, roughness); NbN thickness by ellipsometry; Rsq (4-pt); Tc (dipstick / PPMS [verify access]) | Rsq ≈ 400 Ω/sq ± 15 % [team calc]; Tc ≥ 7.5 K on both pieces [verify]; no hillocks > 100 nm [verify] |
| W1-b | NbN thermal history | W1-a pieces with HSQ / cap → 5 × D2-equivalent PECVD cycles at 300 °C | Rsq and Tc again | ΔTc ≤ 0.3 K, ΔRsq ≤ 10 % [verify] |
| W2 | **HSQ dose test** on the real stack (Al / spacer / NbN) | Dose matrix (mask_list L20); salty vs TMAH develop; CF₄ 2.0 / 2.5 / 3.0 min | SEM linewidth; remaining HSQ thickness (needed for the cap thickness); RT R of test meanders | 100 ± 10 nm lines, no bridges, no breaks; R / R_expected 0.8–1.3 |
| W3 | **D2-to-dicing rehearsal** (no NbN) | Si / thermal SiO₂ / Al / SiO₂ spacer / SiO₂ cap / 10 µm D2 (+back) / L40 / seed / L50 / plate / seed removal / L45 / gap etch / dice | Bow per D2 increment; D2 BOE rate and index; L40 profile; plating thickness and roughness; seed-removal roughness; gap-etch rate, uniformity and profile (SEM cross-section); Au redeposition on sidewalls; T1/T2/T6/T7 on the test dies; Al pad bondability (pull test); **fill-to-M1 via contact** (step 22): resistance through a via with and without the step-12 Ar pre-clean, plus a cross-section of the seed and Au on the via sidewall | See `process_checks.md`; via link < 10 Ω (`test_plan.md` a13) |
| W5 | Plating test | Seed + nLOF mold (real L50) + 6 µm Au on a W3 wafer or a bare-oxide wafer | Current calibration; thickness map; AFM roughness; gap width top/bottom | 6.0 ± 0.5 µm; roughness ~8 nm rms after seed removal (PTB 8.3(5) nm) |
| W6 | Optional BOE | Al / Ti coupons in 6:1 BOE for 10–60 s | Etch rates | Only if an undercut is ever wanted (step 16 note) |
| W7 | **Bond-and-leak** (step 21) | W3 test-die T2 (Au / D2 / M1 capacitor) and plated Au pads, with the planned wire, tool and force | Au-to-M1 leakage at ≤ 1 V before and after bonding; pull / shear | No leakage change (> 1 GΩ) [verify]. If bonding opens a leak, cut the Al out under the DC pads next revision (keep it under the RF pad). Shorts under bond pads: Leibrandt 2009 (thin Si₃N₄) |

---

## F. Steps

Each step lists: Purpose · Tool · Recipe · Target · Layer · Align · Inspect / go-no-go · Hazards. Sign-off line at the end of each.

### 0. Wafer prep and clean
- **Purpose:** clean HR FZ Si start (ρ > 10⁴ Ω·cm [verify spec sheet]).
- **Tool:** Acid-Etch-General-* hood.
- **Recipe:**
  - Scribe the ID on the backside edge.
  - Piranha 15 min (JoVE substrate step).
  - DI rinse, spin dry. RCA clean if the furnace rules require it before step 2 [verify MIT.nano furnace cleanliness rules].
- **Inspect:** particles under a darkfield microscope.
- **Also:** set aside **≥ 3 dummy Si wafers** for W1/W3/W5.
- [ ] Done — date: ____ operator: ____ notes: ____

### 1. L1 alignment marks (Si RIE ~1 µm)
- **Purpose:** permanent marks for every later layer.
- **Tool:** DirectWrite-MLA150 + RIE-F-Samco-230iP (SF₆/O₂ or a Si recipe [verify recipe name]).
- **Recipe:**
  - HMDS; positive resist ~1.3 µm (S1813-class [verify stocked resist]).
  - MLA expose L1 **drawn** (wafer job on the run GDS, `run_<name>.gds`); develop (TMAH developer is fine here); etch Si ~1 µm.
  - Strip in solvent + O₂ ash.
- **Target:** 1.0 ± 0.2 µm, by Dektak.
- **Layer / align:** L1; first layer, aligned to the wafer flat. Four crosses per die: trap dies (±2150, ±1080), test dies (−1700, ±1080) and (4300, ±1080), die coordinates; die centres in `run_<name>_map.csv`.
- **Inspect:** crosses sharp, depth recorded.
- **Hazards:** none (no metal yet). M1 is cut out 300 × 300 µm at every mark site (A1, resolved), so the marks stay visible through the oxides.
- [ ] Done — date: ____ operator: ____ depth: ____ notes: ____

### 2. Thermal oxide D1, ~1 µm, both sides
- **Purpose:** isolation under M1. The backside oxide also starts the stress balance.
- **Tool:** Ox-Tube-Lindberg or Tube-OxAnneal-Expertech-CTR200.
- **Recipe:** wet oxidation to 1.0 µm [verify time/T on the tool chart]. JoVE used 0.5 µm at 900 °C for 4.5 h plus 0.2 µm LPCVD SiN. Romaszko gives 1–2 µm as typical for D1.
- **Target:** 1.00 ± 0.05 µm, by ellipsometry on 5 points.
- **Inspect:** marks still visible as topography.
- **Hazards:** none.
- [ ] Done — date: ____ operator: ____ t_ox (5 pts): ____ notes: ____

### 3. M1 Al-1%Cu ground plane + mirror (L10)
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

### 4. PECVD SiO₂ spacer (238 nm)
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

### 5. NbN 7 nm, room-temperature RF-bias reactive sputter
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

### 6. Ti/Au SNSPD leads by lift-off (L22), BEFORE the nanowire etch
- **Purpose:** leads, pads and the EBL alignment crosses for step 7 (20 µm crosses, 2 µm arms: on trap dies at (0, ±700) and (600, ±700) around the readout zone, and one at every mark site on both die types). The Au protects the NbN contact region during the CF₄ etch. Todaro thickened his leads with 350 nm Au to avoid latching (Todaro Supp. "Trap fabrication").
- **Tool:** MLA150; EBeam-Temescal-FC2800.
- **Recipe:**
  - Litho: LOR + S1813-class bilayer, MLA expose L22 **drawn** [verify resist stock].
  - **Developer hazard:** CD-26 / AZ 300 MIF is 2.38 % TMAH. 25 % TMAH thins NbN by ~0.25 nm per minute and leaves an etch-blocking residue (Toomey 2018). Use the **shortest develop** that clears the LOR, then a **≥ 3 min running DI rinse** (standing DI does not work, Toomey Expt. 1), then IPA.
  - No-TMAH alternative: a PMMA bilayer written on the EBL and developed in MIBK:IPA [team inference].
  - Deposition: if the evaporator has an in-situ Ar ion clean, use a short one to remove NbOx at the contact [inference, verify]. Then Ti 10 nm / Au 350 nm (Todaro: 350 nm Au).
  - Lift-off: NMP or Remover PG at 60–80 °C. Short sonication is acceptable (Najafi 2015 sonicated 2 min).
- **Layer / align:** L22 → L1 (±1 µm; this sets the L22↔L50 overlay, see `mask_list.md`).
- **Inspect:** lift-off complete; no Au flags; leads continuous. Expected lead RT resistance ~0.1–0.3 kΩ per lead [team calc], negligible next to the meander.
- **Hazards:** TMAH (above). Bare NbN is exposed during the litho.
- [ ] Done — date: ____ operator: ____ develop time: ____ rinse: ____ t_Au: ____ notes: ____

### 7. EBL nanowire (L20): HSQ, salty develop, CF₄ RIE; HSQ left on
- **Purpose:** the meander and tabs (trap dies); the T3 bar and the T4/T4b meanders (test dies). Job contents in `mask_list.md` section 2.
- **Tool:** EBL-Elionix-HS50; RIE-PlasmaTherm-210RL (Toomey used a Plasma-Therm; that this is the same tool or recipe is [verify]).
- **Recipe:**
  1. HSQ spun to **50–70 nm**. Najafi 2015 used 70 nm. Because HSQ + cap must total 80 nm, a thinner HSQ (~50 nm) leaves room for a ≥ 30 nm PECVD cap. Bake per the HSQ datasheet [verify].
  2. Expose L20 **drawn**.
     - Najafi: 700–850 µC/cm² at 30 keV (Raith 150).
     - **Redo the dose test on the Elionix at its actual kV.** HS50 suggests 50 kV; if a 100/125 kV Elionix is used, the dose rises further. Expect roughly kV-proportional scaling [inference].
     - Matrix and PEC notes are in `mask_list.md`. Align to the L22 EBL crosses (A2, resolved).
  3. Develop in **salty developer (NaOH/NaCl)**, preferred over 25 % TMAH (proposed in Toomey 2018; its effect on NbN is not reported. Formulation and time [verify]). Then a ≥ 3 min running DI rinse, IPA, N₂ dry.
  4. CF₄ RIE at 50 W, 10 mTorr, ~2.5 min (Toomey 2018 for 5 nm). For 7 nm, use 2.5–3.0 min, set from W2 [verify].
  5. **Leave the HSQ on.** **No O₂ plasma** (it oxidises the NbN sidewalls).
- **Inspect:**
  - SEM: linewidth on T4/T4b (test dies); no bridges or breaks.
  - Room-temperature R at probe ≤ 1 V: main SNSPD (trap-die pads SNS/SNG), T4/T4b, and T3 4-wire (Rsq).
  - Expected meander R = N_sq × Rsq, with N_sq ≈ 45 400 (A30) or 90 400 (B60): **≈ 18 MΩ (A30) / 36 MΩ (B60) at 400 Ω/sq** [team calc from GDS].
  - Record R₀ (baseline for tracking). Also measure the remaining HSQ thickness on the W2 witness.
- **Go / no-go:** R / R_expected 0.8–1.3 [verify]. Open → die rejected. A low R means unetched bridges.
- **Hazards:** ESD on the open meander. Wear a grounded strap, probe with the SMU at 0 V, compliance ≤ 1 V / ≤ 100 nA [inference].
- [ ] Done — date: ____ operator: ____ dose: ____ etch time: ____ R₀ (A30 dies): ____ notes: ____

### 8. SiO₂ cap, PECVD, same day as step 7
- **Purpose:** protect and passivate the nanowire. This is the Todaro Supp. fix for 12–30 % R rises; Hampel used a 130 nm cap. Here it also sets the matching-layer phase.
- **Target:** cap = 80 nm − measured HSQ remaining, **≥ 30 nm** for sidewall coverage [inference]. HSQ + cap = 80 ± 10 nm. With no ITO the cap touches the D2 SiO₂, so its thickness barely matters optically (NbN absorption ≈ 0.40 for any cap; DESIGN_LOG step 17).
- **Tool:** PECVD at ≤ 300 °C. Measure the cap on a co-loaded Si piece (ellipsometry).
- **Hazards:**
  - The oxidising plasma meets the NbN sidewalls first. Hampel deposited PECVD directly on bare NbTiN without problems; there are no NbN data [inference].
  - From here until step 11 the pads are covered: **no electrical check is possible during steps 8–9**. Use the W1-b witness instead.
- [ ] Done — date: ____ operator: ____ t_cap: ____ HSQ (witness): ____ notes: ____

### 8a, 8b. Removed in v3
These were the L24 via to M1 and the L31 buried ITO. v3 has no ITO (DESIGN_LOG step 17); go from step 8 straight to step 9.

### 9. D2: 10 µm PECVD SiO₂ in increments, stress-balanced
- **Purpose:** RF-to-ground dielectric. V_b ≈ 503 V at 10 µm by Sterling's model [team calc]. Sussex measured > 250 V_amp at 8 µm.
- **Tool:** PECVD-Oxford-TEOS or PECVD-Samco-PD220 at **≤ 300 °C**; Filmstress-Tencor-FLX2320.
- **Recipe:**
  - Deposit in **1–2 µm increments with cool-down pauses** (Leibrandt 2009). JoVE ran ~300 nm/min at 350 °C [verify our rate at 300 °C].
  - **Interleave backside oxide** (JoVE put 14 µm on both sides). Example: front 2 µm → bow → back 2 µm → bow … to front 10 µm, back ~8–10 µm (tune from W3).
  - Do face-down runs only after ≥ 2 µm is on the front, with a clean platen [verify whether the tool allows face-down].
- **Why balance:** a 10 µm film at −200 MPa [assumed, verify] on 525 µm Si bows a 100 mm wafer by ~300 µm (Stoney) [team calc], which is too much for the MLA and EBL chucks.
- **Target:** front 10.0 ± 0.5 µm (reflectometer / ellipsometer [tool name not verified]); |bow| ≤ 50 µm [verify chuck limit]; no cracks or crazing.
- **Hazards:** heat on the Al (hillocks) and on the capped NbN. Micro-voids may outgas (Leibrandt).
- [ ] Done — date: ____ operator: ____ increments: ____ bow log: ____ t_D2: ____ notes: ____

### 10. Removed in v3
This was the L30 top ITO on D2. v3 has no ITO; go from step 9 straight to step 11.

### 11. L40 D2 openings (pads, M1 bond openings, fill-to-M1 ground vias, L50 alignment crosses)
- **Ground vias (step 22):** eight 150 × 150 µm openings per trap die, at (±4700, ±1000) and (±1000, ±2500), etched with everything else in this job. The plated Au ground fill covers them in step 14 (≥ 25 µm overlap all round), which ties the fill to M1 on chip. They need no L45 patch.
- **Tool:** MLA150; RIE-F-Samco-230iP or RIE-PlasmaTherm-210RL.
- **Recipe:**
  - Thick positive resist **≥ 8 µm** (AZ 10XT / AZ 4620-class [verify stock]). JoVE used 6 µm. Expose L40 **drawn**.
  - Etch with CHF₃ 25 / CF₄ 5 / Ar 50 sccm, 130 mTorr, 600 W, ~360 nm/min (JoVE) [verify on our tool].
  - Depth: ~10.36 µm over M1 (D2 + cap + spacer) and ~10.1 µm over the L22 pads, so ~29 min + 10–15 % over-etch. Run in ≤ 5 min segments with cool-down to save the resist [inference].
  - Stops on Al (AlF₃) and on Au.
- **Layer / align:** L40 → L1 (±5 µm).
- **Inspect:**
  - Dektak depth; clean metal at every opening floor, including all eight ground vias.
  - **First probe access since step 7:** meander R₁ (SNS/SNG) and T3/T4/T4b on the test dies.
  - SNSPD pads (both tied together) to M1 (any M1-n opening) at ≤ 1 V must read **> 1 GΩ** (no short through the spacer to the Al).
- **Hazards:** heat in the long etch. The window area is under resist here.
- [ ] Done — date: ____ operator: ____ etch time: ____ R₁: ____ SNSPD–M1: ____ notes: ____

### 12. Plating seed Ti 15 nm / Au 50 nm (PTB)
- **Tool:** Sputter-AJA-* (sputter for step coverage; PTB evaporated).
- **Ar pre-clean first (step 22):** an in-situ RF Ar sputter clean before the Ti, to remove the AlF₃ and native Al₂O₃ that the step-11 fluorine etch leaves on the Al at the ground-via floors. Without it the fill-to-M1 contact may be open. Wire bonds at M1-n break through this film; a sputtered seed does not [inference; verify the AJA has a substrate RF etch, and the time, on W3].
- **Sidewall coverage (step 22):** the seed must run continuously down the ~10.4 µm via wall, or the via floor is never plated and never connected. Sputtering with substrate rotation coats the wall thinly; the 15 nm Ti also sits between the Al and the Au, which slows Au–Al intermetallic growth [inference; verify by cross-section on W3].
- **Note:** the seed shorts every electrode and both SNSPD pads together. That is ESD-safe, but no electrical checks are possible until step 15.
- **Note:** the seed coats the window floor (SiO₂); it is removed in step 15.
- [ ] Done — date: ____ operator: ____ notes: ____

### 13. L50 plating mold (negative, ≥ 8 µm)
- **Tool:** MLA150.
- **Recipe:**
  - AZ nLOF 2070 at ≥ 8 µm (PTB thesis used nLOF 2070; spin curve [verify]). Mold ≥ 1.3 × the plating thickness [inference].
  - MLA expose L50 **inverted** (resist stays where there is no Au). PEB and develop per datasheet.
  - Short O₂ descum.
  - Leave the cathode contact points at the wafer edge free of resist.
- **Layer / align:** L50 → **L40 topography crosses** seen through the seed (±1 µm, critical).
- **Inspect:**
  - Window opening registered to the meander.
  - 5 µm gap lines clean down to the seed.
  - nLOF profile (re-entrant): record the gap width at the bottom.
- [ ] Done — date: ____ operator: ____ t_resist: ____ overlay (µm): ____ notes: ____

### 14. Au electroplating, 6 µm
- **Tool:** Plating-U04. **Whether it is a gold tank, and its chemistry, are not verified.** PTB used a sulfite bath (Enthone Microfab Au 100-B, pH 7.5, compatible with nLOF).
- **Recipe:**
  - Plated area ≈ 0.92 cm² per 10 × 10 mm trap die (Au fraction 0.916) and ≈ 0.17 cm² per test die (0.69 with T8; 0.21 cm² for the trap-only test die), so ≈ 5.9 cm² for `run_R1_TRAP` and ≈ 5.8 cm² for `run_R1_FULL` (8 dies each) [team calc from GDS]. Such a small plated area on a 100 mm wafer needs a low, well-calibrated current; confirm the tank's minimum on W5 with the same run layout [verify].
  - Current density per bath datasheet [verify]. At 3 mA/cm² and 100 % efficiency, Au(I) deposits ~0.19 µm/min, so ~32 min for 6 µm [team calc, Faraday].
  - Plate in two halves and measure in between.
- **Target:** 6.0 ± 0.5 µm (DESIGN_LOG step 2); ≤ 10 % across the wafer [verify]; no nodules.
- [ ] Done — date: ____ operator: ____ I / t: ____ thickness map: ____ notes: ____

### 15. Strip, descum, seed removal
- **Recipe:**
  1. Strip nLOF in hot NMP / Remover PG. Then O₂ plasma + F plasma for resist debris (PTB).
  2. **Ar ion etch of the Au seed** at ~50 nm/min (PTB): ~1 min + ~20 % over [verify that Clean-Ar-Plasma, or an Ar RIE recipe, actually mills].
  3. **F-plasma etch of the Ti** at ~10 nm/min (PTB): ~1.5 min + over.
- **Exposure notes:**
  - The bare SiO₂ window floor sees the F plasma and the end of the Ar etch; expect a few nm of SiO₂ loss there [inference].
  - The SNSPD L22 pads lose a few nm of Au.
  - Line-of-sight redeposition is unavoidable (Sussex).
- **Inspect:**
  - All electrodes isolated (neighbours > 100 MΩ at 10 V).
  - Meander R₂.
  - Window floor optically clean (no Au film).
  - AFM: Au roughness ~8 nm rms (PTB 8.3(5) nm).
- [ ] Done — date: ____ operator: ____ Ar time: ____ F time: ____ R₂: ____ notes: ____

### 16a. Protect resist (L45, drawn in the GDS, see A3)
- Thick positive resist ≥ 10 µm over the 6 µm topography. MLA expose **inverted** (resist stays on the L45 patches), aligned to L40/L50 (±2 µm).
- Covers, on trap dies: the four M1 openings + 10 µm; the SNSPD-lead branch region at the left end (x = −4835 … −4430, |y| ≤ 330: SNSPD pads, their D2 openings, and where the L22 leads leave the centre-DC lead); the readout window + 2.5 µm (onto the 5 µm Au rim).
- On test dies: every D2 opening + 10 µm; the T3, T4 and T4b boxes. T1, T2 and T6 are left open on purpose so they see the gap etch.
- **The window patch must not be dropped in v3.** With no ITO, the window is a hole in the Au etch mask, and the gap etch would go down through the 10 µm SiO₂ toward the NbN.
- [ ] Done — date: ____ operator: ____ notes: ____

### 16. Au-masked D2 gap etch
- **Purpose:** remove D2 from the electrode gaps so the ion does not see oxide; aspect ratio > 1 (Bautista-Salvador 2019).
- **Recipe:**
  - Same CHF₃/CF₄/Ar recipe as step 11.
  - Etch ~9.6 µm, stopping **~0.75 µm above M1** (Sussex: 750(250) nm, 4(1) % uniformity), so ~27 min at 360 nm/min [verify on W3].
  - Etch in segments; check depth on the T1 comb gaps (test dies) by Dektak / optical interferometry.
- **Exposure notes:**
  - The window is protected only by the 16a resist patch (no ITO in v3).
  - The L22 leads cross a 10 µm Au gap in two spots, where they leave the centre-DC lead at x ≈ −4455, |y| ≈ 20–30. Both spots are inside the L45 branch patch. Checked with gdstk: the only L22 not covered by Au, L40 or L45 are the EBL crosses and overlay squares at the mark sites, which are no longer needed. **If 16a is skipped**, the lead top at those spots is ~0.6 µm above M1, with ~0.15 µm of oxide left over it or none [team calc]; then stop at ≥ 0.9 µm.
- **Optional BOE undercut: NOT in run 1.**
  - BOE attacks Al and the Ti adhesion layer under the Au (W6).
  - Near the readout the SNSPD leads are only **1.5–1.7 µm inside the centre-DC Au edge** [GDS check]. A Sussex-style 3 µm undercut would reach them.
  - If it is ever used: dice first (JoVE), keep all windows and pads under resist, and keep the undercut < 1 µm.
- **Inspect:**
  - SEM on a sacrificial die or W3: gap cleared to target; no Au redeposition bridges on the sidewalls.
  - Strip the 16a resist (solvent + O₂ ash; NbN is buried).
  - Meander R₃.
- [ ] Done — date: ____ operator: ____ etch time: ____ depth: ____ R₃: ____ notes: ____

### 17. Room-temperature wafer-level electrical test (before dicing)
- Protocol in `test_plan.md` (a): Dietl 2025 limits, Stick > 100 MΩ.
- Record pass/fail per die against the die IDs in `gds/run_<name>_map.csv`. Test dies (T1–T8) stand in for the trap dies of their run. Dies that fail go to destructive tests: T1 flashover, cross-sections.
- [ ] Done — date: ____ operator: ____ yield: ____ notes: ____

### 18. Protect, dice (10 × 10 mm trap dies, 10 × 2.5 mm test dies), strip
- **Recipe:**
  - Protective resist ≥ 8 µm (covers the 6 µm Au).
  - Diesaw-DAD3240 with a Si blade, on the L101 outlines [verify blade / recipe with staff]. x streets on a 10.2 mm pitch run straight through. The y streets follow the stacked column (10 mm trap dies and 2.5 mm test dies, `make_run.py` / `make_wafer.py`); all columns use the same stack, so the y cuts also run straight through. Streets are 200 µm wide. The kerf plus chipping must fit in the 200 µm street [verify blade width].
  - Remove the tape in acetone (JoVE), then acetone/IPA strip.
  - **No ultrasonic** [inference].
- **Inspect:** chipping < 50 µm [verify] (the Au is pulled back 100 µm and M1 150 µm from the die edge); meander R₄.
- **Hazards:** ESD from the saw spray. Use the saw's standard CO₂-bubbled DI [inference, verify].
- [ ] Done — date: ____ operator: ____ notes: ____

### 19. Package
- **Carrier:** the lab's carrier, or a 100-pin CPGA with a spacer (Stick 2010; Leibrandt 2009) [verify which carrier the cryostat takes].
- **Die attach:**
  - Cryo-compatible epoxy cured ≤ 150 °C [verify product/cure], e.g. EPO-TEK 353ND as listed by JoVE.
  - Au/Sn (Leibrandt) needs a metallised backside, and ours is oxide.
- **Wire bonds:**
  - Au wire on the Au pads (Wirebond-Wedge or -Ball).
  - On the **Al M1 openings use Al wedge wire**, to avoid Au–Al intermetallics on bakes [inference; research notes Q9].
  - Openings are 170 × 170 µm (M1) and 150 × 120 µm (SNSPD, grown from 120 × 90 in step 21) at the bottom of 10 µm wells; get the MIT.nano wedge/capillary part number and draw it to scale in the wells [verify]. The Au pads are 120 × 200 µm on the top/bottom edges and 200 × 200 µm for RF and C, with the Au ground fill held ≥ 30 µm away (step 21).
  - **Wedge-bond the SNSPD pads; no ball bonding there** (the ball bonder's flame-off spark is a risk to electrically sensitive devices: EPFL CMi HB10 guidelines) [inference for NbN].
  - **RF pad: 2–4 wires** in parallel (Sandia Phoenix/Peregrine bonds RF with 7 wires, arXiv:2009.02398 Sec. 5.3; `research/reports/Bond pad sizing for ion traps.md`).
  - **Probe at one end of each 200 µm pad and bond at the other** (step 17 probe marks can hide pad damage) [inference].
  - Plated Au must be wire-bond grade (soft, ≈ ≤ 90 Knoop, vendor figure) [verify with MIT.nano for the bath, or test-bond W5 coupons with and without an anneal].
  - **Bond the Au ground fill to carrier ground at GND-1…4, ≥ 2 of them (A4).** The step-22 vias tie the fill to M1 on chip. Also bond ≥ 1 M1-n opening (Al wire) as a backup; it is **required** on any die whose step-17 ground-link test (`test_plan.md` a13) failed.
  - Bond off the top/bottom edges for the four pad rows, off the right edge for RF (4700, 0), and off the left edge for C and the SNSPD pads. Pads stay at |x| ≤ 3.5 mm on the top/bottom edges and near y = 0 on the side edges, away from the beam exits near the corners (|x| or |y| ≈ 4.7 mm). Keep the loops low anyway.
  - Bond the SNSPD pads last, wearing a strap. Short the carrier SNSPD pins until installation [inference].
- **Bond map** (from `gds/trap_die_v3_A30_pads.csv`, identical for B60; fill in the carrier pin column). Rows run along y = +4720 (T) and y = −4720 (B) at a 180 µm pitch: TL1 … TL8 at x = −3500 … −2240, TR1 … TR9 at x = +3500 … +2060 (same x for BL / BR).

| Chip pad | Electrode | Role | Layer | Wire | Carrier pin |
|---|---|---|---|---|---|
| TL1 | 33 | top cap left | 50 | Au | |
| TL2–TL8 | 3 → 9 | top segments, −1000 … −400 µm from readout | 50 | Au | |
| TR1 | 34 | top cap right | 50 | Au | |
| TR2–TR9 | 17 → 10 | top segments, +400 … −300 µm from readout | 50 | Au | |
| BL1 | 35 | bottom cap left | 50 | Au | |
| BL2–BL8 | 18 → 24 | bottom segments, −1000 … −400 µm | 50 | Au | |
| BR1 | 36 | bottom cap right | 50 | Au | |
| BR2–BR9 | 32 → 25 | bottom segments, +400 … −300 µm | 50 | Au | |
| C | 2 | centre DC, (−4650, 0) | 50 | Au | |
| SNS | SNSPD_S | SNSPD signal, (−4750, +260) | 22 | Au | |
| SNG | SNSPD_G | SNSPD return, (−4750, −260) | 22 | Au | |
| RF | 1 | RF, (4700, 0) | 50 | Au | |
| M1-1…4 | ground plane (tied to the fill on chip by the step-22 vias) | Al through D2, (±4700, ±2000); ≥ 1 bond as a backup | 40 | **Al** | |
| GND-1…4 | Au ground fill | (±4700, ±1500); ≥ 2 bonds | 50 | Au | |

- **After packaging:** repeat the pad-to-pad isolation through the carrier pins, plus meander R₅.
- [ ] Done — date: ____ operator: ____ carrier: ____ notes: ____

---

## G. Substrate deltas (sapphire, fused silica)

The Al ground plane makes RF substrate loss largely irrelevant (Romaszko 2020 Sec. 3.2; Leibrandt Q 100 → 150 with the ground plane). The NbN always grows on the PECVD spacer, so the substrate does not change NbN growth. What changes is handling.

| Step | Sapphire | Fused silica |
|---|---|---|
| Wafer sensing (loadlocks, MLA, EBL height sensor, PECVD/RIE wafer-present sensors) | Transparent wafers are often not detected or focused. Dietl 2025 used a **temporary 2 µm backside poly-Si** for handling on fused silica. For us a permanent backside coating (poly-Si by LPCVD before step 3, or a metal) is fine because nothing is imaged through the back [verify tool rules]. MLA150: use the AirAF variant on transparent substrates [verify] | same |
| 1 Marks | The Si RIE does not apply. Use Ti/Au or Cr/Au lift-off marks, or a Cl₂/BCl₃ sapphire etch (slow) [verify] | CHF₃/CF₄ RIE 1 µm into the glass, or metal marks |
| 2 D1 | No thermal oxide: use PECVD SiO₂ 1 µm, or skip | Optional (the substrate is already SiO₂) |
| 9 D2 stress | Sapphire CTE ≈ 7–8 ppm/K vs SiO₂ ≈ 0.5: extra thermal stress on cooldown [verify]. Re-tune the backside balance on a witness | Good CTE match; intrinsic PECVD stress still needs balancing |
| Ellipsometry | Over the M1 area the stack is opaque, so measure there. On transparent areas, backside reflections spoil the fits | same |
| EBL charging | No issue: the blanket NbN film and Al are conductive at step 7. Ground them through the clip | same |
| 5 K thermal | Sapphire conducts heat well | Glass conducts poorly. RF heating of the SNSPD (Hampel's residual limit) is worse [inference] |
| 18 Dicing | Hard: diamond blade, slow feed [verify] | Dedicated glass blade [verify] |

---

## H. Variant: Hampel-style local mirror, no D2 (not the baseline; no GDS yet)

Team request, 2026-11-08 (DESIGN_LOG step 23). This is an **alternative** to sections B–F, kept here so the two can be compared. The baseline stays the die-wide M1 ground plane under 10 µm D2. Nothing in the GDS implements this variant yet (H.5).

**Idea.** Follow Hampel 2023: the Al sits only under the SNSPD and along its leads, never under the RF rails. The electrodes then sit directly on the thin optical stack, and the 10 µm D2, plating and gap etch all go away. A die-wide Al plane under electrodes on that thin stack would give C_RF–ground ≈ 127 pF instead of 2.9 pF (DESIGN_LOG step 22) [team calc]. That is why the mirror has to be local.

### H.0 Why the baseline has a thick D2: ground plane and mirror together

The Al does two jobs, and each one depends on a different distance:
- **Mirror:** the Al-to-nanowire distance. This is the 238 nm SiO₂ spacer, fixed by the 493 nm cavity phase (DESIGN_LOG steps 9 and 9b).
- **RF ground plane:** the Al-to-electrode distance. The RF Au and the Al form a parallel-plate capacitor, C = ε·A/d. The rail area is fixed (0.877 mm² on A30), so d is the only free parameter. A thicker D2 also raises the RF breakdown voltage.

| Stack | Ground plane under the RF | SNSPD mirror | C_RF–ground; RF current at 53 V, 28 MHz [team calc] | Cost |
|---|---|---|---|---|
| **Baseline: thick D2** (sections B–F) | Yes | Yes | 2.9 pF (10.3 µm SiO₂); ≈ 27 mA | 10 µm D2, plating, gap etch. The detector sits under a 6 µm-deep window; the ion drops 1.38 µm (A30) over the window (step 17). The window floor is bare SiO₂ |
| Thin stack, die-wide Al (FabuBlox flow as drawn) | Yes, but too close | Yes | 127 pF (238 nm SiO₂); ≈ 1.2 A | The RF resonator cannot drive it; loss and breakdown in the SiO₂ |
| **Thin stack, local mirror** (this section) | No | Yes | Only the rail-to-Si capacitance, not computed | Needs Si with ρ > 20 kΩ·cm; the RF over that Si is NIST practice (Todaro, Hampel). Exposed SiO₂ in every gap unless the electrodes are plated thick, as Todaro's 6 µm were (H.4, option E2). Simpler process |

The choice is therefore between process complexity and the ground plane. A thick D2 gives both the plane and the mirror; a thin stack keeps the mirror only by removing the Al from under the RF rails. On Si with ρ > 20 kΩ·cm, dropping the plane is what NIST does (Todaro, Hampel). The 10 µm D2 is the standard surface-trap ground-plane stack (Romaszko 2020 Fig. 3.1; JoVE; Stick 2010; Leibrandt 2009; Sterling 2014 with 10 µm of buried SiO₂).

The thickness of the SiO₂ under the electrodes changes the load on the RF drive and the field inside that SiO₂. It does not change the trapping field at the ion, which the electrode widths set.

### H.1 Mirror size

Hampel gives no dimensions. Measured from Hampel Fig. 1 (arXiv v1, p. 2) against its 20 µm and 100 µm scale bars [team calc]. The 20 × 30 µm SNSPD outline measures 20 × 30.5 µm, which checks the scale.

| | Hampel, small mirror | Hampel, large mirror | **This variant (proposal)** |
|---|---|---|---|
| Along the leads | ≈ 64 µm: 13 µm behind the active area, 20 µm forward under the lead start | ≥ 270 µm along the lead channel; runs ≈ 160 µm past the RF-rail ends | Small part: x = 265 … 328 (X_READ = 300; the meander tabs end at x = 245). Large part: continues under the leads to x ≈ −2400, i.e. ≈ 400 µm past the RF open end at x = −2000 |
| Across | 37–49 µm (visible edge to the black RF gaps) | ≈ 35–50 µm | **\|y\| ≤ 20 µm (40 µm)**: under the centre DC only. Our RF rails start at \|y\| = 25, so 50 µm is the hard limit |
| Margin around the detector | 8–15 µm on the long sides | – | **5 µm** on the long sides (detector \|y\| ≤ 15). Narrower than Hampel's because our channel is 50 µm wide |
| Under the RF rails | No | No | No, by construction |
| Ground | CHF₃ vias + 20 nm Au, "via the trap electrodes" | same | Widen the far end (x ≈ −2500 … −2300) to reach under the Au ground fill and put the via there (H.2 step 11v). Exact spot to be checked in the GDS: the fill must enclose it ≥ 25 µm, as in step 22 |

Capacitance the mirror adds to the centre DC (electrode 2), which sits 318 nm above it (spacer + HSQ/cap): 40 µm × ≈ 2.73 mm ≈ **12 pF** [team calc, ε_r 3.9]. That is harmless on a filtered DC line [inference].

### H.2 Steps (changes against section F)

| Step | Baseline | Variant |
|---|---|---|
| 0–2 | Prep, L1 marks, 1 µm thermal SiO₂ (D1) | Same |
| **3v** | L10 inverted: die-wide plane | **L10 drawn: local mirror only**. Al-1%Cu 150 nm (opaque; Hampel used 50 nm e-beam Al). Either the step-3 etch with the job not inverted, or lift-off as Hampel did. No mark cut-outs needed |
| 4–8 | Spacer 238 nm, NbN, L22 leads, L20 nanowire, HSQ + cap | Same order: leads before the nanowire, cap straight after. **The cap is now the top surface over the detector (vacuum above)**, so its thickness matters optically again: rerun 09b before fixing it (H.4) |
| 9, 10 | 10 µm D2 | **Skipped** |
| **11v** | L40 through ≈ 10.4 µm D2 | **L40 through the thin stack only.** Mirror ground via: HSQ/cap + spacer ≈ 0.32 µm down to the Al. SNSPD pads: ≈ 80 nm down to the L22 Au. Thin positive resist (~1.3 µm); same CHF₃/CF₄/Ar chemistry, ≈ 1 min [verify]. Stops on Al and Au. Add a small Al probe opening on the mirror so it can be checked electrically (H.5) |
| **12v–15v** | Seed, nLOF mold, 6 µm plating, seed removal | **Ti/Au lift-off electrodes, L50 drawn**: LOR + positive resist, MLA. In-situ Ar pre-clean before the Ti (AlF₃ on the via floor; step 22). Ti 10 nm / Au 350 nm (Hampel 350 nm) [verify thickness]. Lift-off in NMP. Option E2: keep steps 12–15 as written and plate 6 µm on the thin stack; the cap protects the NbN under the plating resist (Todaro's damage step) [inference] |
| 16a, 16 | L45 protect, gap etch | **Skipped** (no D2 to clear) |
| 17–19 | Test, dice, package | Same, except: no M1 bond openings (the mirror is grounded through the fill); test fill ↔ mirror probe pad < 10 Ω; check that 350 nm evaporated Au wedge-bonds [verify] |

Thermal budget: no D2, so the long 300 °C exposure goes away.

### H.3 Cross-section under the readout window (variant)

HR Si / 1 µm thermal SiO₂ / 150 nm Al (local mirror) / 238 nm PECVD SiO₂ / 7 nm NbN / 80 nm HSQ + PECVD SiO₂ cap / **vacuum**. The window is a 30 × 30 µm hole in 0.35 µm Au. The ion sees the cap directly. Away from the detector the electrodes sit on spacer + cap over D1, with no Al under them.

### H.4 What the variant changes in the physics (each needs a rerun or a test)

- **RF over thin SiO₂ on HR Si, with no ground plane.** This is proven NIST practice, not an open risk. Todaro trapped on 6 µm plated Au over 134 nm PECVD SiO₂ on intrinsic Si, ρ > 20 kΩ·cm, with no ground plane, and reached days-long lifetimes and F = 0.9991. Hampel used the same kind of substrate. The ground plane in the baseline comes from the Romaszko/JoVE flow (Romaszko 2020 Sec. 3.2; Leibrandt 2009: Q 100 → 150 with the plane), which guards against substrate loss. **Condition: order Si with ρ > 20 kΩ·cm, as NIST did.** The baseline step 0 asks only for > 10⁴ Ω·cm. Measuring the resonator Q with the die mounted is still worth doing.
- **Exposed SiO₂ in every gap.** 0.35 µm Au over 5 µm gaps gives a depth-to-width ratio of 0.07, against ≥ 1 recommended (Bautista-Salvador 2019). The ion sees SiO₂ along the whole trap, not only at the window. Todaro trapped on the same NIST design with 6 µm electrodes; Hampel's paper reports no trapping. Option E2 (plated 6 µm) raises the ratio to 1.2.
- **Optics (09b).** Rerun with vacuum above the cap instead of 10 µm SiO₂.
- **Ion height and recess (04b, 12).** Set `metal_thickness` to 0.35 (or 6 for E2) and `ground_depth: null` (no buried ground) in the `_sim.json`. The window recess shrinks from 6 µm to 0.35 µm, so the 1.4 µm height drop over the window should shrink as well [inference; rerun 04b].
- **RF pickup (10).** Rerun with a local mirror, no D2, and the rail 5 µm laterally from the mirror edge.

### H.5 GDS changes needed (not made)

A `--localmirror` flag in `make_chip.py` would need:
- L10 = the H.1 mirror shape, not the die-wide plane;
- L40 = the mirror ground via + SNSPD pad openings + a mirror probe opening only (no M1 bond openings, no fill-to-M1 vias);
- no L45;
- `_sim.json` stack per H.4;
- **a lead-routing decision.** The L22 leads now run under the centre DC with only ≈ 80 nm of HSQ/cap between them and the Au, over ≈ 2.3 mm inside the trap and ≈ 2.6 mm under the centre lead. A pinhole anywhere shorts the SNSPD to electrode 2. Either (a) move the leads into the electrode layer, in a slot cut along the centre DC (Hampel's Fig. 1 layout; a GDS change and a new five-wire geometry to simulate), or (b) keep them buried and thicken the SiO₂ over the leads only [inference; adds a step].
- `check_chip.py` rules for the above.
