#!/usr/bin/env python3
"""C++ Advanced — module 12 (ub-defensive), 13 (debugging), 14 (testing)."""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 12: ub-defensive ============================
M12 = "ub-defensive"

L12A = "the-ub-zoo"
L12B = "defensive-boundaries"
L12C = "sanitizer-mindset"
L12D = "cppa-checkpoint-ub"

write_module(
    M12,
    "Undefined Behavior & Defensive C++",
    "The UB zoo, boundaries that make bad input impossible, and the sanitizer mindset that turns heisenbugs into test failures.",
    "Hành vi Không Xác Định & C++ Phòng Thủ",
    "Vườn thú UB, biên giới khiến đầu vào xấu trở nên bất khả, và tư duy sanitizer biến heisenbug thành test fail.",
    [L12A, L12B, L12C, L12D],
    ["m12-boundary-practice", "m12-repair-practice"],
)

write_lesson(
    M12, L12A,
    "The UB Zoo",
    "Signed overflow, out-of-bounds, dangling lifetimes, invalid iterators, data races — what the standard actually says and why the optimizer treats UB as permission.",
    12,
    r'''
## UB is not "crash"

Undefined behavior means the standard imposes **no requirements**. The optimizer is allowed to assume UB never happens — and it does assume exactly that: a check like `if (i + 1 < i)` is deleted as impossible (signed overflow is UB), loops containing UB get vectorized away, and "defensive" code after UB may never run. UB is permission granted to the compiler, taken from you.

## The zoo, by danger

- **Signed integer overflow** — UB, not wraparound. `INT_MAX + 1` can do anything. Unsigned wraps; that is defined.
- **Out-of-bounds access** — `v[i]` with `i >= v.size()` reads garbage or corrupts memory. `v.at(i)` throws instead.
- **Dangling references/iterators** — using an object past its lifetime, or an iterator invalidated by `push_back`/`erase`. The read "works" in tests and corrupts in production.
- **Data races** — two threads, one write, no synchronization (module 8). UB even if "it looks fine".
- **Uninitialized reads** — reading an uninitialized `int` is UB; `std::optional`/value-init fixes it.
- **Strict aliasing violations** — reinterpreting a `float`'s bits through an `int*` is UB; use `std::bit_cast` (C++20).

## The professional stance

You do not memorize every corner case — you build systems where UB cannot reach: checked boundaries at the edges, types that make invalid states unrepresentable, sanitizers in CI (next lessons). The graded exercises here grade the *defensive implementation*, not UB observation, because UB observation is not reproducible by definition.
''',
    "Vườn Thú UB",
    "Signed overflow, truy cập ngoài biên, thời điểm sống dang dở, iterator vô hiệu, data race — chuẩn thực sự nói gì và tại sao optimizer coi UB là giấy phép.",
    r'''
## UB không phải "crash"

Hành vi không xác định nghĩa là chuẩn **không đặt yêu cầu nào**. Optimizer được phép giả định UB không bao giờ xảy ra — và nó giả định đúng như vậy: một kiểm tra như `if (i + 1 < i)` bị xóa vì "bất khả" (signed overflow là UB), vòng lặp chứa UB bị vector hóa bỏ đi, và code "phòng thủ" sau UB có thể không bao giờ chạy. UB là giấy phép cấp cho trình biên dịch, rút từ tay bạn.

## Vườn thú, xếp theo độ nguy hiểm

- **Signed integer overflow** — UB, không phải wraparound. `INT_MAX + 1` có thể làm bất cứ gì. Unsigned thì wrap; cái đó mới có định nghĩa.
- **Truy cập ngoài biên** — `v[i]` với `i >= v.size()` đọc rác hoặc hỏng bộ nhớ. `v.at(i)` thay vào đó ném exception.
- **Tham chiếu/iterator dang dở** — dùng đối tượng sau thời điểm sống, hoặc iterator bị vô hiệu bởi `push_back`/`erase`. Trong test "chạy tốt", nơi sản xuất thì hỏng.
- **Data race** — hai thread, một ghi, không đồng bộ (module 8). UB kể cả khi "nhìn có vẻ ổn".
- **Đọc giá trị chưa khởi tạo** — đọc `int` chưa khởi tạo là UB; `std::optional`/value-init chữa được.
- **Vi phạm strict aliasing** — đọc bit của `float` qua `int*` là UB; dùng `std::bit_cast` (C++20).

## Thái độ chuyên nghiệp

Bạn không học thuộc từng góc trường hợp — bạn dựng hệ thống mà UB không thể chạm tới: biên giới có kiểm tra ở rìa, kiểu dữ liệu khiến trạng thái không hợp lệ không thể biểu diễn, sanitizer trong CI (các bài kế tiếp). Bài tập chấm điểm ở đây chấm *bản cài phòng thủ*, không phải quan sát UB, vì quan sát UB vốn không tái lập được.
''',
    difficulty="advanced",
)

write_lesson(
    M12, L12B,
    "Defensive Boundaries",
    "Validate at the edge, then trust the inside: checked conversions, at()-style access, overflow-safe arithmetic, and functions that make bad states unrepresentable.",
    11,
    r'''
## The boundary rule

Public APIs validate; internal helpers assert. A parser converts untrusted bytes into checked types at one choke point; everything downstream works with types that cannot hold invalid values. Scattered `if` checks everywhere mean the boundary is everywhere and nowhere.

## Overflow-safe arithmetic

`a + b` on ints is a trap. The professional shape:

```cpp
bool addChecked(int a, int b, int& out) {
    if (b > 0 && a > INT_MAX - b) return false;
    if (b < 0 && a < INT_MIN - b) return false;
    out = a + b;
    return true;
}
```

or C++20's `<safe_comparison>`-adjacent tools / `__builtin_add_overflow` where available. The same discipline applies to subtraction, multiplication, and index arithmetic (`i + 1` can overflow when `i == INT_MAX`).

## checked access as a type

Return `std::optional<T>` or `std::expected<T, E>`-shaped results instead of sentinel values (`-1`, `nullptr` "sometimes"). A sentinel that callers can forget to check is a bug factory; an optional is a compile-time contract.

## What the graders check here

Feeds the function adversarial inputs (INT_MAX, empty containers, sizes past the end) and requires: defined behavior, correct result or a clean failure — never garbage, never a crash. The naive implementation fails by arithmetic, deterministically.
''',
    "Biên Giới Phòng Thủ",
    "Kiểm tra ở rìa rồi tin bên trong: chuyển đổi có kiểm tra, truy cập kiểu at(), số học an toàn tràn số, và hàm khiến trạng thái xấu không thể biểu diễn.",
    r'''
## Quy tắc biên giới

API công khai kiểm tra; helper nội bộ assert. Parser chuyển byte không tin cậy thành các kiểu đã kiểm tra tại một điểm chặn duy nhất; mọi thứ hạ nguồn làm việc với các kiểu không thể chứa giá trị sai. `if` rải khắp nơi nghĩa là biên giới ở khắp nơi và ở hư không.

## Số học an toàn tràn số

`a + b` trên int là cái bẫy. Hình dạng chuyên nghiệp:

```cpp
bool addChecked(int a, int b, int& out) {
    if (b > 0 && a > INT_MAX - b) return false;
    if (b < 0 && a < INT_MIN - b) return false;
    out = a + b;
    return true;
}
```

hoặc `__builtin_add_overflow` khi có sẵn. Kỷ luật tương tự áp dụng cho trừ, nhân, và phép tính chỉ số (`i + 1` tràn khi `i == INT_MAX`).

## Truy cập có kiểm tra như một kiểu

Trả `std::optional<T>` hoặc kết quả dạng `std::expected<T, E>` thay vì giá trị cắm mốc (`-1`, `nullptr` "đôi khi"). Sentinel mà caller quên kiểm tra là nhà máy sản xuất bug; optional là hợp đồng thời gian biên dịch.

## Grader kiểm gì ở đây

Nạp vào hàm các đầu vào adversarial (INT_MAX, container rỗng, chỉ số vượt cuối) và yêu cầu: hành vi xác định, kết quả đúng hoặc thất bại sạch — không bao giờ rác, không bao giờ crash. Bản cài ngây thơ trượt bằng toán học, tất định.
''',
    difficulty="advanced",
)

write_lesson(
    M12, L12C,
    "The Sanitizer Mindset",
    "ASan, UBSan, TSan and static analysis: what each catches, when to run them, and how to design code so sanitizer findings become ordinary test failures.",
    11,
    r'''
## The four detectors

- **AddressSanitizer (`-fsanitize=address`)** — heap/stack buffer overflows, use-after-free, use-after-return. Run in every debug test run.
- **UndefinedBehaviorSanitizer (`-fsanitize=undefined`)** — signed overflow, misaligned pointers, invalid enum values, null dereferences (most of them).
- **ThreadSanitizer (`-fsanitize=thread`)** — data races via happens-before analysis. Slower (5–15x) but catches bugs no test output can.
- **Static analysis (`-fanalyzer`, clang-tidy)** — finds null-deref and lifetime paths at compile time, no execution needed.

## The CI shape

Debug builds: ASan+UBSan on, fast tests only. Nightly: TSan run of concurrency tests. Release: neither. A finding is a bug — never "probably fine". That policy only works if tests actually execute the risky paths, which is why sanitizer runs pair with coverage thinking.

## Designing for sanitizer-friendliness

- Prefer `std::vector` + `at()` in debug paths over raw pointers + manual bounds.
- Every allocation owner is a type (RAII) — ASan then has no leaks to report.
- Deterministic tests beat random stress for CI (TSan is the exception: it wants concurrency, run it on the race-prone suites).
- Fix order: real UB first, then warnings, then style. Do not teach the team to ignore reports.

The graded exercises here simulate the *outcome*: functions that would trip ASan/UBSan fail their tests by construction (checked vs unchecked implementations diverge on adversarial input).
''',
    "Tư Duy Sanitizer",
    "ASan, UBSan, TSan và phân tích tĩnh: cái nào bắt gì, chạy khi nào, và cách thiết kế code để phát hiện của sanitizer thành test fail bình thường.",
    r'''
## Bốn máy dò

- **AddressSanitizer (`-fsanitize=address`)** — tràn buffer heap/stack, use-after-free, use-after-return. Chạy trong mọi lần test debug.
- **UndefinedBehaviorSanitizer (`-fsanitize=undefined`)** — signed overflow, con trỏ lệch căn chỉnh, giá trị enum sai, dereference null (phần lớn).
- **ThreadSanitizer (`-fsanitize=thread`)** — data race qua phân tích happens-before. Chậm hơn (5–15x) nhưng bắt được bug mà đầu ra test không thể.
- **Phân tích tĩnh (`-fanalyzer`, clang-tidy)** — tìm đường null-deref và lifetime lúc biên dịch, không cần chạy.

## Hình dạng CI

Build debug: ASan+UBSan bật, chỉ test nhanh. Hằng đêm: TSan chạy các test concurrency. Release: không cái nào. Một phát hiện là một bug — không bao giờ "chắc là ổn". Chính sách đó chỉ hiệu quả nếu test thực sự chạy qua các đường rủi ro, đó là lý do sanitizer đi cùng tư duy coverage.

## Thiết kế để thân thiện với sanitizer

- Ưu tiên `std::vector` + `at()` trong đường debug thay vì con trỏ thô + tự kiểm biên.
- Mọi chủ sở hữu cấp phát là một kiểu (RAII) — ASan khi đó không còn leak để báo.
- Test tất định đánh bại stress ngẫu nhiên cho CI (TSan là ngoại lệ: nó muốn concurrency, hãy chạy trên các suite dễ race).
- Thứ tự sửa: UB thật trước, rồi warning, rồi style. Đừng dạy cả đội phớt lờ báo cáo.

Bài tập chấm điểm ở đây mô phỏng *kết quả*: hàm đáng lẽ vấp ASan/UBSan sẽ trượt test bằng cấu trúc (bản có kiểm tra vs không kiểm tra phân kỳ trên đầu vào adversarial).
''',
    difficulty="advanced",
)

# ============================ MODULE 13: debugging ============================
M13 = "debugging"

L13A = "debugger-discipline"
L13B = "crash-forensics"
L13C = "minimizing-repros"
L13D = "cppa-checkpoint-debug"

write_module(
    M13,
    "Advanced Debugging & Diagnostics",
    "Debugger discipline, reading crash forensics, and shrinking giant failures into one-file repros — the incident-response toolkit.",
    "Gỡ Lỗi Nâng Cao & Chẩn Đoán",
    "Kỷ luật dùng debugger, đọc pháp y crash, và thu nhỏ thất bại khổng lồ thành repro một file — bộ dụng cụ xử lý sự cố.",
    [L13A, L13B, L13C, L13D],
    ["m13-forensics-practice", "m13-repair-practice"],
)

write_lesson(
    M13, L13A,
    "Debugger Discipline",
    "Breakpoints, watchpoints, stepping, and the hypothesis loop: debugging as experiment design, not printf archaeology.",
    11,
    r'''
## The hypothesis loop

1. **Reproduce** reliably (same input, same failure).
2. **Localize** with the largest step that keeps the failure: binary search over the pipeline.
3. **Hypothesize** one mechanism ("the index is stale after the erase").
4. **Experiment**: breakpoint/watchpoint that distinguishes hypothesis A from B.
5. **Confirm**, fix, and *add the regression test that would have caught it*.

printf-debugging is a for-loop over guesses; the debugger is a binary search. Both are tools, but only one scales to heisenbugs.

## The moves that matter

- **Breakpoints** — stop at a line/function. Conditional breakpoints (`i == 999`) skip 998 useless stops.
- **Watchpoints** — break when a *variable changes*: the killer feature for "who corrupts this field?" (`watch -l s->count`).
- **Stepping** — `step` into, `next` over, `finish` out. Stepping through library code is noise; step your code, skip the standard library.
- **Backtrace + frame inspection** — after a crash, `bt` lists the stack; frame 0 is where it died, frames up are why.

## Post-mortem state of mind

A crash dump is a recording of the past. The skill is reading it: which frame is library-internal (skim), which is yours (study), which values are plausible vs corrupted (distrust pointers that look like small integers).
''',
    "Kỷ Luật Debugger",
    "Breakpoint, watchpoint, bước chạy, và vòng lặp giả thuyết: gỡ lỗi là thiết kế thí nghiệm, không phải khảo cổ printf.",
    r'''
## Vòng lặp giả thuyết

1. **Tái lập** đáng tin (cùng đầu vào, cùng thất bại).
2. **Địa phương hóa** bằng bước lớn nhất còn giữ thất bại: tìm kiếm nhị phân trên pipeline.
3. **Giả thuyết** một cơ chế ("chỉ số stale sau erase").
4. **Thí nghiệm**: breakpoint/watchpoint phân biệt giả thuyết A với B.
5. **Xác nhận**, sửa, và *thêm regression test lẽ ra bắt được nó*.

printf-debugging là vòng for trên các phỏng đoán; debugger là tìm kiếm nhị phân. Cả hai đều là công cụ, nhưng chỉ một cái mở rộng được cho heisenbug.

## Những nước đi quan trọng

- **Breakpoint** — dừng tại một dòng/hàm. Breakpoint có điều kiện (`i == 999`) bỏ qua 998 lần dừng vô ích.
- **Watchpoint** — dừng khi một *biến thay đổi*: vũ khí sát thủ cho câu hỏi "ai làm hỏng trường này?" (`watch -l s->count`).
- **Bước chạy** — `step` vào trong, `next` bước qua, `finish` thoát ra. Bước qua code thư viện là nhiễu; bước code của bạn, bỏ qua thư viện chuẩn.
- **Backtrace + soi frame** — sau crash, `bt` liệt kê stack; frame 0 là nơi chết, các frame trên là lý do.

## Tâm thế hậu kỳ

Crash dump là bản ghi âm của quá khứ. Kỹ năng là đọc nó: frame nào là nội bộ thư viện (lướt), frame nào là của bạn (nghiên cứu), giá trị nào hợp lý so với bị hỏng (không tin con trỏ trông như số nguyên nhỏ).
''',
    difficulty="advanced",
)

write_lesson(
    M13, L13B,
    "Crash Forensics",
    "From a stack trace and a coredump to a root cause: symbolization, reading corruption patterns, and classifying crashes by their fingerprints.",
    11,
    r'''
## Reading a stack trace like a coroner

Top frame = the immediate cause; frames below = the causal chain. Library-internal frames (`std::`, allocator) usually mean the corruption happened *earlier* — your frame that called into it is the suspect. Signature patterns:

- **Crash in `memcpy`/`std::string` internals** → often a buffer overrun or a destroyed source object.
- **Crash on `0x0`-ish addresses** → null dereference; the offset in the address names the member (`offset 8` = second field).
- **Garbage vtable pointer / wild jump** → use-after-free or virtual call on a destroyed object.
- **Heap corruption reported at a *later* allocation** → the overflow happened before; ASan's "allocated by thread" history names the scene.

## Symbolization

Addresses are useless without symbols. Debug info (`-g`) maps them back to files and lines. Release builds usually strip — keep the symbol files of each release; a crash from production + its symbols = readable stack.

## The minimal-repro discipline

Shrink the input, then the code: delete half the input — still fails? keep deleting. Delete half the code paths. A 20-line repro with a 3-byte input gets fixed same-day; the 2 GB log dump with 400 files does not. Bisection (`git bisect`) finds the *commit* that introduced it when the repro won't shrink further.
''',
    "Pháp Y Crash",
    "Từ stack trace và coredump đến nguyên nhân gốc: symbolization, đọc mẫu hư hỏng, và phân loại crash qua dấu vân tay.",
    r'''
## Đọc stack trace như pháp y

Frame trên cùng = nguyên nhân trực tiếp; các frame dưới = chuỗi nhân quả. Frame nội bộ thư viện (`std::`, allocator) thường nghĩa là hư hỏng xảy ra *sớm hơn* — frame của bạn gọi vào đó là nghi phạm. Các mẫu dấu vết:

- **Crash trong `memcpy`/nội bộ `std::string`** → thường là tràn buffer hoặc đối tượng nguồn đã bị hủy.
- **Crash tại địa chỉ gần `0x0`** → dereference null; offset trong địa chỉ gọi tên trường (`offset 8` = trường thứ hai).
- **Con trỏ vtable rác / nhảy loạn** → use-after-free hoặc gọi ảo trên đối tượng đã hủy.
- **Heap corruption bị báo tại một lần cấp phát *sau*** → phần tràn xảy ra trước đó; lịch sử "allocated by thread" của ASan chỉ hiện trường.

## Symbolization

Địa chỉ vô dụng nếu không có symbol. Debug info (`-g`) ánh xạ ngược về file và dòng. Build release thường bị strip — hãy giữ file symbol của từng bản release; crash từ production + symbol của nó = stack đọc được.

## Kỷ luật repro tối thiểu

Thu nhỏ đầu vào, rồi thu nhỏ code: xóa nửa đầu vào — vẫn fail? cứ xóa tiếp. Xóa nửa các đường code. Repo 20 dòng với đầu vào 3 byte được sửa trong ngày; dump log 2 GB với 400 file thì không. Bisection (`git bisect`) tìm *commit* gây ra khi repro không thu nhỏ được nữa.
''',
    difficulty="advanced",
)

write_lesson(
    M13, L13C,
    "Incident Repair",
    "The professional loop for a live bug: reproduce, write the failing test first, fix, prove the test passes, and leave the system more testable than you found it.",
    10,
    r'''
## Test-first repair

When a bug report arrives, the first artifact is not the fix — it is the **failing test** that reproduces the report. Benefits: proves the bug is real and reproducible; pins the exact expected behavior; and after the fix, it is a permanent regression guard.

## The loop

1. Translate the report into a test with the smallest data that triggers it.
2. Watch it fail — for the *reported reason* (not for a typo in the test).
3. Fix the minimum: no drive-by refactors inside an incident.
4. Watch the full suite: the fix must not break neighbors.
5. Write down the class of the bug (bounds? lifetime? race?) and check siblings for the same pattern.

## Blameless and systemic

"Who wrote this" is irrelevant; "what made this class of bug reachable" is the question. If an unchecked index caused it, the systemic fix is a boundary type at the API edge, not a scolding. The graded exercise here walks exactly this loop: given a described incident and a broken function, write the fixed version — graded by the failing-behavior test and the correct-behavior test both.
''',
    "Sửa Sự Cố",
    "Vòng lặp chuyên nghiệp cho một bug còn sống: tái lập, viết test fail trước, sửa, chứng minh test pass, và để lại hệ thống dễ kiểm thử hơn lúc bạn tìm thấy.",
    r'''
## Sửa kiểu test-trước

Khi một báo cáo bug đến, hiện vật đầu tiên không phải bản vá — mà là **test đang fail** tái lập báo cáo. Lợi ích: chứng minh bug có thật và tái lập được; ghim đúng hành vi kỳ vọng; và sau khi vá, nó là lá chắn hồi quy vĩnh viễn.

## Vòng lặp

1. Dịch báo cáo thành test với dữ liệu nhỏ nhất kích hoạt nó.
2. Xem nó fail — vì *lý do được báo cáo* (không phải vì typo trong test).
3. Sửa tối thiểu: không tái cấu trúc bụi bặm giữa lúc có sự cố.
4. Chạy toàn bộ suite: bản vá không được làm hỏng hàng xóm.
5. Ghi lại lớp bug (biên? lifetime? race?) và rà các chỗ anh em cùng mẫu.

## Không đổ lỗi và mang tính hệ thống

"Ai viết cái này" không quan trọng; "cái gì khiến lớp bug này với tới được" mới là câu hỏi. Nếu một chỉ số không kiểm tra gây ra nó, bản vá hệ thống là một kiểu biên giới ở rìa API, không phải một trận mắng. Bài tập chấm điểm ở đây đi đúng vòng lặp này: cho một sự cố mô tả và một hàm đang hỏng, viết bản sửa — được chấm bởi cả test hành-vi-sai lẫn test hành-vi-đúng.
''',
    difficulty="advanced",
)

# ============================ MODULE 14: testing ============================
M14 = "testing"

L14A = "beyond-unit-tests"
L14B = "property-based-testing"
L14C = "mutation-and-fuzzing"
L14D = "cppa-checkpoint-testing"

write_module(
    M14,
    "Advanced Testing & Verification",
    "Test pyramids for C++, property-based thinking, and mutation/fuzz testing that measure whether your tests can actually fail.",
    "Kiểm Thử & Xác Minh Nâng Cao",
    "Kim tự tháp test cho C++, tư duy dựa trên tính chất, và mutation/fuzz testing đo xem test của bạn có thực sự fail được không.",
    [L14A, L14B, L14C, L14D],
    ["m14-property-practice", "m14-mutant-practice"],
)

write_lesson(
    M14, L14A,
    "Beyond Unit Tests",
    "Unit, integration, and system tests have different jobs in C++; choosing the wrong level makes suites slow and lies comforting.",
    11,
    r'''
## The three levels, in C++ terms

- **Unit**: one class/free function, real objects, no I/O. Fast (ms), pinpoint failures. This is where templates and algorithms get hammered.
- **Integration**: a few real components wired together — parser + builder, pool + users. Catches contract mismatches units cannot see.
- **System**: the whole program on realistic inputs — CLI runs, file round-trips. Slow; reserved for the golden paths and the regressions that escaped.

The C++ specifics: unit tests must compile fast (heavy templates slow every TU); integration tests own the fixtures (temp files, test doubles for I/O); system tests are the only place environment variance is acceptable.

## What makes a suite trustworthy

Deterministic (same input → same result, seeds pinned), independent (order never matters), fast enough to run on every save, and *failing is always meaningful* — a flaky test is a broken test, delete or fix it today, not "retry until green".

## Testing through public behavior

Test the public API's observable behavior, not private internals — internals refactors shouldn't rewrite tests. When you are tempted to test a private helper, test it through the public path that uses it, or promote it to a named, tested utility.
''',
    "Vượt Qua Unit Test",
    "Unit, integration, và system test có vai trò khác nhau trong C++; chọn sai tầng khiến suite chậm và nói dối an ủi.",
    r'''
## Ba tầng, theo đúng nghĩa C++

- **Unit**: một class/hàm tự do, đối tượng thật, không I/O. Nhanh (ms), lỗi chính xác. Đây là nơi template và thuật toán bị rèn đòn.
- **Integration**: vài thành phần thật nối nhau — parser + builder, pool + người dùng. Bắt sự lệch hợp đồng mà unit không nhìn thấy.
- **System**: cả chương trình với đầu vào thực tế — chạy CLI, file khép kín. Chậm; dành cho đường vàng và các hồi quy lọt lưới.

Đặc thù C++: unit test phải biên dịch nhanh (template nặng làm chậm mọi TU); integration test sở hữu fixture (file tạm, test double cho I/O); system test là nơi duy nhất chấp nhận biến động môi trường.

## Điều gì khiến suite đáng tin

Tất định (cùng đầu vào → cùng kết quả, seed được ghim), độc lập (thứ tự không bao giờ quan trọng), đủ nhanh để chạy mỗi lần lưu, và *fail luôn có ý nghĩa* — test flaky là test hỏng, xóa hoặc sửa ngay hôm nay, đừng "retry tới khi xanh".

## Kiểm thử qua hành vi công khai

Test hành vi quan sát được của API công khai, không phải nội dịch riêng — refactor nội dịch không nên phải viết lại test. Khi bạn thấy muốn test một helper riêng, hãy test qua đường công khai dùng nó, hoặc thăng nó thành utility có tên và được test.
''',
    difficulty="advanced",
)

write_lesson(
    M14, L14B,
    "Property-Based Testing",
    "Instead of example inputs, state the invariant that must hold for ALL inputs — then let generated cases hunt for the violation.",
    11,
    r'''
## From examples to properties

An example test: `sort({3,1,2}) == {1,2,3}`. A property: *for every vector, sorting yields the same multiset, non-decreasing*. One property is worth a hundred examples because it covers the inputs you forgot. Classic C++ properties:

- **Round-trip**: parse(serialize(x)) == x (parsers, codecs, string formatting).
- **Involution**: compress(decompress(x)) correctness, `reverse(reverse(v)) == v`.
- **Idempotence**: `sort(sort(v)) == sort(v)`, dedup applied twice is applied once.
- **Oracles**: compare against a slow-but-obviously-correct implementation.

## Random needs structure

Pure random bytes rarely reach interesting code. Generate *structured* randoms: valid-ish inputs with occasional boundary values (0, 1, INT_MAX, empty). Deterministic seeds keep CI reproducible; the failing case is printed and shrunk to the minimal witness.

## Properties as documentation

A property states the contract so precisely that reading the test *is* reading the spec — "for all n >= 0: buildRange(n).size() == n" teaches the requirement better than prose. The graded exercises here grade property implementations: your checker function must accept correct implementations and reject subtly broken ones.
''',
    "Kiểm Thử Dựa Trên Tính Chất",
    "Thay vì đầu vào ví dụ, hãy phát biểu bất biến phải đúng với MỌI đầu vào — rồi để các trường hợp sinh tự động săn tìm vi phạm.",
    r'''
## Từ ví dụ đến tính chất

Test ví dụ: `sort({3,1,2}) == {1,2,3}`. Tính chất: *với mọi vector, sort cho cùng multiset, không giảm*. Một tính chất đáng giá trăm ví dụ vì nó phủ cả những đầu vào bạn quên. Các tính chất kinh điển của C++:

- **Khép kín vòng**: parse(serialize(x)) == x (parser, codec, format chuỗi).
- **Áp hai lần bằng một**: `reverse(reverse(v)) == v`, dedup áp hai lần bằng áp một.
- **Idempotence**: `sort(sort(v)) == sort(v)`.
- **Oracle**: so với bản cài chậm-nhưng-hiển-đúng.

## Ngẫu nhiên cần cấu trúc

Byte ngẫu nhiên thuần hiếm khi chạm code thú vị. Hãy sinh *ngẫu nhiên có cấu trúc*: đầu vào gần-hợp-lệ thỉnh thoảng kèm giá trị biên (0, 1, INT_MAX, rỗng). Seed tất định giữ CI tái lập được; trường hợp fail được in ra và thu nhỏ thành bằng chứng tối thiểu.

## Tính chất như tài liệu

Một tính chất phát biểu hợp đồng đủ chính xác để đọc test chính là đọc đặc tả — "với mọi n >= 0: buildRange(n).size() == n" dạy yêu cầu tốt hơn văn xuôi. Bài tập chấm điểm ở đây chấm bản cài tính chất: hàm kiểm tra của bạn phải chấp nhận bản cài đúng và từ chối bản cài hỏng tinh vi.
''',
    difficulty="advanced",
)

write_lesson(
    M14, L14C,
    "Mutation & Fuzz Testing",
    "Do your tests test anything? Mutants and fuzzers answer with evidence: injected bugs that must die, and structured random inputs that must not crash.",
    11,
    r'''
## Mutation testing: the mirror test

A mutant is a deliberately broken version of your code (`<` → `<=`, `+` → `-`, deleted boundary check). Run the suite against the mutant: if tests still pass, your tests cannot detect that bug class — the mutant *survived* and your suite has a hole. Mutation score = killed / total. It measures the tests, not the code.

## What mutation testing teaches

Boundary conditions (`<=` vs `<` mutants die only if tests probe the boundary), off-by-ones, and dead assertions. If every mutant of a validation function survives except syntax errors, the function is effectively untested.

## Fuzzing: the input machine

A fuzzer feeds structured-random inputs hunting for crashes, sanitizer trips, or hangs. libFuzzer-style harnesses define `LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)` calling your parser with ASan+UBSan enabled; the fuzzer's coverage feedback steers toward untested paths. Any code that parses untrusted bytes deserves a fuzz target — parsers, codecs, protocol handling.

## Where each belongs

Mutation: periodically, on critical modules, to audit the suite. Fuzzing: continuously in CI for input-facing components, with found crashes converted into permanent regression tests (the crash input becomes the test input).
''',
    "Mutation & Fuzz Testing",
    "Test của bạn có kiểm tra gì không? Mutant và fuzzer trả lời bằng bằng chứng: bug cấy ghép phải chết, và đầu vào ngẫu nhiên có cấu trúc không được phép crash.",
    r'''
## Mutation testing: tấm gương soi ngược

Một mutant là bản cố-tình-hỏng của code (`<` → `<=`, `+` → `-`, xóa kiểm tra biên). Chạy suite với mutant: nếu test vẫn pass, suite của bạn không nhận ra lớp bug đó — mutant *sống sót* và suite có lỗ hổng. Điểm mutation = bị giết / tổng số. Nó đo test, không phải code.

## Mutation testing dạy gì

Điều kiện biên (mutant `<=` vs `<` chỉ chết nếu test chạm đúng biên), off-by-one, và assert chết. Nếu mọi mutant của một hàm validation đều sống sót trừ lỗi cú pháp, hàm đó thực ra chưa được test.

## Fuzzing: cỗ máy đầu vào

Fuzzer nạp đầu vào ngẫu nhiên có cấu trúc để săn crash, vấp sanitizer, hoặc treo. Harness kiểu libFuzzer định nghĩa `LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)` gọi parser của bạn với ASan+UBSan bật; phản hồi coverage của fuzzer lái về các đường chưa test. Mọi code parse byte không tin cậy đều xứng đáng có fuzz target — parser, codec, xử lý giao thức.

## Cái nào nằm ở đâu

Mutation: định kỳ, với các module trọng yếu, để kiểm toán suite. Fuzzing: liên tục trong CI cho thành phần đón đầu vào, và crash tìm được chuyển thành regression test vĩnh viễn (đầu vào gây crash thành đầu vào test).
''',
    difficulty="advanced",
)

# ============================ module 12 practices ============================
BOUND_BOILER = r'''#include <climits>
#include <cstdint>
#include <optional>
#include <string>
#include <vector>

// Safe arithmetic at the boundary. All three must return std::nullopt on
// overflow instead of invoking UB.
std::optional<int> addChecked(int a, int b);
std::optional<int> subChecked(int a, int b);
std::optional<int> mulChecked(int a, int b);

// Checked element access: value at index, or nullopt when out of bounds.
std::optional<int> atChecked(const std::vector<int>& v, std::size_t i);
'''

M12_PRAC1_CH = [
    challenge(
        "cppa12-add-checked",
        "Overflow-Safe Addition",
        "Implement `addChecked`: returns the sum, or `std::nullopt` when it would overflow — for every signed combination, including INT_MAX/INT_MIN extremes. No signed overflow may occur in your implementation (pre-check, don't post-detect).",
        BOUND_BOILER,
        [
            ("normal additions",
             r'''CHECK_EQ(addChecked(2, 3).value_or(-999), 5);
CHECK_EQ(addChecked(-2, -3).value_or(-999), -5);
CHECK_EQ(addChecked(0, 0).value_or(-999), 0);
CHECK_EQ(addChecked(-5, 5).value_or(-999), 0);''',
             "Compute b > 0 && a > INT_MAX - b, and b < 0 && a < INT_MIN - b as the two guards; otherwise a + b is safe."),
            ("extremes are rejected, not wrapped",
             r'''CHECK(!addChecked(INT_MAX, 1).has_value());
CHECK(!addChecked(1, INT_MAX).has_value());
CHECK(!addChecked(INT_MIN, -1).has_value());
CHECK(!addChecked(-1, INT_MIN).has_value());
CHECK_EQ(addChecked(INT_MAX, 0).value_or(-999), INT_MAX);
CHECK_EQ(addChecked(INT_MIN, 0).value_or(-999), INT_MIN);''',
             "INT_MAX + 1 and INT_MIN - 1 are the exact UB traps: the guards must fire BEFORE the addition. Adding 0 never overflows."),
            ("mixed signs always safe",
             r'''CHECK_EQ(addChecked(INT_MAX, INT_MIN).value_or(-999), -1);
CHECK_EQ(addChecked(INT_MIN, INT_MAX).value_or(-999), -1);
CHECK_EQ(addChecked(INT_MAX, -1).value_or(-999), INT_MAX - 1);
CHECK_EQ(addChecked(INT_MIN, 1).value_or(-999), INT_MIN + 1);''',
             "A positive plus a negative never overflows — only same-sign sums can; make sure the guards permit mixed signs."),
        ],
        difficulty="advanced",
    ),
]

M12_PRAC1_SOL = [
    ("cppa12-add-checked",
     BOUND_BOILER + "\nstd::optional<int> addChecked(int a, int b) {\n    if (b > 0 && a > INT_MAX - b) return std::nullopt;\n    if (b < 0 && a < INT_MIN - b) return std::nullopt;\n    return a + b;\n}\nstd::optional<int> subChecked(int a, int b) {\n    if (b < 0 && a > INT_MAX + b) return std::nullopt;\n    if (b > 0 && a < INT_MIN + b) return std::nullopt;\n    return a - b;\n}\nstd::optional<int> mulChecked(int a, int b) {\n    if (a == 0 || b == 0) return 0;\n    if (a == -1 && b == INT_MIN) return std::nullopt;\n    if (b == -1 && a == INT_MIN) return std::nullopt;\n    long long r = static_cast<long long>(a) * b;\n    if (r > INT_MAX || r < INT_MIN) return std::nullopt;\n    return static_cast<int>(r);\n}\nstd::optional<int> atChecked(const std::vector<int>& v, std::size_t i) {\n    if (i >= v.size()) return std::nullopt;\n    return v[i];\n}\n",
     BOUND_BOILER + "\nstd::optional<int> addChecked(int a, int b) {\n    return a + b;  // WRONG: signed overflow is UB; no pre-check\n}\nstd::optional<int> subChecked(int a, int b) {\n    return a - b;  // WRONG\n}\nstd::optional<int> mulChecked(int a, int b) {\n    return a * b;  // WRONG\n}\nstd::optional<int> atChecked(const std::vector<int>& v, std::size_t i) {\n    return v[i];   // WRONG: unchecked\n}\n"),
]

M12_PRAC1_VI = {
    "cppa12-add-checked": {
        "title": "Phép Cộng An Toàn Tràn Số",
        "prompt": "Cài `addChecked`: trả tổng, hoặc `std::nullopt` khi sẽ tràn — với mọi tổ hợp có dấu, kể cả INT_MAX/INT_MIN. Bản cài không được phép phát sinh signed overflow (kiểm tra trước, đừng dò sau).",
        "hints": [
            "Hai điều kiện gác: b > 0 && a > INT_MAX - b, và b < 0 && a < INT_MIN - b; còn lại thì a + b an toàn.",
            "INT_MAX + 1 và INT_MIN - 1 đúng là bẫy UB: gác phải kích hoạt TRƯỚC phép cộng. Cộng 0 không bao giờ tràn.",
            "Dương cộng âm không bao giờ tràn — chỉ tổng cùng dấu mới có thể; bảo đảm gác cho phép dấu khác nhau.",
        ],
    },
}

M12_PRAC2_CH = [
    challenge(
        "cppa12-incident-repair",
        "Incident Repair: The Truncated Report",
        "Incident report: `averageOf` returned garbage for a one-element report. The broken function divides by `v.size() - 1` (a `size_t`), so an empty/one-element vector underflows the unsigned size. Repair it: return `std::nullopt` for an empty vector, and the correct mean otherwise.",
        r'''#include <cstdint>
#include <optional>
#include <vector>

// Mean of the values, or nullopt for an empty vector.
// INCIDENT: the previous version computed v.size() - 1 on unsigned size_t,
// underflowing to a gigantic divisor for empty input and returning garbage
// for one-element input. Repaired version must never underflow.
std::optional<double> averageOf(const std::vector<int>& v);
''',
        [
            ("the incident inputs are correct now",
             r'''CHECK(!averageOf({}).has_value());
CHECK_EQ(averageOf({7}).value_or(-1.0), 7.0);
CHECK_EQ(averageOf({2, 4}).value_or(-1.0), 3.0);''',
             "Guard empty first (return nullopt), then sum with a signed/wider accumulator and divide by v.size()."),
            ("mean survives extreme magnitudes",
             r'''CHECK_EQ(averageOf({INT_MAX, INT_MIN}).value_or(0.0), -0.5);
CHECK_EQ(averageOf({INT_MAX, INT_MAX}).value_or(0.0), INT_MAX * 1.0);
CHECK_EQ(averageOf({-1000000, 1000000}).value_or(0.0), 0.0);''',
             "Sum in long long (or double) BEFORE dividing — an int accumulator overflows on the INT_MAX+INT_MIN pair."),
        ],
        difficulty="advanced",
    ),
]

M12_PRAC2_SOL = [
    ("cppa12-incident-repair",
     r'''#include <cstdint>
#include <optional>
#include <vector>

std::optional<double> averageOf(const std::vector<int>& v) {
    if (v.empty()) return std::nullopt;
    long long sum = 0;
    for (int x : v) sum += x;
    return static_cast<double>(sum) / static_cast<double>(v.size());
}
''',
     r'''#include <cstdint>
#include <optional>
#include <vector>

std::optional<double> averageOf(const std::vector<int>& v) {
    if (v.empty()) return std::nullopt;
    int sum = 0;                       // WRONG: int accumulator overflows on extremes
    for (int x : v) sum += x;
    return static_cast<double>(sum) / static_cast<double>(v.size() - 1);  // WRONG: the original off-by-one underflow
}
'''),
]

M12_PRAC2_VI = {
    "cppa12-incident-repair": {
        "title": "Sửa Sự Cố: Bản Báo Bị Cắt",
        "prompt": "Báo cáo sự cố: `averageOf` trả rác với báo cáo một phần tử. Bản hỏng chia cho `v.size() - 1` (một `size_t`), nên vector rỗng/một-phần-tử làm underflow size unsigned. Hãy sửa: trả `std::nullopt` cho vector rỗng, và trung bình đúng cho các trường hợp khác.",
        "hints": [
            "Gác rỗng trước (trả nullopt), rồi cộng dồn bằng accumulator rộng/hơn có dấu và chia cho v.size().",
            "Cộng dồn trong long long (hoặc double) TRƯỚC khi chia — accumulator int tràn với cặp INT_MAX+INT_MIN.",
        ],
    },
}

# ============================ module 13 practices ============================
FORENSICS_BOILER = r'''#include <cstdint>
#include <optional>
#include <string>
#include <vector>

// A parsed crash-frame from a production stack trace:
//   "#2  0x00007f3a in App::handle + 24"  -> frame 2, module App::handle, offset 24
struct Frame {
    int index = -1;
    std::string symbol;   // "" when unresolved
    std::uint64_t offset = 0;
};

// Classify a crash from its frame list:
//   "null-deref"  : frame 0 offset in {0, 8, 16} and symbol empty
//   "heap-corrupt": frame 0 symbol starts with "memcpy" or "malloc"
//   "wild-jump"   : frame 0 symbol empty and offset > 4096
//   "in-app"      : frame 0 symbol starts with "App::"
//   "unknown"     : everything else
// Frames beyond index 0 are context. Empty list -> "unknown".
std::string classifyCrash(const std::vector<Frame>& frames);
'''

M13_PRAC1_CH = [
    challenge(
        "cppa13-crash-forensics",
        "Classify the Crash",
        "Implement `classifyCrash` per the contract in the boilerplate. This is the first skill of forensics: turning raw frames into a named failure class.",
        FORENSICS_BOILER,
        [
            ("each class is recognized",
             r'''CHECK_EQ(classifyCrash({{0, "", 8}}), "null-deref");
CHECK_EQ(classifyCrash({{0, "memcpy", 0}}), "heap-corrupt");
CHECK_EQ(classifyCrash({{0, "malloc", 4}}), "heap-corrupt");
CHECK_EQ(classifyCrash({{0, "", 8192}}), "wild-jump");
CHECK_EQ(classifyCrash({{0, "App::run", 12}}), "in-app");
CHECK_EQ(classifyCrash({{0, "std::string::append", 40}}), "unknown");''',
             "A single if-chain over frame 0 in the documented priority order; empty-symbol + small-offset means null-deref, big-offset means wild-jump."),
            ("context frames and empty input",
             r'''CHECK_EQ(classifyCrash({}), "unknown");
CHECK_EQ(classifyCrash({{1, "App::helper", 4}, {0, "", 8}}), "null-deref");
CHECK_EQ(classifyCrash({{3, "libc", 0}, {2, "std::string::append", 0}, {0, "memcpy", 0}}), "heap-corrupt");
CHECK_EQ(classifyCrash({{2, "App::x", 0}, {1, "App::y", 0}}), "unknown");''',
             "Only the frame with index 0 decides — later frames are context, and a missing index-0 frame is unknown."),
        ],
        difficulty="advanced",
    ),
]

M13_PRAC1_SOL = [
    ("cppa13-crash-forensics",
     FORENSICS_BOILER + "\nstd::string classifyCrash(const std::vector<Frame>& frames) {\n    const Frame* f0 = nullptr;\n    for (const Frame& f : frames) if (f.index == 0) { f0 = &f; break; }\n    if (!f0) return \"unknown\";\n    if (f0->symbol.empty()) return f0->offset > 4096 ? \"wild-jump\" : \"null-deref\";\n    if (f0->symbol.rfind(\"memcpy\", 0) == 0 || f0->symbol.rfind(\"malloc\", 0) == 0) return \"heap-corrupt\";\n    if (f0->symbol.rfind(\"App::\", 0) == 0) return \"in-app\";\n    return \"unknown\";\n}\n",
     FORENSICS_BOILER + "\nstd::string classifyCrash(const std::vector<Frame>& frames) {\n    if (frames.empty()) return \"unknown\";\n    const Frame& f0 = frames[0];\n    if (f0.symbol.empty() && f0.offset > 4096) return \"wild-jump\";   // WRONG: offset check before empty-symbol check\n    if (f0.symbol.empty()) return \"unknown\";                          // WRONG: misses null-deref\n    if (f0.symbol.rfind(\"memcpy\", 0) == 0 || f0.symbol.rfind(\"malloc\", 0) == 0) return \"heap-corrupt\";\n    if (f0.symbol.rfind(\"App::\", 0) == 0) return \"in-app\";\n    return \"unknown\";\n}\n"),
]

M13_PRAC1_VI = {
    "cppa13-crash-forensics": {
        "title": "Phân Loại Crash",
        "prompt": "Cài `classifyCrash` theo hợp đồng trong boilerplate. Đây là kỹ năng đầu tiên của pháp y: biến frame thô thành tên lớp thất bại.",
        "hints": [
            "Một chuỗi if trên frame 0 theo đúng thứ tự ưu tiên trong tài liệu; symbol rỗng + offset nhỏ là null-deref, offset lớn là wild-jump.",
            "Chỉ frame 0 (frame có index 0) quyết định — frame sau là bối cảnh, danh sách rỗng là unknown.",
        ],
    },
}

M13_PRAC2_CH = [
    challenge(
        "cppa13-minimal-repro",
        "The Minimal Repro",
        "A field incident: `lastUnique` was reported to return the wrong element. The contract: return the last value that appears exactly once (nullopt when none). Implement it correctly — the graded tests encode both the reported failure and the general contract.",
        r'''#include <cstdint>
#include <optional>
#include <vector>

// The last element that occurs exactly once in v; nullopt if none.
// INCIDENT REPORT: on {1, 2, 1, 3, 3} the shipped version returned 3
// (it matched "the last of a duplicate group" instead of "unique").
std::optional<int> lastUnique(const std::vector<int>& v);
''',
        [
            ("the reported case",
             r'''CHECK_EQ(lastUnique({1, 2, 1, 3, 3}).value_or(-999), 2);
CHECK_EQ(lastUnique({5}).value_or(-999), 5);
CHECK(!lastUnique({7, 7, 7}).has_value());
CHECK(!lastUnique({}).has_value());''',
             "Count occurrences (map or nested loop), then scan from the end for the first element whose count is 1."),
            ("order matters across the whole range",
             r'''CHECK_EQ(lastUnique({4, 4, 9, 9, 8}).value_or(-999), 8);
CHECK_EQ(lastUnique({8, 9, 9, 4, 4}).value_or(-999), 8);
CHECK_EQ(lastUnique({1, 2, 3, 2, 1}).value_or(-999), 3);
CHECK(!lastUnique({2, 1, 2, 1, 2}).has_value());''',
             "Count first, then a single reverse scan — checking only neighbors (v[i] vs v[i-1]) fails these mixed patterns."),
        ],
        difficulty="advanced",
    ),
]

M13_PRAC2_SOL = [
    ("cppa13-minimal-repro",
     r'''#include <cstdint>
#include <optional>
#include <unordered_map>
#include <vector>

std::optional<int> lastUnique(const std::vector<int>& v) {
    std::unordered_map<int, int> count;
    for (int x : v) ++count[x];
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        if (count[*it] == 1) return *it;
    }
    return std::nullopt;
}
''',
     r'''#include <cstdint>
#include <optional>
#include <vector>

std::optional<int> lastUnique(const std::vector<int>& v) {
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        bool dup = false;
        for (int x : v) if (x == *it && &x != &*it) { dup = true; break; }  // WRONG: still counts itself vs copies; returns duplicates
        if (!dup) return *it;
    }
    return std::nullopt;
}
'''),
]

M13_PRAC2_VI = {
    "cppa13-minimal-repro": {
        "title": "Repro Tối Thiểu",
        "prompt": "Một sự cố từ thực địa: `lastUnique` bị báo trả sai phần tử. Hợp đồng: trả giá trị cuối cùng xuất hiện đúng một lần (nullopt khi không có). Hãy cài đúng — các test chấm điểm mã hóa cả sự cố được báo lẫn hợp đồng tổng quát.",
        "hints": [
            "Đếm tần suất (map hoặc vòng lặp lồng), rồi quét từ cuối về tìm phần tử đầu tiên có count == 1.",
            "Đếm trước, rồi một lần quét ngược — chỉ nhìn hàng xóm (v[i] vs v[i-1]) sẽ trượt các mẫu xen kẽ này.",
        ],
    },
}

# ============================ module 14 practices ============================
VALID_BOILER = r'''#include <cstdint>
#include <optional>
#include <string>
#include <vector>

// A username validator for account creation.
//   length 3..20
//   first char: letter
//   rest: letter, digit or '_'
//   no two consecutive '_'
std::optional<std::string> issues(const std::string& name);
// Returns nullopt when valid; otherwise the first violated rule, one of:
//   "length", "first-char", "char-set", "double-underscore".
// (Checked in that order for names violating several rules.)
'''

M14_PRAC1_CH = [
    challenge(
        "cppa14-kill-the-mutants",
        "Kill the Mutants",
        "Implement the validator `issues` exactly per the contract. The graded tests are a mutation suite: boundary mutants (`<` vs `<=`, missing edge chars) must fail — your implementation has to be exact at every boundary to kill them all.",
        VALID_BOILER,
        [
            ("valid names pass",
             r'''CHECK(!issues("abc").has_value());
CHECK(!issues("a_1").has_value());
CHECK(!issues("Z9_").has_value());
CHECK(!issues("abcdefghij0123456789").has_value());''',
             "Length exactly 3 and exactly 20 are both valid — the boundary is inclusive on both ends."),
            ("every rule fires, in order",
             r'''CHECK_EQ(issues("ab").value_or(""), "length");
CHECK_EQ(issues("").value_or(""), "length");
CHECK_EQ(issues("1abc").value_or(""), "first-char");
CHECK_EQ(issues("_abc").value_or(""), "first-char");
CHECK_EQ(issues("abc-d").value_or(""), "char-set");
CHECK_EQ(issues("ab__c").value_or(""), "double-underscore");
CHECK(!issues("ab_c").has_value());''',
             "Check rules in the documented priority: length, then first-char, then char-set, then double-underscore."),
            ("boundary mutants die",
             r'''CHECK_EQ(issues("ab").value_or(""), "length");        // < 3
CHECK(!issues("abc").has_value());                     // == 3
CHECK(!issues("abcdefghijklmnopqrst").has_value());    // == 20
CHECK_EQ(issues("abcdefghijklmnopqrstu").value_or(""), "length");  // 21
CHECK_EQ(issues("a__b").value_or(""), "double-underscore");''',
             "Off-by-one mutants (`<` vs `<=`) survive only if the exact boundary values are untested — test both 3 and 20 exactly."),
        ],
        difficulty="advanced",
    ),
]

M14_PRAC1_SOL = [
    ("cppa14-kill-the-mutants",
     VALID_BOILER + "\nstatic bool isLetter(char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); }\nstatic bool isNameChar(char c) { return isLetter(c) || (c >= '0' && c <= '9') || c == '_'; }\nstd::optional<std::string> issues(const std::string& name) {\n    if (name.size() < 3 || name.size() > 20) return std::string(\"length\");\n    if (!isLetter(name[0])) return std::string(\"first-char\");\n    for (char c : name) if (!isNameChar(c)) return std::string(\"char-set\");\n    for (std::size_t i = 1; i < name.size(); ++i)\n        if (name[i] == '_' && name[i-1] == '_') return std::string(\"double-underscore\");\n    return std::nullopt;\n}\n",
     VALID_BOILER + "\nstatic bool isLetter(char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); }\nstatic bool isNameChar(char c) { return isLetter(c) || (c >= '0' && c <= '9') || c == '_'; }\nstd::optional<std::string> issues(const std::string& name) {\n    if (name.size() < 3 || name.size() >= 20) return std::string(\"length\");   // WRONG: boundary mutant (>= 20)\n    if (!isLetter(name[0])) return std::string(\"first-char\");\n    for (char c : name) if (!isNameChar(c)) return std::string(\"char-set\");\n    for (std::size_t i = 1; i < name.size(); ++i)\n        if (name[i] == '_' && name[i-1] == '_') return std::string(\"double-underscore\");\n    return std::nullopt;\n}\n"),
]

M14_PRAC1_VI = {
    "cppa14-kill-the-mutants": {
        "title": "Diệt Mutant",
        "prompt": "Cài validator `issues` đúng theo hợp đồng. Các test chấm điểm là một bộ mutation: mutant biên (`<` vs `<=`, thiếu ký tự cạnh) phải chết — bản cài phải chính xác tuyệt đối ở mọi biên để diệt hết.",
        "hints": [
            "Độ dài đúng 3 và đúng 20 đều hợp lệ — biên bao gồm ở cả hai đầu.",
            "Kiểm tra luật theo thứ tự ưu tiên đã ghi: length, rồi first-char, rồi char-set, rồi double-underscore.",
            "Mutant off-by-one (`<` vs `<=`) chỉ sống sót nếu giá trị biên chính xác không được test — hãy test cả 3 lẫn 20.",
        ],
    },
}

M14_PRAC2_CH = [
    challenge(
        "cppa14-property-roundtrip",
        "Property: Round-Trip Codec",
        "Implement both halves of a tiny codec and prove the round-trip property: `decode(encode(v)) == v` for every vector. Encoding: run-length, e.g. {3,3,3,5} -> \"3x3,1x5\". Decode parses that exact format back. Empty vector encodes to the empty string and decodes back to empty.",
        r'''#include <cstdint>
#include <string>
#include <vector>

// Run-length encode: {3,3,3,5} -> "3x3,1x5"  (count 'x' value, comma-separated)
std::string encode(const std::vector<int>& v);

// Inverse of encode for any string produced by encode.
std::vector<int> decode(const std::string& s);
''',
        [
            ("encode format",
             r'''CHECK_EQ(encode({}), "");
CHECK_EQ(encode({7}), "1x7");
CHECK_EQ(encode({3, 3, 3, 5}), "3x3,1x5");
CHECK_EQ(encode({1, 1, 1, 1, 1}), "5x1");
CHECK_EQ(encode({2, 3}), "1x2,1x3");''',
             "Walk the vector, count consecutive equal runs, emit \"<count>x<value>\" joined with commas."),
            ("the round-trip property",
             r'''std::vector<std::vector<int>> cases = {
    {}, {9}, {1, 2}, {5, 5, 5, 5}, {1, 2, 2, 1, 1},
    {0, 0, 0}, {-3, -3, 4}, {100, -100, 100}};
for (const auto& v : cases) {
    auto back = decode(encode(v));
    CHECK(back == v);
}''',
             "decode splits on commas, parses \"<count>x<value>\", and expands each run — round-trip then holds for all inputs including empty."),
        ],
        difficulty="advanced",
    ),
]

M14_PRAC2_SOL = [
    ("cppa14-property-roundtrip",
     r'''#include <cstdint>
#include <sstream>
#include <string>
#include <vector>

std::string encode(const std::vector<int>& v) {
    std::string out;
    for (std::size_t i = 0; i < v.size();) {
        std::size_t j = i;
        while (j < v.size() && v[j] == v[i]) ++j;
        if (!out.empty()) out += ",";
        out += std::to_string(j - i) + "x" + std::to_string(v[i]);
        i = j;
    }
    return out;
}
std::vector<int> decode(const std::string& s) {
    std::vector<int> out;
    if (s.empty()) return out;
    std::stringstream ss(s);
    std::string tok;
    while (std::getline(ss, tok, ',')) {
        auto x = tok.find('x');
        int count = std::stoi(tok.substr(0, x));
        int value = std::stoi(tok.substr(x + 1));
        out.insert(out.end(), count, value);
    }
    return out;
}
''',
     r'''#include <cstdint>
#include <sstream>
#include <string>
#include <vector>

std::string encode(const std::vector<int>& v) {
    std::string out;
    for (std::size_t i = 0; i < v.size();) {
        std::size_t j = i;
        while (j < v.size() && v[j] == v[i]) ++j;
        if (!out.empty()) out += ",";
        out += std::to_string(j - i) + "x" + std::to_string(v[i]);
        i = j;
    }
    return out;
}
std::vector<int> decode(const std::string& s) {
    std::vector<int> out;
    if (s.empty()) return out;
    std::stringstream ss(s);
    std::string tok;
    while (std::getline(ss, tok, ',')) {
        auto x = tok.find('x');
        int count = std::stoi(tok.substr(0, x));
        int value = std::stoi(tok.substr(x + 1));
        out.push_back(count);   // WRONG: pushes the count instead of expanding the run
    }
    return out;
}
'''),
]

M14_PRAC2_VI = {
    "cppa14-property-roundtrip": {
        "title": "Tính Chất: Codec Khép Kín Vòng",
        "prompt": "Cài cả hai nửa của một codec nhỏ và chứng minh tính chất khép kín vòng: `decode(encode(v)) == v` với mọi vector. Mã hóa: run-length, ví dụ {3,3,3,5} -> \"3x3,1x5\". Decode phân tích đúng định dạng đó trở lại. Vector rỗng mã hóa thành chuỗi rỗng và giải mã về rỗng.",
        "hints": [
            "Đi qua vector, đếm các run bằng nhau liên tiếp, phát \"<count>x<value>\" nối bằng dấu phẩy.",
            "decode tách theo dấu phẩy, phân tích \"<count>x<value>\", và nở mỗi run — khi đó khép kín vòng đúng với mọi đầu vào kể cả rỗng.",
        ],
    },
}

# ============================ checkpoints ============================
CP12_MD = r'''
Checkpoint on defensive C++: the full checked-arithmetic battery and a bounds-safe accessor, graded on adversarial extremes.
'''

CP12_BOILER = r'''#include <climits>
#include <cstdint>
#include <optional>
#include <string>
#include <vector>

// The defensive battery: every operation either returns its defined result
// or std::nullopt when the operation would be undefined/unsafe.
std::optional<int> addChecked(int a, int b);
std::optional<int> mulChecked(int a, int b);
std::optional<int> atChecked(const std::vector<int>& v, std::size_t i);
std::optional<int> divChecked(int a, int b);
'''

CP13_MD = r'''
Checkpoint on debugging: forensics classification plus the incident-repair loop on a real reported bug.
'''

CP14_MD = r'''
Checkpoint on testing: kill every mutant with exact boundary behavior, and hold the round-trip property on the codec.
'''

write_checkpoint(
    M12, L12D,
    "Checkpoint: Defensive C++",
    "Prove the boundary battery: add, multiply, index, and divide — each defined everywhere or nullopt, never UB.",
    19,
    CP12_MD,
    "Checkpoint: C++ Phòng Thủ",
    "Chứng minh bộ pin biên giới: cộng, nhân, truy cập chỉ số, chia — mỗi phép hoặc có kết quả xác định hoặc nullopt, không bao giờ UB.",
    r'''
Checkpoint phòng thủ: bộ pin số-học-an-toàn đầy đủ và accessor an toàn biên, chấm trên các giá trị cực đoan adversarial.
''',
    challenge(
        "cppa12-ub-checkpoint",
        "Boundary Battery",
        "Implement all four checked operations. Adversarial extremes (INT_MAX, INT_MIN, empty vector, division by zero and INT_MIN/-1) must return nullopt — the naive versions are UB.",
        CP12_BOILER,
        [
            ("addition and multiplication extremes",
             r'''CHECK(!addChecked(INT_MAX, 1).has_value());
CHECK(!addChecked(INT_MIN, -1).has_value());
CHECK(!mulChecked(INT_MAX, 2).has_value());
CHECK(!mulChecked(INT_MIN, -1).has_value());
CHECK_EQ(mulChecked(INT_MAX, 1).value_or(0), INT_MAX);
CHECK_EQ(addChecked(INT_MAX, INT_MIN).value_or(0), -1);''',
             "Pre-check with wider arithmetic or the guard identities: b>0&&a>INT_MAX-b for add; for mul, long long product then range-check (special-case INT_MIN*-1)."),
            ("bounds and division",
             r'''std::vector<int> v{10, 20};
CHECK_EQ(atChecked(v, 0).value_or(-1), 10);
CHECK(!atChecked(v, 2).has_value());
CHECK(!atChecked({}, 0).has_value());
CHECK(!divChecked(7, 0).has_value());
CHECK(!divChecked(INT_MIN, -1).has_value());
CHECK_EQ(divChecked(7, 2).value_or(0), 3);
CHECK_EQ(divChecked(-7, 2).value_or(0), -3);''',
             "atChecked: i >= v.size() -> nullopt. divChecked: b == 0 or (a == INT_MIN && b == -1) -> nullopt; C++ integer division truncates toward zero."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại biên giới",
        "Cài cả bốn phép có kiểm tra. Các giá trị cực đoan adversarial (INT_MAX, INT_MIN, vector rỗng, chia cho 0 và INT_MIN/-1) phải trả nullopt — bản ngây thơ là UB.",
        [
            ("cực đoan của cộng và nhân", "Kiểm tra trước bằng số học rộng hơn hoặc hằng đẳng thức gác: b>0&&a>INT_MAX-b cho cộng; với nhân, tích long long rồi kiểm biên (đặc biệt INT_MIN*-1)."),
            ("biên chỉ số và phép chia", "atChecked: i >= v.size() -> nullopt. divChecked: b == 0 hoặc (a == INT_MIN && b == -1) -> nullopt; phép chia nguyên C++ cắt về 0."),
        ],
    ),
    solution=CP12_BOILER + "\nstd::optional<int> addChecked(int a, int b) {\n    if (b > 0 && a > INT_MAX - b) return std::nullopt;\n    if (b < 0 && a < INT_MIN - b) return std::nullopt;\n    return a + b;\n}\nstd::optional<int> mulChecked(int a, int b) {\n    if (a == 0 || b == 0) return 0;\n    if (a == -1 && b == INT_MIN) return std::nullopt;\n    if (b == -1 && a == INT_MIN) return std::nullopt;\n    long long r = static_cast<long long>(a) * b;\n    if (r > INT_MAX || r < INT_MIN) return std::nullopt;\n    return static_cast<int>(r);\n}\nstd::optional<int> atChecked(const std::vector<int>& v, std::size_t i) {\n    if (i >= v.size()) return std::nullopt;\n    return v[i];\n}\nstd::optional<int> divChecked(int a, int b) {\n    if (b == 0) return std::nullopt;\n    if (a == INT_MIN && b == -1) return std::nullopt;\n    return a / b;\n}\n",
    wrong=CP12_BOILER + "\nstd::optional<int> addChecked(int a, int b) {\n    return a + b;   // WRONG: UB on overflow\n}\nstd::optional<int> mulChecked(int a, int b) {\n    return a * b;   // WRONG: UB on overflow\n}\nstd::optional<int> atChecked(const std::vector<int>& v, std::size_t i) {\n    return v[i];    // WRONG: unchecked\n}\nstd::optional<int> divChecked(int a, int b) {\n    if (b == 0) return std::nullopt;\n    return a / b;   // WRONG: INT_MIN / -1 is UB\n}\n",
)

write_checkpoint(
    M13, L13D,
    "Checkpoint: Debugging",
    "Classify crashes from frames and repair the reported incident — both halves of incident response, graded.",
    19,
    CP13_MD,
    "Checkpoint: Gỡ Lỗi",
    "Phân loại crash từ frame và sửa sự cố được báo — cả hai nửa của xử lý sự cố, được chấm điểm.",
    r'''
Checkpoint gỡ lỗi: phân loại pháp y cộng với vòng sửa-sau-sự-cố trên một bug được báo cáo thật.
''',
    challenge(
        "cppa13-debug-checkpoint",
        "Incident Response Gauntlet",
        "Two skills in one: `classifyCrash` (per the module-13 contract) and `repairMedian` — the incident: `medianOf` was reported to crash on empty input (it indexed v[0] before checking). Repair it: nullopt when empty, true median (average of two middles, as double) otherwise.",
        FORENSICS_BOILER + "\n#include <algorithm>\n#include <optional>\n#include <vector>\n\n// The incident: crashed on empty input (indexed v[0] unguarded).\n// Contract: nullopt when empty; otherwise the median as double — for even\n// sizes, the mean of the two middle elements of the SORTED data\n// (without reordering the caller's vector).\nstd::optional<double> repairMedian(std::vector<int> v);\n",
        [
            ("classification battery",
             r'''CHECK_EQ(classifyCrash({{0, "", 8}}), "null-deref");
CHECK_EQ(classifyCrash({{0, "memcpy", 0}}), "heap-corrupt");
CHECK_EQ(classifyCrash({{0, "", 9000}}), "wild-jump");
CHECK_EQ(classifyCrash({{0, "App::tick", 0}}), "in-app");
CHECK_EQ(classifyCrash({}), "unknown");''',
             "The documented priority chain over frame 0."),
            ("the median incident, repaired",
             r'''CHECK(!repairMedian({}).has_value());
CHECK_EQ(repairMedian({7}).value_or(-1.0), 7.0);
CHECK_EQ(repairMedian({3, 1, 2}).value_or(-1.0), 2.0);
CHECK_EQ(repairMedian({4, 1, 3, 2}).value_or(-1.0), 2.5);''',
             "Sort a local copy (by value parameter), then: odd -> middle; even -> mean of the two middles."),
            ("caller's data untouched",
             r'''std::vector<int> data{3, 1, 2};
auto m = repairMedian(data);
CHECK_EQ(m.value_or(-1.0), 2.0);
CHECK((data == std::vector<int>{3, 1, 2}));''',
             "The parameter is by-value; even so, never mutate through it — sort the local copy only."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại phản ứng sự cố",
        "Hai kỹ năng trong một: `classifyCrash` (theo hợp đồng module 13) và `repairMedian` — sự cố: `medianOf` bị báo crash với đầu vào rỗng (nó truy cập v[0] trước khi kiểm). Hãy sửa: nullopt khi rỗng, trung vị thật (trung bình hai phần tử giữa, dạng double) trong trường hợp khác.",
        [
            ("bộ pin phân loại", "Chuỗi ưu tiên đã ghi trên frame 0."),
            ("sự cố trung vị, đã sửa", "Sort một bản sao cục bộ (tham số truyền bằng giá trị), rồi: lẻ -> giữa; chẵn -> trung bình hai phần tử giữa."),
            ("dữ liệu caller không bị động vào", "Tham số truyền bằng giá trị; dù vậy, không bao giờ đột biến qua nó — chỉ sort bản sao cục bộ."),
        ],
    ),
    solution=FORENSICS_BOILER + "\n#include <algorithm>\n#include <optional>\n#include <vector>\n\nstd::string classifyCrash(const std::vector<Frame>& frames) {\n    if (frames.empty()) return \"unknown\";\n    const Frame& f0 = frames[0];\n    if (f0.symbol.empty()) return f0.offset > 4096 ? \"wild-jump\" : \"null-deref\";\n    if (f0.symbol.rfind(\"memcpy\", 0) == 0 || f0.symbol.rfind(\"malloc\", 0) == 0) return \"heap-corrupt\";\n    if (f0.symbol.rfind(\"App::\", 0) == 0) return \"in-app\";\n    return \"unknown\";\n}\nstd::optional<double> repairMedian(std::vector<int> v) {\n    if (v.empty()) return std::nullopt;\n    std::sort(v.begin(), v.end());\n    std::size_t n = v.size();\n    if (n % 2 == 1) return static_cast<double>(v[n / 2]);\n    return (static_cast<double>(v[n / 2 - 1]) + static_cast<double>(v[n / 2])) / 2.0;\n}\n",
    wrong=FORENSICS_BOILER + "\n#include <algorithm>\n#include <optional>\n#include <vector>\n\nstd::string classifyCrash(const std::vector<Frame>& frames) {\n    if (frames.empty()) return \"unknown\";\n    const Frame& f0 = frames[0];\n    if (f0.symbol.empty()) return \"unknown\";   // WRONG: misses null-deref and wild-jump\n    if (f0.symbol.rfind(\"memcpy\", 0) == 0 || f0.symbol.rfind(\"malloc\", 0) == 0) return \"heap-corrupt\";\n    if (f0.symbol.rfind(\"App::\", 0) == 0) return \"in-app\";\n    return \"unknown\";\n}\nstd::optional<double> repairMedian(std::vector<int> v) {\n    if (v.empty()) return std::nullopt;\n    std::size_t n = v.size();\n    if (n % 2 == 1) return static_cast<double>(v[n / 2]);   // WRONG: unsorted data\n    return (static_cast<double>(v[n / 2 - 1]) + static_cast<double>(v[n / 2])) / 2.0;\n}\n",
)

write_checkpoint(
    M14, L14D,
    "Checkpoint: Testing",
    "Hold the property and kill the mutants: exact validator boundaries plus a codec whose round-trip holds for every input class.",
    20,
    CP14_MD,
    "Checkpoint: Kiểm Thử",
    "Giữ vững tính chất và diệt mutant: biên validator chính xác tuyệt đối cộng codec khép kín vòng trên mọi lớp đầu vào.",
    r'''
Checkpoint kiểm thử: giết mọi mutant bằng hành vi biên chính xác, và giữ tính chất khép kín vòng của codec trên mọi lớp đầu vào.
''',
    challenge(
        "cppa14-testing-checkpoint",
        "Verification Gauntlet",
        "Implement the run-length codec (module-14 contract) AND the reversed-word validator: `isReversedPair(a, b)` is true iff b is a with all characters in reverse order (single characters and empty strings are trivially pairs). The mutation suite probes boundaries: empty, single-char, palindromes, repeated chars.",
        r'''#include <cstdint>
#include <string>
#include <vector>

// Run-length codec (see module 14): {3,3,3,5} <-> "3x3,1x5"
std::string encode(const std::vector<int>& v);
std::vector<int> decode(const std::string& s);

// True iff b == reverse(a). Empty/1-char strings are pairs of themselves.
bool isReversedPair(const std::string& a, const std::string& b);
''',
        [
            ("codec round-trip over input classes",
             r'''std::vector<std::vector<int>> cases = {
    {}, {1}, {7, 7, 7}, {1, 2, 2, 3, 3, 3, 3}, {0, -1, -1, 0}};
for (const auto& v : cases) CHECK(decode(encode(v)) == v);
CHECK_EQ(encode({2, 2, 2}), "3x2");
CHECK((decode("2x4,1x9") == std::vector<int>{4, 4, 9}));''',
             "encode runs; decode splits on ',' then expands count x value. Round-trip holds for every class."),
            ("reversed-pair boundary battery",
             r'''CHECK(isReversedPair("", ""));
CHECK(isReversedPair("x", "x"));
CHECK(isReversedPair("ab", "ba"));
CHECK(isReversedPair("abc", "cba"));
CHECK(!isReversedPair("ab", "ab"));
CHECK(isReversedPair("aa", "aa"));
CHECK(!isReversedPair("abc", "abd"));
CHECK(isReversedPair("aba", "aba"));
CHECK(isReversedPair("aab", "baa"));''',
             "Compare a[i] with b[a.size()-1-i] for all i — length mismatch first. Note \"aab\"/\"baa\" IS a pair, \"aa\"/\"aa\" is too (palindrome)."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại xác minh",
        "Cài codec run-length (hợp đồng module 14) VÀ validator từ-giáo-đảo: `isReversedPair(a, b)` đúng khi và chỉ khi b là a với mọi ký tự theo thứ tự ngược (chuỗi rỗng và một ký tự là cặp của chính nó). Bộ mutation dò biên: rỗng, một ký tự, palindrome, ký tự lặp.",
        [
            ("khép kín vòng của codec trên các lớp đầu vào", "encode các run; decode tách theo ',' rồi nở count x value. Khép kín vòng đúng với mọi lớp."),
            ("bộ pin biên của cặp đảo", "So a[i] với b[a.size()-1-i] cho mọi i — lệch độ dài thì kiểm trước. Chú ý \"aab\"/\"baa\" LÀ cặp, \"aa\"/\"aa\" cũng vậy (palindrome)."),
        ],
    ),
    solution=r'''#include <cstdint>
#include <sstream>
#include <string>
#include <vector>

std::string encode(const std::vector<int>& v) {
    std::string out;
    for (std::size_t i = 0; i < v.size();) {
        std::size_t j = i;
        while (j < v.size() && v[j] == v[i]) ++j;
        if (!out.empty()) out += ",";
        out += std::to_string(j - i) + "x" + std::to_string(v[i]);
        i = j;
    }
    return out;
}
std::vector<int> decode(const std::string& s) {
    std::vector<int> out;
    if (s.empty()) return out;
    std::stringstream ss(s);
    std::string tok;
    while (std::getline(ss, tok, ',')) {
        auto x = tok.find('x');
        int count = std::stoi(tok.substr(0, x));
        int value = std::stoi(tok.substr(x + 1));
        out.insert(out.end(), count, value);
    }
    return out;
}
bool isReversedPair(const std::string& a, const std::string& b) {
    if (a.size() != b.size()) return false;
    for (std::size_t i = 0; i < a.size(); ++i) {
        if (a[i] != b[a.size() - 1 - i]) return false;
    }
    return true;
}
''',
    wrong=r'''#include <cstdint>
#include <sstream>
#include <string>
#include <vector>

std::string encode(const std::vector<int>& v) {
    std::string out;
    for (std::size_t i = 0; i < v.size();) {
        std::size_t j = i;
        while (j < v.size() && v[j] == v[i]) ++j;
        if (!out.empty()) out += ",";
        out += std::to_string(j - i) + "x" + std::to_string(v[i]);
        i = j;
    }
    return out;
}
std::vector<int> decode(const std::string& s) {
    std::vector<int> out;
    if (s.empty()) return out;
    std::stringstream ss(s);
    std::string tok;
    while (std::getline(ss, tok, ',')) {
        auto x = tok.find('x');
        int count = std::stoi(tok.substr(0, x));
        int value = std::stoi(tok.substr(x + 1));
        out.insert(out.end(), count, value);
    }
    return out;
}
bool isReversedPair(const std::string& a, const std::string& b) {
    if (a.size() != b.size()) return false;
    for (std::size_t i = 0; i < a.size(); ++i) {
        if (a[i] != b[i]) return false;   // WRONG: compares forward — a plain equality check, not a reversal
    }
    return true;
}
''',
)

write_practice(
    M12, "m12-boundary-practice",
    "Practice: Checked Boundaries",
    "Overflow-safe arithmetic and an incident repair — both graded on adversarial input.",
    "Luyện tập: Biên Giới Có Kiểm Tra",
    "Số học an toàn tràn số và một bản sửa sự cố — đều chấm trên đầu vào adversarial.",
    L12A, 16, "advanced",
    challenges=M12_PRAC1_CH, vi_challenges=M12_PRAC1_VI, solutions=M12_PRAC1_SOL)

write_practice(
    M12, "m12-repair-practice",
    "Practice: Sanitizer-Grade Repairs",
    "Reproduce-to-test discipline on a real incident: the truncated-report average.",
    "Luyện tập: Sửa Chuẩn Sanitizer",
    "Kỷ luật tái-lập-thành-test trên một sự cố thật: bản báo trung bình bị cắt.",
    L12B, 15, "advanced",
    challenges=M12_PRAC2_CH, vi_challenges=M12_PRAC2_VI, solutions=M12_PRAC2_SOL)

write_practice(
    M13, "m13-forensics-practice",
    "Practice: Crash Forensics",
    "Turn raw frames into named failure classes — the reading skill behind every post-mortem.",
    "Luyện tập: Pháp Y Crash",
    "Biến frame thô thành tên lớp thất bại — kỹ năng đọc đằng sau mọi bản hậu mãi.",
    L13A, 14, "advanced",
    challenges=M13_PRAC1_CH, vi_challenges=M13_PRAC1_VI, solutions=M13_PRAC1_SOL)

write_practice(
    M13, "m13-repair-practice",
    "Practice: Minimal Repro & Repair",
    "Encode the reported failure as a test, then fix the function it failed against.",
    "Luyện tập: Repro Tối Thiểu & Sửa Lỗi",
    "Mã hóa thất bại được báo thành test, rồi sửa hàm mà nó fail.",
    L13B, 15, "advanced",
    challenges=M13_PRAC2_CH, vi_challenges=M13_PRAC2_VI, solutions=M13_PRAC2_SOL)

write_practice(
    M14, "m14-property-practice",
    "Practice: Properties & Mutants",
    "A validator graded by a mutation suite and a codec graded by its round-trip property.",
    "Luyện tập: Tính Chất & Mutant",
    "Một validator được chấm bằng bộ mutation và một codec được chấm bằng tính chất khép kín vòng.",
    L14A, 16, "advanced",
    challenges=M14_PRAC1_CH, vi_challenges=M14_PRAC1_VI, solutions=M14_PRAC1_SOL)

write_practice(
    M14, "m14-mutant-practice",
    "Practice: Round-Trip Codecs",
    "Build both halves of a codec and let the property test hunt for asymmetries.",
    "Luyện tập: Codec Khép Kín Vòng",
    "Dựng cả hai nửa của một codec và để tính chất test săn tìm sự bất đối xứng.",
    L14B, 15, "advanced",
    challenges=M14_PRAC2_CH, vi_challenges=M14_PRAC2_VI, solutions=M14_PRAC2_SOL)

print("modules 12-14 done")
