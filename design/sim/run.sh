#!/usr/bin/env bash
# Run a design script in the `electrode` conda env without `conda activate`.
# Finds the env from $ELECTRODE_ENV, or else <conda base>/envs/electrode, so it works on any machine.
# On Windows (Git Bash) the env's DLL folders must be on PATH or numpy/matplotlib crash with 0xc06d007f.
# Usage: ./run.sh 01_analytic_fivewire.py     (setup: design/CLAUDE.md, "Setting up the electrode repo")
E="${ELECTRODE_ENV:-}"
if [ -z "$E" ]; then
  base="$(conda info --base 2>/dev/null)" || { echo "run.sh: set ELECTRODE_ENV or put conda on PATH" >&2; exit 1; }
  command -v cygpath >/dev/null && base="$(cygpath -u "$base")"
  E="$base/envs/electrode"
fi
export PYTHONIOENCODING=utf-8 MPLBACKEND=Agg
cd "$(dirname "$0")" || exit 1
if [ -x "$E/python.exe" ]; then        # Windows env layout
  export PATH="$E:$E/Library/mingw-w64/bin:$E/Library/usr/bin:$E/Library/bin:$E/Scripts:$PATH"
  exec "$E/python.exe" -u "$@"
else                                   # macOS / Linux env layout
  exec "$E/bin/python" -u "$@"
fi
