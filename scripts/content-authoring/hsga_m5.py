#!/usr/bin/env python3
"""HSG Advanced — Module 5: hsga-euler (Euler Tour Queries).

Subtree add / point get, path add via the 4-point LCA trick, and marked-node
subtree counts — all on BITs over the Euler tour, under n, q = 2·10^5.
Ground truth for big tests is computed by an embedded deterministic Python
reference (no RNG), following the Intermediate course's formula-array style.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsga import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

Q = chr(92)
NL = chr(10)


def cpp(s):
    return s.replace("{{NL}}", Q + "n")


def T(*lines):
    return "".join(l + NL for l in lines)


CPP_STD = cpp("""#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL


# ---------------------------------------------------------------- reference
def _tree(n, kind):
    """Deterministic parent array; kind 'bin' or 'path' or 'caterpillar'."""
    par = [0] * (n + 1)
    if kind == "bin":
        for v in range(2, n + 1): par[v] = v // 2
    elif kind == "path":
        for v in range(2, n + 1): par[v] = v - 1
    else:  # caterpillar: spine 1..n/2, each spine node has one leaf
        half = n // 2
        for v in range(2, half + 1): par[v] = v - 1
        for v in range(half + 1, n + 1): par[v] = v - half
    return par


def _euler(n, par):
    children = [[] for _ in range(n + 1)]
    for v in range(2, n + 1): children[par[v]].append(v)
    tin = [0] * (n + 1); tout = [0] * (n + 1); dep = [0] * (n + 1)
    timer = 1
    st = [(1, False)]
    while st:
        u, done = st.pop()
        if done:
            tout[u] = timer - 1
            continue
        tin[u] = timer; timer += 1
        st.append((u, True))
        for c in reversed(children[u]):
            dep[c] = dep[u] + 1
            st.append((c, False))
    LOG = 18
    up = [[0] * (n + 1) for _ in range(LOG)]
    for v in range(1, n + 1): up[0][v] = par[v]
    for k in range(1, LOG):
        for v in range(1, n + 1): up[k][v] = up[k-1][up[k-1][v]]

    def lca(u, v):
        if dep[u] < dep[v]: u, v = v, u
        d = dep[u] - dep[v]
        for k in range(LOG):
            if d >> k & 1: u = up[k][u]
        if u == v: return u
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]: u = up[k][u]; v = up[k][v]
        return par[u]
    return tin, tout, lca


class _BIT:
    def __init__(self, n):
        self.n = n; self.f = [0] * (n + 1)
    def upd(self, i, d):
        while i <= self.n: self.f[i] += d; i += i & (-i)
    def pref(self, i):
        s = 0
        while i > 0: s += self.f[i]; i -= i & (-i)
        return s


def _subtree_add_truth(n, kind, init, ops):
    """op ('add', v, x) adds x to subtree(v); op ('get', v) prints val(v)."""
    par = _tree(n, kind)
    tin, tout, _ = _euler(n, par)
    bit = _BIT(n)
    base = [0] * (n + 1)
    for v in range(1, n + 1): base[v] = init(v)
    out = []
    for op in ops:
        if op[0] == "add":
            _, v, x = op
            bit.upd(tin[v], x); bit.upd(tout[v] + 1, -x) if tout[v] + 1 <= n else bit.upd(tout[v] + 1, -x)
        else:
            _, v = op
            out.append(str(base[v] + bit.pref(tin[v])))
    return out


def _path_add_truth(n, kind, ops):
    """op ('add', u, v, x): +x on path u..v; op ('get', w): print val(w).
    Classic: point-adds at u, v, -x at l, -x at parent(l); value(w) =
    subtree-sum of w over the BIT."""
    par = _tree(n, kind)
    tin, tout, lca = _euler(n, par)
    bit = _BIT(n)
    out = []
    for op in ops:
        if op[0] == "add":
            _, u, v, x = op
            l = lca(u, v)
            bit.upd(tin[u], x); bit.upd(tin[v], x); bit.upd(tin[l], -x)
            if par[l]: bit.upd(tin[par[l]], -x)
        else:
            _, w = op
            out.append(str(bit.pref(tout[w]) - bit.pref(tin[w] - 1)))
    return out


def _subtree_cnt_truth(n, kind, ops):
    """op ('tog', v): toggle mark; op ('cnt', v): marked count in subtree(v)."""
    par = _tree(n, kind)
    tin, tout, _ = _euler(n, par)
    bit = _BIT(n)
    marked = [False] * (n + 1)
    out = []
    for op in ops:
        if op[0] == "tog":
            _, v = op
            d = -1 if marked[v] else 1
            marked[v] = not marked[v]
            bit.upd(tin[v], d)
        else:
            _, v = op
            out.append(str(bit.pref(tout[v]) - bit.pref(tin[v] - 1)))
    return out


M = "hsga-euler"
write_module(
    M,
    "Euler Tour Queries",
    "Flatten the tree once and every subtree becomes a range: BIT-backed subtree adds, marked-node counts, and path updates through the 4-point LCA trick.",
    "Truy vấn Euler tour",
    "Trải phẳng cây một lần và mọi cây con thành một đoạn: cộng cây con bằng BIT, đếm nút đánh dấu, và cập nhật đường đi bằng mẹo 4 điểm LCA.",
    ["hsga-m5-flatten", "hsga-m5-paths", "hsga-cp-m5"],
    ["hsga-p5-euler"],
)

write_lesson(
    M, "hsga-m5-flatten",
    "Subtree Problems as Range Problems",
    "One DFS numbering converts subtree add, subtree count, and point get into plain Fenwick exercises you can write in five minutes.",
    30,
    """
# Subtrees are ranges

Record `tin[v]` (DFS entry index) and `tout[v]` (last index inside v's
subtree). The subtree of v is then exactly the interval `[tin[v], tout[v]]`
of positions. Every subtree question becomes a range question:

- **Subtree add, point get**: range-add on `[tin[v], tout[v]]` = two BIT
  point updates (difference trick); value(w) = `prefix(tin[w])`.
- **Marked nodes in a subtree**: BIT of 0/1 marks at `tin` positions;
  count = `prefix(tout[v]) - prefix(tin[v]-1)`.
- **Subtree sum of values**: point updates carry the values themselves.

Recursion depth is the classic implementation trap on the sandbox: a path
graph of 2·10^5 nodes overflows an 8 MB stack with naive recursive DFS.
Write the DFS iteratively with an explicit stack (push (v, done-flag)).

Everything here is the payload of Module 4's Euler lesson, now exercised
under full load.
""",
    "Bài toán cây con thành bài toán đoạn",
    "Một lượt đánh số DFS biến cộng cây con, đếm cây con, truy vấn điểm thành bài Fenwick năm phút.",
    """
# Cây con là một đoạn

Ghi `tin[v]` (chỉ số DFS khi vào) và `tout[v]` (chỉ số cuối trong cây
con). Cây con của v đúng là đoạn `[tin[v], tout[v]]`. Mọi câu hỏi cây con
thành câu hỏi đoạn:

- **Cộng cây con, truy vấn điểm**: cộng đoạn `[tin[v], tout[v]]` = hai
  cập nhật điểm BIT (mẹo sai phân); giá trị(w) = `prefix(tin[w])`.
- **Đếm nút đánh dấu trong cây con**: BIT 0/1 tại vị trí tin; đếm =
  `prefix(tout[v]) − prefix(tin[v]−1)`.
- **Tổng giá trị cây con**: cập nhật điểm mang chính giá trị.

Bẫy cài đặt kinh điển trên sandbox: DFS đệ quy trên đường thẳng 2·10^5
đỉnh tràn stack — viết DFS bằng stack tường minh (đẩy (v, cờ-done)).
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m5-paths",
    "Path Updates with the 4-Point Trick",
    "Adding x to the path u..v is four point updates once you know the LCA — and reading a node is a subtree sum. Derivation, proof, and the classic off-by-one.",
    35,
    """
# Path add, point get

Store point updates in a BIT at `tin` positions. Define the value of w as
the **subtree sum of w** over the BIT:
`val(w) = prefix(tout[w]) - prefix(tin[w] - 1)`.

Why this reading works: the subtree of w contains exactly the `tin`
positions of nodes below w, so the reading sums every stored point inside
w's subtree.

The update — add x on path u..v, l = LCA(u, v):

```
upd(tin[u], x); upd(tin[v], x);
upd(tin[l], -x);
if (parent(l)) upd(tin[parent(l)], -x);
```

Proof sketch: val(w) counts stored points in subtree(w). A node z's stored
point is seen by w iff z is inside subtree(w) iff w is an **ancestor** of z
(inclusive). So val(w) = x·[w anc of u] + x·[w anc of v] − x·[w anc of l]
− x·[w anc of parent(l)]. For w on the path (w ≠ l): exactly one of u, v
lies in subtree(w), l and parent(l) do not → x. For w = l: both u and v
count, l cancels one → x. For w above l: two pluses and two minuses → 0.
For w outside: 0.

The off-by-one that kills implementations: using `prefix(tin[w])` instead
of the two-sided subtree read — that sums ROOT-side ancestors instead of
the subtree, and fails on any non-chain tree.
""",
    "Cập nhật đường đi bằng mẹo 4 điểm",
    "Cộng x vào đường u..v là bốn cập nhật điểm khi biết LCA — và đọc một nút là tổng cây con. Có suy ra, chứng minh, và lỗi lệch một của kinh điển.",
    """
# Cộng đường, truy vấn điểm

Lưu cập nhật điểm tại vị trí tin. Giá trị của w là **tổng cây con của w**:
`val(w) = prefix(tout[w]) − prefix(tin[w]−1)`.

Cập nhật — cộng x trên đường u..v với l = LCA:

```
upd(tin[u], x); upd(tin[v], x);
upd(tin[l], -x);
if (cha(l)) upd(tin[cha(l)], -x);
```

Chứng minh: val(w) đếm điểm lưu trong subtree(w), tức mọi z mà w là tổ
 tiên (kể cả z = w). Kiểm bốn trường hợp: w trên đường (≠ l) được đúng
một dấu +; w = l được hai + một −; w trên l được 2+ 2− = 0; w ngoài
đường = 0.

Lỗi chết người: dùng `prefix(tin[w])` (một phía) thay vì đọc hai phía —
đó là tổng phần tổ tiên phía gốc, sai trên mọi cây không phải đường
thẳng.
""",
    difficulty="advanced",
)

# ---------------------------------------------------------------- checkpoint
CP_M5_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> tin(n + 1), tout(n + 1);
    // iterative euler tour
    vector<pair<int, bool>> st; st.push_back({1, false});
    int timer = 1;
    while (!st.empty()) {
        auto [u, done] = st.back(); st.pop_back();
        if (done) { tout[u] = timer - 1; continue; }
        tin[u] = timer++;
        st.push_back({u, true});
        for (int i = (int)ch[u].size() - 1; i >= 0; --i) st.push_back({ch[u][i], false});
    }
    vector<long long> fen(n + 1, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "SA") { int v; long long x; in >> v >> x; upd(tin[v], x); if (tout[v] + 1 <= n) upd(tout[v] + 1, -x); }
        else { int v; in >> v; out << pref(tin[v]) << "{{NL}}"; }
    }
""") + END

CP_M5_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> tin(n + 1), tout(n + 1);
    vector<pair<int, bool>> st; st.push_back({1, false});
    int timer = 1;
    while (!st.empty()) {
        auto [u, done] = st.back(); st.pop_back();
        if (done) { tout[u] = timer - 1; continue; }
        tin[u] = timer++;
        st.push_back({u, true});
        for (int i = (int)ch[u].size() - 1; i >= 0; --i) st.push_back({ch[u][i], false});
    }
    vector<long long> add(n + 1, 0);
    // WRONG: applies each subtree add by walking the subtree's node list —
    // O(subtree size) per op; 10^5 root adds on n = 2·10^5 is 2·10^10 steps.
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "SA") {
            int v; long long x; in >> v >> x;
            vector<pair<int, bool>> s2; s2.push_back({v, false});
            while (!s2.empty()) {
                auto [u, d] = s2.back(); s2.pop_back();
                add[u] += x;
                if (!d) { s2.push_back({u, true}); for (int c : ch[u]) s2.push_back({c, false}); }
            }
        } else { int v; in >> v; out << add[v] << "{{NL}}"; }
    }
""") + END

_n = 200000
_par = _tree(_n, "caterpillar")
_tin, _tout, _lca = _euler(_n, _par)
# big workload: 50000 subtree adds (alternating roots/spine), 50000 point gets
_ops_big = []
for i in range(50000):
    _ops_big.append(("add", 1 + (i * 4) % _n, (i % 2 * 2 - 1) * (i + 1)))
for i in range(50000):
    _ops_big.append(("get", 1 + (i * 7) % _n))
_big_in = [f"{_n} {len(_ops_big)}"] + [str(_par[v]) for v in range(2, _n + 1)]
for op in _ops_big:
    _big_in.append(f"SA {op[1]} {op[2]}" if op[0] == "add" else f"GET {op[1]}")
_big_res = _subtree_add_truth(_n, "caterpillar", lambda v: 0, _ops_big)

CK_TESTS = [
    contest_test("hand tree", T("6 6", "1 1 2 2 3", "SA 2 10", "GET 4", "GET 3", "GET 2", "SA 1 -1", "GET 5"), T("10", "0", "10", "9"),
        "Caterpillar: par = 1→{2,3}, 2→{4,5}, 3→{6}. Subtree(2)={2,4,5}; then root −1 shifts every node: GET 5 = 10 − 1 = 9."),
    contest_test("single node subtree", T("3 3", "1 2", "SA 3 7", "GET 3", "GET 1"), T("7", "0"),
        "Leaf add does not touch the root."),
    contest_test("n=200000 caterpillar load",
        T(*_big_in), T(*_big_res),
        "50000 subtree adds + 50000 point gets on a caterpillar tree; the subtree-walk wrong solution costs ~2·10^10 node visits."),
]

write_checkpoint(
    M, "hsga-cp-m5", "Checkpoint — Euler Tour under Load",
    "Subtree adds and point gets on a 2·10^5-node caterpillar. The tour turns both into BIT lines; walking subtrees node-by-node times out.",
    25,
    """
**Checkpoint — Euler tour.** Cây n = 200 000 đỉnh (cha v cho trên dòng 2).
q thao tác: `SA v x` = cộng x vào cây con(v); `GET v` = in giá trị nút v.
Tour biến cả hai thành dòng BIT; đi từng nút của cây con sẽ quá thời gian.
""",
    "Điểm kiểm tra — Euler tour dưới tải",
    "Cộng cây con và truy vấn điểm trên cây 200 000 đỉnh dạng sâu bướm.",
    """
**Checkpoint — Euler tour.** Cây n = 200 000 đỉnh. `SA v x` cộng x vào
cây con(v); `GET v` in giá trị nút v.
""",
    challenge(
        "hsga-cp-m5-euler",
        "Subtree Add, Point Get",
        """**Bài toán.** A rooted tree (root 1), parents for v = 2..n, all initial
values 0. q operations: `SA v x` adds x to every node of subtree(v);
`GET v` prints the current value of node v.

**Constraints:** 1 ≤ n, q ≤ 200 000; |x| ≤ 10^9; answers fit in long long.

Euler tour + difference BIT: O(log n) per operation.
""",
        CK_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Cộng cây con, truy vấn điểm",
        """**Bài toán.** Cây gốc 1, cha của v cho trên dòng 2..n, giá trị ban đầu
0. q thao tác: `SA v x` cộng x vào mọi nút của cây con(v); `GET v` in giá
trị hiện tại của nút v.""",
        [("cây tay", "Subtree(2) gồm 2, 4, 5 — cộng 10 rồi đọc từng nút."),
         ("nút lá", "Cộng vào lá không ảnh hưởng gốc."),
         ("n=200000 sâu bướm", "50000 lần cộng cây con + 50000 lần đọc — đi từng nút là ~2·10^10 bước.")],
    ),
    solution=CP_M5_R,
    wrong=CP_M5_W,
)

# ------------------------------------------------------------ practice R/W
# A1: subtree add / point get (same protocol as checkpoint, own tests)
A1_R = CP_M5_R
A1_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<long long> add(n + 1, 0);
    // WRONG: walks the whole subtree per add — O(size) per op.
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "SA") {
            int v; long long x; in >> v >> x;
            vector<pair<int, bool>> s2; s2.push_back({v, false});
            while (!s2.empty()) {
                auto [u, d] = s2.back(); s2.pop_back();
                if (!d) { add[u] += x; s2.push_back({u, true}); for (int c : ch[u]) s2.push_back({c, false}); }
            }
        } else { int v; in >> v; out << add[v] << "{{NL}}"; }
    }
""") + END

_a1_ops = []
for i in range(40000):
    _a1_ops.append(("add", 1 + (i * 9) % _n, i + 1))
for i in range(40000):
    _a1_ops.append(("get", 1 + (i * 13) % _n))
_a1_in = [f"{_n} {len(_a1_ops)}"] + [str(_par[v]) for v in range(2, _n + 1)]
for op in _a1_ops:
    _a1_in.append(f"SA {op[1]} {op[2]}" if op[0] == "add" else f"GET {op[1]}")
_a1_res = _subtree_add_truth(_n, "caterpillar", lambda v: 0, _a1_ops)

A1_TESTS = [
    contest_test("hand tree", T("6 4", "1 1 2 2 3", "SA 2 10", "GET 4", "GET 6", "SA 3 5"), T("10", "0"),
        "Subtree(2)={2,4,5}; subtree(3)={3,6}."),
    contest_test("root add reaches all", T("3 2", "1 2", "SA 1 4", "GET 2"), T("4"),
        "Root subtree is the whole tree."),
    contest_test("n=200000 bulk",
        T(*_a1_in), T(*_a1_res),
        "40000 subtree adds + 40000 gets interleaved by no particular order; per-op must be O(log n)."),
]

# A2: path add via 4-point trick
A2_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> tin(n + 1), tout(n + 1), dep(n + 1, 0);
    vector<pair<int, bool>> st; st.push_back({1, false});
    int timer = 1;
    while (!st.empty()) {
        auto [u, done] = st.back(); st.pop_back();
        if (done) { tout[u] = timer - 1; continue; }
        tin[u] = timer++;
        st.push_back({u, true});
        for (int i = (int)ch[u].size() - 1; i >= 0; --i) { dep[ch[u][i]] = dep[u] + 1; st.push_back({ch[u][i], false}); }
    }
    vector<vector<int>> up(18, vector<int>(n + 1, 0));
    for (int v = 1; v <= n; ++v) up[0][v] = par[v];
    for (int k = 1; k < 18; ++k)
        for (int v = 1; v <= n; ++v) up[k][v] = up[k-1][up[k-1][v]];
    auto lca = [&](int u, int v) {
        if (dep[u] < dep[v]) swap(u, v);
        int d = dep[u] - dep[v];
        for (int k = 0; k < 18; ++k) if (d >> k & 1) u = up[k][u];
        if (u == v) return u;
        for (int k = 17; k >= 0; --k)
            if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
        return par[u];
    };
    vector<long long> fen(n + 1, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "PA") {
            int u, v; long long x; in >> u >> v >> x;
            int l = lca(u, v);
            upd(tin[u], x); upd(tin[v], x); upd(tin[l], -x);
            if (par[l]) upd(tin[par[l]], -x);
        } else {
            int w; in >> w;
            out << pref(tout[w]) - pref(tin[w] - 1) << "{{NL}}";
        }
    }
""") + END

A2_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<long long> add(n + 1, 0);
    // WRONG: adds x by walking u..v node-by-node (climb the deeper, then
    // both) — O(depth) per op; on the path graph with far endpoints that is
    // O(n) per op and 10^5 ops time out.
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "PA") {
            int u, v; long long x; in >> u >> v >> x;
            // walk both up to root, marking by depth matching
            vector<int> au, av;
            for (int z = u; z; z = par[z]) au.push_back(z);
            for (int z = v; z; z = par[z]) av.push_back(z);
            if (au.size() < av.size()) swap(au, av), swap(u, v);
            int du = (int)au.size() - (int)av.size();
            while (du--) { add[u] += x; u = par[u]; }
            int vv = v;
            while (u != vv) { add[u] += x; add[vv] += x; u = par[u]; vv = par[vv]; }
            add[u] += x;
        } else { int w; in >> w; out << add[w] << "{{NL}}"; }
    }
""") + END

_pn = 200000
_ppar = _tree(_pn, "path")
_a2_ops = []
for i in range(30000):
    u = _pn - (i * 3) % _pn
    v = 1 + (i * 5) % _pn
    _a2_ops.append(("add", u, v, ((i % 2) * 2 - 1) * (i + 1)))
for i in range(30000):
    _a2_ops.append(("get", 1 + (i * 11) % _pn))
_a2_in = [f"{_pn} {len(_a2_ops)}"] + [str(_ppar[v]) for v in range(2, _pn + 1)]
for op in _a2_ops:
    if op[0] == "add": _a2_in.append(f"PA {op[1]} {op[2]} {op[3]}")
    else: _a2_in.append(f"GET {op[1]}")
_a2_res = _path_add_truth(_pn, "path", _a2_ops)

A2_TESTS = [
    contest_test("cross branches", T("6 6", "1 1 2 2 3", "PA 4 6 10", "GET 4", "GET 2", "GET 6", "GET 3", "GET 5"), T("10", "10", "10", "10", "0"),
        "Path 4-2-1-3-6 gets +10; leaf 5 untouched."),
    contest_test("lca at endpoint", T("6 3", "1 1 2 2 3", "PA 4 2 5", "GET 4", "GET 2"), T("5", "5"),
        "LCA is an endpoint: 4-2 gets +5."),
    contest_test("n=200000 path load",
        T(*_a2_in), T(*_a2_res),
        "30000 far-apart path adds + 30000 gets on a 200000-node path; walk-per-op costs ~6·10^9 steps."),
]

# A3: marked-node subtree count
A3_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> tin(n + 1), tout(n + 1);
    vector<pair<int, bool>> st; st.push_back({1, false});
    int timer = 1;
    while (!st.empty()) {
        auto [u, done] = st.back(); st.pop_back();
        if (done) { tout[u] = timer - 1; continue; }
        tin[u] = timer++;
        st.push_back({u, true});
        for (int i = (int)ch[u].size() - 1; i >= 0; --i) st.push_back({ch[u][i], false});
    }
    vector<long long> fen(n + 1, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    vector<char> marked(n + 1, 0);
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "TOG") { int v; in >> v; long long d = marked[v] ? -1 : 1; marked[v] ^= 1; upd(tin[v], d); }
        else { int v; in >> v; out << pref(tout[v]) - pref(tin[v] - 1) << "{{NL}}"; }
    }
""") + END

A3_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<char> marked(n + 1, 0);
    // WRONG: DFS-counts the subtree on every query — O(size) per count.
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "TOG") { int v; in >> v; marked[v] ^= 1; }
        else {
            int v; in >> v;
            long long cnt = 0;
            vector<pair<int, bool>> s2; s2.push_back({v, false});
            while (!s2.empty()) {
                auto [u, d] = s2.back(); s2.pop_back();
                if (!d) { cnt += marked[u]; for (int c : ch[u]) s2.push_back({c, false}); }
            }
            out << cnt << "{{NL}}";
        }
    }
""") + END

_a3_ops = []
for i in range(40000):
    _a3_ops.append(("tog", 1 + (i * 17) % _n))
for i in range(40000):
    _a3_ops.append(("cnt", 1 + (i * 23) % _n))
_a3_in = [f"{_n} {len(_a3_ops)}"] + [str(_par[v]) for v in range(2, _n + 1)]
for op in _a3_ops:
    _a3_in.append(f"TOG {op[1]}" if op[0] == "tog" else f"CNT {op[1]}")
_a3_res = _subtree_cnt_truth(_n, "caterpillar", _a3_ops)

A3_TESTS = [
    contest_test("toggle twice", T("5 4", "1 1 2 2", "TOG 4", "CNT 2", "TOG 4", "CNT 2"), T("1", "0"),
        "Mark leaf 4, count, unmark, count."),
    contest_test("nested counts", T("5 4", "1 1 2 2", "TOG 4", "TOG 5", "CNT 2", "CNT 1"), T("2", "2"),
        "Both leaves under 2; root sees them too."),
    contest_test("n=200000 mixed toggles",
        T(*_a3_in), T(*_a3_res),
        "40000 toggles + 40000 subtree counts; DFS-per-count costs ~4·10^9 node visits on the caterpillar."),
]

VI_P5 = {
    "hsga-p5-euler": vi_challenge(
        "Bộ ba truy vấn Euler",
        """**Bài toán.** Ba bài: cộng cây con/truy vấn điểm; cộng đường/truy vấn
điểm (mẹo 4 điểm); bật/tắt đánh dấu + đếm cây con.""",
        [("cộng cây con", "Hai cập nhật điểm sai phân là đủ."),
         ("cộng đường", "Bốn điểm cập nhật với LCA; đọc là tổng cây con HAI PHÍA."),
         ("đếm đánh dấu", "BIT 0/1 tại vị trí tin; đếm bằng hiệu tiền tố.")],
    ),
}

write_practice(
    M, "hsga-p5-euler", "Euler Query Trio",
    "Three tour-backed problems: subtree add/point get, path add via the 4-point trick, and marked-subtree counting — each with a walk-per-op killer test.",
    "Bộ ba truy vấn Euler",
    "Ba bài dựa trên tour: cộng cây con/truy vấn điểm, cộng đường bằng mẹo 4 điểm, và đếm cây con đánh dấu — mỗi bài có test giết cách đi từng nút.",
    "hsga-m5-paths",
    110,
    "advanced",
    [
        challenge("hsga-p5-subtree", "Subtree Add, Point Get",
            """**Bài toán.** Rooted tree (root 1), initial zeros. q ops: `SA v x`
adds x to subtree(v); `GET v` prints value(v).

**Constraints:** 1 ≤ n, q ≤ 200 000; |x| ≤ 10^9.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p5-pathadd", "Path Add via Four Points",
            """**Bài toán.** Rooted tree (root 1), initial zeros. q ops:
`PA u v x` adds x to every node on the path u..v; `GET w` prints value(w).

**Constraints:** 1 ≤ n, q ≤ 200 000; |x| ≤ 10^9. Four point updates +
one subtree-sum read per operation.
""",
            A2_TESTS, level="combination", difficulty="advanced"),
        challenge("hsga-p5-marks", "Marked Nodes in a Subtree",
            """**Bài toán.** Rooted tree (root 1). q ops: `TOG v` toggles the mark
on node v; `CNT v` prints the number of marked nodes in subtree(v).

**Constraints:** 1 ≤ n, q ≤ 200 000. BIT over tin positions.
""",
            A3_TESTS, level="independent", difficulty="advanced"),
    ],
    VI_P5,
    solutions=[
        ("hsga-p5-subtree", A1_R, A1_W),
        ("hsga-p5-pathadd", A2_R, A2_W),
        ("hsga-p5-marks", A3_R, A3_W),
    ],
)
