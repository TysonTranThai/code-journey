#!/usr/bin/env python3
"""Java — Intermediate — Module 11: java-persistence.

The repository pattern with an in-memory store (the sandbox has no JDBC
driver — lessons teach SQL/JDBC concepts honestly; challenges exercise
the *pattern* deterministically). House conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-persistence"

# ── lesson 11.1 — the repository pattern ────────────────────────────────────
L_REPO_EN = r"""
## The repository pattern

A repository makes persistence *look like* a collection of domain
objects, hiding the storage technology:

```java
public interface ExpenseRepository {
    Expense save(Expense e);            // insert or update
    Optional<Expense> findById(String id);
    List<Expense> findAll();
    List<Expense> findByCategory(String category);
    boolean deleteById(String id);
}
```

Service code depends on the interface. Production binds a JDBC
implementation; tests bind an in-memory one. That is dependency inversion
applied to data:

```java
final class InMemoryExpenseRepository implements ExpenseRepository {
    private final Map<String, Expense> store = new LinkedHashMap<>();
    public Expense save(Expense e) { store.put(e.id(), e); return e; }
    public Optional<Expense> findById(String id) { return Optional.ofNullable(store.get(id)); }
    ...
}
```

Benefits: services unit-test with zero infrastructure; the storage swap
is one constructor argument; queries are named domain operations, not
SQL strings leaking everywhere.
"""

L_REPO_VI = r"""
## Mẫu repository

Repository khiến persistence *trông như* một collection các đối tượng
domain, giấu công nghệ lưu trữ phía sau:

```java
public interface ExpenseRepository {
    Expense save(Expense e);            // insert hoặc update
    Optional<Expense> findById(String id);
    List<Expense> findAll();
    List<Expense> findByCategory(String category);
    boolean deleteById(String id);
}
```

Code service phụ thuộc interface. Production gắn hiện thực JDBC; test
gắn bản trong bộ nhớ. Đó là dependency inversion áp dụng cho dữ liệu:

```java
final class InMemoryExpenseRepository implements ExpenseRepository {
    private final Map<String, Expense> store = new LinkedHashMap<>();
    public Expense save(Expense e) { store.put(e.id(), e); return e; }
    public Optional<Expense> findById(String id) { return Optional.ofNullable(store.get(id)); }
    ...
}
```

Lợi ích: service unit test với hạ tầng bằng không; hoán đổi storage chỉ
là một tham số constructor; truy vấn là thao tác domain có tên, không
phải chuỗi SQL rải khắp nơi.
"""

# ── lesson 11.2 — JDBC concepts ────────────────────────────────────────────
L_JDBC_EN = r"""
## JDBC concepts (what your repository would wrap)

The sandbox has no database driver, but the JDBC *shape* is essential
knowledge — here is the canonical safe pattern you'd implement:

```java
public Optional<Expense> findById(String id) {
    String sql = "SELECT id, category, cents FROM expenses WHERE id = ?";
    try (Connection c = dataSource.getConnection();
         PreparedStatement ps = c.prepareStatement(sql)) {
        ps.setString(1, id);                       // bind, NEVER concatenate
        try (ResultSet rs = ps.executeQuery()) {
            if (rs.next()) {
                return Optional.of(new Expense(rs.getString("id"),
                    rs.getString("category"), rs.getInt("cents")));
            }
            return Optional.empty();
        }
    } catch (SQLException e) {
        throw new StorageException("expense lookup failed", e);  // translate (Module 6)
    }
}
```

The four non-negotiables:
1. **PreparedStatement with `?` placeholders** — the only defense against
   SQL injection; concatenating user input is the vulnerability itself.
2. **try-with-resources** — Connection/Statement/ResultSet are all
   AutoCloseable; leaks exhaust connection pools.
3. **Transactions** — multi-statement work needs
   `c.setAutoCommit(false)` … `commit()`/`rollback()`.
4. **Translate SQLException** at the repository boundary.

Connection pooling (HikariCP et al.) exists because connections are
expensive — the repository *borrows* from the pool via a DataSource, it
never constructs raw connections.
"""

L_JDBC_VI = r"""
## Khái niệm JDBC (thứ repository của bạn sẽ bọc)

Sandbox không có driver database, nhưng *dáng* JDBC là kiến thức bắt buộc
— đây là mẫu an toàn kinh điển bạn sẽ hiện thực:

```java
public Optional<Expense> findById(String id) {
    String sql = "SELECT id, category, cents FROM expenses WHERE id = ?";
    try (Connection c = dataSource.getConnection();
         PreparedStatement ps = c.prepareStatement(sql)) {
        ps.setString(1, id);                       // bind, KHÔNG BAO GIỜ nối chuỗi
        try (ResultSet rs = ps.executeQuery()) {
            if (rs.next()) {
                return Optional.of(new Expense(rs.getString("id"),
                    rs.getString("category"), rs.getInt("cents")));
            }
            return Optional.empty();
        }
    } catch (SQLException e) {
        throw new StorageException("expense lookup failed", e);  // chuyển dịch (Module 6)
    }
}
```

Bốn điều không thể thương lượng:
1. **PreparedStatement với placeholder `?`** — phòng tuyến duy nhất chống
   SQL injection; nối input người dùng chính là lỗ hổng.
2. **try-with-resources** — Connection/Statement/ResultSet đều là
   AutoCloseable; rò rỉ cạn kiệt connection pool.
3. **Transaction** — công việc nhiều câu lệnh cần
   `c.setAutoCommit(false)` … `commit()`/`rollback()`.
4. **Chuyển dịch SQLException** tại ranh giới repository.

Connection pooling (HikariCP và tương tự) tồn tại vì connection đắt đỏ —
repository *mượn* từ pool qua một DataSource, không bao giờ tự tạo
connection thô.
"""

# ── lesson 11.3 — modeling relations ───────────────────────────────────────
L_REL_EN = r"""
## Modeling relations without a database

SQL thinking transfers directly to repository design:

- **Primary key** → the map key (id), unique and immutable
- **Foreign key** → a field referencing another aggregate's id
  (`Expense.categoryId()`)
- **JOIN** → a method that combines repositories or a denormalized view
- **UNIQUE constraint** → the store checks and rejects duplicates
  (`save` throws on conflicting email)
- **INDEX** → a secondary `Map<String, List<Expense>>` byCategory, kept
  consistent on every write

That last one is the deep idea: an index is a *derived* structure. Every
write path must maintain it — the classic bug is updating the main store
and forgetting the index:

```java
public Expense save(Expense e) {
    Expense old = store.put(e.id(), e);
    if (old != null) byCategory.get(old.category()).remove(old);
    byCategory.computeIfAbsent(e.category(), k -> new ArrayList<>()).add(e);
    return e;
}
```

Rebuilding indexes on read (`findAll` filters on the fly) is correct but
O(n) per query — the tradeoff databases charge you for.
"""

L_REL_VI = r"""
## Mô hình hóa quan hệ không cần database

Tư duy SQL chuyển thẳng sang thiết kế repository:

- **Primary key** → key của map (id), duy nhất và bất biến
- **Foreign key** → field tham chiếu id của aggregate khác
  (`Expense.categoryId()`)
- **JOIN** → method kết hợp các repository hoặc một view phi chuẩn hóa
- **Ràng buộc UNIQUE** → store kiểm tra và chặn trùng lặp
  (`save` ném khi email xung đột)
- **INDEX** → một `Map<String, List<Expense>>` byCategory phụ, được giữ
  nhất quán ở mọi lần ghi

Ý sâu ở mục cuối: index là cấu trúc *dẫn xuất*. Mọi đường ghi phải duy
trì nó — bug kinh điển là cập nhật store chính rồi quên index:

```java
public Expense save(Expense e) {
    Expense old = store.put(e.id(), e);
    if (old != null) byCategory.get(old.category()).remove(old);
    byCategory.computeIfAbsent(e.category(), k -> new ArrayList<>()).add(e);
    return e;
}
```

Xây lại index lúc đọc (`findAll` lọc tại chỗ) thì đúng nhưng O(n) mỗi
truy vấn — cái giá mà database tính cho bạn.
"""

write_module(
    MOD,
    "Persistence & Repositories",
    "The repository pattern, the JDBC shape it wraps (placeholders, transactions, translation), and index maintenance in stores.",
    "Persistence & Repository",
    "Mẫu repository, dáng JDBC mà nó bọc (placeholder, transaction, chuyển dịch), và duy trì index trong store.",
    ["javi-repository-pattern", "jdbc-shape", "relations-indexes", "javi-checkpoint-persistence"],
    ["javi-p11-persistence"],
)

write_lesson(MOD, "javi-repository-pattern", "The Repository Pattern", "Domain-shaped queries behind an interface, in-memory implementations, and storage as an injected dependency.", 14, L_REPO_EN, "Mẫu repository", "Truy vấn mang hình domain sau một interface, hiện thực trong bộ nhớ, và storage như một phụ thuộc được tiêm.", L_REPO_VI)

write_lesson(MOD, "jdbc-shape", "The JDBC Shape", "PreparedStatement placeholders, try-with-resources on connections, transactions, and SQLException translation — the pattern real repositories wrap.", 15, L_JDBC_EN, "Dáng JDBC", "Placeholder PreparedStatement, try-with-resources cho connection, transaction, và chuyển dịch SQLException — mẫu mà repository thật bọc.", L_JDBC_VI)

write_lesson(MOD, "relations-indexes", "Relations & Indexes", "Primary keys, foreign keys, and secondary indexes as derived structures every write must maintain.", 14, L_REL_EN, "Quan hệ & Index", "Primary key, foreign key, và secondary index là cấu trúc dẫn xuất mà mọi lần ghi phải duy trì.", L_REL_VI)

# ── practice set ────────────────────────────────────────────────────────────
P11_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P11_REPO = challenge(
    "javi-p11-expense-repo",
    "In-Memory Expense Repository",
    r"""Implement in `Solution`:
- `record Expense(String id, String category, int cents)`
- `static class ExpenseRepository` with:
  - `Expense save(Expense e)` (upsert by id)
  - `Optional<Expense> findById(String id)`
  - `List<Expense> findByCategory(String category)` (insertion order)
  - `boolean deleteById(String id)`
  - `List<Expense> findAll()` (insertion order)
  - `int totalCents()`
- `static class DuplicateExpenseException extends RuntimeException`.

`save` acts as a category-guarded upsert: same id + same category
replaces the entry (updates allowed); same id + DIFFERENT category
throws DuplicateExpenseException (an id is bound to one category).""",
    P11_BOILER,
    [
        (
            "save and findById",
            r"""
Solution.ExpenseRepository r = new Solution.ExpenseRepository();
r.save(new Solution.Expense("e1", "food", 1200));
checkEq(r.findById("e1").orElseThrow().cents(), 1200, "roundtrip");
""",
            "Save then fetch returns the same expense.",
        ),
        (
            "upsert replaces",
            r"""
Solution.ExpenseRepository r = new Solution.ExpenseRepository();
r.save(new Solution.Expense("e1", "food", 1200));
r.save(new Solution.Expense("e1", "food", 1500));
checkEq(r.findById("e1").orElseThrow().cents(), 1500, "updated");
checkEq(r.findAll().size(), 1, "still one row");
""",
            "Same id, identical data → idempotent replace.",
        ),
        (
            "conflicting duplicate rejected",
            r"""
Solution.ExpenseRepository r = new Solution.ExpenseRepository();
r.save(new Solution.Expense("e1", "food", 1200));
try { r.save(new Solution.Expense("e1", "travel", 900)); checkTrue(false, "must throw"); }
catch (Solution.DuplicateExpenseException ex) { checkTrue(true, "rejected"); }
""",
            "Same id with different data is a conflict.",
        ),
        (
            "findByCategory filters",
            r"""
Solution.ExpenseRepository r = new Solution.ExpenseRepository();
r.save(new Solution.Expense("a", "food", 100));
r.save(new Solution.Expense("b", "travel", 200));
r.save(new Solution.Expense("c", "food", 300));
checkEq(r.findByCategory("food").size(), 2, "two foods");
checkEq(r.totalCents(), 600, "sum all");
""",
            "Category index filters; total sums everything.",
        ),
        (
            "delete removes",
            r"""
Solution.ExpenseRepository r = new Solution.ExpenseRepository();
r.save(new Solution.Expense("a", "food", 100));
checkEq(r.deleteById("a"), true, "existed");
checkEq(r.deleteById("a"), false, "already gone");
""",
            "True on first delete, false afterwards.",
        ),
    ],
    level="independent",
)

CH_P11_SAFE_SQL = challenge(
    "javi-p11-safe-queries",
    "Build (Conceptually) Safe Queries",
    r"""A SQL-builder exercise without a database. Implement in `Solution`:
- `record Param(String value)`
- `static String buildFind(String table, Param id)` returning
  `"SELECT * FROM " + table + " WHERE id = ?"` — the placeholder, NOT
  the value (demonstrating parameter binding).
- `static String buildFindUnsafe(String table, String id)` returning the
  concatenated version `"SELECT * FROM " + table + " WHERE id = '" + id + "'"`.

The tests demonstrate the attack: an id of `x' OR '1'='1` produces a
harmless placeholder string in the safe builder and a *broken/injected*
query in the unsafe one — making the vulnerability visible.""",
    P11_BOILER,
    [
        (
            "safe builder binds, never interpolates",
            r"""
checkEq(Solution.buildFind("users", new Solution.Param("x' OR '1'='1")),
        "SELECT * FROM users WHERE id = ?", "placeholder only");
""",
            "The payload never enters the SQL text.",
        ),
        (
            "unsafe builder demonstrates the injection",
            r"""
String sql = Solution.buildFindUnsafe("users", "x' OR '1'='1");
checkEq(sql, "SELECT * FROM users WHERE id = 'x' OR '1'='1'", "injected shape");
""",
            "The payload alters the query's meaning — the attack, made visible.",
        ),
        (
            "safe with normal id",
            r"""
checkEq(Solution.buildFind("users", new Solution.Param("u1")),
        "SELECT * FROM users WHERE id = ?", "normal path");
""",
            "Placeholder regardless of the value.",
        ),
    ],
    level="guided",
)

CH_P11_INDEX = challenge(
    "javi-p11-index-sync",
    "Keep the Index Honest",
    r"""Extend the repository idea: an indexed store where every write
maintains a secondary index. Implement in `Solution`:
- `record Book(String isbn, String genre)`
- `static class IndexedStore` with `save(Book b)` (upsert),
  `List<Book> byGenre(String genre)` (insertion order), `int size()`,
  and `remove(String isbn)` (boolean).

The index is the contract: `byGenre` must NEVER return a book that was
updated to another genre, re-saved, or removed. Upserting must move the
book between index buckets — the exact bug from the lesson.""",
    P11_BOILER,
    [
        (
            "genre index groups",
            r"""
Solution.IndexedStore s = new Solution.IndexedStore();
s.save(new Solution.Book("1", "scifi"));
s.save(new Solution.Book("2", "fantasy"));
checkEq(s.byGenre("scifi").size(), 1, "one scifi");
checkEq(s.size(), 2, "two books");
""",
            "Buckets reflect the stored data.",
        ),
        (
            "upsert moves buckets",
            r"""
Solution.IndexedStore s = new Solution.IndexedStore();
s.save(new Solution.Book("1", "scifi"));
s.save(new Solution.Book("1", "fantasy"));   // genre changed
checkEq(s.byGenre("scifi").size(), 0, "old bucket empty");
checkEq(s.byGenre("fantasy").size(), 1, "new bucket has it");
""",
            "The stale-index bug: old bucket must lose the entry.",
        ),
        (
            "remove clears the index",
            r"""
Solution.IndexedStore s = new Solution.IndexedStore();
s.save(new Solution.Book("1", "scifi"));
checkEq(s.remove("1"), true, "removed");
checkEq(s.byGenre("scifi").size(), 0, "index clean");
""",
            "Removal must touch the index too.",
        ),
    ],
    level="independent",
)

VI_CH_P11_REPO = vi_challenge(
    "Expense repository trong bộ nhớ",
    r"""Cài trong `Solution`:
- `record Expense(String id, String category, int cents)`
- `static class ExpenseRepository` với:
  - `Expense save(Expense e)` (upsert theo id)
  - `Optional<Expense> findById(String id)`
  - `List<Expense> findByCategory(String category)` (thứ tự chèn)
  - `boolean deleteById(String id)`
  - `List<Expense> findAll()` (thứ tự chèn)
  - `int totalCents()`
- `static class DuplicateExpenseException extends RuntimeException`.

`save` ném DuplicateExpenseException khi có expense KHÁC với cùng id
(cùng id + category/cents bằng nhau = re-save idempotent, được phép).""",
    [
        ("Save rồi findById", "Save rồi fetch trả cùng một expense."),
        ("Upsert thay thế", "Cùng id, dữ liệu giống hệt → thay thế idempotent."),
        ("Trùng lặp xung đột bị chặn", "Cùng id với dữ liệu khác là xung đột."),
        ("findByCategory lọc", "Index category lọc; total cộng tất cả."),
        ("Delete xóa bỏ", "True lần đầu, false sau đó."),
    ],
)

VI_CH_P11_SAFE_SQL = vi_challenge(
    "Xây (một cách khái niệm) truy vấn an toàn",
    r"""Bài tập SQL-builder không cần database. Cài trong `Solution`:
- `record Param(String value)`
- `static String buildFind(String table, Param id)` trả
  `"SELECT * FROM " + table + " WHERE id = ?"` — placeholder, KHÔNG phải
  giá trị (minh họa parameter binding).
- `static String buildFindUnsafe(String table, String id)` trả bản nối
  chuỗi `"SELECT * FROM " + table + " WHERE id = '" + id + "'"`.

Test minh họa cuộc tấn công: id `x' OR '1'='1` tạo ra chuỗi placeholder
vô hại ở builder an toàn và một truy vấn *bị chèn* ở bản không an toàn —
cho thấy lỗ hổng trần trụi.""",
    [
        ("Builder an toàn bind, không nội suy", "Payload không bao giờ vào trong văn bản SQL."),
        ("Builder không an toàn minh họa injection", "Payload thay đổi ý nghĩa truy vấn — cuộc tấn công hiện nguyên hình."),
        ("An toàn với id bình thường", "Placeholder bất kể giá trị."),
    ],
)

VI_CH_P11_INDEX = vi_challenge(
    "Giữ cho index trung thực",
    r"""Mở rộng ý tưởng repository: một store có index trong đó mọi lần ghi
duy trì một index phụ. Cài trong `Solution`:
- `record Book(String isbn, String genre)`
- `static class IndexedStore` với `save(Book b)` (upsert),
  `List<Book> byGenre(String genre)` (thứ tự chèn), `int size()`,
  và `remove(String isbn)` (boolean).

Index là hợp đồng: `byGenre` KHÔNG BAO GIỜ được trả một cuốn sách đã đổi
genre, re-save, hoặc bị xóa. Upsert phải dời sách giữa các bucket của
index — đúng bug trong bài học.""",
    [
        ("Index genre nhóm đúng", "Các bucket phản chiếu dữ liệu đã lưu."),
        ("Upsert dời bucket", "Bug index cũ: bucket cũ phải mất entry."),
        ("Remove dọn index", "Xóa phải chạm cả index."),
    ],
)

write_practice(
    MOD,
    "javi-p11-persistence",
    "Persistence Lab",
    "A full in-memory repository, the safe-vs-injected query contrast, and honest index maintenance.",
    "Xưởng persistence",
    "Một repository trong bộ nhớ đầy đủ, tương phản truy vấn an toàn so với bị chèn, và duy trì index trung thực.",
    "relations-indexes",
    40,
    "intermediate",
    [CH_P11_REPO, CH_P11_SAFE_SQL, CH_P11_INDEX],
    {CH_P11_REPO["id"]: VI_CH_P11_REPO, CH_P11_SAFE_SQL["id"]: VI_CH_P11_SAFE_SQL, CH_P11_INDEX["id"]: VI_CH_P11_INDEX},
    solutions=[
        (
            CH_P11_REPO["id"],
            r"""
import java.util.*;

public class Solution {
    public record Expense(String id, String category, int cents) {}
    public static class DuplicateExpenseException extends RuntimeException {
        public DuplicateExpenseException(String m) { super(m); }
    }

    public static class ExpenseRepository {
        private final Map<String, Expense> store = new LinkedHashMap<>();

        public Expense save(Expense e) {
            Expense old = store.get(e.id());
            if (old != null && !old.category().equals(e.category())) {
                throw new DuplicateExpenseException("id conflict: " + e.id());
            }
            store.put(e.id(), e);
            return e;
        }
        public Optional<Expense> findById(String id) { return Optional.ofNullable(store.get(id)); }
        public List<Expense> findByCategory(String category) {
            List<Expense> out = new ArrayList<>();
            for (Expense e : store.values()) if (e.category().equals(category)) out.add(e);
            return out;
        }
        public boolean deleteById(String id) { return store.remove(id) != null; }
        public List<Expense> findAll() { return new ArrayList<>(store.values()); }
        public int totalCents() {
            int t = 0;
            for (Expense e : store.values()) t += e.cents();
            return t;
        }
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public record Expense(String id, String category, int cents) {}
    public static class DuplicateExpenseException extends RuntimeException {
        public DuplicateExpenseException(String m) { super(m); }
    }

    public static class ExpenseRepository {
        private final Map<String, Expense> store = new LinkedHashMap<>();

        public Expense save(Expense e) {
            // W: rejects ALL re-saves including legitimate same-category
            // updates — an upsert API must allow amount changes.
            Expense old = store.get(e.id());
            if (old != null) throw new DuplicateExpenseException("id conflict: " + e.id());
            store.put(e.id(), e);
            return e;
        }
        public Optional<Expense> findById(String id) { return Optional.ofNullable(store.get(id)); }
        public List<Expense> findByCategory(String category) {
            List<Expense> out = new ArrayList<>();
            for (Expense e : store.values()) if (e.category().equals(category)) out.add(e);
            return out;
        }
        public boolean deleteById(String id) { return store.remove(id) != null; }
        public List<Expense> findAll() { return new ArrayList<>(store.values()); }
        public int totalCents() {
            int t = 0;
            for (Expense e : store.values()) t += e.cents();
            return t;
        }
    }
}
""",
        ),
        (
            CH_P11_SAFE_SQL["id"],
            r"""
public class Solution {
    public record Param(String value) {}

    public static String buildFind(String table, Param id) {
        return "SELECT * FROM " + table + " WHERE id = ?";
    }

    public static String buildFindUnsafe(String table, String id) {
        return "SELECT * FROM " + table + " WHERE id = '" + id + "'";
    }
}
""",
            r"""
public class Solution {
    public record Param(String value) {}

    // W: "safe" builder interpolates the raw value into the SQL text —
    // identical to buildFindUnsafe. The ? placeholder only protects when
    // the value is actually bound at execution time.
    public static String buildFind(String table, Param id) {
        return "SELECT * FROM " + table + " WHERE id = '" + id.value() + "'";
    }

    public static String buildFindUnsafe(String table, String id) {
        return "SELECT * FROM " + table + " WHERE id = '" + id + "'";
    }
}
""",
        ),
        (
            CH_P11_INDEX["id"],
            r"""
import java.util.*;

public class Solution {
    public record Book(String isbn, String genre) {}

    public static class IndexedStore {
        private final Map<String, Book> books = new LinkedHashMap<>();
        private final Map<String, List<Book>> byGenre = new HashMap<>();

        public void save(Book b) {
            Book old = books.put(b.isbn(), b);
            if (old != null) {
                List<Book> bucket = byGenre.get(old.genre());
                if (bucket != null) bucket.remove(old);
            }
            byGenre.computeIfAbsent(b.genre(), k -> new ArrayList<>()).add(b);
        }

        public List<Book> byGenre(String genre) {
            return new ArrayList<>(byGenre.getOrDefault(genre, List.of()));
        }

        public boolean remove(String isbn) {
            Book old = books.remove(isbn);
            if (old == null) return false;
            List<Book> bucket = byGenre.get(old.genre());
            if (bucket != null) bucket.remove(old);
            return true;
        }

        public int size() { return books.size(); }
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public record Book(String isbn, String genre) {}

    public static class IndexedStore {
        private final Map<String, Book> books = new LinkedHashMap<>();
        private final Map<String, List<Book>> byGenre = new HashMap<>();

        // W: main store updated, index ignored on genre change — the
        // stale-index bug from the lesson verbatim. The book stays in
        // its OLD genre bucket forever.
        public void save(Book b) {
            books.put(b.isbn(), b);
            byGenre.computeIfAbsent(b.genre(), k -> new ArrayList<>()).add(b);
        }

        public List<Book> byGenre(String genre) {
            return new ArrayList<>(byGenre.getOrDefault(genre, List.of()));
        }

        public boolean remove(String isbn) {
            Book old = books.remove(isbn);
            if (old == null) return false;
            List<Book> bucket = byGenre.get(old.genre());
            if (bucket != null) bucket.remove(old);
            return true;
        }

        public int size() { return books.size(); }
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — persistence

You can now: design repositories that make storage swappable, keep
derived indexes consistent on every write, and explain the JDBC
contract your production implementation would honor. Prove it with a
transactional outbox.
"""

CP_MDX_VI = r"""
## Checkpoint — persistence

Giờ bạn có thể: thiết kế repository khiến storage hoán đổi được, giữ
index dẫn xuất nhất quán ở mọi lần ghi, và giải thích hợp đồng JDBC mà
hiện thực production sẽ tôn trọng. Chứng minh bằng một outbox giao dịch.
"""

CH_CP11 = challenge(
    "javi-checkpoint-m11-persistence",
    "Transactional Outbox",
    r"""An outbox records pending side effects atomically with data changes.
Implement in `Solution`:
- `record OutboxEntry(String id, String topic, String payload)`
- `static class OutboxStore`:
  - `boolean offer(OutboxEntry e)` — appends if the id is new, returns
    true; duplicate id returns false (idempotent producer).
  - `List<OutboxEntry> drain(String topic)` — removes and returns ALL
    entries for that topic in insertion order.
  - `int pending()` — total across topics.
- `static int deliverAll(OutboxStore store, String topic,
  java.util.function.Consumer<OutboxEntry> sink)` — drains the topic,
  feeding each entry to sink, returning the count delivered.

The transactional property under test: an entry is delivered exactly
once even if offer() was called multiple times.""",
    r"""
import java.util.*;
import java.util.function.Consumer;

public class Solution {
    public record OutboxEntry(String id, String topic, String payload) {}
    // Provide OutboxStore + deliverAll here.
}
""",
    [
        (
            "offer is idempotent",
            r"""
Solution.OutboxStore s = new Solution.OutboxStore();
Solution.OutboxEntry e = new Solution.OutboxEntry("1", "mail", "hi");
checkEq(s.offer(e), true, "first accepted");
checkEq(s.offer(e), false, "duplicate refused");
checkEq(s.pending(), 1, "still one");
""",
            "Duplicate ids never double-deliver.",
        ),
        (
            "drain empties the topic in order",
            r"""
Solution.OutboxStore s = new Solution.OutboxStore();
s.offer(new Solution.OutboxEntry("1", "mail", "a"));
s.offer(new Solution.OutboxEntry("2", "mail", "b"));
s.offer(new Solution.OutboxEntry("3", "audit", "c"));
List<Solution.OutboxEntry> got = s.drain("mail");
checkEq(got.size(), 2, "two mail entries");
checkEq(got.get(0).id(), "1", "insertion order");
checkEq(s.pending(), 1, "audit remains");
""",
            "drain removes only its topic, preserving order.",
        ),
        (
            "deliverAll feeds the sink exactly once",
            r"""
Solution.OutboxStore s = new Solution.OutboxStore();
s.offer(new Solution.OutboxEntry("1", "mail", "a"));
s.offer(new Solution.OutboxEntry("1", "mail", "a"));   // duplicate offer
List<String> seen = new ArrayList<>();
int n = Solution.deliverAll(s, "mail", e -> seen.add(e.payload()));
checkEq(n, 1, "one delivery");
checkEq(seen, List.of("a"), "sink got payload");
checkEq(s.pending(), 0, "store empty");
""",
            "Exactly-once semantics across duplicate offers.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP11 = vi_challenge(
    "Outbox giao dịch",
    r"""Outbox ghi nhận side effect đang chờ một cách nguyên tử với thay đổi
dữ liệu. Cài trong `Solution`:
- `record OutboxEntry(String id, String topic, String payload)`
- `static class OutboxStore`:
  - `boolean offer(OutboxEntry e)` — nối nếu id mới, trả true; id trùng
    trả false (producer idempotent).
  - `List<OutboxEntry> drain(String topic)` — xóa và trả TẤT CẢ entry
    của topic đó theo thứ tự chèn.
  - `int pending()` — tổng qua mọi topic.
- `static int deliverAll(OutboxStore store, String topic,
  java.util.function.Consumer<OutboxEntry> sink)` — drain topic, đưa
  từng entry cho sink, trả số entry đã giao.

Tính chất giao dịch bị test: một entry được giao đúng một lần kể cả khi
offer() được gọi nhiều lần.""",
    [
        ("offer idempotent", "Id trùng không bao giờ giao hai lần."),
        ("drain dọn topic theo thứ tự", "drain chỉ xóa topic của nó, giữ thứ tự."),
        ("deliverAll đưa sink đúng một lần", "Ngữ nghĩa exactly-once qua các lần offer trùng."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-persistence",
    "Checkpoint: Persistence",
    "Graded checkpoint: an idempotent outbox store with ordered draining and exactly-once delivery.",
    15,
    CP_MDX,
    "Checkpoint: Persistence",
    "Checkpoint chấm điểm: outbox store idempotent với drain có thứ tự và giao hàng exactly-once.",
    CP_MDX_VI,
    CH_CP11,
    VI_CH_CP11,
    solution=r"""
import java.util.*;
import java.util.function.Consumer;

public class Solution {
    public record OutboxEntry(String id, String topic, String payload) {}

    public static class OutboxStore {
        private final List<OutboxEntry> entries = new ArrayList<>();

        public boolean offer(OutboxEntry e) {
            for (OutboxEntry existing : entries) {
                if (existing.id().equals(e.id())) return false;
            }
            entries.add(e);
            return true;
        }

        public List<OutboxEntry> drain(String topic) {
            List<OutboxEntry> out = new ArrayList<>();
            Iterator<OutboxEntry> it = entries.iterator();
            while (it.hasNext()) {
                OutboxEntry e = it.next();
                if (e.topic().equals(topic)) { out.add(e); it.remove(); }
            }
            return out;
        }

        public int pending() { return entries.size(); }
    }

    public static int deliverAll(OutboxStore store, String topic, Consumer<OutboxEntry> sink) {
        List<OutboxEntry> batch = store.drain(topic);
        for (OutboxEntry e : batch) sink.accept(e);
        return batch.size();
    }
}
""",
    wrong=r"""
import java.util.*;
import java.util.function.Consumer;

public class Solution {
    public record OutboxEntry(String id, String topic, String payload) {}

    public static class OutboxStore {
        private final List<OutboxEntry> entries = new ArrayList<>();

        // W: offer accepts duplicates — the exactly-once guarantee is
        // gone and the deliverAll test counts two deliveries.
        public boolean offer(OutboxEntry e) {
            entries.add(e);
            return true;
        }

        public List<OutboxEntry> drain(String topic) {
            List<OutboxEntry> out = new ArrayList<>();
            Iterator<OutboxEntry> it = entries.iterator();
            while (it.hasNext()) {
                OutboxEntry e = it.next();
                if (e.topic().equals(topic)) { out.add(e); it.remove(); }
            }
            return out;
        }

        public int pending() { return entries.size(); }
    }

    public static int deliverAll(OutboxStore store, String topic, Consumer<OutboxEntry> sink) {
        List<OutboxEntry> batch = store.drain(topic);
        for (OutboxEntry e : batch) sink.accept(e);
        return batch.size();
    }
}
""",
)
