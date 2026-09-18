"""One-shot fixer: correct the timezone R/W solution pair in hsg_m1.py.

Replaces the two solution lines containing `(t + k * 60) / 60` with the
floor-mod reference and the truncate-toward-zero near-miss.
Idempotent: aborts without writing if exactly two such lines are absent.
"""
import io

P = "scripts/content-authoring/hsg_m1.py"
with io.open(P, "r", encoding="utf-8") as f:
    lines = f.readlines()

hits = [i for i, ln in enumerate(lines) if "(t + k * 60) / 60" in ln]
if len(hits) != 2:
    raise SystemExit("expected exactly 2 timezone solution lines, found %d" % len(hits))

R_NEW = (
    '            "#include <iostream>\\nvoid solve(std::istream& in, std::ostream& out) {\\n'
    "    long long t, k;\\n    in >> t >> k;\\n    long long m = t + k * 60;\\n"
    "    long long x = ((m % 60) + 60) % 60;          // floor-mod minutes\\n"
    '    out << (((m - x) / 60 % 24) + 24) % 24 << "\\\\n";\\n}",\n'
)
W_NEW = (
    '            "#include <iostream>\\nvoid solve(std::istream& in, std::ostream& out) {\\n'
    "    long long t, k;\\n    in >> t >> k;\\n    long long m = t + k * 60;\\n"
    "    // near-miss: C++ division truncates toward zero — a negative hour\\n"
    "    // prints negative instead of wrapping into 0..23\\n"
    '    out << (m / 60) % 24 << "\\\\n";\\n}",\n'
)

# hits[0] is the R line, hits[1] the W line (emitted in that order).
lines[hits[1]] = W_NEW
lines[hits[0]] = R_NEW

with io.open(P, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("patched R line", hits[0] + 1, "W line", hits[1] + 1)
