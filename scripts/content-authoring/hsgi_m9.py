#!/usr/bin/env python3
"""HSG Intermediate — Module 9: hsgi-topo (DAG & Topological Sort).

Kahn's algorithm with in-degrees, the cycle verdict, min-heap lexicographic
order, longest chain on a DAG, critical-path scheduling, and path counting.
Graded checkpoint: course prerequisites.

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
#include <queue>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-topo"
write_module(
    M,
    "DAGs & Topological Order — When Precedence Rules",
    "Kahn's in-degree queue, the cycle verdict (count short of n), lexicographic order via min-heap, longest chains, critical paths, and path counting on DAGs.",
    "DAG & Thứ tự topo — Khi thứ tự ưu tiên cai trị",
    "Hàng đợi in-degree của Kahn, phán quyết chu trình, thứ tự từ điển qua min-heap, chuỗi dài nhất, đường tới hạn, và đếm đường đi trên DAG.",
    ["hsgi-m9-kahn", "hsgi-m9-longest", "hsgi-cp-m9"],
    ["hsgi-p9-topo"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m9-kahn",
    "Kahn's Algorithm — In-Degree Zero First",
    "Peel nodes with no remaining prerequisites, decrement as you go, count what you peeled: fewer than n means a cycle.",
    18,
    """## The problem

n công việc, m ràng buộc "u phải trước v". In MỘT thứ tự hợp lệ — hoặc
báo IMPOSSIBLE khi ràng buộc xoay vòng. Đây là thứ tự topo (topological
order) trên đồ thị CÓ HƯỚNG KHÔNG CHU TRÌNH (DAG).

### Kahn's algorithm

Đỉnh in-degree 0 là đỉnh không phụ thuộc ai — lấy trước. Lấy ra, trừ
in-degree của mọi đỉnh nó trỏ tới; về 0 thì vào hàng đợi.

```cpp
int n, m;
vector<vector<int>> adj;          // u -> v
vector<int> deg;                  // in-degree

vector<int> topo() {
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<int> order;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--deg[v] == 0) bq.push(v);
    }
    // ít hơn n đỉnh: chu trình chặn các đỉnh còn lại
    return order;                 // size() < n ⇒ IMPOSSIBLE
}
```

### The cycle verdict

order.size() < n: các đỉnh còn lại nằm trên (hoặc sau) chu trình —
in-degree không bao giờ về 0. In −1. Đây là bài kiểm tra chu trình
CÓ HƯỚNG rẻ nhất (O(n + m)) — khác với chu trình vô hướng của Beginner.

### Tie-breaking (đề hay đòi)

"Thứ tự nhỏ nhất theo từ điển": thay queue bằng min-heap, mỗi bước lấy
đỉnh NHỎ NHẤT trong số in-degree 0. O((n + m) log n).

### Two classic bugs

1. Quên ++deg[v] cho cạnh — mọi đỉnh trông tự do, thứ tự sai ngay.
2. Kiểm tra deg[v] == 0 TRƯỚC khi trừ — mất đỉnh. Luôn trừ rồi kiểm.

**Điểm mấu chốt:** in-degree 0 vào hàng; lấy ra → trừ con; thiếu n =
chu trình.""",
    "Thuật toán Kahn — In-degree 0 trước",
    "Bóc đỉnh không còn phụ thuộc, trừ dần khi đi, đếm: ít hơn n nghĩa là có chu trình.",
    """## Vấn đề

n công việc, m ràng buộc "u trước v". In MỘT thứ tự hợp lệ — hoặc
IMPOSSIBLE khi xoay vòng. Thứ tự topo trên DAG.

### Thuật toán Kahn

Đỉnh in-degree 0 không phụ thuộc ai — lấy trước. Lấy ra, trừ in-degree
của mọi đỉnh nó trỏ tới; về 0 thì vào hàng đợi.

```cpp
int n, m;
vector<vector<int>> adj;          // u -> v
vector<int> deg;                  // in-degree

vector<int> topo() {
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<int> order;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--deg[v] == 0) bq.push(v);
    }
    return order;                 // size() < n ⇒ IMPOSSIBLE
}
```

### Phán quyết chu trình

order.size() < n: đỉnh còn lại nằm trên (hoặc sau) chu trình — in −1.
Bài kiểm tra chu trình CÓ HƯỚNG rẻ nhất (O(n + m)).

### Tie-breaking (đề hay đòi)

"Thứ tự nhỏ nhất theo từ điển": queue → min-heap, mỗi bước lấy đỉnh
NHỎ NHẤT trong số in-degree 0. O((n + m) log n).

### Hai lỗi kinh điển

1. Quên ++deg[v] — mọi đỉnh trông tự do, thứ tự sai ngay.
2. Kiểm deg[v] == 0 TRƯỚC khi trừ — mất đỉnh. Luôn trừ rồi kiểm.

**Điểm mấu chốt:** in-degree 0 vào hàng; lấy ra → trừ con; thiếu n =
chu trình.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m9-longest",
    "Longest Path on a DAG — The First Graph DP",
    "Process vertices in topo order and relax each edge exactly once: O(n + m) — the pattern behind scheduling and counting.",
    18,
    """## Why the DAG matters

Đường dài nhất trên đồ thị tổng quát là NP-khó (chu trình dương cho đi
vòng mãi). Trên DAG không đi lại được — topo order cho phép MỘT lượt:

```cpp
vector<long long> dp(n + 1, 0);   // dp[u] = đường dài nhất KẾT THÚC tại u
for (int u : order)               // thứ tự topo
    for (int v : adj[u])
        dp[v] = max(dp[v], dp[u] + 1);   // +w nếu có trọng số
```

Mỗi cạnh nới lỏng ĐÚNG MỘT LẦN, khi đầu nó đã chốt — O(n + m). Trả lời
max(dp) cho toàn đồ thị; dp[v] cho đường kết thúc tại v.

### Two directions, one trick

- Kết thúc TẠI u: duyệt theo topo, relax cạnh ra.
- Bắt đầu TẠI u: duyệt NGƯỢC topo, hoặc đảo đồ thị rồi làm như trên.

### The family

Cùng khung, đổi phép hợp:
- số đường đi từ 1 đến n: ways[v] += ways[u] trên cạnh vào;
- critical path: fin[v] = max(fin[u] + t_v);
- số đỉnh tối đa trên đường: dp[v] = max(dp[u]) + 1.

Nhận diện: "thứ tự công việc + tối ưu trên chuỗi phụ thuộc" → DAG DP.
Đồ thị CÓ chu trình mà hỏi đường dài nhất: vô hạn — hoặc bạn đọc thiếu
ràng buộc.

### Sanity drill

Chuỗi 1→2→...→n: topo duy nhất, đường dài nhất có n−1 cạnh. Không có
cạnh: mọi dp = 0. Chu trình: order thiếu đỉnh — IMPOSSIBLE, đừng dùng
dp của chúng.

**Điểm mấu chốt:** topo order = mỗi cạnh tính một lần; một lượt quét.""",
    "Đường dài nhất trên DAG — DP trên đồ thị đầu tiên",
    "Xử lý đỉnh theo topo order, nới lỏng mỗi cạnh đúng một lần: O(n + m).",
    """## Vì sao DAG quan trọng

Đường dài nhất trên đồ thị tổng quát là NP-khó. Trên DAG không đi lại
được — topo order cho phép MỘT lượt:

```cpp
vector<long long> dp(n + 1, 0);   // dp[u] = đường dài nhất KẾT THÚC tại u
for (int u : order)               // thứ tự topo
    for (int v : adj[u])
        dp[v] = max(dp[v], dp[u] + 1);   // +w nếu có trọng số
```

Mỗi cạnh nới lỏng ĐÚNG MỘT LẦN, khi đầu đã chốt — O(n + m). max(dp)
cho toàn đồ thị; dp[v] cho đường kết thúc tại v.

### Hai chiều, một mẹo

- Kết thúc TẠI u: duyệt topo, relax cạnh ra.
- Bắt đầu TẠI u: duyệt ngược topo, hoặc đảo đồ thị.

### Gia đình bài toán

Cùng khung, đổi phép hợp:
- số đường đi 1→n: ways[v] += ways[u];
- critical path: fin[v] = max(fin[u] + t_v);
- số đỉnh tối đa: dp[v] = max(dp[u]) + 1.

Nhận diện: "thứ tự + tối ưu trên chuỗi phụ thuộc" → DAG DP. Có chu
trình mà hỏi đường dài nhất: vô hạn — đọc lại ràng buộc.

### Drill kiểm tra

Chuỗi 1..n: topo duy nhất, đường dài nhất n−1 cạnh. Không cạnh: dp = 0.
Chu trình: order thiếu đỉnh — IMPOSSIBLE.

**Điểm mấu chốt:** topo order = mỗi cạnh tính một lần; một lượt quét.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p9-topo-basic",
    "Thứ tự khóa học",
    """**Bài toán.** n môn học, m ràng buộc "phải học u trước v". In thứ tự
học hợp lệ NHỎ NHẤT theo từ điển (nếu nhiều lựa chọn, chọn số hiệu nhỏ
nhất trước); nếu ràng buộc xoay vòng in −1.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ u, v ≤ n (u ≠ v).""",
    [
        contest_test(
            "ví dụ",
            T("4 4", "1 2", "1 3", "2 4", "3 4"),
            T("1 2 3 4"),
            "1 mở khóa 2, 3 — chọn 2 trước theo từ điển; 4 cuối.",
        ),
        contest_test(
            "từ điển buộc đổi nhánh",
            T("3 2", "2 1", "3 1"),
            T("2 3 1"),
            "2 và 3 đều in-degree 0 — nhặt 2 trước; 3 rồi 1.",
        ),
        contest_test(
            "chu trình — −1",
            T("3 3", "1 2", "2 3", "3 1"),
            T("-1"),
            "Ba môn chờ nhau — không môn nào bắt đầu được.",
        ),
        contest_test(
            "n lớn — chuỗi nghịch",
            T("100000 99999")
            + T(*[str(i + 1) + " " + str(i) for i in range(1, 100000)]),
            T(" ".join(str(i) for i in range(100000, 0, -1))),
            "Chuỗi 100000→99999→...→1: topo duy nhất GIẢM dần, in MỘT DÒNG cách nhau dấu cách — min-heap trả đúng nhưng chỉ một lựa chọn mỗi bước.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p9-cycle",
    "Đồ thị có vòng?",
    """**Bài toán.** Đồ thị CÓ HƯỚNG n đỉnh, m cạnh. In YES nếu có chu trình,
NO nếu là DAG.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ u, v ≤ n (u = v
được — khuyên tự thân là chu trình).""",
    [
        contest_test(
            "ví dụ DAG",
            T("4 4", "1 2", "1 3", "2 4", "3 4"),
            T("NO"),
            "Bốn cạnh trỏ xuôi — topo đủ n đỉnh.",
        ),
        contest_test(
            "chu trình ba đỉnh",
            T("3 3", "1 2", "2 3", "3 1"),
            T("YES"),
            "1→2→3→1 — không đỉnh nào in-degree 0.",
        ),
        contest_test(
            "khuyên tự thân",
            T("2 1", "1 1"),
            T("YES"),
            "u = v: cạnh tự khuyên — deg[1] không bao giờ về 0.",
        ),
        contest_test(
            "n lớn — ngôi sao ngược",
            T("100000 99999")
            + T(*[str(j + 2) + " 1" for j in range(99999)]),
            T("NO"),
            "Mọi đỉnh trỏ về 1 — các đỉnh lá in-degree 0, topo đủ n → DAG.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p9-longest",
    "Chuỗi nhiệm vụ dài nhất",
    """**Bài toán.** n nhiệm vụ, m ràng buộc một chiều "u trước v". In số
nhiệm vụ NHIỀU NHẤT trên một chuỗi thực hiện được. Đồ thị đảm bảo DAG.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ u, v ≤ n.""",
    [
        contest_test(
            "ví dụ",
            T("4 4", "1 2", "1 3", "2 4", "3 4"),
            T("3"),
            "1→2→4 hoặc 1→3→4: 3 nhiệm vụ.",
        ),
        contest_test(
            "không ràng buộc",
            T("5 0"),
            T("1"),
            "Không cạnh: chuỗi dài nhất là một nhiệm vụ bất kỳ.",
        ),
        contest_test(
            "tuyến dài nhánh ngắn",
            T("5 4", "1 2", "2 3", "3 5", "4 5"),
            T("4"),
            "1→2→3→5: 4 nhiệm vụ; nhánh 4→5 chỉ 2.",
        ),
        contest_test(
            "đỉnh sau trong danh sách — bẫy thứ tự đọc",
            T("4 3", "4 2", "2 3", "3 1"),
            T("4"),
            "Cạnh 4→2 xuất hiện TRƯỚC cạnh 2→3: tính dp theo thứ tự đọc sẽ chốt dp[3] trước khi đường 4→2→3 kịp chảy — topo order buộc 4 trước 2 trước 3.",
        ),
        contest_test(
            "n lớn — chuỗi + đỉnh rời",
            T("100000 99998")
            + T(*[str(i) + " " + str(i + 1) for i in range(1, 99999)]),
            T("99999"),
            "Chuỗi 1..99999 cho đường 99999 đỉnh; đỉnh 100000 rời rạc — max dp + 1.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p9-critical",
    "Lịch thi công — đường tới hạn",
    """**Bài toán.** Dự án có n công đoạn; công đoạn i mất t_i ngày; m ràng
buộc "công đoạn u phải XONG trước khi v BẮT ĐẦU". Công đoạn có thể chạy
song song nếu không ràng buộc cấm. In số ngày SỚM NHẤT hoàn thành toàn
bộ dự án. Đồ thị đảm bảo DAG.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ t_i ≤ 10^9;
1 ≤ u, v ≤ n.

Critical path: fin[v] = max(fin[u]) + t_v theo topo order.""",
    [
        contest_test(
            "ví dụ",
            T("4 3", "2 2 4 3", "1 2", "1 3", "1 4"),
            T("6"),
            "fin[1] = 2; 2, 3, 4 chỉ phụ thuộc 1: fin[2] = 4, fin[3] = 6, fin[4] = 5 — dự án xong khi công đoạn muộn nhất xong: max = 6.",
        ),
        contest_test(
            "không ràng buộc — chạy song song",
            T("3 0", "5 7 2"),
            T("7"),
            "Ba công đoạn độc lập: dự án xong khi đoạn dài nhất xong.",
        ),
        contest_test(
            "chuỗi cộng dồn",
            T("3 2", "4 5 6", "1 2", "2 3"),
            T("15"),
            "4 + 5 + 6 nối tiếp — tổng toàn chuỗi.",
        ),
        contest_test(
            "hai nhánh song song hội tụ",
            T("5 4", "3 1 1 5 1", "1 2", "2 5", "3 4", "4 5"),
            T("7"),
            "fin[1] = 3, fin[2] = 4, fin[3] = 1, fin[4] = 6, fin[5] = max(fin[2], fin[4]) + t5 = max(4, 6) + 1 = 7 — dự án xong khi công đoạn muộn nhất xong.",
        ),
        contest_test(
            "n lớn — chuỗi + đoạn nặng cuối",
            T("100000 99999")
            + T(" ".join(["1"] * 99999 + ["1000000000"]))
            + T(*[str(i) + " " + str(i + 1) for i in range(1, 100000)]),
            T("1000099999"),
            "99999 đoạn đầu ×1 nối tiếp, đoạn cuối 10^9: fin[100000] = 99999 + 10^9 = 1000099999 — long long, một lượt topo.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p9-ways",
    "Số đường đi trên DAG",
    """**Bài toán.** Đồ thị CÓ HƯỚNG không chu trình (DAG) n đỉnh, m cạnh.
Đếm số đường đi phân biệt từ 1 đến n, theo modulo 10^9 + 7.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ u, v ≤ n.""",
    [
        contest_test(
            "ví dụ",
            T("4 4", "1 2", "1 3", "2 4", "3 4"),
            T("2"),
            "1→2→4 và 1→3→4: 2 đường; không có cạnh 1→4 trực tiếp.",
        ),
        contest_test(
            "kim cương + đường trực tiếp",
            T("4 5", "1 2", "1 3", "2 4", "3 4", "1 4"),
            T("3"),
            "Qua 2, qua 3, trực tiếp: 3 đường.",
        ),
        contest_test(
            "không đường tới đích",
            T("3 1", "1 2"),
            T("0"),
            "Đỉnh 3 không nối — 0 đường.",
        ),
        contest_test(
            "chuỗi dài — đếm 1",
            T("100000 99999")
            + T(*[str(i) + " " + str(i + 1) for i in range(1, 100000)]),
            T("1"),
            "Chuỗi duy nhất: chỉ một đường 1→n.",
        ),
        contest_test(
            "n lớn — thang kim cương 30 tầng",
            T("91 120")
            + T(*[f"{3 * i - 2} {3 * i - 1} {3 * i - 2} {3 * i} {3 * i - 1} {3 * i + 1} {3 * i} {3 * i + 1}" for i in range(1, 31)]),
            T("73741817"),
            "30 tầng kim cương nối tiếp: mỗi tầng nhân đôi số đường — 2^30 = 1073741824 ≡ 73741817 (mod 10^9 + 7). Mỗi cạnh cộng đúng một lần theo topo.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI9 = {
    "hsgi-p9-topo-basic": vi_challenge(
        "Thứ tự khóa học",
        """**Bài toán.** n môn, m ràng buộc "u trước v". In thứ tự học nhỏ nhất
theo từ điển; xoay vòng in −1.""",
        [("ví dụ", "1 2 3 4."),
         ("n lớn", "Kahn + min-heap, O((n+m) log n).")],
    ),
    "hsgi-p9-cycle": vi_challenge(
        "Đồ thị có vòng?",
        """**Bài toán.** Đồ thị CÓ HƯỚNG: YES nếu có chu trình, NO nếu DAG.
Khuyên tự thân là chu trình.""",
        [("ví dụ", "NO; chu trình ba đỉnh YES."),
         ("n lớn", "Kahn thiếu n đỉnh = chu trình.")],
    ),
    "hsgi-p9-longest": vi_challenge(
        "Chuỗi nhiệm vụ dài nhất",
        """**Bài toán.** DAG: in số nhiệm vụ nhiều nhất trên một chuỗi hợp lệ.
dp theo topo order — kể cả khi cạnh lùi xuất hiện trước trong input.""",
        [("ví dụ", "3 nhiệm vụ."),
         ("n lớn", "O(n + m).")],
    ),
    "hsgi-p9-critical": vi_challenge(
        "Lịch thi công — đường tới hạn",
        """**Bài toán.** Công đoạn i mất t_i; u phải xong trước khi v bắt đầu;
chạy song song khi được. In ngày sớm nhất xong toàn bộ.""",
        [("không ràng buộc", "max(t_i)."),
         ("n lớn", "fin[v] = max(fin[u]) + t_v.")],
    ),
    "hsgi-p9-ways": vi_challenge(
        "Số đường đi trên DAG",
        """**Bài toán.** Đếm đường đi 1→n trên DAG, modulo 10^9 + 7.""",
        [("ví dụ", "2 đường qua hai nhánh."),
         ("n lớn", "ways[v] += ways[u] theo topo.")],
    ),
}

write_practice(
    M,
    "hsgi-p9-topo",
    "Topo Problem Set",
    "Five problems: lexicographic topological order, directed cycle detection, longest task chain, critical-path scheduling, and path counting on a DAG.",
    "Bài tập topo",
    "Năm bài: thứ tự topo từ điển, phát hiện chu trình có hướng, chuỗi nhiệm vụ dài nhất, lịch thi công tới hạn, và đếm đường đi trên DAG.",
    "hsgi-m9-longest",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI9,
    solutions=[
        (
            "hsgi-p9-topo-basic",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    priority_queue<int, vector<int>, greater<>> pq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) pq.push(i);
    vector<int> order;
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--deg[v] == 0) pq.push(v);
    }
    if ((int)order.size() < n) { out << -1 << "{{NL}}"; return; }
    for (size_t i = 0; i < order.size(); ++i)
        out << order[i] << " \\n"[i + 1 == order.size()];
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        // near-miss: quên ++deg[v] — mọi đỉnh trông tự do, Kahn xả theo
        // thứ tự đọc vào thay vì thứ tự phụ thuộc
    }
    priority_queue<int, vector<int>, greater<>> pq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) pq.push(i);
    vector<int> order;
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--deg[v] == 0) pq.push(v);
    }
    for (size_t i = 0; i < order.size(); ++i)
        out << order[i] << " \\n"[i + 1 == order.size()];
""") + END,
        ),
        (
            "hsgi-p9-cycle",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    int seen = 0;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        ++seen;
        for (int v : adj[u])
            if (--deg[v] == 0) bq.push(v);
    }
    out << (seen == n ? "NO" : "YES") << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    // near-miss: Kahn chạy ĐẦU NGUỒN CHỈ ĐỈNH 1 (bỏ các đỉnh in-degree 0
    // khác) — đỉnh rời rạc được báo là "chu trình" dù chúng chỉ đứng ngoài
    queue<int> bq;
    if (deg[1] == 0) bq.push(1);
    int seen = 0;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        ++seen;
        for (int v : adj[u])
            if (--deg[v] == 0) bq.push(v);
    }
    out << (seen == n ? "NO" : "YES") << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p9-longest",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<int> order;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--deg[v] == 0) bq.push(v);
    }
    vector<int> dp(n + 1, 0);
    int best = 0;
    for (int u : order)
        for (int v : adj[u]) {
            if (dp[u] + 1 > dp[v]) dp[v] = dp[u] + 1;
            if (dp[v] > best) best = dp[v];
        }
    out << best + 1 << "{{NL}}";     // +1: đếm cả đỉnh bắt đầu
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    // near-miss: tính dp theo THỨ TỰ ĐỌC vào thay vì topo order — cạnh
    // lùi xuất hiện trước làm dp[v] chốt sớm, các đường dài hơn tới đầu
    // kia không kịp chảy về
    vector<int> dp(n + 1, 0);
    int best = 0;
    for (int i = 1; i <= n; ++i)
        for (int v : adj[i]) {
            if (dp[i] + 1 > dp[v]) dp[v] = dp[i] + 1;
            if (dp[v] > best) best = dp[v];
        }
    out << best + 1 << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p9-critical",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<long long> t(n + 1);
    for (int i = 1; i <= n; ++i) in >> t[i];
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<long long> fin(n + 1, 0);
    long long ans = 0;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        fin[u] += t[u];               // công đoạn u hoàn tất
        if (fin[u] > ans) ans = fin[u];
        for (int v : adj[u]) {
            if (fin[u] > fin[v]) fin[v] = fin[u];
            if (--deg[v] == 0) bq.push(v);
        }
    }
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<long long> t(n + 1);
    for (int i = 1; i <= n; ++i) in >> t[i];
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    // near-miss: CỘNG thời gian của mọi tiền nhiệm thay vì LẤY MAX —
    // hai nhánh song song bị tính như nối tiếp
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<long long> fin(n + 1, 0);
    long long ans = 0;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        fin[u] += t[u];
        if (fin[u] > ans) ans = fin[u];
        for (int v : adj[u]) {
            fin[v] += fin[u];
            if (--deg[v] == 0) bq.push(v);
        }
    }
    out << ans << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p9-ways",
            CPP_STD + cpp("""    const long long MOD = 1000000007;
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<long long> ways(n + 1, 0);
    ways[1] = 1;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u]) {
            ways[v] = (ways[v] + ways[u]) % MOD;
            if (--deg[v] == 0) bq.push(v);
        }
    }
    out << ways[n] % MOD << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    const long long MOD = 1000000007;
    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    // near-miss: GHI ĐÈ thay vì CỘNG — ways[v] = ways[u] giữ đường CUỐI
    // cùng được duyệt thay vì đếm TẤT CẢ các đường
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<long long> ways(n + 1, 0);
    ways[1] = 1;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u]) {
            ways[v] = ways[u] % MOD;
            if (--deg[v] == 0) bq.push(v);
        }
    }
    out << ways[n] % MOD << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH9 = challenge(
    "hsgi-cp-m9-prereq",
    "Checkpoint — Điều kiện học phần",
    """**Bài toán.** Chương trình có n học phần; m ràng buộc "phải hoàn
thành u trước khi học v". In thứ tự học TỐT NHẤT theo nghĩa: trong các
thứ tự hợp lệ, chọn thứ tự theo TỪ ĐIỂN (số hiệu nhỏ hơn được ưu tiên).
Nếu ràng buộc xoay vòng, in −1.

**Ràng buộc:** 1 ≤ n ≤ 100 000; 1 ≤ m ≤ 200 000; 1 ≤ u, v ≤ n (u ≠ v).""",
    [
        contest_test(
            "ví dụ",
            T("4 4", "1 2", "1 3", "2 4", "3 4"),
            T("1 2 3 4"),
            "1 mở khóa 2 và 3 — chọn 2 trước theo từ điển; 4 cuối cùng.",
        ),
        contest_test(
            "xoay vòng — −1",
            T("3 3", "1 2", "2 3", "3 1"),
            T("-1"),
            "Ba học phần chờ nhau mãi.",
        ),
        contest_test(
            "nhiều nguồn — từ điển quyết",
            T("5 3", "3 1", "5 1", "2 4"),
            T("2 3 4 5 1"),
            "Nguồn {2,3,5}: 2 → mở 4; heap vẫn còn 3 < 4 → 3; 4; 5; cuối là 1.",
        ),
        contest_test(
            "n lớn — chuỗi nghịch",
            T("100000 99999")
            +            T(*[str(i + 1) + " " + str(i) for i in range(1, 100000)]),
            T(" ".join(str(i) for i in range(100000, 0, -1))),
            "Chuỗi 100000→99999→...→1: topo duy nhất giảm dần, một dòng dấu cách — một lượt Kahn.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP9 = vi_challenge(
    "Checkpoint — Điều kiện học phần",
    """**Bài toán.** n học phần, m ràng buộc "u trước v". In thứ tự học theo
từ điển; xoay vòng in −1.""",
    [("ví dụ", "1 2 3 4."),
     ("xoay vòng", "−1."),
     ("n lớn", "Kahn + min-heap.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m9",
    "Checkpoint — DAG & Topo",
    "Pass the graded problem to finish the DAG & topological order module.",
    25,
    """**Checkpoint — DAG & Topo.** Pass the graded challenge below to
complete the module: Kahn's algorithm with a min-heap for the
lexicographic requirement and the count-short-of-n cycle verdict. The
heap swap (queue → min-heap) decides right-vs-wrong here: a plain queue
prints a VALID but not smallest order, which fails every byte-exact
test.

**Điểm kiểm tra — DAG & Topo.** Pass bài chấm bên dưới để hoàn thành
module: Kahn với min-heap cho yêu cầu từ điển và phán quyết chu trình
(đếm thiếu n). Queue thường in thứ tự HỢP LỆ nhưng KHÔNG NHỎ NHẤT —
trượt từng byte trên test chấm.""",
    "Checkpoint — DAG & Topo",
    "Pass bài chấm để hoàn thành module DAG & topo.",
    """**Điểm kiểm tra — DAG & Topo.** Pass bài chấm bên dưới: Kahn +
min-heap (thứ tự từ điển), thiếu n = −1.""",
    CH9,
    VI_CP9,
    solution=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    priority_queue<int, vector<int>, greater<>> pq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) pq.push(i);
    vector<int> order;
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--deg[v] == 0) pq.push(v);
    }
    if ((int)order.size() < n) { out << -1 << "{{NL}}"; return; }
    for (size_t i = 0; i < order.size(); ++i)
        out << order[i] << " \\n"[i + 1 == order.size()];
""") + END,
    wrong=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        ++deg[v];
    }
    // near-miss: queue THƯỜNG thay min-heap — thứ tự vẫn hợp lệ nhưng
    // KHÔNG nhỏ nhất theo từ điển; test chấm từng byte bị trượt
    queue<int> bq;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) bq.push(i);
    vector<int> order;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--deg[v] == 0) bq.push(v);
    }
    if ((int)order.size() < n) { out << -1 << "{{NL}}"; return; }
    for (size_t i = 0; i < order.size(); ++i)
        out << order[i] << " \\n"[i + 1 == order.size()];
""") + END,
)
