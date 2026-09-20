#!/usr/bin/env python3
"""HSG Advanced — Module 20: hsga-contests3 (Final HSG Simulation).

The closing mock-contest module: four synthesis problems mixing sweeps,
binary search on answer, convex hulls, and Mobius counting, plus a
mixed drill (subarray sums, keyed BFS, digit DP). Every W is a classic
near-miss.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \\n escapes.
"""
import sys, os, random, bisect
from collections import deque
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
#include <array>
#include <map>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-contests3"

# ------------------------------------------------------------------ models
def m_inv2_brute(a):
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > 2 * a[j])


def m_inv2_bit(a):
    vals = sorted(set(a) | set(2 * x for x in a))
    m = len(vals)
    fen = [0] * (m + 1)

    def upd(i, d):
        while i <= m:
            fen[i] += d
            i += i & (-i)

    def pref(i):
        s = 0
        while i > 0:
            s += fen[i]
            i -= i & (-i)
        return s

    total = 0
    for x in reversed(a):
        # count inserted values strictly less than x (so a[i] > 2*a[j])
        cnt_lt = bisect.bisect_left(vals, x)
        total += pref(cnt_lt)
        r2 = bisect.bisect_right(vals, 2 * x)
        upd(r2, 1)
    return total


def m_cargo_brute(a, k):
    n = len(a)
    # dp over partitions: minimal possible max-sum with j parts
    INF = float("inf")
    pre = [0] * (n + 1)
    for i, x in enumerate(a, 1):
        pre[i] = pre[i - 1] + x
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            for t in range(j - 1, i):
                seg = pre[i] - pre[t]
                cand = max(dp[t][j - 1], seg)
                if cand < dp[i][j]:
                    dp[i][j] = cand
    return dp[n][k]


def m_cargo_bs(a, k, strict):
    lo, hi = max(a), sum(a)

    def parts(limit):
        cnt = 1
        cur = 0
        for x in a:
            if cur + x > limit:
                cnt += 1
                cur = x
            else:
                cur += x
        return cnt

    while lo < hi:
        mid = (lo + hi) // 2
        if (parts(mid) < k) if strict else (parts(mid) <= k):
            hi = mid
        else:
            lo = mid + 1
    return lo


def m_hull_area2(pts):
    # strict monotone chain, doubled shoelace of the hull
    pts = sorted(set(pts))
    if len(pts) < 3:
        return 0

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    hull = lo[:-1] + up[:-1]
    if len(hull) < 3:
        return 0
    s = 0
    for i in range(len(hull)):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % len(hull)]
        s += x1 * y2 - x2 * y1
    return abs(s)


def m_shoelace2(seq):
    s = 0
    n = len(seq)
    for i in range(n):
        x1, y1 = seq[i]
        x2, y2 = seq[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s)


def m_coprime_pairs(a):
    mx = max(a)
    cnt = [0] * (mx + 1)
    for x in a:
        cnt[x] += 1
    cmul = [0] * (mx + 1)
    for d in range(1, mx + 1):
        c = 0
        for multiple in range(d, mx + 1, d):
            c += cnt[multiple]
        cmul[d] = c
    mobius = [1] * (mx + 1)
    is_prime = [True] * (mx + 1)
    primes = []
    for p in range(2, mx + 1):
        if is_prime[p]:
            primes.append(p)
            mobius[p] = -1
        for q in primes:
            if p * q > mx:
                break
            is_prime[p * q] = False
            if p % q == 0:
                mobius[p * q] = 0
                break
            mobius[p * q] = -mobius[p]
    total = 0
    for d in range(1, mx + 1):
        if mobius[d] and cmul[d] >= 2:
            total += mobius[d] * (cmul[d] * (cmul[d] - 1) // 2)
    return total


def m_coprime_w(a):
    # WRONG model: pairs sharing any common divisor >= 2
    mx = max(a)
    cnt = [0] * (mx + 1)
    for x in a:
        cnt[x] += 1
    total = 0
    for d in range(2, mx + 1):
        c = 0
        for multiple in range(d, mx + 1, d):
            c += cnt[multiple]
        total += c * (c - 1) // 2
    return total


def m_subsum(a, S):
    seen = {0: 1}
    cur = 0
    cnt = 0
    for x in a:
        cur += x
        cnt += seen.get(cur - S, 0)
        seen[cur] = seen.get(cur, 0) + 1
    return cnt


def m_subsum_w(a, S):
    # WRONG: two-pointer assuming non-negative values
    n = len(a)
    cnt = 0
    lo = 0
    cur = 0
    for hi in range(n):
        cur += a[hi]
        while lo <= hi and cur > S:
            cur -= a[lo]
            lo += 1
        if cur == S:
            cnt += 1
    return cnt


def m_grid_bfs(grid, with_key):
    R, C = len(grid), len(grid[0])
    start = exit_ = key = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                exit_ = (r, c)
            elif grid[r][c] == "K":
                key = (r, c)
    # state: (r, c, haskey) if with_key else (r, c)
    seen = set()
    start_state = (start[0], start[1], False)
    seen.add(start_state)
    dq = deque([(start_state, 0)])
    while dq:
        (r, c, hk), d = dq.popleft()
        if (r, c) == exit_:
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < R and 0 <= nc < C):
                continue
            ch = grid[nr][nc]
            if ch == "#":
                continue
            if ch == "D" and not (with_key and hk):
                continue
            nhk = hk or (with_key and (nr, nc) == key)
            st = (nr, nc, nhk)
            if st not in seen:
                seen.add(st)
                dq.append((st, d + 1))
    return -1


def m_digitdp(N, k):
    s = str(N)
    L = len(s)
    free = [[0] * k for _ in range(L + 1)]
    free[L][0] = 1
    for i in range(L - 1, -1, -1):
        for m in range(k):
            for d in range(10):
                free[i][(m + d) % k] += free[i + 1][m]
    total = 0
    mod = 0
    for i, ch in enumerate(s):
        di = int(ch)
        for d in range(di):
            # suffix must supply (-(mod + d)) mod k
            total += free[i + 1][(k - (mod + d) % k) % k]
        mod = (mod + di) % k
    if mod == 0:
        total += 1
    return total - 1  # exclude x = 0


def m_digitdp_brute(N, k):
    return sum(1 for x in range(1, N + 1) if sum(int(c) for c in str(x)) % k == 0)


# ------------------------------------------------------------------ C5-A bodies (inversion doubles)
A1_R = CPP_STD + cpp("""
    // Count pairs i<j with a[i] > 2*a[j]: BIT over compressed {a, 2a},
    // sweep right to left.
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> vals(2 * n);
    for (int i = 0; i < n; ++i) { vals[i] = a[i]; vals[n + i] = 2 * a[i]; }
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = (int)vals.size();
    vector<int> fen(m + 1, 0);
    auto upd = [&](int i, int d) { for (; i <= m; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    long long total = 0;
    for (int i = n - 1; i >= 0; --i) {
        int lt = (int)(lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin());
        total += pref(lt);  // inserted 2*a[j] strictly below a[i]
        int r2 = (int)(upper_bound(vals.begin(), vals.end(), 2 * a[i]) - vals.begin());
        upd(r2, 1);
    }
    out << total << "{{NL}}";
""") + END

A1_W = CPP_STD + cpp("""
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: all-pairs scan — n = 200000 is 2e10 comparisons.
    long long total = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (a[i] > 2 * a[j]) ++total;
    out << total << "{{NL}}";
""") + END

# ------------------------------------------------------------------ C5-B bodies (cargo split)
A2_R = CPP_STD + cpp("""
    // Binary search the answer: min max-segment-sum with k contiguous parts.
    int n; int k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    auto parts = [&](long long limit) {
        int cnt = 1;
        long long cur = 0;
        for (long long x : a) {
            if (cur + x > limit) { ++cnt; cur = x; }
            else cur += x;
        }
        return cnt;
    };
    long long lo = *max_element(a.begin(), a.end()), hi = 0;
    for (long long x : a) hi += x;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (parts(mid) <= k) hi = mid;
        else lo = mid + 1;
    }
    out << lo << "{{NL}}";
""") + END

A2_W = CPP_STD + cpp("""
    int n; int k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    auto parts = [&](long long limit) {
        int cnt = 1;
        long long cur = 0;
        for (long long x : a) {
            if (cur + x > limit) { ++cnt; cur = x; }
            else cur += x;
        }
        return cnt;
    };
    long long lo = *max_element(a.begin(), a.end()), hi = 0;
    for (long long x : a) hi += x;
    // WRONG: predicate demands STRICTLY fewer than k parts, so the search
    // overshoots to a larger limit than the optimum.
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (parts(mid) < k) hi = mid;
        else lo = mid + 1;
    }
    out << lo << "{{NL}}";
""") + END

# ------------------------------------------------------------------ C6-A bodies (hull area)
A3_R = CPP_STD + cpp("""
    // Strict convex hull (monotone chain), then doubled shoelace area.
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& q : p) in >> q.first >> q.second;
    sort(p.begin(), p.end());
    p.erase(unique(p.begin(), p.end()), p.end());
    int m = (int)p.size();
    if (m < 3) { out << 0 << "{{NL}}"; return; }
    auto cross = [](const pair<long long, long long>& o,
                    const pair<long long, long long>& a,
                    const pair<long long, long long>& b) {
        return (a.first - o.first) * (b.second - o.second)
             - (a.second - o.second) * (b.first - o.first);
    };
    vector<pair<long long, long long>> h(2 * m);
    int k = 0;
    for (int i = 0; i < m; ++i) {
        while (k >= 2 && cross(h[k - 2], h[k - 1], p[i]) <= 0) --k;
        h[k++] = p[i];
    }
    for (int i = m - 2, t = k + 1; i >= 0; --i) {
        while (k >= t && cross(h[k - 2], h[k - 1], p[i]) <= 0) --k;
        h[k++] = p[i];
    }
    // h[0..k-1) is the hull walk with h[k-1] == h[0]; edges h_i->h_{i+1}
    // for i = 0..k-2 close the polygon back to h[0].
    long long s = 0;
    for (int i = 0; i + 1 < k; ++i) {
        s += h[i].first * h[i + 1].second - h[i + 1].first * h[i].second;
    }
    out << ((s < 0 ? -s : s)) << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& q : p) in >> q.first >> q.second;
    // WRONG: shoelace over the INPUT order — for anything but a convex,
    // properly ordered polygon this is not the hull area.
    long long s = 0;
    for (int i = 0; i < n; ++i) {
        s += p[i].first * p[(i + 1) % n].second - p[(i + 1) % n].first * p[i].second;
    }
    out << ((s < 0 ? -s : s)) << "{{NL}}";
""") + END

# ------------------------------------------------------------------ C6-B bodies (coprime pairs)
A4_R = CPP_STD + cpp("""
    // Pairs with gcd == 1: Mobius over the value range.
    int n; in >> n;
    int mx = 0;
    vector<int> a(n);
    for (auto& x : a) { in >> x; mx = max(mx, x); }
    vector<int> cnt(mx + 1, 0);
    for (int x : a) ++cnt[x];
    vector<int> cmul(mx + 1, 0);
    for (int d = 1; d <= mx; ++d)
        for (int v = d; v <= mx; v += d) cmul[d] += cnt[v];
    vector<int> mobius(mx + 1, 1);
    vector<char> composite(mx + 1, 0);
    vector<int> primes;
    for (int p = 2; p <= mx; ++p) {
        if (!composite[p]) { primes.push_back(p); mobius[p] = -1; }
        for (int q : primes) {
            if ((long long)p * q > mx) break;
            composite[p * q] = 1;
            if (p % q == 0) { mobius[p * q] = 0; break; }
            mobius[p * q] = -mobius[p];
        }
    }
    long long total = 0;
    for (int d = 1; d <= mx; ++d) {
        if (mobius[d] && cmul[d] >= 2)
            total += (long long)mobius[d] * cmul[d] * (cmul[d] - 1) / 2;
    }
    out << total << "{{NL}}";
""") + END

A4_W = CPP_STD + cpp("""
    int n; in >> n;
    int mx = 0;
    vector<int> a(n);
    for (auto& x : a) { in >> x; mx = max(mx, x); }
    vector<int> cnt(mx + 1, 0);
    for (int x : a) ++cnt[x];
    // WRONG: counts every pair sharing ANY divisor d >= 2 — a pair with
    // gcd 6 is counted at d = 2, 3, and 6. Mobius inclusion-exclusion is
    // required; this overcounts whenever values share several primes.
    long long total = 0;
    for (int d = 2; d <= mx; ++d) {
        long long c = 0;
        for (int v = d; v <= mx; v += d) c += cnt[v];
        total += c * (c - 1) / 2;
    }
    out << total << "{{NL}}";
""") + END

# ------------------------------------------------------------------ p20 practice bodies
P1_R = CPP_STD + cpp("""
    // Subarrays summing to exactly S: prefix + hash map.
    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // simple open-addressing map via sorted vector is overkill; use map
    // semantics through an unordered_map
    // (educational version keeps the standard container)
    map<long long, long long> seen;
    seen[0] = 1;
    long long cur = 0, cnt = 0;
    for (long long x : a) {
        cur += x;
        auto it = seen.find(cur - S);
        if (it != seen.end()) cnt += it->second;
        ++seen[cur];
    }
    out << cnt << "{{NL}}";
""") + END

P1_W = CPP_STD + cpp("""
    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: two-pointer shrink assumes all values non-negative — with
    // negative values the window sum is not monotone and counts break.
    long long cnt = 0, cur = 0;
    int lo = 0;
    for (int hi = 0; hi < n; ++hi) {
        cur += a[hi];
        while (lo <= hi && cur > S) { cur -= a[lo]; ++lo; }
        if (cur == S) ++cnt;
    }
    out << cnt << "{{NL}}";
""") + END

P2_R = CPP_STD + cpp("""
    // BFS over (row, col, hasKey).
    int R, C; in >> R >> C;
    vector<string> g(R);
    for (auto& row : g) in >> row;
    int sr = 0, sc = 0, kr = -1, kc = -1;
    for (int r = 0; r < R; ++r)
        for (int c = 0; c < C; ++c) {
            if (g[r][c] == 'S') { sr = r; sc = c; }
            if (g[r][c] == 'K') { kr = r; kc = c; }
        }
    vector<vector<array<char, 2>>> seen(R, vector<array<char, 2>>(C, {0, 0}));
    vector<array<int, 3>> q;
    q.push_back({sr, sc, 0});
    seen[sr][sc][0] = 1;
    int head = 0, dist = 0;
    while (head <= (int)q.size() - 1) {
        int sz = (int)q.size();
        for (int t = head; t < sz; ++t) {
            auto [r, c, hk] = q[t];
            if (g[r][c] == 'E') { out << dist << "{{NL}}"; return; }
            int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
            for (int d4 = 0; d4 < 4; ++d4) {
                int nr = r + dr[d4], nc = c + dc[d4];
                if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
                char ch = g[nr][nc];
                if (ch == '#') continue;
                if (ch == 'D' && !hk) continue;
                int nhk = hk || (nr == kr && nc == kc);
                if (!seen[nr][nc][nhk]) {
                    seen[nr][nc][nhk] = 1;
                    q.push_back({nr, nc, nhk});
                }
            }
        }
        head = sz;
        ++dist;
    }
    out << -1 << "{{NL}}";
""") + END

P2_W = CPP_STD + cpp("""
    int R, C; in >> R >> C;
    vector<string> g(R);
    for (auto& row : g) in >> row;
    int sr = 0, sc = 0;
    for (int r = 0; r < R; ++r)
        for (int c = 0; c < C; ++c)
            if (g[r][c] == 'S') { sr = r; sc = c; }
    // WRONG: plain BFS — the key state is dropped, so the door is either
    // an impassable wall (key forgotten) or a free shortcut (stateless);
    // either way the path length is wrong on keyed mazes.
    vector<vector<char>> seen(R, vector<char>(C, 0));
    vector<pair<int, int>> q;
    q.push_back({sr, sc});
    seen[sr][sc] = 1;
    int head = 0, dist = 0;
    while (head <= (int)q.size() - 1) {
        int sz = (int)q.size();
        for (int t = head; t < sz; ++t) {
            auto [r, c] = q[t];
            if (g[r][c] == 'E') { out << dist << "{{NL}}"; return; }
            int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
            for (int d4 = 0; d4 < 4; ++d4) {
                int nr = r + dr[d4], nc = c + dc[d4];
                if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
                if (g[nr][nc] == '#' || g[nr][nc] == 'D') continue;
                if (!seen[nr][nc]) { seen[nr][nc] = 1; q.push_back({nr, nc}); }
            }
        }
        head = sz;
        ++dist;
    }
    out << -1 << "{{NL}}";
""") + END

P3_R = CPP_STD + cpp("""
    // Count x in [1, N] with digitSum(x) % k == 0 (digit DP).
    string N; int k; in >> N >> k;
    int L = (int)N.size();
    vector<vector<long long>> fr(L + 1, vector<long long>(k, 0));
    fr[L][0] = 1;
    for (int i = L - 1; i >= 0; --i)
        for (int m = 0; m < k; ++m)
            for (int d = 0; d <= 9; ++d)
                fr[i][(m + d) % k] += fr[i + 1][m];
    long long total = 0;
    int mod = 0;
    for (int i = 0; i < L; ++i) {
        int di = N[i] - '0';
        for (int d = 0; d < di; ++d)
            total += fr[i + 1][(k - (mod + d) % k) % k];  // suffix supplies the complement
        mod = (mod + di) % k;
    }
    if (mod == 0) ++total;
    out << total - 1 << "{{NL}}";  // exclude x = 0
""") + END

P3_W = CPP_STD + cpp("""
    string N; int k; in >> N >> k;
    // WRONG: enumerates every number up to N — N = 1e18 never finishes.
    long long x = 1, cnt = 0;
    while (true) {
        long long t = x, ds = 0;
        while (t) { ds += t % 10; t /= 10; }
        if (ds % k == 0) ++cnt;
        if (x == stoll(N)) break;
        ++x;
    }
    out << cnt << "{{NL}}";
""") + END

# ------------------------------------------------------------------ ground truths
A1_T1 = [3, 1, 4, 1, 5, 9, 2, 6]
assert m_inv2_brute(A1_T1) == m_inv2_bit(A1_T1)
_rng = random.Random(20)
A1_T2 = [_rng.randint(-1000, 1000) for _ in range(2000)]
assert m_inv2_brute(A1_T2) == m_inv2_bit(A1_T2)
A1_T3 = [_rng.randint(-10**6, 10**6) for _ in range(200000)]
A1_WANT3 = m_inv2_bit(A1_T3)

A2_T1 = ([1, 2, 3, 4], 2)
assert m_cargo_brute(*A2_T1) == 6
assert m_cargo_bs(*A2_T1, strict=False) == 6
assert m_cargo_bs(*A2_T1, strict=True) == 10
A2_T2 = ([5, 1, 3, 5, 2, 8], 3)
assert m_cargo_brute(*A2_T2) == m_cargo_bs(*A2_T2, strict=False)
_rng2 = random.Random(201)
A2_T3 = [_rng2.randint(1, 10**9) for _ in range(200000)]
A2_WANT3 = m_cargo_bs(A2_T3, 25, strict=False)

A3_T1 = [(0, 0), (4, 0), (4, 4), (2, 1), (0, 4)]
assert m_hull_area2(A3_T1) == 32
assert m_shoelace2(A3_T1) != 32
A3_T2 = [(0, 0), (2, 0), (2, 2), (0, 2)]
assert m_hull_area2(A3_T2) == 8 and m_shoelace2(A3_T2) == 8
A3_T3 = [(0, 0), (1, 1), (2, 2)]  # collinear
assert m_hull_area2(A3_T3) == 0
_rng3 = random.Random(202)
A3_T4 = [(_rng3.randint(0, 10**6), _rng3.randint(0, 10**6)) for _ in range(200000)]
A3_WANT4 = m_hull_area2(A3_T4)
assert m_shoelace2(A3_T4) != A3_WANT4

A4_T1 = [6, 10, 15]
assert m_coprime_pairs(A4_T1) == 0
assert m_coprime_w(A4_T1) == 3
A4_T2 = [2, 3, 5, 7]
assert m_coprime_pairs(A4_T2) == 6
_rng4 = random.Random(203)
A4_T3 = [_rng4.randint(1, 10**6) for _ in range(100000)]
A4_WANT3 = m_coprime_pairs(A4_T3)
assert m_coprime_w(A4_T3) != A4_WANT3

P1_T1 = ([1, -1, 1, -1], 0)
assert m_subsum(*P1_T1) == 4
assert m_subsum_w(*P1_T1) != 4
P1_T2 = ([1, 2, 3], 3)
assert m_subsum(*P1_T2) == 2 and m_subsum_w(*P1_T2) == 2
_rng5 = random.Random(204)
P1_T3 = [_rng5.randint(-5, 5) for _ in range(200000)]
P1_WANT3 = m_subsum(P1_T3, 3)

P2_T1 = [
    "S..",
    ".##",
    "KDE",
]
# E sits behind the door; the key is on the left column
assert m_grid_bfs(P2_T1, True) == 4
assert m_grid_bfs(P2_T1, False) == -1  # W: door impassable, exit unreachable
P2_T2 = [
    "S.E",
]
assert m_grid_bfs(P2_T2, True) == 2 and m_grid_bfs(P2_T2, False) == 2
_rng6 = random.Random(205)
P2_R3, P2_C3 = 200, 200
P2_G3 = []
for r in range(P2_R3):
    row = []
    for c in range(P2_C3):
        row.append("#" if _rng6.random() < 0.28 else ".")
    P2_G3.append("".join(row))
P2_G3[0] = "S" + P2_G3[0][1:]
P2_G3[P2_R3 - 1] = P2_G3[P2_R3 - 1][:-1] + "E"
P2_G3[P2_R3 // 2] = P2_G3[P2_R3 // 2][:P2_C3 // 2] + "K" + P2_G3[P2_R3 // 2][P2_C3 // 2 + 1:]
# guarantee a door-free route exists by clearing row 0 and the middle column walkway
P2_G3[0] = "S" + "." * (P2_C3 - 2) + "."  # top row clear
P2_G3[P2_R3 - 1] = "." * (P2_C3 - 1) + "E"
P2_G3[P2_R3 // 2] = "." * P2_C3
P2_G3[P2_R3 // 2] = P2_G3[P2_R3 // 2][:P2_C3 // 2] + "K" + P2_G3[P2_R3 // 2][P2_C3 // 2 + 1:]
# carve vertical corridor at column 0 and a door on the middle row right side
P2_G3 = [list(row) for row in P2_G3]
for r in range(P2_R3):
    P2_G3[r][0] = "." if P2_G3[r][0] != "S" else "S"
P2_G3[P2_R3 // 2][P2_C3 - 2] = "D"
P2_G3 = ["".join(row) for row in P2_G3]
P2_WANT3 = m_grid_bfs(P2_G3, True)

P3_T1 = (20, 3)
assert m_digitdp(*P3_T1) == m_digitdp_brute(*P3_T1)
_rng7 = random.Random(206)
for _ in range(200):
    N = _rng7.randint(1, 100000)
    k = _rng7.randint(2, 12)
    assert m_digitdp(N, k) == m_digitdp_brute(N, k), (N, k)
P3_T2 = (10**18, 7)
P3_WANT2 = m_digitdp(*P3_T2)

# ------------------------------------------------------------------ tests
A1_TESTS = [
    contest_test("small mix", T("8", "3", "1", "4", "1", "5", "9", "2", "6"),
        T(str(m_inv2_brute(A1_T1))),
        "Sweep right-to-left counting earlier 2*a[j] strictly below a[i]."),
    contest_test("negatives allowed", T("2000", " ".join(map(str, A1_T2))),
        T(str(m_inv2_bit(A1_T2))),
        "Negative values break divide-and-conquer assumptions; the BIT only needs ranks."),
    contest_test(
        "load: 200000 values",
        T("200000", " ".join(map(str, A1_T3))),
        T(str(A1_WANT3)),
        "O(n log n) sweep + BIT; the all-pairs scan is 2e10 comparisons."),
]

A2_TESTS = [
    contest_test("four crates, two trucks", T("4 2", "1", "2", "3", "4"), T("6"),
        "Best split [1,2,3 | 4]: max segment 6. Strict-< W overshoots to 10."),
    contest_test("three trucks", T("6 3", "5", "1", "3", "5", "2", "8"),
        T(str(m_cargo_brute(*A2_T2))),
        "Predicate must be parts(mid) <= k."),
    contest_test(
        "load: 200000 values up to 1e9, 25 trucks",
        T("200000 25", " ".join(map(str, A2_T3))),
        T(str(A2_WANT3)),
        "Binary search over the answer: O(n log(sum))."),
]

A3_TESTS = [
    contest_test("concave input order", T("5", "0 0", "4 0", "4 4", "2 1", "0 4"), T("32"),
        "The hull is the square (0,0)-(4,0)-(4,4)-(0,4); input-order shoelace misfolds at (2,1)."),
    contest_test("convex square", T("4", "0 0", "2 0", "2 2", "0 2"), T("8"),
        "Already convex and ordered: both approaches agree."),
    contest_test("collinear", T("3", "0 0", "1 1", "2 2"), T("0"),
        "Degenerate hull: zero area."),
    contest_test(
        "load: 200000 random points",
        T("200000", *[("%d %d" % p) for p in A3_T4]),
        T(str(A3_WANT4)),
        "Monotone chain is O(n log n); input-order shoelace is wrong AND order-blind."),
]

A4_TESTS = [
    contest_test("pairwise non-coprime, gcd 1 overall", T("3", "6", "10", "15"), T("0"),
        "Every pair shares exactly one prime (2, 3, 5): Mobius cancels to 0; the naive divisor count says 3."),
    contest_test("all coprime primes", T("4", "2", "3", "5", "7"), T("6"),
        "C(4,2) pairs, all gcd 1."),
    contest_test(
        "load: 100000 values up to 1e6",
        T("100000", " ".join(map(str, A4_T3))),
        T(str(A4_WANT3)),
        "Mobius sieve over the value range; harmonic divisor sums stay linear."),
]

P1_TESTS = [
    contest_test("negative values", T("4 0", "1", "-1", "1", "-1"), T("4"),
        "Four subarrays sum to 0. The two-pointer W miscounts with negatives."),
    contest_test("positive sanity", T("3 3", "1", "2", "3"), T("2"),
        "[1,2] and [3]: both approaches agree here."),
    contest_test(
        "load: 200000 mixed values, S = 3",
        T("200000 3", " ".join(map(str, P1_T3))),
        T(str(P1_WANT3)),
        "Prefix + hash map is O(n)."),
]

P2_TESTS = [
    contest_test("keyed maze", T("3 3", "S..", ".##", "KDE"), T("4"),
        "Down for the key, then through the door: 4 steps. Stateless W leaves E unreachable (-1)."),
    contest_test("no door", T("1 3", "S.E"), T("2"),
        "Without a door both searches agree."),
    contest_test(
        "load: 200x200 maze with key and door",
        T("200 200", *P2_G3),
        T(str(P2_WANT3)),
        "BFS over (row, col, hasKey) states — 2x the grid."),
]

P3_TESTS = [
    contest_test("small bound", T("20 3"), T(str(m_digitdp_brute(20, 3))),
        "Digit sums divisible by 3 up to 20: 3, 6, 9, 12, 15, 18 — plus 20? 2+0=2 no. Brute-verified."),
    contest_test(
        "load: N = 1e18, k = 7",
        T("1000000000000000000 7"),
        T(str(P3_WANT2)),
        "Digit DP walks 19 positions x k states; enumeration never terminates."),
]

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Final HSG Simulation",
    "The closing contest set: sweeps, answer binary search, convex hulls, Mobius counting, and a mixed drill.",
    "Kỳ thi giả lập HSG cuối",
    "Bộ kỳ thi khép lại: quét tuyến tính, tìm kiếm nhị phân đáp án, bao lồi, đếm Mobius, và bài tập tổng hợp.",
    ["hsga-m20-pace", "hsga-m20-ladder", "hsga-cp-m20a", "hsga-cp-m20b",
     "hsga-cp-m20c", "hsga-cp-m20d"],
    ["hsga-p20-mixed"],
)

write_lesson(
    M, "hsga-m20-pace",
    "Pacing the Full Simulation",
    "A full HSG paper is a resource-allocation problem: the score is the sum of what you finish, not what you attempt.",
    30,
    """
# Pacing

Divide the paper into three passes. Pass 1 (first 20% of time): read
everything, solve every problem whose full solution is already clear —
these are the points that fund the rest. Pass 2 (next 60%): the two
hardest problems you believe you can finish, alternating when stuck.
Pass 3 (final 20%): bank partial scores — write the subtask brute
forces, verify formats, re-read statements for missed constraints.

Track a simple rule: if 30 minutes produce no new invariant, bank what
you have and switch. Returning later with fresh eyes is a strategy,
not a defeat.
""", "Phân bổ cả kỳ thi",
    "Một đề HSG đầy đủ là bài toán phân bổ tài nguyên: điểm là tổng những gì bạn HOÀN THÀNH.",
    """
# Chia ba lượt

Lượt 1 (20% thời gian đầu): đọc hết đề, giải ngay bài đã rõ lời giải
đầy đủ — đây là vốn điểm. Lượt 2 (60% giữa): hai bài khó nhất bạn tin
mình xong, luân phiên khi bí. Lượt 3 (20% cuối): gom điểm một phần —
viết brute force cho subtask, soát định dạng in, đọc lại đề tìm ràng
buộc bỏ sót.

Quy tắc: 30 phút không ra bất biến mới thì gom phần đã có và chuyển
bài. Quay lại sau với đầu óc mới là chiến thuật, không phải thất bại.
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m20-ladder",
    "The Submission Ladder",
    "Rank problems by expected points per minute and climb the ladder: guaranteed partials first, full solutions second, gambles last.",
    30,
    """
# Expected points per minute

For every open problem, estimate: P(full solve) x full points vs
P(subtask) x partial points, divided by the minutes each needs. Submit
the best ratio first. A 40-point subtask at minute 40 usually beats a
100-point gamble at minute 150.

Keep every partial-score opportunity alive: constraints listed in the
statement ARE the subtask map. n <= 1000 means the O(n^2) writer is
being invited. Two independent constraints usually mean two independent
partial solutions.
""", "Thang điểm nộp bài",
    "Xếp bài theo điểm kỳ vọng mỗi phút: điểm một phần chắc chắn trước, lời giải đầy đủ sau, đánh cược cuối.",
    """
# Điểm kỳ vọng trên mỗi phút

Với mỗi bài đang mở, ước lượng: P(giải hết) x điểm đầy đủ so với
P(subtask) x điểm một phần, chia số phút cần. Nộp tỉ số tốt nhất trước.
Subtask 40 điểm ở phút 40 thường thắng canh bạc 100 điểm ở phút 150.

Giữ sống mọi cơ hội điểm một phần: các ràng buộc trong đề CHÍNH LÀ bản
đồ subtask. n <= 1000 nghĩa là người viết O(n^2) đang được mời. Hai
ràng buộc độc lập thường là hai lời giải một phần độc lập.
""", difficulty="advanced",
)

CP_A = challenge(
    "hsga-cp20-invd",
    "Inversion Doubles",
    """**Problem.** Line 1: n. Line 2: n integers (may be negative). Print
the number of pairs i < j with a[i] > 2*a[j].

**Constraints:** 1 <= n <= 200000; |a[i]| <= 1e6.

Sweep + BIT synthesis; negatives allowed.
""",
    A1_TESTS, level="real-world", difficulty="advanced")

VI_A = vi_challenge(
    "Đảo đôi",
    """**Bài toán.** Đếm cặp i < j với a[i] > 2·a[j]. Giá trị có thể âm.""",
    [("kỹ thuật", "Nén toạ độ {a, 2a} + Fenwick, quét từ phải sang trái."),
     ("bẫy", "Quét mọi cặp là O(n^2)."),
     ("âm", "Chỉ cần thứ tự tương đối — giá trị âm không sao.")],
)

CP_B = challenge(
    "hsga-cp20-cargo",
    "Cargo Split",
    """**Problem.** Line 1: n k. Line 2: n shipment weights. Split them
into at most k contiguous blocks minimizing the largest block total.
Print that minimum.

**Constraints:** 1 <= k <= n <= 200000; 1 <= a[i] <= 1e9.

**R versus W.** The graded wrong solution binary-searches with a
strictly-fewer-parts predicate.
""",
    A2_TESTS, level="real-world", difficulty="advanced")

VI_B = vi_challenge(
    "Chia hàng",
    """**Bài toán.** Chia mảng thành tối đa k đoạn liền kề sao cho tổng đoạn
lớn nhất là nhỏ nhất.""",
    [("tìm nhị phân đáp án", "Chặt ƯLN của tổng lớn nhất; greedy đếm đoạn."),
     ("bẫy", "Vị từ parts(mid) < k làm kết quả vượt tối ưu."),
     ("phức tạp", "O(n log tổng).")],
)

CP_C = challenge(
    "hsga-cp20-fence",
    "Fence Blueprint",
    """**Problem.** Line 1: n. Then n points. Print the doubled area of
their convex hull (an integer; 0 if the hull is degenerate).

**Constraints:** 1 <= n <= 200000; coordinates up to 1e6 in absolute
value; the doubled area fits in 64 bits.

**R versus W.** The graded wrong solution applies the shoelace formula
to the INPUT order instead of the hull.
""",
    A3_TESTS, level="real-world", difficulty="advanced")

VI_C = vi_challenge(
    "Bản đồ hàng rào",
    """**Bài toán.** In diện tích nhân đôi của bao lồi (số nguyên; 0 nếu suy
biến).""",
    [("bao lồi", "Monotone chain với tích có hướng thuần số nguyên."),
     ("bẫy", "Shoelace theo THỨ TỰ NHẬP chỉ đúng với đa giác lồi đã xếp."),
     ("độ chính xác", "Nhân đôi tránh chia; long long đủ.")],
)

CP_D = challenge(
    "hsga-cp20-coprime",
    "Coprimality Census",
    """**Problem.** Line 1: n. Line 2: n values. Print the number of pairs
i < j with gcd(a[i], a[j]) == 1.

**Constraints:** 1 <= n <= 100000; 1 <= a[i] <= 1e6.

**R versus W.** The graded wrong solution counts every pair sharing
any common divisor >= 2.
""",
    A4_TESTS, level="real-world", difficulty="advanced")

VI_D = vi_challenge(
    "Điều tra nguyên tố cùng nhau",
    """**Bài toán.** Đếm cặp i < j với gcd(a[i], a[j]) = 1.""",
    [("Mobius", "Đáp án = Σ mu(d)·C(c_d, 2) với c_d = số phần tử chia hết cho d."),
     ("bẫy", "Σ_{d≥2} C(c_d,2) đếm trùm — cặp gcd 6 bị đếm ở d = 2, 3, 6."),
     ("sàng", "Mobius tuyến tính tới 1e6.")],
)

write_checkpoint(
    M, "hsga-cp-m20a",
    "Final 1-A: Inversion Doubles",
    "Final simulation, problem A: sweep + BIT with negative values. Target: solved within 40 minutes.",
    40,
    """**Final 1-A — Inversion Doubles.** Count a[i] > 2*a[j] pairs over
200000 possibly-negative values: coordinate-compress {a, 2a}, sweep
right-to-left with a Fenwick tree. Graded near-miss: all-pairs scan.

**Final 1-A.** The sweep reuses the inversion template with a doubling
twist; negatives cost nothing because only ranks matter.
""",
    "Final 1-A: Đảo đôi",
    "Kỳ thi cuối, bài A: quét + BIT với giá trị âm. Mục tiêu: 40 phút.",
    """**Final 1-A — Đảo đôi.** Đếm cặp a[i] > 2·a[j] trên 200000 giá trị có
thể âm: nén toạ độ {a, 2a}, quét phải-sang-trái với Fenwick. Near-miss
bị chấm: quét mọi cặp. Giá trị âm không sao vì chỉ cần thứ tự tương
đối.""",
    CP_A, VI_A,
    solution=A1_R,
    wrong=A1_W,
)

write_checkpoint(
    M, "hsga-cp-m20b",
    "Final 1-B: Cargo Split",
    "Final simulation, problem B: binary search on the answer with a greedy check. Target: solved within 40 minutes.",
    40,
    """**Final 1-B — Cargo Split.** Minimize the largest contiguous block
with at most k blocks: binary-search the answer, greedy-count parts,
predicate parts(mid) <= k. Graded near-miss: strict < predicate.

**Final 1-B.** The wrong predicate returns a feasible-but-suboptimal
limit — visible on the very first test.
""",
    "Final 1-B: Chia hàng",
    "Kỳ thi cuối, bài B: tìm nhị phân trên đáp án với kiểm tra tham lam. Mục tiêu: 40 phút.",
    """**Final 1-B — Chia hàng.** Tối thiểu hoá tổng đoạn lớn nhất với tối đa
k đoạn: chặt đáp án, greedy đếm đoạn, vị từ parts(mid) <= k. Near-miss
bị chấm: vị từ < nghiêm ngặt — trả về giới hạn khả thi nhưng vượt tối
ưu, lộ ngay ở test đầu.""",
    CP_B, VI_B,
    solution=A2_R,
    wrong=A2_W,
)

write_checkpoint(
    M, "hsga-cp-m20c",
    "Final 2-A: Fence Blueprint",
    "Final simulation, problem C: convex hull + integer shoelace. Target: solved within 40 minutes.",
    40,
    """**Final 2-A — Fence Blueprint.** Strict monotone-chain hull, then a
doubled shoelace over the HULL, not the input. Graded near-miss:
shoelace on the input order.

**Final 2-A.** The wrong version agrees only on convex, pre-ordered
polygons; the concave and random-order tests break it.
""",
    "Final 2-A: Bản đồ hàng rào",
    "Kỳ thi cuối, bài C: bao lồi + shoelace số nguyên. Mục tiêu: 40 phút.",
    """**Final 2-A — Bản đồ hàng rào.** Monotone chain nghiêm ngặt, rồi
shoelace nhân đôi trên BAO LỒI, không phải thứ tự nhập. Near-miss bị
chấm: shoelace theo thứ tự nhập — chỉ đúng với đa giác lồi đã xếp sẵn.""",
    CP_C, VI_C,
    solution=A3_R,
    wrong=A3_W,
)

write_checkpoint(
    M, "hsga-cp-m20d",
    "Final 2-B: Coprimality Census",
    "Final simulation, problem D: Mobius inclusion-exclusion over the value range. Target: solved within 40 minutes.",
    40,
    """**Final 2-B — Coprimality Census.** gcd == 1 pairs: total =
Sum mu(d) * C(c_d, 2). Graded near-miss: summing C(c_d, 2) for every
d >= 2 without the Mobius signs.

**Final 2-B.** The wrong version triple-counts pairs like (6, 10, 15)
whose gcds share several primes — the classic inclusion-exclusion
failure.
""",
    "Final 2-B: Điều tra nguyên tố cùng nhau",
    "Kỳ thi cuối, bài D: loại trừ bao hàm Mobius trên dải giá trị. Mục tiêu: 40 phút.",
    """**Final 2-B — Điều tra nguyên tố cùng nhau.** Cặp gcd = 1: tổng =
Σ mu(d)·C(c_d, 2). Near-miss bị chấm: cộng C(c_d, 2) cho mọi d ≥ 2 mà
không có dấu Mobius — đếm trùm kinh điển của loại trừ bao hàm.""",
    CP_D, VI_D,
    solution=A4_R,
    wrong=A4_W,
)

# ------------------------------------------------------------------ practice
PR_A = challenge(
    "hsga-p20-subsum",
    "Lucky Receipts",
    """**Problem.** Line 1: n S. Line 2: n integers (may be negative). Print
the number of contiguous subarrays whose sum is exactly S.

**Constraints:** 1 <= n <= 200000; |a[i]|, |S| <= 1e9.

Two-pointer shrinking is the classic near-miss here.
""",
    P1_TESTS, level="combination", difficulty="advanced")

VIP1 = vi_challenge(
    "Hoá đơn may mắn",
    """**Bài toán.** Đếm đoạn con liên tiếp có tổng đúng bằng S. Giá trị có
thể âm.""",
    [("prefix + map", "Đếm prefix đã gặp: cur − S."),
     ("bẫy", "Hai con trỏ co giãn chỉ đúng khi toàn dương."),
     ("kích thước", "n = 2e5: O(n).")],
)

PR_B = challenge(
    "hsga-p20-maze",
    "Keyed Maze",
    """**Problem.** A grid maze: '.', '#', 'S' (start), 'E' (exit), 'K'
(key), 'D' (locked door — passable only after picking up the key).
Print the minimum number of steps from S to E, or -1.

**Constraints:** 1 <= R, C <= 500.

**R versus W.** The graded wrong solution runs BFS without the key
state.
""",
    P2_TESTS, level="combination", difficulty="advanced")

VIP2 = vi_challenge(
    "Mê cung khoá",
    """**Bài toán.** Lưới mê cung: '.','#','S','E','K' (chìa khoá),'D' (cửa
khoá). In số bước ít nhất từ S tới E, hoặc -1.""",
    [("trạng thái", "BFS trên (hàng, cột, có-khoá) — không gian gấp đôi."),
     ("bẫy", "BFS thường mất trạng thái khoá: cửa hoặc tường sai hoặc lối tắt sai."),
     ("kích thước", "500x500: 2 trạng thái mỗi ô.")],
)

PR_C = challenge(
    "hsga-p20-digitdp",
    "Digit Harmony",
    """**Problem.** Line 1: N (up to 1e18, given as a string). Line 2: k.
Print how many x in [1, N] have digitSum(x) divisible by k.

**Constraints:** 1 <= N <= 1e18; 2 <= k <= 100.

**R versus W.** The graded wrong solution enumerates every number.
""",
    P3_TESTS, level="combination", difficulty="advanced")

VIP3 = vi_challenge(
    "Hoà âm chữ số",
    """**Bài toán.** Đếm x trong [1, N] có tổng chữ số chia hết cho k.""",
    [("digit DP", "Trạng thái (vị trí, tổng mod k, bám biên)."),
     ("bẫy", "Liệt kê từng số — N = 1e18 không bao giờ xong."),
     ("biên", "Trừ x = 0 (tổng chữ số 0, chia hết cho mọi k).")],
)

write_practice(
    M, "hsga-p20-mixed", "Mixed Drill — Final Synthesis",
    "Three timed synthesis problems: prefix counting, state-space BFS, and digit DP.",
    "Bài tập hỗn hợp — tổng hợp cuối",
    "Ba bài tổng hợp có tính giờ: đếm prefix, BFS không gian trạng thái, và digit DP.",
    "hsga-m20-ladder",
    110,
    "advanced",
    [PR_A, PR_B, PR_C],
    {
        "hsga-p20-mixed": vi_challenge(
            "Bài tập hỗn hợp III",
            """**Bài toán.** Ba bài: đếm đoạn con tổng S, mê cung có chìa khoá,
và đếm số có tổng chữ số chia hết cho k.""",
            [("đoạn con", "Prefix + bản đếm."),
             ("mê cung", "BFS (hàng, cột, khoá)."),
             ("chữ số", "Digit DP với trạng thái mod.")],
        ),
    },
    solutions=[
        ("hsga-p20-subsum", P1_R, P1_W),
        ("hsga-p20-maze", P2_R, P2_W),
        ("hsga-p20-digitdp", P3_R, P3_W),
    ],
)

print("module m20 complete")
