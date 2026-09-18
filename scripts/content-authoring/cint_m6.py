#!/usr/bin/env python3
"""C — Intermediate — Module 6: cint-strings.

Strings as buffers with boundaries: length-vs-capacity, the safe-copy
family, tokenization without strtok's hidden state, and parsing that
validates instead of trusting. All graded code ISO C (strtok_r is POSIX —
taught in prose, not used in graded solutions). House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-strings"

write_module(
    M,
    "Strings & Buffers",
    "Length vs capacity, the safe-copy family, tokenization you can reason "
    "about, and parsing that validates before it trusts.",
    "Chuỗi & Buffer",
    "Length vs capacity, họ hàm copy an toàn, tokenization có thể suy luận, "
    "và parsing kiểm chứng trước khi tin.",
    lessons=["buffers-boundaries", "safe-copying", "tokenize-parse", "cint-checkpoint-m6"],
    practices=["cint-p6-copy", "cint-p6-parse"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "buffers-boundaries",
    "Buffers & Boundaries",
    "A C string is a pointer plus a convention; a buffer is a pointer plus a "
    "size. Confusing them is the root of every overflow.",
    15,
    r"""
## Two numbers, one pointer

A C *string* is `char *` plus a convention: bytes until `'\0'`. Its length
is *discovered* by walking (`strlen`). A C *buffer* is `char *` plus a
*capacity* someone must track: how many bytes the allocation actually
holds. The classic disasters come from conflating them:

```c
char buf[8];
strcpy(buf, "0123456789");   /* writes 11 bytes into 8 — gone */
```

`strcpy` knows the source length but not the destination capacity — it
*cannot* be safe. The functions that can be safe take both numbers:

```c
/* strncpy: copies at most n bytes; NO '\0' if source fills n! */
strncpy(buf, src, sizeof buf);
/* snprintf: always terminates, returns what it WOULD have written */
int need = snprintf(buf, sizeof buf, "%s/%s", a, b);
if (need < 0 || (size_t)need >= sizeof buf) /* truncated — handle it */;
```

`snprintf` is the workhorse: bounded, terminating, and it *tells you*
when the output did not fit. That return value is the truncation
detector most code forgets to check.

## The boundary question, every time

Before touching a buffer, answer three questions in a comment: capacity?
current length? who terminates? Code that cannot answer those three
questions in its own comments is code that overflows under maintenance.
""",
"Buffer & Biên giới",
    "String C là pointer + quy ước; buffer là pointer + kích thước. Lẫn lộn "
    "hai thứ là gốc của mọi overflow.",
    r"""
## Hai con số, một con trỏ

*String* trong C là `char *` cộng một quy ước: các byte cho đến `'\0'`.
Độ dài được *khám phá* bằng cách đi bộ (`strlen`). *Buffer* trong C là
`char *` cộng một *capacity* ai đó phải theo dõi: vùng cấp phát thực sự
chứa được bao nhiêu byte. Thảm họa kinh điển đến từ việc lẫn lộn hai thứ:

```c
char buf[8];
strcpy(buf, "0123456789");   /* ghi 11 byte vào 8 — toi */
```

`strcpy` biết độ dài nguồn nhưng không biết capacity đích — nó *không thể*
an toàn. Các hàm có thể an toàn nhận cả hai con số:

```c
/* strncpy: copy tối đa n byte; KHÔNG có '\0' nếu nguồn chiếm hết n! */
strncpy(buf, src, sizeof buf);
/* snprintf: luôn terminate, trả về số byte SẼ ghi */
int need = snprintf(buf, sizeof buf, "%s/%s", a, b);
if (need < 0 || (size_t)need >= sizeof buf) /* bị cắt — xử lý */;
```

`snprintf` là lao công chính: có giới hạn, luôn terminate, và *báo cho bạn
biết* khi output không vừa. Giá trị trả về đó là máy dò truncate mà phần
lớn code quên kiểm.

## Câu hỏi biên giới, mỗi lần

Trước khi đụng vào buffer, trả lời ba câu hỏi trong comment: capacity?
độ dài hiện tại? ai terminate? Code không trả lời được ba câu đó trong
comment của chính nó là code sẽ tràn khi được bảo trì.
"""
)

write_lesson(
    M, "safe-copying",
    "Dynamic Strings & Safe Concatenation",
    "Building strings at runtime: the realloc-append pattern, and why every "
    "append is a (maybe-failing) allocation.",
    16,
    r"""
## A growable string is a tiny dynamic array

```c
typedef struct {
    char  *data;    /* malloc'd, always '\0'-terminated */
    size_t len;     /* characters, not counting '\0' */
    size_t cap;     /* allocated bytes */
} StrBuf;
```

Append is the whole API, and every append is three jobs in one: make
room, copy, terminate — with a failure path at step one:

```c
int sb_append(StrBuf *b, const char *s) {
    size_t need = b->len + strlen(s) + 1;
    if (need > b->cap) {
        size_t ncap = b->cap ? b->cap : 16;
        while (ncap < need) ncap *= 2;
        char *nd = realloc(b->data, ncap);
        if (!nd) return -1;          /* old b->data still valid! */
        b->data = nd;
        b->cap = ncap;
    }
    memcpy(b->data + b->len, s, strlen(s) + 1);
    b->len += strlen(s);
    return 0;
}
```

Note the oom discipline: `realloc` returning NULL does **not** free the
old block — keep the pointer, return the error, let the caller decide.
Assigning `b->data = realloc(b->data, ...)` directly would leak the old
buffer exactly when memory is already exhausted.

## Worst-case capacity planning

`snprintf(NULL, 0, ...)` measures first, so you can allocate exactly:

```c
int need = snprintf(NULL, 0, "%s: %d", name, value);  /* +1 for '\0' */
char *out = malloc((size_t)need + 1);
snprintf(out, (size_t)need + 1, "%s: %d", name, value);
```

Measure-then-allocate is how code formats without fixed buffers and
without truncation.
""",
"Chuỗi động & nối an toàn",
    "Xây string lúc runtime: mẫu realloc-append, và vì sao mỗi append là "
    "một (có thể thất bại) phép cấp phát.",
    r"""
## String growable là một dynamic array tí hon

```c
typedef struct {
    char  *data;    /* malloc'd, luôn '\0'-terminated */
    size_t len;     /* số ký tự, không tính '\0' */
    size_t cap;     /* byte đã cấp phát */
} StrBuf;
```

Append là toàn bộ API, và mỗi append là ba việc: chổ chỗ, copy, terminate
— với đường lỗi ở bước một:

```c
int sb_append(StrBuf *b, const char *s) {
    size_t need = b->len + strlen(s) + 1;
    if (need > b->cap) {
        size_t ncap = b->cap ? b->cap : 16;
        while (ncap < need) ncap *= 2;
        char *nd = realloc(b->data, ncap);
        if (!nd) return -1;          /* b->data cũ vẫn hợp lệ! */
        b->data = nd;
        b->cap = ncap;
    }
    memcpy(b->data + b->len, s, strlen(s) + 1);
    b->len += strlen(s);
    return 0;
}
```

Chú ý kỷ luật oom: `realloc` trả NULL **không** free block cũ — giữ con
trỏ, báo lỗi, để caller quyết định. Gán thẳng
`b->data = realloc(b->data, ...)` sẽ leak buffer cũ đúng lúc bộ nhớ đã cạn.

## Lập kế hoạch capacity xấu nhất

`snprintf(NULL, 0, ...)` đo trước, để cấp phát vừa đúng:

```c
int need = snprintf(NULL, 0, "%s: %d", name, value);
char *out = malloc((size_t)need + 1);
snprintf(out, (size_t)need + 1, "%s: %d", name, value);
```

Đo-rồi-cấp-phát là cách format không cần buffer cố định và không truncate.
"""
)

write_lesson(
    M, "tokenize-parse",
    "Tokenizing & Parsing Without Trust",
    "Splitting input you do not control: bounded tokenization, numeric "
    "parsing with full validation, and why atoi is a trap.",
    17,
    r"""
## strtok owns global state — and you cannot see it

```c
char *tok = strtok(line, ",");     /* mutates line, remembers position
                                      in hidden static state */
while (tok) { use(tok); tok = strtok(NULL, ","); }
```

Two problems: the hidden position makes the function unusable across two
concurrent parses, and it *writes `'\0'` into your buffer* — the input is
consumed. ISO C offers nothing reentrant here (`strtok_r` is POSIX, not
standard C). The honest standard-C pattern is a cursor you control:

```c
/* split on ',' without mutating input: report [start,end) spans */
const char *p = line;
while (*p) {
    const char *start = p;
    while (*p && *p != ',') p++;
    /* token = start..p, length p-start */
    if (*p) p++;
}
```

Spans, not mutation: the caller decides what to do with each token, the
input survives, and the loop has no hidden state.

## Numbers from strangers

`atoi("12abc")` returns 12 and shrugs. `atoi` reports *nothing* about
garbage, overflow, or empty input. The validated pattern:

```c
/* parse a nonneg int in [0..999999]; 0 ok, -1 bad */
int parse_bounded(const char *s, long *out) {
    if (!s || !*s) return -1;
    char *end;
    long v = strtol(s, &end, 10);
    if (*end != '\0') return -1;          /* trailing garbage */
    if (v < 0 || v > 999999) return -1;   /* range */
    *out = v;
    return 0;
}
```

`strtol` gives you the end pointer; the discipline is checking every
failure mode: empty, non-numeric tail, overflow (check `errno == ERANGE`
when bounds matter), and your own domain range.
""",
"Tokenize & Parse không tin tưởng",
    "Tách input bạn không kiểm soát: tokenization có giới hạn, parse số "
    "kiểm chứng đầy đủ, và vì sao atoi là cái bẫy.",
    r"""
## strtok sở hữu state toàn cục — bạn không nhìn thấy

```c
char *tok = strtok(line, ",");     /* biến đổi line, nhớ vị trí
                                      trong static state ẩn */
while (tok) { use(tok); tok = strtok(NULL, ","); }
```

Hai vấn đề: vị trí ẩn khiến hàm không dùng được cho hai lần parse song
song, và nó *ghi `'\0'` vào buffer của bạn* — input bị tiêu thụ. ISO C
không có gì reentrant ở đây (`strtok_r` là POSIX, không phải chuẩn). Mẫu
chuẩn-C trung thực là con trỏ cursor bạn tự kiểm soát:

```c
/* tách theo ',' không biến đổi input: báo các span [start,end) */
const char *p = line;
while (*p) {
    const char *start = p;
    while (*p && *p != ',') p++;
    /* token = start..p, độ dài p-start */
    if (*p) p++;
}
```

Span, không biến đổi: caller quyết định làm gì với từng token, input
nguyên vẹn, vòng lặp không có state ẩn.

## Số từ người lạ

`atoi("12abc")` trả 12 và nhún vai. `atoi` không báo gì về rác, tràn số,
hay input rỗng. Mẫu có kiểm chứng:

```c
/* parse int không âm trong [0..999999]; 0 ok, -1 xấu */
int parse_bounded(const char *s, long *out) {
    if (!s || !*s) return -1;
    char *end;
    long v = strtol(s, &end, 10);
    if (*end != '\0') return -1;          /* rác phía sau */
    if (v < 0 || v > 999999) return -1;   /* khoảng */
    *out = v;
    return 0;
}
```

`strtol` cho bạn end pointer; kỷ luật là kiểm mọi chế độ lỗi: rỗng, đuôi
không số, tràn (`errno == ERANGE` khi cần), và khoảng domain của bạn.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p6-copy",
    "Safe Copy Gym",
    "Bounded copies with honest truncation reporting, and a growable string buffer.",
    "Phòng gym copy an toàn",
    "Copy có giới hạn với báo truncation trung thực, và string buffer growable.",
    after_lesson="safe-copying",
    minutes=24,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p6-bounded-copy",
            "A Copy That Reports Truncation",
            """Implement the copy family that never lies:

```c
/* copies src into dst (capacity dstcap).
   Always '\0'-terminates when dstcap > 0.
   Returns: 0 if src + its '\0' fit (exact fit), 1 copied-but-truncated,
   -1 bad args
   (dst NULL, dstcap == 0, or src NULL). src == dst returns 0. */
int copy_bounded(char *dst, size_t dstcap, const char *src);
/* like copy_bounded but only the length that WOULD be needed
   (excluding '\0'); 0 for NULL src */
size_t copy_needed(const char *src);
```""",
            C_PRELUDE + "\n#include <stddef.h>\nint copy_bounded(char *dst, size_t dstcap, const char *src);\nsize_t copy_needed(const char *src);\n",
            [
                (
                    "truncation is reported, not silent",
                    r"""
char buf[8];
CHECK_EQ(copy_bounded(buf, 8, "ok"), 0);
CHECK(!strcmp(buf, "ok"));
CHECK_EQ(copy_bounded(buf, 8, "0123456"), 0);    /* exact fit: 7 + '\0' == 8 */
CHECK(!strcmp(buf, "0123456"));
CHECK_EQ(copy_bounded(buf, 8, "01234567"), 1);   /* 8 chars into 8 bytes: no room for '\0' */
CHECK(!strcmp(buf, "0123456"));                  /* truncated to 7 */
CHECK_EQ(copy_bounded(buf, 8, "0123456789"), 1); /* truncated */
CHECK(!strcmp(buf, "0123456"));                  /* 7 + '\0' */
CHECK_EQ(copy_bounded(NULL, 8, "x"), -1);
CHECK_EQ(copy_bounded(buf, 0, "x"), -1);
CHECK_EQ(copy_bounded(buf, 8, NULL), -1);
char self[4] = "abc";
CHECK_EQ(copy_bounded(self, 4, self), 0);        /* self-copy ok */
CHECK(!strcmp(self, "abc"));
CHECK_EQ(copy_needed("hello"), 5);
CHECK_EQ(copy_needed(NULL), 0);
""",
                    "snprintf gives you both: bounded copy and the would-be length. Careful with src==dst (memcpy overlaps).",
                ),
            ],
        ),
        challenge(
            "cint-p6-strbuf",
            "Build the Growable String",
            """Implement the StrBuf from the lesson. The boilerplate declares:

```c
typedef struct { char *data; size_t len; size_t cap; } StrBuf;
void sb_init(StrBuf *b);                  /* empty but valid; data may be NULL */
int  sb_append(StrBuf *b, const char *s); /* 0 ok, -1 bad args/oom */
void sb_free(StrBuf *b);                  /* ends ownership, back to init state */
```

After append, `data` must be a valid '\0'-terminated string of `len`
characters with room for at least `len + 1` bytes.""",
            C_PRELUDE + "\n#include <stddef.h>\ntypedef struct { char *data; size_t len; size_t cap; } StrBuf;\nvoid sb_init(StrBuf *b);\nint sb_append(StrBuf *b, const char *s);\nvoid sb_free(StrBuf *b);\n",
            [
                (
                    "append, grow, free",
                    r"""
StrBuf b;
sb_init(&b);
CHECK(b.data == NULL || strlen(b.data) == 0);
CHECK_EQ(b.len, 0);
CHECK_EQ(sb_append(&b, "hello"), 0);
CHECK_EQ(sb_append(&b, " "), 0);
CHECK_EQ(sb_append(&b, "world"), 0);
CHECK_EQ(b.len, 11);
CHECK(b.cap >= 12);
CHECK(!strcmp(b.data, "hello world"));
CHECK_EQ(sb_append(NULL, "x"), -1);
CHECK_EQ(sb_append(&b, NULL), -1);
sb_free(&b);
CHECK_EQ(b.len, 0);                       /* back to init state */
CHECK_EQ(sb_append(&b, "again"), 0);      /* reusable after free */
CHECK(!strcmp(b.data, "again"));
sb_free(&b);
""",
                    "realloc with a temp pointer; double the cap starting at 16; append keeps '\0' termination.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p6-bounded-copy": vi_challenge(
            "Copy báo truncation",
            "Cài copy_bounded (0 vừa đúng, 1 bị cắt, -1 sai args, luôn terminate) và copy_needed.",
            [("truncation được báo", "snprintf cho cả hai: bounded copy và độ dài cần.")],
        ),
        "cint-p6-strbuf": vi_challenge(
            "Xây string growable",
            "Cài StrBuf: init/append/free, lỗi -1, reusable sau free.",
            [("append, grow, free", "realloc qua con trỏ tạm; cap nhân đôi từ 16.")],
        ),
    },
    solutions=[
        (
            "cint-p6-bounded-copy",
            r"""
#include <string.h>
#include <stddef.h>
int copy_bounded(char *dst, size_t dstcap, const char *src) {
    if (!dst || dstcap == 0 || !src) return -1;
    size_t slen = strlen(src);
    if (slen + 1 <= dstcap) {
        memmove(dst, src, slen + 1);          /* memmove: src==dst safe */
        return 0;
    }
    if (dstcap > 1) {
        memmove(dst, src, dstcap - 1);
        dst[dstcap - 1] = '\0';
    } else {
        dst[0] = '\0';
    }
    return 1;
}
size_t copy_needed(const char *src) { return src ? strlen(src) : 0; }""",
            r"""
#include <string.h>
#include <stddef.h>
int copy_bounded(char *dst, size_t dstcap, const char *src) {
    if (!dst || !src) return -1;              /* wrong: dstcap==0 accepted */
    size_t slen = strlen(src);
    if (slen <= dstcap) {
        memcpy(dst, src, slen + 1);           /* wrong: slen == dstcap overruns by the '\0' */
        return 0;
    }
    memcpy(dst, src, dstcap);                 /* wrong: no room for '\0' */
    return 1;
}
size_t copy_needed(const char *src) { return src ? strlen(src) + 1 : 0; }  /* wrong: counts '\0' */
""",
        ),
        (
            "cint-p6-strbuf",
            r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
void sb_init(StrBuf *b) {
    if (!b) return;
    b->data = NULL;
    b->len = 0;
    b->cap = 0;
}
int sb_append(StrBuf *b, const char *s) {
    if (!b || !s) return -1;
    size_t slen = strlen(s);
    size_t need = b->len + slen + 1;
    if (need > b->cap) {
        size_t ncap = b->cap ? b->cap : 16;
        while (ncap < need) ncap *= 2;
        char *nd = realloc(b->data, ncap);
        if (!nd) return -1;
        b->data = nd;
        b->cap = ncap;
    }
    if (b->len == 0) b->data[0] = '\0';
    memcpy(b->data + b->len, s, slen + 1);
    b->len += slen;
    return 0;
}
void sb_free(StrBuf *b) {
    if (!b) return;
    free(b->data);
    sb_init(b);
}""",
            r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
void sb_init(StrBuf *b) {
    if (!b) return;
    b->data = NULL; b->len = 0; b->cap = 0;
}
int sb_append(StrBuf *b, const char *s) {
    if (!b || !s) return -1;
    size_t slen = strlen(s);
    size_t need = b->len + slen + 1;
    if (need > b->cap) {
        size_t ncap = b->cap ? b->cap : 16;
        while (ncap < need) ncap *= 2;
        b->data = realloc(b->data, ncap);     /* wrong: old block leaked on failure */
        if (!b->data) return -1;
        b->cap = ncap;
    }
    if (b->len == 0) b->data[0] = '\0';
    memcpy(b->data + b->len, s, slen);        /* wrong: '\0' not copied */
    b->len += slen;
    return 0;
}
void sb_free(StrBuf *b) {
    if (!b) return;
    free(b->data);
    b->data = NULL;                           /* wrong: len/cap left stale */
}""",
        ),
    ],
)

write_practice(
    M, "cint-p6-parse",
    "Parse Gym",
    "Cursor-based tokenization over immutable input, and numeric parsing that rejects garbage.",
    "Phòng gym parse",
    "Tokenization qua cursor trên input bất biến, và parse số từ chối rác.",
    after_lesson="tokenize-parse",
    minutes=24,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p6-span-split",
            "Split Without Mutating",
            """Implement span-based splitting. The boilerplate declares:

```c
typedef struct { const char *start; size_t len; } Span;
/* fills spans (array of capacity cap) with the ','-separated tokens of
   line (NOT modified). Empty tokens ARE reported (len 0).
   Returns the number of spans written, or -1 if more than cap needed. */
int split_spans(const char *line, Span *spans, size_t cap);
```""",
            C_PRELUDE + "\n#include <stddef.h>\ntypedef struct { const char *start; size_t len; } Span;\nint split_spans(const char *line, Span *spans, size_t cap);\n",
            [
                (
                    "spans, not mutation",
                    r"""
const char *line = "alpha,,gamma";
Span sp[4];
int n = split_spans(line, sp, 4);
CHECK_EQ(n, 3);
CHECK(sp[0].len == 5 && !strncmp(sp[0].start, "alpha", 5));
CHECK(sp[1].len == 0);                        /* empty token kept */
CHECK(sp[2].len == 5 && !strncmp(sp[2].start, "gamma", 5));
CHECK(line[0] == 'a');                        /* input untouched */
CHECK_EQ(split_spans("solo", sp, 4), 1);
CHECK_EQ(split_spans("", sp, 4), 0);
CHECK_EQ(split_spans("a,", sp, 4), 2);        /* trailing empty field */
CHECK(sp[1].len == 0);
CHECK_EQ(split_spans("a,b,c", sp, 2), -1);    /* needs 3, cap 2 */
CHECK_EQ(split_spans(NULL, sp, 4), -1);
""",
                    "Walk with a cursor; emit [start, p-start) for each comma-delimited run; count first or fail on overflow.",
                ),
            ],
        ),
        challenge(
            "cint-p6-numbers",
            "Numbers From Strangers",
            """Implement validated numeric parsing:

```c
/* parse a decimal int in [min,max]; 0 ok, -1 on: NULL/empty,
   any non-digit character (leading '-' allowed iff it yields
   a value >= min), or value outside [min,max]. No leading
   whitespace, no '+', no trailing junk. */
int parse_range(const char *s, long min, long max, long *out);
```""",
            C_PRELUDE + "\n#include <stddef.h>\nint parse_range(const char *s, long min, long max, long *out);\n",
            [
                (
                    "every failure mode",
                    r"""
long v;
CHECK_EQ(parse_range("42", 0, 100, &v), 0);
CHECK_EQ(v, 42);
CHECK_EQ(parse_range("-7", -10, 10, &v), 0);
CHECK_EQ(v, -7);
CHECK_EQ(parse_range("007", 0, 100, &v), 0);   /* leading zeros fine */
CHECK_EQ(v, 7);
CHECK_EQ(parse_range("", 0, 10, &v), -1);
CHECK_EQ(parse_range("42abc", 0, 100, &v), -1);
CHECK_EQ(parse_range("  42", 0, 100, &v), -1); /* no whitespace */
CHECK_EQ(parse_range("+42", 0, 100, &v), -1);  /* no '+' */
CHECK_EQ(parse_range("101", 0, 100, &v), -1);  /* out of range */
CHECK_EQ(parse_range("-11", -10, 10, &v), -1);
CHECK_EQ(parse_range("-", 0, 10, &v), -1);     /* lone minus */
CHECK_EQ(parse_range(NULL, 0, 10, &v), -1);
""",
                    "strtol + *end check; but strtol accepts whitespace and '+' — validate the character set yourself, digit by digit.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p6-span-split": vi_challenge(
            "Tách không biến đổi",
            "Cài split_spans: span [start,len), token rỗng vẫn báo, quá cap -> -1, input nguyên vẹn.",
            [("span, không biến đổi", "cursor đi bộ; mỗi run giữa hai dấu phẩy là một span.")],
        ),
        "cint-p6-numbers": vi_challenge(
            "Số từ người lạ",
            "Cài parse_range: từ chối rỗng/rác/whitespace/'+'/ngoài khoảng; '-' chỉ khi kết quả >= min.",
            [("mọi chế độ lỗi", "tự kiểm tập ký tự từng chữ số; strtol chấp nhận whitespace và '+' nên không đủ.")],
        ),
    },
    solutions=[
        (
            "cint-p6-span-split",
            r"""
#include <string.h>
#include <stddef.h>
int split_spans(const char *line, Span *spans, size_t cap) {
    if (!line || !spans) return -1;
    if (*line == '\0') return 0;              /* empty line: no tokens */
    size_t n = 0;
    const char *p = line;
    while (1) {
        const char *start = p;
        while (*p && *p != ',') p++;
        if (n == cap) return -1;
        spans[n].start = start;
        spans[n].len = (size_t)(p - start);
        n++;
        if (*p == '\0') break;
        p++;                       /* skip the comma */
        if (*p == '\0') {          /* trailing comma: one empty token */
            if (n == cap) return -1;
            spans[n].start = p;
            spans[n].len = 0;
            n++;
            break;
        }
    }
    return (int)n;
}""",
            r"""
#include <string.h>
#include <stddef.h>
int split_spans(const char *line, Span *spans, size_t cap) {
    if (!line || !spans) return -1;
    size_t n = 0;
    const char *p = line;
    while (*p) {
        const char *start = p;
        while (*p && *p != ',') p++;
        if (n == cap) return -1;
        spans[n].start = start;
        spans[n].len = (size_t)(p - start);
        n++;
        if (*p) p++;
    }
    return (int)n;                 /* wrong: trailing comma lost, "" -> 0 spans */
}""",
        ),
        (
            "cint-p6-numbers",
            r"""
#include <string.h>
#include <stddef.h>
int parse_range(const char *s, long min, long max, long *out) {
    if (!s || !out || !*s) return -1;
    int neg = 0;
    const char *p = s;
    if (*p == '-') { neg = 1; p++; if (!*p) return -1; }
    long v = 0;
    for (; *p; p++) {
        if (*p < '0' || *p > '9') return -1;
        v = v * 10 + (*p - '0');
        if (v > 1000000000L) return -1;      /* cheap overflow guard */
    }
    if (neg) v = -v;
    if (v < min || v > max) return -1;
    *out = v;
    return 0;
}""",
            r"""
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
int parse_range(const char *s, long min, long max, long *out) {
    if (!s || !out || !*s) return -1;
    char *end;
    long v = strtol(s, &end, 10);   /* wrong: accepts "  42" and "+42" and "42\n" */
    if (*end != '\0' && *end != '\n') return -1;
    if (v < min || v > max) return -1;
    *out = v;
    return 0;
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m6-task",
    "CSV Line Validator & Parser",
    """Implement a one-line CSV parser for the format `name,age,score`
(name: 1..15 non-comma chars; age: 0..130; score: 0..100). The boilerplate
declares:

```c
/* parses exactly three fields. Returns 0 and fills outputs on success.
   Returns -1 on ANY deviation: wrong field count, empty name, name too
   long, non-numeric or out-of-range age/score, trailing junk.
   line is NOT modified. */
int csv_parse(const char *line, char name[16], int *age, int *score);
```""",
    C_PRELUDE + "\n#include <stddef.h>\nint csv_parse(const char *line, char name[16], int *age, int *score);\n",
    [
        (
            "accept the well-formed, reject the rest",
            r"""
char name[16];
int age, score;
CHECK_EQ(csv_parse("ann,30,95", name, &age, &score), 0);
CHECK(!strcmp(name, "ann"));
CHECK_EQ(age, 30);
CHECK_EQ(score, 95);
CHECK_EQ(csv_parse("bob,0,0", name, &age, &score), 0);
CHECK(!strcmp(name, "bob")); CHECK_EQ(age, 0); CHECK_EQ(score, 0);
CHECK_EQ(csv_parse("cat,130,100", name, &age, &score), 0);
CHECK_EQ(csv_parse("ann,30", name, &age, &score), -1);        /* too few */
CHECK_EQ(csv_parse("ann,30,95,extra", name, &age, &score), -1);
CHECK_EQ(csv_parse(",30,95", name, &age, &score), -1);        /* empty name */
CHECK_EQ(csv_parse("0123456789abcdefg,30,95", name, &age, &score), -1); /* 17 chars */
CHECK_EQ(csv_parse("ann,abc,95", name, &age, &score), -1);
CHECK_EQ(csv_parse("ann,131,95", name, &age, &score), -1);    /* age range */
CHECK_EQ(csv_parse("ann,30,101", name, &age, &score), -1);    /* score range */
CHECK_EQ(csv_parse("ann,30.5,95", name, &age, &score), -1);
CHECK_EQ(csv_parse(NULL, name, &age, &score), -1);
""",
            "Two passes: split into exactly 3 spans, then validate each. Reuse your parse discipline digit by digit.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Trình kiểm & parse dòng CSV",
        "Cài csv_parse `name,age,score`: đúng 3 trường, tên 1..15 ký tự, age 0..130, score 0..100, từ chối mọi lệch.",
        [("chấp nhận đúng dạng, từ chối phần còn lại", "hai lượt: tách đúng 3 span rồi kiểm từng trường.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m6",
    "Checkpoint: Parsing Untrusted Input",
    "Prove the full discipline: bounded tokenization, character-set validation, range checks, no mutation.",
    24,
    r"""
## The task

Implement `csv_parse` (see the challenge) for the strict format
`name,age,score`. This is the module's whole argument in one function:
spans instead of mutation, digit-by-digit numeric validation instead of
`atoi`, range checks against your domain, and rejection as the default.

Passing this proves you can take input you do not control and turn it
into values you can trust — the boundary every real program lives at.

Next module: linked data structures — nodes, ownership, and the free-
exactly-once discipline.
""",
    "Kiểm tra: Parse input không tin tưởng",
    "Chứng minh trọn bộ kỷ luật: tokenization có giới hạn, kiểm tập ký tự, kiểm khoảng, không biến đổi.",
    r"""
## Bài toán

Cài `csv_parse` (xem challenge) cho định dạng nghiêm `name,age,score`.
Đây là toàn bộ lập luận của module trong một hàm: span thay vì biến đổi,
kiểm số từng chữ số thay vì `atoi`, kiểm khoảng theo domain, và từ chối
là mặc định.

Vượt qua có nghĩa là bạn biến input mình không kiểm soát thành giá trị
đáng tin — biên giới mà mọi chương trình thật sống ở đó.

Module sau: cấu trúc dữ liệu liên kết — node, ownership, và kỷ luật
free-đúng-một-lần.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <string.h>
#include <stddef.h>
static int parse_num(const char *start, size_t len, long lo, long hi, int *out) {
    if (len == 0) return -1;
    long v = 0;
    for (size_t i = 0; i < len; i++) {
        if (start[i] < '0' || start[i] > '9') return -1;
        v = v * 10 + (start[i] - '0');
        if (v > 1000000L) return -1;
    }
    if (v < lo || v > hi) return -1;
    *out = (int)v;
    return 0;
}
int csv_parse(const char *line, char name[16], int *age, int *score) {
    if (!line || !name || !age || !score) return -1;
    const char *sp[3];
    size_t sl[3];
    int n = 0;
    const char *p = line;
    while (1) {
        const char *start = p;
        while (*p && *p != ',') p++;
        if (n == 3) return -1;                 /* 4+ fields */
        sp[n] = start;
        sl[n] = (size_t)(p - start);
        n++;
        if (*p == '\0') break;
        p++;
        if (*p == '\0') return -1;             /* trailing comma */
    }
    if (n != 3) return -1;                     /* fewer fields */
    if (sl[0] == 0 || sl[0] > 15) return -1;
    if (memchr(sp[0], ',', sl[0])) return -1;  /* cannot happen post-split; belt and braces */
    memcpy(name, sp[0], sl[0]);
    name[sl[0]] = '\0';
    if (parse_num(sp[1], sl[1], 0, 130, age) != 0) return -1;
    if (parse_num(sp[2], sl[2], 0, 100, score) != 0) return -1;
    return 0;
}""",
    wrong=r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
int csv_parse(const char *line, char name[16], int *age, int *score) {
    if (!line || !name || !age || !score) return -1;
    char buf[256];
    snprintf(buf, sizeof buf, "%s", line);
    char *save = buf;
    char *f1 = strtok(save, ",");
    char *f2 = strtok(NULL, ",");
    char *f3 = strtok(NULL, ",");
    if (!f1 || !f2 || !f3) return -1;
    if (!*f1 || strlen(f1) > 15) return -1;
    strcpy(name, f1);
    *age = atoi(f2);      /* wrong: accepts "abc" as 0, "30.5" as 30, " 30" */
    *score = atoi(f3);    /* wrong: no range checks, no junk rejection */
    return 0;             /* wrong: "ann,30,95,extra" wrongly accepted */
}""",
)

print("module 6 complete")
