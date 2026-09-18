#!/usr/bin/env python3
"""Round-2 QA repairs for Python Intermediate challenges.

1. Harness: prepend challenge boilerplate before the solution — mirrors
   production (the editor seeds boilerplate; the learner's full editor
   content is what gets graded). Fixes pi5-exc-order without touching tests.
2. pi11-sec-deser R: docstring mentioned 'pickle' (its own test forbids the
   word) — reword.
3. Wrong-solution swaps where the previous W was accidentally equivalent:
   - pi7-mock-clock: W now tests only one band (incomplete coverage — the
     exact bug this lesson teaches).
   (pi3-ctx-tracker/pi3-gen-parse/pi1/pi6 overrides from round 1 stay; the
   discriminating probes below are what make them fail.)
4. Discriminating probes folded into existing tests (test counts unchanged,
   so VI overlays need no edits):
   - pi2-cls-counter: instance state, not a class attribute
   - pi1-sort-records: tie pair whose name order differs from input order
   - pi6-path-organize: case-insensitive keys + sorted names
   - pi3-ctx-tracker: __exit__ must not swallow the exception
   - pi3-gen-parse: laziness probe (endless input must not hang)
"""
import glob
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/python/courses/python-intermediate")
LEDGER = os.path.join(ROOT, "scripts/content-authoring/pi-solutions.mjs")
HARNESS = os.path.join(ROOT, "scripts/content-authoring/_pi_harness_chunk.py")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def edit(cid, fn):
    for p in glob.glob(
        os.path.join(COURSE, "modules/*/practices/*/challenges", cid + ".json")
    ) + glob.glob(
        os.path.join(COURSE, "modules/*/lessons/*/challenges", cid + ".json")
    ):
        if p.endswith(".vi.json"):
            continue
        ch = load(p)
        fn(ch)
        save(p, ch)
        print("patched", cid)
        return
    raise SystemExit("missing " + cid)


# ---- 1. harness mirrors production: boilerplate + solution ------------------
def patch_harness():
    src = io.open(HARNESS, encoding="utf-8").read()
    if "BOILERPLATE" in src:
        print("harness already patched")
        return
    src = src.replace(
        '        tasks.append((cid, ref, wrong, ch["tests"]))',
        '        tasks.append((cid, ref, wrong, ch["tests"], ch.get("boilerplate", "")))',
    )
    src = src.replace(
        "    missing = [t[0] for t in tasks if t[1] is None or t[2] is None]\n"
        "    tasks = [t for t in tasks if t[1] is not None and t[2] is not None]",
        "    missing = [t[0] for t in tasks if t[1] is None or t[2] is None]\n"
        "    tasks = [t for t in tasks if t[1] is not None and t[2] is not None]\n"
        "    # Production contract: the editor seeds boilerplate and the learner's\n"
        "    # full editor content is graded, so the graded unit is boiler+solution.\n"
        "    tasks = [(cid, bo + \"\\n\\n\" + ref, bo + \"\\n\\n\" + wrong, tests)\n"
        "             for (cid, ref, wrong, tests, bo) in tasks]",
    )
    src = src.replace(
        "def verify(task):\n    cid, ref, wrong, tests = task",
        "def verify(task):\n    cid, ref, wrong, tests = task",
    )
    io.open(HARNESS, "w", encoding="utf-8").write(src)
    print("harness: boilerplate prepending enabled")


# ---- 2. sec-deser reference must not contain the word pickle ----------------
def patch_deser_r():
    src = io.open(LEDGER, encoding="utf-8").read()
    old = (
        'R["pi11-sec-deser"] = "import json\\n\\ndef load_payload(data):\\n'
        '    \\"\\"\\"Decode UNTRUSTED payloads. JSON only — pickle never (code exec risk).'
        '\\"\\"\\"\\n'
    )
    # Robust: find the R line and reword its docstring via json round-trip.
    m = re.search(r'R\["pi11-sec-deser"\] = ("(?:[^"\\]|\\.)*");', src, re.S)
    assert m, "sec-deser R not found"
    val = json.loads(m.group(1))
    val = val.replace(
        '"""Decode UNTRUSTED payloads. JSON only — pickle never (code exec risk)."""',
        '"""Decode untrusted payloads as JSON data only."""',
    )
    assert "pickle" not in val
    src = (
        src[: m.start()]
        + 'R["pi11-sec-deser"] = ' + json.dumps(val) + ";"
        + src[m.end():]
    )
    io.open(LEDGER, "w", encoding="utf-8").write(src)
    print("sec-deser R reworded")


# ---- 3. mock-clock wrong solution: one-band suite ---------------------------
MOCK_CLOCK_W = (
    "import unittest\n"
    "from datetime import datetime\n"
    "\n"
    "def greeting(name, now=None):\n"
    "    hour = now.hour if now is not None else datetime.now().hour\n"
    "    if hour < 12:\n"
    "        part = 'Good morning'\n"
    "    elif hour < 18:\n"
    "        part = 'Good afternoon'\n"
    "    else:\n"
    "        part = 'Good evening'\n"
    "    return f'{part}, {name}!'\n"
    "\n"
    "class TestGreeting(unittest.TestCase):\n"
    "    def test_morning(self):\n"
    "        self.assertEqual(greeting('An', datetime(2026, 1, 1, 8)), 'Good morning, An!')\n"
    "\n"
    "SUITE_TEST = TestGreeting\n"
)


def append_ledger(pairs):
    marker = "/* --- QA repair round 2 (last key wins) --- */"
    src = io.open(LEDGER, encoding="utf-8").read()
    if marker in src:
        print("ledger overrides already present, skipping")
        return
    with io.open(LEDGER, "a", encoding="utf-8") as f:
        f.write("\n" + marker + "\n")
        for cid, kind, val in pairs:
            f.write(kind + "[" + json.dumps(cid) + "] = " + json.dumps(val) + ";\n")
    print("ledger overrides:", len(pairs))


# ---- 4. discriminating probes ----------------------------------------------
def fix_counter(ch):
    for t in ch["tests"]:
        if t["name"] == "independent counters":
            t["code"] = (
                "a, b = Counter(), Counter()\n"
                "a.tick(); a.tick()\n"
                "assert b.tick() == 1\n"
                "assert 'count' not in Counter.__dict__, "
                "'count must be instance state set in __init__, not a class attribute'\n"
            )


def fix_sort_records(ch):
    for t in ch["tests"]:
        if t["name"] == "input order preserved on ties (stable)":
            t["code"] = (
                "ps = [{\"name\": \"Z\", \"price\": 5}, {\"name\": \"A\", \"price\": 5}]\n"
                "assert [p[\"name\"] for p in cheapest_first(ps)] == [\"Z\", \"A\"], "
                "'stable sort must keep input order for equal prices (not re-tie by name)'\n"
            )


def fix_path_organize(ch):
    for t in ch["tests"]:
        if t["name"] == "groups by suffix":
            t["code"] = (
                "ps = [Path('a.txt'), Path('b.py'), Path('c.txt')]\n"
                "assert by_suffix(ps) == {'.py': ['b.py'], '.txt': ['a.txt', 'c.txt']}\n"
                "ps2 = [Path('b.txt'), Path('D.TXT')]\n"
                "assert by_suffix(ps2)['.txt'] == ['D.TXT', 'b.txt'], "
                "'suffix keys are lowercase and names come out sorted'\n"
            )


def fix_ctx_tracker(ch):
    for t in ch["tests"]:
        if t["name"] == "cleanup on exception":
            t["code"] = (
                "global EVENTS\n"
                "EVENTS.clear()\n"
                "raised = False\n"
                "try:\n"
                "    with Session():\n"
                "        raise RuntimeError('boom')\n"
                "except RuntimeError:\n"
                "    raised = True\n"
                "assert raised, '__exit__ must not swallow the exception (return falsy)'\n"
                "assert EVENTS == ['open', 'closed']\n"
            )


def fix_gen_parse(ch):
    for t in ch["tests"]:
        if t["name"] == "skips bad lines":
            t["code"] = (
                "assert list(parse_scores(['10', ' oops ', '42'])) == [10, 42]\n"
                "def endless():\n"
                "    i = 0\n"
                "    while True:\n"
                "        yield str(i)\n"
                "        i += 1\n"
                "gen = parse_scores(endless())\n"
                "assert next(gen) == 0, 'must be lazy: return a generator, yield the first valid score without consuming everything'\n"
            )


def fix_mock_clock(ch):
    for t in ch["tests"]:
        if t["name"] == "all three bands tested":
            # Behavioral probe: spy on greeting inside the suite's own globals,
            # run the suite, and require all three bands to be exercised.
            # (Static source probes are defeated by the boilerplate, which
            # contains the class skeleton and the band strings.)
            t["code"] = (
                "import unittest, io\n"
                "seen = []\n"
                "real = SUITE_TEST.test_morning.__globals__['greeting']\n"
                "def spy(name, now=None):\n"
                "    if now is not None:\n"
                "        seen.append(now.hour)\n"
                "    return real(name, now)\n"
                "SUITE_TEST.test_morning.__globals__['greeting'] = spy\n"
                "result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)"
                ".run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\n"
                "assert result.wasSuccessful(), 'greeting tests failed'\n"
                "bands = {'morning' if h < 12 else 'afternoon' if h < 18 else 'evening' for h in seen}\n"
                "assert {'morning', 'afternoon', 'evening'} <= bands, "
                "'test all three bands with injected times'\n"
            )


if __name__ == "__main__":
    patch_harness()
    patch_deser_r()
    edit("pi2-cls-counter", fix_counter)
    edit("pi1-sort-records", fix_sort_records)
    edit("pi6-path-organize", fix_path_organize)
    edit("pi3-ctx-tracker", fix_ctx_tracker)
    edit("pi3-gen-parse", fix_gen_parse)
    edit("pi7-mock-clock", fix_mock_clock)
    append_ledger([("pi7-mock-clock", "W", MOCK_CLOCK_W)])
    print("round 2 complete")
