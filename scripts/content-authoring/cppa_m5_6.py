#!/usr/bin/env python3
"""C++ Advanced — module 5 (compile-time) and module 6 (ranges-views)."""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 5: compile-time ============================
M5 = "compile-time"

L5A = "constexpr-consteval-constinit"
L5B = "type-traits-ic"
L5C = "cppa-checkpoint-compiletime"

write_module(
    M5,
    "Compile-Time C++",
    "constexpr, consteval, constinit, and type traits — move work from runtime to build time and let the compiler refuse invalid configurations.",
    "C++ Lúc Biên Dịch",
    "constexpr, consteval, constinit và type traits — chuyển công việc từ runtime về build time, và để compiler từ chối các cấu hình không hợp lệ.",
    [L5A, L5B, L5C],
    ["m5-constexpr-practice", "m5-traits-practice"],
)

write_lesson(
    M5, L5A,
    "constexpr, consteval, constinit",
    "Three keywords, three contracts: can-run-at-compile-time, must-run-at-compile-time, and must-be-initialized-statically.",
    11,
    r'''
## constexpr — "can be constant"

On variables: the initializer must be a constant expression. On functions: the function *may* run at compile time when given constant arguments — and still runs at runtime otherwise. One implementation, both worlds:

```cpp
constexpr int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
constexpr int F = fib(10);          // compile time
int x = fib(runtimeInput);          // runtime, same body
```

## consteval — "must be immediate"

An **immediate function**: every call produces a compile-time constant; a runtime call is a hard error. Use for constructors of "compile-time-only" types and for functions whose result must be baked in:

```cpp
consteval int square(int n) { return n * n; }
constexpr int S = square(9);        // OK
// int y = square(runtimeVal);      // error: not a constant expression
```

## constinit — "initialized statically, checked at compile time"

`constinit` guarantees **static initialization** (no runtime constructor, no SIOF — static initialization order fiasco) while keeping the variable *mutable*:

```cpp
constinit std::atomic<unsigned> requests{0};   // zero-init at load, mutable later
```

The rule of thumb: `constexpr` = value is fixed; `constinit` = initialization is fixed, value is not.
''',
    "constexpr, consteval, constinit",
    "Ba từ khóa, ba hợp đồng: chạy được lúc biên dịch, bắt buộc lúc biên dịch, và khởi tạo tĩnh bắt buộc.",
    r'''
## constexpr — "có thể là hằng"

Trên biến: initializer phải là constant expression. Trên hàm: hàm *có thể* chạy lúc biên dịch khi nhận đối số hằng — và vẫn chạy lúc runtime nếu không. Một cài đặt, hai thế giới:

```cpp
constexpr int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
constexpr int F = fib(10);          // compile time
int x = fib(runtimeInput);          // runtime, cùng phần thân
```

## consteval — "bắt buộc ngay lập tức"

**Immediate function**: mọi lời gọi cho ra hằng compile-time; gọi lúc runtime là lỗi cứng. Dùng cho constructor của các kiểu "chỉ tồn tại lúc biên dịch" và các hàm mà kết quả phải được nướng sẵn:

```cpp
consteval int square(int n) { return n * n; }
constexpr int S = square(9);        // OK
// int y = square(runtimeVal);      // lỗi: không phải constant expression
```

## constinit — "khởi tạo tĩnh, kiểm tra lúc biên dịch"

`constinit` bảo đảm **static initialization** (không có constructor lúc chạy, không SIOF — static initialization order fiasco) trong khi biến vẫn *được phép thay đổi*:

```cpp
constinit std::atomic<unsigned> requests{0};   // zero-init khi nạp, đổi được sau
```

Nguyên tắc nhớ nhanh: `constexpr` = giá trị cố định; `constinit` = cách khởi tạo cố định, giá trị thì không.
''',
    difficulty="advanced",
)

write_lesson(
    M5, L5B,
    "Type Traits and std::integral_constant",
    "The original metaprogramming interface: traits answer questions about types, integral_constant carries compile-time values as types.",
    10,
    r'''
## Traits: questions about types

`std::is_integral_v<T>`, `std::is_same_v<A, B>`, `std::is_nothrow_move_constructible_v<T>`, `std::underlying_type_t<E>` — each is a compile-time query. Traits come in `_t` (type result) and `_v` (value result) flavors; the `_v` forms are the modern spelling of `::value`.

## std::integral_constant: a value wearing a type

`std::integral_constant<int, 5>` is a *type* whose value is part of it. That lets you pass compile-time numbers through normal overload machinery — dispatch on value:

```cpp
constexpr int route(std::integral_constant<int, 0>) { return 0; }  // empty pack
constexpr int route(std::integral_constant<int, 1>) { return 1; }  // one element
```

You rarely write the type by hand — you usually receive it: a function template parameter `std::size_t N` produces `std::integral_constant<std::size_t, N>` when deduced through helpers, and `std::bool_constant<B>` is `integral_constant<bool, B>`.

## When traits beat if constexpr

Use traits in *concepts and constraints* (Module 4) and in type-level arithmetic (`std::conditional_t<flag, A, B>`). Use `if constexpr` when *values* in the function body differ. The graded exercises use both together.
''',
    "Type Traits và std::integral_constant",
    "Giao diện metaprogramming gốc: traits trả lời câu hỏi về kiểu, integral_constant mang giá trị compile-time dưới dạng kiểu.",
    r'''
## Traits: câu hỏi về kiểu

`std::is_integral_v<T>`, `std::is_same_v<A, B>`, `std::is_nothrow_move_constructible_v<T>`, `std::underlying_type_t<E>` — mỗi cái là một truy vấn compile-time. Traits có hai hương: `_t` (kết quả là kiểu) và `_v` (kết quả là giá trị); dạng `_v` là cách viết hiện đại của `::value`.

## std::integral_constant: một giá trị đội lốt kiểu

`std::integral_constant<int, 5>` là một *kiểu* mà giá trị là một phần của nó. Nhờ vậy bạn chuyển số compile-time qua cơ chế overload bình thường — dispatch theo giá trị:

```cpp
constexpr int route(std::integral_constant<int, 0>) { return 0; }  // pack rỗng
constexpr int route(std::integral_constant<int, 1>) { return 1; }  // một phần tử
```

Bạn hiếm khi tự viết kiểu này — thường bạn *nhận* nó: tham số template `std::size_t N` sinh ra `std::integral_constant<std::size_t, N>` khi được suy qua các helper, và `std::bool_constant<B>` chính là `integral_constant<bool, B>`.

## Khi nào traits thắng if constexpr

Dùng traits trong *concept và ràng buộc* (Module 4) và trong phép toán cấp kiểu (`std::conditional_t<flag, A, B>`). Dùng `if constexpr` khi *giá trị* trong thân hàm khác nhau. Các bài tập chấm điểm dùng cả hai cùng lúc.
''',
    difficulty="advanced",
)

# ---- module 5 practices ----
PARSE_BOILER = r'''#include <cstddef>
#include <string>
#include <string_view>

// Parse "name:value;name2:value2" into the output at COMPILE time,
// recording the entries into the provided fixed storage.
// Return the number of entries parsed.
constexpr std::size_t parseSpec(std::string_view spec,
                                std::string_view names[],
                                int values[],
                                std::size_t maxEntries);
'''

CH_CONSTEXPR_PARSE = challenge(
    "cppa5-constexpr-parse",
    "A constexpr Config Parser",
    "Implement `parseSpec` as a `constexpr` function: split on `;`, each entry on the first `:`, trim spaces, store name and int value, and return the count. The test bakes the result into a compile-time constant — the proof that the whole parser runs before main.",
    PARSE_BOILER,
    [
        ("runtime parse works",
         r'''std::string_view n[4]; int v[4];
CHECK_EQ(parseSpec("port: 8080; retries: 3", n, v, 4), std::size_t{2});
CHECK_EQ(n[0], std::string_view("port"));
CHECK_EQ(v[0], 8080);
CHECK_EQ(n[1], std::string_view("retries"));
CHECK_EQ(v[1], 3);''',
         "Walk the string_view: find ';' and ':', substr, trim ' ', std::stoi is NOT constexpr — parse the digits yourself (v = v*10 + (c - '0'))."),
        ("compile-time parse works",
         r'''constexpr std::string_view cn[2] = {}; constexpr int cv[2] = {};
// constexpr locals with mutation need C++14+ constexpr semantics:
constexpr auto count = [] {
    std::string_view names[2];
    int values[2];
    std::size_t c = parseSpec("a: 1; b: 22", names, values, 2);
    return c == 2 && values[1] == 22;
}();
static_assert(count, "must parse at compile time");''',
         "constexpr functions may mutate local arrays — the lambda runs the same code at compile time; keep every operation constexpr-legal (no std::stoi, no allocations)."),
    ],
    difficulty="advanced",
)

VI_CONSTEXPR_PARSE = vi_challenge(
    "Parser constexpr cho cấu hình",
    "Cài `parseSpec` là hàm `constexpr`: tách theo `;`, mỗi mục tách tại dấu `:` đầu tiên, cắt khoảng trắng, lưu tên và giá trị int, trả về số mục. Bài kiểm tra nướng kết quả thành hằng compile-time — bằng chứng toàn bộ parser chạy trước main.",
    [
        ("parse lúc chạy đúng", "Duyệt string_view: tìm ';' và ':', substr, cắt ' ', std::stoi KHÔNG phải constexpr — tự parse chữ số (v = v*10 + (c - '0'))."),
        ("parse lúc biên dịch được", "Hàm constexpr được phép thay đổi mảng cục bộ — lambda chạy cùng code đó lúc compile; giữ mọi thao tác hợp lệ constexpr (không std::stoi, không cấp phát)."),
    ],
)

VALTEST_BOILER = r'''#include <concepts>
#include <cstddef>
#include <type_traits>

// TODO: consteval unsigned specVersion(unsigned v);
//       must REJECT versions below 2 at compile time:
//       throw (or fail to be a constant expression) for v < 2.
// TODO: constexpr unsigned pick(bool useA, unsigned a, unsigned b);
'''

CH_CONSTEVAL_GATE = challenge(
    "cppa5-consteval-gate",
    "consteval as a Compile-Time Gate",
    "Implement `specVersion` as `consteval`, rejecting anything below version 2 at compile time (throw in the constexpr path), and `pick` as a plain constexpr selector.",
    VALTEST_BOILER,
    [
        ("valid versions pass at compile time",
         r'''constexpr unsigned v = specVersion(3);
static_assert(v == 3, "baked");
CHECK_EQ(pick(true, 1, 2), 1);
CHECK_EQ(pick(false, 1, 2), 2);''',
         "consteval unsigned specVersion(unsigned v) { if (v < 2) throw \"too old\"; return v; } — throw is allowed in constexpr paths to FAIL compilation."),
        ("pick selects at compile time too",
         r'''static_assert(pick(false, 10, 20) == 20, "selector");''',
         "constexpr unsigned pick(bool useA, unsigned a, unsigned b) { return useA ? a : b; }"),
    ],
    difficulty="advanced",
)

VI_CONSTEVAL_GATE = vi_challenge(
    "consteval làm cổng compile-time",
    "Cài `specVersion` là `consteval`, từ chối mọi thứ dưới phiên bản 2 ngay lúc biên dịch (throw trong đường constexpr), và `pick` là constexpr selector thường.",
    [
        ("phiên bản hợp lệ pass lúc biên dịch", "consteval unsigned specVersion(unsigned v) { if (v < 2) throw \"too old\"; return v; } — throw được phép trong đường constexpr để khiếm BIÊN DỊCH thất bại."),
        ("pick cũng chọn được lúc biên dịch", "constexpr unsigned pick(bool useA, unsigned a, unsigned b) { return useA ? a : b; }"),
    ],
)

CH_TRAITS_IC = challenge(
    "cppa5-traits-dispatch",
    "Dispatch on Type and Value",
    "Implement `kindName<T>()` returning \"int\", \"double\", \"string\", or \"other\" via traits; and `pickN<K>(a, b)` where `K` is a `std::size_t` NTTP returning the K-th argument (K beyond 1 wraps).",
    r'''#include <cstddef>
#include <string>
#include <type_traits>

template <class T>
std::string kindName();   // traits-based classification

template <std::size_t K, class A, class B>
auto pickN(A a, B b);     // K==0 -> a, K>=1 -> b (wrap)
''',
    [
        ("kindName classifies by traits",
         r'''CHECK_EQ(kindName<int>(), std::string("int"));
CHECK_EQ(kindName<double>(), std::string("double"));
CHECK_EQ(kindName<std::string>(), std::string("string"));
CHECK_EQ(kindName<std::size_t>(), std::string("int"));   // size_t is integral
CHECK_EQ(kindName<std::vector<int>>(), std::string("other"));''',
         "if constexpr (std::is_integral_v<T>) return \"int\"; else if constexpr (std::is_floating_point_v<T>) ... else if constexpr (std::is_same_v<T, std::string>) ... else \"other\"."),
        ("pickN wraps by NTTP",
         r'''CHECK_EQ(pickN<0>(1, 2), 1);
CHECK_EQ(pickN<1>(1, 2), 2);
CHECK_EQ(pickN<5>(1, 2), 2);
CHECK_EQ(pickN<4>(1, 2), 1);''',
         "return K % 2 == 0 ? a : b; — the NTTP is part of the type, so each K is a distinct instantiation."),
    ],
    difficulty="advanced",
)

VI_TRAITS_IC = vi_challenge(
    "Dispatch theo kiểu và giá trị",
    "Cài `kindName<T>()` trả về \"int\", \"double\", \"string\", hoặc \"other\" bằng traits; và `pickN<K>(a, b)` với `K` là NTTP `std::size_t` trả về đối số thứ K (K vượt 1 thì quấn vòng).",
    [
        ("kindName phân loại bằng traits", "if constexpr (std::is_integral_v<T>) return \"int\"; else if constexpr (std::is_floating_point_v<T>) ... else if constexpr (std::is_same_v<T, std::string>) ... else \"other\"."),
        ("pickN quấn theo NTTP", "return K % 2 == 0 ? a : b; — NTTP là một phần của kiểu, mỗi K là một khởi tạo riêng."),
    ],
)

M5_PRAC1 = dict(
    sid="m5-constexpr-practice",
    title="Compile-Time Computing",
    description="A constexpr parser baked into constants, consteval validation gates, and constexpr selectors.",
    vi_title="Tính toán lúc biên dịch",
    vi_description="Parser constexpr nướng vào hằng số, cổng kiểm tra consteval, và selector constexpr.",
    after_lesson=L5A,
    minutes=22,
    difficulty="advanced",
)

M5_PRAC1_CH = [CH_CONSTEXPR_PARSE, CH_CONSTEVAL_GATE, CH_TRAITS_IC]
M5_PRAC1_VI = {"cppa5-constexpr-parse": VI_CONSTEXPR_PARSE,
               "cppa5-consteval-gate": VI_CONSTEVAL_GATE,
               "cppa5-traits-dispatch": VI_TRAITS_IC}

M5_PRAC1_SOL = [
    ("cppa5-constexpr-parse",
     PARSE_BOILER + "\nconstexpr std::size_t parseSpec(std::string_view spec, std::string_view names[], int values[], std::size_t maxEntries) {\n    std::size_t count = 0, pos = 0;\n    while (pos < spec.size() && count < maxEntries) {\n        while (pos < spec.size() && spec[pos] == ' ') ++pos;\n        std::size_t semi = pos;\n        while (semi < spec.size() && spec[semi] != ';') ++semi;\n        std::size_t colon = pos;\n        while (colon < semi && spec[colon] != ':') ++colon;\n        if (colon == semi) break;\n        std::size_t e = colon;\n        while (e > pos && spec[e-1] == ' ') --e;\n        std::size_t s2 = pos;\n        while (s2 < e && spec[s2] == ' ') ++s2;\n        names[count] = spec.substr(s2, e - s2);\n        std::size_t vstart = colon + 1;\n        while (vstart < semi && spec[vstart] == ' ') ++vstart;\n        int val = 0;\n        for (std::size_t i = vstart; i < semi; ++i) {\n            char c = spec[i];\n            if (c >= '0' && c <= '9') val = val * 10 + (c - '0');\n        }\n        values[count] = val;\n        ++count;\n        pos = semi + 1;\n    }\n    return count;\n}\n",
     PARSE_BOILER + "\nconstexpr std::size_t parseSpec(std::string_view spec, std::string_view names[], int values[], std::size_t maxEntries) {\n    std::size_t count = 0, pos = 0;\n    while (pos < spec.size() && count < maxEntries) {\n        std::size_t semi = pos;\n        while (semi < spec.size() && spec[semi] != ';') ++semi;\n        std::size_t colon = pos;\n        while (colon < semi && spec[colon] != ':') ++colon;\n        if (colon == semi) break;\n        names[count] = spec.substr(pos, colon - pos);   // WRONG: no trim of spaces\n        int val = 0;\n        for (std::size_t i = colon + 1; i < semi; ++i) val = val * 10 + (spec[i] - '0');  // WRONG: includes spaces -> garbage\n        values[count] = val;\n        ++count;\n        pos = semi + 1;\n    }\n    return count;\n}\n"),
    ("cppa5-consteval-gate",
     VALTEST_BOILER + "\nconsteval unsigned specVersion(unsigned v) { if (v < 2) throw \"spec too old\"; return v; }\nconstexpr unsigned pick(bool useA, unsigned a, unsigned b) { return useA ? a : b; }\n",
     VALTEST_BOILER + "\nconsteval unsigned specVersion(unsigned v) { if (v < 5) throw \"spec too old\"; return v; }  // WRONG: gate set to 5, v==3 must pass\nconstexpr unsigned pick(bool useA, unsigned a, unsigned b) { return useA ? a : b; }\n"),
    ("cppa5-traits-dispatch",
     r'''#include <cstddef>
#include <string>
#include <type_traits>
#include <vector>

template <class T>
std::string kindName() {
    if constexpr (std::is_integral_v<T>) return "int";
    else if constexpr (std::is_floating_point_v<T>) return "double";
    else if constexpr (std::is_same_v<T, std::string>) return "string";
    else return "other";
}

template <std::size_t K, class A, class B>
auto pickN(A a, B b) { return K % 2 == 0 ? a : b; }
''',
     r'''#include <cstddef>
#include <string>
#include <type_traits>
#include <vector>

template <class T>
std::string kindName() {
    if constexpr (std::is_integral_v<T>) return "int";
    else if constexpr (std::is_floating_point_v<T>) return "double";
    else if constexpr (std::is_same_v<T, std::string>) return "string";
    else return "other";
}

template <std::size_t K, class A, class B>
auto pickN(A a, B b) { return K % 2 == 0 ? b : a; }  // WRONG: parity flipped
'''),
]

write_practice(M5, **M5_PRAC1, challenges=M5_PRAC1_CH, vi_challenges=M5_PRAC1_VI, solutions=M5_PRAC1_SOL)

M5_PRAC2 = dict(
    sid="m5-traits-practice",
    title="Traits in Constraints",
    description="Strengthen concepts with trait plumbing and std::conditional_t type selection.",
    vi_title="Traits trong ràng buộc",
    vi_description="Củng cố concept bằng plumbing traits và std::conditional_t để chọn kiểu.",
    after_lesson=L5B,
    minutes=14,
    difficulty="advanced",
)

CH_CONDITIONAL = challenge(
    "cppa5-conditional-type",
    "std::conditional_t Type Selection",
    "Implement `Storage<T>` whose `value_type` is `T` for small types (<= 8 bytes) but `std::shared_ptr<T>` for large ones — via `std::conditional_t` — plus `biggest(a, b)` returning the larger by reference using `std::conditional_t` on a comparison trait is overkill; just use std::conditional_t<std::is_integral_v<T>, int, double> fallback semantics in `numberKind<T>()`.",
    r'''#include <cstddef>
#include <memory>
#include <string>
#include <type_traits>

template <class T>
struct Storage {
    // TODO: using value_type = ...;   // T if sizeof(T) <= 8 else std::shared_ptr<T>
};

// TODO: template <class T> using Scalar = std::conditional_t<std::is_integral_v<T>, long long, double>;
template <class T>
using Scalar;   // finish the alias
''',
    [
        ("small types store inline",
         r'''static_assert(std::is_same_v<Storage<int>::value_type, int>, "small stays inline");''',
         "using value_type = std::conditional_t<sizeof(T) <= 8, T, std::shared_ptr<T>>;"),
        ("large types store via shared_ptr",
         r'''struct Big { char pad[64]; };
static_assert(std::is_same_v<Storage<Big>::value_type, std::shared_ptr<Big>>, "big goes indirect");''',
         "Same conditional — sizeof(Big) is 64, so the shared_ptr branch selects."),
        ("Scalar alias switches on integrality",
         r'''static_assert(std::is_same_v<Scalar<int>, long long>, "integral -> long long");
static_assert(std::is_same_v<Scalar<double>, double>, "floating -> double");''',
         "template <class T> using Scalar = std::conditional_t<std::is_integral_v<T>, long long, double>;"),
    ],
    difficulty="advanced",
)

VI_CONDITIONAL = vi_challenge(
    "std::conditional_t chọn kiểu",
    "Cài `Storage<T`> mà `value_type` là `T` với kiểu nhỏ (<= 8 byte) nhưng `std::shared_ptr<T>` với kiểu lớn — qua `std::conditional_t` — cùng alias `Scalar<T>` chuyển kiểu nguyên sang long long, kiểu chấm động sang double.",
    [
        ("kiểu nhỏ lưu trực tiếp", "using value_type = std::conditional_t<sizeof(T) <= 8, T, std::shared_ptr<T>>;"),
        ("kiểu lớn lưu qua shared_ptr", "Cùng conditional — sizeof(Big) là 64 nên nhánh shared_ptr được chọn."),
        ("alias Scalar đổi theo tính nguyên", "template <class T> using Scalar = std::conditional_t<std::is_integral_v<T>, long long, double>;"),
    ],
)

M5_PRAC2_CH = [CH_CONDITIONAL]
M5_PRAC2_VI = {"cppa5-conditional-type": VI_CONDITIONAL}

M5_PRAC2_SOL = [
    ("cppa5-conditional-type",
     r'''#include <cstddef>
#include <memory>
#include <string>
#include <type_traits>

template <class T>
struct Storage {
    using value_type = std::conditional_t<sizeof(T) <= 8, T, std::shared_ptr<T>>;
};

template <class T>
using Scalar = std::conditional_t<std::is_integral_v<T>, long long, double>;
''',
     r'''#include <cstddef>
#include <memory>
#include <string>
#include <type_traits>

template <class T>
struct Storage {
    using value_type = std::conditional_t<sizeof(T) <= 16, T, std::shared_ptr<T>>;  // WRONG: threshold 16
};

template <class T>
using Scalar = std::conditional_t<std::is_integral_v<T>, double, double>;  // WRONG: both branches double
'''),
]

write_practice(M5, **M5_PRAC2, challenges=M5_PRAC2_CH, vi_challenges=M5_PRAC2_VI, solutions=M5_PRAC2_SOL)

# ---- module 5 checkpoint ----
CP5_MD = r'''
The compile-time checkpoint: a constexpr prefix-sum table, validated by static_assert.
'''

CP5_BOILER = r'''#include <cstddef>

// TODO: constexpr int tableSum(const int* a, std::size_t n);  // sum via constexpr recursion/loop
// The graded test builds the sum at compile time via a lambda and static_asserts it.
'''

write_checkpoint(
    M5, L5C,
    "Checkpoint: Compile-Time",
    "Prove constexpr computation survives the grader: a sum computed before main runs.",
    14,
    CP5_MD,
    "Checkpoint: Compile-Time",
    "Chứng minh phép tính constexpr sống sót qua grader: một tổng được tính trước khi main chạy.",
    r'''
Checkpoint compile-time: bảng prefix-sum constexpr, xác thực bằng static_assert.
''',
    challenge(
        "cppa5-compiletime-checkpoint",
        "Bake the Sum",
        "Implement `tableSum` so the test computes it at compile time inside a lambda and static_asserts the result.",
        CP5_BOILER,
        [
            ("compile-time sum bakes",
             r'''constexpr auto baked = [] { constexpr int d[] = {3, 1, 4, 1, 5}; return tableSum(d, 5); }();
int live5[] = {3, 1, 4, 1, 5};
static_assert(baked == 14, "must compute at compile time");
CHECK_EQ(tableSum(live5, 5), 14);''',
             "constexpr int tableSum(const int* a, std::size_t n) { int s = 0; for (std::size_t i = 0; i < n; ++i) s += a[i]; return s; } — loops are fine in constexpr."),
            ("runtime use still works",
             r'''int live[] = {10, 20, 30};
CHECK_EQ(tableSum(live, 3), 60);''',
             "Same function serves runtime arrays — constexpr is a capability, not a restriction."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Nướng tổng vào hằng số",
        "Cài `tableSum` để bài kiểm tra tính nó lúc biên dịch trong một lambda và static_assert kết quả.",
        [
            ("tổng compile-time được nướng", "constexpr int tableSum(const int* a, std::size_t n) { int s = 0; for (std::size_t i = 0; i < n; ++i) s += a[i]; return s; } — vòng lặp là hợp lệ trong constexpr."),
            ("dùng lúc chạy vẫn ổn", "Cùng hàm phục vụ mảng runtime — constexpr là năng lực, không phải giới hạn."),
        ],
    ),
    solution=CP5_BOILER + "\nconstexpr int tableSum(const int* a, std::size_t n) { int s = 0; for (std::size_t i = 0; i < n; ++i) s += a[i]; return s; }\n",
    wrong=CP5_BOILER + "\nconstexpr int tableSum(const int* a, std::size_t n) { int s = 1; for (std::size_t i = 0; i < n; ++i) s += a[i]; return s; }  // WRONG: starts at 1\n",
)

# ============================ MODULE 6: ranges-views ============================
M6 = "ranges-views"

L6A = "views-pipelines"
L6B = "projections-custom"
L6C = "view-dangling"
L6D = "cppa-checkpoint-ranges"

write_module(
    M6,
    "Ranges & Lazy Pipelines",
    "Views, adaptors, projections, and custom pipelines — transform data lazily, compose cleanly, and know exactly where view lifetimes bite.",
    "Ranges & Pipeline Lười",
    "View, adaptor, projection và pipeline tùy biến — biến đổi dữ liệu lười biếng, kết hợp gọn gàng, và biết chính xác chỗ vòng đời của view cắn bạn.",
    [L6A, L6B, L6C, L6D],
    ["m6-pipeline-practice", "m6-custom-view-practice", "m6-dangling-practice"],
)

write_lesson(
    M6, L6A,
    "Views and Pipelines",
    "A view is a non-owning range. Adaptors compose with |; nothing runs until you iterate.",
    11,
    r'''
## The mental model

A **view** is a lightweight, non-owning wrapper over elements — it *presents* data differently without copying it. Adaptation is lazy: building the pipeline does no work; iterating pulls elements through it.

```cpp
namespace rv = std::views;

int total = 0;
for (int v : rv::iota(1, 11) | rv::filter([](int x) { return x % 2 == 0; })
                             | rv::transform([](int x) { return x * x; })) {
    total += v;
}
// total == 220 — squares of 2,4,6,8,10, computed one element at a time
```

`rv::iota(1, 11)` is a generated range — no vector exists. `filter` skips; `transform` maps; `take`/`drop` slice; `reverse` walks backwards. `views::all(v)` materializes a container into a view when you need the boundary.

## Why pipelines win

- **No intermediate containers**: chained algorithm calls would build a vector per stage; views build none.
- **Single pass composition**: each element flows through the whole chain before the next one starts — cache-friendly and early-exit-able (`take(5)` stops the whole pipeline).
- **Composability**: the pipeline is a value; store it, pass it, reuse it.

## The costs to respect

Iteration is not free (a filter+transform chain re-tests per element); deeply nested lambdas can hurt inlining; and — the big one — a view **does not own** what it points at. That is the next lessons' subject.
''',
    "View và Pipeline",
    "View là range không sở hữu dữ liệu. Adaptor kết hợp bằng |; không gì chạy cho tới khi bạn duyệt.",
    r'''
## Mô hình tư duy

**View** là lớp bọc nhẹ, không sở hữu dữ liệu — nó *trình diễn* dữ liệu khác đi mà không sao chép. Phép biến đổi là lười biếng: dựng pipeline không tốn công; duyệt thì kéo phần tử đi qua nó.

```cpp
namespace rv = std::views;

int total = 0;
for (int v : rv::iota(1, 11) | rv::filter([](int x) { return x % 2 == 0; })
                             | rv::transform([](int x) { return x * x; })) {
    total += v;
}
// total == 220 — bình phương của 2,4,6,8,10, tính từng phần tử một
```

`rv::iota(1, 11)` là range sinh ra — không có vector nào tồn tại. `filter` bỏ qua; `transform` ánh xạ; `take`/`drop` cắt lát; `reverse` đi ngược. `views::all(v)` biến container thành view khi bạn cần ranh giới.

## Vì sao pipeline thắng

- **Không container trung gian**: chuỗi thuật toán thường phải dựng một vector mỗi giai đoạn; view thì không.
- **Kết hợp một lượt**: mỗi phần tử chảy hết chuỗi trước khi phần tử kế tiếp bắt đầu — thân thiện cache và thoát sớm được (`take(5)` dừng cả pipeline).
- **Khả năng kết hợp**: pipeline là một giá trị; lưu nó, chuyển nó, tái sử dụng nó.

## Những cái giá phải tôn trọng

Duyệt không miễn phí (chuỗi filter+transform kiểm tra lại từng phần tử); lambda lồng sâu có thể hại inlining; và — cái lớn nhất — view **không sở hữu** thứ nó trỏ tới. Đó là chủ đề của bài học kế tiếp.
''',
    difficulty="advanced",
)

write_lesson(
    M6, L6B,
    "Projections and Custom Views",
    "Projections decouple sorting/keying from element type; writing your own view teaches you the range machinery for real.",
    12,
    r'''
## Projections: transform for algorithms

Most range algorithms accept a final **projection** — a callable applied to elements before the algorithm sees them:

```cpp
std::vector<Student> roster = ...;
std::ranges::sort(roster, std::ranges::less{}, &Student::score);   // sort by score
auto oldest = std::ranges::max_element(roster, {}, &Student::age);
```

No copy, no pre-transform pass, no separate key vector. `{}` is the default comparator; the projection goes last.

## The view interface — what "custom" means

A minimal view needs: `begin`/`end` (iterators), and `empty`/`size` when cheaply available. The practical recipe: store a `std::ranges::range` reference + your parameters, expose an iterator whose `operator++` and `operator*` implement your transformation, and mark the wrapper `std::ranges::view`-compatible by inheriting view semantics (or simply deriving from `std::ranges::view_interface`).

```cpp
template <std::ranges::view V>
class SquaredView : public std::ranges::view_interface<SquaredView<V>> {
    V base_;
public:
    SquaredView() = default;
    explicit SquaredView(V v) : base_(std::move(v)) {}
    auto begin() const { return std::ranges::begin(base_); }   // simplified: transform iterator
    auto end() const   { return std::ranges::end(base_); }
};
```

The *real* custom view uses `std::views::transform`-style iterator adaptation; the graded exercise instead has you build a **stride view** (every K-th element) with a hand-written iterator — small enough to finish, complete enough to teach the machinery.
''',
    "Projection và View Tùy Biến",
    "Projection tách việc sắp xếp/lập khóa khỏi kiểu phần tử; tự viết một view dạy bạn cơ chế range thật sự.",
    r'''
## Projection: transform cho thuật toán

Hầu hết thuật toán range nhận một **projection** ở cuối — callable áp lên phần tử trước khi thuật toán nhìn thấy:

```cpp
std::vector<Student> roster = ...;
std::ranges::sort(roster, std::ranges::less{}, &Student::score);   // sort theo score
auto oldest = std::ranges::max_element(roster, {}, &Student::age);
```

Không copy, không lượt biến đổi trước, không vector khóa riêng. `{}` là comparator mặc định; projection đi cuối.

## Giao diện view — "tùy biến" nghĩa là gì

Một view tối thiểu cần: `begin`/`end` (iterator), và `empty`/`size` khi có sẵn rẻ. Công thức thực tế: lưu một tham chiếu `std::ranges::range` + tham số của bạn, phơi ra một iterator mà `operator++` và `operator*` cài đặt phép biến đổi của bạn, và đánh dấu lớp bọc tương thích `std::ranges::view` (hoặc đơn giản là kế thừa `std::ranges::view_interface`).

```cpp
template <std::ranges::view V>
class SquaredView : public std::ranges::view_interface<SquaredView<V>> {
    V base_;
public:
    SquaredView() = default;
    explicit SquaredView(V v) : base_(std::move(v)) {}
    auto begin() const { return std::ranges::begin(base_); }   // đơn giản hóa: iterator transform
    auto end() const   { return std::ranges::end(base_); }
};
```

View tùy biến *đúng nghĩa* dùng kiểu thích ứng iterator theo phong cách `std::views::transform`; bài tập chấm điểm thay vào đó yêu cầu dựng một **stride view** (mỗi phần tử thứ K) với iterator viết tay — vừa đủ nhỏ để hoàn thành, vừa đủ đầy để dạy cơ chế.
''',
    difficulty="advanced",
)

write_lesson(
    M6, L6C,
    "View Dangling: The #1 Ranges Bug",
    "A view borrows. Pipe it over a temporary and the pipeline dangles. C++20 rejects the classic case; C++23 relaxed it — learn the rule, not the folklore.",
    11,
    r'''
## The bug

```cpp
auto bad = std::string{"data"} | std::views::transform(f);   // dangles: the string dies on this line
```

The view stores a reference to its source. If the source is a temporary **container**, the view outlives it — every use after is UB.

## The rule

- C++20 **rejects at compile time** the classic case: piping a *container* rvalue into a view (the owning-rvalue rule). It cannot catch everything: `auto v = std::views::iota(0) | std::views::take(5);` is safe (iota owns its state), but piping a *view* that itself borrowed a temporary still slips through.
- C++23 relaxed the most-annoying cases (owning rvalues are now allowed in more adaptor positions). With `-std=c++20`, learn the conservative rule:

**Conservative rule: a view may only borrow from things that outlive the view variable.** Named container, static, or another view with a provable lifetime. If you need a temporary's data, materialize: `auto owned = src | ... | std::ranges::to<std::vector>();` (C++23) or copy into a named vector in C++20.

## Spotting it in review

- `auto v = getContainer() | views::filter(...)` — dangles (getContainer returns a temporary),
- `for (auto x : makeVec() | views::take(3))` — actually safe: the temporary lives for the full range-for statement, the classic exception,
- `class C { std::span<int> s_; ... };` storing a span of a local in a constructor — dangles at the constructor's exit.

The graded exercises are a spotting clinic: mark each snippet safe/dangle, then fix the danging one by materializing.
''',
    "View Dangling: Lỗi Số 1 Của Ranges",
    "View là mượn. Nối nó với một đối tượng tạm và pipeline sẽ dangling. C++20 từ chối ca kinh điển; C++23 nới lỏng — hãy học quy tắc, không học tin đồn.",
    r'''
## Cái lỗi

```cpp
auto bad = std::string{"data"} | std::views::transform(f);   // dangling: chuỗi chết ngay dòng này
```

View lưu tham chiếu đến nguồn. Nếu nguồn là **container** tạm, view sống lâu hơn nó — mọi lần dùng sau là UB.

## Quy tắc

- C++20 **từ chối lúc biên dịch** ca kinh điển: nối một rvalue *container* vào view (quy tắc owning-rvalue). Nó không bắt được tất cả: `auto v = std::views::iota(0) | std::views::take(5);` là an toàn (iota tự giữ trạng thái), nhưng nối một *view* vốn đang mượn một đối tượng tạm vẫn lọt qua.
- C++23 nới lỏng các ca khó chịu nhất (owning rvalue được phép ở nhiều vị trí adaptor hơn). Với `-std=c++20`, hãy học quy tắc bảo thủ:

**Quy tắc bảo thủ: view chỉ được mượn từ những thứ sống lâu hơn biến view.** Container có tên, static, hoặc một view khác có vòng đời chứng minh được. Nếu cần dữ liệu của đối tượng tạm, hãy cụ thể hóa: `auto owned = src | ... | std::ranges::to<std::vector>();` (C++23) hoặc copy vào một vector có tên trong C++20.

## Nhận diện khi review

- `auto v = getContainer() | views::filter(...)` — dangling (getContainer trả về đối tượng tạm),
- `for (auto x : makeVec() | views::take(3))` — thực ra an toàn: đối tượng tạm sống suốt câu range-for, ngoại lệ kinh điển,
- `class C { std::span<int> s_; ... };` lưu span của biến cục bộ trong constructor — dangling khi constructor kết thúc.

Các bài tập chấm điểm là phòng khám nhận diện: dán nhãn an toàn/dangling cho từng đoạn, rồi sửa đoạn dangling bằng cách cụ thể hóa.
''',
    difficulty="advanced",
)

# ---- module 6 practices ----
PIPE_BOILER = r'''#include <ranges>
#include <string>
#include <vector>

// Sum of squares of even numbers in [1, limit).
int sumEvenSquares(int limit);

// Concatenate (space-separated) the uppercased first letters of words longer
// than n characters, in order. Words come in a vector<string>.
std::string initials(const std::vector<std::string>& words, std::size_t n);
'''

CH_PIPELINE_BASICS = challenge(
    "cppa6-pipeline-basics",
    "Lazy Pipelines by Hand",
    "Implement `sumEvenSquares` with `views::iota | filter | transform` and `initials` with `filter | transform` — no loops over intermediate containers.",
    PIPE_BOILER,
    [
        ("sumEvenSquares matches the math",
         r'''CHECK_EQ(sumEvenSquares(11), 220);
CHECK_EQ(sumEvenSquares(1), 0);
CHECK_EQ(sumEvenSquares(2), 0);''',
         "namespace rv = std::views; for (int v : rv::iota(1, limit) | rv::filter([](int x){ return x % 2 == 0; }) | rv::transform([](int x){ return x * x; })) total += v;"),
        ("initials filters and maps",
         r'''std::vector<std::string> words{"alpha", "be", "gamma", "hi", "fog", "delta"};
CHECK_EQ(initials(words, 3), std::string("AGD"));  // "fog" is exactly 3 chars: excluded (strictly greater)''',
         "words | rv::filter([n](const std::string& w){ return w.size() > n; }) | rv::transform([](const std::string& w){ return (char)std::toupper((unsigned char)w[0]); }) — accumulate into a string."),
    ],
    difficulty="advanced",
)

VI_PIPELINE_BASICS = vi_challenge(
    "Pipeline lười bằng tay",
    "Cài `sumEvenSquares` bằng `views::iota | filter | transform` và `initials` bằng `filter | transform` — không dùng vòng lặp trên container trung gian.",
    [
        ("sumEvenSquares khớp toán học", "namespace rv = std::views; for (int v : rv::iota(1, limit) | rv::filter([](int x){ return x % 2 == 0; }) | rv::transform([](int x){ return x * x; })) total += v;"),
        ("initials lọc và ánh xạ", "words | rv::filter([n](const std::string& w){ return w.size() > n; }) | rv::transform([](const std::string& w){ return (char)std::toupper((unsigned char)w[0]); }) — cộng dồn vào một chuỗi."),
    ],
)

PROJ_BOILER = r'''#include <algorithm>
#include <ranges>
#include <string>
#include <vector>

struct Employee {
    std::string name;
    int level;
    double salary;
};

// Return the name of the highest-salary employee.
std::string topEarner(const std::vector<Employee>& staff);

// Sort in place by level (ascending), ties by name.
void sortRoster(std::vector<Employee>& staff);
'''

CH_PROJECTIONS = challenge(
    "cppa6-projections",
    "Algorithms with Projections",
    "Implement `topEarner` (max_element with a salary projection) and `sortRoster` (sort by level, ties broken by name — a projection cannot express two keys, so use a comparator) — both without copying the vector.",
    PROJ_BOILER,
    [
        ("topEarner projects on salary",
         r'''std::vector<Employee> staff{{"Ada", 3, 120.0}, {"Lin", 5, 98.5}, {"Zoe", 2, 155.0}};
CHECK_EQ(topEarner(staff), std::string("Zoe"));''',
         "auto it = std::ranges::max_element(staff, {}, &Employee::salary); return it->name; — {} is the default comparator, the projection is the last argument."),
        ("sortRoster orders by level then name",
         r'''std::vector<Employee> roster{{"b", 2, 1.0}, {"a", 2, 1.0}, {"c", 1, 1.0}};
sortRoster(roster);
CHECK_EQ(roster[0].name, std::string("c"));
CHECK_EQ(roster[1].name, std::string("a"));
CHECK_EQ(roster[2].name, std::string("b"));''',
         "std::ranges::sort(staff, [](const Employee& x, const Employee& y) { return x.level != y.level ? x.level < y.level : x.name < y.name; }); — two keys need a comparator, not a projection."),
    ],
    difficulty="advanced",
)

VI_PROJECTIONS = vi_challenge(
    "Thuật toán với projection",
    "Cài `topEarner` (max_element với projection theo salary) và `sortRoster` (sort theo level, hòa thì theo tên — projection không diễn đạt được hai khóa, nên dùng comparator) — cả hai không được copy vector.",
    [
        ("topEarner chiếu theo salary", "auto it = std::ranges::max_element(staff, {}, &Employee::salary); return it->name; — {} là comparator mặc định, projection là đối số cuối."),
        ("sortRoster sắp theo level rồi tên", "std::ranges::sort(staff, [](const Employee& x, const Employee& y) { return x.level != y.level ? x.level < y.level : x.name < y.name; }); — hai khóa cần comparator, không phải projection."),
    ],
)

CH_STRIDE_VIEW = challenge(
    "cppa6-stride-view",
    "A Hand-Written Stride View",
    "Implement `strideView(vec, k)` returning a type with begin()/end() that walks every k-th element (k >= 1). Iterate the returned view in the usual range-for.",
    r'''#include <cstddef>
#include <vector>

// Return a view-like object over every k-th element of data.
// Must support: for (const auto& x : strideView(data, k)) ...
// (Implement your own iterator; std::views::stride is C++23 — do not use it.)
auto strideView(const std::vector<int>& data, std::size_t k);
''',
    [
        ("stride walks every k-th element",
         r'''std::vector<int> data{0, 1, 2, 3, 4, 5, 6};
std::string got;
for (int x : strideView(data, 3)) got += std::to_string(x) + ",";
CHECK_EQ(got, std::string("0,3,6,"));''',
         "Iterator holds pointer-to-vector, index, and k; operator* returns (*v)[i]; operator+= (k) advances; end is index >= size."),
        ("k of 1 is the identity",
         r'''std::vector<int> small{7, 8};
std::string all;
for (int x : strideView(small, 1)) all += std::to_string(x);
CHECK_EQ(all, std::string("78"));''',
         "Stride 1 visits everything — the degenerate case must work."),
        ("empty and short inputs",
         r'''std::vector<int> none;
int seen = 0;
for (int x : strideView(none, 2)) { ++seen; }
CHECK_EQ(seen, 0);''',
         "begin == end immediately when data is empty — no dereference may happen."),
    ],
    difficulty="advanced",
)

VI_STRIDE_VIEW = vi_challenge(
    "Stride view viết tay",
    "Cài `strideView(vec, k)` trả về một kiểu có begin()/end() đi qua mỗi phần tử thứ k (k >= 1). Duyệt view trả về bằng range-for thông thường.",
    [
        ("stride đi qua mỗi phần tử thứ k", "Iterator giữ con trỏ tới vector, chỉ số và k; operator* trả về (*v)[i]; bước nhảy +k; end là index >= size."),
        ("k bằng 1 là định thức", "Stride 1 duyệt hết — trường hợp suy biến phải chạy đúng."),
        ("input rỗng và ngắn", "begin == end ngay khi data rỗng — không được phép dereference."),
    ],
)

M6_PRAC1 = dict(
    sid="m6-pipeline-practice",
    title="Pipelines and Projections",
    description="Compose lazy pipelines and use projections with range algorithms — no intermediate containers allowed.",
    vi_title="Pipeline và projection",
    vi_description="Kết hợp pipeline lười và dùng projection với thuật toán range — cấm container trung gian.",
    after_lesson=L6A,
    minutes=22,
    difficulty="advanced",
)

M6_PRAC1_CH = [CH_PIPELINE_BASICS, CH_PROJECTIONS]
M6_PRAC1_VI = {"cppa6-pipeline-basics": VI_PIPELINE_BASICS,
               "cppa6-projections": VI_PROJECTIONS}

M6_PRAC1_SOL = [
    ("cppa6-pipeline-basics",
     PIPE_BOILER + "\nint sumEvenSquares(int limit) {\n    namespace rv = std::views;\n    int total = 0;\n    for (int v : rv::iota(1, limit) | rv::filter([](int x) { return x % 2 == 0; })\n                                   | rv::transform([](int x) { return x * x; })) {\n        total += v;\n    }\n    return total;\n}\nstd::string initials(const std::vector<std::string>& words, std::size_t n) {\n    namespace rv = std::views;\n    std::string out;\n    for (char c : words | rv::filter([n](const std::string& w) { return w.size() > n; })\n                        | rv::transform([](const std::string& w) { return (char)std::toupper((unsigned char)w[0]); })) {\n        out += c;\n    }\n    return out;\n}\n",
     PIPE_BOILER + "\nint sumEvenSquares(int limit) {\n    int total = 0;\n    for (int x = 1; x < limit; ++x) { if (x % 2 == 1) total += x * x; }  // WRONG: odds, not evens\n    return total;\n}\nstd::string initials(const std::vector<std::string>& words, std::size_t n) {\n    std::string out;\n    for (const auto& w : words) { if ((int)w.size() >= (int)n) out += (char)std::toupper((unsigned char)w[0]); }  // WRONG: >= includes boundary\n    return out;\n}\n"),
    ("cppa6-projections",
     PROJ_BOILER + "\nstd::string topEarner(const std::vector<Employee>& staff) {\n    auto it = std::ranges::max_element(staff, {}, &Employee::salary);\n    return it->name;\n}\nvoid sortRoster(std::vector<Employee>& staff) {\n    std::ranges::sort(staff, [](const Employee& x, const Employee& y) {\n        return x.level != y.level ? x.level < y.level : x.name < y.name;\n    });\n}\n",
     PROJ_BOILER + "\nstd::string topEarner(const std::vector<Employee>& staff) {\n    auto it = std::ranges::max_element(staff, {}, &Employee::level);  // WRONG: projects on level\n    return it->name;\n}\nvoid sortRoster(std::vector<Employee>& staff) {\n    std::ranges::sort(staff, {}, &Employee::level);  // WRONG: ignores the name tiebreak\n}\n"),
]

write_practice(M6, **M6_PRAC1, challenges=M6_PRAC1_CH, vi_challenges=M6_PRAC1_VI, solutions=M6_PRAC1_SOL)

M6_PRAC2 = dict(
    sid="m6-custom-view-practice",
    title="Build a View",
    description="Write your own iterator-backed view — the machinery every library author eventually needs.",
    vi_title="Tự dựng một view",
    vi_description="Tự viết view dựa trên iterator — cơ chế mà mọi tác giả thư viện sớm muộn cũng cần.",
    after_lesson=L6B,
    minutes=20,
    difficulty="advanced",
)

M6_PRAC2_CH = [CH_STRIDE_VIEW]
M6_PRAC2_VI = {"cppa6-stride-view": VI_STRIDE_VIEW}

M6_PRAC2_SOL = [
    ("cppa6-stride-view",
     r'''#include <cstddef>
#include <string>
#include <vector>

namespace detail {
class StrideIterator {
public:
    StrideIterator(const std::vector<int>* v, std::size_t i, std::size_t k)
        : v_(v), i_(i), k_(k) {}
    int operator*() const { return (*v_)[i_]; }
    StrideIterator& operator++() { i_ += k_; return *this; }
    bool operator!=(const StrideIterator& o) const { return i_ != o.i_ && !(i_ >= v_->size()); }
    bool operator==(const StrideIterator& o) const { return !(*this != o); }
private:
    const std::vector<int>* v_;
    std::size_t i_;
    std::size_t k_;
};
}  // namespace detail

class StrideView {
public:
    StrideView(const std::vector<int>& v, std::size_t k) : v_(&v), k_(k) {}
    detail::StrideIterator begin() const { return {v_, 0, k_}; }
    detail::StrideIterator end() const { return {v_, v_->size(), k_}; }
private:
    const std::vector<int>* v_;
    std::size_t k_;
};

auto strideView(const std::vector<int>& data, std::size_t k) { return StrideView(data, k); }
''',
     r'''#include <cstddef>
#include <string>
#include <vector>

namespace detail {
class StrideIterator {
public:
    StrideIterator(const std::vector<int>* v, std::size_t i, std::size_t k)
        : v_(v), i_(i), k_(k) {}
    int operator*() const { return (*v_)[i_]; }
    StrideIterator& operator++() { i_ += 1; return *this; }   // WRONG: ignores k
    bool operator!=(const StrideIterator& o) const { return i_ != o.i_ && !(i_ >= v_->size()); }
    bool operator==(const StrideIterator& o) const { return !(*this != o); }
private:
    const std::vector<int>* v_;
    std::size_t i_;
    std::size_t k_;
};
}  // namespace detail

class StrideView {
public:
    StrideView(const std::vector<int>& v, std::size_t k) : v_(&v), k_(k) {}
    detail::StrideIterator begin() const { return {v_, 0, k_}; }
    detail::StrideIterator end() const { return {v_, v_->size(), k_}; }
private:
    const std::vector<int>* v_;
    std::size_t k_;
};

auto strideView(const std::vector<int>& data, std::size_t k) { return StrideView(data, k); }
'''),
]

write_practice(M6, **M6_PRAC2, challenges=M6_PRAC2_CH, vi_challenges=M6_PRAC2_VI, solutions=M6_PRAC2_SOL)

M6_PRAC3 = dict(
    sid="m6-dangling-practice",
    title="Dangling Spotting Clinic",
    description="Mark which view snippets dangle and repair the dangerous one by materializing.",
    vi_title="Phòng khám nhận diện dangling",
    vi_description="Dán nhãn đoạn view nào dangling và sửa đoạn nguy hiểm bằng cách cụ thể hóa.",
    after_lesson=L6C,
    minutes=14,
    difficulty="advanced",
)

CH_DANGLING_FIX = challenge(
    "cppa6-dangling-fix",
    "Repair the Dangling Pipeline",
    "Implement `firstLetters(std::vector<std::string> words)`: return the uppercase first letters of long words as a **std::string** — computed through a view pipeline over `words`, but returned by value so nothing dangles after the call.",
    r'''#include <cctype>
#include <string>
#include <vector>

// Caller passes a fresh vector each time; your job is to produce a value,
// not a view — so the caller can never hold a dangling pipeline.
std::string firstLetters(std::vector<std::string> words, std::size_t n);
''',
    [
        ("returns a value, not a view",
         r'''std::string out = firstLetters(std::vector<std::string>{"alpha", "be", "gamma"}, 2);
CHECK_EQ(out, std::string("AG"));''',
         "Build the pipeline over the (by-value, caller-owned-copy) words parameter, accumulate into a std::string, return the string — the view dies inside the function, the value survives."),
        ("works through the by-value copy",
         r'''std::vector<std::string> src{"one", "two", "three"};
std::string out = firstLetters(src, 2);
CHECK_EQ(out, std::string("OTT"));  // all three words exceed 2 chars
CHECK_EQ(src.size(), std::size_t{3});''',
         "The parameter is a copy — mutating/adapting it inside is safe; the caller's vector is untouched."),
    ],
    difficulty="advanced",
)

VI_DANGLING_FIX = vi_challenge(
    "Sửa pipeline dangling",
    "Cài `firstLetters(std::vector<std::string> words)`: trả về các chữ cái đầu viết hoa của từ dài dưới dạng **std::string** — tính qua pipeline view trên `words`, nhưng trả theo giá trị để không gì còn dangling sau lời gọi.",
    [
        ("trả về giá trị, không phải view", "Dựng pipeline trên tham số words (truyền giá trị, là bản copy của caller), cộng dồn vào std::string, trả chuỗi — view chết trong hàm, giá trị thì sống."),
        ("chạy qua bản copy truyền giá trị", "Tham số là bản copy — biến đổi bên trong là an toàn; vector của caller không bị động tới."),
    ],
)

M6_PRAC3_CH = [CH_DANGLING_FIX]
M6_PRAC3_VI = {"cppa6-dangling-fix": VI_DANGLING_FIX}

M6_PRAC3_SOL = [
    ("cppa6-dangling-fix",
     r'''#include <cctype>
#include <ranges>
#include <string>
#include <vector>

std::string firstLetters(std::vector<std::string> words, std::size_t n) {
    namespace rv = std::views;
    std::string out;
    for (char c : words | rv::filter([n](const std::string& w) { return w.size() > n; })
                        | rv::transform([](const std::string& w) { return (char)std::toupper((unsigned char)w[0]); })) {
        out += c;
    }
    return out;
}
''',
     r'''#include <cctype>
#include <string>
#include <vector>

#include <ranges>

auto firstLetters(std::vector<std::string> words, std::size_t n) {
    namespace rv = std::views;
    return words | rv::filter([n](const std::string& w) { return w.size() > n; })
                 | rv::transform([](const std::string& w) { return (char)std::toupper((unsigned char)w[0]); });
    // WRONG: returns a view over the parameter — dangles the moment the function returns
}
'''),
]

write_practice(M6, **M6_PRAC3, challenges=M6_PRAC3_CH, vi_challenges=M6_PRAC3_VI, solutions=M6_PRAC3_SOL)

# ---- module 6 checkpoint ----
CP6_MD = r'''
The ranges checkpoint: pipelines with early exit, graded on exact element flow.
'''

CP6_BOILER = r'''#include <ranges>
#include <string>
#include <vector>

// Third even number in [start, end) — or -1 if there are fewer than three.
int thirdEven(int start, int end);

// Last word longer than n characters — or the empty string.
std::string lastLongWord(const std::vector<std::string>& words, std::size_t n);
'''

write_checkpoint(
    M6, L6D,
    "Checkpoint: Ranges",
    "Prove lazy pipelines with early-exit semantics in one graded challenge.",
    15,
    CP6_MD,
    "Checkpoint: Ranges",
    "Chứng minh pipeline lười với ngữ nghĩa thoát sớm trong một thử thách có chấm điểm.",
    r'''
Checkpoint ranges: pipeline lười với ngữ nghĩa thoát sớm trong một thử thách.
''',
    challenge(
        "cppa6-ranges-checkpoint",
        "Pipeline Gauntlet",
        "Implement `thirdEven` and `lastLongWord` with view pipelines. No intermediate containers, no manual index loops.",
        CP6_BOILER,
        [
            ("thirdEven with early exit",
             r'''CHECK_EQ(thirdEven(1, 10), 6);
CHECK_EQ(thirdEven(2, 6), -1);
CHECK_EQ(thirdEven(10, 11), -1);
CHECK_EQ(thirdEven(10, 12), -1);''',
         "rv::iota(start, end) | rv::filter(even) | rv::take(3) — then check whether 3 elements arrived (the take stops the pipeline; an empty result means -1)."),
            ("lastLongWord walks backwards",
             r'''std::vector<std::string> words{"a", "longer", "longest!", "tiny"};
CHECK_EQ(lastLongWord(words, 4), std::string("longest!"));
CHECK_EQ(lastLongWord(words, 100), std::string(""));''',
         "words | rv::filter(...) | rv::reverse | rv::take(1) — first element of the reversed filtered range, or \"\" when none."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại pipeline",
        "Cài `thirdEven` và `lastLongWord` bằng view pipeline. Cấm container trung gian, cấm vòng lặp chỉ số thủ công.",
        [
            ("thirdEven thoát sớm", "rv::iota(start, end) | rv::filter(even) | rv::take(3) — rồi kiểm tra có đủ 3 phần tử không (take dừng pipeline; kết quả rỗng nghĩa là -1)."),
            ("lastLongWord đi ngược", "words | rv::filter(...) | rv::reverse | rv::take(1) — phần tử đầu của dải đã lọc đảo ngược, hoặc \"\" khi không có."),
        ],
    ),
    solution=CP6_BOILER + "\nint thirdEven(int start, int end) {\n    namespace rv = std::views;\n    int count = 0, last = -1;\n    for (int v : rv::iota(start, end) | rv::filter([](int x) { return x % 2 == 0; }) | rv::take(3)) {\n        ++count;\n        last = v;\n    }\n    return count == 3 ? last : -1;\n}\nstd::string lastLongWord(const std::vector<std::string>& words, std::size_t n) {\n    namespace rv = std::views;\n    std::string out;\n    for (const auto& w : words | rv::filter([n](const std::string& s) { return s.size() > n; }) | rv::reverse | rv::take(1)) {\n        out = w;\n    }\n    return out;\n}\n",
    wrong=CP6_BOILER + "\nint thirdEven(int start, int end) {\n    namespace rv = std::views;\n    int count = 0, last = -1;\n    for (int v : rv::iota(start, end) | rv::filter([](int x) { return x % 2 == 0; }) | rv::take(2)) {  // WRONG: take(2)\n        ++count;\n        last = v;\n    }\n    return count == 3 ? last : -1;\n}\nstd::string lastLongWord(const std::vector<std::string>& words, std::size_t n) {\n    namespace rv = std::views;\n    std::string out;\n    for (const auto& w : words | rv::filter([n](const std::string& s) { return s.size() > n; }) | rv::take(1)) {  // WRONG: no reverse\n        out = w;\n    }\n    return out;\n}\n",
)

print("modules 5-6 done")
