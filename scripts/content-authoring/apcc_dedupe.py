#!/usr/bin/env python3
"""Dedupe apcc-solutions.mjs: keep the LAST R[id]/W[id] per id."""
import io
import json
import re

PATH = __file__.replace("apcc_dedupe.py", "apcc-solutions.mjs")

with io.open(PATH, encoding="utf-8") as f:
    src = f.read()

# Split into header (up to and including the export line) and body lines.
m = re.search(r"^export \{ R, W \};\s*$", src, re.M)
header = src[: m.end()]
body = src[m.end():]

entries = []  # (kind, id, full_line)
for line in body.splitlines():
    line = line.strip()
    if not line:
        continue
    em = re.match(r'^(R|W)\[("(.*)")\] = ', line)
    if not em:
        raise SystemExit("unexpected ledger line: " + line[:80])
    kind, raw = em.group(1), em.group(2)
    cid = json.loads(raw)
    entries.append((kind, cid, line))


# keep last occurrence per (kind, id)
latest = {}
for kind, cid, line in entries:
    latest[(kind, cid)] = line

out_lines = []
seen = set()
# preserve ledger order but only the latest version of each id
ordered = []
for kind, cid, line in entries:
    if (kind, cid) in latest and (kind, cid) not in seen:
        seen.add((kind, cid))
        ordered.append(latest[(kind, cid)])

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(header + "\n" + "\n".join(ordered) + "\n")

print("entries before:", len(entries))
print("unique after dedupe:", len(ordered))
r_ids = {cid for (kind, cid) in latest if kind == "R"}
w_ids = {cid for (kind, cid) in latest if kind == "W"}
print("R ids:", len(r_ids), "W ids:", len(w_ids), "symmetric:", r_ids == w_ids)
