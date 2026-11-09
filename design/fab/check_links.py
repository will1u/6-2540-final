"""Check every relative Markdown link under design/ (Claude-authored).

For each [text](target) or ![alt](target) in a .md file: the target file must exist, and if the link has
a #anchor the target file must have a heading whose GitHub-style slug equals it. Web links and mailto
links are skipped. Prints one line per broken link and exits non-zero if any is broken.

Slug rule (GitHub): lower-case the heading, drop everything that is not a letter, digit, space, hyphen or
underscore, then turn each space into a hyphen.

Run:  python design/fab/check_links.py [folder]      (default folder: design/fab; plain Python, no packages)
"""

import os
import re
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
LINK = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEAD = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def slug(heading):
    text = re.sub(r"[`*]", "", heading).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path):
    out, seen, fenced = set(), {}, False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.lstrip().startswith("```"):
                fenced = not fenced
            m = None if fenced else HEAD.match(line)
            if m:
                s = slug(m.group(1))
                n = seen.get(s, 0)
                seen[s] = n + 1
                out.add(s if n == 0 else f"{s}-{n}")
    return out


bad, checked, cache = 0, 0, {}
for folder, _, files in os.walk(ROOT):
    if ".obsidian" in folder or "_swarm" in folder:
        continue
    for name in sorted(files):
        if not name.endswith(".md"):
            continue
        src = os.path.join(folder, name)
        fenced = False
        with open(src, encoding="utf-8") as fh:
            lines = fh.readlines()
        for k, line in enumerate(lines, 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
            if fenced:
                continue
            for m in LINK.finditer(re.sub(r"`[^`]*`", "", line)):
                target = m.group(1).strip("<>")
                if re.match(r"^[a-z][a-z0-9+.\-]*:", target):       # http:, https:, mailto:, ...
                    continue
                checked += 1
                path, _, frag = target.partition("#")
                dest = src if not path else os.path.normpath(os.path.join(folder, unquote(path)))
                rel = os.path.relpath(src, ROOT)
                if not os.path.exists(dest):
                    bad += 1
                    print(f"{rel}:{k}: missing file  {target}")
                elif frag and dest.endswith(".md"):
                    if dest not in cache:
                        cache[dest] = anchors(dest)
                    if unquote(frag).lower() not in cache[dest]:
                        bad += 1
                        print(f"{rel}:{k}: missing anchor  {target}")
print(f"{checked} relative links checked under {ROOT}; {bad} broken")
sys.exit(1 if bad else 0)
