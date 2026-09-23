#!/usr/bin/env python3
"""HSG Mastery — Module 10: hsgm-partial (Partial Scoring Laboratory).

Subtask harvesting: reading a problem's scoring bands as a design spec,
solving the easiest band first, and upgrading honestly.
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


M = "hsgm-partial"
write_module(
    M,
    "Partial Scoring Laboratory",
    "Reading scoring bands as a design spec: every subtask is a solvable problem, the bands are a ladder, and a correct 40 points beats a heroic 0.",
    "Phòng thí nghiệm điểm một phần",
    "Đọc các dải điểm như một bản đặc tả thiết kế: mọi subtask là một bài giải được, các dải là một cái thang, và 40 điểm đúng đắn hơn 0 điểm anh hùng.",
    ["hsgm-m10-bands", "hsgm-m10-harvest", "hsgm-cp-m10"],
    ["hsgm-p10-drills"],
)

write_lesson(
    M, "hsgm-m10-bands",
    "The Bands Are a Ladder",
    "Constraints per subtask name algorithms; the easiest band is a guaranteed-points problem of its own.",
    12,
    """
# The Bands Are a Ladder

A partial-scoring problem is really a stack of problems with a shared
statement. The scoring bands are not consolation prizes — they are a
**design document**:

- "n ≤ 20" → the full 2^n enumeration is *intended* for that band.
- "n ≤ 2000" → O(n²) is invited.
- "n ≤ 200000, no updates" → static prefix structures.
- "values ≤ 10^9" → coordinate compression or 64-bit.
- "all a_i equal" / "a_i ≤ 2" → degenerate-case specialization.

## Reading order

1. Read the full statement once.
2. Read the bands **top-down from the easiest**: what algorithm does each
   band's constraint permit? Name it. That is the band's intended solution.
3. Estimate implementation time per band, in order. Implement band 1
   completely before thinking about band 2.
4. The bands often *teach* the full solution: the n² band's DP frequently
   becomes the full solution's recurrence with a data structure grafted on.

## The scoring arithmetic

If band 1 is worth 20 and costs 10 minutes, and the full solution is
uncertain and costs 90, the expected-value arithmetic is not close. Bank
the certain band first; you can always upgrade later — you cannot submit
an empty file at the end.
""",
    "Các dải là một cái thang",
    "Giới hạn theo từng subtask gọi tên thuật toán; dải dễ nhất là một bài Guaranteed-Points riêng.",
    """
# Các dải là một cái thang

Một bài chấm điểm một phần thực chất là một chồng bài với cùng đề. Các
dải điểm không là phần thưởng an ủi — chúng là một **tài liệu thiết kế**:

- "n ≤ 20" → phép vét cạn 2^n là *chủ đích* cho dải đó.
- "n ≤ 2000" → O(n²) được mời.
- "n ≤ 200000, không cập nhật" → cấu trúc tiền tố tĩnh.
- "giá trị ≤ 10^9" → nén tọa độ hoặc 64-bit.
- "mọi a_i bằng nhau" / "a_i ≤ 2" → chuyên biệt hóa degenerate.

## Thứ tự đọc

1. Đọc đề một lượt.
2. Đọc các dải **từ dưới lên** (dễ nhất trước): giới hạn của mỗi dải cho
   phép thuật toán nào? Gọi tên. Đó là lời giải chủ đích của dải đó.
3. Ước lượng thời gian cài đặt mỗi dải, theo thứ tự. Cài xong dải 1 hoàn
   chỉnh trước khi nghĩ tới dải 2.
4. Các dải thường *dạy* lời giải đầy đủ: DP của dải n² thường trở thành
   truy hồi của lời giải đầy đủ sau khi ghép thêm một cấu trúc dữ liệu.

## Phép tính điểm

Nếu dải 1 trị 20 điểm và tốn 10 phút, còn lời giải đầy đủ bất định và tốn
90, phép tính kỳ vọng không gần nhau. Gửi ngân điểm chắc trước; nâng cấp
luôn luôn được — còn nộp file rỗng thì không.
""",
)

write_lesson(
    M, "hsgm-m10-harvest",
    "Harvesting Without Breaking",
    "One submission can serve every band: special-case the small inputs, run the heavy path only when needed — and never let the upgrade break the harvest.",
    13,
    """
# Harvesting Without Breaking

The professional partial-score submission is **one program with tiers**:

```text
read n, the values
if (n <= 20)      → run brute force, output, exit
if (n <= 2000)    → run O(n²), output, exit
run full solution
```

Each tier is independently testable; a bug in the full solution cannot
destroy the n ≤ 20 points if the tier exits before the heavy path runs.

## Tier discipline

- **Tier order = band order.** Ship and verify the easiest tier first.
- **Shared input parsing.** Parse everything once, correctly; most tier
  bugs are actually parsing bugs (the tier never sees the real input).
- **The upgrade rule.** When adding tier k+1, re-run tier k's tests. The
  most expensive contest mistake is a refactor that silently breaks the
  guaranteed points.
- **Fallback ladder.** If the full solution TLEs on the real test, the
  tiers above it still answered — partial scoring rewards programs that
  degrade gracefully.

## Honesty

Never special-case the *sample tests* themselves. Hard-coding sample
outputs is detectable, worth zero learning, and trains exactly the wrong
instinct. Specialize on *constraint shapes*, not on the sample files.
""",
    "Thu hoạch mà không phá",
    "Một lần nộp phục vụ mọi dải: special-case input nhỏ, chỉ chạy nhánh nặng khi cần — và đừng bao giờ để nâng cấp phá thu hoạch.",
    """
# Thu hoạch mà không phá

Lời giải điểm-một-phần chuyên nghiệp là **một chương trình nhiều tầng**:

```text
đọc n, các giá trị
if (n <= 20)      → chạy brute force, in, thoát
if (n <= 2000)    → chạy O(n²), in, thoát
chạy lời giải đầy đủ
```

Mỗi tầng kiểm thử độc lập; bug ở lời giải đầy đủ không thể phá điểm n ≤ 20
nếu tầng đó thoát trước khi nhánh nặng chạy.

## Kỷ luật tầng

- **Thứ tự tầng = thứ tự dải.** Gửi và xác minh tầng dễ nhất trước.
- **Phân tích input dùng chung.** Đọc hết một lần, đúng; đa số bug tầng
  thực ra là bug đọc input (tầng chưa bao giờ thấy input thật).
- **Luật nâng cấp.** Khi thêm tầng k+1, chạy lại test của tầng k. Lỗi thi
  đắt giá nhất là một lần refactor âm thầm phá điểm chắc chắn.
- **Thang dự phòng.** Nếu lời giải đầy đủ TLE ở test thật, các tầng phía
  trên vẫn đã trả lời — điểm một phần thưởng cho chương trình suy giảm
  một cách đàng hoàng.

## Trung thực

Đừng bao giờ special-case chính *các test mẫu*. Cứng-hóa đáp án mẫu là
điều phát hiện được, không dạy được gì, và rèn đúng bản năng sai. Chuyên
biệt hóa trên *hình dạng giới hạn*, không phải trên tệp mẫu.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p10-d1", "The Three Bands",
    "A counting problem: subtask 1 (20 pts) n ≤ 20; subtask 2 (30 pts) n ≤ 2000; subtask 3 (50 pts) n ≤ 200000. You have a proven O(n²) idea and 60 minutes left. Optimal plan?",
    [
        "Implement only O(n²) — it passes subtask 2 fully and maybe 3",
        "Ship brute force for subtask 1 first (15 min), then O(n²) for subtask 2; skip 3 — banking 50 certain points",
        "Spend all 60 minutes attempting the full O(n log n) solution",
        "Submit brute force for everything — it is simplest",
    ],
    "B",
    "Band-value arithmetic: 15 min for 20 + O(n²) for 30 banks 50 certain points; chasing the 50-pt band with an unproven O(n log n) risks the whole submission.",
    vi_title="Ba dải điểm",
    vi_scenario="Bài đếm: subtask 1 (20 đ) n ≤ 20; subtask 2 (30 đ) n ≤ 2000; subtask 3 (50 đ) n ≤ 200000. Bạn có một ý tưởng O(n²) đã chứng minh và 60 phút. Kế hoạch tối ưu?",
    vi_options=[
        "Chỉ cài O(n²) — nó qua trọn subtask 2 và có thể cả 3",
        "Nộp brute force cho subtask 1 trước (15 phút), rồi O(n²) cho subtask 2; bỏ 3 — gửi ngân 50 điểm chắc chắn",
        "Dành cả 60 phút cho lời giải đầy đủ O(n log n)",
        "Nộp brute force cho mọi thứ — nó đơn giản nhất",
    ],
    vi_hint="Phép tính giá trị dải: 15 phút cho 20 điểm + O(n²) cho 30 điểm gửi ngân 50 điểm chắc; lao theo dải 50 điểm với O(n log n) chưa chứng minh nguy cơ mất cả lần nộp.",
)

D2, D2VI = recognition_drill(
    "hsgm-p10-d2", "The Degenerate Band",
    "Subtask: 'all a_i ≤ 2'. The full solution is a complex DP. What is the band's intended shortcut?",
    [
        "The same DP with smaller numbers",
        "Count only the frequencies of 0, 1, and 2 — with values bounded by 2 the answer usually collapses to a closed form over the three counts",
        "Skip the band; it is only worth a few points",
        "Sort and binary search",
    ],
    "B",
    "Degenerate value-ranges specialize: three counters replace the DP entirely. Value-bound bands are invitations to closed forms, not smaller instances of the same algorithm.",
    vi_title="Dải thoái hóa",
    vi_scenario="Subtask: 'mọi a_i ≤ 2'. Lời giải đầy đủ là một DP phức tạp. Đường tắt chủ đích của dải này là gì?",
    vi_options=[
        "Cùng DP đó với số nhỏ hơn",
        "Chỉ đếm tần suất của 0, 1, 2 — với giá trị chặn bởi 2, đáp án thường sập thành công thức đóng trên ba bộ đếm",
        "Bỏ qua dải; chỉ đáng vài điểm",
        "Sort rồi chặt nhị phân",
    ],
    vi_hint="Dải giá-trị-thoái hóa chuyên biệt hóa: ba bộ đếm thay trọn DP. Dải chặn giá trị là lời mời cho công thức đóng, không phải phiên bản nhỏ hơn của cùng thuật toán.",
)

D3, D3VI = recognition_drill(
    "hsgm-p10-d3", "The Upgrade Accident",
    "Your tiered submission passes subtask 1 and 2. You add the full-solution tier and now subtask 1 FAILS. Most likely cause?",
    [
        "The judge changed",
        "Shared code changed underneath the lower tier — a refactor of parsing or a helper modified behavior the brute-force tier depends on; the upgrade rule (re-run lower-tier tests) was skipped",
        "Brute force cannot fail",
        "The full solution is too slow",
    ],
    "B",
    "The upgrade rule exists precisely for this: tiers share parsing/helpers, and edits ripple. Always re-run every lower tier after touching shared code.",
    vi_title="Tai nạn nâng cấp",
    vi_scenario="Lần nộp nhiều tầng của bạn qua subtask 1 và 2. Bạn thêm tầng lời-giải-đầy-đủ và giờ subtask 1 THẤT BẠI. Nguyên nhân khả dĩ nhất?",
    vi_options=[
        "Trình chấm bị thay đổi",
        "Code dùng chung đổi bên dưới tầng thấp — một lần refactor parsing hoặc một hàm phụ đã đổi hành vi mà tầng brute-force dựa vào; luật nâng cấp (chạy lại test tầng thấp) bị bỏ qua",
        "Brute force không thể thất bại",
        "Lời giải đầy đủ quá chậm",
    ],
    vi_hint="Luật nâng cấp tồn tại đúng cho việc này: các tầng dùng chung parsing/hàm phụ, và chỉnh sửa lan truyền. Luôn chạy lại mọi tầng thấp sau khi đụng code chung.",
)

write_practice(
    M, "hsgm-p10-drills", "Partial Scoring Drills",
    "Three drills: band-value arithmetic, degenerate-band specialization, and the upgrade rule.",
    "Drill điểm một phần",
    "Ba drill: phép tính giá trị dải, chuyên biệt hóa dải thoái hóa, và luật nâng cấp.",
    "hsgm-m10-harvest", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p10-d1": D1VI, "hsgm-p10-d2": D2VI, "hsgm-p10-d3": D3VI},
    solutions=[
        ("hsgm-p10-d1", letter("B"), letter("A")),
        ("hsgm-p10-d2", letter("B"), letter("A")),
        ("hsgm-p10-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task with explicit bands (declared in the prompt, honored by tests):
# "Count pairs i<j with a_i + a_j even" — band 1: all a_i even (answer =
# C(cnt,2)); band 2: n ≤ 2000 (O(n²)); full: parity counting in O(n).
# The W: full-solution formula applied everywhere BUT counts pairs with
# a_i + a_j ODD-symmetric wrongly — it counts ordered pairs (i≠j) and
# divides by 1 — i.e., it reports cnt0*cnt1 (unordered cross pairs) plus
# C(even,2)+C(odd,2) but computes C(x,2) = x*(x-1) forgetting /2 — the
# classic ordered/unordered stumble.
def _gt_pairs_parity(a):
    n = len(a)
    c = sum(1 for v in a if v % 2 == 0)
    d = n - c
    return c * (c - 1) // 2 + d * (d - 1) // 2


def _w_pairs(a):
    c = sum(1 for v in a if v % 2 == 0)
    d = len(a) - c
    return c * (c - 1) + d * (d - 1)  # BUG: ordered-pair count (missing /2)


_ta = [
    [1, 2, 3, 4],
    [2, 4, 6],
    [1, 3, 5],
    [2],
    [1, 1],
    [2, 2, 2, 2, 1],
    [0, 0],
    [5, 5, 5, 6, 6, 6, 7],
]
_ansa = [_gt_pairs_parity(x) for x in _ta]
_wa = [_w_pairs(x) for x in _ta]
assert any(w != a for w, a in zip(_wa, _ansa)), (_wa, _ansa)

_n10 = 200000
_a10 = [(i * 31337) % 1000000007 for i in range(1, _n10 + 1)]
_c10 = _gt_pairs_parity(_a10)
CP_M10_IN = T(str(_n10), " ".join(map(str, _a10)))
CP_M10_WANT = T(str(_c10))

CP10C = challenge(
    "hsgm-cp-m10-paripairs",
    "Checkpoint: The Even-Pair Harvest",
    """**Task.** Count pairs (i, j), i < j, with a_i + a_j even.

**Scoring bands (this checkpoint grades all of them):**
- Band A (test 1–2): all a_i even, n ≤ 2000.
- Band B (test 3–4): n ≤ 2000, arbitrary values.
- Band C (test 5): n ≤ 200000, a_i < 10^9.

**Hint-free budget:** the answer only needs the counts of even and odd
values — but an O(n²) sweep still passes band B honestly.
""",
    [
        contest_test("tiny", T("3", "2 4 6"), T("3"), "Three evens: C(3,2) = 3."),
        contest_test("odds only", T("3", "1 3 5"), T("3"), "Three odds: C(3,2) = 3."),
    ],
    level="combination",
    difficulty="advanced",
)
CP10C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("band A mixed", T("4", "1 2 3 4"), T(str(_ansa[0])),
            "Even pairs among {2,4}: 1; odd pairs among {1,3}: 1 → 2."),
        contest_test("band B bigger", T("7", "5 5 5 6 6 6 7"), T(str(_gt_pairs_parity([5, 5, 5, 6, 6, 6, 7]))),
            "Odds {5,5,5,7}: C(4,2)=6; evens {6,6,6}: C(3,2)=3 → 9."),
        contest_test("band C full scale", CP_M10_IN, CP_M10_WANT,
            "n = 200000: count evens c and odds d, answer C(c,2) + C(d,2) in O(n). Ground truth computed in Python."),
    )
]

CP10VI = vi_challenge(
    "Điểm kiểm tra: thu hoạch cặp chẵn",
    """**Bài toán.** Đếm cặp (i, j), i < j sao cho a_i + a_j chẵn.

**Các dải điểm (checkpoint này chấm tất cả):**
- Dải A (test 1–2): mọi a_i chẵn, n ≤ 2000.
- Dải B (test 3–4): n ≤ 2000, giá trị tùy ý.
- Dải C (test 5): n ≤ 200000, a_i < 10^9.

**Ngân sách không-gợi-ý:** đáp án chỉ cần số đếm chẵn/lẻ — nhưng phép
quét O(n²) vẫn qua dải B một cách trung thực.
""",
    [("nhỏ", "Ba số chẵn: C(3,2) = 3."),
     ("chỉ lẻ", "Ba số lẻ: C(3,2) = 3."),
     ("dải C đúng giới hạn", "n = 200000: đếm chẵn c và lẻ d, đáp án C(c,2) + C(d,2) trong O(n).")],
)

CP_M10_R = CPP_STD + cpp("""    long long n; in >> n;
    long long c = 0;              // evens
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        if ((x & 1) == 0) ++c;
    }
    long long d = n - c;          // odds
    out << c * (c - 1) / 2 + d * (d - 1) / 2 << "{{NL}}";
""") + END

CP_M10_W = CPP_STD + cpp("""    long long n; in >> n;
    long long c = 0;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        if ((x & 1) == 0) ++c;
    }
    long long d = n - c;
    // WRONG: reports the ORDERED pair count — x*(x-1) without the /2.
    // The distinction i<j (unordered) versus (i,j), (j,i) (ordered) is the
    // classic counting stumble; small tests with distinct parities pin it.
    out << c * (c - 1) + d * (d - 1) << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m10", "Checkpoint — Bank the Bands",
    "Even-sum pair counting with explicit bands: O(n) formula at full scale, honest O(n²) available for band B. The W forgets the /2 — the ordered/unordered counting stumble.",
    25,
    """
**Checkpoint — Bank the Bands.** a_i + a_j is even exactly when both are
even or both are odd: count parities, answer C(c,2) + C(d,2) — O(n), no
pairs enumerated. The W is the ordered/unordered stumble: x·(x−1) without
the halving, silently doubling the answer. Counting discipline: state
WHETHER your pairs are ordered, once, before the formula.
""",
    "Điểm kiểm tra — Gửi ngân các dải",
    "Đếm cặp tổng-chẵn với các dải tường minh: công thức O(n) ở đúng giới hạn, O(n²) trung thực cho dải B. W quên /2 — cú vấp đếm có-thứ-tự/không-thứ-tự.",
    """
**Điểm kiểm tra — Gửi ngân các dải.** a_i + a_j chẵn đúng khi cả hai chẵn
hoặc cả hai lẻ: đếm parity, đáp án C(c,2) + C(d,2) — O(n), không liệt kê
cặp nào. W là cú vấp có-thứ-tự/không-thứ-tự: x·(x−1) thiếu phép chia 2,
âm thầm gấp đôi đáp án. Kỷ luật đếm: phát biểu CẶP của bạn CÓ thứ tự
không, một lần, trước công thức.
""",
    CP10C,
    CP10VI,
    CP_M10_R,
    CP_M10_W,
)

print("module m10 complete")
