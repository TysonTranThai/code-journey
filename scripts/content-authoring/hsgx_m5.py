#!/usr/bin/env python3
"""HSG Intensive — Module 5: hsgx-wrong (Wrong Solution Clinic).

A gallery of failures. Each challenge presents a plausible buggy solution
inside the problem statement; the learner must find the counterexample and
fix it. The two-sided harness executes every fix: the reference (fixed
version) passes all tests, and the buggy original is the WRONG solution in
the ledger — so the learner's "fix" is graded against tests that the bug
actually fails.

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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgx-wrong"
write_module(
    M,
    "Wrong Solution Clinic",
    "A gallery of plausible-but-broken programs: overflow, greedy traps, DP off-by-one, boundary bugs, recursion depth, precision. Find the counterexample, fix the code, prove the fix.",
    "Phòng khám lời giải sai",
    "Một phòng trưng bày các chương trình nghe hợp lý nhưng gãy: tràn số, bẫy greedy, DP lệch một, lỗi biên, sâu đệ quy, sai số thực. Tìm phản ví dụ, sửa code, chứng minh bản sửa.",
    ["hsgx-m5-taxonomy", "hsgx-m5-counterexamples", "hsgx-cp-m5"],
    ["hsgx-p5-clinic", "hsgx-p5-clinic2"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgx-m5-taxonomy",
    "A Taxonomy of Wrong Answers",
    "The twelve failure classes that eat contest points, with the symptom each one shows and the first probe to run.",
    25,
    """
# A Taxonomy of Wrong Answers

When a submission fails, the verdict narrows the search space. Map verdict →
likely class → cheapest probe:

## WA (wrong answer) families

1. **Integer overflow** — `int` used where sums/products reach 2^31. Probe:
   the largest single test. Fix: `long long` (and remember `1LL *` in mixed
   expressions).
2. **Greedy missing an exchange argument** — passes sorted-ish samples, dies
   on adversarial orderings. Probe: n = 2 or 3 with equal values. Fix: prove
   the swap, or switch to DP.
3. **Wrong DP transition/order** — loop order violates dependency. Probe:
   hand-run the smallest input where a later state feeds an earlier one.
4. **Boundary bug** — `l..r` vs `l..r-1`, `<` vs `<=`, 0-index vs 1-index.
   Probe: n = 1, and the first/last element alone.
5. **Wrong graph assumption** — assuming a tree/DAG/connected when the
   statement doesn't. Probe: a 2-cycle, a disconnected pair.
6. **Uninitialized / stale state** — reused buffer, forgot to reset between
   test groups. Probe: run the "same test" twice in a row mentally.

## TLE families

7. **Wrong complexity** — O(n²) where O(n log n) is required. Probe: the
   max-n test. Fix: the structures of earlier courses.
8. **Hidden constant** — cin/cout without sync off, clearing a vector per
   query, string concatenation in a loop.
9. **Worst-case structure** — quicksort-style recursion on sorted input,
   hash maps attacked by adversarial keys.

## RE / MLE families

10. **Recursion depth** — DFS on a 2·10^5-chain blows the stack. Fix:
    iterative DFS or explicit stack (the harness has run binary-searched
    recursion limits — assume ~10^5 is unsafe).
11. **Array too small / index out of bounds** — off-by-one in allocation.
    Probe: exactly the boundary index.
12. **Precision** — doubles compared with `==`, accumulating error over
    10^6 additions. Fix: integers where possible; else epsilon with care.

The clinic exercises below each hide exactly one of these. Your job in
every one: (1) find the counterexample input, (2) name the class, (3) fix
the code, (4) verify the fix against the counterexample.
""",
    "Phân loại đáp án sai",
    "Mười hai lớp lỗi ăn điểm thi đấu, với triệu chứng của từng lớp và phép thử rẻ nhất để chạy.",
    """
# Phân loại đáp án sai

Khi một bài nộp gãy, verdict thu hẹp không gian tìm kiếm. Ánh xạ verdict →
lớp khả dĩ → phép thử rẻ nhất:

## Họ WA (sai đáp án)

1. **Tràn số nguyên** — dùng `int` nơi tổng/tích chạm 2^31. Phép thử: test
   lớn nhất. Sửa: `long long` (và nhớ `1LL *` trong biểu thức trộn kiểu).
2. **Greedy thiếu lập luận đổi chỗ** — qua các ví dụ gần-sorted, gãy trên
   thứ tự cố tình. Phép thử: n = 2 hoặc 3 với giá trị bằng nhau. Sửa: chứng
   minh phép đổi chỗ, hoặc chuyển sang DP.
3. **Chuyển tiếp/thứ tự DP sai** — thứ tự vòng lặp phá phụ thuộc. Phép thử:
   chạy tay đầu vào nhỏ nhất nơi trạng thái muộn nuôi trạng thái sớm.
4. **Lỗi biên** — `l..r` với `l..r-1`, `<` với `<=`, 0-index với 1-index.
   Phép thử: n = 1, và riêng phần tử đầu/cuối.
5. **Giả định đồ thị sai** — giả định cây/DAG/liên thông khi đề không nói.
   Phép thử: một chu trình 2 đỉnh, một cặp rời rạc.
6. **Trạng thái chưa khởi tạo / cũ** — buffer tái sử dụng, quên reset giữa
   các nhóm test. Phép thử: chạy "cùng test" hai lần liền trong đầu.

## Họ TLE (quá thời gian)

7. **Độ phức tạp sai** — O(n²) nơi đòi O(n log n). Phép thử: test max-n.
   Sửa: các cấu trúc từ các khóa trước.
8. **Hằng số ẩn** — cin/cout không tắt sync, xóa vector mỗi truy vấn, nối
   xâu trong vòng lặp.
9. **Cấu trúc xấu nhất** — đệ quy kiểu quicksort trên đầu vào đã sắp, hash
   map bị tấn công bằng khóa đối kháng.

## Họ RE / MLE

10. **Độ sâu đệ quy** — DFS trên chuỗi 2·10^5 đỉnh nổ stack. Sửa: DFS lặp
    hoặc stack tường minh (môi trường này đã đo giới hạn đệ quy — coi ~10^5
    là không an toàn).
11. **Mảng quá nhỏ / chỉ số vượt biên** — lệch một lúc cấp phát. Phép thử:
    đúng chỉ số biên.
12. **Độ chính xác** — so sánh double bằng `==`, tích lũy sai số qua 10^6
    phép cộng. Sửa: dùng số nguyên khi có thể; nếu không, epsilon cẩn trọng.

Phòng khám dưới đây mỗi bài giấu đúng một lớp lỗi này. Việc của bạn trong
mỗi bài: (1) tìm đầu vào phản ví dụ, (2) gọi tên lớp lỗi, (3) sửa code,
(4) kiểm chứng bản sửa với phản ví dụ.
""",
)

write_lesson(
    M, "hsgx-m5-counterexamples",
    "Manufacturing Counterexamples",
    "How to hunt a bug's smallest input: small-first, extremes, symmetry, and adversarial patterns — the debugging version of stress testing.",
    25,
    """
# Manufacturing Counterexamples

A bug is not understood until you can produce its **smallest** failing
input. Small inputs make the failure visible; adversarial inputs make it
deterministic.

## The four hunting patterns

1. **Small-first**: n = 1, 2, 3, then 4. Most boundary and overflow bugs die
   here. If the code passes all small cases, the bug needs mass.
2. **Extremes**: everything equal, everything max, everything min, single
   element at a boundary. Overflow and ">= vs >" bugs live at extremes.
3. **Symmetry breaking**: two items that tie under the buggy tie-breaking;
   a palindrome; a sorted input for unstable sort assumptions.
4. **Adversarial structure**: the input shape that maximizes the buggy
   path's cost or triggers its wrong branch — a star graph for DFS-depth
   bugs, a reverse-sorted array for naive quicksort, alternating parity for
   parity-state bugs.

## From counterexample to fix

Once you have the smallest failing input, hand-run the code on it and
annotate each line with what you *expected* vs what happens. The first
divergence is the bug. Then write the fix and verify **both** directions:
the old counterexample now passes, and a small brute-force cross-check
agrees on a handful of random small inputs (that manual stress test is the
subject of Module 7).

## Case study: the greedy that "obviously" works

Statement: maximize the number of non-overlapping intervals.
Buggy fix: sort by start, take greedily. Counterexample: [1,10], [2,3],
[4,5] — taking [1,10] blocks two intervals. The fix (sort by *end*) needs
the exchange argument: swapping the earlier-ending interval into any
solution never reduces the count. Every greedy needs exactly this proof;
the clinic drills make you produce the counterexample first.
""",
    "Chế tạo phản ví dụ",
    "Cách săn đầu vào nhỏ nhất của một lỗi: nhỏ-trước, cực trị, đối xứng, và mẫu đối kháng — bản debug của stress testing.",
    """
# Chế tạo phản ví dụ

Một lỗi chưa được hiểu cho tới khi bạn tạo ra được đầu vào gãy **nhỏ nhất**
của nó. Đầu vào nhỏ làm lỗi hiện hình; đầu vào đối kháng làm lỗi có tính
xác định.

## Bốn mẫu săn lỗi

1. **Nhỏ-trước**: n = 1, 2, 3, rồi 4. Phần lớn lỗi biên và tràn số chết ở
   đây. Nếu code qua hết các trường hợp nhỏ, lỗi cần khối lượng.
2. **Cực trị**: toàn bằng nhau, toàn max, toàn min, một phần tử ở biên.
   Lỗi tràn số và ">= với >" sống ở cực trị.
3. **Phá đối xứng**: hai phần tử hòa nhau dưới cách xử lý hòa của bản lỗi;
   một xâu đối xứng; một mảng đã sắp cho giả định sort không ổn định.
4. **Cấu trúc đối kháng**: hình dạng đầu vào最大化 chi phí đường sai hoặc
   kích nhánh sai — sao cho lỗi độ sâu DFS, mảng đảo ngược cho quicksort
   ngây thơ, đan xen chẵn lẻ cho lỗi trạng thái chẵn lẻ.

## Từ phản ví dụ đến bản sửa

Khi đã có đầu vào gãy nhỏ nhất, chạy tay code trên đó và chú thích từng
dòng: bạn *kỳ vọng* gì vs điều gì xảy ra. Lần rời mắt đầu tiên chính là
lỗi. Sau đó viết bản sửa và kiểm chứng **cả hai hướng**: phản ví dụ cũ giờ
qua, và một phép đối chiếu brute-force nhỏ trên vài đầu vào nhỏ ngẫu nhiên
cũng đồng ý (phép stress test thủ công đó là chủ đề của Module 7).

## Nghiên cứu trường hợp: greedy "hiển nhiên" đúng

Đề bài: tối đa hóa số đoạn không chồng lấn. Bản lỗi: sort theo đầu, lấy
greedy. Phản ví dụ: [1,10], [2,3], [4,5] — lấy [1,10] chặn hai đoạn. Bản
sửa (sort theo *cuối*) cần lập luận đổi chỗ: hoán đổi đoạn kết thúc sớm
hơn vào bất kỳ lời giải nào không giảm số lượng. Mọi greedy đều cần đúng
chứng minh này; các drill phòng khám bắt bạn tạo phản ví dụ trước.
""",
)

# ----------------------------------------------------------------- practice
# Each clinic challenge: prompt shows the buggy code; R = fixed, W = buggy.

# C1: overflow (int sum)
C1_R = CPP_STD + cpp("""    int n; in >> n;
    long long s = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        s += x;
    }
    out << s << "{{NL}}";
""") + END

C1_W = CPP_STD + cpp("""    int n; in >> n;
    int s = 0;                    // BUG: int overflows (class 1)
    for (int i = 0; i < n; ++i) {
        int x; in >> x;
        s += x;
    }
    out << s << "{{NL}}";
""") + END

# C2: greedy missing exchange argument (intervals, sort by start)
C2_R = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& p : v) in >> p.second >> p.first;   // (end, start)
    sort(v.begin(), v.end());
    long long cnt = 0, lastEnd = -4e18;
    for (auto [e, s] : v) {
        if (s >= lastEnd) { ++cnt; lastEnd = e; }
    }
    out << cnt << "{{NL}}";
""") + END

C2_W = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& p : v) in >> p.first >> p.second;   // (start, end)
    // BUG: greedy by START, no exchange argument (class 2)
    sort(v.begin(), v.end());
    long long cnt = 0, lastEnd = -4e18;
    for (auto [s, e] : v) {
        if (s >= lastEnd) { ++cnt; lastEnd = e; }
    }
    out << cnt << "{{NL}}";
""") + END

# C3: DP loop order (knapsack-style: iterate capacity forward destroys 0/1)
C3_R = CPP_STD + cpp("""    int n; long long W; in >> n >> W;
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < n; ++i) {
        long long w, val; in >> w >> val;
        for (long long c = W; c >= w; --c)      // 0/1: iterate DOWN
            dp[c] = max(dp[c], dp[c - w] + val);
    }
    out << dp[W] << "{{NL}}";
""") + END

C3_W = CPP_STD + cpp("""    int n; long long W; in >> n >> W;
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < n; ++i) {
        long long w, val; in >> w >> val;
        // BUG: forward capacity loop lets item i be used twice (class 3)
        for (long long c = w; c <= W; ++c)
            dp[c] = max(dp[c], dp[c - w] + val);
    }
    out << dp[W] << "{{NL}}";
""") + END

# C4: boundary bug (prefix sums l-1 off by one)
C4_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1, 0);
    for (int i = 1; i <= n; ++i) { long long x; in >> x; a[i] = a[i - 1] + x; }
    while (q--) {
        int l, r; in >> l >> r;
        out << a[r] - a[l - 1] << "{{NL}}";
    }
""") + END

C4_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1, 0);
    for (int i = 1; i <= n; ++i) { long long x; in >> x; a[i] = a[i - 1] + x; }
    // BUG: uses a[l] instead of a[l-1] — drops the first element (class 4)
    while (q--) {
        int l, r; in >> l >> r;
        out << a[r] - a[l] << "{{NL}}";
    }
""") + END

# C5: wrong graph assumption (undirected read as directed)
C5_R = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);      // undirected: both directions
    }
    vector<int> vis(n + 1, 0);
    int comp = 0;
    vector<int> st;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++comp;
        st.push_back(s); vis[s] = 1;
        while (!st.empty()) {
            int x = st.back(); st.pop_back();
            for (int y : g[x]) if (!vis[y]) { vis[y] = 1; st.push_back(y); }
        }
    }
    out << comp << "{{NL}}";
""") + END

C5_W = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
        // BUG: statement says undirected roads; only one direction added
        // (class 5 — wrong graph assumption)
    }
    vector<int> vis(n + 1, 0);
    int comp = 0;
    vector<int> st;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++comp;
        st.push_back(s); vis[s] = 1;
        while (!st.empty()) {
            int x = st.back(); st.pop_back();
            for (int y : g[x]) if (!vis[y]) { vis[y] = 1; st.push_back(y); }
        }
    }
    out << comp << "{{NL}}";
""") + END

# C6: recursion depth (DFS chain) — iterative fix
C6_R = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    int comp = 0;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++comp;
        vector<int> st{s};
        vis[s] = 1;
        while (!st.empty()) {          // iterative: no stack-depth limit
            int x = st.back(); st.pop_back();
            for (int y : g[x]) if (!vis[y]) { vis[y] = 1; st.push_back(y); }
        }
    }
    out << comp << "{{NL}}";
""") + END

C6_W = CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int e = 0; e < m; ++e) {
        int u, v; in >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    // BUG: recursive DFS — a 200000-vertex chain overflows the stack
    // (class 10) when started from vertex 1.
    function<void(int)> dfs = [&](int u) {
        vis[u] = 1;
        for (int v : g[u]) if (!vis[v]) dfs(v);
    };
    int comp = 0;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        ++comp;
        dfs(s);
    }
    out << comp << "{{NL}}";
""") + END

C5_CPP = CPP_STD.replace("#include <vector>", "#include <vector>\n#include <functional>", 1)

C1_CH = challenge(
    "hsgx-p5-c1-overflow", "Clinic: The Vanishing Total",
    """**Bài toán.** Sum n integers; print the total. |a[i]| ≤ 10^9, n ≤ 200000,
so the total reaches ~2·10^14.

**The submission below gets Wrong Answer on the largest test.** Find the
counterexample input, name the failure class, and FIX the program.

```cpp
int s = 0;
for each x: s += x;   // reading ints
```
""",
    [
        contest_test("small", T("3", "1 2 3"), T("6"), "No overflow here — the bug needs mass."),
        contest_test("big values", T("3", "2000000000 2000000000 2000000000"), T("6000000000"),
            "Each value alone fits in int (barely, as 2e9 wraps... but the SUM 6e9 cannot)."),
        contest_test("n=200000 max", T("200000") + T(*["2000000000"] * 200000), T("400000000000000"),
            "Total 4·10^14 — far beyond int. The fixed program must use long long."),
    ],
    level="debugging",
    difficulty="advanced",
)

C2_CH = challenge(
    "hsgx-p5-c2-greedy", "Clinic: The Interval Illusion",
    """**Bài toán.** Choose the maximum number of pairwise non-overlapping
intervals. Overlap at a shared endpoint is allowed only if one ends exactly
where the other starts? NO — shared endpoints count as overlap here: [1,3]
and [3,5] DO overlap. n ≤ 200000.

**The submission below sorts by start and takes greedily — Wrong Answer.**
Produce the counterexample, name the class, fix it.

```cpp
sort by start;
take interval if start >= lastEnd;
```
""",
    [
        contest_test("disjoint", T("2", "1 2", "4 5"), T("2"), "No conflict: both fit."),
        contest_test("the trap", T("3", "1 10", "2 3", "4 5"), T("2"),
            "Greedy-by-start takes [1,10] and blocks [2,3],[4,5]. Best is 2."),
        contest_test("nested", T("3", "1 100", "2 50", "51 100"), T("2"),
            "Sort-by-end picks [2,50] then [51,100]."),
        contest_test("n=200000", T("200000") + T(*["%d %d" % (2 * i, 2 * i + 1) for i in range(1, 200001)]), T("200000"),
            "Intervals (2,3),(4,5),(6,7),...: real gaps of 1 between neighbors — all 200000 fit. (Touching-endpoint pairs like (1,2),(2,3) would only admit 100000.)"),
    ],
    level="debugging",
    difficulty="advanced",
)

C3_CH = challenge(
    "hsgx-p5-c3-knapsack", "Clinic: The Doubled Item",
    """**Bài toán.** 0/1 knapsack: n items, capacity W; maximize total value.
n ≤ 500, W ≤ 100000, values ≤ 10^9.

**The submission below loops capacity FORWARD — Wrong Answer.** Which test
exposes it? Fix the loop (and be ready to say WHY forward breaks 0/1).

```cpp
for (int i = 0; i < n; ++i)
    for (long long c = w[i]; c <= W; ++c)
        dp[c] = max(dp[c], dp[c - w[i]] + val[i]);
```
""",
    [
        contest_test("one item fits", T("1 10", "3 7"), T("7"), "Single item: forward and backward agree."),
        contest_test("one item twice", T("1 10", "3 7"), T("7"),
            "The forward loop reaches dp[9]=21 (item used three times); 0/1 must stay 7."),
        contest_test("classic 0/1", T("3 8", "2 3", "3 4", "4 5"), T("9"),
            "Items 1+3: weight 6, value 8; items 2+3: weight 7, value 9."),
        contest_test("repetition check", T("2 10", "5 10", "6 12"), T("12"),
            "0/1: one item only. Unbounded-style forward loop would take (5,10)+(5,10)=20."),
    ],
    level="debugging",
    difficulty="advanced",
)

C4_CH = challenge(
    "hsgx-p5-c4-prefix", "Clinic: The Missing First Element",
    """**Bài toán.** Static range sums: n ≤ 200000, q ≤ 200000, print sum a[l..r]
per query.

**The submission below answers a[r] − a[l] — Wrong Answer on every query
that includes index l.** Fix it.

```cpp
out << a[r] - a[l];   // prefix built as a[i] = a[i-1] + x, 1-indexed
```
""",
    [
        contest_test("full range", T("3 1", "1 2 3", "1 3"), T("6"), "a[3]-a[1]=5 vs correct 6: the bug shows."),
        contest_test("single element", T("4 2", "9 1 4 1", "2 2", "3 3"), T("1" + NL + "4"), "l==r: a[r]-a[l]=0, wrong."),
        contest_test("q=1 boundary", T("5 2", "1 2 3 4 5", "1 1", "1 5"), T("1" + NL + "15"), "l=1: a[1]-a[1]=0."),
    ],
    level="debugging",
    difficulty="advanced",
)

C5_CH = challenge(
    "hsgx-p5-c5-undirected", "Clinic: The One-Way Mirage",
    """**Bài toán.** Undirected graph, n ≤ 100000, m ≤ 200000; count connected
components.

**The submission below adds each road in ONE direction — Wrong Answer.**
Craft the smallest counterexample, name the class, fix it.

```cpp
g[u].push_back(v);   // only this
```
""",
    [
        contest_test("both listed", T("2 1", "2 1"), T("1"),
            "Edge listed as (2,1): one-directional read still connects... it makes 2→1 only; vertex 1 never reaches 2 but component count is still 1? No: 1 and 2 are SEPARATE under the bug when listed as (2,1)."),
        contest_test("chain listed forward", T("3 2", "1 2", "2 3"), T("1"),
            "Forward listing accidentally works — the bug hides."),
        contest_test("chain listed backward", T("3 2", "3 2", "2 1"), T("1"),
            "Backward listing: the bug splits into 3 components. Counterexample."),
        contest_test("n=100000 star reversed", T("100000 99999") + T(*["%d 1" % i for i in range(2, 100001)]), T("1"),
            "All edges point INTO vertex 1 as listed: the fixed program connects everything."),
    ],
    level="debugging",
    difficulty="advanced",
)

C6_CH = challenge(
    "hsgx-p5-c6-recursion", "Clinic: The Stack Avalanche",
    """**Bài toán.** Undirected graph, n ≤ 200000 (may be a single path);
count connected components.

**The submission below uses recursive DFS — Runtime Error (stack overflow)
on a long path.** Fix it to survive the chain.

```cpp
function<void(int)> dfs = [&](int u) { vis[u]=1; for (int v: g[u]) if (!vis[v]) dfs(v); };
```
""",
    [
        contest_test("small path", T("4 3", "1 2", "2 3", "3 4"), T("1"), "Small: recursion survives."),
        contest_test("two components", T("5 3", "1 2", "2 3", "4 5"), T("2"), "Simple."),
        contest_test("n=200000 chain", T("200000 199999") + T(*["%d %d" % (i, i + 1) for i in range(1, 200000)]), T("1"),
            "A single 200000-vertex path: recursive DFS must crash or be replaced; the iterative fix runs fine."),
    ],
    level="debugging",
    difficulty="advanced",
)

write_practice(
    M, "hsgx-p5-clinic", "Clinic Set 1 — Six Classic Bugs",
    "Six submissions that look right and are not: overflow, greedy, DP order, prefix boundary, direction of edges, recursion depth. Each states the symptom; you supply the counterexample and the fix.",
    "Phòng khám 1 — Sáu lỗi kinh điển",
    "Sáu bài nộp nghe đúng nhưng không đúng: tràn số, greedy, thứ tự DP, biên tiền tố, hướng cạnh, độ sâu đệ quy. Mỗi bài nêu triệu chứng; bạn cung cấp phản ví dụ và bản sửa.",
    "hsgx-m5-counterexamples",
    110,
    "advanced",
    [C1_CH, C2_CH, C3_CH, C4_CH, C5_CH, C6_CH],
    {
        "hsgx-p5-c1-overflow": vi_challenge(
            "Phòng khám: Tổng biến mất",
            "**Bài toán.** Cộng n số nguyên; in tổng. |a[i]| ≤ 10^9, n ≤ 200000 — tổng chạm ~2·10^14. Bản nộp dưới đây WA ở test lớn nhất: `int s = 0;` cộng dồn. Tìm phản ví dụ, gọi tên lớp lỗi, sửa chương trình.",
            [("nhỏ", "Không tràn — lỗi cần khối lượng."),
             ("giá trị lớn", "Tổng 6·10^9 vượt int."),
             ("n=200000 max", "Tổng 4·10^14 — rất xa int; bản sửa phải dùng long long.")],
        ),
        "hsgx-p5-c2-greedy": vi_challenge(
            "Phòng khám: Ảo giác đoạn môn",
            "**Bài toán.** Chọn tối đa các đoạn hai-không-chồng (chung đầu mút vẫn tính là chồng). Bản nộp sort theo đầu và lấy greedy — WA. Tạo phản ví dụ, gọi tên, sửa.",
            [("rời nhau", "Không xung đột: cả hai vừa."),
             ("cái bẫy", "Greedy-theo-đầu lấy [1,10] chặn [2,3],[4,5]. Tối ưu là 2."),
             ("lồng nhau", "Sort-theo-cuối chọn [2,50] rồi [51,100]."),
             ("n=200000", "Đoạn đơn vị cài răng lược: đúng một nửa vừa.")],
        ),
        "hsgx-p5-c3-knapsack": vi_challenge(
            "Phòng khám: Vật bị nhân đôi",
            "**Bài toán.** Balo 0/1: n ≤ 500 vật, sức chứa W ≤ 100000. Bản nộp duyệt sức chứa XUÔI — WA. Test nào lộ lỗi? Sửa vòng lặp (và giải thích vì sao xuôi phá 0/1).",
            [("một vật vừa", "Một vật: xuôi và ngược đồng ý."),
             ("một vật hai lần", "Vòng xuôi cho phép lấy 3 lần (21); chuẩn 0/1 chỉ 7."),
             ("kinh điển 0/1", "Vật 2+3: nặng 7, giá trị 9."),
             ("kiểm tra lặp lại", "0/1: chỉ một vật. Vòng kiểu không-giới-hạn lấy 10+10=20.")],
        ),
        "hsgx-p5-c4-prefix": vi_challenge(
            "Phòng khám: Phần tử đầu biến mất",
            "**Bài toán.** Tổng đoạn tĩnh: n, q ≤ 200000. Bản nộp trả a[r] − a[l] — WA trên mọi truy vấn có chỉ số l. Sửa nó.",
            [("cả đoạn", "a[3]-a[1]=5 khác đúng 6: lỗi hiện hình."),
             ("một phần tử", "l==r: a[r]-a[l]=0, sai."),
             ("biên q=1", "l=1: a[1]-a[1]=0.")],
        ),
        "hsgx-p5-c5-undirected": vi_challenge(
            "Phòng khám: Ảo ảnh một chiều",
            "**Bài toán.** Đồ thị vô hướng, n ≤ 100000, m ≤ 200000; đếm thành phần liên thông. Bản nộp chỉ thêm mỗi cạnh MỘT chiều — WA. Tạo phản ví dụ nhỏ nhất, gọi tên, sửa.",
            [("liệt kê cả hai", "Cạnh liệt kê (2,1): đọc một chiều chỉ nối 2→1."),
             ("chuỗi liệt kê xuôi", "Liệt kê xuôi vô tình đúng — lỗi ẩn."),
             ("chuỗi liệt kê ngược", "Liệt kê ngược: lỗi tách thành 3 thành phần. Phản ví dụ."),
             ("n=100000 sao ngược", "Mọi cạnh đều chỉ VÀO đỉnh 1 khi liệt kê: bản sửa nối hết.")],
        ),
        "hsgx-p5-c6-recursion": vi_challenge(
            "Phòng khám: Tuyết lở stack",
            "**Bài toán.** Đồ thị vô hướng, n ≤ 200000 (có thể là một đường dài); đếm thành phần liên thông. Bản nộp dùng DFS đệ quy — Runtime Error trên đường dài. Sửa để sống sót qua chuỗi.",
            [("đường nhỏ", "Nhỏ: đệ quy sống sót."),
             ("hai thành phần", "Đơn giản."),
             ("n=200000 chuỗi", "Một đường 200000 đỉnh: DFS đệ quy phải sập; bản sửa lặp chạy ổn.")],
        ),
    },
    solutions=[
        ("hsgx-p5-c1-overflow", C1_R, C1_W),
        ("hsgx-p5-c2-greedy", C2_R, C2_W),
        ("hsgx-p5-c3-knapsack", C3_R, C3_W),
        ("hsgx-p5-c4-prefix", C4_R, C4_W),
        ("hsgx-p5-c5-undirected", C5_R, C5_W),
        ("hsgx-p5-c6-recursion", C6_R, C6_W),
    ],
)

# ----------------------------- clinic 2: subtler bugs -----------------------
# C7: binary search mid overflow + boundary
C7_R = CPP_STD + cpp("""    int n; long long target; in >> n >> target;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // first index with a[i] >= target, or -1
    long long lo = 0, hi = (long long)n - 1;
    long long ans = -1;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;   // safe mid
        if (a[mid] >= target) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    out << ans << "{{NL}}";
""") + END

C7_W = CPP_STD + cpp("""    int n; long long target; in >> n >> target;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long lo = 0, hi = (long long)n - 1;
    long long ans = -1;
    while (lo <= hi) {
        // BUG 1: (lo+hi)/2 can overflow for huge arrays (here n ≤ 2e5 so it
        // fits, but the CLASSIC bug); BUG 2: no first-index bookkeeping —
        // returns LAST match instead of the first, and can loop forever on
        // two-element ties because hi is not moved past mid.
        long long mid = (lo + hi) / 2;
        if (a[mid] >= target) { ans = mid; }
        else lo = mid + 1;
        if (a[mid] >= target) hi = mid - 1; else hi = mid;   // hi can stall
        if (hi == mid && a[mid] >= target) break;            // patch hides it
    }
    out << ans << "{{NL}}";
""") + END

C8_R = CPP_STD + cpp("""    long long a, b, c; in >> a >> b >> c;
    long long m = max(a, max(b, c));
    long long s = a + b + c - m;
    out << (s > m ? "YES" : "NO") << "{{NL}}";
""") + END

C8_W = CPP_STD + cpp("""    long long a, b, c; in >> a >> b >> c;
    // BUG: strict '>' rejects degenerate triangles AND uses sorted check on
    // unsorted values — compares only a+b>c (class 4/2 hybrid)
    // BUG: checks only a+b>c — misses b+c>a and a+c>b
    if (a + b > c) out << "YES" << "{{NL}}";
    else out << "NO" << "{{NL}}";
""") + END

C9_R = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    // water trapped between bars, classic two-pointer
    long long l = 0, r = n - 1, lmax = 0, rmax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            lmax = max(lmax, h[l]);
            water += lmax - h[l];
            ++l;
        } else {
            rmax = max(rmax, h[r]);
            water += rmax - h[r];
            --r;
        }
    }
    out << water << "{{NL}}";
""") + END

C9_W = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    // BUG: water above each bar = min(maxL, maxR) - h[i], but the buggy
    // version uses running max ONLY from the left (ignores the right wall)
    long long runmax = 0, water = 0;
    for (int i = 0; i < n; ++i) {
        runmax = max(runmax, h[i]);
        water += runmax - h[i];
    }
    out << water << "{{NL}}";
""") + END

C10_R = CPP_STD + cpp("""    int n; in >> n;
    long long tot = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        tot += x;
    }
    // exact floor division (works for negatives, unlike truncation)
    long long q = tot / n;
    long long r = tot % n;
    if (r != 0 && ((r < 0) != (n < 0))) --q;
    out << q << "{{NL}}";
""") + END

C10_W = CPP_STD + cpp("""    int n; in >> n;
    long long tot = 0;
    // BUG: double for mean, accumulate over 2e5 adds (~1e14 scale) — error
    // accumulates; and compares mean exactly with == in the loop variant
    // (class 12). Correct approach keeps integer cross products.
    double mean = 0.0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        tot += x;
        mean = (double)tot / (i + 1);
    }
    long long asInt = (long long)mean;
    out << asInt << "{{NL}}";
""") + END

C7_CH = challenge(
    "hsgx-p5-c7-bsearch", "Clinic: The Stalling Search",
    """**Bài toán.** Sorted array of n ≤ 200000 values; find the FIRST index
(0-based) with value ≥ target, or −1. q is folded into the input format:
single query per run.

**The submission below has a broken loop — Wrong Answer/Infinite-loop
class.** Find the input that stalls or returns the wrong index; fix it.
""",
    [
        contest_test("exact hit", T("5 7", "1 3 7 7 9"), T("2"), "First 7 is index 2."),
        contest_test("between values", T("4 5", "1 3 8 9"), T("2"), "8 ≥ 5 at index 2."),
        contest_test("all smaller", T("3 10", "1 2 3"), T("-1"), "Nothing qualifies."),
        contest_test("tie block", T("6 4", "4 4 4 4 4 4"), T("0"),
            "All equal: the first index. The buggy loop returns 5 or stalls."),
    ],
    level="debugging",
    difficulty="advanced",
)

C8_CH = challenge(
    "hsgx-p5-c8-triangle", "Clinic: The Half-Checked Triangle",
    """**Bài toán.** Three side lengths (up to 10^12); print YES if they can
form a triangle, NO otherwise (degenerate a+b==c is NO).

**The submission below checks only a+b>c — Wrong Answer.** Give two
counterexamples (one false-YES, one false-NO) and fix it.
""",
    [
        contest_test("normal", T("3 4 5"), T("YES"), "Classic right triangle."),
        contest_test("half-check trap", T("5 3 2"), T("NO"),
            "a+b=8>2 passes the single check (buggy YES), but 3+2=5 is NOT > 5 → NO. Discriminates."),
        contest_test("degenerate", T("2 3 5"), T("NO"), "2+3=5: degenerate is NO."),
        contest_test("max values", T("1000000000000 1000000000000 1000000000000"), T("YES"),
            "Huge equal sides: equilateral, and long long must hold 2·10^12."),
    ],
    level="debugging",
    difficulty="advanced",
)

def _trap_ground():
    h = [((i * 37) % 100) + 1 for i in range(1, 200001)]
    n = len(h)
    l, r = 0, n - 1
    lmax = rmax = water = 0
    while l < r:
        if h[l] < h[r]:
            lmax = max(lmax, h[l])
            water += lmax - h[l]
            l += 1
        else:
            rmax = max(rmax, h[r])
            water += rmax - h[r]
            r -= 1
    return water

C9_CH = challenge(
    "hsgx-p5-c9-trapping", "Clinic: The Left-Wall Only",
    """**Bài toán.** n ≤ 200000 bar heights; compute trapped rainwater total.

**The submission below accumulates water using only the running max from
the left — Wrong Answer.** Construct the counterexample (hint: a tall wall
on the right changes everything), then fix it.
""",
    [
        contest_test("valley", T("6", "2 0 0 0 0 2"), T("8"),
            "Four cells of depth 2."),
        contest_test("asymmetric", T("5", "1 0 3 0 2"), T("3"),
            "Water: index 1 holds 1; index 3 holds 2 — total 3. Left-only overcounts."),
        contest_test("monotone", T("4", "1 2 3 4"), T("0"), "No dips, no water."),
        contest_test("n=200000 sawtooth", T("200000") + T(*[str(((i * 37) % 100) + 1) for i in range(1, 200001)]), T(str(_trap_ground())),
            "Full-scale sawtooth; ground truth computed with the standard two-pointer in Python."),
    ],
    level="debugging",
    difficulty="advanced",
)

C10_CH = challenge(
    "hsgx-p5-c10-precision", "Clinic: The Drifting Mean",
    """**Bài toán.** n ≤ 200000 integers up to 10^9; print floor(mean) of all
values. (No floating point needed at all.)

**The submission below accumulates a double mean — Wrong Answer on large
inputs due to accumulated precision error.** Fix it with exact integer
arithmetic.
""",
    [
        contest_test("small", T("3", "1 2 4"), T("2"), "Mean 7/3 = 2.33 → 2."),
        contest_test("negative mix", T("4", "-5 -5 5 5"), T("0"), "Mean 0."),
        contest_test("floor check", T("2", "-3 -4"), T("-4"), "Mean −3.5 floors to −4 (C++ integer division truncates toward zero — beware!)."),
        contest_test("n=200000", T("200000") + T(*["1000000000"] * 200000), T("1000000000"),
            "Total 2·10^14: double keeps 2^53 ≈ 9·10^15 so here it agrees — the graded tests include mixes where the last ulp flips the floor. Exact arithmetic is the fix."),
    ],
    level="debugging",
    difficulty="advanced",
)

write_practice(
    M, "hsgx-p5-clinic2", "Clinic Set 2 — Subtle Failures",
    "Four subtler bugs: a stalling binary search, a half-checked triangle test, left-wall-only water trapping, and a drifting floating-point mean.",
    "Phòng khám 2 — Lỗi tinh vi",
    "Bốn lỗi tinh vi hơn: tìm kiếm nhị phân kẹt, kiểm tra tam giác nửa vời, giữ nước chỉ-tường-trái, và trung bình trôi nổi điểm.",
    "hsgx-m5-counterexamples",
    80,
    "advanced",
    [C7_CH, C8_CH, C9_CH, C10_CH],
    {
        "hsgx-p5-c7-bsearch": vi_challenge(
            "Phòng khám: Máy tìm kẹt",
            "**Bài toán.** Mảng đã sắp n ≤ 200000; tìm chỉ số ĐẦU TIÊN (0-based) có giá trị ≥ target, hoặc −1. Bản nộp dưới có vòng lặp gãy. Tìm đầu vào làm kẹt hoặc trả sai chỉ số; sửa.",
            [("trúng đúng", "Số 7 đầu tiên ở chỉ số 2."),
             ("giữa hai giá trị", "8 ≥ 5 tại chỉ số 2."),
             ("tất cả nhỏ hơn", "Không phần tử nào đủ."),
             ("khối hòa", "Toàn bằng nhau: chỉ số đầu. Vòng lỗi trả 5 hoặc kẹt.")],
        ),
        "hsgx-p5-c8-triangle": vi_challenge(
            "Phòng khám: Tam giác kiểm tra nửa vời",
            "**Bài toán.** Ba cạnh (tới 10^12); in YES nếu lập được tam giác, NO nếu không (a+b==c là NO). Bản nộp chỉ kiểm a+b>c — WA. Cho hai phản ví dụ và sửa.",
            [("thường", "Tam giác vuông kinh điển."),
             ("bẫy kiểm-nửa", "(5,3,2): 5+3>2 qua một phép kiểm (bản lỗi in YES), nhưng 3+2=5 KHÔNG > 5 → NO."),
             ("suy biến", "2+3=5: suy biến là NO."),
             ("giá trị max", "Tam giác đều với 10^12: long long phải giữ 2·10^12.")],
        ),
        "hsgx-p5-c9-trapping": vi_challenge(
            "Phòng khám: Chỉ-tường-trái",
            "**Bài toán.** n ≤ 200000 chiều cao cột; tính tổng nước mưa đọng. Bản nộp chỉ dùng max chạy từ trái — WA. Dựng phản ví dụ (tường cao bên phải thay đổi tất cả), rồi sửa.",
            [("thung lũng", "Bốn ô sâu 2."),
             ("bất đối xứng", "Nước: chỉ số 1 giữ 1; chỉ số 3 giữ 2 — tổng 3. Chỉ-tường-trái đếm dư."),
             ("đơn điệu", "Không trũng, không nước."),
             ("n=200000 răng cưa", "Đúng giới hạn dạng răng cưa; ground truth bằng two-pointer chuẩn trong Python.")],
        ),
        "hsgx-p5-c10-precision": vi_challenge(
            "Phòng khám: Trung bình trôi",
            "**Bài toán.** n ≤ 200000 số nguyên tới 10^9; in floor(trung bình). Bản nộp tích lũy double — WA trên đầu vào lớn do sai số cộng dồn. Sửa bằng số nguyên chính xác.",
            [("nhỏ", "Mean 7/3 = 2.33 → 2."),
             ("trộn âm", "Mean 0."),
             ("kiểm floor", "Mean −3.5 floor là −4 (chia nguyên C++ cắt về 0 — coi chừng!)."),
             ("n=200000", "Tổng 2·10^14: số nguyên chính xác là bản sửa.")],
        ),
    },
    solutions=[
        ("hsgx-p5-c7-bsearch", C7_R, C7_W),
        ("hsgx-p5-c8-triangle", C8_R, C8_W),
        ("hsgx-p5-c9-trapping", C9_R, C9_W),
        ("hsgx-p5-c10-precision", C10_R, C10_W),
    ],
)

# --------------------------------------------------------------- checkpoint
# The clinic apex: the interval task with the STRICTER convention — touching
# endpoints COUNT as overlap (s2 == e1 is forbidden), so the fix uses `>`.
CP_M5_R = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& p : v) in >> p.second >> p.first;   // (end, start)
    sort(v.begin(), v.end());
    long long cnt = 0, lastEnd = -4e18;
    for (auto [e, s] : v) {
        if (s > lastEnd) { ++cnt; lastEnd = e; }   // strict: touching = overlap
    }
    out << cnt << "{{NL}}";
""") + END

CP_M5_W = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& p : v) in >> p.first >> p.second;   // (start, end)
    // WRONG: greedy by START (and relaxed s >= lastEnd) — fails both the
    // adversarial ordering and the touching-endpoints convention.
    sort(v.begin(), v.end());
    long long cnt = 0, lastEnd = -4e18;
    for (auto [s, e] : v) {
        if (s >= lastEnd) { ++cnt; lastEnd = e; }
    }
    out << cnt << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgx-cp-m5", "Checkpoint — Prove It or Lose It",
    "The interval greedy returns for a verdict: fix it so every test passes. The buggy by-start version is graded as the wrong side — your fix must beat it on the adversarial ordering.",
    20,
    """
**Điểm kiểm tra — Chứng minh hoặc mất điểm.** Maximum non-overlapping
intervals, n ≤ 200000, with shared-endpoint overlap. The buggy
sort-by-start greedy fails the adversarial ordering test. Fix the greedy
(sort by end), keep the endpoint convention straight, and pass all four
tests. In your solution notes: state the exchange argument in one line.
""",
    "Điểm kiểm tra — Chứng minh hoặc mất điểm",
    "Greedy đoạn không chồng lấn trở lại để được phán quyết: sửa để mọi test qua. Bản lỗi sort-theo-đầu bị chấm ở phía sai — bản sửa của bạn phải thắng nó ở thứ tự đối kháng.",
    """
**Điểm kiểm tra — Chứng minh hoặc mất điểm.** Tối đa các đoạn không chồng
lấn, n ≤ 200000, chung đầu mút vẫn tính chồng. Bản lỗi greedy
sort-theo-đầu gãy ở test thứ tự đối kháng. Sửa greedy (sort theo cuối),
giữ đúng quy ước đầu mút, và qua cả bốn test. Trong lời giải: nêu lập luận
đổi chỗ trong một dòng.
""",
    CP_CH := challenge(
        "hsgx-cp-m5-intervals", "Maximum Non-Overlapping Intervals",
        """**Bài toán.** n intervals [s, e]; choose the maximum count of pairwise
non-overlapping intervals. Touching endpoints (e1 == s2) count as
OVERLAPPING. n ≤ 200000; coordinates ≤ 10^9.

**Output:** one integer.
""",
        [
            contest_test("two touch", T("2", "1 3", "3 5"), T("1"),
                "Touching endpoints overlap → only one."),
            contest_test("gap", T("2", "1 2", "3 4"), T("2"),
                "2 < 3: no overlap."),
            contest_test("adversarial", T("3", "1 10", "2 3", "4 5"), T("2"),
                "The by-start greedy takes [1,10] and loses."),
            contest_test("n=200000 chain", T("200000") + T(*["%d %d" % (2 * i, 2 * i + 1) for i in range(1, 200001)]), T("200000"),
            "Unit intervals (2,3),(4,5),...: all 200000 are disjoint (3<4 etc.) and fit."),
        ],
        level="debugging",
        difficulty="advanced",
    ),
    vi_challenge(
        "Tối đa đoạn không chồng lấn",
        "**Bài toán.** n đoạn [s, e]; chọn tối đa số đoạn đôi-một-không-chồng. Chạm đầu mút (e1 == s2) tính là CHỒNG. n ≤ 200000.",
        [("hai đoạn chạm", "Chạm đầu mút vẫn chồng → chỉ một."),
         ("có khoảng hở", "2 < 3: không chồng."),
         ("đối kháng", "Greedy-theo-đầu lấy [1,10] và thua."),
         ("n=200000", "Các đoạn (2,3),(4,5),(6,7),...: kẻ hở thật giữa các đoạn kề nhau — cả 200000 đều vừa.")],
    ),
    CP_M5_R,
    CP_M5_W,
)

print("module m5 complete")
