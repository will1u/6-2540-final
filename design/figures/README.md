> **Claude-authored.** Index of the report figure scripts and outputs in `design/figures/`, 2026-11-10.

| Figure file | Script and function | Data file(s) read | What is plotted (axis names only) |
|---|---|---|---|
| `report/die_map.pdf`, `.png`, `.svg` | `make_die_map.py` (module level) | `design/gds/trap_die_v4_A30.gds` (the v4 A30 die as `make_chip.py` writes it by default; layer 50 is unioned and the centre DC is the U-shaped piece), `design/gds/trap_die_v4_A30_pads.csv`, `design/gds/trap_die_v4_A30_sim.json` | (a) x (mm), y (mm); (b) x (µm), y (µm) |
| `report/rf_null_height.pdf`, `.png` | `make_report_figures.py` `fig_rf_null_height` | `design/sim/out/12_final_chip/{trap_die_v4_A30,trap_die_v4_A30_E1,trap_die_v4_NODET}/summary.json`, `design/gds/trap_die_v4_A30_sim.json` | axial position from the readout zone (µm); RF null height (µm) |
| `report/transport_static.pdf`, `.png` | `make_report_figures.py` `fig_transport_static` | `design/sim/out/12_final_chip/trap_die_v4_A30_V2zero/waveforms.csv` | ion position (µm); electrode voltage (V) |
| `report/collection_vs_height.pdf`, `.png` | `make_report_figures.py` `fig_collection_vs_height` | `design/sim/out/17_height_tradeoff/summary.json` | ion height (µm); geometric collection (%) |
| `report/termination.pdf`, `.png` | `make_report_figures.py` `fig_termination` | `design/sim/out/19_lead_termination/summary.json` | RF current through the nanowire (µA, log); case (y) |
| `report/stack.pdf`, `.png` | `make_report_figures.py` `fig_stack` | the final stack of 2026-11-12, typed in the function (not parsed): raised 100 nm Al mirror, base SiO₂ 1.0 µm nominal, SiO₂ spacer 238 nm, NbN 7 nm, HSQ 50 nm + SiO₂ cap 110 nm | layer bands (no axes) |
| `report/transport_waveform.pdf`, `.png` | `make_report_figures.py` `fig_transport_waveform` | `design/sim/out/21_transport_waveform/trap_die_v4_A30_V2zero/waveform.csv` | time (µs); ion position (µm); electrode voltage (V) |
| `report/rf_capacitance_sections.pdf`, `.png` | `make_report_figures.py` `fig_rf_capacitance_sections` | `design/sim/out/22_rf_capacitance/summary.json` | RF capacitance to ground (pF); configuration (y) |

Regenerate from `design/sim`:

    ./run.sh ../figures/make_die_map.py
    ./run.sh ../figures/make_report_figures.py
