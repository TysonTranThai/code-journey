#!/usr/bin/env python3
"""C Beginner — batch 7: modules 13 (dynamic-memory) and 14 (structs)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ======================== MODULE 13: dynamic-memory =========================
M13 = "dynamic-memory"

L13A = "stack-vs-heap"
L13B = "malloc-free"
L13C = "calloc-realloc"
L13D = "ownership-errors"
L13E = "cb-checkpoint-m13"

write_module(
    M13,
    "Dynamic Memory",
    "malloc, calloc, realloc, free — and the ownership discipline that keeps heap programs alive.",
    "Bộ nhớ động",
    "malloc, calloc, realloc, free — và kỷ luật sở hữu giữ cho chương trình heap sống sót.",
    [L13A, L13B, L13C, L13D, L13E],
    ["cb-p13-alloc", "cb-p13-own"],
)

write_lesson(
    M13,
    L13A,
    "Stack vs Heap",
    "Two memories, two lifetimes: automatic locals vs allocations you control.",
    13,
    r"""
## The stack: automatic and fast

Function locals live on the **stack**. When the function returns, that memory
is reclaimed automatically:

```c
void f(void) {
    int a[100];        // lives until f returns
}                      // gone — no cleanup code written by you
```

Fast, but two limits: the size must be known at compile time, and the memory
dies with the function.

## The heap: manual and flexible

The **heap** holds memory you request at runtime with `malloc` and release
yourself with `free`:

```c
#include <stdlib.h>

int *p = malloc(10 * sizeof(int));   // ask for room for 10 ints
// ... p stays valid across function boundaries ...
free(p);                             // YOU give it back
```

Heap memory survives until you free it — it can outlive the function that
created it.

## The one rule that follows you forever

> If you allocated it, you own it: someone must free it exactly once.

- forget to free → **memory leak**
- free twice → undefined behavior (heap corruption)
- use after free → undefined behavior

Modules ahead (file I/O, data structures) build directly on this rule.
""",
    "Ngăn xếp vs Đống",
    "Hai vùng nhớ, hai vòng đời: biến cục bộ tự động vs vùng cấp phát bạn tự kiểm soát.",
    r"""
## Ngăn xếp: tự động và nhanh

Biến cục bộ sống trên **ngăn xếp** (stack). Khi hàm trả về, vùng nhớ đó được
thu hồi tự động:

```c
void f(void) {
    int a[100];        // sống tới khi f kết thúc
}                      // biến mất — bạn không viết code dọn dẹp
```

Nhanh, nhưng có hai giới hạn: kích thước phải biết lúc biên dịch, và vùng nhớ
chết theo hàm.

## Đống: thủ công và linh hoạt

**Đống** (heap) chứa vùng nhớ bạn xin tại thời điểm chạy bằng `malloc` và tự
trả bằng `free`:

```c
#include <stdlib.h>

int *p = malloc(10 * sizeof(int));   // xin chỗ cho 10 int
// ... p vẫn hợp lệ qua ranh giới hàm ...
free(p);                             // BẠN trả lại
```

Vùng nhớ heap sống tới khi bạn free — nó có thể sống lâu hơn hàm tạo ra nó.

## Một quy tắc theo bạn mãi mãi

> Nếu bạn cấp phát nó, bạn sở hữu nó: phải có ai đó free đúng một lần.

- quên free → **rò rỉ bộ nhớ**
- free hai lần → hành vi không xác định (hỏng heap)
- dùng sau khi free → hành vi không xác định

Các module phía sau (file I/O, cấu trúc dữ liệu) xây trực tiếp trên quy tắc
này.
""",
)

write_lesson(
    M13,
    L13B,
    "malloc and free",
    "Requesting memory, checking for failure, and releasing exactly once.",
    15,
    r"""
## The call

```c
int *p = malloc(n * sizeof(int));   // bytes, computed from the element type
```

`malloc` returns `void*` — assignment to `int*` converts implicitly. Always
multiply by `sizeof` the element type, never hardcode 4.

## Always check for failure

`malloc` returns `NULL` when it cannot satisfy the request (out of memory, or
an absurd size):

```c
int *p = malloc(n * sizeof(int));
if (p == NULL) {
    fprintf(stderr, "out of memory\n");
    return 1;
}
```

Un-checked malloc is how programs crash later, far from the cause.

## Exactly one free

```c
free(p);      // memory returned
p = NULL;     // now p cannot be used-after-free by accident
```

Free takes the pointer back to the START of the allocation — the pointer you
got from malloc, unchanged. Advancing it loses the address `free` needs:

```c
p++;          // legal to walk the array
free(p);      // WRONG — p no longer points at the allocation start
```

Keep the original pointer (or free a saved copy).

## After free

`p` still holds the old address but the memory is no longer yours — reading
or writing `*p` is undefined behavior. Setting `p = NULL` immediately after
free is a cheap, effective habit.
""",
    "malloc và free",
    "Xin vùng nhớ, kiểm tra thất bại, và trả lại đúng một lần.",
    r"""
## Lời gọi

```c
int *p = malloc(n * sizeof(int));   // theo BYTE, tính từ kiểu phần tử
```

`malloc` trả về `void*` — gán cho `int*` chuyển đổi ngầm. Luôn nhân với
`sizeof` kiểu phần tử, đừng hardcode số 4.

## Luôn kiểm tra thất bại

`malloc` trả về `NULL` khi không đáp ứng được yêu cầu (hết bộ nhớ, hoặc kích
thước vô lý):

```c
int *p = malloc(n * sizeof(int));
if (p == NULL) {
    fprintf(stderr, "out of memory\n");
    return 1;
}
```

malloc không kiểm tra là cách chương trình crash về sau, xa chỗ gây lỗi.

## Đúng một lần free

```c
free(p);      // trả lại bộ nhớ
p = NULL;     // giờ p không thể bị dùng-sau-free do sơ suất
```

free cần con trỏ trỏ về ĐẦU vùng cấp phát — con trỏ bạn nhận từ malloc, nguyên
vẹn. Tăng nó lên sẽ làm mất địa chỉ mà free cần:

```c
p++;          // đi bộ trên mảng thì hợp lệ
free(p);      // SAI — p không còn trỏ tới đầu vùng cấp phát
```

Giữ con trỏ gốc (hoặc free một bản sao đã lưu).

## Sau free

`p` vẫn giữ địa chỉ cũ nhưng bộ nhớ không còn của bạn — đọc hay ghi `*p` đều
là hành vi không xác định. Gán `p = NULL` ngay sau free là một thói quen rẻ
và hiệu quả.
""",
)

write_lesson(
    M13,
    L13C,
    "calloc and realloc",
    "Zero-filled allocation, and growing an array while keeping its contents.",
    13,
    r"""
## calloc: malloc + zero fill

```c
int *p = calloc(n, sizeof(int));   // n elements, EACH set to 0
```

Two differences from `malloc(n * sizeof(int))`: two arguments (count, size),
and every byte is zeroed. Choose calloc when "all zeros" is the state you
want; choose malloc when you will overwrite everything immediately.

## realloc: grow or shrink

```c
int *q = realloc(p, new_count * sizeof(int));
```

`realloc` may extend in place or move the block — if it moves, it COPIES the
old contents. Either way you get the block's new address.

## The realloc idiom — do not lose your only pointer

```c
int *tmp = realloc(p, m * sizeof(int));
if (tmp == NULL) {
    free(p);                 // old block is still valid; clean up
    return 1;
}
p = tmp;                     // success: adopt the new address
```

Assigning straight to `p` (`p = realloc(p, ...)`) is the classic bug: on
failure it returns NULL and the ORIGINAL address is lost — a leak with no way
to free.

## Growing a dynamic array

```c
int count = 0, cap = 4;
int *a = malloc(cap * sizeof(int));
// ... need more room ...
cap *= 2;
int *tmp = realloc(a, cap * sizeof(int));
if (tmp == NULL) { free(a); /* handle */ }
else a = tmp;
```

This grow-by-doubling pattern is the heart of every dynamic array you will
build in module 20.
""",
    "calloc và realloc",
    "Cấp phát phủ zero, và mở rộng mảng mà vẫn giữ được nội dung.",
    r"""
## calloc: malloc + phủ zero

```c
int *p = calloc(n, sizeof(int));   // n phần tử, MỖI phần tử bằng 0
```

Hai điểm khác `malloc(n * sizeof(int))`: hai đối số (số lượng, kích thước),
và mọi byte được đặt về 0. Chọn calloc khi "toàn zero" là trạng thái bạn muốn;
chọn malloc khi bạn sẽ ghi đè ngay lập tức.

## realloc: phóng to hoặc thu nhỏ

```c
int *q = realloc(p, new_count * sizeof(int));
```

`realloc` có thể mở rộng ngay tại chỗ hoặc dời khối — nếu dời, nó SAO CHÉP nội
dung cũ. Dù thế nào bạn cũng nhận địa chỉ mới của khối.

## Cách dùng realloc chuẩn — đừng đánh mất con trỏ duy nhất

```c
int *tmp = realloc(p, m * sizeof(int));
if (tmp == NULL) {
    free(p);                 // khối cũ vẫn hợp lệ; dọn dẹp
    return 1;
}
p = tmp;                     // thành công: nhận địa chỉ mới
```

Gán thẳng vào `p` (`p = realloc(p, ...)`) là lỗi kinh điển: khi thất bại nó
trả NULL và địa chỉ GỐC bị mất — rò rỉ không cách nào free.

## Mở rộng mảng động

```c
int count = 0, cap = 4;
int *a = malloc(cap * sizeof(int));
// ... cần thêm chỗ ...
cap *= 2;
int *tmp = realloc(a, cap * sizeof(int));
if (tmp == NULL) { free(a); /* xử lý */ }
else a = tmp;
```

Mẫu nhân đôi này là trái tim của mọi mảng động bạn sẽ dựng ở module 20.
""",
)

write_lesson(
    M13,
    L13D,
    "Ownership and the Classic Errors",
    "Leak, double free, use-after-free — recognizing all three on sight.",
    14,
    r"""
## Ownership in one line

Every allocation has exactly one owner — a function or module responsible for
freeing it. When you take ownership, you take the duty. When you hand it
over, you give up the right to free it yourself. Design functions so the
ownership story is obvious from the name:

- `create_*` / `alloc_*` → caller frees
- `*_destroy` / `*_free` → this function frees; don't double-free afterwards

## Leak

```c
void f(void) {
    int *p = malloc(8 * sizeof(int));
    if (cond) return;          // LEAK: p dies unfreed
    free(p);
}
```

Memory leaks rarely crash a program — they starve it slowly. Long-running
programs (servers!) die from accumulated leaks.

## Double free

```c
free(p);
free(p);        // undefined behavior — heap metadata corrupted
```

Set `p = NULL` after freeing; `free(NULL)` is defined and harmless.

## Use-after-free

```c
free(p);
*p = 5;         // undefined behavior — the block may already be reused
```

This is the most dangerous of the three: it can silently "work" in tests and
corrupt data in production.

## Reading them in the wild

None of these crash at the error site. The skill is recognizing the SHAPE:
a return/break path that skips free, two frees of one name, any use of a
name after its free. Training that eye is what the practice below is for.
""",
    "Sở hữu và các lỗi kinh điển",
    "Rò rỉ, double free, use-after-free — nhận ra cả ba chỉ bằng một cái nhìn.",
    r"""
## Sở hữu trong một dòng

Mỗi vùng cấp phát có đúng một chủ sở hữu — một hàm hoặc module chịu trách
nhiệm free. Khi bạn nhận sở hữu, bạn nhận nghĩa vụ. Khi bạn trao đi, bạn từ
bỏ quyền tự free. Thiết kế hàm để câu chuyện sở hữu hiện rõ từ chính tên gọi:

- `create_*` / `alloc_*` → người gọi free
- `*_destroy` / `*_free` → hàm này free; đừng free thêm lần nữa sau đó

## Rò rỉ (leak)

```c
void f(void) {
    int *p = malloc(8 * sizeof(int));
    if (cond) return;          // RÒ RỈ: p chết mà chưa free
    free(p);
}
```

Rò rỉ bộ nhớ hiếm khi làm crash chương trình — chúng bóp nghẹt từ từ. Các
chương trình chạy dài (server!) chết vì rò rỉ tích tụ.

## Double free

```c
free(p);
free(p);        // hành vi không xác định — hỏng metadata của heap
```

Gán `p = NULL` sau khi free; `free(NULL)` được định nghĩa và vô hại.

## Use-after-free

```c
free(p);
*p = 5;         // hành vi không xác định — khối có thể đã bị tái sử dụng
```

Đây là nguy hiểm nhất trong ba lỗi: nó có thể âm thầm "chạy đúng" trong test
và hỏng dữ liệu thật ở production.

## Nhận diện trong tự nhiên

Không lỗi nào crash ngay tại chỗ sai. Kỹ năng ở đây là nhận ra HÌNH DẠNG:
một nhánh return/break bỏ qua free, hai lần free cùng một tên, mọi lần dùng
tên đó sau khi free. Rèn con mắt đó chính là mục đích của phần luyện tập
dưới đây.
""",
)

write_practice(
    M13,
    "cb-p13-alloc",
    "Allocation Workbench",
    "malloc/calloc/realloc mechanics: fill, grow, and preserve.",
    "Bàn làm việc cấp phát",
    "Cơ chế malloc/calloc/realloc: đổ đầy, mở rộng, và bảo toàn.",
    L13C,
    18,
    "beginner",
    [
        challenge(
            "cb13-ints-1to-n",
            "Allocate 1..n",
            "Implement `int* ints_up_to(int n)` returning a heap-allocated array holding 1,2,...,n. Return NULL for n <= 0. The CALLER frees it.",
            C_PRELUDE,
            [
                ("values", "int *p = ints_up_to(4);\nCHECK_NOT_NULL(p);\nCHECK_EQ(p[0], 1);\nCHECK_EQ(p[3], 4);\nfree(p);", "malloc(4 * sizeof(int)) then fill in a loop."),
                ("n<=0 null", "CHECK_EQ(ints_up_to(0), NULL);", "Guard the nonsense size first."),
                ("negative null", "CHECK_EQ(ints_up_to(-3), NULL);", "Same guard covers negatives."),
            ],
            level="guided",
        ),
        challenge(
            "cb13-zeros",
            "Zeroed Buffer",
            "Implement `int* zero_buffer(int n)`: heap array of n ints where EVERY element is 0 (n >= 1 guaranteed). Return NULL if allocation fails.",
            C_PRELUDE,
            [
                ("zeros then sentinel", "int *p = zero_buffer(4);\nCHECK_NOT_NULL(p);\nCHECK_EQ(p[0], 0);\nCHECK_EQ(p[2], 0);\nCHECK_EQ(p[3], 1);\nfree(p);", "calloc zeroes everything; then set the LAST element to 1."),
                ("single", "int *p = zero_buffer(1);\nCHECK_EQ(p[0], 1);\nfree(p);", "n=1: the only element is the sentinel."),
            ],
            level="imitation",
        ),
        challenge(
            "cb13-grow-preserve",
            "Grow and Preserve",
            "A dynamic array grows by DOUBLING when full: implement `int* grow(int *old, int old_cap)` returning a new block of 2*old_cap ints whose first old_cap elements equal the old ones. Free nothing — the CALLER still owns old. Return NULL on failure.",
            C_PRELUDE,
            [
                ("contents preserved", "int *a = malloc(2 * sizeof(int));\na[0] = 7; a[1] = 8;\nint *b = grow(a, 2);\nCHECK_NOT_NULL(b);\nCHECK_EQ(b[0], 7);\nCHECK_EQ(b[1], 8);\nCHECK_EQ(b[3], 0);\nfree(a); free(b);", "realloc copies contents on move."),
                ("cap doubles", "int *a = malloc(1 * sizeof(int));\na[0] = 3;\nint *b = grow(a, 1);\nCHECK_NOT_NULL(b);\nCHECK_EQ(b[0], 3);\nfree(a); free(b);", "New capacity is 2*old_cap = 2."),
            ],
            level="independent",
        ),
        challenge(
            "cb13-sum-heap",
            "Heap Array Sum",
            "Implement `int heap_sum(const int *a, int n)` summing n elements of a heap array (n >= 0) — then, in the same file, a `main` is NOT needed: the harness provides it.",
            C_PRELUDE,
            [
                ("sums", "int *p = malloc(3 * sizeof(int));\np[0] = 4; p[1] = 5; p[2] = 6;\nCHECK_EQ(heap_sum(p, 3), 15);\nfree(p);", "Heap arrays index like any other."),
                ("empty", "int *p = malloc(sizeof(int));\nCHECK_EQ(heap_sum(p, 0), 0);\nfree(p);", "n=0 sums to 0."),
            ],
            level="imitation",
        ),
    ],
    {
        "cb13-ints-1to-n": vi_challenge(
            "Cấp phát 1..n",
            "Cài `int* ints_up_to(int n)` trả về mảng cấp phát trên heap chứa 1,2,...,n. Trả NULL cho n <= 0. NGƯỜI GỌI free.",
            [("giá trị", "malloc(4 * sizeof(int)) rồi đổ trong vòng lặp."), ("n<=0 là NULL", "Chặn kích thước vô lý trước."), ("số âm là NULL", "Cùng một lời chặn phủ số âm.")],
        ),
        "cb13-zeros": vi_challenge(
            "Bộ đệm zero",
            "Cài `int* zero_buffer(int n)`: mảng heap gồm n int mà MỌI phần tử bằng 0, TRỪ phần tử cuối bằng 1 (n >= 1). Trả NULL nếu cấp phát thất bại.",
            [("zero rồi cắm mốc", "calloc phủ zero; rồi đặt phần tử CUỐI thành 1."), ("một phần tử", "n=1: phần tử duy nhất chính là mốc.")],
        ),
        "cb13-grow-preserve": vi_challenge(
            "Mở rộng và bảo toàn",
            "Mảng động phóng to bằng cách NHÂN ĐÔI khi đầy: cài `int* grow(int *old, int old_cap)` trả về khối mới 2*old_cap int mà old_cap phần tử đầu bằng các phần tử cũ. Free không gì cả — NGƯỜI GỌI vẫn sở hữu old. Trả NULL khi thất bại.",
            [("nội dung được giữ", "realloc sao chép nội dung khi dời khối."), ("cap nhân đôi", "Dung lượng mới là 2*old_cap = 2.")],
        ),
        "cb13-sum-heap": vi_challenge(
            "Tổng mảng heap",
            "Cài `int heap_sum(const int *a, int n)` cộng n phần tử của mảng heap (n >= 0) — file không cần `main`: harness cung cấp.",
            [("cộng", "Mảng heap đánh chỉ số như mảng thường."), ("rỗng", "n=0 cộng ra 0.")],
        ),
    },
    solutions=[
        (
            "cb13-ints-1to-n",
            '#include <stdio.h>\n#include <stdlib.h>\nint* ints_up_to(int n) {\n    if (n <= 0) return NULL;\n    int *p = malloc(n * sizeof(int));\n    if (p == NULL) return NULL;\n    for (int i = 0; i < n; i++) p[i] = i + 1;\n    return p;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\nint* ints_up_to(int n) {\n    if (n <= 0) return NULL;\n    int *p = malloc(n * sizeof(int));\n    if (p == NULL) return NULL;\n    for (int i = 0; i < n; i++) p[i] = i;\n    return p;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb13-zeros",
            '#include <stdio.h>\n#include <stdlib.h>\nint* zero_buffer(int n) {\n    int *p = calloc(n, sizeof(int));\n    if (p == NULL) return NULL;\n    p[n - 1] = 1;\n    return p;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\nint* zero_buffer(int n) {\n    int *p = calloc(n, sizeof(int));\n    if (p == NULL) return NULL;\n    p[0] = 1;\n    return p;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb13-grow-preserve",
            '#include <stdio.h>\n#include <stdlib.h>\nint* grow(int *old, int old_cap) {\n    int *b = calloc(old_cap * 2, sizeof(int));\n    if (b == NULL) return NULL;\n    for (int i = 0; i < old_cap; i++) b[i] = old[i];\n    return b;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\nint* grow(int *old, int old_cap) {\n    return calloc(old_cap * 2, sizeof(int));\n}\nint main(void) { return 0; }',
        ),
        (
            "cb13-sum-heap",
            '#include <stdio.h>\n#include <stdlib.h>\nint heap_sum(const int *a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\nint heap_sum(const int *a, int n) {\n    int s = 0;\n    for (int i = 1; i < n; i++) s += a[i];\n    return s;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M13,
    "cb-p13-own",
    "Ownership Discipline",
    "NULL-checked allocation helpers and a cleanup function that frees exactly what it created.",
    "Kỷ luật sở hữu",
    "Hàm cấp phát có kiểm tra NULL và hàm dọn dẹp free đúng những gì nó tạo ra.",
    L13D,
    16,
    "beginner",
    [
        challenge(
            "cb13-xmalloc",
            "Checked Allocate",
            "Implement `int* checked_alloc(int n, int *ok)`: allocate n ints; on success set *ok=1 and return the block; on failure (n <= 0 or malloc NULL) set *ok=0 and return NULL.",
            C_PRELUDE,
            [
                ("success", "int ok = 0;\nint *p = checked_alloc(4, &ok);\nCHECK_EQ(ok, 1);\nCHECK_NOT_NULL(p);\nfree(p);", "Both outputs set on success."),
                ("bad n", "int ok = 1;\nint *p = checked_alloc(0, &ok);\nCHECK_EQ(ok, 0);\nCHECK_EQ(p, NULL);", "n=0 reports failure."),
                ("negative n", "int ok = 1;\nCHECK_EQ(checked_alloc(-2, &ok), NULL);\nCHECK_EQ(ok, 0);", "Negatives too."),
            ],
            level="independent",
        ),
        challenge(
            "cb13-free-all",
            "Cleanup All",
            "Implement `void cleanup(int *a, int *b, int *c)` freeing each NON-NULL pointer among the three. (free(NULL) is safe anyway — call free unconditionally if you prefer.)",
            C_PRELUDE,
            [
                ("frees all", "int *a = malloc(4), *b = malloc(4), *c = malloc(4);\ncleanup(a, b, c);\nCHECK_EQ(1, 1);", "No crash = correct frees."),
                ("some null", "int *a = malloc(4);\ncleanup(a, NULL, NULL);\nCHECK_EQ(1, 1);", "NULLs are tolerated."),
            ],
            level="guided",
        ),
        challenge(
            "cb13-transfer",
            "Ownership Transfer",
            "Implement `int* take(int **slot)` that returns the pointer currently in *slot and sets *slot to NULL — handing ownership to the caller without leaving a dangling alias.",
            C_PRELUDE,
            [
                ("handover", "int *p = malloc(4 * sizeof(int));\np[0] = 9;\nint *got = take(&p);\nCHECK_NOT_NULL(got);\nCHECK_EQ(got[0], 9);\nCHECK_EQ(p, NULL);\nfree(got);", "The old name becomes NULL."),
                ("empty slot", "int *p = NULL;\nCHECK_EQ(take(&p), NULL);", "Taking from NULL yields NULL."),
            ],
            level="independent",
        ),
    ],
    {
        "cb13-xmalloc": vi_challenge(
            "Cấp phát có kiểm tra",
            "Cài `int* checked_alloc(int n, int *ok)`: cấp phát n int; thành công thì đặt *ok=1 và trả khối; thất bại (n <= 0 hoặc malloc NULL) thì đặt *ok=0 và trả NULL.",
            [("thành công", "Cả hai đầu ra được đặt khi thành công."), ("n xấu", "n=0 báo thất bại."), ("n âm", "Số âm cũng vậy.")],
        ),
        "cb13-free-all": vi_challenge(
            "Dọn dẹp tất cả",
            "Cài `void cleanup(int *a, int *b, int *c)` free từng con trỏ KHÁC NULL trong ba con trỏ. (free(NULL) an toàn — gọi free vô điều kiện cũng được.)",
            [("free đủ", "Không crash = free đúng."), ("có NULL", "NULL được chấp nhận.")],
        ),
        "cb13-transfer": vi_challenge(
            "Chuyển giao sở hữu",
            "Cài `int* take(int **slot)` trả về con trỏ đang nằm trong *slot và đặt *slot thành NULL — trao sở hữu cho người gọi mà không để lại bí danh treo.",
            [("bàn giao", "Tên cũ thành NULL."), ("slot rỗng", "Lấy từ NULL cho ra NULL.")],
        ),
    },
    solutions=[
        (
            "cb13-xmalloc",
            '#include <stdio.h>\n#include <stdlib.h>\nint* checked_alloc(int n, int *ok) {\n    if (n <= 0) { *ok = 0; return NULL; }\n    int *p = malloc(n * sizeof(int));\n    if (p == NULL) { *ok = 0; return NULL; }\n    *ok = 1;\n    return p;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\nint* checked_alloc(int n, int *ok) {\n    if (n <= 0) { *ok = 1; return NULL; }\n    int *p = malloc(n * sizeof(int));\n    if (p == NULL) { *ok = 1; return NULL; }\n    *ok = 1;\n    return p;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb13-free-all",
            '#include <stdio.h>\n#include <stdlib.h>\nvoid cleanup(int *a, int *b, int *c) {\n    if (a != NULL) free(a);\n    if (b != NULL) free(b);\n    if (c != NULL) free(c);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\nvoid cleanup(int *a, int *b, int *c) {\n    if (a != NULL) free(a);\n    if (b != NULL) free(a);\n    if (c != NULL) free(c);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb13-transfer",
            '#include <stdio.h>\n#include <stdlib.h>\nint* take(int **slot) {\n    int *p = *slot;\n    *slot = NULL;\n    return p;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\nint* take(int **slot) {\n    int *p = *slot;\n    return p;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M13,
    L13E,
    "Checkpoint: Dynamic Memory",
    "Build a fill-and-scale dynamic array pair with NULL-checked allocation.",
    16,
    r"""
## Checkpoint

Allocation + ownership = the pattern behind every data structure to come.
""",
    "Điểm kiểm tra: Bộ nhớ động",
    "Dựng cặp hàm đổ-đầy-và-nhân của mảng động với cấp phát có kiểm tra NULL.",
    r"""
## Điểm kiểm tra

Cấp phát + sở hữu = mẫu nền của mọi cấu trúc dữ liệu sắp tới.
""",
    challenge(
        "cb13-checkpoint-fill-scale",
        "Fill Then Scale",
        "Implement `int* make_filled(int n)` returning a heap array of n ints filled with 1..n (NULL for n <= 0 or allocation failure), and `void scale_all(int *a, int n, int k)` multiplying each element by k.",
        C_PRELUDE,
        [
            ("filled", "int *p = make_filled(5);\nCHECK_NOT_NULL(p);\nCHECK_EQ(p[0], 1);\nCHECK_EQ(p[4], 5);\nfree(p);", "malloc, check NULL, fill."),
            ("bad size null", "CHECK_EQ(make_filled(0), NULL);", "Guard first."),
            ("scale", "int *p = make_filled(3);\nscale_all(p, 3, 10);\nCHECK_EQ(p[0], 10);\nCHECK_EQ(p[2], 30);\nfree(p);", "In-place multiply."),
            ("scale zero", "int *p = make_filled(2);\nscale_all(p, 2, 0);\nCHECK_EQ(p[1], 0);\nfree(p);", "k=0 zeroes."),
        ],
    ),
    vi_challenge(
        "Đổ đầy rồi nhân",
        "Cài `int* make_filled(int n)` trả về mảng heap gồm n int chứa 1..n (NULL cho n <= 0 hoặc cấp phát thất bại), và `void scale_all(int *a, int n, int k)` nhân mỗi phần tử với k.",
        [("đổ đầy", "malloc, kiểm tra NULL, đổ giá trị."), ("kích thước xấu là NULL", "Chặn trước."), ("nhân", "Nhân tại chỗ."), ("nhân 0", "k=0 đưa về 0.")],
    ),
    solution='#include <stdio.h>\n#include <stdlib.h>\nint* make_filled(int n) {\n    if (n <= 0) return NULL;\n    int *p = malloc(n * sizeof(int));\n    if (p == NULL) return NULL;\n    for (int i = 0; i < n; i++) p[i] = i + 1;\n    return p;\n}\nvoid scale_all(int *a, int n, int k) {\n    for (int i = 0; i < n; i++) a[i] *= k;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\n#include <stdlib.h>\nint* make_filled(int n) {\n    if (n <= 0) return NULL;\n    int *p = malloc(n * sizeof(int));\n    for (int i = 0; i < n; i++) p[i] = i + 1;\n    return p;\n}\nvoid scale_all(int *a, int n, int k) {\n    for (int i = 0; i < n; i++) a[i] += k;\n}\nint main(void) { return 0; }',
)

# ============================== MODULE 14: structs ==============================
M14 = "structs"

L14A = "struct-basics"
L14B = "structs-functions"
L14C = "struct-pointers"
L14D = "cb-checkpoint-m14"

write_module(
    M14,
    "Structs",
    "Grouping related data, passing it around, and reaching members through pointers.",
    "Struct",
    "Gom dữ liệu liên quan, truyền nó đi khắp nơi, và chạm thành viên qua con trỏ.",
    [L14A, L14B, L14C, L14D],
    ["cb-p14-model", "cb-p14-ops"],
)

write_lesson(
    M14,
    L14A,
    "Struct Basics",
    "A struct is a new type you define: named members, one unit.",
    13,
    r"""
## Defining and declaring

```c
struct Point {          // defines a new TYPE
    int x;
    int y;
};

struct Point p = {3, 4};        // positional initializer
struct Point q = {.x = 3, .y = 4};  // designated (clearer, order-free)
```

The `struct` keyword is part of the type name. Members are accessed with the
dot: `p.x`, `p.y`.

## Assignment copies the whole thing

```c
struct Point a = {1, 2};
struct Point b = a;     // b gets its OWN copy of both members
b.x = 99;               // a.x is still 1
```

Arrays copy element-by-element only when you write the loop; structs copy in
one assignment. That makes them natural value objects.

## Nested structs

```c
struct Rect {
    struct Point topleft;
    struct Point size;
};
struct Rect r = {{0, 0}, {10, 5}};
printf("%d\n", r.size.y);   // 5 — dots chain
```

## Arrays of structs

```c
struct Point pts[3] = {{1, 1}, {2, 2}, {3, 3}};
printf("%d\n", pts[1].x);   // 2 — index first, then member
```
""",
    "Cơ bản về struct",
    "Struct là một kiểu mới do bạn định nghĩa: thành viên có tên, một khối thống nhất.",
    r"""
## Định nghĩa và khai báo

```c
struct Point {          // định nghĩa một KIỂU mới
    int x;
    int y;
};

struct Point p = {3, 4};            // khởi tạo theo vị trí
struct Point q = {.x = 3, .y = 4};  // theo tên (rõ hơn, không phụ thuộc thứ tự)
```

Từ khóa `struct` là một phần của tên kiểu. Thành viên được truy cập bằng dấu
chấm: `p.x`, `p.y`.

## Gán là chép toàn bộ

```c
struct Point a = {1, 2};
struct Point b = a;     // b có BẢN SAO riêng của cả hai thành viên
b.x = 99;               // a.x vẫn là 1
```

Mảng phải tự viết vòng lặp mới chép được từng phần tử; struct chép trong một
lệnh gán. Vì thế struct là đối tượng giá trị tự nhiên.

## Struct lồng nhau

```c
struct Rect {
    struct Point topleft;
    struct Point size;
};
struct Rect r = {{0, 0}, {10, 5}};
printf("%d\n", r.size.y);   // 5 — dấu chấm nối tiếp
```

## Mảng struct

```c
struct Point pts[3] = {{1, 1}, {2, 2}, {3, 3}};
printf("%d\n", pts[1].x);   // 2 — đánh chỉ số trước, thành viên sau
```
""",
)

write_lesson(
    M14,
    L14B,
    "Structs and Functions",
    "Pass by copy, or pass a pointer when the function must modify.",
    13,
    r"""
## Passing by value (copy)

```c
int area(struct Rect r) {          // r is a COPY
    return r.size.x * r.size.y;
}
```

Small structs pass cheaply and safely — the function cannot touch the
caller's original.

## Returning structs

```c
struct Point make_point(int x, int y) {
    struct Point p = {x, y};
    return p;                      // a copy comes back
}
```

## Passing a pointer to modify

```c
void move_by(struct Point *p, int dx, int dy) {
    p->x += dx;                    // arrow: dereference + member
    p->y += dy;
}
...
struct Point pos = {0, 0};
move_by(&pos, 3, 4);              // pos is now (3, 4)
```

`p->x` is exactly shorthand for `(*p).x` — dereference then take the member.
The arrow exists because `.` binds tighter than `*`, making `*p.x` mean the
wrong thing.

## Choosing the shape

- read-only use of a small struct → pass by value
- must modify, or the struct is large → pass `struct S *`
""",
    "Struct và hàm",
    "Truyền bằng bản sao, hoặc truyền con trỏ khi hàm phải sửa.",
    r"""
## Truyền bằng giá trị (bản sao)

```c
int area(struct Rect r) {          // r là BẢN SAO
    return r.size.x * r.size.y;
}
```

Struct nhỏ truyền rẻ và an toàn — hàm không thể đụng tới bản gốc của người
gọi.

## Trả về struct

```c
struct Point make_point(int x, int y) {
    struct Point p = {x, y};
    return p;                      // một bản sao quay về
}
```

## Truyền con trỏ để sửa

```c
void move_by(struct Point *p, int dx, int dy) {
    p->x += dx;                    // mũi tên: giải tham chiếu + thành viên
    p->y += dy;
}
...
struct Point pos = {0, 0};
move_by(&pos, 3, 4);              // pos giờ là (3, 4)
```

`p->x` chính là cách viết ngắn của `(*p).x` — giải tham chiếu rồi lấy thành
viên. Mũi tên ra đời vì `.` kết hợp chặt hơn `*`, khiến `*p.x` mang nghĩa sai.

## Chọn hình dạng

- chỉ đọc với struct nhỏ → truyền bằng giá trị
- phải sửa, hoặc struct lớn → truyền `struct S *`
""",
)

write_lesson(
    M14,
    L14C,
    "Pointers to Structs",
    "The arrow operator, struct pointers in arrays, and -> chains.",
    13,
    r"""
## Arrow vs dot

```c
struct Point p = {1, 2};
struct Point *pp = &p;

p.x            // through the variable: dot
pp->x          // through the pointer: arrow
(*pp).x        // same thing, written the hard way
```

## Walking an array of structs

```c
struct Point pts[3] = {{1, 1}, {2, 4}, {3, 9}};
struct Point *end = pts + 3;
for (struct Point *it = pts; it < end; it++) {
    printf("(%d,%d)\n", it->x, it->y);   // it++ moves one WHOLE struct
}
```

Pointer arithmetic scales by `sizeof(struct Point)` — one step, one struct.

## Mixed models

A common C API shape: the array is passed as a pointer, each element used
through the arrow:

```c
int total_x(struct Point *pts, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += pts[i].x;   // or (pts+i)->x
    return s;
}
```

## NULL discipline applies too

A struct pointer can be NULL; any function that receives one must either
trust the contract or check it, just like int pointers.
""",
    "Con trỏ tới struct",
    "Toán tử mũi tên, mảng con trỏ struct, và chuỗi ->.",
    r"""
## Mũi tên vs dấu chấm

```c
struct Point p = {1, 2};
struct Point *pp = &p;

p.x            // qua biến: dấu chấm
pp->x          // qua con trỏ: mũi tên
(*pp).x        // cùng một thứ, viết cách dài
```

## Đi bộ trên mảng struct

```c
struct Point pts[3] = {{1, 1}, {2, 4}, {3, 9}};
struct Point *end = pts + 3;
for (struct Point *it = pts; it < end; it++) {
    printf("(%d,%d)\n", it->x, it->y);   // it++ tiến một STRUCT NGUYÊN
}
```

Số học con trỏ nhân với `sizeof(struct Point)` — một bước, một struct.

## Mô hình hỗn hợp

Hình dạng API C phổ biến: mảng được truyền như con trỏ, mỗi phần tử dùng qua
mũi tên:

```c
int total_x(struct Point *pts, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += pts[i].x;   // hoặc (pts+i)->x
    return s;
}
```

## Kỷ luật NULL cũng áp dụng

Con trỏ struct có thể là NULL; hàm nào nhận nó đều phải tin giao ước hoặc
kiểm tra, giống hệt con trỏ int.
""",
)

write_practice(
    M14,
    "cb-p14-model",
    "Data Modeling",
    "Build the Point/Rect models and their read-only queries.",
    "Mô hình dữ liệu",
    "Dựng mô hình Point/Rect và các truy vấn chỉ-đọc của nó.",
    L14A,
    15,
    "beginner",
    [
        challenge(
            "cb14-distance-sq",
            "Distance Squared",
            "Given `struct Point { int x; int y; };` in scope, implement `int dist_sq(struct Point a, struct Point b)` returning the squared distance between them.",
            C_PRELUDE + "struct Point { int x; int y; };\n",
            [
                ("axis aligned", "struct Point a = {0, 0}, b = {3, 4};\nCHECK_EQ(dist_sq(a, b), 25);", "dx*dx + dy*dy — no sqrt."),
                ("same point", "struct Point a = {2, 2};\nCHECK_EQ(dist_sq(a, a), 0);", "Zero distance."),
                ("negatives", "struct Point a = {-1, -1}, b = {2, 3};\nCHECK_EQ(dist_sq(a, b), 25);", "Signs cancel in the difference."),
            ],
            level="guided",
        ),
        challenge(
            "cb14-rect-area",
            "Rectangle Area",
            "Given `struct Rect { int w; int h; };` in scope, implement `int area(struct Rect r)` and `int perimeter(struct Rect r)`.",
            C_PRELUDE + "struct Rect { int w; int h; };\n",
            [
                ("area", "struct Rect r = {3, 4};\nCHECK_EQ(area(r), 12);", "w * h."),
                ("perimeter", "struct Rect r = {3, 4};\nCHECK_EQ(perimeter(r), 14);", "2*(w + h)."),
                ("square", "struct Rect r = {5, 5};\nCHECK_EQ(area(r), 25);\nCHECK_EQ(perimeter(r), 20);", "Same formulas."),
            ],
            level="imitation",
        ),
        challenge(
            "cb14-leftmost",
            "Leftmost Point",
            "Given `struct Point { int x; int y; };` in scope, implement `struct Point* leftmost(struct Point *pts, int n)` returning a pointer to the point with the SMALLEST x (ties: the first such point).",
            C_PRELUDE + "struct Point { int x; int y; };\n",
            [
                ("basic", "struct Point pts[] = {{3, 0}, {1, 5}, {2, 7}};\nCHECK_EQ(leftmost(pts, 3), &pts[1]);", "Track the best index, return its address."),
                ("tie first", "struct Point pts[] = {{1, 9}, {1, 2}};\nCHECK_EQ(leftmost(pts, 2), &pts[0]);", "Strictly smaller to replace."),
                ("single", "struct Point one = {5, 5};\nCHECK_EQ(leftmost(&one, 1), &one);", "n=1 returns it."),
            ],
            level="independent",
        ),
    ],
    {
        "cb14-distance-sq": vi_challenge(
            "Bình phương khoảng cách",
            "Với `struct Point { int x; int y; };` có sẵn, cài `int dist_sq(struct Point a, struct Point b)` trả về bình phương khoảng cách giữa hai điểm.",
            [("cùng trục", "dx*dx + dy*dy — không cần sqrt."), ("trùng điểm", "Khoảng cách bằng 0."), ("số âm", "Dấu triệt tiêu khi lấy hiệu.")],
        ),
        "cb14-rect-area": vi_challenge(
            "Diện tích hình chữ nhật",
            "Với `struct Rect { int w; int h; };` có sẵn, cài `int area(struct Rect r)` và `int perimeter(struct Rect r)`.",
            [("diện tích", "w * h."), ("chu vi", "2*(w + h)."), ("hình vuông", "Cùng công thức.")],
        ),
        "cb14-leftmost": vi_challenge(
            "Điểm trái nhất",
            "Với `struct Point { int x; int y; };` có sẵn, cài `struct Point* leftmost(struct Point *pts, int n)` trả con trỏ tới điểm có x NHỎ NHẤT (bằng nhau: lấy điểm đầu tiên).",
            [("cơ bản", "Theo dõi chỉ số tốt nhất, trả địa chỉ của nó."), ("hòa lấy trước", "Chỉ thay thế khi NHỎ HƠN hẳn."), ("một điểm", "n=1 trả chính nó.")],
        ),
    },
    solutions=[
        (
            "cb14-distance-sq",
            '#include <stdio.h>\nstruct Point { int x; int y; };\nint dist_sq(struct Point a, struct Point b) {\n    int dx = a.x - b.x;\n    int dy = a.y - b.y;\n    return dx * dx + dy * dy;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstruct Point { int x; int y; };\nint dist_sq(struct Point a, struct Point b) {\n    int dx = a.x - b.x;\n    int dy = a.y - b.y;\n    return dx + dy;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb14-rect-area",
            '#include <stdio.h>\nstruct Rect { int w; int h; };\nint area(struct Rect r) {\n    return r.w * r.h;\n}\nint perimeter(struct Rect r) {\n    return 2 * (r.w + r.h);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstruct Rect { int w; int h; };\nint area(struct Rect r) {\n    return r.w + r.h;\n}\nint perimeter(struct Rect r) {\n    return 2 * (r.w + r.h);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb14-leftmost",
            '#include <stdio.h>\nstruct Point { int x; int y; };\nstruct Point* leftmost(struct Point *pts, int n) {\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (pts[i].x < pts[best].x) best = i;\n    return &pts[best];\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstruct Point { int x; int y; };\nstruct Point* leftmost(struct Point *pts, int n) {\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (pts[i].x > pts[best].x) best = i;\n    return &pts[best];\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M14,
    "cb-p14-ops",
    "Mutating Operations",
    "Struct functions that modify through pointers, plus a record scan.",
    "Thao tác biến đổi",
    "Các hàm struct sửa dữ liệu qua con trỏ, cùng một lượt quét bản ghi.",
    L14C,
    16,
    "beginner",
    [
        challenge(
            "cb14-move-by",
            "Move By",
            "Given `struct Point { int x; int y; };` in scope, implement `void move_by(struct Point *p, int dx, int dy)` shifting the point in place.",
            C_PRELUDE + "struct Point { int x; int y; };\n",
            [
                ("shift", "struct Point p = {0, 0};\nmove_by(&p, 3, -2);\nCHECK_EQ(p.x, 3);\nCHECK_EQ(p.y, -2);", "Use the arrow operator."),
                ("zero shift", "struct Point p = {5, 5};\nmove_by(&p, 0, 0);\nCHECK_EQ(p.x, 5);\nCHECK_EQ(p.y, 5);", "No-op is fine."),
            ],
            level="imitation",
        ),
        challenge(
            "cb14-normalize",
            "Normalize Health",
            "Given `struct Player { int hp; };` in scope, implement `void heal(struct Player *pl, int amount)` raising hp by amount but never above 100.",
            C_PRELUDE + "struct Player { int hp; };\n",
            [
                ("within limit", "struct Player p = {80};\nheal(&p, 15);\nCHECK_EQ(p.hp, 95);", "Simple addition suffices."),
                ("clamped", "struct Player p = {90};\nheal(&p, 50);\nCHECK_EQ(p.hp, 100);", "Cap at 100."),
                ("already max", "struct Player p = {100};\nheal(&p, 30);\nCHECK_EQ(p.hp, 100);", "Stays at 100."),
            ],
            level="guided",
        ),
        challenge(
            "cb14-total-inventory",
            "Inventory Value",
            "Given `struct Item { int qty; int unit_cost; };` in scope, implement `long inventory_value(const struct Item *items, int n)` summing qty*unit_cost over n items.",
            C_PRELUDE + "struct Item { int qty; int unit_cost; };\n",
            [
                ("basic", "struct Item its[] = {{2, 300}, {1, 500}};\nCHECK_EQ(inventory_value(its, 2), 1100);", "Accumulate qty*unit_cost."),
                ("empty", "struct Item its[] = {{0, 0}};\nCHECK_EQ(inventory_value(its, 0), 0);", "n=0 gives 0."),
                ("zero qty", "struct Item its[] = {{0, 999}, {3, 100}};\nCHECK_EQ(inventory_value(its, 2), 300);", "Zero-qty items contribute nothing."),
            ],
            level="independent",
        ),
        challenge(
            "cb14-find-id",
            "Find by Id",
            "Given `struct Rec { int id; int score; };` in scope, implement `const struct Rec* find_id(const struct Rec *rs, int n, int id)` returning a pointer to the record with that id, or NULL.",
            C_PRELUDE + "struct Rec { int id; int score; };\n",
            [
                ("found", "struct Rec rs[] = {{1, 10}, {2, 20}};\nCHECK_EQ(find_id(rs, 2, 2), &rs[1]);", "Return the record's address."),
                ("missing null", "struct Rec rs[] = {{1, 10}};\nCHECK_EQ(find_id(rs, 1, 9), NULL);", "NULL for absent ids."),
                ("first match", "struct Rec rs[] = {{7, 1}, {7, 2}};\nCHECK_EQ(find_id(rs, 2, 7), &rs[0]);", "Earliest wins."),
            ],
            level="independent",
        ),
    ],
    {
        "cb14-move-by": vi_challenge(
            "Di chuyển theo delta",
            "Với `struct Point { int x; int y; };` có sẵn, cài `void move_by(struct Point *p, int dx, int dy)` dịch điểm tại chỗ.",
            [("dịch", "Dùng toán tử mũi tên."), ("delta 0", "Không làm gì cũng ổn.")],
        ),
        "cb14-normalize": vi_challenge(
            "Chuẩn hóa máu",
            "Với `struct Player { int hp; };` có sẵn, cài `void heal(struct Player *pl, int amount)` tăng hp lên amount nhưng không vượt 100.",
            [("trong giới hạn", "Cộng đơn giản là đủ."), ("kẹp trần", "Giới hạn ở 100."), ("đã max", "Vẫn giữ 100.")],
        ),
        "cb14-total-inventory": vi_challenge(
            "Tổng giá kho",
            "Với `struct Item { int qty; int unit_cost; };` có sẵn, cài `long inventory_value(const struct Item *items, int n)` cộng qty*unit_cost trên n món.",
            [("cơ bản", "Cộng dồn qty*unit_cost."), ("rỗng", "n=0 cho ra 0."), ("qty 0", "Món có qty=0 không đóng góp.")],
        ),
        "cb14-find-id": vi_challenge(
            "Tìm theo id",
            "Với `struct Rec { int id; int score; };` có sẵn, cài `const struct Rec* find_id(const struct Rec *rs, int n, int id)` trả con trỏ tới bản ghi có id đó, hoặc NULL.",
            [("thấy", "Trả địa chỉ của bản ghi."), ("không có trả NULL", "NULL cho id vắng mặt."), ("khớp đầu tiên", "Lấy sớm nhất.")],
        ),
    },
    solutions=[
        (
            "cb14-move-by",
            '#include <stdio.h>\nstruct Point { int x; int y; };\nvoid move_by(struct Point *p, int dx, int dy) {\n    p->x += dx;\n    p->y += dy;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstruct Point { int x; int y; };\nvoid move_by(struct Point *p, int dx, int dy) {\n    p->x = dx;\n    p->y = dy;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb14-normalize",
            '#include <stdio.h>\nstruct Player { int hp; };\nvoid heal(struct Player *pl, int amount) {\n    pl->hp += amount;\n    if (pl->hp > 100) pl->hp = 100;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstruct Player { int hp; };\nvoid heal(struct Player *pl, int amount) {\n    pl->hp = amount;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb14-total-inventory",
            '#include <stdio.h>\nstruct Item { int qty; int unit_cost; };\nlong inventory_value(const struct Item *items, int n) {\n    long total = 0;\n    for (int i = 0; i < n; i++)\n        total += (long)items[i].qty * items[i].unit_cost;\n    return total;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstruct Item { int qty; int unit_cost; };\nlong inventory_value(const struct Item *items, int n) {\n    long total = 0;\n    for (int i = 0; i < n; i++)\n        total += (long)(items[i].qty + items[i].unit_cost);\n    return total;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb14-find-id",
            '#include <stdio.h>\nstruct Rec { int id; int score; };\nconst struct Rec* find_id(const struct Rec *rs, int n, int id) {\n    for (int i = 0; i < n; i++)\n        if (rs[i].id == id) return &rs[i];\n    return NULL;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstruct Rec { int id; int score; };\nconst struct Rec* find_id(const struct Rec *rs, int n, int id) {\n    for (int i = 0; i < n; i++)\n        if (rs[i].score == id) return &rs[i];\n    return NULL;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M14,
    L14D,
    "Checkpoint: Structs",
    "A bank-account model with query and mutation through pointers.",
    16,
    r"""
## Checkpoint

Model + query + mutate = the building blocks of every C program bigger than a toy.
""",
    "Điểm kiểm tra: Struct",
    "Mô hình tài khoản ngân hàng với truy vấn và biến đổi qua con trỏ.",
    r"""
## Điểm kiểm tra

Mô hình + truy vấn + biến đổi = những viên gạch của mọi chương trình C lớn hơn
món đồ chơi.
""",
    challenge(
        "cb14-checkpoint-account",
        "Account Operations",
        "Given `struct Account { int balance; };` in scope, implement `void deposit(struct Account *a, int amount)` adding amount, `int withdraw(struct Account *a, int amount)` subtracting and returning 1 only if the balance stayed >= 0 (else 0 and no change), and `const struct Account* richest(const struct Account *as, int n)` returning the account with the highest balance.",
        C_PRELUDE + "struct Account { int balance; };\n",
        [
            ("deposit", "struct Account a = {100};\ndeposit(&a, 50);\nCHECK_EQ(a.balance, 150);", "Arrow add."),
            ("withdraw ok", "struct Account a = {100};\nCHECK_EQ(withdraw(&a, 30), 1);\nCHECK_EQ(a.balance, 70);", "Subtract and report success."),
            ("withdraw rejected", "struct Account a = {10};\nCHECK_EQ(withdraw(&a, 30), 0);\nCHECK_EQ(a.balance, 10);", "Refuse overdrafts; balance unchanged."),
            ("richest", "struct Account as[] = {{100}, {300}, {200}};\nCHECK_EQ(richest(as, 3), &as[1]);", "Max scan returning an address."),
            ("richest tie first", "struct Account as[] = {{300}, {300}};\nCHECK_EQ(richest(as, 2), &as[0]);", "Strictly greater to replace."),
        ],
    ),
    vi_challenge(
        "Thao tác tài khoản",
        "Với `struct Account { int balance; };` có sẵn, cài `void deposit(struct Account *a, int amount)` cộng tiền, `int withdraw(struct Account *a, int amount)` trừ tiền và trả 1 chỉ khi số dư vẫn >= 0 (ngược lại trả 0 và không đổi), và `const struct Account* richest(const struct Account *as, int n)` trả tài khoản có số dư cao nhất.",
        [("nạp tiền", "Cộng qua mũi tên."), ("rút thành công", "Trừ và báo thành công."), ("rút bị từ chối", "Từ chối thấu chi; số dư giữ nguyên."), ("giàu nhất", "Quét max trả về địa chỉ."), ("hòa lấy trước", "Chỉ thay khi LỚN HƠN hẳn.")],
    ),
    solution='#include <stdio.h>\nstruct Account { int balance; };\nvoid deposit(struct Account *a, int amount) {\n    a->balance += amount;\n}\nint withdraw(struct Account *a, int amount) {\n    if (a->balance - amount < 0) return 0;\n    a->balance -= amount;\n    return 1;\n}\nconst struct Account* richest(const struct Account *as, int n) {\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (as[i].balance > as[best].balance) best = i;\n    return &as[best];\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\nstruct Account { int balance; };\nvoid deposit(struct Account *a, int amount) {\n    a->balance += amount;\n}\nint withdraw(struct Account *a, int amount) {\n    if (a->balance - amount < 0) return 0;\n    a->balance -= amount;\n    return 0;\n}\nconst struct Account* richest(const struct Account *as, int n) {\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (as[i].balance > as[best].balance) best = i;\n    return &as[best];\n}\nint main(void) { return 0; }',
)

print("batch 7 done: modules 13-14")
