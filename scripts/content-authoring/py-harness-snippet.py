import builtins as _builtins
import io as _io
import sys as _sys
from contextlib import redirect_stdout as _redirect_stdout


def _run_solution():
    _buf = _io.StringIO()
    _g = {"__name__": "__solution__", "__builtins__": _builtins}
    with _redirect_stdout(_buf):
        exec(SOLUTION_SOURCE, _g)
    return _buf.getvalue(), _g


_stdout_text, _globals = _run_solution()
printed = [line for line in _stdout_text.splitlines()]
stdout = _stdout_text

# Solution top-level names visible to author snippets (see python-runtime.ts).
# __builtins__ stays in _globals: solution-defined functions carry this dict as
# their globals, so builtins (sum, len, ValueError...) resolve when tests call
# those functions later.
globals().update(_globals)
__name__ = "__main__"
code = SOLUTION_SOURCE  # the learner's raw source, mirroring the JS test contract


def _no_input(*_a, **_k):
    raise AssertionError(
        "input() is not available in graded challenge runs - "
        "challenge solutions take parameters or print output."
    )


_builtins.input = _no_input
