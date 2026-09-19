#!/usr/bin/env python3
"""HSG Intermediate — Module 10: hsgi-trees (Tree Techniques).

Rooted-tree traversal with parent-skip (iterative — no recursion-depth
risk), parent/depth reporting, subtree sizes via reverse-BFS accumulation,
pre-order with sorted children, tree diameter (DP on tree vs the max-depth
near-miss), and node-weight / edge-weight path DP. Graded checkpoint:
weighted cable diameter.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgi import (
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-trees"
write_module(
    M,
    "Trees — Traversal, Subtrees, and Diameter",
    "Parent-skip DFS/BFS (iterative), subtree sizes in reverse-BFS order, pre-order with sorted children, and diameter as the first DP on trees.",
    "Cây — Duyệt, cây con, và đường kính",
    "Duyệt cây với parent-skip (không đệ quy), kích thước cây con theo thứ tự BFS ngược, pre-order với con sắp tăng, và đường kính — DP trên cây đầu tiên.",
    ["hsgi-m10-traverse", "hsgi-m10-diameter", "hsgi-cp-m10"],
    ["hsgi-p10-trees"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m10-traverse",
    "Traversing Trees — The Parent-Skip Pattern",
    "A tree with n nodes has exactly n−1 edges; store undirected adjacency, skip the parent, and never need a visited array — but always iterate, never recurse deeply.",
    18,
    """## What makes a tree different

Cây: n đỉnh, n−1 cạnh, liên thông, không chu trình. Ba hệ quả dùng liên
tục: (1) mọi cặp đỉnh nối bằng ĐÚNG MỘT đường; (2) bỏ đi một cạnh → đồ
thị tách đôi; (3) thêm một cạnh → tạo đúng một chu trình.

### The parent-skip pattern

Lưu cạnh VÔ HƯỚNG (cả hai chiều), duyệt BFS/DFS từ gốc 1, và khi đứng ở
u bỏ qua đỉnh vừa đi từ nó (cha):

```cpp
vector<vector<int>> adj;          // CẢ HAI CHIỀU
vector<int> par, dep;

void bfs(int root) {
    par.assign(n + 1, 0);
    dep.assign(n + 1, 0);
    queue<int> bq;
    bq.push(root);
    par[root] = 0;                // gốc không có cha
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (v != par[u]) {    // parent-skip
                par[v] = u;
                dep[v] = dep[u] + 1;
                bq.push(v);
            }
    }
}
```

Không cần visited: mọi đỉnh chỉ có MỘT cha — parent-skip chặn đường quay
lại duy nhất.

### The one direction to store

Quên `adj[v].push_back(u)` là lỗi phổ biến nhất: cây trở thành đồ thị
CÓ HƯỚNG theo thứ tự đọc; các cạnh "con trước, cha sau" bị mất — một
phần cây biến mất khỏi phép duyệt. Test phản đối: liệt kê ít nhất một
cạnh theo thứ tự con-cha.

### Iterative only

Chuỗi n = 200 000 làm DFS đệ quy sâu 200 000 khung — rủi ro tràn ngăn
xếp. BFS ở trên (hoặc DFS với stack tường minh) là hình thức an toàn.

### Subtree sizes without recursion

Thứ tự BFS từ gốc có tính chất: cha luôn đứng TRƯỚC con. Đảo lại và cộng
size[par] += size[u]: được post-order mà không đệ quy.

```cpp
vector<int> order;                // từ BFS
vector<long long> sz(n + 1, 1);
for (int i = n - 1; i >= 0; --i) {
    int u = order[i];
    if (par[u]) sz[par[u]] += sz[u];
}
```

**Điểm mấu chốt:** hai chiều + parent-skip; cha trước con trong BFS;
đảo BFS = post-order rẻ.""",
    "Duyệt cây — Mẫu parent-skip",
    "Cây n đỉnh có n−1 cạnh; lưu adjacency vô hướng, bỏ qua cha, không cần visited — và luôn khử đệ quy.",
    """## Điều gì làm cây khác biệt

Cây: n đỉnh, n−1 cạnh, liên thông, không chu trình. Ba hệ quả: (1) mọi
cặp đỉnh nối bằng ĐÚNG MỘT đường; (2) bỏ một cạnh → tách đôi; (3) thêm
một cạnh → đúng một chu trình.

### Mẫu parent-skip

Lưu cạnh VÔ HƯỚNG, duyệt từ gốc 1, bỏ qua cha:

```cpp
vector<vector<int>> adj;          // CẢ HAI CHIỀU
vector<int> par, dep;

void bfs(int root) {
    par.assign(n + 1, 0);
    dep.assign(n + 1, 0);
    queue<int> bq;
    bq.push(root);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (v != par[u]) {    // parent-skip
                par[v] = u;
                dep[v] = dep[u] + 1;
                bq.push(v);
            }
    }
}
```

Không cần visited: mọi đỉnh chỉ MỘT cha — parent-skip chặn duy nhất
đường quay lại.

### Một hướng phải nhớ

Quên `adj[v].push_back(u)`: cạnh "con trước, cha sau" bị mất — một
phần cây biến mất. Test phản đối: ít nhất một cạnh liệt kê theo kiểu
con-cha.

### Khử đệ quy

Chuỗi n = 200 000 → DFS đệ quy sâu 200 000 khung: rủi ro tràn ngăn xếp.
BFS (hoặc stack tường minh) là hình thức an toàn.

### Kích thước cây con không đệ quy

BFS từ gốc: cha luôn TRƯỚC con. Đảo thứ tự và cộng:

```cpp
vector<int> order;                // từ BFS
vector<long long> sz(n + 1, 1);
for (int i = n - 1; i >= 0; --i) {
    int u = order[i];
    if (par[u]) sz[par[u]] += sz[u];
}
```

**Điểm mấu chốt:** hai chiều + parent-skip; cha trước con; đảo BFS =
post-order rẻ.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m10-diameter",
    "Tree Diameter — The First DP on Trees",
    "For every node, combine the two best downward paths; the answer never has to pass through the root.",
    18,
    """## The definition

Đường kính: số cạnh (hoặc tổng trọng số) của đường đi DÀI NHẤT trên cây.
Đường đi trên cây = đường giữa hai đỉnh — KHÔNG nhất quán đi qua gốc.

### The near-miss to kill first

"Chiều cao cây từ gốc" ≠ đường kính. Cây 1–2, 1–3, 2–4, 3–5: chiều cao
từ 1 là 2, đường kính là 4 (4–2–1–3–5). Mọi nghiệm "từ gốc đi
xuống" đều sai khi đường dài nhất nằm giữa hai nhánh.

### The DP

Với mỗi u, down[u] = đường đi dài nhất XUỐNG XUỐNG từ u (đi vào một cây
con). Khi duyệt u, hai giá trị tốt nhất trong các down[child] + w(u, c)
cho đường đi tốt nhất CHỨA u như khúc khuỷu:

```cpp
long long best = 0;
// duyệt theo BFS order (cha trước con), xử lý NGƯỢC:
for (int i = order.size() - 1; i >= 0; --i) {
    int u = order[i];
    // down[u] đã sẵn sàng (đã cộng từ con)
    long long d1 = 0, d2 = 0;          // hai nhánh tốt nhất
    // khi xử lý u: gộp mỗi con c một lần
    // d1 ≥ d2
    // best = max(best, d1 + d2);        // đường qua u
    // xuống cha: down[par] = max(down[par], d1 + w)
}
```

Chi tiết cài đặt: duyệt ngược BFS order; với mỗi u giữ d1, d2 = hai giá
trị lớn nhất của (down[c] + w(u,c)) cho con c; cập nhật best bằng
d1 + d2 và đẩy d1 + w lên cha. Mỗi cạnh xử lý đúng một lần: O(n).

### The two-BFS alternative

Phép "ma thuật" kinh điển: BFS từ đỉnh bất kỳ → đỉnh a xa nhất; BFS từ
a → đỉnh b xa nhất; khoảng cách a–b là đường kính. ĐÚNG cho cây (có
chứng minh) nhưng bí ẩn hơn; DP ở trên là khung tổng quát dùng lại được
cho trọng số, đếm đường, v.v. Hãy thuộc DP; two-BFS chỉ để kiểm chéo.

### Why graphs break this

Trên đồ thị tổng quát, đường dài nhất là NP-khó. Cây đặc biệt: đường
giữa hai đỉnh DUY NHẤT — DP hợp lệ. Nhận diện "cây + đường dài nhất" →
DP hai nhánh.

**Điểm mấu chốt:** down[u] = nhánh tốt nhất; đường qua u = d1 + d2;
đáp án KHÔNG phải chiều cao từ gốc.""",
    "Đường kính cây — DP trên cây đầu tiên",
    "Với mỗi đỉnh, gộp hai nhánh đi xuống tốt nhất; đáp án không cần đi qua gốc.",
    """## Định nghĩa

Đường kính: đường đi DÀI NHẤT trên cây (số cạnh hoặc tổng trọng số).
Đường giữa hai đỉnh — KHÔNG nhất quán qua gốc.

### Near-miss cần diệt ngay

"Chiều cao từ gốc" ≠ đường kính. Cây 1–2, 1–3, 2–4, 3–5: chiều cao 2,
đường kính 4 (4–2–1–3–5). Mọi nghiệm "từ gốc xuống" sai khi đường dài
nhất nằm giữa hai nhánh.

### DP

down[u] = đường dài nhất từ u đi XUỐNG một cây con. Với u: d1, d2 = hai
giá trị (down[c] + w) lớn nhất trong các con; đường qua u = d1 + d2:

```cpp
long long best = 0;
for (int i = order.size() - 1; i >= 0; --i) {   // ngược BFS
    int u = order[i];
    long long d1 = 0, d2 = 0;
    // với mỗi con c: val = down[c] + w(u, c)
    //   cập nhật d1/d2 (hai giá trị lớn nhất)
    // best = max(best, d1 + d2);
    // down[par[u]] = max(down[par[u]], d1 + w(u, par));
}
```

Mỗi cạnh một lần: O(n).

### Hai lần BFS

BFS từ đỉnh bất kỳ → a xa nhất; BFS từ a → b xa nhất: a–b là đường
kính. ĐÚNG nhưng bí ẩn; DP tổng quát hơn (trọng số, đếm đường). Thuộc
DP; two-BFS để kiểm chéo.

### Vì sao đồ thị phá nó

Đường dài nhất trên đồ thị tổng quát là NP-khó. Cây đặc biệt: đường
giữa hai đỉnh DUY NHẤT. Nhận diện "cây + đường dài nhất" → DP hai
nhánh.

**Điểm mấu chốt:** down[u] = nhánh tốt nhất; qua u = d1 + d2; KHÔNG
phải chiều cao gốc.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p10-family",
    "Cây phả hệ",
    """**Bài toán.** Cây n đỉnh gốc tại 1; n−1 cạnh liệt kê theo thứ tự bất
kỳ. Với mỗi đỉnh 1..n in "cha độ-sâu" trên một dòng (cha của gốc là 0,
độ sâu gốc là 0).

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ u, v ≤ n.""",
    [
        contest_test(
            "ví dụ",
            T("4", "1 2", "1 3", "4 3"),
            T("0 0", "1 1", "1 1", "3 2"),
            "Cạnh 4-3 liệt kê CON-TRƯỚC: vẫn phải nối đúng — parent(4) = 3, depth 2.",
        ),
        contest_test(
            "hai đỉnh",
            T("2", "2 1"),
            T("0 0", "1 1"),
            "Cạnh duy nhất cũng liệt kê ngược — gốc vẫn là 1.",
        ),
        contest_test(
            "chổi — nhánh lệch",
            T("5", "1 2", "2 3", "3 4", "3 5"),
            T("0 0", "1 1", "2 2", "3 3", "3 3"),
            "Đỉnh 4, 5 cùng cha 3 cùng độ sâu 3.",
        ),
        contest_test(
            "n lớn — chuỗi cạnh ngược toàn bộ",
            T("200000")
            + T(*[str(i + 1) + " " + str(i) for i in range(1, 200000)]),
            T("0 0") + T(*[str(i - 1) + " " + str(i - 1) for i in range(2, 200001)]),
            "Chuỗi 2→1, 3→2, ...: mọi cạnh ngược — BFS cha-trước-con vẫn trả đúng; W mất cạnh ngược sẽ bỏ sót nửa cây.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p10-subtree",
    "Kích thước cây con",
    """**Bài toán.** Cây n đỉnh gốc tại 1. In size(i) — số đỉnh trong cây
con gốc i — cho mọi i theo thứ tự 1..n, mỗi đỉnh một dòng.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ u, v ≤ n.""",
    [
        contest_test(
            "ví dụ",
            T("4", "1 2", "1 3", "3 4"),
            T("4", "1", "2", "1"),
            "size(1) = 4 toàn cây; 3 có con 4; lá có size 1.",
        ),
        contest_test(
            "chuỗi năm đỉnh",
            T("5", "1 2", "2 3", "3 4", "4 5"),
            T("5", "4", "3", "2", "1"),
            "Chuỗi: size(i) = n − i + 1 — W chỉ đếm con trực tiếp sẽ ra 1,1,1,1,0.",
        ),
        contest_test(
            "ngôi sao",
            T("5", "1 2", "1 3", "1 4", "1 5"),
            T("5", "1", "1", "1", "1"),
            "Gốc giữ cả 5; mọi lá size 1.",
        ),
        contest_test(
            "n lớn — chuỗi khổng lồ",
            T("200000")
            + T(*[str(i) + " " + str(i + 1) for i in range(1, 200000)]),
            T(*[str(200001 - i) for i in range(1, 200001)]),
            "Chuỗi 1..200000: size giảm từ 200000 về 1 — đảo BFS order cộng một lượt, O(n).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p10-diameter",
    "Đường kính cây",
    """**Bài toán.** Cây n đỉnh; in số cạnh của đường đi dài nhất (đường
kính). Đường đi KHÔNG nhất quán đi qua gốc.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ u, v ≤ n.""",
    [
        contest_test(
            "chuỗi — đường kính qua gốc",
            T("5", "1 2", "2 3", "3 4", "4 5"),
            T("4"),
            "Chuỗi 5 đỉnh: đường kính 4 cạnh — đi qua mọi đỉnh.",
        ),
        contest_test(
            "hai nhánh qua gốc",
            T("5", "1 2", "1 3", "2 4", "3 5"),
            T("4"),
            "Đường 4–2–1–3–5 dài 4 cạnh nhưng chiều cao từ 1 chỉ là 2 — nghiệm chỉ xét gốc→lá trả 2.",
        ),
        contest_test(
            "ngôi sao",
            T("5", "1 2", "1 3", "1 4", "1 5"),
            T("2"),
            "Mọi đường qua 1: dài đúng 2 cạnh.",
        ),
        contest_test(
            "hai chổi đối xứng",
            T("7", "1 2", "2 3", "2 4", "4 5", "5 6", "5 7"),
            T("4"),
            "Đường 3–2–4–5–6: 4 cạnh (3–2, 2–4, 4–5, 5–6) — hai nhánh gộp qua khúc khuỷu 2–4.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p10-preorder",
    "Duyệt trước — thứ tự chuẩn",
    """**Bài toán.** Cây n đỉnh gốc tại 1. In duyệt TRƯỚC (pre-order): gốc
trước, rồi các cây con; các con duyệt theo SỐ HIỆU TĂNG DẦN. In trên
một dòng, cách nhau dấu cách.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ u, v ≤ n.""",
    [
        contest_test(
            "ví dụ",
            T("4", "1 2", "1 3", "2 4"),
            T("1 2 4 3"),
            "Gốc 1; con {2,3} tăng dần — cây con của 2 (gồm 4) in trước cây con 3.",
        ),
        contest_test(
            "con ngược trong input",
            T("4", "1 3", "1 2", "2 4"),
            T("1 2 4 3"),
            "Cạnh 1-3 xuất hiện trước 1-2 nhưng SẮP theo số hiệu: 2 trước 3 — không tin thứ tự đọc.",
        ),
        contest_test(
            "ngôi sao sắp từ điển",
            T("5", "1 5", "1 4", "1 3", "1 2"),
            T("1 2 3 4 5"),
            "Bốn lá in tăng dần dù input đưa ngược.",
        ),
        contest_test(
            "chổi lệch phải",
            T("6", "3 1", "3 2", "2 4", "4 5", "4 6"),
            T("1 3 2 4 5 6"),
            "Gốc 1 → con 3; cây con của 3 đi 2 (→4→5,6) — pre-order 1 3 2 4 5 6.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p10-weightpath",
    "Đường đi năng lượng tốt nhất",
    """**Bài toán.** Cây n đỉnh, đỉnh i có năng lượng w_i. Chọn đường đi
trên cây (các đỉnh đôi một khác nhau) có TỔNG w lớn nhất. In tổng đó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ w_i ≤ 10^9; 1 ≤ u, v ≤ n.

Tổng tới 2·10^14 — long long.""",
    [
        contest_test(
            "chuỗi",
            T("4 3 7 2 5", "1 2", "2 3", "3 4"),
            T("17"),
            "Cả chuỗi 3+7+2+5 = 17 — đường đi duy nhất dài nhất.",
        ),
        contest_test(
            "một đỉnh",
            T("1 42"),
            T("42"),
            "Đường đi một đỉnh: chính nó.",
        ),
        contest_test(
            "hai nhánh nặng qua khúc khuỷu",
            T("5 1 10 10 10 10", "1 2", "2 4", "1 3", "3 5"),
            T("41"),
            "4→2→1→3→5 = 10+10+1+10+10 = 41 — đường KHÔNG qua một nhánh đơn; đường từ gốc xuống lá chỉ được 21.",
        ),
        contest_test(
            "n lớn — chuỗi toàn 10^9",
            T("200000 " + " ".join(["1000000000"] * 200000))
            + T(*[str(i) + " " + str(i + 1) for i in range(1, 200000)]),
            T("200000000000000"),
            "Cả chuỗi: 200000 × 10^9 = 2·10^14 — DP hai nhánh quét một lượt.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI10 = {
    "hsgi-p10-family": vi_challenge(
        "Cây phả hệ",
        """**Bài toán.** Cây n đỉnh gốc 1, cạnh liệt kê bất kỳ thứ tự. Với mỗi
đỉnh in "cha độ-sâu"; gốc in "0 0".""",
        [("ví dụ", "Cạnh con-trước vẫn nối đúng: 4 có cha 3."),
         ("n lớn", "BFS + parent-skip, O(n).")],
    ),
    "hsgi-p10-subtree": vi_challenge(
        "Kích thước cây con",
        """**Bài toán.** Cây gốc 1: in size(i) — số đỉnh cây con gốc i —
mỗi đỉnh một dòng.""",
        [("ví dụ", "4, 1, 2, 1."),
         ("n lớn", "Đảo BFS order, cộng một lượt.")],
    ),
    "hsgi-p10-diameter": vi_challenge(
        "Đường kính cây",
        """**Bài toán.** In số cạnh của đường đi dài nhất — KHÔNG nhất quán
qua gốc.""",
        [("chổi", "Chiều cao 3 nhưng đường kính 4."),
         ("n lớn", "DP hai nhánh, O(n).")],
    ),
    "hsgi-p10-preorder": vi_challenge(
        "Duyệt trước — thứ tự chuẩn",
        """**Bài toán.** Pre-order: gốc trước, con duyệt theo số hiệu tăng
dần — bất kể thứ tự input.""",
        [("ví dụ", "1 2 4 3."),
         ("input ngược", "Sắp adjacency trước khi duyệt.")],
    ),
    "hsgi-p10-weightpath": vi_challenge(
        "Đường đi năng lượng tốt nhất",
        """**Bài toán.** Chọn đường đi các đỉnh khác nhau có tổng w lớn nhất.
long long!""",
        [("hai nhánh", "41 > 21: đường gập qua gốc."),
         ("n lớn", "DP hai nhánh một lượt.")],
    ),
}

write_practice(
    M,
    "hsgi-p10-trees",
    "Tree Problem Set",
    "Five problems: parent/depth reporting, subtree sizes, diameter, sorted pre-order, and max node-weight path.",
    "Bài tập cây",
    "Năm bài: cha + độ sâu, kích thước cây con, đường kính, pre-order sắp tăng, và đường đi tổng trọng số lớn nhất.",
    "hsgi-m10-diameter",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI10,
    solutions=[
        (
            "hsgi-p10-family",
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (v != par[u]) {
                par[v] = u;
                dep[v] = dep[u] + 1;
                bq.push(v);
            }
    }
    for (int i = 1; i <= n; ++i)
        out << par[i] << " " << dep[i] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    // near-miss: chỉ lưu MỘT CHIỀU theo thứ tự đọc — cạnh "con trước,
    // cha sau" bị mất, nửa cây biến mất khỏi phép duyệt
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
    }
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (v != par[u]) {
                par[v] = u;
                dep[v] = dep[u] + 1;
                bq.push(v);
            }
    }
    for (int i = 1; i <= n; ++i)
        out << par[i] << " " << dep[i] << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p10-subtree",
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (v != par[u]) {
                par[v] = u;
                bq.push(v);
            }
    }
    vector<long long> sz(n + 1, 1);
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];
        if (par[u]) sz[par[u]] += sz[u];
    }
    for (int i = 1; i <= n; ++i) out << sz[i] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> par(n + 1, 0);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (v != par[u]) { par[v] = u; bq.push(v); }
    }
    // near-miss: size = số con TRỰC TIẾP (degree trong cây gốc) — đếm
    // thiếu cả nhánh dưới; trên chuỗi mọi node trả 1 thay vì n−i+1
    for (int i = 1; i <= n; ++i) out << (long long)adj[i].size() - (i != 1) << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p10-diameter",
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (v != par[u]) { par[v] = u; bq.push(v); }
    }
    // down[u] = chiều dài nhánh dài nhất đi XUỐNG từ u
    vector<int> down(n + 1, 0);
    int best = 0;
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];
        int d1 = 0, d2 = 0;                     // hai nhánh tốt nhất
        for (int v : adj[u]) {
            if (v == par[u]) continue;
            int val = down[v] + 1;
            if (val > d1) { d2 = d1; d1 = val; }
            else if (val > d2) d2 = val;
        }
        down[u] = d1;
        if (d1 + d2 > best) best = d1 + d2;     // đường qua u
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> par(n + 1, 0), dep(n + 1, 0);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (v != par[u]) {
                par[v] = u;
                dep[v] = dep[u] + 1;
                bq.push(v);
            }
    }
    // near-miss: trả CHIỀU CAO từ gốc — đường dài nhất không qua gốc
    // (chổi hai nhánh) bị tính thiếu
    int best = 0;
    for (int i = 1; i <= n; ++i)
        if (dep[i] > best) best = dep[i];
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p10-preorder",
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    for (int i = 1; i <= n; ++i)
        sort(adj[i].begin(), adj[i].end());     // con duyệt theo số hiệu
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    // DFS bằng stack tường minh — đưa con theo THỨ TỰ NGƯỢC để pop ra
    // đúng tăng dần
    vector<int> st;
    st.push_back(1);
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        order.push_back(u);
        for (auto it = adj[u].rbegin(); it != adj[u].rend(); ++it)
            if (*it != par[u]) {
                par[*it] = u;
                st.push_back(*it);
            }
    }
    for (size_t i = 0; i < order.size(); ++i)
        out << order[i] << " \\n"[i + 1 == order.size()];
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    for (int i = 1; i <= n; ++i)
        sort(adj[i].begin(), adj[i].end());
    // near-miss: DUYỆT TẦNG (BFS) thay vì pre-order — đúng trên sao,
    // sai ngay khi cây có độ sâu 2 trở lên
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (v != par[u]) { par[v] = u; bq.push(v); }
    }
    for (size_t i = 0; i < order.size(); ++i)
        out << order[i] << " \\n"[i + 1 == order.size()];
""") + END,
        ),
        (
            "hsgi-p10-weightpath",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> w(n + 1);
    for (int i = 1; i <= n; ++i) in >> w[i];
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (v != par[u]) { par[v] = u; bq.push(v); }
    }
    // down[u] = w[u] + nhánh con tốt nhất (hoặc chỉ w[u] nếu mọi nhánh kém)
    vector<long long> down(n + 1, 0);
    long long best = 0;
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];
        long long d1 = 0, d2 = 0;               // hai nhánh tốt nhất (≥ 0)
        for (int v : adj[u]) {
            if (v == par[u]) continue;
            long long val = down[v];
            if (val > d1) { d2 = d1; d1 = val; }
            else if (val > d2) d2 = val;
        }
        down[u] = w[u] + d1;
        best = max(best, w[u] + d1 + d2);       // đường qua u
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> w(n + 1);
    for (int i = 1; i <= n; ++i) in >> w[i];
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (v != par[u]) { par[v] = u; bq.push(v); }
    }
    // near-miss: chỉ xét đường TỪ GỐC XUỐNG LÁ (một nhánh) — đường gập
    // qua gốc hai nhánh nặng bị bỏ; trên "hai nhánh 10" trả 21 thay vì 41
    vector<long long> down(n + 1, 0);
    long long best = 0;
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];
        long long bestChild = 0;
        for (int v : adj[u]) {
            if (v == par[u]) continue;
            bestChild = max(bestChild, down[v]);
        }
        down[u] = w[u] + bestChild;
        best = max(best, down[u]);
    }
    out << best << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH10 = challenge(
    "hsgi-cp-m10-cable",
    "Checkpoint — Trục cáp quang",
    """**Bài toán.** Tòa nhà có n phòng; n−1 cáp nối (u, v, w) với w là
độ dài cáp — mạng đảm bảo dạng CÂY (mọi phòng liên thông, không chu
trình). Hai phòng p, q được nối server nếu dùng cáp trên đường p–q.
Chọn p, q để TỔNG ĐỘ DÀI cáp của đường p–q LỚN NHẤT (server phủ xa
nhất). In tổng đó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ w ≤ 10^9; 1 ≤ u, v ≤ n.

Tổng tới ~2·10^14 — long long.""",
    [
        contest_test(
            "chuỗi cáp",
            T("4", "1 2 3", "2 3 4", "3 4 5"),
            T("12"),
            "Cây là chuỗi: 3+4+5 = 12 từ phòng 1 đến phòng 4.",
        ),
        contest_test(
            "một phòng — không cần cáp",
            T("1"),
            T("0"),
            "Chỉ một phòng: đường đi rỗng dài 0.",
        ),
        contest_test(
            "chổi — đường tránh gốc",
            T("5", "1 2 1", "2 3 9", "2 4 9", "4 5 8"),
            T("26"),
            "Đường 3–2–4–5: 9+9+8 = 26; nhánh sâu nhất từ 1 chỉ 1-2-4-5 = 18 — nghiệm một nhánh trả 18.",
        ),
        contest_test(
            "n lớn — chuỗi cáp khổng lồ",
            T("200000")
            + T(*[str(i) + " " + str(i + 1) + " 1000000000" for i in range(1, 200000)]),
            T("199999000000000"),
            "Chuỗi 199999 cáp × 10^9 = 199999000000000 — DP hai nhánh quét một lượt, long long.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP10 = vi_challenge(
    "Checkpoint — Trục cáp quang",
    """**Bài toán.** Mạng n phòng dạng cây; cáp (u, v, w). Chọn p, q để
tổng độ dài đường p–q lớn nhất. In tổng.""",
    [("chuỗi", "3+4+5 = 12."),
     ("chổi", "Đường 3–2–4–5 = 26, tránh gốc."),
     ("n lớn", "DP hai nhánh, long long.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m10",
    "Checkpoint — Trees",
    "Pass the graded problem to finish the tree techniques module.",
    25,
    """**Checkpoint — Trees.** Pass the graded challenge below to complete
the module: weighted diameter as DP on trees — two best downward
branches per node, best = max(d1 + d2) — plus long long sums and the
n = 1 edge case. The "two branches" is where solutions break: taking
only the single best child (root-to-leaf) silently undercounts on
brooms, exactly the failure mode this module drilled.

**Điểm kiểm tra — Cây.** Pass bài chấm bên dưới để hoàn thành module:
đường kính có trọng số bằng DP hai nhánh (d1 + d2), long long, và
trường hợp n = 1. "Hai nhánh" là chỗ gãy: chỉ lấy một con tốt nhất
(đường gốc→lá) tính thiếu trên cây chổi — đúng lỗi module này đã luyện.""",
    "Checkpoint — Trees",
    "Pass bài chấm để hoàn thành module cây.",
    """**Điểm kiểm tra — Cây.** Pass bài chấm bên dưới: DP hai nhánh cho
đường kính có trọng số; long long; n = 1 → 0.""",
    CH10,
    VI_CP10,
    solution=CPP_STD + cpp("""    int n; in >> n;
    if (n == 1) { out << 0 << "{{NL}}"; return; }
    vector<long long> wv(n + 1, 0);
    vector<vector<array<long long,2>>> adj(n + 1);   // (đỉnh, trọng số)
    for (int i = 0; i < n - 1; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (auto& [v, w] : adj[u])
            if (v != par[u]) { par[v] = u; bq.push(v); }
    }
    vector<long long> down(n + 1, 0);
    long long best = 0;
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];
        long long d1 = 0, d2 = 0;
        for (auto& [v, w] : adj[u]) {
            if (v == par[u]) continue;
            long long val = down[v] + w;
            if (val > d1) { d2 = d1; d1 = val; }
            else if (val > d2) d2 = val;
        }
        down[u] = d1;
        best = max(best, d1 + d2);
    }
    out << best << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    if (n == 1) { out << 0 << "{{NL}}"; return; }
    vector<vector<array<long long,2>>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    vector<int> par(n + 1, 0), order;
    order.reserve(n);
    queue<int> bq;
    bq.push(1);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (auto& [v, w] : adj[u])
            if (v != par[u]) { par[v] = u; bq.push(v); }
    }
    // near-miss: CHIỀU CAO CÓ TRỌNG SỐ từ gốc (một nhánh) thay vì d1 + d2 —
    // đường gập qua gốc hai nhánh nặng bị tính thiếu trên cây chổi
    vector<long long> down(n + 1, 0);
    long long best = 0;
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];
        long long bestChild = 0;
        for (auto& [v, w] : adj[u]) {
            if (v == par[u]) continue;
            bestChild = max(bestChild, down[v] + w);
        }
        down[u] = bestChild;
        best = max(best, down[u]);
    }
    out << best << "{{NL}}";
""") + END,
)
