#!/usr/bin/env python3
"""Module 11 practices: sql, schema, api-db, fullstack. Raw strings throughout."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "databases-full-stack"

# ── sql-practice ────────────────────────────────────────────────────────────
write_practice(
    MOD, "sql-practice",
    "SQL Mechanics — Practice",
    "A query engine in miniature: filter, sort, paginate, aggregate, and audit statements for safety.",
    "Cơ chế SQL — Luyện tập",
    "Một query engine thu nhỏ: lọc, sắp, phân trang, tổng hợp, và kiểm toán câu lệnh vì an toàn.",
    "sql-crud", 22, "intermediate",
    [
        {
            "id": "i2-select-filter",
            "title": "SELECT Filter Simulator",
            "prompt": 'Write `selectRows(rows, spec)` — rows is an array of objects; spec is { where: { col: value }?, orderBy?: [col, "asc"|"desc"], limit?, offset? }. Apply WHERE (all pairs must equal; a spec value of null matches rows where the column IS null), ORDER BY (stable), then OFFSET, then LIMIT. Return the resulting array.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function selectRows(rows, spec) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "filters, sorts, paginates in order",
                    "code": fn_wrap("selectRows", "selectRows") + r'''
const rows = [
  { id: 1, done: false, n: 3 },
  { id: 2, done: true, n: 1 },
  { id: 3, done: false, n: 2 },
];
const out = selectRows(rows, { where: { done: false }, orderBy: ["n", "asc"], limit: 1 });
if (out.length === 1 && out[0].id === 3) throw new Error(""); // replaced below
'''.replace('throw new Error(""); // replaced below', 'if (out.length !== 1 || out[0].id !== 3) throw new Error("done=false sorted by n, first row.");'),
                    "hint": "Filter -> sort -> offset -> limit, exactly the SQL order.",
                },
                {
                    "name": "null matching and desc",
                    "code": fn_wrap("selectRows", "selectRows") + r'''
const rows = [
  { id: 1, due: "2026-01-01" },
  { id: 2, due: null },
  { id: 3, due: "2025-06-01" },
];
const nulls = selectRows(rows, { where: { due: null } });
if (nulls.length !== 1 || nulls[0].id !== 2) throw new Error("null spec matches IS NULL.");
const desc = selectRows(rows, { orderBy: ["due", "desc"] });
if (desc[0].id !== 1) throw new Error("Latest due first.");
''',
                    "hint": "A where-value of null means the column must be null.",
                },
            ],
        },
        {
            "id": "i2-aggregate",
            "title": "GROUP BY Simulator",
            "prompt": 'Write `groupByCount(rows, key)` returning an array of { key: keyValue, count } sorted by count desc (ties: key asc). Write `having(rows, key, min)` chaining: group, then keep groups with count >= min.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function groupByCount(rows, key) {\n  // your code\n}\n\nfunction having(rows, key, min) {\n  // your code — reuse groupByCount\n}\n",
            "tests": [
                {
                    "name": "counts per group, sorted",
                    "code": fn_wrap("groupByCount, having", "groupByCount, having") + r'''
const rows = [
  { author: "ada" }, { author: "ada" }, { author: "bo" },
];
const out = groupByCount(rows, "author");
if (out[0].key !== "ada" || out[0].count !== 2) throw new Error("ada leads with 2.");
if (out[1].count !== 1) throw new Error("bo trails with 1.");
''',
                    "hint": "Map<string, number>, then entries sorted by count desc, key asc.",
                },
                {
                    "name": "HAVING filters groups",
                    "code": fn_wrap("groupByCount, having", "groupByCount, having") + r'''
const rows = [{ a: "x" }, { a: "x" }, { a: "x" }, { a: "y" }];
if (having(rows, "a", 2).length !== 1) throw new Error("Only x survives count >= 2.");
if (having(rows, "a", 5).length !== 0) throw new Error("Nothing survives count >= 5.");
''',
                    "hint": "Filter the grouped output by count.",
                },
            ],
        },
        {
            "id": "i2-sql-audit",
            "title": "SQL Safety Auditor",
            "prompt": 'Write `auditStatement(sql)` — return "unsafe" when the statement is an UPDATE/DELETE without WHERE, or builds SQL via string concatenation (contains `" + ` or backtick-interpolation `${`), or contains "= NULL". Return "parameterized" when it contains "$1" (or "?" placeholder) with a WHERE. Otherwise "ok".',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function auditStatement(sql) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "flags the dangerous statements",
                    "code": fn_wrap("auditStatement", "auditStatement") + r'''
if (auditStatement("UPDATE tasks SET done = true;") !== "unsafe") throw new Error("No WHERE on UPDATE.");
if (auditStatement('DELETE FROM tasks WHERE id = ' + '" + id') !== "unsafe") throw new Error("Concatenation.");
if (auditStatement("SELECT * FROM t WHERE x = NULL") !== "unsafe") throw new Error("= NULL is always wrong.");
''',
                    "hint": "Three independent danger patterns; check them in order.",
                },
                {
                    "name": "parameterized is the gold standard",
                    "code": fn_wrap("auditStatement", "auditStatement") + r'''
if (auditStatement("SELECT * FROM tasks WHERE id = $1") !== "parameterized") throw new Error("Placeholder detected.");
if (auditStatement("SELECT title FROM tasks WHERE author_id = 7") !== "ok") throw new Error("Plain safe select.");
''',
                    "hint": "The parameterized check needs a placeholder AND a WHERE.",
                },
            ],
        },
    ],
    {
        "i2-select-filter": {
            "title": "Mô phỏng bộ lọc SELECT",
            "prompt": 'Viết `selectRows(rows, spec)` — rows là mảng object; spec là { where: { col: value }?, orderBy?: [col, "asc"|"desc"], limit?, offset? }. Áp WHERE (mọi cặp phải bằng; giá trị null trong spec khớp các hàng có cột IS null), ORDER BY (ổn định), rồi OFFSET, rồi LIMIT. Trả về mảng kết quả.',
            "tests": [
                {"name": "lọc, sắp, phân trang theo đúng thứ tự", "hint": "Filter -> sort -> offset -> limit, đúng thứ tự SQL."},
                {"name": "khớp null và desc", "hint": "Giá trị where là null nghĩa là cột phải null."},
            ],
        },
        "i2-aggregate": {
            "title": "Mô phỏng GROUP BY",
            "prompt": 'Viết `groupByCount(rows, key)` trả về mảng { key: keyValue, count } sắp theo count giảm dần (bằng nhau: key tăng dần). Viết `having(rows, key, min)` nối tiếp: nhóm, rồi giữ nhóm có count >= min.',
            "tests": [
                {"name": "đếm theo nhóm, đã sắp", "hint": "Map<string, number>, rồi entries sắp theo count desc, key asc."},
                {"name": "HAVING lọc nhóm", "hint": "Lọc output đã nhóm theo count."},
            ],
        },
        "i2-sql-audit": {
            "title": "Kiểm toán an toàn SQL",
            "prompt": 'Viết `auditStatement(sql)` — trả về "unsafe" khi câu lệnh là UPDATE/DELETE không có WHERE, hoặc dựng SQL bằng nối chuỗi (chứa `" + ` hoặc nội suy backtick `${`), hoặc chứa "= NULL". Trả về "parameterized" khi chứa "$1" (hoặc placeholder "?") kèm WHERE. Còn lại "ok".',
            "tests": [
                {"name": "gắn cờ câu lệnh nguy hiểm", "hint": "Ba pattern nguy hiểm độc lập; kiểm tra theo thứ tự."},
                {"name": "parameterized là chuẩn vàng", "hint": "Check parameterized cần placeholder VÀ WHERE."},
            ],
        },
    },
    [
        ["i2-select-filter", r'''function selectRows(rows, spec) {
  let out = rows;
  if (spec.where) {
    out = out.filter((r) =>
      Object.entries(spec.where).every(([col, val]) => (val === null ? r[col] === null : r[col] === val))
    );
  }
  if (spec.orderBy) {
    const [col, dir] = spec.orderBy;
    out = [...out].sort((a, b) => (a[col] < b[col] ? -1 : a[col] > b[col] ? 1 : 0));
    if (dir === "desc") out.reverse();
  }
  const offset = spec.offset ?? 0;
  const limit = spec.limit ?? out.length;
  return out.slice(offset, offset + limit);
}''', r'''function selectRows(rows, spec) {
  return rows;
}'''],
        ["i2-aggregate", r'''function groupByCount(rows, key) {
  const counts = new Map();
  for (const r of rows) counts.set(r[key], (counts.get(r[key]) ?? 0) + 1);
  return [...counts.entries()]
    .map(([k, c]) => ({ key: k, count: c }))
    .sort((a, b) => b.count - a.count || String(a.key).localeCompare(String(b.key)));
}
function having(rows, key, min) {
  return groupByCount(rows, key).filter((g) => g.count >= min);
}''', r'''function groupByCount(rows, key) {
  return rows.map((r) => ({ key: r[key], count: 1 }));
}
function having(rows, key, min) {
  return groupByCount(rows, key);
}'''],
        ["i2-sql-audit", r'''function auditStatement(sql) {
  const upd = /^(UPDATE|DELETE)\b/.test(sql);
  if (upd && !/\bWHERE\b/i.test(sql)) return "unsafe";
  if (sql.includes('" + ') || sql.includes("${") || sql.includes("= NULL")) return "unsafe";
  if (/\$1|\?/.test(sql) && /\bWHERE\b/i.test(sql)) return "parameterized";
  return "ok";
}''', r'''function auditStatement(sql) {
  return "ok";
}'''],
    ],
)

# ── schema-practice ─────────────────────────────────────────────────────────
write_practice(
    MOD, "schema-practice",
    "Schema Design — Practice",
    "Model relationships in code: foreign-key validation, junction-table integrity, and normalization checks.",
    "Thiết kế schema — Luyện tập",
    "Mô hình hóa quan hệ trong code: kiểm tra khóa ngoại, toàn vẹn bảng nối, và kiểm tra chuẩn hóa.",
    "relational-model", 20, "intermediate",
    [
        {
            "id": "i2-fk-enforce",
            "title": "Foreign-Key Enforcer",
            "prompt": "Write `insertWithFK(tables, table, row)` — tables is { users: Set of ids, tasks: [] }; the tasks table's `authorId` must exist in users. Valid insert => append and return { ok: true, id } (ids are \"t<n>\" incrementing); FK violation => { ok: false, error: \"fk-violation\" } and nothing inserted.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function insertWithFK(tables, table, row) {\n  // your code — support table === \"tasks\" with row.authorId\n}\n",
            "tests": [
                {
                    "name": "valid insert lands",
                    "code": "const fn = new Function(code + \"\\nreturn { insertWithFK };\");\nconst { insertWithFK } = fn();\nconst db = { users: new Set([\"u1\"]), tasks: [] };\nconst r = insertWithFK(db, \"tasks\", { title: \"A\", authorId: \"u1\" });\nif (!r.ok || r.id !== \"t1\" || db.tasks.length !== 1) throw new Error(\"Row stored with id t1.\");\nconst r2 = insertWithFK(db, \"tasks\", { title: \"B\", authorId: \"u1\" });\nif (r2.id !== \"t2\") throw new Error(\"Ids increment.\");",
                    "hint": "Check membership before pushing.",
                },
                {
                    "name": "bad author rejected cleanly",
                    "code": 'const fn = new Function(code + "\\nreturn { insertWithFK };");\nconst { insertWithFK } = fn();\nconst db = { users: new Set(["u1"]), tasks: [] };\nconst r = insertWithFK(db, "tasks", { title: "A", authorId: "ghost" });\nif (r.ok !== false || r.error !== "fk-violation") throw new Error("FK violation named.");\nif (db.tasks.length !== 0) throw new Error("Nothing was inserted.");',
                    "hint": "The rejection must leave state untouched.",
                },
            ],
        },
        {
            "id": "i2-junction-check",
            "title": "Junction Integrity",
            "prompt": 'Write `link(tables, taskId, tagId)` for the junction table `tables.taskTags` (array of { taskId, tagId }): both ids must exist (tables.tasks / tables.tags are arrays with .id fields); duplicates (same pair) are rejected. Success => { ok: true, pair } appended; failure => { ok: false, error: "fk-violation" | "duplicate" }.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function link(tables, taskId, tagId) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "valid pairs link once",
                    "code": 'const fn = new Function(code + "\\nreturn { link };");\nconst { link } = fn();\nconst db = { tasks: [{ id: "t1" }], tags: [{ id: "g1" }], taskTags: [] };\nconst r = link(db, "t1", "g1");\nif (!r.ok || db.taskTags.length !== 1) throw new Error("Pair stored.");\nconst dup = link(db, "t1", "g1");\nif (dup.ok !== false || dup.error !== "duplicate") throw new Error("Same pair twice => duplicate.");',
                    "hint": "Existence checks, then a pair-membership check.",
                },
                {
                    "name": "missing sides rejected",
                    "code": 'const fn = new Function(code + "\\nreturn { link };");\nconst { link } = fn();\nconst db = { tasks: [], tags: [{ id: "g1" }], taskTags: [] };\nconst r = link(db, "t1", "g1");\nif (r.ok !== false || r.error !== "fk-violation") throw new Error("Missing task => FK violation.");\nif (db.taskTags.length !== 0) throw new Error("No partial links.");',
                    "hint": "Both sides must exist before linking.",
                },
            ],
        },
        {
            "id": "i2-normalize-check",
            "title": "Normalization Checker",
            "prompt": 'Write `isNormalized(rows)` — rows are task rows; return false when any row has an `authorName` alongside `authorId` (denormalized duplicate — the name belongs to users), true otherwise. Write `normalize(rows, users)` producing normalized rows: drop authorName, keep authorId; users is the lookup you would join to later.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function isNormalized(rows) {\n  // your code\n}\n\nfunction normalize(rows, users) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "detects duplicated facts",
                    "code": fn_wrap("isNormalized, normalize", "isNormalized, normalize") + r'''
const rows = [
  { id: "t1", authorId: "u1", authorName: "Ada" },
  { id: "t2", authorId: "u2" },
];
if (isNormalized(rows) !== false) throw new Error("authorName duplicates users data.");
if (isNormalized([{ id: "t3", authorId: "u1" }]) !== true) throw new Error("Clean rows are normalized.");
''',
                    "hint": "One check: any row with both fields.",
                },
                {
                    "name": "normalization strips the duplicate",
                    "code": fn_wrap("isNormalized, normalize", "isNormalized, normalize") + r'''
const rows = [{ id: "t1", authorId: "u1", authorName: "Ada", title: "A" }];
const out = normalize(rows);
if ("authorName" in out[0]) throw new Error("The duplicate is gone.");
if (out[0].authorId !== "u1" || out[0].title !== "A") throw new Error("Everything else survives.");
''',
                    "hint": "Destructure out the offender, spread the rest.",
                },
            ],
        },
    ],
    {
        "i2-fk-enforce": {
            "title": "Trình thực thi khóa ngoại",
            "prompt": 'Viết `insertWithFK(tables, table, row)` — tables là { users: Set of ids, tasks: [] }; `authorId` của bảng tasks phải tồn tại trong users. Insert hợp lệ => thêm vào và trả về { ok: true, id } (id dạng "t<n>" tăng dần); vi phạm FK => { ok: false, error: "fk-violation" } và không insert gì.',
            "tests": [
                {"name": "insert hợp lệ được lưu", "hint": "Kiểm tra thuộc tập trước khi push."},
                {"name": "author sai bị từ chối sạch sẽ", "hint": "Lời từ chối phải không động vào trạng thái."},
            ],
        },
        "i2-junction-check": {
            "title": "Toàn vẹn bảng nối",
            "prompt": 'Viết `link(tables, taskId, tagId)` cho bảng nối `tables.taskTags` (mảng { taskId, tagId }): cả hai id phải tồn tại (tables.tasks / tables.tags là các mảng có trường .id); cặp trùng lặp bị từ chối. Thành công => { ok: true, pair } được thêm; thất bại => { ok: false, error: "fk-violation" | "duplicate" }.',
            "tests": [
                {"name": "cặp hợp lệ nối một lần", "hint": "Kiểm tra tồn tại, rồi kiểm tra cặp đã có."},
                {"name": "thiếu một bên bị từ chối", "hint": "Cả hai phía phải tồn tại trước khi nối."},
            ],
        },
        "i2-normalize-check": {
            "title": "Bộ kiểm chuẩn hóa",
            "prompt": 'Viết `isNormalized(rows)` — rows là các hàng task; trả về false khi bất kỳ hàng nào có `authorName` đứng cạnh `authorId` (trùng lặp phi chuẩn — tên thuộc về users), true nếu ngược lại. Viết `normalize(rows)` sinh các hàng đã chuẩn hóa: bỏ authorName, giữ authorId.',
            "tests": [
                {"name": "phát hiện sự thật bị nhân bản", "hint": "Một check: có hàng nào chứa cả hai trường."},
                {"name": "chuẩn hóa xóa bản sao", "hint": "Destructure phần tử lỗi, spread phần còn lại."},
            ],
        },
    },
    [
        ["i2-fk-enforce", r'''function insertWithFK(tables, table, row) {
  if (table === "tasks") {
    if (!tables.users.has(row.authorId)) {
      return { ok: false, error: "fk-violation" };
    }
    const id = "t" + (tables.tasks.length + 1);
    tables.tasks.push({ ...row, id });
    return { ok: true, id };
  }
  return { ok: false, error: "unknown-table" };
}''', r'''function insertWithFK(tables, table, row) {
  const id = "t" + (tables.tasks.length + 1);
  tables.tasks.push({ ...row, id });
  return { ok: true, id };
}'''],
        ["i2-junction-check", r'''function link(tables, taskId, tagId) {
  const hasTask = tables.tasks.some((t) => t.id === taskId);
  const hasTag = tables.tags.some((t) => t.id === tagId);
  if (!hasTask || !hasTag) return { ok: false, error: "fk-violation" };
  const pair = { taskId, tagId };
  if (tables.taskTags.some((p) => p.taskId === taskId && p.tagId === tagId)) {
    return { ok: false, error: "duplicate" };
  }
  tables.taskTags.push(pair);
  return { ok: true, pair };
}''', r'''function link(tables, taskId, tagId) {
  tables.taskTags.push({ taskId, tagId });
  return { ok: true };
}'''],
        ["i2-normalize-check", r'''function isNormalized(rows) {
  return !rows.some((r) => "authorName" in r && "authorId" in r);
}
function normalize(rows) {
  return rows.map(({ authorName, ...rest }) => rest);
}''', r'''function isNormalized(rows) {
  return true;
}
function normalize(rows) {
  return rows;
}'''],
    ],
)

# ── api-db-practice ─────────────────────────────────────────────────────────
write_practice(
    MOD, "api-db-practice",
    "API ↔ Database — Practice",
    "Connect the layers: a repository that maps API operations to data operations with transactions and honest errors.",
    "API ↔ Database — Luyện tập",
    "Nối các tầng: một repository ánh xạ thao tác API sang thao tác dữ liệu với transaction và lỗi trung thực.",
    "transactions-migrations", 20, "intermediate",
    [
        {
            "id": "i2-repository",
            "title": "Repository Pattern",
            "prompt": "Write `makeRepo(db)` — db is { rows: [], nextId: 1 }. The repo exposes `create(data)`, `findById(id)`, `update(id, patch)`, `remove(id)`. create assigns `id` (\"r<n>\") and returns the row; findById returns the row or null; update returns { ok: true, row } or { ok: false, error: \"not-found\" }; remove returns { ok: true } or { ok: false, error: \"not-found\" }. The repo is the ONLY code that touches db.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function makeRepo(db) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "full CRUD cycle",
                    "code": 'const fn = new Function(code + "\\nreturn { makeRepo };");\nconst { makeRepo } = fn();\nconst repo = makeRepo({ rows: [], nextId: 1 });\nconst row = repo.create({ title: "A" });\nif (row.id !== "r1") throw new Error("Created with id.");\nif (repo.findById("r1").title !== "A") throw new Error("Found by id.");\nif (repo.findById("r9") !== null) throw new Error("Missing => null.");\nconst up = repo.update("r1", { title: "B" });\nif (!up.ok || up.row.title !== "B") throw new Error("Updated.");\nif (repo.update("r9", {}).error !== "not-found") throw new Error("Missing update named.");\nif (repo.remove("r1").ok !== true) throw new Error("Removed.");\nif (repo.remove("r1").error !== "not-found") throw new Error("Second remove fails.");',
                    "hint": "One closure over db; four small methods.",
                },
                {
                    "name": "repo hides the storage",
                    "code": 'const fn = new Function(code + "\\nreturn { makeRepo };");\nconst { makeRepo } = fn();\nconst db = { rows: [], nextId: 1 };\nconst repo = makeRepo(db);\nrepo.create({ title: "X" });\nif (db.rows.length !== 1) throw new Error("Backing store used.");\nif (!Array.isArray(db.rows) || typeof db.nextId !== "number") throw new Error("Storage shape unchanged by the repo.");',
                    "hint": "The repo mutates the db object — callers never do.",
                },
            ],
        },
        {
            "id": "i2-transfer-tx",
            "title": "Transactional Transfer",
            "prompt": 'Write `transfer(accounts, fromId, toId, amount)` — accounts is a Map id => { balance }. Rules: missing account => { ok: false, error: "not-found" }; insufficient funds => { ok: false, error: "insufficient" } with NOTHING changed; success debits and credits and returns { ok: true }. The two writes must be atomic in effect: any failure leaves both balances untouched.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function transfer(accounts, fromId, toId, amount) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "happy path moves money once",
                    "code": fn_wrap("transfer", "transfer") + r'''
const acc = new Map([["a", { balance: 100 }], ["b", { balance: 0 }]]);
const r = transfer(acc, "a", "b", 40);
if (!r.ok || acc.get("a").balance !== 60 || acc.get("b").balance !== 40) throw new Error("Atomic debit+credit.");
''',
                    "hint": "Validate first, mutate second — the app-level transaction.",
                },
                {
                    "name": "failures change nothing",
                    "code": fn_wrap("transfer", "transfer") + r'''
const acc = new Map([["a", { balance: 10 }], ["b", { balance: 0 }]]);
if (transfer(acc, "a", "b", 50).error !== "insufficient") throw new Error("Overdraft named.");
if (acc.get("a").balance !== 10 || acc.get("b").balance !== 0) throw new Error("Balances untouched.");
if (transfer(acc, "a", "ghost", 5).error !== "not-found") throw new Error("Missing target named.");
if (acc.get("a").balance !== 10) throw new Error("Still untouched.");
''',
                    "hint": "Every check before the first write.",
                },
            ],
        },
        {
            "id": "i2-n1-refactor",
            "title": "N+1 Refactor",
            "prompt": "Write `countFetches(taskCount, strategy)` — strategy \"naive\" => 1 + taskCount queries; \"join\" => 1; \"batch\" => 2. Then `refactorReport(taskCount, savedMs)` — compute naive vs join query counts and estimate time saved as (naive - join) * savedMs; return { naive, join, msSaved }. This is the arithmetic that convinces teams to fix N+1.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function countFetches(taskCount, strategy) {\n  // your code\n}\n\nfunction refactorReport(taskCount, savedMs) {\n  // your code — use countFetches\n}\n",
            "tests": [
                {
                    "name": "counts per strategy",
                    "code": fn_wrap("countFetches, refactorReport", "countFetches, refactorReport") + r'''
if (countFetches(50, "naive") !== 51) throw new Error("1 list + 50 lookups.");
if (countFetches(50, "join") !== 1) throw new Error("One join.");
if (countFetches(50, "batch") !== 2) throw new Error("List + one IN query.");
''',
                    "hint": "Three formulas.",
                },
                {
                    "name": "the report makes the case",
                    "code": fn_wrap("countFetches, refactorReport", "countFetches, refactorReport") + r'''
const out = refactorReport(100, 5);
if (out.naive !== 101 || out.join !== 1) throw new Error("Counts correct.");
if (out.msSaved !== 500) throw new Error("100 extra queries × 5ms each.");
''',
                    "hint": "(naive - join) * savedMs.",
                },
            ],
        },
    ],
    {
        "i2-repository": {
            "title": "Repository Pattern",
            "prompt": 'Viết `makeRepo(db)` — db là { rows: [], nextId: 1 }. Repo cung cấp `create(data)`, `findById(id)`, `update(id, patch)`, `remove(id)`. create gán `id` ("r<n>") và trả về hàng; findById trả về hàng hoặc null; update trả về { ok: true, row } hoặc { ok: false, error: "not-found" }; remove trả về { ok: true } hoặc { ok: false, error: "not-found" }. Repo là code DUY NHẤT đụng vào db.',
            "tests": [
                {"name": "vòng đời CRUD đầy đủ", "hint": "Một closure trên db; bốn method nhỏ."},
                {"name": "repo giấu kho lưu trữ", "hint": "Repo mutate object db — người gọi không bao giờ làm vậy."},
            ],
        },
        "i2-transfer-tx": {
            "title": "Chuyển tiền dạng transaction",
            "prompt": 'Viết `transfer(accounts, fromId, toId, amount)` — accounts là Map id => { balance }. Quy tắc: thiếu tài khoản => { ok: false, error: "not-found" }; không đủ tiền => { ok: false, error: "insufficient" } với KHÔNG THỨ GÌ thay đổi; thành công thì ghi nợ và ghi có và trả về { ok: true }. Hai phép ghi phải atomic trong hiệu ứng: bất kỳ thất bại nào để nguyên cả hai số dư.',
            "tests": [
                {"name": "ca vui chuyển tiền đúng một lần", "hint": "Validate trước, mutate sau — transaction cấp ứng dụng."},
                {"name": "thất bại không đổi gì", "hint": "Mọi check đứng trước phép ghi đầu tiên."},
            ],
        },
        "i2-n1-refactor": {
            "title": "Refactor N+1",
            "prompt": 'Viết `countFetches(taskCount, strategy)` — strategy "naive" => 1 + taskCount query; "join" => 1; "batch" => 2. Rồi `refactorReport(taskCount, savedMs)` — tính số query naive so với join và ước tính thời gian tiết kiệm (naive - join) * savedMs; trả về { naive, join, msSaved }. Đây là phép toán thuyết phục team sửa N+1.',
            "tests": [
                {"name": "đếm theo từng strategy", "hint": "Ba công thức."},
                {"name": "báo cáo đưa ra lập luận", "hint": "(naive - join) * savedMs."},
            ],
        },
    },
    [
        ["i2-repository", r'''function makeRepo(db) {
  return {
    create(data) {
      const row = { ...data, id: "r" + db.nextId++ };
      db.rows.push(row);
      return row;
    },
    findById(id) {
      return db.rows.find((r) => r.id === id) ?? null;
    },
    update(id, patch) {
      const row = db.rows.find((r) => r.id === id);
      if (!row) return { ok: false, error: "not-found" };
      Object.assign(row, patch);
      return { ok: true, row };
    },
    remove(id) {
      const i = db.rows.findIndex((r) => r.id === id);
      if (i === -1) return { ok: false, error: "not-found" };
      db.rows.splice(i, 1);
      return { ok: true };
    },
  };
}''', r'''function makeRepo(db) {
  return {
    create(data) { db.rows.push(data); return data; },
    findById(id) { return db.rows[0] ?? null; },
    update(id, patch) { return { ok: true, row: db.rows[0] }; },
    remove(id) { return { ok: true }; },
  };
}'''],
        ["i2-transfer-tx", r'''function transfer(accounts, fromId, toId, amount) {
  const from = accounts.get(fromId);
  const to = accounts.get(toId);
  if (!from || !to) return { ok: false, error: "not-found" };
  if (from.balance < amount) return { ok: false, error: "insufficient" };
  from.balance -= amount;
  to.balance += amount;
  return { ok: true };
}''', r'''function transfer(accounts, fromId, toId, amount) {
  accounts.get(fromId).balance -= amount;
  accounts.get(toId).balance += amount;
  return { ok: true };
}'''],
        ["i2-n1-refactor", r'''function countFetches(taskCount, strategy) {
  if (strategy === "naive") return 1 + taskCount;
  if (strategy === "join") return 1;
  return 2;
}
function refactorReport(taskCount, savedMs) {
  const naive = countFetches(taskCount, "naive");
  const join = countFetches(taskCount, "join");
  return { naive, join, msSaved: (naive - join) * savedMs };
}''', r'''function countFetches(taskCount, strategy) {
  return taskCount;
}
function refactorReport(taskCount, savedMs) {
  return { naive: 0, join: 0, msSaved: 0 };
}'''],
    ],
)

# ── fullstack-practice ──────────────────────────────────────────────────────
write_practice(
    MOD, "fullstack-practice",
    "Full-Stack Integration — Practice",
    "The module mini-build: a typed request pipeline from client call to data layer, with every UI state accounted for.",
    "Tích hợp Full-Stack — Luyện tập",
    "Mini-build của module: một pipeline request có kiểu từ lời gọi client đến tầng dữ liệu, với mọi trạng thái UI đều được tính.",
    "fullstack-integration", 25, "intermediate",
    [
        {
            "id": "i2-request-flow",
            "title": "Request Flow State Machine",
            "prompt": 'Write `uiStateFor(event)` — a fetch\'s UI state machine. States: "idle", "loading", "success", "empty", "error". Transitions: ("fetch" => "loading"), ("resolve-with-data" => "success"), ("resolve-empty" => "empty"), ("reject" => "error"), ("reset" => "idle"). Invalid transitions (e.g. "success" from "idle") return "idle-state-invalid".',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function uiStateFor(event) {\n  // your code — event is { from, on }\n}\n",
            "tests": [
                {
                    "name": "happy path transitions",
                    "code": fn_wrap("uiStateFor", "uiStateFor") + r'''
if (uiStateFor({ from: "idle", on: "fetch" }) !== "loading") throw new Error("Fetch starts loading.");
if (uiStateFor({ from: "loading", on: "resolve-with-data" }) !== "success") throw new Error("Data arrives.");
if (uiStateFor({ from: "loading", on: "resolve-empty" }) !== "empty") throw new Error("Empty is its own state.");
if (uiStateFor({ from: "loading", on: "reject" }) !== "error") throw new Error("Failure is a state.");
''',
                    "hint": "A lookup keyed by from+on.",
                },
                {
                    "name": "invalid transitions rejected",
                    "code": fn_wrap("uiStateFor", "uiStateFor") + r'''
if (uiStateFor({ from: "idle", on: "resolve-with-data" }) !== "idle-state-invalid") throw new Error("No data without a request.");
if (uiStateFor({ from: "success", on: "fetch" }) !== "loading") throw new Error("Refetching from success is fine.");
''',
                    "hint": "Unknown from+on pairs are invalid; known ones include refetching.",
                },
            ],
        },
        {
            "id": "i2-shared-schema",
            "title": "Shared Contract",
            "prompt": "Write `makeContract()` returning `{ validateTask, toApiShape }`: validateTask(body) returns { ok: true, value } when title is a non-empty string <= 200 and done is a boolean (missing done defaults false), else { ok: false, issues: [{field, message}] }; toApiShape(task) maps the internal { id, title, done, ownerId } to the public shape { id, title, done, author: ownerId } — ownerId never leaves the server under its real name.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function makeContract() {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "validation both ways",
                    "code": 'const fn = new Function(code + "\\nreturn { makeContract };");\nconst { makeContract } = fn();\nconst c = makeContract();\nconst good = c.validateTask({ title: "Ship" });\nif (!good.ok || good.value.done !== false) throw new Error("done defaults to false.");\nconst bad = c.validateTask({ title: "", done: "yes" });\nif (bad.ok !== false || bad.issues.length !== 2) throw new Error("Both issues reported.");',
                    "hint": "Two checks, both pushing issues.",
                },
                {
                    "name": "internal names stay internal",
                    "code": 'const fn = new Function(code + "\\nreturn { makeContract };");\nconst { makeContract } = fn();\nconst c = makeContract();\nconst pub = c.toApiShape({ id: "t1", title: "A", done: true, ownerId: "u9" });\nif (pub.author !== "u9") throw new Error("ownerId exposed as author.");\nif ("ownerId" in pub) throw new Error("The internal name must not leak.");',
                    "hint": "Rename on the way out; delete the internal key.",
                },
            ],
        },
        {
            "id": "i2-optimistic-ui",
            "title": "Optimistic Update",
            "prompt": 'Write `optimisticApply(state, action)` — state is { items, pending: [] }. For action { type: "add", item }: append item AND record it in pending. For { type: "confirm", id }: remove id from pending (it\'s now real). For { type: "rollback", id }: remove the pending item from items too. Return the new state (non-mutating). Optimistic UI = show first, reconcile later.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function optimisticApply(state, action) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "add, confirm, rollback",
                    "code": fn_wrap("optimisticApply", "optimisticApply") + r'''
let s = { items: [], pending: [] };
s = optimisticApply(s, { type: "add", item: { id: "t1", title: "A" } });
if (s.items.length !== 1 || s.pending.length !== 1) throw new Error("Shown immediately, marked pending.");
s = optimisticApply(s, { type: "confirm", id: "t1" });
if (s.pending.length !== 0 || s.items.length !== 1) throw new Error("Confirmed is real.");
s = optimisticApply(s, { type: "add", item: { id: "t2", title: "B" } });
s = optimisticApply(s, { type: "rollback", id: "t2" });
if (s.items.some((i) => i.id === "t2")) throw new Error("Rolled back means gone.");
''',
                    "hint": "Three action types; each adjusts items and/or pending.",
                },
                {
                    "name": "non-mutation discipline",
                    "code": fn_wrap("optimisticApply", "optimisticApply") + r'''
const original = { items: [{ id: "t1" }], pending: [] };
const out = optimisticApply(original, { type: "add", item: { id: "t2" } });
if (original.items.length !== 1) throw new Error("Original untouched.");
if (out.items.length !== 2) throw new Error("New state returned.");
''',
                    "hint": "Spread arrays; never push on the input.",
                },
            ],
        },
    ],
    {
        "i2-request-flow": {
            "title": "Máy trạng thái luồng request",
            "prompt": 'Viết `uiStateFor(event)` — máy trạng thái UI của một fetch. Trạng thái: "idle", "loading", "success", "empty", "error". Chuyển tiếp: ("fetch" => "loading"), ("resolve-with-data" => "success"), ("resolve-empty" => "empty"), ("reject" => "error"), ("reset" => "idle"). Chuyển tiếp không hợp lệ (ví dụ "success" từ "idle") trả về "idle-state-invalid".',
            "tests": [
                {"name": "chuyển tiếp của ca vui", "hint": "Một lookup khóa bởi from+on."},
                {"name": "chuyển tiếp không hợp lệ bị từ chối", "hint": "Cặp from+on lạ là invalid; các cặp quen thuộc gồm cả refetch."},
            ],
        },
        "i2-shared-schema": {
            "title": "Hợp đồng dùng chung",
            "prompt": 'Viết `makeContract()` trả về `{ validateTask, toApiShape }`: validateTask(body) trả về { ok: true, value } khi title là chuỗi khác rỗng <= 200 và done là boolean (thiếu done mặc định false), ngược lại { ok: false, issues: [{field, message}] }; toApiShape(task) ánh xạ hình dạng nội bộ { id, title, done, ownerId } sang hình dạng công khai { id, title, done, author: ownerId } — ownerId không bao giờ rời server dưới tên thật.',
            "tests": [
                {"name": "validation cả hai hướng", "hint": "Hai check, cả hai push issues."},
                {"name": "tên nội bộ ở lại nội bộ", "hint": "Đổi tên lúc ra ngoài; xóa key nội bộ."},
            ],
        },
        "i2-optimistic-ui": {
            "title": "Cập nhật optimistic",
            "prompt": 'Viết `optimisticApply(state, action)` — state là { items, pending: [] }. Với action { type: "add", item }: thêm item VÀ ghi nó vào pending. Với { type: "confirm", id }: xóa id khỏi pending (giờ nó là thật). Với { type: "rollback", id }: xóa item khỏi items luôn. Trả về state mới (không mutate). Optimistic UI = hiển thị trước, đối chiếu sau.',
            "tests": [
                {"name": "add, confirm, rollback", "hint": "Ba loại action; mỗi loại chỉnh items và/hoặc pending."},
                {"name": "kỷ luật không mutate", "hint": "Spread mảng; đừng bao giờ push trên input."},
            ],
        },
    },
    [
        ["i2-request-flow", r'''const TRANSITIONS = {
  "idle|fetch": "loading",
  "loading|resolve-with-data": "success",
  "loading|resolve-empty": "empty",
  "loading|reject": "error",
  "success|fetch": "loading",
  "error|fetch": "loading",
  "empty|fetch": "loading",
  "idle|reset": "idle",
  "success|reset": "idle",
  "error|reset": "idle",
  "empty|reset": "idle",
  "loading|reset": "idle",
};
function uiStateFor(event) {
  return TRANSITIONS[event.from + "|" + event.on] ?? "idle-state-invalid";
}''', r'''function uiStateFor(event) {
  return "loading";
}'''],
        ["i2-shared-schema", r'''function makeContract() {
  return {
    validateTask(body) {
      const issues = [];
      if (typeof body.title !== "string" || !body.title.trim() || body.title.length > 200) {
        issues.push({ field: "title", message: "required, 1-200 chars" });
      }
      if (body.done !== undefined && typeof body.done !== "boolean") {
        issues.push({ field: "done", message: "must be boolean" });
      }
      if (issues.length) return { ok: false, issues };
      return { ok: true, value: { title: body.title, done: body.done ?? false } };
    },
    toApiShape(task) {
      const { ownerId, ...rest } = task;
      return { ...rest, author: ownerId };
    },
  };
}''', r'''function makeContract() {
  return {
    validateTask(body) {
      return { ok: true, value: body };
    },
    toApiShape(task) {
      return { ...task, author: task.ownerId };
    },
  };
}'''],
        ["i2-optimistic-ui", r'''function optimisticApply(state, action) {
  if (action.type === "add") {
    return {
      items: [...state.items, action.item],
      pending: [...state.pending, action.item.id],
    };
  }
  if (action.type === "confirm") {
    return { ...state, pending: state.pending.filter((id) => id !== action.id) };
  }
  if (action.type === "rollback") {
    return {
      items: state.items.filter((i) => i.id !== action.id),
      pending: state.pending.filter((id) => id !== action.id),
    };
  }
  return state;
}''', r'''function optimisticApply(state, action) {
  state.items.push(action.item);
  return state;
}'''],
    ],
)

print("Module 11 practices written.")
