#!/usr/bin/env python3
"""C# — Intermediate — Module 22: csi-capstone.

Capstone: Task Management Engine. Milestone-graded mini-builds that compose
the whole course — domain + validation, repository, service + authorization,
reporting + persistence, and the DI-wired async engine — no copy-paste
solution.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-capstone"

write_module(
    M,
    "Capstone: Task Management Engine",
    "The whole course in one system: domain and validation, a repository, a service layer with authorization, reporting, persistence, and dependency wiring — built milestone by milestone.",
    "Capstone: Task Management Engine",
    "Cả khóa học trong một hệ thống: domain và validation, repository, service layer với phân quyền, báo cáo, persistence, và wiring phụ thuộc — dựng theo từng cột mốc.",
    ["capstone-domain", "capstone-service", "csi-checkpoint-m22"],
    ["csi-p22-capstone"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "capstone-domain",
    "The Engine's Domain: Entities, Invariants, Validation",
    "A capstone starts from the data: records that carry invariants, validated once at the boundary so every layer below can trust them.",
    26,
    r"""
## What you are building

A **Task Management Engine** — the core of a project tracker:

- **Users** (`Id`, `Name`, `Role` ∈ `Admin`/`Member`),
- **Projects** (`Id`, `Name`, `OwnerId`),
- **Tasks** (`Id`, `ProjectId`, `Title`, `AssigneeId?`, `Priority` ∈
  `Low`/`Medium`/`High`, `Status` ∈ `Todo`/`InProgress`/`Done`),
- operations wrapped in a service layer with validation and authorization,
  backed by a repository, reporting via LINQ, state persisted as JSON.

## Domain first, and make invalid states unrepresentable

Model choices as enums, not strings — the compiler then rejects half the bug
space:

```csharp
public enum Priority { Low, Medium, High }
public enum Status { Todo, InProgress, Done }
```

Validation lives **at the boundary** (the service methods that accept input),
one place, not smeared through every consumer:

- title: required, non-empty after trimming, ≤ 120 chars,
- priority/status: must be a defined enum value (`Enum.IsDefined` — a cast
  `(Priority)99` compiles and is garbage),
- assignee must exist and belong to the same system the task belongs to.

A failed check throws `ArgumentException` (input problem) — the service's
contract. `InvalidOperationException` is reserved for state problems
(completing an already-done task).

## Records for entities

Entities are immutable-with-replacement here: changing a task produces a new
record in the store. Records give value equality and `with` — the engine's
mutations become visible, comparable state transitions:

```csharp
public sealed record Task(
    int Id, int ProjectId, string Title,
    int? AssigneeId, Priority Priority, Status Status);

var opened = t with { Status = Status.InProgress, AssigneeId = uid };
```

## IDs and the store

The repository owns ID allocation (monotonic counter). Services never invent
IDs. Everything else in the engine is built on this foundation.
""",
    "Domain của Engine: Entities, Bất biến, Validation",
    "Capstone bắt đầu từ dữ liệu: record mang bất biến, được validate một lần ở ranh giới để mọi layer dưới tin tưởng.",
    r"""
## Bạn đang dựng gì

Một **Task Management Engine** — lõi của một trình quản lý dự án:

- **Users** (`Id`, `Name`, `Role` ∈ `Admin`/`Member`),
- **Projects** (`Id`, `Name`, `OwnerId`),
- **Tasks** (`Id`, `ProjectId`, `Title`, `AssigneeId?`, `Priority` ∈
  `Low`/`Medium`/`High`, `Status` ∈ `Todo`/`InProgress`/`Done`),
- các thao tác bọc trong service layer với validation và phân quyền, tựa trên
  repository, báo cáo bằng LINQ, trạng thái lưu thành JSON.

## Domain trước, và biến trạng thái sai thành không thể diễn đạt

Model lựa chọn bằng enum, không phải string — compiler từ chối luôn một nửa
không gian lỗi:

```csharp
public enum Priority { Low, Medium, High }
public enum Status { Todo, InProgress, Done }
```

Validation nằm **tại ranh giới** (các method service nhận input), một chỗ,
không rải khắp mọi nơi tiêu thụ:

- title: bắt buộc, không rỗng sau khi trim, ≤ 120 ký tự,
- priority/status: phải là giá trị enum hợp lệ (`Enum.IsDefined` — cast
  `(Priority)99` vẫn compile và là rác),
- assignee phải tồn tại trong cùng hệ thống với task.

Kiểm tra thất bại ném `ArgumentException` (vấn đề input) — hợp đồng của
service. `InvalidOperationException` dành cho vấn đề trạng thái (hoàn thành
một task đã Done).

## Record cho entity

Entity ở đây là bất-variant-quá-thay-thế: đổi một task sinh một record mới
trong kho. Record cho value equality và `with` — các mutation của engine trở
thành chuyển đổi trạng thái nhìn thấy được, so sánh được (xem ví dụ trong bản
tiếng Anh).

## ID và kho

Repository nắm việc cấp ID (bộ đếm tăng dần). Service không bao giờ tự đặt ID.
Mọi thứ còn lại của engine dựng trên nền này.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "capstone-service",
    "The Service Layer: Validation, Authorization, Persistence",
    "The capstone's outer ring: every operation checked (is it valid? is it allowed?), state flowing through the repository, snapshots as JSON — and async at the edges.",
    26,
    r"""
## Operations and their gates

Each service operation answers three questions, in order:

1. **Valid?** — input shape (lesson 1). Bad input → `ArgumentException`.
2. **Allowed?** — authorization. Only an `Admin` adds users to the system;
   only the project's `OwnerId` (or an `Admin`) creates tasks in it or
   reassigns them. Not allowed → `InvalidOperationException` (a *state*
   problem: this caller, this state). Bad actor knowledge is a 401/403 in a
   real API; here the exception type carries the same boundary.
3. **Possible?** — does the referenced project/task exist? Missing →
   `KeyNotFoundException` or a `TryXxx` return, per the operation's contract.

## Repositories behind interfaces

The engine's services depend on `IUserStore`/`IProjectStore`/`ITaskStore`
interfaces; an in-memory implementation backs tests, a JSON-file
implementation backs snapshots. Same code, swappable edge — the module 11/15
/19 lesson composed into one system:

```csharp
public interface ITaskStore
{
    Task Add(Task t);                 // Task = System.Threading.Tasks.Task
    Task<Task?> Find(int id);
    Task Update(Task t);
    Task<System.Collections.Generic.IReadOnlyList<Task>> All();
}
```

## Reporting is just LINQ

Overdue, workload per assignee, project progress — all one-pass pipelines
over `All()`:

```csharp
var open = tasks.Where(t => t.Status != Status.Done)
                .GroupBy(t => t.AssigneeId)
                .OrderByDescending(g => g.Count());
```

## Persistence as a snapshot

JSON round-trip: on demand, serialize the stores (enum values as strings for
readability) to a file; on boot, load. The rules from module 14 apply —
case-insensitive reads, string enums, and never trusting a file's shape.

## Async at the edges

Store I/O is `async` (a real DB would be); the service composes with
`await`, propagates `CancellationToken`, and the UI layer never blocks on
`.Result` — the module 9 contract, one last time.
""",
    "Service Layer: Validation, Phân quyền, Persistence",
    "Vòng ngoài của capstone: mọi thao tác được kiểm tra (hợp lệ? được phép?), trạng thái chảy qua repository, snapshot dạng JSON — và async ở rìa.",
    r"""
## Các thao tác và cổng của chúng

Mỗi thao tác service trả lời ba câu hỏi, theo thứ tự:

1. **Hợp lệ?** — hình dạng input (lesson 1). Input xấu → `ArgumentException`.
2. **Được phép?** — phân quyền. Chỉ `Admin` thêm người dùng vào hệ thống; chỉ
   chủ `OwnerId` của dự án (hoặc `Admin`) tạo task trong đó hoặc gán lại.
   Không được phép → `InvalidOperationException` (vấn đề *trạng thái*).
   Trong API thật, đây là 401/403; ở đây loại exception mang cùng ranh giới.
3. **Có thể?** — project/task được tham chiếu có tồn tại? Thiếu →
   `KeyNotFoundException` hoặc trả về `TryXxx`, tùy hợp đồng.

## Repository sau interface

Service của engine phụ thuộc interface `IUserStore`/`IProjectStore`/
`ITaskStore`; bản in-memory phục vụ test, bản JSON-file phục vụ snapshot.
Cùng code, rìa hoán đổi được — bài học module 11/15/19 ghép thành một hệ
thống (xem chữ ký trong bản tiếng Anh).

## Báo cáo chỉ là LINQ

Quá hạn, khối lượng theo assignee, tiến độ dự án — đều là pipeline một lượt
trên `All()` (ví dụ trong bản tiếng Anh).

## Persistence như một snapshot

JSON hai chiều: khi cần, serialize các kho (giá trị enum dạng string cho dễ
đọc) ra tệp; khi khởi động, nạp vào. Quy tắc module 14 vẫn đúng — đọc
case-insensitive, enum dạng string, và không bao giờ tin hình dạng tệp.

## Async ở rìa

I/O của kho là `async` (database thật cũng vậy); service ghép bằng `await`,
truyền `CancellationToken`, và lớp UI không bao giờ block bằng `.Result` —
hợp đồng module 9, lần cuối.
""",
)

# ---------------------------------------------------------------- practice
DOMAIN_NOTE = (
    "\n"
    "// Provided infrastructure — do not modify. The engine's shared domain\n"
    "// types (all milestones build on these).\n"
    "public enum Priority { Low, Medium, High }\n"
    "public enum Status { Todo, InProgress, Done }\n"
    "public enum Role { Member, Admin }\n"
    "\n"
    "public sealed record User(int Id, string Name, Role Role);\n"
    "public sealed record Project(int Id, string Name, int OwnerId);\n"
    "public sealed record TaskItem(\n"
    "    int Id, int ProjectId, string Title,\n"
    "    int? AssigneeId, Priority Priority, Status Status);\n"
    "\n"
    "public static class DomainGuard\n"
    "{\n"
    "    public static void ValidTitle(string title)\n"
    "    {\n"
    "        if (title == null || title.Trim().Length == 0)\n"
    "            throw new System.ArgumentException(\"title required\");\n"
    "        if (title.Trim().Length > 120)\n"
    "            throw new System.ArgumentException(\"title too long\");\n"
    "    }\n"
    "\n"
    "    public static void Defined(Priority p)\n"
    "    {\n"
    "        if (!System.Enum.IsDefined(typeof(Priority), p))\n"
    "            throw new System.ArgumentException(\"bad priority\");\n"
    "    }\n"
    "\n"
    "    public static void Defined(Status s)\n"
    "    {\n"
    "        if (!System.Enum.IsDefined(typeof(Status), s))\n"
    "            throw new System.ArgumentException(\"bad status\");\n"
    "    }\n"
    "}\n"
)

write_practice(
    M,
    "csi-p22-capstone",
    "Capstone Milestones: Domain to Engine",
    "Build the engine in milestones: task domain with validation, a task repository behind its interface, the authorized service layer, reporting pipelines, and the async JSON snapshot.",
    "Cột mốc Capstone: Từ Domain đến Engine",
    "Dựng engine theo cột mốc: domain task với validation, repository task sau interface, service layer có phân quyền, pipeline báo cáo, và snapshot JSON bất đồng bộ.",
    "capstone-service",
    42,
    "intermediate",
    [
        challenge(
            "csi-p22-domain",
            "Milestone 1 — Task Domain Validation",
            r"""The engine's first gate: `CreateTask` input validation. Write
`Solution.ValidateTaskInput(string title, Priority priority, Status status)`
which:

- throws `System.ArgumentException` when the title is null, empty/whitespace
  after trimming, or over 120 chars (after trim),
- throws `System.ArgumentException` when priority or status is not a defined
  enum value (e.g. `(Priority)99`),
- returns the **trimmed** title when everything is valid,

and `Solution.NewTask(int id, int projectId, string title, Priority priority)`
returning a new `TaskItem` with `Status = Status.Todo`, `AssigneeId = null`
(title already validated/trimmed by you).

Provided: `DomainGuard.ValidTitle/Defined` helpers — reuse them, do not
re-implement the checks.

```csharp
public static class Solution
{
    public static string ValidateTaskInput(string title, Priority priority, Status status);
    public static TaskItem NewTask(int id, int projectId, string title, Priority priority);
}
```

Provided types: `TaskItem(int Id, int ProjectId, string Title, int? AssigneeId, Priority Priority, Status Status)`, `Priority`, `Status`.""",
            CS_PRELUDE + DOMAIN_NOTE,
            [
                (
                    "valid input trims and returns",
                    r"""
var t = Solution.ValidateTaskInput("  Ship the beta  ", Priority.High, Status.Todo);
Cj.Eq(t, "Ship the beta", "trimmed");
""",
                    "Trim once at the boundary; everyone downstream trusts it.",
                ),
                (
                    "bad titles throw ArgumentException",
                    r"""
bool Threw(System.Action a) { try { a(); return false; } catch (System.ArgumentException) { return true; } }
Cj.True(Threw(() => Solution.ValidateTaskInput("", Priority.Low, Status.Todo)), "empty");
Cj.True(Threw(() => Solution.ValidateTaskInput("   ", Priority.Low, Status.Todo)), "whitespace");
Cj.True(Threw(() => Solution.ValidateTaskInput(null, Priority.Low, Status.Todo)), "null");
Cj.True(Threw(() => Solution.ValidateTaskInput(new string('x', 121), Priority.Low, Status.Todo)), "too long");
""",
                    "Every title rule is one ArgumentException away.",
                ),
                (
                    "out-of-range enum values are rejected",
                    r"""
bool ThrewP(Priority p) { try { Solution.ValidateTaskInput("t", p, Status.Todo); return false; } catch (System.ArgumentException) { return true; } }
bool ThrewS(Status s) { try { Solution.ValidateTaskInput("t", Priority.Low, s); return false; } catch (System.ArgumentException) { return true; } }
Cj.True(ThrewP((Priority)99), "undefined priority");
Cj.True(ThrewS((Status)42), "undefined status");
Cj.True(!ThrewP(Priority.Medium), "defined priority passes");
""",
                    "A cast is not a validation — Enum.IsDefined is.",
                ),
                (
                    "NewTask opens in Todo with no assignee",
                    r"""
var task = Solution.NewTask(7, 3, "  Wire the CI  ", Priority.High);
Cj.Eq(task.Id, 7, "id preserved");
Cj.Eq(task.ProjectId, 3, "project preserved");
Cj.Eq(task.Title, "Wire the CI", "trimmed title");
Cj.Eq(task.Status, Status.Todo, "starts in Todo");
Cj.True(task.AssigneeId == null, "unassigned");
""",
                    "The factory composes validation and the opening state.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p22-repository",
            "Milestone 2 — Task Repository",
            r"""Implement the in-memory task store behind its interface — ID
allocation included:

```csharp
public sealed class TaskRepo : Solution.ITaskRepo
{
    public TaskRepo();                       // empty store
    public int NextId();                     // starts at 1, monotonic
    public TaskItem Add(int projectId, string title, Priority priority);  // allocates id, Todo, unassigned
    public bool TryFind(int id, out TaskItem task);
    public bool Update(TaskItem task);       // replace by id; false when missing
    public System.Collections.Generic.IReadOnlyList<TaskItem> All();
}

public interface ITaskRepo
{
    int NextId();
    TaskItem Add(int projectId, string title, Priority priority);
    bool TryFind(int id, out TaskItem task);
    bool Update(TaskItem task);
    System.Collections.Generic.IReadOnlyList<TaskItem> All();
}
```

Both types nest inside `Solution`. Rules:

- IDs start at 1 and increase by one per `Add`, independent of removal
  attempts (there are none — this repo never deletes),
- `Add` stores the item as given (validation already happened at the
  service),
- `Update` replaces the whole item; unknown ids return `false` and change
  nothing,
- `All` returns a snapshot safe to enumerate while the repo keeps changing
  (copy, not live view).""",
            CS_PRELUDE + DOMAIN_NOTE,
            [
                (
                    "ids are monotonic and Add stores the opening state",
                    r"""
var repo = new Solution.TaskRepo();
Cj.Eq(repo.NextId(), 1, "first id");
var a = repo.Add(1, "a", Priority.Low);
var b = repo.Add(1, "b", Priority.High);
Cj.Eq(a.Id, 1, "a gets 1");
Cj.Eq(b.Id, 2, "b gets 2");
Cj.Eq(a.Status, Status.Todo, "opens in Todo");
Cj.True(a.AssigneeId == null, "unassigned");
""",
                    "The repo owns identity; the service never invents ids.",
                ),
                (
                    "TryFind and Update round-trip",
                    r"""
var repo = new Solution.TaskRepo();
var t = repo.Add(2, "t", Priority.Medium);
Cj.True(repo.TryFind(t.Id, out var found), "found");
Cj.Eq(found.Title, "t", "same item");
var moved = found with { Status = Status.InProgress, AssigneeId = 5 };
Cj.True(repo.Update(moved), "update ok");
repo.TryFind(t.Id, out var after);
Cj.Eq(after.Status, Status.InProgress, "state advanced");
Cj.Eq(after.AssigneeId, 5, "assignee set");
""",
                    "Update is replace-by-id; records make transitions explicit.",
                ),
                (
                    "unknown ids fail without side effects",
                    r"""
var repo = new Solution.TaskRepo();
var t = repo.Add(1, "t", Priority.Low);
Cj.True(!repo.Update(t with { Id = 999, Title = "x" }), "unknown update false");
Cj.True(repo.TryFind(t.Id, out var still) && still.Title == "t", "store untouched");
""",
                    "A failed mutation must leave the store exactly as it was.",
                ),
                (
                    "All is a snapshot",
                    r"""
var repo = new Solution.TaskRepo();
repo.Add(1, "a", Priority.Low);
var snap = repo.All();
repo.Add(1, "b", Priority.Low);
Cj.Eq(snap.Count, 1, "snapshot is stable");
Cj.Eq(repo.All().Count, 2, "repo moved on");
""",
                    "Enumerating a changing store needs a copy, not a view.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p22-service-authz",
            "Milestone 3 — The Authorized Service Layer",
            r"""The engine's gates, in one service. Given provided user/project
registries (test seeds them through `Solution.Register`/`Solution.AddProject`),
implement:

```csharp
public static class Solution
{
    public static void Register(int id, string name, Role role);
    public static void AddProject(int id, string name, int ownerId);
    public static int CreateTask(int callerId, int projectId, string title, Priority priority);
    public static void Assign(int callerId, int taskId, int assigneeId);
    public static TaskItem? FindTask(int taskId);
}
```

Both types nest inside `Solution`. Gates, in order:

1. **valid input** — title via `DomainGuard.ValidTitle`, priority defined;
   bad → `System.ArgumentException`,
2. **allowed** — `CreateTask` requires the caller to be the project's owner
   or an `Admin`; `Assign` requires the caller to be the task's project
   owner or an `Admin`. Not allowed → `System.InvalidOperationException`,
3. **possible** — unknown project/task/assignee/user →
   `System.Collections.Generic.KeyNotFoundException`,
4. success — `CreateTask` stores a `Todo` task (via your own repo logic or a
   plain list — your choice, IDs 1,2,3…) and returns its id; `Assign` sets
   the assignee; `FindTask` returns the item or `null`.""",
            CS_PRELUDE + DOMAIN_NOTE,
            [
                (
                    "owner creates, admin creates, stranger does not",
                    r"""
Solution.Register(1, "own", Role.Member);
Solution.Register(2, "adm", Role.Admin);
Solution.Register(3, "out", Role.Member);
Solution.AddProject(10, "p", 1);
Cj.Eq(Solution.CreateTask(1, 10, "owner task", Priority.Low), 1, "owner allowed");
Cj.Eq(Solution.CreateTask(2, 10, "admin task", Priority.Low), 2, "admin allowed");
bool threw = false;
try { Solution.CreateTask(3, 10, "nope", Priority.Low); }
catch (System.InvalidOperationException) { threw = true; }
Cj.True(threw, "outsider refused");
""",
                    "Authorization is explicit: owner or Admin, nobody else.",
                ),
                (
                    "validation fires before authorization",
                    r"""
Solution.Register(1, "own", Role.Member);
Solution.AddProject(10, "p", 1);
bool threw = false;
try { Solution.CreateTask(99, 999, "", Priority.Low); }
catch (System.ArgumentException) { threw = true; }
Cj.True(threw, "invalid input wins first");
""",
                    "The gate order is validate, authorize, resolve.",
                ),
                (
                    "assign checks project ownership and known assignee",
                    r"""
Solution.Register(1, "own", Role.Member);
Solution.Register(5, "dev", Role.Member);
Solution.AddProject(10, "p", 1);
var tid = Solution.CreateTask(1, 10, "t", Priority.Medium);
Solution.Assign(1, tid, 5);
Cj.True(Solution.FindTask(tid)!.AssigneeId == 5, "assigned");
bool threw = false;
try { Solution.Assign(5, tid, 1); }
catch (System.InvalidOperationException) { threw = true; }
Cj.True(threw, "non-owner cannot assign");
""",
                    "Reassignment follows the same owner-or-admin rule.",
                ),
                (
                    "unknown references throw KeyNotFound",
                    r"""
Solution.Register(1, "own", Role.Member);
Solution.AddProject(10, "p", 1);
bool threwProject = false;
try { Solution.CreateTask(1, 999, "t", Priority.Low); }
catch (System.Collections.Generic.KeyNotFoundException) { threwProject = true; }
Cj.True(threwProject, "unknown project");
bool threwAssign = false;
try { Solution.Assign(1, 999, 1); }
catch (System.Collections.Generic.KeyNotFoundException) { threwAssign = true; }
Cj.True(threwAssign, "unknown task");
""",
                    "Referential failures are KeyNotFoundException — a different gate.",
                ),
            ],
            level="mini-build",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p22-reporting",
            "Milestone 4 — Reporting Pipelines",
            r"""LINQ over the store (all inputs are `TaskItem` lists; no mutation):

```csharp
public static class Solution
{
    // "P<projectId>:<openCount>:<doneCount>" ordered by projectId ascending
    public static System.Collections.Generic.List<string> Progress(
        System.Collections.Generic.IReadOnlyList<TaskItem> tasks);

    // ids of open (not Done) tasks of the given priority, highest priority
    // first, ties by id ascending
    public static System.Collections.Generic.List<int> Backlog(
        System.Collections.Generic.IReadOnlyList<TaskItem> tasks, Priority priority);

    // assigneeId -> count of their open tasks; unassigned (null) tasks are
    // excluded; absent assignees simply do not appear
    public static System.Collections.Generic.Dictionary<int, int> Workload(
        System.Collections.Generic.IReadOnlyList<TaskItem> tasks);
}
```

Provided types: `TaskItem`, `Priority`, `Status`.""",
            CS_PRELUDE + DOMAIN_NOTE,
            [
                (
                    "progress counts open vs done per project",
                    r"""
var tasks = new System.Collections.Generic.List<TaskItem> {
    new TaskItem(1, 10, "a", null, Priority.Low, Status.Done),
    new TaskItem(2, 10, "b", null, Priority.Low, Status.Todo),
    new TaskItem(3, 20, "c", null, Priority.Low, Status.InProgress),
};
Cj.Eq(string.Join("|", Solution.Progress(tasks)), "P10:1:1|P20:1:0", "open/done per project, id order");
""",
                    "GroupBy project, count by status, order by id.",
                ),
                (
                    "backlog filters, sorts deterministically",
                    r"""
var tasks = new System.Collections.Generic.List<TaskItem> {
    new TaskItem(1, 10, "a", null, Priority.High, Status.Todo),
    new TaskItem(2, 10, "b", null, Priority.High, Status.Done),
    new TaskItem(3, 10, "c", null, Priority.High, Status.Todo),
    new TaskItem(4, 10, "d", null, Priority.Medium, Status.Todo),
};
Cj.Eq(string.Join(",", Solution.Backlog(tasks, Priority.High)), "1,3", "open high, id order");
""",
                    "Done tasks leave the backlog even at the same priority.",
                ),
                (
                    "workload counts open tasks per assignee",
                    r"""
var tasks = new System.Collections.Generic.List<TaskItem> {
    new TaskItem(1, 10, "a", 5, Priority.Low, Status.Todo),
    new TaskItem(2, 10, "b", 5, Priority.Low, Status.InProgress),
    new TaskItem(3, 10, "c", 5, Priority.Low, Status.Done),
    new TaskItem(4, 10, "d", 6, Priority.Low, Status.Todo),
    new TaskItem(5, 10, "e", null, Priority.Low, Status.Todo),
};
var w = Solution.Workload(tasks);
Cj.True(w.ContainsKey(5) && w[5] == 2, "5 has two open");
Cj.True(w.ContainsKey(6) && w[6] == 1, "6 has one open");
Cj.True(!w.ContainsKey(0), "unassigned excluded");
""",
                    "Done tasks do not weigh on anyone; nulls never become key 0.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p22-domain": vi_challenge(
            "Cột mốc 1 — Validation domain task",
            "Cổng đầu tiên của engine: `Solution.ValidateTaskInput(string title, Priority priority, Status status)` ném `System.ArgumentException` khi title null/rỗng/khoảng trắng/đài hơn 120 ký tự sau trim hoặc enum không hợp lệ (ví dụ `(Priority)99`), trả title đã trim khi hợp lệ; và `Solution.NewTask(...)` trả `TaskItem` mới với `Status.Todo`, không gán. Dùng lại helper `DomainGuard` cấp sẵn, đừng viết lại kiểm tra.",
            [
                ("valid input trims and returns", "Trim một lần ở ranh giới; mọi nơi dưới tin tưởng."),
                ("bad titles throw ArgumentException", "Mọi quy tắc title cách nhau một ArgumentException."),
                ("out-of-range enum values are rejected", "Cast không phải validation — Enum.IsDefined mới là."),
                ("NewTask opens in Todo with no assignee", "Factory ghép validation và trạng thái mở."),
            ],
        ),
        "csi-p22-repository": vi_challenge(
            "Cột mốc 2 — Repository task",
            "Hiện kho task in-memory sau interface (cả hai kiểu lồng trong `Solution`): `TaskRepo` với `NextId()` (từ 1, tăng dần), `Add` (cấp id, Todo, chưa gán), `TryFind`, `Update` (thay toàn bộ theo id; false khi thiếu, không tác dụng phụ), `All` (snapshot, không phải view sống).",
            [
                ("ids are monotonic and Add stores the opening state", "Kho nắm định danh; service không bao giờ tự đặt id."),
                ("TryFind and Update round-trip", "Update là thay-theo-theo-id; record làm chuyển đổi tường minh."),
                ("unknown ids fail without side effects", "Mutation thất bại phải để kho nguyên vẹn."),
                ("All is a snapshot", "Enumerate kho đang đổi cần bản sao, không phải view."),
            ],
        ),
        "csi-p22-service-authz": vi_challenge(
            "Cột mốc 3 — Service layer có phân quyền",
            "Các cổng của engine trong một service (kiểu lồng trong `Solution`): 1) **hợp lệ** — title qua `DomainGuard.ValidTitle`, priority hợp lệ; xấu -> `System.ArgumentException`; 2) **được phép** — `CreateTask`/`Assign` yêu cầu caller là chủ project hoặc `Admin`; không -> `System.InvalidOperationException`; 3) **có thể** — project/task/assignee không tồn tại -> `System.Collections.Generic.KeyNotFoundException`; 4) thành công — lưu task `Todo`, id tăng dần từ 1, `FindTask` trả item hoặc `null`.",
            [
                ("owner creates, admin creates, stranger does not", "Phân quyền tường minh: chủ hoặc Admin, không ai khác."),
                ("validation fires before authorization", "Thứ tự cổng là validate, phân quyền, tra tồn tại."),
                ("assign checks project ownership and known assignee", "Gán lại theo cùng quy tắc chủ-hoặc-admin."),
                ("unknown references throw KeyNotFound", "Lỗi tham chiếu là KeyNotFoundException — một cổng khác."),
            ],
        ),
        "csi-p22-reporting": vi_challenge(
            "Cột mốc 4 — Pipeline báo cáo",
            "LINQ trên kho (input là list `TaskItem`; không mutation): `Progress` trả `\"P<projectId>:<openCount>:<doneCount>\"` theo projectId tăng dần — ví dụ `\"10:1:1|20:1:0\"`; `Backlog(tasks, priority)` trả id các task chưa Done đúng priority, priority cao trước, hòa thì id tăng; `Workload` trả assigneeId -> số task chưa gán Done của họ, loại task chưa gán và người không có task.",
            [
                ("progress counts open vs done per project", "GroupBy project, đếm theo status, sắp theo id."),
                ("backlog filters, sorts deterministically", "Task Done rời backlog kể cả cùng priority."),
                ("workload counts open tasks per assignee", "Task Done không đè lên ai; null không bao giờ thành khóa 0."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p22-domain",
            'public static class Solution\n{\n    public static string ValidateTaskInput(string title, Priority priority, Status status)\n    {\n        DomainGuard.ValidTitle(title);\n        DomainGuard.Defined(priority);\n        DomainGuard.Defined(status);\n        return title.Trim();\n    }\n\n    public static TaskItem NewTask(int id, int projectId, string title, Priority priority)\n    {\n        var clean = ValidateTaskInput(title, priority, Status.Todo);\n        return new TaskItem(id, projectId, clean, null, priority, Status.Todo);\n    }\n}\n',
            'public static class Solution\n{\n    public static string ValidateTaskInput(string title, Priority priority, Status status)\n    {\n        // near-miss: checks length but not null/whitespace, and trusts the\n        // enum cast without Enum.IsDefined\n        if (title != null && title.Length > 120)\n            throw new System.ArgumentException("title too long");\n        return (title ?? "").Trim();\n    }\n\n    public static TaskItem NewTask(int id, int projectId, string title, Priority priority)\n    {\n        var clean = ValidateTaskInput(title, priority, Status.Todo);\n        return new TaskItem(id, projectId, clean, null, priority, Status.Todo);\n    }\n}\n',
        ),
        (
            "csi-p22-repository",
            'public static class Solution\n{\n    public interface ITaskRepo\n    {\n        int NextId();\n        TaskItem Add(int projectId, string title, Priority priority);\n        bool TryFind(int id, out TaskItem task);\n        bool Update(TaskItem task);\n        System.Collections.Generic.IReadOnlyList<TaskItem> All();\n    }\n\n    public sealed class TaskRepo : ITaskRepo\n    {\n        private readonly System.Collections.Generic.Dictionary<int, TaskItem> _items\n            = new System.Collections.Generic.Dictionary<int, TaskItem>();\n        private int _next = 1;\n\n        public int NextId() => _next;\n\n        public TaskItem Add(int projectId, string title, Priority priority)\n        {\n            var t = new TaskItem(_next, projectId, title, null, priority, Status.Todo);\n            _items[_next] = t;\n            _next++;\n            return t;\n        }\n\n        public bool TryFind(int id, out TaskItem task)\n            => _items.TryGetValue(id, out task);\n\n        public bool Update(TaskItem task)\n        {\n            if (!_items.ContainsKey(task.Id)) return false;\n            _items[task.Id] = task;\n            return true;\n        }\n\n        public System.Collections.Generic.IReadOnlyList<TaskItem> All()\n            => new System.Collections.Generic.List<TaskItem>(_items.Values);\n    }\n}\n',
            'public static class Solution\n{\n    public interface ITaskRepo\n    {\n        int NextId();\n        TaskItem Add(int projectId, string title, Priority priority);\n        bool TryFind(int id, out TaskItem task);\n        bool Update(TaskItem task);\n        System.Collections.Generic.IReadOnlyList<TaskItem> All();\n    }\n\n    public sealed class TaskRepo : ITaskRepo\n    {\n        private readonly System.Collections.Generic.Dictionary<int, TaskItem> _items\n            = new System.Collections.Generic.Dictionary<int, TaskItem>();\n        private int _next = 1;\n\n        public int NextId() => _next;\n\n        public TaskItem Add(int projectId, string title, Priority priority)\n        {\n            var t = new TaskItem(_next, projectId, title, null, priority, Status.Todo);\n            _items[_next] = t;\n            _next++;\n            return t;\n        }\n\n        public bool TryFind(int id, out TaskItem task)\n            => _items.TryGetValue(id, out task);\n\n        public bool Update(TaskItem task)\n        {\n            // near-miss: reports success without checking existence — silently\n            // inserting a task the store never issued, ids and all\n            _items[task.Id] = task;\n            return true;\n        }\n\n        public System.Collections.Generic.IReadOnlyList<TaskItem> All()\n            => new System.Collections.Generic.List<TaskItem>(_items.Values);\n    }\n}\n',
        ),
        (
            "csi-p22-service-authz",
            'public static class Solution\n{\n    private sealed record User(int Id, string Name, Role Role);\n    private static readonly System.Collections.Generic.Dictionary<int, User> _users\n        = new System.Collections.Generic.Dictionary<int, User>();\n    private static readonly System.Collections.Generic.Dictionary<int, Project> _projects\n        = new System.Collections.Generic.Dictionary<int, Project>();\n    private static readonly System.Collections.Generic.Dictionary<int, TaskItem> _tasks\n        = new System.Collections.Generic.Dictionary<int, TaskItem>();\n    private static int _nextTask = 1;\n\n    public static void Register(int id, string name, Role role)\n        => _users[id] = new User(id, name, role);\n\n    public static void AddProject(int id, string name, int ownerId)\n        => _projects[id] = new Project(id, name, ownerId);\n\n    public static int CreateTask(int callerId, int projectId, string title, Priority priority)\n    {\n        DomainGuard.ValidTitle(title);\n        DomainGuard.Defined(priority);\n        if (!_users.ContainsKey(callerId))\n            throw new System.Collections.Generic.KeyNotFoundException("caller");\n        if (!_projects.TryGetValue(projectId, out var project))\n            throw new System.Collections.Generic.KeyNotFoundException("project");\n        if (project.OwnerId != callerId && _users[callerId].Role != Role.Admin)\n            throw new System.InvalidOperationException("not allowed");\n        var t = new TaskItem(_nextTask, projectId, title.Trim(), null, priority, Status.Todo);\n        _tasks[t.Id] = t;\n        _nextTask++;\n        return t.Id;\n    }\n\n    public static void Assign(int callerId, int taskId, int assigneeId)\n    {\n        if (!_users.ContainsKey(callerId) || !_users.ContainsKey(assigneeId))\n            throw new System.Collections.Generic.KeyNotFoundException("user");\n        if (!_tasks.TryGetValue(taskId, out var task))\n            throw new System.Collections.Generic.KeyNotFoundException("task");\n        if (!_projects.TryGetValue(task.ProjectId, out var project))\n            throw new System.Collections.Generic.KeyNotFoundException("project");\n        if (project.OwnerId != callerId && _users[callerId].Role != Role.Admin)\n            throw new System.InvalidOperationException("not allowed");\n        _tasks[taskId] = task with { AssigneeId = assigneeId };\n    }\n\n    public static TaskItem? FindTask(int taskId)\n        => _tasks.TryGetValue(taskId, out var t) ? t : null;\n}\n',
            'public static class Solution\n{\n    private sealed record User(int Id, string Name, Role Role);\n    private static readonly System.Collections.Generic.Dictionary<int, User> _users\n        = new System.Collections.Generic.Dictionary<int, User>();\n    private static readonly System.Collections.Generic.Dictionary<int, Project> _projects\n        = new System.Collections.Generic.Dictionary<int, Project>();\n    private static readonly System.Collections.Generic.Dictionary<int, TaskItem> _tasks\n        = new System.Collections.Generic.Dictionary<int, TaskItem>();\n    private static int _nextTask = 1;\n\n    public static void Register(int id, string name, Role role)\n        => _users[id] = new User(id, name, role);\n\n    public static void AddProject(int id, string name, int ownerId)\n        => _projects[id] = new Project(id, name, ownerId);\n\n    public static int CreateTask(int callerId, int projectId, string title, Priority priority)\n    {\n        DomainGuard.ValidTitle(title);\n        DomainGuard.Defined(priority);\n        if (!_users.ContainsKey(callerId))\n            throw new System.Collections.Generic.KeyNotFoundException("caller");\n        if (!_projects.TryGetValue(projectId, out var project))\n            throw new System.Collections.Generic.KeyNotFoundException("project");\n        // near-miss: the authorization check asks the wrong question — it\n        // lets anyone who is *not* the owner through instead of only owners\n        // and admins\n        if (!(project.OwnerId != callerId && _users[callerId].Role != Role.Admin))\n            throw new System.InvalidOperationException("not allowed");\n        var t = new TaskItem(_nextTask, projectId, title.Trim(), null, priority, Status.Todo);\n        _tasks[t.Id] = t;\n        _nextTask++;\n        return t.Id;\n    }\n\n    public static void Assign(int callerId, int taskId, int assigneeId)\n    {\n        if (!_users.ContainsKey(callerId) || !_users.ContainsKey(assigneeId))\n            throw new System.Collections.Generic.KeyNotFoundException("user");\n        if (!_tasks.TryGetValue(taskId, out var task))\n            throw new System.Collections.Generic.KeyNotFoundException("task");\n        if (!_projects.TryGetValue(task.ProjectId, out var project))\n            throw new System.Collections.Generic.KeyNotFoundException("project");\n        if (project.OwnerId != callerId && _users[callerId].Role != Role.Admin)\n            throw new System.InvalidOperationException("not allowed");\n        _tasks[taskId] = task with { AssigneeId = assigneeId };\n    }\n\n    public static TaskItem? FindTask(int taskId)\n        => _tasks.TryGetValue(taskId, out var t) ? t : null;\n}\n',
        ),
        (
            "csi-p22-reporting",
            'public static class Solution\n{\n    public static System.Collections.Generic.List<string> Progress(\n        System.Collections.Generic.IReadOnlyList<TaskItem> tasks)\n    {\n        var rows = new System.Collections.Generic.List<string>();\n        var projects = new System.Collections.Generic.SortedSet<int>();\n        foreach (var t in tasks) projects.Add(t.ProjectId);\n        foreach (var p in projects)\n        {\n            int open = 0, done = 0;\n            foreach (var t in tasks)\n            {\n                if (t.ProjectId != p) continue;\n                if (t.Status == Status.Done) done++; else open++;\n            }\n            rows.Add("P" + p + ":" + open + ":" + done);\n        }\n        return rows;\n    }\n\n    public static System.Collections.Generic.List<int> Backlog(\n        System.Collections.Generic.IReadOnlyList<TaskItem> tasks, Priority priority)\n    {\n        var ids = new System.Collections.Generic.List<int>();\n        foreach (var t in tasks)\n            if (t.Priority == priority && t.Status != Status.Done) ids.Add(t.Id);\n        ids.Sort();\n        return ids;\n    }\n\n    public static System.Collections.Generic.Dictionary<int, int> Workload(\n        System.Collections.Generic.IReadOnlyList<TaskItem> tasks)\n    {\n        var counts = new System.Collections.Generic.Dictionary<int, int>();\n        foreach (var t in tasks)\n        {\n            if (t.AssigneeId == null || t.Status == Status.Done) continue;\n            int a = t.AssigneeId.Value;\n            counts[a] = counts.TryGetValue(a, out var c) ? c + 1 : 1;\n        }\n        return counts;\n    }\n}\n',
            'public static class Solution\n{\n    public static System.Collections.Generic.List<string> Progress(\n        System.Collections.Generic.IReadOnlyList<TaskItem> tasks)\n    {\n        var rows = new System.Collections.Generic.List<string>();\n        var projects = new System.Collections.Generic.SortedSet<int>();\n        foreach (var t in tasks) projects.Add(t.ProjectId);\n        foreach (var p in projects)\n        {\n            int open = 0, done = 0;\n            foreach (var t in tasks)\n            {\n                if (t.ProjectId != p) continue;\n                // near-miss: InProgress tasks are counted as Done — the\n                // report flatters the project and the burn-down lies\n                if (t.Status != Status.Todo) done++; else open++;\n            }\n            rows.Add("P" + p + ":" + open + ":" + done);\n        }\n        return rows;\n    }\n\n    public static System.Collections.Generic.List<int> Backlog(\n        System.Collections.Generic.IReadOnlyList<TaskItem> tasks, Priority priority)\n    {\n        var ids = new System.Collections.Generic.List<int>();\n        foreach (var t in tasks)\n            if (t.Priority == priority && t.Status != Status.Done) ids.Add(t.Id);\n        ids.Sort();\n        return ids;\n    }\n\n    public static System.Collections.Generic.Dictionary<int, int> Workload(\n        System.Collections.Generic.IReadOnlyList<TaskItem> tasks)\n    {\n        var counts = new System.Collections.Generic.Dictionary<int, int>();\n        foreach (var t in tasks)\n        {\n            if (t.AssigneeId == null || t.Status == Status.Done) continue;\n            int a = t.AssigneeId.Value;\n            counts[a] = counts.TryGetValue(a, out var c) ? c + 1 : 1;\n        }\n        return counts;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
FAKE_STORE = (
    "\n"
    "// Provided infrastructure — do not modify. The async fake store the\n"
    "// engine's service is wired against: records puts, seeds initial items,\n"
    "// and completes synchronously (a fake, not a real DB).\n"
    "public sealed class FakeStore\n"
    "{\n"
    "    public System.Collections.Generic.List<TaskItem> Puts { get; } = new System.Collections.Generic.List<TaskItem>();\n"
    "    public System.Collections.Generic.List<TaskItem> Seeds { get; } = new System.Collections.Generic.List<TaskItem>();\n"
    "    public bool Clog { get; set; }\n"
    "    public void Seed(TaskItem item) => Seeds.Add(item);\n"
    "    public System.Threading.Tasks.Task PutAsync(TaskItem item, System.Threading.CancellationToken ct)\n"
    "    {\n"
    "        if (Clog) throw new System.IO.IOException(\"disk full (simulated)\");\n"
    "        Puts.Add(item);\n"
    "        return System.Threading.Tasks.Task.CompletedTask;\n"
    "    }\n"
    "}\n"
)

write_checkpoint(
    M,
    "csi-checkpoint-m22",
    "Checkpoint — The Wired Engine",
    "The capstone's final composition: async JSON persistence behind the store interface, load-boot round-trips, and the DI-shaped wiring that hands the service its collaborators.",
    35,
    r"""
## The gate (mini-build)

Two seams, final form:

1. **JSON snapshot round-trip** — implement
   `Solution.Snapshot(System.Collections.Generic.IReadOnlyList<TaskItem> tasks)` returning
   the JSON string for the list (camelCase property names, enums as strings),
   and
   `Solution.Load(string json)` parsing it back with case-insensitive names.
   Round-trip must preserve id, projectId, title, assigneeId, priority, and
   status exactly (order included).
2. **Wiring** — implement
   `Solution.BuildEngine(FakeStore store)` that constructs the
   engine as the composition root would: a `Service` over the given store,
   returning it. The `Service` (nested in `Solution`, constructor takes
   `FakeStore`) must expose
   `System.Threading.Tasks.Task<int> CreateAsync(int projectId, string title, Priority priority, System.Threading.CancellationToken ct)`
   — validates the title (`DomainGuard.ValidTitle`), allocates ids 1,2,3…,
   stores via the store's
   `Task PutAsync(TaskItem item, System.Threading.CancellationToken ct)`,
   respects cancellation (a cancelled caller gets
   `System.OperationCanceledException` and nothing is stored), surfaces store
   failures to its caller, and returns the new id. `FakeStore` (provided) records puts and can be pre-seeded with
   `Seed(TaskItem)`; its `Task PutAsync` completes synchronously (a fake),
   and `Puts` lists what arrived.

```csharp
public static class Solution
{
    public static string Snapshot(System.Collections.Generic.IReadOnlyList<TaskItem> tasks);
    public static TaskItem[] Load(string json);
    public sealed class Service
    {
        public Service(FakeStore store);
        public System.Threading.Tasks.Task<int> CreateAsync(int projectId, string title, Priority priority, System.Threading.CancellationToken ct);
    }
    public static Service BuildEngine(FakeStore store);
}
// provided: TaskItem, Priority, Status, DomainGuard.ValidTitle,
// FakeStore { Task PutAsync(TaskItem, CancellationToken); List<TaskItem> Puts; void Seed(TaskItem); }
```""",
    "Checkpoint — Engine Được Wired",
    "Ghép cuối của capstone: persistence JSON bất đồng bộ sau interface của kho, vòng lặp load-boot, và wiring kiểu DI trao cho service các cộng sự của nó.",
    r"""
## Cổng kiểm tra (mini-build)

Hai đường nối, hình dạng cuối:

1. **Vòng lặp JSON snapshot** — hiện thực
   `Solution.Snapshot(...)` trả chuỗi JSON của danh sách (tên property
   camelCase, enum dạng string) và `Solution.Load(string json)` phân tích lại
   với tên case-insensitive. Round-trip phải giữ chính xác id, projectId,
   title, assigneeId, priority, status (kể cả thứ tự).
2. **Wiring** — `Solution.BuildEngine(FakeStore store)` dựng engine
   như composition root: một `Service` trên kho đã cho. `Service` (lồng trong
   `Solution`) phải có
   `CreateAsync(...)`: validate title (`DomainGuard.ValidTitle`), cấp id
   1,2,3…, lưu qua `PutAsync` của kho, tôn trọng hủy (kiểm tra
   `ct.IsCancellationRequested` trước khi lưu; ném
   `System.OperationCanceledException`), và trả id mới. `FakeStore` (cấp sẵn)
   ghi nhận các lần put và có thể seed trước.

Xem chữ ký `Solution` trong bản tiếng Anh.
""",
    challenge(
        "csi-checkpoint-m22-task",
        "Wire the Engine",
        "JSON snapshot round-trip with case-insensitive load, plus the DI-wired async service with cancellation.",
        CS_PRELUDE + DOMAIN_NOTE + FAKE_STORE,
        [
            (
                "snapshot round-trips exactly",
                r"""
var tasks = new System.Collections.Generic.List<TaskItem> {
    new TaskItem(1, 10, "alpha", null, Priority.High, Status.Todo),
    new TaskItem(2, 10, "beta", 7, Priority.Low, Status.InProgress),
};
var back = Solution.Load(Solution.Snapshot(tasks));
Cj.Eq(back.Length, 2, "two items");
Cj.Eq(back[0].Title, "alpha", "first preserved");
Cj.Eq(back[1].AssigneeId, 7, "assignee preserved");
Cj.Eq(back[1].Status, Status.InProgress, "status preserved");
""",
                "Serialize camelCase + string enums; parse case-insensitively.",
            ),
            (
                "load tolerates its own output shape and case",
                r"""
var json = Solution.Snapshot(new System.Collections.Generic.List<TaskItem> {
    new TaskItem(9, 3, "gamma", null, Priority.Medium, Status.Done),
});
Cj.True(json.Contains("\"title\"") || json.Contains("\"Title\""), "looks like JSON");
var back = Solution.Load(json);
Cj.Eq(back[0].Priority, Priority.Medium, "enum decoded");
Cj.True(back[0].AssigneeId == null, "null assignee survives");
""",
                "Your loader must read what your writer wrote, whatever the casing.",
            ),
            (
                "BuildEngine hands the store to the service",
                r"""
var store = new FakeStore();
var engine = Solution.BuildEngine(store);
var id = engine.CreateAsync(10, "wire me", Priority.High, System.Threading.CancellationToken.None).GetAwaiter().GetResult();
Cj.Eq(id, 1, "first id");
Cj.Eq(store.Puts.Count, 1, "one put");
Cj.Eq(store.Puts[0].Title, "wire me", "right item stored");
Cj.Eq(store.Puts[0].Status, Status.Todo, "opens in Todo");
""",
                "The composition root's job: one graph, collaborators injected.",
            ),
            (
                "ids continue across the store, cancellation is honored",
                r"""
var store = new FakeStore();
store.Seed(new TaskItem(41, 10, "seeded", null, Priority.Low, Status.Todo));
var engine = Solution.BuildEngine(store);
var id = engine.CreateAsync(10, "next", Priority.Low, System.Threading.CancellationToken.None).GetAwaiter().GetResult();
Cj.Eq(id, 42, "id continues past seeds");
int putsBefore = store.Puts.Count;
using var cts = new System.Threading.CancellationTokenSource();
cts.Cancel();
bool cancelled = false;
try { engine.CreateAsync(10, "never", Priority.Low, cts.Token).GetAwaiter().GetResult(); }
catch (System.OperationCanceledException) { cancelled = true; }
Cj.True(cancelled, "cancelled create throws OperationCanceledException");
Cj.Eq(store.Puts.Count, putsBefore, "cancelled create must persist nothing");
""",
                "Check the token before the store sees anything.",
            ),
            (
                "invalid input never reaches the store",
                r"""
var store = new FakeStore();
var engine = Solution.BuildEngine(store);
bool threw = false;
try { engine.CreateAsync(10, "   ", Priority.Low, System.Threading.CancellationToken.None).GetAwaiter().GetResult(); }
catch (System.ArgumentException) { threw = true; }
Cj.True(threw, "blank title throws");
Cj.Eq(store.Puts.Count, 0, "store untouched");
""",
                "Validation gates before persistence — always.",
            ),
            (
                "store failures propagate to the caller",
                r"""
var store = new FakeStore();
store.Clog = true;
var engine = Solution.BuildEngine(store);
bool failed = false;
try { engine.CreateAsync(10, "blocked", Priority.Low, System.Threading.CancellationToken.None).GetAwaiter().GetResult(); }
catch (System.IO.IOException) { failed = true; }
Cj.True(failed, "the store failure reaches the caller");
Cj.Eq(store.Puts.Count, 0, "the failed put is not recorded as a success");
""",
                "Observe the store task; failures must surface, not vanish.",
            ),
        ],
        level="mini-build",
        difficulty="intermediate",
    ),
    vi_challenge(
        "Wire the Engine",
        "Vòng lặp JSON snapshot (tên case-insensitive khi nạp) cộng service bất đồng bộ wired kiểu DI với hủy.",
        [
            ("snapshot round-trips exactly", "Serialize camelCase + enum dạng string; phân tích case-insensitive."),
            ("load tolerates its own output shape and case", "Loader phải đọc được những gì writer của bạn ghi, bất kể casing."),
            ("BuildEngine hands the store to the service", "Việc của composition root: một đồ thị, collaborator được inject."),
            ("ids continue across the store, cancellation is honored", "Kiểm tra token và quyết định sau khi kho trả lời, không trước."),
            ("store failures propagate to the caller", "Quan sát task của kho; thất bại phải nổi lên, không biến mất."),
            ("invalid input never reaches the store", "Validation chặn trước persistence — luôn luôn."),
        ],
    ),
    solution='public static class Solution\n{\n    private static int _next = 1;\n\n    public static string Snapshot(System.Collections.Generic.IReadOnlyList<TaskItem> tasks)\n    {\n        var opts = new System.Text.Json.JsonSerializerOptions\n        {\n            PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase,\n            Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter() },\n        };\n        return System.Text.Json.JsonSerializer.Serialize(tasks, opts);\n    }\n\n    public static TaskItem[] Load(string json)\n    {\n        var opts = new System.Text.Json.JsonSerializerOptions\n        {\n            PropertyNameCaseInsensitive = true,\n            Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter() },\n        };\n        return System.Text.Json.JsonSerializer.Deserialize<TaskItem[]>(json, opts)\n            ?? new TaskItem[0];\n    }\n\n    public sealed class Service\n    {\n        private readonly FakeStore _store;\n        private int _nextId;\n\n        public Service(FakeStore store)\n        {\n            _store = store;\n            int max = 0;\n            foreach (var t in store.Puts) if (t.Id > max) max = t.Id;\n            foreach (var t in store.Seeds) if (t.Id > max) max = t.Id;\n            _nextId = max + 1;\n        }\n\n        public System.Threading.Tasks.Task<int> CreateAsync(\n            int projectId, string title, Priority priority,\n            System.Threading.CancellationToken ct)\n        {\n            DomainGuard.ValidTitle(title);\n            if (ct.IsCancellationRequested)\n                throw new System.OperationCanceledException(ct);\n            var item = new TaskItem(_nextId, projectId, title.Trim(), null, priority, Status.Todo);\n            return _store.PutAsync(item, ct).ContinueWith(t =>\n            {\n                if (t.IsFaulted) throw t.Exception.InnerException ?? t.Exception;\n                if (ct.IsCancellationRequested)\n                    throw new System.OperationCanceledException(ct);\n                _nextId++;\n                return item.Id;\n            });\n        }\n    }\n\n    public static Service BuildEngine(FakeStore store) => new Service(store);\n}\n',
    wrong='public static class Solution\n{\n    private static int _next = 1;\n\n    public static string Snapshot(System.Collections.Generic.IReadOnlyList<TaskItem> tasks)\n    {\n        var opts = new System.Text.Json.JsonSerializerOptions\n        {\n            PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase,\n            Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter() },\n        };\n        return System.Text.Json.JsonSerializer.Serialize(tasks, opts);\n    }\n\n    public static TaskItem[] Load(string json)\n    {\n        var opts = new System.Text.Json.JsonSerializerOptions\n        {\n            PropertyNameCaseInsensitive = true,\n            Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter() },\n        };\n        return System.Text.Json.JsonSerializer.Deserialize<TaskItem[]>(json, opts)\n            ?? new TaskItem[0];\n    }\n\n    public sealed class Service\n    {\n        private readonly FakeStore _store;\n        private int _nextId;\n\n        public Service(FakeStore store)\n        {\n            _store = store;\n            int max = 0;\n            foreach (var t in store.Puts) if (t.Id > max) max = t.Id;\n            foreach (var t in store.Seeds) if (t.Id > max) max = t.Id;\n            _nextId = max + 1;\n        }\n\n        public System.Threading.Tasks.Task<int> CreateAsync(\n            int projectId, string title, Priority priority,\n            System.Threading.CancellationToken ct)\n        {\n            DomainGuard.ValidTitle(title);\n            // near-miss: stores first, never observes the result — cancelled\n            // callers still persist (no exception) and store failures vanish\n            var item = new TaskItem(_nextId, projectId, title.Trim(), null, priority, Status.Todo);\n            _nextId++;\n            return _store.PutAsync(item, ct).ContinueWith(_ => item.Id);\n        }\n    }\n\n    public static Service BuildEngine(FakeStore store) => new Service(store);\n}\n',
)

print("module 22 authored")
