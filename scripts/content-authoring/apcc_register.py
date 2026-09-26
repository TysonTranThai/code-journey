#!/usr/bin/env python3
"""Additively register ap-csa-core in the ap-csa track manifests."""
import io
import json
import os

TRACK = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "src/content/tracks/ap-csa",
)

for name in ("track.json",):
    path = os.path.join(TRACK, name)
    with io.open(path, encoding="utf-8") as f:
        data = json.load(f)
    refs = [c["reference"] for c in data.get("courses", [])]
    if "ap-csa-core" not in refs:
        data["courses"].append({"reference": "ap-csa-core"})
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print("registered ap-csa-core in", name)
    else:
        print("already registered in", name)
