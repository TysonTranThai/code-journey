#!/usr/bin/env python3
"""HSG Advanced — Module 7: hsga-hld (Heavy-Light Decomposition).

Flagship composition: HLD chains + the M2 lazy trees over positions.
A1 path add/max, A2 path assign/max, A3 path add/sum with a bamboo load
test whose wrong solution is the honest per-op path climb (timeout).
Checkpoint: mixed add/assign/max with the classic final-segment W.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes.
"""
import sys, os, random
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
#include <functional>
#include <climits>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-hld"


# ---------------------------------------------------------------- models
def _bintree_par(n):
    par = [0] * (n + 1)
    for v in range(2, n + 1):
        par[v] = v // 2
    return par


def _bamboo_par(n):
    par = [0] * (n + 1)
    for v in range(2, n + 1):
        par[v] = v - 1
    return par


def _path_of(par, u, v):
    au = []
    z = u
    while z:
        au.append(z)
        z = par[z]
    av = []
    z = v
    while z:
        av.append(z)
        z = par[z]
    common = set(au)
    L = None
    for z in av:
        if z in common:
            L = z
            break
    path = []
    for z in au:
        if z == L:
            break
        path.append(z)
    for z in av:
        if z == L:
            break
        path.append(z)
    path.append(L)
    return path


def _model_add_max_assign(n, par, val, ops):
    """ops: ('add',u,v,x) | ('asg',u,v,x) | ('max',u,v) -> list of str answers."""
    val = val[:]
    want = []
    for op in ops:
        if op[0] == "max":
            _, u, v = op
            want.append(str(max(val[z] for z in _path_of(par, u, v))))
        else:
            _, u, v, x = op
            for z in _path_of(par, u, v):
                if op[0] == "add":
                    val[z] += x
                else:
                    val[z] = x
    return want


def _model_suffix_sum(n, ops):
    """Bamboo 1-2-..-n, initial value 1 per vertex. Protocol of A3:
    ("add", u, x) adds x on the path u..n (a suffix in i-space);
    ("sum", u) prints the sum over u..n.
    Reversed index r = n+1-i turns suffix ops into PREFIX ops over r:
    suffix add u..n == prefix add over r in [1 .. n+1-u]; suffix sum == the
    same prefix sum. Two-BIT trick (difference d and j*d) does prefix-add /
    prefix-sum in O(log n). Brute-verified on the n=4 case ([6, 7]).
    """
    fen1 = [0] * (n + 2)  # d[j]
    fen2 = [0] * (n + 2)  # j*d[j]

    def upd(fen, i, d):
        while i <= n + 1:
            fen[i] += d
            i += i & (-i)

    def qry(fen, i):
        s = 0
        while i >= 1:
            s += fen[i]
            i -= i & (-i)
        return s

    def prefix_add(r0, x):
        upd(fen1, 1, x)
        upd(fen2, 1, x)
        if r0 + 1 <= n + 1:
            upd(fen1, r0 + 1, -x)
            upd(fen2, r0 + 1, -(r0 + 1) * x)

    def prefix_sum(r0):
        return (r0 + 1) * qry(fen1, r0) - qry(fen2, r0)

    want = []
    for op in ops:
        if op[0] == "add":
            prefix_add(n + 1 - op[1], op[2])
        else:
            r0 = n + 1 - op[1]
            want.append(str(r0 + prefix_sum(r0)))  # r0 baseline ones
    return want


# ---------------------------------------------------------------- lessons
write_module(
    M,
    "Heavy-Light Decomposition",
    "Split a tree into chains so every root path is O(log n) segments; run the M2 lazy trees over chain positions to answer path updates and path aggregates in O(log^2 n).",
    "Phân rã nặng-nhẹ",
    "Chia cây thành chuỗi để mỗi đường đi lên gốc chỉ còn O(log n) đoạn; chạy cây lazy của M2 trên vị trí chuỗi để trả lời cập nhật và truy vấn đường đi trong O(log^2 n).",
    ["hsga-m7-size", "hsga-m7-decompose", "hsga-m7-vs", "hsga-cp-m7"],
    ["hsga-p7-hld"],
)

write_lesson(
    M, "hsga-m7-size",
    "Sizing the Chains",
    "Subtree sizes pick the heavy child; every other edge is light. A path crosses at most log2(n) light edges — that bound is the whole complexity proof.",
    35,
    """
# Heavy and light

Root the tree. For each node u, the child with the largest subtree is
the **heavy child**; every other child edge is **light**.

Why it works: whenever a path moves across a light edge, the subtree
size at least doubles. So a root path crosses at most log2(n) light
edges, and any u..v path decomposes into at most 2·log2(n) contiguous
vertical segments. That single bound is the entire HLD complexity proof —
no amortization, no potential function.

One iterative DFS computes everything HLD needs later:

```
sz[u] = 1 + sum(sz[c]);  hv[u] = argmax child
```

Store `hv[u] = 0` for leaves. The DFS must be iterative: a bamboo of
2·10^5 nodes overflows the 8 MB sandbox stack with plain recursion.
""",
    "Đo đạc chuỗi",
    "Kích thước cây con chọn con nặng; mọi cạnh khác là nhẹ. Một đường đi vượt tối đa log2(n) cạnh nhẹ — chặn đó là toàn bộ chứng minh độ phức tạp.",
    """
# Nặng và nhẹ

Gốc cây. Với mỗi nút u, con có cây con lớn nhất là **con nặng**; mọi
cạnh con khác là **nhẹ**.

Vì sao đúng: mỗi lần đường đi bước qua một cạnh nhẹ, kích thước cây con
ít nhất gấp đôi. Vậy đường đi lên gốc vượt tối đa log2(n) cạnh nhẹ, và
mỗi đường u..v phân rã thành tối đa 2·log2(n) đoạn dọc liền kề. Chặn đó
là toàn bộ chứng minh độ phức tạp của HLD — không amortize, không hàm
tiềm năng.

Một DFS lặp tính mọi thứ HLD cần về sau:

```
sz[u] = 1 + sum(sz[c]);  hv[u] = con.argmax
```

Lá có `hv[u] = 0`. DFS phải lặp: cây dạng đường 2·10^5 đỉnh làm tràn
stack 8 MB của sandbox nếu đệ quy thuần.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m7-decompose",
    "Positions, Heads, and the Walk",
    "A heavy-first preorder makes each chain one contiguous range; the query loop lifts the deeper chain head, then finishes with one same-chain segment.",
    35,
    """
# The decomposition walk

Second DFS, preorder, heavy child first:

```
pos[u]  = cnt++;                          // entry order
head[u] = (hv[par[u]] == u) ? head[par[u]] : u;
```

Heavy-first entry order makes every chain a contiguous range of
positions — a chain [1,2,4] gets pos 0,1,2 on the hand tree. The segment
tree is built over POSITIONS: `a[pos[v]] = val[v]`.

The path query loop:

```
while (head[u] != head[v]) {                if (dep[head[u]] < dep[head[v]]) swap(u, v);
    apply(pos[head[u]], pos[u]);          // whole chain head..u
    u = par[head[u]];                     // jump above the chain
}
if (pos[u] > pos[v]) swap(u, v);
apply(pos[u], pos[v]);                    // final same-chain segment
```

Lift the DEEPER HEAD (not the deeper node — `sz[head[·]]` compares chain
tops). Two classic real bugs: forgetting the final same-chain segment
(entirely, or its swap), and indexing the tree by vertex id instead of
`pos`. Both pass the tiny sample, both die on any real test.
""",
    "Vị trí, đầu chuỗi, và vòng đi",
    "Preorder vào con nặng trước biến mỗi chuỗi thành một đoạn liền; vòng truy vấn nâng đầu chuỗi sâu hơn rồi kết thúc bằng một đoạn cùng chuỗi.",
    """
# Vòng phân rã

DFS thứ hai, preorder, con nặng trước:

```
pos[u]  = cnt++;                          // thứ tự vào
head[u] = (hv[par[u]] == u) ? head[par[u]] : u;
```

Thứ tự vào nặng-trước biến mỗi chuỗi thành một đoạn vị trí liền kề —
chuỗi [1,2,4] nhận pos 0,1,2 trên cây tay. Cây đoạn dựng trên VỊ TRÍ:
`a[pos[v]] = val[v]`.

Vòng truy vấn đường đi:

```
while (head[u] != head[v]) {                if (dep[head[u]] < dep[head[v]]) swap(u, v);
    apply(pos[head[u]], pos[u]);          // cả đoạn đầu chuỗi..u
    u = par[head[u]];                     // nhảy lên trên chuỗi
}
if (pos[u] > pos[v]) swap(u, v);
apply(pos[u], pos[v]);                    // đoạn cuối cùng chuỗi
```

Nâng ĐẦU chuỗi sâu hơn (không phải nút sâu hơn — `sz[head[·]]` so đầu
chuỗi). Hai lỗi thật kinh điển: quên đoạn cuối cùng chuỗi (hoặc quên
swap của nó), và đánh chỉ số cây theo id đỉnh thay vì `pos`. Cả hai đều
qua mẫu nhỏ và chết trên test thật.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m7-vs",
    "HLD vs the Cheaper Structure",
    "Subtree queries need only an Euler tour; commutative path sums fit binary lifting; HLD earns its 150 lines only when path aggregates meet path updates.",
    35,
    """
# Paying for HLD only when needed

Decision ladder, cheapest first:

1. **Subtree** add/count → Euler tour + BIT (M5). No chains.
2. **Path u..v, point updates, distance-sum style** → binary lifting +
   rerooting bookkeeping (M4/M6).
3. **Path u..v aggregates (max/sum) WITH path or range updates** → HLD +
   lazy segment tree (M2). The only structure in the course that answers
   path-max under path-add for n, q ≤ 2·10^5.

HLD costs ~150 lines and buys O((n+q)·log² n). The log² is real: each
op touches ≤ 2·log2(n) chain segments, each a tree op. On the sandbox's
20 s job budget that is comfortable — the danger is the naive per-op
path climb, O(depth) per query, which dies exactly like A3's wrong
solution below.
""",
    "HLD so với cấu trúc rẻ hơn",
    "Truy vấn cây con chỉ cần Euler tour; tổng đường đi giao hoán vừa binary lifting; HLD chỉ đáng 150 dòng khi tổng kết đường đi gặp cập nhật đường đi.",
    """
# Chỉ trả tiền HLD khi cần

Thang quyết định, rẻ trước:

1. **Cây con** add/đếm → Euler tour + BIT (M5). Không cần chuỗi.
2. **Đường u..v, cập nhật điểm, dạng tổng khoảng cách** → binary lifting
   + sổ đổi gốc (M4/M6).
3. **Tổng kết đường u..v (max/sum) CÓ cập nhật đường/đoạn** → HLD + cây
   đoạn lazy (M2). Cấu trúc duy nhất trong khóa trả lời path-max dưới
   path-add với n, q ≤ 2·10^5.

HLD tốn ~150 dòng và mua O((n+q)·log² n). Cái log² là thật: mỗi phép
chạm ≤ 2·log2(n) đoạn chuỗi, mỗi đoạn một phép cây. Trong ngân sách
20 s/job của sandbox thì dư dả — cái nguy hiểm là leo đường đi từng
phép, O(depth)/truy vấn, chết đúng như bản sai của A3 bên dưới.
""",
    difficulty="advanced",
)

# ------------------------------------------------------------ practice R/W
# shared HLD prelude: read tree, sizes/heavy, heads/positions (1-based pos)
_HLD_PRE = """
    int n; in >> n;
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    for (int v = 2; v <= n; ++v) dep[v] = dep[par[v]] + 1;
    vector<long long> val(n + 1, 0);
    for (int v = 1; v <= n; ++v) in >> val[v];
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) ch[par[v]].push_back(v);
    vector<int> sz(n + 1, 1), hv(n + 1, 0), head(n + 1, 0), pos(n + 1, 0);
    {
        vector<int> order; order.reserve(n);
        vector<pair<int, bool>> st; st.push_back({1, false});
        while (!st.empty()) {
            auto [u, d] = st.back(); st.pop_back();
            if (d) { order.push_back(u); continue; }
            st.push_back({u, true});
            for (int c : ch[u]) st.push_back({c, false});
        }
        for (int u : order) {
            int big = 0, bc = 0;
            for (int c : ch[u]) { sz[u] += sz[c]; if (sz[c] > big) { big = sz[c]; bc = c; } }
            hv[u] = bc;
        }
        int cnt = 1;
        vector<pair<int, bool>> st2; st2.push_back({1, false});
        while (!st2.empty()) {
            auto [u, d] = st2.back(); st2.pop_back();
            if (d) continue;
            pos[u] = cnt++;
            head[u] = (u == 1 || hv[par[u]] != u) ? u : head[par[u]];
            for (int c : ch[u]) if (c != hv[u]) st2.push_back({c, false});
            if (hv[u]) st2.push_back({hv[u], false});
        }
    }
"""

# A1 R: lazy range-add / range-max tree over positions + the HLD walk
A1_R = CPP_STD + _HLD_PRE + cpp("""
    vector<long long> a(n + 1, 0);
    for (int v = 1; v <= n; ++v) a[pos[v]] = val[v];
    vector<long long> t(4 * n), lz(4 * n, 0); vector<int> ln(4 * n);
    function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { t[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<void(int, int, int, int, int, long long)> upd =
        [&](int nd, int l, int r, int ql, int qr, long long x) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { t[nd] += x; lz[nd] += x; return; }
        if (lz[nd]) {
            for (int c = 2 * nd; c <= 2 * nd + 1; ++c) { t[c] += lz[nd]; lz[c] += lz[nd]; }
            lz[nd] = 0;
        }
        int m = (l + r) / 2;
        upd(2 * nd, l, m, ql, qr, x); upd(2 * nd + 1, m + 1, r, ql, qr, x);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<long long(int, int, int, int, int)> qry =
        [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MIN;
        if (ql <= l && r <= qr) return t[nd];
        if (lz[nd]) {
            for (int c = 2 * nd; c <= 2 * nd + 1; ++c) { t[c] += lz[nd]; lz[c] += lz[nd]; }
            lz[nd] = 0;
        }
        int m = (l + r) / 2;
        return max(qry(2 * nd, l, m, ql, qr), qry(2 * nd + 1, m + 1, r, ql, qr));
    };
    build(1, 1, n);
    int q; in >> q;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) {
            int u, v; long long x; in >> u >> v >> x;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                upd(1, 1, n, pos[head[u]], pos[u], x);
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            upd(1, 1, n, pos[u], pos[v], x);
        } else {
            int u, v; in >> u >> v;
            long long r = LLONG_MIN;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                r = max(r, qry(1, 1, n, pos[head[u]], pos[u]));
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            r = max(r, qry(1, 1, n, pos[u], pos[v]));
            out << r << "{{NL}}";
        }
    }
""") + END

# A1 W: walk lifts heads but the final same-chain segment assumes
# pos[u] <= pos[v] and drops the deeper endpoint — silent wrong answers.
A1_W = CPP_STD + _HLD_PRE + cpp("""
    vector<long long> a(n + 1, 0);
    for (int v = 1; v <= n; ++v) a[pos[v]] = val[v];
    vector<long long> t(4 * n), lz(4 * n, 0); vector<int> ln(4 * n);
    function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { t[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<void(int, int, int, int, int, long long)> upd =
        [&](int nd, int l, int r, int ql, int qr, long long x) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { t[nd] += x; lz[nd] += x; return; }
        if (lz[nd]) {
            for (int c = 2 * nd; c <= 2 * nd + 1; ++c) { t[c] += lz[nd]; lz[c] += lz[nd]; }
            lz[nd] = 0;
        }
        int m = (l + r) / 2;
        upd(2 * nd, l, m, ql, qr, x); upd(2 * nd + 1, m + 1, r, ql, qr, x);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<long long(int, int, int, int, int)> qry =
        [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MIN;
        if (ql <= l && r <= qr) return t[nd];
        if (lz[nd]) {
            for (int c = 2 * nd; c <= 2 * nd + 1; ++c) { t[c] += lz[nd]; lz[c] += lz[nd]; }
            lz[nd] = 0;
        }
        int m = (l + r) / 2;
        return max(qry(2 * nd, l, m, ql, qr), qry(2 * nd + 1, m + 1, r, ql, qr));
    };
    build(1, 1, n);
    int q; in >> q;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) {
            int u, v; long long x; in >> u >> v >> x;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                upd(1, 1, n, pos[head[u]], pos[u], x);
                u = par[head[u]];
            }
            upd(1, 1, n, pos[u], pos[v] - 1, x);   // BUG: no swap, drops endpoint
        } else {
            int u, v; in >> u >> v;
            long long r = LLONG_MIN;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                r = max(r, qry(1, 1, n, pos[head[u]], pos[u]));
                u = par[head[u]];
            }
            r = max(r, qry(1, 1, n, pos[u], pos[v] - 1));   // BUG: same here
            out << r << "{{NL}}";
        }
    }
""") + END

# A2 R now shares the three-tag tree (_R_THREETAG) — add/assign/max protocol.
# A2 W: assign tag that never clears a pending add — the M2 classic,
# fatal exactly when an add precedes an assign on an overlapping segment.
A2_W = CPP_STD + _HLD_PRE + cpp("""
    vector<long long> a(n + 1, 0);
    for (int v = 1; v <= n; ++v) a[pos[v]] = val[v];
    vector<long long> t(4 * n), asg(4 * n, 0), ad(4 * n, 0);
    vector<char> mk(4 * n, 0); vector<int> ln(4 * n);
    function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { t[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<void(int, long long)> applyA = [&](int nd, long long v) { t[nd] = v; asg[nd] = v; mk[nd] = 1; };
    function<void(int, long long)> applyD = [&](int nd, long long v) { t[nd] += v; if (mk[nd]) asg[nd] += v; else ad[nd] += v; };
    function<void(int)> push = [&](int nd) {
        if (mk[nd]) { applyA(2 * nd, asg[nd]); applyA(2 * nd + 1, asg[nd]); mk[nd] = 0; }   // BUG: ad not cleared
        if (ad[nd]) { applyD(2 * nd, ad[nd]); applyD(2 * nd + 1, ad[nd]); ad[nd] = 0; }
    };
    function<void(int, int, int, int, int, int, long long)> upd =
        [&](int nd, int l, int r, int tp, int ql, int qr, long long x) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { if (tp == 3) applyA(nd, x); else applyD(nd, x); return; }
        push(nd); int m = (l + r) / 2;
        upd(2 * nd, l, m, tp, ql, qr, x); upd(2 * nd + 1, m + 1, r, tp, ql, qr, x);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<long long(int, int, int, int, int)> qry =
        [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MIN;
        if (ql <= l && r <= qr) return t[nd];
        push(nd); int m = (l + r) / 2;
        return max(qry(2 * nd, l, m, ql, qr), qry(2 * nd + 1, m + 1, r, ql, qr));
    };
    build(1, 1, n);
    int q; in >> q;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1 || tp == 3) {
            int u, v; long long x; in >> u >> v >> x;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                upd(1, 1, n, tp, pos[head[u]], pos[u], x);
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            upd(1, 1, n, tp, pos[u], pos[v], x);
        } else {
            int u, v; in >> u >> v;
            long long r = LLONG_MIN;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                r = max(r, qry(1, 1, n, pos[head[u]], pos[u]));
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            r = max(r, qry(1, 1, n, pos[u], pos[v]));
            out << r << "{{NL}}";
        }
    }
""") + END

# A3 R: lazy range-add / range-SUM tree + HLD walk
A3_R = CPP_STD + _HLD_PRE + cpp("""
    vector<long long> a(n + 1, 0);
    for (int v = 1; v <= n; ++v) a[pos[v]] = val[v];
    vector<long long> t(4 * n), lz(4 * n, 0); vector<int> ln(4 * n);
    function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { t[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        t[nd] = t[2 * nd] + t[2 * nd + 1];
    };
    function<void(int, int, int, int, int, long long)> upd =
        [&](int nd, int l, int r, int ql, int qr, long long x) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { t[nd] += x * ln[nd]; lz[nd] += x; return; }
        if (lz[nd]) {
            for (int c = 2 * nd; c <= 2 * nd + 1; ++c) { t[c] += lz[nd] * ln[c]; lz[c] += lz[nd]; }
            lz[nd] = 0;
        }
        int m = (l + r) / 2;
        upd(2 * nd, l, m, ql, qr, x); upd(2 * nd + 1, m + 1, r, ql, qr, x);
        t[nd] = t[2 * nd] + t[2 * nd + 1];
    };
    function<long long(int, int, int, int, int)> qry =
        [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return t[nd];
        if (lz[nd]) {
            for (int c = 2 * nd; c <= 2 * nd + 1; ++c) { t[c] += lz[nd] * ln[c]; lz[c] += lz[nd]; }
            lz[nd] = 0;
        }
        int m = (l + r) / 2;
        return qry(2 * nd, l, m, ql, qr) + qry(2 * nd + 1, m + 1, r, ql, qr);
    };
    build(1, 1, n);
    int q; in >> q;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) {
            int u, v; long long x; in >> u >> v >> x;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                upd(1, 1, n, pos[head[u]], pos[u], x);
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            upd(1, 1, n, pos[u], pos[v], x);
        } else {
            int u, v; in >> u >> v;
            long long r = 0;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                r += qry(1, 1, n, pos[head[u]], pos[u]);
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            r += qry(1, 1, n, pos[u], pos[v]);
            out << r << "{{NL}}";
        }
    }
""") + END

# A3 W (intentional near-miss): no HLD at all — per-op parent climb.
# O(depth) per op; on the bamboo load test (2·10^5 full-suffix ops over
# n = 2·10^5) that is ~4·10^10 steps: TIMEOUT.
A3_W = CPP_STD + cpp("""
    int n; in >> n;
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    vector<long long> val(n + 1, 0);
    for (int v = 1; v <= n; ++v) in >> val[v];
    for (int v = 2; v <= n; ++v) dep[v] = dep[par[v]] + 1;
    int q; in >> q;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) {
            int u, v; long long x; in >> u >> v >> x;
            while (u != v) {
                if (dep[u] < dep[v]) swap(u, v);
                val[u] += x; u = par[u];
            }
            val[u] += x;
        } else {
            int u, v; in >> u >> v;
            long long r = 0;
            while (u != v) {
                if (dep[u] < dep[v]) swap(u, v);
                r += val[u]; u = par[u];
            }
            r += val[u];
            out << r << "{{NL}}";
        }
    }
""") + END

# CP R: three-tag (assign/add) max tree — M2's exact composition — on HLD.
_R_THREETAG = CPP_STD + _HLD_PRE + cpp("""
    vector<long long> a(n + 1, 0);
    for (int v = 1; v <= n; ++v) a[pos[v]] = val[v];
    vector<long long> t(4 * n), asg(4 * n, 0), ad(4 * n, 0);
    vector<char> mk(4 * n, 0); vector<int> ln(4 * n);
    function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { t[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<void(int, long long)> applyA = [&](int nd, long long v) { t[nd] = v; asg[nd] = v; mk[nd] = 1; ad[nd] = 0; };
    function<void(int, long long)> applyD = [&](int nd, long long v) { t[nd] += v; if (mk[nd]) asg[nd] += v; else ad[nd] += v; };
    function<void(int)> push = [&](int nd) {
        if (mk[nd]) { applyA(2 * nd, asg[nd]); applyA(2 * nd + 1, asg[nd]); mk[nd] = 0; }
        if (ad[nd]) { applyD(2 * nd, ad[nd]); applyD(2 * nd + 1, ad[nd]); ad[nd] = 0; }
    };
    function<void(int, int, int, int, int, int, long long)> upd =
        [&](int nd, int l, int r, int tp, int ql, int qr, long long x) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { if (tp == 3) applyA(nd, x); else applyD(nd, x); return; }
        push(nd); int m = (l + r) / 2;
        upd(2 * nd, l, m, tp, ql, qr, x); upd(2 * nd + 1, m + 1, r, tp, ql, qr, x);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<long long(int, int, int, int, int)> qry =
        [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MIN;
        if (ql <= l && r <= qr) return t[nd];
        push(nd); int m = (l + r) / 2;
        return max(qry(2 * nd, l, m, ql, qr), qry(2 * nd + 1, m + 1, r, ql, qr));
    };
    build(1, 1, n);
    int q; in >> q;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1 || tp == 3) {
            int u, v; long long x; in >> u >> v >> x;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                upd(1, 1, n, tp, pos[head[u]], pos[u], x);
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            upd(1, 1, n, tp, pos[u], pos[v], x);
        } else {
            int u, v; in >> u >> v;
            long long r = LLONG_MIN;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                r = max(r, qry(1, 1, n, pos[head[u]], pos[u]));
                u = par[head[u]];
            }
            if (pos[u] > pos[v]) swap(u, v);
            r = max(r, qry(1, 1, n, pos[u], pos[v]));
            out << r << "{{NL}}";
        }
    }
""") + END

A2_R = _R_THREETAG
CP_M7_R = _R_THREETAG


# CP W: the mixed-op tree is right; the walk's final same-chain segment
# assumes pos[u] <= pos[v] and drops an endpoint — wrong answers whenever
# a query's last segment runs "upward".
CP_M7_W = CPP_STD + _HLD_PRE + cpp("""
    vector<long long> a(n + 1, 0);
    for (int v = 1; v <= n; ++v) a[pos[v]] = val[v];
    vector<long long> t(4 * n), asg(4 * n, 0), ad(4 * n, 0);
    vector<char> mk(4 * n, 0); vector<int> ln(4 * n);
    function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { t[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<void(int, long long)> applyA = [&](int nd, long long v) { t[nd] = v; asg[nd] = v; mk[nd] = 1; ad[nd] = 0; };
    function<void(int, long long)> applyD = [&](int nd, long long v) { t[nd] += v; if (mk[nd]) asg[nd] += v; else ad[nd] += v; };
    function<void(int)> push = [&](int nd) {
        if (mk[nd]) { applyA(2 * nd, asg[nd]); applyA(2 * nd + 1, asg[nd]); mk[nd] = 0; }
        if (ad[nd]) { applyD(2 * nd, ad[nd]); applyD(2 * nd + 1, ad[nd]); ad[nd] = 0; }
    };
    function<void(int, int, int, int, int, int, long long)> upd =
        [&](int nd, int l, int r, int tp, int ql, int qr, long long x) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { if (tp == 3) applyA(nd, x); else applyD(nd, x); return; }
        push(nd); int m = (l + r) / 2;
        upd(2 * nd, l, m, tp, ql, qr, x); upd(2 * nd + 1, m + 1, r, tp, ql, qr, x);
        t[nd] = max(t[2 * nd], t[2 * nd + 1]);
    };
    function<long long(int, int, int, int, int)> qry =
        [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MIN;
        if (ql <= l && r <= qr) return t[nd];
        push(nd); int m = (l + r) / 2;
        return max(qry(2 * nd, l, m, ql, qr), qry(2 * nd + 1, m + 1, r, ql, qr));
    };
    build(1, 1, n);
    int q; in >> q;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1 || tp == 3) {
            int u, v; long long x; in >> u >> v >> x;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                upd(1, 1, n, tp, pos[head[u]], pos[u], x);
                u = par[head[u]];
            }
            upd(1, 1, n, tp, pos[u], pos[v] - 1, x);   // BUG: no swap, drops endpoint
        } else {
            int u, v; in >> u >> v;
            long long r = LLONG_MIN;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                r = max(r, qry(1, 1, n, pos[head[u]], pos[u]));
                u = par[head[u]];
            }
            r = max(r, qry(1, 1, n, pos[u], pos[v] - 1));   // BUG: same here
            out << r << "{{NL}}";
        }
    }
""") + END


# ----------------------------------------------------------------- tests
def _ops_str(ops):
    out = []
    for op in ops:
        if op[0] == "add":
            out.append("1 %d %d %d" % (op[1], op[2], op[3]))
        elif op[0] == "asg":
            out.append("3 %d %d %d" % (op[1], op[2], op[3]))
        elif op[0] == "max":
            out.append("2 %d %d" % (op[1], op[2]))
    return out


def _tree_input(par, val, ops_lines):
    n = len(val) - 1
    lines = [str(n), " ".join(str(par[v]) for v in range(2, n + 1)),
             " ".join(str(val[v]) for v in range(1, n + 1)), str(len(ops_lines))]
    lines += ops_lines
    return T(*lines)


# big-test inputs for A1/A2/CP (built BEFORE the test lists)
_rnd = random.Random(7)
_big_par = _bintree_par(100000)
_big_val = list(range(0, 100001))
_big_val[1] = 1
_big_ops = []
for _ in range(1500):
    _u = _rnd.randint(50000, 100000)
    _v = _rnd.randint(50000, 100000)
    _big_ops.append(("add", _u, _v, _rnd.randint(-5, 9)))
for _ in range(1500):
    _u = _rnd.randint(50000, 100000)
    _v = _rnd.randint(50000, 100000)
    _big_ops.append(("max", _u, _v))

# bamboo load inputs for A3 (built BEFORE the test lists)
_rnd3 = random.Random(13)
_n3 = 200000
_ops3 = []
for _ in range(100000):
    _u = _rnd3.randint(1, _n3)
    _ops3.append(("add", _u, _rnd3.randint(1, 9)))
for _ in range(100000):
    _u = _rnd3.randint(1, _n3)
    _ops3.append(("sum", _u))
_bp3 = _bamboo_par(_n3)
_lines3 = [str(_n3),
           " ".join(str(_bp3[v]) for v in range(2, _n3 + 1)),
           " ".join("1" for _ in range(_n3)),
           str(len(_ops3))]
for op in _ops3:
    if op[0] == "add":
        _lines3.append("1 %d %d %d" % (op[1], _n3, op[2]))
    else:
        _lines3.append("2 %d %d" % (op[1], _n3))

A1_TESTS = [
    contest_test(
        "hand tree basic",
        _tree_input(_bintree_par(0) if False else [0, 0, 1, 1, 2, 2, 3],
                    [0, 1, 2, 3, 4, 5, 6],
                    ["1 4 6 10", "2 4 6", "2 5 2", "1 2 5 -3", "2 4 5"]),
        T("16", "12", "14"),
        "Add 10 on 4..6, then maxes; after -3 on 2..5 the last max reads 14. Exercises both lift rounds and the same-chain finish."),
    contest_test(
        "single vertex path",
        _tree_input([0, 1, 1, 1], [0, 5, 7, 9], ["2 3 3", "1 2 2 4", "2 2 2"]),
        T("9", "11"),
        "u == v paths must hit the final same-chain segment — an off-by-one there reads an empty range."),
    contest_test(
        "balanced binary tree, 3000 mixed ops",
        _tree_input(_big_par, _big_val, _ops_str(_big_ops)),
        T(*_model_add_max_assign(100000, _big_par, _big_val, _big_ops)),
        "3000 ops over a 100k balanced binary tree: O(q log^2 n) vs O(q-depth)."),
]

A2_TESTS = [
    contest_test(
        "assign then read",
        _tree_input([0, 0, 1, 1, 2, 2, 3], [0, 1, 2, 3, 4, 5, 6],
                    ["3 4 6 10", "2 4 6", "3 6 6 -3", "2 3 6"]),
        T("10", "10"),
        "Assign 10 on 4..6 (path bends at the root, so 1 and 3 are included) → max 10; assign -3 at 6 → max 3..6 = 10. The assign must hit every path vertex."),
    contest_test(
        "stale add leaks through a sub-segment query",
        _tree_input([0, 0, 1, 2, 3], [0, 1, 1, 1, 1],
                    ["1 3 4 10", "3 1 4 0", "2 3 3", "2 4 4"]),
        T("0", "0"),
        "Add +10 on 3..4, assign 0 on 1..4, then query single vertices: a pending add that survives the assign leaks 10."),
]
_rnd2 = random.Random(11)
_big2_ops = []
for _ in range(1500):
    _u = _rnd2.randint(50000, 100000)
    _v = _rnd2.randint(50000, 100000)
    _big2_ops.append(("asg", _u, _v, _rnd2.randint(1, 40)))
for _ in range(1500):
    _u = _rnd2.randint(50000, 100000)
    _v = _rnd2.randint(50000, 100000)
    _big2_ops.append(("max", _u, _v))
A2_TESTS.append(contest_test(
    "balanced binary tree, 3000 assign/max ops",
    _tree_input(_big_par, _big_val, _ops_str(_big2_ops)),
    T(*_model_add_max_assign(100000, _big_par, _big_val, _big2_ops)),
    "Assign tags compose across chains; only the tag tree survives this load."))

A3_TESTS = [
    contest_test(
        "hand tree sums",
        _tree_input([0, 0, 1, 1, 2, 2, 3], [0, 1, 2, 3, 4, 5, 6],
                    ["1 4 6 10", "2 4 6", "2 5 2", "1 2 5 -3", "2 4 5"]),
        T("66", "17", "25"),
        "Sum after add 10: 14+12+11+13+16 = 66; path 5..2 sums 17; after -3 on 2..5, path 4..5 sums 13+2+5+5 = 25."),
    contest_test(
        "bamboo, 200000 full-suffix ops",
        T(*_lines3),
        T(*_model_suffix_sum(_n3, _ops3)),
        "Every op touches a path of length up to n on a bamboo: the per-op parent climb is O(n) — timeout; HLD + lazy tree is log^2."),
]

CP_TESTS = [
    contest_test(
        "mixed add/assign/max",
        _tree_input([0, 0, 1, 1, 2, 2, 3], [0, 1, 2, 3, 4, 5, 6],
                    ["1 4 6 10", "2 4 6", "3 4 6 1", "2 4 6", "1 5 5 7", "2 2 5"]),
        T("16", "1", "12"),
        "Add 10 → max 16; assign 1 resets the path → max 1; +7 at 5 lifts max(2..5) to 12."),
    contest_test(
        "assign clears pending adds",
        _tree_input([0, 1, 1, 2], [5, 5, 5, 5],
                    ["1 2 3 7", "2 2 3", "3 2 3 1", "2 2 3"]),
        T("12", "1"),
        "A stale pending add leaks 8; the assign tag must kill it."),
]
_rnd4 = random.Random(17)
_cp_ops = []
for _ in range(2000):
    _u = _rnd4.randint(50000, 100000)
    _v = _rnd4.randint(50000, 100000)
    _cp_ops.append(("add", _u, _v, _rnd4.randint(-5, 9)))
for _ in range(2000):
    _u = _rnd4.randint(50000, 100000)
    _v = _rnd4.randint(50000, 100000)
    _cp_ops.append(("asg", _u, _v, _rnd4.randint(1, 40)))
for _ in range(2000):
    _u = _rnd4.randint(50000, 100000)
    _v = _rnd4.randint(50000, 100000)
    _cp_ops.append(("max", _u, _v))
CP_TESTS.append(contest_test(
    "balanced binary tree, 6000 mixed ops",
    _tree_input(_big_par, _big_val, _ops_str(_cp_ops)),
    T(*_model_add_max_assign(100000, _big_par, _big_val, _cp_ops)),
    "All three tags compose across chain lifts; 6000 ops keep the log^2 honest."))


# ----------------------------------------------------------------- emit
write_lesson(
    M, "hsga-m7-size",
    "Sizing the Chains",
    "Subtree sizes pick the heavy child; every other edge is light. A path crosses at most log2(n) light edges — that bound is the whole complexity proof.",
    35,
    """
# Heavy and light

Root the tree. For each node u, the child with the largest subtree is
the **heavy child**; every other child edge is **light**.

Why it works: whenever a path moves across a light edge, the subtree
size at least doubles. So a root path crosses at most log2(n) light
edges, and any u..v path decomposes into at most 2·log2(n) contiguous
vertical segments. That single bound is the entire HLD complexity proof —
no amortization, no potential function.

One iterative DFS computes everything HLD needs later:

```
sz[u] = 1 + sum(sz[c]);  hv[u] = argmax child
```

Store `hv[u] = 0` for leaves. The DFS must be iterative: a bamboo of
2·10^5 nodes overflows the 8 MB sandbox stack with plain recursion.
""",
    "Đo đạc chuỗi",
    "Kích thước cây con chọn con nặng; mọi cạnh khác là nhẹ. Một đường đi vượt tối đa log2(n) cạnh nhẹ — chặn đó là toàn bộ chứng minh độ phức tạp.",
    """
# Nặng và nhẹ

Gốc cây. Với mỗi nút u, con có cây con lớn nhất là **con nặng**; mọi
cạnh con khác là **nhẹ**.

Vì sao đúng: mỗi lần đường đi bước qua một cạnh nhẹ, kích thước cây con
ít nhất gấp đôi. Vậy đường đi lên gốc vượt tối đa log2(n) cạnh nhẹ, và
mỗi đường u..v phân rã thành tối đa 2·log2(n) đoạn dọc liền kề. Chặn đó
là toàn bộ chứng minh độ phức tạp của HLD — không amortize, không hàm
tiềm năng.

Một DFS lặp tính mọi thứ HLD cần về sau:

```
sz[u] = 1 + sum(sz[c]);  hv[u] = argmax child
```

Lá có `hv[u] = 0`. DFS phải lặp: cây dạng đường 2·10^5 đỉnh làm tràn
stack 8 MB của sandbox nếu đệ quy thuần.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m7-decompose",
    "Positions, Heads, and the Walk",
    "A heavy-first preorder makes each chain one contiguous range; the query loop lifts the deeper chain head, then finishes with one same-chain segment.",
    35,
    """
# The decomposition walk

Second DFS, preorder, heavy child first:

```
pos[u]  = cnt++;                          // entry order
head[u] = (hv[par[u]] == u) ? head[par[u]] : u;
```

Heavy-first entry order makes every chain a contiguous range of
positions — a chain [1,2,4] gets pos 0,1,2 on the hand tree. The segment
tree is built over POSITIONS: `a[pos[v]] = val[v]`.

The path query loop:

```
while (head[u] != head[v]) {                if (dep[head[u]] < dep[head[v]]) swap(u, v);
    apply(pos[head[u]], pos[u]);          // whole chain head..u
    u = par[head[u]];                     // jump above the chain
}
if (pos[u] > pos[v]) swap(u, v);
apply(pos[u], pos[v]);                    // final same-chain segment
```

Lift the DEEPER HEAD (not the deeper node). Two classic real bugs:
forgetting the final same-chain segment (entirely, or its swap), and
indexing the tree by vertex id instead of `pos`. Both pass the tiny
sample, both die on any real test.
""",
    "Vị trí, đầu chuỗi, và vòng đi",
    "Preorder vào con nặng trước biến mỗi chuỗi thành một đoạn liền; vòng truy vấn nâng đầu chuỗi sâu hơn rồi kết thúc bằng một đoạn cùng chuỗi.",
    """
# Vòng phân rã

DFS thứ hai, preorder, con nặng trước:

```
pos[u]  = cnt++;                          // thứ tự vào
head[u] = (hv[par[u]] == u) ? head[par[u]] : u;
```

Thứ tự vào nặng-trước biến mỗi chuỗi thành một đoạn vị trí liền kề —
chuỗi [1,2,4] nhận pos 0,1,2 trên cây tay. Cây đoạn dựng trên VỊ TRÍ:
`a[pos[v]] = val[v]`.

Vòng truy vấn đường đi:

```
while (head[u] != head[v]) {                if (dep[head[u]] < dep[head[v]]) swap(u, v);
    apply(pos[head[u]], pos[u]);          // cả đoạn đầu chuỗi..u
    u = par[head[u]];                     // nhảy lên trên chuỗi
}
if (pos[u] > pos[v]) swap(u, v);
apply(pos[u], pos[v]);                    // đoạn cuối cùng chuỗi
```

Nâng ĐẦU chuỗi sâu hơn (không phải nút sâu hơn). Hai lỗi thật kinh
điển: quên đoạn cuối cùng chuỗi (hoặc quên swap của nó), và đánh chỉ số
cây theo id đỉnh thay vì `pos`. Cả hai đều qua mẫu nhỏ và chết trên test
thật.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m7-vs",
    "HLD vs the Cheaper Structure",
    "Subtree queries need only an Euler tour; commutative path sums fit binary lifting; HLD earns its 150 lines only when path aggregates meet path updates.",
    35,
    """
# Paying for HLD only when needed

Decision ladder, cheapest first:

1. **Subtree** add/count → Euler tour + BIT (M5). No chains.
2. **Path u..v, point updates, distance-sum style** → binary lifting +
   rerooting bookkeeping (M4/M6).
3. **Path u..v aggregates (max/sum) WITH path or range updates** → HLD +
   lazy segment tree (M2). The only structure in the course that answers
   path-max under path-add for n, q ≤ 2·10^5.

HLD costs ~150 lines and buys O((n+q)·log² n). Each op touches at most
2·log2(n) chain segments, each a tree op — comfortable inside the
sandbox's 20 s job budget. The danger is the naive per-op path climb,
O(depth) per query: it dies exactly like A3's wrong solution below.
""",
    "HLD so với cấu trúc rẻ hơn",
    "Truy vấn cây con chỉ cần Euler tour; tổng đường đi giao hoán vừa binary lifting; HLD chỉ đáng 150 dòng khi tổng kết đường đi gặp cập nhật đường đi.",
    """
# Chỉ trả tiền HLD khi cần

Thang quyết định, rẻ trước:

1. **Cây con** add/đếm → Euler tour + BIT (M5). Không cần chuỗi.
2. **Đường u..v, cập nhật điểm, dạng tổng khoảng cách** → binary lifting
   + sổ đổi gốc (M4/M6).
3. **Tổng kết đường u..v (max/sum) CÓ cập nhật đường/đoạn** → HLD + cây
   đoạn lazy (M2). Cấu trúc duy nhất trong khóa trả lời path-max dưới
   path-add với n, q ≤ 2·10^5.

HLD tốn ~150 dòng và mua O((n+q)·log² n). Mỗi phép chạm tối đa
2·log2(n) đoạn chuỗi, mỗi đoạn một phép cây — thoải mái trong ngân sách
20 s/job của sandbox. Cái nguy hiểm là leo đường đi từng phép,
O(depth)/truy vấn: chết đúng như bản sai của A3 bên dưới.
""",
    difficulty="advanced",
)

write_checkpoint(
    M, "hsga-cp-m7",
    "Checkpoint — Path Queries with HLD",
    "A 2·10^5-node balanced tree under 6000 mixed add/assign/max path operations; the walk that drops the final same-chain segment is the graded wrong answer.",
    40,
    """
**Checkpoint — HLD.** Cây gốc 1: dòng 1 là n; dòng 2 là cha của 2..n;
dòng 3 là val[1..n]; dòng 4 là q; theo sau là q phép toán:
"1 u v x" — cộng x vào mọi đỉnh trên đường u..v; "3 u v x" — gán x cho
mọi đỉnh trên đường u..v; "2 u v" — in GIÁ TRỊ LỚN NHẤT trên đường u..v
(mỗi truy vấn một dòng).

HLD + cây đoạn ba-tag (gán/cộng, max); vòng đi phải xử lý đúng đoạn cuối
cùng chuỗi, kể cả khi pos[u] > pos[v].
""",
    "Điểm kiểm tra — Truy vấn đường đi với HLD",
    "Cây 2·10^5 đỉnh dưới 6000 phép cộng/gán/max trên đường đi; vòng đi bỏ sót đoạn cuối cùng chuỗi là đáp án sai bị chấm.",
    """
**Checkpoint — HLD.** Cây gốc 1 (dòng 1: n; dòng 2: cha 2..n; dòng 3:
val[1..n]; dòng 4: q; q dòng phép toán 1/3/2 như bản EN).
""",
    challenge(
        "hsga-cp-m7-hldmix",
        "Mixed Path Operations",
        """**Bài toán.** A rooted tree (root 1): n on line 1; parents par[2..n]
on line 2 (par[v] < v); vertex values val[1..n] on line 3; q on line 4;
then q operations: "1 u v x" — add x to every vertex on the path u..v;
"3 u v x" — assign x to every vertex on the path u..v; "2 u v" — print
the MAXIMUM value on the path u..v, one per line.

**Constraints:** 1 ≤ n, q ≤ 200 000; |val|, |x| ≤ 10^9.

HLD over chain positions with a three-tag lazy tree (assign kills the
pending add); the walk must handle the final same-chain segment even
when pos[u] > pos[v].
""",
        CP_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Phép toán đường đi hỗn hợp",
        """**Bài toán.** Cây gốc 1 (dòng 1: n; dòng 2: cha 2..n; dòng 3:
val[1..n]; dòng 4: q; q phép toán "1 u v x" cộng, "3 u v x" gán,
"2 u v" in max trên đường).""",
        [("đoạn cuối cùng chuỗi", "Khi pos[u] > pos[v], quên swap làm mất cả đoạn."),
         ("gán xóa cộng", "Tag gán phải xóa pending add của nút đó."),
         ("n=200000", "O((n+q)·log² n); leo đường từng phép là O(n·q) — timeout.")],
    ),
    solution=CP_M7_R,
    wrong=CP_M7_W,
)

VI_P7 = {
    "hsga-p7-hld": vi_challenge(
        "Bộ ba HLD",
        """**Bài toán.** Ba bài trên cùng giao thức: (1) cộng/max trên đường;
(2) gán/max trên đường; (3) cộng/tổng trên đường với bài tải bamboo.""",
        [("đoạn cuối", "Quên đoạn cùng chuỗi (hoặc swap) là lỗi kinh điển."),
         ("gán vs cộng", "Gán phải xóa pending add; cộng sau gán cộng vào tag gán."),
         ("bamboo 2·10^5", "Leo đường từng phép O(n)/op — chỉ HLD sống.")],
    ),
}

write_practice(
    M, "hsga-p7-hld", "HLD Trio",
    "Path add/max, path assign/max, and path add/sum — same protocol, three lazy trees, one near-miss timeout on a bamboo.",
    "Bộ ba HLD",
    "Cộng/max, gán/max, cộng/tổng trên đường — cùng giao thức, ba cây lazy, một bài near-miss timeout trên bamboo.",
    "hsga-m7-vs",
    110,
    "advanced",
    [
        challenge("hsga-p7-pathmax", "Path Add, Path Max",
            """**Bài toán.** A rooted tree (root 1): n on line 1; parents par[2..n]
on line 2 (par[v] < v); vertex values val[1..n] on line 3; q on line 4;
then q operations: "1 u v x" — add x to every vertex on the path u..v;
"2 u v" — print the MAXIMUM value on the path u..v, one per line.

**Constraints:** 1 ≤ n, q ≤ 200 000; |val|, |x| ≤ 10^9.

HLD over chain positions + a lazy range-add/range-max tree:
O((n + q)·log² n). The final same-chain segment needs the swap.
""",
            A1_TESTS, level="combination", difficulty="advanced"),
        challenge("hsga-p7-assignmax", "Path Assign, Path Max",
            """**Bài toán.** Same input protocol; operations: "1 u v x" — add x
to every vertex on the path u..v; "3 u v x" — assign x to every vertex
on the path u..v; "2 u v" — print the MAXIMUM value on the path u..v,
one per line.

**Constraints:** 1 ≤ n, q ≤ 200 000; |val|, |x| ≤ 10^9.

Three-tag lazy tree over HLD positions. A pending add that survives an
assign is the classic bug this challenge is built to catch.
""",
            A2_TESTS, level="combination", difficulty="advanced"),
        challenge("hsga-p7-pathsum", "Path Add, Path Sum",
            """**Bài toán.** Same input protocol; operations: "1 u v x" — add x to
every vertex on the path u..v; "2 u v" — print the SUM of values on the
path u..v, one per line.

**Constraints:** 1 ≤ n, q ≤ 200 000; |val|, |x| ≤ 10^9 (sums fit in
long long).

HLD + lazy range-add/range-sum tree. The load test is a bamboo with
2·10^5 path operations — the per-op parent climb times out.
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    VI_P7,
    solutions=[
        ("hsga-p7-pathmax", A1_R, A1_W),
        ("hsga-p7-assignmax", A2_R, A2_W),
        ("hsga-p7-pathsum", A3_R, A3_W),
    ],
)

print("module m7 complete")
