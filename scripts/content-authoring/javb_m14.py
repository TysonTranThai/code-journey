#!/usr/bin/env python3
"""Java - Beginner - Module 14: java-files-capstone.

Real file I/O with java.nio.file (taught honestly: the sandbox grades via
string-content functions so tests stay deterministic), then the course
capstone: a personal transaction ledger integrating collections, records,
defensive parsing, and streams. House contract.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-files-capstone"

# ── lesson 14.1 — files with java.nio.file ──────────────────────────────────
L_FILES_EN = r"""
Everything you've written so far dies when the program ends. Files make
data outlive the process. Modern Java does file I/O with the
`java.nio.file` API - two classes carry almost everything: `Path` (a
*reference* to a file) and `Files` (the *operations* on it).

```java
import java.nio.file.Files;
import java.nio.file.Path;

Path notes = Path.of("notes.txt");

// write (replaces the file)
Files.writeString(notes, "first line\nsecond line\n");

// read whole file as one String
String content = Files.readString(notes);

// read as a list of lines
java.util.List<String> lines = Files.readAllLines(notes);

// check before you act
if (Files.exists(notes)) { ... }
```

Every read/write method declares `throws IOException` - the *checked*
exception from Module 11 finally earning its keep: the compiler forces you
to decide what happens when the disk disagrees with you.

```java
try {
    String config = Files.readString(Path.of("config.txt"));
} catch (java.io.IOException e) {
    System.out.println("no config file, using defaults");
}
```

## Appending, walking, and the small print

```java
// append: CREATE first (if missing), then APPEND
Files.writeString(notes, "another line\n",
    java.nio.file.StandardOpenOption.CREATE,
    java.nio.file.StandardOpenOption.APPEND);

// visit every file under a directory
try (var walk = Files.walk(Path.of("logs"))) {
    walk.filter(p -> p.toString().endsWith(".txt"))
        .forEach(System.out::println);
}
```

`Files.walk` returns a stream - the try-with-resources block closes the
directory handle when done. And remember the defensive habits from the
parsing lesson: file content is *dirty data*. Every line you read gets
the same null-guard, trim, and parse-check treatment as a CSV import.
"""

L_FILES_VI = r"""
Mọi thứ bạn viết từ trước đến nay đều biến mất khi chương trình kết thúc.
File giúp dữ liệu sống lâu hơn tiến trình. Java hiện đại làm I/O file với
API `java.nio.file` - hai lớp gánh gần như mọi thứ: `Path` (*tham chiếu*
đến file) và `Files` (*các thao tác* trên nó).

```java
import java.nio.file.Files;
import java.nio.file.Path;

Path notes = Path.of("notes.txt");

// ghi (ghi đè file cũ)
Files.writeString(notes, "dòng đầu\ndòng hai\n");

// đọc cả file thành một String
String content = Files.readString(notes);

// đọc thành danh sách các dòng
java.util.List<String> lines = Files.readAllLines(notes);

// kiểm tra trước khi hành động
if (Files.exists(notes)) { ... }
```

Mọi phương thức đọc/ghi khai báo `throws IOException` - checked exception
từ Module 11 cuối cùng cũng phát huy tác dụng: compiler buộc bạn phải
quyết định điều gì xảy ra khi ổ đĩa không nghe lời bạn.

## Nối thêm, đi cây thư mục, và các chi tiết nhỏ

```java
// nối: CREATE trước (nếu chưa có), rồi APPEND
Files.writeString(notes, "dòng nữa\n",
    java.nio.file.StandardOpenOption.CREATE,
    java.nio.file.StandardOpenOption.APPEND);

// thăm mọi file dưới một thư mục
try (var walk = Files.walk(Path.of("logs"))) {
    walk.filter(p -> p.toString().endsWith(".txt"))
        .forEach(System.out::println);
}
```

`Files.walk` trả về một stream - khối try-with-resources đóng con trỏ thư
mục khi xong. Và nhớ các thói quen phòng thủ từ bài parsing: nội dung file
là *dữ liệu bẩn*. Mỗi dòng đọc được đều trải qua null-guard, trim,
parse-check như một đợt import CSV.
"""

# ── lesson 14.2 — capstone brief ────────────────────────────────────────────
L_CAP_EN = r"""
Time to assemble. The capstone is a **personal transaction ledger**: a
text-persisted record of money in and money out. Nothing here is new -
that's the point. It composes:

- **records** (Module 9) - an immutable `Transaction` with a compact
  constructor validating itself;
- **collections + streams** (Modules 10, 12) - a `List<Transaction>`
  queried with pipelines;
- **defensive parsing** (Module 11) - every loaded line survives a
  `try/catch` gauntlet;
- **file persistence** (this module) - save and load through
  `Files.writeString`/`readString`;
- **testing discipline** (Module 13) - the grading tests are the bar, and
  you've written your own all course.

## The format you're building

One transaction per line, four fields, `|`-separated:

```
2026-01-15|coffee|CASH_OUT|4.50
2026-01-16|salary|CASH_IN|2500.00
```

`CASH_IN` adds to the balance, `CASH_OUT` subtracts. That's the entire
schema - the complexity lives in *handling it well*.

## How the capstone is graded

You get requirements, tests, and hints - not a tutorial. The four test
blocks each fail until the matching behavior exists: validation, round-trip
persistence, filtering/summary queries, and balance arithmetic with
defensive guards. Build the `Ledger` methods one test block at a time;
when all four pass, the capstone is done and so is the course.

## Where you could go next

Java Intermediate would take you from this: generics you write (not just
read), inheritance hierarchies that pay rent, interfaces as contracts,
builder patterns, and the first real concurrency. The ledger is the
foundation those courses assume - finish it, understand every line, and
you've earned the title this course promised: someone who can write Java.
"""

L_CAP_VI = r"""
Đến giờ lắp ráp. Capstone là một **sổ giao dịch cá nhân**: bản ghi tiền
vào tiền ra được lưu trong file văn bản. Ở đây không có gì mới - và đó
chính là điểm. Nó kết hợp:

- **record** (Module 9) - `Transaction` bất biến với compact constructor
  tự kiểm tra;
- **collection + stream** (Module 10, 12) - một `List<Transaction>` được
  truy vấn bằng pipeline;
- **parse phòng thủ** (Module 11) - mọi dòng nạp về đều vượt cổng
  `try/catch`;
- **lưu file** (module này) - save và load qua
  `Files.writeString`/`readString`;
- **kỷ luật test** (Module 13) - các test chấm điểm chính là chuẩn, và
  bạn đã tự viết suốt khóa học.

## Định dạng bạn đang xây

Mỗi dòng một giao dịch, bốn trường, phân tách bằng `|`:

```
2026-01-15|coffee|CASH_OUT|4.50
2026-01-16|salary|CASH_IN|2500.00
```

`CASH_IN` cộng vào số dư, `CASH_OUT` trừ. Đó là toàn bộ schema - độ phức
tạp nằm ở chỗ *xử lý nó cho tốt*.

## Capstone được chấm thế nào

Bạn nhận yêu cầu, test, và gợi ý - không phải một bài hướng dẫn. Bốn khối
test lần lượt fail cho đến khi hành vi tương ứng tồn tại: validation,
round-trip lưu/nạp, truy vấn lọc/tổng hợp, và số học số dư có chặn phòng
thủ. Hãy xây các phương thức `Ledger` lần lượt theo từng khối test; khi
cả bốn pass, capstone hoàn thành và khóa học cũng vậy.

## Bạn có thể đi tiếp đâu

Java Intermediate sẽ đưa bạn đi xa hơn từ đây: generic do bạn viết (không
chỉ đọc), hệ kế thừa đáng tiền, interface như hợp đồng, builder pattern,
và bước đầu với concurrency. Sổ giao dịch này là nền mà các khóa sau giả
định bạn có - hoàn thành nó, hiểu từng dòng, và bạn đã xứng đáng với danh
hiệu khóa học này hứa: một người viết được Java.
"""

# ── challenges ───────────────────────────────────────────────────────────────
BOILER_TX = r"""public class Solution {
    public enum Direction { CASH_IN, CASH_OUT }

    public record Transaction(String date, String label, Direction direction, double amount) {
        public Transaction {
            if (date == null) {
                throw new IllegalArgumentException("date must not be null");
            }
            try {
                java.time.LocalDate.parse(date);   // real calendar: rejects 2026-13-40
            } catch (java.time.format.DateTimeParseException e) {
                throw new IllegalArgumentException("bad date: " + date);
            }
            if (label == null || label.isBlank()) {
                throw new IllegalArgumentException("label must not be blank");
            }
            if (amount <= 0) {
                throw new IllegalArgumentException("amount must be positive: " + amount);
            }
        }
    }

    public static Transaction parse(String line) {
        return null;
    }
}
"""

P14_TX = challenge(
    "javb-m14-parse-transaction",
    "Parse the ledger line",
    "Implement `parse(String line)` in the provided skeleton: split on `|` into exactly 4 fields; return `new Transaction(date, label, Direction.valueOf(field.toUpperCase()), Double.parseDouble(amount))`. The record's compact constructor already validates - let its exceptions propagate unchanged (callers need the real reason).",
    BOILER_TX,
    [
        (
            "valid lines parse",
            r"""
Solution.Transaction t = Solution.parse("2026-01-15|coffee|CASH_OUT|4.50");
CjTestBase.checkEq(t.date(), "2026-01-15", "date kept");
CjTestBase.checkEq(t.direction(), Solution.Direction.CASH_OUT, "direction parsed");
CjTestBase.checkEq(t.amount(), 4.5, "amount parsed");
""",
            "split(\"\\|\") - the pipe is a regex metacharacter and must be escaped.",
        ),
        (
            "lowercase direction is accepted",
            r"""
CjTestBase.checkEq(Solution.parse("2026-01-16|salary|cash_in|2500.00").direction(),
    Solution.Direction.CASH_IN, "case-insensitive direction");
""",
            "field.toUpperCase() before Direction.valueOf.",
        ),
        (
            "bad lines throw the record's exception",
            r"""
try {
    Solution.parse("2026-13-40|coffee|CASH_OUT|4.50");
    CjTestBase.checkTrue(false, "impossible date must throw");
} catch (IllegalArgumentException e) {
    CjTestBase.checkTrue(true, "record validation fired");
}
try {
    Solution.parse("2026-01-15|coffee|CASH_OUT|-1");
    CjTestBase.checkTrue(false, "negative amount must throw");
} catch (IllegalArgumentException e) {
    CjTestBase.checkTrue(true, "amount validation fired");
}
""",
            "Don't catch inside parse - the constructor already throws the right thing.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

P14_TX_VI = vi_challenge(
    "Parse dòng sổ giao dịch",
    "Cài đặt `parse(String line)` trong khung có sẵn: tách theo `|` thành đúng 4 trường; trả về `new Transaction(date, label, Direction.valueOf(field.toUpperCase()), Double.parseDouble(amount))`. Compact constructor của record đã kiểm tra sẵn - để exception của nó lan truyền nguyên vẹn (caller cần lý do thật).",
    [("dòng hợp lệ được parse", "split(\"\\|\") - dấu gạch là ký tự đặc biệt của regex nên phải escape."),
     ("direction viết thường vẫn nhận", "field.toUpperCase() trước Direction.valueOf."),
     ("dòng xấu ném exception của record", "Đừng bắt exception trong parse - constructor đã ném đúng thứ cần ném.")],
)

# ── checkpoint: the capstone ─────────────────────────────────────────────────
BOILER_LEDGER = r"""public class Solution {
    public enum Direction { CASH_IN, CASH_OUT }

    public record Transaction(String date, String label, Direction direction, double amount) {
        public Transaction {
            if (date == null) {
                throw new IllegalArgumentException("date must not be null");
            }
            try {
                java.time.LocalDate.parse(date);   // real calendar: rejects 2026-13-40
            } catch (java.time.format.DateTimeParseException e) {
                throw new IllegalArgumentException("bad date: " + date);
            }
            if (label == null || label.isBlank()) {
                throw new IllegalArgumentException("label must not be blank");
            }
            if (amount <= 0) {
                throw new IllegalArgumentException("amount must be positive: " + amount);
            }
        }
    }

    public static class Ledger {
        private final java.util.List<Transaction> txs = new java.util.ArrayList<>();

        public void add(Transaction t) { txs.add(t); }

        public int count(java.util.function.Predicate<Transaction> p) {
            return (int) txs.stream().filter(p).count();
        }

        public double net(String datePrefix) {
            return 0;
        }

        public java.util.List<String> labelsSince(String datePrefix) {
            return java.util.List.of();
        }

        public java.util.List<String> saveLines() {
            return java.util.List.of();
        }

        public void loadLine(String line) {
        }
    }
}
"""

P14_CP_CH = challenge(
    "javb-m14-cp-ledger",
    "Capstone: the personal ledger",
    "Finish the `Ledger` class. `net(datePrefix)` = sum of amounts with sign by direction, counting only transactions whose date starts with the prefix (use `\"\"` for all). `labelsSince(datePrefix)` = labels of matching transactions, in insertion order, uppercase. `saveLines()` = every transaction rendered as `date|label|DIRECTION|amount` with exactly two decimal places, insertion order. `loadLine(line)` = parse one saved line and add it - but a malformed line must not corrupt the ledger: skip it silently if it fails the record's validation.",
    BOILER_LEDGER,
    [
        (
            "net sums signed by direction and filters by date prefix",
            r"""
Solution.Ledger l = new Solution.Ledger();
l.add(new Solution.Transaction("2026-01-15", "coffee", Solution.Direction.CASH_OUT, 4.50));
l.add(new Solution.Transaction("2026-01-16", "salary", Solution.Direction.CASH_IN, 2500.00));
l.add(new Solution.Transaction("2026-02-01", "rent", Solution.Direction.CASH_OUT, 1200.00));
CjTestBase.checkEq(l.net(""), 1295.5, "2500 - 4.5 - 1200");
CjTestBase.checkEq(l.net("2026-01"), 2495.5, "january only");
CjTestBase.checkEq(l.net("2026-03"), 0.0, "quiet month");
""",
            "map sign by direction, filter by date.startsWith(prefix), sum into a double.",
        ),
        (
            "labels are uppercase, insertion order",
            r"""
Solution.Ledger l = new Solution.Ledger();
l.add(new Solution.Transaction("2026-01-15", "coffee", Solution.Direction.CASH_OUT, 4.50));
l.add(new Solution.Transaction("2026-01-16", "salary", Solution.Direction.CASH_IN, 2500.00));
CjTestBase.checkEq(l.labelsSince("2026-01"), java.util.List.of("COFFEE", "SALARY"), "january labels");
""",
            "filter, then map(String::toUpperCase) BEFORE collecting.",
        ),
        (
            "save renders two decimals in order",
            r"""
Solution.Ledger l = new Solution.Ledger();
l.add(new Solution.Transaction("2026-01-15", "coffee", Solution.Direction.CASH_OUT, 4.5));
l.add(new Solution.Transaction("2026-01-16", "salary", Solution.Direction.CASH_IN, 2500));
CjTestBase.checkEq(l.saveLines(), java.util.List.of(
    "2026-01-15|coffee|CASH_OUT|4.50",
    "2026-01-16|salary|CASH_IN|2500.00"), "canonical save format");
""",
            "String.format(\"%s|%s|%s|%.2f\", ...) - %.2f gives exactly two decimals.",
        ),
        (
            "load round-trips, junk is skipped silently",
            r"""
Solution.Ledger l = new Solution.Ledger();
l.loadLine("2026-01-15|coffee|CASH_OUT|4.50");
l.loadLine("garbage line");
l.loadLine("2026-13-40|impossible date|CASH_OUT|1.00");
l.loadLine("2026-02-01|rent|CASH_OUT|1200.00");
CjTestBase.checkEq(l.saveLines(), java.util.List.of(
    "2026-01-15|coffee|CASH_OUT|4.50",
    "2026-02-01|rent|CASH_OUT|1200.00"), "two survivors, junk skipped");
CjTestBase.checkEq(l.net(""), -1204.5, "survivors contribute to balance");
""",
            "try { add(parse-like code) } catch (IllegalArgumentException e) { /* skip */ } - never let one bad line crash the load.",
        ),
    ],
    level="real-world",
    difficulty="advanced",
)

P14_CP_VI = vi_challenge(
    "Capstone: sổ giao dịch cá nhân",
    "Hoàn thiện lớp `Ledger`. `net(datePrefix)` = tổng các khoản theo dấu của direction, chỉ đếm giao dịch có ngày bắt đầu bằng prefix (dùng `\"\"` cho tất cả). `labelsSince(datePrefix)` = label của các giao dịch khớp, theo thứ tự thêm vào, viết hoa. `saveLines()` = mọi giao dịch render thành `date|label|DIRECTION|amount` với đúng hai chữ số thập phân, theo thứ tự thêm vào. `loadLine(line)` = parse một dòng đã lưu và thêm vào - nhưng dòng lỗi không được làm hỏng sổ: bỏ qua im lặng nếu nó fails validation của record.",
    [("net cộng có dấu theo direction và lọc theo prefix ngày", "map dấu theo direction, lọc theo date.startsWith(prefix), cộng vào một double."),
     ("label viết hoa, đúng thứ tự thêm vào", "filter, rồi map(String::toUpperCase) TRƯỚC khi collect."),
     ("save render hai chữ số thập phân đúng thứ tự", "String.format(\"%s|%s|%s|%.2f\", ...) - %.2f cho đúng hai chữ số."),
     ("load round-trip, rác bị bỏ qua im lặng", "try { add(code-parse) } catch (IllegalArgumentException e) { /* bỏ qua */ } - đừng để một dòng xấu làm sập cả lần nạp.")],
)

P14_CP_R = r"""public class Solution {
    public enum Direction { CASH_IN, CASH_OUT }

    public record Transaction(String date, String label, Direction direction, double amount) {
        public Transaction {
            if (date == null) {
                throw new IllegalArgumentException("date must not be null");
            }
            try {
                java.time.LocalDate.parse(date);   // real calendar: rejects 2026-13-40
            } catch (java.time.format.DateTimeParseException e) {
                throw new IllegalArgumentException("bad date: " + date);
            }
            if (label == null || label.isBlank()) {
                throw new IllegalArgumentException("label must not be blank");
            }
            if (amount <= 0) {
                throw new IllegalArgumentException("amount must be positive: " + amount);
            }
        }
    }

    public static class Ledger {
        private final java.util.List<Transaction> txs = new java.util.ArrayList<>();

        public void add(Transaction t) { txs.add(t); }

        public int count(java.util.function.Predicate<Transaction> p) {
            return (int) txs.stream().filter(p).count();
        }

        public double net(String datePrefix) {
            double sum = 0;
            for (Transaction t : txs) {
                if (!t.date().startsWith(datePrefix)) continue;
                sum += t.direction() == Direction.CASH_IN ? t.amount() : -t.amount();
            }
            return sum;
        }

        public java.util.List<String> labelsSince(String datePrefix) {
            return txs.stream()
                .filter(t -> t.date().startsWith(datePrefix))
                .map(t -> t.label().toUpperCase())
                .collect(java.util.stream.Collectors.toList());
        }

        public java.util.List<String> saveLines() {
            java.util.List<String> out = new java.util.ArrayList<>();
            for (Transaction t : txs) {
                out.add(String.format("%s|%s|%s|%.2f",
                    t.date(), t.label(), t.direction(), t.amount()));
            }
            return out;
        }

        public void loadLine(String line) {
            try {
                String[] parts = line.split("\\|", -1);
                if (parts.length != 4) return;
                add(new Transaction(parts[0], parts[1],
                    Direction.valueOf(parts[2].trim().toUpperCase()),
                    Double.parseDouble(parts[3])));
            } catch (IllegalArgumentException e) {
                // malformed line: skip silently, never corrupt the ledger
            }
        }
    }
}
"""

P14_CP_W = r"""public class Solution {
    public enum Direction { CASH_IN, CASH_OUT }

    public record Transaction(String date, String label, Direction direction, double amount) {
        public Transaction {
            if (date == null) {
                throw new IllegalArgumentException("date must not be null");
            }
            try {
                java.time.LocalDate.parse(date);   // real calendar: rejects 2026-13-40
            } catch (java.time.format.DateTimeParseException e) {
                throw new IllegalArgumentException("bad date: " + date);
            }
            if (label == null || label.isBlank()) {
                throw new IllegalArgumentException("label must not be blank");
            }
            if (amount <= 0) {
                throw new IllegalArgumentException("amount must be positive: " + amount);
            }
        }
    }

    public static class Ledger {
        private final java.util.List<Transaction> txs = new java.util.ArrayList<>();

        public void add(Transaction t) { txs.add(t); }

        public int count(java.util.function.Predicate<Transaction> p) {
            return (int) txs.stream().filter(p).count();
        }

        public double net(String datePrefix) {
            double sum = 0;
            for (Transaction t : txs) {
                if (!t.date().startsWith(datePrefix)) continue;
                sum += t.direction() == Direction.CASH_IN ? t.amount() : -t.amount();
            }
            return sum;
        }

        public java.util.List<String> labelsSince(String datePrefix) {
            return txs.stream()
                .filter(t -> t.date().startsWith(datePrefix))
                .map(t -> t.label().toUpperCase())
                .collect(java.util.stream.Collectors.toList());
        }

        public java.util.List<String> saveLines() {
            java.util.List<String> out = new java.util.ArrayList<>();
            for (Transaction t : txs) {
                out.add(String.format("%s|%s|%s|%.2f",
                    t.date(), t.label(), t.direction(), t.amount()));
            }
            return out;
        }

        public void loadLine(String line) {
            // BUG: no guard - "garbage line" throws unchecked exception
            //      and crashes the whole load (and the program)
            String[] parts = line.split("\\|", -1);
            if (parts.length != 4) return;
            add(new Transaction(parts[0], parts[1],
                Direction.valueOf(parts[2].trim().toUpperCase()),
                Double.parseDouble(parts[3])));
        }
    }
}
"""

CK_M14_MD = r"""
The ledger - the whole course in four methods.

`net` needs the *signed* sum: `CASH_IN ? +amount : -amount`, filtered by
`date.startsWith(prefix)`. Note `net("")` means everything - the prefix
check passes trivially. `labelsSince` is filter-then-uppercase-then-collect;
insertion order comes free from `ArrayList`. `saveLines` is
`String.format("%s|%s|%s|%.2f", ...)` per transaction - and the format
string is exactly what `loadLine` will split on, which is what makes the
round-trip test honest: save, load into a *fresh* ledger, save again,
compare.

`loadLine` is the module-11 lesson wearing a capstone costume: wrap the
construct-and-add in `try { } catch (IllegalArgumentException e) { }` and
skip silently. One malformed line must never take down the whole import -
you proved you understand that in the checkpoint before last; here it
ships in the final product.

When all four test blocks pass, every module of this course has
contributed something to a working artifact. That's the finish line.
"""

CK_M14_MD_VI = r"""
Sổ giao dịch - cả khóa học gói lại trong bốn phương thức.

`net` cần tổng *có dấu*: `CASH_IN ? +amount : -amount`, lọc theo
`date.startsWith(prefix)`. Chú ý `net("")` nghĩa là tất cả - điều kiện
prefix luôn thỏa. `labelsSince` là filter-rồi-uppercase-rồi-collect; thứ
tự thêm vào là món quà miễn phí từ `ArrayList`. `saveLines` là
`String.format("%s|%s|%s|%.2f", ...)` cho từng giao dịch - và chuỗi format
đúng là thứ `loadLine` sẽ tách theo, đó là điều làm cho test round-trip
trung thực: save, nạp vào một sổ *mới tinh*, save lần nữa, so sánh.

`loadLine` là bài học module 11 khoác áo capstone: bọc construct-and-add
trong `try { } catch (IllegalArgumentException e) { }` và bỏ qua im lặng.
Một dòng lỗi không bao giờ được kéo sập cả đợt nạp - bạn đã chứng minh
mình hiểu điều đó ở checkpoint trước; giờ nó lên thuyền sản phẩm cuối.

Khi cả bốn khối test đều pass, mọi module của khóa học đều đã đóng góp
một phần vào một sản phẩm chạy được. Đó là vạch đích.
"""

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Files, Persistence & the Capstone",
    "Reading and writing real files with java.nio.file, then the course capstone: a personal transaction ledger composing every module.",
    "File, lưu trữ & capstone",
    "Đọc ghi file thật với java.nio.file, rồi capstone của khóa học: sổ giao dịch cá nhân kết hợp mọi module.",
    ["files-nio", "capstone-brief", "java-checkpoint-capstone"],
    ["javb-p14-files"],
)

write_lesson(
    MOD, "files-nio",
    "Files with java.nio.file",
    "Path and Files, write/read/append, IOException as a checked contract, and Files.walk.",
    18,
    L_FILES_EN,
    "File với java.nio.file",
    "Path và Files, ghi/đọc/nối, IOException như một hợp đồng checked, và Files.walk.",
    L_FILES_VI,
)

write_lesson(
    MOD, "java-capstone-brief",
    "The Capstone Brief",
    "The ledger spec, the grading contract, and what Java Intermediate will ask of what you build here.",
    12,
    L_CAP_EN,
    "Bản yêu cầu capstone",
    "Đặc tả sổ giao dịch, hợp đồng chấm điểm, và những gì Java Intermediate sẽ đòi hỏi từ thứ bạn xây ở đây.",
    L_CAP_VI,
)

write_practice(
    MOD, "javb-p14-files",
    "Practice: Parse the Ledger",
    "Model a transaction as a self-validating record and parse the pipe-separated format.",
    "Thực hành: Parse sổ giao dịch",
    "Mô hình hóa giao dịch bằng record tự kiểm tra và parse định dạng phân tách bằng gạch đứng.",
    "files-nio", 30, "beginner",
    [P14_TX],
    {P14_TX["id"]: P14_TX_VI},
    solutions=[
        (
            P14_TX["id"],
            r"""public class Solution {
    public enum Direction { CASH_IN, CASH_OUT }

    public record Transaction(String date, String label, Direction direction, double amount) {
        public Transaction {
            if (date == null) {
                throw new IllegalArgumentException("date must not be null");
            }
            try {
                java.time.LocalDate.parse(date);   // real calendar: rejects 2026-13-40
            } catch (java.time.format.DateTimeParseException e) {
                throw new IllegalArgumentException("bad date: " + date);
            }
            if (label == null || label.isBlank()) {
                throw new IllegalArgumentException("label must not be blank");
            }
            if (amount <= 0) {
                throw new IllegalArgumentException("amount must be positive: " + amount);
            }
        }
    }

    public static Transaction parse(String line) {
        String[] parts = line.split("\\|", -1);
        if (parts.length != 4) {
            throw new IllegalArgumentException("expected 4 fields, got " + parts.length);
        }
        return new Transaction(parts[0], parts[1],
            Direction.valueOf(parts[2].trim().toUpperCase()),
            Double.parseDouble(parts[3]));
    }
}
""",
            r"""public class Solution {
    public enum Direction { CASH_IN, CASH_OUT }

    public record Transaction(String date, String label, Direction direction, double amount) {
        public Transaction {
            if (date == null) {
                throw new IllegalArgumentException("date must not be null");
            }
            try {
                java.time.LocalDate.parse(date);   // real calendar: rejects 2026-13-40
            } catch (java.time.format.DateTimeParseException e) {
                throw new IllegalArgumentException("bad date: " + date);
            }
            if (label == null || label.isBlank()) {
                throw new IllegalArgumentException("label must not be blank");
            }
            if (amount <= 0) {
                throw new IllegalArgumentException("amount must be positive: " + amount);
            }
        }
    }

    public static Transaction parse(String line) {
        String[] parts = line.split("|", -1);   // BUG: unescaped pipe splits between EVERY character
        if (parts.length != 4) {
            throw new IllegalArgumentException("expected 4 fields, got " + parts.length);
        }
        return new Transaction(parts[0], parts[1],
            Direction.valueOf(parts[2].trim().toUpperCase()),
            Double.parseDouble(parts[3]));
    }
}
""",
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-capstone",
    "Checkpoint: The Personal Ledger",
    "Signed sums, uppercase labels, canonical save format, junk-proof loading - the course assembled.",
    50, CK_M14_MD,
    "Checkpoint: Sổ giao dịch cá nhân",
    "Tổng có dấu, label viết hoa, định dạng lưu chuẩn, nạp chống rác - cả khóa học lắp lại.",
    CK_M14_MD_VI,
    P14_CP_CH, P14_CP_VI,
    solution=P14_CP_R, wrong=P14_CP_W,
)

print("module 14 complete")
