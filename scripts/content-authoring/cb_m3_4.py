#!/usr/bin/env python3
"""C Beginner — batch 2: modules 3 (io-formatting) and 4 (operators-expressions).

Sandbox honesty note: the graded sandbox is non-interactive, so "reading
input" is graded as parse logic with sscanf on provided strings; interactive
scanf habits are taught in prose with safety rules (width limits).
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

# ============================ MODULE 3: io-formatting ============================
M3 = "io-formatting"

L3A = "format-specifiers"
L3B = "parsing-input"
L3C = "cb-checkpoint-m3"

write_module(
    M3,
    "Input & Output",
    "Format specifiers in depth, field widths and precision, and reading values from text the safe way.",
    "Vào & Ra",
    "Định dạng dạng % sâu hơn, độ rộng trường và độ chính xác, và đọc giá trị từ văn bản một cách an toàn.",
    [L3A, L3B, L3C],
    ["cb-p3-format", "cb-p3-parse"],
)

write_lesson(
    M3,
    L3A,
    "Format Specifiers, Width & Precision",
    "The full % vocabulary for the core types, plus minimum widths, zero padding, and decimal precision.",
    11,
    r"""
## The % vocabulary

| Specifier | Prints | Example |
|---|---|---|
| `%d` | int (decimal) | `42` |
| `%c` | one character | `A` |
| `%s` | a C string | `hi` |
| `%f` | double, 6 decimals default | `3.141593` |
| `%e` | double, scientific | `3.141593e+00` |
| `%zu` | size_t (sizeof results) | `4` |
| `%%` | a literal percent | `50%` |

## Width and padding

A number between `%` and the letter sets a **minimum width**:

```c
printf("[%5d]\n", 42);     // [   42]  — right-aligned, space-padded
printf("[%-5d]\n", 42);    // [42   ]  — left-aligned
printf("[%05d]\n", 42);    // [00042]  — zero-padded
```

## Precision

For `%f`, `.N` sets digits after the decimal point (rounding, not truncating):

```c
printf("%.2f\n", 3.14159);   // 3.14
printf("%.0f\n", 2.5);       // 2  (banker's-ish rounding of exactly .5)
```

Combined: `%8.2f` = at least 8 characters wide, 2 decimals.
""",
    "Định dạng dạng %, độ rộng & độ chính xác",
    "Toàn bộ từ vựng % cho các kiểu cốt lõi, cùng độ rộng tối thiểu, đệm số 0 và độ chính xác thập phân.",
    r"""
## Từ vựng %

| Định dạng | In | Ví dụ |
|---|---|---|
| `%d` | int (thập phân) | `42` |
| `%c` | một ký tự | `A` |
| `%s` | chuỗi C | `hi` |
| `%f` | double, 6 số lẻ mặc định | `3.141593` |
| `%e` | double, dạng khoa học | `3.141593e+00` |
| `%zu` | size_t (kết quả sizeof) | `4` |
| `%%` | dấu phần trăm thật | `50%` |

## Độ rộng và đệm

Một số giữa `%` và chữ cái đặt **độ rộng tối thiểu**:

```c
printf("[%5d]\n", 42);     // [   42]  — căn phải, đệm dấu cách
printf("[%-5d]\n", 42);    // [42   ]  — căn trái
printf("[%05d]\n", 42);    // [00042]  — đệm số 0
```

## Độ chính xác

Với `%f`, `.N` đặt số chữ số sau dấu thập phân (làm tròn, không cắt):

```c
printf("%.2f\n", 3.14159);   // 3.14
```

Kết hợp: `%8.2f` = rộng ít nhất 8 ký tự, 2 số lẻ.
""",
)

write_lesson(
    M3,
    L3B,
    "Reading Input — and Parsing Text Safely",
    "How scanf works interactively, why it is dangerous without width limits, and the sscanf pattern graded in this course.",
    12,
    r"""
## Interactive input: scanf, carefully

`scanf("%d", &n)` reads whitespace-separated tokens from standard input.
Note the `&` — scanf needs the **address** of `n` to store into (module 11
explains why). Always check its return value: the number of items successfully
read.

```c
int n;
if (scanf("%d", &n) == 1) {
    printf("read %d\n", n);
}
```

**Danger:** `scanf("%s", buf)` with no width can overflow `buf` with long
input — a buffer overflow, the classic C vulnerability. With a width it is
bounded: `scanf("%63s", buf)` reads at most 63 characters plus the terminator
into a 64-byte buffer.

## The graded pattern: sscanf

This course's challenges run non-interactively, so graded input handling uses
`sscanf` — the same parsing engine, reading from a string instead of stdin:

```c
const char* line = "Alice 42";
char name[32]; int age = 0;
int got = sscanf(line, "%31s %d", name, &age);
// got == 2, name == "Alice", age == 42
```

The skill being graded is identical to reading user input: describe the shape
of the line, extract the fields, verify the count.
""",
    "Đọc dữ liệu vào — và phân tích văn bản an toàn",
    "scanf hoạt động thế nào khi tương tác, vì sao nguy hiểm khi thiếu giới hạn độ rộng, và mẫu sscanf được chấm trong khóa này.",
    r"""
## Vào tương tác: scanf, cẩn thận

`scanf("%d", &n)` đọc các token cách nhau bởi khoảng trắng từ đầu vào chuẩn.
Chú ý `&` — scanf cần **địa chỉ** của `n` để lưu vào (mô-đun 11 giải thích).
Luôn kiểm tra giá trị trả về: số mục đọc thành công.

```c
int n;
if (scanf("%d", &n) == 1) {
    printf("read %d\n", n);
}
```

**Nguy hiểm:** `scanf("%s", buf)` không có độ rộng có thể làm tràn `buf` với
đầu vào dài — tràn bộ đệm, lỗ hổng kinh điển của C. Có độ rộng thì bị chặn:
`scanf("%63s", buf)` đọc tối đa 63 ký tự cộng dấu kết thúc vào bộ đệm 64 byte.

## Mẫu được chấm: sscanf

Các thử thách của khóa này chạy không tương tác, nên xử lý đầu vào được chấm
qua `sscanf` — cùng cỗ máy phân tích, đọc từ chuỗi thay vì stdin:

```c
const char* line = "Alice 42";
char name[32]; int age = 0;
int got = sscanf(line, "%31s %d", name, &age);
// got == 2, name == "Alice", age == 42
```

Kỹ năng được chấm giống hệt đọc输入 của người dùng: mô tả dạng của dòng, tách
trường, xác minh số lượng.
""",
)

write_practice(
    M3,
    "cb-p3-format",
    "Format Workshop",
    "Produce exactly-formatted columns, padding, and rounded numbers.",
    "Xưởng định dạng",
    "Tạo cột, đệm và số làm tròn đúng định dạng yêu cầu.",
    L3A,
    14,
    "beginner",
    [
        challenge(
            "cb3-column-table",
            "Aligned Table",
            "Implement `void program(void)` printing a right-aligned two-column table:\n\n```\n  name | qty\n apple |   3\n mango |  12\n```\n\nColumn 1 is left-aligned width 6; column 2 is right-aligned width 3. Spaces around `|` exactly as shown.",
            C_PRELUDE,
            [
                ("exact table", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "name   | qty\\napple  |   3\\nmango  |  12\\n");', 'printf("%-6s | %3s\\n", "name", "qty"); then ints with %3d.'),
            ],
            level="guided",
        ),
        challenge(
            "cb3-money-format",
            "Money Format",
            "Implement `void program(void)` printing three prices, each on its own line, formatted as dollars with exactly 2 decimals: `1.5` -> `$1.50`, `12` -> `$12.00`, `0.05` -> `$0.05`.",
            C_PRELUDE,
            [
                ("exact money lines", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "$1.50\\n$12.00\\n$0.05\\n");', 'printf("$%.2f\\n", price); with double values 1.5, 12.0, 0.05.'),
            ],
            level="imitation",
        ),
    ],
    {
        "cb3-column-table": vi_challenge(
            "Bảng căn cột",
            "Cài `void program(void)` in bảng hai cột căn đúng như đề bài: cột 1 căn trái độ rộng 6, cột 2 căn phải độ rộng 3.",
            [("bảng chính xác", 'printf("%-6s | %3s\\n", "name", "qty"); rồi các số nguyên với %3d.')],
        ),
        "cb3-money-format": vi_challenge(
            "Định dạng tiền",
            "Cài `void program(void)` in ba giá, mỗi giá một dòng, dạng đô la với đúng 2 số lẻ.",
            [("ba dòng tiền chính xác", 'printf("$%.2f\\n", price); với double 1.5, 12.0, 0.05.')],
        ),
    },
    solutions=[
        (
            "cb3-column-table",
            '#include <stdio.h>\nvoid program(void) {\n    printf("%-6s | %3s\\n", "name", "qty");\n    printf("%-6s | %3d\\n", "apple", 3);\n    printf("%-6s | %3d\\n", "mango", 12);\n}\nint main(void) { program(); return 0; }',
            '#include <stdio.h>\nvoid program(void) {\n    printf("%-6s | %3s\\n", "name", "qty");\n    printf("%-6s | %-3d\\n", "apple", 3);\n    printf("%-6s | %-3d\\n", "mango", 12);\n}\nint main(void) { program(); return 0; }',
        ),
        (
            "cb3-money-format",
            '#include <stdio.h>\nvoid program(void) {\n    printf("$%.2f\\n", 1.5);\n    printf("$%.2f\\n", 12.0);\n    printf("$%.2f\\n", 0.05);\n}\nint main(void) { program(); return 0; }',
            '#include <stdio.h>\nvoid program(void) {\n    printf("$%.1f\\n", 1.5);\n    printf("$%.2f\\n", 12.0);\n    printf("$%.2f\\n", 0.05);\n}\nint main(void) { program(); return 0; }',
        ),
    ],
)

write_practice(
    M3,
    "cb-p3-parse",
    "Parse the Line",
    "Extract typed fields from text lines with sscanf — the graded form of reading input.",
    "Phân tích dòng",
    "Tách trường có kiểu từ dòng văn bản bằng sscanf — dạng được chấm của việc đọc đầu vào.",
    L3B,
    14,
    "beginner",
    [
        challenge(
            "cb3-parse-pair",
            "Parse Name and Age",
            "Implement `int parse_person(const char* line, char* name, int* age)`: parse `<name> <age>` from the line. Store the name (max 31 chars + terminator) and age through the out-parameters. Return 1 if both fields were read, 0 otherwise.",
            C_PRELUDE,
            [
                ("valid line", 'char name[32]; int age = -1;\nCHECK_EQ(parse_person("Linh 21", name, &age), 1);\nCHECK_STR_EQ(name, "Linh");\nCHECK_EQ(age, 21);', 'int got = sscanf(line, "%31s %d", name, age); return got == 2;'),
                ("missing age fails", 'char name[32]; int age = -1;\nCHECK_EQ(parse_person("Linh", name, &age), 0);', "sscanf returns how many items it read — 1 here, so return 0."),
            ],
            level="guided",
        ),
        challenge(
            "cb3-parse-rgb",
            "Parse RGB",
            "Implement `int parse_rgb(const char* text, int* r, int* g, int* b)` parsing decimal colors like `\"12, 200, 3\"` (comma-separated, optional spaces). Return 1 only when all three parsed, else 0.",
            C_PRELUDE,
            [
                ("valid rgb", "int r, g, b;\nCHECK_EQ(parse_rgb(\"12, 200, 3\", &r, &g, &b), 1);\nCHECK_EQ(r, 12);\nCHECK_EQ(g, 200);\nCHECK_EQ(b, 3);", 'sscanf(text, "%d , %d , %d", r, g, b) — spaces in the format match any whitespace.'),
                ("two fields fail", "int r, g, b;\nCHECK_EQ(parse_rgb(\"12, 200\", &r, &g, &b), 0);", "Only 2 items read -> return 0."),
            ],
            level="independent",
        ),
    ],
    {
        "cb3-parse-pair": vi_challenge(
            "Tách tên và tuổi",
            "Cài `int parse_person(const char* line, char* name, int* age)`: tách `<ten> <tuoi>` từ dòng; lưu qua tham số ra; trả 1 nếu đọc đủ cả hai, ngược lại 0.",
            [("dòng hợp lệ", 'int got = sscanf(line, "%31s %d", name, age); return got == 2;'), ("thiếu tuổi", "sscanf trả về số mục đọc được — 1 ở đây, nên trả 0.")],
        ),
        "cb3-parse-rgb": vi_challenge(
            "Tách RGB",
            "Cài `int parse_rgb(const char* text, int* r, int* g, int* b)` tách màu dạng `\"12, 200, 3\"`. Trả 1 chỉ khi đọc đủ cả ba.",
            [("rgb hợp lệ", 'sscanf(text, "%d , %d , %d", r, g, b) — dấu cách trong định dạng khớp bất kỳ khoảng trắng nào.'), ("thiếu trường", "Chỉ đọc được 2 mục -> trả 0.")],
        ),
    },
    solutions=[
        (
            "cb3-parse-pair",
            '#include <stdio.h>\nint parse_person(const char* line, char* name, int* age) {\n    int got = sscanf(line, "%31s %d", name, age);\n    return got == 2;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint parse_person(const char* line, char* name, int* age) {\n    int got = sscanf(line, "%31s", name);\n    return got == 2;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb3-parse-rgb",
            '#include <stdio.h>\nint parse_rgb(const char* text, int* r, int* g, int* b) {\n    int got = sscanf(text, "%d , %d , %d", r, g, b);\n    return got == 3;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint parse_rgb(const char* text, int* r, int* g, int* b) {\n    int got = sscanf(text, "%d", r);\n    return got == 3;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M3,
    L3C,
    "Checkpoint: Input & Output",
    "One graded flow: parse a record line, then print it as a formatted report row.",
    14,
    r"""
## Checkpoint

Parse then format — the two halves of real I/O — in one challenge.
""",
    "Điểm kiểm tra: Vào & Ra",
    "Một luồng được chấm: tách một dòng dữ liệu, rồi in nó thành hàng báo cáo có định dạng.",
    r"""
## Điểm kiểm tra

Tách rồi định dạng — hai nửa của vào/ra thật — trong một thử thách.
""",
    challenge(
        "cb3-checkpoint-report-row",
        "Record to Report Row",
        "Implement `void report_row(const char* line)` that parses `<item> <count> <price>` (e.g. `\"bolt 12 0.05\"`) and prints one row:\n\n```\n| bolt        |  12 | 0.05 |\n```\n\nItem left-aligned width 12; count right-aligned width 3; price with exactly 2 decimals, right-aligned width 5. Spaces around `|` exactly as shown.",
        C_PRELUDE,
        [                ("exact report row", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "| bolt         |  12 |  0.05 |\\n");',
                'char item[32]; int count; double price; sscanf(line, "%31s %d %lf", item, &count, &price); then printf("| %-12s | %3d | %5.2f |\\n", ...).',
            ),
        ],
    ),
    vi_challenge(
        "Dữ liệu thành hàng báo cáo",
        "Cài `void report_row(const char* line)` tách `<mon> <so_luong> <gia>` và in một hàng đúng định dạng đề bài.",
        [("hàng báo cáo chính xác", 'sscanf(line, "%31s %d %lf", ...) rồi printf("| %-12s | %3d | %5.2f |\\n", ...).')],
    ),
    solution='#include <stdio.h>\nvoid report_row(const char* line) {\n    char item[32]; int count = 0; double price = 0.0;\n    sscanf(line, "%31s %d %lf", item, &count, &price);\n    printf("| %-12s | %3d | %5.2f |\\n", item, count, price);\n}\nvoid program(void) { report_row("bolt 12 0.05"); }\nint main(void) { program(); return 0; }',
    wrong='#include <stdio.h>\nvoid report_row(const char* line) {\n    char item[32]; int count = 0; double price = 0.0;\n    sscanf(line, "%31s %d %lf", item, &count, &price);\n    printf("| %-12s | %3d | %.2f |\\n", item, count, price);\n}\nvoid program(void) { report_row("bolt 12 0.05"); }\nint main(void) { program(); return 0; }',
)

# ============================ MODULE 4: operators-expressions ============================
M4 = "operators-expressions"

L4A = "arithmetic-and-division"
L4B = "logic-and-precedence"
L4C = "conversions-casts"
L4D = "cb-checkpoint-m4"

write_module(
    M4,
    "Operators & Expressions",
    "Arithmetic, the integer-division trap, logical operators, precedence, and explicit conversions.",
    "Toán tử & Biểu thức",
    "Số học, bẫy chia số nguyên, toán tử logic, thứ tự ưu tiên và ép kiểu tường minh.",
    [L4A, L4B, L4C, L4D],
    ["cb-p4-arithmetic", "cb-p4-logic"],
)

write_lesson(
    M4,
    L4A,
    "Arithmetic and the Integer-Division Trap",
    "The arithmetic operators, increment/decrement, and why 1/2 is 0 in C.",
    11,
    r"""
## Arithmetic

`+ - * / %` — add, subtract, multiply, divide, remainder. `%` (modulo) is
integer-only and gives the remainder: `7 % 3` is `1`.

## The trap: int / int is int

```c
printf("%d\n", 1 / 2);        // 0  — integer division truncates
printf("%f\n", 1.0 / 2);      // 0.500000 — one double promotes all
printf("%d\n", 7 % 3);        // 1
```

When both operands are integers, `/` truncates toward zero. This single rule
explains a huge share of beginner bugs (averages that print 0, percentages
stuck at 100).

## Increment and decrement

```c
int i = 5;
i++;   // i is 6 (post-increment: value of i++ is the OLD 5)
++i;   // pre-increment: value is the NEW 6
```

Prefer standalone `i++` statements; the difference between pre/post only
matters when the expression's value is used.
""",
    "Số học và bẫy chia số nguyên",
    "Các toán tử số học, tăng/giảm, và vì sao 1/2 bằng 0 trong C.",
    r"""
## Số học

`+ - * / %` — cộng, trừ, nhân, chia, lấy dư. `%` (modulo) chỉ dành cho số
nguyên và cho phần dư: `7 % 3` là `1`.

## Bẫy: int / int là int

```c
printf("%d\n", 1 / 2);        // 0  — chia số nguyên cắt cụt
printf("%f\n", 1.0 / 2);      // 0.500000 — một double làm tất cả thành double
printf("%d\n", 7 % 3);        // 1
```

Khi cả hai toán hạng là số nguyên, `/` cắt cụt về 0. Một quy tắc này giải thích
phần lớn lỗi của người mới (trung bình in ra 0, phần trăm kẹt ở 100).

## Tăng và giảm

```c
int i = 5;
i++;   // i là 6 (hậu tăng: giá trị của i++ là 5 CŨ)
++i;   // tiền tăng: giá trị là 6 MỚI
```

Ưu tiên `i++` đứng một mình; khác biệt tiền/hậu chỉ quan trọng khi dùng giá trị
của biểu thức.
""",
)

write_lesson(
    M4,
    L4B,
    "Comparisons, Logic & Precedence",
    "Boolean results in C, short-circuit && and ||, !, and the precedence rules that decide what an expression means.",
    11,
    r"""
## Comparisons yield 0 or 1

`== != < <= > >=` produce `int`: `1` (true) or `0` (false). C has no separate
boolean type in everyday use — any nonzero value is "true".

**The classic bug:** `=` assigns, `==` compares. `if (x = 5)` assigns 5 to x
and is always true. Compilers warn; turn warnings on (this course always does).

## Logical operators, short-circuit

```c
int a = 0, b = 5;
a && b   // 0 — a is false, b never evaluated (short-circuit)
b || a   // 1 — b is true, a never evaluated
!b       // 0 — not true is false
```

Short-circuiting is a feature: `p != NULL && p->value > 0` is safe — the second
operand only runs when `p` is non-NULL.

## Precedence (the rules that matter now)

1. `!`, unary `-` — highest
2. `* / %`
3. `+ -`
4. `< <= > >=`
5. `== !=`
6. `&&`
7. `||`
8. `=` — lowest

`x + y == 3 && a < b` parses as `((x + y) == 3) && (a < b)`. When in doubt,
parenthesize for humans.
""",
    "So sánh, logic & thứ tự ưu tiên",
    "Kết quả boolean trong C, && và || cắt ngắn, !, và quy tắc ưu tiên quyết định ý nghĩa của biểu thức.",
    r"""
## So sánh cho ra 0 hoặc 1

`== != < <= > >=` cho ra `int`: `1` (đúng) hoặc `0` (sai). C không có kiểu
boolean riêng trong dùng hàng ngày — mọi giá trị khác 0 là "đúng".

**Lỗi kinh điển:** `=` gán, `==` so sánh. `if (x = 5)` gán 5 cho x và luôn
đúng. Trình biên dịch cảnh báo; hãy bật cảnh báo (khóa này luôn bật).

## Toán tử logic, cắt ngắn

```c
int a = 0, b = 5;
a && b   // 0 — a sai, b không được tính (cắt ngắn)
b || a   // 1 — b đúng, a không được tính
!b       // 0 — phủ định của đúng là sai
```

Cắt ngắn là tính năng: `p != NULL && p->value > 0` an toàn — toán hạng hai chỉ
chạy khi `p` khác NULL.

## Thứ tự ưu tiên (phần cần ngay)

1. `!`, `-` một ngôi — cao nhất
2. `* / %`
3. `+ -`
4. `< <= > >=`
5. `== !=`
6. `&&`
7. `||`
8. `=` — thấp nhất

`x + y == 3 && a < b` phân tích thành `((x + y) == 3) && (a < b)`. Khi nghi
ngờ, thêm ngoặc cho con người đọc.
""",
)

write_lesson(
    M4,
    L4C,
    "Conversions and Casts",
    "What C converts automatically, what it truncates, and how to convert explicitly on purpose.",
    10,
    r"""
## Implicit conversions

C silently converts in mixed expressions — the "usual arithmetic
conversions": the smaller/weaker type is promoted to the wider one.

```c
int i = 3;
double d = i;          // int -> double, exact: 3.0
double half = i / 2;   // int / int FIRST (0), then int -> double: 0.0!
double ok = i / 2.0;   // i promoted to double: 1.5
```

The assignment case truncates the other way: `int x = 2.9;` stores `2` — the
fraction is dropped, not rounded.

## Explicit casts

A cast says "convert on purpose":

```c
double avg = (double)total / count;   // divide as doubles
int rounded = (int)(x + 0.5);         // round-half-up for positive x
char c = (char)('A' + 3);             // int -> char
```

Cast when you mean it; never to silence a warning you do not understand.
""",
    "Chuyển đổi và ép kiểu",
    "C tự chuyển đổi gì, cắt cụt gì, và cách chuyển đổi tường minh có chủ đích.",
    r"""
## Chuyển đổi ngầm

C âm thầm chuyển đổi trong biểu thức trộn kiểu — "các phép chuyển đổi số học
thông thường": kiểu yếu hơn được nâng lên kiểu rộng hơn.

```c
int i = 3;
double d = i;          // int -> double, chính xác: 3.0
double half = i / 2;   // int / int TRƯỚC (0), rồi int -> double: 0.0!
double ok = i / 2.0;   // i được nâng thành double: 1.5
```

Phép gán chiều ngược lại cắt cụt: `int x = 2.9;` lưu `2` — phần lẻ bị bỏ,
không làm tròn.

## Ép kiểu tường minh

Ép kiểu nói "chuyển đổi có chủ đích":

```c
double avg = (double)total / count;   // chia như double
int rounded = (int)(x + 0.5);         // làm tròn nửa lên cho x dương
char c = (char)('A' + 3);             // int -> char
```

Ép kiểu khi bạn thật sự muốn; đừng bao giờ ép chỉ để tắt một cảnh báo bạn
không hiểu.
""",
)

write_practice(
    M4,
    "cb-p4-arithmetic",
    "Arithmetic Clinic",
    "Integer division, modulo cycles, and truncation — computed exactly.",
    "Phòng khám số học",
    "Chia số nguyên, chu kỳ modulo và cắt cụt — tính chính xác.",
    L4A,
    14,
    "beginner",
    [
        challenge(
            "cb4-int-div",
            "Integer Division Behavior",
            "Implement `void program(void)` printing three lines for `a=7, b=2`: the int quotient, the remainder, and the double quotient with 1 decimal:\n\n```\n7/2=3\n7%2=1\n7/2=3.5\n```\n\nLine 3 must be a real double division (`7.0/2`), not a computed constant.",
            C_PRELUDE,
            [
                ("exact division lines", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "7/2=3\\n7%2=1\\n7/2=3.5\\n");', "int q = a / b; int r = a % b; double dq = (double)a / b;"),
            ],
            level="guided",
        ),
        challenge(
            "cb4-minutes-convert",
            "Minutes to h:mm",
            "Implement `void program(void)` printing `195` minutes as exactly `3:15` (hours:minutes with the minutes zero-padded to 2 digits). Compute both parts with / and %.",
            C_PRELUDE,
            [
                ("formatted duration", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "3:15\\n");', "int h = 195 / 60; int m = 195 % 60; printf(\"%d:%02d\\n\", h, m);"),
            ],
            level="imitation",
        ),
        challenge(
            "cb4-average-trap",
            "Average Without the Trap",
            "Implement `double average(int total, int count)` returning the true mathematical average. The starter's signature is already double — the fix is in the division, not the type.",
            C_PRELUDE,
            [
                ("exact average", "CHECK_NEAR(average(7, 2), 3.5, 1e-9);", "Cast one operand: (double)total / count."),
                ("zero stays exact", "CHECK_NEAR(average(9, 3), 3.0, 1e-9);", "Works when the division is exact too."),
            ],
            level="debugging",
        ),
    ],
    {
        "cb4-int-div": vi_challenge(
            "Hành vi chia số nguyên",
            "Cài `void program(void)` in ba dòng cho a=7, b=2: thương nguyên, số dư, và thương double với 1 số lẻ. Dòng 3 phải là phép chia double thật.",
            [("ba dòng chia chính xác", "int q = a / b; int r = a % b; double dq = (double)a / b;")],
        ),
        "cb4-minutes-convert": vi_challenge(
            "Đổi phút sang h:mm",
            "Cài `void program(void)` in 195 phút thành đúng `3:15` (phút đệm 0 tới 2 chữ số). Tính cả hai phần bằng / và %.",
            [("thời lượng đúng định dạng", "int h = 195 / 60; int m = 195 % 60; printf(\"%d:%02d\\n\", h, m);")],
        ),
        "cb4-average-trap": vi_challenge(
            "Trung bình không dính bẫy",
            "Cài `double average(int total, int count)` trả về trung bình toán học đúng. Lỗi nằm ở phép chia, không phải kiểu trả về.",
            [("trung bình chính xác", "Ép một toán hạng: (double)total / count."), ("tròn vẫn chính xác", "Chạy đúng cả khi chia hết.")],
        ),
    },
    solutions=[
        (
            "cb4-int-div",
            '#include <stdio.h>\nvoid program(void) {\n    int a = 7, b = 2;\n    printf("%d/%d=%d\\n", a, b, a / b);\n    printf("%d%%%d=%d\\n", a, b, a % b);\n    printf("%d/%d=%.1f\\n", a, b, (double)a / b);\n}\nint main(void) { program(); return 0; }',
            '#include <stdio.h>\nvoid program(void) {\n    int a = 7, b = 2;\n    printf("%d/%d=%d\\n", a, b, a / b);\n    printf("%d%%%d=%d\\n", a, b, a % b);\n    printf("%d/%d=%.1f\\n", a, b, a / b);\n}\nint main(void) { program(); return 0; }',
        ),
        (
            "cb4-minutes-convert",
            '#include <stdio.h>\nvoid program(void) {\n    int total = 195;\n    printf("%d:%02d\\n", total / 60, total % 60);\n}\nint main(void) { program(); return 0; }',
            '#include <stdio.h>\nvoid program(void) {\n    int total = 195;\n    printf("%d:%02d\\n", total / 60, total - (total / 60));\n}\nint main(void) { program(); return 0; }',
        ),
        (
            "cb4-average-trap",
            "#include <stdio.h>\ndouble average(int total, int count) {\n    return (double)total / count;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\ndouble average(int total, int count) {\n    return total / count;\n}\nint main(void) { return 0; }",
        ),
    ],
)

write_practice(
    M4,
    "cb-p4-logic",
    "Logic Bench",
    "Comparison chains, boolean functions, and precedence under pressure.",
    "Bàn chạy logic",
    "Chuỗi so sánh, hàm boolean và thứ tự ưu tiên dưới áp lực.",
    L4B,
    12,
    "beginner",
    [
        challenge(
            "cb4-in-range",
            "In Range?",
            "Implement `int in_range(int x, int lo, int hi)` returning 1 when `lo <= x <= hi` and 0 otherwise — as one boolean expression.",
            C_PRELUDE,
            [
                ("inside", "CHECK_EQ(in_range(5, 1, 10), 1);", "x >= lo && x <= hi."),
                ("below", "CHECK_EQ(in_range(0, 1, 10), 0);", "Fails the left half."),
                ("above", "CHECK_EQ(in_range(11, 1, 10), 0);", "Fails the right half."),
                ("boundaries count", "CHECK_EQ(in_range(1, 1, 10), 1);\nCHECK_EQ(in_range(10, 1, 10), 1);", "Both ends are inclusive."),
            ],
            level="imitation",
        ),
        challenge(
            "cb4-leap-year",
            "Leap Year Rule",
            "Implement `int is_leap(int year)`: divisible by 4, EXCEPT centuries not divisible by 400. One boolean expression; test data covers the tricky centuries.",
            C_PRELUDE,
            [
                ("plain leap", "CHECK_EQ(is_leap(2024), 1);", "2024 % 4 == 0 and not a century."),
                ("century non-leap", "CHECK_EQ(is_leap(1900), 0);", "Divisible by 100 but not 400."),
                ("400-year leap", "CHECK_EQ(is_leap(2000), 1);", "Divisible by 400 wins."),
                ("plain non-leap", "CHECK_EQ(is_leap(2023), 0);", "Not divisible by 4."),
            ],
            level="guided",
        ),
    ],
    {
        "cb4-in-range": vi_challenge(
            "Trong khoảng?",
            "Cài `int in_range(int x, int lo, int hi)` trả 1 khi `lo <= x <= hi`, ngược lại 0 — bằng một biểu thức boolean.",
            [("trong khoảng", "x >= lo && x <= hi."), ("dưới", "Sai nửa trái."), ("trên", "Sai nửa phải."), ("biên được tính", "Cả hai đầu là bao hàm.")],
        ),
        "cb4-leap-year": vi_challenge(
            "Quy tắc năm nhuận",
            "Cài `int is_leap(int year)`: chia hết cho 4, TRỪ các thế kỷ không chia hết cho 400. Một biểu thức boolean.",
            [("nhuận thường", "2024 % 4 == 0 và không phải thế kỷ."), ("thế kỷ không nhuận", "Chia hết cho 100 nhưng không cho 400."), ("nhuận 400 năm", "Chia hết cho 400 thắng."), ("không nhuận", "Không chia hết cho 4.")],
        ),
    },
    solutions=[
        (
            "cb4-in-range",
            "#include <stdio.h>\nint in_range(int x, int lo, int hi) {\n    return x >= lo && x <= hi;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nint in_range(int x, int lo, int hi) {\n    return x > lo && x <= hi;\n}\nint main(void) { return 0; }",
        ),
        (
            "cb4-leap-year",
            "#include <stdio.h>\nint is_leap(int year) {\n    return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nint is_leap(int year) {\n    return year % 4 == 0;\n}\nint main(void) { return 0; }",
        ),
    ],
)

write_checkpoint(
    M4,
    L4D,
    "Checkpoint: Operators & Expressions",
    "Integrated arithmetic + conversion + formatting: a computed invoice line.",
    14,
    r"""
## Checkpoint

Operators, conversions, and exact formatting combine into one invoice-line
computation.
""",
    "Điểm kiểm tra: Toán tử & Biểu thức",
    "Số học, chuyển đổi và định dạng chính xác gộp lại trong một dòng hóa đơn.",
    r"""
## Điểm kiểm tra

Toán tử, chuyển đổi và định dạng chính xác gộp lại trong một dòng hóa đơn.
""",
    challenge(
        "cb4-checkpoint-invoice",
        "Invoice Line",
        "Given `int qty = 3;` and `double unit = 1.25;`, implement `void program(void)` printing exactly:\n\n```\n3 x 1.25 = 3.75\navg/unit pieces: 8\n```\n\nLine 1: the total computed as a real double product (2 decimals). Line 2: how many WHOLE items `10.0` dollars buys at `unit` price — computed as `(int)(10.0 / unit)`.",
        C_PRELUDE,
        [                ("exact invoice lines", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "3 x 1.25 = 3.75\\navg/unit pieces: 8\\n");',
                'printf("%d x %.2f = %.2f\\n", qty, unit, qty * unit); then printf("avg/unit pieces: %d\\n", (int)(10.0 / unit));',
            ),
        ],
    ),
    vi_challenge        ("Dòng hóa đơn", "Cho `int qty = 3;` và `double unit = 1.25;`, cài `void program(void)` in đúng hai dòng: tổng là tích double thật (2 số lẻ) và số món NGUYÊN mua được với 10.0 đô (chia double rồi ép int) — kết quả 8.",
        [("hai dòng hóa đơn chính xác", 'printf("%d x %.2f = %.2f\\n", ...) rồi printf("avg/unit pieces: %d\\n", (int)(10.0 / unit));')],
    ),
    solution='#include <stdio.h>\nvoid program(void) {\n    int qty = 3;\n    double unit = 1.25;\n    printf("%d x %.2f = %.2f\\n", qty, unit, qty * unit);\n    printf("avg/unit pieces: %d\\n", (int)(10.0 / unit));\n}\nint main(void) { program(); return 0; }',
    wrong='#include <stdio.h>\nvoid program(void) {\n    int qty = 3;\n    double unit = 1.25;\n    printf("%d x %.2f = %.2f\\n", qty, unit, qty * unit);\n    printf("avg/unit pieces: %d\\n", (int)(10.0 / unit) + 1);\n}\nint main(void) { program(); return 0; }',
)

print("batch 2 complete: modules 3-4")
