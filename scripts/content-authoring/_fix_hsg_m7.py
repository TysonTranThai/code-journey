"""One-shot fixer for hsg_m7.py.

1. Test I/O strings hold literal backslash-n sequences; the platform
   convention (see green hsg_m6.py) is real newlines. Rewrite every string
   constant that contains backslash-n but no real newline (and is not C++
   code) with a json.dumps-produced literal.
2. write_practice(solutions=[...]) has 2-tuples (cid, R) — the W body is
   missing. Insert honest, deterministic W bodies after each R element.
3. The checkpoint's wrong solution (counts gaps, not planks) needs a
   discriminator: add a "tall gap" test where one gap of 10 with k=5
   planks must yield 5, not 10.

Idempotent: re-running finds nothing to do and exits 0.
"""
import ast
import json

P = "scripts/content-authoring/hsg_m7.py"
BS = chr(92)
NL = chr(10)

with open(P, encoding="utf-8") as f:
    src = f.read()

tree = ast.parse(src)


def seg(node):
    return ast.get_source_segment(src, node)


def lit(value):
    """Source text for a string literal holding real newlines."""
    return json.dumps(value, ensure_ascii=False)


# --- pass 1: fix literal-backslash-n strings -------------------------------
fixed_io = 0
repls = []  # (old_segment, new_segment)
for node in ast.walk(tree):
    if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
        continue
    v = node.value
    if NL in v:
        continue  # already real newlines
    if (BS + "n") not in v:
        continue
    if "#include" in v or "solve(" in v:
        continue  # C++ source, leave alone
    new_v = v.replace(BS + "n", NL)
    old = seg(node)
    new = lit(new_v)
    if old != new:
        repls.append((old, new))
        fixed_io += 1

for old, new in repls:
    src = src.replace(old, new)

# --- pass 2: add the tall-gap discriminator to the checkpoint tests --------
ADDED_TEST = None
tree2 = ast.parse(src)
for node in ast.walk(tree2):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "challenge"
            and ast.literal_eval(node.args[0]) == "hsg-cp-m7-climb"):
        tests_list = node.args[3]
        names = [ast.literal_eval(e.args[0]) for e in tests_list.elts]
        if "tall gap" not in names:
            last = tests_list.elts[-1]
            end = (last.end_lineno, last.end_col_offset)
            new_test = (
                'contest_test("tall gap", "2 5' + BS + 'n0 10' + BS + 'n' + BS
                + 'n", "5' + BS + 'n", "One 10-high gap: 5 planks leave step 5; '
                'a wrong solver that counts gaps instead of planks says 10.")'
            )
            lines = src.split(NL)
            lines[end[0] - 1] = (lines[end[0] - 1][:end[1]] + ", " + new_test
                                 + lines[end[0] - 1][end[1]:])
            src = NL.join(lines)
            ADDED_TEST = "tall gap"

# --- pass 3: complete the 2-tuples with W bodies ---------------------------
HDR = (
    "#include <iostream>" + NL
    + "#include <algorithm>" + NL
    + "using namespace std;" + NL
    + "void solve(std::istream& in, std::ostream& out) {" + NL
)
FTR = "}" + NL

W_BODIES = {
    "hsg-p7-count-x": (
        HDR
        + "    int n, q; in >> n >> q;" + NL
        + "    vector<long long> a(n);" + NL
        + "    for (long long& x : a) in >> x;" + NL
        + "    while (q--) {" + NL
        + "        long long x; in >> x;" + NL
        + "        // near-miss: prints how many elements are STRICTLY BELOW x" + NL
        + "        int lb = int(lower_bound(a.begin(), a.end(), x) - a.begin());" + NL
        + "        out << lb << \"" + BS + "n\";" + NL
        + "    }" + NL
        + FTR
    ),
    "hsg-p7-closest": (
        HDR
        + "    int n, q; in >> n >> q;" + NL
        + "    vector<long long> a(n);" + NL
        + "    for (long long& x : a) in >> x;" + NL
        + "    while (q--) {" + NL
        + "        long long x; in >> x;" + NL
        + "        int lb = int(lower_bound(a.begin(), a.end(), x) - a.begin());" + NL
        + "        long long best;" + NL
        + "        if (lb == n) best = a[n-1];" + NL
        + "        else if (lb == 0) best = a[0];" + NL
        + "        else {" + NL
        + "            long long hi = a[lb], lo = a[lb-1];" + NL
        + "            long long dh = hi - x, dl = x - lo;" + NL
        + "            // near-miss: ties broken toward the LARGER value" + NL
        + "            best = (dh <= dl) ? hi : lo;" + NL
        + "        }" + NL
        + "        out << best << \"" + BS + "n\";" + NL
        + "    }" + NL
        + FTR
    ),
    "hsg-p7-cows": (
        HDR
        + "    int n, k; in >> n >> k;" + NL
        + "    vector<long long> p(n);" + NL
        + "    for (long long& x : p) in >> x;" + NL
        + "    sort(p.begin(), p.end());" + NL
        + "    long long lo = 1, hi = p[n-1] - p[0];" + NL
        + "    auto feasible = [&](long long d) {" + NL
        + "        int used = 1; long long last = p[0];" + NL
        + "        for (int i = 1; i < n; ++i)" + NL
        + "            // near-miss: strict > skips positions exactly d apart" + NL
        + "            if (p[i] - last > d) { ++used; last = p[i]; }" + NL
        + "        return used >= k;" + NL
        + "    };" + NL
        + "    while (lo < hi) {" + NL
        + "        long long mid = lo + (hi - lo + 1) / 2;" + NL
        + "        if (feasible(mid)) lo = mid; else hi = mid - 1;" + NL
        + "    }" + NL
        + "    out << lo << \"" + BS + "n\";" + NL
        + FTR
    ),
    "hsg-p7-router": (
        HDR
        + "    int n, k; in >> n >> k;" + NL
        + "    vector<long long> a(n);" + NL
        + "    for (long long& x : a) in >> x;" + NL
        + "    long long lo = *max_element(a.begin(), a.end()), hi = 0;" + NL
        + "    for (long long x : a) hi += x;" + NL
        + "    auto feasible = [&](long long cap) {" + NL
        + "        // near-miss: counts SPLITS, not segments — allows one too many" + NL
        + "        int segs = 0; long long cur = 0;" + NL
        + "        for (long long x : a) {" + NL
        + "            if (cur + x > cap) { ++segs; cur = x; }" + NL
        + "            else cur += x;" + NL
        + "        }" + NL
        + "        return segs <= k;" + NL
        + "    };" + NL
        + "    while (lo < hi) {" + NL
        + "        long long mid = lo + (hi - lo) / 2;" + NL
        + "        if (feasible(mid)) hi = mid; else lo = mid + 1;" + NL
        + "    }" + NL
        + "    out << lo << \"" + BS + "n\";" + NL
        + FTR
    ),
    "hsg-p7-sub-sum": (
        HDR
        + "    int n; long long s; in >> n >> s;" + NL
        + "    vector<long long> a(n);" + NL
        + "    for (long long& x : a) in >> x;" + NL
        + "    long long cur = 0; int l = 0;" + NL
        + "    bool ok = false;" + NL
        + "    for (int r = 0; r < n && !ok; ++r) {" + NL
        + "        cur += a[r];" + NL
        + "        // near-miss: >= s in the shrink loop discards exact hits" + NL
        + "        while (l <= r && cur >= s) { cur -= a[l]; ++l; }" + NL
        + "        if (cur == s) ok = true;" + NL
        + "    }" + NL
        + "    out << (ok ? \"YES\" : \"NO\") << \"" + BS + "n\";" + NL
        + FTR
    ),
}

tree3 = ast.parse(src)
done_w = []
for node in ast.walk(tree3):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "write_practice"):
        for k in node.keywords:
            if k.arg != "solutions" or not isinstance(k.value, ast.List):
                continue
            for it in k.value.elts:
                if not (isinstance(it, ast.Tuple) and len(it.elts) == 2):
                    continue
                cid = ast.literal_eval(it.elts[0])
                if cid not in W_BODIES:
                    continue
                r_node = it.elts[1]
                end = (r_node.end_lineno, r_node.end_col_offset)
                lines = src.split(NL)
                insertion = ", " + NL.join(lit(W_BODIES[cid]).split(NL))
                # splice the W literal right after the R element
                lines[end[0] - 1] = (lines[end[0] - 1][:end[1]] + insertion
                                     + lines[end[0] - 1][end[1]:])
                src = NL.join(lines)
                done_w.append(cid)

with open(P, "w", encoding="utf-8") as f:
    f.write(src)

print("io strings fixed:", fixed_io)
print("tall-gap test added:", ADDED_TEST)
print("W bodies inserted:", done_w)
ast.parse(src)
print("parses OK")
