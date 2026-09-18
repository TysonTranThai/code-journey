"""One-shot fixer for the four M3–M5 defects surfaced by the harness.

1. hsg-p3-max-k-sum W: replace the "merely slow" O(n·k) near-miss with an
   honest correctness bug (window slide forgets to drop the old element).
2. hsg-p4-duplicates R+W: add missing `#include <vector>` + `using namespace std;`.
3. hsg-p5-waiting: correct the reverse-sorted expectation (0+1+2+4 = 7, not 8)
   in the test hint and the VI overlay.
4. hsg-p5-cover W: replace the no-op near-miss with the exclusive-end
   (half-open) bug, which fails the touching-ends test.

Line-based; aborts without writing if any anchor is missing.
"""
import io, json

P = "scripts/content-authoring/hsg_m3_m5.py"
lines = io.open(P, encoding="utf-8").readlines()


def find_one(pred, what):
    hits = [i for i, ln in enumerate(lines) if pred(ln)]
    assert len(hits) == 1, f"{what}: expected 1 hit, got {len(hits)}"
    return hits[0]


# --- 1. max-k-sum W -------------------------------------------------------
mkW_cpp = (
    "#include <iostream>\n#include <algorithm>\nusing namespace std;\n"
    "void solve(std::istream& in, std::ostream& out) {\n"
    "    int n, k; in >> n >> k;\n"
    "    vector<long long> a(n);\n"
    "    for (long long& x : a) in >> x;\n"
    "    // near-miss: slides the window but never drops the old element\n"
    "    // (sum += a[i] without subtracting a[i-k]) — the running sum\n"
    "    // grows monotonically instead of tracking a fixed window\n"
    "    long long sum = 0;\n"
    "    for (int i = 0; i < k; ++i) sum += a[i];\n"
    "    long long best = sum;\n"
    "    for (int i = k; i < n; ++i) {\n"
    "        sum += a[i];\n"
    "        best = max(best, sum);\n"
    "    }\n"
    "    out << best << \"\\n\";\n"
    "}"
)
i = find_one(lambda ln: "near-miss: O(n*k) double loop" in ln, "max-k-sum W")
indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
lines[i] = indent + json.dumps(mkW_cpp) + ",\n"

# --- 2. duplicates R+W includes -------------------------------------------
i = find_one(
    lambda ln: '"#include <iostream>\\nvoid solve' in ln
    and "seen(n + 1" in ln
    and "i <= n" in ln,
    "duplicates R",
)
lines[i] = lines[i].replace(
    '"#include <iostream>\\nvoid solve',
    '"#include <iostream>\\n#include <vector>\\nusing namespace std;\\nvoid solve',
    1,
)
i = find_one(
    lambda ln: '"#include <iostream>\\nvoid solve' in ln
    and "seen(n + 1" in ln
    and "i < n; ++i" in ln,
    "duplicates W",
)
lines[i] = lines[i].replace(
    '"#include <iostream>\\nvoid solve',
    '"#include <iostream>\\n#include <vector>\\nusing namespace std;\\nvoid solve',
    1,
)

# --- 3. waiting expectation ------------------------------------------------
i = find_one(lambda ln: '"reverse sorted"' in ln, "waiting test")
lines[i] = (
    '        contest_test("reverse sorted", "4\\n3 2 1 1\\n", "7\\n", '
    '"Sorted ascending 1,1,2,3: waits 0+1+2+4 = 7."),\n'
)
i = find_one(lambda ln: "chờ 0+1+2+5 = 8." in ln, "waiting VI overlay")
lines[i] = lines[i].replace("chờ 0+1+2+5 = 8.", "chờ 0+1+2+4 = 7.")

# --- 4. cover W -------------------------------------------------------------
covW_cpp = (
    "#include <iostream>\n#include <algorithm>\nusing namespace std;\n"
    "void solve(std::istream& in, std::ostream& out) {\n"
    "    int n; in >> n;\n"
    "    vector<pair<long long, long long>> v(n);\n"
    "    for (auto& p : v) in >> p.first >> p.second;\n"
    "    vector<pair<long long, int>> ev;\n"
    "    for (auto& p : v) { ev.push_back({p.first, +1}); ev.push_back({p.second, -1}); }\n"
    "    sort(ev.begin(), ev.end());\n"
    "    // near-miss: treats the end as exclusive (interval [s, e) not [s, e]),\n"
    "    // so intervals that merely touch at one point count as disjoint\n"
    "    int cur = 0, best = 0;\n"
    "    for (auto& e : ev) {\n"
    "        cur += e.second;\n"
    "        if (e.second == +1) best = max(best, cur);\n"
    "    }\n"
    "    out << best << \"\\n\";\n"
    "}"
)
i = find_one(lambda ln: "near-miss: counts the -1 events" in ln, "cover W comment")
indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
lines[i] = indent + json.dumps(covW_cpp) + ",\n"

io.open(P, "w", encoding="utf-8").writelines(lines)
print("all 4 fixes applied")
