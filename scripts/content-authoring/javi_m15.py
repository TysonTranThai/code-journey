#!/usr/bin/env python3
"""Java — Intermediate — Module 15: java-inter-capstone.

The capstone: a layered expense tracker that integrates the course —
records, generics/collections, streams, repository pattern, exception
architecture, and testable seams. Three challenges ladder up the final
system; the checkpoint grades the integrated whole. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-inter-capstone"

# ── lesson 15.1 — capstone brief ───────────────────────────────────────────
L_BRIEF_EN = r"""
## Capstone: the Expense Tracker

You will assemble a small but *real* system. The domain: expenses with
categories; the report layer answers money questions; persistence hides
behind a repository interface.

```
ReportService → ExpenseRepository (interface) → InMemoryExpenseRepository
      ↓ uses
Money / Category value types, Expense record
```

Everything you built this course appears:
- **records + validation** (Module 1): Expense refuses bad data at birth
- **interfaces + injection** (Modules 2, 12): the service never sees the
  in-memory map
- **generics + collections** (Modules 3–4): typed repositories, comparators
- **streams/collectors** (Module 5): the report layer groups and totals
- **exception architecture** (Module 6): domain exceptions carry data
- **testing** (Module 8): every graded test is a boundary net
- **architecture** (Module 12): DTO-shaped report rows leave the service

The three challenges below are milestones; the checkpoint is the
integrated system.
"""

L_BRIEF_VI = r"""
## Capstone: bộ theo dõi chi tiêu

Bạn sẽ lắp ráp một hệ thống nhỏ nhưng *thật*. Domain: chi tiêu theo hạng
mục; tầng báo cáo trả lời các câu hỏi về tiền; persistence giấu sau một
interface repository.

```
ReportService → ExpenseRepository (interface) → InMemoryExpenseRepository
      ↓ dùng
Money / Category value type, record Expense
```

Mọi thứ bạn xây trong khóa học đều xuất hiện:
- **record + kiểm tra** (Module 1): Expense chặn dữ liệu xấu ngay khi sinh
- **interface + tiêm** (Module 2, 12): service không bao giờ thấy map
  trong bộ nhớ
- **generic + collection** (Module 3–4): repository có kiểu, comparator
- **stream/collector** (Module 5): tầng báo cáo nhóm và tính tổng
- **kiến trúc exception** (Module 6): exception domain mang dữ liệu
- **kiểm thử** (Module 8): mọi test chấm điểm là một lưới biên
- **kiến trúc** (Module 12): dòng báo cáo hình DTO rời service

Ba thử thách dưới đây là các cột mốc; checkpoint là hệ thống tích hợp.
"""

# ── lesson 15.2 — reading the system ───────────────────────────────────────
L_READ_EN = r"""
## Reading the system you built

After the capstone, walk the code like a reviewer:

1. **Where are the rules?** Every money rule should live in the service
   or the domain type — not the controller, not the repository.
2. **What does each test net catch?** If you deleted a boundary test,
   which regression would slip through? (If none, the test is dead.)
3. **What would change first?** Swapping persistence should be one
   constructor line. Adding a report should be one service method. If
   either needs surgery, the boundaries leak.
4. **Where does it hurt?** The rule you had to duplicate is the next
   extraction candidate.

This is the intermediate→advanced turn: advanced engineers don't just
build systems — they read their own systems for the stresses that will
shape the next refactor.
"""

L_READ_VI = r"""
## Đọc lại hệ thống bạn vừa xây

Sau capstone, đi qua code như một reviewer:

1. **Quy tắc nằm ở đâu?** Mọi quy tắc tiền phải nằm ở service hoặc kiểu
   domain — không phải controller, không phải repository.
2. **Mỗi lưới test bắt được gì?** Nếu xóa một test biên, lỗi hồi quy nào
   sẽ lọt qua? (Nếu không có, test đó đã chết.)
3. **Thứ gì sẽ đổi đầu tiên?** Hoán đổi persistence phải là một dòng
   constructor. Thêm báo cáo phải là một method service. Nếu cái nào cần
   phẫu thuật, ranh giới đang rò.
4. **Nơi nào đau?** Quy tắc bạn phải nhân bản là ứng cử viên tách tiếp
   theo.

Đây là bước ngoặt trung-cấp→nâng-cao: kỹ sư nâng cao không chỉ xây hệ
thống — họ đọc chính hệ thống của mình để tìm áp lực sẽ định hình lần
refactor kế tiếp.
"""

write_module(
    MOD,
    "Capstone: Expense Tracker",
    "Integrate the whole course into a layered expense tracker — validated records, injected repositories, stream reports, and boundary-tested rules.",
    "Capstone: Bộ theo dõi chi tiêu",
    "Tích hợp cả khóa học vào một bộ theo dõi chi tiêu phân lớp — record có kiểm tra, repository được tiêm, báo cáo bằng stream, và quy tắc test biên.",
    ["javi-capstone-brief", "reading-the-system", "javi-checkpoint-capstone"],
    ["javi-p15-capstone"],
)

write_lesson(MOD, "javi-capstone-brief", "Capstone Brief", "The system map, which modules surface where, and the milestone ladder.", 12, L_BRIEF_EN, "Thông điệp capstone", "Sơ đồ hệ thống, module nào xuất hiện ở đâu, và thang cột mốc.", L_BRIEF_VI)

write_lesson(MOD, "reading-the-system", "Reading the System", "Reviewer questions for your own code: where rules live, what each test catches, what changes first.", 11, L_READ_EN, "Đọc lại hệ thống", "Câu hỏi reviewer cho chính code của bạn: quy tắc ở đâu, mỗi test bắt gì, cái gì đổi trước.", L_READ_VI)

# ── practice set ────────────────────────────────────────────────────────────
P15_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P15_EXPENSE = challenge(
    "javi-p15-expense-domain",
    "Milestone 1: Validated Domain",
    r"""Build the domain in `Solution`:
- `static class InvalidExpenseException extends RuntimeException` —
  carries `String problem` (getter).
- `record Expense(String id, String category, int cents)`:
  - constructor validates: id/category non-blank, cents > 0 — failures
    throw InvalidExpenseException with a specific problem message
    (e.g. `"blank category"`, `"non-positive cents"`)
- `Expense` is a hash-contract value type (records already are — note
  WHY in a comment).

This is Module 1 + 6 fused: fail fast, exceptions carry data.""",
    P15_BOILER,
    [
        (
            "valid expense constructs",
            r"""
Solution.Expense e = new Solution.Expense("e1", "food", 1200);
checkEq(e.cents(), 1200, "fields held");
""",
            "Happy path stores all fields.",
        ),
        (
            "invalid data rejected with reasons",
            r"""
try { new Solution.Expense("e1", "  ", 100); checkTrue(false, "must throw"); }
catch (Solution.InvalidExpenseException ex) {
    checkEq(ex.problem(), "blank category", "reasoned");
}
try { new Solution.Expense("e1", "food", 0); checkTrue(false, "must throw"); }
catch (Solution.InvalidExpenseException ex) {
    checkEq(ex.problem(), "non-positive cents", "reasoned");
}
""",
            "Each rule violation names itself.",
        ),
    ],
    level="independent",
)

CH_P15_REPO = challenge(
    "javi-p15-expense-repo",
    "Milestone 2: The Repository",
    r"""Add persistence behind an interface in `Solution`:
- `interface ExpenseStore { void save(Solution.Expense e); Optional<Solution.Expense> find(String id); List<Solution.Expense> all(); }`
  (referencing the nested record as `Solution.Expense` — inside Solution
  you can write `Expense` directly)
- `static class InMemoryExpenseStore implements ExpenseStore`
  (insertion order preserved)
- `static class DuplicateExpenseException extends RuntimeException`
- `ExpenseStore.save` throws DuplicateExpenseException when a DIFFERENT
  expense already occupies the id (idempotent identical re-save is
  fine); note: category may legitimately change on update — id is the
  only conflict dimension.

Two saves with the same id but different cents = update, allowed.
Same id, different category = conflict, throw.""",
    P15_BOILER,
    [
        (
            "save/find/all roundtrip",
            r"""
Solution.InMemoryExpenseStore s = new Solution.InMemoryExpenseStore();
s.save(new Solution.Expense("a", "food", 100));
checkEq(s.find("a").orElseThrow().cents(), 100, "found");
checkEq(s.all().size(), 1, "one row");
""",
            "Basic storage contract.",
        ),
        (
            "same-id update allowed",
            r"""
Solution.InMemoryExpenseStore s = new Solution.InMemoryExpenseStore();
s.save(new Solution.Expense("a", "food", 100));
s.save(new Solution.Expense("a", "food", 250));
checkEq(s.find("a").orElseThrow().cents(), 250, "updated in place");
checkEq(s.all().size(), 1, "still one row");
""",
            "Upsert semantics on identical category.",
        ),
        (
            "category conflict throws",
            r"""
Solution.InMemoryExpenseStore s = new Solution.InMemoryExpenseStore();
s.save(new Solution.Expense("a", "food", 100));
try { s.save(new Solution.Expense("a", "travel", 100)); checkTrue(false, "must throw"); }
catch (Solution.DuplicateExpenseException ex) { checkTrue(true, "conflict caught"); }
""",
            "An id is bound to one category.",
        ),
    ],
    level="independent",
)

CH_P15_REPORT = challenge(
    "javi-p15-expense-report",
    "Milestone 3: Stream Reports",
    r"""Add the report layer in `Solution` (types from milestones 1–2 are
available):
- `static int totalForCategory(Solution.ExpenseStore store,
  String category)` — sum of that category's cents.
- `static List<String> categoryTotals(Solution.ExpenseStore store)` —
  one `"category:cents"` line per category, sorted by category name,
  categories with zero expenses (never saved) excluded.
- `static Optional<String> biggestSpend(Solution.ExpenseStore store)` —
  the expense id with the highest cents (ties: lexicographically
  smallest id); empty store → Optional.empty().

Use streams with groupingBy/reducing or toMap merges — the point is
expressing aggregation declaratively.""",
    P15_BOILER,
    [
        (
            "category totals",
            r"""
Solution.InMemoryExpenseStore s = new Solution.InMemoryExpenseStore();
s.save(new Solution.Expense("a", "food", 100));
s.save(new Solution.Expense("b", "food", 50));
s.save(new Solution.Expense("c", "travel", 200));
checkEq(Solution.categoryTotals(s), List.of("food:150", "travel:200"), "grouped and summed");
""",
            "groupingBy + summingInt, keys sorted.",
        ),
        (
            "single category total",
            r"""
Solution.InMemoryExpenseStore s = new Solution.InMemoryExpenseStore();
s.save(new Solution.Expense("a", "food", 100));
checkEq(Solution.totalForCategory(s, "food"), 100, "the one food expense");
checkEq(Solution.totalForCategory(s, "travel"), 0, "absent category");
""",
            "Unknown category totals to 0.",
        ),
        (
            "biggest spend with tie-break",
            r"""
Solution.InMemoryExpenseStore s = new Solution.InMemoryExpenseStore();
s.save(new Solution.Expense("b", "food", 500));
s.save(new Solution.Expense("a", "travel", 500));
checkEq(Solution.biggestSpend(s).orElseThrow(), "a", "tie → smaller id");
""",
            "Max cents, then min id.",
        ),
        (
            "empty store",
            r"""
checkEq(Solution.biggestSpend(new Solution.InMemoryExpenseStore()).isPresent(), false, "empty → empty");
""",
            "Optional.empty on no data.",
        ),
    ],
    level="real-world",
)

VI_CH_P15_EXPENSE = vi_challenge(
    "Cột mốc 1: domain có kiểm tra",
    r"""Xây domain trong `Solution`:
- `static class InvalidExpenseException extends RuntimeException` —
  mang `String problem` (getter).
- `record Expense(String id, String category, int cents)`:
  - constructor kiểm tra: id/category khác rỗng, cents > 0 — lỗi thì ném
    InvalidExpenseException với message nêu rõ lý do (ví dụ
    `"blank category"`, `"non-positive cents"`)
- `Expense` là kiểu giá trị đúng hợp đồng hash (record vốn vậy — viết
  comment GIẢI THÍCH vì sao).

Đây là Module 1 + 6 hòa quyện: fail fast, exception mang dữ liệu.""",
    [
        ("Chi tiêu hợp lệ được dựng", "Hướng bình thường lưu đủ field."),
        ("Dữ liệu lỗi bị chặn kèm lý do", "Mỗi vi phạm quy tắc tự nêu tên."),
    ],
)

VI_CH_P15_REPO = vi_challenge(
    "Cột mốc 2: repository",
    r"""Thêm persistence sau một interface trong `Solution`:
- `interface ExpenseStore { void save(Expense e); Optional<Expense> find(String id); List<Expense> all(); }`
- `static class InMemoryExpenseStore implements ExpenseStore`
  (giữ thứ tự chèn)
- `static class DuplicateExpenseException extends RuntimeException`
- `ExpenseStore.save` ném DuplicateExpenseException khi một expense
  KHÁC đã chiếm id (re-save giống hệt là idempotent, ổn); lưu ý:
  category được phép đổi khi cập nhật — id là chiều xung đột duy nhất.

Hai lần save cùng id nhưng cents khác = cập nhật, được phép.
Cùng id, khác category = xung đột, ném.""",
    [
        ("Save/find/all trọn vòng", "Hợp đồng lưu trữ cơ bản."),
        ("Cập nhật cùng id được phép", "Ngữ nghĩa upsert trên cùng category."),
        ("Xung đột category ném", "Một id gắn với một category."),
    ],
)

VI_CH_P15_REPORT = vi_challenge(
    "Cột mốc 3: báo cáo bằng stream",
    r"""Thêm tầng báo cáo trong `Solution` (kiểu từ cột mốc 1–2 có sẵn):
- `static int totalForCategory(ExpenseStore store, String category)` —
  tổng cents của hạng mục đó.
- `static List<String> categoryTotals(ExpenseStore store)` — một dòng
  `"category:cents"` mỗi hạng mục, sắp theo tên hạng mục, loại bỏ hạng
  mục không có chi tiêu nào.
- `static Optional<String> biggestSpend(ExpenseStore store)` — id chi
  tiêu có cents cao nhất (hòa: id nhỏ hơn theo bảng chữ cái thắng);
  store rỗng → Optional.empty().

Dùng stream với groupingBy/reducing hoặc merge toMap — điểm nhấn là
diễn đạt phép tổng hợp một cách khai báo.""",
    [
        ("Tổng theo hạng mục", "groupingBy + summingInt, key đã sắp."),
        ("Tổng một hạng mục", "Một chi tiêu food 100 → tổng 100; hạng mục lạ cộng về 0."),
        ("Chi tiêu lớn nhất với tie-break", "Max cents, rồi min id."),
        ("Store rỗng", "Optional.empty khi không có dữ liệu."),
    ],
)

write_practice(
    MOD,
    "javi-p15-capstone",
    "Capstone Milestones",
    "Domain → repository → reports: the three milestones of the integrated expense tracker.",
    "Cột mốc capstone",
    "Domain → repository → báo cáo: ba cột mốc của bộ theo dõi chi tiêu tích hợp.",
    "javi-capstone-brief",
    45,
    "intermediate",
    [CH_P15_EXPENSE, CH_P15_REPO, CH_P15_REPORT],
    {CH_P15_EXPENSE["id"]: VI_CH_P15_EXPENSE, CH_P15_REPO["id"]: VI_CH_P15_REPO, CH_P15_REPORT["id"]: VI_CH_P15_REPORT},
    solutions=[
        (
            CH_P15_EXPENSE["id"],
            r"""
public class Solution {
    public static class InvalidExpenseException extends RuntimeException {
        private final String problem;
        public InvalidExpenseException(String problem) {
            super(problem);
            this.problem = problem;
        }
        public String problem() { return problem; }
    }

    public record Expense(String id, String category, int cents) {
        public Expense {
            // Records give value semantics: correct equals/hashCode for
            // free — that's WHY no manual contract code is needed here.
            if (id == null || id.isBlank()) throw new InvalidExpenseException("blank id");
            if (category == null || category.isBlank()) throw new InvalidExpenseException("blank category");
            if (cents <= 0) throw new InvalidExpenseException("non-positive cents");
        }
    }
}
""",
            r"""
public class Solution {
    public static class InvalidExpenseException extends RuntimeException {
        private final String problem;
        public InvalidExpenseException(String problem) {
            super(problem);
            this.problem = problem;
        }
        public String problem() { return problem; }
    }

    // W: validates only the FIRST rule and its message is a constant —
    // blank categories pass through and every failure reports "bad".
    public record Expense(String id, String category, int cents) {
        public Expense {
            if (id == null || id.isBlank()) throw new InvalidExpenseException("bad");
        }
    }
}
""",
        ),
        (
            CH_P15_REPO["id"],
            r"""
import java.util.*;

public class Solution {
    public record Expense(String id, String category, int cents) {}

    public interface ExpenseStore {
        void save(Expense e);
        Optional<Expense> find(String id);
        List<Expense> all();
    }

    public static class DuplicateExpenseException extends RuntimeException {
        public DuplicateExpenseException(String m) { super(m); }
    }

    public static class InMemoryExpenseStore implements ExpenseStore {
        private final Map<String, Expense> store = new LinkedHashMap<>();

        @Override public void save(Expense e) {
            Expense old = store.get(e.id());
            if (old != null && !old.category().equals(e.category())) {
                throw new DuplicateExpenseException("category conflict for " + e.id());
            }
            store.put(e.id(), e);
        }

        @Override public Optional<Expense> find(String id) { return Optional.ofNullable(store.get(id)); }
        @Override public List<Expense> all() { return new ArrayList<>(store.values()); }
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public record Expense(String id, String category, int cents) {}

    public interface ExpenseStore {
        void save(Expense e);
        Optional<Expense> find(String id);
        List<Expense> all();
    }

    public static class DuplicateExpenseException extends RuntimeException {
        public DuplicateExpenseException(String m) { super(m); }
    }

    public static class InMemoryExpenseStore implements ExpenseStore {
        private final Map<String, Expense> store = new LinkedHashMap<>();

        // W: ANY re-save throws — legitimate cent updates are rejected,
        // so upsert semantics are gone.
        @Override public void save(Expense e) {
            if (store.containsKey(e.id())) {
                throw new DuplicateExpenseException("duplicate " + e.id());
            }
            store.put(e.id(), e);
        }

        @Override public Optional<Expense> find(String id) { return Optional.ofNullable(store.get(id)); }
        @Override public List<Expense> all() { return new ArrayList<>(store.values()); }
    }
}
""",
        ),
        (
            CH_P15_REPORT["id"],
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Expense(String id, String category, int cents) {}

    public static class InMemoryExpenseStore {
        private final Map<String, Expense> store = new LinkedHashMap<>();
        public void save(Expense e) { store.put(e.id(), e); }
        public Optional<Expense> find(String id) { return Optional.ofNullable(store.get(id)); }
        public List<Expense> all() { return new ArrayList<>(store.values()); }
    }

    public static int totalForCategory(InMemoryExpenseStore store, String category) {
        return store.all().stream()
            .filter(e -> e.category().equals(category))
            .mapToInt(Expense::cents)
            .sum();
    }

    public static List<String> categoryTotals(InMemoryExpenseStore store) {
        return store.all().stream()
            .collect(Collectors.groupingBy(Expense::category,
                Collectors.summingInt(Expense::cents)))
            .entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .map(e -> e.getKey() + ":" + e.getValue())
            .collect(Collectors.toList());
    }

    public static Optional<String> biggestSpend(InMemoryExpenseStore store) {
        return store.all().stream()
            .max(Comparator.comparingInt(Expense::cents)
                .thenComparing(Expense::id, Comparator.reverseOrder()))
            .map(Expense::id);
    }
}
""",
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Expense(String id, String category, int cents) {}

    public static class InMemoryExpenseStore {
        private final Map<String, Expense> store = new LinkedHashMap<>();
        public void save(Expense e) { store.put(e.id(), e); }
        public Optional<Expense> find(String id) { return Optional.ofNullable(store.get(id)); }
        public List<Expense> all() { return new ArrayList<>(store.values()); }
    }

    public static int totalForCategory(InMemoryExpenseStore store, String category) {
        return store.all().stream()
            .filter(e -> e.category().equals(category))
            .mapToInt(Expense::cents)
            .sum();
    }

    public static List<String> categoryTotals(InMemoryExpenseStore store) {
        return store.all().stream()
            .collect(Collectors.groupingBy(Expense::category,
                Collectors.summingInt(Expense::cents)))
            .entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .map(e -> e.getKey() + ":" + e.getValue())
            .collect(Collectors.toList());
    }

    // W: tie-break is REVERSED — equal cents pick the LARGEST id, so
    // "b" beats "a" on ties. The deterministic tie-break contract breaks.
    public static Optional<String> biggestSpend(InMemoryExpenseStore store) {
        return store.all().stream()
            .max(Comparator.comparingInt(Expense::cents)
                .thenComparing(Expense::id))
            .map(Expense::id);
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — the integrated system

The full expense tracker, assembled. Failing this checkpoint means one
of the milestone contracts broke under integration — the tests will
name it.
"""

CP_MDX_VI = r"""
## Checkpoint — hệ thống tích hợp

Bộ theo dõi chi tiêu đầy đủ, đã lắp ráp. Trượt checkpoint này nghĩa là
một hợp đồng cột mốc đã vỡ khi tích hợp — test sẽ gọi tên nó.
"""

CH_CP15 = challenge(
    "javi-checkpoint-m15-capstone",
    "The Integrated Tracker",
    r"""Assemble the WHOLE tracker in `Solution` (you may reuse your
milestone code):
- `record Expense(String id, String category, int cents)` with
  constructor validation (blank id/category, non-positive cents throw
  `IllegalArgumentException` with a specific message)
- `interface ExpenseStore { void save(Expense e); Optional<Expense> find(String id);
  List<Expense> all(); }` + `InMemoryExpenseStore`
- `static class ExpenseService` with constructor `(ExpenseStore store)`:
  - `void add(String id, String category, int cents)` — constructs
    (letting validation throw), then saves
  - `Map<String, Integer> totalsByCategory()` — stream aggregation
  - `Optional<String> topExpense()` — highest cents, tie → smallest id

The checkpoint test drives the three layers together, exactly as the
milestones promised.""",
    r"""
import java.util.*;

public class Solution {
    // Assemble Expense, ExpenseStore, InMemoryExpenseStore, ExpenseService here.
}
""",
    [
        (
            "end-to-end add and total",
            r"""
Solution.InMemoryExpenseStore store = new Solution.InMemoryExpenseStore();
Solution.ExpenseService svc = new Solution.ExpenseService(store);
svc.add("e1", "food", 1000);
svc.add("e2", "food", 500);
svc.add("e3", "travel", 2000);
checkEq(svc.totalsByCategory(), Map.of("food", 1500, "travel", 2000), "aggregated");
""",
            "Service → validated record → store → stream report.",
        ),
        (
            "validation rejects through the stack",
            r"""
Solution.InMemoryExpenseStore store = new Solution.InMemoryExpenseStore();
Solution.ExpenseService svc = new Solution.ExpenseService(store);
try { svc.add("e1", "food", 0); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(e.getMessage().contains("cents"), "reasoned"); }
checkEq(store.all().size(), 0, "nothing saved");
""",
            "Bad data never reaches the store.",
        ),
        (
            "topExpense with tie-break",
            r"""
Solution.InMemoryExpenseStore store = new Solution.InMemoryExpenseStore();
Solution.ExpenseService svc = new Solution.ExpenseService(store);
svc.add("b", "food", 700);
svc.add("a", "travel", 700);
checkEq(svc.topExpense().orElseThrow(), "a", "tie → smaller id");
""",
            "Deterministic tie-breaking.",
        ),
        (
            "update flows through",
            r"""
Solution.InMemoryExpenseStore store = new Solution.InMemoryExpenseStore();
Solution.ExpenseService svc = new Solution.ExpenseService(store);
svc.add("e1", "food", 1000);
svc.add("e1", "food", 1200);
checkEq(svc.totalsByCategory(), Map.of("food", 1200), "updated total");
""",
            "Upsert visible in the report layer.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP15 = vi_challenge(
    "Bộ theo dõi tích hợp",
    r"""Lắp ráp TOÀN BỘ tracker trong `Solution` (được tái dùng code cột
mốc của bạn):
- `record Expense(String id, String category, int cents)` với kiểm tra
  constructor (id/category rỗng, cents không dương ném
  `IllegalArgumentException` kèm message cụ thể)
- `interface ExpenseStore { void save(Expense e); Optional<Expense> find(String id);
  List<Expense> all(); }` + `InMemoryExpenseStore`
- `static class ExpenseService` với constructor `(ExpenseStore store)`:
  - `void add(String id, String category, int cents)` — dựng record (để
    phần kiểm tra ném), rồi save
  - `Map<String, Integer> totalsByCategory()` — tổng hợp bằng stream
  - `Optional<String> topExpense()` — cents cao nhất, hòa → id nhỏ hơn

Test checkpoint điều khiển ba lớp cùng lúc, đúng như các cột mốc hứa.""",
    [
        ("Thêm và tổng trọn vẹn", "Service → record có kiểm tra → store → báo cáo stream."),
        ("Kiểm tra chặn xuyên suốt stack", "Dữ liệu xấu không bao giờ chạm store."),
        ("topExpense với tie-break", "Phân định hòa mang tính xác định."),
        ("Cập nhật chảy qua", "Upsert hiện rõ ở tầng báo cáo."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-capstone",
    "Checkpoint: The Integrated Tracker",
    "Graded checkpoint: the full three-layer expense tracker — validation, upsert, aggregation, and deterministic tie-breaks.",
    15,
    CP_MDX,
    "Checkpoint: Bộ theo dõi tích hợp",
    "Checkpoint chấm điểm: bộ theo dõi chi tiêu ba lớp trọn vẹn — kiểm tra, upsert, tổng hợp, và tie-break xác định.",
    CP_MDX_VI,
    CH_CP15,
    VI_CH_CP15,
    solution=r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Expense(String id, String category, int cents) {
        public Expense {
            if (id == null || id.isBlank()) throw new IllegalArgumentException("blank id");
            if (category == null || category.isBlank()) throw new IllegalArgumentException("blank category");
            if (cents <= 0) throw new IllegalArgumentException("non-positive cents");
        }
    }

    public interface ExpenseStore {
        void save(Expense e);
        Optional<Expense> find(String id);
        List<Expense> all();
    }

    public static class InMemoryExpenseStore implements ExpenseStore {
        private final Map<String, Expense> store = new LinkedHashMap<>();
        @Override public void save(Expense e) { store.put(e.id(), e); }
        @Override public Optional<Expense> find(String id) { return Optional.ofNullable(store.get(id)); }
        @Override public List<Expense> all() { return new ArrayList<>(store.values()); }
    }

    public static class ExpenseService {
        private final ExpenseStore store;
        public ExpenseService(ExpenseStore store) { this.store = store; }

        public void add(String id, String category, int cents) {
            store.save(new Expense(id, category, cents));
        }

        public Map<String, Integer> totalsByCategory() {
            return store.all().stream()
                .collect(Collectors.groupingBy(Expense::category,
                    Collectors.summingInt(Expense::cents)));
        }

        public Optional<String> topExpense() {
            return store.all().stream()
                .max(Comparator.comparingInt(Expense::cents)
                    .thenComparing(Expense::id, Comparator.reverseOrder()))
                .map(Expense::id);
        }
    }
}
""",
    wrong=r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public record Expense(String id, String category, int cents) {
        public Expense {
            if (id == null || id.isBlank()) throw new IllegalArgumentException("blank id");
            if (category == null || category.isBlank()) throw new IllegalArgumentException("blank category");
            if (cents <= 0) throw new IllegalArgumentException("non-positive cents");
        }
    }

    public interface ExpenseStore {
        void save(Expense e);
        Optional<Expense> find(String id);
        List<Expense> all();
    }

    public static class InMemoryExpenseStore implements ExpenseStore {
        private final Map<String, Expense> store = new LinkedHashMap<>();
        @Override public void save(Expense e) { store.put(e.id(), e); }
        @Override public Optional<Expense> find(String id) { return Optional.ofNullable(store.get(id)); }
        @Override public List<Expense> all() { return new ArrayList<>(store.values()); }
    }

    public static class ExpenseService {
        private final ExpenseStore store;
        public ExpenseService(ExpenseStore store) { this.store = store; }

        public void add(String id, String category, int cents) {
            store.save(new Expense(id, category, cents));
        }

        // W: totals count DISTINCT categories but ignore amounts —
        // every sum comes back as the number of expenses, not their total.
        public Map<String, Integer> totalsByCategory() {
            Map<String, Integer> out = new HashMap<>();
            for (Expense e : store.all()) out.put(e.category(), out.getOrDefault(e.category(), 0) + 1);
            return out;
        }

        public Optional<String> topExpense() {
            return store.all().stream()
                .max(Comparator.comparingInt(Expense::cents)
                    .thenComparing(Expense::id, Comparator.reverseOrder()))
                .map(Expense::id);
        }
    }
}
""",
)
