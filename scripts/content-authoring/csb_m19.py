#!/usr/bin/env python3
"""C# — Beginner — Module 19: csb-git.

Professional workflow: the commit graph as data, branch/merge reasoning,
.gitignore semantics, and commit-message hygiene. Graded as code over a
modeled repo — no git binary needed in the sandbox. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-git"

write_module(
    M,
    "Git and Professional Workflow",
    "The commit graph as a data structure: branches, merges, ignores, and the hygiene that makes a history readable.",
    "Git và Quy trình chuyên nghiệp",
    "Đồ thị commit như một cấu trúc dữ liệu: nhánh, hợp nhất, ignore, và vệ sinh giúp lịch sử dễ đọc.",
    ["csb-m19-commits", "csb-m19-branches", "csb-m19-ignore-hygiene", "csb-checkpoint-m19"],
    ["csb-p19-git"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m19-commits",
    "Commits: snapshots with parents",
    "A commit is a named snapshot pointing at its parent(s) — the history is just a graph you traverse.",
    12,
    r"""
## The mental model that survives

```text
A --- B --- C   (main)
```

Each node is a full snapshot plus metadata: message, author, timestamp, and a pointer to its parent(s). `main` is just a movable label pointing at the newest commit on that line. A commit hash like `a1b2c3d` names one node forever.

**Small, complete commits** tell a story: "add login form", "fix email validation", each self-contained. A week of work as one commit titled "stuff" is a story nobody can review or bisect.
""",
    "Commit: ảnh chụp có cha",
    "Một commit là ảnh chụp được đặt tên trỏ tới cha của nó — lịch sử chỉ là một đồ thị bạn duyệt qua.",
    r"""
## Mô hình tinh thần bền vững

```text
A --- B --- C   (main)
```

Mỗi nút là một ảnh chụp đầy đủ cộng siêu dữ liệu: message, tác giả, thời gian, và con trỏ tới cha. `main` chỉ là một nhãn di động trỏ tới commit mới nhất trên đường đó. Một hash như `a1b2c3d` đặt tên vĩnh viễn cho một nút.

**Commit nhỏ, hoàn chỉnh** kể một câu chuyện: "thêm form đăng nhập", "sửa kiểm tra email", mỗi cái tự chứa. Một tuần công sức gộp thành một commit tên "vài thứ" là câu chuyện không ai review hay bisect nổi.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m19-branches",
    "Branches and merges",
    "A branch is a movable label; a merge is a commit with two parents; conflicts are overlapping edits, nothing mystical.",
    13,
    r"""
## Branch = label

```text
        D --- E   (feature)
       /
A --- B --- C   (main)
```

`git switch feature` moves your working copy; `main` stays parked at C. Commits on a branch don't affect main until you merge — cheap experimentation is the whole point.

## Merge = two-parent commit

```text
        D --- E
       /       \
A --- B --- C --- F   (main, after merge)
```

F has both C and E as parents; the histories join. When both sides edited the same lines differently, git refuses to guess — a **conflict**. Resolution is a human decision recorded in the merge commit: keep theirs, keep yours, or write the version that's actually correct. Conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) mark the two candidate texts; delete the markers, keep the intended code, stage, commit.
""",
    "Nhánh và hợp nhất",
    "Nhánh là một nhãn di động; merge là commit có hai cha; xung đột là các lần sửa chồng lên nhau, không gì huyền bí.",
    r"""
## Nhánh = nhãn

```text
        D --- E   (feature)
       /
A --- B --- C   (main)
```

`git switch feature` di chuyển bản làm việc; `main` đỗ tại C. Commit trên nhánh không ảnh hưởng main cho tới khi bạn hợp nhất — thí nghiệm giá rẻ là toàn bộ ý nghĩa.

## Merge = commit hai cha

```text
        D --- E
       /       \
A --- B --- C --- F   (main, sau merge)
```

F có cả C và E làm cha; hai dòng lịch sử nối vào nhau. Khi cả hai bên sửa cùng những dòng khác nhau, git từ chối đoán — một **xung đột**. Giải quyết là quyết định con người được ghi trong merge commit: giữ của họ, giữ của bạn, hoặc viết phiên bản đúng thật. Các dấu xung đột (`<<<<<<<`, `=======`, `>>>>>>>`) đánh dấu hai bản ứng viên; xóa dấu, giữ mã đúng ý, stage, commit.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m19-ignore-hygiene",
    ".gitignore and history hygiene",
    "What belongs in version control: source yes, build output no — and messages that explain why.",
    12,
    r"""
## What gets ignored

```gitignore
bin/
obj/
*.user
```

Build outputs (`bin/`, `obj/`) are regenerable — committing them bloats every clone and breeds merge conflicts on binary files. Machine-local settings (`*.user`) don't describe the project. The test for what to commit: **can a teammate rebuild the world from what's checked in?** Source, project files, and configuration yes; artifacts no.

## Messages that explain why

```text
Fix off-by-one in SumRange

The exclusive upper bound was treated as inclusive after the
refactor; SumRange(1,5) returned 15 instead of 10.
```

A good message has a subject line (imperative, ~50 chars) and, when needed, a body explaining *why* — the diff already shows *what*. "fix bug" describes nothing; six months later, nobody (including you) knows which bug or why it happened.
""",
    ".gitignore và vệ sinh lịch sử",
    "Điều gì thuộc về phiên bản: mã nguồn thì có, kết quả build thì không — và thông điệp giải thích tại sao.",
    r"""
## Những gì bị bỏ qua

```gitignore
bin/
obj/
*.user
```

Kết quả build (`bin/`, `obj/`) tái tạo được — commit chúng làm phình to mọi bản clone và sinh xung đột trên tệp nhị phân. Thiết lập theo-máy (`*.user`) không mô tả dự án. Phép thử cho thứ cần commit: **đồng nghiệp có thể dựng lại thế giới từ những gì được kiểm vào kho?** Mã nguồn, tệp dự án, cấu hình thì có; sản phẩm build thì không.

## Thông điệp giải thích tại sao

```text
Fix off-by-one in SumRange

The exclusive upper bound was treated as inclusive after the
refactor; SumRange(1,5) returned 15 instead of 10.
```

Một thông điệp tốt có dòng tiêu đề (mệnh lệnh, ~50 ký tự) và khi cần, phần thân giải thích *tại sao* — diff đã cho thấy *cái gì*. "fix bug" không mô tả điều gì; sáu tháng sau, không ai (kể cả bạn) biết bug nào và vì sao.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p19-git",
    "Workflow workshop",
    "Commit graphs, merge reasoning, ignore semantics, and message hygiene — workflow as testable code.",
    "Xưởng quy trình",
    "Đồ thị commit, suy luận hợp nhất, ngữ nghĩa ignore, và vệ sinh thông điệp — quy trình thành mã kiểm chứng được.",
    "csb-m19-ignore-hygiene",
    40,
    "beginner",
    [
        challenge(
            "csb-p19-graph",
            "Commit graph traversal",
            "Implement `static List<string> History(Dictionary<string, string> parent, string head)` — given `parent[commit] = parentCommit` (root commits have parent null), return the history from head back to the root, newest first. Unknown head → `ArgumentException`.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var parent = new Dictionary<string, string> { [\"c\"] = \"b\", [\"b\"] = \"a\" };\nparent[\"a\"] = null;\nCj.Eq(string.Join(\",\", Solution.History(parent, \"c\")), \"c,b,a\", \"newest first\");",
                    "Walk parents from the head; the root terminates the walk.",
                ),
                (
                    "edges",
                    "var parent = new Dictionary<string, string>();\nparent[\"lonely\"] = null;\nCj.Eq(string.Join(\",\", Solution.History(parent, \"lonely\")), \"lonely\", \"single-commit repo\");\nbool t = false;\ntry { Solution.History(new Dictionary<string, string>(), \"ghost\"); } catch (ArgumentException) { t = true; }\nCj.True(t, \"unknown head rejected\");",
                    "A one-commit history and the unknown-head contract.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p19-merge",
            "Merge base reasoning",
            "Implement `static string? CommonAncestor(Dictionary<string, string> parent, string a, string b)` — the nearest commit both a and b descend from (null when no shared ancestor).",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var parent = new Dictionary<string, string> { [\"d\"] = \"b\", [\"e\"] = \"b\", [\"b\"] = \"a\" };\nparent[\"a\"] = null;\nCj.Eq(Solution.CommonAncestor(parent, \"d\", \"e\"), \"b\", \"branch point\");\nCj.Eq(Solution.CommonAncestor(parent, \"d\", \"b\"), \"b\", \"ancestor counts as common\");",
                    "Walk both lines to the deepest shared node.",
                ),
                (
                    "unrelated",
                    "var parent = new Dictionary<string, string> { [\"x\"] = null, [\"y\"] = null };\nCj.Eq(Solution.CommonAncestor(parent, \"x\", \"y\"), null, \"no shared history\");\nCj.Eq(Solution.CommonAncestor(parent, \"x\", \"x\"), \"x\", \"same commit\");",
                    "Disconnected histories have no ancestor; a commit contains itself.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p19-ignore",
            ".gitignore semantics",
            "Implement `static bool IsIgnored(string path, List<string> rules)` — rules like \"bin/\" (directory prefix), \"*.log\" (extension wildcard), or exact names; earlier rules win, and any rule starting with \"!\" un-ignores. Path matches \"bin/\" when the path starts with \"bin/\".",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var rules = new List<string> { \"bin/\", \"*.log\" };\nCj.True(Solution.IsIgnored(\"bin/obj/file.dll\", rules), \"directory rule\");\nCj.True(Solution.IsIgnored(\"logs/app.log\", rules), \"wildcard rule\");\nCj.False(Solution.IsIgnored(\"src/Program.cs\", rules), \"source not ignored\");",
                    "Prefix and extension rules applied in order.",
                ),
                (
                    "negation",
                    "var rules = new List<string> { \"*.log\", \"!keep.log\" };\nCj.True(Solution.IsIgnored(\"debug.log\", rules), \"wildcard\");\nCj.False(Solution.IsIgnored(\"keep.log\", rules), \"negation wins (later rule)\");",
                    "The last matching rule decides — git's actual semantic.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p19-message",
            "Commit message hygiene",
            "Implement `static string? ValidateMessage(string message)` — return null for a good message (non-empty first line, ≤ 72 chars, no trailing period, doesn't start lowercase) or a short reason string: \"empty\", \"too-long\", \"trailing-period\", \"lowercase-start\".",
            CS_PRELUDE,
            [
                (
                    "good",
                    "Cj.Eq(Solution.ValidateMessage(\"Fix off-by-one in SumRange\"), null, \"clean message\");\nCj.Eq(Solution.ValidateMessage(\"Add retry loop to importer\"), null, \"another clean one\");\nCj.Eq(Solution.ValidateMessage(new string('A', 72)), null, \"exactly 72 chars is legal\");",
                    "Imperative, concise, no period.",
                ),
                (
                    "failures",
                    "Cj.Eq(Solution.ValidateMessage(\"\"), \"empty\", \"empty rejected\");\nCj.Eq(Solution.ValidateMessage(new string('x', 73)), \"too-long\", \"over 72\");\nCj.Eq(Solution.ValidateMessage(\"Fix the thing.\"), \"trailing-period\", \"period\");\nCj.Eq(Solution.ValidateMessage(\"fix the thing\"), \"lowercase-start\", \"lowercase\");",
                    "Each failure mode has its own reason — diagnosable messages about messages.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p19-graph": vi_challenge(
            "Duyệt đồ thị commit",
            "Hiện thực `static List<string> History(Dictionary<string, string> parent, string head)` — với `parent[commit] = commitCha` (commit gốc có cha null), trả lịch sử từ head ngược về gốc, mới nhất trước. Head lạ → `ArgumentException`.",
            [
                ("normal", "Đi theo cha từ head; gốc kết thúc cuộc đi."),
                ("edges", "Lịch sử một-commit và hợp đồng head-lạ."),
            ],
        ),
        "csb-p19-merge": vi_challenge(
            "Suy luận merge base",
            "Hiện thực `static string? CommonAncestor(Dictionary<string, string> parent, string a, string b)` — commit gần nhất mà cả a và b đều xuất phát từ đó (null khi không có tổ tiên chung).",
            [
                ("normal", "Đi cả hai đường tới nút chia sẻ sâu nhất."),
                ("unrelated", "Hai lịch sử rời rạc không có tổ tiên; một commit chứa chính nó."),
            ],
        ),
        "csb-p19-ignore": vi_challenge(
            "Ngữ nghĩa .gitignore",
            "Hiện thực `static bool IsIgnored(string path, List<string> rules)` — quy tắc dạng \"bin/\" (tiền tố thư mục), \"*.log\" (wildcard đuôi tệp), hoặc tên chính xác; quy tắc nào khớp sau cùng thắng, và quy tắc bắt đầu bằng \"!\" bỏ-qua-lệnh-ignore. Đường dẫn khớp \"bin/\" khi nó bắt đầu bằng \"bin/\".",
            [
                ("normal", "Quy tắc tiền-tố và đuôi-tệp áp dụng theo thứ tự."),
                ("negation", "Quy tắc khớp CUỐI CÙNG quyết định — đúng ngữ nghĩa của git."),
            ],
        ),
        "csb-p19-message": vi_challenge(
            "Vệ sinh thông điệp commit",
            "Hiện thực `static string? ValidateMessage(string message)` — trả null cho thông điệp tốt (dòng đầu không rỗng, ≤ 72 ký tự, không kết thúc bằng dấu chấm, không bắt đầu bằng chữ thường) hoặc một lý do ngắn: \"empty\", \"too-long\", \"trailing-period\", \"lowercase-start\".",
            [
                ("good", "Mệnh lệnh, ngắn gọn, không dấu chấm — và đúng 72 ký tự vẫn hợp lệ."),
                ("failures", "Mỗi kiểu thất bại có lý do riêng — thông điệp chẩn đoán được về chính thông điệp."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p19-graph",
            'public class Solution\n{\n    public static List<string> History(Dictionary<string, string> parent, string head)\n    {\n        if (!parent.ContainsKey(head))\n            throw new ArgumentException("unknown head");\n        var result = new List<string>();\n        string? current = head;\n        while (current != null)\n        {\n            result.Add(current);\n            current = parent[current];\n        }\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static List<string> History(Dictionary<string, string> parent, string head)\n    {\n        if (!parent.ContainsKey(head))\n            throw new ArgumentException("unknown head");\n        var result = new List<string>();\n        string? current = head;\n        // near-miss: builds the list then REVERSES it — oldest first,\n        // contradicting the newest-first contract\n        while (current != null)\n        {\n            result.Add(current);\n            current = parent[current];\n        }\n        result.Reverse();\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p19-merge",
            'public class Solution\n{\n    public static string? CommonAncestor(Dictionary<string, string> parent, string a, string b)\n    {\n        var ancestors = new HashSet<string>();\n        string? cur = a;\n        while (cur != null) { ancestors.Add(cur); cur = parent[cur]; }\n        cur = b;\n        while (cur != null)\n        {\n            if (ancestors.Contains(cur)) return cur;\n            cur = parent[cur];\n        }\n        return null;\n    }\n}\n',
            'public class Solution\n{\n    public static string? CommonAncestor(Dictionary<string, string> parent, string a, string b)\n    {\n        var ancestors = new HashSet<string>();\n        string? cur = a;\n        while (cur != null) { ancestors.Add(cur); cur = parent[cur]; }\n        // near-miss: does not test b\'s chain\'s START before stepping — when\n        // b itself is the ancestor, the walk skips it and keeps climbing\n        cur = parent[b];\n        while (cur != null)\n        {\n            if (ancestors.Contains(cur)) return cur;\n            cur = parent[cur];\n        }\n        return null;\n    }\n}\n',
        ),
        (
            "csb-p19-ignore",
            'public class Solution\n{\n    public static bool IsIgnored(string path, List<string> rules)\n    {\n        bool ignored = false;\n        foreach (string rule in rules)\n        {\n            if (rule.StartsWith("!"))\n            {\n                string target = rule.Substring(1);\n                if (Matches(path, target)) ignored = false;\n            }\n            else if (Matches(path, rule))\n            {\n                ignored = true;\n            }\n        }\n        return ignored;\n    }\n    private static bool Matches(string path, string rule)\n    {\n        if (rule.EndsWith("/")) return path.StartsWith(rule, StringComparison.Ordinal);\n        if (rule.StartsWith("*.")) return path.EndsWith(rule.Substring(1), StringComparison.Ordinal);\n        return path == rule || path.EndsWith("/" + rule, StringComparison.Ordinal);\n    }\n}\n',
            'public class Solution\n{\n    public static bool IsIgnored(string path, List<string> rules)\n    {\n        // near-miss: FIRST matching rule wins — negations placed later never\n        // get a chance, breaking git\'s last-match-wins semantic\n        foreach (string rule in rules)\n        {\n            if (rule.StartsWith("!"))\n            {\n                string target = rule.Substring(1);\n                if (Matches(path, target)) return false;\n            }\n            else if (Matches(path, rule))\n            {\n                return true;\n            }\n        }\n        return false;\n    }\n    private static bool Matches(string path, string rule)\n    {\n        if (rule.EndsWith("/")) return path.StartsWith(rule, StringComparison.Ordinal);\n        if (rule.StartsWith("*.")) return path.EndsWith(rule.Substring(1), StringComparison.Ordinal);\n        return path == rule || path.EndsWith("/" + rule, StringComparison.Ordinal);\n    }\n}\n',
        ),
        (
            "csb-p19-message",
            'public class Solution\n{\n    public static string? ValidateMessage(string message)\n    {\n        if (string.IsNullOrEmpty(message)) return "empty";\n        if (message.Length > 72) return "too-long";\n        if (message.EndsWith(".")) return "trailing-period";\n        if (char.IsLower(message[0])) return "lowercase-start";\n        return null;\n    }\n}\n',
            'public class Solution\n{\n    public static string? ValidateMessage(string message)\n    {\n        if (string.IsNullOrEmpty(message)) return "empty";\n        // near-miss: 72 treated as INCLUSIVE upper bound but strict < used —\n        // a 72-char message is wrongly rejected as too-long\n        if (message.Length >= 72) return "too-long";\n        if (message.EndsWith(".")) return "trailing-period";\n        if (char.IsLower(message[0])) return "lowercase-start";\n        return null;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m19",
    "Checkpoint — Workflow",
    "A repo auditor: linear-history checks, rebase-vs-merge reasoning, and a change-classification helper.",
    20,
    r"""
## Checkpoint: the repo auditor

**Task:** implement in `Solution`:

1. `static bool IsLinear(List<string> commits)` — true when no commit appears twice (a fork/re-entry breaks linearity); empty list → true.
2. `static string DescribeChange(string before, string after)` — `"added"` when before is empty, `"removed"` when after is empty, `"modified"` otherwise.
3. `static List<string> StaleBranches(Dictionary<string, string> branchTip, string mainTip, List<string> mergedIntoMain)` — branch names whose tip is not main's tip AND are not in `mergedIntoMain`, sorted alphabetically.
""",
    "Checkpoint — Quy trình",
    "Bộ kiểm toán kho: kiểm tra lịch-sử-tuyến-tính, suy luận rebase-vs-merge, và helper phân loại thay đổi.",
    r"""
## Checkpoint: bộ kiểm toán kho

**Nhiệm vụ:** hiện thực trong `Solution`:

1. `static bool IsLinear(List<string> commits)` — true khi không commit nào xuất hiện hai lần (một nhánh/tái-vào phá tính tuyến tính); danh sách rỗng → true.
2. `static string DescribeChange(string before, string after)` — `"added"` khi before rỗng, `"removed"` khi after rỗng, `"modified"` nếu khác.
3. `static List<string> StaleBranches(Dictionary<string, string> branchTip, string mainTip, List<string> mergedIntoMain)` — tên các nhánh có tip khác tip của main VÀ không nằm trong `mergedIntoMain`, sắp theo alphabet.
""",
    challenge(
        "csb-checkpoint-m19-task",
        "RepoAuditor",
        "Implement `IsLinear`, `DescribeChange`, and `StaleBranches` — small pure functions over repo data.",
        CS_PRELUDE,
        [
            (
                "history",
                "Cj.True(Solution.IsLinear(new List<string> { \"a\", \"b\", \"c\" }), \"linear\");\nCj.False(Solution.IsLinear(new List<string> { \"a\", \"b\", \"a\" }), \"re-entry breaks linearity\");\nCj.True(Solution.IsLinear(new List<string>()), \"empty is linear\");\nCj.Eq(Solution.DescribeChange(\"\", \"file.cs\"), \"added\", \"new file\");\nCj.Eq(Solution.DescribeChange(\"file.cs\", \"\"), \"removed\", \"deleted\");\nCj.Eq(Solution.DescribeChange(\"file.cs\", \"file.cs\"), \"modified\", \"edited\");",
                "Linearity, empty-list contract, and the change taxonomy.",
            ),
            (
                "branches",
                "var tips = new Dictionary<string, string>\n{\n    [\"feature/fresh\"] = \"e5\",\n    [\"feature/merged\"] = \"c3\",\n    [\"feature/stale\"] = \"b2\",\n};\nvar stale = Solution.StaleBranches(tips, \"e5\", new List<string> { \"feature/merged\" });\nCj.Eq(string.Join(\",\", stale), \"feature/stale\", \"merged branch is not stale\");",
                "Merged branches are excused; everything else at an old tip is stale.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "RepoAuditor",
        "Hiện thực `IsLinear`, `DescribeChange`, và `StaleBranches` — các hàm thuần nhỏ trên dữ liệu kho.",
        [
            ("history", "Tính tuyến tính, hợp đồng rỗng, và phân loại thay đổi."),
            ("branches", "Nhánh đã merge được miễn; mọi thứ khác ở tip cũ là stale."),
        ],
    ),
    solution='public class Solution\n{\n    public static bool IsLinear(List<string> commits)\n    {\n        var seen = new HashSet<string>();\n        foreach (string c in commits)\n        {\n            if (!seen.Add(c)) return false;\n        }\n        return true;\n    }\n    public static string DescribeChange(string before, string after)\n    {\n        if (before.Length == 0) return "added";\n        if (after.Length == 0) return "removed";\n        return "modified";\n    }\n    public static List<string> StaleBranches(Dictionary<string, string> branchTip, string mainTip, List<string> mergedIntoMain)\n    {\n        var merged = new HashSet<string>(mergedIntoMain);\n        var result = new List<string>();\n        foreach (var kv in branchTip)\n        {\n            if (kv.Value != mainTip && !merged.Contains(kv.Key))\n                result.Add(kv.Key);\n        }\n        result.Sort(StringComparer.Ordinal);\n        return result;\n    }\n}\n',
    wrong='public class Solution\n{\n    public static bool IsLinear(List<string> commits)\n    {\n        var seen = new HashSet<string>();\n        foreach (string c in commits)\n        {\n            if (!seen.Add(c)) return false;\n        }\n        return true;\n    }\n    public static string DescribeChange(string before, string after)\n    {\n        if (before.Length == 0) return "added";\n        if (after.Length == 0) return "removed";\n        return "modified";\n    }\n    public static List<string> StaleBranches(Dictionary<string, string> branchTip, string mainTip, List<string> mergedIntoMain)\n    {\n        var merged = new HashSet<string>(mergedIntoMain);\n        var result = new List<string>();\n        foreach (var kv in branchTip)\n        {\n            // near-miss: treats a branch AT main\'s tip as stale too —\n            // synchronized branches should never be flagged\n            if (!merged.Contains(kv.Key))\n                result.Add(kv.Key);\n        }\n        result.Sort(StringComparer.Ordinal);\n        return result;\n    }\n}\n',
)

print("module 19 authored")
