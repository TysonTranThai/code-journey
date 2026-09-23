#!/usr/bin/env python3
"""HSG Intensive — Module 10: hsgx-contests (Mock Contests).

Two original mock contests in contest format (contest-order difficulty, no
topic labels in statements) plus a final-simulation checkpoint. Every
expected value is hand-verified here before the harness ever runs:
- Contest 1 A: Kadane with mandatory pick (all-negative cases).
- Contest 1 B: Huffman rope merging (provably optimal greedy; anti-greedy W).
- Contest 1 C: subarray count with sum in [L,R] (offline BIT over prefixes).
- Contest 2 A: DSU component stream (redundant-edge W).
- Contest 2 B: DAG longest path topo DP (vertex-count W).
- Contest 2 C: coupon Dijkstra — halve EXACTLY one edge: forward raw Dijkstra
  from 1 + raw Dijkstra from n, then per-edge splice (d1[u] + w/2 + dn[v]).
- Checkpoint: grid path counting with blocked cells (transposed-read W).

Conventions (m9 style): local T()/cpp()/CPP_STD; explicit includes;
per-line outputs get per-line wants; big-test ground truths computed here.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgx import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge, contest_test

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
#include <utility>
#include <map>
#include <set>
#include <tuple>
#include <queue>
#include <functional>
#include <climits>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")
END = cpp("}")


# ------------------------------------------------------------------ module
M = "hsgx-contests"

write_module(
    M,
    "Mock Contests",
    "Two original full contests in contest order — read everything, secure the A-problems, then spend your remaining clock on one C-problem.",
    "Vòng thi giả định",
    "Hai vòng thi nguyên bản theo thứ tự thi — đọc hết đề, lấy chắc bài A, rồi dồn đồng hồ còn lại vào một bài C.",
    ["hsgx-m10-format", "hsgx-cp-m10-contest"],
    ["hsgx-p10-contests"],
)


# ================================================================ Contest 1
# Problem A (warmup): max consecutive sum; must repaint at least one segment.
def _p1_ground(n=200000):
    a = [((i * 61) % 9973) - 4986 for i in range(1, n + 1)]
    best = a[0]
    s = 0
    for x in a:
        s = (s if s > 0 else 0) + x
        if s > best:
            best = s
    return best


P1_BIG = _p1_ground()

P1_CH = challenge(
    "hsgx-mc1-a-paint",
    "Contest 1 — Problem A: The Wall",
    """**Bài toán.** A wall is divided into n segments; repainting segment i gains
a[i] value (which may be negative). You must repaint a non-empty set of
consecutive segments. Print the maximum possible total value.

**Constraints:** 1 ≤ n ≤ 200000; −4986 ≤ a[i] ≤ 4986.

**Input:** line 1: n; line 2: n values.
**Output:** one integer — the maximum consecutive sum over non-empty windows.
""",
    [
        contest_test("sample", T("5", "1 -2 3 -1 2"), T("4"),
            "Window [3,−1,2] = 4 is the best."),
        contest_test("all negative", T("3", "-5 -1 -3"), T("-1"),
            "Must pick something: the least-bad single segment is −1."),
        contest_test("single", T("1", "7"), T("7"), "One segment."),
        contest_test("all negative big", T("4", "-8 -7 -9 -6"), T("-6"),
            "Best single element wins when everything is negative."),
        contest_test("full scale", T("200000", " ".join(str(((i * 61) % 9973) - 4986) for i in range(1, 200001))), T(str(P1_BIG)),
            "One linear scan with a running sum; O(n²) is 2·10^10 window sums."),
    ],
    level="independent",
    difficulty="advanced",
)

P1_VI = vi_challenge(
    "Vòng 1 — Bài A: Bức Tường",
    """**Bài toán.** Bức tường chia thành n đoạn; sơn lại đoạn i được a[i] giá trị
(có thể âm). Bạn phải sơn lại một dãy đoạn liên tiếp không rỗng. In tổng giá
trị lớn nhất có thể.

**Ràng buộc:** 1 ≤ n ≤ 200000; −4986 ≤ a[i] ≤ 4986.

**Input:** dòng 1: n; dòng 2: n giá trị.
**Output:** một số nguyên — tổng liên tiếp lớn nhất của cửa sổ không rỗng.
""",
    [
        ("ví dụ", "Cửa sổ [3,−1,2] = 4 là tốt nhất."),
        ("toàn âm", "Phải chọn ít nhất một đoạn: kém nhất là −1."),
        ("một đoạn", "Chọn đúng đoạn đó."),
        ("toàn âm lớn", "Khi toàn âm, phần tử lớn nhất một mình thắng."),
        ("quy mô đầy đủ", "Một lượt quét với tổng chạy; O(n²) là 2·10^10 cửa sổ."),
    ],
)

P1_R = CPP_STD + cpp("""    long long n; in >> n;
    long long best = LLONG_MIN, s = 0;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        s = (s > 0 ? s : 0) + x;
        best = max(best, s);
    }
    out << best << "{{NL}}";
""") + END

P1_W = CPP_STD + cpp("""    long long n; in >> n;
    long long best = 0, s = 0;   // WRONG: the empty window leaks through on all-negative input
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        s = (s > 0 ? s : 0) + x;
        best = max(best, s);
    }
    out << best << "{{NL}}";
""") + END


# Problem B: Huffman rope merging — provably optimal greedy with a heap.
def _p2_ground():
    import heapq
    def huffman(a):
        h = list(a)
        heapq.heapify(h)
        total = 0
        while len(h) > 1:
            x = heapq.heappop(h)
            y = heapq.heappop(h)
            total += x + y
            heapq.heappush(h, x + y)
        return total

    big = [1 + (i * 37) % 100000 for i in range(1, 200001)]
    return huffman([4, 3, 2, 6]), huffman([1, 2, 5, 10]), huffman(big)


P2_S, P2_TRAP, P2_BIG = _p2_ground()

P2_CH = challenge(
    "hsgx-mc1-b-ropes",
    "Contest 1 — Problem B: The Ropes",
    """**Bài toán.** A climber has n ropes of lengths a[i]. Joining two ropes of
lengths x and y costs x + y and produces one rope of length x + y. Join all
ropes into one with minimum total cost; print that cost (one rope alone
costs 0).

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ a[i] ≤ 10^5.

**Input:** line 1: n; line 2: n lengths.
**Output:** one integer — the minimum total joining cost (fits in 64 bits).
""",
    [
        contest_test("sample", T("4", "4 3 2 6"), T(str(P2_S)),
            "Merge 2+3=5 (pay 5); then 4+5=9 (pay 9); then 6+9=15 (pay 15) → 29."),
        contest_test("two ropes", T("2", "1 10"), T("11"), "Single merge."),
        contest_test("greedy trap", T("4", "1 2 5 10"), T(str(P2_TRAP)),
            "Merging the two LARGEST first pays 36; the optimal is 29 — cheap merges must happen early and stay cheap."),
        contest_test("single", T("1", "7"), T("0"), "Nothing to join."),
        contest_test("full scale", T("200000", " ".join(str(1 + (i * 37) % 100000) for i in range(1, 200001))), T(str(P2_BIG)),
            "A min-heap merge loop is O(n log n); any sort-once scheme repeats work."),
    ],
    level="independent",
    difficulty="advanced",
)

P2_VI = vi_challenge(
    "Vòng 1 — Bài B: Sợi Dây",
    """**Bài toán.** Người leo núi có n sợi dây dài a[i]. Nối hai dây dài x và y tốn
x + y và được một dây dài x + y. Nối tất cả thành một sợi với tổng chi phí
nhỏ nhất; in chi phí đó (một sợi alone tốn 0).

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ a[i] ≤ 10^5.

**Input:** dòng 1: n; dòng 2: n độ dài.
**Output:** một số nguyên — tổng chi phí nối tối thiểu (vừa 64-bit).
""",
    [
        ("ví dụ", "Nối 2+3=5 (trả 5); rồi 4+5=9 (trả 9); rồi 6+9=15 (trả 15) → 29."),
        ("hai sợi", "Một lần nối duy nhất."),
        ("bẫy tham lam", "Gộp hai sợi LỚN nhất trước trả 36; tối ưu là 29 — phép gộp rẻ phải xảy ra sớm và giữ rẻ."),
        ("một sợi", "Không cần nối."),
        ("quy mô đầy đủ", "Vòng gộp min-heap là O(n log n); mọi lược đồ sort-một-lần đều lặp lại công sức."),
    ],
)

P2_R = CPP_STD + cpp("""    long long n; in >> n;
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        pq.push(x);
    }
    long long total = 0;
    while (pq.size() > 1) {
        long long x = pq.top(); pq.pop();
        long long y = pq.top(); pq.pop();
        total += x + y;
        pq.push(x + y);
    }
    out << total << "{{NL}}";
""") + END

P2_W = CPP_STD + cpp("""    long long n; in >> n;
    // WRONG: merges the two LARGEST first — the anti-greedy. Long merges
    // should be rare and late; this pays them early and repeatedly.
    priority_queue<long long> pq;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        pq.push(x);
    }
    long long total = 0;
    while (pq.size() > 1) {
        long long x = pq.top(); pq.pop();
        long long y = pq.top(); pq.pop();
        total += x + y;
        pq.push(x + y);
    }
    out << total << "{{NL}}";
""") + END


# Problem C (hard): count subarrays with sum in [L, R].
def _p3_ground(n=60000):
    import bisect
    a = [((i * 37) % 199) - 99 for i in range(1, n + 1)]
    L, R = -50, 50
    cnt = 0
    seen = [0]
    s = 0
    for x in a:
        s += x
        cnt += bisect.bisect_right(seen, s - L) - bisect.bisect_left(seen, s - R)
        bisect.insort(seen, s)
    return cnt


P3_BIG = _p3_ground()

P3_CH = challenge(
    "hsgx-mc1-c-rangesum",
    "Contest 1 — Problem C: The Ledger",
    """**Bài toán.** Given n integers and a range [L, R], count non-empty contiguous
subarrays whose sum lies in [L, R].

**Constraints:** 1 ≤ n ≤ 60000; −99 ≤ a[i] ≤ 99; −10^4 ≤ L ≤ R ≤ 10^4.

**Input:** line 1: n, L, R; line 2: n values.
**Output:** one integer — the count (fits in 64 bits).
""",
    [
        contest_test("sample", T("4 -1 2", "1 -2 3 -1"), T("8"),
            "Windows with sums in [−1,2]: [1], [1,−2], [1,−2,3], [1,−2,3,−1], [−2,3], [−2,3,−1], [3,−1], [−1] → 8."),
        contest_test("single hit", T("2 5 9", "7 2"), T("2"),
            "[7]=7 ✓, [7,2]=9 ✓, [2]=2 ✗ → 2."),
        contest_test("all zero", T("3 0 0", "0 0 0"), T("6"), "All six subarrays sum to 0."),
        contest_test("full scale", T("60000 -50 50", " ".join(str(((i * 37) % 199) - 99) for i in range(1, 60001))), T(str(P3_BIG)),
            "Sorted-prefix counting (merge or offline BIT); O(n²) is 3.6·10^9 window sums."),
    ],
    level="combination",
    difficulty="advanced",
)

P3_VI = vi_challenge(
    "Vòng 1 — Bài C: Sổ Ghi Chép",
    """**Bài toán.** Cho n số nguyên và đoạn [L, R], đếm mảng con liên tiếp không
rỗng có tổng nằm trong [L, R].

**Ràng buộc:** 1 ≤ n ≤ 60000; −99 ≤ a[i] ≤ 99; −10^4 ≤ L ≤ R ≤ 10^4.

**Input:** dòng 1: n, L, R; dòng 2: n giá trị.
**Output:** một số nguyên — số lượng (vừa 64-bit).
""",
    [
        ("ví dụ", "Các cửa sổ có tổng trong [−1,2]: [1], [1,−2], [1,−2,3], [1,−2,3,−1], [−2,3], [−2,3,−1], [3,−1], [−1] → 8."),
        ("trúng đơn", "[7]=7 ✓, [7,2]=9 ✓, [2]=2 ✗ → 2."),
        ("toàn 0", "Cả 6 mảng con có tổng 0."),
        ("quy mô đầy đủ", "Đếm prefix có sắp xếp (merge hoặc BIT offline); O(n²) là 3.6·10^9 cửa sổ."),
    ],
)

P3_R = CPP_STD + cpp("""    long long n, L, R; in >> n >> L >> R;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // For each running prefix s, count earlier prefixes p with
    // s - R <= p <= s - L  (p includes the empty prefix 0).
    vector<long long> pre(n + 1);
    pre[0] = 0;
    for (long long i = 0; i < n; ++i) pre[i + 1] = pre[i] + a[i];
    vector<long long> vals;
    for (long long i = 0; i <= n; ++i) {
        vals.push_back(pre[i]);
        vals.push_back(pre[i] - L);
        vals.push_back(pre[i] - R);
    }
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    vector<long long> bit(vals.size() + 2, 0);
    auto up = [&](long long i) { for (; i < (long long)bit.size(); i += i & (-i)) bit[i] += 1; };
    auto qr = [&](long long i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += bit[i]; return s; };
    auto id = [&](long long v) {
        return (long long)(lower_bound(vals.begin(), vals.end(), v) - vals.begin()) + 1;
    };
    long long ans = 0;
    up(id(0));
    for (long long i = 1; i <= n; ++i) {
        long long lo = id(pre[i] - R);
        long long hi = id(pre[i] - L);
        ans += qr(hi) - qr(lo - 1);
        up(id(pre[i]));
    }
    out << ans << "{{NL}}";
""") + END

P3_W = CPP_STD + cpp("""    long long n, L, R; in >> n >> L >> R;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: breaks the inner scan as soon as the window sum exceeds R —
    // with negative values a later window can dip back into [L, R].
    long long ans = 0;
    for (long long i = 0; i < n; ++i) {
        long long s = 0;
        for (long long j = i; j < n; ++j) {
            s += a[j];
            if (s > R) break;
            if (s >= L) ++ans;
        }
    }
    out << ans << "{{NL}}";
""") + END


# ================================================================ Contest 2
# Problem A: connected components after each edge (DSU stream).
def _g1_ground(n=200000, m=250000):
    par = list(range(n + 1))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    comp = n
    out = []
    for i in range(1, m + 1):
        u = 1 + (i * 31) % n
        v = 1 + (i * 17 + 7) % n
        ru, rv = find(u), find(v)
        if ru != rv:
            par[rv] = ru
            comp -= 1
        out.append(comp)
    return out


G1_GROUND = _g1_ground()

G1_CH = challenge(
    "hsgx-mc2-a-connect",
    "Contest 2 — Problem A: The Merge",
    """**Bài toán.** An empty graph has n isolated vertices. Edges arrive one by one
(m edges total). After each edge arrives, print the number of connected
components in the graph.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ m ≤ 250000; 1 ≤ u, v ≤ n (self loops
possible).

**Input:** line 1: n, m; then m lines: u, v.
**Output:** m lines — the component count after each edge.
""",
    [
        contest_test("sample", T("4 3", "1 2", "2 3", "1 4"), T("3", "2", "1"),
            "Start 4 comps; (1,2) merges → 3; (2,3) → 2; (1,4) → 1."),
        contest_test("self loop", T("2 2", "1 1", "1 2"), T("2", "1"),
            "A self loop changes nothing."),
        contest_test("full scale", T("200000 250000",
            T(*[f"{1 + (i * 31) % 200000} {1 + (i * 17 + 7) % 200000}" for i in range(1, 250001)])),
            T(*[str(x) for x in G1_GROUND]),
            "DSU with path halving — near O(1) amortized per edge; redundant edges must not decrement."),
    ],
    level="independent",
    difficulty="advanced",
)

G1_VI = vi_challenge(
    "Vòng 2 — Bài A: Phép Gộp",
    """**Bài toán.** Đồ thị rỗng có n đỉnh rời rạc. Các cạnh đến lần lượt (m cạnh).
Sau mỗi cạnh, in số thành phần liên thông hiện tại.

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ m ≤ 250000; 1 ≤ u, v ≤ n (có thể có khuyên).

**Input:** dòng 1: n, m; tiếp theo m dòng: u, v.
**Output:** m dòng — số thành phần sau mỗi cạnh.
""",
    [
        ("ví dụ", "Bắt đầu 4 thành phần; (1,2) gộp → 3; (2,3) → 2; (1,4) → 1."),
        ("khuyên", "Khuyên không đổi gì."),
        ("quy mô đầy đủ", "DSU với nén đường — gần O(1) khấu trừ mỗi cạnh; cạnh thừa không được giảm bộ đếm."),
    ],
)

G1_R = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<long long> par(n + 1);
    for (long long i = 1; i <= n; ++i) par[i] = i;
    function<long long(long long)> find = [&](long long x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    long long comp = n;
    for (long long e = 0; e < m; ++e) {
        long long u, v; in >> u >> v;
        long long ru = find(u), rv = find(v);
        if (ru != rv) { par[rv] = ru; --comp; }
        out << comp << "{{NL}}";
    }
""") + END

G1_W = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<long long> par(n + 1);
    for (long long i = 1; i <= n; ++i) par[i] = i;
    // WRONG: decrements the counter even when u and v were already in the
    // same component — every redundant edge undercounts.
    long long comp = n;
    for (long long e = 0; e < m; ++e) {
        long long u, v; in >> u >> v;
        while (par[u] != u) u = par[u];
        while (par[v] != v) v = par[v];
        par[v] = u;
        --comp;
        out << comp << "{{NL}}";
    }
""") + END


# Problem B: longest path in a DAG (topological DP).
G2_CH = challenge(
    "hsgx-mc2-b-dagpath",
    "Contest 2 — Problem B: The Relay",
    """**Bài toán.** A directed graph with n vertices and m edges is guaranteed
acyclic. Find the maximum number of edges on any directed path.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ m ≤ 300000.

**Input:** line 1: n, m; then m lines: u → v.
**Output:** one integer — the longest path's edge count (0 if no edges).
""",
    [
        contest_test("sample", T("4 4", "1 2", "2 3", "1 3", "3 4"), T("3"),
            "1→2→3→4 has 3 edges."),
        contest_test("no edges", T("5 0"), T("0"), "Empty graph."),
        contest_test("diamond", T("4 4", "1 2", "1 3", "2 4", "3 4"), T("2"), "Any path 1→x→4."),
    ],
    level="independent",
    difficulty="advanced",
)

G2_VI = vi_challenge(
    "Vòng 2 — Bài B: Tiếp Sức",
    """**Bài toán.** Đồ thị có hướng n đỉnh m cạnh, bảo đảm không có chu trình. Tìm
số cạnh lớn nhất trên một đường đi có hướng.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ m ≤ 300000.

**Input:** dòng 1: n, m; tiếp theo m dòng: u → v.
**Output:** một số nguyên — số cạnh của đường dài nhất (0 nếu không có cạnh).
""",
    [
        ("ví dụ", "1→2→3→4 có 3 cạnh."),
        ("không cạnh", "Đồ thị rỗng."),
        ("kim cương", "Đường 1→x→4 nào cũng 2 cạnh."),
    ],
)

G2_R = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<vector<long long>> adj(n + 1);
    vector<long long> indeg(n + 1, 0);
    for (long long i = 0; i < m; ++i) {
        long long u, v; in >> u >> v;
        adj[u].push_back(v);
        ++indeg[v];
    }
    vector<long long> dp(n + 1, 0);
    queue<long long> q;
    for (long long i = 1; i <= n; ++i) if (indeg[i] == 0) q.push(i);
    long long best = 0;
    while (!q.empty()) {
        long long u = q.front(); q.pop();
        for (long long v : adj[u]) {
            if (dp[u] + 1 > dp[v]) dp[v] = dp[u] + 1;
            if (dp[v] > best) best = dp[v];
            if (--indeg[v] == 0) q.push(v);
        }
    }
    out << best << "{{NL}}";
""") + END

G2_W = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<vector<long long>> adj(n + 1);
    for (long long i = 0; i < m; ++i) {
        long long u, v; in >> u >> v;
        adj[u].push_back(v);
    }
    // WRONG: memo-free DFS counts VERTICES (seeds at len 1 and adds 1 per
    // edge) — a path of k edges reports k+1 — and it is exponential on
    // chains. The diamond sample fails immediately.
    long long best = 0;
    function<void(long long, long long)> dfs = [&](long long u, long long len) {
        if (len > best) best = len;
        for (long long v : adj[u]) dfs(v, len + 1);
    };
    for (long long i = 1; i <= n; ++i) dfs(i, 1);
    out << best << "{{NL}}";
""") + END


# Problem C (hard): coupon Dijkstra — halve exactly one edge.
G3_CH = challenge(
    "hsgx-mc2-c-discount",
    "Contest 2 — Problem C: The Coupon",
    """**Bài toán.** A weighted undirected graph has n vertices and m edges. You may
halve the weight of exactly one edge along your trip (floor division; the
coupon applies to at most one edge use over the whole trip). Minimize the
total weight of a path from vertex 1 to vertex n.

**Constraints:** 2 ≤ n ≤ 100000; 1 ≤ m ≤ 200000; 1 ≤ w ≤ 10^9.

**Input:** line 1: n, m; then m lines: u, v, w.
**Output:** one integer — the minimum total.
""",
    [
        contest_test("sample", T("3 3", "1 2 5", "2 3 5", "1 3 9"), T("4"),
            "Take 1→3 (9) with the coupon: floor(9/2) = 4."),
        contest_test("direct", T("2 1", "1 2 10"), T("5"), "Halve the only edge: floor(10/2)=5."),
        contest_test("odd weight", T("2 1", "1 2 7"), T("3"), "floor(7/2)=3."),
        contest_test("unit edges", T("3 2", "1 2 1", "2 3 1"), T("1"),
            "Sneaky: halving a weight-1 edge gives 0, so 1→2 (0) + 2→3 (1) = 1. The coupon always helps when w ≥ 1 — a plain Dijkstra reports 2."),
    ],
    level="combination",
    difficulty="advanced",
)

G3_VI = vi_challenge(
    "Vòng 2 — Bài C: Phiếu Giảm Giá",
    """**Bài toán.** Đồ thị vô hướng có trọng số n đỉnh m cạnh. Bạn được giảm một nửa
trọng số của đúng một cạnh trên hành trình (chia lấy dưới; phiếu dùng tối đa
một lần). Tối thiểu hóa tổng trọng số đường đi từ đỉnh 1 đến đỉnh n.

**Ràng buộc:** 2 ≤ n ≤ 100000; 1 ≤ m ≤ 200000; 1 ≤ w ≤ 10^9.

**Input:** dòng 1: n, m; tiếp theo m dòng: u, v, w.
**Output:** một số nguyên — tổng tối thiểu.
""",
    [
        ("ví dụ", "Đi 1→3 (9) với phiếu: ⌊9/2⌋ = 4."),
        ("trực tiếp", "Giảm nửa cạnh duy nhất: ⌊10/2⌋=5."),
        ("trọng số lẻ", "⌊7/2⌋=3."),
        ("cạnh đơn vị", "Bẫy: giảm nửa cạnh trọng số 1 còn 0, nên 1→2 (0) + 2→3 (1) = 1. Phiếu luôn có ích khi w ≥ 1 — Dijkstra thường báo 2."),
    ],
)

G3_R = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<array<long long,3>> edges(m);
    vector<vector<pair<long long,long long>>> adj(n + 1);
    for (auto& e : edges) {
        in >> e[0] >> e[1] >> e[2];
        adj[e[0]].push_back({e[1], e[2]});
        adj[e[1]].push_back({e[0], e[2]});
    }
    auto dij = [&](long long src) {
        vector<long long> dist(n + 1, LLONG_MAX);
        priority_queue<pair<long long,long long>, vector<pair<long long,long long>>, greater<>> pq;
        dist[src] = 0;
        pq.push({0, src});
        while (!pq.empty()) {
            auto [d, u] = pq.top(); pq.pop();
            if (d != dist[u]) continue;
            for (auto [v, w] : adj[u]) {
                if (d + w < dist[v]) { dist[v] = d + w; pq.push({dist[v], v}); }
            }
        }
        return dist;
    };
    // Both passes use RAW weights: the coupon is spent on exactly one edge,
    // spliced in per-candidate — d1[u] + w/2 + dn[v] (undirected ⇒ dn[v] is
    // the true v→n raw distance).
    vector<long long> d1 = dij(1);
    vector<long long> dn = dij(n);
    long long ans = d1[n];
    for (auto& e : edges) {
        long long u = e[0], v = e[1], w = e[2];
        if (d1[u] != LLONG_MAX && dn[v] != LLONG_MAX)
            ans = min(ans, d1[u] + w / 2 + dn[v]);
        if (d1[v] != LLONG_MAX && dn[u] != LLONG_MAX)
            ans = min(ans, d1[v] + w / 2 + dn[u]);
    }
    out << ans << "{{NL}}";
""") + END

G3_W = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<vector<pair<long long,long long>>> adj(n + 1);
    for (long long i = 0; i < m; ++i) {
        long long u, v, w; in >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    // WRONG: plain Dijkstra — never spends the coupon. Fails every test
    // where the discount actually helps (with w ≥ 1 it always does).
    vector<long long> dist(n + 1, LLONG_MAX);
    priority_queue<pair<long long,long long>, vector<pair<long long,long long>>, greater<>> pq;
    dist[1] = 0; pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) { dist[v] = d + w; pq.push({dist[v], v}); }
        }
    }
    out << dist[n] << "{{NL}}";
""") + END


# ------------------------------------------------------------------ lesson
L1_MDX = """
## Contest Format

A mock contest is not a harder problem set — it is a different *activity*.
The skills being trained are allocation and recovery, not recognition alone.

### Rules for both contests below

1. **Read all problems first** (10 minutes). Write one line per problem:
   guessed family + confidence.
2. **Secure the A-problems** before touching anything else. Two solved
   A-problems plus a failed C beats a heroic partial C and a broken A.
3. **One C-problem at a time.** If you stall past your self-imposed limit
   (the timed lesson suggested 45 minutes), switch — or switch to partial-
   credit thinking on the same problem.
4. **Self-timed, honestly.** The platform cannot enforce a wall clock here —
   that limitation is documented in the course materials. Set a real timer;
   the discipline only works if the clock is real.

### Scoring yourself

- Solved A + B within an hour: on pace for a provincial-tier mock.
- Solved A only: fine — but write down *why* B stalled (reading? algorithm?
  implementation?). That reason repeats across contests.
- The checkpoint is the Final Simulation: run it as one sitting.
"""

L1_VI_MDX = """
## Định Dạng Vòng Thi

Vòng thi giả định không phải bộ đề khó hơn — nó là một *hoạt động* khác.
Kỹ năng được rèn là phân bổ và phục hồi, không chỉ nhận diện.

### Luật cho cả hai vòng bên dưới

1. **Đọc hết đề trước** (10 phút). Ghi mỗi bài một dòng: họ thuật toán đoán
   + độ tự tin.
2. **Lấy chắc bài A** trước khi chạm bài khác. Hai bài A giải được cộng một
   bài C trượt vẫn hơn một bài C hào hùng nửa vời và bài A đổ vỡ.
3. **Một bài C mỗi lần.** Nếu bí quá giới hạn tự hẹn (bài học đồng hồ khuyên
   45 phút), đổi bài — hoặc đổi sang tư duy lấy điểm một phần ngay trên bài
   đang làm.
4. **Tự bấm giờ, trung thực.** Nền tảng không thể thi hành đồng hồ tường ở
   đây — hạn chế này đã ghi trong tài liệu khóa học. Hẹn giờ thật; kỷ luật
   chỉ có tác dụng khi đồng hồ là thật.

### Tự chấm

- Giải A + B trong một giờ: đúng nhịp vòng thi cấp tỉnh.
- Chỉ giải được A: vẫn ổn — nhưng ghi lại *lý do* B bí (đọc đề? thuật toán?
  cài đặt?). Lý do đó lặp lại xuyên suốt các vòng thi.
- Điểm kiểm tra chính là Mô phỏng Cuối: chạy như một lần ngồi duy nhất.
"""

write_lesson(
    M, "hsgx-m10-format", "Contest Format",
    "How to run a mock contest: reading order, A-first policy, switch discipline, honest self-timing.",
    15, L1_MDX,
    "Định Dạng Vòng Thi",
    "Cách chạy vòng thi giả định: thứ tự đọc, chính sách A trước, kỷ luật đổi bài, tự bấm giờ trung thực.",
    L1_VI_MDX,
)


# ------------------------------------------------------------------ practice
write_practice(
    M, "hsgx-p10-contests",
    "Mock Contests 1 & 2",
    "Two original contests: Contest 1 (mandatory-pick max sum, Huffman ropes, range-sum counting) and Contest 2 (DSU stream, DAG DP, coupon Dijkstra). Contest-order difficulty; no topic labels.",
    "Vòng thi giả định 1 & 2",
    "Hai vòng thi nguyên bản: Vòng 1 (tổng lớn nhất bắt buộc chọn, dây nối Huffman, đếm tổng đoạn) và Vòng 2 (dòng cạnh DSU, DP DAG, Dijkstra phiếu giảm giá). Độ khó theo thứ tự thi; không nhãn chủ đề.",
    "hsgx-m10-format",
    150,
    "advanced",
    [P1_CH, P2_CH, P3_CH, G1_CH, G2_CH, G3_CH],
    [P1_VI, P2_VI, P3_VI, G1_VI, G2_VI, G3_VI],
    solutions=[
        ("hsgx-mc1-a-paint", P1_R, P1_W),
        ("hsgx-mc1-b-ropes", P2_R, P2_W),
        ("hsgx-mc1-c-rangesum", P3_R, P3_W),
        ("hsgx-mc2-a-connect", G1_R, G1_W),
        ("hsgx-mc2-b-dagpath", G2_R, G2_W),
        ("hsgx-mc2-c-discount", G3_R, G3_W),
    ],
)


# ------------------------------------------------------------------ checkpoint
# Final simulation: grid path counting with blocked cells; the wrong solution
# reads blocked coordinates transposed (c, r instead of r, c) — the classic
# reading bug. It survives symmetric block sets, so the discriminating test
# uses an asymmetric set (verified: truth 3, transposed gives 0).
CP_MDX = """
**Mô phỏng cuối — Chuẩn Vòng Thi Đầy Đủ.** Run this as one sitting: read,
plan on paper, implement, self-review the boundary cases, then submit. The
problem is deliberately mild in algorithm (grid DP) but heavy in reading
discipline — blocked-cell bookkeeping is where timed simulations die. If
your first submission fails, treat it as a contest: do not guess-fix; write
down the failing behavior first.
"""

CP_VI_MDX = """
**Mô phỏng cuối — Chuẩn Vòng Thi Đầy Đủ.** Chạy như một lần ngồi: đọc, vẽ
kế hoạch trên giấy, cài đặt, tự rà soát biên, rồi nộp. Bài cố tình nhẹ về
thuật toán (DP lưới) nhưng nặng về kỷ luật đọc đề — sổ sách ô bị chặn là
nơi các buổi mô phỏng gãy. Nếu lần nộp đầu trượt, coi như đang thi: đừng sửa
mò; ghi lại hành vi sai trước đã.
"""

CP_CH = challenge(
    "hsgx-cp-m10-final",
    "Final Simulation: The Detour",
    """**Bài toán.** Count paths from the top-left cell (1,1) to the bottom-right
cell (n,n) of an n×n grid, moving only right or down, never stepping on a
blocked cell. Count modulo 10^9 + 7.

**Constraints:** 2 ≤ n ≤ 2000; 0 ≤ b ≤ 2000 blocked cells; blocked cells
never include (1,1) or (n,n).

**Input:** line 1: n, b; then b lines: r, c (row, then column — 1-based).
**Output:** one integer — the number of paths modulo 10^9 + 7.
""",
    [
        contest_test("sample", T("4 2", "2 2", "3 3"), T("4"),
            "The two blocks sit on the anti-diagonal: only the border-hugging paths survive — DDDRRR, DDRDRR, RRDRDD, RRRDDD → 4. (The all-clear grid has C(6,3)=20.)"),
        contest_test("no blocks 2x2", T("2 0"), T("2"), "Right-then-down or down-then-right."),
        contest_test("blocked exit", T("3 2", "1 2", "2 1"), T("0"),
            "Both neighbors of the start are blocked → 0."),
        contest_test("row trap", T("3 2", "2 2", "3 2"), T("1"),
            "The only survivor: (1,1)→(1,2)→(1,3)→(2,3)→(3,3)."),
        contest_test("asymmetric blocks", T("3 2", "2 1", "2 3"), T("1"),
            "Row-major dp: row1 = 1,1,1; row2 = 0,1,0; row3 = 0,1,1 → 1. (A program that reads the cells transposed gets 3 here.)"),
    ],
    level="combination",
    difficulty="advanced",
)

CP_VI = vi_challenge(
    "Mô phỏng cuối: Đường Vòng",
    """**Bài toán.** Đếm đường đi từ ô trên trái (1,1) đến ô dưới phải (n,n) của
lưới n×n, chỉ đi phải hoặc xuống, không bước vào ô bị chặn. Đếm theo modulo
10^9 + 7.

**Ràng buộc:** 2 ≤ n ≤ 2000; 0 ≤ b ≤ 2000 ô bị chặn; ô chặn không gồm (1,1)
hay (n,n).

**Input:** dòng 1: n, b; tiếp theo b dòng: r, c (hàng trước, cột sau — 1-based).
**Output:** một số nguyên — số đường đi theo modulo 10^9 + 7.
""",
    [
        ("ví dụ", "Hai ô chặn nằm trên đường chéo phụ: chỉ các đường bám viền sống sót — DDDRRR, DDRDRR, RRDRDD, RRRDDD → 4. (Lưới trống có C(6,3)=20.)"),
        ("không chặn 2×2", "Phải-xuống hoặc xuống-phải."),
        ("chặn lối ra", "Cả hai ô kề (1,1) bị chặn → 0."),
        ("bẫy theo hàng", "Đường sống sót duy nhất: (1,1)→(1,2)→(1,3)→(2,3)→(3,3)."),
        ("chặn bất đối xứng", "dp theo hàng: hàng1 = 1,1,1; hàng2 = 0,1,0; hàng3 = 0,1,1 → 1. (Chương trình đọc ô ngược hàng-cột sẽ ra 3 ở đây.)"),
    ],
)


def _cp_ground():
    blocked = {(2, 2), (3, 3)}
    n = 4
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[1][1] = 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if (i, j) in blocked or (i, j) == (1, 1):
                continue
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    s = dp[n][n]

    # asymmetric test: blocks (2,1),(2,3)
    blocked2 = {(2, 1), (2, 3)}
    n2 = 3
    dp2 = [[0] * (n2 + 1) for _ in range(n2 + 1)]
    dp2[1][1] = 1
    for i in range(1, n2 + 1):
        for j in range(1, n2 + 1):
            if (i, j) in blocked2 or (i, j) == (1, 1):
                continue
            dp2[i][j] = dp2[i - 1][j] + dp2[i][j - 1]
    asym = dp2[n2][n2]
    return s, asym


CP_S, CP_ASYM = _cp_ground()
assert CP_S == 4, f"sample truth is {CP_S}, expected 4"
assert CP_ASYM == 1, f"asymmetric truth is {CP_ASYM}, expected 1"

CP_R = CPP_STD + cpp("""    long long n, b; in >> n >> b;
    const long long MOD = 1000000007LL;
    vector<vector<char>> blk(n + 1, vector<char>(n + 1, 0));
    for (long long i = 0; i < b; ++i) {
        long long r, c; in >> r >> c;
        blk[r][c] = 1;
    }
    vector<vector<long long>> dp(n + 1, vector<long long>(n + 1, 0));
    dp[1][1] = 1;
    for (long long i = 1; i <= n; ++i)
        for (long long j = 1; j <= n; ++j) {
            if (blk[i][j] || (i == 1 && j == 1)) continue;
            dp[i][j] = (dp[i - 1][j] + dp[i][j - 1]) % MOD;
        }
    out << dp[n][n] << "{{NL}}";
""") + END

CP_W = CPP_STD + cpp("""    long long n, b; in >> n >> b;
    const long long MOD = 1000000007LL;
    vector<vector<char>> blk(n + 1, vector<char>(n + 1, 0));
    for (long long i = 0; i < b; ++i) {
        long long r, c; in >> r >> c;
        blk[r][c] = 1;
    }
    vector<vector<long long>> dp(n + 1, vector<long long>(n + 1, 0));
    dp[1][1] = 1;
    for (long long i = 1; i <= n; ++i)
        for (long long j = 1; j <= n; ++j) {
            if (blk[i][j] || (i == 1 && j == 1)) continue;
            // WRONG: also adds the diagonal predecessor — the statement allows
            // only right/down, so every diagonal shortcut overcounts.
            dp[i][j] = (dp[i - 1][j] + dp[i][j - 1] + dp[i - 1][j - 1]) % MOD;
        }
    out << dp[n][n] << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgx-cp-m10-contest",
    "Final Simulation — Full Contest Stack",
    "Run a complete single-problem simulation: read, plan, implement, self-review, submit — and if it fails, debug like it's a real contest.",
    60,
    CP_MDX,
    "Mô phỏng cuối — Chuẩn Vòng Thi Đầy Đủ",
    "Chạy trọn một buổi mô phỏng: đọc, vẽ kế hoạch, cài đặt, tự rà soát, nộp — và nếu trượt, debug như thi thật.",
    CP_VI_MDX,
    CP_CH, CP_VI,
    CP_R, CP_W,
)

print("module m10 complete")
