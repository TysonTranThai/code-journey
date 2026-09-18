#!/usr/bin/env python3
"""Java — Advanced — Module 7: javaa-reflection-di.

Reflection as an engineering tool, not a magic trick: reading class metadata,
runtime-retention annotations driving dispatch, and the checkpoint — a mini
dependency-injection container (constructor injection, recursive resolution,
singletons, cycle detection) built with the JDK alone. No Spring anywhere.
House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-reflection-di"

L_META_EN = """
`Class<?>` is the door to everything the JVM knows about a type:

```java
Class<?> c = Widget.class;
for (Field f : c.getDeclaredFields()) { }   // ALL declared, any visibility
for (Method m : c.getDeclaredMethods()) { }
c.getConstructors();  c.getDeclaredConstructors();
c.isInstance(obj);    c.isInterface();      c.getSuperclass();
```

The `getDeclared*` family ignores inheritance and visibility — it is the
honest inventory. `getFields()`/`getMethods()` return only *accessible*
members (public, including inherited). Confusing the two is the classic
reflection bug: your private fields exist but "aren't found".

**Runtime cost is real but modern**: the JIT can inline through reflective
calls after warmup, so hot-path reflection is no longer automatically slow.
The *real* costs are structural: no compile-time checking (a typo surfaces at
runtime), broken encapsulation (`setAccessible`), and friction with modules
(JDK 17+ blocks deep reflection across module boundaries by default). Rule:
reflection at *framework* boundaries, types at *domain* boundaries.
"""
L_META_VI = """
`Class<?>` là cánh cửa đến mọi thứ JVM biết về một kiểu:

```java
Class<?> c = Widget.class;
for (Field f : c.getDeclaredFields()) { }   // TẤT CẢ khai báo, mọi visibility
for (Method m : c.getDeclaredMethods()) { }
c.getConstructors();  c.getDeclaredConstructors();
c.isInstance(obj);    c.isInterface();      c.getSuperclass();
```

Nhóm `getDeclared*` bỏ qua kế thừa và visibility — đó là bản kê khai trung
thực. `getFields()`/`getMethods()` chỉ trả về thành viên *truy cập được*
(public, kể cả kế thừa). Nhầm hai nhóm này là bug reflection kinh điển: field
private của bạn có tồn tại nhưng "không tìm thấy".

**Chi phí lúc chạy có thật nhưng hiện đại**: JIT có thể inline xuyên qua lời
gọi reflective sau warmup, nên reflection trên đường nóng không còn tự động
chậm. Chi phí *thật* là cấu trúc: không có kiểm tra lúc biên dịch (lỗi chính
tả lộ ra lúc chạy), phá vỡ encapsulation (`setAccessible`), và ma sát với
module (JDK 17+ chặn deep reflection xuyên module mặc định). Quy tắc:
reflection ở *ranh giới framework*, kiểu ở *ranh giới domain*.
"""

L_ANNOT_EN = """
Annotations are typed metadata attached to program elements. Their power
depends entirely on **retention**:

- `SOURCE` — compiler-only (like `@Override`); gone in the class file.
- `CLASS` — in the class file, invisible at runtime (the default, rarely used).
- `RUNTIME` — readable via reflection; this is what frameworks use.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Route { String value(); }
```

Reading them back is the whole trick behind every routing table, validator,
and injection engine:

```java
for (Method m : obj.getClass().getDeclaredMethods()) {
    Route r = m.getAnnotation(Route.class);
    if (r != null) table.put(r.value(), m);
}
```

An annotation with no reader is a comment. The *reader* is the framework —
which means you can write one.
"""
L_ANNOT_VI = """
Annotation là metadata có kiểu gắn lên phần tử chương trình. Sức mạnh phụ thuộc
hoàn toàn vào **retention**:

- `SOURCE` — chỉ cho compiler (như `@Override`); mất trong class file.
- `CLASS` — có trong class file, vô hình lúc chạy (mặc định, hiếm dùng).
- `RUNTIME` — đọc được qua reflection; đây là thứ framework dùng.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Route { String value(); }
```

Đọc ngược lại là toàn bộ trò đằng sau mọi bảng định tuyến, validator, và engine
inject:

```java
for (Method m : obj.getClass().getDeclaredMethods()) {
    Route r = m.getAnnotation(Route.class);
    if (r != null) table.put(r.value(), m);
}
```

Annotation không có người đọc chỉ là bình luận. *Người đọc* mới là framework —
nghĩa là bạn hoàn toàn có thể tự viết một cái.
"""

L_DI_EN = """
A DI container is three recursive rules:

1. **Resolve(type)**: find the constructor, resolve each parameter type, then
   instantiate.
2. **Memoize**: one instance per type (singleton scope) — otherwise every
   resolution builds a fresh object graph.
3. **Detect cycles**: resolving A needs B needs A — without an "in progress"
   set, recursion never terminates (you get a `StackOverflowError` in
   production, at 3 a.m.).

```java
public <T> T resolve(Class<T> type) {
    if (cache.containsKey(type)) return type.cast(cache.get(type));
    if (!inProgress.add(type)) throw new IllegalStateException("circular dependency: " + type);
    Constructor<?> ctor = type.getDeclaredConstructors()[0];
    Object[] args = Arrays.stream(ctor.getParameterTypes())
                          .map(this::resolve).toArray();
    T instance = type.cast(ctor.newInstance(args));
    inProgress.remove(type);
    cache.put(type, instance);
    return instance;
}
```

Forty lines, zero dependencies — and now Spring's `@Autowired` is a
*consumer* of ideas you own. Constructor injection keeps the graph honest:
dependencies are visible in the signature, final by default, and impossible
to construct half-baked.
"""
L_DI_VI = """
Một DI container là ba quy tắc đệ quy:

1. **Resolve(type)**: tìm constructor, resolve từng kiểu tham số, rồi khởi tạo.
2. **Memoize**: một instance mỗi kiểu (singleton scope) — nếu không, mỗi lần
   resolve dựng lại toàn bộ đồ thị đối tượng mới.
3. **Phát hiện chu trình**: resolve A cần B cần A — không có tập "đang xử lý",
   đệ quy không bao giờ dừng (bạn nhận `StackOverflowError` trong production,
   lúc 3 giờ sáng).

```java
public <T> T resolve(Class<T> type) {
    if (cache.containsKey(type)) return type.cast(cache.get(type));
    if (!inProgress.add(type)) throw new IllegalStateException("circular dependency: " + type);
    Constructor<?> ctor = type.getDeclaredConstructors()[0];
    Object[] args = Arrays.stream(ctor.getParameterTypes())
                          .map(this::resolve).toArray();
    T instance = type.cast(ctor.newInstance(args));
    inProgress.remove(type);
    cache.put(type, instance);
    return instance;
}
```

Bốn mươi dòng, không phụ thuộc nào — và giờ `@Autowired` của Spring chỉ là
*người tiêu dùng* những ý tưởng bạn sở hữu. Constructor injection giữ đồ thị
trung thực: dependency hiện trong chữ ký, final mặc định, không thể dựng dở
dang.
"""

write_module(
    M, "Reflection & the Mini-DI Container",
    "Class metadata, runtime annotations, and a dependency-injection container built from the JDK alone.",
    "Reflection & Mini-DI Container",
    "Metadata lớp, annotation runtime, và DI container dựng thuần từ JDK.",
    ["javaa-reflect-metadata", "javaa-annotations-runtime", "javaa-di-container"],
    ["javaa-p7-reflect"],
)

write_lesson(M, "javaa-reflect-metadata",
    "Reading class metadata",
    "The getDeclared* family vs the accessible family, and the real costs of reflection.",
    16, L_META_EN,
    "Đọc metadata lớp",
    "Nhóm getDeclared* vs nhóm accessible, và chi phí thật của reflection.",
    L_META_VI)

write_lesson(M, "javaa-annotations-runtime",
    "Runtime annotations",
    "Retention policies, declaring custom annotations, and reading them reflectively — the framework reader pattern.",
    15, L_ANNOT_EN,
    "Annotation runtime",
    "Chính sách retention, khai báo annotation tùy chỉnh, và đọc bằng reflection — mẫu framework reader.",
    L_ANNOT_VI)

write_lesson(M, "javaa-di-container",
    "Build a DI container",
    "Recursive constructor resolution, singleton memoization, and cycle detection in forty lines.",
    20, L_DI_EN,
    "Dựng DI container",
    "Resolve constructor đệ quy, memoize singleton, và phát hiện chu trình trong bốn mươi dòng.",
    L_DI_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_INSPECT = challenge(
    "javaa-p7-inspect",
    "Inventory a class honestly",
    "Inside Solution, define `static class Widget { private int a; private String b; public int c; }` then:\n"
    "1. `static int declaredFieldCount()` — Widget.class.getDeclaredFields().length\n"
    "2. `static int accessibleFieldCount()` — Widget.class.getFields().length\n"
    "3. `static boolean knowsPrivate()` — true iff one of the DECLARED fields is named \"a\"\n"
    "(search by name; do not hardcode an index).\n"
    "4. `static String superName()` — Widget.class.getSuperclass().getName()",
    P_BOILER,
    [
        ("declared sees everything, accessible sees public", r"""
checkEq(Solution.declaredFieldCount(), 3, "getDeclaredFields sees all visibility");
checkEq(Solution.accessibleFieldCount(), 1, "getFields sees only public");
checkTrue(Solution.knowsPrivate(), "private field found by name");
checkEq(Solution.superName(), "java.lang.Object", "default superclass");
""", "The two inventories differ exactly by visibility."),
    ],
    level="guided",
)
CH_INSPECT_VI = vi_challenge(
    "Kê khai lớp một cách trung thực",
    "declaredFieldCount/accessibleFieldCount/knowsPrivate/superName: hai bản kê khai khác nhau đúng theo visibility.",
    [("Declared thấy tất cả, accessible thấy public", "3 field khai báo, 1 field truy cập được."),
     ("Tìm field private theo tên", "Duyệt theo tên, không hardcode vị trí.")],
)

CH_DISPATCH = challenge(
    "javaa-p7-dispatch",
    "Annotation-driven dispatch",
    "Inside Solution:\n"
    "1. Declare `@Retention(RetentionPolicy.RUNTIME) @Target(ElementType.METHOD)\n"
    "public @interface Route { String value(); }`\n"
    "2. Add three STATIC methods annotated with routes: `@Route(\"/home\") static String serveHome()`,\n"
    "`@Route(\"/about\") static String serveAbout()`, `@Route(\"/help\") static String serveHelp()`\n"
    "returning \"home-page\", \"about-page\", \"help-page\" respectively. (Method names deliberately\n"
    "differ from the route paths — the mapping must come from the annotation.)\n"
    "3. `static Map<String, String> routeTable()` — reflect over getDeclaredMethods, map\n"
    "each @Route value to the METHOD NAME that carries it.\n"
    "4. `static String dispatch(String path, String body)` — look up the handler method\n"
    "name for path in routeTable(); if found, invoke it reflectively (it's static, no\n"
    "receiver) and return the result; if unknown, return exactly \"404\". The body arg is\n"
    "unused (routes take no input) — keep it for signature stability.",
    P_BOILER,
    [
        ("routes come from annotations, not method names", r"""
java.util.Map<String, String> t = Solution.routeTable();
checkEq(t.get("/home"), "serveHome", "annotation value maps to method name");
checkEq(t.get("/about"), "serveAbout", "second route");
checkEq(Solution.dispatch("/home", ""), "home-page", "reflective invocation works");
checkEq(Solution.dispatch("/nope", ""), "404", "unknown path handled");
""", "The reader pattern: scan, map, invoke."),
    ],
    level="independent",
)
CH_DISPATCH_VI = vi_challenge(
    "Định tuyến theo annotation",
    "routeTable/dispatch: quét getDeclaredMethods, map giá trị @Route sang tên method, invoke reflective, 404 cho đường lạ.",
    [("Route đến từ annotation, không phải tên method", "Giá trị @Route ánh xạ sang tên method."),
     ("Invoke reflective hoạt động", "Method static, không cần receiver.")],
)

CH_CONTAINER = challenge(
    "javaa-p7-container-core",
    "The container core",
    "Inside Solution, write `public static class Container`:\n"
    "1. `public <T> T resolve(Class<T> type)` — recursive constructor injection: pick the\n"
    "first declared constructor, resolve EVERY parameter type the same way, instantiate\n"
    "with `ctor.newInstance(...)`, cast back via `type.cast(...)`.\n"
    "2. Singleton scope: resolving the same type twice returns the SAME instance (cache\n"
    "by Class token — Module 6's heterogeneous map).\n"
    "3. Cycle detection: if resolution of A reaches A again, throw\n"
    "`IllegalStateException` with a message containing \"circular\".\n"
    "Supports: nested classes you define are resolved through their constructors.",
    P_BOILER,
    [
        ("recursive construction", r"""
Solution.Container c = new Solution.Container();
Solution.Service s = c.resolve(Solution.Service.class);
checkTrue(s.repo != null, "dependency injected");
checkTrue(c.resolve(Solution.Facade.class).svc.repo != null, "two-level graph");
""", "Params resolved depth-first."),
        ("singleton identity", r"""
Solution.Container c = new Solution.Container();
checkTrue(c.resolve(Solution.Repo.class) == c.resolve(Solution.Repo.class), "same instance");
checkTrue(c.resolve(Solution.Facade.class).svc == c.resolve(Solution.Service.class), "graph shares one Service");
""", "One object graph per container."),
        ("cycle detected, not a stack overflow", r"""
Solution.Container c = new Solution.Container();
try {
    c.resolve(Solution.CycleA.class);
    checkTrue(false, "must throw");
} catch (IllegalStateException e) {
    checkTrue(e.getMessage().contains("circular"), "message says circular: " + e.getMessage());
}
""", "In-progress set ends the recursion with a real diagnostic."),
    ],
    level="real-world",
)
CH_CONTAINER_VI = vi_challenge(
    "Lõi container",
    "resolve: inject constructor đệ quy, singleton theo Class token, phát hiện chu trình với thông điệp circular.",
    [("Dựng đệ quy", "Tham số được resolve chiều sâu trước."),
     ("Singleton identity", "Một đồ thị đối tượng mỗi container."),
     ("Chu trình bị bắt, không phải stack overflow", "Tập in-progress kết thúc đệ quy bằng diagnostic thật.")],
)

write_practice(M, "javaa-p7-reflect",
    "Reflection & DI drills",
    "Inventory classes, drive behavior from annotations, and wire an object graph by hand.",
    "Bài tập reflection & DI",
    "Kê khai lớp, điều khiển hành vi từ annotation, và tự tay nối đồ thị đối tượng.",
    "javaa-di-container", 60, "advanced",
    [CH_INSPECT, CH_DISPATCH, CH_CONTAINER],
    {"javaa-p7-inspect": CH_INSPECT_VI, "javaa-p7-dispatch": CH_DISPATCH_VI, "javaa-p7-container-core": CH_CONTAINER_VI},
    solutions=[
        ("javaa-p7-inspect", r"""
import java.lang.reflect.*;

public class Solution {
    static class Widget {
        private int a;
        private String b;
        public int c;
    }

    public static int declaredFieldCount() {
        return Widget.class.getDeclaredFields().length;
    }

    public static int accessibleFieldCount() {
        return Widget.class.getFields().length;
    }

    public static boolean knowsPrivate() {
        for (Field f : Widget.class.getDeclaredFields()) {
            if (f.getName().equals("a")) return true;
        }
        return false;
    }

    public static String superName() {
        return Widget.class.getSuperclass().getName();
    }
}
""", r"""
import java.lang.reflect.*;

public class Solution {
    static class Widget {
        private int a;
        private String b;
        public int c;
    }

    public static int declaredFieldCount() {
        return Widget.class.getFields().length;       // WRONG: accessible inventory, not declared
    }

    public static int accessibleFieldCount() {
        return Widget.class.getDeclaredFields().length;  // WRONG: swapped
    }

    public static boolean knowsPrivate() {
        for (Field f : Widget.class.getFields()) {    // WRONG: searches the wrong inventory
            if (f.getName().equals("a")) return true;
        }
        return false;
    }

    public static String superName() {
        return Widget.class.getName();                 // WRONG: self, not superclass
    }
}
"""),
        ("javaa-p7-dispatch", r"""
import java.lang.annotation.*;
import java.lang.reflect.*;
import java.util.*;

public class Solution {
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.METHOD)
    public @interface Route { String value(); }

    @Route("/home")
    public static String serveHome() { return "home-page"; }

    @Route("/about")
    public static String serveAbout() { return "about-page"; }

    @Route("/help")
    public static String serveHelp() { return "help-page"; }

    public static Map<String, String> routeTable() {
        Map<String, String> table = new HashMap<>();
        for (Method m : Solution.class.getDeclaredMethods()) {
            Route r = m.getAnnotation(Route.class);
            if (r != null) table.put(r.value(), m.getName());
        }
        return table;
    }

    public static String dispatch(String path, String body) {
        String name = routeTable().get(path);
        if (name == null) return "404";
        try {
            Method m = Solution.class.getDeclaredMethod(name);
            return (String) m.invoke(null);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException(e);
        }
    }
}
""", r"""
import java.lang.annotation.*;
import java.lang.reflect.*;
import java.util.*;

public class Solution {
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.METHOD)
    public @interface Route { String value(); }

    @Route("/home")
    public static String serveHome() { return "home-page"; }

    @Route("/about")
    public static String serveAbout() { return "about-page"; }

    @Route("/help")
    public static String serveHelp() { return "help-page"; }

    public static Map<String, String> routeTable() {
        Map<String, String> table = new HashMap<>();
        for (Method m : Solution.class.getDeclaredMethods()) {
            if (m.getParameterCount() == 0 && m.getReturnType() == String.class) {
                table.put("/" + m.getName(), m.getName());   // WRONG: name-derived keys — /home maps to /serveHome
            }
        }
        return table;
    }

    public static String dispatch(String path, String body) {
        String name = routeTable().get(path);
        if (name == null) return "404";
        try {
            Method m = Solution.class.getDeclaredMethod(name);
            return (String) m.invoke(null);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException(e);
        }
    }
}
"""),
        ("javaa-p7-container-core", r"""
import java.lang.reflect.*;
import java.util.*;

public class Solution {
    public static class Repo {
        public String name() { return "repo"; }
    }

    public static class Service {
        public final Repo repo;
        public Service(Repo repo) { this.repo = repo; }
    }

    public static class Facade {
        public final Service svc;
        public Facade(Service svc) { this.svc = svc; }
    }

    public static class CycleA {
        public CycleA(CycleB b) { }
    }

    public static class CycleB {
        public CycleB(CycleA a) { }
    }

    public static class Container {
        private final Map<Class<?>, Object> cache = new HashMap<>();
        private final Set<Class<?>> inProgress = new HashSet<>();

        @SuppressWarnings("unchecked")
        public <T> T resolve(Class<T> type) {
            Object cached = cache.get(type);
            if (cached != null) return type.cast(cached);
            if (!inProgress.add(type)) {
                throw new IllegalStateException("circular dependency resolving " + type.getName());
            }
            try {
                Constructor<?> ctor = type.getDeclaredConstructors()[0];
                ctor.setAccessible(true);
                Class<?>[] params = ctor.getParameterTypes();
                Object[] args = new Object[params.length];
                for (int i = 0; i < params.length; i++) {
                    args[i] = resolve(params[i]);
                }
                T instance = type.cast(ctor.newInstance(args));
                cache.put(type, instance);
                return instance;
            } catch (ReflectiveOperationException e) {
                throw new IllegalStateException("cannot construct " + type.getName(), e);
            } finally {
                inProgress.remove(type);
            }
        }
    }
}
""", r"""
import java.lang.reflect.*;
import java.util.*;

public class Solution {
    public static class Repo {
        public String name() { return "repo"; }
    }

    public static class Service {
        public final Repo repo;
        public Service(Repo repo) { this.repo = repo; }
    }

    public static class Facade {
        public final Service svc;
        public Facade(Service svc) { this.svc = svc; }
    }

    public static class CycleA {
        public CycleA(CycleB b) { }
    }

    public static class CycleB {
        public CycleB(CycleA a) { }
    }

    public static class Container {
        private final Map<Class<?>, Object> cache = new HashMap<>();

        @SuppressWarnings("unchecked")
        public <T> T resolve(Class<T> type) {
            Object cached = cache.get(type);
            if (cached != null) return type.cast(cached);
            Constructor<?> ctor = type.getDeclaredConstructors()[0];
            ctor.setAccessible(true);
            Class<?>[] params = ctor.getParameterTypes();
            Object[] args = new Object[params.length];
            for (int i = 0; i < params.length; i++) {
                args[i] = resolve(params[i]);   // WRONG: no in-progress set — A→B→A recurses forever
            }
            T instance = type.cast(ctor.newInstance());
            cache.put(type, instance);
            return instance;
        }
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the mini DI container, complete

Everything from the practice set plus one production-shaped rule: the
container reports *missing* dependencies with a real exception instead of
building half an object graph. After this checkpoint, reflection is no longer
magic — it is a tool you have shipped.
"""

CP_CH = challenge(
    "javaa-checkpoint-m7-task",
    "Checkpoint: full container",
    "Extend the practice Container (copy it in) with:\n"
    "1. Everything from before: recursive constructor injection, singleton cache by\n"
    "Class token, cycle detection throwing IllegalStateException(\"...circular...\").\n"
    "2. `public <T> boolean canResolve(Class<T> type)` — true iff resolve(type) would\n"
    "succeed: every constructor parameter type must itself be resolvable (primitive or\n"
    "array parameter types cannot be injected -> false), and there must be no cycle\n"
    "reachable from type. MUST NOT throw for unresolvable types — answer the question.\n"
    "canResolve must never mutate the singleton cache for types it merely inspects.\n"
    "3. `public int constructions` on the CONTAINER (public field) — incremented for every\n"
    "constructor invocation the container performs. (Lets tests distinguish real\n"
    "construction from mere inspection.)",
    P_BOILER,
    [
        ("graph resolves and shares instances", r"""
Solution.Container c = new Solution.Container();
Solution.Facade f = c.resolve(Solution.Facade.class);
checkTrue(f.svc.repo != null, "two-level injection");
checkTrue(c.resolve(Solution.Service.class) == f.svc, "singleton shared with graph");
""", "Recursive injection + memoization."),
        ("cycles answer, not crash", r"""
Solution.Container c = new Solution.Container();
try { c.resolve(Solution.CycleA.class); checkTrue(false, "resolve must throw"); }
catch (IllegalStateException e) { checkTrue(e.getMessage().contains("circular"), "diagnostic"); }
checkTrue(!c.canResolve(Solution.CycleA.class), "cycle reported via canResolve");
""", "Both APIs agree on the cycle."),
        ("unresolvable types answered honestly", r"""
Solution.Container c = new Solution.Container();
checkTrue(c.canResolve(Solution.Repo.class), "plain class resolvable");
checkEq(c.constructions, 0, "canResolve NEVER constructs");
checkTrue(!c.canResolve(int.class), "primitives cannot be injected");
checkTrue(!c.canResolve(String[].class), "arrays cannot be injected");
checkEq(c.constructions, 0, "still zero constructions after failed probes");
checkTrue(c.resolve(Solution.Repo.class) != null, "resolve DOES construct");
checkEq(c.constructions, 1, "exactly one construction");
""", "Inspection without construction — counted."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: container hoàn chỉnh",
    "Container đầy đủ: inject đệ quy, singleton, chu trình qua cả resolve lẫn canResolve, trả lời trung thực cho kiểu không thể inject.",
    [("Đồ thị resolve và chia sẻ instance", "Inject hai tầng + memoization."),
     ("Chu trình trả lời, không crash", "resolve ném, canResolve báo false."),
     ("Kiểu không inject được được trả lời trung thực", "Inspect không dựng.")],
)

write_checkpoint(M, "javaa-checkpoint-m7",
    "Checkpoint: The Complete Mini-DI Container",
    "Recursive injection, singletons, cycle diagnostics, and honest capability queries.",
    30, CP_MD,
    "Checkpoint: Mini-DI Container hoàn chỉnh",
    "Inject đệ quy, singleton, chẩn đoán chu trình, và truy vấn năng lực trung thực.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.lang.reflect.*;
import java.util.*;

public class Solution {
    public static class Repo {
        public String name() { return "repo"; }
    }

    public static class Service {
        public final Repo repo;
        public Service(Repo repo) { this.repo = repo; }
    }

    public static class Facade {
        public final Service svc;
        public Facade(Service svc) { this.svc = svc; }
    }

    public static class CycleA {
        public CycleA(CycleB b) { }
    }

    public static class CycleB {
        public CycleB(CycleA a) { }
    }

    public static class Container {
        private final Map<Class<?>, Object> cache = new HashMap<>();
        private final Set<Class<?>> inProgress = new HashSet<>();
        public int constructions = 0;

        @SuppressWarnings("unchecked")
        public <T> T resolve(Class<T> type) {
            Object cached = cache.get(type);
            if (cached != null) return type.cast(cached);
            if (!inProgress.add(type)) {
                throw new IllegalStateException("circular dependency resolving " + type.getName());
            }
            try {
                Constructor<?> ctor = type.getDeclaredConstructors()[0];
                ctor.setAccessible(true);
                Object[] args = new Object[ctor.getParameterTypes().length];
                for (int i = 0; i < args.length; i++) {
                    args[i] = resolve(ctor.getParameterTypes()[i]);
                }
                constructions++;
                T instance = type.cast(ctor.newInstance(args));
                cache.put(type, instance);
                return instance;
            } catch (ReflectiveOperationException e) {
                throw new IllegalStateException("cannot construct " + type.getName(), e);
            } finally {
                inProgress.remove(type);
            }
        }

        public <T> boolean canResolve(Class<T> type) {
            if (type.isPrimitive() || type.isArray()) return false;
            Set<Class<?>> seen = new HashSet<>();
            return inspect(type, seen);
        }

        private boolean inspect(Class<?> type, Set<Class<?>> seen) {
            if (type.isPrimitive() || type.isArray()) return false;
            if (!seen.add(type)) return false;   // cycle reachable
            Constructor<?> ctor = type.getDeclaredConstructors()[0];
            for (Class<?> p : ctor.getParameterTypes()) {
                if (cache.containsKey(p)) continue;   // already built — resolvable
                if (!inspect(p, seen)) return false;
            }
            return true;
        }
    }
}
""", wrong=r"""
import java.lang.reflect.*;
import java.util.*;

public class Solution {
    public static class Repo {
        public String name() { return "repo"; }
    }

    public static class Service {
        public final Repo repo;
        public Service(Repo repo) { this.repo = repo; }
    }

    public static class Facade {
        public final Service svc;
        public Facade(Service svc) { this.svc = svc; }
    }

    public static class CycleA {
        public CycleA(CycleB b) { }
    }

    public static class CycleB {
        public CycleB(CycleA a) { }
    }

    public static class Container {
        private final Map<Class<?>, Object> cache = new HashMap<>();
        private final Set<Class<?>> inProgress = new HashSet<>();
        public int constructions = 0;

        @SuppressWarnings("unchecked")
        public <T> T resolve(Class<T> type) {
            Object cached = cache.get(type);
            if (cached != null) return type.cast(cached);
            if (!inProgress.add(type)) {
                throw new IllegalStateException("circular dependency resolving " + type.getName());
            }
            try {
                Constructor<?> ctor = type.getDeclaredConstructors()[0];
                ctor.setAccessible(true);
                Object[] args = new Object[ctor.getParameterTypes().length];
                for (int i = 0; i < args.length; i++) {
                    args[i] = resolve(ctor.getParameterTypes()[i]);
                }
                constructions++;
                T instance = type.cast(ctor.newInstance(args));
                cache.put(type, instance);
                return instance;
            } catch (ReflectiveOperationException e) {
                throw new IllegalStateException("cannot construct " + type.getName(), e);
            } finally {
                inProgress.remove(type);
            }
        }

        public <T> boolean canResolve(Class<T> type) {
            try {
                resolve(type);      // WRONG: actually builds — constructions must stay 0 during
                return true;        // inspection, and this pollutes the singleton cache
            } catch (RuntimeException e) {
                return false;
            }
        }
    }
}
""")

print("module 7 authored")
