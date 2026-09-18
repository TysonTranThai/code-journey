#!/usr/bin/env python3
"""C — Intermediate — Module 14: cint-ub.

Undefined behavior as a design concept, not a bogeyman: the optimizer's
license, the categories that matter (signed overflow, out-of-bounds,
lifetime, invalid shifts, indeterminate reads), and how defensive code
is WRITTEN — never how UB is exploited (graded code is always the
well-defined version; Ws are defined-but-wrong behaviors, since UB
cannot be relied on to fail). House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-ub"

write_module(
    M,
    "Undefined Behavior",
    "The optimizer's license: what the standard promises, what it leaves "
    "open, and how correct code stays on the defined side of the line.",
    "Hành vi undefined",
    "Giấy phép của optimizer: chuẩn hứa gì, để ngỏ gì, và code đúng viết "
    "thế nào để ở phía có định nghĩa của đường biên.",
    lessons=["why-ub-exists", "ub-catalog", "defensive-c", "cint-checkpoint-m14"],
    practices=["cint-p14-boundaries", "cint-p14-defensive"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "why-ub-exists",
    "Why Undefined Behavior Exists",
    "UB is not 'random results' — it is the standard telling the optimizer "
    "it may assume you never did it.",
    17,
    r"""
## Three labels, one line

The C standard classifies constructs the compiler cannot reasonably
support:

- **Undefined behavior (UB)** — *no requirements at all*. The compiler
  may assume it never happens: delete the branch, reorder around it,
  invent any result. Signed overflow, out-of-bounds access, use-after-
  free, invalid shifts.
- **Unspecified behavior** — the standard offers a menu of valid
  outcomes and doesn't say which (`f()` and `g()` in `f() + g()` may
  run in either order). Every choice is legal; the program is still
  correct C.
- **Implementation-defined behavior** — the implementation must
  *document* its choice (`sizeof(int)`, char signedness, right-shift of
  negatives).

The distinction matters because the response differs: avoid UB
absolutely, tolerate unspecified by not depending on it, and check the
docs for implementation-defined.

## The optimizer's license

"Assume it never happens" is the part people miss. This is legal:

```c
int sat_add(int a, int b) {
    if (a + b < a) return INT_MAX;   /* intent: overflow check */
    return a + b;                    /* but a + b IS the overflow — UB */
}
```

The compiler sees `a + b < a` and reasons: *overflow is UB, so if we
reached the comparison, no overflow happened, so `a + b >= a` is always
true, so this check is dead code* — and deletes your guard. The check
was written in the language of the very thing it guards against. The
defined way computes in a wider type:

```c
int sat_add(int a, int b) {
    long long r = (long long)a + b;              /* defined: no int overflow */
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
```

## Time-travel is allowed

Because the compiler may reorder freely around UB, a UB operation can
"corrupt" code that *textually precedes* it: the store before the bad
dereference may be sunk past it, the bounds-check after the array write
may be hoisted before it. This is why "it worked when I printed the
value" is not evidence — printing changed the optimization. The only
stable position is: never execute UB, not even once, not even on a
path you "know" is impossible.
""",
"Vì sao UB tồn tại",
    "UB không phải 'kết quả ngẫu nhiên' — là chuẩn nói với optimizer rằng "
    "nó được phép cho rằng bạn chưa từng làm điều đó.",
    r"""
## Ba nhãn, một đường biên

Chuẩn C phân loại các cấu trúc compiler không thể hỗ trợ hợp lý:

- **Hành vi undefined (UB)** — *không yêu cầu gì cả*. Compiler được phép
  cho rằng nó không bao giờ xảy ra: xóa nhánh, sắp xếp lại xuyên qua,
  sáng tạo bất kỳ kết quả nào. Tràn số có dấu, truy cập ngoài biên,
  use-after-free, shift không hợp lệ.
- **Hành vi unspecified** — chuẩn đưa một thực đơn các kết quả hợp lệ và
  không nói chọn cái nào (`f()` và `g()` trong `f() + g()` có thể chạy
  theo thứ tự nào cũng được). Mọi lựa chọn đều hợp pháp; chương trình
  vẫn là C đúng.
- **Hành vi phụ thuộc cài đặt** — cài đặt phải *ghi tài liệu* lựa chọn
  của mình (`sizeof(int)`, char có dấu hay không, shift phải của số âm).

Phân biệt này quan trọng vì cách phản ứng khác nhau: tránh UB tuyệt đối,
chấp nhận unspecified bằng cách không phụ thuộc vào nó, và tra tài liệu
cho implementation-defined.

## Giấy phép của optimizer

"Cho rằng nó không bao giờ xảy ra" là phần mọi người bỏ lỡ. Đây là hợp
pháp:

```c
int sat_add(int a, int b) {
    if (a + b < a) return INT_MAX;   /* ý định: kiểm tra tràn số */
    return a + b;                    /* nhưng a + b CHÍNH LÀ tràn số — UB */
}
```

Compiler nhìn `a + b < a` và suy luận: *tràn số là UB, nên nếu tới được
phép so sánh thì không có tràn số, nên `a + b >= a` luôn đúng, nên phép
kiểm này là code chết* — và xóa bỏ ignoring của bạn. Phép kiểm được viết
bằng ngôn ngữ của chính thứ nó chống lại. Cách có định nghĩa tính trong
kiểu rộng hơn:

```c
int sat_add(int a, int b) {
    long long r = (long long)a + b;              /* có định nghĩa */
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
```

## Du hành thời gian là được phép

Vì compiler được sắp xếp lại tự do quanh UB, một thao tác UB có thể
"làm hỏng" code *đứng trước nó trong văn bản*: phép ghi trước cú
dereference xấu có thể bị chìm xuống sau, phép kiểm biên sau khi ghi
mảng có thể được kéo lên trước. Vì sao "chạy được khi tôi in giá trị"
không phải bằng chứng — việc in đã thay đổi tối ưu hóa. Vị trí ổn định
duy nhất là: không bao giờ chạy UB, dù một lần, dù trên đường "biết
chắc" không thể xảy ra.
"""
)

write_lesson(
    M, "ub-catalog",
    "The Working Catalog",
    "The UB categories you will actually meet: overflow, bounds, lifetime, "
    "shifts, indeterminate reads — with the defined replacement for each.",
    18,
    r"""
## Signed integer overflow

`INT_MAX + 1` is UB — not wraparound. The defined replacements: wider
types (`long long`), pre-checks (`a > INT_MAX - b`), or unsigned
arithmetic where wraparound *is* the defined semantics (`unsigned int`
arithmetic wraps modulo 2³² — that is specified).

## Out-of-bounds access

`a[n]` on an n-element array is UB even to *compute the address
correctly* past the end plus one (the one-past pointer exists; reading
or forming more than one-past does not). String functions that trust
the caller's buffer (`strcpy`, `strcat`, `sprintf`) are UB factories —
the bounded family (`snprintf`, `memcpy` with explicit sizes) is the
replacement.

## Lifetime violations

`use-after-free` (object's lifetime ended), `double free`, returning a
pointer to a local (the local dies at the return). All UB. The
structural fix is ownership discipline (Module 3): every free paired,
every loan documented, every dangling candidate nulled.

## Invalid shifts and indeterminate reads

`x << 32` on a 32-bit int, negative shifts, `1 << 31` *as a signed
int* (overflows) — all UB. Shift amounts must be in `[0, width-1]` and
left operands unsigned when the high bit matters. Reading an automatic
variable never initialized (`int x; use(x);`) is indeterminate — UB in
practice. Initialize everything; `-Wuninitialized` catches what it
can.

## The toolchain helps where it can

Warnings (`-Wall -Wextra -Wpedantic` — this platform's flags) catch the
statically visible slice. UBSan/ASan would catch more, but this
sandbox ships without them — so the *catalog* above is what you carry,
and the discipline is writing the defined form by reflex.
""",
"Danh mục làm việc",
    "Các nhóm UB bạn thực sự gặp: tràn số, biên, lifetime, shift, đọc "
    "không xác định — kèm dạng có định nghĩa thay thế cho từng loại.",
    r"""
## Tràn số có dấu

`INT_MAX + 1` là UB — không phải wraparound. Thay thế có định nghĩa:
kiểu rộng hơn (`long long`), kiểm trước (`a > INT_MAX - b`), hoặc số
học unsigned khi wraparound *chính là* ngữ nghĩa mong muốn (unsigned
wrap modulo 2³² — được chỉ định).

## Truy cập ngoài biên

`a[n]` trên mảng n phần tử là UB dù chỉ *tính địa chỉ* quá một-phần-tử
cuối (con trỏ một-phần-tử tồn tại; đọc hoặc tạo xa hơn thì không). Các
hàm chuỗi tin vào buffer của caller (`strcpy`, `strcat`, `sprintf`) là
nhà máy UB — họ có giới hạn (`snprintf`, `memcpy` với kích thước tường
minh) là thay thế.

## Vi phạm lifetime

`use-after-free` (lifetime đã kết thúc), `double free`, trả con trỏ vào
biến cục bộ (biến cục bộ chết tại return). Đều là UB. Cách chữa cấu
trúc là kỷ luật ownership (Module 3): mỗi free ghép cặp, mỗi khoản mượn
ghi rõ, mọi ứng viên dangling được null.

## Shift không hợp lệ và đọc không xác định

`x << 32` trên int 32-bit, shift âm, `1 << 31` *dưới dạng int có dấu*
(tràn số) — đều UB. Số bit shift phải nằm trong `[0, width-1]` và toán
tử trái là unsigned khi bit cao có ý nghĩa. Đọc biến tự động chưa khởi
tạo (`int x; use(x);`) là không xác định — UB trong thực tế. Khởi tạo
mọi thứ; `-Wuninitialized` bắt được phần nhìn tĩnh được.

## Toolchain giúp được đâu thì giúp

Cảnh báo (`-Wall -Wextra -Wpedantic` — flags của platform này) bắt phần
nhìn tĩnh được. UBSan/ASan bắt thêm được, nhưng sandbox này không có —
nên *danh mục* trên là thứ bạn mang theo, và kỷ luật là viết dạng có
định nghĩa một cách phản xạ.
"""
)

write_lesson(
    M, "defensive-c",
    "Defensive C",
    "The reflexes that keep code on the defined side: pre-checks, bounded "
    "APIs, initialization, and the sanitize-the-input posture.",
    16,
    r"""
## Pre-check instead of post-detect

Every UB trap has a defined-side pre-check:

```c
/* overflow */   if (a > 0 && b > INT_MAX - a) ...
/* shift */      if (k < 32) x = (unsigned)x << k;
/* bounds */     if (i < n) use(a[i]);
/* null */       if (p && p->next) ...
```

The check and the use must be made of *different* operations — checking
`a + b < 0` before computing `a + b` is checking with the UB itself.

## Bounded by default

Every buffer-carrying call names its capacity. `snprintf` over
`sprintf`; `memcpy(dst, src, n)` where n is computed from the
*destination's* capacity, not the source's promise. The bounded call is
never slower by an amount that matters and never the bug's origin.

## Initialize at the declaration

```c
int x = 0;                     /* not "int x;" */
TNode *n = calloc(1, sizeof *n);   /* zeroed: fields have defined values */
char buf[64] = {0};
```

`calloc` for structs whose fields must start defined; explicit
initializers for stack arrays. The cost is unmeasurable; the UB class
it deletes is real.

## The honest test posture

Because UB cannot be *relied on* to fail (it may work on your machine
today), tests assert the *defined replacement's* behavior: sat_add
returns INT_MAX at the boundary, parse rejects the overflow input, the
shift helper clamps. The W-solution pattern in this course is exactly
that: Ws are *defined but wrong* — they misparse, drop, or corrupt in
ways tests deterministically catch. Graded code never depends on UB
failing; it depends on correct behavior being verifiable.
""",
"Phòng thủ trong C",
    "Các phản xạ giữ code ở phía có định nghĩa: kiểm trước, API bounded, "
    "khởi tạo, và tư thế làm sạch input.",
    r"""
## Kiểm trước thay vì phát hiện sau

Mọi bẫy UB có phép kiểm phía-có-định-nghĩa:

```c
/* tràn */   if (a > 0 && b > INT_MAX - a) ...
/* shift */  if (k < 32) x = (unsigned)x << k;
/* biên */   if (i < n) use(a[i]);
/* null */   if (p && p->next) ...
```

Phép kiểm và phép dùng phải là *hai thao tác khác nhau* — kiểm
`a + b < 0` trước khi tính `a + b` là kiểm bằng chính UB.

## Bounded theo mặc định

Mọi lời gọi mang buffer nêu capacity. `snprintf` thay `sprintf`;
`memcpy(dst, src, n)` với n tính từ *capacity của đích*, không phải lời
hứa của nguồn. Lời gọi bounded không chậm hơn đáng kể và không bao giờ
là nguồn gốc bug.

## Khởi tạo ngay tại khai báo

```c
int x = 0;                     /* không phải "int x;" */
TNode *n = calloc(1, sizeof *n);   /* zeroed: các field có giá trị xác định */
char buf[64] = {0};
```

`calloc` cho struct cần field khởi đầu xác định; initializer tường minh
cho mảng stack. Giá phí không đo được; nhóm UB nó xóa là thật.

## Tư thế test trung thực

Vì UB không thể *tin được* là sẽ fail (nó có thể chạy đúng trên máy bạn
hôm nay), test khẳng định hành vi của *dạng thay thế có định nghĩa*:
sat_add trả INT_MAX tại biên, parse từ chối input tràn, helper shift
kẹp số bit. Mẫu W-solution trong khóa học đúng là vậy: W là *có định
nghĩa nhưng sai* — misparse, rơi, hoặc hỏng theo cách test bắt được
một cách all định. Code chấm điểm không bao giờ dựa vào UB sẽ fail; nó
dựa vào hành vi đúng được kiểm chứng.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p14-boundaries",
    "Boundary Gym",
    "Defined-side arithmetic: saturating ops, safe shifts, bounded math.",
    "Phòng gym đường biên",
    "Số học phía-có-định-nghĩa: bão hòa, shift an toàn, toán có giới hạn.",
    after_lesson="ub-catalog",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p14-saturate",
            "Saturating Arithmetic",
            """Implement overflow-proof integer ops. The boilerplate declares:

```c
/* a + b saturated into [INT_MIN, INT_MAX] */
int sat_add(int a, int b);
/* a - b saturated */
int sat_sub(int a, int b);
/* a * b saturated (compute in long long) */
int sat_mul(int a, int b);
/* x << k as unsigned; 0 if k is out of range [0, 31] */
unsigned safe_shl(unsigned x, unsigned k);
```

No signed overflow may occur in your implementation — that is the whole
exercise.""",
            C_PRELUDE + "\n#include <limits.h>\nint sat_add(int a, int b);\nint sat_sub(int a, int b);\nint sat_mul(int a, int b);\nunsigned safe_shl(unsigned x, unsigned k);\n",
            [
                (
                    "the boundaries hold",
                    r"""
CHECK_EQ(sat_add(2, 3), 5);
CHECK_EQ(sat_add(INT_MAX, 1), INT_MAX);
CHECK_EQ(sat_add(INT_MAX, INT_MAX), INT_MAX);
CHECK_EQ(sat_add(INT_MIN, -1), INT_MIN);
CHECK_EQ(sat_add(-5, 5), 0);
CHECK_EQ(sat_sub(INT_MIN, 1), INT_MIN);
CHECK_EQ(sat_sub(5, 8), -3);
CHECK_EQ(sat_mul(INT_MAX, 2), INT_MAX);
CHECK_EQ(sat_mul(INT_MIN, -1), INT_MAX);      /* +2147483648 saturates */
CHECK_EQ(sat_mul(-3, -7), 21);
CHECK_EQ(sat_mul(0, INT_MIN), 0);
CHECK_EQ(safe_shl(1u, 31), 2147483648u);      /* unsigned: defined */
CHECK_EQ(safe_shl(3u, 4), 48u);
CHECK_EQ(safe_shl(1u, 32), 0u);               /* out of range -> 0 */
CHECK_EQ(safe_shl(1u, 100), 0u);
""",
                    "Compute in long long (or unsigned), clamp to [INT_MIN, INT_MAX], cast back. safe_shl: range-check first.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p14-saturate": vi_challenge(
            "Số học bão hòa",
            "Cài sat_add/sat_sub/sat_mul (long long + kẹp biên) và safe_shl (kiểm [0,31]).",
            [("biên giới giữ vững", "tính trong long long, kẹp [INT_MIN, INT_MAX], cast về.")],
        ),
    },
    solutions=[
        (
            "cint-p14-saturate",
            r"""
#include <limits.h>
int sat_add(int a, int b) {
    long long r = (long long)a + b;
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
int sat_sub(int a, int b) {
    long long r = (long long)a - b;
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
int sat_mul(int a, int b) {
    long long r = (long long)a * b;
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
unsigned safe_shl(unsigned x, unsigned k) {
    if (k >= 32) return 0;
    return x << k;
}""",
            r"""
#include <limits.h>
int sat_add(int a, int b) {
    if (a > 0 && b > INT_MAX - a) return INT_MAX;   /* fine... */
    if (a < 0 && b < INT_MIN - a) return INT_MIN;
    return a + b;
}
int sat_sub(int a, int b) {
    long long r = (long long)a - b;
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
int sat_mul(int a, int b) {
    return a * b;              /* wrong: the multiply itself overflows
                                       before any check could run — the
                                       exact bug the lesson forbids */
}
unsigned safe_shl(unsigned x, unsigned k) {
    return x << (k & 31);      /* wrong: silently wraps k (shift 32
                                       becomes shift 0 — a wrong answer
                                       dressed as success) */
}""",
        ),
    ],
)

write_practice(
    M, "cint-p14-defensive",
    "Defensive Gym",
    "Bounded APIs that refuse to trust their callers.",
    "Phòng gym phòng thủ",
    "API bounded từ chối tin caller của mình.",
    after_lesson="defensive-c",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p14-bounded-api",
            "The Untrustworthy API",
            """Implement defensive string/number helpers. The boilerplate
declares:

```c
/* copies at most cap-1 chars + '\0' from src to dst; returns copied
   char count, or -1 if dstcap == 0 / NULL args. NEVER reads more
   than src's length. */
int str_copy_bounded(char *dst, size_t dstcap, const char *src);
/* parses a decimal in [lo, hi]; 0 ok, -1 bad syntax/out-of-range/
   overflow (value must fit long via digit-count guard) */
int num_parse_bounded(const char *s, long lo, long hi, long *out);
/* returns 1 if the n-byte region [p, p+n) is all-zero; 0 otherwise;
   0 if p is NULL and n == 0, -1 if p is NULL and n > 0 */
int region_zero(const unsigned char *p, size_t n);
```""",
            C_PRELUDE + "\n#include <stddef.h>\nint str_copy_bounded(char *dst, size_t dstcap, const char *src);\nint num_parse_bounded(const char *s, long lo, long hi, long *out);\nint region_zero(const unsigned char *p, size_t n);\n",
            [
                (
                    "nothing is trusted",
                    r"""
char buf[8];
CHECK_EQ(str_copy_bounded(buf, 8, "ok"), 2);
CHECK(!strcmp(buf, "ok"));
CHECK_EQ(str_copy_bounded(buf, 8, "too long for eight"), -1 == 0 ? 1 : 7);  /* truncation reported */
CHECK(!strcmp(buf, "too lon"));
CHECK_EQ(str_copy_bounded(NULL, 8, "x"), -1);
CHECK_EQ(str_copy_bounded(buf, 0, "x"), -1);
CHECK_EQ(str_copy_bounded(buf, 8, NULL), -1);
long v;
CHECK_EQ(num_parse_bounded("42", 0, 100, &v), 0); CHECK_EQ(v, 42);
CHECK_EQ(num_parse_bounded("999999999999999999999", 0, 100, &v), -1);  /* overflow guard */
CHECK_EQ(num_parse_bounded("101", 0, 100, &v), -1);
CHECK_EQ(num_parse_bounded("12x", 0, 100, &v), -1);
CHECK_EQ(num_parse_bounded("", 0, 100, &v), -1);
CHECK_EQ(region_zero((const unsigned char *)"\0\0\0", 3), 1);
const unsigned char nz[3] = {0, 1, 0};
CHECK_EQ(region_zero(nz, 3), 0);
CHECK_EQ(region_zero(NULL, 0), 0);
CHECK_EQ(region_zero(NULL, 5), -1);
""",
                    "Copy: scan src, stop at cap-1, always terminate. Parse: digit loop with an upper digit-count bound before multiply. Region: NULL policy per contract.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p14-bounded-api": vi_challenge(
            "API không tin ai",
            "Cài str_copy_bounded, num_parse_bounded (chặn tràn theo số chữ số), region_zero.",
            [("không tin gì cả", "copy: quét src, dừng ở cap-1, luôn terminate. parse: chặn số chữ số trước khi nhân.")],
        ),
    },
    solutions=[
        (
            "cint-p14-bounded-api",
            r"""
#include <string.h>
#include <stddef.h>
int str_copy_bounded(char *dst, size_t dstcap, const char *src) {
    if (!dst || dstcap == 0 || !src) return -1;
    size_t i = 0;
    while (i + 1 < dstcap && src[i] != '\0') {
        dst[i] = src[i];
        i++;
    }
    dst[i] = '\0';
    return (int)i;                 /* copied count; caller sees short copy */
}
int num_parse_bounded(const char *s, long lo, long hi, long *out) {
    if (!s || !out || !*s) return -1;
    int neg = 0;
    const char *p = s;
    if (*p == '-') { neg = 1; p++; if (!*p) return -1; }
    if (*p < '0' || *p > '9') return -1;
    long v = 0;
    int digits = 0;
    for (; *p; p++, digits++) {
        if (*p < '0' || *p > '9') return -1;
        if (digits >= 18) return -1;         /* 18 digits: can't overflow long */
        v = v * 10 + (*p - '0');
    }
    if (neg) v = -v;
    if (v < lo || v > hi) return -1;
    *out = v;
    return 0;
}
int region_zero(const unsigned char *p, size_t n) {
    if (!p) return n == 0 ? 0 : -1;
    for (size_t i = 0; i < n; i++)
        if (p[i] != 0) return 0;
    return 1;
}""",
            r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
int str_copy_bounded(char *dst, size_t dstcap, const char *src) {
    if (!dst || dstcap == 0 || !src) return -1;
    strncpy(dst, src, dstcap);   /* wrong: strncpy does NOT terminate when
                                       src fills the cap — caller's buffer
                                       left unterminated */
    return (int)strlen(src);
}
int num_parse_bounded(const char *s, long lo, long hi, long *out) {
    if (!s || !out || !*s) return -1;
    *out = atol(s);              /* wrong: atol accepts "12x" and overflows
                                       silently far outside [lo,hi] */
    if (*out < lo || *out > hi) return -1;
    return 0;
}
int region_zero(const unsigned char *p, size_t n) {
    if (!p) return 0;            /* wrong: n > 0 with NULL p is an error,
                                       not "nothing to check" */
    for (size_t i = 0; i < n; i++)
        if (p[i] != 0) return 0;
    return 1;
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m14-task",
    "The Safe Expression Evaluator",
    """Assemble the module into one hardened component: an evaluator for
tiny integer expressions that CANNOT exhibit UB on any input. The
boilerplate declares:

```c
/* grammar: NUMBER op NUMBER   (op: + - *)
   input: the expression string; out: the result
   returns 0 ok, -1 on ANY problem: syntax, too long (numbers must fit
   int), intermediate or final overflow (int arithmetic), unknown op.
   All arithmetic is saturating (Module 14 rules); no UB anywhere. */
int eval_expr(const char *s, int *out);
/* saturating helpers from this module's practice (implement them here) */
int sat_add2(int a, int b);
int sat_mul2(int a, int b);
```

Grammar: whitespace allowed around tokens; numbers are unsigned decimal
(fit int, checked); exactly one operator; nothing else.""",
    C_PRELUDE + "\n#include <limits.h>\n#include <stddef.h>\nint eval_expr(const char *s, int *out);\nint sat_add2(int a, int b);\nint sat_mul2(int a, int b);\n",
    [
        (
            "no input can hurt it",
            r"""
int r;
CHECK_EQ(eval_expr("2 + 3", &r), 0); CHECK_EQ(r, 5);
CHECK_EQ(eval_expr("7*6", &r), 0); CHECK_EQ(r, 42);
CHECK_EQ(eval_expr("  10 - 4  ", &r), 0); CHECK_EQ(r, 6);
CHECK_EQ(eval_expr("2147483647 + 1", &r), 0); CHECK_EQ(r, INT_MAX);   /* saturated, defined */
CHECK_EQ(eval_expr("2147483647 * 2", &r), 0); CHECK_EQ(r, INT_MAX);
CHECK_EQ(eval_expr("-5 - 3", &r), -1);        /* no unary minus in grammar */
CHECK_EQ(eval_expr("1 / 2", &r), -1);         /* unknown op */
CHECK_EQ(eval_expr("99999999999 + 1", &r), -1);  /* number doesn't fit int */
CHECK_EQ(eval_expr("1 +", &r), -1);
CHECK_EQ(eval_expr("+ 1", &r), -1);
CHECK_EQ(eval_expr("", &r), -1);
CHECK_EQ(eval_expr(NULL, &r), -1);
CHECK_EQ(eval_expr("1 + 2", NULL), -1);
""",
            "Tokenize strictly, parse numbers with a digit-count guard, apply saturating ops, never compute an overflowing expression.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Bộ đánh giá biểu thức an toàn",
        "Cài eval_expr: NUMBER op NUMBER, số học bão hòa, từ chối mọi thứ lệch — không UB với input nào.",
        [("không input nào làm nó tổn thương", "tokenize nghiêm, parse số có chặn số chữ số, áp dụng op bão hòa.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m14",
    "Checkpoint: The Unbreakable Evaluator",
    "Prove the discipline: an arithmetic evaluator that stays defined on every possible input.",
    30,
    r"""
## The task

Implement `eval_expr` (see the challenge). Every graded case is a
boundary: saturation at INT_MAX, a number that does not fit, a malformed
grammar, NULL arguments. A "works on my machine" evaluator that computes
`2147483647 + 1` in int arithmetic would be UB — and UB cannot be
trusted to fail the tests; that is precisely why the defined, saturating
implementation is the only passing one.

Passing this proves the module's thesis in one component: you can write
C that processes arbitrary input with a *proof-shaped* guarantee — no
input can push it off the defined side.

Next module: threads — making multiple things happen at once, safely.
""",
    "Kiểm tra: Bộ đánh giá không thể phá",
    "Chứng minh kỷ luật: một bộ đánh giá số học luôn ở phía có định nghĩa với mọi input.",
    r"""
## Bài toán

Cài `eval_expr` (xem challenge). Mọi trường hợp chấm điểm là một đường
biên: bão hòa tại INT_MAX, số không vừa, grammar méo, tham số NULL. Bộ
đánh giá "chạy đúng trên máy tôi" mà tính `2147483647 + 1` bằng int là
UB — và UB không thể tin là sẽ fail test; chính vì thế cài đặt bão hòa,
có định nghĩa mới là duy nhất vượt qua.

Vượt qua chứng minh luận điểm của module trong một thành phần: bạn viết
được C xử lý input tùy ý với đảm bảo *dạng-chứng-minh* — không input nào
đẩy nó khỏi phía có định nghĩa.

Module sau: thread — làm nhiều việc cùng lúc, an toàn.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <string.h>
#include <limits.h>
#include <stddef.h>
int sat_add2(int a, int b) {
    long long r = (long long)a + b;
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
int sat_mul2(int a, int b) {
    long long r = (long long)a * b;
    if (r > INT_MAX) return INT_MAX;
    if (r < INT_MIN) return INT_MIN;
    return (int)r;
}
static int parse_uint(const char *s, size_t len, int *out) {
    if (len == 0 || len > 10) return -1;
    long v = 0;
    for (size_t i = 0; i < len; i++) {
        if (s[i] < '0' || s[i] > '9') return -1;
        v = v * 10 + (s[i] - '0');
    }
    if (v > INT_MAX) return -1;
    *out = (int)v;
    return 0;
}
int eval_expr(const char *s, int *out) {
    if (!s || !out) return -1;
    int a, b;
    char op = 0;
    size_t i = 0;
    while (s[i] == ' ') i++;
    size_t start = i;
    while (s[i] && s[i] != ' ' && s[i] != '+' && s[i] != '-' && s[i] != '*') i++;
    if (parse_uint(s + start, i - start, &a) != 0) return -1;
    while (s[i] == ' ') i++;
    if (s[i] != '+' && s[i] != '-' && s[i] != '*') return -1;
    op = s[i++];
    while (s[i] == ' ') i++;
    start = i;
    while (s[i] && s[i] != ' ' && s[i] != '+' && s[i] != '-' && s[i] != '*') i++;
    if (parse_uint(s + start, i - start, &b) != 0) return -1;
    while (s[i] == ' ') i++;
    if (s[i] != '\0') return -1;               /* trailing junk */
    if (op == '+') { *out = sat_add2(a, b); return 0; }
    if (op == '-') { *out = sat_add2(a, -b); return 0; }   /* -b: b <= INT_MAX,
                                                  so -b overflows only when
                                                  b == INT_MIN — impossible
                                                  here since b >= 0 */
    *out = sat_mul2(a, b);
    return 0;
}""",
    wrong=r"""
#include <string.h>
#include <limits.h>
#include <stdlib.h>
#include <stddef.h>
int sat_add2(int a, int b) {
    return a + b;                /* wrong: signed overflow IS the operation —
                                       undefined, not saturating */
}
int sat_mul2(int a, int b) {
    return a * b;                /* wrong: same */
}
int eval_expr(const char *s, int *out) {
    if (!s || !out) return -1;
    int a = atoi(s);             /* wrong: atoi stops at the op, accepts
                                       "12x", overflows silently */
    while (*s >= '0' && *s <= '9') s++;
    while (*s == ' ') s++;
    char op = *s++;
    while (*s == ' ') s++;
    int b = atoi(s);
    switch (op) {
    case '+': *out = a + b; return 0;      /* wrong: UB on overflow */
    case '-': *out = a - b; return 0;
    case '*': *out = a * b; return 0;
    default: return -1;
    }
}""",
)

print("module 14 complete")
