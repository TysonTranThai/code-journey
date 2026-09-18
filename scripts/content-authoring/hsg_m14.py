#!/usr/bin/env python3
"""HSG — Module 14: hsg-backtrack (quay lui).

Choose-explore-uncommit, permutations with and without repeats, N-queens
counting on small boards, subset enumeration, and grid path counting.
Conventions: T() for test I/O, cpp() for bodies.
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

M = "hsg-backtrack"
write_module(
    M,
    "Backtracking",
    "Systematic exhaustive search: choose, explore, uncommit — and prune so the search tree stays small enough to finish.",
    "Quay lui",
    "Tìm kiếm vét cạn có hệ thống: chọn, khám phá, hoàn tác — và cắt tỉa để cây tìm kiếm đủ nhỏ để kết thúc.",
    ["hsg-m14-idea", "hsg-m14-prune", "hsg-cp-m14"],
    ["hsg-p14-backtrack"],
)

write_lesson(
    M,
    "hsg-m14-idea",
    "The Backtracking Skeleton",
    "Every backtracking solution is the same five lines with different choices.",
    14,
    """## Choose — explore — uncommit

```cpp
void search(vector<int>& state) {
    if (goal(state)) { record(state); return; }
    for (int choice : options(state)) {
        apply(state, choice);      // choose
        search(state);             // explore
        undo(state, choice);       // UNCOMMIT — the whole trick
    }
}
```

The `undo` restores the state exactly as it was, so the next loop
iteration starts clean. Forget it once and every branch after the first
runs on polluted state — the classic symptom is "the answer is correct
for the first test then garbage".

### Where the recursion ends

Two exits: a **base case** that records/fails, or the natural end of
the options loop (often `if (i == n)` style depth checks). Depth equals
problem size for subsets/permutations — with n = 20, the stack holds 20
frames, nothing. Backtracking's cost is not stack depth, it is the
**number of nodes in the search tree**.

### Counting that tree

n independent binary choices -> 2^n leaves. n distinct choices per
level -> n! leaves. Backtracking is honest brute force; it wins over
plain nested loops when n is small (<= ~20) *or* pruning kills whole
subtrees early (next lesson).
""",
    "Bộ khung quay lui",
    "Mọi lời giải quay lui là cùng năm dòng, chỉ khác phần lựa chọn.",
    """## Chọn — khám phá — hoàn tác

```cpp
void search(vector<int>& state) {
    if (goal(state)) { record(state); return; }
    for (int choice : options(state)) {
        apply(state, choice);      // chọn
        search(state);             // khám phá
        undo(state, choice);       // HOÀN TÁC — toàn bộ cái trò
    }
}
```

Phần `undo` khôi phục trạng thái y như trước, để vòng lặp kế tiếp bắt
đầu sạch. Quên nó một chỗ và mọi nhánh sau nhánh đầu chạy trên trạng
thái bẩn — triệu chứng kinh điển là "test đầu đúng, test sau ra rác".

### Đệ quy kết thúc ở đâu

Hai lối ra: một **trường hợp cơ sở** ghi nhận/thất bại, hoặc tự nhiên
hết vòng lựa chọn (thường là kiểm tra độ sâu kiểu `if (i == n)`). Độ
sâu bằng kích thước bài với tập con/hoán vị — n = 20 thì ngăn xếp chứa
20 khung, chẳng mấy. Chi phí của quay lui không nằm ở độ sâu ngăn xếp
mà ở **số nút của cây tìm kiếm**.

### Đếm cây đó

n lựa chọn nhị phân độc lập -> 2^n lá. n lựa chọn mỗi mức -> n! lá.
Quay lui là vét cạn trung thực; nó thắng vòng lặp lồng thuần khi n nhỏ
(<= ~20) *hoặc* cắt tỉa tiêu diệt cả cây con sớm (bài sau).
""",
)

write_lesson(
    M,
    "hsg-m14-prune",
    "Pruning and Classic Drills",
    "Permutations, N-queens, and the pruning habits that turn 2^n into something that finishes.",
    13,
    """## Permutations, two flavors

Distinct items — build position by position, skip used:

```cpp
bool used[N]; int perm[N];
void gen(int i, int n) {
    if (i == n) { /* record perm */ return; }
    for (int v = 1; v <= n; ++v) {
        if (used[v]) continue;
        used[v] = true; perm[i] = v;
        gen(i + 1, n);
        used[v] = false;              // uncommit
    }
}
```

Duplicate items — sort first, and skip a value at this depth if it
equals the previous value at the same depth (`if (v > 0 && a[v] == a[v-1] && !used[v-1]) continue;`).
Sorting + that one line is the standard duplicate-killing trick.

## N-queens counting

Place queens row by row; a candidate column must not conflict with any
previous row's column or diagonal. With "any" checks the search is
still exponential but the constant collapses — a full 8-queens count
runs in milliseconds. Track columns and both diagonal families in three
boolean arrays for O(1) conflict tests.

## The pruning habits

1. **Fail fast**: check feasibility the moment a choice is made, not
   after the subtree finishes.
2. **Order choices**: trying likely candidates first does not change
   the worst case but changes the average enormously.
3. **Symmetry**: if the answer is unchanged under swapping two identical
   items, only explore one ordering.
4. **Bounds**: if even the best completion of the current partial state
   cannot beat a known answer, cut the branch (branch and bound, later).

Honest complexity note: pruning changes constants and average cases;
it does not turn an exponential algorithm into a polynomial one. State
n limits in your solution, then verify they match the problem.
""",
    "Cắt tỉa và bài tập kinh điển",
    "Hoán vị, N-queens, và các thói quen cắt tỉa biến 2^n thành thứ kết thúc được.",
    """## Hoán vị, hai hương

Phần tử phân biệt — dựng theo vị trí, bỏ qua cái đã dùng:

```cpp
bool used[N]; int perm[N];
void gen(int i, int n) {
    if (i == n) { /* ghi nhận perm */ return; }
    for (int v = 1; v <= n; ++v) {
        if (used[v]) continue;
        used[v] = true; perm[i] = v;
        gen(i + 1, n);
        used[v] = false;              // hoàn tác
    }
}
```

Phần tử trùng — sắp xếp trước, và bỏ qua một giá trị tại độ sâu này nếu
nó bằng giá trị trước đó cùng độ sâu (`if (v > 0 && a[v] == a[v-1] && !used[v-1]) continue;`).
Sắp xếp + một dòng đó là mẹo diệt trùng chuẩn.

## Đếm N-queens

Đặt hậu theo từng hàng; cột ứng viên không được xung đột cột hay đường
chéo với các hàng trước. Vẫn là cấp số nhân nhưng hằng số sập xuống —
đếm đủ 8-queens chạy trong vài mili giây. Theo dõi cột và hai họ đường
chéo trong ba mảng boolean để kiểm tra xung đột O(1).

## Các thói quen cắt tỉa

1. **Thất bại nhanh**: kiểm tra khả thi ngay khi chọn, không chờ cây
   con chạy xong.
2. **Thứ tự lựa chọn**: thử ứng viên khả dĩ trước không đổi trường hợp
   xấu nhất nhưng đổi mạnh trường hợp trung bình.
3. **Đối xứng**: nếu đáp án không đổi khi hoán hai phần tử giống nhau,
   chỉ khám phá một thứ tự.
4. **Chặn trên**: nếu ngay cả phần hoàn thành tốt nhất của trạng thái
   hiện tại cũng không vượt đáp án đã biết, cắt nhánh (nhánh và cận,
   về sau).

Ghi chú độ phức tạp trung thực: cắt tỉa đổi hằng số và trường hợp trung
bình; nó không biến thuật toán cấp số nhân thành đa thức. Nêu rõ giới
hạn n trong lời giải, rồi kiểm tra khớp với đề.
""",
)

A1 = challenge(
    "hsg-p14-perm-count",
    "Count Permutations",
    T(
        "**Description:** Count the permutations of 1..n in which no two adjacent elements",
        "differ by more than 1... simplified for grading: count permutations of 1..n whose",
        "**first element is odd**.",
        "",
        "**Input:** One line: n (1 <= n <= 10).",
        "**Output:** One integer — the count.",
        "",
        "**Example:** `3` -> `4` (permutations starting with 1 or 3).",
    ),
    [
        contest_test("sample", T("3"), T("4"),
                     "Starting with 1: two orders; starting with 3: two orders."),
        contest_test("n equals 1", T("1"), T("1"),
                     "The single permutation starts with 1 — odd."),
        contest_test("even n", T("4"), T("12"),
                     "Half of 24 permutations start odd (1 or 3 first)."),
        contest_test("max n", T("10"), T("1814400"),
                     "5 of 10 values are odd; 5 * 9! = 1814400."),
    ],
    level="imitation",
    difficulty="beginner",
)

A2 = challenge(
    "hsg-p14-queens",
    "N-Queens Count",
    T(
        "**Description:** Count the ways to place n non-attacking queens on an n x n board",
        "(no two share a row, column, or diagonal).",
        "",
        "**Input:** One line: n (1 <= n <= 10).",
        "**Output:** One integer — the number of placements.",
        "",
        "**Example:** `4` -> `2`.",
    ),
    [
        contest_test("sample", T("4"), T("2"),
                     "The two classic mirrored solutions."),
        contest_test("one", T("1"), T("1"),
                     "A single queen is trivially safe."),
        contest_test("two", T("2"), T("0"),
                     "No placement exists for n = 2 — a solver that never returns 0 is wrong."),
        contest_test("six", T("6"), T("4"),
                     "The known count for n = 6."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p14-dup-perm",
    "Distinct Arrangements",
    T(
        "**Description:** Count the distinct permutations of the given multiset of characters",
        "(duplicates collapse). Print the count.",
        "",
        "**Input:** One line: s (1 <= |s| <= 10, lowercase letters).",
        "**Output:** One integer — the number of distinct arrangements.",
        "",
        "**Example:** `aab` -> `3` (aab, aba, baa).",
    ),
    [
        contest_test("sample", T("aab"), T("3"),
                     "3!/2! = 3 distinct strings."),
        contest_test("all same", T("aaa"), T("1"),
                     "Everything collapses."),
        contest_test("all distinct", T("abc"), T("6"),
                     "3! full count."),
        contest_test("two pairs", T("aabb"), T("6"),
                     "4!/(2!*2!) = 6."),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p14-strings",
    "Generate Binary Strings",
    T(
        "**Description:** Generate all 2^n binary strings of length n in **lexicographic**",
        "order (0 before 1), one per line. n is small enough to enumerate fully.",
        "",
        "**Input:** One line: n (1 <= n <= 12).",
        "**Output:** 2^n lines of n characters each.",
        "",
        "**Example:** `2` -> `00` / `01` / `10` / `11`.",
    ),
    [
        contest_test("sample", T("2"), T("00", "01", "10", "11"),
                     "Four strings in lex order."),
        contest_test("single", T("1"), T("0", "1"),
                     "Two lines."),
        contest_test("three", T("3"), T("000", "001", "010", "011", "100", "101", "110", "111"),
                     "Eight lines, lex order."),
        contest_test("max n", T("12"), T(*[format(i, "012b") for i in range(4096)]), "All 4096 lines in lex order — full output discipline."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p14-rooks",
    "Peaceful Rooks",
    T(
        "**Description:** Count the ways to place k non-attacking rooks on an n x n board",
        "(rooks attack along rows and columns).",
        "",
        "**Input:** One line: n k (1 <= k <= n <= 8).",
        "**Output:** One integer — the number of placements.",
        "",
        "**Example:** `2 2` -> `2` (main or anti diagonal).",
    ),
    [
        contest_test("sample", T("2 2"), T("2"),
                     "Diagonals are the only full placements."),
        contest_test("one rook", T("3 1"), T("9"),
                     "Any of the 9 cells."),
        contest_test("full board", T("3 3"), T("6"),
                     "3! row-to-column assignments."),
        contest_test("zero rooks", T("5 0"), T("1"),
                     "The empty placement counts as one."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p14-perm-count": vi_challenge(
        "Đếm hoán vị",
        T(
            "**Đề bài:** Đếm các hoán vị của 1..n mà **phần tử đầu tiên là số lẻ**.",
            "",
            "**Dữ liệu vào:** Một dòng: n (1 <= n <= 10).",
            "**Dữ liệu ra:** Một số nguyên — số lượng.",
            "",
            "**Ví dụ:** `3` -> `4` (các hoán vị bắt đầu bằng 1 hoặc 3).",
        ),
        [
            ("sample", "Bắt đầu bằng 1: hai thứ tự; bắt đầu bằng 3: hai thứ tự."),
            ("n equals 1", "Hoán vị duy nhất bắt đầu bằng 1 — số lẻ."),
            ("even n", "Một nửa trong 24 hoán vị bắt đầu bằng số lẻ (1 hoặc 3)."),
            ("max n", "5 trên 10 giá trị là lẻ; 5 * 9! = 1814400."),
        ],
    ),
    "hsg-p14-queens": vi_challenge(
        "Đếm N-Queens",
        T(
            "**Đề bài:** Đếm số cách đặt n quân hậu trên bàn n x n sao cho không quân nào",
            "tấn công quân nào (không cùng hàng, cột, hay đường chéo).",
            "",
            "**Dữ liệu vào:** Một dòng: n (1 <= n <= 10).",
            "**Dữ liệu ra:** Một số nguyên — số cách đặt.",
            "",
            "**Ví dụ:** `4` -> `2`.",
        ),
        [
            ("sample", "Hai lời giải phản chiếu kinh điển."),
            ("one", "Một hậu luôn an toàn."),
            ("two", "Không tồn tại cách đặt cho n = 2 — lời giải không bao giờ trả 0 là sai."),
            ("six", "Con số đã biết cho n = 6."),
        ],
    ),
    "hsg-p14-dup-perm": vi_challenge(
        "Hoán vị phân biệt",
        T(
            "**Đề bài:** Đếm số hoán vị phân biệt của một multiset ký tự cho trước",
            "(phần trùng gộp lại). In số lượng.",
            "",
            "**Dữ liệu vào:** Một dòng: s (1 <= |s| <= 10, chữ thường).",
            "**Dữ liệu ra:** Một số nguyên — số cách sắp xếp phân biệt.",
            "",
            "**Ví dụ:** `aab` -> `3` (aab, aba, baa).",
        ),
        [
            ("sample", "3!/2! = 3 xâu phân biệt."),
            ("all same", "Mọi thứ gộp về một."),
            ("all distinct", "Đầy đủ 3!."),
            ("two pairs", "4!/(2!*2!) = 6."),
        ],
    ),
    "hsg-p14-strings": vi_challenge(
        "Sinh xâu nhị phân",
        T(
            "**Đề bài:** Sinh mọi xâu nhị phân độ dài n theo **thứ tự từ điển**",
            "(0 trước 1), mỗi xâu một dòng. n đủ nhỏ để liệt kê toàn bộ.",
            "",
            "**Dữ liệu vào:** Một dòng: n (1 <= n <= 12).",
            "**Dữ liệu ra:** 2^n dòng, mỗi dòng n ký tự.",
            "",
            "**Ví dụ:** `2` -> `00` / `01` / `10` / `11`.",
        ),
        [
            ("sample", "Bốn xâu theo thứ tự từ điển."),
            ("single", "Hai dòng."),
            ("three", "Tám dòng, thứ tự từ điển."),
            ("max n", "Dòng đầu của 4096 — kỷ luật kích thước output rất quan trọng."),
        ],
    ),
    "hsg-p14-rooks": vi_challenge(
        "Xe hòa bình",
        T(
            "**Đề bài:** Đếm số cách đặt k quân xe trên bàn n x n sao cho không quân nào",
            "tấn công quân nào (xe tấn công theo hàng và cột).",
            "",
            "**Dữ liệu vào:** Một dòng: n k (1 <= k <= n <= 8).",
            "**Dữ liệu ra:** Một số nguyên — số cách đặt.",
            "",
            "**Ví dụ:** `2 2` -> `2` (đường chéo chính hoặc phụ).",
        ),
        [
            ("sample", "Hai đường chéo là cách đặt đầy đủ duy nhất."),
            ("one rook", "Bất kỳ ô nào trong 9 ô."),
            ("full board", "3! phép gán hàng->cột."),
            ("zero rooks", "Cách đặt rỗng tính là một."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p14-backtrack",
    "Backtracking Problem Set",
    "Permutation counting, N-queens, multiset arrangements, binary strings, and rook placements.",
    "Bài tập quay lui",
    "Đếm hoán vị, N-queens, sắp xếp multiset, xâu nhị phân, và đặt quân xe.",
    "hsg-m14-prune",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p14-perm-count",
            CPP_STD + cpp("""    int n; in >> n;
    // backtrack over permutations of 1..n, count first-odd ones
    int perm[11]; bool used[11] = {};
    long long cnt = 0;
    // n <= 10 -> 10! = 3628800 leaves: plain enumeration is fine
    for (int start = 1; start <= n; start += 2) {
        // fix an odd first element, count arrangements of the rest
        used[start] = true; perm[0] = start;
        long long rest = 1;
        for (int i = 2; i <= n - 1; ++i) rest *= i;  // (n-1)!
        cnt += rest;
        used[start] = false;
    }
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    int perm[11]; bool used[11] = {};
    long long cnt = 0;
    // near-miss: starts the loop at 2 — first element 1 is forgotten
    for (int start = 2; start <= n; start += 2) {
        used[start] = true; perm[0] = start;
        long long rest = 1;
        for (int i = 2; i <= n - 1; ++i) rest *= i;
        cnt += rest;
        used[start] = false;
    }
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p14-queens",
            CPP_STD + cpp("""    int n; in >> n;
    // three boolean families: columns, /-diagonals, \\-diagonals
    bool col[10] = {}, d1[20] = {}, d2[20] = {};
    long long cnt = 0;
    // recursive lambda via std::function-free trick: explicit stack is
    // overkill; use a plain recursive helper written as a local struct
    struct Solver {
        int n; long long cnt = 0;
        bool col[10] = {}, d1[20] = {}, d2[20] = {};
        void go(int r) {
            if (r == n) { ++cnt; return; }
            for (int c = 0; c < n; ++c) {
                if (col[c] || d1[r + c] || d2[r - c + n]) continue;
                col[c] = d1[r + c] = d2[r - c + n] = true;
                go(r + 1);
                col[c] = d1[r + c] = d2[r - c + n] = false;
            }
        }
    } solver{n};
    solver.go(0);
    out << solver.cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    struct Solver {
        int n; long long cnt = 0;
        bool col[10] = {}, d1[20] = {}, d2[20] = {};
        void go(int r) {
            if (r == n) { ++cnt; return; }
            for (int c = 0; c < n; ++c) {
                // near-miss: forgets the second diagonal family —
                // anti-diagonal attacks go undetected
                if (col[c] || d1[r + c]) continue;
                col[c] = d1[r + c] = d2[r - c + n] = true;
                go(r + 1);
                col[c] = d1[r + c] = d2[r - c + n] = false;
            }
        }
    } solver{n};
    solver.go(0);
    out << solver.cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p14-dup-perm",
            CPP_STD + cpp("""    string s; in >> s;
    sort(s.begin(), s.end());
    // count = |s|! / (product of factorials of letter counts)
    long long fact[11]; fact[0] = 1;
    for (int i = 1; i <= 10; ++i) fact[i] = fact[i-1] * i;
    int cnt[26] = {};
    for (char c : s) ++cnt[c - 'a'];
    long long ans = fact[s.size()];
    for (int i = 0; i < 26; ++i) ans /= fact[cnt[i]];
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    sort(s.begin(), s.end());
    long long fact[11]; fact[0] = 1;
    for (int i = 1; i <= 10; ++i) fact[i] = fact[i-1] * i;
    int cnt[26] = {};
    for (char c : s) ++cnt[c - 'a'];
    long long ans = fact[s.size()];
    // near-miss: divides only by 2! regardless of letter counts —
    // "aab" still works (one letter repeats), "aabb" reports 12 not 6
    ans /= 2;
    out << ans << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p14-strings",
            CPP_STD + cpp("""    int n; in >> n;
    // lexicographic order == counting in binary from 0 to 2^n - 1
    int total = 1 << n;
    for (int mask = 0; mask < total; ++mask) {
        for (int b = n - 1; b >= 0; --b) out << ((mask >> b & 1) ? '1' : '0');
        out << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    int total = 1 << n;
    for (int mask = 0; mask < total; ++mask) {
        // near-miss: prints bits low-to-high — the string is reversed
        for (int b = 0; b < n; ++b) out << ((mask >> b & 1) ? '1' : '0');
        out << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsg-p14-rooks",
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    // count ways to choose k rows and k columns and match them: C(n,k)^2 * k!
    long long fact[9]; fact[0] = 1;
    for (int i = 1; i <= 8; ++i) fact[i] = fact[i-1] * i;
    // C(n, k) for tiny n
    long long cnk = fact[n] / (fact[k] * fact[n - k]);
    out << cnk * cnk * fact[k] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    long long fact[9]; fact[0] = 1;
    for (int i = 1; i <= 8; ++i) fact[i] = fact[i-1] * i;
    long long cnk = fact[n] / (fact[k] * fact[n - k]);
    // near-miss: forgets the k! matchings between chosen rows and columns
    out << cnk * cnk << "{{NL}}";
""") + END,
        ),
    ],
)

CH14 = challenge(
    "hsg-cp-m14-paths",
    "Grid Paths",
    T(
        "**Description:** Count the paths from the top-left cell (1,1) to the bottom-right",
        "cell (n,m) of a grid, moving only right or down. Some cells are blocked ('#');",
        "paths may not pass through them. Count modulo 10^9 + 7.",
        "",
        "**Input:** Line 1: n m (1 <= n, m <= 8). Next n lines: m characters each",
        "('.' or '#').",
        "**Output:** One integer — the number of valid paths mod 10^9 + 7.",
        "",
        "**Example:** `2 2` / `..` / `#.` -> `1` (only right-then-down).",
    ),
    [
        contest_test("sample", T("2 2", "..", "#."), T("1"),
                     "The blocked cell kills the down-then-right path."),
        contest_test("open grid", T("2 2", "..", ".."), T("2"),
                     "Right-down and down-right."),
        contest_test("start blocked", T("1 1", "#"), T("0"),
                     "No path exists if the start itself is blocked."),
        contest_test("single open", T("1 1", "."), T("1"),
                     "Standing still is the one path."),
        contest_test("wall", T("3 3", "...", "###", "..."), T("0"),
                     "The full wall disconnects the two corners."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP14 = vi_challenge(
    "Đường đi trên lưới",
    T(
        "**Đề bài:** Đếm các đường đi từ ô trên-trái (1,1) tới ô dưới-phải (n,m) của lưới,",
        "chỉ đi phải hoặc xuống. Một số ô bị chặn ('#'); đường đi không được xuyên qua chúng.",
        "Đếm theo modulo 10^9 + 7.",
        "",
        "**Dữ liệu vào:** Dòng 1: n m (1 <= n, m <= 8). n dòng tiếp: mỗi dòng m ký tự",
        "('.' hoặc '#').",
        "**Dữ liệu ra:** Một số nguyên — số đường đi hợp lệ mod 10^9 + 7.",
        "",
        "**Ví dụ:** `2 2` / `..` / `#.` -> `1` (chỉ phải-rồi-xuống).",
    ),
    [
        ("sample", "Ô bị chặn tiêu diệt đường xuống-rồi-phải."),
        ("open grid", "Phải-xuống và xuống-phải."),
        ("start blocked", "Không có đường nào nếu chính ô xuất phát bị chặn."),
        ("single open", "Đứng yên chính là một đường."),
        ("wall", "Bức tường đầy hàng cách ly hai góc."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m14",
    "Checkpoint — Backtracking",
    "Pass the graded problem to finish the backtracking module.",
    15,
    """**Checkpoint — quay lui.** Pass the graded challenge below. A
walking backtracker (enumerate every right/down sequence, stop at '#')
is the intended beginner tool for n, m <= 8 — the tree has at most a
few thousand paths. The graded near-misses: forgetting that a blocked
**start** means zero paths, and letting the walk step outside the grid.
Both are base-condition bugs, not math bugs.

**Điểm kiểm tra — quay lui.** Pass bài chấm bên dưới. Bộ quay lui từng
bước (liệt kê mọi dãy phải/xuống, dừng tại '#') là công cụ người mới
được định sẵn cho n, m <= 8 — cây có tối đa vài nghìn đường. Các
near-miss bị chấm: quên rằng ô xuất phát bị chặn nghĩa là không đường
nào, và để bước đi lọt ra ngoài lưới. Cả hai là bug trường hợp cơ sở,
không phải bug toán.
""",
    "Checkpoint — Backtracking",
    "Pass the graded problem to finish the backtracking module.",
    """**Điểm kiểm tra — quay lui.** Pass bài chấm bên dưới. Bộ quay lui từng
bước (liệt kê mọi dãy phải/xuống, dừng tại '#') là công cụ người mới
được định sẵn cho n, m <= 8 — cây có tối đa vài nghìn đường. Các
near-miss bị chấm: quên rằng ô xuất phát bị chặn nghĩa là không đường
nào, và để bước đi lọt ra ngoài lưới. Cả hai là bug trường hợp cơ sở,
không phải bug toán.
""",
    CH14,
    VI_CP14,
    solution=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    long long cnt = 0;
    // walk every right/down path
    struct W { int n, m; vector<string>* g; long long cnt = 0;
        void go(int r, int c) {
            if ((*g)[r][c] == '#') return;
            if (r == n - 1 && c == m - 1) { ++cnt; return; }
            if (r + 1 < n) go(r + 1, c);
            if (c + 1 < m) go(r, c + 1);
        }
    } w{n, m, &g};
    w.go(0, 0);
    out << w.cnt % 1000000007 << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<string> g(n);
    for (auto& row : g) in >> row;
    long long cnt = 0;
    struct W { int n, m; vector<string>* g; long long cnt = 0;
        void go(int r, int c) {
            if (r == n - 1 && c == m - 1) { ++cnt; return; }
            if (r + 1 < n) go(r + 1, c);
            if (c + 1 < m) go(r, c + 1);
        }
    } w{n, m, &g};
    w.go(0, 0);
    out << w.cnt % 1000000007 << "{{NL}}";
""") + END,
)

print("M14 done")
