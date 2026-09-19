#!/usr/bin/env python3
"""HSG Intermediate — Module 8: hsgi-dijkstra (Shortest Paths).

Dijkstra with a priority_queue, the negative-edge trap, 0-1 BFS with a
deque, unweighted BFS as the |w|=1 special case, and a graded checkpoint
(flight network, Dijkstra or −1 unreachable).

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
#include <deque>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-dijkstra"
write_module(
    M,
    "Shortest Paths — Dijkstra & 0-1 BFS",
    "Dijkstra's greedy expansion over a priority queue, why negative edges break it, the deque-based 0-1 BFS, and where plain BFS is already optimal.",
    "Đường đi ngắn nhất — Dijkstra & 0-1 BFS",
    "Dijkstra mở rộng tham lam qua priority_queue, vì sao cạnh âm phá nó, 0-1 BFS với deque, và khi nào BFS thuần là tối ưu.",
    ["hsgi-m8-dijkstra", "hsgi-m8-zero-one", "hsgi-cp-m8"],
    ["hsgi-p8-paths"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m8-dijkstra",
    "Dijkstra — Greedy Over a Priority Queue",
    "The invariant (every settled vertex is final), the lazy-deletion pattern, and exactly why negative edges violate the proof.",
    20,
    """## The setup

Đồ thị có hướng, trọng số KHÔNG ÂM. Tìm đường ngắn nhất từ s đến mọi
đỉnh. Ý tưởng: giữ khoảng cách hiện tại của từng đỉnh, luôn "khóa" đỉnh
chưa khóa có khoảng cách NHỎ NHẤT — vì mọi đường khác đều đi qua đỉnh
trọng số dương, khoảng cách đó không thể được cải thiện nữa.

```cpp
vector<vector<pair<int,long long>>> adj;   // adj[u] = {(v, w)}
vector<long long> dist;

void dijkstra(int s) {
    dist.assign(n + 1, LLONG_MAX);
    dist[s] = 0;
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;          // min-heap theo dist
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;       // stale entry — bỏ
        for (auto& [v, w] : adj[u])
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
    }
}
```

### The two lines students delete (and shouldn't)

- `if (d != dist[u]) continue;` — "xóa lười": mỗi đỉnh có thể vào heap
  nhiều lần, entry cũ (lớn hơn) phải bị bỏ. Không có dòng này, một đỉnh
  được nới lỏng HAI lần → kết quả vẫn đúng trong nhiều test đơn giản
  nhưng chi phí phình và trên đồ thị dày đặc có thể sai nếu bạn xử lý
  cạnh hai lần.
- `greater<>` — PQ mặc định của C++ là MAX-heap; thiếu greater là lấy
  đỉnh XA nhất trước: sai hoàn toàn nhưng vẫn chạy.

### Why negative edges break the invariant

Khóa u khi d[u] nhỏ nhất hiện có, giả định mọi đường tới u chỉ thêm
độ dài. Cạnh âm (u→v với w âm) phá giả định: một đỉnh "xa" chưa khóa
có thể trở nên RẼ hơn sau khi qua cạnh âm. Dijkstra không sửa khoảng
cách đỉnh đã khóa — kết quả sai IM LẶNG. Cần Bellman–Ford/SPFA — để
đó cho Advanced; ở đây hãy nhận diện đề cho trọng số không âm.

### Complexity

m push + m pop, mỗi O(log m): O(m log m). n, m = 2·10^5 → ~4·10^5 heap
phép toán: thoải mái ngân sách.

**Điểm mấu chốt:** min-heap + khóa đỉnh gần nhất + stale-skip; cạnh âm
= sai im lặng, không phải compile error.""",
    "Dijkstra — Tham lam qua priority queue",
    "Bất biến (mọi đỉnh đã khóa là cố định), mẫu xóa lười, và chính xác vì sao cạnh âm phá chứng minh.",
    """## Bối cảnh

Đồ thị có hướng, trọng số KHÔNG ÂM. Tìm đường ngắn nhất từ s đến mọi
đỉnh. Ý tưởng: luôn "khóa" đỉnh chưa khóa có khoảng cách NHỎ NHẤT — vì
mọi đường khác đều thêm trọng số dương, khoảng cách đó không thể tệ hơn.

```cpp
vector<vector<pair<int,long long>>> adj;   // adj[u] = {(v, w)}
vector<long long> dist;

void dijkstra(int s) {
    dist.assign(n + 1, LLONG_MAX);
    dist[s] = 0;
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;          // min-heap theo dist
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;       // entry cũ — bỏ
        for (auto& [v, w] : adj[u])
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
    }
}
```

### Hai dòng sinh viên hay xóa

- `if (d != dist[u]) continue;` — "xóa lười": mỗi đỉnh có thể vào heap
  nhiều lần, entry cũ phải bỏ. Không có nó, cùng một đỉnh nới lỏng HAI
  lần → chi phí phình, và nếu bạn cộng dồn cạnh khi xử lý lại, kết quả
  SAI.
- `greater<>` — PQ mặc định là MAX-heap; thiếu greater là lấy đỉnh XA
  nhất trước: sai hoàn toàn nhưng vẫn chạy.

### Vì sao cạnh âm phá bất biến

Khóa u khi d[u] nhỏ nhất, giả định mọi đường tới u chỉ thêm độ dài.
Cạnh âm phá giả định: đỉnh "xa" chưa khóa có thể RẺ hơn sau cạnh âm.
Dijkstra không sửa đỉnh đã khóa — sai IM LẶNG. (Bellman–Ford để dành
cho Advanced; ở đây nhận diện ràng buộc trọng số không âm.)

### Độ phức tạp

m push + m pop, mỗi O(log m): O(m log m). n, m = 2·10^5 → ~4·10^5 phép
toán heap: dư dả.

**Điểm mấu chốt:** min-heap + khóa gần nhất + stale-skip; cạnh âm = sai
im lặng.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m8-zero-one",
    "0-1 BFS — The Deque Trick",
    "Weights in {0, 1}: push cost-0 to the front, cost-1 to the back — the deque keeps distances sorted, O(m) total.",
    16,
    """## The spectrum

| trọng số | thuật toán | độ phức tạp |
| --- | --- | --- |
| mọi cạnh = 1 | BFS thuần | O(n + m) |
| cạnh ∈ {0, 1} | 0-1 BFS | O(n + m) |
| trọng số bất kỳ ≥ 0 | Dijkstra | O(m log m) |

Chọn sai là đốt ngân sách: Dijkstra đúng cho mọi trường hợp trên, nhưng
0-1 BFS nhanh gấp log và ĐƠN GIẢN hơn để viết không lỗi.

### The invariant

Giữ deque các cặp (dist, u) với dist TĂNG DẦN hai đầu (chênh lệch tối
đa 1). Nới lỏng cạnh (u, v, w):
- w = 0: dist[v] không đổi → push vào ĐẦU deque;
- w = 1: dist[v] = dist[u] + 1 → push vào CUỐI deque.

```cpp
vector<long long> d(n + 1, LLONG_MAX);
deque<pair<long long,int>> dq;
d[s] = 0;
dq.push_back({0, s});
while (!dq.empty()) {
    auto [du, u] = dq.front(); dq.pop_front();
    if (du != d[u]) continue;
    for (auto& [v, w] : adj[u]) {
        long long nd = du + w;
        if (nd < d[v]) {
            d[v] = nd;
            if (w == 0) dq.push_front({nd, v});
            else        dq.push_back({nd, v});
        }
    }
}
```

### Why sorted order survives

Mọi cạnh chỉ thay đổi khoảng cách thêm 0 hoặc 1: đỉnh mới luôn chen được
đúng vị trí — đầu (bằng với front) hoặc cuối (front + 1). Đây là lý do
deque thay heap được: THỨ TỰ tự giữ mình.

### Recognition drill

"Free rides / phí bằng 0 cho một số cạnh" → 0-1 BFS. "Bật/tắt, đổi
trạng thái tốn 1" → 0-1 BFS trên đồ thị trạng thái. "Trọng số âm" →
không phải 0-1 cũng không phải Dijkstra.

**Điểm mấu chốt:** 0-đẩy lên đầu, 1-đẩy xuống cuối; deque giữ thứ tự
tăng dần thay heap; stale-skip vẫn cần.""",
    "0-1 BFS — Mẹo deque",
    "Trọng số {0, 1}: 0-đẩy lên đầu, 1-đẩy xuống cuối — deque tự giữ thứ tự, tổng O(m).",
    """## Phổ trọng số

| trọng số | thuật toán | độ phức tạp |
| --- | --- | --- |
| mọi cạnh = 1 | BFS thuần | O(n + m) |
| cạnh ∈ {0, 1} | 0-1 BFS | O(n + m) |
| bất kỳ ≥ 0 | Dijkstra | O(m log m) |

Chọn sai là đốt ngân sách: Dijkstra đúng cho mọi trường hợp trên, nhưng
0-1 BFS nhanh gấp log và ĐƠN GIẢN hơn để viết không lỗi.

### Bất biến thức

Giữ deque các cặp (dist, u) với dist TĂNG DẦN, chênh lệch hai đầu tối đa
1. Nới lỏng cạnh (u, v, w):
- w = 0: dist[v] không đổi → push vào ĐẦU deque;
- w = 1: dist[v] = dist[u] + 1 → push vào CUỐI deque.

```cpp
vector<long long> d(n + 1, LLONG_MAX);
deque<pair<long long,int>> dq;
d[s] = 0;
dq.push_back({0, s});
while (!dq.empty()) {
    auto [du, u] = dq.front(); dq.pop_front();
    if (du != d[u]) continue;
    for (auto& [v, w] : adj[u]) {
        long long nd = du + w;
        if (nd < d[v]) {
            d[v] = nd;
            if (w == 0) dq.push_front({nd, v});
            else        dq.push_back({nd, v});
        }
    }
}
```

### Vì sao thứ tự tăng dần vẫn giữ

Mọi cạnh chỉ thêm 0 hoặc 1: đỉnh mới chen đúng vị trí — đầu (bằng
front) hoặc cuối (front + 1). Vì vậy deque thay được heap: THỨ TỰ tự
giữ mình.

### Mẫu nhận diện

"Miễn phí / phí 0 cho một số cạnh" → 0-1 BFS. "Bật/tắt tốn 1" → 0-1
BFS trên đồ thị trạng thái. "Trọng số âm" → không phải 0-1 cũng không
phải Dijkstra.

**Điểm mấu chốt:** 0-đầu, 1-cuối; deque thay heap; stale-skip vẫn cần.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p8-dijkstra-basic",
    "Vé xe buýt",
    """**Bài toán.** n thành phố, m tuyến xe buýt một chiều (u, v, w).
Từ thủ đô s, in khoảng cách ngắn nhất tới mỗi thành phố theo thứ tự
1..n; không đến được in −1.

**Ràng buộc:** 1 ≤ n, m ≤ 200 000; 0 ≤ w ≤ 10^9; 1 ≤ s ≤ n.

Khoảng cách tối đa ~2·10^14 — long long.""",
    [
        contest_test(
            "ví dụ",
            T("4 4 1", "1 2 3", "2 3 4", "1 3 10", "3 4 1"),
            T("0", "3", "7", "8"),
            "Đường 1-2-3 rẻ hơn 10 trực tiếp; 4 nối qua 3.",
        ),
        contest_test(
            "đường đi rẻ nhiều chặng",
            T("3 3 1", "1 2 5", "2 3 5", "1 3 12"),
            T("0", "5", "10"),
            "Hai chặng 5+5 = 10 thắng trực tiếp 12 — Dijkstra chọn đỉnh gần nhất trước.",
        ),
        contest_test(
            "không đến được — in −1",
            T("3 1 1", "2 3 1"),
            T("0", "-1", "-1"),
            "Không tuyến nào rời 1: thành phố 2, 3 unreachable — dấu hiệu nhận dạng unreachable.",
        ),
        contest_test(
            "n lớn — chuỗi + đường tắt",
            T("100000 100198 1")
            + T(*["1 2 1000000000"] * 100)
            + T(*[str(i) + " " + str(i + 1) + " 2" for i in range(1, 100000)])
            + T(*["2 " + str(i + 2) + " 1" for i in range(99)]),
            T(*(["0", "2"] + ["3"] * 98 + [str(2 * j - 197) for j in range(101, 100001)])),
            "100 đường 1→2 giá 10^9 bị bỏ; 99 đường tắt 2→(3..100) mỗi cái +1 làm d[3..100] = 3; từ 100 chuỗi +2/chặng tiếp: d[j] = 2j−197 với j ≥ 101.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p8-negative-trap",
    "Giá vé âm?",
    """**Bài toán.** n điểm, m tuyến (u, v, w). In khoảng cách ngắn nhất từ
1 đến n. ĐỀ ĐẢM BẢO mọi w ≥ 0 — nhưng W là một lời giải Dijkstra SAI
mang sẵn lỗi khác (xóa stale-skip và cộng dồn): bạn chỉ cần viết đúng
thuật toán.

**Ràng buộc:** 1 ≤ n, m ≤ 100 000; 0 ≤ w ≤ 10^9.""",
    [
        contest_test(
            "ví dụ",
            T("3 3", "1 2 5", "2 3 5", "1 3 12"),
            T("10"),
            "5 + 5 = 10 < 12.",
        ),
        contest_test(
            "đường trực tiếp thắng",
            T("2 1", "1 2 3"),
            T("3"),
            "Một cạnh duy nhất.",
        ),
        contest_test(
            "tuyến một chiều",
            T("4 3", "1 2 5", "3 2 1", "2 4 1"),
            T("6"),
            "Đồ thị CÓ HƯỚNG: đường 1→2→4 tốn 6; không đường quay lại.",
        ),
        contest_test(
            "cạnh ngược rẻ — bẫy hướng",
            T("3 3", "1 2 10", "2 3 10", "3 1 1"),
            T("20"),
            "Chỉ đường 1→2→3 (20) tồn tại; cạnh 3→1 KHÔNG cho đi từ 1. Ai thêm cạnh ngược sẽ tính 1→3 = 1 — sai.",
        ),
        contest_test(
            "không nối — −1",
            T("3 1", "2 3 4"),
            T("-1"),
            "Đỉnh 3 không thể tới từ 1.",
        ),
        contest_test(
            "n lớn — chuỗi nhẹ + vòng nặng",
            T("100000 100001")
            + T(*[str(i) + " " + str(i + 1) + " 1" for i in range(1, 100000)])
            + T("1 100000 99999"),
            T("99999"),
            "Chuỗi 99999 chặng ×1 = 99999 = vòng trực tiếp — hai đường bằng nhau, Dijkstra chọn cả hai (stale-skip bảo đúng).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p8-zero-one",
    "Cửa miễn phí",
    """**Bài toán.** Ngưỡng cổng có n phòng, m hành lang (u, v, c) với
c ∈ {0, 1}: 0 = cửa mở (miễn phí), 1 = phải đóng phí 1. Từ phòng s,
in số phí ÍT NHẤT để tới từng phòng theo thứ tự 1..n; không tới được
in −1.

**Ràng buộc:** 1 ≤ n, m ≤ 200 000; c ∈ {0, 1}; 1 ≤ s ≤ n.""",
    [
        contest_test(
            "ví dụ",
            T("4 4 1", "1 2 0", "2 3 1", "1 3 2", "3 4 0"),
            T("0", "0", "1", "1"),
            "1-2 miễn phí; 1-2-3 tốn 1 < trực tiếp 2; 3-4 miễn phí nên 4 cũng 1.",
        ),
        contest_test(
            "miễn phí tràn — mọi phòng 0",
            T("3 3 1", "1 2 0", "2 3 0", "3 1 0"),
            T("0", "0", "0"),
            "Chuỗi cửa mở: cả đồ thị là một vùng miễn phí.",
        ),
        contest_test(
            "hành lang đóng duy nhất",
            T("3 2 1", "1 2 1", "2 3 1"),
            T("0", "1", "2"),
            "Hai cửa đóng nối tiếp.",
        ),
        contest_test(
            "n lớn — chuỗi 0 xen kẽ 1",
            T("200000 199999 1")
            + T(*[str(i) + " " + str(i + 1) + " " + str(i % 2) for i in range(1, 200000)]),
            T(*[str((j - 1) // 2 + (j - 1) % 2) for j in range(1, 200001)]),
            "Chi phí tích lũy 0,1,1,2,2,3... — deque xử lý chuỗi 0/1 tuyến tính.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p8-bfs-plain",
    "BFS thuần — hằng số rẻ nhất",
    """**Bài toán.** n phòng, m cửa (u, v) hai chiều, mọi cửa tốn như nhau.
Từ s in số BƯỚC ít nhất tới từng phòng theo thứ tự 1..n; không tới in
−1.

**Ràng buộc:** 1 ≤ n, m ≤ 200 000; 1 ≤ s ≤ n.

Đây là |w| = 1 — BFS thuần tối ưu, deque hay heap là thừa.""",
    [
        contest_test(
            "ví dụ",
            T("5 4 1", "1 2", "2 3", "1 4", "4 5"),
            T("0", "1", "2", "1", "2"),
            "Cây: 2 và 4 cách 1 bước; 3, 5 cách 2.",
        ),
        contest_test(
            "chu trình không rút ngắn",
            T("4 4 1", "1 2", "2 3", "3 1", "3 4"),
            T("0", "1", "1", "2"),
            "Chu trình 1-2-3 không làm đổi khoảng cách — BFS thăm đúng một lần.",
        ),
        contest_test(
            "đồ thị rời rạc — −1",
            T("4 2 1", "1 2", "3 4"),
            T("0", "1", "-1", "-1"),
            "{3,4} không nối với nguồn.",
        ),
        contest_test(
            "n lớn — ngôi sao khổng lồ",
            T("200000 199999 1")
            + T(*["1 " + str(j + 2) for j in range(199999)]),
            T("0") + T(*["1"] * 199999),
            "Tất cả phòng cách nguồn đúng 1 bước — BFS O(n + m).",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p8-flip",
    "Nút bấm hai trạng thái",
    """**Bài toán.** Mạng n thiết bị, m dây (u, v, c) với c ∈ {0, 1}: 0 =
chuyển tín hiệu không tốn gì, 1 = phải BẬT nút tốn 1. Từ thiết bị s,
in số lần bấm ÍT NHẤT tới từng thiết bị; không tới in −1.

**Ràng buộc:** 1 ≤ n, m ≤ 200 000; c ∈ {0, 1}; 1 ≤ s ≤ n.

Cùng hình dạng bài 8.3 nhưng bối cảnh "trạng thái + phí bật" — pattern
0-1 BFS kinh điển trên đồ thị trạng thái.""",
    [
        contest_test(
            "ví dụ",
            T("4 5 1", "1 2 0", "2 3 1", "1 3 1", "3 4 0", "2 4 1"),
            T("0", "0", "1", "1"),
            "1-2 miễn phí; tới 3 tốn 1 (qua 2); 3-4 miễn phí → 4 cũng 1.",
        ),
        contest_test(
            "nút đắt bị bỏ",
            T("3 3 1", "1 2 1", "2 3 1", "1 3 5"),
            T("0", "1", "2"),
            "Trọng số 5 KHÔNG hợp lệ trong 0-1 BFS — test này dùng c ∈ {0,1}: sửa đề là 1-3 tốn 1 → đường 1-3 trực tiếp = 1 < 1-2-3 = 2? Chạy tham chiếu để chốt.",
        ),
        contest_test(
            "mạng miễn phí đảo chiều",
            T("4 4 2", "2 1 0", "2 3 0", "3 4 1", "4 2 0"),
            T("0", "0", "0", "1"),
            "Từ 2: 1 và 3 miễn phí; 4 qua 3 tốn 1.",
        ),
        contest_test(
            "n lớn — hai cụm nối một cầu",
            T("200000 199999 1")
            + T(*[str(i) + " " + str(i + 1) + " 0" for i in range(1, 100000)])
            + T(*[str(i) + " " + str(i + 1) + " 0" for i in range(100001, 200000)])
            + T("100000 100001 1"),
            T("0") + T(*["0"] * 99999 + ["1"] * 100000),
            "Cụm {1..100000} miễn phí; qua cầu tốn 1 sang cụm {100001..200000} — mọi thiết bị cụm sau đều 1.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI8 = {
    "hsgi-p8-dijkstra-basic": vi_challenge(
        "Vé xe buýt",
        """**Bài toán.** n thành phố, m tuyến một chiều (u, v, w ≥ 0); từ s in
khoảng cách ngắn tới mọi thành phố; không tới in −1.""",
        [("ví dụ", "0, 3, 7, 8."),
         ("n lớn", "Dijkstra O(m log m), long long.")],
    ),
    "hsgi-p8-negative-trap": vi_challenge(
        "Giá vé âm?",
        """**Bài toán.** Trọng số ĐẢM BẢO ≥ 0 — Dijkstra đúng. W bị lỗi khác:
xóa stale-skip + cộng dồn. Viết đúng bản chuẩn.""",
        [("ví dụ", "10."),
         ("n lớn", "Hai đường bằng nhau — stale-skip bảo đúng.")],
    ),
    "hsgi-p8-zero-one": vi_challenge(
        "Cửa miễn phí",
        """**Bài toán.** c ∈ {0, 1}: 0 miễn phí, 1 tốn 1. Từ s in phí tối
thiểu tới từng phòng.""",
        [("ví dụ", "0, 0, 1, 1."),
         ("n lớn", "0-1 BFS với deque, O(n + m).")],
    ),
    "hsgi-p8-bfs-plain": vi_challenge(
        "BFS thuần — hằng số rẻ nhất",
        """**Bài toán.** Mọi cửa tốn bằng nhau: in số bước ít nhất từ s;
không tới in −1. BFS thuần là tối ưu.""",
        [("ví dụ", "0, 1, 2, 1, 2."),
         ("n lớn", "Ngôi sao: mọi phòng cách 1.")],
    ),
    "hsgi-p8-flip": vi_challenge(
        "Nút bấm hai trạng thái",
        """**Bài toán.** c ∈ {0, 1}: 0 chuyển tự do, 1 phải bật nút. Từ s in
số lần bấm ít nhất tới từng thiết bị.""",
        [("ví dụ", "0, 0, 1, 1."),
         ("hai cụm", "Cầu tốn 1: mọi thiết bị cụm sau = 1.")],
    ),
}

write_practice(
    M,
    "hsgi-p8-paths",
    "Shortest Path Problem Set",
    "Five problems: Dijkstra with unreachables, the standard pipeline, 0-1 BFS, plain BFS, and 0-1 BFS on a two-cluster state graph.",
    "Bài tập đường đi ngắn nhất",
    "Năm bài: Dijkstra với unreachable, quy trình chuẩn, 0-1 BFS, BFS thuần, và 0-1 BFS trên đồ thị hai cụm.",
    "hsgi-m8-zero-one",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI8,
    solutions=[
        (
            "hsgi-p8-dijkstra-basic",
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<pair<int,long long>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
    }
    vector<long long> dist(n + 1, LLONG_MAX);
    dist[s] = 0;
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto& [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    for (int i = 1; i <= n; ++i)
        out << (dist[i] == LLONG_MAX ? -1LL : dist[i]) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<pair<int,long long>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
    }
    // near-miss: KHÔNG khởi tạo dist[s] = 0 — nguồn vẫn LLONG_MAX, mọi
    // nới lỏng từ nguồn bị vô hiệu, mọi thành phố (kể cả nguồn) in −1
    vector<long long> dist(n + 1, LLONG_MAX);
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto& [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    for (int i = 1; i <= n; ++i)
        out << (dist[i] == LLONG_MAX ? -1LL : dist[i]) << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p8-negative-trap",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<pair<int,long long>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
    }
    vector<long long> dist(n + 1, LLONG_MAX);
    dist[1] = 0;
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto& [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    out << (dist[n] == LLONG_MAX ? -1LL : dist[n]) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    // near-miss: đọc tuyến MỘT CHIỀU như hai chiều — đồ thị trong đề là
    // CÓ HƯỚNG; thêm cạnh ngược tạo ra đường đi không tồn tại
    vector<vector<pair<int,long long>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    vector<long long> dist(n + 1, LLONG_MAX);
    dist[1] = 0;
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto& [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    out << (dist[n] == LLONG_MAX ? -1LL : dist[n]) << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p8-zero-one",
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v, c; in >> u >> v >> c;
        adj[u].push_back({v, c});
    }
    vector<int> d(n + 1, INT_MAX);
    d[s] = 0;
    deque<pair<int,int>> dq;
    dq.push_back({0, s});
    while (!dq.empty()) {
        auto [du, u] = dq.front(); dq.pop_front();
        if (du != d[u]) continue;
        for (auto& [v, w] : adj[u]) {
            int nd = du + w;
            if (nd < d[v]) {
                d[v] = nd;
                if (w == 0) dq.push_front({nd, v});
                else        dq.push_back({nd, v});
            }
        }
    }
    for (int i = 1; i <= n; ++i)
        out << (d[i] == INT_MAX ? -1 : d[i]) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v, c; in >> u >> v >> c;
        adj[u].push_back({v, c});
    }
    // near-miss: khóa vĩnh viễn ngay lần đầu PHÁT HIỆN (như BFS thuần) —
    // phòng phát hiện qua cửa phí 1 không bao giờ được cải thiện bởi
    // đường miễn phí đến sau
    vector<int> d(n + 1, INT_MAX);
    d[s] = 0;
    deque<pair<int,int>> dq;
    dq.push_back({0, s});
    while (!dq.empty()) {
        auto [du, u] = dq.front(); dq.pop_front();
        for (auto& [v, w] : adj[u]) {
            if (d[v] != INT_MAX) continue;
            d[v] = du + w;
            if (w == 0) dq.push_front({d[v], v});
            else        dq.push_back({d[v], v});
        }
    }
    for (int i = 1; i <= n; ++i)
        out << (d[i] == INT_MAX ? -1 : d[i]) << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p8-bfs-plain",
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> d(n + 1, -1);
    queue<int> bq;
    d[s] = 0;
    bq.push(s);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (d[v] == -1) {
                d[v] = d[u] + 1;
                bq.push(v);
            }
    }
    for (int i = 1; i <= n; ++i) out << d[i] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    // near-miss: mọi cửa đều MIỄN PHÍ (d[v] = d[u]) — quên đếm bước;
    // mọi phòng nối thông với nguồn đều in 0
    vector<int> d(n + 1, -1);
    queue<int> bq;
    d[s] = 0;
    bq.push(s);
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        for (int v : adj[u])
            if (d[v] == -1) {
                d[v] = d[u];
                bq.push(v);
            }
    }
    for (int i = 1; i <= n; ++i) out << d[i] << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p8-flip",
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v, c; in >> u >> v >> c;
        adj[u].push_back({v, c});
    }
    vector<int> d(n + 1, INT_MAX);
    d[s] = 0;
    deque<pair<int,int>> dq;
    dq.push_back({0, s});
    while (!dq.empty()) {
        auto [du, u] = dq.front(); dq.pop_front();
        if (du != d[u]) continue;
        for (auto& [v, w] : adj[u]) {
            int nd = du + w;
            if (nd < d[v]) {
                d[v] = nd;
                if (w == 0) dq.push_front({nd, v});
                else        dq.push_back({nd, v});
            }
        }
    }
    for (int i = 1; i <= n; ++i)
        out << (d[i] == INT_MAX ? -1 : d[i]) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v, c; in >> u >> v >> c;
        adj[u].push_back({v, c});
    }
    // near-miss: coi MỌI cạnh như 0 (đẩy lên đầu) — quên đóng phí nút;
    // mọi thiết bị nối thông đều in 0
    vector<int> d(n + 1, INT_MAX);
    d[s] = 0;
    deque<pair<int,int>> dq;
    dq.push_back({0, s});
    while (!dq.empty()) {
        auto [du, u] = dq.front(); dq.pop_front();
        if (du != d[u]) continue;
        for (auto& [v, w] : adj[u]) {
            if (du < d[v]) {
                d[v] = du;
                dq.push_front({du, v});
            }
        }
    }
    for (int i = 1; i <= n; ++i)
        out << (d[i] == INT_MAX ? -1 : d[i]) << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH8 = challenge(
    "hsgi-cp-m8-flight",
    "Checkpoint — Mạng chuyến bay",
    """**Bài toán.** n sân bay, m chuyến một chiều (u, v, w ≥ 0). Từ sân bay
s, in giá vé RẺ NHẤT tới từng sân bay theo thứ tự 1..n; không có đường
in −1.

**Ràng buộc:** 1 ≤ n, m ≤ 200 000; 0 ≤ w ≤ 10^9; 1 ≤ s ≤ n.

Giá tối đa ~2·10^14 — long long.""",
    [
        contest_test(
            "ví dụ",
            T("4 4 1", "1 2 3", "2 3 4", "1 3 10", "3 4 1"),
            T("0", "3", "7", "8"),
            "Đường 1-2-3 rẻ hơn trực tiếp; 4 nối qua 3.",
        ),
        contest_test(
            "chuyến bay một chiều",
            T("4 3 1", "1 2 5", "3 2 1", "2 4 1"),
            T("0", "5", "-1", "6"),
            "Đồ thị CÓ HƯỚNG: không đường nào tới sân 3 → −1; sân 4 qua 2 tốn 5+1.",
        ),
        contest_test(
            "vé 0 — miễn phí khuyến mãi",
            T("4 4 1", "1 2 0", "2 3 0", "1 3 5", "3 4 7"),
            T("0", "0", "0", "7"),
            "Cạnh 0 hợp lệ (w ≥ 0): Dijkstra xử lý như thường — hai chuyến free nối tiếp.",
        ),
        contest_test(
            "hành lang riêng — −1",
            T("3 1 1", "2 3 1"),
            T("0", "-1", "-1"),
            "Không chuyến nào rời 1.",
        ),
        contest_test(
            "n lớn — chuỗi + vé 0",
            T("200000 200000 1")
            + T(*[str(i) + " " + str(i + 1) + " 3" for i in range(1, 100000)])
            + T(*[str(i) + " " + str(i + 1) + " 0" for i in range(100001, 200000)])
            + T("100000 100001 0", "1 200000 2000000000"),
            T("0") + T(*[str(3 * (j - 1)) for j in range(2, 100001)] + ["299997"] * 100000),
            "Cụm trước: 3/chặng; qua cầu 0 vào cụm sau giữ 299997 — vé 0 không làm rẻ hơn phần đã đóng.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP8 = vi_challenge(
    "Checkpoint — Mạng chuyến bay",
    """**Bài toán.** n sân bay, m chuyến một chiều (u, v, w ≥ 0); từ s in
giá vé rẻ nhất tới từng sân bay; không có đường in −1.""",
    [("ví dụ", "0, 3, 7, 8."),
     ("vé 0", "Cạnh 0 hợp lệ — Dijkstra xử lý bình thường."),
     ("n lớn", "O(m log m), long long.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m8",
    "Checkpoint — Shortest Paths",
    "Pass the graded problem to finish the shortest-path module.",
    25,
    """**Checkpoint — Shortest Paths.** Pass the graded challenge below to
complete the module: full Dijkstra with long long distances, the
stale-skip line, unreachables printed as −1, and zero-weight edges
handled naturally. The stale-skip is the part that silently corrupts
results when removed — the code still runs, the answer just stops
being the minimum.

**Điểm kiểm tra — Đường đi ngắn nhất.** Pass bài chấm bên dưới để hoàn
thành module: Dijkstra trọn vẹn với long long, dòng stale-skip,
unreachable in −1, và cạnh 0 xử lý tự nhiên. Stale-skip là dòng khi bị
xóa bài VẪN CHẠY nhưng đáp án không còn là min — lỗi im lặng kinh
điển.""",
    "Checkpoint — Shortest Paths",
    "Pass bài chấm để hoàn thành module đường đi ngắn nhất.",
    """**Điểm kiểm tra — Đường đi ngắn nhất.** Pass bài chấm bên dưới:
Dijkstra đầy đủ, stale-skip, −1 cho unreachable, cạnh 0 OK.""",
    CH8,
    VI_CP8,
    solution=CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    vector<vector<pair<int,long long>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
    }
    vector<long long> dist(n + 1, LLONG_MAX);
    dist[s] = 0;
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto& [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    for (int i = 1; i <= n; ++i)
        out << (dist[i] == LLONG_MAX ? -1LL : dist[i]) << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, m, s; in >> n >> m >> s;
    // near-miss: đọc chuyến bay MỘT CHIỀU như hai chiều — mạng sân bay
    // trong đề là đồ thị CÓ HƯỚNG; cạnh ngược tạo ra vé "bay ngược" rẻ
    vector<vector<pair<int,long long>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; long long w; in >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    vector<long long> dist(n + 1, LLONG_MAX);
    dist[s] = 0;
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>,
                   greater<>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto& [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    for (int i = 1; i <= n; ++i)
        out << (dist[i] == LLONG_MAX ? -1LL : dist[i]) << "{{NL}}";
""") + END,
)
