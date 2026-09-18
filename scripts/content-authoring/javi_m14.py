#!/usr/bin/env python3
"""Java — Intermediate — Module 14: java-clean-code.

Professional code quality: names that carry meaning, functions that do
one thing, the smells that flag refactor opportunities, and comments that
explain why (not what). House conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-clean-code"

# ── lesson 14.1 — naming & functions ────────────────────────────────────────
L_NAMING_EN = r"""
## Names and functions that respect the reader

A name is a contract with the next reader (usually you, in six months):

```java
// what does "d" mean? days? data? delta?
int d = getD(u);

// reads like the sentence it implements
int daysUntilExpiry = daysBetween(today, subscription.endDate());
```

Naming rules that scale:
- booleans read as predicates: `isExpired`, `hasChildren`, `canRetry`
- methods are verbs: `calculateTotal`, not `total` (that's a getter's job)
- no abbreviations unless the domain owns them (`vat`, `isbn` are fine)
- one concept, one word: `fetch`/`get`/`retrieve` for the same idea
  across a codebase is noise

Functions:
- **do one thing** at one level of abstraction
- small enough that its `if`s fit your field of vision
- few parameters (two or three; more means a parameter object wants to
  exist)

```java
// before
public void process(List<Order> os, boolean f, boolean d) { ... }

// after — flags are usually two functions hiding
public void processForInvoice(List<Order> orders) { ... }
public void processForDisplay(List<Order> orders) { ... }
```
"""

L_NAMING_VI = r"""
## Tên và hàm tôn trọng người đọc

Tên là một hợp đồng với người đọc tiếp theo (thường là chính bạn, sáu
tháng nữa):

```java
// "d" là gì? days? data? delta?
int d = getD(u);

// đọc như câu văn mà nó hiện thực
int daysUntilExpiry = daysBetween(today, subscription.endDate());
```

Quy tắc đặt tên mở rộng được:
- boolean đọc như vị từ: `isExpired`, `hasChildren`, `canRetry`
- method là động từ: `calculateTotal`, không phải `total` (việc của
  getter)
- không viết tắt trừ khi domain sở hữu nó (`vat`, `isbn` thì ổn)
- một khái niệm, một từ: `fetch`/`get`/`retrieve` cho cùng một ý tưởng
  trong cùng codebase là nhiễu

Hàm:
- **làm một việc** ở một mức trừu tượng
- nhỏ đến mức các `if` của nó nằm gọn trong tầm mắt
- ít tham số (hai ba là cùng; nhiều hơn nghĩa là một parameter object
  đang muốn ra đời)

```java
// trước
public void process(List<Order> os, boolean f, boolean d) { ... }

// sau — cờ thường là hai hàm đang trốn
public void processForInvoice(List<Order> orders) { ... }
public void processForDisplay(List<Order> orders) { ... }
```
"""

# ── lesson 14.2 — smells & refactoring ─────────────────────────────────────
L_SMELLS_EN = r"""
## Code smells and the refactoring reflex

Smells don't prove a bug — they *invite a look*:

- **Long method** — many blank lines and levels; extract methods
- **Primitive obsession** — money as `int`, phone as `String` everywhere;
  introduce tiny value types
- **Data clumps** — `city, street, zip` traveling together forever; make
  an `Address` record
- **Feature envy** — a method reaching into another object's getters
  more than its own fields; move it there
- **Shotgun surgery** — one change touches ten files; the concept needs
  a home
- **Comment explaining WHAT** — the code should say what; comments say
  *why* (constraints, links, tradeoffs)

```java
// before — primitive obsession + long method
static boolean ok(String u, String p) { ... }

// after — names and types carry the design
static boolean isPasswordValid(Password candidate, PasswordPolicy policy) { ... }
```

Refactoring discipline (from Module 12): small verified steps, tests
green between each, behavior unchanged by construction.
"""

L_SMELLS_VI = r"""
## Code smell và phản xạ refactor

Smell không chứng minh có bug — chúng *mời bạn nhìn vào*:

- **Method dài** — nhiều dòng trống và nhiều cấp; tách method
- **Nghiện primitive** — tiền là `int`, điện thoại là `String` khắp nơi;
  giới thiệu value type tí hon
- **Cục dữ liệu ríu nhau** — `city, street, zip` đi cùng nhau vĩnh viễn;
  làm một record `Address`
- **Ghen feature** — một method chộp getter của đối tượng khác nhiều
  hơn field của chính nó; dời nó sang đó
- **Phẫu thuật tán loạn** — một thay đổi chạm mười file; khái niệm cần
  một ngôi nhà
- **Comment giải thích WHAT** — code phải nói được cái gì; comment nói
  *tại sao* (ràng buộc, liên kết, tradeoff)

```java
// trước — nghiện primitive + method dài
static boolean ok(String u, String p) { ... }

// sau — tên và kiểu mang theo thiết kế
static boolean isPasswordValid(Password candidate, PasswordPolicy policy) { ... }
```

Kỷ luật refactor (từ Module 12): các bước nhỏ đã kiểm chứng, test xanh
giữa các bước, hành vi không đổi do cấu trúc.
"""

# ── lesson 14.3 — defensive readability ────────────────────────────────────
L_READ_EN = r"""
## Defensive readability

Write code that *prevents* misreading:

- **guard clauses first** — fail fast, then the happy path reads straight
  down without else-nesting:

```java
if (order == null) throw new IllegalArgumentException("order required");
if (order.items().isEmpty()) return OrderResult.empty();
// happy path continues at indentation 0
```

- **early returns over else-terraces** — each `else` adds a level the
  reader must track
- **expressions over statements where the name is the point**:
  `boolean isAdult = age >= 18;` beats re-reading `age >= 18` four times
- **structure beats cleverness** — the branchless bit-trick version of
  `max` costs a comment and a future bug; `Math.max` costs nothing

The test: could a teammate skimming a PR diff misread any line? If yes,
rename, extract, or flatten until the answer is no.
"""

L_READ_VI = r"""
## Khả đọc phòng thủ

Viết code *ngăn* hiểu sai:

- **guard clause trước** — fail fast, rồi hướng bình thường đọc thẳng
  xuống không else-lồng nhau:

```java
if (order == null) throw new IllegalArgumentException("order required");
if (order.items().isEmpty()) return OrderResult.empty();
// hướng bình thường tiếp tục ở thụt lề 0
```

- **return sớm thay bậc thang else** — mỗi `else` thêm một cấp mà người
  đọc phải theo dõi
- **biểu thức thay câu lệnh khi cái tên mới là vấn đề**:
  `boolean isAdult = age >= 18;` tốt hơn đọc lại `age >= 18` bốn lần
- **cấu trúc thắng sự tinh ranh** — bản bit-trick không nhánh của `max`
  tốn một comment và một bug trong tương lai; `Math.max` không tốn gì

Phép thử: đồng nghiệp đọc lướt diff PR có thể hiểu sai dòng nào không?
Nếu có — đổi tên, tách, hoặc làm phẳng cho đến khi câu trả lời là không.
"""

write_module(
    MOD,
    "Professional Java Code",
    "Names and functions that respect the reader, the smell→refactor reflex, and defensive readability.",
    "Code Java chuyên nghiệp",
    "Tên và hàm tôn trọng người đọc, phản xạ smell→refactor, và khả đọc phòng thủ.",
    ["naming-functions", "smells-refactoring", "defensive-readability", "javi-checkpoint-clean"],
    ["javi-p14-clean"],
)

write_lesson(MOD, "naming-functions", "Naming & Function Design", "Predicates read as questions, flags as two functions, and parameter objects that want to exist.", 13, L_NAMING_EN, "Đặt tên & thiết kế hàm", "Vị từ đọc như câu hỏi, cờ là hai hàm đang trốn, và parameter object đang muốn ra đời.", L_NAMING_VI)

write_lesson(MOD, "smells-refactoring", "Smells & Refactoring", "Long methods, primitive obsession, feature envy — and comments that explain why instead of what.", 14, L_SMELLS_EN, "Smell & refactor", "Method dài, nghiện primitive, ghen feature — và comment giải thích tại sao thay vì cái gì.", L_SMELLS_VI)

write_lesson(MOD, "defensive-readability", "Defensive Readability", "Guard clauses, early returns, and structure over cleverness — code that prevents misreading.", 12, L_READ_EN, "Khả đọc phòng thủ", "Guard clause, return sớm, và cấu trúc thắng tinh ranh — code ngăn hiểu sai.", L_READ_VI)

# ── practice set ────────────────────────────────────────────────────────────
P14_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement methods below.
}
"""

CH_P14_RENAME = challenge(
    "javi-p14-guard-rename",
    "Guard Clauses & Honest Names",
    r"""Refactor (re-implement) `static int shipFee(int weightGrams,
boolean vip, String country)` — behavior frozen by these tests, but the
implementation must use GUARD CLAUSES (no else-nesting) and the local
variables must carry meaningful names:
- country not "VN" or "SG" → IllegalArgumentException
- weight <= 0 → IllegalArgumentException
- base fee: 400 cents; plus 200 if weight > 2000
- vip: 50% off the running total (integer division)

The grader checks behavior AND structure: the method must not contain
an `else` branch and must use a variable named `feeCents`.""",
    P14_BOILER,
    [
        (
            "fee schedule",
            r"""
checkEq(Solution.shipFee(1000, false, "VN"), 400, "base");
checkEq(Solution.shipFee(3000, false, "SG"), 600, "base + heavy");
checkEq(Solution.shipFee(3000, true, "SG"), 300, "vip half");
""",
            "400 base, +200 heavy, vip halves.",
        ),
        (
            "validation fails fast",
            r"""
try { Solution.shipFee(500, false, "FR"); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "country"); }
try { Solution.shipFee(0, false, "VN"); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "weight"); }
""",
            "Unsupported country and non-positive weight throw immediately.",
        ),
    ],
    level="independent",
)

CH_P14_VALUE = challenge(
    "javi-p14-value-object",
    "Beat Primitive Obsession",
    r"""Introduce a value object in `Solution`:
- `static class Email` with constructor `(String raw)` that validates:
  exactly one '@', non-empty local part and domain, domain contains a
  '.' after the '@'. Invalid → IllegalArgumentException.
  Store a normalized (trimmed, lowercased) final field `value` with
  getter `value()`.
- `static List<String> uniqueEmails(List<String> rawList)` — parses each
  into Email (invalid ones skipped) and returns distinct normalized
  values, insertion order.

Strings stay strings at the edges; inside this code, an Email is not a
String.""",
    P14_BOILER,
    [
        (
            "valid emails normalize",
            r"""
Solution.Email e = new Solution.Email("  Ann@Example.COM ");
checkEq(e.value(), "ann@example.com", "normalized");
""",
            "Trimmed and lowercased at construction.",
        ),
        (
            "invalid shapes rejected",
            r"""
for (String bad : new String[]{"nope", "a@b", "@x.com", "a@.com", "a@@b.com"}) {
    try { new Solution.Email(bad); checkTrue(false, "should reject " + bad); }
    catch (IllegalArgumentException e) { /* expected */ }
}
""",
            "Missing domain dot, double @, empty local — all rejected.",
        ),
        (
            "uniqueEmails dedupes",
            r"""
List<String> out = Solution.uniqueEmails(List.of(
    "A@x.com", "bad", "a@X.COM", "b@y.com"));
checkEq(out, List.of("a@x.com", "b@y.com"), "distinct normalized");
""",
            "Invalid skipped, duplicates collapse case-insensitively.",
        ),
    ],
    level="independent",
)

CH_P14_EXTRACT = challenge(
    "javi-p14-extract-statements",
    "Extract, Don't Duplicate",
    r"""Re-implement `static List<String> auditLines(List<Integer> amountsCents)`
with EXTRACTED helpers (the grader inspects that helpers exist):
- `static boolean isSuspicious(int cents)` — |amount| > 10000
- `static String describe(int cents)` — `"CREDIT " + cents` when >= 0,
  `"DEBIT " + (-cents)` otherwise
- auditLines returns one line per amount: `describe(a)` plus
  `" [SUSPECT]"` appended when isSuspicious(a).

The old version (comments in starter) had the threshold and format
duplicated three times — your version states each once.""",
    P14_BOILER,
    [
        (
            "lines describe amounts",
            r"""
List<String> out = Solution.auditLines(List.of(500, -200));
checkEq(out, List.of("CREDIT 500", "DEBIT 200"), "described");
""",
            "Debits show the positive magnitude.",
        ),
        (
            "suspicious amounts flagged",
            r"""
List<String> out = Solution.auditLines(List.of(10001, 10000));
checkEq(out.get(0), "CREDIT 10001 [SUSPECT]", "over threshold");
checkEq(out.get(1), "CREDIT 10000", "at threshold is fine");
""",
            "Strictly greater than 10000 is suspicious.",
        ),
        (
            "helpers exist and agree",
            r"""
checkEq(Solution.isSuspicious(15000), true, "helper true");
checkEq(Solution.isSuspicious(10000), false, "helper false");
checkEq(Solution.describe(-5), "DEBIT 5", "helper format");
""",
            "Single source of truth for threshold and format.",
        ),
    ],
    level="independent",
)

VI_CH_P14_RENAME = vi_challenge(
    "Guard clause & tên trung thực",
    r"""Refactor (cài lại) `static int shipFee(int weightGrams,
boolean vip, String country)` — hành vi bị đóng băng bởi các test này,
nhưng hiện thực phải dùng GUARD CLAUSE (không else-lồng) và biến cục
bộ phải mang tên có nghĩa:
- country không phải "VN" hoặc "SG" → IllegalArgumentException
- weight <= 0 → IllegalArgumentException
- phí gốc: 400 cents; cộng 200 nếu weight > 2000
- vip: giảm 50% tổng tạm thời (chia nguyên)

Máy chấm kiểm cả hành vi LẪN cấu trúc: method không được chứa bất kỳ
nhánh `else` nào và phải dùng biến tên `feeCents`.""",
    [
        ("Biểu phí", "400 gốc, +200 cồng kềnh, vip chia đôi."),
        ("Kiểm tra fail fast", "Country không hỗ trợ và weight không dương ném ngay."),
    ],
)

VI_CH_P14_VALUE = vi_challenge(
    "Đánh bại nghiện primitive",
    r"""Giới thiệu một value object trong `Solution`:
- `static class Email` với constructor `(String raw)` kiểm tra: đúng một
  '@', phần local và domain khác rỗng, domain có '.' sau '@'. Không hợp
  lệ → IllegalArgumentException. Lưu field final `value` đã chuẩn hóa
  (trim, viết thường) với getter `value()`.
- `static List<String> uniqueEmails(List<String> rawList)` — parse từng
  cái thành Email (bỏ qua cái lỗi) và trả các giá trị chuẩn hóa phân
  biệt, theo thứ tự chèn.

String vẫn là string ở rìa; bên trong code này, một Email không phải
String.""",
    [
        ("Email hợp lệ được chuẩn hóa", "Trim và viết thường ngay lúc dựng."),
        ("Dáng không hợp lệ bị chặn", "Thiếu chấm domain, @@ kép, local rỗng — đều bị chặn."),
        ("uniqueEmails khử trùng lặp", "Bỏ cái lỗi, gộp trùng không kể hoa thường."),
    ],
)

VI_CH_P14_EXTRACT = vi_challenge(
    "Tách, đừng nhân bản",
    r"""Cài lại `static List<String> auditLines(List<Integer> amountsCents)`
với helper ĐƯỢC TÁCH RA (máy chấm kiểm helper có tồn tại):
- `static boolean isSuspicious(int cents)` — |amount| > 10000
- `static String describe(int cents)` — `"CREDIT " + cents` khi >= 0,
  `"DEBIT " + (-cents)` nếu ngược lại
- auditLines trả một dòng mỗi amount: `describe(a)` cộng thêm
  `" [SUSPECT]"` khi isSuspicious(a).

Bản cũ (comment trong starter) nhân bản ngưỡng và format ba lần — bản
của bạn nêu mỗi cái đúng một lần.""",
    [
        ("Các dòng mô tả amount", "Debit hiện độ lớn dương."),
        ("Amount đáng ngờ được gắn cờ", "Nghiêm ngặt trên 10000 mới đáng ngờ."),
        ("Helper tồn tại và khớp nhau", "Một nguồn sự thật cho ngưỡng và format."),
    ],
)

write_practice(
    MOD,
    "javi-p14-clean",
    "Clean Code Lab",
    "Behavior-frozen refactors: guard clauses, a real Email value type, and extracted single-source helpers.",
    "Xưởng code sạch",
    "Refactor đóng băng hành vi: guard clause, một kiểu Email thật, và helper trích xuất một nguồn sự thật.",
    "defensive-readability",
    40,
    "intermediate",
    [CH_P14_RENAME, CH_P14_VALUE, CH_P14_EXTRACT],
    {CH_P14_RENAME["id"]: VI_CH_P14_RENAME, CH_P14_VALUE["id"]: VI_CH_P14_VALUE, CH_P14_EXTRACT["id"]: VI_CH_P14_EXTRACT},
    solutions=[
        (
            CH_P14_RENAME["id"],
            r"""
public class Solution {
    public static int shipFee(int weightGrams, boolean vip, String country) {
        if (!"VN".equals(country) && !"SG".equals(country)) {
            throw new IllegalArgumentException("unsupported country");
        }
        if (weightGrams <= 0) throw new IllegalArgumentException("weight required");
        int feeCents = 400;
        if (weightGrams > 2000) feeCents += 200;
        if (vip) feeCents = feeCents / 2;
        return feeCents;
    }
}
""",
            r"""
public class Solution {
    // W: vip discount applied to the BASE only, before the heavy
    // surcharge — a VIP with a heavy parcel pays 400/2+200 = 400 instead
    // of the correct 600/2 = 300. Wrong on the heavy-VIP row.
    public static int shipFee(int weightGrams, boolean vip, String country) {
        if (!"VN".equals(country) && !"SG".equals(country)) {
            throw new IllegalArgumentException("unsupported country");
        }
        if (weightGrams <= 0) throw new IllegalArgumentException("weight required");
        int feeCents = 400;
        if (vip) feeCents = feeCents / 2;
        if (weightGrams > 2000) feeCents += 200;
        return feeCents;
    }
}
""",
        ),
        (
            CH_P14_VALUE["id"],
            r"""
import java.util.*;

public class Solution {
    public static class Email {
        private final String value;
        public Email(String raw) {
            if (raw == null) throw new IllegalArgumentException("email required");
            String v = raw.trim().toLowerCase();
            int at = v.indexOf('@');
            if (at <= 0 || at != v.lastIndexOf('@')) throw new IllegalArgumentException("bad email");
            String local = v.substring(0, at);
            String domain = v.substring(at + 1);
            int dot = domain.lastIndexOf('.');
            if (local.isEmpty() || domain.isEmpty() || dot < 1 || dot == domain.length() - 1) {
                throw new IllegalArgumentException("bad email");
            }
            this.value = v;
        }
        public String value() { return value; }
    }

    public static List<String> uniqueEmails(List<String> rawList) {
        List<String> out = new ArrayList<>();
        Set<String> seen = new HashSet<>();
        for (String raw : rawList) {
            try {
                Email e = new Email(raw);
                if (seen.add(e.value())) out.add(e.value());
            } catch (IllegalArgumentException ignored) { }
        }
        return out;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static class Email {
        private final String value;
        public Email(String raw) {
            if (raw == null) throw new IllegalArgumentException("email required");
            String v = raw.trim().toLowerCase();
            int at = v.indexOf('@');
            if (at <= 0 || at != v.lastIndexOf('@')) throw new IllegalArgumentException("bad email");
            String local = v.substring(0, at);
            String domain = v.substring(at + 1);
            int dot = domain.lastIndexOf('.');
            if (local.isEmpty() || domain.isEmpty() || dot < 1 || dot == domain.length() - 1) {
                throw new IllegalArgumentException("bad email");
            }
            this.value = v;
        }
        public String value() { return value; }
    }

    // W: uniqueEmails ignores parse failures and emits the RAW strings —
    // normalization and error-handling both skipped, so duplicates in
    // different cases survive and garbage leaks through.
    public static List<String> uniqueEmails(List<String> rawList) {
        List<String> out = new ArrayList<>();
        for (String raw : rawList) {
            if (!out.contains(raw)) out.add(raw);
        }
        return out;
    }
}
""",
        ),
        (
            CH_P14_EXTRACT["id"],
            r"""
import java.util.*;

public class Solution {
    public static boolean isSuspicious(int cents) {
        return Math.abs(cents) > 10000;
    }

    public static String describe(int cents) {
        return cents >= 0 ? "CREDIT " + cents : "DEBIT " + (-cents);
    }

    public static List<String> auditLines(List<Integer> amountsCents) {
        List<String> out = new ArrayList<>();
        for (int a : amountsCents) {
            String line = describe(a);
            if (isSuspicious(a)) line += " [SUSPECT]";
            out.add(line);
        }
        return out;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static boolean isSuspicious(int cents) {
        return Math.abs(cents) > 10000;
    }

    public static String describe(int cents) {
        return cents >= 0 ? "CREDIT " + cents : "DEBIT " + (-cents);
    }

    // W: the SUSPECT threshold is re-hardcoded as 9999 here instead of
    // calling isSuspicious — two thresholds now disagree, exactly the
    // duplication the exercise removed.
    public static List<String> auditLines(List<Integer> amountsCents) {
        List<String> out = new ArrayList<>();
        for (int a : amountsCents) {
            String line = describe(a);
            if (Math.abs(a) > 9999) line += " [SUSPECT]";
            out.add(line);
        }
        return out;
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — professional code

You can now: freeze behavior and improve structure, give every concept
one home, and let types carry meaning instead of primitives. Prove it
with a validator refactor.
"""

CP_MDX_VI = r"""
## Checkpoint — code chuyên nghiệp

Giờ bạn có thể: đóng băng hành vi và cải thiện cấu trúc, cho mọi khái
niệm một ngôi nhà, và để kiểu mang ý nghĩa thay vì primitive. Chứng minh
bằng một bản refactor validator.
"""

CH_CP14 = challenge(
    "javi-checkpoint-m14-clean",
    "Refactor the Validator",
    r"""`static String validateOrder(String id, int cents, String coupon)`
returns one of `"OK"`, `"BAD_ID"`, `"BAD_AMOUNT"`, `"BAD_COUPON"` —
first failure wins. Rules:
- id: non-null, 3..20 chars → else BAD_ID
- cents: 1..1_000_000 → else BAD_AMOUNT
- coupon: null/empty OK; otherwise must match `[A-Z0-9]{4,10}` →
  else BAD_COUPON

Implement it CLEANLY: extract `static boolean isValidId(String id)`,
`static boolean isValidAmount(int cents)`, and
`static boolean isValidCoupon(String coupon)` — validateOrder calls the
three helpers, no duplicated rule logic, guard-style.""",
    r"""
public class Solution {
    // Provide the three isValid helpers + validateOrder here.
}
""",
    [
        (
            "valid order",
            r"""
checkEq(Solution.validateOrder("abc", 500, null), "OK", "clean order");
checkEq(Solution.validateOrder("abc", 500, "SAVE10"), "OK", "coupon ok");
""",
            "Null coupon means none.",
        ),
        (
            "failure precedence",
            r"""
checkEq(Solution.validateOrder("ab", -5, "bad"), "BAD_ID", "id first");
checkEq(Solution.validateOrder("abc", 0, "bad"), "BAD_AMOUNT", "amount second");
checkEq(Solution.validateOrder("abc", 500, "x!"), "BAD_COUPON", "coupon last");
""",
            "ID → amount → coupon, first failure wins.",
        ),
        (
            "boundary values",
            r"""
checkEq(Solution.validateOrder("abc", 1, null), "OK", "min amount");
checkEq(Solution.validateOrder("abc", 1000000, null), "OK", "max amount");
checkEq(Solution.validateOrder("abc", 1000001, null), "BAD_AMOUNT", "over max");
""",
            "Ranges inclusive at the ends.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CH_CP14 = vi_challenge(
    "Refactor bộ kiểm tra",
    r"""`static String validateOrder(String id, int cents, String coupon)`
trả một trong `"OK"`, `"BAD_ID"`, `"BAD_AMOUNT"`, `"BAD_COUPON"` — lỗi
đầu tiên thắng. Quy tắc:
- id: không null, 3..20 ký tự → không thì BAD_ID
- cents: 1..1_000_000 → không thì BAD_AMOUNT
- coupon: null/rỗng thì OK; nếu không phải khớp `[A-Z0-9]{4,10}` →
  không thì BAD_COUPON

Cài nó SẠCH: tách `static boolean isValidId(String id)`,
`static boolean isValidAmount(int cents)`, và
`static boolean isValidCoupon(String coupon)` — validateOrder gọi ba
helper, không nhân bản logic quy tắc, kiểu guard.""",
    [
        ("Đơn hàng hợp lệ", "Coupon null nghĩa là không có."),
        ("Thứ tự ưu tiên lỗi", "ID → amount → coupon, lỗi đầu tiên thắng."),
        ("Giá trị biên", "Hai đầu khoảng được tính vào."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-clean",
    "Checkpoint: Professional Code",
    "Graded checkpoint: a rule-extracted validator with single-source helpers and frozen behavior.",
    15,
    CP_MDX,
    "Checkpoint: Code chuyên nghiệp",
    "Checkpoint chấm điểm: validator tách quy tắc với helper một nguồn sự thật và hành vi đóng băng.",
    CP_MDX_VI,
    CH_CP14,
    VI_CH_CP14,
    solution=r"""
public class Solution {
    public static boolean isValidId(String id) {
        return id != null && id.length() >= 3 && id.length() <= 20;
    }

    public static boolean isValidAmount(int cents) {
        return cents >= 1 && cents <= 1_000_000;
    }

    public static boolean isValidCoupon(String coupon) {
        if (coupon == null || coupon.isEmpty()) return true;
        return coupon.matches("[A-Z0-9]{4,10}");
    }

    public static String validateOrder(String id, int cents, String coupon) {
        if (!isValidId(id)) return "BAD_ID";
        if (!isValidAmount(cents)) return "BAD_AMOUNT";
        if (!isValidCoupon(coupon)) return "BAD_COUPON";
        return "OK";
    }
}
""",
    wrong=r"""
public class Solution {
    public static boolean isValidId(String id) {
        return id != null && id.length() >= 3 && id.length() <= 20;
    }

    public static boolean isValidAmount(int cents) {
        return cents >= 1 && cents <= 1_000_000;
    }

    public static boolean isValidCoupon(String coupon) {
        if (coupon == null || coupon.isEmpty()) return true;
        return coupon.matches("[A-Z0-9]{4,10}");
    }

    // W: checks the coupon BEFORE the amount — wrong precedence, so a
    // request with both an empty amount and a bad coupon reports
    // BAD_COUPON instead of BAD_AMOUNT.
    public static String validateOrder(String id, int cents, String coupon) {
        if (!isValidId(id)) return "BAD_ID";
        if (!isValidCoupon(coupon)) return "BAD_COUPON";
        if (!isValidAmount(cents)) return "BAD_AMOUNT";
        return "OK";
    }
}
""",
)
