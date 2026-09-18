#!/usr/bin/env python3
"""C Advanced — batch 7: modules 13 (reading-assembly) and
14 (build-engineering). Zero-backslash authoring: @NL@ = statement
separator, @CE@ = newline escape inside C string literals."""
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

# ==================== MODULE 13: ca-reading-assembly ========================
M13 = "ca-reading-assembly"

L13A = "ca-compiler-output"
L13B = "ca-optimization-visible"
L13CP = "ca-checkpoint-m13"

write_module(
    M13,
    "Reading What the Compiler Emits",
    "Compiler-generated assembly as evidence: prologues, register discipline, and watching optimization transform real functions — arch-aware, never arch-worshipping.",
    "Đọc thứ trình biên dịch phát ra",
    "Assembly do trình biên dịch tạo ra là bằng chứng: prologue, kỷ luật register, và xem tối ưu hóa biến đổi hàm thật — nhận diện kiến trúc, không tôn thờ kiến trúc.",
    [L13A, L13B, L13CP],
    ["ca-p13-asm"],
)

write_lesson(
    M13,
    L13A,
    "Anatomy of Emitted Code",
    "Function prologues and epilogues, frame pointers, and how to map C statements onto instruction sequences.",
    16,
    """
## Every function has a shape

A typical prologue pushes callee-saved registers it will use, adjusts the stack pointer for locals, and sometimes keeps a frame pointer. The epilogue reverses it. Recognizing this shape is 80% of reading any dump: everything between the prologue and epilogue is *your* function's logic.

## Mapping C to instructions

```c
int tri(int n) { return n * (n + 1) / 2; }
```

The emitted code may never touch a multiply in the way you wrote it — compilers turn `n * (n + 1) / 2` into shifts and adds when profitable. The lesson is not 'assembly is hard'; it is *the compiler is already optimizing*, and reading its output shows you the transformations modules 4 and 10 only described.

## How to look, honestly

`gcc -S` (assembly text), `gcc -c` + `objdump -d` (disassembly of the object). Output differs across architectures (aarch64 vs x86-64) and across optimization levels. Professional practice: read *your own* function's dump, compare -O0 against -O2, and explain each difference. Never memorize one platform's mnemonics as 'the truth'.
""",
    "Giải phẫu code phát ra",
    "Prologue và epilogue của hàm, frame pointer, và cách ánh xạ câu lệnh C vào chuỗi lệnh máy.",
    """
## Mọi hàm đều có hình dáng

Prologue điển hình push các register callee-saved sẽ dùng, dời stack pointer cho biến cục bộ, và đôi khi giữ frame pointer. Epilogue làm ngược lại. Nhận ra hình dáng này là 80% việc đọc bất kỳ dump nào: mọi thứ giữa prologue và epilogue là logic *của hàm bạn*.

## Ánh xạ C sang lệnh máy

```c
int tri(int n) { return n * (n + 1) / 2; }
```

Code phát ra có thể không chạm phép nhân theo cách bạn viết — trình biên dịch biến `n * (n + 1) / 2` thành shift và add khi có lợi. Bài học không phải 'assembly khó'; mà là *trình biên dịch đã tối ưu sẵn*, và đọc đầu ra của nó cho thấy các phép biến đổi mà mô-đun 4 và 10 chỉ nói tới.

## Cách nhìn, trung thực

`gcc -S` (assembly dạng văn bản), `gcc -c` + `objdump -d` (disassembly của object). Đầu ra khác nhau giữa các kiến trúc (aarch64 so với x86-64) và giữa các mức tối ưu. Thực hành chuyên nghiệp: đọc dump của *hàm của chính bạn*, so -O0 với -O2, và giải thích từng khác biệt. Đừng thuộc các mnemonic của một nền tảng rồi coi là 'chân lý'.
""",
)

write_lesson(
    M13,
    L13B,
    "Watching Optimizations Happen",
    "Constant folding, dead-code elimination, and loop-invariant motion — each visible as a *smaller* or *cheaper* dump.",
    16,
    """
## Optimizations have signatures

- **Constant folding**: a function computing 21 * 2 with locals becomes a load of an immediate (or `return 42` inline) — no multiply instruction remains.
- **Dead-code elimination**: code whose result is never used disappears entirely.
- **Loop-invariant code motion**: a computation that does not depend on the loop variable is hoisted before the loop — one evaluation instead of n.
- **Strength reduction**: multiplications by powers of two become shifts.

Each has a visible footprint: instruction counts, removed loads, hoisted lines. That is why this course grounds optimization talk in *comparing dumps*, not folklore.

## The honest measuring loop

Count something concrete: instructions in the dump, branches taken in a benchmark harness, bytes of the .text section (module 11's `size`). 'Faster' claims without a counter are vibes. The challenges below give you the counters.
""",
    "Xem tối ưu hóa diễn ra",
    "Gập hằng, loại code chết, chuyển invariant ra khỏi vòng lặp — mỗi cái hiện hình là một dump *nhỏ hơn* hoặc *rẻ hơn*.",
    """
## Tối ưu hóa có chữ ký

- **Gập hằng**: hàm tính 21 * 2 với biến cục bộ thành load một immediate — không còn lệnh nhân.
- **Loại code chết**: code có kết quả không bao giờ được dùng biến mất hoàn toàn.
- **Chuyển invariant khỏi vòng lặp**: phép tính không phụ thuộc biến vòng lặp bị kéo lên trước vòng — một lần thay vì n lần.
- **Giảm cường độ**: nhân với lũy thừa hai thành shift.

Mỗi cái có dấu vết nhìn được: số lệnh, load bị xóa, dòng bị kéo lên. Vì vậy khóa học này neo talk tối ưu vào *so sánh dump*, không phải lời truyền miệng.

## Vòng lặp đo trung thực

Đếm thứ cụ thể: số lệnh trong dump, số nhánh trong benchmark, byte của section .text (lệnh `size` của mô-đun 11). Tuyên bố 'nhanh hơn' không có bộ đếm là cảm tính. Các bài dưới đây trao cho bạn bộ đếm.
""",
)

write_practice(
    M13,
    "ca-p13-asm",
    "Assembly Evidence Drills",
    "Functions whose semantics prove which transformations happened — folding, invariants, strength reduction, and stack discipline — without betting on mnemonics.",
    "Bài tập bằng chứng assembly",
    "Các hàm mà ngữ nghĩa chứng minh phép biến đổi nào đã xảy ra — gập hằng, invariant, giảm cường độ, kỷ luật stack — không cá cược vào mnemonic.",
    L13A,
    22,
    "advanced",
    [
        challenge(
            "ca13-fold-signature",
            "Folding Leaves No Multiply",
            "Implement `int folded_const(void)` returning 21 * 2 via two automatic locals, and `int folded_param(int x)` returning x * 2. The first's dump must contain no runtime multiply (the test verifies the *value* 42 and that repeated calls agree — folding is transparent to behavior); the second cannot fold (its argument is runtime data). Explain the difference in your hint text.",
            C_PRELUDE,
            [
                ("constant folds to immediate", "CHECK_EQ(folded_const(), 42);@NL@CHECK_EQ(folded_const(), folded_const());", "21 * 2 with automatic locals is compile-time constant — behavior identical, dump smaller."),
                ("parameter cannot fold", "CHECK_EQ(folded_param(21), 42);@NL@CHECK_EQ(folded_param(-3), -6);", "The multiply must happen at runtime; the dump carries a real instruction for it."),
            ],
            level="guided",
        ),
        challenge(
            "ca13-invariant-hoist",
            "Invariant Leaves the Loop",
            "Implement `long long hoisted(int base, size_t n)` totaling base*2 + i for i in 0..n-1, computed with the invariant `base*2` *outside* the loop (store it in a local first). Implement `long long naive(int base, size_t n)` recomputing base*2 inside the loop. Both return the same value — the optimizer may hoist the naive one anyway; the discipline is yours to keep.",
            C_PRELUDE,
            [
                ("identical totals", "CHECK_EQ(hoisted(5, 4), naive(5, 4));@NL@CHECK_EQ(hoisted(3, 100), naive(3, 100));", "Reordering an invariant out of a loop cannot change the sum — only the instruction count."),
                ("sum value is right", "CHECK_EQ((long long)hoisted(5, 4), 2 * 5 + 0 + 2 * 5 + 1 + 2 * 5 + 2 + 2 * 5 + 3);", "n=4, base=5: each term is base*2 + i."),
            ],
            level="independent",
        ),
        challenge(
            "ca13-strength-reduction",
            "Shifts for Powers of Two",
            "Implement `unsigned int by_shift(unsigned int x)` returning x * 8 using a left shift, and `unsigned int by_mul(unsigned int x)` returning x * 8 with multiplication. Values agree for every input below 2^29 (no overflow); the *dump* differs — the test pins the arithmetic contract, your hint explains the emission difference.",
            C_PRELUDE,
            [
                ("shift equals multiply", "CHECK_EQ(by_shift(12345u), by_mul(12345u));@NL@CHECK_EQ(by_shift(0u), 0u);", "x * 8 == x << 3 for all x without overflow — the compiler knows this too."),
                ("large values agree", "CHECK_EQ(by_shift(268435455u), 2147483640u);", "2^28 - 1 times 8 = 2^31 - 8, still within unsigned range."),
            ],
            level="independent",
        ),
        challenge(
            "ca13-saved-registers",
            "What Survives a Call",
            "File-scope `static int callee_touch = 0;` is in your editor. Implement `void callee(void)` that increments it (proving the call happened) and `int caller_keeps(int a, int b)` that computes a*2 into a local, calls callee(), then returns the local + b — the local's value must survive the call, which is the caller/callee register split working as designed.",
            C_PRELUDE + "static int callee_touch = 0;@NL@",
            [
                ("locals survive calls", "CHECK_EQ(caller_keeps(10, 5), 25);@NL@CHECK_EQ(callee_touch, 1);", "The intermediate a*2 persists across callee() — the ABI's register contract, felt from source."),
            ],
            level="combination",
        ),
    ],
    {
        "ca13-fold-signature": vi_challenge(
            "Gập hằng không còn phép nhân",
            "Cài folded_const() (21 * 2 qua biến cục bộ) và folded_param(x) (x * 2) — cái đầu gập được, cái sau không.",
            [
                ("hằng gập thành immediate", "21 * 2 với biến tự động là hằng lúc biên dịch — hành vi như nhau, dump nhỏ hơn."),
                ("tham số không gập được", "Phép nhân phải xảy ra lúc chạy; dump chứa lệnh thật cho nó."),
            ],
        ),
        "ca13-invariant-hoist": vi_challenge(
            "Invariant rời vòng lặp",
            "Cài hoisted() đặt base*2 ra ngoài vòng và naive() tính lại trong vòng — kết quả như nhau, chỉ số lệnh khác nhau.",
            [
                ("tổng giống hệt", "Chuyển invariant khỏi vòng không thể đổi tổng — chỉ đổi số lệnh."),
                ("giá trị tổng đúng", "n=4, base=5: mỗi số hạng là base*2 + i."),
            ],
        ),
        "ca13-strength-reduction": vi_challenge(
            "Shift thay lũy thừa hai",
            "Cài by_shift (x << 3) và by_mul (x * 8) — giá trị khớp với mọi đầu vào không tràn; dump khác nhau.",
            [
                ("shift bằng nhân", "x * 8 == x << 3 với mọi x không tràn — trình biên dịch cũng biết điều đó."),
                ("giá trị lớn vẫn khớp", "2^28 - 1 nhân 8 = 2^31 - 8, vẫn trong phạm vi unsigned."),
            ],
        ),
        "ca13-saved-registers": vi_challenge(
            "Cái gì sống sót qua lời gọi",
            "Có sẵn `static int callee_touch = 0;`. Cài callee() tăng nó, và caller_keeps(a, b) giữ a*2 qua lời gọi rồi cộng b.",
            [
                ("biến cục bộ sống qua lời gọi", "Giá trị trung gian a*2 bền qua callee() — hợp đồng register của ABI, cảm nhận từ mã nguồn."),
            ],
        ),
    },
    solutions=[
        (
            "ca13-fold-signature",
            C_PRELUDE
            + "int folded_const(void) { int a = 21; int b = 2; return a * b; }@NL@"
            + "int folded_param(int x) { return x * 2; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int folded_const(void) { int a = 21; int b = 2; return a + b; }@NL@"
            + "int folded_param(int x) { return x * 2; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca13-invariant-hoist",
            C_PRELUDE
            + "long long hoisted(int base, size_t n) {@NL@    long long b2 = (long long)base * 2;@NL@    long long s = 0;@NL@    for (size_t i = 0; i < n; i++) s += b2 + (long long)i;@NL@    return s;@NL@}@NL@"
            + "long long naive(int base, size_t n) {@NL@    long long s = 0;@NL@    for (size_t i = 0; i < n; i++) s += (long long)base * 2 + (long long)i;@NL@    return s;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "long long hoisted(int base, size_t n) {@NL@    long long b2 = (long long)base * 2;@NL@    long long s = 0;@NL@    for (size_t i = 0; i < n; i++) s += b2 + (long long)i;@NL@    return s;@NL@}@NL@"
            + "long long naive(int base, size_t n) {@NL@    long long s = 0;@NL@    for (size_t i = 0; i < n; i++) s += (long long)base * 3 + (long long)i;@NL@    return s;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca13-strength-reduction",
            C_PRELUDE
            + "unsigned int by_shift(unsigned int x) { return x << 3; }@NL@"
            + "unsigned int by_mul(unsigned int x) { return x * 8u; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "unsigned int by_shift(unsigned int x) { return x << 3; }@NL@"
            + "unsigned int by_mul(unsigned int x) { return x * 9u; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca13-saved-registers",
            C_PRELUDE
            + "static int callee_touch = 0;@NL@"
            + "void callee(void) { callee_touch++; }@NL@"
            + "int caller_keeps(int a, int b) {@NL@    int local = a * 2;@NL@    callee();@NL@    return local + b;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "static int callee_touch = 0;@NL@"
            + "void callee(void) { callee_touch++; }@NL@"
            + "int caller_keeps(int a, int b) {@NL@    callee();@NL@    int local = a * 2;@NL@    return local + b + callee_touch;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

# ================== MODULE 14: ca-build-engineering =========================
M14 = "ca-build-engineering"

L14A = "ca-make-discipline"
L14B = "ca-flags-hardening"
L14CP = "ca-checkpoint-m14"

write_module(
    M14,
    "Build Engineering: Make, Flags, and Warnings",
    "Make dependency graphs, incremental builds, and the warning-and-hardening flags that turn the toolchain into a static analyzer — practiced on real builds inside the sandbox.",
    "Kỹ thuật build: Make, cờ, và cảnh báo",
    "Đồ thị phụ thuộc Make, build tăng dần, và các cờ cảnh báo-tăng cường biến toolchain thành máy phân tích tĩnh — luyện trên build thật trong sandbox.",
    [L14A, L14B, L14CP],
    ["ca-p14-build"],
)

write_lesson(
    M14,
    L14A,
    "Make as a Dependency Graph",
    "Targets, prerequisites, recipes, automatic variables, and why incremental builds are correct only when dependencies are complete.",
    16,
    """
## The whole model in three sentences

A Makefile states: a **target** depends on **prerequisites**, and a **recipe** rebuilds it when any prerequisite is newer. Make walks this graph bottom-up, skipping everything already up to date. That is the entire theory.

```make
CC = gcc
CFLAGS = -std=c23 -Wall -Wextra -O2

app: main.o util.o
	$(CC) main.o util.o -o app

%.o: %.c util.h
	$(CC) $(CFLAGS) -c $< -o $@
```

`$<` is the first prerequisite, `$@` the target, `%.o: %.c` a pattern rule — three pieces of syntax covering most real builds.

## Incompleteness is the classic failure

If util.o's rule forgets its dependency on util.h, editing util.h rebuilds nothing — the build *succeeds* while shipping stale objects. Missing dependencies do not fail loudly; they lie quietly. Header dependency generators (`-MMD -MP`) exist precisely because humans forget.

## Order-only and phony targets

Directories as prerequisites should be order-only (`| bin`), and non-file targets like `clean` must be declared `.PHONY` — or a stray file named `clean` silently disables it.
""",
    "Make như đồ thị phụ thuộc",
    "Target, prerequisite, recipe, biến tự động, và vì sao build tăng dần chỉ đúng khi phụ thuộc đầy đủ.",
    """
## Toàn bộ mô hình trong ba câu

Makefile tuyên bố: một **target** phụ thuộc các **prerequisite**, và **recipe** dựng lại nó khi bất kỳ prerequisite nào mới hơn. Make đi đồ thị này từ dưới lên, bỏ qua mọi thứ đã cập nhật. Đó là toàn bộ lý thuyết.

```make
CC = gcc
CFLAGS = -std=c23 -Wall -Wextra -O2

app: main.o util.o
	$(CC) main.o util.o -o app

%.o: %.c util.h
	$(CC) $(CFLAGS) -c $< -o $@
```

`$<` là prerequisite đầu, `$@` là target, `%.o: %.c` là pattern rule — ba mảnh cú pháp phủ phần lớn build thật.

## Thiếu sót là lỗi kinh điển

Nếu rule của util.o quên phụ thuộc util.h, sửa util.h không dựng lại gì — build *thành công* trong khi vẫn vận hành object cũ. Phụ thuộc thiếu không hụt ầm ầm; chúng nói dối một cách lặng lẽ. Bộ sinh phụ thuộc header (`-MMD -MP`) tồn tại chính vì con người quên.

## Order-only và phony target

Thư mục làm prerequisite nên là order-only (`| bin`), và target phi-file như `clean` phải khai báo `.PHONY` — hoặc một file tên `clean` sẽ lặng lẽ vô hiệu hóa nó.
""",
)

write_lesson(
    M14,
    L14B,
    "Warning Discipline and Hardening Flags",
    "The flag set that catches real bugs before runtime — and what each one actually looks for.",
    15,
    """
## The baseline set

- `-Wall -Wextra` — the standard radar: uninitialized use, sign compare, unused results, missing returns.
- `-Werror` — warnings become build failures; a warning backlog cannot accumulate.
- `-Wpedantic` — refuses non-standard constructs, guarding portability claims.
- `-Wshadow` — a local shadowing an outer name is a read-the-wrong-variable bug waiting.
- `-Wconversion` — implicit narrowing (int to char, size_t to int) made visible.

Each flag is a *class* of defect, not a style opinion. This course's own challenges compile under -Wall -Wextra -Wpedantic — the code you write here passes a strict baseline by construction.

## Hardening for the runtime

- `-D_FORTIFY_SOURCE` — the library checks buffer sizes where it can prove them.
- `-fstack-protector-strong` — canaries before return addresses on frames with arrays.
- Position-independent flags plus ASLR (module 24) make memory-corruption exploits substantially harder.

Hardening flags are not a substitute for correct code; they are the safety net that turns latent corruption into loud aborts during testing.
""",
    "Kỷ luật cảnh báo và cờ tăng cường",
    "Bộ cờ bắt lỗi thật trước lúc chạy — và từng cờ thực sự tìm cái gì.",
    """
## Bộ cơ sở

- `-Wall -Wextra` — radar tiêu chuẩn: dùng chưa khởi tạo, so sánh dấu, kết quả không dùng, thiếu return.
- `-Werror` — cảnh báo thành lỗi build; tồn đọng cảnh báo không thể tích tụ.
- `-Wpedantic` — từ chối cấu trúc phi chuẩn, bảo vệ tuyên bố khả chuyển.
- `-Wshadow` — biến cục bộ che tên ngoài là một bug đọc-sai-biến đang chờ.
- `-Wconversion` — thu hẹp ngầm (int sang char, size_t sang int) trở nên thấy được.

Mỗi cờ là một *lớp* lỗi, không phải ý kiến phong cách. Các bài của chính khóa học này biên dịch dưới -Wall -Wextra -Wpedantic — code bạn viết ở đây đạt baseline nghiêm ngặt ngay từ đầu.

## Tăng cường cho lúc chạy

- `-D_FORTIFY_SOURCE` — thư viện kiểm tra kích thước buffer ở nơi chứng minh được.
- `-fstack-protector-strong` — canary trước return address trên frame có mảng.
- Cờ position-independent cộng ASLR (mô-đun 24) khiến khai thác hủy hoại bộ nhớ khó hơn hẳn.

Cờ tăng cường không thay thế code đúng; chúng là lưới an toàn biến hủy hoại tiềm ẩn thành abort ầm ầm trong lúc kiểm thử.
""",
)

write_practice(
    M14,
    "ca-p14-build",
    "Build Model Drills",
    "Make's graph semantics and warning-class knowledge, as executable functions — the build system as testable design.",
    "Bài tập mô hình build",
    "Ngữ nghĩa đồ thị của Make và kiến thức lớp cảnh báo, dưới dạng hàm chạy được — hệ thống build như thiết kế kiểm thử được.",
    L14A,
    20,
    "advanced",
    [
        challenge(
            "ca14-rebuild-model",
            "Model Incremental Rebuilds",
            "Implement `int needs_rebuild(long long tgt_mtime, long long dep_mtimes, size_t n)` returning 1 iff any prerequisite mtime is strictly newer than the target's. Then implement `int make_would_build(long long tgt, const long long *deps, size_t n, int phony)` — same, but a phony target always rebuilds.",
            C_PRELUDE,
            [
                ("newer prerequisite triggers", "long long deps[2] = {100, 105};@NL@CHECK_EQ(needs_rebuild(102, deps, 2), 1);@NL@CHECK_EQ(needs_rebuild(106, deps, 2), 0);@NL@CHECK_EQ(needs_rebuild(105, deps, 2), 0);", "One newer prerequisite (105 > 102) is enough; all older means up to date. Equal timestamps mean up to date (strictly-newer semantics)."),
                ("phony always rebuilds", "long long deps2[1] = {10};@NL@CHECK_EQ(make_would_build(20, deps2, 1, 1), 1);", ".PHONY ignores timestamps by definition."),
            ],
            level="independent",
        ),
        challenge(
            "ca14-flag-taxonomy",
            "Classify the Flag",
            "Implement `const char *flag_intent(const char *flag)` mapping each flag to its intent class: '-Wall' → \"warnings\", '-Werror' → \"escalation\", '-g' → \"debug-info\", '-O2' → \"optimization\", '-c' → \"compile-only\", '-fsanitize=address' → \"runtime-check\", anything else → \"other\".",
            C_PRELUDE,
            [
                ("warning classes", "CHECK_STR_EQ(flag_intent(\"-Wall\"), \"warnings\");@NL@CHECK_STR_EQ(flag_intent(\"-Werror\"), \"escalation\");", "-Wall detects defect classes; -Werror changes failure policy, not detection."),
                ("build phases", "CHECK_STR_EQ(flag_intent(\"-c\"), \"compile-only\");@NL@CHECK_STR_EQ(flag_intent(\"-O2\"), \"optimization\");", "Phase flags select what runs; optimization flags select how hard."),
                ("runtime tools", "CHECK_STR_EQ(flag_intent(\"-fsanitize=address\"), \"runtime-check\");@NL@CHECK_STR_EQ(flag_intent(\"-g\"), \"debug-info\");", "Sanitizer flags add runtime machinery; -g adds metadata for humans."),
            ],
            level="imitation",
        ),
        challenge(
            "ca14-dependency-closure",
            "Header Dependency Closure",
            "Given the edge table already in your editor (`struct dep { int obj; int header; }; deps[]` mapping objects to the headers they include: main.o→util.h, util.o→util.h, main.o→main.h), implement `int header_touch_breaks(size_t n_objects, const int *obj_uses_header, size_t n_uses)` returning how many objects must rebuild when a header changes — obj_uses_header being a 0/1 per object. Then implement `int stale_objects_possible(int rule_includes_header)` returning 1 iff omitting a real header dependency can leave stale objects after an edit.",
            C_PRELUDE,
            [
                ("affected objects rebuild", "int uses[3] = {1, 1, 0};@NL@CHECK_EQ(header_touch_breaks(3, uses, 3), 2);", "Two of the three objects include the changed header: two rebuilds."),
                ("omission leaves stale objects", "CHECK_EQ(stale_objects_possible(0), 1);", "A rule that forgets a header dependency lets edited headers ship as stale objects — the quiet lie of incomplete graphs."),
            ],
            level="combination",
        ),
    ],
    {
        "ca14-rebuild-model": vi_challenge(
            "Mô hình dựng lại tăng dần",
            "Cài needs_rebuild (một prerequisite mới hơn target là đủ) và make_would_build (phony luôn dựng lại).",
            [
                ("prerequisite mới hơn kích hoạt", "Một prerequisite mới hơn (105 > 102) là đủ; tất cả cũ hơn nghĩa là đã cập nhật."),
                ("phony luôn dựng lại", ".PHONY bỏ qua timestamp theo định nghĩa."),
            ],
        ),
        "ca14-flag-taxonomy": vi_challenge(
            "Phân loại cờ",
            "Cài flag_intent(flag) ánh xạ cờ sang lớp ý định — -Wall phát hiện lớp lỗi, -Werror đổi chính sách thất bại.",
            [
                ("lớp cảnh báo", "-Wall phát hiện các lớp lỗi; -Werror đổi chính sách thất bại chứ không đổi khả năng phát hiện."),
                ("các pha build", "Cờ pha chọn cái gì chạy; cờ tối ưu chọn mức độ mạnh."),
                ("công cụ lúc chạy", "Cờ sanitizer thêm máy móc lúc chạy; -g thêm metadata cho con người."),
            ],
        ),
        "ca14-dependency-closure": vi_challenge(
            "Đóng phụ thuộc header",
            "Có sẵn bảng phụ thuộc. Cài header_touch_breaks (đếm object phải dựng lại khi header đổi) và stale_objects_possible.",
            [
                ("object bị ảnh hưởng dựng lại", "Hai trong ba object include header vừa đổi: hai lần dựng lại."),
                ("thiếu sót để lại object cũ", "Rule quên phụ thuộc header cho phép header đã sửa vẫn vận hành object cũ — lời nói dối lặng lẽ của đồ thị thiếu sót."),
            ],
        ),
    },
    solutions=[
        (
            "ca14-rebuild-model",
            C_PRELUDE
            + "int needs_rebuild(long long tgt_mtime, const long long *dep_mtimes, size_t n) {@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (dep_mtimes[i] > tgt_mtime) return 1;@NL@    }@NL@    return 0;@NL@}@NL@"
            + "int make_would_build(long long tgt, const long long *deps, size_t n, int phony) {@NL@    if (phony) return 1;@NL@    return needs_rebuild(tgt, deps, n);@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int needs_rebuild(long long tgt_mtime, const long long *dep_mtimes, size_t n) {@NL@    long long newest = 0;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (dep_mtimes[i] > newest) newest = dep_mtimes[i];@NL@    }@NL@    return newest >= tgt_mtime;@NL@}@NL@"
            + "int make_would_build(long long tgt, const long long *deps, size_t n, int phony) {@NL@    if (phony) return 1;@NL@    return needs_rebuild(tgt, deps, n);@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca14-flag-taxonomy",
            C_PRELUDE
            + "const char *flag_intent(const char *flag) {@NL@    if (flag[0] != '-') return \"other\";@NL@    if (flag[1] == 'W') {@NL@        if (flag[2] == 'e') return \"escalation\";@NL@        return \"warnings\";@NL@    }@NL@    if (flag[1] == 'g' && flag[2] == 0) return \"debug-info\";@NL@"
            + "    if (flag[1] == 'O') return \"optimization\";@NL@"
            + "    if (flag[1] == 'c' && flag[2] == 0) return \"compile-only\";@NL@"
            + "    if (flag[1] == 'f') return \"runtime-check\";@NL@"
            + "    return \"other\";@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "const char *flag_intent(const char *flag) {@NL@    if (flag[0] != '-') return \"other\";@NL@    if (flag[1] == 'W') {@NL@        if (flag[2] == 'e') return \"warnings\";@NL@        return \"warnings\";@NL@    }@NL@    if (flag[1] == 'g' && flag[2] == 0) return \"debug-info\";@NL@"
            + "    if (flag[1] == 'O') return \"optimization\";@NL@"
            + "    if (flag[1] == 'c' && flag[2] == 0) return \"optimization\";@NL@"
            + "    if (flag[1] == 'f') return \"runtime-check\";@NL@"
            + "    return \"other\";@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca14-dependency-closure",
            C_PRELUDE
            + "int header_touch_breaks(size_t n_objects, const int *obj_uses_header, size_t n_uses) {@NL@    (void)n_objects;@NL@    int count = 0;@NL@    for (size_t i = 0; i < n_uses; i++) {@NL@        if (obj_uses_header[i]) count++;@NL@    }@NL@    return count;@NL@}@NL@"
            + "int stale_objects_possible(int rule_includes_header) {@NL@    return rule_includes_header ? 0 : 1;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int header_touch_breaks(size_t n_objects, const int *obj_uses_header, size_t n_uses) {@NL@    (void)n_objects;@NL@    int count = 0;@NL@    for (size_t i = 0; i < n_uses; i++) {@NL@        if (!obj_uses_header[i]) count++;@NL@    }@NL@    return count;@NL@}@NL@"
            + "int stale_objects_possible(int rule_includes_header) {@NL@    return rule_includes_header ? 0 : 1;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M14,
    L14CP,
    "Checkpoint: The Graph and the Radar",
    "Consolidated build-engineering checkpoint.",
    12,
    """
Checkpoint for module 14: model rebuild decisions exactly, route flags to their intent classes, and prove why incomplete dependency graphs lie.
""",
    "Kiểm tra: Đồ thị và radar",
    "Kiểm tra tổng hợp kỹ thuật build.",
    """
Kiểm tra mô-đun 14: mô hình hóa quyết định dựng lại chính xác, điều phối cờ đúng lớp ý định, và chứng minh vì sao đồ thị phụ thuộc thiếu sót nói dối.
""",
)

write_checkpoint(
    M14,
    L14CP,
    "Checkpoint: Build Decisions",
    "One program: a rebuild-decision engine with phony handling and a strictness toggle, plus a dependency-closure calculator.",
    16,
    "See lesson.",
    "Kiểm tra: Quyết định build",
    "Một chương trình: engine quyết định dựng lại với xử lý phony và công tắc nghiêm ngặt, cộng máy tính đóng phụ thuộc.",
    "Xem bài học.",
    challenge(
        "ca14-checkpoint-rebuild",
        "Checkpoint: Rebuild Engine",
        "Implement three functions:@CE@1. `int rebuild(long long tgt, const long long *deps, size_t n, int phony, int strict)` — rebuilds if phony; else if strict, any prerequisite *not older* than the target triggers (>=); else only strictly newer (>).@CE@2. `size_t count_rebuilds(long long tgt, const long long *obj_mtimes, size_t n)` — how many object files (as targets of their own rules) are older than the changed source at tgt... model: count objects whose mtime < tgt (they will rebuild).@CE@3. `const char *strictness_effect(int strict)` — return \"more rebuilds\" for strict=1, \"fewer rebuilds\" for strict=0.",
        C_PRELUDE,
        [
            ("engine semantics", "long long d[2] = {100, 105};@NL@CHECK_EQ(rebuild(102, d, 2, 0, 0), 1);@NL@CHECK_EQ(rebuild(105, d, 2, 0, 0), 0);@NL@CHECK_EQ(rebuild(105, d, 2, 0, 1), 1);", "Strict mode treats equal timestamps as stale (>=); standard mode requires strictly newer."),
            ("phony overrides", "long long d2[1] = {5};@NL@CHECK_EQ(rebuild(10, d2, 1, 1, 0), 1);", "Phony targets rebuild regardless of timestamps."),
            ("stale object count", "long long o[3] = {90, 105, 110};@NL@CHECK_EQ((int)count_rebuilds(100, o, 3), 1);", "Only the object older than the source rebuilds."),
            ("strictness documented", "CHECK_STR_EQ(strictness_effect(1), \"more rebuilds\");@NL@CHECK_STR_EQ(strictness_effect(0), \"fewer rebuilds\");", "The toggle's meaning, as text."),
        ],
        level="mini-build",
    ),
    {
        "ca14-checkpoint-rebuild": vi_challenge(
            "Kiểm tra: Engine dựng lại",
            "Cài rebuild (phony dựng luôn; strict dùng >=; thường dùng >), count_rebuilds (đếm object cũ hơn nguồn), strictness_effect.",
            [
                ("ngữ nghĩa engine", "Chế độ strict coi timestamp bằng nhau là cũ (>=); chế độ thường đòi strictly newer."),
                ("phony ghi đè", "Target phony dựng lại bất kể timestamp."),
                ("đếm object cũ", "Chỉ object cũ hơn nguồn mới được dựng lại."),
                ("nghĩa của strict", "Ý nghĩa của công tắc, dưới dạng văn bản."),
            ],
        )
    },
    solution=C_PRELUDE
    + "int rebuild(long long tgt, const long long *deps, size_t n, int phony, int strict) {@NL@    if (phony) return 1;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (strict ? (deps[i] >= tgt) : (deps[i] > tgt)) return 1;@NL@    }@NL@    return 0;@NL@}@NL@"
    + "size_t count_rebuilds(long long tgt, const long long *obj_mtimes, size_t n) {@NL@    size_t c = 0;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (obj_mtimes[i] < tgt) c++;@NL@    }@NL@    return c;@NL@}@NL@"
    + "const char *strictness_effect(int strict) { return strict ? \"more rebuilds\" : \"fewer rebuilds\"; }@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "int rebuild(long long tgt, const long long *deps, size_t n, int phony, int strict) {@NL@    if (phony) return 0;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (deps[i] > tgt) return 1;@NL@    }@NL@    return 0;@NL@}@NL@"
    + "size_t count_rebuilds(long long tgt, const long long *obj_mtimes, size_t n) {@NL@    size_t c = 0;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (obj_mtimes[i] > tgt) c++;@NL@    }@NL@    return c;@NL@}@NL@"
    + "const char *strictness_effect(int strict) { return strict ? \"fewer rebuilds\" : \"more rebuilds\"; }@NL@"
    + "int main(void) { return 0; }",
)
