#!/usr/bin/env python3
"""HSG Advanced — Module 9: hsga-flow (Max Flow & Matching).

Flow modeling, residual graphs, Edmonds–Karp on small graphs, Dinic on
the load test, bipartite matching as flow, and min-cut reading. Wrong
solutions: greedy path pushing without back-edges (behavioral) and
Edmonds–Karp on the Dinic-scale load (near-miss timeout).

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
#include <queue>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-flow"


# ---------------------------------------------------------------- models
def _maxflow(n, edges, s, t):
    cap = {}
    adj = [[] for _ in range(n + 1)]
    for u, v, c in edges:
        if (u, v) not in cap:
            cap[(u, v)] = 0
            adj[u].append(v)
        if (v, u) not in cap:
            cap[(v, u)] = 0
            adj[v].append(u)
        cap[(u, v)] += c
    flow = 0
    while True:
        par = [0] * (n + 1)
        par[s] = s
        q = [s]
        while q and not par[t]:
            nq = []
            for u in q:
                for v in adj[u]:
                    if not par[v] and cap.get((u, v), 0) > 0:
                        par[v] = u
                        nq.append(v)
            q = nq
        if not par[t]:
            break
        b = None
        v = t
        while v != s:
            u = par[v]
            c = cap[(u, v)]
            b = c if b is None else min(b, c)
            v = u
        v = t
        while v != s:
            u = par[v]
            cap[(u, v)] -= b
            cap[(v, u)] += b
            v = u
        flow += b
    return flow


# ---------------------------------------------------------------- lessons
write_module(
    M,
    "Max Flow and Matching",
    "Model capacities as networks, augment along BFS shortest paths, and read the min cut out of the final residual graph — bipartite matching included as a special case.",
    "Luồng cực đại và ghép cặp",
    "Mô hình hóa năng lực thành mạng, tăng_flow theo đường BFS ngắn nhất, đọc min-cut từ đồ thị dư cuối — ghép cặp hai phía là trường hợp đặc biệt.",
    ["hsga-m9-network", "hsga-m9-augment", "hsga-m9-modeling", "hsga-cp-m9"],
    ["hsga-p9-flow"],
)

write_lesson(
    M, "hsga-m9-network",
    "Networks and Residual Graphs",
    "Capacities on edges, an equal-and-opposite residual edge on every arc — the data structure that makes 'undo' legal and guarantees termination.",
    35,
    """
# The residual trick

Every edge (u, v, c) becomes TWO arcs: forward with capacity c, backward
with capacity 0. Pushing f units along u→v does: cap(u→v) -= f,
cap(v→u) += f. The backward arc is the UNDO button — a later path may
"cancel" earlier flow, which is exactly why greedy pushing without
back-edges is wrong (the A1 wrong solution below demonstrates).

Termination is not obvious: Ford–Fulkerson with integer capacities adds
at least 1 unit per augmentation, so it terminates — but Edmonds–Karp
(BFS shortest augmenting path) also guarantees O(V·E) augmentations.
That is the bound that makes flow polynomial.
""",
    "Mạng và đồ thị dư",
    "Năng lực trên cạnh, một cạnh dư ngược chiều trên mỗi cung — cấu trúc dữ liệu biến 'hoàn tác' thành hợp lệ và đảm bảo dừng.",
    """
# Mẹo đồ thị dư

Mỗi cạnh (u, v, c) thành HAI cung: xuôi với năng lực c, ngược với năng
lực 0. Đẩy f đơn vị theo u→v: cap(u→v) -= f, cap(v→u) += f. Cung ngược
là NÚT HOÀN TÁC — đường đi sau có thể "hủy" luồng trước, và đó chính là
lý do đẩy tham lam không có cạnh ngược là sai (bản sai của A1 bên dưới
chứng minh bằng test).

Việc dừng không hiển nhiên: Ford–Fulkerson với năng lực nguyên cộng ít
nhất 1 đơn vị mỗi lần tăng nên dừng — nhưng Edmonds–Karp (đường tăng
BFS ngắn nhất) còn đảm bảo O(V·E) lần tăng. Chặn đó làm luồng thành đa
thức.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m9-augment",
    "Augmenting Paths and the Min Cut",
    "BFS finds the shortest augmenting path; when none remains, the reachable set from s IS the min cut — flow value equals cut capacity, always.",
    35,
    """
# From augmentations to the cut

Edmonds–Karp: BFS the residual graph s→t, push the bottleneck, repeat.
When BFS finds no path, let S = nodes reachable from s. Every original
edge S→(not S) is saturated and every (not S)→S edge is empty — so the
cut capacity equals the flow value. Max-flow = min-cut is not a slogan;
it falls out of this final state.

For the sandbox: Dinic (BFS level graph + DFS blocking flow) is the
default for n, m up to a few hundred thousand. Edmonds–Karp is fine for
teaching and for m ≤ a few thousand — the A3 wrong solution shows it
dying on the Dinic-scale load.
""",
    "Đường tăng và lát cắt nhỏ nhất",
    "BFS tìm đường tăng ngắn nhất; khi không còn đường, tập với được từ s CHÍNH là min-cut — giá trị luồng bằng năng lực lát cắt, luôn vậy.",
    """
# Từ đường tăng đến lát cắt

Edmonds–Karp: BFS đồ thị dư s→t, đẩy nút thắt, lặp. Khi BFS hết đường,
gọi S = các nút với được từ s. Mọi cạnh gốc S→(ngoài S) đã bão hòa và
mọi cạnh (ngoài S)→S trống rỗng — năng lực lát cắt bằng giá trị luồng.
Max-flow = min-cut không phải khẩu hiệu; nó rơi ra khỏi trạng thái cuối
này.

Trong sandbox: Dinic (BFS đồ thị mức + DFS blocking flow) là mặc định
cho n, m tới vài trăm nghìn. Edmonds–Karp ổn để dạy và cho m tới vài
nghìn — bản sai của A3 cho thấy nó chết trên tải cỡ Dinic.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m9-modeling",
    "Modeling Problems as Flow",
    "Bipartite matching is source→left→right→sink with unit caps; node capacities split nodes; the modeling IS the algorithm choice.",
    35,
    """
# Seeing networks everywhere

- Bipartite matching: source→each left node (cap 1), left→right per the
  compatibility edges (cap 1), each right→sink (cap 1). Max flow = max
  matching; the matched edges are the saturated middle arcs.
- Node capacity c: split v into v_in→v_out with cap c.
- Multi-source/multi-sink: one super-source, one super-sink.
- 'How many disjoint x-y paths' = flow with all caps 1 (vertex-disjoint:
  also split nodes).

The exam skill is recognizing capacity structure in word problems — the
Dinic implementation is boilerplate by comparison.
""",
    "Mô hình hóa bài toán thành luồng",
    "Ghép cặp hai phía là source→trái→phải→sink với năng lực 1; năng lực đỉnh thì tách đỉnh; việc mô hình hóa CHÍNH là lựa chọn thuật toán.",
    """
# Nhìn thấy mạng ở khắp nơi

- Ghép cặp hai phía: source→mỗi đỉnh trái (cap 1), trái→phải theo các
  cạnh tương thích (cap 1), mỗi đỉnh phải→sink (cap 1). Max flow = ghép
  cực đại; các cạnh khớp là các cung giữa đã bão hòa.
- Năng lực đỉnh c: tách v thành v_in→v_out với cap c.
- Nhiều nguồn/nhiều bể: một siêu nguồn, một siêu bể.
- 'Bao nhiêu đường đi không giao nhau x-y' = luồng với mọi cap 1
  (không giao nhau ở đỉnh: tách đỉnh thêm).

Kỹ năng thi là nhận cấu trúc năng lực trong đề chữ — cài Dinic chỉ là
boilerplate bên cạnh.
""",
    difficulty="advanced",
)

# ------------------------------------------------------------ practice R/W
# A1: max flow value, small graphs. Input: n m s t; m lines u v c.
A1_R = CPP_STD + cpp("""
    int n, m, s, t; in >> n >> m >> s >> t;
    vector<long long> cap(2 * m, 0);
    vector<vector<int>> g(n + 1);
    vector<int> to(2 * m, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; long long c; in >> u >> v >> c;
        to[2*i] = v; cap[2*i] = c; g[u].push_back(2*i);
        to[2*i+1] = u; cap[2*i+1] = 0; g[v].push_back(2*i+1);
    }
    long long flow = 0;
    while (true) {
        // BFS
        vector<int> par(n + 1, -1), pedge(n + 1, -1);
        par[s] = s;
        queue<int> q; q.push(s);
        while (!q.empty() && par[t] == -1) {
            int u = q.front(); q.pop();
            for (int e : g[u]) {
                if (cap[e] > 0 && par[to[e]] == -1) {
                    par[to[e]] = u; pedge[to[e]] = e; q.push(to[e]);
                }
            }
        }
        if (par[t] == -1) break;
        long long b = LLONG_MAX;
        for (int v = t; v != s; v = par[v]) b = min(b, cap[pedge[v]]);
        for (int v = t; v != s; v = par[v]) { cap[pedge[v]] -= b; cap[pedge[v]^1] += b; }
        flow += b;
    }
    out << flow << "{{NL}}";
""") + END

# A1 W: greedy DFS pushing without residual back-edges — succeeds on the
# acyclic happy path, fails whenever cancellation is needed.
A1_W = CPP_STD + cpp("""
    int n, m, s, t; in >> n >> m >> s >> t;
    vector<long long> cap(2 * m, 0);
    vector<vector<int>> g(n + 1);
    vector<int> to(2 * m, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; long long c; in >> u >> v >> c;
        to[2*i] = v; cap[2*i] = c; g[u].push_back(2*i);
        to[2*i+1] = u; cap[2*i+1] = 0; g[v].push_back(2*i+1);
    }
    // WRONG: single DFS each round that only ever walks FORWARD arcs —
    // residual back-edges are banned, so once a greedy path saturates the
    // wrong edge the flow can never be cancelled (no undo).
    long long flow = 0;
    while (true) {
        vector<int> par(n + 1, -1), pedge(n + 1, -1);
        // DFS with residual-arc ban
        vector<char> vis(n + 1, 0);
        vector<int> st; st.push_back(s); vis[s] = 1;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            if (u == t) break;
            for (int e : g[u]) {
                int v = to[e];
                if (cap[e] > 0 && !vis[v] && e % 2 == 0) {
                    vis[v] = 1; par[v] = u; pedge[v] = e; st.push_back(v);
                }
            }
        }
        if (par[t] == -1) break;
        long long b = LLONG_MAX;
        for (int v = t; v != s; v = par[v]) b = min(b, cap[pedge[v]]);
        for (int v = t; v != s; v = par[v]) cap[pedge[v]] -= b;
        flow += b;
    }
    out << flow << "{{NL}}";
""") + END

# A2: bipartite matching size via flow. Input: L R m; m lines u v (u in
# left 1..L, v in right 1..R). Print matching size.
A2_R = CPP_STD + cpp("""
    int L, R, m; in >> L >> R >> m;
    int s = L + R + 1, t = L + R + 2, N = L + R + 2;
    vector<long long> cap(2 * (m + L + R), 0);
    vector<vector<int>> g(N + 1);
    vector<int> to(2 * (m + L + R), 0);
    int e = 0;
    auto add = [&](int u, int v, long long c) {
        to[e] = v; cap[e] = c; g[u].push_back(e); ++e;
        to[e] = u; cap[e] = 0; g[v].push_back(e); ++e;
    };
    for (int i = 0; i < m; ++i) { int u, v; in >> u >> v; add(u, L + v, 1); }
    for (int u = 1; u <= L; ++u) add(s, u, 1);
    for (int v = 1; v <= R; ++v) add(L + v, t, 1);
    long long flow = 0;
    while (true) {
        vector<int> par(N + 1, -1), pedge(N + 1, -1);
        par[s] = s;
        queue<int> q; q.push(s);
        while (!q.empty() && par[t] == -1) {
            int u = q.front(); q.pop();
            for (int ei : g[u]) {
                if (cap[ei] > 0 && par[to[ei]] == -1) {
                    par[to[ei]] = u; pedge[to[ei]] = ei; q.push(to[ei]);
                }
            }
        }
        if (par[t] == -1) break;
        long long b = LLONG_MAX;
        for (int v = t; v != s; v = par[v]) b = min(b, cap[pedge[v]]);
        for (int v = t; v != s; v = par[v]) { cap[pedge[v]] -= b; cap[pedge[v]^1] += b; }
        flow += b;
    }
    out << flow << "{{NL}}";
""") + END

# A2 W: greedy matching (first free partner per left node, no augmenting) —
# fails whenever augmenting paths exist.
A2_W = CPP_STD + cpp("""
    int L, R, m; in >> L >> R >> m;
    vector<vector<int>> cand(L + 1);
    for (int i = 0; i < m; ++i) { int u, v; in >> u >> v; cand[u].push_back(v); }
    // WRONG: greedy — each left node takes its first free right neighbor.
    vector<char> usedR(R + 1, 0);
    long long match = 0;
    for (int u = 1; u <= L; ++u) {
        for (int v : cand[u]) {
            if (!usedR[v]) { usedR[v] = 1; ++match; break; }
        }
    }
    out << match << "{{NL}}";
""") + END

# A3: Dinic on the load test — grid-ish layered graph, big flow.
A3_R = CPP_STD + cpp("""
    int n, m, s, t; in >> n >> m >> s >> t;
    vector<long long> cap(2 * m, 0);
    vector<vector<int>> g(n + 1);
    vector<int> to(2 * m, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; long long c; in >> u >> v >> c;
        to[2*i] = v; cap[2*i] = c; g[u].push_back(2*i);
        to[2*i+1] = u; cap[2*i+1] = 0; g[v].push_back(2*i+1);
    }
    vector<int> level(n + 1, -1), it(n + 1, 0);
    auto bfs = [&]() {
        fill(level.begin(), level.end(), -1);
        level[s] = 0;
        queue<int> q; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int e : g[u]) if (cap[e] > 0 && level[to[e]] == -1) {
                level[to[e]] = level[u] + 1; q.push(to[e]);
            }
        }
        return level[t] != -1;
    };
    auto dfs = [&](auto&& self, int u, long long f) -> long long {
        if (u == t) return f;
        for (int& i = it[u]; i < (int)g[u].size(); ++i) {
            int e = g[u][i], v = to[e];
            if (cap[e] > 0 && level[v] == level[u] + 1) {
                long long d = self(self, v, min(f, cap[e]));
                if (d > 0) { cap[e] -= d; cap[e^1] += d; return d; }
            }
        }
        return 0;
    };
    long long flow = 0;
    while (bfs()) {
        fill(it.begin(), it.end(), 0);
        while (long long d = dfs(dfs, s, LLONG_MAX)) flow += d;
    }
    out << flow << "{{NL}}";
""") + END

# A3 W (near-miss): Edmonds–Karp BFS on the Dinic-scale load — many
# augmentations, each O(m): TIMEOUT.
A3_W = CPP_STD + cpp("""
    int n, m, s, t; in >> n >> m >> s >> t;
    vector<long long> cap(2 * m, 0);
    vector<vector<int>> g(n + 1);
    vector<int> to(2 * m, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; long long c; in >> u >> v >> c;
        to[2*i] = v; cap[2*i] = c; g[u].push_back(2*i);
        to[2*i+1] = u; cap[2*i+1] = 0; g[v].push_back(2*i+1);
    }
    long long flow = 0;
    while (true) {
        vector<int> par(n + 1, -1), pedge(n + 1, -1);
        par[s] = s;
        queue<int> q; q.push(s);
        while (!q.empty() && par[t] == -1) {
            int u = q.front(); q.pop();
            for (int e : g[u]) {
                if (cap[e] > 0 && par[to[e]] == -1) {
                    par[to[e]] = u; pedge[to[e]] = e; q.push(to[e]);
                }
            }
        }
        if (par[t] == -1) break;
        long long b = LLONG_MAX;
        for (int v = t; v != s; v = par[v]) b = min(b, cap[pedge[v]]);
        // push ONE unit per round (wrong: bottleneck split into unit pushes)
        b = 1;
        for (int v = t; v != s; v = par[v]) { cap[pedge[v]] -= b; cap[pedge[v]^1] += b; }
        flow += b;
    }
    out << flow << "{{NL}}";
""") + END

# CP: model a word problem — cross edges min cut. A layered graph where the
# answer is max flow; input n m s t with capacities.
CP_M9_R = A3_R
CP_M9_W = CPP_STD + cpp("""
    // WRONG: prints the capacity of the widest single s-t path (a variant of
    // the widest-path greedy) — overestimates whenever the min cut < widest path.
    int n, m, s, t; in >> n >> m >> s >> t;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; long long c; in >> u >> v >> c;
        g[u].push_back({v, c});
    }
    // widest path: max over paths of min edge
    vector<long long> best(n + 1, -1);
    priority_queue<pair<long long, int>> pq;
    best[s] = LLONG_MAX;
    pq.push({LLONG_MAX, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d < best[u]) continue;
        for (auto& [v, c] : g[u]) {
            long long nd = min(d, c);
            if (nd > best[v]) { best[v] = nd; pq.push({nd, v}); }
        }
    }
    out << (best[t] == LLONG_MAX ? best[t] : best[t]) << "{{NL}}";
""") + END


# ----------------------------------------------------------------- tests
def _flow_input(n, edges, s, t):
    lines = ["%d %d %d %d" % (n, len(edges), s, t)]
    lines += ["%d %d %d" % (u, v, c) for (u, v, c) in edges]
    return T(*lines)


def _match_input(L, R, edges):
    lines = ["%d %d %d" % (L, R, len(edges))]
    lines += ["%d %d" % (u, v) for (u, v) in edges]
    return T(*lines)


A1_TESTS = [
    contest_test(
        "classic diamond",
        _flow_input(4, [(1, 2, 2), (1, 3, 2), (2, 4, 2), (3, 4, 2), (2, 3, 1)], 1, 4),
        T("4"),
        "Two parallel 2-routes plus the crossing edge: max flow 4 — the crossing edge is never needed."),
    contest_test(
        "cancellation required",
        _flow_input(4, [(1, 2, 1), (1, 3, 1), (2, 3, 1), (2, 4, 1), (3, 4, 1)], 1, 4),
        T("2"),
        "A greedy first-path push saturates 1->2 the wrong way; residual back-edges fix it. Answer 2."),
    contest_test(
        "bottleneck chain",
        _flow_input(4, [(1, 2, 3), (2, 3, 2), (3, 4, 3)], 1, 4),
        T("2"),
        "The middle edge caps everything: 2."),
    contest_test(
        "disconnected sink",
        _flow_input(5, [(1, 2, 5), (4, 5, 5)], 1, 5),
        T("0"),
        "No s-t connection: flow 0."),
    contest_test(
        "augmenting path required",
        _flow_input(4, [(1, 2, 1), (1, 3, 1), (3, 4, 1), (3, 2, 1), (2, 4, 1)], 1, 4),
        T("2"),
        "Greedy DFS takes s→b→a→t first, saturating a→t; only the residual arc can reroute to s→a→t + s→b→t = 2. Without residual arcs the answer stays 1."),
    contest_test(
        "two disjoint paths, one stolen middle",
        _flow_input(7, [(1, 5, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (3, 6, 1), (4, 7, 1), (5, 6, 1), (6, 7, 1)], 1, 7),
        T("2"),
        "Max flow 2: 1→2→3→4→7 and 1→5→6→7 are edge-disjoint. A no-residual DFS crosses onto the second route via 3→6 and saturates 6→7, stranding both: it reports 1. Only the residual arc can cancel 3→6's unit and reroute it through 3→4."),
]

A2_TESTS = [
    contest_test(
        "perfect matching",
        _match_input(3, 3, [(1, 1), (1, 2), (2, 2), (3, 3)]),
        T("3"),
        "Everyone matched: size 3."),
    contest_test(
        "greedy undercounts: shared neighbor taken first",
        _match_input(2, 2, [(1, 1), (1, 2), (2, 1)]),
        T("2"),
        "Greedy: left1 takes right1, left2's only neighbor right1 is used → 1. Augmenting path rematches left1→right2: max 2."),
    contest_test(
        "greedy undercounts: chain of steals",
        _match_input(3, 3, [(1, 1), (1, 2), (2, 1), (3, 3)]),
        T("3"),
        "Greedy: 1→1, 2 blocked (right1 used), 3→3 → 2. Augmenting rematches 1→2: 3."),
    contest_test(
        "imperfect ceiling",
        _match_input(3, 3, [(1, 1), (2, 1), (3, 1)]),
        T("1"),
        "All three left nodes only reach right1: matching ceiling 1 — flow and greedy agree here."),
]

# Layered load: 3 layers, injective L1→L2 mapping, all caps 5 — analytic
# min-cut answer (s→L1 cut = L2→t cut = 5·49999).
_cp_edges = []
_n = 100000
_L1 = list(range(2, 2 + (_n - 2) // 2))
_L2 = list(range(2 + len(_L1), _n))
for u in _L1:
    _cp_edges.append((1, u, 5))
for u in _L1:
    _cp_edges.append((u, _L2[u % len(_L2)], 5))
for v in _L2:
    _cp_edges.append((v, _n, 5))

CP_TESTS = [
    contest_test(
        "small layered net",
        _flow_input(4, [(1, 2, 3), (2, 4, 2), (1, 3, 2), (3, 4, 3)], 1, 4),
        T("4"),
        "Two routes: 1-2-4 capped 2 and 1-3-4 capped 2 — flow 4, cut edges (1,2)+(1,3) also 4."),
    contest_test(
        "load: layered graph 100k nodes",
        _flow_input(_n, _cp_edges, 1, _n),
        T("249995"),
        "Layered network, analytic answer: the s→L1 cut (5·49999) equals the L2→t cut, so the flow is 249995."),
]

# A3 uses the same load shape
A3_TESTS = [
    contest_test(
        "small sanity",
        _flow_input(4, [(1, 2, 3), (2, 3, 2), (3, 4, 3)], 1, 4),
        T("2"),
        "Bottleneck chain: Dinic answers 2."),
    contest_test(
        "layered load 100k",
        _flow_input(_n, _cp_edges, 1, _n),
        T("249995"),
        "Same analytic min-cut answer as the checkpoint load: 5*49999."),
]

# ----------------------------------------------------------------- emit
write_lesson(
    M, "hsga-m9-network",
    "Networks and Residual Graphs",
    "Capacities on edges, an equal-and-opposite residual edge on every arc — the data structure that makes 'undo' legal and guarantees termination.",
    35,
    """
# The residual trick

Every edge (u, v, c) becomes TWO arcs: forward with capacity c, backward
with capacity 0. Pushing f units along u→v: cap(u→v) -= f, cap(v→u) +=
f. The backward arc is the UNDO button — later paths may cancel earlier
flow, which is exactly why greedy pushing without back-edges is wrong.

Termination: Edmonds–Karp (BFS shortest augmenting path) guarantees
O(V·E) augmentations — the bound that makes flow polynomial.
""",
    "Mạng và đồ thị dư",
    "Năng lực trên cạnh, một cạnh dư ngược chiều trên mỗi cung — cấu trúc dữ liệu biến 'hoàn tác' thành hợp lệ và đảm bảo dừng.",
    """
# Mẹo đồ thị dư

Mỗi cạnh (u, v, c) thành HAI cung: xuôi năng lực c, ngược năng lực 0.
Đẩy f đơn vị theo u→v: cap(u→v) -= f, cap(v→u) += f. Cung ngược là NÚT
HOÀN TÁC — đường sau được hủy luồng trước, và đó là lý do đẩy tham lam
không có cạnh ngược là sai.

Việc dừng: Edmonds–Karp (đường tăng BFS ngắn nhất) đảm bảo O(V·E) lần
tăng — chặn đó làm luồng thành đa thức.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m9-augment",
    "Augmenting Paths and the Min Cut",
    "BFS finds the shortest augmenting path; when none remains, the set reachable from s IS the min cut — max-flow = min-cut falls out.",
    35,
    """
# From augmentations to the cut

Edmonds–Karp: BFS the residual graph, push the bottleneck, repeat. When
BFS finds no path, S = reachable-from-s: every original edge S→outside
is saturated, every outside→S edge is empty — cut capacity = flow value.

Dinic (BFS level graph + DFS blocking flow) is the default for the
course's load tests; Edmonds–Karp is for teaching and small m.
""",
    "Đường tăng và lát cắt nhỏ nhất",
    "BFS tìm đường tăng ngắn nhất; khi hết đường, tập với được từ s CHÍNH là min-cut — max-flow = min-cut rơi ra.",
    """
# Từ đường tăng đến lát cắt

Edmonds–Karp: BFS đồ thị dư, đẩy nút thắt, lặp. Khi BFS hết đường,
S = tập với được từ s: mọi cạnh gốc S→ngoài đã bão hòa, mọi cạnh
ngoài→S trống — năng lực lát cắt = giá trị luồng.

Dinic (BFS đồ thị mức + DFS blocking flow) là mặc định cho các bài tải
của khóa; Edmonds–Karp để dạy và cho m nhỏ.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m9-modeling",
    "Modeling Problems as Flow",
    "Bipartite matching is source→left→right→sink with unit caps; node capacities split nodes; the modeling IS the algorithm choice.",
    35,
    """
# Seeing networks everywhere

- Bipartite matching: source→left (1), left→right per compatibility (1),
  right→sink (1). Max flow = max matching.
- Node capacity c: split v into v_in→v_out cap c.
- Multi-source/sink: super-source, super-sink.
- Disjoint x-y paths: all caps 1 (vertex-disjoint: also split).

The exam skill is seeing capacity structure in word problems.
""",
    "Mô hình hóa bài toán thành luồng",
    "Ghép cặp hai phía là source→trái→phải→sink năng lực 1; năng lực đỉnh thì tách đỉnh; mô hình hóa CHÍNH là lựa chọn thuật toán.",
    """
# Nhìn thấy mạng ở khắp nơi

- Ghép cặp hai phía: source→trái (1), trái→phải theo tương thích (1),
  phải→sink (1). Max flow = ghép cực đại.
- Năng lực đỉnh c: tách v thành v_in→v_out cap c.
- Nhiều nguồn/bể: siêu nguồn, siêu bể.
- Đường đi không giao nhau: mọi cap 1 (không giao ở đỉnh: tách thêm).

Kỹ năng thi là nhìn thấy cấu trúc năng lực trong đề chữ.
""",
    difficulty="advanced",
)

write_checkpoint(
    M, "hsga-cp-m9",
    "Checkpoint — Flow Value",
    "A 100k-node layered network; the widest-path greedy that reports one route's capacity instead of the total cut is the graded wrong answer.",
    40,
    """
**Checkpoint — Luồng.** Dòng 1: n m s t; m dòng u v c (năng lực c).
In GIÁ TRỊ LUỒNG CỰC ĐẠI từ s đến t.

Dinic trên mạng phân tầng 10^5 đỉnh; giá trị không phải đường rộng nhất
mà là tổng qua lát cắt.
""",
    "Điểm kiểm tra — Giá trị luồng",
    "Mạng phân tầng 10^5 đỉnh; tham lam đường-rộng-nhất báo một đường thay vì tổng lát cắt là đáp án sai bị chấm.",
    """
**Checkpoint — Luồng.** Dòng 1: n m s t; m dòng u v c. In luồng cực
đại s→t.
""",
    challenge(
        "hsga-cp-m9-flowval",
        "Maximum Flow Value",
        """**Bài toán.** Line 1: n m s t. Then m lines u v c — a directed edge
with capacity c. Print the MAXIMUM FLOW from s to t.

**Constraints:** 1 ≤ n, m ≤ 100 000; 1 ≤ c ≤ 10^9.

Dinic on a layered network: the answer is the total across a cut, not
one route's capacity.
""",
        CP_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Giá trị luồng cực đại",
        """**Bài toán.** Dòng 1: n m s t; m dòng u v c. In LUỒNG CỰC ĐẠI
từ s đến t.""",
        [("min-cut", "Đáp án là tổng qua lát cắt, không phải một đường."),
         ("cạnh ngược", "Không có cung dư thì hủy luồng là bất khả thi."),
         ("n=100000", "Dinic nhiều pha ngắn; đẩy từng đơn vị là timeout.")],
    ),
    solution=CP_M9_R,
    wrong=CP_M9_W,
)

VI_P9 = {
    "hsga-p9-flow": vi_challenge(
        "Bộ ba luồng",
        """**Bài toán.** Ba bài: giá trị luồng nhỏ; kích thước ghép cặp hai
phía; luồng trên mạng phân tầng lớn.""",
        [("cạnh dư", "Cung ngược = nút hoàn tác; thiếu nó là sai."),
         ("augmenting path", "Ghép tham lam không dùng đường tăng thêm."),
         ("Dinic vs EK", "Mạng lớn: Dinic; đẩy từng đơn vị timeout.")],
    ),
}

write_practice(
    M, "hsga-p9-flow", "Flow Trio",
    "Small max flow with cancellation, bipartite matching as flow, and Dinic on a layered load — greedy, no-augment, and unit-push wrongs.",
    "Bộ ba luồng",
    "Luồng nhỏ có hủy, ghép cặp hai phía qua luồng, và Dinic trên tải phân tầng — bản sai tham lam, không-augment, và đẩy-đơn-vị.",
    "hsga-m9-modeling",
    110,
    "advanced",
    [
        challenge("hsga-p9-flowval", "Max Flow Value",
            """**Bài toán.** Line 1: n m s t; then m lines u v c. Print the
maximum flow from s to t.

**Constraints:** 1 ≤ n, m ≤ 2000; 1 ≤ c ≤ 10^9. Small enough for
Edmonds–Karp; cancellation via residual arcs is required.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p9-match", "Bipartite Matching",
            """**Bài toán.** Line 1: L R m; then m lines u v — left node u
compatible with right node v. Print the MAXIMUM MATCHING size.

**Constraints:** 1 ≤ L, R, m ≤ 2000.

Model as flow: source→left→right→sink, all caps 1. Greedy without
augmenting paths undercounts on the right graph.
""",
            A2_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p9-dinic", "Layered Network Flow",
            """**Bài toán.** Line 1: n m s t; then m lines u v c. Print the
maximum flow from s to t.

**Constraints:** 1 ≤ n, m ≤ 100 000; 1 ≤ c ≤ 10^9.

Dinic required: BFS level graph + DFS blocking flow. Unit-push
augmentation times out on the layered load.
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    VI_P9,
    solutions=[
        ("hsga-p9-flowval", A1_R, A1_W),
        ("hsga-p9-match", A2_R, A2_W),
        ("hsga-p9-dinic", A3_R, A3_W),
    ],
)

print("module m9 complete")
