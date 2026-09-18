#!/usr/bin/env python3
"""Debug: run wrong solution of py-ex-raise-negative + py-ex-safe-int through the real harness."""
import builtins as _builtins
import io as _io
import sys as _sys
from contextlib import redirect_stdout as _redirect_stdout

CASES = {
    "py-ex-raise-negative": (
        # WRONG solution (from ledger)
        'def set_age(age):\n    if not (0 <= age <= 150):\n        raise ValueError(f"invalid age: {age}")\n    return min(age, 150)',
        # test snippet (from challenge JSON)
        'assert set_age(30) == 30\ntry:\n    set_age(200)\n    assert False, "200 must raise"\nexcept ValueError as e:\n    assert "200" in str(e), "message must mention the bad value"',
    ),
    "py-ex-safe-int": (
        'text = "42x"\ntry:\n    number = int(text)\n    print("converted:", number)\nexcept:\n    print("bad input, skipping")',
        'assert printed[0] == "bad input, skipping", f"got {printed}"',
    ),
}

for cid, (solution, snippet) in CASES.items():
    SOLUTION_SOURCE = solution
    _buf = _io.StringIO()
    _g = {"__name__": "__solution__", "__builtins__": _builtins}
    with _redirect_stdout(_buf):
        exec(SOLUTION_SOURCE, _g)
    printed = [line for line in _buf.getvalue().splitlines()]
    stdout = _buf.getvalue()
    code = SOLUTION_SOURCE
    globals().update(_g)
    __name__ = "__main__"
    try:
        exec(snippet, globals())
        print(cid, "-> SNIPPET PASSED (harness would mark WRONG as pass)")
    except BaseException as e:
        print(cid, "-> SNIPPET FAILED:", type(e).__name__, str(e)[:90])
