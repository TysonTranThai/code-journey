#!/usr/bin/env python3
"""C — Intermediate — Module 2: cint-pointers.

Pointers as addresses, not syntax: arithmetic and one-past-the-end, the
four const placements and what each forbids, argv-style arrays of pointers.
House conventions: ISO C only, self-contained tests, Ws are behavioral
near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-pointers"

write_module(
    M,
    "Pointers as Addresses",
    "Pointer arithmetic with one-past-the-end, the four const placements, "
    "pointer-to-pointer, and arrays of pointers — the argv model.",
    "Con trỏ như địa chỉ",
    "Phép toán trên con trỏ với one-past-the-end, bốn vị trí của const, "
    "con trỏ đến con trỏ, và mảng con trỏ — mô hình argv.",
    lessons=["pointer-arithmetic", "const-correctness", "pointer-arrays", "cint-checkpoint-m2"],
    practices=["cint-p2-arithmetic", "cint-p2-const"],
)
print("module json done")

write_lesson(
    M, "pointer-arithmetic",
    "Pointer Arithmetic & One-Past-the-End",
    "What p + 1 really means, why one-past-the-end is legal but one-past-that is not, and the subtraction idiom.",
    15,
    r"""
## Scaling by the pointee

`p + 1` does not add one byte — it advances by `sizeof *p` **bytes**. For an
`int *` on this platform that is 4 bytes; for a `struct Big *`, maybe 64. The
compiler does the scaling; you do the reasoning:

```c
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;          /* points at arr[0] */
p + 3                  /* points at arr[3] */
*(p + 3)               /* 40 — the value there */
p[3]                   /* exactly the same thing: a[i] is *(a + i) */
```

The array-index operator is *defined* in terms of pointer arithmetic. That is
why `3[arr]` also compiles (it is `*(3 + arr)`) — legal, unforgettable once
seen, and never written on purpose.

## The one legal out-of-bounds pointer

C guarantees you may form a pointer **one past the end** of an array object.
You may compare with it and subtract from it, but you may **not dereference** it:

```c
int *end = arr + 5;    /* legal: one past the last element */
for (int *p = arr; p != end; p++) use(*p);   /* the classic walk */
*(arr + 5)             /* UB: dereferencing the one-past pointer */
arr + 6                /* UB: even forming it */
```

This is not pedantry: `<stdlib.h>`'s own conventions rely on it. Functions
returning "position" return `NULL` or an end pointer, and algorithms like
`qsort` reason in `[first, last)` half-open ranges — exactly this shape.

## Subtraction gives counts

```c
size_t n = (size_t)(end - start);   /* number of elements, not bytes */
```

Subtracting two pointers into the *same array* yields `ptrdiff_t`: how many
elements apart. Subtracting pointers into different objects is undefined.

## Walking with pointers instead of indices

```c
/* sum an array the pointer way — same machine result, different mental model */
int total = 0;
for (const int *p = arr, *end = arr + 5; p != end; ++p) total += *p;
```

Neither style is "faster" by definition. The pointer style generalizes to
structures where indices make no sense (linked lists, Module 9); the index
style resists off-by-one errors better in dense arrays. Choose per situation.

## Check your understanding

- `sizeof` an array of 7 `double` is 56; `arr + 3` advances how many bytes?
  (24.)
- Is `arr + 5` legal for a 5-element array? (Yes — one-past-the-end. Dereferencing
  it is not.)
- What is `*(arr + 2) == arr[2]`? (True by definition of `[]`.)
""",
    "Phép toán con trỏ & one-past-the-end",
    "`p + 1` thực sự nghĩa là gì, vì sao one-past-the-end hợp lệ nhưng one-past-that thì không, và mẫu trừ con trỏ.",
r"""
## Nhân theo kiểu của phần tử

`p + 1` không cộng một byte — nó tiến `sizeof *p` **byte**. Với `int *` trên
nền tảng này là 4 byte; với `struct Big *`, có thể 64. Compiler làm phép nhân;
bạn làm phần suy luận:

```c
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;          /* trỏ vào arr[0] */
p + 3                  /* trỏ vào arr[3] */
*(p + 3)               /* 40 — giá trị ở đó */
p[3]                   /* y hệt: a[i] là *(a + i) */
```

Toán tử chỉ số mảng được *định nghĩa* qua phép toán con trỏ. Vì vậy `3[arr]`
cũng biên dịch được (nó là `*(3 + arr)`) — hợp lệ, không thể quên khi đã thấy,
và không bao giờ cố tình viết.

## Con trỏ ngoài-biên hợp lệ duy nhất

C bảo đảm bạn có thể tạo con trỏ **trỏ đến ngay sau phần tử cuối** của mảng.
Bạn được so sánh và trừ với nó, nhưng **không được dereference**:

```c
int *end = arr + 5;    /* hợp lệ: sau phần tử cuối */
for (int *p = arr; p != end; p++) use(*p);   /* cách đi kinh điển */
*(arr + 5)             /* UB: dereference con trỏ one-past */
arr + 6                /* UB: tạo ra nó cũng là UB */
```

Đây không phải kiểu cách: chính quy ước của `<stdlib.h>` dựa vào nó. Hàm trả
"vị trí" trả `NULL` hoặc con trỏ cuối, và thuật toán như `qsort` suy luận trong
nửa-khoảng `[first, last)` — đúng hình dạng này.

## Phép trừ cho ra số phần tử

```c
size_t n = (size_t)(end - start);   /* số phần tử, không phải byte */
```

Trừ hai con trỏ vào *cùng một mảng* cho `ptrdiff_t`: chúng cách nhau bao nhiêu
phần tử. Trừ con trỏ của hai đối tượng khác nhau là undefined.

## Đi bằng con trỏ thay vì chỉ số

```c
/* tổng mảng theo kiểu con trỏ — cùng kết quả máy, khác mô hình tinh thần */
int total = 0;
for (const int *p = arr, *end = arr + 5; p != end; ++p) total += *p;
```

Không kiểu nào "nhanh hơn" một cách mặc định. Kiểu con trỏ tổng quát hóa cho
cấu trúc mà chỉ số vô nghĩa (danh sách liên kết, Module 9); kiểu chỉ số chống
lỗi off-by-one tốt hơn trong mảng dày. Chọn theo tình huống.

## Kiểm tra hiểu biết

- `sizeof` mảng 7 `double` là 56; `arr + 3` tiến bao nhiêu byte? (24.)
- `arr + 5` có hợp lệ với mảng 5 phần tử? (Có — one-past-the-end. Dereference
  thì không.)
- `*(arr + 2) == arr[2]`? (Đúng, theo định nghĩa của `[]`.)
"""
)

write_lesson(
    M, "const-correctness",
    "The Four Placements of `const`",
    "Read any const pointer declaration at sight, and design signatures that state exactly what may change.",
    14,
    r"""
## Read from the right

`const` binds to what is on its **left** (unless nothing is there — then to the
right). Four placements, four contracts:

```c
const int *p;         /* pointer to const int: *p read-only, p movable */
int const *p;         /* identical to the previous line */
int *const p;         /* const pointer to int: p fixed, *p writable */
const int *const p;   /* const pointer to const int: nothing movable */
```

A reading trick: sweep right-to-left. `int *const p` → "p is a const pointer
to int". `const int *p` → "p is a pointer to int-const".

## What each placement forbids — and does not

```c
int x = 1, y = 2;
const int *a = &x;
a = &y;               /* fine: the pointer itself moves */
*a = 5;               /* compile error: pointee is const */

int *const b = &x;
b = &y;               /* compile error: pointer is const */
*b = 5;               /* fine: pointee is writable */
```

**The guarantee is by type, not by reality.** `const int *p` promises *through
p* you will not write — it does not make the object immutable:

```c
int v = 7;
const int *spy = &v;
/* *spy = 9;            compile error */
v = 9;                 /* fine: v itself was never const */
```

## Signatures are where this pays

```c
size_t length(const char *s);        /* "I only read your string" */
int clamp(int *value, int lo, int hi); /* "I will write through this" */
const int *find(const int *a, size_t n, int key); /* read-only in, read-only out */
```

`const` in a parameter is a promise to your caller, checked by the compiler.
APIs that read data take pointers-to-const — every string function in the
standard library does (`strlen(const char *)`).

## Casting const away

`const int *` → `int *` via cast is legal syntax and undefined behavior **if
the object was defined const**. The honest uses are rare (interfacing with an
old API that lacks const). If you reach for it in new code, the signature is
wrong instead.

## Check your understanding

- `char *const argv0` vs `const char *argv0` — which can point somewhere else?
  (The first cannot; the second can.)
- Why does `strlen` take `const char *`? (It promises not to modify the string.)
""",
    "Bốn vị trí của `const`",
    "Đọc bất kỳ khai báo con trỏ const nào ngay lập tức, và thiết kế chữ ký nói rõ điều gì được phép thay đổi.",
r"""
## Đọc từ phải sang

`const` gắn với cái bên **trái** (trừ khi không có gì ở đó — thì sang phải).
Bốn vị trí, bốn hợp đồng:

```c
const int *p;         /* con trỏ đến int hằng: *p chỉ đọc, p di chuyển được */
int const *p;         /* giống hệt dòng trên */
int *const p;         /* con trỏ hằng đến int: p cố định, *p ghi được */
const int *const p;   /* con trỏ hằng đến int hằng: không gì di chuyển */
```

Mẹo đọc: quét phải-sang-trái. `int *const p` → "p là con trỏ hằng đến int".
`const int *p` → "p là con trỏ đến int-hằng".

## Mỗi vị trí cấm gì — và không cấm gì

```c
int x = 1, y = 2;
const int *a = &x;
a = &y;               /* được: con trỏ tự nó di chuyển */
*a = 5;               /* lỗi biên dịch: phần tử bị const */

int *const b = &x;
b = &y;               /* lỗi biên dịch: con trỏ bị const */
*b = 5;               /* được: phần tử ghi được */
```

**Lời bảo đảm là theo kiểu dữ liệu, không theo thực tế.** `const int *p` hứa
*qua p* bạn sẽ không ghi — nó không làm đối tượng bất biến:

```c
int v = 7;
const int *spy = &v;
/* *spy = 9;            lỗi biên dịch */
v = 9;                 /* được: bản thân v chưa bao giờ là const */
```

## Chữ ký là nơi điều này trả lương

```c
size_t length(const char *s);        /* "tôi chỉ đọc chuỗi của bạn" */
int clamp(int *value, int lo, int hi); /* "tôi sẽ ghi qua con trỏ này" */
const int *find(const int *a, size_t n, int key); /* đọc-only vào, đọc-only ra */
```

`const` trong tham số là lời hứa với người gọi, được compiler kiểm tra. API
đọc dữ liệu nhận con-trỏ-đến-const — mọi hàm chuỗi trong thư viện chuẩn đều
vậy (`strlen(const char *)`).

## Ép kiểu bỏ const

`const int *` → `int *` qua cast là cú pháp hợp lệ và là undefined behavior
**nếu đối tượng được định nghĩa là const**. Các dùng trung thực hiếm (giao
tiếp với API cũ thiếu const). Nếu bạn với tới cast này trong code mới, chữ ký
mới là thứ sai.

## Kiểm tra hiểu biết

- `char *const argv0` vs `const char *argv0` — cái nào được trỏ chỗ khác?
  (Cái đầu không được; cái hai được.)
- Vì sao `strlen` nhận `const char *`? (Nó hứa không sửa chuỗi.)
"""
)

write_lesson(
    M, "pointer-arrays",
    "Pointers to Pointers & Arrays of Pointers",
    "The argv model: an array of char pointers, out-parameters that return pointers, and two-level ownership.",
    16,
    r"""
## Two levels of indirection

`char **` means: follow me to a `char *`, follow that to a `char`. The iconic
example is `main`'s second parameter:

```c
int main(int argc, char **argv)   /* argv[i] is a char* — one string each */
```

`argv` is an array (here: a pointer to its first element) of pointers, each
pointing to a string. Drawing it is half of understanding it:

```
argv ──► [0] ──► "./program"
         [1] ──► "--verbose"
         [2] ──► NULL (conventionally argv[argc] == NULL)
```

Each string owns its own storage (from the OS); the array holds the addresses.

## Out-parameters that return pointers

The strongest everyday use of `char **` (or `T **`) is the **out-parameter**:
a function that wants to hand you a pointer must write through a pointer to
that pointer:

```c
/* try to allocate; return 1 and set *out on success */
int make_buffer(size_t n, char **out) {
    char *b = malloc(n);
    if (!b) return 0;
    *out = b;          /* write the pointer itself through the second level */
    return 1;
}
```

Why not return the pointer? Because you often need to signal failure *and*
produce a value. C has one return channel; the out-parameter is the second.
Module 3 pairs this with the ownership rule: `make_buffer`'s caller owns `*out`
and must `free` it.

## Modifying an array of pointers

```c
void sort_strings(char **tab, size_t n);   /* rearranges POINTERS, not chars */
```

Sorting an array of strings moves the `char *` values inside the array — the
string bytes never move. This is why `qsort` on `char *` tables is cheap and
why the compare function receives `char *const *` (pointers to the elements).

## The ownership ladder

Two levels means two ownership questions, always:
1. Who owns the array of pointers? (Frees the array itself.)
2. Who owns each pointed-to string? (Frees each.)

Different answers create different freeing loops. Module 3 turns this into a
checklist; Module 10 (hash tables) makes you live it.

## Check your understanding

- In `char *tab[4]`, what is `tab[i]`'s type? (`char *` — a single string.)
- To let a callee change which string `tab[0]` points to, what do you pass?
  (`&tab[0]`, i.e. a `char **`.)
""",
    "Con trỏ đến con trỏ & mảng con trỏ",
    "Mô hình argv: mảng các char pointer, out-parameter trả con trỏ, và quyền sở hữu hai tầng.",
r"""
## Hai tầng gián tiếp

`char **` nghĩa là: theo tôi đến một `char *`, theo tiếp đến `char`. Ví dụ
kinh điển là tham số thứ hai của `main`:

```c
int main(int argc, char **argv)   /* argv[i] là char* — mỗi cái một chuỗi */
```

`argv` là một mảng (ở đây: con trỏ đến phần tử đầu) gồm các con trỏ, mỗi con
trỏ trỏ vào một chuỗi. Vẽ nó ra là một nửa của việc hiểu:

```
argv ──► [0] ──► "./program"
         [1] ──► "--verbose"
         [2] ──► NULL (theo quy ước argv[argc] == NULL)
```

Mỗi chuỗi sở hữu bộ nhớ riêng (từ OS); mảng giữ các địa chỉ.

## Out-parameter trả con trỏ

Ứng dụng mạnh nhất hàng ngày của `char **` (hay `T **`) là **out-parameter**:
hàm muốn đưa cho bạn một con trỏ phải ghi qua con-trỏ-đến-con-trỏ:

```c
/* cố cấp phát; trả 1 và đặt *out khi thành công */
int make_buffer(size_t n, char **out) {
    char *b = malloc(n);
    if (!b) return 0;
    *out = b;          /* ghi chính con trỏ qua tầng thứ hai */
    return 1;
}
```

Vì sao không trả con trỏ trực tiếp? Vì bạn thường cần báo thất bại *và* tạo
giá trị. C có một kênh trả về; out-parameter là kênh thứ hai. Module 3 ghép
điều này với quy tắc sở hữu: caller của `make_buffer` sở hữu `*out` và phải
`free`.

## Sửa mảng con trỏ

```c
void sort_strings(char **tab, size_t n);   /* xáo các CON TRỎ, không phải các char */
```

Sắp xếp mảng chuỗi di chuyển các giá trị `char *` trong mảng — các byte của
chuỗi không bao giờ di chuyển. Vì vậy `qsort` trên bảng `char *` rẻ và vì sao
hàm so sánh nhận `char *const *` (con trỏ đến các phần tử).

## Bậc thang sở hữu

Hai tầng nghĩa là hai câu hỏi sở hữu, luôn luôn:
1. Ai sở hữu mảng con trỏ? (Free chính mảng.)
2. Ai sở hữu từng chuỗi được trỏ tới? (Free từng chuỗi.)

Câu trả lời khác nhau tạo ra các vòng free khác nhau. Module 3 biến điều này
thành checklist; Module 10 (hash table) bắt bạn sống với nó.

## Kiểm tra hiểu biết

- Trong `char *tab[4]`, kiểu của `tab[i]` là gì? (`char *` — một chuỗi.)
- Để callee thay đổi `tab[0]` trỏ vào đâu, bạn truyền gì? (`&tab[0]`, tức một
  `char **`.)
"""
)

# ---------------------------------------------------------------- practice 2a
P2A_CH = [
    challenge(
        "cint-p2-walk-sum",
        "Walk, Don't Index",
        """Implement two sums over an int array using ONLY pointer arithmetic —
no `[ ]` indexing anywhere in your implementation:

```c
long long sum_walk(const int *a, size_t n);      /* forward walk */
long long sum_reverse(const int *a, size_t n);   /* walk from one-past-end backwards */
```

Both return 0 for NULL or n == 0. Use `(a + n)` as the one-past-the-end pointer.""",
        C_PRELUDE,
        [
            (
                "forward and reverse walks",
                r"""
int a1[] = {1, 2, 3, 4};
CHECK_EQ(sum_walk(a1, 4), 10);
CHECK_EQ(sum_reverse(a1, 4), 10);
int a2[] = {5};
CHECK_EQ(sum_walk(a2, 1), 5);
CHECK_EQ(sum_walk(NULL, 0), 0);
CHECK_EQ(sum_reverse(NULL, 0), 0);
""",
                "for (const int *p = a, *e = a + n; p != e; ++p) — and start reverse from a + n going down to a.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p2-span",
        "Distance Between Pointers",
        """Implement range queries with pointer subtraction:

```c
/* returns how many elements lie in [lo, hi) of array a (n elements),
   where lo and hi are pointers INTO a (or hi == a + n). Invalid inputs
   (NULL, hi < lo, pointers outside the array's [a, a+n] range) return 0. */
size_t span(const int *a, size_t n, const int *lo, const int *hi);
```""",
        C_PRELUDE,
        [
            (
                "half-open span",
                r"""
int a[] = {0, 1, 2, 3, 4, 5};
CHECK_EQ(span(a, 6, a + 1, a + 4), 3);
CHECK_EQ(span(a, 6, a, a + 6), 6);
CHECK_EQ(span(a, 6, a + 3, a + 3), 0);
CHECK_EQ(span(a, 6, a + 4, a + 2), 0);   /* inverted */
CHECK_EQ(span(NULL, 0, NULL, NULL), 0);
""",
                "Validate: a != NULL, lo and hi within [a, a+n], lo <= hi. Then (size_t)(hi - lo).",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p2-const-sort-pair",
        "Read-Only In, Write Out",
        """Implement the const-discipline pair:

```c
/* returns a NEW heap array holding a's elements sorted ascending;
   a is never modified. Caller owns the result (frees it).
   Returns NULL for NULL input or allocation failure. */
int *sorted_copy(const int *a, size_t n);
/* returns 1 iff a is already sorted ascending */
int is_sorted(const int *a, size_t n);
```""",
        C_PRELUDE,
        [
            (
                "copy is sorted, original untouched",
                r"""
int src[] = {5, 1, 4, 2, 8};
int *cp = sorted_copy(src, 5);
CHECK_NOT_NULL(cp);
CHECK_EQ(cp[0], 1); CHECK_EQ(cp[4], 8);
CHECK_EQ(src[0], 5); CHECK_EQ(src[1], 1);   /* original untouched */
CHECK_EQ(is_sorted(src, 5), 0);
CHECK_EQ(is_sorted(cp, 5), 1);
free(cp);
CHECK_EQ(sorted_copy(NULL, 0), NULL);
""",
                "malloc n ints, memcpy, qsort with a comparator; const params keep src safe.",
            ),
            (
                "trivially sorted",
                r"""
int one[] = {42};
CHECK_EQ(is_sorted(one, 1), 1);
int two[] = {1, 2};
CHECK_EQ(is_sorted(two, 2), 1);
int bad[] = {2, 1};
CHECK_EQ(is_sorted(bad, 2), 0);
CHECK_EQ(is_sorted(NULL, 0), 1);
""",
                "Empty and single-element arrays are sorted.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p2-const-swap",
        "Swap Through Qualifiers",
        """Implement two swap variants that demonstrate the const contracts:

```c
void swap(int *x, int *y);                       /* ordinary swap */
int swap_if_sorted(const int **px, const int **py); /* if **px > **py, swap the
    POINTERS so *px ends up pointing at the smaller value; returns 1 if swapped */
```

`swap_if_sorted` takes pointers-to-pointers-to-const: it may move which pointer
points where, but never write through to the ints.""",
        C_PRELUDE,
        [
            (
                "values vs pointer reshuffle",
                r"""
int a = 2, b = 1;
swap(&a, &b);
CHECK_EQ(a, 1); CHECK_EQ(b, 2);
int c = 9, d = 4;                 /* fresh inverted pair for the pointer swap */
const int *pa = &c, *pb = &d;
int moved = swap_if_sorted(&pa, &pb);
CHECK_EQ(moved, 1);
CHECK_EQ(*pa, 4); CHECK_EQ(*pb, 9);   /* pointers now point small-first */
CHECK_EQ(c, 9); CHECK_EQ(d, 4);   /* the ints never changed */
""",
                "In swap_if_sorted: if (**px > **py) { const int *t = *px; *px = *py; *py = t; return 1; } return 0;",
            ),
        ],
        level="guided",
    ),
]
P2A_SOL = [
    (
        "cint-p2-walk-sum",
        r"""
long long sum_walk(const int *a, size_t n) {
    if (!a || n == 0) return 0;
    long long t = 0;
    for (const int *p = a, *e = a + n; p != e; ++p) t += *p;
    return t;
}
long long sum_reverse(const int *a, size_t n) {
    if (!a || n == 0) return 0;
    long long t = 0;
    for (const int *p = a + n; p != a; --p) t += *(p - 1);
    return t;
}""",
        r"""
long long sum_walk(const int *a, size_t n) {
    if (!a || n == 0) return 0;
    long long t = 0;
    for (size_t i = 0; i <= n; i++) t += a[i];   /* wrong: i <= n reads one past */
    return t;
}
long long sum_reverse(const int *a, size_t n) {
    (void)a; (void)n;
    return 0;   /* wrong: not implemented */
}""",
    ),
    (
        "cint-p2-span",
        r"""
size_t span(const int *a, size_t n, const int *lo, const int *hi) {
    if (!a || !lo || !hi || n == 0) return 0;
    const int *first = a, *onepast = a + n;
    if (lo < first || hi < first || lo > onepast || hi > onepast) return 0;
    if (hi < lo) return 0;
    return (size_t)(hi - lo);
}""",
        r"""
size_t span(const int *a, size_t n, const int *lo, const int *hi) {
    if (!a || !lo || !hi || n == 0) return 0;
    if (hi < lo) return 0;
    return (size_t)(hi - lo) + 1;   /* wrong: inclusive length, not half-open */
}""",
    ),
    (
        "cint-p2-const-sort-pair",
        r"""
static int cmp_int(const void *x, const void *y) {
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}
int *sorted_copy(const int *a, size_t n) {
    if (!a || n == 0) return NULL;
    int *cp = malloc(n * sizeof(int));
    if (!cp) return NULL;
    for (size_t i = 0; i < n; i++) cp[i] = a[i];
    qsort(cp, n, sizeof(int), cmp_int);
    return cp;
}
int is_sorted(const int *a, size_t n) {
    if (!a) return 1;
    for (size_t i = 1; i < n; i++)
        if (a[i - 1] > a[i]) return 0;
    return 1;
}""",
        r"""
static int cmp_int(const void *x, const void *y) {
    return *(const int *)x - *(const int *)y;   /* wrong: overflows on extremes */
}
int *sorted_copy(const int *a, size_t n) {
    if (!a || n == 0) return NULL;
    int *cp = malloc(n * sizeof(int));
    if (!cp) return NULL;
    for (size_t i = 0; i < n; i++) cp[i] = a[i];
    qsort(cp, n, sizeof(int), cmp_int);
    return cp;
}
int is_sorted(const int *a, size_t n) {
    (void)a; (void)n;
    return 1;   /* wrong: always claims sorted */
}""",
    ),
    (
        "cint-p2-const-swap",
        r"""
void swap(int *x, int *y) {
    int t = *x; *x = *y; *y = t;
}
int swap_if_sorted(const int **px, const int **py) {
    if (!px || !py || !*px || !*py) return 0;
    if (**px > **py) {
        const int *t = *px;
        *px = *py;
        *py = t;
        return 1;
    }
    return 0;
}""",
        r"""
void swap(int *x, int *y) {
    int t = *x; *x = *y; *y = t;
}
int swap_if_sorted(const int **px, const int **py) {
    if (!px || !py || !*px || !*py) return 0;
    if (**px > **py) {
        /* wrong: writes through to the ints (which are const here) */
        int x = **px, y = **py;
        *(*px) = y;   /* compile-error bait removed: cast instead */
        *(int *)*px = y;
        *(int *)*py = x;
        return 1;
    }
    return 0;
}""",
    ),
]
write_practice(
    M, "cint-p2-arithmetic",
    "Address Walking Gym",
    "Pointer arithmetic under exam conditions: one-past-the-end, subtraction, walking.",
    "Phòng gym đi địa chỉ",
    "Phép toán con trỏ trong điều kiện thi: one-past-the-end, trừ con trỏ, đi bộ.",
    after_lesson="pointer-arithmetic",
    minutes=24,
    difficulty="intermediate",
    challenges=P2A_CH,
    vi_challenges={
        "cint-p2-walk-sum": vi_challenge(
            "Đi bộ, đừng dùng chỉ số",
            "Cài hai hàm tổng chỉ dùng phép toán con trỏ, không dùng dấu [ ].",
            [("đi tới và đi lùi", "for (const int *p = a, *e = a + n; p != e; ++p) — và lùi từ a + n về a.")],
        ),
        "cint-p2-span": vi_challenge(
            "Khoảng cách giữa hai con trỏ",
            "Cài `span` trả số phần tử trong [lo, hi), kiểm tra tính hợp lệ của con trỏ.",
            [("nửa khoảng", "Kiểm tra a != NULL, lo/hi nằm trong [a, a+n], lo <= hi. Rồi (size_t)(hi - lo).")],
        ),
        "cint-p2-const-sort-pair": vi_challenge(
            "Đọc-only vào, ghi ra bản sao",
            "Cài `sorted_copy` (bản sao heap đã sắp) và `is_sorted`; mảng gốc không bao giờ đổi.",
            [("bản sao đã sắp, gốc nguyên vẹn", "malloc, memcpy, qsort với comparator; tham số const giữ src an toàn.")],
        ),
        "cint-p2-const-swap": vi_challenge(
            "Đổi chỗ qua các qualifier",
            "Cài `swap` thường và `swap_if_sorted` đổi chỗ các CON TRỎ (không đổi int).",
            [("đổi giá trị vs xáo con trỏ", "swap_if_sorted đổi *px/*py, trả 1 nếu đã đổi.")],
        ),
    },
    solutions=P2A_SOL,
)

# ---------------------------------------------------------------- practice 2b
P2B_CH = [
    challenge(
        "cint-p2-string-table",
        "The argv Model",
        """Work with an array of strings the way `main` does:

```c
/* returns the total number of characters across all strings in tab
   (n entries; a NULL entry counts 0 and stops nothing). */
size_t total_chars(char *const *tab, size_t n);
/* finds the longest string's INDEX (first wins ties); -1 if none. */
long longest_index(char *const *tab, size_t n);
```""",
        C_PRELUDE,
        [
            (
                "array of pointers traversal",
                r"""
char *tab[] = {"alpha", "be", "gamma!"};
CHECK_EQ(total_chars(tab, 3), 13);
CHECK_EQ(longest_index(tab, 3), 2);
char *t2[] = {"aa", "bb"};
CHECK_EQ(longest_index(t2, 2), 0);   /* tie: first wins */
char *t3[] = {NULL, "x"};
CHECK_EQ(total_chars(t3, 2), 1);
CHECK_EQ(total_chars(NULL, 0), 0);
CHECK_EQ(longest_index(NULL, 0), -1);
""",
                "Walk i in [0,n): strlen(tab[i]) summed; longest tracks best index.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p2-out-param",
        "Return a Pointer via `T **`",
        """Implement the out-parameter pair:

```c
/* allocates n+1 bytes, copies s, NUL-terminates; sets *out.
   Returns 1 on success, 0 on any failure (NULL args, malloc fail). */
int str_dup(const char *s, char **out);
/* frees *out and sets *out to NULL (so double-free becomes a no-op);
   returns 1 if there was something to free, 0 otherwise. */
int str_release(char **out);
```""",
        C_PRELUDE,
        [
            (
                "dup and safe release",
                r"""
char *copy = NULL;
CHECK_EQ(str_dup("hello", &copy), 1);
CHECK_STR_EQ(copy, "hello");
CHECK_EQ(str_release(&copy), 1);
CHECK_NULL(copy);
CHECK_EQ(str_release(&copy), 0);   /* already NULL: safe no-op */
CHECK_EQ(str_dup(NULL, &copy), 0);
""",
                "malloc(strlen(s)+1); memcpy; (*out)[len] = 0; free(*out) then *out = NULL.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p2-ptr-to-ptr",
        "The Second Level",
        """Demonstrate two-level indirection with a "cursor" API. The type is
provided in the boilerplate:

```c
typedef struct { const int *cur, *end; } IntCursor;
```

Implement:

```c
/* initializes the cursor over [a, a+n); NULL args leave it empty
   (cur == end == NULL). */
void cursor_init(IntCursor *c, const int *a, size_t n);
/* copies the next value into *out and advances; returns 1, or 0 when exhausted
   (leaving *out untouched). */
int cursor_next(IntCursor *c, int *out);
/* rewinds to the start of the original range (no-op if empty). */
void cursor_reset(IntCursor *c, const int *a, size_t n);
```""",
        C_PRELUDE + "\ntypedef struct { const int *cur, *end; } IntCursor;\n",
        [
            (
                "cursor protocol",
                r"""
int a[] = {10, 20, 30};
IntCursor c;
int v = -999;
cursor_init(&c, a, 3);
CHECK_EQ(cursor_next(&c, &v), 1); CHECK_EQ(v, 10);
CHECK_EQ(cursor_next(&c, &v), 1); CHECK_EQ(v, 20);
CHECK_EQ(cursor_next(&c, &v), 1); CHECK_EQ(v, 30);
CHECK_EQ(cursor_next(&c, &v), 0); CHECK_EQ(v, 30);   /* untouched on 0 */
cursor_reset(&c, a, 3);
CHECK_EQ(cursor_next(&c, &v), 1); CHECK_EQ(v, 10);
""",
                "cur/end pointers; next checks cur != end; reset restores both.",
            ),
        ],
        level="mini-build",
    ),
    challenge(
        "cint-p2-const-table",
        "Read-Only Table Queries",
        """Queries over a read-only table of C strings:

```c
/* returns 1 iff tab contains needle (strcmp equality). */
int table_contains(char *const *tab, size_t n, const char *needle);
/* returns the number of entries strictly shorter than len. NULL entries
   count as length 0. */
size_t count_shorter(char *const *tab, size_t n, size_t len);
```""",
        C_PRELUDE,
        [
            (
                "membership and length filter",
                r"""
char *tab[] = {"red", "green", "blue"};
CHECK_EQ(table_contains(tab, 3, "green"), 1);
CHECK_EQ(table_contains(tab, 3, "pink"), 0);
CHECK_EQ(table_contains(tab, 3, "ree"), 0);   /* substring of "red"? no such member */
CHECK_EQ(table_contains(NULL, 0, "red"), 0);
CHECK_EQ(count_shorter(tab, 3, 5), 2);   /* red(3) and blue(4) */
CHECK_EQ(count_shorter(tab, 3, 4), 1);   /* red(3) */
CHECK_EQ(count_shorter(tab, 3, 3), 0);
""",
                "strcmp == 0 for membership; strlen < len counted.",
            ),
        ],
        level="imitation",
    ),
]
P2B_SOL = [
    (
        "cint-p2-string-table",
        r"""
size_t total_chars(char *const *tab, size_t n) {
    if (!tab || n == 0) return 0;
    size_t t = 0;
    for (size_t i = 0; i < n; i++)
        if (tab[i]) t += strlen(tab[i]);
    return t;
}
long longest_index(char *const *tab, size_t n) {
    if (!tab || n == 0) return -1;
    long best = -1;
    size_t best_len = 0;
    for (long i = 0; i < (long)n; i++) {
        if (!tab[i]) continue;
        size_t L = strlen(tab[i]);
        if (L > best_len) { best_len = L; best = i; }
    }
    return best;
}""",
        r"""
size_t total_chars(char *const *tab, size_t n) {
    if (!tab || n == 0) return 0;
    size_t t = 0;
    for (size_t i = 0; i < n; i++)
        if (tab[i]) t += strlen(tab[i]);
    return t;
}
long longest_index(char *const *tab, size_t n) {
    if (!tab || n == 0) return -1;
    long best = -1;
    size_t best_len = 0;
    for (long i = 0; i < (long)n; i++) {
        if (!tab[i]) continue;
        size_t L = strlen(tab[i]);
        if (L >= best_len) { best_len = L; best = i; }   /* wrong: last wins ties */
    }
    return best;
}""",
    ),
    (
        "cint-p2-out-param",
        r"""
int str_dup(const char *s, char **out) {
    if (!s || !out) return 0;
    size_t n = strlen(s);
    char *b = malloc(n + 1);
    if (!b) return 0;
    memcpy(b, s, n + 1);
    *out = b;
    return 1;
}
int str_release(char **out) {
    if (!out) return 0;
    if (*out) { free(*out); *out = NULL; return 1; }
    return 0;
}""",
        r"""
int str_dup(const char *s, char **out) {
    if (!s || !out) return 0;
    size_t n = strlen(s);
    char *b = malloc(n);            /* wrong: no room for the NUL */
    if (!b) return 0;
    memcpy(b, s, n + 1);
    *out = b;
    return 1;
}
int str_release(char **out) {
    if (!out) return 0;
    if (*out) { free(*out); return 1; }   /* wrong: leaves dangling pointer */
    return 0;
}""",
    ),
    (
        "cint-p2-ptr-to-ptr",
        r"""
void cursor_init(IntCursor *c, const int *a, size_t n) {
    if (!c) return;
    if (!a) { c->cur = NULL; c->end = NULL; return; }
    c->cur = a;
    c->end = a + n;
}
int cursor_next(IntCursor *c, int *out) {
    if (!c || !out || !c->cur || c->cur == c->end) return 0;
    *out = *c->cur;
    c->cur++;
    return 1;
}
void cursor_reset(IntCursor *c, const int *a, size_t n) {
    cursor_init(c, a, n);
}""",
        r"""
void cursor_init(IntCursor *c, const int *a, size_t n) {
    if (!c) return;
    if (!a) { c->cur = NULL; c->end = NULL; return; }
    c->cur = a;
    c->end = a + n;
}
int cursor_next(IntCursor *c, int *out) {
    if (!c || !out || !c->cur || c->cur == c->end) return 0;
    *out = *c->cur;
    c->end--;   /* wrong: shrinks from the end instead of advancing cur */
    return 1;
}
void cursor_reset(IntCursor *c, const int *a, size_t n) {
    cursor_init(c, a, n);
}""",
    ),
    (
        "cint-p2-const-table",
        r"""
int table_contains(char *const *tab, size_t n, const char *needle) {
    if (!tab || !needle) return 0;
    for (size_t i = 0; i < n; i++)
        if (tab[i] && strcmp(tab[i], needle) == 0) return 1;
    return 0;
}
size_t count_shorter(char *const *tab, size_t n, size_t len) {
    if (!tab) return 0;
    size_t c = 0;
    for (size_t i = 0; i < n; i++) {
        size_t L = tab[i] ? strlen(tab[i]) : 0;
        if (L < len) c++;
    }
    return c;
}""",
        r"""
int table_contains(char *const *tab, size_t n, const char *needle) {
    if (!tab || !needle) return 0;
    for (size_t i = 0; i < n; i++)
        if (tab[i] && strstr(tab[i], needle) != NULL) return 1;   /* wrong: substring match */
    return 0;
}
size_t count_shorter(char *const *tab, size_t n, size_t len) {
    if (!tab) return 0;
    size_t c = 0;
    for (size_t i = 0; i < n; i++) {
        size_t L = tab[i] ? strlen(tab[i]) : 0;
        if (L < len) c++;
    }
    return c;
}""",
    ),
]
write_practice(
    M, "cint-p2-const",
    "Two-Level Indirection Gym",
    "Out-parameters, arrays of pointers, and the const contracts that keep them honest.",
    "Phòng gym gián tiếp hai tầng",
    "Out-parameter, mảng con trỏ, và các hợp đồng const giữ chúng trung thực.",
    after_lesson="pointer-arrays",
    minutes=26,
    difficulty="intermediate",
    challenges=P2B_CH,
    vi_challenges={
        "cint-p2-string-table": vi_challenge(
            "Mô hình argv",
            "Cài `total_chars` và `longest_index` (hòa: chọn chỉ số đầu).",
            [("duyệt mảng con trỏ", "strlen(tab[i]) cộng dồn; longest theo dõi chỉ số tốt nhất.")],
        ),
        "cint-p2-out-param": vi_challenge(
            "Trả con trỏ qua `T **`",
            "Cài `str_dup` và `str_release` (free rồi đặt NULL để double-free thành no-op).",
            [("dup và giải phóng an toàn", "malloc(strlen+1); memcpy; free(*out) rồi *out = NULL.")],
        ),
        "cint-p2-ptr-to-ptr": vi_challenge(
            "Tầng thứ hai",
            "Cài cursor: init/next/reset với con trỏ cur/end.",
            [("giao thức cursor", "next kiểm tra cur != end; reset khôi phục cả hai.")],
        ),
        "cint-p2-const-table": vi_challenge(
            "Truy vấn bảng chỉ-đọc",
            "Cài `table_contains` (strcmp đúng bằng) và `count_shorter`.",
            [("thành viên và lọc độ dài", "strcmp == 0 cho membership; strlen < len được đếm.")],
        ),
    },
    solutions=P2B_SOL,
)

# ---------------------------------------------------------------- checkpoint
CP_CH = challenge(
    "cint-checkpoint-m2-task",
    "Checkpoint: Pointer Forensics",
    """Given the pointer model below, implement the analyzer:

```c
/* a[] has n elements; lo, hi are pointers claimed to be inside [a, a+n].
   Return:
     0  if lo..hi form a valid ascending run (each element > previous),
    -1  if any input is invalid (NULL a; lo or hi outside [a, a+n]; hi < lo),
     1  if the run is valid range but not strictly ascending,
     2  if the run contains exactly one element. */
int run_classify(const int *a, size_t n, const int *lo, const int *hi);
```""",
    C_PRELUDE,
    [
        (
            "forensic verdicts",
            r"""
int a[] = {1, 3, 3, 7, 9};
int ascending[] = {1, 2, 3, 7, 9};
CHECK_EQ(run_classify(ascending, 5, ascending, ascending + 5), 0);
CHECK_EQ(run_classify(a, 5, a + 2, a + 4), 0);   /* 3,7 strictly ascending */
CHECK_EQ(run_classify(a, 5, a + 1, a + 3), 1);   /* 3,3 not strictly ascending */
CHECK_EQ(run_classify(a, 5, a, a + 1), 2);
CHECK_EQ(run_classify(a, 5, a + 4, a + 2), -1);
CHECK_EQ(run_classify(NULL, 0, NULL, NULL), -1);
""",
            "Validate bounds first (one-past allowed for hi), then compare elements in [lo, hi).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)
CP_VI = vi_challenge(
    "Kiểm tra: Pháp y con trỏ",
    "Cài `run_classify` phân loại đoạn [lo, hi) của mảng: 0 tăng nghiêm ngặt, -1 không hợp lệ, 1 hợp lệ nhưng không tăng nghiêm ngặt, 2 đúng một phần tử.",
    [("phán quyết pháp y", "Kiểm tra biên trước (one-past được phép cho hi), rồi so sánh phần tử trong [lo, hi).")],
)
write_checkpoint(
    M, "cint-checkpoint-m2",
    "Checkpoint: Pointers as Addresses",
    "Prove you can reason about bounds, const contracts, and two-level indirection before memory management.",
    20,
    r"""
## What you just proved

- One-past-the-end reasoning under pressure (bounds validation with `hi == a + n` allowed).
- Half-open ranges as the native shape of pointer algorithms.
- Const as a machine-checked contract, including pointer-reshuffling vs value-writing.
- The `T **` out-parameter protocol.

Module 3: who owns the memory behind the pointer, and what happens when that
question goes unanswered.
""",
    "Kiểm tra: Con trỏ như địa chỉ",
    "Chứng minh bạn suy luận được biên, hợp đồng const, và gián tiếp hai tầng trước khi vào quản lý bộ nhớ.",
    r"""
## Bạn vừa chứng minh điều gì

- Suy luận one-past-the-end dưới áp lực (kiểm tra biên cho phép `hi == a + n`).
- Nửa-khoảng là hình dạng tự nhiên của thuật toán con trỏ.
- Const là hợp đồng được máy kiểm tra, gồm xáo con trỏ vs ghi giá trị.
- Giao thức out-parameter `T **`.

Module 3: ai sở hữu bộ nhớ sau con trỏ, và điều gì xảy ra khi câu hỏi đó không
được trả lời.
""",
    CP_CH,
    CP_VI,
    solution=r"""
int run_classify(const int *a, size_t n, const int *lo, const int *hi) {
    if (!a || !lo || !hi || n == 0) return -1;
    const int *first = a, *onepast = a + n;
    if (lo < first || hi < first || lo > onepast || hi > onepast) return -1;
    if (hi < lo) return -1;
    size_t len = (size_t)(hi - lo);
    if (len == 1) return 2;
    for (const int *p = lo + 1; p < hi; p++)
        if (*(p - 1) >= *p) return 1;
    return 0;
}""",
    wrong=r"""
int run_classify(const int *a, size_t n, const int *lo, const int *hi) {
    if (!a || !lo || !hi || n == 0) return -1;
    const int *first = a, *onepast = a + n;
    if (lo < first || hi < first || lo > onepast || hi > onepast) return -1;
    if (hi < lo) return -1;
    size_t len = (size_t)(hi - lo);
    if (len == 1) return 2;
    for (const int *p = lo + 1; p < hi; p++)
        if (*(p - 1) > *p) return 1;   /* wrong: allows equal (not strict) */
    return 0;
}""",
)

print("module 2 complete")
