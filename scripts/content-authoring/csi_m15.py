#!/usr/bin/env python3
"""C# — Intermediate — Module 15: csi-data.

Data access fundamentals without a database server: the contracts SQL shape
(connection/command/reader/transaction), parameterized queries as the
injection defense, mapping rows to objects, and the repository pattern.
Graded with an in-memory store that mirrors ADO.NET's object model.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-data"

DB_PRELUDE = CS_PRELUDE + (
    "\n"
    "// Provided infrastructure — do not modify. In-memory relational-ish\n"
    "// store mirroring the ADO.NET object model (no server, deterministic).\n"
    "public sealed class CjDb\n"
    "{\n"
    "    public sealed class CjParameter\n"
    "    {\n"
    "        public string Name { get; }\n"
    "        public object? Value { get; }\n"
    "        public CjParameter(string name, object? value) { Name = name; Value = value; }\n"
    "    }\n"
    "\n"
    "    public sealed class CjCommand\n"
    "    {\n"
    "        public string Sql { get; set; } = \"\";\n"
    "        public System.Collections.Generic.List<CjParameter> Parameters { get; } = new();\n"
    "        public CjCommand(string sql) { Sql = sql; }\n"
    "        public void AddParameter(string name, object? value) => Parameters.Add(new CjParameter(name, value));\n"
    "    }\n"
    "\n"
    "    public System.Collections.Generic.List<System.Collections.Generic.Dictionary<string, object?>> Users { get; } = new();\n"
    "    public System.Collections.Generic.List<string> ExecutedSql { get; } = new();\n"
    "    public int PendingTransactions;\n"
    "    // Test hook: fail the Nth insert (1-based; 0 = never), simulating a\n"
    "    // downstream constraint failure. Like a real engine, the failure\n"
    "    // ABORTS any open transaction: staged rows discarded.\n"
    "    public int FailOnInsertNumber;\n"
    "    private int insertCount;\n"
    "    private readonly System.Collections.Generic.List<string> staged = new();\n"
    "    // Rows inserted inside an open transaction: invisible until commit,\n"
    "    // and lost entirely if the transaction is never committed.\n"
    "    public int StagedCount => staged.Count;\n"
    "\n"
    "    public CjCommand CreateCommand(string sql) => new CjCommand(sql);\n"
    "\n"
    "    public void BeginTransaction() => PendingTransactions++;\n"
    "    public void CommitTransaction()\n"
    "    {\n"
    "        if (PendingTransactions <= 0) return;\n"
    "        PendingTransactions--;\n"
    "        if (PendingTransactions == 0)\n"
    "        {\n"
    "            // Commit: staged rows become visible.\n"
    "            foreach (var name in staged)\n"
    "                Users.Add(new System.Collections.Generic.Dictionary<string, object?> { [\"name\"] = name });\n"
    "            staged.Clear();\n"
    "        }\n"
    "    }\n"
    "\n"
    "    // Runs a command. Only SELECT * FROM <table> (optionally WHERE name = @p)\n"
    "    // and INSERT INTO <table> (name) VALUES (@p) are supported.\n"
    "    public System.Collections.Generic.List<System.Collections.Generic.Dictionary<string, object?>> ExecuteReader(CjCommand cmd)\n"
    "    {\n"
    "        ExecutedSql.Add(cmd.Sql);\n"
    "        var sql = cmd.Sql.Trim();\n"
    "        if (sql.StartsWith(\"SELECT\", System.StringComparison.OrdinalIgnoreCase))\n"
    "        {\n"
    "            string table = ExtractTable(sql);\n"
    "            var rows = new System.Collections.Generic.List<System.Collections.Generic.Dictionary<string, object?>>();\n"
    "            if (sql.Contains(\"WHERE\", System.StringComparison.OrdinalIgnoreCase))\n"
    "            {\n"
    "                // Parameterized WHERE: only matches with a bound parameter are honored.\n"
    "                if (cmd.Parameters.Count == 1 && cmd.Parameters[0].Name == \"@name\")\n"
    "                {\n"
    "                    foreach (var row in Users)\n"
    "                        if (Equals(row[\"name\"], cmd.Parameters[0].Value)) rows.Add(row);\n"
    "                }\n"
    "                else\n"
    "                {\n"
    "                    // Non-parameterized WHERE: rejected by the engine (like real\n"
    "                    // engines reject unsafe literal comparison here).\n"
    "                    throw new System.InvalidOperationException(\"unsafe query: unparameterized WHERE\");\n"
    "                }\n"
    "                return rows;\n"
    "            }\n"
    "            foreach (var row in Users) rows.Add(new System.Collections.Generic.Dictionary<string, object?>(row));\n"
    "            return rows;\n"
    "        }\n"
    "        throw new System.InvalidOperationException(\"ExecuteReader supports SELECT only\");\n"
    "    }\n"
    "\n"
    "    public int ExecuteNonQuery(CjCommand cmd)\n"
    "    {\n"
    "        ExecutedSql.Add(cmd.Sql);\n"
    "        var sql = cmd.Sql.Trim();\n"
    "        if (sql.StartsWith(\"INSERT\", System.StringComparison.OrdinalIgnoreCase))\n"
    "        {\n"
    "            if (cmd.Parameters.Count != 1 || cmd.Parameters[0].Name != \"@name\")\n"
    "                throw new System.InvalidOperationException(\"INSERT requires @name parameter\");\n"
    "            insertCount++;\n"
    "            if (FailOnInsertNumber > 0 && insertCount >= FailOnInsertNumber)\n"
    "            {\n"
    "                FailOnInsertNumber = 0;\n"
    "                staged.Clear();\n"
    "                PendingTransactions = 0;   // engine aborts the open transaction\n"
    "                throw new System.InvalidOperationException(\"constraint violation: insert failed\");\n"
    "            }\n"
    "            if (PendingTransactions == 0)\n"
    "            {\n"
    "                Users.Add(new System.Collections.Generic.Dictionary<string, object?> { [\"name\"] = cmd.Parameters[0].Value });\n"
    "            }\n"
    "            else\n"
    "            {\n"
    "                staged.Add((string)cmd.Parameters[0].Value!);\n"
    "            }\n"
    "            return 1;\n"
    "        }\n"
    "        throw new System.InvalidOperationException(\"ExecuteNonQuery supports INSERT only\");\n"
    "    }\n"
    "\n"
    "    private static string ExtractTable(string sql)\n"
    "    {\n"
    "        var parts = sql.Split(' ', System.StringSplitOptions.RemoveEmptyEntries);\n"
    "        int idx = System.Array.FindIndex(parts, p => p.Equals(\"FROM\", System.StringComparison.OrdinalIgnoreCase));\n"
    "        return idx >= 0 && idx + 1 < parts.Length ? parts[idx + 1] : \"?\";\n"
    "    }\n"
    "}\n"
)

write_module(
    M,
    "Data Access Fundamentals",
    "Connections, commands, parameters, transactions — the relational vocabulary every data layer stands on.",
    "Nền tảng Truy cập Dữ liệu",
    "Connection, command, tham số, transaction — từ vựng quan hệ mà mọi tầng dữ liệu dựa vào.",
    ["relational-basics", "repositories", "csi-checkpoint-m15"],
    ["csi-p15-data"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "relational-basics",
    "Connections, Commands, and Parameterized Queries",
    "The ADO.NET object model, why parameters are non-negotiable, and transactions as all-or-nothing units.",
    18,
    r"""
## The relational object model

Every data access stack shares this shape (ADO.NET, EF Core underneath, and
every other runtime):

- **Connection** — the session to the database. Open late, close early; pool
  them (like HttpClient).
- **Command** — SQL text plus parameters. `ExecuteReader` for queries,
  `ExecuteNonQuery` for mutations.
- **Reader** — a forward-only cursor over result rows; each row maps to
  your object (reading columns by name, converting types).

```csharp
var cmd = db.CreateCommand("SELECT * FROM users WHERE name = @name");
cmd.AddParameter("@name", userName);
var rows = db.ExecuteReader(cmd);
foreach (var row in rows)
    Console.WriteLine(row["name"]);
```

## SQL injection: the one rule that saves you

Never build SQL by concatenating values:

```csharp
// FATAL: a name like '; DROP TABLE users; -- becomes part of the program
var sql = "SELECT * FROM users WHERE name = '" + input + "'";
```

Parameters keep DATA as data — the engine sends the query text and the
values separately, so a value can never change the query's meaning. This is
structural, not optional; string-built queries with user input are a
vulnerability even when you "know" the input is clean.

## Transactions: all or nothing

Multiple related writes must succeed or fail together — a transfer that
debits but never credits is a corrupted ledger. `Begin` marks the unit,
`Commit` makes it permanent, and any failure (or abort) rolls back
everything since Begin.

## Check your understanding

- Why can't an attacker inject through a parameter? (Values travel separately from the SQL text — they're never parsed as code.)
- When does a transaction help? (Multiple related writes that must be atomic.)
""",
    "Connection, Command, và Truy vấn Tham số hóa",
    "Mô hình đối tượng ADO.NET, vì sao tham số là bất di bất dịch, và transaction là đơn vị tất-cả-hoặc-không.",
    r"""
## Mô hình đối tượng quan hệ

Mọi stack truy cập dữ liệu đều chia sẻ hình dạng này (ADO.NET, EF Core ở
dưới, và mọi runtime khác):

- **Connection** — phiên kết nối tới database. Mở muộn, đóng sớm; hãy pool
  (như HttpClient).
- **Command** — văn bản SQL kèm tham số. `ExecuteReader` cho truy vấn,
  `ExecuteNonQuery` cho biến đổi.
- **Reader** — con trỏ chỉ-đi-tới trên các hàng kết quả; mỗi hàng map thành
  đối tượng của bạn (đọc cột theo tên, chuyển kiểu).

```csharp
var cmd = db.CreateCommand("SELECT * FROM users WHERE name = @name");
cmd.AddParameter("@name", userName);
var rows = db.ExecuteReader(cmd);
foreach (var row in rows)
    Console.WriteLine(row["name"]);
```

## SQL injection: quy tắc duy nhất cứu bạn

Không bao giờ ghép SQL bằng cách nối giá trị:

```csharp
// CHẾT NGƯỜI: một name như '; DROP TABLE users; -- trở thành một phần của chương trình
var sql = "SELECT * FROM users WHERE name = '" + input + "'";
```

Tham số giữ cho DỮ LIỆU là dữ liệu — engine gửi văn bản query và các giá trị
tách biệt, nên giá trị không thể thay đổi ý nghĩa của query. Điều này mang
tính cấu trúc, không tùy chọn; query nối chuỗi với đầu vào người dùng là lỗ
hổng kể cả khi bạn "biết" đầu vào sạch.

## Transaction: tất cả hoặc không có gì

Nhiều lần ghi liên quan phải thành công hay thất bại cùng nhau — một lệnh
chuyển tiền ghi nợ nhưng không ghi có là sổ cái hỏng. `Begin` đánh dấu đơn
vị, `Commit` làm vĩnh viễn, và bất kỳ thất bại (hoặc hủy) nào sẽ hoàn tác
mọi thứ từ Begin.

## Kiểm tra hiểu biết

- Vì sao kẻ tấn công không thể inject qua tham số? (Giá trị đi tách biệt văn bản SQL — không bao giờ bị parse thành code.)
- Khi nào transaction có ích? (Nhiều lần ghi liên quan cần nguyên tử.)
""",
    r"""
## Mô hình đối tượng quan hệ

Mọi stack truy cập dữ liệu đều chia sẻ hình dạng này (ADO.NET, EF Core ở
dưới, và mọi runtime khác):

- **Connection** — phiên kết nối tới database. Mở muộn, đóng sớm; hãy pool
  (như HttpClient).
- **Command** — văn bản SQL kèm tham số. `ExecuteReader` cho truy vấn,
  `ExecuteNonQuery` cho biến đổi.
- **Reader** — con trỏ chỉ-đi-tới trên các hàng kết quả; mỗi hàng map thành
  đối tượng của bạn (đọc cột theo tên, chuyển kiểu).

```csharp
var cmd = db.CreateCommand("SELECT * FROM users WHERE name = @name");
cmd.AddParameter("@name", userName);
var rows = db.ExecuteReader(cmd);
foreach (var row in rows)
    Console.WriteLine(row["name"]);
```

## SQL injection: quy tắc duy nhất cứu bạn

Không bao giờ ghép SQL bằng cách nối giá trị:

```csharp
// CHẾT NGƯỜI: một name như '; DROP TABLE users; -- trở thành một phần của chương trình
var sql = "SELECT * FROM users WHERE name = '" + input + "'";
```

Tham số giữ cho DỮ LIỆU là dữ liệu — engine gửi văn bản query và các giá trị
tách biệt, nên giá trị không thể thay đổi ý nghĩa của query. Điều này mang
tính cấu trúc, không tùy chọn; query nối chuỗi với đầu vào người dùng là lỗ
hổng kể cả khi bạn "biết" đầu vào sạch.

## Transaction: tất cả hoặc không có gì

Nhiều lần ghi liên quan phải thành công hay thất bại cùng nhau — một lệnh
chuyển tiền ghi nợ nhưng không ghi có là sổ cái hỏng. `Begin` đánh dấu đơn
vị, `Commit` làm vĩnh viễn, và bất kỳ thất bại (hoặc hủy) nào sẽ hoàn tác
mọi thứ từ Begin.

## Kiểm tra hiểu biết

- Vì sao kẻ tấn công không thể inject qua tham số? (Giá trị đi tách biệt văn bản SQL — không bao giờ bị parse thành code.)
- Khi nào transaction có ích? (Nhiều lần ghi liên quan cần nguyên tử.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "repositories",
    "Mapping Rows and the Repository Pattern",
    "Turning row dictionaries into domain objects, and hiding data access behind an interface.",
    16,
    r"""
## Row mapping: the boring glue

Readers hand you rows; the domain wants objects. The mapping function is
where nulls become defaults, column names are spelled once, and types are
converted:

```csharp
private static User Map(System.Collections.Generic.Dictionary<string, object?> row)
    => new User(
        Name: (string)row["name"]!,
        Balance: Convert.ToDecimal(row["balance"] ?? 0m));
```

Keep mapping in ONE place — a mapper method or the repository itself — so a
schema change touches one file.

## The repository: a collection-shaped façade

A repository exposes the domain's idea of persistence — Add, Get, Find —
while hiding SQL inside:

```csharp
public interface IUserRepository
{
    void Add(User user);
    User? FindByName(string name);
    System.Collections.Generic.IReadOnlyList<User> All();
}

public sealed class SqlUserRepository : IUserRepository
{
    private readonly CjDb _db;
    public SqlUserRepository(CjDb db) => _db = db;   // injected (Module 11)
    // ... every SQL string lives here, parameterized, nowhere else ...
}
```

Benefits: business code reads like the domain; a different backend is an
implementation swap; and testing needs only a fake repository (no database
at all).

## What belongs where

- SQL strings: repository implementations only.
- Domain logic: services — never inside repositories.
- Mapping: between the two, in the repository.
- A repository that returns IQueryable invites leaks; keep the boundary
  concrete (lists, single objects).

## Check your understanding

- Where does a new WHERE clause go? (The one repository implementation that owns that table's SQL.)
- Why does the service take IUserRepository, not SqlUserRepository? (Depend on the abstraction; swap implementations; test with fakes.)
""",
    "Map Hàng và Repository Pattern",
    "Biến hàng (dạng dictionary) thành đối tượng nghiệp vụ, và giấu truy cập dữ liệu sau interface.",
    r"""
## Row mapping: keo dán nhàm chán

Reader đưa bạn các hàng; nghiệp vụ muốn đối tượng. Hàm mapping là nơi null
trở thành mặc định, tên cột được viết đúng một lần, và các kiểu được chuyển:

```csharp
private static User Map(System.Collections.Generic.Dictionary<string, object?> row)
    => new User(
        Name: (string)row["name"]!,
        Balance: Convert.ToDecimal(row["balance"] ?? 0m));
```

Giữ mapping ở MỘT nơi — một hàm mapper hoặc chính repository — để thay đổi
schema chỉ chạm một file.

## Repository: mặt tiền hình tập hợp

Repository phơi bày quan điểm của nghiệp vụ về lưu trữ — Add, Get, Find —
trong khi giấu SQL bên trong:

```csharp
public interface IUserRepository
{
    void Add(User user);
    User? FindByName(string name);
    System.Collections.Generic.IReadOnlyList<User> All();
}

public sealed class SqlUserRepository : IUserRepository
{
    private readonly CjDb _db;
    public SqlUserRepository(CjDb db) => _db = db;   // injected (Module 11)
    // ... mọi chuỗi SQL sống ở đây, đã tham số hóa, không nơi nào khác ...
}
```

Lợi ích: code nghiệp vụ đọc như nghiệp vụ; backend khác chỉ là thay đổi
hiện thực; và test chỉ cần fake repository (không cần database).

## Cái gì nằm ở đâu

- Chuỗi SQL: chỉ trong các hiện thực repository.
- Logic nghiệp vụ: các service — không bao giờ trong repository.
- Mapping: giữa hai tầng, trong repository.
- Repository trả IQueryable mời rò rỉ ranh giới; giữ biên giới cụ thể
  (danh sách, đối tượng đơn).

## Kiểm tra hiểu biết

- Mệnh đề WHERE mới nằm ở đâu? (Trong đúng một hiện thực repository sở hữu SQL của bảng đó.)
- Vì sao service nhận IUserRepository chứ không phải SqlUserRepository? (Phụ thuộc abstraction; hoán đổi hiện thực; test bằng fake.)
""",
    r"""
## Row mapping: keo dán nhàm chán

Reader đưa bạn các hàng; nghiệp vụ muốn đối tượng. Hàm mapping là nơi null
trở thành mặc định, tên cột được viết đúng một lần, và các kiểu được chuyển:

```csharp
private static User Map(System.Collections.Generic.Dictionary<string, object?> row)
    => new User(
        Name: (string)row["name"]!,
        Balance: Convert.ToDecimal(row["balance"] ?? 0m));
```

Giữ mapping ở MỘT nơi — một hàm mapper hoặc chính repository — để thay đổi
schema chỉ chạm một file.

## Repository: mặt tiền hình tập hợp

Repository phơi bày quan điểm của nghiệp vụ về lưu trữ — Add, Get, Find —
trong khi giấu SQL bên trong:

```csharp
public interface IUserRepository
{
    void Add(User user);
    User? FindByName(string name);
    System.Collections.Generic.IReadOnlyList<User> All();
}

public sealed class SqlUserRepository : IUserRepository
{
    private readonly CjDb _db;
    public SqlUserRepository(CjDb db) => _db = db;   // injected (Module 11)
    // ... mọi chuỗi SQL sống ở đây, đã tham số hóa, không nơi nào khác ...
}
```

Lợi ích: code nghiệp vụ đọc như nghiệp vụ; backend khác chỉ là thay đổi
hiện thực; và test chỉ cần fake repository (không cần database).

## Cái gì nằm ở đâu

- Chuỗi SQL: chỉ trong các hiện thực repository.
- Logic nghiệp vụ: các service — không bao giờ trong repository.
- Mapping: giữa hai tầng, trong repository.
- Repository trả IQueryable mời rò rỉ ranh giới; giữ biên giới cụ thể
  (danh sách, đối tượng đơn).

## Kiểm tra hiểu biết

- Mệnh đề WHERE mới nằm ở đâu? (Trong đúng một hiện thực repository sở hữu SQL của bảng đó.)
- Vì sao service nhận IUserRepository chứ không phải SqlUserRepository? (Phụ thuộc abstraction; hoán đổi hiện thực; test bằng fake.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p15-data",
    "Data Practice: Parameters, Mapping, Transactions",
    "Query through parameters only, map rows to objects, and wrap multi-step writes in a transaction.",
    "Luyện Dữ liệu: Tham số, Mapping, Transaction",
    "Truy vấn chỉ qua tham số, map hàng thành đối tượng, và bọc các lần ghi nhiều bước trong transaction.",
    "repositories",
    30,
    "intermediate",
    [
        challenge(
            "csi-p15-parameterized-lookup",
            "The Only Safe Lookup",
            """Implement FindUser: SELECT * FROM users WHERE name = @name with the caller's string bound as a parameter — the engine REJECTS unparameterized WHERE clauses (like real engines punish injection). Returns "user:<name>" or "notfound".

```csharp
static string FindUser(CjDb db, string name);
```""",
            DB_PRELUDE,
            [
                (
                    "parameterized lookup works",
                    r"""
var db = new CjDb();
var insert = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");
insert.AddParameter("@name", "ada");
db.ExecuteNonQuery(insert);
Cj.Eq(Solution.FindUser(db, "ada"), "user:ada", "found");
Cj.Eq(Solution.FindUser(db, "grace"), "notfound", "missing");
""",
                    "CreateCommand with @name in the text; AddParameter(\"@name\", name); ExecuteReader.",
                ),
                (
                    "injection attempt stays data",
                    r"""
var db = new CjDb();
var insert = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");
insert.AddParameter("@name", "'; DROP TABLE users; --");
db.ExecuteNonQuery(insert);
Cj.Eq(Solution.FindUser(db, "'; DROP TABLE users; --"), "user:'; DROP TABLE users; --", "malicious string is just a name");
""",
                    "The parameter binds the whole string as a value — the engine never parses it as SQL.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p15-row-mapping",
            "Map Rows to Objects",
            """Implement LoadUsers: read all users and map each row (columns "name" string, "age" int, "balance" decimal) into User records, sorted by name. Rows may contain null age — map null to 0.

```csharp
public sealed record User(string Name, int Age, decimal Balance);
static System.Collections.Generic.List<Solution.User> LoadUsers(CjDb db);
```""",
            DB_PRELUDE,
            [
                (
                    "mapping with null defaulting",
                    r"""
var db = new CjDb();
var u1 = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");
u1.AddParameter("@name", "cody");
var u2 = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");
u2.AddParameter("@name", "ada");
db.ExecuteNonQuery(u1);
db.ExecuteNonQuery(u2);
var users = Solution.LoadUsers(db);
Cj.Eq(users.Count, 2, "all users loaded");
Cj.Eq(users[0].Name, "ada", "sorted by name");
""",
                    "Read rows, Map(row) for each, sort by Name.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p15-transaction-debug",
            "Debug: The Half-Written Transfer",
            """Transfer inserts a debit row and a credit row. A downstream constraint failure (set CjDb.FailOnInsertNumber = 2 in the test) means the SECOND insert can fail — and the buggy version leaves the debit visible: a half-written ledger. Fix: wrap BOTH inserts in a transaction (BeginTransaction ... CommitTransaction) so the write is all-or-nothing: on failure, NOTHING is committed; on success, both rows land.

```csharp
static void Transfer(CjDb db, string from, string to);
// CjDb: BeginTransaction(), CommitTransaction(), PendingTransactions property
```""",
            DB_PRELUDE,
            [
                (
                    "both inserts are one unit",
                    r"""
var db = new CjDb();
Solution.Transfer(db, "ann", "bob");
Cj.Eq(db.Users.Count, 2, "happy path: both rows committed");
Cj.Eq(db.PendingTransactions, 0, "no leaked transaction");

var half = new CjDb();
half.FailOnInsertNumber = 2;   // the credit insert fails
try { Solution.Transfer(half, "ann", "bob"); Cj.True(false, "failure must propagate"); }
catch (System.InvalidOperationException) { Cj.True(true, "failure propagates"); }
Cj.Eq(half.Users.Count, 0, "failed transfer commits NOTHING (no debit row)");
Cj.Eq(half.PendingTransactions, 0, "no leaked transaction after failure");
""",
                    "BeginTransaction before the first insert; commit after the last. When an insert throws inside the transaction, the staged rows vanish — let the exception propagate.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p15-parameterized-lookup": vi_challenge(
            "Tra cứu an toàn duy nhất",
            "Hiện thực FindUser: SELECT * FROM users WHERE name = @name với chuỗi của caller bó thành tham số — engine TỪ CHỐI mệnh đề WHERE không tham số (như engine thật trừng phạt injection). Trả \"user:<name>\" hoặc \"notfound\".",
            [
                ("parameterized lookup works", "CreateCommand với @name trong văn bản; AddParameter(\"@name\", name); ExecuteReader."),
                ("injection attempt stays data", "Tham số bó toàn bộ chuỗi thành giá trị — engine không bao giờ parse nó thành SQL."),
            ],
        ),
        "csi-p15-row-mapping": vi_challenge(
            "Map hàng thành đối tượng",
            "Hiện thực LoadUsers: đọc tất cả users và map mỗi hàng (cột \"name\" string, \"age\" int, \"balance\" decimal) thành record User, xếp theo name. Hàng có thể chứa age null — map null thành 0.",
            [
                ("mapping with null defaulting", "Đọc hàng, Map(row) cho từng cái, xếp theo Name."),
            ],
        ),
        "csi-p15-transaction-debug": vi_challenge(
            "Debug: Lệnh chuyển tiền ghi dở dang",
            "Transfer chèn một hàng ghi nợ và một hàng ghi có; khi insert ghi có ném lỗi, ghi nợ vẫn được commit — sổ cái hỏng. Sửa: bọc CẢ HAI insert trong transaction (BeginTransaction ... CommitTransaction) để chúng tất-cả-hoặc-không.",
            [
                ("both inserts are one unit", "BeginTransaction trước insert đầu; CommitTransaction sau insert cuối."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p15-parameterized-lookup",
            'public class Solution\n{\n    public static string FindUser(CjDb db, string name)\n    {\n        var cmd = db.CreateCommand("SELECT * FROM users WHERE name = @name");\n        cmd.AddParameter("@name", name);\n        var rows = db.ExecuteReader(cmd);\n        return rows.Count > 0 ? "user:" + rows[0]["name"] : "notfound";\n    }\n}\n',
            'public class Solution\n{\n    public static string FindUser(CjDb db, string name)\n    {\n        // near-miss: string-concatenated SQL — the engine rejects the\n        // unparameterized WHERE (and in a real engine, this is the injection hole)\n        var cmd = db.CreateCommand("SELECT * FROM users WHERE name = \'" + name + "\'");\n        var rows = db.ExecuteReader(cmd);\n        return rows.Count > 0 ? "user:" + rows[0]["name"] : "notfound";\n    }\n}\n',
        ),
        (
            "csi-p15-row-mapping",
            'public class Solution\n{\n    public sealed record User(string Name, int Age, decimal Balance);\n\n    private static User Map(System.Collections.Generic.Dictionary<string, object?> row)\n    {\n        return new User(\n            Name: (string)row["name"]!,\n            Age: row.ContainsKey("age") && row["age"] is not null ? Convert.ToInt32(row["age"]) : 0,\n            Balance: row.ContainsKey("balance") && row["balance"] is not null ? Convert.ToDecimal(row["balance"]) : 0m);\n    }\n\n    public static System.Collections.Generic.List<User> LoadUsers(CjDb db)\n    {\n        var cmd = db.CreateCommand("SELECT * FROM users");\n        var rows = db.ExecuteReader(cmd);\n        var users = new System.Collections.Generic.List<User>();\n        foreach (var row in rows) users.Add(Map(row));\n        users.Sort((a, b) => string.CompareOrdinal(a.Name, b.Name));\n        return users;\n    }\n}\n',
            'public class Solution\n{\n    public sealed record User(string Name, int Age, decimal Balance);\n\n    public static System.Collections.Generic.List<User> LoadUsers(CjDb db)\n    {\n        var cmd = db.CreateCommand("SELECT * FROM users");\n        var rows = db.ExecuteReader(cmd);\n        var users = new System.Collections.Generic.List<User>();\n        foreach (var row in rows)\n        {\n            // near-miss: no mapping layer — the raw row dictionary leaks into\n            // the domain and the null-age rule is nowhere\n            users.Add(new User((string)row["name"]!, -1, 0m));\n        }\n        return users;\n    }\n}\n',
        ),
        (
            "csi-p15-transaction-debug",
            'public class Solution\n{\n    public static void Transfer(CjDb db, string from, string to)\n    {\n        db.BeginTransaction();\n        var debit = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");\n        debit.AddParameter("@name", "-" + from);\n        db.ExecuteNonQuery(debit);\n\n        var credit = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");\n        credit.AddParameter("@name", "+" + to);\n        db.ExecuteNonQuery(credit);\n\n        db.CommitTransaction();\n    }\n}\n',
            'public class Solution\n{\n    public static void Transfer(CjDb db, string from, string to)\n    {\n        // near-miss: no transaction — if the credit insert fails, the debit\n        // is already committed: a half-written transfer\n        var debit = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");\n        debit.AddParameter("@name", "-" + from);\n        db.ExecuteNonQuery(debit);\n\n        var credit = db.CreateCommand("INSERT INTO users (name) VALUES (@name)");\n        credit.AddParameter("@name", "+" + to);\n        db.ExecuteNonQuery(credit);\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m15",
    "Checkpoint — The User Directory with a Repository",
    "Compose the layer: parameterized repository over the engine, transactional registration, fake-backed service tests.",
    25,
    r"""
## The gate (mini-build)

A user directory service over the in-memory engine:

1. `IUserRepository` — `Register(string name)`, `FindByName(string name)`
   (returns `User?`), `Count()`.
2. `SqlUserRepository(CjDb db) : IUserRepository` — every SQL parameterized;
   `Register` wraps a uniqueness pre-check and the insert in ONE transaction
   (begin → check → insert → commit) and returns "ok" or "duplicate".
3. `Map(row)` → `User(Name, Balance)` — balance defaults to 0 when the
   column is null.
4. `UserService(IUserRepository)` — `Invite(string name)` returns
   "invited:<name>" on success, "exists:<name>" when the name is taken
   (Module 11: the service knows only the interface).

User: `record User(string Name, decimal Balance)`.
""",
    "Checkpoint — Danh bạ người dùng với Repository",
    "Ghép tầng: repository tham số hóa trên engine, đăng ký nguyên tử, test service bằng fake.",
    r"""
## Cổng kiểm tra (mini-build)

Dịch vụ danh bạ người dùng trên engine trong bộ nhớ:

1. `IUserRepository` — `Register(string name)`, `FindByName(string name)`
   (trả `User?`), `Count()`.
2. `SqlUserRepository(CjDb db) : IUserRepository` — mọi SQL tham số hóa;
   `Register` bọc kiểm tra-trước-tính-duy-nhất và insert trong MỘT
   transaction (begin → check → insert → commit), trả "ok" hoặc "duplicate".
3. `Map(row)` → `User(Name, Balance)` — balance mặc định 0 khi cột null.
4. `UserService(IUserRepository)` — `Invite(string name)` trả
   "invited:<name>" khi thành công, "exists:<name>" khi tên đã có
   (Module 11: service chỉ biết interface).

User: `record User(string Name, decimal Balance)`.
""",
    challenge(
        "csi-checkpoint-m15-task",
        "Checkpoint: Directory Wired",
        """Implement the directory described in the checkpoint:

```csharp
public sealed record User(string Name, decimal Balance);
public interface IUserRepository
{
    string Register(string name);   // "ok" | "duplicate"
    Solution.User? FindByName(string name);
    int Count();
}
public sealed class SqlUserRepository : IUserRepository { public SqlUserRepository(CjDb db); }
public sealed class UserService
{
    public UserService(IUserRepository repo);
    public string Invite(string name);   // "invited:<name>" | "exists:<name>"
}
```""",
        DB_PRELUDE,
        [
            (
                "register and find through the repository",
                r"""
var db = new CjDb();
var repo = new Solution.SqlUserRepository(db);
Cj.Eq(repo.Register("ada"), "ok", "first registration");
Cj.Eq(repo.Register("ada"), "duplicate", "name taken");
Cj.True(repo.FindByName("ada")!.Name == "ada", "found by name");
Cj.True(repo.FindByName("ghost") is null, "missing -> null");
""",
                    "Register: begin, SELECT for existence, INSERT, commit. Find: parameterized SELECT.",
                ),
                (
                    "service uses only the interface",
                    r"""
var db = new CjDb();
var svc = new Solution.UserService(new Solution.SqlUserRepository(db));
Cj.Eq(svc.Invite("grace"), "invited:grace", "invited");
Cj.Eq(svc.Invite("grace"), "exists:grace", "second time exists");
""",
                    "UserService delegates to IUserRepository; no SQL knowledge in the service.",
                ),
                (
                    "parameters everywhere",
                    r"""
var db = new CjDb();
var repo = new Solution.SqlUserRepository(db);
repo.Register("hacker'; --");
Cj.True(repo.FindByName("hacker'; --") is not null, "weird name stored and found verbatim");
""",
                    "Names with SQL fragments are just values — parameterized end to end.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Danh bạ đã nối",
            "Hiện thực: SqlUserRepository trên CjDb (mọi SQL tham số hóa, Register trong một transaction với kiểm tra duy nhất, trả \"ok\"/\"duplicate\"); Map hàng thành User (balance mặc định 0); UserService chỉ dùng IUserRepository — Invite trả \"invited:<name>\" hoặc \"exists:<name>\".",
            [
                ("register and find through the repository", "Register: begin, SELECT tồn tại, INSERT, commit. Find: SELECT tham số hóa."),
                ("service uses only the interface", "UserService ủy quyền cho IUserRepository; service không biết gì về SQL."),
                ("parameters everywhere", "Tên chứa mảnh SQL chỉ là giá trị — tham số hóa từ đầu đến cuối."),
            ],
        ),
        solution='public class Solution\n{\n    public sealed record User(string Name, decimal Balance);\n\n    public interface IUserRepository\n    {\n        string Register(string name);\n        User? FindByName(string name);\n        int Count();\n    }\n\n    public sealed class SqlUserRepository : IUserRepository\n    {\n        private readonly CjDb _db;\n\n        public SqlUserRepository(CjDb db) => _db = db;\n\n        public string Register(string name)\n        {\n            _db.BeginTransaction();\n            try\n            {\n                var check = _db.CreateCommand("SELECT * FROM users WHERE name = @name");\n                check.AddParameter("@name", name);\n                if (_db.ExecuteReader(check).Count > 0)\n                {\n                    _db.CommitTransaction();\n                    return "duplicate";\n                }\n\n                var insert = _db.CreateCommand("INSERT INTO users (name) VALUES (@name)");\n                insert.AddParameter("@name", name);\n                _db.ExecuteNonQuery(insert);\n                _db.CommitTransaction();\n                return "ok";\n            }\n            catch\n            {\n                throw;   // engine aborts; nothing half-written survives\n            }\n        }\n\n        public User? FindByName(string name)\n        {\n            var cmd = _db.CreateCommand("SELECT * FROM users WHERE name = @name");\n            cmd.AddParameter("@name", name);\n            var rows = _db.ExecuteReader(cmd);\n            return rows.Count > 0 ? Map(rows[0]) : null;\n        }\n\n        public int Count()\n        {\n            var cmd = _db.CreateCommand("SELECT * FROM users");\n            return _db.ExecuteReader(cmd).Count;\n        }\n\n        private static User Map(System.Collections.Generic.Dictionary<string, object?> row)\n        {\n            return new User(\n                Name: (string)row["name"]!,\n                Balance: row.ContainsKey("balance") && row["balance"] is not null\n                    ? Convert.ToDecimal(row["balance"]) : 0m);\n        }\n    }\n\n    public sealed class UserService\n    {\n        private readonly IUserRepository _repo;\n\n        public UserService(IUserRepository repo) => _repo = repo;\n\n        public string Invite(string name)\n        {\n            return _repo.Register(name) == "ok" ? "invited:" + name : "exists:" + name;\n        }\n    }\n}\n',
        wrong='public class Solution\n{\n    public sealed record User(string Name, decimal Balance);\n\n    public interface IUserRepository\n    {\n        string Register(string name);\n        User? FindByName(string name);\n        int Count();\n    }\n\n    public sealed class SqlUserRepository : IUserRepository\n    {\n        private readonly CjDb _db;\n\n        public SqlUserRepository(CjDb db) => _db = db;\n\n        public string Register(string name)\n        {\n            // near-miss: NO transaction and NO uniqueness check — duplicate\n            // names insert happily and Register always returns "ok"\n            var insert = _db.CreateCommand("INSERT INTO users (name) VALUES (@name)");\n            insert.AddParameter("@name", name);\n            _db.ExecuteNonQuery(insert);\n            return "ok";\n        }\n\n        public User? FindByName(string name)\n        {\n            // near-miss: unparameterized WHERE — the engine throws\n            // "unsafe query" instead of returning a row\n            var cmd = _db.CreateCommand("SELECT * FROM users WHERE name = \'" + name + "\'");\n            var rows = _db.ExecuteReader(cmd);\n            return rows.Count > 0 ? new User((string)rows[0]["name"]!, 0m) : null;\n        }\n\n        public int Count()\n        {\n            var cmd = _db.CreateCommand("SELECT * FROM users");\n            return _db.ExecuteReader(cmd).Count;\n        }\n    }\n\n    public sealed class UserService\n    {\n        private readonly IUserRepository _repo;\n\n        public UserService(IUserRepository repo) => _repo = repo;\n\n        public string Invite(string name)\n        {\n            return _repo.Register(name) == "ok" ? "invited:" + name : "exists:" + name;\n        }\n    }\n}\n',
    )
print("module 15 authored")
