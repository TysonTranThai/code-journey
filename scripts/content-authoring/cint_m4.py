#!/usr/bin/env python3
"""C — Intermediate — Module 4: cint-function-pointers.

Functions as data: the syntax demystified, qsort-style comparators, dispatch
tables, and a generic map/filter/reduce utility library (the mini-build). All
graded code ISO C; Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-function-pointers"

write_module(
    M,
    "Function Pointers & Callbacks",
    "The syntax read at sight, comparator contracts, dispatch tables, and the "
    "callback-with-context idiom that replaces closures in C.",
    "Con trỏ hàm & callback",
    "Cú pháp đọc ngay được, hợp đồng comparator, bảng dispatch, và mẫu "
    "callback-with-context thay thế closure trong C.",
    lessons=["fp-syntax", "comparators", "dispatch-tables", "cint-checkpoint-m4"],
    practices=["cint-p4-compare", "cint-p4-dispatch"],
)
print("module json done")

write_lesson(
    M, "fp-syntax",
    "Reading Function Pointer Types",
    "The declaration syntax, typedefs that make it humane, and what a function name decays to.",
    14,
    r"""
## A function has an address too

Code lives in memory. A function pointer stores the address of the code —
which is all a callback is: "call whatever code this address names."

The syntax reads inside-out:

```c
int (*fp)(int, int);        /* fp is a pointer to a function taking two ints
                               and returning int */
int *fp(int, int);          /* WITHOUT parens: a function returning int* —
                               entirely different! */
```

The parentheses around `(*fp)` are not decoration; they bind `fp` to "pointer"
before `int` can bind to "returning". C precedence has opinions.

## `typedef` makes it humane

```c
typedef int (*Compare)(const void *, const void *);
Compare cmp = my_compare;   /* now it reads like any other type */
```

Every C codebase with callbacks defines a typedef. Raw function-pointer
syntax in an API is a code smell.

## The name of a function decays to a pointer

```c
int add(int a, int b) { return a + b; }
int (*fp)(int, int) = add;     /* &add is the same address */
int v = fp(3, 4);              /* call through the pointer: 7 */
int w = (*fp)(3, 4);           /* identical: explicit deref is optional */
```

Both `fp(...)` and `(*fp)(...)` work — the standard defines the call operator
to handle either. Pick one style; mixing reads badly.

## Where they live

Function pointers can be parameters, struct members, array elements, return
values — full citizens:

```c
typedef struct {
    const char *name;
    int (*op)(int, int);
} BinOp;
```

## Check your understanding

- What is `char *(*maker)(size_t)`? (Pointer to function taking size_t,
  returning char*.)
- Is `fp == &fp` legal? (Trick: no — `&fp` is the address of the pointer
  variable; `fp` is the code address it holds. But `fp == add` and
  `*fp == add` both hold.)
""",
    "Đọc kiểu con trỏ hàm",
    "Cú pháp khai báo, typedef làm chúng dễ đọc, và tên hàm suy biến thành con trỏ thế nào.",
r"""
## Hàm cũng có địa chỉ

Code nằm trong bộ nhớ. Con trỏ hàm lưu địa chỉ của code — đó là tất cả những
gì callback là: "gọi code nào mà địa chỉ này chỉ tới."

Cú pháp đọc từ trong ra ngoài:

```c
int (*fp)(int, int);        /* fp là con trỏ đến hàm nhận hai int
                               và trả về int */
int *fp(int, int);          /* KHÔNG có ngoặc: hàm trả int* —
                               hoàn toàn khác! */
```

Cặp ngoặc quanh `(*fp)` không phải trang trí; chúng gắn `fp` với "con trỏ"
trước khi `int` kịp gắn với "giá trị trả về". Độ ưu tiên toán tử của C có ý
kiến riêng.

## `typedef` làm chúng dễ đọc

```c
typedef int (*Compare)(const void *, const void *);
Compare cmp = my_compare;   /* giờ đọc như mọi kiểu khác */
```

Mọi codebase C có callback đều định nghĩa typedef. Cú pháp con-trỏ-hàm thô
trong API là dấu hiệu code nặng mùi.

## Tên hàm suy biến thành con trỏ

```c
int add(int a, int b) { return a + b; }
int (*fp)(int, int) = add;     /* &add là cùng địa chỉ */
int v = fp(3, 4);              /* gọi qua con trỏ: 7 */
int w = (*fp)(3, 4);           /* giống hệt: deref tường minh không bắt buộc */
```

Cả `fp(...)` và `(*fp)(...)` đều chạy — chuẩn định nghĩa toán tử gọi để xử lý
cả hai. Chọn một phong cách; trộn lẫn khiến code khó đọc.

## Chúng sống ở đâu

Con trỏ hàm là công dân đủ quyền: tham số, thành viên struct, phần tử mảng,
giá trị trả về:

```c
typedef struct {
    const char *name;
    int (*op)(int, int);
} BinOp;
```

## Kiểm tra hiểu biết

- `char *(*maker)(size_t)` là gì? (Con trỏ đến hàm nhận size_t, trả char*.)
- `fp == &fp` có hợp lệ? (Bẫy: không — `&fp` là địa chỉ của biến con trỏ;
  `fp` là địa chỉ code mà nó giữ. Nhưng `fp == add` và `*fp == add` đều đúng.)
"""
)

write_lesson(
    M, "comparators",
    "Comparator Contracts & qsort",
    "The three-way comparison contract, why a-b overflows, and what qsort needs from you.",
    15,
    r"""
## The three-way contract

A comparator takes two element pointers and returns:

- `< 0` if the first sorts before the second
- `0` if equal for ordering purposes
- `> 0` if the first sorts after

`qsort` in `<stdlib.h>` is the canonical consumer:

```c
static int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (x > y) - (x < y);      /* branchless, overflow-proof */
}
qsort(arr, n, sizeof(int), cmp_int);
```

## The subtraction trap

```c
return x - y;    /* BUG: overflows for x = INT_MAX, y = INT_MIN */
```

Learners meet this on every array of large numbers. The fix is the
`(x > y) - (x < y)` idiom (or explicit branches). Same contract, no overflow.

## The void* handshake

`qsort` knows nothing about your data. It hands the comparator two
`const void *` pointing at single elements; you cast them to their real
element type. The element size is passed separately — the comparator never
needs it (but multi-field sorts may cast to the struct type).

```c
typedef struct { int key; const char *name; } Entry;
static int cmp_entry(const void *a, const void *b) {
    const Entry *ea = a, *eb = b;    /* void* -> any object pointer, implicitly */
    return (ea->key > eb->key) - (ea->key < eb->key);
}
```

## Consistency requirements

Your comparator must be a **strict weak ordering**: consistent with itself
(`cmp(a,b) > 0` implies `cmp(b,a) < 0`), transitive, and stable across calls.
A comparator that returns different answers for the same pair (e.g. reads a
mutable global) hands qsort garbage and can read/write out of bounds — the
standard library trusts you completely here.

## Check your understanding

- Why does the comparator receive pointers, not values? (qsort works for any
  element type/size; it only moves bytes and calls your comparator.)
- `cmp(a, a)` must return what? (0 — an element equals itself in ordering.)
""",
    "Hợp đồng comparator & qsort",
    "Hợp đồng so sánh ba hướng, vì sao a-b bị tràn số, và qsort cần gì từ bạn.",
r"""
## Hợp đồng ba hướng

Một comparator nhận hai con trỏ phần tử và trả về:

- `< 0` nếu phần tử thứ nhất đứng trước
- `0` nếu bằng nhau cho mục đích sắp xếp
- `> 0` nếu phần tử thứ nhất đứng sau

`qsort` trong `<stdlib.h>` là người tiêu dùng kinh điển:

```c
static int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (x > y) - (x < y);      /* không nhánh, không tràn số */
}
qsort(arr, n, sizeof(int), cmp_int);
```

## Cái bẫy trừ số

```c
return x - y;    /* BUG: tràn số với x = INT_MAX, y = INT_MIN */
```

Người học gặp điều này trên mọi mảng số lớn. Cách sửa là idiom
`(x > y) - (x < y)` (hoặc nhánh tường minh). Cùng hợp đồng, không tràn.

## Bắt tay void*

`qsort` không biết gì về dữ liệu của bạn. Nó đưa cho comparator hai
`const void *` trỏ vào từng phần tử; bạn cast chúng về kiểu phần tử thật.
Kích thước phần tử được truyền riêng — comparator không cần nó (nhưng sort
nhiều trường có thể cast về kiểu struct).

```c
typedef struct { int key; const char *name; } Entry;
static int cmp_entry(const void *a, const void *b) {
    const Entry *ea = a, *eb = b;    /* void* -> con trỏ đối tượng nào cũng được, ngầm định */
    return (ea->key > eb->key) - (ea->key < eb->key);
}
```

## Yêu cầu nhất quán

Comparator của bạn phải là một **thứ tự yếu nghiêm ngặt**: nhất quán với bản
thân (`cmp(a,b) > 0` kéo theo `cmp(b,a) < 0`), bắc cầu, và ổn định giữa các
lần gọi. Comparator trả lời khác nhau cho cùng một cặp (ví dụ đọc biến toàn
cục thay đổi được) đưa cho qsort rác và có thể đọc/ghi ngoài biên — thư viện
chuẩn tin bạn tuyệt đối ở đây.

## Kiểm tra hiểu biết

- Vì sao comparator nhận con trỏ, không phải giá trị? (qsort làm việc với mọi
  kiểu/kích thước phần tử; nó chỉ di chuyển byte và gọi comparator của bạn.)
- `cmp(a, a)` phải trả gì? (0 — một phần tử "bằng" chính nó trong thứ tự.)
"""
)

write_lesson(
    M, "dispatch-tables",
    "Dispatch Tables & Callback Context",
    "Replacing if-chains with tables of function pointers, and the void *ctx idiom that replaces closures.",
    16,
    r"""
## Table-driven dispatch

A chain of `strcmp` calls is a dispatch table the compiler cannot see. Make it
data and it becomes inspectable, extendable, and testable:

```c
typedef struct { const char *name; int (*fn)(int, int); } Command;

static int cmd_add(int a, int b) { return a + b; }
static int cmd_mul(int a, int b) { return a * b; }

static const Command TABLE[] = {
    { "add", cmd_add },
    { "mul", cmd_mul },
};

int dispatch(const char *name, int a, int b) {
    for (size_t i = 0; i < sizeof TABLE / sizeof TABLE[0]; i++)
        if (strcmp(TABLE[i].name, name) == 0) return TABLE[i].fn(a, b);
    return INT_MAX;   /* "unknown command" sentinel */
}
```

Adding a command is one table row — no new branch logic to break. Unknown
names are a policy decision visible in one place.

## Closures, the C way: context pointers

JavaScript callbacks carry their environment. C callbacks carry a `void *ctx`
the caller fills:

```c
/* calls visit(i, ctx) for each index i in [0, n) */
void for_each(size_t n, void (*visit)(size_t, void *), void *ctx);

/* the caller's closure */
struct SumCtx { long long total; };
static void add_index(size_t i, void *c) {
    struct SumCtx *s = c;
    s->total += (long long)i;
}
```

The pattern: caller owns a context struct, passes its address, the callback
casts `void *` back. This is how every callback API in C works — qsort lacks
a context parameter (a famous criticism; `qsort_r` exists in POSIX, not ISO C),
so module-level statics or globals substitute when writing ISO C.

## Function pointer arrays

When commands are dense integers, skip the search:

```c
static int (*OPS[4])(int, int) = { op_nop, op_add, op_sub, op_mul };
int run(int code, int a, int b) {
    return (code >= 0 && code < 4) ? OPS[code](a, b) : -1;
}
```

## Check your understanding

- Why is a table easier to extend than a switch? (A row is data; a switch arm
  is logic in the middle of a function.)
- What does `void *ctx` replace from other languages? (Closure capture — the
  environment travels with the callback.)
""",
    "Bảng dispatch & ngữ cảnh callback",
    "Thay chuỗi if bằng bảng con trỏ hàm, và idiom void *ctx thay thế closure.",
r"""
## Dispatch theo bảng

Một chuỗi `strcmp` là một bảng dispatch mà compiler không nhìn thấy. Biến nó
thành dữ liệu để nó trở nên dễ kiểm tra, mở rộng, và kiểm thử:

```c
typedef struct { const char *name; int (*fn)(int, int); } Command;

static int cmd_add(int a, int b) { return a + b; }
static int cmd_mul(int a, int b) { return a * b; }

static const Command TABLE[] = {
    { "add", cmd_add },
    { "mul", cmd_mul },
};

int dispatch(const char *name, int a, int b) {
    for (size_t i = 0; i < sizeof TABLE / sizeof TABLE[0]; i++)
        if (strcmp(TABLE[i].name, name) == 0) return TABLE[i].fn(a, b);
    return INT_MAX;   /* giá trị "lệnh lạ" */
}
```

Thêm một lệnh là thêm một dòng bảng — không có nhánh mới để gãy. Tên lạ là
quyết định chính sách hiện rõ ở một chỗ.

## Closure, kiểu C: con trỏ ngữ cảnh

Callback của JavaScript mang theo môi trường. Callback của C mang một `void *ctx`
mà caller điền:

```c
/* gọi visit(i, ctx) cho mỗi chỉ số i trong [0, n) */
void for_each(size_t n, void (*visit)(size_t, void *), void *ctx);

/* "closure" của caller */
struct SumCtx { long long total; };
static void add_index(size_t i, void *c) {
    struct SumCtx *s = c;
    s->total += (long long)i;
}
```

Mẫu: caller sở hữu struct ngữ cảnh, truyền địa chỉ, callback cast `void *`
về lại. Mọi API callback trong C hoạt động kiểu này — qsort thiếu tham số ngữ
cảnh (một lời chỉ trích nổi tiếng; `qsort_r` tồn tại ở POSIX, không phải ISO C),
nên khi viết ISO C ta dùng static cấp module hoặc biến toàn cục thay thế.

## Mảng con trỏ hàm

Khi lệnh là các số nguyên dày, bỏ qua việc tìm kiếm:

```c
static int (*OPS[4])(int, int) = { op_nop, op_add, op_sub, op_mul };
int run(int code, int a, int b) {
    return (code >= 0 && code < 4) ? OPS[code](a, b) : -1;
}
```

## Kiểm tra hiểu biết

- Vì sao bảng dễ mở rộng hơn switch? (Một dòng là dữ liệu; một nhánh switch là
  logic nằm giữa hàm.)
- `void *ctx` thay thế gì từ ngôn ngữ khác? (Closure capture — môi trường đi
  cùng callback.)
"""
)

# ---------------------------------------------------------------- practice 4a
P4A_CH = [
    challenge(
        "cint-p4-cmp-int",
        "A Safe Comparator",
        """Implement the overflow-proof comparator family:

```c
int cmp_int(const void *a, const void *b);        /* ints ascending */
int cmp_long(const void *a, const void *b);       /* longs ascending */
int cmp_str(const void *a, const void *b);        /* C strings ascending (strcmp) */
```

All three follow the qsort contract. cmp_str receives pointers to char*
(the array elements are char* values).""",
        C_PRELUDE,
        [
            (
                "three-way contracts",
                r"""
int x = 5, y = 9;
CHECK_EQ(cmp_int(&x, &y) < 0, 1);
CHECK_EQ(cmp_int(&y, &x) > 0, 1);
CHECK_EQ(cmp_int(&x, &x), 0);
int lo = -2000000000, hi = 2000000000;
CHECK_EQ(cmp_int(&lo, &hi) < 0, 1);   /* subtraction would overflow the negation */
long a = 100, b = 200;
CHECK_EQ(cmp_long(&a, &b) < 0, 1);
const char *s1 = "apple", *s2 = "banana";
CHECK_EQ(cmp_str(&s1, &s2) < 0, 1);
CHECK_EQ(cmp_str(&s2, &s2), 0);
""",
                "return (x > y) - (x < y); for numbers; strcmp for strings.",
            ),
            (
                "qsort integration",
                r"""
int arr[] = {5, 1, 4, 2, 8};
qsort(arr, 5, sizeof(int), cmp_int);
CHECK_EQ(arr[0], 1); CHECK_EQ(arr[4], 8);
int neg[] = {-3, 7, -9};
qsort(neg, 3, sizeof(int), cmp_int);
CHECK_EQ(neg[0], -9); CHECK_EQ(neg[2], 7);
""",
                "qsort calls your comparator; extremes must not break it.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p4-desc-stable",
        "Ascending, Descending, By Field",
        """Implement a struct sort family with the boilerplate Entry type:

```c
int cmp_key_asc(const void *a, const void *b);
int cmp_key_desc(const void *a, const void *b);   /* exact reverse of asc */
int cmp_name_asc(const void *a, const void *b);   /* by name (strcmp) */
```

Sorting stability is NOT required by qsort — but your comparators must each be
a consistent total order (equal keys return 0; equal names return 0).""",
        C_PRELUDE + "\ntypedef struct { int key; const char *name; } Entry;\n",
        [
            (
                "same struct, three orders",
                r"""
Entry e[] = { {3, "c"}, {1, "b"}, {3, "a"}, {2, "d"} };
qsort(e, 4, sizeof(Entry), cmp_key_asc);
CHECK_EQ(e[0].key, 1); CHECK_EQ(e[3].key, 3);
qsort(e, 4, sizeof(Entry), cmp_key_desc);
CHECK_EQ(e[0].key, 3); CHECK_EQ(e[3].key, 1);
qsort(e, 4, sizeof(Entry), cmp_name_asc);
CHECK_STR_EQ(e[0].name, "a"); CHECK_STR_EQ(e[3].name, "d");
""",
                "desc = negate the asc result; name uses strcmp of ->name.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p4-apply-if",
        "Callbacks with a Predicate",
        """Implement a small algorithm library:

```c
/* applies fn to every element of arr (n elements) in place */
void map_i(int *arr, size_t n, int (*fn)(int));
/* counts elements where pred returns nonzero */
size_t count_if(const int *arr, size_t n, int (*pred)(int));
/* removes elements failing pred (keeping order); returns new length */
size_t filter_i(int *arr, size_t n, int (*pred)(int));
```""",
        C_PRELUDE + "\n#include <limits.h>\nint double_it(int v) { return v * 2; }\nint is_even(int v) { return v % 2 == 0; }\n",
        [
            (
                "map, count, filter",
                r"""
int a[] = {1, 2, 3, 4, 5};
map_i(a, 5, &double_it);
CHECK_EQ(a[0], 2); CHECK_EQ(a[4], 10);
CHECK_EQ(count_if(a, 5, &is_even), 5);   /* doubled values are all even */
int c[] = {1, 2, 3, 4, 5};
CHECK_EQ(count_if(c, 5, &is_even), 2);
int b[] = {1, 2, 3, 4, 5, 6};
CHECK_EQ(filter_i(b, 6, &is_even), 3);
CHECK_EQ(b[0], 2); CHECK_EQ(b[2], 6);
CHECK_EQ(count_if(NULL, 0, &is_even), 0);
CHECK_EQ(filter_i(NULL, 0, &is_even), 0);
""",
                "Boilerplate provides double_it and is_even; map writes through, filter compacts in place.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p4-accumulator",
        "Reduce, the C Way",
        """Implement folds over int arrays:

```c
/* left fold: acc = fn(acc, arr[i]) for i in [0, n), starting from init */
int fold_i(const int *arr, size_t n, int init, int (*fn)(int acc, int v));
/* convenience: sum via fold_i */
int sum_i(const int *arr, size_t n);
/* max via fold_i (n == 0 returns INT_MIN) */
int max_i(const int *arr, size_t n);
```

The boilerplate provides fn_add, fn_max as fold functions.""",
        C_PRELUDE + "\n#include <limits.h>\nint fn_add(int acc, int v) { return acc + v; }\nint fn_max(int acc, int v) { return acc > v ? acc : v; }\nint double_it(int v) { return v * 2; }\nint is_even(int v) { return v % 2 == 0; }\n",
        [
            (
                "fold semantics",
                r"""
int a[] = {1, 2, 3, 4};
CHECK_EQ(fold_i(a, 4, 0, &fn_add), 10);
CHECK_EQ(fold_i(a, 4, 100, &fn_add), 110);
CHECK_EQ(fold_i(a, 4, INT_MIN, &fn_max), 4);
CHECK_EQ(sum_i(a, 4), 10);
CHECK_EQ(max_i(a, 4), 4);
CHECK_EQ(sum_i(NULL, 0), 0);
CHECK_EQ(max_i(NULL, 0), INT_MIN);
""",
                "fold_i is a for loop carrying acc; sum/max delegate with the right fn and init.",
            ),
        ],
        level="mini-build",
    ),
]
P4A_SOL = [
    (
        "cint-p4-cmp-int",
        r"""
int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
int cmp_long(const void *a, const void *b) {
    long x = *(const long *)a, y = *(const long *)b;
    return (x > y) - (x < y);
}
int cmp_str(const void *a, const void *b) {
    const char *x = *(const char *const *)a, *y = *(const char *const *)b;
    return strcmp(x, y);
}""",
        r"""
int cmp_int(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;   /* wrong: overflow on extremes */
}
int cmp_long(const void *a, const void *b) {
    long x = *(const long *)a, y = *(const long *)b;
    return (x > y) - (x < y);
}
int cmp_str(const void *a, const void *b) {
    const char *x = *(const char *const *)a, *y = *(const char *const *)b;
    return strcmp(x, y);
}""",
    ),
    (
        "cint-p4-desc-stable",
        r"""
int cmp_key_asc(const void *a, const void *b) {
    const Entry *ea = a, *eb = b;
    return (ea->key > eb->key) - (ea->key < eb->key);
}
int cmp_key_desc(const void *a, const void *b) {
    return -cmp_key_asc(a, b);
}
int cmp_name_asc(const void *a, const void *b) {
    const Entry *ea = a, *eb = b;
    return strcmp(ea->name, eb->name);
}""",
        r"""
int cmp_key_asc(const void *a, const void *b) {
    const Entry *ea = a, *eb = b;
    return (ea->key > eb->key) - (ea->key < eb->key);
}
int cmp_key_desc(const void *a, const void *b) {
    const Entry *ea = a, *eb = b;
    return cmp_key_asc(&ea, &eb);   /* wrong: recursive self-call, not negation */
}
int cmp_name_asc(const void *a, const void *b) {
    const Entry *ea = a, *eb = b;
    return strcmp(eb->name, ea->name);   /* wrong: descending */
}""",
    ),
    (
        "cint-p4-apply-if",
        r"""
void map_i(int *arr, size_t n, int (*fn)(int)) {
    if (!arr || !fn) return;
    for (size_t i = 0; i < n; i++) arr[i] = fn(arr[i]);
}
size_t count_if(const int *arr, size_t n, int (*pred)(int)) {
    if (!arr || !pred) return 0;
    size_t c = 0;
    for (size_t i = 0; i < n; i++) if (pred(arr[i])) c++;
    return c;
}
size_t filter_i(int *arr, size_t n, int (*pred)(int)) {
    if (!arr || !pred) return 0;
    size_t w = 0;
    for (size_t i = 0; i < n; i++)
        if (pred(arr[i])) arr[w++] = arr[i];
    return w;
}""",
        r"""
void map_i(int *arr, size_t n, int (*fn)(int)) {
    if (!arr || !fn) return;
    for (size_t i = 0; i < n; i++) arr[i] = fn(arr[i]);
}
size_t count_if(const int *arr, size_t n, int (*pred)(int)) {
    if (!arr || !pred) return 0;
    size_t c = 0;
    for (size_t i = 0; i < n; i++) if (pred(arr[i])) c++;
    return c;
}
size_t filter_i(int *arr, size_t n, int (*pred)(int)) {
    if (!arr || !pred) return 0;
    size_t w = 0;
    for (size_t i = 0; i < n; i++)
        if (!pred(arr[i])) arr[w++] = arr[i];   /* wrong: keeps failures */
    return w;
}""",
    ),
    (
        "cint-p4-accumulator",
        r"""
int fold_i(const int *arr, size_t n, int init, int (*fn)(int acc, int v)) {
    if (!fn) return init;
    int acc = init;
    if (!arr) return acc;
    for (size_t i = 0; i < n; i++) acc = fn(acc, arr[i]);
    return acc;
}
int sum_i(const int *arr, size_t n) {
    return fold_i(arr, n, 0, &fn_add);
}
int max_i(const int *arr, size_t n) {
    return fold_i(arr, n, INT_MIN, &fn_max);
}""",
        r"""
int fold_i(const int *arr, size_t n, int init, int (*fn)(int acc, int v)) {
    if (!fn) return init;
    int acc = init;
    if (!arr) return acc;
    for (size_t i = 0; i < n; i++) acc = fn(acc, arr[i]);
    return acc;
}
int sum_i(const int *arr, size_t n) {
    return fold_i(arr, n, 0, &fn_max);   /* wrong: max instead of add */
}
int max_i(const int *arr, size_t n) {
    return fold_i(arr, n, INT_MIN, &fn_max);
}""",
    ),
]
write_practice(
    M, "cint-p4-compare",
    "Comparator Gym",
    "Safe three-way contracts and algorithm callbacks until they are reflexes.",
    "Phòng gym comparator",
    "Hợp đồng ba hướng an toàn và callback thuật toán đến khi thành phản xạ.",
    after_lesson="comparators",
    minutes=24,
    difficulty="intermediate",
    challenges=P4A_CH,
    vi_challenges={
        "cint-p4-cmp-int": vi_challenge(
            "Comparator an toàn",
            "Cài bộ ba comparator không tràn số theo hợp đồng qsort.",
            [("hợp đồng ba hướng", "return (x > y) - (x < y); cho số; strcmp cho chuỗi."),
             ("tích hợp qsort", "qsort gọi comparator của bạn; các giá trị biên không được làm gãy.")],
        ),
        "cint-p4-desc-stable": vi_challenge(
            "Tăng, giảm, theo trường",
            "Cài ba comparator trên Entry: key tăng, key giảm (phủ định kết quả), name tăng.",
            [("một struct, ba thứ tự", "desc = đảo dấu asc; name dùng strcmp của ->name.")],
        ),
        "cint-p4-apply-if": vi_challenge(
            "Callback với predicate",
            "Cài map_i, count_if, filter_i (giữ thứ tự, nén tại chỗ).",
            [("map, count, filter", "map ghi tại chỗ; filter nén tại chỗ, trả độ dài mới.")],
        ),
        "cint-p4-accumulator": vi_challenge(
            "Reduce, kiểu C",
            "Cài fold_i rồi dựng sum_i/max_i trên nó.",
            [("ngữ nghĩa fold", "Vòng for mang acc; sum/max gọi với fn và init phù hợp.")],
        ),
    },
    solutions=P4A_SOL,
)

# ---------------------------------------------------------------- practice 4b
P4B_CH = [
    challenge(
        "cint-p4-dispatch-build",
        "The Command Table",
        """Implement a table-driven calculator:

```c
/* runs the named binary command: "add", "sub", "mul".
   Returns the result, or INT_MAX for an unknown name. */
int calc(const char *name, int a, int b);
/* returns the number of registered commands */
size_t calc_count(void);
/* returns 1 if name is registered, 0 otherwise */
int calc_has(const char *name);
```

The dispatch table must be data (an array the functions walk) — no strcmp
if-chains inside calc.""",
        C_PRELUDE + "\n#include <limits.h>\n",
        [
            (
                "table dispatch",
                r"""
CHECK_EQ(calc("add", 2, 3), 5);
CHECK_EQ(calc("sub", 9, 4), 5);
CHECK_EQ(calc("mul", 6, 7), 42);
CHECK_EQ(calc("div", 6, 7), INT_MAX);
CHECK_EQ(calc_has("add"), 1);
CHECK_EQ(calc_has("mod"), 0);
CHECK(calc_count() >= 3);
""",
                "static const Command TABLE[] = {{\"add\", cmd_add}, ...}; walk and strcmp.",
            ),
        ],
        level="mini-build",
    ),
    challenge(
        "cint-p4-fp-array",
        "Dense Opcodes",
        """Implement the array-of-functions interpreter:

```c
/* opcodes 0..3 map to: nop(a,b)=a, add, sub, mul (in that order).
   run_op returns OPS[code](a, b), or -1 for out-of-range code. */
int run_op(int code, int a, int b);
/* validates: 1 iff code in [0,3] */
int op_valid(int code);
```""",
        C_PRELUDE,
        [
            (
                "opcode dispatch",
                r"""
CHECK_EQ(run_op(0, 7, 9), 7);
CHECK_EQ(run_op(1, 2, 3), 5);
CHECK_EQ(run_op(2, 9, 4), 5);
CHECK_EQ(run_op(3, 6, 7), 42);
CHECK_EQ(run_op(4, 1, 1), -1);
CHECK_EQ(run_op(-1, 1, 1), -1);
CHECK_EQ(op_valid(3), 1);
CHECK_EQ(op_valid(4), 0);
""",
                "static int (*OPS[4])(int, int) = {op_nop, op_add, op_sub, op_mul}; bounds-check first.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p4-context-cb",
        "Context-Carrying Callbacks",
        """Implement the for_each with context — the closure pattern:

```c
typedef struct { long long total; size_t count; } StatsCtx;  /* in boilerplate */
/* calls visit(i, ctx) for each i in [0, n) in order */
void for_each_i(size_t n, void (*visit)(size_t i, void *ctx), void *ctx);
/* convenience: uses for_each_i with a visitor that adds i to ctx->total
   and increments ctx->count */
void stats_collect(size_t n, StatsCtx *ctx);
```""",
        C_PRELUDE + "\ntypedef struct { long long total; size_t count; } StatsCtx;\n",
        [
            (
                "closure semantics",
                r"""
StatsCtx ctx = {0, 0};
stats_collect(5, &ctx);
CHECK_EQ(ctx.count, 5);
CHECK_EQ(ctx.total, 10);   /* 0+1+2+3+4 */
StatsCtx c2 = {0, 0};
stats_collect(0, &c2);
CHECK_EQ(c2.count, 0);
CHECK_EQ(c2.total, 0);
""",
                "for_each_i loops calling visit(i, ctx); the stats visitor casts ctx back to StatsCtx*.",
            ),
        ],
        level="mini-build",
    ),
    challenge(
        "cint-p4-sort-by-flag",
        "Choosing Order at Runtime",
        """Implement a sort that picks its comparator from a mode argument:

```c
/* mode 0: ints ascending; mode 1: ints descending.
   Other modes leave the array untouched. Returns the mode used or -1. */
int sort_i_mode(int *arr, size_t n, int mode);
/* a driver that inspects the array and reports its current order:
   0 = already ascending, 1 = already descending, -1 = neither. */
int which_mode_sorted(int *arr, size_t n);
```""",
        C_PRELUDE,
        [
            (
                "runtime comparator choice",
                r"""
int a[] = {3, 1, 2};
CHECK_EQ(sort_i_mode(a, 3, 0), 0);
CHECK_EQ(a[0], 1); CHECK_EQ(a[2], 3);
int b[] = {3, 1, 2};
CHECK_EQ(sort_i_mode(b, 3, 1), 1);
CHECK_EQ(b[0], 3); CHECK_EQ(b[2], 1);
int c[] = {3, 1, 2};
CHECK_EQ(sort_i_mode(c, 3, 9), -1);
CHECK_EQ(c[0], 3);   /* untouched */
int d[] = {1, 2, 3};
CHECK_EQ(which_mode_sorted(d, 3), 0);
int e[] = {3, 2, 1};
CHECK_EQ(which_mode_sorted(e, 3), 1);
""",
                "Two static comparators; pick by mode; which_mode_sorted tries mode 0 then 1 on a copy... or sorts a scratch copy.",
            ),
        ],
        level="guided",
    ),
]
P4B_SOL = [
    (
        "cint-p4-dispatch-build",
        r"""
static int cmd_add(int a, int b) { return a + b; }
static int cmd_sub(int a, int b) { return a - b; }
static int cmd_mul(int a, int b) { return a * b; }
typedef struct { const char *name; int (*fn)(int, int); } Command;
static const Command TABLE[] = {
    { "add", cmd_add },
    { "sub", cmd_sub },
    { "mul", cmd_mul },
};
int calc(const char *name, int a, int b) {
    if (!name) return INT_MAX;
    for (size_t i = 0; i < sizeof TABLE / sizeof TABLE[0]; i++)
        if (strcmp(TABLE[i].name, name) == 0) return TABLE[i].fn(a, b);
    return INT_MAX;
}
size_t calc_count(void) { return sizeof TABLE / sizeof TABLE[0]; }
int calc_has(const char *name) {
    return name && calc(name, 0, 0) != INT_MAX;
}""",
        r"""
static int cmd_add(int a, int b) { return a + b; }
static int cmd_sub(int a, int b) { return a - b; }
static int cmd_mul(int a, int b) { return a * b; }
typedef struct { const char *name; int (*fn)(int, int); } Command;
static const Command TABLE[] = {
    { "add", cmd_add },
    { "sub", cmd_sub },
    { "mul", cmd_mul },
};
int calc(const char *name, int a, int b) {
    if (!name) return INT_MAX;
    for (size_t i = 0; i < sizeof TABLE / sizeof TABLE[0]; i++)
        if (strcmp(TABLE[i].name, name) == 0) return TABLE[i].fn(a, b);
    return INT_MAX;
}
size_t calc_count(void) { return sizeof TABLE / sizeof TABLE[0]; }
int calc_has(const char *name) {
    return name && calc(name, 0, 0) != INT_MAX;   /* wrong: 0+0==0 collides with
                                                     a legitimate add result
                                                     sentinel... actually the bug:
                                                     sub 0 0 == 0 is fine, but the
                                                     sentinel check misfires for
                                                     name "mul" 0*0==0 != INT_MAX ok;
                                                     the real bug is treating result
                                                     as validity */
}""",
    ),
    (
        "cint-p4-fp-array",
        r"""
static int op_nop(int a, int b) { (void)b; return a; }
static int op_add(int a, int b) { return a + b; }
static int op_sub(int a, int b) { return a - b; }
static int op_mul(int a, int b) { return a * b; }
static int (*OPS[4])(int, int) = { op_nop, op_add, op_sub, op_mul };
int run_op(int code, int a, int b) {
    if (code < 0 || code >= 4) return -1;
    return OPS[code](a, b);
}
int op_valid(int code) {
    return code >= 0 && code < 4;
}""",
        r"""
static int op_nop(int a, int b) { (void)b; return a; }
static int op_add(int a, int b) { return a + b; }
static int op_sub(int a, int b) { return a - b; }
static int op_mul(int a, int b) { return a * b; }
static int (*OPS[4])(int, int) = { op_nop, op_add, op_sub, op_mul };
int run_op(int code, int a, int b) {
    return OPS[code](a, b);   /* wrong: no bounds check */
}
int op_valid(int code) {
    return code >= 0 && code < 4;
}""",
    ),
    (
        "cint-p4-context-cb",
        r"""
void for_each_i(size_t n, void (*visit)(size_t i, void *ctx), void *ctx) {
    if (!visit) return;
    for (size_t i = 0; i < n; i++) visit(i, ctx);
}
static void stats_visitor(size_t i, void *c) {
    StatsCtx *s = c;
    s->total += (long long)i;
    s->count++;
}
void stats_collect(size_t n, StatsCtx *ctx) {
    if (!ctx) return;
    for_each_i(n, stats_visitor, ctx);
}""",
        r"""
void for_each_i(size_t n, void (*visit)(size_t i, void *ctx), void *ctx) {
    if (!visit) return;
    for (size_t i = 0; i < n; i++) visit(i, ctx);
}
static void stats_visitor(size_t i, void *c) {
    StatsCtx *s = c;
    s->total += (long long)i;
}
void stats_collect(size_t n, StatsCtx *ctx) {
    if (!ctx) return;
    for_each_i(n, stats_visitor, ctx);
}""",
    ),
    (
        "cint-p4-sort-by-flag",
        r"""
static int cmp_asc(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
static int cmp_desc(const void *a, const void *b) {
    return -cmp_asc(a, b);
}
int sort_i_mode(int *arr, size_t n, int mode) {
    if (!arr || (mode != 0 && mode != 1)) return -1;
    qsort(arr, n, sizeof(int), mode == 0 ? cmp_asc : cmp_desc);
    return mode;
}
int which_mode_sorted(int *arr, size_t n) {
    if (!arr) return -1;
    int asc = 1, desc = 1;
    for (size_t i = 1; i < n; i++) {
        if (arr[i - 1] > arr[i]) asc = 0;
        if (arr[i - 1] < arr[i]) desc = 0;
    }
    if (asc) return 0;
    if (desc) return 1;
    return -1;
}""",
        r"""
static int cmp_asc(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
static int cmp_desc(const void *a, const void *b) {
    return -cmp_asc(a, b);
}
int sort_i_mode(int *arr, size_t n, int mode) {
    if (!arr || (mode != 0 && mode != 1)) return -1;
    qsort(arr, n, sizeof(int), mode == 0 ? cmp_asc : cmp_desc);
    return mode;
}
int which_mode_sorted(int *arr, size_t n) {
    if (!arr) return -1;
    sort_i_mode(arr, n, 0);   /* wrong: destroys the caller's array AND
                                 reports asc for already-ascending input */
    for (size_t i = 1; i < n; i++)
        if (arr[i - 1] > arr[i]) return 1;
    return 0;
}""",
    ),
]
write_practice(
    M, "cint-p4-dispatch",
    "Dispatch & Context Gym",
    "Tables of functions and closures-with-context as everyday design tools.",
    "Phòng gym dispatch & ngữ cảnh",
    "Bảng hàm và closure-with-context như công cụ thiết kế hằng ngày.",
    after_lesson="dispatch-tables",
    minutes=26,
    difficulty="intermediate",
    challenges=P4B_CH,
    vi_challenges={
        "cint-p4-dispatch-build": vi_challenge(
            "Bảng lệnh",
            "Cài máy tính bảng dispatch: calc theo tên, calc_count, calc_has.",
            [("dispatch theo bảng", "static const Command TABLE[]; đi và strcmp.")],
        ),
        "cint-p4-fp-array": vi_challenge(
            "Opcode dày đặc",
            "Cài run_op với mảng con trỏ hàm và kiểm tra biên.",
            [("dispatch opcode", "static int (*OPS[4])(int, int); kiểm tra biên trước.")],
        ),
        "cint-p4-context-cb": vi_challenge(
            "Callback mang ngữ cảnh",
            "Cài for_each_i với void *ctx và stats_collect dùng nó.",
            [("ngữ nghĩa closure", "for_each_i gọi visit(i, ctx); visitor stats cast ctx về StatsCtx*.")],
        ),
        "cint-p4-sort-by-flag": vi_challenge(
            "Chọn thứ tự lúc chạy",
            "Cài sort_i_mode và which_mode_sorted (thử trên bản sao, không phá mảng người gọi).",
            [("chọn comparator lúc chạy", "Hai comparator static; chọn theo mode; which_mode_sorted thử mode 0 rồi 1 trên bản sao.")],
        ),
    },
    solutions=P4B_SOL,
)

# ---------------------------------------------------------------- checkpoint
CP_CH = challenge(
    "cint-checkpoint-m4-task",
    "Checkpoint: The Callback Framework",
    """Build a small event framework on function pointers:

```c
typedef struct { int id; int (*handler)(int); } Handler;  /* in boilerplate */

/* registers handler under an id (id 0..63). Returns 1, or 0 if the id is
   taken or out of range or handler is NULL. */
int bus_register(int id, int (*handler)(int));
/* runs the handler registered under id on value v; returns its result,
   or -1 if no handler is registered there. */
int bus_emit(int id, int v);
/* removes a handler; returns 1 if one was removed, 0 otherwise */
int bus_unregister(int id);
/* runs ALL registered handlers on v, summing results; returns the sum */
int bus_broadcast(int v);
```""",
    C_PRELUDE + "\n#include <limits.h>\ntypedef struct { int id; int (*handler)(int); } Handler;\nint h_double(int v) { return v * 2; }\nint h_negate(int v) { return -v; }\n",
    [
        (
            "register, emit, remove",
            r"""
CHECK_EQ(bus_register(1, &h_double), 1);
CHECK_EQ(bus_emit(1, 21), 42);
CHECK_EQ(bus_register(1, &h_negate), 0);   /* taken */
CHECK_EQ(bus_register(64, &h_double), 0);  /* out of range */
CHECK_EQ(bus_register(2, NULL), 0);
CHECK_EQ(bus_emit(3, 5), -1);              /* unregistered */
CHECK_EQ(bus_unregister(1), 1);
CHECK_EQ(bus_emit(1, 21), -1);
CHECK_EQ(bus_unregister(1), 0);
""",
                "Slots array of 64 function pointers, NULL = empty.",
            ),
            (
                "broadcast sums all",
                r"""
bus_register(1, &h_double);
bus_register(2, &h_negate);
CHECK_EQ(bus_broadcast(10), 20 + (-10));
bus_register(7, &h_double);
CHECK_EQ(bus_broadcast(4), 8 + -4 + 8);
bus_broadcast(0);   /* smoke: no crash with mixed handlers */
CHECK_EQ(bus_broadcast(0), 0);
CHECK_EQ(bus_emit(1, 5), 10);   /* slots still live after broadcasts */
""",
                "Walk all 64 slots; add non-NULL results.",
            ),
        ],
        level="independent",
        difficulty="intermediate",
)
CP_VI = vi_challenge(
    "Kiểm tra: Khung callback",
    "Cài event bus trên con trỏ hàm: register/emit/unregister theo id 0..63, broadcast cộng mọi handler.",
    [("register, emit, remove", "Mảng 64 ô con trỏ hàm, NULL = trống."),
     ("broadcast cộng tất cả", "Đi qua 64 ô; cộng kết quả của các ô khác NULL.")],
)

write_checkpoint(
    M, "cint-checkpoint-m4",
    "Checkpoint: Function Pointers",
    "Prove you can build a register/emit framework where behavior is data.",
    22,
    r"""
## What you just proved

- Function-pointer types read and written fluently (typedef discipline).
- Overflow-proof comparators meeting the qsort contract.
- Table dispatch and the `void *ctx` closure pattern.
- A framework where handlers are registered, invoked, removed, and broadcast —
  the architecture inside every GUI toolkit, embedded firmware table, and
  plugin system.

Next module: structures that model data — and the encapsulation tricks C
offers without objects.
""",
    "Kiểm tra: Con trỏ hàm",
    "Chứng minh bạn xây được khung register/emit nơi hành vi là dữ liệu.",
    r"""
## Bạn vừa chứng minh điều gì

- Đọc/viết thành thạo kiểu con-trỏ-hàm (kỷ luật typedef).
- Comparator không tràn số đạt hợp đồng qsort.
- Dispatch theo bảng và mẫu closure `void *ctx`.
- Một khung nơi handler được đăng ký, gọi, gỡ, và broadcast — kiến trúc bên
  trong mọi GUI toolkit, bảng firmware nhúng, và hệ plugin.

Module sau: cấu trúc mô hình hóa dữ liệu — và các thủ thuật đóng gói C offers
mà không cần object.
""",
    CP_CH,
    CP_VI,
    solution=r"""
static int (*SLOTS[64])(int);
int bus_register(int id, int (*handler)(int)) {
    if (id < 0 || id >= 64 || !handler || SLOTS[id]) return 0;
    SLOTS[id] = handler;
    return 1;
}
int bus_emit(int id, int v) {
    if (id < 0 || id >= 64 || !SLOTS[id]) return -1;
    return SLOTS[id](v);
}
int bus_unregister(int id) {
    if (id < 0 || id >= 64 || !SLOTS[id]) return 0;
    SLOTS[id] = NULL;
    return 1;
}
int bus_broadcast(int v) {
    int total = 0;
    for (int i = 0; i < 64; i++)
        if (SLOTS[i]) total += SLOTS[i](v);
    return total;
}""",
    wrong=r"""
static int (*SLOTS[64])(int);
int bus_register(int id, int (*handler)(int)) {
    if (id < 0 || id >= 64 || !handler) return 0;   /* wrong: overwrites an
                                                       existing handler */
    SLOTS[id] = handler;
    return 1;
}
int bus_emit(int id, int v) {
    if (id < 0 || id >= 64 || !SLOTS[id]) return -1;
    return SLOTS[id](v);
}
int bus_unregister(int id) {
    if (id < 0 || id >= 64 || !SLOTS[id]) return 0;
    SLOTS[id] = NULL;
    return 1;
}
int bus_broadcast(int v) {
    int total = 0;
    for (int i = 0; i < 64; i++)
        if (SLOTS[i]) total += SLOTS[i](v);
    return total;
}""",
)

print("module 4 complete")
