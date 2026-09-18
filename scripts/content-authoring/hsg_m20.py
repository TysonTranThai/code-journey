#!/usr/bin/env python3
"""HSG — Module 20: hsg-contests (chuỗi kỳ thi).

Three graded mock contests (A+B pairs, timed-style) plus a mixed practice
set. Every problem is original and two-sided verified. Conventions: T()
for test I/O, cpp() for bodies.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
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

M = "hsg-contests"
write_module(
    M,
    "Beginner Contest Series",
    "Three mock contests mixing every beginner tool — time management and problem selection are graded skills too.",
    "Chuỗi kỳ thi người mới",
    "Ba kỳ thi giả lập trộn mọi công cụ đã học — quản lý thời gian và chọn bài cũng là kỹ năng bị chấm.",
    ["hsg-m20-strategy", "hsg-m20-manage", "hsg-cp-m20a", "hsg-cp-m20b", "hsg-cp-m20final"],
    ["hsg-p20-mixed"],
)

write_lesson(
    M,
    "hsg-m20-strategy",
    "Contest Strategy",
    "Scan everything, solve in profit order, bank partial credit, never gamble on an unverified guess.",
    15,
    """## The first 10 minutes

Read EVERY problem before solving any. Rank them by (expected
solution time, confidence). Start with the highest
confidence-per-minute — usually the easiest A-problem, but not
always: sometimes your strongest topic appears in problem C.

## During the contest

- One problem at a time; set a mental timer. Stuck 20+ minutes with
  no new idea? Move on. Coming back fresh often cracks it in 5.
- Submit brute force when the subtask allows it. Points on the board
  change your strategy for the better.
- Never submit untested code — 30 seconds of local checking on the
  samples beats a 20-minute penalty queue (in judges without penalty,
  it still saves your confidence).

## The last 20 minutes

Protect what you have. A risky rewrite that breaks a passing problem
is a net loss. Fix compile warnings, re-read output formats, check
the largest inputs you can construct by hand.

## After

Every contest ends with a post-mortem: which problems did others
solve that you missed? Which of your misses was a knowledge gap vs a
time-management gap vs an implementation slip? The three have
different fixes: study, drills, and checklists respectively.
""",
    "Chiến lược thi",
    "Quét tất cả, giải theo thứ tự lợi nhuận, lấy điểm phần, không bao giờ đánh cược vào phỏng đoán chưa kiểm chứng.",
    """## 10 phút đầu

Đọc MỌI bài trước khi giải bài nào. Xếp hạng theo (thời gian giải dự
kiến, độ tự tin). Bắt đầu với điểm-tự-tin-trên-phút cao nhất — thường
là bài A dễ nhất, nhưng không hẳn: đôi khi chủ đề mạnh nhất của bạn
nằm ở bài C.

## Trong kỳ thi

- Một bài một lúc; đặt đồng hồ tinh thần. Kẹt 20+ phút không có ý
  tưởng mới? Chuyển bài. Quay lại với đầu óc mới thường gỡ trong 5
  phút.
- Nộp vét cạn khi subtask cho phép. Điểm trên bảng thay đổi chiến
  lược của bạn theo hướng tốt.
- Không bao giờ nộp code chưa test — 30 giây kiểm tra sample cục bộ
  đáng hơn 20 phút penalty (với máy chấm không penalty, nó vẫn giữ
  sự bình tĩnh của bạn).

## 20 phút cuối

Bảo vệ những gì đang có. Một bản viết lại mạo hiểm làm hỏng bài đang
giữ điểm là lỗ ròng. Rà warning biên dịch, đọc lại định dạng output,
kiểm tra input lớn nhất dựng được bằng tay.

## Sau thi

Mọi kỳ thi kết thúc bằng hậu kiểm: bài nào người khác giải được mà
bạn bỏ lỡ? Lỗi của bạn là lỗ hổng kiến thức, lỗi quản lý thời gian,
hay lỗi triển khai? Ba loại có ba cách khắc phục khác nhau: học,
drill, và checklist.
""",
    15,
)

write_lesson(
    M,
    "hsg-m20-manage",
    "Time Management Under a Clock",
    "Budget minutes per problem by expected value, not by order on the paper.",
    14,
    """## Budgeting

A 150-minute exam with 4 problems is NOT 37 minutes each. Estimate
each problem's difficulty first, then allocate: 20-40-50-40 beats
equal splits when problems have different weight. Re-check the plan
at fixed checkpoints (minute 60, minute 100): are you on plan? If
not, re-plan — plans are tools, not contracts.

## Partial-credit arithmetic

A 40% subtask banked is worth more than a 100% solution that never
lands. When stuck at 80% confidence on the full solution with 30
minutes left, ask: can I GUARANTEE the subtask in 10 minutes instead?
Then take the guarantee.

## The two-pass sweep

Pass 1: read all, solve all "immediate" problems (I/O, simulation,
one-idea problems). Pass 2: return to heavy problems with the score
already safe. Beginners lose most points by doing the reverse —
grinding problem B while D's 15-minute solution sits untouched.

## Stamina is a skill

Contest performance degrades with fatigue. Practice full-length
mocks at your real exam time of day, eat beforehand, skip no sleep
the night before. This sounds trivial; it decides ties.
""",
    "Quản lý thời gian dưới áp lực",
    "Phân bổ số phút cho từng bài theo giá trị kỳ vọng, không theo thứ tự trên giấy.",
    """## Phân bổ

Kỳ thi 150 phút 4 bài KHÔNG phải 37 phút mỗi bài. Ước lượng độ khó
trước, rồi phân bổ: 20-40-50-40 thắng chia đều khi các bài nặng nhẹ
khác nhau. Kiểm tra lại kế hoạch tại các mốc cố định (phút 60, phút
100): có đúng kế hoạch không? Không thì phân bổ lại — kế hoạch là
công cụ, không phải hợp đồng.

## Phép tính điểm phần

40% subtask lấy được đáng giá hơn lời giải 100% không bao giờ kịp.
Khi kẹt ở 80% tự tin với lời giải trọn vẹn còn 30 phút, hãy hỏi: có
thể ĐẢM BẢO subtask trong 10 phút không? Nếu được, lấy sự đảm bảo.

## Quét hai lượt

Lượt 1: đọc hết, giải hết các bài "nhìn là làm được" (I/O, mô phỏng,
một ý tưởng). Lượt 2: quay lại các bài nặng với số điểm đã an toàn.
Người mới mất điểm nhiều nhất làm ngược lại — mải miết bài B trong
khi lời giải 15 phút của bài D nằm đó không ai đụng.

## Sức bền là kỹ năng

Hiệu suất thi giảm theo mệt mỏi. Tập mock đủ độ dài đúng khung giờ
thi thật, ăn trước khi thi, đêm trước ngủ đủ. Nghe tầm thường; nó
quyết định các trận đấu cân bằng.
""",
    14,
)

# ============ Mixed practice set (A1-A5) ============

A1 = challenge(
    "hsg-p20-beads",
    "Bead Necklace",
    T(
        "**Description:** A necklace of n beads (n >= 2) in a circle; bead i has color c[i]",
        "(1..100). Count the adjacent pairs (including bead n next to bead 1) with",
        "DIFFERENT colors.",
        "",
        "**Input:** Line 1: n (2 <= n <= 100000). Line 2: n integers c[i].",
        "**Output:** One integer — the number of color-changing adjacencies.",
        "",
        "**Example:** `4` / `1 2 2 1` -> `2` (1-2 and 1-2 across the closure).",
    ),
    [
        contest_test("sample", T("4", "1 2 2 1"), T("2"),
                     "Pairs: (1,2) diff, (2,2) same, (2,1) diff, closure (1,1) same."),
        contest_test("all same", T("3", "5 5 5"), T("0"), "No changes anywhere."),
        contest_test("alternating", T("4", "1 2 1 2"), T("4"), "Every adjacency changes — including the closure."),
        contest_test("two beads", T("2", "3 3"), T("0"), "3-3 and closure 3-3."),
        contest_test("one boundary", T("5", "1 1 2 2 2"), T("2"), "Changes at 2-3 and the closure 2-1."),
    ],
    level="guided",
    difficulty="intermediate",
)

A2 = challenge(
    "hsg-p20-prices",
    "Price Spikes",
    T(
        "**Description:** Given n daily prices, count the days that are strict local maxima:",
        "higher than BOTH neighbors (day 1 and day n have only one neighbor).",
        "",
        "**Input:** Line 1: n (1 <= n <= 200000). Line 2: n integers (|p[i]| <= 10^9).",
        "**Output:** One integer — the number of strict local maxima.",
        "",
        "**Example:** `5` / `1 3 2 3 1` -> `2`.",
    ),
    [
        contest_test("sample", T("5", "1 3 2 3 1"), T("2"), "Both 3s."),
        contest_test("single day", T("1", "7"), T("1"), "One day with no neighbors — counts."),
        contest_test("two days", T("2", "4 9"), T("1"),
                     "9 has one neighbor and is higher — counts; 4 does not."),
        contest_test("plateau", T("5", "1 5 5 5 1"), T("0"),
                     "Equal neighbors are not STRICTLY higher."),
        contest_test("valley only", T("3", "5 1 5"), T("0"), "A minimum is not a maximum."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p20-classify",
    "Number Classes",
    T(
        "**Description:** For each query value x, classify: `perfect-square` if x is a",
        "perfect square (0, 1, 4, 9, ...), `even` if even, `odd` otherwise.",
        "Perfect-square wins over parity.",
        "",
        "**Input:** Line 1: q (1 <= q <= 100000). Next q lines: x (0 <= x <= 10^9).",
        "**Output:** q lines: the classification.",
        "",
        "**Example:** `3` / `16` / `6` / `7` -> `perfect-square` / `even` / `odd`.",
    ),
    [
        contest_test("sample", T("3", "16", "6", "7"),
                     T("perfect-square", "even", "odd"), "Square beats parity."),
        contest_test("zero", T("1", "0"), T("perfect-square"), "0 = 0^2."),
        contest_test("one", T("1", "1"), T("perfect-square"), "1 = 1^2."),
        contest_test("big square", T("1", "999999999"), T("odd"),
                     "31622^2 = 999950884; 31623^2 = 1000013129 > 1e9 — x is neither, classify by parity."),
        contest_test("perfect big", T("1", "999950884"), T("perfect-square"), "31622^2 exactly."),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p20-queue",
    "Cafeteria Queue",
    T(
        "**Description:** n students queue; student i needs t[i] seconds to be served. The",
        "counter serves them in order. Print, for each student, the second they finish",
        "(student 1 finishes at t[1]; student i finishes when student i-1 did, plus t[i]).",
        "",
        "**Input:** Line 1: n (1 <= n <= 200000). Line 2: n integers (1 <= t[i] <= 1000).",
        "**Output:** One line: n finish times, space-separated (fits in 64 bits).",
        "",
        "**Example:** `3` / `2 5 1` -> `2 7 8`.",
    ),
    [
        contest_test("sample", T("3", "2 5 1"), T("2 7 8"), "Running prefix sums."),
        contest_test("single", T("1", "4"), T("4"), "One student."),
        contest_test("all same", T("4", "3 3 3 3"), T("3 6 9 12"), "Arithmetic progression."),
        contest_test("big", T("3", "1000 1000 1000"), T("1000 2000 3000"), "64-bit not strictly needed but keep it."),
        contest_test("max n sanity", T("5", "1 1 1 1 1"), T("1 2 3 4 5"), "Count up."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p20-presents",
    "Present Bags",
    T(
        "**Description:** n bags; bag i contains a[i] candies. Split the bags into two",
        "groups so that the difference of total candies between groups is minimized.",
        "Print that minimum difference. n is small — full search is intended.",
        "",
        "**Input:** Line 1: n (1 <= n <= 20). Line 2: n integers (1 <= a[i] <= 10^6).",
        "**Output:** One integer — the minimal |sum1 - sum2|.",
        "",
        "**Example:** `3` / `1 2 4` -> `1` (1+2=3 vs 4).",
    ),
    [
        contest_test("sample", T("3", "1 2 4"), T("1"), "3 vs 4."),
        contest_test("even split", T("2", "5 5"), T("0"), "Perfect balance."),
        contest_test("one bag", T("1", "9"), T("9"), "One group gets everything."),
        contest_test("big total", T("3", "1000000 999999 3"), T("2"),
                     "1000000 vs 999999+3: difference 2."),
        contest_test("all equal", T("4", "7 7 7 7"), T("0"), "2 and 2."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p20-beads": vi_challenge(
        "Vòng xuyến",
        T(
            "**Đề bài:** Vòng xuyến n hạt (n >= 2) xếp tròn; hạt i có màu c[i] (1..100). Đếm",
            "các cặp kề nhau (gồm hạt n cạnh hạt 1) có màu KHÁC nhau.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (2 <= n <= 100000). Dòng 2: n số nguyên c[i].",
            "**Dữ liệu ra:** Một số nguyên — số chỗ kề đổi màu.",
            "",
            "**Ví dụ:** `4` / `1 2 2 1` -> `2` (1-2 và 1-2 qua khép vòng).",
        ),
        [
            ("sample", "Các cặp: (1,2) khác, (2,2) same, (2,1) khác, khép vòng (1,1) same."),
            ("all same", "Không đổi chỗ nào."),
            ("alternating", "Mọi chỗ kề đều đổi — kể cả khép vòng."),
            ("two beads", "3-3 và khép vòng 3-3."),
            ("one boundary", "Đổi tại 2-3 và khép vòng 2-1."),
        ],
    ),
    "hsg-p20-prices": vi_challenge(
        "Đỉnh giá",
        T(
            "**Đề bài:** Cho n giá theo ngày, đếm các ngày là cục bộ-tối-đa NGHIÊM NGẶT: cao",
            "hơn CẢ hai hàng xóm (ngày 1 và ngày n chỉ có một hàng xóm).",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 200000). Dòng 2: n số nguyên (|p[i]| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — số đỉnh cục bộ nghiêm ngặt.",
            "",
            "**Ví dụ:** `5` / `1 3 2 3 1` -> `2`.",
        ),
        [
            ("sample", "Cả hai số 3."),
            ("single day", "Một ngày không hàng xóm — được tính."),
            ("two days", "9 có một hàng xóm và cao hơn — được tính; 4 thì không."),
            ("plateau", "Bằng nhau không phải CAO HƠN nghiêm ngặt."),
            ("valley only", "Đáy không phải đỉnh."),
        ],
    ),
    "hsg-p20-classify": vi_challenge(
        "Phân loại số",
        T(
            "**Đề bài:** Với mỗi truy vấn x, phân loại: `perfect-square` nếu x là chính phương",
            "(0, 1, 4, 9, ...), `even` nếu chẵn, `odd` ngược lại. Chính phương ưu tiên hơn",
            "tính chẵn lẻ.",
            "",
            "**Dữ liệu vào:** Dòng 1: q (1 <= q <= 100000). q dòng tiếp: x (0 <= x <= 10^9).",
            "**Dữ liệu ra:** q dòng: phân loại.",
            "",
            "**Ví dụ:** `3` / `16` / `6` / `7` -> `perfect-square` / `even` / `odd`.",
        ),
        [
            ("sample", "Chính phương thắng tính chẵn lẻ."),
            ("zero", "0 = 0^2."),
            ("one", "1 = 1^2."),
            ("big square", "31622^2 = 999950884; 31623^2 vượt 1e9 — x không hai loại, xét chẵn lẻ."),
            ("perfect big", "31622^2 chính xác."),
        ],
    ),
    "hsg-p20-queue": vi_challenge(
        "Hàng căng-tin",
        T(
            "**Đề bài:** n sinh viên xếp hàng; sinh viên i cần t[i] giây để được phục vụ. Quầy",
            "phục vụ theo thứ tự. In, với mỗi sinh viên, giây họ xong (sinh viên 1 xong ở",
            "t[1]; sinh viên i xong khi sinh viên i-1 xong, cộng thêm t[i]).",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 200000). Dòng 2: n số nguyên (1 <= t[i] <= 1000).",
            "**Dữ liệu ra:** Một dòng: n thời điểm kết thúc, cách nhau dấu cách (vừa 64 bit).",
            "",
            "**Ví dụ:** `3` / `2 5 1` -> `2 7 8`.",
        ),
        [
            ("sample", "Tổng tiền tố chạy."),
            ("single", "Một sinh viên."),
            ("all same", "Cấp số cộng."),
            ("big", "64-bit không bắt buộc nhưng cứ giữ."),
            ("max n sanity", "Đếm lên."),
        ],
    ),
    "hsg-p20-presents": vi_challenge(
        "Túi quà",
        T(
            "**Đề bài:** n túi; túi i chứa a[i] viên kẹo. Chia các túi thành hai nhóm sao cho",
            "chênh lệch tổng kẹo giữa hai nhóm nhỏ nhất. In chênh lệch nhỏ nhất đó. n nhỏ —",
            "vét cạn toàn bộ là chủ ý.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 20). Dòng 2: n số nguyên (1 <= a[i] <= 10^6).",
            "**Dữ liệu ra:** Một số nguyên — |sum1 - sum2| nhỏ nhất.",
            "",
            "**Ví dụ:** `3` / `1 2 4` -> `1` (1+2=3 với 4).",
        ),
        [
            ("sample", "3 với 4."),
            ("even split", "Cân hoàn hảo."),
            ("one bag", "Một nhóm nhận tất cả."),
            ("big total", "1000000 với 999999+3: chênh 2."),
            ("all equal", "2 và 2."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p20-mixed",
    "Mixed Mock Problems",
    "A sampler of every beginner technique: simulation, local extrema, classification, prefix sums, exhaustive search.",
    "Bài giả lập hỗn hợp",
    "Mẫu của mọi kỹ thuật: mô phỏng, cực trị cục bộ, phân loại, tổng tiền tố, tìm kiếm vét cạn.",
    "hsg-m20-manage",
    60,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p20-beads",
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> c(n);
    for (auto& x : c) in >> x;
    int cnt = 0;
    for (int i = 0; i < n; ++i)
        if (c[i] != c[(i + 1) % n]) ++cnt;   // closure handled by modulo
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> c(n);
    for (auto& x : c) in >> x;
    int cnt = 0;
    for (int i = 0; i + 1 < n; ++i)          // near-miss: forgets the closure pair
        if (c[i] != c[i + 1]) ++cnt;
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p20-prices",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> p(n);
    for (auto& x : p) in >> x;
    int cnt = 0;
    for (int i = 0; i < n; ++i) {
        bool left = (i == 0) || p[i] > p[i-1];
        bool right = (i == n-1) || p[i] > p[i+1];
        if (left && right) ++cnt;
    }
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> p(n);
    for (auto& x : p) in >> x;
    int cnt = 0;
    for (int i = 1; i + 1 < n; ++i)          // near-miss: skips both endpoints
        if (p[i] > p[i-1] && p[i] > p[i+1]) ++cnt;
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p20-classify",
            CPP_STD + cpp("""    int q; in >> q;
    string res;
    for (int i = 0; i < q; ++i) {
        long long x; in >> x;
        long long r = (long long)sqrtl((long double)x);
        while (r * r > x) --r;
        while ((r + 1) * (r + 1) <= x) ++r;   // fix floating-point drift
        if (i) res += "{{NL}}";
        if (r * r == x) res += "perfect-square";
        else if (x % 2 == 0) res += "even";
        else res += "odd";
    }
    out << res << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int q; in >> q;
    string res;
    for (int i = 0; i < q; ++i) {
        long long x; in >> x;
        // near-miss: parity check FIRST — even perfect squares (4, 16, 36...)
        // get misclassified
        if (i) res += "{{NL}}";
        if (x % 2 == 0) res += "even";
        else {
            long long r = (long long)sqrtl((long double)x);
            while (r * r > x) --r;
            while ((r + 1) * (r + 1) <= x) ++r;
            res += (r * r == x) ? "perfect-square" : "odd";
        }
    }
    out << res << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p20-queue",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> t(n);
    for (auto& x : t) in >> x;
    string res;
    long long run = 0;
    for (int i = 0; i < n; ++i) {
        run += t[i];
        res += to_string(run);
        if (i + 1 < n) res += " ";
    }
    out << res << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> t(n);
    for (auto& x : t) in >> x;
    string res;
    long long run = 0;
    for (int i = 0; i < n; ++i) {
        // near-miss: prints the WAIT time (before adding) instead of finish time
        res += to_string(run);
        if (i + 1 < n) res += " ";
        run += t[i];
    }
    out << res << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p20-presents",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long best = -1;
    for (int mask = 0; mask < (1 << n); ++mask) {
        long long s1 = 0, s2 = 0;
        for (int i = 0; i < n; ++i)
            ((mask >> i & 1) ? s1 : s2) += a[i];
        long long d = s1 > s2 ? s1 - s2 : s2 - s1;
        if (best < 0 || d < best) best = d;
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // near-miss: greedy — sort desc, add each to the smaller side;
    // not optimal (e.g. 5 4 3 3: greedy gives 8/7 -> 1, but 5+3 / 4+3 -> 1;
    // use 6 5 5 4: greedy 10/10 -> 0... the failing case is 8 7 6 5 5 5:
    // greedy 17/19 -> 2, optimal 18/18 -> 0)
    long long s1 = 0, s2 = 0;
    sort(a.begin(), a.end(), greater<long long>());
    for (int i = 0; i < n; ++i) {
        if (s1 <= s2) s1 += a[i]; else s2 += a[i];
    }
    out << (s1 > s2 ? s1 - s2 : s2 - s1) << "{{NL}}";
""") + END,
        ),
    ],
)

# ============ Contest checkpoints ============

C1A = challenge(
    "hsg-cp-m20a-mirage",
    "Contest 1 — A: Desert Mirage",
    T(
        "**Description:** Standing in the desert, you see a row of n heat shimmer waves;",
        "wave i has height h[i]. A wave is VISIBLE from the left if it is strictly taller",
        "than every wave before it. Count the visible waves.",
        "",
        "**Input:** Line 1: n (1 <= n <= 200000). Line 2: n integers (|h[i]| <= 10^9).",
        "**Output:** One integer — the count.",
        "",
        "**Example:** `5` / `3 1 4 1 5` -> `3` (3, 4, 5).",
    ),
    [
        contest_test("sample", T("5", "3 1 4 1 5"), T("3"), "Prefix maxima walk."),
        contest_test("single", T("1", "0"), T("1"), "The first wave is always visible."),
        contest_test("descending", T("4", "9 5 3 1"), T("1"), "Only the first."),
        contest_test("equal runs", T("3", "7 7 7"), T("1"), "Strictly taller required."),
        contest_test("negatives", T("3", "-5 -3 -1"), T("3"), "All rising negatives — each beats the prefix max."),
    ],
    level="guided",
    difficulty="intermediate",
)

VI_C1A = vi_challenge(
    "Kỳ thi 1 — A: Ảo cảnh sa mạc",
    T(
        "**Đề bài:** Giữa sa mạc, bạn thấy n sóng lóa nhiệt; sóng i cao h[i]. Một sóng",
        "NHÌN THẤY từ bên trái nếu cao nghiêm ngặt hơn mọi sóng trước nó. Đếm sóng nhìn",
        "thấy.",
        "",
        "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 200000). Dòng 2: n số nguyên (|h[i]| <= 10^9).",
        "**Dữ liệu ra:** Một số nguyên — số sóng.",
        "",
        "**Ví dụ:** `5` / `3 1 4 1 5` -> `3` (3, 4, 5).",
    ),
    [
        ("sample", "Duyệt max tiền tố."),
        ("single", "Sóng đầu tiên luôn nhìn thấy."),
        ("descending", "Chỉ sóng đầu."),
        ("equal runs", "Bắt buộc cao hơn nghiêm ngặt."),
        ("negatives", "Toàn dãy tăng số âm — sóng nào cũng thắng max tiền tố."),
    ],
)

C1B = challenge(
    "hsg-cp-m20a-oasis",
    "Contest 1 — B: Oasis Shares",
    T(
        "**Description:** n travelers share m liters of water. The i-th traveler (in order)",
        "takes water greedily: as many full liters as remain, but at most c[i]. Print how",
        "many liters each traveler actually takes; leftovers at the end go unclaimed.",
        "",
        "**Input:** Line 1: n m (1 <= n <= 200000, 0 <= m <= 10^9). Line 2: n integers",
        "(1 <= c[i] <= 10^9).",
        "**Output:** One line: n numbers, space-separated — liters taken by each traveler.",
        "",
        "**Example:** `3 10` / `4 5 2` -> `4 5 1`.",
    ),
    [
        contest_test("sample", T("3 10", "4 5 2"), T("4 5 1"), "4+5=9; the third gets the last liter."),
        contest_test("empty source", T("2 0", "3 4"), T("0 0"), "Nobody takes anything."),
        contest_test("exact", T("2 9", "4 5"), T("4 5"), "Everyone is satisfied exactly."),
        contest_test("shortage", T("3 2", "1 1 1"), T("1 1 0"), "The queue outruns the water."),
        contest_test("huge caps", T("2 1000000000", "1000000000 1"), T("1000000000 0"), "64-bit discipline."),
    ],
    level="guided",
    difficulty="intermediate",
)

VI_C1B = vi_challenge(
    "Kỳ thi 1 — B: Chia nước ốc đảo",
    T(
        "**Đề bài:** n người chia m lít nước. Người thứ i (theo thứ tự) lấy tham lam: càng",
        "nhiều lít đầy càng tốt nhưng tối đa c[i]. In số lít mỗi người thực lấy; phần còn",
        "lại cuối cùng không ai nhận.",
        "",
        "**Dữ liệu vào:** Dòng 1: n m (1 <= n <= 200000, 0 <= m <= 10^9). Dòng 2: n số nguyên",
        "(1 <= c[i] <= 10^9).",
        "**Dữ liệu ra:** Một dòng: n số cách nhau dấu cách — số lít mỗi người lấy.",
        "",
        "**Ví dụ:** `3 10` / `4 5 2` -> `4 5 1`.",
    ),
    [
        ("sample", "4+5=9; người thứ ba nhận lít cuối."),
        ("empty source", "Không ai lấy gì."),
        ("exact", "Ai cũng vừa đủ."),
        ("shortage", "Hàng đợi dài hơn nguồn nước."),
        ("huge caps", "Kỷ luật 64-bit."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m20a",
    "Contest 1 — Warm-up (A+B)",
    "Two-entry mock contest: prefix maxima and greedy simulation. Target: both solved within 30 minutes.",
    30,
    """**Contest 1 — khởi động.** Hai bài A/B: duyệt max tiền tố và mô phỏng
tham lam. Mục tiêu: giải cả hai trong 30 phút. Near-miss bị chấm ở bài
A: dùng >= thay vì > (đếm thừa các sóng bằng nhau); ở bài B: in dung
tích thay vì phần thực lấy (người cuối phải in số lít còn lại, không
phải c[i]).

**Contest 1 — warm-up.** A/B pair: prefix maxima and greedy
simulation. Target both in 30 minutes. Graded near-misses: A counts
equal waves as visible; B prints capacity instead of the taken amount.
""",
    "Kỳ thi 1 — Khởi động (A+B)",
    "Kỳ thi giả hai bài: max tiền tố và mô phỏng tham lam. Mục tiêu: giải cả hai trong 30 phút.",
    """**Kỳ thi 1 — khởi động.** Hai bài A/B: duyệt max tiền tố và mô phỏng
tham lam. Mục tiêu: giải cả hai trong 30 phút. Near-miss bị chấm ở bài
A: dùng >= thay vì > (đếm thừa các sóng bằng nhau); ở bài B: in dung
tích thay vì phần thực lấy (người cuối phải in số lít còn lại, không
phải c[i]).
""",
    [C1A, C1B],
    [VI_C1A, VI_C1B],
    solutions=[
        (
            "hsg-cp-m20a-mirage",
            CPP_STD + cpp("""    int n; in >> n;
    long long best = 0;
    bool first = true;
    int cnt = 0;
    for (int i = 0; i < n; ++i) {
        long long h; in >> h;
        if (first || h > best) { ++cnt; best = h; first = false; }
    }
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    long long best = 0;
    bool first = true;
    int cnt = 0;
    for (int i = 0; i < n; ++i) {
        long long h; in >> h;
        // near-miss: >= counts equal waves as newly visible
        if (first || h >= best) { ++cnt; best = h; first = false; }
    }
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsg-cp-m20a-oasis",
            CPP_STD + cpp("""    long long n, m; in >> n >> m;
    string res;
    for (int i = 0; i < n; ++i) {
        long long c; in >> c;
        long long take = c < m ? c : m;
        m -= take;
        res += to_string(take);
        if (i + 1 < n) res += " ";
    }
    out << res << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long n, m; in >> n >> m;
    string res;
    for (int i = 0; i < n; ++i) {
        long long c; in >> c;
        long long take = c < m ? c : m;
        // near-miss: forgets to consume the water — everyone takes full capacity
        res += to_string(c);
        if (i + 1 < n) res += " ";
    }
    out << res << "{{NL}}";
""") + END,
        ),
    ],
)

C2A = challenge(
    "hsg-cp-m20b-lanterns",
    "Contest 2 — A: Lantern Rows",
    T(
        "**Description:** A street has n lamp posts in a row; some are lit ('L'), some",
        "dark ('D'). Every dark segment (maximal run of 'D') must receive ONE lantern",
        "anywhere inside it. Count the lanterns needed.",
        "",
        "**Input:** Line 1: n (1 <= n <= 200000). Line 2: the string of L/D characters.",
        "**Output:** One integer — the number of lanterns.",
        "",
        "**Example:** `7` / `LLDDDLD` -> `2`.",
    ),
    [
        contest_test("sample", T("7", "LLDDDLD"), T("2"), "Two maximal D runs."),
        contest_test("all lit", T("3", "LLL"), T("0"), "Nothing to light."),
        contest_test("all dark", T("4", "DDDD"), T("1"), "One segment."),
        contest_test("alternating", T("5", "DDDDD" if False else "LDLDL"), T("2"),
                     "Two single-cell segments."),
        contest_test("single dark tail", T("3", "LLD"), T("1"), "The tail run."),
    ],
    level="guided",
    difficulty="intermediate",
)

VI_C2A = vi_challenge(
    "Kỳ thi 2 — A: Hàng đèn lồng",
    T(
        "**Đề bài:** Một phố có n cột đèn xếp hàng; có cột sáng ('L'), có cột tối ('D').",
        "Mỗi đoạn tối (dãy 'D' dài nhất liên tiếp) cần MỘT đèn lồng đặt ở bất kỳ đâu trong",
        "đoạn. Đếm số đèn lồng cần.",
        "",
        "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 200000). Dòng 2: xâu ký tự L/D.",
        "**Dữ liệu ra:** Một số nguyên — số đèn lồng.",
        "",
        "**Ví dụ:** `7` / `LLDDDLD` -> `2`.",
    ),
    [
        ("sample", "Hai đoạn D dài nhất."),
        ("all lit", "Không cần thắp gì."),
        ("all dark", "Một đoạn."),
        ("alternating", "Hai đoạn một ô."),
        ("single dark tail", "Đoạn cuối."),
    ],
)

C2B = challenge(
    "hsg-cp-m20b-balloon",
    "Contest 2 — B: Balloon Heights",
    T(
        "**Description:** n balloons float at distinct heights. You may swap any two",
        "balloons' positions. Find the minimum number of swaps so the heights end in",
        "strictly increasing order. Heights are a permutation of distinct values — map",
        "them to ranks 1..n first.",
        "",
        "**Input:** Line 1: n (1 <= n <= 100000). Line 2: n distinct integers (|h[i]| <= 10^9).",
        "**Output:** One integer — the minimum number of swaps.",
        "",
        "**Example:** `4` / `4 3 2 1` -> `2` (swap 4<->1, swap 3<->2).",
    ),
    [
        contest_test("sample", T("4", "4 3 2 1"), T("2"), "Two disjoint transpositions."),
        contest_test("sorted", T("3", "1 2 3"), T("0"), "Already ordered."),
        contest_test("one swap", T("3", "2 1 3"), T("1"), "Single transposition."),
        contest_test("cycle of 3", T("3", "2 3 1"), T("2"), "A 3-cycle needs size-1 = 2 swaps."),
        contest_test("negatives", T("3", "-5 -9 -1"), T("1"),
                     "Ranks: -9(1) -5(2) -1(3) — current order is 2 1 3, one swap."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_C2B = vi_challenge(
    "Kỳ thi 2 — B: Độ cao bóng bay",
    T(
        "**Đề bài:** n bóng bay bay ở độ cao đôi một khác nhau. Bạn được đổi chỗ hai bóng",
        "bất kỳ. Tìm số lần đổi chỗ ít nhất để độ cao theo thứ tự tăng nghiêm ngặt. Độ cao",
        "là một hoán vị các giá trị phân biệt — ánh xạ chúng thành hạng 1..n trước.",
        "",
        "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100000). Dòng 2: n số nguyên phân biệt (|h[i]| <= 10^9).",
        "**Dữ liệu ra:** Một số nguyên — số lần đổi chỗ ít nhất.",
        "",
        "**Ví dụ:** `4` / `4 3 2 1` -> `2` (đổi 4<->1, đổi 3<->2).",
    ),
    [
        ("sample", "Hai hoán vị rời nhau."),
        ("sorted", "Đã đúng thứ tự."),
        ("one swap", "Một hoán vị đơn."),
        ("cycle of 3", "Chu trình 3 cần kích-thước-1 = 2 lần đổi."),
        ("negatives", "Hạng: -9(1) -5(2) -1(3) — thứ tự hiện tại 2 1 3, một lần đổi."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m20b",
    "Contest 2 — Technique (A+B)",
    "Two-entry mock contest: run counting and cycle decomposition. Target: both within 45 minutes.",
    45,
    """**Contest 2 — kỹ thuật.** A đếm đoạn 'D' dài nhất (một dòng quét); B
phân rã chu trình hoán vị sau khi ánh xạ hạng. Near-miss bị chấm ở bài
A: đếm từng ô 'D' thay vì từng đoạn (DDDD phải là 1 không phải 4); ở
bài B: đếm nửa số cặp sai thứ tự thay vì chu trình (đúng cho hoán vị
đối xứng, sai cho chu trình dài).

**Contest 2 — technique.** A counts maximal D-runs (one scan); B does
permutation cycle decomposition after rank mapping. Graded near-misses:
A counts D cells instead of runs; B counts inversions/2 instead of
cycle cost (right for reversed pairs, wrong for long cycles).
""",
    "Kỳ thi 2 — Kỹ thuật (A+B)",
    "Kỳ thi giả hai bài: đếm đoạn và phân rã chu trình. Mục tiêu: giải cả hai trong 45 phút.",
    """**Kỳ thi 2 — kỹ thuật.** A đếm đoạn 'D' dài nhất (một dòng quét); B
phân rã chu trình hoán vị sau khi ánh xạ hạng. Near-miss bị chấm ở bài
A: đếm từng ô 'D' thay vì từng đoạn (DDDD phải là 1 không phải 4); ở
bài B: đếm nửa số cặp sai thứ tự thay vì chu trình (đúng cho hoán vị
đối xứng, sai cho chu trình dài).
""",
    [C2A, C2B],
    [VI_C2A, VI_C2B],
    solutions=[
        (
            "hsg-cp-m20b-lanterns",
            CPP_STD + cpp("""    int n; in >> n;
    string s; in >> s;
    int runs = 0;
    bool inRun = false;
    for (char ch : s) {
        if (ch == 'D' && !inRun) { ++runs; inRun = true; }
        if (ch == 'L') inRun = false;
    }
    out << runs << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    string s; in >> s;
    int runs = 0;
    for (char ch : s)
        if (ch == 'D') ++runs;               // near-miss: per cell, not per run
    out << runs << "{{NL}}";
""") + END,
        ),
        (
            "hsg-cp-m20b-balloon",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    vector<long long> s = h;
    sort(s.begin(), s.end());
    vector<int> p(n + 1);
    for (int i = 0; i < n; ++i) {
        int idx = lower_bound(s.begin(), s.end(), h[i]) - s.begin();
        p[i + 1] = idx + 1;                  // 1-based permutation target
    }
    vector<char> vis(n + 1, 0);
    long long swaps = 0;
    for (int i = 1; i <= n; ++i) {
        if (vis[i]) continue;
        int len = 0, j = i;
        while (!vis[j]) { vis[j] = 1; j = p[j]; ++len; }
        swaps += len - 1;
    }
    out << swaps << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    vector<long long> s = h;
    sort(s.begin(), s.end());
    vector<int> p(n + 1);
    for (int i = 0; i < n; ++i) {
        int idx = lower_bound(s.begin(), s.end(), h[i]) - s.begin();
        p[i + 1] = idx + 1;
    }
    // near-miss: counts fixed-point misses / 2 — wrong for 3+ cycles
    int wrong = 0;
    for (int i = 1; i <= n; ++i)
        if (p[i] != i) ++wrong;
    out << wrong / 2 << "{{NL}}";
""") + END,
        ),
    ],
)

C3A = challenge(
    "hsg-cp-m20final-gridsum",
    "Final — A: Grid Corridor",
    T(
        "**Description:** An n x m grid of digits (0-9). You start at the top-left cell and",
        "walk to the bottom-right, moving only right or down, collecting the digits along",
        "the way (including both ends). Print the maximum total collectible.",
        "",
        "**Input:** Line 1: n m (1 <= n, m <= 1000). Next n lines: m digits each.",
        "**Output:** One integer — the maximum total.",
        "",
        "**Example:** `2 2` / `19` / `28` -> `11` (1->9->8).",
    ),
    [
        contest_test("sample", T("2 2", "19", "28"), T("11"), "1+9+8 beats 1+2+8 = 11? Both 11 — the point is the DP, not the winner."),
        contest_test("single cell", T("1 1", "7"), T("7"), "Just the start."),
        contest_test("one row", T("1 4", "1234"), T("10"), "Everything collected."),
        contest_test("zeros", T("2 2", "00", "00"), T("0"), "Nothing to collect."),
        contest_test("bigger", T("3 3", "123", "456", "789"), T("29"),
                     "1->4->7->8->9: classic diagonal."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_C3A = vi_challenge(
    "Chốt — A: Hành lang lưới",
    T(
        "**Đề bài:** Lưới n x m các chữ số (0-9). Bạn bắt đầu ở ô trên-trái và đi tới ô",
        "dưới-phải, chỉ đi phải hoặc xuống, thu các chữ số trên đường (gồm cả hai đầu).",
        "In tổng lớn nhất thu được.",
        "",
        "**Dữ liệu vào:** Dòng 1: n m (1 <= n, m <= 1000). n dòng tiếp: mỗi dòng m chữ số.",
        "**Dữ liệu ra:** Một số nguyên — tổng lớn nhất.",
        "",
        "**Ví dụ:** `2 2` / `19` / `28` -> `11` (1->9->8).",
    ),
    [
        ("sample", "1+9+8 bằng 1+2+8 = 11 — điểm nằm ở DP, không ở bên thắng."),
        ("single cell", "Chỉ ô xuất phát."),
        ("one row", "Thu hết."),
        ("zeros", "Không có gì để thu."),
        ("bigger", "1->4->7->8->9: đường chéo kinh điển."),
    ],
)

C3B = challenge(
    "hsg-cp-m20final-vault",
    "Final — B: The Vault Clock",
    T(
        "**Description:** A vault door shows a 4-digit display (0000..9999). Each second",
        "you may press one of two buttons: +1 or -1 on the LAST digit (wrapping: 9+1=0,",
        "0-1=9). Given the current display and the target display, print the minimum",
        "number of seconds.",
        "",
        "**Input:** Line 1: t (1 <= t <= 100000). Next t lines: two 4-digit strings cur",
        "and target.",
        "**Output:** t lines: the minimum presses for each case.",
        "",
        "**Example:** `1` / `1234 1230` -> `4` (press -1 four times on the last digit).",
    ),
    [
        contest_test("sample", T("1", "1234 1230"), T("4"), "Last digit 4->0: four -1 presses."),
        contest_test("same", T("1", "7777 7777"), T("0"), "Already there."),
        contest_test("wrap up", T("1", "0009 0001"), T("2"), "9->0->1: two presses."),
        contest_test("wrap down", T("1", "0001 0009"), T("2"), "1->0->9."),
        contest_test("multi", T("2", "9999 0000", "1234 4321"),
                     T("4", "12"),
                     "Each digit independently: 9->0 costs 1; 4->3->2->1 = 3, 3->2->1 = 2... per-digit sums."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_C3B = vi_challenge(
    "Chốt — B: Đồng hồ két sắt",
    T(
        "**Đề bài:** Cửa két hiển thị 4 chữ số (0000..9999). Mỗi giây bạn được bấm một",
        "trong hai nút: +1 hoặc -1 trên CHỮ SỐ CUỐI (quay vòng: 9+1=0, 0-1=9). Cho hiển",
        "thị hiện tại và hiển thị mục tiêu, in số giây ít nhất.",
        "",
        "**Dữ liệu vào:** Dòng 1: t (1 <= t <= 100000). t dòng tiếp: hai xâu 4 chữ số cur",
        "và target.",
        "**Dữ liệu ra:** t dòng: số lần bấm ít nhất cho mỗi case.",
        "",
        "**Ví dụ:** `1` / `1234 1230` -> `4` (bấm -1 bốn lần trên chữ số cuối).",
    ),
    [
        ("sample", "Chữ số cuối 4->0: bốn lần -1."),
        ("same", "Đã ở đích."),
        ("wrap up", "9->0->1: hai lần bấm."),
        ("wrap down", "1->0->9."),
        ("multi", "Từng chữ số độc lập: 9->0 tốn 1; cộng theo từng chữ số."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m20final",
    "Final Mock — Beginner Championship",
    "Two graded problems mixing DP and math. Target: both within 60 minutes, full score.",
    60,
    """**Mock cuối — vô địch người mới.** A là QHD lưới kinh điển; B là toán
độ cao modulo-10 (min bước quay vòng per digit). Near-miss bị chấm ở
bài A: duyệt thiếu cột/hàng đầu (khởi tạo dp sai biên); ở bài B: tính
hiệu số thường thay vì quay vòng (9->0 phải là 1 bước, không phải 9).

**Final mock — beginner championship.** A is the classic grid DP; B is
modulo-10 circular distance math. Graded near-misses: A initializes
the dp border wrong (misses first row/column); B uses plain
difference instead of circular distance (9->0 is 1 press, not 9).
""",
    "Mock cuối — Vô địch người mới",
    "Hai bài chấm trộn QHD và toán học. Mục tiêu: giải cả hai trong 60 phút, điểm trọn vẹn.",
    """**Mock cuối — vô địch người mới.** A là QHD lưới kinh điển; B là toán
độ cao modulo-10 (min bước quay vòng per digit). Near-miss bị chấm ở
bài A: duyệt thiếu cột/hàng đầu (khởi tạo dp sai biên); ở bài B: tính
hiệu số thường thay vì quay vòng (9->0 phải là 1 bước, không phải 9).
""",
    [C3A, C3B],
    [VI_C3A, VI_C3B],
    solutions=[
        (
            "hsg-cp-m20final-gridsum",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    vector<vector<long long>> dp(n, vector<long long>(m, 0));
    dp[0][0] = g[0][0] - '0';
    for (int j = 1; j < m; ++j) dp[0][j] = dp[0][j-1] + (g[0][j] - '0');
    for (int i = 1; i < n; ++i) dp[i][0] = dp[i-1][0] + (g[i][0] - '0');
    for (int i = 1; i < n; ++i)
        for (int j = 1; j < m; ++j)
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + (g[i][j] - '0');
    out << dp[n-1][m-1] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    vector<vector<long long>> dp(n, vector<long long>(m, 0));
    dp[0][0] = g[0][0] - '0';
    for (int j = 1; j < m; ++j) dp[0][j] = dp[0][j-1] + (g[0][j] - '0');
    for (int i = 1; i < n; ++i) dp[i][0] = dp[i-1][0] + (g[i][0] - '0');
    for (int i = 1; i < n; ++i)
        for (int j = 1; j < m; ++j)
            // near-miss: min instead of max — the corridor avoids valuable digits
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + (g[i][j] - '0');
    out << dp[n-1][m-1] << "{{NL}}";
""") + END,
        ),
        (
            "hsg-cp-m20final-vault",
            CPP_STD + cpp("""    int t; in >> t;
    string res;
    for (int i = 0; i < t; ++i) {
        string a, b; in >> a >> b;
        int total = 0;
        for (int k = 0; k < 4; ++k) {
            int d = a[k] - b[k];
            if (d < 0) d = -d;
            total += (d < 10 - d) ? d : 10 - d;   // circular distance
        }
        if (i) res += "{{NL}}";
        res += to_string(total);
    }
    out << res << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int t; in >> t;
    string res;
    for (int i = 0; i < t; ++i) {
        string a, b; in >> a >> b;
        int total = 0;
        for (int k = 0; k < 4; ++k) {
            int d = a[k] - b[k];
            if (d < 0) d = -d;
            // near-miss: plain difference — 9->0 costs 1, not 9
            total += d;
        }
        if (i) res += "{{NL}}";
        res += to_string(total);
    }
    out << res << "{{NL}}";
""") + END,
        ),
    ],
)

print("M20 done")
