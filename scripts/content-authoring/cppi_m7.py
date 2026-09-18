#!/usr/bin/env python3
"""C++ Intermediate — Module 7: modern-cpp.

Authoring discipline: every C++ code string (tests, solutions, boilerplate) is
a raw triple-quoted string, so real newlines stay real and C++ "\\n" literals
stay literal. Snippets are self-contained: each test is its own translation
unit (solution.cpp is #included; no cross-test state).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "modern-cpp"

# ---- lesson auto-and-deduction ----------------------------------------------
L_auto_EN = r"""
`auto` asks the compiler to deduce a type from the initializer. Use it where
the type is *obvious or irrelevant*, hide it where the type *is the meaning*.

```cpp
auto it = v.begin();            // iterator type is noise — auto shines
auto n = words.size();          // std::size_t, spelled correctly for free
for (const auto& [key, value] : m) { ... }   // structured bindings
```

The rules that matter:

- `auto x = expr;` copies and drops references/const — `auto&` and
  `const auto&` re-add them. `auto x = v[0];` on a vector of big objects
  silently copies.
- `auto` on an initializer_list braced expression deduces
  `std::initializer_list`, not the element type.
- Function return types can be deduced (`auto f() { return 42; }`), but a
  public API benefits from spelled-out returns: the signature is
  documentation.
- `decltype(expr)` yields the type of an expression without evaluating it —
  the tool for "same type as that other thing" declarations.

The smell test: if deleting `auto` and writing the real type makes the code
*clearer*, write the type. If it makes the line a 70-character template
spelling, `auto` is serving you.
"""

L_auto_VI = r"""
`auto` nhờ compiler suy luận kiểu từ initializer. Dùng nó ở chỗ kiểu *hiển
nhiên hoặc không quan trọng*, và giấu nó ở chỗ *chính kiểu là ý nghĩa*.

```cpp
auto it = v.begin();            // kiểu iterator là chi tiết ồn ào — auto phát huy
auto n = words.size();          // std::size_t, viết đúng tự động
for (const auto& [key, value] : m) { ... }   // structured bindings
```

Những quy tắc quan trọng:

- `auto x = expr;` copy và mất reference/const — `auto&` và `const auto&`
  thêm lại. `auto x = v[0];` trên vector object lớn âm thầm copy.
- `auto` với initializer_list suy ra `std::initializer_list`, không phải
  kiểu phần tử.
- Kiểu trả về của hàm được suy luận được (`auto f() { return 42; }`), nhưng
  API công khai nên viết rõ kiểu trả về: chữ ký hàm chính là tài liệu.
- `decltype(expr)` cho ra kiểu của biểu thức mà không đánh giá nó — công cụ
  cho khai báo "cùng kiểu với cái kia".

Bài kiểm tra mùi: nếu xóa `auto` và viết kiểu thật làm code *dễ đọc hơn*,
hãy viết kiểu. Nếu điều đó biến dòng code thành một chính tả template dài
70 ký tự, `auto` đang phục vụ bạn.
"""

# ---- lesson constexpr-enums ---------------------------------------------------
L_constexpr_EN = r"""
Two features move work from runtime to compile time — and make intent
visible to both the compiler and the reader.

`constexpr` marks an expression or function as computable at compile time
when given constant arguments:

```cpp
constexpr int max_users = 1000;              // a true constant
constexpr int square(int x) { return x * x; }
static_assert(square(7) == 49);              // proven at compile time
```

`enum class` is a scoped, strongly-typed enum: enumerators live inside the
enum's name, do not leak, do not implicitly convert to int, and the
underlying type is your choice:

```cpp
enum class Status { Ok, NotFound, Error };

Status s = Status::Ok;
// int x = s;            // error: no implicit conversion — the whole point
if (s == Status::Ok) { }  // comparisons are type-checked
```

The classic bug `enum class` eliminates: two unrelated unscoped enums (or
an enum and an int) silently comparing equal. Prefer it for every new
enumeration; pass it by value; switch over it exhaustively — most compilers
warn when a switch misses an enumerator.
"""

L_constexpr_VI = r"""
Hai tính năng chuyển công việc từ runtime sang compile time — và khiến ý
đồ hiện rõ với cả compiler lẫn người đọc.

`constexpr` đánh dấu một biểu thức hoặc hàm tính được lúc biên dịch khi
nhận đối số hằng:

```cpp
constexpr int max_users = 1000;              // hằng số thật sự
constexpr int square(int x) { return x * x; }
static_assert(square(7) == 49);              // được chứng minh lúc biên dịch
```

`enum class` là enum có phạm vi, kiểu mạnh: các enumerator sống trong tên
enum, không rò rỉ ra ngoài, không chuyển ngầm thành int, và kiểu nền do bạn
chọn:

```cpp
enum class Status { Ok, NotFound, Error };

Status s = Status::Ok;
// int x = s;            // lỗi: không chuyển ngầm — chính là điểm giá trị
if (s == Status::Ok) { }  // so sánh được kiểm tra kiểu
```

Bug kinh điển mà `enum class` loại bỏ: hai enum không-phạm-vi không liên
quan (hoặc một enum và một int) âm thầm so sánh bằng nhau. Hãy dùng nó cho
mọi enum mới; truyền bằng giá trị; switch đầy đủ — đa số compiler cảnh báo
khi switch thiếu một enumerator.
"""

# ---- lesson optional-variant ----------------------------------------------------
L_optional_EN = r"""
`std::optional<T>` is a T that may be absent — the vocabulary type for
"maybe no value" without sentinel magic (`-1`, `nullptr`, empty string).

```cpp
#include <optional>

std::optional<int> find_index(const std::vector<int>& v, int target) {
    for (std::size_t i = 0; i < v.size(); ++i)
        if (v[i] == target) return static_cast<int>(i);
    return std::nullopt;
}

auto idx = find_index(v, 7);
if (idx.has_value()) use(*idx);      // or idx.value() (throws if empty)
int fallback = idx.value_or(-1);     // read with a default
```

`std::variant<A, B>` is a type-safe union: it holds exactly one of the
alternatives, and `std::visit` dispatches on which one:

```cpp
#include <variant>

std::variant<int, std::string> result = 42;
result = std::string{"overflow"};

auto text = std::visit([](auto&& x) {
    using T = std::decay_t<decltype(x)>;
    if constexpr (std::is_same_v<T, int>) return std::to_string(x);
    else return x;
}, result);
```

Choose `optional` when the question is "is there a value?"; choose
`variant` when the answer is "one of several different types" — parse
results, state machines, tagged outputs. Both replace error-channel
out-parameters and make signatures honest.
"""

L_optional_VI = r"""
`std::optional<T>` là một T có thể vắng mặt — kiểu từ vựng cho "có thể
không có giá trị" thay cho các giá trị-sentinel (`-1`, `nullptr`, chuỗi rỗng).

```cpp
#include <optional>

std::optional<int> find_index(const std::vector<int>& v, int target) {
    for (std::size_t i = 0; i < v.size(); ++i)
        if (v[i] == target) return static_cast<int>(i);
    return std::nullopt;
}

auto idx = find_index(v, 7);
if (idx.has_value()) use(*idx);      // hoặc idx.value() (ném ngoại lệ nếu rỗng)
int fallback = idx.value_or(-1);     // đọc kèm giá trị mặc định
```

`std::variant<A, B>` là union an toàn kiểu: nó giữ đúng một trong các phương
án, và `std::visit` điều phối theo phương án đang giữ:

```cpp
#include <variant>

std::variant<int, std::string> result = 42;
result = std::string{"overflow"};

auto text = std::visit([](auto&& x) {
    using T = std::decay_t<decltype(x)>;
    if constexpr (std::is_same_v<T, int>) return std::to_string(x);
    else return x;
}, result);
```

Chọn `optional` khi câu hỏi là "có giá trị không?"; chọn `variant` khi câu
trả lời là "một trong vài kiểu khác nhau" — kết quả parse, máy trạng thái,
kết quả có nhãn. Cả hai thay thế tham-chiếu-ra kênh-báo-lỗi và làm chữ ký
hàm trung thực hơn.
"""

# ---- lesson modern-idioms -----------------------------------------------------
L_idioms_EN = r"""
Modern C++ is mostly *removing* footguns. Four idioms pay rent immediately.

1. **Narrow interfaces with types.** A `std::string_view` parameter accepts
   `std::string`, a literal, or a slice without copying:

```cpp
#include <string_view>

bool is_command(std::string_view s) {
    return s.starts_with("--");   // C++20
}
```

   Views do not own; they must not outlive the underlying string.

2. **Structured bindings for pair/tuple/struct unpacking** — `for (const
   auto& [k, v] : map)` beats `.first/.second` for readability.

3. **`constexpr` for tables and limits** — magic numbers move to named,
   compile-time-checked constants.

4. **Exhaustive `switch` over `enum class`** with no `default` — the
   compiler then forces you to update every switch when the enum grows.
   That is free maintenance.

And one deprecation to know: `std::auto_ptr` and throwing `std::vector::operator[]`
are history; dynamic exception specifications (`throw(...)`) are gone from
the language. Modern code catches specific exception types — Module 10's job.
"""

L_idioms_VI = r"""
Modern C++ phần lớn là *loại bỏ* bẫy lỗi. Bốn idiom trả tiền ngay lập tức.

1. **Thu hẹp interface bằng kiểu.** Tham số `std::string_view` nhận được
   `std::string`, chuỗi literal, hoặc một lát cắt mà không copy:

```cpp
#include <string_view>

bool is_command(std::string_view s) {
    return s.starts_with("--");   // C++20
}
```

   View không sở hữu; nó không được sống lâu hơn chuỗi nền tảng.

2. **Structured bindings để bóc pair/tuple/struct** — `for (const auto&
   [k, v] : map)` dễ đọc hơn `.first/.second`.

3. **`constexpr` cho bảng hằng và giới hạn** — magic number chuyển thành
   hằng có tên, được kiểm tra lúc biên dịch.

4. **`switch` đầy đủ trên `enum class`** không có `default` — compiler khi
   đó buộc bạn cập nhật mọi switch khi enum thêm giá trị. Đó là bảo trì
   miễn phí.

Và một deprecation cần biết: `std::auto_ptr` và `std::vector::operator[]`
ném ngoại lệ là lịch sử; dynamic exception specification (`throw(...)`) đã
bị loại khỏi ngôn ngữ. Code hiện đại catch các kiểu ngoại lệ cụ thể —
công việc của Module 10.
"""

# ---- practice cppi-p7-utilities ---------------------------------------------
R_SAFE_DIVIDE = r'''#include <optional>

std::optional<int> safe_divide(int a, int b) {
    if (b == 0) return std::nullopt;
    return a / b;
}
'''

W_SAFE_DIVIDE = r'''#include <optional>

std::optional<int> safe_divide(int a, int b) {
    if (b == 0) return 0;  // BUG: returns a value instead of nullopt
    return a / b;
}
'''

R_PRIORITY_WEIGHT = r'''enum class Priority { Low, Normal, High, Critical };

int priority_weight(Priority p) {
    switch (p) {
        case Priority::Low: return 0;
        case Priority::Normal: return 1;
        case Priority::High: return 5;
        case Priority::Critical: return 20;
    }
    return 0;  // unreachable when the switch is exhaustive
}
'''

W_PRIORITY_WEIGHT = r'''enum class Priority { Low, Normal, High, Critical };

int priority_weight(Priority p) {
    switch (p) {
        case Priority::Low: return 0;
        case Priority::Normal: return 1;
        case Priority::High: return 5;
        case Priority::Critical: return 10;  // BUG: wrong weight for Critical
    }
    return 0;
}
'''

# ---- practice cppi-p7-variants ----------------------------------------------
R_PARSE_POSITIVE = r'''#include <optional>
#include <string>
#include <variant>

std::variant<int, std::string> parse_positive(const std::string& s) {
    std::size_t i = 0;
    if (s.empty()) return "invalid: " + s;
    if (s[0] == '+') i = 1;
    if (i >= s.size()) return "invalid: " + s;
    for (std::size_t j = i; j < s.size(); ++j) {
        if (s[j] < '0' || s[j] > '9') return "invalid: " + s;
    }
    long value = 0;
    for (std::size_t j = i; j < s.size(); ++j) {
        value = value * 10 + (s[j] - '0');
        if (value > 2147483647L) return "invalid: " + s;
    }
    if (value <= 0) return "invalid: " + s;
    return static_cast<int>(value);
}
'''

W_PARSE_POSITIVE = r'''#include <string>
#include <variant>

std::variant<int, std::string> parse_positive(const std::string& s) {
    std::size_t i = 0;
    if (s.empty()) return "invalid: " + s;
    if (s[0] == '+') i = 1;
    if (s[0] == '-') i = 1;  // BUG: accepts negatives
    if (i >= s.size()) return "invalid: " + s;
    for (std::size_t j = i; j < s.size(); ++j) {
        if (s[j] < '0' || s[j] > '9') return "invalid: " + s;
    }
    long value = 0;
    for (std::size_t j = i; j < s.size(); ++j) {
        value = value * 10 + (s[j] - '0');
        if (value > 2147483647L) return "invalid: " + s;
    }
    return static_cast<int>(value);
}
'''

# ---- checkpoint: describe via std::visit --------------------------------------
R_DESCRIBE = r'''#include <sstream>
#include <string>
#include <variant>

std::string describe(const std::variant<int, double, std::string>& v) {
    return std::visit([](auto&& x) -> std::string {
        using T = std::decay_t<decltype(x)>;
        std::ostringstream os;
        if constexpr (std::is_same_v<T, int>) {
            os << "int: " << x;
        } else if constexpr (std::is_same_v<T, double>) {
            os.precision(2);
            os << std::fixed << "double: " << x;
        } else {
            os << "string: " << x;
        }
        return os.str();
    }, v);
}
'''

W_DESCRIBE = r'''#include <sstream>
#include <string>
#include <variant>

std::string describe(const std::variant<int, double, std::string>& v) {
    return std::visit([](auto&& x) -> std::string {
        using T = std::decay_t<decltype(x)>;
        std::ostringstream os;
        if constexpr (std::is_same_v<T, int>) {
            os << "int: " << x;
        } else if constexpr (std::is_same_v<T, double>) {
            os << "double: " << x;  // BUG: no fixed 2-decimal formatting
        } else {
            os << "string: " << x;
        }
        return os.str();
    }, v);
}
'''

# ---- challenges ---------------------------------------------------------------
CH_SAFE_DIVIDE = challenge(
    "cppi-m7-safe-divide",
    "std::optional divide",
    "Implement `std::optional<int> safe_divide(int a, int b)`: return the quotient when `b != 0`, and `std::nullopt` when `b == 0`. No exceptions, no sentinel ints.",
    r'''#include <optional>
#include <iostream>

// std::optional<int> safe_divide(int a, int b)
''',
    [
        ("basic", 'CHECK_EQ(safe_divide(7, 2).value(), 3);', "Integer division truncates toward zero."),
        ("zero", 'CHECK(!safe_divide(1, 0).has_value());', "Division by zero is absence, not zero."),
        ("negative", 'CHECK_EQ(safe_divide(-7, 2).value(), -3);', "Negatives follow the same truncation rule."),
    ],
    level="imitation",
)

CH_PRIORITY = challenge(
    "cppi-m7-priority-weight",
    "enum class Priority weights",
    "Define `enum class Priority { Low, Normal, High, Critical }` and implement `int priority_weight(Priority)` returning 0, 1, 5, 20 respectively. Use an exhaustive `switch` (no `default` case) so a future enumerator fails compilation.",
    r'''#include <iostream>

// enum class Priority { Low, Normal, High, Critical };
// int priority_weight(Priority p)
''',
    [
        ("all-values", 'CHECK_EQ(priority_weight(Priority::Low), 0);\nCHECK_EQ(priority_weight(Priority::Normal), 1);\nCHECK_EQ(priority_weight(Priority::High), 5);\nCHECK_EQ(priority_weight(Priority::Critical), 20);', "One weight per enumerator, exactly."),
        ("type-safe", 'Priority p = Priority::High;\nCHECK_EQ(priority_weight(p), 5);', "enum class values are passed by name, not as raw ints."),
    ],
    level="guided",
)

CH_PARSE = challenge(
    "cppi-m7-parse-positive",
    "Parse a positive integer into a variant",
    "Implement `std::variant<int, std::string> parse_positive(const std::string& s)`. On success (a syntactically valid integer literal greater than 0, fitting int) return the value; otherwise return the error string `\"invalid: <s>\"`. An optional leading `+` is allowed; `-5`, `abc`, an empty string, and 0 are invalid. Overflow beyond INT_MAX is invalid.",
    r'''#include <string>
#include <variant>
#include <iostream>

// std::variant<int, std::string> parse_positive(const std::string& s)
''',
    [
        ("valid", 'auto r = parse_positive("42");\nCHECK(std::holds_alternative<int>(r));\nCHECK_EQ(std::get<int>(r), 42);', "Success branch holds an int."),
        ("plus-sign", 'auto r = parse_positive("+7");\nCHECK(std::holds_alternative<int>(r));\nCHECK_EQ(std::get<int>(r), 7);', "A single leading + is permitted."),
        ("negative", 'auto r = parse_positive("-5");\nCHECK(std::holds_alternative<std::string>(r));\nCHECK_EQ(std::get<std::string>(r), std::string("invalid: -5"));', "Negatives are not positive — the error string includes the input."),
        ("zero-and-garbage", 'CHECK(std::holds_alternative<std::string>(parse_positive("0")));\nCHECK(std::holds_alternative<std::string>(parse_positive("1x2")));', "0 fails the positivity rule; mixed chars fail syntax."),
    ],
    level="combination",
)

# ---- checkpoint ----------------------------------------------------------------
CP_DESCRIBE = challenge(
    "cppi-checkpoint-modern",
    "Checkpoint: Describe a variant",
    "Implement `std::string describe(const std::variant<int, double, std::string>& v)` returning exactly `\"int: 42\"`, `\"double: 3.50\"` (always two decimals), or `\"string: hi\"` depending on the held alternative. Use `std::visit` with a generic lambda and `if constexpr` — no manual `index()` branching.",
    r'''#include <sstream>
#include <string>
#include <variant>
#include <iostream>

// std::string describe(const std::variant<int, double, std::string>& v)
''',
    [
        ("int-case", 'CHECK_EQ(describe(std::variant<int, double, std::string>{42}), std::string("int: 42"));', "The int branch prints the raw value."),
        ("double-case", 'CHECK_EQ(describe(std::variant<int, double, std::string>{3.5}), std::string("double: 3.50"));\nCHECK_EQ(describe(std::variant<int, double, std::string>{2.0}), std::string("double: 2.00"));', "Two decimals, always — std::fixed with precision 2."),
        ("string-case", 'CHECK_EQ(describe(std::variant<int, double, std::string>{std::string("hi")}), std::string("string: hi"));', "The string branch passes the text through."),
    ],
    difficulty="intermediate",
)

VI_SAFE_DIVIDE = vi_challenge(
    "Phép chia với std::optional",
    "Cài `std::optional<int> safe_divide(int a, int b)`: trả thương khi `b != 0`, và `std::nullopt` khi `b == 0`. Không ngoại lệ, không int-sentinel.",
    [
        ("basic", "Phép chia nguyên cắt cụt về phía 0."),
        ("zero", "Chia cho 0 là sự vắng mặt, không phải số 0."),
        ("negative", "Số âm theo cùng quy tắc cắt cụt."),
    ],
)

VI_PRIORITY = vi_challenge(
    "Trọng số enum class Priority",
    "Định nghĩa `enum class Priority { Low, Normal, High, Critical }` và cài `int priority_weight(Priority)` trả 0, 1, 5, 20 tương ứng. Dùng `switch` đầy đủ (không có case `default`) để một enumerator mới trong tương lai gây lỗi biên dịch.",
    [
        ("all-values", "Mỗi enumerator một trọng số, chính xác."),
        ("type-safe", "Giá trị enum class được truyền theo tên, không phải int thô."),
    ],
)

VI_PARSE = vi_challenge(
    "Parse số nguyên dương thành variant",
    "Cài `std::variant<int, std::string> parse_positive(const std::string& s)`. Thành công (một literal số nguyên hợp lệ lớn hơn 0, vừa int) thì trả giá trị; ngược lại trả chuỗi lỗi `\"invalid: <s>\"`. Cho phép một dấu `+` đầu chuỗi; `-5`, `abc`, chuỗi rỗng và 0 đều không hợp lệ. Tràn quá INT_MAX là không hợp lệ.",
    [
        ("valid", "Nhánh thành công giữ một int."),
        ("plus-sign", "Một dấu + duy nhất ở đầu được phép."),
        ("negative", "Số âm không phải số dương — chuỗi lỗi có kèm input."),
        ("zero-and-garbage", "0 rơi vào quy tắc tính dương; ký tự trộn lỗi cú pháp."),
    ],
)

VI_CP_DESCRIBE = vi_challenge(
    "Kiểm tra điểm: Mô tả một variant",
    "Cài `std::string describe(const std::variant<int, double, std::string>& v)` trả chính xác `\"int: 42\"`, `\"double: 3.50\"` (luôn hai chữ số thập phân), hoặc `\"string: hi\"` tùy phương án đang giữ. Dùng `std::visit` với generic lambda và `if constexpr` — không rẽ nhánh theo `index()` thủ công.",
    [
        ("int-case", "Nhánh int in giá trị thô."),
        ("double-case", "Luôn hai chữ số thập phân — std::fixed với precision 2."),
        ("string-case", "Nhánh string đưa văn bản đi qua nguyên vẹn."),
    ],
)

P1 = [CH_SAFE_DIVIDE, CH_PRIORITY]
VI_P1 = {"cppi-m7-safe-divide": VI_SAFE_DIVIDE, "cppi-m7-priority-weight": VI_PRIORITY}
P2 = [CH_PARSE]
VI_P2 = {"cppi-m7-parse-positive": VI_PARSE}

# ---- emit ---------------------------------------------------------------------
write_lesson(
    MOD, "auto-and-deduction",
    "auto and Type Deduction",
    "Where deduction helps, where it hides meaning, and decltype for same-type declarations.",
    20, L_auto_EN,
    "auto và suy luận kiểu",
    "Suy luận giúp gì ở đâu, khi nào nó che ý nghĩa, và decltype cho khai báo cùng-kiểu.",
    L_auto_VI,
)
write_lesson(
    MOD, "constexpr-enums",
    "constexpr and enum class",
    "Compile-time computation with static_assert, and scoped enums that refuse accidental int conversions.",
    25, L_constexpr_EN,
    "constexpr và enum class",
    "Tính toán lúc biên dịch với static_assert, và enum có phạm vi từ chối chuyển ngầm thành int.",
    L_constexpr_VI,
)
write_lesson(
    MOD, "optional-variant",
    "std::optional and std::variant",
    "Absence without sentinels, sum types with visit, and honest signatures for parse-style results.",
    30, L_optional_EN,
    "std::optional và std::variant",
    "Sự vắng mặt không cần sentinel, kiểu tổng với visit, và chữ ký trung thực cho kết quả kiểu parse.",
    L_optional_VI,
)
write_lesson(
    MOD, "modern-idioms",
    "Modern Idioms That Pay Rent",
    "string_view parameters, structured bindings, constexpr tables, and exhaustive switches over enum class.",
    25, L_idioms_EN,
    "Các idiom hiện đại đáng giá",
    "Tham số string_view, structured bindings, bảng constexpr, và switch đầy đủ trên enum class.",
    L_idioms_VI,
)

write_practice(
    MOD, "cppi-p7-utilities",
    "optional and enum practice",
    "A null-safe divide and a weighted enum with an exhaustive switch.",
    "Luyện optional và enum",
    "Phép chia an toàn và enum có trọng số với switch đầy đủ.",
    "constexpr-enums", 25, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m7-safe-divide", R_SAFE_DIVIDE, W_SAFE_DIVIDE),
        ("cppi-m7-priority-weight", R_PRIORITY_WEIGHT, W_PRIORITY_WEIGHT),
    ],
)
write_practice(
    MOD, "cppi-p7-variants",
    "variant practice",
    "Parse positive integers into a value-or-error variant.",
    "Luyện variant",
    "Parse số nguyên dương vào variant giá-trị-hoặc-lỗi.",
    "optional-variant", 30, "intermediate", P2, VI_P2,
    solutions=[
        ("cppi-m7-parse-positive", R_PARSE_POSITIVE, W_PARSE_POSITIVE),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-modern",
    "Checkpoint: One Function, Three Types",
    "std::visit + if constexpr formatting across a variant — the modern dispatch idiom under exam conditions.",
    35,
    r"""
`describe` is the module's exam: a three-way variant, one generic lambda,
and compile-time branch selection with `if constexpr`.

The design decisions you are rehearsing:

- the visitor handles every alternative — add a fourth alternative later
  and the lambda must grow or fail to compile
- `std::decay_t<decltype(x)>` names the held type inside the generic lambda
- the double case needs `std::fixed` with `precision(2)` BEFORE the value
  is streamed — output state is order-sensitive

If the int case passes but doubles print as `3.5`, you have rediscovered
why formatting state lives on the stream, not in the value.
""",
    "Kiểm tra điểm: Một hàm, ba kiểu",
    "std::visit + if constexpr định dạng trên variant — idiom điều phối hiện đại trong điều kiện thi.",
    r"""
`describe` là bài kiểm tra của module: một variant ba nhánh, một generic
lambda, và chọn nhánh lúc biên dịch bằng `if constexpr`.

Những quyết định thiết kế bạn đang luyện:

- visitor xử lý mọi phương án — thêm phương án thứ tư sau này thì lambda
  phải lớn lên hoặc không biên dịch
- `std::decay_t<decltype(x)>` gọi tên kiểu đang giữ bên trong generic lambda
- nhánh double cần `std::fixed` với `precision(2)` TRƯỚC khi đẩy giá trị —
  trạng thái định dạng nhạy với thứ tự

Nếu nhánh int pass nhưng double in ra `3.5`, bạn vừa tự khám phá vì sao
trạng thái định dạng nằm trên stream, không nằm trong giá trị.
""",
    CP_DESCRIBE, VI_CP_DESCRIBE,
    solution=R_DESCRIBE, wrong=W_DESCRIBE,
)

write_module(
    MOD,
    "Modern C++",
    "The modern toolkit: auto and deduction, constexpr and enum class, optional and variant, and the idioms that make C++ code safe by default.",
    "Modern C++",
    "Bộ công cụ hiện đại: auto và suy luận kiểu, constexpr và enum class, optional và variant, và các idiom giúp code C++ an toàn mặc định.",
    ["auto-and-deduction", "constexpr-enums", "optional-variant", "modern-idioms", "advanced-checkpoint-modern"],
    ["cppi-p7-utilities", "cppi-p7-variants"],
)
print("module 7 emitted")
