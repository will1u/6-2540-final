"""Check the numbers quoted in the docs (Claude-authored).

Three parts, all driven by design/facts_now.json:
  1. Print the live value of each fact, read from its sim output file under design/sim/out/.
  2. Check that each doc listed in must_contain quotes that value as a plain substring.
  3. Scan every .md and .svg file under the repo root for the stale strings in the "stale" list.
     Lines inside history files, or inside the history sections of a file, are skipped.

Run:    cd design/sim && ./run.sh ../check_numbers.py
        cd design/sim && ./run.sh ../check_numbers.py --table   (Markdown table of the facts only)
Inputs: design/facts_now.json, design/sim/out/<file>, the .md files of the repo.
Output: printed lines. Exit 0 when nothing is flagged, exit 1 otherwise.
Limits: quoted numbers are matched as plain substrings, so "1.9" also matches "11.9".
        Stale patterns are regular expressions (re.search).
"""

import fnmatch
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))   # the design/ folder
ROOT = os.path.dirname(HERE)                          # repo root
OUT = os.path.join(HERE, "sim", "out")
HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def rel_of(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def walk_keys(data, keys):
    # Follow the keys one level at a time; None if any key is missing.
    node = data
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def source_text(fact):
    return fact["file"] + " -> " + ".".join(fact["keys"])


def live_value(fact):
    # Returns (formatted text, None) or (None, reason).
    path = os.path.join(OUT, fact["file"])
    if not os.path.exists(path):
        return None, "file not found"
    value = walk_keys(json.loads(read_text(path)), fact["keys"])
    if value is None:
        return None, "key path not found"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None, "value is not a number"
    value = value * fact.get("scale", 1)
    return format(value, fact["show"]), None


def check_facts(facts, values):
    # Part 1: print each value. Fills values[id] with the text, for part 2.
    flags = 0
    print("PART 1: live values")
    for fact in facts:
        text, err = live_value(fact)
        if err:
            print(f"MISSING SOURCE: {fact['id']}: {err}  ({source_text(fact)})")
            flags += 1
            continue
        values[fact["id"]] = text
        print(f"{fact['id']}: {text}   {source_text(fact)}")
    return flags


def check_quoted(facts, values):
    # Part 2: each must_contain doc has to quote the formatted value.
    flags = 0
    print("PART 2: quoted in docs")
    for fact in facts:
        if fact["id"] not in values:
            continue
        text = values[fact["id"]]
        for doc in fact.get("must_contain", []):
            full = os.path.join(ROOT, doc)
            if not os.path.exists(full) or text not in read_text(full):
                print(f"NOT QUOTED: {doc} does not contain {text} ({fact['label']})")
                flags += 1
    return flags


def is_history_file(rel, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat):
            return True
        if pat.endswith("/**") and rel.startswith(pat[:-2]):
            return True
    return False


def scan_file(rel, path, rules, prefixes):
    # Test each line against the stale rules, skipping history sections.
    flags, hist_level, in_hist, fenced = 0, 0, False, False
    for n, line in enumerate(read_text(path).splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            m = HEAD.match(line)
            if m:
                level, title = len(m.group(1)), m.group(2)
                if any(title.startswith(p) for p in prefixes):
                    in_hist, hist_level = True, level
                elif in_hist and level <= hist_level:
                    in_hist = False
        if in_hist:
            continue
        for regex, why in rules:
            if regex.search(line):
                flags += 1
                print(f"STALE: {rel}:{n}: {why}")
                print(f"    {line.strip()[:160]}")
    return flags


def check_stale(stale, history_files, history_sections):
    # Part 3: scan every .md and .svg file under the repo root.
    flags = 0
    rules = [(re.compile(s["pattern"]), s["why"]) for s in stale]
    print("PART 3: stale strings")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d != ".git" and rel_of(os.path.join(dirpath, d)) != "proposal"]
        for name in sorted(filenames):
            if not name.endswith((".md", ".svg")):   # figures carry numbers too
                continue
            rel = rel_of(os.path.join(dirpath, name))
            if is_history_file(rel, history_files):
                continue
            flags += scan_file(rel, os.path.join(dirpath, name), rules,
                               history_sections.get(rel, []))
    return flags


def print_table(facts):
    print("| Quantity | Value | Source |")
    print("| --- | --- | --- |")
    for fact in facts:
        text, err = live_value(fact)
        shown = text if text is not None else "MISSING SOURCE"
        label = fact["label"].replace("|", "\\|")   # labels such as |V| would split the row
        print(f"| {label} | {shown} | {source_text(fact)} |")


def main():
    spec = json.loads(read_text(os.path.join(HERE, "facts_now.json")))
    facts = spec["facts"]
    if "--table" in sys.argv:
        print_table(facts)
        return 0
    values = {}
    flags = check_facts(facts, values)
    flags += check_quoted(facts, values)
    flags += check_stale(spec["stale"], spec["history_files"], spec["history_sections"])
    if flags == 0:
        print("ALL NUMBERS CONSISTENT")
        return 0
    print(f"CHECK NUMBERS: {flags} flags")
    return 1


if __name__ == "__main__":
    sys.exit(main())
