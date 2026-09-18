#!/usr/bin/env python3
"""Java — Beginner — Module 10: java-collections-generics."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-collections-generics"

L_LIST_EN = r'''
The **Collections Framework** is Java's toolbox of growable data structures.
`List` is the everyday one: an ordered, growable sequence.

```java
import java.util.ArrayList;
import java.util.List;

List<String> names = new ArrayList<>();   // interface left, implementation right
names.add("Ada");
names.add("Grace");
names.add(1, "Linus");                    // insert at index 1
System.out.println(names.get(0));         // Ada
System.out.println(names.size());         // 3
System.out.println(names.remove("Ada"));  // true (removed)
```

Declare the **interface** type (`List`), construct the **implementation**
(`ArrayList`). All your calling code sees the interface; swapping to
`LinkedList` tomorrow touches exactly one line. The `<String>` is a
**generic type parameter** — more on it in a moment, but it already pays:
`names.get(0)` is statically known to be a String.

The core List methods: `add(e)`, `add(i, e)`, `get(i)`, `set(i, e)`,
`remove(i)`, `remove(Object)`, `size()`, `contains(e)`, `indexOf(e)`,
`isEmpty()`, `clear()`. Iteration uses for-each like arrays:

```java
for (String n : names) { System.out.println(n); }
```

**ArrayList vs LinkedList** — the interview staple, kept honest: ArrayList
is a resizable array; `get(i)` is instant, middle inserts shift elements.
LinkedList is a chain; ends are cheap, `get(i)` walks from the nearest end.
For beginners the honest summary: **use ArrayList** until you have measured
a real problem (and in a Beginner course you almost certainly have not).

**Next:** sets, maps, and the shape of lookups.
'''

L_LIST_VI = r'''
**Collections Framework** là hộp công cụ các cấu trúc dữ liệu có thể lớn lên
của Java. `List` là cái hằng ngày: một chuỗi có thứ tự, lớn lên được.

```java
import java.util.ArrayList;
import java.util.List;

List<String> names = new ArrayList<>();   // interface bên trái, hiện thực bên phải
names.add("Ada");
names.add("Grace");
names.add(1, "Linus");                    // chèn vào chỉ số 1
System.out.println(names.get(0));         // Ada
System.out.println(names.size());         // 3
System.out.println(names.remove("Ada"));  // true (đã xóa)
```

Khai báo kiểu **interface** (`List`), khởi tạo **hiện thực** (`ArrayList`).
Toàn bộ code gọi chỉ nhìn thấy interface; đổi sang `LinkedList` ngày mai chỉ
sửa đúng một dòng. `<String>` là **tham số kiểu generic** — sẽ nói kỹ sau,
nhưng nó đã trả tiền ngay: `names.get(0)` được biết tĩnh là String.

Các phương thức List cốt lõi: `add(e)`, `add(i, e)`, `get(i)`, `set(i, e)`,
`remove(i)`, `remove(Object)`, `size()`, `contains(e)`, `indexOf(e)`,
`isEmpty()`, `clear()`. Duyệt dùng for-each như với mảng:

```java
for (String n : names) { System.out.println(n); }
```

**ArrayList vs LinkedList** — câu hỏi phỏng vấn kinh điển, nói cho thật:
ArrayList là mảng tự phình; `get(i)` tức thì, chèn giữa dồn phần tử.
LinkedList là chuỗi liên kết; hai đầu rẻ, `get(i)` đi bộ từ đầu gần nhất.
Tóm tắt trung thực cho người mới: **dùng ArrayList** cho tới khi bạn đo được
một bài toán thật (và trong khóa Cơ bản thì hầu như chưa).

**Tiếp theo:** set, map, và hình dạng của tra cứu.
'''

L_SETMAP_EN = r'''
**Set** — no duplicates, no order promises (HashSet):

```java
Set<Integer> seen = new HashSet<>();
seen.add(1);
seen.add(1);                    // ignored: add returns false
System.out.println(seen.size()); // 1
```

Membership tests are the point: `contains` on a HashSet is effectively
instant regardless of size — it buckets by hash code. "Have I processed
this id before?" is a Set question, not a List scan.

**Map** — key → value pairs (HashMap):

```java
Map<String, Integer> stock = new HashMap<>();
stock.put("pen", 12);
stock.put("book", 3);
stock.get("pen");               // 12
stock.getOrDefault("ink", 0);   // 0 — no missing-key surprise
stock.containsKey("book");      // true
stock.remove("pen");

for (var entry : stock.entrySet()) {          // both halves
    System.out.println(entry.getKey() + "=" + entry.getValue());
}
for (String key : stock.keySet()) { /* keys */ }
for (int qty : stock.values())    { /* values */ }
```

`get` on a missing key returns `null` — with primitive-like wrapper types
(`Integer` here) that null can NPE on unboxing later. `getOrDefault` and
`containsKey` are the defensive reads. Note `var` (Java 10+): local type
inference when the right-hand side makes the type obvious.

**Choosing, in one table:**

| Need | Structure |
|---|---|
| ordered sequence, index access | `ArrayList` |
| unique members, fast contains | `HashSet` (or `LinkedHashSet` to keep insertion order) |
| key → value lookup | `HashMap` (or `TreeMap` for sorted keys) |
| first-in-first-out processing | `ArrayDeque` as a queue |
| undo / recent items | `ArrayDeque` as a stack (`push`/`pop`) |

**Next:** what the `<…>` actually means.
'''

L_SETMAP_VI = r'''
**Set** — không trùng lặp, không hứa thứ tự (HashSet):

```java
Set<Integer> seen = new HashSet<>();
seen.add(1);
seen.add(1);                    // bị bỏ qua: add trả false
System.out.println(seen.size()); // 1
```

Điểm giá trị nằm ở phép kiểm thành viên: `contains` trên HashSet nhanh gần
như tức thì bất kể kích thước — nó xếp bucket theo hash code. "Id này tôi
đã xử lý chưa?" là câu hỏi của Set, không phải của việc quét List.

**Map** — cặp khóa → giá trị (HashMap):

```java
Map<String, Integer> stock = new HashMap<>();
stock.put("pen", 12);
stock.put("book", 3);
stock.get("pen");               // 12
stock.getOrDefault("ink", 0);   // 0 — không bất ngờ khi thiếu khóa
stock.containsKey("book");      // true
stock.remove("pen");

for (var entry : stock.entrySet()) {          // cả hai nửa
    System.out.println(entry.getKey() + "=" + entry.getValue());
}
for (String key : stock.keySet()) { /* khóa */ }
for (int qty : stock.values())    { /* giá trị */ }
```

`get` với khóa thiếu trả `null` — với các kiểu wrapper (`Integer` ở đây),
null đó có thể NPE lúc unboxing sau này. `getOrDefault` và `containsKey`
là cách đọc phòng thủ. Chú ý `var` (Java 10+): suy luận kiểu cục bộ khi
vế phải đã nói rõ kiểu.

**Chọn cấu trúc, gói trong một bảng:**

| Nhu cầu | Cấu trúc |
|---|---|
| chuỗi có thứ tự, truy cập theo chỉ số | `ArrayList` |
| thành viên duy nhất, contains nhanh | `HashSet` (hoặc `LinkedHashSet` giữ thứ tự thêm vào) |
| tra cứu khóa → giá trị | `HashMap` (hoặc `TreeMap` khi cần khóa có thứ tự) |
| xử lý vào-trước-ra-trước | `ArrayDeque` làm hàng đợi |
| undo / các mục gần đây | `ArrayDeque` làm ngăn xếp (`push`/`pop`) |

**Tiếp theo:** `<…>` thực chất là gì.
'''

L_GENERICS_EN = r'''
Generic type parameters (`<T>`) are how Java collections stay type-safe —
and how you write your own reusable containers.

**Using them**, you already do: `List<String>`, `Map<String, Integer>`. The
compiler stops `list.add(42)` on a `List<String>` at compile time, and
eliminates casts on the way out. Before generics (Java 4 and earlier),
everything was `Object` and every read was a risky downcast — generics
moved those crashes from runtime to the compiler.

**Writing them** is one angle-bracket declaration:

```java
class Box<T> {                       // T: a type filled in later
    private T value;

    public void put(T v) { value = v; }
    public T get() { return value; }
}

Box<String> words = new Box<>();
words.put("hi");                     // compile-checked
String s = words.get();              // no cast
```

**Generic methods** declare their own type parameter before the return
type:

```java
static <T> T firstOrNull(List<T> list) {
    return list.isEmpty() ? null : list.get(0);
}
```

Call it with `List<String>` and T becomes String; with `List<Integer>` and
T becomes Integer — one method, every element type, no duplication.

**Bounded types** constrain T when behavior needs a guarantee:

```java
static <T extends Comparable<T>> T maxOf(List<T> items) {
    T best = items.get(0);
    for (T item : items) {
        if (item.compareTo(best) > 0) best = item;
    }
    return best;
}
```

`T extends Comparable<T>` reads "any type that knows how to compare itself"
— inside, `compareTo` is legal. Bounds are the beginner-safe half of
generics; wildcards (`? extends`, `? super`) and variance belong to
Intermediate — this course deliberately stops at bounds.

**Next:** exceptions.
'''

L_GENERICS_VI = r'''
Tham số kiểu generic (`<T>`) là cách collection của Java giữ an toàn kiểu —
và cách bạn viết container tái sử dụng của riêng mình.

**Dùng**, bạn đã làm rồi: `List<String>`, `Map<String, Integer>`. Compiler
chặn `list.add(42)` trên một `List<String>` ngay lúc biên dịch, và xóa bỏ
cast khi đọc ra. Trước thời đại generic (Java 4 trở về trước), mọi thứ là
`Object` và mọi lần đọc là một cast mạo hiểm — generic chuyển những cú
ngã đó từ runtime về compiler.

**Viết** chỉ cần một khai báo trong ngoặc nhọn:

```java
class Box<T> {                       // T: một kiểu sẽ được điền sau
    private T value;

    public void put(T v) { value = v; }
    public T get() { return value; }
}

Box<String> words = new Box<>();
words.put("hi");                     // được kiểm tra lúc biên dịch
String s = words.get();              // không cần cast
```

**Phương thức generic** tự khai báo tham số kiểu ngay trước kiểu trả về:

```java
static <T> T firstOrNull(List<T> list) {
    return list.isEmpty() ? null : list.get(0);
}
```

Gọi với `List<String>` thì T thành String; với `List<Integer>` thì T thành
Integer — một phương thức, mọi kiểu phần tử, không sao chép.

**Kiểu có giới hạn (bounded)** ràng buộc T khi hành vi cần một lời bảo đảm:

```java
static <T extends Comparable<T>> T maxOf(List<T> items) {
    T best = items.get(0);
    for (T item : items) {
        if (item.compareTo(best) > 0) best = item;
    }
    return best;
}
```

`T extends Comparable<T>` đọc là "bất kỳ kiểu nào biết tự so sánh" — bên
trong, `compareTo` là hợp lệ. Bounds là nửa an-toàn-người-mới của generic;
wildcard (`? extends`, `? super`) và variance thuộc về Trung cấp — khóa này
cố tình dừng ở bounds.

**Tiếp theo:** exception.
'''

# ── practice set 10 ─────────────────────────────────────────────────────────
P10_STOCK = challenge(
    "javb-m10-stock-ledger",
    "Stock ledger",
    "Implement `static int totalQuantity(java.util.List<Integer> quantities)` "
    "(sum of a List — generics in action) and `static java.util.Map<String, "
    "Integer> mergeStock(java.util.Map<String, Integer> a, java.util.Map<String, "
    "Integer> b)` returning a NEW map with quantities summed per key.",
    r'''public class Solution {
    public static int totalQuantity(java.util.List<Integer> quantities) {
        return 0;
    }

    public static java.util.Map<String, Integer> mergeStock(
            java.util.Map<String, Integer> a, java.util.Map<String, Integer> b) {
        return null;
    }
}
''',
    [
        (
            "list summation",
            r"""
CjTestBase.checkEq(Solution.totalQuantity(java.util.List.of(2, 3, 5)), 10, "2+3+5");
CjTestBase.checkEq(Solution.totalQuantity(java.util.List.of()), 0, "empty list");
""",
            "for-each over the list; empty list sums to 0.",
        ),
        (
            "map merging",
            r"""
java.util.Map<String, Integer> a = java.util.Map.of("pen", 2, "book", 1);
java.util.Map<String, Integer> b = java.util.Map.of("pen", 3, "ink", 5);
java.util.Map<String, Integer> out = Solution.mergeStock(a, b);
CjTestBase.checkEq(out.get("pen"), 5, "2+3 pens");
CjTestBase.checkEq(out.get("book"), 1, "book untouched");
CjTestBase.checkEq(out.get("ink"), 5, "ink added");
""",
            "Copy a, then add b's entries with getOrDefault.",
        ),
        (
            "no mutation of inputs",
            r"""
java.util.Map<String, Integer> a = new java.util.HashMap<>();
a.put("pen", 2);
Solution.mergeStock(a, java.util.Map.of("ink", 1));
CjTestBase.checkEq(a.size(), 1, "input map untouched");
""",
            "Build a new map; never write into the parameters.",
        ),
    ],
    level="independent",
)

P10_STOCK_VI = vi_challenge(
    "Sổ tồn kho",
    "Viết `static int totalQuantity(java.util.List<Integer> quantities)` "
    "(tổng của một List — generic tại chỗ làm) và `static java.util.Map<String, "
    "Integer> mergeStock(...)` trả một map MỚI với số lượng cộng theo từng khóa.",
    [
        ("list summation", "for-each trên list; list rỗng cho tổng 0."),
        ("map merging", "Sao chép a, rồi cộng các mục của b bằng getOrDefault."),
        ("no mutation of inputs", "Dựng map mới; không bao giờ ghi vào tham số."),
    ],
)

P10_UNIQUE = challenge(
    "javb-m10-unique-words",
    "Unique words and their counts",
    "Implement `static int distinctWords(String sentence)` (whitespace-split, "
    "case-insensitive) and `static java.util.Map<String, Integer> wordCounts("
    "String sentence)` mapping each lowercase word to its count.",
    r'''public class Solution {
    public static int distinctWords(String sentence) {
        return 0;
    }

    public static java.util.Map<String, Integer> wordCounts(String sentence) {
        return null;
    }
}
''',
    [
        (
            "distinct counting",
            r"""
CjTestBase.checkEq(Solution.distinctWords("the cat THE dog"), 3, "case-insensitive distinct");
CjTestBase.checkEq(Solution.distinctWords(""), 0, "empty");
""",
            "Lowercase, split on \\s+, collect into a HashSet.",
        ),
        (
            "word counts",
            r"""
java.util.Map<String, Integer> counts = Solution.wordCounts("a b a c b a");
CjTestBase.checkEq(counts.get("a"), 3, "three a's");
CjTestBase.checkEq(counts.get("b"), 2, "two b's");
CjTestBase.checkEq(counts.getOrDefault("z", 0), 0, "no z");
""",
            "The classic counting map: getOrDefault(key, 0) + 1.",
        ),
    ],
    level="guided",
)

P10_UNIQUE_VI = vi_challenge(
    "Từ duy nhất và tần suất",
    "Viết `static int distinctWords(String sentence)` (tách theo khoảng trắng, "
    "không phân biệt hoa thường) và `static java.util.Map<String, Integer> "
    "wordCounts(String sentence)` ánh xạ mỗi từ viết thường sang số lần xuất hiện.",
    [
        ("distinct counting", "Viết thường, tách theo \\s+, thu vào HashSet."),
        ("word counts", "Bộ đếm map kinh điển: getOrDefault(key, 0) + 1."),
    ],
)

P10_BOX = challenge(
    "javb-m10-generic-box",
    "Your own generic Box",
    "Implement `static class Box<T>` with `private T value`, `put(T)`, "
    "`get()`, `isEmpty()`, and `static <T> Box<T> of(T value)` factory. "
    "Also implement `static <T extends Comparable<T>> T maxOf(java.util.List<T> "
    "items)` using the bound.",
    r'''public class Solution {
    public static class Box<T> {
        public void put(T v) {
        }

        public T get() {
            return null;
        }

        public boolean isEmpty() {
            return false;
        }
    }

    public static <T> Box<T> of(T value) {
        return null;
    }

    public static <T extends Comparable<T>> T maxOf(java.util.List<T> items) {
        return null;
    }
}
''',
    [
        (
            "box behavior",
            r"""
Solution.Box<String> box = new Solution.Box<>();
CjTestBase.checkTrue(box.isEmpty(), "starts empty");
box.put("pearl");
CjTestBase.checkEq(box.get(), "pearl", "stored value");
CjTestBase.checkTrue(!box.isEmpty(), "no longer empty");
""",
            "isEmpty depends on whether a value was ever put.",
        ),
        (
            "factory",
            r"""
Solution.Box<Integer> box = Solution.of(7);
CjTestBase.checkEq(box.get(), 7, "of(7)");
""",
            "of() constructs and puts in one step.",
        ),
        (
            "bounded maxOf",
            r"""
CjTestBase.checkEq(Solution.maxOf(java.util.List.of(3, 9, 4)), 9, "max of ints");
CjTestBase.checkEq(Solution.maxOf(java.util.List.of("apple", "pear")), "pear", "max of strings");
""",
            "One method, any Comparable type — that is the bound at work.",
        ),
    ],
    level="combination",
)

P10_BOX_VI = vi_challenge(
    "Generic Box của chính bạn",
    "Viết `static class Box<T>` với `private T value`, `put(T)`, `get()`, "
    "`isEmpty()`, và factory `static <T> Box<T> of(T value)`. Cùng viết "
    "`static <T extends Comparable<T>> T maxOf(java.util.List<T> items)` "
    "dùng bound.",
    [
        ("box behavior", "isEmpty phụ thuộc việc đã put giá trị nào chưa."),
        ("factory", "of() tạo và put trong một bước."),
        ("bounded maxOf", "Một phương thức, mọi kiểu Comparable — đó là tác dụng của bound."),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M10_MD = r'''
The Contact Book — collections composing.

Inside `Solution`, using collections throughout:

1. `static java.util.List<String> sortedUnique(java.util.List<String> raw)` —
   distinct names, case-insensitively, returned ALPHABETICALLY (lowercase
   order); keep the lowercase form in the result.
2. `static java.util.Map<Character, Integer> initialCounts(java.util.List<String>
   names)` — map from first letter (lowercase) to how many names start
   with it.
3. `record Contact(String name, java.util.List<String> phones) { }` with a
   compact constructor rejecting blank names; and
   `static String findPhone(java.util.List<Contact> contacts, String name)`
   — case-insensitive lookup returning the FIRST phone of the matching
   contact, `null` when the name is unknown.
'''

CK_M10_MD_VI = r'''
Sổ danh bạ — các collection ghép với nhau.

Bên trong `Solution`, dùng collection xuyên suốt:

1. `static java.util.List<String> sortedUnique(java.util.List<String> raw)` —
   các tên phân biệt, không phân biệt hoa thường, trả về theo THỨ TỰ ABC
   (dạng viết thường); giữ dạng viết thường trong kết quả.
2. `static java.util.Map<Character, Integer> initialCounts(java.util.List<String>
   names)` — map từ chữ cái đầu (viết thường) sang số tên bắt đầu bằng nó.
3. `record Contact(String name, java.util.List<String> phones) { }` với
   compact constructor từ chối tên rỗng; và
   `static String findPhone(java.util.List<Contact> contacts, String name)`
   — tra không phân biệt hoa thường, trả điện thoại ĐẦU TIÊN của contact
   khớp, `null` khi không biết tên.
'''

CK_M10_CH = challenge(
    "javb-checkpoint-collections",
    "Checkpoint: Contact Book",
    CK_M10_MD,
    r'''public class Solution {
    public static java.util.List<String> sortedUnique(java.util.List<String> raw) {
        return null;
    }

    public static java.util.Map<Character, Integer> initialCounts(java.util.List<String> names) {
        return null;
    }

    public record Contact(String name, java.util.List<String> phones) {
        public Contact {
        }
    }

    public static String findPhone(java.util.List<Contact> contacts, String name) {
        return null;
    }
}
''',
    [
        (
            "sorted unique names",
            r"""
java.util.List<String> out = Solution.sortedUnique(java.util.List.of("BO", "ada", "bo", "Cat"));
CjTestBase.checkEq(out, java.util.List.of("ada", "bo", "cat"), "distinct + sorted");
""",
            "Lowercase, dedupe with a set, sort.",
        ),
        (
            "initial letter counts",
            r"""
java.util.Map<Character, Integer> m =
    Solution.initialCounts(java.util.List.of("ada", "alan", "bo"));
CjTestBase.checkEq(m.get('a'), 2, "two a-names");
CjTestBase.checkEq(m.get('b'), 1, "one b-name");
""",
            "First letter of each lowercased name.",
        ),
        (
            "contact lookup",
            r"""
java.util.List<Solution.Contact> contacts = java.util.List.of(
    new Solution.Contact("Ada", java.util.List.of("111", "222")),
    new Solution.Contact("Bo", java.util.List.of("333")));
CjTestBase.checkEq(Solution.findPhone(contacts, "ada"), "111", "first phone wins");
CjTestBase.checkEq(Solution.findPhone(contacts, "BO"), "333", "case-insensitive name");
CjTestBase.checkTrue(Solution.findPhone(contacts, "Cy") == null, "unknown name");
CjTestBase.checkThrows(() -> new Solution.Contact("  ", java.util.List.of()), "blank name rejected");
""",
            "equals/equalsIgnoreCase on the name; first phone of the match.",
        ),
    ],
    difficulty="beginner",
)

CK_M10_VI = vi_challenge(
    "Checkpoint: Sổ danh bạ",
    CK_M10_MD_VI,
    [
        ("sorted unique names", "Viết thường, khử trùng lặp bằng set, sắp xếp."),
        ("initial letter counts", "Chữ cái đầu của mỗi tên đã viết thường."),
        ("contact lookup", "So tên không phân biệt hoa thường; điện thoại đầu tiên của contact khớp."),
    ],
)

CK_M10_R = r'''public class Solution {
    public static java.util.List<String> sortedUnique(java.util.List<String> raw) {
        java.util.TreeSet<String> set = new java.util.TreeSet<>();
        for (String name : raw) {
            if (name != null && !name.isBlank()) {
                set.add(name.trim().toLowerCase());
            }
        }
        return new java.util.ArrayList<>(set);
    }

    public static java.util.Map<Character, Integer> initialCounts(java.util.List<String> names) {
        java.util.Map<Character, Integer> counts = new java.util.HashMap<>();
        for (String name : names) {
            if (name == null || name.isBlank()) continue;
            char first = Character.toLowerCase(name.trim().charAt(0));
            counts.merge(first, 1, Integer::sum);
        }
        return counts;
    }

    public record Contact(String name, java.util.List<String> phones) {
        public Contact {
            if (name == null || name.isBlank()) {
                throw new IllegalArgumentException("name required");
            }
            phones = java.util.List.copyOf(phones);
        }
    }

    public static String findPhone(java.util.List<Contact> contacts, String name) {
        for (Contact c : contacts) {
            if (c.name().equalsIgnoreCase(name)) {
                return c.phones().isEmpty() ? null : c.phones().get(0);
            }
        }
        return null;
    }
}
'''

CK_M10_W = r'''public class Solution {
    public static java.util.List<String> sortedUnique(java.util.List<String> raw) {
        java.util.TreeSet<String> set = new java.util.TreeSet<>();
        for (String name : raw) {
            if (name != null && !name.isBlank()) {
                set.add(name.trim().toLowerCase());
            }
        }
        return new java.util.ArrayList<>(set);
    }

    public static java.util.Map<Character, Integer> initialCounts(java.util.List<String> names) {
        java.util.Map<Character, Integer> counts = new java.util.HashMap<>();
        for (String name : names) {
            if (name == null || name.isBlank()) continue;
            char first = Character.toLowerCase(name.trim().charAt(0));
            counts.merge(first, 1, Integer::sum);
        }
        return counts;
    }

    public record Contact(String name, java.util.List<String> phones) {
        public Contact {
            if (name == null || name.isBlank()) {
                throw new IllegalArgumentException("name required");
            }
            phones = java.util.List.copyOf(phones);
        }
    }

    public static String findPhone(java.util.List<Contact> contacts, String name) {
        for (Contact c : contacts) {
            // BUG: case-sensitive equality — "BO" never finds "Bo"
            if (c.name().equals(name)) {
                return c.phones().isEmpty() ? null : c.phones().get(0);
            }
        }
        return null;
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Collections & Generics",
    "List, Set, Map, and Deque in practice; generic type parameters, your own generic types, and bounded methods.",
    "Collection & Generic",
    "List, Set, Map, và Deque trong thực chiến; tham số kiểu generic, kiểu generic tự viết, và phương thức có bound.",
    ["list-and-arraylist", "set-map-deque", "generics-bounds", "java-checkpoint-collections"],
    ["javb-p10-collections"],
)

write_lesson(
    MOD, "list-and-arraylist",
    "List & ArrayList",
    "Interface vs implementation, the core methods, ArrayList vs LinkedList honestly.", 20,
    L_LIST_EN,
    "List & ArrayList",
    "Interface vs hiện thực, các phương thức cốt lõi, ArrayList vs LinkedList nói cho thật.",
    L_LIST_VI,
)

write_lesson(
    MOD, "set-map-deque",
    "Set, Map & Deque",
    "Membership, key-value lookups, defensive reads, and the choosing table.", 20,
    L_SETMAP_EN,
    "Set, Map & Deque",
    "Kiểm thành viên, tra khóa–giá trị, cách đọc phòng thủ, và bảng chọn cấu trúc.",
    L_SETMAP_VI,
)

write_lesson(
    MOD, "generics-bounds",
    "Generics & Bounded Types",
    "Type parameters, your own Box<T>, generic methods, and T extends Comparable<T>.", 20,
    L_GENERICS_EN,
    "Generic & kiểu có giới hạn",
    "Tham số kiểu, Box<T> tự viết, phương thức generic, và T extends Comparable<T>.",
    L_GENERICS_VI,
)

write_practice(
    MOD, "javb-p10-collections",
    "Practice: Collections at Work",
    "A stock ledger of maps, word counting, and a hand-rolled generic Box with a bounded max.",
    "Thực hành: Collection tại chỗ làm",
    "Sổ tồn kho bằng map, đếm từ, và một generic Box tự viết cùng max có bound.",
    "generics-bounds", 50, "beginner",
    [P10_STOCK, P10_UNIQUE, P10_BOX],
    {c["id"]: v for c, v in [(P10_STOCK, P10_STOCK_VI), (P10_UNIQUE, P10_UNIQUE_VI), (P10_BOX, P10_BOX_VI)]},
    solutions=[
        (
            P10_STOCK["id"],
            r'''public class Solution {
    public static int totalQuantity(java.util.List<Integer> quantities) {
        int total = 0;
        for (int q : quantities) {
            total += q;
        }
        return total;
    }

    public static java.util.Map<String, Integer> mergeStock(
            java.util.Map<String, Integer> a, java.util.Map<String, Integer> b) {
        java.util.Map<String, Integer> out = new java.util.HashMap<>(a);
        for (var entry : b.entrySet()) {
            out.merge(entry.getKey(), entry.getValue(), Integer::sum);
        }
        return out;
    }
}
''',
            r'''public class Solution {
    public static int totalQuantity(java.util.List<Integer> quantities) {
        int total = 0;
        for (int q : quantities) {
            total += q;
        }
        return total;
    }

    public static java.util.Map<String, Integer> mergeStock(
            java.util.Map<String, Integer> a, java.util.Map<String, Integer> b) {
        // BUG: mutates the first input instead of building a new map
        java.util.Map<String, Integer> out = a;
        for (var entry : b.entrySet()) {
            out.merge(entry.getKey(), entry.getValue(), Integer::sum);
        }
        return out;
    }
}
''',
        ),
        (
            P10_UNIQUE["id"],
            r'''public class Solution {
    public static int distinctWords(String sentence) {
        if (sentence == null || sentence.isBlank()) return 0;
        java.util.Set<String> words = new java.util.HashSet<>();
        for (String w : sentence.toLowerCase().trim().split("\\s+")) {
            words.add(w);
        }
        return words.size();
    }

    public static java.util.Map<String, Integer> wordCounts(String sentence) {
        java.util.Map<String, Integer> counts = new java.util.HashMap<>();
        if (sentence == null || sentence.isBlank()) return counts;
        for (String w : sentence.toLowerCase().trim().split("\\s+")) {
            counts.merge(w, 1, Integer::sum);
        }
        return counts;
    }
}
''',
            r'''public class Solution {
    public static int distinctWords(String sentence) {
        if (sentence == null || sentence.isBlank()) return 0;
        java.util.Set<String> words = new java.util.HashSet<>();
        for (String w : sentence.toLowerCase().trim().split("\\s+")) {
            words.add(w);
        }
        return words.size();
    }

    public static java.util.Map<String, Integer> wordCounts(String sentence) {
        java.util.Map<String, Integer> counts = new java.util.HashMap<>();
        if (sentence == null || sentence.isBlank()) return counts;
        for (String w : sentence.toLowerCase().trim().split("\\s+")) {
            // BUG: overwrites instead of accumulating — counts are always 1
            counts.put(w, 1);
        }
        return counts;
    }
}
''',
        ),
        (
            P10_BOX["id"],
            r'''public class Solution {
    public static class Box<T> {
        private T value;

        public void put(T v) { this.value = v; }
        public T get() { return value; }
        public boolean isEmpty() { return value == null; }
    }

    public static <T> Box<T> of(T value) {
        Box<T> box = new Box<>();
        box.put(value);
        return box;
    }

    public static <T extends Comparable<T>> T maxOf(java.util.List<T> items) {
        T best = items.get(0);
        for (T item : items) {
            if (item.compareTo(best) > 0) best = item;
        }
        return best;
    }
}
''',
            r'''public class Solution {
    public static class Box<T> {
        private T value;

        public void put(T v) { this.value = v; }
        public T get() { return value; }
        public boolean isEmpty() { return value == null; }
    }

    public static <T> Box<T> of(T value) {
        Box<T> box = new Box<>();
        box.put(value);
        return box;
    }

    public static <T extends Comparable<T>> T maxOf(java.util.List<T> items) {
        // BUG: comparison reversed — returns the MIN
        T best = items.get(0);
        for (T item : items) {
            if (item.compareTo(best) < 0) best = item;
        }
        return best;
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-collections",
    "Checkpoint: Contact Book",
    "Sets, maps, records, and case-insensitive lookups composing into one small address book.", 50, CK_M10_MD,
    "Checkpoint: Sổ danh bạ",
    "Set, map, record, và tra cứu không phân biệt hoa thường ghép thành một sổ địa chỉ nhỏ.",
    CK_M10_MD_VI,
    CK_M10_CH, CK_M10_VI,
    solution=CK_M10_R, wrong=CK_M10_W,
)

print("module 10 complete")
