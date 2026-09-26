#!/usr/bin/env python3
"""AP CSA Advanced M2 — Difficult code tracing (state tables, aliasing, mutation)."""
from apx import *

M = "apx-tracing"

write_module(
    M,
    "Difficult Code Tracing",
    "State tables, object/static ledgers, aliasing, removal-while-iterating, and nested-loop shapes — hard traces with verified answers. Difficulty E3–E4.",
    "Truy vết mã khó",
    "Bảng trạng thái, sổ cái đối tượng/static, bí danh, xóa-while-duyệt, và hình dạng vòng lặp lồng — truy vết khó với đáp án đã kiểm chứng. Độ khó E3–E4.",
    lessons=["apx-m2-tables", "apx-m2-objects", "apx-m2-invariants", "apx-cp-m2"],
    practices=["apx-p2-trace"],
)

L1 = r"""
**Tracing is a skill with technique.** The exam's hardest tracing items
share three properties: many small state changes, at least one
misdirection (a variable that *looks* important but is dead), and a
boundary case in the middle of the loop, not at the start.

The state-table discipline:

1. One row per *event* (a call, an iteration, an assignment to a
   reference) — not per line.
2. One column per piece of state that can change. Include the object
   graph when references move: `a → obj1` is a row of its own.
3. Never recompute a column from memory; read the row above and apply
   exactly the code you see.
4. The answer is a cell in the table. If it is not, you traced the
   wrong thing.

Watch for the two classic misdirections: a variable updated but never
read (dead), and a variable read but never updated after the first
iteration (frozen).
"""

L2 = r"""
**Object and static state.** Instance fields belong to an object;
static fields belong to the class — one copy shared by every instance
and every call. Traces go wrong when the two mix:

```java
public class Counter {
    private static int created = 0;
    private int value;
    public Counter(int v) { value = v; created++; }
    public int bump() { value++; return value; }
}
```

After `new Counter(5)`, `new Counter(7)`, and `c.bump()` on the first:
`value` lives per-object (5→6), `created` lives on the class (2). A
question asking "what is created after these calls" is testing whether
you keep the two ledgers separate.

**ArrayList mutation** adds its own trap: `remove(i)` shifts everything
after `i` left. A loop that removes while iterating forward *skips* the
element that slid into position `i` — the classic trace answer is "one
element survived that you believe was removed."

**Pass-by-value of references**: a method can mutate the object its
parameter points at (visible to the caller) but can never make the
caller's variable point somewhere else. Traced precisely:

```java
public static void scramble(int[] a, int[] b) {
    a[0] = 100;      // visible to caller
    b = new int[9];  // local rebinding only
    b[0] = 7;        // lost
}
```
"""

L3 = r"""
**Nested loops and invariants.** When the loop nest is too deep to
simulate fully, find the *pattern of the inner loop's total*:

```java
for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
        count++;
    }
}
```

`count` gains `n + (n-1) + ... + 1` — n(n+1)/2. Recognizing the
arithmetic series beats simulating 6 rows, and the exam counts on you
seeing it. The general kit:

- **Sum shapes**: constant per pass → multiply; growing per pass →
  series; halving per pass → logarithmic.
- **Order of updates**: does the inner loop restart the accumulator?
  Does the outer loop read what the inner wrote?
- **Break/continue position**: a `break` inside the inner loop changes
  the *shape* of the series, not just the count.

When in doubt on the real exam, simulate a *small* n (2 or 3) and
generalize — small-case simulation plus pattern is faster and safer
than full tracing.
"""

VI_L1 = r"""
**Truy vết là kỹ năng có kỹ thuật.** Các bài truy vết khó nhất của đề
thi chung ba đặc điểm: nhiều thay đổi trạng thái nhỏ, ít nhất một yếu
tố đánh lạc hướng (một biến *trông* quan trọng nhưng chết), và một
trường hợp biên nằm giữa vòng lặp, không phải ở đầu.

Kỷ luật bảng trạng thái:

1. Mỗi *sự kiện* một dòng (một lời gọi, một vòng lặp, một phép gán tham
   chiếu) — không phải mỗi dòng mã.
2. Mỗi trạng thái có thể thay đổi một cột. Có tham chiếu di chuyển thì
   vẽ đồ thị đối tượng: `a → obj1` là một dòng riêng.
3. Không bao giờ tính lại một cột từ trí nhớ; đọc dòng phía trên và áp
   dụng đúng mã bạn thấy.
4. Đáp án là một ô trong bảng. Nếu không phải, bạn truy vết nhầm thứ.

Chú ý hai yếu tố đánh lạc hướng kinh điển: biến được cập nhật nhưng
không bao giờ được đọc (chết), và biến được đọc nhưng không được cập
nhật sau vòng lặp đầu (đóng băng).
"""

VI_L2 = r"""
**Trạng thái đối tượng và static.** Trường instance thuộc về một đối
tượng; trường static thuộc về lớp — một bản sao dùng chung cho mọi
thực thể và mọi lời gọi. Truy vết sai khi hai sổ cái này trộn vào nhau:

```java
public class Counter {
    private static int created = 0;
    private int value;
    public Counter(int v) { value = v; created++; }
    public int bump() { value++; return value; }
}
```

Sau `new Counter(5)`, `new Counter(7)`, và `c.bump()` trên đối tượng
đầu: `value` theo từng đối tượng (5→6), `created` theo lớp (2). Câu
hỏi "created bằng bao nhiêu sau các lời gọi" kiểm tra việc tách hai sổ.

**Biến đổi ArrayList** có bẫy riêng: `remove(i)` đẩy mọi phần tử sau `i`
sang trái. Vòng lặp vừa duyệt tăng dần vừa xóa sẽ *bỏ sót* phần tử trượt
vào vị trí `i` — đáp án truy vết kinh điển là "một phần tử còn sót dù
bạn tin nó đã bị xóa."

**Truyền tham chiếu theo giá trị**: phương thức có thể biến đổi đối
tượng mà tham số trỏ tới (caller thấy được) nhưng không bao giờ làm biến
của caller trỏ chỗ khác. Truy vết chính xác:

```java
public static void scramble(int[] a, int[] b) {
    a[0] = 100;      // caller thấy được
    b = new int[9];  // chỉ gán lại cục bộ
    b[0] = 7;        // mất
}
```
"""

VI_L3 = r"""
**Vòng lặp lồng và bất biến.** Khi tổ hợp lặp quá sâu để mô phỏng hết,
tìm *quy luật của tổng vòng trong*:

```java
for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
        count++;
    }
}
```

`count` tăng `n + (n-1) + ... + 1` — n(n+1)/2. Nhận diện cấp số cộng
nhanh hơn mô phỏng 6 dòng, và đề thi đánh vào việc bạn nhìn ra điều đó.
Bộ dụng cụ tổng quát:

- **Dạng tổng**: mỗi lượt không đổi → nhân; mỗi lượt tăng → cấp số cộng;
  mỗi lượt chia đôi → logarithm.
- **Thứ tự cập nhật**: vòng trong có khởi động lại bộ tích lũy không?
  Vòng ngoài có đọc kết quả vòng trong không?
- **Vị trí break/continue**: một `break` trong vòng trong đổi *hình dạng*
  của tổng, không chỉ đổi số đếm.

Khi bối rối trong phòng thi, mô phỏng n nhỏ (2 hoặc 3) rồi khái quát —
mô phỏng ca nhỏ cộng nhận dạng quy luật nhanh và an toàn hơn truy vết
toàn bộ.
"""

BOILER_SEQ = r"""public class Solution {
    public static String result() {
        return ""; // replace: the exact output of the code in the prompt
    }
}
"""

BOILER_VAL = r"""public class Solution {
    public static int result() {
        return 0; // replace: the final value asked for in the prompt
    }
}
"""

P_SEQ = challenge(
    "apx-m2-looptrace",
    "Trace the nested loop (E3)",
    "Trace this program **on paper** and return the exact output "
    "(concatenate everything printed, no separators):\n\n```java\n"
    "String s = \"\";\nfor (int i = 1; i <= 3; i++) {\n"
    "    for (int j = i; j <= 3; j++) {\n"
    "        s += (i * j) % 4;\n    }\n}\nSystem.out.print(s);\n```",
    BOILER_SEQ,
    [(
        "exact concatenated output",
        r"""
CjTestBase.checkEq(Solution.result(), "123021", "i*j mod 4 per pass");
""",
        "Row i=1: 1 2 3; row i=2: 0 2 (4%4, 6%4); row i=3: 1 (9%4). Concatenate in order.",
    )],
    level="independent",
    difficulty="advanced",
)

P_OBJ = challenge(
    "apx-m2-objtrace",
    "Trace object state across calls (E3)",
    "Trace this class and call sequence **on paper**:\n\n```java\n"
    "public class Meter {\n    private int units;\n    private int cap;\n"
    "    public Meter(int c) { cap = c; units = 0; }\n"
    "    public void tick() {\n        if (units < cap) { units++; }\n"
    "        else { units = units / 2; }\n    }\n"
    "    public int get() { return units; }\n}\n```\n\n"
    "Calls: `new Meter(3)`, then `tick(); tick(); tick(); tick(); tick();`.\n"
    "Return the **final** value of `get()`.",
    BOILER_VAL,
    [(
        "final meter units",
        r"""
CjTestBase.checkEq(Solution.result(), 2, "five ticks against cap 3");
""",
        "ticks: 1, 2, 3 (at cap), 3/2=1, 1+1=2.",
    )],
    level="independent",
    difficulty="advanced",
)

P_AL = challenge(
    "apx-m2-altrace",
    "Trace removal while iterating (E3)",
    "Trace this loop **on paper**:\n\n```java\n"
    "ArrayList<String> list = new ArrayList<String>();\n"
    "list.add(\"a\"); list.add(\"b\"); list.add(\"c\");\n"
    "list.add(\"d\"); list.add(\"e\");\n"
    "for (int i = 0; i < list.size(); i++) {\n"
    "    if (i % 2 == 0) { list.remove(i); }\n}\n"
    "System.out.print(list);\n```\n\n"
    "Return the printed contents exactly (bracketed, comma-space separated, "
    "as ArrayList prints — e.g. `[b, d]`).",
    BOILER_SEQ,
    [(
        "list after shifting removals",
        r"""
CjTestBase.checkEq(Solution.result(), "[b, c, e]", "remove at 0 and 2 of a shrinking list");
""",
        "i=0 removes a → [b,c,d,e]; i=1 is odd, skipped; i=2 removes d (c slid left) → [b,c,e]; i=3 is not < size 3, loop ends.",
    )],
    level="combination",
    difficulty="advanced",
)

P_STATIC = challenge(
    "apx-m2-static",
    "Two ledgers: instance vs static (E3)",
    "Trace this class and sequence **on paper**:\n\n```java\n"
    "public class Ticket {\n    private static int issued = 0;\n"
    "    private int id;\n    public Ticket() { issued++; id = issued * 10; }\n"
    "    public int getId() { return id; }\n"
    "    public static int total() { return issued; }\n}\n```\n\n"
    "Sequence: `new Ticket()`, `new Ticket()`, `new Ticket()`; then a "
    "**fourth** constructor call is skipped. Return `total() + "
    "lastTicket.getId()` where lastTicket is the third ticket.",
    BOILER_VAL,
    [(
        "static plus instance",
        r"""
CjTestBase.checkEq(Solution.result(), 33, "issued 3 + id 30");
""",
        "issued counts all three constructions; id = 10 * order for the third.",
    )],
    level="guided",
    difficulty="advanced",
)

P_SWAP = challenge(
    "apx-m2-passvalue",
    "Reference semantics under misdirection (E4)",
    "Trace this program **on paper**:\n\n```java\n"
    "public static void adjust(int[] a, int[] b, int k) {\n"
    "    a[0] += k;          // mutation of the shared array\n"
    "    b = new int[3];     // local rebinding\n"
    "    b[0] += k;          // lost\n"
    "    k = 99;             // lost\n}\n\n"
    "int[] x = {1, 2};\nint[] y = {3, 4};\nint k = 5;\n"
    "adjust(x, y, k);\nSystem.out.print(x[0] + \",\" + y[0] + \",\" + k);\n```\n\n"
    "Return the printed text exactly.",
    BOILER_SEQ,
    [(
        "output after call",
        r"""
CjTestBase.checkEq(Solution.result(), "6,3,5", "array mutation visible; rebinding and int are not");
""",
        "x[0] mutated via reference (1+5); y rebound locally only; k is a copy.",
    )],
    level="combination",
    difficulty="advanced",
)

write_practice(
    M, "apx-p2-trace", "Trace drills: state tables and misdirection",
    "Multi-step traces over loops, objects, statics, and reference semantics.",
    "Bài tập truy vết: bảng trạng thái và đánh lạc hướng",
    "Truy vết nhiều bước qua vòng lặp, đối tượng, static và ngữ nghĩa tham chiếu.",
    after_lesson="apx-m2-objects", minutes=50, difficulty="advanced",
    challenges=[P_SEQ, P_STATIC, P_OBJ, P_AL, P_SWAP],
    vi_challenges={
        "apx-m2-looptrace": vi_challenge(
            "Truy vết vòng lặp lồng (E3)",
            "Truy vết chương trình này **trên giấy** và trả về kết quả chính xác "
            "(nối mọi thứ được in, không có ký tự phân cách):\n\n```java\n"
            "String s = \"\";\nfor (int i = 1; i <= 3; i++) {\n"
            "    for (int j = i; j <= 3; j++) {\n"
            "        s += (i * j) % 4;\n    }\n}\nSystem.out.print(s);\n```",
            [("exact concatenated output", "Dòng i=1: 1 2 3; dòng i=2: 0 1; dòng i=3: 1. Nối theo thứ tự.")],
        ),
        "apx-m2-objtrace": vi_challenge(
            "Truy vết trạng thái đối tượng qua các lời gọi (E3)",
            "Truy vết lớp và chuỗi lời gọi này **trên giấy**:\n\n```java\n"
            "public class Meter {\n    private int units;\n    private int cap;\n"
            "    public Meter(int c) { cap = c; units = 0; }\n"
            "    public void tick() {\n        if (units < cap) { units++; }\n"
            "        else { units = units / 2; }\n    }\n"
            "    public int get() { return units; }\n}\n```\n\n"
            "Lời gọi: `new Meter(3)`, rồi `tick(); tick(); tick(); tick(); tick();`.\n"
            "Trả về giá trị **cuối** của `get()`.",
            [("final meter units", "Các tick: 1, 2, 3 (chạm trần), 3/2=1, 1+1=2.")],
        ),
        "apx-m2-altrace": vi_challenge(
            "Truy vết xóa khi đang duyệt (E3)",
            "Truy vết vòng lặp này **trên giấy**:\n\n```java\n"
            "ArrayList<String> list = new ArrayList<String>();\n"
            "list.add(\"a\"); list.add(\"b\"); list.add(\"c\");\n"
            "list.add(\"d\"); list.add(\"e\");\n"
            "for (int i = 0; i < list.size(); i++) {\n"
            "    if (i % 2 == 0) { list.remove(i); }\n}\n"
            "System.out.print(list);\n```\n\n"
            "Trả về nội dung được in chính xác (trong ngoặc, phân cách bởi "
            "dấu phẩy và dấu cách — như ArrayList in, ví dụ `[b, d]`).",
            [("list after shifting removals", "i=0 xóa a → [b,c,d,e]; i=1 lẻ, bỏ qua; i=2 xóa d (c trượt trái) → [b,c,e]; i=3 không nhỏ hơn kích thước 3, vòng lặp dừng.")],
        ),
        "apx-m2-static": vi_challenge(
            "Hai sổ cái: instance vs static (E3)",
            "Truy vết lớp và chuỗi lệnh này **trên giấy**:\n\n```java\n"
            "public class Ticket {\n    private static int issued = 0;\n"
            "    private int id;\n    public Ticket() { issued++; id = issued * 10; }\n"
            "    public int getId() { return id; }\n"
            "    public static int total() { return issued; }\n}\n```\n\n"
            "Chuỗi lệnh: `new Ticket()` ba lần; lần tạo **thứ tư** bị bỏ qua. "
            "Trả về `total() + lastTicket.getId()` với lastTicket là vé thứ ba.",
            [("static plus instance", "issued đếm cả ba lần tạo; id = 10 * thứ tự cho vé thứ ba.")],
        ),
        "apx-m2-passvalue": vi_challenge(
            "Ngữ nghĩa tham chiếu dưới đánh lạc hướng (E4)",
            "Truy vết chương trình này **trên giấy**:\n\n```java\n"
            "public static void adjust(int[] a, int[] b, int k) {\n"
            "    a[0] += k;          // biến đổi mảng dùng chung\n"
            "    b = new int[3];     // gán lại cục bộ\n"
            "    b[0] += k;          // mất\n"
            "    k = 99;             // mất\n}\n\n"
            "int[] x = {1, 2};\nint[] y = {3, 4};\nint k = 5;\n"
            "adjust(x, y, k);\nSystem.out.print(x[0] + \",\" + y[0] + \",\" + k);\n```\n\n"
            "Trả về văn bản được in chính xác.",
            [("output after call", "x[0] bị biến đổi qua tham chiếu (1+5); y chỉ được gán lại cục bộ; k là bản sao.")],
        ),
    },
    solutions=[
        ("apx-m2-looptrace", r"""public class Solution {
    public static String result() {
        return "123021";
    }
}
""", r"""public class Solution {
    // BUG: started j at 0 for every row (traced the wrong loop bounds)
    public static String result() {
        return "1002002301";
    }
}
"""),
        ("apx-m2-objtrace", r"""public class Solution {
    public static int result() {
        return 2;
    }
}
""", r"""public class Solution {
    // BUG: forgot the else-branch halving — traced 3 (capped forever)
    public static int result() {
        return 3;
    }
}
"""),
        ("apx-m2-altrace", r"""public class Solution {
    public static String result() {
        return "[b, c, e]";
    }
}
""", r"""public class Solution {
    // BUG: forgot that removals shift later indices left
    public static String result() {
        return "[a, c, e]";
    }
}
"""),
        ("apx-m2-static", r"""public class Solution {
    public static int result() {
        return 33;
    }
}
""", r"""public class Solution {
    // BUG: treated id as 1-based order, not order * 10
    public static int result() {
        return 4;
    }
}
"""),
        ("apx-m2-passvalue", r"""public class Solution {
    public static String result() {
        return "6,3,5";
    }
}
""", r"""public class Solution {
    // BUG: believed the local rebinding escaped the method
    public static String result() {
        return "6,5,99";
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m2", "Checkpoint: full trace under misdirection",
    "One program, many state changes: static, instance, and a dead variable.",
    20,
    r"""
Every trace in this module rewards the same discipline: one row per
event, read the code you see, keep instance and static ledgers apart,
and ignore variables the code never reads.
""",
    "Điểm kiểm tra: truy vết đầy đủ dưới đánh lạc hướng",
    "Một chương trình, nhiều thay đổi trạng thái: static, instance và biến chết.",
    r"""
Mọi bài truy vết trong module này thưởng cùng một kỷ luật: mỗi sự kiện
một dòng, đọc đúng mã bạn thấy, tách sổ instance và static, và bỏ qua
các biến mà mã không bao giờ đọc.
""",
    challenge(
        "apx-cp-m2-cache",
        "Checkpoint: the two-branch machine",
        "Trace this class and sequence, then return the **final** value of "
        "`probe()`:\n\n```java\npublic class Gate {\n"
        "    private static int visits = 0;\n    private int passes;\n"
        "    private int blocked;\n    public Gate() { passes = 0; blocked = 0; }\n"
        "    public void enter(boolean ok) {\n        visits++;\n"
        "        if (ok) { passes++; }\n        else {\n"
        "            blocked++;\n            if (blocked > 2) { passes = 0; }\n"
        "        }\n    }\n    public int probe() { return passes * 10 + blocked; }\n}\n```\n\n"
        "Calls: `new Gate()`, then `enter(true); enter(false); enter(false); "
        "enter(false); enter(true);`.",
        BOILER_VAL,
        [(
            "probe after sequence",
            r"""
CjTestBase.checkEq(Solution.result(), 13, "passes 1 * 10 + blocked 3");
""",
            "blocked reaches 3 on the third false → passes reset to 0; the final true makes passes 1. probe = 1*10 + 3.",
        )],
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Điểm kiểm tra: máy hai nhánh",
        "Truy vết lớp và chuỗi lời gọi này rồi trả về giá trị **cuối** của "
        "`probe()`:\n\n```java\npublic class Gate {\n"
        "    private static int visits = 0;\n    private int passes;\n"
        "    private int blocked;\n    public Gate() { passes = 0; blocked = 0; }\n"
        "    public void enter(boolean ok) {\n        visits++;\n"
        "        if (ok) { passes++; }\n        else {\n"
        "            blocked++;\n            if (blocked > 2) { passes = 0; }\n"
        "        }\n    }\n    public int probe() { return passes * 10 + blocked; }\n}\n```\n\n"
        "Lời gọi: `new Gate()`, rồi `enter(true); enter(false); enter(false); "
        "enter(false); enter(true);`.",
        [("probe after sequence", "blocked chạm 3 ở lần false thứ ba → passes bị reset 0; true cuối làm passes thành 1. probe = 1*10 + 3.")],
    ),
    solution=r"""public class Solution {
    public static int result() {
        return 13;
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: forgot the reset — traced passes as 2
    public static int result() {
        return 21;
    }
}
""",
)

print("M2 done")
