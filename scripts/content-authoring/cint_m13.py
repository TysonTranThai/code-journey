#!/usr/bin/env python3
"""C — Intermediate — Module 13: cint-errors.

Error handling as API design: return-code conventions, errno, the
cleanup-goto pattern, two-phase init, and error propagation through
layers. House conventions: ISO C only, self-contained tests, Ws are
behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-errors"

write_module(
    M,
    "Errors & Robust APIs",
    "Failure as a designed outcome: codes that cannot be ignored, cleanup "
    "that cannot be forgotten, layers that add context without lying.",
    "Lỗi & API bền vững",
    "Thất bại là kết quả được thiết kế: return code không thể bỏ qua, "
    "dọn dẹp không thể quên, các tầng thêm ngữ cảnh mà không nói dối.",
    lessons=["return-codes", "cleanup-goto", "layered-errors", "cint-checkpoint-m13"],
    practices=["cint-p13-codes", "cint-p13-layers"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "return-codes",
    "Return Codes & errno",
    "The C error vocabulary: -1/NULL conventions, errno's contract, and "
    "why every failure path must be reachable in a test.",
    16,
    r"""
## The vocabulary, written down

C has no exceptions — every function *negotiates* failure through its
return value. The conventions that make an API predictable:

```c
/* success: 0 or a value; failure: -1 (numeric) or NULL (pointer) */
long  parse(const char *s, long *out);      /* 0 ok, -1 bad */
char *dup_str(const char *s);               /* NULL on failure */
/* three-valued: 0 = yes, 1 = no, -1 = error (like ferror semantics) */
int   contains(const Set *s, int v);        /* distinguish "absent" from "broken" */
```

The cardinal rule: **one meaning per value.** A function that returns
`int` where 0 means "found", 1 means "not found", and -1 means "error"
is *documenting* that its caller must check all three — write that in
the header, and test all three.

## errno: the thread of context

On failure, library functions set `errno` — a global(ish) int with
symbolic names in `<errno.h>`:

```c
#include <errno.h>
FILE *f = fopen(path, "r");
if (!f) {
    if (errno == ENOENT) /* no such file */;
    else if (errno == EACCES) /* permission */;
    /* ... */
}
```

The contract is subtle: errno is meaningful **only immediately after a
call that failed** — and only when that function documents setting it.
Reading errno after a success (or after another call) is garbage. `perror`
and `strerror(errno)` translate the number for humans. ISO C defines the
mechanism; the *specific* values beyond a core set (ENOENT, EACCES,
ENOMEM...) are platform territory — another ISO/POSIX boundary to mark.

## Failure paths are code too

Every `-1` in your implementation is a branch a test must reach. An API
whose failure paths cannot be triggered from tests has failure paths
nobody has ever run — the most dangerous code in the codebase. Design
failures to be injectable: bad arguments (NULL, empty, out-of-range) are
the honest lever in unit tests.
""",
"Return code & errno",
    "Từ vựng lỗi của C: quy ước -1/NULL, hợp đồng errno, và vì sao mọi "
    "đường thất bại phải chạm được trong test.",
    r"""
## Từ vựng, viết ra giấy

C không có exception — mọi hàm *đàm phán* thất bại qua giá trị trả về.
Các quy ước khiến API dự đoán được:

```c
/* thành công: 0 hoặc giá trị; thất bại: -1 (số) hoặc NULL (con trỏ) */
long  parse(const char *s, long *out);      /* 0 ok, -1 xấu */
char *dup_str(const char *s);               /* NULL khi thất bại */
/* ba giá trị: 0 = có, 1 = không, -1 = lỗi */
int   contains(const Set *s, int v);        /* phân biệt "vắng" với "hỏng" */
```

Quy tắc tối thượng: **một giá trị, một nghĩa.** Hàm trả `int` với 0 là
"tìm thấy", 1 là "không có", -1 là "lỗi" đang *ghi rõ* caller phải kiểm
cả ba — viết vào header, và test cả ba.

## errno: sợi chỉ ngữ cảnh

Khi thất bại, hàm thư viện đặt `errno` — một int toàn cục (tương đối)
với tên biểu tượng trong `<errno.h>`:

```c
#include <errno.h>
FILE *f = fopen(path, "r");
if (!f) {
    if (errno == ENOENT) /* không có tệp */;
    else if (errno == EACCES) /* không quyền */;
}
```

Hợp đồng tinh tế: errno có nghĩa **chỉ ngay sau một lời gọi vừa thất
bại** — và chỉ khi hàm đó ghi rõ là đặt nó. Đọc errno sau một thành công
(hoặc sau lời gọi khác) là rác. `perror` và `strerror(errno)` dịch số
cho người. ISO C định nghĩa cơ chế; *các giá trị cụ thể* ngoài nhóm lõi
(ENOENT, EACCES, ENOMEM...) là lãnh thổ platform — một biên giới ISO/
POSIX nữa cần đánh dấu.

## Đường thất bại cũng là code

Mỗi `-1` trong cài đặt là một nhánh mà test phải chạm tới. API có đường
thất bại không thể kích hoạt từ test có các đường thất bại chưa từng
được chạy — code nguy hiểm nhất của codebase. Thiết kế thất bại để tiêm
được: tham số xấu (NULL, rỗng, ngoài khoảng) là đòn bẩy trung thực trong
unit test.
"""
)

write_lesson(
    M, "cleanup-goto",
    "The cleanup-goto Pattern",
    "One exit, many cleanups: how C keeps resource pairing sane without "
    "destructors.",
    17,
    r"""
## The problem: N resources, 2^N exit paths

```c
int process(const char *in, const char *out) {
    FILE *fi = fopen(in, "rb");
    if (!fi) return -1;
    unsigned char *buf = malloc(SIZE);
    if (!buf) { fclose(fi); return -1; }        /* repeat for every resource */
    FILE *fo = fopen(out, "wb");
    if (!fo) { free(buf); fclose(fi); return -1; }
    /* ... body: every early return must free everything ... */
}
```

Three resources means every new early return must remember the exact
cleanup list of everything acquired so far — the code review game of
whack-a-mole. The C-idiomatic answer is **one entry, one exit, cleanup
in reverse order at the bottom**:

```c
int process(const char *in, const char *out) {
    int rc = -1;
    FILE *fi = NULL, *fo = NULL;
    unsigned char *buf = NULL;

    fi = fopen(in, "rb");
    if (!fi) goto cleanup;
    buf = malloc(SIZE);
    if (!buf) goto cleanup;
    fo = fopen(out, "wb");
    if (!fo) goto cleanup;

    rc = do_work(fi, buf, fo);     /* the happy path */

cleanup:
    free(buf);                     /* free(NULL) is a no-op: safe */
    if (fo) fclose(fo);
    if (fi) fclose(fi);
    return rc;
}
```

`goto` is not a swear word here: the Linux kernel's error handling is
built on exactly this pattern, at every level, everywhere. The
discipline is the *direction* — forward jumps to a single cleanup label
only, never backward, never out of allocation contexts. Variables are
initialized to their empty state (`NULL`, 0) so the cleanup block is
correct even when the failure happened before acquisition.

## Why not just nest ifs?

Nesting works for two resources and collapses at four. The cleanup block
also becomes the *single place to audit*: every resource appears exactly
once, in reverse-acquisition order — the pairing is visually verifiable.
That property is what "robust API" means in C.
""",
"Mẫu cleanup-goto",
    "Một lối thoát, nhiều lần dọn dẹp: cách C giữ ghép cặp tài nguyên "
    "chân lý mà không cần destructor.",
    r"""
## Vấn đề: N tài nguyên, 2^N đường thoát

```c
int process(const char *in, const char *out) {
    FILE *fi = fopen(in, "rb");
    if (!fi) return -1;
    unsigned char *buf = malloc(SIZE);
    if (!buf) { fclose(fi); return -1; }        /* lặp lại cho mỗi tài nguyên */
    FILE *fo = fopen(out, "wb");
    if (!fo) { free(buf); fclose(fi); return -1; }
    /* ... thân: mọi return sớm phải free đúng các thứ đã lấy ... */
}
```

Ba tài nguyên nghĩa là mỗi return sớm mới phải nhớ chính xác danh sách
dọn dẹp của mọi thứ đã lấy — trò chơi chuột chũi trong code review. Câu
trả lời idiomatic của C là **một lối vào, một lối ra, dọn dẹp ngược thứ
tự ở đáy**:

```c
int process(const char *in, const char *out) {
    int rc = -1;
    FILE *fi = NULL, *fo = NULL;
    unsigned char *buf = NULL;

    fi = fopen(in, "rb");
    if (!fi) goto cleanup;
    buf = malloc(SIZE);
    if (!buf) goto cleanup;
    fo = fopen(out, "wb");
    if (!fo) goto cleanup;

    rc = do_work(fi, buf, fo);     /* đường hạnh phúc */

cleanup:
    free(buf);                     /* free(NULL) là no-op: an toàn */
    if (fo) fclose(fo);
    if (fi) fclose(fi);
    return rc;
}
```

`goto` ở đây không phải từ xấu: xử lý lỗi của Linux kernel xây trên đúng
mẫu này, mọi tầng, mọi nơi. Kỷ luật nằm ở *hướng* — nhảy tới trước tới
một label dọn dẹp duy nhất, không bao giờ nhảy ngược, không bao giờ nhảy
ra khỏi ngữ cảnh cấp phát. Biến được khởi tạo về trạng thái rỗng
(`NULL`, 0) để khối dọn dẹp đúng ngay cả khi thất bại xảy ra trước khi
lấy tài nguyên.

## Sao không lồng if?

Lồng if chạy với hai tài nguyên và sụp ở bốn. Khối cleanup còn là *nơi
duy nhất để soát*: mỗi tài nguyên xuất hiện đúng một lần, theo thứ tự
ngược lúc lấy — phép ghép cặp soát bằng mắt được. Tính chất đó chính là
nghĩa của "API bền vững" trong C.
"""
)

write_lesson(
    M, "layered-errors",
    "Errors Through Layers",
    "Propagation that adds context: wrap, don't swallow; distinguish, "
    "don't conflate; and the two-phase init that makes construction "
    "failable.",
    17,
    r"""
## Swallowing is the original sin

```c
int load_config(Config *c) {
    if (read_file(c) != 0) return 0;      /* failed, but reports success */
    return 0;
}
```

A layer that converts failure into success doesn't remove the failure —
it *hides* it, so the bug surfaces three layers away from its cause.
The opposite sin is conflation: returning the same code for "file
missing" and "file unreadable", so the caller cannot react differently.
The middle path is **wrap and add context**:

```c
/* layer 1 returns: 0 ok, -1 io error */
/* layer 2 adds meaning without lying: */
int load_app(App *app) {
    if (load_config(&app->cfg) != 0) return CFG_ERR;     /* distinct code */
    if (load_assets(&app->art) != 0) return ASSET_ERR;   /* distinct code */
    return OK;
}
```

Each layer translates the codes below it into codes that mean something
at its own abstraction level. The caller of `load_app` does not care
*which* file read failed — it cares that configuration, specifically,
is broken.

## Construction can fail: two-phase init

Constructors in C cannot return errors inside the object — so the
idiom is either NULL-returning constructors or **two-phase init**:

```c
/* phase 1: make it valid-but-empty; returns error code */
int conn_init(Conn *c);
/* phase 2: attach resources; returns error code */
int conn_connect(Conn *c, const char *target);
/* teardown is always safe, from any state */
void conn_destroy(Conn *c);
```

The rule that makes it work: `destroy` must be safe from *every*
reachable state — freshly-init'd, connected, or failed-connect. That
invariant is testable: init, destroy; init, connect-fail, destroy;
init, connect, destroy — no leak, no crash in any order.

## The panic boundary

Some failures are not recoverable by the layer that sees them: a NULL
*self* argument is a *contract violation by the caller* — a programming
error, not a runtime condition. Real APIs either crash fast (assert)
with a message naming the file/line, or document the UB honestly.
Silently "handling" a NULL self hides the bug from the only person who
can fix it: the programmer who made the call.
""",
"Lỗi xuyên qua các tầng",
    "Truyền lỗi có thêm ngữ cảnh: bọc, không nuốt; phân biệt, không gộp; "
    "và init hai pha khiến construction có thể thất bại.",
    r"""
## Nuốt lỗi là tội gốc

```c
int load_config(Config *c) {
    if (read_file(c) != 0) return 0;      /* thất bại nhưng báo thành công */
    return 0;
}
```

Một tầng biến thất bại thành thành công không xóa được thất bại — nó
*giấu* nó, để bug nổi lên cách nguyên nhân ba tầng. Tội ngược lại là
gộp chung: cùng một code cho "thiếu tệp" và "tệp không đọc được", nên
caller không thể phản ứng khác nhau. Đường giữa là **bọc và thêm ngữ
cảnh**:

```c
/* tầng 1 trả: 0 ok, -1 lỗi io */
/* tầng 2 thêm nghĩa mà không nói dối: */
int load_app(App *app) {
    if (load_config(&app->cfg) != 0) return CFG_ERR;     /* code riêng */
    if (load_assets(&app->art) != 0) return ASSET_ERR;   /* code riêng */
    return OK;
}
```

Mỗi tầng dịch các code bên dưới thành code có nghĩa ở mức trừu tượng của
chính nó. Caller của `load_app` không quan tâm *tệp nào* đọc lỗi — nó
quan tâm rằng cấu hình, cụ thể, đã hỏng.

## Construction có thể thất bại: init hai pha

Constructor trong C không thể trả lỗi bên trong object — nên idiom là
constructor trả NULL hoặc **init hai pha**:

```c
/* pha 1: hợp lệ-nhưng-rỗng; trả error code */
int conn_init(Conn *c);
/* pha 2: gắn tài nguyên; trả error code */
int conn_connect(Conn *c, const char *target);
/* teardown luôn an toàn, từ mọi trạng thái */
void conn_destroy(Conn *c);
```

Quy tắc khiến nó chạy: `destroy` phải an toàn từ *mọi* trạng thái chạm
được — vừa init, đã connect, hoặc connect-thất-bại. Bất biến đó kiểm
được: init, destroy; init, connect-lỗi, destroy; init, connect, destroy
— không leak, không crash với bất kỳ thứ tự nào.

## Ranh giới panic

Một số thất bại không thể phục hồi ở tầng nhìn thấy nó: tham số *self*
NULL là *vi phạm hợp đồng bởi caller* — lỗi lập trình, không phải điều
kiện runtime. API thật hoặc crash nhanh (assert) với thông báo nêu
file/dòng, hoặc ghi UB trung thực. "Xử lý" lặng lẽ một self NULL giấu
bug khỏi người duy nhất sửa được nó: lập trình viên đã gọi.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p13-codes",
    "Error Contract Gym",
    "Three-valued returns, errno-style context, and failure paths under test.",
    "Phòng gym hợp đồng lỗi",
    "Return ba giá trị, ngữ cảnh kiểu errno, và các đường thất bại dưới test.",
    after_lesson="return-codes",
    minutes=24,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p13-threeval",
            "Three-Valued APIs",
            """Implement the discriminating API. The boilerplate declares:

```c
#define LOOKUP_FOUND    0
#define LOOKUP_ABSENT   1
#define LOOKUP_ERROR   (-1)
typedef struct { long keys[16]; long vals[16]; size_t n; } Table;
void tab_init(Table *t);
int tab_put(Table *t, long k, long v);       /* 0 ok, -1 full/NULL */
/* FOUND (fills *out) | ABSENT | ERROR (bad args) */
int tab_get(const Table *t, long k, long *out);
int tab_del(Table *t, long k);               /* 1 removed, 0 absent, -1 NULL */
```

The tests distinguish all three values — a conflation fails them.""",
            C_PRELUDE + "\n#include <stddef.h>\n#define LOOKUP_FOUND    0\n#define LOOKUP_ABSENT   1\n#define LOOKUP_ERROR   (-1)\ntypedef struct { long keys[16]; long vals[16]; size_t n; } Table;\nvoid tab_init(Table *t);\nint tab_put(Table *t, long k, long v);\nint tab_get(const Table *t, long k, long *out);\nint tab_del(Table *t, long k);\n",
            [
                (
                    "found, absent, error — all distinct",
                    r"""
Table t;
tab_init(&t);
long v;
CHECK_EQ(tab_get(&t, 5, &v), LOOKUP_ABSENT);      /* empty: absent, not error */
CHECK_EQ(tab_put(&t, 5, 50), 0);
CHECK_EQ(tab_get(&t, 5, &v), LOOKUP_FOUND);
CHECK_EQ(v, 50);
CHECK_EQ(tab_get(&t, 6, &v), LOOKUP_ABSENT);
CHECK_EQ(tab_get(&t, 5, NULL), LOOKUP_ERROR);     /* bad out: error */
CHECK_EQ(tab_get(NULL, 5, &v), LOOKUP_ERROR);
CHECK_EQ(tab_put(NULL, 1, 1), -1);
CHECK_EQ(tab_del(&t, 5), 1);
CHECK_EQ(tab_del(&t, 5), 0);
CHECK_EQ(tab_del(NULL, 5), -1);
/* fill to capacity (16), then overflow is an ERROR, not silent loss */
for (long i = 0; i < 16; i++) CHECK_EQ(tab_put(&t, 100 + i, i), 0);
CHECK_EQ(tab_put(&t, 999, 1), -1);
""",
                    "absent and error are different answers to different questions: the key isn't there vs. the call itself is invalid.",
                ),
            ],
        ),
        challenge(
            "cint-p13-cleanup",
            "The Cleanup Ladder",
            """Implement a multi-resource pipeline with the cleanup-goto
pattern. The boilerplate declares a tiny fake-resource stack:

```c
/* resources must be acquired in order and released in REVERSE order;
   the tracker records acquire/release for verification */
void tr_reset(void);
int  tr_acquire(int id);        /* 0 ok; -1 if id already held */
void tr_release(int id);        /* no-op if not held */
int  tr_holds(int id);
/* your function: acquire 1, 2, 3; fail if any acquire fails;
   "work" = return 0; release in reverse order — ALWAYS, on every path */
int pipeline(int fail_at);      /* 0 = no failure; 1..3 = fail that acquire */
/* the tracker's record of events, as a string like "a1a2a3r3r2r1" */
const char *tr_log(void);
```

pipeline(fail_at) must leave NO resources held — whatever happens.""",
            C_PRELUDE + "\n#include <stddef.h>\nstatic char LOG[64]; static int held[4];\nvoid tr_reset(void) { LOG[0] = 0; for (int i = 0; i < 4; i++) held[i] = 0; }\nstatic void log_ev(char c, int id) { size_t n = 0; while (LOG[n]) n++; LOG[n++] = c; LOG[n++] = (char)('0' + id); LOG[n] = 0; }\nint  tr_acquire(int id) { if (id < 1 || id > 3 || held[id]) return -1; held[id] = 1; log_ev('a', id); return 0; }\nvoid tr_release(int id) { if (id >= 1 && id <= 3 && held[id]) { held[id] = 0; log_ev('r', id); } }\nint  tr_holds(int id) { return id >= 1 && id <= 3 ? held[id] : 0; }\nconst char *tr_log(void) { return LOG; }\nint pipeline(int fail_at);\n",
            [
                (
                    "every path cleans up",
                    r"""
tr_reset();
CHECK_EQ(pipeline(0), 0);
CHECK(!strcmp(tr_log(), "a1a2a3r3r2r1"));   /* full reverse release */
CHECK(!tr_holds(1) && !tr_holds(2) && !tr_holds(3));
tr_reset();
CHECK_EQ(pipeline(2), -1);                  /* acquire 2 fails */
CHECK(!strcmp(tr_log(), "a1r1"));           /* 1 was released */
CHECK(!tr_holds(1));
tr_reset();
CHECK_EQ(pipeline(3), -1);
CHECK(!strcmp(tr_log(), "a1a2r2r1"));
tr_reset();
CHECK_EQ(pipeline(1), -1);
CHECK(!strcmp(tr_log(), ""));               /* nothing acquired */
""",
                    "goto cleanup with all pointers pre-nulled; release 3, 2, 1 unconditionally at the label.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p13-threeval": vi_challenge(
            "API ba giá trị",
            "Cài Table với FOUND/ABSENT/ERROR phân biệt rõ — gộp chung là fail test.",
            [("found, absent, error — phân biệt", "absent và error là câu trả lời cho hai câu hỏi khác nhau.")],
        ),
        "cint-p13-cleanup": vi_challenge(
            "Cầu thang cleanup",
            "Cài pipeline(fail_at) với cleanup-goto: lấy 1,2,3; luôn trả ngược 3,2,1 trên mọi đường.",
            [("mọi đường đều dọn dẹp", "goto cleanup, mọi biến rỗng sẵn; release 3,2,1 vô điều kiện.")],
        ),
    },
    solutions=[
        (
            "cint-p13-threeval",
            r"""
#include <string.h>
#include <stddef.h>
void tab_init(Table *t) {
    if (!t) return;
    memset(t, 0, sizeof *t);
}
int tab_put(Table *t, long k, long v) {
    if (!t || t->n == 16) return -1;
    for (size_t i = 0; i < t->n; i++)
        if (t->keys[i] == k) { t->vals[i] = v; return 0; }
    t->keys[t->n] = k;
    t->vals[t->n] = v;
    t->n++;
    return 0;
}
int tab_get(const Table *t, long k, long *out) {
    if (!t || !out) return LOOKUP_ERROR;
    for (size_t i = 0; i < t->n; i++)
        if (t->keys[i] == k) { *out = t->vals[i]; return LOOKUP_FOUND; }
    return LOOKUP_ABSENT;
}
int tab_del(Table *t, long k) {
    if (!t) return -1;
    for (size_t i = 0; i < t->n; i++)
        if (t->keys[i] == k) {
            t->keys[i] = t->keys[t->n - 1];
            t->vals[i] = t->vals[t->n - 1];
            t->n--;
            return 1;
        }
    return 0;
}""",
            r"""
#include <string.h>
#include <stddef.h>
void tab_init(Table *t) {
    if (!t) return;
    memset(t, 0, sizeof *t);
}
int tab_put(Table *t, long k, long v) {
    if (!t || t->n == 16) return -1;
    t->keys[t->n] = k;
    t->vals[t->n] = v;
    t->n++;
    return 0;                     /* wrong: duplicate keys pile up —
                                       get returns whichever copy it meets */
}
int tab_get(const Table *t, long k, long *out) {
    if (!t) return LOOKUP_ABSENT;   /* wrong: bad ARGS reported as ABSENT */
    if (!out) return LOOKUP_ERROR;
    for (size_t i = 0; i < t->n; i++)
        if (t->keys[i] == k) { *out = t->vals[i]; return LOOKUP_FOUND; }
    return LOOKUP_ABSENT;
}
int tab_del(Table *t, long k) {
    if (!t) return 0;             /* wrong: NULL t is an error, not "absent" */
    for (size_t i = 0; i < t->n; i++)
        if (t->keys[i] == k) {
            t->n--;               /* wrong: leaves the deleted key in place
                                       and shifts nothing — later puts
                                       overwrite live entries */
            return 1;
        }
    return 0;
}""",
        ),
        (
            "cint-p13-cleanup",
            r"""
int pipeline(int fail_at) {
    int a1 = 0, a2 = 0, a3 = 0;
    int rc = -1;
    if (fail_at == 1) goto cleanup;
    if (tr_acquire(1) != 0) goto cleanup;
    a1 = 1;
    if (fail_at == 2) goto cleanup;
    if (tr_acquire(2) != 0) goto cleanup;
    a2 = 1;
    if (fail_at == 3) goto cleanup;
    if (tr_acquire(3) != 0) goto cleanup;
    a3 = 1;
    rc = 0;                        /* the work */
cleanup:
    if (a3) tr_release(3);
    if (a2) tr_release(2);
    if (a1) tr_release(1);
    return rc;
}""",
            r"""
int pipeline(int fail_at) {
    if (fail_at == 1) return -1;
    if (tr_acquire(1) != 0) return -1;
    if (fail_at == 2) return -1;   /* wrong: 1 never released */
    if (tr_acquire(2) != 0) { tr_release(1); return -1; }
    if (fail_at == 3) return -1;   /* wrong: 1 and 2 never released */
    if (tr_acquire(3) != 0) { tr_release(2); tr_release(1); return -1; }
    tr_release(3);
    tr_release(2);
    tr_release(1);
    return 0;
}""",
        ),
    ],
)

write_practice(
    M, "cint-p13-layers",
    "Layered Errors Gym",
    "Two-phase init with failable construction, and error codes that wrap without lying.",
    "Phòng gym lỗi phân tầng",
    "Init hai pha với construction có thể thất bại, và mã lỗi bọc mà không nói dối.",
    after_lesson="layered-errors",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p13-two-phase",
            "Two-Phase Init, Provable",
            """Implement a two-phase connection object. The boilerplate
declares:

```c
typedef enum { C_NEW, C_READY, C_CONNECTED, C_FAILED } CState;
typedef struct {
    CState state;
    char target[32];
    int attempts;
} Conn;
int conn_init(Conn *c);                       /* -> C_READY; 0 ok, -1 NULL */
int conn_connect(Conn *c, const char *target);/* 0 ok, -1 bad; -> C_CONNECTED
                                                 or C_FAILED (attempts counted) */
void conn_close(Conn *c);                     /* -> C_READY from CONNECTED/FAILED;
                                                 no-op from NEW/READY */
int conn_destroy(Conn *c);                    /* safe from EVERY state; 0 ok, -1 NULL */
```

connect fails (state C_FAILED) iff target is NULL/empty or longer than
31 chars. destroy must succeed from every reachable state.""",
            C_PRELUDE + "\n#include <stddef.h>\n#include <string.h>\ntypedef enum { C_NEW, C_READY, C_CONNECTED, C_FAILED } CState;\ntypedef struct {\n    CState state;\n    char target[32];\n    int attempts;\n} Conn;\nint conn_init(Conn *c);\nint conn_connect(Conn *c, const char *target);\nvoid conn_close(Conn *c);\nint conn_destroy(Conn *c);\n",
            [
                (
                    "every state is destroyable",
                    r"""
Conn c;
CHECK_EQ(conn_destroy(NULL), -1);
CHECK_EQ(conn_init(NULL), -1);
CHECK_EQ(conn_init(&c), 0);
CHECK_EQ(conn_destroy(&c), 0);               /* destroy from READY */
CHECK_EQ(conn_init(&c), 0);                  /* reusable */
CHECK_EQ(conn_connect(&c, NULL), -1);
CHECK_EQ(c.state, C_FAILED);
CHECK_EQ(c.attempts, 1);
CHECK_EQ(conn_destroy(&c), 0);               /* destroy from FAILED */
CHECK_EQ(conn_init(&c), 0);
CHECK_EQ(conn_connect(&c, ""), -1);
CHECK_EQ(conn_connect(&c, "host"), 0);
CHECK_EQ(c.state, C_CONNECTED);
conn_close(&c);
CHECK_EQ(c.state, C_READY);
CHECK_EQ(conn_destroy(&c), 0);
""",
                    "init sets state C_READY and zeroes everything; destroy works by inspection of nothing — it just returns 0 (no resources).",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p13-two-phase": vi_challenge(
            "Init hai pha, chứng minh được",
            "Cài Conn: init/connect/close/destroy — destroy an toàn từ MỌI trạng thái.",
            [("mọi trạng thái đều destroy được", "init đặt C_READY và zero; destroy không cần soi trạng thái.")],
        ),
    },
    solutions=[
        (
            "cint-p13-two-phase",
            r"""
#include <string.h>
#include <stddef.h>
int conn_init(Conn *c) {
    if (!c) return -1;
    memset(c, 0, sizeof *c);
    c->state = C_READY;
    return 0;
}
int conn_connect(Conn *c, const char *target) {
    if (!c) return -1;
    c->attempts++;
    if (!target || !*target || strlen(target) >= 32) {
        c->state = C_FAILED;
        return -1;
    }
    snprintf(c->target, sizeof c->target, "%s", target);
    c->state = C_CONNECTED;
    return 0;
}
void conn_close(Conn *c) {
    if (!c) return;
    if (c->state == C_CONNECTED || c->state == C_FAILED)
        c->state = C_READY;
}
int conn_destroy(Conn *c) {
    if (!c) return -1;
    c->state = C_NEW;
    return 0;
}""",
            r"""
#include <string.h>
#include <stddef.h>
int conn_init(Conn *c) {
    if (!c) return -1;
    memset(c, 0, sizeof *c);
    c->state = C_READY;
    return 0;
}
int conn_connect(Conn *c, const char *target) {
    if (!c) return -1;
    if (!target || !*target || strlen(target) >= 32) {
        c->state = C_FAILED;
        return -1;                 /* wrong: attempts not counted */
    }
    snprintf(c->target, sizeof c->target, "%s", target);
    c->state = C_CONNECTED;
    return 0;
}
void conn_close(Conn *c) {
    if (!c) return;
    c->state = C_READY;            /* wrong: closes from NEW too —
                                       invents a state transition that
                                       never happened */
}
int conn_destroy(Conn *c) {
    if (!c) return -1;
    if (c->state == C_CONNECTED) return -1;   /* wrong: destroy refuses a
                                                  valid state — leaks the object */
    c->state = C_NEW;
    return 0;
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m13-task",
    "A Layered Service With Honest Errors",
    """Assemble the module: a three-layer pipeline where each layer
translates errors, cleans up its own resources, and never lies. The
boilerplate declares:

```c
/* layer 3 (top) codes */
#define APP_OK 0
#define APP_ECONFIG 1      /* config stage failed */
#define APP_EDATA 2        /* data stage failed */
#define APP_EARGS (-1)     /* contract violation by caller */

/* layer 2 stages: 0 ok, -1 fail. Records what happened: */
/* config: parses "k=v\n..." lines (max 8, key/value <= 7 chars) */
int cfg_stage(const char *input, char *report, size_t cap);
/* data: sums "n\n" lines; all lines must be nonneg ints */
int data_stage(const char *input, long *total, char *report, size_t cap);
/* layer 3: runs both stages in order; first failure aborts and
   returns the APP_E* code for the FAILING stage (args bad -> APP_EARGS).
   report (cap chars) gets "config:..." then "data:..." details. */
int app_run(const char *cfg_in, const char *data_in, char *report, size_t cap);
```

The error taxonomy is the test: config failures and data failures must
be DISTINGUISHABLE at the top, and caller errors (NULL report) must be
a third thing.""",
    C_PRELUDE + "\n#include <stddef.h>\n#define APP_OK 0\n#define APP_ECONFIG 1\n#define APP_EDATA 2\n#define APP_EARGS (-1)\nint cfg_stage(const char *input, char *report, size_t cap);\nint data_stage(const char *input, long *total, char *report, size_t cap);\nint app_run(const char *cfg_in, const char *data_in, char *report, size_t cap);\n",
    [
        (
            "distinguish, wrap, never swallow",
            r"""
char report[128];
long total = -1;
CHECK_EQ(app_run("name=ann\nrole=dev\n", "5\n10\n", report, sizeof report), APP_OK);
CHECK(!strstr(report, "fail"));
/* config failure is APP_ECONFIG, not APP_EDATA */
CHECK_EQ(app_run("noequals\n", "5\n", report, sizeof report), APP_ECONFIG);
CHECK(!strstr(report, "config") == 0);        /* report names the stage */
/* data failure is APP_EDATA */
CHECK_EQ(app_run("a=1\n", "5\n-3\n", report, sizeof report), APP_EDATA);
CHECK(!strstr(report, "data") == 0);
/* caller errors are their own thing */
CHECK_EQ(app_run("a=1\n", "5\n", NULL, 10), APP_EARGS);
CHECK_EQ(app_run(NULL, "5\n", report, sizeof report), APP_ECONFIG);
""",
            "app_run: NULL report or cfg_in -> APP_EARGS/APP_ECONFIG by layer; run config first, stop at first failure, prefix the report with the stage name.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Dịch vụ phân tầng với lỗi trung thực",
        "Cài app_run ba tầng: lỗi config/data phân biệt được, lỗi caller là thứ ba, report nêu tên tầng.",
        [("phân biệt, bọc, không nuốt", "NULL report -> APP_EARGS; config chạy trước, dừng ở thất bại đầu, report ghi tên tầng.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m13",
    "Checkpoint: Errors You Can Trust",
    "Prove the taxonomy: every failure distinguishable, every cleanup run, no lie in any report.",
    28,
    r"""
## The task

Implement `app_run` and the two stages (see the challenge). The graded
surface is the *shape* of failure: config vs data vs caller-error are
three different answers; the report names the failing stage; a failure
in config means data never runs. Swallowing, conflating, or reporting
success on failure — the classic sins — all fail the tests.

Passing this proves you can design the error dimension of an API, not
just its happy path — the difference between code that works and code
that can be operated.

Next module: undefined behavior — the errors the compiler is allowed
to make for you.
""",
    "Kiểm tra: Lỗi đáng tin",
    "Chứng minh phép phân loại: mọi thất bại phân biệt được, mọi cleanup chạy, không lời nói dối trong report.",
    r"""
## Bài toán

Cài `app_run` và hai tầng (xem challenge). Bề mặt chấm điểm là *hình
dạng* của thất bại: config vs data vs lỗi-caller là ba câu trả lời
khác nhau; report nêu tên tầng hỏng; config hỏng thì data không chạy.
Nuốt lỗi, gộp chung, hoặc báo thành công khi thất bại — các tội kinh
điển — đều fail test.

Vượt qua chứng minh bạn thiết kế được chiều lỗi của một API, không chỉ
đường hạnh phúc — ranh giới giữa code chạy được và code vận hành được.

Module sau: hành vi undefined — những lỗi compiler được phép thay bạn
tạo ra.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <stdio.h>
#include <string.h>
#include <stddef.h>
int cfg_stage(const char *input, char *report, size_t cap) {
    if (!input || !report || cap == 0) return -1;
    report[0] = '\0';
    const char *p = input;
    int pairs = 0;
    while (*p) {
        const char *eq = strchr(p, '=');
        const char *eol = strchr(p, '\n');
        size_t linelen = eol ? (size_t)(eol - p) : strlen(p);
        if (!eq || (eol && eq > eol) || eq == p) {
            snprintf(report, cap, "config: line %d lacks key=value", pairs + 1);
            return -1;
        }
        pairs++;
        if (!eol) break;
        p = eol + 1;
    }
    if (pairs == 0) {
        snprintf(report, cap, "config: empty");
        return -1;
    }
    snprintf(report, cap, "config: ok (%d pairs)", pairs);
    return 0;
}
int data_stage(const char *input, long *total, char *report, size_t cap) {
    if (!input || !total || !report || cap == 0) return -1;
    report[0] = '\0';
    long sum = 0;
    const char *p = input;
    int lines = 0;
    while (*p) {
        const char *eol = strchr(p, '\n');
        size_t linelen = eol ? (size_t)(eol - p) : strlen(p);
        if (linelen == 0) {
            snprintf(report, cap, "data: empty line %d", lines + 1);
            return -1;
        }
        long v = 0;
        for (size_t i = 0; i < linelen; i++) {
            if (p[i] < '0' || p[i] > '9') {
                snprintf(report, cap, "data: line %d not a nonneg int", lines + 1);
                return -1;
            }
            v = v * 10 + (p[i] - '0');
            if (v > 1000000000L) {
                snprintf(report, cap, "data: line %d too large", lines + 1);
                return -1;
            }
        }
        sum += v;
        lines++;
        if (!eol) break;
        p = eol + 1;
    }
    *total = sum;
    snprintf(report, cap, "data: ok (%d lines, total %ld)", lines, sum);
    return 0;
}
int app_run(const char *cfg_in, const char *data_in, char *report, size_t cap) {
    if (!report || cap == 0) return APP_EARGS;
    report[0] = '\0';
    if (!cfg_in) return APP_ECONFIG;
    if (!data_in) return APP_EDATA;
    char stage[64];
    if (cfg_stage(cfg_in, stage, sizeof stage) != 0) {
        snprintf(report, cap, "%s", stage);
        return APP_ECONFIG;
    }
    long total = 0;
    if (data_stage(data_in, &total, stage, sizeof stage) != 0) {
        snprintf(report, cap, "%s", stage);
        return APP_EDATA;
    }
    snprintf(report, cap, "%s | %s", "ok", stage);
    return APP_OK;
}""",
    wrong=r"""
#include <stdio.h>
#include <string.h>
#include <stddef.h>
int cfg_stage(const char *input, char *report, size_t cap) {
    if (!input || !report || cap == 0) return -1;
    report[0] = '\0';
    const char *eq = strchr(input, '=');
    if (!eq) {
        snprintf(report, cap, "config: bad");
        return -1;
    }
    snprintf(report, cap, "config: ok");
    return 0;                    /* wrong: only checks the FIRST line —
                                       "a=1\nnoequals" wrongly passes */
}
int data_stage(const char *input, long *total, char *report, size_t cap) {
    if (!input || !total || !report || cap == 0) return -1;
    report[0] = '\0';
    *total = 0;
    const char *p = input;
    while (*p) {
        if (*p == '\n') { p++; continue; }
        if (*p == '-') {         /* wrong: '-' skipped silently — negatives
                                       accepted into a nonneg sum */
            p++;
            continue;
        }
        if (*p < '0' || *p > '9') {
            snprintf(report, cap, "data: bad");
            return -1;
        }
        *total = *total * 10 + (*p - '0');   /* wrong: accumulates digits
                                                  across lines without line
                                                  boundaries */
        p++;
    }
    snprintf(report, cap, "data: ok");
    return 0;
}
int app_run(const char *cfg_in, const char *data_in, char *report, size_t cap) {
    if (!report || cap == 0) return APP_EARGS;
    report[0] = '\0';
    char stage[64];
    if (cfg_stage(cfg_in, stage, sizeof stage) != 0
        || data_stage(data_in, &stage[0] != NULL ? stage : stage, sizeof stage) != 0)
        return APP_ECONFIG;      /* wrong: BOTH failures reported as config —
                                       data failures are indistinguishable */
    snprintf(report, cap, "%s", stage);
    return APP_OK;
}""",
)

print("module 13 complete")
