#!/usr/bin/env python3
"""Java — Intermediate — Module 3: java-generics-deep.

Bounds, wildcards, PECS, and the erasure mental model. House conventions:
Solution-qualified test refs, explicit CjTestBase messages, Ws are
behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-generics-deep"

# ── lesson 3.1 — bounded type parameters ────────────────────────────────────
L_BOUNDS_EN = r"""
## Bounded type parameters

A bare `<T>` promises almost nothing. A bound makes the promise concrete:

```java
// T can be any Number subtype — so .doubleValue() is legal on it
static double average(List<? extends Number> xs) { ... }

// <T extends Comparable<T>> lets you call compareTo on values of type T
static <T extends Comparable<T>> T max(List<T> xs) {
    T best = xs.get(0);
    for (T x : xs) if (x.compareTo(best) > 0) best = x;
    return best;
}
```

Two bound forms:
- **Type-parameter bound** `<T extends Comparable<T>>` — used when T must
  flow *through* the method (in and out).
- **Wildcard bound** `List<? extends Number>` — used when T only flows
  *out* of the list (you read it, never write).

Multiple bounds: `<T extends Number & Comparable<T>>` — class first,
interfaces after.
"""

L_BOUNDS_VI = r"""
## Bounded type parameter

`<T>` trần trụi hầu như không hứa gì. Bound biến lời hứa thành cụ thể:

```java
// T là subtype bất kỳ của Number — nên .doubleValue() hợp lệ trên nó
static double average(List<? extends Number> xs) { ... }

// <T extends Comparable<T>> cho phép gọi compareTo trên giá trị kiểu T
static <T extends Comparable<T>> T max(List<T> xs) {
    T best = xs.get(0);
    for (T x : xs) if (x.compareTo(best) > 0) best = x;
    return best;
}
```

Hai dạng bound:
- **Bound trên type parameter** `<T extends Comparable<T>>` — dùng khi T
  phải chảy *qua* method (vào và ra).
- **Wildcard bound** `List<? extends Number>` — dùng khi T chỉ chảy *ra*
  khỏi list (đọc, không ghi).

Nhiều bound: `<T extends Number & Comparable<T>>` — class trước, interface
sau.
"""

# ── lesson 3.2 — wildcards & PECS ───────────────────────────────────────────
L_PECS_EN = r"""
## Wildcards and PECS

`Integer` is a `Number`, but `List<Integer>` is NOT a `List<Number>` —
generics are invariant. Wildcards restore flexibility safely:

```java
static double sum(List<? extends Number> src) {   // producer: read out
    double t = 0;
    for (Number n : src) t += n.doubleValue();
    return t;
}

static void fill(List<? super Integer> dst) {     // consumer: write in
    dst.add(1); dst.add(2); dst.add(3);
}
```

**PECS** (from Effective Java): *Producer Extends, Consumer Super.*
- If the parameter **produces** values for you → `? extends T`
- If the parameter **consumes** values from you → `? super T`
- Both (e.g. copy) → use both wildcards.

Why `? extends` forbids writes: the compiler only knows "some unknown
subtype of Number" — any specific element you add might be the wrong one.
Reads are always safe; writes are not, so they are banned.
"""

L_PECS_VI = r"""
## Wildcard và PECS

`Integer` là `Number`, nhưng `List<Integer>` KHÔNG phải `List<Number>` —
generic bất biến. Wildcard khôi phục sự linh hoạt một cách an toàn:

```java
static double sum(List<? extends Number> src) {   // producer: đọc ra
    double t = 0;
    for (Number n : src) t += n.doubleValue();
    return t;
}

static void fill(List<? super Integer> dst) {     // consumer: ghi vào
    dst.add(1); dst.add(2); dst.add(3);
}
```

**PECS** (từ Effective Java): *Producer Extends, Consumer Super.*
- Nếu tham số **sản xuất** giá trị cho bạn → `? extends T`
- Nếu tham số **tiêu thụ** giá trị từ bạn → `? super T`
- Cả hai (ví dụ copy) → dùng cả hai wildcard.

Vì sao `? extends` cấm ghi: compiler chỉ biết "một subtype không xác định
của Number" — bất kỳ phần tử nào bạn thêm vào có thể là sai kiểu. Đọc luôn
an toàn; ghi thì không, nên bị cấm.
"""

# ── lesson 3.3 — erasure ────────────────────────────────────────────────────
L_ERASURE_EN = r"""
## Type erasure — what generics really are

Generics exist at compile time only. `List<String>` and `List<Integer>`
are the same class at runtime — both erase to `List`. Consequences:

```java
List<String> a = new ArrayList<>();
List<Integer> b = new ArrayList<>();
a.getClass() == b.getClass()   // true!

// can't do these:
// new T[10]                       — no T at runtime
// if (x instanceof List<String>)  — erased
// catch (MyEx<String> e)          — generics in catch are banned
```

Practical rules:
- Arrays of generic type are unsafe (`new T[10]` won't compile; use
  `ArrayList<T>`)
- You cannot overload on erased parameters:
  `f(List<String>)` + `f(List<Integer>)` — same erasure, compile error
- Need runtime type info? Pass a `Class<T>` token: `<T> T parse(String s, Class<T> type)`

Erasure explains *why* wildcards exist: flexibility must be expressible in
the type system without runtime cost.
"""

L_ERASURE_VI = r"""
## Type erasure — generic thực chất là gì

Generic chỉ tồn tại lúc biên dịch. `List<String>` và `List<Integer>` là
cùng một class lúc runtime — cả hai erase thành `List`. Hệ quả:

```java
List<String> a = new ArrayList<>();
List<Integer> b = new ArrayList<>();
a.getClass() == b.getClass()   // true!

// không làm được những điều này:
// new T[10]                       — không có T lúc runtime
// if (x instanceof List<String>)  — đã bị erase
// catch (MyEx<String> e)          — generic trong catch bị cấm
```

Quy tắc thực dụng:
- Mảng của kiểu generic không an toàn (`new T[10]` không biên dịch; dùng
  `ArrayList<T>`)
- Không thể overload trên tham số bị erase:
  `f(List<String>)` + `f(List<Integer>)` — cùng erasure, lỗi biên dịch
- Cần thông tin kiểu lúc runtime? Truyền token `Class<T>`: `<T> T parse(String s, Class<T> type)`

Erasure giải thích *vì sao* wildcard tồn tại: sự linh hoạt phải diễn đạt
được trong hệ thống kiểu mà không tốn chi phí runtime.
"""

write_module(
    MOD,
    "Generics Deep Dive",
    "Bounded type parameters, wildcards with PECS, and the erasure mental model that explains every generic restriction.",
    "Generic chuyên sâu",
    "Bounded type parameter, wildcard với PECS, và mô hình erasure giải thích mọi hạn chế của generic.",
    ["generic-bounds", "wildcards-pecs", "type-erasure", "javi-checkpoint-generics"],
    ["javi-p3-generics"],
)

write_lesson(MOD, "generic-bounds", "Bounded Type Parameters", "Making promises concrete with extends bounds: through-flowing T vs read-only wildcards, and multi-bound syntax.", 14, L_BOUNDS_EN, "Bounded type parameter", "Biến lời hứa thành cụ thể với bound extends: T chảy qua so với wildcard chỉ đọc, và cú pháp nhiều bound.", L_BOUNDS_VI)

write_lesson(MOD, "wildcards-pecs", "Wildcards & PECS", "Producer Extends, Consumer Super: restoring flexibility to invariant generics and why extends-wildcards ban writes.", 15, L_PECS_EN, "Wildcard & PECS", "Producer Extends, Consumer Super: khôi phục linh hoạt cho generic bất biến và vì sao wildcard extends cấm ghi.", L_PECS_VI)

write_lesson(MOD, "type-erasure", "Type Erasure", "Why List<String> and List<Integer> are one class at runtime, and the compile rules erasure forces on arrays, overloads, and instanceof.", 13, L_ERASURE_EN, "Type Erasure", "Vì sao List<String> và List<Integer> là một class lúc runtime, và những quy tắc biên dịch mà erasure áp đặt lên mảng, overload, và instanceof.", L_ERASURE_VI)

# ── practice set ─────────────────────────────────────────────────────────────
P3_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement methods below.
}
"""

CH_P3_STATS = challenge(
    "javi-p3-pecs-stats",
    "PECS: Sum Into and Out Of Lists",
    r"""Implement two methods that demonstrate PECS signatures:
- `static double sum(List<? extends Number> src)` — producer side,
  returns the total as double.
- `static void fill(List<? super Integer> dst, int a, int b, int c)` —
  consumer side, appends a, b, c in order.

Then `static List<Number> demo()` returns a `List<Number>` produced by
calling `fill` on it and then `sum` over it — proving one method reads a
List<Number> and the other writes into it, exactly as the wildcards
promise.""",
    P3_BOILER,
    [
        (
            "sum reads any Number list",
            r"""
checkNear(Solution.sum(List.of(1, 2.5, 3L)), 6.5, 1e-9, "sum of mixed numbers");
""",
            "List.of(1, 2.5, 3L) is List<? extends Number> — sum must accept it.",
        ),
        (
            "fill writes into a supertype list",
            r"""
List<Object> dst = new ArrayList<>();
Solution.fill(dst, 4, 5, 6);
checkEq(dst, List.of(4, 5, 6), "fill appended in order");
""",
            "List<Object> is List<? super Integer> — fill must accept and append a, b, c.",
        ),
        (
            "demo exercises both sides",
            r"""
List<Number> out = Solution.demo();
checkEq(out, List.of(7, 8, 9), "demo filled 7,8,9");
checkNear(Solution.sum(out), 24.0, 1e-9, "demo sums");
""",
            "demo() should fill(7,8,9) into its own list then return it.",
        ),
    ],
    level="guided",
)

CH_P3_MAX = challenge(
    "javi-p3-generic-max",
    "Generic max() with a Bound",
    r"""Implement `static <T extends Comparable<T>> T max(List<T> xs)` —
returns the largest element per natural ordering. Empty or null list
throws IllegalArgumentException. Then two call sites:
- `static Integer maxInt(List<Integer> xs)` delegating to max
- `static String maxString(List<String> xs)` delegating to max

This is the bound doing real work: compareTo would not compile without
`T extends Comparable<T>`.""",
    P3_BOILER,
    [
        (
            "max of integers",
            r"""
checkEq(Solution.maxInt(List.of(3, 9, 4)), 9, "max int");
""",
            "Natural ordering through the Comparable bound.",
        ),
        (
            "max of strings",
            r"""
checkEq(Solution.maxString(List.of("pear", "apple", "plum")), "plum", "max string");
""",
            "String is Comparable<String> — the bound admits it.",
        ),
        (
            "empty input fails fast",
            r"""
try { Solution.maxInt(List.of()); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "threw"); }
""",
            "Empty (or null) list throws IllegalArgumentException.",
        ),
    ],
    level="independent",
)

CH_P3_ERASURE = challenge(
    "javi-p3-erasure-token",
    "Erasure Workaround: the Class Token",
    r"""Because generics erase, a method that must *create* an instance of T
needs runtime type information. Implement:
- `static <T> List<T> fill(int n, Class<T> type, Function<Object, T> maker)`:
  builds a List with n elements, each produced by maker, typed by the
  token (use `java.util.function.Function`).
- `static <T> List<T> nCopiesOf(int n, T value)` — erasure-friendly
  copying that needs no token at all.

The tests show which operations survive erasure and which need help.""",
    P3_BOILER,
    [
        (
            "token-typed creation",
            r"""
List<String> out = Solution.fill(3, String.class, s -> "v" + 1);
checkEq(out, List.of("v1", "v1", "v1"), "token fill");
""",
            "maker receives a placeholder; produce three equal values.",
        ),
        (
            "nCopiesOf needs no token",
            r"""
List<Integer> out = Solution.nCopiesOf(2, 42);
checkEq(out, List.of(42, 42), "n copies");
""",
            "Value-based copying erases cleanly.",
        ),
        (
            "runtime classes agree",
            r"""
List<String> a = Solution.nCopiesOf(1, "x");
List<Integer> b = Solution.nCopiesOf(1, 1);
checkEq(a.getClass() == b.getClass(), true, "same erased class");
""",
            "Erasure: both lists share one runtime class.",
        ),
    ],
    level="independent",
)

VI_CH_P3_STATS = vi_challenge(
    "PECS: đọc vào và ghi ra list",
    r"""Cài hai method thể hiện chữ ký PECS:
- `static double sum(List<? extends Number> src)` — phía producer, trả
  tổng dưới dạng double.
- `static void fill(List<? super Integer> dst, int a, int b, int c)` —
  phía consumer, nối a, b, c theo thứ tự.

Rồi `static List<Number> demo()` trả về một `List<Number>` được tạo bằng
cách gọi `fill` lên nó rồi `sum` trên nó — chứng minh một method đọc
List<Number> và method kia ghi vào nó, đúng như wildcard hứa.""",
    [
        ("sum đọc mọi list Number", "List.of(1, 2.5, 3L) là List<? extends Number> — sum phải nhận được nó."),
        ("fill ghi vào list supertype", "List<Object> là List<? super Integer> — fill phải nhận được và nối a, b, c."),
        ("demo tập cả hai phía", "demo() nên fill(7,8,9) vào list riêng rồi trả nó về."),
    ],
)

VI_CH_P3_MAX = vi_challenge(
    "Generic max() với bound",
    r"""Cài `static <T extends Comparable<T>> T max(List<T> xs)` — trả phần tử
lớn nhất theo thứ tự tự nhiên. List rỗng hoặc null ném
IllegalArgumentException. Rồi hai điểm gọi:
- `static Integer maxInt(List<Integer> xs)` ủy quyền cho max
- `static String maxString(List<String> xs)` ủy quyền cho max

Bound làm việc thật ở đây: compareTo sẽ không biên dịch nếu thiếu
`T extends Comparable<T>`.""",
    [
        ("max của số nguyên", "Thứ tự tự nhiên qua bound Comparable."),
        ("max của chuỗi", "String là Comparable<String> — bound chấp nhận nó."),
        ("Input rỗng fail fast", "List rỗng (hoặc null) ném IllegalArgumentException."),
    ],
)

VI_CH_P3_ERASURE = vi_challenge(
    "Giải pháp erasure: Class token",
    r"""Vì generic bị erase, method phải *tạo* instance của T cần thông tin
kiểu lúc runtime. Cài:
- `static <T> List<T> fill(int n, Class<T> type, Function<Object, T> maker)`:
  dựng List n phần tử, mỗi phần tử do maker tạo, được định kiểu bởi token
  (dùng `java.util.function.Function`).
- `static <T> List<T> nCopiesOf(int n, T value)` — sao chép thân thiện
  erasure, không cần token.

Test cho thấy thao tác nào sống sót qua erasure và thao tác nào cần giúp.""",
    [
        ("Tạo kiểu bởi token", "maker nhận placeholder; tạo ba giá trị bằng nhau."),
        ("nCopiesOf không cần token", "Sao chép theo giá trị erase sạch sẽ."),
        ("Class runtime trùng nhau", "Erasure: hai list dùng chung một class runtime."),
    ],
)

write_practice(
    MOD,
    "javi-p3-generics",
    "Generics Lab",
    "PECS signatures in action, a Comparable-bounded max, and the Class-token erasure workaround.",
    "Xưởng generic",
    "Chữ ký PECS trong thực chiến, max có bound Comparable, và mẹo Class token chống erasure.",
    "type-erasure",
    40,
    "intermediate",
    [CH_P3_STATS, CH_P3_MAX, CH_P3_ERASURE],
    {CH_P3_STATS["id"]: VI_CH_P3_STATS, CH_P3_MAX["id"]: VI_CH_P3_MAX, CH_P3_ERASURE["id"]: VI_CH_P3_ERASURE},
    solutions=[
        (
            CH_P3_STATS["id"],
            r"""
import java.util.*;

public class Solution {
    public static double sum(List<? extends Number> src) {
        double t = 0;
        for (Number n : src) t += n.doubleValue();
        return t;
    }
    public static void fill(List<? super Integer> dst, int a, int b, int c) {
        dst.add(a); dst.add(b); dst.add(c);
    }
    public static List<Number> demo() {
        List<Number> out = new ArrayList<>();
        fill(out, 7, 8, 9);
        return out;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    // W: sum uses intValue() — truncates every non-integer silently.
    // 2.5 contributes 2, so mixed sums drift below the true total.
    public static double sum(List<? extends Number> src) {
        double t = 0;
        for (Number n : src) t += n.intValue();
        return t;
    }
    public static void fill(List<? super Integer> dst, int a, int b, int c) {
        dst.add(a); dst.add(b); dst.add(c);
    }
    public static List<Number> demo() {
        List<Number> out = new ArrayList<>();
        fill(out, 7, 8, 9);
        return out;
    }
}
""",
        ),
        (
            CH_P3_MAX["id"],
            r"""
import java.util.*;

public class Solution {
    public static <T extends Comparable<T>> T max(List<T> xs) {
        if (xs == null || xs.isEmpty()) throw new IllegalArgumentException("xs required");
        T best = xs.get(0);
        for (T x : xs) if (x.compareTo(best) > 0) best = x;
        return best;
    }
    public static Integer maxInt(List<Integer> xs) { return max(xs); }
    public static String maxString(List<String> xs) { return max(xs); }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static <T extends Comparable<T>> T max(List<T> xs) {
        if (xs == null || xs.isEmpty()) throw new IllegalArgumentException("xs required");
        T best = xs.get(0);
        // W: comparison flipped — converges to the MINIMUM, the classic
        // sign-slip in comparison loops.
        for (T x : xs) if (x.compareTo(best) < 0) best = x;
        return best;
    }
    public static Integer maxInt(List<Integer> xs) { return max(xs); }
    public static String maxString(List<String> xs) { return max(xs); }
}
""",
        ),
        (
            CH_P3_ERASURE["id"],
            r"""
import java.util.*;
import java.util.function.Function;

public class Solution {
    public static <T> List<T> fill(int n, Class<T> type, Function<Object, T> maker) {
        List<T> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(maker.apply(i));
        return out;
    }
    public static <T> List<T> nCopiesOf(int n, T value) {
        List<T> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(value);
        return out;
    }
}
""",
            r"""
import java.util.*;
import java.util.function.Function;

public class Solution {
    public static <T> List<T> fill(int n, Class<T> type, Function<Object, T> maker) {
        List<T> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(maker.apply(i));
        return out;
    }
    // W: fills n+1 copies — off-by-one the size-sensitive test catches.
    public static <T> List<T> nCopiesOf(int n, T value) {
        List<T> out = new ArrayList<>();
        for (int i = 0; i <= n; i++) out.add(value);
        return out;
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — generics

You can now: bound type parameters so methods actually work, choose
wildcards by the PECS rule, and route around erasure with Class tokens.
Prove it with a reusable collector API.
"""

CP_MDX_VI = r"""
## Checkpoint — generic

Giờ bạn có thể: đặt bound cho type parameter để method thực sự chạy, chọn
wildcard theo quy tắc PECS, và né erasure bằng Class token. Chứng minh với
một API gom dữ liệu tái sử dụng.
"""

CH_CP3 = challenge(
    "javi-checkpoint-m3-generics",
    "Reusable Bounded Collector API",
    r"""Build a small generic API inside `Solution`:
- `static <T extends Comparable<T>> List<T> topN(List<T> xs, int n)` —
  the n largest elements in DESCENDING order; n larger than size returns
  all; n <= 0 throws IllegalArgumentException; xs null/empty throws too.
- `static double sumNumbers(List<? extends Number> xs)` — PECS producer.
- `static <T> List<? super T> drain(List<T> src, List<? super T> dst)` —
  moves every element from src into dst and returns dst; src ends empty.

All three signatures must keep the generic promises above (the tests
compile call sites that would fail with weaker types).""",
    r"""
import java.util.*;

public class Solution {
    // Provide topN, sumNumbers, drain here.
}
""",
    [
        (
            "topN descending",
            r"""
checkEq(Solution.topN(List.of(1, 9, 4, 9), 2), List.of(9, 9), "two largest, ties kept");
""",
            "Sort descending; take first n; duplicates count individually.",
        ),
        (
            "topN validates n",
            r"""
try { Solution.topN(List.of(1), 0); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "threw"); }
""",
            "n <= 0 throws IllegalArgumentException.",
        ),
        (
            "sumNumbers wildcard",
            r"""
checkNear(Solution.sumNumbers(List.of(1, 2.5)), 3.5, 1e-9, "wildcard sum");
""",
            "Reads via doubleValue().",
        ),
        (
            "drain moves and returns dst",
            r"""
List<Integer> src = new ArrayList<>(List.of(1, 2, 3));
List<Object> dst = new ArrayList<>(List.of(0));
List<? super Integer> out = Solution.drain(src, dst);
checkEq(out, List.of(0, 1, 2, 3), "dst gained all");
checkEq(src.isEmpty(), true, "src drained empty");
""",
            "Iterate src, addAll into dst, clear src, return dst.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CH_CP3 = vi_challenge(
    "API gom dữ liệu tái sử dụng",
    r"""Xây một API generic nhỏ bên trong `Solution`:
- `static <T extends Comparable<T>> List<T> topN(List<T> xs, int n)` —
  n phần tử lớn nhất theo thứ tự GIẢM DẦN; n lớn hơn size trả tất cả;
  n <= 0 ném IllegalArgumentException; xs null/rỗng cũng ném.
- `static double sumNumbers(List<? extends Number> xs)` — producer PECS.
- `static <T> List<? super T> drain(List<T> src, List<? super T> dst)` —
  dời mọi phần tử từ src sang dst rồi trả dst; src kết thúc rỗng.

Cả ba chữ ký phải giữ đúng lời hứa generic (test biên dịch các điểm gọi
sẽ vỡ nếu kiểu yếu hơn).""",
    [
        ("topN giảm dần", "Sắp giảm dần; lấy n đầu; phần tử trùng đếm riêng."),
        ("topN kiểm tra n", "n <= 0 ném IllegalArgumentException."),
        ("sumNumbers wildcard", "Đọc qua doubleValue()."),
        ("drain dời và trả dst", "Duyệt src, addAll vào dst, clear src, trả dst."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-generics",
    "Checkpoint: Generics & PECS",
    "Graded checkpoint: a bounded topN, a wildcard sum, and a drain that exercises both wildcard directions.",
    15,
    CP_MDX,
    "Checkpoint: Generic & PECS",
    "Checkpoint chấm điểm: topN có bound, tổng wildcard, và drain tập cả hai hướng wildcard.",
    CP_MDX_VI,
    CH_CP3,
    VI_CH_CP3,
    solution=r"""
import java.util.*;

public class Solution {
    public static <T extends Comparable<T>> List<T> topN(List<T> xs, int n) {
        if (xs == null || xs.isEmpty()) throw new IllegalArgumentException("xs required");
        if (n <= 0) throw new IllegalArgumentException("n must be positive");
        List<T> sorted = new ArrayList<>(xs);
        sorted.sort(Comparator.reverseOrder());
        return new ArrayList<>(sorted.subList(0, Math.min(n, sorted.size())));
    }

    public static double sumNumbers(List<? extends Number> xs) {
        double t = 0;
        for (Number n : xs) t += n.doubleValue();
        return t;
    }

    public static <T> List<? super T> drain(List<T> src, List<? super T> dst) {
        dst.addAll(src);
        src.clear();
        return dst;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public static <T extends Comparable<T>> List<T> topN(List<T> xs, int n) {
        if (xs == null || xs.isEmpty()) throw new IllegalArgumentException("xs required");
        if (n <= 0) throw new IllegalArgumentException("n must be positive");
        List<T> sorted = new ArrayList<>(xs);
        // W: ASCENDING order — returns the SMALLEST n. Any descending
        // expectation (and duplicate-max handling) exposes the bug.
        sorted.sort(Comparator.naturalOrder());
        return new ArrayList<>(sorted.subList(0, Math.min(n, sorted.size())));
    }

    public static double sumNumbers(List<? extends Number> xs) {
        double t = 0;
        for (Number n : xs) t += n.doubleValue();
        return t;
    }

    public static <T> List<? super T> drain(List<T> src, List<? super T> dst) {
        dst.addAll(src);
        src.clear();
        return dst;
    }
}
""",
)
