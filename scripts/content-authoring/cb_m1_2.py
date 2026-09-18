#!/usr/bin/env python3
"""C Beginner — batch 1: modules 1 (first-programs) and 2 (variables-types).

Authoring-call shapes (single source of truth, cb.py):
  write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
  write_practice(m, sid, title, desc, vi_title, vi_desc, after_lesson, minutes, difficulty, challenges, vi_challenges, solutions)
  write_checkpoint(m, lid, title, desc, minutes, mdx, vi_title, vi_desc, vi_mdx, ch, vi_ch, solution, wrong)
"""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ============================ MODULE 1: first-programs ============================
M1 = "first-programs"

L1A = "what-is-c"
L1B = "anatomy-of-a-program"
L1C = "cb-checkpoint-m1"

write_module(
    M1,
    "What Is C?",
    "From source code to a running program: the compile pipeline, main(), printf, and your first working C.",
    "C là gì?",
    "Từ mã nguồn đến chương trình chạy được: quy trình biên dịch, main(), printf và chương trình C đầu tiên của bạn.",
    [L1A, L1B, L1C],
    ["cb-p1-hello", "cb-p1-fix-output"],
)

write_lesson(
    M1,
    L1A,
    "What Is C and Why It Still Matters",
    "Where C lives — operating systems, embedded devices, language runtimes — and what it means that C is compiled.",
    9,
    r"""
## Where C lives

C is a small, fast, close-to-the-machine language. It powers operating-system
kernels (Linux, Windows kernels), embedded firmware, database engines, and the
runtimes of languages like Python and Java. Learning C teaches you how the
machine actually behaves — memory, addresses, and exact types.

## Compiled, not interpreted

You write **source code** (a `.c` text file). A **compiler** translates it into
machine instructions, and a **linker** stitches the translated pieces plus the
standard library into one **executable** the CPU can run directly. Nothing
hides this pipeline from you in C — you will run it yourself in this course.

## The smallest complete program

```c
#include <stdio.h>

int main(void) {
    printf("Hello, C!\n");
    return 0;
}
```

- `#include <stdio.h>` — bring in the declarations for input/output (`printf`).
- `int main(void)` — every program starts here. `void` means it takes no
  parameters; the `int` result is a status code (`0` = success).
- `printf("...\n")` — write text to standard output. `\n` is a newline.
- `return 0;` — report success to whoever ran the program.

## Comments

```c
/* a block comment */
// a line comment (C99 and later)
```

Comments are for humans; the compiler deletes them.
""",
    "C là gì và vì sao nó vẫn quan trọng",
    "C sống ở đâu — hệ điều hành, thiết bị nhúng, runtime của ngôn ngữ khác — và \"biên dịch\" nghĩa là gì.",
    r"""
## C sống ở đâu

C là ngôn ngữ nhỏ, nhanh, gần với máy. Nó chạy trong nhân hệ điều hành (Linux,
Windows), firmware nhúng, cỗ máy cơ sở dữ liệu, và runtime của Python hay Java.
Học C giúp bạn hiểu máy móc thật sự vận hành: bộ nhớ, địa chỉ, kiểu dữ liệu chính xác.

## Biên dịch, không thông dịch

Bạn viết **mã nguồn** (tệp `.c`). **Trình biên dịch** dịch nó thành lệnh máy,
**trình liên kết** nối các mảnh đã dịch cùng thư viện chuẩn thành một **tệp
thực thi** CPU chạy trực tiếp. Trong C bạn sẽ tự chạy quy trình này.

## Chương trình nhỏ nhất nhưng hoàn chỉnh

```c
#include <stdio.h>

int main(void) {
    printf("Xin chao, C!\n");
    return 0;
}
```

- `#include <stdio.h>` — mang khai báo vào/ra (`printf`) vào tệp.
- `int main(void)` — mọi chương trình bắt đầu từ đây; `return 0` nghĩa là thành công.
- `printf("...\n")` — in văn bản ra đầu ra chuẩn; `\n` là xuống dòng.
- `return 0;` — báo hiệu chạy thành công.

## Chú thích

```c
/* chú thích khối */
// chú thích một dòng (từ C99)
```

Chú thích dành cho người đọc; trình biên dịch bỏ qua chúng.
""",
)

write_lesson(
    M1,
    L1B,
    "Anatomy of a Program (and Its Output)",
    "Statements, braces, escape sequences, and printing several lines — plus the exact output rules printf follows.",
    10,
    r"""
## Statements and braces

A statement is one instruction, ended with a semicolon. Braces `{ }` group
statements into a block — the body of `main` is a block. C does not care about
indentation, but humans do: always indent one level inside braces.

## Printing exactly

`printf` prints its format string literally, except for **escape sequences**
and **format specifiers**. The escapes you need now:

| Sequence | Meaning |
|---|---|
| `\n` | newline |
| `\t` | tab |
| `\"` | a literal `"` |
| `\\` | a literal `\` |

Two `printf` calls with no `\n` run together on one line. The newline goes
where you put it — this program prints `AB` then stops:

```c
printf("A");
printf("B\n");
```

## Multiple lines

```c
printf("Line one\n");
printf("Line two\n");
printf("\n");            // an empty line
printf("The end.\n");
```

Output:

```text
Line one
Line two

The end.
```

Exactness matters: in graded exercises, a missing space or newline is a wrong
answer. Read the required output character by character.
""",
    "Giải phẫu một chương trình (và đầu ra của nó)",
    "Câu lệnh, ngoặc nhọn, escape sequence và in nhiều dòng — cùng quy tắc đầu ra chính xác của printf.",
    r"""
## Câu lệnh và ngoặc nhọn

Một câu lệnh là một chỉ thị, kết thúc bằng dấu chấm phẩy. Cặp ngoặc `{ }` gom
các câu lệnh thành khối — thân của `main` là một khối. C không quan tâm thụt
lề, nhưng con người có: luôn thụt một cấp bên trong ngoặc.

## In chính xác

`printf` in chuỗi định dạng nguyên văn, trừ **escape sequence** và **định dạng
dạng %**. Các escape bạn cần ngay bây giờ:

| Chuỗi | Ý nghĩa |
|---|---|
| `\n` | xuống dòng |
| `\t` | tab |
| `\"` | dấu nháy kép `"` |
| `\\` | dấu gạch chéo `\` |

Hai lời `printf` không có `\n` sẽ in dính vào một dòng. Xuống dòng nằm ở nơi
bạn đặt nó.

## Nhiều dòng

```c
printf("Dong mot\n");
printf("Dong hai\n");
printf("\n");            // một dòng trống
printf("Het.\n");
```

Chính xác tuyệt đối là điểm số: thiếu một khoảng trắng hay xuống dòng là sai.
Đọc đầu ra yêu cầu từng ký tự một.
""",
)

write_practice(
    M1,
    "cb-p1-hello",
    "Hello Practice",
    "Write and shape your first C output: exact lines, exact newlines.",
    "Luyện Hello",
    "Viết và định hình dòng đầu ra C đầu tiên: đúng dòng, đúng xuống dòng.",
    L1A,
    12,
    "beginner",
    [
        challenge(
            "cb1-hello-journey",
            "Print a Greeting",
            "Implement `void program(void)` that prints exactly:\n\n```\nHello, Code Journey!\n```\n\nOne line, ending with a newline.",
            C_PRELUDE,
            [
                ("exact greeting", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "Hello, Code Journey!\\n");', "printf the text once, with \\n at the end."),
            ],
            level="imitation",
        ),
        challenge(
            "cb1-three-lines",
            "Three Lines",
            "Implement `void program(void)` that prints exactly three lines:\n\n```\nC is compiled\nfast and small\nI am learning it\n```\n\nNothing else — no extra blank lines.",
            C_PRELUDE,
            [
                ("three exact lines", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "C is compiled\\nfast and small\\nI am learning it\\n");', "One printf per line (or one printf with two \\n inside)."),
            ],
            level="imitation",
        ),
    ],
    {
        "cb1-hello-journey": vi_challenge(
            "In lời chào",
            "Cài `void program(void)` in đúng một dòng `Hello, Code Journey!` kết thúc bằng xuống dòng.",
            [("lời chào chính xác", "printf một lần, có \\n ở cuối.")],
        ),
        "cb1-three-lines": vi_challenge(
            "Ba dòng",
            "Cài `void program(void)` in đúng ba dòng như đề bài, không thừa dòng trống.",
            [("ba dòng chính xác", "Một printf mỗi dòng (hoặc một printf chứa hai \\n).")],
        ),
    },
    solutions=[
        (
            "cb1-hello-journey",
            "#include <stdio.h>\nvoid program(void) { printf(\"Hello, Code Journey!\\n\"); }\nint main(void) { program(); return 0; }",
            "#include <stdio.h>\nvoid program(void) { printf(\"Hello, Code Journey\"); }\nint main(void) { program(); return 0; }",
        ),
        (
            "cb1-three-lines",
            "#include <stdio.h>\nvoid program(void) {\n    printf(\"C is compiled\\n\");\n    printf(\"fast and small\\n\");\n    printf(\"I am learning it\\n\");\n}\nint main(void) { program(); return 0; }",
            "#include <stdio.h>\nvoid program(void) {\n    printf(\"C is compiled\\nfast and small\\nI am learning it\");\n}\nint main(void) { program(); return 0; }",
        ),
    ],
)

write_practice(
    M1,
    "cb-p1-fix-output",
    "Fix the Output",
    "A program compiles but prints the wrong thing. Diagnose and repair.",
    "Sửa đầu ra",
    "Chương trình biên dịch được nhưng in sai. Chẩn đoán và sửa.",
    L1B,
    10,
    "beginner",
    [
        challenge(
            "cb1-fix-newline",
            "Missing Newlines",
            "This program was supposed to print three lines but everything runs together on one line. Fix `program` so the output is exactly:\n\n```\nA\nB\nC\n```\n\nDo not change how many times it prints — fix the newlines.",
            '#include <stdio.h>\n\nvoid program(void) {\n    /* BROKEN: prints ABC on one line */\n    printf("A");\n    printf("B");\n    printf("C");\n}\n\nint main(void) { program(); return 0; }',
            [
                ("three lines now", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "A\\nB\\nC\\n");', "Each line needs its own \\n (or one \\n between them)."),
            ],
            level="debugging",
        ),
    ],
    {
        "cb1-fix-newline": vi_challenge(
            "Thiếu xuống dòng",
            "Chương trình lẽ ra in ba dòng nhưng tất cả dính một dòng. Sửa `program` để in đúng A\\nB\\nC\\n — không đổi số lần in.",
            [("ba dòng", "Mỗi dòng cần \\n của riêng nó.")],
        ),
    },
    solutions=[
        (
            "cb1-fix-newline",
            "#include <stdio.h>\nvoid program(void) {\n    printf(\"A\\n\");\n    printf(\"B\\n\");\n    printf(\"C\\n\");\n}\nint main(void) { program(); return 0; }",
            "#include <stdio.h>\nvoid program(void) {\n    printf(\"A\");\n    printf(\"B\\n\");\n    printf(\"C\");\n}\nint main(void) { program(); return 0; }",
        ),
    ],
)

write_checkpoint(
    M1,
    L1C,
    "Checkpoint: What Is C?",
    "One integrated challenge over module 1: exact multi-line output.",
    12,
    r"""
## Checkpoint

You can now read a complete C program and predict — then verify — its exact
output. The checkpoint grades a small "program banner": three parts, exact
newlines, an escape sequence used correctly.
""",
    "Điểm kiểm tra: C là gì?",
    "Một thử thách tích hợp cho mô-đun 1: đầu ra nhiều dòng chính xác.",
    r"""
## Điểm kiểm tra

Bạn đã có thể đọc một chương trình C hoàn chỉnh và dự đoán — rồi xác minh —
đầu ra chính xác của nó. Điểm kiểm tra chấm một "banner" nhỏ: ba phần, xuống
dòng chính xác, dùng đúng một escape sequence.
""",
    challenge(
        "cb1-checkpoint-banner",
        "Program Banner",
        "Implement `void program(void)` printing exactly:\n\n```\n=== CJ BANK ===\n \"Trusted C\" \n==============\n```\n\nLine 2 contains a leading space, the quoted words (with real `\"` characters), and a trailing space.",
        C_PRELUDE,
        [
            (
                "exact banner",
                'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "=== CJ BANK ===\\n \\"Trusted C\\" \\n==============\\n");',
                "Use \\\" for the quote characters; mind the leading/trailing spaces on line 2.",
            ),
        ],
    ),
    vi_challenge(
        "Banner chương trình",
        "Cài `void program(void)` in đúng banner ba dòng như đề bài; dòng 2 có dấu cách đầu/cuối và dấu nháy kép thật (dùng \\\" ).",
        [("banner chính xác", "Dùng \\\" cho ký tự nháy; chú ý khoảng trắng ở dòng 2.")],
    ),
    solution='#include <stdio.h>\nvoid program(void) {\n    printf("=== CJ BANK ===\\n");\n    printf(" \\"Trusted C\\" \\n");\n    printf("==============\\n");\n}\nint main(void) { program(); return 0; }',
    wrong='#include <stdio.h>\nvoid program(void) {\n    printf("=== CJ BANK ===\\n");\n    printf("\\"Trusted C\\"\\n");\n    printf("==============\\n");\n}\nint main(void) { program(); return 0; }',
)

# ============================ MODULE 2: variables-types ============================
M2 = "variables-types"

L2A = "variables-and-assignment"
L2B = "types-and-limits"
L2C = "constants-sizeof"
L2D = "cb-checkpoint-m2"

write_module(
    M2,
    "Variables & Types",
    "Names for values: declaration, initialization, assignment, the core types, signedness, constants, and sizeof.",
    "Biến & Kiểu",
    "Tên gọi cho giá trị: khai báo, khởi tạo, gán, các kiểu cốt lõi, có dấu/không dấu, hằng số và sizeof.",
    [L2A, L2B, L2C, L2D],
    ["cb-p2-values", "cb-p2-sizeof"],
)

write_lesson(
    M2,
    L2A,
    "Variables, Declaration & Assignment",
    "A variable is a named box of memory. Declaration creates it, assignment replaces its content, initialization does both at once.",
    10,
    r"""
## Boxes with names

A variable is a named region of memory holding a value of one type.

```c
int score;          // declaration: box exists, content UNSET
score = 42;         // assignment: put 42 in the box
int lives = 3;      // declaration + initialization together
```

**Reading an uninitialized variable is undefined behavior.** The compiler may
warn; the program may print garbage. Rule: initialize on declaration whenever
you can.

## Assignment replaces

```c
int x = 1;
x = 2;      // x is now 2; the 1 is gone
x = x + 5;  // right side computed first: 2 + 5 = 7
x += 5;     // shorthand for x = x + 5
```

Assignment is not equality — it is a command: "evaluate the right side, store
it into the left side".

## Multiple variables

```c
int a = 1, b = 2;   // legal but style prefers one per line
```
""",
    "Biến, khai báo & gán",
    "Biến là một hộp bộ nhớ có tên. Khai báo tạo hộp, gán thay nội dung, khởi tạo làm cả hai cùng lúc.",
    r"""
## Hộp có tên

Biến là một vùng bộ nhớ có tên, giữ một giá trị thuộc đúng một kiểu.

```c
int score;          // khai báo: hộp tồn tại, nội dung CHƯA XÁC ĐỊNH
score = 42;         // gán: đưa 42 vào hộp
int lives = 3;      // khai báo + khởi tạo cùng lúc
```

**Đọc biến chưa khởi tạo là hành vi không xác định.** Trình biên dịch có thể
cảnh báo; chương trình có thể in rác. Quy tắc: khởi tạo ngay khi khai báo.

## Gán là thay thế

```c
int x = 1;
x = 2;      // x giờ là 2; giá trị 1 biến mất
x = x + 5;  // tính vế phải trước: 2 + 5 = 7
x += 5;     // viết tắt của x = x + 5
```

Gán không phải dấu bằng — nó là mệnh lệnh: "tính vế phải, cất vào vế trái".
""",
)

write_lesson(
    M2,
    L2B,
    "The Core Types: int, char, float, double",
    "Exact ranges and behavior of the everyday types, what signed/unsigned means, and how char is secretly a small integer.",
    11,
    r"""
## The everyday types

| Type | Typical size | Holds |
|---|---|---|
| `int` | 4 bytes | whole numbers, about ±2.1 billion |
| `char` | 1 byte | one character — and a small integer (-128..127) |
| `float` | 4 bytes | approximate real numbers, ~7 significant digits |
| `double` | 8 bytes | approximate real numbers, ~15 significant digits |

Sizes are *typical*, not guaranteed — that is what `sizeof` (next lesson) is
for. `%zu` prints a `size_t` (what `sizeof` returns).

## char is a number

```c
char c = 'A';        // character literal — a single quote
printf("%d\n", c);   // 65 — the ASCII code
printf("%c\n", c);   // A
```

`'A' + 1` is `'B'`. This identity between characters and small integers powers
text processing in C.

## signed and unsigned

An `int` is **signed** by default: it can be negative. `unsigned int` drops the
sign and doubles the positive range. Mixing them in one expression is a classic
bug source — for now, keep arithmetic in signed types.

## float vs double

`float` rounds sooner. Default your real-number work to `double`
(`printf("%f", ...)` prints a double).
""",
    "Các kiểu cốt lõi: int, char, float, double",
    "Miền giá trị và hành vi của các kiểu hằng ngày, signed/unsigned nghĩa là gì, và char thực chất là số nguyên nhỏ.",
    r"""
## Các kiểu hằng ngày

| Kiểu | Kích thước thường gặp | Chứa |
|---|---|---|
| `int` | 4 byte | số nguyên, khoảng ±2,1 tỷ |
| `char` | 1 byte | một ký tự — và một số nguyên nhỏ (-128..127) |
| `float` | 4 byte | số thực xấp xỉ, ~7 chữ số có nghĩa |
| `double` | 8 byte | số thực xấp xỉ, ~15 chữ số có nghĩa |

Kích thước là *thường gặp*, không đảm bảo — đó là lý do có `sizeof`. `%zu` in
một `size_t` (kiểu trả về của `sizeof`).

## char là một số

```c
char c = 'A';        // ký tự literal — nháy đơn
printf("%d\n", c);   // 65 — mã ASCII
printf("%c\n", c);   // A
```

`'A' + 1` là `'B'`. Đồng nhất ký tự–số nguyên này là nền của xử lý văn bản trong C.

## signed và unsigned

`int` mặc định **có dấu**: có thể âm. `unsigned int` bỏ dấu và nhân đôi miền
dương. Trộn chúng trong một biểu thức là nguồn lỗi kinh điển — hiện tại, hãy
giữ phép tính trong các kiểu có dấu.

## float hay double

`float` làm tròn sớm hơn. Mặc định dùng `double` cho số thực
(`printf("%f", ...)` in một double).
""",
)

write_lesson(
    M2,
    L2C,
    "Constants and sizeof",
    "Values that cannot change (const, #define) and asking the compiler how big things really are.",
    9,
    r"""
## Constants

A `const` variable cannot be assigned after initialization:

```c
const int MAX_USERS = 100;
MAX_USERS = 5;   // compile error
```

`#define` is a preprocessor text substitution — different mechanism, same goal
for simple constants:

```c
#define MAX_USERS 100   // no semicolon, no equals
```

Prefer `const` for typed constants; you will meet the preprocessor properly in
module 17.

## sizeof asks the compiler

`sizeof` yields the size of a type or expression **in bytes**; its result type
is `size_t`, printed with `%zu`:

```c
printf("%zu\n", sizeof(int));      // typically 4
printf("%zu\n", sizeof(double));   // typically 8
char c = 'x';
printf("%zu\n", sizeof(c));        // 1
```

`sizeof` is evaluated at compile time for types — no runtime cost.
""",
    "Hằng số và sizeof",
    "Giá trị không thể đổi (const, #define) và cách hỏi trình biên dịch một thứ lớn bao nhiêu byte.",
    r"""
## Hằng số

Biến `const` không thể gán sau khi khởi tạo:

```c
const int MAX_USERS = 100;
MAX_USERS = 5;   // lỗi biên dịch
```

`#define` là thay thế văn bản của bộ tiền xử lý — cơ chế khác, cùng mục tiêu
cho hằng đơn giản:

```c
#define MAX_USERS 100   // không chấm phẩy, không dấu bằng
```

Ưu tiên `const` cho hằng có kiểu; bạn sẽ gặp tiền xử lý kỹ ở mô-đun 17.

## sizeof hỏi trình biên dịch

`sizeof` cho kích thước của một kiểu hoặc biểu thức **tính bằng byte**; kết quả
thuộc kiểu `size_t`, in bằng `%zu`:

```c
printf("%zu\n", sizeof(int));      // thường là 4
printf("%zu\n", sizeof(double));   // thường là 8
char c = 'x';
printf("%zu\n", sizeof(c));        // 1
```

`sizeof` được tính lúc biên dịch cho kiểu — không tốn chi phí chạy.
""",
)

write_practice(
    M2,
    "cb-p2-values",
    "Value Surgery",
    "Declare, assign, and re-assign — prove you know what each variable holds at the end.",
    "Phẫu thuật giá trị",
    "Khai báo, gán và gán lại — chứng minh bạn biết mỗi biến chứa gì ở cuối.",
    L2A,
    14,
    "beginner",
    [
        challenge(
            "cb2-final-value",
            "Final Value",
            "Implement `int final_value(void)` that performs exactly this sequence with one local `int x`: start at 10, add 5, double it (x = x * 2), subtract 3. Return the final value.",
            C_PRELUDE,
            [
                ("final value is 27", "CHECK_EQ(final_value(), 27);", "10 + 5 = 15; 15 * 2 = 30; 30 - 3 = 27."),
            ],
            level="imitation",
        ),
        challenge(
            "cb2-swap-via-temp",
            "Swap with a Temp",
            "Implement `void swap(int* a, int* b)` that exchanges the two ints through the pointers using a temporary. (Full pointer theory comes in module 11; for now the pattern `*a` means \"the int a points at\".)",
            C_PRELUDE,
            [
                ("swaps two values", "int x = 3; int y = 8;\nswap(&x, &y);\nCHECK_EQ(x, 8);\nCHECK_EQ(y, 3);", "int t = *a; *a = *b; *b = t;"),
                ("swap with equal values", "int x = 5; int y = 5;\nswap(&x, &y);\nCHECK_EQ(x, 5);\nCHECK_EQ(y, 5);", "The temp-based swap handles equal values naturally."),
            ],
            level="guided",
        ),
        challenge(
            "cb2-char-math",
            "Character Arithmetic",
            "Implement `char letter_at(int index)` that returns the uppercase letter at `index` from 'A' (so 0 -> 'A', 2 -> 'C', 25 -> 'Z'). One arithmetic expression on a char base is enough.",
            C_PRELUDE,
            [
                ("first letter", "CHECK_EQ(letter_at(0), 'A');", "Start from 'A' and add the index."),
                ("middle letter", "CHECK_EQ(letter_at(2), 'C');", "'A' + 2 is 'C'."),
                ("last letter", "CHECK_EQ(letter_at(25), 'Z');", "'A' + 25 is 'Z'."),
            ],
            level="guided",
        ),
    ],
    {
        "cb2-final-value": vi_challenge(
            "Giá trị cuối",
            "Cài `int final_value(void)` dùng một biến `int x` cục bộ: bắt đầu 10, cộng 5, nhân đôi, trừ 3. Trả về giá trị cuối.",
            [("kết quả là 27", "10 + 5 = 15; 15 * 2 = 30; 30 - 3 = 27.")],
        ),
        "cb2-swap-via-temp": vi_challenge(
            "Hoán đổi bằng biến tạm",
            "Cài `void swap(int* a, int* b)` hoán đổi hai số nguyên qua con trỏ bằng một biến tạm. (`*a` nghĩa là \"số nguyên mà a trỏ tới\".)",
            [("hoán đổi hai giá trị", "int t = *a; *a = *b; *b = t;"), ("hai giá trị bằng nhau", "Hoán đổi kiểu tạm xử lý trường hợp bằng nhau tự nhiên.")],
        ),
        "cb2-char-math": vi_challenge(
            "Phép tính ký tự",
            "Cài `char letter_at(int index)` trả về chữ hoa tại `index` tính từ 'A' (0 -> 'A', 25 -> 'Z').",
            [("chữ đầu", "Xuất phát từ 'A' cộng chỉ số."), ("chữ giữa", "'A' + 2 là 'C'."), ("chữ cuối", "'A' + 25 là 'Z'.")],
        ),
    },
    solutions=[
        (
            "cb2-final-value",
            "#include <stdio.h>\nint final_value(void) {\n    int x = 10;\n    x = x + 5;\n    x = x * 2;\n    x = x - 3;\n    return x;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nint final_value(void) {\n    int x = 10;\n    x = x + 5;\n    x = x + 2;\n    x = x - 3;\n    return x;\n}\nint main(void) { return 0; }",
        ),
        (
            "cb2-swap-via-temp",
            "#include <stdio.h>\nvoid swap(int* a, int* b) {\n    int t = *a;\n    *a = *b;\n    *b = t;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nvoid swap(int* a, int* b) {\n    int t = a;\n    *a = *b;\n    *b = t;\n}\nint main(void) { return 0; }",
        ),
        (
            "cb2-char-math",
            "#include <stdio.h>\nchar letter_at(int index) {\n    return (char)('A' + index);\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nchar letter_at(int index) {\n    return (char)('a' + index);\n}\nint main(void) { return 0; }",
        ),
    ],
)

write_practice(
    M2,
    "cb-p2-sizeof",
    "Size Detective",
    "Use sizeof and printf to report the real sizes and values on this platform.",
    "Thám tử kích thước",
    "Dùng sizeof và printf để báo kích thước và giá trị thật trên nền tảng này.",
    L2C,
    12,
    "beginner",
    [
        challenge(
            "cb2-sizeof-report",
            "Sizeof Report",
            "Implement `void program(void)` printing exactly two lines using `%zu`:\n\n```\nint=4\ndouble=8\n```\n\nDo NOT hard-code the digits — compute them with `sizeof`.",
            C_PRELUDE,
            [
                ("computed sizeof lines", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "int=4\\ndouble=8\\n");', 'printf("int=%zu\\n", sizeof(int)); — %zu is the size_t specifier.'),
            ],
            level="guided",
        ),
    ],
    {
        "cb2-sizeof-report": vi_challenge(
            "Báo cáo sizeof",
            "Cài `void program(void)` in đúng hai dòng dùng `%zu` cho sizeof(int) và sizeof(double) — không hard-code con số.",
            [("dòng sizeof tính được", 'printf("int=%zu\\n", sizeof(int)); — %zu là định dạng cho size_t.')],
        ),
    },
    solutions=[
        (
            "cb2-sizeof-report",
            "#include <stdio.h>\nvoid program(void) {\n    printf(\"int=%zu\\n\", sizeof(int));\n    printf(\"double=%zu\\n\", sizeof(double));\n}\nint main(void) { program(); return 0; }",
            "#include <stdio.h>\nvoid program(void) {\n    printf(\"int=%zu\\n\", sizeof(double));\n    printf(\"double=%zu\\n\", sizeof(int));\n}\nint main(void) { program(); return 0; }",
        ),
    ],
)

write_checkpoint(
    M2,
    L2D,
    "Checkpoint: Variables & Types",
    "Integrated: typed values, char arithmetic, and computed sizeof output in one program.",
    14,
    r"""
## Checkpoint

Module 2 in one program: pick types deliberately, compute from a character
code, and report sizes the computed way.
""",
    "Điểm kiểm tra: Biến & Kiểu",
    "Tích hợp: giá trị có kiểu, phép tính ký tự, và đầu ra sizeof theo cách tính toán.",
    r"""
## Điểm kiểm tra

Mô-đun 2 trong một chương trình: chọn kiểu có chủ đích, tính từ mã ký tự, và
báo kích thước theo cách tính toán.
""",
    challenge(
        "cb2-checkpoint-profile",
        "Computed Profile",
        "Implement `void program(void)` that prints exactly:\n\n```\ngrade=D (68)\nint bytes=4\n```\n\nLine 1: compute the character `'D'` from `'A' + 3` (print it with %c) and its numeric code with %d. Line 2: compute the byte count with `sizeof(int)` and `%zu`. Do not hard-code `D`, `68`, or `4`.",
        C_PRELUDE,
        [
            (
                "computed profile",
                'const char* out = cj_capture(program);\nCHECK_CONTAINS(out, "grade=D (68)");\nCHECK_CONTAINS(out, "int bytes=4");',
                "char g = 'A' + 3; printf(\"grade=%c (%d)\\n\", g, g); then printf(\"int bytes=%zu\\n\", sizeof(int));",
            ),
        ],
    ),
    vi_challenge(
        "Hồ sơ tính toán",
        "Cài `void program(void)` in đúng hai dòng: ký tự 'D' tính từ 'A' + 3 (in bằng %c) và mã số của nó (%d); sau đó số byte của int bằng sizeof(int) với %zu. Không hard-code D, 68, hay 4.",
        [("hồ sơ tính được", "char g = 'A' + 3; in %c và %d; rồi sizeof(int) với %zu.")],
    ),
    solution='#include <stdio.h>\nvoid program(void) {\n    char g = (char)(\'A\' + 3);\n    printf("grade=%c (%d)\\n", g, g);\n    printf("int bytes=%zu\\n", sizeof(int));\n}\nint main(void) { program(); return 0; }',
    wrong='#include <stdio.h>\nvoid program(void) {\n    char g = (char)(\'A\' + 4);\n    printf("grade=%c (%d)\\n", g, g);\n    printf("int bytes=%zu\\n", sizeof(int));\n}\nint main(void) { program(); return 0; }',
)

print("batch 1 complete: modules 1-2")
