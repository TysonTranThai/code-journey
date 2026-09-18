#!/usr/bin/env python3
"""C++ Beginner — module 3 (conditions) and module 4 (loops)."""
from cppb import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 3: conditions ============================
M3 = "conditions"

L3A = "if-else-and-logic"
L3B = "switch-and-branches"
L3C = "checkpoint-conditions"

write_module(
    M3,
    "Conditions",
    "Branching: if/else chains, boolean logic, and switch — plus the validation mindset that turns input into trustworthy data.",
    "Cấu trúc điều kiện",
    "Rẽ nhánh: chuỗi if/else, logic boolean, và switch — cùng tư duy validation biến dữ liệu đầu vào thành dữ liệu đáng tin.",
    [L3A, L3B, L3C],
    ["m3-if-practice", "m3-switch-practice"],
)

write_lesson(
    M3, L3A,
    "if / else and Boolean Logic",
    "The if statement, else-if chains, combining conditions with && || !, and common logic pitfalls.",
    11,
    '''
## The shape

```cpp
if (temperature > 30) {
    std::cout << "hot\\n";
} else if (temperature > 20) {
    std::cout << "warm\\n";
} else {
    std::cout << "cool\\n";
}
```

Conditions run top to bottom; the **first** true branch wins and the rest are skipped. That ordering *is* the logic: swapping the first two branches breaks the program even though every condition is "correct".

## Combining conditions

```cpp
bool can_enter = age >= 18 && has_ticket;   // both
bool discount   = is_student || is_senior;  // at least one
bool not_member = !is_member;               // negation
```

Two classic beginner pitfalls:

1. **Range chains.** `if (0 < x < 10)` compiles but does NOT test what you think — it evaluates `(0 < x) < 10`, i.e. `true/false < 10`, always true. Write `x > 0 && x < 10`.
2. **Assignment in conditions.** `if (x = 5)` assigns 5, yields 5 (truthy), and runs the branch. Compilers warn (`-Wall`) — read the warning.

## Braces are not optional in this course

C++ allows `if (x) std::cout << "yes";` without braces — and that style is how the famous Apple `goto fail` bug happened: one added line silently left the guard. **Always brace your branches**, even single-line ones. Modern style guides and this course agree.

## Validation mindset

Real programs spend most of their `if`-budget validating: is this input present? non-empty? in range? The earlier you write checks, the fewer crashes reach your logic. You will practice exactly that in this module's exercises: reject invalid input *at the door* with clear messages, then compute with confidence.
''',
    "if / else và logic boolean",
    "Câu lệnh if, chuỗi else-if, kết hợp điều kiện bằng && || !, và những bẫy logic thường gặp.",
    '''
## Dạng chuẩn

```cpp
if (temperature > 30) {
    std::cout << "hot\\n";
} else if (temperature > 20) {
    std::cout << "warm\\n";
} else {
    std::cout << "cool\\n";
}
```

Các nhánh được xét từ trên xuống; nhánh **đầu tiên** đúng sẽ thắng và phần còn lại bị bỏ qua. Chính thứ tự đó *là* logic: đổi chỗ hai nhánh đầu sẽ hỏng chương trình dù mọi điều kiện đều "đúng".

## Kết hợp điều kiện

```cpp
bool can_enter = age >= 18 && has_ticket;   // cả hai
bool discount   = is_student || is_senior;  // ít nhất một
bool not_member = !is_member;               // phủ định
```

Hai cái bẫy kinh điển của người mới:

1. **Chuỗi khoảng giá trị.** `if (0 < x < 10)` biên dịch được nhưng KHÔNG kiểm tra điều bạn nghĩ — nó tính `(0 < x) < 10`, tức `true/false < 10`, luôn đúng. Hãy viết `x > 0 && x < 10`.
2. **Gán trong điều kiện.** `if (x = 5)` gán 5, cho ra 5 (truthy), và chạy nhánh đó. Compiler có cảnh báo (`-Wall`) — hãy đọc cảnh báo.

## Ngoặc nhọn không tùy chọn trong khóa này

C++ cho phép `if (x) std::cout << "yes";` không cần ngoặc nhọn — và kiểu viết đó chính là nguồn cơn của bug `goto fail` nổi tiếng ở Apple: thêm một dòng là guard bị bỏ ngầm. **Luôn đặt ngoặc nhọn cho mọi nhánh**, kể cả một dòng. Các style guide hiện đại và khóa này cùng thống nhất.

## Tư duy validation

Chương trình thật dành phần lớn ngân sách `if` để validating: input này có tồn tại không? khác rỗng không? nằm trong khoảng không? Viết kiểm tra càng sớm, càng ít crash chạm tới phần logic. Chính xác điều đó là bài tập của module này: chặn input không hợp lệ *ngay cửa* với thông báo rõ ràng, rồi tính toán trong sự tự tin.
''',
)

write_lesson(
    M3, L3B,
    "switch and Choosing a Branch Style",
    "switch for discrete values, fall-through dangers, when switch beats if/else, and the conditional operator.",
    10,
    '''
## switch: choosing among discrete values

```cpp
switch (command) {
    case 'h':
        print_help();
        break;
    case 'q':
        quit = true;
        break;
    default:
        std::cout << "unknown command\\n";
        break;
}
```

`switch` compares one integral or enum value against `case` labels. It reads better than a long `if/else if` chain *when the tests are all equality against constants*.

## The fall-through trap (and the one legit use)

Without `break`, execution *falls through* into the next case:

```cpp
case 1:
    std::cout << "one";
    // NO break — also prints "two"!
case 2:
    std::cout << "two";
    break;
```

GCC warns about accidental fall-through (`-Wimplicit-fallthrough` with `-Wextra`). The one legitimate use — shared code for several cases — must be an *explicit* `[[fallthrough]];` comment-attribute so reviewers know it is intended. Beginners: always `break;`.

## switch vs if/else — how to choose

- Equality against a fixed set of constants (`char` command, `int` menu, `enum class` state) → `switch`.
- Ranges, compound logic, `std::string` comparisons → `if/else`.
- (`switch` on `std::string` does not work; if/else with `==` does.)

## One-liners: the conditional operator

```cpp
std::string label = (score >= 50) ? "pass" : "fail";
```

`cond ? a : b` is an *expression* — useful for initializing a variable from a tiny choice. Anything hairier belongs in a real `if`.

## Coming up

Conditions decide once; loops decide a thousand times. Next module: repetition.
''',
    "switch và cách chọn kiểu rẽ nhánh",
    "switch cho các giá trị rời rạc, nguy cơ fall-through, khi nào switch hơn if/else, và toán tử điều kiện.",
    '''
## switch: chọn giữa các giá trị rời rạc

```cpp
switch (command) {
    case 'h':
        print_help();
        break;
    case 'q':
        quit = true;
        break;
    default:
        std::cout << "unknown command\\n";
        break;
}
```

`switch` so sánh một giá trị nguyên hoặc enum với các nhãn `case`. Nó dễ đọc hơn chuỗi `if/else if` dài *khi mọi phép so sánh đều là đẳng thức với hằng số*.

## Cái bẫy fall-through (và một 용 dụng chính đáng duy nhất)

Không có `break`, việc thực thi sẽ *rơi xuống* case kế tiếp:

```cpp
case 1:
    std::cout << "one";
    // KHÔNG có break — in thêm "two"!
case 2:
    std::cout << "two";
    break;
```

GCC cảnh báo về fall-through vô ý (`-Wimplicit-fallthrough` với `-Wextra`). Một 용 dụng chính đáng duy nhất — dùng chung code cho vài case — phải được đánh dấu tường minh bằng `[[fallthrough]];` để người review biết đó là chủ ý. Người mới: luôn viết `break;`.

## switch hay if/else — cách chọn

- So đẳng thức với một tập hằng cố định (lệnh `char`, menu `int`, trạng thái `enum class`) → `switch`.
- Khoảng giá trị, logic phức hợp, so sánh `std::string` → `if/else`.
- (`switch` trên `std::string` không hoạt động; if/else với `==` thì được.)

## Dòng đơn: toán tử điều kiện

```cpp
std::string label = (score >= 50) ? "pass" : "fail";
```

`cond ? a : b` là một *biểu thức* — hữu ích khi khởi tạo biến từ một lựa chọn bé xíu. Bất cứ thứ gì rối hơn nên nằm trong một `if` thật.

## Sắp tới

Điều kiện quyết định một lần; vòng lặp quyết định một nghìn lần. Module sau: sự lặp lại.
''',
)

# ---- Module 3 checkpoint ----
write_checkpoint(
    M3, L3C,
    "Checkpoint: Conditions",
    "One graded challenge: implement eligibility rules with precise boundary logic.",
    15,
    '''
**Checkpoint — conditions.** Pass the graded challenge below to finish the module.

You will implement a lending-eligibility check with compound rules — every boundary condition from this module is in play (>= vs >, and-vs-or, order of checks).
''',
    "Checkpoint: Cấu trúc điều kiện",
    "Một challenge có chấm: cài đặt quy tắc đủ điều kiện với logic biên chính xác.",
    '''
**Checkpoint — cấu trúc điều kiện.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Bạn sẽ cài đặt kiểm tra đủ điều kiện vay với các quy tắc phức hợp — mọi điều kiện biên của module đều xuất hiện (>= với >, và-vs-hoặc, thứ tự kiểm tra).
''',
    challenge(
        "cpp3-check-eligibility",
        "Eligibility Checker",
        "Implement `eligible(age, income, has_job)` returning `true` only when: age is at least 18, AND (income >= 2000 OR has_job). Age exactly 18 counts; 17 does not.",
        "bool eligible(int age, double income, bool has_job) {\\n    // TODO\\n}",
        [
            ("adult with job", "CHECK(eligible(18, 0, true));", "18 counts as adult; having a job alone qualifies."),
            ("adult with income", "CHECK(eligible(30, 2500, false));", "Income >= 2000 alone qualifies."),
            ("minor rejected", "CHECK(!eligible(17, 9000, true));", "Under 18 never qualifies, even with income and a job."),
            ("adult nothing rejected", "CHECK(!eligible(21, 1999.99, false));", "No job and income below 2000 must fail."),
        ],
        level="combination",
    ),
    vi_challenge(
        "Kiểm tra đủ điều kiện",
        "Cài đặt `eligible(age, income, has_job)` trả về `true` chỉ khi: tuổi ít nhất 18, VÀ (thu nhập >= 2000 HOẶC có việc làm). Tuổi đúng 18 được tính; 17 thì không.",
        [("người lớn có việc", "18 tính là người lớn; chỉ cần có việc làm là đủ."), ("người lớn có thu nhập", "Thu nhập >= 2000 một mình cũng đủ."), ("vị thành niên bị từ chối", "Dưới 18 không bao giờ đủ, dù có thu nhập và việc làm."), ("người lớn không có gì bị từ chối", "Không việc làm và thu nhập dưới 2000 phải bị từ chối.")],
    ),
    solution="bool eligible(int age, double income, bool has_job) {\\n    return age >= 18 && (income >= 2000 || has_job);\\n}",
    wrong="bool eligible(int age, double income, bool has_job) {\\n    return age > 18 && (income >= 2000 || has_job);\\n}",
)

# ---- Module 3 practice sets ----
write_practice(
    M3, "m3-if-practice",
    "Conditions Practice: Logic That Bites",
    "Grading, pricing tiers, and a leap-year check — the classic compound-logic workout.",
    "Luyện Điều kiện: Logic nhọn",
    "Xếp hạng, bậc giá, và kiểm tra năm nhuận — bài tập luyện logic phức hợp kinh điển.",
    L3A, 25, "beginner",
    [
        challenge(
            "cpp3-leap-year",
            "Leap Year",
            "Implement `is_leap(year)`: divisible by 4, but centuries must be divisible by 400 (1900 is not a leap year; 2000 is).",
            "bool is_leap(int year) {\\n    // TODO\\n}",
            [("1996 yes", "CHECK(is_leap(1996));", "Divisible by 4, not a century."), ("1900 no", "CHECK(!is_leap(1900));", "Century not divisible by 400."), ("2000 yes", "CHECK(is_leap(2000));", "Century divisible by 400."), ("2023 no", "CHECK(!is_leap(2023));", "Not divisible by 4.")],
            level="guided",
        ),
    ],
    {"cpp3-leap-year": vi_challenge("Năm nhuận", "Cài đặt `is_leap(year)`: chia hết cho 4, nhưng thế kỷ phải chia hết cho 400 (1900 không nhuận; 2000 nhuận).", [("1996 có", "Chia hết cho 4, không phải thế kỷ."), ("1900 không", "Thế kỷ không chia hết cho 400."), ("2000 có", "Thế kỷ chia hết cho 400."), ("2023 không", "Không chia hết cho 4.")])},
    solutions=[
        ("cpp3-leap-year", "bool is_leap(int year) { return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0); }", "bool is_leap(int year) { return year % 4 == 0; }"),
    ],
)

write_practice(
    M3, "m3-switch-practice",
    "Switch Practice: Menu Logic",
    "Map commands to actions with switch, and fix a fall-through bug.",
    "Luyện Switch: Logic menu",
    "Ánh xạ lệnh sang hành động bằng switch, và sửa một bug fall-through.",
    L3B, 20, "beginner",
    [
        challenge(
            "cpp3-menu-command",
            "Command Router",
            "Implement `handle(command)` returning: 'h' -> 1 (help), 'q' -> 2 (quit), anything else -> 0 (unknown). Use a switch.",
            "int handle(char command) {\\n    // TODO\\n}",
            [("help", "CHECK_EQ(handle('h'), 1);", "'h' maps to 1."), ("quit", "CHECK_EQ(handle('q'), 2);", "'q' maps to 2."), ("unknown", "CHECK_EQ(handle('x'), 0);", "Anything else is 0 via default.")],
            level="imitation",
        ),
    ],
    {"cpp3-menu-command": vi_challenge("Điều hướng lệnh", "Cài đặt `handle(command)` trả về: 'h' -> 1 (help), 'q' -> 2 (quit), mọi thứ khác -> 0 (không rõ). Dùng switch.", [("help", "'h' ánh xạ tới 1."), ("quit", "'q' ánh xạ tới 2."), ("không rõ", "Mọi thứ khác là 0 qua default.")])},
    solutions=[
        ("cpp3-menu-command", "int handle(char command) {\\n    switch (command) {\\n        case 'h': return 1;\\n        case 'q': return 2;\\n        default: return 0;\\n    }\\n}", "int handle(char command) {\\n    switch (command) {\\n        case 'h':\\n        case 'q': return 2;\\n        default: return 0;\\n    }\\n}"),
    ],
)

# ============================ MODULE 4: loops ============================
M4 = "loops"

L4A = "for-and-range-for"
L4B = "while-and-validation"
L4C = "nested-loops-patterns"
L4D = "checkpoint-loops"

write_module(
    M4,
    "Loops & Repetition",
    "for, range-based for, while, do/while, break/continue, nesting — the machinery of accumulation, search, and validation.",
    "Vòng lặp & Sự lặp lại",
    "for, range-based for, while, do/while, break/continue, lồng nhau — cơ chế của tích lũy, tìm kiếm, và validation.",
    [L4A, L4B, L4C, L4D],
    ["m4-for-practice", "m4-while-practice"],
)

write_lesson(
    M4, L4A,
    "for and range-based for",
    "Counting loops, the off-by-one discipline, and the range-based for you will use for everything else.",
    11,
    '''
## Counting: the classic for

```cpp
for (int i = 1; i <= 5; ++i) {
    std::cout << i << ' ';
}
// prints: 1 2 3 4 5
```

Three parts: initialize (`int i = 1`), condition (`i <= 5`, checked *before* each pass), step (`++i`, after each pass). Prefer `++i` over `i++` as a style habit (never slower, occasionally faster).

## Off-by-one discipline

Counting 1..N uses `i = 1; i <= N`. Indexing positions 0..N-1 uses `i = 0; i < N`. Mixing the two habits produces the classic off-by-one bug: one extra or one missing iteration. Decide *why* you are looping, then pick the shape deliberately.

## Range-based for — the modern default

```cpp
#include <vector>
#include <string>

std::vector<int> scores{9, 7, 10};

for (int s : scores) {          // one pass, no index bookkeeping
    std::cout << s << ' ';
}

for (const auto& name : names) { // const& = read-only, no copy (module 11 explains &)
    std::cout << name << '\\n';
}
```

Use range-for whenever you just *visit* every element — it cannot run off the end. Use the classic for when you need the index (positions, strides, two-at-a-time).

## break and continue

`break` exits the loop now; `continue` skips to the next iteration. Use them to keep the happy path unindented:

```cpp
for (const auto& line : lines) {
    if (line.empty() || line[0] == '#') continue;  // skip noise
    if (line == "STOP") break;                     // early exit
    process(line);
}
```
''',
    "for và range-based for",
    "Vòng lặp đếm, kỷ luật off-by-one, và range-based for bạn sẽ dùng cho mọi thứ còn lại.",
    '''
## Đếm: for kinh điển

```cpp
for (int i = 1; i <= 5; ++i) {
    std::cout << i << ' ';
}
// in ra: 1 2 3 4 5
```

Ba phần: khởi tạo (`int i = 1`), điều kiện (`i <= 5`, kiểm tra *trước* mỗi vòng), bước nhảy (`++i`, sau mỗi vòng). Nên dùng `++i` thay vì `i++` như một thói quen phong cách (chưa bao giờ chậm hơn, đôi khi nhanh hơn).

## Kỷ luật off-by-one

Đếm 1..N dùng `i = 1; i <= N`. Truy cập vị trí 0..N-1 dùng `i = 0; i < N`. Trộn hai thói quen tạo ra bug off-by-one kinh điển: thừa hoặc thiếu đúng một vòng. Hãy quyết định *lý do* bạn lặp, rồi chọn dạng tương ứng một cách chủ ý.

## Range-based for — mặc định hiện đại

```cpp
#include <vector>
#include <string>

std::vector<int> scores{9, 7, 10};

for (int s : scores) {          // một lượt, không cần quản lý chỉ số
    std::cout << s << ' ';
}

for (const auto& name : names) { // const& = chỉ đọc, không sao chép (module 11 giải thích &)
    std::cout << name << '\\n';
}
```

Dùng range-for bất cứ khi nào bạn chỉ *ghé thăm* từng phần tử — nó không thể chạy quá cuối. Dùng for kinh điển khi bạn cần chỉ số (vị trí, bước nhảy, đi hai phần tử một lần).

## break và continue

`break` thoát vòng lặp ngay lập tức; `continue` bỏ qua sang vòng kế tiếp. Dùng chúng để giữ luồng chính không bị thụt lề:

```cpp
for (const auto& line : lines) {
    if (line.empty() || line[0] == '#') continue;  // bỏ nhiễu
    if (line == "STOP") break;                     // thoát sớm
    process(line);
}
```
''',
)

write_lesson(
    M4, L4B,
    "while, do/while, and Validation Loops",
    "Condition-first vs body-first loops, accumulators, input validation patterns, and infinite-loop hygiene.",
    10,
    '''
## while: as long as the condition holds

```cpp
int cups = 0;
while (cups < 3) {
    std::cout << "refilling...\\n";
    ++cups;               // forget this and the loop never ends
}
```

Use `while` when the number of repetitions is *unknown in advance* — reading until end-of-file, searching until found, waiting for a condition.

## do/while: check after the first try

```cpp
std::string choice;
do {
    choice = ask_menu();      // body runs FIRST, at least once
} while (choice != "h" && choice != "q");
```

`do/while` is for "ask at least once, then re-ask while invalid" — menu loops, retry prompts. If you never need the guaranteed first pass, plain `while` reads better.

## Accumulators and search

Two patterns cover most loops you will write this year:

```cpp
// accumulator
int total = 0;
for (int s : scores) total += s;

// first-match search
int first_below_60 = -1;
for (std::size_t i = 0; i < scores.size(); ++i) {
    if (scores[i] < 60) { first_below_60 = static_cast<int>(i); break; }
}
```

Module 8 replaces both hand-rolled versions with STL algorithms — but write them by hand now; you cannot trust abstractions you have never built.

## Infinite-loop hygiene

A `while` loop needs something inside it that moves the state toward the exit condition: `++cups`, `std::cin >> value`, `break`. The sandbox kills runaway programs with a timeout and reports "timeout" — if you see that verdict in a graded run, look for the missing step.
''',
    "while, do/while, và vòng lặp validation",
    "Vòng lặp kiểm tra điều kiện trước hay sau thân hàm, bộ tích lũy, các mẫu validation, và vệ sinh chống vòng lặp vô hạn.",
    '''
## while: chừng nào điều kiện còn đúng

```cpp
int cups = 0;
while (cups < 3) {
    std::cout << "refilling...\\n";
    ++cups;               // quên dòng này là vòng lặp không bao giờ dứt
}
```

Dùng `while` khi số lần lặp *không biết trước* — đọc đến cuối file, tìm cho tới khi thấy, chờ một điều kiện.

## do/while: kiểm tra sau lần thử đầu

```cpp
std::string choice;
do {
    choice = ask_menu();      // thân hàm chạy TRƯỚC, ít nhất một lần
} while (choice != "h" && choice != "q");
```

`do/while` dành cho "hỏi ít nhất một lần, rồi hỏi lại khi còn sai" — vòng menu, nhắc nhập lại. Nếu bạn không cần lượt chạy đầu tiên được bảo đảm, `while` thường dễ đọc hơn.

## Bộ tích lũy và tìm kiếm

Hai mẫu này bao phủ phần lớn vòng lặp bạn sẽ viết trong năm nay:

```cpp
// bộ tích lũy
int total = 0;
for (int s : scores) total += s;

// tìm phần tử đầu tiên khớp
int first_below_60 = -1;
for (std::size_t i = 0; i < scores.size(); ++i) {
    if (scores[i] < 60) { first_below_60 = static_cast<int>(i); break; }
}
```

Module 8 sẽ thay cả hai bản viết tay này bằng thuật toán STL — nhưng hãy viết tay bây giờ; bạn không thể tin tưởng vào sự trừu tượng mà bạn chưa từng tự dựng.

## Vệ sinh chống vòng lặp vô hạn

Một vòng `while` cần thứ gì đó bên trong nó đưa trạng thái tiến về điều kiện thoát: `++cups`, `std::cin >> value`, `break`. Sandbox sẽ tiêu diệt chương trình chạy hoài bằng timeout và báo "timeout" — nếu thấy verdict đó trong lần chạy có chấm, hãy tìm bước nhảy bị thiếu.
''',
)

write_lesson(
    M4, L4C,
    "Nested Loops and Shapes",
    "Loops inside loops: grids, tables, and triangle patterns — and how to reason about the cost of nesting.",
    10,
    '''
## The grid shape

```cpp
for (int row = 0; row < 3; ++row) {
    for (int col = 0; col < 4; ++col) {
        std::cout << row << ',' << col << ' ';
    }
    std::cout << '\\n';       // end of one row
}
```

The inner loop runs *completely* for each single step of the outer loop: 3 × 4 = 12 iterations. The newline after the inner loop is what gives the output its shape.

## Classic patterns (you will build these in practice)

```
*            1
* *          1 2
* * *        1 2 3
```

Triangle one: outer loop counts rows `r`, inner loop prints `r` stars. Triangle two: inner prints numbers `1..r`. Neither is about stars — both are about controlling an inner loop's *range* from the outer loop's *current value*.

## Tables

Multiplication tables pair a row loop with a column loop and format with padding. Nested loops over rows and columns are also exactly how you will later iterate 2-D data (`vector<vector<int>>` — module 7) and how image/flood-fill algorithms begin.

## The cost of nesting

3 × 4 = 12 is nothing. But 1,000 × 1,000 = 1,000,000 — and 10,000 × 10,000 takes seconds even in C++. When you nest, multiply the sizes in your head *first*; it is your first complexity instinct (module 18 develops it properly).
''',
    "Vòng lặp lồng nhau và các hình dạng",
    "Vòng lặp trong vòng lặp: lưới, bảng, và các hình tam giác — cùng cách suy nghĩ về cái giá của việc lồng nhau.",
    '''
## Dạng lưới

```cpp
for (int row = 0; row < 3; ++row) {
    for (int col = 0; col < 4; ++col) {
        std::cout << row << ',' << col << ' ';
    }
    std::cout << '\\n';       // kết thúc một hàng
}
```

Vòng trong chạy *hoàn toàn* cho từng bước một của vòng ngoài: 3 × 4 = 12 lần lặp. Ký tự xuống dòng sau vòng trong chính là thứ tạo ra hình dạng của output.

## Các mẫu kinh điển (bạn sẽ dựng chúng trong phần luyện tập)

```
*            1
* *          1 2
* * *        1 2 3
```

Tam giác một: vòng ngoài đếm hàng `r`, vòng trong in `r` dấu sao. Tam giác hai: vòng trong in số `1..r`. Cả hai không phải là chuyện dấu sao — mà là chuyện điều khiển *khoảng* của vòng trong từ *giá trị hiện tại* của vòng ngoài.

## Bảng cửu chương

Bảng cửu chương ghép một vòng hàng với một vòng cột và format bằng padding. Vòng lặp lồng trên hàng và cột cũng chính là cách bạn sẽ duyệt dữ liệu 2 chiều sau này (`vector<vector<int>>` — module 7) và là khởi đầu của các thuật toán image/flood-fill.

## Cái giá của việc lồng nhau

3 × 4 = 12 thì chẳng là gì. Nhưng 1.000 × 1.000 = 1.000.000 — và 10.000 × 10.000 mất vài giây ngay cả với C++. Khi bạn lồng vòng lặp, hãy nhân kích thước trong đầu *trước tiên*; đó là bản năng đầu tiên về độ phức tạp (module 18 sẽ phát triển đúng mức).
''',
)

# ---- Module 4 checkpoint ----
write_checkpoint(
    M4, L4D,
    "Checkpoint: Loops",
    "One graded challenge: accumulate statistics and find a first match — the two loop patterns of the year.",
    15,
    '''
**Checkpoint — loops.** Pass the graded challenge below to finish the module.

Two tasks in one: total-and-average (accumulator) and first-match (search with break). Both hand-rolled — no algorithms yet.
''',
    "Checkpoint: Vòng lặp",
    "Một challenge có chấm: tích lũy số liệu và tìm kết quả khớp đầu tiên — hai mẫu vòng lặp của năm.",
    '''
**Checkpoint — vòng lặp.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Hai việc trong một: tổng-và-trung-bình (bộ tích lũy) và tìm-khớp-đầu-tiên (tìm kiếm với break). Cả hai viết tay — chưa dùng thuật toán.
''',
    challenge(
        "cpp4-check-stats",
        "Stats and First Match",
        "Implement `total(scores)` (sum of all elements), `average(scores)` (0 when empty), and `first_below(scores, limit)` returning the INDEX of the first element below limit, or -1 if none.",
        "#include <vector>\\n\\nint total(const std::vector<int>& scores) {\\n    // TODO\\n}\\ndouble average(const std::vector<int>& scores) {\\n    // TODO\\n}\\nint first_below(const std::vector<int>& scores, int limit) {\\n    // TODO\\n}",
        [
            ("total", "CHECK_EQ(total({9, 7, 10}), 26);", "Sum every element."),
            ("average empty", "CHECK_EQ(average({}), 0.0);", "Empty input must give 0, not a division by zero."),
            ("average", "CHECK_NEAR(average({9, 7, 10}), 8.6666, 0.001);", "Divide as doubles, not integers."),
            ("first match", "CHECK_EQ(first_below({8, 5, 9, 3}, 6), 1);", "Index 1 holds the first value below 6."),
            ("no match", "CHECK_EQ(first_below({8, 5, 9}, 1), -1);", "No element below 1: return -1."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Thống kê và khớp đầu tiên",
        "Cài đặt `total(scores)` (tổng mọi phần tử), `average(scores)` (0 khi rỗng), và `first_below(scores, limit)` trả về CHỈ SỐ của phần tử đầu tiên nhỏ hơn limit, hoặc -1 nếu không có.",
        [("tổng", "Cộng mọi phần tử."), ("trung bình rỗng", "Input rỗng phải cho 0, không phải chia cho 0."), ("trung bình", "Chia theo double, không phải số nguyên."), ("khớp đầu tiên", "Chỉ số 1 chứa giá trị đầu tiên nhỏ hơn 6."), ("không khớp", "Không phần tử nào nhỏ hơn 1: trả về -1.")],
    ),
    solution="#include <vector>\\nint total(const std::vector<int>& scores) {\\n    int t = 0;\\n    for (int s : scores) t += s;\\n    return t;\\n}\\ndouble average(const std::vector<int>& scores) {\\n    if (scores.empty()) return 0.0;\\n    return static_cast<double>(total(scores)) / scores.size();\\n}\\nint first_below(const std::vector<int>& scores, int limit) {\\n    for (std::size_t i = 0; i < scores.size(); ++i) {\\n        if (scores[i] < limit) return static_cast<int>(i);\\n    }\\n    return -1;\\n}",
    wrong="#include <vector>\\nint total(const std::vector<int>& scores) {\\n    int t = 0;\\n    for (int s : scores) t += s;\\n    return t;\\n}\\ndouble average(const std::vector<int>& scores) {\\n    return static_cast<double>(total(scores)) / scores.size();\\n}\\nint first_below(const std::vector<int>& scores, int limit) {\\n    for (std::size_t i = 0; i < scores.size(); ++i) {\\n        if (scores[i] < limit) return static_cast<int>(i);\\n    }\\n    return -1;\\n}",
)

# ---- Module 4 practice sets ----
write_practice(
    M4, "m4-for-practice",
    "Loop Practice: Shapes and Sums",
    "Triangles, multiplication table, FizzBuzz's serious cousin, and a sum-with-skip.",
    "Luyện Vòng lặp: Hình dạng và tổng",
    "Tam giác, bảng cửu chương, anh họ nghiêm túc của FizzBuzz, và tổng có điều kiện bỏ qua.",
    L4A, 25, "beginner",
    [
        challenge(
            "cpp4-triangle",
            "Star Triangle",
            "Implement `triangle(rows)` so `program()` prints a left-aligned triangle: row 1 has one `*`, row `rows` has `rows` stars, each row on its own line.",
            "#include <iostream>\\n\\nvoid program() {\\n    // TODO: print triangle(rows = 3)\\n}\\n\\nint main() {\\n    program();\\n    return 0;\\n}",
            [("shape", "auto out = capture([]{ triangle(3); });\\nCHECK_CONTAINS(out, \"*\\n**\\n***\");", "Inner loop range grows with the outer row counter.")],
            level="imitation",
        ),
    ],
    {"cpp4-triangle": vi_challenge("Tam giác sao", "Cài đặt `triangle(rows)` để `program()` in tam giác căn trái: hàng 1 có một `*`, hàng `rows` có `rows` dấu sao, mỗi hàng một dòng.", [("hình dạng", "Miền của vòng trong lớn dần theo bộ đếm hàng của vòng ngoài.")])},
    solutions=[
        ("cpp4-triangle", "void triangle(int rows) {\\n    for (int r = 1; r <= rows; ++r) {\\n        for (int c = 0; c < r; ++c) std::cout << '*';\\n        std::cout << '\\\\n';\\n    }\\n}", "void triangle(int rows) {\\n    for (int r = 1; r <= rows; ++r) {\\n        for (int c = 0; c <= rows; ++c) std::cout << '*';\\n        std::cout << '\\\\n';\\n    }\\n}"),
    ],
)

write_practice(
    M4, "m4-while-practice",
    "While Practice: Search and Validate",
    "A digit-sum loop, a first-match search, and a validation loop that keeps asking until sane.",
    "Luyện While: Tìm kiếm và validate",
    "Vòng lặp tính tổng chữ số, tìm khớp đầu tiên, và vòng validation hỏi đến khi hợp lý.",
    L4B, 25, "beginner",
    [
        challenge(
            "cpp4-digit-sum",
            "Digit Sum",
            "Implement `digit_sum(n)`: sum of the decimal digits of a non-negative integer. Use `% 10` and `/ 10` in a while loop.",
            "int digit_sum(int n) {\\n    // TODO\\n}",
            [("single digit", "CHECK_EQ(digit_sum(7), 7);", "One digit is itself."), ("multi digit", "CHECK_EQ(digit_sum(1234), 10);", "1+2+3+4 = 10: peel digits with n % 10, then n /= 10."), ("zero", "CHECK_EQ(digit_sum(0), 0);", "0 has digit sum 0 — loop must not run.")],
            level="guided",
        ),
    ],
    {"cpp4-digit-sum": vi_challenge("Tổng chữ số", "Cài đặt `digit_sum(n)`: tổng các chữ số thập phân của một số nguyên không âm. Dùng `% 10` và `/ 10` trong vòng while.", [("một chữ số", "Một chữ số là chính nó."), ("nhiều chữ số", "1+2+3+4 = 10: bóc từng chữ số bằng n % 10, rồi n /= 10."), ("không", "0 có tổng chữ số là 0 — vòng lặp không được chạy.")])},
    solutions=[
        ("cpp4-digit-sum", "int digit_sum(int n) {\\n    int s = 0;\\n    while (n > 0) { s += n % 10; n /= 10; }\\n    return s;\\n}", "int digit_sum(int n) {\\n    int s = 0;\\n    while (n > 1) { s += n % 10; n /= 10; }\\n    return s;\\n}"),
    ],
)

print("modules 3-4 authored")
