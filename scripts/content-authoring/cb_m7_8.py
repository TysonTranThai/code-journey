#!/usr/bin/env python3
"""C Beginner — batch 4: modules 7 (functions) and 8 (scope-lifetime)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ============================ MODULE 7: functions ============================
M7 = "functions"

L7A = "defining-functions"
L7B = "parameters-return"
L7C = "prototypes-organization"
L7D = "cb-checkpoint-m7"

write_module(
    M7,
    "Functions",
    "Declaring, defining, and calling functions; parameters, return values, prototypes, and decomposition.",
    "Hàm",
    "Khai báo, định nghĩa và gọi hàm; tham số, giá trị trả về, nguyên mẫu và phân rã bài toán.",
    [L7A, L7B, L7C, L7D],
    ["cb-p7-basics", "cb-p7-decompose"],
)

write_lesson(
    M7,
    L7A,
    "Defining and Calling Functions",
    "The anatomy of a function: return type, name, parameters, body, and the call.",
    11,
    r"""
## Anatomy

```c
int add(int a, int b) {      // return type, name, parameters
    return a + b;            // body: compute and return
}

int sum = add(2, 3);         // call: arguments 2 and 3
```

A function packages a computation under a name. Define it once, call it many
times. `void` means "returns nothing":

```c
void greet(const char* name) {
    printf("Hello, %s!\n", name);
    return;                   // optional for void
}
```

## Why functions

- **Name the idea** — `is_leap(y)` reads better than a wall of conditions.
- **Test in isolation** — a pure function is trivially testable (our whole
  grading model depends on this).
- **One responsibility** — if you can't name it in a few words, split it.

## Execution

A call jumps to the body, runs it, and resumes right after the call site,
carrying the return value. Arguments are **copies** (module 11 shows how to
let a function modify the caller's variables).
""",
    "Định nghĩa và gọi hàm",
    "Giải phẫu một hàm: kiểu trả về, tên, tham số, thân và lời gọi.",

    r"""
## Giải phẫu

```c
int add(int a, int b) {      // kiểu trả về, tên, tham số
    return a + b;            // thân: tính và trả về
}

int sum = add(2, 3);         // gọi: đối số 2 và 3
```

Hàm gói một phép tính dưới một cái tên. Định nghĩa một lần, gọi nhiều lần.
`void` nghĩa là "không trả về gì":

```c
void greet(const char* name) {
    printf("Xin chào, %s!\n", name);
    return;                   // tùy chọn với void
}
```

## Vì sao cần hàm

- **Đặt tên cho ý tưởng** — `is_leap(y)` dễ đọc hơn cả màn điều kiện.
- **Kiểm thử độc lập** — hàm thuần rất dễ kiểm thử (mô hình chấm điểm của
  khóa này dựa trên điều đó).
- **Một trách nhiệm** — nếu không gọi được tên trong vài từ, hãy tách nó.

## Luồng thực thi

Lời gọi nhảy vào thân, chạy xong rồi quay lại ngay sau chỗ gọi, mang theo giá
trị trả về. Đối số được **sao chép** (module 11 sẽ chỉ cách cho hàm sửa được
biến của caller).
""",
)

write_lesson(
    M7,
    L7B,
    "Parameters and Return Values",
    "Value semantics: copies in, one value out. Multiple outputs need pointers.",
    12,
    r"""
## Parameters are copies

```c
void set_to_zero(int x) {
    x = 0;                    // modifies the COPY — caller unaffected
}

int a = 5;
set_to_zero(a);              // a is still 5
```

C passes by value, always. The function's parameter is a fresh variable
initialized with the argument's value. (Output parameters via pointers come in
module 11 — this is the "why".)

## One return value

```c
int clamp(int v, int lo, int hi) {
    if (v < lo) return lo;
    if (v > hi) return hi;
    return v;
}
```

`return` exits immediately — it can appear anywhere in the body. A
non-`void` function that reaches the end of its body without a `return` hands
the caller an **indeterminate value** (undefined behavior if the caller uses
it). GCC warns with `-Wreturn-type`; our harness compiles with warnings shown.

## Early returns beat nesting

```c
// prefer this                          // over this
int f(int x) {                          int f(int x) {
    if (bad(x)) return -1;                  if (!bad(x)) {
    ... main path ...                           ... deep nesting ...
}                                           }
                                        }
```
""",
    "Tham số và giá trị trả về",
    "Ngữ nghĩa giá trị: bản sao vào, một giá trị ra. Nhiều đầu ra cần con trỏ.",

    r"""
## Tham số là bản sao

```c
void set_to_zero(int x) {
    x = 0;                    // sửa bản SAO — caller không đổi
}

int a = 5;
set_to_zero(a);              // a vẫn là 5
```

C luôn truyền theo giá trị. Tham số của hàm là biến mới được khởi tạo bằng giá
trị đối số. (Tham số đầu ra qua con trỏ ở module 11 — đây là "vì sao".)

## Một giá trị trả về

```c
int clamp(int v, int lo, int hi) {
    if (v < lo) return lo;
    if (v > hi) return hi;
    return v;
}
```

`return` thoát ngay lập tức — có thể nằm bất kỳ đâu trong thân. Hàm khác
`void` mà chạy hết thân mà không `return` sẽ trao cho caller một giá trị
**không xác định** (hành vi không xác định nếu caller dùng nó). GCC cảnh báo
với `-Wreturn-type`; harness biên dịch kèm cảnh báo hiển thị.

## Return sớm đỡ lồng nhau

```c
// nên viết thế này                        // thay vì thế này
int f(int x) {                              int f(int x) {
    if (bad(x)) return -1;                      if (!bad(x)) {
    ... đường chính ...                             ... lồng sâu ...
}                                               }
                                            }
```
""",
)

write_lesson(
    M7,
    L7C,
    "Prototypes and Program Organization",
    "Declaration before use: why prototypes exist and how files are organized.",
    10,
    r"""
## Declare before use

C reads top-down. Calling a function whose name the compiler hasn't seen yet
is an error (in C23 and under GCC 14 with our flags):

```c
int main(void) {
    return area(3, 4);        // ERROR: 'area' unknown here
}

int area(int w, int h) { return w * h; }
```

Fix with a **prototype** (declaration) — signature only, no body:

```c
int area(int w, int h);       // prototype

int main(void) { return area(3, 4); }   // OK now

int area(int w, int h) { return w * h; } // definition
```

## The rule you'll actually use

In graded challenges, define helpers **above** `main` (or prototype them) so
the compiler has seen every name before it compiles the caller.

## Files (a taste)

Real projects put prototypes in `.h` headers and definitions in `.c` files —
module 18 builds that out. For now: one file, helpers first, `main` last.
""",
    "Nguyên mẫu và tổ chức chương trình",
    "Khai báo trước khi dùng: vì sao nguyên mẫu tồn tại và cách tổ chức tệp.",

    r"""
## Khai báo trước khi dùng

C đọc từ trên xuống. Gọi một hàm mà trình biên dịch chưa từng thấy tên đó là
lỗi (trong C23 và với GCC 14 cùng cờ của chúng ta):

```c
int main(void) {
    return area(3, 4);        // LỖI: 'area' chưa biết tại đây
}

int area(int w, int h) { return w * h; }
```

Sửa bằng **nguyên mẫu** (khai báo) — chỉ chữ ký, không thân:

```c
int area(int w, int h);       // nguyên mẫu

int main(void) { return area(3, 4); }   // OK rồi

int area(int w, int h) { return w * h; } // định nghĩa
```

## Quy tắc bạn sẽ dùng

Trong thử thách có chấm điểm, định nghĩa hàm trợ giúp **trên** `main` (hoặc
nguyên mẫu chúng) để trình biên dịch đã thấy mọi tên trước khi dịch caller.

## Tệp (hương dẫn)

Dự án thật đặt nguyên mẫu trong `.h` và định nghĩa trong `.c` — module 18 sẽ
làm kỹ phần này. Tạm thời: một tệp, hàm trợ giúp trước, `main` cuối.
""",
)

write_practice(
    M7,
    "cb-p7-basics",
    "Function Basics",
    "Write small single-purpose functions and call them.",
    "Hàm cơ bản",
    "Viết các hàm nhỏ, một mục đích, và gọi chúng.",
    L7A,
    14,
    "beginner",
    [
        challenge(
            "cb7-cube",
            "Cube Function",
            "Implement `long cube(int n)` returning n cubed.",
            C_PRELUDE,
            [
                ("positives", "CHECK_EQ(cube(2), 8);\nCHECK_EQ(cube(5), 125);", "n*n*n."),
                ("zero", "CHECK_EQ(cube(0), 0);", "0 cubed is 0."),
                ("negatives", "CHECK_EQ(cube(-3), -27);", "Sign is preserved when n is odd."),
            ],
            level="imitation",
        ),
        challenge(
            "cb7-max3",
            "Max of Three",
            "Implement `int max3(int a, int b, int c)` returning the largest.",
            C_PRELUDE,
            [
                ("first wins", "CHECK_EQ(max3(9, 4, 2), 9);", "Compare step by step."),
                ("last wins", "CHECK_EQ(max3(1, 2, 7), 7);", "Don't stop early."),
                ("ties", "CHECK_EQ(max3(5, 5, 5), 5);", "Ties may return that value."),
                ("negatives", "CHECK_EQ(max3(-8, -3, -6), -3);", "Works below zero too."),
            ],
            level="guided",
        ),
        challenge(
            "cb7-is-vowel",
            "Vowel Test",
            "Implement `int is_vowel(char c)` returning 1 for a/e/i/o/u (and their uppercase), else 0.",
            C_PRELUDE,
            [
                ("lowercase", "CHECK_EQ(is_vowel('a'), 1);\nCHECK_EQ(is_vowel('e'), 1);", "Check each vowel."),
                ("uppercase", "CHECK_EQ(is_vowel('U'), 1);", "Handle both cases."),
                ("consonants", "CHECK_EQ(is_vowel('x'), 0);\nCHECK_EQ(is_vowel('Z'), 0);", "Return 0."),
                ("non-letters", "CHECK_EQ(is_vowel('1'), 0);", "Digits aren't vowels."),
            ],
            level="guided",
        ),
        challenge(
            "cb7-pay-rate",
            "Pay Calculator",
            "Implement `double pay(double hours, double rate)`: hours up to and including 40 pay `rate`; each hour above 40 pays 1.5*rate. 45 h at 10.0/h -> 475.00.",
            C_PRELUDE,
            [
                ("straight time", "CHECK_NEAR(pay(30, 10.0), 300.00, 1e-9);", "Under 40 is hours*rate."),
                ("boundary 40", "CHECK_NEAR(pay(40, 10.0), 400.00, 1e-9);", "40 is straight time."),
                ("overtime", "CHECK_NEAR(pay(45, 10.0), 475.00, 1e-9);", "5 extra hours at 15.0."),
            ],
            level="independent",
        ),
    ],
    {
        "cb7-cube": vi_challenge(
            "Hàm lập phương",
            "Cài `long cube(int n)` trả về n lập phương.",
            [("dương", "n*n*n."), ("không", "0 lập phương là 0."), ("âm", "Dấu được giữ khi n lẻ.")],
        ),
        "cb7-max3": vi_challenge(
            "Max của ba",
            "Cài `int max3(int a, int b, int c)` trả về số lớn nhất.",
            [("đầu lớn nhất", "So sánh từng bước."), ("cuối lớn nhất", "Đừng dừng sớm."), ("bằng nhau", "Trả về chính giá trị đó."), ("số âm", "Hoạt động dưới 0.")],
        ),
        "cb7-is-vowel": vi_challenge(
            "Kiểm tra nguyên âm",
            "Cài `int is_vowel(char c)` trả 1 với a/e/i/o/u (kể cả chữ hoa), ngược lại 0.",
            [("thường", "Kiểm từng nguyên âm."), ("hoa", "Xử lý cả hai dạng chữ."), ("phụ âm", "Trả về 0."), ("không phải chữ", "Chữ số không phải nguyên âm.")],
        ),
        "cb7-pay-rate": vi_challenge(
            "Tính lương",
            "Cài `double pay(double hours, double rate)`: giờ tính đến và gồm 40 trả theo `rate`; mỗi giờ trên 40 trả 1.5*rate. 45 giờ, 10.0/giờ -> 475.00.",
            [("giờ thường", "Dưới 40 là hours*rate."), ("biên 40", "40 là giờ thường."), ("tăng ca", "5 giờ thêm với 15.0.")],
        ),
    },
    solutions=[
        (
            "cb7-cube",
            '#include <stdio.h>\nlong cube(int n) {\n    return (long)n * n * n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nlong cube(int n) {\n    return (long)n * n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb7-max3",
            '#include <stdio.h>\nint max3(int a, int b, int c) {\n    int m = a;\n    if (b > m) m = b;\n    if (c > m) m = c;\n    return m;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint max3(int a, int b, int c) {\n    int m = a;\n    if (b > m) m = b;\n    return m;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb7-is-vowel",
            '#include <stdio.h>\nint is_vowel(char c) {\n    switch (c) {\n        case \'a\': case \'e\': case \'i\': case \'o\': case \'u\':\n        case \'A\': case \'E\': case \'I\': case \'O\': case \'U\':\n            return 1;\n        default:\n            return 0;\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint is_vowel(char c) {\n    switch (c) {\n        case \'a\': case \'e\': case \'i\': case \'o\': case \'u\':\n            return 1;\n        default:\n            return 0;\n    }\n}\nint main(void) { return 0; }',
        ),
        (
            "cb7-pay-rate",
            '#include <stdio.h>\ndouble pay(double hours, double rate) {\n    if (hours <= 40.0) return hours * rate;\n    return 40.0 * rate + (hours - 40.0) * 1.5 * rate;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ndouble pay(double hours, double rate) {\n    return hours * rate;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M7,
    "cb-p7-decompose",
    "Decomposition",
    "Split a task into helpers, then compose them.",
    "Phân rã bài toán",
    "Tách công việc thành các hàm trợ giúp rồi ghép chúng.",
    L7B,
    15,
    "beginner",
    [
        challenge(
            "cb7-in-range-fn",
            "Range Helper",
            "Implement `int in_range(int v, int lo, int hi)` returning 1 when lo <= v <= hi (inclusive both ends).",
            C_PRELUDE,
            [
                ("inside", "CHECK_EQ(in_range(5, 1, 10), 1);", "Both comparisons hold."),
                ("edges", "CHECK_EQ(in_range(1, 1, 10), 1);\nCHECK_EQ(in_range(10, 1, 10), 1);", "Inclusive edges."),
                ("outside", "CHECK_EQ(in_range(0, 1, 10), 0);\nCHECK_EQ(in_range(11, 1, 10), 0);", "Both sides fail."),
            ],
            level="imitation",
        ),
        challenge(
            "cb7-fizzbuzz-fn",
            "FizzBuzz Function",
            "Implement `const char* fizzbuzz(int n)`: \"fizzbuzz\" when divisible by 15, \"fizz\" by 3, \"buzz\" by 5, else \"no\".",
            C_PRELUDE,
            [
                ("fifteens", "CHECK_STR_EQ(fizzbuzz(15), \"fizzbuzz\");\nCHECK_STR_EQ(fizzbuzz(30), \"fizzbuzz\");", "Divisible by 3 AND 5 first."),
                ("threes", "CHECK_STR_EQ(fizzbuzz(9), \"fizz\");", "Not by 5."),
                ("fives", "CHECK_STR_EQ(fizzbuzz(10), \"buzz\");", "Not by 3."),
                ("others", "CHECK_STR_EQ(fizzbuzz(7), \"no\");", "Nothing matches."),
            ],
            level="guided",
        ),
        challenge(
            "cb7-seconds-split",
            "Time Splitter",
            "Implement `void split_hms(int total, int* h, int* m, int* s)` filling hours, minutes (0-59), seconds (0-59) through the OUT parameters. total=7275 -> h=2, m=1, s=15.",
            C_PRELUDE,
            [
                ("known split", "int h, m, s;\nsplit_hms(7275, &h, &m, &s);\nCHECK_EQ(h, 2);\nCHECK_EQ(m, 1);\nCHECK_EQ(s, 15);", "7275 s = 2 h + 1 m + 15 s: divide down, keep remainders."),
                ("exact hour", "int h, m, s;\nsplit_hms(7200, &h, &m, &s);\nCHECK_EQ(h, 2);\nCHECK_EQ(m, 0);\nCHECK_EQ(s, 0);", "Remainders can be zero."),
                ("under an hour", "int h, m, s;\nsplit_hms(59, &h, &m, &s);\nCHECK_EQ(h, 0);\nCHECK_EQ(m, 0);\nCHECK_EQ(s, 59);", "h and m are 0."),
            ],
            level="real-world",
        ),
        challenge(
            "cb7-minmax",
            "Min and Max via Pointers",
            "Implement `void minmax(const int* a, int n, int* lo, int* hi)` writing the smallest and largest of n values through the out-parameters.",
            C_PRELUDE,
            [
                ("mixed", "int lo, hi;\nint a[] = {4, -2, 9, 3};\nminmax(a, 4, &lo, &hi);\nCHECK_EQ(lo, -2);\nCHECK_EQ(hi, 9);", "Track both extremes in one pass."),
                ("single", "int lo, hi;\nint a[] = {7};\nminmax(a, 1, &lo, &hi);\nCHECK_EQ(lo, 7);\nCHECK_EQ(hi, 7);", "One element is both."),
                ("duplicates", "int lo, hi;\nint a[] = {5, 5, 5};\nminmax(a, 3, &lo, &hi);\nCHECK_EQ(lo, 5);\nCHECK_EQ(hi, 5);", "All equal."),
            ],
            level="real-world",
        ),
    ],
    {
        "cb7-in-range-fn": vi_challenge(
            "Hàm kiểm tra khoảng",
            "Cài `int in_range(int v, int lo, int hi)` trả 1 khi lo <= v <= hi (bao gồm cả hai đầu).",
            [("trong khoảng", "Cả hai so sánh đều đúng."), ("biên", "Hai biên đều bao gồm."), ("ngoài khoảng", "Cả hai phía đều fail.")],
        ),
        "cb7-fizzbuzz-fn": vi_challenge(
            "Hàm FizzBuzz",
            "Cài `const char* fizzbuzz(int n)`: \"fizzbuzz\" khi chia hết cho 15, \"fizz\" cho 3, \"buzz\" cho 5, còn lại \"no\".",
            [("mười lăm", "Chia hết cho 3 VÀ 5 trước."), ("ba", "Không chia hết cho 5."), ("năm", "Không chia hết cho 3."), ("còn lại", "Không khớp gì cả.")],
        ),
        "cb7-seconds-split": vi_challenge(
            "Tách thời gian",
            "Cài `void split_hms(int total, int* h, int* m, int* s)` ghi giờ, phút (0-59), giây (0-59) qua các THAM SỐ ĐẦU RA. total=7275 -> h=2, m=1, s=15.",
            [("tách đã biết", "7275 s = 2 giờ + 1 phút + 15 giây: chia dần, giữ số dư."), ("đúng một giờ", "Số dư có thể là 0."), ("dưới một giờ", "h và m đều 0.")],
        ),
        "cb7-minmax": vi_challenge(
            "Min và Max qua con trỏ",
            "Cài `void minmax(const int* a, int n, int* lo, int* hi)` ghi giá trị nhỏ nhất và lớn nhất của n phần tử qua tham số đầu ra.",
            [("hỗn hợp", "Theo dõi cả hai cực trong một lượt."), ("một phần tử", "Một phần tử vừa min vừa max."), ("trùng nhau", "Tất cả bằng nhau.")],
        ),
    },
    solutions=[
        (
            "cb7-in-range-fn",
            '#include <stdio.h>\nint in_range(int v, int lo, int hi) {\n    return (v >= lo) && (v <= hi);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint in_range(int v, int lo, int hi) {\n    return (v > lo) && (v <= hi);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb7-fizzbuzz-fn",
            '#include <stdio.h>\nconst char* fizzbuzz(int n) {\n    if (n % 15 == 0) return "fizzbuzz";\n    if (n % 3 == 0) return "fizz";\n    if (n % 5 == 0) return "buzz";\n    return "no";\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nconst char* fizzbuzz(int n) {\n    if (n % 3 == 0) return "fizz";\n    if (n % 5 == 0) return "buzz";\n    if (n % 15 == 0) return "fizzbuzz";\n    return "no";\n}\nint main(void) { return 0; }',
        ),
        (
            "cb7-seconds-split",
            '#include <stdio.h>\nvoid split_hms(int total, int* h, int* m, int* s) {\n    *h = total / 3600;\n    *m = (total % 3600) / 60;\n    *s = total % 60;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid split_hms(int total, int* h, int* m, int* s) {\n    *h = total / 3600;\n    *m = total / 60;\n    *s = total % 60;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb7-minmax",
            '#include <stdio.h>\nvoid minmax(const int* a, int n, int* lo, int* hi) {\n    *lo = a[0];\n    *hi = a[0];\n    for (int i = 1; i < n; i++) {\n        if (a[i] < *lo) *lo = a[i];\n        if (a[i] > *hi) *hi = a[i];\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid minmax(const int* a, int n, int* lo, int* hi) {\n    *lo = a[0];\n    *hi = a[n - 1];\n    for (int i = 0; i < n; i++) {\n        if (a[i] < *lo) *lo = a[i];\n    }\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M7,
    L7D,
    "Checkpoint: Functions",
    "A BMI toolkit built from helpers you compose.",
    15,
    r"""
## Checkpoint

Functions make a pipeline readable: one helper per idea, composed in `main`.
""",
    "Điểm kiểm tra: Hàm",
    "Hàm làm cho chuỗi xử lý dễ đọc: mỗi ý một hàm trợ giúp, ghép trong `main`.",

    r"""
## Điểm kiểm tra

Hàm giúp chuỗi xử lý dễ đọc: mỗi ý một hàm trợ giúp, được ghép trong `main`.
""",
    challenge(
        "cb7-checkpoint-bmi",
        "BMI Toolkit",
        "Implement `double bmi(double weight_kg, double height_m)` = weight / (height*height), and `const char* bmi_band(double b)`: <18.5 -> \"under\", <25 -> \"normal\", <30 -> \"over\", else \"obese\".",
        C_PRELUDE,
        [
            ("formula", "CHECK_NEAR(bmi(70, 1.75), 22.857142857, 1e-6);", "weight / (height*height)."),
            ("bands", "CHECK_STR_EQ(bmi_band(17.0), \"under\");\nCHECK_STR_EQ(bmi_band(22.0), \"normal\");\nCHECK_STR_EQ(bmi_band(27.0), \"over\");\nCHECK_STR_EQ(bmi_band(31.0), \"obese\");", "Band edges: 18.5, 25, 30 — each boundary belongs to the band above it."),
            ("band edges", "CHECK_STR_EQ(bmi_band(18.5), \"normal\");\nCHECK_STR_EQ(bmi_band(25.0), \"over\");\nCHECK_STR_EQ(bmi_band(30.0), \"obese\");", "The comparison is strict < on each threshold."),
        ],
    ),
    vi_challenge(
        "Bộ công cụ BMI",
        "Cài `double bmi(double weight_kg, double height_m)` = weight / (height*height), và `const char* bmi_band(double b)`: <18.5 -> \"under\", <25 -> \"normal\", <30 -> \"over\", còn lại \"obese\".",
        [("công thức", "weight / (height*height)."), ("khoảng", "Mỗi ngưỡng thuộc về khoảng phía trên nó."), ("biên", "So sánh là < chặt tại từng ngưỡng.")],
    ),
    solution='#include <stdio.h>\ndouble bmi(double weight_kg, double height_m) {\n    return weight_kg / (height_m * height_m);\n}\nconst char* bmi_band(double b) {\n    if (b < 18.5) return "under";\n    if (b < 25.0) return "normal";\n    if (b < 30.0) return "over";\n    return "obese";\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\ndouble bmi(double weight_kg, double height_m) {\n    return weight_kg / (height_m * height_m);\n}\nconst char* bmi_band(double b) {\n    if (b <= 18.5) return "under";\n    if (b < 25.0) return "normal";\n    if (b < 30.0) return "over";\n    return "obese";\n}\nint main(void) { return 0; }',
)

# ========================= MODULE 8: scope-lifetime =========================
M8 = "scope-lifetime"

L8A = "scopes-blocks"
L8B = "storage-duration"
L8C = "cb-checkpoint-m8"

write_module(
    M8,
    "Scope, Lifetime & Storage",
    "Where names are visible, when storage exists, and why global state needs care.",
    "Phạm vi, Thời gian sống & Lưu trữ",
    "Tên nhìn thấy ở đâu, bộ nhớ tồn tại khi nào, và vì sao biến toàn cục cần cẩn trọng.",
    [L8A, L8B, L8C],
    ["cb-p8-scope"],
)

write_lesson(
    M8,
    L8A,
    "Blocks and Scopes",
    "A name lives from its declaration to the end of its block — and inner names shadow outer ones.",
    11,
    r"""
## Block scope

A **block** is `{ ... }`. A name declared inside a block exists from its
declaration to that block's closing brace:

```c
int main(void) {
    int x = 1;            // visible to the end of main
    {
        int y = 2;        // visible inside these braces only
        x = x + y;
    }
    // y does not exist here
    return x;             // 3
}
```

Loop and `if` bodies are blocks too — the classic bug:

```c
for (int i = 0; i < 3; i++) { }   // i exists only in the loop
// i++ here is an error
```

## Shadowing

An inner declaration with the same name hides the outer one:

```c
int total = 100;
{
    int total = 5;        // a DIFFERENT variable
    printf("%d\n", total); // 5
}
printf("%d\n", total);    // 100 — untouched
```

Shadowing is legal but confusing. Avoid reusing names in nested scopes.
""",
    "Khối và phạm vi",
    "Một tên sống từ chỗ khai báo đến hết khối — và tên trong có thể che tên ngoài.",

    r"""
## Phạm vi khối

Một **khối** là `{ ... }`. Tên khai báo trong khối tồn tại từ chỗ khai báo đến
ngoặc đóng của khối đó:

```c
int main(void) {
    int x = 1;            // nhìn thấy đến hết main
    {
        int y = 2;        // chỉ trong ngoặc này
        x = x + y;
    }
    // y không tồn tại ở đây
    return x;             // 3
}
```

Thân vòng lặp và `if` cũng là khối — cái bẫy kinh điển:

```c
for (int i = 0; i < 3; i++) { }   // i chỉ tồn tại trong vòng lặp
// i++ ở đây là lỗi
```

## Che tên (shadowing)

Khai báo trong trùng tên sẽ che biến ngoài:

```c
int total = 100;
{
    int total = 5;        // một biến KHÁC
    printf("%d\n", total); // 5
}
printf("%d\n", total);    // 100 — không đổi
```

Che tên hợp lệ nhưng gây nhiễu. Tránh dùng lại tên trong phạm vi lồng nhau.
""",
)

write_lesson(
    M8,
    L8B,
    "Storage Duration: auto, static, extern",
    "Where a variable's memory lives: per-call automatic, program-long static, or shared via extern.",
    12,
    r"""
## Automatic (the default)

Local variables get fresh storage **per call** and die when the block exits:

```c
int counter(void) {
    int n = 0;      // fresh every call
    n++;
    return n;       // always returns 1
}
```

## Static: born once, lives forever

`static` on a local makes it initialize **once** and persist across calls:

```c
int counter(void) {
    static int n = 0;   // initialized once
    n++;
    return n;           // 1, 2, 3, ...
}
```

Same scope rules as a local (invisible outside the function), different
lifetime. `static` on a **file-scope** function or variable instead means
"private to this file" — module 18 uses that for internal helpers.

## File-scope (global) variables

Declared outside all functions; visible from their declaration to the end of
the file, alive for the whole program:

```c
int g_attempts = 0;     // every function below can see it

void attempt(void) { g_attempts++; }
```

Globals are readable state — but mutable global state couples functions
together in ways that break testing and reuse. The course rule: **pass what a
function needs as parameters**; reach for a global only for genuinely
program-wide constants.

## extern (recognition level)

`extern int g;` says "g exists, defined elsewhere" — the linker connects the
uses to the one definition. You need this at module 18; here, just read it.
""",
    "Thời gian sống: auto, static, extern",
    "Bộ nhớ của biến sống ở đâu: tự động theo từng lời gọi, static suốt chương trình, hoặc chia sẻ qua extern.",

    r"""
## Tự động (mặc định)

Biến cục bộ có bộ nhớ mới **theo từng lời gọi** và chết khi khối kết thúc:

```c
int counter(void) {
    int n = 0;      // mới mỗi lần gọi
    n++;
    return n;       // luôn trả về 1
}
```

## Static: sinh một lần, sống mãi

`static` trên biến cục bộ làm nó khởi tạo **một lần** và giữ giá trị qua các
lời gọi:

```c
int counter(void) {
    static int n = 0;   // khởi tạo một lần
    n++;
    return n;           // 1, 2, 3, ...
}
```

Vẫn là phạm vi cục bộ (không nhìn thấy ngoài hàm), khác ở thời gian sống.
`static` trên **hàm/biến phạm-vĩ-tệp** thì nghĩa là "riêng của tệp này" —
module 18 dùng nó cho hàm nội bộ.

## Biến phạm vi tệp (toàn cục)

Khai báo ngoài mọi hàm; nhìn thấy từ chỗ khai báo đến hết tệp, sống suốt
chương trình:

```c
int g_attempts = 0;     // mọi hàm bên dưới đều thấy

void attempt(void) { g_attempts++; }
```

Biến toàn cục giúp đọc trạng thái — nhưng trạng thái toàn cục có thể sửa sẽ
trói buộc các hàm vào nhau theo cách phá vỡ việc kiểm thử và tái sử dụng. Quy
tắc của khóa: **truyền những gì hàm cần qua tham số**; chỉ dùng biến toàn cục
cho hằng số mang tính toàn chương trình.

## extern (mức nhận diện)

`extern int g;` nói "g tồn tại, định nghĩa ở nơi khác" — linker nối các chỗ
dùng về một định nghĩa duy nhất. Bạn sẽ cần nó ở module 18; bây giờ chỉ cần
đọc hiểu.
""",
)

write_practice(
    M8,
    "cb-p8-scope",
    "Scope & Storage",
    "Predict and control visibility and lifetime.",
    "Phạm vi & Lưu trữ",
    "Dự đoán và kiểm soát tầm nhìn và thời gian sống.",
    L8B,
    14,
    "beginner",
    [
        challenge(
            "cb8-static-counter",
            "Static Counter",
            "Implement `int next_id(void)` returning 1 on the first call, 2 on the second, 3 on the third — using a static local (no globals).",
            C_PRELUDE,
            [
                ("sequence", "CHECK_EQ(next_id(), 1);\nCHECK_EQ(next_id(), 2);\nCHECK_EQ(next_id(), 3);\nCHECK_EQ(next_id(), 4);\nCHECK_EQ(next_id(), 5);", "static int n = 0; then n++ and return n. One test = one process, so the whole sequence lives in a single test."),
            ],
            level="guided",
        ),
        challenge(
            "cb8-not-static",
            "Automatic Reset",
            "Implement `int auto_counter(void)` that ALWAYS returns 1 — demonstrate that a plain local resets every call.",
            C_PRELUDE,
            [
                ("always one", "CHECK_EQ(auto_counter(), 1);\nCHECK_EQ(auto_counter(), 1);\nCHECK_EQ(auto_counter(), 1);", "int n = 0; n++; return n; — fresh storage each call."),
            ],
            level="imitation",
        ),
        challenge(
            "cb8-shadow-read",
            "Shadow Reading",
            "Implement `int shadow_value(void)`: an outer `int v = 10;` then an inner block declaring its own `int v = 20;` — return the OUTER v after the block (so 10).",
            C_PRELUDE,
            [
                ("outer survives", "CHECK_EQ(shadow_value(), 10);", "The inner v is a different variable; the outer keeps 10."),
            ],
            level="debugging",
        ),
        challenge(
            "cb8-global-sum",
            "Parameter, Not Global",
            "Implement `int total_sum(const int* a, int n)` returning the sum — full marks only if you use NO file-scope variables (parameter in, return out).",
            C_PRELUDE,
            [
                ("basics", "int a[] = {1, 2, 3};\nCHECK_EQ(total_sum(a, 3), 6);", "Accumulate a local and return it."),
                ("empty", "int a[] = {9};\nCHECK_EQ(total_sum(a, 0), 0);", "n=0 means no elements: 0."),
                ("negatives", "int a[] = {-4, 4};\nCHECK_EQ(total_sum(a, 2), 0);", "Signs cancel."),
            ],
            level="independent",
        ),
    ],
    {
        "cb8-static-counter": vi_challenge(
            "Bộ đếm static",
            "Cài `int next_id(void)` trả về 1 ở lần gọi đầu, 2 ở lần hai, 3 ở lần ba — dùng biến static cục bộ (không dùng biến toàn cục).",
            [("dãy số", "static int n = 0; rồi n++ và return n."), ("tiếp tục", "Giá trị được giữ giữa các lần gọi.")],
        ),
        "cb8-not-static": vi_challenge(
            "Tự động đặt lại",
            "Cài `int auto_counter(void)` LUÔN trả về 1 — chứng minh biến thường được đặt lại mỗi lần gọi.",
            [("luôn là một", "int n = 0; n++; return n; — bộ nhớ mới mỗi lần gọi.")],
        ),
        "cb8-shadow-read": vi_challenge(
            "Đọc hiểu che tên",
            "Cài `int shadow_value(void)`: một `int v = 10;` bên ngoài rồi một khối trong khai báo `int v = 20;` riêng — trả về v BÊN NGOÀI sau khối (tức 10).",
            [("bên ngoài sống", "v trong là biến khác; v ngoài vẫn giữ 10.")],
        ),
        "cb8-global-sum": vi_challenge(
            "Tham số, không toàn cục",
            "Cài `int total_sum(const int* a, int n)` trả về tổng — điểm tối đa chỉ khi KHÔNG dùng biến phạm vi tệp (tham số vào, return ra).",
            [("cơ bản", "Cộng dồn vào biến cục bộ rồi trả về."), ("rỗng", "n=0 nghĩa là không phần tử: 0."), ("số âm", "Dấu triệt tiêu.")],
        ),
    },
    solutions=[
        (
            "cb8-static-counter",
            '#include <stdio.h>\nint next_id(void) {\n    static int n = 0;\n    n++;\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint next_id(void) {\n    int n = 0;\n    n++;\n    return n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb8-not-static",
            '#include <stdio.h>\nint auto_counter(void) {\n    int n = 0;\n    n++;\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint auto_counter(void) {\n    static int n = 0;\n    n++;\n    return n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb8-shadow-read",
            '#include <stdio.h>\nint shadow_value(void) {\n    int v = 10;\n    {\n        int v = 20;\n        (void)v;\n    }\n    return v;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint shadow_value(void) {\n    int v = 10;\n    {\n        v = 20;\n    }\n    return v;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb8-global-sum",
            '#include <stdio.h>\nint total_sum(const int* a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint total_sum(const int* a, int n) {\n    int s = 1;\n    for (int i = 0; i < n; i++) s += a[i];\n    return s;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M8,
    L8C,
    "Checkpoint: Scope & Storage",
    "A rate limiter whose state must persist correctly across calls.",
    15,
    r"""
## Checkpoint

Choose the right storage duration: per-call freshness vs. persistent state.
""",
    "Điểm kiểm tra: Phạm vi & Lưu trữ",
    "Chọn đúng thời gian sống: tươi mới theo lời gọi hay trạng thái bền qua các lần gọi.",

    r"""
## Điểm kiểm tra

Chọn đúng thời gian sống: tươi mới theo từng lời gọi, hay trạng thái bền vững
qua các lần gọi.
""",
    challenge(
        "cb8-checkpoint-limiter",
        "Rate Limiter",
        "Implement `int allow_request(void)` using a static local: it returns 1 for the first 3 calls and 0 for every call after (a fixed budget of 3). Also implement `void limiter_reset(void)` that makes the next 3 calls allowed again — two functions sharing one file-scope `static int used;`.",
        C_PRELUDE,
        [
            ("full cycle", "CHECK_EQ(allow_request(), 1);\nCHECK_EQ(allow_request(), 1);\nCHECK_EQ(allow_request(), 1);\nCHECK_EQ(allow_request(), 0);\nCHECK_EQ(allow_request(), 0);", "used < 3 allows; after 3, blocked. One test = one process, so the whole cycle lives in a single test."),
            ("reset refills", "CHECK_EQ(allow_request(), 1);\nlimiter_reset();\nCHECK_EQ(allow_request(), 1);\nCHECK_EQ(allow_request(), 1);\nCHECK_EQ(allow_request(), 1);\nCHECK_EQ(allow_request(), 0);", "After one spent call, reset refills the budget: three allowed again, then blocked."),
        ],
    ),
    vi_challenge(
        "Bộ giới hạn tần suất",
        "Cài `int allow_request(void)` dùng static cục bộ: trả 1 cho 3 lời gọi đầu và 0 cho mọi lời gọi sau (ngân sách cố định 3). Thêm `void limiter_reset(void)` để 3 lời gọi kế tiếp được phép lại — hai hàm dùng chung một biến static phạm vi tệp `static int used;`.",
        [("trọn chu kỳ", "used < 3 thì cho phép; sau 3 lần thì chặn. Một test = một tiến trình, nên cả chu kỳ nằm trong một test."), ("reset nạp lại", "Sau một lần đã dùng, reset nạp lại ngân sách: ba lần được phép tiếp, rồi bị chặn.")],
    ),
    solution='#include <stdio.h>\nstatic int used = 0;\nint allow_request(void) {\n    if (used < 3) {\n        used++;\n        return 1;\n    }\n    return 0;\n}\nvoid limiter_reset(void) {\n    used = 0;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\nstatic int used = 0;\nint allow_request(void) {\n    if (used < 3) {\n        used++;\n        return 1;\n    }\n    return 0;\n}\nvoid limiter_reset(void) {\n    used = 3;\n}\nint main(void) { return 0; }',
)

print("batch 4 complete: modules 7-8")
