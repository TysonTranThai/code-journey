#!/usr/bin/env python3
"""Fast two-sided harness for PYTHON-ADVANCED challenges (parallel per challenge).

Usage: python3 scripts/content-authoring/_harness_pa.py [--ids id1,id2,...]
Scoped strictly to courses/python-advanced — python-beginner (its own ledger)
and python-intermediate (separate agent, pi-solutions.mjs) are NOT touched.

Runs on python3.11 when available (graded code targets 3.11; the sandbox's
python 3.12 is a superset). Falls back to `python3` otherwise.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/python")
COURSE = os.path.join(TRACK, "courses/python-advanced")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/py-solutions.mjs")
HARNESS = os.path.join(ROOT, "scripts/content-authoring/py-harness-snippet.py")

PYTHON = "python3.11" if shutil.which("python3.11") else "python3"


def load_solutions():
    """Parse the R/W ledger (one complete JSON string per physical line).

    Line-based on purpose: a lazy multi-line regex truncates at escaped
    quotes inside solution values and corrupts the parse.
    """
    sols = {}
    for line in open(SOLUTIONS, encoding="utf-8"):
        line = line.strip()
        if not line.startswith(("R[", "W[")):
            continue
        kind = line[0]
        rest = line[2:]
        close = rest.index("]")
        key = json.loads(rest[:close])
        val_raw = rest[close + 1:].strip()
        assert val_raw.startswith("= ") and val_raw.endswith(";"), line[:60]
        val = json.loads(val_raw[2:-1])
        sols[(kind, key)] = val
    return sols


def run_case(test_code, solution, harness_src):
    indented = "\n".join(("  " + ln if ln.strip() else ln) for ln in test_code.split("\n"))
    file = f"SOLUTION_SOURCE = {solution!r}\n{harness_src}\ntry:\n{indented}\n  print('PASS')\nexcept BaseException as _err:\n  print(_err, file=__import__('sys').stderr)\n  raise SystemExit(1)\n"
    fd, path = tempfile.mkstemp(suffix=".py")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(file)
    try:
        r = subprocess.run([PYTHON, path], capture_output=True, text=True, timeout=20)
        return r.returncode == 0, (r.stderr or "")[:200]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (possible infinite loop in solution)"
    finally:
        os.unlink(path)


def verify(task):
    cid, ref, wrong, tests = task
    harness_src = open(HARNESS, encoding="utf-8").read()
    for t in tests:
        ok, err = run_case(t["code"], ref, harness_src)
        if not ok:
            return cid, False, f"REF FAILED at {t['name']}: {err}"
    wrong_fails = False
    for t in tests:
        ok, err = run_case(t["code"], wrong, harness_src)
        if not ok:
            wrong_fails = True
            break
    if not wrong_fails:
        return cid, False, "WRONG PASSED — grading not strict enough"
    return cid, True, "OK"


def main():
    sols = load_solutions()
    only = None
    if "--ids" in sys.argv:
        only = set(sys.argv[sys.argv.index("--ids") + 1].split(","))

    tasks = []
    for ch_path in glob.glob(os.path.join(COURSE, "modules/*/practices/*/challenges/*.json")) + \
                   glob.glob(os.path.join(COURSE, "modules/*/lessons/*/challenges/*.json")):
        if ch_path.endswith(".vi.json"):
            continue
        ch = json.load(open(ch_path, encoding="utf-8"))
        cid = ch["id"]
        if only and cid not in only:
            continue
        ref = sols.get(("R", cid))
        wrong = sols.get(("W", cid))
        tasks.append((cid, ref, wrong, ch["tests"]))

    missing = [t[0] for t in tasks if t[1] is None or t[2] is None]
    tasks = [t for t in tasks if t[1] is not None and t[2] is not None]

    passed, failed = 0, []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for cid, ok, msg in ex.map(verify, tasks):
            if ok:
                passed += 1
            else:
                failed.append((cid, msg))

    print(f"[{PYTHON}] {passed} challenges verified, {len(failed)} failed")
    for cid, msg in failed:
        print("  x", cid, "->", msg)
    for m in missing:
        print("  x", m, "-> missing solution entry")
    sys.exit(1 if (failed or missing) else 0)


if __name__ == "__main__":
    main()
