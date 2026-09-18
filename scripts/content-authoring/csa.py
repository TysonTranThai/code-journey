"""Code Journey — C# Advanced authoring helpers (course csharp-advanced).

Emit EN JSON+MDX and VI sidecars/overlays with the same file layout the C#
Beginner course uses (loader contract), enforce slug/ID uniqueness, and
collect the solutions ledger for the two-sided QA harness.

Run from repo root:  python3 scripts/content-authoring/csa_emit.py
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COURSE_DIR = os.path.join(ROOT, "src/content/tracks/csharp/courses/csharp-advanced")
COURSE = "csharp-advanced"
TRACK = "csharp"

# ---------------------------------------------------------------------------
# Registries (filled by the csa_mXX.py content modules, emitted by csa_emit)
# ---------------------------------------------------------------------------

MODULES: list[dict] = []       # {id,title,summary,lessons:[...],practices:[...]}
LESSONS: list[dict] = []       # {id,module,title,description,minutes,difficulty,mdx,mdx_vi}
PRACTICES: list[dict] = []     # {id,module,title,description,minutes,difficulty,afterLesson,challenges:[ids]}
CHALLENGES: dict[str, dict] = {}  # id -> challenge dict (EN) incl. boilerplate/tests/reference/wrong
LEVELS: dict[str, str] = {}    # practice challenge id -> deliberate-practice level
CHECKPOINT_CHALLENGES: set[str] = set()  # lesson-attached checkpoint challenge ids

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
USED_IDS: dict[str, str] = {}

# Boilerplate: every C# challenge carries explicit usings (raw csc has no
# implicit-usings flag — probed). Advanced challenges get the standard set.
DEFAULT_BOILERPLATE = (
    "using System;\n"
    "using System.Buffers;\n"
    "using System.Collections.Concurrent;\n"
    "using System.Collections.Generic;\n"
    "using System.Collections.Immutable;\n"
    "using System.Diagnostics;\n"
    "using System.Diagnostics.Metrics;\n"
    "using System.Diagnostics.Tracing;\n"
    "using System.Globalization;\n"
    "using System.IO;\n"
    "using System.IO.Pipelines;\n"
    "using System.Linq;\n"
    "using System.Linq.Expressions;\n"
    "using System.Net;\n"
    "using System.Net.Http;\n"
    "using System.Net.Sockets;\n"
    "using System.Reflection;\n"
    "using System.Reflection.Metadata;\n"
    "using System.Reflection.PortableExecutable;\n"
    "using System.Runtime.CompilerServices;\n"
    "using System.Runtime.InteropServices;\n"
    "using System.Runtime.Loader;\n"
    "using System.Security.Cryptography;\n"
    "using System.Text;\n"
    "using System.Text.Json;\n"
    "using System.Threading;\n"
    "using System.Threading.Channels;\n"
    "using System.Threading.Tasks;\n"
)


def slug(value: str, kind: str) -> str:
    if not SLUG_RE.match(value):
        raise ValueError(f"invalid slug for {kind}: {value!r}")
    if value in USED_IDS and USED_IDS[value] != kind:
        raise ValueError(f"duplicate id across kinds: {value!r} ({USED_IDS[value]} vs {kind})")
    USED_IDS[value] = kind
    return value


def register_module(mid: str, title: str, summary: str) -> str:
    slug(mid, "module")
    MODULES.append({"id": mid, "title": title, "summary": summary, "lessons": [], "practices": []})
    return mid


def register_lesson(module_id: str, lid: str, title: str, description: str, minutes: int,
                    difficulty: str, mdx: str, mdx_vi: str) -> str:
    slug(lid, "lesson")
    if minutes < 1 or minutes > 240:
        raise ValueError(f"lesson {lid}: minutes out of range")
    if difficulty not in ("beginner", "intermediate", "advanced"):
        raise ValueError(f"lesson {lid}: invalid difficulty")
    if len(description) < 1 or len(description) > 400:
        raise ValueError(f"lesson {lid}: description length {len(description)} (max 400)")
    LESSONS.append({
        "id": lid, "module": module_id, "title": title, "description": description,
        "minutes": minutes, "difficulty": difficulty, "mdx": mdx, "mdx_vi": mdx_vi,
    })
    for m in MODULES:
        if m["id"] == module_id:
            m["lessons"].append(lid)
            return lid
    raise ValueError(f"lesson {lid}: unknown module {module_id}")


def register_practice(module_id: str, pid: str, title: str, description: str, minutes: int,
                      difficulty: str, after_lesson: str, challenge_ids: list[str]) -> str:
    slug(pid, "practice")
    if minutes < 1 or minutes > 240:
        raise ValueError(f"practice {pid}: minutes out of range")
    if difficulty not in ("beginner", "intermediate", "advanced"):
        raise ValueError(f"practice {pid}: invalid difficulty")
    if len(description) < 1 or len(description) > 400:
        raise ValueError(f"practice {pid}: description length {len(description)}")
    PRACTICES.append({
        "id": pid, "module": module_id, "title": title, "description": description,
        "minutes": minutes, "difficulty": difficulty, "afterLesson": after_lesson,
        "challenges": challenge_ids,
    })
    for m in MODULES:
        if m["id"] == module_id:
            m["practices"].append(pid)
            return pid
    raise ValueError(f"practice {pid}: unknown module {module_id}")


VALID_LEVELS = {"imitation", "guided", "independent", "combination", "real-world", "debugging", "mini-build"}


def register_challenge(cid: str, module_id: str, *, title: str, prompt: str, difficulty: str,
                       tests: list[dict], reference: str, wrong: str,
                       level: str | None = None, boilerplate: str = DEFAULT_BOILERPLATE,
                       checkpoint: bool = False) -> str:
    slug(cid, "challenge")
    if level is not None and level not in VALID_LEVELS:
        raise ValueError(f"challenge {cid}: invalid level {level!r}")
    if checkpoint:
        CHECKPOINT_CHALLENGES.add(cid)
        if level is not None:
            raise ValueError(f"challenge {cid}: checkpoint challenges omit level")
    else:
        if level is None:
            raise ValueError(f"challenge {cid}: practice challenges require a level")
        LEVELS[cid] = level
    if not tests:
        raise ValueError(f"challenge {cid}: at least one test required")
    for t in tests:
        if not t.get("hint") or len(t["hint"]) > 400:
            raise ValueError(f"challenge {cid}: each test needs a hint (max 400 chars)")
    if len(prompt) > 4000:
        raise ValueError(f"challenge {cid}: prompt too long ({len(prompt)})")
    CHALLENGES[cid] = {
        "id": cid, "module": module_id, "title": title, "prompt": prompt,
        "difficulty": difficulty, "language": "csharp", "boilerplate": boilerplate,
        "tests": tests, "reference": reference, "wrong": wrong,
    }
    return cid


# ---------------------------------------------------------------------------
# Emitters
# ---------------------------------------------------------------------------

def _write_json(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def emit() -> None:
    # Course manifest
    _write_json(os.path.join(COURSE_DIR, "course.json"), {
        "id": COURSE,
        "title": "C# — Advanced",
        "description": (
            "Understand why .NET behaves the way it does: memory and the GC, advanced type "
            "system and generics, delegates and expression trees, reflection and Roslyn "
            "metaprogramming, async and concurrency internals, channels and backpressure, "
            "performance engineering that measures first, diagnostics, native interop, "
            "security, and a production capstone — every challenge executed in the real "
            ".NET 10 sandbox."
        ),
        "audience": (
            "Developers who finished C# Intermediate and want runtime-level depth: memory, "
            "concurrency, metaprogramming, performance, security, and production architecture."
        ),
        "outcomes": [
            "Reason about value/reference semantics, boxing, and the memory model",
            "Write advanced generic abstractions with variance and static abstracts",
            "Build delegates, closures, and expression trees deliberately",
            "Use reflection, analyzers, and source generators safely",
            "Master async internals: state machines, ValueTask, cancellation",
            "Diagnose races, deadlocks, and memory leaks with evidence",
            "Engineer performance by measuring allocations and collections",
            "Read IL and metadata with PEReader/MetadataReader",
            "Design channels, backpressure, and graceful shutdown pipelines",
            "Apply security thinking: injection, deserialization, SSRF, secrets",
            "Ship a distributed-style job platform with retries and idempotency",
        ],
        "prerequisites": ["csharp-intermediate"],
        "modules": [{"reference": m["id"]} for m in MODULES],
    })
    # VI course manifest (complete technical translation)
    _write_json(os.path.join(COURSE_DIR, "course.vi.json"), {
        "id": COURSE,
        "title": "C# — Nâng cao",
        "description": (
            "Hiểu vì sao .NET hành xử như vậy: bộ nhớ và GC, hệ thống kiểu nâng cao, delegate "
            "và expression tree, reflection và metaprogramming với Roslyn, nội bộ async và "
            "đồng thời, channels và backpressure, kỹ năng hiệu năng đo lường trước, diagnostics, "
            "interop thuần, bảo mật, và capstone cấp production — mọi challenge đều được thực "
            "thi trong sandbox .NET 10 thật."
        ),
        "audience": (
            "Lập trình viên đã hoàn thành C# Intermediate và muốn chiều sâu cấp runtime: bộ nhớ, "
            "đồng thời, metaprogramming, hiệu năng, bảo mật và kiến trúc production."
        ),
        "outcomes": [
            "Lý giải ngữ nghĩa value/reference, boxing và mô hình bộ nhớ",
            "Xây dựng trừu tượng generic nâng cao với variance và static abstract",
            "Dùng delegate, closure và expression tree một cách có chủ đích",
            "Dùng reflection, analyzer và source generator an toàn",
            "Nắm nội bộ async: state machine, ValueTask, cancellation",
            "Chẩn đoán race, deadlock và rò rỉ bộ nhớ bằng bằng chứng",
            "Tối ưu hiệu năng bằng cách đo cấp phát và bộ đếm GC",
            "Đọc IL và metadata với PEReader/MetadataReader",
            "Thiết kế pipeline channels, backpressure và tắt dữ dội",
            "Áp dụng tư duy bảo mật: injection, deserialization, SSRF, secret",
            "Hoàn thành nền tảng xử lý job phân tán với retry và idempotency",
        ],
        "prerequisites": ["csharp-intermediate"],
        "modules": [{"reference": m["id"]} for m in MODULES],
    })

    for m in MODULES:
        mdir = os.path.join(COURSE_DIR, "modules", m["id"])
        _write_json(os.path.join(mdir, "module.json"), {
            "id": m["id"], "title": m["title"], "summary": m["summary"],
            "lessons": [{"reference": l} for l in m["lessons"]],
            "practices": [{"reference": p} for p in m["practices"]],
        })
        import csa_vi_meta
        vt, vs = csa_vi_meta.VI_MODULES[m["id"]]
        _write_json(os.path.join(mdir, "module.vi.json"), {
            "id": m["id"], "title": vt, "summary": vs,
            "lessons": [{"reference": l} for l in m["lessons"]],
            "practices": [{"reference": p} for p in m["practices"]],
        })

    for l in LESSONS:
        ldir = os.path.join(COURSE_DIR, "modules", l["module"], "lessons")
        _write_json(os.path.join(ldir, f"{l['id']}.json"), {
            "id": l["id"], "title": l["title"], "description": l["description"],
            "minutes": l["minutes"], "difficulty": l["difficulty"],
            "contentPath": f"./{l['id']}.mdx",
        })
        import csa_vi_meta
        lt, ld = csa_vi_meta.VI_LESSONS[l["id"]]
        _write_json(os.path.join(ldir, f"{l['id']}.vi.json"), {
            "id": l["id"], "title": lt, "description": ld,
            "minutes": l["minutes"], "difficulty": l["difficulty"],
            "contentPath": f"./{l['id']}.vi.mdx",
        })
        _write_text(os.path.join(ldir, f"{l['id']}.mdx"), l["mdx"])
        _write_text(os.path.join(ldir, f"{l['id']}.vi.mdx"), l["mdx_vi"])

    for p in PRACTICES:
        pdir = os.path.join(COURSE_DIR, "modules", p["module"], "practices")
        data = {
            "id": p["id"], "title": p["title"], "description": p["description"],
            "minutes": p["minutes"], "difficulty": p["difficulty"],
            "challenges": p["challenges"],
        }
        if p["afterLesson"]:
            data["afterLesson"] = p["afterLesson"]
        _write_json(os.path.join(pdir, f"{p['id']}.json"), data)
        import csa_vi_meta
        pt, pd = csa_vi_meta.VI_PRACTICES[p["id"]]
        _write_json(os.path.join(pdir, f"{p['id']}.vi.json"), {**data, "title": pt, "description": pd})

    for cid, c in CHALLENGES.items():
        module_id = c["module"]
        # Lesson-attached checkpoint challenges live in lessons/<id>/challenges;
        # practice challenges live in practices/<pid>/challenges.
        placed = False
        for p in PRACTICES:
            if cid in p["challenges"]:
                cdir = os.path.join(COURSE_DIR, "modules", module_id, "practices", p["id"], "challenges")
                _write_json(os.path.join(cdir, f"{cid}.json"), {
                    "id": cid, "title": c["title"], "prompt": c["prompt"],
                    "difficulty": c["difficulty"], "language": "csharp",
                    "boilerplate": c["boilerplate"],
                    "tests": [{"name": t["name"], "code": t["code"], "hint": t["hint"]} for t in c["tests"]],
                    "level": LEVELS.get(cid),
                })
                placed = True
                break
        if placed:
            continue
        for l in LESSONS:
            if l["module"] == module_id and cid.startswith(l["id"]):
                cdir = os.path.join(COURSE_DIR, "modules", module_id, "lessons", l["id"], "challenges")
                _write_json(os.path.join(cdir, f"{cid}.json"), {
                    "id": cid, "title": c["title"], "prompt": c["prompt"],
                    "difficulty": c["difficulty"], "language": "csharp",
                    "boilerplate": c["boilerplate"],
                    "tests": [{"name": t["name"], "code": t["code"], "hint": t["hint"]} for t in c["tests"]],
                })
                placed = True
                break
        if not placed:
            raise ValueError(f"challenge {cid}: no placement found (practice or lesson dir)")

    # VI overlays: challenge title+prompt+test hints (code/boilerplate stay EN
    # per the loader contract — see Beginner/Intermediate precedent).
    import csa_vi
    merged_vi = dict(csa_vi.VI)
    for extra in ("csa_vi2", "csa_vi3"):
        mod = __import__(extra)
        for k, v in mod.VI.items():
            if k in merged_vi:
                raise ValueError(f"duplicate VI overlay for challenge {k}")
            merged_vi[k] = v
    vi_overlays(merged_vi)

    # VI overlays: challenge title+prompt+test hints (code/boilerplate stay EN
    # per the loader contract — see Beginner/Intermediate precedent).
    import csa_vi
    merged_vi = dict(csa_vi.VI)
    for extra in ("csa_vi2", "csa_vi3"):
        mod = __import__(extra)
        for k, v in mod.VI.items():
            if k in merged_vi:
                raise ValueError(f"duplicate VI overlay for challenge {k}")
            merged_vi[k] = v
    vi_overlays(merged_vi)
    # Ledger for the two-sided harness
    with open(os.path.join(os.path.dirname(__file__), "csa-solutions.mjs"), "w", encoding="utf-8") as f:
        f.write("// Auto-generated by csa.py emit() — solutions ledger for C# Advanced.\n")
        f.write("export const R = " + json.dumps({cid: c["reference"] for cid, c in CHALLENGES.items()},
                                                 ensure_ascii=False, indent=2) + ";\n\n")
        f.write("export const W = " + json.dumps({cid: c["wrong"] for cid, c in CHALLENGES.items()},
                                                 ensure_ascii=False, indent=2) + ";\n")
    print(f"emitted: {len(MODULES)} modules, {len(LESSONS)} lessons, {len(PRACTICES)} practices, "
          f"{len(CHALLENGES)} challenges")


def vi_overlays(vi: dict) -> None:
    """VI overlays for challenges: {cid: {"title","prompt","hints": {test: hint}}}."""
    for cid, c in CHALLENGES.items():
        v = vi.get(cid)
        if not v:
            raise ValueError(f"challenge {cid}: missing VI overlay")
        for t in c["tests"]:
            if t["name"] not in v.get("hints", {}):
                raise ValueError(f"challenge {cid}/{t['name']}: missing VI hint")
        module_id = c["module"]
        for p in PRACTICES:
            if cid in p["challenges"]:
                cdir = os.path.join(COURSE_DIR, "modules", module_id, "practices", p["id"], "challenges")
                _write_json(os.path.join(cdir, f"{cid}.vi.json"), {
                    "title": v["title"], "prompt": v["prompt"],
                    "tests": [{"name": t["name"], "hint": v["hints"][t["name"]]} for t in c["tests"]],
                })
                break
        else:
            for l in LESSONS:
                if l["module"] == module_id and cid.startswith(l["id"]):
                    cdir = os.path.join(COURSE_DIR, "modules", module_id, "lessons", l["id"], "challenges")
                    _write_json(os.path.join(cdir, f"{cid}.vi.json"), {
                        "title": v["title"], "prompt": v["prompt"],
                        "tests": [{"name": t["name"], "hint": v["hints"][t["name"]]} for t in c["tests"]],
                    })
                    break


def vi_lesson_overlay(lid: str, *, title: str, description: str) -> None:
    l = next(x for x in LESSONS if x["id"] == lid)
    ldir = os.path.join(COURSE_DIR, "modules", l["module"], "lessons")
    _write_json(os.path.join(ldir, f"{lid}.vi.json"), {
        "title": title, "description": description,
    })


def vi_module_overlay(mid: str, *, title: str, summary: str) -> None:
    _write_json(os.path.join(COURSE_DIR, "modules", mid, "module.vi.json"), {
        "title": title, "summary": summary,
    })


def vi_practice_overlay(pid: str, *, title: str, description: str) -> None:
    p = next(x for x in PRACTICES if x["id"] == pid)
    pdir = os.path.join(COURSE_DIR, "modules", p["module"], "practices", p["id"])
    _write_json(os.path.join(pdir, f"{pid}.vi.json"), {
        "title": title, "description": description,
    })
