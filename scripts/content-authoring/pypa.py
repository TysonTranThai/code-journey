#!/usr/bin/env python3
"""
Authoring library for the Python — Advanced course (python track).

Mirrors scripts/content-authoring/pypb.py but writes to
src/content/tracks/python/courses/python-advanced and emits Python-language
challenges (language: "python") with the pa-* challenge-id namespace.
Solutions append to scripts/content-authoring/py-solutions.mjs (shared ledger,
same two-sided harness contract). Graded code targets Python 3.11.
"""

import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/python")
BASE = os.path.join(TRACK, "courses/python-advanced")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/py-solutions.mjs")


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def mod_dir(m):
    return os.path.join(BASE, "modules", m)


def write_module(m, title, summary, vi_title, vi_summary, lessons, practices):
    _w(
        os.path.join(mod_dir(m), "module.json"),
        _j(
            {
                "id": m,
                "title": title,
                "summary": summary,
                "lessons": [{"reference": l} for l in lessons],
                "practices": [{"reference": p} for p in practices],
            }
        ),
    )
    _w(
        os.path.join(mod_dir(m), "module.vi.json"),
        _j({"title": vi_title, "summary": vi_summary}),
    )
    print("module:", m)


def write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="advanced"):
    d = os.path.join(mod_dir(m), "lessons")
    _w(
        os.path.join(d, lid + ".json"),
        _j(
            {
                "id": lid,
                "title": title,
                "description": description,
                "minutes": minutes,
                "difficulty": difficulty,
                "contentPath": "./" + lid + ".mdx",
            }
        ),
    )
    _w(os.path.join(d, lid + ".vi.json"), _j({"title": vi_title, "description": vi_description}))
    _w(os.path.join(d, lid + ".mdx"), mdx.strip() + "\n")
    _w(os.path.join(d, lid + ".vi.mdx"), vi_mdx.strip() + "\n")
    print("lesson:", m + "/" + lid)


def challenge(cid, title, prompt, boilerplate, tests, level=None, difficulty="advanced"):
    """Python-language challenge. tests = [(name, code, hint), ...]."""
    out = {
        "id": cid,
        "title": title,
        "prompt": prompt,
        "difficulty": difficulty,
        "language": "python",
        "boilerplate": boilerplate,
        "tests": [{"name": n, "code": c, "hint": h} for (n, c, h) in tests],
    }
    if level:
        out["level"] = level
    return out


def vi_challenge(vi_title, vi_prompt, vi_tests):
    return {
        "title": vi_title,
        "prompt": vi_prompt,
        "tests": [{"name": n, "hint": h} for (n, h) in vi_tests],
    }


def write_practice(m, sid, title, description, vi_title, vi_description, after_lesson, minutes, difficulty, challenges, vi_challenges, solutions=None):
    d = os.path.join(mod_dir(m), "practices")
    _w(
        os.path.join(d, sid + ".json"),
        _j(
            {
                "id": sid,
                "title": title,
                "description": description,
                "afterLesson": after_lesson,
                "minutes": minutes,
                "difficulty": difficulty,
                "challenges": [c["id"] for c in challenges],
            }
        ),
    )
    _w(os.path.join(d, sid + ".vi.json"), _j({"title": vi_title, "description": vi_description}))
    for c in challenges:
        _w(os.path.join(d, sid, "challenges", c["id"] + ".json"), _j(c))
    for cid, vc in vi_challenges.items():
        _w(os.path.join(d, sid, "challenges", cid + ".vi.json"), _j(vc))
    if solutions:
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            for cid, ref, wrong in solutions:
                f.write("R[" + json.dumps(cid) + "] = " + json.dumps(ref) + ";\n")
                f.write("W[" + json.dumps(cid) + "] = " + json.dumps(wrong) + ";\n")
    print("practice set:", m + "/" + sid)


def write_checkpoint(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, ch, vi_ch, solution=None, wrong=None):
    """Checkpoint lesson with a lesson-attached challenge (+ optional solution pair)."""
    write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
    d = os.path.join(mod_dir(m), "lessons", lid, "challenges")
    _w(os.path.join(d, ch["id"] + ".json"), _j(ch))
    _w(os.path.join(d, ch["id"] + ".vi.json"), _j(vi_ch))
    if solution is not None and wrong is not None:
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("R[" + json.dumps(ch["id"]) + "] = " + json.dumps(solution) + ";\n")
            f.write("W[" + json.dumps(ch["id"]) + "] = " + json.dumps(wrong) + ";\n")
    print("  checkpoint challenge:", ch["id"])
