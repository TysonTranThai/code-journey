#!/usr/bin/env python3
"""C Advanced — batch 1: modules 1 (ca-object-model) and 2 (ca-abstract-machine).

Backslash-free authoring: C statement lines are real newlines; C string-literal
escapes are written as @CE@ and expanded by ca.py's esc() at write time. Every
R/W ledger entry is a COMPLETE standalone program (own includes, helpers from
the prompt defined at file scope, int main(void)) — verified against the
c-runtime harness contract.

write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
"""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ======================== MODULE 1: ca-object-model =========================
M1 = "ca-object-model"

L1A = "ca-objects-and-representation"
L1B = "ca-alignment-padding-layout"
L1C = "ca-implementation-defined-vs-ub"
L1CP = "ca-checkpoint-m1"

write_module(
    M1,
    "The C Object Model",
    "What a C object is at the byte level: representations, alignment, padding, and the behavior classes (unspecified, implementation-defined, undefined) that everything later in this course depends on.",
    "Mô hình đối tượng C",
    "Đối tượng C ở cấp độ byte: biểu diễn, căn chỉnh, đệm và các lớp hành vi (không xác định, do hiện thực định nghĩa, không định nghĩa) mà toàn bộ khóa học dựa vào.",
    [L1A, L1B, L1C, L1CP],
    ["ca-p1-object-size"],
)

write_lesson(
    M1,
    L1A,
    "Objects, Bytes, and Representation",
    "Objects as bytes: representation vs value, and honest platform probing.",
    14,
    """
## Every object is bytes

In C, an **object** is a region of memory that holds a value of some type. The C standard does not say `int` means "a 32-bit two's complement number" — it says `int` has *an object representation* made of `sizeof(int)` bytes, each byte at least 8 bits (`CHAR_BIT`).

Three distinct notions, three different questions:

| Notion | Question | Portable answer? |
| --- | --- | --- |
| Type | What values can this hold? | Yes — from the standard |
| Object representation | Which bytes exist? | `sizeof` only |
| Value representation | Which bits encode the value? | No — implementation-defined |

C23 finally mandates two's complement for signed integers, but width is still implementation-defined: `sizeof(int)` can be 2, 4, or 8 on real platforms.

## Probing your platform honestly

```c
#include <stdio.h>
#include <limits.h>

int main(void) {
    printf("CHAR_BIT = %d@CE@", CHAR_BIT);
    printf("sizeof(int) = %zu@CE@", sizeof(int));
    printf("INT_MIN = %d@CE@", INT_MIN);
    return 0;
}
```

This program is fully portable — it prints *your platform's truth* rather than assuming one.

## Representation is not value

For `unsigned char` (and all unsigned types) every bit pattern is a valid value. For signed integers C23 guarantees two's complement, but still allows padding bits in the representation — bits that exist in the object but participate in no value. `memcpy`-ing an object and inspecting its bytes is always valid; *reading* an int's representation as an int through a reinterpreted pointer is not (that journey starts in the UB module).
""",
    "Đối tượng, byte và biểu diễn",
    "Đối tượng là byte: biểu diễn khác giá trị, và cách đo nền tảng một cách trung thực.",
    """
## Mọi đối tượng đều là byte

Trong C, một **đối tượng** là vùng bộ nhớ chứa giá trị của một kiểu nào đó. Chuẩn C không nói `int` là "số bù 2 32-bit" — nó nói `int` có *biểu diễn đối tượng* gồm `sizeof(int)` byte, mỗi byte ít nhất 8 bit (`CHAR_BIT`).

Ba khái niệm riêng biệt:

| Khái niệm | Câu hỏi | Trả lời khả chuyển? |
| --- | --- | --- |
| Kiểu | Giữ được giá trị nào? | Có — theo chuẩn |
| Biểu diễn đối tượng | Có byte nào? | Chỉ `sizeof` |
| Biểu diễn giá trị | Bit nào mã hóa giá trị? | Không — do hiện thực định nghĩa |

C23 bắt buộc bù 2 cho số nguyên có dấu, nhưng độ rộng vẫn do hiện thực định nghĩa.

## Đo nền tảng của bạn một cách trung thực

Dùng `CHAR_BIT`, `sizeof`, `INT_MIN` để in sự thật của nền tảng thay vì giả định.

## Biểu diễn ≠ giá trị

Với `unsigned char`, mọi bit pattern đều là giá trị hợp lệ. Số nguyên có dấu C23 vẫn cho phép padding bits — bit tồn tại trong đối tượng nhưng không tham gia giá trị.
""",
)

write_lesson(
    M1,
    L1B,
    "Alignment, Padding, and Layout",
    "Why structs have holes: alignment rules, offsetof measurement, layout engineering.",
    16,
    """
## Why structs have holes

Every complete object type has an **alignment requirement**: addresses at which objects of that type may *validly* start. The compiler inserts **padding** between and after members so each member sits at its natural alignment.

```c
struct S {
    char  c;   /* offset 0        */
    /* 3 bytes padding  */
    int   i;   /* offset 4        */
    char  d;   /* offset 8        */
    /* 7 bytes padding  */
};             /* sizeof == 16    */
```

Rules you can rely on (ISO C):

- Members appear in declaration order.
- Each member is aligned to its type's alignment.
- The struct's alignment is the max of its members'.
- `sizeof` is a multiple of the struct's alignment (arrays must still work).

## Measuring, not memorizing

`offsetof` gives the byte offset of each member:

```c
#include <stddef.h>
#include <stdio.h>

struct S { char c; int i; char d; };

int main(void) {
    printf("c at %zu@CE@", offsetof(struct S, c));
    printf("i at %zu@CE@", offsetof(struct S, i));
    printf("d at %zu@CE@", offsetof(struct S, d));
    printf("sizeof = %zu@CE@", sizeof(struct S));
    return 0;
}
```

Reordering members largest-first (`int i; char c; char d;` → sizeof 8) is the classic size win. The exact layout is implementation-defined — but on a fixed platform, like this sandbox, it is *stable and inspectable*, which is what the practice set does.

## Why you care

Padding leaks into files and network protocols; comparing structs with `==` reads padding bytes (unspecified values); `memcpy` of a struct copies the holes. Layout literacy is a systems-programming survival skill.
""",
    "Căn chỉnh, đệm và bố cục",
    "Vì sao struct có lỗ: quy tắc căn chỉnh, đo bằng offsetof, kỹ thuật bố cục.",
    """
## Vì sao struct có lỗ

Mọi kiểu đều có **yêu cầu căn chỉnh**; trình biên dịch chèn **đệm** để mỗi thành phần ngồi đúng căn chỉnh tự nhiên của nó.

Quy tắc có thể dựa vào (ISO C): thành phần theo thứ tự khai báo, mỗi thành phần căn theo căn chỉnh kiểu của nó, căn chỉnh của struct = max của các thành phần, `sizeof` là bội của căn chỉnh struct.

## Đo, đừng học thuộc

`offsetof` cho biết offset byte của từng thành phần. Sắp xếp thành phần lớn-trước là mẹo thu nhỏ kích thước kinh điển. Bố cục chính xác là implementation-defined — nhưng trên một nền tảng cố định như sandbox này, nó **ổn định và đo được**.

## Vì sao quan trọng

Đệm lọt vào file và giao thức mạng; so sánh struct bằng `==` đọc cả byte đệm; `memcpy` struct sao chép cả lỗ.
""",
)

write_lesson(
    M1,
    L1C,
    "The Behavior Map: Unspecified, Implementation-Defined, Undefined",
    "The three behavior classes and the working rule that keeps you off UB.",
    15,
    """
## Three behavior classes — learn them cold

C gives every construct a *contract*. Advanced C is knowing which contract you're standing on:

1. **Implementation-defined**: the implementation must choose, document it, and stay consistent. Example: `sizeof(int)`, whether plain `char` is signed.
2. **Unspecified**: the implementation must pick *some* valid behavior from a set, without documenting which. Example: order of evaluation of function arguments; the value of padding bytes.
3. **Undefined (UB)**: no requirements whatsoever. The compiler may do *anything* — including assuming it never happens, which lets it delete your "safety check".

```c
/* Implementation-defined: -1 or 255 depends on the platform's plain char */
char c = -1;
printf("%d@CE@", c);

/* Unspecified: argument evaluation order */
int i = 0;
printf("%d %d@CE@", i, ++i);    /* DON'T. Order is unspecified. */

/* Undefined: signed overflow. The compiler may assume it can't happen. */
int big = INT_MAX;
int overflowed = big + 1;     /* UB — no wraparound guarantee */
```

## Why UB is not "it crashes"

UB usually does something *quietly reasonable* at -O0 and something *shocking* at -O2, because optimizations are built on the assumption that UB never executes. Deleted null checks, dead branches after overflow, and out-of-bounds accesses that "work" are all the same root cause.

## The working rule

Before shipping a construct, place it on this map. If it's UB, no amount of testing makes it correct — fix the construct, not the test.
""",
    "Bản đồ hành vi",
    "Ba lớp hành vi và quy tắc làm việc giữ bạn khỏi UB.",
    """
## Ba lớp hành vi

1. **Implementation-defined**: hiện thực phải chọn, ghi rõ và giữ nhất quán. Ví dụ: `sizeof(int)`.
2. **Unspecified**: hiện thực chọn *một* hành vi hợp lệ trong tập, không cần ghi rõ. Ví dụ: thứ tự tính giá trị đối số.
3. **Không định nghĩa (UB)**: không ràng buộc gì. Trình biên dịch có thể làm *bất cứ điều gì* — kể cả giả định điều đó không xảy ra.

```c
char c = -1;
printf("%d@CE@", c);            /* tùy nền tảng */

int i = 0;
printf("%d %d@CE@", i, ++i);    /* ĐỪNG. Thứ tự không xác định. */

int big = INT_MAX;
int overflowed = big + 1;     /* UB */
```

## UB không có nghĩa là "nó crash"

UB thường chạy "khá ổn" ở -O0 và "kinh khủng" ở -O2, vì tối ưu hóa dựa trên giả định UB không bao giờ xảy ra.

## Quy tắc làm việc

Đặt mỗi cấu trúc lên bản đồ này. Nếu là UB, kiểm thử không cứu được — sửa cấu trúc, đừng sửa test.
""",
)

write_practice(
    M1,
    "ca-p1-object-size",
    "Object Layout Forensics",
    "Probe representation, layout, and padding on the real platform — measuring, never assuming.",
    "Pháp y bố cục đối tượng",
    "Đo biểu diễn, bố cục và đệm trên nền tảng thật — đo, đừng đoán.",
    L1A,
    18,
    "advanced",
    [
        challenge(
            "ca1-sizes",
            "Report Object Sizes",
            "Implement `void program(void)` that prints the sizes of the fundamental integer types on this platform, one per line:@CE@ @CE@```@CE@char: 1@CE@short: 2@CE@int: 4@CE@long: 8@CE@```@CE@ @CE@Use `sizeof` for each type — your code must compute them, not hard-code numbers.",
            C_PRELUDE,
            [
                ("all four sizes", 'const char* out = cj_capture(program);@CE@CHECK_STR_EQ(out, "char: 1@CE@short: 2@CE@int: 4@CE@long: 8@CE@");', "Four printf calls, each ending with the newline escape; format %zu with sizeof(T). char is 1 by definition."),
                ("deterministic", 'for (int k = 0; k < 3; k++) { const char* out = cj_capture(program); CHECK_STR_EQ(out, "char: 1@CE@short: 2@CE@int: 4@CE@long: 8@CE@"); }', "sizeof is a compile-time constant — repeated runs are identical."),
            ],
            level="imitation",
        ),
        challenge(
            "ca1-layout",
            "Report Struct Layout",
            "Given@CE@ @CE@```c@CE@struct S { char a; int b; char c; };@CE@```@CE@ @CE@implement `void program(void)` that prints each member's offset and the struct size:@CE@ @CE@```@CE@a@0 b@4 c@8 size:12@CE@```@CE@ @CE@Use `offsetof` from `<stddef.h>` and `sizeof` — measure, do not hard-code.",
            "#include <stddef.h>@NL@" + C_PRELUDE,
            [
                ("exact layout line", 'const char* out = cj_capture(program);@CE@CHECK_STR_EQ(out, "a@0 b@4 c@8 size:12@CE@");', "offsetof(struct S, a) is 0; b sits at its 4-byte alignment; trailing padding grows sizeof to a multiple of 4."),
                ("padding detected", 'struct S { char a; int b; char c; };@CE@CHECK_EQ((int)(sizeof(struct S) - (offsetof(struct S, c) + sizeof(char))), 3);', "size minus (last member offset + its size) is exactly the trailing padding."),
                ("compact alternative", 'struct T { int b; char a; char c; };@CE@CHECK_EQ((int)sizeof(struct T), 8);', "Largest-first ordering packs both chars after the int: 4+1+1+2 tail = 8."),
            ],
            level="guided",
        ),
        challenge(
            "ca1-behavior-map",
            "Classify the Contract",
            "Implement `const char* classify(int code)` mapping each code to its standard-contract class for the construct described:@CE@ @CE@- code 0: reading `sizeof(int)` → returns `\"implementation-defined\"`@CE@- code 1: the value of an uninitialized automatic `int` → returns `\"indeterminate\"`@CE@- code 2: signed integer overflow → returns `\"undefined\"`@CE@- code 3: order of evaluation of two function arguments → returns `\"unspecified\"`@CE@- code 4: `unsigned int` wraparound on overflow → returns `\"well-defined\"`@CE@ @CE@Any other code returns `\"unknown\"`.",
            C_PRELUDE,
            [
                ("all six codes", 'CHECK_STR_EQ(classify(0), "implementation-defined");@CE@CHECK_STR_EQ(classify(1), "indeterminate");@CE@CHECK_STR_EQ(classify(2), "undefined");@CE@CHECK_STR_EQ(classify(3), "unspecified");@CE@CHECK_STR_EQ(classify(4), "well-defined");@CE@CHECK_STR_EQ(classify(9), "unknown");', "A plain switch on code; unsigned arithmetic is fully defined modulo 2^N."),
                ("default is unknown", 'CHECK_STR_EQ(classify(-1), "unknown");', "The default case must return the same string for any unrecognized code."),
            ],
            level="independent",
        ),
        challenge(
            "ca1-two-char",
            "Signed or Plain char?",
            "Plain `char` signedness is implementation-defined. On a typical x86-64 Linux box plain char is signed; on this machine it is not — implementation-defined means the platform decides and your code must adapt. Implement `void program(void)` that prints two lines:@CE@ @CE@```@CE@plain char: <signed|unsigned — derived>@CE@min value: <CHAR_MIN>@CE@```@CE@ @CE@Derive BOTH facts at runtime: assign `(char)-1` and compare with -1 (signed) or 255 (unsigned), then print `CHAR_MIN` from `<limits.h>`. Your output here may differ from x86-64 — that difference is the lesson.",
            "#include <limits.h>@NL@" + C_PRELUDE,
            [
                ("derived signedness", 'const char* out = cj_capture(program);@CE@char probe = (char)-1; CHECK_CONTAINS(out, probe == -1 ? "signed" : "unsigned");', "The test derives the platform truth the same way your code must: probe == -1 means signed, probe == 255 means unsigned."),
                ("exact two-line output", 'char probe = (char)-1;@CE@char mn[64];@CE@sprintf(mn, "plain char: %s@CE@min value: %d@CE@", probe == -1 ? "signed" : "unsigned", CHAR_MIN);@CE@CHECK_STR_EQ(cj_capture(program), mn);', "sprintf builds the platform-truth expectation from probe and CHAR_MIN, then the program must match it exactly — hard-coding either line fails somewhere."),
            ],
            level="combination",
        ),
        challenge(
            "ca1-pack-swap",
            "Reorder for Size",
            "The struct@CE@ @CE@```c@CE@struct Blob { char tag; double weight; short qty; char flag; };@CE@```@CE@ @CE@measures 24 bytes here. Implement `size_t packed_size(void)` returning what `sizeof` would be for the best reordering of the same members (largest-first). Define the reordered struct locally and return its `sizeof` — reasoning made executable.",
            C_PRELUDE,
            [
                ("expected packed size", 'CHECK_EQ((int)packed_size(), 16);', "double(8) + short(2) + char(1) + char(1) + 4 tail padding = 16."),
                ("arithmetic matches reality", 'struct Packed { double weight; short qty; char tag; char flag; };@CE@CHECK_EQ((int)packed_size(), (int)sizeof(struct Packed));', "Your function must measure a real struct with exactly the same member set."),
            ],
            level="independent",
        ),
        challenge(
            "ca1-rep-copy",
            "Representation Copy",
            "Implement `unsigned int rep_bytes(double d)` that returns the number of leading zero **bytes** in d's object representation on this little-endian platform. Copy the double's bytes via `memcpy` into an `unsigned char` array, then scan from the highest index (most significant byte) downward while bytes are zero.@CE@ @CE@- `rep_bytes(1.0)` is 0: 1.0 is 0x3FF0000000000000, whose most significant byte (index 7, little-endian) is 0x3F — nonzero, so the scan stops immediately.@CE@- `rep_bytes(0.0)` is 8: every representation byte of +0.0 is zero.@CE@- `rep_bytes(5e-324)` is 7: the smallest positive subnormal is 0x0000000000000001 — its single nonzero byte is index 0, so exactly the seven bytes above it are zero.",
            C_PRELUDE,
            [
                ("1.0 scans from the top", 'CHECK_EQ((int)rep_bytes(1.0), 0);', "1.0 = 0x3FF0...: the most significant byte (index 7) is 0x3F, nonzero, so there are 0 leading zero bytes."),
                ("tiny subnormal", 'CHECK_EQ((int)rep_bytes(5e-324), 7);', "0x0000000000000001: one nonzero byte at index 0, so scanning from index 7 counts seven zero bytes."),
                ("zero is all zeros", 'CHECK_EQ((int)rep_bytes(0.0), 8);', "Every representation byte of +0.0 is zero."),
            ],
            level="independent",
        ),
    ],
    {
        "ca1-sizes": vi_challenge(
            "Kích thước kiểu cơ bản",
            "Cài đặt `void program(void)` in kích thước các kiểu nguyên cơ bản, mỗi kiểu một dòng, dùng `sizeof` — không hard-code số.",
            [
                ("đủ bốn kiểu", "Bốn printf, mỗi cái kết thúc bằng escape xuống dòng; dùng %zu cho sizeof(T). char luôn là 1."),
                ("xác định", "sizeof là hằng thời gian biên dịch — chạy lại giống hệt."),
            ],
        ),
        "ca1-layout": vi_challenge(
            "Bố cục struct",
            "Cho struct S { char a; int b; char c; }, in offset từng thành phần và kích thước struct theo đúng định dạng yêu cầu, dùng `offsetof` và `sizeof`.",
            [
                ("đúng dòng bố cục", "offsetof cho từng thành phần; đệm cuối đưa sizeof lên bội của 4."),
                ("phát hiện đệm", "sizeof trừ (offset thành phần cuối + kích thước của nó) chính là đệm cuối."),
                ("phương án gọn", "Sắp lớn-trước: 4+1+1+2 đệm = 8."),
            ],
        ),
        "ca1-behavior-map": vi_challenge(
            "Phân loại hợp đồng",
            "Cài đặt `const char* classify(int code)` trả về đúng lớp hợp đồng cho từng mã mô tả trong đề.",
            [
                ("đủ sáu mã", "Switch thuần trên code; số nguyên không dấu luôn xác định modulo 2^N."),
                ("mặc định là unknown", "Nhánh mặc định trả cùng một chuỗi cho mã không nhận diện."),
            ],
        ),
        "ca1-two-char": vi_challenge(
            "char có dấu hay không?",
            "In hai dòng đúng định dạng, suy luận cả hai sự kiện lúc chạy: gán (char)-1 để biết dấu (nền tảng này là unsigned), in CHAR_MIN từ limits.h.",
            [
                ("suy luận đúng dấu", "probe == -1 nghĩa là có dấu; probe == 255 là không dấu."),
                ("đầu ra đúng hai dòng", "Tạo kỳ vọng từ probe và CHAR_MIN rồi so khớp chính xác — hard-code chữ sẽ sai trên nền tảng khác."),
            ],
        ),
        "ca1-pack-swap": vi_challenge(
            "Sắp lại cho gọn",
            "Trả về sizeof của phương án sắp lại thành phần tốt nhất (lớn-trước) cho struct Blob — định nghĩa struct sắp lại cục bộ và trả sizeof của nó.",
            [
                ("kích thước mong đợi", "double(8)+short(2)+char(1)+char(1)+4 đệm = 16."),
                ("lý thuyết khớp thực tế", "Hàm phải đo một struct thật có cùng tập thành phần."),
            ],
        ),
        "ca1-rep-copy": vi_challenge(
            "Sao chép biểu diễn",
            "Trả về số byte 0 đứng đầu trong biểu diễn đối tượng của double (memcpy sang unsigned char, quét từ chỉ số cao nhất xuống tới khi gặp byte khác 0).",
            [
                ("1.0 quét từ trên", "1.0 = 0x3FF0...: byte cao nhất (chỉ số 7) là 0x3F khác 0, nên kết quả là 0."),
                ("subnormal nhỏ", "0x0000000000000001: byte khác 0 duy nhất ở chỉ số 0, nên quét từ trên xuống đếm được 7 byte 0."),
                ("zero toàn số 0", "Mọi byte biểu diễn của +0.0 đều bằng 0."),
            ],
        ),
    },
    solutions=[
        (
            "ca1-sizes",
            '#include <stdio.h>@NL@void program(void) {@NL@    printf("char: %zu@CE@", sizeof(char));@NL@    printf("short: %zu@CE@", sizeof(short));@NL@    printf("int: %zu@CE@", sizeof(int));@NL@    printf("long: %zu@CE@", sizeof(long));@NL@}@NL@int main(void) { program(); return 0; }',
            '#include <stdio.h>@NL@void program(void) {@NL@    printf("char: 2@CE@short: 2@CE@int: 4@CE@long: 8@CE@");@NL@}@NL@int main(void) { program(); return 0; }',
        ),
        (
            "ca1-layout",
            '#include <stddef.h>@NL@#include <stdio.h>@NL@struct S { char a; int b; char c; };@NL@void program(void) {@NL@    printf("a@%zu b@%zu c@%zu size:%zu@CE@", offsetof(struct S, a), offsetof(struct S, b), offsetof(struct S, c), sizeof(struct S));@NL@}@NL@int main(void) { program(); return 0; }',
            '#include <stddef.h>@NL@#include <stdio.h>@NL@struct S { char a; int b; char c; };@NL@void program(void) {@NL@    printf("a@0 b@1 c@2 size:6@CE@");@NL@}@NL@int main(void) { program(); return 0; }',
        ),
        (
            "ca1-behavior-map",
            '#include <stdio.h>@NL@const char* classify(int code) {@NL@    switch (code) {@NL@    case 0: return "implementation-defined";@NL@    case 1: return "indeterminate";@NL@    case 2: return "undefined";@NL@    case 3: return "unspecified";@NL@    case 4: return "well-defined";@NL@    default: return "unknown";@NL@    }@NL@}@NL@int main(void) { return 0; }',
            '#include <stdio.h>@NL@const char* classify(int code) {@NL@    switch (code) {@NL@    case 0: return "undefined";@NL@    case 1: return "implementation-defined";@NL@    case 2: return "unspecified";@NL@    case 3: return "indeterminate";@NL@    case 4: return "undefined";@NL@    default: return "undefined";@NL@    }@NL@}@NL@int main(void) { return 0; }',
        ),
        (
            "ca1-two-char",
            '#include <limits.h>@NL@#include <stdio.h>@NL@void program(void) {@NL@    char probe = (char)-1;@NL@    const char *s = (probe == -1) ? "signed" : "unsigned";@NL@    printf("plain char: %s@CE@", s);@NL@    printf("min value: %d@CE@", CHAR_MIN);@NL@}@NL@int main(void) { program(); return 0; }',
            '#include <limits.h>@NL@#include <stdio.h>@NL@void program(void) {@NL@    printf("plain char: unsigned@CE@min value: 255@CE@");@NL@}@NL@int main(void) { program(); return 0; }',
        ),
        (
            "ca1-pack-swap",
            '#include <stddef.h>@NL@size_t packed_size(void) {@NL@    struct Packed { double weight; short qty; char tag; char flag; };@NL@    return sizeof(struct Packed);@NL@}@NL@int main(void) { return 0; }',
            '#include <stddef.h>@NL@size_t packed_size(void) {@NL@    return 24;@NL@}@NL@int main(void) { return 0; }',
        ),
        (
            "ca1-rep-copy",
            '#include <string.h>@NL@unsigned int rep_bytes(double d) {@NL@    unsigned char b[sizeof(double)];@NL@    memcpy(b, &d, sizeof d);@NL@    unsigned int n = 0;@NL@    for (int i = (int)sizeof b - 1; i >= 0 && b[i] == 0; i--) n++;@NL@    return n;@NL@}@NL@int main(void) { return 0; }',
            '#include <string.h>@NL@unsigned int rep_bytes(double d) {@NL@    unsigned char b[sizeof(double)];@NL@    memcpy(b, &d, sizeof d);@NL@    unsigned int n = 0;@NL@    for (int i = (int)sizeof b - 1; i >= 0 && b[i] != 0; i--) n++;@NL@    return n;@NL@}@NL@int main(void) { return 0; }',
        ),
    ],
)

write_lesson(
    M1,
    L1CP,
    "Checkpoint: Reading the Machine",
    "Consolidated layout + behavior-class checkpoint.",
    12,
    """
You can now measure any object's representation, explain its holes, and name its contract. Prove it in one exercise: given a struct, report every member's offset, the size, and the trailing-padding count — all computed at runtime — then classify signed overflow by its contract class.
""",
    "Kiểm tra: Đọc máy",
    "Kiểm tra tổng hợp bố cục + lớp hành vi.",
    """
Bạn đo được biểu diễn bất kỳ đối tượng, giải thích lỗ đệm và gọi tên hợp đồng của từng cấu trúc. Chứng minh trong một bài tập tổng hợp tính lúc chạy.
""",
)

write_checkpoint(
    M1,
    L1CP,
    "Checkpoint: Reading the Machine",
    "Checkpoint for module 1.",
    12,
    "See lesson.",
    "Kiểm tra: Đọc máy",
    "Kiểm tra mô-đun 1.",
    "Xem bài học.",
    challenge(
        "ca1-checkpoint-layout",
        "Checkpoint: Full Layout Report",
        "Given@CE@ @CE@```c@CE@struct Record { char kind; long id; char active; double score; };@CE@```@CE@ @CE@implement `void program(void)` printing exactly one layout line:@CE@ @CE@```@CE@kind@0 id@8 active@16 score@24 size:32 pad:0@CE@```@CE@ @CE@All numbers must come from `offsetof`/`sizeof` measured on a locally defined identical struct (`<stddef.h>`); `pad:` is the *trailing* padding — size minus (last member offset + last member size). Internal padding before `score` is not counted. On a second line, print the contract class of signed overflow by calling `classify_overflow()`, which you also implement and which returns exactly `\"undefined\"`.",
        "#include <stddef.h>@NL@" + C_PRELUDE,
        [
            ("layout line", 'const char* out = cj_capture(program);@CE@CHECK_CONTAINS(out, "kind@0 id@8 active@16 score@24 size:32");', "long is 8-aligned here, so id lands at 8; double at 24; total 32 is already a multiple of 8."),
            ("trailing pad is zero", 'CHECK_CONTAINS(cj_capture(program), "pad:0");', "size 32 minus (offset 24 + 8) = 0 — the 7 missing bytes are INTERNAL padding before score, not trailing."),
            ("overflow class", 'CHECK_CONTAINS(cj_capture(program), "undefined");', "Signed overflow is undefined behavior — print what your own classify_overflow returns."),
        ],
        level="mini-build",
    ),
    {
        "ca1-checkpoint-layout": vi_challenge(
            "Kiểm tra: Báo cáo bố cục đầy đủ",
            "In dòng bố cục đúng định dạng từ offsetof/sizeof đo trên struct thật, dòng đệm cuối (đệm CUỐI, không tính đệm trong), và dòng phân loại tràn số có dấu.",
            [
                ("dòng bố cục", "long căn 8 nên id ở 8; double ở 24; tổng 32 đã là bội của 8."),
                ("đệm cuối bằng 0", "size 32 trừ (offset 24 + 8) = 0 — 7 byte thiếu là đệm TRONG trước score."),
                ("lớp hành vi", "Tràn số có dấu là hành vi không định nghĩa — in kết quả classify_overflow của bạn."),
            ],
        )
    },
    solution='#include <stddef.h>@CE@#include <stdio.h>@CE@struct Record { char kind; long id; char active; double score; };@CE@const char* classify_overflow(void) { return "undefined"; }@CE@void program(void) {@CE@    printf("kind@%zu id@%zu active@%zu score@%zu size:%zu pad:%zu@CE@", offsetof(struct Record, kind), offsetof(struct Record, id), offsetof(struct Record, active), offsetof(struct Record, score), sizeof(struct Record), sizeof(struct Record) - (offsetof(struct Record, score) + sizeof(double)));@CE@    printf("%s@CE@", classify_overflow());@CE@}@CE@int main(void) { program(); return 0; }',
    wrong='#include <stddef.h>@CE@#include <stdio.h>@CE@struct Record { char kind; long id; char active; double score; };@CE@const char* classify_overflow(void) { return "unspecified"; }@CE@void program(void) {@CE@    printf("kind@%zu id@%zu active@%zu score@%zu size:%zu pad:%zu@CE@", offsetof(struct Record, kind), offsetof(struct Record, id), offsetof(struct Record, active), offsetof(struct Record, score), sizeof(struct Record), sizeof(struct Record) - (offsetof(struct Record, score) + sizeof(double)));@CE@    printf("%s@CE@", classify_overflow());@CE@}@CE@int main(void) { program(); return 0; }',
)

# ===================== MODULE 2: ca-abstract-machine ========================
M2 = "ca-abstract-machine"

L2A = "ca-abstract-machine-model"
L2B = "ca-sequencing-side-effects"
L2C = "ca-lvalues-value-objects"
L2CP = "ca-checkpoint-m2"

GIVEN_COUNTERS = (
    C_PRELUDE
    + "static int calls_a = 0, calls_b = 0;@NL@"
    + "static int bump_a(void) { return ++calls_a; }@NL@"
    + "static int bump_b(void) { return ++calls_b; }@NL@"
)

GIVEN_LEAK = (
    C_PRELUDE
    + "static int g_probe = 7;@NL@"
    + "static int *leak_local(void) { int local = g_probe; return &local; }@NL@"
)

write_module(
    M2,
    "The C Abstract Machine",
    "The invisible machine your C code describes: objects, lvalues, sequencing, side effects, and observable behavior — the model the optimizer is allowed to break.",
    "Máy trừu tượng C",
    "Cỗ máy vô hình mà mã C của bạn mô tả: đối tượng, lvalue, thứ tự thực hiện, hiệu ứng phụ và hành vi quan sát được — mô hình mà trình tối ưu hóa được phép phá vỡ.",
    [L2A, L2B, L2C, L2CP],
    ["ca-p2-sequencing"],
)

write_lesson(
    M2,
    L2A,
    "The Machine That Isn't There",
    "The abstract machine, observable behavior, and what optimizers may delete.",
    14,
    """
## C describes a machine; the compiler builds a different one

Your C program is a *description* of an abstract machine: memory cells, sequential execution, each statement's effects finishing before the next begins. The compiler must produce a program with the same **observable behavior** — nothing more. Anything the abstract machine does that you cannot observe may be reordered, fused, or deleted.

Observable behavior is exactly: writes to files, volatile accesses, and (interactively) reads from input streams. Everything else — register use, stack shape, dead stores, pure computations — is the compiler's to optimize.

## What that buys the optimizer

```c
int f(void) {
    int x = 3;
    int y = x * x;      /* no observable effect yet */
    return y;           /* y's computation must happen */
}
/* x's STORE may be deleted entirely: y is computable at compile time,
   and x's memory cell was never observable. */
```

The abstract machine is why "it works when I print it" proves nothing: adding a `printf` adds an observation point, changing what the compiler may keep alive.

## The one-way door

Optimizers are licensed by the standard to *assume* your program never executes undefined behavior. A null check *after* a dereference, an overflow check *after* the addition — these can be legally deleted because the earlier UB "proves" the branch unreachable. Module 4 builds this out in full; here, internalize the principle: **the abstract machine is the contract, the hardware is just an approximation of it.**
""",
    "Cỗ máy không tồn tại",
    "Máy trừu tượng, hành vi quan sát được, và những gì trình tối ưu hóa được xóa.",
    """
## C mô tả một cỗ máy; trình biên dịch dựng một cỗ máy khác

Chương trình C là *mô tả* của máy trừu tượng: ô nhớ, thực hiện tuần tự. Trình biên dịch chỉ cần bảo đảm **hành vi quan sát được** — viết ra file, truy cập volatile, đọc input. Mọi thứ khác có thể sắp xếp lại, gộp hoặc xóa.

## Điều đó mang lại gì cho trình tối ưu hóa

```c
int f(void) {
    int x = 3;
    int y = x * x;
    return y;
}
/* STORE của x có thể bị xóa: y tính được lúc biên dịch,
   ô nhớ của x chưa bao giờ quan sát được. */
```

Đó là lý do "chạy đúng khi thêm printf" không chứng minh gì: printf thêm điểm quan sát, thay đổi những gì trình biên dịch được giữ.

## Cánh cửa một chiều

Trình tối ưu hóa được chuẩn cho phép *giả định* UB không bao giờ xảy ra — vì vậy một lệnh kiểm tra null *sau* khi hủy tham chiếu có thể bị xóa hợp pháp.
""",
)

write_lesson(
    M2,
    L2B,
    "Sequencing, Side Effects, and the Unsequenced Trap",
    "Sequencing points, unsequenced traps, and the review rule that survives.",
    15,
    """
## What is ordered, what is not

Within an expression, C defines *sequencing points* (C11+: *sequenced before* relations):

- `&&`, `||`, `,` (comma operator), `?:` — left side fully evaluated (all side effects done) before right.
- End of a full expression; initializer boundaries.

Everything else — operands of `+`, function **arguments**, subscripts — is **unsequenced relative to each other**.

```c
int i = 0;
int a[2] = {0, 0};
int k = i++ + i++;      /* UB: i modified twice without sequencing */
int j = f() + g();      /* fine, but f/g call order is UNSPECIFIED */
a[i] = i++;             /* UB: unsequenced read and write of i */
```

## The rule that survives code review

If an expression both (1) modifies an object and (2) reads or modifies that same object anywhere else, and those two actions are unsequenced — the program is UB. Not "platform-dependent": undefined.

Splitting into statements is the portable cure:

```c
int t = i++;
a[i] = t;               /* now sequenced: the read of i happens before the store */
```

## Unspecified is not a license either

`f() + g()` is well-defined C, but you cannot know which side runs first. Side effects in unsequenced argument lists (`printf("%d %d", i++, i)`) are not UB — but their output is unpredictable, and relying on it produces real damage.
""",
    "Thứ tự thực hiện và hiệu ứng phụ",
    "Điểm thứ tự thực hiện, bẫy không có thứ tự, và quy tắc review sống sót.",
    """
## Cái gì có thứ tự, cái gì không

Có *sequencing* tại `&&`, `||`, `,`, `?:`; còn toán hạng của `+`, **đối số hàm**, subscript là **không có thứ tự** với nhau.

```c
int i = 0;
int k = i++ + i++;      /* UB: i bị sửa hai lần không có thứ tự */
int j = f() + g();      /* hợp lệ, nhưng thứ tự gọi KHÔNG xác định */
```

## Quy tắc sống sót khi review

Một biểu thức vừa sửa vừa đọc cùng một đối tượng mà không có thứ tự → UB. Tách thành nhiều câu lệnh là cách chữa khả chuyển.

## Unspecified cũng không phải giấy phép

`f() + g()` hợp lệ nhưng bạn không biết bên nào chạy trước. Đặt hiệu ứng phụ vào danh sách đối số không có thứ tự là khó lường — thứ tự không xác định vẫn gây hại thật.
""",
)

write_lesson(
    M2,
    L2C,
    "Lvalues, Value Categories, and Object Lifetime",
    "Lvalues, decay, string-literal lvalue-ness, and object lifetime.",
    14,
    """
## Lvalue vs value

An **lvalue** is an expression that *refers to an object* — it has an address. A non-lvalue is a value: `x` is an lvalue; `x + 1` is not. Assignment needs an lvalue on the left precisely because storing requires an object to store into.

The subtle corners:

- An array expression *decays* to a pointer to its first element — the value is an address, not the array object.
- String literals are lvalues (unnamed arrays of char) — you can take their address, but must not modify them.
- A function designator decays to a function pointer.

```c
int x = 1;
int *p = &x;        /* &x: operand must be an lvalue (or function) */
x + 1 = 3;          /* ERROR: not an lvalue */
"hi"[0] = 'H';      /* compiles; UB at runtime: modifying a literal */
```

## Lifetime begins and ends

An object's **lifetime** — the time during which its representation holds stable values — is fixed by storage duration: automatic objects live their enclosing block; static/allocated objects live until program end or `free`. Accessing an object outside its lifetime (after the block, after free, before initialization) is UB.

The classic dangling case is not exotic — it is *this*:

```c
int *bad(void) {
    int local = 7;
    return &local;      /* lifetime ends at the closing brace */
}
```
""",
    "Lvalue, nhóm giá trị và vòng đời",
    "Lvalue, decay, tính lvalue của string literal, và vòng đời đối tượng.",
    """
## Lvalue và giá trị

**Lvalue** là biểu thức *tham chiếu đến đối tượng* — nó có địa chỉ. Gán cần lvalue bên trái vì lưu trữ cần đối tượng để lưu.

```c
int x = 1;
int *p = &x;        /* &x: toán hạng phải là lvalue */
x + 1 = 3;          /* LỖI: không phải lvalue */
"hi"[0] = 'H';      /* biên dịch được; UB lúc chạy */
```

## Vòng đời bắt đầu và kết thúc

**Vòng đời** của đối tượng do thời lượng lưu trữ quyết định: đối tượng tự động sống theo khối bao quanh; đối tượng tĩnh/cấp phát sống đến hết chương trình hoặc `free`. Truy cập ngoài vòng đời là UB — ví dụ kinh điển: trả về địa chỉ biến cục bộ.
""",
)

write_practice(
    M2,
    "ca-p2-sequencing",
    "Sequencing and Lifetime Drills",
    "Decide sequencing and lifetime questions by building them — each challenge compiles a real program whose answer a test can check.",
    "Bài tập thứ tự và vòng đời",
    "Quyết định câu hỏi sequencing và vòng đời bằng cách dựng chúng — mỗi bài là chương trình thật mà test kiểm tra được.",
    L2A,
    20,
    "advanced",
    [
        challenge(
            "ca2-dangling",
            "Read Inside the Lifetime",
            "The helper below is already in your editor — and it is deliberately buggy:@CE@ @CE@```c@CE@static int g_probe = 7;@CE@static int *leak_local(void) { int local = g_probe; return &local; }@CE@```@CE@ @CE@The pointer it returns is *indeterminate* the moment `local` dies: dereferencing it is UB, and even *comparing* it (say, `leak_local() != 0`) is UB — the optimizer exploits that and folds the check away. Never touch a dangling value. Implement `int safe_read(void)`: the defined counterpart — take the address of an automatic `int` initialized from `g_probe`, dereference the pointer *while the object is alive*, and return the value it reads.",
            GIVEN_LEAK,
            [
                ("defined read", "CHECK_EQ(safe_read(), 7);", "p = &local; return *p; — the read happens before the block ends, so it is perfectly defined."),
                ("matches the probe", "CHECK_EQ(safe_read(), g_probe);", "The defined path must observe exactly g_probe — the same value leak_local *would* have dangled with."),
                ("repeatable", "CHECK_EQ(safe_read(), safe_read());", "A lifetime-correct read is stable; UB is the thing that comes and goes."),
            ],
            level="debugging",
        ),
        challenge(
            "ca2-sequenced-sum",
            "Fix the Unsequenced Sum",
            "This expression is UB: `int k = i++ + i++;`. Implement `int sequenced_sum(int start)` returning the value that `start + (start+1)` computes, but built WITHOUT any unsequenced pair: use temporaries or separate statements. Your submitted source is exposed as `sequenced_sum_src` (a string constant you also define) so the checker can verify it contains no `++` at all.",
            C_PRELUDE,
            [
                ("correct arithmetic", 'CHECK_EQ(sequenced_sum(5), 11);@CE@CHECK_EQ(sequenced_sum(0), 1);@CE@CHECK_EQ(sequenced_sum(-3), -5);', "start + (start + 1): for -3 that is -3 + -2 = -5 — computed via temporaries or separate statements, never two unsequenced ++."),
                ("no increments at all", 'CHECK(strstr(sequenced_sum_src, "++") == 0);', "sequenced_sum_src is the string you define; keep it free of ++ — temporaries need none."),
            ],
            level="debugging",
        ),
        challenge(
            "ca2-observe-folding",
            "Watch the Optimizer Fold",
            "Implement `int folded(void)` whose body computes `21 * 2` through plain automatic locals and returns it. Then implement `int unfolded(void)` doing the same multiplication but through a `volatile int`. Return the difference `folded() - unfolded()`; it must be 0 (folding changes nothing observable), which is the standard's own guarantee.",
            C_PRELUDE,
            [
                ("difference is zero", "CHECK_EQ(folded() - unfolded(), 0);", "Both must compute 42; volatile merely forces a runtime load/store."),
                ("both functions real", "CHECK(folded != 0 && unfolded != 0);", "Both must exist as real, addressable functions — taking their addresses is the observation."),
            ],
            level="guided",
        ),
        challenge(
            "ca2-literal-lvalue",
            "Literals are Lvalues",
            "Implement `size_t literal_addr_delta(void)`: take the address of the string literal `\"ca\"` twice (two separate `&\"ca\"[0]` expressions), return the byte distance between them as a size_t (0 if equal). Then implement `int literal_is_lvalue(void)` returning 1 unconditionally — because taking that address compiled at all, proving literals are lvalues (modifying them would be UB, not a compile error).",
            C_PRELUDE,
            [
                ("addresses comparable", "CHECK_EQ((int)literal_addr_delta(), 0);", "Both expressions designate the same pooled literal on this compiler — distance 0."),
                ("lvalue proof", "CHECK_EQ(literal_is_lvalue(), 1);", "Address-of on a literal only compiles for lvalues."),
            ],
            level="independent",
        ),
        challenge(
            "ca2-order-probe",
            "Unspecified Order, Deterministically Handled",
            "The counters below are already in your editor:@CE@ @CE@```c@CE@static int calls_a = 0, calls_b = 0;@CE@static int bump_a(void) { return ++calls_a; }@CE@static int bump_b(void) { return ++calls_b; }@CE@```@CE@ @CE@Implement `int observed_sum(void)` returning `bump_a() + bump_b()` (one call to each). Then implement `int order_safe(void)` returning the same total but computed in separate statements so it never depends on evaluation order. Also implement `int counters_match_sum(int s)` returning 1 iff `calls_a + calls_b == s`.",
            GIVEN_COUNTERS,
            [
                ("sum is 2 regardless of order", "CHECK_EQ(observed_sum(), 2);", "Both bumps happen before the addition completes; order only affects which returns 1 first."),
                ("counters consistent", "CHECK_EQ(observed_sum(), 2);@CE@CHECK_EQ(counters_match_sum(2), 1);", "Call observed_sum() first so each bump happens exactly once in this process; then 2 is the only consistent total."),
                ("order-safe variant also 2", "CHECK_EQ(order_safe(), 2);", "Sequenced statements give the same observable total — without the unspecified-order risk."),
            ],
            level="combination",
        ),
    ],
    {
        "ca2-dangling": vi_challenge(
            "Đọc trong vòng đời",
            "Con trỏ từ leak_local là *không xác định* sau khi local chết: hủy tham chiếu là UB, kể cả so sánh cũng là UB. Cài `int safe_read(void)`: lấy địa chỉ một biến tự động khởi tạo từ g_probe, hủy tham chiếu *khi đối tượng còn sống*, trả về giá trị.",
            [
                ("đọc hợp lệ", "p = &local; return *p; — phép đọc xảy ra trước khi khối kết thúc."),
                ("khớp probe", "Đường hợp lệ phải quan sát đúng g_probe."),
                ("lặp lại ổn định", "Đọc đúng vòng đời thì ổn định; UB mới là thứ đến rồi đi."),
            ],
        ),
        "ca2-sequenced-sum": vi_challenge(
            "Sửa tổng không có thứ tự",
            "Cài `int sequenced_sum(int start)` trả start + (start+1) mà không có cặp biểu thức không có thứ tự nào; nguồn của bạn được lộ qua `sequenced_sum_src`.",
            [
                ("số học đúng", "Trả start + (start + 1) hoặc tương đương."),
                ("không còn ++", "sequenced_sum_src là chuỗi bạn định nghĩa; giữ không có ++ — biến tạm không cần."),
            ],
        ),
        "ca2-observe-folding": vi_challenge(
            "Quan sát trình tối ưu hóa gập hằng",
            "Cài `folded()` (locals thường) và `unfolded()` (nhân qua volatile); hiệu phải bằng 0 — gập hằng không đổi hành vi quan sát được.",
            [
                ("hiệu bằng không", "Cả hai phải ra 42; volatile chỉ ép load/store lúc chạy."),
                ("cả hai hàm thật", "Cả hai phải tồn tại, lấy địa chỉ được."),
            ],
        ),
        "ca2-literal-lvalue": vi_challenge(
            "Literal là lvalue",
            "Cài `literal_addr_delta()` (khoảng cách giữa hai lần lấy địa chỉ của literal \"ca\") và `literal_is_lvalue()` luôn trả 1.",
            [
                ("địa chỉ so sánh được", "Hai biểu thức chỉ vào cùng literal gộp chung — khoảng cách 0."),
                ("bằng chứng lvalue", "Lấy địa chỉ literal chỉ biên dịch được với lvalue."),
            ],
        ),
        "ca2-order-probe": vi_challenge(
            "Thứ tự không xác định, xử lý tất định",
            "Cài `observed_sum()`, `order_safe()` (tính bằng các câu lệnh riêng) và `counters_match_sum(s)`.",
            [
                ("tổng bằng 2", "Cả hai bump xảy ra trước khi phép cộng hoàn tất."),
                ("bộ đếm nhất quán", "Sau đúng một lần gọi mỗi hàm, tổng là 2."),
                ("biến thể an toàn", "Câu lệnh có thứ tự cho cùng tổng quan sát được."),
            ],
        ),
    },
    solutions=[
        (
            "ca2-dangling",
            GIVEN_LEAK
            + 'int safe_read(void) {@NL@    int local = g_probe;@NL@    int *p = &local;@NL@    return *p;@NL@}@NL@int main(void) { return 0; }',
            GIVEN_LEAK
            + 'int safe_read(void) {@NL@    return g_probe + 1;@NL@}@NL@int main(void) { return 0; }',
        ),
        (
            "ca2-sequenced-sum",
            '#include <stdio.h>@NL@#include <string.h>@NL@const char *sequenced_sum_src =@NL@    "int sequenced_sum(int start) { int a = start; int b = start + 1; return a + b; }";@NL@int sequenced_sum(int start) {@NL@    int a = start;@NL@    int b = start + 1;@NL@    return a + b;@NL@}@NL@int main(void) { return 0; }',
            '#include <stdio.h>@NL@#include <string.h>@NL@const char *sequenced_sum_src =@NL@    "int sequenced_sum(int start) { return start++ + start++; }";@NL@int sequenced_sum(int start) {@NL@    return start++ + start++;@NL@}@NL@int main(void) { return 0; }',
        ),
        (
            "ca2-observe-folding",
            '#include <stdio.h>@NL@int folded(void) {@NL@    int a = 21;@NL@    int b = 2;@NL@    return a * b;@NL@}@NL@int unfolded(void) {@NL@    volatile int a = 21;@NL@    volatile int b = 2;@NL@    return a * b;@NL@}@NL@int main(void) { return 0; }',
            '#include <stdio.h>@NL@int folded(void) {@NL@    int a = 21;@NL@    int b = 2;@NL@    return a * b;@NL@}@NL@int unfolded(void) {@NL@    volatile int a = 21;@NL@    volatile int b = 2;@NL@    return a + b;@NL@}@NL@int main(void) { return 0; }',
        ),
        (
            "ca2-literal-lvalue",
            '#include <stddef.h>@NL@#include <stdio.h>@NL@size_t literal_addr_delta(void) {@NL@    const char *p = &"ca"[0];@NL@    const char *q = &"ca"[0];@NL@    return (size_t)(p > q ? p - q : q - p);@NL@}@NL@int literal_is_lvalue(void) {@NL@    return 1;@NL@}@NL@int main(void) { return 0; }',
            '#include <stddef.h>@NL@#include <stdio.h>@NL@size_t literal_addr_delta(void) {@NL@    return (size_t)-1;@NL@}@NL@int literal_is_lvalue(void) {@NL@    return 0;@NL@}@NL@int main(void) { return 0; }',
        ),
        (
            "ca2-order-probe",
            GIVEN_COUNTERS
            + 'int observed_sum(void) { return bump_a() + bump_b(); }@NL@int order_safe(void) {@NL@    int x = bump_a();@NL@    int y = bump_b();@NL@    return x + y;@NL@}@NL@int counters_match_sum(int s) {@NL@    return (calls_a + calls_b == s) ? 1 : 0;@NL@}@NL@int main(void) { return 0; }',
            GIVEN_COUNTERS
            + 'int observed_sum(void) { return bump_a() + bump_b(); }@NL@int order_safe(void) {@NL@    int x = bump_b();@NL@    int y = bump_a();@NL@    return x - y + 1;@NL@}@NL@int counters_match_sum(int s) {@NL@    return (calls_a - calls_b == s) ? 1 : 0;@NL@}@NL@int main(void) { return 0; }',
        ),
    ],
)

write_lesson(
    M2,
    L2CP,
    "Checkpoint: The Optimizer's Contract",
    "Consolidated observable-behavior checkpoint.",
    12,
    """
Checkpoint for module 2: build a folded computation, make it observable through exactly one channel, and take a pointer *inside* an object's lifetime. One program, three functions, every guarantee from this module in play.
""",
    "Kiểm tra: Hợp đồng của trình tối ưu hóa",
    "Kiểm tra tổng hợp hành vi quan sát được.",
    """
Kiểm tra mô-đun 2: dựng một phép tính gập được, biến nó thành quan sát được qua đúng một kênh, và lấy con trỏ *bên trong* vòng đời đối tượng.
""",
)

write_checkpoint(
    M2,
    L2CP,
    "Checkpoint: The Optimizer's Contract",
    "Prove you know what the abstract machine guarantees and what it leaves to the optimizer: build a pure computation, an observation channel for it, and a lifetime-correct pointer read — all in one program.",
    14,
    "See lesson.",
    "Kiểm tra: Hợp đồng của trình tối ưu hóa",
    "Chứng minh bạn biết máy trừu tượng bảo đảm gì và gì thuộc về trình tối ưu hóa.",
    "Xem bài học.",
    challenge(
        "ca2-checkpoint-observe",
        "Checkpoint: Observable Behavior Only",
        "A static `int g_seen = 0;` is already in your editor. Implement three functions:@CE@ @CE@1. `int pure_compute(int x)` returning `x * 3 + 1`, locals only, no globals touched.@CE@2. `void observe(int x)` storing `pure_compute(x)`'s result into `g_seen`.@CE@3. `int lifetime_alive(int v)` creating an automatic `int`, assigning v, and returning its value read back through a pointer taken while the object is alive.@CE@ @CE@`pure_compute` must remain side-effect free; `observe` is the only thing making the computation observable.",
        C_PRELUDE + "static int g_seen = 0;@NL@",
        [
            ("observe writes 13", "int before = g_seen; observe(4); CHECK_EQ(g_seen, before + 13);", "13 = 4*3+1; observe is what makes the result visible."),
            ("pure stays pure", "g_seen = 100; CHECK_EQ(pure_compute(10), 31); CHECK_EQ(g_seen, 100);", "A direct call must return 31 without touching g_seen."),
            ("read inside lifetime", "CHECK_EQ(lifetime_alive(-7), -7);", "Take the pointer, deref before the block ends."),
        ],
        level="mini-build",
    ),
    {
        "ca2-checkpoint-observe": vi_challenge(
            "Kiểm tra: Chỉ hành vi quan sát được",
            "Có sẵn `static int g_seen = 0;`. Cài ba hàm: pure_compute (thuần), observe (ghi kết quả vào g_seen), lifetime_alive (đọc trong vòng đời).",
            [
                ("observe ghi 13", "13 = 4*3+1; observe là nơi biến kết quả thành quan sát được."),
                ("thuần vẫn thuần", "Gọi trực tiếp phải trả 31 và không đụng g_seen."),
                ("đọc trong vòng đời", "Lấy con trỏ rồi hủy tham chiếu trước khi khối kết thúc."),
            ],
        )
    },
    solution=C_PRELUDE
    + 'static int g_seen = 0;@NL@'
    + 'int pure_compute(int x) {@NL@    int t = x * 3;@NL@    return t + 1;@NL@}@NL@void observe(int x) {@NL@    g_seen = pure_compute(x);@NL@}@NL@int lifetime_alive(int v) {@NL@    int local;@NL@    int *p = &local;@NL@    local = v;@NL@    return *p;@NL@}@NL@int main(void) { return 0; }',
    wrong=C_PRELUDE
    + 'static int g_seen = 0;@NL@'
    + 'int pure_compute(int x) {@NL@    g_seen = x * 3 + 1;@NL@    return x * 3 + 1;@NL@}@NL@void observe(int x) {@NL@    g_seen += pure_compute(x);@NL@}@NL@int lifetime_alive(int v) {@NL@    int local = v;@NL@    return 0;@NL@}@NL@int main(void) { return 0; }',
)
