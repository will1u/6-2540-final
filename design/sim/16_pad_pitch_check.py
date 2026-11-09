"""Compare the current pad layout with the preserved 180 um baseline (Claude-authored).

Run through ./run.sh 16_pad_pitch_check.py. Runs sim 12 sequentially and stops at
the first failed acceptance check. Does not edit documentation or layout inputs.
Baseline directories are copied once and are never overwritten on a rerun.
Use --resume to recheck completed cases and continue, only with identical inputs.
"""

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "16_pad_pitch_check"
BASE = HERE / "out" / "12_final_chip" / "pad180"
CASES = [
    ("A30_E2", "A30", False, False),
    ("A30_E1", "A30", True, False),
    ("A30_E2_V2zero", "A30", False, True),
    ("B60_E2", "B60", False, False),
    ("B60_E1", "B60", True, False),
    ("B60_E2_V2zero", "B60", False, True),
    ("NODET", "NODET", False, False),
]
OUT.mkdir(parents=True, exist_ok=True)
# Keep the compiler's disposable cache in a writable, git-ignored directory.
os.environ["NUMBA_CACHE_DIR"] = str(OUT / "__pycache__")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paths(die, e1, zero):
    stem = "trap_die_v4_" + die
    tag = stem + ("_E1" if e1 else "") + ("_V2zero" if zero else "")
    js = HERE.parent / "gds" / (stem + ("_E1_sim.json" if e1 else "_sim.json"))
    return tag, js


# Preserve all seven baselines before starting any simulation.
for name, die, e1, zero in CASES:
    tag, js = paths(die, e1, zero)
    oldlog = HERE / "out" / ("12_log_v4_" + name + "_pad180.txt")
    if not oldlog.is_file():
        raise RuntimeError(f"Missing baseline log: {oldlog}")
    dest = BASE / tag
    if not dest.exists():
        current_log = HERE / "out" / ("12_log_v4_" + name + ".txt")
        if sha(oldlog) != sha(current_log):
            raise RuntimeError(f"Current outputs may not be the pad180 baseline: {name}")
        shutil.copytree(HERE / "out" / "12_final_chip" / tag, dest)
        shutil.copy2(oldlog, dest / "run.txt")
    if not (dest / "summary.json").is_file() or not (dest / "waveforms.csv").is_file():
        raise RuntimeError(f"Incomplete baseline: {dest}")

inputs = {HERE / "12_final_chip_check.py", HERE / "trapcalc.py", HERE / "run.sh",
          HERE / "run_cached_geometry.py"}
for name, die, e1, zero in CASES:
    tag, js = paths(die, e1, zero)
    layout = json.loads(js.read_text())
    inputs.update((js, js.parent / layout["_gds"]))
    if layout["_window"]["wx"]:
        inputs.add(HERE / "out" / "04b_window_3d" / ("summary_" + layout["_window"]["floor"] + ".json"))
fingerprints = {str(p.relative_to(HERE.parent)): sha(p) for p in sorted(inputs)}
report = dict(started_utc=datetime.now(timezone.utc).isoformat(), inputs_sha256=fingerprints,
              transport_limit_V=1.75, planar_height_limits_um=[49.96, 49.98],
              height_precision_decimals=2, cases=[])
completed = set()
if "--resume" in sys.argv:
    previous = json.loads((OUT / "comparison.json").read_text())
    if previous["inputs_sha256"] != fingerprints:
        raise RuntimeError("Cannot resume: simulation inputs changed")
    completed = {c["case"] for c in previous["cases"]}
    report["started_utc"] = previous["started_utc"]
    report["resumed_utc"] = datetime.now(timezone.utc).isoformat()
voltage_rows = []

for name, die, e1, zero in CASES:
    tag, js = paths(die, e1, zero)
    old = json.loads((BASE / tag / "summary.json").read_text())
    logfile = HERE / "out" / ("12_log_v4_" + name + ".txt")
    command = [sys.executable, "-u", str(HERE / "run_cached_geometry.py"),
               str(HERE / "12_final_chip_check.py"), str(js)]
    if zero:
        command.append("--centre-dc-zero")
    if name in completed:
        print(f"RECHECK {name} (completed simulation; identical inputs)", flush=True)
    else:
        print(f"START {name}", flush=True)
        with logfile.open("w", encoding="utf-8") as fh:
            subprocess.run(command, cwd=HERE, stdout=fh, stderr=subprocess.STDOUT, check=True)
    new = json.loads((HERE / "out" / "12_final_chip" / tag / "summary.json").read_text())
    errors = []
    row = dict(case=name, zones={}, transport=new["transport"])
    for zone in ("loading", "readout"):
        a, b = old[zone], new[zone]
        deltas = {n: b["V"].get(n, 0.0) - a["V"].get(n, 0.0) for n in set(a["V"]) | set(b["V"])}
        row["zones"][zone] = dict(old_vmax=a["vmax"], new_vmax=b["vmax"],
                                  max_electrode_delta_V=max(map(abs, deltas.values())),
                                  old_null_um=a["null_z"], new_null_um=b["null_z"],
                                  delta_null_um=b["null_z"] - a["null_z"])
        for n in sorted(deltas, key=int):
            voltage_rows.append(dict(case=name, zone=zone, electrode=n,
                                     old_V=a["V"].get(n, 0.0), new_V=b["V"].get(n, 0.0), delta_V=deltas[n]))
        if not zero and (b["vmax"] > 10 or b["bounded"] or abs(b["f_axial_MHz"] - 0.8) > 0.001):
            errors.append(f"{zone}: voltage limit or intended axial confinement failed")
        if not 49.96 <= round(b["null_z"], 2) <= 49.98:
            errors.append(f"{zone}: planar null outside 49.96-49.98 um at two decimals")
    t = new["transport"]
    row["old_transport"] = old["transport"]
    if not (49.96 <= round(min(t["height_range_um"]), 2) <= round(max(t["height_range_um"]), 2) <= 49.98):
        errors.append("transport planar null outside 49.96-49.98 um at two decimals")
    if t["any_bounded"] or any(abs(f - 0.8) > 0.001 for f in t["f_axial_range_MHz"]):
        errors.append("transport voltage limit or axial confinement failed")
    if (zero or die == "NODET") and t["max_step_change_V"] > 1.75:
        errors.append("transport step exceeds 1.75 V")
    row["errors"] = errors
    report["cases"].append(row)
    report["sim13_needed"] = any(c["zones"]["readout"]["max_electrode_delta_V"] > 0.10
                                  for c in report["cases"])
    (OUT / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    with (OUT / "zone_voltage_comparison.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(voltage_rows[0]))
        writer.writeheader()
        writer.writerows(voltage_rows)
    print(f"DONE {name}: zone max {new['loading']['vmax']:.2f}/{new['readout']['vmax']:.2f} V; "
          f"transport step {t['max_step_change_V']:.6f} V; errors={errors}", flush=True)
    if errors:
        raise RuntimeError(f"STOP: {name}: {errors}; do not update documentation")

if fingerprints != {str(p.relative_to(HERE.parent)): sha(p) for p in sorted(inputs)}:
    raise RuntimeError("Inputs changed during queue; do not update documentation")

# Compare every exported waveform electrode and the complete saved RF-null scan.
wave_rows = []
for row, (name, die, e1, zero) in zip(report["cases"], CASES):
    tag, js = paths(die, e1, zero)
    folder = HERE / "out" / "12_final_chip" / tag
    old = json.loads((BASE / tag / "summary.json").read_text())
    new = json.loads((folder / "summary.json").read_text())
    assert old["null_along_axis"]["y"] == new["null_along_axis"]["y"]
    row["max_null_scan_delta_um"] = max(abs(a - b) for a, b in
                                       zip(old["null_along_axis"]["z"], new["null_along_axis"]["z"]))
    with (BASE / tag / "waveforms.csv").open(newline="") as fh:
        old_wave = list(csv.DictReader(fh))
    with (folder / "waveforms.csv").open(newline="") as fh:
        new_wave = list(csv.DictReader(fh))
    assert len(old_wave) == len(new_wave) == 49
    assert old_wave[0].keys() == new_wave[0].keys()
    assert [r["y_um"] for r in old_wave] == [r["y_um"] for r in new_wave]
    deltas = []
    for electrode in new_wave[0]:
        if electrode == "y_um":
            continue
        a = [float(r[electrode]) for r in old_wave]
        b = [float(r[electrode]) for r in new_wave]
        delta = max(abs(v - u) for u, v in zip(a, b))
        deltas.append(delta)
        wave_rows.append(dict(case=name, electrode=electrode, max_delta_V=delta,
                              old_max_abs_V=max(map(abs, a)), new_max_abs_V=max(map(abs, b))))
    row["max_waveform_electrode_delta_V"] = max(deltas)
with (OUT / "transport_voltage_comparison.csv").open("w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(wave_rows[0]))
    writer.writeheader()
    writer.writerows(wave_rows)
report["validation_script_sha256"] = sha(Path(__file__))
report["completed_utc"] = datetime.now(timezone.utc).isoformat()
report["all_passed"] = True
(OUT / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
print(f"ALL SEVEN PASS; sim13_needed={report['sim13_needed']}", flush=True)
