#!/usr/bin/env python3
"""HSG Intermediate — Module 7: hsgi-dsu (DSU & Minimum Spanning Tree).

Union–find with path halving + union by size, dynamic component counting,
Kruskal's MST, redundant-edge detection, bottleneck (min-max edge) queries
via offline small-to-large merging, and a graded checkpoint (MST or −1).

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
#include <array>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-dsu"
write_module(
    M,
    "DSU & Minimum Spanning Trees — Connectivity as a Tool",
    "Disjoint set union with path halving and union by size, Kruskal's MST, redundant edges, and bottleneck queries answered offline while the forest grows.",
    "DSU & Cây khung nhỏ nhất — Liên thông thành công cụ",
    "Disjoint set union với path halving và hợp theo kích thước, cây khung nhỏ nhất Kruskal, cạnh thừa, và truy vấn bottleneck trả lời offline trong lúc rừng lớn dần.",
    ["hsgi-m7-uf", "hsgi-m7-mst", "hsgi-cp-m7"],
    ["hsgi-p7-dsu"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m7-uf",
    "Union–Find — Near-Constant Connectivity",
    "The two optimizations that make DSU effectively O(α(n)): path halving and union by size, plus the connectivity counter pattern.",
    16,
    """## The problem

n người, m quan hệ bạn bè: "hai người này có chung một nhóm bạn?" — trả
lời mỗi câu trong O(1)? Không hoàn toàn, nhưng O(α(n)) — nghịch đảo Ackermann,
≤ 4 cho mọi kích thước thực tế — đủ gần.

### The structure: a forest of parent pointers

Mỗi tập hợp là một cây: mỗi đỉnh trỏ lên cha; gốc là "đại diện" của tập.

```cpp
vector<int> par, sz_;

void init(int n) {
    par.resize(n + 1); sz_.assign(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
}

int find(int x) {                    // path HALVING
    while (par[x] != x) {
        par[x] = par[par[x]];        // nhảy cóc lên ông nội
        x = par[x];
    }
    return x;
}

bool unite(int a, int b) {           // union by SIZE
    a = find(a); b = find(b);
    if (a == b) return false;        // đã cùng tập — KHÔNG hợp lại
    if (sz_[a] < sz_[b]) swap(a, b);
    par[b] = a; sz_[a] += sz_[b];
    return true;
}
```

### The two optimizations are not optional

- **Path halving** (mỗi lần tìm lại nối x lên ông nội) làm cây phẳng dần
  sau mỗi truy vấn.
- **Union by size** (cây NHỎER nhập vào cây LỚN hơn) giữ chiều sâu cây
  O(log n) ngay cả khi không có path compression.

Chỉ một trong hai: O(log n). Cả hai: O(α(n)) — thực tế là hằng số.

### The counter pattern

Đếm thành phần: khởi đầu là n; mỗi lần unite TRẢ VỀ TRUE (hai tập khác
nhau vừa nhập) giảm 1. Mọi lần unite trả về FALSE (u, v đã liên thông)
KHÔNG đổi số đếm — quên nhánh này là lỗi kinh điển (bài 7.1).

### Find without recursion

find VIẾT Đệ quy dễ nhưng sâu 10^5 gây tràn ngăn xếp trong sandbox —
vòng while ở trên là hình thức an toàn duy nhất bạn cần nhớ.

**Điểm mấu chốt:** DSU = rừng cha + path halving + union by size;
unite trả về FALSE khi hai đỉnh đã liên thông — tín hiệu.cycle.""",
    "Union–Find — Liên thông gần hằng số",
    "Hai tối ưu hóa đưa DSU về O(α(n)): path halving và union by size, cùng mẫu đếm thành phần.",
    """## Vấn đề

n người, m quan hệ bạn bè: "hai người này cùng nhóm?" — trả lời mỗi câu
trong O(α(n)) — nghịch đảo Ackermann, ≤ 4 cho mọi kích thước thực tế.

### Cấu trúc: rừng con trỏ cha

Mỗi tập là một cây: mỗi đỉnh trỏ lên cha; gốc là đại diện của tập.

```cpp
vector<int> par, sz_;

void init(int n) {
    par.resize(n + 1); sz_.assign(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
}

int find(int x) {                    // path HALVING
    while (par[x] != x) {
        par[x] = par[par[x]];        // nhảy cóc lên ông nội
        x = par[x];
    }
    return x;
}

bool unite(int a, int b) {           // union by SIZE
    a = find(a); b = find(b);
    if (a == b) return false;        // đã cùng tập — KHÔNG hợp lại
    if (sz_[a] < sz_[b]) swap(a, b);
    par[b] = a; sz_[a] += sz_[b];
    return true;
}
```

### Hai tối ưu không phải tùy chọn

- **Path halving** làm cây phẳng dần sau mỗi truy vấn.
- **Union by size** giữ chiều sâu O(log n) ngay cả khi không có path
  compression.

Chỉ một: O(log n). Cả hai: O(α(n)) — thực tế là hằng số.

### Mẫu bộ đếm

Đếm thành phần: khởi đầu n; mỗi unite trả TRUE giảm 1. unite trả FALSE
(u, v đã liên thông) KHÔNG đổi số đếm — quên nhánh này là lỗi kinh điển.

### find không đệ quy

find đệ quy sâu 10^5 gây tràn ngăn xếp trong sandbox — vòng while là
hình thức an toàn duy nhất cần nhớ.

**Điểm mấu chốt:** DSU = rừng cha + path halving + union by size;
unite trả FALSE khi đã liên thông.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m7-mst",
    "Kruskal — Greedy on Sorted Edges",
    "Sort edges ascending, unite greedily, skip edges inside a component: the cycle property, the bottleneck property, and the −1 disconnected case.",
    18,
    """## The algorithm

Cây khung nhỏ nhất (MST): chọn n−1 cạnh có tổng trọng số nhỏ nhất giữ
nguyên đồ thị liên thông. Kruskal:

1. Sắp mọi cạnh theo trọng số TĂNG DẦN.
2. Duyệt lần lượt: cạnh (u, v, w) — nếu find(u) ≠ find(v), unite và
   NHẬN cạnh; ngược lại BỎ (nó tạo chu trình).
3. Dừng sau n−1 cạnh nhận.

Độ phức tạp: O(m log m) cho sort — phần DSU chỉ O(m α(n)).

```cpp
long long kruskal(int n, vector<array<long long,3>>& e) {
    sort(e.begin(), e.end());            // theo w
    long long total = 0; int taken = 0;
    for (auto& [w, u, v] : e) {
        if (unite(u, v)) { total += w; ++taken; }
        if (taken == n - 1) break;
    }
    return taken == n - 1 ? total : -1;  // -1: đồ thị không liên thông
}
```

### Why greed is safe here (the cycle property)

Cạnh nhẹ nhất của MỌI "cắt" (partition đỉnh thành hai phần) luôn thuộc
một MST nào đó. Khi Kruskal nhặt cạnh w nhỏ nhất nối hai thành phần,
không cạnh đắt hơn nào có thể thay nó — đổi vào chỉ làm tổng tăng.
Đây là một trong số ít tham lam có CHỨNG MINH ngắn gọn — hãy nhớ cảm
giác: "cạnh nhỏ nhất vượt qua mỗi ranh giới".

### The bottleneck property (dùng lại ở bài 7.4)

Trên đường đi u→v trong MST, cạnh TỐI ĐA là nhỏ nhất có thể so với mọi
đường đi khác. Hệ quả: trả lời "truy vấn bottleneck" bằng cách ghi lại
cạnh Kruskal vừa làm hai đỉnh truy vấn nhập chung thành phần — đó chính
là đáp án. Bài 7.4 hiện thực hóa ý này.

### When the answer is −1

Nếu duyệt hết m cạnh mà chưa nhận đủ n−1: đồ thị KHÔNG liên thông —
in −1 (hoặc báo vô nghiệm theo đề). Kiểm tra này rẻ nhưng dễ quên.

**Điểm mấu chốt:** sort tăng + unite được thì nhận, trùng tập thì bỏ;
đủ n−1 cạnh = MST; hết cạnh chưa đủ = −1.""",
    "Kruskal — Tham lam trên cạnh đã sắp",
    "Sắp cạnh tăng dần, hợp tham lam, bỏ cạnh trong cùng thành phần: tính chất chu trình, bottleneck, và trường hợp −1.",
    """## Thuật toán

Cây khung nhỏ nhất: chọn n−1 cạnh tổng nhỏ nhất giữ liên thông. Kruskal:

1. Sắp mọi cạnh theo trọng số TĂNG DẦN.
2. Duyệt lần lượt: cạnh (u, v, w) — nếu find(u) ≠ find(v), unite và
   NHẬN cạnh; ngược lại BỎ (tạo chu trình).
3. Dừng sau n−1 cạnh nhận.

Độ phức tạp: O(m log m) cho sort — DSU chỉ O(m α(n)).

```cpp
long long kruskal(int n, vector<array<long long,3>>& e) {
    sort(e.begin(), e.end());            // theo w
    long long total = 0; int taken = 0;
    for (auto& [w, u, v] : e) {
        if (unite(u, v)) { total += w; ++taken; }
        if (taken == n - 1) break;
    }
    return taken == n - 1 ? total : -1;  // -1: không liên thông
}
```

### Vì sao tham lam an toàn (tính chất chu trình)

Cạnh nhẹ nhất của MỌI "cắt" luôn thuộc một MST nào đó. Khi Kruskal nhặt
cạnh w nhỏ nhất nối hai thành phần, không cạnh đắt hơn có thể thay nó —
đổi vào chỉ làm tổng tăng. Đây là một trong ít tham lam có CHỨNG MINH
ngắn gọn — nhớ cảm giác: "cạnh nhỏ nhất vượt qua mỗi ranh giới".

### Tính chất bottleneck (dùng lại ở bài 7.4)

Trên đường u→v trong MST, cạnh TỐI ĐA là nhỏ nhất có thể so với mọi
đường khác. Hệ quả: trả lời truy vấn bottleneck bằng cách ghi lại cạnh
Kruskal vừa làm hai đỉnh truy vấn nhập chung thành phần — đó là đáp án.

### Khi đáp án là −1

Duyệt hết m cạnh mà chưa nhận đủ n−1: đồ thị KHÔNG liên thông — in −1.
Kiểm tra này rẻ nhưng dễ quên.

**Điểm mấu chốt:** sort tăng + nhận/bỏ theo tập; đủ n−1 = MST; hết cạnh
chưa đủ = −1.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p7-components",
    "Đếm thành phần động",
    """**Bài toán.** n thành phố, ban đầu không có đường nào. Đến lần lượt
m đường (u, v). Sau MỖI đường, in số vùng liên thông hiện tại.

**Ràng buộc:** 1 ≤ n, m ≤ 200 000; 1 ≤ u, v ≤ n (có thể u = v hoặc
đường trùng).""",
    [
        contest_test(
            "ví dụ",
            T("5 4", "1 2", "3 4", "2 4", "5 1"),
            T("4", "3", "2", "1"),
            "5 vùng → nối 1-2 còn 4 → 3-4 còn 3 → 2-4 gộp hai vùng còn 2 → 5-1 còn 1.",
        ),
        contest_test(
            "đường trùng không đổi số",
            T("3 4", "1 2", "1 2", "2 1", "1 3"),
            T("2", "2", "2", "1"),
            "Ba đường đầu đều nối 1-2: chỉ lần ĐẦU giảm số vùng — hai lần sau là nhánh unite trả FALSE.",
        ),
        contest_test(
            "khuyên tự thân",
            T("2 2", "1 1", "1 2"),
            T("2", "1"),
            "Đường u = v không gộp gì — số vùng chỉ giảm ở đường thứ hai.",
        ),
        contest_test(
            "n lớn — một ngôi sao và đường trùng",
            T("200000 200000")
            + T(*["1 " + str(j + 2) for j in range(100000)])
            + T(*["1 2"] * 100000),
            T(*[str(199999 - j) for j in range(100000)] + ["100000"] * 100000),
            "100000 đường (1, j+2) mới mỗi lần: 199999 giảm dần về 100000; sau đó 100000 đường trùng (1,2) giữ nguyên — mỗi thao tác O(α(n)).",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p7-mst-kruskal",
    "Tổng cây khung nhỏ nhất",
    """**Bài toán.** Đồ thị vô hướng n đỉnh, m cạnh (u, v, w). In tổng trọng
số cây khung nhỏ nhất. Đồ thị đảm bảo liên thông.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ w ≤ 10^9.

Tổng có thể tới ~10^14 — long long.""",
    [
        contest_test(
            "ví dụ",
            T("4 5", "1 2 1", "2 3 2", "3 4 3", "1 3 10", "2 4 10"),
            T("6"),
            "Kruskal nhận 1, 2, 3 rồi dừng — hai cạnh 10 tạo chu trình với cây đã có.",
        ),
        contest_test(
            "cạnh song song chọn rẻ",
            T("2 2", "1 2 5", "1 2 3"),
            T("3"),
            "Hai cạnh song song: Kruskal sắp tăng nên cạnh 3 được nhận trước, cạnh 5 thành chu trình bị bỏ.",
        ),
        contest_test(
            "tam giác đường vòng đắt",
            T("3 3", "1 2 1", "2 3 2", "1 3 100"),
            T("3"),
            "Cạnh 100 không bao giờ vào cây — hai cạnh rẻ hơn đã nối cả ba đỉnh.",
        ),
        contest_test(
            "n lớn — chuỗi + 500 cạnh trùng rẻ",
            T("100000 100499")
            + T(*["1 2 1"] * 500)
            + T(*[str(i) + " " + str(i + 1) + " " + str(i + 7) for i in range(1, 100000)]),
            T("5000649986"),
            "MST = cạnh trùng (1,2,1) + chuỗi i+7 với i = 2..99999 = 1 + 5000649985. Cộng cạnh rẻ của chu trình — Kruskal tự xử lý.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p7-redundant",
    "Cạnh thừa",
    """**Bài toán.** Đồ thị vô hướng n đỉnh; đến lần lượt m cạnh (u, v).
Với mỗi cạnh in YES nếu hai đầu MÃI liên thông với nhau trước khi thêm
(cạnh này thừa), ngược lại in NO.

**Ràng buộc:** 1 ≤ n, m ≤ 200 000; 1 ≤ u, v ≤ n (u = v được — luôn YES).""",
    [
        contest_test(
            "ví dụ",
            T("4 5", "1 2", "2 3", "3 4", "1 4", "2 4"),
            T("NO", "NO", "NO", "YES", "YES"),
            "Ba cạnh đầu mở rộng vùng; 1-4 và 2-4 nối hai đỉnh đã cùng vùng {1,2,3,4}.",
        ),
        contest_test(
            "khuyên tự thân",
            T("2 2", "1 1", "2 1"),
            T("YES", "NO"),
            "u = v: hai đầu của đường là MỘT đỉnh — luôn YES; đường 2-1 thật sự nối hai vùng.",
        ),
        contest_test(
            "tam giác cạnh khép",
            T("3 3", "1 2", "2 3", "3 1"),
            T("NO", "NO", "YES"),
            "Cạnh 3-1 khép tam giác: 3 và 1 đã liên thông qua 2.",
        ),
        contest_test(
            "n lớn — chuỗi dài rồi khép",
            T("200000 200000")
            + T(*[str(i) + " " + str(i + 1) for i in range(1, 200000)])
            + T("1 200000"),
            T(*["NO"] * 199999 + ["YES"]),
            "199999 cạnh chuỗi đều mở rộng; cạnh cuối (1, 200000) nối hai đầu đã cùng vùng.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p7-bottleneck",
    "Cạnh tối đa nhỏ nhất trên đường",
    """**Bài toán.** Đồ thị vô hướng LIÊN THÔNG n đỉnh, m cạnh (u, v, w).
q truy vấn (u, v): trên mọi đường đi từ u đến v, xét cạnh có trọng số
TỐI ĐA trên đường đó — in giá trị nhỏ nhất có thể đạt được.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m, q ≤ 200 000; 1 ≤ w ≤ 10^9.

Đây là truy vấn bottleneck của tính chất Kruskal (bài 7.2): đáp án là
cạnh đang xét khi hai đỉnh truy vấn lần ĐẦU nhập chung thành phần.""",
    [
        contest_test(
            "ví dụ",
            T("3 3 1", "2 3 3", "1 2 5", "1 3 10", "1 3"),
            T("5"),
            "Đường 1-2-3: max(5,3) = 5; đường trực tiếp 1-3: 10 → đáp án 5.",
        ),
        contest_test(
            "cạnh song song",
            T("2 2 1", "1 2 7", "1 2 4", "1 2"),
            T("4"),
            "Hai hành lang trực tiếp: chọn cạnh rẻ hơn.",
        ),
        contest_test(
            "hai hành lang",
            T("4 4 1", "1 2 1", "2 4 9", "1 3 2", "3 4 3", "1 4"),
            T("3"),
            "1-2-4: max = 9; 1-3-4: max(2,3) = 3 → đáp án 3.",
        ),
        contest_test(
            "n lớn — chuỗi tăng dần, hai truy vấn",
            T("100000 99999 2")
            + T(*[str(i) + " " + str(i + 1) + " " + str(i) for i in range(1, 100000)])
            + T("1 100000", "1 2"),
            T("99999", "1"),
            "Chuỗi trọng số 1..99999: đường duy nhất từ 1 đến 100000 có max = 99999; truy vấn (1,2) là một cạnh trọng số 1.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p7-same-set",
    "Cùng nhóm?",
    """**Bài toán.** n người; q thao tác:
- `1 u v` — u và v trở thành cùng nhóm (hợp);
- `2 u v` — in YES nếu u, v cùng nhóm, NO nếu khác.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; 1 ≤ u, v ≤ n.""",
    [
        contest_test(
            "ví dụ",
            T("5 6", "1 1 2", "2 1 2", "2 2 3", "1 3 5", "2 3 5", "2 1 5"),
            T("YES", "NO", "YES", "NO"),
            "Hợp 1-2 → YES; 2 với 3 khác nhóm; hợp 3-5 → YES; 1 với 5 vẫn khác.",
        ),
        contest_test(
            "cùng tập nhưng cha khác",
            T("4 6", "1 1 2", "1 3 4", "1 2 4", "2 3 4", "2 4 3", "2 1 4"),
            T("YES", "YES", "YES"),
            "Sau hợp 2-4, tập {1,2,3,4} — cặp (3,4) cùng nhóm dù cha TRỰC TIẾP khác nhau: phải dùng find, không so par[u] == par[v].",
        ),
        contest_test(
            "hợp rồi hỏi chéo",
            T("6 6", "1 1 2", "1 4 5", "1 2 4", "2 1 5", "2 1 6", "2 3 6"),
            T("YES", "NO", "NO"),
            "{1,2,4,5} một nhóm; 6 và 3 đứng ngoài.",
        ),
        contest_test(
            "n lớn — sao rồi hỏi",
            T("100000 199999")
            + T(*["1 1 " + str(j + 2) for j in range(99999)])
            + T(*["2 1 " + str(j + 2) for j in range(99999)])
            + T("2 1 1"),
            T(*["YES"] * 99999 + ["YES"]),
            "99999 hợp tạo sao quanh 1 rồi 99999 hỏi đều YES; truy vấn cuối (1,1) — cùng chính nó.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

VI7 = {
    "hsgi-p7-components": vi_challenge(
        "Đếm thành phần động",
        """**Bài toán.** n thành phố; đến lần lượt m đường (u, v). Sau mỗi
đường in số vùng liên thông. Đường trùng / u = v không đổi số.""",
        [("ví dụ", "4, 3, 2, 1."),
         ("n lớn", "Mỗi thao tác O(α(n)) — DSU + bộ đếm.")],
    ),
    "hsgi-p7-mst-kruskal": vi_challenge(
        "Tổng cây khung nhỏ nhất",
        """**Bài toán.** Đồ thị vô hướng liên thông; in tổng trọng số MST.
Kruskal: sort tăng + DSU.""",
        [("ví dụ", "Nhận 1+2+3, bỏ hai cạnh 10."),
         ("n lớn", "long long — tổng tới 10^14.")],
    ),
    "hsgi-p7-redundant": vi_challenge(
        "Cạnh thừa",
        """**Bài toán.** Mỗi cạnh đến lần lượt: YES nếu hai đầu đã liên thông
trước khi thêm, NO nếu ngược. u = v → YES.""",
        [("ví dụ", "NO, NO, NO, YES, YES."),
         ("n lớn", "find(u) == find(v) kiểm tra O(α(n)).")],
    ),
    "hsgi-p7-bottleneck": vi_challenge(
        "Cạnh tối đa nhỏ nhất trên đường",
        """**Bài toán.** Đồ thị liên thông; mỗi truy vấn (u, v) in giá trị nhỏ
nhất có thể của cạnh tối đa trên đường u→v.""",
        [("ví dụ", "1-2-3: max 5 < 10 → 5."),
         ("n lớn", "Offline: ghi lại cạnh Kruskal gộp cặp truy vấn (small-to-large).")],
    ),
    "hsgi-p7-same-set": vi_challenge(
        "Cùng nhóm?",
        """**Bài toán.** `1 u v` hợp nhóm; `2 u v` in YES/NO cùng nhóm.
So sánh qua find — KHÔNG so cha trực tiếp.""",
        [("ví dụ", "YES, NO, YES, NO."),
         ("cùng tập cha khác", "par[u] == par[v] sai — phải find.")],
    ),
}

write_practice(
    M,
    "hsgi-p7-dsu",
    "DSU & MST Problem Set",
    "Five problems: dynamic component counting, MST total, redundant edges, bottleneck queries, and same-set checks.",
    "Bài tập DSU & MST",
    "Năm bài: đếm thành phần động, tổng MST, cạnh thừa, truy vấn bottleneck, và kiểm tra cùng nhóm.",
    "hsgi-m7-mst",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI7,
    solutions=[
        (
            "hsgi-p7-components",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    int comps = n;
    while (m--) {
        int u, v; in >> u >> v;
        u = find(u); v = find(v);
        if (u != v) {
            if (sz_[u] < sz_[v]) swap(u, v);
            par[v] = u; sz_[u] += sz_[v];
            --comps;
        }
        out << comps << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    // near-miss: giảm bộ đếm MỌI lần gọi, kể cả khi u, v đã cùng vùng —
    // quên nhánh unite trả FALSE của bài 7.1
    int comps = n;
    while (m--) {
        int u, v; in >> u >> v;
        u = find(u); v = find(v);
        if (sz_[u] < sz_[v]) swap(u, v);
        par[v] = u; sz_[u] += sz_[v];
        --comps;
        out << comps << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p7-mst-kruskal",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<array<long long,3>> e(m);
    for (auto& [w, u, v] : e) in >> u >> v >> w;
    sort(e.begin(), e.end());
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    long long total = 0; int taken = 0;
    for (auto& [w, u, v] : e) {
        int a = find(u), b = find(v);
        if (a != b) {
            if (sz_[a] < sz_[b]) swap(a, b);
            par[b] = a; sz_[a] += sz_[b];
            total += w; ++taken;
            if (taken == n - 1) break;
        }
    }
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<array<long long,3>> e(m);
    for (auto& [w, u, v] : e) in >> u >> v >> w;
    sort(e.begin(), e.end());
    // near-miss: cộng (n−1) cạnh RẺ NHẤT bất kể chúng có nối mọi đỉnh hay
    // không — các cạnh rẻ trong chu trình bị đếm nhiều lần, cạnh đắt bắt
    // buộc bị bỏ sót
    long long total = 0;
    for (int i = 0; i < n - 1 && i < m; ++i) total += e[i][0];
    out << total << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p7-redundant",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    while (m--) {
        int u, v; in >> u >> v;
        int a = find(u), b = find(v);
        if (a == b) out << "YES" << "{{NL}}";
        else {
            if (sz_[a] < sz_[b]) swap(a, b);
            par[b] = a; sz_[a] += sz_[b];
            out << "NO" << "{{NL}}";
        }
    }
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    // near-miss: đoán chu trình bằng KỀ trực tiếp — in YES nếu u, v đã là
    // hàng xóm của nhau; bỏ sót mọi chu trình qua đỉnh trung gian
    while (m--) {
        int u, v; in >> u >> v;
        bool dup = false;
        for (int x : adj[u]) if (x == v) { dup = true; break; }
        out << (dup ? "YES" : "NO") << "{{NL}}";
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
""") + END,
        ),
        (
            "hsgi-p7-bottleneck",
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<array<long long,3>> e(m);
    for (auto& [w, u, v] : e) in >> u >> v >> w;
    sort(e.begin(), e.end());
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    vector<long long> ans(q, -1);
    vector<vector<pair<int,int>>> pend(n + 1);   // gốc -> (đầu kia, chỉ số truy vấn)
    for (int j = 0; j < q; ++j) {
        int u, v; in >> u >> v;
        if (u == v) ans[j] = 0;
        else { pend[u].push_back({v, j}); pend[v].push_back({u, j}); }
    }
    for (auto& [w, u, v] : e) {
        int a = find(u), b = find(v);
        if (a == b) continue;
        if (sz_[a] < sz_[b]) { swap(a, b); }
        par[b] = a; sz_[a] += sz_[b];
        if (pend[b].size() > pend[a].size()) swap(pend[a], pend[b]);
        vector<pair<int,int>> keep;
        for (auto& [v2, j] : pend[b]) {
            if (find(v2) == a) ans[j] = w;       // lần đầu nhập chung — chính là bottleneck
            else keep.push_back({v2, j});
        }
        for (auto& p : keep) pend[a].push_back(p);
        pend[b].clear();
    }
    for (int j = 0; j < q; ++j) out << ans[j] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<array<long long,3>> e(m);
    for (auto& [w, u, v] : e) in >> u >> v >> w;
    // near-miss: sort GIẢM dần và lấy cạnh đầu tiên khiến u, v liên thông —
    // tính nhầm "bottleneck LỚN nhất" thay vì nhỏ nhất
    sort(e.rbegin(), e.rend());
    while (q--) {
        int u, v; in >> u >> v;
        vector<int> par(n + 1);
        for (int i = 1; i <= n; ++i) par[i] = i;
        auto find = [&](int x) {
            while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
            return x;
        };
        long long res = -1;
        for (auto& [w, a, b] : e) {
            int ra = find(a), rb = find(b);
            if (ra != rb) par[rb] = ra;
            if (find(u) == find(v)) { res = w; break; }
        }
        out << res << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p7-same-set",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    while (q--) {
        int tp, u, v; in >> tp >> u >> v;
        if (tp == 1) {
            int a = find(u), b = find(v);
            if (a != b) {
                if (sz_[a] < sz_[b]) swap(a, b);
                par[b] = a; sz_[a] += sz_[b];
            }
        } else {
            out << (find(u) == find(v) ? "YES" : "NO") << "{{NL}}";
        }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    // near-miss: so CHA TRỰC TIẾP thay vì find — hai đỉnh cùng tập vẫn
    // NO khi cha trực tiếp khác nhau (union by size để cây không sao chép)
    while (q--) {
        int tp, u, v; in >> tp >> u >> v;
        if (tp == 1) {
            int a = find(u), b = find(v);
            if (a != b) {
                if (sz_[a] < sz_[b]) swap(a, b);
                par[b] = a; sz_[a] += sz_[b];
            }
        } else {
            out << (par[u] == par[v] ? "YES" : "NO") << "{{NL}}";
        }
    }
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH7 = challenge(
    "hsgi-cp-m7-rescue",
    "Checkpoint — Trạm cứu hộ",
    """**Bài toán.** Tỉnh có n trạm y tế và m tuyến đường hai chiều (u, v,
w) với chi phí duy trì w. Chọn một tập tuyến đường giữ MỌI trạm liên
thông với chi phí duy trì TỔNG nhỏ nhất — in tổng đó. Nếu không thể
nối tất cả, in −1.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ w ≤ 10^9.

Tổng tới ~10^14 — long long.""",
    [
        contest_test(
            "ví dụ",
            T("3 3", "1 2 4", "2 3 6", "1 3 8"),
            T("10"),
            "Cây khung: 4 + 6 = 10; cạnh 8 thành chu trình bị bỏ.",
        ),
        contest_test(
            "không thể nối — in −1",
            T("4 2", "1 2 1", "3 4 1"),
            T("-1"),
            "Hai vùng {1,2} và {3,4} không có tuyến nào nối — −1.",
        ),
        contest_test(
            "cạnh rẻ gộp chu kỳ",
            T("4 4", "1 2 1", "2 3 1", "3 1 1", "3 4 50"),
            T("52"),
            "Chu trình ba cạnh 1: chỉ nhận HAI; trạm 4 phải qua cạnh 50 → 1+1+50.",
        ),
        contest_test(
            "n lớn — chuỗi + cạnh trùng rẻ",
            T("100000 100499")
            + T(*["1 2 1"] * 500)
            + T(*[str(i) + " " + str(i + 1) + " " + str(i + 7) for i in range(1, 100000)]),
            T("5000649986"),
            "MST = 1 (một bản của cạnh trùng) + chuỗi i+7 với i = 2..99999.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP7 = vi_challenge(
    "Checkpoint — Trạm cứu hộ",
    """**Bài toán.** n trạm, m tuyến (u, v, w). Chọn tập tuyến giữ mọi trạm
liên thông với tổng w nhỏ nhất; không thể thì in −1.""",
    [("ví dụ", "4 + 6 = 10."),
     ("không nối được", "−1."),
     ("n lớn", "Kruskal + DSU, long long.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m7",
    "Checkpoint — DSU & MST",
    "Pass the graded problem to finish the DSU & MST module.",
    25,
    """**Checkpoint — DSU & MST.** Pass the graded challenge below to
complete the module. It is Kruskal end-to-end: sort edges, unite with
DSU, count accepted edges — accept exactly n−1 for a spanning tree,
print −1 if the graph never connects. The counter (taken) is the part
students forget; the sum without it silently prints a wrong total on
disconnected inputs.

**Điểm kiểm tra — DSU & MST.** Pass bài chấm bên dưới để hoàn thành
module. Đây là Kruskal trọn vẹn: sort cạnh, hợp bằng DSU, đếm cạnh đã
nhận — đủ n−1 là cây khung, không đủ là −1. Bộ đếm (taken) là phần dễ
quên nhất; thiếu nó bài vẫn in tổng nhưng SAI trên đồ thị rời rạc.""",
    "Checkpoint — DSU & MST",
    "Pass bài chấm để hoàn thành module DSU & MST.",
    """**Điểm kiểm tra — DSU & MST.** Pass bài chấm bên dưới: Kruskal + DSU,
đủ n−1 cạnh → tổng; hết cạnh chưa đủ → −1.""",
    CH7,
    VI_CP7,
    solution=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<array<long long,3>> e(m);
    for (auto& [w, u, v] : e) in >> u >> v >> w;
    sort(e.begin(), e.end());
    vector<int> par(n + 1), sz_(n + 1, 1);
    for (int i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](int x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    long long total = 0; int taken = 0;
    for (auto& [w, u, v] : e) {
        int a = find(u), b = find(v);
        if (a != b) {
            if (sz_[a] < sz_[b]) swap(a, b);
            par[b] = a; sz_[a] += sz_[b];
            total += w; ++taken;
            if (taken == n - 1) break;
        }
    }
    out << (taken == n - 1 ? total : -1) << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<array<long long,3>> e(m);
    for (auto& [w, u, v] : e) in >> u >> v >> w;
    sort(e.begin(), e.end());
    // near-miss: cộng (n−1) cạnh rẻ nhất mà KHÔNG kiểm tra liên thông —
    // cạnh rẻ trong chu trình bị cộng nhiều lần, cạnh đắt bắt buộc bị bỏ,
    // và đồ thị rời rạc vẫn in ra một tổng vô nghĩa
    long long total = 0;
    for (int i = 0; i < n - 1 && i < m; ++i) total += e[i][0];
    out << total << "{{NL}}";
""") + END,
)
