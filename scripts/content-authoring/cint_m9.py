#!/usr/bin/env python3
"""C — Intermediate — Module 9: cint-generic.

Generic programming in ISO C: void* with byte-size metadata, qsort/bsearch
as the standard generic engine, memcpy-based element moves, _Generic for
compile-time selection, and macro wrappers that restore type safety.
House conventions: ISO C only (C23 _Generic verified in-sandbox),
self-contained tests, Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-generic"

write_module(
    M,
    "Generic Programming in C",
    "void* plus size plus callbacks: the C toolchain for code that works on "
    "any type — and the discipline that keeps it type-safe.",
    "Lập trình generic trong C",
    "void* cộng size cộng callback: bộ công cụ C cho code hoạt động trên "
    "mọi kiểu — và kỷ luật giữ nó type-safe.",
    lessons=["void-bytes", "qsort-bsearch", "generic-selection", "cint-checkpoint-m9"],
    practices=["cint-p9-void", "cint-p9-generic"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "void-bytes",
    "void*, Element Size & memcpy",
    "A generic array is (pointer, count, element_size). Everything else "
    "follows.",
    16,
    r"""
## The universal triple

Every generic array function in C has the same skeleton:

```c
void *my_lsearch(const void *key, const void *base, size_t n,
                 size_t size, int (*cmp)(const void *, const void *));
```

`base` points at element 0, `n` counts elements, `size` is one element's
byte size, `cmp` knows the real type. Inside, element `i` lives at:

```c
const char *p = (const char *)base + i * size;
```

`char*` arithmetic is byte arithmetic — that is the one guaranteed
addressable unit. Two disciplines keep this safe:

**1. Never cast to the wrong type — cast to `char *` and move bytes.**
Copying an element is `memcpy(dst, src, size)`, never a struct or
pointer dereference. `void *` converts to/from any object pointer
*implicitly* in C — no cast needed on either side — but you still cannot
dereference it.

**2. Alignment is inherited, not manufactured.** If `base` really points
at an array of `T`, every `i * size` offset is a valid `T` address. The
caller's types stay aligned because you never invent storage of your
own.

## The swap primitive

Generic algorithms bottom out in byte-wise element swaps:

```c
static void swap_bytes(char *a, char *b, size_t size) {
    while (size--) {
        char t = *a;
        *a++ = *b;
        *b++ = t;
    }
}
```

One byte at a time is slow but universally correct; `memcpy` through a
small stack buffer is the faster classical form. Overlapping elements
would be UB — the caller's contract (distinct element slots) is what
makes the primitive legal.
""",
"void*, kích thước phần tử & memcpy",
    "Mảng generic là (con trỏ, số lượng, kích thước phần tử). Mọi thứ khác "
    "xuất phát từ đó.",
    r"""
## Bộ ba phổ quát

Mỗi hàm generic trên mảng trong C có cùng bộ khung:

```c
void *my_lsearch(const void *key, const void *base, size_t n,
                 size_t size, int (*cmp)(const void *, const void *));
```

`base` trỏ vào phần tử 0, `n` đếm phần tử, `size` là số byte của một
phần tử, `cmp` biết kiểu thật. Bên trong, phần tử `i` nằm tại:

```c
const char *p = (const char *)base + i * size;
```

Phép cộng trên `char*` là phép cộng theo byte — đó là đơn vị địa chỉ
bảo đảm duy nhất. Hai kỷ luật giữ nó an toàn:

**1. Không bao giờ cast sang kiểu sai — cast sang `char *` rồi chuyển
byte.** Copy một phần tử là `memcpy(dst, src, size)`, không bao giờ là
dereference struct hay con trỏ. `void *` đổi qua/lại với con trỏ object
bất kỳ *tự động* trong C — không cần cast về hai phía — nhưng bạn vẫn
không được dereference nó.

**2. Alignment được thừa kế, không tự chế.** Nếu `base` thực sự trỏ vào
mảng `T`, mọi offset `i * size` là địa chỉ `T` hợp lệ. Kiểu của caller
giữ alignment vì bạn không tự tạo kho lưu trữ nào của riêng mình.

## Nguyên thủy swap

Thuật toán generic chạm đáy ở swap theo byte:

```c
static void swap_bytes(char *a, char *b, size_t size) {
    while (size--) {
        char t = *a;
        *a++ = *b;
        *b++ = t;
    }
}
```

Từng byte là chậm nhưng đúng phổ quát; `memcpy` qua buffer nhỏ trên
stack là dạng kinh điển nhanh hơn. Các phần tử chồng lấn sẽ là UB — hợp
đồng của caller (các slot phần tử khác nhau) mới là thứ khiến nguyên thủy
này hợp pháp.
"""
)

write_lesson(
    M, "qsort-bsearch",
    "qsort & bsearch: the Standard Generic Engine",
    "The stdlib's generic sort and search: comparator contracts, stability "
    "caveats, and binary search's precondition.",
    17,
    r"""
## The two functions every C programmer must own

```c
void qsort(void *base, size_t n, size_t size,
           int (*cmp)(const void *, const void *));
void *bsearch(const void *key, const void *base, size_t n, size_t size,
              int (*cmp)(const void *, const void *));
```

Both work on *any* element type through exactly the triple from the last
lesson. The comparator decides everything:

```c
/* int elements: read through const void*, return three-way */
int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);      /* never a - b: INT_MIN overflows it */
}
```

The contract: negative/zero/positive for less/equal/greater. `(x > y) -
(x < y)` is the overflow-proof idiom; `a - b` on ints breaks at the
extremes, and on doubles can round to 0 for distinct values.

## Two honest caveats

**qsort is not stable.** Equal elements may be reordered (the standard
does not promise otherwise; implementations vary). If order among
equals matters, extend the comparator with a tiebreaker key, or sort an
array of (key, original-index) pairs.

**bsearch demands sorted input.** Binary search's O(log n) is rented
from the precondition. Calling bsearch on unsorted data is not "wrong
answer" — it is undefined which element (if any) you find. And
bsearch's contract says *any* matching element when duplicates exist;
if you need first/last, write the lower_bound variant by hand.

## When qsort is the wrong tool

Its generality costs: comparator calls through a function pointer
(defeating inlining), `size`-byte memcpys. Specialized sorts on ints
can be several times faster. qsort is the *default*; specialize when
measurement says so.
""",
"qsort & bsearch: động cơ generic chuẩn",
    "Sort và search generic của stdlib: hợp đồng comparator, lưu ý ổn "
    "định, và tiền đề của tìm kiếm nhị phân.",
    r"""
## Hai hàm mọi lập trình viên C phải sở hữu

```c
void qsort(void *base, size_t n, size_t size,
           int (*cmp)(const void *, const void *));
void *bsearch(const void *key, const void *base, size_t n, size_t size,
              int (*cmp)(const void *, const void *));
```

Cả hai chạy trên *bất kỳ* kiểu phần tử nào qua đúng bộ ba ở bài trước.
Comparator quyết định tất cả:

```c
/* phần tử int: đọc qua const void*, trả ba chiều */
int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);      /* không bao giờ a - b: INT_MIN làm tràn */
}
```

Hợp đồng: âm/không/dương cho nhỏ/bằng/lớn. `(x > y) - (x < y)` là mẫu
chống tràn; `a - b` trên int gãy ở hai đầu mút, và trên double có thể
làm tròn về 0 cho hai giá trị khác nhau.

## Hai lưu ý trung thực

**qsort không ổn định.** Phần tử bằng nhau có thể bị đảo thứ tự (chuẩn
không hứa gì; mỗi cài đặt một khác). Nếu thứ tự trong nhóm bằng nhau
quan trọng, thêm tiebreaker vào comparator, hoặc sort mảng cặp
(key, chỉ-số-gốc).

**bsearch đòi input đã sắp.** O(log n) của tìm kiếm nhị phân được thuê
từ tiền đề. bsearch trên dữ liệu chưa sắp không phải "kết quả sai" —
là undefined bạn tìm thấy phần tử nào (hoặc không). Và hợp đồng bsearch
nói *bất kỳ* phần tử khớp khi có trùng; cần first/last thì tự viết biến
thể lower_bound.

## Khi nào qsort là công cụ sai

Tính generic có giá: gọi comparator qua con trỏ hàm (phá inline),
memcpy `size` byte. Sort chuyên cho int có thể nhanh gấp nhiều lần.
qsort là *mặc định*; chuyên hóa khi đo đạc nói vậy.
"""
)

write_lesson(
    M, "generic-selection",
    "_Generic & Type-Safe Wrappers",
    "C's compile-time overloading: _Generic picks an expression by type, "
    "and macro wrappers seal the void* seams shut.",
    15,
    r"""
## Compile-time selection by type

C23's `_Generic` (available since C11) is overloading without functions:

```c
#define type_name(x) _Generic((x), \
    int: "int", double: "double", \
    char *: "char *", default: "other")
```

The selector `(x)` is *not evaluated* — only its type is examined after
lvalue conversion. Each association yields a different expression; the
compiler splices in exactly one. That makes `_Generic` the glue for
type-safe generic APIs:

```c
#define vec_push(v, val) _Generic((val), \
    int:    vpush_i, \
    double: vpush_d, \
    default: vpush_i)((v), (val))
```

The macro dispatches to the right concrete function *at compile time* —
zero runtime cost, full type checking, no `void*` at the call site.
The user of the library writes `vec_push(v, 42)` and the compiler
verifies `42` matches an implemented branch.

## The three layers, honestly ranked

1. **Concretely typed functions** (`vpush_i`) — the real work, fully
   type-checked.
2. **`_Generic` dispatch macro** — compile-time selection among them;
   documents the supported set; `default:` should fail loudly (a
   `(void)0`-style dead branch or a _Static_assert-friendly error).
3. **Raw `void *` + size + callback** — the universal engine beneath,
   needed when the *type itself* is a runtime parameter.

_Generic cannot dispatch on runtime values, cannot list every type, and
does not work on unresolved pointers-to-incomplete. It kills the
*common* typos; the engine still handles the general case.

## Static assertions seal the contract

```c
_Static_assert(sizeof(int) == 4, "vec_i assumes 4-byte int");
```

Compile-time contracts over representation assumptions: better a failed
build on an exotic platform than silent corruption shipped to users.
""",
"_Generic & wrapper type-safe",
    "Overloading compile-time của C: _Generic chọn biểu thức theo kiểu, "
    "và macro wrapper bịt kín các đường void*.",
    r"""
## Chọn tại compile-time theo kiểu

`_Generic` (có từ C11) là overloading không cần hàm:

```c
#define type_name(x) _Generic((x), \
    int: "int", double: "double", \
    char *: "char *", default: "other")
```

Bộ chọn `(x)` *không được tính giá trị* — chỉ kiểu của nó được xét sau
lvalue conversion. Mỗi liên kết cho một biểu thức khác nhau; compiler
ghép vào đúng một. Điều đó biến `_Generic` thành keo dán cho API generic
type-safe:

```c
#define vec_push(v, val) _Generic((val), \
    int:    vpush_i, \
    double: vpush_d, \
    default: vpush_i)((v), (val))
```

Macro dispatch tới đúng hàm cụ thể *lúc compile* — không tốn runtime,
kiểm kiểu đầy đủ, không `void*` ở chỗ gọi. Người dùng viết
`vec_push(v, 42)` và compiler kiểm chứng `42` khớp một nhánh đã cài.

## Ba tầng, xếp hạng trung thực

1. **Hàm kiểu cụ thể** (`vpush_i`) — việc thật, kiểm kiểu đầy đủ.
2. **Macro dispatch `_Generic`** — chọn lúc compile; liệt kê tập được
   hỗ trợ; `default:` nên hỏng ồn ào.
3. **`void *` thô + size + callback** — động cơ phổ quát bên dưới, cần
   khi *bản thân kiểu* là tham số runtime.

_Generic không dispatch trên giá trị runtime, không liệt kê được mọi
kiểu, và không chạy với pointer-to-incomplete. Nó giết các typo *thường
gặp*; động cơ vẫn xử lý trường hợp tổng quát.

## _Static_assert chốt hợp đồng

```c
_Static_assert(sizeof(int) == 4, "vec_i assumes 4-byte int");
```

Hợp đồng compile-time trên giả định biểu diễn: build gãy trên platform
lạ tốt hơn hỏng âm thầm tới tay người dùng.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p9-void",
    "void* Engine Gym",
    "Generic search, reverse, and dedup over raw bytes.",
    "Phòng gym động cơ void*",
    "Search, reverse, dedup generic trên byte thô.",
    after_lesson="void-bytes",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p9-void-core",
            "The Generic Engine",
            """Implement three generic array algorithms:

```c
/* returns pointer to first element where cmp returns 0, else NULL.
   base has n elements of `size` bytes. */
void *g_lsearch(const void *key, const void *base, size_t n, size_t size,
                int (*cmp)(const void *, const void *));
/* reverses element order in place */
void g_reverse(void *base, size_t n, size_t size);
/* returns 1 if some two elements compare equal, else 0.
   O(n^2) is fine. */
int g_has_dup(const void *base, size_t n, size_t size,
              int (*cmp)(const void *, const void *));
```""",
            C_PRELUDE + "\n#include <stddef.h>\nstatic int cmp_int(const void *a, const void *b) {\n    int x = *(const int *)a, y = *(const int *)b;\n    return (x > y) - (x < y);\n}\nstatic int cmp_short(const void *a, const void *b) {\n    short x = *(const short *)a, y = *(const short *)b;\n    return (x > y) - (x < y);\n}\nvoid *g_lsearch(const void *key, const void *base, size_t n, size_t size,\n                int (*cmp)(const void *, const void *));\nvoid g_reverse(void *base, size_t n, size_t size);\nint g_has_dup(const void *base, size_t n, size_t size,\n              int (*cmp)(const void *, const void *));\n",
            [
                (
                    "search, reverse, duplicate-hunt",
                    r"""
int a[] = {10, 20, 30, 40};
int key = 30;
int *hit = g_lsearch(&key, a, 4, sizeof(int), cmp_int);
CHECK(hit && *hit == 30 && hit == &a[2]);
key = 99;
CHECK(g_lsearch(&key, a, 4, sizeof(int), cmp_int) == NULL);
CHECK(g_lsearch(&key, NULL, 4, sizeof(int), cmp_int) == NULL);
g_reverse(a, 4, sizeof(int));
CHECK(a[0] == 40 && a[3] == 10);
double d[] = {1.5, 2.5};
g_reverse(d, 2, sizeof(double));
CHECK(d[0] == 2.5 && d[1] == 1.5);           /* any type, same code */
short s[] = {1, 2, 3, 2};
CHECK_EQ(g_has_dup(s, 4, sizeof(short), cmp_short), 1);
short s2[] = {1, 2, 3, 4};
CHECK_EQ(g_has_dup(s2, 4, sizeof(short), cmp_short), 0);
""",
                    "char* stepping: (const char*)base + i*size. Reverse: swap element i with n-1-i via a byte loop or temp buffer.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p9-void-core": vi_challenge(
            "Động cơ generic",
            "Cài g_lsearch, g_reverse, g_has_dup trên (base, n, size, cmp).",
            [("tìm, đảo, săn trùng", "đi bước char*: (const char*)base + i*size; reverse swap i với n-1-i.")],
        ),
    },
    solutions=[
        (
            "cint-p9-void-core",
            r"""
#include <string.h>
#include <stddef.h>
void *g_lsearch(const void *key, const void *base, size_t n, size_t size,
                int (*cmp)(const void *, const void *)) {
    if (!key || !base || !cmp) return NULL;
    const char *p = base;
    for (size_t i = 0; i < n; i++, p += size)
        if (cmp(key, p) == 0) return (void *)p;
    return NULL;
}
void g_reverse(void *base, size_t n, size_t size) {
    if (!base || n < 2) return;
    char *lo = base, *hi = (char *)base + (n - 1) * size;
    unsigned char tmp[64];
    while (lo < hi) {
        size_t k = size < sizeof tmp ? size : sizeof tmp;
        /* element-sized swap via buffer; elements assumed <= 64 bytes here */
        (void)k;
        for (size_t b = 0; b < size; b++) {
            char t = lo[b];
            lo[b] = hi[b];
            hi[b] = t;
        }
        lo += size;
        hi -= size;
    }
}
int g_has_dup(const void *base, size_t n, size_t size,
              int (*cmp)(const void *, const void *)) {
    if (!base || !cmp) return 0;
    const char *p = base;
    for (size_t i = 0; i < n; i++, p += size)
        for (size_t j = i + 1; j < n; j++)
            if (cmp(p, (const char *)base + j * size) == 0) return 1;
    return 0;
}""",
            r"""
#include <string.h>
#include <stddef.h>
void *g_lsearch(const void *key, const void *base, size_t n, size_t size,
                int (*cmp)(const void *, const void *)) {
    if (!key || !base || !cmp) return NULL;
    const char *p = base;
    for (size_t i = 0; i < n; i++, p += size)
        if (cmp(key, p) == 0) return (void *)p;
    return NULL;
}
void g_reverse(void *base, size_t n, size_t size) {
    if (!base || n < 2) return;
    char *lo = base, *hi = (char *)base + (n - 1) * size;
    while (lo < hi) {
        lo = lo + size;      /* wrong: advances lo by one element but
                                  never swaps — reverse does nothing */
        hi = hi - size;
    }
}
int g_has_dup(const void *base, size_t n, size_t size,
              int (*cmp)(const void *, const void *)) {
    if (!base || !cmp) return 0;
    const char *p = base;
    for (size_t i = 0; i < n; i++, p += size)
        for (size_t j = 0; j < i; j++)         /* wrong: compares with EARLIER
                                                      elements only up to i... but
                                                      j goes 0..i which includes the
                                                      element itself at j==i? no —
                                                      j < i so self-pair excluded;
                                                      real defect: returns 1 for the
                                                      FIRST pair even when none:
                                                      missing equality check */
            if (cmp(p, (const char *)base + j * size) == 0) return 1;
    return 0;
}""",
        ),
    ],
)

write_practice(
    M, "cint-p9-generic",
    "qsort, bsearch & _Generic Gym",
    "Standard-library generic algorithms plus a _Generic type-safe facade.",
    "Phòng gym qsort, bsearch & _Generic",
    "Thuật toán generic của stdlib cộng facade type-safe bằng _Generic.",
    after_lesson="generic-selection",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p9-qsort",
            "Sort & Search Through stdlib",
            """Use qsort and bsearch — no hand-rolled sorts. Implement:

```c
/* sorts n ints ascending */
void sort_ints(int *a, size_t n);
/* returns index of ANY occurrence of key in the SORTED array via
   bsearch; -1 if absent. Precondition: a is sorted ascending. */
long find_int(const int *a, size_t n, int key);
/* sorts n doubles ascending (careful: doubles need a different cmp) */
void sort_doubles(double *d, size_t n);
```

The boilerplate provides both comparators; you wire qsort/bsearch.""",
            C_PRELUDE + "\n#include <stdlib.h>\n#include <stddef.h>\nstatic int cmp_int(const void *a, const void *b) {\n    int x = *(const int *)a, y = *(const int *)b;\n    return (x > y) - (x < y);\n}\nstatic int cmp_double(const void *a, const void *b) {\n    double x = *(const double *)a, y = *(const double *)b;\n    return (x > y) - (x < y);\n}\nvoid sort_ints(int *a, size_t n);\nlong find_int(const int *a, size_t n, int key);\nvoid sort_doubles(double *d, size_t n);\n",
            [
                (
                    "stdlib wiring",
                    r"""
int a[] = {5, 3, 9, 1, 3};
sort_ints(a, 5);
CHECK(a[0] == 1 && a[1] == 3 && a[2] == 3 && a[4] == 9);
CHECK_EQ(find_int(a, 5, 3) >= 1 && find_int(a, 5, 3) <= 2, 1);  /* any of the two */
CHECK_EQ(find_int(a, 5, 4), -1);
CHECK_EQ(find_int(a, 0, 1), -1);
double d[] = {2.5, -1.0, 0.0};
sort_doubles(d, 3);
CHECK(d[0] == -1.0 && d[2] == 2.5);
""",
                    "qsort(a, n, sizeof *a, cmp_int); bsearch(&key, a, n, sizeof *a, cmp_int) then subtract base to get the index.",
                ),
            ],
        ),
        challenge(
            "cint-p9-typed-facade",
            "A Type-Safe Stack Facade",
            """The boilerplate provides an int-stack and a double-stack with
concrete functions (`si_push`, `sd_push`, ...). Implement ONLY the
_Generic dispatch macros:

```c
#define stack_push(st, val)  /* dispatches to si_push/sd_push by val's type */
#define stack_pop(st, out)   /* dispatches to si_pop/sd_pop by *out's type */
```

the type checking
(no void*, no runtime tag).""",
            C_PRELUDE + "\n#include <stddef.h>\ntypedef struct { int data[32]; size_t n; } IStack;\ntypedef struct { double data[32]; size_t n; } DStack;\nstatic int si_push(IStack *s, int v) { if (s->n == 32) return -1; s->data[s->n++] = v; return 0; }\nstatic int sd_push(DStack *s, double v) { if (s->n == 32) return -1; s->data[s->n++] = v; return 0; }\nstatic int si_pop(IStack *s, int *out) { if (s->n == 0) return -1; *out = s->data[--s->n]; return 0; }\nstatic int sd_pop(DStack *s, double *out) { if (s->n == 0) return -1; *out = s->data[--s->n]; return 0; }\n",
            [
                (
                    "compile-time dispatch",
                    r"""
IStack is = {0}; DStack ds = {0};
CHECK_EQ(stack_push(&is, 42), 0);
CHECK_EQ(stack_push(&ds, 2.5), 0);
int iv; double dv;
CHECK_EQ(stack_pop(&is, &iv), 0); CHECK_EQ(iv, 42);
CHECK_EQ(stack_pop(&ds, &dv), 0); CHECK(dv == 2.5);
CHECK_EQ(stack_pop(&is, &iv), -1);
CHECK_EQ(stack_push(&is, 1), 0);
CHECK_EQ(stack_pop(&is, &iv), 0);
""",
                    "_Generic((val), int: si_push, double: sd_push) selects the function at compile time; the call stays fully checked.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p9-qsort": vi_challenge(
            "Sort & search qua stdlib",
            "Dùng qsort/bsearch (không tự viết sort): sort_ints, find_int, sort_doubles.",
            [("nối dây stdlib", "qsort(a, n, sizeof *a, cmp); bsearch rồi trừ base ra chỉ số.")],
        ),
        "cint-p9-typed-facade": vi_challenge(
            "Facade type-safe",
            "Cài macro _Generic stack_push/stack_pop dispatch theo kiểu, không void*, không tag runtime.",
            [("dispatch compile-time", "_Generic((val), int: si_push, double: sd_push)((st), (val))")],
        ),
    },
    solutions=[
        (
            "cint-p9-qsort",
            r"""
#include <stdlib.h>
#include <stddef.h>
void sort_ints(int *a, size_t n) {
    if (!a) return;
    qsort(a, n, sizeof *a, cmp_int);
}
long find_int(const int *a, size_t n, int key) {
    if (!a || n == 0) return -1;
    const int *hit = bsearch(&key, a, n, sizeof *a, cmp_int);
    return hit ? (long)(hit - a) : -1;
}
void sort_doubles(double *d, size_t n) {
    if (!d) return;
    qsort(d, n, sizeof *d, cmp_double);
}""",
            r"""
#include <stdlib.h>
#include <stddef.h>
void sort_ints(int *a, size_t n) {
    if (!a) return;
    qsort(a, n, sizeof(int), cmp_int);      /* fine */
}
long find_int(const int *a, size_t n, int key) {
    if (!a || n == 0) return -1;
    const int *hit = bsearch(&key, a, n, sizeof(int), cmp_int);
    return hit ? (long)(hit - a) : -1;
}
void sort_doubles(double *d, size_t n) {
    if (!d) return;
    qsort(d, n, sizeof *d, cmp_int);        /* wrong: int comparator on doubles —
                                                 reads 4 of the 8 bytes, garbage order */
}""",
        ),
        (
            "cint-p9-typed-facade",
            r"""
#define stack_push(st, val) _Generic((val), int: si_push, double: sd_push)((st), (val))
#define stack_pop(st, out) _Generic((out), int *: si_pop, double *: sd_pop)((st), (out))""",
            r"""
#define stack_push(st, val) _Generic((val), int: si_push, double: sd_push)((st), (val))
#define stack_pop(st, out) (*(out) = 0, (st)->n--)   /* wrong: bypasses the typed
                                                 functions — writes 0 instead of the
                                                 popped value, returns the old count
                                                 instead of 0/-1, and underflows n
                                                 when empty */""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m9-task",
    "Generic Library: Sort, Search, Dedup",
    """Ship the mini-library: a generic toolkit over void* with a typed
facade. The boilerplate declares the raw engine and the facade macro
(you implement the engine functions; the facade is given):

```c
/* engine: */
void g_sort(void *base, size_t n, size_t size,
            int (*cmp)(const void *, const void *));    /* any sort you like */
size_t g_dedup(void *base, size_t n, size_t size,
               int (*cmp)(const void *, const void *));
/* removes adjacent duplicates (array MUST be sorted first — sort it
   yourself inside), returns new length. In place; tail is unspecified. */
/* facade over int arrays only: */
#define isort(a, n) g_sort((a), (n), sizeof(int), cmp_int)
```

`cmp_int` is provided in the boilerplate.""",
    C_PRELUDE + "\n#include <stddef.h>\nstatic int cmp_int(const void *a, const void *b) {\n    int x = *(const int *)a, y = *(const int *)b;\n    return (x > y) - (x < y);\n}\nstatic int cmp_double(const void *a, const void *b) {\n    double x = *(const double *)a, y = *(const double *)b;\n    return (x > y) - (x < y);\n}\nvoid g_sort(void *base, size_t n, size_t size,\n            int (*cmp)(const void *, const void *));\nsize_t g_dedup(void *base, size_t n, size_t size,\n               int (*cmp)(const void *, const void *));\n#define isort(a, n) g_sort((a), (n), sizeof(int), cmp_int)\n",
    [
        (
            "engine + facade",
            r"""
int a[] = {5, 1, 5, 3, 1, 9, 5};
isort(a, 7);                       /* facade dispatches with sizeof(int) */
CHECK(a[0] == 1 && a[1] == 1 && a[6] == 9);
size_t m = g_dedup(a, 7, sizeof(int), cmp_int);
CHECK_EQ(m, 4);
CHECK(a[0] == 1 && a[1] == 3 && a[2] == 5 && a[3] == 9);
double d[] = {2.5, 2.5, 2.5};
g_sort(d, 3, sizeof(double), cmp_double);
size_t md = g_dedup(d, 3, sizeof(double), cmp_double);
CHECK_EQ(md, 1);
CHECK(d[0] == 2.5);
""",
            "Sort first (any algorithm — even insertion sort via swap_bytes), then two-finger compaction copying distinct elements down.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Thư viện generic: sort, search, dedup",
        "Cài động cơ g_sort + g_dedup (dedup tự sort trước, in-place, trả chiều dài mới).",
        [("động cơ + facade", "sort trước, rồi hai ngón nén các phần tử phân biệt xuống.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m9",
    "Checkpoint: The Generic Layer Cake",
    "Prove the whole stack: byte engine, stdlib wiring, and a typed facade — one API, three layers.",
    26,
    r"""
## The task

Implement `g_sort` and `g_dedup` (see the challenge). The facade macro
`isort` is given — your engine beneath it must be correct for ANY
element type, and dedup must enforce its own precondition (sort
internally). This is the module's thesis in two functions: the
byte-level engine does the work, the type system lives in the callers.

Passing this proves you can write the layer C libraries actually ship:
generic at the bottom, type-safe at the top, contracts in between.

Next module: the preprocessor — macros as a language over the language.
""",
    "Kiểm tra: Ba tầng generic",
    "Chứng minh trọn bộ chồng: động cơ byte, nối dây stdlib, facade kiểu — một API, ba tầng.",
    r"""
## Bài toán

Cài `g_sort` và `g_dedup` (xem challenge). Macro facade `isort` đã cho —
động cơ bên dưới phải đúng với MỌI kiểu phần tử, và dedup phải tự thực
thi tiền đề (sort bên trong). Đây là luận điểm của module trong hai hàm:
động cơ cấp byte làm việc, hệ kiểu sống ở phía caller.

Vượt qua chứng minh bạn viết được tầng mà thư viện C thật sự đóng gói:
generic ở đáy, type-safe trên đỉnh, hợp đồng ở giữa.

Module sau: preprocessor — macro như ngôn ngữ trên ngôn ngữ.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <string.h>
#include <stddef.h>
static void swap_elems(char *a, char *b, size_t size) {
    while (size--) {
        char t = *a;
        *a++ = *b;
        *b++ = t;
    }
}
void g_sort(void *base, size_t n, size_t size,
            int (*cmp)(const void *, const void *)) {
    if (!base || !cmp || n < 2) return;
    char *b = base;
    for (size_t i = 1; i < n; i++)           /* insertion sort via swaps */
        for (size_t j = i; j > 0 &&
             cmp(b + (j - 1) * size, b + j * size) > 0; j--)
            swap_elems(b + (j - 1) * size, b + j * size, size);
}
size_t g_dedup(void *base, size_t n, size_t size,
               int (*cmp)(const void *, const void *)) {
    if (!base || !cmp) return 0;
    g_sort(base, n, size, cmp);              /* enforce the precondition */
    char *wr = (char *)base + size;          /* element 0 already kept */
    size_t m = 1;
    for (size_t i = 1; i < n; i++) {
        char *cur = (char *)base + i * size;
        if (cmp(wr - size, cur) != 0) {      /* distinct from last KEPT */
            if (wr != cur) memcpy(wr, cur, size);
            wr += size;
            m++;
        }
    }
    return m;
}""",
    wrong=r"""
#include <string.h>
#include <stddef.h>
static void swap_miss(char *a, char *b, size_t size) { (void)a; (void)b; (void)size; }
void g_sort(void *base, size_t n, size_t size,
            int (*cmp)(const void *, const void *)) {
    if (!base || !cmp || n < 2) return;
    char *b = base;
    for (size_t i = 1; i < n; i++)
        for (size_t j = i; j > 0 &&
             cmp(b + (j - 1) * size, b + j * size) > 0; j--)
            swap_miss(b + (j - 1) * size, b + j * size, size);   /* wrong: the swap
                                                  is a no-op — the sort never reorders,
                                                  so both isort and dedup's internal
                                                  sort leave data unsorted */
}
size_t g_dedup(void *base, size_t n, size_t size,
               int (*cmp)(const void *, const void *)) {
    if (!base || !cmp) return 0;
    g_sort(base, n, size, cmp);
    char *rd = base, *wr = base;
    size_t m = 1;
    for (size_t i = 1; i < n; i++) {
        char *cur = (char *)base + i * size;
        if (cmp(rd, cur) != 0) {             /* wrong: compares against the READ
                                                  cursor (last SEEN) instead of last
                                                  KEPT — on input 1,1,2 it advances rd
                                                  even for duplicates and can drop
                                                  distinct elements */
            rd = cur;
            memcpy(wr, cur, size);
            wr += size;
            m++;
        }
        rd += size;
    }
    return m;
}""",
)

print("module 9 complete")
