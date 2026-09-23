#!/usr/bin/env python3
"""AP CSA M11 — Searching and Sorting (linear, binary, selection, insertion)."""
from apc import *

M = "apc-searchsort"

L1 = r"""
**Linear search** checks every element until it finds the target — O(n):

```java
public static int search(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}
```

**Binary search** halves the range each step — but requires a **sorted**
array. O(log n):

```java
public static int binarySearch(int[] arr, int target) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            lo = mid + 1;       // target is in the right half
        } else {
            hi = mid - 1;       // target is in the left half
        }
    }
    return -1;
}
```

Trace `binarySearch({2, 5, 8, 12, 16}, 12)`: lo=0 hi=4 mid=2 (8 < 12, go
right) → lo=3 hi=4 mid=3 → found at 3. Two steps instead of four scans.

The **invariant** to recite: at every loop entry, if target is present, it
lies in arr[lo..hi]. The loop ends when lo > hi — the range is empty — so
absence is proven, not guessed.
"""

L2 = r"""
**Selection sort** — find the smallest remaining, swap it into place:

```java
for (int i = 0; i < arr.length - 1; i++) {
    int min = i;
    for (int j = i + 1; j < arr.length; j++) {
        if (arr[j] < arr[min]) {
            min = j;
        }
    }
    int temp = arr[i];
    arr[i] = arr[min];
    arr[min] = temp;
}
```

Trace {5, 2, 8, 1}: pass 1 finds 1 (index 3), swaps → {1, 2, 8, 5}; pass 2
finds 2, already in place → {1, 2, 8, 5}; pass 3 finds 5 → {1, 2, 5, 8}.
After pass k, the first k elements are final.

**Insertion sort** — grow a sorted prefix; each new element walks left to
its slot (like sorting playing cards in your hand):

```java
for (int i = 1; i < arr.length; i++) {
    int key = arr[i];
    int j = i - 1;
    while (j >= 0 && arr[j] > key) {
        arr[j + 1] = arr[j];    // shift right
        j--;
    }
    arr[j + 1] = key;           // drop into the gap
}
```

Both are O(n²). The exam asks you to *trace* a couple of passes and count
comparisons/swaps — selection sort always does the full inner scan; insertion
sort stops early on nearly-sorted data.
"""

L3 = r"""
Tracing rules the exam drills:

**Selection sort pass k**: (1) scan from index k to the end for the minimum,
(2) one swap at the end. Comparisons in a pass: `n - k - 1`. Total swaps:
exactly n − 1 (or fewer if an element swaps with itself — usually counted as
n − 1 passes).

**Insertion sort**: element k is inserted into the sorted prefix 0..k−1.
The number of shifts for element k equals the number of prefix elements
greater than it. A sorted array does zero shifts (fast); a reverse-sorted
array does the maximum.

**Binary search on even-length ranges**: `mid = (lo + hi) / 2` rounds down,
so for lo=0, hi=3, mid=1 (the *left* middle). The exam expects you to use
exactly this convention.

**When to use which search**: data sorted → binary search; unsorted or
tiny → linear. Searching an *unsorted* array with binary search silently
returns wrong answers — not an error, which is exactly what makes the
multiple-choice version dangerous.
"""

write_module(
    M,
    "Searching and Sorting",
    "Linear vs binary search, the sorted-array invariant, selection and insertion sort with hand traces.",
    "Tìm kiếm và sắp xếp",
    "Tìm tuyến tính so với nhị phân, bất biến mảng đã sắp, sắp xếp chọn và chèn với truy vết tay.",
    lessons=["apc-m11-search", "apc-m11-sort", "apc-m11-trace", "apc-cp-m11"],
    practices=["apc-p11-searchsort"],
)

write_lesson(
    M, "apc-m11-search", "Linear and binary search",
    "Two search algorithms, the sorted invariant, halving the range.",
    14, L1,
    "Tìm tuyến tính và nhị phân",
    "Hai thuật toán tìm kiếm, bất biến mảng đã sắp, chia đôi khoảng.",
    r"""
**Tìm tuyến tính** kiểm tra từng phần tử cho tới khi gặp mục tiêu — O(n):

```java
public static int search(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}
```

**Tìm nhị phân** chia đôi khoảng mỗi bước — nhưng đòi hỏi mảng **đã sắp**.
O(log n):

```java
public static int binarySearch(int[] arr, int target) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            lo = mid + 1;       // mục tiêu ở nửa phải
        } else {
            hi = mid - 1;       // mục tiêu ở nửa trái
        }
    }
    return -1;
}
```

Truy vết `binarySearch({2, 5, 8, 12, 16}, 12)`: lo=0 hi=4 mid=2 (8 < 12, sang
phải) → lo=3 hi=4 mid=3 → thấy tại 3. Hai bước thay vì bốn lần quét.

**Bất biến** cần thuộc: ở mỗi lần vào vòng lặp, nếu mục tiêu có mặt thì nó
nằm trong arr[lo..hi]. Vòng lặp kết thúc khi lo > hi — khoảng rỗng — nên sự
vắng mặt được chứng minh, không phải đoán.
""",
)

write_lesson(
    M, "apc-m11-sort", "Selection and insertion sort",
    "Two quadratic sorts, the algorithms, and their behavior.",
    14, L2,
    "Sắp xếp chọn và chèn",
    "Hai thuật toán bậc hai, bản chất thuật toán, và hành vi của chúng.",
    r"""
**Sắp xếp chọn** — tìm phần tử nhỏ nhất còn lại, hoán đổi vào chỗ:

```java
for (int i = 0; i < arr.length - 1; i++) {
    int min = i;
    for (int j = i + 1; j < arr.length; j++) {
        if (arr[j] < arr[min]) {
            min = j;
        }
    }
    int temp = arr[i];
    arr[i] = arr[min];
    arr[min] = temp;
}
```

Truy vết {5, 2, 8, 1}: lượt 1 tìm 1 (chỉ số 3), hoán đổi → {1, 2, 8, 5};
lượt 2 tìm 2, đã đúng chỗ → {1, 2, 8, 5}; lượt 3 tìm 5 → {1, 2, 5, 8}. Sau
lượt k, k phần tử đầu đã cố định.

**Sắp xếp chèn** — nuôi một tiền tố đã sắp; mỗi phần tử mới đi sang trái tới
chỗ của nó (như xếp bài trên tay):

```java
for (int i = 1; i < arr.length; i++) {
    int key = arr[i];
    int j = i - 1;
    while (j >= 0 && arr[j] > key) {
        arr[j + 1] = arr[j];    // dịch phải
        j--;
    }
    arr[j + 1] = key;           // thả vào khoảng trống
}
```

Cả hai là O(n²). Đề thi yêu cầu *truy vết* vài lượt và đếm phép so
sánh/hoán đổi — sắp xếp chọn luôn quét hết vòng trong; sắp xếp chèn dừng
sớm trên dữ liệu gần như đã sắp.
""",
)

write_lesson(
    M, "apc-m11-trace", "Tracing rules and trade-offs",
    "Comparison counts, the mid-rounding convention, choosing a search.",
    10, L3,
    "Luật truy vết và sự đánh đổi",
    "Số phép so sánh, quy ước làm tròn mid, chọn thuật toán tìm kiếm.",
    r"""
Các luật truy vết đề thị rèn:

**Sắp xếp chọn lượt k**: (1) quét từ chỉ số k tới cuối tìm minimum, (2) một
hoán đổi ở cuối. Số so sánh trong lượt: `n - k - 1`. Tổng số hoán đổi: đúng
n − 1 (hoặc ít hơn nếu phần tử tự hoán đổi với chính nó — thường tính là n −
1 lượt).

**Sắp xếp chèn**: phần tử k được chèn vào tiền tố đã sắp 0..k−1. Số lần dịch
của phần tử k bằng số phần tử trong tiền tố lớn hơn nó. Mảng đã sắp thực hiện
không lần dịch nào (nhanh); mảng đảo ngược thực hiện tối đa.

**Tìm nhị phân trên khoảng chẵn**: `mid = (lo + hi) / 2` làm tròn xuống, nên
với lo=0, hi=3, mid=1 (giữa *bên trái*). Đề thi yêu cầu dùng đúng quy ước
này.

**Khi nào dùng tìm nào**: dữ liệu đã sắp → nhị phân; chưa sắp hoặc rất nhỏ →
tuyến tính. Tìm nhị phân trên mảng *chưa sắp* âm thầm trả về đáp án sai —
không phải lỗi, và chính điều đó làm phiên bản trắc nghiệm nguy hiểm.
""",
)

BOILER_LIN = r"""public class Solution {
    public static int search(String[] arr, String target) {
        return -1; // replace
    }
}
"""

BOILER_BIN = r"""public class Solution {
    public static int binarySearch(int[] arr, int target) {
        return -1; // replace; arr is sorted ascending, no duplicates
    }
}
"""

BOILER_SEL = r"""public class Solution {
    public static int[] selectionSort(int[] arr) {
        return arr; // replace: sort a NEW array ascending
    }
}
"""

BOILER_INS = r"""public class Solution {
    public static int insertionShifts(int[] arr) {
        return 0; // replace: total shifts insertion sort would do
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static int find(int[] arr, int target) {
        int lo = 0;
        int hi = arr.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }
        return -1;
    }
}
"""

CP11 = r"""public class Solution {
    public static int[] sortNames(int[] keys) {
        // replace: return a new array sorted ascending by (value % 10), ties broken
        // by original order (stable) — i.e. insertion sort on (value % 10)
        return keys;
    }
}
"""

P_LIN = challenge(
    "apc-m11-linsearch",
    "Linear search on Strings",
    "Implement `int search(String[] arr, String target)`: the first index whose element equals target (use .equals!), or -1.",
    BOILER_LIN,
    [        ("finds and misses", r"""
String pooled = "b";              // interned literal
String fresh = new String("b");   // equal, but a different object
CjTestBase.checkEq(Solution.search(new String[]{"a", "b", "c"}, pooled), 1, "middle");
CjTestBase.checkEq(Solution.search(new String[]{"a", "b", "c"}, fresh), 1, "equals sees through new String");
CjTestBase.checkEq(Solution.search(new String[]{"a", "b"}, "z"), -1, "absent");
CjTestBase.checkEq(Solution.search(new String[]{}, "a"), -1, "empty");
""",
        "Compare with equals, not == — new String(\"b\") is equal but not identical.",
    )],
    level="imitation",
)

P_BIN = challenge(
    "apc-m11-binsearch",
    "Binary search",
    "Implement `int binarySearch(int[] arr, int target)` on an ascending, duplicate-free array: the target's index or -1. Use the exam's exact loop (lo/hi/mid with mid = (lo+hi)/2).",
    BOILER_BIN,
    [(
        "binary verdicts",
        r"""
int[] a = {2, 5, 8, 12, 16, 23, 38};
CjTestBase.checkEq(Solution.binarySearch(a, 23), 5, "find late");
CjTestBase.checkEq(Solution.binarySearch(a, 2), 0, "find first");
CjTestBase.checkEq(Solution.binarySearch(a, 38), 6, "find last");
CjTestBase.checkEq(Solution.binarySearch(a, 9), -1, "absent inside range");
CjTestBase.checkEq(Solution.binarySearch(a, 1), -1, "absent below");
""",
        "lo + hi bounds, mid rounding down, move lo past mid or hi before mid.",
    )],
    level="guided",
)

P_SEL = challenge(
    "apc-m11-selectionsort",
    "Selection sort (new array)",
    "Implement `int[] selectionSort(int[] arr)`: return a NEW array sorted ascending, using selection sort. The input must stay unmodified (copy first).",
    BOILER_SEL,
    [(
        "sorted copy",
        r"""
int[] src = {5, 2, 8, 1};
int[] out = Solution.selectionSort(src);
CjTestBase.checkEq(out[0], 1, "min first");
CjTestBase.checkEq(out[3], 8, "max last");
CjTestBase.checkEq(src[0], 5, "input untouched");
CjTestBase.checkEq(Solution.selectionSort(new int[]{1})[0], 1, "single");
""",
        "Copy with a loop, then the classic select-min-and-swap passes.",
    )],
    level="combination",
)

P_INS = challenge(
    "apc-m11-insertionshifts",
    "Count insertion shifts",
    "Implement `int insertionShifts(int[] arr)`: the total number of shifts insertion sort would perform on arr — for each element, the number of earlier elements greater than it. Pure trace arithmetic, no sorting needed: for each i, count j < i with arr[j] > arr[i].",
    BOILER_INS,
    [(
        "shift arithmetic",
        r"""
CjTestBase.checkEq(Solution.insertionShifts(new int[]{1, 2, 3}), 0, "sorted: none");
CjTestBase.checkEq(Solution.insertionShifts(new int[]{3, 2, 1}), 3, "reverse: 2+1+0");
CjTestBase.checkEq(Solution.insertionShifts(new int[]{2, 3, 1}), 2, "3 dips, 1 dips twice");
""",
        "Sum over all pairs (j < i, arr[j] > arr[i]).",
    )],
    level="independent",
)

P_FIX = challenge(
    "apc-m11-fix-binary",
    "Debug the binary search",
    "This binary search returns wrong (or misses) answers on a sorted array. The algorithm's branch logic is inverted somewhere — trace `find({1, 3, 5, 7, 9}, 9)` by hand, find the flaw, and fix the branches (structure must stay a binary search).",
    BOILER_FIX,
    [(
        "binary repaired",
        r"""
int[] a = {1, 3, 5, 7, 9};
CjTestBase.checkEq(Solution.find(a, 9), 4, "last element");
CjTestBase.checkEq(Solution.find(a, 1), 0, "first element");
CjTestBase.checkEq(Solution.find(a, 5), 2, "middle");
CjTestBase.checkEq(Solution.find(a, 4), -1, "absent");
""",
        "arr[mid] < target means the target is RIGHT — lo = mid + 1.",
    )],
    level="debugging",
)

CP11C = challenge(
    "apc-cp-m11-sortkeys",
    "Checkpoint: sort by key digit",
    "Implement `int[] sortNames(int[] keys)`: return a new array sorted ascending by the last digit (value % 10); ties keep original order (stable — insertion sort does this naturally). keys is non-empty.",
    CP11,
    [        ("stable key sort", r"""
int[] out = Solution.sortNames(new int[]{31, 41, 22, 12});
CjTestBase.checkEq(out[0], 31, "digit-1 tie: 31 keeps its original lead");
CjTestBase.checkEq(out[1], 41, "digit-1 tie: 41 follows");
CjTestBase.checkEq(out[2], 22, "digit-2 tie: 22 first");
CjTestBase.checkEq(out[3], 12, "digit-2 tie: 12 last");
""",
        "Insertion sort comparing (a % 10) < (b % 10), shifting only on strict >.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p11-searchsort", "Search & sort reps", "Both searches, both sorts, shift arithmetic, branch debugging.",
    "Luyện tìm & sắp", "Cả hai phép tìm, cả hai thuật sắp, số học dịch, sửa nhánh.",
    after_lesson="apc-m11-sort", minutes=55, difficulty="beginner",
    challenges=[P_LIN, P_BIN, P_SEL, P_INS, P_FIX],
    vi_challenges={
        "apc-m11-linsearch": vi_challenge("Tìm tuyến tính trên String", "Cài đặt `int search(String[] arr, String target)`: chỉ số đầu tiên có phần tử bằng target (dùng .equals!), hoặc -1.",
            [("finds and misses", "So sánh bằng equals, không phải ==.")]),
        "apc-m11-binsearch": vi_challenge("Tìm nhị phân", "Cài đặt `int binarySearch(int[] arr, int target)` trên mảng tăng dần, không trùng: chỉ số của target hoặc -1. Dùng đúng vòng lặp của đề thi (lo/hi/mid với mid = (lo+hi)/2).",
            [("binary verdicts", "Chặn lo + hi, mid làm tròn xuống, dời lo qua mid hoặc hi về trước mid.")]),
        "apc-m11-selectionsort": vi_challenge("Sắp xếp chọn (mảng mới)", "Cài đặt `int[] selectionSort(int[] arr)`: trả về mảng MỚI đã sắp tăng dần, dùng sắp xếp chọn. Đầu vào không được bị sửa (sao chép trước).",
            [("sorted copy", "Sao chép bằng vòng lặp, rồi các lượt chọn-min-và-hoán đổi kinh điển.")]),
        "apc-m11-insertionshifts": vi_challenge("Đếm lần dịch của sắp chèn", "Cài đặt `int insertionShifts(int[] arr)`: tổng số lần dịch mà sắp xếp chèn sẽ thực hiện trên arr — với mỗi phần tử, đếm số phần tử đứng trước lớn hơn nó. Chỉ là số học truy vết, không cần sắp: với mỗi i, đếm j < i với arr[j] > arr[i].",
            [("shift arithmetic", "Tổng qua mọi cặp (j < i, arr[j] > arr[i]).")]),
        "apc-m11-fix-binary": vi_challenge("Sửa tìm nhị phân", "Tìm nhị phân này trả về kết quả sai (hoặc bỏ sót) trên mảng đã sắp. Logic nhánh bị đảo chỗ nào đó — truy vết tay `find({1, 3, 5, 7, 9}, 9)`, tìm khuyết tật, sửa các nhánh (cấu trúc vẫn phải là tìm nhị phân).",
            [("binary repaired", "arr[mid] < target nghĩa là mục tiêu ở PHẢI — lo = mid + 1.")]),
    },
    solutions=[
        ("apc-m11-linsearch", r"""public class Solution {
    public static int search(String[] arr, String target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i].equals(target)) {
                return i;
            }
        }
        return -1;
    }
}
""",
         r"""public class Solution {
    public static int search(String[] arr, String target) {
        // BUG: == compares references — literal vs new String misses
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
}
"""),
        ("apc-m11-binsearch", r"""public class Solution {
    public static int binarySearch(int[] arr, int target) {
        int lo = 0;
        int hi = arr.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return -1;
    }
}
""",
         r"""public class Solution {
    public static int binarySearch(int[] arr, int target) {
        // BUG: hi never shrinks below mid — infinite loop on misses? no:
        // BUG: moves lo on the wrong branch, walks off the array end
        int lo = 0;
        int hi = arr.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        return -1;
    }
}
""".replace("// BUG: hi never shrinks below mid — infinite loop on misses? no:\n        ", "")),
        ("apc-m11-selectionsort", r"""public class Solution {
    public static int[] selectionSort(int[] arr) {
        int[] out = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            out[i] = arr[i];
        }
        for (int i = 0; i < out.length - 1; i++) {
            int min = i;
            for (int j = i + 1; j < out.length; j++) {
                if (out[j] < out[min]) {
                    min = j;
                }
            }
            int temp = out[i];
            out[i] = out[min];
            out[min] = temp;
        }
        return out;
    }
}
""",
         r"""public class Solution {
    public static int[] selectionSort(int[] arr) {
        // BUG: sorts the input in place — caller's array destroyed
        int[] out = arr;
        for (int i = 0; i < out.length - 1; i++) {
            int min = i;
            for (int j = i + 1; j < out.length; j++) {
                if (out[j] < out[min]) {
                    min = j;
                }
            }
            int temp = out[i];
            out[i] = out[min];
            out[min] = temp;
        }
        return out;
    }
}
"""),
        ("apc-m11-insertionshifts", r"""public class Solution {
    public static int insertionShifts(int[] arr) {
        int shifts = 0;
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[j] > arr[i]) {
                    shifts++;
                }
            }
        }
        return shifts;
    }
}
""",
         r"""public class Solution {
    public static int insertionShifts(int[] arr) {
        // BUG: counts the wrong comparison direction
        int shifts = 0;
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[j] < arr[i]) {
                    shifts++;
                }
            }
        }
        return shifts;
    }
}
"""),
        ("apc-m11-fix-binary", r"""public class Solution {
    public static int find(int[] arr, int target) {
        int lo = 0;
        int hi = arr.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return -1;
    }
}
""",
         r"""public class Solution {
    public static int find(int[] arr, int target) {
        // BUG: original flaw kept — branches inverted, chases the wrong half
        int lo = 0;
        int hi = arr.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }
        return -1;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m11", "Checkpoint: sort by key",
    "Stable insertion sort on a computed key (last digit).",
    25,
    r"""
Sorting by a computed key with stability preserved is the exam's trickiest
sort variant: compare (x % 10), shift only on strict inequality, and the
original order of ties survives automatically.
""",
    "Điểm kiểm tra: sắp theo khóa",
    "Sắp chèn ổn định trên khóa tính được (chữ số cuối).",
    r"""
Sắp theo khóa tính được mà giữ tính ổn định là biến thể khó nhất của đề thi:
so sánh (x % 10), chỉ dịch khi bất đẳng ngặt, và thứ tự gốc của các phần tử
bằng nhau tự động được bảo toàn.
""",
    CP11C,
    vi_challenge("Điểm kiểm tra: sắp theo khóa", "Cài đặt `int[] sortNames(int[] keys)`: trả về mảng mới sắp tăng dần theo chữ số cuối (value % 10); bằng nhau giữ thứ tự gốc (ổn định — sắp chèn làm điều này tự nhiên). keys khác rỗng.",
        [("stable key sort", "Sắp chèn so sánh (a % 10) < (b % 10), chỉ dịch khi lớn hơn ngặt.")]),
    solution=r"""public class Solution {
    public static int[] sortNames(int[] keys) {
        int[] out = new int[keys.length];
        for (int i = 0; i < keys.length; i++) {
            out[i] = keys[i];
        }
        for (int i = 1; i < out.length; i++) {
            int key = out[i];
            int j = i - 1;
            while (j >= 0 && out[j] % 10 > key % 10) {
                out[j + 1] = out[j];
                j--;
            }
            out[j + 1] = key;
        }
        return out;
    }
}
""",
    wrong=r"""public class Solution {
    public static int[] sortNames(int[] keys) {
        // BUG: unstable tie handling — equal keys come out reversed
        int[] out = new int[keys.length];
        for (int i = 0; i < keys.length; i++) {
            out[i] = keys[i];
        }
        for (int i = 1; i < out.length; i++) {
            int key = out[i];
            int j = i - 1;
            while (j >= 0 && out[j] % 10 >= key % 10) {
                out[j + 1] = out[j];
                j--;
            }
            out[j + 1] = key;
        }
        return out;
    }
}
""",
)
