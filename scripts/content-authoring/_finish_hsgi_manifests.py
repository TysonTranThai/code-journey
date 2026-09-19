#!/usr/bin/env python3
"""Finish the HSG Intermediate course: course.json + course.vi.json +
track.json/track.vi.json registering both HSG courses (Beginner first).
Module list = actual emitted module dirs, in the locked plan order."""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/hsg/courses/hsg-intermediate")
TRACK = os.path.join(ROOT, "src/content/tracks/hsg")

PLAN = [
    "hsgi-analysis", "hsgi-binsearch", "hsgi-intervals", "hsgi-greedy2",
    "hsgi-fenwick", "hsgi-segtree", "hsgi-dsu", "hsgi-dijkstra", "hsgi-topo",
    "hsgi-trees", "hsgi-seqdp", "hsgi-knap", "hsgi-bitmask", "hsgi-numth",
    "hsgi-strings", "hsgi-synthesis", "hsgi-debug", "hsgi-contests",
]

MODDIR = os.path.join(COURSE, "modules")
have = {d for d in os.listdir(MODDIR) if os.path.isfile(os.path.join(MODDIR, d, "module.json"))}
missing = [m for m in PLAN if m not in have]
extra = [d for d in os.listdir(MODDIR) if d not in PLAN]
if missing or extra:
    print("PLAN mismatch — missing:", missing, "extra:", extra)
    raise SystemExit(1)

course = {
    "id": "hsg-intermediate",
    "title": "Competitive Programming — High School Intermediate",
    "description": "The provincial-HSG level of the Vietnamese competitive-programming path: complexity budgets, binary search, interval sweeps, exchange-argument greedy, Fenwick and segment trees, DSU/MST, Dijkstra, DAG counting, tree algorithms, sequence/knapsack/bitmask DP, number theory, hashing and KMP, synthesis, debugging, and three mock contests — all graded in the C++20 sandbox.",
    "audience": "Students who finished the HSG Beginner course (or equivalent): fluent C++ I/O, arrays, sorting, prefix sums, basic DP and graphs, ready for provincial-level HSG Tin hoc.",
    "outcomes": [
        "Pick an algorithm from the constraint line and defend the complexity choice",
        "Implement Fenwick trees, segment trees, DSU, Dijkstra, and topological DP under contest time limits",
        "Derive sequence/knapsack/bitmask DP states and transitions from scratch",
        "Apply hashing, KMP, two pointers, and exchange-argument greedy with correctness arguments",
        "Debug defective contest programs systematically: reproduce, isolate, verify",
        "Sit three 120-minute mock contests, banking subtask points under time pressure",
    ],
    "prerequisites": ["hsg-beginner"],
    "modules": [{"reference": m} for m in PLAN],
}
course_vi = {
    "title": "Lập trình thi đấu — Học sinh giỏi trình độ trung cấp",
    "description": "Cấp độ HSG cấp tỉnh của lộ trình lập trình thi đấu: ngân sách độ phức tạp, tìm kiếm nhị phân, quét khoảng, tham lam đổi chỗ, cây Fenwick và cây đoạn, DSU/MST, Dijkstra, đếm trên DAG, thuật toán trên cây, quy hoạch động dãy/balo/bitmask, lý thuyết số, băm xâu và KMP, tổng hợp kỹ thuật, gỡ lỗi, và ba kỳ thi giả lập — chấm thật trong sandbox C++20.",
}

_w = lambda p, s: io.open(p, "w", encoding="utf-8").write(s)
_j = lambda o: json.dumps(o, indent=2, ensure_ascii=False) + "\n"

_w(os.path.join(COURSE, "course.json"), _j(course))
_w(os.path.join(COURSE, "course.vi.json"), _j(course_vi))

track = json.load(io.open(os.path.join(TRACK, "track.json"), encoding="utf-8"))
refs = [c["reference"] for c in track["courses"]]
if "hsg-beginner" not in refs:
    track["courses"] = [{"reference": "hsg-beginner"}] + track["courses"]
if "hsg-intermediate" not in refs:
    track["courses"].append({"reference": "hsg-intermediate"})
_w(os.path.join(TRACK, "track.json"), _j(track))
print("course.json + course.vi.json written; track.json courses:", [c["reference"] for c in track["courses"]])
