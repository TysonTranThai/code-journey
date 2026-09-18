#!/usr/bin/env python3
"""C Advanced — batch 8: modules 15 (debugging-forensics) and
16 (sanitizer-concepts). Zero-backslash authoring: @NL@ = statement
separator, @CE@ = newline escape inside C string literals.
Environment honesty (verified in probes): no gdb/sanitizers/valgrind/make in
the sandbox image. Debugging is modeled via invariant functions; sanitizers
are concept modules with detection-by-reasoning drills."""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ================= MODULE 15: ca-debugging-forensics ========================
M15 = "ca-debugging-forensics"

L15A = "ca-invariant-method"
L15B = "ca-repro-discipline"
L15CP = "ca-checkpoint-m15"

write_module(
    M15,
    "Debugging Forensics Without a Debugger",
    "No gdb in the graded sandbox — so this module teaches the durable skill: invariants that fail loudly, minimal repro, and assertion discipline that survives every environment.",
    "Điều tra gỡ lỗi không cần debugger",
    "Sandbox không có gdb — nên mô-đun này dạy kỹ năng bền vững: bất biến hụ ầm ầm, tái hiện tối giản, và kỷ luật assertion sống sót ở mọi môi trường.",
    [L15A, L15B, L15CP],
    ["ca-p15-forensics"],
)

write_lesson(
    M15,
    L15A,
    "Invariants: Assertions That Catch Bugs Early",
    "The proven debugging method when no debugger exists: encode what must be true, and let the violation point at the culprit.",
    16,
    """
## Debugging without symbols

Professional C work happens in environments where you cannot step through code: production, CI, embedded targets, sandboxes. The durable method is *invariant-driven debugging*: for each data structure and loop, write down the property that must always hold, then check it aggressively in debug builds.

```c
static void ds_invariant(const int *heap, size_t n) {
    for (size_t i = 1; i < n; i++) {
        size_t parent = (i - 1) / 2;
        if (heap[parent] < heap[i]) {
            fprintf(stderr, "heap invariant broken at %zu@CE@n", i);
            abort();
        }
    }
}
```

This is what `-DNDEBUG` toggles: with NDEBUG the compiler drops `assert()`; your own `_invariant` functions can stay compiled-in for tests and compiled-out for production.

## The forensic sequence

1. Reproduce — a failing input you can paste, not a story.
2. Localize — bisect: which half of the program corrupts the state?
3. Hypothesize — name the invariant you believe is broken.
4. Prove — an assertion that fires earlier than the crash.
5. Fix the cause, not the symptom — then keep the assertion.

Crashes are late. Invariants are early. A corruption found at `free()` was caused lines earlier; the assertion lattice shrinks that distance to near zero.
""",
    "Bất biến: Assertion bắt bug sớm",
    "Phương pháp gỡ lỗi đã được chứng minh khi không có debugger: mã hóa điều chắc chắn phải đúng, và để vi phạm chỉ tay vào thủ phạm.",
    """
## Gỡ lỗi khi không có symbol

Công việc C chuyên nghiệp xảy ra ở nơi không thể bước qua code: production, CI, nhúng, sandbox. Phương pháp bền vững là *gỡ lỗi dựa trên bất biến*: với mỗi cấu trúc dữ liệu và vòng lặp, viết ra tính chất luôn phải đúng, rồi kiểm tra hung hăng trong build debug.

```c
static void ds_invariant(const int *heap, size_t n) {
    for (size_t i = 1; i < n; i++) {
        size_t parent = (i - 1) / 2;
        if (heap[parent] < heap[i]) {
            fprintf(stderr, "heap invariant broken at %zu@CE@n", i);
            abort();
        }
    }
}
```

Đây là điều `-DNDEBUG` bật/tắt: có NDEBUG trình biên dịch bỏ `assert()`; các hàm `_invariant` của bạn có thể giữ lại trong build kiểm thử và loại trong production.

## Trình tự điều tra

1. Tái hiện — đầu vào lỗi có thể dán lại được, không phải một câu chuyện.
2. Định vị — chia đôi: nửa nào của chương trình hủy hoại trạng thái?
3. Giả thuyết — nêu tên bất biến bạn tin đã vỡ.
4. Chứng minh — assertion phát trước khi crash.
5. Sửa nguyên nhân, không phải triệu chứng — rồi giữ lại assertion.

Crash là muộn. Bất biến là sớm. Sự hủy hoại phát hiện tại `free()` vốn được gây ra trước đó nhiều dòng; lưới assertion rút ngắn khoảng cách đó về gần bằng không.
""",
)

write_lesson(
    M15,
    L15B,
    "Minimal Reproductions and Assert Discipline",
    "Shrinking a failure to its smallest form — and what belongs in an assertion versus what belongs in real error handling.",
    15,
    """
## The repro is the unit of work

A bug report says 'it crashes sometimes'. A repro says 'this 12-line program, compiled with these flags, prints X but must print Y'. The second one is half-solved. Professional practice: strip a failing case until removing one more line makes it pass. The shrunk repro usually *reveals* the cause — the act of minimizing is diagnosis.

In graded sandboxes without debuggers, repro discipline doubles as your test harness: every diagnosed defect becomes a permanent regression test. This course's two-sided challenges (reference passes, mutants fail) are exactly that artifact.

## assert() is a contract, not error handling

```c
/* contract: caller promised non-NULL and sorted */
assert(buf != NULL);
assert(is_sorted(buf, n));

/* runtime condition: user input CAN be bad - handle it */
if (n == 0) return -1;             /* error path, not assert */
if (read(fd, buf, cap) < 0) ...    /* errno path, not assert */
```

Assert conditions must be *impossible by contract*. If a condition can legitimately happen (bad user input, file missing, allocation failure), it is error handling, and putting it in an assert makes your release build lie. Getting this distinction right is the difference between an assertion lattice and a minefield.
""",
    "Tái hiện tối giản và kỷ luật assert",
    "Thu nhỏ một lỗi về dạng nhỏ nhất — và cái gì thuộc về assertion, cái gì thuộc về xử lý lỗi thật.",
    """
## Repro là đơn vị công việc

Báo lỗi nói 'đôi khi nó crash'. Repro nói 'chương trình 12 dòng này, biên dịch với cờ này, in X nhưng phải in Y'. Cái thứ hai đã giải được một nửa. Thực hành chuyên nghiệp: cắt một case lỗi cho đến khi bỏ thêm một dòng nữa là nó pass. Repro thu nhỏ thường *bộc lộ* nguyên nhân — hành động tối thiểu hóa chính là chẩn đoán.

Trong sandbox không có debugger, kỷ luật repro kiêm luôn vai trò harness kiểm thử: mỗi lỗi được chẩn đoán trở thành regression test vĩnh viễn. Các bài two-sided của khóa học này (tham chiếu pass, mutant fail) chính là artifact đó.

## assert() là hợp đồng, không phải xử lý lỗi

```c
/* hợp đồng: người gọi đã hứa non-NULL và đã sắp xếp */
assert(buf != NULL);
assert(is_sorted(buf, n));

/* điều kiện lúc chạy: input người dùng CÓ THỂ xấu - xử lý nó */
if (n == 0) return -1;             /* nhánh lỗi, không phải assert */
if (read(fd, buf, cap) < 0) ...    /* nhánh errno, không phải assert */
```

Điều kiện assert phải là *không thể xảy ra theo hợp đồng*. Nếu điều kiện có thể xảy ra hợp lệ (input xấu, thiếu file, lỗi cấp phát), đó là xử lý lỗi, và đặt nó vào assert khiến build release của bạn nói dối. Phân biệt đúng là khác biệt giữa lưới assertion và bãi mìn.
""",
)

write_practice(
    M15,
    "ca-p15-forensics",
    "Forensics Drills",
    "Invariant lattices, binary-search diagnosis, and repro discipline — as testable functions.",
    "Bài tập điều tra",
    "Lưới bất biến, chẩn đoán chia đôi, và kỷ luật repro — dưới dạng hàm kiểm thử được.",
    L15A,
    20,
    "advanced",
    [
        challenge(
            "ca15-heap-invariant",
            "Heap Invariant Checker",
            "Implement `bool heap_ok(const int *a, size_t n)` verifying the max-heap invariant: every node >= its children. NULL with n>0 violates; n<=1 is trivially ok.",
            C_PRELUDE,
            [
                ("valid heap passes", "int good[5] = {9, 7, 8, 3, 1};@NL@CHECK(heap_ok(good, 5));", "Each parent (9,7,8) dominates its children — the lattice holds."),
                ("broken heap caught", "int bad[5] = {9, 10, 8, 3, 1};@NL@CHECK(!heap_ok(bad, 5));", "Child 10 exceeds parent 9: invariant violated at the first interior node."),
                ("boundary cases", "int good2[1] = {5};@NL@CHECK(heap_ok(NULL, 0));@NL@CHECK(heap_ok(good2, 1));", "Empty and single-node heaps are trivially valid; NULL with n>0 is not a heap."),
            ],
            level="guided",
        ),
        challenge(
            "ca15-bisect-diagnosis",
            "Bisect the Corruption",
            "A pipeline of n stages transforms a value; exactly one stage is broken (it flips sign). You receive the stage functions pre-implemented in your editor and must implement `size_t find_bad_stage(const int *injections, size_t n)` — injections holds each stage's output for the known input; find the first index where the value's sign differs from injections[0]'s sign (all stages before the bad one preserve it, all after inherit the flip).",
            C_PRELUDE + "static int apply_stage(int v) { return v; }@NL@",
            [
                ("finds the first flip", "int in1[5] = {2, 2, -2, -2, -2};@NL@CHECK_EQ((int)find_bad_stage(in1, 5), 2);", "Sign flips at index 2; everything after is downstream of the corruption."),
                ("no corruption", "int in2[4] = {3, 3, 3, 3};@NL@CHECK_EQ((int)find_bad_stage(in2, 4), 4);", "No flip means no bad stage — return n (sentinel for 'none')."),
                ("localizes the flip, not the value change", "int in3[3] = {5, 3, -7};@NL@CHECK_EQ((int)find_bad_stage(in3, 3), 2);", "The value changed at index 1 without a sign flip — not the corruption; the sign first differs from injections[0] at index 2."),
            ],
            level="combination",
        ),
        challenge(
            "ca15-assert-vs-error",
            "Contract or Error Path?",
            "Implement `const char *classify_condition(int kind)` mapping: 0 (NULL from malloc) → \"error-handling\", 1 (user typed negative size) → \"error-handling\", 2 (internal: node->next == node in an acyclic list) → \"assert\", 3 (file open failure) → \"error-handling\", 4 (internal: popped an empty stack the API forbids) → \"assert\". The rule: caller-controllable or environmental → handle; contract-impossible → assert.",
            C_PRELUDE,
            [
                ("environmental conditions", "CHECK_STR_EQ(classify_condition(0), \"error-handling\");@NL@CHECK_STR_EQ(classify_condition(3), \"error-handling\");", "Allocation failure and file errors happen in correct programs — they need error paths, not asserts."),
                ("contract violations", "CHECK_STR_EQ(classify_condition(2), \"assert\");@NL@CHECK_STR_EQ(classify_condition(4), \"assert\");", "A cycle in an acyclic list or a forbidden pop is an internal bug — assert fires in debug, aborts loudly."),
                ("user input", "CHECK_STR_EQ(classify_condition(1), \"error-handling\");", "User input is never contract-impossible."),
            ],
            level="imitation",
        ),
        challenge(
            "ca15-shrink-repro",
            "Shrink the Repro",
            "Given a boolean test over a bitmask (bit i = keep element i), implement `unsigned int shrink(unsigned int failing, size_t width, pred_fn pred)` — pred(bits) returns true iff the masked element subset still fails; return the smallest subset (as bits) that still fails. Simple greedy: try removing each kept element from the highest index down; keep the removal if it still fails. Never reduce below a single element — a repro must still exercise the failure.",
            C_PRELUDE + "typedef bool (*pred_fn)(unsigned int);@NL@",
            [
                ("shrinks to minimal failing subset", "CHECK_EQ((int)shrink(0b1111u, 4, pred_all_fail), 1);", "pred_all_fail always returns true, so deletion proceeds until a single element remains — a repro keeps one; the lowest bit survives, value 1."),
                ("irreducible case", "CHECK_EQ((int)shrink(0b101u, 3, pred_pair_fail), 0b101u);", "pred_pair_fail only fails with both bits set — neither removal still fails, so the repro is already minimal."),
            ],
            level="combination",
        ),
    ],
    {
        "ca15-heap-invariant": vi_challenge(
            "Kiểm tra bất biến heap",
            "Cài heap_ok xác minh bất biến max-heap: mọi node >= con của nó.",
            [
                ("heap hợp lệ pass", "Mỗi cha (9,7,8) trội hơn con — lưới bất biến giữ vững."),
                ("bắt heap vỡ", "Con 10 vượt cha 9: vi phạm tại node trong đầu tiên."),
                ("trường hợp biên", "Heap rỗng và một node hợp lệ hiển nhiên; NULL với n>0 không phải heap."),
            ],
        ),
        "ca15-bisect-diagnosis": vi_challenge(
            "Chia đôi tìm hủy hoại",
            "Có sẵn hàm stage. Cài find_bad_stage — tìm chỉ số đầu tiên dấu bị lật.",
            [
                ("tìm lật đầu tiên", "Dấu lật tại index 2; mọi thứ sau nằm hạ nguồn của hủy hoại."),
                ("không hủy hoại", "Không lật nghĩa là không stage lỗi — trả n (cờ 'không có')."),
                ("định vị lật dấu", "Giá trị đổi ở index 1 nhưng không lật dấu — không phải hủy hoại; dấu khác injections[0] lần đầu tại index 2."),
            ],
        ),
        "ca15-assert-vs-error": vi_challenge(
            "Hợp đồng hay nhánh lỗi?",
            "Cài classify_condition phân loại: môi trường/người gọi kiểm soát → xử lý lỗi; không thể xảy ra theo hợp đồng → assert.",
            [
                ("điều kiện môi trường", "Lỗi cấp phát và lỗi file xảy ra cả trong chương trình đúng — chúng cần nhánh lỗi, không phải assert."),
                ("vi phạm hợp đồng", "Chu trình trong danh sách không chu kỳ là bug nội bộ — assert phát khi debug, abort ầm ầm."),
                ("input người dùng", "Input người dùng không bao giờ 'không thể theo hợp đồng'."),
            ],
        ),
        "ca15-shrink-repro": vi_challenge(
            "Thu nhỏ repro",
            "Cài shrink: thử bỏ từng phần tử được giữ từ chỉ số cao xuống; giữ phép bỏ nếu vẫn còn lỗi. Không giảm dưới một phần tử — repro vẫn phải còn lỗi.",
            [
                ("thu về tập tối tiểu", "pred_all_fail luôn true nên phép xóa chạy đến khi còn đúng một phần tử — repro phải giữ lại một; bit thấp nhất còn lại, giá trị 1."),
                ("trường hợp bất khả giảm", "pred_pair_fail chỉ lỗi khi cả hai bit được đặt — repro đã tối tiểu."),
            ],
        ),
    },
    solutions=[
        (
            "ca15-heap-invariant",
            C_PRELUDE
            + "bool heap_ok(const int *a, size_t n) {@NL@    if (n <= 1) return true;@NL@    for (size_t i = 1; i < n; i++) {@NL@        size_t parent = (i - 1) / 2;@NL@        if (a[parent] < a[i]) return false;@NL@    }@NL@    return true;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "bool heap_ok(const int *a, size_t n) {@NL@    if (n <= 1) return true;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (a[i] < 0) return false;@NL@    }@NL@    return true;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca15-bisect-diagnosis",
            C_PRELUDE
            + "static int apply_stage(int v) { return v; }@NL@"
            + "size_t find_bad_stage(const int *injections, size_t n) {@NL@    if (n == 0) return 0;@NL@    int ref_sign = (injections[0] >= 0) ? 1 : -1;@NL@    for (size_t i = 0; i < n; i++) {@NL@        int s = (injections[i] >= 0) ? 1 : -1;@NL@        if (s != ref_sign) return i;@NL@    }@NL@    return n;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "static int apply_stage(int v) { return v; }@NL@"
            + "size_t find_bad_stage(const int *injections, size_t n) {@NL@    for (size_t i = 0; i + 1 < n; i++) {@NL@        if (injections[i] != injections[i + 1]) return i + 1;@NL@    }@NL@    return n;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca15-assert-vs-error",
            C_PRELUDE
            + "const char *classify_condition(int kind) {@NL@    switch (kind) {@NL@    case 0: return \"error-handling\";@NL@    case 1: return \"error-handling\";@NL@    case 2: return \"assert\";@NL@    case 3: return \"error-handling\";@NL@    case 4: return \"assert\";@NL@    default: return \"error-handling\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "const char *classify_condition(int kind) {@NL@    switch (kind) {@NL@    case 0: return \"assert\";@NL@    case 1: return \"assert\";@NL@    case 2: return \"assert\";@NL@    case 3: return \"error-handling\";@NL@    case 4: return \"error-handling\";@NL@    default: return \"error-handling\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca15-shrink-repro",
            C_PRELUDE
            + "typedef bool (*pred_fn)(unsigned int);@NL@"
            + "bool pred_all_fail(unsigned int b) { (void)b; return true; }@NL@"
            + "bool pred_pair_fail(unsigned int b) { return b == 0b101u; }@NL@"
            + "unsigned int shrink(unsigned int failing, size_t width, pred_fn pred) {@NL@    unsigned int cur = failing;@NL@    for (size_t i = width; i-- > 0;) {@NL@        if ((cur & (cur - 1)) == 0) break;@NL@        unsigned int bit = 1u << i;@NL@        if (cur & bit) {@NL@            unsigned int trial = cur & ~bit;@NL@            if (pred(trial)) cur = trial;@NL@        }@NL@    }@NL@    return cur;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "typedef bool (*pred_fn)(unsigned int);@NL@"
            + "bool pred_all_fail(unsigned int b) { (void)b; return true; }@NL@"
            + "bool pred_pair_fail(unsigned int b) { return b == 0b101u; }@NL@"
            + "unsigned int shrink(unsigned int failing, size_t width, pred_fn pred) {@NL@    unsigned int cur = failing;@NL@    for (size_t i = width; i-- > 0;) {@NL@        unsigned int bit = 1u << i;@NL@        if (cur & bit) {@NL@            cur &= ~bit;@NL@        }@NL@    }@NL@    return cur;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

# ================= MODULE 16: ca-sanitizer-concepts =========================
M16 = "ca-sanitizer-concepts"

L16A = "ca-sanitizer-mindset"
L16B = "ca-detection-by-reasoning"
L16CP = "ca-checkpoint-m16"

write_module(
    M16,
    "Sanitizers: Concepts and Detection Without Them",
    "What ASan/UBSan/TSan actually detect, why they belong in every CI — and, because this sandbox ships none of them, how to find the same defect classes by disciplined reasoning.",
    "Sanitizer: khái niệm và phát hiện khi không có chúng",
    "ASan/UBSan/TSan thực sự phát hiện gì, vì sao chúng thuộc về mọi CI — và vì sandbox này không có, cách tìm đúng lớp lỗi đó bằng lý luận có kỷ luật.",
    [L16A, L16B, L16CP],
    ["ca-p16-detection"],
)

write_lesson(
    M16,
    L16A,
    "What Each Sanitizer Sees",
    "The defect classes each tool targets — honestly labeled: these tools are NOT available in this course's execution environment.",
    15,
    """
## Environment honesty first

This course's execution sandbox has no AddressSanitizer, no UBSan, no TSan, no Valgrind, no gdb. The *skills* below are taught as reasoning drills; the *tools* are described so you can run them in your own environment. Both halves are professional knowledge.

## The tool map (run these locally, not here)

- **ASan** (compile with `-fsanitize=address`): use-after-free, buffer overflow (heap/stack/global), double free, invalid frees. Slowdown ~2x; shadow-memory technique.
- **UBSan** (`-fsanitize=undefined`): signed overflow, invalid shifts, misaligned access, null dereference — each caught *at the moment it executes*.
- **TSan** (`-fsanitize=thread`): data races via happens-before tracking.
- **LSan** (bundled with ASan on most platforms): leak reports at exit.
- **Valgrind** (dynamic binary instrumentation): memory errors and leaks without recompiling, at larger slowdowns.

## Why they change how you write code

A sanitizer converts silent corruption into an immediate, attributed abort. Teams that adopt them in CI stop debugging mysteries because mysteries never reach production. The reasoning drills in the next lesson give you the same early-detection instinct for environments without the tools — including this one.
""",
    "Từng sanitizer thấy gì",
    "Lớp lỗi mỗi công cụ nhắm tới — ghi nhãn trung thực: các công cụ này KHÔNG có trong môi trường thực thi của khóa học.",
    """
## Trung thực về môi trường trước tiên

Sandbox thực thi của khóa học không có AddressSanitizer, UBSan, TSan, Valgrind, hay gdb. *Kỹ năng* dưới đây được dạy dưới dạng bài lý luận; *công cụ* được mô tả để bạn tự chạy trong môi trường của mình. Cả hai nửa đều là kiến thức chuyên nghiệp.

## Bản đồ công cụ (chạy cục bộ, không phải ở đây)

- **ASan** (biên dịch với `-fsanitize=address`): use-after-free, tràn buffer (heap/stack/global), double free, free không hợp lệ. Chậm hơn ~2 lần; kỹ thuật shadow-memory.
- **UBSan** (`-fsanitize=undefined`): tràn số có dấu, shift không hợp lệ, truy cập lệch alignment, deref null — mỗi cái bị bắt *tại thời điểm nó thực thi*.
- **TSan** (`-fsanitize=thread`): data race qua theo dõi happens-before.
- **LSan** (kèm ASan trên đa số nền tảng): báo cáo rò rỉ lúc thoát.
- **Valgrind** (thiết bị hóa nhị phân động): lỗi bộ nhớ và rò rỉ không cần biên dịch lại, với độ trễ lớn hơn.

## Vì sao chúng thay đổi cách bạn viết code

Sanitizer biến hủy hoại im lặng thành abort ngay lập tức, có nguồn. Nhóm áp dụng chúng trong CI ngừng gỡ các vụ bí ẩn vì bí ẩn không bao giờ tới production. Các bài lý luận ở bài học sau trao cho bạn bản năng phát hiện sớm tương tự cho môi trường không có công cụ — kể cả môi trường này.
""",
)

write_lesson(
    M16,
    L16B,
    "Detection by Reasoning",
    "The sanitizer's questions, asked by hand: who owns this memory, how long does it live, who writes it concurrently, what does the caller pass?",
    15,
    """
## Four questions catch most of what ASan catches

1. **Ownership**: who frees this? If two answers exist, expect double-free. If zero, expect a leak.
2. **Lifetime**: can this pointer outlive its object? Returned locals, stored-then-freed members, and iterator invalidation live here.
3. **Bounds**: what is the largest legal index, and what proves every access is below it? Unchecked sizes and off-by-one loops live here.
4. **Concurrency** (module 18 applies it): which threads touch this without a lock? Two writers or a writer plus a reader without synchronization is a data race by definition.

## Turning questions into executable checks

Without ASan, you *encode* the questions: an ownership table that records every allocation and its designated freer (checked at shutdown); bounds-checked accessors that assert `i < n` on every read; single-threaded-by-design or lock-discipline reviews for shared state. Weaker than the tools, but structurally the same detection — and it runs anywhere C runs, including this sandbox.

## When you do have the tools

Run them under every test, in CI, with `-Werror`-level strictness: sanitizer findings are build failures, not suggestions. The habit this module builds — name the owner, name the lifetime, name the bound — is precisely what makes sanitizer reports fast to read when you meet them.
""",
    "Phát hiện bằng lý luận",
    "Những câu hỏi của sanitizer, hỏi bằng tay: ai sở hữu bộ nhớ này, nó sống bao lâu, ai ghi nó đồng thời, caller truyền gì?",
    """
## Bốn câu hỏi bắt phần lớn những gì ASan bắt

1. **Sở hữu**: ai giải phóng cái này? Có hai câu trả lời → chờ double-free. Không có → chờ rò rỉ.
2. **Tuổi thọ**: con trỏ này có thể sống lâu hơn đối tượng của nó không? Local được trả về, thành viên lưu rồi bị free, và invalidation của iterator nằm ở đây.
3. **Giới hạn**: chỉ số hợp lệ lớn nhất là bao nhiêu, và cái gì chứng minh mọi truy cập nằm dưới nó? Kích thước không kiểm tra và vòng lặp off-by-one nằm ở đây.
4. **Đồng thời** (mô-đun 18 áp dụng): những thread nào chạm trạng thái này không có khóa? Hai writer hoặc một writer cộng một reader thiếu đồng bộ là data race theo định nghĩa.

## Biến câu hỏi thành kiểm tra chạy được

Thiếu ASan, bạn *mã hóa* câu hỏi: bảng sở hữu ghi lại mọi cấp phát và freer được chỉ định (kiểm tra lúc tắt); accessor kiểm tra giới hạn khẳng định `i < n` trên mỗi lần đọc; thiết kế đơn-thread hoặc rà soát kỷ luật khóa cho trạng thái chia sẻ. Yếu hơn công cụ, nhưng về cấu trúc là cùng một phép phát hiện — và nó chạy ở bất cứ đâu C chạy, kể cả sandbox này.

## Khi bạn có công cụ

Chạy chúng dưới mọi bài kiểm thử, trong CI, nghiêm ngặt mức `-Werror`: phát hiện của sanitizer là lỗi build, không phải gợi ý. Thói quen mô-đun này xây — nêu chủ sở hữu, nêu tuổi thọ, nêu giới hạn — chính là thứ khiến báo cáo sanitizer nhanh để đọc khi bạn gặp chúng.
""",
)

write_practice(
    M16,
    "ca-p16-detection",
    "Detection Drills",
    "The four questions as executable detectors: ownership accounting, lifetime tracking, bounds discipline, race classification.",
    "Bài tập phát hiện",
    "Bốn câu hỏi thành máy dò chạy được: kế toán sở hữu, theo dõi tuổi thọ, kỷ luật giới hạn, phân loại race.",
    L16A,
    20,
    "advanced",
    [
        challenge(
            "ca16-ownership-ledger",
            "Ownership Ledger",
            "An allocation ledger lives in your editor (`struct ent { const void *p; int freed; }; static struct ent ledger[16]; static size_t n_led;`). Implement `void own(const void *p)` (record), `void release(const void *p)` (mark freed; double-release must be detectable), and `int audit(void)` returning the count of leaked (never freed) entries — the shutdown check LSan performs.",
            C_PRELUDE + "struct ent { const void *p; int freed; };@NL@static struct ent ledger[16];@NL@static size_t n_led;@NL@",
            [
                ("leak counting", "int x = 1;@NL@own(&x);@NL@own(&x);@NL@CHECK_EQ(audit(), 2);", "Two live allocations, none freed: two leaks — the audit question answered."),
                ("released entries do not leak", "int y = 1;@NL@own(&y);@NL@release(&y);@NL@CHECK_EQ(audit(), 0);", "Marking freed before audit yields zero leaks."),
            ],
            level="guided",
        ),
        challenge(
            "ca16-lifetime-classify",
            "Lifetime Violation or Not?",
            "Implement `const char *lifetime_verdict(int kind)` for five scenarios: 0 returning a pointer to a local → \"dangling\", 1 returning a malloc'd buffer → \"valid\", 2 storing a pointer to a stack array in a global → \"dangling\", 3 returning a pointer into a static buffer → \"valid\", 4 freeing then returning the freed pointer → \"dangling\".",
            C_PRELUDE,
            [
                ("dangling scenarios", "CHECK_STR_EQ(lifetime_verdict(0), \"dangling\");@NL@CHECK_STR_EQ(lifetime_verdict(2), \"dangling\");", "The object dies at return; the pointer survives — question 2 fails."),
                ("valid scenarios", "CHECK_STR_EQ(lifetime_verdict(1), \"valid\");@NL@CHECK_STR_EQ(lifetime_verdict(3), \"valid\");", "Heap and static storage outlive the function — the pointer's lifetime is covered."),
                ("free-then-return", "CHECK_STR_EQ(lifetime_verdict(4), \"dangling\");", "Free ends the lifetime immediately; the returned pointer is use-after-free by construction."),
            ],
            level="imitation",
        ),
        challenge(
            "ca16-bounds-discipline",
            "Bounds-Checked Access",
            "Implement `int checked_get(const int *a, size_t n, size_t i, int *out)` returning 0 and writing *out on success, returning -1 without writing on out-of-range or NULL — then `int checked_sum(const int *a, size_t n)` summing via checked_get (a NULL array with n>0 must sum to 0 with -1 per element).",
            C_PRELUDE,
            [
                ("in-range reads", "int a[3] = {5, 6, 7};@NL@int v = 0;@NL@CHECK_EQ(checked_get(a, 3, 1, &v), 0);@NL@CHECK_EQ(v, 6);", "The bound is proven before every access — question 3 encoded."),
                ("out-of-range refused", "int a2[3] = {5, 6, 7};@NL@int v2 = 6;@NL@CHECK_EQ(checked_get(a2, 3, 3, &v2), -1);@NL@CHECK_EQ(v2, 6);", "Index n is one-past-the-end: refused, and out is untouched on failure (v2 still 6)."),
                ("NULL array", "int v3 = 0;@NL@CHECK_EQ(checked_get(NULL, 2, 0, &v3), -1);@NL@CHECK_EQ(checked_sum(NULL, 2), 0);", "NULL with nonzero n is refused per element; the sum degrades to 0."),
            ],
            level="guided",
        ),
        challenge(
            "ca16-race-classify",
            "Race or Not?",
            "Implement `const char *race_verdict(int kind)`: 0 two threads write a plain int without locks → \"race\", 1 two threads read a const table → \"not-a-race\", 2 one thread writes while another reads a plain int → \"race\", 3 both threads update different mutex-protected counters → \"not-a-race\", 4 two threads write distinct elements of an array → \"not-a-race\" (distinct memory objects).",
            C_PRELUDE,
            [
                ("conflicting unsynchronized access", "CHECK_STR_EQ(race_verdict(0), \"race\");@NL@CHECK_STR_EQ(race_verdict(2), \"race\");", "Two writers, or writer+reader, on the same object without synchronization: the definition of a data race."),
                ("read-only sharing", "CHECK_STR_EQ(race_verdict(1), \"not-a-race\");", "Concurrent reads never conflict."),
                ("disjoint or locked", "CHECK_STR_EQ(race_verdict(3), \"not-a-race\");@NL@CHECK_STR_EQ(race_verdict(4), \"not-a-race\");", "Distinct objects or proper locking: no conflicting pair."),
            ],
            level="imitation",
        ),
    ],
    {
        "ca16-ownership-ledger": vi_challenge(
            "Sổ cái sở hữu",
            "Có sẵn sổ cái cấp phát trong trình soạn thảo. Cài own, release (double-release phải phát hiện được), và audit (đếm rò rỉ — phép kiểm LSan làm lúc tắt).",
            [
                ("đếm rò rỉ", "Hai cấp phát còn sống, không cái nào được giải phóng: hai rò rỉ."),
                ("mục đã giải phóng không rò", "Đánh dấu freed trước audit cho kết quả không rò rỉ."),
            ],
        ),
        "ca16-lifetime-classify": vi_challenge(
            "Vi phạm tuổi thọ hay không?",
            "Cài lifetime_verdict cho 5 tình huống: local bị trả về, buffer malloc, mảng stack lưu vào global, static buffer, free rồi trả con trỏ.",
            [
                ("tình huống treo", "Đối tượng chết lúc return; con trỏ sống sót — câu hỏi 2 thất bại."),
                ("tình huống hợp lệ", "Heap và static sống lâu hơn hàm — tuổi thọ con trỏ được bao phủ."),
                ("free rồi trả", "Free kết thúc tuổi thọ ngay lập tức; con trỏ trả về là use-after-free từ thiết kế."),
            ],
        ),
        "ca16-bounds-discipline": vi_challenge(
            "Truy cập có kiểm tra giới hạn",
            "Cài checked_get (thành công ghi out, thất bại không ghi) và checked_sum dựa trên checked_get.",
            [
                ("đọc trong phạm vi", "Giới hạn được chứng minh trước mọi truy cập — câu hỏi 3 được mã hóa."),
                ("từ chối ngoài phạm vi", "Chỉ số n là one-past-the-end: bị từ chối, và out không bị đụng khi thất bại."),
                ("mảng NULL", "NULL với n>0 bị từ chối từng phần tử; tổng suy giảm về 0."),
            ],
        ),
        "ca16-race-classify": vi_challenge(
            "Race hay không?",
            "Cài race_verdict: hai writer không khóa, đọc chung, writer+reader, khóa đúng, phần tử rời nhau.",
            [
                ("xung đột thiếu đồng bộ", "Hai writer, hoặc writer+cộng reader, trên cùng đối tượng không đồng bộ: định nghĩa của data race."),
                ("chia sẻ chỉ đọc", "Đọc đồng thời không bao giờ xung đột."),
                ("rời nhau hoặc có khóa", "Đối tượng khác nhau hoặc khóa đúng: không cặp xung đột."),
            ],
        ),
    },
    solutions=[
        (
            "ca16-ownership-ledger",
            C_PRELUDE
            + "struct ent { const void *p; int freed; };@NL@static struct ent ledger[16];@NL@static size_t n_led;@NL@"
            + "void own(const void *p) { ledger[n_led].p = p; ledger[n_led].freed = 0; n_led++; }@NL@"
            + "void release(const void *p) {@NL@    for (size_t i = 0; i < n_led; i++) {@NL@        if (ledger[i].p == p && !ledger[i].freed) { ledger[i].freed = 1; return; }@NL@    }@NL@}@NL@"
            + "int audit(void) {@NL@    int leaks = 0;@NL@    for (size_t i = 0; i < n_led; i++) {@NL@        if (!ledger[i].freed) leaks++;@NL@    }@NL@    return leaks;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "struct ent { const void *p; int freed; };@NL@static struct ent ledger[16];@NL@static size_t n_led;@NL@"
            + "void own(const void *p) { (void)p; n_led++; }@NL@"
            + "void release(const void *p) { (void)p; }@NL@"
            + "int audit(void) {@NL@    int leaks = 0;@NL@    for (size_t i = 0; i < n_led; i++) {@NL@        if (i % 2 == 0) leaks++;@NL@    }@NL@    return leaks;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca16-lifetime-classify",
            C_PRELUDE
            + "const char *lifetime_verdict(int kind) {@NL@    switch (kind) {@NL@    case 0: return \"dangling\";@NL@    case 1: return \"valid\";@NL@    case 2: return \"dangling\";@NL@    case 3: return \"valid\";@NL@    case 4: return \"dangling\";@NL@    default: return \"valid\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "const char *lifetime_verdict(int kind) {@NL@    switch (kind) {@NL@    case 0: return \"valid\";@NL@    case 1: return \"valid\";@NL@    case 2: return \"valid\";@NL@    case 3: return \"dangling\";@NL@    case 4: return \"valid\";@NL@    default: return \"valid\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca16-bounds-discipline",
            C_PRELUDE
            + "int checked_get(const int *a, size_t n, size_t i, int *out) {@NL@    if (a == NULL || i >= n) return -1;@NL@    *out = a[i];@NL@    return 0;@NL@}@NL@"
            + "int checked_sum(const int *a, size_t n) {@NL@    int s = 0;@NL@    int v;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (checked_get(a, n, i, &v) == 0) s += v;@NL@    }@NL@    return s;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int checked_get(const int *a, size_t n, size_t i, int *out) {@NL@    if (a == NULL || i > n) return -1;@NL@    *out = a[i];@NL@    return 0;@NL@}@NL@"
            + "int checked_sum(const int *a, size_t n) {@NL@    int s = 0;@NL@    int v;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (checked_get(a, n, i, &v) == 0) s += v;@NL@    }@NL@    return s;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca16-race-classify",
            C_PRELUDE
            + "const char *race_verdict(int kind) {@NL@    switch (kind) {@NL@    case 0: return \"race\";@NL@    case 1: return \"not-a-race\";@NL@    case 2: return \"race\";@NL@    case 3: return \"not-a-race\";@NL@    case 4: return \"not-a-race\";@NL@    default: return \"not-a-race\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "const char *race_verdict(int kind) {@NL@    switch (kind) {@NL@    case 0: return \"not-a-race\";@NL@    case 1: return \"race\";@NL@    case 2: return \"not-a-race\";@NL@    case 3: return \"race\";@NL@    case 4: return \"race\";@NL@    default: return \"not-a-race\";@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M15,
    L15CP,
    "Checkpoint: Forensics Without a Debugger",
    "Consolidated debugging checkpoint.",
    12,
    """
Checkpoint for module 15: invariant checker, sign-flip localization, and the assert-vs-error taxonomy in one program.
""",
    "Kiểm tra: Điều tra không cần debugger",
    "Kiểm tra tổng hợp gỡ lỗi.",
    """
Kiểm tra mô-đun 15: máy kiểm bất biến, định vị lật dấu, và phân loại assert-so-với-lỗi trong một chương trình.
""",
)

write_lesson(
    M16,
    L16CP,
    "Checkpoint: Detection Without Tools",
    "Consolidated detection checkpoint.",
    12,
    """
Checkpoint for module 16: ownership ledger audit, lifetime classification, and race reasoning in one program.
""",
    "Kiểm tra: Phát hiện khi không có công cụ",
    "Kiểm tra tổng hợp phát hiện.",
    """
Kiểm tra mô-đun 16: audit sổ cái sở hữu, phân loại tuổi thọ, và lý luận race trong một chương trình.
""",
)

write_checkpoint(
    M15,
    L15CP,
    "Checkpoint: Forensic Engine",
    "One program: an invariant engine for a sorted-ring buffer (sortedness, wrap order, and size bounds as separate verdicts) plus a diagnosis classifier.",
    16,
    "See lesson.",
    "Kiểm tra: Engine điều tra",
    "Một chương trình: engine bất biến cho ring buffer có sắp xếp (sortedness, thứ tự wrap, và giới hạn kích thước là các phán quyết riêng) cộng máy phân loại chẩn đoán.",
    "Xem bài học.",
    challenge(
        "ca15-checkpoint-ring",
        "Checkpoint: Ring Forensics",
        "A ring buffer's public fields live in your editor (`struct ring { int buf[8]; size_t head, tail, count; };`). Implement three verdicts:@CE@1. `bool ring_size_ok(const struct ring *r)` — count <= capacity 8, and head/tail in [0, 8).@CE@2. `bool ring_count_matches(const struct ring *r, size_t expected)` — the recorded count equals the actual occupancy derived from head/tail/count consistency (here: count <= 8 && head < 8 && tail < 8 && (r->count == 0 ? r->head == r->tail : true)).@CE@3. `const char *diagnose(const struct ring *r)` — return \"ok\" when both verdicts hold; \"size-corrupt\" when sizes are out of range; \"index-corrupt\" when head or tail is out of range (checked first).",
        C_PRELUDE + "struct ring { int buf[8]; size_t head, tail, count; };@NL@",
        [
            ("healthy ring", "struct ring r = {{0}, 0, 0, 0};@NL@CHECK_STR_EQ(diagnose(&r), \"ok\");", "Empty ring, all indices in range: both lattices hold."),
            ("index corruption diagnosed first", "struct ring r2 = {{0}, 9, 0, 0};@NL@CHECK_STR_EQ(diagnose(&r2), \"index-corrupt\");", "head 9 is outside [0,8) — index verdict fires before size."),
            ("size corruption", "struct ring r3 = {{0}, 2, 3, 9};@NL@CHECK_STR_EQ(diagnose(&r3), \"size-corrupt\");", "count 9 exceeds capacity 8 with valid indices — size verdict."),
            ("both corrupt: index wins", "struct ring r4 = {{0}, 9, 0, 9};@NL@CHECK_STR_EQ(diagnose(&r4), \"index-corrupt\");@NL@CHECK(!ring_size_ok(&r4));@NL@CHECK(!ring_count_matches(&r4, 0));", "head 9 breaks indices AND count 9 breaks size — index is diagnosed first, and both boolean verdicts reject."),
        ],
        level="mini-build",
    ),
    {
        "ca15-checkpoint-ring": vi_challenge(
            "Kiểm tra: Điều tra ring",
            "Có sẵn các trường công khai của ring buffer. Cài ring_size_ok, ring_count_matches, và diagnose (kiểm tra index trước).",
            [
                ("ring khỏe mạnh", "Ring rỗng, mọi chỉ số trong phạm vi: cả hai lưới giữ vững."),
                ("hủy hoại chỉ số được chẩn đoán trước", "head 9 nằm ngoài [0,8) — phán quyết index phát trước size."),
                ("hủy hoại kích thước", "count 9 vượt dung lượng 8 với chỉ số hợp lệ — phán quyết size."),
            ],
        )
    },
    solution=C_PRELUDE
    + "struct ring { int buf[8]; size_t head, tail, count; };@NL@"
    + "bool ring_size_ok(const struct ring *r) { return r->count <= 8 && r->head < 8 && r->tail < 8; }@NL@"
    + "bool ring_count_matches(const struct ring *r, size_t expected) {@NL@    (void)expected;@NL@    return r->count <= 8 && r->head < 8 && r->tail < 8 && (r->count != 0 || r->head == r->tail);@NL@}@NL@"
    + "const char *diagnose(const struct ring *r) {@NL@    if (r->head >= 8 || r->tail >= 8) return \"index-corrupt\";@NL@    if (r->count > 8) return \"size-corrupt\";@NL@    return \"ok\";@NL@}@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "struct ring { int buf[8]; size_t head, tail, count; };@NL@"
    + "bool ring_size_ok(const struct ring *r) { return r->count < 8; }@NL@"
    + "bool ring_count_matches(const struct ring *r, size_t expected) {@NL@    (void)expected;@NL@    return r->count <= 8;@NL@}@NL@"
    + "const char *diagnose(const struct ring *r) {@NL@    if (r->count > 8) return \"size-corrupt\";@NL@    if (r->head >= 8 || r->tail >= 8) return \"index-corrupt\";@NL@    return \"ok\";@NL@}@NL@"
    + "int main(void) { return 0; }",
)
