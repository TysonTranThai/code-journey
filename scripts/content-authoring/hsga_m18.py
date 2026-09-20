#!/usr/bin/env python3
"""HSG Advanced — Module 18: hsga-contests (Contest Series I).

Two 120-minute mock contests (two graded problems each) retesting the
advanced data-structure and graph toolkit under contest time pressure:
lazy range-add/range-sum, SCC sizes, second-best MST, and a DSU
component timeline. Every W is a classic near-miss.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \\n escapes.
"""
import sys, os, random, bisect, heapq
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
#include <functional>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-contests"

# ------------------------------------------------------------------ models
def m_lazy(a, ops):
    arr = list(a)
    outs = []
    for op in ops:
        if op[0] == 1:
            _, l, r, v = op
            for i in range(l, r + 1):
                arr[i - 1] += v
        else:
            _, l, r = op
            outs.append(sum(arr[l - 1:r]))
    return outs


def m_scc_sizes(n, edges):
    # iterative Kosaraju: largest strongly connected component
    g = [[] for _ in range(n + 1)]
    gr = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        gr[v].append(u)
    vis = [False] * (n + 1)
    order = []
    for s in range(1, n + 1):
        if vis[s]:
            continue
        st = [(s, 0)]
        vis[s] = True
        while st:
            v, i = st[-1]
            if i < len(g[v]):
                st[-1] = (v, i + 1)
                u = g[v][i]
                if not vis[u]:
                    vis[u] = True
                    st.append((u, 0))
            else:
                order.append(v)
                st.pop()
    comp = [0] * (n + 1)
    c = 0
    for s in reversed(order):
        if comp[s]:
            continue
        c += 1
        comp[s] = c
        st = [s]
        while st:
            v = st.pop()
            for u in gr[v]:
                if not comp[u]:
                    comp[u] = c
                    st.append(u)
    from collections import Counter
    return max(Counter(comp[1:]).values())


def m_scc_w_forward(n, edges):
    # the W model: label by forward reach from each unvisited node
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
    vis = [False] * (n + 1)
    best = 0
    for s in range(1, n + 1):
        if vis[s]:
            continue
        st = [s]
        vis[s] = True
        cnt = 0
        while st:
            v = st.pop()
            cnt += 1
            for u in g[v]:
                if not vis[u]:
                    vis[u] = True
                    st.append(u)
        best = max(best, cnt)
    return best


def m_kruskal(n, wedges, descending):
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    es = sorted(wedges, key=lambda e: -e[0] if descending else e[0])
    total = 0
    used = []
    for w, u, v in es:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
            used.append((w, u, v))
    return total, used


def m_second_mst(n, wedges):
    mst, tree = m_kruskal(n, wedges, False)
    adj = [[] for _ in range(n + 1)]
    for w, u, v in tree:
        adj[u].append((v, w))
        adj[v].append((u, w))
    best = None
    tw = set(map(lambda e: (min(e[1], e[2]), max(e[1], e[2])), tree))
    for w, u, v in wedges:
        if (min(u, v), max(u, v)) in tw:
            continue
        # BFS u->v tracking max edge
        mx = [0] * (n + 1)
        seen = [False] * (n + 1)
        seen[u] = True
        st = [u]
        while st:
            x = st.pop()
            if x == v:
                break
            for y, ew in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    mx[y] = max(mx[x], ew)
                    st.append(y)
        cand = mst - mx[v] + w
        if cand > mst and (best is None or cand < best):
            best = cand
    return best


def m_dsu_timeline(n, ops):
    parent = list(range(n + 1))
    comps = n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    outs = []
    for u, v in ops:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            comps -= 1
        outs.append(comps)
    return outs


def m_ords(ops):
    sl = []
    outs = []
    for op in ops:
        if op[0] == 1:
            bisect.insort(sl, op[1])
        else:
            outs.append(sl[op[1] - 1])
    return outs


def m_circ_max(a):
    tot = sum(a)
    # kadane max
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    if best < 0:
        return best
    # min subarray
    mn = cur = a[0]
    for x in a[1:]:
        cur = min(x, cur + x)
        mn = min(mn, cur)
    return max(best, tot - mn)


def m_dijkstra(n, edges, src):
    g = [[] for _ in range(n + 1)]
    for w, u, v in edges:
        g[u].append((v, w))
    dist = [None] * (n + 1)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, v = heapq.heappop(pq)
        if dist[v] is not None and d > dist[v]:
            continue
        for u, w in g[v]:
            nd = d + w
            if dist[u] is None or nd < dist[u]:
                dist[u] = nd
                heapq.heappush(pq, (nd, u))
    return dist


# ------------------------------------------------------------------ C1-A bodies (lazy range add / range sum)
A1_R = CPP_STD + cpp("""
    int n, q; in >> n >> q;
    vector<long long> sm(4 * n), lz(4 * n, 0), ln(4 * n);
    std::function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { in >> sm[nd]; return; }
        int m = (l + r) / 2;
        build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        sm[nd] = sm[2 * nd] + sm[2 * nd + 1];
    };
    auto applyA = [&](int nd, long long v) { sm[nd] += v * ln[nd]; lz[nd] += v; };
    std::function<void(int)> push = [&](int nd) {
        if (lz[nd]) { applyA(2 * nd, lz[nd]); applyA(2 * nd + 1, lz[nd]); lz[nd] = 0; }
    };
    std::function<void(int, int, int, int, int, long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyA(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2 * nd, l, m, ql, qr, v); upd(2 * nd + 1, m + 1, r, ql, qr, v);
        sm[nd] = sm[2 * nd] + sm[2 * nd + 1];
    };
    std::function<long long(int, int, int, int, int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return sm[nd];
        push(nd); int m = (l + r) / 2;
        return qry(2 * nd, l, m, ql, qr) + qry(2 * nd + 1, m + 1, r, ql, qr);
    };
    build(1, 1, n);
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long v; in >> l >> r >> v; upd(1, 1, n, l, r, v); }
        else { int l, r; in >> l >> r; out << qry(1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END

A1_W = CPP_STD + cpp("""
    int n, q; in >> n >> q;
    vector<long long> sm(4 * n), lz(4 * n, 0), ln(4 * n);
    std::function<void(int, int, int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { in >> sm[nd]; return; }
        int m = (l + r) / 2;
        build(2 * nd, l, m); build(2 * nd + 1, m + 1, r);
        sm[nd] = sm[2 * nd] + sm[2 * nd + 1];
    };
    // WRONG: applyA forgets the length factor — a tag of v adds v, not
    // v * (segment length), so every add lands short.
    auto applyA = [&](int nd, long long v) { sm[nd] += v; lz[nd] += v; };
    std::function<void(int)> push = [&](int nd) {
        if (lz[nd]) { applyA(2 * nd, lz[nd]); applyA(2 * nd + 1, lz[nd]); lz[nd] = 0; }
    };
    std::function<void(int, int, int, int, int, long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyA(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2 * nd, l, m, ql, qr, v); upd(2 * nd + 1, m + 1, r, ql, qr, v);
        sm[nd] = sm[2 * nd] + sm[2 * nd + 1];
    };
    std::function<long long(int, int, int, int, int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return sm[nd];
        push(nd); int m = (l + r) / 2;
        return qry(2 * nd, l, m, ql, qr) + qry(2 * nd + 1, m + 1, r, ql, qr);
    };
    build(1, 1, n);
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long v; in >> l >> r >> v; upd(1, 1, n, l, r, v); }
        else { int l, r; in >> l >> r; out << qry(1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END

# ------------------------------------------------------------------ C1-B bodies (largest SCC)
A2_R = CPP_STD + cpp("""
    // Iterative Kosaraju — largest strongly connected component.
    int n; long long m; in >> n >> m;
    vector<vector<int>> g(n + 1), gr(n + 1);
    for (long long e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
        gr[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    vector<int> order;
    order.reserve(n);
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        vector<pair<int, int>> st;
        st.push_back({s, 0});
        vis[s] = 1;
        while (!st.empty()) {
            int v = st.back().first;
            int i = st.back().second;
            if (i < (int)g[v].size()) {
                ++st.back().second;
                int u = g[v][i];
                if (!vis[u]) { vis[u] = 1; st.push_back({u, 0}); }
            } else {
                order.push_back(v);
                st.pop_back();
            }
        }
    }
    vector<int> comp(n + 1, 0);
    int c = 0;
    vector<int> sz(1, 0);
    for (int i = n - 1; i >= 0; --i) {
        int s = order[i];
        if (comp[s]) continue;
        ++c;
        sz.push_back(0);
        comp[s] = c;
        vector<int> st(1, s);
        while (!st.empty()) {
            int v = st.back();
            st.pop_back();
            ++sz[c];
            for (int u : gr[v]) if (!comp[u]) { comp[u] = c; st.push_back(u); }
        }
    }
    int best = 0;
    for (int i = 1; i <= c; ++i) best = max(best, sz[i]);
    out << best << "{{NL}}";
""") + END

A2_W = CPP_STD + cpp("""
    int n; long long m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    for (long long e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
    }
    // WRONG: labels "components" by forward reach from each unvisited
    // node — a cycle plus everything it can reach becomes one component.
    vector<char> vis(n + 1, 0);
    int best = 0;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        vector<int> st(1, s);
        vis[s] = 1;
        int cnt = 0;
        while (!st.empty()) {
            int v = st.back();
            st.pop_back();
            ++cnt;
            for (int u : g[v]) if (!vis[u]) { vis[u] = 1; st.push_back(u); }
        }
        best = max(best, cnt);
    }
    out << best << "{{NL}}";
""") + END

# ------------------------------------------------------------------ C2-A bodies (second-best MST, small n)
A3_R = CPP_STD + cpp("""
    // Second-best MST: Kruskal, then each non-tree edge replaces the max
    // tree edge on its cycle. n <= 2000 so per-edge BFS is affordable.
    int n, m; in >> n >> m;
    vector<array<long long, 3>> e(m);
    for (int i = 0; i < m; ++i) in >> e[i][1] >> e[i][2] >> e[i][0];
    sort(e.begin(), e.end());
    vector<int> par(n + 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    std::function<int(int)> find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    vector<vector<pair<int, long long>>> t(n + 1);
    long long mst = 0;
    vector<char> used(m, 0);
    for (int i = 0; i < m; ++i) {
        int ru = find(e[i][1]), rv = find(e[i][2]);
        if (ru != rv) {
            par[ru] = rv;
            mst += e[i][0];
            used[i] = 1;
            t[e[i][1]].push_back({e[i][2], e[i][0]});
            t[e[i][2]].push_back({e[i][1], e[i][0]});
        }
    }
    long long best = -1;
    for (int i = 0; i < m; ++i) {
        if (used[i]) continue;
        int u = e[i][1], v = e[i][2];
        // BFS u->v tracking max edge on the tree path
        vector<long long> mx(n + 1, 0);
        vector<char> seen(n + 1, 0);
        vector<int> st(1, u);
        seen[u] = 1;
        while (!st.empty()) {
            int x = st.back();
            st.pop_back();
            if (x == v) break;
            for (auto& pr : t[x]) {
                if (!seen[pr.first]) {
                    seen[pr.first] = 1;
                    mx[pr.first] = max(mx[x], pr.second);
                    st.push_back(pr.first);
                }
            }
        }
        long long cand = mst - mx[v] + e[i][0];
        if (cand > mst && (best < 0 || cand < best)) best = cand;
    }
    out << best << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<array<long long, 3>> e(m);
    for (int i = 0; i < m; ++i) in >> e[i][1] >> e[i][2] >> e[i][0];
    // WRONG: sorts DESCENDING — builds the MAXIMUM spanning tree and
    // reports its weight instead of the second-best MST.
    sort(e.begin(), e.end(), [](const array<long long, 3>& a, const array<long long, 3>& b) {
        return a[0] > b[0];
    });
    vector<int> par(n + 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    std::function<int(int)> find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    long long total = 0;
    for (int i = 0; i < m; ++i) {
        int ru = find(e[i][1]), rv = find(e[i][2]);
        if (ru != rv) { par[ru] = rv; total += e[i][0]; }
    }
    out << total << "{{NL}}";
""") + END

# ------------------------------------------------------------------ C2-B bodies (component timeline)
A4_R = CPP_STD + cpp("""
    int n; long long k; in >> n >> k;
    vector<int> par(n + 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    std::function<int(int)> find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    int comps = n;
    for (long long t = 0; t < k; ++t) {
        int u, v; in >> u >> v;
        int ru = find(u), rv = find(v);
        if (ru != rv) { par[ru] = rv; --comps; }
        out << comps << "{{NL}}";
    }
""") + END

A4_W = CPP_STD + cpp("""
    int n; long long k; in >> n >> k;
    vector<int> par(n + 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    std::function<int(int)> find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    for (long long t = 0; t < k; ++t) {
        int u, v; in >> u >> v;
        int ru = find(u), rv = find(v);
        if (ru != rv) par[ru] = rv;
        // WRONG: recounts components by scanning every node's root —
        // O(n) per op; 2e5 ops on n = 2e5 is 4e10 steps.
        int comps = 0;
        for (int i = 1; i <= n; ++i) if (find(i) == i) ++comps;
        out << comps << "{{NL}}";
    }
""") + END

# ------------------------------------------------------------------ p18 practice bodies
P1_R = CPP_STD + cpp("""
    // order statistics: BIT over value range 1..1e6 + k-th descent
    const int MX = 1000000;
    int q; in >> q;
    vector<int> fen(MX + 1, 0);
    auto upd = [&](int i, int d) { for (; i <= MX; i += i & (-i)) fen[i] += d; };
    auto kth = [&](int k) {
        int pos = 0;
        for (int pw = 1 << 19; pw; pw >>= 1) {
            int np = pos + pw;
            if (np <= MX && fen[np] < k) { pos = np; k -= fen[np]; }
        }
        return pos + 1;
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int x; in >> x; upd(x, 1); }
        else { int k; in >> k; out << kth(k) << "{{NL}}"; }
    }
""") + END

P1_W = CPP_STD + cpp("""
    int q; in >> q;
    vector<long long> a;
    a.reserve(200005);
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { long long x; in >> x; a.push_back(x); }
        else {
            int k; in >> k;
            // WRONG: re-sorts the whole vector for every k-th query —
            // 1e5 sorts of up to 2e5 elements is far beyond the budget.
            vector<long long> b = a;
            sort(b.begin(), b.end());
            out << b[k - 1] << "{{NL}}";
        }
    }
""") + END

P2_R = CPP_STD + cpp("""
    // circular max subarray: kadane max, or total - kadane min (wrap)
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long tot = 0, bcur = 0, bbest = a[0], mcur = 0, mbest = a[0];
    tot = 0;
    for (int i = 0; i < n; ++i) {
        tot += a[i];
        if (i == 0) { bbest = mbest = a[0]; bcur = mcur = a[0]; continue; }
        bcur = max(a[i], bcur + a[i]);
        bbest = max(bbest, bcur);
        mcur = min(a[i], mcur + a[i]);
        mbest = min(mbest, mcur);
    }
    long long ans = bbest;
    if (bbest > 0) ans = max(ans, tot - mbest);
    out << ans << "{{NL}}";
""") + END

P2_W = CPP_STD + cpp("""
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: plain Kadane ignores the circular wrap — the best window may
    // cross the seam (total minus the worst interior stretch).
    long long bcur = a[0], bbest = a[0];
    for (int i = 1; i < n; ++i) {
        bcur = max(a[i], bcur + a[i]);
        bbest = max(bbest, bcur);
    }
    out << bbest << "{{NL}}";
""") + END

P3_R = CPP_STD + cpp("""
    int n; long long m; in >> n >> m;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (long long e = 0; e < m; ++e) {
        int u, v; long long w; in >> u >> v >> w;
        g[u].push_back({v, w});
    }
    vector<long long> dist(n + 1, -1);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
    dist[1] = 0;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, v] = pq.top();
        pq.pop();
        if (dist[v] != -1 && d > dist[v]) continue;
        for (auto& [u, w] : g[v]) {
            long long nd = d + w;
            if (dist[u] == -1 || nd < dist[u]) { dist[u] = nd; pq.push({nd, u}); }
        }
    }
    out << dist[n] << "{{NL}}";
""") + END

P3_W = CPP_STD + cpp("""
    int n; long long m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    for (long long e = 0; e < m; ++e) {
        int u, v; long long w; in >> u >> v >> w;
        g[u].push_back(v);
    }
    // WRONG: BFS counts HOPS, not tolls — the first layer to reach n
    // wins regardless of how expensive its edges are.
    vector<int> dist(n + 1, -1);
    vector<int> q(1, 1);
    dist[1] = 0;
    for (int h = 0; h < (int)q.size(); ++h) {
        int v = q[h];
        for (int u : g[v]) if (dist[u] == -1) { dist[u] = dist[v] + 1; q.push_back(u); }
    }
    out << dist[n] << "{{NL}}";
""") + END

# ------------------------------------------------------------------ ground truths
A1_N = 200000
A1_arr = [((i * 37 + 11) % 1000) - 500 for i in range(1, A1_N + 1)]
_rng = random.Random(18)
A1_ops = []
for _ in range(200000):
    if _rng.random() < 0.5:
        l = _rng.randint(1, A1_N)
        r = min(A1_N, l + _rng.randint(0, 5000))
        A1_ops.append((1, l, r, _rng.randint(-100, 100)))
    else:
        l = _rng.randint(1, A1_N)
        r = min(A1_N, l + _rng.randint(0, 5000))
        A1_ops.append((2, l, r))
A1_WANT = m_lazy(A1_arr, A1_ops)
assert m_lazy([1, 2, 3, 4], [(1, 1, 4, 5), (2, 2, 3), (1, 2, 2, 10), (2, 1, 4)]) == [15, 40]

A2_T1 = [(1, 2), (2, 1), (1, 3)]
A2_T2 = [(1, 2), (2, 1), (2, 3), (3, 4), (4, 3)]
A2_T3 = [(1, 2), (2, 3), (3, 1)]
_rng2 = random.Random(181)
A2_N = 50000
A2_T4 = [(_rng2.randint(1, A2_N), _rng2.randint(1, A2_N)) for _ in range(120000)]
A2_T4 = [(u, v) for u, v in A2_T4 if u != v]
assert m_scc_sizes(3, A2_T1) == 2 and m_scc_w_forward(3, A2_T1) == 3
assert m_scc_sizes(4, A2_T2) == 2 and m_scc_w_forward(4, A2_T2) == 4
assert m_scc_sizes(3, A2_T3) == 3 and m_scc_w_forward(3, A2_T3) == 3
A2_WANT4 = m_scc_sizes(A2_N, A2_T4)
assert m_scc_w_forward(A2_N, A2_T4) != A2_WANT4

A3_T1 = [(1, 1, 2), (2, 2, 3), (4, 1, 3)]
A3_T2 = [(1, 1, 2), (2, 2, 3), (3, 3, 4), (10, 1, 4), (4, 2, 4)]
_rng3 = random.Random(182)
A3_N, A3_M = 300, 900
A3_T3 = []
_seenw = set()
while len(A3_T3) < A3_M:
    u = _rng3.randint(1, A3_N)
    v = _rng3.randint(1, A3_N)
    w = _rng3.randint(1, 10 ** 6)
    if u != v and w not in _seenw:
        _seenw.add(w)
        A3_T3.append((w, u, v))
assert m_second_mst(3, A3_T1) == 5
assert m_second_mst(4, A3_T2) == 7
A3_WANT3 = m_second_mst(A3_N, A3_T3)
# W (max spanning tree) must differ on every multi-cycle test
assert m_kruskal(3, A3_T1, True)[0] != m_second_mst(3, A3_T1)
assert m_kruskal(A3_N, A3_T3, True)[0] != A3_WANT3

A4_T1 = [(1, 2), (3, 4), (2, 3)]
A4_T2 = [(1, 2), (1, 2), (2, 3)]
_rng4 = random.Random(183)
A4_N, A4_K = 200000, 200000
A4_T3 = [(_rng4.randint(1, A4_N), _rng4.randint(1, A4_N)) for _ in range(A4_K)]
A4_T3 = [(u, v) for u, v in A4_T3 if u != v]
assert m_dsu_timeline(4, A4_T1) == [3, 2, 1]
assert m_dsu_timeline(5, A4_T2) == [4, 4, 3]
A4_WANT3 = m_dsu_timeline(A4_N, A4_T3)

P1_ops = [
    (1, 5), (1, 3), (2, 1), (1, 7), (2, 2), (2, 3),
]
assert m_ords(P1_ops) == [3, 5, 7]
_rng5 = random.Random(184)
P1_ops2 = []
_vals = 0
for _ in range(200000):
    P1_ops2.append((1, _rng5.randint(1, 1000000)))
for _ in range(100000):
    _vals += 1
    P1_ops2.append((2, _rng5.randint(1, _vals)))
P1_WANT2 = m_ords(P1_ops2)

P2_T1 = [8, -1, 3, 4]
P2_T2 = [-3, -1, -2]
P2_T3 = [5, -2, 5]
assert m_circ_max(P2_T1) == 15
assert m_circ_max(P2_T2) == -1
assert m_circ_max(P2_T3) == 10
_rng6 = random.Random(185)
P2_T4 = [_rng6.randint(-10000, 10000) for _ in range(200000)]
P2_WANT4 = m_circ_max(P2_T4)

P3_T1 = [(5, 1, 2), (2, 1, 3), (1, 3, 2), (3, 2, 4), (7, 3, 4)]
P3_T2 = [(1, 1, 2), (1, 2, 3), (1, 3, 4)]
_rng7 = random.Random(186)
P3_N, P3_M = 100000, 200000
P3_T3 = [(1, i, i + 1) for i in range(1, P3_N)]  # guaranteed chain 1->2->...->N
while len(P3_T3) < P3_M:
    u = _rng7.randint(1, P3_N)
    v = _rng7.randint(1, P3_N)
    if u != v:
        P3_T3.append((_rng7.randint(1, 10 ** 9), u, v))
assert m_dijkstra(4, P3_T1, 1)[4] == 6
assert m_dijkstra(4, P3_T2, 1)[4] == 3
P3_WANT3 = m_dijkstra(P3_N, P3_T3, 1)[P3_N]

def _fmt_edges3(es):
    return [("%d %d %lld" % (u, v, w)) if False else ("%d %d %d" % (u, v, w)) for (w, u, v) in es]

# ------------------------------------------------------------------ tests
A1_TESTS = [
    contest_test("partial covers and stacked adds",
        T("4 4", "1 2 3 4", "1 1 4 5", "2 2 3", "1 2 2 10", "2 1 4"),
        T("15", "40"),
        "Add 5 everywhere: [6,7,8,9]; sum [2,3]=15; then [6,17,8,9] totals 40. The no-length-factor W reports 5 and 22."),
    contest_test(
        "load: 200000 mixed ops",
        T("200000 200000", " ".join(map(str, A1_arr)),
          *[("%d %d %d %d" % op) if op[0] == 1 else ("%d %d %d" % op) for op in A1_ops]),
        T(*[str(v) for v in A1_WANT]),
        "O((n + q) log n) lazy tree; the W's tags add v instead of v*length."),
]

A2_TESTS = [
    contest_test("cycle plus a tail", T("3 3", "1 2", "2 1", "2 3"), T("2"),
        "SCCs are {1,2} and {3}: the tail is reachable but not returning. Forward-reach W reports 3."),
    contest_test("two chained cycles", T("4 5", "1 2", "2 1", "2 3", "3 4", "4 3"), T("2"),
        "Cycles {1,2} and {3,4} are separate SCCs; forward reach from 1 swallows all 4."),
    contest_test("one big cycle", T("3 3", "1 2", "2 3", "3 1"), T("3"),
        "Everything mutually reachable: both approaches say 3."),
    contest_test(
        "load: 50000 nodes, 120000 edges",
        T("%d %d" % (A2_N, len(A2_T4)), *[("%d %d" % e) for e in A2_T4]),
        T(str(A2_WANT4)),
        "Iterative Kosaraju is O(n + m); recursive DFS also risks stack depth at n = 5e4."),
]

A3_TESTS = [
    contest_test("triangle", T("3 3", "1 2 1", "2 3 2", "1 3 4"), T("5"),
        "MST = 1+2 = 3; swap edge 2 for edge 4 gives the second-best 5. Max-spanning W says 6."),
    contest_test("four nodes", T("4 5", "1 2 1", "2 3 2", "3 4 3", "1 4 10", "2 4 4"), T("7"),
        "MST = 6; the 2-4 edge (w=4) replaces the path max 3, giving 7."),
    contest_test(
        "load: 300 nodes, 900 distinct-weight edges",
        T("%d %d" % (A3_N, A3_M), *[("%d %d %d" % (u, v, w)) for (w, u, v) in A3_T3]),
        T(str(A3_WANT3)),
        "Kruskal + per-non-tree-edge path max; O(m * n) fits n = 2000 easily."),
]

A4_TESTS = [
    contest_test("merge two pairs then bridge", T("4 3", "1 2", "3 4", "2 3"), T("3", "2", "1"),
        "4 -> 3 -> 2 -> 1 components as unions land."),
    contest_test("duplicate union is a no-op", T("5 3", "1 2", "1 2", "2 3"), T("4", "4", "3"),
        "Re-unioning the same pair must not decrease the count."),
    contest_test(
        "load: 200000 unions",
        T("%d %d" % (A4_N, len(A4_T3)), *[("%d %d" % e) for e in A4_T3]),
        T(*[str(v) for v in A4_WANT3]),
        "DSU with path compression answers per op in near-O(1); rescanning roots per op is O(n*k)."),
]

P1_TESTS = [
    contest_test("inserts interleaved with k-th queries",
        T("6", "1 5", "1 3", "2 1", "1 7", "2 2", "2 3"), T("3", "5", "7"),
        "Multiset {3,5,7}: 1st=3, then 5, then 7."),
    contest_test(
        "load: 200000 inserts, 100000 order queries",
        T(str(len(P1_ops2)), *[("%d %d" % op) for op in P1_ops2]),
        T(*[str(v) for v in P1_WANT2]),
        "BIT + binary descent answers k-th in O(log V); per-query re-sort is O(k * n log n)."),
]

P2_TESTS = [
    contest_test("wrap beats straight", T("4", "8", "-1", "3", "4"), T("15"),
        "Best straight run is 14; wrapping through the seam drops the -1: total 14 - (-1) = 15."),
    contest_test("all negative", T("3", "-3", "-1", "-2"), T("-1"),
        "Wrap formula must not fire when every element is negative: answer is the max element."),
    contest_test("no wrap needed", T("3", "5", "-2", "5"), T("10"),
        "Straight 5-2+5 = 10; wrap gives 8 - (-2) = 10 too — same answer."),
    contest_test(
        "load: 200000 mixed-sign values",
        T("200000", " ".join(map(str, P2_T4))),
        T(str(P2_WANT4)),
        "Two Kadane passes, O(n)."),
]

P3_TESTS = [
    contest_test("tolls beat hops", T("4 5", "1 2 5", "1 3 2", "3 2 1", "2 4 3", "3 4 7"), T("6"),
        "Cheapest: 1->3 (2), 3->2 (1), 2->4 (3) = 6. Hop-counting BFS reaches n in 2 hops."),
    contest_test("unit weights agree", T("4 3", "1 2 1", "2 3 1", "3 4 1"), T("3"),
        "With every toll 1, hops and tolls coincide."),
    contest_test(
        "load: 100000 nodes, 200000 weighted arcs",
        T("%d %d" % (P3_N, P3_M), *[("%d %d %d" % (u, v, w)) for (w, u, v) in P3_T3]),
        T(str(P3_WANT3)),
        "Dijkstra with a binary heap; BFS-on-weights misorders the frontier."),
]

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Contest Series I — Structures and Graphs",
    "Two 120-minute mock contests retesting lazy trees, SCC, MST reasoning, and DSU under time pressure.",
    "Chuỗi kỳ thi I — Cấu trúc và đồ thị",
    "Hai kỳ thi giả lập 120 phút rèn lazy tree, SCC, suy luận MST và DSU dưới áp lực thời gian.",
    ["hsga-m18-scan", "hsga-m18-bank", "hsga-cp-m18a", "hsga-cp-m18b",
     "hsga-cp-m18c", "hsga-cp-m18d"],
    ["hsga-p18-mixed"],
)

write_lesson(
    M, "hsga-m18-scan",
    "Contest Scan — Reading for Structure",
    "Advanced problems hide their structure behind stories. The first read extracts constraints, operation mix, and the family each problem belongs to.",
    25,
    """
# Scan before you solve

For each problem, extract three things in the first read: the largest
n and q, the OPERATION MIX (updates vs queries, ordered vs arbitrary),
and what quantity is asked (value? count? existence?). That triple
usually pins the algorithm family before you understand the story.

Range question + updates on segments = lazy tree family. Reachability
questions = SCC/DSU/union family. "Best swap after building X" = exchange
argument on top of the standard construction. Say the family out loud,
then verify with the constraints: n = 2e5 with per-op O(n) is dead;
O(n log n) or O(n alpha) is alive.
""", "Quét đề — đọc để tìm cấu trúc",
    "Bài nâng cao giấu cấu trúc phía sau câu chuyện. Lần đọc đầu trích ràng buộc, hỗn hợp phép toán, và họ thuật toán.",
    """
# Quét trước khi giải

Lần đọc đầu trích ba thứ: n và q lớn nhất, HỖN HỢP PHÉP TOÁN (cập nhật
vs truy vấn, có thứ tự hay tuỳ ý), và đại lượng cần hỏi (giá trị? số
lượng? tồn tại?). Bộ ba đó thường chốt họ thuật toán trước khi bạn hiểu
câu chuyện.

Truy vấn đoạn + cập nhật = họ lazy tree. Câu hỏi liên thông = SCC/DSU.
"Đổi một cạnh sau khi dựng X" = lập luận trao đổi trên cấu trúc chuẩn.
Nói to tên họ, rồi đối chiếu ràng buộc: n = 2e5 với O(n) mỗi phép là
chết; O(n log n) hoặc O(n alpha) là sống.
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m18-bank",
    "Banking Points — Partial Credit as a Strategy",
    "A subtask brute force submitted at minute 30 is worth more than a full solution submitted never.",
    25,
    """
# Bank the easy points first

HSG contests score totals, not elegance. If the full solution is not
CLEAR within your time budget, submit the subtask solution now: brute
force with the right complexity for small n, or the O(n^2) that passes
half the tests. Then return with the full idea. Two partial scores
usually beat one abandoned full attempt.

Write the brute force FIRST even when you know the full solution: it
becomes your stress-test oracle and your insurance if the clever
version misbehaves.
""", "Gom điểm — điểm một phần là chiến thuật",
    "Bài brute force nộp ở phút 30 đáng giá hơn bài giải đầy đủ mãi không nộp.",
    """
# Gom điểm dễ trước

Thi HSG chấm tổng điểm, không chấm độ đẹp. Nếu lời giải đầy đủ chưa
RÕ trong ngân sách thời gian, nộp lời giải subtask ngay: brute force
đúng phức tạp cho n nhỏ, hoặc bản O(n^2) qua một nửa test. Rồi quay
lại với ý đầy đủ. Hai điểm một phần thường thắng một bài bỏ dở.

Viết brute force TRƯỚC cả khi biết lời giải đầy đủ: nó vừa là mồi
stress test, vừa là bảo hiểm nếu bản thông minh lỗi.
""", difficulty="advanced",
)

CP_A = challenge(
    "hsga-cp18-rangesum",
    "Fever Chart",
    """**Problem.** Line 1: n q. Line 2: n initial values. Then q ops:
"1 l r v" adds v on [l, r]; "2 l r" prints the sum of [l, r].

**Constraints:** 1 <= n, q <= 200000; |values|, |v| <= 1e4; sums fit in
64 bits.

**R versus W.** The graded wrong solution applies each add tag without
multiplying by the segment length — every add lands short. Target:
full solve within 40 minutes.
""",
    A1_TESTS, level="real-world", difficulty="advanced")

VI_A = vi_challenge(
    "Bảng sốt",
    """**Bài toán.** Dòng 1: n q. Dòng 2: n giá trị ban đầu. Sau đó q phép:
"1 l r v" cộng v trên [l, r]; "2 l r" in tổng [l, r].""",
    [("lazy", "Tag cộng phải nhân độ dài đoạn khi áp lên tổng nút."),
     ("bẫy", "Quên nhân hệ số độ dài — mọi phép cộng đều bị thiếu."),
     ("kích thước", "n, q = 2e5: O((n+q) log n).")],
)

CP_B = challenge(
    "hsga-cp18-scc",
    "Recipe Clusters",
    """**Problem.** Line 1: n m. Then m lines: u v (a directed dependency
u depends on v). Print the size of the largest set of items that are
mutually reachable (directly or transitively).

**Constraints:** 1 <= n <= 50000; 0 <= m <= 120000.

**R versus W.** The graded wrong solution labels components by forward
reach from each unvisited node — a cycle plus everything it can reach
becomes one fake cluster. Target: full solve within 40 minutes.
""",
    A2_TESTS, level="real-world", difficulty="advanced")

VI_B = vi_challenge(
    "Cụm công thức",
    """**Bài toán.** n mục, m phụ thuộc có hướng: in kích thước tập lớn nhất
mà mọi cặp đều với nhau được (SCC lớn nhất).""",
    [("SCC", "Kosaraju lặp hai lượt: thứ tự trên đồ thị gốc, đếm trên đồ thị ngược."),
     ("bẫy", "Reach một chiều KHÔNG phải SCC — chu kỳ + đuôi sẽ bị gộp sai."),
     ("đệ quy", "n = 5e4: DFS lặp với ngăn xếp tường minh.")],
)

CP_C = challenge(
    "hsga-cp18-secondmst",
    "Backup Network",
    """**Problem.** Line 1: n m. Then m lines: u v w (undirected cable,
distinct weights). Print the weight of the SECOND-best spanning tree —
the minimum total weight over all spanning trees different from the MST.

**Constraints:** 2 <= n <= 2000; n-1 <= m <= 4000; weights distinct,
<= 1e6. A spanning tree always exists.

**R versus W.** The graded wrong solution sorts edges descending and
reports the maximum spanning tree's weight. Target: full solve within
40 minutes.
""",
    A3_TESTS, level="real-world", difficulty="advanced")

VI_C = vi_challenge(
    "Mạng dự phòng",
    """**Bài toán.** n điểm, m cáp phân biệt trọng số: in tổng trọng số của
cây khung TỐT THỨ HAI (khác cây khung nhỏ nhất).""",
    [("kỹ thuật", "Kruskal dựng MST; mỗi cạnh ngoài cây thay cạnh lớn nhất trên chu trình của nó."),
     ("bẫy", "Sắp giảm dần là cây khung LỚN nhất — không phải tốt thứ hai."),
     ("kích thước", "n = 2000: BFS tìm max-edge trên đường cho từng cạnh ngoài là đủ.")],
)

CP_D = challenge(
    "hsga-cp18-timeline",
    "Island Mergers",
    """**Problem.** Line 1: n k. Then k lines: u v — after each line, the
two islands merge if not already connected. After EVERY line print the
current number of connected island groups.

**Constraints:** 1 <= n, k <= 200000; 1 <= u, v <= n.

**R versus W.** The graded wrong solution rescans all roots after each
union — correct output, O(n) per operation, hopeless at full load.
Target: full solve within 40 minutes.
""",
    A4_TESTS, level="real-world", difficulty="advanced")

VI_D = vi_challenge(
    "Nhập đảo",
    """**Bài toán.** n đảo, k lượt nối: sau MỖI lượt in số nhóm đảo hiện có.""",
    [("DSU", "Giữ biến đếm: mỗi lần union thành công giảm 1."),
     ("bẫy", "Quét lại toàn bộ gốc sau mỗi lượt là O(n*k) — đúng nhưng quá chậm."),
     ("biên", "Nối hai đảo đã cùng nhóm: đếm không đổi.")],
)

write_checkpoint(
    M, "hsga-cp-m18a",
    "Contest 1-A: Fever Chart",
    "Mock contest 1, problem A: lazy range-add/range-sum. Target: solved within 40 minutes.",
    40,
    """**Contest 1-A — Fever Chart.** Lazy propagation with ADD tags only:
the tag must multiply by segment length when applied to a node's sum.
Graded near-miss: the tag applied without the length factor.

**Contest 1-A.** Range add, range sum with a lazy segment tree. The
apply step is sm += v * len. The graded wrong version adds v alone, so
every range add lands short — most visible on the very first full-range
add.
""",
    "Contest 1-A: Bảng sốt",
    "Kỳ thi 1, bài A: lazy range-add/range-sum. Mục tiêu: giải xong trong 40 phút.",
    """**Contest 1-A — Bảng sốt.** Lan truyền lười với tag CỘNG: khi áp tag
lên tổng nút phải nhân độ dài đoạn (sm += v * len). Near-miss bị chấm:
cộng v không nhân hệ số — mọi phép cộng đều thiếu.""",
    CP_A, VI_A,
    solution=A1_R,
    wrong=A1_W,
)

write_checkpoint(
    M, "hsga-cp-m18b",
    "Contest 1-B: Recipe Clusters",
    "Mock contest 1, problem B: largest SCC via iterative Kosaraju. Target: solved within 40 minutes.",
    40,
    """**Contest 1-B — Recipe Clusters.** Largest strongly connected
component. Iterative Kosaraju: order by finish time on G, then count
reach on the reverse graph. Graded near-miss: forward reach treated as
components.

**Contest 1-B.** The wrong version labels by forward reach from
unvisited nodes, merging a cycle with its whole downstream tail. Any
test where a cycle can reach extra nodes kills it.
""",
    "Contest 1-B: Cụm công thức",
    "Kỳ thi 1, bài B: SCC lớn nhất bằng Kosaraju lặp. Mục tiêu: giải xong trong 40 phút.",
    """**Contest 1-B — Cụm công thức.** SCC lớn nhất. Kosaraju lặp: xếp thứ
tự kết thúc trên G, đếm thành phần trên đồ thị ngược. Near-miss bị chấm:
lấy reach một chiều làm thành phần — chu kỳ cộng toàn bộ phần nó với
được bị gộp thành một cụm giả.""",
    CP_B, VI_B,
    solution=A2_R,
    wrong=A2_W,
)

write_checkpoint(
    M, "hsga-cp-m18c",
    "Contest 2-A: Backup Network",
    "Mock contest 2, problem A: second-best MST via Kruskal + cycle replacement. Target: solved within 40 minutes.",
    40,
    """**Contest 2-A — Backup Network.** Second-best spanning tree:
Kruskal for the MST, then for every non-tree edge replace the maximum
tree edge on its cycle. Graded near-miss: descending sort = maximum
spanning tree.

**Contest 2-A.** The wrong version inverts the sort direction and
reports the heaviest spanning tree — a one-character bug with a
completely different meaning.
""",
    "Contest 2-A: Mạng dự phòng",
    "Kỳ thi 2, bài A: cây khung tốt thứ hai bằng Kruskal + thay thế trên chu trình. Mục tiêu: 40 phút.",
    """**Contest 2-A — Mạng dự phòng.** Cây khung tốt thứ hai: Kruskal dựng
MST, rồi mỗi cạnh ngoài cây thay cạnh lớn nhất trên chu trình của nó.
Near-miss bị chấm: sắp GIẢM dần — ra cây khung lớn nhất, khác hẳn nghĩa
bài.""",
    CP_C, VI_C,
    solution=A3_R,
    wrong=A3_W,
)

write_checkpoint(
    M, "hsga-cp-m18d",
    "Contest 2-B: Island Mergers",
    "Mock contest 2, problem B: component count after every union (DSU with a counter). Target: solved within 40 minutes.",
    40,
    """**Contest 2-B — Island Mergers.** DSU plus one integer: components
start at n and drop by one per successful union. Graded near-miss:
recounting roots per query — correct but O(n*k).

**Contest 2-B.** The wrong version produces the right answers on small
data and times out at full load: 200000 rescans of 200000 nodes.
""",
    "Contest 2-B: Nhập đảo",
    "Kỳ thi 2, bài B: số thành phần sau mỗi lần nối (DSU + biến đếm). Mục tiêu: 40 phút.",
    """**Contest 2-B — Nhập đảo.** DSU cộng một số nguyên: đếm bắt đầu từ n,
giảm 1 mỗi union thành công. Near-miss bị chấm: đếm lại gốc sau mỗi
truy vấn — đúng kết quả nhưng O(n*k), chết ở dữ liệu đầy đủ.""",
    CP_D, VI_D,
    solution=A4_R,
    wrong=A4_W,
)

# ------------------------------------------------------------------ practice
PR_A = challenge(
    "hsga-p18-ords",
    "Order Statistics Dispatch",
    """**Problem.** q ops: "1 x" inserts value x into the multiset;
"2 k" prints the k-th smallest value (guaranteed to exist).

**Constraints:** 1 <= q <= 300000; 1 <= x <= 1e6; at most 200000
inserts before any k-th query.

Sort-per-query is the classic near-miss here.
""",
    P1_TESTS, level="combination", difficulty="advanced")

VIP1 = vi_challenge(
    "Điều phối thứ tự",
    """**Bài toán.** q phép: "1 x" thêm x vào đa tập; "2 k" in giá trị nhỏ
thứ k.""",
    [("BIT", "Fenwick trên dải giá trị + descent nhị phân tìm k-th."),
     ("bẫy", "Sắp lại toàn bộ mỗi truy vấn là O(q * n log n)."),
     ("kích thước", "q tới 3e5, giá trị tới 1e6.")],
)

PR_B = challenge(
    "hsga-p18-circ",
    "Cyclic Harvest",
    """**Problem.** A circular field of n plots with yields a[i] (may be
negative). Choose a non-empty contiguous arc maximizing the total yield.
Print that maximum.

**Constraints:** 1 <= n <= 200000; |a[i]| <= 1e4.

The seam is the whole problem: the best arc may wrap.
""",
    P2_TESTS, level="combination", difficulty="advanced")

VIP2 = vi_challenge(
    "Mùa vòng tròn",
    """**Bài toán.** n thửa arranged vòng tròn: chọn cung liên tiếp không
rỗng có tổng lớn nhất.""",
    [("hai Kadane", "max Kadane thẳng, và tổng - min Kadane (cung quấn seam)."),
     ("bẫy", "Toàn âm: công thức wrap phải tắt, đáp án là phần tử lớn nhất."),
     ("kiểm", "8 -1 3 4: thẳng 14, quấn 15.")],
)

PR_C = challenge(
    "hsga-p18-tolls",
    "Bridge Tolls",
    """**Problem.** Directed graph, tolls on arcs. Print the minimum total
toll from city 1 to city n.

**Constraints:** 1 <= n <= 100000; 0 <= m <= 200000; tolls <= 1e9;
n is always reachable.

Hop-counting BFS is the classic near-miss.
""",
    P3_TESTS, level="combination", difficulty="advanced")

VIP3 = vi_challenge(
    "Phí cầu đường",
    """**Bài toán.** Đồ thị có hướng có phí: in tổng phí nhỏ nhất từ 1 tới n.""",
    [("Dijkstra", "Heap nhị phân,Dist nhỏ nhất ưu tiên trước."),
     ("bẫy", "BFS đếm SỐ CẦU, không phải tổng phí."),
     ("kích thước", "n = 1e5, m = 2e5.")],
)

write_practice(
    M, "hsga-p18-mixed", "Mixed Drill — Structures and Graphs",
    "Three timed synthesis problems: order statistics over a BIT, circular Kadane, and weighted shortest paths.",
    "Bài tập hỗn hợp — cấu trúc và đồ thị",
    "Ba bài tổng hợp có tính giờ: thống kê thứ tự trên BIT, Kadane vòng, và đường đi ngắn có trọng số.",
    "hsga-m18-bank",
    110,
    "advanced",
    [PR_A, PR_B, PR_C],
    {
        "hsga-p18-mixed": vi_challenge(
            "Bài tập hỗn hợp I",
            """**Bài toán.** Ba bài: k-th nhỏ nhất trên đa tập, tổng cung tròn
lớn nhất, và đường phí nhỏ nhất 1 -> n.""",
            [("thứ tự", "Fenwick + descent."),
             ("vòng", "Hai Kadane: thẳng và quấn."),
             ("đường", "Dijkstra, không phải BFS.")],
        ),
    },
    solutions=[
        ("hsga-p18-ords", P1_R, P1_W),
        ("hsga-p18-circ", P2_R, P2_W),
        ("hsga-p18-tolls", P3_R, P3_W),
    ],
)

print("module m18 complete")
