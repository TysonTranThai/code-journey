#!/usr/bin/env python3
"""Python Intermediate — module 8 (databases)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

M8 = "databases"
L8A = "sql-fundamentals"
L8B = "parameterized-queries"
L8C = "transactions-schema"
L8D = "repository-pattern"
L8E = "checkpoint-database-app"

write_module(
    M8,
    "Databases and SQL with Python",
    "Persist real data with SQLite: queries, transactions, constraints — and parameterized everything.",
    "Cơ sở dữ liệu và SQL với Python",
    "Lưu trữ dữ liệu thật với SQLite: truy vấn, transaction, ràng buộc — và tham số hóa tất cả.",
    [L8A, L8B, L8C, L8D, L8E],
    ["m8-sql-practice", "m8-params-practice", "m8-tx-practice", "m8-repo-practice"],
)

write_lesson(
    M8, L8A,
    "SQL Fundamentals",
    "Tables, SELECT, INSERT, WHERE, ORDER BY, JOIN — the vocabulary of persistence.",
    15,
    '''
A relational database stores **tables** of rows with typed columns. SQL is
the query language; SQLite is the zero-config engine built into Python:

```python
import sqlite3

conn = sqlite3.connect(":memory:")     # or "app.db" for a real file
conn.execute(
    """
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )
    """
)
conn.execute("INSERT INTO tasks (title) VALUES (?)", ("write lesson",))
conn.commit()

rows = conn.execute("SELECT id, title FROM tasks WHERE done = 0").fetchall()
```

The vocabulary that matters:

- **SELECT ... FROM ... WHERE** — read rows matching a condition.
- **ORDER BY ... LIMIT** — sort and take the top rows.
- **INSERT INTO ... VALUES** — add rows; **UPDATE ... SET ... WHERE** — modify matched rows.
- **DELETE FROM ... WHERE** — remove rows. (The WHERE on UPDATE/DELETE is not optional in practice — forgetting it changes every row.)
- **COUNT, SUM, AVG, GROUP BY** — aggregate per group: `SELECT region, SUM(amount) FROM sales GROUP BY region`.

`conn.row_factory = sqlite3.Row` makes rows behave like dicts
(`row["title"]`) — better than bare tuples for readability.
''',
    "Nền tảng SQL",
    "Bảng, SELECT, INSERT, WHERE, ORDER BY, JOIN — vốn từ của việc lưu trữ.",
    '''
Cơ sở dữ liệu quan hệ lưu **bảng** gồm các dòng với cột có kiểu. SQL là
ngôn ngữ truy vấn; SQLite là engine không cần cấu hình, tích hợp sẵn trong
Python:

```python
import sqlite3

conn = sqlite3.connect(":memory:")     # hoặc "app.db" cho tệp thật
conn.execute(
    """
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )
    """
)
conn.execute("INSERT INTO tasks (title) VALUES (?)", ("write lesson",))
conn.commit()

rows = conn.execute("SELECT id, title FROM tasks WHERE done = 0").fetchall()
```

Vốn từ quan trọng:

- **SELECT ... FROM ... WHERE** — đọc các dòng khớp điều kiện.
- **ORDER BY ... LIMIT** — sắp và lấy nhóm dòng đầu.
- **INSERT INTO ... VALUES** — thêm dòng; **UPDATE ... SET ... WHERE** — sửa các dòng khớp.
- **DELETE FROM ... WHERE** — xóa dòng. (WHERE trong UPDATE/DELETE không phải tùy chọn — quên nó là thay đổi mọi dòng.)
- **COUNT, SUM, AVG, GROUP BY** — tổng hợp theo nhóm: `SELECT region, SUM(amount) FROM sales GROUP BY region`.

`conn.row_factory = sqlite3.Row` khiến dòng dữ liệu dùng như dict
(`row["title"]`) — dễ đọc hơn tuple trần.
''',
)

write_lesson(
    M8, L8B,
    "Parameterized Queries: The Law",
    "Never build SQL with string formatting — placeholders separate code from data.",
    15,
    """
The single most important database habit, stated as a law: **SQL and data
travel separately.** Placeholders (`?` in sqlite3) hand values to the driver,
which binds them safely:

```python
# GOOD: the value is data, never executable SQL
conn.execute("SELECT * FROM users WHERE name = ?", (user_input,))

# NEVER: string formatting builds executable SQL from input
conn.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
```

Why the f-string version is catastrophic: input `' OR '1'='1` turns the query
into `WHERE name = '' OR '1'='1'` — matching **every user**. That is SQL
injection, and it has topped vulnerability lists for two decades. A parameter
binds `' OR '1'='1` as a *literal string to compare*, defusing it completely.

## What parameters cannot do

Placeholders only work where a **value** belongs: after `=`, `IN (...)`,
`VALUES`. Identifiers (table names, column names) cannot be parameterized —
if those must be dynamic, validate against a whitelist:

```python
ALLOWED_SORTS = {"title": "title", "created": "id"}
column = ALLOWED_SORTS.get(user_choice)      # None → reject
if column is None:
    raise ValueError("invalid sort column")
```

## executemany for batches

```python
conn.executemany("INSERT INTO tasks (title) VALUES (?)", [("a",), ("b",)])
```

One round trip for many rows — and one more place the driver handles the
escaping for you.
""",
    "Truy vấn tham số hóa: Quy tắc bất di bất dịch",
    "Không bao giờ dựng SQL bằng chuỗi — placeholder tách mã khỏi dữ liệu.",
    """
Thói quen cơ sở dữ liệu quan trọng nhất, phát biểu thành luật: **SQL và dữ
liệu đi hai đường riêng.** Placeholder (`?` trong sqlite3) trao giá trị cho
driver, driver gán chúng một cách an toàn:

```python
# ĐÚNG: giá trị là dữ liệu, không bao giờ là SQL chạy được
conn.execute("SELECT * FROM users WHERE name = ?", (user_input,))

# TUYỆT ĐỐI KHÔNG: định dạng chuỗi dựng SQL chạy được từ input
conn.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
```

Vì sao bản f-string là thảm họa: input `' OR '1'='1` biến truy vấn thành
`WHERE name = '' OR '1'='1'` — khớp **mọi người dùng**. Đó là SQL injection,
nhiều thập kỷ nằm đầu danh sách lỗ hổng. Một tham số gắn `' OR '1'='1` như
*chuỗi so sánh nguyên văn*, vô hiệu hóa hoàn toàn.

## Tham số không làm được gì

Placeholder chỉ hoạt động nơi **giá trị** đứng: sau `=`, `IN (...)`,
`VALUES`. Định danh (tên bảng, tên cột) không thể tham số hóa — nếu buộc phải
động, hãy xác thực theo whitelist:

```python
ALLOWED_SORTS = {"title": "title", "created": "id"}
column = ALLOWED_SORTS.get(user_choice)      # None → từ chối
if column is None:
    raise ValueError("invalid sort column")
```

## executemany cho theo lô

```python
conn.executemany("INSERT INTO tasks (title) VALUES (?)", [("a",), ("b",)])
```

Một lượt cho nhiều dòng — và thêm một chỗ driver lo phần escape thay bạn.
""",
)

write_lesson(
    M8, L8C,
    "Transactions and Schema Integrity",
    "Commit, rollback, constraints, and indexes — correctness by construction.",
    14,
    """
A **transaction** makes a group of statements all-or-nothing. Money moves A
→ B? Both updates commit together or neither does:

```python
try:
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (100, 1))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (100, 2))
    conn.commit()                    # both applied
except sqlite3.Error:
    conn.rollback()                  # neither applied
```

## Constraints: the database defends itself

Schema-level rules enforce integrity even against buggy code:

```python
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 0)
)
```

`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, and foreign keys make bad data
impossible at the storage layer — `IntegrityError` beats silently corrupted
tables. **Indexes** (`CREATE INDEX idx_tasks_done ON tasks(done)`) make
filtered queries fast; every index slightly slows writes, so index the
columns you actually filter on.

## Connections are resources

Connection discipline from module 3 applies: open with `with` semantics where
possible, close deterministically, and keep one connection per logical unit
of work. Long-lived shared connections plus threads is a classic deadlock
recipe — the capstone keeps storage single-threaded for exactly this reason.
""",
    "Transaction và Toàn vẹn Schema",
    "Commit, rollback, ràng buộc, và index — đúng đắn ngay từ cấu trúc.",
    """
**Transaction** khiến một nhóm câu lệnh hoặc là tất cả hoặc là không có gì.
Chuyển tiền A → B? Cả hai cập nhật commit cùng nhau hoặc không cái nào:

```python
try:
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (100, 1))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (100, 2))
    conn.commit()                    # cả hai được áp dụng
except sqlite3.Error:
    conn.rollback()                  # không cái nào được áp dụng
```

## Ràng buộc: cơ sở dữ liệu tự vệ

Quy tắc ở mức schema bảo đảm tính toàn vẹn ngay cả trước code có lỗi:

```python
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 0)
)
```

`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, và khóa ngoại khiến dữ liệu xấu
trở nên bất khả thi ở tầng lưu trữ — `IntegrityError` tốt hơn bảng bị hỏng
một cách lặng lẽ. **Index** (`CREATE INDEX idx_tasks_done ON tasks(done)`)
làm truy vấn lọc nhanh lên; mỗi index làm ghi chậm đi một chút, nên hãy index
các cột bạn thực sự lọc.

## Connection là một tài nguyên

Kỷ luật connection từ module 3 vẫn đúng: mở với ngữ nghĩa `with` khi có thể,
đóng dứt khoát, và giữ một connection cho mỗi đơn vị công việc logic.
Connection dùng chung tồn tại lâu cộng với thread là công thức deadlock
kinh điển — capstone giữ storage đơn luồng vì chính lý do này.
""",
)

write_lesson(
    M8, L8D,
    "The Repository Pattern",
    "Hide SQL behind a class: the domain speaks objects, storage speaks tables.",
    13,
    """
Sprinkling SQL through business logic couples everything to storage
details. A **repository** isolates persistence behind a small interface:

```python
class TaskRepository:
    def __init__(self, conn):
        self._conn = conn

    def add(self, title: str) -> int:
        cur = self._conn.execute(
            "INSERT INTO tasks (title) VALUES (?)", (title,)
        )
        self._conn.commit()
        return cur.lastrowid

    def get(self, task_id: int) -> dict | None:
        row = self._conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None

    def all(self) -> list[dict]:
        return [dict(r) for r in self._conn.execute("SELECT id, title, done FROM tasks")]
```

What this buys:

- **The domain stays storage-free**: services call `repo.add(...)`, never SQL. Swap SQLite for Postgres and the domain code doesn't change.
- **Testing gets easy** (module 7!): a fake in-memory repository satisfies the same calls — no database needed to test business rules.
- **SQL lives in one layer**, where review, optimization, and auditing actually happen.

This pattern is the module-4 Protocol idea applied to persistence — and it's
the exact shape of the capstone's storage layer.
""",
    "Mẫu Repository",
    "Che SQL sau một lớp: miền dữ liệu nói object, storage nói bảng.",
    """
Rải SQL khắp business logic khiến mọi thứ bị trói vào chi tiết lưu trữ.
Một **repository** cô lập persistence sau một interface nhỏ:

```python
class TaskRepository:
    def __init__(self, conn):
        self._conn = conn

    def add(self, title: str) -> int:
        cur = self._conn.execute(
            "INSERT INTO tasks (title) VALUES (?)", (title,)
        )
        self._conn.commit()
        return cur.lastrowid

    def get(self, task_id: int) -> dict | None:
        row = self._conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None

    def all(self) -> list[dict]:
        return [dict(r) for r in self._conn.execute("SELECT id, title, done FROM tasks")]
```

Những gì điều này mua được:

- **Miền dữ liệu không dính storage**: service gọi `repo.add(...)`, không bao giờ SQL. Đổi SQLite sang Postgres, code miền không đổi.
- **Test trở nên dễ dàng** (module 7!): một repository giả trong bộ nhớ thỏa mãn cùng các lời gọi — không cần database để test business rule.
- **SQL sống trong một tầng**, nơi review, tối ưu, và audit thực sự diễn ra.

Mẫu này là ý tưởng Protocol của module 4 áp dụng cho persistence — và chính
là hình dạng tầng storage của capstone.
""",
)

# --- module 8 practice sets ---
write_practice(
    M8, "m8-sql-practice",
    "SQL Drills",
    "Create, insert, select, aggregate.",
    "Luyện SQL",
    "Tạo, chèn, truy vấn, tổng hợp.",
    L8A, 30, "intermediate",
    [
        challenge(
            "pi8-sql-crud", "CRUD the Hard Way",
            "Implement setup(conn) that creates table items(id INTEGER PRIMARY KEY, name TEXT NOT NULL, qty INTEGER NOT NULL DEFAULT 0), and restock(conn, name, qty) inserting a row and returning its id.",
            "import sqlite3\n\ndef setup(conn):\n    pass\n\ndef restock(conn, name, qty):\n    pass\n",
            [
                ("creates and inserts",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nsetup(conn)\niid = restock(conn, 'tea', 10)\nrow = conn.execute('SELECT name, qty FROM items WHERE id = ?', (iid,)).fetchone()\nassert row == ('tea', 10)",
                 "CREATE TABLE then INSERT with placeholder values; commit."),
                ("constraint enforced",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nsetup(conn)\ntry:\n    conn.execute('INSERT INTO items (name, qty) VALUES (?, ?)', (None, 1))\n    failed = False\nexcept sqlite3.IntegrityError:\n    failed = True\nassert failed",
                 "NOT NULL must be in the schema — the database rejects violations."),
            ],
            level="guided",
        ),
        challenge(
            "pi8-sql-agg", "Aggregate by Region",
            "Given table sales(region TEXT, amount INTEGER), implement totals_by_region(conn) returning a dict region → SUM(amount), sorted by region name (insertion order of the dict).",
            "import sqlite3\n\ndef totals_by_region(conn):\n    pass\n",
            [
                ("sums per region",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE sales (region TEXT, amount INTEGER)')\nconn.executemany('INSERT INTO sales VALUES (?, ?)', [('east', 5), ('west', 2), ('east', 3)])\nconn.commit()\nassert totals_by_region(conn) == {'east': 8, 'west': 2}",
                 "SELECT region, SUM(amount) ... GROUP BY region."),
                ("empty table gives empty dict",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE sales (region TEXT, amount INTEGER)')\nassert totals_by_region(conn) == {}",
                 "No rows → no keys."),
            ],
            level="independent",
        ),
    ],
    {
        "pi8-sql-crud": vi_challenge("CRUD theo cách chuẩn", "Viết setup(conn) tạo bảng items(id INTEGER PRIMARY KEY, name TEXT NOT NULL, qty INTEGER NOT NULL DEFAULT 0), và restock(conn, name, qty) chèn một dòng rồi trả về id của nó.", [("Tạo bảng và chèn", "CREATE TABLE rồi INSERT với giá trị placeholder; commit."), ("Ràng buộc được thực thi", "NOT NULL phải nằm trong schema — database tự từ chối vi phạm.")]),
        "pi8-sql-agg": vi_challenge("Tổng hợp theo vùng", "Cho bảng sales(region TEXT, amount INTEGER), viết totals_by_region(conn) trả về dict region → SUM(amount), theo thứ tự tên region (thứ tự chèn của dict).", [("Cộng theo từng vùng", "SELECT region, SUM(amount) ... GROUP BY region."), ("Bảng rỗng cho dict rỗng", "Không dòng → không key.")]),
    },
    solutions=[
        ("pi8-sql-crud", "import sqlite3\n\ndef setup(conn):\n    conn.execute('''CREATE TABLE items (\n        id INTEGER PRIMARY KEY,\n        name TEXT NOT NULL,\n        qty INTEGER NOT NULL DEFAULT 0\n    )''')\n    conn.commit()\n\ndef restock(conn, name, qty):\n    cur = conn.execute('INSERT INTO items (name, qty) VALUES (?, ?)', (name, qty))\n    conn.commit()\n    return cur.lastrowid", "import sqlite3\n\ndef setup(conn):\n    conn.execute('''CREATE TABLE items (\n        id INTEGER PRIMARY KEY,\n        name TEXT,\n        qty INTEGER NOT NULL DEFAULT 0\n    )''')\n    conn.commit()\n\ndef restock(conn, name, qty):\n    cur = conn.execute('INSERT INTO items (name, qty) VALUES (?, ?)', (name, qty))\n    conn.commit()\n    return cur.lastrowid"),
        ("pi8-sql-agg", "import sqlite3\n\ndef totals_by_region(conn):\n    rows = conn.execute(\n        'SELECT region, SUM(amount) FROM sales GROUP BY region ORDER BY region'\n    ).fetchall()\n    return {region: total for region, total in rows}", "import sqlite3\n\ndef totals_by_region(conn):\n    rows = conn.execute(\n        'SELECT region, amount FROM sales ORDER BY region'\n    ).fetchall()\n    return {region: amount for region, amount in rows}"),
    ],
)

write_practice(
    M8, "m8-params-practice",
    "Injection-Proof Drills",
    "Every query parameterized; identifiers whitelisted.",
    "Luyện Chống Injection",
    "Mọi truy vấn đều tham số hóa; định danh qua whitelist.",
    L8B, 30, "intermediate",
    [
        challenge(
            "pi8-param-lookup", "Safe Lookup",
            "Implement safe_lookup(conn, name) returning rows from users WHERE name = ?. It MUST survive the injection attempt in the test (the classic quote trick must be treated as a literal name).",
            "import sqlite3\n\ndef safe_lookup(conn, name):\n    pass\n",
            [
                ("finds exact matches",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE users (name TEXT)')\nconn.execute(\"INSERT INTO users VALUES ('An')\")\nassert safe_lookup(conn, 'An') == [('An',)]",
                 "Parameterized WHERE with the ? placeholder."),
                ("injection attempt is inert",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE users (name TEXT)')\nconn.execute(\"INSERT INTO users VALUES ('An')\")\nrows = safe_lookup(conn, \"' OR '1'='1\")\nassert rows == []",
                 "A parameterized query treats the payload as a literal name — zero rows."),
            ],
            level="guided",
        ),
        challenge(
            "pi8-param-sorted", "Whitelist the Sort",
            "Implement sorted_users(conn, sort) where sort is 'name' or 'id' — the ONLY two allowed columns. Map through a whitelist and raise ValueError for anything else. Return list of (id, name).",
            "import sqlite3\n\ndef sorted_users(conn, sort):\n    pass\n",
            [
                ("valid sorts work",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')\nconn.executemany('INSERT INTO users (name) VALUES (?)', [('B',), ('A',)])\nassert sorted_users(conn, 'name') == [(2, 'A'), (1, 'B')]\nassert sorted_users(conn, 'id') == [(1, 'B'), (2, 'A')]",
                 "ORDER BY the whitelisted column name."),
                ("unknown sort rejected",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')\ntry:\n    sorted_users(conn, 'name; DROP TABLE users')\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
                 "Anything outside {'name', 'id'} raises ValueError before touching SQL."),
            ],
            level="combination",
        ),
    ],
    {
        "pi8-param-lookup": vi_challenge("Tra cứu an toàn", "Viết safe_lookup(conn, name) trả về các dòng từ users WHERE name = ?. Nó PHẢI sống sót qua nỗ lực injection trong test (mẹo dấu nháy kinh điển phải bị coi như một tên nguyên văn).", [("Tìm thấy khớp chính xác", "WHERE tham số hóa với placeholder ?."), ("Nỗ lực injection vô hại", "Truy vấn tham số hóa coi payload là tên nguyên văn — không dòng nào trả về.")]),
        "pi8-param-sorted": vi_challenge("Whitelist cột sắp xếp", "Viết sorted_users(conn, sort) với sort là 'name' hoặc 'id' — chỉ hai cột được phép. Map qua whitelist và raise ValueError với mọi thứ khác. Trả về list các (id, name).", [("Các sort hợp lệ hoạt động", "ORDER BY tên cột đã whitelist."), ("Sort lạ bị từ chối", "Mọi thứ ngoài {'name', 'id'} raise ValueError trước khi chạm vào SQL.")]),
    },
    solutions=[
        ("pi8-param-lookup", "import sqlite3\n\ndef safe_lookup(conn, name):\n    return conn.execute(\n        'SELECT name FROM users WHERE name = ?', (name,)\n    ).fetchall()", "import sqlite3\n\ndef safe_lookup(conn, name):\n    return conn.execute(\n        f'SELECT name FROM users WHERE name = \\'{name}\\''\n    ).fetchall()"),
        ("pi8-param-sorted", "import sqlite3\n\n_ALLOWED = {'name': 'name', 'id': 'id'}\n\ndef sorted_users(conn, sort):\n    column = _ALLOWED.get(sort)\n    if column is None:\n        raise ValueError(f'invalid sort column: {sort}')\n    return conn.execute(\n        f'SELECT id, name FROM users ORDER BY {column}'\n    ).fetchall()", "import sqlite3\n\ndef sorted_users(conn, sort):\n    return conn.execute(\n        f'SELECT id, name FROM users ORDER BY {sort}'\n    ).fetchall()"),
    ],
)

write_practice(
    M8, "m8-tx-practice",
    "Transaction Drills",
    "All-or-nothing transfers and constraint-backed integrity.",
    "Luyện Transaction",
    "Chuyển tiền all-or-nothing và toàn vẹn dựa trên ràng buộc.",
    L8C, 25, "intermediate",
    [
        challenge(
            "pi8-tx-transfer", "Atomic Transfer",
            "Implement transfer(conn, src, dst, amount) moving money between rows of accounts(id INTEGER PRIMARY KEY, balance INTEGER). Raise ValueError if either account is missing or src has insufficient funds (and roll back). On success, commit.",
            "import sqlite3\n\ndef transfer(conn, src, dst, amount):\n    pass\n",
            [
                ("moves the money",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)')\nconn.executemany('INSERT INTO accounts VALUES (?, ?)', [(1, 100), (2, 0)])\ntransfer(conn, 1, 2, 40)\nbals = dict(conn.execute('SELECT id, balance FROM accounts'))\nassert bals == {1: 60, 2: 40}",
                 "Two UPDATEs inside one commit."),
                ("insufficient funds rejected atomically",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)')\nconn.executemany('INSERT INTO accounts VALUES (?, ?)', [(1, 10), (2, 0)])\ntry:\n    transfer(conn, 1, 2, 50)\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed\nbals = dict(conn.execute('SELECT id, balance FROM accounts'))\nassert bals == {1: 10, 2: 0}",
                 "Nothing changes when the transfer is rejected — rollback."),
            ],
            level="guided",
        ),
        challenge(
            "pi8-tx-unique", "Unique Means Unique",
            "Implement add_user(conn, email) inserting into users(id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE). A duplicate email must raise ValueError('duplicate email') — translate the sqlite3.IntegrityError (module 5 chaining!).",
            "import sqlite3\n\ndef add_user(conn, email):\n    pass\n",
            [
                ("first insert succeeds",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE)')\nassert add_user(conn, 'a@x.io') == 1",
                 "Plain parameterized insert; return lastrowid."),
                ("duplicate translated",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE)')\nadd_user(conn, 'a@x.io')\ntry:\n    add_user(conn, 'a@x.io')\n    failed = False\nexcept ValueError as e:\n    failed = 'duplicate email' in str(e)\nassert failed",
                 "Catch sqlite3.IntegrityError, raise ValueError from it."),
            ],
            level="independent",
        ),
    ],
    {
        "pi8-tx-transfer": vi_challenge("Chuyển tiền nguyên tử", "Viết transfer(conn, src, dst, amount) chuyển tiền giữa các dòng của accounts(id INTEGER PRIMARY KEY, balance INTEGER). Raise ValueError nếu thiếu một trong hai tài khoản hoặc src không đủ tiền (và rollback). Khi thành công, commit.", [("Di chuyển tiền", "Hai UPDATE trong một commit."), ("Thiếu tiền bị từ chối một cách nguyên tử", "Không gì thay đổi khi giao dịch bị từ chối — rollback.")]),
        "pi8-tx-unique": vi_challenge("Unique nghĩa là duy nhất", "Viết add_user(conn, email) chèn vào users(id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE). Email trùng phải raise ValueError('duplicate email') — dịch từ sqlite3.IntegrityError (nối chuỗi kiểu module 5!).", [("Lần chèn đầu thành công", "INSERT tham số hóa thường; trả lastrowid."), ("Trùng lặp được dịch lỗi", "Bắt sqlite3.IntegrityError, raise ValueError từ nó.")]),
    },
    solutions=[
        ("pi8-tx-transfer", "import sqlite3\n\ndef transfer(conn, src, dst, amount):\n    try:\n        src_bal = conn.execute('SELECT balance FROM accounts WHERE id = ?', (src,)).fetchone()\n        dst_row = conn.execute('SELECT 1 FROM accounts WHERE id = ?', (dst,)).fetchone()\n        if src_bal is None or dst_row is None:\n            raise ValueError('account not found')\n        if src_bal[0] < amount:\n            raise ValueError('insufficient funds')\n        conn.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, src))\n        conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, dst))\n        conn.commit()\n    except ValueError:\n        conn.rollback()\n        raise\n    except sqlite3.Error:\n        conn.rollback()\n        raise", "import sqlite3\n\ndef transfer(conn, src, dst, amount):\n    conn.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, src))\n    conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, dst))\n    conn.commit()"),
        ("pi8-tx-unique", "import sqlite3\n\ndef add_user(conn, email):\n    try:\n        cur = conn.execute('INSERT INTO users (email) VALUES (?)', (email,))\n        conn.commit()\n        return cur.lastrowid\n    except sqlite3.IntegrityError as exc:\n        raise ValueError('duplicate email') from exc", "import sqlite3\n\ndef add_user(conn, email):\n    cur = conn.execute('INSERT INTO users (email) VALUES (?)', (email,))\n    conn.commit()\n    return cur.lastrowid"),
    ],
)

write_practice(
    M8, "m8-repo-practice",
    "Repository Drills",
    "Wrap SQL behind a clean class boundary.",
    "Luyện Repository",
    "Bọc SQL sau một ranh giới lớp sạch sẽ.",
    L8D, 30, "intermediate",
    [
        challenge(
            "pi8-repo-tasks", "Task Repository",
            "Implement TaskRepository(conn) with methods: add(title) -> int (insert, return id), get(task_id) -> dict | None ({id, title, done}), complete(task_id) -> bool (mark done, True if a row changed), and all() -> list[dict] ordered by id. All SQL parameterized.",
            "import sqlite3\n\nclass TaskRepository:\n    def __init__(self, conn):\n        pass\n\n    def add(self, title):\n        pass\n\n    def get(self, task_id):\n        pass\n\n    def complete(self, task_id):\n        pass\n\n    def all(self):\n        pass\n",
            [
                ("add and get round-trip",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER DEFAULT 0)')\nconn.row_factory = sqlite3.Row\nrepo = TaskRepository(conn)\ntid = repo.add('write docs')\nassert repo.get(tid) == {'id': tid, 'title': 'write docs', 'done': 0}",
                 "INSERT returning lastrowid; SELECT one row → dict."),
                ("complete flips and reports",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER DEFAULT 0)')\nconn.row_factory = sqlite3.Row\nrepo = TaskRepository(conn)\ntid = repo.add('x')\nassert repo.complete(tid) is True\nassert repo.complete(tid) is False\nassert repo.get(tid)['done'] == 1",
                 "UPDATE ... WHERE id = ?; rowcount tells whether a row changed (already-done → False)."),
                ("all ordered by id",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER DEFAULT 0)')\nconn.row_factory = sqlite3.Row\nrepo = TaskRepository(conn)\nrepo.add('a'); repo.add('b')\nassert [t['title'] for t in repo.all()] == ['a', 'b']",
                 "SELECT ... ORDER BY id, mapped to dicts."),
            ],
            level="combination",
        ),
    ],
    {
        "pi8-repo-tasks": vi_challenge("Task Repository", "Viết TaskRepository(conn) với các method: add(title) -> int (chèn, trả id), get(task_id) -> dict | None ({id, title, done}), complete(task_id) -> bool (đánh dấu done, True nếu có dòng thay đổi), và all() -> list[dict] sắp theo id. Toàn bộ SQL phải tham số hóa.", [("add và get khép vòng", "INSERT trả lastrowid; SELECT một dòng → dict."), ("complete lật cờ và báo kết quả", "UPDATE ... WHERE id = ?; rowcount cho biết có dòng nào đổi không (đã-done → False)."), ("all sắp theo id", "SELECT ... ORDER BY id, map sang các dict.")]),
    },
    solutions=[
        ("pi8-repo-tasks", "import sqlite3\n\nclass TaskRepository:\n    def __init__(self, conn):\n        self._conn = conn\n\n    def add(self, title):\n        cur = self._conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))\n        self._conn.commit()\n        return cur.lastrowid\n\n    def get(self, task_id):\n        row = self._conn.execute(\n            'SELECT id, title, done FROM tasks WHERE id = ?', (task_id,)\n        ).fetchone()\n        return dict(row) if row else None\n\n    def complete(self, task_id):\n        cur = self._conn.execute(\n            'UPDATE tasks SET done = 1 WHERE id = ? AND done = 0', (task_id,)\n        )\n        self._conn.commit()\n        return cur.rowcount == 1\n\n    def all(self):\n        return [\n            dict(r)\n            for r in self._conn.execute('SELECT id, title, done FROM tasks ORDER BY id')\n        ]", "import sqlite3\n\nclass TaskRepository:\n    def __init__(self, conn):\n        self._conn = conn\n\n    def add(self, title):\n        cur = self._conn.execute(f'INSERT INTO tasks (title) VALUES (\\'{title}\\')')\n        self._conn.commit()\n        return cur.lastrowid\n\n    def get(self, task_id):\n        row = self._conn.execute(\n            'SELECT id, title, done FROM tasks WHERE id = ?', (task_id,)\n        ).fetchone()\n        return dict(row) if row else None\n\n    def complete(self, task_id):\n        cur = self._conn.execute(\n            'UPDATE tasks SET done = 1 WHERE id = ? AND done = 0', (task_id,)\n        )\n        self._conn.commit()\n        return cur.rowcount == 1\n\n    def all(self):\n        return [\n            dict(r)\n            for r in self._conn.execute('SELECT id, title, done FROM tasks ORDER BY id')\n        ]"),
    ],
)

# --- module 8 checkpoint ---
write_checkpoint(
    M8, L8E,
    "Checkpoint: Database-Backed Application",
    "Build a repository over a constrained schema — with an injection attempt on the tests.",
    20,
    """
The checkpoint assembles the whole module: schema with constraints,
parameterized repository, translated errors, and a test that actively tries
to inject.

**Working with AI:** ask the mentor to generate *attack inputs* for your
queries — then prove each one is inert.
""",
    "Checkpoint: Ứng dụng có Database",
    "Dựng một repository trên schema có ràng buộc — với một nỗ lực injection ngay trong test.",
    """
Checkpoint ghép cả module: schema có ràng buộc, repository tham số hóa, lỗi
được dịch, và một test chủ động cố inject.

**Làm việc cùng AI:** nhờ mentor sinh *các input tấn công* cho truy vấn của
bạn — rồi chứng minh từng input đều vô hại.
""",
    challenge(
        "pi8-ckpt-notes", "Notes Repository",
        "Implement init_notes(conn) creating notes(id INTEGER PRIMARY KEY, title TEXT NOT NULL UNIQUE, body TEXT NOT NULL) and class NotesRepository(conn) with add(title, body) -> int (translate UNIQUE violation to ValueError 'duplicate title'), search(term) -> list[dict] of notes whose title CONTAINS term (LIKE with parameter-bound pattern; survives the injection test), and delete(note_id) -> bool.",
        "import sqlite3\n\ndef init_notes(conn):\n    pass\n\nclass NotesRepository:\n    def __init__(self, conn):\n        pass\n\n    def add(self, title, body):\n        pass\n\n    def search(self, term):\n        pass\n\n    def delete(self, note_id):\n        pass\n",
        [
            ("add, duplicate translated",
             "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_notes(conn)\nrepo = NotesRepository(conn)\nnid = repo.add('meeting', 'agenda')\ntry:\n    repo.add('meeting', 'again')\n    failed = False\nexcept ValueError as e:\n    failed = 'duplicate title' in str(e)\nassert failed",
             "UNIQUE in schema; IntegrityError → ValueError('duplicate title')."),
            ("search matches substrings",
             "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_notes(conn)\nrepo = NotesRepository(conn)\nrepo.add('team meeting', 'x')\nrepo.add('meetup', 'y')\nfound = repo.search('meet')\nassert {n['title'] for n in found} == {'team meeting', 'meetup'}",
             "LIKE '%' || ? || '%' — the pattern is bound, not formatted."),
            ("injection via search is inert",
             "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_notes(conn)\nrepo = NotesRepository(conn)\nrepo.add('safe', 'b')\nassert repo.search(\"%' OR '1'='1\") == []",
             "Parameter-bound LIKE treats the payload as a literal substring."),
            ("delete reports reality",
             "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_notes(conn)\nrepo = NotesRepository(conn)\nnid = repo.add('gone', 'x')\nassert repo.delete(nid) is True\nassert repo.delete(nid) is False",
             "DELETE ... WHERE id = ?; rowcount decides True/False."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Notes Repository",
        "Viết init_notes(conn) tạo bảng notes(id INTEGER PRIMARY KEY, title TEXT NOT NULL UNIQUE, body TEXT NOT NULL) và class NotesRepository(conn) với add(title, body) -> int (dịch vi phạm UNIQUE thành ValueError 'duplicate title'), search(term) -> list[dict] các note có tiêu đề CHỨA term (LIKE với pattern được gán tham số; sống sót qua test injection), và delete(note_id) -> bool.",
        [
            ("add, trùng lặp được dịch", "UNIQUE trong schema; IntegrityError → ValueError('duplicate title')."),
            ("search khớp chuỗi con", "LIKE '%' || ? || '%' — pattern được gán tham số, không phải định dạng."),
            ("Injection qua search vô hại", "LIKE gán tham số coi payload là chuỗi con nguyên văn."),
            ("delete báo cáo sự thật", "DELETE ... WHERE id = ?; rowcount quyết định True/False."),
        ],
    ),
    solution="import sqlite3\n\ndef init_notes(conn):\n    conn.execute('''CREATE TABLE notes (\n        id INTEGER PRIMARY KEY,\n        title TEXT NOT NULL UNIQUE,\n        body TEXT NOT NULL\n    )''')\n    conn.commit()\n\nclass NotesRepository:\n    def __init__(self, conn):\n        self._conn = conn\n\n    def add(self, title, body):\n        try:\n            cur = self._conn.execute(\n                'INSERT INTO notes (title, body) VALUES (?, ?)', (title, body)\n            )\n            self._conn.commit()\n            return cur.lastrowid\n        except sqlite3.IntegrityError as exc:\n            raise ValueError('duplicate title') from exc\n\n    def search(self, term):\n        rows = self._conn.execute(\n            \"SELECT id, title, body FROM notes WHERE title LIKE '%' || ? || '%'\",\n            (term,),\n        ).fetchall()\n        return [dict(r) for r in rows]\n\n    def delete(self, note_id):\n        cur = self._conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))\n        self._conn.commit()\n        return cur.rowcount == 1",
    wrong="import sqlite3\n\ndef init_notes(conn):\n    conn.execute('''CREATE TABLE notes (\n        id INTEGER PRIMARY KEY,\n        title TEXT NOT NULL,\n        body TEXT NOT NULL\n    )''')\n    conn.commit()\n\nclass NotesRepository:\n    def __init__(self, conn):\n        self._conn = conn\n\n    def add(self, title, body):\n        try:\n            cur = self._conn.execute(\n                'INSERT INTO notes (title, body) VALUES (?, ?)', (title, body)\n            )\n            self._conn.commit()\n            return cur.lastrowid\n        except sqlite3.IntegrityError as exc:\n            raise ValueError('duplicate title') from exc\n\n    def search(self, term):\n        rows = self._conn.execute(\n            f\"SELECT id, title, body FROM notes WHERE title LIKE '%{term}%'\",\n        ).fetchall()\n        return [dict(r) for r in rows]\n\n    def delete(self, note_id):\n        cur = self._conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))\n        self._conn.commit()\n        return cur.rowcount == 1",
)

print("module 8 done")
