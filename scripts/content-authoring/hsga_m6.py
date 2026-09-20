#!/usr/bin/env python3
"""HSG Advanced — Module 6: hsga-treedp (Tree DP).

The take/skip (in/out) discipline on rooted trees: weighted independent set,
diameter via the cross term checked at every node, minimum vertex cover, and
rerooting for all-nodes distance sums. Ground truth for big tests is computed
by deterministic in-module Python models (no RNG).

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


# ---------------------------------------------------------------- models
def _tree(n, kind):
    par = [0] * (n + 1)
    if kind == "bin":
        for v in range(2, n + 1): par[v] = v // 2
    elif kind == "path":
        for v in range(2, n + 1): par[v] = v - 1
    else:  # caterpillar: spine 1..n/2, one leaf per spine node
        half = n // 2
        for v in range(2, half + 1): par[v] = v - 1
        for v in range(half + 1, n + 1): par[v] = v - half
    return par


def _postorder(n, par):
    ch = [[] for _ in range(n + 1)]
    for v in range(2, n + 1): ch[par[v]].append(v)
    st = [(1, False)]
    order = []
    while st:
        u, done = st.pop()
        if done:
            order.append(u)
            continue
        st.append((u, True))
        for c in ch[u]: st.append((c, False))
    return order, ch  # children always precede parents


def _maxind(n, par, val):
    order, ch = _postorder(n, par)
    din = [0] * (n + 1); dout = [0] * (n + 1)
    for u in order:
        din[u] = val[u] + sum(dout[c] for c in ch[u])
        dout[u] = sum(max(din[c], dout[c]) for c in ch[u])
    return max(din[1], dout[1])


def _diameter(n, par, w):
    order, ch = _postorder(n, par)
    h = [0] * (n + 1); best = 0
    for u in order:
        h1 = h2 = 0
        for c in ch[u]:
            hh = h[c] + w[c]
            if hh > h1: h2, h1 = h1, hh
            elif hh > h2: h2 = hh
        best = max(best, h1 + h2)
        h[u] = h1
    return best


def _mincover(n, par):
    order, ch = _postorder(n, par)
    inn = [0] * (n + 1); out = [0] * (n + 1)
    for u in order:
        inn[u] = 1 + sum(min(inn[c], out[c]) for c in ch[u])
        out[u] = sum(inn[c] for c in ch[u])
    return min(inn[1], out[1])


def _dist_sums_bfs(n, par):
    """O(n^2) brute — for small ground truth."""
    adj = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        adj[v].append(par[v]); adj[par[v]].append(v)
    res = []
    for s in range(1, n + 1):
        dist = [-1] * (n + 1); dist[s] = 0
        q = [s]
        for u in q:
            for x in adj[u]:
                if dist[x] < 0:
                    dist[x] = dist[u] + 1; q.append(x)
        res.append(str(sum(dist[1:n + 1])))
    return res


M = "hsga-treedp"
write_module(
    M,
    "Tree DP: Take, Skip, and Reroot",
    "The in/out state pattern solves independent set, vertex cover, and matching-shaped problems on trees; the cross term finds diameters; rerooting answers every node's question in one extra pass.",
    "Quy hoạch động trên cây",
    "Mẫu trạng thái lấy/bỏ giải bài tập độc lập, đỉnh phủ trên cây; số hạng qua biên tìm đường đi dài nhất; đổi gốc trả lời câu hỏi của mọi đỉnh trong một lượt duyệt thêm.",
    ["hsga-m6-inout", "hsga-m6-cross", "hsga-cp-m6"],
    ["hsga-p6-treedp"],
)

write_lesson(
    M, "hsga-m6-inout",
    "The In/Out State Pattern",
    "Two states per node — best if u is taken, best if u is skipped — solve independent set, vertex cover, and friends in one post-order pass.",
    35,
    """
# dp_in and dp_out

Root the tree. For every node u define:

- `dp_in[u]` — the best value achievable **inside u's subtree if u is
  taken**;
- `dp_out[u]` — the best value **if u is not taken**.

Both are computed from children in one post-order pass:

```
dp_in[u]  = val[u] + sum(dp_out[c])                  // children forbidden
dp_out[u] = sum(max(dp_in[c], dp_out[c]))            // children free
answer   = max(dp_in[root], dp_out[root])
```

Instantiating the same skeleton:

- **Maximum weight independent set**: exactly the formula above.
- **Minimum vertex cover** (cover every edge): `dp_in[u] = 1 +
  sum(min(dp_in[c], dp_out[c]))`, `dp_out[u] = sum(dp_in[c])` — skipping u
  FORCES every child to be taken, because edge (u, c) must be covered.

The classic bugs, all three seen in real contests:

1. `dp_in[u] = val[u] + max(dp_in[c], dp_out[c])` — allows u and c both
   taken; not an independent set (overestimates whenever adjacency
   conflicts).
2. `dp_out[u] = sum(min(...))` for vertex cover — allows an uncovered edge
   (underestimates: returns 0 on any tree with leaves).
3. Recursive DFS on a path-shaped tree — stack overflow at n ≈ 10^5 on the
   8 MB sandbox stack. Iterative post-order with an explicit stack, or the
   pop-order trick (append u to `order` when the done-flag pops), is
   mandatory.

Values may be negative: the empty selection is legal, so the answer is at
least 0 — `dp_in` may be negative, and that is fine.

**Bài học (VI).** Gốc cây. Hai trạng thái: `dp_in[u]` — tốt nhất trong cây
con nếu lấy u; `dp_out[u]` — nếu bỏ u. Một lượt hậu thứ tự:
`dp_in[u] = val[u] + Σ dp_out[c]`, `dp_out[u] = Σ max(dp_in[c], dp_out[c])`.
Đỉnh phủ nhỏ nhất: `dp_in[u] = 1 + Σ min(dp_in[c], dp_out[c])`,
`dp_out[u] = Σ dp_in[c]` — bỏ u BUỘC mọi con phải lấy vì cạnh (u, c) phải
được phủ. Ba lỗi kinh điển: lấy cả u và c (không còn độc lập), dùng min
cho đỉnh phủ (cho phép cạnh chưa phủ — trả về 0), và DFS đệ quy trên cây
dạng đường (tràn stack ~10^5 đỉnh). Giá trị âm hợp lệ — chọn tập rỗng
nghĩa là đáp án ≥ 0.
""",
    "Mẫu trạng thái lấy/bỏ",
    "Hai trạng thái mỗi nút — tốt nhất nếu lấy u, tốt nhất nếu bỏ u — giải bài tập độc lập, đỉnh phủ và họ bài tương tự trong một lượt hậu thứ tự.",
    """
# dp_in và dp_out

Gốc cây. Với mỗi nút u định nghĩa:

- `dp_in[u]` — giá trị tốt nhất **trong cây con của u nếu lấy u**;
- `dp_out[u]` — giá trị tốt nhất **nếu bỏ u**.

Cả hai tính từ con trong một lượt hậu thứ tự:

```
dp_in[u]  = val[u] + Σ dp_out[c]                  // cấm con
dp_out[u] = Σ max(dp_in[c], dp_out[c])            // con tự do
đáp án    = max(dp_in[gốc], dp_out[gốc])
```

Cùng một khung:

- **Tập độc lập trọng số lớn nhất**: đúng công thức trên.
- **Đỉnh phủ nhỏ nhất** (phủ mọi cạnh): `dp_in[u] = 1 +
  Σ min(dp_in[c], dp_out[c])`, `dp_out[u] = Σ dp_in[c]` — bỏ u BUỘC
  mọi con phải lấy, vì cạnh (u, c) phải được phủ.

Ba lỗi kinh điển gặp trong contest:

1. `dp_in[u] = val[u] + max(dp_in[c], dp_out[c])` — cho u và c cùng lấy;
   không còn độc lập (đánh giá quá cao khi có xung đột kề).
2. `dp_out[u] = Σ min(...)` cho đỉnh phủ — cho phép cạnh chưa phủ
   (đánh giá thấp: trả về 0 trên mọi cây có lá).
3. DFS đệ quy trên cây dạng đường — tràn stack khi n ≈ 10^5 với stack
   8 MB của sandbox. Bắt buộc hậu thứ tự với stack tường minh hoặc mẹo
   pop-order (đẩy u vào `order` khi pop cờ done).

Giá trị có thể âm: chọn tập rỗng hợp lệ nên đáp án ít nhất 0 — dp_in âm
là bình thường.
""",
    difficulty="intermediate",
)

write_lesson(
    M, "hsga-m6-cross",
    "The Cross Term and Rerooting",
    "A diameter can bend anywhere — check h1+h2 at EVERY node. And one bottom-up + one top-down pass answer 'sum of distances from v' for all v at once.",
    35,
    """
# Diameters bend

Keep `height[u]` = the longest downward path from u (child heights plus
edge weights). At each node the best path that **bends** at u is
`h1 + h2` — the two largest child-heights. The tree diameter is the
maximum of h1 + h2 over ALL nodes, updated during the same post-order
pass:

```
h1 = h2 = 0;
for (c : ch[u]) {
    long long hh = height[c] + w[c];
    if (hh > h1) { h2 = h1; h1 = hh; } else if (hh > h2) h2 = hh;
}
best = max(best, h1 + h2);
height[u] = h1;
```

The bug that survives toy tests: updating `best` only at the ROOT. On a
broom (chain 1→2→3 with two leaves at 3) the root-only answer is the
depth 3, but the true diameter is 2 — the path bends at node 3, never
touching the root.

# Rerooting

Compute for every node v the sum of distances to all other nodes. Brute
force is O(n²). Two passes give O(n):

1. **Bottom-up**: `cnt[u]` = subtree size, `sd[u]` = sum of distances from
   u to every node inside its subtree: `sd[u] = Σ (sd[c] + cnt[c])`.
2. **Top-down**: `ans[root] = sd[root]`; walking parent → child,
   `ans[c] = ans[u] + (n − cnt[c]) − cnt[c]` — every node outside c's
   subtree gets 1 farther (n − cnt[c] of them), every node inside gets
   1 closer (cnt[c] of them).

The rerooting identity is worth memorizing: moving the root across an
edge changes the answer by `+ (n − cnt[c]) − cnt[c]`.

**Bài học (VI).** `height[u]` = đường đi xuống dài nhất từ u. Đường đi tốt
nhất bẻ gãy tại u là `h1 + h2` — hai chiều cao con lớn nhất. Đường đi dài
nhất của cây = max của h1 + h2 trên MỌI nút. Lỗi sống sót qua test nhỏ:
chỉ cập nhật ở gốc — trên cây chổi (1→2→3, hai lá tại 3) root-only ra 3,
đáp án thật là 2. Đổi gốc: lượt lên tính `cnt`, `sd`; lượt xuống
`ans[c] = ans[cha] + (n − cnt[c]) − cnt[c]` — đi qua một cạnh: n − cnt[c]
nút xa thêm 1, cnt[c] nút gần bớt 1.
""",
    "Số hạng qua biên và kỹ thuật đổi gốc",
    "Kiểm h1+h2 tại mọi nút để bắt đường đi bẻ gãy; đổi gốc trả lời tổng khoảng cách của mọi đỉnh trong O(n).",
    """
# Đường đi dài nhất bẻ gãy

Giữ `height[u]` = đường đi xuống dài nhất từ u (chiều cao con cộng trọng
số cạnh). Tại mỗi nút, đường đi tốt nhất **bẻ gãy** tại u là `h1 + h2` —
hai chiều cao con lớn nhất. Đường đi dài nhất của cây là max của h1 + h2
trên MỌI nút, cập nhật trong cùng lượt hậu thứ tự:

```
h1 = h2 = 0;
for (c : ch[u]) {
    long long hh = height[c] + w[c];
    if (hh > h1) { h2 = h1; h1 = hh; } else if (hh > h2) h2 = hh;
}
best = max(best, h1 + h2);
height[u] = h1;
```

Lỗi sống sót qua test nhỏ: chỉ cập nhật `best` ở GỐC. Trên cây chổi
(1→2→3 với hai lá tại 3), đáp án root-only là chiều sâu 3, nhưng đường
di dài nhất thật là 2 — nó bẻ gãy ở nút 3, không chạm gốc.

# Đổi gốc

Tính cho mọi đỉnh v tổng khoảng cách đến mọi đỉnh khác. Vét cạn là O(n²).
Hai lượt cho O(n):

1. **Lượt lên**: `cnt[u]` = kích thước cây con, `sd[u]` = tổng khoảng cách
   từ u đến mọi nút trong cây con: `sd[u] = Σ (sd[c] + cnt[c])`.
2. **Lượt xuống**: `ans[gốc] = sd[gốc]`; đi từ cha → con,
   `ans[c] = ans[u] + (n − cnt[c]) − cnt[c]` — mọi nút ngoài cây con của c
   xa thêm 1 (n − cnt[c] nút), mọi nút trong cây con gần bớt 1 (cnt[c] nút).

Công thức đổi gốc đáng nhớ: dịch gốc qua một cạnh thay đổi đáp án
`+ (n − cnt[c]) − cnt[c]`.
""",
    difficulty="advanced",
)

# ---------------------------------------------------------------- checkpoint
CP_M6_R = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<long long> val(n + 1, 0);
    for (int v = 1; v <= n; ++v) in >> val[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> order; order.reserve(n);
    vector<pair<int, bool>> st; st.push_back({1, false});
    while (!st.empty()) {
        auto [u, d] = st.back(); st.pop_back();
        if (d) { order.push_back(u); continue; }
        st.push_back({u, true});
        for (int c : ch[u]) st.push_back({c, false});
    }
    vector<long long> din(n + 1, 0), dout(n + 1, 0);
    for (int u : order) {
        long long take = val[u], skip = 0;
        for (int c : ch[u]) { take += dout[c]; skip += max(din[c], dout[c]); }
        din[u] = take; dout[u] = skip;
    }
    out << max(din[1], dout[1]) << "{{NL}}";
""") + END

CP_M6_W = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<long long> val(n + 1, 0);
    for (int v = 1; v <= n; ++v) in >> val[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> order; order.reserve(n);
    vector<pair<int, bool>> st; st.push_back({1, false});
    while (!st.empty()) {
        auto [u, d] = st.back(); st.pop_back();
        if (d) { order.push_back(u); continue; }
        st.push_back({u, true});
        for (int c : ch[u]) st.push_back({c, false});
    }
    vector<long long> din(n + 1, 0), dout(n + 1, 0);
    for (int u : order) {
        long long take = val[u], skip = 0;
        // WRONG: taking u still lets every child be taken — adjacency
        // conflicts ignored, so this is just "sum of all values".
        for (int c : ch[u]) { take += max(din[c], dout[c]); skip += max(din[c], dout[c]); }
        din[u] = take; dout[u] = skip;
    }
    out << max(din[1], dout[1]) << "{{NL}}";
""") + END

_cn = 200000
_cpar = _tree(_cn, "caterpillar")
_cval = [0] + [((i * 37) % 199) - 99 for i in range(1, _cn + 1)]
_cp_truth = _maxind(_cn, _cpar, _cval)

CK_TESTS = [
    contest_test("conflict on a path", T("3", "1 2", "5 5 5"), T("10"),
        "Path 1-2-3: best non-adjacent pair is 10; taking all three (15) breaks independence."),
    contest_test("negatives allow empty", T("4", "1 1 2", "-1 -2 -3 -4"), T("0"),
        "Every selection is negative — the empty set wins."),
    contest_test("n=200000 caterpillar",
        T(str(_cn)) + T(*[str(_cpar[v]) for v in range(2, _cn + 1)]) + T(*[str(_cval[v]) for v in range(1, _cn + 1)]),
        T(str(_cp_truth)),
        "200000-node caterpillar, values in [-99, 99]: ground truth via an independent post-order DP in Python. The conflict-ignoring wrong solution prints the plain value sum."),
]

write_checkpoint(
    M, "hsga-cp-m6", "Checkpoint — In/Out Tree DP",
    "Weighted independent set on a 2·10^5-node caterpillar; the conflict-ignoring DP that lets adjacent nodes both be taken is the graded wrong answer.",
    30,
    """
**Checkpoint — Tree DP.** Cây n = 200 000 đỉnh: dòng 2 là cha của
2..n, dòng 3 là giá trị val[1..n] (có thể âm). In tổng lớn nhất của tập
độc lập trọng số (tập rỗng hợp lệ). DP lấy/bỏ hậu thứ tự; bản gãy cho
phép hai đỉnh kề cùng lấy — in ra tổng mọi giá trị.
""",
    "Điểm kiểm tra — Tree DP lấy/bỏ",
    "Tập độc lập trọng số trên cây 200 000 đỉnh; DP bỏ quên xung đột kề là đáp án sai bị chấm.",
    """
**Checkpoint — Tree DP.** Cây n đỉnh (dòng 2: cha; dòng 3: giá trị).
In tổng lớn nhất của tập độc lập trọng số; tập rỗng hợp lệ.
""",
    challenge(
        "hsga-cp-m6-indep",
        "Maximum Weight Independent Set",
        """**Bài toán.** A rooted tree with n nodes (root 1; parents given for
v = 2..n), node values val[1..n] (possibly negative). Print the maximum
total value of a set of nodes with no two adjacent — the empty set is
legal.

**Constraints:** 1 ≤ n ≤ 200 000; |val[i]| ≤ 10^9; answer fits in
long long.

In/out DP in one iterative post-order pass: O(n).
""",
        CK_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Tập độc lập trọng số lớn nhất",
        """**Bài toán.** Cây gốc 1 (cha của v cho trên dòng 2..n), giá trị đỉnh
val[1..n] (có thể âm). In tổng lớn nhất của một tập đỉnh không có hai đỉnh
kề nhau — tập rỗng hợp lệ.""",
        [("xung đột trên đường thẳng", "3 đỉnh giá trị 5: chọn hai đầu (10), không lấy cả ba (15)."),
         ("toàn giá trị âm", "Tập rỗng thắng — đáp án 0."),
         ("n=200000 sâu bướm", "Giá trị trong [-99, 99]; DP hậu thứ tự O(n), DFS đệ quy sẽ tràn stack.")],
    ),
    solution=CP_M6_R,
    wrong=CP_M6_W,
)

# ------------------------------------------------------------ practice R/W
# A1: weighted diameter
A1_R = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<long long> w(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> w[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> order; order.reserve(n);
    vector<pair<int, bool>> st; st.push_back({1, false});
    while (!st.empty()) {
        auto [u, d] = st.back(); st.pop_back();
        if (d) { order.push_back(u); continue; }
        st.push_back({u, true});
        for (int c : ch[u]) st.push_back({c, false});
    }
    vector<long long> h(n + 1, 0);
    long long best = 0;
    for (int u : order) {
        long long h1 = 0, h2 = 0;
        for (int c : ch[u]) {
            long long hh = h[c] + w[c];
            if (hh > h1) { h2 = h1; h1 = hh; } else if (hh > h2) h2 = hh;
        }
        best = max(best, h1 + h2);
        h[u] = h1;
    }
    out << best << "{{NL}}";
""") + END

A1_W = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<long long> w(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> w[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> order; order.reserve(n);
    vector<pair<int, bool>> st; st.push_back({1, false});
    while (!st.empty()) {
        auto [u, d] = st.back(); st.pop_back();
        if (d) { order.push_back(u); continue; }
        st.push_back({u, true});
        for (int c : ch[u]) st.push_back({c, false});
    }
    vector<long long> h(n + 1, 0);
    // WRONG: cross term checked only at the root — misses diameters that
    // bend deeper (overestimates them with the depth, or misses entirely).
    long long h1 = 0, h2 = 0;
    for (int u : order) {
        long long a = 0, b = 0;
        for (int c : ch[u]) {
            long long hh = h[c] + w[c];
            if (hh > a) { b = a; a = hh; } else if (hh > b) b = hh;
        }
        h[u] = a;
    }
    for (int c : ch[1]) {
        long long hh = h[c] + w[c];
        if (hh > h1) { h2 = h1; h1 = hh; } else if (hh > h2) h2 = hh;
    }
    out << h1 + h2 << "{{NL}}";
""") + END

_dn = 200000
_dpar = _tree(_dn, "caterpillar")
_dw = [0] * (_dn + 1)
for _i in range(2, _dn + 1):
    _dw[_i] = ((_i * 13) % 41) + 1
_d_truth = _diameter(_dn, _dpar, _dw)

A1_TESTS = [
    contest_test("bend below the root", T("6", "1 2 2 3 4", "1 1 1 5 7"), T("14"),
        "Y-tree: path 5-3-2-4-6 (weight 14) bends at node 2; a root-only cross term reports just the deepest arm (9)."),
    contest_test("through the root", T("6", "1 1 2 2 3", "1 1 1 1 1"), T("4"),
        "Path 4-2-1-3-6 bends at the root."),
    contest_test("n=200000 weighted caterpillar",
        T(str(_dn)) + T(*[str(_dpar[v]) for v in range(2, _dn + 1)]) + T(*[str(_dw[v]) for v in range(2, _dn + 1)]),
        T(str(_d_truth)),
        "200000-node caterpillar with edge weights 1..41: ground truth via an independent post-order model."),
]

# A2: minimum vertex cover
A2_R = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> order; order.reserve(n);
    vector<pair<int, bool>> st; st.push_back({1, false});
    while (!st.empty()) {
        auto [u, d] = st.back(); st.pop_back();
        if (d) { order.push_back(u); continue; }
        st.push_back({u, true});
        for (int c : ch[u]) st.push_back({c, false});
    }
    vector<long long> cov(n + 1, 0), unc(n + 1, 0);
    for (int u : order) {
        long long s = 0, f = 0;
        for (int c : ch[u]) { s += min(cov[c], unc[c]); f += cov[c]; }
        cov[u] = 1 + s;
        unc[u] = f;
    }
    out << min(cov[1], unc[1]) << "{{NL}}";
""") + END

A2_W = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    // WRONG: "cover = every non-leaf node" — overcounts on long paths and
    // undercounts nowhere, but it is not optimal: path of 5 needs 2, this
    // prints 3.
    int cnt = 0;
    for (int v = 1; v <= n; ++v) if (!ch[v].empty()) ++cnt;
    out << cnt << "{{NL}}";
""") + END

_pn2 = 200000
_ppar2 = _tree(_pn2, "path")
_pc_truth = _mincover(_pn2, _ppar2)

A2_TESTS = [
    contest_test("path of five", T("5", "1 2 3 4"), T("2"),
        "Cover {2,4} (or {2,3}); the non-leaf heuristic prints 3."),
    contest_test("star", T("5", "1 1 1 1"), T("1"),
        "The center alone covers every edge; both approaches agree here."),
    contest_test("n=200000 path",
        T(str(_pn2)) + T(*[str(_ppar2[v]) for v in range(2, _pn2 + 1)]),
        T(str(_pc_truth)),
        "200000-node path: minimum vertex cover is 100000 alternating nodes; the heuristic prints 199998."),
]

# A3: rerooting — sum of distances from every node
A3_R = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> order; order.reserve(n);
    vector<pair<int, bool>> st; st.push_back({1, false});
    while (!st.empty()) {
        auto [u, d] = st.back(); st.pop_back();
        if (d) { order.push_back(u); continue; }
        st.push_back({u, true});
        for (int c : ch[u]) st.push_back({c, false});
    }
    vector<long long> cnt(n + 1, 0), sd(n + 1, 0), ans(n + 1, 0);
    for (int u : order) {
        cnt[u] = 1;
        long long s = 0;
        for (int c : ch[u]) { cnt[u] += cnt[c]; s += sd[c] + cnt[c]; }
        sd[u] = s;
    }
    // parents before children in BFS order from the root
    vector<int> bfs; bfs.reserve(n); bfs.push_back(1);
    for (int i = 0; i < (int)bfs.size(); ++i) {
        int u = bfs[i];
        for (int c : ch[u]) bfs.push_back(c);
    }
    ans[1] = sd[1];
    for (int i = 1; i < (int)bfs.size(); ++i) {
        int v = bfs[i];
        ans[v] = ans[par[v]] + (long long)n - 2 * cnt[v];
    }
    for (int v = 1; v <= n; ++v) out << ans[v] << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""    int n; in >> n;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> adj(n + 1);
    for (int v = 2; v <= n; ++v) { adj[v].push_back(par[v]); adj[par[v]].push_back(v); }
    // WRONG: BFS from every node — correct output, O(n^2); on n = 2·10^5
    // that is 4·10^10 edge visits and times out.
    for (int s = 1; s <= n; ++s) {
        vector<long long> dist(n + 1, -1);
        dist[s] = 0;
        vector<int> q; q.push_back(s);
        for (int i = 0; i < (int)q.size(); ++i) {
            int u = q[i];
            for (int x : adj[u]) if (dist[x] < 0) { dist[x] = dist[u] + 1; q.push_back(x); }
        }
        long long tot = 0;
        for (int v = 1; v <= n; ++v) tot += dist[v];
        out << tot << "{{NL}}";
    }
""") + END

_rn = 200000
_rpar = _tree(_rn, "path")
# closed form on a path: sum(v) = (v-1)v/2 + (n-v)(n-v+1)/2
_r_truth = [str((v - 1) * v // 2 + (_rn - v) * (_rn - v + 1) // 2) for v in range(1, _rn + 1)]

A3_TESTS = [
    contest_test("hand tree", T("6", "1 1 2 2 3"), T(*_dist_sums_bfs(6, [0, 0, 1, 1, 2, 2, 3])),
        "Six-node tree: ground truth via per-node BFS."),
    contest_test("path of five", T("5", "1 2 3 4"), T("10", "7", "6", "7", "10"),
        "Middle node 3 has the smallest total; ends have 10."),
    contest_test("n=200000 path",
        T(str(_rn)) + T(*[str(_rpar[v]) for v in range(2, _rn + 1)]),
        T(*_r_truth),
        "Every node's distance sum on a 200000-node path: closed-form ground truth. BFS-per-node costs 4·10^10 visits."),
]

VI_P6 = {
    "hsga-p6-treedp": vi_challenge(
        "Bộ ba Tree DP",
        """**Bài toán.** Ba bài: đường đi dài nhất có trọng số (số hạng qua biên
tại mọi nút); đỉnh phủ nhỏ nhất (lấy/bỏ với ràng buộc bắt buộc); tổng
khoảng cách từ mọi đỉnh (đổi gốc).""",
        [("bẻ gãy dưới gốc", "Cây chổi: đường đi dài nhất bẻ ở nút sâu, không chạm gốc."),
         ("đường năm đỉnh", "Đỉnh phủ nhỏ nhất là 2 — đếm nút không lá cho ra 3."),
         ("n=200000", "Đổi gốc O(n); BFS từng đỉnh là O(n²) — quá thời gian.")],
    ),
}

write_practice(
    M, "hsga-p6-treedp", "Tree DP Trio",
    "Diameter with the cross term, minimum vertex cover with forced states, and rerooting for all-nodes distance sums — each with a small behavioral kill and a full-size load.",
    "Bộ ba Tree DP",
    "Đường đi dài nhất với số hạng qua biên, đỉnh phủ nhỏ nhất với trạng thái bắt buộc, và đổi gốc cho tổng khoảng cách mọi đỉnh — mỗi bài có test giết nhỏ và tải đầy đủ.",
    "hsga-m6-cross",
    110,
    "advanced",
    [
        challenge("hsga-p6-diameter", "Weighted Diameter",
            """**Bài toán.** A rooted tree (root 1); parents for v = 2..n on line 2,
edge weights w[v] (edge parent(v)–v) on line 3. Print the diameter — the
maximum total weight of any path.

**Constraints:** 1 ≤ n ≤ 200 000; 1 ≤ w[v] ≤ 10^4; answer fits in
long long.

Post-order heights with the cross term h1 + h2 checked at EVERY node.
""",
            A1_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p6-mincover", "Minimum Vertex Cover",
            """**Bài toán.** A rooted tree (root 1), parents for v = 2..n. Print the
minimum number of nodes covering every edge.

**Constraints:** 1 ≤ n ≤ 200 000. In/out DP where skipping u forces all
children to be taken: O(n).
""",
            A2_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p6-reroot", "Sum of Distances from Every Node",
            """**Bài toán.** An unweighted tree (root 1), parents for v = 2..n. For
every node v (in order 1..n) print the sum of distances from v to all
other nodes.

**Constraints:** 1 ≤ n ≤ 200 000; answers fit in long long. One bottom-up
and one top-down pass: O(n).
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    VI_P6,
    solutions=[
        ("hsga-p6-diameter", A1_R, A1_W),
        ("hsga-p6-mincover", A2_R, A2_W),
        ("hsga-p6-reroot", A3_R, A3_W),
    ],
)
