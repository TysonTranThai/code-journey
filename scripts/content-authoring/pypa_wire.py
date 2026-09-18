#!/usr/bin/env python3
"""One-time wiring for python-advanced:
- create the missing production-apis module manifests (EN + VI)
- append each module's checkpoint lesson to its manifest (consistent with beginner)
- fill course.json modules (curriculum order)
- register the course in track.json
Idempotent: safe to re-run.
"""
import json
import os

ROOT = "src/content/tracks/python/courses/python-advanced"
MODS = os.path.join(ROOT, "modules")
ORDER = [
    "data-model-protocols",
    "metaprogramming",
    "advanced-typing",
    "concurrency-parallelism",
    "structured-async",
    "performance-engineering",
    "cpython-internals",
    "architecture-patterns",
    "production-apis",
    "distributed-systems",
    "databases-data-access",
    "security-engineering",
    "advanced-testing",
    "production-tooling",
    "capstone-production-platform",
]

# ── 1. production-apis manifest ──────────────────────────────────────────────
pa_dir = os.path.join(MODS, "production-apis")
pa_manifest = os.path.join(pa_dir, "module.json")
if not os.path.exists(pa_manifest):
    lesson_files = sorted(
        f for f in os.listdir(os.path.join(pa_dir, "lessons"))
        if f.endswith(".json") and not f.endswith(".vi.json")
    )
    lesson_ids = [f[: -len(".json")] for f in lesson_files]
    lessons = [i for i in lesson_ids if "checkpoint" not in i]
    cp = [i for i in lesson_ids if "checkpoint" in i]

    def meta(mod, lid, vi=False):
        suffix = ".vi" if vi else ""
        p = os.path.join(MODS, mod, "lessons", f"{lid}{suffix}.json")
        with open(p, encoding="utf-8") as f:
            return json.load(f)

    v1 = meta("production-apis", "api-design-contracts", vi=True)
    manifest = {
        "id": "production-apis",
        "title": "Production APIs",
        "summary": (
            "Design HTTP APIs as contracts — precise status codes, envelopes, pagination and "
            "idempotency keys — then harden them with layered validation, problem-details error "
            "shapes, and the production concerns that keep serving when dependencies wobble."
        ),
        "lessons": [{"reference": r} for r in lessons + cp],
        "practices": [
            {"reference": "pa-p9-design-practice"},
            {"reference": "pa-p9-validation-practice"},
            {"reference": "pa-p9-api-project"},
        ],
    }
    with open(pa_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    vi_manifest = {
        "title": v1.get("_module_title", "API trực tiếp môi trường sản xuất"),
        "summary": (
            "Thiết kế API HTTP như một hợp đồng — mã trạng thái chính xác, cấu trúc phản hồi, "
            "phân trang và idempotency key — rồi gia cố bằng lớp xác thực, hình dạng lỗi "
            "problem-details và những mối quan tâm vận hành giúp dịch vụ vẫn sống khi phụ thuộc trục trặc."
        ),
    }
    with open(os.path.join(pa_dir, "module.vi.json"), "w", encoding="utf-8") as f:
        json.dump(vi_manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("created production-apis manifests; lessons:", lesson_ids)
else:
    print("production-apis manifest already exists")

# ── 2. normalize: checkpoint lesson appended to every manifest ───────────────
for name in ORDER:
    mdir = os.path.join(MODS, name)
    mpath = os.path.join(mdir, "module.json")
    with open(mpath, encoding="utf-8") as f:
        m = json.load(f)
    refs = [l["reference"] for l in m["lessons"]]
    cps = [d for d in os.listdir(os.path.join(mdir, "lessons")) if os.path.isdir(os.path.join(mdir, "lessons", d)) and d.startswith("pa-checkpoint")]
    if cps and not any("checkpoint" in r for r in refs):
        assert len(cps) == 1, (name, cps)
        m["lessons"].append({"reference": cps[0]})
        with open(mpath, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"appended checkpoint {cps[0]} to {name}")

# ── 3. course.json modules ───────────────────────────────────────────────────
cpath = os.path.join(ROOT, "course.json")
with open(cpath, encoding="utf-8") as f:
    course = json.load(f)
for name in ORDER:
    mpath = os.path.join(MODS, name, "module.json")
    assert os.path.exists(mpath), mpath
if [m.get("reference") for m in course["modules"]] != ORDER:
    course["modules"] = [{"reference": r} for r in ORDER]
    with open(cpath, "w", encoding="utf-8") as f:
        json.dump(course, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("course.json modules filled:", len(ORDER))
else:
    print("course.json already wired")

# ── 4. track.json ────────────────────────────────────────────────────────────
tpath = "src/content/tracks/python/track.json"
with open(tpath, encoding="utf-8") as f:
    track = json.load(f)
refs = [c["reference"] for c in track["courses"]]
if "python-advanced" not in refs:
    track["courses"].append({"reference": "python-advanced"})
    with open(tpath, "w", encoding="utf-8") as f:
        json.dump(track, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("track.json: python-advanced registered")
else:
    print("track.json already registers python-advanced")

print("WIRING DONE")
