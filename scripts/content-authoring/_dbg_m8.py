#!/usr/bin/env python3
"""Debug: find which vi_challenge receives a non-(name,hint) tuple."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pypb

orig = pypb.vi_challenge
calls = []


def spy(title, prompt, tests):
    for t in tests:
        if not (isinstance(t, tuple) and len(t) == 2):
            calls.append((title, t))
    return orig(title, prompt, tests)


pypb.vi_challenge = spy
try:
    exec(compile(open("scripts/content-authoring/pypb_m8.py", encoding="utf-8").read(), "pypb_m8.py", "exec"), {"__name__": "__main__", "__file__": "scripts/content-authoring/pypb_m8.py"})
except SystemExit:
    pass
except BaseException as e:
    print("stopped with:", type(e).__name__, str(e)[:80])
print("BAD CALLS:")
for title, t in calls:
    print("-", title, "->", repr(t)[:120])
