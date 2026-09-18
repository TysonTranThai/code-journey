#!/usr/bin/env python3
"""C# — Beginner — Module 20: csb-algorithms.

Problem-solving toolkit: growth reasoning (Big-O), linear vs binary
search, frequency maps, and the recursion contract. House conventions:
ISO-idiomatic C#, self-contained tests, Ws are behavioral near-misses
that fail at least one discriminating test.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-algorithms"

write_module(
    M,
    "Problem Solving and Algorithms",
    "Reasoning about growth, searching honestly, and the two loop shapes that solve most problems: frequency maps and recursion.",
    "Giải quyết vấn đề và thuật toán",
    "Suy luận về độ tăng trưởng, tìm kiếm trung thực, và hai hình dạng vòng lặp giải quyết phần lớn bài toán: đếm tần suất và đệ quy.",
    ["csb-m20-big-o", "csb-m20-searching", "csb-m20-patterns", "csb-checkpoint-m20"],
    ["csb-p20-algo"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m20-big-o",
    "Growth, not stopwatches",
    "Big-O describes how work grows with input size — counting operations beats timing a machine.",
    13,
    r"""
## Counting, not timing

A stopwatch measures a machine; growth describes an algorithm. Count how the work grows as input size `n` grows:

| Shape | Example | n = 10 | n = 10,000 |
| --- | --- | --- | --- |
| O(1) | dictionary lookup | 1 | 1 |
| O(log n) | binary search | ~3 | ~14 |
| O(n) | one loop | 10 | 10,000 |
| O(n²) | nested loops | 100 | 100,000,000 |

Nested loops **multiply**: an outer loop over `n` with an inner loop over `n` is `n × n`. That last row is why "it works on my test data" is not a performance argument — a fix that turns 100,000,000 steps into 10,000 is the difference between a feature and a freeze.
""",
    "Tăng trưởng, không phải đồng hồ bấm giây",
    "Big-O mô tả công việc tăng thế nào theo kích thước đầu vào — đếm phép toán thắng việc bấm giờ chiếc máy.",
    r"""
## Đếm, không phải bấm giờ

Đồng hồ bấm giây đo chiếc máy; độ tăng trưởng mô tả thuật toán. Hãy đếm công việc tăng thế nào khi kích thước đầu vào `n` tăng:

| Dạng | Ví dụ | n = 10 | n = 10,000 |
| --- | --- | --- | --- |
| O(1) | tra từ điển | 1 | 1 |
| O(log n) | tìm kiếm nhị phân | ~3 | ~14 |
| O(n) | một vòng lặp | 10 | 10,000 |
| O(n²) | vòng lặp lồng nhau | 100 | 100,000,000 |

Vòng lặp lồng nhau **nhân**: vòng ngoài qua `n` với vòng trong qua `n` là `n × n`. Dòng cuối cùng đó là lý do "chạy được với dữ liệu thử của tôi" không phải lập luận hiệu năng — một bản sửa biến 100,000,000 bước thành 10,000 là khoảng cách giữa một tính năng và một cú treo.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m20-searching",
    "Linear and binary search",
    "Unsorted data forces a linear scan; sorted data lets each comparison throw away half the candidates.",
    12,
    r"""
## Linear: the honest default

Unsorted data gives you no choice — check items one by one, O(n). Correct, simple, and the right tool when `n` is small or the data refuses to stay sorted.

## Binary: pay for order once

A **sorted** array lets each comparison discard half the candidates:

```text
[1 3 5 7 9]  target 7
lo=0 hi=4 mid=2:  5 < 7 → keep right half
lo=3 hi=4 mid=3:  found at 3
```

The invariant: *if the target exists, it is always within `[lo, hi]`*. Each step preserves the invariant while shrinking the window — O(log n). A million sorted items need ~20 comparisons. The classic bugs are off-by-one on the window (`lo <= hi` vs `lo < hi` — the last element never gets examined) and on the move (`mid` vs `mid ± 1` — infinite loops); both come from breaking the invariant.
""",
    "Tìm kiếm tuyến tính và nhị phân",
    "Dữ liệu chưa sắp buộc quét tuyến tính; dữ liệu đã sắp cho phép mỗi phép so sánh vứt bỏ một nửa ứng viên.",
    r"""
## Tuyến tính: mặc định trung thực

Dữ liệu chưa sắp không cho bạn lựa chọn — kiểm tra từng phần tử một, O(n). Đúng, đơn giản, và là công cụ đúng khi `n` nhỏ hoặc dữ liệu không chịu sắp xếp.

## Nhị phân: trả tiền cho trật tự một lần

Một mảng **đã sắp** cho phép mỗi phép so sánh bỏ đi một nửa ứng viên:

```text
[1 3 5 7 9]  target 7
lo=0 hi=4 mid=2:  5 < 7 → giữ nửa phải
lo=3 hi=4 mid=3:  tìm thấy tại 3
```

Bất biến: *nếu đích tồn tại, nó luôn nằm trong `[lo, hi]`*. Mỗi bước giữ bất biến trong khi thu hẹp cửa sổ — O(log n). Một triệu phần tử đã sắp chỉ cần ~20 phép so sánh. Các lỗi kinh điển là lệch-một trên cửa sổ (`lo <= hi` với `lo < hi` — phần tử cuối không bao giờ được xét) và lệch-một trên bước di chuyển (`mid` với `mid ± 1` — vòng lặp vô hạn); cả hai đều do phá vỡ bất biến.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m20-patterns",
    "Frequency maps and recursion",
    "The dictionary-as-counter pattern solves a family of problems, and recursion is just a contract: base case plus smaller step.",
    13,
    r"""
## The frequency map

Counting things is the most reusable loop shape in the collections chapter:

```csharp
var counts = new Dictionary<string, int>();
foreach (string w in words)
    counts[w] = counts.GetValueOrDefault(w) + 1;
```

Many problems are this pattern wearing a costume: first duplicate, top word, anagram check, pair-sum lookup — each is a dictionary doing the memory work that a nested loop would redo O(n²) times.

## The recursion contract

Every recursive method needs two things, or it never terminates:

1. **Base case** — an input answered directly, without recursing.
2. **Smaller step** — each call works on a strictly smaller input, moving toward the base case.

The call stack does the bookkeeping: every call gets its own frame with its own locals, and the answer is assembled as frames return.
""",
    "Bản đồ tần suất và đệ quy",
    "Mẫu từ-điển-làm-bộ-đếm giải quyết cả một họ bài toán, và đệ quy chỉ là một hợp đồng: trường hợp gốc cộng bước nhỏ hơn.",
    r"""
## Bản đồ tần suất

Đếm các thứ là hình dạng vòng lặp tái sử dụng nhất trong chương collection:

```csharp
var counts = new Dictionary<string, int>();
foreach (string w in words)
    counts[w] = counts.GetValueOrDefault(w) + 1;
```

Nhiều bài toán chỉ là mẫu này mặc trang phục: bản sao đầu tiên, từ đứng đầu, kiểm tra đảo chữ, tra cặp tổng — mỗi bài là một từ điển làm phần việc ghi nhớ mà vòng lặp lồng nhau sẽ phải làm lại O(n²) lần.

## Hợp đồng đệ quy

Mọi phương thức đệ quy cần hai thứ, nếu không nó không bao giờ dừng:

1. **Trường hợp gốc** — một đầu vào được trả lời trực tiếp, không gọi đệ quy.
2. **Bước nhỏ hơn** — mỗi lời gọi làm việc trên đầu vào nhỏ hơn một cách nghiêm ngặt, tiến về trường hợp gốc.

Ngăn xếp lời gọi lo phần sổ sách: mỗi lời gọi có khung riêng với biến cục bộ riêng, và kết quả được ghép lại khi các khung quay về.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p20-algo",
    "Algorithm workshop",
    "Duplicates, binary search, tie-breaking, bracket matching — each a pattern from the lessons, each with edge cases that punish near-misses.",
    "Xưởng thuật toán",
    "Bản trùng, tìm kiếm nhị phân, hòa-sắp-xếp, khớp ngoặc — mỗi bài một mẫu từ các bài học, mỗi bài có các trường hợp biên trừng phạt gần-đúng.",
    "csb-m20-patterns",
    45,
    "beginner",
    [
        challenge(
            "csb-p20-firstdup",
            "First duplicate",
            "Implement `static int FirstDuplicate(int[] nums)` — return the value whose **second occurrence appears earliest** when scanning left to right; -1 if no value repeats. For [2,1,3,1,2] the answer is 1 (its second occurrence at index 3 beats 2's at index 4).",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.FirstDuplicate(new[] { 2, 1, 3, 1, 2 }), 1, \"scan order, not value order\");\nCj.Eq(Solution.FirstDuplicate(new[] { 5, 5, 5 }), 5, \"immediate repeat\");",
                    "One pass with a set of seen values; the first Add that fails wins.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.FirstDuplicate(new[] { 1, 2, 3 }), -1, \"no duplicates\");\nCj.Eq(Solution.FirstDuplicate(new int[] { }), -1, \"empty input\");\nCj.Eq(Solution.FirstDuplicate(new[] { 1, 2, 1 }), 1, \"duplicate is NOT adjacent to itself\");",
                    "No-repeat, empty, and a duplicate separated from its twin.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p20-binsearch",
            "Binary search",
            "Implement `static int BinarySearch(int[] sorted, int target)` — return the index of `target` in the ascending array, or -1. Keep the invariant: if the target exists, it stays within [lo, hi].",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var a = new[] { 1, 3, 5, 7, 9 };\nCj.Eq(Solution.BinarySearch(a, 7), 3, \"middle hit\");\nCj.Eq(Solution.BinarySearch(a, 1), 0, \"first element\");\nCj.Eq(Solution.BinarySearch(a, 9), 4, \"last element\");\nCj.Eq(Solution.BinarySearch(a, 4), -1, \"absent\");",
                    "Both boundaries and an absent value — window edges are where bugs live.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.BinarySearch(new[] { 5 }, 5), 0, \"single-element hit\");\nCj.Eq(Solution.BinarySearch(new[] { 5 }, 4), -1, \"single-element miss\");\nCj.Eq(Solution.BinarySearch(new int[] { }, 1), -1, \"empty\");",
                    "A one-element window (lo == hi) must still be examined.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p20-freq",
            "Top word with a tie rule",
            "Implement `static string TopWord(List<string> words)` — the most frequent word; on a tie, the **alphabetically first**. Every list has at least one word.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.TopWord(new List<string> { \"milo\", \"milo\", \"ajax\", \"ajax\" }), \"ajax\", \"tie broken alphabetically\");\nCj.Eq(Solution.TopWord(new List<string> { \"c\", \"c\", \"a\" }), \"c\", \"clear winner\");",
                    "The tie case is the contract — count first, name second.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.TopWord(new List<string> { \"b\", \"a\" }), \"a\", \"all tied\");\nCj.Eq(Solution.TopWord(new List<string> { \"zulu\", \"zulu\", \"alpha\", \"bravo\", \"bravo\", \"alpha\" }), \"alpha\", \"three-way tie\");",
                    "Insertion order must not leak into the result.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p20-paren",
            "Balanced brackets",
            "Implement `static bool IsBalanced(string s)` — true when every bracket in s (only `()[]{} appear`) closes in the correct nesting order. \"([)]\" is NOT balanced.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.True(Solution.IsBalanced(\"([]{})\"), \"clean nesting\");\nCj.False(Solution.IsBalanced(\"([)]\"), \"interleaved\");\nCj.False(Solution.IsBalanced(\"([]{}\"), \"unclosed\");",
                    "A stack: push openers, pop and match closers.",
                ),
                (
                    "edges",
                    "Cj.True(Solution.IsBalanced(\"\"), \"empty is balanced\");\nCj.False(Solution.IsBalanced(\")(\"), \"close before open\");\nCj.False(Solution.IsBalanced(\"(((\"), \"openers left over\");",
                    "Empty string, closer-first, and dangling openers.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p20-firstdup": vi_challenge(
            "Bản trùng đầu tiên",
            "Hiện thực `static int FirstDuplicate(int[] nums)` — trả giá trị có **lần xuất-hiện-thứ-hai sớm nhất** khi quét từ trái sang phải; -1 nếu không giá trị nào lặp. Với [2,1,3,1,2] đáp án là 1 (lần thứ hai của nó ở chỉ số 3 sớm hơn của 2 ở chỉ số 4).",
            [
                ("normal", "Một lượt duyệt với tập các giá trị đã thấy; Add đầu tiên thất bại là người thắng."),
                ("edges", "Không-lặp, rỗng, và một bản trùng KHÔNG kề với bản kép của nó."),
            ],
        ),
        "csb-p20-binsearch": vi_challenge(
            "Tìm kiếm nhị phân",
            "Hiện thực `static int BinarySearch(int[] sorted, int target)` — trả chỉ số của `target` trong mảng tăng dần, hoặc -1. Giữ bất biến: nếu đích tồn tại, nó luôn nằm trong [lo, hi].",
            [
                ("normal", "Cả hai biên và một giá trị vắng mặt — mép cửa sổ là nơi lỗi sống."),
                ("edges", "Cửa sổ một-phần-tử (lo == hi) vẫn phải được xét."),
            ],
        ),
        "csb-p20-freq": vi_challenge(
            "Từ đứng đầu với luật hòa",
            "Hiện thực `static string TopWord(List<string> words)` — từ xuất hiện nhiều nhất; khi hòa, chọn **theo alphabet trước tiên**. Mọi danh sách có ít nhất một từ.",
            [
                ("normal", "Trường hợp hòa chính là hợp đồng — đếm trước, tên sau."),
                ("edges", "Thứ-tự-xuất-hiện không được rò rỉ vào kết quả."),
            ],
        ),
        "csb-p20-paren": vi_challenge(
            "Ngoặc cân bằng",
            "Hiện thực `static bool IsBalanced(string s)` — true khi mọi ngoặc trong s (chỉ có `()[]{}`) được đóng theo đúng thứ tự lồng nhau. \"([)]\" KHÔNG cân bằng.",
            [
                ("normal", "Một ngăn xếp: đẩy ngoặc mở, lấy ra và khớp ngoặc đóng."),
                ("edges", "Chuỗi rỗng, đóng-trước-mở, và ngoặc mở bỏ dở."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p20-firstdup",
            'public class Solution\n{\n    public static int FirstDuplicate(int[] nums)\n    {\n        var seen = new HashSet<int>();\n        foreach (int n in nums)\n        {\n            if (!seen.Add(n)) return n;\n        }\n        return -1;\n    }\n}\n',
            'public class Solution\n{\n    public static int FirstDuplicate(int[] nums)\n    {\n        // near-miss: compares only ADJACENT pairs — a duplicate that is\n        // not next to its twin goes unnoticed\n        for (int i = 0; i + 1 < nums.Length; i++)\n        {\n            if (nums[i] == nums[i + 1]) return nums[i];\n        }\n        return -1;\n    }\n}\n',
        ),
        (
            "csb-p20-binsearch",
            'public class Solution\n{\n    public static int BinarySearch(int[] sorted, int target)\n    {\n        int lo = 0, hi = sorted.Length - 1;\n        while (lo <= hi)\n        {\n            int mid = lo + (hi - lo) / 2;\n            if (sorted[mid] == target) return mid;\n            if (sorted[mid] < target) lo = mid + 1;\n            else hi = mid - 1;\n        }\n        return -1;\n    }\n}\n',
            'public class Solution\n{\n    public static int BinarySearch(int[] sorted, int target)\n    {\n        int lo = 0, hi = sorted.Length - 1;\n        // near-miss: strict < — when the window shrinks to ONE element\n        // (lo == hi) it is never examined, so a final-position target\n        // is reported missing\n        while (lo < hi)\n        {\n            int mid = lo + (hi - lo) / 2;\n            if (sorted[mid] == target) return mid;\n            if (sorted[mid] < target) lo = mid + 1;\n            else hi = mid - 1;\n        }\n        return -1;\n    }\n}\n',
        ),
        (
            "csb-p20-freq",
            'public class Solution\n{\n    public static string TopWord(List<string> words)\n    {\n        var counts = new Dictionary<string, int>();\n        foreach (string w in words)\n        {\n            counts[w] = counts.GetValueOrDefault(w) + 1;\n        }\n        string best = "";\n        int bestCount = -1;\n        foreach (var kv in counts)\n        {\n            if (kv.Value > bestCount ||\n                (kv.Value == bestCount && string.CompareOrdinal(kv.Key, best) < 0))\n            {\n                best = kv.Key;\n                bestCount = kv.Value;\n            }\n        }\n        return best;\n    }\n}\n',
            'public class Solution\n{\n    public static string TopWord(List<string> words)\n    {\n        var counts = new Dictionary<string, int>();\n        foreach (string w in words)\n        {\n            counts[w] = counts.GetValueOrDefault(w) + 1;\n        }\n        string best = "";\n        int bestCount = -1;\n        foreach (var kv in counts)\n        {\n            // near-miss: ties resolved by INSERTION order (first seen\n            // wins) instead of alphabetically\n            if (kv.Value > bestCount)\n            {\n                best = kv.Key;\n                bestCount = kv.Value;\n            }\n        }\n        return best;\n    }\n}\n',
        ),
        (
            "csb-p20-paren",
            'public class Solution\n{\n    public static bool IsBalanced(string s)\n    {\n        var stack = new Stack<char>();\n        foreach (char c in s)\n        {\n            if (c == \'(\' || c == \'[\' || c == \'{\')\n            {\n                stack.Push(c);\n            }\n            else if (c == \')\' || c == \']\' || c == \'}\')\n            {\n                if (stack.Count == 0) return false;\n                char open = stack.Pop();\n                if ((c == \')\' && open != \'(\') ||\n                    (c == \']\' && open != \'[\') ||\n                    (c == \'}\' && open != \'{\'))\n                    return false;\n            }\n        }\n        return stack.Count == 0;\n    }\n}\n',
            'public class Solution\n{\n    public static bool IsBalanced(string s)\n    {\n        // near-miss: counts openers and closers — nesting and matching\n        // are ignored entirely\n        int opens = 0, closes = 0;\n        foreach (char c in s)\n        {\n            if (c == \'(\' || c == \'[\' || c == \'{\') opens++;\n            else if (c == \')\' || c == \']\' || c == \'}\') closes++;\n        }\n        return opens == closes;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m20",
    "Checkpoint — Algorithm toolkit",
    "Three classic patterns in one solution: sum-formula gaps, single-use pair sums, and run-length encoding.",
    20,
    r"""
## Checkpoint: the algorithm toolkit

**Task:** implement in `Solution`:

1. `static int MissingNumber(int[] nums)` — the array holds `n` distinct numbers from `0..n` with exactly one missing; return it. ([3,0,1] → 2.)
2. `static bool HasPairSum(int[] nums, int target)` — true when **two distinct elements** sum to target (an element may not pair with itself).
3. `static string Compress(string s)` — run-length encoding: "aaabbc" → "a3b2c1"; every run's count is written, even 1 ("a" → "a1"); empty → empty.
""",
    "Checkpoint — Bộ công cụ thuật toán",
    "Ba mẫu kinh điển trong một lời giải: khoảng hở theo công thức tổng, cặp tổng dùng-một-lần, và nén theo độ dài chuỗi.",
    r"""
## Checkpoint: bộ công cụ thuật toán

**Nhiệm vụ:** hiện thực trong `Solution`:

1. `static int MissingNumber(int[] nums)` — mảng chứa `n` số phân biệt thuộc `0..n` với đúng một số bị thiếu; trả số đó. ([3,0,1] → 2.)
2. `static bool HasPairSum(int[] nums, int target)` — true khi **hai phần tử phân biệt** có tổng bằng target (một phần tử không thể ghép với chính nó).
3. `static string Compress(string s)` — nén theo độ dài chuỗi: "aaabbc" → "a3b2c1"; số đếm của mọi chuỗi đều được ghi, kể cả 1 ("a" → "a1"); rỗng → rỗng.
""",
    challenge(
        "csb-checkpoint-m20-task",
        "AlgorithmToolkit",
        "Implement `MissingNumber`, `HasPairSum`, and `Compress` — each is one of the module's patterns.",
        CS_PRELUDE,
        [
            (
                "gaps",
                "Cj.Eq(Solution.MissingNumber(new[] { 3, 0, 1 }), 2, \"missing middle\");\nCj.Eq(Solution.MissingNumber(new[] { 0 }), 1, \"missing one past the end\");\nCj.Eq(Solution.MissingNumber(new[] { 0, 1, 2 }), 3, \"missing last\");",
                "The array has n numbers from 0..n — so n equals nums.Length, not Length+1.",
            ),
            (
                "pairs",
                "Cj.True(Solution.HasPairSum(new[] { 1, 2, 3, 4 }, 6), \"2+4\");\nCj.False(Solution.HasPairSum(new[] { 1, 2, 3, 4 }, 8), \"4+4 is one element twice\");\nCj.False(Solution.HasPairSum(new int[] { }, 5), \"empty\");",
                "Check `seen` BEFORE adding the current value — that's what forbids self-pairing.",
            ),
            (
                "runs",
                "Cj.Eq(Solution.Compress(\"aaabbc\"), \"a3b2c1\", \"runs of 3, 2, 1\");\nCj.Eq(Solution.Compress(\"a\"), \"a1\", \"count of one is still written\");\nCj.Eq(Solution.Compress(\"\"), \"\", \"empty\");",
                "Flush the final run after the loop — the last run has no next character to trigger it.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "AlgorithmToolkit",
        "Hiện thực `MissingNumber`, `HasPairSum`, và `Compress` — mỗi bài là một mẫu của module này.",
        [
            ("gaps", "Mảng có n số thuộc 0..n — vậy n bằng nums.Length, không phải Length+1."),
            ("pairs", "Kiểm tra `seen` TRƯỚC khi thêm giá trị hiện tại — đó là điều cấm tự-ghép."),
            ("runs", "Xả chuỗi cuối cùng sau vòng lặp — chuỗi cuối không có ký tự kế để kích nó."),
        ],
    ),
    solution='public class Solution\n{\n    public static int MissingNumber(int[] nums)\n    {\n        int n = nums.Length;\n        long expected = (long)n * (n + 1) / 2;\n        long actual = 0;\n        foreach (int v in nums) actual += v;\n        return (int)(expected - actual);\n    }\n    public static bool HasPairSum(int[] nums, int target)\n    {\n        var seen = new HashSet<int>();\n        foreach (int v in nums)\n        {\n            if (seen.Contains(target - v)) return true;\n            seen.Add(v);\n        }\n        return false;\n    }\n    public static string Compress(string s)\n    {\n        if (s.Length == 0) return "";\n        var sb = new System.Text.StringBuilder();\n        int run = 1;\n        for (int i = 1; i < s.Length; i++)\n        {\n            if (s[i] == s[i - 1]) run++;\n            else\n            {\n                sb.Append(s[i - 1]).Append(run);\n                run = 1;\n            }\n        }\n        sb.Append(s[s.Length - 1]).Append(run);\n        return sb.ToString();\n    }\n}\n',
    wrong='public class Solution\n{\n    public static int MissingNumber(int[] nums)\n    {\n        // near-miss: treats the range as 0..n+1 (uses Length+1) — every\n        // answer comes back too large\n        int n = nums.Length + 1;\n        long expected = (long)n * (n + 1) / 2;\n        long actual = 0;\n        foreach (int v in nums) actual += v;\n        return (int)(expected - actual);\n    }\n    public static bool HasPairSum(int[] nums, int target)\n    {\n        // near-miss: compares every pair INCLUDING an element with\n        // itself — target 8 on [.., 4, ..] "pairs" 4 with 4\n        for (int i = 0; i < nums.Length; i++)\n            for (int j = 0; j < nums.Length; j++)\n                if (nums[i] + nums[j] == target) return true;\n        return false;\n    }\n    public static string Compress(string s)\n    {\n        // near-miss: omits counts of 1 — "a3b2c1" becomes "a3bc"\n        if (s.Length == 0) return "";\n        var sb = new System.Text.StringBuilder();\n        int run = 1;\n        for (int i = 1; i < s.Length; i++)\n        {\n            if (s[i] == s[i - 1]) run++;\n            else\n            {\n                sb.Append(s[i - 1]);\n                if (run > 1) sb.Append(run);\n                run = 1;\n            }\n        }\n        sb.Append(s[s.Length - 1]);\n        if (run > 1) sb.Append(run);\n        return sb.ToString();\n    }\n}\n',
)

print("module 20 authored")
