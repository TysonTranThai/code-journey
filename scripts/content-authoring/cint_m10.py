#!/usr/bin/env python3
"""C — Intermediate — Module 10: cint-preproc.

The preprocessor as a language over the language: object/function-like
macros, argument hazards (double evaluation, precedence), token pasting,
_Static_assert compile-time contracts, and X-macro tables. House
conventions: ISO C only, self-contained tests, Ws are behavioral
near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-preproc"

write_module(
    M,
    "Preprocessor Mastery",
    "Macros as text surgery with sharp edges: evaluation hazards, hygiene, "
    "token pasting, and compile-time contracts.",
    "Làm chủ Preprocessor",
    "Macro là phẫu thuật văn bản với lưỡi sắc: nguy hiểm khi đánh giá, vệ "
    "sinh macro, dán token, và hợp đồng compile-time.",
    lessons=["macro-basics", "macro-hazards", "static-assert-xmacro", "cint-checkpoint-m10"],
    practices=["cint-p10-macros", "cint-p10-hygiene"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "macro-basics",
    "Object & Function-like Macros",
    "Text substitution before compilation: constants, do-while wrappers, "
    "and why macros live in a different phase than your code.",
    15,
    r"""
## Two kinds, one rule

Object-like macros define constants:

```c
#define MAX_USERS 100
#define ARRAY_LEN(a) (sizeof(a) / sizeof((a)[0]))
```

Function-like macros take arguments — and everything is *text*:

```c
#define SQUARE(x) ((x) * (x))
```

The one rule: **the preprocessor knows nothing about C.** It tokenizes
and substitutes. There is no type checking, no scope, no evaluation
order — just replacement, then the compiler sees the result. `ARRAY_LEN`
works on any array precisely because it compiles to
`sizeof(a)/sizeof(a[0])` — it is an expression, not a loop.

## The do-while wrapper

Multi-statement macros need a form that works inside `if/else` without
braces:

```c
#define LOG(msg) do { log_write((msg)); log_count++; } while (0)

if (bad)
    LOG("bad input");        /* expands to one STATEMENT, not a block
                                    that swallows the else */
else
    ...
```

Without `do { } while (0)`, the expanded `if (bad) { ...; count++; }`
plus a trailing `;` breaks the `else`. The wrapper is the professional
reflex — and `log_count++` here is a *side effect inside a macro*,
which is exactly how real code gets burned (next lesson).

## The compiler never sees your macro names

Debuggers step through expansions; error messages cite line 1 of the
#define. Prefer inline functions and enums where they suffice:

```c
enum { MAX_USERS = 100 };                 /* typed, scoped, debuggable */
static inline int square_int(int x) { return x * x; }   /* type-checked */
```

Macros remain the only tool for: token pasting, conditional compilation,
`ARRAY_LEN`, and anything that must work on *types*.
""",
"Macro object & function-like",
    "Thay thế văn bản trước khi compile: hằng, vỏ bọc do-while, và vì sao "
    "macro sống ở một pha khác với code của bạn.",
    r"""
## Hai loại, một quy tắc

Object-like macro định nghĩa hằng:

```c
#define MAX_USERS 100
#define ARRAY_LEN(a) (sizeof(a) / sizeof((a)[0]))
```

Function-like macro nhận tham số — và mọi thứ là *văn bản*:

```c
#define SQUARE(x) ((x) * (x))
```

Một quy tắc: **preprocessor không biết gì về C.** Nó tokenize và thay
thế. Không kiểm kiểu, không scope, không thứ tự đánh giá — chỉ thay thế,
rồi compiler nhìn kết quả. `ARRAY_LEN` chạy với mảng nào vì nó compile
thành `sizeof(a)/sizeof(a[0])` — là biểu thức, không phải vòng lặp.

## Vỏ bọc do-while

Macro nhiều câu lệnh cần dạng chạy được trong `if/else` không ngoặc:

```c
#define LOG(msg) do { log_write((msg)); log_count++; } while (0)

if (bad)
    LOG("bad input");        /* mở rộng thành MỘT câu lệnh, không phải
                                    khối nuốt else */
else
    ...
```

Không `do { } while (0)`, dạng mở rộng `if (bad) { ...; count++; }` cộng
dấu `;` đuôi làm gãy `else`. Vỏ bọc là phản xạ chuyên nghiệp — và
`log_count++` ở đây là *tác dụng phụ trong macro*, chính là cách code
thật bị đốt (bài sau).

## Compiler không bao giờ thấy tên macro

Debugger bước qua phần mở rộng; thông báo lỗi trích dòng 1 của #define.
Ưu tiên inline function và enum khi đủ:

```c
enum { MAX_USERS = 100 };                 /* có kiểu, có scope, debug được */
static inline int square_int(int x) { return x * x; }   /* kiểm kiểu */
```

Macro vẫn là công cụ duy nhất cho: dán token, biên dịch có điều kiện,
`ARRAY_LEN`, và bất cứ thứ gì phải chạy trên *kiểu*.
"""
)

write_lesson(
    M, "macro-hazards",
    "Evaluation Hazards & Hygiene",
    "Double evaluation, missing parens, and the argument that runs twice. "
    "Why MAX(a, b) has bitten every C codebase.",
    17,
    r"""
## The argument that runs twice

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int i = 0;
int m = MAX(i++, 5);      /* expands: ((i++) > (5) ? (i++) : (5)) */
```

`i++` appears twice in the expansion — the ternary evaluates the winner
a *second* time. Undefined behavior, wrong results, and it compiles
clean. The fix is not "more parens"; the argument must be evaluated
*exactly once*:

```c
/* GCC/clang statement-expression, NOT ISO C: */
/* ISO C honest alternative: a static inline function */
static inline int max_int(int a, int b) { return a > b ? a : b; }
```

Inline functions type-check, evaluate arguments once, and debug
normally — they are the default answer. Macros stay for cases where the
type must stay open (`MAX` on any numeric type) — and then the *contract
documented* is "arguments must be side-effect free."

## Precedence traps outside the macro

```c
#define DOUBLE(x) (x) + (x)      /* wrong at the seam */
int r = 2 * DOUBLE(3);           /* 2 * (3) + (3) == 9, not 12 */
```

Every macro body must be parenthesized *as a whole* too:
`#define DOUBLE(x) ((x) + (x))`. The rule is mechanical: wrap every
parameter occurrence and the entire expansion.

## Hygiene: names that escape

A macro's "local" names are not local — they can collide with the
caller's:

```c
#define SWAP(a, b) do { int tmp_ = a; a = b; b = tmp_; } while (0)
/* caller's variable named tmp_? silent corruption */
```

Convention: underscore-suffixed internal names (`tmp_`, `i_`) reduce —
never eliminate — collisions. Token pasting with unique names is the
next lesson's tool.
""",
"Nguy hiểm khi đánh giá & vệ sinh",
    "Đánh giá hai lần, thiếu ngoặc, và tham số chạy hai lần. Vì sao "
    "MAX(a, b) đã cắn mọi codebase C.",
    r"""
## Tham số chạy hai lần

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int i = 0;
int m = MAX(i++, 5);      /* mở rộng: ((i++) > (5) ? (i++) : (5)) */
```

`i++` xuất hiện hai lần trong phần mở rộng — ternary đánh giá bên thắng
*lần thứ hai*. Undefined behavior, kết quả sai, và compile sạch. Cách
chữa không phải "thêm ngoặc"; tham số phải được đánh giá *đúng một lần*:

```c
/* ISO C, câu trả lời trung thực: static inline function */
static inline int max_int(int a, int b) { return a > b ? a : b; }
```

Inline function kiểm kiểu, đánh giá tham số một lần, debug bình thường —
là câu trả lời mặc định. Macro còn lại cho trường hợp kiểu phải mở
(`MAX` trên mọi kiểu số) — và khi đó *hợp đồng được ghi rõ* là "tham số
phải không có tác dụng phụ."

## Bẫy độ ưu tiên ngoài mép macro

```c
#define DOUBLE(x) (x) + (x)      /* sai tại mép */
int r = 2 * DOUBLE(3);           /* 2 * (3) + (3) == 9, không phải 12 */
```

Thân macro phải được bọc ngoặc *tổng thể*:
`#define DOUBLE(x) ((x) + (x))`. Quy tắc máy móc: bọc mọi vị trí tham số
và toàn bộ phần mở rộng.

## Vệ sinh: tên thoát ra ngoài

Tên "cục bộ" của macro không cục bộ — chúng có thể đụng biến của caller:

```c
#define SWAP(a, b) do { int tmp_ = a; a = b; b = tmp_; } while (0)
/* caller có biến tên tmp_? hỏng âm thầm */
```

Quy ước: tên nội bộ có hậu tố gạch dưới (`tmp_`, `i_`) giảm — không loại
trừ — va chạm. Dán token với tên độc nhất là công cụ của bài sau.
"""
)

write_lesson(
    M, "static-assert-xmacro",
    "_Static_assert & X-Macros",
    "Compile-time contracts and the token-pasting table pattern that "
    "keeps parallel lists in lockstep.",
    16,
    r"""
## Fail the build, not the customer

`_Static_assert` (C11, no-message form in C23) checks a constant
expression at compile time:

```c
_Static_assert(sizeof(int) == 4, "protocol assumes 32-bit int");
_Static_assert(OTAB_CAP > 0 && (OTAB_CAP & (OTAB_CAP - 1)) == 0,
               "capacity must be a power of two");
```

When the assumption breaks — a new platform, a refactored constant —
the build fails with your message, at the site of the assumption. That
is the cheapest possible bug: one that never ships. Static asserts
document *invariants the compiler can check*, complementing the runtime
checks you already write.

## X-macros: one data, many views

The pattern keeps parallel lists (enum ↔ name ↔ table row) in lockstep
by defining the list once:

```c
/* commands.def — the single source of truth */
X(ADD,  cmd_add,  "adds")
X(SUB,  cmd_sub,  "subs")

/* the enum: */
#define X(id, fn, desc) CMD_##id,
enum cmd_id { CMD_NONE, X_ROWS CMD_COUNT };
#undef X

/* the dispatch table: */
#define X(id, fn, desc) { CMD_##id, fn, desc },
static const struct { int id; int (*fn)(int, int); const char *desc; }
CMDS[] = { X_ROWS };
#undef X
```

Add a command by editing **one file** — the enum, the table, and the
name-to-string helpers all update together, and forgetting one is
impossible because there is only one list. `#X` (stringize) and
`X##Y` (paste) are the token operators that make it work. Real codebases
use X-macros for opcodes, error codes, config keys — anywhere two or
more parallel lists would otherwise drift.

## #undef is part of the pattern

Each use-site defines `X`, uses it, then undefines. This keeps the
macro's scope one screen wide and makes accidental reuse a compile
error rather than a silent surprise.
""",
"_Static_assert & X-Macros",
    "Hợp đồng compile-time và mẫu bảng dán token giữ các danh sách song "
    "song đồng bộ.",
    r"""
## Fail build, không fail khách hàng

`_Static_assert` (C11) kiểm biểu thức hằng lúc compile:

```c
_Static_assert(sizeof(int) == 4, "protocol assumes 32-bit int");
_Static_assert(OTAB_CAP > 0 && (OTAB_CAP & (OTAB_CAP - 1)) == 0,
               "capacity must be a power of two");
```

Khi giả định gãy — platform mới, hằng bị refactor — build gãy với thông
điệp của bạn, ngay tại nơi giả định. Đó là bug rẻ nhất có thể: bug không
bao giờ ship. Static assert ghi *bất biến compiler kiểm được*, bổ sung
cho các kiểm runtime bạn đã viết.

## X-macros: một dữ liệu, nhiều góc nhìn

Mẫu giữ các danh sách song song (enum ↔ tên ↔ dòng bảng) đồng bộ bằng
cách định nghĩa danh sách đúng một lần:

```c
/* commands.def — nguồn sự thật duy nhất */
X(ADD,  cmd_add,  "adds")
X(SUB,  cmd_sub,  "subs")

/* enum: */
#define X(id, fn, desc) CMD_##id,
enum cmd_id { CMD_NONE, X_ROWS CMD_COUNT };
#undef X

/* bảng dispatch: */
#define X(id, fn, desc) { CMD_##id, fn, desc },
static const struct { int id; int (*fn)(int, int); const char *desc; }
CMDS[] = { X_ROWS };
#undef X
```

Thêm lệnh bằng cách sửa **một file** — enum, bảng, name-to-string cùng
cập nhật, và quên một nơi là bất khả vì chỉ có một danh sách. `#X`
(stringize) và `X##Y` (dán) là toán tử token khiến nó chạy. Codebase thật
dùng X-macro cho opcode, mã lỗi, config key — mọi nơi có từ hai danh sách
song song trở lên mà không được phép lệch nhau.

## #undef là một phần của mẫu

Mỗi nơi dùng định nghĩa `X`, dùng, rồi undefine. Điều này giữ scope của
macro trong một màn hình và biến việc tái dùng nhầm thành lỗi compile
thay vì bất ngờ âm thầm.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p10-macros",
    "Macro Gym",
    "Safe-by-construction macros: ARRAY_LEN, bounded helpers, do-while wrappers.",
    "Phòng gym macro",
    "Macro an toàn theo cấu trúc: ARRAY_LEN, helper có giới hạn, vỏ bọc do-while.",
    after_lesson="macro-hazards",
    minutes=24,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p10-macro-write",
            "Write the Safe Macros",
            """The boilerplate defines the macros under test. Your job is to
implement the FUNCTIONS that use them correctly — and one macro:

```c
/* provided (correct): */
#define ARRAY_LEN(a) (sizeof(a) / sizeof((a)[0]))
#define MAXI(a, b) ((a) > (b) ? (a) : (b))

/* implement the function: sum of array using ARRAY_LEN (no explicit n) */
long sum_all(const int *a, size_t n);
/* implement: clamp v into [lo, hi] using MAXI twice */
int clamp(int v, int lo, int hi);
/* implement THE MACRO (the boilerplate declares it for you to fill):
   runs stmt exactly once per call, usable in if/else without braces */
#define RUN_ONCE(stmt) ...
```

Careful: `ARRAY_LEN` only works on real arrays — `sum_all` takes a
pointer, which is why it needs `n`.""",
            C_PRELUDE + "\n#include <stddef.h>\n#define ARRAY_LEN(a) (sizeof(a) / sizeof((a)[0]))\n#define MAXI(a, b) ((a) > (b) ? (a) : (b))\nlong sum_all(const int *a, size_t n);\nint clamp(int v, int lo, int hi);\n#define RUN_ONCE(stmt) do { stmt; } while (0)\n",
            [
                (
                    "macros at their seams",
                    r"""
int a[] = {1, 2, 3, 4};
CHECK_EQ(ARRAY_LEN(a), 4);                    /* real array: works */
CHECK_EQ(sum_all(a, ARRAY_LEN(a)), 10);
CHECK_EQ(sum_all(a, 2), 3);
CHECK_EQ(sum_all(NULL, 0), 0);
CHECK_EQ(clamp(5, 0, 10), 5);
CHECK_EQ(clamp(-3, 0, 10), 0);
CHECK_EQ(clamp(42, 0, 10), 10);
int counter_ = 0;
RUN_ONCE(counter_ += 1);
RUN_ONCE(counter_ += 1);
CHECK_EQ(counter_, 2);
if (counter_ == 2)
    RUN_ONCE(counter_ += 10);
else
    counter_ = -1;                            /* must compile & run: else intact */
CHECK_EQ(counter_, 12);
""",
                    "sum_all walks n elements (ARRAY_LEN on a POINTER is sizeof(*)/sizeof(int) == 1 — the trap the prompt names). clamp: MAXI(v, lo) then MIN via MAXI trick or direct.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p10-macro-write": vi_challenge(
            "Viết macro an toàn",
            "Dùng ARRAY_LEN/MAXI đúng mép: sum_all(n), clamp, và RUN_ONCE dạng do-while.",
            [("macro tại mép", "ARRAY_LEN trên con trỏ là 1 — bẫy được nêu trong đề.")],
        ),
    },
    solutions=[
        (
            "cint-p10-macro-write",
            r"""
#include <stddef.h>
long sum_all(const int *a, size_t n) {
    if (!a) return 0;
    long s = 0;
    for (size_t i = 0; i < n; i++) s += a[i];
    return s;
}
int clamp(int v, int lo, int hi) {
    if (lo > hi) return lo;                 /* degenerate range: pick lo */
    int low = (v < lo) ? lo : v;            /* one side at a time avoids
                                               double-evaluation surprises */
    return (low > hi) ? hi : low;
}""",
            r"""
#include <stddef.h>
long sum_all(const int *a, size_t n) {
    if (!a) return 0;
    return ARRAY_LEN(a) * n;                /* wrong: ARRAY_LEN on a pointer is
                                                  sizeof(int*)/sizeof(int) == 2 on
                                                  64-bit — garbage multiplied in */
}
int clamp(int v, int lo, int hi) {
    return MAXI(lo, MAXI(v, hi));           /* wrong: MAX of all three — returns
                                                  hi for in-range values */
}""",
        ),
    ],
)

write_practice(
    M, "cint-p10-hygiene",
    "X-Macro & Assert Gym",
    "Token pasting tables and compile-time contracts.",
    "Phòng gym X-macro & assert",
    "Bảng dán token và hợp đồng compile-time.",
    after_lesson="static-assert-xmacro",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p10-xmacro",
            "Build the X-Macro Table",
            """The boilerplate defines a color table via X-macros:

```c
#define COLORS \\
  X(RED,    0xFF0000) \\
  X(GREEN,  0x00FF00) \\
  X(BLUE,   0x0000FF)
```

Implement the two views over it (the enum and lookup are YOURS to write
using `COLORS`):

```c
/* the enum must contain CLR_RED, CLR_GREEN, CLR_BLUE (via pasting),
   plus CLR_COUNT as the sentinel */
/* returns the enum value for name ("RED" -> CLR_RED), or -1 */
int clr_from_name(const char *name);
/* returns the hex value for the enum, or -1 */
long clr_hex(int clr);
```""",
            C_PRELUDE + "\n#include <stddef.h>\n#include <string.h>\n#define COLORS \\\n  X(RED,    0xFF0000) \\\n  X(GREEN,  0x00FF00) \\\n  X(BLUE,   0x0000FF)\n\n#define X(id, hex) CLR_##id,\nenum { COLORS CLR_COUNT };\n#undef X\n\nstatic const struct { const char *name; long hex; } CLR_TAB[] = {\n#define X(id, hex) { #id, hex },\nCOLORS\n#undef X\n};\n\nint clr_from_name(const char *name);\nlong clr_hex(int clr);\n",
            [
                (
                    "one list, two views",
                    r"""
CHECK_EQ(clr_from_name("RED"), 0);
CHECK_EQ(clr_from_name("GREEN"), 1);
CHECK_EQ(clr_from_name("BLUE"), 2);
CHECK_EQ(clr_from_name("PINK"), -1);
CHECK_EQ(clr_from_name(NULL), -1);
CHECK_EQ(clr_hex(0), 0xFF0000);
CHECK_EQ(clr_hex(2), 0x0000FF);
CHECK_EQ(clr_hex(-1), -1);
CHECK_EQ(clr_hex(CLR_COUNT), -1);
CHECK_EQ(CLR_COUNT, 3);
""",
                    "clr_from_name walks CLR_TAB with strcmp, returning the index; clr_hex bounds-checks then reads hex.",
                ),
            ],
        ),
        challenge(
            "cint-p10-assert",
            "Compile-Time Contracts",
            """The boilerplate contains `_Static_assert`s your code must not
violate — and functions that RELY on them. Implement:

```c
/* packs two nibbles into a byte — relies on the static assert that
   unsigned char is exactly 8 bits */
unsigned char pack_nibbles(unsigned lo, unsigned hi);
/* returns the table capacity; the static assert guarantees it is a
   power of two, so capacity-1 is a mask */
size_t tab_mask(void);
/* returns 1 if v is a power of two (v > 0), using the bit trick */
int is_pow2(size_t v);
```""",
            C_PRELUDE + "\n#include <stddef.h>\n_Static_assert(sizeof(unsigned char) * 8 == 8, \"byte is 8 bits\");\n#define TAB_CAP 16\n_Static_assert(TAB_CAP > 0 && (TAB_CAP & (TAB_CAP - 1)) == 0, \"power of two\");\nunsigned char pack_nibbles(unsigned lo, unsigned hi);\nsize_t tab_mask(void);\nint is_pow2(size_t v);\n",
            [
                (
                    "asserts hold, functions deliver",
                    r"""
CHECK_EQ(pack_nibbles(0xF, 0xA), 0xAF);
CHECK_EQ(pack_nibbles(0x0, 0x7), 0x70);
CHECK_EQ(tab_mask(), 15);
CHECK_EQ(is_pow2(1), 1);
CHECK_EQ(is_pow2(16), 1);
CHECK_EQ(is_pow2(0), 0);
CHECK_EQ(is_pow2(3), 0);
CHECK_EQ(is_pow2(6), 0);
""",
                    "pack: (hi << 4) | (lo & 0xF). mask: TAB_CAP - 1. pow2: v && !(v & (v-1)).",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p10-xmacro": vi_challenge(
            "Dựng bảng X-macro",
            "Dùng COLORS để cài clr_from_name (strcmp trong CLR_TAB) và clr_hex (bounds-check).",
            [("một danh sách, hai góc nhìn", "đi CLR_TAB, trả chỉ số; kiểm biên trước khi đọc hex.")],
        ),
        "cint-p10-assert": vi_challenge(
            "Hợp đồng compile-time",
            "Cài pack_nibbles, tab_mask (TAB_CAP-1), is_pow2 (bit trick).",
            [("assert giữ vững, hàm giao hàng", "(hi << 4) | (lo & 0xF); v && !(v & (v-1)).")],
        ),
    },
    solutions=[
        (
            "cint-p10-xmacro",
            r"""
#include <string.h>
#include <stddef.h>
int clr_from_name(const char *name) {
    if (!name) return -1;
    for (size_t i = 0; i < sizeof CLR_TAB / sizeof CLR_TAB[0]; i++)
        if (strcmp(CLR_TAB[i].name, name) == 0) return (int)i;
    return -1;
}
long clr_hex(int clr) {
    if (clr < 0 || (size_t)clr >= sizeof CLR_TAB / sizeof CLR_TAB[0]) return -1;
    return CLR_TAB[clr].hex;
}""",
            r"""
#include <string.h>
#include <stddef.h>
int clr_from_name(const char *name) {
    if (!name) return -1;
    for (size_t i = 0; i < sizeof CLR_TAB / sizeof CLR_TAB[0]; i++)
        if (strstr(CLR_TAB[i].name, name) != NULL) return (int)i;   /* wrong: substring
                                                  match — "R" wrongly resolves to RED */
    return -1;
}
long clr_hex(int clr) {
    if (clr < 0 || (size_t)clr >= sizeof CLR_TAB / sizeof CLR_TAB[0]) return -1;
    return CLR_TAB[clr].hex;
}""",
        ),
        (
            "cint-p10-assert",
            r"""
#include <stddef.h>
unsigned char pack_nibbles(unsigned lo, unsigned hi) {
    return (unsigned char)((hi << 4) | (lo & 0xFu));
}
size_t tab_mask(void) { return TAB_CAP - 1; }
int is_pow2(size_t v) { return v != 0 && (v & (v - 1)) == 0; }""",
            r"""
#include <stddef.h>
unsigned char pack_nibbles(unsigned lo, unsigned hi) {
    return (unsigned char)((hi << 4) | lo);    /* wrong: no mask — lo >= 16
                                                  bleeds bits into the high nibble */
}
size_t tab_mask(void) { return TAB_CAP; }      /* wrong: returns capacity, not mask */
int is_pow2(size_t v) { return (v & (v - 1)) == 0; }  /* wrong: 0 passes (0 & -1 == 0) */""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m10-task",
    "Opcode Table via X-Macros",
    """Build a complete opcode subsystem from one X-macro list. The
boilerplate provides:

```c
#define OPS \\
  X(ADD, 1) \\
  X(SUB, 2) \\
  X(MUL, 3)
```

Implement (using OPS — the enum, dispatch, and name lookup must all be
generated from it):

```c
/* OP_ADD=1, OP_SUB=2, OP_MUL=3 via pasting, plus OP_COUNT sentinel */
/* applies op to a and b; returns 0 and fills *out; -1 on bad op/args */
int op_apply(int op, int a, int b, int *out);
/* "ADD" -> OP_ADD; -1 if unknown */
int op_from_name(const char *name);
```

Rules: SUB is a-b; MUL is a*b; arithmetic must not overflow (use long
internally, return -1 if the true result does not fit int).""",
    C_PRELUDE + "\n#include <stddef.h>\n#include <string.h>\n#define OPS \\\n  X(ADD, 1) \\\n  X(SUB, 2) \\\n  X(MUL, 3)\n\n#define X(id, code) OP_##id = code,\nenum { OPS OP_COUNT };\n#undef X\n\nint op_apply(int op, int a, int b, int *out);\nint op_from_name(const char *name);\n",
    [
        (
            "one list, three views",
            r"""
int r;
CHECK_EQ(OP_ADD, 1); CHECK_EQ(OP_SUB, 2); CHECK_EQ(OP_MUL, 3);
CHECK_EQ(OP_COUNT, 4);
CHECK_EQ(op_apply(OP_ADD, 7, 5, &r), 0); CHECK_EQ(r, 12);
CHECK_EQ(op_apply(OP_SUB, 7, 5, &r), 0); CHECK_EQ(r, 2);
CHECK_EQ(op_apply(OP_MUL, 7, 5, &r), 0); CHECK_EQ(r, 35);
CHECK_EQ(op_apply(99, 1, 2, &r), -1);
CHECK_EQ(op_apply(OP_ADD, 1, 2, NULL), -1);
CHECK_EQ(op_apply(OP_MUL, INT_MAX, 2, &r), -1);   /* overflow rejected */
CHECK_EQ(op_from_name("ADD"), OP_ADD);
CHECK_EQ(op_from_name("MUL"), OP_MUL);
CHECK_EQ(op_from_name("DIV"), -1);
CHECK_EQ(op_from_name(NULL), -1);
""",
            "Name lookup: a static table built with #id inside another X pass. Overflow: compute in long long, compare against INT_MIN/INT_MAX.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Bảng opcode qua X-macro",
        "Từ OPS: cài op_apply (tràn số -> -1) và op_from_name (strcmp; lạ -> -1).",
        [("một danh sách, ba góc nhìn", "bảng tên sinh từ #id trong một lượt X khác; tính trong long long.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m10",
    "Checkpoint: One List, Many Views",
    "Prove the X-macro discipline: enum, dispatch, and lookup all generated from a single source of truth.",
    26,
    r"""
## The task

Implement `op_apply` and `op_from_name` (see the challenge) over the
provided `OPS` list — every view generated from it, none hand-copied.
The overflow rule makes `op_apply` a real API: compute wide, reject
what does not fit, document nothing twice.

Passing this proves the preprocessor's superpower: parallel structures
that cannot drift, because there is only one list.

Next module: trees and heaps — the hierarchy beyond lists.
""",
    "Kiểm tra: Một danh sách, nhiều góc nhìn",
    "Chứng minh kỷ luật X-macro: enum, dispatch, và lookup đều sinh từ một nguồn sự thật.",
    r"""
## Bài toán

Cài `op_apply` và `op_from_name` (xem challenge) trên danh sách `OPS` đã
cho — mọi góc nhìn sinh từ nó, không cái nào chép tay. Quy tắc tràn số
khiến `op_apply` thành API thật: tính rộng, từ chối thứ không vừa, không
ghi gì hai lần.

Vượt qua chứng minh siêu năng lực của preprocessor: các cấu trúc song
song không thể lệch nhau, vì chỉ có một danh sách.

Module sau: cây và heap — phân cấp vượt qua danh sách.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <limits.h>
#include <string.h>
#include <stddef.h>
static const struct { const char *name; int code; } OP_NAMES[] = {
#define X(id, code) { #id, code },
    OPS
#undef X
};
int op_apply(int op, int a, int b, int *out) {
    if (!out) return -1;
    long long r;
    switch (op) {
    case OP_ADD: r = (long long)a + b; break;
    case OP_SUB: r = (long long)a - b; break;
    case OP_MUL: r = (long long)a * b; break;
    default: return -1;
    }
    if (r < INT_MIN || r > INT_MAX) return -1;
    *out = (int)r;
    return 0;
}
int op_from_name(const char *name) {
    if (!name) return -1;
    for (size_t i = 0; i < sizeof OP_NAMES / sizeof OP_NAMES[0]; i++)
        if (strcmp(OP_NAMES[i].name, name) == 0) return OP_NAMES[i].code;
    return -1;
}""",
    wrong=r"""
#include <limits.h>
#include <string.h>
#include <stddef.h>
static const struct { const char *name; int code; } OP_NAMES[] = {
#define X(id, code) { #id, code },
    OPS
#undef X
};
int op_apply(int op, int a, int b, int *out) {
    if (!out) return -1;
    int r;                                   /* wrong: int math — INT_MAX * 2
                                                  is UB, not a detectable overflow */
    switch (op) {
    case OP_ADD: r = a + b; break;
    case OP_SUB: r = a - b; break;
    case OP_MUL: r = a * b; break;
    default: return -1;
    }
    *out = r;
    return 0;
}
int op_from_name(const char *name) {
    if (!name) return -1;
    for (size_t i = 0; i < sizeof OP_NAMES / sizeof OP_NAMES[0]; i++)
        if (strstr(OP_NAMES[i].name, name) != NULL) return OP_NAMES[i].code;  /* wrong:
                                                  substring match: "A" -> ADD, "U" -> SUB/MUL first hit */
    return -1;
}""",
)

print("module 10 complete")
