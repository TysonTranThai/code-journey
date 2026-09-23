#!/usr/bin/env python3
"""AP CSA M17 — Algorithmic reasoning: iteration counting, O(n) vs O(n^2), choosing algorithms."""
from apc import *

M = "apc-reasoning"

L1 = r"""
**Algorithmic reasoning** = predicting what code does and what it
costs, before running it. The exam's favorite costs:

- **O(1)** — constant: one comparison, one assignment. Array indexing
  `a[5]` is O(1) no matter how big `a` is.
- **O(n)** — linear: work grows in step with the input. One pass over
  `n` elements (sum, max, count) is O(n).
- **O(n²)** — quadratic: a loop **inside** a loop, each over n. All
  pairs, all grid cells, most "compare everything to everything"
  algorithms. 100 elements → 10,000 steps; 10,000 elements →
  100,000,000 steps. Quadratic code is the one that times out.

```java
for (int i = 0; i < n; i++) {        // n times
    for (int j = 0; j < n; j++) {    // n times each → n * n total
        // O(n^2)
    }
}
```

Logarithmic intuition: binary search halves the remaining range each
step, so 1,000,000 elements need ~20 steps. You only need the
*intuition* on this exam — halving beats scanning.
"""

L2 = r"""
Counting iterations exactly — the trace skill applied to loops:

```java
int total = 0;
for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
        total++;            // how many times?
    }
}
```

The inner loop depends on the outer one: for `i = 0` it runs `n-1`
times, `i = 1` → `n-2`, ..., total `n(n-1)/2` — still O(n²), but
**half** the work. Two loops over the same n in sequence is `n + n =
2n` — linear. Two loops **nested** is `n * n`. The shape of the
nesting decides the class, not the number of loops.

The other counting traps:

- `j < n` vs `j <= n` — one iteration difference, one test difference.
- Inner bound `j < i` vs `j < n` — triangle vs square.
- Loop variables mutated **inside** the body — the iteration count
  changes; trace it, don't pattern-match.
"""

L3 = r"""
**Choosing an algorithm** — matching the tool to the constraint:

- Need the max/min/sum of an array? One pass — O(n). Nothing better
  exists (you must look at every element at least once).
- Need to know whether a value is present in an **unsorted** array?
  Linear scan, O(n).
- Same question, **sorted** array? Binary search, O(log n) — but only
  because sortedness lets you discard half each step.
- Need all pairs? That's n² by nature; the trick is usually to *avoid*
  needing all pairs.

```java
// sorted: discards half each step — unsorted: cannot
while (lo <= hi) {
    int mid = (lo + hi) / 2;
    if (a[mid] == target) return mid;
    if (a[mid] < target) lo = mid + 1;
    else hi = mid - 1;
}
return -1;
```

The exam phrases this as "which algorithm is most appropriate" —
answer by naming what the data guarantees (sorted or not) and what
the question needs (one value? all pairs? a position?). Guarantees
are what you buy complexity savings with.
"""

write_module(
    M,
    "Algorithmic Reasoning",
    "Iteration counting, complexity classes O(n) and O(n squared), and matching algorithms to data guarantees.",
    "Lý giải thuật toán",
    "Đếm vòng lặp, các lớp độ phức tạp O(n) và O(n bình), và chọn thuật toán theo tính chất dữ liệu.",
    lessons=["apc-m17-classes", "apc-m17-counting", "apc-m17-choosing", "apc-cp-m17"],
    practices=["apc-p17-reasoning"],
)

write_lesson(
    M, "apc-m17-classes", "Complexity classes",
    "O(1), O(n), O(n squared); why nesting decides the class; logarithmic intuition.",
    10, L1,
    "Các lớp độ phức tạp",
    "O(1), O(n), O(n bình); vì sao cấu trúc lồng quyết định lớp; trực giác logarit.",
    r"""
**Lý giải thuật toán** = đoán trước mã làm gì và tốn bao nhiêu, trước
khi chạy. Các mức chi phí được đề yêu thích:

- **O(1)** — hằng: một so sánh, một phép gán. Truy cập mảng `a[5]` là
  O(1) bất kể `a` to cỡ nào.
- **O(n)** — tuyến tính: công việc tăng theo đúng đầu vào. Một lượt
  qua `n` phần tử (tổng, max, đếm) là O(n).
- **O(n²)** — bậc hai: một vòng lặp **bên trong** một vòng lặp, mỗi
  vòng trên n. Tất cả các cặp, mọi ô lưới, đa số thuật toán "so mọi
  thứ với mọi thứ". 100 phần tử → 10.000 bước; 10.000 phần tử →
  100.000.000 bước. Mã bậc hai chính là mã bị timeout.

```java
for (int i = 0; i < n; i++) {        // n lần
    for (int j = 0; j < n; j++) {    // n lần mỗi lần → n * n tổng
        // O(n^2)
    }
}
```

Trực giác logarit: tìm kiếm nhị phân chia đôi phạm vi còn lại mỗi
bước, nên 1.000.000 phần tử chỉ cần ~20 bước. Bạn chỉ cần *trực giác*
cho kỳ thi này — chia đôi thắng quét tuyến tính.
""",
)

write_lesson(
    M, "apc-m17-counting", "Counting iterations",
    "Dependent inner bounds, triangle vs square, sequential vs nested loops.",
    12, L2,
    "Đếm số vòng lặp",
    "Cận trong phụ thuộc, tam giác so với vuông, tuần tự so với lồng nhau.",
    r"""
Đếm số vòng lặp chính xác — kỹ năng truy vết áp dụng cho vòng lặp:

```java
int total = 0;
for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
        total++;            // chạy bao nhiêu lần?
    }
}
```

Vòng trong phụ thuộc vòng ngoài: với `i = 0` nó chạy `n-1` lần,
`i = 1` → `n-2`, ..., tổng `n(n-1)/2` — vẫn O(n²), nhưng chỉ **một
nửa** công việc. Hai vòng trên cùng n đặt TUẦN TỰ là `n + n = 2n` —
tuyến tính. Hai vòng **lồng nhau** là `n * n`. Hình dạng của sự lồng
quyết định lớp, không phải số vòng lặp.

Các bẫy đếm còn lại:

- `j < n` so với `j <= n` — khác một vòng lặp, khác một test.
- Cận trong `j < i` so với `j < n` — tam giác so với vuông.
- Biến vòng lặp bị thay đổi **bên trong thân** — số vòng thay đổi;
  truy vết, đừng bắt mẫu hình.
""",
)

write_lesson(
    M, "apc-m17-choosing", "Choosing an algorithm",
    "Match the tool to the guarantee: sorted vs unsorted, one value vs all pairs.",
    10, L3,
    "Chọn thuật toán",
    "Ghép công cụ với tính chất: có thứ tự hay không, một giá trị hay mọi cặp.",
    r"""
**Chọn thuật toán** — ghép công cụ với ràng buộc:

- Cần max/min/tổng của mảng? Một lượt — O(n). Không gì nhanh hơn được
  (bắt buộc phải nhìn mỗi phần tử ít nhất một lần).
- Cần biết một giá trị có mặt trong mảng **chưa sắp**? Quét tuyến
  tính, O(n).
- Cùng câu hỏi, mảng **đã sắp**? Tìm kiếm nhị phân, O(log n) — nhưng
  chỉ vì tính có thứ tự cho phép bỏ nửa phạm vi mỗi bước.
- Cần mọi cặp? Bản chất là n²; mẹo thường là *tránh* cần mọi cặp.

```java
// đã sắp: bỏ nửa mỗi bước — chưa sắp: không thể
while (lo <= hi) {
    int mid = (lo + hi) / 2;
    if (a[mid] == target) return mid;
    if (a[mid] < target) lo = mid + 1;
    else hi = mid - 1;
}
return -1;
```

Đề diễn đạt điều này thành "thuật toán nào phù hợp nhất" — trả lời
bằng cách gọi tên những gì dữ liệu bảo đảm (đã sắp hay chưa) và câu
hỏi cần gì (một giá trị? mọi cặp? một vị trí?). Tính chất bảo đảm là
thứ bạn dùng để đổi lấy tiết kiệm độ phức tạp.
""",
)

BOILER_SUMN = r"""public class Solution {
    public static long sumTo(long n) {
        // complete: 1 + 2 + ... + n  (must handle large n efficiently)
        return 0;
    }
}
"""

BOILER_PAIRS = r"""public class Solution {
    public static int countPairs(int[] a) {
        // complete: number of index pairs i < j with a[i] == a[j]
        return 0;
    }
}
"""

BOILER_BSEARCH = r"""public class Solution {
    public static int binarySearch(int[] sorted, int target) {
        // complete: index of target in the SORTED array, or -1
        return -1;
    }
}
"""

BOILER_FIXSEQ = r"""public class Solution {
    public static int twiceMax(int[] a) {
        // BUG: original flaw kept — the second loop re-scans from 0
        // and doubles the FIRST element instead of returning 2 * max
        int max = a[0];
        for (int x : a) {
            if (x > max) {
                max = x;
            }
        }
        for (int i = 0; i < a.length; i++) {
            if (a[i] == max) {
                return a[0] * 2;
            }
        }
        return -1;
    }
}
"""

CP17 = r"""public class Solution {
    public static int missingNumber(int[] a) {
        // complete: a holds n distinct values from 0..n with exactly
        // one missing; return the missing value (one pass)
        return 0;
    }
}
"""

P_SUMN = challenge(
    "apc-m17-sumn",
    "Sum without the loop",
    "Implement `sumTo(long n)`: return 1 + 2 + ... + n. A loop works for small n but the formula `n * (n + 1) / 2` works for any n — use it (watch: n * (n + 1) can overflow int, use long).",
    BOILER_SUMN,
    [(
        "large n",
        r"""
CjTestBase.checkEq(Solution.sumTo(5), 15L, "small case");
CjTestBase.checkEq(Solution.sumTo(1), 1L, "one term");
CjTestBase.checkEq(Solution.sumTo(100000L), 5000050000L, "large n, no overflow");
""",
        "return n * (n + 1) / 2; with long arithmetic throughout.",
    )],
    level="guided",
)

P_PAIRS = challenge(
    "apc-m17-pairs",
    "Count equal pairs",
    "Implement `countPairs(int[] a)`: count index pairs `i < j` where `a[i] == a[j]`. The double loop over i then j (starting at i + 1) is the honest O(n squared) approach — fine here.",
    BOILER_PAIRS,
    [(
        "duplicates",
        r"""
CjTestBase.checkEq(Solution.countPairs(new int[] {1, 1, 1}), 3, "three 1s: pairs (0,1) (0,2) (1,2)");
CjTestBase.checkEq(Solution.countPairs(new int[] {1, 2, 3}), 0, "all distinct");
CjTestBase.checkEq(Solution.countPairs(new int[] {}), 0, "empty");
""",
        "inner loop starts at i + 1, not 0 — otherwise pairs count twice.",
    )],
    level="independent",
)

P_BSEARCH = challenge(
    "apc-m17-bsearch",
    "Binary search",
    "Implement `binarySearch(int[] sorted, int target)`: return the index of target (the array IS sorted ascending), or -1 if absent. Halve the range each step — do not scan.",
    BOILER_BSEARCH,
    [(
        "present and absent",
        r"""
int[] a = {2, 5, 8, 12, 16, 23, 38};
CjTestBase.checkEq(Solution.binarySearch(a, 16), 4, "middle hit");
CjTestBase.checkEq(Solution.binarySearch(a, 2), 0, "first element");
CjTestBase.checkEq(Solution.binarySearch(a, 38), 6, "last element");
CjTestBase.checkEq(Solution.binarySearch(a, 9), -1, "absent in range");
CjTestBase.checkEq(Solution.binarySearch(new int[] {}, 1), -1, "empty");
""",
        "lo + (hi - lo) style midpoint; loop while lo <= hi.",
    )],
    level="independent",
)

P_FIXSEQ = challenge(
    "apc-m17-fix-seq",
    "Debug: doubled max",
    "`twiceMax(int[] a)` should return `2 *` the largest element. It compiles, always terminates, and returns 2 * a[0] whenever the max exists — wrong whenever the max is not first. Repair it (keep the two-loop shape if you like).",
    BOILER_FIXSEQ,
    [(
        "max repaired",
        r"""
CjTestBase.checkEq(Solution.twiceMax(new int[] {3, 9, 4}), 18, "max not first");
CjTestBase.checkEq(Solution.twiceMax(new int[] {5}), 10, "single element");
CjTestBase.checkEq(Solution.twiceMax(new int[] {-7, -2}), -4, "negatives");
""",
        "return max * 2; the second loop only needed to FIND it.",
    )],
    level="debugging",
)

CP17C = challenge(
    "apc-cp-m17-missing",
    "Checkpoint: the missing number",
    "`a` holds n distinct values taken from 0..n with exactly one value missing. Implement `missingNumber(int[] a)`: return the missing value, in one pass (O(n)) — the expected sum trick.",
    CP17,
    [(
        "one pass",
        r"""
CjTestBase.checkEq(Solution.missingNumber(new int[] {3, 0, 1}), 2, "middle gap");
CjTestBase.checkEq(Solution.missingNumber(new int[] {0, 1}), 2, "missing at the end");
CjTestBase.checkEq(Solution.missingNumber(new int[] {1}), 0, "missing zero");
""",
        "expected = n*(n+1)/2 for n == a.length; subtract the actual sum.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p17-reasoning", "Algorithmic reasoning reps", "Formula vs loop, equal pairs, binary search, max repair, sum trick.",
    "Luyện lý giải thuật toán", "Công thức thay vòng lặp, cặp bằng nhau, tìm nhị phân, sửa max, mẹo tổng.",
    after_lesson="apc-m17-choosing", minutes=55, difficulty="beginner",
    challenges=[P_SUMN, P_PAIRS, P_BSEARCH, P_FIXSEQ],
    vi_challenges={
        "apc-m17-sumn": vi_challenge("Tổng không cần vòng lặp", "Cài đặt `sumTo(long n)`: trả 1 + 2 + ... + n. Vòng lặp ổn với n nhỏ nhưng công thức `n * (n + 1) / 2` đúng với mọi n — hãy dùng nó (chú ý: n * (n + 1) có thể tràn int, dùng long).",
            [("large n", "return n * (n + 1) / 2; với số học long xuyên suốt.")]),
        "apc-m17-pairs": vi_challenge("Đếm cặp bằng nhau", "Cài đặt `countPairs(int[] a)`: đếm các cặp chỉ số `i < j` sao cho `a[i] == a[j]`. Vòng kép i rồi j (bắt đầu từ i + 1) là cách O(n bình) trung thực — ổn ở đây.",
            [("duplicates", "vòng trong bắt đầu từ i + 1, không phải 0 — nếu không mỗi cặp bị đếm hai lần.")]),
        "apc-m17-bsearch": vi_challenge("Tìm kiếm nhị phân", "Cài đặt `binarySearch(int[] sorted, int target)`: trả chỉ số của target (mảng ĐÃ sắp tăng dần), hoặc -1 nếu vắng mặt. Chia đôi phạm vi mỗi bước — đừng quét.",
            [("present and absent", "điểm giữa dạng lo + (hi - lo); lặp trong khi lo <= hi.")]),
        "apc-m17-fix-seq": vi_challenge("Gỡ lỗi: max nhân đôi", "`twiceMax(int[] a)` phải trả `2 *` phần tử lớn nhất. Nó biên dịch, luôn kết thúc, và trả 2 * a[0] khi max tồn tại — sai bất cứ khi nào max không đứng đầu. Sửa lại (giữ hình dạng hai vòng nếu muốn).",
            [("max repaired", "return max * 2; vòng hai chỉ cần TÌM nó.")]),
    },
    solutions=[
        ("apc-m17-sumn", r"""public class Solution {
    public static long sumTo(long n) {
        return n * (n + 1) / 2;
    }
}
""", r"""public class Solution {
    public static long sumTo(long n) {
        // BUG: casts to int BEFORE multiplying — int * int overflows
        // for large n even though the method returns long
        return (int) n * (int) (n + 1) / 2;
    }
}
"""),
        ("apc-m17-pairs", r"""public class Solution {
    public static int countPairs(int[] a) {
        int count = 0;
        for (int i = 0; i < a.length; i++) {
            for (int j = i + 1; j < a.length; j++) {
                if (a[i] == a[j]) {
                    count++;
                }
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    public static int countPairs(int[] a) {
        // BUG: inner loop starts at 0, so each equal pair is counted
        // twice (i,j) and (j,i)
        int count = 0;
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < a.length; j++) {
                if (i != j && a[i] == a[j]) {
                    count++;
                }
            }
        }
        return count;
    }
}
"""),
        ("apc-m17-bsearch", r"""public class Solution {
    public static int binarySearch(int[] sorted, int target) {
        int lo = 0;
        int hi = sorted.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (sorted[mid] == target) {
                return mid;
            }
            if (sorted[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return -1;
    }
}
""", r"""public class Solution {
    public static int binarySearch(int[] sorted, int target) {
        // BUG: loop runs while lo < hi with hi = mid - 1 — the range
        // collapses before the last candidate is examined, so the first
        // and last elements are never found
        int lo = 0;
        int hi = sorted.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (sorted[mid] == target) {
                return mid;
            }
            if (sorted[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return -1;
    }
}
"""),
        ("apc-m17-fix-seq", r"""public class Solution {
    public static int twiceMax(int[] a) {
        int max = a[0];
        for (int x : a) {
            if (x > max) {
                max = x;
            }
        }
        return max * 2;
    }
}
""", r"""public class Solution {
    public static int twiceMax(int[] a) {
        // BUG: original flaw kept — the second loop re-scans from 0
        // and doubles the FIRST element instead of returning 2 * max
        int max = a[0];
        for (int x : a) {
            if (x > max) {
                max = x;
            }
        }
        for (int i = 0; i < a.length; i++) {
            if (a[i] == max) {
                return a[0] * 2;
            }
        }
        return -1;
    }
}
"""),
        ("apc-cp-m17-missing", r"""public class Solution {
    public static int missingNumber(int[] a) {
        int n = a.length;
        long expected = (long) n * (n + 1) / 2;
        long actual = 0;
        for (int x : a) {
            actual += x;
        }
        return (int) (expected - actual);
    }
}
""", r"""public class Solution {
    public static int missingNumber(int[] a) {
        // BUG: sums indices instead of values — expected - actual is
        // meaningless noise
        int n = a.length;
        long expected = (long) n * (n + 1) / 2;
        long actual = 0;
        for (int i = 0; i < n; i++) {
            actual += i;
        }
        return (int) (expected - actual);
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m17", "Checkpoint: the missing number",
    "The sum trick: O(n), one pass, overflow-safe arithmetic.",
    25,
    r"""
The pattern: turn a search problem into arithmetic. The expected sum
of 0..n is n(n+1)/2; whatever is missing from the actual sum IS the
answer. Note the two traps the W commits: summing the wrong thing,
and letting n*(n+1) overflow int before the long division.
""",
    "Điểm kiểm tra: số còn thiếu",
    "Mẹo tổng: O(n), một lượt, số học an toàn tràn.",
    r"""
Mẫu hình: biến bài tìm kiếm thành phép toán. Tổng mong đợi của 0..n
là n(n+1)/2; phần thiếu trong tổng thực tế CHÍNH LÀ đáp án. Chú ý hai
bẫy mà W mắc: cộng nhầm thứ, và để n*(n+1) tràn int trước phép chia
long.
""",
    CP17C,
    vi_challenge("Điểm kiểm tra: số còn thiếu", "`a` chứa n giá trị phân biệt rút từ 0..n với đúng một giá trị thiếu. Cài đặt `missingNumber(int[] a)`: trả giá trị thiếu, trong một lượt (O(n)) — dùng mẹo tổng mong đợi.",
        [("one pass", "expected = n*(n+1)/2 với n == a.length; trừ đi tổng thực tế.")]),
    solution=r"""public class Solution {
    public static int missingNumber(int[] a) {
        int n = a.length;
        long expected = (long) n * (n + 1) / 2;
        long actual = 0;
        for (int x : a) {
            actual += x;
        }
        return (int) (expected - actual);
    }
}
""",
    wrong=r"""public class Solution {
    public static int missingNumber(int[] a) {
        // BUG: sums indices instead of values — expected - actual is
        // meaningless noise
        int n = a.length;
        long expected = (long) n * (n + 1) / 2;
        long actual = 0;
        for (int i = 0; i < n; i++) {
            actual += i;
        }
        return (int) (expected - actual);
    }
}
""",
)
