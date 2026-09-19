#!/usr/bin/env python3
"""HSG Intermediate — Module 2: hsgi-binsearch (binary search mastery).

lower_bound/upper_bound as first-class tools, counting occurrences, the
monotonic predicate F(x) = "x is feasible", and binary search ON THE ANSWER.
Near-misses are the classic boundary diseases: r-1 instead of r-2^k-style
window errors, l <= r with wrong mid adjustment (infinite loop family),
and "ans never updated" predicates.
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

M = "hsgi-binsearch"
write_module(
    M,
    "Binary Search Mastery — From Arrays to the Answer",
    "lower_bound and upper_bound as precision tools, occurrence counting, the monotonic predicate, and binary searching the answer itself with an honest feasibility check.",
    "Tìm kiếm nhị phân chuyên sâu — Từ mảng đến đáp án",
    "lower_bound và upper_bound như công cụ chính xác, đếm số lần xuất hiện, vị từ đơn điệu, và tìm kiếm nhị phân trên chính đáp án với hàm kiểm tra trung thực.",
    ["hsgi-m2-bounds", "hsgi-m2-answer", "hsgi-cp-m2"],
    ["hsgi-p2-binsearch"],
)

# ---------------------------------------------------------------- lesson 2.1
write_lesson(
    M,
    "hsgi-m2-bounds",
    "lower_bound, upper_bound, and Counting",
    "The two half-open iterators, their exact meanings, and the three counting idioms built from them.",
    15,
    """## The two bounds — precise meanings

On a sorted range, `lower_bound(x)` points to the **first element ≥ x**;
`upper_bound(x)` points to the **first element > x**. Everything else is
derived:

```cpp
int lo = lower_bound(v.begin(), v.end(), x) - v.begin();  // # of elements < x
int up = upper_bound(v.begin(), v.end(), x) - v.begin();  // # of elements <= x
int cnt = up - lo;                                        // # of elements == x
bool present = (lo < n && v[lo] == x);
```

Three idioms worth drilling:
1. **range [a, b] count** = `upper_bound(b) − lower_bound(a)`.
2. **predecessor** (largest element ≤ x) = `upper_bound(x) − 1` — check the
   iterator did not move before subtracting.
3. **successor** (smallest element ≥ x) = `lower_bound(x)` — check against
   `end()`.

### Hand-rolled binary search — the two loop shapes

```cpp
// Shape A: find first index with a[i] >= x (the lower_bound skeleton)
int l = 0, r = n;              // half-open [l, r)
while (l < r) {
    int mid = l + (r - l) / 2;
    if (a[mid] >= x) r = mid; else l = mid + 1;
}
// l == r == answer (n if none)
```

```cpp
// Shape B: maximize ans where F(ans) holds on [lo, hi] (monotonic!)
int l = lo, r = hi;            // closed [l, r]
while (l < r) {
    int mid = l + (r - l + 1) / 2;   // CEILING mid — kills the l=mid loop
    if (F(mid)) l = mid; else r = mid - 1;
}
// l == r == largest feasible value
```

The two classic diseases:
- **floor mid with `l = mid`** → infinite loop when `r = l + 1`.
- **`r = mid` with closed bounds and floor mid** → skips `r` itself, may
  miss the answer sitting at the boundary.

Decide the shape FIRST, then never mix pieces across shapes.

### Counting inside a window

"Trong dãy đã sắp, có bao nhiêu phần tử trong [l, r]?" — with values, use the
two bounds. With *positions*, same thing: the answer is `up − lo + ... ` —
no, positions are already sorted, it is plain index arithmetic. Recognizing
*what is sorted* is half the problem.

## Practice recognition

Q: "mảng đã sắp, truy vấn: phần tử lớn nhất ≤ x" — which idiom?
A: `upper_bound(x)`; if it returned `begin()`, answer "không có".

**Next:** [Binary Search on the Answer](./hsgi-m2-answer)""",
    "lower_bound, upper_bound, và Đếm",
    "Hai iterator nửa mở với ý nghĩa chính xác, và ba thành ngữ đếm dựng từ chúng.",
    """## Hai đường biên — ý nghĩa chính xác

Trên dãy đã sắp, `lower_bound(x)` trỏ tới **phần tử đầu ≥ x**;
`upper_bound(x)` trỏ tới **phần tử đầu > x**. Mọi thứ khác suy ra được:

```cpp
int lo = lower_bound(v.begin(), v.end(), x) - v.begin();  // số phần tử < x
int up = upper_bound(v.begin(), v.end(), x) - v.begin();  // số phần tử <= x
int cnt = up - lo;                                        // số phần tử == x
bool present = (lo < n && v[lo] == x);
```

Ba thành ngữ cần thuộc:
1. **đếm trong đoạn giá trị [a, b]** = `upper_bound(b) − lower_bound(a)`.
2. **tiền nhiệm** (phần tử lớn nhất ≤ x) = `upper_bound(x) − 1` — kiểm tra
   iterator đã dịch chuyển trước khi trừ.
3. **hậu nhiệm** (phần tử nhỏ nhất ≥ x) = `lower_bound(x)` — kiểm tra với
   `end()`.

### Tìm nhị phân tự viết — hai khuôn vòng lặp

```cpp
// Khuôn A: tìm chỉ số đầu có a[i] >= x (bộ khung lower_bound)
int l = 0, r = n;              // nửa mở [l, r)
while (l < r) {
    int mid = l + (r - l) / 2;
    if (a[mid] >= x) r = mid; else l = mid + 1;
}
// l == r == đáp án (n nếu không có)
```

```cpp
// Khuôn B: cực đại hóa ans sao cho F(ans) đúng trên [lo, hi] (đơn điệu!)
int l = lo, r = hi;            // đóng [l, r]
while (l < r) {
    int mid = l + (r - l + 1) / 2;   // mid TRẦN — diệt vòng lặp l=mid
    if (F(mid)) l = mid; else r = mid - 1;
}
// l == r == giá trị khả thi lớn nhất
```

Hai bệnh kinh điển:
- **mid sàn với `l = mid`** → lặp vô hạn khi `r = l + 1`.
- **`r = mid` với biên đóng và mid sàn** → bỏ qua chính `r`, có thể mất đáp án
  nằm ngay biên.

Chọn khuôn TRƯỚC, rồi không bao giờ trộn linh kiện giữa hai khuôn.

### Đếm bên trong cửa sổ

"Trong dãy đã sắp, có bao nhiêu phần tử trong [l, r]?" — với *giá trị*, dùng
hai đường biên. Với *vị trí*, dãy vị trí đã sắp sẵn — chỉ là số học chỉ số.
Nhận ra **cái gì đã sắp** là một nửa bài toán.

## Luyện nhận diện

H: "mảng đã sắp, truy vấn: phần tử lớn nhất ≤ x" — thành ngữ nào?
Đ: `upper_bound(x)`; nếu trả về `begin()` thì đáp án "không có".

**Tiếp:** [Tìm kiếm nhị phân trên đáp án](./hsgi-m2-answer)""",
)

# ---------------------------------------------------------------- lesson 2.2
write_lesson(
    M,
    "hsgi-m2-answer",
    "Binary Search on the Answer",
    "Recognize the monotonic-feasibility pattern, write an honest check(x), and tune its complexity.",
    17,
    """## The pattern

The answer is a *number*, and feasibility is **monotonic**: if x works, every
x' ≤ x works (minimization) or every x' ≥ x works (maximization). Then binary
search the answer over its range.

Signatures that scream "binary search on answer":
- "tối thiểu hóa khoảng cách lớn nhất", "tối đa hóa khoảng cách nhỏ nhất"
- "chia thành k phần sao cho phần lớn nhất nhỏ nhất"
- "đặt m trạm sao cho khoảng cách tối thiểu lớn nhất"
- ANY "min-max" / "max-min" phrasing

### Worked example — aggressive signal placement

"n vị trí trục, đặt c trạm, khoảng cách giữa hai trạm gần nhau nhất phải lớn
nhất có thể."

F(d) = "đặt được ≥ c trạm, mỗi trạm cách trạm trước ≥ d" — greedy: place the
first at the leftmost point, then always the next point ≥ last + d. O(n) per
check, monotonic (nếu đặt được với khoảng cách d thì đặt được với d' < d) →
binary search d.

```cpp
bool F(long long d) {
    int placed = 1;
    long long last = a[0];
    for (int i = 1; i < n; ++i)
        if (a[i] - last >= d) { ++placed; last = a[i]; }
    return placed >= c;
}
// Shape B over d in [1, a[n-1] - a[0]]
```

### The check must be HONEST

Two ways students cheat `check(x)`:
1. **Silent approximation** — "đủ gần đúng là được". The check must be the
   *exact* decision procedure for the reduced problem, or the search converges
   to garbage. The garbage is silent: no crash, just wrong answers on
   adversarial tests.
2. **Wrong complexity** — a check that is O(n^2) turns the whole thing into
   O(n^2 log n). Compute it: n = 10^5 → 10^10 · 17 — dead. The check needs to
   fit the same budget logic as everything else.

### What binary search on answer is NOT for

- Non-monotonic feasibility (then: sweep, DP, or parametric search — Advanced).
- When the answer is not a simple number but a structure (then: constructive /
  greedy with proof — M4).

**Next:** [Checkpoint](./hsgi-cp-m2)""",
    "Tìm kiếm nhị phân trên đáp án",
    "Nhận diện mẫu khả thi-đơn điệu, viết hàm check(x) trung thực, và tính đúng độ phức tạp của nó.",
    """## Mẫu bài

Đáp án là một *con số*, và tính khả thi **đơn điệu**: nếu x thỏa thì mọi
x' ≤ x thỏa (bài tối thiểu hóa) hoặc mọi x' ≥ x thỏa (bài tối đa hóa). Khi đó
tìm nhị phân đáp án trên đoạn giá trị của nó.

Dấu hiệu hô to "tìm nhị phân trên đáp án":
- "tối thiểu hóa khoảng cách lớn nhất", "tối đa hóa khoảng cách nhỏ nhất"
- "chia thành k phần sao cho phần lớn nhất nhỏ nhất"
- "đặt m trạm sao cho khoảng cách tối thiểu lớn nhất"
- MỌI cách diễn đạt dạng "min-max" / "max-min"

### Ví dụ làm mẫu — đặt trạm thông minh

"n vị trí trên trục, đặt c trạm, khoảng cách giữa hai trạm gần nhau nhất phải
lớn nhất có thể."

F(d) = "đặt được ≥ c trạm, mỗi trạm cách trạm trước ≥ d" — tham lam: đặt trạm
đầu ở điểm trái nhất, sau đó luôn chọn điểm ≥ trạm trước + d. O(n) mỗi lần
check, đơn điệu (đặt được với d thì đặt được với d' < d) → tìm nhị phân d.

```cpp
bool F(long long d) {
    int placed = 1;
    long long last = a[0];
    for (int i = 1; i < n; ++i)
        if (a[i] - last >= d) { ++placed; last = a[i]; }
    return placed >= c;
}
// Khuôn B trên d trong [1, a[n-1] - a[0]]
```

### Hàm check phải TRUNG THỰC

Hai kiểu gian lận trong `check(x)`:
1. **Xấp xỉ trong im lặng** — "đủ gần đúng là được". Check phải là thủ tục
   quyết định *chính xác* cho bài con, nếu không tìm nhị phân hội tụ về kết
   quả rác. Rác này im lặng: không crash, chỉ sai trên test mốc.
2. **Sai độ phức tạp** — check O(n^2) biến mọi thứ thành O(n^2 log n).
   Tính: n = 10^5 → 10^10 · 17 — chết. Check cũng phải nằm trong cùng ngân
   sách như mọi thứ khác.

### Khi nào KHÔNG dùng tìm nhị phân trên đáp án

- Tính khả thi không đơn điệu (khi đó: quét, DP, hoặc tham số hóa — Advanced).
- Đáp án là một cấu trúc chứ không phải một số (khi đó: dựng nghiệm /
  tham lam có chứng minh — M4).

**Tiếp:** [Điểm kiểm tra](./hsgi-cp-m2)""",
)

# ---------------------------------------------------------------- practice
A1 = challenge(
    "hsgi-p2-count-range",
    "Đếm phần tử trong đoạn giá trị",
    """**Bài toán.** Cho dãy n số và q truy vấn (a, b): có bao nhiêu phần tử
thuộc [a, b]?

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |x_i|, |a|, |b| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số (sắp theo thứ tự tăng — đã cho sắp);
q dòng: a b.
**Ra:** q dòng, mỗi dòng một số lượng.

**Điểm:** 100. Nếu a > b đáp án là 0.""",
    [
        contest_test(
            "ví dụ",
            T("6 3", "1 2 2 3 5 7", "2 3", "4 4", "-1 100"),
            T("3", "0", "6"),
            "upper_bound(b) − lower_bound(a). [2,3] chứa 2,2,3 → 3; [4,4]: không phần tử.",
        ),
        contest_test(
            "a > b",
            T("3 1", "1 2 3", "5 2"),
            T("0"),
            "Đoạn ngược: lower_bound(5) > upper_bound(2) → chênh âm, ép về 0.",
        ),
        contest_test(
            "mọi phần tử trùng giá trị truy vấn",
            T("5 1", "4 4 4 4 4", "4 4"),
            T("5"),
            "Giá trị biên trùng hẳn: upper_bound(4) − lower_bound(4) = 5.",
        ),
        contest_test(
            "n lớn, giá trị biên âm/dương",
            T("200000 2") + T(" ".join(str(i) for i in range(200000)), "-1 200000", "5000 5000"),
            T("200000", "1"),
            "Mảng phải sắp TĂNG để hai đường biên có nghĩa; truy vấn phủ toàn dải 2·10^5, giá trị đơn 1.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p2-predecessor",
    "Tiền nhiệm trên dãy sắp",
    """**Bài toán.** Cho dãy n số đã sắp và q truy vấn x: phần tử **lớn nhất ≤ x**
là bao nhiêu? Nếu không có, in "NONE".

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |x_i|, |x| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số; q dòng: x.
**Ra:** q dòng: giá trị hoặc NONE.""",
    [
        contest_test(
            "ví dụ",
            T("5 3", "1 3 5 7 9", "4", "9", "0"),
            T("3", "9", "NONE"),
            "upper_bound(4) trỏ tới 5, lùi 1 → 3. x = 9 trùng phần tử: upper_bound qua 9, lùi 1 → 9. x = 0: không lùi được.",
        ),
        contest_test(
            "x nhỏ hơn mọi phần tử",
            T("2 1", "10 20", "5"),
            T("NONE"),
            "upper_bound trả về begin(): không có tiền nhiệm — phải kiểm tra trước khi trừ.",
        ),
        contest_test(
            "một phần tử, truy vấn đúng biên",
            T("1 2", "-7", "-7", "-8"),
            T("-7", "NONE"),
            "Giá trị âm và biên bằng đúng: -7 tìm được; -8 nhỏ hơn mọi thứ → NONE.",
        ),
        contest_test(
            "n lớn, truy vấn xen giữa hai phần tử kề",
            T("200000 1") + T(" ".join(str(2 * i) for i in range(200000)), "3"),
            T("2"),
            "3 nằm giữa 2 và 4: tiền nhiệm 2. Truy vấn O(log n).",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p2-stations",
    "Đặt trạm on tên lửa (min-max khoảng cách)",
    """**Bài toán.** Trên trục có n điểm (đã sắp). Chọn c điểm làm trạm sao cho
**khoảng cách nhỏ nhất** giữa hai trạm kề nhau **lớn nhất**. In khoảng cách
đó.

**Ràng buộc:** 2 ≤ c ≤ n ≤ 100 000; 0 ≤ x_i ≤ 10^9.

**Vào:** dòng đầu n c; dòng hai n điểm (sắp tăng).
**Ra:** một số — khoảng cách nhỏ nhất tối đa hóa được.

**Điểm:** 100. Đây CHÍNH XÁC là mẫu "max-min": F(d) = "đặt được ≥ c trạm cách
nhau ≥ d" là đơn điệu trên d.""",
    [
        contest_test(
            "ví dụ",
            T("3 3", "0 5 10"),
            T("5"),
            "Đặt 0, 5, 10: F(5) đủ 3 trạm; F(6) chỉ còn 2 (0 rồi 10... 10−0 ≥ 6 nhưng điểm giữa 5 bỏ lỡ). Đáp án 5.",
        ),
        contest_test(
            "c = n",
            T("4 4", "1 2 3 4"),
            T("1"),
            "Phải lấy mọi điểm: khoảng cách nhỏ nhất là 1.",
        ),
        contest_test(
            "hai điểm duy nhất",
            T("2 2", "0 1000000000"),
            T("1000000000"),
            "c = n = 2: đáp án là đúng khoảng cách 10^9 — int 32 bit vẫn đủ nhưng long long an toàn.",
        ),
        contest_test(
            "n lớn, trạm thưa",
            T("100000 3") + T(" ".join(str(i) for i in range(100000)), "0", "0"),
            T("49999"),
            "Điểm 0..99999, 3 trạm: đặt 0, 50000, 99999 → min(50000, 49999) = 49999; F(50000) chỉ đặt được 2.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p2-woodcut",
    "Cưa gỗ (máy cưa cao bao nhiêu?)",
    """**Bài toán.** Máy cưa đặt ở độ cao h cắt phần cây cao hơn h. Cần thu được
ít nhất M mét gỗ. H cao nhất để đủ gỗ là bao nhiêu? (cây cao ≤ h cho 0 mét).

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ M ≤ 2·10^9; 0 ≤ chiều cao cây ≤ 10^9.

**Vào:** dòng đầu n M; dòng hai n chiều cao.
**Ra:** một số — h lớn nhất thỏa.

**Điểm:** 100. F(h) = "tổng max(0, chiều cao − h) ≥ M" đơn điệu giảm theo h →
tìm h lớn nhất (Khuôn B, mid trần).""",
    [
        contest_test(
            "ví dụ",
            T("4 7", "20 15 10 17"),
            T("15"),
            "h = 15: (5 + 0 + 0 + 2) = 7 ≥ 7. h = 16: (4 + 0 + 0 + 1) = 5 < 7. Đáp án 15.",
        ),
        contest_test(
            "cần toàn bộ gỗ",
            T("2 2000000000", "1000000000 1000000000"),
            T("0"),
            "M = tổng chính xác: h = 0 mới đủ. Kỳ vọng nằm ở BIÊN dưới.",
        ),
        contest_test(
            "một cây đủ",
            T("1 1", "1000000000"),
            T("999999999"),
            "h = 999999999 cho đúng 1 mét. Tràn int nếu tính tổng bằng int 32.",
        ),
        contest_test(
            "n lớn, phân bố đều",
            T("200000 1000000000") + T(" ".join("1000000000" for _ in range(200000))),
            T("999995000"),
            "Mỗi cây góp (10^9 − h): 200000·(10^9 − h) ≥ 10^9 → h ≤ 10^9 − 5000 = 999995000.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p2-chocolate",
    "Chia socola (phần lớn nhất nhỏ nhất)",
    """**Bài toán.** Một thanh socola gồm n ô nối tiếp, ô i có độ ngọt a[i].
Cắt thành **k đoạn không rỗng** liên tiếp sao cho **đoạn ngọt nhất** có độ
ngọt **nhỏ nhất**. In độ ngọt của đoạn ngọt nhất.

**Ràng buộc:** 1 ≤ k ≤ n ≤ 100 000; 1 ≤ a[i] ≤ 10^4; tổng ≤ 2·10^9.

**Vào:** dòng đầu n k; dòng hai n số.
**Ra:** một số — min của max đoạn.

**Điểm:** 100. F(s) = "chia được ≤ k đoạn với mỗi đoạn ≤ s" — tham lam gom
tối đa rồi cắt; đơn điệu trên s.""",
    [
        contest_test(
            "ví dụ",
            T("5 3", "1 2 3 4 5"),
            T("6"),
            "Cắt [1 2 3][4][5]: max 6? Thử [1 2][3 4][5]: max 6. s = 5: [1 2][3][4][5] cần 4 đoạn > 3. Đáp án 6 — kiểm tra bằng tay trước khi tin.",
        ),
        contest_test(
            "k = n",
            T("3 3", "7 1 9"),
            T("9"),
            "Mỗi ô một đoạn: max là phần tử lớn nhất 9.",
        ),
        contest_test(
            "k = 1",
            T("4 1", "3 1 4 1"),
            T("9"),
            "Một đoạn duy nhất: tổng 9.",
        ),
        contest_test(
            "n lớn, tất cả bằng nhau",
            T("100000 50") + T(" ".join("1000" for _ in range(100000))),
            T("2000000"),
            "Tổng 10^8 chia 50 đoạn: mỗi đoạn 2000 ô = 2·10^6 ngọt. Đoạn đều nhất cho max 2·10^6.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)
VI2 = {
    "hsgi-p2-count-range": vi_challenge(
        "Đếm phần tử trong đoạn giá trị",
        """**Bài toán.** Cho dãy n số và q truy vấn (a, b): có bao nhiêu phần tử
thuộc [a, b]?

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |x_i|, |a|, |b| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số; q dòng: a b.
**Ra:** q dòng, mỗi dòng một số lượng.""",
        [("ví dụ", "upper_bound(b) − lower_bound(a)."),
         ("a > b", "Đoạn ngược → 0."),
         ("mọi phần tử trùng giá trị truy vấn", "Chênh hai biên = 5."),
         ("n lớn, giá trị biên âm/dương", "Truy vấn phủ toàn dải: 2·10^5.")],
    ),
    "hsgi-p2-predecessor": vi_challenge(
        "Tiền nhiệm trên dãy sắp",
        """**Bài toán.** Cho dãy n số đã sắp và q truy vấn x: phần tử **lớn nhất ≤ x**
là bao nhiêu? Nếu không có, in "NONE".

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |x_i|, |x| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số; q dòng: x.
**Ra:** q dòng: giá trị hoặc NONE.""",
        [("ví dụ", "upper_bound(4) lùi 1 → 3; biên đúng vẫn tìm được."),
         ("x nhỏ hơn mọi phần tử", "Kiểm tra begin() trước khi trừ."),
         ("một phần tử, truy vấn đúng biên", "-7 tìm được; -8 → NONE."),
         ("n lớn, truy vấn xen giữa hai phần tử kề", "Truy vấn O(log n).")],
    ),
    "hsgi-p2-stations": vi_challenge(
        "Đặt trạm (min-max khoảng cách)",
        """**Bài toán.** Trên trục có n điểm (đã sắp). Chọn c điểm làm trạm sao cho
**khoảng cách nhỏ nhất** giữa hai trạm kề nhau **lớn nhất**. In khoảng cách
đó.

**Ràng buộc:** 2 ≤ c ≤ n ≤ 100 000; 0 ≤ x_i ≤ 10^9.

**Vào:** dòng đầu n c; dòng hai n điểm.
**Ra:** một số — khoảng cách nhỏ nhất tối đa hóa được.""",
        [("ví dụ", "1, 8, 100: min(7, 92) = 7."),
         ("c = n", "Lấy mọi điểm: min gap 1."),
         ("hai điểm duy nhất", "Đúng 10^9."),
         ("n lớn, trạm thưa", "Chia trục làm đôi: 0, 50000, 99999 → 49999.")],
    ),
    "hsgi-p2-woodcut": vi_challenge(
        "Cưa gỗ (máy cưa cao bao nhiêu?)",
        """**Bài toán.** Máy cưa đặt ở độ cao h cắt phần cây cao hơn h. Cần thu được
ít nhất M mét gỗ. H cao nhất để đủ gỗ là bao nhiêu?

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ M ≤ 2·10^9; 0 ≤ chiều cao cây ≤ 10^9.

**Vào:** dòng đầu n M; dòng hai n chiều cao.
**Ra:** một số — h lớn nhất thỏa.""",
        [("ví dụ", "h = 15 cho 7 mét."),
         ("cần toàn bộ gỗ", "M = tổng: h = 0."),
         ("một cây đủ", "h = 999999999; cẩn thận tràn int."),
         ("n lớn, phân bố đều", "10^9 − 5000 = 999995000.")],
    ),
    "hsgi-p2-chocolate": vi_challenge(
        "Chia socola (phần lớn nhất nhỏ nhất)",
        """**Bài toán.** Một thanh gồm n ô nối tiếp, ô i ngọt a[i]. Cắt thành **k đoạn
không rỗng** sao cho **đoạn ngọt nhất** có độ ngọt **nhỏ nhất**. In độ ngọt đó.

**Ràng buộc:** 1 ≤ k ≤ n ≤ 100 000; 1 ≤ a[i] ≤ 10^4; tổng ≤ 2·10^9.

**Vào:** dòng đầu n k; dòng hai n số.
**Ra:** một số — min của max đoạn.""",
        [("ví dụ", "s = 5 cần 4 đoạn > 3; đáp án 6."),
         ("k = n", "max phần tử."),
         ("k = 1", "Tổng toàn bộ."),
         ("n lớn, tất cả bằng nhau", "10^8 / 50 đoạn → 2·10^6.")],
    ),
}
write_practice(
    M,
    "hsgi-p2-binsearch",
    "Binary Search Problem Set",
    "Five problems: both bounds idioms, predecessor queries, and three binary-search-on-answer classics with honest checks.",
    "Bài tập tìm kiếm nhị phân",
    "Năm bài: hai thành ngữ đường biên, truy vấn tiền nhiệm, và ba bài kinh điển tìm nhị phân trên đáp án với hàm check trung thực.",
    "hsgi-m2-answer",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI2,
    solutions=[
        (
            "hsgi-p2-count-range",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> v(n);
    for (auto& x : v) in >> x;
    while (q--) {
        long long a, b; in >> a >> b;
        long long cnt = upper_bound(v.begin(), v.end(), b) - lower_bound(v.begin(), v.end(), a);
        out << max(0LL, cnt) << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> v(n);
    for (auto& x : v) in >> x;
    while (q--) {
        long long a, b; in >> a >> b;
        // near-miss: lower_bound(b) instead of upper_bound(b) — drops
        // every element EQUAL to b
        long long cnt = lower_bound(v.begin(), v.end(), b) - lower_bound(v.begin(), v.end(), a);
        out << max(0LL, cnt) << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p2-predecessor",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> v(n);
    for (auto& x : v) in >> x;
    while (q--) {
        long long x; in >> x;
        auto it = upper_bound(v.begin(), v.end(), x);
        if (it == v.begin()) out << "NONE" << "{{NL}}";
        else out << *prev(it) << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> v(n);
    for (auto& x : v) in >> x;
    while (q--) {
        long long x; in >> x;
        // near-miss: dùng lower_bound và quên trường hợp x TỒN TẠI —
        // báo phần tử NGHIÊM NGẶT nhỏ hơn x thay vì chính x (≤ bị hiểu thành <)
        auto it = lower_bound(v.begin(), v.end(), x);
        if (it == v.begin()) out << "NONE" << "{{NL}}";
        else out << *prev(it) << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p2-stations",
            CPP_STD + cpp("""    int n, c; in >> n >> c;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long l = 1, r = a[n-1] - a[0];
    while (l < r) {
        long long mid = l + (r - l + 1) / 2;
        int placed = 1;
        long long last = a[0];
        for (int i = 1; i < n && placed < c; ++i)
            if (a[i] - last >= mid) { ++placed; last = a[i]; }
        if (placed >= c) l = mid; else r = mid - 1;
    }
    out << l << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, c; in >> n >> c;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long l = 1, r = a[n-1] - a[0];
    while (l < r) {
        long long mid = l + (r - l + 1) / 2;
        int placed = 1;
        long long last = a[0];
        for (int i = 1; i < n; ++i)
            // near-miss: > mid instead of >= mid — a station at exactly
            // distance mid is rejected, so the answer shortchanges by one
            if (a[i] - last > mid) { ++placed; last = a[i]; }
        if (placed >= c) l = mid; else r = mid - 1;
    }
    out << l << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p2-woodcut",
            CPP_STD + cpp("""    int n; long long M; in >> n >> M;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    long long l = 0, r = *max_element(h.begin(), h.end());
    while (l < r) {
        long long mid = l + (r - l + 1) / 2;
        long long got = 0;
        for (int i = 0; i < n; ++i)
            if (h[i] > mid) got += h[i] - mid;
        if (got >= M) l = mid; else r = mid - 1;
    }
    out << l << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long M; in >> n >> M;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    long long l = 0, r = *max_element(h.begin(), h.end());
    while (l < r) {
        long long mid = l + (r - l) / 2;
        long long got = 0;
        for (int i = 0; i < n; ++i)
            if (h[i] > mid) got += h[i] - mid;
        // near-miss: nhầm CHIỀU đơn điệu — F(h) ĐÚNG khi h NHỎ (thu nhiều
        // gỗ), nên tìm "h nhỏ nhất còn đủ" thay vì "h lớn nhất": trả về 0
        if (got >= M) r = mid; else l = mid + 1;
    }
    out << l << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p2-chocolate",
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long lo = *max_element(a.begin(), a.end());
    long long hi = 0;
    for (auto x : a) hi += x;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        int parts = 1;
        long long cur = 0;
        bool ok = true;
        for (int i = 0; i < n; ++i) {
            if (cur + a[i] <= mid) cur += a[i];
            else { ++parts; cur = a[i]; if (parts > k) { ok = false; break; } }
        }
        if (ok) hi = mid; else lo = mid + 1;
    }
    out << lo << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long lo = *max_element(a.begin(), a.end());
    long long hi = 0;
    for (auto x : a) hi += x;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        // near-miss: greedy packs greedily but never counts the piece
        // it must CLOSE when moving on — undercounts parts by one,
        // accepting sums that need k+1 pieces
        int parts = 1;
        long long cur = 0;
        bool ok = true;
        for (int i = 0; i < n; ++i) {
            if (cur + a[i] <= mid) cur += a[i];
            else { cur = a[i]; if (parts > k) { ok = false; break; } ++parts; }
        }
        if (ok) hi = mid; else lo = mid + 1;
    }
    out << lo << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH2 = challenge(
    "hsgi-cp-m2-wifi",
    "Checkpoint — Bộ thu WiFi",
    """**Bài toán.** Dọc hành lang có n lớp học tại vị trí x_1 < x_2 < ... < x_n.
Trường mua **k bộ thu WiFi** (k ≤ n). Đặt các bộ thu TẠI các vị trí lớp học,
mỗi vị trí nhiều nhất một bộ. Khoảng cách phát của hệ thống là khoảng cách
**lớn nhất** giữa hai lớp kề nhau được phủ bởi **cùng một** bộ thu... đơn
giản hơn: mỗi bộ thu phủ liên tiếp các lớp từ vị trí của nó tới bộ thu kế;
khoảng cách phát = khoảng cách xa nhất giữa một lớp và bộ thu của nó. Tối
thiểu hóa khoảng cách phát đó.

**Ràng buộc:** 1 ≤ k ≤ n ≤ 100 000; 0 ≤ x_i ≤ 10^9.

**Vào:** dòng đầu n k; dòng hai n vị trí (sắp tăng).
**Ra:** một số — khoảng cách phát nhỏ nhất.

**Điểm:** 100. F(d) = "đặt được ≤ k bộ thu phủ mọi lớp với bán kính d" — tham
lam quét từ trái, mở bộ mới khi lớp hiện tại vượt vùng phủ; đơn điệu trên d.""",
    [
        contest_test(
            "ví dụ",
            T("5 2", "1 2 8 9 100"),
            T("8"),
            "F(8): bộ tại 1 phủ [1,9] (lớp 1,2,8,9), bộ tại 100 phủ lớp 100 → 2 bộ ✓. F(7): bộ tại 1 phủ [1,8], lớp 9 phải mở bộ thứ hai tại 9, lớp 100 lại mở bộ thứ ba → ✗. Đáp án 8.",
        ),
        contest_test(
            "một bộ thu",
            T("3 1", "0 5 10"),
            T("10"),
            "Một bộ phủ mọi lớp: bán kính = max(x) − min(x) = 10.",
        ),
        contest_test(
            "bộ nhiều như lớp",
            T("4 4", "3 6 9 12"),
            T("0"),
            "Mỗi lớp một bộ: bán kính 0.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)
VI_CP2 = vi_challenge(
    "Checkpoint — Bộ thu WiFi",
    """**Bài toán.** Dọc hành lang có n lớp tại vị trí x_1 < ... < x_n. Trường mua
**k bộ thu**, đặt tại vị trí lớp (mỗi vị trí nhiều nhất một bộ). Khoảng cách
phát = khoảng cách xa nhất giữa một lớp và bộ thu phủ nó. **Tối thiểu hóa**
khoảng cách phát.

**Ràng buộc:** 1 ≤ k ≤ n ≤ 100 000; 0 ≤ x_i ≤ 10^9.

**Vào:** dòng đầu n k; dòng hai n vị trí.
**Ra:** một số — khoảng cách phát nhỏ nhất.""",        [("ví dụ", "F(8): bộ tại 1 phủ 1..9, bộ tại 100. F(7) cần 3 bộ → đáp án 8."),
         ("một bộ thu", "Bán kính = max − min."),
         ("bộ nhiều như lớp", "Bán kính 0.")],
)
write_checkpoint(
    M,
    "hsgi-cp-m2",
    "Checkpoint — Binary Search",
    "Pass the graded problem to finish the binary-search module.",
    20,
    """**Checkpoint — tìm kiếm nhị phân.** Pass the graded challenge below to
complete the module. It is the full skill: recognize max-min phrasing → write
an honest greedy check(d) (sweep left to right, open a new transmitter only
when the current class escapes coverage) → binary search d. Watch the sample
discussion — it walks through a FAILED guess on purpose, which is exactly how
you should debug your own F(d).

**Điểm kiểm tra — tìm kiếm nhị phân.** Pass bài chấm bên dưới để hoàn thành
module. Đây là kỹ năng trọn vẹn: nhận diện cách diễn đạt max-min → viết tham
lam check(d) trung thực (quét trái→phải, chỉ mở bộ thu mới khi lớp hiện tại
thoát vùng phủ) → tìm nhị phân d. Đọc phần bàn luận ví dụ — nó cố tình đi qua
MỘT lần đoán SAI, đúng cách bạn nên tự gỡ F(d) của mình.""",
    "Checkpoint — Tìm kiếm nhị phân",
    "Pass bài chấm để hoàn thành module tìm kiếm nhị phân.",
    """**Điểm kiểm tra — tìm kiếm nhị phân.** Pass bài chấm bên dưới để hoàn thành
module. Đây là kỹ năng trọn vẹn: nhận diện max-min → viết tham lam check(d)
trung thực → tìm nhị phân d. Đọc phần bàn luận ví dụ — nó cố tình đi qua một
lần đoán sai, đúng cách bạn nên tự gỡ F(d) của mình.""",
    CH2,
    VI_CP2,
    solution=CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> x(n);
    for (auto& v : x) in >> v;
    long long l = 0, r = x[n-1] - x[0];
    while (l < r) {
        long long mid = l + (r - l) / 2;
        int towers = 1;
        long long base = x[0];
        for (int i = 1; i < n; ++i)
            if (x[i] - base > mid) { ++towers; base = x[i]; }
        if (towers <= k) r = mid; else l = mid + 1;
    }
    out << l << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> x(n);
    for (auto& v : x) in >> v;
    long long l = 0, r = x[n-1] - x[0];
    while (l < r) {
        long long mid = l + (r - l) / 2;
        int towers = 1;
        long long base = x[0];
        for (int i = 1; i < n; ++i)
            // near-miss: >= mid — a class at exactly distance mid from the
            // current tower is forced onto a NEW tower, inflating the count
            // and pushing the reported radius one notch too high
            if (x[i] - base >= mid) { ++towers; base = x[i]; }
        if (towers <= k) r = mid; else l = mid + 1;
    }
    out << l << "{{NL}}";
""") + END,
)
