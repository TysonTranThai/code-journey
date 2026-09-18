#!/usr/bin/env python3
"""Java — Intermediate — Module 1: java-equality-immutability.

Opens the course by replacing "records just work" with a real understanding
of object contracts: identity vs equality, the equals/hashCode pairing rule,
defensive copying, and where mutability leaks through APIs. Every Java code
string is a raw triple-quoted string; tests are self-contained; CjTestBase
helpers take an explicit message argument (arity learned from the runtime).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-equality-immutability"

# ── lesson 1.1 — identity vs equality ────────────────────────────────────────
L_ID_EN = r"""
## Identity vs equality

`==` on objects asks: *is this the same object in memory?* (identity)
`.equals()` asks: *do these two objects represent the same value?* (equality)

```java
String a = new String("hi");
String b = new String("hi");
a == b        // false — two distinct objects
a.equals(b)   // true  — same value
```

The JVM caches small strings and small Integer boxes, so `==` can
*accidentally* return true for equal values — until it doesn't. Never use
`==` for value comparison on objects. Primitives (`int`, `long`, ...) are
the exception: `==` is correct there because there is no object identity.

```java
Integer x = 127, y = 127;
Integer p = 128, q = 128;
x == y   // true — cached box (do not rely on this!)
p == q   // false — new boxes above 127
```

This is the classic intermediate trap: code works in tests, breaks in
production with bigger numbers.
"""

L_ID_VI = r"""
## Đồng nhất so với bằng giá trị

`==` trên đối tượng hỏi: *đây có phải cùng một đối tượng trong bộ nhớ?*
(đồng nhất — identity). `.equals()` hỏi: *hai đối tượng này có cùng giá trị?*
(bằng giá trị — equality).

```java
String a = new String("hi");
String b = new String("hi");
a == b        // false — hai đối tượng khác nhau
a.equals(b)   // true  — cùng giá trị
```

JVM cache string nhỏ và Integer nhỏ, nên `==` có thể *vô tình* trả về true
với giá trị bằng nhau — cho đến khi không còn vậy. Không bao giờ dùng `==`
để so sánh giá trị của đối tượng. Primitive (`int`, `long`, ...) là ngoại lệ:
`==` đúng ở đó vì không có khái niệm identity.

```java
Integer x = 127, y = 127;
Integer p = 128, q = 128;
x == y   // true — box được cache (đừng dựa vào điều này!)
p == q   // false — box mới trên 127
```

Đây là bẫy kinh điển của trình độ trung cấp: code chạy trong test, hỏng ở
production với số lớn hơn.
"""

# ── lesson 1.2 — the equals/hashCode contract ───────────────────────────────
L_CONTRACT_EN = r"""
## The equals/hashCode contract

Write `equals()` and you **must** write `hashCode()`. The contract:

1. Equal objects must have equal hash codes.
2. Unequal objects *may* share a hash code (collision) — but shouldn't, or
   hash-based collections degrade toward lists.

Break the pairing and `HashSet`/`HashMap` silently misbehave. The loudest
failure is the **mutable key trap**: put a mutable object in a `HashSet`,
then mutate a field it hashes on — the object stays in its *old* bucket,
so `contains` returns false even though `equals` says it should be there:

```java
Set<Point> pts = new HashSet<>();   // mutable Point
pts.add(p);
p.x = 99;                           // hashCode changes under the set
pts.contains(p);                    // false! — searches the wrong bucket
```

That is why hash keys should be immutable.

Rules for hand-written `equals`:
- parameter is `Object`, then narrow with `instanceof`
- reflexive, symmetric, transitive, consistent, never `null == true`
- `@Override` so a typo like `equals(Point)` fails the build

`hashCode` should mix all fields used in `equals`:
`Objects.hash(x, y)` does it correctly and consistently.
"""

L_CONTRACT_VI = r"""
## Hợp đồng equals/hashCode

Viết `equals()` thì **bắt buộc** phải viết `hashCode()`. Hợp đồng:

1. Hai đối tượng bằng nhau phải có hash code bằng nhau.
2. Hai đối tượng khác nhau *có thể* cùng hash code (va chạm) — nhưng không
   nên, vì collection dựa trên hash sẽ suy giảm về phía danh sách.

Vi phạm cặp đôi này và `HashSet`/`HashMap` hành xử sai âm thầm. Cách hỏng
to rõ nhất là **bẫy key khả biến**: đưa một đối tượng khả biến vào
`HashSet`, rồi sửa field mà nó hash — đối tượng kẹt lại trong bucket *cũ*,
nên `contains` trả false dù `equals` nói nó phải ở đó:

```java
Set<Point> pts = new HashSet<>();   // Point khả biến
pts.add(p);
p.x = 99;                           // hashCode đổi dưới chân set
pts.contains(p);                    // false! — tìm nhầm bucket
```

Vì vậy key dùng cho hash nên bất biến.

Quy tắc viết tay `equals`:
- tham số là `Object`, rồi thu hẹp bằng `instanceof`
- phản xạ, đối xứng, bắc cầu, ổn định, không bao giờ trả true với `null`
- luôn có `@Override` để lỗi chính tả như `equals(Point)` vỡ ngay lúc build

`hashCode` nên trộn tất cả field có trong `equals`:
`Objects.hash(x, y)` làm đúng và nhất quán.
"""

# ── lesson 1.3 — immutability & defensive copying ───────────────────────────
L_IMMUT_EN = r"""
## Immutability and defensive copying

An immutable class: `final` fields, no setters, no leaked mutable state.
Immutable objects are thread-safe by construction, safe map keys, and easy
to reason about.

```java
public final class Range {
    private final int lo, hi;
    public Range(int lo, int hi) {
        if (lo > hi) throw new IllegalArgumentException("lo > hi");
        this.lo = lo; this.hi = hi;
    }
    public int lo() { return lo; }
    public int hi() { return hi; }
}
```

Mutability leaks in two directions:

**1. Mutable field leaked** — the caller can change your state without going
through your methods:

```java
public final class Team {
    private final List<String> members;
    Team(List<String> members) { this.members = members; }
    public List<String> members() { return members; }  // LEAK
}
// caller: team.members().clear();  — your "final" field is now empty
```

Fix: return an unmodifiable view (or a copy) and copy on the way in:

```java
Team(List<String> members) { this.members = List.copyOf(members); }
public List<String> members() { return Collections.unmodifiableList(members); }
```

**2. Mutable field stored** — you keep a reference to the caller's list;
they mutate it later and your object changes underneath you.

`record` solves the field-leak but still shallow-copies arrays and lists —
a record holding a mutable `List` is only as immutable as that list allows.
"""

L_IMMUT_VI = r"""
## Tính bất biến và bản sao phòng thủ

Class bất biến: field `final`, không setter, không rò rỉ trạng thái khả biến.
Đối tượng bất biến an toàn luồng ngay từ thiết kế, làm key của map an toàn,
và dễ suy luận.

```java
public final class Range {
    private final int lo, hi;
    public Range(int lo, int hi) {
        if (lo > hi) throw new IllegalArgumentException("lo > hi");
        this.lo = lo; this.hi = hi;
    }
    public int lo() { return lo; }
    public int hi() { return hi; }
}
```

Tính khả biến rò rỉ theo hai hướng:

**1. Field khả biến bị lộ ra ngoài** — caller thay đổi trạng thái của bạn
mà không đi qua method nào:

```java
public final class Team {
    private final List<String> members;
    Team(List<String> members) { this.members = members; }
    public List<String> members() { return members; }  // RÒ RỈ
}
// caller: team.members().clear();  — field "final" giờ rỗng toạch
```

Cách sửa: trả về view không thể sửa (hoặc bản sao), và sao chép khi nhận vào:

```java
Team(List<String> members) { this.members = List.copyOf(members); }
public List<String> members() { return Collections.unmodifiableList(members); }
```

**2. Field giữ tham chiếu của caller** — bạn giữ list của caller; họ sửa sau
đó và đối tượng của bạn đổi dưới chân họ.

`record` xử lý việc lộ field nhưng vẫn chỉ sao chép nông với mảng và list —
record chứa `List` khả biến chỉ bất biến bằng đúng mức list đó cho phép.
"""

write_module(
    MOD,
    "Equality, Immutability & Object Contracts",
    "The contracts every Java type must keep: identity vs equality, the equals/hashCode pairing, and defensive copying.",
    "Bằng giá trị, tính bất biến & hợp đồng đối tượng",
    "Các hợp đồng mà mọi kiểu Java phải giữ: identity so với equality, cặp equals/hashCode, và bản sao phòng thủ.",
    ["identity-vs-equality", "equals-hashcode-contract", "immutability-defensive-copies", "javi-checkpoint-contracts"],
    ["javi-p1-contracts"],
)

write_lesson(MOD, "identity-vs-equality", "Identity vs Equality", "Why == and .equals() answer different questions, and how Integer caching and string interning hide the bug until it ships.", 12, L_ID_EN, "Identity so với Equality", "Vì sao == và .equals() trả lời hai câu hỏi khác nhau, và cách cache Integer cùng string interning che giấu lỗi đến tận production.", L_ID_VI)

write_lesson(MOD, "equals-hashcode-contract", "The equals/hashCode Contract", "The pairing rule that keeps HashSet and HashMap correct, and the mutable-key trap that makes contains lie.", 14, L_CONTRACT_EN, "Hợp đồng equals/hashCode", "Quy tắc cặp đôi giữ cho HashSet và HashMap đúng, và bẫy key khả biến khiến contains nói dối.", L_CONTRACT_VI)

write_lesson(MOD, "immutability-defensive-copies", "Immutability & Defensive Copies", "Building truly immutable classes, and the two directions mutability leaks through final fields and return values.", 14, L_IMMUT_EN, "Tính bất biến & bản sao phòng thủ", "Xây class bất biến đúng nghĩa, và hai hướng mà tính khả biến rò rỉ qua field final và giá trị trả về.", L_IMMUT_VI)

# ── practice set ─────────────────────────────────────────────────────────────
P1_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement methods below.
}
"""

CH_P1_EQ = challenge(
    "javi-p1-color-equals",
    "Write the equals/hashCode Pair",
    r"""Implement a `Color` value class inside `Solution`:
- public constructor `Color(int r, int g, int b)` storing fields as final
- `equals(Object)` returning true only for another `Color` with identical r, g, b
- `hashCode()` consistent with equals (use `Objects.hash(...)`)
- `toString()` returning `Color[r=...,g=...,b=...]`

The tests put two equal Colors into a HashSet and expect the set to treat
them as one element — the classic contract check.""",
    P1_BOILER,
    [
        (
            "equal colors deduplicate in a HashSet",
            r"""
Solution.Color a = new Solution.Color(10, 20, 30);
Solution.Color b = new Solution.Color(10, 20, 30);
Set<Solution.Color> set = new HashSet<>();
set.add(a); set.add(b);
checkEq(set.size(), 1, "two equal colors must be one element");
""",
            "Two equal objects must occupy one set slot — that requires equals AND hashCode together.",
        ),
        (
            "different colors stay distinct",
            r"""
Solution.Color a = new Solution.Color(1, 2, 3);
Solution.Color b = new Solution.Color(1, 2, 4);
checkTrue(!a.equals(b), "different channels differ");
Set<Solution.Color> set = new HashSet<>();
set.add(a); set.add(b);
checkEq(set.size(), 2, "distinct colors stay two elements");
""",
            "Changing one channel must change both equality and the hash bucket.",
        ),
        (
            "toString format",
            r"""
checkEq(new Solution.Color(255, 0, 128).toString(), "Color[r=255,g=0,b=128]", "format");
""",
            "Format exactly: Color[r=255,g=0,b=128]",
        ),
    ],
    level="independent",
)

CH_P1_W = challenge(
    "javi-p1-spot-leak",
    "Find the Leaked Mutability",
    r"""`Badge` stores an internal `List<String> log` of scan events.
The current implementation returns the internal list directly. A caller can
`clear()` your history without your class knowing.

Fix `Badge` so that:
- the internal list can never be modified from outside
- scans still accumulate internally via `scan(String event)`
- `history()` returns a read-only view

Keep the constructor defensive too: copy the incoming list.""",
    P1_BOILER,
    [
        (
            "history is unmodifiable",
            r"""
Solution.Badge b = new Solution.Badge(List.of("start"));
b.scan("door-1");
List<String> h = b.history();
try { h.add("hack"); checkTrue(false, "add must throw"); }
catch (UnsupportedOperationException e) { checkTrue(true, "threw correctly"); }
""",
            "history() must return Collections.unmodifiableList(...) — an add() must throw.",
        ),
        (
            "constructor copies input",
            r"""
List<String> src = new ArrayList<>(List.of("a"));
Solution.Badge b = new Solution.Badge(src);
src.clear();
checkEq(b.history(), List.of("a"), "badge survives caller mutation");
""",
            "Copy the incoming list (List.copyOf) so later caller mutation cannot reach the badge.",
        ),
        (
            "scans accumulate internally",
            r"""
Solution.Badge b = new Solution.Badge(List.of());
b.scan("x"); b.scan("y");
checkEq(b.history(), List.of("x", "y"), "scans accumulate");
""",
            "scan() appends to the internal (mutable) list; history() only wraps it read-only.",
        ),
    ],
    level="debugging",
)

CH_P1_CACHED = challenge(
    "javi-p1-box-cache",
    "Predict the Box Comparison",
    r"""Without running code first, predict each result, then implement
`Solution.answers()` returning them as a `boolean[]`:

1. `Integer a = 1000, b = 1000; a == b` — ?
2. `Integer c = 100, d = 100; c == d` — ?
3. `Integer e = 1000, f = 1000; e.equals(f)` — ?
4. `int g = 1000; Integer h = 1000; g == h` — ? (unboxing comparison)

Index 0..3 in the returned array. Then read the explanation the tests give
you and reconcile it with your intuition.""",
    P1_BOILER,
    [
        (
            "four predictions in order",
            r"""
boolean[] ans = Solution.answers();
checkEq(ans.length, 4, "four answers");
checkEq(ans[0], false, "1000 > 127 → distinct boxes");
checkEq(ans[1], true, "100 ≤ 127 → shared cache box (accident!)");
checkEq(ans[2], true, "equals compares values");
checkEq(ans[3], true, "h unboxes to int, primitive ==");
""",
            "The Integer cache covers -128..127 only; above that each box is a new object. Unboxing comparisons use primitive ==.",
        ),
    ],
    level="independent",
)

VI_CH_P1_EQ = vi_challenge(
    "Viết cặp equals/hashCode",
    r"""Cài đặt class giá trị `Color` bên trong `Solution`:
- constructor public `Color(int r, int g, int b)` lưu field final
- `equals(Object)` chỉ trả true với `Color` khác có đúng r, g, b
- `hashCode()` nhất quán với equals (dùng `Objects.hash(...)`)
- `toString()` trả về `Color[r=...,g=...,b=...]`

Test đưa hai Color bằng nhau vào HashSet và mong set coi chúng là một phần
tử — phép kiểm tra hợp đồng kinh điển.""",
    [
        ("Hai màu bằng nhau bị gộp trong HashSet", "Hai đối tượng bằng nhau phải chiếm một ô set — cần equals VÀ hashCode cùng lúc."),
        ("Màu khác nhau vẫn phân biệt", "Đổi một kênh phải đổi cả equality lẫn hash bucket."),
        ("Định dạng toString", "Format chính xác: Color[r=255,g=0,b=128]"),
    ],
)

VI_CH_P1_W = vi_challenge(
    "Tìm chỗ rò rỉ tính khả biến",
    r"""`Badge` lưu một `List<String> log` nội bộ của các sự kiện quét.
Bản hiện tại trả trực tiếp list nội bộ. Caller có thể `clear()` lịch sử của
bạn mà class không hề hay biết.

Sửa `Badge` để:
- list nội bộ không thể bị sửa từ bên ngoài
- quét vẫn tích lũy qua `scan(String event)`
- `history()` trả về view chỉ đọc

Constructor cũng phải phòng thủ: sao chép list nhận vào.""",
    [
        ("history không thể sửa", "history() phải trả Collections.unmodifiableList(...) — một add() phải ném ngoại lệ."),
        ("constructor sao chép đầu vào", "Sao chép list nhận vào (List.copyOf) để caller sửa sau không ảnh hưởng badge."),
        ("quét vẫn tích lũy", "scan() nối vào list nội bộ (khả biến); history() chỉ bọc lại ở chế độ chỉ đọc."),
    ],
)

VI_CH_P1_CACHED = vi_challenge(
    "Dự đoán so sánh box",
    r"""Không chạy code trước, dự đoán từng kết quả, rồi cài
`Solution.answers()` trả chúng về dưới dạng `boolean[]`:

1. `Integer a = 1000, b = 1000; a == b` — ?
2. `Integer c = 100, d = 100; c == d` — ?
3. `Integer e = 1000, f = 1000; e.equals(f)` — ?
4. `int g = 1000; Integer h = 1000; g == h` — ? (so sánh sau unbox)

Index 0..3 trong mảng trả về. Sau đó đọc giải thích của test và đối chiếu
với trực giác của bạn.""",
    [
        ("Bốn dự đoán đúng thứ tự", "Cache Integer chỉ phủ -128..127; trên ngưỡng đó mỗi box là đối tượng mới. So sánh sau unbox dùng primitive ==."),
    ],
)

write_practice(
    MOD,
    "javi-p1-contracts",
    "Contract Lab",
    "Build value classes with correct equals/hashCode, seal leaky APIs, and defeat the Integer-cache trap.",
    "Xưởng hợp đồng",
    "Xây class giá trị với equals/hashCode đúng, bịt API rò rỉ, và vượt bẫy cache Integer.",
    "immutability-defensive-copies",
    35,
    "intermediate",
    [CH_P1_EQ, CH_P1_W, CH_P1_CACHED],
    {CH_P1_EQ["id"]: VI_CH_P1_EQ, CH_P1_W["id"]: VI_CH_P1_W, CH_P1_CACHED["id"]: VI_CH_P1_CACHED},
    solutions=[
        (
            CH_P1_EQ["id"],
            r"""
import java.util.*;

public class Solution {
    public static class Color {
        private final int r, g, b;
        public Color(int r, int g, int b) { this.r = r; this.g = g; this.b = b; }
        @Override public boolean equals(Object o) {
            return o instanceof Color c && c.r == r && c.g == g && c.b == b;
        }
        @Override public int hashCode() { return Objects.hash(r, g, b); }
        @Override public String toString() { return "Color[r=" + r + ",g=" + g + ",b=" + b + "]"; }
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static class Color {
        private final int r, g, b;
        public Color(int r, int g, int b) { this.r = r; this.g = g; this.b = b; }
        // equals compares ONLY r — green(1,2,3) equals blue(1,9,9).
        // This is the classic partial-equality bug: hashCode mirrors the
        // same subset, so the pair stays "consistent" while value equality
        // is simply wrong.
        @Override public boolean equals(Object o) {
            return o instanceof Color c && c.r == r;
        }
        @Override public int hashCode() { return Integer.hashCode(r); }
        @Override public String toString() { return "Color[r=" + r + ",g=" + g + ",b=" + b + "]"; }
    }
}
""",
        ),
        (
            CH_P1_W["id"],
            r"""
import java.util.*;

public class Solution {
    public static class Badge {
        private final List<String> log;
        public Badge(List<String> initial) { this.log = new ArrayList<>(List.copyOf(initial)); }
        public void scan(String event) { log.add(event); }
        public List<String> history() { return Collections.unmodifiableList(log); }
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static class Badge {
        private final List<String> log;
        public Badge(List<String> initial) { this.log = initial; }  // stored caller's list!
        public void scan(String event) { log.add(event); }
        public List<String> history() { return Collections.unmodifiableList(log); }
    }
}
""",
        ),
        (
            CH_P1_CACHED["id"],
            r"""
public class Solution {
    public static boolean[] answers() { return new boolean[]{false, true, true, true}; }
}
""",
            r"""
public class Solution {
    public static boolean[] answers() { return new boolean[]{true, true, false, false}; }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — object contracts

You can now: distinguish identity from equality, pair equals with hashCode,
and build immutable classes that do not leak mutability. Prove it by fixing
a class whose hash contract and API boundaries are both broken.
"""

CP_MDX_VI = r"""
## Checkpoint — hợp đồng đối tượng

Giờ bạn có thể: phân biệt identity với equality, ghép cặp equals với
hashCode, và xây class bất biến không rò rỉ tính khả biến. Chứng minh bằng
cách sửa một class mà cả hợp đồng hash lẫn ranh giới API đều hỏng.
"""

CH_CP1 = challenge(
    "javi-checkpoint-m1-contracts",
    "Repair the Broken Value Class",
    r"""`Config` is meant to be an immutable settings key, but it is broken:
`hashCode` uses only one field and the constructor accepts nulls.

Inside `Solution`, provide a fixed `Config`:
- final fields `String app, String key` (both participate in equality)
- equals via instanceof pattern comparing both fields
- hashCode via `Objects.hash(app, key)`
- constructor throws `IllegalArgumentException` when app or key is null

Then implement `static List<String> sortedKeys(List<Config> configs)`
returning the distinct configs' `key` values in natural sorted order,
using a `HashSet` for dedup (which only works because Config now keeps
its hash contract).""",
    r"""
import java.util.*;

public class Solution {
    // Provide Config + sortedKeys here.
}
""",
    [
        (
            "distinct apps, same key: both kept",
            r"""
Set<Object> seen = new HashSet<>(List.of(
    new Solution.Config("web", "timeout"), new Solution.Config("db", "timeout")));
checkEq(seen.size(), 2, "org/app must be hashed");
""",
            "hashCode must mix app in — two apps' keys are distinct entries.",
        ),
        (
            "identical configs deduplicate",
            r"""
Set<Object> seen = new HashSet<>(List.of(
    new Solution.Config("web", "timeout"), new Solution.Config("web", "timeout")));
checkEq(seen.size(), 1, "equal configs dedupe");
""",
            "equals true + hashCode equal ⇒ one set element.",
        ),
        (
            "null fields rejected",
            r"""
try { new Solution.Config(null, "a"); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "threw correctly"); }
""",
            "Fail fast in the constructor: null app or key must throw IllegalArgumentException.",
        ),
        (
            "sortedKeys dedupes and sorts",
            r"""
List<Object> cfgs = List.of(
    new Solution.Config("web", "timeout"), new Solution.Config("db", "host"),
    new Solution.Config("web", "timeout"));
List<String> out = Solution.sortedKeys((List) cfgs);
checkEq(out, List.of("host", "timeout"), "distinct + sorted");
""",
            "Feed the list through a HashSet, map to key, sort.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CH_CP1 = vi_challenge(
    "Sửa lại class giá trị hỏng",
    r"""`Config` đáng lẽ là một settings key bất biến, nhưng nó hỏng:
`hashCode` chỉ dùng một field và constructor chấp nhận null.

Bên trong `Solution`, cung cấp `Config` đã sửa:
- field final `String app, String key` (cả hai tham gia equality)
- equals qua instanceof pattern so sánh cả hai field
- hashCode qua `Objects.hash(app, key)`
- constructor ném `IllegalArgumentException` khi app hoặc key là null

Sau đó cài `static List<String> sortedKeys(List<Config> configs)` trả về
các giá trị `key` phân biệt theo thứ tự tự nhiên, dùng `HashSet` để khử
trùng lặp (chỉ hoạt động vì Config giờ giữ đúng hợp đồng hash).""",
    [
        ("App khác nhau, cùng key: giữ cả hai", "hashCode phải trộn app vào — key của hai app là hai phần tử phân biệt."),
        ("Config giống nhau bị khử trùng lặp", "equals true + hashCode bằng nhau ⇒ một phần tử set."),
        ("Chặn field null", "Fail fast trong constructor: app hoặc key null phải ném IllegalArgumentException."),
        ("sortedKeys khử trùng lặp và sắp xếp", "Đưa list qua HashSet, map sang key, rồi sort."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-contracts",
    "Checkpoint: Object Contracts",
    "Graded checkpoint: repair a broken value class and count distinct settings correctly.",
    15,
    CP_MDX,
    "Checkpoint: Hợp đồng đối tượng",
    "Checkpoint chấm điểm: sửa class giá trị hỏng và đếm cấu hình phân biệt đúng.",
    CP_MDX_VI,
    CH_CP1,
    VI_CH_CP1,
    solution=r"""
import java.util.*;

public class Solution {
    public static class Config {
        private final String app, key;
        public Config(String app, String key) {
            if (app == null || key == null) throw new IllegalArgumentException("app/key required");
            this.app = app; this.key = key;
        }
        public String key() { return key; }
        @Override public boolean equals(Object o) {
            return o instanceof Config c && c.app.equals(app) && c.key.equals(key);
        }
        @Override public int hashCode() { return Objects.hash(app, key); }
    }

    public static List<String> sortedKeys(List<Config> configs) {
        Set<String> distinct = new HashSet<>();
        for (Config c : configs) distinct.add(c.key());
        List<String> out = new ArrayList<>(distinct);
        Collections.sort(out);
        return out;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public static class Config {
        private final String app, key;
        public Config(String app, String key) {
            this.app = app; this.key = key;  // no null check
        }
        public String key() { return key; }
        @Override public boolean equals(Object o) {
            return o instanceof Config c && c.app.equals(app) && c.key.equals(key);
        }
        @Override public int hashCode() { return key.hashCode(); }  // app ignored
    }

    public static List<String> sortedKeys(List<Config> configs) {
        Set<String> distinct = new HashSet<>();
        for (Config c : configs) distinct.add(c.key());
        List<String> out = new ArrayList<>(distinct);
        Collections.sort(out);
        return out;
    }
}
""",
)
