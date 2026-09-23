#!/usr/bin/env python3
"""AP CSA M9 — Arrays (declaration, traversal, accumulation, min/max)."""
from apc import *

M = "apc-arrays"

L1 = r"""
An **array** holds a fixed number of values of one type, numbered from 0:

```java
int[] scores = new int[4];          // {0, 0, 0, 0} — zero-filled
int[] primes = {2, 3, 5, 7};        // literal form
primes[0] = 2;                       // index (read/write)
int n = primes.length;               // LENGTH IS A FIELD — no parentheses!
```

`length` without `()` is the array idiosyncrasy (Strings use `length()`,
ArrayLists use `size()` — the exam mixes all three on purpose).

**Bounds**: valid indices are 0 .. length − 1. Index 4 on a length-4 array
compiles fine and throws `ArrayIndexOutOfBoundsException` at **runtime** —
the most common crash in student code.

**Default values**: `new int[4]` is all zeros; `new boolean[4]` all false;
`new String[4]` all **null** (an array of references, not objects).

The two traversal loops:

```java
for (int i = 0; i < arr.length; i++) {   // when you need the index
    System.out.println(arr[i]);
}

for (int x : arr) {                      // enhanced for: values only
    System.out.println(x);
}
```

The enhanced for cannot *modify* the array (its variable is a copy) and
gives no position — use it for read-only visits.
"""

L2 = r"""
The three accumulation patterns (declare **outside**, update **inside**):

```java
// total
int sum = 0;
for (int x : arr) { sum += x; }

// count matching a rule
int evens = 0;
for (int x : arr) { if (x % 2 == 0) evens++; }

// extremum — seed with the first element, not 0
int max = arr[0];
for (int i = 1; i < arr.length; i++) {
    if (arr[i] > max) {
        max = arr[i];
    }
}
```

Why seed with `arr[0]`? Seeding `max = 0` is wrong for all-negative arrays
(the answer would be 0, an element that isn't even there) and `max =
Integer.MIN_VALUE` works but obscures intent. Seeding with the first element
is the exam's preferred style.

**Average** = sum / count — cast the sum first:
`double avg = (double) sum / arr.length;`

**Searching for a position** (linear search):

```java
public static int indexOf(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;          // found: position
        }
    }
    return -1;                 // not found convention
}
```

`-1` as "absent" is a universal Java convention — it can never be confused
with a real index.
"""

L3 = r"""
**Shifting and inserting** — the exam's hardest array operations. To remove
the element at index `k` (keeping order), shift everything after it left:

```java
// {a, b, c, d} remove index 1 → {a, c, d, ?}
for (int i = k; i < arr.length - 1; i++) {
    arr[i] = arr[i + 1];
}
```

The loop bound `length - 1` is the crux: on the last pass, `arr[i + 1]` is
the final element — one past that would be out of bounds. The last slot now
holds a duplicate; track a logical size separately when needed.

**Copying**: `copy = original;` copies the *reference*, not the values —
both names then mutate one array. The value copy needs a loop (or
`Arrays.copyOf`):

```java
int[] copy = new int[arr.length];
for (int i = 0; i < arr.length; i++) {
    copy[i] = arr[i];
}
```

**Swapping** two elements needs the three-line temp dance:

```java
int temp = arr[i];
arr[i] = arr[j];
arr[j] = temp;
```

Forgetting the temp silently destroys one value — the classic bug the wrong
solutions below commit.
"""

write_module(
    M,
    "Arrays",
    "Declaration and traversal, length vs indexes, accumulation, linear search, shifting, copying and swapping.",
    "Mảng",
    "Khai báo và duyệt, length so với chỉ số, tích lũy, tìm kiếm tuyến tính, dịch chuyển, sao chép và hoán đổi.",
    lessons=["apc-m9-basics", "apc-m9-accumulate", "apc-m9-shift", "apc-cp-m9"],
    practices=["apc-p9-arrays"],
)

write_lesson(
    M, "apc-m9-basics", "Array anatomy",
    "Creation, indexing, length, bounds, default values, both loop forms.",
    14, L1,
    "Giải phẫu mảng",
    "Tạo, đánh chỉ số, length, biên, giá trị mặc định, hai dạng vòng lặp.",
    r"""
**Mảng** giữ số lượng giá trị cố định của một kiểu, đánh số từ 0:

```java
int[] scores = new int[4];          // {0, 0, 0, 0} — toàn số 0
int[] primes = {2, 3, 5, 7};        // dạng literal
primes[0] = 2;                       // chỉ số (đọc/ghi)
int n = primes.length;               // length LÀ TRƯỜNG — không có ngoặc!
```

`length` không có `()` là đặc thù của mảng (String dùng `length()`,
ArrayList dùng `size()` — đề thi cố tình trộn cả ba).

**Biên**: chỉ số hợp lệ là 0 .. length − 1. Chỉ số 4 trên mảng dài 4 biên
dịch tốt và ném `ArrayIndexOutOfBoundsException` khi **chạy** — vấp phổ biến
nhất trong code sinh viên.

**Giá trị mặc định**: `new int[4]` toàn 0; `new boolean[4]` toàn false;
`new String[4]` toàn **null** (mảng tham chiếu, không phải đối tượng).

Hai vòng lặp duyệt:

```java
for (int i = 0; i < arr.length; i++) {   // khi cần chỉ số
    System.out.println(arr[i]);
}

for (int x : arr) {                      // enhanced for: chỉ giá trị
    System.out.println(x);
}
```

Enhanced for không thể *sửa* mảng (biến của nó là bản sao) và không cho biết
vị trí — chỉ dùng để đọc.
""",
)

write_lesson(
    M, "apc-m9-accumulate", "Accumulate, count, extremum, search",
    "Sum/count/max patterns, seeding the extremum, linear search with -1.",
    14, L2,
    "Tích lũy, đếm, cực trị, tìm kiếm",
    "Các mẫu tổng/đếm/max, khởi tạo cực trị, tìm tuyến tính với -1.",
    r"""
Ba mẫu tích lũy (khai báo **ngoài**, cập nhật **trong**):

```java
// tổng
int sum = 0;
for (int x : arr) { sum += x; }

// đếm theo quy tắc
int evens = 0;
for (int x : arr) { if (x % 2 == 0) evens++; }

// cực trị — khởi tạo bằng phần tử đầu, không phải 0
int max = arr[0];
for (int i = 1; i < arr.length; i++) {
    if (arr[i] > max) {
        max = arr[i];
    }
}
```

Vì sao khởi tạo bằng `arr[0]`? Khởi tạo `max = 0` là sai với mảng toàn số âm
(đáp án sẽ là 0 — một phần tử không hề có mặt) và `max = Integer.MIN_VALUE`
được nhưng che mất ý định. Khởi tạo bằng phần tử đầu là phong cách đề thi
ưa chuộng.

**Trung bình** = tổng / số phần tử — ép kiểu tổng trước:
`double avg = (double) sum / arr.length;`

**Tìm vị trí** (tìm kiếm tuyến tính):

```java
public static int indexOf(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;          // thấy: vị trí
        }
    }
    return -1;                 // quy ước không tìm thấy
}
```

`-1` như "vắng mặt" là quy ước phổ quát của Java — không bao giờ lẫn với chỉ
số thật.
""",
)

write_lesson(
    M, "apc-m9-shift", "Shift, copy, swap",
    "Removal by shifting, reference vs value copies, the temp-variable swap.",
    12, L3,
    "Dịch, sao chép, hoán đổi",
    "Xóa bằng cách dịch, sao chép tham chiếu so với giá trị, hoán đổi bằng biến tạm.",
    r"""
**Dịch và chèn** — những phép toán mảng khó nhất của đề thi. Để xóa phần tử
tại chỉ số `k` (giữ thứ tự), dịch mọi phần tử sau nó sang trái:

```java
// {a, b, c, d} xóa chỉ số 1 → {a, c, d, ?}
for (int i = k; i < arr.length - 1; i++) {
    arr[i] = arr[i + 1];
}
```

Chặn vòng lặp `length - 1` là mấu chốt: lượt cuối, `arr[i + 1]` là phần tử
cuối — vượt qua một bước nữa là ra ngoài biên. Ô cuối giờ giữ một bản sao
lặp; khi cần, theo dõi riêng một "kích thước logic".

**Sao chép**: `copy = original;` sao chép *tham chiếu*, không phải giá trị —
hai tên sẽ cùng sửa một mảng. Bản sao giá trị cần vòng lặp (hoặc
`Arrays.copyOf`):

```java
int[] copy = new int[arr.length];
for (int i = 0; i < arr.length; i++) {
    copy[i] = arr[i];
}
```

**Hoán đổi** hai phần tử cần ba dòng biến tạm:

```java
int temp = arr[i];
arr[i] = arr[j];
arr[j] = temp;
```

Quên biến tạm âm thầm phá hủy một giá trị — lỗi kinh điển mà các lời giải
sai dưới đây phạm phải.
""",
)

BOILER_SUM = r"""public class Solution {
    public static int sum(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_MAX = r"""public class Solution {
    public static int maxIndex(int[] arr) {
        return -1; // replace: index of the largest element
    }
}
"""

BOILER_COUNT = r"""public class Solution {
    public static int countAbove(int[] arr, int threshold) {
        return 0; // replace
    }
}
"""

BOILER_REV = r"""public class Solution {
    public static int[] reversed(int[] arr) {
        return arr; // replace: NEW array in opposite order
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static int total(int[] arr) {
        int sum = 0;
        for (int i = 0; i <= arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }
}
"""

CP9 = r"""public class Solution {
    public static int[] trimNegatives(int[] arr) {
        return arr; // replace: new array keeping only non-negative values, in order
    }
}
"""

P_SUM = challenge(
    "apc-m9-sum",
    "Array sum",
    "Implement `int sum(int[] arr)`: the total of all elements. Enhanced-for or indexed loop — your pick.",
    BOILER_SUM,
    [(
        "sums all",
        r"""
CjTestBase.checkEq(Solution.sum(new int[]{3, 1, 4}), 8, "three items");
CjTestBase.checkEq(Solution.sum(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.sum(new int[]{-5, 5}), 0, "cancels");
""",
        "Accumulator starts at 0; empty array must return 0.",
    )],
    level="imitation",
)

P_MAX = challenge(
    "apc-m9-maxindex",
    "Index of the maximum",
    "Implement `int maxIndex(int[] arr)`: the *position* of the largest element (first one if tied; arr is non-empty). Track the best index, not just the best value.",
    BOILER_MAX,
    [(
        "max position",
        r"""
CjTestBase.checkEq(Solution.maxIndex(new int[]{4, 9, 2}), 1, "middle max");
CjTestBase.checkEq(Solution.maxIndex(new int[]{9, 2, 9}), 0, "tie keeps first");
CjTestBase.checkEq(Solution.maxIndex(new int[]{7}), 0, "single");
""",
        "Seed bestIndex = 0; replace when arr[i] > arr[bestIndex].",
    )],
    level="guided",
)

P_COUNT = challenge(
    "apc-m9-countabove",
    "Threshold counter",
    "Implement `int countAbove(int[] arr, int threshold)`: how many elements are strictly greater than threshold.",
    BOILER_COUNT,
    [(
        "count matches",
        r"""
CjTestBase.checkEq(Solution.countAbove(new int[]{1, 5, 9}, 4), 2, "5 and 9");
CjTestBase.checkEq(Solution.countAbove(new int[]{4, 4}, 4), 0, "equal not above");
CjTestBase.checkEq(Solution.countAbove(new int[]{}, 0), 0, "empty");
""",
        "Strictly greater: use >, not >=.",
    )],
    level="imitation",
)

P_REV = challenge(
    "apc-m9-reversed",
    "Build a reversed copy",
    "Implement `int[] reversed(int[] arr)`: a NEW array with the elements in opposite order. The original must be untouched — this is the copy-vs-reference test.",
    BOILER_REV,
    [(
        "reversed copy",
        r"""
int[] src = {1, 2, 3};
int[] out = Solution.reversed(src);
CjTestBase.checkEq(out[0], 3, "first is last");
CjTestBase.checkEq(out[2], 1, "last is first");
CjTestBase.checkEq(src[0], 1, "original untouched");
CjTestBase.checkEq(Solution.reversed(new int[]{5})[0], 5, "single");
""",
        "new int[arr.length]; then copy[i] = arr[arr.length - 1 - i].",
    )],
    level="combination",
)

P_FIX = challenge(
    "apc-m9-fix-bounds",
    "Debug the boundary",
    "`total` crashes with ArrayIndexOutOfBoundsException on every call. Fix the loop bound — the smallest possible repair.",
    BOILER_FIX,
    [(
        "no crash",
        r"""
CjTestBase.checkEq(Solution.total(new int[]{1, 2, 3}), 6, "sums without crash");
CjTestBase.checkEq(Solution.total(new int[]{}), 0, "empty safe");
""",
        "i <= arr.length runs one index too far; use i < arr.length.",
    )],
    level="debugging",
)

CP9C = challenge(
    "apc-cp-m9-trim",
    "Checkpoint: filter into a new array",
    "Implement `int[] trimNegatives(int[] arr)`: return a new array holding only the non-negative elements of arr, in their original order. Two passes make it clean: first count them, then fill.",
    CP9,
    [(
        "filter copy",
        r"""
int[] out = Solution.trimNegatives(new int[]{3, -1, 4, -1, 5});
CjTestBase.checkEq(out.length, 3, "three survivors");
CjTestBase.checkEq(out[0], 3, "order kept a");
CjTestBase.checkEq(out[2], 5, "order kept b");
CjTestBase.checkEq(Solution.trimNegatives(new int[]{-2, -3}).length, 0, "all filtered");
""",
        "Count the survivors first to size the new array, then fill it.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p9-arrays", "Array reps", "Accumulate, locate, count, copy, and debug boundaries.",
    "Luyện mảng", "Tích lũy, định vị, đếm, sao chép, sửa biên.",
    after_lesson="apc-m9-accumulate", minutes=55, difficulty="beginner",
    challenges=[P_SUM, P_MAX, P_COUNT, P_REV, P_FIX],
    vi_challenges={
        "apc-m9-sum": vi_challenge("Tổng mảng", "Cài đặt `int sum(int[] arr)`: tổng tất cả phần tử. Enhanced-for hoặc vòng có chỉ số — tùy bạn.",
            [("sums all", "Bộ tích lũy bắt đầu 0; mảng rỗng phải trả về 0.")]),
        "apc-m9-maxindex": vi_challenge("Chỉ số của giá trị lớn nhất", "Cài đặt `int maxIndex(int[] arr)`: *vị trí* của phần tử lớn nhất (lấy phần đầu nếu bằng nhau; arr khác rỗng). Theo dõi chỉ số tốt nhất, không chỉ giá trị tốt nhất.",
            [("max position", "Khởi tạo bestIndex = 0; thay khi arr[i] > arr[bestIndex].")]),
        "apc-m9-countabove": vi_challenge("Bộ đếm ngưỡng", "Cài đặt `int countAbove(int[] arr, int threshold)`: bao nhiêu phần tử lớn hơn ngưỡng một cách nghiêm ngặt.",
            [("count matches", "Lớn hơn nghiêm ngặt: dùng >, không phải >=.")]),
        "apc-m9-reversed": vi_challenge("Dựng bản sao đảo ngược", "Cài đặt `int[] reversed(int[] arr)`: một mảng MỚI với các phần tử theo thứ tự ngược. Mảng gốc không được đụng tới — đây là bài kiểm tra sao chép so với tham chiếu.",
            [("reversed copy", "new int[arr.length]; rồi copy[i] = arr[arr.length - 1 - i].")]),
        "apc-m9-fix-bounds": vi_challenge("Sửa biên", "`total` sập với ArrayIndexOutOfBoundsException ở mọi lời gọi. Sửa chặn vòng lặp — sửa chữa nhỏ nhất có thể.",
            [("no crash", "i <= arr.length chạy vượt một chỉ số; dùng i < arr.length.")]),
    },
    solutions=[
        ("apc-m9-sum", r"""public class Solution {
    public static int sum(int[] arr) {
        int total = 0;
        for (int x : arr) {
            total += x;
        }
        return total;
    }
}
""",
         r"""public class Solution {
    public static int sum(int[] arr) {
        // BUG: starts the total at 1 — empty array returns 1, sums off by 1
        int total = 1;
        for (int x : arr) {
            total += x;
        }
        return total;
    }
}
"""),
        ("apc-m9-maxindex", r"""public class Solution {
    public static int maxIndex(int[] arr) {
        int best = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > arr[best]) {
                best = i;
            }
        }
        return best;
    }
}
""",
         r"""public class Solution {
    public static int maxIndex(int[] arr) {
        // BUG: tracks the value, returns it as if it were an index
        int best = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > best) {
                best = arr[i];
            }
        }
        return best;
    }
}
"""),
        ("apc-m9-countabove", r"""public class Solution {
    public static int countAbove(int[] arr, int threshold) {
        int count = 0;
        for (int x : arr) {
            if (x > threshold) {
                count++;
            }
        }
        return count;
    }
}
""",
         r"""public class Solution {
    public static int countAbove(int[] arr, int threshold) {
        // BUG: counts equal values too — boundary leaked in
        int count = 0;
        for (int x : arr) {
            if (x >= threshold) {
                count++;
            }
        }
        return count;
    }
}
"""),
        ("apc-m9-reversed", r"""public class Solution {
    public static int[] reversed(int[] arr) {
        int[] out = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            out[i] = arr[arr.length - 1 - i];
        }
        return out;
    }
}
""",
         r"""public class Solution {
    public static int[] reversed(int[] arr) {
        // BUG: copies the reference — original gets reversed too
        int[] out = arr;
        for (int i = 0; i < arr.length / 2; i++) {
            int temp = out[i];
            out[i] = out[arr.length - 1 - i];
            out[arr.length - 1 - i] = temp;
        }
        return out;
    }
}
"""),
        ("apc-m9-fix-bounds", r"""public class Solution {
    public static int total(int[] arr) {
        int sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }
}
""",
         r"""public class Solution {
    public static int total(int[] arr) {
        // BUG: original flaw kept — i <= length reads past the end
        int sum = 0;
        for (int i = 0; i <= arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m9", "Checkpoint: arrays",
    "Count-and-fill filtering into a right-sized new array.",
    22,
    r"""
trimNegatives is the two-pass pattern (count, then fill) the exam uses
whenever a fixed-size array must hold an unknown number of results. The
wrong solution to avoid: destroying the source while building the target.
""",
    "Điểm kiểm tra: mảng",
    "Lọc đếm-rồi-lắp vào mảng mới với kích thước đúng.",
    r"""
trimNegatives là mẫu hai lượt (đếm, rồi lắp) mà đề thi dùng mỗi khi mảng
kích thước cố định phải giữ số kết quả chưa biết. Lời giải sai cần tránh:
phá hủy nguồn trong khi dựng đích.
""",
    CP9C,
    vi_challenge("Điểm kiểm tra: mảng", "Cài đặt `int[] trimNegatives(int[] arr)`: trả về mảng mới chỉ giữ các phần tử không âm của arr, theo thứ tự gốc. Hai lượt sẽ gọn: đầu tiên đếm, rồi lắp.",
        [("filter copy", "Đếm số phần tử sót lại trước để cấp phát kích thước, rồi lắp vào.")]),
    solution=r"""public class Solution {
    public static int[] trimNegatives(int[] arr) {
        int count = 0;
        for (int x : arr) {
            if (x >= 0) {
                count++;
            }
        }
        int[] out = new int[count];
        int idx = 0;
        for (int x : arr) {
            if (x >= 0) {
                out[idx] = x;
                idx++;
            }
        }
        return out;
    }
}
""",
    wrong=r"""public class Solution {
    public static int[] trimNegatives(int[] arr) {
        // BUG: one pass with a wrong-sized target — crashes when negatives exist
        int[] out = new int[arr.length];
        int idx = 0;
        for (int x : arr) {
            if (x >= 0) {
                out[idx] = x;
                idx++;
            }
        }
        return out;
    }
}
""",
)
