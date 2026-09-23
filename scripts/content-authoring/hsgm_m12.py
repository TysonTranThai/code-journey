#!/usr/bin/env python3
"""HSG Mastery — Module 12: hsgm-adversary (Counterexample & Adversarial Lab).

Breaking your own solutions: the adversarial checklist, minimal
counterexample construction, and the discipline of proving before trusting.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgm import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test, recognition_drill,
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL


def letter(l):
    return CPP_STD + cpp('    out << "' + l + '";') + END


M = "hsgm-adversary"
write_module(
    M,
    "Counterexample and Adversarial Lab",
    "Attacking your own solution before the judge does: the adversarial checklist (ties, asymmetry, degeneracy, scale), minimal counterexample construction, and proof-first trust.",
    "Phòng thí nghiệm phản ví dụ và phản đốidraulic",
    "Tấn công lời giải của chính mình trước khi trình chấm làm: danh mục phản đốidraulic (hòa, bất đối xứng, thoái hóa, thang lớn), dựng phản ví dụ tối giản, và tin-từ-chứng-minh.",
    ["hsgm-m12-checklist", "hsgm-m12-minimal", "hsgm-cp-m12"],
    ["hsgm-p12-drills"],
)

write_lesson(
    M, "hsgm-m12-checklist",
    "The Adversarial Checklist",
    "Five input shapes break most unproven solutions. Run the checklist on every solution you are proud of.",
    12,
    """
# The Adversarial Checklist

Before trusting any solution, attack it with these five shapes:

1. **All ties.** Every element equal; every weight identical; every
   deadline the same. Tie-break branches that never ran on random data
   run now.
2. **Asymmetry.** A path graph; one huge element among tiny ones; an
   interval swallowing all others. Symmetric data flatters symmetric
   bugs.
3. **Degeneracy.** n = 1; n = 0 if legal; empty ranges; single-point
   intervals; self-loops; duplicates everywhere.
4. **Extremes.** Maximum values (overflow), minimum values (underflow of
   assumptions like "positive"), alternating max/min patterns that
   maximize comparison counts.
5. **Adversarial order.** Sorted-descending input to a "sort then
   process" claim; reversed trees; queries ordered worst-case-first.

## The mindset

For each shape, the question is not "will my code break?" but **"what
would I input if I were trying to break it?"** That inversion finds
bugs that rereading never will, because you wrote the code and your
brain auto-corrects while reading.

## Cost-benefit

The checklist costs minutes. A wrong submission costs the problem, the
confidence, and often the contest. There is no scenario where skipping
the checklist is correct arithmetic.
""",
    "Danh mục phản đốidraulic",
    "Năm hình dạng input phá phần lớn lời giải chưa chứng minh. Chạy danh mục trên mọi lời giải bạn tự hào.",
    """
# Danh mục phản đốidraulic

Trước khi tin bất kỳ lời giải nào, tấn công nó bằng năm hình dạng này:

1. **Toàn hòa.** Mọi phần tử bằng nhau; mọi trọng số giống nhau; mọi
   deadline như nhau. Các nhánh tie-break chưa từng chạy trên dữ liệu
   ngẫu nhiên giờ chạy.
2. **Bất đối xứng.** Đồ thị đường; một phần tử khổng lồ giữa các phần tử
   tí hon; một đoạn nuốt mọi đoạn khác. Dữ liệu đối xứng nịnh các bug
   đối xứng.
3. **Thoái hóa.** n = 1; n = 0 nếu hợp lệ; miền rỗng; đoạn một điểm;
   khuyên tự vòng; trùng lặp khắp nơi.
4. **Cực trị.** Giá trị tối đa (tràn), giá trị tối thiểu (sập các giả
   định kiểu "dương"), mẫu xen kẽ max/min tối đa hóa số phép so sánh.
5. **Thứ tự phản đốidraulic.** Input sort-giảm-dần cho một tuyên bố
   "sort-rồi-xử-lý"; cây đảo ngược; truy vấn sắp xấu-nhất-trước.

## Tư duy

Với mỗi hình dạng, câu hỏi không phải "code tôi có gãy không?" mà là
**"nếu tôi muốn phá nó, tôi sẽ nhập gì?"** Phép đảo ngược đó tìm ra các
bug mà đọc lại không bao giờ thấy, vì bạn viết code và não bạn tự sửa
trong lúc đọc.

## Lợi-ích

Danh mục tốn vài phút. Một lần nộp sai lấy mất bài toán, sự tự tin, và
thường là cả kỳ thi. Không có kịch bản nào mà bỏ qua danh mục là phép
tính đúng.
""",
)

write_lesson(
    M, "hsgm-m12-minimal",
    "The Minimal Counterexample",
    "Shrink any counterexample to its skeleton: the minimal case is both the proof of wrongness and the specification of the fix.",
    13,
    """
# The Minimal Counterexample

Given any failing input, shrink it. Every step of shrinking either keeps
the failure (good — smaller) or breaks it (better — you have localized a
necessary component of the bug).

## The shrink loop

1. Delete an element. Still fails? Keep it deleted.
2. Halve the values (preserve order/parity relationships that matter).
3. Merge adjacent equal elements.
4. Replace large values with {1, 2, 3}-style stand-ins, preserving only
   the comparisons the solution makes.

Stop when the case is irreducible — typically n ≤ 5. The irreducible
case states the bug as a theorem: *for this input shape, this code
outputs X, correct is Y.*

## Why minimal matters

- **Diagnosis:** the minimal case usually fits on one screen; the
  offending line is visible.
- **The fix spec:** the minimal case says exactly which structure the
  code mishandles — the fix must handle that shape, and the case becomes
  the regression test.
- **Communication:** "this fails on [3, 1, 2]" is a complete bug report;
  "it fails on my 200-line random test" is not.

## When nothing small fails

If n ≤ 5 never fails but n = 40 does, the bug is either scale-dependent
(overflow, O(n²) death) or structural (needs ≥ k items to interact). Then
build the *structured* minimal case: k = the smallest interacting count,
with a repeating pattern — not random bulk.
""",
    "Phản ví dụ tối giản",
    "Thu nhỏ mọi phản ví dụ về bộ xương của nó: case tối giản vừa là bằng chứng của sai lầm vừa là đặc tả của phép vá.",
    """
# Phản ví dụ tối giản

Có sẵn một input gãy, hãy thu nhỏ nó. Mỗi bước thu nhỏ hoặc giữ được sự
gãy (tốt — nhỏ hơn) hoặc phá nó (tốt hơn — bạn đã khoanh vùng một thành
phần bắt buộc của bug).

## Vòng thu nhỏ

1. Xóa một phần tử. Vẫn gãy? Giữ nguyên trạng thái xóa.
2. Chia đôi các giá trị (giữ những quan hệ thứ tự/parity quan trọng).
3. Gộp các phần tử bằng nhau liền kề.
4. Thay giá trị lớn bằng các đại diện kiểu {1, 2, 3}, chỉ giữ lại các
   phép so sánh mà lời giải thực hiện.

Dừng khi case không thể thu nhỏ thêm — thường n ≤ 5. Case không-thu-nhỏ
phát biểu bug như một định lý: *với hình dạng input này, code này in X,
đúng phải là Y.*

## Vì sao tối giản quan trọng

- **Chẩn đoán:** case tối giản thường vừa một màn hình; dòng gây lỗi
   hiện ra.
- **Đặc tả phép vá:** case tối giản nói đúng cấu trúc mà code xử sai —
   phép vá phải xử lý được hình dạng đó, và case trở thành test hồi quy.
- **Giao tiếp:** "cái này gãy với [3, 1, 2]" là một báo cáo bug trọn vẹn;
   "nó gãy với test ngẫu nhiên 200 dòng của tôi" thì không.

## Khi không case nhỏ nào gãy

Nếu n ≤ 5 không bao giờ gãy nhưng n = 40 gãy, bug hoặc phụ thuộc thang
(tràn số, cái chết O(n²)) hoặc cấu trúc (cần ≥ k phần tử để tương tác).
Khi đó dựng case tối giản *có cấu trúc*: k = số tương tác nhỏ nhất, với
một mẫu hình lặp lại — không phải đống ngẫu nhiên.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p12-d1", "The Flattering Test",
    "Your greedy passed 300 random tests with distinct values. Which input shape have you NOT tested at all?",
    [
        "Large inputs",
        "All-ties — random distinct data never creates equal keys, so tie-break code has zero coverage",
        "Negative numbers",
        "Sorted input",
    ],
    "B",
    "Distinct-value randomness structurally excludes ties: every comparison-branch variant for equal keys is untested. Generate the tie storm on purpose.",
    vi_title="Test nịnh",
    vi_scenario="Greedy của bạn qua 300 test ngẫu nhiên với các giá trị khác nhau. Bạn CHƯA kiểm tra hình dạng input nào?",
    vi_options=[
        "Input lớn",
        "Toàn hòa — dữ liệu ngẫu nhiên khác nhau không bao giờ sinh khóa bằng nhau nên code tie-break có độ phủ bằng 0",
        "Số âm",
        "Input đã sort",
    ],
    vi_hint="Tính ngẫu nhiên khác-nhau cấu trúc loại trừ hòa: mọi biến thể nhánh so sánh cho khóa bằng nhau chưa được kiểm thử. Hãy chủ động tạo bão hòa.",
)

D2, D2VI = recognition_drill(
    "hsgm-p12-d2", "The Shrinking Discipline",
    "A 200-element random test fails. Your first shrink step should be:",
    [
        "Rerun with the same input twice to check determinism",
        "Delete one element and re-test — keep every deletion that preserves the failure",
        "Print the entire input and read it",
        "Double n to see if it still fails",
    ],
    "B",
    "Deletion is the cheapest, most localizing shrink move: every preserved deletion eliminates a suspect. Determinism checks and printing come after a few deletion rounds.",
    vi_title="Kỷ luật thu nhỏ",
    vi_scenario="Một test ngẫu nhiên 200 phần tử gãy. Bước thu nhỏ đầu tiên của bạn nên là:",
    vi_options=[
        "Chạy lại cùng input hai lần để kiểm tra tất định",
        "Xóa một phần tử và thử lại — giữ mọi phép xóa mà vẫn giữ được sự gãy",
        "In toàn bộ input và đọc",
        "Nhân đôi n xem có còn gãy không",
    ],
    vi_hint="Phép xóa là nước đi thu nhỏ rẻ nhất, khoanh vùng nhất: mỗi phép xóa được giữ loại bỏ một nghi phạm. Kiểm tra tất định và in input đến sau vài vòng xóa.",
)

D3, D3VI = recognition_drill(
    "hsgm-p12-d3", "The Structured Minimum",
    "A divide-and-conquer solution fails only when n ≥ 16, never below. What is the right minimal-case hunt?",
    [
        "Keep testing random n = 15 inputs",
        "Build the structured case: the smallest complete recursion depth (n = 16 = 2^4) with a pattern that forces the failing merge — e.g., all elements arranged to maximize cross-half interaction",
        "Give up and submit",
        "Test n = 1000 to confirm scale sensitivity",
    ],
    "B",
    "When the bug needs k interacting items, the minimal case is the smallest structured n that triggers the interaction — 2^d for depth-d recursion — with an arrangement aimed at the merge, not random bulk.",
    vi_title="Tối giản có cấu trúc",
    vi_scenario="Một lời giải chia-trị chỉ gãy khi n ≥ 16, không bao giờ dưới. Cuộc săn case-tối-đúng đúng là gì?",
    vi_options=[
        "Tiếp tục thử các input ngẫu nhiên n = 15",
        "Dựng case có cấu trúc: độ sâu đệ quy trọn vẹn nhỏ nhất (n = 16 = 2^4) với một mẫu ép phép hợp gãy — ví dụ mọi phần tử được xếp để tối đa hóa tương tác liên-phân-nửa",
        "Bỏ cuộc và nộp",
        "Thử n = 1000 để xác nhận nhạy thang",
    ],
    vi_hint="Khi bug cần k phần tử tương tác, case tối giản là n có cấu trúc nhỏ nhất kích hoạt tương tác — 2^d cho đệ quy sâu-d — với một cách xếp nhắm vào phép hợp, không phải đống ngẫu nhiên.",
)

write_practice(
    M, "hsgm-p12-drills", "Adversarial Drills",
    "Three drills: the tie blind spot, the deletion shrink loop, and structured minimal cases for scale-dependent bugs.",
    "Drill phản đốidraulic",
    "Ba drill: điểm mù hòa, vòng thu nhỏ bằng xóa, và case tối giản có cấu trúc cho bug phụ thuộc thang.",
    "hsgm-m12-minimal", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p12-d1": D1VI, "hsgm-p12-d2": D2VI, "hsgm-p12-d3": D3VI},
    solutions=[
        ("hsgm-p12-d1", letter("B"), letter("A")),
        ("hsgm-p12-d2", letter("B"), letter("A")),
        ("hsgm-p12-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: majority element (value appearing > n/2 times) — the W is the
# random-data-flattered "check if the max-frequency value reaches n/2"
# ... no: make W the plausible-but-wrong 'mode must be unique' assumption:
# W returns the SMALLEST value with max frequency; R returns whether ANY
# value has frequency > n/2 (yes/no). W's tie-smallest rule diverges on
# adversarial input where the smallest max-frequency value is NOT the
# majority (e.g., [1,1,2,2,3]: no majority → GT NO; W prints 1 as "the
# majority candidate"). Task: print YES/NO whether a strict majority
# exists (> n/2 occurrences).
def _gt_majority(a):
    from collections import Counter
    c = Counter(a)
    n = len(a)
    return 1 if any(v > n // 2 for v in c.values()) else 0


def _w_majority(a):
    # W: 'mode' heuristic — the most frequent value must be the majority;
    # answers YES if the smallest most-frequent value has count >= n/2
    # (note: >= instead of >, and picks mode not strict majority).
    from collections import Counter
    c = Counter(a)
    n = len(a)
    m = min(k for k, v in c.items() if v == max(c.values()))
    return 1 if c[m] >= n // 2 else 0


_ta = [
    [1, 1, 2],
    [1, 2, 2, 3],
    [5, 5, 5, 5],
    [1, 2, 3, 4],
    [7, 7, 7, 1, 2],
    [2, 2, 3, 3],
    [9],
    [1, 1, 1, 2, 2],
]
_ga = [_gt_majority(x) for x in _ta]
_wa = [_w_majority(x) for x in _ta]
assert any(w != g for w, g in zip(_wa, _ga)), (_wa, _ga)
# Divergence: [1,1,2,2,3]-like and [2,2,3,3] (ties, >= vs >)

import random as _r2
_r2.seed(12)
_a12 = [_r2.randrange(0, 5) for _ in range(200000)]  # heavy ties by design
_cp12 = _gt_majority(_a12)

CP_M12_IN = T("200000", " ".join(map(str, _a12)))
CP_M12_WANT = T(str(_cp12))

CP12C = challenge(
    "hsgm-cp-m12-majority",
    "Checkpoint: The Tyrant Check",
    """**Task.** n numbers. Print 1 if some value appears STRICTLY more than
n/2 times, else 0.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a_i < 10^9.

**Adversarial note:** ties and boundary counts (exactly n/2) are where
plausible solutions die. The full-scale test is tie-heavy on purpose.
""",
    [
        contest_test("clear majority", T("3", "1 1 2"), T("1"), "1 appears twice > 1.5 → 1."),
        contest_test("no majority", T("4", "1 2 3 4"), T("0"), "Max frequency 1 ≤ 2 → 0."),
    ],
    level="debugging",
    difficulty="advanced",
)
CP12C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("clear majority", T("3", "1 1 2"), T("1"),
            "1 appears twice > 1.5 → 1."),
        contest_test("no majority", T("4", "1 2 3 4"), T("0"),
            "Max frequency 1 ≤ 2 → 0."),
        contest_test("exact half", T("4", "2 2 3 3"), T("0"),
            "2 appears exactly n/2 = 2 times, NOT strictly more → 0. (The >= stumble reports 1.)"),
        contest_test("tie storm", T("5", "1 1 2 2 3"), T("0"),
            "Two values tie at 2 ≤ 2.5 → 0. (The 'mode must be majority' heuristic reports 1.)"),
        contest_test("full scale", CP_M12_IN, CP_M12_WANT,
            "n = 200000 tie-heavy by design. Ground truth computed in Python."),
    )
]

CP12VI = vi_challenge(
    "Điểm kiểm tra: phép kiểm tra bạo chúa",
    """**Bài toán.** n số. In 1 nếu có giá trị xuất hiện NGHIÊM NGẶT hơn n/2
lần, ngược lại in 0.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a_i < 10^9.

**Ghi chú phản đốidraulic:** hòa và số đếm biên (đúng n/2) là nơi các
lời giải hợp lý chết. Test đúng giới hạn cố ý nhiều hòa.
""",
    [("bạo chúa rõ", "1 xuất hiện hai lần > 1.5 → 1."),
     ("không bạo chúa", "Tần suất max 1 ≤ 2 → 0."),
     ("đúng một nửa", "2 xuất hiện đúng n/2 = 2 lần, KHÔNG nghiêm ngặt hơn → 0. (Cú vấp >= báo 1.)"),
     ("bão hòa", "Hai giá trị hòa nhau ở 2 ≤ 2.5 → 0. (Heuristic 'mode phải là đa số' báo 1.)"),
     ("đúng giới hạn", "n = 200000 nhiều hòa do chủ đích. Đáp án chuẩn tính bằng Python.")],
)

CP_M12_R = CPP_STD + cpp("""    long long n; in >> n;
    unordered_map<long long, long long> cnt;
    cnt.reserve(n * 2);
    long long x;
    for (long long i = 0; i < n; ++i) { in >> x; ++cnt[x]; }
    long long half = n / 2;
    int ans = 0;
    for (auto& [v, c] : cnt) if (c > half) { ans = 1; break; }
    out << ans << "{{NL}}";
""") + END

CP_M12_W = CPP_STD + cpp("""    long long n; in >> n;
    unordered_map<long long, long long> cnt;
    cnt.reserve(n * 2);
    long long x;
    for (long long i = 0; i < n; ++i) { in >> x; ++cnt[x]; }
    // WRONG: two stumbles in one. (1) It assumes the most frequent value
    // must be the majority candidate — but with ties the 'mode' may hold
    // fewer than n/2 while nothing else does either; and it picks the
    // smallest tied value, arbitrary. (2) It tests count >= n/2 instead of
    // > n/2 — the strictness boundary case (exactly half) flips to a
    // false YES.
    long long best = -1, bc = -1;
    for (auto& [v, c] : cnt) {
        if (c > bc || (c == bc && v < best)) { bc = c; best = v; }
    }
    out << (bc >= n / 2 ? 1 : 0) << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m12", "Checkpoint — Break It Yourself",
    "Strict-majority check: the honest O(n) count vs the plausible mode-heuristic with a >= boundary stumble. The tie-storm and exact-half tests are the adversarial shapes this module teaches.",
    25,
    """
**Checkpoint — Break It Yourself.** Strict majority (> n/2) is a one-pass
count with a strict comparison. The W embodies the two adversarial
shapes from this module: the tie assumption (mode must be the majority —
false under ties) and the boundary stumble (>= instead of >, flipping
the exactly-half case to a false YES). The tests are the shapes, made
explicit: exact-half and tie-storm. When you can *predict* which tests
will kill a plausible solution before running it, the adversarial skill
has arrived.
""",
    "Điểm kiểm tra — Tự phá nó đi",
    "Kiểm tra đa số-nghiêm-ngặt: đếm O(n) trung thực so với heuristic mode hợp lý với cú vấp >= tại biên. Test bão-hòa và đúng-một-nửa là các hình dạng phản đốidraulic mà module này dạy.",
    """
**Điểm kiểm tra — Tự phá nó đi.** Đa số nghiêm ngặt (> n/2) là một lần
đếm với phép so sánh nghiêm ngặt. W thể hiện hai hình dạng phản đốidraulic
của module này: giả định hòa (mode phải là đa số — sai dưới hòa) và cú
vấp biên (>= thay vì >, lật case đúng-một-nửa thành YES sai). Các test
chính là các hình dạng, làm tường minh: đúng-một-nửa và bão-hòa. Khi bạn
*đoán trước được* test nào sẽ giết một lời giải hợp lý trước khi chạy nó,
kỹ năng phản đốidraulic đã đến.
""",
    CP12C,
    CP12VI,
    CP_M12_R,
    CP_M12_W,
)

print("module m12 complete")
