#!/usr/bin/env bash
# Run a design script in the `electrode` conda env without `conda activate` (Git Bash on Windows).
# The env's DLL folders must be on PATH or numpy/matplotlib crash with 0xc06d007f.
# Usage: ./run.sh 01_analytic_fivewire.py
E=/c/Users/willi/anaconda3/envs/electrode
export PATH="$E:$E/Library/mingw-w64/bin:$E/Library/usr/bin:$E/Library/bin:$E/Scripts:$PATH"
export PYTHONIOENCODING=utf-8 MPLBACKEND=Agg
cd "$(dirname "$0")" && exec "$E/python.exe" -u "$@"
