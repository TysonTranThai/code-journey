#!/usr/bin/env python3
"""C — Intermediate — Module 7: cint-linked.

Singly and doubly linked lists built from scratch: ownership discipline,
edge-first insertion, O(1) tail with a tail pointer, safe unlinking in
doubly-linked form. Every operation handles the empty/single/head cases.
House conventions: ISO C only, self-contained tests, Ws are behavioral
near-misses (leaks are unobservable here — Ws corrupt behavior).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-linked"

write_module(
    M,
    "Linked Data Structures",
    "Lists you build from raw nodes: the empty-list is the hard case, the "
    "head is a moving target, and every node is freed exactly once.",
    "Cấu trúc dữ liệu liên kết",
    "Danh sách dựng từ node thô: rỗng là trường hợp khó, đầu danh sách là "
    "mục tiêu di động, và mỗi node được free đúng một lần.",
    lessons=["singly-lists", "doubly-lists", "stacks-queues", "cint-checkpoint-m7"],
    practices=["cint-p7-slist", "cint-p7-dlist"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "singly-lists",
    "Singly Linked Lists",
    "The node, the empty-list discipline, head insertion, and why the tail "
    "costs you O(n) until you buy one.",
    17,
    r"""
## The node is the whole idea

```c
typedef struct SNode {
    int            value;
    struct SNode  *next;    /* NULL ends the list */
} SNode;
```

The list *is* the head pointer. An empty list is `SNode *head = NULL;` —
there is no list object to initialize. Every function that mutates the
list must handle three special cases: **empty** (head is NULL), **single
element**, and **the head itself** (which changes).

Head insertion is the cheap one — O(1), no traversal, and it naturally
reverses insertion order:

```c
int push_front(SNode **head, int v) {
    SNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    n->next = *head;      /* works for empty: *head is NULL */
    *head = n;
    return 0;
}
```

The `SNode **head` is not decoration. The function must *change the
caller's head* — and to change a pointer you need its address. The
alternative (returning the new head) works but forces the caller to
reassign on every call, which is one forgotten `head = ...` away from a
leak.

## Deletion is where lists punish you

To delete a node you need the *previous* node — but singly-linked nodes
point only forward. Either walk with two fingers (`prev`/`cur`), or copy
the next node's payload into the doomed node and unlink it (great for
tail-agnostic O(1) delete, changes iteration semantics). The two-finger
walk is the honest default:

```c
int remove_val(SNode **head, int v) {
    SNode **link = head;              /* points at whoever points at cur */
    for (SNode *cur = *head; cur; cur = cur->next) {
        if (cur->value == v) {
            *link = cur->next;        /* unlink: fixes head OR prev->next */
            free(cur);
            return 1;
        }
        link = &cur->next;
    }
    return 0;
}
```

`SNode **link` walks the *links*, not the nodes: `*link` is "whatever
points at cur" — the head itself, or the previous node's `next`. One
code path for both, no special cases.

## Destroying a list

Free every node exactly once, then null the head. The trap is
`free(cur); cur = cur->next;` — reading a freed node. Save the next
pointer first, always.
""",
"Danh sách liên kết đơn",
    "Node, kỷ luật danh sách rỗng, chèn đầu, và vì sao đuôi tốn O(n) cho "
    "đến khi bạn mua một con trỏ tail.",
    r"""
## Node là toàn bộ ý tưởng

```c
typedef struct SNode {
    int            value;
    struct SNode  *next;    /* NULL kết thúc danh sách */
} SNode;
```

Danh sách *là* con trỏ head. Danh sách rỗng là `SNode *head = NULL;` —
không có object list nào để khởi tạo. Mỗi hàm biến đổi phải xử lý ba
trường hợp đặc biệt: **rỗng**, **một phần tử**, và **chính head** (thay đổi).

Chèn đầu là rẻ nhất — O(1), không đi bộ, và tự nhiên đảo ngược thứ tự:

```c
int push_front(SNode **head, int v) {
    SNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    n->next = *head;      /* rỗng cũng đúng: *head là NULL */
    *head = n;
    return 0;
}
```

`SNode **head` không phải trang trí. Hàm phải *thay đổi head của caller*
— và để đổi một con trỏ bạn cần địa chỉ của nó. Cách thay thế (trả về
head mới) được nhưng buộc caller gán lại mỗi lần — cách một `head = ...`
quên là một leak.

## Xóa là nơi danh sách trừng phạt bạn

Để xóa một node bạn cần node *trước* nó — nhưng node singly-linked chỉ
chỉ về phía trước. Hoặc đi bằng hai ngón tay (`prev`/`cur`), hoặc copy
payload của node kế vào node sắp chết rồi unlinh (O(1) không cần tail,
nhưng đổi ngữ nghĩa duyệt). Đi hai ngón là mặc định trung thực:

```c
int remove_val(SNode **head, int v) {
    SNode **link = head;              /* trỏ vào "kẻ trỏ vào cur" */
    for (SNode *cur = *head; cur; cur = cur->next) {
        if (cur->value == v) {
            *link = cur->next;        /* gỡ: sửa head HOẶC prev->next */
            free(cur);
            return 1;
        }
        link = &cur->next;
    }
    return 0;
}
```

`SNode **link` đi qua các *link*, không phải node: `*link` là "bất cứ cái
gì đang trỏ vào cur" — head, hoặc `next` của node trước. Một đường code
cho cả hai, không trường hợp đặc biệt.

## Hủy danh sách

Free từng node đúng một lần rồi null head. Bẫy kinh điển:
`free(cur); cur = cur->next;` — đọc node đã free. Lưu next trước, luôn luôn.
"""
)

write_lesson(
    M, "doubly-lists",
    "Doubly Linked Lists",
    "prev pointers make deletion O(1) — and give you two more pointers to "
    "keep consistent.",
    16,
    r"""
## Pay two pointers, delete in O(1)

```c
typedef struct DNode {
    int            value;
    struct DNode  *prev, *next;
} DNode;
```

With `prev`, a node carries its own "who points at me" — unlinking needs
no search:

```c
void unlink(DNode *n) {
    if (n->prev) n->prev->next = n->next; else /* was head */;
    if (n->next) n->next->prev = n->prev; else /* was tail */;
    n->prev = n->next = NULL;      /* node is now detached */
}
```

The price is **four pointer updates per insert/delete instead of two**,
and a whole class of new bugs: forgetting one side leaves a node that
thinks it is detached while the list still reaches it — or worse, a
*prev* chain that disagrees with the *next* chain. After any structural
change, a forward walk and a backward walk must visit the same nodes in
reverse order. Tests should verify both directions.

## Sentinels: trading one node for zero special cases

Keep a dummy node that is never stored-to; the real list runs between
its two links. Head and tail operations stop having NULL cases:

```c
DNode sentinel;                     /* never holds data */
sentinel.next = &sentinel;
sentinel.prev = &sentinel;          /* empty list: both point home */
```

Insertion becomes one statement regardless of position; iteration is
`for (DNode *p = s.next; p != &s; p = p->next)`. The cost: one extra node
and the discipline that *nothing* may dereference the sentinel's value.
Production list implementations (Linux `list_head` among them) are
sentinel-based.
""",
"Danh sách liên kết kép",
    "Con trỏ prev giúp xóa O(1) — và cho bạn thêm hai con trỏ phải giữ "
    "nhất quán.",
    r"""
## Trả hai con trỏ, xóa O(1)

```c
typedef struct DNode {
    int            value;
    struct DNode  *prev, *next;
} DNode;
```

Có `prev`, node tự mang "ai trỏ vào mình" — gỡ không cần tìm:

```c
void unlink(DNode *n) {
    if (n->prev) n->prev->next = n->next; else /* là head */;
    if (n->next) n->next->prev = n->prev; else /* là tail */;
    n->prev = n->next = NULL;      /* node đã tách rời */
}
```

Giá: **bốn lần cập nhật con trỏ mỗi thao tác thay vì hai**, và cả một
họ bug mới: quên một bên để lại node tưởng đã tách rời trong khi danh
sách vẫn với tới nó — hoặc tệ hơn, chuỗi *prev* bất đồng với chuỗi
*next*. Sau mọi thay đổi cấu trúc, đi xuôi và đi ngược phải gặp cùng các
node theo thứ tự ngược. Test nên kiểm cả hai hướng.

## Sentinel: lấy một node đổi không trường hợp đặc biệt

Giữ một node giả không bao giờ chứa dữ liệu; danh sách thật chạy giữa
hai link của nó. Thao tác đầu/đuôi hết có trường hợp NULL:

```c
DNode sentinel;
sentinel.next = &sentinel;
sentinel.prev = &sentinel;          /* rỗng: cả hai trỏ về nhà */
```

Chèn thành một câu lệnh bất kể vị trí; duyệt là
`for (DNode *p = s.next; p != &s; p = p->next)`. Giá: một node thừa và
kỷ luật *không bao giờ* dereference giá trị của sentinel. Các cài đặt
list thật (Linux `list_head` trong số đó) đều dựa trên sentinel.
"""
)

write_lesson(
    M, "stacks-queues",
    "Stacks, Queues & Deques",
    "The constrained interfaces that make linked structures useful: LIFO, "
    "FIFO, and both-ends.",
    14,
    r"""
## Constraints are the feature

A stack is a list you may only touch at one end. A queue is a list you
may only append at one end and remove from the other. The constraint is
what makes reasoning possible — and the implementation is where the
costs live:

- **Stack**: head-insert, head-remove. O(1) with a singly-linked list.
  Nothing else needed.
- **Queue**: append at tail, remove at head. With a singly-linked list
  that means keeping a *tail pointer too* — and the discipline that
  every append updates it (`tail->next = n; tail = n;` and when the
  queue was empty, `head = tail = n`).
- **Deque**: both ends. A singly-linked list cannot remove from the
  tail in O(1) — you need a doubly-linked list (or sentinel ring).

## The empty/one-element boundary, again

Every queue bug in the wild is one of: append to empty queue forgetting
to set head; pop to empty forgetting to clear tail; or popping the last
element leaving a stale tail. Write the two-element invariant in a
comment — `head == NULL  <=>  tail == NULL` — and test the boundary:
push one, pop one, push again.

## Ownership stays the same

The container owns its nodes; values are copied in and out by value
(or borrowed pointers with documented loans). `destroy` walks and frees
exactly once — the same discipline as any list, now wrapped in the
constrained API.
""",
"Stack, Queue & Deque",
    "Các interface ràng buộc khiến linked structure hữu dụng: LIFO, FIFO, "
    "và hai đầu.",
    r"""
## Ràng buộc chính là tính năng

Stack là danh sách chỉ đụng được một đầu. Queue là danh sách thêm một
đầu, bỏ đầu kia. Ràng buộc khiến việc suy luận khả thi — và phần cài đặt
là nơi chi phí sống:

- **Stack**: chèn đầu, bỏ đầu. O(1) với singly-linked. Không cần gì thêm.
- **Queue**: thêm đuôi, bỏ đầu. Cần *thêm con trỏ tail* — và kỷ luật
  cập nhật nó trong mọi thao tác (queue rỗng: `head = tail = n`).
- **Deque**: hai đầu. Singly không bỏ được đuôi O(1) — cần doubly
  (hoặc ring với sentinel).

## Biên rỗng/một-phần-tử, lần nữa

Mọi bug queue ngoài kia là một trong: thêm vào queue rỗng quên set head;
pop về rỗng quên clear tail; pop phần tử cuối để lại tail cũ. Ghi
bất biến hai chiều vào comment — `head == NULL  <=>  tail == NULL` — và
test biên: push một, pop một, push lại.

## Ownership không đổi

Container sở hữu node; giá trị copy in/out (hoặc con trỏ mượn có ghi rõ
khoản mượn). `destroy` đi và free đúng một lần — cùng kỷ luật với mọi
list, giờ bọc trong API ràng buộc.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p7-slist",
    "Singly List Gym",
    "Build the core singly-linked list with pointer-to-link surgery.",
    "Phòng gym singly list",
    "Dựng lõi singly-linked list với phẫu thuật pointer-to-link.",
    after_lesson="singly-lists",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p7-slist-core",
            "List Surgery",
            """Implement the singly list core. The boilerplate declares:

```c
typedef struct SNode { int value; struct SNode *next; } SNode;
/* all take/return the caller's head pointer by address */
int  s_push(SNode **head, int v);              /* 0 ok, -1 oom */
int  s_pop(SNode **head, int *out);            /* 0 ok, -1 empty */
int  s_remove(SNode **head, int v);            /* 1 removed, 0 absent */
size_t s_len(const SNode *head);
int  s_sum(const SNode *head);
void s_clear(SNode **head);                    /* frees all, head becomes NULL */
/* insert keeping ascending order; 0 ok, -1 oom */
int  s_insert_sorted(SNode **head, int v);
```""",
            C_PRELUDE + "\n#include <stddef.h>\ntypedef struct SNode { int value; struct SNode *next; } SNode;\nint  s_push(SNode **head, int v);\nint  s_pop(SNode **head, int *out);\nint  s_remove(SNode **head, int v);\nsize_t s_len(const SNode *head);\nint  s_sum(const SNode *head);\nvoid s_clear(SNode **head);\nint  s_insert_sorted(SNode **head, int v);\n",
            [
                (
                    "push/pop/remove/clear",
                    r"""
SNode *head = NULL;
int v;
CHECK_EQ(s_len(head), 0);
CHECK_EQ(s_pop(&head, &v), -1);              /* empty */
CHECK_EQ(s_push(&head, 3), 0);
CHECK_EQ(s_push(&head, 1), 0);
CHECK_EQ(s_push(&head, 2), 0);               /* list: 2 1 3 */
CHECK_EQ(s_len(head), 3);
CHECK_EQ(s_sum(head), 6);
CHECK_EQ(s_pop(&head, &v), 0); CHECK_EQ(v, 2);
CHECK_EQ(s_remove(&head, 3), 1);
CHECK_EQ(s_remove(&head, 3), 0);             /* already gone */
CHECK_EQ(s_remove(&head, 1), 1);             /* removes last node */
CHECK_EQ(s_len(head), 0);
CHECK_EQ(s_push(&head, 9), 0);               /* reusable after drain */
CHECK_EQ(s_sum(head), 9);
s_clear(&head);
CHECK(head == NULL);
""",
                    "pop: save next, free, update head. remove: the **link walk avoids special cases.",
                ),
                (
                    "sorted insert",
                    r"""
SNode *head = NULL;
int vals[] = {5, 1, 3, 9, 7};
for (int i = 0; i < 5; i++) CHECK_EQ(s_insert_sorted(&head, vals[i]), 0);
/* expect: 1 3 5 7 9 */
const SNode *p = head;
CHECK(p && p->value == 1);
CHECK(p->next && p->next->value == 3);
CHECK(p->next->next && p->next->next->value == 5);
CHECK(p->next->next->next && p->next->next->next->value == 7);
CHECK(p->next->next->next->next && p->next->next->next->next->value == 9);
CHECK_EQ(s_len(head), 5);
s_clear(&head);
""",
                    "Walk until the first node with value > v; insert before it. Empty list inserts at head.",
                ),
            ],
        ),
        challenge(
            "cint-p7-slist-algos",
            "List Algorithms",
            """Extend the list with the classic interview algorithms:

```c
/* reverses the list in place; head updated through the pointer */
void s_reverse(SNode **head);
/* returns the middle node's value; for even lengths returns the
   FIRST of the two middles; -1 if empty. Does not modify the list. */
int s_middle(const SNode *head);
/* returns 1 if the list's values are in nondecreasing order */
int s_is_sorted(const SNode *head);
/* removes every node whose value equals v (possibly many) */
void s_remove_all(SNode **head, int v);
```""",
            C_PRELUDE + "\n#include <stddef.h>\n#include <stdlib.h>\ntypedef struct SNode { int value; struct SNode *next; } SNode;\nvoid s_reverse(SNode **head);\nint s_middle(const SNode *head);\nint s_is_sorted(const SNode *head);\nvoid s_remove_all(SNode **head, int v);\n/* support helpers provided (implement only the four above) */\nstatic void s_push(SNode **head, int v) { SNode *n = malloc(sizeof *n); if (!n) return; n->value = v; n->next = *head; *head = n; }\nstatic size_t s_len(const SNode *head) { size_t n = 0; for (const SNode *p = head; p; p = p->next) n++; return n; }\nstatic void s_clear(SNode **head) { SNode *cur = *head; while (cur) { SNode *nx = cur->next; free(cur); cur = nx; } *head = NULL; }\n",
            [
                (
                    "reverse, middle, remove_all",
                    r"""
SNode *head = NULL;
for (int i = 1; i <= 5; i++) s_push(&head, i);   /* 5 4 3 2 1 */
s_reverse(&head);
/* now 1 2 3 4 5 */
CHECK(head->value == 1);
CHECK(head->next->value == 2);
CHECK(head->next->next->next->next->value == 5);
CHECK_EQ(s_middle(head), 3);
CHECK_EQ(s_is_sorted(head), 1);
s_remove_all(&head, 3);
CHECK_EQ(s_len(head) == 0 ? 0 : head->value, 1);  /* survived */
/* rebuild: 5 3 3 1 */
SNode *h2 = NULL;
s_push(&h2, 1); s_push(&h2, 3); s_push(&h2, 3); s_push(&h2, 5);
s_remove_all(&h2, 3);
CHECK_EQ(s_len(h2), 2);
CHECK(h2->value == 5 && h2->next->value == 1);
s_clear(&h2);
s_clear(&head);
""",
                    "Middle: two pointers, slow/fast — slow lands on the first middle for even lengths. remove_all: **link walk.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p7-slist-core": vi_challenge(
            "Phẫu thuật danh sách",
            "Cài s_push/s_pop/s_remove/s_len/s_sum/s_clear/s_insert_sorted.",
            [("phẫu thuật", "pop: lưu next, free, cập nhật head. remove: đi bằng **link.")],
        ),
        "cint-p7-slist-algos": vi_challenge(
            "Thuật toán trên danh sách",
            "Cài s_reverse, s_middle (hai con trỏ), s_is_sorted, s_remove_all.",
            [("reverse, middle, remove_all", "middle: slow/fast — slow dừng ở middle đầu cho chiều chẵn.")],
        ),
    },
    solutions=[
        (
            "cint-p7-slist-core",
            r"""
#include <stdlib.h>
#include <stddef.h>
int s_push(SNode **head, int v) {
    if (!head) return -1;
    SNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    n->next = *head;
    *head = n;
    return 0;
}
int s_pop(SNode **head, int *out) {
    if (!head || !*head || !out) return -1;
    SNode *n = *head;
    *out = n->value;
    *head = n->next;
    free(n);
    return 0;
}
int s_remove(SNode **head, int v) {
    if (!head) return 0;
    SNode **link = head;
    for (SNode *cur = *head; cur; cur = cur->next) {
        if (cur->value == v) {
            *link = cur->next;
            free(cur);
            return 1;
        }
        link = &cur->next;
    }
    return 0;
}
size_t s_len(const SNode *head) {
    size_t n = 0;
    for (const SNode *p = head; p; p = p->next) n++;
    return n;
}
int s_sum(const SNode *head) {
    int t = 0;
    for (const SNode *p = head; p; p = p->next) t += p->value;
    return t;
}
void s_clear(SNode **head) {
    if (!head) return;
    SNode *cur = *head;
    while (cur) {
        SNode *next = cur->next;
        free(cur);
        cur = next;
    }
    *head = NULL;
}
int s_insert_sorted(SNode **head, int v) {
    if (!head) return -1;
    SNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    SNode **link = head;
    while (*link && (*link)->value <= v) link = &(*link)->next;
    n->next = *link;
    *link = n;
    return 0;
}""",
            r"""
#include <stdlib.h>
#include <stddef.h>
int s_push(SNode **head, int v) {
    if (!head) return -1;
    SNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    n->next = *head;
    *head = n;
    return 0;
}
int s_pop(SNode **head, int *out) {
    if (!head || !*head || !out) return -1;
    SNode *n = *head;
    *out = n->value;
    free(n);                      /* wrong: *head now dangles */
    *head = n->next;              /* wrong: use-after-free ordering */
    return 0;
}
int s_remove(SNode **head, int v) {
    if (!head) return 0;
    for (SNode *cur = *head; cur; cur = cur->next) {
        if (cur->value == v) {
            free(cur);            /* wrong: previous node still points here */
            return 1;
        }
        cur = cur->next;          /* wrong: also reads freed memory on the walk */
    }
    return 0;
}
size_t s_len(const SNode *head) {
    size_t n = 0;
    for (const SNode *p = head; p; p = p->next) n++;
    return n;
}
int s_sum(const SNode *head) {
    int t = 0;
    for (const SNode *p = head; p; p = p->next) t += p->value;
    return t;
}
void s_clear(SNode **head) {
    if (!head) return;
    SNode *cur = *head;
    while (cur) {
        free(cur);                /* wrong: cur->next read after free */
        cur = cur->next;
    }
    *head = NULL;
}
int s_insert_sorted(SNode **head, int v) {
    if (!head) return -1;
    SNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->value = v;
    SNode **link = head;
    while (*link && (*link)->value < v) link = &(*link)->next;   /* wrong: < puts equal values AFTER existing equals (unstable) — hidden by tiny tests, but wrong contract */
    n->next = *link;
    *link = n;
    return 0;
}""",
        ),
        (
            "cint-p7-slist-algos",
            r"""
#include <stdlib.h>
#include <stddef.h>
void s_reverse(SNode **head) {
    if (!head) return;
    SNode *prev = NULL, *cur = *head;
    while (cur) {
        SNode *next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
    }
    *head = prev;
}
int s_middle(const SNode *head) {
    if (!head) return -1;
    const SNode *slow = head, *fast = head;
    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow->value;
}
int s_is_sorted(const SNode *head) {
    for (const SNode *p = head; p && p->next; p = p->next)
        if (p->value > p->next->value) return 0;
    return 1;
}
void s_remove_all(SNode **head, int v) {
    if (!head) return;
    SNode **link = head;
    while (*link) {
        if ((*link)->value == v) {
            SNode *doomed = *link;
            *link = doomed->next;
            free(doomed);
        } else {
            link = &(*link)->next;
        }
    }
}""",
            r"""
#include <stdlib.h>
#include <stddef.h>
void s_reverse(SNode **head) {
    if (!head || !*head) return;
    SNode *prev = NULL, *cur = *head;
    while (cur) {
        SNode *next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
    }
    *head = prev;
}
int s_middle(const SNode *head) {
    if (!head) return -1;
    const SNode *slow = head, *fast = head->next;   /* wrong: fast starts one ahead */
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow->value;
}
int s_is_sorted(const SNode *head) {
    if (!head) return 0;                 /* wrong: empty is sorted */
    for (const SNode *p = head; p && p->next; p = p->next)
        if (p->value > p->next->value) return 0;
    return 1;
}
void s_remove_all(SNode **head, int v) {
    if (!head) return;
    for (SNode *cur = *head; cur; cur = cur->next) {
        if (cur->value == v) {
            SNode *doomed = cur;
            free(doomed);                /* wrong: prev still points at freed node */
            cur = cur->next;             /* wrong: read after free */
        }
    }
}""",
        ),
    ],
)

write_practice(
    M, "cint-p7-dlist",
    "Doubly List & Deque Gym",
    "Sentinel ring list with O(1) push/pop at both ends.",
    "Phòng gym doubly list & deque",
    "Danh sách ring với sentinel, push/pop O(1) ở cả hai đầu.",
    after_lesson="stacks-queues",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p7-deque",
            "Build the Sentinel Deque",
            """Implement a deque over a sentinel ring. The boilerplate declares:

```c
typedef struct DNode {
    int value;
    struct DNode *prev, *next;
} DNode;
/* the caller owns the sentinel; init makes it self-linked */
void dq_init(DNode *s);
void dq_push_front(DNode *s, int v);
void dq_push_back(DNode *s, int v);
int  dq_pop_front(DNode *s, int *out);   /* 0 ok, -1 empty */
int  dq_pop_back(DNode *s, int *out);    /* 0 ok, -1 empty */
size_t dq_len(const DNode *s);
/* 1 if a forward walk and a backward walk see the same values reversed */
int dq_consistent(const DNode *s);
```""",
            C_PRELUDE + "\n#include <stddef.h>\ntypedef struct DNode {\n    int value;\n    struct DNode *prev, *next;\n} DNode;\nvoid dq_init(DNode *s);\nvoid dq_push_front(DNode *s, int v);\nvoid dq_push_back(DNode *s, int v);\nint  dq_pop_front(DNode *s, int *out);\nint  dq_pop_back(DNode *s, int *out);\nsize_t dq_len(const DNode *s);\nint dq_consistent(const DNode *s);\n",
            [
                (
                    "both ends, one ring",
                    r"""
DNode s;
dq_init(&s);
int v;
CHECK_EQ(dq_len(&s), 0);
CHECK_EQ(dq_pop_front(&s, &v), -1);
CHECK_EQ(dq_pop_back(&s, &v), -1);
dq_push_back(&s, 2);
dq_push_front(&s, 1);
dq_push_back(&s, 3);                    /* 1 2 3 */
CHECK_EQ(dq_len(&s), 3);
CHECK_EQ(dq_pop_front(&s, &v), 0); CHECK_EQ(v, 1);
CHECK_EQ(dq_pop_back(&s, &v), 0); CHECK_EQ(v, 3);
CHECK_EQ(dq_pop_front(&s, &v), 0); CHECK_EQ(v, 2);
CHECK_EQ(dq_len(&s), 0);
CHECK_EQ(dq_pop_back(&s, &v), -1);      /* drained both ways */
dq_push_front(&s, 7);                   /* reusable */
CHECK_EQ(dq_len(&s), 1);
CHECK_EQ(dq_consistent(&s), 1);
""",
                    "push X: link between s and s->next (front) or s->prev and s (back). Sentinel never stores data.",
                ),
                (
                    "consistency under churn",
                    r"""
DNode s;
dq_init(&s);
for (int i = 0; i < 10; i++) {
    if (i % 2) dq_push_back(&s, i); else dq_push_front(&s, i);
}
CHECK_EQ(dq_len(&s), 10);
CHECK_EQ(dq_consistent(&s), 1);
int v;
for (int i = 0; i < 10; i++) CHECK_EQ(dq_pop_front(&s, &v), 0);
CHECK_EQ(dq_len(&s), 0);
CHECK_EQ(dq_consistent(&s), 1);         /* empty ring is consistent */
""",
                    "If prev/next ever disagree, dq_consistent catches it — forward and backward walks differ.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p7-deque": vi_challenge(
            "Dựng sentinel deque",
            "Cài deque trên ring sentinel: push/pop hai đầu, dq_len, dq_consistent.",
            [("hai đầu, một ring", "push front: nối giữa s và s->next; back: giữa s->prev và s.")],
        ),
    },
    solutions=[
        (
            "cint-p7-deque",
            r"""
#include <stdlib.h>
#include <stddef.h>
void dq_init(DNode *s) {
    if (!s) return;
    s->prev = s;
    s->next = s;
}
static void link_after(DNode *at, DNode *n) {
    n->prev = at;
    n->next = at->next;
    at->next->prev = n;
    at->next = n;
}
void dq_push_front(DNode *s, int v) {
    if (!s) return;
    DNode *n = malloc(sizeof *n);
    if (!n) return;
    n->value = v;
    link_after(s, n);
}
void dq_push_back(DNode *s, int v) {
    if (!s) return;
    DNode *n = malloc(sizeof *n);
    if (!n) return;
    n->value = v;
    link_after(s->prev, n);
}
static int unlink_pop(DNode *victim, int *out) {
    *out = victim->value;
    victim->prev->next = victim->next;
    victim->next->prev = victim->prev;
    free(victim);
    return 0;
}
int dq_pop_front(DNode *s, int *out) {
    if (!s || !out || s->next == s) return -1;
    return unlink_pop(s->next, out);
}
int dq_pop_back(DNode *s, int *out) {
    if (!s || !out || s->prev == s) return -1;
    return unlink_pop(s->prev, out);
}
size_t dq_len(const DNode *s) {
    if (!s) return 0;
    size_t n = 0;
    for (const DNode *p = s->next; p != s; p = p->next) n++;
    return n;
}
int dq_consistent(const DNode *s) {
    if (!s) return 0;
    /* forward walk: every node's links must be mutual, and the walk
       must return home; backward walk must take exactly as many steps. */
    size_t forward = 0;
    for (const DNode *p = s->next; p != s; p = p->next) {
        if (p->next->prev != p) return 0;   /* forward chain consistent */
        if (p->prev->next != p) return 0;   /* backward chain consistent */
        forward++;
        if (forward > 1000000) return 0;    /* cycle guard */
    }
    size_t backward = 0;
    for (const DNode *p = s->prev; p != s; p = p->prev) {
        backward++;
        if (backward > forward) return 0;
    }
    return forward == backward;
}""",
            r"""
#include <stdlib.h>
#include <stddef.h>
void dq_init(DNode *s) {
    if (!s) return;
    s->prev = s;
    s->next = s;
}
void dq_push_front(DNode *s, int v) {
    if (!s) return;
    DNode *n = malloc(sizeof *n);
    if (!n) return;
    n->value = v;
    n->next = s->next;
    s->next = n;              /* wrong: forgot n->prev and the back-link fix */
    n->prev = s;
}
void dq_push_back(DNode *s, int v) {
    if (!s) return;
    DNode *n = malloc(sizeof *n);
    if (!n) return;
    n->value = v;
    n->prev = s->prev;
    s->prev = n;              /* wrong: forgot n->next and the forward-link fix */
    n->next = s;
}
int dq_pop_front(DNode *s, int *out) {
    if (!s || !out || s->next == s) return -1;
    DNode *n = s->next;
    *out = n->value;
    s->next = n->next;        /* wrong: n->next's prev still points at freed node */
    free(n);
    return 0;
}
int dq_pop_back(DNode *s, int *out) {
    if (!s || !out || s->prev == s) return -1;
    DNode *n = s->prev;
    *out = n->value;
    s->prev = n->prev;        /* wrong: same, other direction */
    free(n);
    return 0;
}
size_t dq_len(const DNode *s) {
    if (!s) return 0;
    size_t n = 0;
    for (const DNode *p = s->next; p != s; p = p->next) n++;
    return n;
}
int dq_consistent(const DNode *s) {
    if (!s) return 0;
    return 1;                 /* wrong: claims consistency without checking */
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m7-task",
    "Merge Two Sorted Lists",
    """The classic in-place merge. The boilerplate declares:

```c
typedef struct SNode { int value; struct SNode *next; } SNode;
/* merges ascending lists a and b into ONE ascending list; returns its
   head. On success *a_head and *b_head are set to NULL (the merge takes
   the nodes, no new allocations, no copying). Either input may be empty.
   Lists need not be pre-deduplicated; equal values keep both. */
SNode *s_merge_sorted(SNode **a_head, SNode **b_head);
```""",
    C_PRELUDE + "\n#include <stddef.h>\ntypedef struct SNode { int value; struct SNode *next; } SNode;\nSNode *s_merge_sorted(SNode **a_head, SNode **b_head);\n",
    [
        (
            "merge with no allocation",
            r"""
SNode *a = NULL, *b = NULL;
/* build a: 1 3 5 ; b: 2 3 6 (helper-free: use push then reverse) */
int av[] = {5, 3, 1}, bv[] = {6, 3, 2};
for (int i = 0; i < 3; i++) {
    SNode *n = malloc(sizeof *n);
    CHECK(n);
    n->value = av[i]; n->next = a; a = n;
    SNode *m = malloc(sizeof *m);
    CHECK(m);
    m->value = bv[i]; m->next = b; b = m;
}
SNode *m = s_merge_sorted(&a, &b);
CHECK(a == NULL && b == NULL);          /* inputs consumed */
CHECK(m->value == 1);
int expect[] = {1, 2, 3, 3, 5, 6};
SNode *p = m;
for (int i = 0; i < 6; i++) {
    CHECK(p && p->value == expect[i]);
    p = p->next;
}
CHECK(p == NULL);                        /* exactly 6 nodes */
/* drain-destroy: free the merged list */
while (m) { SNode *nx = m->next; free(m); m = nx; }
""",
            "Splice by walking both heads; the smaller head becomes the next output node. Take care: advance the head you took FROM.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Trộn hai danh sách đã sắp",
        "Cài s_merge_sorted: trộn in-place, không cấp phát, tiêu thụ cả hai input, giữ trùng.",
        [("trộn không cấp phát", "đi cả hai head; head nhỏ hơn thành node output kế.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m7",
    "Checkpoint: The Linked Toolkit",
    "Prove the pointer surgery: in-place merge of two sorted lists with zero allocation.",
    24,
    r"""
## The task

Implement `s_merge_sorted` (see the challenge). This is the module's
harvest: you must walk two lists, splice nodes without allocating, keep
duplicates, handle either-empty inputs, and leave both input heads NULL —
pure pointer surgery under contract.

Passing this proves you can build the canonical linked-list operation
that every higher structure (merge sort, LRU splices, intrusive lists)
rests on.

Next module: hash tables — arrays of nodes, hashing, and collision
handling.
""",
    "Kiểm tra: Bộ công cụ liên kết",
    "Chứng minh phẫu thuật con trỏ: trộn in-place hai danh sách đã sắp với không cấp phát.",
    r"""
## Bài toán

Cài `s_merge_sorted` (xem challenge). Đây là mùa quả của module: đi hai
danh sách, nối node không cấp phát, giữ trùng, xử lý input rỗng, và để
cả hai head input thành NULL — phẫu thuật con trỏ thuần túy dưới hợp đồng.

Vượt qua chứng minh bạn dựng được thao tác list kinh điển mà mọi cấu trúc
cao hơn (merge sort, LRU splice, intrusive list) dựa vào.

Module sau: hash table — mảng của node, hashing, và xử lý va chạm.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <stdlib.h>
#include <stddef.h>
SNode *s_merge_sorted(SNode **a_head, SNode **b_head) {
    if (!a_head || !b_head) return NULL;
    SNode *a = *a_head, *b = *b_head;
    SNode *head = NULL, **tail = &head;
    while (a && b) {
        SNode **take = (a->value <= b->value) ? &a : &b;
        SNode *n = *take;
        *take = n->next;          /* advance the list we took from */
        n->next = NULL;
        *tail = n;                /* append to output */
        tail = &n->next;
    }
    SNode *rest = a ? a : b;      /* append the leftover run */
    *tail = rest;
    *a_head = NULL;
    *b_head = NULL;
    return head;
}""",
    wrong=r"""
#include <stdlib.h>
#include <stddef.h>
SNode *s_merge_sorted(SNode **a_head, SNode **b_head) {
    if (!a_head || !b_head) return NULL;
    SNode *a = *a_head, *b = *b_head;
    SNode *head = NULL, **tail = &head;
    while (a && b) {
        if (a->value < b->value) {          /* wrong: < loses ties' stability AND
                                               advances the wrong list below on equal */
            SNode *n = a;
            a = n->next;
            n->next = NULL;
            *tail = n;
            tail = &n->next;
        } else {
            SNode *n = b;
            b = n->next;
            n->next = a->next;              /* wrong: corrupts a's chain */
            *tail = n;
            tail = &n->next;
        }
    }
    *tail = a ? a : b;
    *a_head = NULL;
    *b_head = NULL;
    return head;
}""",
)

print("module 7 complete")
