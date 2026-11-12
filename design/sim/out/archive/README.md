> **Claude-authored.** Index of the superseded console logs moved out of `design/sim/out/`, 2026-11-10.
This folder holds 26 saved console logs (`*_log*.txt`) from earlier sim runs, moved here with `git mv`.
No script reads these files; the current logs stay in `design/sim/out/`. `14_staircase_check.py` cites two of them in its docstring as history (`12_log_v3_UNIFORM.txt` and `12_log_v3_NODET_rerun.txt`); the script itself reads the `trap_die_v3_UNIFORM` and `trap_die_v3_NODET` summaries in `out/12_final_chip/`.
The `out/` folders (for example `12_final_chip/`) are not moved here.
Names encode the version: no tag = v1; `v2` and `v3` = the v2 and v3 stacks; `_600um` = v4 before the zones moved to 480 µm apart (v3 zones were 600 µm apart).
Logs are named by their sim (`04b`, `10`, `12`, `13`); see `design/sim/INDEX.md` for the scripts.
