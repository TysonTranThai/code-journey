#!/usr/bin/env python3
"""
Authoring library for C — Advanced (c track, course 3).

Clones cb.py (C Beginner) so shapes stay byte-compatible with the platform
loaders. Writes to src/content/tracks/c/courses/c-advanced; challenges are
language:"c" (difficulty "advanced"); solution pairs append to
scripts/content-authoring/ca-solutions.mjs (R[id] = reference source,
W[id] = intentionally wrong source) for the two-sided harness
verify-challenges-ca.mjs.

Environment policy (probed in the real sandbox, see
docs/CURRICULUM-RESEARCH-C-ADVANCED.md): gcc 14.2.0 -std=c23; POSIX symbols
require a feature macro in the challenge boilerplate (probed: works even
though the test harness includes headers first — musl re-guards at each
include point); pthreads/atomics/sockets/mmap/fork all work; NO make/cmake/
gdb/valgrind/sanitizers (never claimed); binutils (nm/objdump/readelf/ar) are
available and drivable from tests via system(); host arch is aarch64 (assembly
content stays arch-guarded/property-based).
"""

import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/c")
BASE = os.path.join(TRACK, "courses/c-advanced")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/ca-solutions.mjs")

# Zero-backslash authoring: escape layers in tool transports are unreliable, so
# batch scripts NEVER type a backslash. C newline escapes are written as @CE@
# inside triple-quoted strings and expanded here via chr(92).
B = chr(92)
CE = B + "n"  # the two characters backslash+n (C newline escape, inside C strings)
NL = chr(10)  # a real newline (between C statements, markdown line breaks)


# Runtime placeholder registry. Batch files never type quotes/backslashes into
# C string literals; they write @NAME@ tokens, expanded here. Inside C string
# literals the content is spliced in escaped; outside, it becomes a real
# quoted C literal. Built entirely with chr() so no transport can mangle it.
import re as _re

DQ = chr(34)  # double quote
PLACEHOLDERS = {
    "@T1@": "echo pipe-ok",
    "@T2@": "pipe-ok",
    "@T3@": "exit 3",
    "@T4@": "exit 0",
    "@T5@": "CJ_DEFINITELY_UNSET_XYZ",
    "@T6@": "fallback",
    "@T7@": "PATH",
    "@T8@": "none",
    "@T9@": "x",
    "@T10@": "A",
    "@TPATH@": "/tmp/cj_ca21_pattern.bin",
    "@TMISS@": "/tmp/cj_definitely_missing.bin",
    "@TLINES@": "/tmp/cj_ca21_lines.txt",
    "@TLINE@": "line.\\n",
    "@TL1@": "interleaved",
    "@TL2@": "split",
    "@TBIG@": "big",
    "@TPR@": "world:42",
    "@TBAD@": "exit:x",
    "@GS1@": "hello",
    "@GS2@": "-",
    "@GS3@": "world",
    "@GS4@": "hello-world",
    "@FDSH@": "/bin/sh",
    "@FDsh@": "sh",
    "@FDdashc@": "-c",
    "@J1@": "true",
    "@J2@": "true",
    "@J3@": "exit 5",
    "@LV0@": "deadlock-risk",
    "@LV1@": "safe",
}
_PAT = _re.compile("@(?:T|J|LV)[0-9]+@|@FDSH@|@FDsh@|@FDdashc@|@TPATH@|@TMISS@|@TLINES@|@TLINE@|@TL1@|@TL2@|@GS1@|@GS2@|@GS3@|@GS4@|@TBIG@|@TPR@|@TBAD@")


def _c_escape(content):
    """Escape raw content for splicing inside a C string literal."""
    return content.replace(BS, BS + BS).replace(DQ, BS + DQ)


def _expand_tokens(s, outside_map):
    """Shared scanner: replaces @NL@/@CE@ and @T*/@J*/@LV* tokens. Inside C
    string/char literals @NL@/@CE@ become the backslash-n escape and content
    placeholders splice in escaped; outside, tokens map to the caller's
    replacement (real newline, or a full quoted C literal for placeholders)."""
    if not isinstance(s, str):
        return s
    out = []
    i = 0
    in_dq = in_sq = False
    while i < len(s):
        tok = s[i : i + 4]
        if tok in ("@NL@", "@CE@"):
            if in_dq or in_sq:
                out.append(CE)
            else:
                out.append(outside_map[tok])
            i += 4
            continue
        m = _PAT.match(s, i)
        if m:
            content = PLACEHOLDERS[m.group(0)]
            if in_dq or in_sq:
                out.append(_c_escape(content))
            else:
                out.append(DQ + content + DQ)
            i = m.end()
            continue
        c = s[i]
        if c == B and (in_dq or in_sq) and i + 1 < len(s):
            out.append(s[i : i + 2])
            i += 2
            continue
        if c == '"' and not in_sq:
            in_dq = not in_dq
        elif c == "'" and not in_dq:
            in_sq = not in_sq
        out.append(c)
        i += 1
    return "".join(out)


def esc_c(s):
    """C source conversion: statement separators become real newlines,
    escapes inside C string literals stay backslash-n."""
    return _expand_tokens(s, {"@NL@": NL, "@CE@": NL})


def esc_p(s):
    """Prose conversion: both tokens are markdown line breaks."""
    return _expand_tokens(s, {"@NL@": NL, "@CE@": NL}) if isinstance(s, str) else s


def esc_list_p(xs):
    return [esc_p(x) for x in xs]

# Standard C starter set for graded TUs.
C_PRELUDE = "#include <stdio.h>\n#include <stdbool.h>\n#include <string.h>\n#include <stdlib.h>\n"

# POSIX 2024 feature macro + the common system include set for systems modules.
# Probed: defining this in solution.c (before its includes) exposes POSIX
# symbols in the merged test TU even though the harness includes headers first.
POSIX_PRELUDE = (
    "#define _POSIX_C_SOURCE 200809L\n"
    "#include <stdio.h>\n"
    "#include <stdlib.h>\n"
    "#include <string.h>\n"
    "#include <unistd.h>\n"
    "#include <time.h>\n"
)

# pthreads + atomics prelude (musl: pthread lives in libc, no -pthread needed).
THREADS_PRELUDE = (
    "#define _POSIX_C_SOURCE 200809L\n"
    "#include <pthread.h>\n"
    "#include <stdatomic.h>\n"
    "#include <stdio.h>\n"
    "#include <stdlib.h>\n"
    "#include <string.h>\n"
    "#include <unistd.h>\n"
)


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def mod_dir(m):
    return os.path.join(BASE, "modules", m)


def _ensure_solutions_header():
    if not os.path.exists(SOLUTIONS):
        _w(
            SOLUTIONS,
            "/**\n"
            " * Reference (R) and intentionally-wrong (W) solutions for the\n"
            " * C Advanced two-sided harness (verify-challenges-ca.mjs).\n"
            " * Appended by the ca_*.py authoring scripts; parsed as a ledger.\n"
            " */\n"
            "const R = {};\n"
            "const W = {};\n",
        )
    with io.open(SOLUTIONS, "r", encoding="utf-8") as f:
        src = f.read()
    if "export { R, W };" not in src:
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("\nexport { R, W };\n")


def write_module(m, title, summary, vi_title, vi_summary, lessons, practices):
    title, summary, vi_title, vi_summary = esc_list_p([title, summary, vi_title, vi_summary])
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
    title, description, mdx = esc_list_p([title, description, mdx])
    vi_title, vi_description, vi_mdx = esc_list_p([vi_title, vi_description, vi_mdx])
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
    """C challenge. tests = [(name, code, hint), ...]. All strings @CE@-expanded."""
    title, prompt = esc_list_p([title, prompt])
    boilerplate = esc_c(boilerplate)
    tests = [(esc_p(n), esc_c(c), esc_p(h)) for (n, c, h) in tests]
    out = {
        "id": cid,
        "title": title,
        "prompt": prompt,
        "difficulty": difficulty,
        "language": "c",
        "boilerplate": boilerplate,
        "tests": [{"name": n, "code": c, "hint": h} for (n, c, h) in tests],
    }
    if level:
        out["level"] = level
    return out


def vi_challenge(vi_title, vi_prompt, vi_tests):
    vi_title, vi_prompt = esc_list_p([vi_title, vi_prompt])
    return {
        "title": vi_title,
        "prompt": vi_prompt,
        "tests": [{"name": esc_p(n), "hint": esc_p(h)} for (n, h) in vi_tests],
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
        _ensure_solutions_header()
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            for cid, ref, wrong in solutions:
                f.write("R[" + json.dumps(cid) + "] = " + json.dumps(esc_c(ref)) + ";\n")
                f.write("W[" + json.dumps(cid) + "] = " + json.dumps(esc_c(wrong)) + ";\n")
    print("practice set:", m + "/" + sid)


def write_checkpoint(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, ch, vi_ch, solution=None, wrong=None):
    """Checkpoint lesson with a lesson-attached challenge (+ solution pair)."""
    write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
    d = os.path.join(mod_dir(m), "lessons", lid, "challenges")
    _w(os.path.join(d, ch["id"] + ".json"), _j(ch))
    _w(os.path.join(d, ch["id"] + ".vi.json"), _j(vi_ch))
    if solution is not None and wrong is not None:
        _ensure_solutions_header()
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("R[" + json.dumps(ch["id"]) + "] = " + json.dumps(esc_c(solution)) + ";\n")
            f.write("W[" + json.dumps(ch["id"]) + "] = " + json.dumps(esc_c(wrong)) + ";\n")


def write_course(course_id, title, description, audience, outcomes, prerequisites, modules, vi_title, vi_description):
    _w(
        os.path.join(BASE, "course.json"),
        _j(
            {
                "id": course_id,
                "title": title,
                "description": description,
                "audience": audience,
                "outcomes": outcomes,
                "prerequisites": prerequisites,
                "modules": [{"reference": m} for m in modules],
            }
        ),
    )
    _w(os.path.join(BASE, "course.vi.json"), _j({"title": vi_title, "description": vi_description}))
    print("course manifest:", course_id, "modules:", len(modules))
