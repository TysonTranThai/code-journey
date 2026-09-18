#!/usr/bin/env python3
"""HSG — Module 19: hsg-debug (gỡ lỗi).

Real broken programs, real bugs: off-by-one, overflow, uninitialized
accumulators, wrong comparator, missing visited reset. The statement
embeds the buggy source; the learner fixes it. W = the bug verbatim.
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

M = "hsg-debug"
write_module(
    M,
    "Debugging Competitive Programs",
    "Wrong answers are clues: reproduce, isolate, instrument, fix — then re-test the boundary that broke you.",
    "Gỡ lỗi chương trình thi đấu",
    "WA là manh mối: tái hiện, cô lập, đo đạc, sửa — rồi test lại chính biên vừa làm bạn thất bại.",
    ["hsg-m19-method", "hsg-m19-taxonomy", "hsg-cp-m19"],
    ["hsg-p19-debug"],
)

write_lesson(
    M,
    "hsg-m19-method",
    "A Debugging Method",
    "Stress against a slow correct solution — the fastest bug finder you own.",
    15,
    """## The loop

1. **Reproduce** on the smallest failing input. A bug that only shows
   at N = 100,000 usually shows at N = 7 once you know where to look.
2. **Isolate** — print intermediate state (prefix sums, loop
   variables) or cut the program in half.
3. **Form a hypothesis**, predict the output, run. Wrong prediction
   narrows the search space; right prediction means you found it.
4. **Fix the cause**, not the symptom. Adding `if (x == 42)` special
   cases is how bugs become monsters.
5. **Re-test every old case** plus the boundary that broke you.

## Stress testing (the superpower)

Write a slow-but-obviously-correct solver plus a tiny random-input
generator, then compare outputs in a loop:

```
gen > in.txt && slow < in.txt > slow.txt && fast < in.txt > fast.txt
diff slow.txt fast.txt  # mismatch = your minimal witness
```

Ten seconds of this beats an hour of staring. It finds the failing
input FOR you.

## Reading judge verdicts

- **WA** on a small test: logic bug. On a big test only: overflow or
  complexity.
- **TLE**: count your operations; print a counter if unsure.
- **RTE**: array bounds, division by zero, stack depth.
- **WA only on samples with negatives**: initialization (0 is not
  neutral for max).
""",
    "Một phương pháp gỡ lỗi",
    "Stress-test với một lời giải chậm nhưng chắc chắn đúng — công cụ săn bug nhanh nhất bạn có.",
    """## Vòng lặp

1. **Tái hiện** trên input failing nhỏ nhất. Bug chỉ lộ ở N = 100,000
   thường lộ ở N = 7 một khi bạn biết tìm đâu.
2. **Cô lập** — in trạng thái trung gian (mảng cộng dồn, biến vòng
   lặp) hoặc cắt đôi chương trình.
3. **Đặt giả thuyết**, đoán output, chạy. Đoán sai thu hẹp không gian
   tìm kiếm; đoán đúng nghĩa là bạn đã tìm ra nó.
4. **Sửa nguyên nhân**, không sửa triệu chứng. Chèn `if (x == 42)`
   xử lý đặc biệt là cách biến bug thành quái vật.
5. **Chạy lại mọi case cũ** cộng đúng biên vừa làm bạn thất bại.

## Stress testing (siêu năng lực)

Viết một solver chậm-nhưng-chắc-chắn-đúng cộng một bộ sinh input nhỏ
ngẫu nhiên, rồi so sánh đầu ra trong vòng lặp:

```
gen > in.txt && slow < in.txt > slow.txt && fast < in.txt > fast.txt
diff slow.txt fast.txt  # lệch = bằng chứng tối tiểu của bạn
```

Mười giây làm cái này hơn một giờ nhìn màn hình. Nó tìm GIÙM bạn
input gây lỗi.

## Đọc verdict từ máy chấm

- **WA** ở test nhỏ: bug logic. Chỉ ở test to: tràn số hoặc độ phức
  tạp.
- **TLE**: đếm phép tính; không chắc thì in bộ đếm.
- **RTE**: tràn mảng, chia cho 0, độ sâu ngăn xếp.
- **WA chỉ ở sample có số âm**: khởi tạo (0 không trung tính cho max).
""",
)

write_lesson(
    M,
    "hsg-m19-taxonomy",
    "The Beginner Bug Zoo",
    "Five families cause most WA: boundaries, initialization, overflow, comparisons, state.",
    16,
    """## 1. Boundary bugs

`<` vs `<=`, `n-1` vs `n`, 0-based vs 1-based. Symptom: wrong on the
smallest or largest input only. Test: N = 1 and N = max, always.

## 2. Initialization bugs

`max = 0` with all-negative input; forgetting to reset a counter
between test cases. Symptom: correct except on extreme values or
later cases.

## 3. Overflow bugs

`int a = 100000; long long s = a * a;` — the product happens in int
FIRST. Symptom: WA on big tests only, garbage-looking numbers.

## 4. Comparison bugs

Wrong comparator direction (sorts descending when you need ascending)
or `<=` where strictness matters (ties counted twice). Symptom:
almost-right order, or off-by-small amounts.

## 5. State bugs

Missing `visited` reset between queries, mutating shared data during
iteration, forgetting the undo in backtracking. Symptom: first query
correct, later ones garbage — or only the first test passes.

## The fix discipline

After ANY fix: re-run every test you have, plus the one that failed.
Two bugs often hide in one wrong program — fixing the first can
change the symptoms of the second.
""",
    "Vườn thú bug của người mới",
    "Năm họ gây phần lớn WA: biên, khởi tạo, tràn số, so sánh, trạng thái.",
    """## 1. Bug biên

`<` với `<=`, `n-1` với `n`, 0-based với 1-based. Triệu chứng: sai
chỉ ở input nhỏ nhất hoặc lớn nhất. Test: luôn thử N = 1 và N = max.

## 2. Bug khởi tạo

`max = 0` với input toàn âm; quên reset bộ đếm giữa các test. Triệu
chứng: đúng trừ các giá trị cực đoan hoặc các case sau.

## 3. Bug tràn số

`int a = 100000; long long s = a * a;` — phép nhân xảy ra trong int
TRƯỚC. Triệu chứng: WA chỉ ở test to, số ra rác.

## 4. Bug so sánh

Sai hướng bộ so sánh (sắp giảm khi cần tăng) hoặc `<=` chỗ cần nghiêm
ngặt (bị đếm hai lần). Triệu chứng: thứ tự gần đúng, hoặc lệch một
lượng nhỏ.

## 5. Bug trạng thái

Quên reset `visited` giữa các truy vấn, sửa dữ liệu chung khi đang
duyệt, quên hoàn tác trong quay lui. Triệu chứng: truy vấn đầu đúng,
sau đó ra rác — hoặc chỉ test đầu tiên passes.

## Kỷ luật sửa lỗi

Sau MỌI lần sửa: chạy lại mọi test đang có, cộng đúng test vừa fail.
Hai bug thường trú chung một chương trình sai — sửa bug đầu có thể
thay đổi triệu chứng của bug hai.
""",
)

# --- A1: boundary bug (off-by-one loop bound) ---
A1 = challenge(
    "hsg-p19-offbyone",
    "Debug: Off-by-One Sum",
    T(
        "**Description:** The program below must print the sum of all n array elements,",
        "but it is wrong. Identify the bug and fix it.",
        "",
        "**Broken code:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int n; in >> n;",
        "    vector<long long> a(n);",
        "    for (auto& x : a) in >> x;",
        "    long long s = 0;",
        "    for (int i = 0; i < n - 1; ++i) s += a[i];",
        "    out << s;",
        "}",
        "```",
        "",
        "**Input:** Line 1: n (1 <= n <= 100000). Line 2: n integers (|a[i]| <= 10^9).",
        "**Output:** One integer — the total sum.",
        "",
        "**Example:** `3` / `1 2 3` -> `6`.",
    ),
    [
        contest_test("sample", T("3", "1 2 3"), T("6"), "The broken code prints 3 — the last element is dropped."),
        contest_test("single", T("1", "42"), T("42"), "n = 1: the broken loop adds nothing."),
        contest_test("negatives", T("3", "-5 5 -1"), T("-1"), "Signs must not matter."),
        contest_test("big", T("2", "1000000000 1000000000"), T("2000000000"), "64-bit sum."),
        contest_test("max n", T("4", "1 2 3 4"), T("10"), "All four count."),
    ],
    level="guided",
    difficulty="intermediate",
)

# --- A2: initialization bug (max starts at 0) ---
A2 = challenge(
    "hsg-p19-initmax",
    "Debug: The Zero Anchor",
    T(
        "**Description:** The program must print the maximum VALUE in the array. It fails",
        "on some inputs. Find and fix the bug.",
        "",
        "**Broken code:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int n; in >> n;",
        "    long long best = 0;",
        "    for (int i = 0; i < n; ++i) {",
        "        long long x; in >> x;",
        "        best = max(best, x);",
        "    }",
        "    out << best;",
        "}",
        "```",
        "",
        "**Input:** Line 1: n (1 <= n <= 100000). Line 2: n integers (|a[i]| <= 10^9).",
        "**Output:** One integer — the maximum value.",
        "",
        "**Example:** `3` / `-2 7 -9` -> `7`.",
    ),
    [
        contest_test("sample", T("3", "-2 7 -9"), T("7"), "Broken code passes this one."),
        contest_test("all negative", T("4", "-1 -5 -3 -2"), T("-1"),
                     "The killer: zero-anchored best prints 0 — never a valid maximum here."),
        contest_test("single negative", T("1", "-8"), T("-8"), "One element, negative."),
        contest_test("mixed", T("3", "-7 0 -2"), T("0"), "Zero CAN be the max."),
        contest_test("big values", T("3", "-1000000000 3 1000000000"), T("1000000000"),
                     "64-bit reading discipline."),
    ],
    level="guided",
    difficulty="intermediate",
)

# --- A3: overflow bug (int multiplication) ---
A3 = challenge(
    "hsg-p19-overflow",
    "Debug: The Shrinking Product",
    T(
        "**Description:** The program must print a[0] * a[1] (values up to 10^5), but",
        "sometimes prints nonsense. Find and fix the bug.",
        "",
        "**Broken code:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int a, b; in >> a >> b;",
        "    int p = a * b;",
        "    out << p;",
        "}",
        "```",
        "",
        "**Input:** One line: a b (|a|, |b| <= 100000).",
        "**Output:** One integer — the product.",
        "",
        "**Example:** `300 400` -> `120000`.",
    ),
    [
        contest_test("small", T("300 400"), T("120000"), "Fits int — broken code passes."),
        contest_test("negative small", T("-3 7"), T("-21"), "Signs fine."),
        contest_test("overflow", T("100000 100000"), T("10000000000"),
                     "10^10 overflows 32-bit int — the broken code prints garbage."),
        contest_test("negative overflow", T("-100000 99999"), T("-9999900000"),
                     "Just under 10^10 — still needs 64 bits."),
        contest_test("zero", T("0 99999"), T("0"), "Zero absorbs."),
    ],
    level="guided",
    difficulty="intermediate",
)

# --- A4: wrong comparator (descending instead of ascending) ---
A4 = challenge(
    "hsg-p19-comparator",
    "Debug: Backwards Sort",
    T(
        "**Description:** The program must sort n pairs by their first element ASCENDING",
        "(ties: any order) and print the first elements. Find and fix the bug.",
        "",
        "**Broken code:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int n; in >> n;",
        "    vector<pair<int,int>> v(n);",
        "    for (auto& p : v) in >> p.first >> p.second;",
        "    sort(v.begin(), v.end(), [](const pair<int,int>& x, const pair<int,int>& y) {",
        "        return x.first > y.first;",
        "    });",
        "    for (int i = 0; i < n; ++i)",
        "        out << v[i].first << (i + 1 < n ? \" \" : \"\");",
        "    out << \"\\\\n\";",
        "}",
        "```",
        "",
        "**Input:** Line 1: n (1 <= n <= 100000). Next n lines: a b (|a|, |b| <= 10^9).",
        "**Output:** One line: the first elements in ascending order, space-separated.",
        "",
        "**Example:** `3` / `3 0` / `1 9` / `2 4` -> `1 2 3`.",
    ),
    [
        contest_test("sample", T("3", "3 0", "1 9", "2 4"), T("1 2 3"),
                     "The broken code prints 3 2 1."),
        contest_test("already sorted", T("2", "1 0", "2 0"), T("1 2"), "Hides the bug."),
        contest_test("duplicates", T("4", "5 1", "5 2", "3 9", "5 0"), T("3 5 5 5"),
                     "Ties keep any order — the firsts must be 3 5 5 5."),
        contest_test("negatives", T("3", "-1 0", "-9 0", "4 0"), T("-9 -1 4"),
                     "Negative firsts sort first."),
        contest_test("single", T("1", "7 7"), T("7"), "One element."),
    ],
    level="independent",
    difficulty="intermediate",
)

# --- A5: state bug (missing visited reset between queries) ---
A5 = challenge(
    "hsg-p19-state",
    "Debug: The One-Shot Reachability",
    T(
        "**Description:** The program answers q reachability queries on an undirected",
        "graph, but only the first query is ever right. Find and fix the bug.",
        "",
        "**Broken code:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int n, m, q; in >> n >> m >> q;",
        "    vector<vector<int>> adj(n + 1);",
        "    for (int i = 0; i < m; ++i) {",
        "        int u, v; in >> u >> v;",
        "        adj[u].push_back(v); adj[v].push_back(u);",
        "    }",
        "    vector<char> vis(n + 1, 0);",
        "    for (int i = 0; i < q; ++i) {",
        "        int a, b; in >> a >> b;",
        "        vector<int> st{a};",
        "        vis[a] = 1;",
        "        while (!st.empty()) {",
        "            int u = st.back(); st.pop_back();",
        "            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }",
        "        }",
        "        out << (vis[b] ? \"YES\" : \"NO\") << \"\\\\n\";",
        "    }",
        "}",
        "```",
        "",
        "**Input:** Line 1: n m q (1 <= n <= 1000, 0 <= m <= 5000, 1 <= q <= 1000). Next m",
        "lines: u v. Next q lines: a b.",
        "**Output:** q lines: `YES` if b is reachable from a, else `NO`.",
        "",
        "**Example:** `3 1 2` / `1 2` / `1 2` / `2 3` -> `YES` / `NO`.",
    ),
    [
        contest_test("sample", T("3 1 2", "1 2", "1 2", "2 3"), T("YES", "NO"),
                     "The broken code answers the second query from stale visited state."),
        contest_test("repeat query", T("2 1 2", "1 2", "1 2", "1 2"), T("YES", "YES"),
                     "The same query twice must agree."),
        contest_test("self", T("2 0 1", "1 1"), T("YES"), "Everyone reaches themselves."),
        contest_test("reverse edge", T("3 1 1", "2 3", "3 2"), T("YES"),
                     "Undirected — the reverse direction must also work."),
        contest_test("cross component", T("4 2 2", "1 2", "3 4", "1 2", "3 1"), T("YES", "NO"),
                     "Query 1 marks {1,2}; query 3->1 crosses components — stale visited answers YES."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p19-offbyone": vi_challenge(
        "Gỡ lỗi: Lệch một tổng",
        T(
            "**Đề bài:** Chương trình dưới đây phải in tổng của cả n phần tử mảng, nhưng nó",
            "sai. Xác định bug và sửa nó.",
            "",
            "**Mã lỗi:**",
            "```cpp",
            "void solve(std::istream& in, std::ostream& out) {",
            "    int n; in >> n;",
            "    vector<long long> a(n);",
            "    for (auto& x : a) in >> x;",
            "    long long s = 0;",
            "    for (int i = 0; i < n - 1; ++i) s += a[i];",
            "    out << s;",
            "}",
            "```",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100000). Dòng 2: n số nguyên (|a[i]| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — tổng.",
            "",
            "**Ví dụ:** `3` / `1 2 3` -> `6`.",
        ),
        [
            ("sample", "Mã lỗi in 3 — phần tử cuối bị bỏ."),
            ("single", "n = 1: vòng lặp lỗi không cộng gì."),
            ("negatives", "Dấu không được ảnh hưởng."),
            ("big", "Tổng 64 bit."),
            ("max n", "Cả bốn phần tử được tính."),
        ],
    ),
    "hsg-p19-initmax": vi_challenge(
        "Gỡ lỗi: Mỏ neo 0",
        T(
            "**Đề bài:** Chương trình phải in GIÁ TRỊ lớn nhất trong mảng. Nó sai với một",
            "số input. Tìm và sửa bug.",
            "",
            "**Mã lỗi:**",
            "```cpp",
            "void solve(std::istream& in, std::ostream& out) {",
            "    int n; in >> n;",
            "    long long best = 0;",
            "    for (int i = 0; i < n; ++i) {",
            "        long long x; in >> x;",
            "        best = max(best, abs(x));",
            "    }",
            "    out << best;",
            "}",
            "```",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100000). Dòng 2: n số nguyên (|a[i]| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — giá trị lớn nhất.",
            "",
            "**Ví dụ:** `3` / `-2 7 -9` -> `7`.",
        ),
        [
            ("sample", "Mã lỗi vẫn qua test này."),
            ("all negative", "Case sát thủ: best neo-0 in 0 — không phải max hợp lệ."),
            ("single negative", "Một phần tử, âm."),
            ("mixed", "0 CÓ THỂ là max."),
            ("big values", "Kỷ luật đọc 64 bit."),
        ],
    ),
    "hsg-p19-overflow": vi_challenge(
        "Gỡ lỗi: Tích bị co cụm",
        T(
            "**Đề bài:** Chương trình phải in a[0] * a[1] (giá trị tới 10^5), nhưng thỉnh",
            "thoảng in ra rác. Tìm và sửa bug.",
            "",
            "**Mã lỗi:**",
            "```cpp",
            "void solve(std::istream& in, std::ostream& out) {",
            "    int a, b; in >> a >> b;",
            "    int p = a * b;",
            "    out << p;",
            "}",
            "```",
            "",
            "**Dữ liệu vào:** Một dòng: a b (|a|, |b| <= 100000).",
            "**Dữ liệu ra:** Một số nguyên — tích.",
            "",
            "**Ví dụ:** `300 400` -> `120000`.",
        ),
        [
            ("small", "Vừa int — mã lỗi passes."),
            ("negative small", "Dấu ổn."),
            ("overflow", "10^10 tràn int 32-bit — mã lỗi in rác."),
            ("negative overflow", "Ngay dưới 10^10 — vẫn cần 64 bit."),
            ("zero", "0 hấp thụ mọi thứ."),
        ],
    ),
    "hsg-p19-comparator": vi_challenge(
        "Gỡ lỗi: Sắp ngược",
        T(
            "**Đề bài:** Chương trình phải sắp n cặp theo phần tử đầu TĂNG DẦN (bằng nhau:",
            "thứ tự bất kỳ) và in các phần tử đầu. Tìm và sửa bug.",
            "",
            "**Mã lỗi:**",
            "```cpp",
            "void solve(std::istream& in, std::ostream& out) {",
            "    int n; in >> n;",
            "    vector<pair<int,int>> v(n);",
            "    for (auto& p : v) in >> p.first >> p.second;",
            "    sort(v.begin(), v.end(), [](const pair<int,int>& x, const pair<int,int>& y) {",
            "        return x.first > y.first;",
            "    });",
            "    for (int i = 0; i < n; ++i)",
            "        out << v[i].first << (i + 1 < n ? \" \" : \"\");",
            "    out << \"\\\\n\";",
            "}",
            "```",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100000). n dòng tiếp: a b (|a|, |b| <= 10^9).",
            "**Dữ liệu ra:** Một dòng: các phần tử đầu theo thứ tự tăng, cách nhau dấu cách.",
            "",
            "**Ví dụ:** `3` / `3 0` / `1 9` / `2 4` -> `1 2 3`.",
        ),
        [
            ("sample", "Mã lỗi in 3 2 1."),
            ("already sorted", "Che được bug."),
            ("duplicates", "Bằng nhau giữ thứ tự bất kỳ — các first phải là 3 5 5 5."),
            ("negatives", "Số âm đứng trước."),
            ("single", "Một phần tử."),
        ],
    ),
    "hsg-p19-state": vi_challenge(
        "Gỡ lỗi: Tính-tới-một-lần",
        T(
            "**Đề bài:** Chương trình trả lời q truy vấn tính-tới-được trên đồ thị vô hướng,",
            "nhưng chỉ truy vấn đầu bao giờ đúng. Tìm và sửa bug.",
            "",
            "**Mã lỗi:**",
            "```cpp",
            "void solve(std::istream& in, std::ostream& out) {",
            "    int n, m, q; in >> n >> m >> q;",
            "    vector<vector<int>> adj(n + 1);",
            "    for (int i = 0; i < m; ++i) {",
            "        int u, v; in >> u >> v;",
            "        adj[u].push_back(v); adj[v].push_back(u);",
            "    }",
            "    vector<char> vis(n + 1, 0);",
            "    for (int i = 0; i < q; ++i) {",
            "        int a, b; in >> a >> b;",
            "        vector<int> st{a};",
            "        vis[a] = 1;",
            "        while (!st.empty()) {",
            "            int u = st.back(); st.pop_back();",
            "            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }",
            "        }",
            "        out << (vis[b] ? \"YES\" : \"NO\") << \"\\\\n\";",
            "    }",
            "}",
            "```",
            "",
            "**Dữ liệu vào:** Dòng 1: n m q (1 <= n <= 1000, 0 <= m <= 5000, 1 <= q <= 1000).",
            "m dòng tiếp: u v. q dòng tiếp: a b.",
            "**Dữ liệu ra:** q dòng: `YES` nếu b tới được từ a, ngược lại `NO`.",
            "",
            "**Ví dụ:** `3 1 2` / `1 2` / `1 2` / `2 3` -> `YES` / `NO`.",
        ),
        [
            ("sample", "Mã lỗi trả lời truy vấn hai bằng trạng thái visited cũ."),
            ("repeat query", "Cùng một truy vấn hai lần phải đồng nhất."),
            ("self", "Ai cũng tới được chính mình."),
            ("reverse edge", "Vô hướng — chiều ngược cũng phải hoạt động."),
            ("cross component", "Truy vấn 1 đánh dấu {1,2}; truy vấn 3->1 sang thành phần khác — visited cũ sẽ trả lời YES."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p19-debug",
    "Debugging Problem Set",
    "Off-by-one sums, zero-anchored maxima, int products, reversed comparators, stale visited state.",
    "Bài tập gỡ lỗi",
    "Tổng lệch-một, max neo-0, tích int, bộ so sánh ngược, trạng thái visited cũ.",
    "hsg-m19-taxonomy",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p19-offbyone",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long s = 0;
    for (int i = 0; i < n; ++i) s += a[i];   // FIXED: n, not n - 1
    out << s << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long s = 0;
    for (int i = 0; i < n - 1; ++i) s += a[i];
    out << s << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p19-initmax",
            CPP_STD + cpp("""    int n; in >> n;
    long long best;
    in >> best;                          // FIXED: anchor on the first element
    for (int i = 1; i < n; ++i) {
        long long x; in >> x;
        best = max(best, x);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    long long best = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        best = max(best, x);
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p19-overflow",
            CPP_STD + cpp("""    long long a, b; in >> a >> b;        // FIXED: read as 64-bit
    out << a * b << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int a, b; in >> a >> b;
    int p = a * b;
    out << p << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p19-comparator",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<int,int>> v(n);
    for (auto& p : v) in >> p.first >> p.second;
    sort(v.begin(), v.end(), [](const pair<int,int>& x, const pair<int,int>& y) {
        return x.first < y.first;        // FIXED: ascending
    });
    for (int i = 0; i < n; ++i)
        out << v[i].first << (i + 1 < n ? " " : "");
    out << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<int,int>> v(n);
    for (auto& p : v) in >> p.first >> p.second;
    sort(v.begin(), v.end(), [](const pair<int,int>& x, const pair<int,int>& y) {
        return x.first > y.first;
    });
    for (int i = 0; i < n; ++i)
        out << v[i].first << (i + 1 < n ? " " : "");
    out << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p19-state",
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    string res;
    for (int i = 0; i < q; ++i) {
        int a, b; in >> a >> b;
        vector<char> vis(n + 1, 0);      // FIXED: fresh state per query
        vector<int> st{a};
        vis[a] = 1;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }
        }
        res += vis[b] ? "YES" : "NO";
        if (i + 1 < q) res += "{{NL}}";
    }
    out << res << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v; in >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    string res;
    for (int i = 0; i < q; ++i) {
        int a, b; in >> a >> b;
        vector<int> st{a};
        vis[a] = 1;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; st.push_back(v); }
        }
        res += vis[b] ? "YES" : "NO";
        if (i + 1 < q) res += "{{NL}}";
    }
    out << res << "{{NL}}";
""") + END,
        ),
    ],
)

CH19 = challenge(
    "hsg-cp-m19-recover",
    "Debug: The Missing Reset",
    T(
        "**Description:** This program must print, for each of q values x, how many array",
        "elements are less than x — but it degrades after the first query. Find and fix",
        "the bug.",
        "",
        "**Broken code:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int n, q; in >> n >> q;",
        "    vector<long long> a(n);",
        "    for (auto& x : a) in >> x;",
        "    sort(a.begin(), a.end());",
        "    int cnt = 0;",
        "    for (int i = 0; i < q; ++i) {",
        "        long long x; in >> x;",
        "        while (cnt < n && a[cnt] < x) ++cnt;",
        "        out << cnt << \"\\\\n\";",
        "    }",
        "}",
        "```",
        "",
        "**Input:** Line 1: n q (1 <= n, q <= 100000). Line 2: n integers (|a[i]| <= 10^9).",
        "Next q lines: x (|x| <= 10^9).",
        "**Output:** q lines: the count of elements strictly less than x.",
        "",
        "**Example:** `4 2` / `1 3 5 7` / `4` / `6` -> `2` / `3`.",
    ),
    [
        contest_test("sample", T("4 2", "1 3 5 7", "4", "6"), T("2", "3"),
                     "The monotone pointer is never reset — the broken code prints 2 then 3? No: it prints 2 then 2... run it: cnt stops at 2 for x=4, then continues for x=6 — actually correct for ASCENDING x. Try x=6 first: 3 then x=4 prints 3 (WRONG, must be 2)."),
        contest_test("descending queries", T("4 2", "1 3 5 7", "6", "4"), T("3", "2"),
                     "The killer case — a stale pointer over-counts the second query."),
        contest_test("below all", T("3 1", "1 2 3", "0"), T("0"), "Nothing is below 0."),
        contest_test("above all", T("3 1", "1 2 3", "10"), T("3"), "Everything is."),
        contest_test("equal boundary", T("3 2", "5 5 5", "5", "6"), T("0", "3"),
                     "Strictly less: 5 counts for nothing at x=5."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP19 = vi_challenge(
    "Gỡ lỗi: Cái reset bị mất",
    T(
        "**Đề bài:** Chương trình này phải in, với mỗi giá trị x trong q truy vấn, số phần",
        "tử mảng nhỏ hơn x — nhưng nó suy giảm sau truy vấn đầu. Tìm và sửa bug.",
        "",
        "**Mã lỗi:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int n, q; in >> n >> q;",
        "    vector<long long> a(n);",
        "    for (auto& x : a) in >> x;",
        "    sort(a.begin(), a.end());",
        "    int cnt = 0;",
        "    for (int i = 0; i < q; ++i) {",
        "        long long x; in >> x;",
        "        while (cnt < n && a[cnt] < x) ++cnt;",
        "        out << cnt << \"\\\\n\";",
        "    }",
        "}",
        "```",
        "",
        "**Dữ liệu vào:** Dòng 1: n q (1 <= n, q <= 100000). Dòng 2: n số nguyên (|a[i]| <= 10^9).",
        "q dòng tiếp: x (|x| <= 10^9).",
        "**Dữ liệu ra:** q dòng: số phần tử nhỏ hơn x một cách nghiêm ngặt.",
        "",
        "**Ví dụ:** `4 2` / `1 3 5 7` / `6` / `4` -> `3` / `2`.",
    ),
    [
        ("sample", "Con trỏ đơn điệu không bao giờ được reset — case x=6 trước, x=4 sau sẽ lộ bug."),
        ("descending queries", "Case sát thủ — con trỏ cũ đếm thừa truy vấn sau."),
        ("below all", "Không gì nhỏ hơn 0."),
        ("above all", "Tất cả đều nhỏ hơn."),
        ("equal boundary", "Nghiêm ngặt: 5 không được tính khi x=5."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m19",
    "Checkpoint — Debugging",
    "Pass the graded problem to finish the debugging module.",
    15,
    """**Checkpoint — gỡ lỗi.** Pass the graded challenge below. The bug is
a monotone pointer reused across queries — correct only when queries
arrive in ascending order. Two honest fixes: reset the pointer per
query (O(nq), fine at these constraints) or answer each query with
binary search / lower_bound (O(log n) per query). The graded
near-misses: keeping the shared pointer, and counting with `<=` (the
boundary test with equal values catches both).

**Điểm kiểm tra — gỡ lỗi.** Pass bài chấm bên dưới. Bug là một con trỏ
đơn điệu dùng chung qua các truy vấn — chỉ đúng khi truy vấn đến theo
thứ tự tăng. Hai cách sửa chính trực: reset con trỏ theo từng truy vấn
(O(nq), ổn với giới hạn này) hoặc trả lời mỗi truy vấn bằng tìm kiếm
nhị phân / lower_bound (O(log n) mỗi truy vấn). Các near-miss bị chấm:
giữ con trỏ dùng chung, và đếm bằng `<=` (test biên với giá trị bằng
bắt được cả hai).
""",
    "Checkpoint — Debugging",
    "Pass the graded problem to finish the debugging module.",
    """**Điểm kiểm tra — gỡ lỗi.** Pass bài chấm bên dưới. Bug là một con trỏ
đơn điệu dùng chung qua các truy vấn — chỉ đúng khi truy vấn đến theo
thứ tự tăng. Hai cách sửa chính trực: reset con trỏ theo từng truy vấn
(O(nq), ổn với giới hạn này) hoặc trả lời mỗi truy vấn bằng tìm kiếm
nhị phân / lower_bound (O(log n) mỗi truy vấn). Các near-miss bị chấm:
giữ con trỏ dùng chung, và đếm bằng `<=` (test biên với giá trị bằng
bắt được cả hai).
""",
    CH19,
    VI_CP19,
    solution=CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    string res;
    for (int i = 0; i < q; ++i) {
        long long x; in >> x;
        int lo = 0, hi = n;              // first index with a[idx] >= x
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (a[mid] < x) lo = mid + 1; else hi = mid;
        }
        res += to_string(lo);
        if (i + 1 < q) res += "{{NL}}";
    }
    out << res << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    int cnt = 0;
    string res;
    for (int i = 0; i < q; ++i) {
        long long x; in >> x;
        while (cnt < n && a[cnt] < x) ++cnt;
        res += to_string(cnt);
        if (i + 1 < q) res += "{{NL}}";
    }
    out << res << "{{NL}}";
""") + END,
)

print("M19 done")
