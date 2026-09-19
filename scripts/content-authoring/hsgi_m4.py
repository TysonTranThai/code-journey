#!/usr/bin/env python3
"""HSG Intermediate — Module 4: hsgi-greedy2 (greedy & exchange arguments).

Heap-based greedy (merge cost), earliest-deadline-first, the running median
(two heaps), shortest-job-first, slot-filling profit, and the fuel-station
lookahead. Every near-miss fails a test for a *structural* reason (wrong
invariant, wrong sort key, wrong lookahead) — never by crashing.
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

# ---- generated ground truth for the max-n median test (from the DEFINITION:
# rank m//2 + 1 of the sorted prefix — bisect, not the heap algorithm) ----
import bisect as _bisect

_MED_N = 20000
_arr = []
_MEDS = []
for _i in range(_MED_N):
    _bisect.insort(_arr, _i % 7)
    _MEDS.append(_arr[len(_arr) // 2])
assert _MEDS[:7] == [0, 1, 1, 2, 2, 3, 3]

M = "hsgi-greedy2"
write_module(
    M,
    "Greedy With Proof — Exchange Arguments and Heaps",
    "Proving greedy by adjacent swaps, heap-driven merging, earliest-deadline-first, the two-heap running median, slot filling, and lookahead refueling.",
    "Tham lam có chứng minh — Lập luận đổi chỗ và heap",
    "Chứng minh tham lam bằng đổi chỗ kề nhau, ghép bằng heap, deadline sớm nhất trước, trung vị chạy hai heap, lấp khe nhận việc, và tiếp nhiên liệu nhìn trước.",
    ["hsgi-m4-exchange", "hsgi-m4-heaps", "hsgi-cp-m4"],
    ["hsgi-p4-greedy"],
)

# ---------------------------------------------------------------- lesson 4.1
write_lesson(
    M,
    "hsgi-m4-exchange",
    "Exchange Arguments — Why the Greedy Is Right",
    "The swap proof pattern, three worked examples, and when greedy is provably wrong.",
    16,
    """## The proof pattern

Greedy claims: some sorted order (by p, by deadline, by ratio...) is optimal.
Proof by **adjacent exchange**: take any optimal solution where two adjacent
items violate the claimed order; swap them; show the objective does not get
worse. Repeating closes the gap between "some optimum" and "the sorted order".

### Example 1 — minimize total waiting (SPT)

One machine, jobs with times p_i, waiting of job i = sum of p of everyone
before it. Claim: shortest job first is optimal.

Swap proof: with adjacent jobs a (longer) before b (shorter), swapping changes
total waiting by p_a − p_b ≥ 0... precisely: everything before the pair is
unchanged; between the two orders the pair contributes (0·p_a + p_a·p_b) vs
(0·p_b + p_b·p_a) for the pair members — the other jobs after shift by
p_a + p_b either way. Total difference = p_a − p_b... anyway: shorter first
never loses. Easier to verify on numbers than on algebra — THAT is the exam
skill: compute the swap delta on a 2-job example, generalize.

### Example 2 — minimize maximum lateness (EDF)

Jobs (p_i, d_i); finish times f_i; lateness L_i = max(0, f_i − d_i). Claim:
sort by deadline (earliest first) minimizes max L. The adjacent exchange: if
d_a > d_b with a before b, swapping keeps the pair's finish times the same set
{f, f + p}, and the LATER deadline getting the LATER finish never increases
the max. So EDF dominates.

### Example 3 — merge cost (Huffman-style)

n ropes, merging two costs their length sum; merge all into one, minimize
total cost. Claim: always merge the two SMALLEST. The exchange argument is
deeper (the smallest two must both be merged last-ish), but the *structure* is
the same: local optimum (smallest pair) survives swaps. Implementation: a
min-heap, pop two, push sum, accumulate — O(n log n).

## When greedy is WRONG — recognize fast

- Coins non-canonical (1, 3, 4 for 6: greedy 4+1+1 = 3 coins vs 3+3 = 2) →
  DP (Beginner M15 pattern).
- Interval scheduling with WEIGHTS → DP instead of earliest-end greedy.
- Anything with "mỗi lựa chọn ảnh hưởng các lựa chọn sau theo cách không đơn
  điệu" — test a tiny counterexample by hand BEFORE trusting greedy.

Habit: 30 seconds with paper. Two adversarial items. If the swap delta is
never negative, trust greedy; if you find one counterexample, go DP.

**Next:** [Heaps Do the Work](./hsgi-m4-heaps)""",
    "Lập luận đổi chỗ — Vì sao tham lam đúng",
    "Mẫu chứng minh bằng đổi chỗ, ba ví dụ làm mẫu, và khi nào tham lam bị chứng minh là sai.",
    """## Mẫu chứng minh

Tham lam khẳng định: một thứ tự sắp nào đó (theo p, theo deadline, theo tỉ
số...) là tối ưu. Chứng minh bằng **đổi chỗ kề nhau**: lấy bất kỳ lời giải tối
ưu nào mà hai phần tử kề nhau vi phạm thứ tự đó; đổi chỗ chúng; chứng minh
mục tiêu không tệ đi. Lặp lại thu hẹp khoảng cách giữa "một lời giải tối ưu"
và "thứ tự đã sắp".

### Ví dụ 1 — tối thiểu tổng thời gian chờ (SPT)

Một máy, công việc có thời gian p_i, thời gian chờ của việc i = tổng p của
mọi việc trước nó. Khẳng định: việc ngắn nhất trước là tối ưu.

Chứng minh đổi chỗ: với hai việc kề a (dài) trước b (ngắn), đổi chỗ làm tổng
chờ thay đổi p_a − p_b ≥ 0... dễ nhất là tính delta của cặp trên một ví dụ
2 việc bằng số rồi khái quát — ĐÓ chính là kỹ năng phòng thi: tính delta đổi
chỗ bằng ví dụ nhỏ, không cần đại số.

### Ví dụ 2 — tối thiểu trễ tối đa (EDF)

Việc (p_i, d_i); thời điểm xong f_i; độ trễ L_i = max(0, f_i − d_i). Khẳng
định: sắp theo deadline (sớm nhất trước) tối thiểu hóa max L. Đổi chỗ: nếu
d_a > d_b mà a trước b, đổi chỗ giữ nguyên tập thời điểm xong {f, f + p} của
cặp, và deadline MUỘN nhận thời điểm xong MUỘN không làm max tăng.

### Ví dụ 3 — chi phí ghép (kiểu Huffman)

n sợi dây, ghép hai sợi tốn tổng độ dài; ghép tất cả thành một, tối thiểu tổng
chi phí. Khẳng định: luôn ghép hai sợi NHỎ NHẤT. Cấu trúc chứng minh giống hệt:
tối ưu cục bộ (cặp nhỏ nhất) sống sót qua các phép đổi chỗ. Cài đặt: min-heap,
lấy hai nhỏ nhất, đẩy tổng, cộng dồn — O(n log n).

## Khi nào tham lam SAI — nhận diện nhanh

- Tiền không chuẩn hóa (1, 3, 4 cho 6: tham lam 4+1+1 = 3 xu vs 3+3 = 2) →
  DP (mẫu Beginner M15).
- Sắp lịch khoảng CÓ TRỌNG SỐ → DP thay vì tham lam kết-thúc-sớm-nhất.
- Mọi bài "mỗi lựa chọn ảnh hưởng các lựa chọn sau theo cách không đơn
  điệu" — thử một phản ví dụ nhỏ trên giấy TRƯỚC khi tin tham lam.

Thói quen: 30 giây với giấy. Hai phần tử phản đề. Nếu delta đổi chỗ không bao
giờ âm, tin tham lam; nếu tìm ra một phản ví dụ, chuyển DP.

**Tiếp:** [Heap làm việc thay bạn](./hsgi-m4-heaps)""",
)

# ---------------------------------------------------------------- lesson 4.2
write_lesson(
    M,
    "hsgi-m4-heaps",
    "Heaps Do the Work — Median, Slots, and Lookahead",
    "priority_queue patterns: two-heap median, latest-free-slot filling, and the fuel-stop lookahead that defers choices.",
    17,
    """## Two heaps for a running median

Stream of numbers; after each insert report the upper median (the ⌊m/2⌋+1-th
smallest). Keep:
- `left`: max-heap of the smaller half,
- `right`: min-heap of the larger half,
with sizes |right| ≤ |left| ≤ |right| + 1.

```cpp
priority_queue<int> left;                       // max-heap
priority_queue<int, vector<int>, greater<int>> right;   // min-heap
// push:
if (left.empty() || x <= left.top()) left.push(x);
else right.push(x);
// balance:
if (left.size() > right.size() + 1) { right.push(left.top()); left.pop(); }
if (right.size() > left.size())     { left.push(right.top()); right.pop(); }
// report: m odd → left.top();  m even → right.top()
```

The invariant decides the answer — one flipped comparison and every median
drifts. Draw the sizes on paper for m = 1..5 to convince yourself.

### Latest-free-slot (unit jobs with deadlines)

Each job takes 1 slot in {1..n}, has deadline d and profit w; maximize total
profit. Sort by **profit descending**; for each job take the LATEST free slot
≤ d; if none, drop the job.

```cpp
sort(jobs.begin(), jobs.end(), [](auto& a, auto& b){ return a.w > b.w; });
vector<bool> used(n + 1, false);
long long total = 0;
for (auto [d, w] : jobs)
    for (int s = min(d, n); s >= 1; --s)
        if (!used[s]) { used[s] = true; total += w; break; }
```

Why latest? Early slots are the scarcest resource — a job with a late deadline
can use them, but need not. (Naive DSU makes the scan O(α); the honest loop is
O(n^2) worst — fine at n ≤ 10^4, and the statement's constraint says which.)

### Lookahead — defer the decision (fuel stops)

"Đi hết D km, bình chứa T, trạm ở p_i (châm đầy)." Minimize stops: drive, and
only when the NEXT stretch is unreachable, refuel at the **best station
already passed** (max capacity → but all fills are full, so the best station
is simply any — the trick is to keep a max-heap of PASSED-but-unused stations
and pop one only when forced).

```cpp
priority_queue<long long> passed;
long long pos = 0, fuel = T;     // start with a full tank
int stops = 0;
for each next gap g:
    while (fuel < g) {
        if (passed.empty()) { unreachable; }
        fuel += passed.top(); passed.pop(); ++stops;   // retro-fill
    }
    fuel -= g; pos += g;
    if (is a station at pos) passed.push(T);           // remember, don't spend
```

Deferring the choice is the pattern: greedy decisions made at the LAST
responsible moment dominate early commitments.

**Next:** [Checkpoint](./hsgi-cp-m4)""",
    "Heap làm việc thay bạn — Trung vị, khe, và nhìn trước",
    "Các mẫu priority_queue: trung vị hai heap, lấp khe muộn-nhất, và tiếp nhiên liệu trì hoãn quyết định.",
    """## Hai heap cho trung vị chạy

Dòng số; sau mỗi lần chèn báo trung vị trên (phần tử nhỏ thứ ⌊m/2⌋+1). Giữ:
- `left`: max-heap nửa nhỏ hơn,
- `right`: min-heap nửa lớn hơn,
kích thước |right| ≤ |left| ≤ |right| + 1.

```cpp
priority_queue<int> left;                       // max-heap
priority_queue<int, vector<int>, greater<int>> right;   // min-heap
// chèn:
if (left.empty() || x <= left.top()) left.push(x);
else right.push(x);
// cân bằng:
if (left.size() > right.size() + 1) { right.push(left.top()); left.pop(); }
if (right.size() > left.size())     { left.push(right.top()); right.pop(); }
// báo: m lẻ → left.top();  m chẵn → right.top()
```

Bất biến quyết định đáp án — đảo một dấu so sánh là mọi trung vị trôi. Vẽ kích
thước hai heap trên giấy cho m = 1..5 để tự tin.

### Khe muộn-nhất (việc đơn vị có deadline)

Mỗi việc chiếm 1 khe trong {1..n}, có deadline d và lợi nhuận w; tối đa hóa
tổng lợi nhuận. Sắp theo **lợi nhuận giảm dần**; mỗi việc lấy khe TRỐNG MUỘN
NHẤT ≤ d; không có thì bỏ việc.

```cpp
sort(jobs.begin(), jobs.end(), [](auto& a, auto& b){ return a.w > b.w; });
vector<bool> used(n + 1, false);
long long total = 0;
for (auto [d, w] : jobs)
    for (int s = min(d, n); s >= 1; --s)
        if (!used[s]) { used[s] = true; total += w; break; }
```

Vì sao muộn nhất? Khe sớm là tài nguyên khan hiếm nhất — việc deadline muộn
dùng được chúng nhưng không cần. (DSU đưa scan về O(α); vòng ngây thơ O(n^2)
xấu nhất — đủ dùng ở n ≤ 10^4, và ràng buộc của đề nói điều đó.)

### Nhìn trước — trì hoãn quyết định (trạm xăng)

"Đi hết D km, bình chứa T, trạm ở p_i (châm đầy)." Tối thiểu số lần dừng: chạy,
chỉ khi CHẶNG KẾ tiếp không tới được thì châm tại **trạm tốt nhất đã đi qua**
(giữ max-heap các trạm đã qua-chưa-dùng và chỉ rút khi bị ép).

```cpp
priority_queue<long long> passed;
long long pos = 0, fuel = T;     // xuất phát bình đầy
int stops = 0;
mỗi khoảng trống g:
    while (fuel < g) {
        if (passed.empty()) { không tới được; }
        fuel += passed.top(); passed.pop(); ++stops;   // châm hồi tố
    }
    fuel -= g; pos += g;
    if (có trạm tại pos) passed.push(T);               // ghi nhớ, chưa tiêu
```

Trì hoãn quyết định là mẫu bài: quyết định tham lam tại thời điểm BẮT BUỘC
CUỐI cùng luôn thắng cam kết sớm.

**Tiếp:** [Điểm kiểm tra](./hsgi-cp-m4)""",
)

# ---------------------------------------------------------------- practice
A1 = challenge(
    "hsgi-p4-ropes",
    "Ghép dây với chi phí nhỏ nhất",
    """**Bài toán.** n sợi dây, sợi i dài l_i. Mỗi lượt ghép hai sợi thành một
sợi dài bằng tổng, tốn chi phí bằng tổng đó. Ghép tất cả thành một sợi. In
TỔNG chi phí nhỏ nhất.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ l_i ≤ 10^6.

**Vào:** dòng đầu n; dòng hai n độ dài.
**Ra:** một số — tổng chi phí nhỏ nhất.""",
    [
        contest_test(
            "ví dụ",
            T("4", "4 3 2 6"),
            T("29"),
            "Min-heap: 2+3=5 (chi phí 5), 4+5=9 (9), 6+9=15 (15) → 5+9+15 = 29.",
        ),
        contest_test(
            "một sợi duy nhất",
            T("1", "7"),
            T("0"),
            "Không cần ghép: chi phí 0.",
        ),
        contest_test(
            "hai sợi",
            T("2", "1000000 1000000"),
            T("2000000"),
            "Một lượt ghép: chi phí 2·10^6 — long long.",
        ),
        contest_test(
            "n lớn bằng nhau",
            T("200000") + T(" ".join("1" for _ in range(200000))),
            T("3537856"),
            "Ghép đôi đều: tổng chi phí = 3537856 (cây ghép cân của 2·10^5 lá đơn vị) — min-heap trả lời tức thì.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p4-edf",
    "Độ trễ lớn nhất nhỏ nhất (deadline sớm trước)",
    """**Bài toán.** n việc trên một máy, việc i mất p_i và có hạn d_i (bắt đầu
lúc 0, chạy liên tục theo thứ tự bạn chọn). Độ trễ của việc i là
max(0, f_i − d_i) với f_i là thời điểm xong. Chọn thứ tự để độ trễ LỚN NHẤT
nhỏ nhất. In độ trễ lớn nhất đó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ p_i ≤ 10^6; 1 ≤ d_i ≤ 10^15.

**Vào:** dòng đầu n; n dòng: p d.
**Ra:** một số — max lateness nhỏ nhất.""",
    [
        contest_test(
            "ví dụ",
            T("3", "3 4", "2 2", "1 8"),
            T("1"),
            "EDF: (2,2) xong 2 (trễ 0), (3,4) xong 5 (trễ 1), (1,8) xong 6 (trễ 0) → max 1.",
        ),
        contest_test(
            "không việc nào trễ",
            T("2", "1 5", "2 5"),
            T("0"),
            "Cả hai xong trước hạn: 0.",
        ),
        contest_test(
            "việc dài hạn sớm",
            T("2", "10 1", "1 100"),
            T("9"),
            "EDF: việc (10,1) trước: xong 10, trễ 9; việc kia xong 11 trễ 0 → 9. SPT sẽ chọn (1,100) trước: trễ (10,1) là 10 — tệ hơn.",
        ),
        contest_test(
            "n lớn cùng hạn",
            T("200000") + T(" ".join("1 " + str(200000) for _ in range(200000))),
            T("0"),
            "Mọi việc 1 đơn vị, hạn n: hoàn tất đúng hạn lần lượt → max trễ 0.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p4-median",
    "Trung vị chạy (hai heap)",
    """**Bài toán.** Đọc n số theo lượt. Sau MỖI số, in "trung vị trên" — phần tử
nhỏ thứ ⌊m/2⌋ + 1 trong m số đã đọc (m chẵn: phần tử trên của hai phần giữa;
m lẻ: phần giữa).

**Ràng buộc:** 1 ≤ n ≤ 200 000; |x| ≤ 10^9.

**Vào:** dòng đầu n; dòng hai n số.
**Ra:** n dòng — trung vị trên sau mỗi lượt.""",
    [
        contest_test(
            "ví dụ",
            T("5", "3 1 2 5 4"),
            T("3", "3", "2", "3", "3"),
            "m=1: 3. m=2 {1,3}: phần tử thứ 2 = 3. m=3 {1,2,3}: thứ 2 = 2. m=4 {1,2,3,5}: thứ 3 = 3. m=5: thứ 3 = 3.",
        ),
        contest_test(
            "sắp giảm dần",
            T("4", "9 7 5 3"),
            T("9", "9", "7", "7"),
            "m=1: 9. m=2 {7,9}: thứ 2 = 9. m=3 {5,7,9}: thứ 2 = 7. m=4 {3,5,7,9}: thứ 3 = 7.",
        ),
        contest_test(
            "hai phần tử",
            T("2", "-5 5"),
            T("-5", "5"),
            "Giá trị âm hợp lệ; m=2: phần tử thứ 2 = 5 (trung vị trên = max của hai phần giữa).",
        ),
        contest_test(
            "n lớn luân phiên",
            T(str(_MED_N)) + T(" ".join(str(i % 7) for i in range(_MED_N))),
            T(*[str(v) for v in _MEDS]),
            "Kỳ vọng sinh từ ĐỊNH NGHĨA (phần tử nhỏ thứ ⌊m/2⌋+1 của tiền tố đã sắp) — hai heap trả lời O(log)/lượt; sắp lại mỗi lượt là chết ngân sách.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p4-wait",
    "Tổng thời gian chờ nhỏ nhất",
    """**Bài toán.** n khách, khách i cần p_i phút phục vụ, một quầy. Khách chờ =
tổng thời gian phục vụ của những khách trước mình. Chọn thứ tự để TỔNG thời
gian chờ nhỏ nhất. In tổng đó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ p_i ≤ 10^6.

**Vào:** dòng đầu n; dòng hai p_i.
**Ra:** một số.""",
    [
        contest_test(
            "ví dụ",
            T("3", "5 2 3"),
            T("7"),
            "SPT: khách 2 (chờ 0), khách 3 (chờ 2), khách 5 (chờ 2+3=5) → tổng 7. FIFO cho 0+5+7 = 12.",
        ),
        contest_test(
            "một khách",
            T("1", "9"),
            T("0"),
            "Không ai chờ trước: 0.",
        ),
        contest_test(
            "đã sắp sẵn",
            T("3", "1 2 3"),
            T("4"),
            "SPT trùng thứ tự cho: chờ 0, 1, 3 → 4.",
        ),
        contest_test(
            "n lớn đều nhau",
            T("200000") + T(" ".join(str(3 + (i % 5)) for i in range(200000))),
            T("83999500000"),
            "SPT 40000 lần 4,5,6,7,8: tổng chờ = 83999500000 — long long bắt buộc (8.4·10^10).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p4-slots",
    "Việc theo giờ — tối đa hóa lợi nhuận",
    """**Bài toán.** n công việc, mỗi việc chiếm ĐÚNG một khung giờ trong
{1..n giờ}, việc i có hạn d_i và lợi nhuận w_i (bỏ dở không được). Chọn tập
việc và xếp giờ để TỔNG lợi nhuận lớn nhất.

**Ràng buộc:** 1 ≤ n ≤ 10 000; 1 ≤ d_i ≤ n; 1 ≤ w_i ≤ 10^9.

**Vào:** dòng đầu n; n dòng: d w.
**Ra:** một số — tổng lợi nhuận lớn nhất.""",
    [
        contest_test(
            "ví dụ",
            T("4", "2 20", "2 10", "3 40", "4 30"),
            T("100"),
            "Lợi nhuận giảm: 40 (khe 3), 30 (khe 4), 20 (khe 2), 10 (khe 1) — cả bốn vừa: 100.",
        ),
        contest_test(
            "deadline chật loại việc",
            T("3", "1 50", "1 30", "4 40"),
            T("90"),
            "50 (khe 1), 40 (khe 4), 30 bỏ (khe ≤ 1 đã kín) → 90.",
        ),
        contest_test(
            "khe muộn phải để dành",
            T("3", "3 60", "1 50", "3 40"),
            T("150"),
            "60 (khe 3), 50 (khe 1), 40 (khe 2) → 150. Nếu 60 chiếm khe 1 sớm: 40 mất khe... kiểm: chọn 60@3, 50@1, 40@2 — đầy đủ, 150.",
        ),
        contest_test(
            "n lớn trùng hạn",
            T("10000") + T(" ".join("1 " + str(1000000000 - i) for i in range(10000))),
            T("1000000000"),
            "Mọi việc hạn 1: chỉ nhận 1 việc lợi nhuận cao nhất (10^9), còn lại bỏ — long long không cần nhưng kỷ luật có.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)
VI4 = {
    "hsgi-p4-ropes": vi_challenge(
        "Ghép dây với chi phí nhỏ nhất",
        """**Bài toán.** n sợi dây dài l_i. Mỗi lượt ghép hai sợi (chi phí = tổng
độ dài). Ghép tất cả thành một. In tổng chi phí nhỏ nhất.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ l_i ≤ 10^6.

**Vào:** dòng đầu n; dòng hai n độ dài.
**Ra:** một số.""",
        [("ví dụ", "Min-heap: 2+3=5, 4+5=9, 6+9=15 → 29."),
         ("một sợi duy nhất", "Không ghép: 0."),
         ("hai sợi", "2·10^6 — long long."),
         ("n lớn bằng nhau", "Cỡ n·log2 n ≈ 2.95·10^6.")],
    ),
    "hsgi-p4-edf": vi_challenge(
        "Độ trễ lớn nhất nhỏ nhất (deadline sớm trước)",
        """**Bài toán.** n việc trên một máy, việc i mất p_i, hạn d_i. Độ trễ =
max(0, f_i − d_i). Chọn thứ tự để độ trễ LỚN NHẤT nhỏ nhất. In nó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ p_i ≤ 10^6; 1 ≤ d_i ≤ 10^15.

**Vào:** dòng đầu n; n dòng: p d.
**Ra:** một số.""",
        [("ví dụ", "EDF: (2,2),(3,4),(1,8) → max trễ 1."),
         ("không việc nào trễ", "0."),
         ("việc dài hạn sớm", "EDF 9, SPT 10 — EDF thắng."),
         ("n lớn cùng hạn", "Hoàn tất đúng hạn: 0.")],
    ),
    "hsgi-p4-median": vi_challenge(
        "Trung vị chạy (hai heap)",
        """**Bài toán.** Đọc n số theo lượt. Sau MỖI số, in "trung vị trên" — phần
tử nhỏ thứ ⌊m/2⌋ + 1 trong m số đã đọc.

**Ràng buộc:** 1 ≤ n ≤ 200 000; |x| ≤ 10^9.

**Vào:** dòng đầu n; dòng hai n số.
**Ra:** n dòng.""",
        [("ví dụ", "3, 3, 2, 3, 3."),
         ("sắp giảm dần", "9, 9, 7, 7."),
         ("hai phần tử", "-5, 5."),
         ("n lớn luân phiên", "Hai heap O(log)/lượt; sắp lại mỗi lượt là chết.")],
    ),
    "hsgi-p4-wait": vi_challenge(
        "Tổng thời gian chờ nhỏ nhất",
        """**Bài toán.** n khách, khách i cần p_i phút, một quầy. Chờ của khách =
tổng phục vụ của những khách trước. Chọn thứ tự để TỔNG chờ nhỏ nhất. In nó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ p_i ≤ 10^6.

**Vào:** dòng đầu n; dòng hai p_i.
**Ra:** một số.""",
        [("ví dụ", "SPT: chờ 0+2+5 = 7 (FIFO là 12)."),
         ("một khách", "0."),
         ("đã sắp sẵn", "0+1+3 = 4."),
         ("n lớn đều nhau", "SPT 4,5,6,7,8 tuần tự — long long.")],
    ),
    "hsgi-p4-slots": vi_challenge(
        "Việc theo giờ — tối đa hóa lợi nhuận",
        """**Bài toán.** n việc, mỗi việc chiếm đúng 1 giờ trong {1..n}, việc i có
hạn d_i, lợi nhuận w_i. Chọn tập việc để tổng lợi nhuận lớn nhất.

**Ràng buộc:** 1 ≤ n ≤ 10 000; 1 ≤ d_i ≤ n; 1 ≤ w_i ≤ 10^9.

**Vào:** dòng đầu n; n dòng: d w.
**Ra:** một số.""",
        [("ví dụ", "40@3, 30@4, 20@2, 10@1 → 100."),
         ("deadline chật loại việc", "50@1, 40@4 → 90."),
         ("khe muộn phải để dành", "60@3, 50@1, 40@2 → 150."),
         ("n lớn trùng hạn", "Chỉ nhận việc 10^9 tốt nhất.")],
    ),
}
write_practice(
    M,
    "hsgi-p4-greedy",
    "Greedy Problem Set",
    "Five problems: Huffman merging, EDF lateness, the two-heap median, SPT waiting, latest-slot profit — each greedy proved by exchange.",
    "Bài tập tham lam",
    "Năm bài: ghép Huffman, độ trễ EDF, trung vị hai heap, chờ SPT, lợi nhuận khe muộn — mỗi tham lam đều có chứng minh đổi chỗ.",
    "hsgi-m4-heaps",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI4,
    solutions=[
        (
            "hsgi-p4-ropes",
            CPP_STD + cpp("""    int n; in >> n;
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        pq.push(x);
    }
    long long total = 0;
    while (pq.size() > 1) {
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        total += a + b;
        pq.push(a + b);
    }
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    priority_queue<long long> pq;   // near-miss: MAX-heap — luôn ghép hai
    for (int i = 0; i < n; ++i) {   // sợi LỚN NHẤT, tốn hơn trên data lệch
        long long x; in >> x;
        pq.push(x);
    }
    long long total = 0;
    while (pq.size() > 1) {
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        total += a + b;
        pq.push(a + b);
    }
    out << total << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p4-edf",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> j(n);
    for (auto& [p, d] : j) in >> p >> d;
    sort(j.begin(), j.end(), [](auto& a, auto& b){ return a.second < b.second; });
    long long t = 0, worst = 0;
    for (auto& [p, d] : j) {
        t += p;
        worst = max(worst, max(0LL, t - d));
    }
    out << worst << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,long long>> j(n);
    for (auto& [p, d] : j) in >> p >> d;
    // near-miss: sort theo thời gian xử lý (SPT) thay vì deadline —
    // việc dài có hạn sớm bị trễ phạt nặng
    sort(j.begin(), j.end());
    long long t = 0, worst = 0;
    for (auto& [p, d] : j) {
        t += p;
        worst = max(worst, max(0LL, t - d));
    }
    out << worst << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p4-median",
            CPP_STD + cpp("""    int n; in >> n;
    priority_queue<int> left;
    priority_queue<int, vector<int>, greater<int>> right;
    for (int i = 0; i < n; ++i) {
        int x; in >> x;
        if (left.empty() || x <= left.top()) left.push(x);
        else right.push(x);
        if ((int)left.size() > (int)right.size() + 1) { right.push(left.top()); left.pop(); }
        if ((int)right.size() > (int)left.size())     { left.push(right.top()); right.pop(); }
        int m = i + 1;
        if (m % 2 == 1) out << left.top() << "{{NL}}";
        else            out << right.top() << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    priority_queue<int> everything;   // near-miss: chỉ một max-heap —
    for (int i = 0; i < n; ++i) {     // in top = MAX của mọi số đã đọc
        int x; in >> x;               // thay vì trung vị trên
        everything.push(x);
        out << everything.top() << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p4-wait",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> p(n);
    for (auto& x : p) in >> x;
    sort(p.begin(), p.end());
    long long t = 0, total = 0;
    for (int i = 0; i < n; ++i) {
        total += t;
        t += p[i];
    }
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> p(n);
    for (auto& x : p) in >> x;
    // near-miss: giữ nguyên thứ tự nhập (FIFO) thay vì SPT — tổng chờ
    // phồng trên mọi data chưa sắp
    long long t = 0, total = 0;
    for (int i = 0; i < n; ++i) {
        total += t;
        t += p[i];
    }
    out << total << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p4-slots",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,int>> j(n);   // (w, d)
    for (auto& [w, d] : j) in >> d >> w;
    sort(j.begin(), j.end(), [](auto& a, auto& b){ return a.first > b.first; });
    vector<bool> used(n + 1, false);
    long long total = 0;
    for (auto& [w, d] : j) {
        for (int s = min(d, n); s >= 1; --s) {
            if (!used[s]) { used[s] = true; total += w; break; }
        }
    }
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,int>> j(n);   // (w, d)
    for (auto& [w, d] : j) in >> d >> w;
    sort(j.begin(), j.end(), [](auto& a, auto& b){ return a.first > b.first; });
    vector<bool> used(n + 1, false);
    long long total = 0;
    for (auto& [w, d] : j) {
        // near-miss: chiếm khe SỚM NHẤT còn trống (≤ d) thay vì muộn nhất —
        // khe sớm là tài nguyên khan hiếm, việc hạn muộn bị ép bỏ
        for (int s = 1; s <= min(d, n); ++s) {
            if (!used[s]) { used[s] = true; total += w; break; }
        }
    }
    out << total << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH4 = challenge(
    "hsgi-cp-m4-fuel",
    "Checkpoint — Chuyến xe tải xuyên tỉnh",
    """**Bài toán.** Xe tải đi từ A đến B cách D km, bình chứa T lít, mỗi lít đi
1 km, xuất phát với bình ĐẦY. Dọc đường có n trạm xăng tại km p_i
(0 < p_1 < p_2 < ... < p_n < D), đến trạm có thể CHÂM ĐẦY bình. Tối thiểu bao
nhiêu lần châm để tới B? Không thể → in −1.

**Ràng buộc:** 1 ≤ D, T ≤ 10^9; 1 ≤ n ≤ 200 000; 0 < p_i < D.

**Vào:** dòng đầu D T n; n dòng: p_i (sắp tăng).
**Ra:** một số — số lần châm ít nhất hoặc −1.""",
    [
        contest_test(
            "ví dụ",
            T("30 10 4", "4", "8", "13", "21"),
            T("2"),
            "Bình 10: đi 4, 8 (còn 2). 13 vượt — châm tại 8 (đầy), đi 13, 21 (còn 5). 30 vượt — châm tại 21. Đáp án 2.",
        ),
        contest_test(
            "không cần châm",
            T("10 10 2", "3", "6"),
            T("0"),
            "Bình đầy đủ đi hết 10 km: 0 lần châm.",
        ),
        contest_test(
            "khoảng trống vô vọng",
            T("100 10 1", "50"),
            T("-1"),
            "Giữa km 50 và 100 hụt 40 km không trạm: bình 10 không bao giờ vượt — −1.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)
VI_CP4 = vi_challenge(
    "Checkpoint — Chuyến xe tải xuyên tỉnh",
    """**Bài toán.** Xe đi từ A đến B cách D km, bình T lít (1 lít = 1 km), xuất
phát bình đầy. n trạm tại km p_i (sắp tăng), đến trạm được châm đầy. Tối
thiểu số lần châm? Không thể → −1.

**Ràng buộc:** 1 ≤ D, T ≤ 10^9; 1 ≤ n ≤ 200 000; 0 < p_i < D.

**Vào:** dòng đầu D T n; n dòng: p_i.
**Ra:** một số hoặc −1.""",
    [("ví dụ", "Châm tại 8 và 21 → 2 lần."),
     ("không cần châm", "0."),
     ("khoảng trống vô vọng", "−1.")],
)
write_checkpoint(
    M,
    "hsgi-cp-m4",
    "Checkpoint — Greedy",
    "Pass the graded problem to finish the greedy module.",
    20,
    """**Checkpoint — tham lam.** Pass the graded challenge below to complete the
module. The fuel problem is the deferred-decision greedy: keep a max-heap of
stations passed but unused; only when the next stretch is unreachable, retro-
fill at the best passed station. Also handle the two honest edge answers:
0 (never needed) and −1 (a gap no tank size can bridge).

**Điểm kiểm tra — tham lam.** Pass bài chấm bên dưới để hoàn thành module. Bài
xăng là tham lam trì hoãn quyết định: giữ max-heap các trạm đã qua-chưa-dùng;
chỉ khi chặng kế không tới được mới châm hồi tố tại trạm tốt nhất. Xử lý cả
hai đáp án biên: 0 (không cần) và −1 (khoảng trống vô vọng).""",
    "Checkpoint — Tham lam",
    "Pass bài chấm để hoàn thành module tham lam.",
    """**Điểm kiểm tra — tham lam.** Pass bài chấm bên dưới để hoàn thành module.
Tham lam trì hoãn quyết định: max-heap trạm đã qua, châm hồi tố khi ép buộc;
xử lý 0 và −1.""",
    CH4,
    VI_CP4,
    solution=CPP_STD + cpp("""    long long D, T; int n; in >> D >> T >> n;
    priority_queue<long long> passed;
    long long pos = 0, fuel = T;
    int stops = 0;
    bool impossible = false;
    for (int i = 0; i < n && !impossible; ++i) {
        long long p; in >> p;
        long long g = p - pos;
        while (fuel < g) {
            if (passed.empty()) { impossible = true; break; }
            fuel += passed.top(); passed.pop(); ++stops;
        }
        if (impossible) break;
        fuel -= g;
        pos = p;
        passed.push(T);
    }
    if (!impossible) {
        long long g = D - pos;
        while (fuel < g) {
            if (passed.empty()) { impossible = true; break; }
            fuel += passed.top(); passed.pop(); ++stops;
        }
    }
    out << (impossible ? -1 : stops) << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    long long D, T; int n; in >> D >> T >> n;
    // near-miss: tham lam SỚM — châm tại MỌI trạm đi qua, số lần dừng
    // phồng trên mọi data có nhiều trạm liên tiếp
    long long pos = 0, fuel = T;
    int stops = 0;
    bool impossible = false;
    for (int i = 0; i < n && !impossible; ++i) {
        long long p; in >> p;
        long long g = p - pos;
        if (fuel < g) { impossible = true; break; }
        fuel -= g;
        pos = p;
        ++stops;              // châm dù không cần
        fuel = T;
    }
    if (!impossible && fuel < D - pos) impossible = true;
    out << (impossible ? -1 : stops) << "{{NL}}";
""") + END,
)
