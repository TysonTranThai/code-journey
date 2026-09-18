#!/usr/bin/env python3
"""Java — Intermediate — Module 5: java-functional-deep.

Collectors depth (groupingBy/partitioningBy/toMap/teeing), functional
composition, and the judgment call: when a stream beats a loop and when it
doesn't. House conventions: Solution-qualified refs, explicit CjTestBase
messages, behavioral Ws.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-functional-deep"

# ── lesson 5.1 — collectors that reshape data ───────────────────────────────
L_COLLECTORS_EN = r"""
## Collectors: reshaping data in one pass

Beginner streams end at `collect(toList())`. The real power is reshaping:

```java
// group orders by customer
Map<String, List<Order>> byCustomer =
    orders.stream().collect(Collectors.groupingBy(Order::customer));

// count per group — groupingBy + counting downstream
Map<String, Long> counts =
    words.stream().collect(Collectors.groupingBy(w -> w, Collectors.counting()));

// partition into two buckets by a predicate
Map<Boolean, List<Integer>> parts =
    nums.stream().collect(Collectors.partitioningBy(n -> n % 2 == 0));

// toMap with a merge function (duplicate keys otherwise explode)
Map<String, Integer> merged =
    sales.stream().collect(Collectors.toMap(
        Sale::region, Sale::amount, Integer::sum));
```

`teeing` runs two collectors at once and merges their results — perfect
for "average and max" style passes over one stream.
"""

L_COLLECTORS_VI = r"""
## Collectors: biến đổi dữ liệu trong một lượt

Stream trình độ mới kết thúc ở `collect(toList())`. Sức mạnh thật nằm ở
việc biến đổi hình dạng dữ liệu:

```java
// nhóm đơn theo khách
Map<String, List<Order>> byCustomer =
    orders.stream().collect(Collectors.groupingBy(Order::customer));

// đếm theo nhóm — groupingBy + counting downstream
Map<String, Long> counts =
    words.stream().collect(Collectors.groupingBy(w -> w, Collectors.counting()));

// chia làm hai nhóm theo predicate
Map<Boolean, List<Integer>> parts =
    nums.stream().collect(Collectors.partitioningBy(n -> n % 2 == 0));

// toMap với merge function (không có thì key trùng sẽ nổ)
Map<String, Integer> merged =
    sales.stream().collect(Collectors.toMap(
        Sale::region, Sale::amount, Integer::sum));
```

`teeing` chạy hai collector cùng lúc rồi trộn kết quả — hoàn hảo cho kiểu
"vừa trung bình vừa lớn nhất" trên một stream.
"""

# ── lesson 5.2 — composition & judgment ────────────────────────────────────
L_JUDGMENT_EN = r"""
## Functional composition — and when NOT to stream

Streams compose: `map` → `filter` → `sorted` → `collect` reads as a
data pipeline. Function types compose too:

```java
Function<String, String> trim = String::trim;
Function<String, String> lower = String::toLowerCase;
Function<String, String> clean = trim.andThen(lower);
```

But the intermediate skill is *judgment*:

**Stream when**: transforming data, grouping, reductions, parallelizable
independent work.

**Loop when**: early exit matters (`break` beats `takeWhile` for
readability), you're updating external state, indices are involved, or
the stream version needs three nested collectors to express one idea.

```java
// clear loop
for (int i = 0; i < xs.size(); i++) {
    if (xs.get(i).matches(q)) return i;   // index + early exit
}
// awkward stream
IntStream.range(0, xs.size()).filter(i -> xs.get(i).matches(q)).findFirst().orElse(-1);
```

The loop is not a failure of style — it's the clearer program here.
"""

L_JUDGMENT_VI = r"""
## Composition hàm — và khi nào KHÔNG nên stream

Stream compose được: `map` → `filter` → `sorted` → `collect` đọc như một
pipeline dữ liệu. Các kiểu hàm cũng compose:

```java
Function<String, String> trim = String::trim;
Function<String, String> lower = String::toLowerCase;
Function<String, String> clean = trim.andThen(lower);
```

Nhưng kỹ năng trung cấp là *sự phán đoán*:

**Dùng stream khi**: biến đổi dữ liệu, nhóm, reduction, công việc độc lập
có thể song song.

**Dùng vòng lặp khi**: cần thoát sớm (`break` dễ đọc hơn `takeWhile`),
đang cập nhật trạng thái bên ngoài, cần index, hoặc bản stream cần ba
collector lồng nhau mới diễn đạt được một ý.

```java
// vòng lặp rõ ràng
for (int i = 0; i < xs.size(); i++) {
    if (xs.get(i).matches(q)) return i;   // index + thoát sớm
}
// bản stream gượng ép
IntStream.range(0, xs.size()).filter(i -> xs.get(i).matches(q)).findFirst().orElse(-1);
```

Vòng lặp không phải lỗi phong cách — nó là chương trình rõ hơn ở đây.
"""

write_module(
    MOD,
    "Functional Java & Collectors",
    "Collectors that reshape data, function composition, and the judgment to know when a plain loop is the better program.",
    "Java hàm & Collectors",
    "Collectors biến đổi dữ liệu, composition hàm, và sự phán đoán biết khi nào vòng lặp thường mới là chương trình tốt hơn.",
    ["collectors-depth", "functional-judgment", "javi-checkpoint-functional"],
    ["javi-p5-functional"],
)

write_lesson(MOD, "collectors-depth", "Collectors in Depth", "groupingBy with downstream collectors, partitioningBy, toMap with merge functions, and teeing for two-at-once reductions.", 15, L_COLLECTORS_EN, "Collectors chuyên sâu", "groupingBy với downstream collector, partitioningBy, toMap với merge function, và teeing cho reduction kép.", L_COLLECTORS_VI)

write_lesson(MOD, "functional-judgment", "Composition & Judgment", "Composing functions and pipelines — and the honest checklist for when a loop is clearer than a stream.", 13, L_JUDGMENT_EN, "Composition & phán đoán", "Soi hàm và pipeline — và checklist thật lòng để biết khi nào vòng lặp rõ hơn stream.", L_JUDGMENT_VI)

# ── practice set ────────────────────────────────────────────────────────────
P5_BOILER = r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    // Implement methods below.
}
"""

CH_P5_WORDS = challenge(
    "javi-p5-word-freq",
    "Frequency Map & Grouping",
    r"""Given `List<String> words`, implement with Collectors (no explicit
loops):
- `static Map<String, Long> frequencies(List<String> words)` — each
  distinct word → how many times it appears (case-SENSITIVE keys).
- `static Map<Integer, List<String>> byLength(List<String> words)` —
  group words by their length.
- `static Map<Boolean, List<String>> longWords(List<String> words)` —
  partition into length > 4 (true) vs rest (false).""",
    P5_BOILER,
    [
        (
            "frequencies count duplicates",
            r"""
checkEq(Solution.frequencies(List.of("a", "b", "a")), Map.of("a", 2L, "b", 1L), "freq");
""",
            "groupingBy(identity, counting()) — returns Long values.",
        ),
        (
            "byLength groups",
            r"""
checkEq(Solution.byLength(List.of("hi", "there", "hey")), Map.of(2, List.of("hi"), 5, List.of("there"), 3, List.of("hey")), "by length");
""",
            "groupingBy(String::length).",
        ),
        (
            "partition by threshold",
            r"""
checkEq(Solution.longWords(List.of("hi", "there")), Map.of(true, List.of("there"), false, List.of("hi")), "partition");
""",
            "partitioningBy(w -> w.length() > 4).",
        ),
    ],
    level="guided",
)

CH_P5_SALES = challenge(
    "javi-p5-sales-merge",
    "toMap with a Merge Function",
    r"""- `record Sale(String region, int amount)` in `Solution`
- `static Map<String, Integer> totalsByRegion(List<Sale> sales)` — sum
  amounts per region using `Collectors.toMap` with `Integer::sum` as the
  merge function.
- `static Map.Entry<String, Integer> topRegion(List<Sale> sales)` —
  returns the region's entry with the highest total (ties: smallest
  region name wins).

Duplicate keys without a merge function throw IllegalStateException —
the tests make sure you used one.""",
    P5_BOILER,
    [
        (
            "totals merge duplicates",
            r"""
List<Object> sales = List.of(
    new Solution.Sale("east", 10), new Solution.Sale("west", 5),
    new Solution.Sale("east", 7));
checkEq(Solution.totalsByRegion((List) sales), Map.of("east", 17, "west", 5), "merged totals");
""",
            "toMap(Sale::region, Sale::amount, Integer::sum).",
        ),
        (
            "top region",
            r"""
List<Object> sales = List.of(
    new Solution.Sale("east", 10), new Solution.Sale("west", 5),
    new Solution.Sale("east", 7));
var top = Solution.topRegion((List) sales);
checkEq(top.getKey(), "east", "winner region");
checkEq(top.getValue(), 17, "winner total");
""",
            "Max entry of the totals map; ties resolved by name.",
        ),
    ],
    level="independent",
)

CH_P5_STATS = challenge(
    "javi-p5-teeing-stats",
    "Two Stats, One Pass",
    r"""Use `Collectors.teeing` (or an equivalent single-pass reduction) on a
list of integers:
- `static double average(List<Integer> xs)` — arithmetic mean; empty
  throws IllegalArgumentException.
- `static Map<String, Integer> rangeStats(List<Integer> xs)` — returns
  `{"min": ..., "max": ...}` computed in one teeing pass.
- `static String classify(List<Integer> xs)` — stream composition drill:
  map each x to x*2, keep only values > 10, join with commas; return the
  joined string (empty list → empty string).""",
    P5_BOILER,
    [
        (
            "average",
            r"""
checkNear(Solution.average(List.of(2, 4, 6)), 4.0, 1e-9, "mean");
""",
            "Sum/count as double.",
        ),
        (
            "min/max in one pass",
            r"""
checkEq(Solution.rangeStats(List.of(3, 9, 1)), Map.of("min", 1, "max", 9), "range");
""",
            "teeing(min, max, Map::entry) or equivalent.",
        ),
        (
            "classify composition",
            r"""
checkEq(Solution.classify(List.of(3, 6, 9, 12)), "12,18,24", "doubled, filtered, joined");
""",
            "3*2=6 (dropped), 6*2=12, 9*2=18, 12*2=24 — join in stream order.",
        ),
        (
            "average rejects empty",
            r"""
try { Solution.average(List.of()); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "threw"); }
""",
            "Empty list throws IllegalArgumentException.",
        ),
    ],
    level="independent",
)

VI_CH_P5_WORDS = vi_challenge(
    "Tần suất & nhóm",
    r"""Cho `List<String> words`, cài bằng Collectors (không vòng lặp hiện
hữu):
- `static Map<String, Long> frequencies(List<String> words)` — mỗi từ
  phân biệt → số lần xuất hiện (key phân biệt HOA/thường).
- `static Map<Integer, List<String>> byLength(List<String> words)` —
  nhóm từ theo độ dài.
- `static Map<Boolean, List<String>> longWords(List<String> words)` —
  chia hai nhóm length > 4 (true) so với còn lại (false).""",
    [
        ("frequencies đếm trùng lặp", "groupingBy(identity, counting()) — trả giá trị Long."),
        ("byLength nhóm theo độ dài", "groupingBy(String::length)."),
        ("Phân vùng theo ngưỡng", "partitioningBy(w -> w.length() > 4)."),
    ],
)

VI_CH_P5_SALES = vi_challenge(
    "toMap với merge function",
    r"""- `record Sale(String region, int amount)` trong `Solution`
- `static Map<String, Integer> totalsByRegion(List<Sale> sales)` — cộng
  amount theo region bằng `Collectors.toMap` với `Integer::sum` làm
  merge function.
- `static Map.Entry<String, Integer> topRegion(List<Sale> sales)` —
  trả entry region có tổng cao nhất (hòa: region tên nhỏ hơn thắng).

Key trùng không có merge function sẽ ném IllegalStateException — test
đảm bảo bạn đã dùng merge.""",
    [
        ("Tổng có merge trùng lặp", "toMap(Sale::region, Sale::amount, Integer::sum)."),
        ("Region dẫn đầu", "Entry max của map tổng; hòa bể theo tên."),
    ],
)

VI_CH_P5_STATS = vi_challenge(
    "Hai chỉ số, một lượt",
    r"""Dùng `Collectors.teeing` (hoặc reduction một lượt tương đương) trên
một list số nguyên:
- `static double average(List<Integer> xs)` — trung bình cộng; rỗng thì
  ném IllegalArgumentException.
- `static Map<String, Integer> rangeStats(List<Integer> xs)` — trả
  `{"min": ..., "max": ...}` tính trong một lượt teeing.
- `static String classify(List<Integer> xs)` — bài tập composition: map
  mỗi x thành x*2, giữ giá trị > 10, nối bằng dấu phẩy; trả chuỗi đã nối
  (list rỗng → chuỗi rỗng).""",
    [
        ("average", "Tổng/count dưới dạng double."),
        ("min/max một lượt", "teeing(min, max, Map::entry) hoặc tương đương."),
        ("classify composition", "3*2=6 (bỏ), 6*2=12, 9*2=18, 12*2=24 — nối theo thứ tự stream."),
        ("average chặn rỗng", "List rỗng ném IllegalArgumentException."),
    ],
)

write_practice(
    MOD,
    "javi-p5-functional",
    "Functional Lab",
    "Reshape data with groupingBy/partitioningBy/toMap/teeing, and judge composition vs loops.",
    "Xưởng hàm",
    "Biến đổi dữ liệu bằng groupingBy/partitioningBy/toMap/teeing, và phán đoán composition so với vòng lặp.",
    "functional-judgment",
    40,
    "intermediate",
    [CH_P5_WORDS, CH_P5_SALES, CH_P5_STATS],
    {CH_P5_WORDS["id"]: VI_CH_P5_WORDS, CH_P5_SALES["id"]: VI_CH_P5_SALES, CH_P5_STATS["id"]: VI_CH_P5_STATS},
    solutions=[
        (
            CH_P5_WORDS["id"],
            r"""
import java.util.*;
import java.util.stream.*;
import java.util.function.Function;

public class Solution {
    public static Map<String, Long> frequencies(List<String> words) {
        return words.stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
    }
    public static Map<Integer, List<String>> byLength(List<String> words) {
        return words.stream().collect(Collectors.groupingBy(String::length));
    }
    public static Map<Boolean, List<String>> longWords(List<String> words) {
        return words.stream().collect(Collectors.partitioningBy(w -> w.length() > 4));
    }
}
""",
            r"""
import java.util.*;
import java.util.stream.*;
import java.util.function.Function;

public class Solution {
    // W: groupingBy but counts each group's DISTINCT words instead of
    // occurrences — {"a":1} where {"a":2} is correct.
    public static Map<String, Long> frequencies(List<String> words) {
        return words.stream().collect(Collectors.groupingBy(Function.identity(),
            Collectors.collectingAndThen(Collectors.toSet(), s -> (long) s.size())));
    }
    public static Map<Integer, List<String>> byLength(List<String> words) {
        return words.stream().collect(Collectors.groupingBy(String::length));
    }
    public static Map<Boolean, List<String>> longWords(List<String> words) {
        return words.stream().collect(Collectors.partitioningBy(w -> w.length() > 4));
    }
}
""",
        ),
        (
            CH_P5_SALES["id"],
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Sale(String region, int amount) {}

    public static Map<String, Integer> totalsByRegion(List<Sale> sales) {
        return sales.stream().collect(Collectors.toMap(Sale::region, Sale::amount, Integer::sum));
    }

    public static Map.Entry<String, Integer> topRegion(List<Sale> sales) {
        Map<String, Integer> totals = totalsByRegion(sales);
        return totals.entrySet().stream()
            .max(Map.Entry.<String, Integer>comparingByValue()
                .thenComparing(Map.Entry.comparingByKey(Comparator.reverseOrder())))
            .orElseThrow();
    }
}
""",
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Sale(String region, int amount) {}

    // W: toMap WITHOUT a merge function — a second sale in the same
    // region throws IllegalStateException. The merge function exists
    // precisely for this.
    public static Map<String, Integer> totalsByRegion(List<Sale> sales) {
        return sales.stream().collect(Collectors.toMap(Sale::region, Sale::amount));
    }

    public static Map.Entry<String, Integer> topRegion(List<Sale> sales) {
        Map<String, Integer> totals = totalsByRegion(sales);
        return totals.entrySet().stream()
            .max(Map.Entry.<String, Integer>comparingByValue()
                .thenComparing(Map.Entry.comparingByKey(Comparator.reverseOrder())))
            .orElseThrow();
    }
}
""",
        ),
        (
            CH_P5_STATS["id"],
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static double average(List<Integer> xs) {
        if (xs == null || xs.isEmpty()) throw new IllegalArgumentException("xs required");
        return xs.stream().mapToInt(Integer::intValue).average().orElseThrow();
    }

    public static Map<String, Integer> rangeStats(List<Integer> xs) {
        return xs.stream().collect(Collectors.teeing(
            Collectors.minBy(Integer::compare),
            Collectors.maxBy(Integer::compare),
            (mn, mx) -> Map.of("min", mn.orElseThrow(), "max", mx.orElseThrow())));
    }

    public static String classify(List<Integer> xs) {
        return xs.stream().map(x -> x * 2)
            .filter(v -> v > 10)
            .map(String::valueOf)
            .collect(Collectors.joining(","));
    }
}
""",
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static double average(List<Integer> xs) {
        if (xs == null || xs.isEmpty()) throw new IllegalArgumentException("xs required");
        return xs.stream().mapToInt(Integer::intValue).average().orElseThrow();
    }

    public static Map<String, Integer> rangeStats(List<Integer> xs) {
        return xs.stream().collect(Collectors.teeing(
            Collectors.minBy(Integer::compare),
            Collectors.maxBy(Integer::compare),
            (mn, mx) -> Map.of("min", mn.orElseThrow(), "max", mx.orElseThrow())));
    }

    // W: filter BEFORE doubling — keeps x > 10 rather than x*2 > 10,
    // dropping values like 6 whose double qualifies.
    public static String classify(List<Integer> xs) {
        return xs.stream().filter(x -> x > 10)
            .map(x -> x * 2)
            .map(String::valueOf)
            .collect(Collectors.joining(","));
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — functional Java

You can now: reshape collections in a single pass with downstream
collectors, merge duplicate keys safely, and judge when a loop beats a
pipeline. Prove it with an analytics reducer.
"""

CP_MDX_VI = r"""
## Checkpoint — Java hàm

Giờ bạn có thể: biến đổi collection trong một lượt với downstream
collector, merge key trùng an toàn, và phán đoán khi nào vòng lặp thắng
pipeline. Chứng minh bằng một bộ reducer phân tích.
"""

CH_CP5 = challenge(
    "javi-checkpoint-m5-functional",
    "Analytics Reducer",
    r"""Build `Solution` analytics over `record Event(String user, String type, int ms)`:
- `static Map<String, Long> eventsByType(List<Event> events)` — counts
  per type (Long values).
- `static Map<String, Integer> msByUser(List<Event> events)` — total ms
  per user (merge duplicates with sum).
- `static Map<Boolean, List<String>> slowVsFast(List<Event> events,
  int threshold)` — partition event *types* by whether their average ms
  exceeds the threshold (true bucket = slower). Types in each bucket
  sorted alphabetically.""",
    r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Event(String user, String type, int ms) {}
    // Provide the three analytics methods here.
}
""",
    [
        (
            "counts per type",
            r"""
List<Object> evs = List.of(
    new Solution.Event("u", "read", 10), new Solution.Event("v", "read", 20),
    new Solution.Event("u", "write", 50));
checkEq(Solution.eventsByType((List) evs), Map.of("read", 2L, "write", 1L), "type counts");
""",
            "groupingBy(Event::type, counting()).",
        ),
        (
            "ms totals merge per user",
            r"""
List<Object> evs = List.of(
    new Solution.Event("u", "read", 10), new Solution.Event("u", "write", 50));
checkEq(Solution.msByUser((List) evs), Map.of("u", 60), "user ms merged");
""",
            "toMap(Event::user, Event::ms, Integer::sum).",
        ),
        (
            "slow vs fast by average",
            r"""
List<Object> evs = List.of(
    new Solution.Event("u", "quick", 5), new Solution.Event("u", "slow", 90),
    new Solution.Event("v", "slow", 30));
Map<Boolean, List<String>> out = Solution.slowVsFast((List) evs, 40);
checkEq(out.get(true), List.of("slow"), "slow type");
checkEq(out.get(false), List.of("quick"), "fast type");
""",
            "Average per type: quick=5 ≤ 40 (false), slow=60 > 40 (true).",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP5 = vi_challenge(
    "Bộ reducer phân tích",
    r"""Xây `Solution` phân tích trên `record Event(String user, String type, int ms)`:
- `static Map<String, Long> eventsByType(List<Event> events)` — đếm theo
  type (giá trị Long).
- `static Map<String, Integer> msByUser(List<Event> events)` — tổng ms
  theo user (merge trùng bằng sum).
- `static Map<Boolean, List<String>> slowVsFast(List<Event> events,
  int threshold)` — phân loại *type* sự kiện theo việc trung bình ms của
  nó có vượt ngưỡng không (nhóm true = chậm hơn). Type trong mỗi nhóm
  sắp theo bảng chữ cái.""",
    [
        ("Đếm theo type", "groupingBy(Event::type, counting())."),
        ("Tổng ms merge theo user", "toMap(Event::user, Event::ms, Integer::sum)."),
        ("Chậm vs nhanh theo trung bình", "Trung bình theo type: quick=5 ≤ 40 (false), slow=60 > 40 (true)."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-functional",
    "Checkpoint: Functional & Collectors",
    "Graded checkpoint: analytics reducers over an event log using groupingBy, toMap merges, and partitioning.",
    15,
    CP_MDX,
    "Checkpoint: Hàm & Collectors",
    "Checkpoint chấm điểm: các reducer phân tích trên log sự kiện dùng groupingBy, merge toMap, và partitioning.",
    CP_MDX_VI,
    CH_CP5,
    VI_CH_CP5,
    solution=r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Event(String user, String type, int ms) {}

    public static Map<String, Long> eventsByType(List<Event> events) {
        return events.stream().collect(Collectors.groupingBy(Event::type, Collectors.counting()));
    }

    public static Map<String, Integer> msByUser(List<Event> events) {
        return events.stream().collect(Collectors.toMap(Event::user, Event::ms, Integer::sum));
    }

    public static Map<Boolean, List<String>> slowVsFast(List<Event> events, int threshold) {
        Map<String, Double> avgByType = events.stream().collect(Collectors.groupingBy(
            Event::type, Collectors.averagingInt(Event::ms)));
        Map<Boolean, List<String>> out = new HashMap<>();
        out.put(true, new ArrayList<>());
        out.put(false, new ArrayList<>());
        avgByType.forEach((type, avg) ->
            out.get(avg > threshold).add(type));
        out.get(true).sort(null);
        out.get(false).sort(null);
        return out;
    }
}
""",
    wrong=r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Event(String user, String type, int ms) {}

    public static Map<String, Long> eventsByType(List<Event> events) {
        return events.stream().collect(Collectors.groupingBy(Event::type, Collectors.counting()));
    }

    public static Map<String, Integer> msByUser(List<Event> events) {
        return events.stream().collect(Collectors.toMap(Event::user, Event::ms, Integer::sum));
    }

    public static Map<Boolean, List<String>> slowVsFast(List<Event> events, int threshold) {
        // W: compares each event's ms to the threshold instead of the
        // TYPE average — one fast event in a slow type flips its bucket.
        Map<Boolean, List<String>> out = new HashMap<>();
        out.put(true, new ArrayList<>());
        out.put(false, new ArrayList<>());
        for (Event e : events) {
            out.get(e.ms() > threshold).add(e.type());
        }
        out.get(true).sort(null);
        out.get(false).sort(null);
        return out;
    }
}
""",
)
