#!/usr/bin/env python3
"""HSG Advanced — Module 8: hsga-scc (SCC & Condensation).

Iterative Kosaraju, SCC counting with sizes, condensation-edge counting,
and "the condensation is a DAG" reasoning. Wrong solutions: one-sided DFS
reachability (behavioral), and an O(n·m) per-pair reachability near-miss.

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
#include <set>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-scc"


# ---------------------------------------------------------------- models
def _kosaraju(n, edges):
    adj = [[] for _ in range(n + 1)]
    radj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        radj[v].append(u)
    vis = [False] * (n + 1)
    order = []
    for s in range(1, n + 1):
        if vis[s]:
            continue
        st = [(s, False)]
        while st:
            u, d = st.pop()
            if d:
                order.append(u)
                continue
            if vis[u]:
                continue
            vis[u] = True
            st.append((u, True))
            for v in adj[u]:
                if not vis[v]:
                    st.append((v, False))
    comp = [0] * (n + 1)
    c = 0
    for s in reversed(order):
        if comp[s]:
            continue
        c += 1
        st = [s]
        comp[s] = c
        while st:
            u = st.pop()
            for v in radj[u]:
                if not comp[v]:
                    comp[v] = c
                    st.append(v)
    return comp, c


def _cond_edges(n, edges):
    comp, c = _kosaraju(n, edges)
    ce = set()
    for u, v in edges:
        if comp[u] != comp[v]:
            ce.add((comp[u], comp[v]))
    return len(ce)


def _gen_pairs(n):
    """Deterministic: pairs (2k-1, 2k) form 2-cycles chained forward."""
    edges = []
    half = n // 2
    for k in range(1, half + 1):
        a, b = 2 * k - 1, 2 * k
        edges.append((a, b))
        edges.append((b, a))
        if k < half:
            edges.append((b, a + 2))
    return edges


def _gen_bigcycle(n):
    edges = []
    for v in range(1, n):
        edges.append((v, v + 1))
    edges.append((n, 1))
    return edges


# ---------------------------------------------------------------- lessons
write_module(
    M,
    "Strongly Connected Components",
    "Kosaraju's two-pass DFS finds every SCC in O(n + m); shrinking components turns any digraph into a DAG, unlocking the whole Intermediate DAG toolbox.",
    "Thành phần liên thông mạnh",
    "Hai lượt DFS của Kosaraju tìm mọi SCC trong O(n + m); co thành phần biến mọi đồ thị có hướng thành DAG, mở khóa toàn bộ công cụ DAG của Trung cấp.",
    ["hsga-m8-kosaraju", "hsga-m8-condensation", "hsga-m8-recognize", "hsga-cp-m8"],
    ["hsga-p8-scc"],
)

write_lesson(
    M, "hsga-m8-kosaraju",
    "Kosaraju's Two Passes",
    "One DFS on G records finish order; one DFS on the reverse graph in reverse finish order labels every SCC — proven by the finish-time ordering.",
    35,
    """
# Two passes, one theorem

Pass 1: DFS over G, push each node when its DFS finishes. Pass 2: DFS
over the REVERSE graph G^T, starting from unvisited nodes in decreasing
finish order; each pass-2 tree is exactly one SCC.

Why it is correct: the node u with the largest finish time lies in a
"source" SCC C of the condensation. Reversing the graph makes C a sink —
no edges leave C in G^T, so its pass-2 DFS cannot escape, and every
other SCC is still reachable FROM C in G^T exactly when C was reachable
from it in G. Induction on the condensation finishes the proof.

Implementation must be ITERATIVE on both passes: the 2·10^5-node
recursion-depth wall applies to the reverse pass too. Record edges of
G^T once, up front.
""",
    "Kosaraju hai lượt",
    "Một DFS trên G ghi thứ tự kết thúc; một DFS trên đồ thị NGƯỢC theo thứ tự kết thúc ngược gán nhãn từng SCC — chứng minh bằng thứ tự thời điểm kết thúc.",
    """
# Hai lượt, một định lý

Lượt 1: DFS trên G, đẩy nút vào stack khi DFS của nó kết thúc. Lượt 2:
DFS trên đồ thị NGƯỢC G^T, bắt đầu từ các nút chưa thăm theo thứ tự kết
thức giảm dần; mỗi cây DFS lượt 2 là đúng một SCC.

Vì sao đúng: nút u có thời điểm kết thúc lớn nhất nằm ở SCC "nguồn" C
của phép co. Đảo chiều đồ thị biến C thành bể — không cạnh nào rời C
trong G^T, nên DFS lượt 2 không thể thoát khỏi C, và mọi SCC khác vẫn
với được TỪ C trong G^T đúng khi C với được từ nó trong G. Quy nạp trên
phép co kết thúc chứng minh.

Cài đặt phải LẶP trên cả hai lượt: bức tường sâu đệ quy 2·10^5 đỉnh áp
dụng cho lượt ngược nữa. Dự sẵn danh sách cạnh G^T một lần.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m8-condensation",
    "Condensation: Every Digraph Is a DAG",
    "Shrink each SCC to one node and the result is acyclic — DP on the condensation inherits every Intermediate DAG technique.",
    35,
    """
# The condensation is a DAG

If the condensation had a cycle, its SCCs would merge into one — so it
is acyclic by construction. Consequences students must internalize:

- Counting distinct condensation edges needs a SET of (comp[u], comp[v])
  pairs: m raw edges collapse to far fewer.
- Any "can u reach v" question now runs on a DAG where you can DP:
  longest path, reachability bitsets, counting paths — all O(n + m) on
  the shrunk graph.
- Chain decomposition of answers: SCC for cycles, then DAG DP for order.
  Provincial problems love this two-step shape.

The classic bug: forgetting that self-loops and duplicate edges
disappear in the condensation (a self-loop is inside one SCC; duplicates
are one edge).
""",
    "Phép co: mọi đồ thị thành DAG",
    "Co mỗi SCC thành một nút và kết quả không có chu trình — DP trên phép co kế thừa mọi kỹ thuật DAG của Trung cấp.",
    """
# Phép co là DAG

Nếu phép co có chu trình, các SCC đó sẽ gộp thành một — vậy nó không có
chu trình do cấu trúc. Hệ quả cần thấm:

- Đếm cạnh co PHÂN BIỆT cần tập SET các cặp (comp[u], comp[v]): m cạnh
  thô co lại còn ít hơn nhiều.
- Mọi câu "u với được v?" giờ chạy trên DAG nơi bạn được DP: đường dài
  nhất, reachability bitset, đếm đường đi — hết O(n + m) trên đồ thị co.
- Công thức chia để trả lời: SCC cho chu trình, rồi DAG DP cho thứ tự.
  Đề tỉnh rất mê dạng hai bước này.

Lỗi kinh điển: quên rằng self-loop và cạnh trùng biến mất trong phép co
(self-loop nằm trong một SCC; cạnh trùng là một cạnh).
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m8-recognize",
    "Recognizing SCC Problems",
    "Mutual reachability, 2-cycles, 'in the same group', and any digraph DP that must ignore back edges — the four signatures of SCC.",
    35,
    """
# The four signatures

1. "u can reach v AND v can reach u" — mutual reachability IS the SCC
   relation.
2. Bidirectional pairs / swaps that propagate: if swapping i and j is
   allowed and j and k too, one component {i, j, k} forms.
3. "Group", "clique of reachability" — sizes of SCCs are the answer.
4. DP on a digraph where back edges break your state — condense first,
   then the Intermediate DAG DP applies.

Anti-signature: a DAG needs no SCC pass; undirected connectivity is
M5/Intermediate territory. SCC is for DIRECTED cycles with structure.
""",
    "Nhận diện bài SCC",
    "Tương hỗ với được, chu trình đôi, 'cùng nhóm', và mọi DP trên đồ thị có hướng mà cạnh ngược phá trạng thái — bốn dấu hiệu của SCC.",
    """
# Bốn dấu hiệu

1. "u với được v VÀ v với được u" — tính tương hỗ CHÍNH là quan hệ SCC.
2. Cặp hoán đổi hai chiều lan truyền: được đổi i với j, được đổi j với
   k — thành phần {i, j, k} hình thành.
3. "Nhóm", "độ bao phủ bằng với được" — kích thước SCC chính là đáp án.
4. DP trên đồ thị có hướng mà cạnh ngược phá trạng thái — co trước, rồi
   DAG DP của Trung cấp áp dụng.

Chống-dấu-hiệu: DAG không cần lượt SCC; liên thông vô hướng là đất của
M5/Trung cấp. SCC dành cho CHU TRÌNH CÓ HƯỚNG có cấu trúc.
""",
    difficulty="advanced",
)

# ------------------------------------------------------------ practice R/W
# A1 R: iterative Kosaraju, print (#SCCs, largest size)
A1_R = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1), radj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        radj[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    vector<int> order; order.reserve(n);
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        vector<pair<int, bool>> st; st.push_back({s, false});
        while (!st.empty()) {
            auto [u, d] = st.back(); st.pop_back();
            if (d) { order.push_back(u); continue; }
            if (vis[u]) continue;
            vis[u] = 1;
            st.push_back({u, true});
            for (int v : adj[u]) if (!vis[v]) st.push_back({v, false});
        }
    }
    vector<int> comp(n + 1, 0);
    int c = 0;
    for (int i = n - 1; i >= 0; --i) {
        int s = order[i];
        if (comp[s]) continue;
        ++c;
        vector<int> st; st.push_back(s); comp[s] = c;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : radj[u]) if (!comp[v]) { comp[v] = c; st.push_back(v); }
        }
    }
    vector<int> sz(c + 1, 0);
    for (int v = 1; v <= n; ++v) sz[comp[v]]++;
    int big = 0;
    for (int i = 1; i <= c; ++i) big = max(big, sz[i]);
    out << c << " " << big << "{{NL}}";
""") + END

# A1 W: counts connected components of the UNDIRECTED version (ignores
# direction) — behavioral, fails whenever direction merges/splits differ.
A1_W = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);   // WRONG: treats the graph as undirected
    }
    vector<char> vis(n + 1, 0);
    int comps = 0, big = 0;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++comps;
        int cnt = 0;
        vector<int> st; st.push_back(s); vis[s] = 1;
        while (!st.empty()) {
            int u = st.back(); st.pop_back(); ++cnt;
            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }
        }
        big = max(big, cnt);
    }
    out << comps << " " << big << "{{NL}}";
""") + END

# A2 R: condensation edge count (distinct pairs)
A2_R = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1), radj(n + 1);
    vector<pair<int, int>> es; es.reserve(m);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); radj[v].push_back(u); es.push_back({u, v});
    }
    vector<char> vis(n + 1, 0);
    vector<int> order; order.reserve(n);
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        vector<pair<int, bool>> st; st.push_back({s, false});
        while (!st.empty()) {
            auto [u, d] = st.back(); st.pop_back();
            if (d) { order.push_back(u); continue; }
            if (vis[u]) continue;
            vis[u] = 1;
            st.push_back({u, true});
            for (int v : adj[u]) if (!vis[v]) st.push_back({v, false});
        }
    }
    vector<int> comp(n + 1, 0);
    int c = 0;
    for (int i = n - 1; i >= 0; --i) {
        int s = order[i];
        if (comp[s]) continue;
        ++c;
        vector<int> st; st.push_back(s); comp[s] = c;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : radj[u]) if (!comp[v]) { comp[v] = c; st.push_back(v); }
        }
    }
    set<pair<int, int>> ce;
    for (auto& [u, v] : es) if (comp[u] != comp[v]) ce.insert({comp[u], comp[v]});
    out << ce.size() << "{{NL}}";
""") + END

# A2 W: counts RAW edges crossing components (duplicates included) —
# fails whenever the graph has duplicate condensation edges.
A2_W = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1), radj(n + 1);
    vector<pair<int, int>> es; es.reserve(m);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); radj[v].push_back(u); es.push_back({u, v});
    }
    vector<char> vis(n + 1, 0);
    vector<int> order; order.reserve(n);
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        vector<pair<int, bool>> st; st.push_back({s, false});
        while (!st.empty()) {
            auto [u, d] = st.back(); st.pop_back();
            if (d) { order.push_back(u); continue; }
            if (vis[u]) continue;
            vis[u] = 1;
            st.push_back({u, true});
            for (int v : adj[u]) if (!vis[v]) st.push_back({v, false});
        }
    }
    vector<int> comp(n + 1, 0);
    int c = 0;
    for (int i = n - 1; i >= 0; --i) {
        int s = order[i];
        if (comp[s]) continue;
        ++c;
        vector<int> st; st.push_back(s); comp[s] = c;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : radj[u]) if (!comp[v]) { comp[v] = c; st.push_back(v); }
        }
    }
    long long cross = 0;
    for (auto& [u, v] : es) if (comp[u] != comp[v]) cross++;   // WRONG: no dedupe
    out << cross << "{{NL}}";
""") + END

# A3 R: comp id per node (labels renumbered so comp of node 1's SCC = 1,
# i.e. labels in first-encounter order over 1..n)
A3_R = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1), radj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); radj[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    vector<int> order; order.reserve(n);
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        vector<pair<int, bool>> st; st.push_back({s, false});
        while (!st.empty()) {
            auto [u, d] = st.back(); st.pop_back();
            if (d) { order.push_back(u); continue; }
            if (vis[u]) continue;
            vis[u] = 1;
            st.push_back({u, true});
            for (int v : adj[u]) if (!vis[v]) st.push_back({v, false});
        }
    }
    vector<int> comp(n + 1, 0);
    int c = 0;
    for (int i = n - 1; i >= 0; --i) {
        int s = order[i];
        if (comp[s]) continue;
        ++c;
        vector<int> st; st.push_back(s); comp[s] = c;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : radj[u]) if (!comp[v]) { comp[v] = c; st.push_back(v); }
        }
    }
    // renumber: first-seen order over 1..n
    vector<int> lab(n + 1, 0);
    int next = 0;
    vector<int> rel(n + 1, 0);
    for (int v = 1; v <= n; ++v) {
        if (!rel[comp[v]]) rel[comp[v]] = ++next;
        lab[v] = rel[comp[v]];
    }
    for (int v = 1; v <= n; ++v) {
        if (v > 1) out << ' ';
        out << lab[v];
    }
    out << "{{NL}}";
""") + END

# A3 W (near-miss): per-node BFS forward-reachability marking "same comp"
# by scanning ALL nodes per node — O(n·(n+m)): TIMEOUT on 2·10^5 load.
A3_W = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
    }
    // WRONG: for each node, BFS and assign same-group labels by mutual
    // reachability discovered per node — O(n·(n+m)) total.
    vector<int> lab(n + 1, 0);
    int next = 0;
    for (int s = 1; s <= n; ++s) {
        if (lab[s]) continue;
        ++next;
        // forward from s
        vector<char> fwd(n + 1, 0);
        vector<int> st; st.push_back(s); fwd[s] = 1;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u]) if (!fwd[v]) { fwd[v] = 1; st.push_back(v); }
        }
        for (int v = 1; v <= n; ++v) {
            if (lab[v] || !fwd[v]) continue;
            // check v reaches s?
            vector<char> bk(n + 1, 0);
            vector<int> st2; st2.push_back(v); bk[v] = 1;
            while (!st2.empty()) {
                int u = st2.back(); st2.pop_back();
                for (int w : adj[u]) if (!bk[w]) { bk[w] = 1; st2.push_back(w); }
            }
            if (bk[s]) { lab[v] = next; }
        }
        if (!lab[s]) lab[s] = next;
    }
    for (int v = 1; v <= n; ++v) {
        if (v > 1) out << ' ';
        out << lab[v];
    }
    out << "{{NL}}";
""") + END

# CP R: SCC count + condensation edges in one program
CP_M8_R = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1), radj(n + 1);
    vector<pair<int, int>> es; es.reserve(m);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); radj[v].push_back(u); es.push_back({u, v});
    }
    vector<char> vis(n + 1, 0);
    vector<int> order; order.reserve(n);
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        vector<pair<int, bool>> st; st.push_back({s, false});
        while (!st.empty()) {
            auto [u, d] = st.back(); st.pop_back();
            if (d) { order.push_back(u); continue; }
            if (vis[u]) continue;
            vis[u] = 1;
            st.push_back({u, true});
            for (int v : adj[u]) if (!vis[v]) st.push_back({v, false});
        }
    }
    vector<int> comp(n + 1, 0);
    int c = 0;
    for (int i = n - 1; i >= 0; --i) {
        int s = order[i];
        if (comp[s]) continue;
        ++c;
        vector<int> st; st.push_back(s); comp[s] = c;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : radj[u]) if (!comp[v]) { comp[v] = c; st.push_back(v); }
        }
    }
    set<pair<int, int>> ce;
    for (auto& [u, v] : es) if (comp[u] != comp[v]) ce.insert({comp[u], comp[v]});
    vector<int> sz(c + 1, 0);
    for (int v = 1; v <= n; ++v) sz[comp[v]]++;
    int big = 0;
    for (int i = 1; i <= c; ++i) big = max(big, sz[i]);
    out << c << " " << big << " " << ce.size() << "{{NL}}";
""") + END

# CP W: undirected-components + raw-cross — wrong on both axes.
CP_M8_W = CPP_STD + cpp("""
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<pair<int, int>> es; es.reserve(m);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);   // WRONG: undirected
        es.push_back({u, v});
    }
    vector<char> vis(n + 1, 0);
    vector<int> comp(n + 1, 0);
    int c = 0;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++c;
        vector<int> st; st.push_back(s); vis[s] = 1; comp[s] = c;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; comp[v] = c; st.push_back(v); }
        }
    }
    long long cross = 0;
    for (auto& [u, v] : es) if (comp[u] != comp[v]) cross++;
    vector<int> sz(c + 1, 0);
    for (int v = 1; v <= n; ++v) sz[comp[v]]++;
    int big = 0;
    for (int i = 1; i <= c; ++i) big = max(big, sz[i]);
    out << c << " " << big << " " << cross << "{{NL}}";
""") + END


# ----------------------------------------------------------------- tests
def _edges_input(n, edges):
    lines = [str(n), str(len(edges))]
    lines += ["%d %d" % (u, v) for (u, v) in edges]
    return T(*lines)


# hand graph: 3-cycle {1,2,3}, 2-cycle {4,5}, tail 6. Verified:
# comp [1,1,1,2,2,3], 3 SCCs, largest 3, cond edges 2.
_HAND_EDGES = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 4), (5, 6)]

A1_TESTS = [
    contest_test(
        "hand graph",
        _edges_input(6, _HAND_EDGES),
        T("3 3"),
        "SCCs {1,2,3} {4,5} {6}: 3 components, largest size 3."),
    contest_test(
        "DAG needs no merging",
        _edges_input(4, [(1, 2), (1, 3), (3, 2), (2, 4)]),
        T("4 1"),
        "A DAG has every node its own SCC: 4 components of size 1."),
    contest_test(
        "giant cycle, 200000 nodes",
        _edges_input(200000, _gen_bigcycle(200000)),
        T("1 200000"),
        "One directed cycle swallows everything: a single SCC of size n."),
    contest_test(
        "2-cycle chain, 200000 nodes",
        _edges_input(200000, _gen_pairs(200000)),
        T("100000 2"),
        "100000 two-cycles chained forward: 100000 SCCs, largest 2 — direction matters, undirected would give 1."),
]

A2_TESTS = [
    contest_test(
        "hand graph condensation",
        _edges_input(6, _HAND_EDGES),
        T("2"),
        "Cycles collapse; edges (C123 -> C45) and (C45 -> C6) remain: 2."),
    contest_test(
        "duplicate cross edges collapse",
        _edges_input(3, [(1, 2), (1, 2), (1, 2), (2, 3), (2, 3)]),
        T("2"),
        "Five raw edges, two distinct condensation edges — dedupe is the point."),
    contest_test(
        "2-cycle chain, condensation edges",
        _edges_input(200000, _gen_pairs(200000)),
        T("99999"),
        "99999 forward links survive the shrink: O(n + m) with a set."),
]

A3_TESTS = [
    contest_test(
        "hand labels",
        _edges_input(6, _HAND_EDGES),
        T("1 1 1 2 2 3"),
        "First-encounter relabeling: node 1's SCC gets 1, then {4,5} gets 2, singleton 6 gets 3."),
    contest_test(
        "DAG labels all distinct",
        _edges_input(4, [(1, 2), (1, 3), (3, 2), (2, 4)]),
        T("1 2 3 4"),
        "Four singletons; labels follow first-encounter order."),
    contest_test(
        "2-cycle chain labels",
        _edges_input(200000, _gen_pairs(200000)),
        T(" ".join(str((v + 1) // 2) for v in range(1, 200001))),
        "Pairs (1,2)->1, (3,4)->2, ... : 100000 labels over 200000 nodes — Kosaraju label order coincides with first-encounter order here."),
]

CP_TESTS = [
    contest_test(
        "hand graph triple",
        _edges_input(6, _HAND_EDGES),
        T("3 3 2"),
        "3 SCCs, largest 3, 2 condensation edges — all three numbers from one pass pair."),
    contest_test(
        "giant cycle triple",
        _edges_input(200000, _gen_bigcycle(200000)),
        T("1 200000 0"),
        "One SCC, size n, zero condensation edges."),
    contest_test(
        "2-cycle chain triple",
        _edges_input(200000, _gen_pairs(200000)),
        T("100000 2 99999"),
        "The load: 100000 SCCs, largest 2, 99999 condensation edges."),
]

# ----------------------------------------------------------------- emit
write_lesson(
    M, "hsga-m8-kosaraju",
    "Kosaraju's Two Passes",
    "One DFS on G records finish order; one DFS on the reverse graph in reverse finish order labels every SCC — proven by the finish-time ordering.",
    35,
    """
# Two passes, one theorem

Pass 1: DFS over G, push each node when its DFS finishes. Pass 2: DFS
over the REVERSE graph G^T, starting from unvisited nodes in decreasing
finish order; each pass-2 tree is exactly one SCC.

Why it is correct: the node u with the largest finish time lies in a
"source" SCC C of the condensation. Reversing the graph makes C a sink —
no edges leave C in G^T, so its pass-2 DFS cannot escape. Induction on
the condensation finishes the proof.

Implementation must be ITERATIVE on both passes; build G^T once.
""",
    "Kosaraju hai lượt",
    "Một DFS trên G ghi thứ tự kết thúc; một DFS trên đồ thị NGƯỢC theo thứ tự kết thúc ngược gán nhãn từng SCC.",
    """
# Hai lượt, một định lý

Lượt 1: DFS trên G, đẩy nút khi DFS kết thúc. Lượt 2: DFS trên G^T,
bắt đầu theo thứ tự kết thúc giảm dần; mỗi cây lượt 2 là đúng một SCC.

Vì sao đúng: nút có thời điểm kết thúc lớn nhất nằm ở SCC "nguồn" C.
Đảo chiều biến C thành bể — DFS lượt 2 không thoát được khỏi C. Quy nạp
trên phép co kết thúc chứng minh.

Cài đặt phải LẶP trên cả hai lượt; dựng G^T một lần.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m8-condensation",
    "Condensation: Every Digraph Is a DAG",
    "Shrink each SCC to one node and the result is acyclic — DP on the condensation inherits every Intermediate DAG technique.",
    35,
    """
# The condensation is a DAG

If the condensation had a cycle, its SCCs would merge into one — so it
is acyclic by construction. Consequences:

- Distinct condensation edges need a SET of (comp[u], comp[v]) pairs.
- "Can u reach v" now runs on a DAG: longest path, reachability bitsets,
  path counting — all inherit.
- Two-step shape: SCC for cycles, then DAG DP for order.

Classic bug: self-loops and duplicate edges vanish in the condensation.
""",
    "Phép co: mọi đồ thị thành DAG",
    "Co mỗi SCC thành một nút và kết quả không có chu trình — DP trên phép co kế thừa mọi kỹ thuật DAG của Trung cấp.",
    """
# Phép co là DAG

Nếu phép co có chu trình, các SCC đó đã gộp thành một — vậy nó không có
chu trình. Hệ quả:

- Cạnh co phân biệt cần SET các cặp (comp[u], comp[v]).
- "u với được v?" giờ chạy trên DAG: đường dài nhất, reachability
  bitset, đếm đường đi — tất cả kế thừa được.
- Dạng hai bước: SCC cho chu trình, rồi DAG DP cho thứ tự.

Lỗi kinh điển: self-loop và cạnh trùng biến mất trong phép co.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m8-recognize",
    "Recognizing SCC Problems",
    "Mutual reachability, propagating swaps, 'same group' sizes, and digraph DP that back edges break — the four signatures of SCC.",
    35,
    """
# The four signatures

1. "u reaches v AND v reaches u" — mutual reachability IS the SCC
   relation.
2. Bidirectional swaps that propagate: swap(i,j) and swap(j,k) allowed →
   one component {i, j, k}.
3. "Group" answers — SCC sizes.
4. DP on a digraph where back edges break the state — condense first.

Anti-signature: a DAG needs no SCC pass; undirected connectivity is not
SCC territory.
""",
    "Nhận diện bài SCC",
    "Tương hỗ với được, hoán đổi lan truyền, kích thước 'cùng nhóm', và DP mà cạnh ngược phá trạng thái — bốn dấu hiệu của SCC.",
    """
# Bốn dấu hiệu

1. "u với được v VÀ v với được u" — tính tương hỗ CHÍNH là quan hệ SCC.
2. Hoán đổi hai chiều lan truyền: được đổi i-j và j-k → thành phần
   {i, j, k}.
3. Đáp án "nhóm" — kích thước SCC.
4. DP trên đồ thị có hướng mà cạnh ngược phá trạng thái — co trước.

Chống-dấu-hiệu: DAG không cần SCC; liên thông vô hướng không phải đất
SCC.
""",
    difficulty="advanced",
)

write_checkpoint(
    M, "hsga-cp-m8",
    "Checkpoint — SCC Triple",
    "One 2·10^5-node digraph, three numbers: SCC count, largest component, distinct condensation edges. The undirected-components misread is the graded wrong answer.",
    40,
    """
**Checkpoint — SCC.** Dòng 1: n, m. Theo sau m cạnh có hướng u v.
In ba số: SỐ thành phần liên thông mạnh, KÍCH THƯỚC thành phần lớn nhất,
và SỐ CẠNH PHÂN BIỆT của phép co (comp khác nhau, đếm mỗi cặp một lần).

Kosaraju lặp O(n + m); phép co phải khử trùng lặp.
""",
    "Điểm kiểm tra — Bộ ba SCC",
    "Một đồ thị 2·10^5 đỉnh, ba số: số SCC, thành phần lớn nhất, số cạnh co phân biệt. Đọc nhầm thành vô hướng là đáp án sai bị chấm.",
    """
**Checkpoint — SCC.** Dòng 1: n, m; m cạnh có hướng. In: số SCC,
kích thước lớn nhất, số cạnh co phân biệt.
""",
    challenge(
        "hsga-cp-m8-scc",
        "SCC Count, Size, Condensation",
        """**Bài toán.** Line 1: n m. Then m directed edges u v (1-based).
Print three numbers on one line: the NUMBER of strongly connected
components, the SIZE of the largest component, and the number of
DISTINCT edges in the condensation (pairs (comp[u], comp[v]) with
comp[u] != comp[v], each counted once).

**Constraints:** 1 ≤ n, m ≤ 200 000.

Iterative Kosaraju in O(n + m); the condensation deduplicates.
""",
        CP_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Số SCC, kích thước, phép co",
        """**Bài toán.** Dòng 1: n m; m cạnh có hướng. In ba số: số SCC,
kích thước lớn nhất, số cạnh co phân biệt.""",
        [("đọc nhầm vô hướng", "Thêm cạnh ngược làm gộp sai thành phần."),
         ("quên khử trùng lặp", "Đếm cạnh thô thay vì cạnh co phân biệt."),
         ("n=200000", "Kosaraju lặp O(n + m); DFS đệ quy tràn stack.")],
    ),
    solution=CP_M8_R,
    wrong=CP_M8_W,
)

VI_P8 = {
    "hsga-p8-scc": vi_challenge(
        "Bộ ba SCC",
        """**Bài toán.** Ba bài: đếm SCC + thành phần lớn nhất; số cạnh co
phân biệt; nhãn thành phần theo thứ tự gặp đầu tiên.""",
        [("DAG vẫn là SCC", "DAG có n thành phần cỡ 1."),
         ("khử trùng lặp", "Cạnh co phải là SET của (comp[u], comp[v])."),
         ("n=200000", "Kosaraju lặp; quét mutual-reach từng cặp là O(n·m) — timeout.")],
    ),
}

write_practice(
    M, "hsga-p8-scc", "SCC Trio",
    "Count and size components, count distinct condensation edges, and label components — with an undirected misread, a dedupe miss, and an O(n·m) near-miss.",
    "Bộ ba SCC",
    "Đếm và đo thành phần, đếm cạnh co phân biệt, gán nhãn thành phần — với đọc nhầm vô hướng, thiếu khử trùng lặp, và near-miss O(n·m).",
    "hsga-m8-recognize",
    110,
    "advanced",
    [
        challenge("hsga-p8-scccount", "Count and Largest SCC",
            """**Bài toán.** Line 1: n m; then m directed edges u v. Print two
numbers: the number of strongly connected components and the size of the
largest one.

**Constraints:** 1 ≤ n, m ≤ 200 000.

Iterative Kosaraju, O(n + m). Treating the graph as undirected fails
exactly when direction matters.
""",
            A1_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p8-condense", "Condensation Edge Count",
            """**Bài toán.** Line 1: n m; then m directed edges u v. Print one
number: the number of DISTINCT edges in the condensation DAG — pairs
(comp[u], comp[v]) with comp[u] != comp[v], counted once each.

**Constraints:** 1 ≤ n, m ≤ 200 000.

Kosaraju + a set of pairs. Counting raw crossing edges fails on
duplicates.
""",
            A2_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p8-complabel", "Component Labels",
            """**Bài toán.** Line 1: n m; then m directed edges u v. Print n
labels: for every node in order 1..n, the index of its SCC, renumbered
1..k in first-encounter order over nodes 1..n.

**Constraints:** 1 ≤ n, m ≤ 200 000.

Kosaraju labels in O(n + m). Per-node mutual-reachability scanning is
O(n·m) — timeout.
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    VI_P8,
    solutions=[
        ("hsga-p8-scccount", A1_R, A1_W),
        ("hsga-p8-condense", A2_R, A2_W),
        ("hsga-p8-complabel", A3_R, A3_W),
    ],
)

print("module m8 complete")
