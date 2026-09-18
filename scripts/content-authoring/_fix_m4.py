#!/usr/bin/env python3
"""Fix m4 escaping: test snippets + boilerplate carry literal `\\n` instead of
real newlines (and over-escaped `\\"`). Patches emitted JSONs (EN + VI) and the
authoring source cppi_m4.py so a re-emit cannot regress. Idempotent."""
import glob
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MOD = os.path.join(ROOT, "src/content/tracks/cpp/courses/cpp-intermediate/modules/operators-copy-move")
SRC = os.path.join(ROOT, "scripts/content-authoring/cppi_m4.py")


def fix_text(s: str) -> str:
    # Literal two-char backslash-n (as it appears in the *file*) -> real newline.
    # Safe here: no challenge string legitimately contains a C++ "\\n" literal.
    return s.replace("\\n", "\n").replace('\\"', '"')


def fix_json(p: str) -> int:
    d = json.load(io.open(p, encoding="utf-8"))
    n = 0
    for t in d.get("tests", []):
        if isinstance(t.get("code"), str) and "\\n" in t["code"]:
            t["code"] = fix_text(t["code"])
            n += 1
    if n:
        with io.open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return n


total = 0
for p in sorted(glob.glob(os.path.join(MOD, "**/*.json"), recursive=True)):
    total += fix_json(p)
print(f"json test strings fixed: {total}")

# Boilerplate (starter) fields live in challenge JSON too if present.
for p in sorted(glob.glob(os.path.join(MOD, "**/*.json"), recursive=True)):
    d = json.load(io.open(p, encoding="utf-8"))
    changed = False
    for key in ("boilerplate", "starterCode", "starter"):
        if isinstance(d.get(key), str) and "\\n" in d[key]:
            d[key] = fix_text(d[key])
            changed = True
    if changed:
        with io.open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"  boilerplate fixed in {os.path.basename(p)}")

# Authoring source: same replacement so re-emit matches.
src = io.open(SRC, encoding="utf-8").read()
fixed_src = fix_text(src)
if fixed_src != src:
    io.open(SRC, "w", encoding="utf-8").write(fixed_src)
    print(f"source patched: {SRC}")
else:
    print("source already clean")
