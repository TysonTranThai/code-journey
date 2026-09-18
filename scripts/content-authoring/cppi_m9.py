#!/usr/bin/env python3
"""C++ Intermediate — Module 9: templates.

Authoring discipline: every C++ code string (tests, solutions, boilerplate) is
a raw triple-quoted string, so real newlines stay real and C++ "\\n" literals
stay literal. Snippets are self-contained: each test is its own translation
unit (solution.cpp is #included; no cross-test state).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "templates"

# ---- lesson function-templates -------------------------------------------------
L_function_templates_EN = r"""
A function template is a recipe the compiler stamps out per type. You write
the algorithm once; the compiler writes the type-specific versions.

```cpp
template <typename T>
T max_of(const T& a, const T& b) {
    return a < b ? b : a;   // T must support operator< — that's the contract
}

int i = max_of(3, 7);          // T = int (deduced)
double d = max_of(2.5, 1.5);   // T = double
auto m = max_of(std::string{"a"}, std::string{"b"});
```

Key mechanics:

- **Deduction** happens from the arguments; explicit spelling
  `max_of<double>(3, 7)` forces it (and permits conversions).
- The **contract is implicit**: whatever operations the body uses become
  requirements on T. A type without `operator<` fails at instantiation —
  with a long error, but at compile time, never at runtime.
- Two-phase translation: the template itself is only *syntax-checked*;
  each instantiation is fully checked against the real T.
- Templates live in headers. The compiler needs the definition at the
  point of instantiation — a .cpp definition produces linker errors.
"""

L_function_templates_VI = r"""
Function template là một công thức mà compiler đóng khuôn theo từng kiểu.
Bạn viết thuật toán một lần; compiler viết các bản đặc thù theo kiểu.

```cpp
template <typename T>
T max_of(const T& a, const T& b) {
    return a < b ? b : a;   // T phải hỗ trợ operator< — đó là hợp đồng
}

int i = max_of(3, 7);          // T = int (suy luận)
double d = max_of(2.5, 1.5);   // T = double
auto m = max_of(std::string{"a"}, std::string{"b"});
```

Cơ chế then chốt:

- **Suy luận** diễn ra từ đối số; viết tường minh `max_of<double>(3, 7)`
  épbuộc nó (và cho phép chuyển đổi kiểu).
- **Hợp đồng là ngầm định**: mọi thao tác thân hàm dùng trở thành yêu cầu
  với T. Một kiểu thiếu `operator<` fail lúc instantiate — với lỗi dài,
  nhưng ở compile time, không bao giờ ở runtime.
- Dịch hai pha: bản thân template chỉ được *kiểm tra cú pháp*; mỗi lần
  instantiate được kiểm tra đầy đủ với T thật.
- Template sống trong header. Compiler cần định nghĩa tại điểm
  instantiate — định nghĩa trong .cpp sinh lỗi linker.
"""

# ---- lesson class-templates -------------------------------------------------------
L_class_templates_EN = r"""
Class templates parameterize a whole type. `std::vector<int>` is the
canonical example; here is a minimal Box:

```cpp
template <typename T>
class Box {
public:
    explicit Box(T value) : value_{std::move(value)} {}
    const T& get() const { return value_; }
    void set(T value) { value_ = std::move(value); }
private:
    T value_;
};

Box<int> a{42};
Box<std::string> b{"hi"};
```

Rules that matter:

- Members are instantiated **lazily**: a member function that would not
  compile for T is only an error if some code actually calls it. This is
  why `std::vector` works for non-copyable types as long as you never
  copy it.
- Multiple parameters compose: `template <typename K, typename V> class
  Map { ... };`
- Default template arguments work like default function arguments:
  `template <typename T, typename C = std::less<T>> class Sorted { ... };`
- CTAD (C++17): `Box b{42};` deduces `Box<int>`. Convenient for locals;
  spell types in interfaces.

Templates do not replace inheritance for runtime polymorphism — they
implement **static polymorphism**: the type is resolved at compile time,
zero virtual dispatch, but one concrete instantiation per type.
"""

L_class_templates_VI = r"""
Class template tham số hóa cả một kiểu. `std::vector<int>` là ví dụ kinh
điển; đây là một Box tối giản:

```cpp
template <typename T>
class Box {
public:
    explicit Box(T value) : value_{std::move(value)} {}
    const T& get() const { return value_; }
    void set(T value) { value_ = std::move(value); }
private:
    T value_;
};

Box<int> a{42};
Box<std::string> b{"hi"};
```

Những quy tắc quan trọng:

- Các member được instantiate **lười**: một hàm thành viên không biên dịch
  được với T chỉ thành lỗi khi có code thật sự gọi nó. Vì vậy `std::vector`
  chạy được với kiểu không copy được miễn là bạn không bao giờ copy nó.
- Nhiều tham số kết hợp được: `template <typename K, typename V> class
  Map { ... };`
- Tham số template mặc định giống tham số hàm mặc định: `template
  <typename T, typename C = std::less<T>> class Sorted { ... };`
- CTAD (C++17): `Box b{42};` suy ra `Box<int>`. Tiện cho biến cục bộ;
  viết rõ kiểu trong interface.

Template không thay thế inheritance cho đa hình runtime — chúng thực hiện
**đa hình tĩnh**: kiểu được quyết ở compile time, không tốn virtual
dispatch, nhưng mỗi kiểu một bản hiện thực cụ thể.
"""

# ---- lesson specialization --------------------------------------------------------
L_specialization_EN = r"""
Sometimes one type needs a different implementation than the generic
recipe. **Specialization** provides it — opt in per type, keep the
generic elsewhere.

```cpp
template <typename T>
struct Serializer {
    static std::string to(const T& v) { return std::to_string(v); }
};

// full specialization for std::string
template <>
struct Serializer<std::string> {
    static std::string to(const std::string& v) { return v; }
};

// partial specialization for every std::vector<T>
template <typename T>
struct Serializer<std::vector<T>> {
    static std::string to(const std::vector<T>& v) {
        std::string out = "[";
        for (std::size_t i = 0; i < v.size(); ++i) {
            if (i) out += ",";
            out += Serializer<T>::to(v[i]);   // recursion through the generic
        }
        return out + "]";
    }
};
```

Reading order for the compiler: full specializations beat partial ones,
which beat the primary template. The vector case above recurses: a
`std::vector<int>` uses the partial, whose elements use the primary, and
a nested vector keeps recursing — generic machinery composing itself.

Use sparingly: specialization is a hook for *implementations*, not for
changing public behavior. If the specialized type's semantics differ, a
plain overload or a differently-named function is usually clearer.
"""

L_specialization_VI = r"""
Đôi khi một kiểu cần cách hiện thực khác với công thức chung.
**Specialization** cung cấp điều đó — chọn cho từng kiểu, giữ bản chung
ở nơi khác.

```cpp
template <typename T>
struct Serializer {
    static std::string to(const T& v) { return std::to_string(v); }
};

// specialization toàn phần cho std::string
template <>
struct Serializer<std::string> {
    static std::string to(const std::string& v) { return v; }
};

// specialization riêng phần cho mọi std::vector<T>
template <typename T>
struct Serializer<std::vector<T>> {
    static std::string to(const std::vector<T>& v) {
        std::string out = "[";
        for (std::size_t i = 0; i < v.size(); ++i) {
            if (i) out += ",";
            out += Serializer<T>::to(v[i]);   // đệ quy qua bản chung
        }
        return out + "]";
    }
};
```

Thứ tự ưu tiên của compiler: specialization toàn phần thắng riêng phần,
riêng phần thắng template gốc. Trường hợp vector ở trên đệ quy: một
`std::vector<int>` dùng bản riêng phần, phần tử của nó dùng bản gốc, và
vector lồng nhau tiếp tục đệ quy — cơ chế chung tự kết hợp với nhau.

Dùng tiết chế: specialization là cái móc cho *cách hiện thực*, không phải
để thay đổi hành vi công khai. Nếu ngữ nghĩa của kiểu được chuyên biệt hóa
khác hẳn, một overload thường hoặc hàm đặt tên khác thường rõ ràng hơn.
"""

# ---- lesson generic-design ----------------------------------------------------------
L_generic_design_EN = r"""
Writing your own templates is a design activity. The discipline:

1. **Write the concrete version first.** Make it work for one type.
2. **Generalize mechanically.** Replace the concrete type with T and
   move type-specific operations behind the contract.
3. **Name the contract in comments or concepts.** "T must be movable and
   support operator<" is the interface your callers read.
4. **Test with at least two unrelated types** — int and std::string is
   the classic pair; if your template only compiles for one, it is not
   generic yet.

```cpp
// step 1-3 applied: a generic clamp
template <typename T>
T clamp_to(const T& v, const T& lo, const T& hi) {
    // contract: T supports operator< (and copies cheaply or is passed by ref)
    if (v < lo) return lo;
    if (hi < v) return hi;
    return v;
}
```

When *not* to template: runtime-varying behavior (that is polymorphism),
a single concrete call site (premature), or an API boundary where the
type must be named for documentation. Templates trade error-message
clarity for code reuse — charge that cost only when reuse is real.
"""

L_generic_design_VI = r"""
Tự viết template là một hoạt động thiết kế. Kỷ luật:

1. **Viết bản cụ thể trước.** Cho nó chạy đúng với một kiểu.
2. **Tổng quát hóa một cách cơ học.** Thay kiểu cụ thể bằng T và đẩy các
   thao tác đặc thù theo kiểu ra sau hợp đồng.
3. **Ghi tên hợp đồng trong chú thích hoặc concepts.** "T phải movable và
   hỗ trợ operator<" chính là interface mà caller đọc.
4. **Thử với ít nhất hai kiểu không liên quan** — int và std::string là
   cặp kinh điển; nếu template chỉ biên dịch với một kiểu, nó chưa phải
   generic.

```cpp
// bước 1-3 áp dụng: một clamp tổng quát
template <typename T>
T clamp_to(const T& v, const T& lo, const T& hi) {
    // hợp đồng: T hỗ trợ operator< (và copy rẻ, hoặc truyền bằng reference)
    if (v < lo) return lo;
    if (hi < v) return hi;
    return v;
}
```

Khi nào *không* nên template: hành vi thay đổi lúc runtime (đó là đa hình),
chỉ có một điểm gọi cụ thể (sớm quá), hoặc ranh giới API nơi kiểu phải được
gọi tên cho tài liệu. Template đánh đổi độ rõ của thông báo lỗi lấy khả
năng tái sử dụng — chỉ trả cái giá đó khi việc tái sử dụng là thật.
"""

# ---- practice cppi-p9-function-templates --------------------------------------------
R_MAX_OF = r'''template <typename T>
const T& max_of(const T& a, const T& b) {
    return a < b ? b : a;
}
'''

W_MAX_OF = r'''template <typename T>
const T& max_of(const T& a, const T& b) {
    return a < b ? a : b;  // BUG: returns the smaller element
}
'''

R_CLAMP = r'''template <typename T>
T clamp_to(const T& v, const T& lo, const T& hi) {
    if (v < lo) return lo;
    if (hi < v) return hi;
    return v;
}
'''

W_CLAMP = r'''template <typename T>
T clamp_to(const T& v, const T& lo, const T& hi) {
    if (v < lo) return hi;   // BUG: bounds swapped on the low branch
    if (hi < v) return hi;
    return v;
}
'''

# ---- practice cppi-p9-class-templates -----------------------------------------------
R_STACK_T = r'''#include <vector>

template <typename T>
class Stack {
public:
    void push(T value) { data_.push_back(std::move(value)); }
    T pop() {
        T out = std::move(data_.back());
        data_.pop_back();
        return out;
    }
    const T& top() const { return data_.back(); }
    bool empty() const { return data_.empty(); }
    std::size_t size() const { return data_.size(); }
private:
    std::vector<T> data_;
};
'''

W_STACK_T = r'''#include <vector>

template <typename T>
class Stack {
public:
    void push(T value) { data_.push_back(std::move(value)); }
    T pop() {
        T out = data_.back();      // BUG: copies, then pops — moves are lost
        data_.pop_back();
        return out;
    }
    const T& top() const { return data_.back(); }
    bool empty() const { return data_.empty(); }
    std::size_t size() const { return data_.size(); }
private:
    std::vector<T> data_;
};
'''

# ---- checkpoint: serializer ----------------------------------------------------------
R_SERIALIZER = r'''#include <sstream>
#include <string>
#include <vector>

template <typename T>
struct Serializer {
    static std::string to(const T& v) { return std::to_string(v); }
};

template <>
struct Serializer<std::string> {
    static std::string to(const std::string& v) { return v; }
};

template <typename T>
struct Serializer<std::vector<T>> {
    static std::string to(const std::vector<T>& v) {
        std::string out = "[";
        for (std::size_t i = 0; i < v.size(); ++i) {
            if (i) out += ",";
            out += Serializer<T>::to(v[i]);
        }
        return out + "]";
    }
};
'''

W_SERIALIZER = r'''#include <sstream>
#include <string>
#include <vector>

template <typename T>
struct Serializer {
    static std::string to(const T& v) { return std::to_string(v); }
};

template <>
struct Serializer<std::string> {
    static std::string to(const std::string& v) { return v; }
};

template <typename T>
struct Serializer<std::vector<T>> {
    static std::string to(const std::vector<T>& v) {
        std::string out = "[";
        for (std::size_t i = 0; i < v.size(); ++i) {
            out += Serializer<T>::to(v[i]);   // BUG: no comma between elements
        }
        return out + "]";
    }
};
'''

# ---- challenges -----------------------------------------------------------------------
CH_MAX_OF = challenge(
    "cppi-m9-max-of",
    "Function template: max_of",
    "Implement `template <typename T> const T& max_of(const T& a, const T& b)` returning a const reference to the larger element (ties: return either — `b` is fine). It must instantiate for int, double, and std::string alike.",
    r'''#include <string>
#include <iostream>

// template <typename T> const T& max_of(const T& a, const T& b)
''',
    [
        ("ints", 'CHECK_EQ(max_of(3, 7), 7);\nCHECK_EQ(max_of(9, 2), 9);', "Deduction picks T = int from the arguments."),
        ("doubles", 'CHECK(max_of(2.5, 1.5) > 2.49);\nCHECK(max_of(2.5, 1.5) < 2.51);', "T = double works without spelling it."),
        ("strings", 'CHECK_EQ(max_of(std::string{"apple"}, std::string{"banana"}), std::string("banana"));', "std::string has operator<, lexicographic — the contract holds."),
    ],
    level="imitation",
)

CH_CLAMP = challenge(
    "cppi-m9-clamp",
    "Function template: clamp_to",
    "Implement `template <typename T> T clamp_to(const T& v, const T& lo, const T& hi)` returning v bounded into [lo, hi]. Contract: T supports operator<. Must work for int and double.",
    r'''#include <iostream>

// template <typename T> T clamp_to(const T& v, const T& lo, const T& hi)
''',
    [
        ("in-range", 'CHECK_EQ(clamp_to(5, 1, 10), 5);', "Inside the bounds, unchanged."),
        ("below", 'CHECK_EQ(clamp_to(-3, 1, 10), 1);', "Below lo snaps to lo."),
        ("above", 'CHECK_EQ(clamp_to(42, 1, 10), 10);', "Above hi snaps to hi."),
        ("double", 'CHECK(clamp_to(0.5, 1.0, 2.0) > 0.99 && clamp_to(0.5, 1.0, 2.0) < 1.01);', "Same template, T = double."),
    ],
    level="guided",
)

CH_STACK_T = challenge(
    "cppi-m9-stack-template",
    "Class template: Stack<T>",
    "Implement `template <typename T> class Stack` backed by `std::vector<T>` with: `void push(T)`, `T pop()` (removes and returns the top — moving, not copying), `const T& top() const`, `bool empty() const`, `std::size_t size() const`. It must instantiate for int and std::string.",
    r'''#include <memory>
#include <string>
#include <vector>
#include <iostream>

// template <typename T> class Stack { ... };
''',
    [
        ("lifo-int", 'Stack<int> s;\ns.push(1);\ns.push(2);\nCHECK_EQ(s.size(), 2);\nCHECK_EQ(s.pop(), 2);\nCHECK_EQ(s.pop(), 1);', "Last pushed, first popped."),
        ("strings", 'Stack<std::string> s;\ns.push("a");\ns.push("b");\nCHECK_EQ(s.top(), std::string("b"));\ns.pop();\nCHECK_EQ(s.top(), std::string("a"));', "top() peeks without removing."),
        ("move-out", 'Stack<std::string> s;\ns.push(std::string("payload"));\nstd::string out = s.pop();\nCHECK_EQ(out, std::string("payload"));\nCHECK(s.empty());', "pop() hands the value out and leaves the stack empty."),
        ("move-only", 'Stack<std::unique_ptr<int>> s;\ns.push(std::make_unique<int>(9));\nstd::unique_ptr<int> p = s.pop();\nCHECK(p != nullptr);\nCHECK_EQ(*p, 9);\nCHECK(s.empty());', "unique_ptr is non-copyable: only a moving pop() compiles."),
    ],
    level="independent",
)

# ---- checkpoint -----------------------------------------------------------------------
CP_SERIALIZER = challenge(
    "cppi-checkpoint-templates",
    "Checkpoint: Serializer with specialization",
    "Implement `template <typename T> struct Serializer` with `static std::string to(const T&)` producing `std::to_string(v)`; a **full specialization** for `std::string` returning the string unchanged; and a **partial specialization** for `std::vector<T>` producing `\"[a,b,c]\"` (no spaces), recursively serializing elements. Nested vectors must work: a `std::vector<std::vector<int>>` serializes as `\"[[1,2],[3]]\"`.",
    r'''#include <string>
#include <vector>
#include <iostream>

// template <typename T> struct Serializer { static std::string to(const T&); };
// full spec for std::string; partial spec for std::vector<T>
''',
    [
        ("int", 'CHECK_EQ(Serializer<int>::to(42), std::string("42"));', "The primary template handles numeric types."),
        ("string", 'CHECK_EQ(Serializer<std::string>::to(std::string("hi")), std::string("hi"));', "The full specialization passes text through unchanged."),
        ("vector-int", 'CHECK_EQ(Serializer<std::vector<int>>::to({1, 2, 3}), std::string("[1,2,3]"));', "The partial specialization joins with commas."),
        ("nested", 'std::vector<std::vector<int>> v{{1, 2}, {3}};\nCHECK_EQ(Serializer<std::vector<std::vector<int>>>::to(v), std::string("[[1,2],[3]]"));', "Recursion through the generic composes the output."),
    ],
    difficulty="intermediate",
)

VI_MAX_OF = vi_challenge(
    "Function template: max_of",
    "Cài `template <typename T> const T& max_of(const T& a, const T& b)` trả reference const tới phần tử lớn hơn (hoà: trả bên nào cũng được — `b` là ổn). Nó phải instantiate được cho int, double, và std::string.",
    [
        ("ints", "Suy luận chọn T = int từ các đối số."),
        ("doubles", "T = double chạy mà không cần viết tường minh."),
        ("strings", "std::string có operator<, theo thứ tự từ điển — hợp đồng được giữ."),
    ],
)

VI_CLAMP = vi_challenge(
    "Function template: clamp_to",
    "Cài `template <typename T> T clamp_to(const T& v, const T& lo, const T& hi)` trả v bị chặn trong [lo, hi]. Hợp đồng: T hỗ trợ operator<. Phải chạy với int và double.",
    [
        ("in-range", "Trong khoảng, giữ nguyên."),
        ("below", "Dưới lo thì neo về lo."),
        ("above", "Trên hi thì neo về hi."),
        ("double", "Cùng template, T = double."),
    ],
)

VI_STACK_T = vi_challenge(
    "Class template: Stack<T>",
    "Cài `template <typename T> class Stack` dựa trên `std::vector<T>` với: `void push(T)`, `T pop()` (lấy và trả phần tử đỉnh — bằng move, không phải copy), `const T& top() const`, `bool empty() const`, `std::size_t size() const`. Phải instantiate được cho int và std::string.",
    [
        ("lifo-int", "Vào sau, ra trước."),
        ("strings", "top() nhìn.peek mà không lấy ra."),
        ("move-out", "pop() trao giá trị ra ngoài và để stack rỗng."),
        ("move-only", "unique_ptr không thể copy: chỉ pop() kiểu move mới biên dịch được."),
    ],
)

VI_CP_SERIALIZER = vi_challenge(
    "Kiểm tra điểm: Serializer với specialization",
    "Cài `template <typename T> struct Serializer` với `static std::string to(const T&)` sinh `std::to_string(v)`; một **specialization toàn phần** cho `std::string` trả chuỗi nguyên vẹn; và một **specialization riêng phần** cho `std::vector<T>` sinh `\"[a,b,c]\"` (không có dấu cách), đệ quy serialize từng phần tử. Vector lồng nhau phải chạy: `std::vector<std::vector<int>>` serialize thành `\"[[1,2],[3]]\"`.",
    [
        ("int", "Template gốc lo các kiểu số."),
        ("string", "Specialization toàn phần đưa văn bản qua nguyên vẹn."),
        ("vector-int", "Specialization riêng phần nối các phần tử bằng dấu phẩy."),
        ("nested", "Đệ quy qua bản chung tự kết hợp đầu ra."),
    ],
)

P1 = [CH_MAX_OF, CH_CLAMP]
VI_P1 = {"cppi-m9-max-of": VI_MAX_OF, "cppi-m9-clamp": VI_CLAMP}
P2 = [CH_STACK_T]
VI_P2 = {"cppi-m9-stack-template": VI_STACK_T}

# ---- emit -------------------------------------------------------------------------------
write_lesson(
    MOD, "function-templates",
    "Function Templates",
    "Deduction, implicit contracts, two-phase checking, and why templates live in headers.",
    25, L_function_templates_EN,
    "Function template",
    "Suy luận kiểu, hợp đồng ngầm định, kiểm tra hai pha, và vì sao template sống trong header.",
    L_function_templates_VI,
)
write_lesson(
    MOD, "class-templates",
    "Class Templates",
    "Parameterized types, lazy member instantiation, multiple and default parameters, CTAD, and static vs runtime polymorphism.",
    30, L_class_templates_EN,
    "Class template",
    "Kiểu được tham số hóa, instantiate member lười, tham số nhiều lớp và mặc định, CTAD, và đa hình tĩnh vs runtime.",
    L_class_templates_VI,
)
write_lesson(
    MOD, "specialization",
    "Template Specialization",
    "Full and partial specializations, compiler precedence, and recursive composition through the primary template.",
    25, L_specialization_EN,
    "Template specialization",
    "Specialization toàn phần và riêng phần, thứ tự ưu tiên của compiler, và kết hợp đệ quy qua template gốc.",
    L_specialization_VI,
)
write_lesson(
    MOD, "generic-design",
    "Designing Generic Code",
    "Concrete-first workflow, naming the contract, testing with unrelated types, and when not to template.",
    20, L_generic_design_EN,
    "Thiết kế code generic",
    "Quy trình cụ thể-trước, gọi tên hợp đồng, thử với các kiểu không liên quan, và khi nào không nên template.",
    L_generic_design_VI,
)

write_practice(
    MOD, "cppi-p9-function-templates",
    "Function template practice",
    "max_of and clamp_to — the two-recipe starter kit for generic algorithms.",
    "Luyện function template",
    "max_of và clamp_to — bộ đôi công thức mở đầu cho thuật toán generic.",
    "function-templates", 25, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m9-max-of", R_MAX_OF, W_MAX_OF),
        ("cppi-m9-clamp", R_CLAMP, W_CLAMP),
    ],
)
write_practice(
    MOD, "cppi-p9-class-templates",
    "Class template practice",
    "A move-correct Stack<T> over std::vector.",
    "Luyện class template",
    "Stack<T> move-đúng trên nền std::vector.",
    "class-templates", 30, "intermediate", P2, VI_P2,
    solutions=[
        ("cppi-m9-stack-template", R_STACK_T, W_STACK_T),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-templates",
    "Checkpoint: Serializer",
    "Primary template + full specialization + partial specialization, composed recursively for nested containers.",
    35,
    r"""
`Serializer` is the exam because it requires all three template forms in
one small system:

- the **primary** handles anything `std::to_string` accepts
- the **full specialization** for `std::string` stops numbers-only
  behavior from mangling text
- the **partial specialization** for `std::vector<T>` recurses: element
  serialization goes back through the chooser, so nested vectors compose

The recursion is the concept being tested: `Serializer<vector<T>>::to`
calls `Serializer<T>::to` without knowing what T is. That single line is
how the whole standard library composes.

Watch the exact output format: `[1,2,3]` — no spaces, brackets included.
Off-by-one separators are the classic specialization bug.
""",
    "Kiểm tra điểm: Serializer",
    "Template gốc + specialization toàn phần + riêng phần, kết hợp đệ quy cho container lồng nhau.",
    r"""
`Serializer` là bài kiểm tra vì nó đòi hỏi cả ba dạng template trong một hệ
thống nhỏ:

- **bản gốc** xử lý mọi thứ `std::to_string` nhận được
- **specialization toàn phần** cho `std::string` ngăn hành vi chỉ-số-hủy
  làm hỏng văn bản
- **specialization riêng phần** cho `std::vector<T>` đệ quy: serialize
  phần tử quay lại bộ chọn, nên vector lồng nhau tự kết hợp

Đệ quy là khái niệm được kiểm tra: `Serializer<vector<T>>::to` gọi
`Serializer<T>::to` mà không cần biết T là gì. Một dòng đó là cách toàn bộ
thư viện chuẩn kết hợp với nhau.

Chú ý định dạng đầu ra chính xác: `[1,2,3]` — không dấu cách, đủ dấu ngoặc.
Sai lệch dấu phân cách là bug kinh điển của specialization.
""",
    CP_SERIALIZER, VI_CP_SERIALIZER,
    solution=R_SERIALIZER, wrong=W_SERIALIZER,
)

write_module(
    MOD,
    "Templates",
    "Generic programming: function and class templates, deduction and contracts, full and partial specialization, and a workflow for designing your own.",
    "Template",
    "Lập trình generic: function và class template, suy luận và hợp đồng, specialization toàn phần và riêng phần, và quy trình tự thiết kế.",
    ["function-templates", "class-templates", "specialization", "generic-design", "advanced-checkpoint-templates"],
    ["cppi-p9-function-templates", "cppi-p9-class-templates"],
)
print("module 9 emitted")
