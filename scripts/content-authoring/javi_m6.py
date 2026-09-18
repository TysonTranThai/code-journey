#!/usr/bin/env python3
"""Java — Intermediate — Module 6: java-exception-architecture.

Try-with-resources, exception boundaries, custom hierarchies, and fail-fast
validation. Honest about the sandbox: AutoCloseable is exercised with
in-memory Closeable types. House conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-exception-architecture"

# ── lesson 6.1 — try-with-resources ─────────────────────────────────────────
L_TWR_EN = r"""
## try-with-resources

Any `AutoCloseable` can be managed by try-with-resources; the compiler
writes the finally-cleanup for you — in *reverse* acquisition order:

```java
static String firstLine(Path p) throws IOException {
    try (BufferedReader r = Files.newBufferedReader(p)) {
        return r.readLine();
    }   // r.close() guaranteed, even on exception
}
```

Two resources close right-to-left:

```java
try (var in = openInput(); var out = openOutput(in)) {
    ...
}   // out closed first, then in — the dependency order
```

Suppressed exceptions: if the body throws AND close() throws, the close
exception is *attached* to the body exception (`getSuppressed()`), never
lost. With hand-written finally, the close exception would *replace* the
body exception — swallowing the real failure.

The sandbox cannot touch real files, so this course exercises
AutoCloseable with in-memory resources — the semantics are identical.
"""

L_TWR_VI = r"""
## try-with-resources

Mọi `AutoCloseable` đều được try-with-resources quản lý; compiler tự viết
phần dọn dẹp trong finally cho bạn — theo thứ tự mở *ngược lại*:

```java
static String firstLine(Path p) throws IOException {
    try (BufferedReader r = Files.newBufferedReader(p)) {
        return r.readLine();
    }   // r.close() đảm bảo chạy, kể cả khi có ngoại lệ
}
```

Hai tài nguyên đóng từ phải sang trái:

```java
try (var in = openInput(); var out = openOutput(in)) {
    ...
}   // out đóng trước, rồi in — đúng thứ tự phụ thuộc
```

Suppressed exception: nếu thân try ném VÀ close() cũng ném, ngoại lệ của
close được *gắn thêm* vào ngoại lệ thân (`getSuppressed()`), không bao giờ
mất. Với finally viết tay, ngoại lệ close sẽ *thay thế* ngoại lệ thân —
nuốt mất lỗi thật.

Sandbox không chạm file thật, nên khóa học này tập AutoCloseable bằng
tài nguyên trong bộ nhớ — ngữ nghĩa thì y hệt.
"""

# ── lesson 6.2 — exception boundaries ──────────────────────────────────────
L_BOUNDARY_EN = r"""
## Exception boundaries and translation

An intermediate codebase *translates* exceptions at architectural
boundaries instead of letting them leak:

```java
// repository layer
public User findUser(String id) {
    try {
        return db.lookup(id);
    } catch (SQLException e) {
        throw new StorageException("user lookup failed", e);  // translate + chain
    }
}
```

Rules that hold up in review:
- **catch only what you can handle** — otherwise translate or declare
- **always chain the cause** (`new X("...", e)`) so the stack trace keeps
  the original story
- **don't catch Throwable/Error** — OutOfMemoryError is not yours
- **don't swallow** — an empty catch block is a hidden bug
- low-level types (SQLException, IOException) should not cross into the
  service layer's API

Checked vs unchecked at the boundary: use *checked* for recoverable,
expected conditions the caller must handle (parse failures); *unchecked*
for programming errors and unrecoverable state (IllegalArgument,
IllegalState).
"""

L_BOUNDARY_VI = r"""
## Ranh giới exception và chuyển dịch

Codebase trình trung cấp *chuyển dịch* exception tại ranh giới kiến trúc
thay vì để chúng rò ra ngoài:

```java
// tầng repository
public User findUser(String id) {
    try {
        return db.lookup(id);
    } catch (SQLException e) {
        throw new StorageException("user lookup failed", e);  // chuyển dịch + móc nối
    }
}
```

Quy tắc sống sót qua review:
- **chỉ catch những gì bạn xử lý được** — không thì chuyển dịch hoặc khai báo
- **luôn móc cause** (`new X("...", e)`) để stack trace giữ nguyên câu chuyện gốc
- **không catch Throwable/Error** — OutOfMemoryError không phải việc của bạn
- **không nuốt** — khối catch rỗng là một bug được giấu kỹ
- kiểu cấp thấp (SQLException, IOException) không được xuyên vào API tầng service

Checked so với unchecked tại ranh giới: dùng *checked* cho điều kiện có
thể phục hồi, caller bắt buộc xử lý (lỗi parse); *unchecked* cho lỗi lập
trình và trạng thái không thể phục hồi (IllegalArgument, IllegalState).
"""

# ── lesson 6.3 — custom hierarchies ────────────────────────────────────────
L_HIERARCHY_EN = r"""
## Custom exception hierarchies

Model *domain failures* as types, not strings:

```java
public class OrderException extends RuntimeException {
    public OrderException(String message) { super(message); }
    public OrderException(String message, Throwable cause) { super(message, cause); }
}

public final class InsufficientFundsException extends OrderException {
    private final int shortfallCents;
    public InsufficientFundsException(String message, int shortfallCents) {
        super(message);
        this.shortfallCents = shortfallCents;
    }
    public int shortfallCents() { return shortfallCents; }
}
```

Callers can now catch at the right granularity:
`catch (InsufficientFundsException e)` to show a friendly message, or
`catch (OrderException e)` for all order failures.

Keep hierarchy shallow (base + 2–3 leaf types), extend RuntimeException
unless the caller can genuinely recover, and carry *data* on the
exception (like shortfallCents) instead of forcing callers to parse the
message.
"""

L_HIERARCHY_VI = r"""
## Hệ thống exception riêng

Mô hình hóa *lỗi domain* thành kiểu, không phải chuỗi:

```java
public class OrderException extends RuntimeException {
    public OrderException(String message) { super(message); }
    public OrderException(String message, Throwable cause) { super(message, cause); }
}

public final class InsufficientFundsException extends OrderException {
    private final int shortfallCents;
    public InsufficientFundsException(String message, int shortfallCents) {
        super(message);
        this.shortfallCents = shortfallCents;
    }
    public int shortfallCents() { return shortfallCents; }
}
```

Caller giờ có thể catch đúng độ mịn:
`catch (InsufficientFundsException e)` để hiển thị thông báo thân thiện,
hoặc `catch (OrderException e)` cho mọi lỗi đơn hàng.

Giữ hệ thống nông (base + 2–3 kiểu lá), extends RuntimeException trừ khi
caller thực sự phục hồi được, và *mang dữ liệu* trên exception (như
shortfallCents) thay vì ép caller đọc chuỗi message.
"""

write_module(
    MOD,
    "Exceptions & Error Architecture",
    "try-with-resources semantics, exception translation at boundaries, and custom hierarchies that carry data.",
    "Exception & kiến trúc lỗi",
    "Ngữ nghĩa try-with-resources, chuyển dịch exception tại ranh giới, và hệ thống exception riêng mang theo dữ liệu.",
    ["try-with-resources", "exception-boundaries", "custom-hierarchies", "javi-checkpoint-exceptions"],
    ["javi-p6-exceptions"],
)

write_lesson(MOD, "try-with-resources", "try-with-resources", "Compiler-managed cleanup, reverse close order, and suppressed exceptions that hand-written finally loses.", 13, L_TWR_EN, "try-with-resources", "Dọn dẹp do compiler quản, thứ tự đóng ngược, và suppressed exception mà finally viết tay đánh mất.", L_TWR_VI)

write_lesson(MOD, "exception-boundaries", "Boundaries & Translation", "Translating low-level exceptions with chained causes, and choosing checked vs unchecked deliberately.", 14, L_BOUNDARY_EN, "Ranh giới & chuyển dịch", "Chuyển dịch exception cấp thấp với cause được móc nối, và chọn checked hay unchecked một cách chủ đích.", L_BOUNDARY_VI)

write_lesson(MOD, "custom-hierarchies", "Custom Exception Hierarchies", "Domain failures as shallow type trees carrying data, so callers catch at the right granularity.", 13, L_HIERARCHY_EN, "Hệ thống exception riêng", "Lỗi domain thành cây kiểu nông mang dữ liệu, để caller catch đúng độ mịn.", L_HIERARCHY_VI)

# ── practice set ────────────────────────────────────────────────────────────
P6_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P6_TWR = challenge(
    "javi-p6-resource-order",
    "Close Order & Suppression",
    r"""Model in-memory resources inside `Solution`:
- `static class Res implements AutoCloseable` with a `StringBuilder log`
  passed in and a name; `close()` appends `name + ":closed"` to the log.
- `static String run(boolean failSecond, StringBuilder log)`:
  opens `new Res("a", log)`, then `new Res("b", log)` in ONE
  try-with-resources statement (body appends "work" to the log);
  when failSecond is true the body throws IllegalStateException AFTER
  the first resource was opened.

Return `log.toString()`. Correct behavior:
- happy path: `work` then `b:closed` then `a:closed` (reverse order)
- failure: `a:closed b:closed` STILL both closed, exception propagates""",
    P6_BOILER,
    [
        (
            "happy path closes in reverse",
            r"""
StringBuilder log = new StringBuilder();
String out = Solution.run(false, log);
checkEq(out, "workb:closeda:closed", "work then reverse close");
""",
            "Body first, then resources closed b→a (reverse acquisition).",
        ),
        (
            "failure still closes both",
            r"""
StringBuilder log = new StringBuilder();
try { Solution.run(true, log); checkTrue(false, "must throw"); }
catch (IllegalStateException e) { checkTrue(true, "propagated"); }
checkTrue(log.toString().contains("b:closed"), "b closed");
checkTrue(log.toString().contains("a:closed"), "a closed");
""",
            "Both close() calls run even though the body threw.",
        ),
    ],
    level="guided",
)

CH_P6_TRANSLATE = challenge(
    "javi-p6-translation",
    "Translate at the Boundary",
    r"""Implement a storage boundary inside `Solution`:
- `static class StorageException extends RuntimeException` with
  `(String message, Throwable cause)` constructor.
- `static class FlakyStore` with `static String fetch(String key)`:
  returns `"data-" + key`, but throws `IllegalStateException("boom")`
  when the key starts with `"!"`.
- `static String repositoryGet(String key)` — calls fetch and translates
  any IllegalStateException into StorageException("lookup failed for " + key, e),
  chaining the original cause.

Callers of repositoryGet must never see IllegalStateException.""",
    P6_BOILER,
    [
        (
            "clean key passes through",
            r"""
checkEq(Solution.repositoryGet("user-1"), "data-user-1", "clean passthrough");
""",
            "No exception on valid keys.",
        ),
        (
            "flaky key translated with cause",
            r"""
try { Solution.repositoryGet("!bad"); checkTrue(false, "must throw"); }
catch (RuntimeException e) {
    checkTrue(e instanceof Solution.StorageException, "translated type");
    checkTrue(e.getCause() instanceof IllegalStateException, "cause chained");
    checkTrue(e.getMessage().contains("!bad"), "message carries key");
}
""",
            "Translate to StorageException, keep the cause, mention the key.",
        ),
    ],
    level="independent",
)

CH_P6_HIERARCHY = challenge(
    "javi-p6-account-errors",
    "Domain Errors That Carry Data",
    r"""Model payments in `Solution`:
- `static class PaymentException extends RuntimeException`
- `static final class InsufficientFundsException extends PaymentException`
  carrying `int shortfallCents` with a getter.
- `static void withdraw(int balance, int amount)`: throws
  IllegalArgumentException for negative amount; throws
  InsufficientFundsException with shortfall `amount - balance` when
  amount > balance; otherwise completes (no-op).
- `static int shortfallOf(RuntimeException e)`: returns
  `((InsufficientFundsException) e).shortfallCents()` when applicable,
  otherwise -1.

The tests catch at both granularities.""",
    P6_BOILER,
    [
        (
            "negative amount is a programming error",
            r"""
try { Solution.withdraw(100, -5); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "iafte"); }
""",
            "Negative amounts throw IllegalArgumentException.",
        ),
        (
            "shortfall carried as data",
            r"""
try { Solution.withdraw(100, 250); checkTrue(false, "must throw"); }
catch (Solution.InsufficientFundsException e) {
    checkEq(e.shortfallCents(), 150, "shortfall data");
}
""",
            "250 - 100 = 150 shortfall, carried on the exception.",
        ),
        (
            "catch at parent granularity",
            r"""
try { Solution.withdraw(0, 5); checkTrue(false, "must throw"); }
catch (Solution.PaymentException e) {
    checkTrue(e instanceof Solution.InsufficientFundsException, "leaf type");
}
""",
            "PaymentException catch covers the leaf.",
        ),
        (
            "shortfallOf helper",
            r"""
RuntimeException e = new Solution.InsufficientFundsException("x", 42);
checkEq(Solution.shortfallOf(e), 42, "extracted");
checkEq(Solution.shortfallOf(new RuntimeException("y")), -1, "not applicable");
""",
            "Cast when possible, -1 otherwise.",
        ),
    ],
    level="independent",
)

VI_CH_P6_TWR = vi_challenge(
    "Thứ tự đóng & suppression",
    r"""Mô hình hóa tài nguyên trong bộ nhớ bên trong `Solution`:
- `static class Res implements AutoCloseable` nhận `StringBuilder log`
  và một tên; `close()` nối `name + ":closed"` vào log.
- `static String run(boolean failSecond, StringBuilder log)`:
  mở `new Res("a", log)`, rồi `new Res("b", log)` trong MỘT câu lệnh
  try-with-resources (thân nối "work" vào log); khi failSecond là true,
  thân ném IllegalStateException SAU khi tài nguyên đầu đã mở.

Trả `log.toString()`. Hành vi đúng:
- hướng bình thường: `work` rồi `b:closed` rồi `a:closed` (thứ tự ngược)
- lỗi: `a:closed b:closed` VẪN đóng cả hai, ngoại lệ lan ra ngoài""",
    [
        ("Hướng bình thường đóng ngược", "Thân trước, rồi tài nguyên đóng b→a (ngược thứ tự mở)."),
        ("Lỗi vẫn đóng cả hai", "Cả hai close() chạy dù thân đã ném."),
    ],
)

VI_CH_P6_TRANSLATE = vi_challenge(
    "Chuyển dịch tại ranh giới",
    r"""Cài một ranh giới lưu trữ bên trong `Solution`:
- `static class StorageException extends RuntimeException` với
  constructor `(String message, Throwable cause)`.
- `static class FlakyStore` với `static String fetch(String key)`:
  trả `"data-" + key`, nhưng ném `IllegalStateException("boom")` khi key
  bắt đầu bằng `"!"`.
- `static String repositoryGet(String key)` — gọi fetch và chuyển dịch
  mọi IllegalStateException thành StorageException("lookup failed for " + key, e),
  móc cause gốc.

Caller của repositoryGet không bao giờ thấy IllegalStateException.""",
    [
        ("Key sạch đi xuyên suốt", "Không ngoại lệ với key hợp lệ."),
        ("Key lỗi được chuyển dịch kèm cause", "Chuyển thành StorageException, giữ cause, nhắc key trong message."),
    ],
)

VI_CH_P6_HIERARCHY = vi_challenge(
    "Lỗi domain mang dữ liệu",
    r"""Mô hình hóa thanh toán trong `Solution`:
- `static class PaymentException extends RuntimeException`
- `static final class InsufficientFundsException extends PaymentException`
  mang `int shortfallCents` với getter.
- `static void withdraw(int balance, int amount)`: ném
  IllegalArgumentException cho amount âm; ném
  InsufficientFundsException với shortfall `amount - balance` khi
  amount > balance; còn lại hoàn tất (no-op).
- `static int shortfallOf(RuntimeException e)`: trả
  `((InsufficientFundsException) e).shortfallCents()` khi áp dụng được,
  nếu không -1.

Test catch ở cả hai độ mịn.""",
    [
        ("Amount âm là lỗi lập trình", "Amount âm ném IllegalArgumentException."),
        ("Shortfall mang theo dữ liệu", "250 - 100 = 150 shortfall, gắn trên exception."),
        ("Catch ở độ mịn cha", "Catch PaymentException phủ kiểu lá."),
        ("Helper shortfallOf", "Cast khi có thể, -1 khi không."),
    ],
)

write_practice(
    MOD,
    "javi-p6-exceptions",
    "Exception Architecture Lab",
    "Reverse-order cleanup with suppression, boundary translation with chained causes, and data-carrying domain errors.",
    "Xưởng kiến trúc exception",
    "Dọn dẹp ngược thứ tự có suppression, chuyển dịch ranh giới với cause móc nối, và lỗi domain mang dữ liệu.",
    "custom-hierarchies",
    40,
    "intermediate",
    [CH_P6_TWR, CH_P6_TRANSLATE, CH_P6_HIERARCHY],
    {CH_P6_TWR["id"]: VI_CH_P6_TWR, CH_P6_TRANSLATE["id"]: VI_CH_P6_TRANSLATE, CH_P6_HIERARCHY["id"]: VI_CH_P6_HIERARCHY},
    solutions=[
        (
            CH_P6_TWR["id"],
            r"""
public class Solution {
    public static class Res implements AutoCloseable {
        private final String name;
        private final StringBuilder log;
        public Res(String name, StringBuilder log) { this.name = name; this.log = log; }
        @Override public void close() { log.append(name).append(":closed"); }
    }

    public static String run(boolean failSecond, StringBuilder log) {
        Res a = new Res("a", log);
        Res b = new Res("b", log);
        try (Res x = a; Res y = b) {
            log.append("work");
            if (failSecond) throw new IllegalStateException("body failed");
        }
        // return AFTER the try — close() appends during implicit finally,
        // so returning inside would snapshot an incomplete log.
        return log.toString();
    }
}
""",
            r"""
public class Solution {
    public static class Res implements AutoCloseable {
        private final String name;
        private final StringBuilder log;
        public Res(String name, StringBuilder log) { this.name = name; this.log = log; }
        @Override public void close() { log.append(name).append(":closed"); }
    }

    // W: manual finally that returns INSIDE the try — the return value
    // snapshots the log BEFORE finally appends the close markers, the
    // exact trap the Beginner course taught. Both closes do run, but the
    // caller never sees them.
    public static String run(boolean failSecond, StringBuilder log) {
        StringBuilder inner = new StringBuilder();
        Res a = new Res("a", inner);
        Res b = new Res("b", inner);
        try {
            log.append("work");
            if (failSecond) throw new IllegalStateException("body failed");
            return inner.toString();
        } finally {
            try { b.close(); } catch (RuntimeException ignored) { }
            try { a.close(); } catch (RuntimeException ignored) { }
        }
    }
}
""",
        ),
        (
            CH_P6_TRANSLATE["id"],
            r"""
public class Solution {
    public static class StorageException extends RuntimeException {
        public StorageException(String message, Throwable cause) { super(message, cause); }
    }

    public static class FlakyStore {
        public static String fetch(String key) {
            if (key.startsWith("!")) throw new IllegalStateException("boom");
            return "data-" + key;
        }
    }

    public static String repositoryGet(String key) {
        try {
            return FlakyStore.fetch(key);
        } catch (IllegalStateException e) {
            throw new StorageException("lookup failed for " + key, e);
        }
    }
}
""",
            r"""
public class Solution {
    public static class StorageException extends RuntimeException {
        public StorageException(String message, Throwable cause) { super(message, cause); }
    }

    public static class FlakyStore {
        public static String fetch(String key) {
            if (key.startsWith("!")) throw new IllegalStateException("boom");
            return "data-" + key;
        }
    }

    // W: swallows the failure and returns a placeholder — the caller
    // cannot distinguish missing data from a real result.
    public static String repositoryGet(String key) {
        try {
            return FlakyStore.fetch(key);
        } catch (IllegalStateException e) {
            return "data-missing";
        }
    }
}
""",
        ),
        (
            CH_P6_HIERARCHY["id"],
            r"""
public class Solution {
    public static class PaymentException extends RuntimeException {
        public PaymentException(String message) { super(message); }
    }

    public static final class InsufficientFundsException extends PaymentException {
        private final int shortfallCents;
        public InsufficientFundsException(String message, int shortfallCents) {
            super(message);
            this.shortfallCents = shortfallCents;
        }
        public int shortfallCents() { return shortfallCents; }
    }

    public static void withdraw(int balance, int amount) {
        if (amount < 0) throw new IllegalArgumentException("negative amount");
        if (amount > balance) throw new InsufficientFundsException("insufficient", amount - balance);
    }

    public static int shortfallOf(RuntimeException e) {
        return e instanceof InsufficientFundsException f ? f.shortfallCents() : -1;
    }
}
""",
            r"""
public class Solution {
    public static class PaymentException extends RuntimeException {
        public PaymentException(String message) { super(message); }
    }

    public static final class InsufficientFundsException extends PaymentException {
        private final int shortfallCents;
        public InsufficientFundsException(String message, int shortfallCents) {
            super(message);
            this.shortfallCents = shortfallCents;
        }
        public int shortfallCents() { return shortfallCents; }
    }

    // W: validates with the wrong exception type — negative amounts are
    // a caller bug (IllegalArgumentException), not a domain failure.
    public static void withdraw(int balance, int amount) {
        if (amount < 0) throw new InsufficientFundsException("negative", 0);
        if (amount > balance) throw new InsufficientFundsException("insufficient", amount - balance);
    }

    public static int shortfallOf(RuntimeException e) {
        return e instanceof InsufficientFundsException f ? f.shortfallCents() : -1;
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — error architecture

You can now: guarantee cleanup with try-with-resources, translate
exceptions across boundaries with chained causes, and expose domain
failures as typed data. Prove it with a validation pipeline.
"""

CP_MDX_VI = r"""
## Checkpoint — kiến trúc lỗi

Giờ bạn có thể: bảo đảm dọn dẹp bằng try-with-resources, chuyển dịch
exception qua ranh giới với cause móc nối, và lộ lỗi domain thành dữ liệu
có kiểu. Chứng minh bằng một pipeline kiểm tra dữ liệu.
"""

CH_CP6 = challenge(
    "javi-checkpoint-m6-exceptions",
    "Validation Pipeline",
    r"""Build `Solution`:
- `static class ValidationException extends RuntimeException` carrying
  `List<String> errors` (getter `errors()`); message joins the errors.
- `static void validate(List<String> fields)`: collect ALL failures —
  blank fields (`null` or `isBlank`) become error
  `"field " + index + " blank"`; then throw ValidationException with the
  full error list if any.
- `static int firstError(RuntimeException e)`: returns 0 when e is a
  ValidationException, -1 otherwise.

Fail-fast would have stopped at the first problem — you collect everything,
which is what a validation *pipeline* means.""",
    r"""
import java.util.*;

public class Solution {
    // Provide ValidationException + validate + firstError here.
}
""",
    [
        (
            "valid input passes",
            r"""
Solution.validate(List.of("a", "b"));
checkTrue(true, "no throw");
""",
            "No exception when nothing is blank.",
        ),
        (
            "all errors collected",
            r"""
try { Solution.validate(Arrays.asList("ok", "", null)); checkTrue(false, "must throw"); }
catch (Solution.ValidationException e) {
    checkEq(e.errors().size(), 2, "two errors");
    checkTrue(e.errors().contains("field 1 blank"), "index 1");
    checkTrue(e.errors().contains("field 2 blank"), "index 2");
}
""",
            "Both blank fields reported — not just the first.",
        ),
        (
            "firstError discriminator",
            r"""
checkEq(Solution.firstError(new Solution.ValidationException(List.of("x"))), 0, "validation type");
checkEq(Solution.firstError(new RuntimeException("other")), -1, "other type");
""",
            "0 for ValidationException, -1 otherwise.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP6 = vi_challenge(
    "Pipeline kiểm tra dữ liệu",
    r"""Xây `Solution`:
- `static class ValidationException extends RuntimeException` mang
  `List<String> errors` (getter `errors()`); message nối các lỗi.
- `static void validate(List<String> fields)`: gom TẤT CẢ lỗi — field
  rỗng (`null` hoặc `isBlank`) thành lỗi
  `"field " + index + " blank"`; rồi ném ValidationException với danh sách
  lỗi đầy đủ nếu có bất kỳ lỗi nào.

Fail-fast sẽ dừng ở lỗi đầu — bạn gom hết, đó mới là nghĩa của pipeline
kiểm tra.""",
    [
        ("Input hợp lệ đi qua", "Không ngoại lệ khi không có gì rỗng."),
        ("Gom tất cả lỗi", "Cả hai field rỗng được báo cáo — không chỉ lỗi đầu."),
        ("Bộ phân loại firstError", "0 cho ValidationException, -1 cho loại khác."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-exceptions",
    "Checkpoint: Error Architecture",
    "Graded checkpoint: a collecting validation pipeline with a data-carrying exception type.",
    15,
    CP_MDX,
    "Checkpoint: Kiến trúc lỗi",
    "Checkpoint chấm điểm: pipeline kiểm tra gom lỗi với kiểu exception mang dữ liệu.",
    CP_MDX_VI,
    CH_CP6,
    VI_CH_CP6,
    solution=r"""
import java.util.*;

public class Solution {
    public static class ValidationException extends RuntimeException {
        private final List<String> errors;
        public ValidationException(List<String> errors) {
            super(String.join("; ", errors));
            this.errors = List.copyOf(errors);
        }
        public List<String> errors() { return errors; }
    }

    public static void validate(List<String> fields) {
        List<String> errors = new ArrayList<>();
        for (int i = 0; i < fields.size(); i++) {
            String f = fields.get(i);
            if (f == null || f.isBlank()) errors.add("field " + i + " blank");
        }
        if (!errors.isEmpty()) throw new ValidationException(errors);
    }

    public static int firstError(RuntimeException e) {
        return e instanceof ValidationException ? 0 : -1;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public static class ValidationException extends RuntimeException {
        private final List<String> errors;
        public ValidationException(List<String> errors) {
            super(String.join("; ", errors));
            this.errors = List.copyOf(errors);
        }
        public List<String> errors() { return errors; }
    }

    // W: fail-fast — throws at the FIRST blank field, so the errors list
    // never carries more than one entry. A validation pipeline must
    // collect everything.
    public static void validate(List<String> fields) {
        for (int i = 0; i < fields.size(); i++) {
            String f = fields.get(i);
            if (f == null || f.isBlank()) throw new ValidationException(List.of("field " + i + " blank"));
        }
    }

    public static int firstError(RuntimeException e) {
        return e instanceof ValidationException ? 0 : -1;
    }
}
""",
)
