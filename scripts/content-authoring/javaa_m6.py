#!/usr/bin/env python3
"""Java — Advanced — Module 6: javaa-generics-type-system.

Erasure (and what the JVM actually keeps), reified arrays vs erased generics,
wildcard capture in copy-style APIs, recursive self-types for fluent APIs,
and the Class<T>-token heterogeneous container (Effective Java Item 33) as
the checkpoint. House conventions: raw triple-quoted Java strings,
self-contained tests, Solution-qualified refs, explicit CjTestBase messages,
Ws are behaviorally wrong (never merely stylistic).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-generics-type-system"

L_ERASURE_EN = """
**Type erasure**: generics exist at *compile time only*. `ArrayList<String>`
and `ArrayList<Integer>` are the *same class* at runtime — one `ArrayList`
class, checked at the door by the compiler, unverified inside. The compiler
inserts casts where values leave generic boundaries and generates **bridge
methods** when overrides need to match an erased signature.

```java
List<String> a = new ArrayList<>();
List<Integer> b = new ArrayList<>();
a.getClass() == b.getClass()   // true — one erased class
```

**Arrays are the opposite**: reified and covariant.

```java
Object[] objs = new String[1];   // legal — arrays are covariant
objs[0] = 42;                    // ArrayStoreException AT RUNTIME
```

The array knows its element type and enforces it with a runtime check; the
generic list cannot even know its type argument. This is why
`new T[]` is illegal, why `instanceof List<String>` cannot be written, and
why `String[].class != Integer[].class` while the two lists share a class.
Covariance + reification = the runtime store check; invariance + erasure =
the compile-time door check. Two different safety strategies.
"""
L_ERASURE_VI = """
**Type erasure**: generic chỉ tồn tại ở *lúc biên dịch*. `ArrayList<String>`
và `ArrayList<Integer>` là *cùng một class* lúc chạy — một class `ArrayList`,
compiler kiểm ở cửa, bên trong không kiểm. Compiler chèn cast tự động tại ranh
giới generic và sinh **bridge method** khi override cần khớp chữ ký đã bị xóa.

```java
List<String> a = new ArrayList<>();
List<Integer> b = new ArrayList<>();
a.getClass() == b.getClass()   // true — một class duy nhất sau erasure
```

**Mảng thì ngược lại**: reified và covariant.

```java
Object[] objs = new String[1];   // hợp lệ — mảng covariant
objs[0] = 42;                    // ArrayStoreException LÚC CHẠY
```

Mảng biết kiểu phần tử của mình và kiểm tra lúc chạy; list generic thậm chí
không biết kiểu tham số của mình. Vì vậy `new T[]` bất hợp pháp, không viết
được `instanceof List<String>`, và `String[].class != Integer[].class` trong
khi hai list dùng chung một class. Covariance + reification = kiểm tra store
lúc chạy; invariance + erasure = kiểm tra cửa lúc biên dịch. Hai chiến lược
an toàn khác nhau.
"""

L_WILDCARDS_EN = """
**PECS** from Intermediate, applied at API-design depth. A *copy* API reads
from one list and writes to another:

```java
static <T> void copy(List<? extends T> src, List<? super T> dst) {
    for (T t : src) dst.add(t);
}
```

Two wildcards, one inference point: `T` is fixed from the call site, `src`
produces `T`s, `dst` consumes them. When a parameter's type is
`List<?>` *without* a type variable, you need **wildcard capture** — a
private helper reifies the unknown:

```java
static void swap(List<?> list, int i, int j) {
    swapHelper(list, i, j);
}
private static <E> void swapHelper(List<E> list, int i, int j) {
    list.set(i, list.set(j, list.get(i)));   // only legal with a real E
}
```

`list.set(...)` on a raw `List<?>` does not compile — the compiler cannot
prove type safety of the unknown; inside the helper, `E` is a *real* type and
the same operations are provably safe. Capture is not a trick; it is how you
tell the compiler "the unknown element type is *fixed* for this call".
"""
L_WILDCARDS_VI = """
**PECS** từ Intermediate, áp dụng ở độ sâu thiết kế API. API *copy* đọc từ một
list và ghi vào list khác:

```java
static <T> void copy(List<? extends T> src, List<? super T> dst) {
    for (T t : src) dst.add(t);
}
```

Hai wildcard, một điểm suy diễn: `T` cố định theo lời gọi, `src` *sản xuất*
`T`, `dst` *tiêu thụ* chúng. Khi kiểu tham số là `List<?>` *không* có biến
kiểu, bạn cần **wildcard capture** — một helper private đặt tên cho cái chưa
biết:

```java
static void swap(List<?> list, int i, int j) {
    swapHelper(list, i, j);
}
private static <E> void swapHelper(List<E> list, int i, int j) {
    list.set(i, list.set(j, list.get(i)));   // chỉ hợp lệ với E thật
}
```

`list.set(...)` trên `List<?>` thô không biên dịch được — compiler không chứng
minh được an toàn của cái chưa biết; trong helper, `E` là kiểu *thật* và cùng
một phép toán trở nên chứng minh được. Capture không phải mẹo; đó là cách nói
với compiler "kiểu phần tử chưa biết này *cố định* trong suốt lời gọi".
"""

L_SELF_EN = """
**Recursive generics** (the CRTP idiom) make fluent APIs return the *subclass*
type:

```java
abstract static class Node<Self extends Node<Self>> {
    private final List<String> labels = new ArrayList<>();
    @SuppressWarnings("unchecked")
    public Self label(String l) { labels.add(l); return (Self) this; }
}
static class Task extends Node<Task> { }
```

`new Task().label("a").label("b")` stays a `Task` — every link in the chain
returns `Self`. The cast `(Self) this` is safe *by convention*: the subclass
promises `Self` is itself. Its known cost: self-types do not survive
*re-parenting* — `Job extends Task` cannot also be `Node<Job>`; a class has
one generic parent.

**Class tokens**: generics are erased, but a `Class<T>` object *is* the
runtime type. `type.cast(value)` and `type.isInstance(value)` turn erased
storage into checked retrieval — the foundation of type-safe registries,
DI containers, and JSON binders. Where erasure loses the type, an explicit
token carries it.
"""
L_SELF_VI = """
**Recursive generics** (idiom CRTP) giúp fluent API trả về kiểu *lớp con*:

```java
abstract static class Node<Self extends Node<Self>> {
    private final List<String> labels = new ArrayList<>();
    @SuppressWarnings("unchecked")
    public Self label(String l) { labels.add(l); return (Self) this; }
}
static class Task extends Node<Task> { }
```

`new Task().label("a").label("b")` vẫn là `Task` — mọi mắt xích trả về `Self`.
Cast `(Self) this` an toàn *theo quy ước*: lớp con hứa `Self` là chính nó. Cái
giá đã biết: self-type không sống sót qua việc *đổi cha* — `Job extends Task`
không thể đồng thời là `Node<Job>`; một lớp chỉ có một cha generic.

**Class token**: generic bị xóa, nhưng đối tượng `Class<T>` *chính là* kiểu lúc
chạy. `type.cast(value)` và `type.isInstance(value)` biến kho lưu trữ đã mất
kiểu thành truy vấn có kiểm — nền tảng của registry an toàn kiểu, DI container,
JSON binder. Ở nơi erasure mất kiểu, token tường minh mang kiểu thay.
"""

write_module(
    M, "Generics & the Type System",
    "Erasure vs reified arrays, wildcard capture, recursive self-types, and Class-token APIs.",
    "Generics & Hệ thống kiểu",
    "Erasure vs mảng reified, wildcard capture, self-types đệ quy, và API dựa trên Class-token.",
    ["javaa-generics-erasure", "javaa-generics-wildcards", "javaa-generics-selftypes"],
    ["javaa-p6-generics"],
)

write_lesson(M, "javaa-generics-erasure",
    "Erasure and reified arrays",
    "What the JVM keeps (nothing) vs what arrays keep (everything), and the two safety strategies.",
    16, L_ERASURE_EN,
    "Erasure và mảng reified",
    "JVM giữ gì (không gì) vs mảng giữ gì (tất cả), và hai chiến lược an toàn.",
    L_ERASURE_VI)

write_lesson(M, "javaa-generics-wildcards",
    "Wildcards and capture",
    "PECS in copy APIs, and wildcard capture: naming the unknown so operations compile.",
    17, L_WILDCARDS_EN,
    "Wildcard và capture",
    "PECS trong API copy, và wildcard capture: đặt tên cho cái chưa biết để phép toán biên dịch được.",
    L_WILDCARDS_VI)

write_lesson(M, "javaa-generics-selftypes",
    "Self-types and Class tokens",
    "Recursive generics for fluent subclass APIs, and Class<T> tokens carrying types through erasure.",
    18, L_SELF_EN,
    "Self-type và Class token",
    "Generic đệ quy cho fluent API subclass, và token Class<T> mang kiểu xuyên qua erasure.",
    L_SELF_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_ERASURE = challenge(
    "javaa-p6-erasure",
    "Prove erasure to yourself",
    "1. `static boolean sameErasure()` — true iff `new ArrayList<String>().getClass()` is the\n"
    "SAME object as `new ArrayList<Integer>().getClass()` (==).\n"
    "2. `static boolean arraysReified()` — true iff `String[].class != Integer[].class`.\n"
    "3. `static String classOfAList()` — return `new ArrayList<String>().getClass().getName()`.\n"
    "4. `static String arrayStore()` — inside the method: `Object[] objs = new String[1];`\n"
    "then attempt `objs[0] = 42;` catching the runtime failure; return exactly\n"
    "\"ArrayStoreException\" (arrays enforce element type at runtime).",
    P_BOILER,
    [
        ("erased generics share one class", r"""
checkTrue(Solution.sameErasure(), "List<String> and List<Integer> share a class");
checkTrue(Solution.arraysReified(), "array classes are distinct");
checkEq(Solution.classOfAList(), "java.util.ArrayList", "erasure in one string");
checkEq(Solution.arrayStore(), "ArrayStoreException", "covariant arrays check at runtime");
""", "All four facts, executed."),
    ],
    level="guided",
)
CH_ERASURE_VI = vi_challenge(
    "Tự chứng minh erasure",
    "sameErasure/arraysReified/classOfAList/arrayStore: bốn sự thật về erasure và mảng, chạy kiểm chứng.",
    [("Hai list dùng chung một class", "getClass() của List<String> và List<Integer> là một."),
     ("Class mảng phân biệt", "String[].class != Integer[].class."),
     ("Covariant mảng kiểm lúc chạy", "objs[0] = 42 trên Object[] thật là String[] nổ ArrayStoreException.")],
)

CH_COPY = challenge(
    "javaa-p6-copy-capture",
    "The copy API, typed correctly",
    "1. `static <T> void copy(List<? extends T> src, List<? super T> dst)` — append every\n"
    "element of src to the end of dst. Must NOT disturb existing dst content.\n"
    "2. `static void swap(List<?> list, int i, int j)` — swap two elements. Because `?`\n"
    "cannot be written to, implement via a private generic capture helper\n"
    "`static <E> void swapHelper(List<E> list, int i, int j)` and call it.\n"
    "Both must compile with exactly these signatures (wildcards in the public API).",
    P_BOILER,
    [
        ("copy appends without disturbing", r"""
java.util.List<Number> dst = new java.util.ArrayList<>(java.util.List.<Number>of(999));
Solution.copy(java.util.List.of(1, 2), dst);
checkEq(dst, java.util.List.of(999, 1, 2), "existing content preserved");
""", "PECS: src produces, dst consumes."),
        ("swap via wildcard capture", r"""
java.util.List<String> xs = new java.util.ArrayList<>(java.util.List.of("a", "b", "c"));
Solution.swap(xs, 0, 2);
checkEq(xs, java.util.List.of("c", "b", "a"), "captured helper swaps");
""", "The unknown becomes a named E inside the helper."),
    ],
    level="independent",
)
CH_COPY_VI = vi_challenge(
    "API copy, đúng kiểu",
    "copy giữ nguyên nội dung sẵn có của dst; swap hoạt động qua capture helper với chữ ký wildcard công khai.",
    [("Copy không phá nội dung sẵn có", "src sản xuất, dst tiêu thụ; 999 đứng đầu."),
     ("Swap qua wildcard capture", "Cái chưa biết thành E có tên bên trong helper.")],
)

CH_BUILDER = challenge(
    "javaa-p6-builder",
    "Self-typed fluent API",
    "Inside Solution, write:\n"
    "1. `abstract static class Node<Self extends Node<Self>>` with an INSTANCE-level\n"
    "`List<String> labels` and `public Self label(String l)` that records the label and\n"
    "returns `(Self) this` (annotated @SuppressWarnings(\"unchecked\")).\n"
    "2. `static class Task extends Node<Task>` with `public String describe()` returning\n"
    "\"Task\" + labels (e.g. `Task[a, b]`).\n"
    "3. `static class Job extends Node<Job>` with describe() prefixing \"Job\".\n"
    "Instances must NOT share state: labeling one object must never appear in another's\n"
    "describe().",
    P_BOILER,
    [
        ("fluent chain preserves the subtype", r"""
Solution.Task t = new Solution.Task().label("a").label("b");
checkTrue(t instanceof Solution.Task, "chaining keeps Task");
checkTrue(t.describe().contains("a") && t.describe().contains("b"), "labels recorded");
""", "Every link returns Self."),
        ("two subtypes, one parent", r"""
Solution.Job j = new Solution.Job().label("x");
checkTrue(j instanceof Solution.Job, "Job chains as Job");
checkTrue(j.describe().startsWith("Job"), "own describe prefix");
""", "Node<Job> and Node<Task> coexist."),
        ("no shared state between instances", r"""
Solution.Task t1 = new Solution.Task().label("a");
Solution.Task t2 = new Solution.Task().label("b");
checkTrue(!t1.describe().contains("b"), "instances do not bleed state");
""", "Per-instance labels, not statics."),
    ],
    level="real-world",
)
CH_BUILDER_VI = vi_challenge(
    "Fluent API tự kiểu",
    "Node<Self>/Task/Job: chuỗi fluent giữ nguyên kiểu subclass, hai lớp con cùng cha, và không chia sẻ trạng thái giữa các instance.",
    [("Chuỗi fluent giữ subtype", "Mọi mắt xích trả về Self."),
     ("Hai lớp con, một cha", "Node<Job> và Node<Task> cùng tồn tại."),
     ("Không rò trạng thái", "Label theo instance, không phải static.")],
)

write_practice(M, "javaa-p6-generics",
    "Type-system drills",
    "Prove erasure, write capture-style APIs, and build a self-typed fluent hierarchy.",
    "Bài tập hệ thống kiểu",
    "Chứng minh erasure, viết API dạng capture, và xây hệ phân cấp fluent tự kiểu.",
    "javaa-generics-selftypes", 55, "advanced",
    [CH_ERASURE, CH_COPY, CH_BUILDER],
    {"javaa-p6-erasure": CH_ERASURE_VI, "javaa-p6-copy-capture": CH_COPY_VI, "javaa-p6-builder": CH_BUILDER_VI},
    solutions=[
        ("javaa-p6-erasure", r"""
import java.util.*;

public class Solution {
    public static boolean sameErasure() {
        return new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass();
    }

    public static boolean arraysReified() {
        Class<?> a = String[].class;   // via Class<?> — direct == on the literals is a
        Class<?> b = Integer[].class;  // compile-time error: incomparable types
        return a != b;
    }

    public static String classOfAList() {
        return new ArrayList<String>().getClass().getName();
    }

    public static String arrayStore() {
        try {
            Object[] objs = new String[1];
            objs[0] = 42;
            return "no error";
        } catch (ArrayStoreException e) {
            return "ArrayStoreException";
        }
    }
}
""", r"""
import java.util.*;

public class Solution {
    public static boolean sameErasure() {
        return new ArrayList<String>().getClass() != new ArrayList<Integer>().getClass();  // WRONG: generics are erased
    }

    public static boolean arraysReified() {
        Class<?> a = String[].class;
        Class<?> b = Integer[].class;
        return a == b;   // WRONG: compiles via Class<?> but is false at runtime
    }

    public static String classOfAList() {
        return new ArrayList<String>().getClass().getSimpleName();   // WRONG: getName() expected
    }

    public static String arrayStore() {
        try {
            Object[] objs = new String[1];
            objs[0] = 42;
            return "no error";
        } catch (ClassCastException e) {           // WRONG: the thrown type is ArrayStoreException
            return "ArrayStoreException";
        }
    }
}
"""),
        ("javaa-p6-copy-capture", r"""
import java.util.*;

public class Solution {
    public static <T> void copy(List<? extends T> src, List<? super T> dst) {
        for (T t : src) dst.add(t);
    }

    public static void swap(List<?> list, int i, int j) {
        swapHelper(list, i, j);
    }

    private static <E> void swapHelper(List<E> list, int i, int j) {
        list.set(i, list.set(j, list.get(i)));
    }
}
""", r"""
import java.util.*;

public class Solution {
    public static <T> void copy(List<? extends T> src, List<? super T> dst) {
        dst.clear();               // WRONG: destroys existing destination content
        for (T t : src) dst.add(t);
    }

    public static void swap(List<?> list, int i, int j) {
        // WRONG: no capture helper — this cannot compile against List<?> ...
        // (kept compilable by casting through raw types, which erases the check)
        List raw = list;
        Object a = raw.get(i);
        raw.set(i, raw.get(j));
        raw.set(j, a);
    }
}
"""),
        ("javaa-p6-builder", r"""
import java.util.*;

public class Solution {
    abstract static class Node<Self extends Node<Self>> {
        private final List<String> labels = new ArrayList<>();

        @SuppressWarnings("unchecked")
        public Self label(String l) {
            labels.add(l);
            return (Self) this;
        }

        String describeOf(String prefix) {
            return prefix + labels;
        }
    }

    public static class Task extends Node<Task> {
        public String describe() { return describeOf("Task"); }
    }

    public static class Job extends Node<Job> {
        public String describe() { return describeOf("Job"); }
    }
}
""", r"""
import java.util.*;

public class Solution {
    abstract static class Node<Self extends Node<Self>> {
        private static final List<String> labels = new ArrayList<>();   // WRONG: static — shared by every instance

        @SuppressWarnings("unchecked")
        public Self label(String l) {
            labels.add(l);
            return (Self) this;
        }

        String describeOf(String prefix) {
            return prefix + labels;
        }
    }

    public static class Task extends Node<Task> {
        public String describe() { return describeOf("Task"); }
    }

    public static class Job extends Node<Job> {
        public String describe() { return describeOf("Job"); }
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the heterogeneous type-safe container

Generics are erased — but a `Class<T>` token *is* the runtime type. Build the
type-safe heterogeneous container: one map, many value types, retrieval that
cannot lie about its type. This is the 60-line ancestor of every DI container
and JSON binder.
"""

CP_CH = challenge(
    "javaa-checkpoint-m6-task",
    "Checkpoint: Class-token container",
    "Inside Solution, implement `public static class Types` — the type-safe\n"
    "heterogeneous container:\n"
    "1. Private `Map<Class<?>, Object> data = new HashMap<>()`.\n"
    "2. `public <T> void put(Class<T> type, T value)` — store under the token.\n"
    "3. `public <T> T get(Class<T> type)` — retrieve via `type.cast(...)` so the\n"
    "returned value is genuinely a T (no unchecked warnings).\n"
    "4. `public <T> boolean has(Class<T> type)` — true iff a value was put for that token.\n"
    "Retrieval must be exact: two different tokens hold two different values, and each\n"
    "get() returns the value stored under ITS OWN token.",
    P_BOILER,
    [
        ("two tokens, two values, exact retrieval", r"""
Solution.Types box = new Solution.Types();
box.put(String.class, "hi");
box.put(Integer.class, 7);
checkEq(box.get(String.class), "hi", "string by its token");
checkEq(box.get(Integer.class), 7, "integer by its token");
checkTrue(box.has(String.class) && !box.has(Double.class), "has reflects tokens");
""", "Each token retrieves exactly what it stored."),
        ("subtype tokens are honored", r"""
Solution.Types box = new Solution.Types();
box.put(Number.class, 42);
checkEq(box.get(Number.class), 42, "Number token holds an Integer value");
checkTrue(box.get(Number.class) instanceof Number, "cast via token");
""", "type.cast works through the hierarchy."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: Container dùng Class token",
    "Types: put/get/has theo Class<T> token; get trả về đúng giá trị lưu dưới token của nó, cast qua type.cast.",
    [("Hai token, hai giá trị", "Mỗi token lấy đúng giá trị của nó."),
     ("Token subtype được tôn trọng", "type.cast hoạt động xuyên qua phân cấp.")],
)

write_checkpoint(M, "javaa-checkpoint-m6",
    "Checkpoint: The Heterogeneous Type-Safe Container",
    "Carry types through erasure with Class<T> tokens and type.cast retrieval.",
    25, CP_MD,
    "Checkpoint: Container an toàn kiểu dùng Class token",
    "Mang kiểu xuyên qua erasure bằng token Class<T> và truy vấn type.cast.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;

public class Solution {
    public static class Types {
        private final Map<Class<?>, Object> data = new HashMap<>();

        public <T> void put(Class<T> type, T value) {
            data.put(type, value);
        }

        public <T> T get(Class<T> type) {
            return type.cast(data.get(type));
        }

        public <T> boolean has(Class<T> type) {
            return data.containsKey(type);
        }
    }
}
""", wrong=r"""
import java.util.*;

public class Solution {
    public static class Types {
        private final Map<String, Object> data = new HashMap<>();   // WRONG: single "value" slot

        public <T> void put(Class<T> type, T value) {
            data.put("value", value);
        }

        @SuppressWarnings("unchecked")
        public <T> T get(Class<T> type) {
            return (T) data.get("value");    // WRONG: returns the LAST put for ANY token
        }

        public <T> boolean has(Class<T> type) {
            return data.containsKey("value");
        }
    }
}
""")

print("module 6 authored")
