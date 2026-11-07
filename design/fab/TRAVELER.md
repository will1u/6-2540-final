> **Claude-authored.** Run sheet (traveler) for the v2 narrow dies `gds/trap_die_v2_A30.gds` (A30), `gds/trap_die_v2_B60.gds` (B60) and `gds/trap_die_v2_NODET.gds` (plain trap), and the test die `gds/test_die_v2.gds`. Each R&D run writes a small block from `gds/run_<name>.gds` (section A.3); `gds/wafer_v2.gds` is the full-wafer reference. It turns DESIGN_LOG steps 0–10 and 9b plus the research report (`research/reports/Trap integrated SNSPD design.md`) into a step list. It is a starting recipe, not a qualified process: every number marked **[verify]** is an inference, a tool setting nobody has checked, or a value that needs a witness wafer. Companion files: `mask_list.md`, `process_checks.md`, `test_plan.md`.

# Traveler: Ba⁺ surface trap with integrated NbN SNSPD, 100 mm HR float-zone Si

Wafer ID: ________ Run layout: `run_________.gds` (R1_TRAP / R1_FULL / other) Generator versions / date: ________ Start date: ________ Operator: ________

Source shorthand: JoVE = Hong 2017 (JoVE 56060); PTB = Bautista-Salvador 2019 (NJP 21, 043011) and Bautista-Salvador thesis 2015; Sussex = Siegele-Brown 2022; Todaro = Todaro 2021 PRL + Supp.; Hampel = Hampel 2023 (APL 122, 174001). "[team calc]" = computed for this project, not from a paper.

---

## A. Die layout (v2) and tape-out status

The v1 square 10 × 10 mm die with the trap in a corner (`trap_chip_v1*.gds`) was rejected and is archived in `gds/archive_v1_square/`. Nothing in this traveler refers to it any more.

**Trap die floorplan** (`gds/make_chip.py`; checked with gdstk on `trap_die_v2_A30.gds` and `_B60.gds`, 2026-11-02). GDS µm, die centre at (0, 0):

| Feature | Location |
|---|---|
| Die (L101) | 10 × 2.5 mm: x = ±5000, y = ±1250 |
| Trap axis | die centre line, y = 0 |
| RF rails | x = −2000 … +2000, U closed at the right (+x) end; RF pad (4700, 0) on the right short end |
| Zones | loading x = −300, readout (SNSPD, window) x = +300 |
| Segments | 15 + 15 at 100 µm pitch, centres x = −700 … +700; outer DC depth 200 µm |
| Long-edge pads | 120 × 200 µm Au, four rows at \|x\| = 2450 … 4700, y = ±1030: TL1–TL8, TR1–TR9, BL1–BL8, BR1–BR9 |
| Left short end | centre-DC pad C (−4650, 0); SNSPD pads SNS (−4750, +260) and SNG (−4750, −260) |
| Ground | Au ground-fill bond spots GND-1…4 at (±2500, ±820); M1 bond openings M1-1…4 at (±2900, ±820) |
| Alignment marks | L1 at (±2150, ±1080), in edge notches of the Au ground fill |
| Full pad list | `gds/trap_die_v2_A30_pads.csv` (`_B60_pads.csv` is identical) |

**Beam clearance** (`sim/11_beam_clearance.py`, narrow die) [team calc]: fraction of beam power hitting the surface 1.1 × 10⁻⁵ at 493 nm, 1.1 × 10⁻⁴ at 650 nm, 1.4 × 10⁻⁶ at 405 nm. A 2.0 mm wide die would be ~10× better. The beams leave the die at |x| ≲ 1.9 mm (including the carrier), so every pad and bond at |x| ≥ 2.4 mm is off the beam paths.

**Test structures** are no longer on the trap die. They are on `gds/test_die_v2.gds` (`make_test_die.py`, same 10 × 2.5 mm size and layer stack): T1 Au comb (5 µm gap), T2 Au/D2/M1 capacitor 0.8 × 0.8 mm + M1 pad, T3 NbN 4-wire bar, T4 spare SNSPD 30 × 30 and T4b spare SNSPD 60 × 30 (both with buried ITO + via + top ITO), T5 top-ITO 4-wire bar with Au contacts, T6 Au continuity loop, T7 buried-ITO → Al via chain (14 vias), T8 EBL dose array (seven 30 × 30 µm meanders on L20 datatypes 1–7, factors 0.80–1.20 × nominal; `mask_list.md` section 2). Each run layout has two test dies.

**Plain trap die, no SNSPD** (`gds/trap_die_v2_NODET.gds`, `make_chip.py --nodet`, DESIGN_LOG step 14):
- Same electrodes, pads, marks and M1 bond openings as A30. It has no window (solid centre DC) and nothing on L20, L22, L24, L30 or L31.
- It is in both run layouts (`run_R1_TRAP`, `run_R1_FULL`) but not on `wafer_v2.gds`. On a mixed wafer it simply receives no features in those layers' steps.
- **Trap-only wafer:** run steps 0–3, 9, 11–19 and skip steps 4–8b and 10. D2 (step 9) then goes directly on M1. Keep it 10 µm, which is the `ground_depth` the simulation assumes.
- Step 11 opens only the four M1 bond openings and the L50 alignment crosses.
- Step 17 drops the SNSPD tests.

**Wafer jobs** use the run GDS, `gds/run_<name>.gds`: one MLA job per layer and one EBL job for L20, writing only the run's block at the wafer centre (`mask_list.md` section 3).

### A.1 Resolved in GDS v2

| # | Was | Now in the GDS |
|---|---|---|
| A1 | L1 marks under M1 Al | 300 × 300 µm M1 cut-outs at every mark site (trap die: edge notches at (±2150, ±1080); test die: (−1700, ±1080), (4300, ±1080)) |
| A2 | No EBL marks on L22 | 20 µm L22 crosses (2 µm arms) at (0, ±700) and (600, ±700) around the readout zone, plus one at every mark site |
| A3 | No protect layer for the gap etch | L45 PROTECT is drawn: every bond/probe D2 opening + 10 µm, readout window + 2.5 µm, SNSPD-lead branch region at the left end (x = −4835 … −4430, \|y\| ≤ 330). On the test die also the T3, T4/T4b, T5 and T7 areas. Used in step 16a |
| A4 | Ground fill had no bond pad | GND-1…4 bond spots on the fill, listed in `*_pads.csv`. There is still no on-chip link to M1, so they must be bonded (step 19) |
| A5 | No probe-able buried-ITO → Al test | T7 via chain (14 vias) on the test die |
| A6 | Top-ITO radial edges flush with the centre-DC Au edge | Pulled 2 µm inside (L30 \|y\| ≤ 18 µm; Au edge at \|y\| = 20 µm) |
| A7 | Single die only | Full-wafer reference `gds/make_wafer.py` → `wafer_v2.gds` (184 dies); R&D run layouts `gds/make_run.py` → `run_R1_TRAP.gds`, `run_R1_FULL.gds` (8 dies each, section A.3) |

### A.2 Still open

| Item | Why it matters | Action |
|---|---|---|
| Witness wafers W1–W6 (section E) | Most [verify] values in steps 5–16 depend on them; W3 rehearses steps 9–18 | Run W1-a/b/c, W2, W3 and W4 before the device wafer |
| NbN recipe and tool access (step 5) | Flows, power and pressure were not retrieved; RF-bias AJA access is unconfirmed | Get the Dane 2017 recipe from the Berggren group |
| Plating bath (step 14) | Whether Plating-U04 has a gold tank, and its chemistry, are unverified | Ask staff; W5 |
| ITO in the D2 etch (steps 15–16) | ITO etch rate in CHF₃/CF₄/Ar is unknown. The window is under L45 now, so this matters for T5 and for any decision to drop the window patch | W4 |
| BOE undercut (step 16) | Not in run 1: it attacks Al, Ti and probably ITO, and the leads and ITO edges sit within 2 µm of the centre-DC Au edge | W6 only if an undercut is ever wanted |
| TMAH through the thin HSQ/cap; 2 µm margins | Steps 8a/8b develop TMAH-based resist over NbN covered only by HSQ + ≥ 30 nm cap (pinholes possible [inference]). Near the readout the L22 leads are 1.5–1.7 µm and both ITO layers 2 µm inside the centre-DC Au edge, so L22/L30/L31 ↔ L50 overlay must hold ±1 µm | Short develop + ≥ 3 min running rinse (steps 6, 8a, 8b); overlay check after step 13 |
| HS50 mark recognition | The L22 crosses are 20 µm with 2 µm arms; the HS50 auto-alignment may want another shape | Ask EBL staff [verify] |


### A.3 R&D run plan at MIT.nano

The work is organised as a series of short, cheap runs with the layout updated between them, not as one production wafer. Each run is a full 100 mm wafer with only a central block written (`gds/make_run.py`, `mask_list.md` section 3). The MLA is maskless, so changing the GDS between runs costs nothing.

| Run | Layout | Process | Main questions | Feeds the next run |
|---|---|---|---|---|
| **0: short loops** | pieces or spare wafers | section E (W1–W6) | NbN on the real stack; HSQ dose; D2 stress and the full D2-to-dicing rehearsal (W3); ITO survival; plating | Recipes, dose, etch times |
| **1a: trap only** (`run_R1_TRAP`, run sheet `RUNSHEET_R1_TRAP.md`) | 6 NODET + 2 trap-only test dies (T1, T2, T6) | Steps 0–3, 9, 11–19. Skip 4–8b, 10 and every L20–L31 job. No EBL. | Plating, gap etch, leakage and breakdown (`test_plan.md` a1–a5), trapping, transport, heating rate | Trap process frozen; NODET becomes the reference die |
| **1b: full stack** (`run_R1_FULL`) | 2 A30, 2 B60, 2 NODET, 2 TEST | All steps | T8 dose array → nominal dose; T3/T4/T4b Tc, Isw and efficiency; SNSPD with RF on; ion over the window compared with NODET | Dose, spacer and cap thicknesses, die mix for run 2 |
| **2+** | edit `RUNS` in `make_run.py` | All steps | Whatever 1a/1b leave open, plus any `SIMPLIFICATIONS.md` variant worth trying | – |

**William chose 1a first (2026-11-02).** `RUNSHEET_R1_TRAP.md` is the streamlined sheet for it.

**Facility questions to settle with MIT.nano staff before run 1** (all [verify]):
- **Gold.** Which tools accept wafers carrying Au. The D2 gap etch (step 16), the L45 resist step, the probe station and the dicing saw all come *after* plating.
- **NbN.** Which sputter tool and recipe (Dane 2017 is a Berggren-group process), and whether access goes through that group.
- **Plating.** Whether a gold plating tank exists, its chemistry, and its minimum plated area.
- **ITO.** Which sputter source.
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
| 8a | Via to M1 | 24 | – | etch ~0.27 µm | MLA150; RIE-F-Samco-230iP (CHF₃) |
| 8b | Buried ITO (lift-off) | 31 | ITO | 60 nm | MLA150; sputter (ITO target [verify]) |
| 9 | D2 | – | PECVD SiO₂ | 10.0 µm front + backside compensation | PECVD; Filmstress-Tencor-FLX2320 |
| 10 | Top ITO (lift-off) | 30 | ITO | 125 nm optical, deposit 135–140 nm | MLA150; sputter |
| 11 | D2 openings | 40 | – | etch ~10.3 µm | MLA150; RIE-F-Samco-230iP / RIE-PlasmaTherm-210RL |
| 12 | Plating seed | – | Ti/Au | 15 / 50 nm | Sputter-AJA-* |
| 13 | Plating mold | 50 | AZ nLOF 2070 | ≥ 8 µm | MLA150 |
| 14 | Au electroplating | 50 | Au | 6.0 µm | Plating-U04 [chemistry unverified] |
| 15 | Strip, seed removal | – | – | Au 50 nm, Ti 15 nm removed | Asher-*; Clean-Ar-Plasma [verify it can ion-mill]; RIE-F |
| 16a | Protect resist | 45 | thick positive resist | ≥ 10 µm | MLA150 |
| 16 | Au-masked D2 gap etch | – (L50 is the mask) | – | etch ~9.6 µm, stop 0.75 µm above M1 | RIE-F-Samco-230iP |
| 17 | RT wafer-level electrical test | – | – | – | ProbeStation-Summit-11000 |
| 18 | Protect, dice | 101 | – | 10 × 2.5 mm dies, 200 µm streets | Diesaw-DAD3240 |
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
| Buried ITO (L31) | 60 ± 10 nm | Optical matching layer + RF shield. **Grounded to M1** through L24 (10 × 10 µm, 45 µm +x of the meander edge). |y| ≤ 18 µm |
| PECVD SiO₂ (D2) | 10.0 µm | Stays over the detector (ITO-on-D2 window) |
| Top ITO (L30) | 125 nm (deposit 135–140) | Half wave at 493 nm, so optically "absent". Tied to the centre DC through a 5 µm overlap under the Au along the axis; radial edges 2 µm inside the centre-DC Au edge (\|y\| ≤ 18 µm) |
| Au walls (centre DC, 5 µm rims) | 6.0 µm | Window 30 × 30 µm (A30) or 60 × 30 µm (B60); pocket depth 6 µm |
| Vacuum; ion | h ≈ 50 µm above the Au top, minus ~1.2 µm recess effect (DESIGN_LOG step 6) | – |

Expected NbN absorption ≈ 0.53, worst ±10 nm corner 0.41, vs 0.40 without the buried ITO. The model reads ~10 % pessimistic against Hampel. These are TMM effective-medium numbers, not RCWA (DESIGN_LOG step 9b).

Under the trap electrodes elsewhere: Si / D1 / M1 / spacer / cap / D2 / Ti-Au seed / 6 µm Au. Ground is ~10.3 µm below the Au.

---

## D. Thermal budget

| Step | Max T | Time at T | Note |
|---|---|---|---|
| 2 Thermal oxide | ~1000–1100 °C [verify furnace recipe] | hours | Before Al and NbN, so no limit applies |
| 3 Al sputter | < 100 °C [verify] | min | – |
| 4 Spacer PECVD | ≤ 300 °C | ~5 min | First anneal of the Al |
| 5 NbN sputter | ~RT (unheated; plasma heating unquantified) | min | Dane 2017 recipe is unheated |
| 6, 7, 8a, 8b, 10, 11, 13 resist bakes | ≤ 115 °C (HSQ bake per datasheet [verify]) | min | – |
| 8 Cap PECVD | ≤ 300 °C | min | – |
| 9 D2 PECVD (front + back) | ≤ 300 °C | cumulative ~1–2 h [verify rate] | Hottest long step after Al and NbN. JoVE ran 350 °C; we cap at 300 °C because of the Al |
| 10 ITO anneal (optional) | ≤ 250 °C in N₂, or none | ≤ 30 min [verify] | Protects Al and NbN |
| 14 Plating bath | ~50–65 °C [verify bath datasheet] | ~30–60 min | – |
| 19 Die attach / bake-out | ≤ 150–200 °C [verify adhesive] | hours–days | Au–Al intermetallics on bakes [inference] |

| Limit | Value | Source |
|---|---|---|
| Al hillocks / voids | significant at ~350 °C; Al-1%Cu or a Ti/TiW cap suppresses them | SINTEF; JoVE M1 step ("prevent whisker formation during bakeout") |
| **Rule for this run** | **≤ 300 °C for every step after step 3** | team inference from the two lines above |
| NbN, inert ambient | Tc stable to 500 °C | arXiv:2501.07780 |
| NbN, uncapped in O₂ | Tc drops | Ioffe paper (research report) |
| NbN in air | Nb₂O₅ grows as d_ox = 0.78 t^0.17 nm (t in days): ~0.8 nm after 1 day | Medeiros 2019 |
| ITO | crystallises at ≳ 200–250 °C, with lower ρ and better transmission; amorphous as sputtered at RT | search-snippet trends, unverified (`stack_shielding_ito.md` Q2) |

---

## E. Witness wafers and short loops to run first

Run these before committing the device wafers. W3 is the most valuable: it rehearses steps 9–18 with no NbN.

| ID | Short loop | Stack / steps | Measure | Go / no-go |
|---|---|---|---|---|
| W1-a | **NbN on spacer-over-Al** | Si / 1 µm ox / 150 nm Al-1%Cu / 238 nm spacer → NbN 7 nm, co-loaded with a thermal-SiO₂/Si chip (Medeiros ellipsometry model) | AFM on the spacer before NbN (hillocks, roughness); NbN thickness by ellipsometry; Rsq (4-pt); Tc (dipstick / PPMS [verify access]) | Rsq ≈ 400 Ω/sq ± 15 % [team calc]; Tc ≥ 7.5 K on both pieces [verify]; no hillocks > 100 nm [verify] |
| W1-b | NbN thermal history | W1-a pieces with HSQ / cap → buried-ITO sputter → 5 × D2-equivalent PECVD cycles at 300 °C | Rsq and Tc again | ΔTc ≤ 0.3 K, ΔRsq ≤ 10 % [verify] |
| W1-c | **Buried ITO to Al contact** | Al / spacer / cap → L24-type vias (10 µm) → 60 nm ITO, then a 300 °C cycle | Via-chain or Kelvin R. On W3 and the device wafer the same test is the T7 chain on the test dies (14 vias) | ≤ 1 kΩ per via [verify]. If high: in-situ Ar clean before the ITO, or a Ti/Au plug in the via |
| W2 | **HSQ dose test** on the real stack (Al / spacer / NbN) | Dose matrix (mask_list L20); salty vs TMAH develop; CF₄ 2.0 / 2.5 / 3.0 min | SEM linewidth; remaining HSQ thickness (needed for the cap thickness); RT R of test meanders | 100 ± 10 nm lines, no bridges, no breaks; R / R_expected 0.8–1.3 |
| W3 | **D2-to-dicing rehearsal** (no NbN) | Si / ox / Al / spacer / cap / L24 / L31 / 10 µm D2 (+back) / L30 / L40 / seed / L50 / plate / seed removal / L45 / gap etch / dice | Bow per D2 increment; D2 BOE rate and index; L40 profile; plating thickness and roughness; seed-removal roughness; gap-etch rate, uniformity and profile (SEM cross-section); Au redeposition on sidewalls; T1/T2/T6/T7 on the test dies; Al pad bondability (pull test) | See `process_checks.md` |
| W4 | **ITO optics and survival** | 125 nm and 60 nm ITO on PECVD SiO₂ on Si and on a fused-silica slide | Rsq; n,k by ellipsometry; T(493 nm); then Ti/Au seed → Ar mill → F-plasma Ti etch → ΔRsq, ΔT, Δthickness; then 30 min of the step-16 RIE recipe → **ITO etch rate in CHF₃/CF₄/Ar** | Rsq ≤ 400 Ω/sq; k ≤ 0.01 [verify]; ITO loss in the step 15+16 sequence < 10–15 nm. If not, the step-16a protect patch over the window is mandatory |
| W5 | Plating test | Seed + nLOF mold (real L50) + 6 µm Au on a W3 wafer or a bare-oxide wafer | Current calibration; thickness map; AFM roughness; gap width top/bottom | 6.0 ± 0.5 µm; roughness ~8 nm rms after seed removal (PTB 8.3(5) nm) |
| W6 | Optional BOE | Al / Ti / ITO coupons in 6:1 BOE for 10–60 s | Etch rates | Only if an undercut is ever wanted (step 16 note) |

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
- **Also:** set aside **≥ 3 dummy Si wafers** for W1/W3/W5 and fused-silica slides for W4.
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
  - Cut-outs open: trap dies, under the SNSPD pads (260 × 220 µm) and at the 4 mark sites (300 × 300 µm); test dies, the T3/T4/T4b pad areas, the T7 chain area with its isolated M1 islands, and the mark sites.
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
- **Target:** cap = 80 nm − measured HSQ remaining, **≥ 30 nm** for sidewall coverage [inference]. HSQ + cap = 80 ± 10 nm (DESIGN_LOG step 9b).
- **Tool:** PECVD at ≤ 300 °C. Measure the cap on a co-loaded Si piece (ellipsometry).
- **Hazards:**
  - The oxidising plasma meets the NbN sidewalls first. Hampel deposited PECVD directly on bare NbTiN without problems; there are no NbN data [inference].
  - From here until step 11 the pads are covered: **no electrical check is possible during steps 8–10**. Use the W1-b witness instead.
- [ ] Done — date: ____ operator: ____ t_cap: ____ HSQ (witness): ____ notes: ____

### 8a. L24 via to M1 (grounds the buried ITO)
- **Purpose:** 10 × 10 µm via through cap + spacer to the Al, 45 µm +x of the meander edge (`make_chip.py` XV): at (360, 0) on A30 and (375, 0) on B60. The test dies have one via each on T4/T4b and the 14 T7 vias.
- **Tool:** MLA150; RIE-F-Samco-230iP with CHF₃ (Hampel used CHF₃ RIE for the mirror vias).
- **Recipe:**
  - Positive resist ~1.3 µm, expose L24 **drawn**. Short TMAH develop + ≥ 3 min running rinse: the NbN is now under a thin cap, and pinholes are possible [inference].
  - Etch ~0.27 µm (cap + spacer, no HSQ at the via) + 30 % over-etch, stopping on Al [verify rate].
  - Strip in solvent only. **No O₂ ash** while the cap is this thin [inference].
- **Layer / align:** L24 → L1 (±3 µm).
- **Inspect:** via floor shows bright Al (optical).
- [ ] Done — date: ____ operator: ____ etch time: ____ notes: ____

### 8b. L31 buried ITO, 60 nm, lift-off
- **Purpose:** optical matching layer and grounded RF shield directly over the wire (DESIGN_LOG steps 9b and 10, case c1 ≈ 0 pickup). **It must be grounded:** floating it gives 6.6 µA pickup vs 0.72 µA for Al alone (step 10, case d).
- **Tool:** MLA150; RT sputter with Ar/O₂ (ITO target and O₂ flow [verify on tool]).
- **Recipe:**
  - LOR + S1813 bilayer, expose L31 **drawn** (same TMAH precautions as step 6).
  - Short in-situ Ar clean of the via if the tool allows it (W1-c) [verify].
  - Sputter **60 ± 10 nm**; lift-off in NMP.
- **Layer / align:** L31 → L1 (±1.5 µm). It must cover the meander (3 µm margin in y), stay ≥ 2 µm inside the centre-DC Au edge (|y| ≤ 18), and clear the L22 leads by 12 µm.
- **Inspect:** thickness and Rsq on a co-loaded witness (expected ~170–330 Ω/sq from Eltony's ρ = 1–2 × 10⁻⁵ Ω·m [team calc]); lift-off clean; via filled.
- **Hazards:** sputter plasma through the 80 nm oxide onto the NbN. Effect not measured; W1-b covers it.
- [ ] Done — date: ____ operator: ____ t_ITO: ____ Rsq: ____ notes: ____

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

### 10. L30 top ITO on D2 (lift-off)
- **Purpose:** grounded conductor above the window. The ion sees only conductors, which screens click kicks and surface charge (Todaro Supp.; Hampel published version). Tied to the centre DC through the 5 µm overlap under the Au (DESIGN_LOG step 6).
- **Tool:** MLA150; RT sputter.
- **Recipe:**
  - LOR + S1813, expose L30 **drawn** (TMAH is fine now: the NbN is under 10 µm of oxide).
  - Sputter **135–140 nm**: 125 nm optical (half wave, DESIGN_LOG step 9) + 10–15 nm for the step-15 Ar etch.
  - Lift-off in NMP.
  - Anneal: none, or ≤ 250 °C in N₂ (protects Al and NbN) [inference].
- **Layer / align:** L30 → L1 (±1 µm; A6).
- **Inspect:** thickness, Rsq and T(493 nm) on a co-loaded fused-silica witness. Expected ~70–150 Ω/sq at 135 nm [team calc]. On-chip, T5 can only be measured after step 15.
- **Go / no-go:** Rsq ≤ 400 Ω/sq; k ≤ 0.01 [verify].
- [ ] Done — date: ____ operator: ____ t_ITO: ____ Rsq: ____ T493: ____ notes: ____

### 11. L40 D2 openings (pads, M1 bond openings, L50 alignment crosses)
- **Tool:** MLA150; RIE-F-Samco-230iP or RIE-PlasmaTherm-210RL.
- **Recipe:**
  - Thick positive resist **≥ 8 µm** (AZ 10XT / AZ 4620-class [verify stock]). JoVE used 6 µm. Expose L40 **drawn**.
  - Etch with CHF₃ 25 / CF₄ 5 / Ar 50 sccm, 130 mTorr, 600 W, ~360 nm/min (JoVE) [verify on our tool].
  - Depth: ~10.36 µm over M1 (D2 + cap + spacer) and ~10.1 µm over the L22 pads, so ~29 min + 10–15 % over-etch. Run in ≤ 5 min segments with cool-down to save the resist [inference].
  - Stops on Al (AlF₃) and on Au.
- **Layer / align:** L40 → L1 (±5 µm).
- **Inspect:**
  - Dektak depth; clean metal at every opening floor.
  - **First probe access since step 7:** meander R₁ (SNS/SNG) and T3/T4/T4b on the test dies.
  - SNSPD pads (both tied together) to M1 (any M1-n opening) at ≤ 1 V must read **> 1 GΩ**. This checks for no short through the cap to the grounded buried ITO.
- **Hazards:** heat in the long etch. The top ITO and window are under resist here.
- [ ] Done — date: ____ operator: ____ etch time: ____ R₁: ____ SNSPD–M1: ____ notes: ____

### 12. Plating seed Ti 15 nm / Au 50 nm (PTB)
- **Tool:** Sputter-AJA-* (sputter for step coverage; PTB evaporated).
- **Note:** the seed shorts every electrode and both SNSPD pads together. That is ESD-safe, but no electrical checks are possible until step 15.
- **Hazards:** Ti on the top ITO, inside the window and on T5. Ti/ITO contact is assumed ohmic [verify W4].
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
  - Plated area ≈ 0.203 cm² per trap die (Au fraction 0.813 of 0.25 cm²) and ≈ 0.166 cm² per test die (0.664, with T8), so ≈ 1.6 cm² for `run_R1_FULL` or `R1_TRAP` (8 dies) and ≈ 36 cm² for the full `wafer_v2` + any open edge [team calc from GDS]. Such a small plated area on a 100 mm wafer needs a low, well-calibrated current; confirm the tank's minimum on W5 with the same run layout [verify].
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
  - The ITO window and T5 see the F plasma and, once the Ti breaks through, the end of the Ar etch. That is the reason for the 10–15 nm ITO margin.
  - The SNSPD L22 pads lose a few nm of Au.
  - Line-of-sight redeposition is unavoidable (Sussex).
- **Inspect:**
  - All electrodes isolated (neighbours > 100 MΩ at 10 V).
  - Meander R₂.
  - T5 ITO Rsq on the test dies (first on-chip ITO value).
  - Window floor optically clean (no Au film).
  - AFM: Au roughness ~8 nm rms (PTB 8.3(5) nm).
- [ ] Done — date: ____ operator: ____ Ar time: ____ F time: ____ R₂: ____ notes: ____

### 16a. Protect resist (L45, drawn in the GDS, see A3)
- Thick positive resist ≥ 10 µm over the 6 µm topography. MLA expose **inverted** (resist stays on the L45 patches), aligned to L40/L50 (±2 µm).
- Covers, on trap dies: the four M1 openings + 10 µm; the SNSPD-lead branch region at the left end (x = −4835 … −4430, |y| ≤ 330: SNSPD pads, their D2 openings, and where the L22 leads leave the centre-DC lead); the readout window + 2.5 µm (onto the 5 µm Au rim).
- On test dies: every D2 opening + 10 µm; the T3, T4 and T4b boxes; the T5 ITO bar; the T7 chain area. T1, T2 and T6 are left open on purpose so they see the gap etch.
- The window patch can be dropped **only if W4 shows ITO loss < margin in the step-16 recipe**.
- [ ] Done — date: ____ operator: ____ notes: ____

### 16. Au-masked D2 gap etch
- **Purpose:** remove D2 from the electrode gaps so the ion does not see oxide; aspect ratio > 1 (Bautista-Salvador 2019).
- **Recipe:**
  - Same CHF₃/CF₄/Ar recipe as step 11.
  - Etch ~9.6 µm, stopping **~0.75 µm above M1** (Sussex: 750(250) nm, 4(1) % uniformity), so ~27 min at 360 nm/min [verify on W3].
  - Etch in segments; check depth on the T1 comb gaps (test dies) by Dektak / optical interferometry.
- **Exposure notes:**
  - Over the window, the top ITO acts as the etch mask if 16a is not used. Fluorine plasmas etch ITO slowly, but this is **unverified for this recipe (W4)**.
  - The L22 leads cross a 10 µm Au gap in two spots, where they leave the centre-DC lead at x ≈ −4455, |y| ≈ 20–30. Both spots are inside the L45 branch patch. Checked with gdstk: the only L22 not covered by Au, L40 or L45 are the EBL crosses and overlay squares at the mark sites, which are no longer needed. **If 16a is skipped**, the lead top at those spots is ~0.6 µm above M1, with ~0.15 µm of oxide left over it or none [team calc]; then stop at ≥ 0.9 µm.
- **Optional BOE undercut: NOT in run 1.**
  - BOE attacks Al, the Ti adhesion layer under the Au, and probably ITO (W6).
  - Near the readout the SNSPD leads are only **1.5–1.7 µm inside the centre-DC Au edge** [GDS check], and the buried and top ITO are 2 µm inside it. A Sussex-style 3 µm undercut would reach both.
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

### 18. Protect, dice 10 × 2.5 mm, strip
- **Recipe:**
  - Protective resist ≥ 8 µm (covers the 6 µm Au).
  - Diesaw-DAD3240 with a Si blade, on the L101 outlines [verify blade / recipe with staff]. The die grid is regular, so all cuts run straight through: x streets on a 10.2 mm pitch, y streets on a 2.7 mm pitch, 200 µm wide. The kerf plus chipping must fit in the 200 µm street [verify blade width].
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
  - Openings are 170 × 170 µm (M1) and 120 × 90 µm (SNSPD) at the bottom of 10 µm wells; check the wedge foot fits [verify]. The Au pads are 120 × 200 µm on the long edges and 200 × 200 µm for RF and C.
  - **Bond the Au ground fill to carrier ground at GND-1…4, ≥ 2 of them (A4).** There is no on-chip link from the fill to M1.
  - Bond off the long edges for the four pad rows, off the right short end for RF (4700, 0), and off the left short end for C and the SNSPD pads. All pads and GND spots sit at |x| ≥ 2.45 mm, outside where the beams leave the die (|x| ≲ 1.9 mm incl. the carrier). Keep the loops low anyway.
  - Bond the SNSPD pads last, wearing a strap. Short the carrier SNSPD pins until installation [inference].
- **Bond map** (from `gds/trap_die_v2_A30_pads.csv`, identical for B60; fill in the carrier pin column). Rows run along y = +1030 (T) and y = −1030 (B) at a 180 µm pitch: TL1 … TL8 at x = −4700 … −3440, TR1 … TR9 at x = +4700 … +3260 (same x for BL / BR).

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
| C | 2 | centre DC (top ITO tied here), (−4650, 0) | 50 | Au | |
| SNS | SNSPD_S | SNSPD signal, (−4750, +260) | 22 | Au | |
| SNG | SNSPD_G | SNSPD return, (−4750, −260) | 22 | Au | |
| RF | 1 | RF, (4700, 0) | 50 | Au | |
| M1-1…4 | ground plane | Al through D2, (±2900, ±820) | 40 | **Al** | |
| GND-1…4 | Au ground fill | (±2500, ±820); ≥ 2 bonds | 50 | Au | |

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
