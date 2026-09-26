#!/usr/bin/env python3
"""AP CSA Core M2 — Code Tracing Mastery (state tables, calls, objects)."""
from apcc import *

M = "cx-tracing"

L1 = r"""
A **state table** is the exam's native language. One row per step, one
column per variable — never keep state in your head.

```java
int a = 2;
int b = a * 3;
a = a + b;
b = a - b;
```

| step | statement      | a | b |
| ---- | -------------- | - | - |
| 1    | `a = 2`        | 2 | – |
| 2    | `b = a * 3`    | 2 | 6 |
| 3    | `a = a + b`    | 8 | 6 |
| 4    | `b = a - b`    | 8 | 2 |

Two discipline rules make tracing mechanical:

1. **Right side first, then assign.** In step 3, `a + b` uses the *old*
   values (2 and 6) — `a` becomes 8, not 12. Assignment never re-reads
   its own left side.
2. **New row per statement, even when nothing changes.** Gaps are where
   mistakes hide. If a variable is untouched, copy its value down.

Swap puzzles like the one above appear on every exam: after
`a = a + b; b = a - b;`, `b` holds the old `a` (8 − 6 = 2), and a third
statement `a = a - b;` would complete the swap. Tracing beats memorizing
the trick — the table always tells you where you are.
"""

L2 = r"""
Method calls add one rule to your table: **each call gets its own frame** —
its own row block for parameters and locals — and returns exactly one
value to the exact spot it was called from.

```java
public static int twist(int n) {
    n = n + 3;
    return n * 2;
}
```

Trace `x = 5;` then `x = twist(x);`:

1. Call `twist(5)`: new frame, `n = 5`.
2. `n = n + 3` → 8. Return `8 * 2 = 16`.
3. Frame dies. Assignment: `x = 16`.

What does **not** happen: the method cannot see or change the caller's
`x`. Primitives are copied. The classic exam probe:

```java
public static void bump(int n) { n = n + 1; }
// ...
int x = 7;
bump(x);
System.out.println(x);   // 7 — the copy was changed, not x
```

References behave differently: the *reference* is copied, but both copies
point at the same object.

```java
public static void grow(int[] arr) { arr[0] = arr[0] + 10; }
// ...
int[] data = {1, 2};
grow(data);
System.out.println(data[0]);   // 11 — the shared object changed
```

So the table rule is: parameter = a copy of the value. For primitives the
value is the number; for objects the value is the arrow to the object.
Draw the arrow when in doubt.
"""

L3 = r"""
Objects extend the table with one row per **object**, referenced by name:

```java
Counter c = new Counter();
Counter d = c;          // two names, ONE object
c.up(); c.up(); d.up();
System.out.println(c.get());   // 3
System.out.println(d.get());   // 3 — same object
```

| object | count |
| ------ | ----- |
| the one `c` and `d` share | 3 |

The three exam-favorite object questions, and how the table answers them:

1. **Alias or copy?** `d = c` copies the arrow, not the object. Both
   names mutate one row.
2. **Order of calls.** `c.up()` twice then `d.up()` once is 3; if the
   calls were interleaved differently the single shared row would show
   it. Objects do not remember who touched them.
3. **State at print time.** A getter returns the row's *current* value —
   so trace every mutation before any read, in order.

Worked FRQ-style trace:

```java
public class Accum {
    private int total;
    public void add(int v) { if (v > 0) total += v; }
    public int get() { return total; }
}
Accum a = new Accum();
a.add(5); a.add(-2); a.add(3);
```

The object's row: `total` goes 0 → 5 → 5 → 8 (the negative add is
filtered). Any question about `a.get()` is answered by reading that row
at the right moment — including "what does a *second* Accum see?"
(nothing: each object has its own row).
"""

write_module(
    M,
    "Code Tracing Mastery",
    "State tables, call frames, parameter passing, and object rows: a mechanical discipline for predicting any program's behavior.",
    "Làm chủ truy vết mã",
    "Bảng trạng thái, khung gọi, truyền tham số và hàng đối tượng: kỷ luật cơ học để dự đoán hành vi mọi chương trình.",
    lessons=["cx-m2-table", "cx-m2-calls", "cx-m2-objects", "cx-cp-m2"],
    practices=["cx-p2-trace"],
)

write_lesson(
    M, "cx-m2-table", "The state table",
    "One row per statement, one column per variable; right side first.",
    10, L1,
    "Bảng trạng thái",
    "Mỗi câu lệnh một hàng, mỗi biến một cột; tính vế phải trước.",
    r"""
**Bảng trạng thái** là ngôn ngữ mẹ đẻ của đề thi. Mỗi bước một hàng, mỗi
biến một cột — đừng bao giờ giữ trạng thái trong đầu.

```java
int a = 2;
int b = a * 3;
a = a + b;
b = a - b;
```

| bước | câu lệnh       | a | b |
| ---- | -------------- | - | - |
| 1    | `a = 2`        | 2 | – |
| 2    | `b = a * 3`    | 2 | 6 |
| 3    | `a = a + b`    | 8 | 6 |
| 4    | `b = a - b`    | 8 | 2 |

Hai luật kỷ luật khiến truy vết trở nên cơ học:

1. **Tính vế phải trước, rồi gán.** Ở bước 3, `a + b` dùng giá trị *cũ*
   (2 và 6) — `a` thành 8 chứ không phải 12. Phép gán không bao giờ đọc
   lại vế trái của chính nó.
2. **Mỗi câu lệnh một hàng mới, kể cả khi không gì đổi.** Khoảng trống là
   nơi lỗi nấp mình. Biến không bị động đến thì sao chép giá trị xuống.

Các câu đố hoán đổi như trên xuất hiện ở mọi kỳ thi: sau
`a = a + b; b = a - b;`, `b` giữ `a` cũ (8 − 6 = 2), và câu thứ ba
`a = a - b;` sẽ hoàn tất phép hoán đổi. Truy vết thắng việc học thuộc mẹo —
bảng luôn cho biết bạn đang ở đâu.
""",
)

write_lesson(
    M, "cx-m2-calls", "Calls and frames",
    "Each call gets its own frame; primitives copy values, references share objects.",
    12, L2,
    "Lời gọi và khung",
    "Mỗi lời gọi có khung riêng; kiểu nguyên thủy sao chép giá trị, tham chiếu dùng chung đối tượng.",
    r"""
Lời gọi phương thức thêm một luật vào bảng: **mỗi lời gọi có khung riêng** —
khối hàng riêng cho tham số và biến cục bộ — và trả về đúng một giá trị
tại đúng chỗ nó được gọi.

```java
public static int twist(int n) {
    n = n + 3;
    return n * 2;
}
```

Truy vết `x = 5;` rồi `x = twist(x);`:

1. Gọi `twist(5)`: khung mới, `n = 5`.
2. `n = n + 3` → 8. Trả về `8 * 2 = 16`.
3. Khung biến mất. Phép gán: `x = 16`.

Điều **không** xảy ra: phương thức không thể nhìn thấy hay đổi `x` của
người gọi. Kiểu nguyên thủy được sao chép. Câu hỏi thi kinh điển:

```java
public static void bump(int n) { n = n + 1; }
// ...
int x = 7;
bump(x);
System.out.println(x);   // 7 — bản sao bị đổi, không phải x
```

Tham chiếu thì khác: *tham chiếu* được sao chép, nhưng cả hai bản sao đều
chỉ vào cùng một đối tượng.

```java
public static void grow(int[] arr) { arr[0] = arr[0] + 10; }
// ...
int[] data = {1, 2};
grow(data);
System.out.println(data[0]);   // 11 — đối tượng dùng chung đã đổi
```

Vậy luật của bảng là: tham số = bản sao của giá trị. Với kiểu nguyên thủy,
giá trị là con số; với đối tượng, giá trị là mũi tên chỉ vào đối tượng.
Khi phân vân, hãy vẽ mũi tên.
""",
)

write_lesson(
    M, "cx-m2-objects", "Object rows and aliases",
    "One row per object; aliasing, call order, and reading state at the right time.",
    12, L3,
    "Hàng đối tượng và bí danh",
    "Mỗi đối tượng một hàng; bí danh, thứ tự gọi, và đọc trạng thái đúng thời điểm.",
    r"""
Đối tượng mở rộng bảng: mỗi **đối tượng** một hàng, được gọi tên qua biến:

```java
Counter c = new Counter();
Counter d = c;          // hai tên, MỘT đối tượng
c.up(); c.up(); d.up();
System.out.println(c.get());   // 3
System.out.println(d.get());   // 3 — cùng một đối tượng
```

| đối tượng | count |
| --------- | ----- |
| đối tượng duy nhất mà `c` và `d` cùng chỉ | 3 |

Ba câu hỏi đối tượng ưa thích của đề thi, và bảng trả lời thế nào:

1. **Bí danh hay bản sao?** `d = c` sao chép mũi tên, không phải đối
   tượng. Cả hai tên cùng đập vào một hàng.
2. **Thứ tự gọi.** `c.up()` hai lần rồi `d.up()` một lần cho 3; nếu các
   lời gọi xen kẽ khác đi, hàng dùng chung duy nhất đó sẽ lộ ra. Đối
   tượng không nhớ ai đã chạm vào nó.
3. **Trạng thái tại thời điểm in.** Getter trả về giá trị *hiện tại* của
   hàng — nên hãy truy vết mọi phép biến đổi trước mọi phép đọc, theo
   thứ tự.

Truy vết kiểu FRQ:

```java
public class Accum {
    private int total;
    public void add(int v) { if (v > 0) total += v; }
    public int get() { return total; }
}
Accum a = new Accum();
a.add(5); a.add(-2); a.add(3);
```

Hàng của đối tượng: `total` đi 0 → 5 → 5 → 8 (lượt cộng âm bị lọc). Mọi
câu hỏi về `a.get()` đều trả được bằng cách đọc hàng đó đúng thời điểm —
kể cả "một Accum *thứ hai* thấy gì?" (không gì cả: mỗi đối tượng có hàng
riêng).
""",
)

BOILER_NEST = r"""public class Solution {
    public static int nested(int a, int b) {
        int r = 0;
        for (int i = a; i <= b; i++) {
            for (int j = i; j <= b; j++) {
                r += j - i;
            }
        }
        return r;
    }
}
"""

BOILER_PARAM = r"""public class Solution {
    public static int shift(int v) {
        v = v * 2;
        return v - 1;
    }
    public static int run(int v) {
        shift(v);
        return shift(v) + v;
    }
}
"""

BOILER_ALIAS = r"""public class Solution {
    public static class P {
        private int v;
        public P(int start) { v = start; }
        public void bump() { v = v + 1; }
        public int get() { return v; }
    }
    public static int demo() {
        P x = new P(10);
        P y = x;
        y.bump();
        x.bump();
        y.bump();
        return x.get() * 10 + y.get();
    }
}
"""

BOILER_CP_CALLS = r"""public class Solution {
    public static int f(int n) {
        if (n <= 0) { return 1; }
        return n + f(n - 2);
    }
}
"""

P_NESTED = challenge(
    "cx-m2-nested-loop",
    "Trace a nested loop",
    "Read `nested(a, b)` (already implemented). Set up the state table for the call `nested(1, 3)`: rows for each (i, j) pair, and predict the return value by hand first. Then make the tests pass by *keeping the code as-is* — this challenge grades your understanding, the code is already correct.",
    BOILER_NEST,
    [(
        "nested trace value",
        r"""
CjTestBase.checkEq(Solution.nested(1, 3), 4, "pairs (1,1)=0 (1,2)=1 (1,3)=2 (2,2)=0 (2,3)=1 (3,3)=0");
CjTestBase.checkEq(Solution.nested(2, 2), 0, "single pair, j - i = 0");
CjTestBase.checkEq(Solution.nested(0, 2), 4, "pairs contribute 0+1+2+0+1+0");
""",
        "For each i, inner j runs i..b; j - i is the offset. Sum them.",
    )],
    level="guided",
)

P_PARAM = challenge(
    "cx-m2-param-copies",
    "Parameter passing trace",
    "Trace `run(5)` by hand: `shift` doubles its parameter and returns v - 1, but the first call's result is **discarded**. Predict `run(5)`, then implement `run` so the tests pass — the buggy instinct is to think the discarded call changed `v`.",
    BOILER_PARAM,
    [(
        "value semantics",
        r"""
CjTestBase.checkEq(Solution.run(5), 14, "shift(5)=9, plus v=5 kept");
CjTestBase.checkEq(Solution.run(1), 2, "shift(1)=1, plus v=1");
CjTestBase.checkEq(Solution.shift(4), 7, "shift alone: 2*4 - 1");
""",
        "shift(v) returns 2v-1; run adds that to the UNCHANGED v.",
    )],
    level="guided",
)

P_ALIAS = challenge(
    "cx-m2-alias-state",
    "Aliased object state",
    "In `demo`, `x` and `y` are two names for ONE P object. Trace the three bumps on the shared row, predict what `demo()` returns, and keep the implementation consistent with your trace (fix `demo` if your hand trace disagrees with it).",
    BOILER_ALIAS,
    [(
        "aliased bumps",
        r"""
CjTestBase.checkEq(Solution.demo(), 143, "one object bumped 3 times: v=13");
""",
        "10 + 3 bumps = 13 for BOTH names; return encodes 13 and 13.",
    )],
    level="independent",
)

P_FINDBUG = challenge(
    "cx-m2-fix-accumulate",
    "Diagnose a trace bug",
    "This method should return `1 + 2 + ... + n` for n >= 1 (and 0 for n <= 0), but its loop never terminates correctly for some inputs. Trace `sumTo(3)` and `sumTo(-1)` with a state table, find the drift, and fix it.",
    r"""public class Solution {
    public static int sumTo(int n) {
        int total = 0;
        int i = 1;
        while (i != n) {
            total += i;
            i++;
        }
        return total;
    }
}
""",
    [(
        "sums correctly",
        r"""
CjTestBase.checkEq(Solution.sumTo(3), 6, "1+2+3");
CjTestBase.checkEq(Solution.sumTo(1), 1, "single term");
CjTestBase.checkEq(Solution.sumTo(0), 0, "empty sum");
CjTestBase.checkEq(Solution.sumTo(-1), 0, "negative input, empty sum");
""",
        "i != n never stops when n < 1: the counter starts ABOVE n and runs away.",
    )],
    level="debugging",
)

CP2 = challenge(
    "cx-cp-m2-recursion-trace",
    "Checkpoint: trace a recursive call",
    "Trace `f(5)` frame by frame: f(5) → f(3) → f(1) → f(-1). Predict the return value by hand, then implement `f` yourself from the trace (same shape, your own lines).",
    BOILER_CP_CALLS,
    [(
        "recursive trace",
        r"""
CjTestBase.checkEq(Solution.f(5), 10, "5 + 3 + 1 + base 1");
CjTestBase.checkEq(Solution.f(4), 7, "4 + 2 + base");
CjTestBase.checkEq(Solution.f(1), 2, "1 + f(-1) = 1 + 1");
CjTestBase.checkEq(Solution.f(0), 1, "immediate base case");
""",
        "f(5)=5+f(3)=5+3+f(1)=5+3+1+f(-1)=5+3+1+1=10 — check your arithmetic, then encode f(n<=0)->1, f(n)=n+f(n-2).",
    )],
    level="independent",
)

write_practice(
    M, "cx-p2-trace", "Tracing lab",
    "Nested loops, frames, aliases, and a runaway loop to repair.",
    "Phòng truy vết",
    "Vòng lặp lồng, khung gọi, bí danh, và một vòng lặp chạy trốn cần sửa.",
    after_lesson="cx-m2-calls", minutes=50, difficulty="intermediate",
    challenges=[P_NESTED, P_PARAM, P_ALIAS, P_FINDBUG],
    vi_challenges={
        "cx-m2-nested-loop": vi_challenge("Truy vết vòng lặp lồng",
            "Đọc `nested(a, b)` (đã hiện thực). Lập bảng trạng thái cho lời gọi `nested(1, 3)`: mỗi cặp (i, j) một hàng, và dự đoán giá trị trả về bằng tay trước. Sau đó giữ nguyên mã — bài này chấm sự hiểu của bạn, mã đã đúng sẵn.",
            [("nested trace value", "Với mỗi i, j chạy i..b; j - i là độ lệch. Cộng hết lại.")]),
        "cx-m2-param-copies": vi_challenge("Truyền tham số",
            "Truy vết `run(5)` bằng tay: `shift` nhân đôi tham số rồi trả về v - 1, nhưng kết quả lời gọi đầu bị **vứt bỏ**. Dự đoán `run(5)`, rồi hiện thực `run` để test pass — bản năng sai là nghĩ rằng lời gọi bị bỏ đã đổi `v`.",
            [("value semantics", "shift(v) trả về 2v-1; run cộng thêm với v KHÔNG ĐỔI.")]),
        "cx-m2-alias-state": vi_challenge("Trạng thái bí danh",
            "Trong `demo`, `x` và `y` là hai tên của MỘT đối tượng P. Truy vết ba lần bump trên hàng dùng chung, dự đoán `demo()` trả về gì, và giữ mã nhất quán với truy vết của bạn (sửa `demo` nếu truy vết tay lệch).",
            [("aliased bumps", "10 + 3 lần bump = 13 cho CẢ HAI tên; return mã hóa 13 và 13.")]),
        "cx-m2-fix-accumulate": vi_challenge("Chẩn đoán lỗi truy vết",
            "Phương thức này phải trả về `1 + 2 + ... + n` với n >= 1 (và 0 khi n <= 0), nhưng vòng lặp của nó không dừng đúng với một số đầu vào. Truy vết `sumTo(3)` và `sumTo(-1)` bằng bảng trạng thái, tìm chỗ lệch và sửa.",
            [("sums correctly", "i != n không bao giờ dừng khi n < 1: bộ đếm bắt đầu TRÊN n rồi chạy trốn.")]),
    },
    solutions=[
        ("cx-m2-nested-loop", BOILER_NEST,
         BOILER_NEST.replace("r += j - i;", "r += j;")),
        ("cx-m2-param-copies", BOILER_PARAM,
         BOILER_PARAM.replace("return shift(v) + v;", "return shift(v) + 1;")),
        ("cx-m2-alias-state", BOILER_ALIAS,
         BOILER_ALIAS.replace("P y = x;", "P y = new P(10);")),
        ("cx-m2-fix-accumulate",
         r"""public class Solution {
    public static int sumTo(int n) {
        int total = 0;
        int i = 1;
        while (i <= n) {
            total += i;
            i++;
        }
        return total;
    }
}
""",
         r"""public class Solution {
    public static int sumTo(int n) {
        int total = 0;
        int i = 1;
        while (i != n) {
            total += i;
            i++;
        }
        return total;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "cx-cp-m2", "Checkpoint: frames all the way down",
    "Hand-trace a recursive call chain and encode it.",
    20,
    r"""
f(5) opened four frames before any addition happened: 5, 3, 1, then the
base case f(-1) = 1. Unwinding gives 5 + 3 + 1 + 1 = 10 — check that arithmetic against your
own table; the tests are the referee.
If your table disagreed with your first guess, that disagreement is
exactly the skill being built: trust the frame-by-frame trace, not the
impression.
""",
    "Điểm kiểm tra: khung gọi tầng tầng lớp lớp",
    "Truy vết tay chuỗi gọi đệ quy và hiện thực lại.",
    r"""
f(5) mở bốn khung trước khi phép cộng nào xảy ra: 5, 3, 1, rồi trường hợp
cơ sở f(-1) = 1. Dòng chảy hồi quy cho 5 + 3 + 1 + 1 = 10 — hãy đối chiếu
phép tính này với bảng của riêng bạn; phần kiểm thử là trọng tài. Nếu bảng
của bạn lệch khỏi dự đoán đầu tiên, chính sự lệch đó là kỹ năng đang được
rèn: tin vào truy vết từng khung, đừng tin vào cảm giác.
""",
    CP2,
    vi_challenge("Điểm kiểm tra: khung gọi层层 xuống",
        "Truy vết `f(5)` từng khung: f(5) → f(3) → f(1) → f(-1). Dự đoán giá trị trả về bằng tay, rồi hiện thực `f` từ chính truy vết đó (cùng hình dạng, dòng code của bạn).",
        [("recursive trace", "f(5)=5+f(3)=5+3+f(1)=5+3+1+f(-1)=5+3+1+1=10 — kiểm tra phép tính rồi mã hóa f(n<=0)->1, f(n)=n+f(n-2).")]),
    solution=r"""public class Solution {
    public static int f(int n) {
        if (n <= 0) { return 1; }
        return n + f(n - 2);
    }
}
""",
    wrong=r"""public class Solution {
    public static int f(int n) {
        if (n <= 1) { return 1; }
        return n + f(n - 2);
    }
}
""",
)
