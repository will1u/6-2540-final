"""Run an unchanged study with exact repeated gap unions cached (Claude-authored).

Usage through run.sh: run_cached_geometry.py 12_final_chip_check.py <normal args>
The solver repeats union([conductor, claimed_gap]) for every leftover fragment.
Shapely geometries are immutable: reusing the result for the same pair avoids
repeating that calculation. No rounding, simplification or model change is made.
The cache is bounded and used only during split_gaps; the solver repo is untouched.
"""

from functools import lru_cache
from pathlib import Path
import runpy
import sys

import shapely
from shapely.geometry.base import BaseGeometry
from gds2itvg import core

original_split = core.split_gaps
original_union = shapely.union_all


@lru_cache(maxsize=256)
def union_pair(a, b):
    return original_union([a, b])


def cached_union(geoms, *args, **kwargs):
    if (not args and not kwargs and isinstance(geoms, list) and len(geoms) == 2
            and all(isinstance(g, BaseGeometry) for g in geoms)):
        return union_pair(*geoms)
    return original_union(geoms, *args, **kwargs)


def cached_split(*args, **kwargs):
    shapely.union_all = cached_union
    try:
        return original_split(*args, **kwargs)
    finally:
        shapely.union_all = original_union
        print(f"Exact gap-union cache: {union_pair.cache_info()}", flush=True)
        union_pair.cache_clear()


core.split_gaps = cached_split
study = Path(sys.argv[1]).resolve()
sys.argv = [str(study)] + sys.argv[2:]
runpy.run_path(str(study), run_name="__main__")
