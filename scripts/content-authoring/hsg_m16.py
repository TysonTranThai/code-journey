#!/usr/bin/env python3
"""HSG — Module 16: hsg-graph (lý thuyết đồ thị).

Adjacency-list representation, BFS for unweighted shortest paths, DFS
recursion + iterative stack form, connected components, grid-as-graph
(flood fill). Conventions: T() for test I/O, cpp() for bodies.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
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
#include <queue>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsg-graph"
write_module(
    M,
    "Graph Theory Fundamentals",
    "Store a graph as adjacency lists, then walk it: BFS for shortest unweighted paths, DFS for structure, flood fill for grids.",
    "Lý thuyết đồ thị cơ bản",
    "Lưu đồ thị bằng danh sách kề, rồi đi qua nó: BFS cho đường đi ngắn nhất không trọng số, DFS cho cấu trúc, flood fill cho lưới.",
    ["hsg-m16-idea", "hsg-m16-traversal", "hsg-cp-m16"],
    ["hsg-p16-graph"],
)

write_lesson(
    M,
    "hsg-m16-idea",
    "Representing Graphs",
    "Adjacency lists win in contests: O(V+E) memory, cache-friendly iteration, no V^2 tax.",
    16,
    """## The three representations

- **Adjacency matrix** `g[u][v]`: O(V^2) memory — fine for `V <= ~4000`,
  wasteful beyond. Check "is u adjacent to v?" in O(1).
- **Adjacency list** `vector<int> adj[V]`: O(V + E) memory — the
  contest default. Iterate neighbors of u in deg(u).
- **Edge list**: just the edges — useful for algorithms that process
  edges (later: DSU, MST).

## Reading the standard input format

```
n m            (vertices 1..n, m edges)
u v            (m lines: an undirected edge between u and v)
```

```cpp
int n, m; in >> n >> m;
vector<vector<int>> adj(n + 1);
for (int i = 0; i < m; ++i) {
    int u, v; in >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);   // drop this line for DIRECTED graphs
}
```

The one-line-difference directed/undirected switch is a classic
misread: build the wrong one and your component counts are silently
wrong. Note vertices are **1-based** in nearly every Vietnamese
problem — sized n+1 and ignore index 0.

### Trees are graphs

A tree with n vertices has exactly n-1 edges and is connected. Every
tree algorithm is a graph traversal with no visited-check surprises —
but only if you actually build the undirected list (parent can appear
as a "child").
""",
    "Biểu diễn đồ thị",
    "Danh sách kẻ thắng trong thi đấu: bộ nhớ O(V+E), duyệt thân thiện bộ nhớ đệm, không trả thuế V^2.",
    """## Ba cách biểu diễn

- **Ma trận kề** `g[u][v]`: bộ nhớ O(V^2) — ổn với `V <= ~4000`, lãng
  phí lớn hơn. Hỏi "u kề v?" trong O(1).
- **Danh sách kề** `vector<int> adj[V]`: bộ nhớ O(V + E) — mặc định
  của thi đấu. Duyệt láng giềng của u trong deg(u).
- **Danh sách cạnh**: chỉ các cạnh — hữu ích cho thuật toán xử lý
  cạnh (sau này: DSU, MST).

## Đọc định dạng nhập chuẩn

```
n m            (đỉnh 1..n, m cạnh)
u v            (m dòng: một cạnh vô hướng giữa u và v)
```

```cpp
int n, m; in >> n >> m;
vector<vector<int>> adj(n + 1);
for (int i = 0; i < m; ++i) {
    int u, v; in >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);   // bỏ dòng này với đồ thị CÓ HƯỚNG
}
```

Khác biệt một dòng có hướng/vô hướng là lỗi đọc đề kinh điển: dựng
sai và số thành phần liên thông sai âm thầm. Chú ý đỉnh đánh số
**từ 1** trong gần như mọi đề Việt Nam — cấp phát n+1 và bỏ qua chỉ
số 0.

### Cây cũng là đồ thị

Cây n đỉnh có đúng n-1 cạnh và liên thông. Mọi thuật toán trên cây là
một phép duyệt đồ thị không có bất ngờ về visited — nhưng chỉ khi bạn
thực sự dựng danh sách vô hướng (cha cũng xuất hiện như "con").
""",
)

write_lesson(
    M,
    "hsg-m16-traversal",
    "BFS, DFS, and Components",
    "BFS = shortest unweighted paths via a queue; DFS = deep exploration via recursion or a stack; both mark visited ON enqueue/push.",
    17,
    """## BFS — level by level

```cpp
vector<int> dist(n + 1, -1);
queue<int> q;
dist[s] = 0; q.push(s);          // mark AT PUSH, not at pop
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u])
        if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
}
```

dist[v] is the exact shortest edge-count from s. The classic bug:
marking visited at **pop** — the same vertex enters the queue many
times, memory and time blow up on dense graphs.

## DFS — the same graph, different order

Recursive form is shortest to write; depth can hit V, so V = 10^5
needs the explicit-stack form (or a bigger stack — not portable):

```cpp
vector<int> st;
vis[s] = true; st.push_back(s);   // mark AT PUSH here too
while (!st.empty()) {
    int u = st.back(); st.pop_back();
    for (int v : adj[u])
        if (!vis[v]) { vis[v] = true; st.push_back(v); }
}
```

## Connected components

Loop all vertices; each unvisited vertex starts one traversal, and
that traversal marks exactly its component:

```cpp
int comps = 0;
for (int v = 1; v <= n; ++v)
    if (!vis[v]) { ++comps; /* traverse from v */ }
```

## Grids are graphs

Each open cell is a vertex; neighbors are the up/down/left/right open
cells. Flood fill = BFS/DFS on that implicit graph — the same visited
discipline, coordinates instead of indices.
""",
    "BFS, DFS, và thành phần liên thông",
    "BFS = đường ngắn nhất không trọng số bằng hàng đợi; DFS = khám phá sâu bằng đệ quy hoặc ngăn xếp; cả hai đều đánh dấu visited NGAY khi enqueue/push.",
    """## BFS — từng lớp một

```cpp
vector<int> dist(n + 1, -1);
queue<int> q;
dist[s] = 0; q.push(s);          // đánh dấu KHI PUSH, không phải khi pop
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u])
        if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
}
```

dist[v] là đúng số cạnh ít nhất từ s. Bug kinh điển: đánh dấu visited
khi **pop** — cùng một đỉnh chen vào hàng đợi nhiều lần, bộ nhớ và
thời gian nổ tung trên đồ thị dày.

## DFS — cùng đồ thị, thứ tự khác

Dạng đệ quy ngắn nhất để viết; độ sâu có thể chạm V, nên V = 10^5 cần
dạng ngăn xếp tường minh (hoặc tăng ngăn xếp — không khả chuyển):

```cpp
vector<int> st;
vis[s] = true; st.push_back(s);   // đánh dấu KHI PUSH ở đây nữa
while (!st.empty()) {
    int u = st.back(); st.pop_back();
    for (int v : adj[u])
        if (!vis[v]) { vis[v] = true; st.push_back(v); }
}
```

## Thành phần liên thông

Duyệt tất cả đỉnh; mỗi đỉnh chưa thăm mở đầu một lần duyệt, và lần
duyệt đó đánh dấu đúng thành phần của nó:

```cpp
int comps = 0;
for (int v = 1; v <= n; ++v)
    if (!vis[v]) { ++comps; /* duyệt từ v */ }
```

## Lưới chính là đồ thị

Mỗi ô trống là một đỉnh; láng giềng là các ô mở trên/dưới/trái/phải.
Flood fill = BFS/DFS trên đồ thị ẩn đó — cùng kỷ luật visited, dùng
tọa độ thay vì chỉ số.
""",
)

A1 = challenge(
    "hsg-p16-components",
    "Counting Components",
    T(
        "**Description:** Count the connected components of an undirected graph.",
        "",
        "**Input:** Line 1: n m (1 <= n <= 100000, 0 <= m <= 200000). Next m lines:",
        "u v (1 <= u, v <= n).",
        "**Output:** One integer — the number of components.",
        "",
        "**Example:** `4 2` / `1 2` / `3 4` -> `2`.",
    ),
    [
        contest_test("sample", T("4 2", "1 2", "3 4"), T("2"), "Two pairs, no bridge between them."),
        contest_test("no edges", T("5 0"), T("5"), "Every vertex is alone."),
        contest_test("single", T("1 0"), T("1"), "One vertex, one component."),
        contest_test("all connected", T("4 3", "1 2", "2 3", "3 4"), T("1"), "A path is connected."),
        contest_test("star + tail", T("6 4", "1 2", "1 3", "1 4", "5 6"), T("2"),
                     "Star at 1 plus the 5-6 pair."),
    ],
    level="guided",
    difficulty="intermediate",
)

A2 = challenge(
    "hsg-p16-bfs",
    "Shortest Steps",
    T(
        "**Description:** Given an undirected unweighted graph and a start vertex s, print",
        "the shortest distance (edge count) from s to every vertex, -1 if unreachable.",
        "",
        "**Input:** Line 1: n m s (1 <= n <= 100000, 0 <= m <= 200000, 1 <= s <= n).",
        "Next m lines: u v.",
        "**Output:** One line: n integers — dist(s, 1) ... dist(s, n), space-separated.",
        "",
        "**Example:** `4 3 1` / `1 2` / `2 3` / `1 4` -> `0 1 2 1`.",
    ),
    [
        contest_test("sample", T("4 3 1", "1 2", "2 3", "1 4"), T("0 1 2 1"),
                     "Straightforward BFS levels."),
        contest_test("isolated", T("3 1 1", "1 2"), T("0 1 -1"),
                     "Vertex 3 unreachable -> -1."),
        contest_test("start alone", T("2 0 2"), T("-1 0"), "No edges: only s reaches itself."),
        contest_test("shortcut wins", T("5 5 1", "1 2", "2 3", "3 4", "4 5", "1 5"),
                     T("0 1 2 2 1"),
                     "dist(4)=2 through 5 — undirected edges work both ways; directed builds print 3."),
        contest_test("max n", T("100000 2 1", "1 2", "2 3"),
                     T("0 1 2 " + " ".join(["-1"] * 99997)),
                     "Sparse far graph; output formatting discipline at scale."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p16-flood",
    "Flood Fill Rooms",
    T(
        "**Description:** A grid of '.' (open) and '#' (wall) cells. Two open cells are in",
        "the same room if connected horizontally or vertically. Count the rooms.",
        "",
        "**Input:** Line 1: n m (1 <= n, m <= 1000). Next n lines: m characters each.",
        "**Output:** One integer — the number of rooms.",
        "",
        "**Example:** `3 4` / `.#..` / `.#.#` / `.#..` -> `2`.",
    ),
    [
        contest_test("sample", T("3 4", ".#..", ".#.#", ".#.."), T("2"),
                     "Left column wall splits two regions."),
        contest_test("all walls", T("2 2", "##", "##"), T("0"), "No open cells."),
        contest_test("all open", T("2 2", "..", ".."), T("1"), "One big room."),
        contest_test("diagonal not connected", T("2 2", ".#", "#."), T("2"),
                     "Touching only diagonally does NOT connect."),
        contest_test("requires left", T("2 2", "#.", ".."), T("1"),
                     "The room bends left — up/left moves are mandatory, right/down-only floods split it."),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p16-grid-dist",
    "Maze Escape",
    T(
        "**Description:** Shortest walk length from S to E on a grid moving through '.' cells",
        "(up/down/left/right), or -1 if E is unreachable. S and E count as walkable.",
        "",
        "**Input:** Line 1: n m (1 <= n, m <= 1000). Next n lines: m characters each",
        "('.' open, '#' wall, exactly one 'S', exactly one 'E').",
        "**Output:** One integer — the minimum number of moves, or -1.",
        "",
        "**Example:** `2 3` / `S..` / `.#E` -> `3` (right, right, down).",
    ),
    [
        contest_test("sample", T("2 3", "S..", ".#E"), T("3"), "Around the wall."),
        contest_test("adjacent", T("2 2", "S.", ".E"), T("2"), "Down then right."),
        contest_test("blocked", T("2 3", "S#.", ".#E"), T("-1"), "The wall column is complete."),
        contest_test("long detour", T("3 3", "S#E", "...", "..."), T("4"),
                     "Down, right, right, up: four moves around the wall."),
        contest_test("adjacent columns", T("1 2", "SE"), T("1"),
                     "One move."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p16-treecheck",
    "Is It a Tree?",
    T(
        "**Description:** Decide whether an undirected graph with n vertices and m edges is",
        "a tree: connected AND exactly n-1 edges (no cycles).",
        "",
        "**Input:** Line 1: n m (1 <= n <= 100000, 0 <= m <= 200000). Next m lines: u v.",
        "**Output:** Print `YES` if the graph is a tree, otherwise `NO`.",
        "",
        "**Example:** `3 2` / `1 2` / `2 3` -> `YES`.",
    ),
    [
        contest_test("sample path", T("3 2", "1 2", "2 3"), T("YES"), "Path: connected, n-1 edges."),
        contest_test("cycle", T("3 3", "1 2", "2 3", "1 3"), T("NO"), "Too many edges."),
        contest_test("disconnected", T("4 2", "1 2", "3 4"), T("NO"),
                     "Two components — the edge count matches but connectivity fails."),
        contest_test("self loop", T("2 2", "1 1", "1 2"), T("NO"), "A self-loop is a cycle."),
        contest_test("double edge", T("4 3", "1 2", "1 2", "3 4"), T("NO"),
                     "m == n-1 but disconnected — the edge-count check alone is not enough."),
        contest_test("single vertex", T("1 0"), T("YES"), "Trivially a tree."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p16-components": vi_challenge(
        "Đếm thành phần liên thông",
        T(
            "**Đề bài:** Đếm số thành phần liên thông của một đồ thị vô hướng.",
            "",
            "**Dữ liệu vào:** Dòng 1: n m (1 <= n <= 100000, 0 <= m <= 200000). m dòng tiếp:",
            "u v (1 <= u, v <= n).",
            "**Dữ liệu ra:** Một số nguyên — số thành phần.",
            "",
            "**Ví dụ:** `4 2` / `1 2` / `3 4` -> `2`.",
        ),
        [
            ("sample", "Hai cặp, không cầu nối."),
            ("no edges", "Mỗi đỉnh tự tách một."),
            ("single", "Một đỉnh, một thành phần."),
            ("all connected", "Đường đi là liên thông."),
            ("star + tail", "Ngôi sao tại 1 cộng cặp 5-6."),
        ],
    ),
    "hsg-p16-bfs": vi_challenge(
        "Số bước ngắn nhất",
        T(
            "**Đề bài:** Cho đồ thị vô hướng không trọng số và đỉnh xuất phát s, in khoảng cách",
            "ngắn nhất (số cạnh) từ s tới mọi đỉnh, -1 nếu không tới được.",
            "",
            "**Dữ liệu vào:** Dòng 1: n m s (1 <= n <= 100000, 0 <= m <= 200000, 1 <= s <= n).",
            "m dòng tiếp: u v.",
            "**Dữ liệu ra:** Một dòng: n số nguyên — dist(s, 1) ... dist(s, n), cách nhau dấu cách.",
            "",
            "**Ví dụ:** `4 3 1` / `1 2` / `2 3` / `1 4` -> `0 1 2 1`.",
        ),
        [
            ("sample", "Các lớp BFS trực quan."),
            ("isolated", "Đỉnh 3 không tới được -> -1."),
            ("start alone", "Không cạnh: chỉ s với chính nó."),
            ("shortcut wins", "dist(4)=2 đi qua 5 — cạnh vô hướng đi hai chiều; dựng có hướng sẽ in 3."),
            ("max n", "Đồ thị thưa xa; kỷ luật định dạng đầu ra ở quy mô lớn."),
        ],
    ),
    "hsg-p16-flood": vi_challenge(
        "Flood fill đếm phòng",
        T(
            "**Đề bài:** Lưới các ô '.' (trống) và '#' (tường). Hai ô trống cùng phòng nếu",
            "liên thông theo chiều ngang hoặc dọc. Đếm số phòng.",
            "",
            "**Dữ liệu vào:** Dòng 1: n m (1 <= n, m <= 1000). n dòng tiếp: mỗi dòng m ký tự.",
            "**Dữ liệu ra:** Một số nguyên — số phòng.",
            "",
            "**Ví dụ:** `3 4` / `.#..` / `.#.#` / `.#..` -> `2`.",
        ),
        [
            ("sample", "Cột tường giữa tách hai miền."),
            ("all walls", "Không ô trống."),
            ("all open", "Một phòng lớn."),
            ("diagonal not connected", "Chạm chéo KHÔNG nối."),
            ("requires left", "Phòng rẽ sang trái — bắt buộc đi lên/trái, flood chỉ phải/xuống sẽ tách nó."),
        ],
    ),
    "hsg-p16-grid-dist": vi_challenge(
        "Thoát mê cung",
        T(
            "**Đề bài:** Độ dài bước đi ngắn nhất từ S tới E trên lưới, đi qua các ô '.'",
            "(lên/xuống/trái/phải), hoặc -1 nếu không tới E. S và E được coi là đi được.",
            "",
            "**Dữ liệu vào:** Dòng 1: n m (1 <= n, m <= 1000). n dòng tiếp: mỗi dòng m ký tự",
            "('.' trống, '#' tường, đúng một 'S', đúng một 'E').",
            "**Dữ liệu ra:** Một số nguyên — số bước ít nhất, hoặc -1.",
            "",
            "**Ví dụ:** `2 3` / `S..` / `.#E` -> `3` (phải, phải, xuống).",
        ),
        [
            ("sample", "Vòng qua bức tường."),
            ("adjacent", "Xuống rồi phải."),
            ("blocked", "Cột tường kín hoàn toàn."),
            ("long detour", "Xuống, phải, phải, lên: bốn bước vòng qua tường."),
            ("adjacent columns", "Một bước."),
        ],
    ),
    "hsg-p16-treecheck": vi_challenge(
        "Có phải cây?",
        T(
            "**Đề bài:** Kết luận đồ thị vô hướng n đỉnh m cạnh có phải là cây hay không:",
            "liên thông VÀ đúng n-1 cạnh (không có chu trình).",
            "",
            "**Dữ liệu vào:** Dòng 1: n m (1 <= n <= 100000, 0 <= m <= 200000). m dòng tiếp: u v.",
            "**Dữ liệu ra:** In `YES` nếu là cây, ngược lại `NO`.",
            "",
            "**Ví dụ:** `3 2` / `1 2` / `2 3` -> `YES`.",
        ),
        [
            ("sample path", "Đường đi: liên thông, n-1 cạnh."),
            ("cycle", "Thừa cạnh."),
            ("disconnected", "Hai thành phần — số cạnh khớp nhưng liên thông hỏng."),
            ("self loop", "Khuyên tự thân là một chu trình."),
            ("double edge", "m == n-1 nhưng không liên thông — kiểm tra số cạnh một mình là chưa đủ."),
            ("single vertex", "Hiển nhiên là cây."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p16-graph",
    "Graph Theory Problem Set",
    "Components, BFS distances, flood fill, maze escape, and tree checking.",
    "Bài tập lý thuyết đồ thị",
    "Thành phần liên thông, khoảng cách BFS, flood fill, thoát mê cung, và kiểm tra cây.",
    "hsg-m16-traversal",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p16-components",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    int comps = 0;
    vector<int> st;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++comps;
        vis[s] = 1; st.push_back(s);
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }
        }
    }
    out << comps << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    int comps = 0;
    vector<int> st;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++comps;
        vis[s] = 1; st.push_back(s);
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u])
                // near-miss: iterates only the first neighbor — stunted DFS
                if (!vis[v]) { vis[v] = 1; st.push_back(v); break; }
        }
    }
    out << comps << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p16-bfs",
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[s] = 0; q.push(s);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
    }
    for (int v = 1; v <= n; ++v)
        out << dist[v] << (v == n ? "" : " ");
    out << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        // near-miss: builds a DIRECTED graph — drops the reverse edge
    }
    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[s] = 0; q.push(s);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u])
            if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
    }
    for (int v = 1; v <= n; ++v)
        out << dist[v] << (v == n ? "" : " ");
    out << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p16-flood",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    int rooms = 0;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            if (g[i][j] != '.') continue;
            ++rooms;
            vector<pair<int,int>> st{{i, j}};
            g[i][j] = '#';
            while (!st.empty()) {
                auto [r, c] = st.back(); st.pop_back();
                int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
                for (int d = 0; d < 4; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < m && g[nr][nc] == '.') {
                        g[nr][nc] = '#';
                        st.push_back({nr, nc});
                    }
                }
            }
        }
    out << rooms << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    int rooms = 0;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            if (g[i][j] != '.') continue;
            ++rooms;
            vector<pair<int,int>> st{{i, j}};
            g[i][j] = '#';
            while (!st.empty()) {
                auto [r, c] = st.back(); st.pop_back();
                // near-miss: floods only right/down — misses rooms that bend
                // around through up/left
                int dr[] = {1, 0}, dc[] = {0, 1};
                for (int d = 0; d < 2; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < m && g[nr][nc] == '.') {
                        g[nr][nc] = '#';
                        st.push_back({nr, nc});
                    }
                }
            }
        }
    out << rooms << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p16-grid-dist",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    pair<int,int> S{-1, -1}, E{-1, -1};
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            if (g[i][j] == 'S') S = {i, j};
            if (g[i][j] == 'E') E = {i, j};
        }
    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<pair<int,int>> q;
    dist[S.first][S.second] = 0;
    q.push(S);
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int d = 0; d < 4; ++d) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
            if (g[nr][nc] == '#' || dist[nr][nc] != -1) continue;
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    out << dist[E.first][E.second] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    pair<int,int> S{-1, -1}, E{-1, -1};
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            if (g[i][j] == 'S') S = {i, j};
            if (g[i][j] == 'E') E = {i, j};
        }
    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<pair<int,int>> q;
    dist[S.first][S.second] = 0;
    q.push(S);
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int d = 0; d < 4; ++d) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
            // near-miss: 'E' is not in the walkable set — never steps onto it
            if (g[nr][nc] == '#' || g[nr][nc] == 'E' || dist[nr][nc] != -1) continue;
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    out << dist[E.first][E.second] << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p16-treecheck",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    if (m != n - 1) { out << "NO" << "{{NL}}"; return; }
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        if (u == v) { out << "NO" << "{{NL}}"; return; }  // self-loop: cycle
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    vector<int> st{1};
    vis[1] = 1;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }
    }
    for (int v = 1; v <= n; ++v)
        if (!vis[v]) { out << "NO" << "{{NL}}"; return; }
    out << "YES" << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    if (m != n - 1) { out << "NO" << "{{NL}}"; return; }
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    vector<int> st{1};
    vis[1] = 1;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }
    }
    // near-miss: assumes m == n-1 already proves a tree — skips the
    // connectivity check entirely
    out << "YES" << "{{NL}}";
""") + END,
        ),
    ],
)

CH16 = challenge(
    "hsg-cp-m16-stations",
    "Radio Stations",
    T(
        "**Description:** A network of n radio stations (1..n) and m two-way links. Broadcasts",
        "from station s reach every station in s's connected component. For each of q",
        "queries (a, b), answer whether a message can travel between a and b.",
        "",
        "**Input:** Line 1: n m q (1 <= n <= 100000, 0 <= m <= 200000, 1 <= q <= 100000).",
        "Next m lines: u v (links). Next q lines: a b (queries).",
        "**Output:** q lines, each `YES` if a and b are connected, otherwise `NO`.",
        "",
        "**Example:** `3 1 2` / `1 2` / `1 2` / `1 3` -> `YES` / `NO`.",
    ),
    [
        contest_test("sample", T("3 1 2", "1 2", "1 2", "1 3"), T("YES", "NO"),
                     "1-2 linked; 3 is alone."),
        contest_test("same station", T("1 0 1", "1 1"), T("YES"), "A station reaches itself."),
        contest_test("all linked", T("4 3 2", "1 2", "2 3", "3 4", "1 4", "2 4"), T("YES", "YES"),
                     "One component — every query passes."),
        contest_test("no links", T("2 0 1", "1 2"), T("NO"), "Nothing travels."),
        contest_test("multi hop", T("5 2 3", "1 2", "2 3", "1 3", "1 4", "3 5"),
                     T("YES", "NO", "NO"),
                     "{1,2,3}, {4}, {5}: 1->2->3 travels two links; direct-link checkers print NO."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP16 = vi_challenge(
    "Trạm phát sóng",
    T(
        "**Đề bài:** Mạng n trạm phát sóng (1..n) và m liên kết hai chiều. Tín hiệu từ trạm s",
        "tới được mọi trạm trong thành phần liên thông của s. Với mỗi q truy vấn (a, b),",
        "trả lời tín hiệu đi được giữa a và b hay không.",
        "",
        "**Dữ liệu vào:** Dòng 1: n m q (1 <= n <= 100000, 0 <= m <= 200000, 1 <= q <= 100000).",
        "m dòng tiếp: u v (liên kết). q dòng tiếp: a b (truy vấn).",
        "**Dữ liệu ra:** q dòng, mỗi dòng `YES` nếu a và b liên thông, ngược lại `NO`.",
        "",
        "**Ví dụ:** `3 1 2` / `1 2` / `1 2` / `1 3` -> `YES` / `NO`.",
    ),
    [
        ("sample", "1-2 nối nhau; 3 tự tách."),
        ("same station", "Một trạm với chính nó."),
        ("all linked", "Một thành phần — mọi truy vấn đều qua."),
        ("no links", "Không gì đi được."),
        ("multi hop", "{1,2,3}, {4}, {5}: 1->2->3 đi hai liên kết; kiểm tra liên-kết-trực-tiếp sẽ in NO."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m16",
    "Checkpoint — Graph Theory",
    "Pass the graded problem to finish the graph module.",
    15,
    """**Checkpoint — lý thuyết đồ thị.** Pass the graded challenge below.
One component-labeling pass (a traversal from every unvisited vertex,
stamping a component id) then answers every query in O(1). The graded
near-misses: answering queries by launching a fresh traversal per query
(too slow at q = 10^5), and forgetting that a query can name the SAME
station twice.

**Điểm kiểm tra — lý thuyết đồ thị.** Pass bài chấm bên dưới. Một lượt
dán nhãn thành phần (duyet từ mỗi đỉnh chưa thăm, đóng dấu id thành
phần) rồi trả lời mọi truy vấn trong O(1). Các near-miss bị chấm: chạy
một lần duyệt mới cho từng truy vấn (quá chậm với q = 10^5), và quên
rằng truy vấn có thể gọi CÙNG một trạm hai lần.
""",
    "Checkpoint — Graph Theory",
    "Pass the graded problem to finish the graph module.",
    """**Điểm kiểm tra — lý thuyết đồ thị.** Pass bài chấm bên dưới. Một lượt
dán nhãn thành phần (duyet từ mỗi đỉnh chưa thăm, đóng dấu id thành
phần) rồi trả lời mọi truy vấn trong O(1). Các near-miss bị chấm: chạy
một lần duyệt mới cho từng truy vấn (quá chậm với q = 10^5), và quên
rằng truy vấn có thể gọi CÙNG một trạm hai lần.
""",
    CH16,
    VI_CP16,
    solution=CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<int> comp(n + 1, 0);
    int nextc = 0;
    vector<int> st;
    for (int s = 1; s <= n; ++s) {
        if (comp[s]) continue;
        ++nextc;
        comp[s] = nextc; st.push_back(s);
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u]) if (!comp[v]) { comp[v] = nextc; st.push_back(v); }
        }
    }
    string res;
    for (int i = 0; i < q; ++i) {
        int a, b; in >> a >> b;
        res += (comp[a] == comp[b]) ? "YES" : "NO";
        if (i + 1 < q) res += "{{NL}}";
    }
    out << res << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<int> comp(n + 1, 0);
    int nextc = 0;
    vector<int> st;
    for (int s = 1; s <= n; ++s) {
        if (comp[s]) continue;
        ++nextc;
        comp[s] = nextc; st.push_back(s);
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u]) if (!comp[v]) { comp[v] = nextc; st.push_back(v); }
        }
    }
    string res;
    for (int i = 0; i < q; ++i) {
        int a, b; in >> a >> b;
        // near-miss: direct-link check instead of component check —
        // multi-hop paths report NO
        bool ok = comp[a] == comp[b];
        if (a != b) {
            ok = false;
            for (int v : adj[a]) if (v == b) { ok = true; break; }
        }
        res += ok ? "YES" : "NO";
        if (i + 1 < q) res += "{{NL}}";
    }
    out << res << "{{NL}}";
""") + END,
)

print("M16 done")
