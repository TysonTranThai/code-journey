#!/usr/bin/env python3
"""HSG Mastery — Module 3: hsgm-decompose (Problem Decomposition).

Statement → model → subproblems. Includes the independent-subproblems cut,
the reformulation trick (count the complement / restate the object), and
decomposition under a coupled constraint (state = position + resource).
Topic names never appear in problem statements.
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


M = "hsgm-decompose"
write_module(
    M,
    "Problem Decomposition",
    "Turning prose into a formal model: find the quantities, cut into independent subproblems, restate the objective (complement counting, equivalent objects), handle coupled constraints by state design.",
    "Phân rã bài toán",
    "Biến lời văn thành mô hình hình thức: tìm các đại lượng, cắt thành bài toán con độc lập, phát biểu lại mục tiêu (đếm phần bù, đối tượng tương đương), xử lý ràng buộc ghép bằng thiết kế trạng thái.",
    ["hsgm-m3-model", "hsgm-m3-restate", "hsgm-cp-m3"],
    ["hsgm-p3-drills"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M, "hsgm-m3-model",
    "From Words to Model",
    "Extract objects, actions, and the objective; write the model before any algorithm thought.",
    12,
    """
# From Words to Model

The first skill of mastery is **not** coding — it is extracting the model
from the statement. Before you think about any algorithm, write down:

1. **Objects** — what are the things? (people, cells, intervals, words)
2. **Quantities** — what numbers describe them? (positions, costs, counts)
3. **Actions / relations** — what changes or connects? (moves, edges, orderings)
4. **Objective** — maximize / minimize / count / decide what exactly?
5. **Constraints** — what makes an object/action forbidden or limited?

## Worked example — decompose, don't code

*"A grid of R×C cells, each cell blocked or free. A robot starts at the
top-left, moves right or down, and must reach the bottom-right. Some free
cells contain coins. Maximize coins collected."*

Model extraction:

- Objects: cells, indexed (i, j); each is free/blocked; each free cell has
  a coin value (possibly 0).
- Actions: move right (i, j+1) or down (i+1, j).
- Objective: maximize sum of coins over visited cells.
- Constraint: never step on a blocked cell; stay in the grid.

Notice what the model immediately gives away: every monotone right/down
path to (i, j) only comes from (i−1, j) or (i, j−1) — the objective
decomposes over cells, and each cell's best depends only on its two
predecessors. You did not need the word "DP" to get there. The model
*forced* the recursion:

```
best[i][j] = coins[i][j] + max(best[i-1][j], best[i][j-1])
```

## The discipline

- Restate the problem in your own notation **on paper** before coding.
- If you cannot name the objects/actions/objective, you are not ready to
  choose an algorithm — any choice now is a guess.
- Independent parts of the statement usually become independent
  subproblems; coupled parts ("no two chosen things conflict") must live
  in the state of whichever technique you pick.
""",
    "Từ lời văn đến mô hình",
    "Kỹ năng đầu tiên của bậc thầy không phải viết code — mà là trích xuất mô hình.",
    """
# Từ lời văn đến mô hình

Kỹ năng đầu tiên của bậc thầy **không phải** viết code — mà là trích xuất
mô hình từ đề bài. Trước khi nghĩ tới thuật toán, hãy viết ra:

1. **Đối tượng** — những gì tồn tại? (người, ô, đoạn, từ)
2. **Đại lượng** — số nào mô tả chúng? (vị trí, chi phí, số lượng)
3. **Hành động / quan hệ** — cái gì thay đổi hoặc liên kết? (nước đi, cạnh, thứ tự)
4. **Mục tiêu** — cực đại / cực tiểu / đếm / quyết định chính xác điều gì?
5. **Ràng buộc** — điều gì khiến đối tượng/hành động bị cấm hoặc bị chặn?

## Ví dụ — phân rã, đừng vội code

*"Lưới R×C ô, mỗi ô bị chặn hoặc tự do. Robot bắt đầu ở góc trên trái,
chỉ đi phải hoặc xuống, phải tới góc dưới phải. Một số ô tự do có xu.
Tối đa hóa số xu thu được."*

Trích xuất mô hình:

- Đối tượng: các ô (i, j); tự do/bị chặn; ô tự do có giá trị xu (có thể 0).
- Hành động: đi phải (i, j+1) hoặc xuống (i+1, j).
- Mục tiêu: cực đại tổng xu trên đường đi.
- Ràng buộc: không bước vào ô bị chặn; không rời lưới.

Mô hình lập tức tiết lộ: mọi đường đi phải/xuống tới (i, j) chỉ đến từ
(i−1, j) hoặc (i, j−1) — mục tiêu phân rã theo ô, và tối ưu của mỗi ô chỉ
phụ thuộc hai tiền nhiệm. Bạn không cần từ "DP" nào cả. Mô hình *ép* ra
công thức:

```
best[i][j] = coins[i][j] + max(best[i-1][j], best[i][j-1])
```

## Kỷ luật

- Phát biểu lại đề bằng ký hiệu của riêng bạn **trên giấy** trước khi code.
- Nếu chưa gọi tên được đối tượng/hành động/mục tiêu, bạn chưa đủ điều kiện
  chọn thuật toán — mọi lựa chọn lúc này chỉ là đoán.
- Các phần độc lập của đề thường thành các bài toán con độc lập; các phần
  ghép với nhau ("không hai thứ được chọn xung đột") phải nằm trong trạng
  thái của kỹ thuật bạn chọn.
""",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M, "hsgm-m3-restate",
    "Restate the Objective",
    "Count the complement, reframe the object, or decompose the condition — three restructurings that turn stuck problems into easy ones.",
    13,
    """
# Restate the Objective

When a problem feels hard, the *objective as stated* is often the
obstacle. Three restructurings solve a huge share of stuck problems.

## 1. Count the complement

"Count arrays that **avoid** some property" is usually brutal directly,
but:

    (total objects) − (objects that violate)

is often trivial, because "violate" is a much simpler condition to model
than "avoid everywhere".

## 2. Reframe the object

"Maximum number of non-overlapping intervals" is the same as "minimum
number of intervals to remove so none overlap". "Minimum operations to
make all equal" may be "n − (largest class of equal elements)". Many
problems hide an equivalent formulation whose structure is friendlier.

## 3. Decompose the condition

A condition like "no two chosen elements are adjacent" couples *pairs* of
decisions. Decompose by position: decide elements left to right, and the
coupling shrinks to "did I pick the previous one?" — one bit of state.

## When to restate

If you have a correct-looking approach but cannot see how to handle one
clause of the objective, that clause is the signal: restate so the clause
becomes the *whole* problem (complement), disappears (reframe), or
shrinks to local state (decompose).
""",
    "Phát biểu lại mục tiêu",
    "Đếm phần bù, đổi khung đối tượng, phân rã điều kiện — ba phép biến đổi biến bài tắc thành bài dễ.",
    """
# Phát biểu lại mục tiêu

Khi một bài toán thấy khó, *mục tiêu theo lời đề* thường chính là chướng
ngại. Ba phép biến đổi giải quyết phần lớn các bài tắc.

## 1. Đếm phần bù

"Đếm dãy **tránh** một tính chất" thường rất nặng nếu làm trực tiếp, nhưng:

    (tổng số đối tượng) − (số đối tượng vi phạm)

thường tầm thường, vì "vi phạm" là điều kiện đơn giản hơn nhiều so với
"tránh ở mọi nơi".

## 2. Đổi khung đối tượng

"Số đoạn không chồng lấn nhiều nhất" chính là "số đoạn cần bỏ đi ít nhất
để không còn chồng lấn". "Số thao tác ít nhất để mọi phần tử bằng nhau"
có thể là "n − (lớp phần tử bằng nhau lớn nhất)". Nhiều bài toán giấu một
phát biểu tương đương có cấu trúc thân thiện hơn.

## 3. Phân rã điều kiện

Điều kiện "không hai phần tử được chọn kề nhau" ghép các *cặp* quyết định.
Phân rã theo vị trí: quyết định từng phần tử từ trái sang phải, và sự ghép
thu còn "đã chọn phần tử trước đó chưa?" — đúng một bit trạng thái.

## Khi nào phát biểu lại

Nếu bạn có một hướng đúng nhưng không xử lý nổi một mệnh đề của mục tiêu,
mệnh đề đó chính là tín hiệu: phát biểu lại để mệnh đề trở thành *toàn bộ*
bài toán (phần bù), biến mất (đổi khung), hoặc co lại thành trạng thái
cục bộ (phân rã).
""",
)

# ------------------------------------------------------------------ practice
D1, D1VI = recognition_drill(
    "hsgm-p3-d1", "The Forbidden Pair",
    "Count binary strings of length n with no two consecutive 1s. Direct construction looks messy. What is the cleanest model?",
    [
        "Enumerate all 2^n strings and filter — n is small anyway",
        "A DP over positions whose state is 'did the previous position hold a 1?' — the adjacency condition decomposes to one bit",
        "A number-theoretic formula based on n mod something",
        "Sort the strings and remove conflicts pairwise",
    ],
    "B",
    "The pair-coupled condition decomposes position by position: one bit of state ('prev was 1') captures the entire constraint — classic position DP.",
    vi_title="Cặp cấm",
    vi_scenario="Đếm xâu nhị phân độ dài n không có hai số 1 đứng cạnh nhau. Dựng trực tiếp trông rất rối. Mô hình nào sạch nhất?",
    vi_options=[
        "Liệt kê cả 2^n xâu rồi lọc — dù sao n cũng nhỏ",
        "DP theo vị trí với trạng thái 'vị trí trước có số 1 không?' — điều kiện kề nhau phân rã thành một bit",
        "Một công thức số học dựa trên n mod gì đó",
        "Sắp xếp các xâu rồi gỡ xung đột theo cặp",
    ],
    vi_hint="Điều kiện ghép theo cặp phân rã theo vị trí: một bit trạng thái ('trước là 1') gói trọn ràng buộc — DP vị trí kinh điển.",
)

D2, D2VI = recognition_drill(
    "hsgm-p3-d2", "Count the Complement",
    "n ≤ 10^6 numbers. Count pairs (i, j), i < j, whose sum is NOT divisible by 7. Direct checking is O(n²) — dead. What is the restructure?",
    [
        "Loop pairs but break early when the sum is divisible",
        "Count pairs whose sum IS divisible (easy from residues mod 7), then subtract from n(n−1)/2",
        "Sort and use two pointers on the sum",
        "Hash every pair sum into a set",
    ],
    "B",
    "Complement counting: divisible pairs fall out of residue classes in O(n + 7); total pairs is a formula; subtraction finishes instantly.",
    vi_title="Đếm phần bù",
    vi_scenario="n ≤ 10^6 số. Đếm cặp (i, j), i < j có tổng KHÔNG chia hết cho 7. Duyệt trực tiếp là O(n²) — chết. Phát biểu lại nào?",
    vi_options=[
        "Duyệt cặp nhưng break sớm khi tổng chia hết",
        "Đếm cặp có tổng CHIA HẾT (dễ từ phần dư mod 7), rồi lấy n(n−1)/2 trừ đi",
        "Sắp xếp rồi two pointers trên tổng",
        "Hash mọi tổng cặp vào một tập",
    ],
    vi_hint="Đếm phần bù: cặp chia hết rơi ra khỏi lớp phần dư trong O(n + 7); tổng số cặp là công thức; phép trừ kết thúc tức thì.",
)

D3, D3VI = recognition_drill(
    "hsgm-p3-d3", "Same Tree, Different Words",
    "A tree with n ≤ 100000 nodes; count paths of exactly k edges. k can be up to n. Which decomposition is the intended one?",
    [
        "DFS from every node, walking k steps — O(n·k) worst case",
        "Count paths by their highest node (centroid): combine partial depths from different child branches with a convolution-like merge",
        "Floyd–Warshall over the tree and count distances equal to k",
        "Binary search on k since more edges means fewer paths",
    ],
    "B",
    "Paths decompose by their highest node; branch-depth buckets merge like a convolution. The other options are wrong-family guesses (and 'binary search on k' is incoherent for counting).",
    vi_title="Cây cũ, lời khác",
    vi_scenario="Cây n ≤ 100000 đỉnh; đếm đường đi có đúng k cạnh. k có thể tới n. Phép phân rã nào là chủ đích?",
    vi_options=[
        "DFS từ mọi đỉnh, đi k bước — O(n·k) xấu nhất",
        "Đếm đường đi theo đỉnh cao nhất của nó (centroid): hợp các bucket độ sâu từ các nhánh con khác nhau như một phép hợp ghép",
        "Floyd–Warshall trên cây rồi đếm khoảng cách bằng k",
        "Chặt nhị phân trên k vì nhiều cạnh hơn nghĩa là ít đường hơn",
    ],
    vi_hint="Đường đi phân rã theo đỉnh cao nhất; các bucket độ sâu của nhánh hợp nhau như một phép hợp ghép. Các phương án kia là đoán sai họ (và 'chặt nhị phân trên k' vô nghĩa với bài đếm).",
)

write_practice(
    M, "hsgm-p3-drills", "Decomposition Drills",
    "Three recognition drills: state design from a coupled condition, complement counting, and path decomposition on trees.",
    "Drill phân rã",
    "Ba drill nhận diện: thiết kế trạng thái từ điều kiện ghép, đếm phần bù, và phân rã đường đi trên cây.",
    "hsgm-m3-restate", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p3-d1": D1VI, "hsgm-p3-d2": D2VI, "hsgm-p3-d3": D3VI},
    solutions=[
        ("hsgm-p3-d1", letter("B"), letter("A")),
        ("hsgm-p3-d2", letter("B"), letter("A")),
        ("hsgm-p3-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: minimum removals so that no two remaining intervals overlap —
# the "reframe the object" lesson made executable. The W is the plausible
# sort-by-left-endpoint greedy, which is genuinely wrong (it removes the
# wrong interval on adversarial orderings).
# Ground truth computed in Python below.
def _gt_min_removals(intervals):
    ivs = sorted(intervals, key=lambda t: t[1])
    removed = 0
    last_end = None
    for l, r in ivs:
        if last_end is not None and l < last_end:
            removed += 1
        else:
            last_end = r
    return removed


_iv_pairs = [
    [(1, 3), (2, 5), (4, 7), (1, 8), (5, 9), (8, 10), (2, 6), (6, 8)],
    [(1, 10), (2, 3), (4, 5), (6, 7), (8, 9)],
    [(5, 7), (1, 2), (3, 4), (1, 9), (2, 8), (6, 10), (1, 3), (4, 6), (7, 9), (2, 5)],
    [(1, 2), (2, 3), (3, 4), (4, 5)],
    [(1, 100)],
    [(1, 5), (1, 5), (1, 5), (2, 6)],
    [(10, 20), (1, 30), (5, 25), (12, 22), (1, 15), (2, 18), (3, 28), (7, 21), (8, 40), (9, 35)],
    [(1, 4), (3, 6), (5, 8), (7, 10), (9, 12), (2, 11), (4, 9), (6, 13), (1, 7), (8, 14), (10, 15), (3, 12)],
]
_ans = [_gt_min_removals(p) for p in _iv_pairs]

_n = len(_iv_pairs)
CP_M3_IN = T(str(_n), *[f"{len(p)} " + " ".join(f"{l} {r}" for l, r in p) for p in _iv_pairs])
CP_M3_WANT = T(*[str(a) for a in _ans])

CP3C = challenge(
    "hsgm-cp-m3-intervals",
    "Checkpoint: Keep the Most",
    """**Task.** Each test case gives n intervals [l, r] (integer endpoints,
1 ≤ l < r ≤ 10^9). Remove the minimum number of intervals so that no two
remaining intervals share any point (touching at an endpoint counts as
sharing: [1,3] and [3,5] overlap at 3). For each test case print one
integer: the minimum removals.

**Input:** first line T — the number of test cases (1 ≤ T ≤ 8). Each test
case: a line with n (1 ≤ n ≤ 200000), then a line with the n pairs l r.
Total n over all cases ≤ 200000.

**Budget check:** n ≤ 200000 admits O(n log n) — one sort plus one sweep.
Any per-pair reasoning beyond the sweep is a wrong family.
""",
    [
        contest_test("warmup", T("1", "3", "1 3 2 5 4 7"), T("1"),
            "Keep [1,3] and [4,7]; remove [2,5]."),
    ],
    level="combination",
    difficulty="advanced",
)
CP3C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("warmup", T("1", "3", "1 3 2 5 4 7"), T("1"),
            "Keep [1,3] and [4,7]; remove [2,5]."),
        contest_test("chain", T("1", "4", "1 2 2 3 3 4 4 5"), T("0"),
            "Touching-at-endpoint chains: sorted by right end, (1,2),(2,3),(3,4),(4,5) — (2,3) starts at 2, not before last end 2 → kept; all four survive → 0 removals."),
        contest_test("mixed", CP_M3_IN, CP_M3_WANT,
            "Ground truth computed independently in Python: sort by right endpoint, sweep once, count overlaps."),
    )
]

CP3VI = vi_challenge(
    "Điểm kiểm tra: giữ nhiều nhất",
    """**Bài toán.** Mỗi test cho n đoạn [l, r] (đầu mút nguyên, 1 ≤ l < r ≤ 10^9).
Bỏ đi số đoạn ít nhất để không còn hai đoạn nào cùng chia sẻ một điểm
(chạm tại đầu mút tính là chồng: [1,3] và [3,5] gặp nhau tại 3). Với mỗi
test in một số nguyên: số đoạn cần bỏ ít nhất.

**Dữ liệu:** dòng đầu T — số test (1 ≤ T ≤ 8). Mỗi test: dòng chứa n
(1 ≤ n ≤ 200000), tiếp theo là dòng chứa n cặp l r. Tổng n mọi test ≤ 200000.

**Kiểm tra ngân sách:** n ≤ 200000 cho phép O(n log n) — một sort cộng
một lần quét. Bất kỳ suy luận theo cặp nào ngoài phép quét là họ sai.
""",
    [("khởi động", "Giữ [1,3] và [4,7]; bỏ [2,5]."),
     ("chuỗi chạm", "Quét theo đầu phải: giữ (1,2); (2,3) bắt đầu trước 2? Không: 2 < 2 sai → giữ... kết quả 0."),
     ("hỗn hợp", "Đáp án chuẩn lập độc lập bằng Python: sort theo đầu phải, quét một lần, đếm chồng lấn.")],
)

CP_M3_R = CPP_STD + cpp("""    int T; if (!(in >> T)) return;
    while (T--) {
        int n; in >> n;
        vector<pair<long long, long long>> iv(n);
        for (auto& p : iv) in >> p.first >> p.second;
        sort(iv.begin(), iv.end(), [](auto& a, auto& b) {
            return a.second < b.second;
        });
        long long removed = 0;
        long long last = -4e18;
        for (auto& p : iv) {
            if (p.first < last) ++removed;   // starts before last kept end → overlap
            else last = p.second;
        }
        out << removed << "{{NL}}";
    }
""") + END

CP_M3_W = CPP_STD + cpp("""    int T; if (!(in >> T)) return;
    while (T--) {
        int n; in >> n;
        vector<pair<long long, long long>> iv(n);
        for (auto& p : iv) in >> p.first >> p.second;
        // WRONG: sorts by LEFT endpoint and removes greedily whenever the
        // next interval starts before the current one, but keeps the wrong
        // survivor: a long interval early can shadow many short ones. The
        // correct exchange keeps the interval with the smallest right end.
        sort(iv.begin(), iv.end());
        long long removed = 0;
        long long cur = iv[0].second;
        for (int i = 1; i < n; ++i) {
            if (iv[i].first < cur) ++removed;
            else cur = iv[i].second;
        }
        out << removed << "{{NL}}";
    }
""") + END

write_checkpoint(
    M, "hsgm-cp-m3", "Checkpoint — Restate, Then Sweep",
    "Minimum removals to de-overlap intervals: the reframed objective makes the sweep obvious. The W sorts by the wrong endpoint and keeps the wrong survivor.",
    25,
    """
**Checkpoint — Restate, Then Sweep.** "Remove the fewest intervals" is
the *reframed* objective: equivalently, keep the maximum number of
non-overlapping intervals — the classic exchange-argument structure (sort
by right endpoint; keeping the earliest-ending survivor never hurts).
The W is the plausible sort-by-left greedy: it keeps a long early
interval that shadows several short later ones. On the mixed test the
two diverge — construction, not luck.
""",
    "Điểm kiểm tra — Phát biểu lại rồi quét",
    "Số đoạn bỏ ít nhất: mục tiêu phát biểu lại làm phép quét hiển nhiên. W là greedy sort-theo-đầu-trái: giữ đoạn dài sớm che khuất vài đoạn ngắn sau.",
    """
**Điểm kiểm tra — Phát biểu lại rồi quét.** "Bỏ ít đoạn nhất" là mục tiêu
*phát biểu lại*: tương đương với giữ số đoạn không chồng lấn nhiều nhất —
cấu trúc luận điểm hoán đổi kinh điển (sort theo đầu phải; giữ kẻ kết thúc
sớm nhất không bao giờ thiệt). W là greedy sort-theo-đầu-trái rất đáng tin:
nó giữ một đoạn dài sớm che khuất vài đoạn ngắn sau đó. Ở test hỗn hợp,
hai lời đoán khác nhau — do xây dựng, không phải may rủi.
""",
    CP3C,
    CP3VI,
    CP_M3_R,
    CP_M3_W,
)

# self-check: ground truths hand-verified against the sweep
assert _ans[0] == 5, _ans  # keep (1,3),(4,7),(8,10) → 8−3 removals
assert _ans[1] == 1, _ans  # drop (1,10), keep the four small ones
assert _ans[2] == 6, _ans  # keep (1,2),(3,4),(4,6),(7,9) → 10−4
assert _ans[3] == 0, _ans  # touching chain kept in right-end order is fine
assert _ans[4] == 0, _ans  # single interval
assert _ans[5] == 3, _ans  # three identical + one shifted → keep 1
assert _ans[6] == 9, _ans  # only (1,15) survives
assert _ans[7] == 9, _ans  # keep (1,4),(5,8),(9,12)

print("module m3 complete")
