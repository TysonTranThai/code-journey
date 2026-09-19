#!/usr/bin/env python3
"""HSG Intermediate — Module 3: hsgi-intervals (interval & sweep mastery).

Merging, covering with points, minimum rooms (the end-vs-start TIE convention
— contrasts with M1's overlap counting where touching overlapped), interval
insertion, and free-time computation. Every near-miss is a convention or
boundary bug, never a crash.
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

M = "hsgi-intervals"
write_module(
    M,
    "Intervals and Sweep Mastery",
    "Merging, minimum covering points, minimum rooms (the tie convention), interval insertion, and free-time computation — all as sorted-event reasoning.",
    "Khoảng và quét sự kiện chuyên sâu",
    "Ghép đoạn, phủ bằng điểm tối thiểu, số phòng tối thiểu (quy ước chạm biên), chèn đoạn, và tính khoảng rảnh — tất cả bằng suy luận sự kiện có thứ tự.",
    ["hsgi-m3-merge", "hsgi-m3-cover", "hsgi-cp-m3"],
    ["hsgi-p3-intervals"],
)

# ---------------------------------------------------------------- lesson 3.1
write_lesson(
    M,
    "hsgi-m3-merge",
    "Merging and Inserting Intervals",
    "The sort-by-left invariant, merging in one pass, and inserting a new interval into an already-merged list.",
    15,
    """## The invariant

Sort intervals by left endpoint. Then any overlap is **local**: while merging,
you only ever compare the current merged interval's right end with the next
interval's left end.

```cpp
sort(v.begin(), v.end());                 // by (l, r)
vector<pair<long long,long long>> out;
for (auto [l, r] : v) {
    if (!out.empty() && l <= out.back().second)
        out.back().second = max(out.back().second, r);   // absorb
    else
        out.push_back({l, r});
}
```

Why `max(...)`? Because a later interval can be **contained** in the merged
one: [1, 100] then [2, 3] — the naive `out.back().second = r` shrinks the
merged interval to 3. This is the single most common merge bug.

### Inserting into a sorted list

Insert [l, r] into already-merged intervals:
1. everything ending **before l** stays (ends < l, no touch),
2. everything **touching or overlapping** [l, r] merges with it
   (start ≤ r AND end ≥ l),
3. everything starting **after r** stays.

```cpp
// three passes with lower_bound on the left endpoints, then one merge
```

Complexity: O(log n) to locate + O(n) to splice (output rebuilt).

### When NOT to merge

If the problem asks "how many intervals overlap at each point", merging
destroys information — sweep events (M1) answer it without collapsing.

## Practice recognition

"n đoạn, hợp tất cả giao..." — merging is right. "n đoạn, điểm nào bị phủ
nhiều nhất" — sweep is right. "đoạn nào chứa đoạn nào" — sort + stack / upper
bounds, no merging.

**Next:** [Covering and Rooms](./hsgi-m3-cover)""",
    "Ghép và chèn đoạn",
    "Bất biến sắp-theo-trái, ghép trong một lượt, và chèn đoạn mới vào danh sách đã ghép.",
    """## Bất biến

Sắp các đoạn theo đầu trái. Khi đó mọi giao là **cục bộ**: trong khi ghép, bạn
chỉ so right-end của đoạn đã ghép với left-end của đoạn kế tiếp.

```cpp
sort(v.begin(), v.end());                 // theo (l, r)
vector<pair<long long,long long>> out;
for (auto [l, r] : v) {
    if (!out.empty() && l <= out.back().second)
        out.back().second = max(out.back().second, r);   // hấp thụ
    else
        out.push_back({l, r});
}
```

Vì sao `max(...)`? Vì đoạn sau có thể **nằm trọn** trong đoạn đã ghép:
[1, 100] rồi [2, 3] — cách `out.back().second = r` ngây thơ làm đoạn ghép co
còn 3. Đây là lỗi ghép phổ biến nhất.

### Chèn vào danh sách đã sắp

Chèn [l, r] vào các đoạn đã ghép:
1. mọi đoạn kết thúc **trước l** giữ nguyên,
2. mọi đoạn **chạm hoặc giao** [l, r] ghép vào nó
   (bắt đầu ≤ r VÀ kết thúc ≥ l),
3. mọi đoạn bắt đầu **sau r** giữ nguyên.

```cpp
// ba lượt với lower_bound trên đầu trái, rồi một lần ghép
```

Độ phức tạp: O(log n) định vị + O(n) nối (dựng lại output).

### Khi nào KHÔNG ghép

Nếu đề hỏi "mỗi điểm bị bao nhiêu đoạn phủ", ghép phá thông tin — quét sự kiện
(M1) trả lời mà không gộp.

## Luyện nhận diện

"n đoạn, hợp tất cả giao..." — ghép đúng. "n đoạn, điểm nào bị phủ nhiều nhất"
— quét đúng. "đoạn nào chứa đoạn nào" — sắp + stack / chặn nhị phân, không ghép.

**Tiếp:** [Phủ và Phòng](./hsgi-m3-cover)""",
)

# ---------------------------------------------------------------- lesson 3.2
write_lesson(
    M,
    "hsgi-m3-cover",
    "Covering Points, Minimum Rooms, and the Tie Convention",
    "Greedy covering by sorted right ends, the rooms problem, and why 'end at t, start at t' changes the answer by problem.",
    17,
    """## Minimum points to cover intervals

"Chọn ít điểm nhất sao cho mỗi đoạn chứa ít nhất một điểm." Sort by **right
end**; always place the point at the right end of the first uncovered interval.

```cpp
sort(v.begin(), v.end(), [](auto& a, auto& b){ return a.second < b.second; });
long long last = LLONG_MIN;   // point already placed
int cnt = 0;
for (auto [l, r] : v)
    if (l > last) { ++cnt; last = r; }    // new point at r
```

Why right ends? Placing a point further right can never hurt intervals
*starting later*, and it covers the current interval. (Exchange argument:
any optimal solution's points can be slid right to their first covered
interval's end without losing coverage.)

### Minimum rooms — the tie convention

"n ca học [l, r], cần tối thiểu bao nhiêu phòng?" — the classic answer: sweep
events +1 at every start, −1 at every end, **but the tie order depends on the
statement**:

- a class ending at time t and another starting at t **can share a room**
  (room frees instantly): process **ends before starts** at equal time →
  −1 before +1;
- if the problem says cleanup takes a moment (or intervals are closed and
  sharing is forbidden): process **starts before ends** → +1 before −1.

M1's overlap counting (−1 at r+1) is the second convention: touching
intervals overlapped. Here the statement decides. **Read the statement, pick
the convention, state it in your solution.**

```cpp
// reusable-room convention: (time, type) with end < start in sort order
vector<pair<long long,int>> ev;
for (auto [l, r] : v) { ev.push_back({r, -1}); ev.push_back({l, +1}); }
sort(ev.begin(), ev.end());      // (-1 sorts before +1 at equal time)
int cur = 0, rooms = 0;
for (auto [t, d] : ev) { cur += d; rooms = max(rooms, cur); }
```

### Free time

"Khoảng rảnh chung của mọi người" = complement of the union of busy intervals:
merge busy (lesson 3.1), then walk gaps between merged intervals.

**Next:** [Checkpoint](./hsgi-cp-m3)""",
    "Phủ điểm, số phòng tối thiểu, và quy ước chạm biên",
    "Tham lam phủ bằng đầu phải, bài phòng học, và vì sao 'kết thúc tại t, bắt đầu tại t' đổi đáp án tùy bài.",
    """## Phủ đoạn bằng ít điểm nhất

"Chọn ít điểm nhất sao cho mỗi đoạn chứa ít nhất một điểm." Sắp theo **đầu
phải**; luôn đặt điểm ở đầu phải của đoạn đầu chưa được phủ.

```cpp
sort(v.begin(), v.end(), [](auto& a, auto& b){ return a.second < b.second; });
long long last = LLONG_MIN;   // điểm đã đặt
int cnt = 0;
for (auto [l, r] : v)
    if (l > last) { ++cnt; last = r; }    // điểm mới tại r
```

Vì sao đầu phải? Đặt điểm xa hơn bên phải không bao giờ làm mất đoạn *bắt đầu
sau*, và nó phủ đoạn hiện tại. (Lập luận đổi chỗ: điểm của mọi lời giải tối
ưu có thể trượt phải về đầu phải của đoạn đầu nó phủ mà không mất phủ.)

### Số phòng tối thiểu — quy ước chạm biên

"n ca học [l, r], cần tối thiểu bao nhiêu phòng?" — đáp án kinh điển: quét sự
kiện +1 tại mỗi bắt đầu, −1 tại mỗi kết thúc, **nhưng thứ tự chạm tùy đề**:

- ca kết thúc lúc t và ca bắt đầu lúc t **dùng chung phòng được** (phòng rảnh
  ngay): xử lý **kết thúc trước bắt đầu** tại cùng thời điểm → −1 trước +1;
- nếu đề nói dọn phòng mất thời gian (hoặc đoạn đóng và cấm dùng chung):
  xử lý **bắt đầu trước kết thúc** → +1 trước −1.

Cách đếm phủ trùng ở M1 (−1 tại r+1) là quy ước thứ hai: đoạn chạm nhau vẫn
tính trùng. Ở đây đề quyết định. **Đọc đề, chọn quy ước, nêu rõ trong lời giải.**

```cpp
// quy ước phòng-tái-dụng: (thời điểm, loại) với end < end trong sắp xếp
vector<pair<long long,int>> ev;
for (auto [l, r] : v) { ev.push_back({r, -1}); ev.push_back({l, +1}); }
sort(ev.begin(), ev.end());      // (−1 đứng trước +1 tại cùng thời điểm)
int cur = 0, rooms = 0;
for (auto [t, d] : ev) { cur += d; rooms = max(rooms, cur); }
```

### Khoảng rảnh

"Khoảng rảnh chung của mọi người" = phần bù của hợp các đoạn bận: ghép đoạn
bận (bài 3.1), rồi đi qua các khe giữa chúng.

**Tiếp:** [Điểm kiểm tra](./hsgi-cp-m3)""",
)

# ---------------------------------------------------------------- practice
A1 = challenge(
    "hsgi-p3-merge",
    "Ghép các đoạn giao nhau",
    """**Bài toán.** Cho n đoạn [l, r] (đóng). Hợp các đoạn giao hoặc chạm nhau
và in danh sách kết quả (sắp tăng), mỗi đoạn một dòng "l r".

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l ≤ r ≤ 10^9.

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** các đoạn đã hợp, mỗi dòng "l r".

**Điểm:** 100. Đoạn chạm tại một điểm (r1 = l2) được HỢP (đề quy định chạm là
giao).""",
    [
        contest_test(
            "ví dụ",
            T("4", "1 3", "2 6", "8 10", "15 18"),
            T("1 6", "8 10", "15 18"),
            "Sắp theo l; [1,3] và [2,6] giao → [1,6]. Cẩn thận: dùng max(right) khi hấp thụ.",
        ),
        contest_test(
            "đoạn nằm trọn trong đoạn trước",
            T("3", "1 100", "2 3", "50 60"),
            T("1 100"),
            "[2,3] và [50,60] nằm trong [1,100]: nếu gán right = r thay vì max, đoạn co hẹp sai.",
        ),
        contest_test(
            "chạm tại một điểm phải hợp",
            T("2", "1 3", "3 5"),
            T("1 5"),
            "Đề quy định chạm là giao: r1 = l2 → hợp thành [1,5]. Điều kiện là l <= right, không phải l < right.",
        ),
        contest_test(
            "n lớn xen kẽ",
            T("5", "1 5", "5 9", "9 20", "21 30", "40 50"),
            T("1 20", "21 30", "40 50"),
            "Chuỗi chạm 5→5→9→9→20 hợp thành [1,20]; [21,30] và [40,50] có khoảng hở.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p3-cover-points",
    "Phủ đoạn bằng ít điểm nhất",
    """**Bài toán.** Cho n đoạn [l, r] (đóng). Chọn ít điểm sao cho mỗi đoạn chứa
ít nhất một điểm. In số điểm.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l ≤ r ≤ 10^9.

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** một số.

**Điểm:** 100. Tham lam kinh điển: sắp theo đầu phải, đặt điểm tại r của đoạn
đầu chưa phủ.""",
    [
        contest_test(
            "ví dụ",
            T("3", "1 3", "2 5", "4 7"),
            T("2"),
            "Sắp theo đầu phải: [1,3],[2,5],[4,7]. Đặt 3; [2,5] chứa 3 ✓; [4,7] không chứa 3 → đặt 7. Đáp án 2.",
        ),
        contest_test(
            "hai đoạn rời nhau",
            T("2", "1 2", "4 5"),
            T("2"),
            "Không điểm nào thuộc cả hai → 2. last so với l > last (chạm vẫn tính được phủ).",
        ),
        contest_test(
            "đoạn đơn điểm và đoạn dài",
            T("3", "5 5", "1 10", "7 7"),
            T("2"),
            "Sắp theo r: [5,5],[7,7],[1,10]. Đặt 5; [7,7]: 7 > 5 → đặt 7; [1,10] chứa 7 ✓. Đáp án 2.",
        ),
        contest_test(
            "n lớn, lồng nhau",
            T("100000", "0 1000000000") + T(" ".join(str(i) + " " + str(1000000000 - i) for i in range(1, 100000))),
            T("1"),
            "Mọi đoạn chứa điểm 999990... kiểm: đoạn [i, 10^9−i] với i ≥ 1 đều chứa 500000000 → 1 điểm là đúng.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p3-rooms",
    "Số phòng học tối thiểu",
    """**Bài toán.** n ca học, ca i từ l_i đến r_i. Ca kết thúc tại t và ca bắt
đầu tại t **dùng chung phòng được**. Tối thiểu bao nhiêu phòng?

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l_i < r_i ≤ 10^9 (l < r: ca khác rỗng).

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** một số.

**Điểm:** 100. Quy ước quyết định: tại cùng thời điểm, xử lý −1 (kết thúc)
TRƯỚC +1 (bắt đầu).""",
    [
        contest_test(
            "ví dụ — chạm biên tái dụng",
            T("2", "1 3", "3 5"),
            T("1"),
            "Ca một kết thúc 3, ca hai bắt đầu 3: dùng chung phòng → 1. Đây KHÁC M1 (nơi chạm tính là phủ trùng).",
        ),
        contest_test(
            "ba ca giao thật",
            T("3", "1 5", "2 6", "4 7"),
            T("3"),
            "Thời điểm 4..5 có cả ba ca → 3 phòng.",
        ),
        contest_test(
            "kết thúc muộn hơn bắt đầu",
            T("2", "1 5", "5 9"),
            T("1"),
            "Ca hai bắt đầu ĐÚNG lúc ca một kết thúc: tái dụng → 1 phòng.",
        ),
        contest_test(
            "n lớn, xen kẽ đều",
            T("200000") + T(" ".join(str(2 * i) + " " + str(2 * i + 1) for i in range(200000))),
            T("1"),
            "200000 ca nối tiếp cách nhau 1 đơn vị, kết thúc tại 2i+1, ca sau bắt đầu 2i+2 > 2i+1 → không giao, không chạm → 1 phòng tái dụng mãi.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p3-free-time",
    "Khoảng rảnh chung của nhân viên",
    """**Bài toán.** Mỗi nhân viên có danh sách ca bận (đã ghép, không giao, sắp
tăng). Hỏi khoảng rảnh **chung** của TẤT CẢ nhân viên trong ngày [0, D].
In mỗi khoảng rảnh một dòng "l r" (kể cả độ dài 0? KHÔNG — chỉ rảnh > 0).
Nếu không có khoảng nào, không in gì.

**Ràng buộc:** 1 ≤ số nhân viên ≤ 50; mỗi người 0 ≤ số ca ≤ 200 000 (tổng
≤ 200 000); 0 ≤ l < r ≤ D ≤ 10^9; D cho dòng đầu.

**Vào:** dòng đầu D và số nhân viên k; mỗi nhân viên: dòng "m" rồi m dòng
"l r" (đã ghép, sắp tăng).
**Ra:** các khoảng rảnh chung sắp tăng, mỗi dòng "l r".

**Điểm:** 100. Hợp tất cả các ca (nếu cần), rồi phần bù trên [0, D].""",
    [
        contest_test(
            "ví dụ",
            T("10 2", "2", "1 3", "5 7", "1", "2 4"),
            T("0 1", "4 5", "7 10"),
            "Bận hợp: [1,3] ∪ [2,4] = [1,4], [5,7]. Phần bù trên [0,10]: [0,1), [4,5), [7,10]. In các khoảng đóng [l, r]: 0 1 / 4 5 / 7 10.",
        ),
        contest_test(
            "một nhân viên rảnh cả ngày",
            T("8 1", "0"),
            T("0 8"),
            "Không ca bận: cả ngày rảnh.",
        ),
        contest_test(
            "bận kín cả ngày",
            T("10 2", "1", "0 10", "1", "3 5"),
            "",
            "Hợp bận = [0,10] phủ cả ngày: không in dòng nào (output rỗng hợp lệ).",
        ),
        contest_test(
            "rảnh đúng một điểm ở biên",
            T("10 2", "1", "1 10", "1", "0 5"),
            "",
            "Bận [1,10] ∪ [0,5] = [0,10]: kín. Điểm biên không tạo khoảng > 0 → không in.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p3-insert",
    "Chèn một đoạn vào danh sách đã ghép",
    """**Bài toán.** Cho danh sách đoạn **đã ghép** (rời nhau, sắp tăng) và một
đoạn mới [l, r]. Chèn sao cho kết quả vẫn là danh sách đã ghép. In kết quả,
mỗi dòng "l r". Đoạn CHẠM (r1 = l2) được HỢP.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l ≤ r ≤ 10^9.

**Vào:** dòng đầu n; n dòng "l r" (đã ghép sắp tăng); dòng cuối "l r" đoạn mới.
**Ra:** danh sách sau khi chèn.

**Điểm:** 100.""",
    [
        contest_test(
            "ví dụ",
            T("3", "1 2", "4 6", "8 10", "3 5"),
            T("1 2", "3 6", "8 10"),
            "[3,5] chỉ giao [4,6] → [3,6]; [1,2] kết thúc trước 3, [8,10] bắt đầu sau 6 giữ nguyên.",
        ),
        contest_test(
            "đoạn mới bao trùm tất cả",
            T("3", "2 3", "5 6", "8 9", "1 10"),
            T("1 10"),
            "Đoạn mới [1,10] hấp thụ cả ba.",
        ),
        contest_test(
            "đoạn mới chạm hai phía",
            T("2", "1 5", "7 10", "5 7"),
            T("1 10"),
            "[5,7] chạm [1,5] tại 5 và chạm [7,10] tại 7 → hợp hết thành [1,10].",
        ),
        contest_test(
            "chèn vào đầu/cuối",
            T("2", "5 6", "8 9", "0 4"),
            T("0 4", "5 6", "8 9"),
            "Chèn trước tất cả, không giao gì.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)
VI3 = {
    "hsgi-p3-merge": vi_challenge(
        "Ghép các đoạn giao nhau",
        """**Bài toán.** Cho n đoạn [l, r] (đóng). Hợp các đoạn giao hoặc chạm nhau
và in danh sách kết quả (sắp tăng), mỗi dòng "l r".

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l ≤ r ≤ 10^9.

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** các đoạn đã hợp, mỗi dòng "l r".""",
        [("ví dụ", "[1,3]∪[2,6] = [1,6]; giữ [8,10], [15,18]."),
         ("đoạn nằm trọn trong đoạn trước", "max(right) khi hấp thụ."),
         ("chạm tại một điểm phải hợp", "l <= right, không phải l < right."),
         ("n lớn xen kẽ", "Chỉ GIAO hoặc CHẠM mới hợp: 1 5 / 6 30 / 40 50.")],
    ),
    "hsgi-p3-cover-points": vi_challenge(
        "Phủ đoạn bằng ít điểm nhất",
        """**Bài toán.** Cho n đoạn [l, r] (đóng). Chọn ít điểm sao cho mỗi đoạn chứa
ít nhất một điểm. In số điểm.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l ≤ r ≤ 10^9.

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** một số.""",
        [("ví dụ", "Điểm 3 phủ cả ba đoạn."),
         ("hai đoạn rời nhau", "Không điểm chung → 2."),
         ("đoạn đơn điểm và đoạn dài", "5 ∉ [7,7] → 2 điểm."),
         ("n lớn, lồng nhau", "Mọi đoạn chứa 500000000 → 1.")],
    ),
    "hsgi-p3-rooms": vi_challenge(
        "Số phòng học tối thiểu",
        """**Bài toán.** n ca học, ca i từ l_i đến r_i. Ca kết thúc tại t và ca bắt
đầu tại t **dùng chung phòng được**. Tối thiểu bao nhiêu phòng?

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l_i < r_i ≤ 10^9.

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** một số.""",
        [("ví dụ — chạm biên tái dụng", "Kết thúc 3, bắt đầu 3: chung phòng → 1."),
         ("ba ca giao thật", "Thời điểm 4..5: 3 phòng."),
         ("kết thúc muộn hơn bắt đầu", "Tái dụng → 1."),
         ("n lớn, xen kẽ đều", "Ca nối tiếp không giao → 1 phòng.")],
    ),
    "hsgi-p3-free-time": vi_challenge(
        "Khoảng rảnh chung của nhân viên",
        """**Bài toán.** Mỗi nhân viên có danh sách ca bận (đã ghép, sắp tăng). In
các khoảng rảnh **chung** của tất cả nhân viên trong ngày [0, D], mỗi dòng
"l r" (chỉ rảnh > 0). Không có thì không in.

**Ràng buộc:** 1 ≤ k ≤ 50; tổng số ca ≤ 200 000; 0 ≤ l < r ≤ D ≤ 10^9.

**Vào:** dòng đầu D và k; mỗi nhân viên: dòng "m" rồi m dòng "l r".
**Ra:** các khoảng rảnh chung sắp tăng.""",
        [("ví dụ", "Bận [1,4] ∪ [5,7] → rảnh 0 1 / 4 5 / 7 10."),
         ("một nhân viên rảnh cả ngày", "Cả ngày 0 8."),
         ("bận kín cả ngày", "Output rỗng."),
         ("rảnh đúng một điểm ở biên", "Không khoảng > 0 → không in.")],
    ),
    "hsgi-p3-insert": vi_challenge(
        "Chèn một đoạn vào danh sách đã ghép",
        """**Bài toán.** Cho danh sách đoạn **đã ghép** (rời nhau, sắp tăng) và một
đoạn mới [l, r]. Chèn giữ tính đã ghép. Mỗi dòng "l r". CHẠM được HỢP.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ l ≤ r ≤ 10^9.

**Vào:** dòng đầu n; n dòng "l r"; dòng cuối đoạn mới.
**Ra:** danh sách sau khi chèn.""",
        [("ví dụ", "[3,5] chỉ giao [4,6] → 1 2 / 3 6 / 8 10."),
         ("đoạn mới bao trùm tất cả", "Hấp thụ cả ba."),
         ("đoạn mới chạm hai phía", "Chạm 5 và 7 → [1,10]."),
         ("chèn vào đầu/cuối", "0 4 / 5 6 / 8 9.")],
    ),
}
write_practice(
    M,
    "hsgi-p3-intervals",
    "Intervals Problem Set",
    "Five problems: merging (with the containment trap), covering points, the reusable-room tie convention, common free time, and insertion.",
    "Bài tập khoảng",
    "Năm bài: ghép đoạn (bẫy đoạn lồng), phủ điểm, quy ước tái dụng phòng, khoảng rảnh chung, và chèn đoạn.",
    "hsgi-m3-cover",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI3,
    solutions=[
        (
            "hsgi-p3-merge",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> v(n);
    for (auto& [l, r] : v) in >> l >> r;
    sort(v.begin(), v.end());
    vector<pair<long long,long long>> res;
    for (auto& [l, r] : v) {
        if (!res.empty() && l <= res.back().second)
            res.back().second = max(res.back().second, r);
        else
            res.push_back({l, r});
    }
    for (auto& [l, r] : res) out << l << " " << r << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> v(n);
    for (auto& [l, r] : v) in >> l >> r;
    sort(v.begin(), v.end());
    vector<pair<long long,long long>> res;
    for (auto& [l, r] : v) {
        if (!res.empty() && l <= res.back().second)
            // near-miss: gán trực tiếp r thay vì max — đoạn nằm trọn
            // trong đoạn trước làm co đoạn đã hợp
            res.back().second = r;
        else
            res.push_back({l, r});
    }
    for (auto& [l, r] : res) out << l << " " << r << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p3-cover-points",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> v(n);
    for (auto& [l, r] : v) in >> l >> r;
    sort(v.begin(), v.end(), [](auto& a, auto& b){ return a.second < b.second; });
    long long last = -1;
    int cnt = 0;
    for (auto& [l, r] : v) {
        if (l > last) { ++cnt; last = r; }
    }
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> v(n);
    for (auto& [l, r] : v) in >> l >> r;
    sort(v.begin(), v.end(), [](auto& a, auto& b){ return a.second < b.second; });
    long long last = -1;
    int cnt = 0;
    for (auto& [l, r] : v) {
        // near-miss: đặt điểm tại l thay vì r — điểm quá trái, các đoạn
        // sau có l nhỏ hơn last mới... sai trên đoạn bắt đầu sau last
        if (l > last) { ++cnt; last = l; }
    }
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p3-rooms",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({r, 0});   // end (0 sorts before +1's at same time)
        ev.push_back({l, 1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0, rooms = 0;
    for (auto& [t, d] : ev) {
        if (d) { ++cur; rooms = max(rooms, cur); }
        else --cur;
    }
    out << rooms << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({r, 1});   // near-miss: end đánh dấu +1 (như start)
        ev.push_back({l, 1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0, rooms = 0;
    for (auto& [t, d] : ev) {
        if (d) { ++cur; rooms = max(rooms, cur); }
        else --cur;
    }
    out << rooms << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p3-free-time",
            CPP_STD + cpp("""    long long D; int k; in >> D >> k;
    vector<pair<long long,long long>> all;
    for (int e = 0; e < k; ++e) {
        int m; in >> m;
        for (int i = 0; i < m; ++i) {
            long long l, r; in >> l >> r;
            all.push_back({l, r});
        }
    }
    sort(all.begin(), all.end());
    vector<pair<long long,long long>> busy;
    for (auto& [l, r] : all) {
        if (!busy.empty() && l <= busy.back().second)
            busy.back().second = max(busy.back().second, r);
        else busy.push_back({l, r});
    }
    long long prev = 0;
    for (auto& [l, r] : busy) {
        if (l > prev) out << prev << " " << l << "{{NL}}";
        prev = max(prev, r);
    }
    if (prev < D) out << prev << " " << D << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long D; int k; in >> D >> k;
    vector<pair<long long,long long>> all;
    for (int e = 0; e < k; ++e) {
        int m; in >> m;
        for (int i = 0; i < m; ++i) {
            long long l, r; in >> l >> r;
            all.push_back({l, r});
        }
    }
    sort(all.begin(), all.end());
    vector<pair<long long,long long>> busy;
    for (auto& [l, r] : all) {
        if (!busy.empty() && l <= busy.back().second)
            busy.back().second = max(busy.back().second, r);
        else busy.push_back({l, r});
    }
    long long prev = 0;
    for (auto& [l, r] : busy) {
        // near-miss: in cả khoảng độ dài 0 (l == prev) và quên đoạn đuôi
        // sau ca bận cuối — output thừa dòng "x x" và thiếu "prev D"
        if (l >= prev) out << prev << " " << l << "{{NL}}";
        prev = max(prev, r);
    }
""") + END,
        ),
        (
            "hsgi-p3-insert",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> v(n);
    for (auto& [l, r] : v) in >> l >> r;
    long long L, R; in >> L >> R;
    vector<pair<long long,long long>> res;
    bool merged = false;
    for (auto& [l, r] : v) {
        if (r < L || l > R) {
            res.push_back({l, r});
        } else {
            L = min(L, l);
            R = max(R, r);
            if (!merged) { merged = true; }
        }
    }
    res.push_back({L, R});
    sort(res.begin(), res.end());
    for (auto& [l, r] : res) out << l << " " << r << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> v(n);
    for (auto& [l, r] : v) in >> l >> r;
    long long L, R; in >> L >> R;
    vector<pair<long long,long long>> res;
    for (auto& [l, r] : v) {
        // near-miss: điều kiện tách là r < L && l > R (AND thay OR) —
        // gần như luôn sai, đoạn ngoài trái bị hấp thụ nhầm
        if (r < L && l > R) {
            res.push_back({l, r});
        } else {
            L = min(L, l);
            R = max(R, r);
        }
    }
    res.push_back({L, R});
    sort(res.begin(), res.end());
    for (auto& [l, r] : res) out << l << " " << r << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH3 = challenge(
    "hsgi-cp-m3-busday",
    "Checkpoint — Ngày bận nhất của quán",
    """**Bài toán.** Quán có n lượt đặt bàn, lượt i từ l_i đến r_i (đóng;
l = r cho phép — lượt 0 phút). Quán phục vụ trong ngày [0, D]. Cần thuê tối
thiểu bao nhiêu bàn để **một lượt không phải chờ** — bàn kết thúc lúc t có thể
nhận lượt bắt đầu tại t? Lượt 0 phút vẫn chiếm một bàn tại đúng khoảnh khắc
đó (hai lượt điểm cùng thời điểm cần hai bàn). In số bàn tối thiểu.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ D ≤ 10^9; 0 ≤ l ≤ r ≤ D.

**Vào:** dòng đầu n D; n dòng: l r.
**Ra:** một số — số bàn tối thiểu.

**Điểm:** 100. Quét sự kiện với BỨC LOẠI ba lớp tại cùng thời điểm:
start-điểm (l = r) đếm trước, rồi end, rồi start-thường — lượt điểm phải
hiện diện khoảnh khắc đó, trong khi start-thường tái dụng bàn vừa gỡ.""",
    [
        contest_test(
            "ví dụ",
            T("4 10", "1 3", "3 5", "5 7", "2 4"),
            T("2"),
            "Tại t=3: lượt 1 kết thúc trước lượt 2 bắt đầu (tái dụng) → tối đa 2 lượt đồng thời (t=2..3: lượt 1,4). Đáp án 2.",
        ),
        contest_test(
            "chỉ lượt 0 phút",
            T("2 5", "2 2", "2 2"),
            T("2"),
            "Hai lượt điểm cùng thời điểm 2: cả hai chiếm bàn tại khoảnh khắc đó → 2.",
        ),
        contest_test(
            "không giao nào",
            T("2 10", "0 4", "5 9"),
            T("1"),
            "Một bàn tái dụng mãi — và tọa độ 10^9 không sao với quét sự kiện.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)
VI_CP3 = vi_challenge(
    "Checkpoint — Ngày bận nhất của quán",
    """**Bài toán.** Quán có n lượt đặt bàn, lượt i từ l_i đến r_i (đóng; l = r
cho phép — lượt 0 phút). Trong ngày [0, D]. Cần tối thiểu bao nhiêu bàn để
không lượt nào chờ — bàn kết thúc lúc t nhận được lượt bắt đầu tại t? Lượt
0 phút vẫn chiếm một bàn tại đúng khoảnh khắc đó. In số bàn tối thiểu.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 0 ≤ D ≤ 10^9; 0 ≤ l ≤ r ≤ D.

**Vào:** dòng đầu n D; n dòng: l r.
**Ra:** một số — số bàn tối thiểu.""",
    [("ví dụ", "Tái dụng tại chạm: tối đa 2 lượt đồng thời → 2."),
     ("chỉ lượt 0 phút", "Hai lượt điểm cùng thời điểm → 2."),
     ("không giao nào", "1 bàn.")],
)
write_checkpoint(
    M,
    "hsgi-cp-m3",
    "Checkpoint — Intervals",
    "Pass the graded problem to finish the intervals module.",
    20,
    """**Checkpoint — khoảng.** Pass the graded challenge below to complete the
module. It runs TWO sweeps on the same data (minimum tables with the
reuse-at-a-tie convention, then maximum simultaneous occupancy) and adds the
zero-minute booking corner (l = r still occupies a table at that instant).
State your convention explicitly in comments — that is the habit this module
is really grading.

**Điểm kiểm tra — khoảng.** Pass bài chấm bên dưới để hoàn thành module. Chạy
HAI phép quét trên cùng dữ liệu (số bàn tối thiểu với quy ước tái dụng tại
điểm chạm, rồi phủ đồng thời tối đa), cộng góc lượt 0 phút (l = r vẫn chiếm
bàn tại khoảnh khắc đó). Nêu rõ quy ước trong comment — thói quen mà module
này thực sự chấm.""",
    "Checkpoint — Khoảng",
    "Pass bài chấm để hoàn thành module khoảng.",
    """**Điểm kiểm tra — khoảng.** Pass bài chấm bên dưới để hoàn thành module.
HAI phép quét: số bàn tối thiểu (tái dụng tại chạm) và phủ đồng thời tối đa,
cộng góc lượt 0 phút. Nêu rõ quy ước trong comment.""",
    CH3,
    VI_CP3,
    solution=CPP_STD + cpp("""    int n; long long D; in >> n >> D;
    // bậc tại cùng thời điểm: 0 = start-điểm (l == r, chiếm bàn ngay),
    // 1 = end (thường), 2 = start-thường (tái dụng bàn vừa gỡ)
    vector<tuple<long long,int,int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        if (l == r) {
            ev.push_back({l, 0, +1});
            ev.push_back({l, 1, -1});
        } else {
            ev.push_back({l, 2, +1});
            ev.push_back({r, 1, -1});
        }
    }
    sort(ev.begin(), ev.end());
    int cur = 0, tables = 0;
    for (auto& [t, k, d] : ev) {
        cur += d;
        tables = max(tables, cur);
    }
    out << tables << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; long long D; in >> n >> D;
    // near-miss: start-điểm xử lý SAU end (bậc 2 như start-thường) —
    // hai lượt điểm cùng thời điểm bị đếm... 0 bàn vì −1 gỡ trước +1
    vector<tuple<long long,int,int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, 2, +1});
        ev.push_back({r, 1, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0, tables = 0;
    for (auto& [t, k, d] : ev) {
        cur += d;
        tables = max(tables, cur);
    }
    out << tables << "{{NL}}";
""") + END,
)
