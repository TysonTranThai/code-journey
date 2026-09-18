#!/usr/bin/env python3
"""Java — Intermediate — Module 13: java-algorithms-inter.

Reasoning-first algorithm patterns: two pointers, sliding window, prefix
sums, binary search boundaries, and map-based counting. Complexity is
taught as a *consequence* of the loop structure, not recited. House
conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-algorithms-inter"

# ── lesson 13.1 — two pointers & sliding window ────────────────────────────
L_TWOPTR_EN = r"""
## Two pointers and sliding windows

When a *sorted* array pairs up (or a contiguous run must satisfy a
property), two indices moving inward/forward replace nested loops:

```java
// pair summing to target in a sorted array — O(n) not O(n²)
int lo = 0, hi = xs.length - 1;
while (lo < hi) {
    int s = xs[lo] + xs[hi];
    if (s == target) return true;
    if (s < target) lo++; else hi--;
}
```

The **sliding window** maintains a running aggregate while advancing
two co-moving boundaries:

```java
// longest run with at most k distinct values
int left = 0, best = 0;
Map<Integer, Integer> freq = new HashMap<>();
for (int right = 0; right < xs.length; right++) {
    freq.merge(xs[right], 1, Integer::sum);
    while (freq.size() > k) {
        if (freq.merge(xs[left], -1, Integer::sum) == 0) freq.remove(xs[left]);
        left++;
    }
    best = Math.max(best, right - left + 1);
}
```

The key insight: each element enters and leaves the window at most once,
so the *while inside the for* still totals O(n).
"""

L_TWOPTR_VI = r"""
## Two pointer và sliding window

Khi mảng *đã sắp xếp* cần ghép cặp (hoặc một đoạn liền kề phải thỏa tính
chất), hai chỉ số chạy vào/trước thay cho vòng lặp lồng:

```java
// cặp có tổng bằng target trên mảng đã sắp — O(n) thay vì O(n²)
int lo = 0, hi = xs.length - 1;
while (lo < hi) {
    int s = xs[lo] + xs[hi];
    if (s == target) return true;
    if (s < target) lo++; else hi--;
}
```

**Sliding window** duy trì một giá trị tích lũy trong khi hai biên chạy
cùng nhau:

```java
// run dài nhất với tối đa k giá trị phân biệt
int left = 0, best = 0;
Map<Integer, Integer> freq = new HashMap<>();
for (int right = 0; right < xs.length; right++) {
    freq.merge(xs[right], 1, Integer::sum);
    while (freq.size() > k) {
        if (freq.merge(xs[left], -1, Integer::sum) == 0) freq.remove(xs[left]);
        left++;
    }
    best = Math.max(best, right - left + 1);
}
```

Insight then chốt: mỗi phần tử vào và ra khỏi window tối đa một lần, nên
*while bên trong for* vẫn tổng cộng là O(n).
"""

# ── lesson 13.2 — prefix sums & binary search ──────────────────────────────
L_PREFIX_EN = r"""
## Prefix sums and binary search boundaries

**Prefix sums** make any range-sum O(1) after O(n) setup:

```java
long[] pre = new long[n + 1];
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + xs[i];
// sum of [l, r) = pre[r] - pre[l]
```

**Binary search** is not just "find x" — its real power is *boundary*
search on a predicate: the first index where something becomes true.

```java
// first index with xs[i] >= target (classic lower bound)
int lo = 0, hi = xs.length;          // hi exclusive
while (lo < hi) {
    int mid = (lo + hi) >>> 1;
    if (xs[mid] >= target) hi = mid; else lo = mid + 1;
}
return lo;   // == xs.length means "not found"
```

The half-open interval `[lo, hi)` + `hi = mid` / `lo = mid + 1`
invariant kills the off-by-one family. `(lo + hi) >>> 1` avoids int
overflow. If you can phrase a question as "first/last index where P
holds", you can binary-search it in O(log n) — monotonic predicate
required.
"""

L_PREFIX_VI = r"""
## Prefix sum và biên của binary search

**Prefix sum** biến mọi tổng đoạn thành O(1) sau khi chuẩn bị O(n):

```java
long[] pre = new long[n + 1];
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + xs[i];
// tổng đoạn [l, r) = pre[r] - pre[l]
```

**Binary search** không chỉ là "tìm x" — sức mạnh thật là tìm *biên* trên
một predicate: chỉ số đầu tiên mà điều gì đó trở thành đúng.

```java
// chỉ số đầu với xs[i] >= target (lower bound kinh điển)
int lo = 0, hi = xs.length;          // hi loại trừ
while (lo < hi) {
    int mid = (lo + hi) >>> 1;
    if (xs[mid] >= target) hi = mid; else lo = mid + 1;
}
return lo;   // == xs.length nghĩa là "không tìm thấy"
```

Bất biến khoảng nửa mở `[lo, hi)` + `hi = mid` / `lo = mid + 1` tiêu diệt
cả họ lỗi lệch một. `(lo + hi) >>> 1` tránh tràn int. Nếu diễn đạt được
câu hỏi thành "chỉ số đầu/cuối mà P đúng", bạn có thể binary search nó
trong O(log n) — predicate phải đơn điệu.
"""

# ── lesson 13.3 — maps as thinking tools ───────────────────────────────────
L_MAPS_EN = r"""
## Maps as thinking tools

Many "hard" problems collapse once you choose the right auxiliary map:

- **counting** — `freq.merge(x, 1, Integer::sum)` turns "how many" into
  O(1) lookups (anagram detection, majority element)
- **indexing** — `Map<Value, Index>` remembers *where* you saw something
  (two-sum in one pass; last-seen index for window problems)
- **grouping** — `groupingBy` turns equivalence classes into buckets
  (group anagrams by their sorted-letter signature)

```java
// two-sum, one pass — O(n)
Map<Integer, Integer> seen = new HashMap<>();
for (int i = 0; i < xs.length; i++) {
    Integer j = seen.get(target - xs[i]);
    if (j != null) return new int[]{j, i};
    seen.put(xs[i], i);
}
```

The pattern to internalize: *trade space for a cheaper question*. If a
loop exists only to answer "have I seen X?", the map already knows.
"""

L_MAPS_VI = r"""
## Map là công cụ tư duy

Nhiều bài "khó" sụp đổ ngay khi bạn chọn đúng map phụ trợ:

- **đếm** — `freq.merge(x, 1, Integer::sum)` biến "bao nhiêu" thành tra
  cứu O(1) (dò anagram, phần tử đa số)
- **đánh chỉ mục** — `Map<Value, Index>` nhớ *đã thấy ở đâu* (two-sum
  trong một lượt; chỉ số lần-quen-cuối cho bài window)
- **nhóm** — `groupingBy` biến các lớp tương đương thành bucket (nhóm
  anagram theo chữ-sắp-xếpký-tự)

```java
// two-sum, một lượt — O(n)
Map<Integer, Integer> seen = new HashMap<>();
for (int i = 0; i < xs.length; i++) {
    Integer j = seen.get(target - xs[i]);
    if (j != null) return new int[]{j, i};
    seen.put(xs[i], i);
}
```

Mẫu cần thấm: *đổi không gian lấy câu hỏi rẻ hơn*. Nếu một vòng lặp tồn
tại chỉ để trả lời "đã thấy X chưa?", map đã biết sẵn.
"""

write_module(
    MOD,
    "Intermediate Algorithms",
    "Two pointers, sliding windows, prefix sums, binary-search boundaries, and maps as space-for-time tools.",
    "Thuật toán trình trung cấp",
    "Two pointer, sliding window, prefix sum, biên binary search, và map như công cụ đổi không gian lấy thời gian.",
    ["two-pointers-windows", "prefix-binary-search", "maps-thinking", "javi-checkpoint-algorithms"],
    ["javi-p13-algorithms"],
)

write_lesson(MOD, "two-pointers-windows", "Two Pointers & Sliding Windows", "Sorted-array pairing, running aggregates over co-moving boundaries, and why the nested while is still linear.", 15, L_TWOPTR_EN, "Two Pointer & Sliding Window", "Ghép cặp mảng đã sắp, giá trị tích lũy trên biên chạy cùng, và vì sao while lồng vẫn tuyến tính.", L_TWOPTR_VI)

write_lesson(MOD, "prefix-binary-search", "Prefix Sums & Search Boundaries", "O(1) range sums after O(n) setup, and binary search as boundary-finding on monotonic predicates.", 15, L_PREFIX_EN, "Prefix Sum & biên tìm kiếm", "Tổng đoạn O(1) sau khi setup O(n), và binary search như tìm biên trên predicate đơn điệu.", L_PREFIX_VI)

write_lesson(MOD, "maps-thinking", "Maps as Thinking Tools", "Counting, indexing, and grouping patterns that trade space for O(1) answers.", 13, L_MAPS_EN, "Map là công cụ tư duy", "Các mẫu đếm, đánh chỉ mục, và nhóm đổi không gian lấy câu trả lời O(1).", L_MAPS_VI)

# ── practice set ────────────────────────────────────────────────────────────
P13_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement methods below.
}
"""

CH_P13_PAIRSUM = challenge(
    "javi-p13-pair-sum",
    "Sorted Pair Sum",
    r"""Implement `static int[] pairWithSum(int[] sorted, int target)` —
return the two INDICES (ascending) of a pair summing to target, or null
when none exists. Use two pointers — the sorted order is your invariant.

Examples: [1,3,5,8], target 8 → [1,2] (3+5); target 4 → [0,0] is invalid
(distinct indices only), so null unless a real pair exists. Duplicate
values are allowed as a pair ([3,3], target 6 → [0,1]).""",
    P13_BOILER,
    [
        (
            "found pair",
            r"""
checkEq(Solution.pairWithSum(new int[]{1, 3, 5, 8}, 8), new int[]{1, 2}, "3+5");
""",
            "lo=1 (3), hi=2 (5) → 8.",
        ),
        (
            "duplicates pair up",
            r"""
checkEq(Solution.pairWithSum(new int[]{3, 3}, 6), new int[]{0, 1}, "3+3");
""",
            "Two distinct indices holding equal values are a valid pair.",
        ),
        (
            "no pair",
            r"""
checkEq(Solution.pairWithSum(new int[]{1, 2}, 100), null, "none");
""",
            "Pointers cross without a match → null.",
        ),
        (
            "empty input",
            r"""
checkEq(Solution.pairWithSum(new int[]{}, 5), null, "empty");
""",
            "Empty array → null.",
        ),
    ],
    level="guided",
)

CH_P13_WINDOW = challenge(
    "javi-p13-sliding-window",
    "Longest Window with K Distinct",
    r"""Implement `static int longestWindow(int[] xs, int k)` — the length
of the longest contiguous run containing at most k distinct values.
k <= 0 → 0. Use the sliding-window pattern with a frequency map.

[1,2,1,2,3], k=2 → 4 (the run [1,2,1,2]).
[1,1,1], k=1 → 3. Empty → 0.""",
    P13_BOILER,
    [
        (
            "window shrinks on overflow",
            r"""
checkEq(Solution.longestWindow(new int[]{1, 2, 1, 2, 3}, 2), 4, "at most two distinct");
""",
            "The 3 forces a shrink; best is the earlier 4-length run.",
        ),
        (
            "single value",
            r"""
checkEq(Solution.longestWindow(new int[]{7, 7, 7}, 1), 3, "all same");
""",
            "One distinct value, whole array qualifies.",
        ),
        (
            "edge guards",
            r"""
checkEq(Solution.longestWindow(new int[]{1, 2, 3}, 0), 0, "k=0");
checkEq(Solution.longestWindow(new int[]{}, 2), 0, "empty");
""",
            "k <= 0 or empty input → 0.",
        ),
    ],
    level="independent",
)

CH_P13_PREFIX = challenge(
    "javi-p13-prefix-sum",
    "Prefix Sums & Range Queries",
    r"""Implement:
- `static long[] prefixSums(int[] xs)` — length n+1, pre[0]=0,
  pre[i+1] = pre[i] + xs[i].
- `static long rangeSum(long[] pre, int l, int r)` — sum of [l, r)
  via pre[r] - pre[l].
- `static int countSubarraysWithSum(int[] xs, int target)` — number of
  contiguous subarrays summing exactly to target, using the prefix map
  trick (count of earlier prefixes with pre[j] == pre[i] - target).

[-2, 2, -2, 2], target 0 → 5 subarrays (each zero-sum run counts).""",
    P13_BOILER,
    [
        (
            "prefix and range",
            r"""
long[] pre = Solution.prefixSums(new int[]{1, 2, 3, 4});
checkEq(Solution.rangeSum(pre, 1, 3), 5L, "2+3");
""",
            "pre[3] - pre[1] = 6 - 1 = 5.",
        ),
        (
            "full range",
            r"""
long[] pre = Solution.prefixSums(new int[]{1, 2, 3, 4});
checkEq(Solution.rangeSum(pre, 0, 4), 10L, "whole array");
""",
            "pre[4] - pre[0] = 10.",
        ),
        (
            "zero-sum subarray counting",
            r"""
checkEq(Solution.countSubarraysWithSum(new int[]{-2, 2, -2, 2}, 0), 4, "four zero-sum runs");
""",
            "[-2,2], [-2,2](middle), [2,-2], [-2,2](last two), [-2,2,-2,2] — count them exactly.",
        ),
        (
            "target matching single elements",
            r"""
checkEq(Solution.countSubarraysWithSum(new int[]{5, 1, 5}, 5), 2, "two fives");
""",
            "Each 5 alone is one subarray; nothing else sums to 5.",
        ),
    ],
    level="independent",
)

VI_CH_P13_PAIRSUM = vi_challenge(
    "Ghép cặp trên mảng đã sắp",
    r"""Cài `static int[] pairWithSum(int[] sorted, int target)` — trả hai
CHỈ SỐ (tăng dần) của một cặp có tổng bằng target, hoặc null khi không
có. Dùng two pointer — thứ tự đã sắp là bất biến của bạn.

Ví dụ: [1,3,5,8], target 8 → [1,2] (3+5); target 4 → [0,0] không hợp lệ
(hai chỉ số phải khác nhau), nên null trừ khi có cặp thật. Giá trị trùng
được phép làm cặp ([3,3], target 6 → [0,1]).""",
    [
        ("Tìm được cặp", "lo=1 (3), hi=2 (5) → 8."),
        ("Giá trị trùng ghép được", "Hai chỉ số khác nhau giữ giá trị bằng nhau là một cặp hợp lệ."),
        ("Không có cặp", "Hai pointer giao nhau mà không khớp → null."),
        ("Input rỗng", "Mảng rỗng → null."),
    ],
)

VI_CH_P13_WINDOW = vi_challenge(
    "Window dài nhất với K giá trị phân biệt",
    r"""Cài `static int longestWindow(int[] xs, int k)` — độ dài đoạn liền
kề dài nhất chứa tối đa k giá trị phân biệt. k <= 0 → 0. Dùng mẫu
sliding window với một map tần suất.

[1,2,1,2,3], k=2 → 4 (đoạn [1,2,1,2]).
[1,1,1], k=1 → 3. Rỗng → 0.""",
    [
        ("Window co lại khi tràn", "Số 3 ép co window; best là đoạn dài 4 trước đó."),
        ("Một giá trị duy nhất", "Một giá trị phân biệt, cả mảng đạt."),
        ("Guard biên", "k <= 0 hoặc input rỗng → 0."),
    ],
)

VI_CH_P13_PREFIX = vi_challenge(
    "Prefix sum & truy vấn đoạn",
    r"""Cài:
- `static long[] prefixSums(int[] xs)` — độ dài n+1, pre[0]=0,
  pre[i+1] = pre[i] + xs[i].
- `static long rangeSum(long[] pre, int l, int r)` — tổng [l, r)
  qua pre[r] - pre[l].
- `static int countSubarraysWithSum(int[] xs, int target)` — số mảng con
  liền kề có tổng đúng bằng target, dùng mẹo map prefix (đếm các prefix
  trước đó có pre[j] == pre[i] - target).

[-2, 2, -2, 2], target 0 → 4 mảng con (mỗi run có tổng 0 được đếm).""",
    [
        ("Prefix và đoạn", "pre[3] - pre[1] = 6 - 1 = 5."),
        ("Toàn mảng", "pre[4] - pre[0] = 10."),
        ("Đếm mảng con tổng 0", "Đếm chính xác: [-2,2], [2,-2], [-2,2], và cả bốn — 4 run."),
        ("Target khớp phần tử đơn", "Mỗi số 5 riêng lẻ là một mảng con; không gì khác tổng bằng 5."),
    ],
)

write_practice(
    MOD,
    "javi-p13-algorithms",
    "Algorithms Lab",
    "Two-pointer pairing, window shrinking, prefix-map subarray counting — patterns over memorized answers.",
    "Xưởng thuật toán",
    "Ghép cặp two pointer, co window, đếm mảng con bằng map prefix — mẫu tư duy hơn là học thuộc đáp án.",
    "maps-thinking",
    40,
    "intermediate",
    [CH_P13_PAIRSUM, CH_P13_WINDOW, CH_P13_PREFIX],
    {CH_P13_PAIRSUM["id"]: VI_CH_P13_PAIRSUM, CH_P13_WINDOW["id"]: VI_CH_P13_WINDOW, CH_P13_PREFIX["id"]: VI_CH_P13_PREFIX},
    solutions=[
        (
            CH_P13_PAIRSUM["id"],
            r"""
public class Solution {
    public static int[] pairWithSum(int[] sorted, int target) {
        if (sorted == null) return null;
        int lo = 0, hi = sorted.length - 1;
        while (lo < hi) {
            int s = sorted[lo] + sorted[hi];
            if (s == target) return new int[]{lo, hi};
            if (s < target) lo++; else hi--;
        }
        return null;
    }
}
""",
            r"""
public class Solution {
    // W: returns the VALUES as if they were indices — on unsorted-input
    // deployments this silently corrupts callers. Also fails the
    // duplicates case: 3+3=6 reports [3,3] instead of [0,1].
    public static int[] pairWithSum(int[] sorted, int target) {
        if (sorted == null) return null;
        int lo = 0, hi = sorted.length - 1;
        while (lo < hi) {
            int s = sorted[lo] + sorted[hi];
            if (s == target) return new int[]{sorted[lo], sorted[hi]};
            if (s < target) lo++; else hi--;
        }
        return null;
    }
}
""",
        ),
        (
            CH_P13_WINDOW["id"],
            r"""
import java.util.*;

public class Solution {
    public static int longestWindow(int[] xs, int k) {
        if (xs == null || xs.length == 0 || k <= 0) return 0;
        Map<Integer, Integer> freq = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < xs.length; right++) {
            freq.merge(xs[right], 1, Integer::sum);
            while (freq.size() > k) {
                int out = freq.merge(xs[left], -1, Integer::sum);
                if (out == 0) freq.remove(xs[left]);
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    // W: forgets to decrement the outgoing frequency — the map only ever
    // grows, so the window never shrinks and the answer inflates to the
    // longest run with AT MOST one distinct value... plus stale counts.
    public static int longestWindow(int[] xs, int k) {
        if (xs == null || xs.length == 0 || k <= 0) return 0;
        Map<Integer, Integer> freq = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < xs.length; right++) {
            freq.merge(xs[right], 1, Integer::sum);
            while (freq.size() > k) left++;   // map not updated!
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
}
""",
        ),
        (
            CH_P13_PREFIX["id"],
            r"""
import java.util.*;

public class Solution {
    public static long[] prefixSums(int[] xs) {
        long[] pre = new long[xs.length + 1];
        for (int i = 0; i < xs.length; i++) pre[i + 1] = pre[i] + xs[i];
        return pre;
    }

    public static long rangeSum(long[] pre, int l, int r) {
        return pre[r] - pre[l];
    }

    public static int countSubarraysWithSum(int[] xs, int target) {
        Map<Long, Integer> seen = new HashMap<>();
        seen.put(0L, 1);
        long running = 0;
        int count = 0;
        for (int x : xs) {
            running += x;
            count += seen.getOrDefault(running - target, 0);
            seen.merge(running, 1, Integer::sum);
        }
        return count;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static long[] prefixSums(int[] xs) {
        long[] pre = new long[xs.length + 1];
        for (int i = 0; i < xs.length; i++) pre[i + 1] = pre[i] + xs[i];
        return pre;
    }

    public static long rangeSum(long[] pre, int l, int r) {
        return pre[r] - pre[l];
    }

    // W: counts subarrays with sum AT LEAST target instead of EXACTLY —
    // every near-miss range inflates the count.
    public static int countSubarraysWithSum(int[] xs, int target) {
        int count = 0;
        for (int i = 0; i < xs.length; i++) {
            long s = 0;
            for (int j = i; j < xs.length; j++) {
                s += xs[j];
                if (s >= target) count++;
            }
        }
        return count;
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — algorithms

You can now: reason in pointers and windows, find monotonic boundaries
in log time, and reach for the auxiliary map before reaching for a
nested loop. Prove it with a diagnostic pair.
"""

CP_MDX_VI = r"""
## Checkpoint — thuật toán

Giờ bạn có thể: suy luận bằng pointer và window, tìm biên đơn điệu trong
log n, và với tới map phụ trợ trước khi với tới vòng lặp lồng. Chứng minh
bằng một cặp bài chẩn đoán.
"""

CH_CP13 = challenge(
    "javi-checkpoint-m13-algorithms",
    "Diagnosis Pair",
    r"""Two independent problems in `Solution`:

1. `static int lowerBound(int[] sorted, int target)` — first index with
   `sorted[i] >= target` via the half-open binary search; returning
   `sorted.length` means none. (Not indexOf: duplicates must find the
   FIRST.)

2. `static boolean hasMajority(int[] xs)` — true when some value occurs
   more than n/2 times, via one frequency-map pass (no sorting).

[1,2,2,2,3], lowerBound(2) → 1 (not 2 — the first).
[2,2,1,1], hasMajority → false: 1 appears twice, n/2 = 2, needs MORE
than 2 → false. [1,1,1,2] → true: 3 of 4.""",
    r"""
import java.util.*;

public class Solution {
    // Provide lowerBound + hasMajority here.
}
""",
    [
        (
            "lower bound finds first",
            r"""
checkEq(Solution.lowerBound(new int[]{1, 2, 2, 2, 3}, 2), 1, "first 2");
checkEq(Solution.lowerBound(new int[]{1, 2, 2, 2, 3}, 4), 5, "past end");
""",
            "Duplicates → leftmost qualifying index; too-big target → length.",
        ),
        (
            "lower bound smaller than all",
            r"""
checkEq(Solution.lowerBound(new int[]{10, 20}, 5), 0, "everything qualifies");
""",
            "Index 0 is the first ≥ 5.",
        ),
        (
            "majority detection",
            r"""
checkEq(Solution.hasMajority(new int[]{1, 1, 1, 2}), true, "3 of 4");
checkEq(Solution.hasMajority(new int[]{2, 2, 1, 1}), false, "2 of 4 is not > 2");
""",
            "Strictly more than n/2 occurrences.",
        ),
        (
            "majority edge cases",
            r"""
checkEq(Solution.hasMajority(new int[]{7}), true, "single element");
checkEq(Solution.hasMajority(new int[]{}), false, "empty");
""",
            "n=1 → the element counts; empty → false.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CH_CP13 = vi_challenge(
    "Cặp bài chẩn đoán",
    r"""Hai bài độc lập trong `Solution`:

1. `static int lowerBound(int[] sorted, int target)` — chỉ số đầu với
   `sorted[i] >= target` qua binary search khoảng nửa mở; trả
   `sorted.length` nghĩa là không có. (Không phải indexOf: giá trị trùng
   phải tìm cái ĐẦU.)

2. `static boolean hasMajority(int[] xs)` — true khi một giá trị xuất
   hiện nhiều hơn n/2 lần, qua một lượt đếm tần suất (không sort).

[1,2,2,2,3], lowerBound(2) → 1 (không phải 2 — cái đầu).
checkEq(Solution.hasMajority(new int[]{2, 2, 1, 1}), false, "2 of 4 is not > 2");""",
    [
        ("Lower bound tìm cái đầu", "Trùng giá trị → chỉ số trái nhất; target quá lớn → độ dài mảng."),
        ("Lower bound nhỏ hơn tất cả", "Chỉ số 0 là cái đầu ≥ 5."),
        ("Dò phần tử đa số", "Nghiêm ngặt hơn n/2 lần xuất hiện."),
        ("Biên của đa số", "n=1 → phần tử đó đếm; rỗng → false."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-algorithms",
    "Checkpoint: Algorithms",
    "Graded checkpoint: a boundary-faithful lower bound and a one-pass majority detector.",
    15,
    CP_MDX,
    "Checkpoint: Thuật toán",
    "Checkpoint chấm điểm: lower bound trung thành với biên và bộ dò đa số một lượt.",
    CP_MDX_VI,
    CH_CP13,
    VI_CH_CP13,
    solution=r"""
import java.util.*;

public class Solution {
    public static int lowerBound(int[] sorted, int target) {
        int lo = 0, hi = sorted.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (sorted[mid] >= target) hi = mid; else lo = mid + 1;
        }
        return lo;
    }

    public static boolean hasMajority(int[] xs) {
        if (xs == null || xs.length == 0) return false;
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : xs) {
            int c = freq.merge(x, 1, Integer::sum);
            if (c * 2 > xs.length) return true;
        }
        return false;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    // W: lowerBound returns the FIRST EQUAL match (like indexOf) — with
    // duplicates it reports the first x == target, not the first
    // x >= target, missing leftward qualifying values.
    public static int lowerBound(int[] sorted, int target) {
        for (int i = 0; i < sorted.length; i++) {
            if (sorted[i] == target) return i;
        }
        return sorted.length;
    }

    public static boolean hasMajority(int[] xs) {
        if (xs == null || xs.length == 0) return false;
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : xs) {
            int c = freq.merge(x, 1, Integer::sum);
            if (c * 2 > xs.length) return true;
        }
        return false;
    }
}
""",
)
