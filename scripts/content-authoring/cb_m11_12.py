#!/usr/bin/env python3
"""C Beginner — batch 6: modules 11 (pointer-fundamentals) and 12 (pointers-arrays)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ====================== MODULE 11: pointer-fundamentals ======================
M11 = "pointer-fundamentals"

L11A = "addresses-and-pointers"
L11B = "dereferencing"
L11C = "pointer-parameters"
L11D = "null-and-mistakes"
L11E = "cb-checkpoint-m11"

write_module(
    M11,
    "Pointers Fundamentals",
    "Addresses, the & and * operators, pointers as parameters, NULL — and the classic mistakes.",
    "Nền tảng con trỏ",
    "Địa chỉ, toán tử & và *, con trỏ làm tham số, NULL — và những lỗi kinh điển.",
    [L11A, L11B, L11C, L11D, L11E],
    ["cb-p11-address", "cb-p11-swap", "cb-p11-mistakes"],
)

write_lesson(
    M11,
    L11A,
    "Addresses and Pointer Variables",
    "Every variable lives at an address; a pointer is a variable that stores one.",
    14,
    r"""
## Memory as numbered houses

Every byte of memory has an **address** — a number, like a house number on a
very long street. A variable like `int x = 42;` occupies some of those
houses. The **address-of operator** `&` asks "where does x live?"

```c
int x = 42;
printf("%p\n", (void*)&x);   // e.g. 0x7ffe... — an address, different each run
```

## A pointer stores an address

A **pointer** is just a variable whose value is an address:

```c
int x = 42;
int *p = &x;        // p holds the address of x
```

Read `int *p` as "p is a pointer to int". The type matters: an `int*` promises
"the object at this address is an int". A `double*` promises a double. Pointers
to different types are not interchangeable.

## Two spellings, one meaning

```c
int *p;             // declaration context: * says "p is a pointer"
*p = 7;             // expression context:  * means "the object p points to"
```

## Address is not value

`x` is 42. `&x` is where 42 lives. `p` is a copy of that where. Three different
things. Keeping them straight is 80% of understanding pointers.
""",
    "Địa chỉ và biến con trỏ",
    "Mọi biến đều nằm tại một địa chỉ; con trỏ là biến lưu địa chỉ đó.",
    r"""
## Bộ nhớ như những ngôi nhà được đánh số

Mọi byte bộ nhớ đều có một **địa chỉ** — một con số, như số nhà trên một con
đường rất dài. Biến `int x = 42;` chiếm vài "ngôi nhà" đó. **Toán tử
lấy địa chỉ** `&` hỏi "x sống ở đâu?"

```c
int x = 42;
printf("%p\n", (void*)&x);   // vd 0x7ffe... — một địa chỉ, mỗi lần chạy khác nhau
```

## Con trỏ lưu một địa chỉ

**Con trỏ** chỉ là biến mà giá trị của nó là một địa chỉ:

```c
int x = 42;
int *p = &x;        // p giữ địa chỉ của x
```

Đọc `int *p` là "p là con trỏ tới int". Kiểu rất quan trọng: `int*` hứa
"đối tượng tại địa chỉ này là một int". `double*` hứa một double. Con trỏ tới
các kiểu khác nhau không thể thay thế cho nhau.

## Hai cách viết, một ý nghĩa

```c
int *p;             // ngữ cảnh khai báo: * nói "p là con trỏ"
*p = 7;             // ngữ cảnh biểu thức:  * nghĩa là "đối tượng p trỏ tới"
```

## Địa chỉ không phải giá trị

`x` là 42. `&x` là nơi 42 sống. `p` là bản sao của cái "nơi" đó. Ba thứ khác
nhau. Phân biệt được ba thứ này là 80% của việc hiểu con trỏ.
""",
)

write_lesson(
    M11,
    L11B,
    "Dereferencing",
    "The * operator follows the pointer to the object it points at.",
    13,
    r"""
## Following the arrow

**Dereferencing** a pointer means going to the address it holds and using the
object there:

```c
int x = 42;
int *p = &x;

printf("%d\n", *p);   // 42 — the object p points AT
*p = 99;              // writes through p: x is now 99
printf("%d\n", x);    // 99
```

`*p` and `x` are the **same object**. There is one int; two names for it.

## Declaration vs dereference: same star, different jobs

In `int *p = &x;` the star is part of the *type*. In `*p = 99;` the star is
the dereference operator. Same symbol, different contexts.

## Reading and writing through pointers

```c
int a = 1, b = 2;
int *p = &a;
int *q = &b;

*p = *q;        // a = b  (copies the VALUE b holds into a)
p = q;          // p now points at b (copies the ADDRESS)
```

The first copies what the pointers point to; the second re-aims the pointer.
Draw the arrows before you write the code.

## Uninitialized pointers

```c
int *p;         // holds a GARBAGE address
*p = 5;         // undefined behavior — writes to a random place
```

A pointer must be given an address before you dereference it — either `&x`
or `NULL`.
""",
    "Giải tham chiếu",
    "Toán tử * đi theo con trỏ tới đối tượng mà nó trỏ tới.",
    r"""
## Đi theo mũi tên

**Giải tham chiếu** một con trỏ nghĩa là đến địa chỉ nó giữ và dùng đối tượng
ở đó:

```c
int x = 42;
int *p = &x;

printf("%d\n", *p);   // 42 — đối tượng p trỏ TỚI
*p = 99;              // ghi qua p: x giờ là 99
printf("%d\n", x);    // 99
```

`*p` và `x` là **cùng một đối tượng**. Chỉ có một int; hai cái tên cho nó.

## Khai báo vs giải tham chiếu: cùng dấu sao, khác nhiệm vụ

Trong `int *p = &x;` dấu sao là một phần của *kiểu*. Trong `*p = 99;` dấu sao
là toán tử giải tham chiếu. Cùng ký hiệu, khác ngữ cảnh.

## Đọc và ghi qua con trỏ

```c
int a = 1, b = 2;
int *p = &a;
int *q = &b;

*p = *q;        // a = b  (chép GIÁ TRỊ mà b giữ vào a)
p = q;          // p giờ trỏ tới b (chép ĐỊA CHỈ)
```

Câu đầu chép thứ mà con trỏ trỏ tới; câu sau đổi hướng con trỏ. Hãy vẽ mũi
tên trước khi viết code.

## Con trỏ chưa khởi tạo

```c
int *p;         // giữ một địa chỉ RÁC
*p = 5;         // hành vi không xác định — ghi vào một nơi ngẫu nhiên
```

Con trỏ phải được gán địa chỉ trước khi giải tham chiếu — hoặc `&x` hoặc
`NULL`.
""",
)

write_lesson(
    M11,
    L11C,
    "Pointer Parameters",
    "C passes arguments by value; pointers are how a function reaches back.",
    15,
    r"""
## Why plain parameters can't

C function arguments are **copies**:

```c
void bump(int n) { n = n + 1; }   // bumps the COPY

int x = 5;
bump(x);
// x is still 5 — the function changed its own copy
```

## Passing an address changes the object

Give the function the *address*, and it can dereference its way back to the
original:

```c
void bump(int *n) { *n = *n + 1; }   // follows the pointer to the caller's int

int x = 5;
bump(&x);        // pass the ADDRESS
// x is now 6
```

This is the single most important pointer pattern in C: **out-parameters**.
`scanf("%d", &n)` works for exactly this reason — you hand scanf the address
so it can deposit the value.

## Two outputs from one function

```c
void minmax(int a, int b, int *lo, int *hi) {
    if (a <= b) { *lo = a; *hi = b; }
    else        { *lo = b; *hi = a; }
}
...
int lo, hi;
minmax(3, 8, &lo, &hi);
```

A function returns one value; pointers give it many.

## The contract

A pointer parameter is a promise: "this points at a valid int". Passing
`NULL` or an uninitialized pointer breaks the contract — the function will
dereference garbage. Module 14 introduces checking.
""",
    "Tham số con trỏ",
    "C truyền đối số bằng giá trị; con trỏ là cách để hàm chạm ngược lại bản gốc.",
    r"""
## Tại sao tham số thường không làm được

Đối số hàm C là **bản sao**:

```c
void bump(int n) { n = n + 1; }   // tăng BẢN SAO

int x = 5;
bump(x);
// x vẫn là 5 — hàm chỉ đổi bản sao của nó
```

## Truyền địa chỉ thì thay đổi được đối tượng

Đưa cho hàm *địa chỉ*, nó có thể giải tham chiếu để về lại bản gốc:

```c
void bump(int *n) { *n = *n + 1; }   // đi theo con trỏ tới int của người gọi

int x = 5;
bump(&x);        // truyền ĐỊA CHỈ
// x giờ là 6
```

Đây là mẫu con trỏ quan trọng nhất trong C: **tham số xuất**. `scanf("%d", &n)`
hoạt động chính vì lý do này — bạn đưa scanf địa chỉ để nó gửi giá trị vào.

## Hai đầu ra từ một hàm

```c
void minmax(int a, int b, int *lo, int *hi) {
    if (a <= b) { *lo = a; *hi = b; }
    else        { *lo = b; *hi = a; }
}
...
int lo, hi;
minmax(3, 8, &lo, &hi);
```

Hàm trả về một giá trị; con trỏ cho nó nhiều giá trị.

## Giao ước

Tham số con trỏ là một lời hứa: "cái này trỏ tới một int hợp lệ". Truyền
`NULL` hoặc con trỏ chưa khởi tạo là phá vỡ giao ước — hàm sẽ giải tham chiếu
rác. Module 14 sẽ giới thiệu việc kiểm tra.
""",
)

write_lesson(
    M11,
    L11D,
    "NULL and Classic Pointer Mistakes",
    "The one safe invalid value, and the four bugs every C programmer meets.",
    13,
    r"""
## NULL: the pointer that points at nothing — on purpose

```c
#include <stdio.h>      // NULL lives in stdio.h and friends

int *p = NULL;          // "points at nothing", a defined, testable value
if (p == NULL) { /* not aiming at any object */ }
```

Dereferencing NULL is undefined behavior — typically a **crash** (on this
course's sandbox, a segmentation fault). That crash is a *gift*: it is loud and
immediate, unlike garbage pointers that silently corrupt.

Initialize pointers to `NULL` when you have nothing to point at yet.

## Mistake 1: dangling pointer

```c
int *p;
{
    int local = 7;
    p = &local;
}                        // local dies here
printf("%d\n", *p);      // p still holds the dead address — undefined behavior
```

The variable `local` lived in a stack frame that no longer exists. Pointers to
dead locals are **dangling**.

## Mistake 2: dereferencing before assigning

```c
int *p;
*p = 3;          // p was never given an address — undefined behavior
```

## Mistake 3: returning the address of a local

```c
int *make(void) {
    int x = 5;
    return &x;   // x dies when the function returns — dangling on arrival
}
```

## Mistake 4: confusing address with value

```c
int x = 1;
int *p = &x;
if (p == &x) { }      // comparing addresses — true
if (*p == x) { }      // comparing values — true
if (p == x)  { }      // comparing address to int — nonsense (and a warning)
```

The compiler's warnings are your first defense: **read them**.
""",
    "NULL và các lỗi con trỏ kinh điển",
    "Giá trị không hợp lệ duy nhất được định nghĩa, và bốn lỗi mà mọi lập trình viên C đều gặp.",
    r"""
## NULL: con trỏ không trỏ đâu cả — một cách có chủ đích

```c
#include <stdio.h>      // NULL sống trong stdio.h và các header khác

int *p = NULL;          // "không trỏ tới đâu", giá trị xác định, kiểm tra được
if (p == NULL) { /* không nhắm vào đối tượng nào */ }
```

Giải tham chiếu NULL là hành vi không xác định — thường là **crash** (trên
sandbox của khóa này, là lỗi segmentation fault). Cái crash đó là một *món
quà*: nó ồn ào và ngay lập tức, khác với con trỏ rác âm thầm phá hỏng dữ liệu.

Khởi tạo con trỏ thành `NULL` khi bạn chưa có gì để trỏ tới.

## Lỗi 1: con trỏ treo

```c
int *p;
{
    int local = 7;
    p = &local;
}                        // local chết tại đây
printf("%d\n", *p);      // p vẫn giữ địa chỉ đã chết — hành vi không xác định
```

Biến `local` sống trong một khung ngăn xếp không còn tồn tại. Con trỏ trỏ tới
biến cục bộ đã chết gọi là **đang treo**.

## Lỗi 2: giải tham chiếu trước khi gán

```c
int *p;
*p = 3;          // p chưa bao giờ được gán địa chỉ — hành vi không xác định
```

## Lỗi 3: trả về địa chỉ của biến cục bộ

```c
int *make(void) {
    int x = 5;
    return &x;   // x chết khi hàm kết thúc — treo ngay từ đầu
}
```

## Lỗi 4: nhầm địa chỉ với giá trị

```c
int x = 1;
int *p = &x;
if (p == &x) { }      // so sánh địa chỉ — đúng
if (*p == x) { }      // so sánh giá trị — đúng
if (p == x)  { }      // so sánh địa chỉ với int — vô nghĩa (và bị warning)
```

Warning của trình biên dịch là tuyến phòng thủ đầu tiên của bạn: **hãy đọc
chúng**.
""",
)

write_practice(
    M11,
    "cb-p11-address",
    "Address Practice",
    "Observe addresses, write through pointers, and distinguish pointer from pointee.",
    "Luyện tập địa chỉ",
    "Quan sát địa chỉ, ghi qua con trỏ, phân biệt con trỏ với đối tượng bị trỏ.",
    L11B,
    15,
    "beginner",
    [
        challenge(
            "cb11-deref-basics",
            "Through the Pointer",
            "A function `int* aim(int *target)` receives a pointer and must RETURN the same pointer after setting the pointed-to int to 100. Implement it so `*p` is 100 afterwards.",
            C_PRELUDE,
            [
                ("write through", "int x = 0;\nint *p = aim(&x);\nCHECK_EQ(x, 100);\nCHECK_EQ(*p, 100);", "Dereference, assign, return the pointer as-is."),
                ("reusable", "int a = 5;\naim(&a);\nCHECK_EQ(a, 100);", "The pointed-to object changes."),
            ],
            level="imitation",
        ),
        challenge(
            "cb11-max-ptr",
            "Pointer to the Max",
            "Implement `const int* max_ptr(const int* a, int n)` returning a pointer to the LARGEST element of the first n elements (n >= 1).",
            C_PRELUDE,
            [
                ("middle winner", "int a[] = {1, 9, 2};\nCHECK_EQ(*max_ptr(a, 3), 9);", "Track the best element's pointer."),
                ("same address", "int a[] = {1, 9, 2};\nCHECK_EQ(max_ptr(a, 3), &a[1]);", "Return the ADDRESS, not a copy."),
                ("first element", "int a[] = {7, 2};\nCHECK_EQ(max_ptr(a, 2), &a[0]);", "Max can be the first."),
                ("last element", "int a[] = {1, 2, 8};\nCHECK_EQ(max_ptr(a, 3), &a[2]);", "Or the last."),
            ],
            level="guided",
        ),
        challenge(
            "cb11-swap-ptr",
            "swap via Pointers",
            "Implement `void swap(int *a, int *b)` exchanging the two ints the pointers aim at.",
            C_PRELUDE,
            [
                ("plain", "int x = 1, y = 2;\nswap(&x, &y);\nCHECK_EQ(x, 2);\nCHECK_EQ(y, 1);", "Classic three-step with a temp."),
                ("same address", "int x = 5;\nswap(&x, &x);\nCHECK_EQ(x, 5);", "Swapping an object with ITSELF must not corrupt it (no lost value)."),
            ],
            level="guided",
        ),
        challenge(
            "cb11-two-outputs",
            "Two Outputs",
            "Implement `void divmod(int a, int b, int *q, int *r)` storing the quotient and remainder of a/b into *q and *r.",
            C_PRELUDE,
            [
                ("clean split", "int q, r;\ndivmod(17, 5, &q, &r);\nCHECK_EQ(q, 3);\nCHECK_EQ(r, 2);", "Use / and % once each."),
                ("exact", "int q, r;\ndivmod(20, 5, &q, &r);\nCHECK_EQ(q, 4);\nCHECK_EQ(r, 0);", "Remainder can be 0."),
                ("tiny", "int q, r;\ndivmod(2, 10, &q, &r);\nCHECK_EQ(q, 0);\nCHECK_EQ(r, 2);", "Quotient 0 is fine."),
            ],
            level="independent",
        ),
    ],
    {
        "cb11-deref-basics": vi_challenge(
            "Qua con trỏ",
            "Hàm `int* aim(int *target)` nhận một con trỏ và phải TRẢ VỀ chính con trỏ đó sau khi gán int bị trỏ thành 100. Cài để sau đó `*p` là 100.",
            [("ghi qua con trỏ", "Giải tham chiếu, gán, trả lại con trỏ nguyên vẹn."), ("dùng lại được", "Đối tượng bị trỏ thay đổi.")],
        ),
        "cb11-max-ptr": vi_challenge(
            "Con trỏ tới phần tử lớn nhất",
            "Cài `const int* max_ptr(const int* a, int n)` trả về con trỏ trỏ tới phần tử LỚN NHẤT trong n phần tử đầu (n >= 1).",
            [("giữa thắng", "Theo dõi con trỏ tới phần tử tốt nhất."), ("cùng địa chỉ", "Trả về ĐỊA CHỈ, không phải bản sao."), ("phần tử đầu", "Max có thể là phần tử đầu."), ("phần tử cuối", "Hoặc phần tử cuối.")],
        ),
        "cb11-swap-ptr": vi_challenge(
            "swap qua con trỏ",
            "Cài `void swap(int *a, int *b)` hoán đổi hai int mà hai con trỏ trỏ tới.",
            [("thông thường", "Ba bước kinh điển với biến tạm."), ("cùng địa chỉ", "Hoán đổi một đối tượng với CHÍNH NÓ không được làm hỏng nó.")],
        ),
        "cb11-two-outputs": vi_challenge(
            "Hai đầu ra",
            "Cài `void divmod(int a, int b, int *q, int *r)` lưu thương và số dư của a/b vào *q và *r.",
            [("chia sạch", "Dùng / và % mỗi cái một lần."), ("chia hết", "Số dư có thể là 0."), ("nhỏ", "Thương 0 là hợp lệ.")],
        ),
    },
    solutions=[
        (
            "cb11-deref-basics",
            '#include <stdio.h>\nint* aim(int *target) {\n    *target = 100;\n    return target;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint* aim(int *target) {\n    int local = 100;\n    target = &local;\n    return target;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb11-max-ptr",
            '#include <stdio.h>\nconst int* max_ptr(const int* a, int n) {\n    const int *best = a;\n    for (int i = 1; i < n; i++)\n        if (a[i] > *best) best = &a[i];\n    return best;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nconst int* max_ptr(const int* a, int n) {\n    const int *best = a;\n    for (int i = 1; i < n; i++)\n        if (a[i] > *best) *best = a[i];\n    return best;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb11-swap-ptr",
            '#include <stdio.h>\nvoid swap(int *a, int *b) {\n    int t = *a;\n    *a = *b;\n    *b = t;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid swap(int *a, int *b) {\n    *a = *b;\n    *b = *a;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb11-two-outputs",
            '#include <stdio.h>\nvoid divmod(int a, int b, int *q, int *r) {\n    *q = a / b;\n    *r = a % b;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid divmod(int a, int b, int *q, int *r) {\n    *q = a / b;\n    *r = a - b;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M11,
    "cb-p11-swap",
    "Pointer Surgery",
    "Functions that reach back into the caller's variables: normalizers and a three-way swap.",
    "Phẫu thuật con trỏ",
    "Các hàm chạm ngược vào biến của người gọi: hàm chuẩn hóa và hoán đổi ba chiều.",
    L11C,
    15,
    "beginner",
    [
        challenge(
            "cb11-clamp-ptr",
            "Clamp Through a Pointer",
            "Implement `void clamp_to(int *v, int lo, int hi)`: if *v is below lo set it to lo; above hi set it to hi; otherwise leave it.",
            C_PRELUDE,
            [
                ("below", "int x = 3;\nclamp_to(&x, 10, 20);\nCHECK_EQ(x, 10);", "Raise it to the floor."),
                ("above", "int x = 42;\nclamp_to(&x, 10, 20);\nCHECK_EQ(x, 20);", "Cap it at the ceiling."),
                ("inside untouched", "int x = 15;\nclamp_to(&x, 10, 20);\nCHECK_EQ(x, 15);", "Inside the range: no change."),
                ("boundary lo", "int x = 10;\nclamp_to(&x, 10, 20);\nCHECK_EQ(x, 10);", "Lo itself stays."),
                ("boundary hi", "int x = 20;\nclamp_to(&x, 10, 20);\nCHECK_EQ(x, 20);", "Hi itself stays."),
            ],
            level="guided",
        ),
        challenge(
            "cb11-rotate3",
            "Three-Way Rotate",
            "Implement `void rotate3(int *a, int *b, int *c)` that shifts values one step: a gets b's value, b gets c's, c gets a's ORIGINAL value.",
            C_PRELUDE,
            [
                ("forward", "int a = 1, b = 2, c = 3;\nrotate3(&a, &b, &c);\nCHECK_EQ(a, 2);\nCHECK_EQ(b, 3);\nCHECK_EQ(c, 1);", "Save one original before overwriting."),
                ("negatives", "int a = -1, b = -2, c = -3;\nrotate3(&a, &b, &c);\nCHECK_EQ(a, -2);\nCHECK_EQ(b, -3);\nCHECK_EQ(c, -1);", "Signs ride along."),
                ("all equal", "int a = 4, b = 4, c = 4;\nrotate3(&a, &b, &c);\nCHECK_EQ(a, 4);\nCHECK_EQ(b, 4);\nCHECK_EQ(c, 4);", "Rotating equals changes nothing."),
            ],
            level="independent",
        ),
        challenge(
            "cb11-sorted2",
            "Order Two, In Place",
            "Implement `void order2(int *a, int *b)` so that afterwards *a <= *b (swap only if needed).",
            C_PRELUDE,
            [
                ("needs swap", "int x = 9, y = 3;\norder2(&x, &y);\nCHECK_EQ(x, 3);\nCHECK_EQ(y, 9);", "One swap call."),
                ("already ordered", "int x = 1, y = 2;\norder2(&x, &y);\nCHECK_EQ(x, 1);\nCHECK_EQ(y, 2);", "Do NOT swap equal-or-ordered values."),
                ("equal", "int x = 5, y = 5;\norder2(&x, &y);\nCHECK_EQ(x, 5);\nCHECK_EQ(y, 5);", "Equal stays equal."),
            ],
            level="guided",
        ),
    ],
    {
        "cb11-clamp-ptr": vi_challenge(
            "Chặn giá trị qua con trỏ",
            "Cài `void clamp_to(int *v, int lo, int hi)`: nếu *v dưới lo thì gán thành lo; trên hi thì thành hi; giữa khoảng thì giữ nguyên.",
            [("dưới", "Nâng lên sàn."), ("trên", "Hạ xuống trần."), ("trong khoảng", "Giữ nguyên."), ("biên dưới", "Chính lo thì giữ."), ("biên trên", "Chính hi thì giữ.")],
        ),
        "cb11-rotate3": vi_challenge(
            "Xoay ba chiều",
            "Cài `void rotate3(int *a, int *b, int *c)` dịch giá trị một bước: a nhận giá trị của b, b nhận của c, c nhận GIÁ TRỊ GỐC của a.",
            [("vòng tới", "Lưu một giá trị gốc trước khi ghi đè."), ("số âm", "Dấu đi cùng."), ("bằng nhau", "Xoay các số bằng nhau chẳng đổi gì.")],
        ),
        "cb11-sorted2": vi_challenge(
            "Sắp hai số, tại chỗ",
            "Cài `void order2(int *a, int *b)` để sau đó *a <= *b (chỉ hoán đổi khi cần).",
            [("cần hoán đổi", "Một lần gọi swap."), ("đã đúng thứ tự", "ĐỪNG hoán đổi khi đã theo thứ tự."), ("bằng nhau", "Bằng nhau vẫn bằng nhau.")],
        ),
    },
    solutions=[
        (
            "cb11-clamp-ptr",
            '#include <stdio.h>\nvoid clamp_to(int *v, int lo, int hi) {\n    if (*v < lo) *v = lo;\n    else if (*v > hi) *v = hi;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid clamp_to(int *v, int lo, int hi) {\n    if (*v < lo) *v = hi;\n    else if (*v > hi) *v = lo;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb11-rotate3",
            '#include <stdio.h>\nvoid rotate3(int *a, int *b, int *c) {\n    int t = *a;\n    *a = *b;\n    *b = *c;\n    *c = t;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid rotate3(int *a, int *b, int *c) {\n    *a = *b;\n    *b = *c;\n    *c = *a;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb11-sorted2",
            '#include <stdio.h>\nvoid order2(int *a, int *b) {\n    if (*a > *b) {\n        int t = *a;\n        *a = *b;\n        *b = t;\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\\nvoid order2(int *a, int *b) {\\n    if (*a > *b) {\\n        int t = *a;\\n        *a = *b;\\n    }\\n}\\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M11,
    "cb-p11-mistakes",
    "NULL Guard Duty",
    "Defensive pointer functions: reject NULL up front, refuse dangling inputs at compile time.",
    "Trực canh NULL",
    "Các hàm con trỏ phòng thủ: từ chối NULL ngay từ đầu, từ chối dữ liệu treo lúc biên dịch.",
    L11D,
    15,
    "beginner",
    [
        challenge(
            "cb11-safe-get",
            "Guarded Read",
            "Implement `int safe_get(const int *p, int fallback)`: return *p if p is not NULL, otherwise return fallback WITHOUT dereferencing.",
            C_PRELUDE,
            [
                ("real pointer", "int x = 42;\nCHECK_EQ(safe_get(&x, -1), 42);", "Normal case: read through."),
                ("null input", "CHECK_EQ(safe_get(NULL, -1), -1);", "NULL must return fallback, never crash."),
                ("null other fallback", "CHECK_EQ(safe_get(NULL, 7), 7);", "Whatever the caller asked for."),
            ],
            level="guided",
        ),
        challenge(
            "cb11-guarded-write",
            "Guarded Write",
            "Implement `int try_set(int *p, int value)`: if p is NULL return 0 and change nothing; otherwise store value and return 1.",
            C_PRELUDE,
            [
                ("success", "int x = 0;\nCHECK_EQ(try_set(&x, 9), 1);\nCHECK_EQ(x, 9);", "Report success as 1."),
                ("null rejected", "int ok = try_set(NULL, 9);\nCHECK_EQ(ok, 0);", "Return 0, write nothing."),
            ],
            level="independent",
        ),
        challenge(
            "cb11-pick-valid",
            "First Non-Null",
            "Implement `int* first_valid(int *a, int *b, int *c)` returning the first pointer that is not NULL; if all are NULL return NULL.",
            C_PRELUDE,
            [
                ("first wins", "int x = 1;\nCHECK_EQ(first_valid(&x, NULL, NULL), &x);", "Check a first."),
                ("second wins", "int y = 2;\nCHECK_EQ(first_valid(NULL, &y, NULL), &y);", "Then b."),
                ("third wins", "int z = 3;\nCHECK_EQ(first_valid(NULL, NULL, &z), &z);", "Then c."),
                ("all null", "CHECK_EQ(first_valid(NULL, NULL, NULL), NULL);", "Every one NULL: return NULL."),
            ],
            level="independent",
        ),
    ],
    {
        "cb11-safe-get": vi_challenge(
            "Đọc có bảo vệ",
            "Cài `int safe_get(const int *p, int fallback)`: trả *p nếu p khác NULL, còn không thì trả fallback mà KHÔNG giải tham chiếu.",
            [("con trỏ thật", "Trường hợp thường: đọc qua con trỏ."), ("đầu vào NULL", "NULL phải trả fallback, không bao giờ crash."), ("fallback khác", "Bất cứ điều gì người gọi yêu cầu.")],
        ),
        "cb11-guarded-write": vi_challenge(
            "Ghi có bảo vệ",
            "Cài `int try_set(int *p, int value)`: nếu p là NULL trả 0 và không đổi gì; ngược lại lưu value và trả 1.",
            [("thành công", "Báo thành công là 1."), ("từ chối NULL", "Trả 0, không ghi gì.")],
        ),
        "cb11-pick-valid": vi_challenge(
            "Con trỏ khác NULL đầu tiên",
            "Cài `int* first_valid(int *a, int *b, int *c)` trả con trỏ khác NULL đầu tiên; nếu cả ba đều NULL thì trả NULL.",
            [("thắng ở a", "Kiểm tra a trước."), ("thắng ở b", "Rồi tới b."), ("thắng ở c", "Rồi tới c."), ("toàn NULL", "Tất cả NULL: trả NULL.")],
        ),
    },
    solutions=[
        (
            "cb11-safe-get",
            '#include <stdio.h>\nint safe_get(const int *p, int fallback) {\n    if (p == NULL) return fallback;\n    return *p;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint safe_get(const int *p, int fallback) {\n    return *p;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb11-guarded-write",
            '#include <stdio.h>\nint try_set(int *p, int value) {\n    if (p == NULL) return 0;\n    *p = value;\n    return 1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint try_set(int *p, int value) {\n    *p = value;\n    return 1;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb11-pick-valid",
            '#include <stdio.h>\nint* first_valid(int *a, int *b, int *c) {\n    if (a != NULL) return a;\n    if (b != NULL) return b;\n    if (c != NULL) return c;\n    return NULL;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint* first_valid(int *a, int *b, int *c) {\n    if (a != NULL) return b;\n    if (b != NULL) return b;\n    if (c != NULL) return c;\n    return NULL;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M11,
    L11E,
    "Checkpoint: Pointers",
    "A stats pair with out-parameters, plus a NULL-safe accessor.",
    16,
    r"""
## Checkpoint

Out-parameters + NULL discipline = the daily bread of C interfaces.
""",
    "Điểm kiểm tra: Con trỏ",
    "Tham số xuất + kỷ luật NULL = cơm hằng ngày của giao diện C.",
    r"""
## Điểm kiểm tra

Tham số xuất + kỷ luật NULL = cơm hằng ngày của giao diện C.
""",
    challenge(
        "cb11-checkpoint-bounds",
        "Bounds Reporter",
        "Implement `void bounds(const int* a, int n, int *mn, int *mx)` storing the smallest element into *mn and the largest into *mx (n >= 1), and `int pick(const int* p, int alt)` returning *p when p is non-NULL else alt.",
        C_PRELUDE,
        [
            ("bounds basic", "int a[] = {3, 1, 4};\nint mn, mx;\nbounds(a, 3, &mn, &mx);\nCHECK_EQ(mn, 1);\nCHECK_EQ(mx, 4);", "Two scans or one — your choice."),
            ("bounds single", "int a[] = {7};\nint mn, mx;\nbounds(a, 1, &mn, &mx);\nCHECK_EQ(mn, 7);\nCHECK_EQ(mx, 7);", "One element: min and max agree."),
            ("bounds negatives", "int a[] = {-5, -2, -9};\nint mn, mx;\nbounds(a, 3, &mn, &mx);\nCHECK_EQ(mn, -9);\nCHECK_EQ(mx, -2);", "Works below zero."),
            ("pick null", "CHECK_EQ(pick(NULL, 5), 5);", "NULL means alt."),
            ("pick real", "int x = 9;\nCHECK_EQ(pick(&x, 5), 9);", "Non-NULL means *p."),
        ],
    ),
    vi_challenge(
        "Báo cáo biên độ",
        "Cài `void bounds(const int* a, int n, int *mn, int *mx)` lưu phần tử nhỏ nhất vào *mn và lớn nhất vào *mx (n >= 1), và `int pick(const int* p, int alt)` trả *p khi p khác NULL, nếu không trả alt.",
        [("bounds cơ bản", "Quét hai lần hoặc một — tùy bạn."), ("một phần tử", "Min và max trùng nhau."), ("số âm", "Hoạt động dưới 0."), ("pick NULL", "NULL nghĩa là alt."), ("pick thật", "Khác NULL nghĩa là *p.")],
    ),
    solution='#include <stdio.h>\nvoid bounds(const int* a, int n, int *mn, int *mx) {\n    int lo = a[0], hi = a[0];\n    for (int i = 1; i < n; i++) {\n        if (a[i] < lo) lo = a[i];\n        if (a[i] > hi) hi = a[i];\n    }\n    *mn = lo;\n    *mx = hi;\n}\nint pick(const int* p, int alt) {\n    if (p == NULL) return alt;\n    return *p;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\nvoid bounds(const int* a, int n, int *mn, int *mx) {\n    int lo = a[0], hi = a[0];\n    for (int i = 1; i < n; i++) {\n        if (a[i] < lo) lo = a[i];\n        if (a[i] > hi) hi = a[i];\n    }\n    mn = lo;\n    mx = hi;\n}\nint pick(const int* p, int alt) {\n    return alt;\n}\nint main(void) { return 0; }',
)

# ========================= MODULE 12: pointers-arrays =========================
M12 = "pointers-arrays"

L12A = "arrays-decay"
L12B = "pointer-arithmetic"
L12C = "cb-checkpoint-m12"

write_module(
    M12,
    "Pointers & Arrays",
    "Why array parameters are pointers, how +1 moves by one ELEMENT, and writing string functions by hand.",
    "Con trỏ & mảng",
    "Vì sao tham số mảng là con trỏ, cách +1 di chuyển đúng một PHẦN TỬ, và tự tay viết các hàm chuỗi.",
    [L12A, L12B, L12C],
    ["cb-p12-arithmetic", "cb-p12-stringfns"],
)

write_lesson(
    M12,
    L12A,
    "Arrays Decay to Pointers",
    "In expressions — especially function calls — an array name becomes a pointer to its first element.",
    14,
    r"""
## The decay rule

In most expressions, an array name **decays** to a pointer to its first
element:

```c
int a[5] = {5, 10, 15, 20, 25};
int *p = a;              // same as &a[0] — decay

printf("%p\n", (void*)a);     // address of a[0]
printf("%p\n", (void*)&a[0]); // identical
```

The crucial exception: `sizeof a` still knows the full array size (here 20 on
the sandbox's 64-bit int world: 5 × 4). Decay has not happened inside sizeof.

## What functions actually receive

```c
int sum(int arr[], int n)     // arr[] is NOTATION only
int sum(int *arr, int n)      // the compiler sees exactly this
```

The two prototypes are **identical** to the compiler. An array parameter is a
pointer; the array's size never travels with it — that's why `n` exists as a
second parameter. Inside the function, `sizeof arr` is the size of a pointer
(8), not the array.

## Consequence: functions can modify your array

Because the function receives the real address, writes through the parameter
change the caller's array:

```c
void zero_first(int arr[], int n) { arr[0] = 0; }
```

Arrays are the first "pass by reference" you meet in C — and the ONLY one,
until you choose it with pointers.
""",
    "Mảng suy biến thành con trỏ",
    "Trong biểu thức — đặc biệt là lời gọi hàm — tên mảng trở thành con trỏ tới phần tử đầu tiên.",
    r"""
## Quy tắc suy biến

Trong hầu hết biểu thức, tên mảng **suy biến** thành con trỏ tới phần tử đầu
tiên của nó:

```c
int a[5] = {5, 10, 15, 20, 25};
int *p = a;              // giống &a[0] — suy biến

printf("%p\n", (void*)a);     // địa chỉ của a[0]
printf("%p\n", (void*)&a[0]); // giống hệt
```

Ngoại lệ quan trọng: `sizeof a` vẫn biết kích thước toàn mảng (ở đây 20 với
int 64-bit của sandbox: 5 × 4). Bên trong sizeof, suy biến không xảy ra.

## Thứ hàm thực sự nhận được

```c
int sum(int arr[], int n)     // arr[] chỉ là CÁCH VIẾT
int sum(int *arr, int n)      // trình biên dịch nhìn thấy đúng cái này
```

Hai nguyên mẫu này **giống hệt nhau** với trình biên dịch. Tham số mảng là một
con trỏ; kích thước mảng không đi kèm — vì vậy `n` tồn tại như tham số thứ
hai. Bên trong hàm, `sizeof arr` là kích thước của một con trỏ (8), không
phải của mảng.

## Hệ quả: hàm có thể sửa mảng của bạn

Vì hàm nhận địa chỉ thật, ghi qua tham số sẽ thay đổi mảng của người gọi:

```c
void zero_first(int arr[], int n) { arr[0] = 0; }
```

Mảng là "truyền theo tham chiếu" đầu tiên bạn gặp trong C — và là duy nhất,
cho đến khi bạn tự chọn nó với con trỏ.
""",
)

write_lesson(
    M12,
    L12B,
    "Pointer Arithmetic",
    "p + 1 doesn't move one byte — it moves one ELEMENT, guided by the pointer's type.",
    15,
    r"""
## +1 means "one element further"

```c
int a[5] = {5, 10, 15, 20, 25};
int *p = a;          // &a[0]

printf("%d\n", *p);        // 5
printf("%d\n", *(p + 1));  // 10 — one INT further (4 bytes), not one byte
printf("%d\n", *(p + 2));  // 15
```

The compiler scales arithmetic by `sizeof(type)`: for `int*`, +1 is +4 bytes;
for `double*`, +1 is +8. That is why pointer types matter.

## Indexing IS pointer arithmetic

```c
a[i]  is defined as  *(a + i)
```

`a[3]`, `3[a]`, `*(a+3)` — all the same address. The bracket notation exists
for readability, not because it is a different mechanism.

## Walking with a pointer

```c
int *p = a;
int *end = a + 5;          // one PAST the last element — legal to hold
while (p < end) {
    printf("%d ", *p);
    p++;                    // advance one element
}
```

You may compute and compare pointers one past the end; dereferencing there is
undefined behavior.

## Subtraction gives distance

```c
int *p = &a[2];
printf("%ld\\n", (long)(p - a));   // 2 — element count, not bytes
```

## What is NOT legal

- arithmetic between unrelated arrays: `p1 - p2` where they point into
  different arrays — undefined
- dereferencing one-past-the-end, or any address outside the array
- scaling with pointers to incomplete objects
""",
    "Số học con trỏ",
    "p + 1 không di chuyển một byte — nó di chuyển một PHẦN TỬ, theo kiểu của con trỏ.",
    r"""
## +1 nghĩa là "tới phần tử kế tiếp"

```c
int a[5] = {5, 10, 15, 20, 25};
int *p = a;          // &a[0]

printf("%d\n", *p);        // 5
printf("%d\n", *(p + 1));  // 10 — xa thêm một INT (4 byte), không phải 1 byte
printf("%d\n", *(p + 2));  // 15
```

Trình biên dịch nhân số học với `sizeof(type)`: với `int*`, +1 là +4 byte;
với `double*`, +1 là +8. Đó là lý do kiểu con trỏ quan trọng.

## Đánh chỉ số CHÍNH LÀ số học con trỏ

```c
a[i]  được định nghĩa là  *(a + i)
```

`a[3]`, `3[a]`, `*(a+3)` — cùng một địa chỉ. Cú pháp ngoặc vuông tồn tại vì
tính dễ đọc, không phải vì nó là cơ chế khác.

## Đi bộ bằng con trỏ

```c
int *p = a;
int *end = a + 5;          // một vị trí SAU phần tử cuối — giữ thì hợp lệ
while (p < end) {
    printf("%d ", *p);
    p++;                    // tiến một phần tử
}
```

Bạn có thể tính và so sánh con trỏ một vị trí sau cuối; giải tham chiếu ở đó
là hành vi không xác định.

## Phép trừ cho khoảng cách

```c
int *p = &a[2];
printf("%ld\\n", (long)(p - a));   // 2 — đếm phần tử, không phải byte
```

## Điều KHÔNG hợp lệ

- số học giữa hai mảng không liên quan: `p1 - p2` khi chúng trỏ vào hai mảng
  khác nhau — không xác định
- giải tham chiếu vị trí sau-cuối, hoặc bất kỳ địa chỉ nào ngoài mảng
- nhân chia con trỏ trỏ tới đối tượng chưa hoàn chỉnh
""",
)

write_practice(
    M12,
    "cb-p12-arithmetic",
    "Arithmetic Workbench",
    "Functions computed with pure pointer arithmetic — no subscript brackets on the array.",
    "Bàn làm việc số học",
    "Các hàm tính thuần bằng số học con trỏ — không dùng ngoặc chỉ số trên mảng.",
    L12B,
    15,
    "beginner",
    [
        challenge(
            "cb12-ptr-sum",
            "Sum by Walker",
            "Implement `int sum_by_ptr(const int *begin, const int *end)` adding all elements from begin (inclusive) to end (exclusive) using ONLY pointer arithmetic — no [] indexing.",
            C_PRELUDE,
            [
                ("whole array", "int a[] = {1, 2, 3, 4};\nCHECK_EQ(sum_by_ptr(a, a + 4), 10);", "a + 4 is one past the last."),
                ("empty range", "int a[] = {9};\nCHECK_EQ(sum_by_ptr(a, a), 0);", "begin == end: empty."),
                ("middle slice", "int a[] = {1, 2, 3, 4};\nCHECK_EQ(sum_by_ptr(a + 1, a + 3), 5);", "Ranges can start anywhere."),
                ("negatives", "int a[] = {-1, -2, -3};\nCHECK_EQ(sum_by_ptr(a, a + 3), -6);", "Signs add."),
            ],
            level="guided",
        ),
        challenge(
            "cb12-copy-between",
            "Range Copy",
            "Implement `void copy_range(const int *src, int *dst, int n)` copying n elements WITHOUT [] (use *(src + i) or walking pointers).",
            C_PRELUDE,
            [
                ("full copy", "int s[] = {4, 5, 6};\nint d[3] = {0};\ncopy_range(s, d, 3);\nCHECK_EQ(d[0], 4);\nCHECK_EQ(d[2], 6);", "Element by element."),
                ("partial", "int s[] = {9, 8, 7, 6};\nint d[2] = {0};\ncopy_range(s + 1, d, 2);\nCHECK_EQ(d[0], 8);\nCHECK_EQ(d[1], 7);", "src can start mid-array."),
            ],
            level="independent",
        ),
        challenge(
            "cb12-find-ptr",
            "Find by Pointers",
            "Implement `const int* find_ptr(const int *begin, const int *end, int target)` returning a pointer to the first element equal to target, or end if absent. No [] allowed.",
            C_PRELUDE,
            [
                ("found", "int a[] = {2, 7, 4};\nCHECK_EQ(find_ptr(a, a + 3, 7), &a[1]);", "Return the ADDRESS of the match."),
                ("absent returns end", "int a[] = {2, 7, 4};\nCHECK_EQ(find_ptr(a, a + 3, 99), a + 3);", "end signals 'not found'."),
                ("first match", "int a[] = {5, 5};\nCHECK_EQ(find_ptr(a, a + 2, 5), a);", "Ties: earliest."),
            ],
            level="independent",
        ),
        challenge(
            "cb12-distance",
            "Distance Between",
            "Implement `long index_of(const int *begin, const int *end, int target)` returning the ELEMENT DISTANCE from begin to the first match, or -1 if absent. Compute with pointer subtraction on a found position.",
            C_PRELUDE,
            [
                ("middle", "int a[] = {10, 20, 30};\nCHECK_EQ(index_of(a, a + 3, 30), 2);", "p - begin is the index."),
                ("first", "int a[] = {10, 20};\nCHECK_EQ(index_of(a, a + 2, 10), 0);", "Distance 0 is valid."),
                ("absent", "int a[] = {10, 20};\nCHECK_EQ(index_of(a, a + 2, 99), -1);", "Not found keeps -1."),
            ],
            level="independent",
        ),
    ],
    {
        "cb12-ptr-sum": vi_challenge(
            "Tổng bằng con trỏ đi bộ",
            "Cài `int sum_by_ptr(const int *begin, const int *end)` cộng các phần tử từ begin (bao gồm) tới end (không gồm) CHỈ bằng số học con trỏ — không đánh chỉ số []",
            [("cả mảng", "a + 4 là vị trí sau phần tử cuối."), ("khoảng rỗng", "begin == end: rỗng."), ("đoạn giữa", "Khoảng có thể bắt đầu bất cứ đâu."), ("số âm", "Dấu cộng vào nhau.")],
        ),
        "cb12-copy-between": vi_challenge(
            "Chép theo khoảng",
            "Cài `void copy_range(const int *src, int *dst, int n)` chép n phần tử KHÔNG dùng [] (dùng *(src + i) hoặc con trỏ đi bộ).",
            [("chép đủ", "Từng phần tử một."), ("một phần", "src có thể bắt đầu giữa mảng.")],
        ),
        "cb12-find-ptr": vi_challenge(
            "Tìm bằng con trỏ",
            "Cài `const int* find_ptr(const int *begin, const int *end, int target)` trả con trỏ tới phần tử đầu tiên bằng target, hoặc end nếu không có. Cấm [].",
            [("thấy", "Trả ĐỊA CHỈ của phần tử khớp."), ("không có trả end", "end báo hiệu 'không tìm thấy'."), ("khớp đầu tiên", "Trùng nhau: lấy sớm nhất.")],
        ),
        "cb12-distance": vi_challenge(
            "Khoảng cách giữa hai con trỏ",
            "Cài `long index_of(const int *begin, const int *end, int target)` trả KHOẢNG CÁCH THEO PHẦN TỬ từ begin tới khớp đầu tiên, hoặc -1 nếu không có. Tính bằng phép trừ con trỏ trên vị trí đã thấy.",
            [("giữa", "p - begin chính là chỉ số."), ("đầu", "Khoảng cách 0 hợp lệ."), ("không có", "Không thấy thì giữ -1.")],
        ),
    },
    solutions=[
        (
            "cb12-ptr-sum",
            '#include <stdio.h>\nint sum_by_ptr(const int *begin, const int *end) {\n    int s = 0;\n    for (const int *p = begin; p < end; p++)\n        s += *p;\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint sum_by_ptr(const int *begin, const int *end) {\n    int s = 0;\n    for (const int *p = begin; p < end; p++)\n        s += p;\n    return s;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb12-copy-between",
            '#include <stdio.h>\nvoid copy_range(const int *src, int *dst, int n) {\n    for (int i = 0; i < n; i++)\n        *(dst + i) = *(src + i);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid copy_range(const int *src, int *dst, int n) {\n    for (int i = 0; i < n; i++)\n        *(dst + i) = src + i;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb12-find-ptr",
            '#include <stdio.h>\nconst int* find_ptr(const int *begin, const int *end, int target) {\n    for (const int *p = begin; p < end; p++)\n        if (*p == target) return p;\n    return end;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nconst int* find_ptr(const int *begin, const int *end, int target) {\n    for (const int *p = begin; p < end; p++)\n        if (p == target) return p;\n    return end;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb12-distance",
            '#include <stdio.h>\nlong index_of(const int *begin, const int *end, int target) {\n    for (const int *p = begin; p < end; p++)\n        if (*p == target) return p - begin;\n    return -1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nlong index_of(const int *begin, const int *end, int target) {\n    for (const int *p = begin; p < end; p++)\n        if (*p == target) return p + begin;\n    return -1;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M12,
    "cb-p12-stringfns",
    "String Functions by Hand",
    "Rebuild strlen, strcpy-style copy, and concatenation from first principles.",
    "Tự viết hàm chuỗi",
    "Dựng lại strlen, kiểu strcpy để chép, và nối chuỗi từ nền tảng.",
    L12B,
    15,
    "beginner",
    [
        challenge(
            "cb12-my-strlen",
            "my_strlen",
            "Implement `size_t my_strlen(const char *s)` counting characters up to (not including) the NUL terminator, WITHOUT calling strlen.",
            C_PRELUDE,
            [
                ("basic", "CHECK_EQ(my_strlen(\"hello\"), 5);", "Walk until *s == '\\\\0'."),
                ("empty", "CHECK_EQ(my_strlen(\"\"), 0);", "Empty string: terminator first."),
                ("single", "CHECK_EQ(my_strlen(\"x\"), 1);", "One char, then NUL."),
                ("spaces count", "CHECK_EQ(my_strlen(\"a b\"), 3);", "Every byte before NUL counts."),
            ],
            level="guided",
        ),
        challenge(
            "cb12-my-copy",
            "my_strcpy",
            "Implement `void my_strcpy(char *dst, const char *src)` copying src INCLUDING its NUL terminator into dst. Assume dst is large enough.",
            C_PRELUDE,
            [
                ("text", "char d[16] = {0};\nmy_strcpy(d, \"cat\");\nCHECK_STR_EQ(d, \"cat\");", "Copy chars, then the NUL."),
                ("terminator written", "char d[8] = {'x','x','x','x','x','x','x','x'};\nmy_strcpy(d, \"ab\");\nCHECK_EQ(d[2], '\\0');", "The destination must be terminated."),
                ("empty src", "char d[8];\nd[0] = 'q';\nmy_strcpy(d, \"\");\nCHECK_EQ(d[0], '\\0');", "Copying \"\" writes exactly one NUL."),
            ],
            level="independent",
        ),
        challenge(
            "cb12-my-append",
            "my_strcat",
            "Implement `void my_strcat(char *dst, const char *src)` appending src's characters to the END of dst's string (after dst's NUL), then terminating. dst is large enough.",
            C_PRELUDE,
            [
                ("append", "char d[16] = \"foo\";\nmy_strcat(d, \"bar\");\nCHECK_STR_EQ(d, \"foobar\");", "Find dst's NUL, then copy from there."),
                ("append empty", "char d[16] = \"abc\";\nmy_strcat(d, \"\");\nCHECK_STR_EQ(d, \"abc\");", "Appending nothing changes nothing."),
                ("onto empty", "char d[16] = \"\";\nmy_strcat(d, \"hi\");\nCHECK_STR_EQ(d, \"hi\");", "NUL at position 0: append writes at 0."),
            ],
            level="independent",
        ),
    ],
    {
        "cb12-my-strlen": vi_challenge(
            "my_strlen",
            "Cài `size_t my_strlen(const char *s)` đếm ký tự tới (không gồm) bộ kết thúc NUL, KHÔNG gọi strlen.",
            [("cơ bản", "Đi tới khi *s == '\\\\0'."), ("rỗng", "Chuỗi rỗng: gặp bộ kết thúc ngay."), ("một ký tự", "Một char rồi NUL."), ("dấu cách cũng đếm", "Mọi byte trước NUL đều được đếm.")],
        ),
        "cb12-my-copy": vi_challenge(
            "my_strcpy",
            "Cài `void my_strcpy(char *dst, const char *src)` chép src BAO GỒM bộ kết thúc NUL vào dst. Giả sử dst đủ lớn.",
            [("văn bản", "Chép ký tự, rồi NUL."), ("có ghi bộ kết thúc", "Đích phải được kết thúc."), ("src rỗng", "Chép \"\" ghi đúng một NUL.")],
        ),
        "cb12-my-append": vi_challenge(
            "my_strcat",
            "Cài `void my_strcat(char *dst, const char *src)` nối các ký tự của src vào CUỐI chuỗi của dst (sau NUL của dst), rồi kết thúc. dst đủ lớn.",
            [("nối", "Tìm NUL của dst, rồi chép từ đó."), ("nối rỗng", "Nối không có gì chẳng đổi gì."), ("nối vào rỗng", "NUL ở vị trí 0: nối ghi tại 0.")],
        ),
    },
    solutions=[
        (
            "cb12-my-strlen",
            '#include <stdio.h>\n#include <string.h>\nsize_t my_strlen(const char *s) {\n    size_t n = 0;\n    while (s[n] != \'\\0\') n++;\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nsize_t my_strlen(const char *s) {\n    size_t n = 0;\n    while (s[n] != \'\\0\') n++;\n    return n - 1;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb12-my-copy",
            '#include <stdio.h>\n#include <string.h>\nvoid my_strcpy(char *dst, const char *src) {\n    while (*src != \'\\0\') {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n    *dst = \'\\0\';\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nvoid my_strcpy(char *dst, const char *src) {\n    while (*src != \'\\0\') {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n}\nint main(void) { return 0; }',
        ),
        (
            "cb12-my-append",
            '#include <stdio.h>\n#include <string.h>\nvoid my_strcat(char *dst, const char *src) {\n    while (*dst != \'\\0\') dst++;\n    while (*src != \'\\0\') {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n    *dst = \'\\0\';\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nvoid my_strcat(char *dst, const char *src) {\n    while (*src != \'\\0\') {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n    *dst = \'\\0\';\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M12,
    L12C,
    "Checkpoint: Pointers & Arrays",
    "An in-place array transformation plus a hand-rolled scan, both pointer-driven.",
    16,
    r"""
## Checkpoint

Decay + arithmetic = the machinery behind every C array API you will ever use.
""",
    "Điểm kiểm tra: Con trỏ & mảng",
    "Suy biến + số học = cỗ máy đằng sau mọi API mảng C bạn sẽ từng dùng.",
    r"""
## Điểm kiểm tra

Suy biến + số học = cỗ máy đằng sau mọi API mảng C bạn sẽ từng dùng.
""",
    challenge(
        "cb12-checkpoint-scale",
        "Scalar Scale & Locate",
        "Implement `void scale(int *a, int n, int k)` multiplying the first n elements by k IN PLACE, and `const int* last_of(const int *begin, const int *end, int target)` returning a pointer to the LAST occurrence of target (or end if absent).",
        C_PRELUDE,
        [
            ("scale", "int a[] = {1, 2, 3};\nscale(a, 3, 10);\nCHECK_EQ(a[0], 10);\nCHECK_EQ(a[2], 30);", "Write through the pointer."),
            ("scale zero", "int a[] = {1, 2};\nscale(a, 2, 0);\nCHECK_EQ(a[0], 0);\nCHECK_EQ(a[1], 0);", "k=0 zeroes everything."),
            ("last of", "int a[] = {1, 2, 1, 2};\nCHECK_EQ(last_of(a, a + 4, 2), &a[3]);", "Scan forward, keep the latest match."),
            ("last of absent", "int a[] = {1, 2};\nCHECK_EQ(last_of(a, a + 2, 9), a + 2);", "Absent: end is the contract."),
            ("last of only", "int a[] = {5};\nCHECK_EQ(last_of(a, a + 1, 5), a);", "Single element."),
        ],
    ),
    vi_challenge(
        "Nhân bậc & định vị",
        "Cài `void scale(int *a, int n, int k)` nhân n phần tử đầu với k TẠI CHỖ, và `const int* last_of(const int *begin, const int *end, int target)` trả con trỏ tới lần xuất hiện CUỐI của target (hoặc end nếu không có).",
        [("scale", "Ghi qua con trỏ."), ("nhân 0", "k=0 đưa tất cả về 0."), ("last of", "Quét xuôi, giữ khớp mới nhất."), ("last of không có", "Không thấy: end là giao ước."), ("chỉ một phần tử", "Mảng một phần tử.")],
    ),
    solution='#include <stdio.h>\nvoid scale(int *a, int n, int k) {\n    for (int i = 0; i < n; i++)\n        a[i] = a[i] * k;\n}\nconst int* last_of(const int *begin, const int *end, int target) {\n    const int *found = end;\n    for (const int *p = begin; p < end; p++)\n        if (*p == target) found = p;\n    return found;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\nvoid scale(int *a, int n, int k) {\n    for (int i = 0; i < n; i++)\n        a[i] = a[i] + k;\n}\nconst int* last_of(const int *begin, const int *end, int target) {\n    const int *found = end;\n    for (const int *p = begin; p < end; p++)\n        if (*p == target) return p;\n    return found;\n}\nint main(void) { return 0; }',
)

print("batch 6 done: modules 11-12")
