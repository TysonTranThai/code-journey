"""Fast two-sided harness for Python challenges (parallel per challenge).

Usage: python3 scripts/content-authoring/_harness_chunk.py [--ids id1,id2,...]
Runs on the host python3 with the same harness contract as the sandbox
(py-harness-snippet.py). Sandbox equivalence is proven by py-sandbox-smoke.
"""
import json
import glob
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/python")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/py-solutions.mjs")
HARNESS = os.path.join(ROOT, "scripts/content-authoring/py-harness-snippet.py")


def load_solutions():
    """Parse the R/W ledger (plain JS object literal, JSON via JS-safe transform).

    String values are captured with escape-aware patterns — ledger entries
    legitimately contain `\\"` sequences (e.g. SQL strings in solutions),
    which a naive `".*?"` truncates mid-value and breaks json.loads.
    """
    import re
    src = open(SOLUTIONS, encoding="utf-8").read()
    sols = {}
    pattern = re.compile(
        r"(R|W)\[((?:\"(?:[^\"\\]|\\.)*\")|(?:'(?:[^'\\]|\\.)*'))\]\s*=\s*"
        r"(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|\{.*?\}|\[.*?\]);",
        re.S,
    )
    for m in pattern.finditer(src):
        kind, key_raw, val_raw = m.group(1), m.group(2), m.group(3)
        key = json.loads(key_raw)
        val = json.loads(val_raw)
        sols[(kind, key)] = val
    return sols


def run_case(test_code, solution, harness_src):
    indented = "\n".join(("  " + ln if ln.strip() else ln) for ln in test_code.split("\n"))
    file = f"SOLUTION_SOURCE = {solution!r}\n{harness_src}\ntry:\n{indented}\n  print('PASS')\nexcept BaseException as _err:\n  print(_err, file=__import__('sys').stderr)\n  raise SystemExit(1)\n"
    fd, path = tempfile.mkstemp(suffix=".py")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(file)
    try:
        r = subprocess.run(["python3", path], capture_output=True, text=True, timeout=20)
        return r.returncode == 0, (r.stderr or "")[:200]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (possible infinite loop in solution)"
    finally:
        os.unlink(path)


def verify(task):
    cid, ch_path, ref, wrong, tests = task
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
    # Scope: the python-BEGINNER course only. python-intermediate is authored by
    # a separate agent with its own ledger (pi-solutions.mjs) — see PI1 scopes.
    for ch_path in glob.glob(os.path.join(TRACK, "courses/python-beginner/modules/*/practices/*/challenges/*.json")) + \
                   glob.glob(os.path.join(TRACK, "courses/python-beginner/modules/*/lessons/*/challenges/*.json")):
        if ch_path.endswith(".vi.json"):
            continue
        ch = json.load(open(ch_path, encoding="utf-8"))
        cid = ch["id"]
        if only and cid not in only:
            continue
        ref = sols.get(("R", cid))
        wrong = sols.get(("W", cid))
        tasks.append((cid, ch_path, ref, wrong, ch["tests"]))

    missing = [t[0] for t in tasks if t[2] is None or t[3] is None]
    tasks = [t for t in tasks if t[2] is not None and t[3] is not None]

    passed, failed = 0, []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for cid, ok, msg in ex.map(verify, tasks):
            if ok:
                passed += 1
            else:
                failed.append((cid, msg))

    print(f"{passed} challenges verified, {len(failed)} failed")
    for cid, msg in failed:
        print("  ✗", cid, "→", msg)
    for m in missing:
        print("  ✗", m, "→ missing solution entry")
    sys.exit(1 if (failed or missing) else 0)


if __name__ == "__main__":
    main()
