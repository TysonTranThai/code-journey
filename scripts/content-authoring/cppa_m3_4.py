#!/usr/bin/env python3
"""C++ Advanced — module 3 (templates-deep) and module 4 (concepts)."""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 3: templates-deep ============================
M3 = "templates-deep"

L3A = "cppa3-specialization"
L3B = "variadics-folds"
L3C = "if-constexpr-nttp"
L3D = "ctad-deduction"
L3E = "cppa-checkpoint-generic"

write_module(
    M3,
    "Advanced Templates",
    "Specialization, variadics, fold expressions, if constexpr, NTTPs, and CTAD — the techniques behind every serious generic library, each aimed at a real problem.",
    "Template Nâng Cao",
    "Specialization, variadics, fold expressions, if constexpr, NTTP và CTAD — kỹ thuật đằng sau mọi thư viện generic nghiêm túc, mỗi cái giải một bài toán thật.",
    [L3A, L3B, L3C, L3D, L3E],
    ["m3-specialize-practice", "m3-variadic-practice", "m3-constexpr-branch-practice", "m3-ctad-practice"],
)

write_lesson(
    M3, L3A,
    "Specialization: Full, Partial, and Variable Templates",
    "Give specific types exactly the implementation they deserve — the mechanism under std::hash, std::less, and every optimized fast path.",
    12,
    r'''
A primary template states the general algorithm; a **specialization** replaces it for specific arguments. The library uses this everywhere: `std::hash<std::string>` is a specialization of `std::hash<T>`.

## Full specialization

One concrete argument list, `template <>`:

```cpp
template <class T> struct Serializer {
    static std::string dump(const T&) { return "generic"; }
};
template <> struct Serializer<bool> {
    static std::string dump(const bool& b) { return b ? "true" : "false"; }
};
```

## Partial specialization

Still templated, but constrained — a *pattern*, not a point:

```cpp
template <class T> struct Serializer<std::vector<T>> {
    static std::string dump(const std::vector<T>& v);
};
```

The compiler picks the **most specialized** match. This is how `Capacity<std::array<T, N>>` can read `N` out of the type.

## Variable templates

A compile-time value parameterized by type:

```cpp
template <class T> inline constexpr bool is_small_v = sizeof(T) <= 8;
```

Pairs naturally with specialization: give `Rank<T>` per-type values, expose `rank_v<T>`.

**Design rule:** specialize for *behavior the type cannot express with its own members* (external traits). If the behavior belongs inside the type, write a member instead.
''',
    "Specialization: Đầy Đủ, Một Phần và Variable Template",
    "Trao cho từng kiểu cụ thể đúng phần cài đặt nó xứng đáng — cơ chế đứng sau std::hash, std::less và mọi fast path được tối ưu.",
    r'''
Template chính khai báo thuật toán tổng quát; **specialization** thay thế nó cho các đối số cụ thể. Thư viện chuẩn dùng điều này khắp nơi: `std::hash<std::string>` là một specialization của `std::hash<T>`.

## Full specialization

Một danh sách đối số cụ thể, với `template <>`:

```cpp
template <class T> struct Serializer {
    static std::string dump(const T&) { return "generic"; }
};
template <> struct Serializer<bool> {
    static std::string dump(const bool& b) { return b ? "true" : "false"; }
};
```

## Partial specialization

Vẫn còn template nhưng bị ràng buộc — một *mẫu hình*, không phải một điểm:

```cpp
template <class T> struct Serializer<std::vector<T>> {
    static std::string dump(const std::vector<T>& v);
};
```

Compiler chọn mẫu hình **chuyên biệt nhất**. Nhờ vậy `Capacity<std::array<T, N>>` đọc được `N` từ chính kiểu.

## Variable template

Một giá trị compile-time được tham số hóa theo kiểu:

```cpp
template <class T> inline constexpr bool is_small_v = sizeof(T) <= 8;
```

Kết hợp tự nhiên với specialization: cấp giá trị cho `Rank<T>` theo từng kiểu, phơi ra qua `rank_v<T>`.

**Nguyên tắc thiết kế:** chỉ specialize cho *hành vi kiểu đó không tự diễn đạt được bằng thành viên của nó* (trait bên ngoài). Nếu hành vi thuộc về bên trong kiểu, hãy viết thành viên.
''',
    difficulty="advanced",
)

write_lesson(
    M3, L3B,
    "Variadic Templates and Fold Expressions",
    "Parameter packs, pack expansion, and the folds that replaced recursive boilerplate — write sum, min, and counting utilities in one line.",
    11,
    r'''
## Parameter packs

`template <class... A> void f(A... args);` captures *any number* of arguments of *any* types. `sizeof...(args)` is the count. Expansion `args...` unfolds the pack at each use site.

## Unary folds — the one-line algorithms

A **fold expression** applies an operator across a pack:

```cpp
template <class... A> constexpr auto sum(A... a)     { return (a + ... + 0); }  // binary right fold, 0 = empty-pack value
template <class... A> constexpr auto product(A... a) { return (a * ... * 1); }
template <class... A> constexpr int truthy(A... a)   { return (0 + ... + (a ? 1 : 0)); }
```

Forms: `(pack op ...)` (unary right), `(... op pack)` (unary left), `(pack op ... op init)` (binary). The **binary** forms matter: they define the result for an **empty pack** — without one, `sum()` is ill-formed, which is exactly the bug your tests should catch.

## if constexpr — compile-time branching

Inside the fold body you can branch on each element's type:

```cpp
template <class... A> std::string describe(A... a);
// per element: if constexpr (std::is_integral_v<decltype(v)>) ... else ...
```

The discarded branch is not even compiled — which is what makes "serialize this only if it has that member" clean without SFINAE.
''',
    "Variadic Template và Fold Expression",
    "Parameter pack, pack expansion và các fold thay thế boilerplate đệ quy — viết sum, min và tiện ích đếm trong một dòng.",
    r'''
## Parameter pack

`template <class... A> void f(A... args);` giữ *số lượng bất kỳ* đối số với *kiểu bất kỳ*. `sizeof...(args)` là số phần tử. Phép mở rộng `args...` triển khai pack tại mỗi nơi dùng.

## Unary fold — thuật toán một dòng

**Fold expression** áp một toán tử trên toàn bộ pack:

```cpp
template <class... A> constexpr auto sum(A... a)     { return (a + ... + 0); }  // binary right fold, 0 = giá trị khi pack rỗng
template <class... A> constexpr auto product(A... a) { return (a * ... * 1); }
template <class... A> constexpr int truthy(A... a)   { return (0 + ... + (a ? 1 : 0)); }
```

Các dạng: `(pack op ...)` (unary phải), `(... op pack)` (unary trái), `(pack op ... op init)` (binary). Dạng **binary** quan trọng: nó định nghĩa kết quả khi **pack rỗng** — thiếu nó, `sum()` là ill-formed, đúng cái lỗi mà bài kiểm tra của bạn phải bắt được.

## if constexpr — rẽ nhánh lúc biên dịch

Trong thân fold, bạn có thể rẽ nhánh theo kiểu của từng phần tử:

```cpp
template <class... A> std::string describe(A... a);
// từng phần tử: if constexpr (std::is_integral_v<decltype(v)>) ... else ...
```

Nhánh bị loại bỏ thậm chí không được biên dịch — nhờ vậy "chỉ serialize khi có member đó" trở nên sạch sẽ mà không cần SFINAE.
''',
    difficulty="advanced",
)

write_lesson(
    M3, L3C,
    "if constexpr, NTTPs, and Compile-Time Data",
    "Non-type template parameters turn sizes and array lengths into types. Combined with if constexpr, they carry whole tables into compile time.",
    11,
    r'''
## Non-type template parameters (NTTPs)

Template parameters can be *values*: sizes, enumerations, pointers — anything constant-expression-able. The most common: `std::size_t`:

```cpp
template <std::size_t N> struct Ring {
    int data_[N]{};
    std::size_t head_ = 0;
    void push(int v) { data_[head_++ % N] = v; }
    static constexpr std::size_t capacity() { return N; }
};
```

Every `Ring<8>` and `Ring<1024>` is a distinct type with zero heap allocations and a compile-time-known capacity.

## Array-bound NTTP — free string lengths

Deducing `N` from an array reference gives you the literal's length for free: `template <std::size_t N> constexpr std::size_t strLen(const char (&s)[N]) { return N - 1; }` — `strLen("abcd")` is 4, computed at compile time, no `strlen`.

## Partial specialization over NTTPs

The two compose: `Capacity<std::array<T, N>>` peels the size out of the *type* — the standard library's own `tuple_size` works this way.

**Watch out:** each distinct `N` instantiates a distinct type. A `Ring<8>` is not a `Ring<9>`; if you need runtime-variable capacity, that is a `std::vector` job, not an NTTP job.
''',
    "if constexpr, NTTP và Dữ Liệu Compile-Time",
    "Non-type template parameter biến kích thước và độ dài mảng thành kiểu. Kết hợp với if constexpr, chúng mang cả bảng dữ liệu vào compile time.",
    r'''
## Non-type template parameter (NTTP)

Tham số template có thể là *giá trị*: kích thước, enum, con trỏ — bất cứ thứ gì tính được ở constant expression. Phổ biến nhất: `std::size_t`:

```cpp
template <std::size_t N> struct Ring {
    int data_[N]{};
    std::size_t head_ = 0;
    void push(int v) { data_[head_++ % N] = v; }
    static constexpr std::size_t capacity() { return N; }
};
```

Mỗi `Ring<8>` và `Ring<1024>` là một kiểu riêng, không cấp phát heap nào, capacity biết trước lúc biên dịch.

## NTTP là cỡ mảng — độ dài chuỗi miễn phí

Suy diễn `N` từ tham chiếu mảng cho bạn độ dài literal không tốn công: `template <std::size_t N> constexpr std::size_t strLen(const char (&s)[N]) { return N - 1; }` — `strLen("abcd")` là 4, tính lúc biên dịch, không cần `strlen`.

## Partial specialization trên NTTP

Hai kỹ thuật kết hợp với nhau: `Capacity<std::array<T, N>>` tách kích thước ra khỏi *kiểu* — `tuple_size` của thư viện chuẩn cũng hoạt động theo cách này.

**Lưu ý:** mỗi giá trị `N` khởi tạo một kiểu riêng. `Ring<8>` không phải `Ring<9>`; nếu cần capacity thay đổi lúc chạy, đó là việc của `std::vector`, không phải của NTTP.
''',
    difficulty="advanced",
)

write_lesson(
    M3, L3D,
    "CTAD and Deduction Guides",
    "C++17 let the compiler infer template arguments from constructors; C++20 extended it to aliases. Deduction guides are how libraries steer that inference.",
    10,
    r'''
## Class template argument deduction (CTAD)

`std::pair p(1, 2.0);` — no `<int, double>` needed; the constructor's parameters drive deduction. Without CTAD you would write `std::pair<int, double> p(1, 2.0);`.

## Where inference goes wrong: iterator pairs

A constructor `template <class It> Box(It first, It last) : items(first, last) {}` would deduce `Box<int*>` from `Box b(begin(arr), end(arr));` — the *iterator* type, not the *element* type. **Deduction guides** fix the inference without touching the class:

```cpp
template <class It>
Box(It first, It last) -> Box<std::iter_value_t<It>>;
```

The guide says: "when you see this constructor signature, deduce from the *value type* instead." The standard library ships dozens: `std::vector v(begin, end)` deduces the element type this way.

## C++20: alias CTAD

`template <class T> using VecOf = std::vector<T>;` — then `VecOf v{1, 2, 3};` deduces `std::vector<int>`. Aliases became first-class deduction citizens in C++20.

**Review skill:** when a container type comes out "wrong" from a constructor call, suspect the missing guide before suspecting your code.
''',
    "CTAD và Deduction Guide",
    "C++17 cho compiler tự suy luận tham số template từ constructor; C++20 mở rộng sang alias. Deduction guide là cách thư viện dẫn hướng phép suy luận đó.",
    r'''
## Class template argument deduction (CTAD)

`std::pair p(1, 2.0);` — không cần `<int, double>`; tham số của constructor dẫn phép suy diễn. Không có CTAD bạn phải viết `std::pair<int, double> p(1, 2.0);`.

## Chỗ suy luận hay sai: cặp iterator

Constructor `template <class It> Box(It first, It last) : items(first, last) {}` sẽ suy ra `Box<int*>` từ `Box b(begin(arr), end(arr));` — kiểu *iterator*, không phải kiểu *phần tử*. **Deduction guide** sửa phép suy luận mà không đụng vào lớp:

```cpp
template <class It>
Box(It first, It last) -> Box<std::iter_value_t<It>>;
```

Guide nói rằng: "gặp chữ ký constructor này thì suy từ *kiểu giá trị* thay vì kiểu iterator." Thư viện chuẩn có hàng chục guide như vậy: `std::vector v(begin, end)` suy được kiểu phần tử theo đúng cách này.

## C++20: alias CTAD

`template <class T> using VecOf = std::vector<T>;` — sau đó `VecOf v{1, 2, 3};` suy ra `std::vector<int>`. Từ C++20, alias trở thành công dân đầy đủ của cơ chế suy luận.

**Kỹ năng review:** khi kiểu container trả về "sai" sau một lời gọi constructor, hãy nghi ngờ thiếu guide trước khi nghi ngờ code của bạn.
''',
    difficulty="advanced",
)

# ---- module 3 practices ----
V3_BOILER = r'''#include <cstddef>
#include <string>

// Primary template: naive fixed array.
template <class T>
struct Vector3 {
    T x{}, y{}, z{};
    static constexpr const char* storage = "naive";
};

// TODO: full-specialize Vector3<bool> as a bit-packed version:
//   unsigned bits_ = 0;  set(i, v) sets bit i (0..2);  get(i) reads it;
//   storage = "bit-packed"
'''

CH_SPECIALIZE_V3 = challenge(
    "cppa3-specialize-vector3",
    "Specialize Vector3<bool> as Bit-Packed",
    "The generic `Vector3<T>` wastes a byte per bool. Write a **full specialization** `Vector3<bool>` that packs the three flags into one `unsigned` and reports `storage = \"bit-packed\"`.",
    V3_BOILER,
    [
        ("specialization reports bit-packed storage",
         r'''CHECK_EQ(std::string(Vector3<bool>::storage), std::string("bit-packed"));
CHECK_EQ(std::string(Vector3<int>::storage), std::string("naive"));''',
         "template <> struct Vector3<bool> { ... static constexpr const char* storage = \"bit-packed\"; };"),
        ("bits round-trip independently",
         r'''Vector3<bool> v;
v.set(0, true);
v.set(2, true);
CHECK_EQ(v.get(0), true);
CHECK_EQ(v.get(1), false);
CHECK_EQ(v.get(2), true);
v.set(2, false);
CHECK_EQ(v.get(2), false);
CHECK_EQ(v.get(0), true);''',
         "set: bits_ |= (1u << i) when true, bits_ &= ~(1u << i) when false; get: (bits_ >> i) & 1u."),
    ],
    difficulty="advanced",
)

VI_SPECIALIZE_V3 = vi_challenge(
    "Specialize Vector3<bool> đóng gói bằng bit",
    "`Vector3<T>` tổng quát lãng phí một byte cho mỗi bool. Hãy viết **full specialization** `Vector3<bool>` gói ba cờ vào một biến `unsigned` và báo `storage = \"bit-packed\"`.",
    [
        ("specialization báo bit-packed", "template <> struct Vector3<bool> { ... static constexpr const char* storage = \"bit-packed\"; };"),
        ("bit round-trip độc lập", "set: bits_ |= (1u << i) khi true, bits_ &= ~(1u << i) khi false; get: (bits_ >> i) & 1u."),
    ],
)

RANK_BOILER = r'''#include <array>
#include <cstddef>
#include <vector>

// Rank: 0 for unknown types, higher for known ones.
template <class T> struct Rank {
    static constexpr int value = 0;
};
// TODO: specialize Rank<int> -> 2 and Rank<long> -> 3.
// Expose rank_v<T> as a variable template reading Rank<T>::value.

// Capacity: 0 for dynamic containers, N for std::array<T, N>.
template <class C> struct Capacity;   // primary: undefined on purpose
// TODO: partial specialization for std::vector<T> -> 0,
//       partial specialization for std::array<T, N> -> N.
'''

CH_SPECIALIZE_TRAITS = challenge(
    "cppa3-specialize-traits",
    "Rank and Capacity via Specialization",
    "Implement the `Rank` specializations (int -> 2, long -> 3), the `rank_v` variable template, and both `Capacity` partial specializations (`std::vector<T>` -> 0, `std::array<T, N>` -> N).",
    RANK_BOILER,
    [
        ("rank_v reads through specializations",
         r'''static_assert(rank_v<int> == 2, "int rank");
static_assert(rank_v<long> == 3, "long rank");
static_assert(rank_v<double> == 0, "unknown rank");''',
         "template <> struct Rank<int> { static constexpr int value = 2; }; (same for long), then template <class T> inline constexpr int rank_v = Rank<T>::value;"),
        ("Capacity peels N from std::array",
         r'''static_assert(Capacity<std::array<int, 7>>::value == 7, "array N");
static_assert(Capacity<std::vector<int>>::value == 0, "dynamic");''',
         "template <class T, std::size_t N> struct Capacity<std::array<T, N>> { static constexpr std::size_t value = N; }; and a vector<T> one returning 0."),
    ],
    difficulty="advanced",
)

VI_SPECIALIZE_TRAITS = vi_challenge(
    "Rank và Capacity qua specialization",
    "Cài các specialization của `Rank` (int -> 2, long -> 3), variable template `rank_v`, và cả hai partial specialization của `Capacity` (`std::vector<T>` -> 0, `std::array<T, N>` -> N).",
    [
        ("rank_v đọc qua specialization", "template <> struct Rank<int> { static constexpr int value = 2; }; (tương tự cho long), rồi template <class T> inline constexpr int rank_v = Rank<T>::value;"),
        ("Capacity tách N từ std::array", "template <class T, std::size_t N> struct Capacity<std::array<T, N>> { static constexpr std::size_t value = N; }; và một bản vector<T> trả về 0."),
    ],
)

M3_PRAC1 = dict(
    sid="m3-specialize-practice",
    title="Specialization Workshop",
    description="Full specialization for a bit-packed Vector3<bool>, plus partial specializations that read sizes out of types.",
    vi_title="Xưởng specialization",
    vi_description="Full specialization cho Vector3<bool> đóng gói bằng bit, cộng các partial specialization đọc kích thước từ kiểu.",
    after_lesson=L3A,
    minutes=22,
    difficulty="advanced",
)

M3_PRAC1_CH = [CH_SPECIALIZE_V3, CH_SPECIALIZE_TRAITS]
M3_PRAC1_VI = {"cppa3-specialize-vector3": VI_SPECIALIZE_V3,
               "cppa3-specialize-traits": VI_SPECIALIZE_TRAITS}

M3_PRAC1_SOL = [
    ("cppa3-specialize-vector3",
     V3_BOILER + "\ntemplate <>\nstruct Vector3<bool> {\n    unsigned bits_ = 0;\n    void set(int i, bool v) { if (v) bits_ |= (1u << i); else bits_ &= ~(1u << i); }\n    bool get(int i) const { return ((bits_ >> i) & 1u) != 0; }\n    static constexpr const char* storage = \"bit-packed\";\n};\n",
     V3_BOILER + "\ntemplate <>\nstruct Vector3<bool> {\n    unsigned bits_ = 0;\n    void set(int i, bool v) { if (v) bits_ |= (1u << 0); else bits_ &= ~(1u << 0); }  // WRONG: ignores i\n    bool get(int i) const { return ((bits_ >> i) & 1u) != 0; }\n    static constexpr const char* storage = \"bit-packed\";\n};\n"),
    ("cppa3-specialize-traits",
     RANK_BOILER + "\ntemplate <> struct Rank<int> { static constexpr int value = 2; };\ntemplate <> struct Rank<long> { static constexpr int value = 3; };\ntemplate <class T> inline constexpr int rank_v = Rank<T>::value;\ntemplate <class T> struct Capacity<std::vector<T>> { static constexpr std::size_t value = 0; };\ntemplate <class T, std::size_t N> struct Capacity<std::array<T, N>> { static constexpr std::size_t value = N; };\n",
     RANK_BOILER + "\ntemplate <> struct Rank<int> { static constexpr int value = 1; };   // WRONG: wrong rank\ntemplate <> struct Rank<long> { static constexpr int value = 3; };\ntemplate <class T> inline constexpr int rank_v = Rank<T>::value;\ntemplate <class T> struct Capacity<std::vector<T>> { static constexpr std::size_t value = 0; };\ntemplate <class T, std::size_t N> struct Capacity<std::array<T, N>> { static constexpr std::size_t value = N - 1; };  // WRONG: off by one\n"),
]

write_practice(M3, **M3_PRAC1, challenges=M3_PRAC1_CH, vi_challenges=M3_PRAC1_VI, solutions=M3_PRAC1_SOL)

# ---- variadic practice ----
CH_FOLD_SUM = challenge(
    "cppa3-fold-sum",
    "Folds That Survive Empty Packs",
    "Implement `sumAll` and `sumSquares` as one-line folds. The empty-pack calls in the tests are the graded trap: a unary fold over an empty pack is ill-formed — use a binary fold.",
    r'''#include <cstddef>

template <class... A>
constexpr auto sumAll(A... a);        // (a + ... + 0) shape

template <class... A>
constexpr auto sumSquares(A... a);    // sum of a*a, empty pack -> 0
''',
    [
        ("sumAll basic and empty",
         r'''static_assert(sumAll(1, 2, 3) == 6, "sum");
static_assert(sumAll() == 0, "empty pack sum must be 0");
CHECK_EQ(sumAll(10, -3), 7);''',
         "(a + ... + 0) — the binary fold defines the empty-pack result."),
        ("sumSquares basic and empty",
         r'''static_assert(sumSquares(1, 2, 3) == 14, "squares");
static_assert(sumSquares() == 0, "empty pack squares");
CHECK_EQ(sumSquares(5), 25);''',
         "(0 + ... + (a * a)) — fold the square of each element into an accumulator."),
    ],
    difficulty="advanced",
)

VI_FOLD_SUM = vi_challenge(
    "Fold sống sót qua pack rỗng",
    "Cài `sumAll` và `sumSquares` bằng fold một dòng. Các lời gọi pack rỗng trong bài kiểm tra chính là cái bẫy: unary fold trên pack rỗng là ill-formed — hãy dùng binary fold.",
    [
        ("sumAll cơ bản và rỗng", "(a + ... + 0) — binary fold định nghĩa kết quả cho pack rỗng."),
        ("sumSquares cơ bản và rỗng", "(0 + ... + (a * a)) — fold bình phương từng phần tử vào một accumulator."),
    ],
)

CH_VARIADIC_MIN = challenge(
    "cppa3-variadic-min",
    "minOf over a Pack",
    "Implement `minOf(first, rest...)` — at least one argument, returns the smallest. Uses pack expansion (a fold with std::min works), and must also handle the single-argument call.",
    r'''#include <algorithm>

template <class T, class... Rest>
T minOf(T first, Rest... rest);   // min of all arguments
''',
    [
        ("multi-argument minimum",
         r'''CHECK_EQ(minOf(3, 1, 2), 1);
CHECK_EQ(minOf(2.5, 1.5, 9.0), 1.5);''',
         "Assign as you fold: T m = first; ((m = std::min(m, rest)), ...); return m; — a bare (std::min(first, rest), ...) fold DISCARDS every comparison."),
        ("single argument",
         r'''CHECK_EQ(minOf(5), 5);
CHECK_EQ(minOf(std::size_t{9}), std::size_t{9});''',
         "With an empty rest pack, the result is just `first` — the fold over zero elements must not run."),
    ],
    difficulty="advanced",
)

VI_VARIADIC_MIN = vi_challenge(
    "minOf trên một pack",
    "Cài `minOf(first, rest...)` — ít nhất một đối số, trả về phần tử nhỏ nhất. Dùng pack expansion (fold với std::min cũng được), và phải xử lý cả lời gọi một đối số.",
    [
        ("minimum nhiều đối số", "Fold kiểu (std::min(a, rest) ...), hoặc thu gọn đệ quy/vòng lặp trên pack."),
        ("một đối số", "Với rest rỗng, kết quả chỉ là `first` — fold trên không phần tử không được chạy."),
    ],
)

CH_COUNT_TRUE = challenge(
    "cppa3-count-zeros",
    "Count with a Fold",
    "Implement `countTrue(args...)` returning how many of its boolean-convertible arguments are true, and `hasNone(args...)` returning whether all are false. Both must survive an empty pack.",
    r'''#include <cstddef>

template <class... A>
constexpr int countTrue(A... a);   // count of true-ish elements

template <class... A>
constexpr bool hasNone(A... a);    // true iff every element is false (incl. empty)
''',
    [
        ("countTrue counts correctly",
         r'''static_assert(countTrue(true, false, true) == 2, "count");
static_assert(countTrue() == 0, "empty count");
CHECK_EQ(countTrue(false, false), 0);''',
         "(0 + ... + (a ? 1 : 0)) — add 1 per true element."),
        ("hasNone including empty pack",
         r'''static_assert(hasNone(false, false), "all false");
static_assert(hasNone(), "empty is vacuously none");
static_assert(!hasNone(false, true), "one true breaks it");''',
         "(0 + ... + (a ? 1 : 0)) == 0 — reuse the count; the empty pack folds to 0 == 0, true."),
    ],
    difficulty="advanced",
)

VI_COUNT_TRUE = vi_challenge(
    "Đếm bằng fold",
    "Cài `countTrue(args...)` trả về số đối số chuyển được sang true, và `hasNone(args...)` trả về việc tất cả đều false. Cả hai phải sống sót qua pack rỗng.",
    [
        ("countTrue đếm đúng", "(0 + ... + (a ? 1 : 0)) — cộng 1 cho mỗi phần tử true."),
        ("hasNone gồm cả pack rỗng", "(0 + ... + (a ? 1 : 0)) == 0 — tái dùng count; pack rỗng fold về 0 == 0, đúng."),
    ],
)

M3_PRAC2 = dict(
    sid="m3-variadic-practice",
    title="Packs and Folds",
    description="Sum, min, and counting utilities in one-liners — with empty-pack correctness graded.",
    vi_title="Pack và fold",
    vi_description="Các tiện ích sum, min và đếm trong một dòng — chấm điểm cả tính đúng với pack rỗng.",
    after_lesson=L3B,
    minutes=20,
    difficulty="advanced",
)

M3_PRAC2_CH = [CH_FOLD_SUM, CH_VARIADIC_MIN, CH_COUNT_TRUE]
M3_PRAC2_VI = {"cppa3-fold-sum": VI_FOLD_SUM,
               "cppa3-variadic-min": VI_VARIADIC_MIN,
               "cppa3-count-zeros": VI_COUNT_TRUE}

M3_PRAC2_SOL = [
    ("cppa3-fold-sum",
     r'''#include <cstddef>

template <class... A>
constexpr auto sumAll(A... a) { return (a + ... + 0); }

template <class... A>
constexpr auto sumSquares(A... a) { return (0 + ... + (a * a)); }
''',
     r'''#include <cstddef>

template <class... A>
constexpr auto sumAll(A... a) { return (a * ... * 1); }     // WRONG: product, not sum

template <class... A>
constexpr auto sumSquares(A... a) { return (a * ... * 1); } // WRONG: product, not squares
'''),
    ("cppa3-variadic-min",
     r'''#include <algorithm>

template <class T, class... Rest>
T minOf(T first, Rest... rest) { T m = first; ((m = std::min(m, rest)), ...); return m; }
''',
     r'''#include <algorithm>

template <class T, class... Rest>
T minOf(T first, Rest... rest) { return first; }  // WRONG: ignores rest
'''),
    ("cppa3-count-zeros",
     r'''#include <cstddef>

template <class... A>
constexpr int countTrue(A... a) { return (0 + ... + (a ? 1 : 0)); }

template <class... A>
constexpr bool hasNone(A... a) { return countTrue(a...) == 0; }
''',
     r'''#include <cstddef>

template <class... A>
constexpr int countTrue(A... a) { return (0 + ... + (a ? 0 : 1)); }  // WRONG: counts falses

template <class... A>
constexpr bool hasNone(A... a) { return countTrue(a...) == 0; }
'''),
]

write_practice(M3, **M3_PRAC2, challenges=M3_PRAC2_CH, vi_challenges=M3_PRAC2_VI, solutions=M3_PRAC2_SOL)

# ---- if constexpr / NTTP practice ----
PRINT_BOILER = r'''#include <cstddef>
#include <string>
#include <type_traits>

template <class... A>
std::string describe(A... a);
// One token per argument, space-separated:
//   integral  -> int(5)
//   floating  -> dbl(2.500000)
//   string    -> str(text)
// describe(1, 2.5, std::string("x")) == "int(1) dbl(2.500000) str(x)"
'''

CH_UNIFORM_PRINT = challenge(
    "cppa3-uniform-print",
    "describe(...) with if constexpr",
    "Implement `describe(args...)`: fold over the pack, and use `if constexpr` on each element's type to pick its prefix — `int(...)`, `dbl(...)` (via `std::to_string`), or `str(...)` for anything else. Elements join with single spaces.",
    PRINT_BOILER,
    [
        ("mixed pack described",
         r'''CHECK_EQ(describe(1, 2.5, std::string("x")), std::string("int(1) dbl(2.500000) str(x)"));''',
         "Inside the fold: using U = std::decay_t<decltype(v)>; then if constexpr (std::is_integral_v<U>) -> int(...), else if constexpr (std::is_floating_point_v<U>) -> dbl(...), else str(std::string(v)...). Traits are false for references — decay first!"),
        ("single elements",
         r'''CHECK_EQ(describe(7), std::string("int(7)"));
CHECK_EQ(describe(0.5), std::string("dbl(0.500000)"));
CHECK_EQ(describe(std::string("hi")), std::string("str(hi)"));''',
         "The else-if chain must classify each type exactly once — no trailing space after the last element."),
    ],
    difficulty="advanced",
)

VI_UNIFORM_PRINT = vi_challenge(
    "describe(...) với if constexpr",
    "Cài `describe(args...)`: fold trên pack, và dùng `if constexpr` theo kiểu của từng phần tử để chọn tiền tố — `int(...)`, `dbl(...)` (qua `std::to_string`), hoặc `str(...)` cho phần còn lại. Các phần tử cách nhau một dấu cách.",
    [
        ("pack hỗn hợp được mô tả", "Trong fold: if constexpr (std::is_integral_v<decltype(v)>) -> int( + to_string(v) + ), else if constexpr floating -> dbl(...), còn lại str(...) — dùng string(v) để nhúng std::string."),
        ("từng phần tử đơn", "Chuỗi else-if phải phân loại từng kiểu đúng một lần — không có dấu cách thừa sau phần tử cuối."),
    ],
)

RING_BOILER = r'''#include <cstddef>

template <std::size_t N>
struct Ring {
    int data_[N]{};
    std::size_t head_ = 0;
    // TODO: push writes at head_ % N then advances; capacity() returns N.
    void push(int v);
    int at(std::size_t i) const { return data_[i % N]; }
    static constexpr std::size_t capacity();
};
'''

CH_NTPP_BUFFER = challenge(
    "cppa3-nttp-buffer",
    "A Fixed Ring from an NTTP",
    "Finish `Ring<N>`: `push` writes at `head_ % N` and advances `head_` (wrapping is the point), `capacity()` returns `N`. The test wraps around the buffer edge to prove it.",
    RING_BOILER,
    [
        ("capacity is the NTTP",
         r'''static_assert(Ring<4>::capacity() == 4, "N from the type");
static_assert(Ring<64>::capacity() == 64, "N from the type");''',
         "static constexpr std::size_t capacity() { return N; } — N is part of the type."),
        ("push wraps at the edge",
         r'''Ring<3> r;
r.push(1); r.push(2); r.push(3); r.push(4);
CHECK_EQ(r.at(0), 4);
CHECK_EQ(r.at(1), 2);
CHECK_EQ(r.at(2), 3);''',
         "void push(int v) { data_[head_ % N] = v; ++head_; } — the 4th push overwrites slot 0."),
    ],
    difficulty="advanced",
)

VI_NTPP_BUFFER = vi_challenge(
    "Ring cố định từ NTTP",
    "Hoàn thiện `Ring<N>`: `push` ghi tại `head_ % N` rồi tăng `head_` (việc quấn vòng mới là ý chính), `capacity()` trả về `N`. Bài kiểm tra quấn qua mép buffer để chứng minh.",
    [
        ("capacity lấy từ NTTP", "static constexpr std::size_t capacity() { return N; } — N là một phần của kiểu."),
        ("push quấn tại mép", "void push(int v) { data_[head_ % N] = v; ++head_; } — lần push thứ 4 ghi đè slot 0."),
    ],
)

STRLEN_BOILER = r'''#include <cstddef>

// strLen("abcd") must be 4: the array bound carries the length.
template <std::size_t N>
constexpr std::size_t strLen(const char (&s)[N]);

// firstChar picks s[0] the same way (used by the graded checks).
template <std::size_t N>
constexpr char firstChar(const char (&s)[N]);
'''

CH_ARRAY_BOUND = challenge(
    "cppa3-array-bound-nttp",
    "The Array Bound Is a Free NTTP",
    "Implement `strLen` (N - 1, excluding the terminator) and `firstChar` (s[0]) deducing the size from the array reference — both `constexpr`, usable in `static_assert`.",
    STRLEN_BOILER,
    [
        ("strLen excludes the terminator",
         r'''static_assert(strLen("abcd") == 4, "length");
static_assert(strLen("") == 0, "empty literal");
CHECK_EQ(strLen("template"), std::size_t{8});''',
         "return N - 1; — the bound counts the '\\0'."),
        ("firstChar reads through the same NTTP",
         r'''static_assert(firstChar("knot") == 'k', "first");
CHECK_EQ(firstChar("zebra"), 'z');''',
         "return s[0]; — same deduction shape, different body."),
    ],
    difficulty="advanced",
)

VI_ARRAY_BOUND = vi_challenge(
    "Cỡ mảng là NTTP miễn phí",
    "Cài `strLen` (N - 1, không tính ký tự kết thúc) và `firstChar` (s[0]) suy kích thước từ tham chiếu mảng — cả hai `constexpr`, dùng được trong `static_assert`.",
    [
        ("strLen loại ký tự kết thúc", "return N - 1; — cỡ mảng đã tính cả '\\0'."),
        ("firstChar dùng cùng NTTP", "return s[0]; — cùng hình suy luận, khác phần thân."),
    ],
)

M3_PRAC3 = dict(
    sid="m3-constexpr-branch-practice",
    title="if constexpr and NTTPs",
    description="Type-branched formatting, a fixed ring buffer, and the array-bound NTTP trick.",
    vi_title="if constexpr và NTTP",
    vi_description="Định dạng phân nhánh theo kiểu, ring buffer cố định, và mẹo NTTP là cỡ mảng.",
    after_lesson=L3C,
    minutes=20,
    difficulty="advanced",
)

M3_PRAC3_CH = [CH_UNIFORM_PRINT, CH_NTPP_BUFFER, CH_ARRAY_BOUND]
M3_PRAC3_VI = {"cppa3-uniform-print": VI_UNIFORM_PRINT,
               "cppa3-nttp-buffer": VI_NTPP_BUFFER,
               "cppa3-array-bound-nttp": VI_ARRAY_BOUND}

M3_PRAC3_SOL = [
    ("cppa3-uniform-print",
     PRINT_BOILER + "\ntemplate <class... A>\nstd::string describe(A... a) {\n    std::string out;\n    auto add = [&](const auto& v) {\n        using U = std::decay_t<decltype(v)>;\n        if constexpr (std::is_integral_v<U>) {\n            out += \"int(\" + std::to_string(v) + \")\";\n        } else if constexpr (std::is_floating_point_v<U>) {\n            out += \"dbl(\" + std::to_string(v) + \")\";\n        } else {\n            out += \"str(\" + std::string(v) + \")\";\n        }\n    };\n    ((add(a), out += \" \"), ...);\n    if (!out.empty()) out.pop_back();\n    return out;\n}\n",
     PRINT_BOILER + "\ntemplate <class... A>\nstd::string describe(A... a) {\n    std::string out;\n    auto add = [&](const auto& v) {\n        out += \"int(\" + std::to_string(v) + \")\";  // WRONG: no if constexpr, to_string(string) will not compile\n    };\n    ((add(a), out += \" \"), ...);\n    if (!out.empty()) out.pop_back();\n    return out;\n}\n"),
    ("cppa3-nttp-buffer",
     RING_BOILER + "\ntemplate <std::size_t N>\nvoid Ring<N>::push(int v) { data_[head_ % N] = v; ++head_; }\ntemplate <std::size_t N>\nconstexpr std::size_t Ring<N>::capacity() { return N; }\n",
     RING_BOILER + "\ntemplate <std::size_t N>\nvoid Ring<N>::push(int v) { data_[(head_ + 1) % N] = v; ++head_; }  // WRONG: skips a slot\ntemplate <std::size_t N>\nconstexpr std::size_t Ring<N>::capacity() { return N; }\n"),
    ("cppa3-array-bound-nttp",
     STRLEN_BOILER + "\ntemplate <std::size_t N>\nconstexpr std::size_t strLen(const char (&s)[N]) { return N - 1; }\ntemplate <std::size_t N>\nconstexpr char firstChar(const char (&s)[N]) { return s[0]; }\n",
     STRLEN_BOILER + "\ntemplate <std::size_t N>\nconstexpr std::size_t strLen(const char (&s)[N]) { return N; }   // WRONG: includes the terminator\ntemplate <std::size_t N>\nconstexpr char firstChar(const char (&s)[N]) { return s[0]; }\n"),
]

write_practice(M3, **M3_PRAC3, challenges=M3_PRAC3_CH, vi_challenges=M3_PRAC3_VI, solutions=M3_PRAC3_SOL)

# ---- ctad practice ----
BOX_BOILER = r'''#include <cstddef>
#include <iterator>
#include <type_traits>
#include <vector>

template <class T>
struct Box {
    std::vector<T> items;
    template <class It>
    Box(It first, It last) : items(first, last) {}
};

// TODO: write the deduction guide so Box b(begin(arr), end(arr)) deduces
// Box<int> (the element type), NOT Box<int*> (the iterator type).
'''

CH_CTAD_GUIDE = challenge(
    "cppa3-ctad-guide",
    "Write the Missing Deduction Guide",
    "`Box`'s iterator-pair constructor deduces the iterator type by default — `Box<int*>` instead of `Box<int>`. Write the deduction guide that steers CTAD to the element type.",
    BOX_BOILER,
    [
        ("CTAD lands on the element type",
         r'''int arr[] = {5, 6, 7};
Box b(std::begin(arr), std::end(arr));
static_assert(std::is_same_v<decltype(b), Box<int>>, "must deduce element type");
CHECK_EQ(b.items.size(), std::size_t{3});
CHECK_EQ(b.items[1], 6);''',
         "template <class It>\nBox(It first, It last) -> Box<std::iter_value_t<It>>; (or std::iterator_traits<It>::value_type)."),
    ],
    difficulty="advanced",
)

VI_CTAD_GUIDE = vi_challenge(
    "Viết deduction guide còn thiếu",
    "Constructor nhận cặp iterator của `Box` mặc định suy ra kiểu iterator — `Box<int*>` thay vì `Box<int>`. Hãy viết deduction guide dẫn CTAD về kiểu phần tử.",
    [
        ("CTAD đáp đúng kiểu phần tử", "template <class It>\nBox(It first, It last) -> Box<std::iter_value_t<It>>; (hoặc std::iterator_traits<It>::value_type)."),
    ],
)

STATS_BOILER = r'''#include <cstddef>
#include <type_traits>
#include <utility>

template <class T>
struct Stats {
    T min;
    T max;
    Stats(T lo, T hi) : min(std::move(lo)), max(std::move(hi)) {}
    // TODO: add an array constructor that scans the whole array for min/max:
    //   template <std::size_t N> Stats(const T (&a)[N]);
    // plus the deduction guide that lets Stats s{arr}; deduce Stats<T>.
};
'''

CH_CTAD_ARRAY = challenge(
    "cppa3-ctad-array",
    "CTAD from a C Array",
    "Add to `Stats` an array constructor that scans for the real min/max, and the deduction guide so `Stats s{arr};` deduces `Stats<int>` from `int arr[]`.",
    STATS_BOILER,
    [
        ("guide + constructor deduce and scan",
         r'''int arr[] = {4, 8, 2};
Stats s{arr};
static_assert(std::is_same_v<decltype(s), Stats<int>>, "deduce element type");
CHECK_EQ(s.min, 2);
CHECK_EQ(s.max, 8);''',
         "template <std::size_t N> Stats(const T (&a)[N]) : min(a[0]), max(a[0]) { for (std::size_t i = 1; i < N; ++i) { if (a[i] < min) min = a[i]; if (a[i] > max) max = a[i]; } }\ntemplate <class T, std::size_t N> Stats(const T (&)[N]) -> Stats<T>;"),
        ("pair constructor still works",
         r'''Stats p{1, 2};
static_assert(std::is_same_v<decltype(p), Stats<int>>, "pair still deduces");
CHECK_EQ(p.min, 1);
CHECK_EQ(p.max, 2);''',
         "Do not break the original constructor — CTAD tries all guides."),
    ],
    difficulty="advanced",
)

VI_CTAD_ARRAY = vi_challenge(
    "CTAD từ mảng C",
    "Thêm vào `Stats` một constructor nhận mảng quét tìm min/max thật, và deduction guide để `Stats s{arr};` suy ra `Stats<int>` từ `int arr[]`.",
    [
        ("guide + constructor suy luận và quét", "template <std::size_t N> Stats(const T (&a)[N]) : min(a[0]), max(a[0]) { for (std::size_t i = 1; i < N; ++i) { if (a[i] < min) min = a[i]; if (a[i] > max) max = a[i]; } }\ntemplate <class T, std::size_t N> Stats(const T (&)[N]) -> Stats<T>;"),
        ("constructor cặp vẫn chạy", "Đừng phá constructor gốc — CTAD thử tất cả các guide."),
    ],
)

M3_PRAC4 = dict(
    sid="m3-ctad-practice",
    title="CTAD in Anger",
    description="The missing-guide bug class every library author meets, and a deduction guide backed by a scanning constructor.",
    vi_title="CTAD trong thực chiến",
    vi_description="Họ lỗi thiếu guide mà mọi tác giả thư viện đều gặp, và một deduction guide đi cùng constructor quét mảng.",
    after_lesson=L3D,
    minutes=18,
    difficulty="advanced",
)

M3_PRAC4_CH = [CH_CTAD_GUIDE, CH_CTAD_ARRAY]
M3_PRAC4_VI = {"cppa3-ctad-guide": VI_CTAD_GUIDE,
               "cppa3-ctad-array": VI_CTAD_ARRAY}

M3_PRAC4_SOL = [
    ("cppa3-ctad-guide",
     BOX_BOILER + "\ntemplate <class It>\nBox(It first, It last) -> Box<std::iter_value_t<It>>;\n",
     BOX_BOILER + "\ntemplate <class It>\nBox(It first, It last) -> Box<It>;  // WRONG: deduces the iterator type again\n"),
    ("cppa3-ctad-array",
     r'''#include <cstddef>
#include <type_traits>
#include <utility>

template <class T>
struct Stats {
    T min;
    T max;
    Stats(T lo, T hi) : min(std::move(lo)), max(std::move(hi)) {}
    template <std::size_t N>
    Stats(const T (&a)[N]) : min(a[0]), max(a[0]) {
        for (std::size_t i = 1; i < N; ++i) {
            if (a[i] < min) min = a[i];
            if (a[i] > max) max = a[i];
        }
    }
};
template <class T, std::size_t N>
Stats(const T (&)[N]) -> Stats<T>;
''',
     r'''#include <cstddef>
#include <type_traits>
#include <utility>

template <class T>
struct Stats {
    T min;
    T max;
    Stats(T lo, T hi) : min(std::move(lo)), max(std::move(hi)) {}
    template <std::size_t N>
    Stats(const T (&a)[N]) : min(a[0]), max(a[N - 1]) { }  // WRONG: assumes sorted input
};
template <class T, std::size_t N>
Stats(const T (&)[N]) -> Stats<T>;
'''),
]

write_practice(M3, **M3_PRAC4, challenges=M3_PRAC4_CH, vi_challenges=M3_PRAC4_VI, solutions=M3_PRAC4_SOL)

# ---- module 3 checkpoint ----
CP3_MD = r'''
The generic checkpoint: folds, sizeof..., and empty-pack correctness in one challenge.
'''

CP3_BOILER = r'''#include <cstddef>

template <class... A>
constexpr int sumSquares(A... a);   // empty pack -> 0

template <class... A>
constexpr std::size_t countPack(A... a);   // element count
'''

write_checkpoint(
    M3, L3E,
    "Checkpoint: Generic Machinery",
    "Prove variadic folds, pack counting, and empty-pack correctness in one graded challenge.",
    16,
    CP3_MD,
    "Checkpoint: Cỗ máy generic",
    "Chứng minh variadic fold, đếm pack và tính đúng với pack rỗng trong một thử thách có chấm điểm.",
    r'''
Checkpoint generic: fold, sizeof... và tính đúng với pack rỗng trong một thử thách.
''',
    challenge(
        "cppa3-generic-checkpoint",
        "Generic Gauntlet",
        "Implement `sumSquares` (binary fold over squares, empty pack -> 0) and `countPack` (sizeof...).",
        CP3_BOILER,
        [
            ("sumSquares folds squares",
             r'''static_assert(sumSquares(1, 2, 3) == 14, "squares");
static_assert(sumSquares() == 0, "empty");
CHECK_EQ(sumSquares(4), 16);''',
             "(0 + ... + (a * a)) — the binary fold handles the empty pack."),
            ("countPack is sizeof...",
             r'''static_assert(countPack(1, 2, 3, 4) == 4, "count");
static_assert(countPack() == 0, "empty count");''',
             "return sizeof...(a);"),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại generic",
        "Cài `sumSquares` (binary fold trên bình phương, pack rỗng -> 0) và `countPack` (sizeof...).",
        [
            ("sumSquares fold bình phương", "(0 + ... + (a * a)) — binary fold xử lý được pack rỗng."),
            ("countPack là sizeof...", "return sizeof...(a);"),
        ],
    ),
    solution=CP3_BOILER + "\ntemplate <class... A>\nconstexpr int sumSquares(A... a) { return (0 + ... + (a * a)); }\ntemplate <class... A>\nconstexpr std::size_t countPack(A... a) { return sizeof...(a); }\n",
    wrong=CP3_BOILER + "\ntemplate <class... A>\nconstexpr int sumSquares(A... a) { return (a + ...); }   // WRONG: unary fold — breaks on the empty pack\ntemplate <class... A>\nconstexpr std::size_t countPack(A... a) { return sizeof...(a); }\n",
)

# ============================ MODULE 4: concepts ============================
M4 = "concepts"

L4A = "concepts-requires"
L4B = "overloads-subsumption"
L4C = "diagnostics"
L4D = "cppa-checkpoint-concepts"

write_module(
    M4,
    "Concepts & Constrained APIs",
    "requirements, ad-hoc constraints, subsumption, and diagnostics — design APIs whose misuse is a clear compiler error instead of a runtime surprise.",
    "Concepts & API Có Ràng Buộc",
    "requirements, ràng buộc ad-hoc, subsumption và diagnostics — thiết kế API mà việc dùng sai trở thành lỗi compiler rõ ràng thay vì bất ngờ lúc chạy.",
    [L4A, L4B, L4C, L4D],
    ["m4-concept-practice", "m4-overload-practice"],
)

write_lesson(
    M4, L4A,
    "Concepts and requires Expressions",
    "Named constraints, the four kinds of requirements, and ad-hoc requires-clauses on function templates.",
    11,
    r'''
A **concept** is a named compile-time predicate over types. The modern replacement for SFINAE — and the single biggest readability upgrade in modern C++.

## The four requirement kinds

```cpp
template <class C>
concept SizedContainer = requires(const C& c, const C& d, C& mut) {
    c.size();                                   // simple requirement: expression is valid
    { c.size() } -> std::convertible_to<std::size_t>;  // type requirement on the result
    typename C::value_type;                     // type requirement: a member type exists
    requires std::is_class_v<C>;                // nested requirement: a boolean constraint
};
```

The **const-correctness of the probe matters**: `requires(const C& c) { c.size(); }` only accepts containers whose `size()` is const-callable. Probing with a non-const reference is the classic false-positive.

## Ad-hoc constraints on functions

```cpp
template <class T>
requires std::is_arithmetic_v<T>          // ad-hoc requires-clause
T twice(T v) { return v * 2; }

template <class T> requires requires(T t) { t * 2; }   // ad-hoc requires-REQUIRES
T twice2(T v) { return v * 2; }
```

`requires requires` is not a typo: the outer clause, then an inline requires-expression as its operand. Prefer a *named* concept once a constraint appears twice.
''',
    "Concepts và requires Expression",
    "Ràng buộc có tên, bốn loại requirement và mệnh đề requires ad-hoc trên function template.",
    r'''
**Concept** là một vị từ compile-time có tên áp lên các kiểu. Nó là thay thế hiện đại cho SFINAE — và là nâng cấp dễ đọc lớn nhất của C++ hiện đại.

## Bốn loại requirement

```cpp
template <class C>
concept SizedContainer = requires(const C& c, const C& d, C& mut) {
    c.size();                                   // simple requirement: biểu thức hợp lệ
    { c.size() } -> std::convertible_to<std::size_t>;  // ràng buộc kiểu trên kết quả
    typename C::value_type;                     // type requirement: tồn tại kiểu thành viên
    requires std::is_class_v<C>;                // nested requirement: ràng buộc boolean
};
```

**Tính const-correct của probe rất quan trọng**: `requires(const C& c) { c.size(); }` chỉ chấp nhận container có `size()` gọi được trên đối tượng const. Probe bằng reference non-const là false-positive kinh điển.

## Ràng buộc ad-hoc trên hàm

```cpp
template <class T>
requires std::is_arithmetic_v<T>          // mệnh đề requires ad-hoc
T twice(T v) { return v * 2; }

template <class T> requires requires(T t) { t * 2; }   // requires-REQUIRES ad-hoc
T twice2(T v) { return v * 2; }
```

`requires requires` không phải lỗi đánh máy: vế ngoài là mệnh đề, vế trong là requires-expression nội tuyến làm toán hạng. Khi một ràng buộc xuất hiện lần thứ hai, hãy đặt cho nó tên (concept riêng).
''',
    difficulty="advanced",
)

write_lesson(
    M4, L4B,
    "Subsumption: Overloads That Pick Themselves",
    "When one concept implies another, the compiler routes calls to the more specific overload automatically — design constraints as a hierarchy.",
    10,
    r'''
## Subsumption in one picture

If concept `B`'s constraints logically include concept `A`'s (`SizedIterable = Iterable<T> && has_size`), then `B` **subsumes** `A`. Given both overloads, a call satisfying both resolves to the `B` version — no tag dispatch, no priority tricks, no ambiguity:

```cpp
template <Iterable C>     std::string category(const C&) { return "iterable"; }
template <SizedIterable C> std::string category(const C&) { return "sized-iterable"; }
```

`category(std::vector<int>{})` picks "sized-iterable"; a begin/end-only range picks "iterable". The compiler knows `Iterable && X` is *more constrained than* `Iterable` because it tracks the constraint expression's structure.

## Why this beats tag dispatch

The subsumption graph lives in the *types* — a caller cannot pick the wrong overload, and a new level in the hierarchy needs zero call-site changes. tag-dispatch code needs every site updated.

## Design pattern: constraint ladders

Order your overloads from most to least constrained and let subsumption route:

1. `SizedRandomAccess` — indexable and sized: O(1) paths,
2. `Iterable` — anything with begin/end: linear paths,
3. unconstrained fallback — clear error or deferred runtime check.

The graded exercise builds exactly this ladder and asks which rung served the call.
''',
    "Subsumption: Overload Tự Chọn Đường",
    "Khi một concept kéo theo concept khác, compiler tự chuyển lời gọi sang overload chuyên biệt hơn — hãy thiết kế ràng buộc thành hệ phân cấp.",
    r'''
## Subsumption trong một hình

Nếu ràng buộc của concept `B` bao hàm logic ràng buộc của concept `A` (`SizedIterable = Iterable<T> && has_size`), thì `B` **subsumes** `A`. Khi cả hai overload tồn tại, lời gọi thỏa cả hai sẽ phân giải về bản `B` — không cần tag dispatch, không thủ thuật priority, không mơ hồ:

```cpp
template <Iterable C>     std::string category(const C&) { return "iterable"; }
template <SizedIterable C> std::string category(const C&) { return "sized-iterable"; }
```

`category(std::vector<int>{})` chọn "sized-iterable"; một range chỉ có begin/end chọn "iterable". Compiler biết `Iterable && X` *chặt hơn* `Iterable` vì nó theo dõi cấu trúc của biểu thức ràng buộc.

## Vì sao vượt trội hơn tag dispatch

Đồ thị subsumption nằm trong *kiểu* — caller không thể chọn nhầm overload, và thêm một nấc mới vào hệ phân cấp không cần đổi bất cứ lời gọi nào. Code tag-dispatch thì phải cập nhật mọi điểm gọi.

## Mẫu thiết kế: thang ràng buộc

Xếp overload từ chặt nhất đến lỏng nhất và để subsumption dẫn đường:

1. `SizedRandomAccess` — đánh chỉ số được và có size: đường đi O(1),
2. `Iterable` — bất cứ thứ gì có begin/end: đường đi tuyến tính,
3. fallback không ràng buộc — báo lỗi rõ ràng hoặc kiểm tra lúc chạy.

Bài tập chấm điểm dựng đúng cái thang này và hỏi bậc nào đã phục vụ lời gọi.
''',
    difficulty="advanced",
)

write_lesson(
    M4, L4C,
    "Reading Constraint Diagnostics",
    "The skill that pays daily: turning a wall of constraint text into the one line that matters.",
    9,
    r'''
Concept errors fail with *candidate diagnostics*: the compiler lists every overload, why each was rejected, and which requirement in which concept failed. Reading them is a filter, not a parse.

## The three-scan method

1. **Scan for the word "constraint" / "unsatisfied"** — find the concept that failed,
2. **scan for "because" / "note"** — the first note usually names the exact expression that did not type-check (`c.size()` on a const object, a missing `value_type`),
3. **only then** look at the call site.

A 40-line diagnostic is typically 2 lines of signal: *which concept*, *which atomic requirement*.

## The errors that mean you, not the caller

- `no matching function` + `constraints not satisfied` + `the required type 'typename C::value_type' is invalid` — your concept demands a member type the caller's type lacks. Either the caller's type is wrong or your concept over-demands.
- `ambiguous` overloads after adding a concept — your two constrained overloads are **not** subsumed (independent constraints). Tie them: make one a refinement of the other.

## Contract-first habit

Write the concept *before* the implementation; the concept is the API's contract, and the compiler enforces it at every call site. The graded exercise hands you a diagnostic and asks which requirement failed — the same skill as triaging a teammate's template error.
''',
    "Đọc Diagnostics Của Ràng Buộc",
    "Kỹ năng mang lại giá trị hằng ngày: biến cả bức tường chữ ràng buộc thành đúng một dòng quan trọng.",
    r'''
Lỗi concept thất bại với *diagnostics dạng candidate*: compiler liệt kê mọi overload, lý do từng cái bị từ chối, và requirement nào trong concept nào thất bại. Đọc chúng là phép lọc, không phải phép phân tích nguyên văn.

## Phương pháp ba lượt quét

1. **Quét chữ "constraint" / "unsatisfied"** — tìm concept đã thất bại,
2. **quét chữ "because" / "note"** — note đầu tiên thường chỉ ra đúng biểu thức không type-check (`c.size()` trên đối tượng const, thiếu `value_type`),
3. **sau đó** mới xem chỗ gọi.

Diagnostic 40 dòng thường chỉ có 2 dòng tín hiệu: *concept nào*, *requirement nguyên tử nào*.

## Những lỗi nghĩa là lỗi của bạn, không phải của caller

- `no matching function` + `constraints not satisfied` + `the required type 'typename C::value_type' is invalid` — concept của bạn đòi một member type mà kiểu của caller không có. Hoặc caller sai kiểu, hoặc concept của bạn đòi quá mức.
- Overload `ambiguous` sau khi thêm concept — hai overload có ràng buộc của bạn **không** subsume nhau (ràng buộc độc lập). Hãy buộc chúng thành quan hệ tinh chỉnh: một cái là mở rộng của cái kia.

## Thói quen hợp đồng trước

Viết concept *trước* phần cài đặt; concept là hợp đồng của API, và compiler thực thi nó tại mọi điểm gọi. Bài tập chấm điểm đưa cho bạn một diagnostic và hỏi requirement nào đã thất bại — đúng kỹ năng xử lý lỗi template của đồng nghiệp.
''',
    difficulty="advanced",
)

# ---- module 4 practices ----
CH_CONCEPT_WRITE = challenge(
    "cppa4-concept-write",
    "Write Your First Concept",
    "Define `Numeric` (arithmetic types only) and a constrained `maxOf(a, b)`; provide a fallback `maxOfAny` returning a sentinel for non-numeric pairs.",
    r'''#include <string>
#include <type_traits>

// TODO: template <class T> concept Numeric = ...;
// TODO: template <Numeric T> T maxOf(T a, T b);
// TODO: fallback for anything else
std::string maxOfAny(const void*, const void*);  // sentinel path
''',
    [
        ("maxOf works on numerics",
         r'''CHECK_EQ(maxOf(3, 7), 7);
CHECK_EQ(maxOf(2.5, 1.5), 2.5);
CHECK_EQ(maxOf(1, -1), 1);''',
         "template <class T> concept Numeric = std::is_arithmetic_v<T>; then maxOf returns b if a < b else a."),
        ("fallback engages for non-numerics",
         r'''CHECK_EQ(maxOfAny(nullptr, nullptr), std::string("sentinel"));''',
         "An unconstrained overload with different arity/types is the fallback — keep maxOf constrained so it never claims non-numerics."),
    ],
    difficulty="advanced",
)

VI_CONCEPT_WRITE = vi_challenge(
    "Viết concept đầu tiên",
    "Định nghĩa `Numeric` (chỉ kiểu số học) và `maxOf(a, b)` có ràng buộc; cung cấp fallback `maxOfAny` trả về sentinel cho cặp không phải số.",
    [
        ("maxOf chạy với số", "template <class T> concept Numeric = std::is_arithmetic_v<T>; rồi maxOf trả về b nếu a < b, ngược lại a."),
        ("fallback kích hoạt với phi số", "Một overload không ràng buộc với chữ ký khác chính là fallback — giữ maxOf có ràng buộc để nó không nhận kiểu phi số."),
    ],
)

CH_ADHOC_REQUIRES = challenge(
    "cppa4-adhoc-requires",
    "The const-Probe Concept",
    "Implement `Sized` as an ad-hoc `requires requires` clause probing `c.size()` **on a const reference** (with a `std::convertible_to<std::size_t>` result), and `totalIfSized(c)` returning the size — or -1 through the fallback for unsatisfying types.",
    r'''#include <cstddef>
#include <concepts>
#include <vector>

// TODO: template <class C> concept Sized = requires(const C& c) { ... };
// TODO: template <Sized C> std::size_t totalIfSized(const C& c);
// TODO: fallback: template <class C> std::size_t totalIfSized(const C&);  // returns -1 cast
''',
    [
        ("sized containers report their size",
         r'''CHECK_EQ(totalIfSized(std::vector<int>{1, 2, 3}), std::size_t{3});
CHECK_EQ(totalIfSized(std::vector<int>{}), std::size_t{0});''',
         "template <class C> concept Sized = requires(const C& c) { { c.size() } -> std::convertible_to<std::size_t>; };"),
        ("unsized types hit the fallback",
         r'''struct NoSize {};
CHECK_EQ(totalIfSized(NoSize{}), static_cast<std::size_t>(-1));''',
         "The unconstrained fallback overload (declarable as a template taking any C) returns static_cast<std::size_t>(-1)."),
        ("a non-const size() does NOT satisfy",
         r'''struct Constless {
    std::size_t size() { return 99; }   // not const — must not satisfy Sized
};
CHECK_EQ(totalIfSized(Constless{}), static_cast<std::size_t>(-1));''',
         "The probe must be requires(const C& c) — a non-const size() fails the probe, so the fallback answers."),
    ],
    difficulty="advanced",
)

VI_ADHOC_REQUIRES = vi_challenge(
    "Concept probe const",
    "Cài `Sized` bằng mệnh đề `requires requires` ad-hoc, probe `c.size()` **trên tham chiếu const** (kết quả `std::convertible_to<std::size_t>`), và `totalIfSized(c)` trả về size — hoặc -1 qua fallback với kiểu không thỏa.",
    [
        ("container có size báo size", "template <class C> concept Sized = requires(const C& c) { { c.size() } -> std::convertible_to<std::size_t>; };"),
        ("type không có size rơi vào fallback", "Overload fallback không ràng buộc (viết thành template nhận C bất kỳ) trả về static_cast<std::size_t>(-1)."),
        ("size() non-const KHÔNG thỏa", "Probe phải là requires(const C& c) — size() non-const khiến probe thất bại, fallback trả lời."),
    ],
)

CH_SUBSUMPTION_LADDER = challenge(
    "cppa4-overload-subsumption",
    "The Constraint Ladder",
    "Define `Iterable` (begin/end) and `SizedIterable` (refining it with size), then three `category` overloads — sized, iterable-only, and other — and verify subsumption routes each type to the right rung.",
    r'''#include <concepts>
#include <string>
#include <vector>

// TODO: template <class T> concept Iterable = ...;
// TODO: template <class T> concept SizedIterable = Iterable<T> && ...;
// TODO: three overloads:
//   template <SizedIterable C> std::string category(const C&);  -> "sized-iterable"
//   template <Iterable C> std::string category(const C&);       -> "iterable"
//   template <class C> std::string category(const C&);          -> "other"
''',
    [
        ("vector lands on the sized rung",
         r'''CHECK_EQ(category(std::vector<int>{}), std::string("sized-iterable"));''',
         "Subsumption: SizedIterable (more constrained) wins for anything with begin/end/size."),
        ("begin/end-only lands on iterable",
         r'''struct RangeOnly {
    int* begin() { return nullptr; }
    int* end() { return nullptr; }
};
CHECK_EQ(category(RangeOnly{}), std::string("iterable"));''',
         "RangeOnly has begin/end but no size — Iterable only."),
        ("everything else lands on other",
         r'''CHECK_EQ(category(42), std::string("other"));''',
         "The unconstrained overload catches the rest."),
    ],
    difficulty="advanced",
)

VI_SUBSUMPTION_LADDER = vi_challenge(
    "Thang ràng buộc",
    "Định nghĩa `Iterable` (begin/end) và `SizedIterable` (tinh chỉnh thêm size), rồi ba overload `category` — sized, chỉ iterable, và other — kiểm chứng subsumption đưa từng kiểu tới đúng bậc.",
    [
        ("vector đáp bậc sized", "Subsumption: SizedIterable (chặt hơn) thắng với mọi thứ có begin/end/size."),
        ("chỉ begin/end đáp bậc iterable", "RangeOnly có begin/end nhưng không có size — chỉ Iterable."),
        ("còn lại đáp other", "Overload không ràng buộc nhận phần còn lại."),
    ],
)

M4_PRAC1 = dict(
    sid="m4-concept-practice",
    title="Concept Fundamentals",
    description="Named concepts, const-probe requires-clauses, and fallback overloads — the daily toolkit of constrained API design.",
    vi_title="Nền tảng concept",
    vi_description="Concept có tên, mệnh đề requires probe const, và overload fallback — bộ dụng cụ hằng ngày của thiết kế API có ràng buộc.",
    after_lesson=L4A,
    minutes=22,
    difficulty="advanced",
)

M4_PRAC1_CH = [CH_CONCEPT_WRITE, CH_ADHOC_REQUIRES]
M4_PRAC1_VI = {"cppa4-concept-write": VI_CONCEPT_WRITE,
               "cppa4-adhoc-requires": VI_ADHOC_REQUIRES}

M4_PRAC1_SOL = [
    ("cppa4-concept-write",
     r'''#include <string>
#include <type_traits>

template <class T>
concept Numeric = std::is_arithmetic_v<T>;

template <Numeric T>
T maxOf(T a, T b) { return a < b ? b : a; }

std::string maxOfAny(const void*, const void*) { return "sentinel"; }
''',
     r'''#include <string>
#include <type_traits>

template <class T>
concept Numeric = std::is_arithmetic_v<T>;

template <Numeric T>
T maxOf(T a, T b) { return a < b ? a : b; }  // WRONG: inverted comparison

std::string maxOfAny(const void*, const void*) { return "sentinel"; }
'''),
    ("cppa4-adhoc-requires",
     r'''#include <cstddef>
#include <concepts>
#include <vector>

template <class C>
concept Sized = requires(const C& c) {
    { c.size() } -> std::convertible_to<std::size_t>;
};

template <Sized C>
std::size_t totalIfSized(const C& c) { return c.size(); }

template <class C>
std::size_t totalIfSized(const C&) { return static_cast<std::size_t>(-1); }
''',
     r'''#include <cstddef>
#include <concepts>
#include <vector>

template <class C>
concept Sized = requires(C& c) {   // WRONG: non-const probe
    { c.size() } -> std::convertible_to<std::size_t>;
};

template <Sized C>
std::size_t totalIfSized(const C& c) { return c.size(); }

template <class C>
std::size_t totalIfSized(const C&) { return static_cast<std::size_t>(-1); }
'''),
]

write_practice(M4, **M4_PRAC1, challenges=M4_PRAC1_CH, vi_challenges=M4_PRAC1_VI, solutions=M4_PRAC1_SOL)

M4_PRAC2 = dict(
    sid="m4-overload-practice",
    title="Subsumption Ladders",
    description="Constraint hierarchies that route calls themselves — no tag dispatch needed.",
    vi_title="Thang subsumption",
    vi_description="Hệ phân cấp ràng buộc tự dẫn đường cho lời gọi — không cần tag dispatch.",
    after_lesson=L4B,
    minutes=16,
    difficulty="advanced",
)

M4_PRAC2_CH = [CH_SUBSUMPTION_LADDER]
M4_PRAC2_VI = {"cppa4-overload-subsumption": VI_SUBSUMPTION_LADDER}

M4_PRAC2_SOL = [
    ("cppa4-overload-subsumption",
     r'''#include <concepts>
#include <string>
#include <vector>

template <class T>
concept Iterable = requires(T t) { t.begin(); t.end(); };

template <class T>
concept SizedIterable = Iterable<T> && requires(const T& t) {
    { t.size() } -> std::convertible_to<std::size_t>;
};

template <SizedIterable C>
std::string category(const C&) { return "sized-iterable"; }

template <Iterable C>
std::string category(const C&) { return "iterable"; }

template <class C>
std::string category(const C&) { return "other"; }
''',
     r'''#include <concepts>
#include <string>
#include <vector>

template <class T>
concept Iterable = requires(T t) { t.begin(); t.end(); };

template <class T>
concept SizedIterable = requires(const T& t) {   // WRONG: not a refinement of Iterable
    { t.size() } -> std::convertible_to<std::size_t>;
};

template <SizedIterable C>
std::string category(const C&) { return "sized-iterable"; }

template <Iterable C>
std::string category(const C&) { return "iterable"; }

template <class C>
std::string category(const C&) { return "other"; }
'''),
]

write_practice(M4, **M4_PRAC2, challenges=M4_PRAC2_CH, vi_challenges=M4_PRAC2_VI, solutions=M4_PRAC2_SOL)

# ---- module 4 checkpoint ----
CP4_MD = r'''
The concepts checkpoint: one concept, one constrained function, one fallback — const-probing included.
'''

CP4_BOILER = r'''#include <cstddef>
#include <concepts>
#include <functional>
#include <string>

// TODO: concept Hashable: std::hash<T>{}(t) works on a const T and yields something
//       convertible to std::size_t.
// TODO: std::size_t hashOf(const T&) constrained  -> real hash
// TODO: fallback overload                         -> 0
struct NoHash {};
'''

write_checkpoint(
    M4, L4D,
    "Checkpoint: Concepts",
    "Prove concept authorship with a const-correct probe and a clean fallback.",
    15,
    CP4_MD,
    "Checkpoint: Concepts",
    "Chứng minh khả năng viết concept với probe đúng chuẩn const và fallback sạch sẽ.",
    r'''
Checkpoint concepts: một concept, một hàm có ràng buộc, một fallback — có cả probe const.
''',
    challenge(
        "cppa4-concept-checkpoint",
        "Hashable Gauntlet",
        "Implement `Hashable` (std::hash works on a **const** T, result convertible to std::size_t), constrained `hashOf` returning the real hash, and a fallback returning 0.",
        CP4_BOILER,
        [
            ("hashable types hash",
             r'''CHECK_EQ(hashOf(42), std::hash<int>{}(42));
CHECK_EQ(hashOf(std::string("key")), std::hash<std::string>{}(std::string("key")));''',
             "template <class T> concept Hashable = requires(const T& t) { { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>; };"),
            ("non-hashable types fall back to 0",
             r'''CHECK_EQ(hashOf(NoHash{}), std::size_t{0});''',
             "Unconstrained overload returning 0 — std::hash<NoHash> does not exist, so the concept rejects it."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại Hashable",
        "Cài `Hashable` (std::hash chạy trên **const** T, kết quả chuyển được sang std::size_t), `hashOf` có ràng buộc trả về hash thật, và fallback trả về 0.",
        [
            ("kiểu hashable hash được", "template <class T> concept Hashable = requires(const T& t) { { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>; };"),
            ("kiểu không hash được về 0", "Overload không ràng buộc trả về 0 — std::hash<NoHash> không tồn tại nên concept từ chối nó."),
        ],
    ),
    solution=CP4_BOILER + "\ntemplate <class T>\nconcept Hashable = requires(const T& t) {\n    { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>;\n};\ntemplate <Hashable T>\nstd::size_t hashOf(const T& t) { return std::hash<T>{}(t); }\ntemplate <class T>\nstd::size_t hashOf(const T&) { return 0; }\n",
    wrong=CP4_BOILER + "\ntemplate <class T>\nconcept Hashable = requires(const T& t) {\n    { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>;\n};\ntemplate <Hashable T>\nstd::size_t hashOf(const T& t) { return std::hash<T>{}(t); }\ntemplate <class T>\nstd::size_t hashOf(const T&) { return 1; }  // WRONG: fallback must return 0\n",
)

print("modules 3-4 done")
