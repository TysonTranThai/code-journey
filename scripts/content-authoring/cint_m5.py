#!/usr/bin/env python3
"""C — Intermediate — Module 5: cint-structs.

Structs as the modeling tool: layout and padding observed (sizeof is real,
not memorized), self-referential nodes, opaque handles with accessors, and
ownership documented in every API. House conventions: ISO C only, raw
triple-quoted strings, self-contained tests, Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-structs"

write_module(
    M,
    "Structs & Data Modeling",
    "Layout you can measure, self-referential types, opaque handles, and the "
    "who-frees-it rule written into every API.",
    "Struct & mô hình hóa dữ liệu",
    "Layout đo đạc được, kiểu tự tham chiếu, opaque handle, và quy tắc "
    "ai-free-ai được ghi vào từng API.",
    lessons=["layout-sizeof", "self-referential", "opaque-handles", "cint-checkpoint-m5"],
    practices=["cint-p5-layout", "cint-p5-modeling"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "layout-sizeof",
    "Layout, Padding & offsetof",
    "Why sizeof a struct is not the sum of its members, and how to measure layout instead of guessing.",
    16,
    r"""
## The compiler may insert holes

Each member must sit at an offset that is a multiple of its alignment.
The compiler inserts invisible padding to make that true, and pads the
struct's total size so arrays of it stay aligned:

```c
struct Packed {
    char  c;      /* offset 0 */
                  /* 3 bytes padding */
    int   i;      /* offset 4 */
    char  d;      /* offset 8 */
                  /* 3 bytes padding (so sizeof works for arrays) */
};                /* sizeof == 12, not 6 */
```

Reordering members largest-first usually shrinks the struct. But **do not
memorize layouts — measure them**:

```c
#include <stddef.h>
offsetof(struct Packed, i)   /* == 4: the offset as actually compiled */
sizeof(struct Packed)        /* == 12 */
```

`offsetof` answers "where is this member really" under *this* compiler,
*this* standard, *these* flags. Code that files into binary formats uses
it — or better, uses it in a `_Static_assert` to fail the build if the
layout ever drifts:

```c
_Static_assert(offsetof(struct Header, magic) == 0, "header layout");
```

## Alignment is a property of types

`int` aligns to 4, `double` to 8, pointers to 8 (on 64-bit). The struct's
own alignment is the max of its members'. That is why member order
matters and why the trailing padding exists.
""",
    "Layout, Padding & offsetof",
    "Layout đo đạc được: sizeof, offsetof, padding.",
    r"""
## Trình biên dịch có thể chèn lỗ

Mỗi member phải nằm ở offset chia hết cho alignment của nó. Trình biên dịch
chèn padding vô hình để đảm bảo điều đó, và pad tổng kích thước struct để
mảng của nó vẫn alignment:

```c
struct Packed {
    char  c;      /* offset 0 */
                  /* 3 byte padding */
    int   i;      /* offset 4 */
    char  d;      /* offset 8 */
                  /* 3 byte padding */
};                /* sizeof == 12, không phải 6 */
```

Sắp xếp member từ lớn đến nhỏ thường làm struct nhỏ đi. Nhưng **đừng học
thuộc layout — hãy đo**:

```c
#include <stddef.h>
offsetof(struct Packed, i)   /* == 4 */
sizeof(struct Packed)        /* == 12 */
```

`offsetof` trả lời "member này thực sự nằm đâu" dưới compiler/flags hiện tại.
Code ghi file nhị phân dùng nó — hoặc dùng `_Static_assert` để fail build
nếu layout đổi.
""",
)

write_lesson(
    M, "self-referential",
    "Self-Referential Types",
    "Nodes that point to their own kind, why pointers (not values) are mandatory there, and forward declarations.",
    15,
    r"""
## A node contains a link to a node

```c
typedef struct Node {
    int          value;
    struct Node *next;    /* pointer to my own kind */
} Node;
```

Two details carry real weight:

**1. The tag and the typedef are different names.** Inside the braces the
typedef isn't complete yet, so you must write `struct Node *next`. Writing
`Node *next` there does not compile.

**2. It must be a pointer.** `struct Node next;` would ask the compiler
for a struct containing itself — infinite size. A *pointer* to your own
type is fine: a pointer has a fixed size.

The same trick models mutual recursion with a forward declaration:

```c
struct Edge;                     /* forward: name only, no body yet */
typedef struct Vertex {
    struct Edge *out;           /* edges leaving this vertex */
} Vertex;
struct Edge {
    Vertex *to;
    struct Edge *next;
};
```

## Ownership is now a graph question

Every node holds a pointer. Before writing any list/tree API, write in the
header comment: who owns `next`? (Answer that makes bugs rare: the list
owns every node it reachable-holds; freeing the list frees the nodes;
borrowers never free, never store past their loan.)
""",
    "Kiểu tự tham chiếu",
    "Node tự tham chiếu: tag vs typedef, con trỏ bắt buộc, forward declaration.",
    r"""
## Node chứa link đến chính kiểu của nó

```c
typedef struct Node {
    int          value;
    struct Node *next;    /* con trỏ đến cùng kiểu */
} Node;
```

Hai chi tiết mang trọng lượng thật:

**1. Tag và typedef là hai tên khác nhau.** Trong ngoặc, typedef chưa
hoàn tất, nên phải viết `struct Node *next`. Viết `Node *next` tại đó
không compile.

**2. Phải là con trỏ.** `struct Node next;` yêu cầu struct chứa chính nó —
kích thước vô hạn. *Con trỏ* đến kiểu của mình thì ổn: con trỏ có kích
thước cố định.

Cùng thủ thuật mô hình hóa đệ quy hỗ tương với forward declaration:

```c
struct Edge;                     /* forward: chỉ tên, chưa có body */
typedef struct Vertex {
    struct Edge *out;
} Vertex;
struct Edge {
    Vertex *to;
    struct Edge *next;
};
```

## Ownership giờ là câu hỏi của đồ thị

Mỗi node giữ một con trỏ. Trước khi viết API list/tree, hãy ghi vào comment
header: ai sở hữu `next`? (Câu trả lời khiến bug hiếm: list sở hữu mọi node
nó truy cập được; free list là free các node; bên mượn không free, không
lưu con trỏ quá hạn mượn.)
""",
)

write_lesson(
    M, "opaque-handles",
    "Opaque Handles & Encapsulation",
    "The pimpl pattern in C: hide the struct body, expose functions, and make invariants unbreakable from outside.",
    17,
    r"""
## Encapsulation = the client cannot see inside

If a header exposes the struct body, any client can poke `q->data[i]`
directly — and every invariant you maintain becomes unenforceable. C's
encapsulation tool is the **opaque type**: declare the name, define the
body in exactly one .c file:

```c
/* stack.h — the public contract */
typedef struct Stack Stack;          /* name without a body */
Stack *stack_create(void);
int    stack_push(Stack *s, int v);  /* 0 ok, -1 oom */
int    stack_pop(Stack *s, int *out);/* 0 ok, -1 empty */
void   stack_destroy(Stack *s);      /* frees everything it owns */
```

```c
/* stack.c — the private truth */
struct Stack {
    int  *data;
    size_t len, cap;
};
```

Clients get handles (`Stack *`) they can pass around but cannot
dereference. Every access goes through your functions — so the invariant
"`data` is non-NULL while `cap > 0`" is checked in exactly one place.

## The price and the payoff

Price: every field you later want to expose needs a function. Payoff:
you can *change the representation* — grow policy, structure, even a
linked implementation — without recompiling one client. That is why real
libraries (stdio's `FILE`, POSIX's `DIR`) are opaque.

Ownership rule, written on the handle: the creator owns it; functions
borrow; the destroyer ends the story. If an API hands out a pointer
*into* the handle (`const char *map_get(...)`), document that the loan
lives until the next mutating call on the same object.
""",
    "Opaque Handles & Encapsulation",
    "Opaque handle: ẩn body, lộ hàm, bất biến không thể phá từ ngoài.",
    r"""
## Encapsulation = client không nhìn thấy bên trong

Nếu header lộ body của struct, client nào cũng có thể đụng `q->data[i]`
trực tiếp — và mọi invariant bạn giữ trở nên không thể bảo vệ. Công cụ
encapsulation của C là **opaque type**: khai báo tên, định nghĩa body
trong đúng một file .c:

```c
/* stack.h — hợp đồng công khai */
typedef struct Stack Stack;
Stack *stack_create(void);
int    stack_push(Stack *s, int v);  /* 0 ok, -1 oom */
int    stack_pop(Stack *s, int *out);/* 0 ok, -1 empty */
void   stack_destroy(Stack *s);      /* free mọi thứ nó sở hữu */
```

```c
/* stack.c — sự thật riêng tư */
struct Stack {
    int  *data;
    size_t len, cap;
};
```

Client chỉ có handle (`Stack *`) để truyền qua lại chứ không dereference
được. Mọi truy cập đi qua hàm của bạn — invariant "`data` khác NULL khi
`cap > 0`" được kiểm ở đúng một nơi.

## Giá và lợi

Giá: mỗi field muốn lộ ra cần một hàm. Lợi: bạn có thể *đổi cách biểu
diễn* — chiến lược grow, cấu trúc, thậm chí chuyển sang linked — mà không
phải recompile một client nào. Vì thế các thư viện thật (stdio's `FILE`,
POSIX's `DIR`) đều opaque.

Quy tắc ownership ghi trên handle: người tạo sở hữu; hàm chỉ mượn; hàm
destroy kết thúc câu chuyện. Nếu API trả con trỏ *vào trong* handle
(`const char *map_get(...)`), hãy ghi rõ khoản mượn sống đến lần gọi
mutating kế tiếp trên cùng object.
""",
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p5-layout",
    "Layout Gym",
    "Measure struct layout with offsetof and sizeof; assert it.",
    "Phòng gym layout",
    "Đo layout struct bằng offsetof và sizeof; assert nó.",
    after_lesson="layout-sizeof",
    minutes=22,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p5-mixed-layout",
            "Measure a Mixed Struct",
            """The boilerplate defines:

```c
struct Record {
    char  kind;
    long  amount;
    char  flag;
};
```

Implement, **without naming any hard-coded sizes in the answer's logic**
(use the operators, not magic numbers):

```c
/* offset of each member, as actually compiled */
size_t rec_kind_off(void);
size_t rec_amount_off(void);
size_t rec_flag_off(void);
/* total compiled size */
size_t rec_size(void);
/* how many Records fit in a buffer of n bytes (n/sizeof, floor; 0 if n < size) */
size_t rec_capacity(size_t n);
```""",
            C_PRELUDE + "\n#include <stddef.h>\nstruct Record { char kind; long amount; char flag; };\n",
            [
                (
                    "offsets are measured, not guessed",
                    r"""
CHECK(rec_kind_off() == 0);
CHECK(rec_amount_off() >= sizeof(long) && rec_amount_off() <= rec_size());
CHECK(rec_flag_off() > rec_amount_off());
CHECK(rec_size() >= rec_flag_off() + 1);
CHECK_EQ(rec_capacity(0), 0);
CHECK(rec_capacity(rec_size()) == 1);
CHECK(rec_capacity(rec_size() * 7) == 7);
CHECK(rec_capacity(rec_size() - 1) == 0);
""",
                    "offsetof(struct Record, member) for offsets; sizeof for the rest. rec_capacity: n < size -> 0.",
                ),
            ],
        ),
        challenge(
            "cint-p5-reorder",
            "Shrink by Reordering",
            """The boilerplate defines a wasteful struct and a mirror:

```c
struct Naive {  char a; double d; char b; long l; };
struct Tight { double d; long l; char a; char b; };
```

Implement:

```c
/* 1 if Tight is strictly smaller than Naive, else 0 */
int tight_is_smaller(void);
/* bytes wasted by padding inside a struct of size total with raw member bytes raw */
size_t padding_bytes(size_t total, size_t raw);
/* size of an array of n Tight structs */
size_t tight_array_bytes(size_t n);
```""",
            C_PRELUDE + "\n#include <stddef.h>\nstruct Naive {  char a; double d; char b; long l; };\nstruct Tight { double d; long l; char a; char b; };\n",
            [
                (
                    "size arithmetic",
                    r"""
CHECK(tight_is_smaller() == 1);
CHECK_EQ(padding_bytes(sizeof(struct Naive), 1 + 8 + 1 + 8),
         sizeof(struct Naive) - 18);
CHECK_EQ(tight_array_bytes(5), 5 * sizeof(struct Tight));
CHECK_EQ(tight_array_bytes(0), 0);
""",
                    "tight_is_smaller: sizeof comparison. padding_bytes: total - raw. Arrays multiply sizeof.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p5-mixed-layout": vi_challenge(
            "Đo struct lẫn loại",
            "Cài rec_*_off bằng offsetof, rec_size, rec_capacity (n/sizeof, floor; n < size -> 0).",
            [("offset đo được", "offsetof(struct Record, member); không hard-code số.")],
        ),
        "cint-p5-reorder": vi_challenge(
            "Thu nhỏ bằng cách sắp lại",
            "Cài tight_is_smaller, padding_bytes(total, raw), tight_array_bytes(n).",
            [("số học kích thước", "sizeof so sánh; padding = total - raw; mảng nhân sizeof.")],
        ),
    },
    solutions=[
        (
            "cint-p5-mixed-layout",
            r"""
#include <stddef.h>
size_t rec_kind_off(void) { return offsetof(struct Record, kind); }
size_t rec_amount_off(void) { return offsetof(struct Record, amount); }
size_t rec_flag_off(void) { return offsetof(struct Record, flag); }
size_t rec_size(void) { return sizeof(struct Record); }
size_t rec_capacity(size_t n) {
    size_t sz = sizeof(struct Record);
    return n < sz ? 0 : n / sz;
}""",
            r"""
#include <stddef.h>
size_t rec_kind_off(void) { return 0; }
size_t rec_amount_off(void) { return 1; }   /* wrong: ignores padding */
size_t rec_flag_off(void) { return 8; }
size_t rec_size(void) { return 9; }         /* wrong: sum of members */
size_t rec_capacity(size_t n) { return n / 9; }  /* wrong: magic size, wrong floor semantics */
""",
        ),
        (
            "cint-p5-reorder",
            r"""
#include <stddef.h>
int tight_is_smaller(void) { return sizeof(struct Tight) < sizeof(struct Naive); }
size_t padding_bytes(size_t total, size_t raw) {
    return total >= raw ? total - raw : 0;
}
size_t tight_array_bytes(size_t n) { return n * sizeof(struct Tight); }""",
            r"""
#include <stddef.h>
int tight_is_smaller(void) { return 0; }    /* wrong: claims no win */
size_t padding_bytes(size_t total, size_t raw) {
    return total + raw;                     /* wrong: adds instead of subtracts */
}
size_t tight_array_bytes(size_t n) { return n; }  /* wrong: forgets element size */
""",
        ),
    ],
)

write_practice(
    M, "cint-p5-modeling",
    "Modeling & Ownership Gym",
    "Opaque handles with enforced invariants and self-referential graphs with documented ownership.",
    "Phòng gym mô hình hóa & ownership",
    "Opaque handle với bất biến được bảo vệ và đồ thị tự tham chiếu có ownership rõ ràng.",
    after_lesson="opaque-handles",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p5-opaque-counter",
            "Build an Opaque Handle",
            """Implement an opaque multi-counter. The boilerplate declares:

```c
typedef struct MCounter MCounter;
MCounter *mc_create(void);                 /* NULL on oom */
int mc_bump(MCounter *m, const char *key, int by); /* 0 ok, -1 args/oom */
int mc_get(const MCounter *m, const char *key);    /* count, 0 if absent */
size_t mc_keys(const MCounter *m);         /* number of distinct keys */
void mc_destroy(MCounter *m);
```

Keys are short (<= 15 chars). Store them however you like — the tests only
see the API. The constructor must leave a valid object for `mc_keys() == 0`
and `mc_get(...) == 0`; every function must tolerate NULL handles.""",
            C_PRELUDE + "\n#include <stddef.h>\ntypedef struct MCounter MCounter;\nMCounter *mc_create(void);\nint mc_bump(MCounter *m, const char *key, int by);\nint mc_get(const MCounter *m, const char *key);\nsize_t mc_keys(const MCounter *m);\nvoid mc_destroy(MCounter *m);\n",
            [
                (
                    "API discipline",
                    r"""
MCounter *m = mc_create();
CHECK(m != NULL);
CHECK_EQ(mc_keys(m), 0);
CHECK_EQ(mc_get(m, "hits"), 0);
CHECK_EQ(mc_bump(m, "hits", 1), 0);
CHECK_EQ(mc_bump(m, "hits", 4), 0);
CHECK_EQ(mc_bump(m, "miss", 2), 0);
CHECK_EQ(mc_get(m, "hits"), 5);
CHECK_EQ(mc_get(m, "miss"), 2);
CHECK_EQ(mc_keys(m), 2);
CHECK_EQ(mc_bump(NULL, "x", 1), -1);
CHECK_EQ(mc_bump(m, NULL, 1), -1);
CHECK_EQ(mc_get(NULL, "hits"), 0);
mc_destroy(m);
mc_destroy(NULL);   /* must be a no-op */
""",
                    "A small fixed array of {char key[16]; int count;} slots keeps this focused on the API, not storage.",
                ),
            ],
        ),
        challenge(
            "cint-p5-graph-free",
            "Free a Graph Exactly Once",
            """The boilerplate declares a tiny DAG of named nodes:

```c
typedef struct GNode {
    char name;
    struct GNode **kids;   /* array of borrowed pointers, kids_len long */
    size_t kids_len;
} GNode;
```

`kids` and its pointers are **owned by the node**; a node may be a child
of several parents (shared, borrowed from the parents' view). Implement:

```c
/* frees every distinct node reachable from root exactly once, then the
   kids arrays, then returns how many nodes were freed */
size_t graph_free(GNode *root);
```""",
            C_PRELUDE + "\n#include <stddef.h>\ntypedef struct GNode {\n    char name;\n    struct GNode **kids;\n    size_t kids_len;\n} GNode;\nsize_t graph_free(GNode *root);\n",
            [
                (
                    "shared children, single free",
                    r"""
GNode *leaf1 = malloc(sizeof(GNode)); leaf1->name='x'; leaf1->kids=NULL; leaf1->kids_len=0;
GNode *leaf2 = malloc(sizeof(GNode)); leaf2->name='y'; leaf2->kids=NULL; leaf2->kids_len=0;
GNode **k1 = malloc(2 * sizeof(GNode*)); k1[0]=leaf1; k1[1]=leaf2;
GNode *mid = malloc(sizeof(GNode)); mid->name='m'; mid->kids=k1; mid->kids_len=2;
GNode **k2 = malloc(2 * sizeof(GNode*)); k2[0]=leaf1; k2[1]=mid;
GNode *root = malloc(sizeof(GNode)); root->name='r'; root->kids=k2; root->kids_len=2;
/* leaf1 is shared by mid and root: freed exactly once */
CHECK_EQ(graph_free(root), 4);
""",
                    "Mark-and-sweep with a 'freed' flag or collect-then-free. Never free a reachable node twice.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p5-opaque-counter": vi_challenge(
            "Xây opaque handle",
            "Cài MCounter đếm nhiều khóa; NULL-tolerant; mc_destroy(NULL) là no-op.",
            [("kỷ luật API", "mảng cố định {char key[16]; int count;} là đủ.")],
        ),
        "cint-p5-graph-free": vi_challenge(
            "Free đồ thị đúng một lần",
            "Cài graph_free: free mỗi node phân biệt đúng một lần, trả số node đã free.",
            [("con chia sẻ, free một lần", "đánh dấu freed hoặc gom rồi free.")],
        ),
    },
    solutions=[
        (
            "cint-p5-opaque-counter",
            r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#define MC_MAX 32
struct MCounter { char key[MC_MAX][16]; int count[MC_MAX]; size_t n; };
MCounter *mc_create(void) {
    return calloc(1, sizeof(MCounter));
}
int mc_bump(MCounter *m, const char *key, int by) {
    if (!m || !key) return -1;
    for (size_t i = 0; i < m->n; i++)
        if (strcmp(m->key[i], key) == 0) { m->count[i] += by; return 0; }
    if (m->n == MC_MAX || strlen(key) >= 16) return -1;
    snprintf(m->key[m->n], 16, "%s", key);
    m->count[m->n] = by;
    m->n++;
    return 0;
}
int mc_get(const MCounter *m, const char *key) {
    if (!m || !key) return 0;
    for (size_t i = 0; i < m->n; i++)
        if (strcmp(m->key[i], key) == 0) return m->count[i];
    return 0;
}
size_t mc_keys(const MCounter *m) { return m ? m->n : 0; }
void mc_destroy(MCounter *m) { free(m); }""",
            r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#define MC_MAX 32
struct MCounter { char key[MC_MAX][16]; int count[MC_MAX]; size_t n; };
MCounter *mc_create(void) { return calloc(1, sizeof(MCounter)); }
int mc_bump(MCounter *m, const char *key, int by) {
    if (!m || !key) return -1;
    for (size_t i = 0; i < m->n; i++)
        if (strcmp(m->key[i], key) == 0) { m->count[i] = by; return 0; }  /* wrong: replaces instead of accumulating */
    if (m->n == MC_MAX || strlen(key) >= 16) return -1;
    snprintf(m->key[m->n], 16, "%s", key);
    m->count[m->n] = by;
    m->n++;
    return 0;
}
int mc_get(const MCounter *m, const char *key) {
    if (!m || !key) return 1;    /* wrong: returns 1 instead of 0 for missing/NULL */
    for (size_t i = 0; i < m->n; i++)
        if (strcmp(m->key[i], key) == 0) return m->count[i];
    return 0;
}
size_t mc_keys(const MCounter *m) { return m ? m->n + 1 : 0; }  /* wrong: off-by-one */
void mc_destroy(MCounter *m) { if (m) m->n = 0; }  /* wrong: never frees */
""",
        ),
        (
            "cint-p5-graph-free",
            r"""
#include <stdlib.h>
#include <stddef.h>
static size_t sweep(GNode *n) {
    if (!n || n->name == '\0') return 0;   /* '\0' marks freed */
    n->name = '\0';
    size_t count = 1;
    for (size_t i = 0; i < n->kids_len; i++) count += sweep(n->kids[i]);
    free(n->kids);
    free(n);
    return count;
}
size_t graph_free(GNode *root) { return sweep(root); }""",
            r"""
#include <stdlib.h>
#include <stddef.h>
size_t graph_free(GNode *root) {
    if (!root) return 0;
    size_t count = 0;
    for (size_t i = 0; i < root->kids_len; i++) {
        count += graph_free(root->kids[i]);   /* wrong: shared nodes freed multiple times */
    }
    free(root->kids);
    free(root);
    return count + 1;
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint


CP_CH = challenge(
    "cint-checkpoint-m5-task",
    "Bounded String Queue",
    """Implement the declared BQueue API exactly to contract: FIFO, copies
owned by the queue, -1 on full/empty/bad args, NULL-tolerant, fixed cap 8,
strings up to 31 chars.""",
    C_PRELUDE + "\n#include <stddef.h>\ntypedef struct BQueue BQueue;\nBQueue *bq_create(void);\nint bq_push(BQueue *q, const char *s);\nint bq_pop(BQueue *q, char *out);\nsize_t bq_len(const BQueue *q);\nsize_t bq_capacity(const BQueue *q);\nvoid bq_destroy(BQueue *q);\n",
    [
        (
            "fifo under contract",
            r"""
BQueue *q = bq_create();
CHECK(q != NULL);
CHECK_EQ(bq_len(q), 0);
CHECK_EQ(bq_capacity(q), 8);
char out[32];
CHECK_EQ(bq_pop(q, out), -1);
CHECK_EQ(bq_push(q, "first"), 0);
CHECK_EQ(bq_push(q, "second"), 0);
CHECK_EQ(bq_push(q, "third"), 0);
CHECK_EQ(bq_len(q), 3);
CHECK_EQ(bq_pop(q, out), 0); CHECK(!strcmp(out, "first"));
CHECK_EQ(bq_pop(q, out), 0); CHECK(!strcmp(out, "second"));
CHECK_EQ(bq_push(q, "fourth"), 0);
CHECK_EQ(bq_pop(q, out), 0); CHECK(!strcmp(out, "third"));
CHECK_EQ(bq_pop(q, out), 0); CHECK(!strcmp(out, "fourth"));
CHECK_EQ(bq_pop(q, out), -1);
for (int i = 0; i < 8; i++) CHECK_EQ(bq_push(q, "x"), 0);
CHECK_EQ(bq_push(q, "overflow"), -1);
CHECK_EQ(bq_push(NULL, "x"), -1);
CHECK_EQ(bq_push(q, NULL), -1);
CHECK_EQ(bq_pop(NULL, out), -1);
bq_destroy(q);
bq_destroy(NULL);
""",
            "A ring buffer (head, count) over a fixed char[8][32] store passes everything with no malloc at all.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Hàng đợi string có giới hạn",
        "Cài BQueue: push/pop FIFO, đầy -> -1, NULL-tolerant, destroy no-op với NULL.",
        [("fifo", "ring buffer (head, count) trên char[8][32] là đủ, không cần malloc.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m5",
    "Checkpoint: Modeling Under Contract",
    "Prove you can model with structs, enforce invariants through an API, and document ownership.",
    22,
    r"""
## The task

Implement the declared `BQueue` API (see the challenge) exactly to
contract: FIFO order, the queue owns copies of its strings, `-1` on
full/empty/bad args, NULL-tolerant, fixed capacity 8, strings up to 31
characters.

Passing this proves: struct modeling with invariants enforced behind an
opaque handle, ring-buffer index arithmetic, and the discipline of
return-code contracts.

Next module: strings as data — buffers, boundaries, and parsing.
""",
    "Kiểm tra: Mô hình hóa dưới hợp đồng",
    "Chứng minh bạn mô hình hóa bằng struct, giữ bất biến qua API, và ghi rõ ownership.",
    r"""
## Bài toán

Cài API `BQueue` đã khai báo (xem challenge) đúng hợp đồng: thứ tự FIFO,
queue sở hữu bản sao chuỗi của mình, `-1` khi đầy/rỗng/sai tham số,
chấp nhận NULL, capacity cố định 8, chuỗi tối đa 31 ký tự.

Vượt qua có nghĩa là bạn chứng minh: mô hình hóa struct với bất biến được
bảo vệ sau opaque handle, số học chỉ số ring-buffer, và kỷ luật hợp đồng
return-code.

Module sau: chuỗi như dữ liệu — buffer, biên, và parsing.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <string.h>
#include <stddef.h>
struct BQueue { char slot[8][32]; size_t head, count; };
BQueue *bq_create(void) { return calloc(1, sizeof(BQueue)); }
int bq_push(BQueue *q, const char *s) {
    if (!q || !s || strlen(s) >= 32 || q->count == 8) return -1;
    size_t tail = (q->head + q->count) % 8;
    snprintf(q->slot[tail], 32, "%s", s);
    q->count++;
    return 0;
}
int bq_pop(BQueue *q, char *out) {
    if (!q || !out || q->count == 0) return -1;
    snprintf(out, 32, "%s", q->slot[q->head]);
    q->head = (q->head + 1) % 8;
    q->count--;
    return 0;
}
size_t bq_len(const BQueue *q) { return q ? q->count : 0; }
size_t bq_capacity(const BQueue *q) { (void)q; return 8; }
void bq_destroy(BQueue *q) { free(q); }""",
    wrong=r"""
#include <string.h>
#include <stddef.h>
struct BQueue { char slot[8][32]; size_t head, count; };
BQueue *bq_create(void) { return calloc(1, sizeof(BQueue)); }
int bq_push(BQueue *q, const char *s) {
    if (!q || !s || strlen(s) >= 32 || q->count == 8) return -1;
    snprintf(q->slot[q->count], 32, "%s", s);   /* wrong: fills from 0, ignores head */
    q->count++;
    return 0;
}
int bq_pop(BQueue *q, char *out) {
    if (!q || !out || q->count == 0) return -1;
    snprintf(out, 32, "%s", q->slot[0]);        /* wrong: always slot 0, no ring advance */
    for (size_t i = 1; i < q->count; i++)
        snprintf(q->slot[i - 1], 32, "%s", q->slot[i]);  /* wrong: still wrong after full+wrap */
    q->count--;
    return 0;
}
size_t bq_len(const BQueue *q) { return q ? q->count : 1; }  /* wrong: empty returns 1 */
size_t bq_capacity(const BQueue *q) { (void)q; return 8; }
void bq_destroy(BQueue *q) { free(q); }""",
)

print("module 5 complete")
