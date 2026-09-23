#!/usr/bin/env python3
"""HSG Intensive — Module 4: hsgx-combinations (Algorithm Combinations).

Problems that need two known tools fused: binary search + greedy, coordinate
compression + Fenwick, DSU over time, Dijkstra on state graphs, SCC + DAG DP.
Topic names never appear in the problem statements.

Conventions: T() real newlines; cpp() → \n escapes; explicit includes;
per-line outputs get per-line wants; big-test ground truths Python-verified.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgx import (
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
#include <utility>
#include <queue>
#include <map>
#include <set>
#include <functional>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgx-combinations"
write_module(
    M,
    "Algorithm Combinations",
    "Fusing two known tools into one solution: binary search + greedy, compression + Fenwick, DSU across time, Dijkstra over states, SCC + DAG DP — with the recognition each pairing earns.",
    "Vòng kết nối hai công cụ",
    "Hòa hai công cụ quen thuộc thành một lời giải: tìm kiếm nhị phân + greedy, nén tọa độ + Fenwick, DSU theo thời gian, Dijkstra trên đồ thị trạng thái, SCC + DP trên DAG.",
    ["hsgx-m4-fusing", "hsgx-m4-pairings", "hsgx-cp-m4"],
    ["hsgx-p4-combos"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgx-m4-fusing",
    "Fusing Two Tools",
    "Why hard problems are rarely one algorithm: the fuse pattern, the interface between halves, and what makes a combination recognizable.",
    25,
    """
# Fusing Two Tools

A provincial HSG hard problem is rarely "run Dijkstra". It is "run Dijkstra
*on a graph you must first build*". The skill is seeing the two halves and
the interface between them.

## The fuse pattern

Almost every combination has this shape:

```
read input → [transform A] → [core algorithm B] → answer
```

The transformations are where combinations live: sorting to enable greedy,
compression to shrink a domain, building an auxiliary graph (states, time
layers, residual networks), precomputing structure (LCA tables, sparse
tables, prefix DSU forests).

## The interface is the design

When you combine binary search with greedy, the *interface* is a yes/no
feasibility predicate. When you combine SCC with DAG DP, the interface is
the condensation graph. When you fuse Dijkstra with state graphs, the
interface is the state definition — get it wrong (too big → memory death;
too small → wrong answers) and both halves fail.

## Cost accounting for combinations

The total is not A + B; it is usually A · B or A + B depending on how they
nest: binary search (log C) × greedy check O(n) = O(n log C). Compression
O(n log n) + Fenwick queries O((n+q) log n). Budget the *composition*,
not the pieces.

## Recognition: what earns a combination

- "Minimize the maximum / maximize the minimum" + a checkable arrangement →
  binary search + greedy (or + matching).
- Values up to 10^9 but only n ≤ 2·10^5 of them → coordinate compression,
  then anything domain-shaped (Fenwick over values, DP over values).
- Events in time order + connectivity questions → DSU over time (add edges
  in chronological order), or a persistent/LCT structure if removals exist.
- "State" is more than a position (fuel left, keys held, parity, coins) →
  BFS/Dijkstra over the product state graph. Watch the size!
- "If a cycle exists, the answer is impossible" → SCC first, then DP on the
  condensation.
""",
    "Hòa hai công cụ",
    "Vì sao bài khó hiếm khi chỉ là một thuật toán: mẫu hòa trộn, giao diện giữa hai nửa, và điều gì khiến một cặp kết hợp được nhận ra.",
    """
# Hòa hai công cụ

Bài khó cấp tỉnh hiếm khi là "chạy Dijkstra". Nó là "chạy Dijkstra *trên một
đồ thị bạn phải dựng trước*". Kỹ năng là nhìn thấy hai nửa và giao diện giữa
chúng.

## Mẫu hòa trộn

Hầu hết mọi kết hợp có dạng này:

```
đọc dữ liệu → [biến đổi A] → [thuật toán lõi B] → đáp án
```

Các biến đổi chính là nơi kết hợp sống: sắp xếp để greedy hoạt động, nén để
thu nhỏ miền giá trị, dựng đồ thị phụ (trạng thái, tầng thời gian, mạng còn
dư), tiền tính cấu trúc (bảng LCA, sparse table, rừng DSU tiền tố).

## Giao diện chính là thiết kế

Khi hòa tìm kiếm nhị phân với greedy, *giao diện* là một vị từ khả thi
đúng/sai. Khi hòa SCC với DP trên DAG, giao diện là đồ thị cô đặc. Khi hòa
Dijkstra với đồ thị trạng thái, giao diện là định nghĩa trạng thái — định
sai (quá lớn → chết bộ nhớ; quá nhỏ → sai đáp án) thì cả hai nửa gãy.

## Kế toán chi phí cho tổ hợp

Tổng chi phí không phải A + B; thường là A · B hoặc A + B tùy cách lồng:
tìm kiếm nhị phân (log C) × kiểm tra greedy O(n) = O(n log C). Nén
O(n log n) + truy vấn Fenwick O((n+q) log n). Tính ngân sách cho *phép hợp
thành*, không phải từng mảnh.

## Nhận diện: cái gì xứng đáng một cặp kết hợp

- "Tối thiểu hóa giá trị lớn nhất / tối đa hóa giá trị nhỏ nhất" + một cách
  xếp đặt có thể kiểm tra → tìm kiếm nhị phân + greedy (hoặc + ghép đôi).
- Giá trị tới 10^9 nhưng chỉ có n ≤ 2·10^5 giá trị → nén tọa độ, rồi bất cứ
  thứ gì cần miền giá trị (Fenwick trên giá trị, DP trên giá trị).
- Sự kiện theo thứ tự thời gian + câu hỏi liên thông → DSU theo thời gian
  (thêm cạnh theo thứ tự), hoặc cấu trúc persistent/LCT nếu có xóa.
- "Trạng thái" nhiều hơn một vị trí (xăng còn lại, chìa khóa đang giữ, tính
  chẵn lẻ, số xu) → BFS/Dijkstra trên đồ thị tích đề-các. Coi chừng kích
  thước!
- "Nếu có chu trình thì vô nghiệm" → SCC trước, rồi DP trên đồ thị cô đặc.
""",
)

write_lesson(
    M, "hsgx-m4-pairings",
    "The Five Classic Pairings",
    "Worked skeletons of the combinations that appear again and again in HSG sets — each with its interface and its cost.",
    25,
    """
# The Five Classic Pairings

## 1. Binary search + greedy (the answer-is-monotone family)

Interface: `feasible(x)` — a greedy that checks whether target x is
achievable. Cost: O(check · log(range)). Trap: an infeasible-check greedy
must be *provably* optimal for fixed x — "first-fit" is only valid when
items are processed in a fixed order and greed is exchange-argued.

## 2. Coordinate compression + Fenwick (domain shrinking)

Interface: the compressed rank array. Cost: O(n log n) once, then O(log n)
per operation. Appears as: counting inversions, counting pairs with value
conditions, "how many previous elements are ≤ x" online. Trap: compress
*queries too* if they arrive offline and reference values not in the array.

## 3. DSU over time (connectivity with a clock)

Interface: events sorted by time; DSU unions are irreversible, so process
time forward and answer queries that also move forward (or reverse time for
deletions). Cost: near-linear. Appears as: "after each new road, how many
provinces", "earliest moment the graph connects". Trap: queries interleaved
with unions must be answered in the same pass — sorting queries by time and
two-pointering the union list.

## 4. Dijkstra / BFS on a state graph (search with richer nodes)

Interface: state = (position, extra dimension). Cost: O(states · log
states) — you must compute the state count explicitly: grid 1000×1000 × 2
parities = 2·10^6 states, fine; × 10^6 fuel values = dead. Appears as:
shortest path with parity constraint, keys-and-doors, restricted fuel.

## 5. SCC + DAG DP (cycles first, then order)

Interface: the condensation — each SCC collapses to one node with aggregated
weights. Cost: Tarjan/Kosaraju O(n + m), then DP O(n' + m'). Appears as:
"maximum coins collectible with one-way passages, cycles allowed but
pointless inside a component except to bank its total". Trap: the DP must
follow topological order of the *condensation*, not the original graph.

Each pairing has a two-line recognition sentence. If a problem's story maps
to one, write the interface (the predicate, the rank array, the state
definition, the condensation) *before* coding either half.
""",
    "Năm cặp kinh điển",
    "Bộ khung giải mẫu của các kết hợp lặp đi lặp lại trong đề HSG — mỗi cặp với giao diện và chi phí của nó.",
    """
# Năm cặp kinh điển

## 1. Tìm kiếm nhị phân + greedy (họ đáp-án-đơn-điệu)

Giao diện: `feasible(x)` — một greedy kiểm tra mục tiêu x có đạt được không.
Chi phí: O(check · log(range)). Bẫy: greedy kiểm tra phải được chứng minh
*tối ưu* với x cố định — "lấy-first-fit" chỉ hợp lệ khi phần tử xử lý theo
thứ tự cố định và greedy được lập luận đổi chỗ.

## 2. Nén tọa độ + Fenwick (thu nhỏ miền)

Giao diện: mảng hạng đã nén. Chi phí: O(n log n) một lần, rồi O(log n) mỗi
thao tác. Xuất hiện dưới dạng: đếm nghịch thế, đếm cặp theo điều kiện giá
trị, "có bao nhiêu phần tử trước đó ≤ x" trực tuyến. Bẫy: nén cả *truy vấn*
nếu chúng đến offline và tham chiếu giá trị không có trong mảng.

## 3. DSU theo thời gian (liên thông có đồng hồ)

Giao diện: sự kiện đã sắp theo thời gian; các union của DSU không thể đảo
ngược, nên xử lý thời gian xuôi và trả lời các truy vấn cũng đi xuôi (hoặc
đảo thời gian cho phép xóa). Chi phí: gần tuyến tính. Xuất hiện: "sau mỗi
con đường mới, có bao nhiêu tỉnh", "thời điểm sớm nhất đồ thị liên thông".
Bẫy: truy vấn xen kẽ với union phải được trả lời trong cùng một lượt — sort
truy vấn theo thời gian và two-pointer danh sách union.

## 4. Dijkstra / BFS trên đồ thị trạng thái (tìm kiếm với đỉnh giàu hơn)

Giao diện: trạng thái = (vị trí, chiều phụ). Chi phí: O(số trạng thái · log)
— bạn phải tính rõ số trạng thái: lưới 1000×1000 × 2 tính chẵn lẻ = 2·10^6
trạng thái, ổn; × 10^6 mức xăng = chết. Xuất hiện: đường đi ngắn nhất với
ràng buộc chẵn lẻ, chìa khóa và cửa, xăng giới hạn.

## 5. SCC + DP trên DAG (chu trình trước, thứ tự sau)

Giao diện: đồ thị cô đặc — mỗi SCC thu thành một đỉnh với trọng số gộp.
Chi phí: Tarjan/Kosaraju O(n + m), rồi DP O(n' + m'). Xuất hiện: "tối đa số
xu thu được với đường một chiều, có chu trình nhưng vô nghĩa bên trong một
thành phần ngoài việc gộp tổng của nó". Bẫy: DP phải theo thứ tự tô-pô của
*đồ thị cô đặc*, không phải đồ thị gốc.

Mỗi cặp có một câu nhận diện hai dòng. Nếu cốt truyện khớp một câu, hãy viết
giao diện (vị từ, mảng hạng, định nghĩa trạng thái, đồ thị cô đặc) *trước*
khi cài bất kỳ nửa nào.
""",
)

# ----------------------------------------------------------------- practice
# P1: binary search + greedy — aggressive cows style
P1_R = CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    long long lo = 1, hi = a[n - 1] - a[0];
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        long long cnt = 1, last = a[0];
        for (int i = 1; i < n && cnt < k; ++i) {
            if (a[i] - last >= mid) { ++cnt; last = a[i]; }
        }
        if (cnt >= k) lo = mid; else hi = mid - 1;
    }
    out << lo << "{{NL}}";
""") + END

P1_W = CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    // WRONG: average-gap heuristic — place k points at equal average spacing.
    // Deterministically wrong on clustered inputs.
    long long span = a[n - 1] - a[0];
    long long ans = span / max(1, k - 1);
    out << ans << "{{NL}}";
""") + END

# P2: coordinate compression + Fenwick — count pairs a[i] > 2*a[j], i < j
P2_R = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> vals;
    vals.reserve(2 * n);
    for (long long x : a) { vals.push_back(x); vals.push_back(2 * x); }
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    auto rank = [&](long long v) {
        return lower_bound(vals.begin(), vals.end(), v) - vals.begin() + 1;
    };
    int m = (int)vals.size();
    vector<int> bit(m + 1, 0);
    auto upd = [&](int i) { for (; i <= m; i += i & -i) bit[i]++; };
    auto qry = [&](int i) { int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; };
    long long cnt = 0;
    for (int i = n - 1; i >= 0; --i) {
        // inserted j > i: count values 2*a[j] strictly below a[i]
        cnt += qry(rank(a[i]) - 1);
        upd(rank(2 * a[i]));
    }
    out << cnt << "{{NL}}";
""") + END

P2_W = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: O(n^2) nested scan — same answers, times out at n = 200000.
    // The combination (compression + Fenwick) is the whole point.
    long long cnt = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (a[i] > 2 * a[j]) ++cnt;
    out << cnt << "{{NL}}";
""") + END

# P3: DSU over time — components after each road
P3_R = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> par(n + 1), sz(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    // iterative find (path halving)
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    int comp = n;
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        int ru = find(u), rv = find(v);
        if (ru != rv) {
            if (sz[ru] < sz[rv]) swap(ru, rv);
            par[rv] = ru;
            sz[ru] += sz[rv];
            --comp;
        }
        out << comp << "{{NL}}";
    }
""") + END

P3_W = CPP_STD + cpp("""    int n, m; in >> n >> m;
    // WRONG: BFS the whole graph after each road — correct answers but
    // O(n·m) ≈ 2·10^10 at full scale; DSU over time is the point.
    vector<vector<int>> g(n + 1);
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
        vector<int> vis(n + 1, 0);
        int comp = 0;
        for (int s = 1; s <= n; ++s) {
            if (vis[s]) continue;
            ++comp;
            vector<int> st = {s};
            vis[s] = 1;
            while (!st.empty()) {
                int x = st.back(); st.pop_back();
                for (int y : g[x]) if (!vis[y]) { vis[y] = 1; st.push_back(y); }
            }
        }
        out << comp << "{{NL}}";
    }
""") + END

# P4: Dijkstra on state graph — parity-constrained shortest walk
P4_R = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<pair<int,int>>> g(n + 1);
    for (int e = 0; e < m; ++e) {
        int u, v, w; in >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    // state: (vertex, parity of edges used). Min edges-walk with even count.
    const long long INF = 1e18;
    vector<vector<long long>> dist(n + 1, vector<long long>(2, INF));
    priority_queue<tuple<long long,int,int>, vector<tuple<long long,int,int>>, greater<>> pq;
    dist[1][0] = 0;
    pq.push({0, 1, 0});
    while (!pq.empty()) {
        auto [d, u, p] = pq.top(); pq.pop();
        if (d != dist[u][p]) continue;
        for (auto [v, w] : g[u]) {
            int np = p ^ 1;
            if (d + w < dist[v][np]) {
                dist[v][np] = d + w;
                pq.push({d + w, v, np});
            }
        }
    }
    long long ans = dist[n][0];
    out << (ans >= INF ? -1 : ans) << "{{NL}}";
""") + END

P4_W = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<pair<int,int>>> g(n + 1);
    for (int e = 0; e < m; ++e) {
        int u, v, w; in >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    // WRONG: plain Dijkstra from 1 to n ignoring parity — the classic
    // non-state solution. Fails whenever the shortest walk has odd length.
    const long long INF = 1e18;
    vector<long long> dist(n + 1, INF);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[1] = 0;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (d + w < dist[v]) { dist[v] = d + w; pq.push({d + w, v}); }
        }
    }
    out << (dist[n] >= INF ? -1 : dist[n]) << "{{NL}}";
""") + END

# P5: SCC + condensation DP — max coins on one-way passages
P5_R = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    vector<long long> coin(n + 1, 0);
    for (int i = 1; i <= n; ++i) in >> coin[i];
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
    }
    // Tarjan SCC (iterative)
    vector<int> low(n + 1), num(n + 1, 0), comp(n + 1, -1);
    vector<int> stk, path;
    vector<vector<int>> chains(n + 1);
    vector<size_t> it(n + 1, 0);
    int timer = 0, ncomp = 0;
    for (int s = 1; s <= n; ++s) {
        if (num[s]) continue;
        path.push_back(s);
        while (!path.empty()) {
            int u = path.back();
            if (it[u] == 0) { num[u] = low[u] = ++timer; stk.push_back(u); }
            bool advanced = false;
            while (it[u] < g[u].size()) {
                int v = g[u][it[u]++];
                if (!num[v]) { chains[u].push_back(v); path.push_back(v); advanced = true; break; }
                else if (comp[v] < 0) low[u] = min(low[u], num[v]);
            }
            if (!advanced) {
                if (low[u] == num[u]) {
                    ++ncomp;
                    while (true) {
                        int v = stk.back(); stk.pop_back();
                        comp[v] = ncomp;
                        if (v == u) break;
                    }
                }
                path.pop_back();
                if (!path.empty()) {
                    int p = path.back();
                    low[p] = min(low[p], low[u]);
                }
            }
        }
    }
    // condensation: total coins per comp + best DP in reverse topo (comp ids
    // from Tarjan are already reverse-topological: edges go comp[u] -> comp[v]
    // with comp[u] >= comp[v]... actually Tarjan numbers comps in reverse
    // topological order of the condensation, so DP by increasing comp id over
    // reversed edges)
    vector<long long> tot(ncomp + 1, 0);
    for (int v = 1; v <= n; ++v) tot[comp[v]] += coin[v];
    vector<long long> best(ncomp + 1, 0);
    vector<vector<int>> radj(ncomp + 1);
    for (int u = 1; u <= n; ++u)
        for (int v : g[u])
            if (comp[u] != comp[v]) radj[comp[v]].push_back(comp[u]);
    long long ans = 0;
    // Tarjan numbers components in REVERSE topological order of the
    // condensation (sinks get small ids). Edges go comp[u] -> comp[v] with
    // comp[u] > comp[v] for distinct comps, so predecessors have HIGHER ids:
    // DP must run by DESCENDING component id.
    for (int c = ncomp; c >= 1; --c) {
        best[c] = tot[c];
        for (int p : radj[c]) best[c] = max(best[c], tot[c] + best[p]);
        ans = max(ans, best[c]);
    }
    out << ans << "{{NL}}";
""") + END

P5_W = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    vector<long long> coin(n + 1, 0);
    for (int i = 1; i <= n; ++i) in >> coin[i];
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
    }
    // WRONG: longest-path DP on the raw graph assuming it is a DAG —
    // visits nodes multiple times / cycles inflate the count. The tests
    // include cycles whose coins would be double-counted.
    const long long NEG = -1e18;
    vector<long long> best(n + 1, NEG);
    // naive DFS without cycle handling, memoized as if DAG
    vector<long long> memo(n + 1, -1);
    function<long long(int)> dfs = [&](int u) -> long long {
        if (memo[u] != -1) return memo[u];
        long long r = coin[u];
        for (int v : g[u]) r = max(r, coin[u] + dfs(v));
        return memo[u] = r;
    };
    long long ans = 0;
    for (int s = 1; s <= n; ++s) ans = max(ans, dfs(s));
    out << ans << "{{NL}}";
""") + END

# ---- ground truths (defined BEFORE the challenges that reference them)
def _p3_ground():
    n, m = 200000, 300000
    par = list(range(n + 1))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    comp = n
    out = []
    for i in range(1, m + 1):
        u = 1 + (i * 31) % 200000
        v = 1 + (i * 17 + 7) % 200000
        ru, rv = find(u), find(v)
        if ru != rv:
            par[rv] = ru
            comp -= 1
        out.append(comp)
    return out


def _cp4_ground():
    n, m = 200000, 300000
    coin = [(i * 7919) % 1000000000 for i in range(1, 200001)]
    edges = [(1 + (i * 31) % 200000, 1 + (i * 17 + 7) % 200000) for i in range(1, 300001)]
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
    # iterative Tarjan SCC
    index = [0] * (n + 1)
    low = [0] * (n + 1)
    onstk = [False] * (n + 1)
    comp = [-1] * (n + 1)
    stk = []
    ncomp = 0
    timer = 0
    for s in range(1, n + 1):
        if index[s]:
            continue
        work = [(s, 0)]
        while work:
            u, pi = work[-1]
            if pi == 0:
                timer += 1
                index[u] = low[u] = timer
                stk.append(u)
                onstk[u] = True
            adv = False
            while pi < len(g[u]):
                v = g[u][pi]
                pi += 1
                if not index[v]:
                    work[-1] = (u, pi)
                    work.append((v, 0))
                    adv = True
                    break
                elif onstk[v]:
                    low[u] = min(low[u], index[v])
            if adv:
                continue
            work[-1] = (u, pi)
            if low[u] == index[u]:
                ncomp += 1
                while True:
                    v = stk.pop()
                    onstk[v] = False
                    comp[v] = ncomp
                    if v == u:
                        break
            work.pop()
            if work:
                pu = work[-1][0]
                low[pu] = min(low[pu], low[u])
    tot = [0] * (ncomp + 1)
    for v in range(1, n + 1):
        tot[comp[v]] += coin[v - 1]
    radj = [[] for _ in range(ncomp + 1)]
    for u, v in edges:
        if comp[u] != comp[v]:
            radj[comp[v]].append(comp[u])
    best = [0] * (ncomp + 1)
    ans = 0
    for c in range(1, ncomp + 1):
        b = tot[c]
        for p in radj[c]:
            b = max(b, tot[c] + best[p])
        best[c] = b
        ans = max(ans, b)
    return ans


# ---- tests
P1_CH = challenge(
    "hsgx-p4-place", "Spreading the Stations",
    """**Bài toán.** n candidate positions on a line; choose k of them to
maximize the minimum distance between any two chosen positions.

**Constraints:** 2 ≤ k ≤ n ≤ 100000; 0 ≤ a[i] ≤ 10^9.

**Output:** one integer — that maximized minimum distance.
""",
    [
        contest_test("exact fit", T("3 3", "1 5 9"), T("4"),
            "Choose all: min gap 4."),
        contest_test("cluster", T("4 2", "1 2 3 100"), T("99"),
            "1 and 100."),
        contest_test("k equals n", T("5 5", "0 10 20 30 40"), T("10"),
            "All chosen."),
        contest_test("n=100000", T("100000 37") + T(*[str((i * 104729) % 1000000007) for i in range(1, 100001)]), T("27772583"),
            "Full scale; ground truth via an independent binary-search check in Python."),
    ],
    level="combination",
    difficulty="advanced",
)

P2_CH = challenge(
    "hsgx-p4-dominating", "Twice As Small",
    """**Bài toán.** Count the pairs i < j with a[i] > 2·a[j].

**Constraints:** 1 ≤ n ≤ 200000; |a[i]| ≤ 10^9.

**Output:** one integer (64-bit).
""",
    [
        contest_test("none", T("3", "1 2 3"), T("0"),
            "Sorted ascending: nothing dominates."),
        contest_test("simple", T("3", "5 1 2"), T("2"),
            "5>2·1 and 5>2·2 → 2."),
        contest_test("negatives", T("4", "-1 -3 4 1"), T("2"),
            "4>2·1 and 4>2·(-3) → 2."),
        contest_test("n=200000", T("200000") + T(*[str(((i * 6364136223846793005) >> 11) % 2000001 - 1000000) for i in range(1, 200001)]), T("9999988592"),
            "Full scale: O(n²) is 2·10^10 — times out; compression + Fenwick counts in O(n log n). Ground truth in Python via sorted-list bisection."),
    ],
    level="combination",
    difficulty="advanced",
)

P3_CH = challenge(
    "hsgx-p4-roads", "Provinces Under Construction",
    """**Bài toán.** n cities; m roads open one at a time. After each road
opens, print the number of connected groups.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ m ≤ 300000.

**Output:** m lines. Re-scanning the whole graph after every road is far
too slow at full scale.
""",
    [
        contest_test("single road", T("2 1", "1 2"), T("1"),
            "Two cities, one road: one group."),
        contest_test("no merge", T("3 2", "1 2", "1 2"), T("2", "2"),
            "Duplicate road: no change."),
        contest_test("chain", T("4 3", "1 2", "3 4", "2 3"), T("3", "2", "1"),
            "Groups shrink 3 → 2 → 1."),
        contest_test("full scale", T("200000 300000") + T(*["%d %d" % (1 + (i * 31) % 200000, 1 + (i * 17 + 7) % 200000) for i in range(1, 300001)]), T(*["%d" % c for c in _p3_ground()]),
            "Full scale: O(n·m) BFS would be 6·10^10 — times out. Ground truth computed by an independent DSU simulation in Python."),
    ],
    level="combination",
    difficulty="advanced",
)

P4_CH = challenge(
    "hsgx-p4-parity", "Even Number of Tolls",
    """**Bài toán.** Undirected weighted graph; find the minimum-cost walk from
1 to n that uses an **even number of edges** (revisiting allowed).

**Constraints:** 1 ≤ n ≤ 100000; 1 ≤ m ≤ 200000; 1 ≤ w ≤ 10^9.

**Output:** the minimum cost, or −1 if impossible.
""",
    [
        contest_test("single edge", T("2 1", "1 2 5"), T("-1"),
            "Two vertices: any walk 1→2 uses an odd number of edges — impossible."),
        contest_test("triangle flip", T("3 3", "1 2 5", "2 3 1", "1 3 1"), T("6"),
            "Best even walk: 1→2→3 (2 edges, cost 6). Plain Dijkstra answers 1 (odd walk 1→3)."),
        contest_test("detour cheaper", T("4 4", "1 2 1", "2 3 1", "3 4 1", "1 3 1"), T("2"),
            "1→3→4: 2 edges, cost 2. The plain shortest walk 1→2→3→4 has 3 edges (odd)."),
        contest_test("impossible mixed", T("4 3", "1 2 1", "2 3 1", "3 4 1"), T("-1"),
            "A path is bipartite {1,3},{2,4}: even walks from 1 never reach 4."),
    ],
    level="combination",
    difficulty="advanced",
)

P5_CH = challenge(
    "hsgx-p5-coins", "Coin Corridors",
    """**Bài toán.** One-way corridors between n rooms; room i holds coin[i].
Walking a corridor is free. Starting anywhere, collect coins of every room
you enter (each room counts once per visit-route). Maximize coins collected
along one route.

**Constraints:** 1 ≤ n ≤ 100000; 1 ≤ m ≤ 200000; 0 ≤ coin ≤ 10^9. Cycles
may exist.

**Output:** one integer.
""",
    [
        contest_test("chain", T("3 2", "1 2 3", "1 2", "2 3"), T("6"),
            "1→2→3 collects all."),
        contest_test("cycle", T("3 3", "1 2 3", "1 2", "2 3", "3 1"), T("6"),
            "Cycle banks the whole component once."),
        contest_test("two components", T("4 2", "5 6 7 8", "1 2", "3 4"), T("15"),
            "Best single route is 7+8."),
        contest_test("cycle plus tail", T("4 4", "1 2 3 100", "1 2", "2 1", "2 3", "3 4"), T("106"),
            "Bank cycle {1,2} = 3, then 3, then 4: 1+2+3+100 = 106."),
    ],
    level="combination",
    difficulty="advanced",
)

write_practice(
    M, "hsgx-p4-combos", "Combination Drill — Five Fusions",
    "Five problems, each needing two tools fused. Topic names withheld; the wrong solutions are the single-tool answers.",
    "Drill kết hợp — Năm phép hòa trộn",
    "Năm bài, mỗi bài cần hai công cụ hòa làm một. Không nêu tên chủ đề; các lời giải sai là lời giải một-công-cụ.",
    "hsgx-m4-pairings",
    100,
    "advanced",
    [P1_CH, P2_CH, P3_CH, P4_CH, P5_CH],
    {
        "hsgx-p4-place": vi_challenge(
            "Rải trạm quan sát",
            "**Bài toán.** n vị trí ứng viên trên một đường thẳng; chọn k vị trí để tối đa hóa khoảng cách nhỏ nhất giữa hai vị trí được chọn.",
            [("chọn vừa đủ", "Chọn cả ba: khoảng cách nhỏ nhất 4."),
             ("cụm dày", "Chọn 1 và 100."),
             ("k bằng n", "Chọn hết."),
             ("n=100000", "Đối chiếu ground truth bằng tìm kiếm nhị phân độc lập trong Python.")],
        ),
        "hsgx-p4-dominating": vi_challenge(
            "Nhỏ gấp đôi bị át",
            "**Bài toán.** Đếm các cặp i < j với a[i] > 2·a[j].",
            [("không có", "Tăng dần: không cặp nào."),
            ("đơn giản", "5>2·1 và 5>2·2 → 2."),
             ("số âm", "4>2·1 và 4>2·(−3) → 2."),
             ("n=200000", "O(n²) là 2·10^10 — quá thời gian; nén + Fenwick đếm O(n log n). Ground truth bằng bisection trong Python.")],
        ),
        "hsgx-p4-roads": vi_challenge(
            "Tỉnh đang xây",
            "**Bài toán.** n thành phố; m con đường mở dần. Sau mỗi con đường, in số nhóm liên thông.",
            [("một con đường", "Hai thành phố nối nhau: một nhóm."),
             ("không gộp", "Đường trùng: không đổi."),
             ("chuỗi", "Nhóm giảm 3 → 2 → 1."),
             ("đúng giới hạn", "O(n·m) BFS sẽ là 6·10^10 — quá thời gian. Ground truth bằng mô phỏng DSU độc lập trong Python.")],
        ),
        "hsgx-p4-parity": vi_challenge(
            "Số trạm thu phí chẵn",
            "**Bài toán.** Đồ thị vô hướng có trọng số; tìm đường đi chi phí nhỏ nhất từ 1 tới n qua **số cạnh chẵn** (được quay lại).",
            [("một cạnh", "Hai đỉnh: mọi đường 1→2 đều lẻ số cạnh — vô nghiệm."),
             ("tam giác lật chẵn lẻ", "Đường chẵn tốt nhất: 1→2→3 (2 cạnh, chi phí 6). Dijkstra thường trả 1 (đường lẻ 1→3)."),
             ("đường vòng rẻ hơn", "1→3→4: 2 cạnh, chi phí 2. Đường ngắn thường 1→2→3→4 có 3 cạnh (lẻ)."),
             ("vô nghiệm kiểu đường", "Đường đi là hai phía {1,3},{2,4}: đường chẵn từ 1 không bao giờ tới 4.")],
        ),
        "hsgx-p5-coins": vi_challenge(
            "Hành lang xu",
            "**Bài toán.** Hành lang một chiều giữa n phòng; phòng i có coin[i]. Xuất phát bất kỳ, thu xu của mỗi phòng đi qua (mỗi phòng tính một lần mỗi lộ trình). Tối đa hóa số xu.",
            [("chuỗi", "1→2→3 thu hết: 6."),
             ("chu trình", "Chu trình gộp cả thành phần một lần: 6."),
             ("hai thành phần", "Lộ trình tốt nhất là 7+8."),
             ("chu trình + đuôi", "Gộp chu trình {1,2} = 3, rồi 3, rồi 100: tổng 106.")],
        ),
    },
    solutions=[
        ("hsgx-p4-place", P1_R, P1_W),
        ("hsgx-p4-dominating", P2_R, P2_W),
        ("hsgx-p4-roads", P3_R, P3_W),
        ("hsgx-p4-parity", P4_R, P4_W),
        ("hsgx-p5-coins", P5_R, P5_W),
    ],
)

# --------------------------------------------------------------- checkpoint
# SCC + DAG DP executed at scale, plus the state-graph idea (parity) as tests.
CP_M4_R = P5_R
CP_M4_W = P5_W

CP_CH = challenge(
    "hsgx-cp-m4-coinroads", "Checkpoint — Coin Corridors at Scale",
    """**Bài toán.** Same as the practice problem: one-way corridors, per-room
coins, cycles allowed; maximize coins along one route from any start.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ m ≤ 300000; 0 ≤ coin ≤ 10^9.

**Output:** one integer. A DAG-assuming DP will produce wrong (inflated)
answers on cyclic inputs; the cycles must be collapsed first.
""",
    [(t["name"], t["code"], t["hint"]) for t in P5_CH["tests"][:3]] + [
        contest_test("n=200000 cycle chain", T("200000 300000", " ".join(str((i * 7919) % 1000000000) for i in range(1, 200001))) + T(*["%d %d" % (1 + (i * 31) % 200000, 1 + (i * 17 + 7) % 200000) for i in range(1, 300001)]), T(str(_cp4_ground())),
            "Full scale with heavy edge overlap (cycles everywhere); ground truth via an independent SCC + DP computation in Python."),
    ],
    level="combination",
    difficulty="advanced",
)

def _cp4_ground():
    import sys
    sys.setrecursionlimit(300000)
    n, m = 200000, 300000
    coin = [(i * 7919) % 1000000000 for i in range(1, 200001)]
    edges = [(1 + (i * 31) % 200000, 1 + (i * 17 + 7) % 200000) for i in range(1, 300001)]
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
    # iterative Tarjan
    index = [0] * (n + 1)
    low = [0] * (n + 1)
    onstk = [False] * (n + 1)
    comp = [-1] * (n + 1)
    stk = []
    ncomp = 0
    timer = 0
    for s in range(1, n + 1):
        if index[s]:
            continue
        work = [(s, 0)]
        while work:
            u, pi = work[-1]
            if pi == 0:
                timer += 1
                index[u] = low[u] = timer
                stk.append(u)
                onstk[u] = True
            adv = False
            while pi < len(g[u]):
                v = g[u][pi]
                pi += 1
                if not index[v]:
                    work[-1] = (u, pi)
                    work.append((v, 0))
                    adv = True
                    break
                elif onstk[v]:
                    low[u] = min(low[u], index[v])
            if adv:
                continue
            work[-1] = (u, pi)
            if low[u] == index[u]:
                ncomp += 1
                while True:
                    v = stk.pop()
                    onstk[v] = False
                    comp[v] = ncomp
                    if v == u:
                        break
            work.pop()
            if work:
                pu = work[-1][0]
                low[pu] = min(low[pu], low[u])
    tot = [0] * (ncomp + 1)
    for v in range(1, n + 1):
        tot[comp[v]] += coin[v - 1]
    radj = [[] for _ in range(ncomp + 1)]
    for u, v in edges:
        if comp[u] != comp[v]:
            radj[comp[v]].append(comp[u])
    best = [0] * (ncomp + 1)
    ans = 0
    for c in range(1, ncomp + 1):
        b = tot[c]
        for p in radj[c]:
            b = max(b, tot[c] + best[p])
        best[c] = b
        ans = max(ans, b)
    return ans

write_checkpoint(
    M, "hsgx-cp-m4", "Checkpoint — Collapse, Then Walk",
    "The fusion executed at scale: collapse cycles into components, then DP the condensation. A DAG-assuming DP inflates cyclic inputs — that inflation is the graded failure.",
    20,
    """
**Điểm kiểm tra — Cô đặc, rồi đi.** One-way corridors with coins, cycles
allowed, n ≤ 200000. The correct route: find strongly connected components,
bank each component's coins, then DP over the condensation. The plausible
wrong answer runs a longest-path DP assuming a DAG — on cyclic inputs it
double-counts. Deterministic wrong-side failure, verified.
""",
    "Điểm kiểm tra — Cô đặc, rồi đi",
    "Hòa trộn ở đúng giới hạn: hành lang một chiều có xu, cho phép chu trình, n ≤ 200000. Đường đúng: tìm thành phần liên thông mạnh, gộp xu từng thành phần, rồi DP trên đồ thị cô đặc. Đáp án sai nghe hợp lý là DP đường đi dài nhất giả định DAG — trên đầu vào có chu trình nó đếm trùng.",
    """
**Điểm kiểm tra — Cô đặc, rồi đi.** Hành lang một chiều có xu, cho phép
chu trình, n ≤ 200000. Đường đúng: tìm thành phần liên thông mạnh, gộp xu
từng thành phần, rồi DP trên đồ thị cô đặc. Đáp án sai nghe hợp lý là DP
đường đi dài nhất giả định DAG — trên đầu vào có chu trình nó đếm trùng.
""",
    CP_CH,
    vi_challenge(
        "Điểm kiểm tra — Hành lang xu ở đúng giới hạn",
        "**Bài toán.** Hành lang một chiều có xu, cho phép chu trình, n ≤ 200000. Tối đa hóa xu trên một lộ trình. DP giả định DAG sẽ đếm trùng trên đầu vào có chu trình.",
        [("chuỗi", "1→2→3 thu hết: 6."),
         ("chu trình", "Chu trình gộp cả thành phần một lần: 6."),
         ("hai thành phần", "Lộ trình tốt nhất là 7+8."),
         ("n=200000 chu trình dày", "Đúng giới hạn với chồng lấn cạnh lớn; ground truth bằng SCC + DP độc lập trong Python.")],
    ),
    CP_M4_R,
    CP_M4_W,
)

print("module m4 complete")
