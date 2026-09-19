#!/usr/bin/env python3
"""Dedupe hsg-intermediate-solutions.mjs: keep the LAST definition of each
R["id"]/W["id"] one-liner (JS module semantics), drop earlier duplicates.
Idempotent; aborts if the file shape is unexpected."""
import io
import re

P = "scripts/content-authoring/hsg-intermediate-solutions.mjs"
src = io.open(P, encoding="utf-8").read()

HEADER_END = "const W = {};"
idx = src.index(HEADER_END) + len(HEADER_END)
head, body = src[:idx], src[idx:]

# split body into lines; entries are lines starting with R[" or W["
lines = body.split("\n")
entries = [ln for ln in lines if re.match(r'(R|W)\["', ln)]
others = [ln for ln in lines if not re.match(r'(R|W)\["', ln)]
nonempty_others = [ln for ln in others if ln.strip()]
if nonempty_others and nonempty_others != ["export { R, W };"]:
    print("UNEXPECTED non-entry content:", nonempty_others[:3])
    raise SystemExit(1)

def cid(ln):
    return re.match(r'(R|W)\["([^"]+)"\]', ln).group(2)

keep = {}
for i, ln in enumerate(entries):
    keep.setdefault(cid(ln), []).append(i)

drop = set()
for c, idxs in keep.items():
    if len(idxs) > 1:
        drop.update(idxs[:-1])  # keep last

out_entries = [ln for i, ln in enumerate(entries) if i not in drop]
out = head + "\n" + "\n".join(out_entries) + ("\n" if out_entries else "")
io.open(P, "w", encoding="utf-8").write(out)
print(f"entries {len(entries)} -> {len(out_entries)} (dropped {len(drop)} earlier duplicates)")
