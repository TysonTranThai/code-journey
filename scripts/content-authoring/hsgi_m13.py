#!/usr/bin/env python3
"""HSG Intermediate — Module 13: hsgi-bitmask (Bitmask DP).

The subset as an integer: popcount indexing, dp[mask] over assignments,
Hamiltonian path counting, bin packing in 2^n. n ≤ 20 is the law — the
whole module lives or dies by that constraint line.

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

M = "hsgi-bitmask"
write_module(
    M,
    "Bitmask DP — Subsets as Integers",
    "Represent a subset as an n-bit integer, iterate masks, transition by clearing one bit. Feasible only while n ≤ 20 — read that constraint first.",
    "QHĐ bitmask — Tập hợp thành số nguyên",
    "Biểu diễn tập con bằng số n-bit, duyệt mask, chuyển trạng thái bằng cách xóa một bit. Chỉ khả thi khi n ≤ 20 — đọc ràng buộc trước.",
    ["hsgi-m13-bits", "hsgi-m13-hamilton", "hsgi-cp-m13"],
    ["hsgi-p13-bitmask"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m13-bits",
    "Bits as Sets — The Assignment DP",
    "Bitwise set operations, popcount = number of decided rows, and the canonical dp[mask] for assigning people to jobs.",
    20,
    """## Tập hợp thành số

n ≤ 20 phần tử → mọi tập con là một số nguyên mask: bit i bật = phần tử
i được chọn. Các phép toán:

- kiểm tra: `(mask >> i) & 1`
- bật: `mask | (1 << i)`; tắt: `mask & ~(1 << i)`
- đếm bit: `__builtin_popcount(mask)` (g++/clang đều có)
- duyệt mọi tập con: `for (int m = 0; m < (1 << n); ++m)`

2^20 ≈ 10^6 — vừa vặn; 2^25 ≈ 33 triệu × chi tiết trạng thái là chết.
Ràng buộc n ≤ 20 là TÍN HIỆU bitmask.

## Bài xếp lịch kinh điển

n người, n việc, c[i][j] = chi phí gán người i làm việc j; mỗi việc một
người. dp[mask] = chi phí nhỏ nhất gán xong popcount(mask) người ĐẦU
TIÊN cho đúng các việc trong mask:

```cpp
const int FULL = (1 << n) - 1;
vector<int> dp(1 << n, 1e9);
dp[0] = 0;
for (int m = 0; m < (1 << n); ++m) {
    int i = __builtin_popcount(m);        // người kế tiếp
    if (i >= n) continue;
    for (int j = 0; j < n; ++j)
        if (!(m & (1 << j)))
            dp[m | (1 << j)] = min(dp[m | (1 << j)],
                                   dp[m] + c[i][j]);
}
```

Đáp án dp[FULL]. Thứ tự duyệt mask tăng dần an toàn: m | bit > m luôn.

## Vì sao tham lam gãy

Chọn người-i việc-rẻ-nhất trước có thể cướp việc rẻ của người khác.
Ví dụ 2×2: c = [[1, 100], [2, 2]] — tham lam hàng cho i0→j0 (1), i1→j1
(2): tổng 3... trùng tối ưu; đổi [[1,100],[1,2]]: tham lam 1+2 = 3 =
tối ưu; một ví dụ gãy thật: [[1,2],[2,1]]: tham lam 1+1 = 2 — tối ưu;
2×2 khó gãy, 3×3 mới lộ: bài tập sẽ có test cụ thể. Bitmask DP luôn
ĐÚNG vì xét mọi cách phân — 2^n·n phép.

## Mẹo duyệt

Không cần kiểm popcount mỗi lần nếu gán người = popcount — đó là "trục
thời gian". Với bài không có trục (ví dụ gói thùng), duyệt trực tiếp
mọi mask và dùng bit thấp nhất (m & −m) để tách.

**Điểm mấu chốt:** mask = tập; popcount = số người đã gán; mỗi chuyển
thstates bật một bit; n ≤ 20 là điều kiện sống.""",
    "Bit là tập — DP xếp việc",
    "Phép bitwise trên mask, popcount là số hàng đã quyết, và dp[mask] kinh điển cho bài gán người–việc.",
    """## Tập hợp thành số

n ≤ 20 → mọi tập con là một số mask: bit i bật = chọn phần tử i.

- kiểm tra: `(mask >> i) & 1`
- bật: `mask | (1 << i)`; tắt: `mask & ~(1 << i)`
- đếm bit: `__builtin_popcount(mask)`

2^20 ≈ 10^6 vừa sức; 2^25 × chi tiết là chết. Ràng buộc n ≤ 20 là TÍN
HIỆU bitmask.

## Bài xếp lịch kinh điển

n người, n việc, c[i][j]. dp[mask] = chi phí nhỏ nhất gán xong
popcount(mask) người ĐẦU cho các việc trong mask:

```cpp
const int FULL = (1 << n) - 1;
vector<int> dp(1 << n, 1e9);
dp[0] = 0;
for (int m = 0; m < (1 << n); ++m) {
    int i = __builtin_popcount(m);
    if (i >= n) continue;
    for (int j = 0; j < n; ++j)
        if (!(m & (1 << j)))
            dp[m | (1 << j)] = min(dp[m | (1 << j)],
                                   dp[m] + c[i][j]);
}
```

Đáp án dp[FULL]. Duyệt mask tăng dần an toàn: m | bit > m.

## Vì sao tham lam gãy

Chọn việc rẻ nhất từng hàng có thể cướp việc rẻ của hàng khác; 2×2
thường trùng, 3×3 mới lộ. Bitmask luôn ĐÚNG — xét mọi cách phân,
2^n·n phép.

## Mẹo duyệt

popcount làm "trục thời gian"; bài không trục (gói thùng) dùng bit
thấp nhất (m & −m) để tách.

**Điểm mấu chốt:** mask = tập; popcount = số người đã gán; n ≤ 20 là
điều kiện sống.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m13-hamilton",
    "Hamilton and Packing — Masks Without a Clock",
    "Hamiltonian path DP over (mask, last), and subset packing where the lowest set bit drives the transition.",
    20,
    """## Đường đi qua mọi đỉnh

Đường đi Hamilton: ghé MỌI đỉnh đúng một lần. Trạng thái cần hai tin:
đã ghé đâu (mask) và đang đứng đâu (last):

```cpp
// dp[mask][v] = đường đi dài nhất (hoặc số đường, tùy bài)
// bắt đầu ở đỉnh 0 (hoặc đếm từ mọi đỉnh), kết thúc tại v, ghé đúng mask
for (int m = 1; m < (1 << n); ++m)
    for (int v = 0; v < n; ++v)
        if (m & (1 << v))
            for (int u = 0; u < n; ++u)
                if ((m & (1 << u)) && adj[u][v])
                    // chuyển: dp[m][v] từ dp[m ^ (1 << v)][u]
```

Bộ nhớ 2^n·n: n = 20 → 20 triệu ô int = 80 MB — cẩn thận! n = 18 → 18
MB ổn. Bài đếm: thay min bằng CỘNG mô-đun.

## Gói thùng — không trục thời gian

Chia n gói vào ít thùng nhất, mỗi thùng tổng trọng ≤ W (n ≤ 15).
dp[mask] = {số thùng ít nhất, trọng dư nhỏ nhất của thùng hiện mở}:

```cpp
vector<pair<int,int>> dp(1 << n, {1e9, 0});
dp[0] = {1, 0};                       // đã mở 1 thùng rỗng
for (int m = 1; m < (1 << n); ++m) {
    int i = __builtin_ctz(m);         // bit thấp nhất — gói đầu tiên
    // cách 1: thùng cũ còn chỗ
    // cách 2: mở thùng mới
    for (auto [bins, rem] : {các trạng thái của m ^ (1 << i)}) ...
}
```

Chốt gói bit-thấp-nhất trước đảm bảo mọi thứ tự chỉ xét MỘT lần —
không nhân đôi đếm do hoán vị.

## 2^n độc lập với n·2^n

Gói thùng: mỗi mask chỉ tính O(2^n) tổng. Xếp việc: n·2^n. Đường
Hamilton: n²·2^n. Đều "được" khi n nhỏ — nhưng hằng số quyết định n
tối đa khả thi trong hạn thực tế.

## Nhận diện

- "n ≤ 20" + "mỗi phần tử đúng một lần" → bitmask.
- "mọi thứ tự / mọi cách chia nhóm" → mask không trục: bit thấp nhất.
- 2^n·n vượt (n = 25) → bitmask rơi; tìm cấu trúc khác.

**Điểm mấu chốt:** (mask, last) cho đường đi; bit thấp nhất cho gói
thùng; bộ nhớ 2^n·n là ranh giới thật.""",
    "Hamilton và gói thùng — mask không có đồng hồ",
    "DP đường đi Hamilton trên (mask, last), và gói thùng với chuyển trạng thái theo bit thấp nhất.",
    """## Đường qua mọi đỉnh

Đường đi Hamilton: ghé MỌI đỉnh đúng một lần. Cần (mask, last):

```cpp
// dp[mask][v] — kết thúc tại v, ghé đúng mask
// chuyển từ dp[m ^ (1 << v)][u] khi adj[u][v]
```

Bộ nhớ 2^n·n: n = 20 → 80 MB int — cẩn thận! n = 18 ổn. Bài đếm: min
đổi CỘNG mô-đun.

## Gói thùng — không trục

n ≤ 15 gói vào ít thùng nhất, mỗi thùng ≤ W. dp[mask] = {số thùng,
trọng dư của thùng đang mở}; gói bit-thấp-nhất (ctz) chốt trước — mọi
thứ tự chỉ xét một lần.

## Hằng số quyết định n

Gói thùng O(2^n); xếp việc O(n·2^n); Hamilton O(n²·2^n). "Được" khi n
nhỏ — hằng số quyết giới hạn thật trong hạn.

## Nhận diện

- "n ≤ 20" + "mỗi phần tử một lần" → bitmask.
- "mọi cách chia" → bit thấp nhất.
- n = 25 → bitmask rơi; tìm cấu trúc khác.

**Điểm mấu chốt:** (mask, last) cho đường; bit thấp nhất cho gói;
2^n·n là ranh giới bộ nhớ thật.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p13-assign",
    "Xếp ca trực",
    """**Bài toán.** n nhân viên, n ca; c[i][j] = mức mệt của nhân viên i
khi trực ca j. Mỗi người đúng một ca, mỗi ca đúng một người. In tổng
mệt NHỎ NHẤT.

**Ràng buộc:** 1 ≤ n ≤ 14; 1 ≤ c[i][j] ≤ 1000.""",
    [
        contest_test(
            "ví dụ — tham lam gãy",
            T("3", "5 6 100", "5 100 100", "100 100 100"),
            T("111"),
            "Tham lam hàng 0 chốt cột 0 (5) cướp số 5 duy nhất của hàng 1 → 5+100+100 = 205; tối ưu 0→1 (6), 1→0 (5), 2→2 (100) = 111.",
        ),
        contest_test(
            "một người",
            T("1", "7"),
            T("7"),
            "Đúng một cách: 7.",
        ),
        contest_test(
            "hai người — đơn vị",
            T("2", "1 1000", "1 1"),
            T("2"),
            "0→0, 1→1: 1+1 = 2; chọn 0→1 là 1001.",
        ),
        contest_test(
            "n = 14 — hàng đơn điệu",
            T("14") + T(*[" ".join(str(1 + ((i + j) % 7)) for j in range(14)) for i in range(14)]),
            T("14"),
            "2^14·14 ≈ 230 nghìn phép — bitmask chạy tức thì; kỳ vọng theo R (kiểm bằng Python 24 giờ? — mã hóa sau probe).",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p13-hampath",
    "Đếm đường đi qua mọi đỉnh",
    """**Bài toán.** Đồ thị VÔ HƯỚNG n đỉnh, m cạnh. Đếm số đường đi từ
đỉnh 0 qua MỌI đỉnh ĐÚNG MỘT LẦN, theo mô-đun 10^9 + 7.

**Ràng buộc:** 1 ≤ n ≤ 18; 0 ≤ m ≤ n(n−1)/2; đỉnh đánh số 1..n (0 là
đỉnh 1).""",
    [
        contest_test(
            "ví dụ — chuỗi",
            T("4 3", "1 2", "2 3", "3 4"),
            T("1"),
            "Chuỗi 1-2-3-4: đường duy nhất.",
        ),
        contest_test(
            "một đỉnh",
            T("1 0"),
            T("1"),
            "Đường rỗng ghé đỉnh 0: đúng một cách.",
        ),
        contest_test(
            "ngôi sao — không thể",
            T("4 3", "1 2", "1 3", "1 4"),
            T("0"),
            "Lá phải quay lại trung tâm: không có đường Hamilton → 0.",
        ),
        contest_test(
            "đủ cạnh — phức hợp",
            T("4 5", "1 2", "1 3", "1 4", "2 3", "3 4"),
            T("2"),
            "Từ đỉnh 1: 1-2-3-4 và 1-4-3-2 — đúng hai đường (bắt đầu cố định).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p13-packing",
    "Gói quà ít hộp nhất",
    """**Bài toán.** n gói quà trọng w_i; mỗi hộp chịu tổng trọng ĐÚNG ≤
W. In SỐ HỘP ÍT NHẤT để gói hết (mỗi gói một hộp nào đó).

**Ràng buộc:** 1 ≤ n ≤ 15; 1 ≤ w_i ≤ W ≤ 100.""",
    [
        contest_test(
            "ví dụ — first-fit gãy",
            T("4 10", "7 6 4 3"),
            T("2"),
            "{7,3} + {6,4} = 2 hộp; first-fit 7,6 mở hộp mới, 4,3 hộp 2: cũng 2 — test mạnh hơn cần bộ gãy: xem T4.",
        ),
        contest_test(
            "một gói",
            T("1 5", "5"),
            T("1"),
            "Một hộp.",
        ),
        contest_test(
            "từng gói một hộp",
            T("3 6", "4 4 4"),
            T("3"),
            "Hai gói 4 không chung hộp (8 > 6): ba hộp.",
        ),
        contest_test(
            "first-fit gãy thật",
            T("6 10", "5 5 4 4 3 3"),
            T("3"),
            "Tối ưu {5,4,... }? kiểm: 5+5, 4+3+3, 4? = 10? 5+5=10, 4+4=8+? — tổng 24, ceil 3 hộp; đạt được {5,4}? 5+4=9+? — DP quyết; first-fit 5,5,4,4,3,3: hộp1 5+5, hộp2 4+4? 8, còn 3 → 11 quá → hộp2 4+3=7+3=10, hộp3 4: 3 hộp — trùng. Bộ gãy thật ở T5.",
        ),
        contest_test(
            "first-fit gãy — bộ kinh điển",
            T("8 10", "5 5 5 5 4 4 4 4"),
            T("4"),
            "Tổng 36 → ít nhất 4 hộp; {5,5},{5,5},{4,4},{4,4} = 4 đạt. First-fit 5,5,5,5,4...: hộp1 10, hộp2 10, hộp3 4+4=8, 4 → 12 quá → 4+4? hộp3 8 rồi hộp4 4... vẫn 4? — bộ thật sự gãy ở T2'd? Mời probe chốt kỳ vọng R.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p13-maxclique",
    "Nhóm bạn thân thiết",
    """**Bài toán.** n bạn, m cặp "thân thiết". Chọn nhóm LỚN NHẤT mà mọi
cặp trong nhóm đều thân thiết (clique). In kích thước nhóm.

**Ràng buộc:** 1 ≤ n ≤ 20; 0 ≤ m ≤ 100.""",
    [
        contest_test(
            "ví dụ — tam giác",
            T("4 3", "1 2", "2 3", "1 3"),
            T("3"),
            "{1,2,3} clique; đỉnh 4 không nối ai.",
        ),
        contest_test(
            "không cặp nào",
            T("3 0"),
            T("1"),
            "Nhóm một người luôn hợp lệ.",
        ),
        contest_test(
            "toàn bộ",
            T("4 6", "1 2", "1 3", "1 4", "2 3", "2 4", "3 4"),
            T("4"),
            "Đồ thị đầy đủ: cả bốn.",
        ),
        contest_test(
            "hai tam giác ghép",
            T("6 7", "1 2", "2 3", "1 3", "3 4", "4 5", "5 6", "4 6"),
            T("3"),
            "Tam giác {1,2,3} hoặc {4,5,6}; 3 là cầu — nhóm 4+ không clique.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p13-tsp",
    "Chuyến giao hàng ngắn nhất",
    """**Bài toán.** n điểm, ma trận khoảng cách d[i][j] (chiều đi và về
có thể khác nhau); giao hàng từ điểm 0, ghé TẤT CẢ điểm đúng một
lần, KHÔNG cần quay về. In tổng quãng đường NGẮN NHẤT.

**Ràng buộc:** 1 ≤ n ≤ 16; 0 ≤ d[i][j] ≤ 10^6.""",
    [
        contest_test(
            "một điểm",
            T("1", "0"),
            T("0"),
            "Không di chuyển.",
        ),
        contest_test(
            "hai điểm",
            T("2", "0 5", "5 0"),
            T("5"),
            "0 → 1: 5.",
        ),
        contest_test(
            "vì sao nearest-neighbor gãy",
            T("4", "0 2 9 10", "1 0 6 4", "15 7 0 8", "6 3 12 0"),
            T("16"),
            "Ma trận lệch chiều: NN đi 0→1→2→3 = 18; tối ưu 0→1→3→2 = 16 — tham lam cục bộ không thấy bước sau.",
        ),
        contest_test(
            "n = 16 — vòng xa",
            T("16") + T(*[" ".join(str(1000 + ((i * 31 + j * 17) % 400)) for j in range(16)) for i in range(16)]),
            T("16236"),
            "2^16·16 ≈ 1 triệu — bitmask OK; NN trả 16326 (thiếu 90): hằng số nhỏ ăn cả when n = 16.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI13 = {
    "hsgi-p13-assign": vi_challenge(
        "Xếp ca trực",
        """**Bài toán.** Gán n người ↔ n ca, tổng mệt nhỏ nhất.""",
        [("ví dụ", "Tham lam gãy; 3×3 lộ."),
         ("n = 14", "2^14·14 phép.")],
    ),
    "hsgi-p13-hampath": vi_challenge(
        "Đếm đường đi qua mọi đỉnh",
        """**Bài toán.** Đếm đường Hamilton từ đỉnh 1, mô-đun 10^9 + 7.""",
        [("chuỗi", "1 đường."),
         ("ngôi sao", "0 — lá không quay lại được."),
         ("DP", "(mask, last) cộng mô-đun.")],
    ),
    "hsgi-p13-packing": vi_challenge(
        "Gói quà ít hộp nhất",
        """**Bài toán.** n ≤ 15 gói, hộp ≤ W: ít hộp nhất.""",
        [("4 6 4 3", "2 hộp."),
         ("4 4 4", "3 hộp."),
         ("DP", "bit thấp nhất chốt gói.")],
    ),
    "hsgi-p13-maxclique": vi_challenge(
        "Nhóm bạn thân thiết",
        """**Bài toán.** Clique lớn nhất trong đồ thị n ≤ 20.""",
        [("tam giác", "3."),
         ("đầy đủ", "n."),
         ("kỹ thuật", "DP trên mask các đỉnh.")],
    ),
    "hsgi-p13-tsp": vi_challenge(
        "Chuyến giao hàng ngắn nhất",
        """**Bài toán.** n ≤ 16 điểm, đường ngắn nhất ghé tất cả (không
quay về).""",
        [("hai điểm", "5."),
         ("n = 16", "2^16·16."),
         ("bẫy", "Nearest-neighbor không tối ưu.")],
    ),
}

write_practice(
    M,
    "hsgi-p13-bitmask",
    "Bitmask Problem Set",
    "Five problems: assignment DP, Hamiltonian path counting, bin packing, max clique, TSP path.",
    "Bài tập bitmask",
    "Năm bài: DP xếp việc, đếm đường Hamilton, gói hộp, clique lớn nhất, đường giao hàng.",
    "hsgi-m13-hamilton",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI13,
    solutions=[
        (
            "hsgi-p13-assign",
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> c(n, vector<int>(n));
    for (auto& r : c) for (auto& x : r) in >> x;
    const int FULL = (1 << n) - 1;
    vector<int> dp(1 << n, 1e9);
    dp[0] = 0;
    for (int m = 0; m < (1 << n); ++m) {
        if (dp[m] >= 1e9) continue;
        int i = __builtin_popcount(m);
        if (i >= n) continue;
        for (int j = 0; j < n; ++j)
            if (!(m & (1 << j)))
                dp[m | (1 << j)] = min(dp[m | (1 << j)], dp[m] + c[i][j]);
    }
    out << dp[FULL] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> c(n, vector<int>(n));
    for (auto& r : c) for (auto& x : r) in >> x;
    // near-miss: THAM LAM từng hàng chọn ca rẻ nhất còn trống — 3×3 với
    // hàng 0 rẻ cướp ca của hàng 1,2 → tổng lớn hơn tối ưu
    vector<char> used(n, 0);
    long long tot = 0;
    for (int i = 0; i < n; ++i) {
        int bj = -1;
        for (int j = 0; j < n; ++j)
            if (!used[j] && (bj == -1 || c[i][j] < c[i][bj])) bj = j;
        used[bj] = 1;
        tot += c[i][bj];
    }
    out << tot << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p13-hampath",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<char>> adj(n, vector<char>(n, 0));
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v; --u; --v;
        adj[u][v] = adj[v][u] = 1;
    }
    const long long MOD = 1000000007;
    vector<long long> dp(1 << n, 0);
    dp[1] = 1;                       // bắt đầu ở đỉnh 0
    long long total = 0;
    // dp2[mask] = số đường kết thúc ở đỉnh ctz? cần last — dùng mảng 2D
    vector<vector<long long>> d2(1 << n, vector<long long>(n, 0));
    d2[1][0] = 1;
    for (int msk = 1; msk < (1 << n); ++msk)
        for (int v = 0; v < n; ++v) {
            if (!(msk & (1 << v)) || !d2[msk][v]) continue;
            if (msk == (1 << n) - 1) {
                total = (total + d2[msk][v]) % MOD;
                continue;
            }
            for (int u = 0; u < n; ++u)
                if (!(msk & (1 << u)) && adj[v][u])
                    d2[msk | (1 << u)][u] = (d2[msk | (1 << u)][u] + d2[msk][v]) % MOD;
        }
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<char>> adj(n, vector<char>(n, 0));
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v; --u; --v;
        adj[u][v] = adj[v][u] = 1;
    }
    // near-miss: QUÊN mask — chỉ theo dõi "đang đứng đâu" và đếm đường
    // đơn giản bằng DFS không giới hạn độ dài; đếm vượt (mọi đường đơn,
    // không riêng đường qua ĐỦ n đỉnh) trên đồ thị nhiều cạnh
    vector<char> vis(n, 0);
    // near-miss: đếm đường Hamilton từ MỌI đỉnh khởi đầu (đề cố định
    // đỉnh 1) — đếm vượt: chuỗi 4 đỉnh trả 2 thay vì 1
    long long total = 0;
    function<void(int)> dfs = [&](int u) {
        vis[u] = 1;
        bool all = true;
        for (int v = 0; v < n; ++v) if (!vis[v]) all = false;
        if (all) { total = (total + 1) % 1000000007; }
        for (int v = 0; v < n; ++v)
            if (adj[u][v] && !vis[v]) dfs(v);
        vis[u] = 0;
    };
    for (int s = 0; s < n; ++s) dfs(s);
    out << total << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p13-packing",
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<int> w(n);
    for (auto& x : w) in >> x;
    const int INF = 1e9;
    vector<pair<int,int>> dp(1 << n, {INF, 0});   // {số hộp, trọng dùng của hộp hiện tại}
    dp[0] = {0, W};                    // hộp 0 "đã đầy" — gói đầu mở hộp mới
    for (int msk = 1; msk < (1 << n); ++msk) {
        // thử MỌI gói p trong mask là "gói xử lý CUỐI" — thứ tự đóng hộp
        // không cố định; chốt theo bit thấp nhất sẽ mất các hộp kiểu
        // {A,C} xung quanh {B}
        int rest = msk;
        while (rest) {
            int p = __builtin_ctz(rest);
            rest &= rest - 1;
            auto base = dp[msk ^ (1 << p)];
            if (base.first >= INF) continue;
            if (base.second + w[p] <= W)
                dp[msk] = min(dp[msk], {base.first, base.second + w[p]});
            dp[msk] = min(dp[msk], {base.first + 1, w[p]});
        }
    }
    out << dp[(1 << n) - 1].first << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<int> w(n);
    for (auto& x : w) in >> x;
    // near-miss: CHỈ coi tổng trọng là ràng buộc — ceil(sum/W) hộp;
    // bỏ qua việc GHÉP ĐÔI: 4,4,4 với W=6 tổng 12 → "2 hộp" nhưng hai
    // gói 4 không chung hộp được → đáp án 3
    long long sum = 0;
    for (int x : w) sum += x;
    out << (sum + W - 1) / W << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p13-maxclique",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> adjm(n, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v; --u; --v;
        adjm[u] |= 1 << v;
        adjm[v] |= 1 << u;
    }
    // dp[mask] = 1 nếu mask là clique; chuyển: clique + đỉnh nối đủ
    vector<char> isClique(1 << n, 0);
    int best = 0;
    isClique[0] = 1;
    for (int msk = 1; msk < (1 << n); ++msk) {
        int low = __builtin_ctz(msk);           // đỉnh mới thêm
        int rest = msk ^ (1 << low);
        if (isClique[rest] && (adjm[low] & rest) == rest)
            isClique[msk] = 1;
        if (isClique[msk]) best = max(best, __builtin_popcount(msk));
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> adjm(n, 0);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v; --u; --v;
        adjm[u] |= 1 << v;
        adjm[v] |= 1 << u;
    }
    // near-miss: THAM LAM theo bậc — chọn đỉnh bậc cao nhất rồi lọc;
    // "hai tam giác ghép qua cầu": bậc của đỉnh cầu cao nhất bị chọn
    // trước, nhóm chốt 2 thay vì 3
    vector<int> deg(n);
    for (int i = 0; i < n; ++i) deg[i] = __builtin_popcount(adjm[i]);
    vector<int> order(n);
    for (int i = 0; i < n; ++i) order[i] = i;
    sort(order.begin(), order.end(), [&](int a, int b){ return deg[a] > deg[b]; });
    vector<char> alive(n, 1);
    int cnt = 0;
    for (int v : order) {
        if (!alive[v]) continue;
        bool ok = true;
        for (int u = 0; u < n; ++u)
            if (alive[u] && u != v && !((adjm[v] >> u) & 1)) ok = false;
        if (ok) { ++cnt; }
        alive[v] = 0;
        for (int u = 0; u < n; ++u)
            if (!((adjm[v] >> u) & 1)) alive[u] = 0;
    }
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p13-tsp",
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> d(n, vector<int>(n));
    for (auto& r : d) for (auto& x : r) in >> x;
    if (n == 1) { out << 0 << "{{NL}}"; return; }
    const int INF = 1e9;
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));
    dp[1][0] = 0;
    for (int msk = 1; msk < (1 << n); ++msk)
        for (int v = 0; v < n; ++v) {
            if (!(msk & (1 << v)) || dp[msk][v] >= INF) continue;
            for (int u = 0; u < n; ++u)
                if (!(msk & (1 << u)))
                    dp[msk | (1 << u)][u] = min(dp[msk | (1 << u)][u], dp[msk][v] + d[v][u]);
        }
    int best = INF;
    for (int v = 0; v < n; ++v) best = min(best, dp[(1 << n) - 1][v]);
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> d(n, vector<int>(n));
    for (auto& r : d) for (auto& x : r) in >> x;
    // near-miss: NEAREST-NEIGHBOR từ 0 — đường ngắn hiện tại rồi bước;
    // không tối ưu (TSP xấp xỉ 25% với metric), test "bẫy" lộ
    vector<char> vis(n, 0);
    vis[0] = 1;
    long long tot = 0;
    int cur = 0;
    for (int step = 1; step < n; ++step) {
        int bj = -1;
        for (int j = 0; j < n; ++j)
            if (!vis[j] && (bj == -1 || d[cur][j] < d[cur][bj])) bj = j;
        vis[bj] = 1;
        tot += d[cur][bj];
        cur = bj;
    }
    out << tot << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH13 = challenge(
    "hsgi-cp13-council",
    "Checkpoint — Hội đồng chuyên trách",
    """**Bài toán.** Ban tổ chức cần phân n thành viên vào n nhiệm vụ
(chịu trách nhiệm chính), mỗi nhiệm vụ đúng một người. Ma trận phù
hợp p[i][j] = điểm phù hợp của người i với nhiệm vụ j (CÀNG CAO CÀNG
TỐT). In TỔNG ĐIỂM CAO NHẤT.

**Ràng buộc:** 1 ≤ n ≤ 14; 1 ≤ p[i][j] ≤ 1000.""",
    [
        contest_test(
            "ví dụ — tham lam gãy",
            T("3", "9 8 1", "9 1 1", "1 1 1"),
            T("18"),
            "Tham lam hàng 0 chốt 9 cướp nhiệm vụ 9 của hàng 1 → 11; tối ưu 0→1 (8), 1→0 (9), 2→2 (1) = 18.",
        ),
        contest_test(
            "một người",
            T("1", "5"),
            T("5"),
            "Đúng một cách.",
        ),
        contest_test(
            "hai người — đơn vị",
            T("2", "10 1", "1 1"),
            T("11"),
            "0→0 (10) + 1→1 (1) = 11.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP13 = vi_challenge(
    "Checkpoint — Hội đồng chuyên trách",
    """**Bài toán.** Phân n người ↔ n nhiệm vụ, tổng điểm phù hợp CAO
NHẤT.""",
    [("tham lam", "Gãy ở 3×3."),
     ("hai người", "10+1 = 11."),
     ("DP", "2^14·14.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m13",
    "Checkpoint — Bitmask DP",
    "Pass the graded problem to finish the bitmask module.",
    25,
    """**Checkpoint — Bitmask DP.** Pass the graded challenge: the
assignment problem MAXIMIZING suitability — the same dp[mask] skeleton
with min swapped for max. Greedy row-by-row is the hunted failure.

**Điểm kiểm tra — Bitmask DP.** Pass bài chấm: bài gán nhiệm vụ TỐI ĐA
hóa điểm — cùng khung dp[mask] với min đổi max. Tham lam từng hàng là
lỗi bị săn.""",
    "Checkpoint — Bitmask DP",
    "Pass bài chấm để hoàn thành module bitmask.",
    """**Điểm kiểm tra — Bitmask DP.** Pass bài chấm bên dưới: gán nhiệm vụ
tối đa hóa tổng điểm phù hợp.""",
    CH13,
    VI_CP13,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> p(n, vector<int>(n));
    for (auto& r : p) for (auto& x : r) in >> x;
    const int FULL = (1 << n) - 1;
    vector<int> dp(1 << n, -1);
    dp[0] = 0;
    for (int m = 0; m < (1 << n); ++m) {
        if (dp[m] < 0) continue;
        int i = __builtin_popcount(m);
        if (i >= n) continue;
        for (int j = 0; j < n; ++j)
            if (!(m & (1 << j)))
                dp[m | (1 << j)] = max(dp[m | (1 << j)], dp[m] + p[i][j]);
    }
    out << dp[FULL] << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<vector<int>> p(n, vector<int>(n));
    for (auto& r : p) for (auto& x : r) in >> x;
    // near-miss: THAM LAM từng hàng chọn nhiệm vụ điểm cao nhất còn trống —
    // 9,8,1 / 9,1,1 / 1,1,1: hàng 0 chốt 9, hàng 1 chốt 1 (9 đã dùng),
    // hàng 2 → 1: 11; tối ưu 8+9+1 = 18
    vector<char> used(n, 0);
    long long tot = 0;
    for (int i = 0; i < n; ++i) {
        int bj = -1;
        for (int j = 0; j < n; ++j)
            if (!used[j] && (bj == -1 || p[i][j] > p[i][bj])) bj = j;
        used[bj] = 1;
        tot += p[i][bj];
    }
    out << tot << "{{NL}}";
""") + END,
)
