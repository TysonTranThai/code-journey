#!/usr/bin/env python3
"""HSG Mastery — Module 13: hsgm-stress (Stress Testing & Decision Training).

The three-program harness (brute + candidate + generator), mismatch
minimization, and the meta-skill of contest-time decisions.
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


M = "hsgm-stress"
write_module(
    M,
    "Stress Testing and Decision Training",
    "The three-program harness: brute force as oracle, a generator, and differential testing; then the contest-level decisions the harness cannot make for you.",
    "Kiểm thử sức bền và huấn luyện quyết định",
    "Bộ ba chương trình: brute force làm nhà tiên tri, một bộ sinh, và kiểm thử vi phân; rồi những quyết định tầm thi mà harness không thể quyết thay bạn.",
    ["hsgm-m13-harness", "hsgm-m13-decide", "hsgm-cp-m13"],
    ["hsgm-p13-drills"],
)

write_lesson(
    M, "hsgm-m13-harness",
    "The Three-Program Harness",
    "Slow-but-certain beats fast-but-uncertain in testing: differential stress testing mechanizes the hunt for divergence.",
    13,
    """
# The Three-Program Harness

Stress testing is three programs in a loop:

1. **The oracle** — a brute-force solution, too slow for real constraints
   but obviously correct at small n.
2. **The candidate** — your fast solution, the thing under test.
3. **The generator** — a small seeded-random input producer.

The loop: generate → run both on the input → compare byte-exactly. On
the first mismatch, you hold in your hands a *failing input*, guaranteed.
Then shrink it to the minimal counterexample (Module 12) and diagnose.

## Making the harness bite

- **Seed everything.** A reproducible failure is fixable; a one-time
  mismatch you cannot regenerate is a ghost.
- **Vary the generator's *shape*, not just size.** Alternate sorted,
  reversed, tie-heavy, tiny-alphabet, extreme-values profiles — each
  shape is a different attack surface (Module 12's checklist, automated).
- **Compare outputs byte-exactly.** Trailing whitespace differences are
  real verdicts on judges; let the harness teach you that early.

## What stress finds and what it misses

Stress testing finds *behavioral* divergence reachable by your generator's
shapes. It cannot find overflow at n = 200000 (the oracle cannot run
there) or wrong-complexity death. For those, static analysis of the code
and the budget arithmetic remain the tools — stress complements, never
replaces, the checklist.
""",
    "Bộ ba chương trình",
    "Chậm-nhưng-chắc thắng nhanh-nhưng-không-chắc trong kiểm thử: kiểm thử vi phân máy móc hóa cuộc săn phân kỳ.",
    """
# Bộ ba chương trình

Kiểm thử sức bền là ba chương trình trong một vòng lặp:

1. **Nhà tiên tri** — lời giải brute force, quá chậm cho giới hạn thật
   nhưng rõ ràng đúng ở n nhỏ.
2. **Ứng viên** — lời giải nhanh của bạn, thứ đang bị kiểm thử.
3. **Bộ sinh** — bộ sinh input nhỏ có seed ngẫu nhiên.

Vòng lặp: sinh → chạy cả hai trên input → so byte-chính-xác. Tại phân kỳ
đầu tiên, bạn cầm trong tay một *input gãy*, được đảm bảo. Rồi thu nhỏ nó
thành phản ví dụ tối giản (Module 12) và chẩn đoán.

## Làm cho harness cắn

- **Seed mọi thứ.** Một lỗi tái hiện được là lỗi sửa được; một phân kỳ
  không tái hiện được là con ma.
- **Đổi *hình dạng* của bộ sinh, không chỉ kích thước.** Xen kẽ các hồ
  sơ đã-sort, đảo-ngược, nhiều-hòa, bảng-chữ-nhỏ, giá-trị-cực-trị — mỗi
  hình dạng là một bề mặt tấn công khác nhau (danh mục Module 12, tự
  động hóa).
- **So sánh output byte-chính-xác.** Khác biệt khoảng trắng cuối dòng là
  phán quyết thật trên trình chấm; để harness dạy bạn điều đó sớm.

## Stress tìm được gì và bỏ lỡ gì

Kiểm thử sức bền tìm *phân kỳ hành vi* mà các hình dạng của bộ sinh với
tới. Nó không thể tìm tràn số ở n = 200000 (nhà tiên tri không chạy nổi
ở đó) hoặc cái chết vì sai độ phức tạp. Với những cái đó, phân tích tĩnh
của code và phép tính ngân sách vẫn là công cụ — stress bổ sung, không
bao giờ thay thế, danh mục.
""",
)

write_lesson(
    M, "hsgm-m13-decide",
    "The Decision Tree of a Contest",
    "Read all problems first; allocate by certainty; when stuck, harvest partial and move. Time is the real constraint.",
    14,
    """
# The Decision Tree of a Contest

Algorithmic skill loses contests; decision skill loses them slightly less
often. The canonical tree:

1. **Read everything first.** The easy problem you skip by starting at
   problem 1 is the classic disaster. Order problems by
   (certainty × value) ÷ (expected time).
2. **Bank the certain ones.** Problems you know how to solve get solved
   and verified *before* the uncertain ones are touched.
3. **The stuck rule.** After ~15 minutes without a single structural
   insight (a model, an observation, a bound), switch. Stuck-time
   compounds: two 15-minute probes on two problems beat one 30-minute
   tunnel on one.
4. **The partial rule.** If the full solution is unclear but a band is
   clear, harvest the band (Module 10) and return later with fresh eyes.
5. **The last-hour rule.** No new problems in the final stretch unless
   banking one is faster than verifying submitted ones. Spend the end on
   re-reading your own code for the catalog bugs (Module 11).

## In-contest debugging budget

When your submission fails, the harness decides: is this a 5-minute typo
or a 40-minute wrong-model? Decide by evidence — sample tests pass
locally (typo-side) or fail (model-side). Never debug a wrong model
longer than it would take to re-derive the model.
""",
    "Cây quyết định của một kỳ thi",
    "Đọc hết đề trước; phân bổ theo độ chắc chắn; khi bí, thu hoạch điểm một phần và chuyển. Thời gian mới là ràng buộc thật.",
    """
# Cây quyết định của một kỳ thi

Kỹ năng thuật toán thua các kỳ thi; kỹ năng quyết định thua chúng ít hơn
một chút. Cây kinh điển:

1. **Đọc hết trước.** Bài dễ mà bạn bỏ sót vì bắt đầu từ bài 1 là thảm
   họa kinh điển. Xếp hạng bài theo (chắc chắn × giá trị) ÷ (thời gian
   kỳ vọng).
2. **Gửi ngân các bài chắc.** Bài biết cách giải được giải và xác minh
   *trước khi* đụng vào các bài bất định.
3. **Luật bí.** Sau ~15 phút không có một nhận xét cấu trúc nào (một mô
   hình, một nhận xét, một cận), chuyển. Thời gian-bí cộng dồn: hai lần
   dò 15 phút trên hai bài thắng một đường hầm 30 phút trên một bài.
4. **Luật điểm một phần.** Nếu lời giải đầy đủ chưa rõ nhưng một dải rõ,
   thu hoạch dải đó (Module 10) và quay lại sau với đôi mắt mới.
5. **Luật giờ cuối.** Không mở bài mới trong quãng cuối trừ khi gửi ngân
   một bài nhanh hơn xác minh các bài đã nộp. Dành giờ cuối để đọc lại
   code của chính mình tìm các bug trong danh mục (Module 11).

## Ngân sách gỡ lỗi trong thi

Khi lần nộp gãy, harness quyết định: đây là lỗi chính tả 5 phút hay mô
hình sai 40 phút? Quyết định bằng bằng chứng — test mẫu chạy đúng tại chỗ
(phía lỗi-chính-tả) hay sai (phía lỗi-mô-hình). Đừng bao giờ gỡ một mô
hình sai lâu hơn thời gian cần để suy lại mô hình.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p13-d1", "The Silent Generator",
    "Your stress harness ran 10,000 iterations finding nothing, but the judge rejected you. Most likely harness flaw?",
    [
        "Not enough iterations — run a million",
        "The generator only produces one input *shape* (e.g., uniformly random) — the failing shape (ties, sorted-desc, extremes) was never generated",
        "The brute force is wrong",
        "Seeds are unnecessary",
    ],
    "B",
    "Uniform randomness under-samples every adversarial shape. Shape-varied generators (ties, monotone, extreme values) are what make stress testing find the judge's cases.",
    vi_title="Bộ sinh câm lặng",
    vi_scenario="Harness stress của bạn chạy 10,000 vòng không thấy gì, nhưng trình chấm từ chối bạn. Lỗi harness khả dĩ nhất?",
    vi_options=[
        "Chưa đủ vòng — chạy một triệu",
        "Bộ sinh chỉ sinh một *hình dạng* input (ví dụ ngẫu nhiên đều) — hình dạng gãy (hòa, sort-giảm, cực trị) chưa từng được sinh",
        "Brute force bị sai",
        "Seed là không cần thiết",
    ],
    vi_hint="Tính ngẫu nhiên đều lấy mẫu thiếu mọi hình dạng phản đốidraulic. Bộ sinh đa-hình-dạng (hòa, đơn điệu, giá trị cực trị) mới là thứ giúp stress tìm ra các case của trình chấm.",
)

D2, D2VI = recognition_drill(
    "hsgm-p13-d2", "The Tunnel",
    "45 minutes in, you have one structural idea left untested on problem 2, and problem 4 (worth the same) you can solve in 20. The decision tree says:",
    [
        "Finish problem 2's idea — sunk cost means you should not waste the investment",
        "Switch to problem 4: bank the certain solve, then return to 2 with the remaining time",
        "Skip both and read the statements again",
        "Optimize problem 1's solution further",
    ],
    "B",
    "Sunk cost is not a reason. Certainty × value ÷ time favors problem 4; banking it first also removes psychological pressure from the return to problem 2.",
    vi_title="Đường hầm",
    vi_scenario="45 phút trôi qua, bạn còn một ý tưởng cấu trúc chưa thử ở bài 2, và bài 4 (cùng giá trị điểm) bạn giải được trong 20 phút. Cây quyết định nói:",
    vi_options=[
        "Chốt ý tưởng bài 2 — chi phí đã bỏ ra nghĩa là đừng lãng phí khoản đầu tư",
        "Chuyển sang bài 4: gửi ngân ph solve chắc chắn, rồi quay lại bài 2 với thời gian còn lại",
        "Bỏ cả hai và đọc lại đề",
        "Tối ưu thêm lời giải bài 1",
    ],
    vi_hint="Chi phí chìm không phải là lý do. Chắc chắn × giá trị ÷ thời gian nghiêng về bài 4; gửi ngân trước cũng bớt áp lực tâm lý cho lần quay lại bài 2.",
)

D3, D3VI = recognition_drill(
    "hsgm-p13-d3", "The Ghost Mismatch",
    "Your stress harness found one mismatch, but the input was regenerated with a new random seed and now nothing fails. First move?",
    [
        "Move on — it was a fluke",
        "Fix the seed: reproduce first, shrink second. An unreproducible failure is unfixable; re-seed with a fixed value and re-run the exact sequence",
        "Increase the input size in the generator",
        "Delete the brute force to speed up the loop",
    ],
    "B",
    "Reproducibility is the harness's core contract: seed everything, log the seed with every mismatch. Only a reproducible failure can be shrunk into a counterexample.",
    vi_title="Phân kỳ ma",
    vi_scenario="Harness stress tìm thấy một phân kỳ, nhưng input được tái sinh với seed mới và giờ không gì gãy nữa. Nước đi đầu tiên?",
    vi_options=[
        "Chuyển tiếp — chỉ là sự cố nhất thời",
        "Chốt seed: tái hiện trước, thu nhỏ sau. Một lỗi không tái hiện được là không thể sửa; seed lại bằng giá trị cố định và chạy lại đúng chuỗi",
        "Tăng kích thước input trong bộ sinh",
        "Xóa brute force để vòng lặp nhanh hơn",
    ],
    vi_hint="Khả năng tái hiện là hợp đồng lõi của harness: seed mọi thứ, ghi seed cùng mọi phân kỳ. Chỉ lỗi tái hiện được mới thu nhỏ được thành phản ví dụ.",
)

write_practice(
    M, "hsgm-p13-drills", "Stress & Decision Drills",
    "Three drills: shape-varied generation, the sunk-cost trap, and reproducibility discipline.",
    "Drill sức bền & quyết định",
    "Ba drill: sinh đa-hình-dạng, bẫy chi-phí-chìm, và kỷ luật tái hiện.",
    "hsgm-m13-decide", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p13-d1": D1VI, "hsgm-p13-d2": D2VI, "hsgm-p13-d3": D3VI},
    solutions=[
        ("hsgm-p13-d1", letter("B"), letter("A")),
        ("hsgm-p13-d2", letter("B"), letter("A")),
        ("hsgm-p13-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: a min-stack protocol — push x / pop / ask-min — where the W is
# the classic "single min variable" stack that forgets to restore the
# previous min after pops. The two-program idea is embodied in the test
# design: adversarial pop sequences.
def _gt_minstack(ops):
    st = []
    out = []
    for op, v in ops:
        if op == 1:
            st.append(v)
        elif op == 2:
            if st:
                st.pop()
        else:
            out.append(min(st) if st else -1)
    return out


_ops13 = [
    (1, 5), (3, 0), (1, 3), (3, 0), (1, 7), (1, 2), (3, 0),
    (2, 0), (3, 0),           # pop 2 → min back to 3 (the W keeps 2)
    (2, 0), (2, 0), (3, 0),   # pop 7, 3 → min 5 (W still says 2)
    (1, 1), (3, 0),           # push 1 → min 1
    (2, 0), (3, 0),           # pop 1 → min 5 (W says 1 forever)
    (2, 0), (2, 0), (3, 0),   # pop 5 → empty → -1
]
_gt13 = _gt_minstack(_ops13)


def _w_minstack(ops):
    st = []
    mn = None
    out = []
    for op, v in ops:
        if op == 1:
            st.append(v)
            if mn is None or v < mn:
                mn = v
        elif op == 2:
            if st:
                st.pop()   # BUG: mn never restored
        else:
            out.append(mn if st else -1)
    return out


_w13 = _w_minstack(_ops13)
assert _w13 != _gt13, (_gt13, _w13)

CP_M13_IN = T(str(len(_ops13)), *[(f"{op} {v}" if op == 1 else str(op)) for (op, v) in _ops13])
CP_M13_WANT = T(*[str(v) for v in _gt13])

CP13C = challenge(
    "hsgm-cp-m13-minstack",
    "Checkpoint: The Amnesiac Stack",
    """**Task.** Process a stack protocol: `1 x` pushes x; `2` pops the top
(popping an empty stack does nothing); `3` prints the current minimum of
the stack, or −1 if empty.

**Constraints:** 1 ≤ number of operations ≤ 200000; 0 ≤ x < 10^9. Every
`3` prints on its own line.

**Think:** this is the stress-harness module — mentally simulate the
pop-heavy test below twice before submitting.
""",
    [
        contest_test("push push ask", T("3", "1 4", "1 2", "3"), T("2"),
            "Stack {4, 2}: min 2."),
        contest_test("pop empty guard", T("2", "2", "3"), T("-1"),
            "Pop on empty does nothing; ask on empty → −1."),
    ],
    level="debugging",
    difficulty="advanced",
)
CP13C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("push push ask", T("3", "1 4", "1 2", "3"), T("2"),
            "Stack {4, 2}: min 2."),
        contest_test("pop empty guard", T("2", "2", "3"), T("-1"),
            "Pop on empty does nothing; ask on empty → −1."),
        contest_test("pop restores min", T("6", "1 5", "1 3", "1 2", "2", "3", "3"),
            T("3", "3"), "Push 5,3,2 → min 2; pop → stack {5,3}: min 3; ask again: 3. Two asks, both 3."),
        contest_test("amnesia storm", CP_M13_IN, CP_M13_WANT,
            "Pop-heavy sequence with pushes interleaved: every pop must restore the previous min. Ground truth simulated in Python."),
    )
]

CP13VI = vi_challenge(
    "Điểm kiểm tra: ngăn xếp đãng trí",
    """**Bài toán.** Xử lý một giao thức ngăn xếp: `1 x` đẩy x; `2` pop đỉnh
(pop ngăn rỗng thì không làm gì); `3` in min hiện tại của ngăn xếp, hoặc
−1 nếu rỗng.

**Ràng buộc:** 1 ≤ số thao tác ≤ 200000; 0 ≤ x < 10^9. Mỗi `3` in trên
một dòng riêng.

**Suy nghĩ:** đây là module harness-sức-bền — hãy mô phỏng trong đầu test
nhiều-pop dưới đây hai lần trước khi nộp.
""",
    [("đẩy đẩy hỏi", "Ngăn {4, 2}: min 2."),
     ("chặn pop rỗng", "Pop trên rỗng không làm gì; hỏi trên rỗng → −1."),
     ("pop khôi phục min", "Đẩy 5,3,2 → min 2; pop → ngăn {5,3}: min 3; hỏi lại: 3. Min KHÔI PHỤC sau pop."),
     ("bão đãng-trí", "Chuỗi nhiều-pop xen kẽ đẩy: mọi pop phải khôi phục min trước đó. Đáp án chuẩn mô phỏng bằng Python.")],
)

CP_M13_R = CPP_STD + cpp("""    int q; in >> q;
    vector<pair<long long, long long>> st;   // (value, min-at-this-point)
    for (int i = 0; i < q; ++i) {
        int op; long long v; in >> op;
        if (op == 1) {
            in >> v;
            long long m = st.empty() ? v : min(v, st.back().second);
            st.push_back({v, m});
        } else if (op == 2) {
            if (!st.empty()) st.pop_back();
        } else {
            out << (st.empty() ? -1 : st.back().second) << "{{NL}}";
        }
    }
""") + END

CP_M13_W = CPP_STD + cpp("""    int q; in >> q;
    vector<long long> st;
    long long mn = LLONG_MAX;
    for (int i = 0; i < q; ++i) {
        int op; long long v; in >> op;
        if (op == 1) {
            in >> v;
            st.push_back(v);
            mn = min(mn, v);
        } else if (op == 2) {
            if (!st.empty()) st.pop_back();
            // BUG: mn is never restored — after popping the minimum away,
            // every later ask keeps reporting the dead minimum.
        } else {
            out << (st.empty() ? -1 : mn) << "{{NL}}";
        }
    }
""") + END

write_checkpoint(
    M, "hsgm-cp-m13", "Checkpoint — The Amnesiac Stack",
    "Min-stack protocol: pair (value, min-so-far) restores the minimum on every pop. The W is the classic single-variable min that never comes back — the amnesia the pop-heavy test exposes.",
    25,
    """
**Checkpoint — The Amnesiac Stack.** The min-stack is the canonical
'carry the aggregate in the state' structure: each stack entry stores
(value, min-from-bottom-to-here), so a pop restores the previous minimum
automatically. The W keeps a single global min variable and never
restores it — after the minimum is popped, every future ask reports a
value that is no longer in the stack. The pop-heavy test is the harness
discipline made concrete: trace pops twice before trusting.
""",
    "Điểm kiểm tra — Ngăn xếp đãng trí",
    "Giao thức min-stack: cặp (giá trị, min-tới-đây) khôi phục min sau mọi pop. W là biến min đơn kinh điển không bao giờ quay lại — căn bệnh đãng trí mà test nhiều-pop phơi bày.",
    """
**Điểm kiểm tra — Ngăn xếp đãng trí.** Min-stack là cấu trúc kinh điển
'mang tổng hợp trong trạng thái': mỗi phần tử ngăn xếp lưu (giá trị,
min-từ-đáy-đến-đây), nên một pop tự động khôi phục min trước đó. W giữ
một biến min toàn cục duy nhất và không bao giờ khôi phục — sau khi min
bị pop, mọi câu hỏi sau báo một giá trị không còn trong ngăn xếp. Test
nhiều-pop là kỷ luật harness được cụ thể hóa: truy vết pop hai lần trước
khi tin.
""",
    CP13C,
    CP13VI,
    CP_M13_R,
    CP_M13_W,
)

print("module m13 complete")
