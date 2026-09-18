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
    env = {"__builtins__": __builtins__, "Q": Q, "NL": NL}

    # find where the module body starts (M = "...") and exec the header
    m_marker = None
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "M"
                and isinstance(node.value, ast.Constant)):
            m_marker = node.lineno
            break
    hdr_end = src.index("M = ")
    header = src[:hdr_end]
    if "__file__" in header:
        header = header.replace(
            "os.path.dirname(os.path.abspath(__file__))",
            repr(os.path.dirname(path)),
        )
    mod = {"__file__": path}
    for fn in STUBS:
        mod[fn] = (lambda *a, **k: None)
    exec(compile(header, path, "exec"), mod)
    # bind every helper/constant the header defines (T, cpp, CPP_STD, ...)
    # except the stubbed write_* APIs and the module machinery itself
    for k, v in mod.items():
        if k.startswith("__") or k in STUBS or k in ("sys", "os"):
            continue
        if callable(v) and getattr(v, "__module__", None) == "hsg":
            continue
        env.setdefault(k, v)

    def ev(node):
        return eval(compile(ast.Expression(node), "<x>", "eval"), env, {})

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
            for k in node.keywords:
                if k.arg == "solution":
                    cp["R"] = ev(k.value)
                elif k.arg == "wrong":
                    cp["W"] = ev(k.value)
    # attach the checkpoint R/W to its challenge id
    for cid in chals:
        if cid not in rbodies and "R" in cp and cid not in rbodies:
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
                "#include <algorithm>",
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
        ok = row[0] == "PASS" and row[1].startswith("FAIL")
        if not ok:
            bad += 1
        print(cid, "|", row[0], "|", row[1], "" if ok else "  <-- NOT TWO-SIDED")
    print("two-sided:", "CLEAN" if bad == 0 else str(bad) + " DEFECTS")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
