import sys, types, subprocess, tempfile, os

MOD = "scripts/content-authoring/hsgi_m10.py"

rec = {"challenges": {}, "practice_solutions": [], "checkpoint": {}}

fake = types.ModuleType("hsgi")

def _challenge(cid, *a, **k):
    # challenge(cid, title, statement, tests, **kw) — tests = a[2]
    rec["challenges"][cid] = a[2]
    return cid

def _vi_challenge(*a, **k):
    return k

def _write_module(*a, **k):
    pass

def _write_lesson(*a, **k):
    pass

def _write_practice(mid, *a, **k):
    rec["practice_solutions"] = k.get("solutions") or []
    rec["practice_challenges"] = k.get("challenges") or []

def _write_checkpoint(mid, *a, **k):
    rec["checkpoint"] = {"challenge": k.get("challenge"), "solution": k.get("solution"), "wrong": k.get("wrong")}

for nm in ["write_module", "write_lesson", "write_practice", "write_checkpoint"]:
    setattr(fake, nm, {"write_module": _write_module, "write_lesson": _write_lesson,
                       "write_practice": _write_practice, "write_checkpoint": _write_checkpoint}[nm])
setattr(fake, "challenge", _challenge)
setattr(fake, "vi_challenge", _vi_challenge)
setattr(fake, "contest_test", lambda *a, **k: (a, k))

sys.modules["hsgi"] = fake

code = open(MOD, encoding="utf-8").read()
g = {"__name__": "probe", "__file__": MOD}
exec(compile(code, MOD, "exec"), g)

CPP_STD = g["CPP_STD"]
cpp = g["cpp"]

def render(s):
    return s.replace("{{NL}}", "\n")

HDR = "\n".join([
    "#include <iostream>",
    "#include <algorithm>",
    "#include <vector>",
    "#include <queue>",
    "#include <array>",
    "using namespace std;",
    "",
])

def run2(body, inp):
    prog = HDR + render(body) + "\nint main(){ solve(std::cin, std::cout); return 0; }\n"
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "s.cpp")
        open(f, "w").write(prog)
        c = subprocess.run(["clang++", "-std=c++20", "-o", os.path.join(d, "s"), f], capture_output=True, text=True, timeout=60)
        if c.returncode != 0:
            return "COMPILE: " + c.stderr[:400]
        r = subprocess.run([os.path.join(d, "s")], input=inp, capture_output=True, text=True, timeout=15)
        return r.stdout

targets = sys.argv[1:] or ["hsgi-p10-diameter", "hsgi-p10-preorder", "hsgi-cp-m10-cable"]

# practice pairs
for cid, rb, wb in rec["practice_solutions"]:
    if cid in targets:
        print("=====", cid)
        for i, (args, kw) in enumerate(rec["challenges"][cid], 1):
            name, inp, want = args[0], args[1], args[2]
            got = run2(render(rb), inp)
            if got != want:
                print(f"T{i} {name!r}:")
                print("  want:", repr(want[:150]))
                print("  got :", repr(got[:150]))

# checkpoint
ch = rec["checkpoint"]
cid = ch["challenge"] if isinstance(ch["challenge"], str) else None
if "hsgi-cp-m10-cable" in targets and ch.get("solution"):
    print("===== hsgi-cp-m10-cable")
    for i, (args, kw) in enumerate(rec["challenges"]["hsgi-cp-m10-cable"], 1):
        name, inp, want = args[0], args[1], args[2]
        got = run2(render(ch["solution"]), inp)
        if got != want:
            print(f"T{i} {name!r}:")
            print("  want:", repr(want[:150]))
            print("  got :", repr(got[:150]))
