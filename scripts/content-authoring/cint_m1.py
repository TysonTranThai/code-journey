#!/usr/bin/env python3
"""C — Intermediate — Module 1: cint-translation-units.

Opens the course on the model Beginner left implicit: what a translation unit
is, what the preprocessor really does, static vs external linkage, why header
guards exist, and how linker errors are read. All graded code ISO C. House
conventions: raw triple-quoted C strings, self-contained tests, Solution-qualified
helpers, explicit CHECK messages, Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-translation-units"

# ---------------------------------------------------------------- lessons
write_module(
    M,
    "Translation Units, Linking & the Build Model",
    "What the compiler really does with your source: preprocessing, compilation, "
    "linking, internal vs external linkage, and how to read the errors each stage produces.",
    "Đơn vị dịch, liên kết & mô hình build",
    "Compiler thực sự làm gì với mã nguồn của bạn: tiền xử lý, biên dịch, liên kết, "
    "liên kết nội bộ vs bên ngoài, và cách đọc lỗi ở từng giai đoạn.",
    lessons=["linkage-model", "static-extern", "headers-deep", "cint-checkpoint-m1"],
    practices=["cint-p1-linking", "cint-p1-linkage"],
)
print("module json done")

write_lesson(
    M, "linkage-model",
    "The Life of a Translation Unit",
    "Follow one .c file through preprocessing, compilation and linking — and learn which errors belong to which stage.",
    14,
    r"""
## One source file, three stages

Beginner treated "compile" as one step. It is three, and knowing which stage
failed is half of debugging C:

1. **Preprocessing** — textual. `#include` pastes a file's text in place,
   macros are expanded, `#if` blocks are pruned. Output: one big **translation
   unit** (TU).
2. **Compilation** — the TU is parsed and optimized into an **object file**
   (`.o`), machine code with holes where other files' symbols are referenced.
3. **Linking** — the linker merges object files and libraries, filling every
   hole. If it cannot fill one, you get a **linker error**, not a compiler
   error.

```c
/* what #include actually does — it is copy-paste */
#include "myheader.h"   /* pastes myheader.h's full text here */
```

## Why this matters for errors

- `error: unknown type name 'Foo'` → **compile stage** (a declaration is
  missing where the compiler is reading).
- `undefined reference to 'helper'` → **link stage** (the name was declared
  but never defined in any object file).
- `multiple definition of 'counter'` → **link stage** (two TUs both defined it).

## The one-definition rule (in C terms)

A program may **declare** a name many times (that is what headers do) but must
**define** it exactly once across all TUs. A declaration says "this exists
somewhere"; a definition creates it.

```c
extern int counter;   /* declaration: exists somewhere else */
int counter = 0;      /* definition: it lives in THIS object file */
```

## Internal linkage: `static` at file scope

```c
static int helpers_used = 0;   /* private to this TU */
static void tally(void) { helpers_used++; }   /* not visible to the linker */
```

`static` at file scope means "this name is **internal** — other object files
cannot see it, and mine cannot collide with theirs." Two different files may
each have their own `static int count;` without conflict. Without `static`,
the name is **external** and every TU's copy must be one and the same.

## Functions are external by default

```c
static int fast_path(int x) { return x + 1; }  /* internal: this file only */
int slow_path(int x);                          /* external: defined elsewhere */
```

Rule of thumb: give every file-private helper `static`. You get better
diagnostics (unused-function warnings), no accidental cross-file collisions,
and the optimizer can sometimes inline more aggressively when a name has
internal linkage.

## Check your understanding

- Which stage complains about a missing semicolon? (Compile — preprocessing
  only reshuffles text; the parser finds the error.)
- Two files both define `int total;` at file scope. Which stage fails?
  (Link — tentative definitions of the same external name collide.)
- What does the preprocessor do with `#if 0 ... #endif`? (Deletes the block
  before the compiler ever sees it.)
""",
    "Đời sống của một đơn vị dịch",
    "Theo một tệp .c qua tiền xử lý, biên dịch và liên kết — và học lỗi nào thuộc giai đoạn nào.",
    r"""
## Một tệp mã nguồn, ba giai đoạn

Cấp độ mới xem "biên dịch" như một bước. Thực ra là ba, và biết giai đoạn nào
lỗi là một nửa công việc debug C:

1. **Tiền xử lý** — thao tác trên văn bản. `#include` dán nguyên văn nội dung
   tệp vào chỗ include, macro được mở rộng, khối `#if` bị cắt bỏ. Kết quả:
   một **đơn vị dịch** (translation unit).
2. **Biên dịch** — đơn vị dịch được phân tích và tối ưu thành **tệp đối tượng**
   (`.o`): mã máy với các "lỗ" ở những chỗ tham chiếu symbol của tệp khác.
3. **Liên kết** — linker gộp các tệp đối tượng và thư viện, lấp đầy mọi lỗ.
   Không lấp được thì bạn gặp **lỗi liên kết**, không phải lỗi biên dịch.

```c
/* #include thực chất là gì — copy-paste */
#include "myheader.h"   /* dán toàn bộ văn bản myheader.h vào đây */
```

## Vì sao điều này quan trọng khi đọc lỗi

- `error: unknown type name 'Foo'` → **giai đoạn biên dịch** (thiếu khai báo
  ở nơi compiler đang đọc).
- `undefined reference to 'helper'` → **giai đoạn liên kết** (tên được khai
  báo nhưng không có định nghĩa trong tệp đối tượng nào).
- `multiple definition of 'counter'` → **giai đoạn liên kết** (hai TU cùng định nghĩa).

## Quy tắc một định nghĩa

Một chương trình có thể **khai báo** một tên nhiều lần (đó là việc của header)
nhưng chỉ được **định nghĩa** đúng một lần trên toàn bộ các TU. Khai báo nói
"thứ này tồn tại ở đâu đó"; định nghĩa tạo ra nó.

```c
extern int counter;   /* khai báo: tồn tại ở nơi khác */
int counter = 0;      /* định nghĩa: nó nằm trong tệp đối tượng NÀY */
```

## Liên kết nội bộ: `static` ở phạm vi tệp

```c
static int helpers_used = 0;   /* riêng tư trong TU này */
static void tally(void) { helpers_used++; }   /* linker không thấy */
```

`static` ở phạm vi tệp nghĩa là "tên này **nội bộ** — tệp đối tượng khác không
thấy, và tệp của tôi không đụng ai". Hai tệp khác nhau có thể cùng có
`static int count;` riêng mà không xung đột. Không có `static`, tên là
**bên ngoài** và mọi bản sao phải là một thực thể duy nhất.

## Hàm mặc định là bên ngoài

```c
static int fast_path(int x) { return x + 1; }  /* nội bộ: chỉ tệp này */
int slow_path(int x);                          /* bên ngoài: định nghĩa nơi khác */
```

Nguyên tắc: mỗi helper riêng tư của tệp đều có `static`. Bạn nhận được cảnh
báo tốt hơn (unused-function), không va chạm tên ngoài ý muốn, và optimizer
đôi khi inline mạnh hơn khi tên có liên kết nội bộ.

## Kiểm tra hiểu biết

- Giai đoạn nào bắt thiếu dấu chấm phẩy? (Biên dịch — tiền xử lý chỉ xáo trộn
  văn bản; parser mới phát hiện.)
- Hai tệp cùng định nghĩa `int total;` ở phạm vi tệp. Giai đoạn nào fail?
  (Liên kết — định nghĩa "mặc định" trùng tên bên ngoài.)
- Tiền xử lý làm gì với `#if 0 ... #endif`? (Xóa khối trước khi compiler thấy.)
""",
)

write_lesson(
    M, "static-extern",
    "`static` and `extern`: Duration, Scope, Linkage",
    "Three distinct meanings of static, what extern really promises, and the storage-duration model Intermediate needs.",
    15,
    r"""
## `static` has three faces

`static` is one keyword with three meanings depending on where it sits. Conflating
them is the root of many bugs:

| Where | Meaning |
|---|---|
| File scope (`static int x;`) | **Internal linkage** — private to this TU |
| Inside a function (`static int c = 0;`) | **Static storage duration** — one object, lives for the whole program, initialized once |
| On a function parameter/return (`static` in `_Bool static_flag(...)` — rare) | essentially internal linkage for functions |

Inside a function, a `static` variable is *not* on the stack. Every call sees —
and can mutate — the same object:

```c
int next_id(void) {
    static int counter = 0;   /* born once, survives all calls */
    return ++counter;
}
```

That is powerful and dangerous: it makes the function **stateful**, which breaks
re-entrancy. Two "simultaneous" uses (from threads, or even recursion) mutate the
same storage. Intermediate rule: use function-scope `static` only for genuinely
global, single-instance state, and document it.

## `extern` is a promise

`extern int attempts;` says: "an object named `attempts` exists with external
linkage — its definition is in some TU, not necessarily this one." It is the
bridge that lets many files share one object:

```c
/* stats.c */
int attempts = 0;            /* THE definition (external by default) */

/* stats.h */
extern int attempts;         /* declaration every includer sees */
```

Every TU that includes the header declares the same external object; exactly one
TU defines it. Forget the definition and the linker tells you:
`undefined reference to 'attempts'`.

## Storage duration: where objects live

- **Automatic** — locals, including parameters. Born at the `{`, die at the `}`.
  A pointer to an automatic object is invalid the moment the block exits.
- **Static** — file-scope objects and function-scope `static`. One instance,
  whole-program life, zero-initialized if you do not initialize.
- **Allocated** — `malloc`/`calloc`/`realloc`. Lives until you `free` it.
  Module 3 makes ownership of this category rigorous.

The classic bug this model explains:

```c
char *badge(const char *name) {
    char buf[64];                       /* automatic */
    snprintf(buf, sizeof buf, "%s!", name);
    return buf;                         /* BUG: dangling on return */
}
```

The returned pointer points into a dead stack frame. `static char buf[64];`
"fixes" it by making the buffer outlive the call — but now every caller shares
one buffer, and a second call overwrites the first result. The real fix is the
caller owning the storage (Module 3).

## Check your understanding

- What is printed if you call `next_id()` three times? (1, 2, 3 — the static
  persists.)
- Is `extern int x;` a definition? (No — a declaration.)
- Which duration does a string literal have? (Static — it lives for the whole
  program; that is why returning a literal is safe while returning a local
  array is not.)
""",
    "`static` và `extern`: Thời gian sống, phạm vi, liên kết",
    "Ba nghĩa khác nhau của static, extern thực sự hứa gì, và mô hình storage-duration mà Trung cấp cần.",
    r"""
## `static` có ba gương mặt

`static` là một từ khóa với ba nghĩa tùy vị trí. Nhầm lẫn giữa chúng là gốc của
nhiều bug:

| Vị trí | Nghĩa |
|---|---|
| Phạm vi tệp (`static int x;`) | **Liên kết nội bộ** — riêng tư trong TU này |
| Trong hàm (`static int c = 0;`) | **Thời gian sống tĩnh** — một đối tượng duy nhất, sống suốt chương trình, khởi tạo một lần |
| Trên tham số/hàm (hiếm) | về cơ bản là liên kết nội bộ cho hàm |

Trong hàm, biến `static` *không* nằm trên stack. Mọi lời gọi thấy — và có thể
thay đổi — cùng một đối tượng:

```c
int next_id(void) {
    static int counter = 0;   /* sinh một lần, sống qua mọi lời gọi */
    return ++counter;
}
```

Mạnh và nguy hiểm: nó làm hàm **có trạng thái**, phá vỡ khả năng re-entrant.
Hai lần dùng "đồng thời" (từ thread, hay thậm chí đệ quy) cùng biến đổi một ô
nhớ. Nguyên tắc Trung cấp: chỉ dùng `static` trong hàm cho trạng thái toàn cục,
một-thực-thể-thật, và ghi chú rõ.

## `extern` là một lời hứa

`extern int attempts;` nói: "tồn tại một đối tượng tên `attempts` với liên kết
bên ngoài — định nghĩa của nó ở TU nào đó, không nhất thiết là TU này." Đây là
cầu nối để nhiều tệp chia sẻ một đối tượng:

```c
/* stats.c */
int attempts = 0;            /* ĐỊNH NGHĨA duy nhất (mặc định bên ngoài) */

/* stats.h */
extern int attempts;         /* khai báo mà mọi người include đều thấy */
```

Mỗi TU include header đều khai báo cùng một đối tượng bên ngoài; đúng một TU
định nghĩa nó. Quên định nghĩa, linker sẽ nói: `undefined reference to 'attempts'`.

## Thời gian sống: đối tượng sống ở đâu

- **Tự động** — biến cục bộ, kể cả tham số. Sinh tại `{`, chết tại `}`.
  Con trỏ trỏ vào đối tượng tự động vô hiệu ngay khi khối kết thúc.
- **Tĩnh** — đối tượng phạm vi tệp và `static` trong hàm. Một thực thể,
  sống cả chương trình, tự động về 0 nếu bạn không khởi tạo.
- **Cấp phát** — `malloc`/`calloc`/`realloc`. Sống đến khi bạn `free`.
  Module 3 sẽ làm cho quyền sở hữu của nhóm này nghiêm ngặt.

Bug kinh điển mà mô hình này giải thích:

```c
char *badge(const char *name) {
    char buf[64];                       /* tự động */
    snprintf(buf, sizeof buf, "%s!", name);
    return buf;                         /* BUG: lơ lửng khi return */
}
```

Con trỏ trả về trỏ vào khung stack đã chết. `static char buf[64];` "sửa" được
bằng cách cho buffer sống qua lời gọi — nhưng giờ mọi caller chia sẻ một buffer,
lần gọi thứ hai ghi đè kết quả lần đầu. Cách sửa đúng là caller sở hữu bộ nhớ
(Module 3).

## Kiểm tra hiểu biết

- Gọi `next_id()` ba lần in ra gì? (1, 2, 3 — static được giữ lại.)
- `extern int x;` có phải định nghĩa không? (Không — chỉ là khai báo.)
- Chuỗi ký tự literal có thời gian sống nào? (Tĩnh — sống cả chương trình;
  vì vậy trả về literal là an toàn, khác với trả về mảng cục bộ.)
""",
)

write_lesson(
    M, "headers-deep",
    "Headers as Contracts",
    "What belongs in a header, include guards, why declarations in headers never initialize, and designing a clean public API.",
    13,
    r"""
## A header is an interface document

A `.h` file is the public contract of a component: everything a *user* of the
component may rely on. A `.c` file is the private implementation. The discipline:

- **Headers**: type definitions the API exposes, function **declarations**,
  `extern` object declarations, macros that are part of the contract.
- **Source files**: definitions, file-scope `static` helpers, private macros.

A header should compile on its own — it includes what it needs, never " hopes
the includer included things first":

```c
/* vec.h */
#ifndef CINT_VEC_H
#define CINT_VEC_H
#include <stddef.h>       /* for size_t — self-sufficient */

typedef struct Vec Vec;           /* opaque: users hold pointers, not innards */
Vec *vec_create(size_t initial_capacity);
int  vec_push(Vec *v, int value);
size_t vec_len(const Vec *v);
void vec_destroy(Vec *v);
#endif
```

## Include guards, mechanically

`#ifndef/#define/#endif` make a header idempotent: pasting it twice into one TU
still yields one copy of each declaration. Without guards, two headers that each
include a common third header would paste its declarations twice — and repeated
non-`extern` definitions or typedef redefinitions can fail the compile. (C11+
allows this pattern to be replaced by `#pragma once` in practice, but guards are
the portable, standard idiom.)

## Declarations never belong with initializers

```c
/* in a header */
extern int threshold = 50;   /* WRONG: a definition with storage, in every TU */
extern int threshold;        /* RIGHT: a promise; one .c defines it */
```

Const deserves care: `const int limit;` at file scope in a header is a
*definition in each TU* (internal linkage by default for const) — legal but
memory-duplicating. Shared mutable constants use `extern const` + one
definition.

## Designing the boundary

1. **Minimize the surface.** Export functions, not globals. Every global is a
   hidden parameter and a concurrency hazard.
2. **Make ownership explicit in signatures** (Module 3 deepens this):
   `vec_create` returns something the caller must `vec_destroy` — the name says
   both halves.
3. **Opaque types for structure freedom.** If users never dereference `Vec *`,
   you may change the layout without recompiling the world.

## Check your understanding

- Where does the definition of `threshold` live? (Exactly one `.c` file.)
- What breaks if two headers both define `typedef struct Point Point;` with the
  same shape? (Duplicate typedef — C23 relaxes this, but the discipline stands:
  define shared types once in a shared header.)
""",
    "Header như hợp đồng",
    "Điều gì thuộc về header, include guard, vì sao khai báo trong header không bao giờ khởi tạo, và cách thiết kế API công khai sạch.",
    r"""
## Header là văn bản giao kèo

Tệp `.h` là hợp đồng công khai của một thành phần: mọi thứ người *dùng* thành
phần có thể dựa vào. Tệp `.c` là phần hiện thực riêng tư. Nguyên tắc:

- **Header**: định nghĩa kiểu mà API công bố, **khai báo** hàm, khai báo
  đối tượng `extern`, macro thuộc hợp đồng.
- **Tệp nguồn**: định nghĩa, helper `static` phạm vi tệp, macro riêng tư.

Header phải tự biên dịch được một mình — nó include những gì nó cần, không bao
giờ "mong người include đã include trước":

```c
/* vec.h */
#ifndef CINT_VEC_H
#define CINT_VEC_H
#include <stddef.h>       /* cho size_t — tự đủ */

typedef struct Vec Vec;           /* opaque: người dùng giữ con trỏ, không phải ruột */
Vec *vec_create(size_t initial_capacity);
int  vec_push(Vec *v, int value);
size_t vec_len(const Vec *v);
void vec_destroy(Vec *v);
#endif
```

## Include guard, về mặt cơ chế

`#ifndef/#define/#endif` làm header trở nên idempotent: dán nó hai lần vào một
TU vẫn cho một bản duy nhất của mỗi khai báo. Không có guard, hai header cùng
include một header thứ ba sẽ dán khai báo của nó hai lần — và định nghĩa lặp
không phải `extern` hay typedef lặp có thể làm biên dịch fail. (C11+ thực tế
cho phép `#pragma once`, nhưng guard mới là chuẩn mới mang tính di động.)

## Khai báo không bao giờ đi kèm bộ khởi tạo

```c
/* trong header */
extern int threshold = 50;   /* SAI: định nghĩa có ô nhớ, trong mọi TU */
extern int threshold;        /* ĐÚNG: một lời hứa; đúng một .c định nghĩa */
```

Const cần cẩn thận: `const int limit;` ở phạm vi tệp trong header là *định nghĩa
trong mỗi TU* (const mặc định có liên kết nội bộ) — hợp lệ nhưng nhân bản bộ
nhớ. Hằng chia sẻ, có thể thay đổi dùng `extern const` + một định nghĩa.

## Thiết kế ranh giới

1. **Thu nhỏ bề mặt.** Xuất hàm, không xuất biến toàn cục. Mỗi biến toàn cục là
   một tham số ẩn và một rủi ro concurrency.
2. **Làm cho quyền sở hữu hiện rõ trong chữ ký** (Module 3 đào sâu):
   `vec_create` trả về thứ mà caller phải `vec_destroy` — tên hàm nói cả hai nửa.
3. **Kiểu opaque để tự do cấu trúc.** Nếu người dùng không bao giờ dereference
   `Vec *`, bạn có thể đổi layout mà không cần biên dịch lại tất cả.

## Kiểm tra hiểu biết

- Định nghĩa của `threshold` nằm ở đâu? (Đúng một tệp `.c`.)
- Hai header cùng định nghĩa `typedef struct Point Point;` với hình dáng giống
  nhau thì sao? (Typedef trùng — C23 nới lỏng, nhưng nguyên tắc vẫn giữ: định
  nghĩa kiểu dùng chung một lần trong một header chung.)
""",
)

# ---------------------------------------------------------------- practice set 1a
P1A_CH = [
    challenge(
        "cint-p1-tu-count",
        "Count the Translation Units",
        """A build compiles two source files, each including two headers. Read the
`build_log` string (a multi-line compile log: one `gcc ... -c file.c` line per
translation unit, then one linking line) and implement:

```c
int count_translation_units(const char *build_log);
int count_link_errors(const char *build_log);
```

`count_translation_units` returns how many `-c` compile lines appear.
`count_link_errors` returns how many lines contain `undefined reference`.
Both return 0 for NULL or empty input. Lines are separated by `\\n`.""",
        C_PRELUDE,
        [
            (
                "counts compile lines",
                r"""
const char *log1 = "gcc -std=c23 -c main.c\ngcc -std=c23 -c util.c\n";
CHECK_EQ(count_translation_units(log1), 2);
CHECK_EQ(count_translation_units("gcc -c a.c"), 1);
CHECK_EQ(count_translation_units(""), 0);
CHECK_EQ(count_translation_units(NULL), 0);
""",
                "Scan the string for the substring \"-c \"; each occurrence that starts a line is one TU.",
            ),
            (
                "counts undefined references",
                r"""
const char *log2 = "undefined reference to 'helper'\nundefined reference to 'util_fn'\n";
CHECK_EQ(count_link_errors(log2), 2);
CHECK_EQ(count_link_errors("all good\n"), 0);
const char *log3 = "gcc -c x.c\nundefined reference to 'y'\n";
CHECK_EQ(count_link_errors(log3), 1);
""",
                "Count occurrences of \"undefined reference\" as a substring.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p1-static-visibility",
        "Internal Linkage Twins",
        """Implement a file-scope static counter pair that demonstrates internal
linkage semantics:

```c
int tally_a(int n);   /* uses static accumulator a_count */
int tally_b(int n);   /* uses static accumulator b_count */
```

Each function adds `n` to its own accumulator (both start at 0) and returns the
new total. The two accumulators must be independent — that is the whole point of
internal linkage. Also implement `int peek_a(void)` returning a_count unchanged.""",
        C_PRELUDE,
        [
            (
                "accumulators are independent",
                r"""
CHECK_EQ(tally_a(5), 5);
CHECK_EQ(tally_b(3), 3);
CHECK_EQ(tally_a(2), 7);
CHECK_EQ(tally_b(4), 7);
CHECK_EQ(peek_a(), 7);
CHECK_EQ(tally_a(0), 7);
""",
                "static int a_count = 0; static int b_count = 0; — two file-scope statics.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p1-dangling-badge",
        "Fix the Dangling Badge",
        """This program has the classic return-a-local bug. Implement it CORRECTLY:

```c
const char *badge_for(int score);
```

It must return the string `"gold"` when score >= 90, `"silver"` when score >= 80,
`"bronze"` otherwise. The returned pointer must stay valid for the whole program
lifetime — return a string literal (static duration), never a local array.""",
        C_PRELUDE,
        [
            (
                "returns valid static strings",
                r"""
CHECK_STR_EQ(badge_for(95), "gold");
CHECK_STR_EQ(badge_for(90), "gold");
CHECK_STR_EQ(badge_for(85), "silver");
CHECK_STR_EQ(badge_for(80), "silver");
CHECK_STR_EQ(badge_for(10), "bronze");
""",
                "return score >= 90 ? \"gold\" : (score >= 80 ? \"silver\" : \"bronze\"); — literals have static duration.",
            ),
        ],
        level="debugging",
    ),
    challenge(
        "cint-p1-link-order",
        "Simulate the Linker",
        """Implement a tiny model of symbol resolution:

```c
int resolve(int *symbols, size_t n, const char *want);
```

`symbols` encodes definitions across object files: each element is
`1` (definition), `0` (declaration only), or `-1` (duplicate definition).
`resolve` returns: `0` if there is exactly one definition and at least one
declaration-or-definition overall, `-1` if there are zero definitions, and
`1` if there are two or more definitions (multiple definition error).
NULL or empty input returns -1 (nothing defined).""",
        C_PRELUDE,
        [
            (
                "resolution verdicts",
                r"""
int s1[] = {0, 1, 0};
CHECK_EQ(resolve(s1, 3, "fn"), 0);
int s2[] = {0, 0, 0};
CHECK_EQ(resolve(s2, 3, "fn"), -1);
int s3[] = {1, 1, 0};
CHECK_EQ(resolve(s3, 3, "fn"), 1);
CHECK_EQ(resolve(NULL, 0, "fn"), -1);
int s4[] = {1};
CHECK_EQ(resolve(s4, 1, "fn"), 0);
""",
                "Count definitions (== 1): zero -> -1, two or more -> 1, exactly one -> 0.",
            ),
        ],
        level="mini-build",
    ),
]
P1A_SOL = [
    (
        "cint-p1-tu-count",
        r"""
static int count_substr(const char *s, const char *needle) {
    if (!s || !needle) return 0;
    int n = 0;
    for (const char *p = s; (p = strstr(p, needle)) != NULL; p += 1) n++;
    return n;
}
int count_translation_units(const char *b) { return count_substr(b, "-c "); }
int count_link_errors(const char *b) { return count_substr(b, "undefined reference"); }""",
        r"""
int count_translation_units(const char *b) { return b ? 1 : 0; }
int count_link_errors(const char *b) { return 0; }""",
    ),
    (
        "cint-p1-static-visibility",
        r"""
static int a_count = 0;
static int b_count = 0;
int tally_a(int n) { a_count += n; return a_count; }
int tally_b(int n) { b_count += n; return b_count; }
int peek_a(void) { return a_count; }""",
        r"""
static int shared_count = 0;   /* wrong: one shared accumulator */
int tally_a(int n) { shared_count += n; return shared_count; }
int tally_b(int n) { shared_count += n; return shared_count; }
int peek_a(void) { return shared_count; }""",
    ),
    (
        "cint-p1-dangling-badge",
        r"""
const char *badge_for(int score) {
    return score >= 90 ? "gold" : (score >= 80 ? "silver" : "bronze");
}""",
        r"""
const char *badge_for(int score) {
    const char *g = "gold";
    const char *s = "silver";
    char pick[8];                       /* local array: dangling on return */
    snprintf(pick, sizeof pick, "%s", score >= 90 ? g : s);
    return score < 80 ? pick : (score >= 90 ? "gold" : "silver");
}""",
    ),
    (
        "cint-p1-link-order",
        r"""
int resolve(const int *symbols, size_t n, const char *want) {
    (void)want;
    if (!symbols || n == 0) return -1;
    size_t defs = 0;
    for (size_t i = 0; i < n; i++) if (symbols[i] == 1) defs++;
    if (defs == 0) return -1;
    if (defs >= 2) return 1;
    return 0;
}""",
        r"""
int resolve(const int *symbols, size_t n, const char *want) {
    (void)want;
    if (!symbols || n == 0) return -1;
    size_t defs = 0, decls = 0;
    for (size_t i = 0; i < n; i++) {
        if (symbols[i] == 1) defs++;
        if (symbols[i] == 0) decls++;
    }
    if (defs == 0) return decls > 0 ? -1 : -1;   /* wrong: ignores duplicates */
    if (defs >= 2 && decls == 0) return 1;
    if (defs >= 2) return 0;                     /* wrong: duplicates excused by declarations */
    return 0;
}""",
    ),
]
VIT = lambda n, h: (n, h)
write_practice(
    M, "cint-p1-linking",
    "Read the Build",
    "Model the three build stages and their failure modes in miniature.",
    "Đọc bản build",
    "Mô hình hóa ba giai đoạn build và các kiểu lỗi của chúng ở mức nhỏ.",
    after_lesson="linkage-model",
    minutes=22,
    difficulty="intermediate",
    challenges=P1A_CH,
    vi_challenges={
        "cint-p1-tu-count": vi_challenge(
            "Đếm đơn vị dịch",
            "Cài `count_translation_units` đếm số dòng `-c` trong build_log và `count_link_errors` đếm số dòng chứa `undefined reference`. Cả hai trả 0 với NULL/rỗng.",
            [VIT("đếm dòng biên dịch", "Tìm chuỗi con \"-c \"; mỗi lần xuất hiện đầu dòng là một TU."),
             VIT("đếm undefined reference", "Đếm số lần xuất hiện chuỗi \"undefined reference\".")],
        ),
        "cint-p1-static-visibility": vi_challenge(
            "Hai bộ đếm liên kết nội bộ",
            "Cài `tally_a`/`tally_b` với hai bộ đếm static phạm vi tệp độc lập; `peek_a` đọc mà không đổi.",
            [VIT("bộ đếm độc lập", "static int a_count = 0; static int b_count = 0;")],
        ),
        "cint-p1-dangling-badge": vi_challenge(
            "Sửa huy hiệu lơ lửng",
            "Cài `badge_for` trả về literal (static duration) — không bao giờ trả mảng cục bộ.",
            [VIT("chuỗi tĩnh hợp lệ", "Dùng biểu thức ?: trả về literal.")],
        ),
        "cint-p1-link-order": vi_challenge(
            "Mô phỏng linker",
            "Cài `resolve`: 0 nếu đúng một định nghĩa, -1 nếu không có, 1 nếu trùng định nghĩa.",
            [VIT("phán quyết", "Đếm số phần tử == 1: 0 -> -1, >=2 -> 1, ==1 -> 0.")],
        ),
    },
    solutions=P1A_SOL,
)

# ---------------------------------------------------------------- practice set 1b
P1B_CH = [
    challenge(
        "cint-p1-extern-share",
        "One Object, Many Promises",
        """Implement a shared-external pattern in one TU:

```c
int attempts = 0;          /* the definition (external linkage) */
void record_attempt(void); /* increments attempts */
int peek_attempts(void);   /* returns attempts */
```

`record_attempt` must be safe to call any number of times. Then implement
`int reset_attempts(void)` which zeroes attempts and returns how many were
recorded since the last reset.""",
        C_PRELUDE,
        [
            (
                "shared object lifecycle",
                r"""
CHECK_EQ(peek_attempts(), 0);
record_attempt();
record_attempt();
record_attempt();
CHECK_EQ(peek_attempts(), 3);
CHECK_EQ(reset_attempts(), 3);
CHECK_EQ(peek_attempts(), 0);
""",
                "int attempts = 0; at file scope (no static), then the three functions.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p1-stateful-counter",
        "The Stateful Function",
        """Implement `int next_id(void)` using a function-scope static: first call
returns 1, then 2, 3, ... forever. Also implement `void reseed_ids(int n)` which
sets the counter so the next `next_id()` returns `n` (n >= 1).""",
        C_PRELUDE,
        [
            (
                "ids increment and reseed",
                r"""
CHECK_EQ(next_id(), 1);
CHECK_EQ(next_id(), 2);
CHECK_EQ(next_id(), 3);
reseed_ids(100);
CHECK_EQ(next_id(), 100);
CHECK_EQ(next_id(), 101);
""",
                "static int counter; ++counter; return counter; — reseed sets counter = n - 1.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p1-tentative-trap",
        "Tentative Definitions",
        """C allows a file-scope `int x;` (a "tentative definition") that merges with
a later real definition. Implement a tiny analyzer:

```c
/* events: 'T' tentative (`int x;`), 'D' real definition (`int x = 0;`),
   'E' extern declaration. n events across TUs. */
int is_valid_program(const char *events);
```

Valid iff there is exactly one 'D' and zero or more 'T's before or after it, or
zero 'D' and at least one 'E' somewhere (definition lives in another TU).
Any other combination is invalid (return 0; valid returns 1). NULL or empty
returns 0.""",
        C_PRELUDE,
        [
            (
                "tentative analysis",
                r"""
CHECK_EQ(is_valid_program("TD"), 1);
CHECK_EQ(is_valid_program("DT"), 1);
CHECK_EQ(is_valid_program("E"), 1);
CHECK_EQ(is_valid_program("T"), 0);      /* tentative never completed */
CHECK_EQ(is_valid_program("DD"), 0);     /* two definitions */
CHECK_EQ(is_valid_program(""), 0);
CHECK_EQ(is_valid_program(NULL), 0);
""",
                "Count Ds and Es: valid = (one D) or (no D and >=1 E).",
            ),
        ],
        level="guided",
    ),
    challenge(
        "cint-p1-static-lib",
        "A Tiny Static Library Model",
        """Model what `ar` does: bundle object files. Implement:

```c
/* archive ops: 0 = add object, 1 = remove object, 2 = link whole archive.
   objects are named 'a'..'z' characters; adding an existing name replaces it. */
int archive_run(const char *ops);
```

`archive_run` processes ops left to right and returns the number of distinct
objects the archive would contain when a link (`2`) is hit — or -1 if a link op
occurs before any object was added. Duplicates via re-add do not increase the
count. Ops are separated by nothing ('a' then 'b' then '2').""",
        C_PRELUDE,
        [
            (
                "archive model",
                r"""
CHECK_EQ(archive_run("a b 2"), 2);       /* spaced for readability; treat spaces as separators too */
CHECK_EQ(archive_run("ab2"), 2);
CHECK_EQ(archive_run("aba2"), 2);        /* re-add replaces, not duplicates */
CHECK_EQ(archive_run("2"), -1);
CHECK_EQ(archive_run("abc2ab2"), 3);    /* re-add replaces, not duplicates */
""",
                "Track a 26-bool presence array; spaces skipped; on '2' count set bits.",
            ),
        ],
        level="mini-build",
    ),
]
P1B_SOL = [
    (
        "cint-p1-extern-share",
        r"""
int attempts = 0;
void record_attempt(void) { attempts++; }
int peek_attempts(void) { return attempts; }
int reset_attempts(void) { int n = attempts; attempts = 0; return n; }""",
        r"""
int attempts = 0;
void record_attempt(void) { attempts += 2; }   /* wrong: double-counts */
int peek_attempts(void) { return attempts; }
int reset_attempts(void) { int n = attempts; attempts = 0; return n; }""",
    ),
    (
        "cint-p1-stateful-counter",
        r"""
static int counter = 0;
int next_id(void) { return ++counter; }
void reseed_ids(int n) { counter = (n >= 1) ? n - 1 : 0; }""",
        r"""
int next_id(void) {
    int counter = 0;   /* wrong: automatic — resets every call */
    return ++counter;
}
void reseed_ids(int n) { (void)n; }""",
    ),
    (
        "cint-p1-tentative-trap",
        r"""
int is_valid_program(const char *e) {
    if (!e || !*e) return 0;
    int d = 0, t = 0, ee = 0;
    for (const char *p = e; *p; p++) {
        if (*p == 'D') d++;
        else if (*p == 'T') t++;
        else if (*p == 'E') ee++;
        else return 0;
    }
    if (d == 1) return 1;
    if (d == 0 && ee >= 1) return 1;
    (void)t;
    return 0;
}""",
        r"""
int is_valid_program(const char *e) {
    if (!e || !*e) return 0;
    int d = 0;
    for (const char *p = e; *p; p++) if (*p == 'D') d++;
    return d >= 1;   /* wrong: accepts DD (multiple definitions) */
}""",
    ),
    (
        "cint-p1-static-lib",
        r"""
int archive_run(const char *ops) {
    if (!ops) return -1;
    unsigned present = 0;
    int have_any = 0;
    for (const char *p = ops; *p; p++) {
        if (*p == ' ') continue;
        if (*p == '2') {
            if (!have_any) return -1;
            int n = 0;
            for (unsigned m = present; m; m >>= 1) n += (int)(m & 1u);
            return n;
        }
        if (*p >= 'a' && *p <= 'z') {
            present |= 1u << (*p - 'a');
            have_any = 1;
        }
    }
    return have_any ? 0 : -1;
}""",
        r"""
int archive_run(const char *ops) {
    if (!ops) return -1;
    int count = 0;   /* wrong: re-adds duplicate instead of replacing */
    for (const char *p = ops; *p; p++) {
        if (*p == ' ') continue;
        if (*p == '2') return count > 0 ? count : -1;
        count++;
    }
    return count > 0 ? 0 : -1;
}""",
    ),
]
write_practice(
    M, "cint-p1-linkage",
    "Duration & Linkage Gym",
    "Practice static/extern semantics until the storage model is reflexive.",
    "Phòng gym về thời gian sống & liên kết",
    "Luyện static/extern đến khi mô hình bộ nhớ thành phản xạ.",
    after_lesson="static-extern",
    minutes=24,
    difficulty="intermediate",
    challenges=P1B_CH,
    vi_challenges={
        "cint-p1-extern-share": vi_challenge(
            "Một đối tượng, nhiều lời hứa",
            "Cài `attempts` external, `record_attempt`, `peek_attempts`, `reset_attempts`.",
            [VIT("vòng đời đối tượng dùng chung", "int attempts = 0; ở phạm vi tệp (không static).")],
        ),
        "cint-p1-stateful-counter": vi_challenge(
            "Hàm có trạng thái",
            "Cài `next_id` bằng static trong hàm: 1, 2, 3...; `reseed_ids(n)` đặt lần trả tiếp theo là n.",
            [VIT("id tăng và seed lại", "static int counter; ++counter; return counter;")],
        ),
        "cint-p1-tentative-trap": vi_challenge(
            "Định nghĩa mặc định (tentative)",
            "Cài `is_valid_program`: hợp lệ khi đúng một 'D', hoặc không 'D' và có ít nhất một 'E'.",
            [VIT("phân tích tentative", "Đếm D và E: hợp lệ = (một D) hoặc (không D và >=1 E).")],
        ),
        "cint-p1-static-lib": vi_challenge(
            "Mô hình thư viện tĩnh nhỏ",
            "Cài `archive_run` xử lý ops, trả về số object khi gặp '2', -1 nếu link trước khi có object.",
            [VIT("mô hình archive", "Mảng 26 bool đánh dấu; '2' thì đếm bit bật.")],
        ),
    },
    solutions=P1B_SOL,
)

# ---------------------------------------------------------------- checkpoint
CP_CH = challenge(
    "cint-checkpoint-m1-task",
    "Checkpoint: The Two-File Build",
    """Model an entire two-TU build and its failure modes in one API:

```c
/* files: 'C' = compile OK, 'c' = compile ERROR, 'L' = links, 'l' = link ERROR.
   A build string is a sequence like "CCLl" — per-TU compile results followed
   by the link result. */
int build_verdict(const char *stages);
```

Rules: if any compile stage is 'c', the build fails at that point — return
`-1 - <index of first failing TU>` (first TU is index 0). Otherwise if the link
result is 'l', return `-100`. Otherwise return the number of successful TUs.
NULL or empty returns -1. Extra characters (spaces) are skipped.""",
    C_PRELUDE,
    [
        (
            "full build verdicts",
            r"""
CHECK_EQ(build_verdict("CCL"), 2);
CHECK_EQ(build_verdict("cCL"), -1);          /* first TU fails compile */
CHECK_EQ(build_verdict("CcL"), -2);          /* second TU fails compile */
CHECK_EQ(build_verdict("CCl"), -100);
CHECK_EQ(build_verdict("CCC L"), 3);
CHECK_EQ(build_verdict(""), -1);
""",
            "Scan compile chars until you hit L or l; on 'c' return -1 - index.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)
CP_VI = vi_challenge(
    "Kiểm tra: Bản build hai tệp",
    "Cài `build_verdict` mô hình hóa build hai TU: 'C' biên dịch OK, 'c' lỗi biên dịch, 'L' liên kết OK, 'l' lỗi liên kết.",
    [("phán quyết build đầy đủ", "Quét ký tự biên dịch đến khi gặp L hoặc l; gặp 'c' trả -1 - chỉ số.")],
)
write_checkpoint(
    M, "cint-checkpoint-m1",
    "Checkpoint: Translation Units & Linkage",
    "Prove you can model the build pipeline and its failure modes before moving to pointers.",
    20,
    r"""
## What you just proved

- You can distinguish the three build stages and their error signatures.
- You can predict internal vs external linkage consequences (independent
  accumulators, shared objects).
- You understand why returning locals dangles and literals survive.
- You can model symbol resolution — the linker's actual job — in miniature.

Next module stops treating pointers as syntax and starts treating them as
addresses you can reason about precisely.
""",
    "Kiểm tra: Đơn vị dịch & liên kết",
    "Chứng minh bạn có thể mô hình hóa pipeline build và các kiểu lỗi trước khi sang con trỏ.",
    r"""
## Bạn vừa chứng minh điều gì

- Bạn phân biệt được ba giai đoạn build và chữ tín hiệu lỗi của chúng.
- Bạn dự đoán được hậu quả liên kết nội bộ vs bên ngoài (bộ đếm độc lập,
  đối tượng chia sẻ).
- Bạn hiểu vì sao trả về biến cục bộ gây lơ lửng còn literal thì sống sót.
- Bạn mô hình hóa được việc phân giải symbol — công việc thật của linker.

Module sau ngừng coi con trỏ là cú pháp và bắt đầu coi chúng là địa chỉ mà bạn
suy luận chính xác được.
""",
    CP_CH,
    CP_VI,
    solution=r"""
int build_verdict(const char *s) {
    if (!s || !*s) return -1;
    int idx = 0;
    const char *p = s;
    while (*p) {
        if (*p == ' ') { p++; continue; }
        if (*p == 'C') { idx++; p++; continue; }
        if (*p == 'c') return -1 - idx;
        if (*p == 'L') return idx;
        if (*p == 'l') return -100;
        p++;
    }
    return idx;
}""",
    wrong=r"""
int build_verdict(const char *s) {
    if (!s || !*s) return -1;
    int idx = 0;
    for (const char *p = s; *p; p++) {
        if (*p == ' ') continue;
        if (*p == 'C') idx++;
        if (*p == 'c') return -1;      /* wrong: loses the index */
        if (*p == 'L') return idx;
        if (*p == 'l') return -1;      /* wrong: not -100 */
    }
    return idx;
}""",
)

print("module 1 complete")
