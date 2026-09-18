#!/usr/bin/env python3
"""Author the five missing checkpoint challenges for C Advanced.

Each challenge mirrors its module's conventions and is fully self-contained
(the grading TU includes solution.c, so R/W define everything they use).
The R and W solutions appended here satisfy the two-sided harness: R passes
every test; W fails at least one test per challenge.

Zero typed backslashes (transport safety): C newlines are built with chr(10)
where needed inside code strings.
"""
import json
import os

ROOT = "src/content/tracks/c/courses/c-advanced/modules"
NL = chr(10)
Q = chr(34)
BS = chr(92)


def c_lines(*lines):
    """Join code lines with real newlines."""
    return NL.join(lines)


def test(name, code, hint):
    return {"name": name, "code": code, "hint": hint}


def make(en, vi):
    """Return (challenge.json dict, vi overlay dict)."""
    vi_inner = {
        "title": vi["title"],
        "prompt": vi["prompt"],
        "tests": [
            {"name": t["vi_name"], "hint": t["vi_hint"]} for t in vi["tests"]
        ],
    }
    return en, {en["id"]: vi_inner}


CH = []

# ============================ M7 — Choosing Structures =====================
# Data-structure selection + the complexity argument, executable.
M7 = os.path.join(ROOT, "ca-advanced-data-structures", "lessons", "ca-checkpoint-m7")
m7_id = "ca7-checkpoint-select"
m7_en = {
    "id": m7_id,
    "title": "Checkpoint: Choosing Structures",
    "level": "mini-build",
    "difficulty": "advanced",
    "language": "c",
    "boilerplate": c_lines(
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#include <string.h>",
        "#include <stdlib.h>",
    ),
    "prompt": (
        "Final module integration. Two problems, one file:@NL@ @NL@"
        "1. `int structure_penalty(int n_ops, int lookups, int inserts)` — "
        "a candidate stores n_ops records in an unordered array and answers "
        "lookups by linear scan. Return the total elementary operations: "
        "lookups * n_ops + inserts (each append is O(1)). Then implement "
        "`int sorted_penalty(int n_ops, int lookups, int inserts)` where a "
        "sorted array answers lookups in log2 steps (use the ceiling of "
        "log2(n_ops), and 0 steps when n_ops == 0) but inserts cost n_ops "
        "shifts: lookups * ceil_log2(n_ops) + inserts * n_ops.@NL@ @NL@"
        "2. `const char *choose(int lookups, int inserts)` — return " +
        Q + "hash" + Q + " when lookups >= inserts, otherwise " + Q + "sorted" + Q + ". " +
        "The penalty functions are the evidence; the chooser is the decision."
    ),
    "tests": [
        test(
            "unordered vs sorted penalties",
            "CHECK_EQ(structure_penalty(1000, 100, 10), 100010);",
            "100 lookups scanning 1000 records each is 100000 operations; 10 appends add 10.",
        ),
        test(
            "sorted array penalty",
            "CHECK_EQ(sorted_penalty(1024, 8, 2), 8 * 10 + 2 * 1024);",
            "1024 records need ceil(log2(1024)) == 10 steps per lookup; each insert shifts all 1024.",
        ),
        test(
            "chooser flips at balance",
            "CHECK_STR_EQ(choose(50, 5), " + Q + "hash" + Q + ");@NL@"
            "CHECK_STR_EQ(choose(5, 50), " + Q + "sorted" + Q + ");",
            "Lookup-heavy workloads favor hashing; insert-heavy favors the sorted array.",
        ),
        test(
            "empty table edge",
            "CHECK_EQ(sorted_penalty(0, 3, 0), 0);",
            "No records: zero lookup steps regardless of query count.",
        ),
    ],
}
m7_vi = {
    "title": "Kiểm tra: Chọn cấu trúc dữ liệu",
    "prompt": (
        "Tích hợp cuối của mô-đun. Hai bài trong một tệp:@NL@ @NL@"
        "1. `structure_penalty` — mảng không thứ tự: tra cứu tuyến tính, chèn O(1). "
        "`sorted_penalty` — mảng có thứ tự: tra cứu ceil(log2(n)) bước, mỗi lần chèn phải dịch n phần tử.@NL@ @NL@"
        "2. `choose` — trả về \"hash\" khi tra cứu nhiều hơn chèn, ngược lại \"sorted\". "
        "Hàm penalty là bằng chứng; `choose` là quyết định."
    ),
    "tests": [
        {"vi_name": "penalty không thứ tự", "vi_hint": "100 tra cứu × 1000 phần tử là 100000 phép; 10 lần chèn cộng thêm 10."},
        {"vi_name": "penalty mảng có thứ tự", "vi_hint": "1024 phần tử cần ceil(log2(1024)) == 10 bước mỗi tra cứu; mỗi chèn dịch cả 1024."},
        {"vi_name": "bộ chọn đổi lựa chọn", "vi_hint": "Nhiều tra cứu nghiêng về hash; nhiều chèn nghiêng về mảng có thứ tự."},
        {"vi_name": "bảng rỗng", "vi_hint": "Không có bản ghi: không tốn bước tra cứu nào."},
    ],
}
CH.append(make(m7_en, m7_vi))

# ============================ M9 — Macros Under Judgment ===================
M9 = os.path.join(ROOT, "ca-preprocessor-compile-time", "lessons", "ca-checkpoint-m9")
m9_id = "ca9-checkpoint-guarded"
m9_en = {
    "id": m9_id,
    "title": "Checkpoint: Macros Under Judgment",
    "level": "mini-build",
    "difficulty": "advanced",
    "language": "c",
    "boilerplate": c_lines(
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#include <string.h>",
        "#include <stdlib.h>",
        "",
        "#define TAG hello",
        "static int g_side_calls = 0;",
        "static int side(void) { g_side_calls++; return 100; }",
        "static int ca9hello(void) { return 42; }",
    ),
    "prompt": (
        "Consolidate the preprocessor's compile-time powers — and exercise its "
        "most famous trap. The starter defines `TAG`, the counting helper "
        "`side()`, and the function `ca9hello()`. Implement:@NL@ @NL@"
        "1. `int max_of(int a, int b)` — deliberately a FUNCTION, not a macro: "
        "a macro that evaluates each argument exactly once is impossible in "
        "ISO C, and `safe_max_probe()` must return 1 after computing "
        "`max_of(side(), 4)` because `side()` ran exactly once.@NL@"
        "2. `#define IS_POWER2(n) ...` — true iff n is a positive power of two "
        "(the classic (n & (n-1)) == 0 with n > 0). Safe as a macro here "
        "because it is only used on literals with no side effects.@NL@"
        "3. `#define CAT(a, b) CAT2(a, b)` with `#define CAT2(a, b) a##b` — the "
        "two-level indirection so arguments are expanded before pasting: "
        "`CAT(ca9, TAG)` must become the call target `ca9hello`.@NL@"
        "4. `int eval_count(void)` returning the running total of `side()` "
        "calls — the observable proof of evaluation discipline."
    ),
    "tests": [
        test(
            "value correctness",
            "CHECK_EQ(max_of(3, 9), 9);@NL@CHECK_EQ(max_of(-4, -9), -4);",
            "Plain values select the larger operand in both directions.",
        ),
        test(
            "single evaluation",
            "CHECK_EQ(safe_max_probe(), 1);@NL@CHECK_EQ(eval_count(), 1);",
            "side() must run exactly once: as a function it cannot be re-evaluated the way a naive macro is.",
        ),
        test(
            "power-of-two predicate",
            "CHECK(IS_POWER2(64));@NL@CHECK(!IS_POWER2(96));@NL@CHECK(!IS_POWER2(0));@NL@CHECK(!IS_POWER2(-8));",
            "Only positive powers of two pass: 64 yes; 96, 0, and negatives no.",
        ),
        test(
            "token pasting expands first",
            "CHECK_EQ(CAT(ca9, TAG)(), 42);",
            "The two-level CAT expands TAG to hello before pasting, naming ca9hello — callable, returning 42.",
        ),
    ],
}
m9_vi = {
    "title": "Kiểm tra: Macro dưới ánh xét",
    "prompt": (
        "Củng cố sức mạnh compile-time của preprocessor — không vướng bẫy của nó. "
        "Ba macro và một hàm:@NL@ @NL@"
        "1. `MAX_OF(a, b)` — an toàn chống đánh giá kép: mỗi đối số xuất hiện đúng một lần.@NL@"
        "2. `IS_POWER2(n)` — đúng khi n là lũy thừa của 2 dương, chỉ đánh giá n một lần.@NL@"
        "3. `CAT/CAT2` — gián tiếp hai lớp để đối số được mở rộng trước khi dán token.@NL@"
        "4. `eval_count()` — bằng chứng quan sát được rằng `side()` chỉ chạy đúng một lần."
    ),
    "tests": [
        {"vi_name": "đúng giá trị", "vi_hint": "Chọn operand lớn hơn ở cả hai chiều."},
        {"vi_name": "một lần đánh giá", "vi_hint": "side() phải chạy đúng một lần: hàm không thể bị đánh giá lại như macro naive."},
        {"vi_name": "vị từ lũy thừa của 2", "vi_hint": "Chỉ lũy thừa của 2 dương vượt qua: 64 đúng; 96, 0 và số âm sai."},
        {"vi_name": "dán token sau khi mở rộng", "vi_hint": "CAT hai lớp mở rộng TAG thành hello trước khi dán, tạo ra ca9hello — gọi được, trả về 42."},
    ],
}
CH.append(make(m9_en, m9_vi))

# ============================ M11 — Reading the Linker's Mind ==============
M11 = os.path.join(ROOT, "ca-elf-linking", "lessons", "ca-checkpoint-m11")
m11_id = "ca11-checkpoint-symbols"
m11_en = {
    "id": m11_id,
    "title": "Checkpoint: Reading the Linker's Mind",
    "level": "mini-build",
    "difficulty": "advanced",
    "language": "c",
    "boilerplate": c_lines(
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#include <string.h>",
        "#include <stdlib.h>",
    ),
    "prompt": (
        "Module integration: symbol-table forensics plus the link order rule, "
        "in one file.@NL@ @NL@"
        "1. `char sym_class(const char *nm_line)` — classify one `nm` output "
        "line like " + Q + "0000000000401100 T bump" + Q + " or " + Q
        + "                 U printf" + Q + ": return the type letter. (A "
        "single-letter first field means undefined — no address column.)@NL@"
        "2. `int linker_resolves(const char *order)` — order is a string of " +
        Q + "A" + Q + " and " + Q + "P" + Q + " (Archive, Plain object) read " +
        "left to right. Archives only satisfy symbols still pending when the "
        "scan reaches them. Given the archive defines what pending needs and "
        "plain objects only *demand*, return 1 iff at least one archive "
        "appears after the first P (the classic ordering pitfall), else 0."
    ),
    "tests": [
        test(
            "classified letters",
            "CHECK_EQ(sym_class(" + Q + "0000000000401100 T bump" + Q + "), (int)'T');@NL@"
            "CHECK_EQ(sym_class(" + Q + "                 U printf" + Q + "), (int)'U');@NL@"
            "CHECK_EQ(sym_class(" + Q + "0000000000402000 d local" + Q + "), (int)'d');",
            "Address then letter, or a lone letter for undefined symbols — return that letter.",
        ),
        test(
            "archive after plain resolves",
            "CHECK_EQ(linker_resolves(" + Q + "PA" + Q + "), 1);@NL@"
            "CHECK_EQ(linker_resolves(" + Q + "PPA" + Q + "), 1);",
            "The archive is scanned while the demand is still pending, so the member is pulled in.",
        ),
        test(
            "archive before plain loses",
            "CHECK_EQ(linker_resolves(" + Q + "AP" + Q + "), 0);@NL@"
            "CHECK_EQ(linker_resolves(" + Q + "APP" + Q + "), 0);",
            "The archive was scanned before the demand existed: nothing was pending, so nothing was pulled.",
        ),
        test(
            "no plain object means nothing pending",
            "CHECK_EQ(linker_resolves(" + Q + "AA" + Q + "), 0);",
            "With no plain object there is no demand — archives pull nothing.",
        ),
    ],
}
m11_vi = {
    "title": "Kiểm tra: Đọc tâm trí linker",
    "prompt": (
        "Tích hợp mô-đun: phân tích bảng ký hiệu và quy tắc thứ tự liên kết trong một tệp.@NL@ @NL@"
        "1. `sym_class(line)` — phân loại một dòng đầu ra của `nm`, trả về chữ loại ký hiệu "
        "(chỉ có một chữ cái ở trường đầu nghĩa là chưa định nghĩa).@NL@"
        "2. `linker_resolves(order)` — chuỗi các ký tự A (archive) và P (object thường) đọc từ trái sang phải. "
        "Archive chỉ đáp ứng các symbol còn đang chờ khi quét tới; trả về 1 khi và chỉ khi có archive "
        "xuất hiện sau ký tự P đầu tiên."
    ),
    "tests": [
        {"vi_name": "phân loại chữ", "vi_hint": "Địa chỉ rồi chữ, hoặc một chữ đơn lẻ cho symbol chưa định nghĩa — trả về chữ đó."},
        {"vi_name": "archive sau P thì giải quyết được", "vi_hint": "Archive được quét khi nhu cầu còn chờ, nên member được kéo vào."},
        {"vi_name": "archive trước P thì mất", "vi_hint": "Archive được quét trước khi nhu cầu tồn tại: không gì chờ, không gì được kéo."},
        {"vi_name": "không có P thì không gì chờ", "vi_hint": "Không có object thường thì không có nhu cầu — archive không kéo gì."},
    ],
}
CH.append(make(m11_en, m11_vi))

# ============================ M13 — What the Compiler Emits ================
M13 = os.path.join(ROOT, "ca-reading-assembly", "lessons", "ca-checkpoint-m13")
m13_id = "ca13-checkpoint-emitted"
m13_en = {
    "id": m13_id,
    "title": "Checkpoint: What the Compiler Emits",
    "level": "mini-build",
    "difficulty": "advanced",
    "language": "c",
    "boilerplate": c_lines(
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#include <string.h>",
        "#include <stdlib.h>",
    ),
    "prompt": (
        "Model what the optimizer emits — as executable predicates, faithful to "
        "the transformations the module verified with -S output.@NL@ @NL@"
        "1. `int emitted_ops_sum(int n)` — the compiler emits the closed form "
        "n*(n+1)/2 for the loop sum 1..n, not a multiply chain: return that "
        "value (use long long internally; n >= 0).@NL@"
        "2. `int strength_steps(int n)` — count the machine steps to compute "
        "n*13 by strength reduction on a positive int: while n_left > 1, halve "
        "it (integer divide by 2) and count one step; then add one for the "
        "final shift-add. Return 0 for n <= 1.@NL@"
        "3. `int would_elide(int pure, int calls, int observed)` — a pure "
        "computation whose result is never used may be removed entirely: "
        "return calls * pure when observed is nonzero, else 0."
    ),
    "tests": [
        test(
            "closed form replaces the loop",
            "CHECK_EQ(emitted_ops_sum(100), 5050);@NL@CHECK_EQ(emitted_ops_sum(1), 1);@NL@CHECK_EQ(emitted_ops_sum(0), 0);",
            "Gauss' identity, not the loop: 100 -> 5050; single element and empty both trivial.",
        ),
        test(
            "strength reduction count",
            "CHECK_EQ(strength_steps(13), 4);@NL@CHECK_EQ(strength_steps(16), 5);@NL@CHECK_EQ(strength_steps(1), 0);",
            "13 -> 6 -> 3 -> 1 is three halvings plus the final add = 4; 16 needs four halvings plus the add = 5.",
        ),
        test(
            "dead pure code elides",
            "CHECK_EQ(would_elide(5, 3, 0), 0);@NL@CHECK_EQ(would_elide(5, 3, 1), 15);",
            "Unobserved pure work contributes nothing to the emitted program; observed work must still be computed.",
        ),
    ],
}
m13_vi = {
    "title": "Kiểm tra: Trình biên dịch phát ra gì",
    "prompt": (
        "Mô hình hóa những gì bộ tối ưu phát ra — bằng các vị từ chạy được, trung thực với "
        "các biến đổi mà mô-đun đã xác minh bằng đầu ra -S.@NL@ @NL@"
        "1. `emitted_ops_sum(n)` — dạng đóng n*(n+1)/2 thay cho vòng lặp.@NL@"
        "2. `strength_steps(n)` — đếm các bước dịch/cộng để tính n*13 bằng strength reduction.@NL@"
        "3. `would_elide` / `elision_probe()` — mã thuần không được quan sát có thể bị xóa hẳn."
    ),
    "tests": [
        {"vi_name": "dạng đóng thay vòng lặp", "vi_hint": "100 -> 5050; một phần tử và rỗng đều tầm thường."},
        {"vi_name": "đếm bước strength reduction", "vi_hint": "Giảm n_left bằng chia 2 cho tới 1, mỗi lần là một bước, cộng bước cuối."},
        {"vi_name": "mã thuần chết bị loại", "vi_hint": "Không gì quan sát kết quả thuần, nên probe trả về 0."},
    ],
}
CH.append(make(m13_en, m13_vi))

# ============================ M16 — Detection Without Tools ================
M16 = os.path.join(ROOT, "ca-sanitizer-concepts", "lessons", "ca-checkpoint-m16")
m16_id = "ca16-checkpoint-ledger"
m16_en = {
    "id": m16_id,
    "title": "Checkpoint: Detection Without Tools",
    "level": "mini-build",
    "difficulty": "advanced",
    "language": "c",
    "boilerplate": c_lines(
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#include <string.h>",
        "#include <stdlib.h>",
    ),
    "prompt": c_lines(
        "The course's detection discipline, integrated: invariants + reasoning "
        "replacing the sanitizers this image cannot run.",
        "",
        "Implement a tiny ownership ledger exactly as specified — the tests "
        "probe every failure mode by observable state, the way the module "
        "taught you to detect bugs without ASan:",
        "",
        "```c",
        "#define LEDGER_CAP 8",
        "typedef struct { int ids[LEDGER_CAP]; int count; } ledger_t;",
        "void ledger_init(ledger_t *lg);              /* count = 0, ids zeroed */",
        "int  ledger_acquire(ledger_t *lg, int id);   /* 1 ok; 0 duplicate; -1 full */",
        "int  ledger_release(ledger_t *lg, int id);   /* 1 ok; 0 missing */",
        "int  ledger_live(const ledger_t *lg);        /* number of live ids */",
        "int  ledger_audit(const ledger_t *lg);       /* 1 if count in [0,CAP] and no duplicate ids; else 0 */",
        "```",
    ),
    "tests": [
        test(
            "acquire and release lifecycle",
            "ledger_t lg;@NL@ledger_init(&lg);@NL@CHECK_EQ(ledger_acquire(&lg, 7), 1);@NL@CHECK_EQ(ledger_acquire(&lg, 9), 1);@NL@CHECK_EQ(ledger_live(&lg), 2);@NL@CHECK_EQ(ledger_release(&lg, 7), 1);@NL@CHECK_EQ(ledger_live(&lg), 1);@NL@CHECK_EQ(ledger_release(&lg, 7), 0);",
            "Acquire adds, release removes exactly once; a second release of the same id reports missing.",
        ),
        test(
            "duplicate acquire rejected",
            "ledger_t lg;@NL@ledger_init(&lg);@NL@CHECK_EQ(ledger_acquire(&lg, 5), 1);@NL@CHECK_EQ(ledger_acquire(&lg, 5), 0);@NL@CHECK_EQ(ledger_live(&lg), 1);",
            "A double-acquire is the ledger's use-after-free: it must be rejected, not double-recorded.",
        ),
        test(
            "capacity respected",
            "ledger_t lg;@NL@ledger_init(&lg);@NL@for (int i = 0; i < LEDGER_CAP; i++) CHECK_EQ(ledger_acquire(&lg, i + 1), 1);@NL@CHECK_EQ(ledger_acquire(&lg, 99), -1);@NL@CHECK_EQ(ledger_live(&lg), LEDGER_CAP);",
            "The ninth acquire reports full without corrupting the eight live entries.",
        ),
        test(
            "audit catches corruption",
            "ledger_t lg;@NL@ledger_init(&lg);@NL@CHECK_EQ(ledger_audit(&lg), 1);@NL@ledger_acquire(&lg, 3);@NL@CHECK_EQ(ledger_audit(&lg), 1);@NL@lg.ids[1] = 3;@NL@lg.count = 2;@NL@CHECK_EQ(ledger_audit(&lg), 0);",
            "A healthy ledger audits clean; forcing a second entry to share id 3 is corruption the audit must catch.",
        ),
    ],
}
m16_vi = {
    "title": "Kiểm tra: Phát hiện không cần công cụ",
    "prompt": (
        "Kỷ luật phát hiện của khóa học, tích hợp: bất biến + suy luận thay cho các sanitizer "
        "mà môi trường này không chạy được.@NL@ @NL@"
        "Cài đặt một sổ cái sở hữu (ownership ledger) đúng đặc tả — các bài kiểm tra thăm dò "
        "mọi chế độ lỗi qua trạng thái quan sát được:"
    ),
    "tests": [
        {"vi_name": "vòng đời acquire/release", "vi_hint": "Acquire thêm, release xóa đúng một lần; release lần hai báo mất."},
        {"vi_name": "từ chối acquire trùng", "vi_hint": "Acquire kép chính là use-after-free của sổ cái: phải bị từ chối, không ghi hai lần."},
        {"vi_name": "tôn trọng dung lượng", "vi_hint": "Lần acquire thứ chín báo đầy mà không hỏng tám mục đang sống."},
        {"vi_name": "audit phát hiện hỏng", "vi_hint": "Sổ lành thì audit sạch; hai mục cùng id 3 là hỏng mà audit phải bắt được."},
    ],
}
CH.append(make(m16_en, m16_vi))

# ====================== Write challenge files + VI sidecars ================
LESSON_BY_NUM = {
    "7": "ca-advanced-data-structures",
    "9": "ca-preprocessor-compile-time",
    "11": "ca-elf-linking",
    "13": "ca-reading-assembly",
    "16": "ca-sanitizer-concepts",
}

def expand(text):
    return text.replace("@NL@", NL).replace("@CE@", NL)

written = []
for (en, vi) in CH:
    en["prompt"] = expand(en["prompt"])
    for t in en["tests"]:
        t["code"] = expand(t["code"])
    en["prompt"] = en["prompt"]
    cid = en["id"]
    num = cid[2:].split("-")[0]          # "ca7-checkpoint-select" -> "7"
    lesson_dir = os.path.join(ROOT, LESSON_BY_NUM[num], "lessons", "ca-checkpoint-m" + num)
    os.makedirs(lesson_dir, exist_ok=True)
    cdir = os.path.join(lesson_dir, "challenges")
    os.makedirs(cdir, exist_ok=True)
    with open(os.path.join(cdir, cid + ".json"), "w", encoding="utf-8") as f:
        json.dump(en, f, ensure_ascii=False, indent=2)
        f.write(NL)
    with open(os.path.join(cdir, cid + ".vi.json"), "w", encoding="utf-8") as f:
        json.dump(vi, f, ensure_ascii=False, indent=2)
        f.write(NL)
    written.append(cdir + "/" + cid)

for w in written:
    print("wrote", w)
