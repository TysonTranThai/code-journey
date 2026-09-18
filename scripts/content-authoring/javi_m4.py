#!/usr/bin/env python3
"""Java — Intermediate — Module 4: java-collections-advanced.

Beyond the big three: Comparable/Comparator composition, sorted structures,
deque/queue usage, and unmodifiable views vs truly immutable copies. House
conventions: Solution-qualified refs, explicit CjTestBase messages,
behavioral Ws.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-collections-advanced"

# ── lesson 4.1 — ordering ───────────────────────────────────────────────────
L_ORDER_EN = r"""
## Ordering: Comparable and Comparator

`Comparable<T>` is the *natural* order — the object itself decides:

```java
record Weight(int grams) implements Comparable<Weight> {
    public int compareTo(Weight o) { return Integer.compare(grams, o.grams); }
}
```

`Comparator<T>` is an *external, swappable* order:

```java
Comparator<Employee> bySalary = Comparator.comparingInt(Employee::salary);
Comparator<Employee> bySalaryDesc = bySalary.reversed();
Comparator<Employee> byDeptThenSalary =
    Comparator.comparing(Employee::dept).thenComparingInt(Employee::salary);
```

Rules of the road:
- compare(a,b) < 0, 0, or > 0 — sign is the only thing that matters
- comparator must be *consistent with equals* if used in sorted sets/maps,
  or you get duplicate-looking entries
- `Comparator.comparing(keyExtractor)` beats hand-written lambdas for
  readability and null-handling (`nullsFirst`, `nullsLast`)

Sorting with streams (`sorted(cmp)`) and `Collections.sort` share these
interfaces.
"""

L_ORDER_VI = r"""
## Thứ tự: Comparable và Comparator

`Comparable<T>` là thứ tự *tự nhiên* — chính đối tượng quyết định:

```java
record Weight(int grams) implements Comparable<Weight> {
    public int compareTo(Weight o) { return Integer.compare(grams, o.grams); }
}
```

`Comparator<T>` là thứ tự *bên ngoài, hoán đổi được*:

```java
Comparator<Employee> bySalary = Comparator.comparingInt(Employee::salary);
Comparator<Employee> bySalaryDesc = bySalary.reversed();
Comparator<Employee> byDeptThenSalary =
    Comparator.comparing(Employee::dept).thenComparingInt(Employee::salary);
```

Quy tắc:
- compare(a,b) < 0, 0, hoặc > 0 — chỉ dấu là quan trọng
- comparator phải *nhất quán với equals* nếu dùng trong set/map có thứ tự,
  nếu không bạn sẽ thấy các entry "trùng lặp" giả tạo
- `Comparator.comparing(keyExtractor)` dễ đọc hơn lambda tự viết, và xử
  lý null rõ ràng (`nullsFirst`, `nullsLast`)

Sắp xếp bằng stream (`sorted(cmp)`) và `Collections.sort` dùng chung các
interface này.
"""

# ── lesson 4.2 — queues, deques, priority ──────────────────────────────────
L_DEQUE_EN = r"""
## Queue, Deque, PriorityQueue

`ArrayDeque` is Java's best stack AND queue — faster than the legacy
`Stack` class and `LinkedList`:

```java
Deque<String> stack = new ArrayDeque<>();
stack.push("a");          // addFirst
stack.pop();              // removeFirst — LIFO

Deque<String> queue = new ArrayDeque<>();
queue.offer("a");         // addLast
queue.poll();             // removeFirst — FIFO
```

Two method flavors exist for a reason:
- `add/push/offer` throw or lie differently on capacity failure
- `element/peek` vs `remove/poll`: the first pair *throws* when empty,
  the second returns null — choose explicitly, don't mix casually.

`PriorityQueue` is a heap: `poll()` always yields the smallest element
*according to its comparator*, not insertion order:

```java
PriorityQueue<Task> q = new PriorityQueue<>(Comparator.comparingInt(Task::priority));
```

O(log n) insert/poll — the tool for "always process the most urgent next".
"""

L_DEQUE_VI = r"""
## Queue, Deque, PriorityQueue

`ArrayDeque` là stack VÀ queue tốt nhất của Java — nhanh hơn `Stack` cổ
điển và `LinkedList`:

```java
Deque<String> stack = new ArrayDeque<>();
stack.push("a");          // addFirst
stack.pop();              // removeFirst — LIFO

Deque<String> queue = new ArrayDeque<>();
queue.offer("a");         // addLast
queue.poll();             // removeFirst — FIFO
```

Có hai kiểu method là có chủ đích:
- `add/push/offer` ném ngoại lệ hoặc trả báo hiệu khác nhau khi hết chỗ
- `element/peek` so với `remove/poll`: cặp đầu *ném* khi rỗng, cặp sau
  trả null — chọn rõ ràng, đừng trộn tùy hứng.

`PriorityQueue` là một heap: `poll()` luôn cho phần tử nhỏ nhất *theo
comparator của nó*, không phải theo thứ tự chèn:

```java
PriorityQueue<Task> q = new PriorityQueue<>(Comparator.comparingInt(Task::priority));
```

O(log n) cho insert/poll — công cụ cho kiểu "luôn xử lý việc cấp bách
nhất trước".
"""

# ── lesson 4.3 — immutability of collections ────────────────────────────────
L_IMMUTC_EN = r"""
## Unmodifiable views vs immutable copies

Three different "cannot change" guarantees:

```java
List<String> src = new ArrayList<>(List.of("a", "b"));

List<String> view = Collections.unmodifiableList(src);
// view.set(0, "x") throws — but src.set(0, "x") changes the view too!

List<String> copy = List.copyOf(src);
// copy is independent: mutating src cannot reach it

List<String> literal = List.of("a", "b");
// immutable since birth, no copy cost, rejects nulls
```

`List.of`/`Set.of`/`Map.of` are the default for constants. `List.copyOf`
is the tool for sealing *caller-provided* collections. Unmodifiable views
are for *controlled exposure* — the owner keeps mutability, the caller
doesn't get it.

`Arrays.asList` is a trap: fixed-size but writable — `set` works, `add`
throws. Rarely what you mean.
"""

L_IMMUTC_VI = r"""
## View không thể sửa so với bản sao bất biến

Ba mức bảo đảm "không thể thay đổi" khác nhau:

```java
List<String> src = new ArrayList<>(List.of("a", "b"));

List<String> view = Collections.unmodifiableList(src);
// view.set(0, "x") ném ngoại lệ — nhưng src.set(0, "x") đổi cả view!

List<String> copy = List.copyOf(src);
// copy độc lập: sửa src không chạm tới được nó

List<String> literal = List.of("a", "b");
// bất biến từ khi sinh ra, không tốn chi phí copy, chặn null
```

`List.of`/`Set.of`/`Map.of` là mặc định cho hằng số. `List.copyOf` là
công cụ để niêm phong collection *do caller cung cấp*. View không thể sửa
dùng để *kiểm soát việc lộ ra ngoài* — chủ sở hữu vẫn giữ khả năng sửa,
caller thì không.

`Arrays.asList` là bẫy: kích thước cố định nhưng ghi được — `set` chạy,
`add` ném. Hiếm khi là điều bạn muốn.
"""

write_module(
    MOD,
    "Collections & Data Structures in Depth",
    "Comparator composition, sorted structures, deques and priority queues, and the three levels of collection immutability.",
    "Collection & cấu trúc dữ liệu chuyên sâu",
    "Soi comporator, cấu trúc có thứ tự, deque và priority queue, và ba mức bất biến của collection.",
    ["comparator-composition", "deques-priority-queues", "collection-immutability", "javi-checkpoint-collections"],
    ["javi-p4-collections"],
)

write_lesson(MOD, "comparator-composition", "Comparable & Comparator", "Natural order vs external order, comparator chaining with thenComparing, and consistency with equals in sorted collections.", 14, L_ORDER_EN, "Comparable & Comparator", "Thứ tự tự nhiên so với thứ tự ngoài, chuỗi comparator với thenComparing, và tính nhất quán với equals trong collection có thứ tự.", L_ORDER_VI)

write_lesson(MOD, "deques-priority-queues", "Queues, Deques & Priority Queues", "ArrayDeque as stack and queue, the throw-or-null method flavors, and heap-backed PriorityQueue semantics.", 13, L_DEQUE_EN, "Queue, Deque & Priority Queue", "ArrayDeque làm stack và queue, hai kiểu method ném-hoặc-null, và ngữ nghĩa PriorityQueue dựa trên heap.", L_DEQUE_VI)

write_lesson(MOD, "collection-immutability", "Unmodifiable Views vs Immutable Copies", "The difference between a read-only view and an independent copy — and the Arrays.asList trap.", 12, L_IMMUTC_EN, "View không thể sửa so với bản sao bất biến", "Khác nhau giữa view chỉ đọc và bản sao độc lập — và bẫy Arrays.asList.", L_IMMUTC_VI)

# ── practice set ─────────────────────────────────────────────────────────────
P4_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P4_EMPLOYEES = challenge(
    "javi-p4-sort-employees",
    "Compose Comparators",
    r"""Work with records inside `Solution`:
- `record Employee(String name, String dept, int salary)`
- `static List<String> topPaidByDept(List<Employee> staff, int n)`:
  group employees by dept, sort each group by salary DESCENDING (ties by
  name ASCENDING), and return `dept + ":" + name` for the top n of each
  group, with depts in alphabetical order.

Use Comparator.comparing/thenComparing — no anonymous classes.""",
    P4_BOILER,
    [
        (
            "groups sorted, salaries descending",
            r"""
List<Object> staff = List.of(
    new Solution.Employee("ann", "eng", 120),
    new Solution.Employee("bob", "ops", 90),
    new Solution.Employee("cid", "eng", 150),
    new Solution.Employee("dee", "eng", 150));
List<String> out = Solution.topPaidByDept((List) staff, 1);
checkEq(out, List.of("eng:cid", "ops:bob"), "top1 per dept");
""",
            "eng's top is cid or dee — the tie must break by name ascending → cid.",
        ),
        (
            "tie-break by name",
            r"""
List<Object> staff = List.of(
    new Solution.Employee("ann", "eng", 120),
    new Solution.Employee("cid", "eng", 150),
    new Solution.Employee("dee", "eng", 150));
List<String> out = Solution.topPaidByDept((List) staff, 2);
checkEq(out, List.of("eng:cid", "eng:dee"), "tie by name asc");
""",
            "Equal salaries → name ascending.",
        ),
    ],
    level="independent",
)

CH_P4_PRIORITY = challenge(
    "javi-p4-task-queue",
    "Urgency Queue with a Heap",
    r"""Simulate task scheduling with a priority queue:
- `record Task(String name, int priority)` in `Solution`
- `static List<String> processTasks(List<Task> tasks, int slots)`:
  put all tasks into a `PriorityQueue` ordered by priority ASCENDING
  (1 = most urgent), then poll up to `slots` tasks and return their
  names in processing order.

Same priority → FIFO among equals (use a sequence tiebreaker in the
comparator).""",
    P4_BOILER,
    [
        (
            "most urgent first",
            r"""
List<Object> tasks = List.of(
    new Solution.Task("email", 5), new Solution.Task("fire", 1),
    new Solution.Task("build", 3));
List<String> out = Solution.processTasks((List) tasks, 2);
checkEq(out, List.of("fire", "build"), "urgency order");
""",
            "Priority 1 first, then 3 — regardless of insertion order.",
        ),
        (
            "FIFO among equal priorities",
            r"""
List<Object> tasks = List.of(
    new Solution.Task("a", 2), new Solution.Task("b", 2), new Solution.Task("c", 2));
List<String> out = Solution.processTasks((List) tasks, 3);
checkEq(out, List.of("a", "b", "c"), "stable among equals");
""",
            "Tiebreak by insertion sequence: comparator compares priority, then index.",
        ),
        (
            "slots caps the output",
            r"""
List<Object> tasks = List.of(new Solution.Task("a", 1), new Solution.Task("b", 2));
List<String> out = Solution.processTasks((List) tasks, 1);
checkEq(out, List.of("a"), "only one slot");
""",
            "Poll at most `slots` tasks.",
        ),
    ],
    level="guided",
)

CH_P4_VIEWS = challenge(
    "javi-p4-seal-registry",
    "Seal the Registry",
    r"""`Registry` keeps a mutable index but exposes it safely.
Implement in `Solution`:
- `static class Registry` with `put(String k, int v)`,
  `int get(String k)` (missing → throw NoSuchElementException),
  `Map<String, Integer> snapshot()` (unmodifiable view),
  and `Map<String, Integer> frozenCopy()` (independent immutable copy).
- `static int totalOf(Map<String, Integer> values)` summing the values —
  it must compile against either of the two exposure styles.

The test mutates the registry after taking a snapshot to prove the copy
stays independent.""",
    P4_BOILER,
    [
        (
            "snapshot reflects live state",
            r"""
Solution.Registry r = new Solution.Registry();
r.put("a", 1);
checkEq(r.snapshot(), Map.of("a", 1), "live view");
""",
            "snapshot() returns an unmodifiable view of the live map.",
        ),
        (
            "frozenCopy independent of later writes",
            r"""
Solution.Registry r = new Solution.Registry();
r.put("a", 1);
Map<String, Integer> copy = r.frozenCopy();
r.put("b", 2);
checkEq(copy, Map.of("a", 1), "copy frozen");
checkEq(r.snapshot(), Map.of("a", 1, "b", 2), "registry moved on");
""",
            "frozenCopy() must be Map.copyOf(...) — later puts cannot reach it.",
        ),
        (
            "missing key throws",
            r"""
Solution.Registry r = new Solution.Registry();
try { r.get("nope"); checkTrue(false, "must throw"); }
catch (java.util.NoSuchElementException e) { checkTrue(true, "threw"); }
""",
            "get on a missing key throws NoSuchElementException.",
        ),
        (
            "totalOf sums values",
            r"""
checkEq(Solution.totalOf(Map.of("a", 2, "b", 3)), 5, "sum of values");
""",
            "Iterate values() and add.",
        ),
    ],
    level="independent",
)

VI_CH_P4_EMPLOYEES = vi_challenge(
    "Soi comporator",
    r"""Làm việc với record bên trong `Solution`:
- `record Employee(String name, String dept, int salary)`
- `static List<String> topPaidByDept(List<Employee> staff, int n)`:
  nhóm nhân viên theo dept, sắp mỗi nhóm theo lương GIẢM DẦN (trùng thì
  theo tên TĂNG DẦN), và trả `dept + ":" + name` cho top n của mỗi nhóm,
  các dept theo thứ tự bảng chữ cái.

Dùng Comparator.comparing/thenComparing — không class vô danh.""",
    [
        ("Nhóm có thứ tự, lương giảm dần", "Top của eng là cid hoặc dee — hòa phải bể theo tên tăng dần → cid."),
        ("Hòa bể theo tên", "Lương bằng nhau → tên tăng dần."),
    ],
)

VI_CH_P4_PRIORITY = vi_challenge(
    "Hàng đợi độ cấp bách với heap",
    r"""Mô phỏng xếp lịch tác vụ bằng priority queue:
- `record Task(String name, int priority)` trong `Solution`
- `static List<String> processTasks(List<Task> tasks, int slots)`:
  đưa mọi task vào `PriorityQueue` sắp theo priority TĂNG DẦN
  (1 = cấp bách nhất), rồi poll tối đa `slots` task và trả tên của chúng
  theo thứ tự xử lý.

Cùng priority → FIFO giữa các phần tử ngang hạng (thêm tiebreaker theo
thứ tự chèn vào comparator).""",
    [
        ("Cấp bách nhất trước", "Priority 1 trước, rồi 3 — bất kể thứ tự chèn."),
        ("FIFO giữa các phần tử ngang hạng", "Tiebreak theo số thứ tự chèn: comparator so priority, rồi index."),
        ("slots chặn số kết quả", "Poll tối đa `slots` task."),
    ],
)

VI_CH_P4_VIEWS = vi_challenge(
    "Niêm phong registry",
    r"""`Registry` giữ chỉ mục khả biến nhưng lộ ra ngoài an toàn.
Cài trong `Solution`:
- `static class Registry` với `put(String k, int v)`,
  `int get(String k)` (thiếu → ném NoSuchElementException),
  `Map<String, Integer> snapshot()` (view không thể sửa),
  và `Map<String, Integer> frozenCopy()` (bản sao bất biến độc lập).
- `static int totalOf(Map<String, Integer> values)` cộng các giá trị —
  phải biên dịch được với cả hai kiểu lộ dữ liệu.

Test sửa registry sau khi lấy snapshot để chứng minh bản sao độc lập.""",
    [
        ("snapshot phản chiếu trạng thái hiện tại", "snapshot() trả view không thể sửa của map sống."),
        ("frozenCopy độc lập với ghi sau đó", "frozenCopy() phải là Map.copyOf(...) — put sau không chạm tới được."),
        ("Key thiếu phải ném", "get với key không tồn tại ném NoSuchElementException."),
        ("totalOf cộng giá trị", "Duyệt values() và cộng."),
    ],
)

write_practice(
    MOD,
    "javi-p4-collections",
    "Collections Lab",
    "Comparator composition, heap scheduling with stable ties, and sealed vs live collection exposure.",
    "Xưởng collection",
    "Soi comporator, xếp lịch bằng heap với tie ổn định, và niêm phong so với lộ collection sống.",
    "collection-immutability",
    40,
    "intermediate",
    [CH_P4_EMPLOYEES, CH_P4_PRIORITY, CH_P4_VIEWS],
    {CH_P4_EMPLOYEES["id"]: VI_CH_P4_EMPLOYEES, CH_P4_PRIORITY["id"]: VI_CH_P4_PRIORITY, CH_P4_VIEWS["id"]: VI_CH_P4_VIEWS},
    solutions=[
        (
            CH_P4_EMPLOYEES["id"],
            r"""
import java.util.*;

public class Solution {
    public record Employee(String name, String dept, int salary) {}

    public static List<String> topPaidByDept(List<Employee> staff, int n) {
        Map<String, List<Employee>> byDept = new TreeMap<>();
        for (Employee e : staff) {
            byDept.computeIfAbsent(e.dept(), k -> new ArrayList<>()).add(e);
        }
        List<String> out = new ArrayList<>();
        Comparator<Employee> rank =
            Comparator.comparingInt(Employee::salary).reversed()
                      .thenComparing(Employee::name);
        for (var entry : byDept.entrySet()) {
            List<Employee> group = entry.getValue();
            group.sort(rank);
            for (int i = 0; i < Math.min(n, group.size()); i++) {
                out.add(entry.getKey() + ":" + group.get(i).name());
            }
        }
        return out;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public record Employee(String name, String dept, int salary) {}

    public static List<String> topPaidByDept(List<Employee> staff, int n) {
        Map<String, List<Employee>> byDept = new TreeMap<>();
        for (Employee e : staff) {
            byDept.computeIfAbsent(e.dept(), k -> new ArrayList<>()).add(e);
        }
        List<String> out = new ArrayList<>();
        // W: forgot .reversed() — picks the LOWEST paid, then ties break
        // by name DESCENDING. Every salary expectation exposes it.
        Comparator<Employee> rank =
            Comparator.comparingInt(Employee::salary)
                      .thenComparing(Employee::name, Comparator.reverseOrder());
        for (var entry : byDept.entrySet()) {
            List<Employee> group = entry.getValue();
            group.sort(rank);
            for (int i = 0; i < Math.min(n, group.size()); i++) {
                out.add(entry.getKey() + ":" + group.get(i).name());
            }
        }
        return out;
    }
}
""",
        ),
        (
            CH_P4_PRIORITY["id"],
            r"""
import java.util.*;

public class Solution {
    public record Task(String name, int priority) {}

    public static List<String> processTasks(List<Task> tasks, int slots) {
        PriorityQueue<Object[]> pq = new PriorityQueue<>(
            (x, y) -> {
                int c = Integer.compare(((Task) x[0]).priority(), ((Task) y[0]).priority());
                return c != 0 ? c : Integer.compare((int) x[1], (int) y[1]);
            });
        int idx = 0;
        for (Task t : tasks) pq.add(new Object[]{t, idx++});
        List<String> out = new ArrayList<>();
        while (!pq.isEmpty() && out.size() < slots) out.add(((Task) pq.poll()[0]).name());
        return out;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public record Task(String name, int priority) {}

    public static List<String> processTasks(List<Task> tasks, int slots) {
        // W: priority DESCENDING — processes 5 before 1. The "most
        // urgent first" expectation fails immediately.
        PriorityQueue<Object[]> pq = new PriorityQueue<>(
            (x, y) -> {
                int c = Integer.compare(((Task) y[0]).priority(), ((Task) x[0]).priority());
                return c != 0 ? c : Integer.compare((int) x[1], (int) y[1]);
            });
        int idx = 0;
        for (Task t : tasks) pq.add(new Object[]{t, idx++});
        List<String> out = new ArrayList<>();
        while (!pq.isEmpty() && out.size() < slots) out.add(((Task) pq.poll()[0]).name());
        return out;
    }
}
""",
        ),
        (
            CH_P4_VIEWS["id"],
            r"""
import java.util.*;

public class Solution {
    public static class Registry {
        private final Map<String, Integer> map = new HashMap<>();
        public void put(String k, int v) { map.put(k, v); }
        public int get(String k) {
            Integer v = map.get(k);
            if (v == null) throw new NoSuchElementException(k);
            return v;
        }
        public Map<String, Integer> snapshot() { return Collections.unmodifiableMap(map); }
        public Map<String, Integer> frozenCopy() { return Map.copyOf(map); }
    }

    public static int totalOf(Map<String, Integer> values) {
        int t = 0;
        for (int v : values.values()) t += v;
        return t;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static class Registry {
        private final Map<String, Integer> map = new HashMap<>();
        public void put(String k, int v) { map.put(k, v); }
        public int get(String k) {
            Integer v = map.get(k);
            if (v == null) throw new NoSuchElementException(k);
            return v;
        }
        // W: "copy" delegates to the live map — a later put() leaks into
        // the frozen copy, exactly the independence the test checks.
        public Map<String, Integer> frozenCopy() { return map; }
        public Map<String, Integer> snapshot() { return Collections.unmodifiableMap(map); }
    }

    public static int totalOf(Map<String, Integer> values) {
        int t = 0;
        for (int v : values.values()) t += v;
        return t;
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — collections

You can now: compose comparators for multi-level ordering, schedule with
heaps, and choose the right exposure (view, copy, or literal) for shared
data. Prove it with a leaderboard.
"""

CP_MDX_VI = r"""
## Checkpoint — collection

Giờ bạn có thể: soi comporator cho thứ tự nhiều mức, xếp lịch bằng heap,
và chọn cách lộ dữ liệu đúng (view, bản sao, hay literal) cho dữ liệu
dùng chung. Chứng minh bằng một bảng xếp hạng.
"""

CH_CP4 = challenge(
    "javi-checkpoint-m4-collections",
    "Leaderboard",
    r"""Build a leaderboard in `Solution`:
- `record Player(String name, int score)` with natural order = score
  DESCENDING, then name ASCENDING (implement Comparable)
- `static List<String> top(List<Player> players, int n)` — the top n
  names per natural order (duplicates in score allowed, name breaks ties)
- `static NavigableSet<Player> ranked(Set<Player> players)` — a TreeSet
  using that same natural order.

Verify the ordering contract: a TreeSet of the players must iterate
highest-score-first, ties alphabetical.""",
    r"""
import java.util.*;

public class Solution {
    // Provide Player + top + ranked here.
}
""",
    [
        (
            "top honors score then name",
            r"""
List<Object> ps = List.of(
    new Solution.Player("zed", 90), new Solution.Player("amy", 95),
    new Solution.Player("max", 95));
List<String> out = Solution.top((List) ps, 2);
checkEq(out, List.of("amy", "max"), "95s alphabetical, then 90");
""",
            "Score descending; ties name ascending.",
        ),
        (
            "TreeSet iterates in natural order",
            r"""
Set<Object> ps = Set.of(
    new Solution.Player("zed", 90), new Solution.Player("amy", 95),
    new Solution.Player("max", 95));
java.util.NavigableSet<?> ranked = Solution.ranked((Set) ps);
List<String> names = new ArrayList<>();
for (Object p : ranked) names.add(((Solution.Player) p).name());
checkEq(names, List.of("amy", "max", "zed"), "sorted iteration");
""",
            "ranked() returns a TreeSet-backed NavigableSet.",
        ),
        (
            "n caps and ordering holds",
            r"""
List<Object> ps = List.of(
    new Solution.Player("a", 1), new Solution.Player("b", 2), new Solution.Player("c", 3));
List<String> out = Solution.top((List) ps, 1);
checkEq(out, List.of("c"), "just the champion");
""",
            "First element under the order.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CH_CP4 = vi_challenge(
    "Bảng xếp hạng",
    r"""Xây bảng xếp hạng trong `Solution`:
- `record Player(String name, int score)` với thứ tự tự nhiên = score
  GIẢM DẦN, rồi tên TĂNG DẦN (cài Comparable)
- `static List<String> top(List<Player> players, int n)` — n tên đầu theo
  thứ tự tự nhiên (score trùng được phép, tên bể hòa)
- `static NavigableSet<Player> ranked(Set<Player> players)` — một TreeSet
  dùng đúng thứ tự tự nhiên đó.

Kiểm chứng hợp đồng thứ tự: TreeSet chứa các player phải duyệt
score-cao-trước, hòa theo bảng chữ cái.""",
    [
        ("top tôn trọng score rồi tên", "Score giảm dần; hòa theo tên tăng dần."),
        ("TreeSet duyệt theo thứ tự tự nhiên", "ranked() trả NavigableSet dựng trên TreeSet."),
        ("n chặn và thứ tự giữ vững", "Phần tử đầu theo thứ tự."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-collections",
    "Checkpoint: Collections",
    "Graded checkpoint: a Comparable leaderboard with a TreeSet-backed ranked view.",
    15,
    CP_MDX,
    "Checkpoint: Collection",
    "Checkpoint chấm điểm: bảng xếp hạng Comparable với view ranked dựng trên TreeSet.",
    CP_MDX_VI,
    CH_CP4,
    VI_CH_CP4,
    solution=r"""
import java.util.*;

public class Solution {
    public record Player(String name, int score) implements Comparable<Player> {
        @Override public int compareTo(Player o) {
            int c = Integer.compare(o.score(), this.score());
            return c != 0 ? c : this.name().compareTo(o.name());
        }
    }

    public static List<String> top(List<Player> players, int n) {
        List<Player> sorted = new ArrayList<>(players);
        Collections.sort(sorted);
        List<String> out = new ArrayList<>();
        for (int i = 0; i < Math.min(n, sorted.size()); i++) out.add(sorted.get(i).name());
        return out;
    }

    public static NavigableSet<Player> ranked(Set<Player> players) {
        return new TreeSet<>(players);
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public record Player(String name, int score) implements Comparable<Player> {
        @Override public int compareTo(Player o) {
            // W: ascending score — the leaderboard ranks the WORST first.
            int c = Integer.compare(this.score(), o.score());
            return c != 0 ? c : this.name().compareTo(o.name());
        }
    }

    public static List<String> top(List<Player> players, int n) {
        List<Player> sorted = new ArrayList<>(players);
        Collections.sort(sorted);
        List<String> out = new ArrayList<>();
        for (int i = 0; i < Math.min(n, sorted.size()); i++) out.add(sorted.get(i).name());
        return out;
    }

    public static NavigableSet<Player> ranked(Set<Player> players) {
        return new TreeSet<>(players);
    }
}
""",
)
