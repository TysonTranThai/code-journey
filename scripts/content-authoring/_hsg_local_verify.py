#!/usr/bin/env python3
"""Local two-sided pre-verify for an hsg_mN.py module file.

Extracts every challenge(...) test list and every R/W body from the module
AST, compiles each body against the challenge's tests with the host clang++
(-std=c++20, same standard as the sandbox), and prints a PASS/FAIL table.

Gate: every R must PASS; every W must FAIL. Run BEFORE emitting — the
container harness (verify-challenges-hsg.mjs) remains the final authority.

Usage: python3 _hsg_local_verify.py hsg_m8.py
"""
import ast
import os
import subprocess
import sys

Q = chr(92)
NL = chr(10)
BS = Q
TMP = "/tmp/hsgver"
STUBS = ("write_module", "write_lesson", "write_practice",
         "write_checkpoint", "challenge", "vi_challenge", "contest_test")


def load_module(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    env = {"__builtins__": __builtins__, "Q": Q, "NL": NL, "__file__": path}

    # Stub the authoring libraries so a FULL exec of the module file never
    # emits content: `from hsga import write_module` resolves against our
    # fake sys.modules entries and binds no-op functions. Full-file exec is
    # required because hsga_* modules define solution constants (CP_*, A*_R)
    # between the lesson calls and the practice call — slicing at `M = `
    # would leave them unbound.
    import types
    for name in ("hsg", "hsgi", "hsga"):
        stub = types.ModuleType(name)
        for fn in STUBS:
            setattr(stub, fn, (lambda *a, **k: None))
        sys.modules[name] = stub
    for fn in STUBS:
        env[fn] = (lambda *a, **k: None)
    exec(compile(src, path, "exec"), env)

    def ev(node):
        return eval(compile(ast.Expression(node), "<x>", "eval"), env, {})

    # Capture top-level `NAME = [contest_test(...), ...]` lists: the exec used
    # a stub contest_test (returns None), so evaluate the calls ourselves.
    tests_vars = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.List)
                and node.value.elts
                and all(isinstance(e, ast.Call)
                        and getattr(e.func, "id", None) == "contest_test"
                        for e in node.value.elts)):
            nm = node.targets[0].id
            tests_vars[nm] = [
                (ast.literal_eval(e.args[0]), ev(e.args[1]), ev(e.args[2]))
                for e in node.value.elts
            ]

    # Resolve NAME = NAME2 test-list aliases (e.g. CP_TESTS = A3_TESTS) to a
    # fixpoint so later aliases see earlier ones regardless of order.
    for _ in range(4):
        changed = False
        for node in tree.body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.Name)
                    and node.value.id in tests_vars
                    and node.targets[0].id not in tests_vars):
                tests_vars[node.targets[0].id] = tests_vars[node.value.id]
                changed = True
        if not changed:
            break

    # NAME = challenge(...) assignments, so write_checkpoint(ch=NAME) can be
    # resolved back to its challenge id.
    chal_by_name = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Call)
                and getattr(node.value.func, "id", None) == "challenge"
                and node.value.args):
            try:
                chal_by_name[node.targets[0].id] = ast.literal_eval(node.value.args[0])
            except Exception:
                pass

    chals, rbodies, wbodies, cp = {}, {}, {}, {}
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            continue
        if node.func.id == "challenge":
            cid = ast.literal_eval(node.args[0])
            tl = []
            for a in node.args:
                if isinstance(a, ast.List):
                    for it in a.elts:
                        if (isinstance(it, ast.Call)
                                and getattr(it.func, "id", None) == "contest_test"):
                            tl.append((ast.literal_eval(it.args[0]),
                                       ev(it.args[1]), ev(it.args[2])))
                elif isinstance(a, ast.Name):
                    # tests passed as a variable (P2_TESTS_* style)
                    for it in tests_vars.get(a.id, ev(a) or []):
                        tl.append(it)
            chals[cid] = tl
        elif node.func.id == "write_practice":
            for k in node.keywords:
                if k.arg == "solutions" and isinstance(k.value, ast.List):
                    for it in k.value.elts:
                        if isinstance(it, ast.Tuple) and len(it.elts) == 3:
                            cid = ast.literal_eval(it.elts[0])
                            rbodies[cid] = ev(it.elts[1])
                            wbodies[cid] = ev(it.elts[2])
        elif node.func.id == "write_checkpoint":
            # The checkpoint's challenge is the `ch` argument (a challenge()
            # call); its R/W arrive as solution=/wrong= keywords. Modules may
            # hold several checkpoints (contest series), so bind per call.
            cp_cid = None
            for a in node.args:
                if (isinstance(a, ast.Call)
                        and getattr(a.func, "id", None) == "challenge"
                        and a.args):
                    cp_cid = ast.literal_eval(a.args[0])
                    break
                if isinstance(a, ast.Name) and a.id in chal_by_name:
                    cp_cid = chal_by_name[a.id]
                    break
            r = w = None
            for k in node.keywords:
                if k.arg == "solution":
                    r = ev(k.value)
                elif k.arg == "wrong":
                    w = ev(k.value)
            if cp_cid is not None:
                if r is not None:
                    rbodies[cp_cid] = r
                if w is not None:
                    wbodies[cp_cid] = w
            else:
                # legacy single-checkpoint fallback
                if r is not None:
                    cp["R"] = r
                if w is not None:
                    cp["W"] = w
    # legacy fallback: attach the (only) checkpoint R/W to every challenge
    if cp and len(rbodies) == 0:
        for cid in chals:
            rbodies[cid] = cp["R"]
            wbodies[cid] = cp["W"]
    return chals, rbodies, wbodies


def esc(s):
    return s.replace(BS, BS * 2).replace('"', BS + '"').replace(NL, BS + "n")


def compile_run(driver_lines):
    os.makedirs(TMP, exist_ok=True)
    sol = os.path.join(TMP, "sol.cpp")
    exe = os.path.join(TMP, "sol")
    open(sol, "w").write(NL.join(driver_lines))
    r = subprocess.run(
        ["clang++", "-std=c++20", "-O0", "-o", exe, sol],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return "COMPILE-FAIL: " + r.stderr[:200]
    try:
        r2 = subprocess.run([exe], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return "TIMEOUT(>10s)"
    if r2.returncode == 0 and r2.stdout.strip() == "OK":
        return "PASS"
    return "FAIL(" + ((r2.stderr or r2.stdout).strip().replace(NL, " | ")[:110]) + ")"


def main():
    path = sys.argv[1]
    chals, rbodies, wbodies = load_module(path)
    bad = 0
    print("cid | R | W")
    for cid in sorted(rbodies):
        tests = chals.get(cid, [])
        if not tests:
            print(cid, "| NO-TESTS | -")
            bad += 1
            continue
        row = []
        for body in (rbodies.get(cid), wbodies.get(cid)):
            driver = [
                "#include <sstream>", "#include <iostream>",
                "#include <string>", "#include <vector>",
                "#include <algorithm>", "#include <numeric>",
                "#include <climits>",
            ]
            driver.append(body)
            driver.append("int main() {")
            for (n, inp, want) in tests:
                driver.append('  { std::istringstream in("' + esc(inp)
                              + '"); std::ostringstream out; solve(in, out);')
                driver.append('    if (!(out.str() == std::string("'
                              + esc(want) + '"))) return 1; }')
            driver.append('  std::cout << "OK"; return 0; }')
            row.append(compile_run(driver))
        # W must fail behaviorally: wrong answer, crash, or (for intentional
        # O(n)/O(n^2) near-misses) a timeout — same semantics as the real
        # container harness, which kills jobs over the time budget.
        ok = row[0] == "PASS" and (row[1].startswith("FAIL") or row[1].startswith("TIMEOUT"))
        if not ok:
            bad += 1
        print(cid, "|", row[0], "|", row[1], "" if ok else "  <-- NOT TWO-SIDED")
    print("two-sided:", "CLEAN" if bad == 0 else str(bad) + " DEFECTS")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
