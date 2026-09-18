"""Module 22 — Advanced data access (csa-m22)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-data-access",
        "Advanced Data Access",
        "Connection lifecycle, transaction safety, isolation levels, optimistic concurrency, and N+1 — simulated in-box, deterministically.",
    )

    csa.register_lesson(
        MID, "csa-m22-connection-lifecycle", "Connection lifecycle and pooling",
        "Open late, close early: why connections are pooled, what pool exhaustion looks like, and the leak patterns that cause it.",
        15, "advanced", _m22_lifecycle, _m22_lifecycle_vi,
    )
    csa.register_lesson(
        MID, "csa-m22-transactions", "Transactions and isolation levels",
        "ACID in practice: what each isolation level actually prevents, and the anomalies it leaves on the table.",
        16, "advanced", _m22_transactions, _m22_transactions_vi,
    )
    csa.register_lesson(
        MID, "csa-m22-concurrency", "Optimistic vs pessimistic concurrency",
        "Version columns, conflict windows, and retry loops — why most web apps should be optimistic and when they must not be.",
        15, "advanced", _m22_concurrency, _m22_concurrency_vi,
    )
    csa.register_lesson(
        MID, "csa-m22-n-plus-one", "N+1 and the read-shape problem",
        "Why lazy access patterns multiply queries, how to detect them, and the join/batch shapes that fix them.",
        15, "advanced", _m22_nplusone, _m22_nplusone_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m22", "Checkpoint: data access",
        "Synthesis: an optimistic-concurrency store with retry and a query-count budget.",
        12, "advanced", _m22_checkpoint, _m22_checkpoint_vi,
    )

    csa.register_challenge(
        "csa-checkpoint-m22-task", MID,
        title="Data access checkpoint",
        prompt=(
            "Build `class OptimisticStore<T> where T : notnull` with `void Put(string key, T value, int expectedVersion)` "
            "and `(bool ok, T? value) TryGet(string key)` plus `int VersionOf(string key)`. Put stores only if the "
            "expected version matches the current one (missing key = expected version 0), increments the version, and "
            "throws `InvalidOperationException` named by message prefix \"version conflict\" otherwise. Then implement "
            "`static int SaveAll(OptimisticStore<string> store, List<(string Key, string Value, int Expected)> writes, "
            "int maxRounds)` that applies writes in rounds — each round attempts every not-yet-saved write against the "
            "current version, counting conflicts — and returns the number of rounds needed (throw InvalidOperationException "
            "if not done within maxRounds)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "conflict-detected",
                "code": (
                    "var s = new OptimisticStore<string>();\n"
                    "s.Put(\"k\", \"v1\", 0);\n"
                    "bool threw = false;\n"
                    "try { s.Put(\"k\", \"v2\", 0); } catch (InvalidOperationException) { threw = true; }\n"
                    'Cj.True(threw, "stale expected version must throw");\n'
                    'Cj.Eq(s.TryGet("k").value, "v1", "original value preserved");\n'
                    'Cj.Eq(s.VersionOf("k"), 1, "version advanced once");'
                ),
                "hint": "Track Dictionary<string,(T value,int version)>; on Put compare expected to current version before writing.",
            },
            {
                "name": "conflict-retry-converges",
                "code": (
                    "var s = new OptimisticStore<string>();\n"
                    "// The third write is ALREADY stale when submitted: it expects version 0,\n"
                    "// but the first write bumps 'a' to version 1 in the same round.\n"
                    "var writes = new List<(string, string, int)> { (\"a\", \"x\", 0), (\"b\", \"y\", 0), (\"a\", \"x2\", 0) };\n"
                    "int rounds = OptimisticStore<string>.SaveAll(s, writes, 5);\n"
                    'Cj.True(rounds >= 2, "stale write needs a second round");\n'
                    'Cj.Eq(s.TryGet("a").value, "x2", "stale write won after retry");\n'
                    'Cj.Eq(s.VersionOf("a"), 2, "a was written twice");'
                ),
                "hint": "Keep a pending list; each round retry entries whose expectedVersion now matches; count rounds.",
            },
        ],
        reference=(
            "public class OptimisticStore<T> where T : notnull\n{\n"
            "    private readonly Dictionary<string, (T Value, int Version)> _data = new();\n\n"
            "    public void Put(string key, T value, int expectedVersion)\n"
            "    {\n"
            "        int current = _data.TryGetValue(key, out var e) ? e.Version : 0;\n"
            "        if (current != expectedVersion)\n"
            "            throw new InvalidOperationException($\"version conflict on '{key}': expected {expectedVersion}, current {current}\");\n"
            "        _data[key] = (value, current + 1);\n"
            "    }\n\n"
            "    public (bool ok, T? value) TryGet(string key) =>\n"
            "        _data.TryGetValue(key, out var e) ? (true, e.Value) : (false, default);\n\n"
            "    public int VersionOf(string key) => _data.TryGetValue(key, out var e) ? e.Version : 0;\n\n"
            "    public static int SaveAll(OptimisticStore<string> store, List<(string Key, string Value, int Expected)> writes, int maxRounds)\n"
            "    {\n"
            "        var pending = new List<(string Key, string Value, int Expected)>(writes);\n"
            "        int rounds = 0;\n"
            "        while (pending.Count > 0)\n"
            "        {\n"
            "            rounds++;\n"
            "            if (rounds > maxRounds) throw new InvalidOperationException(\"did not converge\");\n"            "        var stillPending = new List<(string Key, string Value, int Expected)>();\n"
            "            foreach (var w in pending)\n"
            "            {\n"
            "                try { store.Put(w.Key, w.Value, w.Expected); }\n"
            "                catch (InvalidOperationException)\n"
            "                {\n"
            "                    // Optimistic retry: re-read the current version, like a real\n"
            "                    // read-modify-write loop would, and try again next round.\n"
            "                    stillPending.Add((w.Key, w.Value, store.VersionOf(w.Key)));\n"
            "                }\n"
            "            }\n"
            "            pending = stillPending;\n"
            "        }\n"
            "        return rounds;\n"
            "    }\n}"
        ),
        wrong=(
            "public class OptimisticStore<T> where T : notnull\n{\n"
            "    private readonly Dictionary<string, (T Value, int Version)> _data = new();\n\n"
            "    public void Put(string key, T value, int expectedVersion)\n"
            "    {\n"
            "        // WRONG: ignores expectedVersion — lost update, no conflict ever\n"
            "        int current = _data.TryGetValue(key, out var e) ? e.Version : 0;\n"
            "        _data[key] = (value, current + 1);\n"
            "    }\n\n"
            "    public (bool ok, T? value) TryGet(string key) =>\n"
            "        _data.TryGetValue(key, out var e) ? (true, e.Value) : (false, default);\n\n"
            "    public int VersionOf(string key) => _data.TryGetValue(key, out var e) ? e.Version : 0;\n\n"
            "    public static int SaveAll(OptimisticStore<string> store, List<(string Key, string Value, int Expected)> writes, int maxRounds)\n"
            "    {\n"
            "        foreach (var w in writes) store.Put(w.Key, w.Value, w.Expected);\n"
            "        return 1;\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p22-data", "Data access drills",
        "Connection-budget arithmetic, isolation anomalies, and N+1 query counting — all deterministic.",
        45, "advanced", "csa-m22-transactions",
        ["csa-p22-pool-budget", "csa-p22-nplus-one-count"],
    )
    csa.register_challenge(
        "csa-p22-pool-budget", MID,
        title="Connection pool budget",
        prompt=(
            "A pool of size P serving concurrent requests: requests hold a connection for `holdMs` milliseconds. "
            "Implement `static int MaxConcurrentWithin(int poolSize, int requests, int holdMs, int windowMs)` = how many "
            "of `requests` can be in-flight simultaneously given poolSize connections (min(poolSize, requests)), and "
            "`static double Utilization(int poolSize, int requests, int holdMs, int windowMs)` = "
            "MaxConcurrentWithin × holdMs / windowMs × 100, rounded to 2 decimals. Then `static bool WillStarve(int "
            "poolSize, int requests, int holdMs, int windowMs)` = true when requests > poolSize."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "pool-limits-concurrency",
                "code": (
                    'Cj.Eq(ConnBudget.MaxConcurrentWithin(8, 100, 10, 1000), 8, "pool caps in-flight");\n'
                    'Cj.Eq(ConnBudget.MaxConcurrentWithin(8, 3, 10, 1000), 3, "fewer requests than pool");\n'
                    'Cj.Eq(ConnBudget.WillStarve(8, 100, 10, 1000), true, "more requests than pool starves");\n'
                    'Cj.Eq(ConnBudget.WillStarve(8, 3, 10, 1000), false, "no starvation under capacity");'
                ),
                "hint": "Pure arithmetic: cap = min(poolSize, requests); starve = requests > poolSize.",
            },
            {
                "name": "utilization-formula",
                "code": (
                    'Cj.Eq(ConnBudget.Utilization(8, 100, 50, 1000), 40.0, "8×50/1000×100");\n'
                    'Cj.Eq(ConnBudget.Utilization(4, 2, 250, 1000), 50.0, "2×250/1000×100");'
                ),
                "hint": "cap × holdMs ÷ windowMs × 100, Math.Round to 2 decimals.",
            },
        ],
        reference=(
            "public static class ConnBudget\n{\n"
            "    public static int MaxConcurrentWithin(int poolSize, int requests, int holdMs, int windowMs) =>\n"
            "        Math.Min(poolSize, requests);\n\n"
            "    public static double Utilization(int poolSize, int requests, int holdMs, int windowMs)\n"
            "    {\n"
            "        int cap = MaxConcurrentWithin(poolSize, requests, holdMs, windowMs);\n"
            "        return Math.Round(cap * (double)holdMs / windowMs * 100, 2);\n"
            "    }\n\n"
            "    public static bool WillStarve(int poolSize, int requests, int holdMs, int windowMs) =>\n"
            "        requests > poolSize;\n"
            "}"
        ),
        wrong=(
            "public static class ConnBudget\n{\n"
            "    public static int MaxConcurrentWithin(int poolSize, int requests, int holdMs, int windowMs) =>\n"
            "        requests;   // WRONG: ignores the pool cap\n\n"
            "    public static double Utilization(int poolSize, int requests, int holdMs, int windowMs)\n"
            "    {\n"
            "        int cap = MaxConcurrentWithin(poolSize, requests, holdMs, windowMs);\n"
            "        return Math.Round(cap * (double)holdMs / windowMs * 100, 2);\n"
            "    }\n\n"
            "    public static bool WillStarve(int poolSize, int requests, int holdMs, int windowMs) =>\n"
            "        requests > poolSize;\n"
            "}"
        ),
        level="real-world",
    )
    csa.register_challenge(
        "csa-p22-nplus-one-count", MID,
        title="N+1 query counter",
        prompt=(
            "Given `orders` (List<string> ids) each needing one query for its lines: a naive loop issues 1 + N queries. "
            "Implement `static int NaiveQueries(int orderCount)` = orderCount + 1, and `static int BatchedQueries(int "
            "orderCount, int batchSize)` = ceil(orderCount / batchSize) + 1 (batch IN-queries). Then implement `static "
            "(int naive, int batched, double saved) Compare(int orderCount, int batchSize)` returning all three with "
            "saved = round((naive − batched) / naive × 100, 2)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "query-math",
                "code": (
                    'Cj.Eq(Queries.NaiveQueries(100), 101, "1 + N");\n'
                    'Cj.Eq(Queries.BatchedQueries(100, 20), 6, "ceil(100/20)=5 IN-queries + 1");\n'
                    'var (n, b, saved) = Queries.Compare(100, 20);\n'
                    'Cj.Eq(n, 101, "naive");\n'
                    'Cj.Eq(b, 6, "batched");\n'
                    'Cj.Eq(saved, 94.06, "(101−6)/101×100");'
                ),
                "hint": "(int)Math.Ceiling(orderCount / (double)batchSize); saved via Math.Round to 2 decimals.",
            },
        ],
        reference=(
            "public static class Queries\n{\n"
            "    public static int NaiveQueries(int orderCount) => orderCount + 1;\n\n"
            "    public static int BatchedQueries(int orderCount, int batchSize) =>\n"
            "        (int)Math.Ceiling(orderCount / (double)batchSize) + 1;\n\n"
            "    public static (int naive, int batched, double saved) Compare(int orderCount, int batchSize)\n"
            "    {\n"
            "        int n = NaiveQueries(orderCount);\n"
            "        int b = BatchedQueries(orderCount, batchSize);\n"
            "        return (n, b, Math.Round((n - b) / (double)n * 100, 2));\n"
            "    }\n}"
        ),
        wrong=(
            "public static class Queries\n{\n"
            "    public static int NaiveQueries(int orderCount) => orderCount;   // WRONG: forgot the initial query\n\n"
            "    public static int BatchedQueries(int orderCount, int batchSize) =>\n"
            "        orderCount / batchSize + 1;   // WRONG: integer division, no ceiling\n\n"
            "    public static (int naive, int batched, double saved) Compare(int orderCount, int batchSize)\n"
            "    {\n"
            "        int n = NaiveQueries(orderCount);\n"
            "        int b = BatchedQueries(orderCount, batchSize);\n"
            "        return (n, b, Math.Round((n - b) / (double)n * 100, 2));\n"
            "    }\n}"
        ),
        level="debugging",
    )

    # ── Lesson bodies ────────────────────────────────────────────────────────


_m22_lifecycle = r"""## Connection lifecycle and pooling

Opening a real database connection costs a TCP handshake, auth, and session
setup — milliseconds you pay per *logical* operation if you are careless. So
ADO.NET (and every driver above it) keeps a **pool**: `Close()` returns the
connection to the pool; the physical socket stays warm. Two rules follow.

**Open late, close early.** Hold a connection only while a query is running —
not while you compute, not while you call another service. A connection held
across a remote HTTP call is the classic "site slows to a crawl at 3 p.m."
bug: the pool is finite (default max 100), and once every connection is
checked out, the next caller **blocks** waiting for one until
`Connection Timeout` (default 15 s) expires with
`InvalidOperationException: Timeout expired... The connection pool has been
exhausted`.

**The leak patterns** that exhaust pools:

- No `using`/`await using` around the connection (exception path skips Close).
- Returning a connection-holding object (reader, command) from a method.
- Holding the connection while awaiting unrelated I/O.
- Dynamic connection strings — the pool keys on the exact string, so
  per-tenant connection strings silently create per-tenant pools.

Pool exhaustion is a *concurrency* symptom: a single-user test never sees it.
That is why the challenge models occupancy arithmetic instead of real
connections — the reasoning transfers unchanged.

*Language note:* connection strings are configuration, not code. Secrets
therefore belong in configuration/secrets management (module 23), never in
source. (EN content; VI translation ships alongside per the loader contract.)
"""


_m22_lifecycle_vi = r"""## Vòng đời kết nối và connection pool

Mở một kết nối database thật tốn TCP handshake, xác thực và thiết lập session
— những mili-giây bạn trả cho *mỗi* thao tác nếu bất cẩn. Vì vậy ADO.NET (và
mọi driver phía trên) giữ một **pool**: `Close()` trả kết nối về pool; socket
vật lý vẫn ấm. Hai quy tắc tuân theo.

**Mở muộn, đóng sớm.** Chỉ giữ kết nối khi truy vấn đang chạy — không phải
khi tính toán, không phải khi gọi service khác. Một kết nối bị giữ qua một
lần gọi HTTP từ xa là bug kinh điển khiến site "chậm như rùa lúc 3 giờ chiều":
pool có hạn (mặc định tối đa 100), và khi mọi kết nối đều được mượn, caller
kế tiếp sẽ **chặn** chờ cho đến khi `Connection Timeout` (mặc định 15 giây)
hết với `InvalidOperationException: Timeout expired... The connection pool
has been exhausted`.

**Các mẫu rò rỉ** làm cạn pool:

- Không có `using`/`await using` quanh kết nối (đường exception bỏ qua Close).
- Trả về một đối tượng đang giữ kết nối (reader, command) từ một phương thức.
- Giữ kết nối trong lúc await I/O không liên quan.
- Chuỗi kết nối động — pool đánh khóa theo chuỗi chính xác, nên connection
  string theo từng tenant âm thầm tạo pool theo từng tenant.

Cạn pool là triệu chứng *đồng thời*: bài kiểm thử một người dùng không bao giờ
thấy. Đó là lý do challenge mô hình hóa phép tính chiếm dụng thay cho kết nối
thật — lập luận vẫn chuyển giao nguyên vẹn.

*Ghi chú ngôn ngữ:* connection string là cấu hình, không phải code. Vì vậy
secret thuộc về cấu hình/quản lý secret (module 23), không bao giờ nằm trong
source.
"""


_m22_transactions = r"""## Transactions and isolation levels

A transaction groups operations so they commit together or not at all. The
interesting part is the **isolation level** — what concurrent transactions are
allowed to see of each other. SQL Server defaults to `READ COMMITTED`; the
anomalies each level prevents is a *ladder*, and each rung you climb costs
concurrency:

| Level | Dirty reads | Non-repeatable reads | Phantoms |
| --- | --- | --- | --- |
| READ UNCOMMITTED | possible | possible | possible |
| READ COMMITTED | prevented | possible | possible |
| REPEATABLE READ | prevented | prevented | possible |
| SERIALIZABLE | prevented | prevented | prevented |

(Plus snapshot flavors — `READ COMMITTED SNAPSHOT`, `SNAPSHOT` — which give
you row versions instead of locks; the same anomaly ladder applies, paid in
tempdb and write conflicts instead of blocking.)

**The production skill** is matching the level to the invariant: a report that
sums rows can usually tolerate non-repeatable reads; a "transfer must not
double-spend" cannot. Escalating everything to SERIALIZABLE is how you build a
single-lane bridge and call it a database.

Two more invariants worth memorizing: transactions that only *read* should not
hold write locks long; and **the shorter the transaction, the less any of this
hurts** — commit before remote calls, never await inside one (module 10's
rule, restated in data terms).
"""


_m22_transactions_vi = r"""## Giao dịch và mức isolation

Một transaction gom các thao tác để chúng commit cùng nhau hoặc không gì cả.
Phần thú vị là **mức isolation** — những gì các transaction đồng thời được
phép nhìn thấy của nhau. SQL Server mặc định `READ COMMITTED`; các异常 mà mỗi
mức ngăn chặn là một *bậc thang*, và mỗi bậc bạn leo trả giá bằng tính đồng
thời:

| Mức | Dirty read | Non-repeatable read | Phantom |
| --- | --- | --- | --- |
| READ UNCOMMITTED | có thể | có thể | có thể |
| READ COMMITTED | ngăn chặn | có thể | có thể |
| REPEATABLE READ | ngăn chặn | ngăn chặn | có thể |
| SERIALIZABLE | ngăn chặn | ngăn chặn | ngăn chặn |

(Cộng thêm các biến thể snapshot — `READ COMMITTED SNAPSHOT`, `SNAPSHOT` —
cho bạn các phiên bản hàng thay vì khóa; cùng bậc thang anomaly, trả giá bằng
tempdb và xung đột ghi thay vì chặn.)

**Kỹ năng production** là khớp mức với bất biến: báo cáo cộng tổng các hàng
thường chịu được non-repeatable read; "chuyển khoản không được chi đôi" thì
không. Nâng mọi thứ lên SERIALIZABLE là cách bạn xây một cây cầu một làn rồi
gọi nó là database.

Hai bất biến nữa đáng nhớ: transaction chỉ *đọc* không nên giữ khóa ghi lâu;
và **transaction càng ngắn, mọi thứ ở trên càng đỡ đau** — commit trước khi
gọi dịch vụ từ xa, không bao giờ await bên trong (quy tắc module 10, nói lại
bằng thuật ngữ dữ liệu).
"""


_m22_concurrency = r"""## Optimistic vs pessimistic concurrency

Two strategies when two writers touch the same row:

**Pessimistic**: lock first (`SELECT ... WITH (UPDLOCK)`, `SELECT ... FOR
UPDATE`). The second writer *waits* before reading. Safe under high conflict,
deadlock-prone, and it holds the lock across your whole unit of work —
including any remote calls (never do that; see module 20).

**Optimistic**: read freely; on write, verify the row is unchanged via a
**version column** (`UPDATE ... WHERE id = @id AND version = @expected`) and
treat `rows affected = 0` as a conflict to retry. The database does the
arbitration atomically — no locks held across user think-time. This is why
nearly every web API should be optimistic: conflict windows are milliseconds,
human think-time is seconds, and holding locks through it is how you build
pool exhaustion on top of lock queues.

The retry loop is the subtle part: on conflict you must **re-read** the
current version and re-apply your change — not blindly re-run with the stale
expected version, which either loops forever or overwrites. The checkpoint
implements exactly this state machine, deterministically.

**When pessimistic wins**: genuinely hot rows (inventory decrement at flash-
sale rates) where retries would thrash, or multi-table invariants that row
versions cannot express. Even then, prefer the shortest possible lock scope.
"""


_m22_concurrency_vi = r"""## Đồng thời tối ưu (optimistic) và bi quan (pessimistic)

Hai chiến lược khi hai writer chạm cùng một hàng:

**Bi quan (pessimistic)**: khóa trước (`SELECT ... WITH (UPDLOCK)`,
`SELECT ... FOR UPDATE`). Writer thứ hai *chờ* trước khi đọc. An toàn khi xung
đột cao, dễ deadlock, và nó giữ khóa suốt đơn vị công việc của bạn — kể cả các
lời gọi từ xa (đừng bao giờ làm vậy; xem module 20).

**Tối ưu (optimistic)**: đọc tự do; khi ghi, xác minh hàng chưa đổi qua một
**cột phiên bản** (`UPDATE ... WHERE id = @id AND version = @expected`) và coi
`rows affected = 0` là xung đột cần thử lại. Database làm trọng tài một cách
nguyên tử — không giữ khóa trong thời gian người dùng suy nghĩ. Vì vậy gần
như mọi web API nên optimistic: cửa sổ xung đột tính bằng mili-giây, thời gian
suy nghĩ của người dùng tính bằng giây, và giữ khóa suốt quãng thời gian đó là
cách bạn xây cạn pool trên nền hàng chờ khóa.

Vòng retry là phần tinh tế: khi xung đột bạn phải **đọc lại** phiên bản hiện
tại và áp dụng lại thay đổi — không phải mù quáng chạy lại với expected version
cũ, điều đó hoặc lặp vô hạn hoặc ghi đè. Checkpoint hiện thực đúng state
machine này, một cách deterministic.

**Khi pessimistic thắng**: các hàng thực sự nóng (trừ kho lúc flash-sale) nơi
retry sẽ xoay trôn, hoặc các bất biến đa bảng mà cột phiên bản không diễn đạt
được. Dù vậy, vẫn ưu tiên phạm vi khóa ngắn nhất có thể.
"""


_m22_nplusone = r"""## N+1 and the read-shape problem

The N+1 pattern: one query for the parent list, then **one query per parent**
for children. 100 orders = 101 round-trips. It survives development because
each query is fast and localhost latency is ~0; it detonates in production
where every round-trip costs real network time.

ORMs make it seductively easy: a lazy `order.Lines` inside a loop is N+1 with
no SQL in sight. Detection is therefore a *counting* discipline — log query
counts per request and alarm on growth proportional to list length.

The fixes, in order of preference:

1. **Join** — fetch parents with children in one result set (projection into
   the right shape).
2. **Batch** — `WHERE id IN (...)` in chunks: ceil(N/batch) queries instead
   of N. Chunks keep IN-lists within parameter limits.
3. **Explicit loading** — `Include`/`ThenInclude` (EF Core) or explicit
   prefetch, when the ORM supports it.

The arithmetic in the drill is the whole skill: at 100 orders and batch size
20, 101 queries collapse to 6 — a 94% cut that no amount of index tuning
inside the queries would buy. First fix the *shape*, then tune what remains.
"""


_m22_nplusone_vi = r"""## N+1 và bài toán hình dạng đọc

Mẫu N+1: một truy vấn cho danh sách cha, rồi **một truy vấn cho mỗi cha** để
lấy con. 100 đơn hàng = 101 lượt đi-về-lại. Nó sống sót qua giai đoạn phát
triển vì mỗi truy vấn đều nhanh và độ trễ localhost gần bằng 0; nó phát nổ
trong production khi mỗi round-trip tốn thời gian mạng thật.

ORM làm nó quyến rũ một cách dễ dãi: một `order.Lines` lazy bên trong vòng
lặp chính là N+1 mà không thấy dòng SQL nào. Vì vậy việc phát hiện là một kỷ
luật *đếm* — log số truy vấn cho mỗi request và báo động khi nó tăng tỉ lệ
với độ dài danh sách.

Các cách sửa, theo thứ tự ưu tiên:

1. **Join** — lấy cha kèm con trong một tập kết quả (projection thành đúng
   hình dạng).
2. **Batch** — `WHERE id IN (...)` theo từng khối: ceil(N/batch) truy vấn thay
   vì N. Chia khối giữ danh sách IN trong giới hạn tham số.
3. **Nạp tường minh** — `Include`/`ThenInclude` (EF Core) hoặc prefetch tường
   minh, khi ORM hỗ trợ.

Phép tính trong bài tập chính là toàn bộ kỹ năng: với 100 đơn hàng và batch
size 20, 101 truy vấn sụp còn 6 — mức cắt 94% mà không phép tinh chỉnh index
nào bên trong các truy vấn ấy mua nổi. Sửa *hình dạng* trước, rồi mới tinh
chỉnh phần còn lại.
"""


_m22_checkpoint = r"""## Checkpoint: data access

One store, one state machine, one budget. The store enforces optimistic
concurrency (version check or conflict); the retry loop re-reads the current
version on conflict and converges in rounds; the pool drill keeps the
occupancy arithmetic honest.

If your first `SaveAll` threw forever, the usual cause is reusing the stale
expected version — the fix is *re-read on conflict*, exactly as in production
retry loops. If `VersionOf` lied after a conflict, check that a *failed* Put
mutates nothing.
"""


_m22_checkpoint_vi = r"""## Checkpoint: truy cập dữ liệu

Một store, một state machine, một ngân sách. Store thi hành đồng thời tối ưu
(kiểm tra phiên bản hoặc xung đột); vòng retry đọc lại phiên bản hiện tại khi
xung đột và hội tụ theo các vòng; bài tập pool giữ phép tính chiếm dụng trung
thực.

Nếu `SaveAll` đầu tiên của bạn ném lỗi vĩnh viễn, nguyên nhân thường là tái sử
dụng expected version cũ — cách sửa là *đọc lại khi xung đột*, đúng như các
vòng retry trong production. Nếu `VersionOf` nói dối sau xung đột, hãy kiểm
tra một Put *thất bại* không thay đổi gì cả.
"""
