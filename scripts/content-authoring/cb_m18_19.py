#!/usr/bin/env python3
"""C Beginner — batch 9: modules 18 (multi-file) and 19 (debugging)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ======================== MODULE 18: multi-file ========================
M18 = "multi-file"

L18A = "api-boundaries"
L18B = "static-privacy"
L18C = "cb-checkpoint-m18"

write_module(
    M18,
    "Multi-File C Projects",
    "Public contracts, private helpers, and the declaration/definition discipline that scales a code base.",
    "Dự án C nhiều tệp",
    "Hợp đồng công khai, trợ giúp riêng tư, và kỷ luật khai báo/định nghĩa giúp mã nguồn lớn lên.",
    [L18A, L18B, L18C],
    ["cb-p18-api", "cb-p18-module"],
)

write_lesson(
    M18,
    L18A,
    "API Boundaries",
    "A module is a promise: the header declares what callers may use, the .c decides how it works.",
    14,
    r"""
## The one-file preview of the two-file world

This course's sandbox compiles a single file, so we rehearse the multi-file
pattern inside it. The rules are exactly the ones a real `geom.h` + `geom.c`
project follows:

```c
/* ---- the CONTRACT (what geom.h would say) ---- */
int stack_push(int v);          // callers may call this
int stack_pop(int *out);        // callers may call this

/* ---- the IMPLEMENTATION (what geom.c would contain) ---- */
static int data[16];            // private: callers never touch this
static int count = 0;           // private state

int stack_push(int v) {
    if (count == 16) return 0;  // full: report failure
    data[count++] = v;
    return 1;
}

int stack_pop(int *out) {
    if (out == NULL || count == 0) return 0;
    *out = data[--count];
    return 1;
}
```

## What makes it a boundary

- **public**: functions a caller is allowed to call — declared first, no
  `static`
- **private**: `static` data and helpers — invisible outside the module
- The header never contains `static` state or function bodies; it is pure
  promise.

## The discipline the compiler enforces

Callers can only reach the public functions. When the private representation
changes (array size, algorithm), no caller's code changes — the boundary held.
That property is the entire point of modules.

## Prototype-then-define inside one file

The same contract/check shape works inside one translation unit: declare the
public functions at the top (that's the "header" region), define them below.
`gcc` checks every call against the declaration, exactly as it would against
a real header.
""",
    "Ranh giới API",
    "Một module là một lời hứa: header khai báo người gọi được dùng gì, còn tệp .c quyết định làm thế nào.",
    r"""
## Xem trước thế giới hai tệp trong một tệp

Sandbox của khóa này biên dịch một tệp, nên ta diễn tập mẫu nhiều tệp ngay
trong đó. Các quy tắc chính là những gì một dự án thật `geom.h` + `geom.c`
tuân theo:

```c
/* ---- HỢP ĐỒNG (thứ geom.h sẽ nói) ---- */
int stack_push(int v);          // người gọi được phép gọi
int stack_pop(int *out);        // người gọi được phép gọi

/* ---- CÀI ĐẶT (thứ geom.c sẽ chứa) ---- */
static int data[16];            // riêng tư: người gọi không đụng tới
static int count = 0;           // trạng thái riêng tư

int stack_push(int v) {
    if (count == 16) return 0;  // đầy: báo thất bại
    data[count++] = v;
    return 1;
}

int stack_pop(int *out) {
    if (out == NULL || count == 0) return 0;
    *out = data[--count];
    return 1;
}
```

## Điều gì khiến nó thành ranh giới

- **công khai**: các hàm người gọi được phép gọi — khai báo trước, không
  `static`
- **riêng tư**: dữ liệu và helper `static` — vô hình bên ngoài module
- Header không bao giờ chứa trạng thái `static` hay thân hàm; nó thuần là
  lời hứa.

## Kỷ luật mà trình biên dịch bắt buộc

Người gọi chỉ chạm tới các hàm công khai. Khi phần biểu diễn riêng tư thay đổi
(kích thước mảng, thuật toán), mã của người gọi không đổi — ranh giới giữ vững.
Đó chính là toàn bộ ý nghĩa của module.

## Khai-báo-rồi-định-nghĩa trong một tệp

Hình dạng hợp đồng/kiểm tra như vậy hoạt động cả trong một đơn vị dịch: khai
báo các hàm công khai ở đầu (vùng "header"), định nghĩa bên dưới. `gcc` kiểm
tra mọi lời gọi theo khai báo, y như với header thật.
""",
)

write_lesson(
    M18,
    L18B,
    "static: Private by Default",
    "static functions and file-scope state are the C visibility keyword.",
    13,
    r"""
## Two meanings of static, one idea: private + persistent

On a **function**: visible only within this translation unit.

```c
static int helper(int x) { return x * 2; }   // nobody outside can link to this
```

On a **file-scope variable**: visible only within this unit AND lives for the
whole program run.

```c
static int hits = 0;     // private counter, persists between calls
void count_hit(void) { hits++; }
int hit_count(void) { return hits; }
```

## Why default-private wins

A function named `helper` without static becomes a global name. Link two .c
files that both define `helper` and the linker fails: duplicate symbol. With
`static`, each file's helper is its own — no collision, no accidental coupling.

Rule of thumb: **every helper starts static**; promote to public only when a
caller genuinely needs it.

## Reusable modules in one file: a "library section"

```c
/* ===== strlib (the module) ===== */
static int is_vowel(char c) {
    return c=='a'||c=='e'||c=='i'||c=='o'||c=='u';
}
int count_vowels(const char *s) {          // public
    int n = 0;
    for (; *s; s++) n += is_vowel(*s);
    return n;
}
/* ===== end strlib ===== */
```

Later files/modules (arrays + structs, module 20) build the same shape: a
private representation, public operations, callers that never peek inside.
""",
    "static: Riêng tư theo mặc định",
    "Hàm static và biến static cấp tệp là từ khóa về khả năng hiển thị của C.",
    r"""
## Hai nghĩa của static, một ý tưởng: riêng tư + bền vững

Trên một **hàm**: chỉ hiện hữu trong đơn vị dịch này.

```c
static int helper(int x) { return x * 2; }   // không ai bên ngoài link tới được
```

Trên một **biến cấp tệp**: chỉ hiện hữu trong đơn vị này VÀ sống suốt chương
trình.

```c
static int hits = 0;     // bộ đếm riêng tư, giữ giá trị giữa các lần gọi
void count_hit(void) { hits++; }
int hit_count(void) { return hits; }
```

## Vì sao mặc định riêng tư là thắng

Một hàm tên `helper` không có static sẽ thành tên toàn cục. Link hai tệp .c
cùng định nghĩa `helper` và linker lỗi: trùng ký hiệu. Với `static`, helper
của mỗi tệp là của riêng nó — không xung đột, không ghép nối vô ý.

Kinh nghiệm: **mọi helper đều bắt đầu bằng static**; chỉ nâng lên công khai
khi người gọi thực sự cần.

## Module tái sử dụng trong một tệp: một "khu thư viện"

```c
/* ===== strlib (module) ===== */
static int is_vowel(char c) {
    return c=='a'||c=='e'||c=='i'||c=='o'||c=='u';
}
int count_vowels(const char *s) {          // công khai
    int n = 0;
    for (; *s; s++) n += is_vowel(*s);
    return n;
}
/* ===== hết strlib ===== */
```

Các module sau (mảng + struct, module 20) dựng cùng hình dạng: một phần biểu
diễn riêng tư, các thao tác công khai, người gọi không bao giờ nhìn vào trong.
""",
)

write_practice(
    M18,
    "cb-p18-api",
    "API Discipline",
    "Modules with private state reached only through public functions.",
    "Kỷ luật API",
    "Các module có trạng thái riêng tư chỉ chạm tới qua hàm công khai.",
    L18A,
    16,
    "beginner",
    [
        challenge(
            "cb18-counter-module",
            "Counter Module",
            "Build a counter module: private file-scope state, public `void counter_reset(void)`, `void counter_add(int n)`, and `int counter_value(void)` returning the running total.",
            "#include <stdio.h>\n",
            [
                ("starts at zero", "counter_reset();\nCHECK_EQ(counter_value(), 0);", "Reset defines the zero point."),
                ("accumulates", "counter_reset();\ncounter_add(5);\ncounter_add(7);\nCHECK_EQ(counter_value(), 12);", "Adds accumulate."),
                ("negative add", "counter_reset();\ncounter_add(3);\ncounter_add(-2);\nCHECK_EQ(counter_value(), 1);", "Add can subtract."),
            ],
            level="guided",
        ),
        challenge(
            "cb18-fifo-module",
            "FIFO Module",
            "Build a bounded queue: private storage, public `void q_clear(void)`, `int q_push(int v)` (0 when full, capacity 8), `int q_pop(int *out)` (0 when empty or out==NULL, else 1 and the OLDEST value).",
            "#include <stdio.h>\n",
            [
                ("fifo order", "q_clear();\nq_push(1); q_push(2); q_push(3);\nint v;\nq_pop(&v);\nCHECK_EQ(v, 1);\nq_pop(&v);\nCHECK_EQ(v, 2);", "First in, first out."),
                ("full rejected", "q_clear();\nfor (int i = 0; i < 8; i++) q_push(i);\nCHECK_EQ(q_push(99), 0);", "Capacity 8: the 9th fails."),
                ("empty rejected", "q_clear();\nint v;\nCHECK_EQ(q_pop(&v), 0);", "Nothing to pop."),
                ("null out", "q_clear();\nq_push(4);\nCHECK_EQ(q_pop(NULL), 0);", "NULL out must be rejected safely."),
            ],
            level="independent",
        ),
        challenge(
            "cb18-registry-module",
            "Name Registry",
            "Build a registry of up to 16 names: private storage, public `int reg_add(const char *name)` (1 = added, 0 = full or NULL), `int reg_has(const char *name)` (1 if present), `int reg_count(void)`.",
            "#include <stdio.h>\n#include <string.h>\n",
            [
                ("add and has", "reg_clear();\nCHECK_EQ(reg_add(\"ana\"), 1);\nCHECK_EQ(reg_has(\"ana\"), 1);\nCHECK_EQ(reg_has(\"bob\"), 0);", "Add then query."),
                ("duplicate rejected", "reg_clear();\nreg_add(\"ana\");\nCHECK_EQ(reg_add(\"ana\"), 0);\nCHECK_EQ(reg_count(), 1);", "Same name twice: the second fails."),
                ("null name", "CHECK_EQ(reg_add(NULL), 0);", "NULL is never stored."),
                ("count", "reg_clear();\nreg_add(\"a\"); reg_add(\"b\");\nCHECK_EQ(reg_count(), 2);", "Count tracks additions."),
            ],
            level="independent",
        ),
    ],
    {
        "cb18-counter-module": vi_challenge(
            "Module bộ đếm",
            "Dựng module bộ đếm: trạng thái riêng tư cấp tệp, công khai `void counter_reset(void)`, `void counter_add(int n)`, và `int counter_value(void)` trả tổng chạy dồn.",
            [("bắt đầu từ 0", "Reset định nghĩa điểm 0."), ("cộng dồn", "Các lần add cộng dồn."), ("add âm", "Add có thể trừ.")],
        ),
        "cb18-fifo-module": vi_challenge(
            "Module FIFO",
            "Dựng hàng đợi giới hạn: kho riêng tư, công khai `void q_clear(void)`, `int q_push(int v)` (0 khi đầy, sức chứa 8), `int q_pop(int *out)` (0 khi rỗng hoặc out==NULL, nếu không 1 và giá trị CŨ NHẤT).",
            [("thứ tự fifo", "Vào trước, ra trước."), ("đầy thì từ chối", "Sức chứa 8: phần tử thứ 9 thất bại."), ("rỗng thì từ chối", "Không có gì để pop."), ("out NULL", "NULL out phải bị từ chối an toàn.")],
        ),
        "cb18-registry-module": vi_challenge(
            "Sổ đăng ký tên",
            "Dựng sổ đăng ký tối đa 16 tên: kho riêng tư, công khai `int reg_add(const char *name)` (1 = thêm được, 0 = đầy hoặc NULL), `int reg_has(const char *name)` (1 nếu có), `int reg_count(void)`.",
            [("thêm rồi tra", "Add rồi truy vấn."), ("trùng bị từ chối", "Cùng tên hai lần: lần hai thất bại."), ("tên NULL", "NULL không bao giờ được lưu."), ("đếm", "Đếm theo lần thêm thành công.")],
        ),
    },
    solutions=[
        (
            "cb18-counter-module",
            '#include <stdio.h>\nstatic int total = 0;\nvoid counter_reset(void) { total = 0; }\nvoid counter_add(int n) { total += n; }\nint counter_value(void) { return total; }\nint main(void) { return 0; }',
            '#include <stdio.h>\nstatic int total = 0;\nvoid counter_reset(void) { total = 0; }\nvoid counter_add(int n) { total += n; }\nint counter_value(void) { return total + 1; }\nint main(void) { return 0; }',
        ),
        (
            "cb18-fifo-module",
            '#include <stdio.h>\n#define QCAP 8\nstatic int buf[QCAP];\nstatic int head = 0, tail = 0, size = 0;\nvoid q_clear(void) { head = tail = size = 0; }\nint q_push(int v) {\n    if (size == QCAP) return 0;\n    buf[tail] = v;\n    tail = (tail + 1) % QCAP;\n    size++;\n    return 1;\n}\nint q_pop(int *out) {\n    if (out == NULL || size == 0) return 0;\n    *out = buf[head];\n    head = (head + 1) % QCAP;\n    size--;\n    return 1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#define QCAP 8\nstatic int buf[QCAP];\nstatic int head = 0, tail = 0, size = 0;\nvoid q_clear(void) { head = tail = size = 0; }\nint q_push(int v) {\n    if (size == QCAP) return 0;\n    buf[tail] = v;\n    tail = (tail + 1) % QCAP;\n    size++;\n    return 1;\n}\nint q_pop(int *out) {\n    if (out == NULL || size == 0) return 0;\n    *out = buf[tail];\n    head = (head + 1) % QCAP;\n    size--;\n    return 1;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb18-registry-module",
            '#include <stdio.h>\n#include <string.h>\n#define RCAP 16\nstatic char names[RCAP][32];\nstatic int ncount = 0;\nvoid reg_clear(void) { ncount = 0; }\nint reg_has(const char *name) {\n    if (name == NULL) return 0;\n    for (int i = 0; i < ncount; i++)\n        if (strcmp(names[i], name) == 0) return 1;\n    return 0;\n}\nint reg_add(const char *name) {\n    if (name == NULL || ncount == RCAP) return 0;\n    if (reg_has(name)) return 0;\n    strcpy(names[ncount], name);\n    ncount++;\n    return 1;\n}\nint reg_count(void) { return ncount; }\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\n#define RCAP 16\nstatic char names[RCAP][32];\nstatic int ncount = 0;\nvoid reg_clear(void) { ncount = 0; }\nint reg_has(const char *name) {\n    if (name == NULL) return 0;\n    for (int i = 0; i < ncount; i++)\n        if (strcmp(names[i], name) == 0) return 1;\n    return 0;\n}\nint reg_add(const char *name) {\n    if (name == NULL || ncount == RCAP) return 0;\n    strcpy(names[ncount], name);\n    ncount++;\n    return 1;\n}\nint reg_count(void) { return ncount; }\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M18,
    "cb-p18-module",
    "Library Building",
    "A string library and a math library, each with static helpers behind public functions.",
    "Dựng thư viện",
    "Một thư viện chuỗi và một thư viện toán, mỗi thư viện có helper static đằng sau hàm công khai.",
    L18B,
    16,
    "beginner",
    [
        challenge(
            "cb18-strlib",
            "strlib: Vowel Report",
            "Implement public `int count_vowels(const char *s)` (aeiou, case-insensitive) and public `double vowel_ratio(const char *s)` (vowels / length; empty string -> 0.0), backed by a static helper `static int is_vowel_ci(char c)`.",
            "#include <stdio.h>\n#include <string.h>\n",
            [
                ("count", "CHECK_EQ(count_vowels(\"Hello\"), 2);", "e and o."),
                ("case insensitive", "CHECK_EQ(count_vowels(\"AEIOU\"), 5);", "Upper case counts."),
                ("none", "CHECK_EQ(count_vowels(\"xyz\"), 0);", "Zero vowels."),
                ("ratio", "CHECK_NEAR(vowel_ratio(\"Hello\"), 0.4, 1e-9);", "2/5 = 0.4."),
                ("empty ratio", "CHECK_NEAR(vowel_ratio(\"\"), 0.0, 1e-9);", "Empty string: 0.0, no division by zero."),
            ],
            level="independent",
        ),
        challenge(
            "cb18-mathlib",
            "mathlib: GCD & LCM",
            "Implement public `int gcd(int a, int b)` (Euclid, inputs > 0) and public `long lcm(int a, int b)` (a*b/gcd), backed by static validation you choose.",
            "#include <stdio.h>\n",
            [
                ("gcd", "CHECK_EQ(gcd(12, 18), 6);", "Euclid's algorithm."),
                ("coprime", "CHECK_EQ(gcd(7, 13), 1);", "No common factor."),
                ("equal", "CHECK_EQ(gcd(9, 9), 9);", "gcd(n, n) = n."),
                ("lcm", "CHECK_EQ(lcm(4, 6), 12);", "24/2."),
                ("lcm coprime", "CHECK_EQ(lcm(3, 5), 15);", "No shared factor: product."),
            ],
            level="independent",
        ),
        challenge(
            "cb18-textstats",
            "textstats: Word Count",
            "Implement public `int count_words(const char *s)` where words are maximal runs of non-space characters (space = ' ', '\\t', '\\n'), with a static helper for the space test.",
            "#include <stdio.h>\n#include <string.h>\n",
            [
                ("basic", "CHECK_EQ(count_words(\"one two three\"), 3);", "Three runs."),
                ("extra spaces", "CHECK_EQ(count_words(\"  a   b  \"), 2);", "Leading/trailing/extra ignored."),
                ("tabs and newlines", "CHECK_EQ(count_words(\"a\\tb\\nc\"), 3);", "All whitespace separates."),
                ("empty", "CHECK_EQ(count_words(\"\"), 0);", "No characters, no words."),
            ],
            level="independent",
        ),
    ],
    {
        "cb18-strlib": vi_challenge(
            "strlib: Báo cáo nguyên âm",
            "Cài công khai `int count_vowels(const char *s)` (aeiou, không phân biệt hoa thường) và công khai `double vowel_ratio(const char *s)` (nguyên âm / độ dài; chuỗi rỗng -> 0.0), đằng sau là helper static `static int is_vowel_ci(char c)`.",
            [("đếm", "e và o."), ("không phân biệt hoa thường", "Chữ hoa cũng được tính."), ("không có", "Không nguyên âm nào."), ("tỉ lệ", "2/5 = 0.4."), ("tỉ lệ rỗng", "Chuỗi rỗng: 0.0, không chia cho 0.")],
        ),
        "cb18-mathlib": vi_challenge(
            "mathlib: GCD & LCM",
            "Cài công khai `int gcd(int a, int b)` (Euclid, đầu vào > 0) và công khai `long lcm(int a, int b)` (a*b/gcd), kèm phần kiểm tra static do bạn chọn.",
            [("gcd", "Thuật toán Euclid."), ("nguyên tố cùng nhau", "Không thừa số chung."), ("bằng nhau", "gcd(n, n) = n."), ("lcm", "24/2."), ("lcm nguyên tố cùng nhau", "Không thừa số chung: tích.")],
        ),
        "cb18-textstats": vi_challenge(
            "textstats: Đếm từ",
            "Cài công khai `int count_words(const char *s)` với từ là các dãy ký tự không phải dấu cách dài nhất (dấu cách = ' ', '\\t', '\\n'), có helper static cho phép thử dấu cách.",
            [("cơ bản", "Ba dãy."), ("thừa dấu cách", "Đầu/cuối/thừa đều bỏ qua."), ("tab và xuống dòng", "Mọi khoảng trắng đều phân tách."), ("rỗng", "Không ký tự, không từ.")],
        ),
    },
    solutions=[
        (
            "cb18-strlib",
            '#include <stdio.h>\n#include <string.h>\nstatic int is_vowel_ci(char c) {\n    if (c >= \'A\' && c <= \'Z\') c = (char)(c + 32);\n    return c==\'a\'||c==\'e\'||c==\'i\'||c==\'o\'||c==\'u\';\n}\nint count_vowels(const char *s) {\n    int n = 0;\n    for (; *s; s++) n += is_vowel_ci(*s);\n    return n;\n}\ndouble vowel_ratio(const char *s) {\n    size_t len = strlen(s);\n    if (len == 0) return 0.0;\n    return (double)count_vowels(s) / (double)len;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nstatic int is_vowel_ci(char c) {\n    if (c >= \'A\' && c <= \'Z\') c = (char)(c + 32);\n    return c==\'a\'||c==\'e\'||c==\'i\'||c==\'o\'||c==\'u\';\n}\nint count_vowels(const char *s) {\n    int n = 0;\n    for (; *s; s++) n += is_vowel_ci(*s);\n    return n + 1;\n}\ndouble vowel_ratio(const char *s) {\n    size_t len = strlen(s);\n    if (len == 0) return 0.0;\n    return (double)count_vowels(s) / (double)len;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb18-mathlib",
            '#include <stdio.h>\nint gcd(int a, int b) {\n    while (b != 0) { int t = a % b; a = b; b = t; }\n    return a;\n}\nlong lcm(int a, int b) {\n    return (long)a * b / gcd(a, b);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint gcd(int a, int b) {\n    while (b != 0) { int t = a % b; a = b; b = t; }\n    return a + 1;\n}\nlong lcm(int a, int b) {\n    return (long)a * b / gcd(a, b);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb18-textstats",
            '#include <stdio.h>\n#include <string.h>\nstatic int is_space(char c) {\n    return c == \' \' || c == \'\\t\' || c == \'\\n\';\n}\nint count_words(const char *s) {\n    int words = 0, in_word = 0;\n    for (; *s; s++) {\n        if (is_space(*s)) in_word = 0;\n        else if (!in_word) { in_word = 1; words++; }\n    }\n    return words;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nstatic int is_space(char c) {\n    return c == \' \' || c == \'\\t\' || c == \'\\n\';\n}\nint count_words(const char *s) {\n    int words = 0, in_word = 0;\n    for (; *s; s++) {\n        if (is_space(*s)) in_word = 0;\n        else if (!in_word) { in_word = 1; words++; }\n    }\n    return words + 1;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M18,
    L18C,
    "Checkpoint: Modules",
    "A temperature library: conversion pair plus a stats summary, private helpers inside.",
    16,
    r"""
## Checkpoint

If your module's public functions are the only thing callers need, the
boundary is right.
""",
    "Điểm kiểm tra: Module",
    "Thư viện nhiệt độ: cặp chuyển đổi kèm tổng kết thống kê, helper riêng tư bên trong.",
    r"""
## Điểm kiểm tra

Nếu các hàm công khai của module là thứ duy nhất người gọi cần, ranh giới đã
đúng.
""",
    challenge(
        "cb18-checkpoint-templib",
        "templib",
        "Implement public `double c_to_f(double c)` (c*9/5+32) and public `double f_to_c(double f)` ((f-32)*5/9), plus public `int comfy_count(const double *cs, int n)` counting temperatures within [18.0, 26.0] inclusive. Use whatever static helpers you like.",
        "#include <stdio.h>\n",
        [
            ("c to f", "CHECK_NEAR(c_to_f(100.0), 212.0, 1e-9);", "Boiling point."),
            ("f to c", "CHECK_NEAR(f_to_c(32.0), 0.0, 1e-9);", "Freezing point."),
            ("round trip", "CHECK_NEAR(f_to_c(c_to_f(23.5)), 23.5, 1e-9);", "Conversions invert."),
            ("comfy count", "double ts[] = {10.0, 20.0, 26.0, 27.0};\nCHECK_EQ(comfy_count(ts, 4), 2);", "Bounds are inclusive."),
            ("comfy none", "double ts[] = {5.0};\nCHECK_EQ(comfy_count(ts, 1), 0);", "Too cold."),
        ],
    ),
    vi_challenge(
        "templib",
        "Cài công khai `double c_to_f(double c)` (c*9/5+32) và công khai `double f_to_c(double f)` ((f-32)*5/9), cộng `int comfy_count(const double *cs, int n)` đếm nhiệt độ nằm trong [18.0, 26.0] (bao gồm biên). Dùng helper static tùy ý.",
        [("c sang f", "Điểm sôi."), ("f sang c", "Điểm đóng băng."), ("vòng hai chiều", "Hai phép chuyển đổi nghịch đảo nhau."), ("đếm dễ chịu", "Hai biên đều thuộc khoảng."), ("không dễ chịu", "Quá lạnh.")],
    ),
    solution='#include <stdio.h>\ndouble c_to_f(double c) {\n    return c * 9.0 / 5.0 + 32.0;\n}\ndouble f_to_c(double f) {\n    return (f - 32.0) * 5.0 / 9.0;\n}\nint comfy_count(const double *cs, int n) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (cs[i] >= 18.0 && cs[i] <= 26.0) c++;\n    return c;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\ndouble c_to_f(double c) {\n    return c * 9.0 / 5.0 + 32.0;\n}\ndouble f_to_c(double f) {\n    return (f - 32.0) * 5.0 / 9.0;\n}\nint comfy_count(const double *cs, int n) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (cs[i] > 18.0 && cs[i] < 26.0) c++;\n    return c;\n}\nint main(void) { return 0; }',
)

# ========================== MODULE 19: debugging ==========================
M19 = "debugging"

L19A = "reading-compiler-output"
L19B = "runtime-failures"
L19C = "forensic-habits"
L19D = "cb-checkpoint-m19"

write_module(
    M19,
    "Debugging C",
    "Reading warnings, recognizing the classic crashes, and forming the forensic habits that find bugs fast.",
    "Gỡ lỗi C",
    "Đọc warning, nhận diện các kiểu crash kinh điển, và rèn thói quen pháp y giúp tìm lỗi nhanh.",
    [L19A, L19B, L19C, L19D],
    ["cb-p19-warnings", "cb-p19-crash"],
)

write_lesson(
    M19,
    L19A,
    "Reading Compiler Output",
    "Warnings are the compiler handing you the bug report before the crash.",
    14,
    r"""
## Compile with warnings ON, always

```sh
gcc -std=c23 -Wall -Wextra -o app main.c
```

`-Wall -Wextra` is the default posture for this course's challenges too: the
build warnings you see are the same ones the grader sees.

## The warnings that mark real bugs

- `unused variable` — you computed something and never used it: often a
  forgotten step
- `uninitialized` — the value is read before any assignment: undefined
  behavior waiting to happen
- `wrong format specifier` — `printf("%d", 3.14)` prints garbage: the type
  and the format must agree
- `control reaches end of non-void function` — a code path returns nothing
- `assignment in condition` — `if (x = 5)` assigns, then tests 5; you
  probably meant `==`

## Read errors bottom-up

The FIRST error is the real one; later errors are often its shockwaves. Fix
the first, recompile, repeat. And read the caret line (`^`) — the compiler
points at the exact token it choked on.

## Error vs warning

A warning compiles anyway — the program runs, wrongly. The discipline:
**treat every warning as a bug**. `-Werror` (turn warnings into errors) is
how professional builds enforce it.
""",
    "Đọc đầu ra trình biên dịch",
    "Warning là trình biên dịch đưa cho bạn báo cáo lỗi trước khi crash.",
    r"""
## Luôn biên dịch với warning bật

```sh
gcc -std=c23 -Wall -Wextra -o app main.c
```

`-Wall -Wextra` cũng là tư thế mặc định cho các challenge của khóa này:
warning build bạn thấy chính là warning bộ chấm thấy.

## Những warning đánh dấu lỗi thật

- `unused variable` — bạn tính một thứ mà không dùng: thường là một bước bị
  quên
- `uninitialized` — giá trị được đọc trước khi gán: hành vi không xác định
  chực chờ
- `wrong format specifier` — `printf("%d", 3.14)` in ra rác: kiểu và định
  dạng phải khớp
- `control reaches end of non-void function` — một đường đi trong hàm không
  trả về gì cả
- `assignment in condition` — `if (x = 5)` gán rồi kiểm tra 5; có lẽ bạn định
  `==`

## Đọc lỗi từ trên xuống... nói đúng hơn, từ lỗi đầu tiên

Lỗi ĐẦU TIÊN mới là lỗi thật; các lỗi sau thường chỉ là sóng xung kích. Sửa
lỗi đầu, biên dịch lại, lặp lại. Và đọc dòng mũi (`^`) — trình biên dịch chỉ
thẳng vào token khiến nó nghẹn.

## Error vs warning

Warning vẫn biên dịch được — chương trình chạy, nhưng chạy sai. Kỷ luật:
**coi mọi warning là lỗi**. `-Werror` (biến warning thành lỗi) là cách các
build chuyên nghiệp bắt buộc điều đó.
""",
)

write_lesson(
    M19,
    L19B,
    "Runtime Failures",
    "Segfaults, wrong outputs, and hangs: the three failure families and their usual suspects.",
    14,
    r"""
## Family 1: the crash (segfault)

The process dies with `Segmentation fault`. Usual suspects, in order:

1. NULL or uninitialized pointer dereference
2. out-of-bounds array index
3. use-after-free / dangling pointer
4. writing through a bad pointer in a string function

A segfault tells you WHERE it died (the stack trace) but not WHY — the bad
address was usually produced much earlier.

## Family 2: wrong output, no crash

The sneakiest. Causes: off-by-one loop bounds, wrong comparison operator,
accumulating into the wrong variable, format-specifier mismatch, integer
division where you meant floating division. The defense is tests with known
answers — exactly what this course's challenges run against your code.

## Family 3: the hang

An infinite loop: the counter never moves toward the bound, or the
termination condition can never become false. Check that something in the
loop body changes every iteration.

## The debugging loop

1. reproduce — find the smallest input that fails
2. predict — say out loud what SHOULD happen
3. instrument — print the values at each step (printf is the oldest
   debugger and still a great one)
4. narrow — binary-search the pipeline: is the input already wrong, or the
   processing?
5. fix the cause, not the symptom — a swallowed crash returns as a worse bug
""",
    "Thất bại lúc chạy",
    "Segfault, đầu ra sai, và treo: ba nhóm thất bại và các nghi phạm quen thuộc.",
    r"""
## Nhóm 1: crash (segfault)

Tiến trình chết với `Segmentation fault`. Các nghi phạm quen thuộc, theo thứ
tự:

1. giải tham chiếu NULL hoặc con trỏ chưa khởi tạo
2. chỉ số mảng vượt biên
3. use-after-free / con trỏ treo
4. ghi qua con trỏ xấu trong hàm chuỗi

Segfault cho bạn biết nó chết Ở ĐÂU (stack trace) nhưng không cho biết TẠI
SAO — địa chỉ xấu thường được tạo ra từ rất trước đó.

## Nhóm 2: đầu ra sai, không crash

Khó phát hiện nhất. Nguyên nhân: biên vòng lặp lệch một, toán tử so sánh sai,
cộng dồn vào nhầm biến, định dạng printf không khớp kiểu, chia số nguyên khi
ý định là chia thực. Hàng phòng thủ là các test có đáp án đã biết — chính là
những gì challenge của khóa này chạy với mã của bạn.

## Nhóm 3: treo

Vòng lặp vô hạn: bộ đếm không bao giờ tiến về giới hạn, hoặc điều kiện dừng
không bao giờ trở thành sai. Kiểm tra xem có gì đó trong thân vòng lặp thay
đổi sau mỗi vòng hay không.

## Vòng lặp gỡ lỗi

1. tái hiện — tìm đầu vào nhỏ nhất gây sai
2. dự đoán — nói to điều Đáng lẽ phải xảy ra
3. đo đạc — in giá trị ở từng bước (printf là debugger lâu đời nhất và vẫn
   rất tốt)
4. thu hẹp — chia đôi đường ống: đầu vào đã sai sẵn, hay phần xử lý sai?
5. sửa nguyên nhân, không sửa triệu chứng — một crash bị nuốt sẽ quay lại
   thành lỗi còn tệ hơn
""",
)

write_lesson(
    M19,
    L19C,
    "Forensic Habits",
    "What a strict warning build says about broken code — and how to interrogate a failing program.",
    13,
    r"""
## Sanitizers: know the name, mind the platform

AddressSanitizer and UBSan catch memory and undefined-behavior bugs at
runtime. This course's sandbox image does NOT ship them, so we do not use
them here — but on a Linux dev box they are the first tools to reach for:

```sh
gcc -fsanitize=address,undefined ...   # works on glibc toolchains
```

Here, your sanitizer is the **warning build plus careful reading**.

## Forensics from warnings alone

A strict build over buggy code is surprisingly loud:

- comparing with `=` instead of `==` → `assignment in condition`
- reading an uninitialized local → `may be used uninitialized`
- a format/type mismatch → `-Wformat`
- a missing return path → `control reaches end of non-void function`
- an unused result that should have been stored → `unused value`

When a program misbehaves, recompile with `-Wall -Wextra` FIRST. Half of
beginner bugs confess immediately.

## Interrogating a wrong answer

- print the inputs at the boundary (what exactly did the function receive?)
- print after each transformation (where does good data turn bad?)
- check the loop bounds by hand on a 3-element example
- verify types: is `a/b` doing integer division when you meant double?

## The habit stack

Fix, then re-run EVERYTHING (not just the failing case) — fixes often break
the neighbors. And when you find the bug, ask "what let this type of bug
in?" — the answer is usually a missing test, which you then write down.
""",
    "Thói quen pháp y",
    "Build warning nghiêm ngặt nói gì về mã lỗi — và cách thẩm vấn một chương trình chạy sai.",
    r"""
## Sanitizer: biết tên, lưu ý nền tảng

AddressSanitizer và UBSan bắt lỗi bộ nhớ và hành vi không xác định ngay lúc
chạy. Ảnh sandbox của khóa này KHÔNG có chúng, nên ở đây ta không dùng —
nhưng trên máy dev Linux, đây là những công cụ đầu tiên nên chạm tới:

```sh
gcc -fsanitize=address,undefined ...   # hoạt động trên chuỗi công cụ glibc
```

Ở đây, sanitizer của bạn là **build warning cộng với đọc cẩn thận**.

## Pháp y chỉ từ warning

Một build nghiêm ngặt trên mã lỗi ồn ào một cách đáng ngạc nhiên:

- so sánh bằng `=` thay vì `==` → `assignment in condition`
- đọc biến cục bộ chưa khởi tạo → `may be used uninitialized`
- kiểu/định dạng không khớp → `-Wformat`
- thiếu đường trả về → `control reaches end of non-void function`
- một kết quả đáng lẽ phải lưu lại → `unused value`

Khi chương trình cư xử sai, hãy biên dịch lại với `-Wall -Wextra` TRƯỚC.
Một nửa lỗi người mới tự thú ngay lập tức.

## Thẩm vấn một đáp án sai

- in đầu vào tại ranh giới (hàm nhận được chính xác cái gì?)
- in sau mỗi lần biến đổi (dữ liệu tốt trở thành xấu từ đâu?)
- tự tay kiểm tra biên vòng lặp trên ví dụ 3 phần tử
- xác minh kiểu: `a/b` đang là chia số nguyên trong khi ý bạn là chia double?

## Ngăn xép thói quen

Sửa xong, chạy lại TẤT CẢ (không chỉ case đang fail) — bản sửa thường làm
hỏng hàng xóm. Và khi tìm ra lỗi, hãy hỏi "điều gì đã cho phép loại lỗi này
lọt vào?" — câu trả lời thường là một test còn thiếu, và bạn sẽ viết nó ra.
""",
)

write_practice(
    M19,
    "cb-p19-warnings",
    "Warning Forensics",
    "Fix the classic warning-marked defects: assignment-in-condition, wrong format, missing return, uninitialized read.",
    "Pháp y từ warning",
    "Sửa các lỗi kinh điển bị warning tố cáo: gán trong điều kiện, định dạng sai, thiếu return, đọc biến chưa khởi tạo.",
    L19A,
    16,
    "beginner",
    [
        challenge(
            "cb19-fix-assign-cond",
            "Fix: = vs ==",
            "`is_full(int used, int cap)` below ALWAYS returns 1 — the condition assigns instead of comparing. Fix it so it returns 1 exactly when used == cap.\n\n```c\nint is_full(int used, int cap) {\n    int r;\n    if (used = cap) r = 1; else r = 0;\n    return r;\n}\n```",
            C_PRELUDE,
            [
                ("full", "CHECK_EQ(is_full(8, 8), 1);", "Equal counts as full."),
                ("not full", "CHECK_EQ(is_full(7, 8), 0);", "Fewer than cap is not full."),
                ("empty", "CHECK_EQ(is_full(0, 8), 0);", "Empty is not full."),
            ],
            level="guided",
        ),
        challenge(
            "cb19-fix-format",
            "Fix: Wrong Format Specifier",
            "Implement `void format_price(double p, char *out)` writing `price=<value>` into out with snprintf, where <value> uses printf's %g formatting for the double. The classic bug is %d with a double — yours must be correct.",
            "#include <stdio.h>\n",
            [
                ("basic", "char buf[32] = {0};\nformat_price(12.5, buf);\nCHECK_STR_EQ(buf, \"price=12.5\");", "snprintf(out, 32, \"price=%g\", p)."),
                ("integer valued", "char buf[32] = {0};\nformat_price(7.0, buf);\nCHECK_STR_EQ(buf, \"price=7\");", "%g drops the trailing .0."),
                ("longer", "char buf[32] = {0};\nformat_price(1234.5, buf);\nCHECK_STR_EQ(buf, \"price=1234.5\");", "Bigger values too."),
            ],
            level="guided",
        ),
        challenge(
            "cb19-fix-missing-return",
            "Fix: Missing Return Path",
            "`sign_of(int x)` falls off the end for x > 0 — undefined behavior. Fix it so it returns -1, 0, or 1 for negative, zero, and positive.\n\n```c\nint sign_of(int x) {\n    if (x < 0) return -1;\n    if (x == 0) return 0;\n}\n```",
            C_PRELUDE,
            [
                ("negative", "CHECK_EQ(sign_of(-4), -1);", "Negative path."),
                ("zero", "CHECK_EQ(sign_of(0), 0);", "Zero path."),
                ("positive", "CHECK_EQ(sign_of(4), 1);", "The missing path: return 1."),
            ],
            level="guided",
        ),
        challenge(
            "cb19-fix-uninit",
            "Fix: Uninitialized Accumulator",
            "`sum_evens(const int *a, int n)` reads `total` before initializing it. Fix the function so it returns the sum of even elements.\n\n```c\nint sum_evens(const int *a, int n) {\n    int total;\n    for (int i = 0; i < n; i++)\n        if (a[i] % 2 == 0) total += a[i];\n    return total;\n}\n```",
            C_PRELUDE,
            [
                ("mixed", "int a[] = {1, 2, 3, 4};\nCHECK_EQ(sum_evens(a, 4), 6);", "2 + 4."),
                ("none even", "int a[] = {1, 3};\nCHECK_EQ(sum_evens(a, 2), 0);", "No evens: 0."),
                ("negative evens", "int a[] = {-2, 4};\nCHECK_EQ(sum_evens(a, 2), 2);", "-2 + 4."),
            ],
            level="guided",
        ),
    ],
    {
        "cb19-fix-assign-cond": vi_challenge(
            "Sửa: = vs ==",
            "`is_full(int used, int cap)` dưới đây LUÔN trả 1 — điều kiện gán thay vì so sánh. Sửa để nó trả 1 đúng khi used == cap.",
            [("đầy", "Bằng nhau tính là đầy."), ("chưa đầy", "Ít hơn cap thì chưa đầy."), ("rỗng", "Rỗng không phải đầy.")],
        ),
        "cb19-fix-format": vi_challenge(
            "Sửa: Định dạng sai kiểu",
            "Cài `void format_price(double p, char *out)` ghi `price=<giá trị>` vào out bằng snprintf, với <giá trị> dùng định dạng %g của printf cho double. Lỗi kinh điển là %d với double — bản của bạn phải đúng.",
            [("cơ bản", "snprintf(out, 32, \"price=%g\", p)."), ("giá trị nguyên", "%g bỏ phần .0 cuối."), ("dài hơn", "Giá trị lớn hơn cũng vậy.")],
        ),
        "cb19-fix-missing-return": vi_challenge(
            "Sửa: Thiếu đường trả về",
            "`sign_of(int x)` rơi khỏi hàm khi x > 0 — hành vi không xác định. Sửa để trả -1, 0, 1 cho âm, không, dương.",
            [("âm", "Nhánh âm."), ("không", "Nhánh không."), ("dương", "Nhánh bị thiếu: trả 1.")],
        ),
        "cb19-fix-uninit": vi_challenge(
            "Sửa: Bộ cộng chưa khởi tạo",
            "`sum_evens(const int *a, int n)` đọc `total` trước khi khởi tạo. Sửa hàm để trả tổng các phần tử chẵn.",
            [("hỗn hợp", "2 + 4."), ("không chẵn nào", "Không có số chẵn: 0."), ("số chẵn âm", "-2 + 4.")],
        ),
    },
    solutions=[
        (
            "cb19-fix-assign-cond",
            '#include <stdio.h>\nint is_full(int used, int cap) {\n    int r;\n    if (used == cap) r = 1; else r = 0;\n    return r;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint is_full(int used, int cap) {\n    int r;\n    if (used = cap) r = 1; else r = 0;\n    return r;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb19-fix-format",
            '#include <stdio.h>\nvoid format_price(double p, char *out) {\n    snprintf(out, 32, "price=%g", p);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid format_price(double p, char *out) {\n    snprintf(out, 32, "price=%d", p);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb19-fix-missing-return",
            '#include <stdio.h>\nint sign_of(int x) {\n    if (x < 0) return -1;\n    if (x == 0) return 0;\n    return 1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint sign_of(int x) {\n    if (x < 0) return -1;\n    if (x == 0) return 0;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb19-fix-uninit",
            '#include <stdio.h>\nint sum_evens(const int *a, int n) {\n    int total = 0;\n    for (int i = 0; i < n; i++)\n        if (a[i] % 2 == 0) total += a[i];\n    return total;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint sum_evens(const int *a, int n) {\n    int total;\n    for (int i = 0; i < n; i++)\n        if (a[i] % 2 == 0) total += a[i];\n    return total;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M19,
    "cb-p19-crash",
    "Crash Forensics",
    "Off-by-one hunts, guard-clause repairs, and termination fixes.",
    "Pháp y crash",
    "Săn lỗi lệch-một, vá mệnh đề bảo vệ, và sửa điều kiện dừng.",
    L19C,
 16,
    "beginner",
    [
        challenge(
            "cb19-fix-off-by-one",
            "Fix: Off-by-One",
            "`copy_all(int *dst, const int *src, int n)` writes one element PAST the end. Fix the loop bound (the tests place a sentinel after the array and check it survives).\n\n```c\nvoid copy_all(int *dst, const int *src, int n) {\n    for (int i = 0; i <= n; i++)\n        dst[i] = src[i];\n}\n```",
            C_PRELUDE,
            [
                ("content correct", "int s[] = {1, 2, 3};\nint d[3] = {0};\ncopy_all(d, s, 3);\nCHECK_EQ(d[0], 1);\nCHECK_EQ(d[2], 3);", "All three copied."),
                ("sentinel intact", "int s[] = {1, 2};\nint d[3];\nd[2] = 777;\ncopy_all(d, s, 2);\nCHECK_EQ(d[2], 777);", "Element n must NOT be touched."),
            ],
            level="guided",
        ),
        challenge(
            "cb19-fix-div-null",
            "Fix: Unguarded Input",
            "`safe_div(int a, int b)` crashes on b == 0 (and on a NULL result slot). Fix it to return 1 and write the quotient on success, or 0 and leave *out untouched when b == 0 or out == NULL.\n\n```c\nint safe_div(int a, int b, int *out) {\n    *out = a / b;\n    return 1;\n}\n```",
            C_PRELUDE,
            [
                ("success", "int q;\nCHECK_EQ(safe_div(10, 2, &q), 1);\nCHECK_EQ(q, 5);", "Normal path."),
                ("zero divisor", "int q = -1;\nCHECK_EQ(safe_div(10, 0, &q), 0);\nCHECK_EQ(q, -1);", "Rejected AND *out untouched."),
                ("null out", "CHECK_EQ(safe_div(10, 2, NULL), 0);", "NULL out must not crash."),
            ],
            level="independent",
        ),
        challenge(
            "cb19-fix-hang",
            "Fix: Infinite Loop",
            "`count_down(int n)` never terminates for n <= 0 and the loop's counter never reaches its bound for n = 5 (it stops early only by luck of the bug). Fix it to return the number of steps counting n, n-1, ..., 1 (so count_down(5) is 5; count_down(0) is 0).\n\n```c\nint count_down(int n) {\n    int steps = 0;\n    while (n != 1) {\n        steps++;\n        n = n - 0;   /* BUG */\n    }\n    return steps;\n}\n```",
            C_PRELUDE,
            [
                ("five", "CHECK_EQ(count_down(5), 5);", "5,4,3,2,1: five steps."),
                ("one", "CHECK_EQ(count_down(1), 1);", "Just 1: one step."),
                ("zero", "CHECK_EQ(count_down(0), 0);", "Nothing to count."),
            ],
            level="independent",
        ),
    ],
    {
        "cb19-fix-off-by-one": vi_challenge(
            "Sửa: Lệch một",
            "`copy_all(int *dst, const int *src, int n)` ghi một phần tử VƯỢT QUÁ biên. Sửa biên vòng lặp (test đặt một mốc sau mảng và kiểm tra nó còn nguyên).",
            [("nội dung đúng", "Cả ba phần tử được chép."), ("mốc còn nguyên", "Phần tử thứ n KHÔNG được đụng tới.")],
        ),
        "cb19-fix-div-null": vi_challenge(
            "Sửa: Đầu vào không được bảo vệ",
            "`safe_div(int a, int b)` crash khi b == 0 (và khi ô kết quả là NULL). Sửa để trả 1 và ghi thương khi thành công, hoặc trả 0 và giữ *out nguyên vẹn khi b == 0 hoặc out == NULL.",
            [("thành công", "Đường thường."), ("chia cho 0", "Bị từ chối VÀ *out giữ nguyên."), ("out NULL", "NULL out không được phép crash.")],
        ),
        "cb19-fix-hang": vi_challenge(
            "Sửa: Vòng lặp vô hạn",
            "`count_down(int n)` không bao giờ dừng với n <= 0 và bộ đếm không bao giờ chạm giới hạn. Sửa để trả số bước đếm n, n-1, ..., 1 (count_down(5) là 5; count_down(0) là 0).",
            [("năm", "5,4,3,2,1: năm bước."), ("một", "Chỉ 1: một bước."), ("không", "Không có gì để đếm.")],
        ),
    },
    solutions=[
        (
            "cb19-fix-off-by-one",
            '#include <stdio.h>\nvoid copy_all(int *dst, const int *src, int n) {\n    for (int i = 0; i < n; i++)\n        dst[i] = src[i];\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid copy_all(int *dst, const int *src, int n) {\n    for (int i = 0; i <= n; i++)\n        dst[i] = src[i];\n}\nint main(void) { return 0; }',
        ),
        (
            "cb19-fix-div-null",
            '#include <stdio.h>\nint safe_div(int a, int b, int *out) {\n    if (out == NULL || b == 0) return 0;\n    *out = a / b;\n    return 1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint safe_div(int a, int b, int *out) {\n    *out = a / b;\n    return 1;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb19-fix-hang",
            '#include <stdio.h>\nint count_down(int n) {\n    if (n <= 0) return 0;\n    int steps = 0;\n    while (n >= 1) {\n        steps++;\n        n = n - 1;\n    }\n    return steps;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint count_down(int n) {\n    if (n <= 0) return 0;\n    int steps = 0;\n    while (n >= 1) {\n        steps++;\n        n = n - 2;\n    }\n    return steps;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M19,
    L19D,
    "Checkpoint: Debugging",
    "Repair a three-bug report pipeline under a strict warning build.",
    16,
    r"""
## Checkpoint

Warnings confess, tests convict. Use both.
""",
    "Điểm kiểm tra: Gỡ lỗi",
    "Vá một đường ống báo cáo có ba lỗi dưới build warning nghiêm ngặt.",
    r"""
## Điểm kiểm tra

Warning tự thú, test kết tội. Dùng cả hai.
""",
    challenge(
        "cb19-checkpoint-pipeline",
        "Report Pipeline Repair",
        "Fix all three defects in the pipeline below: (1) `avg` must not use integer division, (2) `max_of` must handle n == 1 correctly (start from a[0]), (3) `report(const int *a, int n, char *out)` must write `n=<n> avg=<g> max=<g>` into out with snprintf (%g for the doubles). Reference: report({2, 4}, 2, buf) makes buf `n=2 avg=3 max=4`.\n\n```c\ndouble avg(const int *a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return s / n;          /* BUG: integer division */\n}\nint max_of(const int *a, int n) {\n    int m;\n    for (int i = 1; i < n; i++)\n        if (a[i] > m) m = a[i];   /* BUG: m uninitialized */\n    return m;\n}\nvoid report(const int *a, int n, char *out) {\n    printf(\"n=%d avg=%g max=%g\\n\", n, avg(a, n), (double)max_of(a, n));  /* BUG: prints, ignores out */\n}\n```",
        C_PRELUDE,
        [
            ("avg double", "int a[] = {1, 2};\nCHECK_NEAR(avg(a, 2), 1.5, 1e-9);", "(double)s / n."),
            ("max single", "int a[] = {7};\nCHECK_EQ(max_of(a, 1), 7);", "Start m at a[0]."),
            ("report format", "int a[] = {2, 4};\nchar buf[64] = {0};\nreport(a, 2, buf);\nCHECK_STR_EQ(buf, \"n=2 avg=3 max=4\");", "snprintf(out, 64, \"n=%d avg=%g max=%g\", n, avg(a, n), (double)max_of(a, n))."),
        ],
    ),
    vi_challenge(
        "Vá đường ống báo cáo",
        "Sửa cả ba lỗi trong đường ống dưới đây: (1) `avg` không được dùng chia số nguyên, (2) `max_of` phải xử lý đúng n == 1 (bắt đầu từ a[0]), (3) `report(const int *a, int n, char *out)` phải ghi `n=<n> avg=<g> max=<g>` vào out bằng snprintf (%g cho các double). Tham chiếu: report({2, 4}, 2, buf) làm buf thành `n=2 avg=3 max=4`.",
        [("avg kiểu double", "(double)s / n."), ("max một phần tử", "Bắt đầu m từ a[0]."), ("định dạng report", "snprintf với n=%d avg=%g max=%g.")],
    ),
    solution='#include <stdio.h>\ndouble avg(const int *a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return (double)s / n;\n}\nint max_of(const int *a, int n) {\n    int m = a[0];\n    for (int i = 1; i < n; i++)\n        if (a[i] > m) m = a[i];\n    return m;\n}\nvoid report(const int *a, int n, char *out) {\n    snprintf(out, 64, "n=%d avg=%g max=%g", n, avg(a, n), (double)max_of(a, n));\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\ndouble avg(const int *a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return s / n;\n}\nint max_of(const int *a, int n) {\n    int m = a[0];\n    for (int i = 1; i < n; i++)\n        if (a[i] > m) m = a[i];\n    return m;\n}\nvoid report(const int *a, int n, char *out) {\n    snprintf(out, 64, "n=%d avg=%g max=%g", n, avg(a, n), (double)max_of(a, n));\n}\nint main(void) { return 0; }',
)

print("batch 9 done: modules 18-19")
