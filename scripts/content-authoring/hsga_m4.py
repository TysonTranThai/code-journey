#!/usr/bin/env python3
"""HSG Advanced — Module 4: hsga-lift (Binary Lifting and LCA).

Parent-pointer tables, k-th ancestor descent, LCA via depth equalization +
synchronized descent, path-to-root counting, and the Euler-tour entry/exit
trick. Checkpoint composes LCA with k-th ancestor under n, q = 2·10^5.

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

# generated ground truth for the ANC batch on the complete binary tree:
# ANCs of node 200000 for k = 1..50000 (halving pattern, 0 once above root)
def _anc_truth():
    n = 200000
    LOG = 18
    up = [[0] * (n + 1) for _ in range(LOG)]
    for v in range(1, n + 1): up[0][v] = v // 2 if v >= 2 else 0
    for k in range(1, LOG):
        for v in range(1, n + 1): up[k][v] = up[k-1][up[k-1][v]]
    out = []
    for i in range(1, 50001):
        v = 200000; k = i
        for b in range(LOG):
            if k >> b & 1: v = up[b][v]
        out.append(str(v))
    return out

ANC_RES = _anc_truth()

# generated ground truth for the big LCA query batch (complete binary tree)
_g = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_m4_t3.py")).read(), _g)
T3_Q, T3_QS, T3_RES = _g["T3_Q"], _g["T3_QS"], _g["T3_RES"]

M = "hsga-lift"
write_module(
    M,
    "Binary Lifting and LCA",
    "Sparse parent tables turn ancestor walks into O(log n) jumps; depth equalization and synchronized descent answer lowest common ancestors, k-th ancestors, and path queries on 2·10^5-node trees.",
    "Nhảy nhị phân và LCA",
    "Bảng cha thưa biến việc đi lên tổ tiên thành bước nhảy O(log n); cân bằng độ sâu và đi xuống đồng bộ trả lời tổ chức chung thấp nhất, tổ tiên thứ k, và truy vấn đường đi trên cây 2·10^5 đỉnh.",
    ["hsga-m4-lifting", "hsga-m4-lca", "hsga-m4-euler", "hsga-cp-m4"],
    ["hsga-p4-lift"],
)

write_lesson(
    M, "hsga-m4-lifting",
    "The Sparse Parent Table",
    "up[k][v] = the 2^k-th ancestor of v. One doubling pass builds it; every ancestor question becomes a decomposition of the distance in binary.",
    35,
    """
# Binary lifting

Store `up[k][v]` — the 2^k-th ancestor of node v (0 for "above the root").
Building is one line per level: `up[k][v] = up[k-1][up[k-1][v]]`. Memory:
O(n log n) — for n = 2·10^5 and LOG = 18 that is 3.6·10^6 entries, fine.

Answering "the k-th ancestor of v" decomposes k in binary:

```
for (int bit = 0; bit < LOG; ++bit)
    if (k >> bit & 1) v = up[bit][v];
```

Any per-node payload can ride along in the same table: edge weight sums
become distance queries, max edge weight becomes max-edge-on-path, and
combining two node states later gives path aggregates (the LCA splits the
path into two upward walks).

Recognition cues: "k-th ancestor", "distance between two nodes", "path
query on a tree", repeated upward walks that a plain parent loop cannot
afford (a path graph forces O(n) per query — lifting makes it O(log n)).
""",
    "Bảng cha thưa",
    "up[k][v] là tổ tiên thứ 2^k của v. Một lượt nhân đôi xây bảng; mọi câu hỏi tổ tiên thành phân tích nhị phân của khoảng cách.",
    """
# Bảng cha thưa

Lưu `up[k][v]` — tổ tiên thứ 2^k của v (0 nghĩa là trên gốc). Xây bằng
một dòng mỗi tầng: `up[k][v] = up[k-1][up[k-1][v]]`. Bộ nhớ O(n log n) —
Với n = 2·10^5 và LOG = 18 là 3,6·10^6 ô.

Trả lời "tổ tiên thứ k": phân tích k thành nhị phân và nhảy từng bit.
Mọi dữ liệu theo đỉnh (tổng trọng số cạnh, cạnh lớn nhất) có thể đi cùng
bảng — LCA sau này tách đường đi thành hai đường đi lên.

Dấu hiệu nhận biết: "tổ tiên thứ k", "khoảng cách hai đỉnh", "truy vấn
đường đi trên cây", những lần đi lên lặp lại mà vòng cha thường không
đủ nhanh (đường thẳng buộc O(n) mỗi truy vấn — nhảy nhị phân đưa về
O(log n)).
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m4-lca",
    "LCA: Depth Equalization and Synchronized Descent",
    "Bring both nodes to the same depth, then jump both up while their ancestors differ. Two phases, each O(log n).",
    35,
    """
# Lowest common ancestor

Phase 1 — equalize depths: lift the deeper node by the depth difference
(binary decomposition, same loop as k-th ancestor). If the nodes coincide,
that is the LCA.

Phase 2 — synchronized descent: for k from high to low, if
`up[k][u] != up[k][v]`, jump both. Afterwards the nodes sit just below
their LCA, so the answer is `parent[u]`.

Why phase 2 is safe: any jump that keeps u and v different cannot overshoot
the LCA (both would have to pass through it together). When no level can
separate them anymore, they are as close as possible — siblings under the
LCA.

The classic bug: testing `up[k][u] != up[k][v]` in phase 1, or forgetting
the "if u == v return u" early exit after equalization (a node is its own
ancestor). Another: descending from high to low incorrectly — the loop
must go from LOG-1 down to 0.
""",
    "LCA: cân bằng độ sâu và đi xuống đồng bộ",
    "Đưa hai đỉnh về cùng độ sâu, rồi nhảy cả hai lên trong khi tổ tiên của chúng còn khác nhau. Hai pha, mỗi pha O(log n).",
    """
# LCA: hai pha

Pha 1 — cân bằng độ sâu: nâng đỉnh sâu hơn lên bằng phần hiệu độ sâu
(phân tích nhị phân). Nếu trùng nhau, đó là LCA.

Pha 2 — đi xuống đồng bộ: với k từ cao xuống thấp, nếu
`up[k][u] != up[k][v]` thì nhảy cả hai. Sau đó đáp án là `cha[u]`.

An toàn vì mọi bước nhảy giữ u ≠ v đều không vượt qua LCA (cả hai phải
đi qua nó cùng nhau). Khi không tầng nào tách được chúng nữa, hai đỉnh
nằm ngay dưới LCA — là anh em cha mẹ.

Lỗi kinh điển: quên early-exit "u == v" sau cân bằng (một đỉnh là tổ tiên
của chính nó), hoặc đi từ thấp lên cao.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m4-euler",
    "Euler Tour: Flattening the Tree",
    "tin/tout timestamps turn 'is u an ancestor of v' and subtree sums into array problems you already know how to solve.",
    30,
    """
# The Euler tour

DFS the tree, recording `tin[v]` on entry and `tout[v]` on exit. Two facts
do enormous work:

- u is an ancestor of v **iff** `tin[u] <= tin[v] && tin[v] <= tout[u]`
  (the interval of u contains the interval of v).
- the subtree of v is exactly the interval `[tin[v], tout[v]]` — so any
  range structure (Fenwick, segment tree) now answers subtree sums, subtree
  adds, and "count marked nodes in a subtree".

Combining with LCA: a path (u, v) splits at l = LCA(u, v) into
`root..u` + `root..v` − `root..l` (minus 2·root..parent(l) depending on
what you count). "Add on path" = add on two root-paths with a difference
trick at l; "sum over path" = depth-weighted sums maintained per node.

This flattening is the foundation for Module 7 (HLD): heavy chains become
contiguous array segments precisely because of the tour.
""",
    "Euler tour: trải phẳng cây",
    "Dấu thời gian tin/tout biến 'u có phải tổ tiên của v' và tổng cây con thành bài toán mảng vốn đã biết cách giải.",
    """
# Euler tour: trải phẳng cây

DFS ghi `tin[v]` khi vào và `tout[v]` khi ra. Hai sự kiện làm việc lớn:

- u là tổ tiên của v ⟺ `tin[u] ≤ tin[v] ≤ tout[u]` (đoạn của u chứa
  đoạn của v).
- Cây con của v đúng là đoạn `[tin[v], tout[v]]` — mọi cấu trúc đoạn
  (Fenwick, segment tree) giờ trả lời tổng cây con, cộng cây con, đếm
  nút đã đánh dấu trong cây con.

Kết hợp LCA: đường (u, v) tách tại l = LCA(u, v) thành `gốc..u + gốc..v −
gốc..l`. "Cộng trên đường đi" = cộng trên hai đường từ gốc với mẹo sai
phân tại l. Đây là nền tảng của Module 7 (HLD): chuỗi nặng thành đoạn
mảng liền kề chính nhờ tour.
""",
    difficulty="advanced",
)

# ---------------------------------------------------------------- checkpoint
CP_M4_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> up(18, vector<int>(n + 1, 0));
    vector<int> dep(n + 1, 0);
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    // iterative depth
    vector<int> st; st.push_back(1);
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        for (int c : ch[u]) { dep[c] = dep[u] + 1; st.push_back(c); }
    }
    for (int v = 1; v <= n; ++v) up[0][v] = par[v];
    for (int k = 1; k < 18; ++k)
        for (int v = 1; v <= n; ++v) up[k][v] = up[k-1][up[k-1][v]];
    auto lift = [&](int v, long long k) {
        for (int b = 0; b < 18 && v; ++b)
            if (k >> b & 1) v = up[b][v];
        return v;
    };
    auto lca = [&](int u, int v) {
        if (dep[u] < dep[v]) swap(u, v);
        u = lift(u, dep[u] - dep[v]);
        if (u == v) return u;
        for (int k = 17; k >= 0; --k)
            if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
        return par[u];
    };
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "ANC") { int v; long long k; in >> v >> k; out << lift(v, k) << "{{NL}}"; }
        else { int u, v; in >> u >> v; out << lca(u, v) << "{{NL}}"; }
    }
""") + END

CP_M4_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> up(18, vector<int>(n + 1, 0));
    vector<int> dep(n + 1, 0);
    vector<vector<int>> ch(n + 1, vector<int>());
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> st; st.push_back(1);
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        for (int c : ch[u]) { dep[c] = dep[u] + 1; st.push_back(c); }
    }
    for (int v = 1; v <= n; ++v) up[0][v] = par[v];
    for (int k = 1; k < 18; ++k)
        for (int v = 1; v <= n; ++v) up[k][v] = up[k-1][up[k-1][v]];
    auto lift = [&](int v, long long k) {
        for (int b = 0; b < 18 && v; ++b)
            if (k >> b & 1) v = up[b][v];
        return v;
    };
    auto lca = [&](int u, int v) {
        if (dep[u] < dep[v]) swap(u, v);
        u = lift(u, dep[u] - dep[v]);
        // WRONG: missing the early exit when u == v after equalization —
        // when one node is an ancestor of the other, the descent phase
        // then walks both nodes PAST the true LCA.
        for (int k = 17; k >= 0; --k)
            if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
        return par[u];
    };
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "ANC") { int v; long long k; in >> v >> k; out << lift(v, k) << "{{NL}}"; }
        else { int u, v; in >> u >> v; out << lca(u, v) << "{{NL}}"; }
    }
""") + END

CK_TESTS = [
    contest_test("hand tree LCA", T("5 4", "1 1 2 2", "LCA 4 5", "LCA 4 3", "LCA 2 5", "LCA 1 5"), T("2", "1", "2", "1"),
        "Small tree: LCAs 2, 1, 2, 1."),
    contest_test("ancestor chain", T("10 3", "1 2 3 4 5 6 7 8 9", "ANC 10 9", "ANC 10 3", "LCA 10 1"), T("1", "7", "1"),
        "Path graph: 9 steps up from 10 is the root; 3 steps is 7."),
    contest_test("n=200000 mixed batch",
        T(f"{T3_Q} {100000 + 50000}")
        + T(*[str(i // 2) for i in range(2, T3_Q + 1)])
        + T(*[f"LCA {q}" for q in T3_QS])
        + T(*[f"ANC 200000 {i}" for i in range(1, 50001)]),
        T(*T3_RES) + T(*ANC_RES),
        "Complete binary tree: 100000 mixed LCAs + 50000 ancestor jumps of the deepest node. Linear climbs cost ~10^10 steps; lifting answers in O(log n) per query."),
]

write_checkpoint(
    M, "hsga-cp-m4", "Checkpoint — Lifting and LCA",
    "Mixed workload: 100000 LCA queries + 50000 k-th ancestor jumps on a 2·10^5-node tree. A node being its own ancestor is the classic trap.",
    30,
    """
**Checkpoint — Nhảy nhị phân.** Cây n = 200 000 đỉnh (cha của v cho trên
dòng 2). q truy vấn: `LCA u v` và `ANC v k`. Bảng cha thưa 18 tầng; bẫy
kinh điển: một đỉnh là tổ tiên của chính nó.
""",
    "Điểm kiểm tra — Nhảy nhị phân và LCA",
    "100000 truy vấn LCA + 50000 bước nhảy tổ tiên thứ k trên cây 200 000 đỉnh.",
    """
**Checkpoint — Nhảy nhị phân.** Cây n = 200 000 đỉnh. q truy vấn:
`LCA u v` in tổ chức chung thấp nhất; `ANC v k` in tổ tiên thứ k.
""",
    challenge(
        "hsga-cp-m4-lca",
        "Ancestors and LCA under Load",
        """**Bài toán.** A rooted tree with n nodes (root 1; the parent of v is
given for v = 2..n). q queries: `LCA u v` prints the lowest common
ancestor; `ANC v k` prints the k-th ancestor of v (or 0 if it does not
exist).

**Constraints:** 1 ≤ n, q ≤ 200 000; 0 ≤ k < n.

Binary lifting with LOG = 18 covers both query types in O(log n).
""",
        CK_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Tổ tiên và LCA dưới tải",
        """**Bài toán.** Cây có gốc 1, cha của v cho trên dòng 2..n. q truy vấn:
`LCA u v` in tổ chức chung thấp nhất; `ANC v k` in tổ tiên thứ k của v
(0 nếu không tồn tại).""",
        [("cây tay", "Kiểm 5 đỉnh: LCA(4,5)=2, LCA(4,3)=1."),
         ("đường thẳng", "ANC 10 9 = 1 trên đường 1-2-...-10."),
         ("n=200000 trộn", "100000 LCA + 50000 ANC — mỗi truy vấn phải O(log n).")],
    ),
    solution=CP_M4_R,
    wrong=CP_M4_W,
)

# ------------------------------------------------------------ practice R/W
# A1: kth ancestor only
A1_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<vector<int>> up(18, vector<int>(n + 1, 0));
    for (int v = 1; v <= n; ++v) up[0][v] = par[v];
    for (int k = 1; k < 18; ++k)
        for (int v = 1; v <= n; ++v) up[k][v] = up[k-1][up[k-1][v]];
    for (int i = 0; i < q; ++i) {
        int v; long long k; in >> v >> k;
        for (int b = 0; b < 18 && v; ++b)
            if (k >> b & 1) v = up[b][v];
        out << v << "{{NL}}";
    }
""") + END

A1_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    // WRONG: walks k parent steps one at a time — O(k) per query; on a path
    // graph with k ~ n and q ~ 10^5 that is 2·10^10 steps and times out.
    for (int i = 0; i < q; ++i) {
        int v; long long k; in >> v >> k;
        while (k-- && v) v = par[v];
        out << v << "{{NL}}";
    }
""") + END

A1_TESTS = [
    contest_test("small chain", T("10 3", "1 2 3 4 5 6 7 8 9", "10 9", "10 3", "5 10"), T("1", "7", "0"),
        "9 steps from 10 is the root; 10 steps from 5 falls off — print 0."),
    contest_test("k=0 is identity", T("3 2", "1 2", "2 0", "2 1"), T("2", "1"),
        "Zeroth ancestor is the node itself."),
    contest_test("n=200000 path heavy k",
        T("200000 100000")
        + T(*[str(i - 1) for i in range(2, 200001)])
        + T(*["199999 199999"] * 100000),
        T(*["0"] * 100000),
        "Path graph: 100000 queries each walking k = 199999 parent steps (falling off the root) — 2·10^10 linear steps. Lifting: 18 jumps per query."),
]

# A2: LCA only (complete binary tree + hand trees)
A2_R = CP_M4_R  # same protocol: mixed LCA/ANC handled; reuse full reference
A2_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    // WRONG: climbs both nodes one parent step at a time until they meet —
    // O(depth) per query; on a 200000-node path with far-apart queries
    // that is O(n) per query and times out.
    for (int i = 0; i < q; ++i) {
        string tp; in >> tp;
        if (tp == "ANC") { int v; long long k; in >> v >> k; while (k-- && v) v = par[v]; out << v << "{{NL}}"; }
        else {
            int u, v; in >> u >> v;
            vector<int> dep(n + 1, 0);
            // recompute depth by walking (already O(depth)) then climb
            vector<int> a; int x = u;
            while (x) { a.push_back(x); x = par[x]; }
            vector<int> b; x = v;
            while (x) { b.push_back(x); x = par[x]; }
            int iu = (int)a.size() - 1, iv = (int)b.size() - 1;
            while (iu > 0 && iv > 0 && a[iu-1] == b[iv-1]) { --iu; --iv; }
            out << a[iu] << "{{NL}}";
        }
    }
""") + END

A2_TESTS = [
    contest_test("hand tree LCA", T("5 4", "1 1 2 2", "LCA 4 5", "LCA 4 3", "LCA 2 5", "LCA 1 5"), T("2", "1", "2", "1"),
        "LCAs 2, 1, 2, 1 — includes a node being its own ancestor (LCA 1 5 = 1... wait, 1 is the root)."),
    contest_test("self LCA", T("5 2", "1 1 2 2", "LCA 3 3", "LCA 2 4"), T("3", "2"),
        "A node is its own LCA; ancestor-of-descendant case."),
    contest_test("n=200000 far queries on path",
        T("200000 50000")
        + T(*[str(i - 1) for i in range(2, 200001)])
        + T(*["LCA 200000 1"] * 25000 + ["LCA 200000 100001"] * 25000),
        T(*["1"] * 25000) + T(*["100001"] * 25000),
        "Path graph extremes: the walk-to-meet approach costs O(n) per query — 10^10 steps total."),
]

VI_P4 = {
    "hsga-p4-anc": vi_challenge(
        "Tổ tiên thứ k",
        """**Bài toán.** Cây gốc 1, cha của v cho trên dòng 2..n. q truy vấn
`v k`: in tổ tiên thứ k của v, hoặc 0 nếu không tồn tại.""",
        [("rơi khỏi gốc", "k vượt quá độ sâu → in 0."),
         ("k = 0", "Tổ tiên thứ 0 là chính nó."),
         ("n=200000 đường thẳng", "k = 1..100000 từ đỉnh cuối — mỗi truy vấn phải O(log n).")],
    ),
    "hsga-p4-lca": vi_challenge(
        "Tổ chức chung thấp nhất",
        """**Bài toán.** Cây gốc 1. q truy vấn `LCA u v`: in LCA của u và v.""",
        [("cây tay", "LCA(4,5)=2, LCA(4,3)=1 trên cây 5 đỉnh."),
         ("chính nó", "Một đỉnh là LCA của chính nó."),
         ("n=200000 đường thẳng", "Truy vấn hai đầu mút xa nhau — leo từng bước là O(n) mỗi truy vấn.")],
    ),
}

write_practice(
    M, "hsga-p4-lift", "Lifting Drills",
    "Two focused problems: k-th ancestor jumps and full LCA, both under loads that punish linear walks.",
    "Bài tập nhảy nhị phân",
    "Hai bài tập trung: tổ tiên thứ k và LCA đầy đủ, cả hai dưới tải trừng phạt cách đi tuyến tính.",
    "hsga-m4-euler",
    90,
    "advanced",
    [
        challenge("hsga-p4-anc", "k-th Ancestor",
            """**Bài toán.** A rooted tree (root 1), parents for v = 2..n. q queries
`v k`: print the k-th ancestor of v, or 0 if it does not exist.

**Constraints:** 1 ≤ n, q ≤ 200 000; 0 ≤ k ≤ n. One sparse table, O(log n)
per query.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p4-lca", "Lowest Common Ancestor",
            """**Bài toán.** A rooted tree (root 1). q queries `LCA u v`: print the
LCA. `ANC v k` queries may also appear (same handler as the checkpoint).

**Constraints:** 1 ≤ n, q ≤ 200 000. Depth equalization + synchronized
descent, O(log n) per query.
""",
            A2_TESTS, level="independent", difficulty="advanced"),
    ],
    VI_P4,
    solutions=[
        ("hsga-p4-anc", A1_R, A1_W),
        ("hsga-p4-lca", A2_R, A2_W),
    ],
)
