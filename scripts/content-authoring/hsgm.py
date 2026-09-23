#!/usr/bin/env python3
"""
Authoring library for HSG Tin học — Mastery (hsg track, course 5).

Clones scripts/content-authoring/hsgx.py (Intensive) so shapes are
byte-compatible with the platform loaders. Writes to
src/content/tracks/hsg/courses/hsg-mastery; challenges are language:"cpp";
solution pairs append to scripts/content-authoring/hsg-mastery-solutions.mjs
(R[id] = reference source, W[id] = intentionally wrong source) for the
two-sided container harness verify-challenges-hsgm.mjs — a SEPARATE ledger so
other courses' ledgers are never touched.

Grading convention (same as Beginner/Intermediate/Advanced): bits/stdc++
skeleton with a `void solve(std::istream&, std::ostream&)` stub;
contest_test() feeds stdin, redirects cin/cout, asserts byte-exact output.

Mastery discipline (do not regress):
 - Topic names NEVER appear in problem statements; recognition is the task.
 - Constraints are stated exactly; every R must satisfy them; every W must
   be a behavioral near-miss (correct-looking, plausible, wrong) — compile
   errors are not wrong solutions.
 - All big-test ground truths are Python-verified before emit.
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/hsg")
BASE = os.path.join(TRACK, "courses/hsg-mastery")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/hsg-mastery-solutions.mjs")

CID_PREFIX = "hsgm-"

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


def challenge(cid, title, prompt, tests, level=None, difficulty="advanced", boilerplate=BOILERPLATE):
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


def recognition_drill(cid, title, scenario, options, answer, hint, level="independent", vi_title=None, vi_scenario=None, vi_options=None, vi_hint=None):
    """A recognition drill: scenario + lettered options; the program outputs the letter.

    scenario/options: EN text (options is a list of 4 strings). answer: "A"/"B"/"C"/"D".
    VI side must be provided via vi_* params (enforced by caller discipline).
    """
    letters = ["A", "B", "C", "D"]
    body = "\n\n".join("**" + l + ")** " + o for l, o in zip(letters, options))
    prompt = (
        "**Scenario.** " + scenario + "\n\n"
        "**Which approach is the best fit? The program only needs to print the letter.**\n\n"
        + body
    )
    tests = [contest_test("answer", "", answer, hint)]
    ch = challenge(cid, title, prompt, tests, level=level, difficulty="advanced")
    vi_prompt = (
        "**Tình huống.** " + (vi_scenario or scenario) + "\n\n"
        "**Thuật toán nào phù hợp nhất? Chương trình chỉ cần in ra chữ cái.**\n\n"
        + "\n\n".join("**" + l + ")** " + o for l, o in zip(letters, vi_options or options))
    )
    vi = vi_challenge(vi_title or title, vi_prompt, [("đáp án", vi_hint or hint)])
    return ch, vi


def _ensure_solutions_header():
    if not os.path.exists(SOLUTIONS):
        _w(
            SOLUTIONS,
            "/**\n"
            " * Reference (R) and intentionally-wrong (W) solutions for the\n"
            " * HSG Mastery two-sided harness (verify-challenges-hsgm.mjs).\n"
            " * Appended by the hsgm_*.py authoring scripts; parsed as a ledger.\n"
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
    assert len(summary) <= 400, (m, len(summary))
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
    assert len(vi_summary) <= 400, (m + " vi", len(vi_summary))
    _w(
        os.path.join(mod_dir(m), "module.vi.json"),
        _j({"title": vi_title, "summary": vi_summary}),
    )
    print("module:", m)


def write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="advanced"):
    if difficulty not in ("beginner", "intermediate", "advanced"):
        difficulty = "advanced"
    lid = _cid(lid)
    assert len(description) <= 400, (lid, len(description))
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
    assert len(vi_description) <= 400, (lid + " vi", len(vi_description))
    _w(os.path.join(d, lid + ".vi.json"), _j({"title": vi_title, "description": vi_description}))
    _w(os.path.join(d, lid + ".mdx"), mdx.strip() + "\n")
    _w(os.path.join(d, lid + ".vi.mdx"), vi_mdx.strip() + "\n")
    print("lesson:", m + "/" + lid)


def write_practice(m, sid, title, description, vi_title, vi_description, after_lesson, minutes, difficulty, challenges, vi_challenges, solutions=None):
    assert len(description) <= 400, (sid, len(description))
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
    assert len(vi_description) <= 400, (sid + " vi", len(vi_description))
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
    print("checkpoint:", m + "/" + _cid(lid))
