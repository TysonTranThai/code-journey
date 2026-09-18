#!/usr/bin/env python3
"""C Beginner — batch 10: modules 20 (data-structures), 21 (algorithms),
22 (project-engineering + capstone)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ====================== MODULE 20: data-structures ======================
M20 = "data-structures"

L20A = "dynamic-array"
L20B = "linked-list"
L20C = "stack-queue"
L20D = "choosing-structures"
L20E = "cb-checkpoint-m20"

write_module(
    M20,
    "Data Structures Foundations",
    "Dynamic arrays, linked lists, stacks and queues — built by hand, chosen by trade-off.",
    "Nền tảng cấu trúc dữ liệu",
    "Mảng động, danh sách liên kết, ngăn xếp và hàng đợi — tự tay dựng, chọn theo đánh đổi.",
    [L20A, L20B, L20C, L20D, L20E],
    ["cb-p20-darray", "cb-p20-list"],
)

write_lesson(
    M20,
    L20A,
    "The Dynamic Array",
    "A heap buffer, a count, a capacity — and doubling when full.",
    15,
    r"""
## The three ingredients

```c
typedef struct {
    int *data;      // heap buffer (malloc/realloc)
    int size;       // elements used
    int cap;        // elements allocated
} DArray;
```

The invariant that keeps it honest: `0 <= size <= cap`, and `data` either
points at a valid allocation of `cap` ints or is NULL.

## Growing by doubling

```c
int da_push(DArray *a, int v) {
    if (a->size == a->cap) {
        int newcap = a->cap == 0 ? 4 : a->cap * 2;
        int *tmp = realloc(a->data, newcap * sizeof(int));
        if (tmp == NULL) return 0;        // old buffer still valid
        a->data = tmp;
        a->cap = newcap;
    }
    a->data[a->size++] = v;
    return 1;
}
```

Doubling makes N pushes cost O(N) copies TOTAL — the "amortized O(1)" push.

## Why this structure wins most of the time

- index access is O(1) — a single addition and multiply
- memory is contiguous — cache-friendly
- the only expensive operation is insertion in the MIDDLE (O(n) shifting)

Most beginner code should reach for a dynamic array first; fancier structures
must justify themselves.
""",
    "Mảng động",
    "Một bộ đệm heap, một biến số lượng, một dung lượng — và nhân đôi khi đầy.",
    r"""
## Ba thành phần

```c
typedef struct {
    int *data;      // bộ đệm heap (malloc/realloc)
    int size;       // số phần tử đang dùng
    int cap;        // số phần tử đã cấp phát
} DArray;
```

Bất biến giữ cho nó trung thực: `0 <= size <= cap`, và `data` hoặc trỏ tới
một vùng cấp phát hợp lệ gồm `cap` int hoặc là NULL.

## Phóng to bằng nhân đôi

```c
int da_push(DArray *a, int v) {
    if (a->size == a->cap) {
        int newcap = a->cap == 0 ? 4 : a->cap * 2;
        int *tmp = realloc(a->data, newcap * sizeof(int));
        if (tmp == NULL) return 0;        // bộ đệm cũ vẫn hợp lệ
        a->data = tmp;
        a->cap = newcap;
    }
    a->data[a->size++] = v;
    return 1;
}
```

Nhân đôi khiến N lần push tốn tổng cộng O(N) bản sao — push "khuyến mãi
O(1)".

## Vì sao cấu trúc này thắng phần lớn thời gian

- truy cập theo chỉ số là O(1) — một phép cộng và một phép nhân
- bộ nhớ liên tiếp — thân thiện với cache
- phép toán duy nhất đắt là chèn vào GIỮA (O(n) phải dời phần tử)

Đa số mã người mới nên chọn mảng động trước; cấu trúc cầu kỳ hơn phải tự
chứng minh lý do tồn tại.
""",
)

write_lesson(
    M20,
    L20B,
    "The Linked List",
    "Nodes connected by pointers: O(1) insertion at the head, O(n) to reach the middle.",
    15,
    r"""
## The node

```c
typedef struct Node {
    int value;
    struct Node *next;    // the tag lets it point at its own type
} Node;
```

A list is just a `Node *head`. An empty list is `head == NULL`. The last node
stores `next == NULL` — that is the end marker.

## Building and walking

```c
Node c = {3, NULL};
Node b = {2, &c};
Node a = {1, &b};       // list: 1 -> 2 -> 3
Node *head = &a;

for (Node *it = head; it != NULL; it = it->next) {
    printf("%d ", it->value);
}
```

## The trade-off against arrays

| operation | array | linked list |
|-----------|-------|-------------|
| access i-th | O(1) | O(n) — must walk |
| insert at head | O(n) — shift | O(1) — rewire two pointers |
| insert at known node | O(n) | O(1) |
| memory | one block | one malloc PER NODE |

## The classic bugs

- losing the rest of the list: rewiring `next` before saving it
- walking past the end: testing `it->next != NULL` when you meant `it != NULL`
- memory: heap nodes need one `free` each — who owns them?

Insert-at-head for practice:

```c
Node *push_front(Node *head, Node *n) {
    n->next = head;
    return n;               // new head
}
```
""",
    "Danh sách liên kết",
    "Các node nối với nhau bằng con trỏ: chèn vào đầu là O(1), chạm tới giữa là O(n).",
    r"""
## Node

```c
typedef struct Node {
    int value;
    struct Node *next;    // tag cho phép nó trỏ tới chính kiểu của mình
} Node;
```

Một danh sách chỉ là `Node *head`. Danh sách rỗng là `head == NULL`. Node cuối
giữ `next == NULL` — đó là dấu hiệu kết thúc.

## Dựng và đi bộ

```c
Node c = {3, NULL};
Node b = {2, &c};
Node a = {1, &b};       // danh sách: 1 -> 2 -> 3
Node *head = &a;

for (Node *it = head; it != NULL; it = it->next) {
    printf("%d ", it->value);
}
```

## Đánh đổi so với mảng

| thao tác | mảng | danh sách liên kết |
|-----------|-------|-------------|
| truy cập phần tử thứ i | O(1) | O(n) — phải đi bộ |
| chèn vào đầu | O(n) — phải dời | O(1) — nối lại hai con trỏ |
| chèn tại node đã biết | O(n) | O(1) |
| bộ nhớ | một khối | một malloc MỖI NODE |

## Các lỗi kinh điển

- đánh mất phần còn lại của danh sách: nối lại `next` trước khi giữ nó
- đi quá cuối: kiểm tra `it->next != NULL` trong khi ý là `it != NULL`
- bộ nhớ: node trên heap cần đúng một `free` mỗi node — ai sở hữu chúng?

Chèn vào đầu để luyện tập:

```c
Node *push_front(Node *head, Node *n) {
    n->next = head;
    return n;               // head mới
}
```
""",
)

write_lesson(
    M20,
    L20C,
    "Stack and Queue",
    "Two disciplines over the same storage: last-in-first-out and first-in-first-out.",
    14,
    r"""
## Stack: LIFO

Push and pop at ONE end. The most recent push is the next pop — like a stack
of plates.

```c
/* array-backed stack */
static int st[16];
static int top = 0;               // number of elements

int stack_push(int v) {
    if (top == 16) return 0;      // overflow
    st[top++] = v;
    return 1;
}
int stack_pop(int *out) {
    if (top == 0) return 0;       // underflow
    *out = st[--top];
    return 1;
}
```

Stacks power undo histories, expression evaluation, and function calls
themselves — "the call stack" is literally this.

## Queue: FIFO

Push at the back, pop from the front — a waiting line. With an array you
either shift everything (O(n) pop) or use a ring buffer: `head` and `tail`
indices that wrap around with `% cap`.

```c
tail = (tail + 1) % cap;    // wrap after the last slot
```

Module 18's FIFO module is exactly this; revisit it after this lesson.

## Picking between them

Ask: in what ORDER do items leave?
- most recent first → stack
- oldest first → queue
- by priority → heap (beyond this course)
""",
    "Ngăn xếp và hàng đợi",
    "Hai kỷ luật trên cùng một kho chứa: vào-sau-ra-trước và vào-trước-ra-trước.",
    r"""
## Ngăn xếp: LIFO

Push và pop tại MỘT đầu. Lần push gần nhất sẽ được pop tiếp theo — như một
xếp đĩa.

```c
/* ngăn xếp dựng trên mảng */
static int st[16];
static int top = 0;               // số phần tử

int stack_push(int v) {
    if (top == 16) return 0;      // tràn
    st[top++] = v;
    return 1;
}
int stack_pop(int *out) {
    if (top == 0) return 0;       // hụt
    *out = st[--top];
    return 1;
}
```

Ngăn xếp nuôi lệnh undo, việc tính biểu thức, và chính các lời gọi hàm —
"call stack" theo đúng nghĩa là cái này.

## Hàng đợi: FIFO

Push ở đuôi, pop ở đầu — một hàng chờ. Với mảng, bạn hoặc dời toàn bộ (pop
O(n)) hoặc dùng ring buffer: hai chỉ số `head` và `tail` quay vòng bằng
`% cap`.

```c
tail = (tail + 1) % cap;    // quay lại ô đầu sau ô cuối
```

Module FIFO ở module 18 chính là cái này; xem lại sau bài học này.

## Chọn giữa chúng

Hãy hỏi: các phần tử RỜI KHỎI theo thứ tự nào?
- mới nhất trước → ngăn xếp
- cũ nhất trước → hàng đợi
- theo độ ưu tiên → heap (ngoài phạm vi khóa này)
""",
)

write_lesson(
    M20,
    L20D,
    "Choosing a Structure",
    "Complexity classes in plain language, and a decision table you can carry.",
    12,
    r"""
## The vocabulary

- **O(1)**: cost independent of size — one arithmetic step
- **O(log n)**: halving each step — binary search
- **O(n)**: one pass over the data — summing an array
- **O(n log n)**: good sorting
- **O(n²)**: every element against every element — naive sorting

Numbers make it real: for n = 1,000,000, an O(n) scan is a million steps;
O(n²) is a trillion. Same hardware, different worlds.

## Reading a loop's complexity

```c
for (i = 0; i < n; i++)          // O(n)
for (i = 0; i < n; i++)          // O(n) — doubling i reaches n in log n steps
    i *= 2;
for (i = 0; i < n; i++)          // O(n²) — outer n times, inner n times
    for (j = 0; j < n; j++)
```

Nested loops multiply; sequential loops take the larger.

## The beginner decision table

| need | reach for |
|------|-----------|
| a list you index often | dynamic array |
| frequent inserts at the front | linked list |
| undo / matching brackets / DFS | stack |
| fair waiting lines, buffering | queue |
| fastest lookup by key | (hash table — later courses) |

## Measurement beats theory

When unsure, time it. C gives you `clock()`; even a crude before/after print
beats guessing. Theory picks the top 2 candidates; the stopwatch closes the
case.
""",
    "Chọn cấu trúc dữ liệu",
    "Các lớp độ phức tạp bằng ngôn ngữ đời thường, và một bảng quyết định mang theo được.",
    r"""
## Từ vựng

- **O(1)**: chi phí độc lập với kích thước — một bước số học
- **O(log n)**: chia đôi mỗi bước — tìm kiếm nhị phân
- **O(n)**: một lượt qua dữ liệu — cộng dồn một mảng
- **O(n log n)**: sắp xếp ngon lành
- **O(n²)**: mỗi phần tử đối chiếu mọi phần tử — sắp xếp ngây thơ

Con số cho thấy quy mô thật: với n = 1.000.000, quét O(n) là một triệu bước;
O(n²) là một nghìn tỷ. Cùng phần cứng, hai thế giới khác nhau.

## Đọc độ phức tạp của một vòng lặp

```c
for (i = 0; i < n; i++)          // O(n)
for (i = 0; i < n; i++)          // O(n) — nhân đôi i chạm n sau log n bước
    i *= 2;
for (i = 0; i < n; i++)          // O(n²) — ngoài n lần, trong n lần
    for (j = 0; j < n; j++)
```

Vòng lặp lồng nhau nhân; vòng lặp tuần tự lấy cái lớn hơn.

## Bảng quyết định cho người mới

| nhu cầu | chọn |
|------|-----------|
| danh sách hay đánh chỉ số | mảng động |
| chèn đầu danh sách thường xuyên | danh sách liên kết |
| undo / soi dấu ngoặc / DFS | ngăn xếp |
| hàng chờ công bằng, đệm dữ liệu | hàng đợi |
| tra cứu nhanh theo khóa | (bảng băm — khóa sau) |

## Đo đạc thắng lý thuyết

Khi phân vân, hãy bấm giờ. C cho bạn `clock()`; một cặp printf trước/sau còn
hơn đoán mò. Lý thuyết chọn ra 2 ứng viên sáng giá; đồng hồ kết án.
""",
)

write_practice(
    M20,
    "cb-p20-darray",
    "Dynamic Array Build",
    "Construct and operate a heap-backed dynamic array module.",
    "Dựng mảng động",
    "Dựng và vận hành module mảng động trên heap.",
    L20A,
    18,
    "beginner",
    [
        challenge(
            "cb20-da-create",
            "Create and Destroy",
            "Implement `DArray* da_create(int cap)` returning a heap-allocated DArray whose data is a heap array of cap ints (size 0), or NULL for cap <= 0 or allocation failure. Implement `void da_destroy(DArray *a)` freeing data and the struct itself (NULL-safe).",
            C_PRELUDE + "typedef struct { int *data; int size; int cap; } DArray;\n",
            [
                ("usable", "DArray *a = da_create(4);\nCHECK_NOT_NULL(a);\nCHECK_EQ(a->size, 0);\nCHECK_EQ(a->cap, 4);\nCHECK_NOT_NULL(a->data);\nda_destroy(a);", "Two allocations: the struct and its buffer."),
                ("bad cap", "CHECK_EQ(da_create(0), NULL);", "Non-positive capacity is rejected."),
            ],
            level="guided",
        ),
        challenge(
            "cb20-da-push-grow",
            "Push with Grow",
            "Given `int da_push(DArray *a, int v)` exists in spirit, implement `int da_push2(DArray *a, int v)`: append v; when size == cap, DOUBLE cap (cap 0 becomes 4) via realloc; return 1 on success, 0 on realloc failure (leaving the array intact).",
            C_PRELUDE + "#include <stdlib.h>\ntypedef struct { int *data; int size; int cap; } DArray;\n",
            [
                ("fill within cap", "DArray a = {NULL, 0, 0};\nCHECK_EQ(da_push2(&a, 7), 1);\nCHECK_EQ(a.size, 1);\nCHECK_EQ(a.data[0], 7);\nfree(a.data);", "Empty array grows to cap 4."),
                ("grows when full", "DArray a = {NULL, 0, 0};\nfor (int i = 0; i < 5; i++) da_push2(&a, i);\nCHECK_EQ(a.size, 5);\nCHECK_EQ(a.cap, 8);\nCHECK_EQ(a.data[4], 4);\nfree(a.data);", "Fifth push doubles 4 -> 8."),
                ("contents survive growth", "DArray a = {NULL, 0, 0};\nfor (int i = 0; i < 9; i++) da_push2(&a, i * 10);\nCHECK_EQ(a.data[0], 0);\nCHECK_EQ(a.data[8], 80);\nfree(a.data);", "realloc preserved every element."),
            ],
            level="independent",
        ),
        challenge(
            "cb20-da-get",
            "Bounds-checked Get",
            "Implement `int da_get(const DArray *a, int i, int fallback)`: return data[i] when 0 <= i < size, else fallback (never out of bounds).",
            C_PRELUDE + "typedef struct { int *data; int size; int cap; } DArray;\n",
            [
                ("inside", "int raw[3] = {5, 6, 7};\nDArray a = {raw, 3, 3};\nCHECK_EQ(da_get(&a, 1, -1), 6);", "Plain indexing."),
                ("below zero", "int raw[1] = {5};\nDArray a = {raw, 1, 1};\nCHECK_EQ(da_get(&a, -1, -1), -1);", "Negative index rejected."),
                ("at size", "int raw[2] = {5, 6};\nDArray a = {raw, 2, 2};\nCHECK_EQ(da_get(&a, 2, -1), -1);", "size is one past the last valid."),
            ],
            level="imitation",
        ),
    ],
    {
        "cb20-da-create": vi_challenge(
            "Tạo và hủy",
            "Cài `DArray* da_create(int cap)` trả về một DArray cấp phát trên heap mà data là mảng heap gồm cap int (size 0), hoặc NULL cho cap <= 0 hoặc cấp phát thất bại. Cài `void da_destroy(DArray *a)` free data và chính struct (an toàn với NULL).",
            [("dùng được", "Hai lần cấp phát: struct và bộ đệm của nó."), ("cap xấu", "Dung lượng không dương bị từ chối.")],
        ),
        "cb20-da-push-grow": vi_challenge(
            "Push có mở rộng",
            "Cài `int da_push2(DArray *a, int v)`: thêm v vào cuối; khi size == cap, NHÂN ĐÔI cap (cap 0 thành 4) qua realloc; trả 1 khi thành công, 0 khi realloc thất bại (giữ mảng nguyên vẹn).",
            [("đổ trong cap", "Mảng rỗng phóng lên cap 4."), ("đầy thì phóng", "Lần push thứ năm nhân đôi 4 -> 8."), ("dữ liệu sống qua lần phóng", "realloc bảo toàn mọi phần tử.")],
        ),
        "cb20-da-get": vi_challenge(
            "Get có kiểm tra biên",
            "Cài `int da_get(const DArray *a, int i, int fallback)`: trả data[i] khi 0 <= i < size, còn lại fallback (không bao giờ vượt biên).",
            [("trong khoảng", "Đánh chỉ số bình thường."), ("dưới 0", "Chỉ số âm bị từ chối."), ("tại size", "size là vị trí ngay sau phần tử hợp lệ cuối.")],
        ),
    },
    solutions=[
        (
            "cb20-da-create",
            '#include <stdio.h>\n#include <stdlib.h>\ntypedef struct { int *data; int size; int cap; } DArray;\nDArray* da_create(int cap) {\n    if (cap <= 0) return NULL;\n    DArray *a = malloc(sizeof(DArray));\n    if (a == NULL) return NULL;\n    a->data = calloc(cap, sizeof(int));\n    if (a->data == NULL) { free(a); return NULL; }\n    a->size = 0;\n    a->cap = cap;\n    return a;\n}\nvoid da_destroy(DArray *a) {\n    if (a == NULL) return;\n    free(a->data);\n    free(a);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\ntypedef struct { int *data; int size; int cap; } DArray;\nDArray* da_create(int cap) {\n    if (cap <= 0) return NULL;\n    DArray *a = malloc(sizeof(DArray));\n    if (a == NULL) return NULL;\n    a->data = calloc(cap, sizeof(int));\n    if (a->data == NULL) { free(a); return NULL; }\n    a->size = 0;\n    return a;\n}\nvoid da_destroy(DArray *a) {\n    if (a == NULL) return;\n    free(a->data);\n    free(a);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb20-da-push-grow",
            '#include <stdio.h>\n#include <stdlib.h>\ntypedef struct { int *data; int size; int cap; } DArray;\nint da_push2(DArray *a, int v) {\n    if (a->size == a->cap) {\n        int newcap = a->cap == 0 ? 4 : a->cap * 2;\n        int *tmp = realloc(a->data, newcap * sizeof(int));\n        if (tmp == NULL) return 0;\n        a->data = tmp;\n        a->cap = newcap;\n    }\n    a->data[a->size++] = v;\n    return 1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <stdlib.h>\ntypedef struct { int *data; int size; int cap; } DArray;\nint da_push2(DArray *a, int v) {\n    if (a->size == a->cap) {\n        int newcap = a->cap + 1;\n        int *tmp = realloc(a->data, newcap * sizeof(int));\n        if (tmp == NULL) return 0;\n        a->data = tmp;\n        a->cap = newcap;\n    }\n    a->data[a->size++] = v;\n    return 1;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb20-da-get",
            '#include <stdio.h>\ntypedef struct { int *data; int size; int cap; } DArray;\nint da_get(const DArray *a, int i, int fallback) {\n    if (i < 0 || i >= a->size) return fallback;\n    return a->data[i];\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct { int *data; int size; int cap; } DArray;\nint da_get(const DArray *a, int i, int fallback) {\n    if (i < 0 || i > a->size) return fallback;\n    return a->data[i];\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M20,
    "cb-p20-list",
    "Linked List Workbench",
    "Walk, count, and query chains of nodes.",
    "Bàn làm việc danh sách liên kết",
    "Đi bộ, đếm, và truy vấn chuỗi node.",
    L20B,
    16,
    "beginner",
    [
        challenge(
            "cb20-list-len",
            "List Length",
            "Implement `int list_len(const Node *head)` returning the number of nodes in the chain.",
            C_PRELUDE + "typedef struct Node { int value; struct Node *next; } Node;\n",
            [
                ("three", "Node c = {3, NULL};\nNode b = {2, &c};\nNode a = {1, &b};\nCHECK_EQ(list_len(&a), 3);", "Count until NULL."),
                ("single", "Node a = {9, NULL};\nCHECK_EQ(list_len(&a), 1);", "One node."),
                ("empty", "CHECK_EQ(list_len(NULL), 0);", "NULL is the empty list."),
            ],
            level="imitation",
        ),
        challenge(
            "cb20-list-sum",
            "List Sum",
            "Implement `int list_sum(const Node *head)` summing every node's value.",
            C_PRELUDE + "typedef struct Node { int value; struct Node *next; } Node;\n",
            [
                ("chain", "Node c = {3, NULL};\nNode b = {2, &c};\nNode a = {1, &b};\nCHECK_EQ(list_sum(&a), 6);", "1+2+3."),
                ("negatives", "Node b = {-5, NULL};\nNode a = {5, &b};\nCHECK_EQ(list_sum(&a), 0);", "Signs cancel."),
                ("empty", "CHECK_EQ(list_sum(NULL), 0);", "Empty sums to 0."),
            ],
            level="imitation",
        ),
        challenge(
            "cb20-list-find",
            "Find Node",
            "Implement `Node* list_find(Node *head, int target)` returning a pointer to the FIRST node holding target, or NULL.",
            C_PRELUDE + "typedef struct Node { int value; struct Node *next; } Node;\n",
            [
                ("middle", "Node c = {3, NULL};\nNode b = {2, &c};\nNode a = {1, &b};\nCHECK_EQ(list_find(&a, 2), &b);", "Return the node's address."),
                ("absent", "Node a = {1, NULL};\nCHECK_EQ(list_find(&a, 9), NULL);", "NULL when absent."),
                ("first", "Node b = {5, NULL};\nNode a = {5, &b};\nCHECK_EQ(list_find(&a, 5), &a);", "Earliest match."),
            ],
            level="guided",
        ),
        challenge(
            "cb20-list-max",
            "List Max Node",
            "Implement `Node* list_max(Node *head)` returning a pointer to the node with the LARGEST value (ties: the first), or NULL for the empty list.",
            C_PRELUDE + "typedef struct Node { int value; struct Node *next; } Node;\n",
            [
                ("basic", "Node c = {3, NULL};\nNode b = {9, &c};\nNode a = {1, &b};\nCHECK_EQ(list_max(&a), &b);", "Track the best node."),
                ("tie first", "Node b = {5, NULL};\nNode a = {5, &b};\nCHECK_EQ(list_max(&a), &a);", "Strictly greater to replace."),
                ("empty", "CHECK_EQ(list_max(NULL), NULL);", "Empty list: NULL."),
            ],
            level="independent",
        ),
    ],
    {
        "cb20-list-len": vi_challenge(
            "Độ dài danh sách",
            "Cài `int list_len(const Node *head)` trả về số node trong chuỗi.",
            [("ba node", "Đếm tới khi gặp NULL."), ("một node", "Một node."), ("rỗng", "NULL là danh sách rỗng.")],
        ),
        "cb20-list-sum": vi_challenge(
            "Tổng danh sách",
            "Cài `int list_sum(const Node *head)` cộng giá trị của mọi node.",
            [("chuỗi", "1+2+3."), ("số âm", "Dấu triệt tiêu."), ("rỗng", "Danh sách rỗng cộng ra 0.")],
        ),
        "cb20-list-find": vi_challenge(
            "Tìm node",
            "Cài `Node* list_find(Node *head, int target)` trả con trỏ tới node ĐẦU TIÊN chứa target, hoặc NULL.",
            [("ở giữa", "Trả địa chỉ của node."), ("không có", "NULL khi vắng mặt."), ("đầu tiên", "Khớp sớm nhất.")],
        ),
        "cb20-list-max": vi_challenge(
            "Node lớn nhất",
            "Cài `Node* list_max(Node *head)` trả con trỏ tới node có giá trị LỚN NHẤT (bằng nhau: lấy đầu tiên), hoặc NULL cho danh sách rỗng.",
            [("cơ bản", "Theo dõi node tốt nhất."), ("hòa lấy trước", "Chỉ thay khi LỚN HƠN hẳn."), ("rỗng", "Danh sách rỗng: NULL.")],
        ),
    },
    solutions=[
        (
            "cb20-list-len",
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nint list_len(const Node *head) {\n    int n = 0;\n    for (const Node *it = head; it != NULL; it = it->next) n++;\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nint list_len(const Node *head) {\n    int n = 0;\n    for (const Node *it = head; it != NULL; it = it->next->next) n++;\n    return n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb20-list-sum",
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nint list_sum(const Node *head) {\n    int s = 0;\n    for (const Node *it = head; it != NULL; it = it->next) s += it->value;\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nint list_sum(const Node *head) {\n    int s = 0;\n    for (const Node *it = head; it != NULL; it = it->next) s = it->value;\n    return s;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb20-list-find",
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nNode* list_find(Node *head, int target) {\n    for (Node *it = head; it != NULL; it = it->next)\n        if (it->value == target) return it;\n    return NULL;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nNode* list_find(Node *head, int target) {\n    for (Node *it = head; it != NULL; it = it->next->next)\n        if (it->value == target) return it;\n    return NULL;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb20-list-max",
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nNode* list_max(Node *head) {\n    Node *best = NULL;\n    for (Node *it = head; it != NULL; it = it->next)\n        if (best == NULL || it->value > best->value) best = it;\n    return best;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct Node { int value; struct Node *next; } Node;\nNode* list_max(Node *head) {\n    Node *best = NULL;\n    for (Node *it = head; it != NULL; it = it->next)\n        if (best == NULL || it->value < best->value) best = it;\n    return best;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M20,
    L20E,
    "Checkpoint: Data Structures",
    "An array-backed stack with full discipline: overflow, underflow, and size.",
    16,
    r"""
## Checkpoint

One structure, four operations, every edge case guarded.
""",
    "Điểm kiểm tra: Cấu trúc dữ liệu",
    "Một ngăn xếp trên mảng với kỷ luật trọn vẹn: tràn, hụt, và kích thước.",
    r"""
## Điểm kiểm tra

Một cấu trúc, bốn thao tác, mọi trường hợp biên đều được bảo vệ.
""",
    challenge(
        "cb20-checkpoint-stack",
        "Stack Complete",
        "Implement an int stack with capacity 16: `void stack_clear(void)`, `int stack_push(int v)` (0 on overflow), `int stack_pop(int *out)` (0 on underflow or out==NULL; else 1 and the MOST RECENT value), `int stack_size(void)`, and `int stack_top(int *out)` (peeks without removing; same contract as pop).",
        C_PRELUDE,
        [
            ("lifo", "stack_clear();\nstack_push(1);\nstack_push(2);\nint v;\nstack_pop(&v);\nCHECK_EQ(v, 2);", "Last in, first out."),
            ("overflow", "stack_clear();\nfor (int i = 0; i < 16; i++) stack_push(i);\nCHECK_EQ(stack_push(99), 0);\nCHECK_EQ(stack_size(), 16);", "The 17th is rejected."),
            ("underflow", "stack_clear();\nint v;\nCHECK_EQ(stack_pop(&v), 0);", "Popping empty fails."),
            ("size", "stack_clear();\nstack_push(5);\nstack_push(6);\nCHECK_EQ(stack_size(), 2);", "Count tracks pushes."),
            ("top peeks", "stack_clear();\nstack_push(4);\nint v;\nCHECK_EQ(stack_top(&v), 1);\nCHECK_EQ(v, 4);\nCHECK_EQ(stack_size(), 1);", "Top does not remove."),
            ("null out", "stack_clear();\nstack_push(4);\nCHECK_EQ(stack_pop(NULL), 0);", "NULL out is rejected."),
        ],
    ),
    vi_challenge(
        "Ngăn xếp trọn vẹn",
        "Cài ngăn xếp int với sức chứa 16: `void stack_clear(void)`, `int stack_push(int v)` (0 khi tràn), `int stack_pop(int *out)` (0 khi hụt hoặc out==NULL; nếu không 1 và giá trị MỚI NHẤT), `int stack_size(void)`, và `int stack_top(int *out)` (nhìn mà không lấy; cùng giao ước với pop).",
        [("lifo", "Vào sau, ra trước."), ("tràn", "Phần tử thứ 17 bị từ chối."), ("hụt", "Pop trên stack rỗng thất bại."), ("kích thước", "Đếm theo lần push."), ("top nhìn", "Top không lấy ra."), ("out NULL", "NULL out bị từ chối.")],
    ),
    solution='#include <stdio.h>\n#define SCAP 16\nstatic int st[SCAP];\nstatic int stop = 0;\nvoid stack_clear(void) { stop = 0; }\nint stack_push(int v) {\n    if (stop == SCAP) return 0;\n    st[stop++] = v;\n    return 1;\n}\nint stack_pop(int *out) {\n    if (out == NULL || stop == 0) return 0;\n    *out = st[--stop];\n    return 1;\n}\nint stack_size(void) { return stop; }\nint stack_top(int *out) {\n    if (out == NULL || stop == 0) return 0;\n    *out = st[stop - 1];\n    return 1;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\n#define SCAP 16\nstatic int st[SCAP];\nstatic int stop = 0;\nvoid stack_clear(void) { stop = 0; }\nint stack_push(int v) {\n    if (stop == SCAP) return 0;\n    st[stop++] = v;\n    return 1;\n}\nint stack_pop(int *out) {\n    if (out == NULL || stop == 0) return 0;\n    *out = st[0];\n    stop--;\n    return 1;\n}\nint stack_size(void) { return stop; }\nint stack_top(int *out) {\n    if (out == NULL || stop == 0) return 0;\n    *out = st[stop - 1];\n    return 1;\n}\nint main(void) { return 0; }',
)

# ========================= MODULE 21: algorithms =========================
M21 = "algorithms"

L21A = "searching"
L21B = "sorting-basics"
L21C = "recursion-intro"
L21D = "cb-checkpoint-m21"

write_module(
    M21,
    "Algorithms & Problem Solving",
    "Searching, sorting, recursion — and the reasoning that picks the right tool.",
    "Thuật toán & Giải quyết vấn đề",
    "Tìm kiếm, sắp xếp, đệ quy — và lập luận chọn đúng công cụ.",
    [L21A, L21B, L21C, L21D],
    ["cb-p21-search", "cb-p21-sort"],
)

write_lesson(
    M21,
    L21A,
    "Searching: Linear and Binary",
    "O(n) scan vs O(log n) halving — and why sortedness buys speed.",
    14,
    r"""
## Linear search: works always

```c
int find(const int *a, int n, int t) {
    for (int i = 0; i < n; i++)
        if (a[i] == t) return i;
    return -1;
}
```

No preconditions. Cost: up to n comparisons.

## Binary search: needs sorted data

The repeated middle test:

```c
int bsearch_cj(const int *a, int n, int t) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;    // avoids overflow
        if (a[mid] == t) return mid;
        if (a[mid] < t) lo = mid + 1;    // target is in the RIGHT half
        else            hi = mid - 1;    // target is in the LEFT half
    }
    return -1;
}
```

Each iteration halves the remaining range: a million elements take ~20 steps.

## The invariants that make it correct

- the target, if present, is always within [lo, hi]
- `lo + (hi - lo) / 2` never overflows (unlike `(lo + hi) / 2` on huge ranges)
- loop ends when lo passes hi — absence is proven, not guessed

## Choosing

Unsorted data or one-off lookups → linear. Sorted data queried repeatedly →
binary (sorting once costs O(n log n), then every query is nearly free).
""",
    "Tìm kiếm: tuyến tính và nhị phân",
    "Quét O(n) vs chia đôi O(log n) — và vì sao dữ liệu có thứ tự mua được tốc độ.",
    r"""
## Tìm tuyến tính: luôn dùng được

```c
int find(const int *a, int n, int t) {
    for (int i = 0; i < n; i++)
        if (a[i] == t) return i;
    return -1;
}
```

Không cần điều kiện tiên quyết. Chi phí: tới n phép so sánh.

## Tìm nhị phân: cần dữ liệu đã sắp xếp

Phép thử ở giữa lặp đi lặp lại:

```c
int bsearch_cj(const int *a, int n, int t) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;    // tránh tràn số
        if (a[mid] == t) return mid;
        if (a[mid] < t) lo = mid + 1;    // target nằm trong nửa PHẢI
        else            hi = mid - 1;    // target nằm trong nửa TRÁI
    }
    return -1;
}
```

Mỗi vòng lặp chia đôi khoảng còn lại: một triệu phần tử chỉ cần ~20 bước.

## Các bất biến làm nó đúng

- target, nếu có, luôn nằm trong [lo, hi]
- `lo + (hi - lo) / 2` không bao giờ tràn (khác với `(lo + hi) / 2` trên
  khoảng rất lớn)
- vòng lặp kết thúc khi lo vượt hi — sự vắng mặt được chứng minh, không phải
  đoán

## Lựa chọn

Dữ liệu chưa sắp xếp hoặc tra một lần → tuyến tính. Dữ liệu đã sắp xếp, truy
nhiều lần → nhị phân (sắp xếp một lần tốn O(n log n), rồi mỗi truy vấn gần
như miễn phí).
""",
)

write_lesson(
    M21,
    L21B,
    "Sorting Basics",
    "Selection and insertion sort — O(n²) teachers that make O(n log n) make sense later.",
    15,
    r"""
## Selection sort: pick the smallest, put it front

```c
void selection_sort(int *a, int n) {
    for (int i = 0; i < n - 1; i++) {
        int min = i;
        for (int j = i + 1; j < n; j++)
            if (a[j] < a[min]) min = j;
        int t = a[i]; a[i] = a[min]; a[min] = t;   // swap into place
    }
}
```

Invariant: after pass i, the first i+1 elements are the i+1 smallest, sorted.
Always ~n²/2 comparisons — predictable, in-place, easy to verify.

## Insertion sort: grow a sorted prefix

```c
void insertion_sort(int *a, int n) {
    for (int i = 1; i < n; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {   // shift bigger elements right
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}
```

On nearly-sorted data it approaches O(n) — that is why real libraries build
their top-tier sorts on insertion sort for small or nearly-ordered runs.

## What "in place" means

Both algorithms rearrange the array they are given — O(1) extra memory. The
caller sees the permutation; nothing new is allocated.

## Testing a sort

Check: empty, single, already sorted, reverse sorted, duplicates, negatives.
A sort that survives that battery is usually right — the same battery the
graders run below.
""",
    "Sắp xếp cơ bản",
    "Selection và insertion sort — những người thầy O(n²) giúp O(n log n) sau này dễ hiểu.",
    r"""
## Selection sort: chọn nhỏ nhất, đặt lên trước

```c
void selection_sort(int *a, int n) {
    for (int i = 0; i < n - 1; i++) {
        int min = i;
        for (int j = i + 1; j < n; j++)
            if (a[j] < a[min]) min = j;
        int t = a[i]; a[i] = a[min]; a[min] = t;   // hoán đổi vào chỗ
    }
}
```

Bất biến: sau lượt thứ i, i+1 phần tử đầu tiên là i+1 phần tử nhỏ nhất, đã
có thứ tự. Luôn khoảng n²/2 phép so sánh — đoán trước được, tại chỗ, dễ
kiểm chứng.

## Insertion sort: nuôi một tiền tố có thứ tự

```c
void insertion_sort(int *a, int n) {
    for (int i = 1; i < n; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {   // dời phần tử lớn hơn sang phải
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}
```

Trên dữ liệu gần như có thứ tự, nó tiến gần O(n) — vì sao thư viện thật dựng
các sort hạng nặng trên insertion sort cho các đoạn nhỏ hoặc gần có thứ tự.

## "Tại chỗ" nghĩa là gì

Cả hai thuật toán xáo lại đúng mảng được đưa vào — bộ nhớ thêm O(1). Người
gọi nhìn thấy hoán vị; không cấp phát gì mới.

## Kiểm thử một hàm sắp xếp

Kiểm tra: rỗng, một phần tử, đã sắp xếp, sắp ngược, trùng giá trị, số âm.
Một hàm sort sống sót qua bộ test đó thường là đúng — cũng chính là bộ test
bộ chấm chạy dưới đây.
""",
)

write_lesson(
    M21,
    L21C,
    "Recursion Introduction",
    "A function that calls itself: base case, recursive case, progress.",
    13,
    r"""
## The three requirements

Every correct recursion has:

1. a **base case** — an input answered directly, no call
2. a **recursive case** — answer built from a call on a SMALLER input
3. **progress** — every call moves toward the base case

```c
long fact(int n) {
    if (n <= 1) return 1;        // base case
    return n * fact(n - 1);      // smaller input, guaranteed progress
}
```

Miss the base case or the progress and you get infinite recursion — which
crashes with **stack overflow**: every call takes a stack frame, and the
stack is finite.

## The call stack picture

`fact(4)` → `fact(3)` → `fact(2)` → `fact(1)`: four frames deep, then the
answers multiply on the way back up. Depth = n, so fact(100000) is not a
thing to attempt.

## Where recursion shines

Structurally recursive data: trees, nested lists, divide-and-conquer. For a
flat loop over an array, recursion usually adds frames without adding
clarity — the iterative form is the honest tool there.

## A trace to internalize

```c
int sum_digits(int n) {
    if (n < 10) return n;             // single digit
    return n % 10 + sum_digits(n / 10);
}
// sum_digits(472) = 2 + sum_digits(47)
//                 = 2 + (7 + sum_digits(4))
//                 = 2 + (7 + 4) = 13
```,
""",
    "Giới thiệu đệ quy",
    "Một hàm tự gọi chính nó: trường hợp nền, trường hợp đệ quy, sự tiến triển.",
    r"""
## Ba yêu cầu

Mọi đệ quy đúng đều có:

1. một **trường hợp nền** — đầu vào được trả lời ngay, không gọi thêm
2. một **trường hợp đệ quy** — đáp án dựng từ lời gọi trên đầu vào NHỎ HƠN
3. **sự tiến triển** — mỗi lời gọi tiến gần trường hợp nền

```c
long fact(int n) {
    if (n <= 1) return 1;        // trường hợp nền
    return n * fact(n - 1);      // đầu vào nhỏ hơn, tiến triển chắc chắn
}
```

Thiếu trường hợp nền hoặc sự tiến triển là ra đệ quy vô hạn — crash với
**stack overflow**: mỗi lời gọi chiếm một khung ngăn xếp, và ngăn xếp có hạn.

## Bức tranh call stack

`fact(4)` → `fact(3)` → `fact(2)` → `fact(1)`: sâu bốn khung, rồi các đáp án
nhân ngược trở lên. Độ sâu = n, nên đừng thử fact(100000).

## Đệ quy tỏa sáng ở đâu

Dữ liệu có cấu trúc đệ quy: cây, danh sách lồng nhau, chia-để-trị. Với vòng
lặp phẳng trên mảng, đệ quy thường chỉ thêm khung mà không thêm sự rõ ràng —
dạng lặp mới là công cụ trung thực ở đó.

## Một vết trace để thuộc

```c
int sum_digits(int n) {
    if (n < 10) return n;             // một chữ số
    return n % 10 + sum_digits(n / 10);
}
// sum_digits(472) = 2 + sum_digits(47)
//                 = 2 + (7 + sum_digits(4))
//                 = 2 + (7 + 4) = 13
```,
""",
)

write_practice(
    M21,
    "cb-p21-search",
    "Search Practice",
    "Linear scans with contracts, and a binary search that must respect sortedness.",
    "Luyện tìm kiếm",
    "Quét tuyến tính với giao ước rõ, và một tìm nhị phân tôn trọng thứ tự sắp xếp.",
    L21A,
    15,
    "beginner",
    [
        challenge(
            "cb21-count-greater",
            "Count Greater",
            "Implement `int count_greater(const int *a, int n, int t)` counting elements strictly greater than t.",
            C_PRELUDE,
            [
                ("basic", "int a[] = {1, 5, 8, 3};\nCHECK_EQ(count_greater(a, 4, 4), 2);", "5 and 8 beat 4."),
                ("none", "int a[] = {1, 2};\nCHECK_EQ(count_greater(a, 2, 100), 0);", "Nothing qualifies."),
                ("strict", "int a[] = {4, 4};\nCHECK_EQ(count_greater(a, 2, 4), 0);", "Equal is not greater."),
            ],
            level="imitation",
        ),
        challenge(
            "cb21-binary-search",
            "Binary Search",
            "Implement `int binary_search_cj(const int *a, int n, int t)` on an ASCENDING-sorted array: return any index of t, or -1. Use the halving loop.",
            C_PRELUDE,
            [
                ("first", "int a[] = {2, 4, 6, 8, 10};\nCHECK_EQ(binary_search_cj(a, 5, 2), 0);", "Lo boundary."),
                ("last", "int a[] = {2, 4, 6, 8, 10};\nCHECK_EQ(binary_search_cj(a, 5, 10), 4);", "Hi boundary."),
                ("middle", "int a[] = {2, 4, 6, 8, 10};\nCHECK_EQ(binary_search_cj(a, 5, 6), 2);", "First split hits it."),
                ("absent below", "int a[] = {2, 4, 6};\nCHECK_EQ(binary_search_cj(a, 3, 1), -1);", "Below the range."),
                ("absent above", "int a[] = {2, 4, 6};\nCHECK_EQ(binary_search_cj(a, 3, 9), -1);", "Above the range."),
                ("absent middle", "int a[] = {2, 4, 8};\nCHECK_EQ(binary_search_cj(a, 3, 5), -1);", "Inside a gap."),
                ("single found", "int a[] = {7};\nCHECK_EQ(binary_search_cj(a, 1, 7), 0);", "One element."),
                ("single absent", "int a[] = {7};\nCHECK_EQ(binary_search_cj(a, 1, 3), -1);", "One element, miss."),
            ],
            level="independent",
        ),
        challenge(
            "cb21-find-first-ge",
            "First >= Threshold",
            "On an ascending array, implement `int first_ge(const int *a, int n, int t)` returning the index of the FIRST element >= t, or -1 if none. (Binary search variant — linear is acceptable but halving is the habit to build.)",
            C_PRELUDE,
            [
                ("inside", "int a[] = {1, 3, 5, 7};\nCHECK_EQ(first_ge(a, 4, 4), 2);", "5 is the first >= 4."),
                ("at boundary", "int a[] = {1, 3, 5, 7};\nCHECK_EQ(first_ge(a, 4, 3), 1);", "Equal counts."),
                ("all below", "int a[] = {1, 2};\nCHECK_EQ(first_ge(a, 2, 9), -1);", "None qualify."),
                ("all above", "int a[] = {5, 6};\nCHECK_EQ(first_ge(a, 2, 0), 0);", "Index 0 qualifies."),
            ],
            level="independent",
        ),
    ],
    {
        "cb21-count-greater": vi_challenge(
            "Đếm lớn hơn",
            "Cài `int count_greater(const int *a, int n, int t)` đếm phần tử lớn hơn t NGHIÊM NGỈT.",
            [("cơ bản", "5 và 8 vượt 4."), ("không có", "Không phần tử nào đạt."), ("nghiêm ngặt", "Bằng nhau không phải lớn hơn.")],
        ),
        "cb21-binary-search": vi_challenge(
            "Tìm kiếm nhị phân",
            "Cài `int binary_search_cj(const int *a, int n, int t)` trên mảng đã sắp TĂNG DẦN: trả một chỉ số bất kỳ của t, hoặc -1. Dùng vòng chia đôi.",
            [("đầu", "Biên lo."), ("cuối", "Biên hi."), ("giữa", "Lần chia đầu trúng ngay."), ("thiếu dưới", "Dưới khoảng."), ("thiếu trên", "Trên khoảng."), ("thiếu giữa", "Rơi vào khe hở."), ("một phần tử thấy", "Một phần tử."), ("một phần tử trượt", "Một phần tử, hụt.")],
        ),
        "cb21-find-first-ge": vi_challenge(
            "Phần tử đầu >= ngưỡng",
            "Trên mảng tăng dần, cài `int first_ge(const int *a, int n, int t)` trả chỉ số của phần tử ĐẦU TIÊN >= t, hoặc -1 nếu không có. (Biến thể tìm nhị phân — tuyến tính được chấp nhận nhưng chia đôi mới là thói quen cần xây.)",
            [("trong khoảng", "5 là phần tử đầu >= 4."), ("tại biên", "Bằng nhau được tính."), ("tất cả dưới", "Không ai đạt."), ("tất cả trên", "Chỉ số 0 đạt.")],
        ),
    },
    solutions=[
        (
            "cb21-count-greater",
            '#include <stdio.h>\nint count_greater(const int *a, int n, int t) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (a[i] > t) c++;\n    return c;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint count_greater(const int *a, int n, int t) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (a[i] >= t) c++;\n    return c;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb21-binary-search",
            '#include <stdio.h>\nint binary_search_cj(const int *a, int n, int t) {\n    int lo = 0, hi = n - 1;\n    while (lo <= hi) {\n        int mid = lo + (hi - lo) / 2;\n        if (a[mid] == t) return mid;\n        if (a[mid] < t) lo = mid + 1;\n        else hi = mid - 1;\n    }\n    return -1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint binary_search_cj(const int *a, int n, int t) {\n    int lo = 0, hi = n - 1;\n    while (lo <= hi) {\n        int mid = lo + (hi - lo) / 2;\n        if (a[mid] == t) return mid;\n        if (a[mid] < t) hi = mid - 1;\n        else lo = mid + 1;\n    }\n    return -1;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb21-find-first-ge",
            '#include <stdio.h>\nint first_ge(const int *a, int n, int t) {\n    for (int i = 0; i < n; i++)\n        if (a[i] >= t) return i;\n    return -1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint first_ge(const int *a, int n, int t) {\n    for (int i = 0; i < n; i++)\n        if (a[i] > t) return i;\n    return -1;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M21,
    "cb-p21-sort",
    "Sort Practice",
    "Selection and insertion sort, plus a non-mutating median.",
    "Luyện sắp xếp",
    "Selection và insertion sort, cùng một hàm median không phá dữ liệu.",
    L21B,
    16,
    "beginner",
    [
        challenge(
            "cb21-selection-sort",
            "Selection Sort",
            "Implement `void selection_sort(int *a, int n)` sorting ascending in place.",
            C_PRELUDE,
            [
                ("basic", "int a[] = {3, 1, 2};\nselection_sort(a, 3);\nCHECK_EQ(a[0], 1);\nCHECK_EQ(a[2], 3);", "Smallest first."),
                ("sorted stays", "int a[] = {1, 2, 3};\nselection_sort(a, 3);\nCHECK_EQ(a[1], 2);", "Already ordered: no harm."),
                ("duplicates", "int a[] = {2, 1, 2};\nselection_sort(a, 3);\nCHECK_EQ(a[0], 1);\nCHECK_EQ(a[1], 2);\nCHECK_EQ(a[2], 2);", "Duplicates fine."),
                ("single", "int a[] = {5};\nselection_sort(a, 1);\nCHECK_EQ(a[0], 5);", "n=1 no-op."),
            ],
            level="guided",
        ),
        challenge(
            "cb21-insertion-sort",
            "Insertion Sort",
            "Implement `void insertion_sort(int *a, int n)` sorting ascending in place.",
            C_PRELUDE,
            [
                ("basic", "int a[] = {4, 2, 9, 1};\ninsertion_sort(a, 4);\nCHECK_EQ(a[0], 1);\nCHECK_EQ(a[3], 9);", "Grow the sorted prefix."),
                ("negatives", "int a[] = {-1, -9, 4};\ninsertion_sort(a, 3);\nCHECK_EQ(a[0], -9);\nCHECK_EQ(a[2], 4);", "Works below zero."),
                ("two", "int a[] = {9, 3};\ninsertion_sort(a, 2);\nCHECK_EQ(a[0], 3);\nCHECK_EQ(a[1], 9);", "Smallest case that moves."),
            ],
            level="guided",
        ),
        challenge(
            "cb21-median-nomutate",
            "Median Without Mutation",
            "Implement `double median(const int *a, int n)` returning the median WITHOUT modifying a: odd n -> middle of the sorted values; even n -> mean of the two middle values. Copy to a local buffer and sort it.",
            C_PRELUDE,
            [
                ("odd", "int a[] = {5, 1, 9};\nCHECK_NEAR(median(a, 3), 5.0, 1e-9);", "Sorted: 1,5,9."),
                ("even", "int a[] = {4, 1, 3, 2};\nCHECK_NEAR(median(a, 4), 2.5, 1e-9);", "(2+3)/2."),
                ("input intact", "int a[] = {9, 1};\nint keep[2] = {9, 1};\nmedian(a, 2);\nCHECK_EQ(a[0], keep[0]);\nCHECK_EQ(a[1], keep[1]);", "The caller's array is untouched."),
                ("single", "int a[] = {7};\nCHECK_NEAR(median(a, 1), 7.0, 1e-9);", "One element."),
            ],
            level="independent",
        ),
    ],
    {
        "cb21-selection-sort": vi_challenge(
            "Selection Sort",
            "Cài `void selection_sort(int *a, int n)` sắp tăng dần tại chỗ.",
            [("cơ bản", "Nhỏ nhất lên đầu."), ("đã có thứ tự", "Không làm hỏng gì."), ("trùng giá trị", "Trùng giá trị vẫn ổn."), ("một phần tử", "n=1 không làm gì.")],
        ),
        "cb21-insertion-sort": vi_challenge(
            "Insertion Sort",
            "Cài `void insertion_sort(int *a, int n)` sắp tăng dần tại chỗ.",
            [("cơ bản", "Nuôi tiền tố có thứ tự."), ("số âm", "Hoạt động dưới 0."), ("hai phần tử", "Trường hợp nhỏ nhất cần di chuyển.")],
        ),
        "cb21-median-nomutate": vi_challenge(
            "Median không phá dữ liệu",
            "Cài `double median(const int *a, int n)` trả median mà KHÔNG sửa a: n lẻ -> phần giữa của dãy đã sắp; n chẵn -> trung bình hai phần giữa. Chép sang bộ đệm cục bộ rồi sort.",
            [("lẻ", "Đã sắp: 1,5,9."), ("chẵn", "(2+3)/2."), ("đầu vào nguyên vẹn", "Mảng của người gọi không bị đụng tới."), ("một phần tử", "Một phần tử.")],
        ),
    },
    solutions=[
        (
            "cb21-selection-sort",
            '#include <stdio.h>\nvoid selection_sort(int *a, int n) {\n    for (int i = 0; i < n - 1; i++) {\n        int min = i;\n        for (int j = i + 1; j < n; j++)\n            if (a[j] < a[min]) min = j;\n        int t = a[i]; a[i] = a[min]; a[min] = t;\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid selection_sort(int *a, int n) {\n    for (int i = 0; i < n - 1; i++) {\n        int min = i;\n        for (int j = i + 1; j < n; j++)\n            if (a[j] > a[min]) min = j;\n        int t = a[i]; a[i] = a[min]; a[min] = t;\n    }\n}\nint main(void) { return 0; }',
        ),
        (
            "cb21-insertion-sort",
            '#include <stdio.h>\nvoid insertion_sort(int *a, int n) {\n    for (int i = 1; i < n; i++) {\n        int key = a[i];\n        int j = i - 1;\n        while (j >= 0 && a[j] > key) {\n            a[j + 1] = a[j];\n            j--;\n        }\n        a[j + 1] = key;\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid insertion_sort(int *a, int n) {\n    for (int i = 1; i < n; i++) {\n        int key = a[i];\n        int j = i - 1;\n        while (j >= 0 && a[j] < key) {\n            a[j + 1] = a[j];\n            j--;\n        }\n        a[j + 1] = key;\n    }\n}\nint main(void) { return 0; }',
        ),
        (
            "cb21-median-nomutate",
            '#include <stdio.h>\nvoid insertion_sort(int *b, int n) {\n    for (int i = 1; i < n; i++) {\n        int key = b[i];\n        int j = i - 1;\n        while (j >= 0 && b[j] > key) { b[j + 1] = b[j]; j--; }\n        b[j + 1] = key;\n    }\n}\ndouble median(const int *a, int n) {\n    int buf[64];\n    for (int i = 0; i < n; i++) buf[i] = a[i];\n    insertion_sort(buf, n);\n    if (n % 2 == 1) return (double)buf[n / 2];\n    return (buf[n / 2 - 1] + buf[n / 2]) / 2.0;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid insertion_sort(int *b, int n) {\n    for (int i = 1; i < n; i++) {\n        int key = b[i];\n        int j = i - 1;\n        while (j >= 0 && b[j] > key) { b[j + 1] = b[j]; j--; }\n        b[j + 1] = key;\n    }\n}\ndouble median(const int *a, int n) {\n    int buf[64];\n    for (int i = 0; i < n; i++) buf[i] = a[i];\n    insertion_sort(buf, n);\n    if (n % 2 == 1) return (double)buf[n / 2 + 1];\n    return (buf[n / 2 - 1] + buf[n / 2]) / 2.0;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M21,
    L21D,
    "Checkpoint: Algorithms",
    "Sort, then answer range queries — search and sort composing into one tool.",
    16,
    r"""
## Checkpoint

Sort once; answer many queries cheaply. That composition is the point.
""",
    "Điểm kiểm tra: Thuật toán",
    "Sort một lần; trả nhiều truy vấn rẻ. Sự kết hợp đó chính là ý nghĩa.",
    r"""
## Điểm kiểm tra

Sort một lần; trả nhiều truy vấn rẻ. Sự kết hợp đó chính là ý nghĩa.
""",
    challenge(
        "cb21-checkpoint-range",
        "Sorted Range Reporter",
        "Implement `void sort_asc(int *a, int n)` (any in-place algorithm) and `int in_range(const int *sorted_a, int n, int lo, int hi)` counting elements of the ALREADY-SORTED array within [lo, hi] inclusive. For full credit, in_range should exploit sortedness with a scan that can stop early (or binary search twice) — but a correct linear scan also passes.",
        C_PRELUDE,
        [
            ("sort", "int a[] = {5, 1, 3};\nsort_asc(a, 3);\nCHECK_EQ(a[0], 1);\nCHECK_EQ(a[2], 5);", "Ascending order."),
            ("range middle", "int a[] = {1, 3, 5, 7, 9};\nCHECK_EQ(in_range(a, 5, 3, 7), 3);", "3, 5, 7."),
            ("range edges", "int a[] = {1, 3, 5};\nCHECK_EQ(in_range(a, 3, 1, 5), 3);", "Inclusive bounds."),
            ("range none", "int a[] = {1, 3, 5};\nCHECK_EQ(in_range(a, 3, 10, 20), 0);", "Outside everything."),
        ],
    ),
    vi_challenge(
        "Báo cáo khoảng trên dãy đã sắp",
        "Cài `void sort_asc(int *a, int n)` (bất kỳ thuật toán tại chỗ nào) và `int in_range(const int *sorted_a, int n, int lo, int hi)` đếm phần tử của mảng ĐÃ SẮP trong [lo, hi] (bao gồm biên). Để được điểm tối đa, in_range nên tận dụng thứ tự sắp bằng quét dừng sớm (hoặc tìm nhị phân hai lần) — nhưng quét tuyến tính đúng vẫn qua.",
        [("sort", "Thứ tự tăng dần."), ("khoảng giữa", "3, 5, 7."), ("biên khoảng", "Hai biên đều gồm trong."), ("khoảng rỗng", "Ngoài tất cả.")],
    ),
    solution='#include <stdio.h>\nvoid sort_asc(int *a, int n) {\n    for (int i = 1; i < n; i++) {\n        int key = a[i];\n        int j = i - 1;\n        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; j--; }\n        a[j + 1] = key;\n    }\n}\nint in_range(const int *sorted_a, int n, int lo, int hi) {\n    int c = 0;\n    for (int i = 0; i < n; i++) {\n        if (sorted_a[i] > hi) break;\n        if (sorted_a[i] >= lo) c++;\n    }\n    return c;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\nvoid sort_asc(int *a, int n) {\n    for (int i = 1; i < n; i++) {\n        int key = a[i];\n        int j = i - 1;\n        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; j--; }\n        a[j + 1] = key;\n    }\n}\nint in_range(const int *sorted_a, int n, int lo, int hi) {\n    int c = 0;\n    for (int i = 0; i < n; i++) {\n        if (sorted_a[i] > hi) break;\n        if (sorted_a[i] > lo) c++;\n    }\n    return c;\n}\nint main(void) { return 0; }',
)

# =================== MODULE 22: project-engineering ===================
M22 = "project-engineering"

L22A = "build-workflow"
L22B = "project-layout"
L22C = "capstone-brief"
L22D = "cb-checkpoint-m22"

write_module(
    M22,
    "C Project Engineering & Capstone",
    "The build workflow, project layout, and a capstone that composes the whole course.",
    "Kỹ nghệ dự án C & Capstone",
    "Quy trình build, bố cục dự án, và một capstone gom trọn khóa học.",
    [L22A, L22B, L22C, L22D],
    ["cb-p22-quality", "cb-p22-decompose"],
)

write_lesson(
    M22,
    L22A,
    "The Build Workflow",
    "Compile, warn, link — the flags you will type for the rest of your C life.",
    14,
    r"""
## The commands

```sh
gcc -std=c23 -Wall -Wextra -c mathutil.c -o mathutil.o    # compile only
gcc -std=c23 main.c mathutil.o -o app                      # link
gcc -std=c23 -Wall -Wextra main.c mathutil.c -o app        # both at once
```

`-c` stops after compiling (object file, no linking). The final command
compiles AND links in one step — fine while projects are small.

## The flag vocabulary

| flag | meaning |
|------|---------|
| `-std=c23` | which C standard to enforce |
| `-Wall -Wextra` | the warning level this course assumes |
| `-Werror` | warnings become errors (CI builds) |
| `-O2` | optimize for speed (shipping) |
| `-g` | embed debug info (for gdb) |
| `-Iinclude` | add a header search path |
| `-lm` | link the math library |

Debug build: `-g` (plus sanitizers on glibc). Release build: `-O2 -DNDEBUG`.
Never ship what you have not also built with warnings on.

## Make in one screen

```make
app: main.o mathutil.o
	gcc main.o mathutil.o -o app

main.o: main.c mathutil.h
	gcc -std=c23 -Wall -Wextra -c main.c

mathutil.o: mathutil.c mathutil.h
	gcc -std=c23 -Wall -Wextra -c mathutil.c
```

Make rebuilds only what changed — the dependency graph is the Makefile.
Tab indentation is mandatory and famously unforgiving.
""",
    "Quy trình build",
    "Biên dịch, bật warning, liên kết — những cờ bạn sẽ gõ phần còn lại của đời lập trình C.",
    r"""
## Các lệnh

```sh
gcc -std=c23 -Wall -Wextra -c mathutil.c -o mathutil.o    # chỉ biên dịch
gcc -std=c23 main.c mathutil.o -o app                      # liên kết
gcc -std=c23 -Wall -Wextra main.c mathutil.c -o app        # cả hai một bước
```

`-c` dừng sau khi biên dịch (tệp object, chưa liên kết). Lệnh cuối biên dịch
VÀ liên kết cùng lúc — ổn khi dự án còn nhỏ.

## Từ vựng cờ

| cờ | nghĩa |
|------|---------|
| `-std=c23` | bắt buộc chuẩn C nào |
| `-Wall -Wextra` | mức warning khóa này mặc định |
| `-Werror` | warning biến thành lỗi (build CI) |
| `-O2` | tối ưu tốc độ (khi xuất bản) |
| `-g` | nhúng thông tin debug (cho gdb) |
| `-Iinclude` | thêm đường tìm header |
| `-lm` | liên kết thư viện toán |

Build debug: `-g` (cộng sanitizer trên glibc). Build release: `-O2 -DNDEBUG`.
Đừng bao giờ xuất bản thứ bạn chưa từng build với warning bật.

## Make trong một màn hình

```make
app: main.o mathutil.o
	gcc main.o mathutil.o -o app

main.o: main.c mathutil.h
	gcc -std=c23 -Wall -Wextra -c main.c

mathutil.o: mathutil.c mathutil.h
	gcc -std=c23 -Wall -Wextra -c mathutil.c
```

Make chỉ dựng lại cái đã đổi — đồ thị phụ thuộc chính là Makefile. Thụt lề
bằng TAB là bắt buộc và nổi tiếng là không khoan nhượng.
""",
)

write_lesson(
    M22,
    L22B,
    "Project Layout & Quality Bar",
    "Where files live, what the README owes, and the habits that keep a C project reviewable.",
    13,
    r"""
## A layout that scales

```text
project/
  include/           # public headers (the contracts)
    mathutil.h
  src/               # implementations
    main.c
    mathutil.c
  tests/             # test programs (a main per concern)
  Makefile
  README.md
```

The rule: `include/` headers are what OTHERS may use; everything in `src/`
is free to reorganize. Tests live outside `src/` so they never ship inside
the product binary.

## The README's minimum

- what the program does (one paragraph)
- how to build (the exact commands)
- how to run + expected output
- known limitations

## The quality bar you have now reached

- every function small enough to read without scrolling
- warnings clean under `-Wall -Wextra`
- every allocation has one obvious owner
- NULL/guard checks at every boundary you cannot control
- tests with known answers — reproducible with one command

## Git in two paragraphs

Commit small, commit often, write messages that say WHY. Never commit build
artifacts (`.o`, binaries) — a `.gitignore` handles it. A branch per feature;
merge when the feature passes its tests. That is 90% of professional Git
discipline for a project this size.
""",
    "Bố cục dự án & Chuẩn chất lượng",
    "Tệp sống ở đâu, README nợ gì, và những thói quen giữ cho dự án C đủ khả năng review.",
    r"""
## Một bố cục có thể lớn lên

```text
project/
  include/           # header công khai (các hợp đồng)
    mathutil.h
  src/               # phần cài đặt
    main.c
    mathutil.c
  tests/             # chương trình test (một main cho mỗi mối quan tâm)
  Makefile
  README.md
```

Quy tắc: header trong `include/` là thứ NGƯỜI KHÁC được dùng; mọi thứ trong
`src/` được phép tổ chức lại tự do. Test nằm ngoài `src/` để không bao giờ
đóng gói vào binary sản phẩm.

## Mức tối thiểu của README

- chương trình làm gì (một đoạn)
- cách build (lệnh chính xác)
- cách chạy + đầu ra mong đợi
- giới hạn đã biết

## Chuẩn chất lượng bạn vừa chạm tới

- mỗi hàm nhỏ đến mức đọc không cần cuộn
- warning sạch dưới `-Wall -Wextra`
- mỗi vùng cấp phát có đúng một chủ sở hữu rõ ràng
- kiểm tra NULL/guard tại mọi ranh giới bạn không kiểm soát
- test với đáp án đã biết — tái lập bằng một lệnh

## Git trong hai đoạn văn

Commit nhỏ, commit thường, viết message nói rõ VÌ SAO. Không bao giờ commit
sản phẩm build (`.o`, binary) — `.gitignore` lo việc đó. Một branch cho mỗi
tính năng; merge khi tính năng qua test. Đó là 90% kỷ luật Git chuyên nghiệp
cho một dự án cỡ này.
""",
)

write_lesson(
    M22,
    L22C,
    "Capstone Brief: The Finance Core",
    "One program composing structs, pointers, dynamic memory, files, and algorithms.",
    12,
    r"""
## The mission

A **personal finance core** — the computation and persistence heart of a
ledger app, built from everything this course taught:

- a `Txn` record: id, cents amount, category
- operations: add, category totals, biggest expense, report line
- validation at every boundary

## What the graders check

The capstone battery runs against four functions:

1. `total_by_cat` — category-filtered sums
2. `biggest_idx` — the index of the largest expense
3. `after_balance` — running balance from a start value
4. `fmt_report` — one exact summary line, built with snprintf

## Why these four

They force every layer at once: structs (records), pointers (arrays and out
buffers), const discipline (read-only inputs), algorithms (max scan),
and formatting (report). Change any piece and the whole thing still must
hold together — that is integration, the actual skill of engineering.

## Beyond the battery

In a real project you would add: file persistence (module 16 — a save/load
pair), a menu loop (module 5-6), and unit tests per function. The sandbox
battery verifies the core logic; the architecture around it is yours to
build in the project gallery.
""",
    "Đề bài Capstone: Lõi tài chính",
    "Một chương trình gộp struct, con trỏ, bộ nhớ động, tệp, và thuật toán.",
    r"""
## Nhiệm vụ

Một **lõi tài chính cá nhân** — trái tim tính toán và lưu trữ của ứng dụng sổ
sách, dựng từ mọi thứ khóa học đã dạy:

- một bản ghi `Txn`: id, số tiền (cents), danh mục
- các thao tác: thêm, tổng theo danh mục, khoản chi lớn nhất, dòng báo cáo
- kiểm tra hợp lệ tại mọi ranh giới

## Bộ chấm kiểm tra gì

Bộ capstone chạy với bốn hàm:

1. `total_by_cat` — tổng lọc theo danh mục
2. `biggest_idx` — chỉ số của khoản chi lớn nhất
3. `after_balance` — số dư chạy dồn từ một giá trị ban đầu
4. `fmt_report` — một dòng tổng kết chính xác, dựng bằng snprintf

## Vì sao là bốn hàm này

Chúng ép mọi tầng cùng lúc: struct (bản ghi), con trỏ (mảng và bộ đệm xuất),
kỷ luật const (đầu vào chỉ đọc), thuật toán (quét max), và định dạng (báo
cáo). Thay bất kỳ mảnh nào thì tổng thể vẫn phải giữ vững — đó là tích hợp,
kỹ năng thật sự của kỹ nghệ phần mềm.

## Ngoài bộ test

Trong dự án thật, bạn sẽ thêm: lưu tệp (module 16 — cặp save/load), vòng
menu (module 5-6), và unit test cho từng hàm. Bộ test sandbox xác minh lõi
logic; kiến trúc xung quanh là phần của bạn để dựng trong gallery dự án.
""",
)

write_practice(
    M22,
    "cb-p22-quality",
    "Quality Gate",
    "A bracket checker (the classic stack application) and a formatting contract.",
    "Cổng chất lượng",
    "Trình kiểm tra dấu ngoặc (ứng dụng kinh điển của stack) và một hợp đồng định dạng.",
    L22A,
    16,
    "beginner",
    [
        challenge(
            "cb22-brackets",
            "Bracket Checker (mini-build)",
            "Implement `int brackets_ok(const char *s)` returning 1 when every '(' has a matching ')' in proper order (and likewise nothing unclosed at the end), else 0. Use a counter or a stack — both pass.",
            C_PRELUDE,
            [
                ("balanced", "CHECK_EQ(brackets_ok(\"(a(b)c)\"), 1);", "Every open closes."),
                ("empty", "CHECK_EQ(brackets_ok(\"\"), 1);", "Nothing to mismatch."),
                ("unmatched close", "CHECK_EQ(brackets_ok(\"a)b(\"), 0);", "Close before open fails."),
                ("leftover open", "CHECK_EQ(brackets_ok(\"(a\"), 0);", "Trailing open fails."),
                ("deep nesting", "CHECK_EQ(brackets_ok(\"((()))\"), 1);", "Depth three survives."),
            ],
            level="mini-build",
        ),
        challenge(
            "cb22-fmt-money",
            "Money Formatter",
            "Implement `void fmt_cents(int cents, char *out)` writing `<dollars>.<NN>` where NN is the two-digit remainder (e.g. 1234 -> \"12.34\", 5 -> \"0.05\", -250 -> \"-2.50\"). Use snprintf.",
            C_PRELUDE,
            [
                ("positive", "char b[32] = {0};\nfmt_cents(1234, b);\nCHECK_STR_EQ(b, \"12.34\");", "1234 cents = 12.34."),
                ("sub-dollar", "char b[32] = {0};\nfmt_cents(5, b);\nCHECK_STR_EQ(b, \"0.05\");", "Zero dollars, two digits."),
                ("negative", "char b[32] = {0};\nfmt_cents(-250, b);\nCHECK_STR_EQ(b, \"-2.50\");", "Sign and padded cents."),
                ("zero", "char b[32] = {0};\nfmt_cents(0, b);\nCHECK_STR_EQ(b, \"0.00\");", "Zero is 0.00."),
            ],
            level="independent",
        ),
    ],
    {
        "cb22-brackets": vi_challenge(
            "Kiểm tra dấu ngoặc (mini-build)",
            "Cài `int brackets_ok(const char *s)` trả 1 khi mọi '(' có một ')' khớp theo đúng thứ tự (và cuối chuỗi không sót gì mở), ngược lại 0. Dùng biến đếm hoặc stack — cách nào cũng qua.",
            [("cân bằng", "Mỗi dấu mở có dấu đóng."), ("rỗng", "Không gì để lệch."), ("đóng thừa", "Đóng trước mở là fail."), ("sót mở", "Dấu mở bị bỏ lại là fail."), ("lồng sâu", "Độ sâu ba vẫn sống.")],
        ),
        "cb22-fmt-money": vi_challenge(
            "Định dạng tiền",
            "Cài `void fmt_cents(int cents, char *out)` ghi `<đô>.<NN>` với NN là phần dư hai chữ số (vd 1234 -> \"12.34\", 5 -> \"0.05\", -250 -> \"-2.50\"). Dùng snprintf.",
            [("dương", "1234 cents = 12.34."), ("dưới một đô", "Không đô, hai chữ số."), ("âm", "Dấu và cents đệm đủ."), ("số 0", "Zero là 0.00.")],
        ),
    },
    solutions=[
        (
            "cb22-brackets",
            '#include <stdio.h>\nint brackets_ok(const char *s) {\n    int depth = 0;\n    for (; *s; s++) {\n        if (*s == \'(\') depth++;\n        else if (*s == \')\') {\n            depth--;\n            if (depth < 0) return 0;\n        }\n    }\n    return depth == 0;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint brackets_ok(const char *s) {\n    int depth = 0;\n    for (; *s; s++) {\n        if (*s == \'(\') depth++;\n        else if (*s == \')\') depth--;\n    }\n    return depth == 0;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb22-fmt-money",
            '#include <stdio.h>\nvoid fmt_cents(int cents, char *out) {\n    int sign = 1;\n    if (cents < 0) { sign = -1; cents = -cents; }\n    if (sign < 0)\n        snprintf(out, 32, "-%d.%02d", cents / 100, cents % 100);\n    else\n        snprintf(out, 32, "%d.%02d", cents / 100, cents % 100);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid fmt_cents(int cents, char *out) {\n    snprintf(out, 32, "%d.%02d", cents / 100, cents % 10);\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M22,
    "cb-p22-decompose",
    "Decomposition Drill",
    "Split a problem into small testable functions, then compose them.",
    "Bài tập phân rã",
    "Chia bài toán thành các hàm nhỏ kiểm thử được, rồi ghép lại.",
    L22C,
    16,
    "beginner",
    [
        challenge(
            "cb22-txn-total",
            "Category Totals",
            "Given the Txn model in scope, implement `int total_by_cat(const Txn *txs, int n, int cat)` summing cents of transactions whose category equals cat.",
            C_PRELUDE + "typedef struct { int id; int cents; int cat; } Txn;\n",
            [
                ("filters", "Txn t[] = {{1, 500, 1}, {2, 200, 2}, {3, 300, 1}};\nCHECK_EQ(total_by_cat(t, 3, 1), 800);", "500 + 300."),
                ("none", "Txn t[] = {{1, 500, 1}};\nCHECK_EQ(total_by_cat(t, 1, 9), 0);", "Unknown category: 0."),
                ("empty", "Txn t[1];\nCHECK_EQ(total_by_cat(t, 0, 1), 0);", "n=0: 0."),
            ],
            level="guided",
        ),
        challenge(
            "cb22-txn-biggest",
            "Biggest Expense",
            "Given the Txn model in scope, implement `int biggest_idx(const Txn *txs, int n)` returning the INDEX of the transaction with the largest cents (ties: lowest index), or -1 for n == 0.",
            C_PRELUDE + "typedef struct { int id; int cents; int cat; } Txn;\n",
            [
                ("basic", "Txn t[] = {{1, 500, 1}, {2, 900, 2}, {3, 100, 1}};\nCHECK_EQ(biggest_idx(t, 3), 1);", "Index 1 is largest."),
                ("tie", "Txn t[] = {{1, 700, 1}, {2, 700, 2}};\nCHECK_EQ(biggest_idx(t, 2), 0);", "Lowest index wins ties."),
                ("empty", "Txn t[1];\nCHECK_EQ(biggest_idx(t, 0), -1);", "n=0: -1."),
            ],
            level="guided",
        ),
        challenge(
            "cb22-balance",
            "Running Balance",
            "Given the Txn model in scope, implement `int after_balance(const Txn *txs, int n, int start)` returning start plus every transaction's cents (expenses are negative cents).",
            C_PRELUDE + "typedef struct { int id; int cents; int cat; } Txn;\n",
            [
                ("mixed", "Txn t[] = {{1, -200, 1}, {2, 1000, 2}, {3, -300, 1}};\nCHECK_EQ(after_balance(t, 3, 500), 1000);", "500 - 200 + 1000 - 300."),
                ("empty", "Txn t[1];\nCHECK_EQ(after_balance(t, 0, 42), 42);", "No transactions: unchanged."),
                ("all negative", "Txn t[] = {{1, -100, 1}, {2, -50, 1}};\nCHECK_EQ(after_balance(t, 2, 100), -50);", "Can go below zero."),
            ],
            level="independent",
        ),
    ],
    {
        "cb22-txn-total": vi_challenge(
            "Tổng theo danh mục",
            "Với mô hình Txn có sẵn, cài `int total_by_cat(const Txn *txs, int n, int cat)` cộng cents của các giao dịch có danh mục bằng cat.",
            [("lọc", "500 + 300."), ("không có", "Danh mục lạ: 0."), ("rỗng", "n=0: 0.")],
        ),
        "cb22-txn-biggest": vi_challenge(
            "Khoản chi lớn nhất",
            "Với mô hình Txn có sẵn, cài `int biggest_idx(const Txn *txs, int n)` trả CHỈ SỐ của giao dịch có cents lớn nhất (bằng nhau: chỉ số nhỏ nhất), hoặc -1 khi n == 0.",
            [("cơ bản", "Chỉ số 1 lớn nhất."), ("hòa", "Chỉ số nhỏ hơn thắng."), ("rỗng", "n=0: -1.")],
        ),
        "cb22-balance": vi_challenge(
            "Số dư chạy dồn",
            "Với mô hình Txn có sẵn, cài `int after_balance(const Txn *txs, int n, int start)` trả start cộng cents của mọi giao dịch (khoản chi là số âm).",
            [("hỗn hợp", "500 - 200 + 1000 - 300."), ("rỗng", "Không giao dịch: giữ nguyên."), ("toàn âm", "Có thể xuống dưới 0.")],
        ),
    },
    solutions=[
        (
            "cb22-txn-total",
            '#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint total_by_cat(const Txn *txs, int n, int cat) {\n    int s = 0;\n    for (int i = 0; i < n; i++)\n        if (txs[i].cat == cat) s += txs[i].cents;\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint total_by_cat(const Txn *txs, int n, int cat) {\n    int s = 0;\n    for (int i = 0; i < n; i++)\n        if (txs[i].cat != cat) s += txs[i].cents;\n    return s;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb22-txn-biggest",
            '#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint biggest_idx(const Txn *txs, int n) {\n    if (n == 0) return -1;\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (txs[i].cents > txs[best].cents) best = i;\n    return best;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint biggest_idx(const Txn *txs, int n) {\n    if (n == 0) return -1;\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (txs[i].cents < txs[best].cents) best = i;\n    return best;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb22-balance",
            '#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint after_balance(const Txn *txs, int n, int start) {\n    int bal = start;\n    for (int i = 0; i < n; i++)\n        bal += txs[i].cents;\n    return bal;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint after_balance(const Txn *txs, int n, int start) {\n    int bal = start;\n    for (int i = 0; i < n; i++)\n        bal = txs[i].cents;\n    return bal;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M22,
    L22D,
    "Capstone: The Finance Core",
    "Compose the whole course: records, scans, balance math, and an exact report line.",
    20,
    r"""
## Capstone

Four functions, one coherent core. Every module you cleared is in the room.
""",
    "Capstone: Lõi tài chính",
    "Bốn hàm, một lõi gắn kết. Mỗi module bạn đã vượt qua đều góp mặt ở đây.",
    r"""
## Capstone

Bốn hàm, một lõi gắn kết. Mỗi module bạn đã vượt qua đều góp mặt ở đây.
""",
    challenge(
        "cb22-checkpoint-capstone",
        "Finance Core Complete",
        "Given the Txn model in scope, implement all four: `int total_by_cat(const Txn *txs, int n, int cat)` (sum of cents in category cat), `int biggest_idx(const Txn *txs, int n)` (index of largest cents, ties lowest index, -1 for n==0), `int after_balance(const Txn *txs, int n, int start)` (start + all cents), and `void fmt_report(const Txn *txs, int n, int start, char *out)` writing `txns=<n> balance=<b>` where b is after_balance (snprintf).",
        C_PRELUDE + "typedef struct { int id; int cents; int cat; } Txn;\n",
        [
            ("total", "Txn t[] = {{1, 500, 1}, {2, 200, 2}, {3, 300, 1}};\nCHECK_EQ(total_by_cat(t, 3, 1), 800);", "Category filter."),
            ("biggest", "Txn t[] = {{1, 500, 1}, {2, 900, 2}};\nCHECK_EQ(biggest_idx(t, 2), 1);", "Max scan."),
            ("biggest empty", "Txn t[1];\nCHECK_EQ(biggest_idx(t, 0), -1);", "Empty contract."),
            ("balance", "Txn t[] = {{1, -200, 1}, {2, 1000, 2}};\nCHECK_EQ(after_balance(t, 2, 100), 900);", "100 - 200 + 1000."),
            ("report", "Txn t[] = {{1, -200, 1}, {2, 1000, 2}};\nchar b[64] = {0};\nfmt_report(t, 2, 100, b);\nCHECK_STR_EQ(b, \"txns=2 balance=900\");", "Compose after_balance into the line."),
        ],
    ),
    vi_challenge(
        "Lõi tài chính trọn vẹn",
        "Với mô hình Txn có sẵn, cài cả bốn: `int total_by_cat(const Txn *txs, int n, int cat)` (tổng cents theo danh mục), `int biggest_idx(const Txn *txs, int n)` (chỉ số cents lớn nhất, hòa lấy chỉ số nhỏ, -1 khi n==0), `int after_balance(const Txn *txs, int n, int start)` (start + mọi cents), và `void fmt_report(const Txn *txs, int n, int start, char *out)` ghi `txns=<n> balance=<b>` với b là after_balance (snprintf).",
        [("total", "Lọc theo danh mục."), ("biggest", "Quét max."), ("biggest rỗng", "Giao ước rỗng."), ("balance", "100 - 200 + 1000."), ("report", "Ghép after_balance vào dòng.")],
    ),
    solution='#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint total_by_cat(const Txn *txs, int n, int cat) {\n    int s = 0;\n    for (int i = 0; i < n; i++)\n        if (txs[i].cat == cat) s += txs[i].cents;\n    return s;\n}\nint biggest_idx(const Txn *txs, int n) {\n    if (n == 0) return -1;\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (txs[i].cents > txs[best].cents) best = i;\n    return best;\n}\nint after_balance(const Txn *txs, int n, int start) {\n    int bal = start;\n    for (int i = 0; i < n; i++)\n        bal += txs[i].cents;\n    return bal;\n}\nvoid fmt_report(const Txn *txs, int n, int start, char *out) {\n    snprintf(out, 64, "txns=%d balance=%d", n, after_balance(txs, n, start));\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\ntypedef struct { int id; int cents; int cat; } Txn;\nint total_by_cat(const Txn *txs, int n, int cat) {\n    int s = 0;\n    for (int i = 0; i < n; i++)\n        if (txs[i].cat == cat) s += txs[i].cents;\n    return s;\n}\nint biggest_idx(const Txn *txs, int n) {\n    if (n == 0) return -1;\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (txs[i].cents > txs[best].cents) best = i;\n    return best;\n}\nint after_balance(const Txn *txs, int n, int start) {\n    int bal = start;\n    for (int i = 0; i < n; i++)\n        bal += txs[i].cents;\n    return bal;\n}\nvoid fmt_report(const Txn *txs, int n, int start, char *out) {\n    snprintf(out, 64, "txns=%d balance=%d", n, start);\n}\nint main(void) { return 0; }',
)

print("batch 10 done: modules 20-22")
