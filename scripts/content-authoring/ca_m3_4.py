#!/usr/bin/env python3
"""C Advanced — batch 2: modules 3 (advanced-pointer-semantics) and
4 (ub-optimizer). Zero-backslash authoring: @NL@ = statement separator,
@CE@ = newline escape inside C string literals."""
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

# ================== MODULE 3: ca-advanced-pointers ==========================
M3 = "ca-advanced-pointers"

L3A = "ca-pointer-arithmetic-rules"
L3B = "ca-aliasing-const-restrict"
L3C = "ca-fnptr-interfaces"
L3CP = "ca-checkpoint-m3"

write_module(
    M3,
    "Advanced Pointer Semantics",
    "Arithmetic beyond the bounds rule, aliasing and restrict, and pointer-built interfaces — the semantics the compiler actually assumes.",
    "Ngữ nghĩa con trỏ nâng cao",
    "Phép tính con trỏ vượt luật biên, aliasing và restrict, và các giao diện dựng trên con trỏ — ngữ nghĩa mà trình biên dịch thực sự giả định.",
    [L3A, L3B, L3C, L3CP],
    ["ca-p3-pointers"],
)

write_lesson(
    M3,
    L3A,
    "Pointer Arithmetic, Precisely",
    "What pointer arithmetic guarantees — and the exact boundary where it stops.",
    14,
    """
## The one legal region

If `p` points into an array of `N` elements (or one past its end), you may:

- add/subtract an integer, staying within `[begin, begin + N]`;
- subtract two pointers into the same array;
- compare two pointers into the same array;
- dereference only while the result points at an element.

Everything else is undefined. `p + N` is computable but not dereferenceable — that one-past-the-end pointer is the anchor every `for` loop and `memcpy` boundary silently relies on.

```c
int a[4];
int *e = a + 4;        /* OK: one past the end */
int *f = a + 5;        /* UB: not computable */
*e = 0;                /* UB: e is not dereferenceable */
```

## The object does not need to be an array

A pointer to a single object behaves as an array of one: `&obj + 1` is legal (one past it), `&obj + 2` is not. This is what makes member-wise cleanup loops correct.

## struct member arithmetic

Pointer arithmetic between members of a struct is NOT covered by the array rule — `offsetof`-based conversion (`(char *)&s + offsetof(struct S, b)`) is the portable way to walk members; subtracting `&s.b - &s.a` is UB even though it usually prints 4.
""",
    "Phép tính con trỏ, chính xác",
    "Phép tính con trỏ bảo đảm gì — và ranh giới chính xác nơi nó dừng lại.",
    """
## Vùng hợp lệ duy nhất

Nếu `p` trỏ vào mảng `N` phần tử (hoặc một vị trí sau cuối), bạn được phép:

- cộng/trừ số nguyên, giữ trong `[begin, begin + N]`;
- trừ hai con trỏ cùng mảng;
- so sánh hai con trỏ cùng mảng;
- hủy tham chiếu chỉ khi kết quả trỏ vào phần tử thật.

Còn lại là không xác định. `p + N` tính được nhưng không được hủy tham chiếu — con trỏ một-vị-trình-sau-cuối là điểm neo của mọi vòng `for` và biên `memcpy`.

```c
int a[4];
int *e = a + 4;        /* OK: một vị trí sau cuối */
int *f = a + 5;        /* UB: không tính được */
*e = 0;                /* UB: e không hủy tham chiếu được */
```

## Đối tượng đơn cũng dùng được

Con trỏ tới một đối tượng đơn coi như mảng một phần tử: `&obj + 1` hợp lệ, `&obj + 2` thì không.

## Thành phần struct

Phép tính giữa các thành phần struct KHÔNG nằm trong luật mảng — cách khả chuyển là `offsetof`; trừ địa chỉ hai thành phần là UB.
""",
)

write_lesson(
    M3,
    L3B,
    "Aliasing, const, and restrict",
    "What may legally alias what, how const really reads, and the restrict contract you make with the optimizer.",
    15,
    """
## The effective-type rule

An object's stored value may only be accessed through an lvalue of a compatible type — or through `char` (any object's bytes are always readable as chars, which is what `memcpy` and debuggers are built on). This is why:

```c
float f = 1.0f;
int bits = *(int *)&f;          /* UB: wrong effective type */
int bits2;
memcpy(&bits2, &f, sizeof f);   /* defined: byte copy */
```

Compilers assume it hard: after `int *p` and `float *q` are both in play, a store through one may be assumed not to touch the other.

## const is a contract, not protection

`const int *p` says *through this lvalue* you will not write. Casting it away and writing is UB **only if** the object was defined const; writing through a cast on a non-const object is legal. Two different sentences hiding in one keyword.

## restrict: the promise that pays

`void copy(int *restrict d, const int *restrict s, size_t n)` promises: for the function's duration, every write through `d` aliases nothing read through `s`. Break the promise (overlapping ranges) and even memcpy-identical code may miscompute — that is exactly why the standard splits `memcpy` (restrict, UB on overlap) from `memmove` (defined on overlap, may be slower).
""",
    "Aliasing, const, và restrict",
    "Cái gì được phép alias cái gì, const thực sự nghĩa là gì, và hợp đồng restrict với trình tối ưu hóa.",
    """
## Luật effective type

Giá trị của đối tượng chỉ được truy cập qua lvalue kiểu tương thích — hoặc qua `char` (byte của đối tượng nào cũng đọc được thành char, đó là nền của memcpy). Vì vậy:

```c
float f = 1.0f;
int bits = *(int *)&f;          /* UB: sai effective type */
int bits2;
memcpy(&bits2, &f, sizeof f);   /* hợp lệ: sao chép theo byte */
```

Trình biên dịch giả định điều này rất mạnh: `int *p` và `float *q` cùng tồn tại nghĩa là ghi qua cái này được coi không đụng cái kia.

## const là hợp đồng, không phải chống trộm

`const int *p` nghĩa là *qua lvalue này* bạn không được ghi. Ép bỏ const rồi ghi là UB **chỉ khi** đối tượng được khai báo const; ghi qua ép kiểu vào đối tượng vốn không const thì hợp lệ.

## restrict: lời hứa có giá

`copy(restrict d, restrict s, n)` hứa: trong thời gian chạy hàm, mọi ghi qua `d` không alias gì đọc qua `s`. Phá lời hứa (vùng chồng nhau) là code giống memcpy có thể ra kết quả sai — đó chính là lý do chuẩn tách `memcpy` (restrict, UB khi chồng) khỏi `memmove` (hợp lệ khi chồng, có thể chậm hơn).
""",
)

write_lesson(
    M3,
    L3C,
    "Interfaces Built from Pointers",
    "Function pointers, opaque handles, and the calling-contract patterns that scale.",
    14,
    """
## Function pointers name behavior

```c
typedef int (*cmp_fn)(const void *a, const void *b);
void sort(void *base, size_t n, size_t w, cmp_fn cmp);
```

`qsort` is exactly this shape: the algorithm is generic, the *comparison policy* is a runtime pointer. Calling through the pointer is an indirect call — the one thing preventing inlining unless the compiler can see the target.

## Opaque handles hide the struct

Publish a header with `typedef struct cache cache_t;` and functions taking `cache_t *`; define the struct only in the .c file. Clients cannot depend on layout (you can change it freely), and every access goes through your validation. This is the standard C module boundary.

## The context-pointer pattern

Callbacks that need state take `void *ctx`:

```c
void foreach(list_t *l, void (*fn)(void *item, void *ctx), void *ctx);
```

The alternative — global variables — breaks reentrancy and threads. Every serious C API you will meet (event loops, hash iterators, thread pools) uses the context pointer.
""",
    "Giao diện dựng từ con trỏ",
    "Function pointer, opaque handle, và các mẫu hợp đồng gọi có khả năng mở rộng.",
    """
## Function pointer đặt tên cho hành vi

```c
typedef int (*cmp_fn)(const void *a, const void *b);
void sort(void *base, size_t n, size_t w, cmp_fn cmp);
```

`qsort` đúng hình dáng này: thuật toán chung, *chính sách so sánh* là con trỏ lúc chạy. Gọi qua con trỏ là gọi gián tiếp — thứ ngăn inline trừ khi trình biên dịch nhìn thấy đích.

## Opaque handle giấu struct

Header chỉ công bố `typedef struct cache cache_t;` cùng các hàm nhận `cache_t *`; định nghĩa struct nằm trong file .c. Client không phụ thuộc bố cục (đổi thoải mái), mọi truy cập đi qua kiểm tra của bạn.

## Mẫu context pointer

Callback cần trạng thái thì nhận `void *ctx`. Thay thế — biến toàn cục — phá vỡ reentrancy và thread. Mọi API C nghiêm túc (event loop, iterator, thread pool) đều dùng context pointer.
""",
)

write_practice(
    M3,
    "ca-p3-pointers",
    "Pointer Semantics Drills",
    "Turn pointer rules into executable probes: arithmetic, aliasing, restrict, and callback interfaces.",
    "Bài tập ngữ nghĩa con trỏ",
    "Biến luật con trỏ thành thăm dò chạy được: phép tính, aliasing, restrict, và giao diện callback.",
    L3A,
    22,
    "advanced",
    [
        challenge(
            "ca3-ptr-span",
            "Measure the Legal Span",
            "Implement `size_t legal_span(void)`: given the file-scope array `static int arr[6];` (already in your editor), return how many distinct pointer values `arr + k` (k = 0..) are *computable* — including the one-past-the-end value. Then implement `size_t deref_span(void)` returning how many of those are dereferenceable.",
            C_PRELUDE + "static int arr[6];@NL@",
            [
                ("computable includes the end", "CHECK_EQ((int)legal_span(), 7);", "k ranges 0..6: six element pointers plus the one-past-the-end pointer."),
                ("dereferenceable excludes it", "CHECK_EQ((int)deref_span(), 6);", "arr + 6 is computable but never dereferenceable."),
            ],
            level="independent",
        ),
        challenge(
            "ca3-memcpy-bits",
            "Read Bits Legally",
            "Implement `unsigned int float_bits(float f)` returning the 32 bits of f's representation. The cast chain `*(unsigned *)&f` is the UB trap; copy the bytes instead — either via `memcpy`, or through an `unsigned char` walk you accumulate into an unsigned.",
            C_PRELUDE,
            [
                ("1.0f representation", "CHECK_EQ((int)float_bits(1.0f), (int)0x3F800000u);", "memcpy into an unsigned; 1.0f is exponent 127, mantissa 0."),
                ("0.0f representation", "CHECK_EQ((int)float_bits(0.0f), 0);", "All representation bytes of +0.0f are zero."),
            ],
            level="independent",
        ),
        challenge(
            "ca3-restrict-sum",
            "Prove restrict Correct",
            "Implement `long long sum_doubled(const int *restrict a, size_t n)`: add every a[i] twice. Then implement `int ranges_overlap(const void *p1, size_t n1, const void *p2, size_t n2)` returning 1 iff the byte ranges intersect — the check you must run before passing overlapping buffers to a restrict API.",
            C_PRELUDE,
            [
                ("sum doubles", "int v[3] = {1, 2, 3};@NL@CHECK_EQ(sum_doubled(v, 3), 12);", "1+1+2+2+3+3 = 12; reads never alias writes here."),
                ("overlap detection", "int v[4] = {0, 0, 0, 0};@NL@CHECK_EQ(ranges_overlap(v, 3 * sizeof(int), v + 2, 2 * sizeof(int)), 1);@NL@CHECK_EQ(ranges_overlap(v, 2 * sizeof(int), v + 2, 2 * sizeof(int)), 0);", "Byte counts, memcpy-style: [v, v+12) vs [v+8, v+16) intersect; [v, v+8) vs [v+8, v+16) do not."),
            ],
            level="combination",
        ),
        challenge(
            "ca3-opaque-cache",
            "Build an Opaque Cache",
            "Implement a tiny fixed-size cache behind an opaque API: `cache_t *cache_create(size_t cap)`, `int cache_put(cache_t *c, int key, int value)` (returns 1 stored, 0 full), `int *cache_get(cache_t *c, int key)` (returns NULL on miss). Keep the struct definition in your source; the tests only use the functions — that is the opacity contract.",
            C_PRELUDE,
            [
                ("put then get", "cache_t *c = cache_create(4);@NL@CHECK_EQ(cache_put(c, 7, 700), 1);@NL@int *v = cache_get(c, 7);@NL@CHECK_NOT_NULL(v);@NL@CHECK_EQ(*v, 700);", "Store then retrieve through the handle; the caller never sees the layout."),
                ("miss is NULL", "cache_t *c = cache_create(4);@NL@CHECK_NULL(cache_get(c, 999));", "A fresh cache; absent keys must return NULL, not garbage."),
                ("full is rejected", "cache_t *c = cache_create(4);@NL@for (int k = 0; k < 4; k++) cache_put(c, k, k);@NL@CHECK_EQ(cache_put(c, 99, 99), 0);", "cap is respected: the fifth insert reports 0."),
                ("update keeps capacity", "cache_t *c = cache_create(2);@NL@cache_put(c, 1, 10);@NL@cache_put(c, 2, 20);@NL@CHECK_EQ(cache_put(c, 1, 99), 1);@NL@CHECK_EQ(*cache_get(c, 1), 99);", "Updating an existing key must succeed on a FULL cache — an update must not consume a new slot."),
            ],
            level="mini-build",
        ),
        challenge(
            "ca3-ctx-foreach",
            "Sum Through a Callback",
            "Implement `void foreach_int(const int *a, size_t n, void (*fn)(int v, void *ctx), void *ctx)` calling fn once per element, and use it to implement `long long sum_with_ctx(const int *a, size_t n)` which totals the array through a stack-allocated context struct — no globals. The ctx pattern is the point.",
            C_PRELUDE,
            [
                ("sums correctly", "int v[5] = {1, -2, 3, -4, 5};@NL@CHECK_EQ(sum_with_ctx(v, 5), 3);", "The ctx accumulator collects every callback visit; 1-2+3-4+5 = 3."),
                ("empty is zero", "CHECK_EQ(sum_with_ctx(0, 0), 0);", "n = 0 must survive: zero visits, ctx total stays 0."),
            ],
            level="combination",
        ),
    ],
    {
        "ca3-ptr-span": vi_challenge(
            "Đo khoảng hợp lệ",
            "Trả về số giá trị con trỏ tính được (gồm một-vị-trí-sau-cuối) và số giá trị hủy tham chiếu được.",
            [
                ("tính được gồm điểm cuối", "k chạy 0..6: sáu con trỏ phần tử cộng con trỏ sau cuối."),
                ("hủy tham chiếu không gồm nó", "arr + 6 tính được nhưng không bao giờ hủy tham chiếu được."),
            ],
        ),
        "ca3-memcpy-bits": vi_challenge(
            "Đọc bit hợp lệ",
            "Trả về 32 bit biểu diễn của float — ép kiểu sai kiểu là bẫy UB, hãy sao chép byte qua memcpy.",
            [
                ("biểu diễn 1.0f", "memcpy vào unsigned; 1.0f là số mũ 127, định trị 0."),
                ("biểu diễn 0.0f", "Mọi byte biểu diễn của +0.0f đều bằng 0."),
            ],
        ),
        "ca3-restrict-sum": vi_challenge(
            "Chứng minh restrict đúng",
            "Cài sum_doubled (mỗi phần tử cộng hai lần) và ranges_overlap — kiểm tra bạn phải chạy trước khi đưa buffer chồng nhau vào API restrict.",
            [
                ("cộng gấp đôi", "1+1+2+2+3+3 = 12; đọc không alias ghi ở đây."),
                ("phát hiện chồng", "Đếm theo BYTE kiểu memcpy: [v, v+12) giao [v+8, v+16); [v, v+8) không giao [v+8, v+16)."),
            ],
        ),
        "ca3-opaque-cache": vi_challenge(
            "Dựng cache opaque",
            "Cài cache kích thước cố định sau API opaque: create/put/get — struct định nghĩa trong source, test chỉ dùng hàm.",
            [
                ("put rồi get", "Lưu rồi lấy qua handle; caller không bao giờ thấy bố cục."),
                ("miss là NULL", "Khóa vắng mặt trả NULL, không phải rác."),
                ("đầy thì từ chối", "cap được tôn trọng: lần chèn thứ năm báo 0."),
                ("cập nhật giữ năng lực", "Cập nhật khóa tồn tại phải thành công cả khi cache ĐẦY — cập nhật không được tiêu thụ slot mới."),
            ],
        ),
        "ca3-ctx-foreach": vi_challenge(
            "Tổng qua callback",
            "Cài foreach_int với callback (v, ctx) và sum_with_ctx tổng mảng qua ctx trên stack — không biến toàn cục.",
            [
                ("cộng đúng", "Ctx tích lũy mọi lần gọi callback; 1-2+3-4+5 = 3."),
                ("rỗng bằng 0", "n = 0 phải sống sót: không lần gọi nào, tổng ctx giữ 0."),
            ],
        ),
    },
    solutions=[
        (
            "ca3-ptr-span",
            C_PRELUDE
            + "static int arr[6];@NL@"
            + "size_t legal_span(void) {@NL@    return 7;@NL@}@NL@"
            + "size_t deref_span(void) {@NL@    return 6;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "static int arr[6];@NL@"
            + "size_t legal_span(void) {@NL@    return 8;@NL@}@NL@"
            + "size_t deref_span(void) {@NL@    return 7;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca3-memcpy-bits",
            "#include <string.h>@NL@" + C_PRELUDE
            + "unsigned int float_bits(float f) {@NL@    unsigned u;@NL@    memcpy(&u, &f, sizeof u);@NL@    return u;@NL@}@NL@"
            + "int main(void) { return 0; }",
            "#include <string.h>@NL@" + C_PRELUDE
            + "unsigned int float_bits(float f) {@NL@    unsigned int u;@NL@    memcpy(&u, &f, sizeof u);@NL@    return ((u & 0xFFu) << 24) | ((u & 0xFF00u) << 8) | ((u >> 8) & 0xFF00u) | (u >> 24);@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca3-restrict-sum",
            C_PRELUDE
            + "long long sum_doubled(const int *restrict a, size_t n) {@NL@    long long s = 0;@NL@    for (size_t i = 0; i < n; i++) s += (long long)a[i] * 2;@NL@    return s;@NL@}@NL@"
            + "int ranges_overlap(const void *p1, size_t n1, const void *p2, size_t n2) {@NL@    const char *a = p1;@NL@    const char *b = p2;@NL@    return (a < b + n2 && b < a + n1) ? 1 : 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "long long sum_doubled(const int *restrict a, size_t n) {@NL@    long long s = 0;@NL@    for (size_t i = 0; i < n; i++) s += (long long)a[i] * 2;@NL@    return s;@NL@}@NL@"
            + "int ranges_overlap(const void *p1, size_t n1, const void *p2, size_t n2) {@NL@    return (p1 == p2) ? 1 : 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca3-opaque-cache",
            "#include <stdlib.h>@NL@" + C_PRELUDE
            + "typedef struct { int key; int val; int used; } slot_t;@NL@"
            + "typedef struct { slot_t *slots; size_t cap; } cache_t;@NL@"
            + "cache_t *cache_create(size_t cap) {@NL@    cache_t *c = malloc(sizeof *c);@NL@    if (!c) return NULL;@NL@    c->slots = calloc(cap, sizeof *c->slots);@NL@    if (!c->slots) { free(c); return NULL; }@NL@    c->cap = cap;@NL@    return c;@NL@}@NL@"
            + "int cache_put(cache_t *c, int key, int value) {@NL@    for (size_t i = 0; i < c->cap; i++) {@NL@        if (c->slots[i].used && c->slots[i].key == key) { c->slots[i].val = value; return 1; }@NL@    }@NL@    for (size_t i = 0; i < c->cap; i++) {@NL@        if (!c->slots[i].used) { c->slots[i].used = 1; c->slots[i].key = key; c->slots[i].val = value; return 1; }@NL@    }@NL@    return 0;@NL@}@NL@"
            + "int *cache_get(cache_t *c, int key) {@NL@    for (size_t i = 0; i < c->cap; i++) {@NL@        if (c->slots[i].used && c->slots[i].key == key) return &c->slots[i].val;@NL@    }@NL@    return NULL;@NL@}@NL@"
            + "int main(void) { return 0; }",
            "#include <stdlib.h>@NL@" + C_PRELUDE
            + "typedef struct { int key; int val; int used; } slot_t;@NL@"
            + "typedef struct { slot_t *slots; size_t cap; } cache_t;@NL@"
            + "cache_t *cache_create(size_t cap) {@NL@    cache_t *c = malloc(sizeof *c);@NL@    c->slots = calloc(cap, sizeof *c->slots);@NL@    c->cap = cap;@NL@    return c;@NL@}@NL@"
            + "int cache_put(cache_t *c, int key, int value) {@NL@    for (size_t i = 0; i < c->cap; i++) {@NL@        if (!c->slots[i].used) { c->slots[i].used = 1; c->slots[i].key = key; c->slots[i].val = value; return 1; }@NL@    }@NL@    return 0;@NL@}@NL@"
            + "int *cache_get(cache_t *c, int key) {@NL@    for (size_t i = 0; i < c->cap; i++) {@NL@        if (c->slots[i].used && c->slots[i].key == key) return &c->slots[i].val;@NL@    }@NL@    return NULL;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca3-ctx-foreach",
            C_PRELUDE
            + "void foreach_int(const int *a, size_t n, void (*fn)(int v, void *ctx), void *ctx) {@NL@    for (size_t i = 0; i < n; i++) fn(a[i], ctx);@NL@}@NL@"
            + "typedef struct { long long total; } sumctx_t;@NL@"
            + "static void add_fn(int v, void *ctx) { ((sumctx_t *)ctx)->total += v; }@NL@"
            + "long long sum_with_ctx(const int *a, size_t n) {@NL@    sumctx_t c = {0};@NL@    foreach_int(a, n, add_fn, &c);@NL@    return c.total;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "void foreach_int(const int *a, size_t n, void (*fn)(int v, void *ctx), void *ctx) {@NL@    for (size_t i = 0; i < n; i++) fn(a[0], ctx);@NL@}@NL@"
            + "typedef struct { long long total; } sumctx_t;@NL@"
            + "static long long g_total = 0;@NL@"
            + "static void add_fn(int v, void *ctx) { (void)ctx; g_total += v; }@NL@"
            + "long long sum_with_ctx(const int *a, size_t n) {@NL@    g_total = 0;@NL@    foreach_int(a, n, add_fn, 0);@NL@    return g_total;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M3,
    L3CP,
    "Checkpoint: Pointer Contracts",
    "Consolidated pointer-semantics checkpoint.",
    12,
    """
Checkpoint for module 3: one program combining a legal-span probe, a byte-legal representation read, and an opaque handle with a ctx-callback visit counter.
""",
    "Kiểm tra: Hợp đồng con trỏ",
    "Kiểm tra tổng hợp ngữ nghĩa con trỏ.",
    """
Kiểm tra mô-đun 3: một chương trình gồm thăm dò khoảng hợp lệ, đọc biểu diễn theo byte hợp lệ, và opaque handle với bộ đếm lượt callback qua ctx.
""",
)

write_checkpoint(
    M3,
    L3CP,
    "Checkpoint: Pointer Contracts",
    "Combine the module's contracts in one program: count the legal pointer span of an array, read a double's bits through legal byte access, and expose an opaque counter advanced through a context callback.",
    16,
    "See lesson.",
    "Kiểm tra: Hợp đồng con trỏ",
    "Kết hợp các hợp đồng của mô-đun trong một chương trình.",
    "Xem bài học.",
    challenge(
        "ca3-checkpoint-contracts",
        "Checkpoint: Pointer Contracts",
        "A file-scope `static double dvals[4];` is already in your editor. Implement three things:@CE@ @CE@1. `size_t span(void)` — how many pointer values `dvals + k` are computable (including one past the end).@CE@2. `unsigned long long dbytes(void)` — the 8 bytes of `dvals[0]`'s representation, read via `memcpy` into an `unsigned long long` (dvals[0] is 1.5, set it in an initializer).@CE@3. `typedef struct counter counter_t;` with `counter_t *counter_create(void)`, `void counter_visit(counter_t *c, void (*fn)(void *ctx), void *ctx)` (calls fn once, per visit), and `int counter_count(counter_t *c)` returning total visits so far.",
        C_PRELUDE + "static double dvals[4] = {1.5, 0, 0, 0};@NL@",
        [
            ("span includes the end", "CHECK_EQ((int)span(), 5);", "4 element pointers plus the one-past-the-end pointer."),
            ("bits of 1.5", "CHECK_EQ((long long)dbytes(), 0x3FF8000000000000LL);", "1.5 = 1.1b x 2^0: exponent 1023, mantissa 0x8...; memcpy keeps it byte-legal."),
            ("ctx callback counting", "counter_t *c = counter_create();@NL@counter_visit(c, bump_ctx_probe, &hits);@NL@counter_visit(c, bump_ctx_probe, &hits);@NL@CHECK_EQ(counter_count(c), 2);@NL@CHECK_EQ(hits, 2);", "fn runs once per visit; hits lives at file scope in your source and the ctx pointer carries it in."),
        ],
        level="mini-build",
    ),
    {
        "ca3-checkpoint-contracts": vi_challenge(
            "Kiểm tra: Hợp đồng con trỏ",
            "Có sẵn `static double dvals[4] = {1.5, 0, 0, 0};`. Cài span(), dbytes() (memcpy 8 byte của dvals[0]), và counter opaque với visit qua ctx.",
            [
                ("khoảng gồm điểm cuối", "4 con trỏ phần tử cộng một-vị-trí-sau-cuối."),
                ("bit của 1.5", "1.5 = 1.1b x 2^0: số mũ 1023, định trị 0x8...; memcpy giữ phép đọc theo byte hợp lệ."),
                ("đếm qua ctx", "fn chạy đúng một lần mỗi visit; ctx mang trạng thái của caller."),
            ],
        )
    },
    solution=C_PRELUDE
    + "#include <string.h>@NL@"
    + "static double dvals[4] = {1.5, 0, 0, 0};@NL@"
    + "size_t span(void) { return 5; }@NL@"
    + "unsigned long long dbytes(void) {@NL@    unsigned long long u = 0;@NL@    memcpy(&u, &dvals[0], sizeof u);@NL@    return u;@NL@}@NL@"
    + "typedef struct counter { int n; } counter_t;@NL@"
    + "counter_t *counter_create(void) { counter_t *c = malloc(sizeof *c); c->n = 0; return c; }@NL@"
    + "void counter_visit(counter_t *c, void (*fn)(void *ctx), void *ctx) {@NL@    c->n++;@NL@    if (fn) fn(ctx);@NL@}@NL@"
    + "int counter_count(counter_t *c) { return c->n; }@NL@"
    + "static int hits = 0;@NL@"
    + "static void bump_ctx_probe(void *ctx) { (void)ctx; hits++; }@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "#include <string.h>@NL@"
    + "static double dvals[4] = {1.5, 0, 0, 0};@NL@"
    + "size_t span(void) { return 4; }@NL@"
    + "unsigned long long dbytes(void) { return *(unsigned long long *)&dvals[0]; }@NL@"
    + "typedef struct counter { int n; } counter_t;@NL@"
    + "counter_t *counter_create(void) { counter_t *c = malloc(sizeof *c); c->n = 0; return c; }@NL@"
    + "void counter_visit(counter_t *c, void (*fn)(void *ctx), void *ctx) { (void)ctx; if (fn) fn(0); }@NL@"
    + "int counter_count(counter_t *c) { return c->n; }@NL@"
    + "static int hits = 0;@NL@"
    + "static void bump_ctx_probe(void *ctx) { (void)ctx; hits++; }@NL@"
    + "int main(void) { return 0; }",
)

# ======================= MODULE 4: ca-ub-optimizer ==========================
M4 = "ca-ub-optimizer"

L4A = "ca-ub-taxonomy"
L4B = "ca-optimizer-assumptions"
L4C = "ca-ub-tooling"
L4CP = "ca-checkpoint-m4"

write_module(
    M4,
    "Undefined Behavior and the Optimizer",
    "The UB catalog that matters, how optimization exploits its absence, and the discipline of making UB detectable instead of assumed.",
    "Hành vi không định nghĩa và trình tối ưu hóa",
    "Danh mục UB quan trọng, cách tối ưu hóa lợi dụng sự vắng mặt của nó, và kỷ luật làm UB phát hiện được thay vì giả định.",
    [L4A, L4B, L4C, L4CP],
    ["ca-p4-ub"],
)

write_lesson(
    M4,
    L4A,
    "The UB Taxonomy That Matters",
    "Signed overflow, shifts, OOB, uninitialized reads, and lifetime violations — grouped by what the compiler may assume.",
    16,
    """
## The load-bearing categories

- **Signed arithmetic overflow** (`INT_MAX + 1`): the compiler may assume it never happens, so overflow-guard code written *after* the add can be deleted as dead.
- **Out-of-bounds access**: an OOB loop index licenses the compiler to assume the loop bound is large — bounds checks vanish.
- **Uninitialized reads**: an indeterminate value is not 'random garbage' — reading one is UB; the compiler may propagate anything.
- **Shift abuse**: shifting by >= width, or negative left operands, is UB; `1u << 32` on a 32-bit int is not 'wrap to 0'.
- **Lifetime violations**: use-after-free, use-after-scope, use-before-init.

## What UB is for

It is not malice: every category marks a place where the abstract machine stops constraining the implementation, letting optimizers reason about the *other* 99% of the program. The cost is that a bug in the 1% can invalidate proofs about everything.

## The professional response

You do not memorize the 200 rules; you know the load-bearing dozen above, and you make every one *detectable*: warning flags, checked arithmetic at boundaries, initialized-everywhere discipline, and the sanitizer runs of module 16.
""",
    "Phân loại UB quan trọng",
    "Tràn số có dấu, shift, truy cập ngoài biên, đọc chưa khởi tạo, vi phạm vòng đời — nhóm theo điều trình biên dịch được phép giả định.",
    """
## Các nhóm trụ cột

- **Tràn số có dấu** (`INT_MAX + 1`): trình biên dịch được giả định điều đó không xảy ra, nên code chặn tràn viết *sau* phép cộng có thể bị xóa như code chết.
- **Truy cập ngoài biên**: chỉ số vượt biên cho phép giả định vòng lặp đủ dài — kiểm tra biên biến mất.
- **Đọc chưa khởi tạo**: giá trị không xác định không phải 'rác ngẫu nhiên' — đọc là UB; trình biên dịch truyền gì cũng được.
- **Lạm dụng shift**: shift >= bề rộng, hoặc toán hạng trái âm, là UB; `1u << 32` trên int 32-bit không phải 'quay về 0'.
- **Vi phạm vòng đời**: dùng sau free, dùng sau khi hết phạm vi, dùng trước khởi tạo.

## UB tồn tại để làm gì

Không phải ác ý: mỗi nhóm đánh dấu chỗ máy trừu tượng ngừng ràng buộc hiện thực, cho phép tối ưu hóa suy luận về 99% còn lại của chương trình. Cái giá: một lỗi trong 1% có thể làm sập mọi chứng minh.

## Phản ứng chuyên nghiệp

Bạn không học thuộc 200 luật; bạn biết chục luật trụ cột trên và biến mỗi luật thành *phát hiện được*: cờ cảnh báo, số học có kiểm tra tại biên, kỷ luật khởi tạo mọi nơi, và các lần chạy sanitizer ở mô-đun 16.
""",
)

write_lesson(
    M4,
    L4B,
    "How Optimizers Exploit UB",
    "Dead-store elimination, branch deletion, and folding — watched on real computations.",
    15,
    """
## The guarantee you build on

Observable behavior — reads of volatile objects, writes to files, calls to I/O functions — must be preserved exactly. Everything not observable may be reordered, merged, or deleted *provided the observable results are unchanged*. UB anywhere removes the 'provided'.

## Folding in practice

```c
int folded(void)     { int a = 21; int b = 2; return a * b; }
int unfolded(void)   { volatile int a = 21; volatile int b = 2; return a * b; }
```

At -O2 the first returns the constant 42 without executing a multiply; the second must load, multiply, and store at runtime. Same observable result — that is the contract working.

## Why guards disappear

```c
if (p != NULL && *p > 0) use(*p);
```

The null check survives because dereferencing NULL is UB *only if it happens* — here it is guarded. But a write `*p = 1` earlier in the function without a check licenses the optimizer to delete a *later* `p != NULL` test: a null pointer cannot have been dereferenced, so either p is not null or the program is already meaningless. Learning to *see* these deletions in disassembly (module 13) is what makes the rule concrete.
""",
    "Trình tối ưu hóa lợi dụng UB thế nào",
    "Loại bỏ ghi chết, xóa nhánh, gập hằng — quan sát trên phép tính thật.",
    """
## Bảo đảm bạn xây dựng trên đó

Hành vi quan sát được — đọc volatile, ghi file, gọi hàm I/O — phải được giữ nguyên xác. Mọi thứ không quan sát được được sắp xếp lại, gộp, hoặc xóa *miễn là kết quả quan sát được không đổi*. UB ở bất kỳ đâu xóa bỏ chữ 'miễn là'.

## Gập hằng trong thực tế

```c
int folded(void)     { int a = 21; int b = 2; return a * b; }
int unfolded(void)   { volatile int a = 21; volatile int b = 2; return a * b; }
```

Ở -O2 hàm đầu trả hằng 42 không cần lệnh nhân; hàm hai phải load, nhân, store lúc chạy. Kết quả quan sát được như nhau — hợp đồng đang hoạt động.

## Vì sao kiểm tra biến mất

Kiểm tra NULL sống sót vì hủy tham chiếu NULL chỉ là UB *nếu nó xảy ra* — ở đây có chặn. Nhưng một lệnh ghi `*p = 1` không kiểm tra trước đó cho phép trình tối ưu hóa xóa phép thử `p != NULL` về sau: con trỏ NULL không thể đã bị hủy tham chiếu. Học *nhìn thấy* các phép xóa này trong assembly (mô-đun 13) là lúc luật trở nên cụ thể.
""",
)

write_lesson(
    M4,
    L4C,
    "Making UB Detectable",
    "Warning discipline, checked arithmetic, and volatile as an observation tool — the habits before sanitizers.",
    14,
    """
## Warnings are UB radar

`-Wall -Wextra` catches a large share of the classic UB (uninitialized use, format mismatches, shifts). Promote them to errors in CI. A warning you ignore trains you to ignore warnings.

## Checked arithmetic at trust boundaries

Where untrusted sizes meet arithmetic, check *before* it happens:

```c
if (n > SIZE_MAX / sizeof *buf) return ENOMEM;   /* before the multiply */
buf = malloc(n * sizeof *buf);
```

Wraparound-safe idioms (unsigned modular arithmetic) are legitimate tools when the *domain* genuinely wraps — hash sums, counters. The skill is choosing deliberately, not by accident.

## volatile is a porthole, not a fix

Marking a variable volatile forces every read and write to actually happen — it defeats dead-store elimination and makes timing/order experiments honest. It does NOT make data races defined, does not provide atomicity, and is not a synchronization primitive. Race-free code needs atomics or locks (modules 19-20).
""",
    "Làm UB phát hiện được",
    "Kỷ luật cảnh báo, số học có kiểm tra, và volatile như công cụ quan sát — thói quen trước khi đến sanitizer.",
    """
## Cảnh báo là radar UB

`-Wall -Wextra` bắt phần lớn UB kinh điển (dùng chưa khởi tạo, sai format, shift). Nâng chúng thành lỗi trong CI. Cảnh báo bạn phớt lờ dạy bạn phớt lờ cảnh báo.

## Số học có kiểm tra tại biên tin cậy

Nơi kích thước không tin cậy gặp phép tính, kiểm tra *trước khi* nó xảy ra:

```c
if (n > SIZE_MAX / sizeof *buf) return ENOMEM;   /* trước phép nhân */
buf = malloc(n * sizeof *buf);
```

Các idiom an-toàn-tràn (số học modulo unsigned) là công cụ hợp lệ khi *miền* thực sự quay vòng — hash, bộ đếm. Kỹ năng là chọn có chủ đích, không tình cờ.

## volatile là cửa sổ quan sát, không phải sửa lỗi

Biến volatile ép mọi lần đọc/ghi phải xảy ra thật — đánh bại việc xóa ghi chết và làm các thí nghiệm thứ tự/khối lượng trung thực. Nó KHÔNG làm data race trở nên hợp lệ, không cung cấp tính nguyên tử, không phải primitve đồng bộ. Code không race cần atomics hoặc khóa (mô-đun 19-20).
""",
)

write_practice(
    M4,
    "ca-p4-ub",
    "UB and Optimizer Drills",
    "Executable UB probes: guarded vs unguarded, folding, wraparound domains, and detection discipline.",
    "Bài tập UB và trình tối ưu hóa",
    "Thăm dò UB chạy được: có chặn hay không, gập hằng, miền tràn ngược, và kỷ luật phát hiện.",
    L4A,
    22,
    "advanced",
    [
        challenge(
            "ca4-guarded-add",
            "Overflow Guard, Correctly Ordered",
            "Implement `int safe_add3(int a, int b, int *out)`: if a + b would overflow, return 0 and leave *out untouched; otherwise store the sum and return 1. The check must happen BEFORE any signed arithmetic that could overflow — use comparisons against INT_MAX/INT_MIN. Then implement `int naive_add3(int a, int b, int *out)` that just stores a + b (defined for the tested inputs, UB-adjacent by design).",
            "#include <limits.h>@NL@" + C_PRELUDE,
            [
                ("normal path", "int r = 99;@NL@CHECK_EQ(safe_add3(2, 3, &r), 1);@NL@CHECK_EQ(r, 5);", "Defined inputs store and return 1."),
                ("overflow rejected", "int r = 99;@NL@CHECK_EQ(safe_add3(INT_MAX, 1, &r), 0);@NL@CHECK_EQ(r, 99);", "The comparison guard fires before any add; *out is untouched."),
                ("negative edge", "int r = 99;@NL@CHECK_EQ(safe_add3(INT_MIN, -1, &r), 0);@NL@CHECK_EQ(r, 99);", "INT_MIN + (-1) overflows below; the guard must catch that side too."),
                ("naive exists", "int r = 99;@NL@naive_add3(2, 3, &r);@NL@CHECK_EQ(r, 5);", "The naive path works for in-range inputs — the lesson is that its correctness is conditional."),
            ],
            level="independent",
        ),
        challenge(
            "ca4-fold-probe",
            "Folding vs Runtime",
            "Implement `int folded_sq(int x)` returning x*x with locals; `int unfolded_sq(int x)` computing x*x through a volatile local; and `long long fold_penalty(int x)` returning the *number of multiplications* each must perform — implement it as folded_count - unfolded_count where folded_count is 0 (the multiply folds away) and unfolded_count is 1 (volatile forces the runtime multiply).",
            C_PRELUDE,
            [
                ("both compute", "CHECK_EQ(folded_sq(12), 144);@NL@CHECK_EQ(unfolded_sq(12), 144);", "Identical observable results — folding changes nothing semantically."),
                ("penalty is the load", "CHECK_EQ(fold_penalty(12), -1);", "folded does 0 runtime multiplies, unfolded does 1: 0 - 1 = -1."),
            ],
            level="guided",
        ),
        challenge(
            "ca4-wrap-domain",
            "Deliberate Wraparound",
            "Implement `unsigned int fnv1a_step(unsigned int h, unsigned char byte)` — one FNV-1a round: h ^= byte; h *= 16777619u. Unsigned overflow is *defined* modular arithmetic; this hash depends on it. Then implement `int mod16(int x)` returning x mod 16 for non-negative x using only unsigned reasoning (no % on negative signed values).",
            C_PRELUDE,
            [
                ("known FNV step", "CHECK_EQ(fnv1a_step(2166136261u, 0x61), 3826002220u);", "xor 0x61 into the offset basis, then multiply by 16777619 — defined modular 2^32."),
                ("wrap is deterministic", "unsigned int h = 4294967295u;@NL@h = fnv1a_step(h, 1);@NL@CHECK_EQ(h, 4261412058u);", "0xFFFFFFFF ^ 1 = 0xFFFFFFFE; times the prime mod 2^32 = 4261412058 — the same value every run, by definition."),
                ("mod without %", "CHECK_EQ(mod16(37), 5);@NL@CHECK_EQ(mod16(64), 0);", "x & 15 computes the same value as x % 16 for non-negative x."),
            ],
            level="combination",
        ),
        challenge(
            "ca4-uninit-discipline",
            "Initialize Everything",
            "Implement `int sum_known(const int *a, size_t n)` that totals the array — and if n is 0 returns 0. The trap: a wrong answer pattern is returning an uninitialized accumulator 'sometimes works'. Then implement `int *find_or_null(int *a, size_t n, int v)` returning the first match or NULL — the two functions together exercise init-discipline and null contracts.",
            C_PRELUDE,
            [
                ("empty sums to zero", "CHECK_EQ(sum_known(0, 0), 0);", "The accumulator must be initialized at declaration; the n==0 path proves it."),
                ("sums and finds", "int v[4] = {5, 6, 7, 8};@NL@CHECK_EQ(sum_known(v, 4), 26);@NL@CHECK_EQ(*find_or_null(v, 4, 7), 7);@NL@CHECK_NULL(find_or_null(v, 4, 42));", "Both contracts hold: totals and a NULL on miss."),
            ],
            level="independent",
        ),
        challenge(
            "ca4-volatile-order",
            "volatile Makes It Honest",
            "A file-scope `static volatile int ticks = 0;` is already in your editor. Implement `int bump_ticks(void)` (adds 1, returns the new value), `void reset_ticks(void)`, and `int ticks_between(void (*work)(void), int expected)` which resets, runs work(), and returns 1 iff ticks equals expected — proving every write actually happened because volatile forbids collapsing them.",
            C_PRELUDE + "static volatile int ticks = 0;@NL@",
            [
                ("writes are observed", "CHECK_EQ(bump_ticks(), 1);@NL@CHECK_EQ(bump_ticks(), 2);@NL@reset_ticks();@NL@CHECK_EQ(ticks, 0);", "Every increment really happens — volatile prevents store collapsing."),
                ("between works", "CHECK_EQ(ticks_between(bump_twice_probe, 2), 1);", "work() runs between reset and check; volatile makes the count trustworthy."),
                ("wrong expectation fails", "CHECK_EQ(ticks_between(bump_once_probe, 2), 0);", "The honest probe also reports the truth when the expectation is wrong."),
            ],
            level="combination",
        ),
    ],
    {
        "ca4-guarded-add": vi_challenge(
            "Chặn tràn đúng chỗ",
            "Cài safe_add3 — kiểm tra trước mọi phép tính có dấu có thể tràn — và naive_add3 để so sánh.",
            [
                ("đường thường", "Đầu vào hợp lệ: lưu và trả 1."),
                ("từ chối tràn", "Chặn so sánh kích hoạt trước phép cộng; *out không bị đụng."),
                ("biên âm", "INT_MIN + (-1) tràn xuống dưới; chặn phải bắt được cả phía đó."),
                ("naive tồn tại", "Đường naive đúng với đầu vào trong khoảng — bài học là tính đúng đắn của nó có điều kiện."),
            ],
        ),
        "ca4-fold-probe": vi_challenge(
            "Gập hằng đối trọng lúc chạy",
            "Cài folded_sq/unfolded_sq (qua volatile) và fold_penalty đếm số phép nhân lúc chạy của mỗi loại.",
            [
                ("cả hai ra đúng", "Kết quả quan sát được như nhau — gập hằng không đổi ngữ nghĩa."),
                ("phí là phép load", "folded làm 0 phép nhân lúc chạy, unfolded làm 1: 0 - 1 = -1."),
            ],
        ),
        "ca4-wrap-domain": vi_challenge(
            "Tràn ngược có chủ đích",
            "Cài một vòng FNV-1a (xor rồi nhân 16777619u) — hash này dựa vào tràn unsigned được định nghĩa — và mod16 không dùng % cho số âm.",
            [
                ("bước FNV đã biết", "Kết quả nhân được định nghĩa modulo 2^32; xác minh bước xor và phép nhân unsigned hợp lệ."),
                ("tràn tất định", "Tràn cho ra giá trị ổn định — hành vi được định nghĩa, mỗi lần chạy như nhau."),
                ("mod không cần %", "x & 15 cho cùng giá trị x % 16 với x không âm."),
            ],
        ),
        "ca4-uninit-discipline": vi_challenge(
            "Khởi tạo mọi nơi",
            "Cài sum_known (n=0 trả 0) và find_or_null (khớp đầu hoặc NULL) — kỷ luật khởi tạo và hợp đồng NULL.",
            [
                ("rỗng ra không", "Bộ tích lũy phải khởi tạo ngay khi khai báo; đường n==0 chứng minh điều đó."),
                ("cộng và tìm", "Cả hai hợp đồng: tổng đúng và NULL khi vắng."),
            ],
        ),
        "ca4-volatile-order": vi_challenge(
            "volatile làm cho trung thực",
            "Có sẵn `static volatile int ticks = 0;`. Cài bump_ticks, reset_ticks, và ticks_between(work, expected) xác minh mọi phép ghi đều xảy ra thật.",
            [
                ("ghi được quan sát", "Mỗi lần tăng thật sự xảy ra — volatile ngăn gộp các lệnh store."),
                ("between hoạt động", "work() chạy giữa reset và kiểm tra; volatile làm con số đáng tin."),
                ("kỳ vọng sai báo sai", "Probe trung thực cũng báo thật khi kỳ vọng sai."),
            ],
        ),
    },
    solutions=[
        (
            "ca4-guarded-add",
            "#include <limits.h>@NL@" + C_PRELUDE
            + "int safe_add3(int a, int b, int *out) {@NL@    if (b > 0 && a > INT_MAX - b) return 0;@NL@    if (b < 0 && a < INT_MIN - b) return 0;@NL@    *out = a + b;@NL@    return 1;@NL@}@NL@"
            + "int naive_add3(int a, int b, int *out) { *out = a + b; return 1; }@NL@"
            + "int main(void) { return 0; }",
            "#include <limits.h>@NL@" + C_PRELUDE
            + "int safe_add3(int a, int b, int *out) {@NL@    int s = a + b;@NL@    if (a > 0 && s < 0) return 0;@NL@    *out = s;@NL@    return 1;@NL@}@NL@"
            + "int naive_add3(int a, int b, int *out) { *out = a + b; return 1; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca4-fold-probe",
            C_PRELUDE
            + "int folded_sq(int x) { int y = x; return y * x; }@NL@"
            + "int unfolded_sq(int x) { volatile int y = x; return y * x; }@NL@"
            + "long long fold_penalty(int x) { (void)x; return 0 - 1; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int folded_sq(int x) { return x * x; }@NL@"
            + "int unfolded_sq(int x) { volatile int y = x; return y + x; }@NL@"
            + "long long fold_penalty(int x) { (void)x; return 1; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca4-wrap-domain",
            C_PRELUDE
            + "unsigned int fnv1a_step(unsigned int h, unsigned char byte) {@NL@    h ^= (unsigned int)byte;@NL@    h *= 16777619u;@NL@    return h;@NL@}@NL@"
            + "int mod16(int x) { return (int)((unsigned int)x & 15u); }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "unsigned int fnv1a_step(unsigned int h, unsigned char byte) {@NL@    h ^= (unsigned int)byte;@NL@    h += 16777619u;@NL@    return h;@NL@}@NL@"
            + "int mod16(int x) { return x % 16; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca4-uninit-discipline",
            C_PRELUDE
            + "int sum_known(const int *a, size_t n) {@NL@    int s = 0;@NL@    for (size_t i = 0; i < n; i++) s += a[i];@NL@    return s;@NL@}@NL@"
            + "int *find_or_null(int *a, size_t n, int v) {@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (a[i] == v) return &a[i];@NL@    }@NL@    return NULL;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int sum_known(const int *a, size_t n) {@NL@    int s;@NL@    for (size_t i = 0; i < n; i++) s += a[i];@NL@    return s;@NL@}@NL@"
            + "int *find_or_null(int *a, size_t n, int v) {@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (a[i] == v) return &a[i];@NL@    }@NL@    return NULL;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca4-volatile-order",
            C_PRELUDE
            + "static volatile int ticks = 0;@NL@"
            + "int bump_ticks(void) { ticks = ticks + 1; return ticks; }@NL@"
            + "void reset_ticks(void) { ticks = 0; }@NL@"
            + "int ticks_between(void (*work)(void), int expected) {@NL@    reset_ticks();@NL@    if (work) work();@NL@    return (ticks == expected) ? 1 : 0;@NL@}@NL@"
            + "static void bump_twice_probe(void) { bump_ticks(); bump_ticks(); }@NL@"
            + "static void bump_once_probe(void) { bump_ticks(); }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "static volatile int ticks = 0;@NL@"
            + "int bump_ticks(void) { ticks = ticks + 1; return ticks; }@NL@"
            + "void reset_ticks(void) { ticks = 0; }@NL@"
            + "int ticks_between(void (*work)(void), int expected) {@NL@    if (work) work();@NL@    reset_ticks();@NL@    return (ticks == expected) ? 1 : 0;@NL@}@NL@"
            + "static void bump_twice_probe(void) { bump_ticks(); bump_ticks(); }@NL@"
            + "static void bump_once_probe(void) { bump_ticks(); }@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M4,
    L4CP,
    "Checkpoint: Assume Nothing",
    "Consolidated UB-and-optimizer checkpoint.",
    12,
    """
Checkpoint for module 4: guard arithmetic before it can overflow, hash through *defined* wraparound, and verify an observation channel that volatile keeps honest.
""",
    "Kiểm tra: Không giả định gì",
    "Kiểm tra tổng hợp UB và trình tối ưu hóa.",
    """
Kiểm tra mô-đun 4: chặn phép tính trước khi nó có thể tràn, hash qua tràn ngược *được định nghĩa*, và xác minh kênh quan sát mà volatile giữ cho trung thực.
""",
)

write_checkpoint(
    M4,
    L4CP,
    "Checkpoint: Assume Nothing",
    "One program: an overflow-safe accumulator with a deliberate-wraparound hash, plus a volatile observation channel proving the optimizer did not fold your work away.",
    16,
    "See lesson.",
    "Kiểm tra: Không giả định gì",
    "Một chương trình: bộ tích lũy an-toàn-tràn với hash tràn ngược có chủ đích, và kênh quan sát volatile chứng minh trình tối ưu hóa không gập công việc của bạn.",
    "Xem bài học.",
    challenge(
        "ca4-checkpoint-safehash",
        "Checkpoint: Safe Accumulator + Honest Probe",
        "Implement three functions:@CE@ @CE@1. `int safe_accum(int init, const int *deltas, size_t n, int *out)` — repeatedly add each delta using your overflow-guard pattern; on any overflow return 0 leaving *out untouched; on success store the total and return 1.@CE@2. `unsigned int hash_span(const unsigned char *bytes, size_t n)` — FNV-1a over the bytes (offset basis 2166136261u, prime 16777619u) — defined wraparound by design.@CE@3. `int probe_kept(int (*work)(void), int expected)` — volatile file-scope `static int probe = 0;` is in your editor; reset it, run work(), return 1 iff probe == expected. work() itself increments probe.",
        C_PRELUDE + "static volatile int probe = 0;@NL@#include <limits.h>@NL@",
        [
            ("accumulator guards", "int out = 99;@NL@int d1[2] = {5, 7};@NL@CHECK_EQ(safe_accum(0, d1, 2, &out), 1);@NL@CHECK_EQ(out, 12);@NL@int d2[2] = {INT_MAX, 5};@NL@CHECK_EQ(safe_accum(0, d2, 2, &out), 0);@NL@CHECK_EQ(out, 12);", "Overflow mid-stream rejects and leaves *out at its last successful value."),
            ("hash wraps by design", "unsigned char msg[3] = {0x61, 0x62, 0x63};@NL@unsigned int h = hash_span(msg, 3);@NL@CHECK_EQ(hash_span(msg, 0), 2166136261u);@NL@CHECK_EQ(h != 2166136261u, 1);", "Empty span is the offset basis; hashing bytes advances through defined modular arithmetic."),
            ("probe stays honest", "CHECK_EQ(probe_kept(bump_probe_once, 1), 1);@NL@CHECK_EQ(probe_kept(bump_probe_twice, 3), 0);", "work runs after reset; the volatile counter reports exactly what ran."),
        ],
        level="mini-build",
    ),
    {
        "ca4-checkpoint-safehash": vi_challenge(
            "Kiểm tra: Bộ tích lũy an toàn + probe trung thực",
            "Cài safe_accum (chặn tràn, giữ *out khi từ chối), hash_span (FNV-1a, tràn được định nghĩa), và probe_kept (volatile probe).",
            [
                ("bộ tích lũy có chặn", "Tràn giữa đường sẽ từ chối và giữ *out ở giá trị thành công cuối."),
                ("hash tràn có chủ đích", "Span rỗng là offset basis; hash các byte đi qua số học modulo được định nghĩa."),
                ("probe trung thực", "work chạy sau reset; bộ đếm volatile báo đúng những gì đã chạy."),
            ],
        )
    },
    solution=C_PRELUDE
    + "#include <limits.h>@NL@"
    + "static volatile int probe = 0;@NL@"
    + "int safe_accum(int init, const int *deltas, size_t n, int *out) {@NL@    int acc = init;@NL@    for (size_t i = 0; i < n; i++) {@NL@        int d = deltas[i];@NL@        if (d > 0 && acc > INT_MAX - d) return 0;@NL@        if (d < 0 && acc < INT_MIN - d) return 0;@NL@        acc += d;@NL@    }@NL@    *out = acc;@NL@    return 1;@NL@}@NL@"
    + "unsigned int hash_span(const unsigned char *bytes, size_t n) {@NL@    unsigned int h = 2166136261u;@NL@    for (size_t i = 0; i < n; i++) {@NL@        h ^= (unsigned int)bytes[i];@NL@        h *= 16777619u;@NL@    }@NL@    return h;@NL@}@NL@"
    + "int probe_kept(int (*work)(void), int expected) {@NL@    probe = 0;@NL@    if (work) work();@NL@    return (probe == expected) ? 1 : 0;@NL@}@NL@"
    + "static int bump_probe_once(void) { probe = probe + 1; return probe; }@NL@"
    + "static int bump_probe_twice(void) { probe = probe + 1; probe = probe + 1; return probe; }@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "#include <limits.h>@NL@"
    + "static volatile int probe = 0;@NL@"
    + "int safe_accum(int init, const int *deltas, size_t n, int *out) {@NL@    int acc = init;@NL@    for (size_t i = 0; i < n; i++) acc += deltas[i];@NL@    *out = acc;@NL@    return 1;@NL@}@NL@"
    + "unsigned int hash_span(const unsigned char *bytes, size_t n) {@NL@    unsigned int h = 2166136261u;@NL@    for (size_t i = 0; i < n; i++) {@NL@        h += (unsigned int)bytes[i];@NL@        h *= 16777619u;@NL@    }@NL@    return h;@NL@}@NL@"
    + "int probe_kept(int (*work)(void), int expected) {@NL@    if (work) work();@NL@    probe = 0;@NL@    return (probe == expected) ? 1 : 0;@NL@}@NL@"
    + "static int bump_probe_once(void) { probe = probe + 1; return probe; }@NL@"
    + "static int bump_probe_twice(void) { probe = probe + 1; probe = probe + 1; return probe; }@NL@"
    + "int main(void) { return 0; }",
)
