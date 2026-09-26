#!/usr/bin/env python3
"""AP CSA Core M6 — Array Mastery (traversal modes + boundary cases)."""
from apcc import *

M = "cx-arrays"

L1 = r"""
Arrays are the exam's heaviest topic (Data Collections is 30–40% of the
MCQ section). Every array question is a traversal in one of four modes —
name the mode before writing code:

**Forward index scan** — the default; use when you need indexes:
```java
for (int i = 0; i < arr.length; i++) { ... arr[i] ... }
```
**For-each** — when you only read values, never indexes:
```java
for (int v : arr) { ... }
```
**Reverse scan** — when removals or right-to-left order matter:
```java
for (int i = arr.length - 1; i >= 0; i--) { ... }
```
**Pairwise (adjacent) scan** — neighbor logic; loop to `length - 1`
(and read `arr[i + 1]`), or start at 1 and read `arr[i - 1]`:
```java
for (int i = 0; i < arr.length - 1; i++) { compare arr[i] and arr[i + 1]; }
```

Choosing the wrong mode is the #1 structural mistake: modifying while
forward-iterating, or needing the index inside a for-each (impossible —
the loop variable is a *copy* of the element, so `v = 5` changes
nothing).

**Boundary drill:** for `{10, 20, 30}` — `arr.length` is 3, valid
indexes are 0..2, `arr[arr.length - 1]` is the last element, and
`arr[arr.length]` throws `ArrayIndexOutOfBoundsException`. Every MCQ
that "throws an exception" is testing exactly this.
"""

L2 = r"""
Index algebra is a skill you practice on paper. Three workhorses:

**Min/max with the index.** Track the position, not the value, when the
answer needs a location:

```java
int best = 0;
for (int i = 1; i < arr.length; i++) {
    if (arr[i] > arr[best]) { best = i; }
}
return best;   // index of max (first on ties)
```

**Left/right neighbors.** "Every element bigger than both neighbors":

```java
for (int i = 1; i < arr.length - 1; i++) {
    if (arr[i] > arr[i - 1] && arr[i] > arr[i + 1]) { count++; }
}
```

The bounds exclude index 0 and the last index — they have only one
neighbor. Off-by-one here changes the answer silently.

**Rotation.** Shift everything right by 1, last wraps to front:

```java
int[] out = new int[arr.length];
for (int i = 0; i < arr.length; i++) {
    out[(i + 1) % arr.length] = arr[i];
}
```

Or the in-place copy form most students find clearer:

```java
for (int i = 0; i < arr.length - 1; i++) {
    out[i + 1] = arr[i];
}
out[0] = arr[arr.length - 1];
```

Single-element and empty arrays are the two inputs that break careless
rotations — run them in your head first. Note `arr.length - 1` in the
loop bound: with `arr.length`, `out[i + 1]` walks off the end.
"""

L3 = r"""
Two multi-pass shapes complete the toolkit:

**Count-then-act.** *"Move all zeros to the end, preserving order of
the rest."* Pass 1 counts zeros; pass 2 writes non-zeros forward and
fills the tail with zeros:

```java
int next = 0;
for (int i = 0; i < arr.length; i++) {
    if (arr[i] != 0) { arr[next] = arr[i]; next++; }
}
for (int i = next; i < arr.length; i++) { arr[i] = 0; }
```

Trace `{0, 3, 0, 1}`: next walks 0, 1, 1, 2 — after pass one,
`{3, 1, 0, 1}` (the tail is garbage); pass two zeroes it: `{3, 1, 0, 0}`.
Order preserved, no extra array.

**Condition-based dedup** — "count elements NOT already seen". With no
extra structures allowed, compare each element only to the previous
*distinct run*, or accept O(n²) pairwise comparison:

```java
int distinct = 0;
for (int i = 0; i < arr.length; i++) {
    boolean seen = false;
    for (int j = 0; j < i; j++) {
        if (arr[j] == arr[i]) { seen = true; break; }
    }
    if (!seen) { distinct++; }
}
```

`{5, 3, 5, 1}` → distinct = 3. The inner loop only looks *backward*
(`j < i`), so the first occurrence claims each value. On the exam this
pairwise form is acceptable — clarity beats cleverness, and the arrays
are short.
"""

write_module(
    M,
    "Array Mastery",
    "The four traversal modes, index algebra (min/max, neighbors, rotation), and multi-pass shapes (count-then-act, pairwise dedup).",
    "Làm chủ mảng",
    "Bốn chế độ duyệt, đại số chỉ số (min/max, hàng xóm, xoay), và các hình đa-lượt (đếm-rồi-làm, khử trùng lặp từng cặp).",
    lessons=["cx-m6-modes", "cx-m6-index-alg", "cx-m6-multipass", "cx-cp-m6"],
    practices=["cx-p6-arrays"],
)

write_lesson(
    M, "cx-m6-modes", "The four traversal modes",
    "Forward, for-each, reverse, and pairwise — and when each is the wrong tool.",
    12, L1,
    "Bốn chế độ duyệt",
    "Xuôi, for-each, ngược, và từng cặp — và khi nào mỗi chế độ là sai công cụ.",
    r"""
Mảng là chủ đề nặng nhất của đề thi (Data Collections chiếm 30–40% phần
MCQ). Mỗi câu mảng là một lượt duyệt theo một trong bốn chế độ — gọi tên
chế độ trước khi viết mã:

**Quét chỉ số xuôi** — mặc định; dùng khi cần chỉ số:
```java
for (int i = 0; i < arr.length; i++) { ... arr[i] ... }
```
**For-each** — khi chỉ đọc giá trị, không cần chỉ số:
```java
for (int v : arr) { ... }
```
**Quét ngược** — khi việc xóa hoặc thứ tự phải-sang-trái quan trọng:
```java
for (int i = arr.length - 1; i >= 0; i--) { ... }
```
**Quét từng cặp (liền kề)** — logic hàng xóm; lặp đến `length - 1`
(và đọc `arr[i + 1]`), hoặc bắt đầu từ 1 và đọc `arr[i - 1]`:
```java
for (int i = 0; i < arr.length - 1; i++) { so sánh arr[i] và arr[i + 1]; }
```

Chọn sai chế độ là lỗi cấu trúc số một: vừa duyệt xuôi vừa sửa mảng, hoặc
cần chỉ số bên trong for-each (bất khả — biến lặp là một *bản sao* của
phần tử, nên `v = 5` không đổi gì cả).

**Bài tập biên:** với `{10, 20, 30}` — `arr.length` là 3, chỉ số hợp lệ
0..2, `arr[arr.length - 1]` là phần tử cuối, và `arr[arr.length]` ném
`ArrayIndexOutOfBoundsException`. Mọi câu MCQ "ném ngoại lệ" đều đang test
đúng chỗ này.
""",
)

write_lesson(
    M, "cx-m6-index-alg", "Index algebra",
    "Min/max by index, neighbor windows, and rotation formulas.",
    12, L2,
    "Đại số chỉ số",
    "Min/max theo chỉ số, cửa sổ hàng xóm, và công thức xoay.",
    r"""
Đại số chỉ số là kỹ năng luyện trên giấy. Ba con ngựa thồ:

**Min/max theo chỉ số.** Theo dõi vị trí, không phải giá trị, khi đáp án
cần một địa điểm:

```java
int best = 0;
for (int i = 1; i < arr.length; i++) {
    if (arr[i] > arr[best]) { best = i; }
}
return best;   // chỉ số của max (đầu tiên khi đồng giá)
```

**Hàng xóm trái/phải.** "Mọi phần tử lớn hơn cả hai hàng xóm":

```java
for (int i = 1; i < arr.length - 1; i++) {
    if (arr[i] > arr[i - 1] && arr[i] > arr[i + 1]) { count++; }
}
```

Biên lọai trừ chỉ số 0 và chỉ số cuối — chúng chỉ có một hàng xóm. Lệch
một ở đây đổi đáp án một cách lặng lẽ.

**Xoay mảng.** Dịch mọi thứ sang phải 1 bước, phần tử cuối quay về đầu:

```java
int[] out = new int[arr.length];
for (int i = 0; i < arr.length; i++) {
    out[(i + 1) % arr.length] = arr[i];
}
```

Hoặc dạng sao chép tại chỗ mà đa số học sinh thấy dễ hiểu hơn:

```java
for (int i = 0; i < arr.length - 1; i++) {
    out[i + 1] = arr[i];
}
out[0] = arr[arr.length - 1];
```

Mảng một phần tử và mảng rỗng là hai đầu vào phá vỡ các vòng xoay bất cẩn
— hãy chạy chúng trong đầu trước. Chú ý `arr.length - 1` trong biên vòng
lặp: dùng `arr.length` thì `out[i + 1]` bước ra khỏi mảng.
""",
)

write_lesson(
    M, "cx-m6-multipass", "Multi-pass shapes",
    "Count-then-act (move zeros) and backward-looking pairwise dedup.",
    12, L3,
    "Các hình đa-lượt",
    "Đếm-rồi-làm (dồn số 0) và khử trùng lặp từng cặp nhìn về sau.",
    r"""
Hai hình đa-lượt hoàn thiện bộ công cụ:

**Đếm-rồi-làm.** *"Dồn mọi số 0 về cuối, giữ nguyên thứ tự phần còn
lại."* Lượt 1 đếm số 0 (thực ra không cần đếm); lượt 2 ghi các phần tử
khác 0 về trước rồi lấp đuôi bằng số 0:

```java
int next = 0;
for (int i = 0; i < arr.length; i++) {
    if (arr[i] != 0) { arr[next] = arr[i]; next++; }
}
for (int i = next; i < arr.length; i++) { arr[i] = 0; }
```

Truy vết `{0, 3, 0, 1}`: next đi 0, 1, 1, 2 — sau lượt một,
`{3, 1, 0, 1}` (phần đuôi là rác); lượt hai dọn nó: `{3, 1, 0, 0}`. Thứ
tự được giữ, không cần mảng phụ.

**Khử trùng lặp theo điều kiện** — "đếm phần tử CHƯA từng thấy". Khi
không được dùng cấu trúc phụ, so sánh từng phần tử với mọi phần tử *trước
nó* (O(n²), chấp nhận được trong phòng thi):

```java
int distinct = 0;
for (int i = 0; i < arr.length; i++) {
    boolean seen = false;
    for (int j = 0; j < i; j++) {
        if (arr[j] == arr[i]) { seen = true; break; }
    }
    if (!seen) { distinct++; }
}
```

`{5, 3, 5, 1}` → distinct = 3. Vòng trong chỉ nhìn *về sau* (`j < i`),
nên lần xuất hiện đầu tiên là người đoạt giá trị. Trong phòng thi, dạng
từng cặp này là chấp nhận được — rõ ràng thắng khéo léo, và mảng trong đề
đều ngắn.
""",
)

BOILER_PEAKS = r"""public class Solution {
    public static int countPeaks(int[] arr) {
        // CONTRACT: elements strictly bigger than BOTH immediate neighbors.
        // Index 0 and the last index are never peaks.
        return 0; // replace
    }
}
"""

BOILER_ROTATE = r"""public class Solution {
    public static int[] rotateRight(int[] arr) {
        // CONTRACT: NEW array shifted right by one; last element wraps
        // to the front. {1,2,3} -> {3,1,2}. Empty -> empty.
        return null; // replace
    }
}
"""

BOILER_ZEROS = r"""public class Solution {
    // CONTRACT: move every 0 to the END of arr, in place, preserving
    // the order of non-zero elements. {0,3,0,1} -> {3,1,0,0}.
    public static void moveZeros(int[] arr) {
        // replace
    }
}
"""

BOILER_DISTINCT = r"""public class Solution {
    // CONTRACT: count distinct values in arr (empty array -> 0).
    public static int countDistinct(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_LASTIDX = r"""public class Solution {
    // CONTRACT: index of the LAST occurrence of key, or -1.
    public static int lastIndexOf(int[] arr, int key) {
        // BUG: always reports the FIRST occurrence (or -1).
        int at = -1;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == key && at == -1) {
                at = i;
            }
        }
        return at;
    }
}
"""

BOILER_BOUDNED = r"""public class Solution {
    // CONTRACT: sum of the elements at EVEN indexes (0, 2, 4, ...).
    public static int sumEvenIndexes(int[] arr) {
        int total = 0;
        for (int i = 0; i <= arr.length; i++) {
            if (i % 2 == 0) {
                total += arr[i];
            }
        }
        return total;
    }
}
"""

BOILER_CP_ARR = r"""public class Solution {
    // CONTRACT: partition arr IN PLACE around the first element (pivot):
    // smaller values first, then the pivot, then the rest, stable.
    // {5, 2, 8, 1, 9, 5} -> {2, 1, 5, 8, 9, 5}
    // Precondition: arr.length >= 1.
    public static void partition(int[] arr) {
        // replace
    }
}
"""

P_PEAKS = challenge(
    "cx-m6-count-peaks",
    "Count the peaks",
    "Implement `int countPeaks(int[] arr)`: elements strictly greater than BOTH immediate neighbors. The first and last elements are never peaks — size your loop bounds accordingly.",
    BOILER_PEAKS,
    [(
        "peaks counted",
        r"""
CjTestBase.checkEq(Solution.countPeaks(new int[]{1, 3, 2, 5, 4}), 2, "3 and 5 are peaks");
CjTestBase.checkEq(Solution.countPeaks(new int[]{1, 2, 3}), 0, "rising edge has no peak");
CjTestBase.checkEq(Solution.countPeaks(new int[]{5}), 0, "no neighbors, no peak");
CjTestBase.checkEq(Solution.countPeaks(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.countPeaks(new int[]{2, 1, 2}), 0, "equal boundary values are not peaks");
""",
        "Loop i from 1 to arr.length - 2 with strict > on both sides.",
    )],
    level="guided",
)

P_ROTATE = challenge(
    "cx-m6-rotate-right",
    "Rotate right",
    "Implement `int[] rotateRight(int[] arr)`: a NEW array shifted right by one, last element wrapping to the front. Write the two failure cases (length 0 and 1) into your loop before running anything.",
    BOILER_ROTATE,
    [(
        "rotated copy",
        r"""
CjTestBase.checkEq(Solution.rotateRight(new int[]{1, 2, 3}), new int[]{3, 1, 2}, "wrap to front");
CjTestBase.checkEq(Solution.rotateRight(new int[]{}), new int[]{}, "empty stays empty");
CjTestBase.checkEq(Solution.rotateRight(new int[]{7}), new int[]{7}, "single element unchanged");
CjTestBase.checkEq(Solution.rotateRight(new int[]{4, 9}), new int[]{9, 4}, "pair swaps");
""",
        "out[0] = arr[arr.length-1]; out[i+1] = arr[i] for i in 0..length-2; handle empty first.",
    )],
    level="independent",
)

P_ZEROS = challenge(
    "cx-m6-move-zeros",
    "Move zeros in place",
    "Implement `void moveZeros(int[] arr)`: all zeros to the end, in place, preserving non-zero order. Two passes: compact non-zeros forward with a write index, then zero-fill the tail.",
    BOILER_ZEROS,
    [(
        "zeros at end",
        r"""
int[] a = {0, 3, 0, 1};
Solution.moveZeros(a);
CjTestBase.checkEq(a, new int[]{3, 1, 0, 0}, "compacted, order kept");
int[] b = {0, 0};
Solution.moveZeros(b);
CjTestBase.checkEq(b, new int[]{0, 0}, "all zeros");
int[] c = {5};
Solution.moveZeros(c);
CjTestBase.checkEq(c, new int[]{5}, "single non-zero");
""",
        "Write-index compaction, then a second loop zeroing from next to length-1.",
    )],
    level="combination",
)

P_DISTINCT = challenge(
    "cx-m6-count-distinct",
    "Backward-looking dedup",
    "Implement `int countDistinct(int[] arr)`: number of distinct values. The pairwise backward scan (j < i, break on first match) is allowed and expected. Empty array → 0.",
    BOILER_DISTINCT,
    [(
        "distinct counted",
        r"""
CjTestBase.checkEq(Solution.countDistinct(new int[]{5, 3, 5, 1}), 3, "5, 3, 1");
CjTestBase.checkEq(Solution.countDistinct(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.countDistinct(new int[]{2, 2, 2}), 1, "all same");
CjTestBase.checkEq(Solution.countDistinct(new int[]{-1, 0, 1}), 3, "negatives are values too");
""",
        "seen flag per element; inner loop j < i with break.",
    )],
    level="combination",
)

P_LASTIDX = challenge(
    "cx-m6-fix-last-index",
    "Fix the sentinel stop",
    "`lastIndexOf` must return the LAST occurrence's index but stops at the first. Trace {4, 7, 7} with key 7, then remove the guard that freezes the result.",
    BOILER_LASTIDX,
    [(
        "last occurrence index",
        r"""
CjTestBase.checkEq(Solution.lastIndexOf(new int[]{4, 7, 7}, 7), 2, "keeps overwriting");
CjTestBase.checkEq(Solution.lastIndexOf(new int[]{1, 2}, 5), -1, "absent");
CjTestBase.checkEq(Solution.lastIndexOf(new int[]{9}, 9), 0, "single hit");
""",
        "Drop the `&& at == -1` so later matches overwrite.",
    )],
    level="debugging",
)

P_EVENIDX = challenge(
    "cx-m6-fix-even-indexes",
    "Fix the walked-off end",
    "`sumEvenIndexes` should add arr[0] + arr[2] + ... but throws on any input. Diagnose the loop bound, then repair it — one character class of mistake.",
    BOILER_BOUDNED,
    [(
        "even indexes summed",
        r"""
CjTestBase.checkEq(Solution.sumEvenIndexes(new int[]{10, 20, 30, 40}), 40, "10 + 30");
CjTestBase.checkEq(Solution.sumEvenIndexes(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.sumEvenIndexes(new int[]{7}), 7, "index 0 counts");
""",
        "Use i < arr.length; <= reads arr[arr.length].",
    )],
    level="debugging",
)

CP6 = challenge(
    "cx-cp-m6-partition",
    "Checkpoint: stable partition",
    "Implement `void partition(int[] arr)`: reorder in place so values smaller than the pivot (arr's first element) come first, then the pivot itself, then everything else — preserving relative order. {5, 2, 8, 1, 9, 5} → {2, 1, 5, 8, 9, 5}. The count-then-act shape with a pivot slot is one clean solution.",
    BOILER_CP_ARR,
    [(
        "stable partition",
        r"""
int[] a = {5, 2, 8, 1, 9, 5};
Solution.partition(a);
CjTestBase.checkEq(a, new int[]{2, 1, 5, 8, 9, 5}, "small, pivot, rest — order kept");
int[] b = {3};
Solution.partition(b);
CjTestBase.checkEq(b, new int[]{3}, "single element");
int[] c = {1, 2, 3};
Solution.partition(c);
CjTestBase.checkEq(c, new int[]{1, 2, 3}, "pivot already smallest: nothing moves before it");
""",
        "Collect smaller values forward, park the pivot at the boundary, append the rest — all order-preserving.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p6-arrays", "Array lab",
    "Peaks, rotation, compaction, dedup, sentinel repair, and a bounds fix.",
    "Phòng mảng",
    "Đỉnh, xoay, nén, khử trùng lặp, sửa lính canh, và sửa biên vòng lặp.",
    after_lesson="cx-m6-index-alg", minutes=60, difficulty="advanced",
    challenges=[P_PEAKS, P_ROTATE, P_ZEROS, P_DISTINCT, P_LASTIDX, P_EVENIDX],
    vi_challenges={
        "cx-m6-count-peaks": vi_challenge("Đếm các đỉnh",
            "Hiện thực `int countPeaks(int[] arr)`: các phần tử lớn hơn MỘT CÁCH NGHIÊM NGẶT cả hai hàng xóm trực tiếp. Phần tử đầu và cuối không bao giờ là đỉnh — hãy kích thước biên vòng lặp theo điều đó.",
            [("peaks counted", "Vòng lặp i từ 1 đến arr.length - 2 với dấu > nghiêm ngặt ở cả hai phía.")]),
        "cx-m6-rotate-right": vi_challenge("Xoay phải",
            "Hiện thực `int[] rotateRight(int[] arr)`: mảng MỚI dịch phải một bước, phần tử cuối quay về đầu. Hãy ghi hai trường hợp lỗi (độ dài 0 và 1) vào vòng lặp trước khi chạy bất cứ gì.",
            [("rotated copy", "out[0] = arr[arr.length-1]; out[i+1] = arr[i] cho i trong 0..length-2; xử lý rỗng trước.")]),
        "cx-m6-move-zeros": vi_challenge("Dồn số 0 tại chỗ",
            "Hiện thực `void moveZeros(int[] arr)`: mọi số 0 về cuối, tại chỗ, giữ thứ tự phần tử khác 0. Hai lượt: nén phần tử khác 0 về trước bằng chỉ số ghi, rồi lấp đuôi bằng số 0.",
            [("zeros at end", "Nén bằng chỉ số ghi, rồi một vòng lặp thứ hai gán 0 từ next đến length-1.")]),
        "cx-m6-count-distinct": vi_challenge("Khử trùng lặp nhìn về sau",
            "Hiện thực `int countDistinct(int[] arr)`: số giá trị phân biệt. Quét từng cặp nhìn về sau (j < i, break ở lần khớp đầu) là được phép và được kỳ vọng. Mảng rỗng → 0.",
            [("distinct counted", "Cờ seen cho từng phần tử; vòng trong j < i với break.")]),
        "cx-m6-fix-last-index": vi_challenge("Sửa cờ dừng của lính canh",
            "`lastIndexOf` phải trả về chỉ số lần xuất hiện CUỐI nhưng dừng ở lần đầu. Truy vết {4, 7, 7} với key 7, rồi gỡ lớp chặn đang đóng băng kết quả.",
            [("last occurrence index", "Bỏ `&& at == -1` để các lần khớp sau ghi đè.")]),
        "cx-m6-fix-even-indexes": vi_challenge("Sửa lỗi bước quá mép",
            "`sumEvenIndexes` nên cộng arr[0] + arr[2] + ... nhưng ném ngoại lệ với mọi đầu vào. Chẩn đoán biên vòng lặp, rồi sửa — một họ lỗi một ký tự.",
            [("even indexes summed", "Dùng i < arr.length; dấu <= sẽ đọc arr[arr.length].")]),
    },
    solutions=[
        ("cx-m6-count-peaks", BOILER_PEAKS.replace("return 0; // replace",
            "int count = 0;\n        for (int i = 1; i < arr.length - 1; i++) {\n            if (arr[i] > arr[i - 1] && arr[i] > arr[i + 1]) {\n                count++;\n            }\n        }\n        return count;"),
         BOILER_PEAKS.replace("return 0; // replace",
            "int count = 0;\n        for (int i = 0; i < arr.length; i++) {\n            if (arr[i] > arr[i + 1]) {\n                count++;\n            }\n        }\n        return count;")),
        ("cx-m6-rotate-right", BOILER_ROTATE.replace("return null; // replace",
            "if (arr.length == 0) { return new int[]{}; }\n        int[] out = new int[arr.length];\n        out[0] = arr[arr.length - 1];\n        for (int i = 0; i < arr.length - 1; i++) {\n            out[i + 1] = arr[i];\n        }\n        return out;"),
         BOILER_ROTATE.replace("return null; // replace",
            "if (arr.length == 0) { return new int[]{}; }\n        int[] out = new int[arr.length];\n        for (int i = 0; i < arr.length; i++) {\n            out[i] = arr[i];\n        }\n        return out;")),
        ("cx-m6-move-zeros",
         r"""public class Solution {
    public static void moveZeros(int[] arr) {
        int next = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] != 0) {
                arr[next] = arr[i];
                next++;
            }
        }
        for (int i = next; i < arr.length; i++) {
            arr[i] = 0;
        }
    }
}
""",
         r"""public class Solution {
    public static void moveZeros(int[] arr) {
        int next = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] != 0) {
                arr[next] = arr[i];
                next++;
            }
        }
        for (int i = next; i < arr.length; i++) {
            arr[i] = 1;
        }
    }
}
"""),
        ("cx-m6-count-distinct", BOILER_DISTINCT.replace("return 0; // replace",
            "int distinct = 0;\n        for (int i = 0; i < arr.length; i++) {\n            boolean seen = false;\n            for (int j = 0; j < i; j++) {\n                if (arr[j] == arr[i]) { seen = true; break; }\n            }\n            if (!seen) { distinct++; }\n        }\n        return distinct;"),
         BOILER_DISTINCT.replace("return 0; // replace",
            "int distinct = 0;\n        for (int i = 0; i < arr.length; i++) {\n            boolean seen = false;\n            for (int j = 0; j <= i; j++) {\n                if (arr[j] == arr[i]) { seen = true; break; }\n            }\n            if (!seen) { distinct++; }\n        }\n        return distinct;")),
        ("cx-m6-fix-last-index", BOILER_LASTIDX.replace("if (arr[i] == key && at == -1) {", "if (arr[i] == key) {"),
         BOILER_LASTIDX),
        ("cx-m6-fix-even-indexes", BOILER_BOUDNED.replace("for (int i = 0; i <= arr.length; i++) {", "for (int i = 0; i < arr.length; i++) {"),
         BOILER_BOUDNED.replace("for (int i = 0; i <= arr.length; i++) {", "for (int i = 0; i <= arr.length + 1; i++) {")),
    ],
)

write_checkpoint(
    M, "cx-cp-m6", "Checkpoint: stable partition",
    "In-place reordering that preserves relative order — compaction plus a pivot slot.",
    25,
    r"""
Stable partition = compaction (smaller values written forward) + parking
the pivot + appending the remainder, all order-preserving. If your trace
moved a value you did not expect, the write index and the read index
were allowed to touch — they must run on independent pointers. This is
the exam's hardest plain-array shape and it decomposes into machines you
have owned since Module 3.
""",
    "Điểm kiểm tra: phân hoạch ổn định",
    "Sắp xếp lại tại chỗ mà vẫn giữ thứ tự tương đối — nén cộng với chỗ để pivot.",
    r"""
Phân hoạch ổn định = nén (giá trị nhỏ được ghi về trước) + đỗ pivot +
nối phần còn lại, tất cả đều giữ thứ tự. Nếu truy vết của bạn làm một giá
trị di chuyển ngoài dự kiến, tức chỉ số ghi và chỉ số đọc đã chạm nhau —
chúng phải chạy trên hai con trỏ độc lập. Đây là hình dạng mảng-thuần
khó nhất của đề thi và nó phân rã thành những cỗ máy bạn sở hữu từ
Module 3.
""",
    CP6,
    vi_challenge("Điểm kiểm tra: phân hoạch ổn định",
        "Hiện thực `void partition(int[] arr)`: sắp xếp lại tại chỗ để các giá trị nhỏ hơn pivot (phần tử đầu của arr) đứng trước, rồi chính pivot, rồi phần còn lại — giữ nguyên thứ tự tương đối. {5, 2, 8, 1, 9, 5} → {2, 1, 5, 8, 9, 5}. Hình đếm-rồi-làm với một chỗ để pivot là một lời giải sạch.",
        [("stable partition", "Gom giá trị nhỏ về trước, đỗ pivot ở biên, nối phần còn lại — tất cả giữ thứ tự.")]),
    solution=r"""public class Solution {
    public static void partition(int[] arr) {
        int pivot = arr[0];
        int[] smaller = new int[arr.length];
        int[] rest = new int[arr.length];
        int ns = 0, nr = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < pivot) { smaller[ns] = arr[i]; ns++; }
            else { rest[nr] = arr[i]; nr++; }
        }
        int k = 0;
        for (int i = 0; i < ns; i++) { arr[k] = smaller[i]; k++; }
        arr[k] = pivot;
        k++;
        for (int i = 0; i < nr; i++) { arr[k] = rest[i]; k++; }
    }
}
""",
    wrong=r"""public class Solution {
    public static void partition(int[] arr) {
        int pivot = arr[0];
        int[] smaller = new int[arr.length];
        int[] rest = new int[arr.length];
        int ns = 0, nr = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] <= pivot) { smaller[ns] = arr[i]; ns++; }
            else { rest[nr] = arr[i]; nr++; }
        }
        int k = 0;
        for (int i = 0; i < ns; i++) { arr[k] = smaller[i]; k++; }
        arr[k] = pivot;
        k++;
        for (int i = 0; i < nr; i++) { arr[k] = rest[i]; k++; }
    }
}
""",
)
