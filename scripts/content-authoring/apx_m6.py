#!/usr/bin/env python3
"""AP CSA Advanced M6 — Advanced array & ArrayList problems (verified ground truths)."""
from apx import *

M = "apx-arrays"

write_module(
    M,
    "Advanced Array & ArrayList Problems",
    "Second-extremum scans, in-place write-index dedup, rotations, mode, reverse-removal, and two-cursor merges — unfamiliar contexts, tricky indices. Difficulty E3–E4.",
    "Bài toán mảng & ArrayList nâng cao",
    "Quét cực trị thứ hai, dedup bằng chỉ số ghi tại chỗ, xoay mảng, mode, xóa chiều ngược, và trộn hai con trỏ — bối cảnh lạ, chỉ số khó. Độ khó E3–E4.",
    lessons=["apx-m6-twopass", "apx-m6-writeindex", "apx-m6-almutation", "apx-cp-m6"],
    practices=["apx-p6-arrays"],
)

L1 = r"""
**Two passes beat one clever pass.** A surprising number of "hard"
array tasks decompose into: pass 1 computes a summary (max, sum,
count), pass 2 applies it. The exam's favorite: *second distinct
maximum*. One pass is possible but error-prone (three branches: bigger
than max, between max and second, equal to max must be ignored);
two passes — find max, then find max excluding it — is nearly
mechanical. Under time pressure, mechanical wins.

**Equality vs identity for objects**: `==` on Strings/Integers
compares references. Use `.equals(...)` unless both sides are `int`.
The mode problem below is exactly where this bites: comparing
`list.get(j) == v` on Integer objects can pass small-cache tests and
fail larger ones — always `.equals`.

**Boundary table** for any array scan: empty → spec-defined value
(often -1 or a boolean), one element → is it its own answer?, all
equal → tie behavior defined by the spec, negatives present → does
your initialization survive?
"""

L2 = r"""
**The write-index pattern** (in-place compaction):

```java
int w = 0;                       // next slot to write
for (int i = 0; i < a.length; i++) {
    if (keep(a[i])) { a[w] = a[i]; w++; }
}
// w = new logical length; cells a[w..] are garbage-but-safe
```

This solves dedup-on-sorted, remove-matches, move-zeros — every
"compact an array" FRQ the exam has ever written. The pattern's
discipline: `w` never looks back, `i` never skips. W solutions in
this module fail exactly one boundary (the last element or the first)
so you can *see* which boundary your own code forgot.

**Rotation** by k: copy to temp with `tmp[(i + k) % n] = a[i]`, then
copy back. Off-by-one candidates: starting the modulo at 1, or
rotating the wrong direction. Check with n=1 (no change) and k=n
(no change) — both must be no-ops.
"""

L3 = r"""
**ArrayList mutation discipline.** Three legal strategies, one
forbidden one:

- **Reverse index loop** (`for (int i = list.size() - 1; i >= 0;
  i--)`): removals cannot affect not-yet-visited indexes. The safest
  remove-matches loop.
- **Build a new list**: read the old, append survivors. Costs memory,
  never misindexes.
- **Write-index over the same list** via `set` — advanced, rarely
  needed on the exam.

Forbidden: removing from an ArrayList inside a *for-each* loop —
ConcurrentModificationException. (The AP subset *does* test this as a
"why does this crash" MCQ.)

**Two-cursor merge** (interleave): advance whichever input still has
elements, alternating. The drain phase — one list already exhausted —
is the boundary the distractors encode: they drop the tail of the
longer list.
"""

VI_L1 = r"""
**Hai lượt duyệt thắng một lượt thông minh.** Không ít bài mảng "khó"
phân rã thành: lượt 1 tính một đại lượng tóm tắt (max, tổng, đếm),
lượt 2 áp dụng nó. Mục yêu thích của đề thi: *giá trị lớn nhất riêng
biệt thứ hai*. Một lượt là được nhưng dễ lỗi (ba nhánh: lớn hơn max,
nằm giữa max và second, bằng max phải bỏ qua); hai lượt — tìm max,
rồi tìm max loại trừ nó — gần như máy móc. Dưới áp lực thời gian,
máy móc thắng.

**Ngang bằng vs định danh với đối tượng**: `==` trên String/Integer
so sánh tham chiếu. Dùng `.equals(...)` trừ khi cả hai vế là `int`.
Bài mode dưới đây đúng chỗ này: so sánh `list.get(j) == v` trên đối
tượng Integer có thể qua các test nhỏ nhờ cache và fail với số lớn —
luôn luôn `.equals`.

**Bảng biên** cho mọi lượt quét mảng: rỗng → giá trị theo đặc tả
(thường -1 hoặc boolean), một phần tử → nó có tự là đáp án không?, tất
cả bằng nhau → hành vi hòa được đặc tả thế nào, có số âm → cách khởi
tạo của bạn có sống sót không?
"""

VI_L2 = r"""
**Mẫu chỉ số ghi** (nén tại chỗ):

```java
int w = 0;                       // ô trống kế tiếp để ghi
for (int i = 0; i < a.length; i++) {
    if (keep(a[i])) { a[w] = a[i]; w++; }
}
// w = độ dài logic mới; các ô a[w..] là rác-nhưng-an toàn
```

Mẫu này giải dedup-trên-mảng-đã-sắp, xóa-khớp, dời-số-0 — mọi FRQ
"nén mảng" đề thi từng viết. Kỷ luật của mẫu: `w` không bao giờ nhìn
lại, `i` không bao giờ bỏ sót. Các lời giải W trong module này fail
đúng một biên (phần tử cuối hoặc đầu) để bạn *thấy* được mã của mình
quên biên nào.

**Xoay mảng** k bước: sao chép ra mảng tạm với `tmp[(i + k) % n] =
a[i]`, rồi sao chép ngược lại. Ứng viên lệch-một: bắt đầu modulo tại 1,
hoặc xoay sai hướng. Kiểm tra với n=1 (không đổi) và k=n (không đổi) —
cả hai phải là phép no-op.
"""

VI_L3 = r"""
**Kỷ luật biến đổi ArrayList.** Ba chiến lược hợp lệ, một chiến lược
bị cấm:

- **Vòng lặp chỉ số ngược** (`for (int i = list.size() - 1; i >= 0;
  i--)`): phép xóa không thể ảnh hưởng các chỉ số chưa duyệt. Vòng
  xóa-khớp an toàn nhất.
- **Dựng danh sách mới**: đọc danh sách cũ, nối các phần tử sống sót.
  Tốn bộ nhớ, không bao giờ sai chỉ số.
- **Chỉ số ghi trên cùng danh sách** qua `set` — nâng cao, hiếm khi
  cần ở đề thi.

Bị cấm: xóa khỏi ArrayList bên trong vòng lặp *for-each* —
ConcurrentModificationException. (Tập con AP *có* kiểm tra điều này
dưới dạng trắc nghiệm "vì sao mã này sập".)

**Trộn hai con trỏ** (xen kẽ): tiếp tục với đầu vào nào còn phần tử,
xen kẽ nhau. Giai đoạn rút cạn — một danh sách đã hết — là biên mà
các phương án nhiễu mã hóa: chúng làm rơi đuôi của danh sách dài hơn.
"""

BOILER_ARR = r"""public class Solution {
    public static int process(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_ARRSTR = r"""public class Solution {
    public static String process(int[] arr) {
        return ""; // replace
    }
}
"""

BOILER_LIST = r"""public class Solution {
    public static int process(java.util.ArrayList<Integer> list) {
        return 0; // replace
    }
}
"""

P_SECOND = challenge(
    "apx-m6-secondmax",
    "Second distinct maximum",
    "Return the **second distinct maximum** value; return -1 if it does "
    "not exist (fewer than two distinct values, or empty). Implement "
    "`process(int[] arr)`.\n\nExamples: `{4,1,4,2}` → `2` (4 repeats "
    "count once), `{5,5}` → `-1`, `{}` → `-1`.",
    BOILER_ARR,
    [(
        "second maximum",
        r"""
CjTestBase.checkEq(Solution.process(new int[]{4, 1, 4, 2}), 2, "duplicate max counted once");
CjTestBase.checkEq(Solution.process(new int[]{5, 5}), -1, "no distinct second");
CjTestBase.checkEq(Solution.process(new int[]{}), -1, "empty");
CjTestBase.checkEq(Solution.process(new int[]{3, 9}), 3, "two elements");
CjTestBase.checkEq(Solution.process(new int[]{-2, -5, -3}), -3, "all negative");
""",
        "Two passes: find max, then max among values strictly less than it. Duplicates of max are excluded, not errors.",
    )],
    level="independent",
    difficulty="advanced",
)

P_ROT = challenge(
    "apx-m6-rotate",
    "Rotate right by k",
    "Rotate the array **right by k** positions (each element moves "
    "forward, wrapping: last becomes first). Mutate the array in place. "
    "Implement `rotate(int[] arr, int k)` where 0 ≤ k (k may exceed "
    "length — then it wraps; k % length == 0 changes nothing).\n\n"
    "Example: `{1,2,3,4,5}`, k=2 → `{4,5,1,2,3}`.",
    r"""public class Solution {
    public static void rotate(int[] arr, int k) {
        // replace
    }
}
""",
    [(
        "rotated array",
        r"""
int[] a = {1, 2, 3, 4, 5};
Solution.rotate(a, 2);
CjTestBase.checkEq(a, new int[]{4, 5, 1, 2, 3}, "right rotation by 2");
int[] b = {7};
Solution.rotate(b, 5);
CjTestBase.checkEq(b, new int[]{7}, "single element no-op");
int[] c = {1, 2};
Solution.rotate(c, 2);
CjTestBase.checkEq(c, new int[]{1, 2}, "k equals length no-op");
""",
        "k %= length first; tmp[(i + k) % length] = arr[i] into a temp array, then copy back.",
    )],
    level="independent",
    difficulty="advanced",
)

P_MODE = challenge(
    "apx-m6-mode",
    "Mode with a defined tie-break",
    "Return the **mode** (most frequent value). On ties, return the "
    "**smallest** value among the tied ones. The list is non-empty. "
    "Implement `process(java.util.ArrayList<Integer> list)`.\n\n"
    "Example: `[2,3,2,3,5]` → `2` (2 and 3 tie; 2 is smaller).",
    BOILER_LIST,
    [(
        "mode with tie-break",
        r"""
java.util.ArrayList<Integer> l = new java.util.ArrayList<>(java.util.List.of(2, 3, 2, 3, 5));
CjTestBase.checkEq(Solution.process(l), 2, "tie broken to smallest");
java.util.ArrayList<Integer> rev = new java.util.ArrayList<>(java.util.List.of(5, 3, 3, 5));
CjTestBase.checkEq(Solution.process(rev), 3, "tie broken to smallest even when seen later");
java.util.ArrayList<Integer> s = new java.util.ArrayList<>(java.util.List.of(9));
CjTestBase.checkEq(Solution.process(s), 9, "single element");
java.util.ArrayList<Integer> t = new java.util.ArrayList<>(java.util.List.of(-1, -1, 4));
CjTestBase.checkEq(Solution.process(t), -1, "negative mode");
""",
        "Count each value's occurrences; strictly-greater count replaces, equal count keeps the smaller value.",
    )],
    level="combination",
    difficulty="advanced",
)

P_DEDUP = challenge(
    "apx-m6-dedup",
    "Dedup a sorted array in place",
    "Given an array **sorted ascending**, remove duplicates in place so "
    "each value appears once; return the new logical length. Elements "
    "beyond the returned length are ignored by the grader. Implement "
    "`process(int[] arr)` (return 0 for empty).\n\nExample: "
    "`{1,1,2,3,3}` → returns `3`, first three cells `{1,2,3}`.",
    BOILER_ARR,
    [(
        "compacted length and cells",
        r"""
int[] a = {1, 1, 2, 3, 3};
int n = Solution.process(a);
CjTestBase.checkEq(n, 3, "logical length");
CjTestBase.checkEq(java.util.Arrays.copyOf(a, n), new int[]{1, 2, 3}, "compacted cells");
int[] one = {5};
CjTestBase.checkEq(Solution.process(one), 1, "single element");
int[] triple = {2, 2, 2, 7};
int m = Solution.process(triple);
CjTestBase.checkEq(java.util.Arrays.copyOf(triple, m), new int[]{2, 7}, "triple run collapsed");
""",
        "Write-index: w starts at 1; append arr[i] only when it differs from arr[w-1].",
    )],
    level="combination",
    difficulty="advanced",
)

P_FAIL = challenge(
    "apx-m6-removefailing",
    "Remove failing scores, count them",
    "Remove every score **below 60** from the list, returning **how "
    "many** were removed. Order of survivors must be preserved. "
    "Implement `process(java.util.ArrayList<Integer> list)`.\n\n"
    "Example: `[70,50,80,40]` → returns `2`, list becomes `[70, 80]`.",
    BOILER_LIST,
    [(
        "removal count",
        r"""
java.util.ArrayList<Integer> l = new java.util.ArrayList<>(java.util.List.of(70, 50, 80, 40));
CjTestBase.checkEq(Solution.process(l), 2, "two removed");
CjTestBase.checkEq(l, new java.util.ArrayList<>(java.util.List.of(70, 80)), "survivors in order");
java.util.ArrayList<Integer> none = new java.util.ArrayList<>(java.util.List.of(90, 100));
CjTestBase.checkEq(Solution.process(none), 0, "nothing removed");
""",
        "Iterate from the end so removals cannot shift unvisited indices; count each removal.",
    )],
    level="independent",
    difficulty="intermediate",
)

P_MERGE = challenge(
    "apx-m6-interleave",
    "Interleave two arrays",
    "Build a new array alternating elements from `a` and `b` (a first). "
    "When one runs out, append the remainder of the other. Implement "
    "`process(int[] a, int[] b)` — note the two-parameter shape "
    "`interleave`.\n\nExample: `{1,2,3}` and `{9,9}` → `{1,9,2,9,3}`.",
    r"""public class Solution {
    public static int[] interleave(int[] a, int[] b) {
        return new int[0]; // replace
    }
}
""",
    [(
        "interleaved with drain",
        r"""
CjTestBase.checkEq(Solution.interleave(new int[]{1, 2, 3}, new int[]{9, 9}), new int[]{1, 9, 2, 9, 3}, "drain the tail");
CjTestBase.checkEq(Solution.interleave(new int[]{}, new int[]{1, 2}), new int[]{1, 2}, "empty a");
CjTestBase.checkEq(Solution.interleave(new int[]{5, 6}, new int[]{}), new int[]{5, 6}, "empty b");
""",
        "Advance whichever cursor still has elements; the drain phase must append the longer list's tail.",
    )],
    level="real-world",
    difficulty="advanced",
)

CP6 = challenge(
    "apx-cp-m6-suffixsum",
    "Checkpoint: does each element beat the suffix?",
    "Count positions i where `arr[i]` is **strictly greater than the "
    "sum of all elements after i**. Implement `process(int[] arr)` "
    "(0 for empty).\n\nExample: `{3, 1, 2}` → positions: 3>3? no; "
    "1>2? no; 2>0 (nothing after)? yes → `1`.",
    BOILER_ARR,
    [(
        "dominant positions",
        r"""
CjTestBase.checkEq(Solution.process(new int[]{3, 1, 2}), 1, "only the last element");
CjTestBase.checkEq(Solution.process(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.process(new int[]{9}), 1, "single element beats the empty suffix");
CjTestBase.checkEq(Solution.process(new int[]{5, -1, 2, -3}), 2, "negatives shift the balance");
""",
        "Walk from the right keeping a running suffix sum; count when arr[i] > suffixSoFar.",
    )],
    level="combination",
    difficulty="advanced",
)

VI_CP6 = vi_challenge(
    "Điểm kiểm tra: phần tử nào trội hơn hậu tố?",
    "Đếm các vị trí i mà `arr[i]` **lớn hơn hoàn toàn tổng các phần tử "
    "sau i**. Cài đặt `process(int[] arr)` (0 cho rỗng).\n\nVí dụ: "
    "`{3, 1, 2}` → các vị trí: 3>3? không; 1>2? không; 2>0 (không có gì "
    "sau)? có → `1`.",
    [("dominant positions", "Duyệt từ phải sang trái giữ tổng hậu tố chạy; đếm khi arr[i] > tổngHậuTố.")],
)

write_practice(
    M, "apx-p6-arrays", "Array lab: two passes, write indices, safe removal",
    "Six problems where the index discipline is the whole difficulty.",
    "Phòng thí nghiệm mảng: hai lượt, chỉ số ghi, xóa an toàn",
    "Sáu bài toán mà kỷ luật chỉ số là toàn bộ độ khó.",
    after_lesson="apx-m6-almutation", minutes=60, difficulty="advanced",
    challenges=[P_SECOND, P_FAIL, P_DEDUP, P_ROT, P_MODE, P_MERGE],
    vi_challenges={
        "apx-m6-secondmax": vi_challenge(
            "Giá trị lớn nhất riêng biệt thứ hai",
            "Trả về **giá trị lớn nhất riêng biệt thứ hai**; trả -1 nếu không "
            "tồn tại (ít hơn hai giá trị riêng biệt, hoặc rỗng). Cài đặt "
            "`process(int[] arr)`.\n\nVí dụ: `{4,1,4,2}` → `2` (4 lặp chỉ đếm "
            "một lần), `{5,5}` → `-1`, `{}` → `-1`.",
            [("second maximum", "Hai lượt: tìm max, rồi max trong các giá trị nhỏ hơn strictly. Bản sao của max bị loại trừ, không phải lỗi.")],
        ),
        "apx-m6-rotate": vi_challenge(
            "Xoay phải k bước",
            "Xoay mảng **sang phải k** vị trí (mỗi phần tử tiến lên, vòng lại: "
            "phần tử cuối thành đầu). Biến đổi tại chỗ. Cài đặt "
            "`rotate(int[] arr, int k)` với 0 ≤ k (k có thể vượt độ dài — khi "
            "đó vòng lại; k % độ dài == 0 thì không đổi).\n\nVí dụ: "
            "`{1,2,3,4,5}`, k=2 → `{4,5,1,2,3}`.",
            [("rotated array", "k %= độ dài trước; tmp[(i + k) % độ dài] = arr[i] vào mảng tạm, rồi sao chép ngược.")],
        ),
        "apx-m6-mode": vi_challenge(
            "Mode với luật phá hòa",
            "Trả về **mode** (giá trị xuất hiện nhiều nhất). Khi hòa, trả về "
            "**giá trị nhỏ nhất** trong nhóm hòa. Danh sách khác rỗng. Cài "
            "đặt `process(java.util.ArrayList<Integer> list)`.\n\nVí dụ: "
            "`[2,3,2,3,5]` → `2` (2 và 3 hòa; 2 nhỏ hơn).",
            [("mode with tie-break", "Đếm số lần xuất hiện của từng giá trị; đếm lớn hơn thì thay thế, bằng nhau giữ giá trị nhỏ hơn.")],
        ),
        "apx-m6-dedup": vi_challenge(
            "Dedup mảng đã sắp tại chỗ",
            "Cho mảng **đã sắp tăng dần**, loại bản sao tại chỗ để mỗi giá trị "
            "xuất hiện một lần; trả về độ dài logic mới. Các phần tử sau độ dài "
            "trả về bị máy chấm bỏ qua. Cài đặt `process(int[] arr)` (trả 0 cho "
            "rỗng).\n\nVí dụ: `{1,1,2,3,3}` → trả `3`, ba ô đầu `{1,2,3}`.",
            [("compacted length and cells", "Chỉ số ghi: w bắt đầu ở 1; chỉ nối arr[i] khi khác arr[w-1].")],
        ),
        "apx-m6-removefailing": vi_challenge(
            "Xóa điểm liệt, đếm số lượng",
            "Xóa mọi điểm **dưới 60** khỏi danh sách, trả về **số phần tử bị "
            "xóa**. Thứ tự của phần tử sót lại phải được giữ. Cài đặt "
            "`process(java.util.ArrayList<Integer> list)`.\n\nVí dụ: "
            "`[70,50,80,40]` → trả `2`, danh sách thành `[70, 80]`.",
            [("removal count", "Duyệt từ cuối lên để phép xóa không dịch chuyển chỉ số chưa duyệt; đếm mỗi lần xóa.")],
        ),
        "apx-m6-interleave": vi_challenge(
            "Xen kẽ hai mảng",
            "Dựng mảng mới xen kẽ phần tử của `a` và `b` (a trước). Khi một "
            "bên hết, nối phần còn lại của bên kia. Cài đặt "
            "`interleave(int[] a, int[] b)`.\n\nVí dụ: `{1,2,3}` và `{9,9}` "
            "→ `{1,9,2,9,3}`.",
            [("interleaved with drain", "Tăng con trỏ nào còn phần tử; giai đoạn rút cạn phải nối đuôi danh sách dài hơn.")],
        ),
    },
    solutions=[
        ("apx-m6-secondmax", r"""public class Solution {
    public static int process(int[] arr) {
        if (arr.length < 2) {
            return -1;
        }
        int max = arr[0];
        for (int v : arr) {
            if (v > max) {
                max = v;
            }
        }
        int second = Integer.MIN_VALUE;
        for (int v : arr) {
            if (v < max && v > second) {
                second = v;
            }
        }
        return second == Integer.MIN_VALUE ? -1 : second;
    }
}
""", r"""public class Solution {
    // BUG: single-pass branch misses equal-to-max — counts duplicates of max as second
    public static int process(int[] arr) {
        if (arr.length < 2) {
            return -1;
        }
        int max = Integer.MIN_VALUE;
        int second = Integer.MIN_VALUE;
        for (int v : arr) {
            if (v > max) {
                second = max;
                max = v;
            } else if (v > second) {
                second = v;
            }
        }
        return second == Integer.MIN_VALUE ? -1 : second;
    }
}
"""),
        ("apx-m6-rotate", r"""public class Solution {
    public static void rotate(int[] arr, int k) {
        int n = arr.length;
        if (n == 0) {
            return;
        }
        k = k % n;
        int[] tmp = new int[n];
        for (int i = 0; i < n; i++) {
            tmp[(i + k) % n] = arr[i];
        }
        for (int i = 0; i < n; i++) {
            arr[i] = tmp[i];
        }
    }
}
""", r"""public class Solution {
    // BUG: rotates LEFT instead of right (tmp[(i - k + n) % n])
    public static void rotate(int[] arr, int k) {
        int n = arr.length;
        if (n == 0) {
            return;
        }
        k = k % n;
        int[] tmp = new int[n];
        for (int i = 0; i < n; i++) {
            tmp[((i - k) % n + n) % n] = arr[i];
        }
        for (int i = 0; i < n; i++) {
            arr[i] = tmp[i];
        }
    }
}
"""),
        ("apx-m6-mode", r"""public class Solution {
    public static int process(java.util.ArrayList<Integer> list) {
        int bestVal = 0;
        int bestCount = 0;
        for (int i = 0; i < list.size(); i++) {
            int v = list.get(i);
            int cnt = 0;
            for (int j = 0; j < list.size(); j++) {
                if (list.get(j).equals(v)) {
                    cnt++;
                }
            }
            if (cnt > bestCount || (cnt == bestCount && v < bestVal)) {
                bestCount = cnt;
                bestVal = v;
            }
        }
        return bestVal;
    }
}
""", r"""public class Solution {
    // BUG: keeps the FIRST tied value instead of the smallest (ties by first occurrence)
    public static int process(java.util.ArrayList<Integer> list) {
        int bestVal = 0;
        int bestCount = 0;
        for (int i = 0; i < list.size(); i++) {
            int v = list.get(i);
            int cnt = 0;
            for (int j = 0; j < list.size(); j++) {
                if (list.get(j).equals(v)) {
                    cnt++;
                }
            }
            if (cnt > bestCount || (cnt == bestCount && list.indexOf(v) < list.indexOf(bestVal))) {
                bestCount = cnt;
                bestVal = v;
            }
        }
        return bestVal;
    }
}
"""),
        ("apx-m6-dedup", r"""public class Solution {
    public static int process(int[] arr) {
        if (arr.length == 0) {
            return 0;
        }
        int w = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] != arr[w - 1]) {
                arr[w] = arr[i];
                w++;
            }
        }
        return w;
    }
}
""", r"""public class Solution {
    // BUG: off-by-one return — claims one extra element, exposing a garbage cell
    public static int process(int[] arr) {
        if (arr.length == 0) {
            return 0;
        }
        int w = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] != arr[w - 1]) {
                arr[w] = arr[i];
                w++;
            }
        }
        return w + 1;
    }
}
"""),
        ("apx-m6-removefailing", r"""public class Solution {
    public static int process(java.util.ArrayList<Integer> list) {
        int removed = 0;
        for (int i = list.size() - 1; i >= 0; i--) {
            if (list.get(i) < 60) {
                list.remove(i);
                removed++;
            }
        }
        return removed;
    }
}
""", r"""public class Solution {
    // BUG: forgets to count — removes correctly but returns 0
    public static int process(java.util.ArrayList<Integer> list) {
        for (int i = list.size() - 1; i >= 0; i--) {
            if (list.get(i) < 60) {
                list.remove(i);
            }
        }
        return 0;
    }
}
"""),
        ("apx-m6-interleave", r"""public class Solution {
    public static int[] interleave(int[] a, int[] b) {
        int[] out = new int[a.length + b.length];
        int oi = 0;
        int ai = 0;
        int bi = 0;
        while (ai < a.length || bi < b.length) {
            if (ai < a.length) {
                out[oi] = a[ai];
                oi++;
                ai++;
            }
            if (bi < b.length) {
                out[oi] = b[bi];
                oi++;
                bi++;
            }
        }
        return out;
    }
}
""", r"""public class Solution {
    // BUG: stops when the SHORTER list ends — drops the drain phase
    public static int[] interleave(int[] a, int[] b) {
        int[] out = new int[a.length + b.length];
        int oi = 0;
        for (int i = 0; i < Math.min(a.length, b.length); i++) {
            out[oi] = a[i];
            oi++;
            out[oi] = b[i];
            oi++;
        }
        return out;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m6", "Checkpoint: suffix dominance",
    "Reverse-scan checkpoint: a running suffix sum decides each position.",
    18,
    r"""
The reverse walk is the array analog of the write-index: state flows
in one direction, and each decision reads only that state. If your
first instinct is a nested loop per position, the running-sum
refactor is the lesson.
""",
    "Điểm kiểm tra: trội hơn hậu tố",
    "Bài kiểm tra duyệt ngược: tổng hậu tố chạy quyết định từng vị trí.",
    r"""
Duyệt ngược là phiên bản mảng của chỉ số ghi: trạng thái chảy một
hướng, và mỗi quyết định chỉ đọc trạng thái đó. Nếu phản xạ đầu là
vòng lặp lồng cho từng vị trí, việc viết lại bằng tổng chạy chính là
bài học.
""",
    CP6,
    VI_CP6,
    solution=r"""public class Solution {
    public static int process(int[] arr) {
        int count = 0;
        int suffix = 0;
        for (int i = arr.length - 1; i >= 0; i--) {
            if (arr[i] > suffix) {
                count++;
            }
            suffix += arr[i];
        }
        return count;
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: adds arr[i] to the suffix BEFORE comparing — off-by-one state
    public static int process(int[] arr) {
        int count = 0;
        int suffix = 0;
        for (int i = arr.length - 1; i >= 0; i--) {
            suffix += arr[i];
            if (arr[i] > suffix) {
                count++;
            }
        }
        return count;
    }
}
""",
)

print("M6 done")
