#!/usr/bin/env python3
"""Java - Beginner - Module 12: java-streams-optional.

Functional Java: lambdas, method references, one stream pipeline at a time,
Optional at its best boundaries, and honest advice about when a plain loop
is clearer. House contract (declarative write_* calls, CjTestBase tests).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-streams-optional"

# ── lesson 12.1 — lambdas & functional interfaces ───────────────────────────
L_LAMBDA_EN = r"""
Some behavior is too small for a named method. Java 8 added a syntax for
"just the behavior": the **lambda expression**.

```java
// old way: an anonymous class
Comparator<String> byLength = new Comparator<String>() {
    public int compare(String a, String b) {
        return Integer.compare(a.length(), b.length());
    }
};

// new way: the same thing as a lambda
Comparator<String> byLength = (a, b) -> Integer.compare(a.length(), b.length());
```

A lambda `(a, b) -> expression` reads: "given `a` and `b`, produce this
value." Where a variable's type is obvious, Java infers it.

## Functional interfaces

A lambda is not any old shorthand - it fills an interface with **exactly
one abstract method** (a *functional interface*). The core four, all in
`java.util.function`:

| Interface | Method | Meaning |
|---|---|---|
| `Predicate<T>` | `boolean test(T t)` | a yes/no question about `t` |
| `Function<T,R>` | `R apply(T t)` | turn a `T` into an `R` |
| `Consumer<T>` | `void accept(T t)` | do something with `t`, return nothing |
| `Supplier<T>` | `T get()` | produce a value from nothing |

```java
Predicate<String> isEmpty = s -> s.isEmpty();
Function<String, Integer> len = String::length;   // method reference
Consumer<String> shout = s -> System.out.println(s.toUpperCase());
Supplier<java.util.List<String>> maker = java.util.ArrayList::new;
```

The `String::length` form is a **method reference** - a lambda whose body
only calls one method: `Type::method` for instance methods on the
argument, `object::method` for a specific object, `Type::new` for a
constructor.

You can declare your own functional interfaces too - `@FunctionalInterface`
makes the compiler enforce the one-method rule:

```java
@FunctionalInterface
interface Validator<T> {
    boolean check(T value);   // the single abstract method
}
```

## Where you'll meet them first

Sorting, `removeIf`, `replaceAll` on collections:

```java
names.removeIf(s -> s.isBlank());            // Predicate
names.replaceAll(s -> s.trim());             // UnaryOperator (a Function T->T)
names.sort(Comparator.comparingInt(String::length));
```
"""

L_LAMBDA_VI = r"""
Có những hành vi quá nhỏ để trở thành một phương thức có tên. Java 8 bổ
sung cú pháp "chỉ lấy phần hành vi": **biểu thức lambda**.

```java
// cách cũ: anonymous class
Comparator<String> byLength = new Comparator<String>() {
    public int compare(String a, String b) {
        return Integer.compare(a.length(), b.length());
    }
};

// cách mới: cùng một ý bằng lambda
Comparator<String> byLength = (a, b) -> Integer.compare(a.length(), b.length());
```

Lambda `(a, b) -> expression` đọc là: "cho `a` và `b`, tạo ra giá trị
này." Khi kiểu của biến đã rõ ràng, Java tự suy luận.

## Functional interface

Lambda không phải cú tắt tùy tiện - nó lấp vào một interface có **đúng
một phương thức trừu tượng** (*functional interface*). Bốn giao diện cốt
lõi, đều trong `java.util.function`:

| Interface | Phương thức | Ý nghĩa |
|---|---|---|
| `Predicate<T>` | `boolean test(T t)` | câu hỏi có/không về `t` |
| `Function<T,R>` | `R apply(T t)` | biến `T` thành `R` |
| `Consumer<T>` | `void accept(T t)` | làm gì đó với `t`, không trả về |
| `Supplier<T>` | `T get()` | tạo giá trị từ hư không |

Dạng `String::length` là **method reference** - một lambda mà thân chỉ
gọi đúng một phương thức: `Type::method` cho instance method trên đối số,
`object::method` cho một đối tượng cụ thể, `Type::new` cho constructor.

Bạn cũng có thể tự khai báo - `@FunctionalInterface` bắt compiler thi hành
luật một-phương-thức:

```java
@FunctionalInterface
interface Validator<T> {
    boolean check(T value);   // phương thức trừu tượng duy nhất
}
```

## Nơi bạn gặp chúng đầu tiên

Sắp xếp, `removeIf`, `replaceAll` trên collection:

```java
names.removeIf(s -> s.isBlank());            // Predicate
names.replaceAll(s -> s.trim());             // UnaryOperator (Function T->T)
names.sort(Comparator.comparingInt(String::length));
```
"""

# ── lesson 12.2 — the stream pipeline ───────────────────────────────────────
L_STREAM_EN = r"""
A **stream** is a conveyor belt for data: you line up processing steps,
and elements flow through them one stage at a time.

```java
List<String> names = List.of("Ada", "bob", "Grace", "eve", "Turing");

List<String> result = names.stream()          // 1. source
    .filter(n -> n.length() > 3)              // 2. intermediate: keep some
    .map(String::toUpperCase)                 // 3. intermediate: transform
    .sorted()                                 // 4. intermediate: order
    .collect(java.util.stream.Collectors.toList());  // 5. terminal: produce
// [ADA, GRACE, TURING]
```

The vocabulary:

- **Source** - `list.stream()`, `Stream.of(...)`, `map.entrySet().stream()`.
- **Intermediate operations** (return a new stream, are *lazy* - nothing
  runs until a terminal op exists): `filter`, `map`, `sorted`, `distinct`,
  `limit`, `skip`, `peek`.
- **Terminal operations** (actually run the belt, once):
  `collect`, `forEach`, `count`, `anyMatch`/`allMatch`/`noneMatch`,
  `findFirst`, `reduce`.

## Primitive streams avoid boxing

```java
int total = prices.stream()            // Stream<Double>
    .mapToInt(Double::intValue)        // IntStream - no Double objects
    .sum();
```

`mapToInt`/`mapToLong`/`mapToDouble` switch to primitive streams with
`sum()`, `average()`, `max()`, `count()` ready-made.

## Collectors you will actually use

```java
Collectors.toList()                              // the everyday one
Collectors.joining(", ")                         // "Ada, Grace"
Collectors.groupingBy(String::length)            // Map<Integer, List<String>>
Collectors.counting()                            // usually inside groupingBy
```

## The honesty section: when a loop is clearer

Streams are not a badge of honor. Prefer a plain loop when:

- you're **accumulating with tricky state** (running indexes, two counters
  stepping on each other);
- you need **early exit with side effects** mid-computation;
- the chain would run five stages deep and nobody can read it;
- you're processing **two collections in lockstep**.

A good rule: use streams for *describe-a-transformation* code
("filter the valid, map to names, collect"), loops for
*drive-a-procedure* code. If a teammate must squint at your stream, write
the loop.
"""

L_STREAM_VI = r"""
**Stream** là băng chuyền cho dữ liệu: bạn xếp các bước xử lý, và phần tử
chảy qua từng công đoạn.

```java
List<String> names = List.of("Ada", "bob", "Grace", "eve", "Turing");

List<String> result = names.stream()          // 1. nguồn
    .filter(n -> n.length() > 3)              // 2. trung gian: giữ lại một số
    .map(String::toUpperCase)                 // 3. trung gian: biến đổi
    .sorted()                                 // 4. trung gian: sắp xếp
    .collect(java.util.stream.Collectors.toList());  // 5. terminal: tạo kết quả
// [ADA, GRACE, TURING]
```

Từ vựng:

- **Nguồn** - `list.stream()`, `Stream.of(...)`, `map.entrySet().stream()`.
- **Phép toán trung gian** (trả về stream mới, *lazy* - không chạy cho đến
  khi có phép terminal): `filter`, `map`, `sorted`, `distinct`, `limit`,
  `skip`, `peek`.
- **Phép toán terminal** (thực sự chạy băng chuyền, đúng một lần):
  `collect`, `forEach`, `count`, `anyMatch`/`allMatch`/`noneMatch`,
  `findFirst`, `reduce`.

## Stream nguyên thủy tránh boxing

```java
int total = prices.stream()            // Stream<Double>
    .mapToInt(Double::intValue)        // IntStream - không tạo đối tượng Double
    .sum();
```

## Collector hay dùng

```java
Collectors.toList()                              // dùng hằng ngày
Collectors.joining(", ")                         // "Ada, Grace"
Collectors.groupingBy(String::length)            // Map<Integer, List<String>>
Collectors.counting()                            // thường nằm trong groupingBy
```

## Phần nói thật: khi nào vòng lặp rõ hơn

Stream không phải huy hiệu danh dự. Hãy dùng vòng lặp thường khi:

- bạn **tích lũy với trạng thái rối** (nhiều biến đếm ràng buộc nhau);
- bạn cần **thoát sớm giữa chừng** với tác dụng phụ;
- chuỗi sẽ dài năm tầng và không ai đọc nổi;
- bạn xử lý **hai collection song song từng cặp**.

Quy tắc tốt: stream cho code *mô tả phép biến đổi*, loop cho code *điều
khiển quy trình*. Nếu đồng đội phải nheo mắt nhìn stream của bạn, hãy
viết vòng lặp.
"""

# ── lesson 12.3 — Optional ──────────────────────────────────────────────────
L_OPTIONAL_EN = r"""
`null` is Java's oldest footgun: any reference can silently be `null`, and
the explosion happens far from the cause. `Optional<T>` makes "might not
be there" **visible in the type**.

```java
static Optional<String> findEmail(java.util.Map<String, String> users, String name) {
    return Optional.ofNullable(users.get(name));   // may be empty
}

// at the boundary, decide explicitly:
String display = findEmail(users, "ada")
    .map(String::toLowerCase)                      // transform if present
    .orElse("(no email)");                          // default if empty
```

The small set of methods worth knowing by heart:

| Method | Reads as |
|---|---|
| `Optional.of(v)` | wrap a value that must not be null (throws if it is) |
| `Optional.ofNullable(v)` | wrap a value that may be null |
| `Optional.empty()` | nothing here |
| `.isPresent()` / `.isEmpty()` | yes/no check |
| `.get()` | **avoid** - it re-introduces the crash, just with steps |
| `.orElse(default)` | value, or the default |
| `.orElseGet(supplier)` | value, or compute a default lazily |
| `.map(f)` | transform the value if present |
| `.filter(p)` | keep it only if the predicate holds |
| `.ifPresent(c)` | run this consumer if there is a value |

## The intended shape

Optional is a **return type at boundaries**: "this lookup may find
nothing." Fields, method parameters, and collections of Optionals are the
wrong tool - use `null`-free design there instead (an empty list, a
sentinel, or split the type).

## Anti-patterns the compiler won't stop

```java
// These two lines are the same bug wearing different hats:
opt.get()                       // NoSuchElementException if empty
if (opt.isPresent()) x = opt.get();   // verbose null-check reborn

// A null inside an Optional is still a landmine:
Optional.ofNullable(null).get()   // still throws
```

If you find yourself calling `.isPresent()` and `.get()` together, reach
for `.map`/`.orElse` instead - keep the decision *inside* the Optional.
"""

L_OPTIONAL_VI = r"""
`null` là cái bẫy lâu đời nhất của Java: bất kỳ tham chiếu nào cũng có thể
âm thầm là `null`, và vụ nổ xảy ra rất xa nơi gây ra. `Optional<T>` biến
"có thể không có" thành **hiện hữu ngay trên kiểu**.

```java
static Optional<String> findEmail(java.util.Map<String, String> users, String name) {
    return Optional.ofNullable(users.get(name));   // có thể rỗng
}

// tại biên giới, hãy quyết định rõ ràng:
String display = findEmail(users, "ada")
    .map(String::toLowerCase)                      // biến đổi nếu có giá trị
    .orElse("(no email)");                          // mặc định nếu rỗng
```

| Phương thức | Đọc là |
|---|---|
| `Optional.of(v)` | bọc giá trị không được null (ném exception nếu null) |
| `Optional.ofNullable(v)` | bọc giá trị có thể null |
| `Optional.empty()` | không có gì ở đây |
| `.isPresent()` / `.isEmpty()` | kiểm tra có/không |
| `.get()` | **tránh** - tái tạo chính vụ crash, chỉ là qua thêm một bước |
| `.orElse(default)` | giá trị, hoặc mặc định |
| `.orElseGet(supplier)` | giá trị, hoặc tính mặc định một cách lười |
| `.map(f)` | biến đổi giá trị nếu có |
| `.filter(p)` | chỉ giữ nếu điều kiện thỏa |
| `.ifPresent(c)` | chạy consumer này nếu có giá trị |

## Dạng đúng đắn

Optional là **kiểu trả về tại biên giới**: "lần tra này có thể không tìm
thấy." Đừng dùng Optional cho field, tham số, hay collection các Optional.

## Anti-pattern mà compiler không chặn

```java
// Hai dòng này là cùng một bug đội mũ khác nhau:
opt.get()                       // NoSuchElementException nếu rỗng
if (opt.isPresent()) x = opt.get();   // null-check nhiều lời lại hồi sinh
```

Nếu bạn thấy mình gọi `.isPresent()` rồi `.get()` liền nhau, hãy chuyển
sang `.map`/`.orElse` - giữ mọi quyết định *bên trong* Optional.
"""

# ── challenges ───────────────────────────────────────────────────────────────
BOILER_STREAM = r"""public class Solution {
    public static java.util.List<String> loudLongNames(java.util.List<String> names) {
        return java.util.List.of();
    }

    public static int sumLengths(java.util.List<String> words) {
        return 0;
    }
}
"""

P12_STREAM = challenge(
    "javb-m12-stream-pipeline",
    "One pipeline, three stages",
    "Using ONE stream pipeline per method (no loops): `loudLongNames` returns the names longer than 3 characters, uppercased, sorted alphabetically. `sumLengths` returns the total character count of all words (empty list -> 0).",
    BOILER_STREAM,
    [
        (
            "filter, map, sort, collect",
            r"""
CjTestBase.checkEq(Solution.loudLongNames(java.util.List.of("Turing", "bob", "Grace")),
    java.util.List.of("GRACE", "TURING"), "long names, loud, sorted - input order scrambled");
CjTestBase.checkEq(Solution.loudLongNames(java.util.List.of("a", "bb")), java.util.List.of(), "nothing long enough");
""",
            "names.stream().filter(...).map(String::toUpperCase).sorted().collect(...) - do not drop the sorted() stage.",
        ),
        (
            "primitive stream sums",
            r"""
CjTestBase.checkEq(Solution.sumLengths(java.util.List.of("Ada", "Grace")), 8, "3+5");
CjTestBase.checkEq(Solution.sumLengths(java.util.List.of()), 0, "empty list -> 0");
""",
            "mapToInt(String::length).sum() handles the empty case for free.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

P12_STREAM_VI = vi_challenge(
    "Một pipeline, ba công đoạn",
    "Dùng MỘT pipeline stream cho mỗi phương thức (không dùng vòng lặp): `loudLongNames` trả về các tên dài hơn 3 ký tự, in hoa, sắp xếp theo bảng chữ cái. `sumLengths` trả về tổng số ký tự của mọi từ (danh sách rỗng -> 0).",
    [("filter, map, sort, collect", "names.stream().filter(...).map(String::toUpperCase).sorted().collect(...) - không bỏ sân khấu sorted()."),
     ("stream nguyên thủy cộng dồn", "mapToInt(String::length).sum() tự xử lý luôn trường hợp rỗng.")],
)

BOILER_LAMBDA = r"""public class Solution {
    public static java.util.List<String> sortWords(java.util.List<String> words) {
        return java.util.List.of();
    }
}
"""

P12_LAMBDA = challenge(
    "javb-m12-lambda-sort",
    "Sort by rule, not by loop",
    "Using a lambda or method reference (no manual loop): return the words sorted by length, shortest first; same-length words keep alphabetical order.",
    BOILER_LAMBDA,
    [
        (
            "length first, then alphabetical",
            r"""
CjTestBase.checkEq(Solution.sortWords(java.util.List.of("pear", "fig", "kiwi", "date")),
    java.util.List.of("fig", "date", "kiwi", "pear"), "length ties stay alphabetical");
CjTestBase.checkEq(Solution.sortWords(java.util.List.of()), java.util.List.of(), "empty in, empty out");
""",
            "Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder())",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

P12_LAMBDA_VI = vi_challenge(
    "Sắp xếp theo quy tắc, không phải vòng lặp",
    "Dùng lambda hoặc method reference (không viết vòng lặp thủ công): trả về các từ được sắp theo độ dài, ngắn trước; các từ cùng độ dài giữ thứ tự bảng chữ cái.",
    [("độ dài trước, rồi bảng chữ cái", "Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder())")],
)

BOILER_OPTIONAL = r"""public class Solution {
    public static java.util.Optional<Integer> parsePort(String input) {
        return java.util.Optional.empty();
    }
}
"""

P12_OPTIONAL = challenge(
    "javb-m12-optional-parse",
    "Optional at the boundary",
    "Write `parsePort(String input)`: return `Optional` of the parsed port when input is a valid number in 1..65535; `Optional.empty()` otherwise (null, blank, non-numeric, or out of range).",
    BOILER_OPTIONAL,
    [
        (
            "valid ports wrap",
            r"""
CjTestBase.checkEq(Solution.parsePort("8080"), java.util.Optional.of(8080), "8080 parses");
CjTestBase.checkEq(Solution.parsePort(" 443 "), java.util.Optional.of(443), "trimmed and parsed");
""",
            "Optional.ofNullable after your existing parse-check pattern.",
        ),
        (
            "everything else stays empty - never null",
            r"""
CjTestBase.checkEq(Solution.parsePort("abc"), java.util.Optional.empty(), "not a number");
CjTestBase.checkEq(Solution.parsePort("99999"), java.util.Optional.empty(), "out of range");
CjTestBase.checkEq(Solution.parsePort("0"), java.util.Optional.empty(), "0 is not a port");
CjTestBase.checkEq(Solution.parsePort(null), java.util.Optional.empty(), "null -> empty");
""",
            "Range-check after parsing; the result must never be an Optional wrapping null.",
        ),
    ],
    level="guided",
    difficulty="advanced",
)

P12_OPTIONAL_VI = vi_challenge(
    "Optional tại biên giới",
    "Viết `parsePort(String input)`: trả về `Optional` của port đã parse khi input là số hợp lệ trong 1..65535; `Optional.empty()` trong mọi trường hợp khác (null, rỗng, không phải số, hoặc ngoài khoảng).",
    [("port hợp lệ được bọc", "Optional.ofNullable sau khi có mẫu parse-check quen thuộc."),
     ("mọi trường hợp khác giữ rỗng - không bao giờ null", "Kiểm tra khoảng giá trị sau khi parse; kết quả không bao giờ là Optional bọc null.")],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
BOILER_WORDSTATS = r"""public class Solution {
    public record WordStats(java.util.Map<String, Integer> byInitial,
                            java.util.List<String> longest,
                            java.util.Optional<String> joined) {}

    public static WordStats analyze(java.util.List<String> words) {
        return null;
    }
}
"""

P12_CP_CH = challenge(
    "javb-m12-cp-wordstats",
    "Checkpoint: word stats pipeline",
    "Implement `analyze(words)` returning a `WordStats` record with three parts, each built with streams: `byInitial` maps each lowercase first letter to how many words start with it (case-insensitive); `longest` lists every word whose length equals the maximum length found (original casing, in original order); `joined` is `Optional` of all words joined by `\" & \"`, empty when the input is empty.",
    BOILER_WORDSTATS,
    [
        (
            "initials are counted case-insensitively",
            r"""
Solution.WordStats s = Solution.analyze(java.util.List.of("Ada", "amy", "Bob", "grace"));
CjTestBase.checkEq(s.byInitial().get("a"), 2, "a -> 2");
CjTestBase.checkEq(s.byInitial().get("b"), 1, "b -> 1");
CjTestBase.checkEq(s.byInitial().get("g"), 1, "g -> 1");
CjTestBase.checkEq(s.byInitial().size(), 3, "exactly three initials");
""",
            "map(String::toLowerCase) BEFORE groupingBy(w -> w.substring(0, 1)).",
        ),
        (
            "all ties share the crown",
            r"""
Solution.WordStats s = Solution.analyze(java.util.List.of("Ada", "amy", "Bob", "grace"));
CjTestBase.checkEq(s.longest(), java.util.List.of("grace"), "only the 5-letter word");
Solution.WordStats t = Solution.analyze(java.util.List.of("kiwi", "date", "fig"));
CjTestBase.checkEq(t.longest(), java.util.List.of("kiwi", "date"), "4-letter tie, original order");
""",
            "Two passes are fine: find the max length first, then filter equals.",
        ),
        (
            "joined is Optional, empty-safe",
            r"""
CjTestBase.checkEq(Solution.analyze(java.util.List.of("Ada", "Bob")).joined(),
    java.util.Optional.of("Ada & Bob"), "joined with ampersand");
CjTestBase.checkEq(Solution.analyze(java.util.List.of()).joined(),
    java.util.Optional.empty(), "empty input -> empty Optional");
CjTestBase.checkEq(Solution.analyze(java.util.List.of()).byInitial(), java.util.Map.of(), "no initials either");
""",
            "Collectors.joining(\" & \") over an empty stream yields \"\" - wrap with Optional.ofNullable after filtering that case, or guard it.",
        ),
    ],
    level="real-world",
    difficulty="advanced",
)

P12_CP_VI = vi_challenge(
    "Checkpoint: pipeline thống kê từ",
    "Cài đặt `analyze(words)` trả về record `WordStats` với ba phần, mỗi phần dựng bằng stream: `byInitial` ánh xạ mỗi chữ cái đầu (viết thường) sang số từ bắt đầu bằng nó (không phân biệt hoa thường); `longest` liệt kê mọi từ có độ dài bằng độ dài lớn nhất (giữ nguyên hoa thường, theo thứ tự gốc); `joined` là `Optional` của mọi từ nối bằng `\" & \"`, rỗng khi input rỗng.",
    [("chữ cái đầu được đếm không phân biệt hoa thường", "map(String::toLowerCase) TRƯỚC khi groupingBy(w -> w.substring(0, 1))."),
     ("mọi người đồng hạng cùng nhận vương miện", "Hai lượt cũng được: tìm độ dài max trước, rồi filter bằng equals."),
     ("joined là Optional, an toàn với rỗng", "Collectors.joining(\" & \") trên stream rỗng cho ra \"\" - hãy chặn trường hợp đó.")],
)

P12_CP_R = r"""public class Solution {
    public record WordStats(java.util.Map<String, Integer> byInitial,
                            java.util.List<String> longest,
                            java.util.Optional<String> joined) {}

    public static WordStats analyze(java.util.List<String> words) {
        java.util.Map<String, Integer> byInitial = words.stream()
            .filter(w -> !w.isEmpty())
            .map(String::toLowerCase)
            .collect(java.util.stream.Collectors.groupingBy(
                w -> w.substring(0, 1),
                java.util.stream.Collectors.summingInt(w -> 1)));

        int maxLen = words.stream().mapToInt(String::length).max().orElse(0);
        java.util.List<String> longest = words.stream()
            .filter(w -> w.length() == maxLen)
            .collect(java.util.stream.Collectors.toList());

        java.util.Optional<String> joined = words.isEmpty()
            ? java.util.Optional.empty()
            : java.util.Optional.of(String.join(" & ", words));

        return new WordStats(byInitial, longest, joined);
    }
}
"""

P12_CP_W = r"""public class Solution {
    public record WordStats(java.util.Map<String, Integer> byInitial,
                            java.util.List<String> longest,
                            java.util.Optional<String> joined) {}

    public static WordStats analyze(java.util.List<String> words) {
        java.util.Map<String, Integer> byInitial = words.stream()
            .map(String::toLowerCase)
            .collect(java.util.stream.Collectors.groupingBy(
                w -> w.substring(0, 1),
                java.util.stream.Collectors.summingInt(w -> 1)));

        int maxLen = words.stream().mapToInt(String::length).max().orElse(0);
        java.util.List<String> longest = words.stream()
            .filter(w -> w.length() == maxLen)
            .collect(java.util.stream.Collectors.toList());

        // BUG: joins even when empty -> Optional.of("") instead of empty;
        //      and groupingBy crashes on an empty input (no first letter)
        return new WordStats(byInitial, longest, java.util.Optional.of(String.join(" & ", words)));
    }
}
"""

CK_M12_MD = r"""
The word-stats pipeline - three stream stages composing into one record.

Inside the provided `Solution` skeleton, implement `analyze(words)` as the
checkpoint specifies. Three design notes before you start:

1. **Lowercase before grouping** - `groupingBy` after `map(String::toLowerCase)`,
   and filter out empty words first (an empty word has no first letter).
2. **Two passes are idiomatic** - `max()` then `filter(length == max)` is
   clearer than a clever single-pass fold, and streams are cheap to run
   twice on an in-memory list.
3. **Empty input** - `String.join` over nothing yields `""`; the spec wants
   an *empty Optional*, so guard it. This is exactly the boundary honesty
   that `Optional` exists for.

The wrong solution shown in the notes fails two ways: it builds
`Optional.of("")` for empty input, and it crashes on empty input before
that - `substring(0, 1)` has no first letter to take.
"""

CK_M12_MD_VI = r"""
Pipeline thống kê từ - ba công đoạn stream hợp thành một record.

Bên trong khung `Solution`, cài đặt `analyze(words)` theo đúng checkpoint.
Ba ghi chú thiết kế trước khi bắt đầu:

1. **Viết thường trước khi group** - `groupingBy` sau
   `map(String::toLowerCase)`, và lọc từ rỗng trước (từ rỗng không có chữ
   cái đầu).
2. **Hai lượt là chuyện bình thường** - `max()` rồi
   `filter(length == max)` rõ ràng hơn một fold một-lượt thông minh, và
   chạy stream hai lần trên danh sách trong bộ nhớ rất rẻ.
3. **Input rỗng** - `String.join` trên không gì cả cho ra `""`; đề bài
   muốn một *Optional rỗng*, nên hãy chặn trường hợp đó. Đây chính là sự
   trung thực tại biên giới mà `Optional` sinh ra để phục vụ.

Solution sai trong ghi chú sai theo hai cách: nó dựng `Optional.of("")`
cho input rỗng, và trước đó còn sập với input rỗng - `substring(0, 1)`
không có chữ cái đầu để lấy.
"""

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Streams, Lambdas & Optional",
    "Lambdas and method references, one stream pipeline at a time, Optional at boundaries - and honest advice on when a plain loop wins.",
    "Stream, Lambda & Optional",
    "Lambda và method reference, từng pipeline stream một, Optional tại biên giới - và lời khuyên thẳng thắn về khi nào vòng lặp thắng.",
    ["lambdas-functional", "stream-pipeline", "optional-boundaries", "java-checkpoint-streams"],
    ["javb-p12-streams"],
)

write_lesson(
    MOD, "lambdas-functional",
    "Lambdas & Functional Interfaces",
    "The arrow syntax, the core four interfaces, method references, and where you'll meet them first.",
    18,
    L_LAMBDA_EN,
    "Lambda & Functional Interface",
    "Cú pháp mũi tên, bốn giao diện cốt lõi, method reference, và nơi bạn sẽ gặp chúng đầu tiên.",
    L_LAMBDA_VI,
)

write_lesson(
    MOD, "stream-pipeline",
    "The Stream Pipeline",
    "Source, lazy intermediate ops, terminal ops, primitive streams, collectors - plus the honesty section on loops.",
    20,
    L_STREAM_EN,
    "Pipeline Stream",
    "Nguồn, phép trung gian lazy, phép terminal, stream nguyên thủy, collector - cùng phần nói thật về vòng lặp.",
    L_STREAM_VI,
)

write_lesson(
    MOD, "optional-boundaries",
    "Optional at the Boundaries",
    "Making 'might not be there' visible in the type - and the anti-patterns the compiler won't stop.",
    16,
    L_OPTIONAL_EN,
    "Optional tại biên giới",
    "Biến 'có thể không có' thành hiện hữu trên kiểu - và những anti-pattern mà compiler không chặn.",
    L_OPTIONAL_VI,
)

write_practice(
    MOD, "javb-p12-streams",
    "Practice: Pipelines at Work",
    "A three-stage pipeline, comparator composition, and Optional guarding a parse boundary.",
    "Thực hành: Pipeline tại chỗ làm",
    "Pipeline ba công đoạn, ghép comparator, và Optional canh một biên giới parse.",
    "stream-pipeline", 45, "beginner",
    [P12_STREAM, P12_LAMBDA, P12_OPTIONAL],
    {P12_STREAM["id"]: P12_STREAM_VI, P12_LAMBDA["id"]: P12_LAMBDA_VI, P12_OPTIONAL["id"]: P12_OPTIONAL_VI},
    solutions=[
        (
            P12_STREAM["id"],
            r"""public class Solution {
    public static java.util.List<String> loudLongNames(java.util.List<String> names) {
        return names.stream()
            .filter(n -> n.length() > 3)
            .map(String::toUpperCase)
            .sorted()
            .collect(java.util.stream.Collectors.toList());
    }

    public static int sumLengths(java.util.List<String> words) {
        return words.stream().mapToInt(String::length).sum();
    }
}
""",
            r"""public class Solution {
    public static java.util.List<String> loudLongNames(java.util.List<String> names) {
        // BUG: sorted() is missing entirely - output follows input order
        return names.stream()
            .filter(n -> n.length() > 3)
            .map(String::toUpperCase)
            .collect(java.util.stream.Collectors.toList());   // BUG: sorted() missing
    }

    public static int sumLengths(java.util.List<String> words) {
        return words.stream().mapToInt(String::length).sum();
    }
}
""",
        ),
        (
            P12_LAMBDA["id"],
            r"""public class Solution {
    public static java.util.List<String> sortWords(java.util.List<String> words) {
        return words.stream()
            .sorted(java.util.Comparator
                .comparingInt(String::length)
                .thenComparing(java.util.Comparator.naturalOrder()))
            .collect(java.util.stream.Collectors.toList());
    }
}
""",
            r"""public class Solution {
    public static java.util.List<String> sortWords(java.util.List<String> words) {
        // BUG: only compares length - equal-length ties come out in
        //      encounter order, not alphabetical order
        return words.stream()
            .sorted(java.util.Comparator.comparingInt(String::length))
            .collect(java.util.stream.Collectors.toList());
    }
}
""",
        ),
        (
            P12_OPTIONAL["id"],
            r"""public class Solution {
    public static java.util.Optional<Integer> parsePort(String input) {
        if (input == null || input.isBlank()) return java.util.Optional.empty();
        try {
            int port = Integer.parseInt(input.trim());
            if (port < 1 || port > 65535) return java.util.Optional.empty();
            return java.util.Optional.of(port);
        } catch (NumberFormatException e) {
            return java.util.Optional.empty();
        }
    }
}
""",
            r"""public class Solution {
    public static java.util.Optional<Integer> parsePort(String input) {
        if (input == null || input.isBlank()) return java.util.Optional.empty();
        try {
            int port = Integer.parseInt(input.trim());
            return java.util.Optional.of(port);   // BUG: no range check - 99999 and 0 become "valid"
        } catch (NumberFormatException e) {
            return java.util.Optional.empty();
        }
    }
}
""",
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-streams",
    "Checkpoint: The Word-Stats Pipeline",
    "groupingBy, a max-then-filter pass, and an Optional that means empty when it says empty.",
    40, CK_M12_MD,
    "Checkpoint: Pipeline Thống Kê Từ",
    "groupingBy, một lượt max-then-filter, và một Optional nói rỗng là đúng là rỗng.",
    CK_M12_MD_VI,
    P12_CP_CH, P12_CP_VI,
    solution=P12_CP_R, wrong=P12_CP_W,
)

print("module 12 complete")
