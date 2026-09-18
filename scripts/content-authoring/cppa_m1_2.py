#!/usr/bin/env python3
"""C++ Advanced — module 1 (object-model) and module 2 (move-forwarding)."""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# Shared instrumented type: counters prove copy/move behavior in graded checks.
COUNTER_BOILER = r'''#include <cstddef>
#include <string>
#include <utility>

// Instrumented type: counts copies and moves for the graded checks.
struct Tracked {
    static inline int copies = 0;
    static inline int moves = 0;
    std::string tag;
    Tracked() : tag("empty") {}
    explicit Tracked(std::string t) : tag(std::move(t)) {}
    Tracked(const Tracked& o) : tag(o.tag) { ++copies; }
    Tracked(Tracked&& o) noexcept : tag(std::move(o.tag)) { ++moves; }
    Tracked& operator=(const Tracked& o) { tag = o.tag; ++copies; return *this; }
    Tracked& operator=(Tracked&& o) noexcept { tag = std::move(o.tag); ++moves; return *this; }
};
'''

# ============================ MODULE 1: object-model ============================
M1 = "object-model"

L1A = "value-categories"
L1B = "storage-duration-lifetime"
L1C = "initialization-subtleties"
L1D = "cppa-checkpoint-object-model"

write_module(
    M1,
    "The Advanced Object Model",
    "Value categories, storage duration, and initialization — the machinery every other advanced topic is defined in terms of. You will predict exact behavior before running anything.",
    "Mô hình đối tượng nâng cao",
    "Phân loại giá trị, thời gian lưu trữ và khởi tạo — nền móng cho mọi chủ đề nâng cao khác. Bạn sẽ dự đoán hành vi chính xác trước khi chạy.",
    [L1A, L1B, L1C, L1D],
    ["m1-categories-practice", "m1-lifetime-practice", "m1-init-practice"],
)

write_lesson(
    M1, L1A,
    "Value Categories: lvalue, xvalue, prvalue",
    "Every expression is an lvalue, an xvalue, or a prvalue. Mastering the taxonomy explains moves, overloading, and half of the compiler errors you will meet.",
    10,
    r'''
Every **expression** in C++ has two independent properties: a *type*, and a *value category*. The category answers one question: **what does this expression refer to, and can I reuse it?**

## The three categories

- **lvalue** — has identity, *can* be reused: a named variable, a dereferenced pointer, a function returning `T&`.
- **xvalue** ("expiring") — has identity, but *marks it as reusable*: `std::move(x)`, a function returning `T&&`, a member of an xvalue.
- **prvalue** ("pure") — no identity yet, just a value being born: literals, `T{...}`, a function returning `T` by value.

lvalues + xvalues are **glvalues** (they designate an object). xvalues + prvalues are **rvalues** (they can be moved from).

```cpp
std::string a = "hi";        // 'a' is an lvalue
std::move(a);                // std::move(a) is an xvalue
std::string(3, '?');         // prvalue
a + "!";                     // prvalue (operator+ returns by value)
```

## Why the taxonomy exists

Overload resolution cares: `f(T&)` beats `f(T&&)` for lvalues, and `f(T&&)` is *viable* only for rvalues. That is the entire mechanism behind move-on-return, `emplace_back`, and forwarding. `std::move` does not move anything — it is a **cast to xvalue**: "here is identity, please cannibalize it."

## Reading categories out of types with decltype

The standard gives you a probe: for an expression `e`, `decltype((e))` is:
- `T&` if `e` is an lvalue,
- `T&&` if `e` is an xvalue,
- `T` if `e` is a prvalue.

```cpp
static_assert(std::is_same_v<decltype((a)), std::string&>);             // lvalue
static_assert(std::is_same_v<decltype((std::move(a))), std::string&&>); // xvalue
static_assert(std::is_same_v<decltype((a + "!")), std::string>);        // prvalue
```

(Plain `decltype(a)` names the *declared* type; the double parentheses make decltype treat it as an expression.)

## The two classic traps

**Trap 1 — named rvalue references are lvalues.** Inside `void f(T&& x)`, the expression `x` is an lvalue (it has a name!). Passing it on, assigning it, or storing it copies unless you `std::forward`/`std::move` it. One place the compiler compensates: the bare statement `return x;` performs an *implicit move* for rvalue-reference parameters (C++20 P1825) — a convenience, not a rule to lean on. Everywhere else, forward explicitly.

**Trap 2 — rvalue-ness does not mean modifiable.** A `const T&&` parameter binds rvalues but cannot be moved from; some APIs use it deliberately to *reject* moves.

**Practice discipline for this module:** before each exercise, *write down* the category you expect. The graded checks use `decltype` probes — the same tool you will use in code review.
''',
    "Giá trị biểu thức: lvalue, xvalue, prvalue",
    "Mỗi biểu thức đều là lvalue, xvalue hoặc prvalue. Nắm vững hệ thống này sẽ giải thích move, overload và một nửa số lỗi compiler bạn gặp.",
    r'''
Mỗi **biểu thức** trong C++ có hai thuộc tính độc lập: *kiểu* (type) và *phân loại giá trị* (value category). Phân loại trả lời một câu hỏi: **biểu thức này tham chiếu đến cái gì, và tôi có thể tái sử dụng nó không?**

## Ba phân loại

- **lvalue** — có định danh, *có thể* tái sử dụng: biến có tên, biểu thức `*p`, hàm trả về `T&`.
- **xvalue** ("expiring") — có định danh nhưng *đánh dấu là có thể lấy tài nguyên*: `std::move(x)`, hàm trả về `T&&`, thành viên của một xvalue.
- **prvalue** ("pure") — chưa có định danh, chỉ là một giá trị đang được sinh ra: literal, `T{...}`, hàm trả về `T` theo giá trị.

lvalue + xvalue là **glvalue** (chỉ đến một đối tượng). xvalue + prvalue là **rvalue** (có thể move).

```cpp
std::string a = "hi";        // 'a' là lvalue
std::move(a);                // std::move(a) là xvalue
std::string(3, '?');         // prvalue
a + "!";                     // prvalue (operator+ trả về theo giá trị)
```

## Vì sao có hệ thống này

Overload resolution quan tâm đến nó: `f(T&)` thắng `f(T&&)` với lvalue, còn `f(T&&)` chỉ *khả dụng* với rvalue. Đó là toàn bộ cơ chế phía sau move-on-return, `emplace_back` và forwarding. `std::move` không move bất cứ thứ gì — nó là một **cast sang xvalue**: "đây là định danh, hãy mổ xẻ nó."

## Đọc phân loại từ kiểu bằng decltype

Chuẩn cung cấp công cụ: với biểu thức `e`, `decltype((e))` là:
- `T&` nếu `e` là lvalue,
- `T&&` nếu `e` là xvalue,
- `T` nếu `e` là prvalue.

```cpp
static_assert(std::is_same_v<decltype((a)), std::string&>);             // lvalue
static_assert(std::is_same_v<decltype((std::move(a))), std::string&&>); // xvalue
static_assert(std::is_same_v<decltype((a + "!")), std::string>);        // prvalue
```

(`decltype(a)` đơn thuần là kiểu *khai báo*; thêm ngoặc kép để decltype coi nó là biểu thức.)

## Hai bẫy kinh điển

**Bẫy 1 — rvalue reference có tên là lvalue.** Bên trong `void f(T&& x)`, biểu thức `x` là lvalue (nó có tên!). Khi chuyển tiếp, gán hay lưu trữ, nó sẽ bị copy nếu bạn không dùng `std::forward`/`std::move`. Một chỗ compiler tự bù: câu lệnh trơn `return x;` thực hiện *implicit move* cho tham số rvalue reference (C++20 P1825) — đó là tiện lợi, không phải quy tắc để dựa vào. Ở mọi nơi khác, hãy forward tường minh.

**Bẫy 2 — rvalue không có nghĩa là sửa được.** Tham số `const T&&` buộc được rvalue nhưng không thể move; một số API dùng nó có chủ đích để *từ chối* move.

**Kỷ luật luyện tập:** trước mỗi bài tập, *viết ra* phân loại bạn dự đoán. Các bài kiểm tra dùng probe `decltype` — đúng công cụ bạn sẽ dùng khi review code.
''',
    difficulty="advanced",
)

write_lesson(
    M1, L1B,
    "Storage Duration, Lifetime, and Dangling",
    "Static, thread, automatic, dynamic — four clocks that decide when objects live and die. Most catastrophic C++ bugs are lifetime bugs in disguise.",
    11,
    r'''
Every object lives on one of four **storage durations** — four different clocks:

1. **static** — created at program start, destroyed at exit: globals, `static` locals, `static` members. Initialization of function-local statics is thread-safe and lazy (C++11 "magic statics").
2. **thread** — `thread_local`: one instance per thread, born at thread start, dies at thread end.
3. **automatic** — locals: born at definition, destroyed when the scope exits (in **reverse order** of declaration).
4. **dynamic** — `new`/`delete` directly (rare in modern code; ownership should live in RAII types).

## Destruction order is a contract

Within a scope, destruction runs in **reverse construction order**. Members are destroyed in reverse declaration order — *after* the destructor body runs. Locking discipline, mutex scoping, and cleanup code all depend on this:

```cpp
struct Job {
    std::ofstream log;              // declared first  -> destroyed last
    std::lock_guard<std::mutex> g;  // declared second -> destroyed first
    Job(std::mutex& m) : log("job.log"), g(m) {}
};
```

## Dangling: the lifetime bug family

A reference/pointer/view that outlives its object is **dangling** — using it is undefined behavior, and the compiler usually will not stop you:

- returning a reference/pointer to a local,
- storing a `string_view` or `span` over a temporary,
- iterators invalidated by container mutation,
- captured-by-reference lambdas escaping their scope.

```cpp
std::string_view bad() {
    std::string local = "temporary";
    return local;            // compiles; the view dangles on return
}
```

## Lifetime extension — the narrow exception

A **const reference bound to a temporary** extends the temporary's lifetime to the reference's (and a range-for over a temporary container works for the loop's duration). But extension does **not** chain through function returns or past a constructor body into a reference member — the most-surveyed "gotcha" in C++:

```cpp
struct Holder {
    const std::string& s;
    Holder() : s("dangles!") {}   // temporary dies at the closing brace
};
```

**Defensive habit:** views borrow — never store a `string_view`/`span`/`&` in a type whose lifetime you cannot prove is shorter than the viewed object's. In this module's graded work you will repair dangling code and predict destruction order exactly.
''',
    "Thời gian lưu trữ, vòng đời và dangling",
    "Static, thread, automatic, dynamic — bốn chiếc đồng hồ quyết định đối tượng sống và chết khi nào. Phần lớn lỗi nghiêm trọng trong C++ đều là lỗi vòng đời.",
    r'''
Mỗi đối tượng tồn tại theo một trong bốn **storage duration** — bốn chiếc đồng hồ khác nhau:

1. **static** — sinh lúc chương trình khởi động, chết khi thoát: biến toàn cục, `static` cục bộ, thành viên `static`. Khởi tạo static cục bộ là thread-safe và lười (C++11 "magic statics").
2. **thread** — `thread_local`: một thực thể mỗi thread, sinh lúc thread bắt đầu, chết khi thread kết thúc.
3. **automatic** — biến cục bộ: sinh tại dòng khai báo, bị hủy khi ra khỏi phạm vi (theo **thứ tự ngược**).
4. **dynamic** — `new`/`delete` trực tiếp (hiếm trong code hiện đại; quyền sở hữu nên nằm trong các kiểu RAII).

## Thứ tự hủy là một hợp đồng

Trong cùng phạm vi, hủy chạy theo **thứ tự khai báo ngược**. Thành viên bị hủy theo thứ tự khai báo ngược — *sau* phần thân destructor. Cơ chế khóa, phạm vi mutex và mã dọn dẹp đều dựa vào điều này:

```cpp
struct Job {
    std::ofstream log;              // khai báo trước  -> hủy sau
    std::lock_guard<std::mutex> g;  // khai báo sau    -> hủy trước
    Job(std::mutex& m) : log("job.log"), g(m) {}
};
```

## Dangling: họ lỗi vòng đời

Một reference/pointer/view sống lâu hơn đối tượng của nó là **dangling** — sử dụng nó là hành vi không xác định, và compiler thường không cản bạn:

- trả về reference/pointer trỏ vào biến cục bộ,
- lưu `string_view` hoặc `span` trỏ vào một đối tượng tạm,
- iterator bị vô hiệu sau khi container thay đổi,
- lambda bắt theo reference nhưng sống ngoài phạm vi.

```cpp
std::string_view bad() {
    std::string local = "temporary";
    return local;            // biên dịch được; view sẽ dangling khi return
}
```

## Lifetime extension — ngoại lệ hẹp

**const reference buộc vào một đối tượng tạm** sẽ kéo dài đời đối tượng tạm bằng đời reference (và range-for trên container tạm cũng sống trong suốt vòng lặp). Nhưng cơ chế này **không** chuyển tiếp qua return của hàm hay qua member initializer vào thành viên reference sau thân constructor — bẫy nổi tiếng nhất của C++:

```cpp
struct Holder {
    const std::string& s;
    Holder() : s("dangles!") {}   // đối tượng tạm chết ngay tại dấu }
};
```

**Thói quen phòng thủ:** view là mượn — đừng bao giờ lưu `string_view`/`span`/`&` trong một kiểu mà bạn không chứng minh được nó chết *trước* đối tượng bị mượn. Trong phần luyện tập bạn sẽ sửa code dangling và dự đoán thứ tự hủy chính xác từng bước.
''',
    difficulty="advanced",
)

write_lesson(
    M1, L1C,
    "Initialization Subtleties",
    "Copy-init vs direct-init vs list-init, the most-vexing-parse, brace narrowing, and default member initializers — small syntax differences with real consequences.",
    10,
    r'''
C++ has ~17 forms of initialization grouped into a few families. Four matter daily:

## Direct vs copy vs list

```cpp
std::string a("x");     // direct-initialization
std::string b = "x";    // copy-initialization: explicit constructors are OFF limits
std::string c{"x"};     // direct-list-initialization
std::string d = {"x"};  // copy-list-initialization
```

Copy-initialization cannot call an `explicit` constructor — that keyword is how types opt out of surprising implicit conversions. The flip side matters for overload design: a greedy forwarding constructor only hijacks **direct** initialization (`Tracked c{b};`), never copy initialization (`Tracked c = b;`).

## The most vexing parse

`Timer t(Log());` declares a **function** `t` returning `Timer`, taking a function returning `Log`. Braces disambiguate: `Timer t(Log{});` constructs.

## Narrowing in braces

Braces **forbid** narrowing conversions — the safe default:

```cpp
int x{3.9};     // error: narrowing
int y = 3.9;    // compiles: y == 3, silently
```

## Default member initializers and initialization order

Members initialize in **declaration order**, not initializer-list order — `-Wreorder` catches the mismatch. Default member initializers centralize defaults while constructors can still override:

```cpp
struct Session {
    std::chrono::steady_clock::time_point start{std::chrono::steady_clock::now()};
    int retries{0};
    explicit Session(int r) : retries{r} {}   // declaration order: start first
};
```

**Grading note:** the checks in this module use brace-initialization traps and `static_assert` on constructed types. Predict first, then let the compiler grade you.
''',
    "Những điều tinh tế về khởi tạo",
    "Khởi tạo sao chép vs trực tiếp vs bằng ngoặc nhọn, most-vexing-parse, narrowing và default member initializer — khác biệt cú pháp nhỏ, hệ quả thật.",
    r'''
C++ có khoảng 17 dạng khởi tạo gom vào vài nhóm. Bốn nhóm dùng hằng ngày:

## Trực tiếp vs sao chép vs ngoặc nhọn

```cpp
std::string a("x");     // direct-initialization
std::string b = "x";    // copy-initialization: không được dùng constructor explicit
std::string c{"x"};     // direct-list-initialization
std::string d = {"x"};  // copy-list-initialization
```

Copy-initialization không thể gọi constructor `explicit` — chính từ khóa `explicit` giúp kiểu từ chối các chuyển đổi ngầm gây bất ngờ. Mặt còn lại quan trọng cho thiết kế overload: một constructor forwarding tham lam chỉ cướp **direct** initialization (`Tracked c{b};`), không bao giờ cướp copy initialization (`Tracked c = b;`).

## Most vexing parse

`Timer t(Log());` khai báo một **hàm** `t` trả về `Timer`, nhận một hàm trả về `Log`. Ngoặc nhọn gỡ nhầm lẫn: `Timer t(Log{});` mới là tạo đối tượng.

## Narrowing với ngoặc nhọn

Ngoặc nhọn **cấm** thu hẹp kiểu — mặc định an toàn:

```cpp
int x{3.9};     // lỗi: narrowing
int y = 3.9;    // biên dịch được: y == 3, lặng lẽ
```

## Default member initializer và thứ tự khởi tạo

Thành viên được khởi tạo theo **thứ tự khai báo**, không phải thứ tự trong initializer list — `-Wreorder` bắt lỗi lệch pha. Default member initializer tập trung giá trị mặc định trong khi constructor vẫn ghi đè được:

```cpp
struct Session {
    std::chrono::steady_clock::time_point start{std::chrono::steady_clock::now()};
    int retries{0};
    explicit Session(int r) : retries{r} {}   // theo thứ tự khai báo: start trước
};
```

**Ghi chú chấm điểm:** các bài kiểm tra dùng bẫy ngoặc nhọn và `static_assert` trên kiểu được tạo. Hãy dự đoán trước, rồi để compiler chấm.
''',
    difficulty="advanced",
)

# ---- module 1 practices ----
CH_PREDICT_CAT = challenge(
    "cppa1-predict-category",
    "Land Each Call in Its Category",
    "Implement the three probe functions. The tests prove each call expression's value category with `decltype((expr))`.",
    r'''#include <string>
#include <utility>
#include <type_traits>

// Implement the three probe functions so every static_assert passes.
std::string makeGreeting();                 // (1) its call must be a prvalue
std::string& lvalueRef();                   // (2) its call must be an lvalue
std::string&& xvalueRef(std::string& s);    // (3) its call must be an xvalue
''',
    [
        ("makeGreeting is a prvalue",
         r'''static_assert(std::is_same_v<decltype((makeGreeting())), std::string>, "prvalue: plain T");
static_assert(!std::is_reference_v<decltype((makeGreeting()))>, "prvalue is not a reference");
CHECK_CONTAINS(makeGreeting(), "Hello");''',
         "A prvalue's decltype((e)) is the plain type T — no reference. Return a std::string by value."),
        ("lvalueRef is an lvalue",
         r'''static_assert(std::is_lvalue_reference_v<decltype((lvalueRef()))>, "lvalue: T&");
static_assert(!std::is_rvalue_reference_v<decltype((lvalueRef()))>, "not an xvalue");
lvalueRef() += " from ref";''',
         "Return std::string& bound to an object that outlives the call — a function-local static works."),
        ("xvalueRef is an xvalue",
         r'''std::string base = "payload";
static_assert(std::is_rvalue_reference_v<decltype((xvalueRef(base)))>, "xvalue: T&&");
CHECK_EQ(xvalueRef(base), std::string("payload"));''',
         "Return std::string&& — a function returning T&& produces an xvalue. std::move(s) inside does it."),
    ],
    difficulty="advanced",
)

VI_PREDICT_CAT = vi_challenge(
    "Đưa mỗi lời gọi vào đúng phân loại",
    "Cài đặt ba hàm probe. Bài kiểm tra chứng minh phân loại giá trị của mỗi biểu thức gọi bằng `decltype((expr))`.",
    [
        ("makeGreeting là prvalue", "decltype((e)) của prvalue là kiểu T trơn — không phải reference. Hãy trả về std::string theo giá trị."),
        ("lvalueRef là lvalue", "Trả về std::string& buộc vào một đối tượng sống lâu hơn lời gọi — static cục bộ là lựa chọn hợp lệ."),
        ("xvalueRef là xvalue", "Trả về std::string&& — hàm trả về T&& tạo ra xvalue. std::move(s) bên trong là đủ."),
    ],
)

NAMED_RVAL_BOILER = r'''#include <cstddef>
#include <string>
#include <utility>

// Instrumented payload: the counters observe what passOn really does.
struct Tracked {
    static inline int copies = 0;
    static inline int moves = 0;
    std::string tag;
    explicit Tracked(std::string t) : tag(std::move(t)) {}
    Tracked(const Tracked& o) : tag(o.tag) { ++copies; }
    Tracked(Tracked&& o) noexcept : tag(std::move(o.tag)) { ++moves; }
};

Tracked passOn(Tracked&& payload);   // TODO: move it onward, not copy
std::size_t consumeTwice(std::string&& payload);
'''

CH_NAMED_RVAL = challenge(
    "cppa1-named-rvalue-is-lvalue",
    "The Named-Rvalue Trap",
    "A forwarding function receives `Tracked&& payload`. Return it onward *as an rvalue* so exactly one move happens and no copy — the counters observe what you really did.",
    NAMED_RVAL_BOILER,
    [
        ("passOn moves, not copies",
         r'''Tracked::moves = 0; Tracked::copies = 0;
Tracked out = passOn(Tracked("abc"));
CHECK_EQ(Tracked::moves, 1);
CHECK_EQ(Tracked::copies, 0);
CHECK_EQ(out.tag, std::string("abc"));''',
         "Inside the function the parameter has a name, so it is an lvalue. Return std::move(payload) — returning the bare name performs a COPY of a Tracked."),
        ("consumeTwice returns by value",
         r'''std::size_t n = consumeTwice(std::string(5, 'z'));
CHECK_EQ(n, std::size_t{5});''',
         "Take the parameter by rvalue reference, use its size, and return the size by value — the string itself dies at return."),
    ],
    difficulty="advanced",
)

VI_NAMED_RVAL = vi_challenge(
    "Bẫy rvalue có tên",
    "Một hàm forwarding nhận `Tracked&& payload`. Hãy trả nó đi tiếp *dưới dạng rvalue* để đúng một lần move xảy ra và không hề copy — bộ đếm sẽ quan sát những gì bạn thật sự làm.",
    [
        ("passOn move chứ không copy", "Bên trong hàm, tham số có tên nên là lvalue. Return std::move(payload) — nếu return tên trơn, Tracked sẽ bị COPY."),
        ("consumeTwice trả theo giá trị", "Nhận tham số bằng rvalue reference, lấy size rồi trả size theo giá trị — chuỗi gốc chết khi return."),
    ],
)

CH_CONST_RVAL = challenge(
    "cppa1-const-rvalue-rejects-move",
    "A const rvalue cannot be moved from",
    "Implement `std::string concat(const std::string& a, const std::string& b)` returning the concatenation **by value**, and `std::string sabotage(const std::string&& a, const std::string&& b)` that must still produce `a + b` even though its parameters are const rvalues.",
    r'''#include <string>

std::string concat(const std::string& a, const std::string& b);

std::string sabotage(const std::string&& a, const std::string&& b);
''',
    [
        ("concat returns by value",
         r'''std::string x = concat("ab", "cd");
CHECK_EQ(x, std::string("abcd"));''',
         "operator+ already returns by value: return a + b;"),
        ("const rvalues are still readable",
         r'''std::string y = sabotage(std::string("xy"), std::string("zw"));
CHECK_EQ(y, std::string("xyzw"));''',
         "const T&& cannot be moved from, but it can be read: return a + b; compiles and copies — that is the point of the trap."),
    ],
    difficulty="advanced",
)

VI_CONST_RVAL = vi_challenge(
    "const rvalue không thể move",
    "Cài đặt `std::string concat(const std::string& a, const std::string& b)` trả về phép nối **theo giá trị**, và `std::string sabotage(const std::string&& a, const std::string&& b)` vẫn phải tạo `a + b` dù tham số là const rvalue.",
    [
        ("concat trả theo giá trị", "operator+ đã trả theo giá trị: return a + b;"),
        ("const rvalue vẫn đọc được", "const T&& không move được nhưng đọc được: return a + b; biên dịch và copy — đó chính là điểm của cái bẫy."),
    ],
)

M1_PRAC1 = dict(
    sid="m1-categories-practice",
    title="Predict the Category",
    description="Three challenges where you define functions whose call expressions land in exactly the right value category — verified with decltype probes, the tool professionals use.",
    vi_title="Dự đoán phân loại giá trị",
    vi_description="Ba thử thách: định nghĩa các hàm sao cho biểu thức gọi rơi đúng phân loại giá trị — kiểm chứng bằng probe decltype.",
    after_lesson=L1A,
    minutes=22,
    difficulty="advanced",
)

M1_PRAC1_CH = [CH_PREDICT_CAT, CH_NAMED_RVAL, CH_CONST_RVAL]
M1_PRAC1_VI = {"cppa1-predict-category": VI_PREDICT_CAT,
               "cppa1-named-rvalue-is-lvalue": VI_NAMED_RVAL,
               "cppa1-const-rvalue-rejects-move": VI_CONST_RVAL}

M1_PRAC1_SOL = [
    ("cppa1-predict-category",
     r'''#include <string>
#include <utility>
#include <type_traits>

std::string makeGreeting() { return "Hello"; }
std::string& lvalueRef() { static std::string s = "base"; return s; }
std::string&& xvalueRef(std::string& s) { return std::move(s); }
''',
     r'''#include <string>
#include <utility>
#include <type_traits>

std::string makeGreeting() { return "Hello"; }
std::string&& lvalueRef() { static std::string s = "base"; return std::move(s); }  // WRONG: category flipped
std::string& xvalueRef(std::string& s) { return s; }  // WRONG: category flipped
'''),
    ("cppa1-named-rvalue-is-lvalue",
     NAMED_RVAL_BOILER + "\nTracked passOn(Tracked&& payload) { return std::move(payload); }\nstd::size_t consumeTwice(std::string&& payload) { std::string taken = std::move(payload); return taken.size(); }\n",
     NAMED_RVAL_BOILER + "\nTracked passOn(Tracked&& payload) { Tracked out = payload; return out; }  // WRONG: copies once, then moves the copy\nstd::size_t consumeTwice(std::string&& payload) { return payload.size(); }\n"),
    ("cppa1-const-rvalue-rejects-move",
     r'''#include <string>

std::string concat(const std::string& a, const std::string& b) { return a + b; }
std::string sabotage(const std::string&& a, const std::string&& b) { return a + b; }
''',
     r'''#include <string>

std::string concat(const std::string& a, const std::string& b) { return a + "c"; }  // WRONG: drops b
std::string sabotage(const std::string&& a, const std::string&& b) { return a; }    // WRONG: drops b
'''),
]

write_practice(M1, **M1_PRAC1, challenges=M1_PRAC1_CH, vi_challenges=M1_PRAC1_VI, solutions=M1_PRAC1_SOL)

# ---- lifetime practice ----
CH_STABLE_VIEW = challenge(
    "cppa1-static-outlives-view",
    "A View Must Outlive Its Source",
    "Implement `stableView` so the returned `string_view` is still valid when the test inspects it, and fix `danglingView` so it returns a view over storage that lives long enough.",
    r'''#include <string>
#include <string_view>

// Return a view over characters that outlive the call.
std::string_view stableView();

// Return a view over characters that outlive the call (repair the idea).
std::string_view danglingView();
''',
    [
        ("stableView is valid after return",
         r'''std::string v(stableView());
CHECK_CONTAINS(v, "durable");''',
         "A view over a function-local static, a string literal, or dynamic storage survives the return. A view over an automatic local does not."),
        ("danglingView repaired",
         r'''std::string w(danglingView());
CHECK_CONTAINS(w, "persist");''',
         "Give the backing string static storage duration (static std::string) or return dynamic storage — anything whose lifetime continues after the return."),
    ],
    difficulty="advanced",
)

VI_STABLE_VIEW = vi_challenge(
    "View phải sống lâu hơn nguồn",
    "Cài đặt `stableView` để `string_view` trả về vẫn hợp lệ khi kiểm tra, và sửa `danglingView` để nó trả về view trỏ vào bộ nhớ sống đủ lâu.",
    [
        ("stableView hợp lệ sau return", "View trỏ vào static cục bộ, string literal hay bộ nhớ động sẽ sống qua lời return. View trỏ vào biến cục bộ thì không."),
        ("danglingView đã sửa", "Cho chuỗi nền thời gian lưu trữ static (static std::string) hoặc trả về bộ nhớ động — bất cứ thứ gì còn sống sau return."),
    ],
)

CH_DESTRUCTION_ORDER = challenge(
    "cppa1-destruction-order",
    "Predict Destruction Order",
    "Implement `teardownOrder(int n)` returning the destruction order of n guard objects numbered 1..n constructed in order inside one scope, as a comma-joined string like \"3,2,1\".",
    r'''#include <string>

// Objects 1..n are constructed in order inside one scope.
// Return their destruction order as comma-joined numbers.
std::string teardownOrder(int n);
''',
    [
        ("reverse order",
         r'''CHECK_EQ(teardownOrder(3), std::string("3,2,1"));
CHECK_EQ(teardownOrder(5), std::string("5,4,3,2,1"));''',
         "Within a scope, destruction runs in reverse construction order."),
        ("single object",
         r'''CHECK_EQ(teardownOrder(1), std::string("1"));''',
         "n == 1 is just \"1\" — no reversal visible."),
    ],
    difficulty="advanced",
)

VI_DESTRUCTION_ORDER = vi_challenge(
    "Dự đoán thứ tự hủy",
    "Cài đặt `teardownOrder(int n)` trả về thứ tự hủy của n đối tượng guard đánh số 1..n được tạo theo thứ tự trong cùng một phạm vi, dạng chuỗi nối dấu phẩy như \"3,2,1\".",
    [
        ("thứ tự ngược", "Trong cùng phạm vi, hủy chạy theo thứ tự tạo ngược lại."),
        ("một đối tượng", "n == 1 thì chỉ là \"1\" — không thấy phép đảo."),
    ],
)

CH_TEMP_LIFETIME = challenge(
    "cppa1-lifetime-extension",
    "Lifetime Extension — and Where It Fails",
    "Returning a reference to a temporary can never be safe, so `extended()` must back its reference with *static* storage. And `holderTrap()` returns the value a correct `Holder` would have captured **by value** instead of by reference.",
    r'''#include <string>

// Return content that remains valid after the call: back it with static storage.
const std::string& extended();

// Simulate Holder { const std::string& s; Holder() : s("dangles!") {} }
// by returning the value the constructor *copied* into safety.
std::string holderTrap();
''',
    [
        ("extended stays valid",
         r'''const std::string& e = extended();
CHECK_CONTAINS(e, "static");''',
         "Only static/dynamic storage survives; return a reference to a function-local static string containing \"static\"."),
        ("holderTrap returns the salvageable value",
         r'''std::string t = holderTrap();
CHECK_CONTAINS(t, "salvaged");''',
         "Copy the temporary into a return value — return std::string(\"salvaged ...\"); — that is what a correct Holder does with a value member instead of a reference."),
    ],
    difficulty="advanced",
)

VI_TEMP_LIFETIME = vi_challenge(
    "Lifetime extension — và chỗ nó thất bại",
    "Trả về reference vào đối tượng tạm không bao giờ an toàn, nên `extended()` phải đặt reference trên bộ nhớ *static*. Và `holderTrap()` trả về giá trị mà một `Holder` đúng đắn sẽ giữ **bằng giá trị** thay vì bằng reference.",
    [
        ("extended vẫn hợp lệ", "Chỉ static/dynamic sống sót; trả về reference đến chuỗi static cục bộ chứa \"static\"."),
        ("holderTrap trả giá trị được cứu", "Copy đối tượng tạm vào giá trị trả về — return std::string(\"salvaged ...\"); — đó là điều một Holder đúng đắn làm với thành viên giá trị thay vì reference."),
    ],
)

M1_PRAC2 = dict(
    sid="m1-lifetime-practice",
    title="Lifetime Clinic",
    description="Repair dangling views, predict destruction order, and learn exactly where lifetime extension stops working.",
    vi_title="Phòng khám vòng đời",
    vi_description="Sửa view dangling, dự đoán thứ tự hủy, và tìm hiểu chính xác lifetime extension dừng ở đâu.",
    after_lesson=L1B,
    minutes=20,
    difficulty="advanced",
)

M1_PRAC2_CH = [CH_STABLE_VIEW, CH_DESTRUCTION_ORDER, CH_TEMP_LIFETIME]
M1_PRAC2_VI = {"cppa1-static-outlives-view": VI_STABLE_VIEW,
               "cppa1-destruction-order": VI_DESTRUCTION_ORDER,
               "cppa1-lifetime-extension": VI_TEMP_LIFETIME}

M1_PRAC2_SOL = [
    ("cppa1-static-outlives-view",
     r'''#include <string>
#include <string_view>

std::string_view stableView() { static const std::string s = "durable static storage"; return s; }
std::string_view danglingView() { static const std::string s = "persist forever"; return s; }
''',
     r'''#include <string>
#include <string_view>

std::string_view stableView() { return std::string_view("wrong storage"); }   // WRONG: never contains "durable"
std::string_view danglingView() { return std::string_view("also wrong"); }    // WRONG: never contains "persist"
'''),
    ("cppa1-destruction-order",
     r'''#include <string>

std::string teardownOrder(int n) {
    std::string out;
    for (int i = n; i >= 1; --i) { if (!out.empty()) out += ','; out += std::to_string(i); }
    return out;
}
''',
     r'''#include <string>

std::string teardownOrder(int n) {
    std::string out;
    for (int i = 1; i <= n; ++i) { if (!out.empty()) out += ','; out += std::to_string(i); }  // WRONG: forward order
    return out;
}
'''),
    ("cppa1-lifetime-extension",
     r'''#include <string>

const std::string& extended() { static const std::string s = "static backing storage"; return s; }
std::string holderTrap() { return std::string("salvaged copy of the temporary"); }
''',
     r'''#include <string>

const std::string& extended() { static const std::string s = "temporary backing storage"; return s; }  // WRONG: no "static" in content
std::string holderTrap() { return "lost the value"; }  // WRONG: no "salvaged" in content
'''),
]

write_practice(M1, **M1_PRAC2, challenges=M1_PRAC2_CH, vi_challenges=M1_PRAC2_VI, solutions=M1_PRAC2_SOL)

# ---- init practice ----
CH_INIT_NARROW = challenge(
    "cppa1-init-narrowing",
    "Braces Reject Narrowing",
    "Complete `Config` with `name` (std::string, default \"unset\"), `port` (int, default 0), and `tags` (vector<string>, default empty), then implement `int truncateToInt(double d)` that compiles **only** because it avoids brace narrowing.",
    r'''#include <string>
#include <vector>

struct Config {
    // TODO: add the three members with default member initializers
};

int truncateToInt(double d);   // must not use braces around d
''',
    [
        ("defaults apply",
         r'''Config c;
CHECK_EQ(c.name, std::string("unset"));
CHECK_EQ(c.port, 0);
CHECK_EQ(c.tags.size(), std::size_t{0});''',
         "Default member initializers: std::string name{\"unset\"}; int port{0}; std::vector<std::string> tags{};"),
        ("list-init with values",
         r'''Config c{"api", 8080, {"a", "b"}};
CHECK_EQ(c.port, 8080);
CHECK_EQ(c.tags.size(), std::size_t{2});''',
         "Brace/aggregate initialization sets every member in declaration order."),
        ("truncate avoids narrowing",
         r'''CHECK_EQ(truncateToInt(3.9), 3);
CHECK_EQ(truncateToInt(-1.5), -1);''',
         "static_cast<int>(d) — the explicit cast is the honest way to narrow without braces."),
    ],
    difficulty="advanced",
)

VI_INIT_NARROW = vi_challenge(
    "Ngoặc nhọn cấm thu hẹp",
    "Hoàn thiện `Config` với `name` (std::string, mặc định \"unset\"), `port` (int, mặc định 0) và `tags` (vector<string>, mặc định rỗng), rồi cài `int truncateToInt(double d)` biên dịch được chỉ vì nó tránh narrowing của ngoặc nhọn.",
    [
        ("mặc định được áp dụng", "Default member initializer: std::string name{\"unset\"}; int port{0}; std::vector<std::string> tags{};"),
        ("list-init có giá trị", "Khởi tạo bằng ngoặc nhọn/aggregate gán từng thành viên theo thứ tự khai báo."),
        ("truncate tránh narrowing", "static_cast<int>(d) — cast tường minh là cách thu hẹp trung thực mà không cần ngoặc nhọn."),
    ],
)

EXPLICIT_BOILER = r'''#include <string>
#include <type_traits>

struct Meters {
    int v;
    // TODO: make this constructor so int->Meters never happens implicitly
    Meters(int value) : v(value) {}
};

Meters operator""_m(unsigned long long m);   // a literal that must still work
'''

CH_EXPLICIT_CTOR = challenge(
    "cppa1-explicit-conversions",
    "explicit Guards Implicit Conversions",
    "The starter's `Meters(int)` allows accidental implicit conversions like `Meters m = 42;`. Mark the constructor `explicit` (keep the user-defined literal working) so the tests prove conversions require intent.",
    EXPLICIT_BOILER,
    [
        ("conversion requires intent",
         r'''static_assert(!std::is_convertible_v<int, Meters>, "int must not convert implicitly");
static_assert(std::is_constructible_v<Meters, int>, "explicit construction still works");
Meters m{42};
CHECK_EQ(m.v, 42);''',
         "Add explicit to the constructor: Meters m = 42; becomes ill-formed, Meters m{42}; keeps working."),
        ("the literal still constructs directly",
         r'''Meters run = 400_m;
CHECK_EQ(run.v, 400);''',
         "In the literal, call Meters(static_cast<int>(m)) — direct-initialization, which explicit allows."),
    ],
    difficulty="advanced",
)

VI_EXPLICIT_CTOR = vi_challenge(
    "explicit chặn chuyển đổi ngầm",
    "Constructor `Meters(int)` trong code khởi đầu cho phép các chuyển đổi ngầm như `Meters m = 42;`. Hãy thêm `explicit` (vẫn giữ literal hoạt động) để bài kiểm tra chứng minh mọi chuyển đổi đều phải có chủ ý.",
    [
        ("chuyển đổi phải có chủ ý", "Thêm explicit vào constructor: Meters m = 42; thành ill-formed, còn Meters m{42}; vẫn chạy."),
        ("literal vẫn dựng trực tiếp", "Trong literal, gọi Meters(static_cast<int>(m)) — direct-initialization, mà explicit cho phép."),
    ],
)

M1_PRAC3 = dict(
    sid="m1-init-practice",
    title="Initialization Traps",
    description="Brace narrowing and the most vexing parse — the two initialization traps that reach production code.",
    vi_title="Bẫy khởi tạo",
    vi_description="Narrowing với ngoặc nhọn và most vexing parse — hai cái bẫy khởi tạo hay lọt vào code production.",
    after_lesson=L1C,
    minutes=14,
    difficulty="advanced",
)

M1_PRAC3_CH = [CH_INIT_NARROW, CH_EXPLICIT_CTOR]
M1_PRAC3_VI = {"cppa1-init-narrowing": VI_INIT_NARROW,
               "cppa1-explicit-conversions": VI_EXPLICIT_CTOR}

M1_PRAC3_SOL = [
    ("cppa1-init-narrowing",
     r'''#include <string>
#include <vector>

struct Config {
    std::string name{"unset"};
    int port{0};
    std::vector<std::string> tags{};
};
int truncateToInt(double d) { return static_cast<int>(d); }
''',
     r'''#include <string>
#include <vector>

struct Config {
    std::string name{"unset"};
    double port{0};   // WRONG: member type changed, int checks fail
    std::vector<std::string> tags{};
};
int truncateToInt(double d) { return static_cast<int>(d) + 1; }  // WRONG: off-by-one result
'''),
    ("cppa1-explicit-conversions",
     EXPLICIT_BOILER.replace("    Meters(int value) : v(value) {}", "    explicit Meters(int value) : v(value) {}") + "\nMeters operator\"\"_m(unsigned long long m) { return Meters(static_cast<int>(m)); }\n",
     EXPLICIT_BOILER + "\nMeters operator\"\"_m(unsigned long long m) { return Meters(static_cast<int>(m)); }\n" + "\n// WRONG: constructor never made explicit\n"),
]

write_practice(M1, **M1_PRAC3, challenges=M1_PRAC3_CH, vi_challenges=M1_PRAC3_VI, solutions=M1_PRAC3_SOL)

# ---- module 1 checkpoint ----
CP1_MD = r'''
This checkpoint grades three skills at once: value categories, lifetime, and initialization. One challenge, three tests — predict each outcome before reading its hint.
'''

write_checkpoint(
    M1, L1D,
    "Checkpoint: Object Model",
    "Prove you can reason about value categories, lifetime, and initialization with graded compile-time and runtime checks.",
    16,
    CP1_MD,
    "Checkpoint: Mô hình đối tượng",
    "Chứng minh bạn suy luận được phân loại giá trị, vòng đời và khởi tạo bằng các kiểm tra compile-time và runtime.",
    r'''
Checkpoint này chấm ba kỹ năng cùng lúc: phân loại giá trị, vòng đời và khởi tạo. Một thử thách, ba bài kiểm tra — hãy dự đoán kết quả trước khi đọc gợi ý.
''',
    challenge(
        "cppa1-object-model-check",
        "Object Model Gauntlet",
        "Implement the three functions so every check passes: a by-value factory, a reference-returning accessor with persistent storage, and a destruction-order reporter.",
        r'''#include <string>
#include <type_traits>

std::string makeTag();                       // prvalue factory
std::string& registry();                     // lvalue accessor with storage
std::string pops(int n);                     // destruction order of n scoped guards: "n,n-1,...,1"
''',
        [
            ("factory is prvalue",
             r'''static_assert(std::is_same_v<decltype((makeTag())), std::string>, "must be prvalue");
CHECK_CONTAINS(makeTag(), "tag");''',
             "Return a std::string by value containing \"tag\"."),
            ("registry is lvalue with persistence",
             r'''registry() = "written";
CHECK_EQ(registry(), std::string("written"));''',
             "Back it with a function-local static std::string and return std::string&."),
            ("pops reports reverse destruction",
             r'''CHECK_EQ(pops(4), std::string("4,3,2,1"));''',
             "Destruction is reverse construction order; join with commas, no spaces."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại mô hình đối tượng",
        "Cài ba hàm để mọi kiểm tra pass: factory trả theo giá trị, accessor trả reference có bộ nhớ bền, và bộ báo thứ tự hủy.",
        [
            ("factory là prvalue", "Trả về std::string theo giá trị, chứa \"tag\"."),
            ("registry là lvalue còn tồn tại", "Dùng static std::string cục bộ và trả về std::string&."),
            ("pops báo hủy ngược", "Hủy ngược thứ tự tạo; nối bằng dấu phẩy, không có khoảng trắng."),
        ],
    ),
    solution=r'''#include <string>
#include <type_traits>

std::string makeTag() { return "tag-advanced"; }
std::string& registry() { static std::string s; return s; }
std::string pops(int n) {
    std::string out;
    for (int i = n; i >= 1; --i) { if (!out.empty()) out += ','; out += std::to_string(i); }
    return out;
}
''',
    wrong=r'''#include <string>
#include <type_traits>

std::string makeTag() { return "tag-advanced"; }
std::string&& registry() { static std::string s; return std::move(s); }  // WRONG: xvalue that drains the static
std::string pops(int n) { return "1,2,3,4"; }                             // WRONG: forward order
''',
)

# ============================ MODULE 2: move-forwarding ============================
M2 = "move-forwarding"

L2A = "forwarding-references"
L2B = "copy-elision-rvo"
L2C = "noexcept-and-rules"
L2D = "cppa-checkpoint-move"

write_module(
    M2,
    "Move Semantics Under the Hood",
    "Forwarding references, reference collapsing, std::forward, guaranteed elision, and the noexcept that makes vector growth move — the mechanics beneath the syntax you already use.",
    "Move Semantics Đằng Sau Cú Pháp",
    "Forwarding reference, reference collapsing, std::forward, guaranteed elision và noexcept giúp vector lớn lên bằng move — cơ chế bên dưới cú pháp bạn vẫn dùng hằng ngày.",
    [L2A, L2B, L2C, L2D],
    ["m2-forwarding-practice", "m2-noexcept-practice"],
)

write_lesson(
    M2, L2A,
    "Forwarding References and Reference Collapsing",
    "Why T&& sometimes binds lvalues, how collapsing makes std::forward possible, and when a forwarding constructor hijacks copies.",
    11,
    r'''
A `T&&` parameter is usually an rvalue reference — unless `T` is a **deduced** template parameter. Then it is a **forwarding reference**, which binds *everything*:

```cpp
template <class T> void sink(T&& x);   // forwarding reference
void sink2(Widget&& x);                // plain rvalue reference: rvalues only
```

## Deduction and collapsing

For a call `sink(expr)`, the compiler deduces `T` from the *value category* of `expr`:
- lvalue `Widget x` -> `T = Widget&`,
- rvalue -> `T = Widget` (plain).

Then **reference collapsing** builds the parameter type — the only rule that exists: `& &`, `& &&`, `&& &` all collapse to `&`; only `&& &&` stays `&&`.

| Call | T deduced | T&& becomes |
| --- | --- | --- |
| `sink(x)` (lvalue) | `Widget&` | `Widget& &&` -> `Widget&` |
| `sink(std::move(x))` | `Widget` | `Widget&&` |

## std::forward: restore what was lost

Inside the function, `x` is an lvalue (it has a name). `std::forward<T>(x)` casts it back to exactly what the caller had — an xvalue only when the original argument was an rvalue:

```cpp
template <class T, class... A>
auto makeUnique(A&&... a) {
    return std::unique_ptr<T>(new T(std::forward<A>(a)...));
}
```

## The greedy-constructor trap

A `template <class... A> Widget(A&&...)` constructor binds non-const lvalues *exactly*, while the copy constructor needs a qualification conversion — so on **direct initialization** (`Widget w{other};`) the forwarding constructor wins and hijacks the copy. Copy initialization (`Widget w = other;`) is safe because explicit constructors are excluded there. Standard fixes: constrain the template (`requires !std::same_as<std::decay_t<A>, Widget> && ...`) or provide unambiguous overloads. You will meet this trap as a graded exercise.
''',
    "Forwarding Reference và Reference Collapsing",
    "Vì sao T&& đôi khi buộc cả lvalue, collapsing làm std::forward khả thi, và khi nào constructor forwarding cướp thao tác copy.",
    r'''
Tham số `T&&` thường là rvalue reference — trừ khi `T` là tham số template **được suy diễn**. Khi đó nó là **forwarding reference**, buộc được *mọi thứ*:

```cpp
template <class T> void sink(T&& x);   // forwarding reference
void sink2(Widget&& x);                // rvalue reference thường: chỉ rvalue
```

## Suy diễn và collapsing

Với lời gọi `sink(expr)`, compiler suy diễn `T` từ *phân loại giá trị* của `expr`:
- lvalue `Widget x` -> `T = Widget&`,
- rvalue -> `T = Widget` (trơn).

Sau đó **reference collapsing** dựng kiểu tham số — chỉ có một quy tắc: `& &`, `& &&`, `&& &` đều sập về `&`; chỉ `&& &&` giữ nguyên `&&`.

| Lời gọi | T suy diễn | T&& thành |
| --- | --- | --- |
| `sink(x)` (lvalue) | `Widget&` | `Widget& &&` -> `Widget&` |
| `sink(std::move(x))` | `Widget` | `Widget&&` |

## std::forward: khôi phục cái đã mất

Bên trong hàm, `x` là lvalue (nó có tên). `std::forward<T>(x)` ép nó trở lại đúng những gì caller đưa vào — chỉ thành xvalue khi đối số gốc là rvalue:

```cpp
template <class T, class... A>
auto makeUnique(A&&... a) {
    return std::unique_ptr<T>(new T(std::forward<A>(a)...));
}
```

## Bẫy constructor tham lam

Constructor `template <class... A> Widget(A&&...)` buộc lvalue non-const *chính xác*, trong khi copy constructor cần một phép chuyển về const — nên với **direct initialization** (`Widget w{other};`), constructor forwarding thắng và cướp thao tác copy. Copy initialization (`Widget w = other;`) an toàn vì constructor explicit bị loại ở đó. Cách sửa chuẩn: ràng buộc template (`requires !std::same_as<std::decay_t<A>, Widget> && ...`) hoặc viết overload không mơ hồ. Bạn sẽ gặp đúng cái bẫy này trong phần chấm điểm.
''',
    difficulty="advanced",
)

write_lesson(
    M2, L2B,
    "Copy Elision: Guaranteed and Merely Likely",
    "C++17 made returning a prvalue free by definition. NRVO is still a courtesy the compiler usually grants — and std::move(local) disables it.",
    9,
    r'''
Since C++17, returning a **prvalue** is *guaranteed elision*: no copy or move exists even conceptually. The object is constructed directly in its final home:

```cpp
std::string build() { return std::string(1000, 'x'); }   // zero copies, zero moves — by the language
auto s = build();                                        // one allocation, one string
```

## NRVO — the powerful courtesy

Returning a **named** local (NRVO) is not guaranteed, but mainstream compilers do it for simple flows:

```cpp
std::string accumulate(int n) {
    std::string out;              // named local: NRVO candidate
    for (int i = 0; i < n; ++i) out += 'a';
    return out;                   // usually constructed directly in the caller's storage
}
```

## The anti-pattern: return std::move(local)

`return std::move(local);` **disables NRVO** (the expression is no longer the local's name) and forces a move — strictly worse than `return local;`, which moves anyway when elision fails. Compilers flag it (`-Wpessimizing-move`).

## Where elision never applies

- Assignment (only initialization elides),
- parameters (they are copies or references from the start),
- returning a member or parameter (only a local's NRVO or a prvalue return elides).

Count constructions with an instrumented type in the practice — the counters are the proof.
''',
    "Copy Elision: Được Bảo Đảm và Chỉ Thường Xảy Ra",
    "Từ C++17, trả về prvalue là miễn phí theo định nghĩa. NRVO vẫn là ân huệ compiler thường ban — và std::move(local) tắt nó đi.",
    r'''
Từ C++17, trả về **prvalue** là *guaranteed elision*: không hề có copy hay move, kể cả trên lý thuyết. Đối tượng được dựng trực tiếp tại chỗ cuối cùng:

```cpp
std::string build() { return std::string(1000, 'x'); }   // không copy, không move — theo ngôn ngữ
auto s = build();                                        // một lần cấp phát, một chuỗi
```

## NRVO — ân huệ mạnh mẽ

Trả về biến cục bộ **có tên** (NRVO) không được bảo đảm, nhưng compiler hiện đại vẫn làm với luồng đơn giản:

```cpp
std::string accumulate(int n) {
    std::string out;              // biến cục bộ có tên: ứng viên NRVO
    for (int i = 0; i < n; ++i) out += 'a';
    return out;                   // thường được dựng trực tiếp vào bộ nhớ của caller
}
```

## Anti-pattern: return std::move(local)

`return std::move(local);` **tắt NRVO** (biểu thức không còn là tên của biến cục bộ) và ép phải move — tệ hơn hẳn `return local;` vốn tự move khi elision thất bại. Compiler có cờ cảnh báo (`-Wpessimizing-move`).

## Khi nào elision không bao giờ áp dụng

- Phép gán (chỉ khởi tạo mới elide),
- tham số hàm (chúng vốn là bản copy hoặc reference),
- trả về thành viên hoặc tham số (chỉ NRVO của biến cục bộ hay return prvalue mới elide).

Đếm số lần dựng bằng kiểu có bộ đếm trong phần luyện tập — bộ đếm chính là bằng chứng.
''',
    difficulty="advanced",
)

write_lesson(
    M2, L2C,
    "noexcept Moves and the Rules of Zero/Five",
    "vector only moves during growth if the move is noexcept. Rule of Zero first, Rule of Five only when you own a resource.",
    10,
    r'''
## The noexcept that buys performance

`std::vector::push_back` must offer the strong exception guarantee while growing. It can only relocate elements with a **`noexcept` move constructor**; otherwise it falls back to copying (`std::move_if_noexcept`). Declaring your move `noexcept` is not decoration — it is a performance contract:

```cpp
struct Buffer {
    std::unique_ptr<char[]> data_;
    std::size_t size_{0};
    Buffer(Buffer&& b) noexcept : data_(std::exchange(b.data_, nullptr)), size_(std::exchange(b.size_, 0)) {}
    Buffer& operator=(Buffer&& b) noexcept { /* same shape */ return *this; }
};
```

`std::exchange` writes the "moved-from" state and hands you the old value in one step — the idiomatic move body.

## Rule of Zero first

If every member manages itself (`std::string`, `std::vector`, `std::unique_ptr`), you write **none** of the five special members. Defaults do the right thing under copying and moving.

## Rule of Five — all or nothing

Own a raw resource and you must decide about all five: destructor, copy ctor, copy assign, move ctor, move assign. Declaring *any* one suppresses the implicit moves — a silent pessimization. If you declare a destructor, declare (or `= default`) the moves too.

## The moved-from state

Moved-from standard types are **valid but unspecified** — assignable and destructible, nothing more promised. Document what your own types guarantee after a move; the graded exercise asks exactly that discipline.
''',
    "noexcept Move và Quy tắc Zero/Năm",
    "vector chỉ move khi lớn lên nếu move là noexcept. Ưu tiên Rule of Zero, chỉ dùng Rule of Five khi bạn sở hữu tài nguyên.",
    r'''
## Chi tiết noexcept mang lại hiệu năng

`std::vector::push_back` phải giữ đảm bảo ngoại lệ mạnh khi lớn lên. Nó chỉ chuyển chỗ phần tử bằng **move constructor `noexcept`**; nếu không sẽ quay lại copy (`std::move_if_noexcept`). Khai báo move `noexcept` không phải trang trí — đó là hợp đồng hiệu năng:

```cpp
struct Buffer {
    std::unique_ptr<char[]> data_;
    std::size_t size_{0};
    Buffer(Buffer&& b) noexcept : data_(std::exchange(b.data_, nullptr)), size_(std::exchange(b.size_, 0)) {}
    Buffer& operator=(Buffer&& b) noexcept { /* cùng hình dáng */ return *this; }
};
```

`std::exchange` ghi trạng thái "đã bị move" và trao cho bạn giá trị cũ trong một bước — cách viết move chuẩn mực.

## Rule of Zero trước tiên

Nếu mọi thành viên tự quản lý (`std::string`, `std::vector`, `std::unique_ptr`), bạn không viết **bất kỳ** special member nào trong năm. Mặc định làm đúng với cả copy lẫn move.

## Rule of Five — tất cả hoặc không gì

Sở hữu tài nguyên thô thì bạn phải quyết định cả năm: destructor, copy ctor, copy assign, move ctor, move assign. Khai báo *một* cái sẽ tắt các move ngầm — một sự chậm đi âm thầm. Nếu khai báo destructor, hãy khai báo (hoặc `= default`) cả move.

## Trạng thái sau move

Các kiểu chuẩn sau move **hợp lệ nhưng không xác định** — vẫn gán được và hủy được, không hứa gì thêm. Hãy ghi rõ kiểu của bạn đảm bảo gì sau move; bài tập chấm điểm đòi hỏi đúng kỷ luật đó.
''',
    difficulty="advanced",
)

# ---- module 2 practices ----
ELISION_BOILER = COUNTER_BOILER + r'''
Tracked makeTracked(std::string tag);   // TODO: return by value
Tracked accumulateTracked(int n);       // TODO: build a tag of n 'x' chars in a local, return it
'''

CH_GUARANTEED_ELISION = challenge(
    "cppa2-guaranteed-elision",
    "Guaranteed Elision, Proven by Counters",
    "Implement `makeTracked` returning its result **by value**, and `accumulateTracked` building a named local and returning it (NRVO). The counters must show zero copies and zero moves in both paths.",
    ELISION_BOILER,
    [
        ("prvalue return: zero copies, zero moves",
         r'''Tracked::copies = 0; Tracked::moves = 0;
Tracked t = makeTracked("direct");
CHECK_EQ(Tracked::copies, 0);
CHECK_EQ(Tracked::moves, 0);
CHECK_EQ(t.tag, std::string("direct"));''',
         "return Tracked(tag); — a prvalue return has guaranteed elision; constructing the return value from the argument stays copy- and move-free."),
        ("NRVO: zero copies, zero moves",
         r'''Tracked::copies = 0; Tracked::moves = 0;
Tracked a = accumulateTracked(3);
CHECK_EQ(Tracked::copies, 0);
CHECK_EQ(Tracked::moves, 0);
CHECK_EQ(a.tag, std::string("xxx"));''',
         "Build a local Tracked from std::string(3, 'x'), then return the local by name (NOT std::move) — NRVO constructs in place."),
    ],
    difficulty="advanced",
)

VI_GUARANTEED_ELISION = vi_challenge(
    "Guaranteed elision, chứng minh bằng bộ đếm",
    "Cài `makeTracked` trả về kết quả **theo giá trị**, và `accumulateTracked` dựng biến cục bộ rồi trả về nó (NRVO). Bộ đếm phải cho thấy không copy, không move ở cả hai đường.",
    [
        ("return prvalue: không copy, không move", "return Tracked(tag); — return prvalue được bảo đảm elision; dựng giá trị trả về từ đối số không tốn copy hay move."),
        ("NRVO: không copy, không move", "Dựng Tracked cục bộ từ std::string(3, 'x'), rồi return biến đó theo tên (KHÔNG dùng std::move) — NRVO dựng tại chỗ."),
    ],
)

FORWARD_BOILER = COUNTER_BOILER + r'''
#include <memory>

// Construct T from perfectly forwarded arguments.
template <class T, class... A>
std::unique_ptr<T> makeOwned(A&&... a);

// Forward a single argument with the right reference collapsing.
template <class T>
T&& restore(T&& x);
'''

CH_FORWARD_WRAPPER = challenge(
    "cppa2-forward-wrapper",
    "Forward Like make_unique",
    "Implement `makeOwned` that constructs `T` from perfectly forwarded arguments, and `restore` that forwards a single argument with the right collapse.",
    FORWARD_BOILER,
    [
        ("rvalues stay rvalues",
         r'''Tracked::moves = 0; Tracked::copies = 0;
auto p = makeOwned<Tracked>(Tracked("hot"));
CHECK_EQ(Tracked::moves, 1);
CHECK_EQ(Tracked::copies, 0);
CHECK_EQ(p->tag, std::string("hot"));''',
         "new T(std::forward<A>(a)...) — the temporary is moved once into T; a copy here (missing forward) counts 0 moves and fails."),
        ("lvalues stay lvalues (copied, not moved)",
         r'''Tracked::copies = 0; Tracked::moves = 0;
Tracked src("cold");
auto q = makeOwned<Tracked>(src);
CHECK_EQ(Tracked::copies, 1);
CHECK_EQ(Tracked::moves, 0);
CHECK_EQ(q->tag, std::string("cold"));''',
         "The lvalue src must be copied exactly once into T — forward preserves the caller's category."),
        ("restore collapses correctly",
         r'''Tracked base("seed");
Tracked& lref = restore(base);
CHECK_EQ(lref.tag, std::string("seed"));
std::string rv = restore(std::string("tmp"));
CHECK_EQ(rv, std::string("tmp"));''',
         "return std::forward<T>(x); — collapsing restores the original category for both calls."),
    ],
    difficulty="advanced",
)

VI_FORWARD_WRAPPER = vi_challenge(
    "Forward như make_unique",
    "Cài `makeOwned` dựng `T` từ các đối số được forward hoàn hảo, và `restore` forward một đối số với đúng phép collapsing.",
    [
        ("rvalue vẫn là rvalue", "new T(std::forward<A>(a)...) — đối tượng tạm được move một lần vào T; nếu copy (thiếu forward) thì moves bằng 0 và rớt."),
        ("lvalue vẫn là lvalue (copy, không move)", "lvalue src phải được copy đúng một lần vào T — forward giữ nguyên phân loại của caller."),
        ("restore sập đúng luật", "return std::forward<T>(x); — collapsing khôi phục phân loại gốc cho cả hai lời gọi."),
    ],
)

GREEDY_BOILER = COUNTER_BOILER + r'''
#include <string>
#include <type_traits>
#include <utility>

// TODO: constrain this forwarding constructor so it rejects Tracked arguments
// (otherwise it hijacks direct-initialization copies like Tracked c{other};).
template <class... A>
explicit Tracked(A&&... a) : tag(std::forward<A>(a)...) {}
'''

CH_GREEDY_TRAP = challenge(
    "cppa2-greedy-forwarding",
    "The Greedy Forwarding Constructor",
    "The forwarding constructor in the starter hijacks direct-initialization copies. Constrain it with a `requires` clause so `Tracked c{src};` routes to the **copy** constructor, while `Tracked d(\"placed\");` still forwards.",
    GREEDY_BOILER,
    [
        ("direct-init copy routes to the copy ctor",
         r'''Tracked::copies = 0;
Tracked src("origin");
Tracked c{src};
CHECK_EQ(Tracked::copies, 1);
CHECK_EQ(c.tag, std::string("origin"));''',
         "Add requires (!(std::same_as<std::decay_t<A>, Tracked>) && ...) before explicit — a Tracked lvalue then can't match, so the copy ctor wins."),
        ("string literal still forwards",
         r'''Tracked d("placed");
CHECK_EQ(d.tag, std::string("placed"));''',
         "A const char array decays to char*, which is not Tracked — the constraint leaves normal construction alone."),
    ],
    difficulty="advanced",
)

VI_GREEDY_TRAP = vi_challenge(
    "Constructor forwarding tham lam",
    "Constructor forwarding trong code khởi đầu cướp các phép copy khi direct initialization. Hãy ràng buộc nó bằng mệnh đề `requires` để `Tracked c{src};` đi qua **copy** constructor, trong khi `Tracked d(\"placed\");` vẫn forward bình thường.",
    [
        ("copy khi direct-init đi qua copy ctor", "Thêm requires (!(std::same_as<std::decay_t<A>, Tracked>) && ...) trước explicit — khi đó lvalue Tracked không khớp nữa và copy ctor thắng."),
        ("string literal vẫn forward", "Mảng const char suy biến thành char*, không phải Tracked — ràng buộc không ảnh hưởng việc dựng bình thường."),
    ],
)

M2_PRAC1 = dict(
    sid="m2-forwarding-practice",
    title="Forwarding Mechanics",
    description="Perfect forwarding, the greedy-constructor trap, and collapse behavior — with copy/move counters grading you.",
    vi_title="Cơ chế forwarding",
    vi_description="Perfect forwarding, cái bẫy constructor tham lam, và hành vi collapsing — bộ đếm copy/move chấm điểm bạn.",
    after_lesson=L2A,
    minutes=24,
    difficulty="advanced",
)

M2_PRAC1_CH = [CH_GUARANTEED_ELISION, CH_FORWARD_WRAPPER, CH_GREEDY_TRAP]
M2_PRAC1_VI = {"cppa2-guaranteed-elision": VI_GUARANTEED_ELISION,
               "cppa2-forward-wrapper": VI_FORWARD_WRAPPER,
               "cppa2-greedy-forwarding": VI_GREEDY_TRAP}

M2_PRAC1_SOL = [
    ("cppa2-guaranteed-elision",
     ELISION_BOILER + "\nTracked makeTracked(std::string tag) { return Tracked(std::move(tag)); }\nTracked accumulateTracked(int n) { Tracked out{std::string(std::size_t(n), 'x')}; return out; }\n",
     ELISION_BOILER + "\nTracked makeTracked(std::string tag) { Tracked t(std::move(tag)); return std::move(t); }  // WRONG: pessimizing move forces one move\nTracked accumulateTracked(int n) { Tracked out{std::string(std::size_t(n), 'x')}; return std::move(out); }  // WRONG: disables NRVO\n"),
    ("cppa2-forward-wrapper",
     FORWARD_BOILER + "\ntemplate <class T, class... A>\nstd::unique_ptr<T> makeOwned(A&&... a) { return std::unique_ptr<T>(new T(std::forward<A>(a)...)); }\n\ntemplate <class T>\nT&& restore(T&& x) { return std::forward<T>(x); }\n",
     FORWARD_BOILER + "\ntemplate <class T, class... A>\nstd::unique_ptr<T> makeOwned(A&&... a) { return std::unique_ptr<T>(new T(a...)); }  // WRONG: no forward -> copies rvalues\n\ntemplate <class T>\nT&& restore(T&& x) { return x; }  // WRONG: named rvalue stays lvalue\n"),
    ("cppa2-greedy-forwarding",
     r'''#include <cstddef>
#include <string>
#include <type_traits>
#include <utility>

struct Tracked {
    static inline int copies = 0;
    static inline int moves = 0;
    std::string tag;
    Tracked() : tag("empty") {}
    explicit Tracked(std::string t) : tag(std::move(t)) {}
    Tracked(const Tracked& o) : tag(o.tag) { ++copies; }
    Tracked(Tracked&& o) noexcept : tag(std::move(o.tag)) { ++moves; }
    Tracked& operator=(const Tracked& o) { tag = o.tag; ++copies; return *this; }
    Tracked& operator=(Tracked&& o) noexcept { tag = std::move(o.tag); ++moves; return *this; }
    template <class... A>
        requires (!(std::same_as<std::decay_t<A>, Tracked>) && ...)
    explicit Tracked(A&&... a) : tag(std::forward<A>(a)...) {}
};
''',
     r'''#include <cstddef>
#include <string>
#include <type_traits>
#include <utility>

struct Tracked {
    static inline int copies = 0;
    static inline int moves = 0;
    std::string tag;
    Tracked() : tag("empty") {}
    explicit Tracked(std::string t) : tag(std::move(t)) {}
    Tracked(const Tracked& o) : tag(o.tag) { ++copies; }
    Tracked(Tracked&& o) noexcept : tag(std::move(o.tag)) { ++moves; }
    Tracked& operator=(const Tracked& o) { tag = o.tag; ++copies; return *this; }
    Tracked& operator=(Tracked&& o) noexcept { tag = std::move(o.tag); ++moves; return *this; }
    template <class... A>                       // WRONG: unconstrained -> hijacks Tracked c{src};
    explicit Tracked(A&&... a) : tag(std::forward<A>(a)...) {}
};
'''),
]

write_practice(M2, **M2_PRAC1, challenges=M2_PRAC1_CH, vi_challenges=M2_PRAC1_VI, solutions=M2_PRAC1_SOL)

BUFFER_BOILER = r'''#include <algorithm>
#include <cstddef>
#include <utility>
#include <vector>

struct Buffer {
    static inline int copies = 0;   // instrumented for the graded check
    char payload[16] = {};
    std::size_t id = 0;
    Buffer() = default;
    explicit Buffer(std::size_t i) : id(i) {}
    Buffer(const Buffer& o) : id(o.id) { std::copy(std::begin(o.payload), std::end(o.payload), std::begin(payload)); ++copies; }
    Buffer(Buffer&& o) noexcept;            // TODO: noexcept, hand over the state
    Buffer& operator=(Buffer&& o) noexcept; // TODO
};
'''

CH_NOEXCEPT_VECTOR = challenge(
    "cppa2-noexcept-vector",
    "noexcept Unlocks Moving Growth",
    "Complete `Buffer`'s move constructor and move assignment **noexcept** using `std::exchange`. The graded check grows a `std::vector<Buffer>` to 8 elements with push_back and requires the copy counter to stay at zero — the proof that vector relocates by move.",
    BUFFER_BOILER,
    [
        ("move is noexcept",
         r'''static_assert(std::is_nothrow_move_constructible_v<Buffer>, "move must be noexcept");
static_assert(std::is_nothrow_move_assignable_v<Buffer>, "assign must be noexcept");''',
         "Buffer(Buffer&& o) noexcept : payload(o.payload), id(std::exchange(o.id, 0)) {} — the same shape for assignment."),
        ("vector growth performs zero copies",
         r'''Buffer::copies = 0;
std::vector<Buffer> v;
for (std::size_t i = 0; i < 8; ++i) v.push_back(Buffer(i));
CHECK_EQ(Buffer::copies, 0);
CHECK_EQ(v.size(), std::size_t{8});
CHECK_EQ(v[7].id, std::size_t{7});''',
         "With a noexcept move, reallocation relocates elements by move — the copy counter never increments."),
    ],
    difficulty="advanced",
)

VI_NOEXCEPT_VECTOR = vi_challenge(
    "noexcept mở khóa move khi lớn lên",
    "Hoàn thiện move constructor và move assignment của `Buffer` **noexcept** bằng `std::exchange`. Bài kiểm tra làm `std::vector<Buffer>` lớn lên 8 phần tử bằng push_back và đòi bộ đếm copy phải giữ ở 0 — bằng chứng vector chuyển chỗ bằng move.",
    [
        ("move là noexcept", "Buffer(Buffer&& o) noexcept : payload(o.payload), id(std::exchange(o.id, 0)) {} — cùng hình dáng cho phép gán."),
        ("vector lớn lên không copy lần nào", "Với move noexcept, việc cấp phát lại chuyển chỗ phần tử bằng move — bộ đếm copy không bao giờ tăng."),
    ],
)

LEASE_BOILER = r'''#include <cstddef>
#include <utility>

struct Config0 {
    // Rule of Zero: members manage themselves; add NO special members.
    int level{0};
};

struct Lease {
    int* resource_ = nullptr;   // owning pointer — Rule of Five territory
    Lease() = default;
    explicit Lease(int v);
    ~Lease();                                   // delete
    Lease(const Lease& o);                      // deep copy
    Lease& operator=(const Lease& o);           // guarded assignment
    Lease(Lease&& o) noexcept;                  // steal + null
    Lease& operator=(Lease&& o) noexcept;       // steal + null
};
'''

CH_RULE_OF_ZERO = challenge(
    "cppa2-rule-of-zero",
    "Rule of Zero vs Rule of Five",
    "`Config0` already obeys the Rule of Zero — leave it alone. Implement all five special members of `Lease` over its owning `int*`: deep copy, guarded assignment, noexcept steals.",
    LEASE_BOILER,
    [
        ("Rule of Zero needs nothing",
         r'''Config0 a; a.level = 3;
Config0 b = a;
CHECK_EQ(b.level, 3);''',
         "Do nothing — the implicit members copy the int correctly. Do not add any special member declarations."),
        ("Lease deep-copies",
         r'''Lease l1(7);
Lease l2 = l1;
*l2.resource_ = 9;
CHECK_EQ(*l1.resource_, 7);''',
         "new int(*o.resource_) — deep copy, never share the pointer."),
        ("Lease steals on move",
         r'''Lease l3(5);
Lease l4 = std::move(l3);
CHECK_NE(l4.resource_, nullptr);
CHECK_EQ(l3.resource_, nullptr);''',
         "Steal the pointer, null the source: resource_(std::exchange(o.resource_, nullptr))."),
    ],
    difficulty="advanced",
)

VI_RULE_OF_ZERO = vi_challenge(
    "Rule of Zero vs Rule of Five",
    "`Config0` đã tuân thủ Rule of Zero — đừng đụng vào nó. Cài đủ năm special member của `Lease` trên `int*` đang sở hữu: copy sâu, gán có bảo vệ, cướp tài nguyên noexcept.",
    [
        ("Rule of Zero không cần gì", "Không làm gì — các thành viên ngầm copy int đúng cách. Đừng thêm khai báo special member nào."),
        ("Lease copy sâu", "new int(*o.resource_) — copy sâu, không bao giờ dùng chung con trỏ."),
        ("Lease cướp khi move", "Cướp con trỏ, đặt nguồn về null: resource_(std::exchange(o.resource_, nullptr))."),
    ],
)

M2_PRAC2 = dict(
    sid="m2-noexcept-practice",
    title="noexcept and Ownership Rules",
    description="Make vector growth move, and practice Rule of Zero vs a full Rule-of-Five owning type.",
    vi_title="noexcept và quy tắc sở hữu",
    vi_description="Cho vector lớn lên bằng move, và luyện Rule of Zero đối chiếu với một kiểu sở hữu tài nguyên đầy đủ Rule of Five.",
    after_lesson=L2C,
    minutes=20,
    difficulty="advanced",
)

M2_PRAC2_CH = [CH_NOEXCEPT_VECTOR, CH_RULE_OF_ZERO]
M2_PRAC2_VI = {"cppa2-noexcept-vector": VI_NOEXCEPT_VECTOR,
               "cppa2-rule-of-zero": VI_RULE_OF_ZERO}

M2_PRAC2_SOL = [
    ("cppa2-noexcept-vector",
     BUFFER_BOILER + "\nBuffer::Buffer(Buffer&& o) noexcept : id(std::exchange(o.id, 0)) { std::copy(std::begin(o.payload), std::end(o.payload), std::begin(payload)); }\nBuffer& Buffer::operator=(Buffer&& o) noexcept { std::copy(std::begin(o.payload), std::end(o.payload), std::begin(payload)); id = std::exchange(o.id, 0); return *this; }\n",
     BUFFER_BOILER + "\nBuffer::Buffer(Buffer&& o) : payload(o.payload), id(std::exchange(o.id, 0)) {}   // WRONG: not noexcept\nBuffer& Buffer::operator=(Buffer&& o) noexcept { std::copy(std::begin(o.payload), std::end(o.payload), std::begin(payload)); id = std::exchange(o.id, 0); return *this; }\n"),
    ("cppa2-rule-of-zero",
     LEASE_BOILER + "\nLease::Lease(int v) : resource_(new int(v)) {}\nLease::~Lease() { delete resource_; }\nLease::Lease(const Lease& o) : resource_(o.resource_ ? new int(*o.resource_) : nullptr) {}\nLease& Lease::operator=(const Lease& o) { if (this != &o) { int* n = o.resource_ ? new int(*o.resource_) : nullptr; delete resource_; resource_ = n; } return *this; }\nLease::Lease(Lease&& o) noexcept : resource_(std::exchange(o.resource_, nullptr)) {}\nLease& Lease::operator=(Lease&& o) noexcept { if (this != &o) { delete resource_; resource_ = std::exchange(o.resource_, nullptr); } return *this; }\n",
     LEASE_BOILER + "\nLease::Lease(int v) : resource_(new int(v)) {}\nLease::~Lease() { delete resource_; }\nLease::Lease(const Lease& o) : resource_(o.resource_) {}  // WRONG: shallow copy -> shared pointer\nLease& Lease::operator=(const Lease& o) { resource_ = o.resource_; return *this; }  // WRONG: leaks + shares\nLease::Lease(Lease&& o) noexcept : resource_(std::exchange(o.resource_, nullptr)) {}\nLease& Lease::operator=(Lease&& o) noexcept { if (this != &o) { delete resource_; resource_ = std::exchange(o.resource_, nullptr); } return *this; }\n"),
]

write_practice(M2, **M2_PRAC2, challenges=M2_PRAC2_CH, vi_challenges=M2_PRAC2_VI, solutions=M2_PRAC2_SOL)

# ---- module 2 checkpoint ----
CP2_MD = r'''
The move-semantics checkpoint: forwarding with counters, elision proofs, and the noexcept contract. One challenge, two tests.
'''

CP2_BOILER = COUNTER_BOILER + r'''
#include <memory>

std::unique_ptr<Tracked> factoryTracked(Tracked t);   // TODO: forward into a new Tracked
Tracked buildTracked(int n);                          // TODO: NRVO builder
'''

write_checkpoint(
    M2, L2D,
    "Checkpoint: Move Mechanics",
    "Prove forwarding, elision, and noexcept reasoning in one graded challenge.",
    16,
    CP2_MD,
    "Checkpoint: Cơ chế move",
    "Chứng minh forwarding, elision và suy luận noexcept trong một thử thách có chấm điểm.",
    r'''
Checkpoint move-semantics: forwarding với bộ đếm và chứng minh elision. Một thử thách, hai bài kiểm tra.
''',
    challenge(
        "cppa2-move-checkpoint",
        "Move Gauntlet",
        "Implement a forwarding factory and an NRVO builder so the counters prove zero accidental copies.",
        CP2_BOILER,
        [
            ("factory forwards rvalue with exactly one move",
             r'''Tracked::moves = 0; Tracked::copies = 0;
auto owned = factoryTracked(Tracked("goal"));
CHECK_EQ(Tracked::moves, 1);
CHECK_EQ(Tracked::copies, 0);
CHECK_EQ(owned->tag, std::string("goal"));''',
             "new Tracked(std::move(t)) — exactly one move from the by-value parameter into the pointee."),
            ("builder uses NRVO: zero copies, zero moves",
             r'''Tracked::moves = 0; Tracked::copies = 0;
Tracked built = buildTracked(4);
CHECK_EQ(Tracked::copies, 0);
CHECK_EQ(Tracked::moves, 0);
CHECK_EQ(built.tag, std::string("xxxx"));''',
             "Construct a local from std::string(4, 'x') and return it by name — no std::move in the return."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại move",
        "Cài forwarding factory và NRVO builder để bộ đếm chứng minh không có copy ngoài ý muốn.",
        [
            ("factory forward rvalue đúng một lần move", "new Tracked(std::move(t)) — đúng một lần move từ tham số truyền giá trị vào phần tử trỏ tới."),
            ("builder dùng NRVO: không copy, không move", "Dựng biến cục bộ từ std::string(4, 'x') rồi return theo tên — không dùng std::move khi return."),
        ],
    ),
    solution=CP2_BOILER + "\nstd::unique_ptr<Tracked> factoryTracked(Tracked t) { return std::unique_ptr<Tracked>(new Tracked(std::move(t))); }\nTracked buildTracked(int n) { Tracked out{std::string(std::size_t(n), 'x')}; return out; }\n",
    wrong=CP2_BOILER + "\nstd::unique_ptr<Tracked> factoryTracked(Tracked t) { return std::unique_ptr<Tracked>(new Tracked(t)); }  // WRONG: copies\nTracked buildTracked(int n) { Tracked out{std::string(std::size_t(n), 'x')}; return std::move(out); }  // WRONG: blocks NRVO\n",
)

print("modules 1-2 done")
