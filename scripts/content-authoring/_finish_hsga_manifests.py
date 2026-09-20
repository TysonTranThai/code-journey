#!/usr/bin/env python3
"""Write the hsg-advanced course manifest and register it on the hsg track."""
import io, os, json

BASE = os.path.join("src", "content", "tracks", "hsg")
COURSE = os.path.join(BASE, "courses", "hsg-advanced")


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def _w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


MODULES = [
    "hsga-attack",     # M1  meet-in-the-middle, XOR tricks, constructive
    "hsga-lazy",       # M2  lazy segment trees (assign/add, max subarray)
    "hsga-fenwick2",   # M3  Fenwick variants (kth descent, offline, inversion)
    "hsga-lift",       # M4  binary lifting + LCA
    "hsga-treedp",     # M5  tree DP
    "hsga-hld",        # M6  heavy-light decomposition
    "hsga-euler",      # M7  Euler tour + subtree queries
    "hsga-scc",        # M8  SCC & condensation
    "hsga-flow",       # M9  max flow & bipartite matching
    "hsga-digitdp",    # M10 digit DP
    "hsga-intervaldp", # M11 interval DP
    "hsga-suffix",     # M12 suffix structures (hashing, Z, trie, suffix array)
    "hsga-numth2",     # M13 advanced number theory (CRT, phi, combinatorics mod)
    "hsga-combi",      # M14 combinatorics (inclusion-exclusion, Catalan)
    "hsga-geom",       # M15 computational geometry
    "hsga-synth",      # M16 technique synthesis
    "hsga-debug",      # M17 debugging under contest load
    "hsga-contests",   # M18 contest series I (structures + graphs)
    "hsga-contests2",  # M19 contest series II (trees + strings)
    "hsga-contests3",  # M20 final HSG simulation
]

COURSE_EN = {
    "id": "hsg-advanced",
    "title": "Competitive Programming — High School Advanced",
    "description": (
        "The top level of the Vietnamese competitive-programming path, toward national and "
        "olympiad-style problems: lazy trees, binary lifting, tree DP, HLD, SCC, flow and matching, "
        "digit/interval/suffix DP, number theory, combinatorics, geometry, synthesis, debugging, "
        "and mock contests — all graded in the C++20 sandbox."
    ),
    "audience": (
        "Students who finished the HSG Intermediate course (or equivalent): fluent with segment trees, "
        "DSU, Dijkstra, DAG DP, bitmask DP, modular arithmetic, and KMP, ready for national-level "
        "HSG Tin hoc and olympiad preparation."
    ),
    "outcomes": [
        "Derive and prove algorithms for unfamiliar problems from constraints and structure",
        "Implement lazy segment trees, HLD, binary lifting, SCC, and flow networks under contest limits",
        "Model problems as digit DP, interval DP, tree DP, or network flow and defend the transformation",
        "Apply suffix structures, Mobius counting, and integer geometry with correctness arguments",
        "Combine multiple techniques in synthesis problems and stress-test solutions against brute force",
        "Sit six graded mock-contest problems per series, banking partial credit under time pressure",
    ],
    "prerequisites": ["hsg-intermediate"],
    "modules": [{"reference": m} for m in MODULES],
}

COURSE_VI = {
    "title": "Lập trình thi đấu — Trung học chuyên sâu",
    "description": (
        "Bậc cao nhất của lộ trình lập trình thi đấu Việt Nam, hướng tới quốc gia và Olympic: "
        "cây đoạn lười, binary lifting, DP cây, HLD, SCC, max flow và ghép cặp, digit/interval/suffix DP, "
        "lý thuyết số, tổ hợp, hình học, tổng hợp kỹ thuật, gỡ lỗi và kỳ thi giả lập — chấm trong sandbox C++20."
    ),
}

_w(os.path.join(COURSE, "course.json"), _j(COURSE_EN))
_w(os.path.join(COURSE, "course.vi.json"), _j(COURSE_VI))

# register on the track (additive: append after hsg-intermediate)
track_path = os.path.join(BASE, "track.json")
track = json.load(io.open(track_path, encoding="utf-8"))
refs = [c["reference"] for c in track["courses"]]
if "hsg-advanced" not in refs:
    track["courses"].append({"reference": "hsg-advanced"})
    _w(track_path, _j(track))
else:
    print("track.json already registers hsg-advanced")

track_vi_path = os.path.join(BASE, "track.vi.json")
if os.path.exists(track_vi_path):
    tvi = json.load(io.open(track_vi_path, encoding="utf-8"))
    vrefs = [c["reference"] for c in tvi.get("courses", [])]
    if "hsg-advanced" not in vrefs:
        tvi.setdefault("courses", []).append({"reference": "hsg-advanced"})
        _w(track_vi_path, _j(tvi))
    else:
        print("track.vi.json already registers hsg-advanced")

print("hsg-advanced manifests complete")
