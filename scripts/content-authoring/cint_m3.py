#!/usr/bin/env python3
"""C — Intermediate — Module 3: cint-ownership.

Memory ownership as the organizing discipline: allocation-failure contracts,
the realloc idiom, leak/UAF/double-free as contract violations, and the
ownership questions every API must answer. No sanitizers in this sandbox —
the "wrong" solutions encode real, deterministic violations (NULL derefs,
logic leaks observable via behavior, not tools).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-ownership"

write_module(
    M,
    "Ownership & the Heap",
    "Who owns this memory? Allocation-failure contracts, the realloc growth idiom, "
    "and the three classic lifetime violations as API-design failures.",
    "Quyền sở hữu & heap",
    "Ai sở hữu bộ nhớ này? Hợp đồng thất bại cấp phát, mẫu idiom realloc, và ba lỗi "
    "thời gian sống kinh điển như thất bại thiết kế API.",
    lessons=["ownership-contracts", "realloc-growth", "lifetime-violations", "cint-checkpoint-m3"],
    practices=["cint-p3-alloc", "cint-p3-ownership"],
)
print("module json done")

write_lesson(
    M, "ownership-contracts",
    "Who Owns This Memory?",
    "The four ownership questions, allocation-failure handling, and signatures that document the deal.",
    16,
    r"""
## The four questions

Every heap pointer in a C program must have answers to:

1. **Who owns it?** (Who is responsible for freeing it?)
2. **How long does it live?** (Until the owner frees it — or forever?)
3. **Who may write it?** (Single owner, or shared?)
4. **What happens if allocation fails?** (Return NULL? Abort? Retry?)

C does not answer these for you. The API design does — in signatures, docs,
and naming.

## Failure is a contract

```c
/* Contract: returns a heap buffer the caller must free, or NULL on failure.
   The two outcomes are the whole contract; neither may be ignored. */
char *greeting(const char *name);
```

Beginner code often pretends `malloc` never fails. Intermediate code handles
it, because **the sandbox caps memory** and long-running systems fragment:

```c
char *copy = strdup(name);        /* may return NULL */
if (!copy) return 0;              /* propagate, don't dereference */
```

Every allocation site needs a failure path, and every function that can fail
needs a documented way to say so. The out-parameter pattern from Module 2
pairs naturally: `int make(int n, T **out)` — return the status, write the
pointer only on success.

## NULL after free, and the ownership transfer

```c
free(p);
p = NULL;      /* now accidental reuse is a harmless no-op */
```

Setting the pointer to NULL after free converts the nastiest bug class
(use-after-free) into a benign one for that variable. It is cheap insurance
wherever the variable outlives the free.

Ownership **transfer**: a function like `takeover(char *s)` that stores or
frees its argument now *owns* it — the caller must not free it again.
Document every transfer; ownership confusion is the root of double-free.

## The ownership ladder in signatures

| Signature | Deal |
|---|---|
| `size_t len(const char *s)` | borrows; does not keep or free |
| `int dup_str(const char *s, char **out)` | creates new memory; caller owns |
| `void consume(char *s)` | takes ownership; caller must not reuse |
| `void store(struct Table *t, char *s)` | takes ownership into the table |

## Check your understanding

- Who frees the result of `strdup`? (The caller — it created fresh heap memory.)
- Is `free(p); free(p);` valid? (No — double free is undefined behavior.)
- After `free(p); p = NULL;` what does `free(p)` do? (Nothing — free(NULL)
  is a documented no-op.)
""",
    "Ai sở hữu bộ nhớ này?",
    "Bốn câu hỏi sở hữu, xử lý thất bại cấp phát, và chữ ký ghi rõ thỏa thuận.",
r"""
## Bốn câu hỏi

Mọi con trỏ heap trong chương trình C phải có lời giải cho:

1. **Ai sở hữu nó?** (Ai chịu trách nhiệm free?)
2. **Sống bao lâu?** (Cho đến khi owner free — hay mãi mãi?)
3. **Ai được ghi?** (Một owner, hay chia sẻ?)
4. **Thất bại cấp phát thì sao?** (Trả NULL? Dừng? Thử lại?)

C không trả lời giúp bạn. Thiết kế API trả lời — qua chữ ký, tài liệu, và
cách đặt tên.

## Thất bại là một hợp đồng

```c
/* Hợp đồng: trả về buffer heap mà caller phải free, hoặc NULL khi thất bại.
   Hai kết cục là toàn bộ hợp đồng; không được bỏ qua cái nào. */
char *greeting(const char *name);
```

Code sơ cấp thường giả định `malloc` không bao giờ thất bại. Code trung cấp xử
lý nó, vì **sandbox giới hạn bộ nhớ** và hệ thống chạy lâu bị phân mảnh:

```c
char *copy = strdup(name);        /* có thể trả NULL */
if (!copy) return 0;              /* truyền lên, đừng dereference */
```

Mỗi chỗ cấp phát cần một nhánh thất bại, và mỗi hàm có thể thất bại cần một
cách được ghi chú để báo điều đó. Mẫu out-parameter của Module 2 ghép tự
nhiên: `int make(int n, T **out)` — trả trạng thái, chỉ ghi con trỏ khi thành công.

## NULL sau free, và chuyển giao sở hữu

```c
free(p);
p = NULL;      /* giờ tái sử dụng vô tình là no-op vô hại */
```

Đặt con trỏ về NULL sau free biến lớp bug khó chịu nhất (use-after-free)
thành lành tính cho biến đó. Bảo hiểm rẻ ở mọi nơi biến sống lâu hơn lời free.

**Chuyển giao** sở hữu: hàm như `takeover(char *s)` lưu hoặc free tham số thì
*từ giờ sở hữu* nó — caller không được free thêm lần nữa. Ghi chú mọi chuyển
giao; nhầm lẫn sở hữu là gốc của double-free.

## Bậc thang sở hữu trong chữ ký

| Chữ ký | Thỏa thuận |
|---|---|
| `size_t len(const char *s)` | mượn; không giữ, không free |
| `int dup_str(const char *s, char **out)` | tạo bộ nhớ mới; caller sở hữu |
| `void consume(char *s)` | nhận sở hữu; caller không được dùng lại |
| `void store(struct Table *t, char *s)` | nhận sở hữu vào trong bảng |

## Kiểm tra hiểu biết

- Ai free kết quả của `strdup`? (Caller — nó tạo bộ nhớ heap mới.)
- `free(p); free(p);` có hợp lệ? (Không — double free là undefined behavior.)
- Sau `free(p); p = NULL;` thì `free(p)` làm gì? (Không gì cả — free(NULL)
  là no-op được chuẩn ghi rõ.)
"""
)

write_lesson(
    M, "realloc-growth",
    "Growing Buffers: The realloc Idiom",
    "Why temp = realloc(p, n) is the only safe shape, amortized doubling, and shrinking correctly.",
    15,
    r"""
## The trap `realloc` sets

`realloc(p, new_size)` may: extend in place, move the block (copying contents,
freeing the old), or fail — **returning NULL and leaving the original block
valid**. That last case is the trap:

```c
p = realloc(p, n * 2);      /* BUG: on failure the old block leaks —
                               p no longer points at it */
```

The safe idiom keeps the old pointer until success is confirmed:

```c
void *tmp = realloc(p, n * 2);
if (!tmp) {
    /* p is still valid: recover, retry with smaller growth, or fail cleanly */
    return 0;
}
p = tmp;
```

## The standard growth loop

```c
typedef struct {
    int *data;
    size_t len, cap;
} Vec;

int vec_push(Vec *v, int value) {
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 8;      /* amortized doubling */
        if (ncap < v->cap) return 0;                 /* overflow guard */
        int *nd = realloc(v->data, ncap * sizeof *nd);
        if (!nd) return 0;
        v->data = nd;
        v->cap = ncap;
    }
    v->data[v->len++] = value;
    return 1;
}
```

**Amortized doubling** is why dynamic arrays are "O(1) push": most pushes
write one slot; every doubling copies, but copies become geometrically rarer.
Total copy work across n pushes is O(n).

## Shrinking and emptying

```c
/* shrink: realloc to a smaller size cannot fail in practice, but the
   idiom does not hurt */
void *tmp = realloc(v->data, v->len * sizeof *v->data);
if (tmp) v->data = tmp;
v->cap = v->len;

/* the capacity invariant: len <= cap, always */
```

`free` a NULL member is fine (`free(v->data)` when data == NULL is a no-op),
so a "destroy" function needs no special empty case:

```c
void vec_destroy(Vec *v) {
    free(v->data);      /* free(NULL) is fine */
    v->data = NULL;
    v->len = v->cap = 0;
}
```

## Check your understanding

- Why does the naive `p = realloc(p, n)` leak? (On failure, the old block's
  only pointer is overwritten.)
- Why double rather than grow by a fixed 10? (Fixed growth makes n pushes
  O(n²) copies; doubling is O(n).)
""",
    "Phóng lớn buffer: idiom realloc",
    "Vì sao tmp = realloc(p, n) là hình dạng an toàn duy nhất, nhân đôi khấu hao, và thu nhỏ đúng cách.",
r"""
## Cái bẫy `realloc` cài sẵn

`realloc(p, new_size)` có thể: mở rộng tại chỗ, dời khối (copy nội dung, free
khối cũ), hoặc thất bại — **trả NULL nhưng khối cũ vẫn hợp lệ**. Trường hợp
cuối chính là cái bẫy:

```c
p = realloc(p, n * 2);      /* BUG: khi thất bại, khối cũ bị rò rỉ —
                               p không còn trỏ tới nó */
```

Idiom an toàn giữ con trỏ cũ đến khi xác nhận thành công:

```c
void *tmp = realloc(p, n * 2);
if (!tmp) {
    /* p vẫn hợp lệ: phục hồi, thử lại với mức tăng nhỏ hơn, hoặc thất bại sạch */
    return 0;
}
p = tmp;
```

## Vòng lặp tăng trưởng chuẩn

```c
typedef struct {
    int *data;
    size_t len, cap;
} Vec;

int vec_push(Vec *v, int value) {
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 8;      /* nhân đôi khấu hao */
        if (ncap < v->cap) return 0;                 /* chặn tràn số */
        int *nd = realloc(v->data, ncap * sizeof *nd);
        if (!nd) return 0;
        v->data = nd;
        v->cap = ncap;
    }
    v->data[v->len++] = value;
    return 1;
}
```

**Nhân đôi khấu hao** là lý do mảng động được coi là "push O(1)": phần lớn
lần push chỉ ghi một ô; mỗi lần nhân đôi có copy, nhưng copy trở nên thưa theo
cấp số nhân. Tổng công copy qua n lần push là O(n).

## Thu nhỏ và làm rỗng

```c
/* thu nhỏ: realloc xuống kích thước nhỏ hơn về thực tế không thất bại,
   nhưng idiom này không hại */
void *tmp = realloc(v->data, v->len * sizeof *v->data);
if (tmp) v->data = tmp;
v->cap = v->len;

/* bất biến dung lượng: len <= cap, luôn luôn */
```

`free` một thành viên NULL là hợp lệ (`free(v->data)` khi data == NULL là
no-op), nên hàm "destroy" không cần trường hợp rỗng đặc biệt:

```c
void vec_destroy(Vec *v) {
    free(v->data);      /* free(NULL) không sao */
    v->data = NULL;
    v->len = v->cap = 0;
}
```

## Kiểm tra hiểu biết

- Vì sao `p = realloc(p, n)` ngây thơ lại rò rỉ? (Khi thất bại, con trỏ duy
  nhất đến khối cũ bị ghi đè.)
- Vì sao nhân đôi thay vì tăng cố định 10? (Tăng cố định làm n lần push tốn
  O(n²) phép copy; nhân đôi chỉ O(n).)
"""
)

write_lesson(
    M, "lifetime-violations",
    "Leak, Use-After-Free, Double-Free — as Design Failures",
    "The three lifetime violations, why each happens architecturally, and the checklists that prevent them.",
    17,
    r"""
## Not random bad luck — broken ownership

The three classic violations are not "bugs that happen"; each is a specific
ownership question that went unanswered:

| Violation | Unanswered question |
|---|---|
| **Leak** | Who frees this? (Nobody was assigned.) |
| **Use-after-free** | How long does it live? (Someone used it after the answer expired.) |
| **Double-free** | Who owns it? (Two owners both did their duty.) |

## Leak: every path must land somewhere

A function that allocates and exits early (an error return, a loop break) must
still free. The shape that fails:

```c
int load(Config **out) {
    Config *c = malloc(sizeof *c);
    if (!parse(c)) return 0;        /* LEAK: c never freed on this path */
    *out = c;
    return 1;
}
```

The fixed shape frees on every failure path (or uses one exit):

```c
int load(Config **out) {
    Config *c = malloc(sizeof *c);
    if (!c) return 0;
    if (!parse(c)) { free(c); return 0; }   /* every path accounted for */
    *out = c;
    return 1;
}
```

**Rule: count your allocations, then count your frees on every path. They
must balance — except along the success path where ownership is handed off.**

## Use-after-free: the pointer outlived the agreement

```c
char *name = strdup("ada");
free(name);
printf("%s\\n", name);      /* UB: reading freed memory */
```

It reads *garbage or stale data* — no diagnostic, no trap, the worst kind of
bug. Prevention: NULL the pointer after free (Module lesson 1), and never let
a borrowed pointer outlive the borrow. Structures that store borrowed pointers
must document "not owned; do not free; invalid after owner frees."

## Double-free: two owners, one object

```c
void give_away(char *s) { log(s); free(s); }   /* takes ownership */
/* caller: */
give_away(name);
free(name);                /* DOUBLE FREE: caller forgot ownership moved */
```

APIs that take ownership should make it visible: naming (`consume`, `take`),
or by the callee NULLing the caller's handle when practical (`char **s`).

## The Intermediate checklist

Before calling any function that touches heap memory, answer:
1. Does this call allocate? Who frees?
2. Does this call take ownership? (Then stop using my copy.)
3. On this function's failure paths, what must be freed?

## Check your understanding

- `int save(FILE *f)` allocates a temp buffer, writes, returns early on write
  error. What is missing? (free of the temp on the error path.)
- A struct stores `char *name` it never frees and never writes. Who owns it?
  (The creator — the struct borrows; document that.)
""",
    "Rò rỉ, dùng-sau-free, free-hai-lần — như thất bại thiết kế",
    "Ba lỗi thời gian sống, vì sao mỗi lỗi xảy ra về mặt kiến trúc, và các checklist ngăn chúng.",
r"""
## Không phải rủi ro ngẫu nhiên — mà là sở hữu bị gãy

Ba lỗi kinh điển không phải "bug tình cờ"; mỗi lỗi là một câu hỏi sở hữu cụ thể
không được trả lời:

| Lỗi | Câu hỏi bị bỏ ngỏ |
|---|---|
| **Rò rỉ (leak)** | Ai free thứ này? (Chưa ai được giao.) |
| **Dùng-sau-free** | Nó sống bao lâu? (Có người dùng sau khi lời đáp hết hạn.) |
| **Free-hai-lần** | Ai sở hữu nó? (Hai owner cùng làm nghĩa vụ.) |

## Rò rỉ: mọi đường đi phải kết thúc ở đâu đó

Hàm cấp phát rồi thoát sớm (return lỗi, break vòng lặp) vẫn phải free. Hình
dạng thất bại:

```c
int load(Config **out) {
    Config *c = malloc(sizeof *c);
    if (!parse(c)) return 0;        /* RÒ RỈ: c không được free trên nhánh này */
    *out = c;
    return 1;
}
```

Hình dạng sửa được: free trên mọi nhánh thất bại (hoặc dùng một điểm thoát):

```c
int load(Config **out) {
    Config *c = malloc(sizeof *c);
    if (!c) return 0;
    if (!parse(c)) { free(c); return 0; }   /* mọi đường đều được tính */
    *out = c;
    return 1;
}
```

**Nguyên tắc: đếm các phép cấp phát, rồi đếm các phép free trên từng đường đi.
Chúng phải cân — trừ đường thành công nơi quyền sở hữu được bàn giao.**

## Dùng-sau-free: con trỏ sống lâu hơn thỏa thuận

```c
char *name = strdup("ada");
free(name);
printf("%s\\n", name);      /* UB: đọc bộ nhớ đã free */
```

Nó đọc *rác hoặc dữ liệu cũ* — không chẩn đoán, không bẫy, loại bug khó chịu
nhất. Phòng tránh: gán NULL sau free (bài 1 của module), và không bao giờ để
con trỏ mượn sống lâu hơn lần mượn. Cấu trúc lưu con trỏ mượn phải ghi chú
"không sở hữu; không free; vô hiệu sau khi owner free."

## Free-hai-lần: hai owner, một đối tượng

```c
void give_away(char *s) { log(s); free(s); }   /* nhận sở hữu */
/* caller: */
give_away(name);
free(name);                /* FREE HAI LẦN: caller quên rằng sở hữu đã chuyển */
```

API nhận sở hữu nên làm điều đó thấy được: đặt tên (`consume`, `take`), hoặc
callee gán NULL vào handle của caller khi khả thi (`char **s`).

## Checklist Trung cấp

Trước khi gọi hàm nào chạm vào bộ nhớ heap, hãy trả lời:
1. Lời gọi này có cấp phát không? Ai free?
2. Lời gọi này có nhận sở hữu không? (Thì ngừng dùng bản sao của tôi.)
3. Trên các nhánh thất bại của hàm này, cái gì phải được free?

## Kiểm tra hiểu biết

- `int save(FILE *f)` cấp phát buffer tạm, ghi, trả sớm khi lỗi ghi. Thiếu gì?
  (Free buffer tạm trên nhánh lỗi.)
- Một struct lưu `char *name` mà không bao giờ free và không bao giờ ghi. Ai
  sở hữu? (Người tạo ra — struct mượn; hãy ghi chú điều đó.)
"""
)

# ---------------------------------------------------------------- practice 3a
P3A_CH = [
    challenge(
        "cint-p3-safe-dup",
        "Allocation Failure Contracts",
        """Implement the documented-contract pair:

```c
/* duplicates s into fresh heap memory; sets *out and returns 1 on success.
   Returns 0 WITHOUT touching *out on: NULL s, NULL out, or allocation
   failure. */
int safe_dup(const char *s, char **out);
/* joins two strings into fresh memory "a/b" (separator always present);
   same contract as safe_dup. */
int path_join(const char *a, const char *b, char **out);
```""",
        C_PRELUDE,
        [
            (
                "success path",
                r"""
char *s = NULL;
CHECK_EQ(safe_dup("abc", &s), 1);
CHECK_STR_EQ(s, "abc");
CHECK_EQ(safe_dup("", &s), 1);
CHECK_STR_EQ(s, "");
free(s);
CHECK_EQ(path_join("usr", "bin", &s), 1);
CHECK_STR_EQ(s, "usr/bin");
free(s);
""",
                "malloc(len+1), memcpy, NUL-terminate; path_join allocates la+lb+2.",
            ),
            (
                "failure paths leave *out untouched",
                r"""
char *keep = (char *)0x1;   /* sentinel: must remain unchanged */
CHECK_EQ(safe_dup(NULL, &keep), 0);
CHECK(keep == (char *)0x1);
CHECK_EQ(safe_dup("x", NULL), 0);
char *s2 = NULL;
CHECK_EQ(safe_dup("x", &s2), 1);
free(s2);
CHECK_EQ(path_join(NULL, "b", &s2), 0);
CHECK_EQ(path_join("a", NULL, &s2), 0);
""",
                "Validate arguments BEFORE any allocation; never write *out on failure.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p3-vec-grow",
        "The Vec Push Loop",
        """Implement a growable int vector with the exact realloc discipline:

```c
typedef struct { int *data; size_t len, cap; } Vec;   /* in boilerplate */
void vec_init(Vec *v);
int vec_push(Vec *v, int value);   /* 0 on allocation failure; v unchanged then */
size_t vec_len(const Vec *v);
int vec_get(const Vec *v, size_t i, int *out);  /* bounds-checked; 0 if out of range */
void vec_destroy(Vec *v);          /* frees and zeroes the struct */
```""",
        C_PRELUDE + "\ntypedef struct { int *data; size_t len, cap; } Vec;\n",
        [
            (
                "grow and read back",
                r"""
Vec v;
vec_init(&v);
for (int i = 0; i < 100; i++) CHECK_EQ(vec_push(&v, i * i), 1);
CHECK_EQ(vec_len(&v), 100);
int val = -1;
CHECK_EQ(vec_get(&v, 0, &val), 1); CHECK_EQ(val, 0);
CHECK_EQ(vec_get(&v, 99, &val), 1); CHECK_EQ(val, 9801);
CHECK_EQ(vec_get(&v, 100, &val), 0);
vec_destroy(&v);
CHECK_NULL(v.data);
CHECK_EQ(vec_len(&v), 0);
""",
                "Start cap 8; double when full; realloc into a temp first.",
            ),
            (
                "empty and boundary",
                r"""
Vec v;
vec_init(&v);
CHECK_EQ(vec_len(&v), 0);
int val;
CHECK_EQ(vec_get(&v, 0, &val), 0);
CHECK_EQ(vec_push(&v, 42), 1);
CHECK_EQ(vec_get(&v, 0, &val), 1); CHECK_EQ(val, 42);
vec_destroy(&v);
vec_destroy(&v);   /* double destroy must be safe */
CHECK_NULL(v.data);
""",
                "After destroy, data == NULL so free(NULL) makes re-destroy a no-op.",
            ),
        ],
        level="mini-build",
    ),
    challenge(
        "cint-p3-balanced-paths",
        "Every Path Frees",
        """Implement a function with MULTIPLE allocation and failure paths where
every path balances:

```c
/* builds "N=x;D=y" from two ints using two temp buffers; on any failure
   returns 0 with *out untouched; on success returns 1, caller frees *out. */
int format_stats(int n, double d, char **out);
```

Use snprintf into a heap buffer per half, then join. The point of the exercise:
if the second allocation fails, the first must be freed.""",
        C_PRELUDE,
        [
            (
                "success and failure balance",
                r"""
char *s = NULL;
CHECK_EQ(format_stats(7, 0.5, &s), 1);
CHECK_STR_EQ(s, "N=7;D=0.5");
free(s);
CHECK_EQ(format_stats(7, 0.5, NULL), 0);
""",
                "Build two halves with malloc+snprintf; on any failure free what you hold and return 0.",
            ),
        ],
        level="guided",
    ),
    challenge(
        "cint-p3-owning-table",
        "A Table That Takes Ownership",
        """Implement a string table that OWNS its entries:

```c
typedef struct { char **items; size_t len, cap; } OwnedTable;  /* in boilerplate */
void ot_init(OwnedTable *t);
/* copies s into fresh memory and stores it. 0 on failure (t unchanged). */
int ot_add(OwnedTable *t, const char *s);
/* number of entries currently stored */
size_t ot_len(const OwnedTable *t);
/* frees every string AND the array; zeroes the struct */
void ot_destroy(OwnedTable *t);
/* removes the last entry, frees it, returns 1; 0 if empty */
int ot_pop(OwnedTable *t);
```""",
        C_PRELUDE + "\ntypedef struct { char **items; size_t len, cap; } OwnedTable;\n",
        [
            (
                "ownership through the table lifecycle",
                r"""
OwnedTable t;
ot_init(&t);
CHECK_EQ(ot_add(&t, "alpha"), 1);
CHECK_EQ(ot_add(&t, "beta"), 1);
CHECK_EQ(ot_len(&t), 2);
CHECK_EQ(ot_pop(&t), 1);
CHECK_EQ(ot_len(&t), 1);
CHECK_EQ(ot_pop(&t), 1);
CHECK_EQ(ot_pop(&t), 0);   /* empty now */
ot_destroy(&t);
CHECK_NULL(t.items);
""",
                "Growth identical to Vec but for char*; pop frees the string slot.",
            ),
        ],
        level="mini-build",
    ),
]
P3A_SOL = [
    (
        "cint-p3-safe-dup",
        r"""
int safe_dup(const char *s, char **out) {
    if (!s || !out) return 0;
    size_t n = strlen(s);
    char *b = malloc(n + 1);
    if (!b) return 0;
    memcpy(b, s, n + 1);
    *out = b;
    return 1;
}
int path_join(const char *a, const char *b, char **out) {
    if (!a || !b || !out) return 0;
    size_t la = strlen(a), lb = strlen(b);
    char *buf = malloc(la + lb + 2);
    if (!buf) return 0;
    memcpy(buf, a, la);
    buf[la] = '/';
    memcpy(buf + la + 1, b, lb + 1);
    *out = buf;
    return 1;
}""",
        r"""
int safe_dup(const char *s, char **out) {
    if (!out) return 0;
    *out = NULL;           /* wrong: writes *out even when returning 0 */
    if (!s) return 0;
    size_t n = strlen(s);
    char *b = malloc(n + 1);
    if (!b) return 0;
    memcpy(b, s, n + 1);
    *out = b;
    return 1;
}
int path_join(const char *a, const char *b, char **out) {
    if (!a || !b || !out) return 0;
    size_t la = strlen(a), lb = strlen(b);
    char *buf = malloc(la + lb + 2);
    if (!buf) return 0;
    memcpy(buf, a, la);
    buf[la] = '/';
    memcpy(buf + la + 1, b, lb + 1);
    *out = buf;
    return 1;
}""",
    ),
    (
        "cint-p3-vec-grow",
        r"""
void vec_init(Vec *v) {
    if (!v) return;
    v->data = NULL;
    v->len = 0;
    v->cap = 0;
}
int vec_push(Vec *v, int value) {
    if (!v) return 0;
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 8;
        int *nd = realloc(v->data, ncap * sizeof *nd);
        if (!nd) return 0;
        v->data = nd;
        v->cap = ncap;
    }
    v->data[v->len++] = value;
    return 1;
}
size_t vec_len(const Vec *v) { return v ? v->len : 0; }
int vec_get(const Vec *v, size_t i, int *out) {
    if (!v || !out || i >= v->len) return 0;
    *out = v->data[i];
    return 1;
}
void vec_destroy(Vec *v) {
    if (!v) return;
    free(v->data);
    v->data = NULL;
    v->len = v->cap = 0;
}""",
        r"""
void vec_init(Vec *v) {
    if (!v) return;
    v->data = NULL;
    v->len = 0;
    v->cap = 0;
}
int vec_push(Vec *v, int value) {
    if (!v) return 0;
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 8;
        v->data = realloc(v->data, ncap * sizeof *nd_wrong);   /* wrong: direct assign leaks on failure */
        if (!v->data) return 0;
        v->cap = ncap;
    }
    v->data[v->len++] = value;
    return 1;
}
size_t vec_len(const Vec *v) { return v ? v->len : 0; }
int vec_get(const Vec *v, size_t i, int *out) {
    if (!v || !out || i >= v->len) return 0;
    *out = v->data[i];
    return 1;
}
void vec_destroy(Vec *v) {
    if (!v) return;
    free(v->data);
    v->data = NULL;
    v->len = v->cap = 0;
}""",
    ),
    (
        "cint-p3-balanced-paths",
        r"""
int format_stats(int n, double d, char **out) {
    if (!out) return 0;
    char *first = malloc(64);
    if (!first) return 0;
    char *second = malloc(64);
    if (!second) { free(first); return 0; }    /* the balancing act */
    int n1 = snprintf(first, 64, "N=%d;", n);
    int n2 = snprintf(second, 64, "D=%g", d);
    if (n1 < 0 || n2 < 0 || (size_t)n1 >= 64 || (size_t)n2 >= 64) {
        free(first);
        free(second);
        return 0;
    }
    char *joined = malloc((size_t)n1 + (size_t)n2 + 1);
    if (!joined) { free(first); free(second); return 0; }
    memcpy(joined, first, (size_t)n1);
    memcpy(joined + n1, second, (size_t)n2 + 1);
    free(first);
    free(second);
    *out = joined;
    return 1;
}""",
        r"""
int format_stats(int n, double d, char **out) {
    if (!out) return 0;
    char *first = malloc(64);
    if (!first) return 0;
    char *second = malloc(64);
    if (!second) return 0;   /* wrong: first leaks on this path */
    int n1 = snprintf(first, 64, "N=%d ", n);   /* wrong: no semicolon */
    int n2 = snprintf(second, 64, "D=%g", d);
    if (n1 < 0 || n2 < 0) {
        free(first);
        free(second);
        return 0;
    }
    char *joined = malloc((size_t)n1 + (size_t)n2 + 1);
    if (!joined) { free(first); free(second); return 0; }
    memcpy(joined, first, (size_t)n1);
    memcpy(joined + n1, second, (size_t)n2 + 1);
    free(first);
    free(second);
    *out = joined;
    return 1;
}""",
    ),
    (
        "cint-p3-owning-table",
        r"""
void ot_init(OwnedTable *t) {
    if (!t) return;
    t->items = NULL;
    t->len = 0;
    t->cap = 0;
}
int ot_add(OwnedTable *t, const char *s) {
    if (!t || !s) return 0;
    if (t->len == t->cap) {
        size_t ncap = t->cap ? t->cap * 2 : 8;
        char **ni = realloc(t->items, ncap * sizeof *ni);
        if (!ni) return 0;
        t->items = ni;
        t->cap = ncap;
    }
    size_t n = strlen(s);
    char *copy = malloc(n + 1);
    if (!copy) return 0;
    memcpy(copy, s, n + 1);
    t->items[t->len++] = copy;
    return 1;
}
size_t ot_len(const OwnedTable *t) { return t ? t->len : 0; }
void ot_destroy(OwnedTable *t) {
    if (!t) return;
    for (size_t i = 0; i < t->len; i++) free(t->items[i]);
    free(t->items);
    t->items = NULL;
    t->len = t->cap = 0;
}
int ot_pop(OwnedTable *t) {
    if (!t || t->len == 0) return 0;
    free(t->items[--t->len]);
    return 1;
}""",
        r"""
void ot_init(OwnedTable *t) {
    if (!t) return;
    t->items = NULL;
    t->len = 0;
    t->cap = 0;
}
int ot_add(OwnedTable *t, const char *s) {
    if (!t || !s) return 0;
    if (t->len == t->cap) {
        size_t ncap = t->cap ? t->cap * 2 : 8;
        char **ni = realloc(t->items, ncap * sizeof *ni);
        if (!ni) return 0;
        t->items = ni;
        t->cap = ncap;
    }
    t->items[t->len++] = (char *)s;   /* wrong: stores the borrowed pointer —
                                         destroy will free caller memory */
    return 1;
}
size_t ot_len(const OwnedTable *t) { return t ? t->len : 0; }
void ot_destroy(OwnedTable *t) {
    if (!t) return;
    for (size_t i = 0; i < t->len; i++) free(t->items[i]);
    free(t->items);
    t->items = NULL;
    t->len = t->cap = 0;
}
int ot_pop(OwnedTable *t) {
    if (!t || t->len == 0) return 0;
    free(t->items[--t->len]);
    return 1;
}""",
    ),
]
write_practice(
    M, "cint-p3-alloc",
    "Failure-Path Gym",
    "Contracts, growth, and the balancing act of multi-allocation functions.",
    "Phòng gym đường thất bại",
    "Hợp đồng, tăng trưởng, và trò cân bằng của hàm đa-cấp-phát.",
    after_lesson="ownership-contracts",
    minutes=26,
    difficulty="intermediate",
    challenges=P3A_CH,
    vi_challenges={
        "cint-p3-safe-dup": vi_challenge(
            "Hợp đồng thất bại cấp phát",
            "Cài `safe_dup` và `path_join`: trả 1 + đặt *out khi thành công; trả 0 KHÔNG đụng *out khi thất bại.",
            [("đường thành công", "malloc(len+1), memcpy, kết thúc NUL; path_join cấp phát la+lb+2."),
             ("đường thất bại giữ *out nguyên", "Kiểm tra tham số TRƯỚC khi cấp phát; không bao giờ ghi *out khi thất bại.")],
        ),
        "cint-p3-vec-grow": vi_challenge(
            "Vòng lặp push của Vec",
            "Cài Vec đúng kỷ luật realloc: temp trước, gán sau; hủy an toàn hai lần.",
            [("tăng và đọc lại", "Cap đầu 8; nhân đôi khi đầy; realloc vào biến tạm trước."),
             ("rỗng và biên", "Sau destroy, data == NULL nên free(NULL) làm re-destroy thành no-op.")],
        ),
        "cint-p3-balanced-paths": vi_challenge(
            "Mọi đường đều free",
            "Cài `format_stats` với nhiều đường cấp phát/thất bại luôn cân bằng free.",
            [("thành công và thất bại cân bằng", "Hai nửa bằng malloc+snprintf; hỏng ở đâu free cái đang giữ và trả 0.")],
        ),
        "cint-p3-owning-table": vi_challenge(
            "Bảng nhận sở hữu",
            "Cài OwnedTable: add sao chép vào bộ nhớ mới; destroy free từng chuỗi rồi mảng.",
            [("sở hữu qua vòng đời bảng", "Tăng trưởng như Vec nhưng cho char*; pop free ô chuỗi.")],
        ),
    },
    solutions=P3A_SOL,
)

# ---------------------------------------------------------------- practice 3b
P3B_CH = [
    challenge(
        "cint-p3-transfer",
        "Ownership Transfer Protocols",
        """Implement the three transfer flavors:

```c
/* STORE: copies s into the slot; caller keeps ownership of its own copy. */
void store_copy(char **slot, const char *s);
/* TAKE: slot now owns s's memory (no copy). Caller must not free s. */
void take_ownership(char **slot, char *s);
/* RELEASE: hands ownership back; returns the pointer and empties the slot. */
char *release(char **slot);
```

NULL-safe throughout: any NULL argument is a no-op (release returns NULL).""",
        C_PRELUDE,
        [
            (
                "copy vs take vs release",
                r"""
char *slot = NULL;
store_copy(&slot, "copied");
CHECK_STR_EQ(slot, "copied");
char *mine = malloc(6);
memcpy(mine, "taken", 6);
take_ownership(&slot, mine);
CHECK_STR_EQ(slot, "taken");
CHECK_EQ(slot, mine);            /* no copy: same pointer */
char *back = release(&slot);
CHECK_EQ(back, mine);
CHECK_NULL(slot);
free(back);                       /* caller owns it again */
store_copy(NULL, "x");            /* no-ops */
take_ownership(NULL, NULL);
CHECK_EQ(release(NULL), NULL);
""",
                "store_copy strdups; take stores the pointer itself; release reads and NULLs.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p3-leak-arith",
        "Leak Arithmetic",
        """Implement a model of a function's allocation paths and predict balance:

```c
/* ops string: 'A' = allocate (success), 'a' = allocate (FAILED),
   'F' = free, 'R' = early return on this path.
   For ONE path (prefix up to 'R', or whole string if no 'R'):
   return 1 if the path is balanced (no leak), 0 if it leaks. */
int path_leaks(const char *ops);
```

An allocation that failed ('a') needs no free. An allocation that succeeded
('A') must be freed ('F') before the path ends. NULL/empty: balanced (1).""",
        C_PRELUDE,
        [
            (
                "path balance verdicts",
                r"""
CHECK_EQ(path_leaks("AF"), 1);
CHECK_EQ(path_leaks("AR"), 0);     /* returned holding a live allocation */
CHECK_EQ(path_leaks("aFR"), 1);    /* failed alloc needs no free */
CHECK_EQ(path_leaks("AAF"), 0);    /* two allocs, one free */
CHECK_EQ(path_leaks("AFAF"), 1);
CHECK_EQ(path_leaks("a"), 1);      /* a failed alloc owes nothing */
CHECK_EQ(path_leaks(""), 1);
CHECK_EQ(path_leaks(NULL), 1);
""",
                "Count successful allocs minus frees up to 'R' or end; balanced iff zero.",
            ),
        ],
        level="guided",
    ),
    challenge(
        "cint-p3-dangling-doc",
        "Borrowing Rules",
        """A struct holds a BORROWED string. Implement the documented discipline:

```c
typedef struct { const char *name; int score; } Record;   /* in boilerplate */

/* initializes the record with a borrowed name (NOT copied, NOT freed by
   the record). Caller must keep name alive as long as the record lives. */
void record_init(Record *r, const char *name, int score);
/* returns the borrowed name (or NULL) */
const char *record_name(const Record *r);
/* prints "name=score\\n" (e.g. "ada=99\\n") using the borrowed name */
void record_print(const Record *r);
```""",
        C_PRELUDE + "\ntypedef struct { const char *name; int score; } Record;\n",
        [
            (
                "borrowed lifetime respected",
                r"""
char owner[] = "ada";             /* caller-owned storage */
Record r;
record_init(&r, owner, 99);
CHECK_STR_EQ(record_name(&r), "ada");
CHECK_EQ(r.name, owner);          /* truly borrowed: same storage */
record_init(&r, "static-literal", 50);
CHECK_STR_EQ(record_name(&r), "static-literal");
""",
                "Store the pointer as-is; no strdup, no free anywhere in the record API.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "cint-p3-arena",
        "A Tiny Arena (Own Once, Free Once)",
        """Implement a bump allocator (arena) — one ownership boundary for many
small allocations:

```c
typedef struct { unsigned char *buf; size_t cap, used; } Arena;  /* in boilerplate */
int arena_init(Arena *a, size_t cap);     /* malloc cap bytes; 0 on failure */
/* returns cap bytes of zeroed space inside the arena, or NULL if full */
void *arena_alloc(Arena *a, size_t n);
/* frees the whole arena in one free; zeroes the struct */
void arena_destroy(Arena *a);
```""",
        C_PRELUDE + "\ntypedef struct { unsigned char *buf; size_t cap, used; } Arena;\n",
        [
            (
                "bump allocation semantics",
                r"""
Arena a;
CHECK_EQ(arena_init(&a, 64), 1);
unsigned char *warm = arena_alloc(&a, 32);
CHECK_NOT_NULL(warm);
memset(warm, 0xFF, 32);            /* dirty the next region's bytes */
int *ints = arena_alloc(&a, 4 * sizeof(int));
CHECK_NOT_NULL(ints);
CHECK_EQ(ints[0], 0);              /* fresh region must be zeroed */
ints[0] = 10; ints[3] = 40;
CHECK_EQ(ints[3], 40);
CHECK_EQ(arena_alloc(&a, 64), NULL);   /* only 16 bytes left */
CHECK_EQ(arena_alloc(&a, 17), NULL);
char *small = arena_alloc(&a, 8);
CHECK_NOT_NULL(small);
arena_destroy(&a);
CHECK_NULL(a.buf);
""",
                "used += n if it fits; return buf + old used; memset the region to 0.",
            ),
        ],
        level="mini-build",
    ),
]
P3B_SOL = [
    (
        "cint-p3-transfer",
        r"""
void store_copy(char **slot, const char *s) {
    if (!slot || !s) return;
    size_t n = strlen(s);
    char *b = malloc(n + 1);
    if (!b) return;
    memcpy(b, s, n + 1);
    *slot = b;
}
void take_ownership(char **slot, char *s) {
    if (!slot || !s) return;
    *slot = s;
}
char *release(char **slot) {
    if (!slot) return NULL;
    char *p = *slot;
    *slot = NULL;
    return p;
}""",
        r"""
void store_copy(char **slot, const char *s) {
    if (!slot || !s) return;
    size_t n = strlen(s);
    char *b = malloc(n + 1);
    if (!b) return;
    memcpy(b, s, n + 1);
    *slot = b;
}
void take_ownership(char **slot, char *s) {
    if (!slot || !s) return;
    size_t n = strlen(s);
    char *b = malloc(n + 1);   /* wrong: copies instead of taking — caller's
                                  pointer now leaks and slot no longer aliases */
    if (!b) return;
    memcpy(b, s, n + 1);
    *slot = b;
}
char *release(char **slot) {
    if (!slot) return NULL;
    char *p = *slot;
    *slot = NULL;
    return p;
}""",
    ),
    (
        "cint-p3-leak-arith",
        r"""
int path_leaks(const char *ops) {
    if (!ops) return 1;
    int live = 0;
    for (const char *p = ops; *p; p++) {
        if (*p == 'A') live++;
        else if (*p == 'F') { if (live > 0) live--; }
        else if (*p == 'R') break;
    }
    return live == 0;
}""",
        r"""
int path_leaks(const char *ops) {
    if (!ops) return 1;
    int live = 0;
    for (const char *p = ops; *p; p++) {
        if (*p == 'A') live++;
        else if (*p == 'F') { if (live > 0) live--; }
        /* wrong: 'a' (failed alloc) also increments */
        else if (*p == 'a') live++;
        else if (*p == 'R') break;
    }
    return live == 0;
}""",
    ),
    (
        "cint-p3-dangling-doc",
        r"""
void record_init(Record *r, const char *name, int score) {
    if (!r) return;
    r->name = name;
    r->score = score;
}
const char *record_name(const Record *r) {
    return r ? r->name : NULL;
}
void record_print(const Record *r) {
    if (!r || !r->name) return;
    printf("name=%s\\n", r->name);
}""",
        r"""
static char stashed[64];
void record_init(Record *r, const char *name, int score) {
    if (!r) return;
    snprintf(stashed, sizeof stashed, "%s", name);   /* wrong: copies
                                                        instead of borrowing */
    r->name = stashed;
    r->score = score;
}
const char *record_name(const Record *r) {
    return r ? r->name : NULL;
}
void record_print(const Record *r) {
    if (!r || !r->name) return;
    printf("name=%s\\n", r->name);
}""",
    ),
    (
        "cint-p3-arena",
        r"""
int arena_init(Arena *a, size_t cap) {
    if (!a || cap == 0) return 0;
    a->buf = malloc(cap);
    if (!a->buf) return 0;
    a->cap = cap;
    a->used = 0;
    return 1;
}
void *arena_alloc(Arena *a, size_t n) {
    if (!a || !a->buf || n == 0 || n > a->cap - a->used) return NULL;
    void *p = a->buf + a->used;
    a->used += n;
    memset(p, 0, n);
    return p;
}
void arena_destroy(Arena *a) {
    if (!a) return;
    free(a->buf);
    a->buf = NULL;
    a->cap = a->used = 0;
}""",
        r"""
int arena_init(Arena *a, size_t cap) {
    if (!a || cap == 0) return 0;
    a->buf = malloc(cap);
    if (!a->buf) return 0;
    a->cap = cap;
    a->used = 0;
    return 1;
}
void *arena_alloc(Arena *a, size_t n) {
    if (!a || !a->buf || n == 0) return NULL;
    if (a->used + n > a->cap) return NULL;   /* overflow-unsafe add; fine here,
                                                but this version forgets zeroing */
    void *p = a->buf + a->used;
    a->used += n;
    return p;
}
void arena_destroy(Arena *a) {
    if (!a) return;
    free(a->buf);
    a->buf = NULL;
    a->cap = a->used = 0;
}""",
    ),
]
write_practice(
    M, "cint-p3-ownership",
    "Ownership Patterns Gym",
    "Transfer protocols, path-balance arithmetic, borrowed lifetimes, and the arena.",
    "Phòng gym mẫu sở hữu",
    "Giao thức chuyển giao, phép toán cân bằng đường, thời gian sống mượn, và arena.",
    after_lesson="lifetime-violations",
    minutes=26,
    difficulty="intermediate",
    challenges=P3B_CH,
    vi_challenges={
        "cint-p3-transfer": vi_challenge(
            "Giao thức chuyển giao sở hữu",
            "Cài store_copy (sao chép), take_ownership (nhận con trỏ), release (trả về và rỗng slot).",
            [("copy vs take vs release", "store_copy strdups; take lưu chính con trỏ; release đọc rồi gán NULL.")],
        ),
        "cint-p3-leak-arith": vi_challenge(
            "Phép toán rò rỉ",
            "Cài `path_leaks`: đường cân bằng khi số cấp phát thành công bằng số free.",
            [("phán quyết cân bằng", "Đếm cấp phát thành công trừ free đến 'R' hoặc hết chuỗi; cân bằng khi bằng 0.")],
        ),
        "cint-p3-dangling-doc": vi_challenge(
            "Quy tắc mượn",
            "Cài Record mượn chuỗi: không sao chép, không free — caller giữ name còn sống.",
            [("thời gian sống mượn được tôn trọng", "Lưu con trỏ nguyên trạng; không strdup, không free.")],
        ),
        "cint-p3-arena": vi_challenge(
            "Arena nhỏ (sở hữu một lần, free một lần)",
            "Cài bump allocator: alloc vùng zeroed, destroy free toàn bộ.",
            [("ngữ nghĩa bump allocation", "used += n nếu vừa; trả buf + used cũ; memset vùng về 0.")],
        ),
    },
    solutions=P3B_SOL,
)

# ---------------------------------------------------------------- checkpoint
CP_CH = challenge(
    "cint-checkpoint-m3-task",
    "Checkpoint: The Owning Stack",
    """Compose the ownership discipline into one structure — a stack of owned
strings with full lifecycle:

```c
typedef struct { char **items; size_t len, cap; } StrStack;  /* in boilerplate */
void ss_init(StrStack *s);
/* pushes a COPY of s. 0 on failure; stack unchanged then. */
int ss_push(StrStack *s, const char *s2);
/* pops: hands the TOP string's ownership back to the caller and removes it.
   Returns the pointer (caller now owns and must free), or NULL if empty. */
char *ss_pop(StrStack *s);
/* peeks without transferring: the stack still owns it */
const char *ss_peek(const StrStack *s);
/* frees everything; safe to call twice */
void ss_destroy(StrStack *s);
```""",
    C_PRELUDE + "\ntypedef struct { char **items; size_t len, cap; } StrStack;\n",
    [
        (
            "full lifecycle",
            r"""
StrStack st;
ss_init(&st);
CHECK_EQ(ss_push(&st, "one"), 1);
CHECK_EQ(ss_push(&st, "two"), 1);
CHECK_STR_EQ(ss_peek(&st), "two");
char *got = ss_pop(&st);
CHECK_STR_EQ(got, "two");
free(got);                        /* caller owns it now */
CHECK_STR_EQ(ss_peek(&st), "one");
CHECK_EQ(ss_pop(&st) != NULL, 1);
char *none = ss_pop(&st);
CHECK_NULL(none);
free(none);                        /* free(NULL) fine */
ss_destroy(&st);
ss_destroy(&st);
CHECK_NULL(st.items);
""",
                "Push copies (malloc+memcpy); pop returns the stored pointer and decrements; destroy frees items then array.",
            ),
            (
                "LIFO order and capacity growth",
                r"""
StrStack st;
ss_init(&st);
const char *words[] = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j"};
for (int i = 0; i < 10; i++) CHECK_EQ(ss_push(&st, words[i]), 1);
for (int i = 9; i >= 0; i--) {
    char *p = ss_pop(&st);
    CHECK_STR_EQ(p, words[i]);
    free(p);
}
ss_destroy(&st);
""",
                "Growth doubles; pops come back in exact reverse order.",
            ),
        ],
        level="independent",
        difficulty="intermediate",
)
CP_VI = vi_challenge(
    "Kiểm tra: Ngăn xếp sở hữu",
    "Cài StrStack với vòng đời đầy đủ: push sao chép, pop chuyển giao sở hữu, peek mượn, destroy an toàn hai lần.",
    [("vòng đời đầy đủ", "Push copy (malloc+memcpy); pop trả con trỏ đã lưu và giảm len; destroy free items rồi mảng."),
     ("thứ tự LIFO và tăng dung lượng", "Tăng trưởng nhân đôi; pop trả về đúng thứ tự ngược.")],
)
write_checkpoint(
    M, "cint-checkpoint-m3",
    "Checkpoint: Ownership",
    "Prove you can build a structure whose ownership story survives pushes, pops, peeks, and double destroys.",
    22,
    r"""
## What you just proved

- Allocation-failure contracts that never leave a half-built state.
- The realloc temp-pointer discipline, amortized doubling.
- Ownership transfer (store/take/release) as explicit API vocabulary.
- A structure that frees every byte exactly once on every path.

Next module: functions as data — pointers to code, and the designs they unlock.
""",
    "Kiểm tra: Quyền sở hữu",
    "Chứng minh bạn xây được cấu trúc mà câu chuyện sở hữu sống sót qua push, pop, peek, và destroy hai lần.",
    r"""
## Bạn vừa chứng minh điều gì

- Hợp đồng thất bại cấp phát không bao giờ để lại trạng thái dở dang.
- Kỷ luật con-trỏ-tạm của realloc, nhân đôi khấu hao.
- Chuyển giao sở hữu (store/take/release) như từ vựng API tường minh.
- Một cấu trúc free từng byte đúng một lần trên mọi đường đi.

Module sau: hàm như dữ liệu — con trỏ trỏ vào code, và các thiết kế chúng mở ra.
""",
    CP_CH,
    CP_VI,
    solution=r"""
void ss_init(StrStack *s) {
    if (!s) return;
    s->items = NULL;
    s->len = 0;
    s->cap = 0;
}
int ss_push(StrStack *s, const char *s2) {
    if (!s || !s2) return 0;
    if (s->len == s->cap) {
        size_t ncap = s->cap ? s->cap * 2 : 8;
        char **ni = realloc(s->items, ncap * sizeof *ni);
        if (!ni) return 0;
        s->items = ni;
        s->cap = ncap;
    }
    size_t n = strlen(s2);
    char *copy = malloc(n + 1);
    if (!copy) return 0;
    memcpy(copy, s2, n + 1);
    s->items[s->len++] = copy;
    return 1;
}
char *ss_pop(StrStack *s) {
    if (!s || s->len == 0) return NULL;
    return s->items[--s->len];
}
const char *ss_peek(const StrStack *s) {
    if (!s || s->len == 0) return NULL;
    return s->items[s->len - 1];
}
void ss_destroy(StrStack *s) {
    if (!s) return;
    for (size_t i = 0; i < s->len; i++) free(s->items[i]);
    free(s->items);
    s->items = NULL;
    s->len = s->cap = 0;
}""",
    wrong=r"""
void ss_init(StrStack *s) {
    if (!s) return;
    s->items = NULL;
    s->len = 0;
    s->cap = 0;
}
int ss_push(StrStack *s, const char *s2) {
    if (!s || !s2) return 0;
    if (s->len == s->cap) {
        size_t ncap = s->cap ? s->cap * 2 : 8;
        char **ni = realloc(s->items, ncap * sizeof *ni);
        if (!ni) return 0;
        s->items = ni;
        s->cap = ncap;
    }
    s->items[s->len++] = (char *)s2;   /* wrong: stores borrowed pointer —
                                          destroy frees caller memory */
    return 1;
}
char *ss_pop(StrStack *s) {
    if (!s || s->len == 0) return NULL;
    return s->items[--s->len];
}
const char *ss_peek(const StrStack *s) {
    if (!s || s->len == 0) return NULL;
    return s->items[s->len - 1];
}
void ss_destroy(StrStack *s) {
    if (!s) return;
    for (size_t i = 0; i < s->len; i++) free(s->items[i]);
    free(s->items);
    s->items = NULL;
    s->len = s->cap = 0;
}""",
)

print("module 3 complete")
