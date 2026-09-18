"""Fast two-sided harness for Python — INTERMEDIATE challenges (parallel).

Usage: python3 scripts/content-authoring/_pi_harness_chunk.py [--ids id1,id2,...]
Runs on the host python3 with the same harness contract as the sandbox
(py-harness-snippet.py). Scope: python-intermediate course only; solutions
come from pi-solutions.mjs (the Beginner ledger is separate by design).
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/python/courses/python-intermediate")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/pi-solutions.mjs")
HARNESS = os.path.join(ROOT, "scripts/content-authoring/py-harness-snippet.py")

# Prefer the newest local python3 (course targets 3.12+: tomllib, dataclasses,
# unittest.mock). Mirrors the sandbox runtime (python 3.12.14).
def _pick_python():
    candidates = ["/opt/homebrew/bin/python3", "/usr/local/bin/python3", "python3"]
    for cand in candidates:
        try:
            r = subprocess.run(
                [cand, "-c", "import sys; assert sys.version_info >= (3, 12)"],
                capture_output=True,
            )
            if r.returncode == 0:
                return cand
        except OSError:
            continue
    return "python3"


PYTHON = _pick_python()


def load_solutions():
    """Parse the R/W ledger (plain JS object literal) into a dict."""
    src = open(SOLUTIONS, encoding="utf-8").read()
    sols = {}
    for m in re.finditer(
        r'(R|W)\[((?:"[^"]+")|(?:\'[^\']+\'))\]\s*=\s*("(?:[^"\\]|\\.)*");',
        src,
        re.S,
    ):
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
        r = subprocess.run([PYTHON, path], capture_output=True, text=True, timeout=20)
        return r.returncode == 0, (r.stderr or "")[:300]
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
    for t in tests:
        ok, err = run_case(t["code"], wrong, harness_src)
        if not ok:
            return cid, True, "OK"
    return cid, False, "WRONG PASSED — grading not strict enough"


def main():
    sols = load_solutions()
    only = None
    if "--ids" in sys.argv:
        only = set(sys.argv[sys.argv.index("--ids") + 1].split(","))

    tasks = []
    for ch_path in glob.glob(
        os.path.join(COURSE, "modules/*/practices/*/challenges/*.json")
    ) + glob.glob(os.path.join(COURSE, "modules/*/lessons/*/challenges/*.json")):
        if ch_path.endswith(".vi.json"):
            continue
        ch = json.load(open(ch_path, encoding="utf-8"))
        cid = ch["id"]
        if only and cid not in only:
            continue
        ref = sols.get(("R", cid))
        wrong = sols.get(("W", cid))
        tasks.append((cid, ref, wrong, ch["tests"], ch.get("boilerplate", "")))

    missing = [t[0] for t in tasks if t[1] is None or t[2] is None]
    tasks = [t for t in tasks if t[1] is not None and t[2] is not None]
    # Production contract: the editor seeds boilerplate and the learner's
    # full editor content is graded, so the graded unit is boiler+solution.
    tasks = [(cid, bo + "\n\n" + ref, bo + "\n\n" + wrong, tests)
             for (cid, ref, wrong, tests, bo) in tasks]

    passed, failed = 0, []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for cid, ok, msg in ex.map(verify, tasks):
            if ok:
                passed += 1
            else:
                failed.append((cid, msg))

    print(f"{passed} challenges verified, {len(failed)} failed, {len(missing)} missing solutions")
    for cid, msg in failed:
        print("  ✗", cid, "→", msg)
    for m in missing:
        print("  ✗", m, "→ missing solution entry")
    sys.exit(1 if (failed or missing) else 0)


if __name__ == "__main__":
    main()
