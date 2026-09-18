#!/usr/bin/env python3
"""Regenerate cppi_m4.py from the emitted (harness-green) module content.

The original authoring source was corrupted by a bad escaping fix; the on-disk
JSONs/MDX are the verified truth (26/26 two-sided). This walks
modules/operators-copy-move and rebuilds a faithful, idempotent authoring
script: lessons/checkpoints from lessons/*.json + .mdx, practices from
practices/*, solution pairs from the ledger (last-write-wins, matching mjs
execution order).
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MOD_DIR = os.path.join(ROOT, "src/content/tracks/cpp/courses/cpp-intermediate/modules/operators-copy-move")
LEDGER = os.path.join(ROOT, "scripts/content-authoring/cpp-intermediate-solutions.mjs")
OUT = os.path.join(ROOT, "scripts/content-authoring/cppi_m4.py")


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


def ledger_rw():
    r, w = {}, {}
    for ln in io.open(LEDGER, encoding="utf-8"):
        m = re.match(r'^(R|W)\["((?:[^"\\]|\\.)*)"\] = (".*");\s*$', ln)
        if not m:
            continue
        key, cid, val = m.group(1), m.group(2), json.loads(m.group(3))
        (r if key == "R" else w)[cid] = val
    return r, w


def tqs(s, varname):
    """Embed s as a raw triple-quoted literal; fall back to repr."""
    if '"""' not in s and not s.endswith("\\") and '\\\n' not in s:
        return 'r"""' + s + '"""'
    print(f"  (repr fallback for {varname})")
    return repr(s)


def embed_str(s):
    return repr(s)


def py_test_tuples(tests):
    parts = []
    for t in tests:
        parts.append(
            "        (%s, %s, %s),"
            % (embed_str(t["name"]), embed_str(t["code"]), embed_str(t.get("hint", "")))
        )
    return "\n".join(parts)


R, W = ledger_rw()


def vid(s: str) -> str:
    """Sanitize an id into a Python identifier fragment."""
    return s.replace("-", "_")


lines = []
A = lines.append
A('#!/usr/bin/env python3')
A('"""C++ Intermediate — Module 4: operators-copy-move.')
A('')
A('REGENERATED from the emitted, harness-verified content (26/26 two-sided) after')
A('the original source was corrupted by an escaping fix. Emitting this script is')
A('idempotent: it reproduces the exact on-disk JSONs/MDX and appends the same')
A('solution pairs to the ledger (duplicate keys are harmless — last write wins).')
A('"""')
A("import sys, os")
A("sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))")
A("from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint")
A("")
A('MOD = "operators-copy-move"')
A("")

module = load(os.path.join(MOD_DIR, "module.json"))
module_vi = load(os.path.join(MOD_DIR, "module.vi.json"))
lesson_order = [l["reference"] for l in module["lessons"]]
practice_order = [p["reference"] for p in module["practices"]]

lesson_vars = {}      # lid -> (EN, VI) var names
practice_blocks = []  # (sid, en_list_var, vi_map_var, solutions)

# ---- lessons + checkpoints -------------------------------------------------
for lid in lesson_order:
    lp = os.path.join(MOD_DIR, "lessons", lid + ".json")
    l = load(lp)
    lv = load(os.path.join(MOD_DIR, "lessons", lid + ".vi.json"))
    en = io.open(os.path.join(MOD_DIR, "lessons", lid + ".mdx"), encoding="utf-8").read()
    vi = io.open(os.path.join(MOD_DIR, "lessons", lid + ".vi.mdx"), encoding="utf-8").read()

    base = vid(lid)
    en_v, vi_v = f"L_{base}_EN", f"L_{base}_VI"
    lesson_vars[lid] = (en_v, vi_v)

    A(f"# ---- lesson {lid} " + "-" * (60 - len(lid)))
    A(f"{en_v} = " + tqs(en, en_v))
    A("")
    A(f"{vi_v} = " + tqs(vi, vi_v))
    A("")

    ch_dir = os.path.join(MOD_DIR, "lessons", lid, "challenges")
    if os.path.isdir(ch_dir):
        # checkpoint: one lesson-attached challenge
        files = sorted(f for f in os.listdir(ch_dir) if f.endswith(".json") and not f.endswith(".vi.json"))
        assert len(files) == 1, (lid, files)
        c = load(os.path.join(ch_dir, files[0]))
        cv = load(os.path.join(ch_dir, files[0].replace(".json", ".vi.json")))
        ch_var, vi_var = f"CP_CH_{base}", f"VI_CP_{base}"
        A(f"{ch_var} = challenge(")
        A(f"    {embed_str(c['id'])},")
        A(f"    {embed_str(c['title'])},")
        A(f"    {embed_str(c['prompt'])},")
        A(f"    {embed_str(c['boilerplate'])},")
        A("    [")
        A(py_test_tuples(c["tests"]))
        A("    ],")
        if "level" in c:
            A(f"    level={embed_str(c['level'])},")
        A(f"    difficulty={embed_str(c.get('difficulty', 'intermediate'))},")
        A(")")
        A("")
        A(f"{vi_var} = vi_challenge(")
        A(f"    {embed_str(cv['title'])},")
        A(f"    {embed_str(cv['prompt'])},")
        A("    [")
        for t in cv["tests"]:
            A(f"        ({embed_str(t['name'])}, {embed_str(t.get('hint', ''))}),")
        A("    ],")
        A(")")
        A("")
        print(f"checkpoint lesson: {lid} ({c['id']})")
    else:
        print(f"lesson: {lid}")

# ---- practices -------------------------------------------------------------
for sid in practice_order:
    p = load(os.path.join(MOD_DIR, "practices", sid + ".json"))
    pv = load(os.path.join(MOD_DIR, "practices", sid + ".vi.json"))
    ch_dir = os.path.join(MOD_DIR, "practices", sid, "challenges")
    files = sorted(f for f in os.listdir(ch_dir) if f.endswith(".json") and not f.endswith(".vi.json"))

    pvar, vvar = f"P_{vid(sid)}", f"VI_P_{vid(sid)}"
    A(f"# ---- practice {sid} " + "-" * (60 - len(sid)))
    A(f"{pvar} = [")
    for f in files:
        c = load(os.path.join(ch_dir, f))
        A("    challenge(")
        A(f"        {embed_str(c['id'])},")
        A(f"        {embed_str(c['title'])},")
        A(f"        {embed_str(c['prompt'])},")
        A(f"        {embed_str(c['boilerplate'])},")
        A("        [")
        A(py_test_tuples(c["tests"]))
        A("        ],")
        if "level" in c:
            A(f"        level={embed_str(c['level'])},")
        A(f"        difficulty={embed_str(c.get('difficulty', 'intermediate'))},")
        A("    ),")
    A("]")
    A("")
    A(f"{vvar} = {{")
    for f in files:
        c = load(os.path.join(ch_dir, f))
        cv = load(os.path.join(ch_dir, f.replace(".json", ".vi.json")))
        A(f"    {embed_str(c['id'])}: vi_challenge(")
        A(f"        {embed_str(cv['title'])},")
        A(f"        {embed_str(cv['prompt'])},")
        A("        [")
        for t in cv["tests"]:
            A(f"            ({embed_str(t['name'])}, {embed_str(t.get('hint', ''))}),")
        A("        ],")
        A("    ),")
    A("}")
    A("")
    sols = []
    for f in files:
        cid = f[:-5]
        assert cid in R and cid in W, (sid, cid, "missing ledger pair")
        sols.append((cid, R[cid], W[cid]))
    practice_blocks.append((sid, pvar, vvar, sols, p, pv))
    print(f"practice: {sid} ({len(files)} challenges)")

# solution-pair locals for checkpoint (must precede the emit calls)
for lid in lesson_order:
    ch_dir = os.path.join(MOD_DIR, "lessons", lid, "challenges")
    if os.path.isdir(ch_dir):
        files = sorted(f for f in os.listdir(ch_dir) if f.endswith(".json") and not f.endswith(".vi.json"))
        c = load(os.path.join(ch_dir, files[0]))
        base = vid(lid)
        A(f"R_{base} = {embed_str(R[c['id']])}")
        A(f"W_{base} = {embed_str(W[c['id']])}")

# ---- emit calls ------------------------------------------------------------
A("")
A("# ---- emit ------------------------------------------------------------------")
for lid in lesson_order:
    lp = load(os.path.join(MOD_DIR, "lessons", lid + ".json"))
    lv = load(os.path.join(MOD_DIR, "lessons", lid + ".vi.json"))
    en_v, vi_v = lesson_vars[lid]
    ch_dir = os.path.join(MOD_DIR, "lessons", lid, "challenges")
    if os.path.isdir(ch_dir):
        files = sorted(f for f in os.listdir(ch_dir) if f.endswith(".json") and not f.endswith(".vi.json"))
        c = load(os.path.join(ch_dir, files[0]))
        base = vid(lid)
        A("write_checkpoint(")
        A(f"    MOD, {embed_str(lid)},")
        A(f"    {embed_str(lp['title'])}, {embed_str(lp['description'])}, {lp['minutes']},")
        A(f"    {en_v},")
        A(f"    {embed_str(lv['title'])}, {embed_str(lv['description'])},")
        A(f"    {vi_v},")
        A(f"    CP_CH_{base}, VI_CP_{base},")
        A(f"    solution=R_{base}, wrong=W_{base},")
        A(")")
    else:
        A("write_lesson(")
        A(f"    MOD, {embed_str(lid)},")
        A(f"    {embed_str(lp['title'])}, {embed_str(lp['description'])}, {lp['minutes']},")
        A(f"    {en_v},")
        A(f"    {embed_str(lv['title'])}, {embed_str(lv['description'])},")
        A(f"    {vi_v},")
        A(f"    difficulty={embed_str(lp.get('difficulty', 'intermediate'))},")
        A(")")

for sid, pvar, vvar, sols, p, pv in practice_blocks:
    A("write_practice(")
    A(f"    MOD, {embed_str(sid)},")
    A(f"    {embed_str(p['title'])},")
    A(f"    {embed_str(p['description'])},")
    A(f"    {embed_str(pv['title'])},")
    A(f"    {embed_str(pv['description'])},")
    A(f"    {embed_str(p['afterLesson'])}, {p['minutes']}, {embed_str(p['difficulty'])},")
    A(f"    {pvar}, {vvar},")
    A("    solutions=[")
    for cid, ref, wrong in sols:
        A(f"        ({embed_str(cid)}, {embed_str(ref)}, {embed_str(wrong)}),")
    A("    ],")
    A(")")

A("")
A("write_module(")
A(f'    MOD, {embed_str(module["title"])},')
A(f'    {embed_str(module["summary"])},')
A(f'    {embed_str(module_vi["title"])},')
A(f'    {embed_str(module_vi["summary"])},')
A(f"    {embed_str(lesson_order)},")
A(f"    {embed_str(practice_order)},")
A(")")
A('print("module 4 emitted (regenerated source)")')

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print(f"\nwrote {OUT} ({len(lines)} lines)")
