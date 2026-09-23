#!/usr/bin/env python3
"""HSG Mastery — Module 7: hsgm-graphsyn (Graph & Tree Synthesis).

Combining graph traversals with DP/ordering, choosing the right structural
tool (topo order, DSU, tree reroot), and the classic directed-vs-undirected
stumble.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgm import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test, recognition_drill,
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL


def letter(l):
    return CPP_STD + cpp('    out << "' + l + '";') + END


M = "hsgm-graphsyn"
write_module(
    M,
    "Graph and Tree Synthesis",
    "Fusing traversal order with DP: topological order as the DP schedule, DSU as reachability bookkeeping, and rerooting for when every node wants to be the root.",
    "Tổng hợp đồ thị và cây",
    "Ghép thứ tự duyệt với DP: thứ tự topo như lịch DP, DSU như sổ theo dõi khả năng tới, và reroot khi mọi đỉnh đều muốn làm gốc.",
    ["hsgm-m7-schedule", "hsgm-m7-reroot", "hsgm-cp-m7"],
    ["hsgm-p7-drills"],
)

write_lesson(
    M, "hsgm-m7-schedule",
    "The Order Is the Algorithm",
    "Many 'graph problems' are DP problems whose trick is finding a valid processing order.",
    13,
    """
# The Order Is the Algorithm

Once you see `best[v] = f(best of v's predecessors)`, the graph problem
becomes a DP problem — but only if you can process nodes in an order where
every predecessor comes first. That order **is** the algorithm:

- **DAG** → topological sort, then one linear sweep. O(V + E).
- **General graph, reachability/counting** → DSU merges components offline,
  or SCC contraction, then DP on the condensed graph.
- **Tree** → the traversal order (post-order for upward DP, pre-order for
  downward) plays the topo role.

## The misread that costs a medal

The classic stumble: treating an arbitrary graph as a DAG. If cycles
exist, "longest path" is not just hard — it is undefined (infinite) for
the reachability version, and NP-hard for the simple-path version.
Before running topo DP, ask: **is acyclicity actually given, or derived?**
Deriving it (e.g., events ordered by time, states decreasing by a measure)
is itself the key observation of many problems.

## Two-pointer on graphs?

When edge weights are 0/1, 0-1 BFS replaces Dijkstra; when all weights
are equal, plain BFS is optimal. Recognizing the *weakest* tool that
still works is the mastery skill — heavyweight tools invite heavyweight
bugs.
""",
    "Thứ tự chính là thuật toán",
    "Nhiều 'bài đồ thị' là bài DP mà mẹo của nó là tìm một thứ tự xử lý hợp lệ.",
    """
# Thứ tự chính là thuật toán

Khi bạn thấy `best[v] = f(best của các tiền nhiệm của v)`, bài đồ thị trở
thành bài DP — nhưng chỉ khi bạn xử lý các đỉnh theo thứ tự mà mọi tiền
nhiệm đến trước. Thứ tự đó **chính là** thuật toán:

- **DAG** → sort topo, rồi một lần quét tuyến tính. O(V + E).
- **Đồ thị tổng quát, khả năng tới/đếm** → DSU gộp thành phần offline,
  hoặc co SCC, rồi DP trên đồ thị co lại.
- **Cây** → thứ tự duyệt (post-order cho DP đi lên, pre-order cho đi
  xuống) đóng vai topo.

## Cú đọc nhầm đắt giá

Cú vấp kinh điển: coi đồ thị tùy ý là DAG. Nếu có chu trình, "đường đi
dài nhất" không chỉ khó — nó không xác định (vô cực) với phiên bản khả
năng tới, và NP-khó với phiên bản đường đơn. Trước khi chạy topo DP, hãy
hỏi: **tính không có chu trình được cho, hay được suy ra?** Sự suy ra đó
(ví dụ sự kiện có thứ tự thời gian, trạng thái giảm theo một đại lượng)
chính là nhận xét then chốt của nhiều bài.

## Two-pointer trên đồ thị?

Khi trọng số chỉ 0/1, 0-1 BFS thay thế Dijkstra; khi mọi trọng số bằng
nhau, BFS thuần là tối ưu. Nhận diện *công cụ yếu nhất* vẫn còn đủ dùng
là kỹ năng của bậc thầy — công cụ hạng nặng mời gọi bug hạng nặng.
""",
)

write_lesson(
    M, "hsgm-m7-reroot",
    "Changing the Root",
    "When every node must be queried as the root, compute once and reroot with prefix/suffix contributions — don't rerun the DP n times.",
    14,
    """
# Changing the Root

Task shape: "for every vertex v, compute the answer where v is the
root/endpoint/start." Rerunning an O(n) DP from each vertex is O(n²) —
dead at n = 200000.

## The reroot pattern

1. **Up-pass (post-order):** compute for each subtree the contribution it
   would give its parent (e.g., subtree size, best downward path, sum of
   depths within the subtree).
2. **Down-pass (pre-order):** carry the answer for the root down the
   tree; when moving the root from u to child v, update with an
   **exchange formula**: subtract v's contribution from u's aggregate,
   add u's own contribution to v's. O(1) per edge.

## Why it matters beyond trees

The same "compute one global DP, then walk it outward" pattern appears
in DAG rerooting, in offline queries sorted by something, and in
contribution counting ("each element's contribution to every answer").
The general skill: **count contributions, not configurations** — for each
element, ask where it participates, instead of enumerating every final
answer.

## The correctness check

Reroot bugs live in the exchange formula. Test on a path of 3 nodes and a
star of 4 by hand before anything else; the two shapes exercise every
term of the formula (leaf, middle, center, multiple children).
""",
    "Đổi gốc",
    "Khi mọi đỉnh đều phải được hỏi như gốc, tính một lần và reroot với đóng góp tiền tố/hậu tố — đừng chạy lại DP n lần.",
    """
# Đổi gốc

Dạng bài: "với mọi đỉnh v, tính đáp án khi v là gốc/đích/xuất phát."
Chạy lại DP O(n) từ mỗi đỉnh là O(n²) — chết ở n = 200000.

## Mẫu reroot

1. **Lượt lên (post-order):** tính cho mỗi cây con phần đóng góp nó sẽ
   trao cho cha (kích thước cây con, đường đi xuống tốt nhất, tổng độ sâu
   trong cây con).
2. **Lượt xuống (pre-order):** mang đáp án của gốc đi khắp cây; khi dời
   gốc từ u sang con v, cập nhật bằng **công thức hoán đổi**: trừ đóng góp
   của v khỏi tổng của u, cộng đóng góp của u vào v. O(1) mỗi cạnh.

## Tại sao quan trọng ngoài cây

Mẫu "tính một DP toàn cục rồi đi lan nó" xuất hiện trong reroot trên DAG,
trong truy vấn offline đã sort, và trong đếm đóng góp ("đóng góp của mỗi
phần tử vào mọi đáp án"). Kỹ năng tổng quát: **đếm đóng góp, không đếm cấu
hình** — với mỗi phần tử, hỏi nó tham gia ở đâu, thay vì liệt kê mọi đáp
án cuối.

## Kiểm tra tính đúng

Bug reroot sống trong công thức hoán đổi. Thử tay trên đường 3 đỉnh và
ngôi sao 4 đỉnh trước bất cứ điều gì khác; hai hình đó luyện mọi số hạng
của công thức (lá, giữa, tâm, nhiều con).
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p7-d1", "The Cycle in Disguise",
    "States are (position, fuel remaining); moves consume fuel; refueling stations reset it. You must count distinct states reachable from the start. What graph do you build?",
    [
        "A DAG — fuel always decreases along moves",
        "A general directed graph; fuel resets at stations create cycles, so SCC contraction or BFS over states is required",
        "A tree of states — every state has a unique parent",
        "No graph; sort the stations and binary search",
    ],
    "B",
    "Refueling breaks monotonicity (fuel can increase), so the state graph has cycles: topo DP is illegal; BFS/SCC over the (position, fuel) product is the honest structure.",
    vi_title="Chu trình trá hình",
    vi_scenario="Trạng thái là (vị trí, xăng còn lại); nước đi tốn xăng; trạm tiếp xăng làm đầy lại. Phải đếm các trạng thái khác nhau tới được từ xuất phát. Đồ thị nào cần dựng?",
    vi_options=[
        "Một DAG — xăng luôn giảm theo nước đi",
        "Đồ thị có hướng tổng quát; việc tiếp xăng tạo chu trình, cần co SCC hoặc BFS trên các trạng thái",
        "Một cây các trạng thái — mọi trạng thái có cha duy nhất",
        "Không cần đồ thị; sort các trạm rồi chặt nhị phân",
    ],
    vi_hint="Tiếp xăng phá tính đơn điệu (xăng có thể tăng), nên đồ thị trạng thái có chu trình: topo DP bất hợp lệ; BFS/SCC trên tích (vị trí, xăng) là cấu trúc trung thực.",
)

D2, D2VI = recognition_drill(
    "hsgm-p7-d2", "Every Node Wants the Crown",
    "Tree, n ≤ 200000: for every vertex, the sum of distances to all others. What is the intended technique?",
    [
        "Run BFS from every vertex — O(n²) but constants are small",
        "One post-order DP for subtree contributions, then one pre-order reroot pass with an O(1) exchange per edge",
        "Floyd–Warshall on the tree",
        "Binary lifting to LCA, then sum pairwise distances",
    ],
    "B",
    "The classic reroot: two linear passes with the exchange formula. O(n²) dies at 200000; Floyd is nonsense on trees; pairwise LCA sums are O(n²).",
    vi_title="Mọi đỉnh đều muốn ngôi",
    vi_scenario="Cây, n ≤ 200000: với mọi đỉnh, tổng khoảng cách tới mọi đỉnh khác. Kỹ thuật chủ đích là gì?",
    vi_options=[
        "Chạy BFS từ mọi đỉnh — O(n²) nhưng hằng số nhỏ",
        "Một lượt post-order cho đóng góp cây con, rồi một lượt pre-order reroot với hoán đổi O(1) mỗi cạnh",
        "Floyd–Warshall trên cây",
        "Binary lifting tới LCA rồi cộng khoảng cách từng cặp",
    ],
    vi_hint="Reroot kinh điển: hai lượt tuyến tính với công thức hoán đổi. O(n²) chết ở 200000; Floyd vô nghĩa trên cây; tổng từng cặp qua LCA là O(n²).",
)

D3, D3VI = recognition_drill(
    "hsgm-p7-d3", "The Weakest Sufficient Tool",
    "A weighted graph where every edge weight is 0 or 1, n = 200000 edges = 400000: shortest path from s to every node. Which tool?",
    [
        "Dijkstra with a priority queue",
        "0-1 BFS with a deque — O(V + E), no heap",
        "Bellman–Ford, it handles everything",
        "DFS with backtracking on ties",
    ],
    "B",
    "0-1 BFS is the weakest sufficient tool here: same complexity as BFS, no log factor, no heap bugs. Dijkstra is correct but overkill; Bellman–Ford is needlessly slow.",
    vi_title="Công cụ yếu nhất vừa đủ",
    vi_scenario="Đồ thị có trọng số mà mọi cạnh là 0 hoặc 1, n = 200000, cạnh = 400000: đường đi ngắn nhất từ s tới mọi đỉnh. Công cụ nào?",
    vi_options=[
        "Dijkstra với hàng đợi ưu tiên",
        "0-1 BFS với deque — O(V + E), không cần heap",
        "Bellman–Ford, nó xử lý mọi thứ",
        "DFS với backtracking khi hòa",
    ],
    vi_hint="0-1 BFS là công cụ yếu nhất vừa đủ: cùng độ phức tạp với BFS, không thừa số log, không bug heap. Dijkstra đúng nhưng thừa; Bellman–Ford chậm không cần thiết.",
)

write_practice(
    M, "hsgm-p7-drills", "Graph Synthesis Drills",
    "Three drills: cycle detection via state design, rerooting, and weakest-sufficient-tool selection.",
    "Drill tổng hợp đồ thị",
    "Ba drill: phát hiện chu trình qua thiết kế trạng thái, reroot, và chọn công cụ yếu nhất vừa đủ.",
    "hsgm-m7-reroot", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p7-d1": D1VI, "hsgm-p7-d2": D2VI, "hsgm-p7-d3": D3VI},
    solutions=[
        ("hsgm-p7-d1", letter("B"), letter("A")),
        ("hsgm-p7-d2", letter("B"), letter("A")),
        ("hsgm-p7-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: longest path in a DAG (topo DP) at scale — n = 200000, m = 400000.
# W: computes longest path on the UNDIRECTED version (adds the reverse edge) —
# the directed/undirected stumble, behaviorally wrong on asymmetric graphs.
import random as _rnd

_rnd.seed(20260921)
_n7 = 200000
_m7 = 400000
# layered DAG: edges strictly increasing layer => provably acyclic
_layers = 1000
_per = _n7 // _layers
_edges = []
for v in range(1, _n7 + 1):
    lay = (v - 1) // _per
    for _ in range(2):
        nxt_layer = lay + 1 + _rnd.randrange(0, max(1, _layers - lay - 1))
        if nxt_layer >= _layers:
            continue
        w = nxt_layer * _per + _rnd.randrange(1, _per + 1)
        if w <= _n7 and w != v:
            _edges.append((v, w))
_m7 = len(_edges)

# Ground truth via topo DP (Kahn)
from collections import deque as _dq7
_adj = [[] for _ in range(_n7 + 1)]
_indeg = [0] * (_n7 + 1)
for u, v in _edges:
    _adj[u].append(v)
    _indeg[v] += 1
_dp = [0] * (_n7 + 1)
_q = _dq7(i for i in range(1, _n7 + 1) if _indeg[i] == 0)
_seen = 0
while _q:
    u = _q.popleft()
    _seen += 1
    for v in _adj[u]:
        _dp[v] = max(_dp[v], _dp[u] + 1)
        _indeg[v] -= 1
        if _indeg[v] == 0:
            _q.append(v)
assert _seen == _n7  # acyclic by construction
_cp7 = max(_dp)

CP_M7_IN = T(f"{_n7} {_m7}", *[f"{u} {v}" for (u, v) in _edges])
CP_M7_WANT = T(str(_cp7))

CP7C = challenge(
    "hsgm-cp-m7-longest",
    "Checkpoint: The Longest Chain",
    """**Task.** A directed graph with n nodes and m edges (given as pairs u
v, meaning an edge u → v). The graph is guaranteed acyclic. Print the
number of edges on the longest directed path (a path visits distinct
nodes following edge directions).

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ m ≤ 400000. Recursion depth can hit
200000 — an explicit order (Kahn) or iterative DFS is required.

**Budget check:** one topological sort plus one DP sweep: O(n + m).
""",
    [
        contest_test("chain", T("4 3", "1 2", "2 3", "3 4"), T("3"),
            "1→2→3→4: three edges."),
        contest_test("branch", T("4 3", "1 2", "1 3", "3 4"), T("2"),
            "1→3→4 beats 1→2: two edges."),
    ],
    level="combination",
    difficulty="advanced",
)
CP7C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("chain", T("4 3", "1 2", "2 3", "3 4"), T("3"),
            "1→2→3→4: three edges."),
        contest_test("branch", T("4 3", "1 2", "1 3", "3 4"), T("2"),
            "1→3→4 beats 1→2: two edges."),
        contest_test("disconnected", T("5 2", "2 1", "4 5"), T("1"),
            "Two isolated edges: each path has one edge → 1."),
        contest_test("full scale", CP_M7_IN, CP_M7_WANT,
            "n = 200000, m ≈ 400000 layered DAG. Ground truth via Kahn topo DP in Python."),
    )
]

CP7VI = vi_challenge(
    "Điểm kiểm tra: chuỗi dài nhất",
    """**Bài toán.** Đồ thị có hướng n đỉnh, m cạnh (cho như cặp u v, nghĩa là
cạnh u → v). Đồ thị đảm bảo không có chu trình. In số cạnh trên đường đi
có hướng dài nhất (đường đi qua các đỉnh khác nhau, đi theo hướng cạnh).

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ m ≤ 400000. Độ sâu đệ quy có thể tới
200000 — cần thứ tự tường minh (Kahn) hoặc DFS lặp.

**Kiểm tra ngân sách:** một sort topo cộng một lần quét DP: O(n + m).
""",
    [("chuỗi", "1→2→3→4: ba cạnh."),
     ("phân nhánh", "1→3→4 thắng 1→2: hai cạnh."),
     ("rời mảnh", "Hai cạnh cô lập: mỗi đường có một cạnh → 1."),
     ("đúng giới hạn", "n = 200000, m ≈ 400000 DAG phân tầng. Đáp án chuẩn bằng Kahn topo DP trong Python.")],
)

CP_M7_R = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++indeg[v];
    }
    vector<int> dp(n + 1, 0);
    deque<int> q;
    for (int i = 1; i <= n; ++i) if (!indeg[i]) q.push_back(i);
    while (!q.empty()) {
        int u = q.front(); q.pop_front();
        for (int v : adj[u]) {
            dp[v] = max(dp[v], dp[u] + 1);
            if (--indeg[v] == 0) q.push_back(v);
        }
    }
    out << *max_element(dp.begin(), dp.end()) << "{{NL}}";
""") + END

CP_M7_W = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        // WRONG: silently adds the reverse edge too — treats the graph as
        // undirected. Longest path in the undirected version can visit both
        // directions of every edge, inflating the count on any graph whose
        // longest directed chain is not also a chain both ways.
        adj[u].push_back(v);
        adj[v].push_back(u);
        ++indeg[v];
    }
    vector<int> dp(n + 1, 0);
    deque<int> q;
    for (int i = 1; i <= n; ++i) if (!indeg[i]) q.push_back(i);
    while (!q.empty()) {
        int u = q.front(); q.pop_front();
        for (int v : adj[u]) {
            dp[v] = max(dp[v], dp[u] + 1);
            if (--indeg[v] == 0) q.push_back(v);
        }
    }
    out << *max_element(dp.begin(), dp.end()) << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m7", "Checkpoint — The Order Is the Algorithm",
    "Longest path in a DAG at full scale: Kahn order + one sweep. The W adds the reverse edge — the directed/undirected stumble — and reports inflated paths.",
    25,
    """
**Checkpoint — The Order Is the Algorithm.** Longest path needs every
predecessor processed first: Kahn's topological order + a linear DP
sweep, O(n + m), no recursion (depth would hit 200000). The W is the
directed/undirected stumble: it quietly adds the reverse edge, turning a
directional structure into a symmetric one — plausible-looking code,
wrong on any asymmetric graph, and it even risks double-counting in the
indegree logic.
""",
    "Điểm kiểm tra — Thứ tự chính là thuật toán",
    "Đường đi dài nhất trong DAG ở đúng giới hạn: thứ tự Kahn + một lần quét. W thêm cạnh ngược — cú vấp có-hướng/vô-hướng — và báo đường bị thổi phồng.",
    """
**Điểm kiểm tra — Thứ tự chính là thuật toán.** Đường đi dài nhất cần mọi
tiền nhiệm xử lý trước: thứ tự topo Kahn + một lần quét DP tuyến tính,
O(n + m), không đệ quy (độ sâu sẽ chạm 200000). W là cú vấp
có-hướng/vô-hướng: nó lặng lẽ thêm cạnh ngược, biến cấu trúc có hướng
thành đối xứng — code trông hợp lý, sai trên mọi đồ thị không đối xứng,
và còn nguy cơ đếm đôi trong logic indegree.
""",
    CP7C,
    CP7VI,
    CP_M7_R,
    CP_M7_W,
)

print("module m7 complete")
