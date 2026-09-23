#!/usr/bin/env python3
"""HSG Mastery — Module 1: hsgm-process (The Mastery Process).

The solve pipeline: model → constraints → observations → candidates →
simplest-correct → verify (samples + adversarial cases) → complexity check →
implement → defend. Everything later in the course exercises a stage of this
pipeline; this module installs it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgm import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

Q = chr(92)
NL = chr(10)


def cpp(s):
    return s.replace("{{NL}}", Q + "n")


def T(*lines):
    return "".join(l + NL for l in lines)


# NOTE: solutions use explicit includes (hsga pattern) — solution.cpp is
# compiled INTO the QA harness TU (which pre-includes the std headers), and
# the local QA toolchain (Apple clang) lacks bits/stdc++.h.
CPP_STD = cpp("""#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <utility>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgm-process"
write_module(
    M,
    "The Mastery Process",
    "The full pipeline from statement to defended solution: model, budget the complexity, find the cheapest correct idea, verify adversarially, implement. Every later module drills one stage of this loop.",
    "Quy trình làm chủ",
    "Toàn bộ đường đi từ đề bài đến lời giải được bảo vệ: dựng mô hình, tính ngân sách phức tạp, tìm ý tưởng đúng rẻ nhất, kiểm chứng adversarial, rồi cài đặt. Mọi module sau luyện một chặng của vòng lặp này.",
    ["hsgm-m1-pipeline", "hsgm-m1-verify", "hsgm-cp-m1"],
    ["hsgm-p1-drills"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgm-m1-pipeline",
    "The Solve Pipeline",
    "Seven stages from statement to defended solution — and where solvers actually lose time.",
    14,
    """
# The Solve Pipeline

Strong solvers run the same loop on every unfamiliar problem:

1. **Model** — restate the problem in objects and operations, no story. "n
   lamps, flip prefixes" is a model; "the wizard chants" is not.
2. **Budget** — constraints → op-count ceiling → candidate families. If the
   ceiling is ~3·10^8, an O(n log^2 n) solution at n = 3·10^5 is already
   code-it-now territory; grinding for O(n) can *lose* points to
   implementation risk.
3. **Candidates** — list two or three families that fit the budget. Write
   down, for each, the one sentence that would have to be true.
4. **Simplest correct** — among the candidates, the cheapest *correct*
   idea wins. A simpler algorithm that passes beats a cleverer one that
   TLEs or buggy-implements. Correctness first, then speed.
5. **Verify before coding** — attack your own idea: smallest cases (n = 1,
   2), all-equal values, sorted vs reversed input, duplicates, extreme
   values. If it survives, code it. If you find the break yourself, you
   just saved a submission.
6. **Implement defensively** — the operations you are most sure about are
   where the bugs live. Check the sample *by hand-tracing your own code*,
   not by faith.
7. **Defend** — know why your solution is correct (one paragraph) and what
   it does on the worst input. If you cannot state either, you are not
   done.

## Where time is actually lost

Post-mortems of contest rounds consistently show the same sinkholes:

- coding before verifying the idea (step 5 skipped) — the debugging costs
  3× the verification would have;
- optimizing before having a *correct* baseline (step 4 inverted);
- re-reading the statement in the middle of coding because the model was
  never written down (step 1 skipped).

The pipeline is not bureaucracy — it is the order that minimizes total
time, including the time of mistakes.
""",
    "Quy trình bảy bước",
    "Bảy chặng từ đề bài đến lời giải được bảo vệ — và nơi thí sinh thực sự mất thời gian.",
    """
# Quy trình bảy bước

Solver mạnh chạy cùng một vòng lặp trên mọi bài lạ:

1. **Dựng mô hình** — diễn lại bài bằng đối tượng và phép toán, bỏ cốt
   truyện. "n cái đèn, đảo đoạn tiền tố" là mô hình; "pháp sư niệm chú"
   thì không.
2. **Tính ngân sách** — giới hạn → trần số phép toán → các họ ứng cử viên.
   Nếu trần ~3·10^8, một thuật O(n log^2 n) với n = 3·10^5 đã thuộc vùng
   "code ngay"; mải mốt tìm O(n) có thể *mất* điểm vì rủi ro cài đặt.
3. **Ứng cử viên** — liệt kê hai ba họ vừa ngân sách. Với mỗi họ, viết một
   câu khẳng định điều kiện cần đúng để họ đó dùng được.
4. **Đúng trước, nhanh sau** — trong các ứng cử viên, ý tưởng *đúng* rẻ
   nhất thắng. Thuật đơn giản mà pass hơn thuật thông minh bị TLE hoặc cài
   sai. Ưu tiên tính đúng đắn, rồi mới tốc độ.
5. **Kiểm chứng trước khi code** — tự tấn công ý tưởng của mình: n = 1, 2,
   mọi giá trị bằng nhau, input đã sắp / đảo ngược, trùng giá trị, giá trị
   cực trị. Sống sót thì code. Tự tìm ra điểm gãy là vừa tiết kiệm một lần
   nộp.
6. **Cài phòng thủ** — chỗ bạn tự tin nhất chính là chỗ sinh lỗi. Check
   sample bằng cách *truy vết chính code của mình*, không phải bằng niềm
   tin.
7. **Bảo vệ** — biết lời giải vì sao đúng (một đoạn văn) và nó chạy thế
   nào trên input xấu nhất. Không nói được cả hai nghĩa là chưa xong.

## Thời gian thực sự mất ở đâu

Hậu kiểm các kỳ thi cho thấy cùng mấy cái hố:

- code trước khi kiểm chứng ý tưởng (bỏ bước 5) — việc gỡ lỗi tốn gấp ba
  lần thời gian kiểm chứng;
- tối ưu trước khi có baseline *đúng* (đảo bước 4);
- đọc lại đề giữa chừng lúc đang code vì chưa bao giờ viết mô hình ra giấy
  (bỏ bước 1).

Quy trình không phải thủ tục hành chính — nó là thứ tự tối thiểu hóa tổng
thời gian, tính cả thời gian của sai lầm.
""",
)

write_lesson(
    M, "hsgm-m1-verify",
    "Verification Before Submission",
    "The adversarial checklist that catches most bugs before the judge does.",
    12,
    """
# Verification Before Submission

A submission is an experiment; run the experiment yourself first. The
checklist below catches the majority of wrong answers in practice:

## The tiny-n pass

Trace your algorithm by hand on n = 1, n = 2, n = 3. Most loop-bound and
off-by-one bugs live here, and hand-tracing takes seconds. If the code
branches on n, test both branches.

## The degenerate pass

- all values **equal** (hits tie-handling, duplicate logic);
- all values **distinct already** (hits "already satisfied" paths);
- **sorted ascending** and **sorted descending** (hits monotonicity
  assumptions and two-pointer directions);
- **extremes**: minimum and maximum allowed values, including negatives.

## The direction pass

For graph problems: does the edge direction match the statement? For
string problems: prefix vs suffix confusion? For ranges: inclusive vs
exclusive ends? These three are the most common silent misreads.

## The overflow pass

Count the bits. Sum of n values ≤ 10^9 each overflows int32 at n ≈ 2 —
long long from the start is cheaper than one WA. Products: n(n−1)/2 with
n = 10^5 is ~5·10^9, long long territory. A comparator that subtracts
integers can overflow — compare, don't subtract, unless you know the
range.

## The complexity pass

Multiply out the loops at max constraints. n·q with both 2·10^5 is 4·10^10
— dead. n log n with log = 18 is 3.6·10^6 per op-set — comfortable. If the
estimate is near the ceiling (~10^8–3·10^8), reduce constants before
coding: faster I/O, fewer modulo operations, flattened loops.

## The read-back pass

Re-read the statement *after* coding. Output format (trailing newline?
spaces?), multiple test cases per file, "if impossible print −1" clauses —
the requirements your code can satisfy while failing the check anyway.
""",
    "Kiểm chứng trước khi nộp",
    "Danh sách tấn công tự thân giúp bắt phần lớn lỗi trước khi máy chấm kịp thấy.",
    """
# Kiểm chứng trước khi nộp

Mỗi lần nộp là một thí nghiệm; hãy tự chạy thí nghiệm đó trước. Checklist
dưới đây bắt được phần lớn đáp án sai trong thực chiến:

## Lượt n nhỏ

Truy vết tay thuật toán với n = 1, n = 2, n = 3. Phần lớn lỗi cận vòng
lặp và lệch-một sống ở đây, và truy vết tay tốn vài giây. Nếu mã có nhánh
theo n, thử cả hai nhánh.

## Lượt suy biến

- mọi giá trị **bằng nhau** (chạm xử lý hòa, logic trùng lặp);
- mọi giá trị **đã phân biệt** (chạm nhánh "đã thỏa sẵn");
- **sắp tăng** và **sắp giảm** (chạm giả định đơn điệu và hướng two pointers);
- **cực trị**: giá trị nhỏ nhất/lớn nhất được phép, kể cả số âm.

## Lượt chiều

Với bài đồ thị: hướng cạnh có khớp đề không? Với xâu: nhầm tiền tố/hậu tố?
Với đoạn: đầu mút đóng hay mở? Ba chỗ này là những lần đọc nhầm thầm lặng
phổ biến nhất.

## Lượt tràn số

Đếm bit. Tổng n giá trị ≤ 10^9 mỗi giá trị tràn int32 khi n ≈ 2 — dùng
long long từ đầu rẻ hơn một lần WA. Phép nhân: n(n−1)/2 với n = 10^5 là
~5·10^9, đất long long. Comparator trừ hai số nguyên có thể tràn — hãy so
sánh, đừng trừ, trừ khi chắc phạm vi.

## Lượt độ phức tạp

Nhân các vòng lặp ở giới hạn lớn nhất. n·q với cả hai 2·10^5 là 4·10^10 —
chết. n log n với log = 18 là 3.6·10^6 mỗi nhóm phép — thoải mái. Nếu ước
tính sát trần (~10^8–3·10^8), giảm hằng số trước khi code: I/O nhanh hơn,
ít phép modulo hơn, làm phẳng vòng lặp.

## Lượt đọc lại

Đọc lại đề *sau* khi code xong. Định dạng output (dòng cuối? dấu cách?),
nhiều test trong một file, mệnh đề "nếu không khả thi in −1" — những yêu
cầu mà mã của bạn có thể thỏa mãn logic nhưng vẫn trượt check.
""",
)

# ----------------------------------------------------------------- practice
# Recognition + process drills: output the letter.
def letter(l):
    return CPP_STD + cpp('    out << "' + l + '";') + END


from hsgm import recognition_drill

D1, D1VI = recognition_drill(
    "hsgm-p1-d1", "Budget Check",
    "A problem has n ≤ 300000 and a 1 s limit (~3·10^8 ops ceiling). You have a correct O(n log^2 n) idea (≈ 3.3·10^8, borderline) and no O(n log n) idea yet. Best move?",
    ["Keep hunting for O(n log n) before writing anything",
     "Code the O(n log^2 n) now; optimize later only if needed",
     "Code O(n^2); it is simpler and surely correct",
     "Give up the problem and move on"],
    "B",
    "At ~3·10^8 the idea is code-it-now: the expected loss from more thinking usually exceeds the TLE risk. Code, test, and revisit only with time left.",
    vi_title="Kiểm tra ngân sách",
    vi_scenario="Bài có n ≤ 300000, giới hạn 1 s (~trần 3·10^8 phép). Bạn có ý tưởng O(n log^2 n) đúng (≈ 3.3·10^8, sát ngưỡng) và chưa có ý tưởng O(n log n). Nước đi tốt nhất?",
    vi_options=["Còn tìm O(n log n) trước khi viết gì cả",
                "Code O(n log^2 n) ngay; chỉ tối ưu khi cần",
                "Code O(n^2); đơn giản và chắc chắn đúng",
                "Bỏ bài, chuyển bài khác"],
    vi_hint="Sát ~3·10^8 là vùng code-ngay: thiệt hại do nghĩ thêm thường vượt rủi ro TLE. Code, test, chỉ quay lại nếu còn thời gian.",
)
D2, D2VI = recognition_drill(
    "hsgm-p1-d2", "Overflow Smell",
    "You must count pairs i < j in an array of n = 100000 elements; the count can reach ~5·10^9. Your comparator uses `a - b < 0` on values up to 10^9. What is the primary risk?",
    ["Neither — int handles 5·10^9 fine on 64-bit judges",
     "The count needs int64 (long long), and the subtracting comparator can overflow int",
     "Only the comparator is wrong; the count fits int",
     "Both are fine; overflow is only a Java problem"],
    "B",
    "5·10^9 exceeds 32-bit range (≈ 2.1·10^9): count in long long. And subtracting two ints up to 10^9 can overflow int in the comparator — compare directly.",
    vi_title="Dấu hiệu tràn số",
    vi_scenario="Cần đếm cặp i < j trong mảng n = 100000 phần tử; đáp án tới ~5·10^9. Comparator của bạn dùng `a - b < 0` trên giá trị tới 10^9. Rủi ro chính?",
    vi_options=["Không có gì — int chứa được 5·10^9 trên máy chấm 64-bit",
                "Đáp án cần int64 (long long), và comparator trừ hai số có thể tràn int",
                "Chỉ comparator sai; đáp án vừa int",
                "Cả hai ổn; tràn số chỉ là vấn đề của Java"],
    vi_hint="5·10^9 vượt 32-bit (≈ 2.1·10^9): đếm bằng long long. Và trừ hai int tới 10^9 có thể tràn trong comparator — hãy so sánh trực tiếp.",
)
D3, D3VI = recognition_drill(
    "hsgm-p1-d3", "Which Simplest-Correct?",
    "n ≤ 5000, you need the maximum sum of a contiguous subarray. You see Kadane O(n) instantly. The safest professional move is:",
    ["Skip hand-tracing since Kadane is famous",
     "Hand-trace Kadane on an all-negative array before coding",
     "Code O(n^2) instead because it is safer",
     "Binary search the answer first"],
    "B",
    "Kadane's famous pitfall is the all-negative array (must return the max element, not 0). The verification pass exists precisely for famous-but-tricky code.",
    vi_title="Chọn cái đúng-rẻ-nhất",
    vi_scenario="n ≤ 5000, cần tổng đoạn con liên tiếp lớn nhất. Bạn thấy ngay Kadane O(n). Nước đi chuyên nghiệp an toàn nhất:",
    vi_options=["Bỏ truy vết tay vì Kadane nổi tiếng",
                "Truy vết tay Kadane trên mảng toàn âm trước khi code",
                "Code O(n^2) thay thế vì an toàn hơn",
                "Tìm kiếm nhị phân đáp án trước"],
    vi_hint="Bẫy nổi tiếng của Kadane là mảng toàn âm (phải trả phần tử lớn nhất, không phải 0). Lượt kiểm chứng tồn tại chính vì mã nổi-tưng-nhưng-khó.",
)

write_practice(
    M, "hsgm-p1-drills", "Process Drills",
    "Three decision drills about the pipeline itself: budgeting, overflow smells, and verification-first.",
    "Drill quy trình",
    "Ba bài quyết định về chính quy trình: ngân sách, dấu hiệu tràn số, và kiểm-chứng-trước.",
    "hsgm-m1-verify", 25, "advanced",
    [D1, D2, D3],
    {"hsgm-p1-d1": D1VI, "hsgm-p1-d2": D2VI, "hsgm-p1-d3": D3VI},
    solutions=[
        ("hsgm-p1-d1", letter("B"), letter("A")),
        ("hsgm-p1-d2", letter("B"), letter("A")),
        ("hsgm-p1-d3", letter("B"), letter("A")),
    ],
)

# --------------------------------------------------------------- checkpoint
# Real task: process under pressure — a task with a hidden edge case that
# the verification checklist catches (all-equal + negatives + overflow).
# Task: max non-empty subarray sum, n up to 2·10^5 (Kadane) — but with the
# twist that ALL values can be negative (the classic Kadane trap) and the
# answer can overflow int.
CP_M1_IN = T("6", "-3 -1 -4 -1 -5 -9")
CP_M1_IN2 = T("8", "10 9 8 8 8 -100 8 8")
CP_M1_IN3 = T("3", "1000000000 1000000000 1000000000")

CP1C = challenge(
    "hsgm-cp-m1-maxsum",
    "Checkpoint: Max Subarray, Defended",
    """**Task.** Given n integers (possibly all negative), find the maximum sum
of a non-empty contiguous subarray.

**Constraints:** 1 ≤ n ≤ 200000; |a[i]| ≤ 10^9.

**Process requirements (this is the mastery point):**
- Verify on the all-negative case BEFORE trusting Kadane's dp[0] = 0 habit.
- The answer for n = 3 equal 10^9 values is 3·10^9 — outside int range.
- A single O(n) pass suffices; anything slower is wasted effort.
""",
    [
        contest_test("all negative", CP_M1_IN, T("-1"),
            "Whole array is one subarray; the max single element is -1. dp[0] = a[0], not 0."),
        contest_test("ties and negatives", CP_M1_IN2, T("43"),
            "10+9+8+8+8 = 43; the -100 splits the array, and the trailing 8 8 cannot beat 43."),
        contest_test("overflow check", CP_M1_IN3, T("3000000000"),
            "3·10^9 overflows int32 — the running sum must be long long."),
    ],
    level="independent",
    difficulty="advanced",
)
CP1VI = vi_challenge(
    "Điểm kiểm tra: đoạn con lớn nhất, có bảo vệ",
    """**Bài toán.** Cho n số nguyên (có thể toàn âm), tìm tổng lớn nhất của một
đoạn con liên tiếp khác rỗng.

**Ràng buộc:** 1 ≤ n ≤ 200000; |a[i]| ≤ 10^9.

**Yêu cầu quy trình (điểm mastery nằm ở đây):**
- Kiểm chứng trường hợp toàn âm TRƯỚC khi tin thói quen dp[0] = 0 của Kadane.
- Đáp án với n = 3 giá trị 10^9 là 3·10^9 — ngoài phạm vi int.
- Một lượt O(n) là đủ; chậm hơn là phí.
""",
    [("toàn âm", "Cả mảng là một đoạn; phần tử lớn nhất là -1. dp[0] = a[0], không phải 0."),
     ("hòa và âm", "10+9+8+8+8 = 43; khoản −100 cắt đôi, hai số 8 cuối không thắng 43."),
     ("kiểm tra tràn", "3·10^9 tràn int32 — tổng chạy phải là long long.")],
)

CP_M1_R = CPP_STD + cpp("""    int n; in >> n;
    long long best = LLONG_MIN, cur = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        cur = max(x, cur + x);          // extend or restart AT the element
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END

CP_M1_W = CPP_STD + cpp("""    int n; in >> n;
    long long best = 0, cur = 0;      // BUG: best and cur start at 0 — the
    for (int i = 0; i < n; ++i) {     // all-negative case wrongly reports 0
        long long x; in >> x;
        cur = max(x, cur + x);
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m1", "Checkpoint — Defend the Baseline",
    "Kadane under adversarial cases: all-negative input, int overflow, and the dp[0] habit. The pipeline's verification pass is the graded skill.",
    25,
    """
**Checkpoint — Defend the Baseline.** The task is famous; the grading is not.
The full-scale tests embed exactly the cases the verification checklist
names: an all-negative array (where dp[0] = 0 fails silently), a
tie-and-split case, and an overflow probe. If your first instinct is "I
know Kadane", run the checklist anyway — that habit IS the course.
""",
    "Điểm kiểm tra — Bảo vệ baseline",
    "Kadane dưới các trường hợp adversarial: mảng toàn âm, tràn int, và thói quen dp[0]. Kỹ năng được chấm là lượt kiểm chứng trong quy trình.",
    """
**Điểm kiểm tra — Bảo vệ baseline.** Bài toán nổi tiếng; phần chấm thì không.
Các test ở giới hạn nhúng đúng những trường hợp checklist kiểm chứng gọi
tên: mảng toàn âm (nơi dp[0] = 0 sai thầm lặng), trường hợp hòa-và-cắt, và
một lần dò tràn số. Nếu phản xạ đầu là "tôi biết Kadane", vẫn chạy
checklist — thói quen đó CHÍNH LÀ khóa học.
""",
    CP1C,
    CP1VI,
    CP_M1_R,
    CP_M1_W,
)

print("module m1 complete")
