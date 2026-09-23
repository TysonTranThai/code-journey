#!/usr/bin/env python3
"""HSG Intensive — Module 6: hsgx-stress (Stress Testing).

The 3-program harness from the Vietnamese CP community (thuật cần stress +
thuật chắc chắn đúng + thuật sinh test), executed for real: each challenge's
solve() runs a differential loop INSIDE the program — candidate vs brute —
on many generated cases, and reports whether they ever disagree.

Conventions: T() real newlines; cpp() → \n escapes; explicit includes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgx import (
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
#include <string>
#include <utility>
#include <random>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgx-stress"
write_module(
    M,
    "Stress Testing",
    "The differential harness: brute force as oracle, random generators with seeds, and a compare loop that finds what your eyes cannot. Executed inside the sandbox.",
    "Stress test",
    "Bộ harness vi phân: brute force làm oracles, bộ sinh test ngẫu nhiên có seed, và vòng so sánh tìm ra điều mắt thường không thấy. Thực thi thật trong sandbox.",
    ["hsgx-m6-harness", "hsgx-m6-generators", "hsgx-cp-m6"],
    ["hsgx-p6-stress"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgx-m6-harness",
    "The Differential Harness",
    "Three programs, one loop: candidate, oracle, generator — and the discipline of seeds, bounds, and stopping.",
    25,
    """
# The Differential Harness

VNOI's "viết trình chấm" and every serious competitive programmer's arsenal
share one shape: three programs and a loop.

```
repeat forever:
    input  = generator(seed++)
    a      = candidate(input)   # the solution you trust? prove it
    b      = oracle(input)      # slow but certainly correct
    if a != b:
        save input; stop        # you found the bug
```

## Why it works

Human-written tests are biased toward what you *think* the code does. A
random generator is unbiased: it eventually hits the exact shape your bug
needs — the tie you mishandled, the empty range you never considered, the
order that breaks your greedy. On tiny inputs the oracle is fast enough to
check thousands of cases per second.

## The oracle is the hard part

It must be **too simple to be wrong**: full enumeration, O(n!) with n ≤ 8,
or a completely different algorithm than the candidate. Never reuse the
candidate's code inside the oracle — shared bugs survive differential
testing (that is its one blind spot).

## Seeds and reproducibility

Never use unseeded randomness: a bug you cannot reproduce is a bug you
cannot fix. Derive the generator from an explicit counter (`mt19937 rng(seed++)
`), and print the seed with the failing case. The saved input is the
minimal contract: it must reproduce the disagreement exactly.

## Stopping and time budgeting

In a real contest you have maybe 10–20 minutes of stress testing. Decide
the budget up front (e.g. 5000 cases), and if no disagreement is found,
your confidence grows — but a pass is never a proof, only a bound. When
the oracle is too slow, shrink n until it isn't (n ≤ 8 checks thousands of
cases; n ≤ 100 checks hundreds — still a strong net).

## In this course the harness runs for real

Every challenge below embeds the loop inside `solve()`: generate, compare
candidate vs oracle, print `OK trials` if all agree, print `MISMATCH` plus
the case if they ever disagree. The tests grade exactly that.
""",
    "Bộ harness vi phân",
    "Ba chương trình, một vòng lặp: ứng cử viên, oracles, bộ sinh — và kỷ luật về seed, biên, và điểm dừng.",
    """
# Bộ harness vi phân

"Viết trình chấm" của VNOI và kho vũ khí của mọi lập trình viên thi đấu nghiêm
túc đều chung một hình dạng: ba chương trình và một vòng lặp.

```
lặp mãi mãi:
    input  = generator(seed++)
    a      = candidate(input)   # lời giải bạn tin? chứng minh đi
    b      = oracle(input)      # chậm nhưng chắc chắn đúng
    if a != b:
        lưu input; dừng         # bạn tìm ra lỗi rồi
```

## Vì sao nó hiệu quả

Test do người viết thì thiên về điều bạn *nghĩ* code làm. Bộ sinh ngẫu nhiên
không thiên vị: cuối cùng nó chạm đúng hình dạng lỗi của bạn cần — trường hợp
hòa bạn xử sai, khoảng rỗng bạn chưa từng nghĩ tới, thứ tự phá vỡ greedy của
bạn. Với đầu vào nhỏ, oracle đủ nhanh để kiểm tra hàng nghìn trường hợp mỗi giây.

## Oracle mới là phần khó

Nó phải **đơn giản đến mức không thể sai**: liệt kê đầy đủ, O(n!) với n ≤ 8,
hoặc một thuật toán hoàn toàn khác ứng cử viên. Không bao giờ tái sử dụng code
của ứng cử viên bên trong oracle — lỗi dùng chung sống sót qua stress test
(đó là điểm mù duy nhất của nó).

## Seed và khả năng tái lập

Không bao giờ dùng ngẫu nhiên không seed: lỗi không tái lập được là lỗi không
thể sửa. Dẫn xuất bộ sinh từ một bộ đếm tường minh (`mt19937 rng(seed++)`),
và in seed cùng trường hợp gãy. Đầu vào đã lưu là hợp đồng tối thiểu: nó phải
tái lập chính xác sự bất đồng.

## Điểm dừng và phân bổ thời gian

Trong kỳ thi thật bạn có cỡ 10–20 phút stress test. Quyết định ngân sách trước
(ví dụ 5000 case), và nếu không tìm thấy bất đồng, độ tin cậy tăng lên — nhưng
một lượt qua không bao giờ là chứng minh, chỉ là một biên. Khi oracle quá chậm,
giảm n cho tới khi nhanh (n ≤ 8 kiểm hàng nghìn case; n ≤ 100 kiểm hàng trăm —
vẫn là tưới lưới mạnh).

## Trong khóa này harness chạy thật

Mỗi thử thách dưới đây nhúng vòng lặp vào trong `solve()`: sinh, so ứng cử viên
với oracle, in `OK trials` nếu mọi thứ khớp, in `MISMATCH` kèm case nếu từng
bất đồng. Các test chấm đúng điều đó.
""",
)

write_lesson(
    M, "hsgx-m6-generators",
    "Writing Generators That Find Bugs",
    "Uniform randomness is not enough: distributions, special shapes, and how to aim the generator at a suspected bug class.",
    25,
    """
# Writing Generators That Find Bugs

A generator is a hypothesis about where your bug lives, written as code.

## Uniform is the floor, not the ceiling

`uniform_int(1, n)` finds common bugs. But most surviving bugs need
*structure*: equal values (ties), sorted or reverse-sorted input (order
assumptions), tiny values (overflow-free-but-wrong logic), duplicates
(dedup bugs), a single extreme outlier (branch bugs). Aim deliberately:

- **Bug suspect: tie-breaking** → generate from {1, 2, 3} only.
- **Bug suspect: boundaries** → n tiny (0, 1, 2), values at extremes.
- **Bug suspect: order** → generate sorted, then occasionally shuffled.
- **Bug suspect: overflow** → values near INT_MAX/2 so sums exceed 2^31.

## The parameter sweep

Generate over the whole shape space: for t trials, pick n randomly from
{0..10}, then values from a randomly chosen distribution among uniform /
constant / two-valued / sorted / reversed. This mixed generator beats any
single fixed distribution — it is what found most real bugs in judges'
history and in your own future contests.

## Reading a mismatch

When candidate ≠ oracle, don't patch the code immediately. First *shrink*
the failing case: remove elements while the disagreement persists (simple
delta debugging). The minimal case usually reveals the bug in one glance —
and doubles as the regression test you add permanently.

## From stress loop to submission

Contest workflow: keep the harness in a separate file. Once 5000+ cases
pass, delete nothing — just stop including it. The discipline is: no
"seems right" submissions on problems where a brute-force oracle is
writable in five minutes. Five minutes of harness beats an hour of
debugging by print statements.
""",
    "Viết bộ sinh test tìm ra lỗi",
    "Ngẫu nhiên đều không đủ: phân phối, hình dạng đặc biệt, và cách nhắm bộ sinh vào lớp lỗi nghi ngờ.",
    """
# Viết bộ sinh test tìm ra lỗi

Một bộ sinh là một giả thuyết về nơi lỗi của bạn sống, được viết thành code.

## Đều là sàn, không phải trần

`uniform_int(1, n)` tìm ra các lỗi phổ thông. Nhưng phần lớn lỗi sống sót cần
*cấu trúc*: giá trị bằng nhau (trường hợp hòa), đầu vào đã sắp hoặc đảo ngược
(giả định thứ tự), giá trị tí hon (logic sai nhưng không tràn), trùng lặp (lỗi
khử trùng), một ngoại lệ cực đoan duy nhất (lỗi nhánh). Nhắm có chủ đích:

- **Nghi ngờ: xử lý hòa** → sinh từ {1, 2, 3} thôi.
- **Nghi ngờ: biên** → n tí hon (0, 1, 2), giá trị ở cực trị.
- **Nghi ngờ: thứ tự** → sinh đã sắp, thi thoảng xáo trộn.
- **Nghi ngờ: tràn số** → giá trị gần INT_MAX/2 để tổng vượt 2^31.

## Quét tham số

Sinh trên toàn bộ không gian hình dạng: mỗi vòng, chọn n ngẫu nhiên từ
{0..10}, rồi giá trị từ một phân phối ngẫu nhiên trong đều / hằng / hai-giá-trị /
đã-sắp / đảo-ngược. Bộ sinh hỗn hợp này đánh bại mọi phân phối cố định đơn lẻ —
chính nó tìm ra phần lớn lỗi thật trong lịch sử các hệ chấm.

## Đọc một mismatch

Khi ứng cử viên ≠ oracle, đừng vá code ngay. Trước tiên *thu nhỏ* case gãy:
bỏ phần tử trong khi sự bất đồng còn (delta debugging đơn giản). Case tối
tiểu thường lộ lỗi trong một cái nhìn — và là test hồi quy bạn thêm vĩnh viễn.

## Từ vòng stress tới bài nộp

Quy trình thi đấu: giữ harness ở tệp riêng. Khi 5000+ case qua, không xóa gì
hết — chỉ ngừng nhúng nó. Kỷ luật là: không nộp "có vẻ đúng" với bài mà
oracle brute-force viết được trong năm phút. Năm phút harness đáng hơn một
giờ debug bằng lệnh in.
""",
)

# ----------------------------------------------------------------- practice
# S1: is a sequence's max-pairwise-xor? candidate = sort-based neighbor scan? No —
# classic: candidate = O(n log n) greedy? Instead: max subarray sum (Kadane vs brute).
S1_R = CPP_STD + cpp("""    // Harness: Kadane (candidate) vs O(n^2) brute (oracle).
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    mt19937 rng(12345);
    auto kadane = [&](const vector<long long>& v) {
        long long best = LLONG_MIN, cur = 0;
        for (long long x : v) { cur = max(x, cur + x); best = max(best, cur); }
        return best;
    };
    auto brute = [&](const vector<long long>& v) {
        long long best = LLONG_MIN;
        for (size_t i = 0; i < v.size(); ++i) {
            long long s = 0;
            for (size_t j = i; j < v.size(); ++j) { s += v[j]; best = max(best, s); }
        }
        return best;
    };
    const int TRIALS = 3000;
    for (int t = 0; t < TRIALS; ++t) {
        int len = 1 + (int)(rng() % 9);
        vector<long long> v(len);
        int mode = (int)(rng() % 4);
        for (auto& x : v) {
            if (mode == 0) x = (long long)(rng() % 11) - 5;         // small mix
            else if (mode == 1) x = -(long long)(rng() % 5);        // non-positive
            else if (mode == 2) x = (long long)(rng() % 2) * 6 - 3; // two values
            else x = (long long)(rng() % 7) - 3;                    // uniform
        }
        if (kadane(v) != brute(v)) {
            out << "MISMATCH trial " << t << "{{NL}}";
            return;
        }
    }
    out << "OK " << TRIALS << "{{NL}}";
""") + END

S1_W = CPP_STD + cpp("""    // WRONG candidate: resets cur whenever it dips negative — but forgets
    // the all-negative case handling the oracle catches (subtle: best is
    // initialized to 0 instead of the first element).
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    mt19937 rng(12345);
    auto cand = [&](const vector<long long>& v) {
        long long best = 0, cur = 0;              // BUG: 0 initial best
        for (long long x : v) { cur = max(x, cur + x); best = max(best, cur); }
        return best;
    };
    auto brute = [&](const vector<long long>& v) {
        long long best = LLONG_MIN;
        for (size_t i = 0; i < v.size(); ++i) {
            long long s = 0;
            for (size_t j = i; j < v.size(); ++j) { s += v[j]; best = max(best, s); }
        }
        return best;
    };
    const int TRIALS = 3000;
    for (int t = 0; t < TRIALS; ++t) {
        int len = 1 + (int)(rng() % 9);
        vector<long long> v(len);
        int mode = (int)(rng() % 4);
        for (auto& x : v) {
            if (mode == 0) x = (long long)(rng() % 11) - 5;
            else if (mode == 1) x = -(long long)(rng() % 5);
            else if (mode == 2) x = (long long)(rng() % 2) * 6 - 3;
            else x = (long long)(rng() % 7) - 3;
        }
        if (cand(v) != brute(v)) {
            out << "MISMATCH trial " << t << "{{NL}}";
            return;
        }
    }
    out << "OK " << TRIALS << "{{NL}}";
""") + END

# S2: is_sorted-with-one-removal checker vs brute
S2_R = CPP_STD + cpp("""    // Harness: "can delete at most one element to make sorted?" candidate
    // (linear scan) vs brute (try deleting each index).
    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    mt19937 rng(777);
    auto cand = [](const vector<int>& v) {
        int bad = -1;
        for (size_t i = 1; i < v.size(); ++i) {
            if (v[i - 1] > v[i]) { if (bad != -1) return false; bad = (int)i; }
        }
        if (bad == -1) return true;
        auto w = v; w.erase(w.begin() + bad);
        bool okA = true;
        for (size_t i = 1; i < w.size(); ++i) if (w[i - 1] > w[i]) { okA = false; break; }
        if (okA) return true;
        // also try deleting the left element of the violation
        if (bad == 0) return false;
        auto w2 = v; w2.erase(w2.begin() + bad - 1);
        for (size_t i = 1; i < w2.size(); ++i) if (w2[i - 1] > w2[i]) return false;
        return true;
    };
    auto brute = [](const vector<int>& v) {
        if (v.size() <= 1) return true;
        for (size_t d = 0; d < v.size(); ++d) {
            vector<int> w;
            for (size_t i = 0; i < v.size(); ++i) if (i != d) w.push_back(v[i]);
            bool ok = true;
            for (size_t i = 1; i < w.size(); ++i) if (w[i - 1] > w[i]) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    };
    const int TRIALS = 4000;
    for (int t = 0; t < TRIALS; ++t) {
        int len = (int)(rng() % 8);
        vector<int> v(len);
        for (auto& x : v) x = (int)(rng() % 5);   // heavy ties: tie bugs surface
        if (cand(v) != brute(v)) {
            out << "MISMATCH trial " << t << "{{NL}}";
            return;
        }
    }
    out << "OK " << TRIALS << "{{NL}}";
""") + END

S2_W = CPP_STD + cpp("""    // WRONG candidate: counts violations; assumes one violation is always
    // fixable (ignores which side to delete and second violations).
    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    mt19937 rng(777);
    auto cand = [](const vector<int>& v) {
        int bad = 0;
        for (size_t i = 1; i < v.size(); ++i) if (v[i - 1] > v[i]) ++bad;
        return bad <= 1;
    };
    auto brute = [](const vector<int>& v) {
        if (v.size() <= 1) return true;
        for (size_t d = 0; d < v.size(); ++d) {
            vector<int> w;
            for (size_t i = 0; i < v.size(); ++i) if (i != d) w.push_back(v[i]);
            bool ok = true;
            for (size_t i = 1; i < w.size(); ++i) if (w[i - 1] > w[i]) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    };
    const int TRIALS = 4000;
    for (int t = 0; t < TRIALS; ++t) {
        int len = (int)(rng() % 8);
        vector<int> v(len);
        for (auto& x : v) x = (int)(rng() % 5);
        if (cand(v) != brute(v)) {
            out << "MISMATCH trial " << t << "{{NL}}";
            return;
        }
    }
    out << "OK " << TRIALS << "{{NL}}";
""") + END

S3_R = CPP_STD + cpp("""    // Harness: majority element (candidate: Boyer-Moore with verification)
    // vs brute (count each value).
    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    mt19937 rng(2024);
    auto cand = [](const vector<int>& v) {
        // Boyer-Moore + verify; returns element or -1 (no strict majority)
        int c = 0; int cand2 = 0;
        for (int x : v) { if (c == 0) cand2 = x; c += (x == cand2) ? 1 : -1; }
        int cnt = 0;
        for (int x : v) if (x == cand2) ++cnt;
        return (2 * cnt > (int)v.size()) ? cand2 : -1;
    };
    auto brute = [](const vector<int>& v) {
        for (int x : v) {
            int cnt = 0;
            for (int y : v) if (y == x) ++cnt;
            if (2 * cnt > (int)v.size()) return x;
        }
        return -1;
    };
    const int TRIALS = 4000;
    for (int t = 0; t < TRIALS; ++t) {
        int len = (int)(rng() % 10);
        vector<int> v(len);
        int dom = (int)(rng() % 3);   // sometimes a dominant value exists
        for (auto& x : v) x = (rng() % 3 == 0) ? (int)(rng() % 5) : dom;
        if (cand(v) != brute(v)) {
            out << "MISMATCH trial " << t << "{{NL}}";
            return;
        }
    }
    out << "OK " << TRIALS << "{{NL}}";
""") + END

S3_W = CPP_STD + cpp("""    // WRONG candidate: Boyer-Moore WITHOUT verification — returns the
    // residual candidate even when no majority exists (the classic trap).
    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    mt19937 rng(2024);
    auto cand = [](const vector<int>& v) {
        int c = 0; int cand2 = 0;
        for (int x : v) { if (c == 0) cand2 = x; c += (x == cand2) ? 1 : -1; }
        return v.empty() ? -1 : cand2;   // BUG: no verification pass
    };
    auto brute = [](const vector<int>& v) {
        for (int x : v) {
            int cnt = 0;
            for (int y : v) if (y == x) ++cnt;
            if (2 * cnt > (int)v.size()) return x;
        }
        return -1;
    };
    const int TRIALS = 4000;
    for (int t = 0; t < TRIALS; ++t) {
        int len = (int)(rng() % 10);
        vector<int> v(len);
        int dom = (int)(rng() % 3);
        for (auto& x : v) x = (rng() % 3 == 0) ? (int)(rng() % 5) : dom;
        if (cand(v) != brute(v)) {
            out << "MISMATCH trial " << t << "{{NL}}";
            return;
        }
    }
    out << "OK " << TRIALS << "{{NL}}";
""") + END

S1_CH = challenge(
    "hsgx-p6-s1-kadane", "Stress: Segment Sum Oracle",
    """**Bài toán.** Two implementations of max segment sum are compiled below:
a candidate and an O(n²) oracle. Run a differential harness of 3000 random
trials (seeds 12345..., lengths 1–9, four value distributions) and print
`OK 3000` if every trial agrees, or `MISMATCH trial <t>` at the first
disagreement.

**The candidate below is deliberately broken in one small way — your
harness must expose it.** Fix it so the full loop prints OK.
""",
    [
        contest_test("harness run", T("1"), T("OK 3000"),
            "The reference passes all 3000 trials; the broken candidate hits a MISMATCH (all-negative arrays: best initialized to 0)."),
    ],
    level="debugging",
    difficulty="advanced",
)

S2_CH = challenge(
    "hsgx-p6-s2-removeone", "Stress: Delete-One Checker",
    """**Bài toán.** Implement (and stress-test) the predicate: can at most one
element be deleted from the array so it becomes non-decreasing? Candidate:
a linear scan; oracle: try deleting every index. 4000 trials, seed 777,
heavy ties (values 0–4).

**A plausible candidate is provided — it counts violations and assumes ≤ 1
violation is fixable. Your differential loop must catch it.** Fix the
candidate (delete the correct side; re-check).
""",
    [
        contest_test("harness run", T("1"), T("OK 4000"),
            "The fixed candidate passes; the violation-counter fails on cases like [3,3,2,2] (one violation, not fixable by one delete... actually fixable? verify via oracle) or [2,3,1,1]."),
    ],
    level="debugging",
    difficulty="advanced",
)

S3_CH = challenge(
    "hsgx-p6-s3-majority", "Stress: Majority With Proof",
    """**Bài toán.** Boyer–Moore finds a majority *candidate*; a verification
pass is required to confirm a strict majority (> half). Stress 4000 trials,
seed 2024, arrays with a sometimes-dominant value; oracle: direct counting.

**The broken version skips verification — your harness must catch it.**
Fix it.
""",
    [
        contest_test("harness run", T("1"), T("OK 4000"),
            "Verification pass added: the residual candidate is counted; if ≤ half, answer −1. The unverified version returns ghost majorities."),
    ],
    level="debugging",
    difficulty="advanced",
)

write_practice(
    M, "hsgx-p6-stress", "Stress Drill — Three Harnesses",
    "Run three differential harnesses (Kadane, delete-one, Boyer-Moore) against brute oracles; the broken candidates are exposed by the loop, and you fix them.",
    "Drill stress — Ba harness",
    "Chạy ba harness vi phân (Kadane, xóa-một, Boyer-Moore) đối đầu oracle brute; các ứng cử viên gãy bị lộ bằng vòng lặp, và bạn sửa chúng.",
    "hsgx-m6-generators",
    90,
    "advanced",
    [S1_CH, S2_CH, S3_CH],
    {
        "hsgx-p6-s1-kadane": vi_challenge(
            "Stress: Oracle tổng đoạn",
            "**Bài toán.** Hai bản cài max tổng đoạn: ứng cử viên và oracle O(n²). Chạy harness 3000 vòng ngẫu nhiên (seed 12345..., độ dài 1–9, bốn phân phối); in `OK 3000` nếu mọi vòng khớp, hoặc `MISMATCH trial <t>` tại bất đồng đầu tiên. Ứng cử viên bị phá cố ý một chỗ — harness của bạn phải lộ nó. Sửa để in OK.",
            [("harness chạy", "Bản chuẩn qua cả 3000 vòng; ứng cử viên gãy dính MISMATCH (mảng toàn âm: best khởi tạo 0).")],
        ),
        "hsgx-p6-s2-removeone": vi_challenge(
            "Stress: Bộ kiểm xóa-một",
            "**Bài toán.** Cài đặt và stress test vị từ: có thể xóa tối đa một phần tử để dãy trở thành không giảm? Ứng cử viên: quét tuyến tính; oracle: thử xóa từng chỉ số. 4000 vòng, seed 777, nhiều giá trị hòa. Ứng cử viên đếm-violation bị lộ. Sửa nó.",
            [("harness chạy", "Ứng cử viên đã sửa qua hết; bộ đếm violation gãy trên các dãy hòa như [3,3,2,2].")],
        ),
        "hsgx-p6-s3-majority": vi_challenge(
            "Stress: Đa số có chứng minh",
            "**Bài toán.** Boyer–Moore tìm *ứng cử viên* đa số; cần một lượt kiểm chứng để xác nhận đa số nghiêm ngặt (> một nửa). Stress 4000 vòng, seed 2024; oracle: đếm trực tiếp. Bản lỗi bỏ qua kiểm chứng — harness phải bắt được. Sửa nó.",
            [("harness chạy", "Đã thêm lượt kiểm chứng: ứng cử viên dư được đếm lại; nếu ≤ một nửa, đáp án −1.")],
        ),
    },
    solutions=[
        ("hsgx-p6-s1-kadane", S1_R, S1_W),
        ("hsgx-p6-s2-removeone", S2_R, S2_W),
        ("hsgx-p6-s3-majority", S3_R, S3_W),
    ],
)

# --------------------------------------------------------------- checkpoint
# The full harness experience: a subtle sort-based bug found only by stress.
CP_M6_R = S2_R
CP_M6_W = S2_W

write_checkpoint(
    M, "hsgx-cp-m6", "Checkpoint — Trust the Loop, Not Your Eyes",
    "The delete-one checker at full strength: 4000 tie-heavy trials against a deletion oracle. Fix the counting shortcut and make the whole harness print OK.",
    20,
    """
**Điểm kiểm tra — Tin vòng lặp, đừng tin mắt.** The predicate "removable
into non-decreasing order" under heavy ties. The violation-counter passes
small eyeball tests and fails the harness. Replace it with the correct
linear candidate (locate the violation, try deleting either neighbor,
re-verify) so all 4000 trials agree with the oracle.
""",
    "Điểm kiểm tra — Tin vòng lặp, đừng tin mắt.",
    "Vị từ \"xóa được để thành không giảm\" với nhiều giá trị hòa. Bộ đếm violation qua các test nhỏ nhìn bằng mắt và gãy trước harness. Thay bằng ứng cử viên tuyến tính đúng (tìm violation, thử xóa một trong hai bên, kiểm lại) để cả 4000 vòng khớp oracle.",
    """
**Điểm kiểm tra — Tin vòng lặp, đừng tin mắt.** Vị từ "xóa được để thành
không giảm" với nhiều giá trị hòa. Bộ đếm violation qua các test nhỏ nhìn
bằng mắt và gãy trước harness. Thay bằng ứng cử viên tuyến tính đúng (tìm
violation, thử xóa một trong hai bên, kiểm lại) để cả 4000 vòng khớp oracle.
""",
    CP_CH6 := challenge(
        "hsgx-cp-m6-removeone", "Checkpoint: The Delete-One Verdict",
        """**Bài toán.** As practiced: implement the corrected linear candidate for
"delete at most one element → non-decreasing" and run the 4000-trial
harness (seed 777, values 0–4) against the deletion oracle.

**Output:** `OK 4000` when the harness passes.
""",
        [
            contest_test("harness run", T("1"), T("OK 4000"),
                "All trials agree with the oracle."),
        ],
        level="debugging",
        difficulty="advanced",
    ),
    vi_challenge(
        "Điểm kiểm tra: Phán quyết xóa-một",
        "**Bài toán.** Như đã luyện: cài ứng cử viên tuyến tính đã sửa cho vị từ \"xóa tối đa một phần tử → không giảm\" và chạy harness 4000 vòng (seed 777, giá trị 0–4) đối đầu oracle xóa-từng-chỉ-số. **Đầu ra:** `OK 4000` khi harness qua.",
        [("harness chạy", "Mọi vòng khớp với oracle.")],
    ),
    CP_M6_R,
    CP_M6_W,
)

print("module m6 complete")
