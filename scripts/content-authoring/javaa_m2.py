#!/usr/bin/env python3
"""Java — Advanced — Module 2: java-jvm-bytecode.

JVM architecture through observables: when class initialization triggers
(Class.forName vs class-literal), the constant-pool/boxing/interning identity
model, and compiler-generated constructs (synthetic lambda methods) detected
via reflection. javap/JFR-style tooling is taught in prose — the sandbox has
no shell — but every tested behavior is executable Java. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "java-jvm-bytecode"

L_JVM_EN = """
The JVM spec (§2.5, §5) divides runtime memory into areas with different
lifetimes and failure modes. The ones that matter daily:

- **Heap**: all objects; shared by all threads; GC-managed. `OutOfMemoryError`
  here means your *live* set does not fit.
- **Per-thread stacks**: one frame per invoked method (locals + operand
  stack). `StackOverflowError` means *depth*, not heap size.
- **Metaspace**: class metadata (native memory). `OutOfMemoryError:
  Metaspace` usually means classes are being generated at runtime and never
  unloaded.
- **PC register** per thread — why threads can be suspended anywhere.

**Class initialization** (JLS §12.4) is lazy and triggerable. Two ways to
name a class behave differently:

```java
Class<?> a = Loaded.class;                  // NO static init
Class<?> b = Class.forName("Loaded");       // static init runs
```

A class literal is a compile-time constant reference — it does not *use* the
class. `forName` initializes it. So does `new`, static method calls, and
accessing a non-constant static field. This laziness is why a broken static
initializer can hide for weeks until the first real use throws
`ExceptionInInitializerError`.
"""
L_JVM_VI = """
JVM spec (§2.5, §5) chia bộ nhớ runtime thành các vùng khác nhau về thời gian
sống và kiểu lỗi. Những vùng quan trọng hằng ngày:

- **Heap**: mọi đối tượng; dùng chung cho mọi thread; GC quản lý.
  `OutOfMemoryError` ở đây nghĩa là tập dữ liệu *sống* không vừa.
- **Stack mỗi thread**: một frame cho mỗi lần gọi phương thức (locals + operand
  stack). `StackOverflowError` nghĩa là *độ sâu*, không phải heap.
- **Metaspace**: metadata của lớp (native memory). `OutOfMemoryError:
  Metaspace` thường nghĩa là lớp đang được sinh runtime và không bao giờ được
  dọn.
- **PC register** mỗi thread — lý do thread có thể bị treo ở bất kỳ đâu.

**Khởi tạo lớp** (JLS §12.4) là lazy và có thể kích chủ động. Hai cách gọi tên
lớp hành xử khác nhau:

```java
Class<?> a = Loaded.class;                  // KHÔNG chạy static init
Class<?> b = Class.forName("Loaded");       // static init chạy
```

Class literal là tham chiếu hằng compile-time — nó không *sử dụng* lớp.
`forName` khởi tạo lớp. `new`, gọi static method, hay đọc static field
không-hằng cũng vậy. Tính lazy này giải thích vì sao static initializer hỏng
có thể trốn hàng tuần cho đến lần dùng thật đầu tiên ném
`ExceptionInInitializerError`.
"""

L_BYTECODE_EN = """
`javac` compiles to **class files** (JVM spec §4): a constant pool of symbols
plus per-method bytecode for a **stack machine**. You have no shell in this
sandbox, so `javap -c` is shown here in prose — but the *consequences* of the
constant pool are executable:

**String identity** — literals live in the pool, deduplicated:

```java
String a = "adv";                 // pool entry
String b = "adv";                 // same pool entry
String c = new String("adv");     // fresh heap object
a == b      // true  — same constant
a == c      // false — different object
a == c.intern()  // true — intern() returns the pool entry
```

**Boxing cache** — `Integer.valueOf` caches -128..127 (JLS §5.1.7):

```java
Integer.valueOf(127) == Integer.valueOf(127)  // true  (same cached box)
Integer.valueOf(128) == Integer.valueOf(128)  // false (new box each time)
```

**Synthetic constructs** — the compiler generates members you never wrote.
A lambda is desugared to a private synthetic method plus an `invokedynamic`
call site. Reflection can see the synthetic method:

```java
Runnable r = () -> {};
Arrays.stream(Solution.class.getDeclaredMethods())
      .anyMatch(Method::isSynthetic)   // true when a lambda exists
```

Reading bytecode is a skill, but *reasoning about identity and generated
members* is the part you will use weekly.
"""
L_BYTECODE_VI = """
`javac` biên dịch ra **class file** (JVM spec §4): một constant pool các ký
hiệu cộng bytecode cho mỗi phương thức chạy trên **máy xếp chồng**. Sandbox
này không có shell nên `javap -c` chỉ trình bày trong văn bản — nhưng *hậu
quả* của constant pool thì chạy kiểm chứng được:

**Identity của String** — literal sống trong pool, được khử trùng lặp:

```java
String a = "adv";                 // entry trong pool
String b = "adv";                 // cùng entry
String c = new String("adv");     // đối tượng mới trên heap
a == b      // true  — cùng hằng
a == c      // false — khác đối tượng
a == c.intern()  // true — intern() trả về entry trong pool
```

**Boxing cache** — `Integer.valueOf` cache -128..127 (JLS §5.1.7):

```java
Integer.valueOf(127) == Integer.valueOf(127)  // true  (cùng box cache)
Integer.valueOf(128) == Integer.valueOf(128)  // false (box mới mỗi lần)
```

**Thành phần synthetic** — compiler sinh ra thành viên bạn không hề viết.
Lambda bị desugar thành một phương thức private synthetic cộng một call site
`invokedynamic`. Reflection nhìn thấy phương thức synthetic đó:

```java
Runnable r = () -> {};
Arrays.stream(Solution.class.getDeclaredMethods())
      .anyMatch(Method::isSynthetic)   // true khi lớp có lambda
```

Đọc bytecode là một kỹ năng, nhưng *suy luận về identity và thành phần sinh
tự động* mới là thứ bạn dùng hằng tuần.
"""

L_STACK_EN = """
Each method invocation pushes a **frame** (locals + operand stack + return
address). Two consequences you can *test*:

**Depth is finite.** Unbounded recursion throws `StackOverflowError` — and it
is just an `Error` you can catch (though you almost never should):

```java
static int forever(int n) { return forever(n + 1); }
try { forever(0); }
catch (StackOverflowError e) { /* depth limit reached */ }
```

**Frames unwind exactly.** When an exception crosses frames, each frame's
`finally`/catch runs inside-to-outside. Combined with the stack-only operand
model, this is why the JVM can produce a precise stack trace at any moment.

Deep recursion in production code is a design smell — prefer iteration or
explicit stacks — but a professional must recognize the *signature* of each
failure: SOE = depth, OOM = live set, Metaspace OOM = class churn.
"""
L_STACK_VI = """
Mỗi lần gọi phương thức đẩy một **frame** (locals + operand stack + địa chỉ
trả về). Hai hậu quả bạn *kiểm chứng được*:

**Độ sâu có hạn.** Đệ quy vô hạn ném `StackOverflowError` — và nó chỉ là một
`Error` bạn có thể catch (dù gần như không bao giờ nên làm vậy):

```java
static int forever(int n) { return forever(n + 1); }
try { forever(0); }
catch (StackOverflowError e) { /* chạm giới hạn độ sâu */ }
```

**Frame được unwound chính xác.** Khi exception đi qua nhiều frame, mỗi
`finally`/catch chạy từ trong ra ngoài. Kết hợp với mô hình operand trên
stack, đây là lý do JVM luôn in được stack trace chính xác tại mọi thời điểm.

Đệ quy sâu trong code production là mùi thiết kế — hãy dùng vòng lặp hoặc
stack tường minh — nhưng dev chuyên nghiệp phải nhận ra *chữ ký* của từng kiểu
lỗi: SOE = độ sâu, OOM = tập sống, Metaspace OOM = sinh lớp quá nhiều.
"""

write_module(
    M, "JVM Architecture & Bytecode",
    "Runtime data areas, class-initialization triggers, constant-pool identity, boxing caches, synthetic members, and stack frames.",
    "Kiến trúc JVM & Bytecode",
    "Các vùng nhớ runtime, điều kiện kích khởi tạo lớp, identity của constant pool, boxing cache, thành phần synthetic, và stack frame.",
    ["javaa-jvm-runtime", "javaa-bytecode-model", "javaa-stack-model"],
    ["javaa-p2-jvm"],
)

write_lesson(M, "javaa-jvm-runtime",
    "Runtime data areas and class loading",
    "Heap vs stacks vs metaspace, and the exact triggers of lazy class initialization.",
    16, L_JVM_EN,
    "Vùng nhớ runtime và nạp lớp",
    "Heap so với stack so với metaspace, và các điều kiện kích khởi tạo lớp lazy.",
    L_JVM_VI)

write_lesson(M, "javaa-bytecode-model",
    "Constant pool, identity, and synthetic members",
    "String interning, the Integer boxing cache, and compiler-generated methods you can detect with reflection.",
    16, L_BYTECODE_EN,
    "Constant pool, identity, và thành phần synthetic",
    "String interning, boxing cache của Integer, và phương thức do compiler sinh mà reflection nhìn thấy được.",
    L_BYTECODE_VI)

write_lesson(M, "javaa-stack-model",
    "Stack frames and failure signatures",
    "StackOverflowError as depth, OutOfMemoryError as live set, and exact frame unwinding.",
    13, L_STACK_EN,
    "Stack frame và chữ ký lỗi",
    "StackOverflowError là độ sâu, OutOfMemoryError là tập sống, và unwinding frame chính xác.",
    L_STACK_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_TRIGGER = challenge(
    "javaa-p2-init-trigger",
    "Class-initialization triggers",
    "Implement `static List<String> triggerTrace()`:\n"
    "1. `static String touch()` — references `Marker.class` (a literal) and returns \"literal\";\n"
    "   it must NOT cause Marker's static initializer to run.\n"
    "2. `static String force()` — calls `Class.forName(\"Solution$Marker\")` and returns \"forName\";\n"
    "   it MUST cause Marker's static initializer to run.\n"
    "3. `public static class Marker` with `static { trace.add(\"Marker<clinit>\"); }` where trace "
    "is a `static final List<String>` you own.\n"
    "4. `triggerTrace()` calls `touch()` then `force()` then returns the trace — which must show "
    "the literal did NOT initialize the class but forName did.",
    P_BOILER,
    [
        ("literal does not initialize", r"""
java.util.List<String> t = Solution.triggerTrace();
checkEq(t, java.util.List.of("Marker<clinit>"), "only forName triggers <clinit>");
""", "Marker.class is a constant reference, not an active use."),
    ],
    level="guided",
)
CH_TRIGGER_VI = vi_challenge(
    "Điều kiện kích khởi tạo lớp",
    "Cài triggerTrace: literal KHÔNG kích <clinit>, forName CÓ kích; trace phải chứng minh điều đó.",
    [("Literal không khởi tạo", "Marker.class là tham chiếu hằng, không phải dùng chủ động.")],
)

CH_IDENTITY = challenge(
    "javaa-p2-identity-matrix",
    "The identity matrix",
    "Implement four static predicates — each must use `==` (identity), not equals:\n"
    "1. `static boolean pooledLiterals()` — is `\"jvm\" == \"jvm\"` (two literals)?\n"
    "2. `static boolean newStringSameAsLiteral()` — is `new String(\"jvm\") == \"jvm\"`?\n"
    "3. `static boolean internedMatches()` — is `new String(\"jvm\").intern() == \"jvm\"`?\n"
    "4. `static boolean boxCacheHolds()` — is `Integer.valueOf(127) == Integer.valueOf(127)`?\n"
    "5. `static boolean boxCacheMisses()` — is `Integer.valueOf(128) == Integer.valueOf(128)`?\n"
    "6. `static boolean bigBoxSame()` — is `Integer.valueOf(1000) == Integer.valueOf(1000)`?\n"
    "Return the *actual* results, whatever they are — the tests know the truth.",
    P_BOILER,
    [
        ("constant pool and cache truth", r"""
checkTrue(Solution.pooledLiterals(), "literals are pooled");
checkTrue(!Solution.newStringSameAsLiteral(), "new String is a fresh object");
checkTrue(Solution.internedMatches(), "intern returns the pool entry");
""", "Pool deduplicates literals; new always allocates; intern canonicalizes."),
        ("boxing cache boundaries", r"""
checkTrue(Solution.boxCacheHolds(), "127 is cached");
checkTrue(!Solution.boxCacheMisses(), "128 is outside the cache");
checkTrue(!Solution.bigBoxSame(), "1000 boxes are never shared");
""", "The cache covers exactly -128..127."),
    ],
    level="independent",
)
CH_IDENTITY_VI = vi_challenge(
    "Ma trận identity",
    "Cài các predicate identity bằng `==`: literal pool, new String, intern, và biên boxing cache -128..127.",
    [("Sự thật của pool và cache", "Pool khử trùng lặp literal; new luôn cấp phát; intern chuẩn hóa."),
     ("Biên boxing cache", "Cache đúng bằng -128..127.")],
)

CH_SYNTH = challenge(
    "javaa-p2-synthetic-hunter",
    "Hunt the synthetic method",
    "Implement `static java.util.function.Comparator<String> lambdaComparator()` that returns a "
    "comparator built from a **lambda** (e.g. `(a, b) -> a.length() - b.length()`), and "
    "`static boolean hasSyntheticMember()` that reflects over `Solution.class.getDeclaredMethods()` "
    "and returns true iff at least one method `isSynthetic()` (the lambda's desugared helper).\n"
    "Also implement `static java.util.function.Comparator<String> anonymousComparator()` using an "
    "**anonymous inner class** — anonymous classes do not add synthetic *methods* to Solution.\n"
    "The tests verify both the sorting behavior and the reflective difference.",
    P_BOILER,
    [
        ("lambda comparator sorts", r"""
var xs = new java.util.ArrayList<>(List.of("ccc", "a", "bb"));
xs.sort(Solution.lambdaComparator());
checkEq(xs, List.of("a", "bb", "ccc"), "sorted by length");
""", "Compare by length."),
        ("lambda leaves a synthetic trace", r"""
checkTrue(Solution.hasSyntheticMember(), "lambda desugars to a synthetic method");
""", "Reflect over getDeclaredMethods and look for isSynthetic()."),
        ("anonymous comparator works too", r"""
var xs = new java.util.ArrayList<>(List.of("ccc", "a", "bb"));
xs.sort(Solution.anonymousComparator());
checkEq(xs, List.of("a", "bb", "ccc"), "anonymous class comparator");
""", "new Comparator<String>() { ... } — no lambda here."),
    ],
    level="independent",
)
CH_SYNTH_VI = vi_challenge(
    "Săn thành phần synthetic",
    "Cài comparator bằng lambda (để lại synthetic method) và bằng anonymous class (không để lại), kèm phát hiện qua reflection.",
    [("Lambda comparator sắp đúng", "So sánh theo độ dài."),
     ("Lambda để lại vết synthetic", "Duyệt getDeclaredMethods tìm isSynthetic()."),
     ("Anonymous comparator cũng chạy", "new Comparator<String>() { ... } — không dùng lambda.")],
)

write_practice(M, "javaa-p2-jvm",
    "JVM observable drills",
    "Prove initialization triggers, map the identity matrix, and detect compiler-generated members.",
    "Bài tập JVM quan sát được",
    "Chứng minh điều kiện kích khởi tạo, lập ma trận identity, và phát hiện thành phần do compiler sinh.",
    "javaa-stack-model", 45, "advanced",
    [CH_TRIGGER, CH_IDENTITY, CH_SYNTH],
    {"javaa-p2-init-trigger": CH_TRIGGER_VI, "javaa-p2-identity-matrix": CH_IDENTITY_VI, "javaa-p2-synthetic-hunter": CH_SYNTH_VI},
    solutions=[
        ("javaa-p2-init-trigger", r"""
import java.util.*;

public class Solution {
    static final List<String> trace = new ArrayList<>();

    public static class Marker {
        static { trace.add("Marker<clinit>"); }
    }

    public static String touch() {
        Class<?> c = Marker.class;   // constant reference: no <clinit>
        return "literal";
    }

    public static String force() throws Exception {
        Class<?> c = Class.forName("Solution$Marker");  // active use: <clinit> runs
        return "forName";
    }

    public static List<String> triggerTrace() throws Exception {
        trace.clear();
        touch();
        force();
        return List.copyOf(trace);
    }
}
""", r"""
import java.util.*;

public class Solution {
    static final List<String> trace = new ArrayList<>();

    public static class Marker {
        static { trace.add("Marker<clinit>"); }
    }

    public static String touch() {
        Class<?> c = Marker.class;
        return "literal";
    }

    public static String force() throws Exception {
        // WRONG: uses the class literal — never triggers <clinit>
        Class<?> c = Marker.class;
        return "forName";
    }

    public static List<String> triggerTrace() throws Exception {
        trace.clear();
        touch();
        force();
        return List.copyOf(trace);
    }
}
"""),
        ("javaa-p2-identity-matrix", r"""
public class Solution {
    public static boolean pooledLiterals() { return "jvm" == "jvm"; }
    public static boolean newStringSameAsLiteral() { return new String("jvm") == "jvm"; }
    public static boolean internedMatches() { return new String("jvm").intern() == "jvm"; }
    public static boolean boxCacheHolds() { return Integer.valueOf(127) == Integer.valueOf(127); }
    public static boolean boxCacheMisses() { return Integer.valueOf(128) == Integer.valueOf(128); }
    public static boolean bigBoxSame() { return Integer.valueOf(1000) == Integer.valueOf(1000); }
}
""", r"""
public class Solution {
    // WRONG: uses equals() everywhere — collapses identity into value equality
    public static boolean pooledLiterals() { return "jvm".equals("jvm"); }
    public static boolean newStringSameAsLiteral() { return new String("jvm").equals("jvm"); }
    public static boolean internedMatches() { return new String("jvm").intern().equals("jvm"); }
    public static boolean boxCacheHolds() { return Integer.valueOf(127).equals(Integer.valueOf(127)); }
    public static boolean boxCacheMisses() { return Integer.valueOf(128).equals(Integer.valueOf(128)); }
    public static boolean bigBoxSame() { return Integer.valueOf(1000).equals(Integer.valueOf(1000)); }
}
"""),
        ("javaa-p2-synthetic-hunter", r"""
import java.util.*;

public class Solution {
    public static Comparator<String> lambdaComparator() {
        return (a, b) -> a.length() - b.length();
    }

    public static Comparator<String> anonymousComparator() {
        return new Comparator<String>() {
            @Override public int compare(String a, String b) { return a.length() - b.length(); }
        };
    }

    public static boolean hasSyntheticMember() {
        for (var m : Solution.class.getDeclaredMethods()) {
            if (m.isSynthetic()) return true;
        }
        return false;
    }
}
""", r"""
import java.util.*;

public class Solution {
    // WRONG: anonymous class instead of a lambda — no synthetic method is generated
    public static Comparator<String> lambdaComparator() {
        return new Comparator<String>() {
            @Override public int compare(String a, String b) { return a.length() - b.length(); }
        };
    }

    public static Comparator<String> anonymousComparator() {
        return new Comparator<String>() {
            @Override public int compare(String a, String b) { return a.length() - b.length(); }
        };
    }

    public static boolean hasSyntheticMember() {
        for (var m : Solution.class.getDeclaredMethods()) {
            if (m.isSynthetic()) return true;
        }
        return false;
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the loading detective

Three facts about the JVM must fall out of your one implementation: a class
literal never initializes a class; `forName` does; and the constant pool makes
certain identities true that heap allocation makes false. Assemble the
evidence.
"""

CP_CH = challenge(
    "javaa-checkpoint-m2-task",
    "Checkpoint: assemble the evidence",
    "Implement:\n"
    "1. `static class Probe` with `static final List<String> LOG` and a static block that adds \"probe<clinit>\".\n"
    "2. `static String evidence()` that: (a) references `Probe.class` only, (b) records \"literal-silent:\" + "
    "outerTrace.isEmpty() (NOTE: read Probe state only through a list owned by Solution — reading any "
    "non-constant static of Probe is itself an active use that triggers <clinit>!), (c) calls "
    "`Class.forName(\"Solution$Probe\")`, (d) records \"forName-loud:\" + outerTrace.contains(\"probe<clinit>\"), (e) returns "
    "`\"jvm\" == new String(\"jvm\").intern()` ? \"pool-true\" : \"pool-false\" joined with the two flag strings "
    "as one `;`-separated line in order (b), (d), (e).",
    P_BOILER,
    [
        ("evidence line assembled", r"""
String line = Solution.evidence();
checkContains(line, "literal-silent:true");
checkContains(line, "forName-loud:true");
checkContains(line, "pool-true");
""", "Sequence: literal (silent) → forName (loud) → intern (pool)."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: thám tử nạp lớp",
    "Lắp bằng chứng: literal im lặng, forName ồn ào, intern chuẩn hóa — gộp thành một dòng evidence.",
    [("Dòng bằng chứng", "Trình tự: literal (im) → forName (kích) → intern (pool).")],
)

write_checkpoint(M, "javaa-checkpoint-m2",
    "Checkpoint: The Loading Detective",
    "Assemble runtime evidence that class literals are silent, forName is loud, and the pool canonicalizes.",
    20, CP_MD,
    "Checkpoint: Thám tử nạp lớp",
    "Lắp bằng chứng runtime: class literal im lặng, forName kích hoạt, pool chuẩn hóa identity.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;

public class Solution {
    static final List<String> trace = new ArrayList<>();

    public static class Probe {
        static { trace.add("probe<clinit>"); }               // Probe writes into Solution-owned state
    }

    public static String evidence() throws Exception {
        Class<?> silent = Probe.class;                       // no <clinit>
        boolean litSilent = trace.isEmpty();
        Class.forName("Solution$Probe");                     // <clinit> runs
        boolean forNameLoud = trace.contains("probe<clinit>");
        String pool = ("jvm" == new String("jvm").intern()) ? "pool-true" : "pool-false";
        return "literal-silent:" + litSilent + ";forName-loud:" + forNameLoud + ";" + pool;
    }
}
""", wrong=r"""
import java.util.*;

public class Solution {
    public static class Probe {
        static final List<String> LOG = new ArrayList<>();
        static { LOG.add("probe<clinit>"); }
    }

    static final List<String> trace = new ArrayList<>();

    public static class Probe {
        static { trace.add("probe<clinit>"); }
    }

    public static String evidence() throws Exception {
        // WRONG: never actively uses Probe (so <clinit> never runs), and the
        // intern comparison is against a fresh heap object
        Class<?> silent = Probe.class;
        boolean litSilent = trace.isEmpty();
        Class<?> alsoSilent = Probe.class;
        boolean forNameLoud = trace.contains("probe<clinit>");   // always false now
        String pool = ("jvm" == new String("jvm")) ? "pool-true" : "pool-false";  // fresh object != literal
        return "literal-silent:" + litSilent + ";forName-loud:" + forNameLoud + ";" + pool;
    }
}
""")

print("module 2 authored")
