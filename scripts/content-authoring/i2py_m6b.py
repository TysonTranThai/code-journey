#!/usr/bin/env python3
"""Module 6 practices: history, branching, conflicts, recovery, review, secrets."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "git-workflow"

# ── history-practice ────────────────────────────────────────────────────────
write_practice(
    MOD, "history-practice",
    "History as Data — Practice",
    "Model the commit graph the way Git does: parent pointers, reachability, and divergence — as pure functions.",
    "Lịch sử là dữ liệu — Luyện tập",
    "Mô hình hóa đồ thị commit đúng cách Git làm: con trỏ cha, khả năng với tới, và phân kỳ — bằng các hàm thuần.",
    "git-history-internals", 18, "intermediate",
    [
        {
            "id": "i2-commit-reach",
            "title": "Reachability",
            "prompt": "Given `commits` — a map of id → parent id (null for root) — and a target id, return an array of ALL ancestor ids reachable from the target (including itself), ordered oldest-first (walk to root, then reverse).",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function reachable(commits, target) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "walks parents to the root",
                    "code": fn_wrap("reachable", "reachable") + "\nconst cs = { C: \"B\", B: \"A\", A: null };\nconst out = reachable(cs, \"C\");\nif (out.join(\",\") !== \"A,B,C\") throw new Error(\"Oldest-first: root A up to C.\");",
                    "hint": "Follow the parent chain collecting ids, then reverse.",
                },
                {
                    "name": "handles roots and unknown links",
                    "code": fn_wrap("reachable", "reachable") + "\nconst cs = { D: null, E: \"D\" };\nif (reachable(cs, \"D\").join(\",\") !== \"D\") throw new Error(\"A root reaches only itself.\");\nif (reachable(cs, \"E\").join(\",\") !== \"D,E\") throw new Error(\"E reaches D then E.\");\nif (reachable({}, \"X\").length !== 0) throw new Error(\"Unknown target => empty.\");",
                    "hint": "Stop when parent is null or the id is missing from the map.",
                },
            ],
        },
        {
            "id": "i2-diverged",
            "title": "Divergence Detector",
            "prompt": "Write `diverged(commits, a, b)` returning true when NEITHER commit is an ancestor of the other (their histories have split). Use your reachability logic conceptually: a is an ancestor of b (or equal) → false; same for b over a; otherwise true.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function diverged(commits, a, b) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "linear history never diverges",
                    "code": fn_wrap("diverged", "diverged") + "\nconst cs = { C: \"B\", B: \"A\", A: null };\nif (diverged(cs, \"A\", \"C\")) throw new Error(\"A is an ancestor of C.\");\nif (diverged(cs, \"C\", \"B\")) throw new Error(\"Same line of history.\");\nif (diverged(cs, \"C\", \"C\")) throw new Error(\"Equal commits are not diverged.\");",
                    "hint": "Walk ancestors of each side; check membership in the other's set.",
                },
                {
                    "name": "branch points diverge",
                    "code": fn_wrap("diverged", "diverged") + "\nconst cs = { B: \"A\", A: null, D: \"B\", E: \"B\", F: \"E\" };\nif (!diverged(cs, \"D\", \"F\")) throw new Error(\"D and F split at B.\");\nif (diverged(cs, \"B\", \"D\")) throw new Error(\"B is the merge-base of D.\");\nif (diverged(cs, \"B\", \"A\")) throw new Error(\"B descends from A.\");",
                    "hint": "Compute the ancestor set of each; neither contains the other's start => diverged.",
                },
            ],
        },
        {
            "id": "i2-bisect",
            "title": "Bisect Simulator",
            "prompt": "`bisect(commits, isBad)` — commits is an ordered array of ids oldest-first; isBad(id) returns a boolean. Simulate binary search: probe the middle, discard the half that cannot contain the FIRST bad commit, repeat. Return the id of the first bad commit (probe count must not exceed ceil(log2(n)) + 2 — efficiency matters).",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function bisect(commits, isBad) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "finds the first bad commit",
                    "code": fn_wrap("bisect", "bisect") + "\nconst cs = [\"c1\", \"c2\", \"c3\", \"c4\", \"c5\", \"c6\", \"c7\", \"c8\"];\nconst badAt = (n) => (id) => Number(id.slice(1)) >= n;\nif (bisect(cs, badAt(6)) !== \"c6\") throw new Error(\"Found c6, the first bad one.\");\nif (bisect(cs, badAt(1)) !== \"c1\") throw new Error(\"Everything bad => c1.\");",
                    "hint": "Classic binary search on the good/bad boundary.",
                },
                {
                    "name": "probes logarithmically, not linearly",
                    "code": fn_wrap("bisect", "bisect") + "\nlet probes = 0;\nconst cs = Array.from({ length: 1024 }, (_, i) => \"c\" + (i + 1));\nconst found = bisect(cs, (id) => { probes++; return Number(id.slice(1)) >= 777; });\nif (found !== \"c777\") throw new Error(\"Correct answer first.\");\nif (probes > 12) throw new Error(\"1024 commits need ~10 probes, not 777.\");",
                    "hint": "Each probe must halve the candidate range.",
                },
            ],
        },
    ],
    {
        "i2-commit-reach": {
            "title": "Khả năng với tới",
            "prompt": "Cho `commits` — map id → id cha (null với root) — và một id đích, trả về mảng TẤT CẢ id tổ tiên với tới được từ đích (bao gồm chính nó), sắp xếp cũ-trước-mới (đi tới root rồi reverse).",
            "tests": [
                {"name": "đi theo chuỗi cha tới root", "hint": "Đi theo chuỗi cha thu thập id, rồi reverse."},
                {"name": "xử lý root và liên kết không tồn tại", "hint": "Dừng khi cha là null hoặc id không có trong map."},
            ],
        },
        "i2-diverged": {
            "title": "Bộ phát hiện phân kỳ",
            "prompt": "Viết `diverged(commits, a, b)` trả về true khi KHÔNG commit nào là tổ tiên của commit kia (lịch sử đã tách). Dùng logic khả năng với tới: a là tổ tiên của b (hoặc bằng) → false; ngược lại với b; còn lại là true.",
            "tests": [
                {"name": "lịch sử tuyến tính không bao giờ phân kỳ", "hint": "Đi bộ tập tổ tiên của mỗi phía; kiểm tra thuộc tính trong tập của bên kia."},
                {"name": "điểm tách branch là phân kỳ", "hint": "Tính tập tổ tiên của mỗi bên; không tập nào chứa điểm bắt đầu của bên kia => phân kỳ."},
            ],
        },
        "i2-bisect": {
            "title": "Mô phỏng Bisect",
            "prompt": "`bisect(commits, isBad)` — commits là mảng id xếp cũ-trước-mới; isBad(id) trả về boolean. Mô phỏng tìm kiếm nhị phân: thăm giữa, loại nửa không thể chứa commit xấu ĐẦU TIÊN, lặp lại. Trả về id commit xấu đầu tiên (số lần thăm không vượt ceil(log2(n)) + 2 — hiệu quả là yêu cầu).",
            "tests": [
                {"name": "tìm được commit xấu đầu tiên", "hint": "Tìm kiếm nhị phân kinh điển trên biên tốt/xấu."},
                {"name": "thăm theo logarit, không tuyến tính", "hint": "Mỗi lần thăm phải chia đôi khoảng ứng viên."},
            ],
        },
    },
    [
        ["i2-commit-reach", "function reachable(commits, target) {\n  const chain = [];\n  let cur = target;\n  while (cur && commits[cur] !== undefined) {\n    chain.push(cur);\n    cur = commits[cur];\n  }\n  return chain.reverse();\n}", "function reachable(commits, target) {\n  return Object.keys(commits);\n}"],
        ["i2-diverged", "function diverged(commits, a, b) {\n  const anc = (t) => {\n    const s = new Set();\n    let cur = t;\n    while (cur && commits[cur] !== undefined) { s.add(cur); cur = commits[cur]; }\n    return s;\n  };\n  const sa = anc(a), sb = anc(b);\n  return !sa.has(b) && !sb.has(a);\n}", "function diverged(commits, a, b) {\n  return a !== b;\n}"],
        ["i2-bisect", "function bisect(commits, isBad) {\n  let lo = 0, hi = commits.length - 1;\n  while (lo < hi) {\n    const mid = Math.floor((lo + hi) / 2);\n    if (isBad(commits[mid])) hi = mid; else lo = mid + 1;\n  }\n  return commits[lo];\n}", "function bisect(commits, isBad) {\n  return commits.find(isBad);\n}"],
    ],
)

# ── branching-practice ──────────────────────────────────────────────────────
write_practice(
    MOD, "branching-practice",
    "Branch Naming & Flow — Practice",
    "Enforce a branching convention in code: classify branch names, validate a GitHub Flow sequence, and flag long-lived branches.",
    "Đặt tên branch & Flow — Luyện tập",
    "Áp đặt quy ước branch bằng code: phân loại tên branch, kiểm tra chuỗi GitHub Flow hợp lệ, và gắn cờ branch sống quá lâu.",
    "branching-strategies", 15, "intermediate",
    [
        {
            "id": "i2-branch-classify",
            "title": "Branch Classifier",
            "prompt": "Write `classifyBranch(name)` — branches follow `<type>/<kebab-desc>` where type ∈ feat|fix|chore|docs|refactor|test. Return \"feature\" for feat/fix branches, \"maintenance\" for chore/docs/test/refactor, and null for anything malformed (missing slash, bad type, spaces, uppercase).",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function classifyBranch(name) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "classifies valid branches",
                    "code": fn_wrap("classifyBranch", "classifyBranch") + "\nif (classifyBranch(\"feat/search-filters\") !== \"feature\") throw new Error(\"feat => feature.\");\nif (classifyBranch(\"fix/cart-total\") !== \"feature\") throw new Error(\"fix => feature.\");\nif (classifyBranch(\"chore/deps-bump\") !== \"maintenance\") throw new Error(\"chore => maintenance.\");\nif (classifyBranch(\"docs/readme\") !== \"maintenance\") throw new Error(\"docs => maintenance.\");",
                    "hint": "Split on the first '/', switch on the type.",
                },
                {
                    "name": "rejects malformed names",
                    "code": fn_wrap("classifyBranch", "classifyBranch") + "\nif (classifyBranch(\"feature-no-slash\") !== null) throw new Error(\"No slash => null.\");\nif (classifyBranch(\"hotfix/thing\") !== null) throw new Error(\"Unknown type => null.\");\nif (classifyBranch(\"feat/Has Spaces\") !== null) throw new Error(\"Spaces are not kebab.\");\nif (classifyBranch(\"FEAT/thing\") !== null) throw new Error(\"Types are lowercase.\");\nif (classifyBranch(\"feat/\") !== null) throw new Error(\"Empty description => null.\");",
                    "hint": "Whitelist the type list; validate the description is non-empty kebab-case.",
                },
            ],
        },
        {
            "id": "i2-flow-validate",
            "title": "Flow Validator",
            "prompt": "A GitHub Flow session is a list of events: \"branch\", \"commit\", \"push\", \"pr\", \"merge\". Write `validateFlow(events)` returning true only for a valid session: starts with exactly one \"branch\", at least one \"commit\" and \"push\" before the \"pr\", exactly one \"pr\", and \"merge\" last (if present). Order violations => false.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function validateFlow(events) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "accepts well-formed sessions",
                    "code": fn_wrap("validateFlow", "validateFlow") + "\nif (!validateFlow([\"branch\", \"commit\", \"push\", \"pr\", \"merge\"])) throw new Error(\"The canonical flow.\");\nif (!validateFlow([\"branch\", \"commit\", \"commit\", \"push\", \"pr\"])) throw new Error(\"Merge is optional; multiple commits fine.\");",
                    "hint": "Track what you've seen; each event has allowed predecessors.",
                },
                {
                    "name": "rejects out-of-order sessions",
                    "code": fn_wrap("validateFlow", "validateFlow") + "\nif (validateFlow([\"commit\", \"branch\", \"pr\"])) throw new Error(\"Must branch before committing.\");\nif (validateFlow([\"branch\", \"pr\", \"push\"])) throw new Error(\"Push before PR.\");\nif (validateFlow([\"branch\", \"commit\", \"pr\", \"merge\", \"commit\"])) throw new Error(\"Nothing after merge.\");\nif (validateFlow([\"branch\", \"pr\"])) throw new Error(\"A PR needs commits and a push.\");",
                    "hint": "A simple state machine: branch → commit+ → push → pr → merge?.",
                },
            ],
        },
        {
            "id": "i2-stale-branches",
            "title": "Stale Branch Report",
            "prompt": "Given `branches` — array of { name, ageDays, ahead } (ahead = commits main doesn't have) — write `staleReport(branches)`: return names of branches that are stale, where stale = ageDays > 14 AND ahead > 5. Sort alphabetically. This is the exact check a bot runs on real repos.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function staleReport(branches) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "flags only genuinely stale branches",
                    "code": fn_wrap("staleReport", "staleReport") + "\nconst bs = [\n  { name: \"feat/old-big\", ageDays: 30, ahead: 9 },\n  { name: \"feat/fresh\", ageDays: 2, ahead: 3 },\n  { name: \"fix/tiny\", ageDays: 20, ahead: 1 },\n];\nconst out = staleReport(bs);\nif (out.length !== 1 || out[0] !== \"feat/old-big\") throw new Error(\"Only old AND big branches are stale.\");",
                    "hint": "Filter with both conditions.",
                },
                {
                    "name": "sorts output alphabetically",
                    "code": fn_wrap("staleReport", "staleReport") + "\nconst bs = [\n  { name: \"feat/zeta\", ageDays: 20, ahead: 6 },\n  { name: \"feat/alpha\", ageDays: 20, ahead: 6 },\n];\nif (staleReport(bs).join(\",\") !== \"feat/alpha,feat/zeta\") throw new Error(\"Alphabetical, not input order.\");",
                    "hint": "sort() after filter.",
                },
            ],
        },
    ],
    {
        "i2-branch-classify": {
            "title": "Bộ phân loại branch",
            "prompt": "Viết `classifyBranch(name)` — branch theo dạng `<type>/<kebab-desc>` với type ∈ feat|fix|chore|docs|refactor|test. Trả về \"feature\" cho branch feat/fix, \"maintenance\" cho chore/docs/test/refactor, và null cho mọi tên sai dạng (thiếu dấu /, type lạ, có khoảng trắng, chữ hoa).",
            "tests": [
                {"name": "phân loại branch hợp lệ", "hint": "Tách ở '/' đầu tiên, switch trên type."},
                {"name": "từ chối tên sai dạng", "hint": "Danh sách type dạng whitelist; mô tả phải là kebab-case khác rỗng."},
            ],
        },
        "i2-flow-validate": {
            "title": "Trình kiểm tra Flow",
            "prompt": "Một phiên GitHub Flow là danh sách sự kiện: \"branch\", \"commit\", \"push\", \"pr\", \"merge\". Viết `validateFlow(events)` trả về true chỉ khi phiên hợp lệ: bắt đầu bằng đúng một \"branch\", có ít nhất một \"commit\" và \"push\" trước \"pr\", đúng một \"pr\", và \"merge\" đứng cuối (nếu có). Vi phạm thứ tự => false.",
            "tests": [
                {"name": "chấp nhận phiên đúng quy trình", "hint": "Theo dõi những gì đã thấy; mỗi sự kiện có các sự kiện đứng trước được phép."},
                {"name": "từ chối phiên sai thứ tự", "hint": "Một máy trạng thái đơn giản: branch → commit+ → push → pr → merge?."},
            ],
        },
        "i2-stale-branches": {
            "title": "Báo cáo branch ứ đọng",
            "prompt": "Cho `branches` — mảng { name, ageDays, ahead } (ahead = số commit mà main chưa có) — viết `staleReport(branches)`: trả về tên các branch ứ đọng, với ứ đọng = ageDays > 14 VÀ ahead > 5. Sắp xếp theo bảng chữ cái. Đây chính là check mà bot chạy trên repo thật.",
            "tests": [
                {"name": "chỉ gắn cờ branch thực sự ứ đọng", "hint": "Lọc với cả hai điều kiện."},
                {"name": "sắp xếp kết quả theo bảng chữ cái", "hint": "sort() sau khi filter."},
            ],
        },
    },
    [
        ["i2-branch-classify", "function classifyBranch(name) {\n  const types = [\"feat\", \"fix\", \"chore\", \"docs\", \"refactor\", \"test\"];\n  const i = name.indexOf(\"/\");\n  if (i === -1) return null;\n  const type = name.slice(0, i), desc = name.slice(i + 1);\n  if (!types.includes(type)) return null;\n  if (!desc || !/^[a-z0-9-]+$/.test(desc)) return null;\n  return type === \"feat\" || type === \"fix\" ? \"feature\" : \"maintenance\";\n}", "function classifyBranch(name) {\n  return name.includes(\"/\") ? \"feature\" : null;\n}"],
        ["i2-flow-validate", "function validateFlow(events) {\n  let branched = false, commits = 0, pushed = false, prs = 0, merged = false;\n  for (const e of events) {\n    if (merged) return false;\n    if (e === \"branch\") { if (branched) return false; branched = true; }\n    else if (e === \"commit\") { if (!branched) return false; commits++; }\n    else if (e === \"push\") { if (commits === 0) return false; pushed = true; }\n    else if (e === \"pr\") { if (!pushed) return false; prs++; if (prs > 1) return false; }\n    else if (e === \"merge\") { if (prs !== 1) return false; merged = true; }\n    else return false;\n  }\n  return branched && commits > 0 && pushed && prs === 1;\n}", "function validateFlow(events) {\n  return events[0] === \"branch\" && events.includes(\"pr\");\n}"],
        ["i2-stale-branches", "function staleReport(branches) {\n  return branches\n    .filter((b) => b.ageDays > 14 && b.ahead > 5)\n    .map((b) => b.name)\n    .sort();\n}", "function staleReport(branches) {\n  return branches.filter((b) => b.ageDays > 14).map((b) => b.name);\n}"],
    ],
)

# ── conflict-practice ───────────────────────────────────────────────────────
write_practice(
    MOD, "conflict-practice",
    "Conflict Resolution — Practice",
    "Parse conflict markers like Git does, produce clean resolutions, and validate a resolution is actually complete.",
    "Xử lý conflict — Luyện tập",
    "Phân tích conflict marker đúng cách Git làm, tạo bản xử lý sạch, và xác nhận bản xử lý thực sự hoàn tất.",
    "merge-vs-rebase", 18, "intermediate",
    [
        {
            "id": "i2-conflict-parse",
            "title": "Conflict Parser",
            "prompt": "A conflicted file contains lines `<<<<<<< HEAD`, `=======`, `>>>>>>> other`. Write `parseConflict(text)` returning `{ mine, theirs }` — the lines between the markers, joined with \"\\n\" (mine = HEAD side, theirs = the other side). Assume exactly one conflict block.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function parseConflict(text) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "extracts both sides",
                    "code": fn_wrap("parseConflict", "parseConflict") + "\nconst text = \"const a = 1;\\n<<<<<<< HEAD\\nconst total = subtotal * 1.1;\\n=======\\nconst total = subtotal + fee;\\n>>>>>>> main\\n\";\nconst { mine, theirs } = parseConflict(text);\nif (mine !== \"const total = subtotal * 1.1;\") throw new Error(\"HEAD side extracted.\");\nif (theirs !== \"const total = subtotal + fee;\") throw new Error(\"Incoming side extracted.\");",
                    "hint": "Split into lines; track which side you're inside of between the three markers.",
                },
                {
                    "name": "keeps multi-line sides intact",
                    "code": fn_wrap("parseConflict", "parseConflict") + "\nconst text = \"<<<<<<< HEAD\\nline1\\nline2\\n=======\\nx\\n>>>>>>> main\\n\";\nconst { mine, theirs } = parseConflict(text);\nif (mine !== \"line1\\nline2\") throw new Error(\"All HEAD lines, joined.\");\nif (theirs !== \"x\") throw new Error(\"Theirs side joined too.\");",
                    "hint": "Collect arrays of lines, join at the end.",
                },
            ],
        },
        {
            "id": "i2-conflict-resolve",
            "title": "Clean Resolver",
            "prompt": "Write `resolveConflictFile(text, chosen)` where chosen is \"mine\" or \"theirs\": return the file with the conflict block replaced by the chosen side's lines — markers removed, surrounding context preserved exactly.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function resolveConflictFile(text, chosen) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "replaces the block, keeps context",
                    "code": fn_wrap("resolveConflictFile", "resolveConflictFile") + "\nconst text = \"const a = 1;\\n<<<<<<< HEAD\\nconst t = 1.1;\\n=======\\nconst t = 2;\\n>>>>>>> main\\n// done\\n\";\nconst out = resolveConflictFile(text, \"theirs\");\nif (!out.startsWith(\"const a = 1;\\n\")) throw new Error(\"Context before is kept.\");\nif (!out.includes(\"const t = 2;\")) throw new Error(\"Chosen side is in.\");\nif (out.includes(\"<<<<<<<\") || out.includes(\"=======\")) throw new Error(\"No markers may survive.\");",
                    "hint": "Rebuild line by line, emitting context always and only the chosen side inside the block.",
                },
                {
                    "name": "choosing mine works symmetrically",
                    "code": fn_wrap("resolveConflictFile", "resolveConflictFile") + "\nconst text = \"<<<<<<< HEAD\\nA\\n=======\\nB\\n>>>>>>> main\\n\";\nconst out = resolveConflictFile(text, \"mine\");\nif (out !== \"A\\n\") throw new Error(\"Just the HEAD lines remain.\");",
                    "hint": "Same walk, emit the other array.",
                },
            ],
        },
        {
            "id": "i2-conflict-verify",
            "title": "Resolution Verifier",
            "prompt": "Real repos contain multiple conflicts. Write `hasUnresolved(text)` returning true if any conflict markers remain. Markers to detect: a line starting `<<<<<<< `, a line exactly `=======` (7 equals), a line starting `>>>>>>> `. A line of code containing `===` (like `if (a === b)`) is NOT a marker.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function hasUnresolved(text) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "detects leftover markers",
                    "code": fn_wrap("hasUnresolved", "hasUnresolved") + "\nif (!hasUnresolved(\"ok\\n<<<<<<< HEAD\\nx\\n\")) throw new Error(\"Opening marker detected.\");\nif (!hasUnresolved(\"x\\n=======\\ny\")) throw new Error(\"Separator detected.\");\nif (!hasUnresolved(\"x\\n>>>>>>> main\")) throw new Error(\"Closing marker detected.\");",
                    "hint": "Per line: startsWith checks for the arrows, exact equality for the separator.",
                },
                {
                    "name": "code that resembles markers passes",
                    "code": fn_wrap("hasUnresolved", "hasUnresolved") + "\nif (hasUnresolved(\"if (a === b) { return; }\\nconst s = \\\"=====\\\";\\n\")) throw new Error(\"Inline === is code, not a marker.\");\nif (hasUnresolved(\"clean file, no conflicts\")) throw new Error(\"Clean is clean.\");",
                    "hint": "The separator must be a line containing exactly seven '=' and nothing else.",
                },
            ],
        },
    ],
    {
        "i2-conflict-parse": {
            "title": "Bộ phân tích conflict",
            "prompt": "Một file bị conflict chứa các dòng `<<<<<<< HEAD`, `=======`, `>>>>>>> other`. Viết `parseConflict(text)` trả về `{ mine, theirs }` — các dòng nằm giữa các marker, nối bằng \"\\n\" (mine = phía HEAD, theirs = phía kia). Giả định đúng một khối conflict.",
            "tests": [
                {"name": "trích xuất cả hai phía", "hint": "Tách thành dòng; theo dõi mình đang ở phía nào giữa ba marker."},
                {"name": "giữ nguyên các phía nhiều dòng", "hint": "Thu thập mảng dòng, nối ở cuối."},
            ],
        },
        "i2-conflict-resolve": {
            "title": "Bộ xử lý sạch",
            "prompt": "Viết `resolveConflictFile(text, chosen)` với chosen là \"mine\" hoặc \"theirs\": trả về file có khối conflict được thay bằng các dòng của phía đã chọn — marker bị xóa, ngữ cảnh xung quanh giữ nguyên tuyệt đối.",
            "tests": [
                {"name": "thay khối, giữ ngữ cảnh", "hint": "Dựng lại từng dòng: luôn phát ngữ cảnh, và chỉ phát phía đã chọn trong khối."},
                {"name": "chọn mine hoạt động đối xứng", "hint": "Cùng cách đi bộ, phát mảng còn lại."},
            ],
        },
        "i2-conflict-verify": {
            "title": "Trình xác minh bản xử lý",
            "prompt": "Repo thật có nhiều conflict. Viết `hasUnresolved(text)` trả về true nếu còn marker nào. Marker cần phát hiện: dòng bắt đầu `<<<<<<< `, dòng đúng bằng `=======` (7 dấu =), dòng bắt đầu `>>>>>>> `. Dòng code chứa `===` (như `if (a === b)`) KHÔNG phải marker.",
            "tests": [
                {"name": "phát hiện marker còn sót", "hint": "Theo từng dòng: startsWith cho hai mũi tên, so sánh bằng tuyệt đối cho dấu phân cách."},
                {"name": "code giống marker vẫn pass", "hint": "Dấu phân cách phải là dòng chứa đúng bảy dấu '=' và không gì khác."},
            ],
        },
    },
    [
        ["i2-conflict-parse", "function parseConflict(text) {\n  const lines = text.split(\"\\n\");\n  let side = null, mine = [], theirs = [];\n  for (const l of lines) {\n    if (l.startsWith(\"<<<<<<<\")) { side = \"mine\"; continue; }\n    if (l === \"=======\") { side = \"theirs\"; continue; }\n    if (l.startsWith(\">>>>>>>\")) { side = null; continue; }\n    if (side === \"mine\") mine.push(l);\n    else if (side === \"theirs\") theirs.push(l);\n  }\n  return { mine: mine.join(\"\\n\"), theirs: theirs.join(\"\\n\") };\n}", "function parseConflict(text) {\n  return { mine: text, theirs: text };\n}"],
        ["i2-conflict-resolve", "function resolveConflictFile(text, chosen) {\n  const lines = text.split(\"\\n\");\n  let side = null;\n  const out = [];\n  for (const l of lines) {\n    if (l.startsWith(\"<<<<<<<\")) { side = \"mine\"; continue; }\n    if (l === \"=======\") { side = \"theirs\"; continue; }\n    if (l.startsWith(\">>>>>>>\")) { side = null; continue; }\n    if (side === null) out.push(l);\n    else if (side === chosen) out.push(l);\n  }\n  return out.join(\"\\n\");\n}", "function resolveConflictFile(text, chosen) {\n  return text.replace(/<<<<<<<[\\s\\S]*?>>>>>>>[^\\n]*\\n?/, \"\");\n}"],
        ["i2-conflict-verify", "function hasUnresolved(text) {\n  return text.split(\"\\n\").some((l) =>\n    l.startsWith(\"<<<<<<< \") || l === \"=======\" || l.startsWith(\">>>>>>> \")\n  );\n}", "function hasUnresolved(text) {\n  return text.includes(\"======\");\n}"],
    ],
)

# ── recovery-practice ───────────────────────────────────────────────────────
write_practice(
    MOD, "recovery-practice",
    "Recovery Drills — Practice",
    "Choose the right undo for realistic situations, and model reset's three modes precisely.",
    "Bài tập khôi phục — Luyện tập",
    "Chọn đúng cách hoàn tác cho các tình huống thực tế, và mô hình hóa chính xác ba chế độ của reset.",
    "recovering-commits", 15, "intermediate",
    [
        {
            "id": "i2-recovery-choice",
            "title": "Recovery Advisor",
            "prompt": "Write `advise({ pushed, othersHaveIt, hasUncommittedWork })` returning one of \"revert\", \"reset-soft\", \"stash-then-reset\", \"recreate\". Rules: pushed && othersHaveIt → \"revert\". !pushed && hasUncommittedWork → \"stash-then-reset\". !pushed → \"reset-soft\". pushed && !othersHaveIt && hasUncommittedWork → \"stash-then-reset\"; without uncommitted work → \"recreate\" (rebase/cherry-pick onto a fresh branch).",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function advise(o) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "shared history always reverts",
                    "code": fn_wrap("advise", "advise") + "\nif (advise({ pushed: true, othersHaveIt: true, hasUncommittedWork: false }) !== \"revert\") throw new Error(\"Others pulled it: revert only.\");\nif (advise({ pushed: true, othersHaveIt: true, hasUncommittedWork: true }) !== \"revert\") throw new Error(\"Shared is shared.\");",
                    "hint": "The first rule has no exceptions.",
                },
                {
                    "name": "local work respects the working tree",
                    "code": fn_wrap("advise", "advise") + "\nif (advise({ pushed: false, othersHaveIt: false, hasUncommittedWork: true }) !== \"stash-then-reset\") throw new Error(\"Protect uncommitted work first.\");\nif (advise({ pushed: false, othersHaveIt: false, hasUncommittedWork: false }) !== \"reset-soft\") throw new Error(\"Clean tree => soft reset.\");\nif (advise({ pushed: true, othersHaveIt: false, hasUncommittedWork: false }) !== \"recreate\") throw new Error(\"Pushed but private: rewrite on a fresh branch.\");",
                    "hint": "Order the checks exactly as the rules are written.",
                },
            ],
        },
        {
            "id": "i2-reset-modes",
            "title": "Reset Mode Simulator",
            "prompt": "Model reset as data. State = `{ commit, staged: [...], worktree: [...] }`. Write `applyReset(state, mode, n)` where n = how many commits to undo: \"soft\" → commit moves back n, staged and worktree unchanged; \"mixed\" → commit back n, worktree unchanged, staged becomes []; \"hard\" → commit back n, staged [], worktree []. Return the new state (do not mutate).",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function applyReset(state, mode, n) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "soft keeps everything staged",
                    "code": fn_wrap("applyReset", "applyReset") + "\nconst s = { commit: 3, staged: [\"a\"], worktree: [\"b\"] };\nconst out = applyReset(s, \"soft\", 1);\nif (out.commit !== 2 || out.staged.length !== 1 || out.worktree.length !== 1) throw new Error(\"soft: only HEAD moves.\");\nif (s.commit !== 3) throw new Error(\"Input not mutated.\");",
                    "hint": "Spread the state, override only what the mode changes.",
                },
                {
                    "name": "mixed and hard clear progressively",
                    "code": fn_wrap("applyReset", "applyReset") + "\nconst s = { commit: 3, staged: [\"a\"], worktree: [\"b\"] };\nconst m = applyReset(s, \"mixed\", 2);\nif (m.commit !== 1 || m.staged.length !== 0 || m.worktree.length !== 1) throw new Error(\"mixed: staged cleared, worktree kept.\");\nconst h = applyReset(s, \"hard\", 1);\nif (h.commit !== 2 || h.staged.length !== 0 || h.worktree.length !== 0) throw new Error(\"hard: everything cleared.\");",
                    "hint": "Three modes, three override sets.",
                },
            ],
        },
        {
            "id": "i2-reflog-walk",
            "title": "Reflog Walk",
            "prompt": "`reflog` is an array of { head, action } entries, newest FIRST. Write `lastGood(reflog, badAfterAction)` — walk the reflog and return the `head` of the newest entry at or before the LAST occurrence of an entry whose action is \"commit\". (In real terms: find the most recent committed state.) Return null if none.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function lastGood(reflog) {\n  // your code — return the head of the newest 'commit' entry\n}\n",
            "tests": [
                {
                    "name": "finds the most recent commit entry",
                    "code": fn_wrap("lastGood", "lastGood") + "\nconst log = [\n  { head: \"h3\", action: \"reset\" },\n  { head: \"h2\", action: \"commit\" },\n  { head: \"h1\", action: \"commit\" },\n];\nif (lastGood(log) !== \"h2\") throw new Error(\"h2 is the newest commit.\");",
                    "hint": "The array is newest-first: the first 'commit' you meet is the answer.",
                },
                {
                    "name": "null when nothing was committed",
                    "code": fn_wrap("lastGood", "lastGood") + "\nconst log = [{ head: \"h9\", action: \"stash\" }, { head: \"h8\", action: \"reset\" }];\nif (lastGood(log) !== null) throw new Error(\"No commits => null.\");",
                    "hint": "Default to null; only a 'commit' entry produces a value.",
                },
            ],
        },
    ],
    {
        "i2-recovery-choice": {
            "title": "Cố vấn khôi phục",
            "prompt": "Viết `advise({ pushed, othersHaveIt, hasUncommittedWork })` trả về một trong \"revert\", \"reset-soft\", \"stash-then-reset\", \"recreate\". Quy tắc: pushed && othersHaveIt → \"revert\". !pushed && hasUncommittedWork → \"stash-then-reset\". !pushed → \"reset-soft\". pushed && !othersHaveIt && hasUncommittedWork → \"stash-then-reset\"; không có công việc chưa commit → \"recreate\" (rebase/cherry-pick sang branch mới).",
            "tests": [
                {"name": "lịch sử dùng chung luôn revert", "hint": "Quy tắc đầu tiên không có ngoại lệ."},
                {"name": "công việc local tôn trọng working tree", "hint": "Sắp các check đúng thứ tự như quy tắc đã viết."},
            ],
        },
        "i2-reset-modes": {
            "title": "Mô phỏng chế độ reset",
            "prompt": "Mô hình hóa reset bằng dữ liệu. State = `{ commit, staged: [...], worktree: [...] }`. Viết `applyReset(state, mode, n)` với n = số commit cần hoàn tác: \"soft\" → commit lùi n, staged và worktree giữ nguyên; \"mixed\" → commit lùi n, worktree giữ nguyên, staged thành []; \"hard\" → commit lùi n, staged [], worktree []. Trả về state mới (không mutate đầu vào).",
            "tests": [
                {"name": "soft giữ mọi thứ trong staging", "hint": "Spread state, chỉ ghi đè những gì chế độ thay đổi."},
                {"name": "mixed và hard xóa theo cấp bậc", "hint": "Ba chế độ, ba bộ ghi đè."},
            ],
        },
        "i2-reflog-walk": {
            "title": "Đi bộ reflog",
            "prompt": "`reflog` là mảng mục { head, action }, MỚI NHẤT ĐỨNG TRƯỚC. Viết `lastGood(reflog)` — đi bộ reflog và trả về `head` của mục 'commit' mới nhất. (Nghĩa thực tế: tìm trạng thái đã commit gần nhất.) Trả về null nếu không có.",
            "tests": [
                {"name": "tìm mục commit mới nhất", "hint": "Mảng là mới-trước: mục 'commit' đầu tiên bạn gặp là đáp án."},
                {"name": "null khi chưa commit gì", "hint": "Mặc định null; chỉ mục 'commit' mới sinh ra giá trị."},
            ],
        },
    },
    [
        ["i2-recovery-choice", "function advise(o) {\n  if (o.pushed && o.othersHaveIt) return \"revert\";\n  if (!o.pushed && o.hasUncommittedWork) return \"stash-then-reset\";\n  if (!o.pushed) return \"reset-soft\";\n  if (o.hasUncommittedWork) return \"stash-then-reset\";\n  return \"recreate\";\n}", "function advise(o) {\n  return o.pushed ? \"revert\" : \"reset-soft\";\n}"],
        ["i2-reset-modes", "function applyReset(state, mode, n) {\n  const base = { commit: state.commit - n, staged: [...state.staged], worktree: [...state.worktree] };\n  if (mode === \"mixed\") base.staged = [];\n  if (mode === \"hard\") { base.staged = []; base.worktree = []; }\n  return base;\n}", "function applyReset(state, mode, n) {\n  return { commit: state.commit - n, staged: [], worktree: [] };\n}"],
        ["i2-reflog-walk", "function lastGood(reflog) {\n  const c = reflog.find((e) => e.action === \"commit\");\n  return c ? c.head : null;\n}", "function lastGood(reflog) {\n  return reflog[reflog.length - 1]?.head ?? null;\n}"],
    ],
)

# ── review-practice ─────────────────────────────────────────────────────────
write_practice(
    MOD, "review-practice",
    "Review & Conventional Commits — Practice",
    "Machine-check what machines can: conventional commit validity, semver impact, and PR size warnings.",
    "Review & Conventional Commits — Luyện tập",
    "Để máy kiểm những gì máy kiểm được: tính hợp lệ của conventional commit, tác động semver, và cảnh báo PR quá lớn.",
    "github-flow-review", 18, "intermediate",
    [
        {
            "id": "i2-commit-parse",
            "title": "Commit Message Parser",
            "prompt": "Write `parseCommit(msg)` for conventional commits `<type>(<scope>)?: <desc>`. Return `{ type, scope, breaking, desc }` — scope null when absent, breaking true when `!` precedes the colon or a BREAKING CHANGE footer exists (msg contains \"BREAKING CHANGE\"). Return null for malformed messages (no valid type, no colon, empty desc).",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function parseCommit(msg) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "parses the standard forms",
                    "code": fn_wrap("parseCommit", "parseCommit") + "\nconst p = parseCommit(\"feat(auth): add password reset\");\nif (p.type !== \"feat\" || p.scope !== \"auth\" || p.breaking !== false || p.desc !== \"add password reset\") throw new Error(\"Full form parsed.\");\nconst q = parseCommit(\"docs: update guide\");\nif (q.type !== \"docs\" || q.scope !== null) throw new Error(\"Scope-less form: scope is null.\");",
                    "hint": "One regex: /^(\\w+)(?:\\(([^)]*)\\))?!?: (.+)$/.",
                },
                {
                    "name": "flags breaking changes",
                    "code": fn_wrap("parseCommit", "parseCommit") + "\nif (parseCommit(\"feat!: new api\").breaking !== true) throw new Error(\"! marks breaking.\");\nif (parseCommit(\"fix: x\\n\\nBREAKING CHANGE: y\").breaking !== true) throw new Error(\"Footer marks breaking.\");\nif (parseCommit(\"fix: normal\")?.breaking !== false) throw new Error(\"Normal commits are not breaking.\");",
                    "hint": "Check the '!' before the colon OR search the whole message for the footer string.",
                },
                {
                    "name": "rejects malformed messages",
                    "code": fn_wrap("parseCommit", "parseCommit") + "\nif (parseCommit(\"updated stuff\") !== null) throw new Error(\"No type, no colon.\");\nif (parseCommit(\"feat\") !== null) throw new Error(\"Type alone is not a commit.\");\nif (parseCommit(\"feat:\" ) !== null) throw new Error(\"Empty description.\");\nif (parseCommit(\"blah: desc\") !== null) throw new Error(\"Unknown type => null.\");",
                    "hint": "Whitelist types: feat fix refactor perf test docs chore ci.",
                },
            ],
        },
        {
            "id": "i2-semver-impact",
            "title": "Release Notes Builder",
            "prompt": "Given an array of parsed commits `{ type, breaking }`, write `releaseBump(commits)`: return \"major\" if any commit is breaking, else \"minor\" if any type is \"feat\", else \"patch\" if any \"fix\", else null (no release).",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function releaseBump(commits) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "major wins over everything",
                    "code": fn_wrap("releaseBump", "releaseBump") + "\nconst cs = [{ type: \"feat\", breaking: false }, { type: \"fix\", breaking: true }];\nif (releaseBump(cs) !== \"major\") throw new Error(\"Any breaking change => major.\");",
                    "hint": "Priority order: major, minor, patch, null.",
                },
                {
                    "name": "minor, patch, and no-release cases",
                    "code": fn_wrap("releaseBump", "releaseBump") + "\nif (releaseBump([{ type: \"feat\", breaking: false }]) !== \"minor\") throw new Error(\"feat => minor.\");\nif (releaseBump([{ type: \"fix\", breaking: false }]) !== \"patch\") throw new Error(\"fix => patch.\");\nif (releaseBump([{ type: \"docs\", breaking: false }]) !== null) throw new Error(\"No user-facing change => null.\");",
                    "hint": "some() per level, in priority order.",
                },
            ],
        },
        {
            "id": "i2-pr-size",
            "title": "PR Size Gate",
            "prompt": "Write `prVerdict(files)` — files is an array of { path, additions, deletions }. Rules: a PR over 400 total changed lines gets \"split\"; one touching more than 10 files gets \"too-many-files\"; both conditions → \"split\" (size dominates); otherwise \"ok\". Changed lines = additions + deletions.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function prVerdict(files) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "size dominates files count",
                    "code": fn_wrap("prVerdict", "prVerdict") + "\nconst big = Array.from({ length: 12 }, () => ({ path: \"a\", additions: 50, deletions: 10 }));\nif (prVerdict(big) !== \"split\") throw new Error(\"720 lines across 12 files: split wins.\");",
                    "hint": "Compute both totals, check size first.",
                },
                {
                    "name": "file count and ok paths",
                    "code": fn_wrap("prVerdict", "prVerdict") + "\nconst many = Array.from({ length: 11 }, () => ({ path: \"a\", additions: 2, deletions: 0 }));\nif (prVerdict(many) !== \"too-many-files\") throw new Error(\"22 lines but 11 files.\");\nif (prVerdict([{ path: \"a\", additions: 100, deletions: 20 }]) !== \"ok\") throw new Error(\"120 lines, 1 file.\");",
                    "hint": "Then the file-count check, then default ok.",
                },
            ],
        },
    ],
    {
        "i2-commit-parse": {
            "title": "Bộ phân tích commit",
            "prompt": "Viết `parseCommit(msg)` cho conventional commit `<type>(<scope>)?: <desc>`. Trả về `{ type, scope, breaking, desc }` — scope null khi vắng, breaking true khi có `!` trước dấu hai chấm hoặc tồn tại footer BREAKING CHANGE (msg chứa \"BREAKING CHANGE\"). Trả về null cho message sai dạng (type không hợp lệ, thiếu hai chấm, desc rỗng).",
            "tests": [
                {"name": "phân tích các dạng chuẩn", "hint": "Một regex: /^(\\w+)(?:\\(([^)]*)\\))?!?: (.+)$/."},
                {"name": "gắn cờ breaking change", "hint": "Kiểm tra '!' trước hai chấm HOẶC tìm chuỗi footer trong toàn bộ message."},
                {"name": "từ chối message sai dạng", "hint": "Whitelist type: feat fix refactor perf test docs chore ci."},
            ],
        },
        "i2-semver-impact": {
            "title": "Trình dựng release notes",
            "prompt": "Cho mảng commit đã phân tích `{ type, breaking }`, viết `releaseBump(commits)`: trả về \"major\" nếu có commit breaking, không thì \"minor\" nếu có type \"feat\", không thì \"patch\" nếu có \"fix\", còn không thì null (không phát hành).",
            "tests": [
                {"name": "major thắng mọi thứ", "hint": "Thứ tự ưu tiên: major, minor, patch, null."},
                {"name": "các trường hợp minor, patch và không phát hành", "hint": "some() cho từng cấp, theo thứ tự ưu tiên."},
            ],
        },
        "i2-pr-size": {
            "title": "Cổng kiểm tra kích thước PR",
            "prompt": "Viết `prVerdict(files)` — files là mảng { path, additions, deletions }. Quy tắc: PR vượt 400 dòng thay đổi tổng cộng → \"split\"; PR chạm hơn 10 file → \"too-many-files\"; cả hai điều kiện → \"split\" (kích thước ưu tiên); còn lại \"ok\". Dòng thay đổi = additions + deletions.",
            "tests": [
                {"name": "kích thước ưu tiên hơn số file", "hint": "Tính cả hai tổng, kiểm tra kích thước trước."},
                {"name": "số file và đường ok", "hint": "Rồi check số file, mặc định là ok."},
            ],
        },
    },
    [
        ["i2-commit-parse", "function parseCommit(msg) {\n  const types = [\"feat\", \"fix\", \"refactor\", \"perf\", \"test\", \"docs\", \"chore\", \"ci\"];\n  const m = msg.match(/^(\\w+)(?:\\(([^)]*)\\))?!?: (.+)$/);\n  if (!m || !types.includes(m[1])) return null;\n  return {\n    type: m[1],\n    scope: m[2] || null,\n    breaking: /!:$/.test(msg.split(\"\\n\")[0].replace(/\\(.+\\)/, \"\")) || msg.includes(\"BREAKING CHANGE\"),\n    desc: m[3],\n  };\n}", "function parseCommit(msg) {\n  return { type: \"feat\", scope: null, breaking: false, desc: msg };\n}"],
        ["i2-semver-impact", "function releaseBump(commits) {\n  if (commits.some((c) => c.breaking)) return \"major\";\n  if (commits.some((c) => c.type === \"feat\")) return \"minor\";\n  if (commits.some((c) => c.type === \"fix\")) return \"patch\";\n  return null;\n}", "function releaseBump(commits) {\n  return commits.length ? \"minor\" : null;\n}"],
        ["i2-pr-size", "function prVerdict(files) {\n  const lines = files.reduce((n, f) => n + f.additions + f.deletions, 0);\n  if (lines > 400) return \"split\";\n  if (files.length > 10) return \"too-many-files\";\n  return \"ok\";\n}", "function prVerdict(files) {\n  return files.length > 10 ? \"too-many-files\" : \"ok\";\n}"],
    ],
)

# ── secrets-practice ────────────────────────────────────────────────────────
write_practice(
    MOD, "secrets-practice",
    "Secret Detection — Practice",
    "Build the scanner a pre-commit hook would run: recognize credential patterns, scan diffs, and verify gitignore coverage.",
    "Phát hiện secret — Luyện tập",
    "Dựng scanner mà pre-commit hook sẽ chạy: nhận diện mẫu credential, quét diff, và kiểm tra độ phủ của gitignore.",
    "secrets-and-env", 15, "intermediate",
    [
        {
            "id": "i2-secret-detect",
            "title": "Secret Pattern Scanner",
            "prompt": "Write `findSecrets(line)` returning an array of matches. Patterns: AWS access keys (AKIA followed by 16 uppercase letters/digits), GitHub tokens (ghp_ + 36+ chars), API keys (sk- + 20+ chars), and `name = \"value\"` assignments where name matches /key|token|secret|password/i case-insensitively and value is 8+ chars. Return the matched substrings in the order they appear.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function findSecrets(line) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "detects known credential formats",
                    "code": fn_wrap("findSecrets", "findSecrets")
                        + '\nconst out = findSecrets(\'const k = "AKIAIOSFODNN7EXAMPLE";\');\n'
                        + 'if (out.length !== 1 || out[0] !== "AKIAIOSFODNN7EXAMPLE") throw new Error("AWS key found.");\n'
                        + 'if (findSecrets(\'token = "ghp_abc123"\').length !== 1) throw new Error("Assignment with token name found.");\n',
                    "hint": "One regex per pattern, collect all matches.",
                },
                {
                    "name": "ignores safe code",
                    "code": fn_wrap("findSecrets", "findSecrets") + "\nif (findSecrets(\"const keyName = \\\"label\\\";\").length !== 0) throw new Error(\"Value too short to be a secret.\");\nif (findSecrets(\"user.passwordLabel = x\").length !== 0) throw new Error(\"No assignment literal, no secret.\");\nif (findSecrets(\"fetch(url)\").length !== 0) throw new Error(\"Ordinary code is clean.\");",
                    "hint": "The assignment rule needs BOTH a secret-ish name AND a long value.",
                },
            ],
        },
        {
            "id": "i2-diff-scan",
            "title": "Diff Scanner",
            "prompt": "Write `scanDiff(diff)` — diff is an array of lines. Only ADDED lines (starting with \"+\" but not \"+++\") can introduce secrets. Return an array of { line, secrets } for each added line where findSecrets-style detection finds anything, in order.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function scanDiff(diff) {\n  // your code — use the same detection rules as findSecrets\n}\n",
            "tests": [
                {
                    "name": "scans only added lines",
                    "code": fn_wrap("scanDiff", "scanDiff") + "\nconst d = [\n  \"+++ b/config.js\",\n  \"+const KEY = \\\"AKIAIOSFODNN7EXAMPLE\\\";\",\n  \"-const OLD = \\\"AKIAIOSFODNN7EXAMPLE\\\";\",\n  \" context line with AKIAIOSFODNN7EXAMPLE\",\n];\nconst out = scanDiff(d);\nif (out.length !== 1) throw new Error(\"Only the + line is new. Removed/context lines can't leak.\");\nif (out[0].secrets[0] !== \"AKIAIOSFODNN7EXAMPLE\") throw new Error(\"Secret extracted from the added line.\");",
                    "hint": "startsWith('+') && !startsWith('+++').",
                },
                {
                    "name": "multiple secrets on one line",
                    "code": fn_wrap("scanDiff", "scanDiff") + "\nconst d = [\"+const a = \\\"AKIAIOSFODNN7EXAMPLE\\\"; const b = \\\"ghp_\" + \"x\".repeat(36) + \"\\\";\"];\nconst out = scanDiff(d);\nif (out.length !== 1 || out[0].secrets.length !== 2) throw new Error(\"Both credentials on one line are found.\");",
                    "hint": "Run every pattern; concatenate matches.",
                },
            ],
        },
        {
            "id": "i2-gitignore-check",
            "title": "Gitignore Guard",
            "prompt": "Write `ignoreCovers(gitignoreLines, filePath)`: return true when any non-comment, non-empty pattern covers the path. Support: exact name (\".env\"), prefix glob (\".env*\"), directory prefix (\"config/\" covers \"config/local.json\" but NOT \"config-local.json\"), and wildcard (\"*.log\" covers \"a.log\", \"b/c.log\").",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function ignoreCovers(lines, filePath) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "exact and glob matches",
                    "code": fn_wrap("ignoreCovers", "ignoreCovers") + "\nconst gi = [\"# local secrets\", \".env\", \".env*\", \"dist/\"];\nif (!ignoreCovers(gi, \".env\")) throw new Error(\"Exact match.\");\nif (!ignoreCovers(gi, \".env.local\")) throw new Error(\"Glob match.\");\nif (!ignoreCovers(gi, \"dist/bundle.js\")) throw new Error(\"Directory prefix.\");",
                    "hint": "Skip lines starting with '#' or empty; then test each pattern shape.",
                },
                {
                    "name": "no accidental coverage",
                    "code": fn_wrap("ignoreCovers", "ignoreCovers") + "\nconst gi = [\"config/\", \"*.log\"];\nif (ignoreCovers(gi, \"config-local.json\")) throw new Error(\"config/ must not cover config-local.json.\");\nif (!ignoreCovers(gi, \"logs/a.log\")) throw new Error(\"Wildcard reaches nested files.\");\nif (ignoreCovers(gi, \"src/app.js\")) throw new Error(\"Unrelated files are not covered.\");",
                    "hint": "Directory pattern ends with '/': the path must contain that exact directory segment.",
                },
            ],
        },
    ],
    {
        "i2-secret-detect": {
            "title": "Bộ quét mẫu secret",
            "prompt": "Viết `findSecrets(line)` trả về mảng các match. Mẫu: AWS access key (AKIA + 16 ký tự hoa/chữ số), GitHub token (ghp_ + 36+ ký tự), API key (sk- + 20+ ký tự), và phép gán `name = \"value\"` khi name khớp /key|token|secret|password/i và value dài 8+ ký tự. Trả về các chuỗi khớp theo thứ tự xuất hiện.",
            "tests": [
                {"name": "phát hiện định dạng credential đã biết", "hint": "Một regex cho mỗi mẫu, thu thập mọi match."},
                {"name": "bỏ qua code an toàn", "hint": "Quy tắc gán cần CẢ tên giống secret VÀ value đủ dài."},
            ],
        },
        "i2-diff-scan": {
            "title": "Quét diff",
            "prompt": "Viết `scanDiff(diff)` — diff là mảng dòng. Chỉ dòng THÊM MỚI (bắt đầu \"+\" nhưng không phải \"+++\") mới có thể đưa secret vào. Trả về mảng { line, secrets } cho mỗi dòng thêm mới mà cơ chế dò kiểu findSecrets tìm thấy gì đó, theo thứ tự.",
            "tests": [
                {"name": "chỉ quét dòng thêm mới", "hint": "startsWith('+') && !startsWith('+++')."},
                {"name": "nhiều secret trên một dòng", "hint": "Chạy mọi mẫu; nối các match."},
            ],
        },
        "i2-gitignore-check": {
            "title": "Trình canh gác gitignore",
            "prompt": "Viết `ignoreCovers(lines, filePath)`: trả về true khi bất kỳ mẫu nào (không phải comment, không rỗng) bao phủ đường dẫn. Hỗ trợ: tên chính xác (\".env\"), glob tiền tố (\".env*\"), thư mục (\"config/\" bao phủ \"config/local.json\" nhưng KHÔNG bao phủ \"config-local.json\"), và wildcard (\"*.log\" bao phủ \"a.log\", \"b/c.log\").",
            "tests": [
                {"name": "khớp chính xác và glob", "hint": "Bỏ qua dòng bắt đầu '#' hoặc rỗng; rồi thử từng dạng mẫu."},
                {"name": "không bao phủ nhầm", "hint": "Mẫu thư mục kết thúc '/': đường dẫn phải chứa đúng segment thư mục đó."},
            ],
        },
    },
    [
        ["i2-secret-detect", "function findSecrets(line) {\n  const pats = [\n    /AKIA[A-Z0-9]{16}/g,\n    /ghp_[\\w]{36,}/g,\n    /sk-[\\w-]{20,}/g,\n    /(?:key|token|secret|password)\\s*=\\s*\"([^\"]{8,})\"/gi,\n  ];\n  const out = [];\n  for (const re of pats) {\n    let m;\n    while ((m = re.exec(line)) !== null) out.push(m[0]);\n  }\n  return out;\n}", "function findSecrets(line) {\n  return line.includes(\"key\") ? [line] : [];\n}"],
        ["i2-diff-scan", "function scanDiff(diff) {\n  const out = [];\n  for (const line of diff) {\n    if (line.startsWith(\"+\") && !line.startsWith(\"+++\")) {\n      const secrets = findSecrets(line.slice(1));\n      if (secrets.length) out.push({ line, secrets });\n    }\n  }\n  return out;\n}\n\nfunction findSecrets(line) {\n  const pats = [\n    /AKIA[A-Z0-9]{16}/g,\n    /ghp_[\\w]{36,}/g,\n    /sk-[\\w-]{20,}/g,\n    /(?:key|token|secret|password)\\s*=\\s*\"([^\"]{8,})\"/gi,\n  ];\n  const out = [];\n  for (const re of pats) {\n    let m;\n    while ((m = re.exec(line)) !== null) out.push(m[0]);\n  }\n  return out;\n}", "function scanDiff(diff) {\n  return diff.filter((l) => l.startsWith(\"+\")).map((line) => ({ line, secrets: [line] }));\n}"],
        ["i2-gitignore-check", "function ignoreCovers(lines, filePath) {\n  for (const raw of lines) {\n    const p = raw.trim();\n    if (!p || p.startsWith(\"#\")) continue;\n    if (p.endsWith(\"/\")) {\n      if (filePath.includes(\"/\" + p) || filePath.startsWith(p)) return true;\n    } else if (p.startsWith(\"*\")) {\n      if (filePath.endsWith(p.slice(1))) return true;\n    } else if (p.includes(\"*\")) {\n      if (filePath.startsWith(p.replace(\"*\", \"\"))) return true;\n    } else if (p === filePath) return true;\n  }\n  return false;\n}", "function ignoreCovers(lines, filePath) {\n  return lines.some((p) => filePath.includes(p));\n}"],
    ],
)

print("Module 6 practices written.")
