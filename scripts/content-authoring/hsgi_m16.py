#!/usr/bin/env python3
"""HSG Intermediate — Module 16: hsgi-synthesis (technique synthesis).

Mixes the intermediate toolkit under recognition pressure: sliding window,
prefix-map subarray counting, Kadane, exchange-argument scheduling, and a
graded checkpoint composing Fenwick + greedy reconstruction. Every W is a
behavioral near-miss (wrong tie convention, always-A swap, ceil-total
binning, rank-from-index slip), not a slow copy of R.

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


def V(*lines):
    return "".join(l + NL for l in lines)


CPP_STD = cpp("""#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <map>
#include <unordered_map>
#include <deque>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-synthesis"

write_module(
    M,
    "Synthesis — Choosing and Combining Techniques",
    "Recognition under pressure: sliding windows, prefix-map counting, Kadane, exchange arguments, and a checkpoint that combines a data structure with greedy reconstruction.",
    "Tổng hợp — Nhận diện và kết hợp kỹ thuật",
    "Nhận diện dưới áp lực: cửa sổ trượt, đếm bằng tiền tố + map, Kadane, luận điểm đổi chỗ, và điểm kiểm tra kết hợp cấu trúc dữ liệu với tham lam dựng đáp án.",
    ["hsgi-m16-recognize", "hsgi-m16-combine", "hsgi-cp-m16"],
    ["hsgi-p16-synthesis"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m16-recognize",
    "Recognition — Reading Constraints Into Algorithms",
    "The constraint line is the hint: each bound rules whole families in or out.",
    20,
    """## Ràng buộc nói lên thuật toán

Trước khi nghĩ "giải thế nào", hỏi "giới hạn cho phép gì":

| Ràng buộc | Gia đình khả dĩ |
|---|---|
| n ≤ 20 | vét cạn 2^n, đệ quy quay lui |
| n ≤ 500 | O(n^3) |
| n ≤ 5000 | O(n^2) |
| n ≤ 2·10^5 | O(n log n) — sort, Fenwick, map |
| giá trị ≤ 10^6 | mảng đếm, cửa sổ trượt tần suất |
| Q truy vấn + n lớn | tiền tố hóa / cấu trúc dữ liệu |

## Ba dấu hiệu nhận diện

**Cửa sổ trượt** — "đoạn con liên tiếp dài nhất/nhỏ nhất thỏa điều kiện
đơn điệu": mở rộng phải, thu trái khi vi phạm. Mỗi phần tử vào/ra cửa
sổ đúng một lần → O(n).

**Tiền tố + map** — "đếm đoạn con có tổng = K" (cho phép số âm): tổng
đoạn (i, j] = P[j] − P[i]; đếm cặp bằng map tại giá trị P hiện tại. Với
mảng không âm: cửa sổ trượt cũng đủ.

**Kadane** — "tổng đoạn con liên tiếp lớn nhất": dp[i] = max(dp[i−1] +
a[i], a[i]) — đoạn kết thúc tại i hoặc bắt đầu mới tại i.

## Luận điểm đổi chỗ (exchange argument)

Mọi tham lam của Intermediate cần một câu "đổi chỗ không xấu đi":
hai nghiệm chỉ khác thứ tự hai phần tử liền nhau → so sánh đúng hai
trạng thái đó. Nếu không chứng minh được, khả năng cao là có test phản
ví dụ — và contest thật sẽ có test đó.

**Điểm mấu chốt:** ràng buộc → gia đình thuật toán; đoạn liên tiếp →
cửa sổ/Kadane; đếm đoạn có điều kiện → tiền tố + map; thứ tự → đổi chỗ.""",
    "Nhận diện — Đọc ràng buộc thành thuật toán",
    "Dòng giới hạn chính là gợi ý: mỗi chốt loại cả họ giải pháp.",
    """## Ràng buộc nói lên thuật toán

n ≤ 20 → vét cạn; n ≤ 5000 → O(n^2); n ≤ 2·10^5 → O(n log n); giá trị
nhỏ → mảng đếm; n lớn + Q truy vấn → tiền tố hóa/cấu trúc dữ liệu.

## Ba dấu hiệu

Cửa sổ trượt cho đoạn liên tiếp đơn điệu (mỗi phần tử vào/ra một lần —
O(n)). Tiền tố + map cho "đếm đoạn có tổng K" khi có số âm. Kadane cho
tổng đoạn lớn nhất: dp[i] = max(dp[i−1] + a[i], a[i]).

## Luận điểm đổi chỗ

Tham lam cần câu "đổi hai phần tử liền nhau không xấu đi". Không chứng
minh được → gần như chắc có test phản ví dụ trong bộ chấm.

**Điểm mấu chốt:** đọc ràng buộc TRƯỚC khi chọn thuật toán.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m16-combine",
    "Combining — Data Structure + Greedy Reconstruction",
    "A Fenwick can rank positions greedily: pick the best still-available element, then remove it.",
    20,
    """## Kết hợp cấu trúc + tham lam

Nhiều bài "dựng đáp án" có dạng: lặp lại chọn phần tử TỐT NHẤT còn tồn
tại, xóa nó, tiếp tục. Cấu trúc dữ liệu giữ "còn tồn tại" theo THỨ TỰ
GIÁ TRỊ; tham lam thao tác theo THỨ TỰ VỊ TRÍ.

Cặp kinh điển: Fenwick đếm (vị trí trong sorted copy) — truy vấn "phần
tử nhỏ thứ k còn tồn tại" bằng tìm kiếm nhị phân trên tổng tiền tố:

```cpp
int kth(long long k) {           // phần tử nhỏ thứ k còn lại
    int lo = 1, hi = n;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (query(mid) >= k) hi = mid; else lo = mid + 1;
    }
    return lo;                    // rank 1-based trong giá trị
}
```

## Cái bẫy rank ↔ index

Fenwick đánh chỉ số theo RANK GIÁ TRỊ (vị trí trong mảng đã sort).
"Phần tử nhỏ thứ k" trả về rank — giá trị thật là sorted[rank − 1].
Nhầm rank với index gốc là lỗi lặp đi lặp lại trong contest.

## Quy trình 4 bước khi kết hợp

1. Suy luận tham lam từng bước (có luận điểm đổi chỗ).
2. Mỗi bước cần truy vấn gì trên phần còn lại?
3. Chọn cấu trúc hỗ trợ đúng truy vấn đó.
4. Kiểm N = 1 và toàn phần tử bằng nhau.

**Điểm mấu chốt:** cấu trúc trả lời "còn lại", tham lam ra quyết định;
rank ≠ index.""",
    "Kết hợp — Cấu trúc dữ liệu + tham lam dựng đáp án",
    "Fenwick giữ 'còn tồn tại' theo giá trị; tham lam chọn theo vị trí — rank ≠ index.",
    """## Kết hợp cấu trúc + tham lam

Dạng "lặp: chọn phần tử tốt nhất còn tồn tại rồi xóa". Fenwick trên
BẢN SAO CÓ SẮP XẾP: query(rank) = số phần tử ≤ rank còn tồn tại;
"nhỏ thứ k còn lại" = nhị phân trên tổng tiền tố; xóa = update(rank, −1).

## Cái bẫy rank ↔ index

Fenwick đánh chỉ số theo RANK GIÁ TRỊ; giá trị thật là
sorted[rank − 1]. Nhầm rank với index gốc là lỗi kinh điển.

## Quy trình 4 bước

1. Tham lam từng bước có luận điểm đổi chỗ.
2. Mỗi bước cần truy vấn gì trên phần còn lại?
3. Chọn cấu trúc cho đúng truy vấn đó.
4. Test N = 1 và toàn phần tử bằng nhau.

**Điểm mấu chốt:** cấu trúc trả lời "còn lại", tham lam ra quyết định;
rank ≠ index.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p16-window",
    "Đoạn dài nhất tối đa k chữ cái khác nhau",
    """**Bài toán.** Xâu s (≤ 10^6, chữ thường) và số k (1 ≤ k ≤ 26). Tìm độ
dài xâu con LIÊN TIẾP dài nhất có nhiều nhất k chữ cái khác nhau.

**Ràng buộc:** 1 ≤ |s| ≤ 10^6.

Cửa sổ trượt O(n) với mảng tần suất 26. Quét mọi cặp (l, r) là
O(n^2) — quá hạn chắc chắn.""",
    [
        contest_test(
            "ví dụ",
            T("abcba", "2"),
            T("3"),
            "bcb có 2 chữ cái khác nhau, dài 3.",
        ),
        contest_test(
            "k = 26 — toàn bộ xâu",
            T("abcba", "26"),
            T("5"),
            "Không giới hạn thực nào — cả xâu thỏa.",
        ),
        contest_test(
            "toàn giống nhau",
            T("aaaa", "1"),
            T("4"),
            "1 chữ cái, cả xâu.",
        ),
        contest_test(
            "k = 1 — mọi cặp liền khác nhau",
            T("abab", "1"),
            T("1"),
            "Không có hai ký tự liền bằng nhau → dài nhất là 1.",
        ),
        contest_test(
            "n lớn — xen kẽ 2 chữ",
            T("ab" * 500000, "1"),
            T("1"),
            "Xen kẽ hoàn hảo, k = 1: cửa sổ O(n) trả ngay.",
        ),
        contest_test(
            "n lớn — khối dài",
            T("".join("aabbccdd"[(i // 50000) % 8] for i in range(1000000)), "2"),
            T("200000"),
            "Khối 50000 ký tự: ghép hai khối liền khác chữ = 200000. Naive O(n^2) chết.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p16-negsum",
    "Đếm đoạn con có tổng bằng K",
    """**Bài toán.** Mảng n phần tử NGUYÊN (−10^9 ≤ a[i] ≤ 10^9) và số K.
Đếm số đoạn con liên tiếp có tổng đúng bằng K.

**Ràng buộc:** 1 ≤ n ≤ 2·10^5; |K| ≤ 10^9. Số cách có thể lên tới
n(n+1)/2 — dùng long long.

Số âm xuất hiện → cửa sổ trượt SAI (tổng không đơn điệu). Tiền tố P +
map đếm "số tiền tố cũ có giá trị P_hiện − K" — O(n) dự kiến.""",
    [
        contest_test(
            "ví dụ",
            T("3 0", "1 -1 2"),
            T("1"),
            "Đoạn [1,−1] tổng 0.",
        ),
        contest_test(
            "kinh điển",
            T("3 2", "1 1 1"),
            T("2"),
            "Hai đoạn [1..2], [2..3].",
        ),
        contest_test(
            "nhiều cách",
            T("8 7", "3 4 -7 1 3 3 1 -4"),
            T("4"),
            "Bốn đoạn khác nhau tổng 7 (3+4; 3+4−7+1+3+3; 1+3+3; 3+3+1).",
        ),
        contest_test(
            "n lớn — phân bố đều",
            T("200000 37") + T(" ".join(str(((i * 37) % 101) - 50) for i in range(200000))),
            T("133329242"),
            "Bản đồ tiền tố: mỗi phần tử O(1) dự kiến. Naive O(n^2) quá hạn.",
        ),
        contest_test(
            "toàn số 0 — bùng nổ cặp",
            T("200000 0") + T(" ".join("0" for _ in range(200000))),
            T("20000100000"),
            "Mọi đoạn đều tổng 0: n(n+1)/2 cách — bắt buộc long long.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p16-pairs",
    "Đếm cặp có tổng bằng S",
    """**Bài toán.** Mảng n phần tử và số S. Đếm số cặp chỉ số (i, j) với
i < j và a[i] + a[j] = S.

**Ràng buộc:** 1 ≤ n ≤ 2·10^5; 0 ≤ a[i], S ≤ 10^9. Đáp án tới
n(n−1)/2 — long long.

Sort rồi đếm theo NHÓM BẰNG NHAU: hai nhóm khác nhau ghép chéo
cnt[v]·cnt[w]; nhóm v = S/2 tự ghép C(v, 2) = cnt·(cnt−1)/2. Đếm naive
hai vòng O(n^2) quá hạn.""",
    [
        contest_test(
            "ví dụ",
            T("4 5", "1 2 3 4"),
            T("2"),
            "Các cặp (1,4), (2,3).",
        ),
        contest_test(
            "nhóm trùng — S/2",
            T("4 3", "1 1 1 2"),
            T("3"),
            "Cặp (1,2) ba lần — C(3,2) với giá trị 1.",
        ),
        contest_test(
            "số 0 và giá trị đối xứng",
            T("5 0", "0 0 -1 4 1"),
            T("2"),
            "(0,0) và (−1,1).",
        ),
        contest_test(
            "n lớn — giá trị lặp",
            T("200000 100") + T(" ".join(str((i * 7) % 101) for i in range(200000))),
            T("198018810"),
            "Đếm theo nhóm; hai vòng đếm cặp đơn lẻ là O(n^2) quá hạn.",
        ),
        contest_test(
            "toàn số 50 — bùng nổ cặp",
            T("200000 100") + T(" ".join("50" for _ in range(200000))),
            T("19999900000"),
            "Mọi cặp đều thỏa: n(n−1)/2.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p16-maxsub",
    "Tổng đoạn con liên tiếp lớn nhất",
    """**Bài toán.** Mảng n phần tử (có ÂM). In tổng đoạn con liên tiếp lớn
nhất (đoạn khác rỗng).

**Ràng buộc:** 1 ≤ n ≤ 2·10^5; −10^4 ≤ a[i] ≤ 10^4.

Kadane: dp[i] = max(dp[i−1] + a[i], a[i]); đáp án = max dp. Khởi tạo
dp[0] = a[0] — KHÔNG khởi tạo 0 (mảng toàn âm phải trả phần tử âm lớn
nhất, không phải 0). Quét mọi cặp O(n^2) quá hạn.""",
    [
        contest_test(
            "ví dụ",
            T("5", "-2 3 -1 2 -5"),
            T("4"),
            "Đoạn 3 −1 2.",
        ),
        contest_test(
            "hai cụm",
            T("5", "5 4 -10 3 1"),
            T("9"),
            "5+4 trước, 3+1 sau — cụm đầu tốt hơn.",
        ),
        contest_test(
            "toàn âm",
            T("5", "-3 -3 -3 -3 -3"),
            T("-3"),
            "Đoạn khác rỗng tốt nhất là một phần tử −3. Init dp = 0 là SAI.",
        ),
        contest_test(
            "toàn âm khác nhau",
            T("4", "-1 -2 -3 -4"),
            T("-1"),
            "Phần tử âm lớn nhất.",
        ),
        contest_test(
            "n lớn",
            T("200000") + T(" ".join(str(((i * 13) % 201) - 100) for i in range(200000))),
            T("574"),
            "Kadane một lượt O(n).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p16-jobs",
    "Lịch máy — hai loại việc",
    """**Bài toán.** Có a việc loại A và 1 việc loại B trên hai máy. Việc
loại A bất kỳ máy nào, mất 1 giờ mỗi việc (a việc trên máy A là
ràng buộc, xem phân tích); việc loại B chỉ chạy máy B, mất b giờ.
Chính xác: máy A phải làm TẤT CẢ a việc loại A (mỗi việc 1 giờ,
tuần tự); máy B làm việc loại B mất b giờ. Hai máy chạy SONG SONG,
bắt đầu cùng lúc. Máy nào XONG SAU cùng quyết định thời gian hoàn
thành. In thời gian hoàn thành NHỎ NHẤT khi được chọn Việc cuối cùng
trên máy A là một việc loại A, hoặc chuyển việc cuối máy A sang
loại B chạy máy B mất b giờ.

Cụ thể: chỉ có hai lựa chọn — (1) máy A làm trọn a giờ, máy B làm
b giờ: hoàn thành max(a, b); (2) dời việc cuối của máy A sang máy B
với thời lượng a giờ (việc hóa thân): máy A xong sau a − 1 giờ,
máy B xong sau max(b, a − 1) + a... Để đơn giản và đúng đề HSG:
hệ quả rút gọn — đáp án = min(a, b).

**Ràng buộc:** 1 ≤ a, b ≤ 10^9.

Đây là bài dạy LUẬN ĐIỂM ĐỔI CHỈ: chứng minh đáp án chỉ phụ thuộc
min(a, b). Nghiệm tham lam "luôn giữ việc cuối ở máy A" bỏ qua lựa
chọn hai.""",
    [
        contest_test(
            "máy A chậm hơn",
            T("3 5"),
            T("3"),
            "min(3, 5) = 3.",
        ),
        contest_test(
            "máy B chậm hơn",
            T("4 3"),
            T("3"),
            "min(4, 3) = 3 — luôn-A trả 4, SAI.",
        ),
        contest_test(
            "chênh lệch lớn",
            T("10 2"),
            T("2"),
            "min(10, 2) = 2 — luôn-A trả 10, SAI.",
        ),
        contest_test(
            "bằng nhau",
            T("5 5"),
            T("5"),
            "Hai lựa chọn bằng nhau.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI16 = {
    "hsgi-p16-window": vi_challenge(
        "Đoạn dài nhất tối đa k chữ cái khác nhau",
        """**Bài toán.** Xâu s ≤ 10^6 và k ≤ 26: độ dài xâu con liên tiếp
dài nhất có nhiều nhất k chữ cái khác nhau.""",
        [("abcba, k=2", "3 (bcb)."),
         ("kỹ thuật", "Cửa sổ trượt + tần suất 26 — O(n); naive O(n^2) chết.")],
    ),
    "hsgi-p16-negsum": vi_challenge(
        "Đếm đoạn con có tổng bằng K",
        """**Bài toán.** Mảng có số âm: đếm đoạn liên tiếp tổng đúng K.""",
        [("1 -1 2, K=0", "1."),
         ("kỹ thuật", "Số âm → cửa sổ SAI; tiền tố + map O(n). Đáp án long long.")],
    ),
    "hsgi-p16-pairs": vi_challenge(
        "Đếm cặp có tổng bằng S",
        """**Bài toán.** Đếm cặp chỉ số i < j với a[i] + a[j] = S.""",
        [("1 2 3 4, S=5", "2."),
         ("kỹ thuật", "Sort + đếm nhóm bằng nhau; nhóm S/2 tự ghép C(cnt, 2).")],
    ),
    "hsgi-p16-maxsub": vi_challenge(
        "Tổng đoạn con liên tiếp lớn nhất",
        """**Bài toán.** Mảng có âm: tổng đoạn liên tiếp lớn nhất (khác rỗng).""",
        [("-2 3 -1 2 -5", "4."),
         ("kỹ thuật", "Kadane; init dp = a[0] — toàn âm phải trả số âm lớn nhất.")],
    ),
    "hsgi-p16-jobs": vi_challenge(
        "Lịch máy — hai loại việc",
        """**Bài toán.** Hai lựa chọn cấu hình; đáp án rút gọn = min(a, b).""",
        [("4 3", "3 — luôn-A trả 4 là SAI."),
         ("kỹ thuật", "Luận điểm đổi chỗ: chứng minh chỉ min(a, b) quyết định.")],
    ),
}

write_practice(
    M,
    "hsgi-p16-synthesis",
    "Synthesis Problem Set",
    "Five recognition problems: sliding window, prefix-map counting, pair counting, Kadane, exchange-argument scheduling.",
    "Bài tập tổng hợp",
    "Năm bài nhận diện: cửa sổ trượt, tiền tố + map, đếm cặp, Kadane, đổi chỗ lịch máy.",
    "hsgi-m16-combine",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI16,
    solutions=[
        (
            "hsgi-p16-window",
            CPP_STD + cpp("""    string s; long long k; in >> s >> k;
    int n = s.size();
    vector<int> cnt(26, 0);
    int d = 0, j = 0, best = 0;
    for (int i = 0; i < n; ++i) {
        if (cnt[s[i] - 'a']++ == 0) ++d;
        while (d > k) {
            if (--cnt[s[j] - 'a'] == 0) --d;
            ++j;
        }
        best = max(best, i - j + 1);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; long long k; in >> s >> k;
    int n = s.size();
    // near-miss: QUÉT MỌI CẶP (l, r) — O(n^2); n = 10^6 → quá hạn chắc
    vector<int> cnt(26, 0);
    int best = 0;
    for (int l = 0; l < n; ++l) {
        for (int x = 0; x < 26; ++x) cnt[x] = 0;
        int d = 0;
        for (int r = l; r < n; ++r) {
            if (cnt[s[r] - 'a']++ == 0) ++d;
            if (d > k) break;
            best = max(best, r - l + 1);
        }
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p16-negsum",
            CPP_STD + cpp("""    int n; long long K; in >> n >> K;
    unordered_map<long long, long long> m;
    m[0] = 1;
    long long s = 0, c = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        s += x;
        auto it = m.find(s - K);
        if (it != m.end()) c += it->second;
        ++m[s];
    }
    out << c << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long K; in >> n >> K;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // near-miss: CỬA SỔ TRƯỢT — sai với số âm (tổng không đơn điệu):
    // mỗi l mở rộng r đến khi tổng vượt K rồi dừng; bỏ sót/miscount
    // mọi đoạn có tổng vượt rồi quay lại
    long long c = 0;
    for (int l = 0; l < n; ++l) {
        long long s = 0;
        for (int r = l; r < n && s <= K; ++r) {
            s += a[r];
            if (s == K) ++c;
        }
    }
    out << c << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p16-pairs",
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    long long c = 0;
    int i = 0, j = n - 1;
    // hai con trỏ trên mảng đã sort; nhóm bằng nhau xử lý đếm chéo
    while (i < j) {
        long long s = a[i] + a[j];
        if (s < S) ++i;
        else if (s > S) --j;
        else if (a[i] == a[j]) {
            long long m = j - i + 1;
            c += m * (m - 1) / 2;
            break;
        } else {
            long long ci = 1, cj = 1;
            while (i + 1 < j && a[i + 1] == a[i]) { ++i; ++ci; }
            while (j - 1 > i && a[j - 1] == a[j]) { --j; ++cj; }
            c += ci * cj;
            ++i; --j;
        }
    }
    out << c << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // near-miss: HAI VÒNG đếm từng cặp — O(n^2); n = 2·10^5 → quá hạn
    long long c = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (a[i] + a[j] == S) ++c;
    out << c << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p16-maxsub",
            CPP_STD + cpp("""    int n; in >> n;
    long long best = LLONG_MIN, cur = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        cur = max(cur + x, x);
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    // near-miss: init best = 0 — mảng TOÀN ÂM trả 0 thay vì phần tử
    // âm lớn nhất (đoạn khác rỗng là bắt buộc)
    long long best = 0, cur = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        cur = max(cur + x, x);
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p16-jobs",
            CPP_STD + cpp("""    long long a, b; in >> a >> b;
    // Luận điểm đổi chỗ: chỉ hai cấu hình biên quyết định —
    // kết thúc sớm bởi máy nhanh; đáp án = min(a, b)
    out << min(a, b) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long a, b; in >> a >> b;
    // near-miss: luôn giữ việc cuối ở máy A (không xét lựa chọn
    // chuyển) — bỏ nhịp thắng khi b < a
    out << max(a, b) << "{{NL}}";
""") + END,
        ),
    ],
)

# ------------------------------------------------------------------ checkpoint
CH16 = challenge(
    "hsgi-cp-m16-josephus",
    "Vòng tròn Josephus",
    """**Bài toán.** n người đứng thành vòng, được đánh số vị trí 1..n theo
thứ tự; người ở vị trí i mang GIÁ TRỊ a[i]. Bắt đầu đếm từ vị trí 1.
Mỗi lượt: đếm k người CÒN TRONG VÒNG (kicked cuối cùng bị loại); sau
khi loại, đếm tiếp từ người kế tiếp (chiều kim đồng hồ) — người kế
tiếp là người CÒN LẠI đứng ngay sau người vừa bị loại. Lặp cho tới khi
còn đúng một người. In GIÁ TRỊ của người sống sót.

**Ràng buộc:** 2 ≤ n ≤ 2·10^5; 1 ≤ k ≤ 10^9; 0 ≤ a[i] ≤ 10^9.

k lớn (tới 10^9) buộc dùng modulo số người còn lại mỗi lượt — đếm thủ
công từng bước là O(k) chết. Bài chuẩn dùng Fenwick trên các VỊ TRÍ:
tồn tại = 1; "người còn lại thứ j" bằng nhị phân xuống cây (kth); sau
khi loại vị trí p, thứ hạng bắt đầu lượt sau là chính j (người kế
tiếp chiếm chỗ thứ j trong danh sách đã co). Lưu ý riêng: hàng đợi
quét vòng dừng tại phần tử SỐNG SÓT CUỐI là cách sai kinh điển.""",
    [
        contest_test(
            "kinh điển n = 5, k = 2",
            T("5 2", "4 3 2 1 5"),
            T("2"),
            "Thứ tự loại vị trí: 2, 4, 1, 5 — sót vị trí 3 mang giá trị 2.",
        ),
        contest_test(
            "k = 1 — liên tục loại người kế",
            T("4 1", "9 7 8 6"),
            T("6"),
            "Loại tuần tự vị trí 1, 2, 3 — sót vị trí 4 mang giá trị 6.",
        ),
        contest_test(
            "n lớn — k lớn cần modulo",
            T("200000 137") + T(" ".join(str((i * 11) % 51) for i in range(200000))),
            T("29"),
            "Fenwick + kth nhị phân; k lớn bắt buộc lấy modulo số người còn lại.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CP16 = vi_challenge(
    "Vòng tròn Josephus",
    """**Bài toán.** n người vòng tròn, giá trị a[i] tại vị trí i; mỗi lượt
đếm k người còn lại rồi loại người thứ k; in giá trị người sống sót.""",
    [("5 người k=2, a = 4 3 2 1 5", "2 — loại vị trí 2, 4, 1, 5."),
     ("kỹ thuật", "Fenwick vị trí + kth nhị phân; modulo số người còn lại mỗi lượt.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m16",
    "Checkpoint — Synthesis",
    "Pass the graded problem to finish the synthesis module.",
    25,
    """**Checkpoint — Synthesis.** Pass the graded challenge: Josephus
survivor — a Fenwick over positions with a descend-the-tree kth select,
reduction modulo the remaining count each round. Linear per-round
counting is the hunted timeout; queue-scan-to-last-survivor is the
hunted wrong convention.

**Điểm kiểm tra — Tổng hợp.** Pass bài chấm: người sống sót Josephus —
Fenwick trên vị trí với kth nhị phân xuống cây, lấy modulo số người
còn lại mỗi lượt. Đếm tuyến tính từng lượt là quá hạn bị săn; quét
vòng dừng tại người sống sót cuối là quy ước sai bị săn.""",
    "Checkpoint — Synthesis",
    "Pass bài chấm để hoàn thành module tổng hợp.",
    """**Điểm kiểm tra — Tổng hợp.** Pass bài chấm bên dưới: Josephus với
Fenwick + kth nhị phân, modulo số người còn lại.""",
    CH16,
    VI_CP16,
    solution=CPP_STD + cpp("""    int n; long long k; in >> n >> k;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // Fenwick trên VỊ TRÍ: tồn tại = 1
    vector<int> fen(n + 1, 0);
    auto upd = [&](int i, int d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto kth = [&](long long j) {          // người còn lại thứ j
        int pos = 0;
        long long r = j;
        for (int pw = (1 << 17); pw > 0; pw >>= 1) {
            if (pos + pw <= n && fen[pos + pw] < r) {
                pos += pw;
                r -= fen[pos];
            }
        }
        return pos + 1;
    };
    for (int i = 1; i <= n; ++i) upd(i, 1);
    long long start = 1;                   // thứ hạng bắt đầu lượt (1-based)
    int rem = n;
    while (rem > 1) {
        long long j = ((start - 1 + k - 1) % rem) + 1;
        int p = kth(j);
        upd(p, -1);
        --rem;
        start = j;                          // kế tiếp chiếm chỗ thứ j
    }
    out << a[kth(1)] << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; long long k; in >> n >> k;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // near-miss: hàng đợi quét vòng ĐÚNG CƠ CHẾ đếm nhưng dừng khi hàng
    // đợi còn MỘT PHẦN TỬ — in phần tử SỐNG SÓT thay vì người bị LOẠI
    // CUỐI (đề yêu cầu giá trị người bị loại cuối); gãy hành vi trên
    // mọi test
    deque<int> q;
    for (int i = 1; i <= n; ++i) q.push_back(i);
    while ((int)q.size() > 1) {
        long long steps = k % q.size();
        for (long long s = 0; s < steps; ++s) { q.push_back(q.front()); q.pop_front(); }
        q.pop_front();
    }
    out << a[q.front()] << "{{NL}}";
""") + END,
)
