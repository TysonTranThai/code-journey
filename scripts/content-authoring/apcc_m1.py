#!/usr/bin/env python3
"""AP CSA Core M1 — Problem-Solving Bootcamp (exam-question anatomy)."""
from apcc import *

M = "cx-bootcamp"

L1 = r"""
An AP question is a **contract**, not a conversation. Every part of it carries
obligations:

```text
Write method `int countInRange(int[] data, int lo, int hi)`
Return the number of elements of `data` that are greater than or equal
to `lo` and less than or equal to `hi`.
```

Before writing a single line, extract the contract's four parts:

1. **Name & signature** — `countInRange`, three parameters, returns `int`.
   The signature is given; you may not change it.
2. **Inputs** — `data` (an `int[]`, possibly length 0), `lo` and `hi`
   (`int`, any order).
3. **Output** — a **count**: an integer ≥ 0, returned, never printed.
4. **Conditions** — "greater than or equal to `lo`" *and* "less than or
   equal to `hi`": both bounds are inclusive. The words *is* / *or* /
   *and* / *at least* decide your operators.

The exam loves three hidden traps inside plain English:

- **inclusive vs exclusive bounds**: "from the first through the last"
  means `<=`; "between" on the AP exam is stated exactly — obey the words
  given, never a convention you remember from elsewhere.
- **count vs find**: "return the number of..." wants a counter, not the
  element and not its index.
- **return vs print**: an FRQ that asks you to *return* prints nothing.
  A solution that prints the answer scores zero for that part.

Train the reading habit: underline the return type, circle every
comparative phrase, and list the edge inputs (empty array, single element,
all matching, none matching) *before* you code.
"""

L2 = r"""
The AP style guide for humans: **solve the smallest version of the problem
first, then widen it.**

Take: *"Return true if every element of `words` has length at least `k`."*

- Smallest case: an empty array. "Every element" of nothing is vacuously
  true — return `true`.
- One element: check `words[0].length() >= k`.
- All elements: loop, and the moment one fails, return `false`. Only after
  the loop finishes may you return `true`.

```java
public static boolean allLong(String[] words, int k) {
    for (String w : words) {
        if (w.length() < k) {
            return false;
        }
    }
    return true;
}
```

Two habits this procedure builds:

1. **The early-exit pattern.** "Every / no / none" questions want you to
   return the moment the answer is decided, then give the default *after*
   the loop. Students who instead try to track a flag often initialize it
   wrong (`true` vs `false`) — decide the default from the vacuous case.
2. **The negation test.** "Every element has length ≥ k" fails exactly
   when *some* element has `length < k` — so the `if` tests the failure,
   not the success. Translating negations correctly is worth points on
   nearly every exam.

The same widening works for accumulation (sum → sum with condition →
count of condition) and for searching (does it exist → where → first
occurrence). Start where the problem is already solved; add complexity
one obligation at a time.
"""

L3 = r"""
A bug hunt is a trace with a hypothesis. Given a **plausible but wrong**
method — the exam's favorite format — run this loop:

1. **Re-read the contract.** What exactly does it promise? Most planted
   bugs are contract violations, not syntax errors.
2. **Trace a small input by hand** — 3 elements, not 10. Write every
   variable's value after each statement (a *state table*).
3. **Compare the trace to the promise.** At which statement does reality
   drift from the contract? That statement contains the bug.
4. **Fix minimally.** Change one thing; re-trace. Do not rewrite a
   working half.

Worked example — the contract says *return the index of the first
occurrence of `target`, or -1 if absent*:

```java
public static int findFirst(int[] arr, int target) {
    int pos = -1;
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            pos = i;      // keeps overwriting!
        }
    }
    return pos;
}
```

Trace `arr = {4, 7, 7}, target = 7`: `i=1` sets `pos=1`, `i=2` sets
`pos=2` → returns the **last** occurrence. The contract says *first*. The
minimal fix: `return i;` inside the `if` (early exit), or guard the
assignment with `pos == -1`. Both preserve the rest of the method.

Notice the bug was *semantic*: the code compiles, runs, and even passes a
sloppy test with `{7}`. Only a contract-faithful trace with a repeated
target exposes it. This is why Core traces by hand first and runs code
second — on the exam there is no compiler to catch it for you.
"""

write_module(
    M,
    "AP Problem-Solving Bootcamp",
    "How to read an AP question as a contract: extract signatures and bounds, widen small cases into full solutions, and hunt bugs by tracing.",
    "Trại luyện giải bài AP",
    "Đọc đề AP như một hợp đồng: tách chữ ký và biên độ, mở rộng trường hợp nhỏ thành lời giải đầy đủ, và bắt lỗi bằng truy vết.",
    lessons=["cx-m1-contract", "cx-m1-widen", "cx-m1-bughunt", "cx-cp-m1"],
    practices=["cx-p1-bootcamp"],
)

write_lesson(
    M, "cx-m1-contract", "Reading the contract",
    "Extract signature, inputs, output, and bound words before writing code.",
    10, L1,
    "Đọc hợp đồng đề bài",
    "Tách chữ ký, đầu vào, đầu ra và các từ so sánh trước khi viết mã.",
    r"""
Một câu hỏi AP là một **hợp đồng**, không phải một cuộc trò chuyện. Mọi
phần của nó đều mang nghĩa vụ:

```text
Viết phương thức `int countInRange(int[] data, int lo, int hi)`
Trả về số phần tử của `data` mà lớn hơn hoặc bằng `lo` và nhỏ hơn
hoặc bằng `hi`.
```

Trước khi viết dòng mã nào, tách hợp đồng thành bốn phần:

1. **Tên & chữ ký** — `countInRange`, ba tham số, trả về `int`.
   Chữ ký đã cho sẵn; bạn không được đổi nó.
2. **Đầu vào** — `data` (một `int[]`, có thể dài 0), `lo` và `hi`
   (`int`, thứ tự bất kỳ).
3. **Đầu ra** — một **số đếm**: số nguyên ≥ 0, được *trả về*, không in.
4. **Điều kiện** — "lớn hơn hoặc bằng `lo`" *và* "nhỏ hơn hoặc bằng
   `hi`": cả hai biên đều là **kèm cả mép** (inclusive). Các từ
   *là / hoặc / và / ít nhất* quyết định toán tử của bạn.

Đề thi rất thích ba cái bẫy ẩn trong tiếng Anh đơn giản:

- **biên kèm/không kèm**: "từ đầu đến cuối" nghĩa là `<=`; đề AP luôn
  phát biểu chính xác — hãy theo đúng từ trong đề, không theo thói quen
  bạn nhớ từ nơi khác.
- **đếm hay tìm**: "trả về số phần tử..." muốn một bộ đếm, không phải
  phần tử và cũng không phải chỉ số của nó.
- **trả về hay in**: bài FRQ yêu cầu *trả về* thì không in gì cả. Một
  lời giải in đáp án ra màn hình được chấm điểm 0 cho phần đó.

Luyện thói quen đọc: gạch chân kiểu trả về, khoanh mọi cụm so sánh, và
liệt kê các đầu vào biên (mảng rỗng, một phần tử, tất cả khớp, không
khớp cái nào) *trước* khi viết mã.
""",
)

write_lesson(
    M, "cx-m1-widen", "Solve small, then widen",
    "The early-exit pattern, the negation test, and widening minimal cases.",
    10, L2,
    "Giải nhỏ rồi mở rộng",
    "Mẫu thoát sớm, phép kiểm tra phủ định, và mở rộng từ trường hợp nhỏ nhất.",
    r"""
Nguyên tắc giải nhanh: **giải phiên bản nhỏ nhất của bài toán trước, rồi
mở rộng dần.**

Lấy đề: *"Trả về true nếu mọi phần tử của `words` đều có độ dài ít nhất
`k`."*

- Trường hợp nhỏ nhất: mảng rỗng. "Mọi phần tử" của tập rỗng là đúng một
  cách chân không (vacuously true) — trả về `true`.
- Một phần tử: kiểm tra `words[0].length() >= k`.
- Mọi phần tử: dùng vòng lặp, vừa thấy cái sai thì lập tức `return
  false`. Chỉ sau khi vòng lặp chạy hết mới được `return true`.

```java
public static boolean allLong(String[] words, int k) {
    for (String w : words) {
        if (w.length() < k) {
            return false;
        }
    }
    return true;
}
```

Hai thói quen mà quy trình này rèn:

1. **Mẫu thoát sớm.** Câu hỏi kiểu "mọi / không có / không phần tử nào"
   muốn bạn trả lời ngay khi kết quả được quyết định, rồi mới đưa đáp án
   mặc định *sau* vòng lặp. Học sinh cố dùng cờ (flag) thường khởi tạo
   sai (`true` hay `false`) — hãy quyết định giá trị mặc định từ trường
   hợp chân không.
2. **Phép kiểm tra phủ định.** "Mọi phần tử có độ dài ≥ k" sai đúng khi
   *tồn tại* một phần tử có `length < k` — nên `if` kiểm tra điều **sai**,
   không phải điều đúng. Dịch phủ định đúng giúp bạn lấy điểm gần như ở
   mọi câu thi.

Cách mở rộng tương tự áp dụng cho cộng dồn (tổng → tổng có điều kiện →
đếm điều kiện) và tìm kiếm (có tồn tại → ở đâu → lần đầu xuất hiện).
Bắt đầu từ chỗ bài toán đã được giải; thêm phức tạp từng nghĩa vụ một.
""",
)

write_lesson(
    M, "cx-m1-bughunt", "Bug hunting by trace",
    "Trace small inputs, compare against the contract, fix minimally.",
    12, L3,
    "Bắt lỗi bằng truy vết",
    "Truy vết đầu vào nhỏ, đối chiếu với hợp đồng, sửa tối thiểu.",
    r"""
Đi săn lỗi là một phép truy vết kèm giả thuyết. Với một phương thức
**hợp lệ nhưng sai** — dạng ưa thích của đề thi — chạy vòng lặp này:

1. **Đọc lại hợp đồng.** Nó hứa chính xác điều gì? Phần lớn lỗi cài cắm
   là vi phạm hợp đồng, không phải lỗi cú pháp.
2. **Truy vết một đầu vào nhỏ bằng tay** — 3 phần tử, đừng dùng 10. Ghi
   giá trị mọi biến sau mỗi câu lệnh (một *bảng trạng thái*).
3. **Đối chiếu truy vết với lời hứa.** Tại câu lệnh nào thực tế lệch khỏi
   hợp đồng? Câu lệnh đó chứa lỗi.
4. **Sửa tối thiểu.** Đổi đúng một thứ; truy vết lại. Đừng viết lại nửa
   phần đang chạy đúng.

Ví dụ làm mẫu — hợp đồng: *trả về chỉ số của lần xuất hiện **đầu tiên**
của `target`, hoặc -1 nếu vắng mặt*:

```java
public static int findFirst(int[] arr, int target) {
    int pos = -1;
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            pos = i;      // cứ ghi đè mãi!
        }
    }
    return pos;
}
```

Truy vết `arr = {4, 7, 7}, target = 7`: `i=1` đặt `pos=1`, `i=2` đặt
`pos=2` → trả về lần xuất hiện **cuối**. Hợp đồng nói *đầu tiên*. Sửa
tối thiểu: `return i;` ngay trong `if` (thoát sớm), hoặc chỉ gán khi
`pos == -1`. Cả hai đều giữ nguyên phần còn lại của phương thức.

Chú ý: lỗi mang tính *ngữ nghĩa* — mã biên dịch được, chạy được, thậm chí
đạt một bài kiểm tra qua loa với `{7}`. Chỉ một truy vết trung thành với
hợp đồng, dùng target lặp lại, mới phơi ra lỗi. Vì vậy Core luôn truy vết
bằng tay trước, chạy mã sau — phòng thi không có trình biên dịch giúp bạn.
""",
)

BOILER_FIND = r"""public class Solution {
    public static int countInRange(int[] data, int lo, int hi) {
        return 0; // replace: count elements with lo <= value <= hi
    }
}
"""

BOILER_LONG = r"""public class Solution {
    public static boolean anyLonger(String[] words, int k) {
        return false; // replace: true when SOME word has length > k
    }
}
"""

BOILER_FINDMAX = r"""public class Solution {
    public static int findMaxIndex(int[] arr) {
        // CONTRACT: index of the FIRST occurrence of the maximum;
        // arr.length >= 1. Currently returns the last occurrence.
        int best = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] >= arr[best]) {
                best = i;
            }
        }
        return best;
    }
}
"""

BOILER_SUMSKIP = r"""public class Solution {
    public static int sumSkipNeg(int[] arr) {
        // CONTRACT: sum of the NON-NEGATIVE elements only.
        int total = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] < 0) {
                total += arr[i];
            }
        }
        return total;
    }
}
"""

BOILER_REVERSE = r"""public class Solution {
    public static int[] reversed(int[] arr) {
        // CONTRACT: return a NEW array, the reverse of arr
        // (arr must be unchanged). arr may have length 0.
        int[] out = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            out[i] = arr[i];
        }
        return out;
    }
}
"""

BOILER_CP_TRACE = r"""public class Solution {
    public static String mystery(int n) {
        String out = "";
        for (int i = 1; i <= n; i++) {
            if (i % 3 == 0) {
                out += "#";
            } else if (i % 2 == 0) {
                out += ".";
            } else {
                out += "o";
            }
        }
        return out;
    }
}
"""

P_COUNT = challenge(
    "cx-m1-count-range",
    "Implement the contract",
    "Implement `int countInRange(int[] data, int lo, int hi)`: the number of elements `v` with `lo <= v <= hi`. Both bounds are inclusive; `data` may be empty. Return the count — print nothing.",
    BOILER_FIND,
    [(
        "counts inclusive range",
        r"""
CjTestBase.checkEq(Solution.countInRange(new int[]{1, 5, 7, 9}, 5, 9), 3, "both bounds inclusive");
CjTestBase.checkEq(Solution.countInRange(new int[]{1, 2, 3}, 4, 9), 0, "none match");
CjTestBase.checkEq(Solution.countInRange(new int[]{}, 0, 100), 0, "empty array");
CjTestBase.checkEq(Solution.countInRange(new int[]{4}, 4, 4), 1, "single exact hit");
CjTestBase.checkEq(Solution.countInRange(new int[]{-5, 0, 5}, -5, 5), 3, "negatives included");
""",
        "One loop, one counter, two comparisons joined by &&.",
    )],
    level="imitation",
)

P_ANY = challenge(
    "cx-m1-any-longer",
    "Existence check",
    "Implement `boolean anyLonger(String[] words, int k)`: true when **at least one** word has length strictly greater than `k`, false otherwise (including the empty array). Return — do not print.",
    BOILER_LONG,
    [(
        "exists a long word",
        r"""
CjTestBase.checkEq(Solution.anyLonger(new String[]{"a", "bcd"}, 2), true, "bcd has length 3 > 2");
CjTestBase.checkEq(Solution.anyLonger(new String[]{"a", "bb"}, 2), false, "nothing longer than 2");
CjTestBase.checkEq(Solution.anyLonger(new String[]{}, 0), false, "empty is false");
CjTestBase.checkEq(Solution.anyLonger(new String[]{"xyz"}, 2), true, "single word qualifies");
""",
        "Loop; return true the moment one word qualifies; return false after.",
    )],
    level="guided",
)

P_MAXIDX = challenge(
    "cx-m1-fix-first-max",
    "Diagnose the planted bug",
    "The method must return the index of the **first** occurrence of the maximum. It compiles and often looks right. Trace it by hand on `{2, 9, 9}` and `{1, 3, 3, 3}` before touching the code, then fix it minimally.",
    BOILER_FINDMAX,
    [(
        "first max index",
        r"""
CjTestBase.checkEq(Solution.findMaxIndex(new int[]{2, 9, 9}), 1, "first of the two 9s");
CjTestBase.checkEq(Solution.findMaxIndex(new int[]{1, 3, 3, 3}), 1, "first of three 3s");
CjTestBase.checkEq(Solution.findMaxIndex(new int[]{7}), 0, "single element");
CjTestBase.checkEq(Solution.findMaxIndex(new int[]{-2, -1, -2}), 1, "works with negatives");
""",
        ">= lets later equal values overwrite the winner; strict > keeps the first.",
    )],
    level="debugging",
)

P_SKIP = challenge(
    "cx-m1-fix-skip-neg",
    "Second diagnosis",
    "`sumSkipNeg` must return the sum of the **non-negative** elements only. Trace `{3, -1, 4}` against the contract, find the drift, and repair it.",
    BOILER_SUMSKIP,
    [(
        "skips negatives",
        r"""
CjTestBase.checkEq(Solution.sumSkipNeg(new int[]{3, -1, 4}), 7, "3 + 4 only");
CjTestBase.checkEq(Solution.sumSkipNeg(new int[]{-1, -2}), 0, "all negative contributes nothing");
CjTestBase.checkEq(Solution.sumSkipNeg(new int[]{}), 0, "empty sum is 0");
CjTestBase.checkEq(Solution.sumSkipNeg(new int[]{0, 5}), 5, "zero counts as non-negative");
""",
        "The if adds the negatives instead of skipping them; invert the condition.",
    )],
    level="debugging",
)

P_REV = challenge(
    "cx-m1-reversed-copy",
    "Widen a minimal case",
    "Implement `int[] reversed(int[] arr)` returning a **new** array with the elements in reverse order; `arr` itself must be unchanged, and an empty input yields an empty output.",
    BOILER_REVERSE,
    [(
        "reversed copy",
        r"""
int[] src = {1, 2, 3};
int[] got = Solution.reversed(src);
CjTestBase.checkEq(got, new int[]{3, 2, 1}, "reversed order");
CjTestBase.checkEq(src, new int[]{1, 2, 3}, "source untouched");
CjTestBase.checkEq(Solution.reversed(new int[]{}), new int[]{}, "empty in, empty out");
CjTestBase.checkEq(Solution.reversed(new int[]{9}), new int[]{9}, "single element");
""",
        "out[i] = arr[arr.length - 1 - i] — test the index algebra on length 3.",
    )],
    level="independent",
)

CP1 = challenge(
    "cx-cp-m1-trace",
    "Checkpoint: trace, then predict",
    "Trace `mystery` by hand for n = 7 (a state table for `i` and `out` helps). The method is already correct — your job is to **predict** what `mystery(7)` returns and what `mystery(0)` returns, then encode exactly that behavior by implementing `mystery` yourself from the trace rules.",
    BOILER_CP_TRACE,
    [(
        "pattern from trace",
        r"""
CjTestBase.checkEq(Solution.mystery(7), "o.#.o#o", "n = 7 trace");
CjTestBase.checkEq(Solution.mystery(6), "o.#.o#", "n = 6 trace");
CjTestBase.checkEq(Solution.mystery(1), "o", "n = 1");
CjTestBase.checkEq(Solution.mystery(0), "", "empty loop, empty string");
CjTestBase.checkEq(Solution.mystery(3), "o.#", "first three positions");
""",
        "i=1 o, i=2 ., i=3 #, i=4 ., i=5 o, i=6 #, i=7 o — the given loop already does this.",
    )],
    level="independent",
)

write_practice(
    M, "cx-p1-bootcamp", "Bootcamp drills",
    "Implement contracts, diagnose planted bugs, and widen minimal cases.",
    "Bài tập trại luyện",
    "Hiện thực hợp đồng, chẩn đoán lỗi cài cắm, và mở rộng từ trường hợp nhỏ.",
    after_lesson="cx-m1-widen", minutes=45, difficulty="intermediate",
    challenges=[P_COUNT, P_ANY, P_MAXIDX, P_SKIP, P_REV],
    vi_challenges={
        "cx-m1-count-range": vi_challenge("Hiện thực hợp đồng",
            "Hiện thực `int countInRange(int[] data, int lo, int hi)`: số phần tử `v` với `lo <= v <= hi`. Cả hai biên đều kèm cả mép; `data` có thể rỗng. Trả về số đếm — đừng in.",
            [("counts inclusive range", "Một vòng lặp, một bộ đếm, hai phép so sánh nối bằng &&.")]),
        "cx-m1-any-longer": vi_challenge("Kiểm tra tồn tại",
            "Hiện thực `boolean anyLonger(String[] words, int k)`: true khi **có ít nhất một** từ dài hơn `k`, ngược lại false (kể cả mảng rỗng). Trả về — đừng in.",
            [("exists a long word", "Vòng lặp; vừa thấy một từ đạt yêu cầu thì trả về true; sau vòng lặp trả về false.")]),
        "cx-m1-fix-first-max": vi_challenge("Chẩn đoán lỗi cài cắm",
            "Phương thức phải trả về chỉ số của lần xuất hiện **đầu tiên** của giá trị lớn nhất. Nó biên dịch được và thường trông đúng. Hãy truy vết bằng tay trên `{2, 9, 9}` và `{1, 3, 3, 3}` trước khi sửa, rồi sửa tối thiểu.",
            [("first max index", "Dấu >= cho giá trị bằng sau này ghi đè người thắng; dấu > giữ lại phần tử đầu.")]),
        "cx-m1-fix-skip-neg": vi_challenge("Chẩn đoán thứ hai",
            "`sumSkipNeg` phải trả về tổng các phần tử **không âm**. Truy vết `{3, -1, 4}` theo hợp đồng, tìm chỗ lệch, rồi sửa.",
            [("skips negatives", "Câu if lại cộng các số âm thay vì bỏ qua; đảo điều kiện.")]),
        "cx-m1-reversed-copy": vi_challenge("Mở rộng trường hợp nhỏ",
            "Hiện thực `int[] reversed(int[] arr)` trả về một mảng **mới** với các phần tử theo thứ tự ngược; bản thân `arr` không được đổi, và đầu vào rỗng cho kết quả rỗng.",
            [("reversed copy", "out[i] = arr[arr.length - 1 - i] — thử đại số chỉ số với mảng dài 3.")]),
    },
    solutions=[
        ("cx-m1-count-range", BOILER_FIND.replace("return 0; // replace: count elements with lo <= value <= hi",
            "int count = 0;\n        for (int v : data) {\n            if (v >= lo && v <= hi) {\n                count++;\n            }\n        }\n        return count;"),
         BOILER_FIND.replace("lo <= value <= hi", "lo < value < hi")),
        ("cx-m1-any-longer", BOILER_LONG.replace("return false; // replace: true when SOME word has length > k",
            "for (String w : words) {\n            if (w.length() > k) {\n                return true;\n            }\n        }\n        return false;"),
         BOILER_LONG.replace("w.length() > k", "w.length() >= k").replace(
             "return false; // replace: true when SOME word has length > k",
             "for (String w : words) {\n            if (w.length() >= k) {\n                return true;\n            }\n        }\n        return false;")),
        ("cx-m1-fix-first-max", BOILER_FINDMAX.replace("if (arr[i] >= arr[best])", "if (arr[i] > arr[best])"),
         BOILER_FINDMAX.replace("if (arr[i] >= arr[best])", "if (arr[i] >= arr[best]) { /* unchanged */ }")
            .replace("int best = 0;", "int best = arr.length - 1;")
            .replace("for (int i = 0; i < arr.length; i++)", "for (int i = arr.length - 1; i >= 0; i--)")),
        ("cx-m1-fix-skip-neg", BOILER_SUMSKIP.replace("if (arr[i] < 0) {\n                total += arr[i];\n            }",
            "if (arr[i] >= 0) {\n                total += arr[i];\n            }"),
         BOILER_SUMSKIP.replace("if (arr[i] < 0) {\n                total += arr[i];\n            }",
            "if (arr[i] <= 0) {\n                total += arr[i];\n            }")),
        ("cx-m1-reversed-copy", BOILER_REVERSE.replace("out[i] = arr[i];", "out[i] = arr[arr.length - 1 - i];"),
         BOILER_REVERSE.replace("out[i] = arr[i];", "out[i] = arr[i]; // BUG: copies without reversing")),
    ],
)

write_checkpoint(
    M, "cx-cp-m1", "Checkpoint: trace like the exam",
    "Derive a program's behavior from a hand trace, then reproduce it.",
    20,
    r"""
You traced a 7-step loop by hand and predicted its output before running
anything — the core exam skill. The pattern (i=1 `o`, i=2 `.`, i=3 `#`,
i=4 `.`, i=5 `o`, i=6 `#`, i=7 `o`) came from the *divisibility rules*, not
from luck: multiples of 3 are checked first, so 6 is `#` even though it is
also even. The checkpoint asked you to *encode* the traced behavior: when
you can both predict and reproduce, you own the concept. Next module:
scaling this tracing discipline to methods calling methods, with real
object state.
""",
    "Điểm kiểm tra: truy vết như phòng thi",
    "Suy ra hành vi chương trình từ truy vết tay, rồi tái hiện nó.",
    r"""
Bạn đã truy vết một vòng lặp 7 bước bằng tay và dự đoán kết quả trước khi
chạy bất cứ thứ gì — kỹ năng cốt lõi của phòng thi. Bài kiểm tra yêu cầu bạn
*tái hiện* hành vi đã truy vết: khi vừa dự đoán được vừa tái hiện được, bạn
đã làm chủ khái niệm. Module sau: mở rộng kỷ luật truy vết sang phương thức
gọi phương thức, với trạng thái đối tượng thật.
""",
    CP1,
    vi_challenge("Điểm kiểm tra: truy vết như phòng thi",
        "Truy vết `mystery` bằng tay với n = 7 (bảng trạng thái cho `i` và `out` sẽ giúp). Phương thức đã đúng — nhiệm vụ của bạn là **dự đoán** `mystery(7)` và `mystery(0)` trả về gì, rồi hiện thực lại `mystery` từ chính các luật truy vết.",
        [("pattern from trace", "i=1 o, i=2 ., i=3 #, i=4 ., i=5 o, i=6 #, i=7 o — vòng lặp đã cho đã làm đúng vậy.")]),
    solution=BOILER_CP_TRACE,
    wrong=r"""public class Solution {
    public static String mystery(int n) {
        String out = "";
        for (int i = 1; i <= n; i++) {
            if (i % 2 == 0) {
                out += ".";
            } else if (i % 3 == 0) {
                out += "#";
            } else {
                out += "o";
            }
        }
        return out;
    }
}
""",
)
