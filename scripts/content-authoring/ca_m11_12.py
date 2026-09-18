#!/usr/bin/env python3
"""C Advanced — batch 6: modules 11 (elf-linking) and 12 (abi-layout).
Zero-backslash authoring: @NL@ = statement separator, @CE@ = newline escape
inside C string literals."""
from ca import (
    C_PRELUDE,
    POSIX_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ======================= MODULE 11: ca-elf-linking ==========================
M11 = "ca-elf-linking"

L11A = "ca-elf-sections"
L11B = "ca-linker-at-work"
L11CP = "ca-checkpoint-m11"

write_module(
    M11,
    "Object Files, ELF, and the Linker",
    "Sections, symbol tables, and relocation — inspecting real binaries with nm and objdump, and driving the linker by hand.",
    "Object file, ELF, và Linker",
    "Section, bảng ký hiệu, và relocation — soi binary thật bằng nm và objdump, và điều khiển linker bằng tay.",
    [L11A, L11B, L11CP],
    ["ca-p11-elf"],
)

write_lesson(
    M11,
    L11A,
    "Sections and Their Contents",
    "What .text, .data, .bss, and .rodata actually hold — verified with size and nm on a live binary.",
    16,
    """
## Every byte of a program lives in a section

- **.text** — executable code. Read-only at runtime; self-modifying it is UB and modern kernels enforce it.
- **.data** — initialized globals (`int x = 5;`). Occupies file space.
- **.bss** — zero-initialized globals (`int y;`). Occupies *no file space*: the loader simply zeroes pages at load. A million-byte `static char big[1000000];` costs nothing on disk.
- **.rodata** — string literals and const data. Your `"hello"` literals live here; writing to them is the UB from module 2.

`size a.out` prints the totals; `nm a.out` lists which symbol landed where (the T/D/B letters from module 10).

## Relocation: why .o files are not runnable

An object file's calls and global references are *placeholders* — the final addresses do not exist until the linker lays sections out. Relocation entries record 'patch this byte sequence with the address of that symbol'. That is why linking two objects fixes what compiling them separately could not.
""",
    "Section và nội dung của chúng",
    "Mảng .text, .data, .bss, và .rodata thực sự giữ gì — xác minh bằng size và nm trên binary sống.",
    """
## Mọi byte của chương trình nằm trong một section

- **.text** — code chạy được. Chỉ đọc lúc chạy; tự sửa nó là UB và kernel hiện đại cưỡng chế điều đó.
- **.data** — global có khởi tạo (`int x = 5;`). Chiếm chỗ trong file.
- **.bss** — global khởi tạo 0 (`int y;`). KHÔNG chiếm chỗ trong file: loader chỉ cần zero các trang lúc load. `static char big[1000000];` tốn đúng 0 trên đĩa.
- **.rodata** — string literal và dữ liệu const. Các literal của bạn nằm đây; ghi vào là UB của mô-đun 2.

`size a.out` in tổng; `nm a.out` liệt kê ký hiệu nào rơi vào đâu (các chữ T/D/B của mô-đun 10).

## Relocation: vì sao .o không chạy được

Lời gọi và tham chiếu global trong object file là *placeholder* — địa chỉ cuối không tồn tại đến khi linker bố trí các section. Relocation entry ghi lại 'vá chuỗi byte này bằng địa chỉ của ký hiệu kia'. Vì vậy liên kết hai object giải quyết được điều biên dịch riêng lẻ không thể.
""",
)

write_lesson(
    M11,
    L11B,
    "Driving the Linker",
    "Building two objects and an archive by hand, watching symbol resolution fail and succeed — inside the sandbox, with the real toolchain.",
    16,
    """
## A two-file program linked by hand

```c
/* counter.c */  int counter = 5; int bump(void) { return ++counter; }
/* main.c   */  int bump(void); int main(void) { return bump(); }
```

`gcc -c counter.c main.c` produces two objects; `gcc main.o counter.o -o prog` resolves `bump` across the boundary. Reverse the link order with an archive and resolution semantics show their teeth: `ar rcs libcnt.a counter.o` then `gcc main.o -L. -lcnt -o prog` works, while `gcc -L. -lcnt main.o` can fail — the archive is scanned when the linker reaches it, and `main.o`'s undefined `bump` must already be pending.

## What the linker does for you

Merges like sections, assigns final addresses, patches relocations, and drops archive members that resolve nothing. Static libraries are not 'included' — they are *searched*, member by member, for currently-undefined symbols.

## Shared objects versus static archives

A .so is loaded at runtime and symbol-lookup happens then (or at load with binding); a .a is copied into the binary at link time. The sandbox links statically here — but the resolution model you practice (pending U, defining T) is the same machine both use.
""",
    "Điều khiển linker",
    "Dựng hai object và một archive bằng tay, xem giải quyết ký hiệu hụt và thành — ngay trong sandbox, với toolchain thật.",
    """
## Chương trình hai file liên kết bằng tay

```c
/* counter.c */  int counter = 5; int bump(void) { return ++counter; }
/* main.c   */  int bump(void); int main(void) { return bump(); }
```

`gcc -c counter.c main.c` tạo hai object; `gcc main.o counter.o -o prog` giải quyết `bump` xuyên biên giới. Đảo thứ tự liên kết với archive và ngữ nghĩa resolution lộ răng: `ar rcs libcnt.a counter.o` rồi `gcc main.o -L. -lcnt -o prog` chạy, còn `gcc -L. -lcnt main.o` có thể hụt — archive được quét khi linker chạm tới nó, và `bump` của `main.o` phải đang chờ trước đó.

## Linker làm gì cho bạn

Gộp các section cùng loại, gán địa chỉ cuối, vá relocation, và bỏ thành viên archive không giải quyết gì. Thư viện tĩnh không bị 'nhúng vào' — chúng bị *tìm kiếm*, thành viên một thành viên, cho các ký hiệu đang undefined.

## Shared object so với archive tĩnh

.so được nạp lúc chạy và tra ký hiệu xảy ra lúc đó; .a được sao chép vào binary lúc liên kết. Sandbox ở đây liên kết tĩnh — nhưng mô hình resolution bạn luyện (U đang chờ, T định nghĩa) là cùng một cỗ máy mà cả hai dùng.
""",
)

write_practice(
    M11,
    "ca-p11-elf",
    "Binary Forensics Drills",
    "Drive gcc, ar, nm, and size inside the sandbox: compile objects, build archives, resolve symbols — the linker as a lab instrument.",
    "Bài tập pháp y binary",
    "Điều khiển gcc, ar, nm, và size ngay trong sandbox: biên dịch object, dựng archive, giải quyết ký hiệu — linker làm dụng cụ thí nghiệm.",
    L11A,
    24,
    "advanced",
    [
        challenge(
            "ca11-ctor-order",
            "Initialization Across Units",
            "A file-scope `int stage = 1;` is already in your editor. Implement `int advance(void)` (returns the old stage, then increments it) and `int current_stage(void)`. The test program below links as one unit, but your functions model what cross-object globals do: file-scope state lives once, and every caller sees the same object — simulate and confirm.",
            C_PRELUDE + "int stage = 1;@NL@",
            [
                ("shared state advances", "CHECK_EQ(advance(), 1);@NL@CHECK_EQ(advance(), 2);@NL@CHECK_EQ(current_stage(), 3);", "Each call reads and writes the same file-scope object — exactly what two objects linked against one definition share."),
            ],
            level="guided",
        ),
        challenge(
            "ca11-nm-forensics",
            "Forensics by Symbol Table",
            "Implement `char classify_symbol(const char *line)` parsing one `nm` output line like '0000000000401100 T bump' — return the type letter. Then implement `int is_defined(char t)` returning 1 for T/t/D/d/B/b/R/r and 0 for U/u/w/v.",
            C_PRELUDE,
            [
                ("parses the letter", "CHECK_EQ(classify_symbol(\"0000000000401100 T bump\"), 'T');@NL@CHECK_EQ(classify_symbol(\"                 U printf\"), 'U');", "A single-letter first field means the symbol is undefined (no address column); otherwise the letter follows the address."),
                ("defined vs not", "CHECK_EQ(is_defined('T'), 1);@NL@CHECK_EQ(is_defined('t'), 1);@NL@CHECK_EQ(is_defined('U'), 0);@NL@CHECK_EQ(is_defined('w'), 0);", "Lowercase defined letters (t/d/b/r) are file-local but still defined; U/u/w/v are resolution debts."),
            ],
            level="independent",
        ),
        challenge(
            "ca11-archive-model",
            "Model Archive Resolution",
            "Implement the linker's archive scan as a function:@CE@ @CE@```c@CE@typedef struct { int defines[8]; size_t ndefs; } member_t;@CE@int member_pulls(const member_t *m, const int *pending, size_t npending);@CE@```@CE@ @CE@Return 1 iff any of the member's defined symbols appears in the pending list — the pull-in rule from module 10, now executable against arbitrary tables.",
            C_PRELUDE,
            [
                ("resolving member is pulled", "member_t m = {{0}};@NL@int d[2] = {30, 31};@NL@m.ndefs = 2;@NL@m.defines[0] = 30;@NL@m.defines[1] = 31;@NL@int pend[2] = {31, 44};@NL@CHECK_EQ(member_pulls(&m, pend, 2), 1);", "The member defines 31, which is pending: pull it in."),
                ("useless member stays", "member_t m2 = {{0}};@NL@int d2[1] = {90};@NL@m2.ndefs = 1;@NL@m2.defines[0] = 90;@NL@int pend2[1] = {31};@NL@CHECK_EQ(member_pulls(&m2, pend2, 1), 0);", "No overlap: the member is never copied into the binary."),
            ],
            level="combination",
        ),
        challenge(
            "ca11-two-unit-link",
            "Link Two Units by Hand",
            "Implement `int cross_unit_total(void)` that calls two of your own functions declared in a header-style block *above* their definitions' use (prototype `int part_a(void); int part_b(void);`) and returns their sum. This is the one-TU rehearsal of the two-object link: declarations satisfy the compiler, definitions satisfy the linker.",
            C_PRELUDE,
            [
                ("declarations then definitions", "CHECK_EQ(cross_unit_total(), 30);", "part_a returns 10, part_b returns 20: the prototypes bind calls to definitions exactly as the linker does across objects."),
            ],
            level="guided",
        ),
    ],
    {
        "ca11-ctor-order": vi_challenge(
            "Khởi tạo xuyên đơn vị",
            "Có sẵn `int stage = 1;`. Cài advance() (trả giá trị cũ rồi tăng) và current_stage() — trạng thái file-scope là một đối tượng duy nhất mọi caller cùng thấy.",
            [
                ("trạng thái chung tiến lên", "Mỗi lần gọi đọc và ghi cùng một đối tượng file-scope — đúng điều hai object liên kết với một định nghĩa chia sẻ."),
            ],
        ),
        "ca11-nm-forensics": vi_challenge(
            "Pháp y qua bảng ký hiệu",
            "Cài classify_symbol(line) trích chữ loại từ một dòng nm, và is_defined(t) phân loại chữ đã định nghĩa hay chưa.",
            [
                ("trích chữ", "Chữ loại là trường phân tách bằng khoảng trắng thứ ba."),
                ("định nghĩa hay chưa", "Chữ thường (t/d/b/r) vẫn là đã định nghĩa dù chỉ trong file; U/u/w/v là khoản nợ resolution."),
            ],
        ),
        "ca11-archive-model": vi_challenge(
            "Mô hình resolution của archive",
            "Cài member_pulls: trả 1 khi có ký hiệu định nghĩa nào của thành viên nằm trong danh sách chờ — luật pull-in trở nên chạy được.",
            [
                ("thành viên giải quyết được thì bị kéo", "Thành viên định nghĩa 31 đang chờ: kéo vào."),
                ("thành viên vô dụng ở lại", "Không giao nhau: thành viên không bao giờ được sao chép vào binary."),
            ],
        ),
        "ca11-two-unit-link": vi_challenge(
            "Liên kết hai đơn vị bằng tay",
            "Cài cross_unit_total() gọi part_a() + part_b() qua prototype phía trên — diễn tập một-TU của liên kết hai object.",
            [
                ("khai báo rồi định nghĩa", "Prototype gắn lời gọi vào định nghĩa đúng như linker làm xuyên object."),
            ],
        ),
    },
    solutions=[
        (
            "ca11-ctor-order",
            C_PRELUDE
            + "int stage = 1;@NL@"
            + "int advance(void) { int old = stage; stage++; return old; }@NL@"
            + "int current_stage(void) { return stage; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int stage = 1;@NL@"
            + "int advance(void) { stage = stage + 10; return stage; }@NL@"
            + "int current_stage(void) { return stage; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca11-nm-forensics",
            C_PRELUDE
            + "#include <ctype.h>@NL@char classify_symbol(const char *line) {@NL@    const char *p = line;@NL@    while (*p && isspace((unsigned char)*p)) p++;@NL@    const char *f0 = p;@NL@    while (*p && !isspace((unsigned char)*p)) p++;@NL@    size_t len0 = (size_t)(p - f0);@NL@    if (len0 == 1) return f0[0];@NL@    while (*p && isspace((unsigned char)*p)) p++;@NL@    return *p ? *p : 0;@NL@}@NL@"
            + "int is_defined(char t) {@NL@    switch (t) {@NL@    case 'T': case 't': case 'D': case 'd': case 'B': case 'b': case 'R': case 'r': return 1;@NL@    default: return 0;@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "char classify_symbol(const char *line) {@NL@    return line[1];@NL@}@NL@"
            + "int is_defined(char t) {@NL@    switch (t) {@NL@    case 'T': case 't': case 'D': case 'd': case 'B': case 'b': case 'R': case 'r': return 1;@NL@    default: return 0;@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca11-archive-model",
            C_PRELUDE
            + "typedef struct { int defines[8]; size_t ndefs; } member_t;@NL@"
            + "int member_pulls(const member_t *m, const int *pending, size_t npending) {@NL@    for (size_t i = 0; i < m->ndefs; i++) {@NL@        for (size_t j = 0; j < npending; j++) {@NL@            if (m->defines[i] == pending[j]) return 1;@NL@        }@NL@    }@NL@    return 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "typedef struct { int defines[8]; size_t ndefs; } member_t;@NL@"
            + "int member_pulls(const member_t *m, const int *pending, size_t npending) {@NL@    (void)pending; (void)npending;@NL@    return (m->ndefs > 0) ? 1 : 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca11-two-unit-link",
            C_PRELUDE
            + "int part_a(void);@NL@int part_b(void);@NL@"
            + "int part_a(void) { return 10; }@NL@"
            + "int part_b(void) { return 20; }@NL@"
            + "int cross_unit_total(void) { return part_a() + part_b(); }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int part_a(void);@NL@int part_b(void);@NL@"
            + "int part_a(void) { return 10; }@NL@"
            + "int part_b(void) { return 20; }@NL@"
            + "int cross_unit_total(void) { return part_a() - part_b(); }@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

# ========================= MODULE 12: ca-abi-layout =========================
M12 = "ca-abi-layout"

L12A = "ca-calling-conventions"
L12B = "ca-struct-layout-abi"
L12CP = "ca-checkpoint-m12"

write_module(
    M12,
    "ABI and Binary Compatibility",
    "Calling conventions, struct layout, and the stable-interface contract — why two separately compiled files agree, and when they stop.",
    "ABI và tương thích nhị phân",
    "Quy ước gọi, bố cục struct, và hợp đồng giao diện ổn định — vì sao hai file biên dịch riêng vẫn hiểu nhau, và khi nào chúng ngừng hiểu.",
    [L12A, L12B, L12CP],
    ["ca-p12-abi"],
)

write_lesson(
    M12,
    L12A,
    "Calling Conventions",
    "Where arguments go, who saves what, and why the ABI is a contract between compilers, not a language guarantee.",
    15,
    """
## The invisible agreement

When you call a function, both sides agree — without any C syntax saying so — where each argument travels (registers first, then stack), which register returns the value, and which registers the callee must restore. That agreement is the **calling convention**, the core of the platform ABI.

## Caller-saved versus callee-saved

Registers the *callee* may freely scratch are caller-saved: if the caller still needs the value, it must spill it before the call. Registers the callee promises to preserve are callee-saved: the callee spills and restores them. This division is why adding a call can change register allocation in the caller — visible in module 13's disassembly.

## Variadic functions break the pattern on purpose

printf-style functions take a runtime-shaped argument list. `<stdarg.h>` (va_start/va_arg/va_end) is the standard's portable window onto whatever the convention actually did — and the reason printf is a special beast for every ABI ever designed.
""",
    "Quy ước gọi",
    "Đối số đi đâu, ai lưu cái gì, và vì sao ABI là hợp đồng giữa các trình biên dịch chứ không phải bảo đảm của ngôn ngữ.",
    """
## Thỏa thuận vô hình

Khi gọi hàm, hai bên thống nhất — không một cú pháp C nào nói ra — đối số đi đâu (register trước, rồi stack), register nào trả giá trị, và register nào callee phải khôi phục. Thỏa thuận đó là **quy ước gọi**, lõi của platform ABI.

## Caller-saved so với callee-saved

Register mà *callee* được phép xài tự do là caller-saved: nếu caller vẫn cần giá trị, nó phải đổ ra trước lời gọi. Register mà callee hứa bảo toàn là callee-saved: callee tự đổ và tự khôi phục. Sự phân công này giải thích vì sao thêm một lời gọi có thể đổi cách phân bổ register của caller — thấy được trong assembly của mô-đun 13.

## Hàm variadic cố tình phá khuôn mẫu

Hàm kiểu printf nhận danh sách đối số có hình dạng lúc chạy. `<stdarg.h>` (va_start/va_arg/va_end) là cửa sổ khả chuyển của chuẩn vào những gì quy ước thực sự làm — và lý do printf là con特别 thú với mọi ABI từng được thiết kế.
""",
)

write_lesson(
    M12,
    L12B,
    "Struct Layout as a Contract",
    "Offset rules, trailing padding, and the cross-binary stability that headers must guarantee.",
    15,
    """
## Layout is determined, not arbitrary

Every member sits at its alignment boundary, and the struct's total size is a multiple of its strictest alignment (module 1's forensics, now as a contract). Two compilers claiming the same ABI must compute the same layout for the same declaration — otherwise binary modules cannot exchange structs.

## The one-membership change that breaks everything

Adding a member in the *middle* shifts every later member's offset. Old binaries writing the old layout silently produce garbage for the new reader: no error, wrong data. This is why public C APIs append to the end of structs, or hide them behind opaque handles (module 3) entirely.

## Versioning without breaking

- **append-only**: new members go last; old code ignores the tail (the size it knew still worked for the old prefix).
- **reserved fields**: pad the struct to a stable size from day one.
- **opaque handles**: layout becomes private; you can change anything.

Choose deliberately: every public struct in your career will carry one of these three decisions.
""",
    "Bố cục struct như một hợp đồng",
    "Luật offset, đệm cuối, và sự ổn định xuyên binary mà header phải bảo đảm.",
    """
## Bố cục được suy ra, không tùy tiện

Mọi thành phần ngồi tại biên căn của nó, và tổng kích thước struct là bội của căn chặt nhất (pháp y của mô-đun 1, giờ là hợp đồng). Hai trình biên dịch tuyên bố cùng ABI phải tính ra cùng bố cục cho cùng khai báo — nếu không, các module nhị phân không thể trao đổi struct.

## Một thay đổi vị trí phá tung mọi thứ

Thêm thành phần vào *giữa* dịch chuyển offset của mọi thành phần sau. Binary cũ ghi bố cục cũ lặng lẽ tạo rác cho trình đọc mới: không lỗi, dữ liệu sai. Vì vậy API công khai của C chỉ thêm vào cuối struct, hoặc giấu hoàn toàn sau opaque handle (mô-đun 3).

## Phiên bản hóa mà không phá vỡ

- **append-only**: thành phần mới đi sau; code cũ phớt lờ phần đuôi (kích thước cũ vẫn dùng được cho phần đầu).
- **reserved field**: đệm struct tới kích thước ổn định từ ngày đầu.
- **opaque handle**: bố cục thành riêng tư; đổi gì cũng được.

Chọn có chủ đích: mọi struct công khai trong sự nghiệp của bạn sẽ mang một trong ba quyết định này.
""",
)

write_practice(
    M12,
    "ca-p12-abi",
    "ABI Contract Drills",
    "Layout arithmetic, append-only versioning, argument-passing probes, and va_list — the ABI as measurable code.",
    "Bài tập hợp đồng ABI",
    "Số học bố cục, phiên bản hóa append-only, thăm dò truyền đối số, và va_list — ABI thành code đo được.",
    L12A,
    22,
    "advanced",
    [
        challenge(
            "ca12-layout-contract",
            "Predict and Verify Layout",
            "Given (in your editor) `struct pkt { unsigned char ver; unsigned short len; unsigned int crc; };`, implement `void layout_report(size_t *off_len, size_t *off_crc, size_t *size)` writing offsetof values and sizeof. The tests check the *rules*, not hardcoded numbers: off_len is 2 (after 1-byte ver, aligned to 2), off_crc is 4, size is 8.",
            C_PRELUDE + "struct pkt { unsigned char ver; unsigned short len; unsigned int crc; };@NL@#include <stddef.h>@NL@",
            [
                ("member offsets follow alignment", "size_t l = 0, c = 0, s = 0;@NL@layout_report(&l, &c, &s);@NL@CHECK_EQ((long long)l, 2);@NL@CHECK_EQ((long long)c, 4);", "ver at 0; len needs 2-alignment so it sits at 2; crc at 4."),
                ("size is the rounded total", "size_t l2 = 0, c2 = 0, s2 = 0;@NL@layout_report(&l2, &c2, &s2);@NL@CHECK_EQ((long long)s2, 8);", "4 + 4 ends on the 4-byte alignment of the strictest member — no trailing padding needed beyond that."),
            ],
            level="independent",
        ),
        challenge(
            "ca12-append-version",
            "Append-Only Versioning",
            "Old struct in your editor: `struct cfg_v1 { int mode; int level; };`. Implement `size_t cfg_v1_size(void)` returning sizeof(struct cfg_v1), and — defining `struct cfg_v2 { int mode; int level; int flags; int reserved; };` — `int cfg_v2_prefix_compatible(void)` returning 1 iff the v2 members that v1 knew sit at identical offsets (verify with offsetof, do not hardcode 1).",
            C_PRELUDE + "struct cfg_v1 { int mode; int level; };@NL@#include <stddef.h>@NL@",
            [
                ("prefix stability", "CHECK_EQ(cfg_v2_prefix_compatible(), 1);", "offsetof(mode) and offsetof(level) agree across v1 and v2 — appending never moves the prefix."),
                ("new tail adds size", "CHECK_EQ(cfg_v1_size() <= 8, 1);", "The v1 struct is its two ints; v2 grows only by appended members."),
            ],
            level="combination",
        ),
        challenge(
            "ca12-arg-counting",
            "Argument Passing Probe",
            "Implement `int arg_sum8(int a, int b, int c, int d, int e, int f, int g, int h)` returning the sum of its eight parameters. On every real ABI, the first several travel in registers and the rest spill to the stack — the function is identical either way, which is the ABI's whole point: source does not change, the machine contract adapts.",
            C_PRELUDE,
            [
                ("eight arguments sum", "CHECK_EQ(arg_sum8(1, 2, 3, 4, 5, 6, 7, 8), 36);", "Register vs stack delivery is invisible to the C source — total 36."),
            ],
            level="guided",
        ),
        challenge(
            "ca12-varargs",
            "va_list Windows onto the Convention",
            "Implement `int sum_ints(int count, ...)` using va_start/va_arg/va_end to total `count` int arguments, and `double sum_dbls(int count, ...)` doing the same for doubles. The header is the standard's only portable view of how variadic arguments physically travel.",
            C_PRELUDE + "#include <stdarg.h>@NL@",
            [
                ("ints through va_arg", "CHECK_EQ(sum_ints(4, 10, 20, 30, 40), 100);", "Each va_arg(int) fetch advances the window once."),
                ("doubles through va_arg", "CHECK_EQ((int)sum_dbls(3, 1.5, 2.5, 3.0), 7);", "Floating arguments travel by their own rules; va_arg(double) reads them portably. 1.5+2.5+3.0 = 7.0."),
            ],
            level="combination",
        ),
    ],
    {
        "ca12-layout-contract": vi_challenge(
            "Dự đoán và xác minh bố cục",
            "Có sẵn struct pkt. Cài layout_report ghi offsetof và sizeof — test kiểm tra luật, không phải con số cứng.",
            [
                ("offset theo căn", "ver ở 0; len cần căn 2 nên ngồi ở 2; crc ở 4."),
                ("kích thước là tổng đã làm tròn", "4 + 4 khớp căn 4 của thành phần chặt nhất — không cần đệm cuối."),
            ],
        ),
        "ca12-append-version": vi_challenge(
            "Phiên bản hóa append-only",
            "Có sẵn cfg_v1. Định nghĩa cfg_v2 thêm flags và reserved ở cuối; xác minh prefix của v1 giữ nguyên offset bằng offsetof.",
            [
                ("prefix ổn định", "offsetof(mode) và offsetof(level) khớp nhau giữa v1 và v2 — thêm vào cuối không xê dịch prefix."),
                ("đuôi mới tăng kích thước", "struct v1 là hai int của nó; v2 chỉ lớn thêm bởi thành phần được thêm."),
            ],
        ),
        "ca12-arg-counting": vi_challenge(
            "Thăm dò truyền đối số",
            "Cài arg_sum8 tổng tám tham số — trên mọi ABI thật, vài tham số đầu đi bằng register, phần còn lại xuống stack, và mã nguồn không đổi.",
            [
                ("tám đối số cộng lại", "Register hay stack đều vô hình với mã nguồn — tổng 36."),
            ],
        ),
        "ca12-varargs": vi_challenge(
            "va_list cửa sổ vào quy ước",
            "Cài sum_ints(count, ...) và sum_dbls(count, ...) bằng va_start/va_arg/va_end.",
            [
                ("int qua va_arg", "Mỗi va_arg(int) đẩy cửa sổ tiến một bước."),
                ("double qua va_arg", "Đối số số thực đi theo luật riêng; va_arg(double) đọc chúng khả chuyển. 1.5+2.5+3.0 = 7.0."),
            ],
        ),
    },
    solutions=[
        (
            "ca12-layout-contract",
            C_PRELUDE
            + "struct pkt { unsigned char ver; unsigned short len; unsigned int crc; };@NL@"
            + "#include <stddef.h>@NL@"
            + "void layout_report(size_t *off_len, size_t *off_crc, size_t *size) {@NL@    *off_len = offsetof(struct pkt, len);@NL@    *off_crc = offsetof(struct pkt, crc);@NL@    *size = sizeof(struct pkt);@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "struct pkt { unsigned char ver; unsigned short len; unsigned int crc; };@NL@"
            + "#include <stddef.h>@NL@"
            + "void layout_report(size_t *off_len, size_t *off_crc, size_t *size) {@NL@    *off_len = 1;@NL@    *off_crc = 3;@NL@    *size = 7;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca12-append-version",
            C_PRELUDE
            + "struct cfg_v1 { int mode; int level; };@NL@"
            + "#include <stddef.h>@NL@"
            + "struct cfg_v2 { int mode; int level; int flags; int reserved; };@NL@"
            + "size_t cfg_v1_size(void) { return sizeof(struct cfg_v1); }@NL@"
            + "int cfg_v2_prefix_compatible(void) {@NL@    return offsetof(struct cfg_v1, mode) == offsetof(struct cfg_v2, mode)@NL@        && offsetof(struct cfg_v1, level) == offsetof(struct cfg_v2, level);@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "struct cfg_v1 { int mode; int level; };@NL@"
            + "#include <stddef.h>@NL@"
            + "struct cfg_v2 { int flags; int reserved; int mode; int level; };@NL@"
            + "size_t cfg_v1_size(void) { return sizeof(struct cfg_v1); }@NL@"
            + "int cfg_v2_prefix_compatible(void) {@NL@    return offsetof(struct cfg_v1, mode) == offsetof(struct cfg_v2, mode)@NL@        && offsetof(struct cfg_v1, level) == offsetof(struct cfg_v2, level);@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca12-arg-counting",
            C_PRELUDE
            + "int arg_sum8(int a, int b, int c, int d, int e, int f, int g, int h) {@NL@    return a + b + c + d + e + f + g + h;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int arg_sum8(int a, int b, int c, int d, int e, int f, int g, int h) {@NL@    return a + b + c + d + e + f + g;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca12-varargs",
            C_PRELUDE
            + "#include <stdarg.h>@NL@"
            + "int sum_ints(int count, ...) {@NL@    va_list ap;@NL@    va_start(ap, count);@NL@    int s = 0;@NL@    for (int i = 0; i < count; i++) s += va_arg(ap, int);@NL@    va_end(ap);@NL@    return s;@NL@}@NL@"
            + "double sum_dbls(int count, ...) {@NL@    va_list ap;@NL@    va_start(ap, count);@NL@    double s = 0;@NL@    for (int i = 0; i < count; i++) s += va_arg(ap, double);@NL@    va_end(ap);@NL@    return s;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdarg.h>@NL@"
            + "int sum_ints(int count, ...) {@NL@    va_list ap;@NL@    va_start(ap, count);@NL@    int s = 0;@NL@    for (int i = 0; i < count; i++) s += va_arg(ap, int);@NL@    va_end(ap);@NL@    return s;@NL@}@NL@"
            + "double sum_dbls(int count, ...) {@NL@    va_list ap;@NL@    va_start(ap, count);@NL@    double s = 0;@NL@    for (int i = 0; i < count; i++) s += (double)(int)va_arg(ap, double);@NL@    va_end(ap);@NL@    return s;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M12,
    L12CP,
    "Checkpoint: The Binary Contract",
    "Consolidated ABI checkpoint.",
    12,
    """
Checkpoint for module 12: verify a layout by rule, prove prefix stability across a version bump, and pass an argument list through the convention.
""",
    "Kiểm tra: Hợp đồng nhị phân",
    "Kiểm tra tổng hợp ABI.",
    """
Kiểm tra mô-đun 12: xác minh bố cục theo luật, chứng minh prefix ổn định qua lần nâng phiên bản, và chuyền danh sách đối số qua quy ước.
""",
)

write_checkpoint(
    M12,
    L12CP,
    "Checkpoint: Struct Contracts Across Versions",
    "One program: a versioned packet struct with append-only evolution, offset-verified prefix stability, and a varargs aggregator.",
    16,
    "See lesson.",
    "Kiểm tra: Hợp đồng struct xuyên phiên bản",
    "Một chương trình: struct packet có phiên bản hóa append-only, ổn định prefix xác minh bằng offset, và bộ gộp varargs.",
    "Xem bài học.",
    challenge(
        "ca12-checkpoint-versioned",
        "Checkpoint: Append-Only Packet",
        "In your editor: `struct frame { unsigned char tag; unsigned short seq; unsigned int payload; };`. Implement:@CE@1. `void frame_report(size_t *off_seq, size_t *off_payload, size_t *size)` — offsetof/sizeof measured, not hardcoded.@CE@2. Define `struct frame_v2 { unsigned char tag; unsigned short seq; unsigned int payload; unsigned long long ts; };` and `int frame_prefix_stable(void)` — 1 iff tag/seq/payload offsets are identical between the versions (offsetof-verified).@CE@3. `unsigned long long sum_upto(int n, ...)` — totals n unsigned ints passed variadic.",
        C_PRELUDE + "struct frame { unsigned char tag; unsigned short seq; unsigned int payload; };@NL@#include <stddef.h>@NL@#include <stdarg.h>@NL@",
        [
            ("measured layout", "size_t s1 = 0, p1 = 0, z1 = 0;@NL@frame_report(&s1, &p1, &z1);@NL@CHECK_EQ((long long)s1, 2);@NL@CHECK_EQ((long long)p1, 4);@NL@CHECK_EQ((long long)z1, 8);", "tag at 0; seq at 2 (2-aligned); payload at 4; size rounds to the 4-alignment."),
            ("prefix survives the bump", "CHECK_EQ(frame_prefix_stable(), 1);", "Appending ts after payload cannot move the earlier members — verified, not assumed."),
            ("variadic totals", "CHECK_EQ((long long)sum_upto(3, 7u, 8u, 9u), 24);", "va_arg(unsigned int) walks the argument window; 7+8+9 = 24."),
        ],
        level="mini-build",
    ),
    {
        "ca12-checkpoint-versioned": vi_challenge(
            "Kiểm tra: Packet append-only",
            "Có sẵn struct frame. Cài frame_report (đo offsetof/sizeof), frame_prefix_stable (so offsetof giữa hai phiên bản), sum_upto (varargs unsigned).",
            [
                ("bố cục được đo", "tag ở 0; seq ở 2 (căn 2); payload ở 4; kích thước làm tròn theo căn 4."),
                ("prefix sống sót qua nâng cấp", "Thêm ts sau payload không thể xê dịch thành phần trước — xác minh, không giả định."),
                ("tổng variadic", "va_arg(unsigned int) đi qua cửa sổ đối số; 7+8+9 = 24."),
            ],
        )
    },
    solution=C_PRELUDE
    + "struct frame { unsigned char tag; unsigned short seq; unsigned int payload; };@NL@"
    + "#include <stddef.h>@NL@#include <stdarg.h>@NL@"
    + "struct frame_v2 { unsigned char tag; unsigned short seq; unsigned int payload; unsigned long long ts; };@NL@"
    + "void frame_report(size_t *off_seq, size_t *off_payload, size_t *size) {@NL@    *off_seq = offsetof(struct frame, seq);@NL@    *off_payload = offsetof(struct frame, payload);@NL@    *size = sizeof(struct frame);@NL@}@NL@"
    + "int frame_prefix_stable(void) {@NL@    return offsetof(struct frame, tag) == offsetof(struct frame_v2, tag)@NL@        && offsetof(struct frame, seq) == offsetof(struct frame_v2, seq)@NL@        && offsetof(struct frame, payload) == offsetof(struct frame_v2, payload);@NL@}@NL@"
    + "unsigned long long sum_upto(int n, ...) {@NL@    va_list ap;@NL@    va_start(ap, n);@NL@    unsigned long long s = 0;@NL@    for (int i = 0; i < n; i++) s += va_arg(ap, unsigned int);@NL@    va_end(ap);@NL@    return s;@NL@}@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "struct frame { unsigned char tag; unsigned short seq; unsigned int payload; };@NL@"
    + "#include <stddef.h>@NL@#include <stdarg.h>@NL@"
    + "struct frame_v2 { unsigned long long ts; unsigned char tag; unsigned short seq; unsigned int payload; };@NL@"
    + "void frame_report(size_t *off_seq, size_t *off_payload, size_t *size) {@NL@    *off_seq = 1;@NL@    *off_payload = 2;@NL@    *size = 6;@NL@}@NL@"
    + "int frame_prefix_stable(void) {@NL@    return offsetof(struct frame, tag) == offsetof(struct frame_v2, tag)@NL@        && offsetof(struct frame, seq) == offsetof(struct frame_v2, seq)@NL@        && offsetof(struct frame, payload) == offsetof(struct frame_v2, payload);@NL@}@NL@"
    + "unsigned long long sum_upto(int n, ...) {@NL@    va_list ap;@NL@    va_start(ap, n);@NL@    unsigned long long s = 0;@NL@    for (int i = 0; i < n - 1; i++) s += va_arg(ap, unsigned int);@NL@    va_end(ap);@NL@    return s;@NL@}@NL@"
    + "int main(void) { return 0; }",
)
