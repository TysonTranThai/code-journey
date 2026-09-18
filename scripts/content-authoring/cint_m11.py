#!/usr/bin/env python3
"""C — Intermediate — Module 11: cint-trees.

Trees and heaps: BST insert/search/height by recursion, in-order gives
sorted order, array-backed binary heaps with the index arithmetic that
replaces pointers. Ownership carried over from Module 7: every node
freed exactly once, post-order. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-trees"

write_module(
    M,
    "Trees & Heaps",
    "Hierarchy with O(log n) ambitions: BSTs where order does the work, "
    "heaps where the array does the work.",
    "Cây & Heap",
    "Phân cấp với tham vọng O(log n): BST nơi thứ tự làm việc, heap nơi "
    "mảng làm việc.",
    lessons=["bst-basics", "bst-delete", "binary-heaps", "cint-checkpoint-m11"],
    practices=["cint-p11-bst", "cint-p11-heap"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "bst-basics",
    "Binary Search Trees",
    "The order invariant does the searching: insert, find, traversals, "
    "and why one deletion can restructure everything.",
    18,
    r"""
## The invariant is the algorithm

```c
typedef struct TNode {
    int           value;
    struct TNode *left, *right;   /* left < value < right (no dups) */
} TNode;
```

Every node's left subtree holds smaller values, right holds larger.
Search descends one path — O(h) where h is height:

```c
int bst_find(const TNode *t, int v) {
    while (t) {
        if (v == t->value) return 1;
        t = (v < t->value) ? t->left : t->right;
    }
    return 0;
}
```

Insert walks the same path and attaches at the empty slot. All three
traversals are two lines of recursion; **in-order** (left, self, right)
visits values in *sorted order* — the property an entire family of
algorithms rests on.

## Height is the fine print

A balanced tree of n nodes has h ≈ log₂ n. A tree built from sorted
input degenerates into a linked list — h = n, and every O(log n) claim
becomes O(n). Self-balancing trees (AVL, red-black) restore balance
after each change; a plain BST's contract must be honest: fast *when
insertion order cooperates*.

## Destroying a tree: post-order or bust

Free children before the parent — **post-order**. Pre-order frees a
parent and orphans its subtrees (leak); in-order frees a left child,
then the parent the right child is reached *through* (use-after-free).

```c
void bst_destroy(TNode *t) {
    if (!t) return;
    bst_destroy(t->left);     /* children first */
    bst_destroy(t->right);
    free(t);                  /* parent last */
}
```

Recursion depth is O(h) — fine for balanced trees, a stack-overflow
risk for degenerate ones. That risk is another reason height is the
fine print.
""",
"Cây tìm kiếm nhị phân",
    "Bất biến thứ tự làm việc tìm kiếm: insert, find, duyệt, và vì sao "
    "một phép xóa có thể tái cấu trúc tất cả.",
    r"""
## Bất biến chính là thuật toán

```c
typedef struct TNode {
    int           value;
    struct TNode *left, *right;   /* trái < giá trị < phải (không trùng) */
} TNode;
```

Cây con trái của mọi node giữ giá trị nhỏ hơn, phải giữ lớn hơn. Search
đi xuống một đường — O(h) với h là chiều cao:

```c
int bst_find(const TNode *t, int v) {
    while (t) {
        if (v == t->value) return 1;
        t = (v < t->value) ? t->left : t->right;
    }
    return 0;
}
```

Insert đi cùng đường và gắn vào chỗ trống. Cả ba phép duyệt là hai dòng
đệ quy; **in-order** (trái, mình, phải) thăm các giá trị theo *thứ tự
đã sắp* — tính chất mà cả một họ thuật toán dựa vào.

## Chiều cao là chữ in nhỏ

Cây cân bằng n node có h ≈ log₂ n. Cây dựng từ input đã sắp thoái hóa
thành linked list — h = n, và mọi tuyên bố O(log n) thành O(n). Cây tự
cân bằng (AVL, red-black) khôi phục cân bằng sau mỗi thay đổi; hợp đồng
của BST thuần phải trung thực: nhanh *khi thứ tự chèn hợp tác*.

## Hủy cây: post-order hoặc chết

Free con trước cha — **post-order**. Pre-order free cha và làm mồ côi
cây con (leak); in-order free con trái, rồi chính cha mà con phải được
chạm tới *qua đó* (use-after-free).

```c
void bst_destroy(TNode *t) {
    if (!t) return;
    bst_destroy(t->left);     /* con trước */
    bst_destroy(t->right);
    free(t);                  /* cha sau */
}
```

Độ sâu đệ quy là O(h) — ổn cho cây cân bằng, nguy cơ tràn stack cho cây
thoái hóa. Rủi ro đó là lý do khác khiến chiều cao là chữ in nhỏ.
"""
)

write_lesson(
    M, "bst-delete",
    "BST Deletion",
    "The three cases, the in-order successor trick, and why leaf deletion "
    "is the easy 90%.",
    17,
    r"""
## Three cases, one recursion

Deleting a value from a BST:

1. **Leaf** — no children: free it, set the parent's link to NULL.
2. **One child** — splice: the child takes the deleted node's place.
3. **Two children** — the hard case. You cannot just remove the node;
   two subtrees would hang loose. The trick: replace the node's value
   with its **in-order successor** (the smallest value in the right
   subtree), then delete *that* successor — which, by definition, has
   no left child, reducing the problem to case 1 or 2.

```c
TNode *bst_delete(TNode *t, int v) {
    if (!t) return NULL;
    if (v < t->value)      t->left  = bst_delete(t->left, v);
    else if (v > t->value) t->right = bst_delete(t->right, v);
    else {
        if (!t->left)  { TNode *r = t->right; free(t); return r; }
        if (!t->right) { TNode *l = t->left;  free(t); return l; }
        TNode *s = t->right;                   /* successor: leftmost of right */
        while (s->left) s = s->left;
        t->value = s->value;                   /* copy the value up */
        t->right = bst_delete(t->right, s->value);  /* delete the successor */
    }
    return t;
}
```

The `return`-based recursion reassigns the *parent's link* (`t->left =
bst_delete(...)`) — the same pointer-to-link idea from lists, in tree
form. The in-order traversal after any delete must still come out
sorted; that is the test.

## The double-deletion trap

Case 3 copies the successor's value then recurses to delete it. If the
recursion is written against the wrong subtree (or the value compare
uses `<=`), the same node can be visited for deletion twice — the first
frees it, the second reads freed memory. The successor search and the
deletion must agree on *which* node dies.
""",
"Xóa node BST",
    "Ba trường hợp, thủ thuật in-order successor, và vì sao xóa lá là "
    "90% dễ.",
    r"""
## Ba trường hợp, một đệ quy

Xóa một giá trị khỏi BST:

1. **Lá** — không con: free, gán link của cha thành NULL.
2. **Một con** — nối tắt: con chiếm chỗ của node bị xóa.
3. **Hai con** — trường hợp khó. Không thể gỡ node; hai cây con sẽ lơ
   lửng. Thủ thuật: thay giá trị của node bằng **in-order successor**
   (giá trị nhỏ nhất ở cây con phải), rồi xóa *successor đó* — theo định
   nghĩa, nó không có con trái, đưa về trường hợp 1 hoặc 2.

```c
TNode *bst_delete(TNode *t, int v) {
    if (!t) return NULL;
    if (v < t->value)      t->left  = bst_delete(t->left, v);
    else if (v > t->value) t->right = bst_delete(t->right, v);
    else {
        if (!t->left)  { TNode *r = t->right; free(t); return r; }
        if (!t->right) { TNode *l = t->left;  free(t); return l; }
        TNode *s = t->right;                   /* successor: trái nhất của phải */
        while (s->left) s = s->left;
        t->value = s->value;                   /* copy giá trị lên */
        t->right = bst_delete(t->right, s->value);  /* xóa successor */
    }
    return t;
}
```

Đệ quy kiểu `return` gán lại *link của cha* (`t->left =
bst_delete(...)`) — ý tưởng pointer-to-link của danh sách, trong dạng
cây. Duyệt in-order sau mọi phép xóa vẫn phải ra thứ tự đã sắp; đó là
test.

## Bẫy xóa hai lần

Trường hợp 3 copy giá trị successor rồi đệ quy xóa nó. Nếu đệ quy viết
vào sai cây con (hoặc phép so sánh dùng `<=`), cùng một node có thể
được ghé để xóa hai lần — lần đầu free nó, lần hai đọc bộ nhớ đã free.
Việc tìm successor và phép xóa phải đồng thuận về *node nào* chết.
"""
)

write_lesson(
    M, "binary-heaps",
    "Binary Heaps & Priority Queues",
    "A complete binary tree living in a plain array: parent/child index "
    "arithmetic, sift up/down, and O(1) peek.",
    17,
    r"""
## The tree that needs no pointers

A binary heap is a *complete* binary tree with the heap property
(parent ≤ children for min-heap). Completeness lets the tree live in an
array with pure index arithmetic:

```c
/* for the element at index i: */
size_t parent = (i - 1) / 2;
size_t left   = 2 * i + 1;
size_t right  = 2 * i + 2;
```

No pointers, no per-node malloc, and the array's memory locality is
excellent — this is why heapsort and priority queues are array-backed
in every real library.

## Sift up, sift down

**Insert** appends at the end (keeping completeness), then *sifts up*:
while smaller than its parent, swap with the parent. O(log n).

**Extract-min** removes the root (the minimum), moves the *last* element
into the root slot, shrinks, then *sifts down*: swap with the smaller
child while a child is smaller. O(log n). **Peek** is `a[0]` — O(1).

```c
void sift_down(long *a, size_t n, size_t i) {
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, smallest = i;
        if (l < n && a[l] < a[smallest]) smallest = l;
        if (r < n && a[r] < a[smallest]) smallest = r;
        if (smallest == i) return;
        long t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
```

## The index-arithmetic bugs, catalogued

- `parent = (i-1)/2` at i == 0 wraps to SIZE_MAX — guard the root.
- Forgetting `left < n` — a half-full last level reads phantom children.
- Sifting down comparing with only one child — the heap property breaks
  silently.

The invariant to test after every operation: every parent ≤ both
children. A `heap_ok` checker is five lines and catches all of them.
""",
"Binary Heap & Priority Queue",
    "Cây nhị phân đầy đủ sống trong mảng thường: phép tính chỉ số cha/con, "
    "sift up/down, và peek O(1).",
    r"""
## Cây không cần con trỏ

Binary heap là cây nhị phân *đầy đủ* với tính chất heap (cha ≤ con với
min-heap). Tính đầy đủ cho phép cây sống trong mảng với phép tính chỉ số
thuần túy:

```c
/* với phần tử tại chỉ số i: */
size_t parent = (i - 1) / 2;
size_t left   = 2 * i + 1;
size_t right  = 2 * i + 2;
```

Không con trỏ, không malloc từng node, locality bộ nhớ của mảng rất tốt —
vì sao heapsort và priority queue trong mọi thư viện thật đều dựa trên
mảng.

## Sift lên, sift xuống

**Insert** nối vào cuối (giữ tính đầy đủ), rồi *sift up*: khi nhỏ hơn
cha, đổi chỗ với cha. O(log n).

**Extract-min** bỏ gốc (phần tử nhỏ nhất), đưa *phần tử cuối* vào chỗ
gốc, thu ngắn, rồi *sift down*: đổi chỗ với con nhỏ hơn khi con còn nhỏ
hơn. O(log n). **Peek** là `a[0]` — O(1).

```c
void sift_down(long *a, size_t n, size_t i) {
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, smallest = i;
        if (l < n && a[l] < a[smallest]) smallest = l;
        if (r < n && a[r] < a[smallest]) smallest = r;
        if (smallest == i) return;
        long t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
```

## Các bug số học chỉ số, phân loại

- `parent = (i-1)/2` tại i == 0 wrap thành SIZE_MAX — chặn gốc.
- Quên `left < n` — tầng cuối lưng lửng đọc con ma.
- Sift down chỉ so với một con — tính chất heap gãy âm thầm.

Bất biến cần test sau mọi thao tác: mọi cha ≤ cả hai con. Một hàm kiểm
`heap_ok` năm dòng bắt được tất cả.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p11-bst",
    "BST Gym",
    "Insert, search, height, in-order arrays, and the deletion cases.",
    "Phòng gym BST",
    "Insert, search, chiều cao, mảng in-order, và các trường hợp xóa.",
    after_lesson="bst-delete",
    minutes=28,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p11-bst-core",
            "The Search Tree",
            """Implement the BST core. The boilerplate declares:

```c
typedef struct TNode { int value; struct TNode *left, *right; } TNode;
int bst_insert(TNode **root, int v);        /* 0 inserted, 1 duplicate, -1 oom */
int bst_find(const TNode *root, int v);     /* 1 found, 0 absent */
size_t bst_height(const TNode *root);       /* empty tree = 0 */
long bst_min(const TNode *root);            /* LLONG_MIN if empty */
/* fills out with the in-order traversal, returns the count
   (out must have room for the node count) */
size_t bst_inorder(const TNode *root, int *out);
void bst_destroy(TNode *root);
```""",
            C_PRELUDE + "\n#include <stddef.h>\n#include <limits.h>\ntypedef struct TNode { int value; struct TNode *left, *right; } TNode;\nint bst_insert(TNode **root, int v);\nint bst_find(const TNode *root, int v);\nsize_t bst_height(const TNode *root);\nlong bst_min(const TNode *root);\nsize_t bst_inorder(const TNode *root, int *out);\nvoid bst_destroy(TNode *root);\n",
            [
                (
                    "insert, find, order",
                    r"""
TNode *t = NULL;
CHECK_EQ(bst_height(t), 0);
CHECK_EQ(bst_find(t, 5), 0);
CHECK_EQ(bst_insert(&t, 5), 0);
CHECK_EQ(bst_insert(&t, 3), 0);
CHECK_EQ(bst_insert(&t, 8), 0);
CHECK_EQ(bst_insert(&t, 1), 0);
CHECK_EQ(bst_insert(&t, 5), 1);            /* duplicate rejected */
CHECK_EQ(bst_find(t, 8), 1);
CHECK_EQ(bst_find(t, 2), 0);
CHECK_EQ(bst_min(t), 1);
CHECK_EQ(bst_height(t), 3);                /* 5-(3-(1)),8: chain left-left */
int buf[8];
CHECK_EQ(bst_inorder(t, buf), 4);
CHECK(buf[0] == 1 && buf[1] == 3 && buf[2] == 5 && buf[3] == 8);
bst_destroy(t);
""",
                    "Insert returns 1 when the value already exists (walk stops at equal). Height counts nodes on the longest path.",
                ),
                (
                    "degenerate vs balanced",
                    r"""
TNode *t = NULL;
for (int i = 1; i <= 6; i++) CHECK_EQ(bst_insert(&t, i), 0);  /* sorted input! */
CHECK_EQ(bst_height(t), 6);                /* degenerated: a linked list */
int buf[8];
CHECK_EQ(bst_inorder(t, buf), 6);          /* still sorted: 1..6 */
for (int i = 0; i < 6; i++) CHECK_EQ(buf[i], i + 1);
bst_destroy(t);
/* zig-zag build: 4,2,6,1,3,5,7 */
TNode *z = NULL;
int vals[] = {4, 2, 6, 1, 3, 5, 7};
for (int i = 0; i < 7; i++) CHECK_EQ(bst_insert(&z, vals[i]), 0);
CHECK_EQ(bst_height(z), 3);
CHECK_EQ(bst_min(z), 1);
bst_destroy(z);
""",
                    "Sorted input is the documented worst case. The zig-zag build is the balanced best case.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p11-bst-core": vi_challenge(
            "Cây tìm kiếm",
            "Cài bst_insert/find/height/min/inorder/destroy; trùng -> 1; in-order ra mảng sắp.",
            [("insert, find, thứ tự", "insert trả 1 khi đã có; height đếm node trên đường dài nhất.")],
        ),
    },
    solutions=[
        (
            "cint-p11-bst-core",
            r"""
#include <stdlib.h>
#include <stddef.h>
int bst_insert(TNode **root, int v) {
    if (!root) return -1;
    TNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    n->left = n->right = NULL;
    TNode **link = root;
    while (*link) {
        if (v == (*link)->value) { free(n); return 1; }
        link = (v < (*link)->value) ? &(*link)->left : &(*link)->right;
    }
    *link = n;
    return 0;
}
int bst_find(const TNode *t, int v) {
    while (t) {
        if (v == t->value) return 1;
        t = (v < t->value) ? t->left : t->right;
    }
    return 0;
}
size_t bst_height(const TNode *t) {
    if (!t) return 0;
    size_t l = bst_height(t->left), r = bst_height(t->right);
    return 1 + (l > r ? l : r);
}
long bst_min(const TNode *t) {
    if (!t) return LONG_MIN;
    while (t->left) t = t->left;
    return t->value;
}
static size_t inorder_rec(const TNode *t, int *out, size_t n) {
    if (!t) return n;
    n = inorder_rec(t->left, out, n);
    out[n++] = t->value;
    return inorder_rec(t->right, out, n);
}
size_t bst_inorder(const TNode *root, int *out) {
    if (!root || !out) return 0;
    return inorder_rec(root, out, 0);
}
void bst_destroy(TNode *t) {
    if (!t) return;
    bst_destroy(t->left);
    bst_destroy(t->right);
    free(t);
}""",
            r"""
#include <stdlib.h>
#include <stddef.h>
int bst_insert(TNode **root, int v) {
    if (!root) return -1;
    TNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    n->left = n->right = NULL;
    TNode *cur = *root;
    while (cur) {
        if (v == cur->value) { free(n); return 1; }
        cur = (v < cur->value) ? cur->left : cur->right;
    }
    cur = n;                    /* wrong: assigns the LOCAL — nothing is attached */
    return 0;
}
int bst_find(const TNode *t, int v) {
    while (t) {
        if (v == t->value) return 1;
        t = (v < t->value) ? t->left : t->right;
    }
    return 0;
}
size_t bst_height(const TNode *t) {
    if (!t) return 0;
    size_t l = bst_height(t->left), r = bst_height(t->right);
    return 1 + (l > r ? l : r);
}
long bst_min(const TNode *t) {
    if (!t) return LONG_MIN;
    while (t->right) t = t->right;   /* wrong: walks to the MAX */
    return t->value;
}
static size_t inorder_rec(const TNode *t, int *out, size_t n) {
    if (!t) return n;
    n = inorder_rec(t->left, out, n);
    out[n++] = t->value;
    return inorder_rec(t->right, out, n);
}
size_t bst_inorder(const TNode *root, int *out) {
    if (!root || !out) return 0;
    return inorder_rec(root, out, 0);
}
void bst_destroy(TNode *t) {
    if (!t) return;
    free(t);                    /* wrong: frees the parent first — children leak */
    bst_destroy(t->left);
    bst_destroy(t->right);
}""",
        ),
    ],
)

write_practice(
    M, "cint-p11-heap",
    "Heap Gym",
    "Array-backed min-heap: sift up/down, heapify, and heapsort.",
    "Phòng gym Heap",
    "Min-heap trên mảng: sift up/down, heapify, và heapsort.",
    after_lesson="binary-heaps",
    minutes=28,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p11-minheap",
            "The Array Heap",
            """Implement a fixed-capacity min-heap. The boilerplate declares:

```c
#define HCAP 64
typedef struct { long a[HCAP]; size_t n; } Heap;
void heap_init(Heap *h);
int  heap_push(Heap *h, long v);      /* 0 ok, -1 full/NULL */
int  heap_pop(Heap *h, long *out);    /* 0 ok, -1 empty/NULL */
int  heap_peek(const Heap *h, long *out);  /* 0 ok, -1 empty */
size_t heap_size(const Heap *h);
/* 1 if the heap property holds for every parent/child pair */
int  heap_ok(const Heap *h);
```

Min-heap: the smallest element is at index 0.""",
            C_PRELUDE + "\n#include <stddef.h>\n#define HCAP 64\ntypedef struct { long a[HCAP]; size_t n; } Heap;\nvoid heap_init(Heap *h);\nint  heap_push(Heap *h, long v);\nint  heap_pop(Heap *h, long *out);\nint  heap_peek(const Heap *h, long *out);\nsize_t heap_size(const Heap *h);\nint  heap_ok(const Heap *h);\n",
            [
                (
                    "push, pop, invariant",
                    r"""
Heap h;
heap_init(&h);
long v;
CHECK_EQ(heap_peek(&h, &v), -1);
CHECK_EQ(heap_pop(&h, &v), -1);
long vals[] = {7, 3, 9, 1, 5};
for (int i = 0; i < 5; i++) CHECK_EQ(heap_push(&h, vals[i]), 0);
CHECK_EQ(heap_size(&h), 5);
CHECK_EQ(heap_ok(&h), 1);
CHECK_EQ(heap_peek(&h, &v), 0); CHECK_EQ(v, 1);   /* min at root */
CHECK_EQ(heap_pop(&h, &v), 0); CHECK_EQ(v, 1);
CHECK_EQ(heap_pop(&h, &v), 0); CHECK_EQ(v, 3);
CHECK_EQ(heap_ok(&h), 1);                          /* still valid after pops */
CHECK_EQ(heap_push(&h, 0), 0);                     /* new global min */
CHECK_EQ(heap_peek(&h, &v), 0); CHECK_EQ(v, 0);
CHECK_EQ(heap_ok(&h), 1);
""",
                    "Push: place at a[n], sift up while < parent (guard i > 0). Pop: root out, last to root, sift down to the smaller child.",
                ),
            ],
        ),
        challenge(
            "cint-p11-heapsort",
            "Heapify & Heapsort",
            """Two classic builds on the heap idea:

```c
/* transforms a[0..n) into a min-heap in place — O(n) bottom-up heapify */
void heapify(long *a, size_t n);
/* sorts a[0..n) ASCENDING using a MAX-heap built in place:
   heapify as max-heap, repeatedly swap root with end and shrink.
   (Classic heapsort: max-heap gives ascending order in place.) */
void heapsort_asc(long *a, size_t n);
```

No extra arrays: both are in-place.""",
            C_PRELUDE + "\n#include <stddef.h>\nvoid heapify(long *a, size_t n);\nvoid heapsort_asc(long *a, size_t n);\n",
            [
                (
                    "bottom-up heapify, in-place sort",
                    r"""
long a[] = {9, 4, 7, 1, 8, 2};
heapify(a, 6);
/* min-heap property: parent <= children */
CHECK(a[0] == 1);                        /* min at root */
for (size_t i = 1; i < 6; i++) {
    size_t p = (i - 1) / 2;
    CHECK(a[p] <= a[i]);
}
long b[] = {5, 3, 8, 1, 9, 2, 7};
heapsort_asc(b, 7);
for (int i = 0; i < 6; i++) CHECK(b[i] <= b[i + 1]);
CHECK(b[0] == 1 && b[6] == 9);
long one[] = {42};
heapify(one, 1);
CHECK(one[0] == 42);
heapsort_asc(one, 1);
CHECK(one[0] == 42);
""",
                    "Heapify: sift_down from i = n/2 backwards to 0. Heapsort: build a MAX-heap, swap a[0] with a[end], shrink, sift down.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p11-minheap": vi_challenge(
            "Heap trên mảng",
            "Cài Heap: push/pop/peek/size/heap_ok cho min-heap cố định 64 phần tử.",
            [("push, pop, bất biến", "push: đặt a[n], sift lên khi < cha (chặn i > 0).")],
        ),
        "cint-p11-heapsort": vi_challenge(
            "Heapify & heapsort",
            "Cài heapify (sift down từ n/2 về 0) và heapsort_asc (max-heap in-place).",
            [("heapify bottom-up, sort in-place", "max-heap: đổi a[0] với a[end], thu ngắn, sift xuống.")],
        ),
    },
    solutions=[
        (
            "cint-p11-minheap",
            r"""
#include <stddef.h>
void heap_init(Heap *h) { if (h) h->n = 0; }
int heap_push(Heap *h, long v) {
    if (!h || h->n == HCAP) return -1;
    size_t i = h->n++;
    h->a[i] = v;
    while (i > 0) {
        size_t p = (i - 1) / 2;
        if (h->a[p] <= h->a[i]) break;
        long t = h->a[p]; h->a[p] = h->a[i]; h->a[i] = t;
        i = p;
    }
    return 0;
}
int heap_pop(Heap *h, long *out) {
    if (!h || !out || h->n == 0) return -1;
    *out = h->a[0];
    h->a[0] = h->a[--h->n];
    size_t i = 0;
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, smallest = i;
        if (l < h->n && h->a[l] < h->a[smallest]) smallest = l;
        if (r < h->n && h->a[r] < h->a[smallest]) smallest = r;
        if (smallest == i) break;
        long t = h->a[i]; h->a[i] = h->a[smallest]; h->a[smallest] = t;
        i = smallest;
    }
    return 0;
}
int heap_peek(const Heap *h, long *out) {
    if (!h || !out || h->n == 0) return -1;
    *out = h->a[0];
    return 0;
}
size_t heap_size(const Heap *h) { return h ? h->n : 0; }
int heap_ok(const Heap *h) {
    if (!h) return 0;
    for (size_t i = 1; i < h->n; i++)
        if (h->a[(i - 1) / 2] > h->a[i]) return 0;
    return 1;
}""",
            r"""
#include <stddef.h>
void heap_init(Heap *h) { if (h) h->n = 0; }
int heap_push(Heap *h, long v) {
    if (!h || h->n == HCAP) return -1;
    size_t i = h->n++;
    h->a[i] = v;
    while (i > 0) {
        size_t p = (i - 1) / 2;
        if (h->a[p] <= h->a[i]) break;
        long t = h->a[p]; h->a[p] = h->a[i]; h->a[i] = t;
        i = p;
    }
    return 0;
}
int heap_pop(Heap *h, long *out) {
    if (!h || !out || h->n == 0) return -1;
    *out = h->a[0];
    h->a[0] = h->a[h->n - 1];
    h->n--;                    /* fine so far */
    size_t i = 0;
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, smallest = i;
        if (l < h->n && h->a[l] < h->a[smallest]) smallest = l;
        if (r < h->n && h->a[r] < h->a[smallest]) smallest = r;
        if (smallest == i) break;
        long t = h->a[i]; h->a[i] = h->a[smallest]; h->a[smallest] = t;
        i = l;                 /* wrong: descends LEFT regardless — with
                                       r the smaller child the heap property
                                       breaks and pop can return non-min */
    }
    return 0;
}
int heap_peek(const Heap *h, long *out) {
    if (!h || !out || h->n == 0) return -1;
    *out = h->a[0];
    return 0;
}
size_t heap_size(const Heap *h) { return h ? h->n : 0; }
int heap_ok(const Heap *h) {
    if (!h) return 0;
    for (size_t i = 1; i < h->n; i++)
        if (h->a[(i - 1) / 2] > h->a[i]) return 0;
    return 1;
}""",
        ),
        (
            "cint-p11-heapsort",
            r"""
#include <stddef.h>
static void sift_down_min(long *a, size_t n, size_t i) {
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, smallest = i;
        if (l < n && a[l] < a[smallest]) smallest = l;
        if (r < n && a[r] < a[smallest]) smallest = r;
        if (smallest == i) return;
        long t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
static void sift_down_max(long *a, size_t n, size_t i) {
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, largest = i;
        if (l < n && a[l] > a[largest]) largest = l;
        if (r < n && a[r] > a[largest]) largest = r;
        if (largest == i) return;
        long t = a[i]; a[i] = a[largest]; a[largest] = t;
        i = largest;
    }
}
void heapify(long *a, size_t n) {
    if (!a || n < 2) return;
    for (size_t i = n / 2; i-- > 0;)
        sift_down_min(a, n, i);
}
void heapsort_asc(long *a, size_t n) {
    if (!a || n < 2) return;
    for (size_t i = n / 2; i-- > 0;)
        sift_down_max(a, n, i);
    for (size_t end = n - 1; end > 0; end--) {
        long t = a[0]; a[0] = a[end]; a[end] = t;
        sift_down_max(a, end, 0);
    }
}""",
            r"""
#include <stddef.h>
static void sift_down_min(long *a, size_t n, size_t i) {
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, smallest = i;
        if (l < n && a[l] < a[smallest]) smallest = l;
        if (r < n && a[r] < a[smallest]) smallest = r;
        if (smallest == i) return;
        long t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
void heapify(long *a, size_t n) {
    if (!a || n < 2) return;
    for (size_t i = 0; i < n; i++)          /* wrong: sift-down top-down from
                                                  every index is not the O(n)
                                                  build and — worse — descending
                                                  order breaks the invariant it
                                                  is meant to restore */
        sift_down_min(a, n, i);
}
void heapsort_asc(long *a, size_t n) {
    if (!a || n < 2) return;
    heapify(a, n);                          /* wrong: builds a MIN-heap */
    for (size_t end = n - 1; end > 0; end--) {
        long t = a[0]; a[0] = a[end]; a[end] = t;
        sift_down_min(a, end, 0);           /* wrong: min-heap swaps move the
                                                  SMALLEST to the end — output
                                                  is descending */
    }
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m11-task",
    "Top-K with a Bounded Heap",
    """The streaming-top-K problem: keep the K largest values seen, using
a MIN-heap of size K. The boilerplate declares:

```c
#define K 5
typedef struct { long a[K]; size_t n; } TopK;
void tk_init(TopK *t);
/* offer one value; the heap keeps the K largest seen so far.
   0 ok, -1 NULL. Always O(log K). */
int tk_offer(TopK *t, long v);
/* fills out (size K) with the current K largest in DESCENDING order
   (out[0] = largest). Returns the count filled (== t->n, may be < K). */
size_t tk_report(const TopK *t, long *out);
size_t tk_size(const TopK *t);
```""",
    C_PRELUDE + "\n#include <stddef.h>\n#define K 5\ntypedef struct { long a[K]; size_t n; } TopK;\nvoid tk_init(TopK *t);\nint tk_offer(TopK *t, long v);\nsize_t tk_report(const TopK *t, long *out);\nsize_t tk_size(const TopK *t);\n",
    [
        (
            "stream, evict, report",
            r"""
TopK t;
tk_init(&t);
long out[K];
CHECK_EQ(tk_size(&t), 0);
CHECK_EQ(tk_report(&t, out), 0);
long stream[] = {4, 9, 1, 42, 7, 100, 3, 42};
for (int i = 0; i < 8; i++) CHECK_EQ(tk_offer(&t, stream[i]), 0);
CHECK_EQ(tk_size(&t), 5);                 /* capped at K */
CHECK_EQ(tk_report(&t, out), 5);
/* top-5 of {4,9,1,42,7,100,3,42} = 100,42,42,9,7 (both 42s fit) */
CHECK(out[0] == 100);
CHECK(out[1] == 42);
CHECK(out[2] == 42);
CHECK(out[3] == 9);
CHECK(out[4] == 7);
/* 1, 3, 4 can never be in the top-5 of this stream */
int saw_small = 0;
for (int i = 0; i < 5; i++) if (out[i] <= 4) saw_small = 1;
CHECK_EQ(saw_small, 0);
""",
            "Offer: heap not full -> push + sift up. Full and v > min -> replace the min, sift down. Otherwise discard.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Top-K với heap có giới hạn",
        "Cài TopK: min-heap kích thước K giữ K giá trị lớn nhất; report giảm dần.",
        [("stream, evict, report", "đầy và v > min thì thay min, sift xuống; nhỏ hơn thì bỏ.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m11",
    "Checkpoint: Streaming Top-K",
    "Prove the heap discipline: keep the K largest of a stream in O(log K) per element.",
    28,
    r"""
## The task

Implement `TopK` (see the challenge). The bounded min-heap is the
canonical streaming algorithm: the heap holds candidates, its root is
the weakest survivor, and each new value either evicts the root or is
discarded in O(1). Report must sort K ≤ 5 elements — trivial — but the
*heap* must never exceed K and must always contain the true top-K.

Passing this proves you can turn the module's index arithmetic into a
real online algorithm — the pattern behind leaderboards, percentile
trackers, and dedup-by-similarity in production.

Next module: files as bytes — binary formats and robust parsing.
""",
    "Kiểm tra: Top-K streaming",
    "Chứng minh kỷ luật heap: giữ K giá trị lớn nhất của stream với O(log K) mỗi phần tử.",
    r"""
## Bài toán

Cài `TopK` (xem challenge). Min-heap có giới hạn là thuật toán streaming
kinh điển: heap giữ các ứng viên, gốc là kẻ yếu nhất còn sống, và mỗi
giá trị mới hoặc đuổi gốc hoặc bị bỏ trong O(1). Report chỉ cần sort
K ≤ 5 phần tử — dễ — nhưng *heap* không bao giờ vượt K và luôn chứa
top-K thật.

Vượt qua chứng minh bạn biến phép tính chỉ số của module thành thuật
toán online thật — mẫu đứng sau leaderboard, bộ theo dõi percentile, và
dedup-theo-độ-tương-tự trong production.

Module sau: file như byte — định dạng nhị phân và parsing bền vững.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <stddef.h>
void tk_init(TopK *t) { if (t) t->n = 0; }
static void sift_up(long *a, size_t i) {
    while (i > 0) {
        size_t p = (i - 1) / 2;
        if (a[p] <= a[i]) break;
        long t = a[p]; a[p] = a[i]; a[i] = t;
        i = p;
    }
}
static void sift_down(long *a, size_t n, size_t i) {
    while (1) {
        size_t l = 2*i + 1, r = 2*i + 2, smallest = i;
        if (l < n && a[l] < a[smallest]) smallest = l;
        if (r < n && a[r] < a[smallest]) smallest = r;
        if (smallest == i) return;
        long t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
int tk_offer(TopK *t, long v) {
    if (!t) return -1;
    if (t->n < K) {
        t->a[t->n++] = v;
        sift_up(t->a, t->n - 1);
        return 0;
    }
    if (v > t->a[0]) {                 /* beats the weakest survivor */
        t->a[0] = v;
        sift_down(t->a, t->n, 0);
    }
    return 0;                          /* else: discarded in O(1) */
}
size_t tk_size(const TopK *t) { return t ? t->n : 0; }
size_t tk_report(const TopK *t, long *out) {
    if (!t || !out) return 0;
    for (size_t i = 0; i < t->n; i++) out[i] = t->a[i];
    /* insertion sort descending — K <= 5 */
    for (size_t i = 1; i < t->n; i++) {
        long key = out[i];
        size_t j = i;
        while (j > 0 && out[j - 1] < key) {
            out[j] = out[j - 1];
            j--;
        }
        out[j] = key;
    }
    return t->n;
}""",
    wrong=r"""
#include <stddef.h>
void tk_init(TopK *t) { if (t) t->n = 0; }
int tk_offer(TopK *t, long v) {
    if (!t) return -1;
    if (t->n == K) return 0;           /* wrong: full -> always discard, even
                                             when v beats the current minimum:
                                             the true top-K is never tracked */
    t->a[t->n++] = v;                  /* wrong: appended without sift-up —
                                             the min-heap property is not kept */
    return 0;
}
size_t tk_size(const TopK *t) { return t ? t->n : 0; }
size_t tk_report(const TopK *t, long *out) {
    if (!t || !out) return 0;
    for (size_t i = 0; i < t->n; i++) out[i] = t->a[i];
    for (size_t i = 1; i < t->n; i++) {          /* ascending, not descending */
        long key = out[i];
        size_t j = i;
        while (j > 0 && out[j - 1] > key) {
            out[j] = out[j - 1];
            j--;
        }
        out[j] = key;
    }
    return t->n;
}""",
)

print("module 11 complete")
