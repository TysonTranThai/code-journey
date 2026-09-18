#!/usr/bin/env python3
"""Module 11: databases-data-access — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "databases-data-access"

# ── lesson 1 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "relational-thinking",
    "Relational Thinking",
    "Tables are sets, rows have identity, and redundancy is the enemy — normalize to model truth, then denormalize deliberately for speed.",
    28,
    """
A relational database is not a pile of spreadsheets. It is a set of **relations**
whose power comes from three ideas:

## Identity: primary keys

Every row is *the* row — identified by a primary key, never by position or
duplication. `id` is an arbitrary surrogate; an email or an ISBN is a *natural*
key. Choose surrogate keys for stability and natural keys for integrity
(a `UNIQUE` constraint on email does the real work).

## Truth: normalization

Redundancy is a lie waiting to happen. If `orders` stores `customer_name` and
the customer renames themselves, half your rows tell the truth and half don't.
The normal forms discipline this:

- **1NF** — values are atomic; no lists-in-a-column (`tags = "a,b,c"` is a
  future bug).
- **2NF** — every non-key column depends on the *whole* key (no columns that
  really belong to just one part of a composite key).
- **3NF** — and on nothing but the key (if `zip → city`, then `city` doesn't
  belong in the address table; the zip table owns it).

The mnemonic: *"the key, the whole key, and nothing but the key."*

## Relationships: foreign keys

A foreign key is a promise: this value refers to a row that *exists*. Enforced
by the database, not by hope in application code. Referential actions encode
policy — `ON DELETE RESTRICT` (protect the data), `ON DELETE CASCADE` (owned
children die with the parent).

## Denormalization is a decision, not a default

Normalized schemas answer every question with joins. When read traffic makes a
join measurably slow (measure first!), you may *cache a derived value* — a
`comment_count` column maintained in the same transaction as comment writes.
The rule that keeps it honest: **one writer, one transaction, or it will
drift.**

## Constraints are executable documentation

`NOT NULL`, `CHECK (price >= 0)`, `UNIQUE`, foreign keys — each declares an
invariant the schema enforces forever, for every client, including the ones you
haven't written yet.
""",
    "Tư duy quan hệ",
    "Bảng là tập hợp, dòng có định danh, và dư thừa là kẻ thù — chuẩn hóa để mô hình hóa sự thật, rồi phi chuẩn hóa có chủ đích để tăng tốc.",
    """
Một cơ sở dữ liệu quan hệ không phải một đống bảng tính. Nó là một tập các
**quan hệ** mà sức mạnh đến từ ba ý tưởng:

## Định danh: primary key

Mỗi dòng là dòng *duy nhất* — được nhận diện bằng primary key, không bao giờ
bằng vị trí hay trùng lặp. `id` là surrogate tùy ý; email hay ISBN là *natural*
key. Chọn surrogate key vì sự ổn định và natural key vì tính toàn vẹn (ràng
buộc `UNIQUE` trên email mới làm công việc thật).

## Sự thật: chuẩn hóa

Dư thừa là một lời nói dối chờ ngày nổ ra. Nếu `orders` lưu `customer_name` và
khách hàng đổi tên, một nửa dòng của bạn nói thật và nửa còn lại không. Các
dạng chuẩn kỷ luật hóa điều này:

- **1NF** — giá trị là nguyên tử; không có list-trong-một-cột
  (`tags = "a,b,c"` là một bug tương lai).
- **2NF** — mọi cột không phải key phụ thuộc vào *toàn bộ* key (không có cột
  nào thực ra chỉ thuộc về một phần của khóa ghép).
- **3NF** — và không phụ thuộc vào gì ngoài key (nếu `zip → city`, thì `city`
  không thuộc về bảng địa chỉ; bảng zip sở hữu nó).

Câu thần chú: *"the key, the whole key, and nothing but the key."*

## Quan hệ: foreign key

Foreign key là một lời hứa: giá trị này tham chiếu tới một dòng *tồn tại*. Do
database thực thi, không phải do hy vọng trong code ứng dụng. Các hành động
tham chiếu mã hóa chính sách — `ON DELETE RESTRICT` (bảo vệ dữ liệu),
`ON DELETE CASCADE` (con đã được sở hữu chết cùng cha).

## Phi chuẩn hóa là một quyết định, không phải mặc định

Schema chuẩn hóa trả lời mọi câu hỏi bằng join. Khi traffic đọc khiến một join
chậm đo được (hãy đo trước!), bạn có thể *cache một giá trị suy diễn* — cột
`comment_count` được duy trì trong cùng transaction với các lần ghi comment.
Quy tắc giữ cho nó trung thực: **một người ghi, một transaction, nếu không nó
sẽ lệch.**

## Ràng buộc là tài liệu có thể thực thi

`NOT NULL`, `CHECK (price >= 0)`, `UNIQUE`, foreign key — mỗi cái tuyên bố một
bất biến mà schema thực thi mãi mãi, với mọi client, kể cả những client bạn
chưa viết.
""",
)

# ── lesson 2 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "sql-and-transactions",
    "SQL and Transactions",
    "Declarative queries the planner can optimize, joins that model the questions, and transactions whose isolation you can actually reason about.",
    30,
    """
## SQL is declarative — use that

You state *what*; the planner decides *how*. Write queries the planner can
reason about:

- Filter with `WHERE`, aggregate with `GROUP BY`, and let indexes do the seeking.
- `JOIN ... ON` states the relationship explicitly. `INNER JOIN` keeps matches;
  `LEFT JOIN` keeps every left row (and is how you *find the missing* — users
  with no orders are `LEFT JOIN orders ON ... WHERE orders.id IS NULL`).
- `ORDER BY` without an index means a sort — of the whole result set, after all
  the joins. The `LIMIT` doesn't save you.

## Indexes: the planner's shortcuts

An index is a sorted side-structure (typically a B-tree) that turns a scan into
a seek. Rules that survive contact with production:

1. **Index the columns you filter, join, and sort on** — in the order of the
   query (a composite index `(user_id, created_at)` serves
   `WHERE user_id = ? ORDER BY created_at DESC`).
2. **Leftmost prefix:** the index on `(a, b)` serves queries on `a`, and on
   `a AND b` — but not on `b` alone.
3. **Low-selectivity columns barely help** (an index on `active BOOLEAN` in a
   table where 99% are true seeks almost nothing).
4. **Every index taxes every write.** Indexes are not free; each one must be
   updated on INSERT/UPDATE/DELETE.

## Transactions and the classic anomalies

A transaction is all-or-nothing (atomicity) plus isolation — and isolation has
levels, because full isolation is expensive:

| Isolation | Anomaly possible |
|---|---|
| READ UNCOMMITTED | dirty reads (see uncommitted data) |
| READ COMMITTED | non-repeatable reads (same query, different answer) |
| REPEATABLE READ | phantom rows (new rows appear between reads) |
| SERIALIZABLE | none — but the most locking/retrying |

Default for Postgres is READ COMMITTED — which means **write-write races are
your problem**. The fix is *optimistic concurrency*: stamp rows with a version,
and update with `UPDATE ... SET v = v + 1 WHERE id = :id AND v = :seen`. Zero
rows updated means someone raced you: re-read, re-decide, retry. Locking after
the fact beats locking in advance for low-contention data.

## The N+1 query problem

Fetch 50 orders, then loop and fetch each order's customer: 1 + 50 queries.
The network round-trip, not the database work, dominates. Fix: fetch the
collection once (`WHERE user_id IN (...)`) and join in memory — or a single
JOIN. Detect it by *counting queries per request*, which is exactly what the
practice below does.
""",
    "SQL và transaction",
    "Truy vấn khai báo mà planner có thể tối ưu, join mô hình hóa đúng câu hỏi, và transaction mà bạn suy luận được về mức cô lập của nó.",
    """
## SQL là khai báo — hãy tận dụng

Bạn nói *cái gì*; planner quyết định *như thế nào*. Hãy viết truy vấn mà planner
có thể lý giải:

- Lọc bằng `WHERE`, tổng hợp bằng `GROUP BY`, và để index làm việc tìm kiếm.
- `JOIN ... ON` tuyên bố quan hệ một cách tường minh. `INNER JOIN` giữ các cặp
  khớp; `LEFT JOIN` giữ mọi dòng bên trái (và là cách *tìm cái thiếu* — users
  không có orders là `LEFT JOIN orders ON ... WHERE orders.id IS NULL`).
- `ORDER BY` không có index nghĩa là một phép sắp xếp — của toàn bộ tập kết quả,
  sau tất cả các join. `LIMIT` không cứu được bạn.

## Index: lối tắt của planner

Index là một cấu trúc phụ đã sắp xếp (thường là B-tree) biến quét thành nhảy
trực tiếp. Những quy tắc sống sót qua production:

1. **Index các cột bạn lọc, join, và sắp xếp** — theo thứ tự của truy vấn (index
   ghép `(user_id, created_at)` phục vụ
   `WHERE user_id = ? ORDER BY created_at DESC`).
2. **Tiền tố trái nhất:** index trên `(a, b)` phục vụ truy vấn theo `a`, và
   theo `a AND b` — nhưng không phải một mình `b`.
3. **Cột có độ chọn lọc thấp gần như vô dụng** (index trên `active BOOLEAN`
   trong bảng 99% là true gần như không seek được gì).
4. **Mỗi index đánh thuế mọi lần ghi.** Index không miễn phí; mỗi cái phải được
   cập nhật trên INSERT/UPDATE/DELETE.

## Transaction và các bất thường kinh điển

Transaction là tất-cả-hoặc-không-cái-gì (tính nguyên tử) cộng với cô lập — và cô
lập có các mức, vì cô lập hoàn toàn thì đắt:

| Mức cô lập | Bất thường có thể xảy ra |
|---|---|
| READ UNCOMMITTED | dirty read (nhìn thấy dữ liệu chưa commit) |
| READ COMMITTED | non-repeatable read (cùng truy vấn, khác kết quả) |
| REPEATABLE READ | phantom row (dòng mới xuất hiện giữa hai lần đọc) |
| SERIALIZABLE | không — nhưng nhiều khóa/retry nhất |

Mặc định của Postgres là READ COMMITTED — nghĩa là **xung đột ghi-ghi là vấn đề
của bạn**. Cách sửa là *optimistic concurrency*: đóng dấu phiên bản cho dòng,
và cập nhật bằng `UPDATE ... SET v = v + 1 WHERE id = :id AND v = :seen`. Cập
nhật 0 dòng nghĩa là có người vừa tranh chấp với bạn: đọc lại, quyết định lại,
thử lại. Khóa-sau-sự-việc đánh bại khóa-trước-sự-việc với dữ liệu ít tranh chấp.

## Vấn đề N+1 truy vấn

Lấy 50 đơn hàng, rồi vòng lặp lấy khách hàng của từng đơn: 1 + 50 truy vấn.
Chi phí mạng lượt đi-về-lại, không phải công việc database, là thứ thống trị.
Cách sửa: lấy bộ sưu tập một lần (`WHERE user_id IN (...)`) và join trong bộ
nhớ — hoặc một JOIN duy nhất. Phát hiện nó bằng cách *đếm truy vấn trên mỗi
request*, chính là điều bài tập dưới đây làm.
""",
)

# ── lesson 3 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "data-access-architecture",
    "Data Access Architecture",
    "Pools, repositories, and unit-of-work: keeping database mechanics out of business logic without building a fake ORM.",
    28,
    """
## The connection pool

Opening a database connection costs a network handshake, an auth round-trip,
and server-side memory. A **pool** owns a fixed set of connections and lends
them:

- `checkout()` — borrow one (wait or fail if exhausted: *backpressure*),
- `checkin(conn)` — return it (the pool rolls back any open transaction first —
  a borrowed connection must come back clean),
- never share one connection between two concurrent units of work.

Pool sizing is a trade: too small and requests queue; too large and the
database drowns in context switching. Start small (a few per worker) and
measure.

## The repository: your domain's vocabulary

A repository exposes **collections of domain objects**, not tables:

```python
class OrderRepository:
    def get(self, order_id) -> Order | None: ...
    def add(self, order) -> None: ...
    def for_customer(self, customer_id) -> list[Order]: ...
```

Its contract: it raises *domain* errors (`OrderNotFound`), returns *domain*
objects, and never leaks SQL or row tuples upward. That boundary lets tests
swap an in-memory fake, lets the schema change without touching callers, and —
the honest caveat — costs a translation layer. It earns its keep on complex
domains, not on thin CRUD.

## Unit of work: one transaction, one decision

A unit of work collects changes and commits them **atomically**:

```python
with uow:
    uow.orders.add(order)
    uow.payments.record(payment)
# commit happens on exit; either both persist or neither
```

The rule from the API module returns: the *handler* declares the unit of work;
the machinery owns the connection and the transaction. Business logic never
calls `BEGIN` or `COMMIT` itself.

## Migrations: schema change is code change

Schemas evolve; the database must move with the code. A migration is a small,
ordered, versioned step (create table, add column with a default, backfill,
add constraint). Two disciplines: every migration is reversible or explicitly
one-way-and-dangerous, and *add-then-migrate-then-remove* for breaking column
changes (deploy the code that tolerates both shapes first).
""",
    "Kiến trúc truy cập dữ liệu",
    "Pool, repository, và unit-of-work: giữ cơ chế database tách khỏi logic nghiệp vụ mà không cần xây một ORM giả.",
    """
## Connection pool

Mở một kết nối database tốn một bắt tay mạng, một lượt xác thực, và bộ nhớ
phía server. Một **pool** sở hữu một tập kết nối cố định và cho mượn chúng:

- `checkout()` — mượn một (chờ hoặc fail nếu cạn: *backpressure*),
- `checkin(conn)` — trả lại (pool rollback mọi transaction còn mở trước — một
  kết nối mượn phải trả về sạch sẽ),
- không bao giờ chia sẻ một kết nối giữa hai đơn vị công việc đồng thời.

Kích thước pool là một sự cân bằng: quá nhỏ thì request xếp hàng; quá lớn thì
database chết chìm trong context switching. Bắt đầu nhỏ (vài kết nối mỗi
worker) và đo.

## Repository: từ vựng của domain bạn

Một repository phơi **các bộ sưu tập đối tượng nghiệp vụ**, không phải bảng:

```python
class OrderRepository:
    def get(self, order_id) -> Order | None: ...
    def add(self, order) -> None: ...
    def for_customer(self, customer_id) -> list[Order]: ...
```

Hợp đồng của nó: raise *lỗi domain* (`OrderNotFound`), trả về *đối tượng
domain*, và không bao giờ làm lộ SQL hay row tuple lên phía trên. Ranh giới đó
cho phép test thay một fake trong bộ nhớ, cho phép schema thay đổi mà không
đụng tới caller, và — lời cảnh báo trung thực — tốn một tầng dịch. Nó xứng đáng
với domain phức tạp, không phải CRUD mỏng.

## Unit of work: một transaction, một quyết định

Một unit of work gom các thay đổi và commit chúng **nguyên tử**:

```python
with uow:
    uow.orders.add(order)
    uow.payments.record(payment)
# commit xảy ra khi thoát; hoặc cả hai được lưu, hoặc không cái nào
```

Quy tắc từ module API quay trở lại: *handler* khai báo unit of work; cơ chế sở
hữu kết nối và transaction. Logic nghiệp vụ không bao giờ tự gọi `BEGIN` hay
`COMMIT`.

## Migration: đổi schema là đổi code

Schema tiến hóa; database phải di chuyển cùng code. Một migration là một bước
nhỏ, có thứ tự, có phiên bản (tạo bảng, thêm cột với default, backfill, thêm
ràng buộc). Hai kỷ luật: mọi migration đều đảo ngược được hoặc tường minh là
một-chiều-và-nguy-h hiểm, và *thêm-rồi-migrate-rồi-bỏ* cho các thay đổi cột phá
vặng (trước tiên deploy code chịu được cả hai hình dạng).
""",
)

# ── practice 1: schema & queries ─────────────────────────────────────────────
NORMALIZE_REF = (
    "def decompose(rows):\n"
    "    '''rows: list of dicts with keys customer_id, customer_name, order_id, total.\n"
    "    Returns (customers, orders): customers = {customer_id: customer_name},\n"
    "    orders = [{'order_id': ..., 'customer_id': ..., 'total': ...}] in first-seen\n"
    "    order of their order_id. Redundant customer names must agree; conflicting\n"
    "    duplicates raise ValueError('conflicting customer name').'''\n"
    "    customers = {}\n"
    "    orders = []\n"
    "    seen = set()\n"
    "    for row in rows:\n"
    "        cid = row['customer_id']\n"
    "        name = row['customer_name']\n"
    "        if cid in customers and customers[cid] != name:\n"
    "            raise ValueError('conflicting customer name')\n"
    "        customers[cid] = name\n"
    "        if row['order_id'] not in seen:\n"
    "            seen.add(row['order_id'])\n"
    "            orders.append({\n"
    "                'order_id': row['order_id'],\n"
    "                'customer_id': cid,\n"
    "                'total': row['total'],\n"
    "            })\n"
    "    return customers, orders\n"
)
NORMALIZE_WRONG = (
    "def decompose(rows):\n"
    "    customers = {}\n"
    "    orders = []\n"
    "    seen = set()\n"
    "    for row in rows:\n"
    "        cid = row['customer_id']\n"
    "        name = row['customer_name']\n"
    "        customers[cid] = name  # WRONG: last-wins overwrite, conflicts silently absorbed\n"
    "        if row['order_id'] not in seen:\n"
    "            seen.add(row['order_id'])\n"
    "            orders.append({\n"
    "                'order_id': row['order_id'],\n"
    "                'customer_id': cid,\n"
    "                'total': row['total'],\n"
    "            })\n"
    "    return customers, orders\n"
)

INDEX_PICK_REF = (
    "def best_index(queries, available):\n"
    "    '''queries: list of dicts like {'filter': ['user_id'], 'sort': 'created_at'}\n"
    "    (filter columns in WHERE order; sort is a single column or None).\n"
    "    available: list of composite index tuples. Returns the index covering the\n"
    "    MOST queries. An index (a, b, ...) covers a query when its leading columns\n"
    "    match the query's filter columns AND its next column equals the sort column.\n"
    "    Ties broken by the earlier index in `available`. Every query must be covered\n"
    "    by at least one index; otherwise raise ValueError('uncovered query').'''\n"
    "    def covers(index, q):\n"
    "        flt = tuple(q.get('filter', []))\n"
    "        if tuple(index[:len(flt)]) != flt:\n"
    "            return False\n"
    "        sort = q.get('sort')\n"
    "        if sort is None:\n"
    "            return True\n"
    "        return len(index) > len(flt) and index[len(flt)] == sort\n"
    "\n"
    "    best, best_count = None, -1\n"
    "    for idx in available:\n"
    "        count = sum(1 for q in queries if covers(idx, q))\n"
    "        if count > best_count:\n"
    "            best, best_count = idx, count\n"
    "    if best_count == 0 and queries:\n"
    "        raise ValueError('uncovered query')\n"
    "    return best\n"
)
INDEX_PICK_WRONG = (
    "def best_index(queries, available):\n"
    "    def covers(index, q):\n"
    "        flt = tuple(q.get('filter', []))\n"
    "        # WRONG: ignores column order — treats (b, a) as covering a filter on (a, b)\n"
    "        return set(index[:len(flt)]) == set(flt)\n"
    "\n"
    "    best, best_count = None, -1\n"
    "    for idx in available:\n"
    "        count = sum(1 for q in queries if covers(idx, q))\n"
    "        if count > best_count:\n"
    "            best, best_count = idx, count\n"
    "    return best\n"
)

write_practice(
    MOD, "pa-p11-schema-practice",
    "Schema & Query Drills",
    "Decompose a denormalized table into the truth, and pick indexes the way the planner must.",
    "Bài tập schema và truy vấn",
    "Phân rã một bảng phi chuẩn thành sự thật, và chọn index đúng cách mà planner phải làm.",
    "relational-thinking", 24, "advanced",
    [
        challenge(
            "pa-db-decompose",
            "Decompose the denormalized table",
            "Implement `decompose(rows)` — rows are dicts with keys `customer_id`, `customer_name`, `order_id`, `total` (a flat order report). Return `(customers, orders)`:\n\n- `customers`: dict mapping `customer_id → customer_name`\n- `orders`: list of `{'order_id', 'customer_id', 'total'}` dicts, in first-seen order of `order_id` (duplicates of an order_id are ignored)\n- redundancy must be consistent: if the same `customer_id` appears with two different names, raise `ValueError('conflicting customer name')`\n\nThis is normalization as code: eliminate the redundancy, keep the truth.",
            "# TODO: decompose",
            [
                ("dedupes customers and orders",
                 "rows = [\n    {'customer_id': 1, 'customer_name': 'Lan', 'order_id': 'o1', 'total': 100},\n    {'customer_id': 1, 'customer_name': 'Lan', 'order_id': 'o2', 'total': 50},\n    {'customer_id': 2, 'customer_name': 'Minh', 'order_id': 'o3', 'total': 70},\n]\ncustomers, orders = decompose(rows)\nassert customers == {1: 'Lan', 2: 'Minh'}\nassert [o['order_id'] for o in orders] == ['o1', 'o2', 'o3']\nprint('ok')",
                 "Each customer once; each order once, in first-seen order."),
                ("conflicts are loud, not silent",
                 "rows = [\n    {'customer_id': 1, 'customer_name': 'Lan', 'order_id': 'o1', 'total': 100},\n    {'customer_id': 1, 'customer_name': 'LAN PHUONG', 'order_id': 'o4', 'total': 10},\n]\ntry:\n    decompose(rows)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('conflicting names must raise')\nprint('ok')",
                 "A silently renamed customer is a data corruption bug."),
            ],
            level="independent",
        ),
        challenge(
            "pa-db-best-index",
            "Pick the index the planner would",
            "Implement `best_index(queries, available)`:\n\n- each query is `{'filter': [...columns in WHERE order...], 'sort': column-or-None}`\n- an index tuple `(a, b, c)` covers a query when its leading columns equal the filter columns in order, and its next column equals the sort column (or the query has no sort)\n- return the index covering the most queries; ties go to the earlier index in `available`\n- if any query is covered by NO index, raise `ValueError('uncovered query')`\n\nColumn ORDER matters — this is the leftmost-prefix rule as executable code.",
            "# TODO: best_index",
            [
                ("leftmost prefix, order-sensitive",
                 "queries = [\n    {'filter': ['user_id'], 'sort': 'created_at'},\n    {'filter': ['user_id', 'status'], 'sort': None},\n]\nassert best_index(queries, [('status', 'user_id'), ('user_id', 'status', 'created_at'), ('user_id',)]) == ('user_id', 'status', 'created_at')\nprint('ok')",
                 "(user_id, status, created_at) covers both; (status, user_id) covers neither."),
                ("uncovered queries fail loudly",
                 "try:\n    best_index([{'filter': ['email'], 'sort': None}], [('user_id',)])\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('must raise for uncovered query')\nprint('ok')",
                 "A query no index serves is a production incident waiting."),
            ],
            level="independent",
        ),
    ],
    {
        "pa-db-decompose": vi_challenge(
            "Phân rã bảng phi chuẩn",
            "Cài `decompose(rows)` — rows là list dict với keys `customer_id`, `customer_name`, `order_id`, `total` (một báo cáo đơn hàng phẳng). Trả `(customers, orders)`:\n\n- `customers`: dict ánh xạ `customer_id → customer_name`\n- `orders`: list các dict `{'order_id', 'customer_id', 'total'}`, theo thứ tự xuất hiện đầu tiên của `order_id` (order_id trùng lặp bị bỏ qua)\n- dư thừa phải nhất quán: nếu cùng `customer_id` xuất hiện với hai tên khác nhau, raise `ValueError('conflicting customer name')`\n\nĐây là chuẩn hóa bằng code: loại bỏ dư thừa, giữ lại sự thật.",
            [("Khử trùng lặp customer và order", "Mỗi customer một lần; mỗi order một lần, theo thứ tự xuất hiện đầu."),
             ("Xung đột phải ầm ĩ, không im lặng", "Một khách hàng bị đổi tên ngầm là bug hỏng dữ liệu.")],
        ),
        "pa-db-best-index": vi_challenge(
            "Chọn index như planner",
            "Cài `best_index(queries, available)`:\n\n- mỗi query là `{'filter': [...các cột theo thứ tự trong WHERE...], 'sort': cột-hoặc-None}`\n- index tuple `(a, b, c)` phủ một query khi các cột đầu của nó bằng các cột filter theo đúng thứ tự, và cột kế tiếp bằng cột sort (hoặc query không có sort)\n- trả index phủ nhiều query nhất; hòa thì index đứng trước trong `available` thắng\n- nếu có query KHÔNG được index nào phủ, raise `ValueError('uncovered query')`\n\nThứ tự cột là điều kiện bắt buộc — đây là quy tắc tiền-tố-trái nhất dưới dạng code.",
            [("Tiền tố trái nhất, nhạy thứ tự", "(user_id, status, created_at) phủ cả hai; (status, user_id) không phủ cái nào."),
             ("Truy vấn không được phủ phải fail ầm ĩ", "Một truy vấn không index nào phục vụ là sự cố chờ ngày.")],
        ),
    },
    solutions=[("pa-db-decompose", NORMALIZE_REF, NORMALIZE_WRONG),
               ("pa-db-best-index", INDEX_PICK_REF, INDEX_PICK_WRONG)],
)

# ── practice 2: transactions ─────────────────────────────────────────────────
OCC_REF = (
    "def apply_update(row, mutate, seen_version=None):\n"
    "    '''Optimistic concurrency. row: {'id', 'version', ...}. mutate(row_dict)\n"
    "    edits a candidate copy. Simulates UPDATE ... WHERE id=? AND version=seen:\n"
    "    - success: {'ok': True, 'row': new_row (version bumped), 'attempts': n}\n"
    "    - each conflict (someone else bumped the version first) consumes one attempt;\n"
    "      after 3 failed attempts: {'ok': False, 'attempts': 3}\n"
    "    `conflict_on_attempt` is a set of 1-based attempt numbers that simulate\n"
    "    losing a race.'''\n"
    "    attempts = 0\n"
    "    while attempts < 3:\n"
    "        attempts += 1\n"
    "        seen = row['version']\n"
    "        candidate = dict(row)\n"
    "        mutate(candidate)\n"
    "        if attempts in conflict_on_attempt:\n"
    "            row = dict(row)\n"
    "            row['version'] += 1  # the other writer's commit landed first\n"
    "            continue\n"
    "        candidate['version'] = seen + 1\n"
    "        return {'ok': True, 'row': candidate, 'attempts': attempts}\n"
    "    return {'ok': False, 'attempts': attempts}\n"
)
OCC_REF = OCC_REF.replace(
    "def apply_update(row, mutate, seen_version=None):",
    "def apply_update(row, mutate, conflict_on_attempt=()):",
)
OCC_WRONG = (
    "def apply_update(row, mutate, conflict_on_attempt=()):\n"
    "    attempts = 0\n"
    "    while attempts < 3:\n"
    "        attempts += 1\n"
    "        candidate = dict(row)\n"
    "        mutate(candidate)\n"
    "        if attempts in conflict_on_attempt:\n"
    "            row = dict(row)\n"
    "            row['version'] += 1\n"
    "            continue\n"
    "        candidate['version'] = candidate.get('version', 0) + 1  # WRONG: bumps from the candidate, not the seen version\n"
    "        return {'ok': True, 'row': candidate, 'attempts': attempts}\n"
    "    return {'ok': False, 'attempts': attempts}\n"
)

POOL_REF = (
    "class ConnectionPool:\n"
    "    def __init__(self, size):\n"
    "        self._free = [f'conn-{i}' for i in range(size)]\n"
    "        self._lent = 0\n"
    "\n"
    "    def checkout(self):\n"
    "        '''Lend a connection or raise PoolExhausted (backpressure, not blocking).'''\n"
    "        if not self._free:\n"
    "            raise PoolExhausted('pool exhausted')\n"
    "        self._lent += 1\n"
    "        return self._free.pop()\n"
    "\n"
    "    def checkin(self, conn, dirty=False):\n"
    "        '''Return a connection. A dirty one is rolled back before reuse.'''\n"
    "        if dirty:\n"
    "            conn = conn + ':clean'   # simulated ROLLBACK\n"
    "        self._free.append(conn)\n"
    "        self._lent -= 1\n"
    "\n"
    "    @property\n"
    "    def in_use(self):\n"
    "        return self._lent\n"
    "\n"
    "\n"
    "class PoolExhausted(Exception):\n"
    "    pass\n"
)
POOL_WRONG = (
    "class ConnectionPool:\n"
    "    def __init__(self, size):\n"
    "        self._free = [f'conn-{i}' for i in range(size)]\n"
    "        self._lent = 0\n"
    "\n"
    "    def checkout(self):\n"
    "        # WRONG: over-commits beyond the pool size\n"
    "        if self._lent > 2 * len(self._free) + size_guard(self):\n"
    "            raise PoolExhausted('pool exhausted')\n"
    "        self._lent += 1\n"
    "        return f'conn-{self._lent}'\n"
    "\n"
    "    def checkin(self, conn, dirty=False):\n"
    "        self._lent -= 1\n"
    "\n"
    "    @property\n"
    "    def in_use(self):\n"
    "        return self._lent\n"
    "\n"
    "\n"
    "def size_guard(_):\n"
    "    return 0\n"
    "\n"
    "\n"
    "class PoolExhausted(Exception):\n"
    "    pass\n"
)

write_practice(
    MOD, "pa-p11-tx-practice",
    "Transaction & Pool Drills",
    "Optimistic concurrency with version checks, and a pool that enforces its own capacity.",
    "Bài tập transaction và pool",
    "Optimistic concurrency với kiểm tra phiên bản, và một pool tự thực thi dung lượng của chính nó.",
    "sql-and-transactions", 24, "advanced",
    [
        challenge(
            "pa-db-occ",
            "Optimistic concurrency, simulated",
            "Implement `apply_update(row, mutate, conflict_on_attempt=())` — an optimistic-concurrency update over `row` (a dict containing `'id'` and `'version'`):\n\n- loop up to 3 attempts; on each: `seen = row['version']`, copy the row, apply `mutate(copy)`\n- if the attempt number is in `conflict_on_attempt`, simulate losing the race: the stored row's version increments (another writer committed) and you retry\n- otherwise the write lands: the new row keeps the mutations and gets `version = seen + 1`; return `{'ok': True, 'row': new_row, 'attempts': n}`\n- after 3 failed attempts: return `{'ok': False, 'attempts': 3}`\n\nThe discriminating check: a conflict must re-read the bumped version, not blindly overwrite with a stale one.",
            "# TODO: apply_update",
            [
                ("clean write bumps version once",
                 "row = {'id': 7, 'version': 2, 'status': 'new'}\nr = apply_update(row, lambda c: c.update({'status': 'shipped'}))\nassert r['ok'] is True and r['attempts'] == 1\nassert r['row']['status'] == 'shipped' and r['row']['version'] == 3\nassert row['version'] == 2  # original untouched until commit\nprint('ok')",
                 "Copy-mutate-commit; the seen version is what increments."),
                ("conflicts re-read and eventually succeed",
                 "row = {'id': 7, 'version': 0, 'status': 'new'}\nr = apply_update(row, lambda c: c.update({'status': 'x'}), conflict_on_attempt={1, 2})\nassert r['ok'] is True and r['attempts'] == 3\nassert r['row']['version'] == 3  # two lost races (2 bumps) + this writer's commit\nrow2 = {'id': 7, 'version': 0}\nr2 = apply_update(row2, lambda c: None, conflict_on_attempt={1, 2, 3})\nassert r2 == {'ok': False, 'attempts': 3}\nprint('ok')",
                 "Each conflict consumes an attempt; the winner builds on the latest version."),
            ],
            level="combination",
        ),
        challenge(
            "pa-db-pool",
            "A pool that knows its size",
            "Implement `ConnectionPool(size)` with `PoolExhausted`:\n\n- starts with `size` idle connections (`'conn-0'` … `'conn-(size-1)'`)\n- `checkout()` returns an idle connection, or raises `PoolExhausted('pool exhausted')` when none remain — capacity is never exceeded\n- `checkin(conn, dirty=False)` returns the connection to the idle set; if `dirty` is True the returned name gets `':clean'` appended (simulating a ROLLBACK before reuse) — the returned name is what the next checkout hands out\n- `in_use` property: how many connections are currently lent\n\nThe rule under test: a pool of N can never lend more than N.",
            "class PoolExhausted(Exception):\n    pass\n\n\nclass ConnectionPool:\n    def __init__(self, size):\n        ...\n\n    def checkout(self):\n        ...\n\n    def checkin(self, conn, dirty=False):\n        ...\n\n    @property\n    def in_use(self):\n        ...",
            [
                ("capacity is a hard limit, reuse works",
                 "p = ConnectionPool(2)\na = p.checkout(); b = p.checkout()\nassert p.in_use == 2\ntry:\n    p.checkout()\nexcept PoolExhausted:\n    pass\nelse:\n    raise AssertionError('must refuse beyond capacity')\np.checkin(a)\nassert p.in_use == 1\nassert p.checkout() == a\nprint('ok')",
                 "Lend from the idle set only; checked-in connections return to service."),
                ("dirty connections are rolled back before reuse",
                 "p = ConnectionPool(1)\nc = p.checkout()\np.checkin(c, dirty=True)\nassert p.checkout() == c + ':clean'\nprint('ok')",
                 "A borrowed connection must come back clean."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-db-occ": vi_challenge(
            "Optimistic concurrency, mô phỏng",
            "Cài `apply_update(row, mutate, conflict_on_attempt=())` — một lần cập nhật optimistic-concurrency trên `row` (dict chứa `'id'` và `'version'`):\n\n- lặp tối đa 3 lần thử; mỗi lần: `seen = row['version']`, copy row, áp dụng `mutate(copy)`\n- nếu số lần thử nằm trong `conflict_on_attempt`, mô phỏng việc thua tranh chấp: phiên bản của dòng lưu trữ tăng lên (writer khác đã commit) và bạn thử lại\n- ngược lại lần ghi thành công: dòng mới giữ các thay đổi và có `version = seen + 1`; trả `{'ok': True, 'row': new_row, 'attempts': n}`\n- sau 3 lần thử thất bại: trả `{'ok': False, 'attempts': 3}`\n\nPhép kiểm phân biệt: một xung đột phải đọc lại phiên bản đã tăng, không được ghi đè mù quáng bằng bản cũ.",
            [("Ghi sạch tăng phiên bản đúng một lần", "Copy-mutate-commit; phiên bản đã thấy là thứ được tăng."),
             ("Xung đột đọc lại rồi cuối cùng thành công", "Mỗi xung đột tốn một lần thử; kẻ thắng dựa trên phiên bản mới nhất.")],
        ),
        "pa-db-pool": vi_challenge(
            "Pool biết kích thước của chính nó",
            "Cài `ConnectionPool(size)` với `PoolExhausted`:\n\n- khởi tạo với `size` kết nối rảnh (`'conn-0'` … `'conn-(size-1)'`)\n- `checkout()` trả một kết nối rảnh, hoặc raise `PoolExhausted('pool exhausted')` khi không còn — dung lượng không bao giờ bị vượt\n- `checkin(conn, dirty=False)` trả kết nối về tập rảnh; nếu `dirty` là True thì tên trả về được thêm `':clean'` (mô phỏng ROLLBACK trước khi tái sử dụng) — tên đó là thứ lần checkout kế tiếp trao đi\n- property `in_use`: bao nhiêu kết nối đang được cho mượn\n\nQuy tắc bị kiểm: pool N không bao giờ cho mượn quá N.",
            [("Dung lượng là trần cứng, tái sử dụng hoạt động", "Chỉ cho mượn từ tập rảnh; kết nối đã trả quay lại phục vụ."),
             ("Kết nối bẩn được rollback trước khi tái sử dụng", "Một kết nối mượn phải trả về sạch sẽ.")],
        ),
    },
    solutions=[("pa-db-occ", OCC_REF, OCC_WRONG),
               ("pa-db-pool", POOL_REF, POOL_WRONG)],
)

# ── practice 3: data project ─────────────────────────────────────────────────
N1_REF = (
    "def count_queries(request_log):\n"
    "    '''request_log: list of (request_id, [query_description, ...]).\n"
    "    Returns (total, offenders): total = number of queries across all requests;\n"
    "    offenders = request_ids (in first-seen order) executing strictly more than\n"
    "    one query PER fetched entity — the N+1 signature: >= 4 queries where the\n"
    "    extra queries are 1-per-entity (all queries after the first share the same\n"
    "    prefix 'fetch-one:').'''\n"
    "    total = 0\n"
    "    offenders = []\n"
    "    for request_id, queries in request_log:\n"
    "        total += len(queries)\n"
    "        ones = [q for q in queries if q.startswith('fetch-one:')]\n"
    "        if len(ones) >= 3 and queries[0].startswith('fetch-all:'):\n"
    "            offenders.append(request_id)\n"
    "    return total, offenders\n"
)
N1_WRONG = (
    "def count_queries(request_log):\n"
    "    total = 0\n"
    "    offenders = []\n"
    "    for request_id, queries in request_log:\n"
    "        total += len(queries)\n"
    "        if len(queries) > 3:  # WRONG: any big request counts as N+1\n"
    "            offenders.append(request_id)\n"
    "    return total, offenders\n"
)

REPO_REF = (
    "class OrderNotFound(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "class OrderRepository:\n"
    "    '''Domain-shaped repository over an in-memory table (list of row dicts).'''\n"
    "\n"
    "    def __init__(self, rows=None):\n"
    "        self._rows = list(rows or [])\n"
    "\n"
    "    def get(self, order_id):\n"
    "        for row in self._rows:\n"
    "            if row['id'] == order_id:\n"
    "                return dict(row)\n"
    "        raise OrderNotFound(f'order {order_id} not found')\n"
    "\n"
    "    def add(self, order_id, total, customer_id):\n"
    "        if any(r['id'] == order_id for r in self._rows):\n"
    "            raise ValueError('duplicate order id')\n"
    "        self._rows.append({'id': order_id, 'total': total, 'customer_id': customer_id})\n"
    "\n"
    "    def for_customer(self, customer_id):\n"
    "        return [dict(r) for r in self._rows if r['customer_id'] == customer_id]\n"
)
REPO_WRONG = (
    "class OrderNotFound(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "class OrderRepository:\n"
    "    def __init__(self, rows=None):\n"
    "        self._rows = list(rows or [])\n"
    "\n"
    "    def get(self, order_id):\n"
    "        for row in self._rows:\n"
    "            if row['id'] == order_id:\n"
    "                return dict(row)\n"
    "        return None  # WRONG: missing orders silently become None — domain error lost\n"
    "\n"
    "    def add(self, order_id, total, customer_id):\n"
    "        self._rows.append({'id': order_id, 'total': total, 'customer_id': customer_id})  # WRONG: duplicates accepted\n"
    "\n"
    "    def for_customer(self, customer_id):\n"
    "        return [dict(r) for r in self._rows if r['customer_id'] == customer_id]\n"
)

write_practice(
    MOD, "pa-p11-data-project",
    "Data Service Mini-Project",
    "Detect N+1 from a query log, and build a repository that speaks the domain's language.",
    "Dự án mini dữ liệu",
    "Phát hiện N+1 từ một query log, và xây một repository nói thứ tiếng của domain.",
    "data-access-architecture", 30, "advanced",
    [
        challenge(
            "pa-db-n1-detect",
            "Detect N+1 from the query log",
            "Implement `count_queries(request_log)` — `request_log` is a list of `(request_id, queries)` where `queries` is a list of strings:\n\n- `'fetch-all:<entity>'` queries load a collection\n- `'fetch-one:<entity>:<id>'` queries load one entity in a loop\n- return `(total, offenders)`: `total` counts every query; `offenders` lists request_ids (first-seen order) with the N+1 signature — a `fetch-all` followed by **3 or more** `fetch-one` queries\n\nA request with many queries but no fetch-all-then-loop pattern is NOT an offender (batch jobs do big legitimate work).",
            "# TODO: count_queries",
            [
                ("the N+1 signature is specific",
                 "log = [\n    ('r1', ['fetch-all:orders', 'fetch-one:customer:c1', 'fetch-one:customer:c2', 'fetch-one:customer:c3']),\n    ('r2', ['fetch-all:orders', 'fetch-all:customers']),\n    ('r3', ['fetch-one:x:1', 'fetch-one:x:2', 'fetch-one:x:3', 'fetch-one:x:4']),\n]\ntotal, offenders = count_queries(log)\nassert total == 10\nassert offenders == ['r1'], offenders\nprint('ok')",
                 "r1 is classic N+1; r2 is two batch loads; r3 has no fetch-all root."),
            ],
            level="debugging",
        ),
        challenge(
            "pa-db-repository",
            "The repository speaks domain, not rows",
            "Implement `OrderRepository(rows=None)` with `OrderNotFound`:\n\n- `get(order_id)` returns a COPY of the matching row, or raises `OrderNotFound`\n- `add(order_id, total, customer_id)` appends a row; duplicate ids raise `ValueError('duplicate order id')`\n- `for_customer(customer_id)` returns copies of matching rows\n\nThe contract under test: missing data is a loud domain error, duplicates are integrity violations, and callers can never mutate internal state.",
            "class OrderNotFound(Exception):\n    pass\n\n\nclass OrderRepository:\n    def __init__(self, rows=None):\n        ...\n\n    def get(self, order_id):\n        ...\n\n    def add(self, order_id, total, customer_id):\n        ...\n\n    def for_customer(self, customer_id):\n        ...",
            [
                ("domain errors and integrity",
                 "repo = OrderRepository([{'id': 'o1', 'total': 100, 'customer_id': 1}])\ntry:\n    repo.get('nope')\nexcept OrderNotFound:\n    pass\nelse:\n    raise AssertionError('missing order must raise')\nrepo.add('o2', 50, 1)\ntry:\n    repo.add('o2', 99, 2)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('duplicate id must raise')\nprint('ok')",
                 "Loud errors on missing and duplicate; the repository protects its invariants."),
                ("copies, not live references",
                 "repo = OrderRepository([{'id': 'o1', 'total': 100, 'customer_id': 1}])\nsnap = repo.get('o1')\nsnap['total'] = 999\nassert repo.get('o1')['total'] == 100\nrows = repo.for_customer(1)\nrows[0]['total'] = 999\nassert repo.for_customer(1)[0]['total'] == 100\nprint('ok')",
                 "Mutating a returned row must never touch the store."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-db-n1-detect": vi_challenge(
            "Phát hiện N+1 từ query log",
            "Cài `count_queries(request_log)` — `request_log` là list các `(request_id, queries)` với `queries` là list chuỗi:\n\n- `'fetch-all:<entity>'` nạp một bộ sưu tập\n- `'fetch-one:<entity>:<id>'` nạp một thực thể trong vòng lặp\n- trả `(total, offenders)`: `total` đếm mọi truy vấn; `offenders` liệt kê request_id (theo thứ tự xuất hiện đầu) có dấu hiệu N+1 — một `fetch-all` theo sau bởi **3 hoặc nhiều hơn** truy vấn `fetch-one`\n\nRequest có nhiều truy vấn nhưng không theo mẫu fetch-all-rồi-vòng-lặp KHÔNG phải offender (job chạy hàng loạt làm việc lớn hợp pháp).",
            [("Dấu hiệu N+1 phải cụ thể", "r1 là N+1 kinh điển; r2 là hai lần nạp batch; r3 không có gốc fetch-all.")],
        ),
        "pa-db-repository": vi_challenge(
            "Repository nói tiếng domain, không phải tiếng dòng",
            "Cài `OrderRepository(rows=None)` với `OrderNotFound`:\n\n- `get(order_id)` trả một BẢN SAO của dòng khớp, hoặc raise `OrderNotFound`\n- `add(order_id, total, customer_id)` thêm một dòng; id trùng raise `ValueError('duplicate order id')`\n- `for_customer(customer_id)` trả bản sao của các dòng khớp\n\nHợp đồng bị kiểm: dữ liệu thiếu là lỗi domain ầm ĩ, trùng lặp là vi phạm toàn vẹn, và caller không bao giờ can thiệp được trạng thái nội bộ.",
            [("Lỗi domain và tính toàn vẹn", "Lỗi ầm ĩ cho thiếu và trùng; repository bảo vệ các bất biến của nó."),
             ("Bản sao, không phải tham chiếu sống", "Thay đổi một dòng được trả về không bao giờ được chạm vào kho.")],
        ),
    },
    solutions=[("pa-db-n1-detect", N1_REF, N1_WRONG),
               ("pa-db-repository", REPO_REF, REPO_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
write_checkpoint(
    MOD, "pa-checkpoint-databases",
    "Checkpoint: Databases & Data Access",
    "Prove you can fight for consistency under contention and keep the pool honest.",
    25,
    """
**The exam question:** two workers update the same inventory row at the same
time. Both read `stock = 1`. Both decrement. How many widgets does the customer
buy? One — if you built the write correctly.

The checkpoint challenge combines optimistic concurrency and the unit-of-work
rule: apply a batch of decrements against a simulated table, where concurrent
writers (the `conflict_on_attempt` simulation from the practice) race you, and
each unit of work must either fully land or cleanly retry.
""",
    "Checkpoint: Database và truy cập dữ liệu",
    "Chứng minh bạn giành được tính nhất quán dưới tranh chấp và giữ pool trung thực.",
    """
**Câu hỏi thi:** hai worker cập nhật cùng một dòng tồn kho cùng lúc. Cả hai đọc
`stock = 1`. Cả hai trừ đi. Khách hàng mua bao nhiêu cái? Một — nếu bạn xây
đúng phần ghi.

Thử thách checkpoint kết hợp optimistic concurrency và quy tắc unit-of-work:
áp một loạt phép trừ lên một bảng mô phỏng, nơi các writer đồng thời (mô phỏng
`conflict_on_attempt` từ bài tập) tranh chấp với bạn, và mỗi đơn vị công việc
phải hoặc thành công trọn vẹn hoặc retry sạch sẽ.
""",
    challenge(
        "pa-db-inventory-checkout",
        "Fight for the last unit of stock",
        "Implement `checkout(rows, requests)` — a reservation system over `rows` (a list of dicts `{'sku', 'stock', 'version'}`):\n\n- each request is `(sku, conflict_on_attempt_set)` meaning: decrement that SKU's stock by 1, where the given 1-based attempt numbers lose a race (another writer bumped the version first)\n- apply optimistic concurrency per request: read version, mutate, conflict → retry with the bumped row, up to **3 attempts**; after that the request fails\n- a request fails immediately if the stock is 0 at the moment of a winning write: return its sku in `out_of_stock` instead\n- return `{'rows': rows_after_all_requests, 'applied': [skus in request order], 'out_of_stock': [skus that failed]}`\n\nThe invariant: two requests racing for the last unit — exactly one wins, the loser reports `out_of_stock` (or retries and then reports honestly).",
        "# TODO: checkout(rows, requests)",
        [
            ("the loser loses, honestly",
             "rows = [{'sku': 'A', 'stock': 1, 'version': 0}]\nr = checkout(rows, [('A', set()), ('A', set())])\nassert r['applied'] == ['A']\nassert r['out_of_stock'] == ['A']\nfinal = [row for row in r['rows'] if row['sku'] == 'A'][0]\nassert final['stock'] == 0 and final['version'] == 1\nprint('ok')",
             "Two requests, one unit: exactly one wins; the other reports honestly."),
            ("conflicts consume attempts, then succeed",
             "rows = [{'sku': 'B', 'stock': 5, 'version': 0}]\nr = checkout(rows, [('B', {1, 2})])\nassert r['applied'] == ['B'] and r['out_of_stock'] == []\nfinal = [row for row in r['rows'] if row['sku'] == 'B'][0]\nassert final['stock'] == 4\nprint('ok')",
             "Losing races retries with the bumped row; the write lands on the latest state."),
        ],
        level="build",
    ),
    vi_challenge(
        "Giành món hàng cuối cùng",
        "Cài `checkout(rows, requests)` — một hệ thống đặt trước trên `rows` (list dict `{'sku', 'stock', 'version'}`):\n\n- mỗi request là `(sku, conflict_on_attempt_set)` nghĩa là: trừ tồn kho của SKU đó đi 1, trong đó các số lần thử (bắt đầu từ 1) cho trước sẽ thua tranh chấp (writer khác tăng phiên bản trước)\n- áp dụng optimistic concurrency cho từng request: đọc phiên bản, thay đổi, xung đột → retry với dòng đã tăng, tối đa **3 lần thử**; sau đó request thất bại\n- request thất bại ngay nếu stock bằng 0 tại thời điểm ghi thành công: trả sku của nó trong `out_of_stock`\n- trả `{'rows': rows_sau_tất_cả_request, 'applied': [sku theo thứ tự request], 'out_of_stock': [sku thất bại]}`\n\nBất biến: hai request tranh chấp món cuối — đúng một cái thắng, kẻ thua báo `out_of_stock` (hoặc retry rồi báo một cách trung thực).",
            [("Kẻ thua thua một cách trung thực", "Hai request, một món: đúng một cái thắng; cái kia báo thật."),
             ("Xung đột tốn lần thử, rồi thành công", "Thua tranh chấp thì retry với dòng đã tăng; lần ghi hạ xuống trạng thái mới nhất.")],
    ),
    solution=(
        "def checkout(rows, requests):\n"
        "    state = {r['sku']: dict(r) for r in rows}\n"
        "    applied, out = [], []\n"
        "    for sku, conflicts in requests:\n"
        "        attempts = 0\n"
        "        done = False\n"
        "        while attempts < 3 and not done:\n"
        "            attempts += 1\n"
        "            row = dict(state[sku])\n"
        "            if attempts in conflicts:\n"
        "                row['version'] += 1\n"
        "                state[sku] = row\n"
        "                continue\n"
        "            if row['stock'] <= 0:\n"
        "                out.append(sku)\n"
        "                done = True\n"
        "                continue\n"
        "            row['stock'] -= 1\n"
        "            row['version'] = row['version'] + 1\n"
        "            state[sku] = row\n"
        "            applied.append(sku)\n"
        "            done = True\n"
        "        if not done and sku not in out:\n"
        "            out.append(sku)\n"
        "    return {'rows': list(state.values()), 'applied': applied, 'out_of_stock': out}\n"
    ),
    wrong=(
        "def checkout(rows, requests):\n"
        "    state = {r['sku']: dict(r) for r in rows}\n"
        "    applied, out = [], []\n"
        "    for sku, conflicts in requests:\n"
        "        row = state[sku]\n"
        "        if row['stock'] <= 0:\n"
        "            out.append(sku)\n"
        "            continue\n"
        "        row['stock'] -= 1  # WRONG: no version check — both writers decrement the same unit\n"
        "        applied.append(sku)\n"
        "    return {'rows': list(state.values()), 'applied': applied, 'out_of_stock': out}\n"
    ),
)

print("module 11 complete")
