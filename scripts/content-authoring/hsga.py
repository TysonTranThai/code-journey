#!/usr/bin/env python3
"""
Authoring library for HSG Tin học — Advanced (hsg track, course 3).

Clones scripts/content-authoring/hsgi.py ( Intermediate) so shapes are
byte-compatible with the platform loaders. Writes to
src/content/tracks/hsg/courses/hsg-advanced; challenges are language:"cpp";
solution pairs append to scripts/content-authoring/hsg-advanced-solutions.mjs
(R[id] = reference source, W[id] = intentionally wrong source) for the
two-sided container harness verify-challenges-hsga.mjs — a SEPARATE ledger so
other courses' ledgers are never touched.

Same grading convention as Beginner/Intermediate: bits/stdc++ skeleton with a
`void solve(std::istream&, std::ostream&)` stub; contest_test() feeds stdin,
redirects cin/cout, and asserts output byte-exact (CHECK_LINES-style).
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/hsg")
BASE = os.path.join(TRACK, "courses/hsg-advanced")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/hsg-advanced-solutions.mjs")

CID_PREFIX = "hsga-"

BOILERPLATE = (
    "#include <bits/stdc++.h>\n"
    "using namespace std;\n"
    "\n"
    "void solve(istream& in, ostream& out) {\n"
    "    // Đọc dữ liệu từ `in` (dùng như cin), in kết quả ra `out` (dùng như cout).\n"
    "    // (Ghép bài thực tế: chương trình thi đọc từ bàn phím / tệp — ở đây\n"
    "    //  để chấm tự động, dữ liệu vào/ra đi qua hai luồng này.)\n"
    "}\n"
    "\n"
    "int main() {\n"
    "    ios_base::sync_with_stdio(false);\n"
    "    cin.tie(nullptr);\n"
    "    solve(cin, cout);\n"
    "    return 0;\n"
    "}\n"
)


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def _cid(cid):
    return cid if cid.startswith(CID_PREFIX) else CID_PREFIX + cid


def mod_dir(m):
    return os.path.join(BASE, "modules", m)


def _esc(s):
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )


def contest_test(name, inp, want, hint):
    code = (
        'std::istringstream in("' + _esc(inp) + '");\n'
        "std::ostringstream out;\n"
        "std::streambuf* cout_old = std::cout.rdbuf(out.rdbuf());\n"
        "solve(in, out);\n"
        "std::cout.rdbuf(cout_old);\n"
        'CHECK_EQ(out.str(), std::string("' + _esc(want) + '"));'
    )
    return (name, code, hint)


def challenge(cid, title, prompt, tests, level=None, difficulty="beginner", boilerplate=BOILERPLATE):
    out = {
        "id": _cid(cid),
        "title": title,
        "prompt": prompt,
        "difficulty": difficulty,
        "language": "cpp",
        "boilerplate": boilerplate,
        "tests": [{"name": n, "code": c, "hint": h} for (n, c, h) in tests],
    }
    if level:
        if level in {"imitation", "guided", "independent", "combination", "real-world", "debugging", "mini-build"}:
            out["level"] = level
        else:
            print("WARN: dropping invalid level %r for %s" % (level, cid))
    return out


def vi_challenge(vi_title, vi_prompt, vi_tests):
    return {
        "title": vi_title,
        "prompt": vi_prompt,
        "tests": [{"name": n, "hint": h} for (n, h) in vi_tests],
    }


def _ensure_solutions_header():
    if not os.path.exists(SOLUTIONS):
        _w(
            SOLUTIONS,
            "/**\n"
            " * Reference (R) and intentionally-wrong (W) solutions for the\n"
            " * HSG Advanced two-sided harness (verify-challenges-hsga.mjs).\n"
            " * Appended by the hsga_*.py authoring scripts; parsed as a ledger.\n"
            " */\n"
            "const R = {};\n"
            "const W = {};\n",
        )
    with io.open(SOLUTIONS, "r", encoding="utf-8") as f:
        src = f.read()
    if "export { R, W };" not in src:
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("\nexport { R, W };\n")


def append_solutions(pairs):
    _ensure_solutions_header()
    with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
        for cid, ref, wrong in pairs:
            f.write("R[" + json.dumps(_cid(cid)) + "] = " + json.dumps(ref) + ";\n")
            f.write("W[" + json.dumps(_cid(cid)) + "] = " + json.dumps(wrong) + ";\n")


def write_module(m, title, summary, vi_title, vi_summary, lessons, practices):
    _w(
        os.path.join(mod_dir(m), "module.json"),
        _j(
            {
                "id": m,
                "title": title,
                "summary": summary,
                "lessons": [{"reference": _cid(l)} for l in lessons],
                "practices": [{"reference": _cid(p)} for p in practices],
            }
        ),
    )
    _w(
        os.path.join(mod_dir(m), "module.vi.json"),
        _j({"title": vi_title, "summary": vi_summary}),
    )
    print("module:", m)


def write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="beginner"):
    if difficulty not in ("beginner", "intermediate", "advanced"):
        difficulty = "beginner"
    lid = _cid(lid)
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


def write_practice(m, sid, title, description, vi_title, vi_description, after_lesson, minutes, difficulty, challenges, vi_challenges, solutions=None):
    sid = _cid(sid)
    d = os.path.join(mod_dir(m), "practices")
    _w(
        os.path.join(d, sid + ".json"),
        _j(
            {
                "id": sid,
                "title": title,
                "description": description,
                "afterLesson": _cid(after_lesson),
                "minutes": minutes,
                "difficulty": difficulty,
                "challenges": [c["id"] for c in challenges],
            }
        ),
    )
    _w(os.path.join(d, sid + ".vi.json"), _j({"title": vi_title, "description": vi_description}))
    for c in challenges:
        _w(os.path.join(d, sid, "challenges", c["id"] + ".json"), _j(c))
    vi_map = vi_challenges if isinstance(vi_challenges, dict) else {
        (c["id"] if c["id"].startswith(CID_PREFIX) else CID_PREFIX + c["id"]): vc
        for c, vc in zip(challenges, vi_challenges)
    }
    for cid, vc in vi_map.items():
        _w(os.path.join(d, sid, "challenges", _cid(cid) + ".vi.json"), _j(vc))
    if solutions:
        append_solutions(solutions)
    print("practice set:", m + "/" + sid)


def write_checkpoint(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, ch, vi_ch, solution=None, wrong=None):
    """Checkpoint lesson with a lesson-attached challenge (+ solution pair).

    NOTE: the checkpoint lesson id must be listed in write_module's lessons;
    the lesson-attached challenge id must DIFFER from the lesson id.
    """
    write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
    d = os.path.join(mod_dir(m), "lessons", _cid(lid), "challenges")
    _w(os.path.join(d, ch["id"] + ".json"), _j(ch))
    _w(os.path.join(d, ch["id"] + ".vi.json"), _j(vi_ch))
    if solution is not None and wrong is not None:
        append_solutions([(ch["id"], solution, wrong)])


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


def write_track():
    _w(
        os.path.join(TRACK, "track.json"),
        _j(
            {
                "id": "hsg",
                "title": "Competitive Programming",
                "description": "Tuyển Học Sinh Giỏi Tin học — the Vietnamese high-school competitive-programming path. Learn to read a contest problem, choose an algorithm that fits the constraints, implement it fast in C++, and defend it against edge cases — from school selection rounds toward provincial HSG and beyond.",
                "courses": [{"reference": "hsg-beginner"}, {"reference": "hsg-intermediate"}, {"reference": "hsg-advanced"}],
            }
        ),
    )
    _w(
        os.path.join(TRACK, "track.vi.json"),
        _j(
            {
                "title": "Lập trình thi đấu",
                "description": "Tuyển Học Sinh Giỏi Tin học — lộ trình lập trình thi đấu cho học sinh THPT Việt Nam. Học cách đọc đề, chọn thuật toán phù hợp với giới hạn, cài đặt nhanh bằng C++ và phòng thủ trước test biên — từ vòng chọn đội trường tới HSG cấp tỉnh và cấp quốc gia.",
            }
        ),
    )
    print("track manifest: hsg (3 courses)")
