#!/usr/bin/env python3
"""
Python authoring library for the Intermediate course (Course 2).

Emits byte-compatible shapes with scripts/content-authoring/i2-lib.mjs:
  - module.json / module.vi.json
  - lessons/<id>.json/.vi.json + .mdx/.vi.mdx
  - lessons/<id>/challenges/<cid>.json/.vi.json (checkpoints)
  - practices/<set>.json/.vi.json + challenges/<cid>.json/.vi.json
  - appends R/W solutions to scripts/content-authoring/i2-solutions.mjs

Python triple-quoted strings hold MDX bodies directly (no backtick/${} hazards),
and json.dump guarantees valid JS-compatible JSON for prompts and test code.
"""

import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(
    ROOT,
    "src/content/tracks/web-development/courses/web-development-intermediate",
)
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/i2-solutions.mjs")


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


def write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="intermediate"):
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


def _challenge(cid, title, prompt, boilerplate, tests, level, difficulty="intermediate"):
    return {
        "id": cid,
        "title": title,
        "prompt": prompt,
        "difficulty": difficulty,
        "level": level,
        "boilerplate": boilerplate,
        "tests": [
            {"name": n, "code": c, "hint": h} for (n, c, h) in tests
        ],
    }


def _vi_challenge(vi_title, vi_prompt, vi_tests):
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


def write_checkpoint(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, challenge, vi_challenge):
    write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
    d = os.path.join(mod_dir(m), "lessons", lid, "challenges")
    _w(os.path.join(d, challenge["id"] + ".json"), _j(challenge))
    _w(os.path.join(d, challenge["id"] + ".vi.json"), _j(vi_challenge))
    print("  checkpoint challenge:", challenge["id"])


def fn_wrap(code, ret):
    """Standard test preamble: build fn from learner code returning `ret` keys."""
    return (
        'const fn = new Function(code + "\\nreturn { ' + ret + ' };");\n'
        "const { " + ret + " } = fn();"
    )
