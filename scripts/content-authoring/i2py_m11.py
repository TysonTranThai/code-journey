#!/usr/bin/env python3
"""Module 11: databases-full-stack — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint

MOD = "databases-full-stack"

write_module(
    MOD,
    "Databases & Full-Stack Development",
    "Relational thinking: tables, keys, joins, transactions — then wiring frontend, API, and PostgreSQL into one honest application.",
    "Cơ sở dữ liệu & Phát triển Full-Stack",
    "Tư duy quan hệ: bảng, khóa, join, transaction — rồi nối frontend, API, và PostgreSQL thành một ứng dụng trung thực.",
    ["relational-model", "sql-crud", "joins-relationships", "transactions-migrations", "fullstack-integration", "db-checkpoint"],
    ["sql-practice", "schema-practice", "api-db-practice", "fullstack-practice"],
)

write_lesson(
    MOD, "relational-model",
    "The Relational Model",
    "Tables, primary keys, foreign keys, and the normalization instinct: one fact, one place.",
    20,
    """A relational database stores facts in **tables** (relations) of **rows** (records) with fixed **columns** (attributes). SQL is the language; PostgreSQL is the engine.

## Keys

- **Primary key** — the column (or combination) that uniquely identifies a row: `id serial PRIMARY KEY`. Never reuses values, never null.
- **Foreign key** — a column pointing at another table's primary key: `author_id INTEGER REFERENCES users(id)`. The database *enforces* that the referenced row exists — an impossible author_id is rejected at insert, not discovered in production.

## Relationships

- **One-to-many** — most common: one user, many tasks. FK lives on the "many" side (tasks.author_id).
- **Many-to-many** — tasks and tags: a **junction table** `task_tags(task_id, tag_id)` holding a pair per link. Both columns FK; often the pair is the primary key.
- **One-to-one** — a FK with a UNIQUE constraint (users ↔ user_profiles).

## Normalization: the instinct

**One fact, one place.** Storing the author's name on every task row means an update must touch thousands of rows and will eventually disagree with itself. Instead: store `author_id`; join to `users` when you need the name. The classic stages:

- **1NF** — no repeating groups (no "tags" column holding "a,b,c")
- **2NF** — every column depends on the whole key
- **3NF** — no column depends on another non-key column

Denormalization (deliberately duplicating for read speed) is a *tuning* decision made later, with measurement — never the starting shape.

## Data types matter

`INTEGER` vs `TEXT` vs `TIMESTAMPTZ` vs `BOOLEAN` vs `NUMERIC` (money! never float). Types are your first line of defense: the database rejects garbage before your code runs. Postgres-native niceties: `SERIAL`/`GENERATED` for ids, `JSONB` when structure is genuinely flexible, `TIMESTAMPTZ` always over `TIMESTAMP`.

## NULL is its own animal

NULL means "unknown", not zero and not empty string. `NULL = NULL` is not true — it's NULL. Counts, joins, and constraints all treat NULL distinctly; declare columns `NOT NULL` by default and NULL only when absence is meaningful data.""",
    "Mô hình quan hệ",
    "Bảng, khóa chính, khóa ngoại, và bản năng chuẩn hóa: một sự thật, một nơi lưu giữ.",
    """Cơ sở dữ liệu quan hệ lưu các sự thật trong **bảng** (relation) gồm **hàng** (record) với **cột** (attribute) cố định. SQL là ngôn ngữ; PostgreSQL là động cơ.

## Khóa

- **Khóa chính (primary key)** — cột (hoặc tổ hợp) định danh duy nhất một hàng: `id serial PRIMARY KEY`. Không bao giờ tái sử dụng giá trị, không bao giờ null.
- **Khóa ngoại (foreign key)** — cột trỏ tới khóa chính của bảng khác: `author_id INTEGER REFERENCES users(id)`. Database *ép buộc* hàng được tham chiếu phải tồn tại — author_id không thể tồn tại bị chặn ngay lúc insert, không phải được phát hiện ở production.

## Các loại quan hệ

- **Một-nhiều** — phổ biến nhất: một user, nhiều task. Khóa ngoại nằm ở phía "nhiều" (tasks.author_id).
- **Nhiều-nhiều** — task và tag: một **bảng nối** `task_tags(task_id, tag_id)` giữ một cặp cho mỗi liên kết. Cả hai cột là khóa ngoại; thường cặp đó chính là khóa chính.
- **Một-một** — khóa ngoại kèm ràng buộc UNIQUE (users ↔ user_profiles).

## Chuẩn hóa: bản năng

**Một sự thật, một nơi.** Lưu tên tác giả trên mọi hàng task nghĩa là một lần cập nhật phải chạm hàng nghìn hàng và chắc chắn sẽ tự mâu thuẫn. Thay vào đó: lưu `author_id`; join sang `users` khi cần tên. Các mức kinh điển:

- **1NF** — không có nhóm lặp lại (không có cột "tags" chứa "a,b,c")
- **2NF** — mọi cột phụ thuộc vào toàn bộ khóa
- **3NF** — không cột nào phụ thuộc vào một cột không phải khóa khác

Phi chuẩn hóa (cố ý trùng lặp để đọc nhanh) là quyết định *tinh chỉnh* đưa ra sau này, có đo đếm — không bao giờ là hình dạng khởi đầu.

## Kiểu dữ liệu quan trọng

`INTEGER` so với `TEXT` so với `TIMESTAMPTZ` so với `BOOLEAN` so với `NUMERIC` (tiền tệ! đừng bao giờ dùng float). Kiểu là tuyến phòng thủ đầu tiên của bạn: database chặn rác trước khi code chạy. Tiện ích bản địa Postgres: `SERIAL`/`GENERATED` cho id, `JSONB` khi cấu trúc thực sự linh hoạt, `TIMESTAMPTZ` luôn thay cho `TIMESTAMP`.

## NULL là một loài riêng

NULL nghĩa là "không xác định", không phải số 0 và không phải chuỗi rỗng. `NULL = NULL` không đúng — nó là NULL. Count, join, và ràng buộc đều đối xử với NULL khác biệt; mặc định khai báo cột `NOT NULL` và chỉ dùng NULL khi sự vắng mặt là dữ liệu có ý nghĩa.""",
)

write_lesson(
    MOD, "sql-crud",
    "SQL: CRUD in Statements",
    "SELECT, INSERT, UPDATE, DELETE — with WHERE, ORDER BY, and the safety habits that keep data honest.",
    22,
    """## The four statements

```sql
INSERT INTO tasks (title, author_id) VALUES ('Write tests', 7) RETURNING id;

SELECT title, created_at FROM tasks WHERE author_id = 7 AND done = false ORDER BY created_at DESC LIMIT 20 OFFSET 40;

UPDATE tasks SET done = true WHERE id = 42 RETURNING *;

DELETE FROM tasks WHERE id = 42;
```

Read them as sentences. `RETURNING` (Postgres) hands back the affected row — no second query after insert.

## WHERE and friends

- Comparison: `=`, `<>`, `<`, `>`, `<=`, `>=`; ranges `BETWEEN a AND b`; membership `IN (1, 2, 3)`
- Patterns: `LIKE 'wr%'` (% = any string, _ = one char), `ILIKE` for case-insensitivity
- NULL checks: `IS NULL` / `IS NOT NULL` — **never** `= NULL`
- Logic: `AND`/`OR`/`NOT` — parenthesize mixed groups; `a OR b AND c` binds as `a OR (b AND c)`

## Aggregates and grouping

```sql
SELECT author_id, COUNT(*) AS task_count, MAX(created_at) AS latest
FROM tasks
WHERE done = false
GROUP BY author_id
HAVING COUNT(*) > 5
ORDER BY task_count DESC;
```

`WHERE` filters rows *before* grouping; `HAVING` filters groups *after*. COUNT/SUM/AVG/MIN/MAX are the workhorses.

## The safety habits

1. **Always a WHERE on UPDATE/DELETE.** `UPDATE tasks SET done = true;` touches *every* row. Professional habit: write the WHERE first.
2. **Parameterized from application code** (module 9!): `query("... WHERE id = $1", [id])` — never string concatenation.
3. **Transactions for multi-step writes** (next lesson): try in a transaction, verify, commit or roll back.
4. **SELECT the columns you need**, not `*`, in application code — self-documenting and cheaper over the wire.

## Indexes: why lookups are fast

An index is a sorted side-structure (B-tree) letting the engine find rows in log-time instead of scanning everything. Primary keys get one automatically; add them on columns you filter/join/sort by:

```sql
CREATE INDEX idx_tasks_author ON tasks (author_id);
```

Trade-offs: indexes speed reads, slow writes slightly, and consume disk. Index what you query; ignore what you don't (most tools show unused-index reports).""",
    "SQL: CRUD bằng câu lệnh",
    "SELECT, INSERT, UPDATE, DELETE — cùng WHERE, ORDER BY, và những thói quen an toàn giữ cho dữ liệu trung thực.",
    """## Bốn câu lệnh

```sql
INSERT INTO tasks (title, author_id) VALUES ('Write tests', 7) RETURNING id;

SELECT title, created_at FROM tasks WHERE author_id = 7 AND done = false ORDER BY created_at DESC LIMIT 20 OFFSET 40;

UPDATE tasks SET done = true WHERE id = 42 RETURNING *;

DELETE FROM tasks WHERE id = 42;
```

Đọc chúng như câu văn. `RETURNING` (Postgres) trả về hàng bị ảnh hưởng — không cần truy vấn thứ hai sau insert.

## WHERE và bạn bè

- So sánh: `=`, `<>`, `<`, `>`, `<=`, `>=`; miền `BETWEEN a AND b`; thuộc tập `IN (1, 2, 3)`
- Mẫu: `LIKE 'wr%'` (% = chuỗi bất kỳ, _ = một ký tự), `ILIKE` để bỏ qua hoa thường
- Kiểm tra NULL: `IS NULL` / `IS NOT NULL` — **đừng bao giờ** `= NULL`
- Logic: `AND`/`OR`/`NOT` — đặt ngoặc cho nhóm trộn lẫn; `a OR b AND c` ràng buộc thành `a OR (b AND c)`

## Tổng hợp và nhóm

```sql
SELECT author_id, COUNT(*) AS task_count, MAX(created_at) AS latest
FROM tasks
WHERE done = false
GROUP BY author_id
HAVING COUNT(*) > 5
ORDER BY task_count DESC;
```

`WHERE` lọc hàng *trước* khi nhóm; `HAVING` lọc nhóm *sau*. COUNT/SUM/AVG/MIN/MAX là những con ngựa thồ.

## Thói quen an toàn

1. **Luôn có WHERE trên UPDATE/DELETE.** `UPDATE tasks SET done = true;` chạm *mọi* hàng. Thói quen nghề: viết WHERE trước.
2. **Parameterized từ code ứng dụng** (module 9!): `query("... WHERE id = $1", [id])` — không bao giờ nối chuỗi.
3. **Transaction cho ghi nhiều bước** (bài sau): thử trong transaction, xác minh, commit hoặc rollback.
4. **SELECT đúng cột cần**, không phải `*`, trong code ứng dụng — tự ghi chú và rẻ hơn trên đường truyền.

## Index: vì sao tra cứu nhanh

Index là cấu trúc phụ đã sắp xếp (B-tree) giúp động cơ tìm hàng theo thời gian log thay vì quét tất cả. Khóa chính tự có index; thêm cho các cột bạn lọc/join/sort:

```sql
CREATE INDEX idx_tasks_author ON tasks (author_id);
```

Đổi lại: index làm việc đọc nhanh, ghi chậm hơn chút, và tốn đĩa. Index thứ gì bạn truy vấn; bỏ qua thứ không (hầu hết công cụ đều có báo cáo index không dùng).""",
)

write_lesson(
    MOD, "joins-relationships",
    "Joins and Relationships",
    "Combining tables: INNER for matches, LEFT for preservation — reading the results without surprises.",
    20,
    """Data is split across tables (module's first lesson); joins put it back together for a query.

## INNER JOIN: rows that match

```sql
SELECT t.id, t.title, u.name
FROM tasks t
INNER JOIN users u ON u.id = t.author_id;
```

Every task with its author's name; tasks without a valid author vanish (the FK should prevent that, but soft-deleted users, legacy data...). Alias tables (`tasks t`) — you'll type them a lot.

## LEFT JOIN: keep the left side

```sql
SELECT u.name, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON t.author_id = u.id
GROUP BY u.name;
```

Every user appears — even those with zero tasks (COUNT(t.id) is 0 because t.id is NULL). This "count including zeros" pattern is the most common real-world join. RIGHT JOIN exists (rarely used — flip the tables instead); FULL OUTER keeps both sides.

## The NULL trap in joins

A LEFT JOIN's unmatched rows have NULL right-columns. Two consequences:

- `WHERE t.something = x` silently converts your LEFT JOIN into an INNER one (NULL fails the comparison). Put right-side conditions **in the ON clause** if you want preservation.
- `COUNT(*)` counts rows (including matched-with-NULLs); `COUNT(t.id)` counts non-null ids. They differ exactly on the rows you joined to keep.

## Subqueries and CTEs

```sql
-- users with more than 5 open tasks
SELECT name FROM users u
WHERE (SELECT COUNT(*) FROM tasks t WHERE t.author_id = u.id AND t.done = false) > 5;

-- same, as a readable CTE
WITH open_counts AS (
  SELECT author_id, COUNT(*) AS n
  FROM tasks
  WHERE done = false
  GROUP BY author_id
)
SELECT u.name, c.n
FROM open_counts c
JOIN users u ON u.id = c.author_id
WHERE c.n > 5;
```

CTEs (`WITH`) name an intermediate result — often clearer than nesting, and Postgres can still optimize it.

## Many-to-many in practice

```sql
SELECT t.title, array_agg(tg.name) AS tags
FROM tasks t
JOIN task_tags tt ON tt.task_id = t.id
JOIN tags tg ON tg.id = tt.tag_id
GROUP BY t.title;
```

Two hops across the junction table. Filtering ("tasks tagged urgent") is a join with `WHERE tg.name = 'urgent'`; counting per tag is a GROUP BY on the junction.""",
    "Join và quan hệ",
    "Kết hợp các bảng: INNER cho khớp, LEFT để giữ lại — đọc kết quả không ngạc nhiên.",
    """Dữ liệu được tách across các bảng (bài đầu của module); join ráp lại thành một truy vấn.

## INNER JOIN: những hàng khớp nhau

```sql
SELECT t.id, t.title, u.name
FROM tasks t
INNER JOIN users u ON u.id = t.author_id;
```

Mỗi task kèm tên tác giả; task không có tác giả hợp lệ biến mất (khóa ngoại đáng lẽ đã ngăn, nhưng user bị xóa mềm, dữ liệu cũ...). Đặt alias cho bảng (`tasks t`) — bạn sẽ gõ chúng nhiều lắm.

## LEFT JOIN: giữ lại phía trái

```sql
SELECT u.name, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON t.author_id = u.id
GROUP BY u.name;
```

Mọi user đều xuất hiện — kể cả người không có task nào (COUNT(t.id) là 0 vì t.id là NULL). Mô hình "đếm cả số 0" này là join phổ biến nhất ngoài thực tế. RIGHT JOIN tồn tại (hiếm dùng — đảo hai bảng lại); FULL OUTER giữ cả hai phía.

## Bẫy NULL trong join

Hàng không khớp của LEFT JOIN có cột phải là NULL. Hai hệ quả:

- `WHERE t.something = x` lặng lẽ biến LEFT JOIN của bạn thành INNER (NULL trượt phép so sánh). Đặt điều kiện phía phải **trong mệnh đề ON** nếu muốn giữ lại.
- `COUNT(*)` đếm hàng (kể cả hàng khớp-kèm-NULL); `COUNT(t.id)` đếm id khác null. Chúng khác nhau đúng ở những hàng bạn join để giữ lại.

## Subquery và CTE

```sql
-- user có nhiều hơn 5 task đang mở
SELECT name FROM users u
WHERE (SELECT COUNT(*) FROM tasks t WHERE t.author_id = u.id AND t.done = false) > 5;

-- giống hệt, dưới dạng CTE dễ đọc
WITH open_counts AS (
  SELECT author_id, COUNT(*) AS n
  FROM tasks
  WHERE done = false
  GROUP BY author_id
)
SELECT u.name, c.n
FROM open_counts c
JOIN users u ON u.id = c.author_id
WHERE c.n > 5;
```

CTE (`WITH`) đặt tên cho một kết quả trung gian — thường rõ hơn việc lồng nhau, và Postgres vẫn tối ưu hóa được.

## Nhiều-nhiều trong thực chiến

```sql
SELECT t.title, array_agg(tg.name) AS tags
FROM tasks t
JOIN task_tags tt ON tt.task_id = t.id
JOIN tags tg ON tg.id = tt.tag_id
GROUP BY t.title;
```

Hai bước nhảy qua bảng nối. Lọc ("task gắn tag urgent") là một join kèm `WHERE tg.name = 'urgent'`; đếm theo tag là GROUP BY trên bảng nối.""",
)

write_lesson(
    MOD, "transactions-migrations",
    "Transactions, Migrations, and ORMs",
    "All-or-nothing writes, versioned schema changes, and where an ORM helps — and where it doesn't.",
    20,
    """## Transactions: all or nothing

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- or ROLLBACK; on any failure
```

Either both updates land or neither does. The four guarantees (ACID): **Atomicity** (all-or-nothing), **Consistency** (constraints hold before and after), **Isolation** (concurrent transactions don't see each other's half-work), **Durability** (committed data survives crashes).

The transfer above is the canonical case, but so is any app-level multi-step: create user + create profile + send welcome — if step 3 fails, roll back 1 and 2. In Node: `BEGIN` ... run queries ... `COMMIT` in a `try`, `ROLLBACK` in the `catch`.

## Migrations: schema changes under version control

Schema lives in your repo as ordered migration files:

```text
migrations/
  001_create_tasks.sql     CREATE TABLE tasks (...);
  002_add_due_column.sql   ALTER TABLE tasks ADD COLUMN due timestamptz;
  003_tasks_tags.sql       CREATE TABLE task_tags (...);
```

Rules the pros live by:

- **Forward only** — write a new migration to change things; don't edit old ones (they've run elsewhere)
- **Every migration paired with a mental (or written) rollback**
- **Expand/contract for zero-downtime**: add the new column (expand), deploy code writing both, backfill, remove the old column (contract)
- The tool tracks which migrations have run (`drizzle-kit`, `node-pg-migrate`, plain SQL runner)

## ORMs: helpers, not oracles

An ORM (Drizzle, Prisma) maps tables to typed code: `db.select().from(tasks).where(eq(tasks.authorId, 7))`. Gains: type safety end-to-end, fewer injection mistakes, migrations-as-code. Costs: a second mental model, and the temptation to forget SQL — which you *will* need when the ORM generates a slow query and the fix is knowing what SQL you want instead.

The professional stance: **learn SQL first** (you just did), then let the ORM save typing on the boring 80%, and drop to raw SQL (`sql\`...\``) for the interesting 20%. The ORM is a query *builder*, not a database *substitute*.

## Connection pooling

Every query needs a connection; opening one per request kills performance. A pool keeps N connections open and lends them out (`pg.Pool`, max ~10 for most apps). The classic deployment bug: pool size × server count > database's max_connections — everyone's queries start failing at 5pm on a Friday.""",
    "Transaction, migration, và ORM",
    "Ghi tất-cả-hoặc-không-có-gì, thay đổi schema có phiên bản, và chỗ nào ORM giúp — chỗ nào không.",
    """## Transaction: tất cả hoặc không có gì

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- hoặc ROLLBACK; nếu có lỗi
```

Hoặc cả hai cập nhật đều ghi, hoặc không cái nào. Bốn bảo đảm (ACID): **Atomicity** (tất cả-hoặc-không), **Consistency** (ràng buộc được giữ trước và sau), **Isolation** (các transaction song song không nhìn thấy nửa chừng của nhau), **Durability** (đã commit là sống sót qua crash).

Phép chuyển tiền trên là ca kinh điển, nhưng mọi bước nhiều-pha ở tầng ứng dụng cũng vậy: tạo user + tạo profile + gửi email chào mừng — nếu bước 3 hỏng, rollback 1 và 2. Trong Node: `BEGIN` ... chạy các query ... `COMMIT` trong `try`, `ROLLBACK` trong `catch`.

## Migration: thay đổi schema dưới quản lý phiên bản

Schema sống trong repo của bạn dưới dạng file migration có thứ tự:

```text
migrations/
  001_create_tasks.sql     CREATE TABLE tasks (...);
  002_add_due_column.sql   ALTER TABLE tasks ADD COLUMN due timestamptz;
  003_tasks_tags.sql       CREATE TABLE task_tags (...);
```

Các quy tắc dân nghề sống theo:

- **Chỉ đi tới trước** — viết migration mới để thay đổi; đừng sửa migration cũ (chúng đã chạy ở nơi khác)
- **Mỗi migration đi kèm một kế hoạch (đầu óc hoặc ghi chép) rollback**
- **Expand/contract cho zero-downtime**: thêm cột mới (expand), deploy code ghi cả hai, backfill, xóa cột cũ (contract)
- Công cụ theo dõi migration nào đã chạy (`drizzle-kit`, `node-pg-migrate`, trình chạy SQL thuần)

## ORM: người giúp việc, không phải nhà tiên tri

ORM (Drizzle, Prisma) ánh xạ bảng thành code có kiểu: `db.select().from(tasks).where(eq(tasks.authorId, 7))`. Lợi: an toàn kiểu từ đầu đến cuối, ít lỗi injection hơn, migration dưới dạng code. Hại: một mô hình tinh thần thứ hai, và cám dỗ quên SQL — thứ bạn *sẽ* cần khi ORM sinh ra một query chậm mà cách sửa là biết SQL bạn thực sự muốn.

Thái độ chuyên nghiệp: **học SQL trước** (bạn vừa làm xong), rồi để ORM đỡ gõ cho 80% nhàm chán, và hạ xuống SQL thô (`sql\`...\``) cho 20% thú vị. ORM là trình *dựng* query, không phải bản *thay thế* database.

## Connection pool

Mỗi query cần một kết nối; mở một kết nối mỗi request giết chết hiệu năng. Pool giữ N kết nối mở và cho mượn (`pg.Pool`, tối đa ~10 cho đa số app). Bug triển khai kinh điển: pool size × số server > max_connections của database — query của mọi người bắt đầu thất bại lúc 5 giờ chiều thứ Sáu.""",
)

write_lesson(
    MOD, "fullstack-integration",
    "Wiring the Full Stack",
    "Frontend → fetch → API → validation → SQL → response → state → render: one honest request's journey, and where each seam breaks.",
    22,
    """You now own every layer. Time to connect them into one application.

## The journey of one request

1. **Browser** — user submits a form; JS validates cheaply (UX), then `fetch("/api/tasks", { method: "POST", body })`
2. **API layer** — auth (who is calling?), validation (is the body well-formed?), business rules (module 10)
3. **Data layer** — parameterized SQL in a transaction where needed; rows out
4. **Response** — 201 + the created resource as JSON (or 400 + structured errors)
5. **Browser again** — parse response, update state, render; *optimistic UI* shows success instantly and rolls back on failure

Each seam has a classic failure: the network call (timeout, offline), the API (500, wrong shape), the DB (constraint violation, connection exhausted), the client (stale cache, double submit).

## The contract is the schema

Frontend and backend drift apart silently — until runtime. The fix is one source of truth: a Zod schema shared by both sides (client validates what it renders, server validates what it stores), or TypeScript types generated from the database schema (Drizzle's superpower). When the DB column changes, the type changes, the client code fails to compile. Breakage moves from runtime to compile time.

## Loading states are part of the contract

Every fetch has four UI states and they all need design: **loading** (skeleton, not spinner-on-blank), **success**, **empty** (a real "nothing here yet" state, not a blank box), **error** (message + retry button). Forgetting one is a UX bug users find before you do.

## The N+1 problem: the full-stack performance bug

```js
// list 50 tasks, then fetch each author separately = 51 queries
const tasks = await db.select().from(tasks);
for (const t of tasks) {
  t.author = await getUser(t.authorId);   // 50 more round trips
}
```

Fix: one join, or one `WHERE author_id IN (...)`. Recognize the shape: loop containing an await over per-item data. On the web this multiplies latency × round trips and is the most common "why is this page slow" answer once assets are fine.

## Server-side rendering vs the SPA trade-off

Render HTML on the server (fast first paint, SEO, works before JS loads) vs ship an SPA shell (rich interactions, app-like state). Next.js exists because both have merit. The decision axis: how much of the page is *content* (SSR) vs *application* (client). You'll meet frameworks next course — arrive knowing the trade you're asking them to make.""",
    "Nối Full-Stack",
    "Frontend → fetch → API → validation → SQL → response → state → render: hành trình của một request trung thực, và từng chỗ rời rạc hay gãy.",
    """Giờ bạn sở hữu mọi tầng. Đến lúc nối chúng thành một ứng dụng.

## Hành trình của một request

1. **Trình duyệt** — user submit form; JS kiểm tra sơ bộ (UX), rồi `fetch("/api/tasks", { method: "POST", body })`
2. **Tầng API** — auth (ai đang gọi?), validation (body có đúng dạng?), business rules (module 10)
3. **Tầng dữ liệu** — SQL parameterized trong transaction khi cần; các hàng chảy ra
4. **Response** — 201 + tài nguyên vừa tạo dưới dạng JSON (hoặc 400 + lỗi có cấu trúc)
5. **Trình duyệt lần nữa** — parse response, cập nhật state, render; *optimistic UI* báo thành công ngay và rollback khi thất bại

Mỗi chỗ nối có một kiểu hỏng kinh điển: cuộc gọi mạng (timeout, mất mạng), API (500, sai hình dạng), DB (vi phạm ràng buộc, cạn kết nối), client (cache cũ, submit đôi).

## Hợp đồng chính là schema

Frontend và backend trôi dần khỏi nhau trong im lặng — đến tận runtime. Cách sửa là một nguồn chân lý duy nhất: một Zod schema dùng chung cả hai phía (client validate thứ nó render, server validate thứ nó lưu), hoặc kiểu TypeScript sinh từ schema database (siêu năng lực của Drizzle). Khi cột DB đổi, kiểu đổi, code client fail biên dịch. Sự gãy dịch từ runtime về compile time.

## Loading state là một phần của hợp đồng

Mọi fetch có bốn trạng thái UI và cả bốn cần được thiết kế: **loading** (skeleton, không phải spinner trên nền trắng), **success**, **empty** (một trạng thái "chưa có gì" thật, không phải ô trắng), **error** (thông điệp + nút thử lại). Quên một trạng thái là bug UX mà người dùng phát hiện trước bạn.

## Vấn đề N+1: bug hiệu năng của full-stack

```js
// liệt kê 50 task, rồi lấy từng tác giả riêng lẻ = 51 query
const tasks = await db.select().from(tasks);
for (const t of tasks) {
  t.author = await getUser(t.authorId);   // thêm 50 chuyến khứ hồi
}
```

Cách sửa: một join, hoặc một `WHERE author_id IN (...)`. Nhận diện hình dạng: vòng lặp chứa await trên dữ liệu theo từng item. Trên web nó nhân độ trễ × số chuyến khứ hồi và là câu trả lời phổ biến nhất cho "sao trang này chậm" một khi tài sản đã ổn.

## Đánh đổi giữa server-side rendering và SPA

Render HTML ở server (first paint nhanh, SEO, chạy được trước khi JS tải) so với ship một SPA shell (tương tác giàu, state kiểu app). Next.js tồn tại vì cả hai đều có giá trị. Trục quyết định: bao nhiêu % trang là *nội dung* (SSR) so với *ứng dụng* (client). Bạn sẽ gặp các framework trong khóa sau — hãy đến với kiến thức về đánh đổi mà bạn đang yêu cầu chúng thực hiện.""",
)

write_checkpoint(
    MOD,
    "db-checkpoint",
    "Checkpoint: Data Layer",
    "Prove the data instincts: model relationships, write truthful SQL, judge transactions, and spot the N+1.",
    20,
    """This checkpoint grades data-layer reasoning in runnable form: relationship modeling, SQL semantics, transaction judgment, and full-stack integration sense — the decisions a senior reviewer makes on every data-touching PR.""",
    "Kiểm tra kiến thức: Tầng dữ liệu",
    "Chứng minh bản năng dữ liệu: mô hình hóa quan hệ, viết SQL trung thực, phán đoán transaction, và phát hiện N+1.",
    """Checkpoint này chấm lập luận tầng dữ liệu ở dạng chạy được: mô hình hóa quan hệ, ngữ nghĩa SQL, phán đoán transaction, và cảm giác tích hợp full-stack — những quyết định reviewer senior đưa ra trên mọi PR chạm dữ liệu.""",
    {
        "id": "i2-db-checkpoint",
        "title": "Data Bench",
        "prompt": "Write THREE functions. 1) `joinPlan(query)` — given a desired query description, return the join type: \"users and their tasks (skip users with none)\" => \"inner\"; \"all users with task counts (zero included)\" => \"left\"; \"all tasks with their tag names\" (many-to-many) => \"inner-two\" (two joins); anything else => \"none\". 2) `txDecision(steps, hasFailureRisk)` — return \"transaction\" when there are 2+ write steps OR hasFailureRisk; \"single\" when exactly one write step and no risk; \"readonly\" when zero write steps. 3) `countQueries(taskCount, pattern)` — pattern \"n+1\" => taskCount + 1 queries; \"join\" => 1; \"in-clause\" => 2.",
        "difficulty": "intermediate",
        "level": "checkpoint",
        "boilerplate": "function joinPlan(query) {\n  // your code\n}\n\nfunction txDecision(steps, hasFailureRisk) {\n  // your code\n}\n\nfunction countQueries(taskCount, pattern) {\n  // your code\n}\n",
        "tests": [
            {
                "name": "join types match intent",
                "code": "const fn = new Function(code + \"\\nreturn { joinPlan, txDecision, countQueries };\");\nconst { joinPlan } = fn();\nif (joinPlan(\"users and their tasks (skip users with none)\") !== \"inner\") throw new Error(\"Only matched rows => inner.\");\nif (joinPlan(\"all users with task counts (zero included)\") !== \"left\") throw new Error(\"Zeros included => left.\");\nif (joinPlan(\"all tasks with their tag names\") !== \"inner-two\") throw new Error(\"Junction table => two joins.\");",
                "hint": "Preservation decides inner vs left; junction tables need two hops.",
            },
            {
                "name": "transactions where they belong",
                "code": "const fn = new Function(code + \"\\nreturn { joinPlan, txDecision, countQueries };\");\nconst { txDecision } = fn();\nif (txDecision(1, false) !== \"single\") throw new Error(\"One write, no risk => single.\");\nif (txDecision(2, false) !== \"transaction\") throw new Error(\"Two writes => atomic.\");\nif (txDecision(0, false) !== \"readonly\") throw new Error(\"No writes => readonly.\");\nif (txDecision(1, true) !== \"transaction\") throw new Error(\"Risk => wrap it.\");",
                "hint": "Order the checks: zero, then multi-or-risk, then single.",
            },
            {
                "name": "N+1 counted honestly",
                "code": "const fn = new Function(code + \"\\nreturn { joinPlan, txDecision, countQueries };\");\nconst { countQueries } = fn();\nif (countQueries(50, \"n+1\") !== 51) throw new Error(\"50 tasks + 1 list query = 51.\");\nif (countQueries(50, \"join\") !== 1) throw new Error(\"A join is one query.\");\nif (countQueries(50, \"in-clause\") !== 2) throw new Error(\"List + batched fetch = 2.\");",
                "hint": "Three patterns, three formulas.",
            },
        ],
    },
    {
        "id": "i2-db-checkpoint",
        "title": "Bàn dữ liệu",
        "prompt": "Viết BA hàm. 1) `joinPlan(query)` — cho mô tả truy vấn mong muốn, trả về loại join: \"users and their tasks (skip users with none)\" => \"inner\"; \"all users with task counts (zero included)\" => \"left\"; \"all tasks with their tag names\" (nhiều-nhiều) => \"inner-two\" (hai join); còn lại => \"none\". 2) `txDecision(steps, hasFailureRisk)` — trả về \"transaction\" khi có 2+ bước ghi HOẶC hasFailureRisk; \"single\" khi đúng một bước ghi và không rủi ro; \"readonly\" khi không có bước ghi nào. 3) `countQueries(taskCount, pattern)` — pattern \"n+1\" => taskCount + 1 query; \"join\" => 1; \"in-clause\" => 2.",
        "tests": [
            {"name": "loại join khớp ý định", "hint": "Việc giữ lại hàng quyết định inner vs left; bảng nối cần hai bước nhảy."},
            {"name": "transaction đúng chỗ của nó", "hint": "Sắp các check: zero, rồi nhiều-hoặc-rủi-ro, rồi single."},
            {"name": "đếm N+1 trung thực", "hint": "Ba pattern, ba công thức."},
        ],
    },
)

print("Module 11 lessons + checkpoint written.")
