#!/usr/bin/env python3
"""HSG Advanced — Module 19: hsga-contests2 (Contest Series II).

Two more 120-minute mock contests retesting trees and strings under
contest pressure: binary-lifting path sums, KMP period, subtree DP,
overlapping pattern counting, Euler-tour + BIT subtree sums, border
chains, and max-XOR pairs. Every W is a classic near-miss.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \\n escapes.
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-contests2"

# ------------------------------------------------------------------ models
def m_pathsum_bamboo(par, w, queries):
    # bamboo ground truth via prefix sums along the chain
    n = max(w)
    order = [1]
    for v in range(2, n + 1):
        order.append(v)
    pref = [0] * (n + 1)  # pref[i] = w[1..i] along chain order
    for i, v in enumerate(order, start=1):
        pref[i] = pref[i - 1] + w[v]
    pos = {v: i for i, v in enumerate(order, start=1)}
    outs = []
    for u, v in queries:
        a, b = pos[u], pos[v]
        if a > b:
            a, b = b, a
        outs.append(pref[b] - pref[a - 1])
    return outs


def m_pathsum_climb(par, w, queries):
    n = max(w)
    dep = [0] * (n + 1)
    for v in range(2, n + 1):
        dep[v] = dep[par[v]] + 1
    outs = []
    for u, v in queries:
        a, b = u, v
        while dep[a] > dep[b]:
            a = par[a]
        while dep[b] > dep[a]:
            b = par[b]
        while a != b:
            a = par[a]
            b = par[b]
        # collect path by walking again
        path = []
        x = u
        while x != a:
            path.append(x)
            x = par[x]
        path.append(a)
        stack = []
        x = v
        while x != a:
            stack.append(x)
            x = par[x]
        outs.append(sum(w[x] for x in path) + sum(w[x] for x in stack))
    return outs


def m_kmp_fail(s):
    n = len(s)
    f = [0] * (n + 1)
    for i in range(1, n):
        j = f[i]
        while j and s[i] != s[j]:
            j = f[j]
        if s[i] == s[j]:
            j += 1
        f[i + 1] = j
    return f


def m_period(s):
    f = m_kmp_fail(s)
    return len(s) - f[len(s)]


def m_period_w_divisor(s):
    n = len(s)
    for d in range(1, n + 1):
        if n % d == 0:
            ok = True
            for i in range(d, n):
                if s[i] != s[i - d]:
                    ok = False
                    break
            if ok:
                return d
    return n


def m_subtree_height(par, n):
    ch = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        ch[par[v]].append(v)
    dp = [0] * (n + 1)
    order = []
    st = [(1, False)]
    while st:
        v, done = st.pop()
        order.append(v)
        for c in ch[v]:
            st.append((c, False))
    for v in reversed(order):
        dp[v] = 1 + max((dp[c] for c in ch[v]), default=-1)
    return dp


def m_overlap(s, p):
    f = m_kmp_fail(p)
    j = 0
    cnt = 0
    for c in s:
        while j and c != p[j]:
            j = f[j]
        if c == p[j]:
            j += 1
        if j == len(p):
            cnt += 1
            j = f[j]
    return cnt


def m_overlap_w(s, p):
    pos = 0
    cnt = 0
    while True:
        i = s.find(p, pos)
        if i < 0:
            break
        cnt += 1
        pos = i + len(p)
    return cnt


def m_euler(par, n, ops):
    ch = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        ch[par[v]].append(v)
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    timer = 1
    st = [(1, iter(ch[1]))]
    tin[1] = timer
    timer += 1
    while st:
        v, it = st[-1]
        advanced = False
        for c in it:
            tin[c] = timer
            timer += 1
            st.append((c, iter(ch[c])))
            advanced = True
            break
        if not advanced:
            st.pop()
            tout[v] = timer - 1
    # Fenwick over Euler positions: point assign, range sum tin[v]..tout[v]
    fen = [0] * (n + 1)

    def upd(i, d):
        while i <= n:
            fen[i] += d
            i += i & (-i)

    def pref(i):
        s = 0
        while i > 0:
            s += fen[i]
            i -= i & (-i)
        return s

    vals = [0] * (n + 1)
    outs = []
    for op in ops:
        if op[0] == 1:
            _, v, x = op
            upd(tin[v], x - vals[v])
            vals[v] = x
        else:
            _, v = op
            outs.append(pref(tout[v]) - pref(tin[v] - 1))
    return outs


def m_borders(s):
    f = m_kmp_fail(s)
    j = f[len(s)]
    cnt = 0
    while j:
        cnt += 1
        j = f[j]
    return cnt


def m_maxxor(a):
    best = 0
    # trie
    trie = {}
    for x in a:
        node = trie
        for b in range(29, -1, -1):
            bit = (x >> b) & 1
            node = node.setdefault(bit, {})
    for x in a:
        node = trie
        cur = 0
        for b in range(29, -1, -1):
            bit = (x >> b) & 1
            want = 1 - bit
            if want in node:
                cur |= 1 << b
                node = node[want]
            else:
                node = node[bit]
        best = max(best, cur)
    return best


# ------------------------------------------------------------------ C1-A bodies (binary lifting path sums)
A1_R = CPP_STD + cpp("""
    // Node-weighted path sums via LCA: rd[x] = weight sum root..x.
    int n; in >> n;
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    vector<long long> w(n + 1, 0), rd(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    for (int v = 1; v <= n; ++v) in >> w[v];
    const int LOG = 18;
    vector<vector<int>> up(LOG, vector<int>(n + 1, 0));
    up[0][1] = 1;  // root's parent is itself
    rd[1] = w[1];  // root distance before the loop: children read it
    for (int v = 2; v <= n; ++v) {
        dep[v] = dep[par[v]] + 1;
        rd[v] = rd[par[v]] + w[v];
        up[0][v] = par[v];
    }
    for (int k = 1; k < LOG; ++k)
        for (int v = 1; v <= n; ++v)
            up[k][v] = up[k - 1][up[k - 1][v]];
    auto lca = [&](int a, int b) {
        if (dep[a] < dep[b]) swap(a, b);
        int d = dep[a] - dep[b];
        for (int k = 0; k < LOG; ++k)
            if (d >> k & 1) a = up[k][a];
        if (a == b) return a;
        for (int k = LOG - 1; k >= 0; --k)
            if (up[k][a] != up[k][b]) { a = up[k][a]; b = up[k][b]; }
        return up[0][a];
    };
    int q; in >> q;
    while (q--) {
        int u, v; in >> u >> v;
        int l = lca(u, v);
        long long ans = rd[u] + rd[v] - 2 * rd[l] + w[l];
        out << ans << "{{NL}}";
    }
""") + END

A1_W = CPP_STD + cpp("""
    int n; in >> n;
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    vector<long long> w(n + 1, 0), rd(n + 1, 0);
    for (int v = 2; v <= n; ++v) in >> par[v];
    for (int v = 1; v <= n; ++v) in >> w[v];
    rd[1] = w[1];
    for (int v = 2; v <= n; ++v) {
        dep[v] = dep[par[v]] + 1;
        rd[v] = rd[par[v]] + w[v];
    }
    int q; in >> q;
    while (q--) {
        int u, v; in >> u >> v;
        // WRONG: per-query parent climb — correct answers, O(depth) each;
        // a 200000-node bamboo with 200000 deep queries is 4e10 steps.
        int a = u, b = v;
        while (dep[a] > dep[b]) a = par[a];
        while (dep[b] > dep[a]) b = par[b];
        while (a != b) { a = par[a]; b = par[b]; }
        out << rd[u] + rd[v] - 2 * rd[a] + w[a] << "{{NL}}";
    }
""") + END

# ------------------------------------------------------------------ C1-B bodies (shortest period)
A2_R = CPP_STD + cpp("""
    // Shortest period = n - fail[n] (KMP failure function).
    string s; in >> s;
    int n = (int)s.size();
    vector<int> f(n + 1, 0);
    for (int i = 1; i < n; ++i) {
        int j = f[i];
        while (j && s[i] != s[j]) j = f[j];
        if (s[i] == s[j]) ++j;
        f[i + 1] = j;
    }
    out << (n - f[n]) << "{{NL}}";
""") + END

A2_W = CPP_STD + cpp("""
    string s; in >> s;
    int n = (int)s.size();
    // WRONG: only periods that DIVIDE n are checked — "abcabca" has
    // period 3 but n = 7, so the W reports 7.
    for (int d = 1; d <= n; ++d) {
        if (n % d != 0) continue;
        bool ok = true;
        for (int i = d; i < n && ok; ++i) ok = (s[i] == s[i - d]);
        if (ok) { out << d << "{{NL}}"; return; }
    }
    out << n << "{{NL}}";
""") + END

# ------------------------------------------------------------------ C2-A bodies (subtree max distance)
A3_R = CPP_STD + cpp("""
    // dp[v] = max edges from v down into its subtree (iterative postorder).
    int n; in >> n;
    vector<int> par(n + 1, 0);
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) { in >> par[v]; ch[par[v]].push_back(v); }
    vector<int> order;
    order.reserve(n);
    vector<int> st(1, 1);
    while (!st.empty()) {
        int v = st.back();
        st.pop_back();
        order.push_back(v);
        for (int c : ch[v]) st.push_back(c);
    }
    vector<int> dp(n + 1, 0);
    for (int i = n - 1; i >= 0; --i) {
        int v = order[i];
        int best = 0;
        for (int c : ch[v]) best = max(best, dp[c] + 1);
        dp[v] = best;
    }
    for (int v = 1; v <= n; ++v) out << dp[v] << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""
    int n; in >> n;
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    for (int v = 2; v <= n; ++v) { in >> par[v]; dep[v] = dep[par[v]] + 1; }
    // WRONG: prints the GLOBAL tree height for every node — the per-node
    // subtree invariant is lost; any tree with differing answers breaks it.
    int height = 0;
    for (int v = 1; v <= n; ++v) height = max(height, dep[v]);
    for (int v = 1; v <= n; ++v) out << height << "{{NL}}";
""") + END

# ------------------------------------------------------------------ C2-B bodies (overlapping occurrences)
A4_R = CPP_STD + cpp("""
    // KMP per pattern counts OVERLAPPING occurrences.
    int n; in >> n;
    string s; in >> s;
    int q; in >> q;
    while (q--) {
        string p; in >> p;
        int m = (int)p.size();
        vector<int> f(m + 1, 0);
        for (int i = 1; i < m; ++i) {
            int j = f[i];
            while (j && p[i] != p[j]) j = f[j];
            if (p[i] == p[j]) ++j;
            f[i + 1] = j;
        }
        int j = 0;
        long long cnt = 0;
        for (char c : s) {
            while (j && c != p[j]) j = f[j];
            if (c == p[j]) ++j;
            if (j == m) { ++cnt; j = f[j]; }
        }
        out << cnt << "{{NL}}";
    }
""") + END

A4_W = CPP_STD + cpp("""
    int n; in >> n;
    string s; in >> s;
    int q; in >> q;
    while (q--) {
        string p; in >> p;
        // WRONG: non-overlapping find loop — "aa" in "aaaaa" counts 2, not 4.
        long long cnt = 0;
        size_t pos = 0;
        while ((pos = s.find(p, pos)) != string::npos) { ++cnt; pos += p.size(); }
        out << cnt << "{{NL}}";
    }
""") + END

# ------------------------------------------------------------------ p19 practice bodies
P1_R = CPP_STD + cpp("""
    // Euler tour + BIT: point assign, subtree sum.
    int n; int q; in >> n >> q;
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) { int p; in >> p; ch[p].push_back(v); }
    vector<int> tin(n + 1, 0), tout(n + 1, 0);
    int timer = 0;
    {
        // iterative euler with child-index stack
        vector<pair<int, int>> st;
        st.push_back({1, 0});
        tin[1] = ++timer;
        while (!st.empty()) {
            int v = st.back().first;
            int i = st.back().second;
            if (i < (int)ch[v].size()) {
                ++st.back().second;
                int c = ch[v][i];
                tin[c] = ++timer;
                st.push_back({c, 0});
            } else {
                tout[v] = timer;
                st.pop_back();
            }
        }
    }
    vector<long long> fen(n + 1, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    vector<long long> cur(n + 1, 0);
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) {
            int v; long long x; in >> v >> x;
            upd(tin[v], x - cur[v]);
            cur[v] = x;
        } else {
            int v; in >> v;
            out << pref(tout[v]) - pref(tin[v] - 1) << "{{NL}}";
        }
    }
""") + END

P1_W = CPP_STD + cpp("""
    int n; int q; in >> n >> q;
    vector<int> par(n + 1, 0);
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) { in >> par[v]; ch[par[v]].push_back(v); }
    vector<long long> val(n + 1, 0);
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int v; long long x; in >> v >> x; val[v] = x; }
        else {
            int v; in >> v;
            // WRONG: re-walks the whole subtree per query — O(n) each;
            // 100000 subtree queries on n = 200000 is far over budget.
            long long s = 0;
            vector<int> st(1, v);
            while (!st.empty()) {
                int u = st.back();
                st.pop_back();
                s += val[u];
                for (int c : ch[u]) st.push_back(c);
            }
            out << s << "{{NL}}";
        }
    }
""") + END

P2_R = CPP_STD + cpp("""
    // Number of border lengths = steps in the failure chain.
    string s; in >> s;
    int n = (int)s.size();
    vector<int> f(n + 1, 0);
    for (int i = 1; i < n; ++i) {
        int j = f[i];
        while (j && s[i] != s[j]) j = f[j];
        if (s[i] == s[j]) ++j;
        f[i + 1] = j;
    }
    int j = f[n];
    long long cnt = 0;
    while (j) { ++cnt; j = f[j]; }
    out << cnt << "{{NL}}";
""") + END

P2_W = CPP_STD + cpp("""
    string s; in >> s;
    int n = (int)s.size();
    // WRONG: verifies every candidate length by direct comparison —
    // O(n^2); n = 1e6 is 1e12 character comparisons.
    long long cnt = 0;
    for (int l = 1; l < n; ++l) {
        bool ok = true;
        for (int i = 0; i < l && ok; ++i) ok = (s[i] == s[n - l + i]);
        if (ok) ++cnt;
    }
    out << cnt << "{{NL}}";
""") + END

P3_R = CPP_STD + cpp("""
    // Max pairwise XOR via a binary trie (30 levels).
    int n; in >> n;
    vector<unsigned> a(n);
    for (auto& x : a) in >> x;
    struct Node { int ch[2] = {0, 0}; };
    vector<Node> t(1);
    auto insert = [&](unsigned x) {
        int cur = 0;
        for (int b = 29; b >= 0; --b) {
            int bit = (x >> b) & 1u;
            if (!t[cur].ch[bit]) { t[cur].ch[bit] = (int)t.size(); t.push_back(Node()); }
            cur = t[cur].ch[bit];
        }
    };
    for (unsigned x : a) insert(x);
    unsigned best = 0;
    for (unsigned x : a) {
        int cur = 0;
        unsigned v = 0;
        for (int b = 29; b >= 0; --b) {
            int bit = (x >> b) & 1u;
            int want = 1 - bit;
            if (t[cur].ch[want]) { v |= 1u << b; cur = t[cur].ch[want]; }
            else cur = t[cur].ch[bit];
        }
        best = max(best, v);
    }
    out << best << "{{NL}}";
""") + END

P3_W = CPP_STD + cpp("""
    int n; in >> n;
    vector<unsigned> a(n);
    for (auto& x : a) in >> x;
    // WRONG: all-pairs scan — n = 200000 is 2e10 comparisons.
    unsigned best = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            best = max(best, a[i] ^ a[j]);
    out << best << "{{NL}}";
""") + END

# ------------------------------------------------------------------ ground truths
A1_par = {v: v - 1 for v in range(2, 200001)}  # bamboo
A1_w = {v: (v % 97) + 1 for v in range(1, 200001)}
_rng = random.Random(19)
A1_queries = [(1 + _rng.randint(0, 3000), 195000 + _rng.randint(0, 5000)) for _ in range(200000)]
A1_WANT = m_pathsum_bamboo(A1_par, A1_w, A1_queries)
# branching sanity vs climb model
A1_p2 = {2: 1, 3: 1, 4: 2, 5: 2, 6: 3}
A1_w2 = {1: 3, 2: 5, 3: 7, 4: 2, 5: 4, 6: 9}
A1_q2 = [(4, 5), (4, 6), (1, 6), (2, 3), (5, 5)]
assert m_pathsum_climb(A1_p2, A1_w2, A1_q2) == [11, 26, 19, 15, 4]

A2_T1 = "abcabca"
assert m_period(A2_T1) == 3
assert m_period_w_divisor(A2_T1) == 7
assert m_period("aaaa") == 1 and m_period("abcd") == 4
_A2_unit = "a" + "b" * 0 + "c"  # trivial
_A2_rep = "ab" * 3 + "a"        # "abababa": period 2
assert m_period(_A2_rep) == 2
A2_T2 = "abc" * 333333 + "ab"   # n = 1000001, true period 3 (3 does not divide n)
A2_WANT2 = m_period(A2_T2)
assert A2_WANT2 == 3
assert m_period_w_divisor(A2_T2) == 1000001

A3_T1 = {2: 1, 3: 1, 4: 2}      # root with two children, one grandchild
A3_WANT1 = m_subtree_height(A3_T1, 4)
assert A3_WANT1[1:] == [2, 1, 0, 0]
A3_par = {v: v - 1 for v in range(2, 200001)}
A3_WANT2 = m_subtree_height(A3_par, 200000)

A4_T1 = m_overlap("aaaaa", "aa")
assert A4_T1 == 4 and m_overlap_w("aaaaa", "aa") == 2
assert m_overlap("abcabcabc", "abc") == 3
assert m_overlap("ababa", "aba") == 2
_rng4 = random.Random(191)
A4_S = "".join(_rng4.choice("ab") for _ in range(200000))
A4_PATS = ["".join(_rng4.choice("ab") for _ in range(_rng4.randint(5, 1000))) for _ in range(200)]
A4_WANT2 = [m_overlap(A4_S, p) for p in A4_PATS]

P1_par = {v: v - 1 for v in range(2, 200001)}
_rng5 = random.Random(192)
P1_ops = []
for _ in range(100000):
    if _rng5.random() < 0.4:
        P1_ops.append((1, _rng5.randint(1, 200000), _rng5.randint(0, 100)))
    else:
        P1_ops.append((2, _rng5.randint(1, 200000)))
P1_WANT = m_euler(P1_par, 200000, P1_ops)
assert m_euler({2: 1, 3: 1, 4: 2}, 4, [(1, 2, 5), (1, 4, 3), (2, 1), (2, 2), (2, 4)]) == [8, 8, 3]

A_P2_1 = "ababab"
assert m_borders(A_P2_1) == 2          # abab, ab
assert m_borders("aaaa") == 3
P2_LOAD = "ab" * 500000                 # n = 1e6
P2_WANT2 = m_borders(P2_LOAD)
P2_WANT3 = m_borders("aab" * 333333 + "aa")

P3_T1 = [3, 10, 5, 25, 2, 8]
assert m_maxxor(P3_T1) == 28
_rng6 = random.Random(193)
P3_T2 = [_rng6.randint(0, 2**30 - 1) for _ in range(200000)]
P3_WANT2 = m_maxxor(P3_T2)

# ------------------------------------------------------------------ tests
A1_TESTS = [
    contest_test("branching tree, mixed paths",
        T("6", "1", "1", "2", "2", "3", "3 5 7 2 4 9", "5", "4 5", "4 6", "1 6", "2 3", "5 5"),
        T("11", "26", "19", "15", "4"),
        "Path 4-2-1-3-6 = 2+5+3+7+9 = 26; the climb and the lift must meet at the same LCA."),
    contest_test(
        "load: bamboo of 200000, 200000 deep queries",
        T("200000", *[str(A1_par[v]) for v in range(2, 200001)],
          " ".join(str(A1_w[v]) for v in range(1, 200001)),
          "200000",
          *[("%d %d" % q) for q in A1_queries]),
        T(*[str(v) for v in A1_WANT]),
        "Binary lifting answers each query in O(log n); climbing from a leaf region to the top is O(depth) per query."),
]

A2_TESTS = [
    contest_test("period does not divide n", T("abcabca"), T("3"),
        "abcabca repeats every 3 (a|b|c|a|b|c|a) but 3 does not divide 7 — divisor-only W says 7."),
    contest_test("period one", T("aaaa"), T("1"),
        "Every position repeats: the border aa|a gives period 1."),
    contest_test("period n", T("abcd"), T("4"),
        "No border: the whole string is its own period."),
    contest_test(
        "load: 1000001 chars, period 3 not dividing n",
        T(A2_T2),
        T("3"),
        "n - fail[n] is O(n); the divisor W must also fall back to n here (WA)."),
]

A3_TESTS = [
    contest_test("star with one branch", T("4", "1", "1", "2"), T("2", "1", "0", "0"),
        "Subtree of 1 spans 2 edges; leaf 3 and 4 have empty subtrees. Global-height W prints 2 everywhere."),
    contest_test("single node", T("1"), T("0"),
        "A lone node's subtree is itself: 0."),
    contest_test(
        "load: bamboo of 200000",
        T("200000", *[str(A3_par[v]) for v in range(2, 200001)]),
        T(*[str(v) for v in A3_WANT2[1:]]),
        "One iterative postorder is O(n); outputs n lines of per-node depth-to-leaf."),
]

A4_TESTS = [
    contest_test("overlaps matter", T("5", "aaaaa", "1", "aa"), T("4"),
        "aa occurs at positions 0,1,2,3 (overlapping). Non-overlapping W says 2."),
    contest_test("distinct pattern", T("9", "abcabcabc", "1", "abc"), T("3"),
        "Three disjoint hits — both approaches agree here."),
    contest_test("partial repeat", T("5", "ababa", "1", "aba"), T("2"),
        "aba at 0 and 2 (sharing the middle a): overlap counting only."),
    contest_test(
        "load: 200000-char haystack, 200 patterns",
        T("200000", A4_S, "200", *A4_PATS),
        T(*[str(v) for v in A4_WANT2]),
        "KMP per pattern is O(|s| + |p|); 200 patterns stay linear."),
]

P1_TESTS = [
    contest_test("assign then query subtrees",
        T("4 5", "1", "1", "2", "1 2 5", "1 4 3", "2 1", "2 2", "2 4"),
        T("8", "8", "3"),
        "Values 2=5, 4=3: subtree(1) = 8, subtree(2) = 5+3 = 8 (child included), leaf 4 = 3."),
    contest_test(
        "load: 100000 ops on a bamboo of 200000",
        T("200000 100000", *[str(P1_par[v]) for v in range(2, 200001)],
          *[("%d %d %d" % op) if op[0] == 1 else ("2 %d" % op[1]) for op in P1_ops]),
        T(*[str(v) for v in P1_WANT]),
        "Euler tour flattening + BIT answers each op in O(log n); subtree re-walks are O(n)."),
]

P2_TESTS = [
    contest_test("nested borders", T("ababab"), T("2"),
        "Borders abab and ab — the failure chain visits exactly these lengths."),
    contest_test("all equal", T("aaaa"), T("3"),
        "Borders a, aa, aaa: chain of length 3."),
    contest_test(
        "load: 1000000 chars",
        T(P2_LOAD),
        T(str(P2_WANT2)),
        "The failure chain is O(n) total; direct comparison for every length is O(n^2)."),
    contest_test(
        "load: 1000001 chars, many borders",
        T("aab" * 333333 + "aa"),
        T(str(P2_WANT3)),
        "Same O(n) chain on a second large string."),
]

P3_TESTS = [
    contest_test("classic set", T("6", "3", "10", "5", "25", "2", "8"), T("28"),
        "5 xor 25 = 28; the trie walks the complement path bit by bit."),
    contest_test("two values", T("2", "1", "2"), T("3"),
        "01 xor 10 = 11."),
    contest_test(
        "load: 200000 random 30-bit values",
        T("200000", " ".join(map(str, P3_T2))),
        T(str(P3_WANT2)),
        "Trie insert + query is O(n log V); all-pairs is O(n^2)."),
]

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Contest Series II — Trees and Strings",
    "Two more 120-minute mock contests: binary lifting, KMP, subtree DP, Euler tours, and tries under time pressure.",
    "Chuỗi kỳ thi II — Cây và xâu",
    "Hai kỳ thi giả lập 120 phút nữa: binary lifting, KMP, DP cây, Euler tour và trie dưới áp lực thời gian.",
    ["hsga-m19-scan2", "hsga-m19-bank2", "hsga-cp-m19a", "hsga-cp-m19b",
     "hsga-cp-m19c", "hsga-cp-m19d"],
    ["hsga-p19-mixed"],
)

write_lesson(
    M, "hsga-m19-scan2",
    "Contest Scan — Trees and Strings Edition",
    "Tree statements advertise their family through query shape; string statements through what repeats.",
    25,
    """
# Reading trees and strings fast

A tree with q queries on paths = LCA family. If values never change,
root-distance prefixes + LCA finish it; updates push you to HLD or
Euler + BIT on subtrees. "For every node" output = one postorder DFS;
if the answer for a child's parent depends on the child, it is tree DP.

A string asking "what repeats" = borders and failure functions. The
KMP failure array answers period, borders, and occurrence counting in
one preprocessing pass. If the question is "how many distinct", expect
suffix structures or hashing instead.
""", "Quét đề — bản cây và xâu",
    "Đề cây nói ra họ của nó qua hình dạng truy vấn; đề xâu qua cái gì lặp lại.",
    """
# Đọc nhanh cây và xâu

Cây + q truy vấn đường = họ LCA. Giá trị không đổi: prefix khoảng cách
từ gốc + LCA là xong; có cập nhật thì HLD hoặc Euler + BIT trên cây con.
"In cho mọi đỉnh" = một lần postorder; nếu đáp án cha phụ thuộc con, đó
là tree DP.

Xâu hỏi "cái gì lặp lại" = biên và hàm thất bại. Mảng failure của KMP
giải kỳ dại, biên, và đếm xuất hiện trong một lượt tiền xử lý. Nếu hỏi
"có bao nhiêu loại khác nhau", nghĩ tới cấu trúc suffix hoặc băm.
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m19-bank2",
    "Reading Your Own Code — the 5-Minute Audit",
    "Before submitting, audit the four places advanced solutions die: overflow, order of operations, off-by-one, and the invariant you assumed but never tested.",
    25,
    """
# The pre-submission audit

Five minutes before the deadline, do not write new code — audit:
1. WIDTHS: every multiplication or sum of maxima — is the widest
   expression long long?
2. ORDER: for lazy tags and DP pulls, is the compose order the one you
   proved?
3. BOUNDARIES: empty ranges, single elements, the root, the last
   character.
4. INVARIANTS: state in one sentence what must stay true; find the test
   that would break it if false.

Submitting one minute EARLIER with a checked solution beats submitting
a new idea at the buzzer.
""", "Đọc lại code của mình — soát 5 phút",
    "Trước khi nộp, soát bốn chỗ giải nâng cao hay chết: tràn số, thứ tự phép toán, lệch-một, và bất biến bạn giả định.",
    """
# Soát trước khi nộp

Năm phút cuối đừng viết code mới — hãy soát:
1. ĐỘ RỘNG: mọi tích/tổng của giá trị lớn nhất — biểu thức rộng nhất
   có phải long long không?
2. THỨ TỰ: với lazy tag và pull DP, thứ tự hợp có phải như đã chứng
   minh?
3. BIÊN: khoảng rỗng, một phần tử, gốc, ký tự cuối.
4. BẤT BIẾN: nói một câu bất biến phải đúng; chỉ ra test sẽ phá nó nếu
   sai.

Nộp sớm một phút với bài đã soát hơn nộp ý tưởng mới lúc trống giờ.
""", difficulty="advanced",
)

CP_A = challenge(
    "hsga-cp19-pathsum",
    "Signal Chain",
    """**Problem.** A rooted tree of n relay nodes (root 1). Line 1: n.
Then n-1 lines: parent of v (2..n). Then n weights w[1..n]. Then q and
q lines: u v — print the sum of node weights on the path u..v
(inclusive).

**Constraints:** 1 <= n, q <= 200000; 1 <= w[i] <= 100; 1 <= u, v <= n.
The tree may be a bamboo.

**R versus W.** The graded wrong solution answers each query by
climbing parents — correct output, hopeless on the bamboo load.
Target: full solve within 40 minutes.
""",
    A1_TESTS, level="real-world", difficulty="advanced")

VI_A = vi_challenge(
    "Chuỗi tín hiệu",
    """**Bài toán.** Cây gốc 1, trọng số trên đỉnh: với mỗi truy vấn in tổng
trọng số trên đường u..v.""",
    [("LCA", "rd[x] = tổng trọng số gốc..x; đáp án = rd[u]+rd[v]−2·rd[l]+w[l]."),
     ("bẫy", "Trèo cha từng truy vấn là O(depth) — chết trên dây dài."),
     ("kỹ thuật", "Bảng nhảy 2^k: mỗi truy vấn O(log n).")],
)

CP_B = challenge(
    "hsga-cp19-period",
    "Chant Rhythm",
    """**Problem.** Given a chant string s, print the length of its shortest
period p — the smallest p such that s[i] == s[i-p] for every i >= p.

**Constraints:** 1 <= |s| <= 2000001. The period need not divide |s|.

**R versus W.** The graded wrong solution only checks lengths that
divide |s| and reports |s| otherwise.
""",
    A2_TESTS, level="real-world", difficulty="advanced")

VI_B = vi_challenge(
    "Nhịp hô",
    """**Bài toán.** Cho xâu s: in độ dài kỳ dại ngắn nhất p với s[i] = s[i−p]
cho mọi i ≥ p. p không nhất thiết chia hết |s|.""",
    [("KMP", "Kỳ dại ngắn nhất = n − fail[n]."),
     ("bẫy", "Chỉ kiểm ước số của n — bỏ lỡ mọi kỳ dại không chia hết."),
     ("kích thước", "|s| tới 2·10^6: một lượt O(n).")],
)

CP_C = challenge(
    "hsga-cp19-subtree",
    "Watchtower Coverage",
    """**Problem.** A rooted tree of n watchtowers (root 1). Line 1: n.
Then n-1 lines: parent of v. For EVERY node print the maximum number
of edges from it down to any node in its own subtree, one per line in
node order 1..n.

**Constraints:** 1 <= n <= 200000; the tree may be a bamboo.

**R versus W.** The graded wrong solution prints the global tree
height for every node.
""",
    A3_TESTS, level="real-world", difficulty="advanced")

VI_C = vi_challenge(
    "Tầm tháp canh",
    """**Bài toán.** Với MỖI đỉnh: in khoảng cách lớn nhất (số cạnh) xuống
bất kỳ đỉnh nào trong cây con của nó.""",
    [("postorder", "dp[v] = 1 + max(dp[con]); một lượt DFS lặp."),
     ("bẫy", "Chiều cao toàn cây in cho mọi đỉnh — mất bất biến theo đỉnh."),
     ("kích thước", "n = 2e5, có thể là dây: DFS lặp.")],
)

CP_D = challenge(
    "hsga-cp19-motif",
    "Motif Counter",
    """**Problem.** Line 1: n, line 2: a DNA string s of length n. Line 3: q.
Then q motif strings. For each motif print how many times it occurs in
s — overlapping occurrences count separately.

**Constraints:** 1 <= n <= 200000; 1 <= q <= 200; total motif length
<= 200000.

**R versus W.** The graded wrong solution counts non-overlapping
matches only.
""",
    A4_TESTS, level="real-world", difficulty="advanced")

VI_D = vi_challenge(
    "Đếm motive",
    """**Bài toán.** Với mỗi motive: đếm số lần xuất hiện TRÙNG LẤP trong s.""",
    [("KMP", "Trạng thái j chạm m: đếm + nhảy fail[j] để cho phép trùng."),
     ("bẫy", "find() nhảy qua phần chồng — đếm thiếu."),
     ("kích thước", "q = 200, mỗi pattern O(|s|+|p|).")],
)

write_checkpoint(
    M, "hsga-cp-m19a",
    "Contest 3-A: Signal Chain",
    "Mock contest 3, problem A: LCA path sums with binary lifting. Target: solved within 40 minutes.",
    40,
    """**Contest 3-A — Signal Chain.** Node-weighted path sums: preprocess
root distances and a binary-lifting table; answer = rd[u] + rd[v] -
2*rd[lca] + w[lca]. Graded near-miss: per-query parent climbing.

**Contest 3-A.** The wrong version produces correct answers but walks
O(depth) per query — the bamboo load test buries it.
""",
    "Contest 3-A: Chuỗi tín hiệu",
    "Kỳ thi 3, bài A: tổng đường qua LCA + binary lifting. Mục tiêu: 40 phút.",
    """**Contest 3-A — Chuỗi tín hiệu.** Tiền xử lý rd và bảng nhảy 2^k;
đáp án = rd[u] + rd[v] − 2·rd[lca] + w[lca]. Near-miss bị chấm: trèo
cha từng truy vấn — đúng kết quả nhưng O(depth) mỗi lần, dây dài chôn
sạch.""",
    CP_A, VI_A,
    solution=A1_R,
    wrong=A1_W,
)

write_checkpoint(
    M, "hsga-cp-m19b",
    "Contest 3-B: Chant Rhythm",
    "Mock contest 3, problem B: shortest period via the KMP failure function. Target: solved within 40 minutes.",
    40,
    """**Contest 3-B — Chant Rhythm.** Shortest period = n - fail[n]. The
period does NOT have to divide n. Graded near-miss: divisor-only
checking.

**Contest 3-B.** The wrong version scans divisors of n and falls back
to n — "abcabca" (period 3, n 7) and the 1000001-char load both break
it.
""",
    "Contest 3-B: Nhịp hô",
    "Kỳ thi 3, bài B: kỳ dại ngắn nhất qua hàm thất bại KMP. Mục tiêu: 40 phút.",
    """**Contest 3-B — Nhịp hô.** Kỳ dại ngắn nhất = n − fail[n]; KHÔNG cần
chia hết n. Near-miss bị chấm: chỉ kiểm ước số — "abcabca" (kỳ dại 3,
n 7) và load 1000001 ký tự đều vỡ.""",
    CP_B, VI_B,
    solution=A2_R,
    wrong=A2_W,
)

write_checkpoint(
    M, "hsga-cp-m19c",
    "Contest 4-A: Watchtower Coverage",
    "Mock contest 4, problem A: per-node subtree depth via one postorder. Target: solved within 40 minutes.",
    40,
    """**Contest 4-A — Watchtower Coverage.** dp[v] = 1 + max(dp[child]);
single iterative postorder over up to 200000 nodes. Graded near-miss:
global height printed for every node.

**Contest 4-A.** The wrong invariant — "every node sees the tree's
height" — survives symmetric tests and dies on any asymmetric star.
""",
    "Contest 4-A: Tầm tháp canh",
    "Kỳ thi 4, bài A: chiều sâu cây con theo từng đỉnh bằng một postorder. Mục tiêu: 40 phút.",
    """**Contest 4-A — Tầm tháp canh.** dp[v] = 1 + max(dp[con]); một lượt
postorder lặp tới 200000 đỉnh. Near-miss bị chấm: in chiều cao toàn cây
cho mọi đỉnh — bất biến sai sống sót qua test đối xứng, vỡ ngay sao
lệch.""",
    CP_C, VI_C,
    solution=A3_R,
    wrong=A3_W,
)

write_checkpoint(
    M, "hsga-cp-m19d",
    "Contest 4-B: Motif Counter",
    "Mock contest 4, problem B: overlapping occurrence counting with KMP. Target: solved within 40 minutes.",
    40,
    """**Contest 4-B — Motif Counter.** KMP matching with the standard
j = fail[j] after a hit keeps overlapping occurrences. Graded
near-miss: the non-overlapping find loop.

**Contest 4-B.** The wrong version's loop advances by the pattern
length after each hit — "aa" in "aaaaa" reports 2 instead of 4.
""",
    "Contest 4-B: Đếm motive",
    "Kỳ thi 4, bài B: đếm xuất hiện trùng lặp bằng KMP. Mục tiêu: 40 phút.",
    """**Contest 4-B — Đếm motive.** KMP với bước j = fail[j] sau mỗi trúng
giữ được các lần xuất hiện chồng nhau. Near-miss bị chấm: vòng find
không chồng — "aa" trong "aaaaa" ra 2 thay vì 4.""",
    CP_D, VI_D,
    solution=A4_R,
    wrong=A4_W,
)

# ------------------------------------------------------------------ practice
PR_A = challenge(
    "hsga-p19-euler",
    "Treasury Audit",
    """**Problem.** A rooted tree (root 1) of n accounts. Line 1: n q.
Then n-1 lines: parent of v. Then q ops: "1 v x" sets account v's
balance to x; "2 v" prints the total balance in v's subtree.

**Constraints:** 1 <= n <= 200000; 1 <= q <= 100000; 0 <= x <= 100.

Subtree re-walks per query are the classic near-miss.
""",
    P1_TESTS, level="combination", difficulty="advanced")

VIP1 = vi_challenge(
    "Kiểm kê kho bạc",
    """**Bài toán.** Cây gốc 1: "1 v x" gán số dư, "2 v" in tổng cây con.""",
    [("Euler + BIT", "tin/tout làm đoạn cây con thành dải; BIT điểm/cập nhật."),
     ("bẫy", "Đi lại cây con mỗi truy vấn là O(n)."),
     ("kích thước", "n = 2e5, q = 1e5.")],
)

PR_B = challenge(
    "hsga-p19-borders",
    "Border Patrol",
    """**Problem.** Given a string s, count its border lengths: every
1 <= l < |s| with s[0..l) == s[|s|-l..|s|).

**Constraints:** 2 <= |s| <= 2000001.

Checking every length by direct comparison is the classic near-miss.
""",
    P2_TESTS, level="combination", difficulty="advanced")

VIP2 = vi_challenge(
    "Tuần tra biên",
    """**Bài toán.** Đếm số độ dài biên của xâu s: mọi 1 ≤ l < |s| với
tiền tố l bằng hậu tố l.""",
    [("failure chain", "Mỗi bước trên dây fail là một biên — đếm bước."),
     ("bẫy", "So trực tiếp từng l là O(n^2)."),
     ("kích thước", "|s| tới 2·10^6.")],
)

PR_C = challenge(
    "hsga-p19-maxxor",
    "Signal Pairing",
    """**Problem.** Given n device ids, print the maximum value of
a[i] xor a[j] over all pairs i < j.

**Constraints:** 1 <= n <= 200000; 0 <= a[i] < 2^30.

The all-pairs scan is the classic near-miss.
""",
    P3_TESTS, level="combination", difficulty="advanced")

VIP3 = vi_challenge(
    "Ghép tín hiệu",
    """**Bài toán.** In giá trị a[i] xor a[j] lớn nhất trên mọi cặp.""",
    [("trie nhị phân", "Chèn 30 bit; truy vấn đi theo bit ngược."),
     ("bẫy", "Quét mọi cặp là O(n^2)."),
     ("kích thước", "n = 2e5, giá trị < 2^30.")],
)

write_practice(
    M, "hsga-p19-mixed", "Mixed Drill — Trees and Strings",
    "Three timed synthesis problems: Euler + BIT, border chains, and a binary trie.",
    "Bài tập hỗn hợp — cây và xâu",
    "Ba bài tổng hợp có tính giờ: Euler + BIT, dây biên, và trie nhị phân.",
    "hsga-m19-bank2",
    110,
    "advanced",
    [PR_A, PR_B, PR_C],
    {
        "hsga-p19-mixed": vi_challenge(
            "Bài tập hỗn hợp II",
            """**Bài toán.** Ba bài: tổng cây con có cập nhật, đếm biên, và
cặp XOR lớn nhất.""",
            [("cây con", "Euler tour + BIT."),
             ("biên", "Dây failure KMP."),
             ("xor", "Trie nhị phân 30 tầng.")],
        ),
    },
    solutions=[
        ("hsga-p19-euler", P1_R, P1_W),
        ("hsga-p19-borders", P2_R, P2_W),
        ("hsga-p19-maxxor", P3_R, P3_W),
    ],
)

print("module m19 complete")
