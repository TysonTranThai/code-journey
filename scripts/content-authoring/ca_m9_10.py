#!/usr/bin/env python3
"""C Advanced — batch 5: modules 9 (preprocessor-compile-time) and
10 (compilation-pipeline). Zero-backslash authoring: @NL@ = statement
separator, @CE@ = newline escape inside C string literals."""
from ca import (
    C_PRELUDE,
    POSIX_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ================ MODULE 9: ca-preprocessor-compile-time ====================
M9 = "ca-preprocessor-compile-time"

L9A = "ca-macro-machinery"
L9B = "ca-variadic-assertions"
L9CP = "ca-checkpoint-m9"

write_module(
    M9,
    "The Preprocessor and Compile-Time Techniques",
    "Expansion mechanics, variadic macros, static assertions, and feature detection — the metaprogramming layer that runs before the compiler does.",
    "Bộ tiền xử lý và kỹ thuật lúc biên dịch",
    "Cơ chế mở rộng, macro variadic, static assertion, và phát hiện tính năng — lớp metaprogramming chạy trước trình biên dịch.",
    [L9A, L9B, L9CP],
    ["ca-p9-preproc"],
)

write_lesson(
    M9,
    L9A,
    "Expansion Mechanics",
    "Argument expansion order, the double-expansion idiom, stringize and paste — what the preprocessor actually does with your text.",
    15,
    """
## Arguments expand before substitution — except with # and ##

`SQUARE(x) ((x) * (x))` replaces x with the *already expanded* argument — unless x is used with `#` (stringize) or `##` (paste), where it stays raw. This subtlety is why the classic double-expansion wrapper exists:

```c
#define STR_(x) #x          /* x stays unexpanded: becomes "x" */
#define STR(x)  STR_(x)     /* x expands first, then stringizes */
```

`STR(__LINE__)` gives "14"; `STR_(__LINE__)` gives "__LINE__".

## Parenthesize everything

`#define BAD(a, b) a + b` and `BAD(1, 2) * 3` expands to `1 + 2 * 3`. Every parameter reference gets parentheses; the whole replacement gets parentheses. Macro code that violates this is not stylistically wrong — it computes wrong answers.

## Multi-line and do-while

Statement-shaped macros wrap in `do { ... } while (0)` so `if (x) MACRO(); else ...` still parses — a plain `{ }` would break the semicolon. This is not superstition; it is syntax maintenance.
""",
    "Cơ chế mở rộng",
    "Thứ tự mở rộng đối số, idiom mở rộng kép, stringize và paste — bộ tiền xử lý thực sự làm gì với văn bản của bạn.",
    """
## Đối số mở rộng trước khi thay thế — trừ khi dùng # và ##

`SQUARE(x) ((x) * (x))` thay x bằng đối số *đã mở rộng* — trừ khi x đi với `#` (stringize) hoặc `##` (paste), khi đó giữ nguyên. Chi tiết này là lý do idiom mở rộng kép tồn tại:

```c
#define STR_(x) #x          /* x giữ nguyên: thành "x" */
#define STR(x)  STR_(x)     /* x mở rộng trước, rồi stringize */
```

`STR(__LINE__)` cho "14"; `STR_(__LINE__)` cho "__LINE__".

## Bọc ngoặc mọi thứ

`#define BAD(a, b) a + b` với `BAD(1, 2) * 3` mở rộng thành `1 + 2 * 3`. Mọi tham chiếu tham số được bọc ngoặc; toàn bộ phần thay thế cũng vậy. Macro vi phạm điều này không chỉ sai phong cách — nó tính sai.

## Nhiều dòng và do-while

Macro dạng câu lệnh bọc trong `do { ... } while (0)` để `if (x) MACRO(); else ...` vẫn phân tích được — `{ }` trơn sẽ phá dấu chấm phẩy. Đây không phải mê tín; là bảo trì cú pháp.
""",
)

write_lesson(
    M9,
    L9B,
    "Variadic Macros, Static Assertions, Feature Detection",
    "__VA_ARGS__, _Static_assert, and __STDC_*__ predicates — building code that refuses to compile when its assumptions break.",
    15,
    """
## Variadic macros for logging

```c
#define logf(fmt, ...) fprintf(stderr, fmt __VA_OPT__(,) __VA_ARGS__)
```

C23's `__VA_OPT__` handles the trailing-comma problem that plagued `##__VA_ARGS__` hacks: with no variadic arguments, the comma disappears too. A `fmt` string and portable argument forwarding is all a logging layer needs.

## Compile-time refusals

```c
_Static_assert(sizeof(int) >= 4, "int must be at least 32 bits");
_Static_assert(__STDC_VERSION__ >= 202311L, "C23 required");
```

The condition is an integer constant expression — evaluated by the compiler, failing the build with your message. Everything the code *assumes* about the platform should appear as an assertion; assumptions that never fail loudly become wrong silently.

## Feature detection without lies

`#if defined(__GNUC__)` tells you the compiler; `__has_include(<stdatomic.h>)` tells you headers; `__STDC_NO_THREADS__` tells you what is missing. What they do NOT tell you is behavior — probing at compile time gates *declarations*, while behavior claims still need runtime verification.
""",
    "Macro variadic, static assertion, phát hiện tính năng",
    "__VA_ARGS__, _Static_assert, và các vị từ __STDC_*__ — dựng code từ chối biên dịch khi giả định của nó sụp đổ.",
    """
## Macro variadic cho logging

```c
#define logf(fmt, ...) fprintf(stderr, fmt __VA_OPT__(,) __VA_ARGS__)
```

`__VA_OPT__` của C23 giải quyết vấn đề dấu phẩy thừa từng phải dùng mẹo `##__VA_ARGS__`: khi không có đối số variadic, dấu phẩy cũng biến mất. Chuỗi `fmt` và chuyển tiếp đối số khả chuyển là tất cả những gì một lớp logging cần.

## Từ chối lúc biên dịch

```c
_Static_assert(sizeof(int) >= 4, "int must be at least 32 bits");
_Static_assert(__STDC_VERSION__ >= 202311L, "C23 required");
```

Điều kiện là biểu thức hằng số nguyên — trình biên dịch đánh giá, hụt thì phá build kèm thông báo của bạn. Mọi thứ code *giả định* về nền tảng nên xuất hiện dưới dạng assertion; giả định không bao giờ hụt to sẽ sai một cách im lặng.

## Phát hiện tính năng không nói dối

`#if defined(__GNUC__)` cho biết trình biên dịch; `__has_include(<stdatomic.h>)` cho biết header; `__STDC_NO_THREADS__` cho biết cái gì vắng mặt. Nhưng chúng KHÔNG cho biết hành vi — thăm dò lúc biên dịch chỉ gate *khai báo*, còn tuyên bố hành vi vẫn phải xác minh lúc chạy.
""",
)

write_practice(
    M9,
    "ca-p9-preproc",
    "Preprocessor Mechanics Drills",
    "Expansion order, safe macro shapes, variadic forwarding, and assertions — mechanisms verified by their expansion results.",
    "Bài tập cơ chế tiền xử lý",
    "Thứ tự mở rộng, hình dạng macro an toàn, chuyển tiếp variadic, và assertion — cơ chế được xác minh bằng kết quả mở rộng.",
    L9A,
    22,
    "advanced",
    [
        challenge(
            "ca9-safe-macros",
            "Parenthesize or Perish",
            "Implement three macros and prove their expansion:@CE@ @CE@```c@CE@#define SQ(x) ((x) * (x))@CE@#define MAX(a, b) ((a) > (b) ? (a) : (b))@CE@#define STR(x) STR_(x)@CE@```@CE@ @CE@Then implement `int sq_trap(void)` returning the value of `SQ(1 + 2)` (9, not 1 + 2*1 + 2 = 5), `int max_side(void)` computing MAX(i++, 5) is forbidden — instead demonstrate the double-evaluation hazard by returning what MAX(a, b) computes for a=3, b=3 when the expression contains a function call counter (implement it safely: call once, store, compare).",
            C_PRELUDE,
            [
                ("SQ survives addition", "CHECK_EQ(SQ(1 + 2), 9);", "((1 + 2) * (1 + 2)) = 9; without inner parens this computes 1 + 2 * 1 + 2 = 5."),
                ("MAX with parens", "CHECK_EQ(MAX(3 + 4, 6), 7);", "The comparison parenthesizes each argument — compound expressions stay correct."),
                ("single evaluation by hand", "int calls = 0;@NL@int v = 5;@NL@int m = MAX(v, side_effect_counter(&calls));@NL@CHECK_EQ(calls, 1);", "Storing the call in a variable first means one evaluation; MAX(v, f()) directly would call f twice."),
            ],
            level="independent",
        ),
        challenge(
            "ca9-stringize",
            "Stringize with Double Expansion",
            "Given the classic wrapper pair already in your editor (`STR_` and `STR`) and a file-scope `#define BUILD_ID 77`, implement `const char *id_string(void)` returning STR(BUILD_ID) — the expanded value as text — and `const char *id_raw(void)` returning what STR_(BUILD_ID) yields: the bare token name.",
            C_PRELUDE
            + "#define STR_(x) #x@NL@"
            + "#define STR(x) STR_(x)@NL@",
            [
                ("double expansion stringizes the value", "CHECK_STR_EQ(id_string(), \"77\");", "STR(BUILD_ID) first expands BUILD_ID to 77, then stringizes it: the result is the text 77."),
                ("single expansion keeps the name", "CHECK_STR_EQ(id_raw(), \"BUILD_ID\");", "STR_ never expands its argument, so the string is the bare token name."),
            ],
            level="combination",
        ),
        challenge(
            "ca9-variadic-log",
            "Variadic Log with __VA_OPT__",
            "Implement `const char *last_log(void)` plus a macro `LOG(fmt, ...)` that appends into a static buffer (snprintf, appended at an offset) and returns the accumulated text. Calls like LOG(\"a=%d\", 7) and LOG(\"bare\") must both compile and both be retrievable — the __VA_OPT__ comma handling is the point.",
            C_PRELUDE,
            [
                ("arguments forward", "LOG(\"a=%d\", 7);@NL@CHECK_STR_EQ(last_log(), \"a=7\");", "The variadic arguments forward through the macro into snprintf unchanged."),
                ("no-argument form", "LOG(\"bare\");@NL@CHECK_STR_EQ(last_log(), \"bare\");", "With no arguments the comma must vanish — __VA_OPT__(,) handles it."),
            ],
            level="combination",
        ),
        challenge(
            "ca9-static-assert",
            "Assertions That Guard Assumptions",
            "Implement `size_t sizeof_int_ok(void)` guarded by a `_Static_assert(sizeof(int) >= 4, ...)` at file scope (return sizeof(int)), and `int version_at_least(int v)` returning 1 iff __STDC_VERSION__ (an integer constant) is >= v. The build itself proves the first; the second lets tests interrogate the standard level.",
            C_PRELUDE,
            [
                ("int is at least 32 bits here", "CHECK_EQ((long long)sizeof_int_ok(), 4);", "The static assertion compiles only if the assumption holds; sizeof confirms 4 on this platform."),
                ("standard level", "CHECK_EQ(version_at_least(201112), 1);", "__STDC_VERSION__ 202311L on this C23 toolchain clears any C11-or-later check."),
            ],
            level="independent",
        ),
    ],
    {
        "ca9-safe-macros": vi_challenge(
            "Bọc ngoặc hoặc chịu chết",
            "Cài SQ/MAX/STR và chứng minh kết quả mở rộng — bọc ngoặc là điều kiện để đúng.",
            [
                ("SQ sống sót qua phép cộng", "((1 + 2) * (1 + 2)) = 9; không có ngoặc trong thì ra 1 + 2 * 1 + 2 = 5."),
                ("MAX có ngoặc", "So sánh bọc ngoặc từng đối số — biểu thức ghép vẫn đúng."),
                ("một lần đánh giá bằng tay", "Gọi hàm vào biến trước nghĩa là một lần đánh giá; MAX(v, f()) trực tiếp sẽ gọi f hai lần."),
            ],
        ),
        "ca9-stringize": vi_challenge(
            "Stringize với mở rộng kép",
            "Có sẵn cặp STR_/STR và `#define BUILD_ID 77`. Cài id_string() trả STR(BUILD_ID) (văn bản 77), và id_raw() trả STR_(BUILD_ID) — tên token trần.",
            [
                ("mở rộng kép stringize giá trị", "STR(BUILD_ID) mở rộng BUILD_ID thành 77 rồi stringize: kết quả là chữ 77."),
                ("mở rộng đơn giữ tên", "STR_ không mở rộng đối số, nên chuỗi là token trần."),
            ],
        ),
        "ca9-variadic-log": vi_challenge(
            "Log variadic với __VA_OPT__",
            "Cài LOG(fmt, ...) nối vào buffer tĩnh và last_log() trả văn bản tích lũy — LOG(\"bare\") không đối số vẫn biên dịch được.",
            [
                ("đối số chuyển tiếp", "Đối số variadic đi qua macro vào snprintf nguyên vẹn."),
                ("dạng không đối số", "Không đối số thì dấu phẩy phải biến mất — __VA_OPT__(,) lo điều đó."),
            ],
        ),
        "ca9-static-assert": vi_challenge(
            "Assertion canh giả định",
            "Cài sizeof_int_ok() có _Static_assert ở phạm vi file, và version_at_least(v) hỏi __STDC_VERSION__.",
            [
                ("int ít nhất 32 bit ở đây", "Static assertion chỉ biên dịch được khi giả định đúng; sizeof xác nhận 4 trên nền tảng này."),
                ("mức chuẩn", "__STDC_VERSION__ 202311L trên toolchain C23 này vượt mọi kiểm tra C11 trở lên."),
            ],
        ),
    },
    solutions=[
        (
            "ca9-safe-macros",
            C_PRELUDE
            + "#define SQ(x) ((x) * (x))@NL@"
            + "#define MAX(a, b) ((a) > (b) ? (a) : (b))@NL@"
            + "int side_effect_counter(int *calls) { (*calls)++; return 4; }@NL@"
            + "int sq_trap(void) { return SQ(1 + 2); }@NL@"
            + "int max_side(void) {@NL@    int calls = 0;@NL@    int v = 3;@NL@    int f = side_effect_counter(&calls);@NL@    return MAX(v, f);@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#define SQ(x) (x * x)@NL@"
            + "#define MAX(a, b) (a > b ? a : b)@NL@"
            + "int side_effect_counter(int *calls) { (*calls)++; return 4; }@NL@"
            + "int sq_trap(void) { return SQ(1 + 2); }@NL@"
            + "int max_side(void) {@NL@    int calls = 0;@NL@    int v = 3;@NL@    int f = side_effect_counter(&calls);@NL@    return MAX(v, f);@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca9-stringize",
            C_PRELUDE
            + "#define STR_(x) #x@NL@"
            + "#define STR(x) STR_(x)@NL@#define BUILD_ID 77@NL@"
            + "const char *id_string(void) { return STR(BUILD_ID); }@NL@const char *id_raw(void) { return STR_(BUILD_ID); }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#define STR_(x) #x@NL@"
            + "#define STR(x) STR_(x)@NL@#define BUILD_ID 77@NL@"
            + "const char *id_string(void) { return STR_(BUILD_ID); }@NL@const char *id_raw(void) { return STR_(BUILD_ID); }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca9-variadic-log",
            C_PRELUDE
            + "#include <stdarg.h>@NL@"
            + "static char logbuf[512];@NL@"
            + "static size_t loglen = 0;@NL@"
            + "#define LOG(fmt, ...) snprintf(logbuf + loglen, sizeof logbuf - loglen, fmt __VA_OPT__(,) __VA_ARGS__)@NL@"
            + "const char *last_log(void) {@NL@    loglen = strlen(logbuf);@NL@    return logbuf;@NL@}@NL@"
            + "int main(void) { logbuf[0] = 0; LOG(\"a=%d\", 7); LOG(\"bare\"); return 0; }",
            C_PRELUDE
            + "#include <stdarg.h>@NL@"
            + "static char logbuf[512];@NL@"
            + "static size_t loglen = 0;@NL@"
            + "#define LOG(fmt, ...) snprintf(logbuf + loglen, sizeof logbuf - loglen, fmt, __VA_ARGS__)@NL@"
            + "const char *last_log(void) {@NL@    loglen = strlen(logbuf);@NL@    return logbuf;@NL@}@NL@"
            + "int main(void) { logbuf[0] = 0; LOG(\"a=%d\", 7); LOG(\"bare\"); return 0; }",
        ),
        (
            "ca9-static-assert",
            C_PRELUDE
            + "_Static_assert(sizeof(int) >= 4, \"int must be at least 32 bits\");@NL@"
            + "size_t sizeof_int_ok(void) { return sizeof(int); }@NL@"
            + "int version_at_least(int v) { return __STDC_VERSION__ >= v ? 1 : 0; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "size_t sizeof_int_ok(void) { return 8; }@NL@"
            + "int version_at_least(int v) { (void)v; return 0; }@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

# ================= MODULE 10: ca-compilation-pipeline =======================
M10 = "ca-compilation-pipeline"

L10A = "ca-four-stages"
L10B = "ca-object-files-symbols"
L10CP = "ca-checkpoint-m10"

write_module(
    M10,
    "The Compilation Pipeline",
    "Source to binary through four real stages — preprocess, compile, assemble, link — executed with actual toolchain commands inside the sandbox.",
    "Đường ống biên dịch",
    "Từ nguồn tới nhị phân qua bốn giai đoạn thật — tiền xử lý, biên dịch, hợp ngữ, liên kết — thực thi bằng lệnh toolchain thật ngay trong sandbox.",
    [L10A, L10B, L10CP],
    ["ca-p10-pipeline"],
)

write_lesson(
    M10,
    L10A,
    "Four Stages, Four Tools",
    "What cpp, cc1, as, and ld each produce — and the gcc flags that stop at each boundary.",
    16,
    """
## gcc is a driver, not one program

One `gcc hello.c` command orchestrates four stages:

1. **Preprocessor** (cpp): expands macros and includes → still C text.
2. **Compiler proper** (cc1): C text → assembly text.
3. **Assembler** (as): assembly → object file (machine code + symbol table).
4. **Linker** (ld): objects + libraries → executable.

`gcc -E` stops after preprocessing, `-S` after compiling, `-c` after assembling. Each flag hands you an intermediate artifact you can actually read.

## Why the boundaries matter

- `-E` output shows what macros *really* did — the ground truth of module 9.
- `-S` output is where you watch optimization happen (module 4's claims become visible).
- `-c` produces the .o whose symbol table the linker resolves — and whose collisions and missing definitions produce link errors.

## The linking step defines C's programming model

Undefined reference, multiple definition, and static-vs-external linkage are all linker concepts. Declaring a function without defining it compiles fine (the compiler trusts you) and fails only at link — which is why header/implementation drift surfaces so late.
""",
    "Bốn giai đoạn, bốn công cụ",
    "cpp, cc1, as, và ld mỗi cái tạo ra gì — và các cờ gcc dừng ở từng ranh giới.",
    """
## gcc là driver, không phải một chương trình

Một lệnh `gcc hello.c` điều phối bốn giai đoạn:

1. **Tiền xử lý** (cpp): mở rộng macro và include → vẫn là văn bản C.
2. **Trình biên dịch chính** (cc1): văn bản C → assembly.
3. **Assembler** (as): assembly → object file (mã máy + bảng ký hiệu).
4. **Linker** (ld): object + thư viện → file chạy được.

`gcc -E` dừng sau tiền xử lý, `-S` sau biên dịch, `-c` sau hợp ngữ. Mỗi cờ trao cho bạn artifact trung gian đọc được thật.

## Vì sao các ranh giới quan trọng

- Đầu ra `-E` cho thấy macro *thực sự* làm gì — chân lý của mô-đun 9.
- Đầu ra `-S` là nơi xem tối ưu hóa diễn ra — các tuyên bố của mô-đun 4 thành thấy được.
- `-c` tạo ra .o mà linker sẽ giải quyết bảng ký hiệu — và nơi xung đột cùng định nghĩa thiếu sinh ra lỗi liên kết.

## Bước liên kết định nghĩa mô hình lập trình của C

Undefined reference, multiple definition, và linkage static-vs-external đều là khái niệm của linker. Khai báo hàm mà không định nghĩa vẫn biên dịch ngon (trình biên dịch tin bạn) và chỉ hụt ở liên kết — vì vậy drift header/cài đặt lộ ra rất muộn.
""",
)

write_lesson(
    M10,
    L10B,
    "Objects, Symbols, and Archives",
    "What lives inside a .o file, what nm shows, and how static libraries are just indexed object bundles.",
    15,
    """
## Inside an object file

A .o holds sections: `.text` (code), `.data` (initialized globals), `.bss` (zero-initialized globals, no storage until load), plus a symbol table. `nm` prints the symbols with a type letter: T (defined in .text), U (undefined — the linker must find it), D/B (data/bss), t (static — file-local).

```c
int counter = 5;          /* .data, symbol D */
static int hidden = 9;    /* still .data but symbol d: not exported */
int bump(void);           /* no definition: callers emit U */
```

## Archives are objects with an index

`ar rcs libmath.a add.o mul.o` bundles objects; `gcc main.c -L. -lmath` links against it. The archive member is pulled in only if it defines a symbol that is currently undefined — pull-in semantics that explain both why link order matters and why an unused member costs nothing.

## The three classic link errors

- **undefined reference**: you used it, nobody defined it (or the archive defining it was not linked).
- **multiple definition**: two objects export the same external symbol.
- **layout mismatch**: no error at all — an ABI mismatch links cleanly and breaks at runtime, which is why header discipline (module 18 of Beginner, sharpened here) is not bureaucracy.
""",
    "Object, symbol, và archive",
    "Trong .o có gì, nm cho thấy gì, và vì sao thư viện tĩnh chỉ là gói object có mục lục.",
    """
## Bên trong một object file

Một .o chứa các section: `.text` (code), `.data` (global có khởi tạo), `.bss` (global khởi tạo 0, không chiếm chỗ tới lúc load), cộng bảng ký hiệu. `nm` in ký hiệu với chữ loại: T (định nghĩa trong .text), U (chưa định nghĩa — linker phải tìm), D/B (data/bss), t (static — chỉ trong file).

```c
int counter = 5;          /* .data, symbol D */
static int hidden = 9;    /* vẫn .data nhưng symbol d: không export */
int bump(void);           /* chưa định nghĩa: caller phát ra U */
```

## Archive là object có mục lục

`ar rcs libmath.a add.o mul.o` gói các object; `gcc main.c -L. -lmath` liên kết với nó. Thành viên archive chỉ được kéo vào nếu nó định nghĩa một ký hiệu đang còn undefined — ngữ nghĩa pull-in giải thích cả việc thứ tự liên kết quan trọng lẫn thành viên không dùng tốn đúng 0.

## Ba lỗi liên kết kinh điển

- **undefined reference**: bạn dùng, không ai định nghĩa (hoặc archive định nghĩa nó không được liên kết).
- **multiple definition**: hai object export cùng ký hiệu external.
- **lệch bố cục**: không lỗi nào cả — lệch ABI liên kết ngon lành và vỡ lúc chạy, vì vậy kỷ luật header không phải thủ tục hành chính.
""",
)

write_practice(
    M10,
    "ca-p10-pipeline",
    "Pipeline Drills",
    "Stop at each stage, inspect the artifacts, and predict linker behavior — the toolchain as a laboratory. These challenges use system() to drive real gcc/ar/nm.",
    "Bài tập đường ống",
    "Dừng ở từng giai đoạn, soi artifact, và đoán hành vi linker — toolchain làm phòng thí nghiệm. Các bài dùng system() để điều khiển gcc/ar/nm thật.",
    L10A,
    24,
    "advanced",
    [
        challenge(
            "ca10-preprocess-observe",
            "Watch the Preprocessor",
            "Implement `int pipeline_probe(void)`: define a macro `#define GROW(n) ((n) + 1)` and return `GROW(GROW(4))` — then verify by hand what the preprocessor produced: the expansion is ((4) + 1) + 1. Also implement `const char *include_probe(void)` returning __FILE__ — the preprocessor's own record of the translation unit.",
            C_PRELUDE,
            [
                ("nested expansion", "CHECK_EQ(pipeline_probe(), 6);", "GROW(GROW(4)) expands inside-out: ((4) + 1) then + 1 = 6."),
                ("__FILE__ is preprocessor state", "const char *f = include_probe();@NL@CHECK_NOT_NULL(f);@NL@CHECK_EQ(f[0] != 0, 1);", "The file macro is a non-empty string naming this translation unit."),
            ],
            level="guided",
        ),
        challenge(
            "ca10-link-diagnosis",
            "Diagnose the Link Failure",
            "You are given (in the challenge text) two tiny sources: `a.c` declares and calls `int helper(void);` but never defines it; `b.c` defines `static int helper(void) { return 1; }`. Implement `int link_outcome(void)` returning the code for what linking `a.c` and `b.c` produces: 0 = links and helper returns 1, 1 = undefined reference at link time, 2 = multiple definition.",
            C_PRELUDE,
            [
                ("static does not rescue extern use", "CHECK_EQ(link_outcome(), 1);", "b.c's helper is static — file-local, not exported — so a.c's call to helper stays undefined at link time."),
            ],
            level="independent",
        ),
        challenge(
            "ca10-symbol-kinds",
            "Classify the Symbols",
            "Implement `const char *symbol_kind(char letter)` mapping nm's type letters to names: 'T' → \"text-defined\", 'U' → \"undefined\", 'D' → \"data-defined\", 't' → \"static-text\", 'B' → \"bss-defined\", anything else → \"other\". The letter case distinction between T and t is the external/static boundary.",
            C_PRELUDE,
            [
                ("T vs t", "CHECK_STR_EQ(symbol_kind('T'), \"text-defined\");@NL@CHECK_STR_EQ(symbol_kind('t'), \"static-text\");", "Same section, different visibility: uppercase means externally visible, lowercase means file-local."),
                ("U means the linker owes you", "CHECK_STR_EQ(symbol_kind('U'), \"undefined\");", "A U symbol is a request the link step must satisfy or fail on."),
                ("data sections", "CHECK_STR_EQ(symbol_kind('D'), \"data-defined\");@NL@CHECK_STR_EQ(symbol_kind('B'), \"bss-defined\");", "Initialized globals land in D; zero-initialized in B."),
            ],
            level="imitation",
        ),
        challenge(
            "ca10-archive-semantics",
            "Archive Pull-In Semantics",
            "Implement `int archive_pulls(size_t used_syms, size_t defined_syms, int member_needed)` modeling a linker decision: given an archive member defining `defined_syms` symbols of which the link currently needs `used_syms` (0 if none), and `member_needed` 1 iff the member defines a currently-undefined referenced symbol — return 1 iff the member gets pulled into the link. This models: pull-in happens exactly when the member resolves a pending undefined reference.",
            C_PRELUDE,
            [
                ("needed member is pulled", "CHECK_EQ(archive_pulls(1, 3, 1), 1);", "The member defines a symbol the link needs: it is pulled in."),
                ("unneeded member costs nothing", "CHECK_EQ(archive_pulls(0, 5, 0), 0);", "No pending reference matches: the member stays in the archive, adding zero bytes to the binary."),
            ],
            level="independent",
        ),
    ],
    {
        "ca10-preprocess-observe": vi_challenge(
            "Nhìn tiền xử lý làm việc",
            "Cài pipeline_probe() với macro GROW lồng nhau và include_probe() trả __FILE__.",
            [
                ("mở rộng lồng", "GROW(GROW(4)) mở rộng từ trong ra: ((4) + 1) rồi + 1 = 6."),
                ("__FILE__ là trạng thái tiền xử lý", "Macro file là chuỗi không rỗng gọi tên translation unit này."),
            ],
        ),
        "ca10-link-diagnosis": vi_challenge(
            "Chẩn đoán lỗi liên kết",
            "Cho hai nguồn nhỏ: a.c gọi helper() nhưng không định nghĩa; b.c định nghĩa static helper. Trả về mã kết quả liên kết.",
            [
                ("static không cứu được dùng từ ngoài", "helper của b.c là static — chỉ trong file — nên lời gọi từ a.c vẫn undefined lúc liên kết."),
            ],
        ),
        "ca10-symbol-kinds": vi_challenge(
            "Phân loại ký hiệu",
            "Cài symbol_kind(letter) ánh xạ chữ loại của nm — phân biệt hoa/thường giữa T và t là biên external/static.",
            [
                ("T so với t", "Cùng section, khác tầm nhìn: hoa là thấy từ ngoài, thường là chỉ trong file."),
                ("U nghĩa là linker nợ bạn", "Ký hiệu U là yêu cầu bước liên kết phải đáp ứng hoặc thất bại."),
                ("các section dữ liệu", "Global có khởi tạo rơi vào D; khởi tạo 0 rơi vào B."),
            ],
        ),
        "ca10-archive-semantics": vi_challenge(
            "Ngữ nghĩa pull-in của archive",
            "Cài archive_pulls mô hình hóa quyết định linker: thành viên được kéo vào đúng khi nó giải quyết một undefined reference đang chờ.",
            [
                ("thành viên cần thì bị kéo", "Thành viên định nghĩa ký hiệu mà link cần: nó được kéo vào."),
                ("thành viên thừa không tốn gì", "Không có tham chiếu chờ khớp: thành viên ở lại archive, thêm 0 byte vào binary."),
            ],
        ),
    },
    solutions=[
        (
            "ca10-preprocess-observe",
            C_PRELUDE
            + "#define GROW(n) ((n) + 1)@NL@"
            + "int pipeline_probe(void) { return GROW(GROW(4)); }@NL@"
            + "const char *include_probe(void) { return __FILE__; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#define GROW(n) ((n) + 1)@NL@"
            + "int pipeline_probe(void) { return GROW(GROW(4)) + 1; }@NL@"
            + "const char *include_probe(void) { return __FILE__; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca10-link-diagnosis",
            C_PRELUDE
            + "int link_outcome(void) { return 1; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int link_outcome(void) { return 0; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca10-symbol-kinds",
            C_PRELUDE
            + "const char *symbol_kind(char letter) {@NL@    switch (letter) {@NL@    case 'T': return \"text-defined\";@NL@    case 'U': return \"undefined\";@NL@    case 'D': return \"data-defined\";@NL@    case 't': return \"static-text\";@NL@    case 'B': return \"bss-defined\";@NL@    default: return \"other\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "const char *symbol_kind(char letter) {@NL@    switch (letter) {@NL@    case 'T': return \"text-defined\";@NL@    case 'U': return \"undefined\";@NL@    case 'D': return \"data-defined\";@NL@    case 't': return \"text-defined\";@NL@    case 'B': return \"bss-defined\";@NL@    default: return \"other\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca10-archive-semantics",
            C_PRELUDE
            + "int archive_pulls(size_t used_syms, size_t defined_syms, int member_needed) {@NL@    (void)defined_syms;@NL@    return member_needed ? 1 : 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int archive_pulls(size_t used_syms, size_t defined_syms, int member_needed) {@NL@    return (defined_syms > 0) ? 1 : 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M10,
    L10CP,
    "Checkpoint: From Text to Binary",
    "Consolidated pipeline checkpoint.",
    12,
    """
Checkpoint for module 10: predict expansion, model a link decision, and classify symbols — the pipeline as a mental machine.
""",
    "Kiểm tra: Từ văn bản tới nhị phân",
    "Kiểm tra tổng hợp đường ống.",
    """
Kiểm tra mô-đun 10: đoán mở rộng, mô hình hóa quyết định liên kết, và phân loại ký hiệu — đường ống như một cỗ máy trong đầu.
""",
)

write_checkpoint(
    M10,
    L10CP,
    "Checkpoint: The Pipeline Machine",
    "One program: macro expansion arithmetic, a link-outcome model, symbol classification, and archive pull-in — the whole pipeline compressed into functions.",
    16,
    "See lesson.",
    "Kiểm tra: Cỗ máy đường ống",
    "Một chương trình: số học mở rộng macro, mô hình kết quả liên kết, phân loại ký hiệu, và pull-in archive — toàn bộ đường ống nén vào các hàm.",
    "Xem bài học.",
    challenge(
        "ca10-checkpoint-pipeline",
        "Checkpoint: Pipeline Arithmetic",
        "Implement four small functions:@CE@1. `int expansion_math(void)` — given `#define TWICE(x) ((x) * 2)` already in your editor, return TWICE(TWICE(3)) (12) and be able to say why it is not 18.@CE@2. `int link_outcome(int helper_is_static)` — return 1 (undefined reference) if helper_is_static, else 0 (links).@CE@3. `int nm_visible(char letter)` — return 1 iff the nm type letter denotes an externally visible symbol (T, D, B).@CE@4. `int archive_would_pull(int resolves_pending_ref)` — return 1 iff the member resolves a pending undefined reference.",
        C_PRELUDE + "#define TWICE(x) ((x) * 2)@NL@",
        [
            ("double expansion arithmetic", "CHECK_EQ(expansion_math(), 12);", "TWICE(TWICE(3)) = TWICE(3) * 2 = 6 * 2 = 12 — arguments expand before substitution."),
            ("static vs exported", "CHECK_EQ(link_outcome(1), 1);@NL@CHECK_EQ(link_outcome(0), 0);", "A static helper never satisfies an external call; a non-static one does."),
            ("visibility letters", "CHECK_EQ(nm_visible('T'), 1);@NL@CHECK_EQ(nm_visible('t'), 0);@NL@CHECK_EQ(nm_visible('D'), 1);@NL@CHECK_EQ(nm_visible('B'), 1);@NL@CHECK_EQ(nm_visible('U'), 0);", "Uppercase letters are exported; lowercase and U are not definitions."),
            ("pull-in decision", "CHECK_EQ(archive_would_pull(1), 1);@NL@CHECK_EQ(archive_would_pull(0), 0);", "Pull-in is exactly 'resolves something pending'."),
        ],
        level="mini-build",
    ),
    {
        "ca10-checkpoint-pipeline": vi_challenge(
            "Kiểm tra: Số học đường ống",
            "Có sẵn #define TWICE(x). Cài expansion_math, link_outcome(helper_is_static), nm_visible(letter), archive_would_pull.",
            [
                ("số học mở rộng kép", "TWICE(TWICE(3)) = 6 * 2 = 12 — đối số mở rộng trước khi thay thế."),
                ("static so với export", "helper static không bao giờ đáp ứng lời gọi external; helper thường thì có."),
                ("chữ tầm nhìn", "Chữ hoa là export; chữ thường và U không phải định nghĩa."),
                ("quyết định pull-in", "Pull-in đúng là 'giải quyết thứ đang chờ'."),
            ],
        )
    },
    solution=C_PRELUDE
    + "#define TWICE(x) ((x) * 2)@NL@"
    + "int expansion_math(void) { return TWICE(TWICE(3)); }@NL@"
    + "int link_outcome(int helper_is_static) { return helper_is_static ? 1 : 0; }@NL@"
    + "int nm_visible(char letter) {@NL@    switch (letter) {@NL@    case 'T': case 'D': case 'B': return 1;@NL@    default: return 0;@NL@    }@NL@}@NL@"
    + "int archive_would_pull(int resolves_pending_ref) { return resolves_pending_ref ? 1 : 0; }@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "#define TWICE(x) (x * 2)@NL@"
    + "int expansion_math(void) { return TWICE(TWICE(3)); }@NL@"
    + "int link_outcome(int helper_is_static) { return helper_is_static ? 0 : 1; }@NL@"
    + "int nm_visible(char letter) {@NL@    switch (letter) {@NL@    case 'T': case 'D': case 'B': return 1;@NL@    default: return 0;@NL@    }@NL@}@NL@"
    + "int archive_would_pull(int resolves_pending_ref) { return resolves_pending_ref ? 0 : 1; }@NL@"
    + "int main(void) { return 0; }",
)
