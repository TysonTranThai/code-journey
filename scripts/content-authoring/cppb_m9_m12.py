#!/usr/bin/env python3
"""C++ Beginner — modules 9-12: structs/enums, classes/OOP, pointers/references, memory/RAII."""
from cppb import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 9: structs-enums ============================
M9 = "structs-enums"

L9A = "structs-and-aggregates"
L9B = "enum-class-and-aliases"
L9C = "checkpoint-modeling"

write_module(
    M9,
    "Structs, Enums & Data Modeling",
    "Design your own types: aggregates with structs, safe constants with enum class, and models that read like the problem.",
    "Struct, Enum & Mô hình hóa dữ liệu",
    "Thiết kế kiểu dữ liệu của riêng bạn: aggregate với struct, hằng số an toàn với enum class, và những mô hình đọc như chính bài toán.",
    [L9A, L9B, L9C],
    ["m9-struct-practice"],
)

write_lesson(
    M9, L9A,
    "structs: Bundling Data That Belongs Together",
    "Define, initialize (with designated initializers), pass, and return structs; member functions as a bridge to classes.",
    11,
    '''
## The problem structs solve

A student is not three unrelated variables floating around — it is one thing:

```cpp
struct Student {
    std::string name;
    int age{};
    double gpa{};
};
```

Now `Student` is a type, exactly like `int`:

```cpp
Student s{"Linh", 20, 3.8};                    // aggregate initialization
Student t{.name = "Minh", .age = 21, .gpa = 3.5};   // C++20 designated initializers
s.name = "Linh Nguyen";                        // member access with .
Student older = older_of(s, t);                // passes and returns by value like any type
```

The `{}` member initializers (`int age{}`) give every new Student sane defaults — no garbage members, ever.

## Structs are values

Assignment copies every member; passing by value copies; `==` does NOT work automatically (compare members yourself, or write `operator==` — module 10's neighbor topic). The value semantics you learned in module 2 apply to your own types now.

## A taste of member functions

```cpp
struct Rectangle {
    double width{};
    double height{};

    double area() const { return width * height; }   // const: reads, never writes
};
r.area()
```

A function inside the struct operates on the members of whichever object it is called on. The `const` suffix promises it does not modify the object — the same const-correctness as module 2, now per-object. Member functions are the door to module 10.

## Design hint: model the domain, not the storage

`struct Account { std::string owner; long long cents; };` beats `struct AccountData2 { ... };` — name things what they ARE. And when two values always travel together (module 7's hint), that pair deserves a struct with a real name, not `std::pair`.
''',
    "struct: Gói dữ liệu thuộc cùng nhau",
    "Định nghĩa, khởi tạo (với designated initializers), truyền, và trả về struct; hàm thành viên như cầu nối tới class.",
    '''
## Vấn đề mà struct giải quyết

Một học sinh không phải là ba biến rời rạc lơ lửng — nó là MỘT thứ:

```cpp
struct Student {
    std::string name;
    int age{};
    double gpa{};
};
```

Giờ `Student` là một kiểu, y như `int`:

```cpp
Student s{"Linh", 20, 3.8};                    // aggregate initialization
Student t{.name = "Minh", .age = 21, .gpa = 3.5};   // designated initializers C++20
s.name = "Linh Nguyen";                        // truy cập thành viên với .
Student older = older_of(s, t);                // truyền và trả về theo giá trị như mọi kiểu
```

Các bộ khởi tạo thành viên `{}` (`int age{}`) cho mọi Student mới mặc định hợp lý — không bao giờ có thành viên chứa rác.

## Struct là giá trị

Gán là sao chép mọi thành viên; truyền theo giá trị là sao chép; `==` KHÔNG tự hoạt động (tự so các thành viên, hoặc viết `operator==` — chủ đề láng giềng của module 10). Ngữ nghĩa giá trị bạn học ở module 2 giờ áp dụng cho kiểu tự định nghĩa của chính bạn.

## Nếm thử hàm thành viên

```cpp
struct Rectangle {
    double width{};
    double height{};

    double area() const { return width * height; }   // const: chỉ đọc, không ghi
};
r.area()
```

Một hàm nằm trong struct thao tác trên các thành viên của đúng đối tượng được gọi. Hậu tố `const` hứa rằng nó không sửa đối tượng — cùng tính đúng đắn của const ở module 2, giờ là theo từng đối tượng. Hàm thành viên là cánh cửa tới module 10.

## Gợi ý thiết kế: mô hình hóa miền vấn đề, không phải bộ nhớ

`struct Account { std::string owner; long long cents; };` hơn hẳn `struct AccountData2 { ... };` — hãy đặt tên theo NGHĨA của sự vật. Và khi hai giá trị luôn đi cùng nhau (gợi ý ở module 7), cặp đó xứng đáng có một struct với cái tên thật, không phải `std::pair`.
''',
)

write_lesson(
    M9, L9B,
    "enum class and using-aliases",
    "Named constants that respect types: enum class for closed sets of options, using for readable type names.",
    11,
    '''
## The magic-string problem

Functions that take `"admin"`, `"editor"`, `"viewer"` as strings are a bug factory: typos compile, casing drifts, and the set of valid values lives only in documentation. The fix is a **closed set with a type**:

```cpp
enum class Role { Viewer, Editor, Admin };

Role role = Role::Editor;

switch (role) {
    case Role::Viewer: /* ... */ break;
    case Role::Editor: /* ... */ break;
    case Role::Admin:  /* ... */ break;
}
```

## Why `enum class`, not plain `enum`

- **Scoped:** values are `Role::Editor`, never bare `Editor` — no namespace pollution.
- **Strongly typed:** `Role` does not silently convert to `int`; you cannot accidentally compare a Role with a number or pass it where an int is expected. (Plain pre-C++11 `enum` leaks values into the enclosing scope and converts to int — legacy code compat, not a recommendation.)
- **Switch-checked:** with `-Wall -Wextra`, GCC warns when a switch over a `Role` misses a case (add a `default` or handle every enumerator).

## `using`: type nicknames

```cpp
using Inventory = std::map<std::string, int>;
using Scores = std::vector<int>;

Inventory stock;             // reads like the domain
std::vector<std::vector<int>> grid;
using Grid = std::vector<std::vector<int>>;
```

`using` (modern; prefer it over C's `typedef`) gives long types honest names. It is documentation with compiler enforcement: change the alias once, every user follows.

## Modeling exercise ahead

The checkpoint asks you to design `struct Order { ... }` with `enum class Status { ... }` — one glance at the type definitions should explain the whole business domain.
''',
    "enum class và bí danh using",
    "Hằng số có tên tôn trọng kiểu: enum class cho các tập tùy chọn khép kín, using cho tên kiểu dễ đọc.",
    '''
## Vấn đề magic-string

Hàm nhận `"admin"`, `"editor"`, `"viewer"` dạng chuỗi là một nhà máy bug: lỗi chính tả vẫn biên dịch được, chữ hoa/thường trôi dạt, và tập giá trị hợp lệ chỉ tồn tại trong tài liệu. Cách sửa là một **tập khép kín có kiểu**:

```cpp
enum class Role { Viewer, Editor, Admin };

Role role = Role::Editor;

switch (role) {
    case Role::Viewer: /* ... */ break;
    case Role::Editor: /* ... */ break;
    case Role::Admin:  /* ... */ break;
}
```

## Vì sao `enum class`, không phải `enum` trần

- **Có scope:** giá trị là `Role::Editor`, không bao giờ là `Editor` trần — không ô nhiễm namespace.
- **Kiểu mạnh:** `Role` không tự chuyển thành `int`; bạn không thể vô tình so một Role với số hay truyền nó vào chỗ cần int. (enum cổ trước C++11 rò giá trị ra scope bao ngoài và tự chuyển thành int — tương thích code cũ, không phải khuyến nghị.)
- **Switch được kiểm tra:** với `-Wall -Wextra`, GCC cảnh báo khi switch trên `Role` thiếu case (thêm `default` hoặc xử lý mọi enumerator).

## `using`: biệt danh cho kiểu

```cpp
using Inventory = std::map<std::string, int>;
using Scores = std::vector<int>;

Inventory stock;             // đọc như miền vấn đề
std::vector<std::vector<int>> grid;
using Grid = std::vector<std::vector<int>>;
```

`using` (hiện đại; ưu tiên hơn `typedef` của C) đặt tên trung thực cho các kiểu dài. Nó là tài liệu mà compiler thực thi: đổi alias một lần, mọi nơi dùng theo.

## Bài tập mô hình hóa phía trước

Checkpoint yêu cầu bạn thiết kế `struct Order { ... }` với `enum class Status { ... }` — chỉ cần liếc phần định nghĩa kiểu là hiểu cả miền nghiệp vụ.
''',
)

# ---- Module 9 checkpoint ----
write_checkpoint(
    M9, L9C,
    "Checkpoint: Data Modeling",
    "One graded challenge: design an Order model and implement status logic over it.",
    15,
    '''
**Checkpoint — modeling.** Pass the graded challenge below to finish the module.

You define the types yourself this time (the tests include your header — that is, the top of your solution): a struct, an enum class, and functions over them.
''',
    "Checkpoint: Mô hình hóa dữ liệu",
    "Một challenge có chấm: thiết kế mô hình Order và cài đặt logic trạng thái trên đó.",
    '''
**Checkpoint — mô hình hóa.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Lần này bạn tự định nghĩa các kiểu (test dùng chính phần đầu solution của bạn): một struct, một enum class, và các hàm thao tác trên chúng.
''',
    challenge(
        "cpp9-check-order-model",
        "Order Model",
        "Define `struct Order` with `std::string id`, `int quantity`, `double unit_price`, and `enum class Status { Pending, Shipped, Cancelled }` (nested) plus a `status` member (default Pending). Implement `total(order)` (quantity × unit_price) and `cancellable(order)` (true only when status is Pending).",
        "#include <string>\\n\\n// TODO: define Order here\\n\\ndouble total(const Order& order) {\\n    // TODO\\n}\\nbool cancellable(const Order& order) {\\n    // TODO\\n}",
        [
            ("total", "Order o{.id = \"A1\", .quantity = 3, .unit_price = 2.5}; CHECK_NEAR(total(o), 7.5, 0.001);", "3 × 2.5 — members via designated initializers."),
            ("default status", "Order o{.id = \"A2\", .quantity = 1, .unit_price = 1.0}; CHECK(cancellable(o));", "Default-constructed status must be Pending."),
            ("shipped not cancellable", "Order o{.id = \"A3\", .quantity = 1, .unit_price = 1.0}; o.status = Order::Status::Shipped; CHECK(!cancellable(o));", "Only Pending orders can cancel."),
        ],
        level="real-world",
        difficulty="beginner",
    ),
    vi_challenge(
        "Mô hình đơn hàng",
        "Định nghĩa `struct Order` với `std::string id`, `int quantity`, `double unit_price`, và `enum class Status { Pending, Shipped, Cancelled }` (lồng bên trong) cùng thành viên `status` (mặc định Pending). Cài đặt `total(order)` (quantity × unit_price) và `cancellable(order)` (chỉ true khi status là Pending).",
        [("tổng", "3 × 2.5 — truy cập thành viên qua designated initializers."), ("trạng thái mặc định", "status khởi tạo mặc định phải là Pending."), ("đã gửi không hủy được", "Chỉ đơn Pending mới được hủy.")],
    ),
    solution="#include <string>\\nstruct Order {\\n    enum class Status { Pending, Shipped, Cancelled };\\n    std::string id;\\n    int quantity{};\\n    double unit_price{};\\n    Status status{Status::Pending};\\n};\\ndouble total(const Order& order) { return order.quantity * order.unit_price; }\\nbool cancellable(const Order& order) { return order.status == Order::Status::Pending; }",
    wrong="#include <string>\\nstruct Order {\\n    enum class Status { Pending, Shipped, Cancelled };\\n    std::string id;\\n    int quantity{};\\n    double unit_price{};\\n    Status status{Status::Shipped};\\n};\\ndouble total(const Order& order) { return order.quantity * order.unit_price; }\\nbool cancellable(const Order& order) { return order.status == Order::Status::Pending; }",
)

# ---- Module 9 practice ----
write_practice(
    M9, "m9-struct-practice",
    "Struct Practice: Models That Read Like the Domain",
    "Distance math over a Point struct, a Rectangle with member functions, and enum-class state transitions.",
    "Luyện Struct: Mô hình đọc như miền vấn đề",
    "Tính khoảng cách qua struct Point, một Rectangle với hàm thành viên, và chuyển trạng thái bằng enum class.",
    L9A, 25, "beginner",
    [
        challenge(
            "cpp9-rect-grow",
            "Rectangle Member Function",
            "Given the Rectangle struct below, implement the member function `scaled(factor)` returning a NEW Rectangle scaled on both sides (original untouched).",
            "#include <string>\\n\\nstruct Rectangle {\\n    double width{};\\n    double height{};\\n\\n    // TODO: double scaled(double factor) const\\n};",
            [("scales", "Rectangle r{.width = 2.0, .height = 3.0}; Rectangle s = r.scaled(2.0); CHECK_NEAR(s.width, 4.0, 0.001); CHECK_NEAR(s.height, 6.0, 0.001);", "Both members multiply by the factor."), ("original intact", "Rectangle r{.width = 2.0, .height = 3.0}; Rectangle s = r.scaled(2.0); CHECK_NEAR(r.width, 2.0, 0.001);", "The function is const — the original stays put.")],
            level="guided",
        ),
    ],
    {"cpp9-rect-grow": vi_challenge("Hàm thành viên Rectangle", "Cho struct Rectangle bên dưới, cài hàm thành viên `scaled(factor)` trả về một Rectangle MỚI được phóng cả hai cạnh (bản gốc không đổi).", [("phóng to", "Cả hai thành viên nhân với factor."), ("bản origen nguyên vẹn", "Hàm là const — bản gốc giữ nguyên.")])},
    solutions=[
        ("cpp9-rect-grow", "#include <string>\\nstruct Rectangle {\\n    double width{};\\n    double height{};\\n\\n    Rectangle scaled(double factor) const { return Rectangle{.width = width * factor, .height = height * factor}; }\\n};", "#include <string>\\nstruct Rectangle {\\n    double width{};\\n    double height{};\\n\\n    Rectangle scaled(double factor) const { width *= factor; height *= factor; return *this; }\\n};"),
    ],
)

# ============================ MODULE 10: classes-oop ============================
M10 = "classes-oop"

L10A = "classes-and-encapsulation"
L10B = "constructors-and-const-methods"
L10C = "composition-inheritance-polymorphism"
L10D = "checkpoint-oop"

write_module(
    M10,
    "Classes & Object-Oriented C++",
    "Encapsulation with class, constructors that establish invariants, const member functions, and composition-first design — inheritance only where it earns its keep.",
    "Class & C++ Hướng đối tượng",
    "Đóng gói với class, constructor thiết lập bất biến, hàm thành viên const, và thiết kế composition-trước — kế thừa chỉ ở nơi nó xứng đáng.",
    [L10A, L10B, L10C, L10D],
    ["m10-class-practice"],
)

write_lesson(
    M10, L10A,
    "class and Encapsulation",
    "private state, public interface, invariants, and why getters-for-everything is not encapsulation.",
    12,
    '''
## From struct to class: the difference is the door

`struct` leaves everything public. `class` makes members **private by default** — and that is the point:

```cpp
class BankAccount {
public:                                  // the interface — what others may use
    void deposit(long long cents) {
        if (cents <= 0) return;          // the object enforces its own rules
        balance_cents_ += cents;
    }

    long long balance() const { return balance_cents_; }

private:                                 // the state — nobody touches this directly
    long long balance_cents_{0};
};
```

An **invariant** is a rule that must always hold ("balance is never negative"). Hiding the state behind a disciplined interface means the invariant is enforced in *one place* instead of hoped-for at every call site.

## Encapsulation is not getters-and-setters-for-everything

```cpp
// ANTI-PATTERN: a struct with extra steps
class Bad {
public:
    void set_balance(long long b) { balance_ = b; }   // anyone can set anything
    long long get_balance() const { return balance_; }
private:
    long long balance_{};
};
```

If every member has a trivial getter *and* setter, nothing is protected — you built a struct with worse ergonomics. Expose **operations** (deposit, withdraw), not fields. Ask "what can others *do*?" not "what can others *read*?"

## The trailing underscore convention

`balance_cents_` marks private members visually; many styles use `m_` or a plain name. Pick one convention and stay consistent — the point is that a reader never wonders whether a name is a member or a local.

## Composition is still the default

A `class` with `std::vector<Transaction> history_` as a member is *composition* — objects owning other objects. It will remain your most-used tool; the next lessons add constructors and (only then) inheritance.
''',
    "class và đóng gói",
    "Trạng thái private, giao diện public, bất biến, và vì sao getter-cho-mọi-thứ không phải là đóng gói.",
    '''
## Từ struct sang class: khác biệt nằm ở cánh cửa

`struct` để mọi thứ public. `class` mặc định các thành viên **private** — và đó chính là điểm mấu chốt:

```cpp
class BankAccount {
public:                                  // giao diện — những gì người khác được dùng
    void deposit(long long cents) {
        if (cents <= 0) return;          // đối tượng tự thực thi luật của nó
        balance_cents_ += cents;
    }

    long long balance() const { return balance_cents_; }

private:                                 // trạng thái — không ai đụng trực tiếp
    long long balance_cents_{0};
};
```

Một **bất biến** là luật phải luôn đúng ("số dư không bao giờ âm"). Giấu trạng thái sau một giao diện kỷ luật nghĩa là bất biến được thực thi ở *một nơi duy nhất* thay vì được hi vọng ở mọi điểm gọi.

## Đóng gói không phải là getter-và-setter-cho-mọi-thứ

```cpp
// CHỐNG-MẪU: một struct với thêm các bước thừa
class Bad {
public:
    void set_balance(long long b) { balance_ = b; }   // ai cũng set được mọi thứ
    long long get_balance() const { return balance_; }
private:
    long long balance_{};
};
```

Nếu mọi thành viên đều có getter *và* setter tầm thường, chẳng có gì được bảo vệ — bạn vừa dựng một struct với công thái học tệ hơn. Hãy phơi ra các **thao tác** (deposit, withdraw), không phải các trường. Hãy hỏi "người khác có thể *làm* gì?" chứ không phải "người khác có thể *đọc* gì?"

## Quy ước gạch dưới đuôi

`balance_cents_` đánh dấu thành viên private bằng thị giác; nhiều phong cách dùng `m_` hoặc tên trần. Chọn một quy ước và giữ nguyên — điều quan trọng là người đọc không bao giờ phải tự hỏi một cái tên là thành viên hay biến cục bộ.

## Composition vẫn là mặc định

Một `class` có `std::vector<Transaction> history_` làm thành viên là *composition* — đối tượng sở hữu đối tượng khác. Nó vẫn sẽ là công cụ bạn dùng nhiều nhất; các bài sau thêm constructor và (chỉ sau đó) kế thừa.
''',
)

write_lesson(
    M10, L10B,
    "Constructors, Destructors, and const Methods",
    "Establishing invariants at birth, RAII's first look, and reading const member functions correctly.",
    11,
    '''
## Constructors: born valid

A constructor runs automatically when an object is created. Its job is to leave the object **valid** — no "uninitialized then fixed later" window:

```cpp
class Timer {
public:
    explicit Timer(std::string name) : name_(std::move(name)), start_(std::chrono::steady_clock::now()) {}

private:
    std::string name_;
    std::chrono::steady_clock::time_point start_;
};
```

- The **member initializer list** (after `:`) initializes members directly — prefer it over assigning in the body.
- `explicit` stops surprise conversions from single arguments (`Timer t = "x";` will not compile — good).
- `std::move(name)` passes the string's *guts* into the member instead of copying (the standard library does this everywhere; you use `std::move` in constructors, never on const objects, and never manually on locals right before last use without a reason — module 12 revisits).

## Destructors: born valid, die clean

The destructor `~Timer()` runs automatically at scope exit, in reverse construction order. You rarely write one in Beginner (members clean themselves up — the RAII promise of module 12), but you must know it exists and runs **deterministically**: this is why C++ has no `finally` and does not need one.

## const member functions

```cpp
long long balance() const { return balance_cents_; }   // promises: no mutation
```

`const` after the parameter list means "calling this does not modify the object". Non-const objects and const references (i.e., nearly every parameter in well-written code) can only call const methods — so mark every read-only method const, or your API becomes unusable from `const BankAccount&` parameters.

## The discipline, summarized

- Constructor: make every member valid.
- Methods: enforce the invariant on every mutation.
- const on every read-only method.
- Everything else stays private.
''',
    "Constructor, Destructor, và hàm thành viên const",
    "Thiết lập bất biến ngay từ lúc sinh, cái nhìn đầu tiên về RAII, và đọc đúng hàm thành viên const.",
    '''
## Constructor: sinh ra đã hợp lệ

Một constructor chạy tự động khi đối tượng được tạo. Nhiệm vụ của nó là để đối tượng **hợp lệ** — không có khung thời gian "chưa khởi tạo rồi sửa sau":

```cpp
class Timer {
public:
    explicit Timer(std::string name) : name_(std::move(name)), start_(std::chrono::steady_clock::now()) {}

private:
    std::string name_;
    std::chrono::steady_clock::time_point start_;
};
```

- **Danh sách khởi tạo thành viên** (sau `:`) khởi tạo thành viên trực tiếp — ưu tiên hơn gán trong thân hàm.
- `explicit` chặn các chuyển đổi bất ngờ từ một đối số (`Timer t = "x";` sẽ không biên dịch — tốt).
- `std::move(name)` chuyển "ruột" của chuỗi vào thành viên thay vì sao chép (thư viện chuẩn làm điều này khắp nơi; bạn dùng `std::move` trong constructor, không bao giờ trên đối tượng const, và không tự tiện trên biến cục bộ ngay trước lần dùng cuối nếu không có lý do — module 12 sẽ nhắc lại).

## Destructor: sinh ra hợp lệ, chết đi sạch sẽ

Destructor `~Timer()` chạy tự động khi ra khỏi scope, theo thứ tự dựng ngược. Ở trình độ Cơ bản bạn hiếm khi tự viết nó (các thành viên tự dọn dẹp — lời hứa RAII của module 12), nhưng bạn phải biết nó tồn tại và chạy **xác định**: đó là lý do C++ không có `finally` và không cần.

## Hàm thành viên const

```cpp
long long balance() const { return balance_cents_; }   // hứa: không sửa gì cả
```

`const` sau danh sách tham số nghĩa là "gọi hàm này không sửa đối tượng". Đối tượng non-const và tham chiếu const (tức gần như mọi tham số trong code viết tốt) chỉ gọi được các hàm const — nên hãy thêm const cho mọi hàm chỉ đọc, nếu không API của bạn sẽ vô dụng khi truyền qua `const BankAccount&`.

## Kỷ luật, tóm tắt

- Constructor: làm mọi thành viên hợp lệ.
- Hàm: thực thi bất biến ở mọi lần sửa.
- const cho mọi hàm chỉ đọc.
- Mọi thứ còn lại giữ private.
''',
)

write_lesson(
    M10, L10C,
    "Composition First, Inheritance Carefully",
    "has-a beats is-a most days: composition as the default tool, virtual functions and polymorphism when a genuine subtype appears.",
    12,
    '''
## Composition: objects built from objects

```cpp
class Engine { /* ... */ };

class Car {
private:
    Engine engine_;                    // Car HAS-AN Engine
    std::vector<std::string> plates_;
};
```

Most "reuse" is this: an object that owns others and forwards work to them. It is flexible (swap the member), honest (the relationship is visible), and needs no ceremony.

## The inheritance question

Ask: is the new class a genuine **subtype** — same concept, specialized behavior — that code should treat *uniformly through the base interface*? If yes:

```cpp
class Shape {
public:
    virtual ~Shape() = default;                  // ALWAYS a virtual destructor
    virtual double area() const = 0;             // pure virtual: no body here
};

class Circle : public Shape {
public:
    explicit Circle(double r) : radius_(r) {}
    double area() const override { return 3.14159265358979 * radius_ * radius_; }
private:
    double radius_;
};

class Square : public Shape {
public:
    explicit Square(double s) : side_(s) {}
    double area() const override { return side_ * side_; }
private:
    double side_;
};

double total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {   // polymorphism
    double total = 0;
    for (const auto& s : shapes) total += s->area();     // the right area() is chosen at runtime
    return total;
}
```

Read the annotations:

- `virtual` — "subclasses may replace this".
- `= 0` — pure virtual; `Shape` becomes **abstract** (cannot be instantiated; it is a contract).
- `override` — ask the compiler to verify you are actually replacing something (typos become errors — always write it).
- `virtual ~Shape() = default;` — deleting through a base pointer without a virtual destructor is undefined behavior. Write it, every time, no exceptions.
- `std::unique_ptr<Shape>` — owning pointers to polymorphic objects; the memory-safety story is module 12, but you are seeing the real shape of production polymorphism now.

## The honest default

Beginner code that reaches for inheritance usually wanted composition (a `Report` with a `Formatter` member) or nothing at all. Reach for inheritance when you genuinely have *many* subtypes treated uniformly through one interface — the shapes case, plugins, strategy variants. Otherwise: composition.
''',
    "Composition trước, kế thừa cẩn trọng",
    "has-a thắng is-a phần lớn thời gian: composition làm công cụ mặc định, hàm ảo và đa hình khi một kiểu con thật sự xuất hiện.",
    '''
## Composition: đối tượng dựng từ đối tượng

```cpp
class Engine { /* ... */ };

class Car {
private:
    Engine engine_;                    // Car CÓ-MỘT Engine
    std::vector<std::string> plates_;
};
```

Phần lớn "tái sử dụng" là thế này: một đối tượng sở hữu các đối tượng khác và chuyển công việc cho chúng. Nó linh hoạt (đổi thành viên được), trung thực (mối quan hệ nhìn thấy được), và không cần nghi lễ gì.

## Câu hỏi về kế thừa

Hãy hỏi: lớp mới có phải là một **kiểu con** thật sự — cùng khái niệm, hành vi chuyên biệt — mà code nên đối xử *thống nhất qua giao diện lớp cha* không? Nếu có:

```cpp
class Shape {
public:
    virtual ~Shape() = default;                  // LUÔN LUÔN có virtual destructor
    virtual double area() const = 0;             // pure virtual: không có thân ở đây
};

class Circle : public Shape {
public:
    explicit Circle(double r) : radius_(r) {}
    double area() const override { return 3.14159265358979 * radius_ * radius_; }
private:
    double radius_;
};

class Square : public Shape {
public:
    explicit Square(double s) : side_(s) {}
    double area() const override { return side_ * side_; }
private:
    double side_;
};

double total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {   // đa hình
    double total = 0;
    for (const auto& s : shapes) total += s->area();     // area() đúng được chọn lúc chạy
    return total;
}
```

Đọc các chú thích:

- `virtual` — "lớp con có thể thay thế hàm này".
- `= 0` — pure virtual; `Shape` trở thành **trừu tượng** (không thể khởi tạo; nó là một bản hợp đồng).
- `override` — nhờ compiler kiểm tra bạn đang thay thế thứ gì đó có thật (lỗi chính tả thành lỗi biên dịch — luôn viết nó).
- `virtual ~Shape() = default;` — xóa qua con trỏ lớp cha mà không có virtual destructor là hành vi không xác định. Hãy viết nó, mọi lần, không ngoại lệ.
- `std::unique_ptr<Shape>` — con trỏ sở hữu tới đối tượng đa hình; câu chuyện an toàn bộ nhớ là module 12, nhưng bạn đang nhìn thấy hình dạng thật của đa hình trong production ngay bây giờ.

## Mặc định trung thực

Code người mới giơ tay đòi kế thừa thường chỉ muốn composition (một `Report` có thành viên `Formatter`) hoặc chẳng cần gì cả. Hãy với tới kế thừa khi bạn thật sự có *nhiều* kiểu con được đối xử thống nhất qua một giao diện — trường hợp các hình, plugin, biến thể chiến lược. Nếu không: composition.
''',
)

# ---- Module 10 checkpoint ----
write_checkpoint(
    M10, L10D,
    "Checkpoint: OOP",
    "One graded challenge: a class with a real invariant, const-correct interface, and one polymorphic use.",
    15,
    '''
**Checkpoint — OOP.** Pass the graded challenge below to finish the module.

A `Counter` class (encapsulation + invariant) and an area function over shapes (polymorphism) — the module's two halves in one artifact.
''',
    "Checkpoint: OOP",
    "Một challenge có chấm: một class với bất biến thật, giao diện const-correct, và một lần dùng đa hình.",
    '''
**Checkpoint — OOP.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Một lớp `Counter` (đóng gói + bất biến) và một hàm diện tích trên các hình (đa hình) — hai nửa của module trong cùng một sản phẩm.
''',
    challenge(
        "cpp10-check-counter-shapes",
        "Counter and Shapes",
        "Implement class `Counter` with: a constructor taking an initial value (default 0), `inc()` (+1), `reset()` (back to the value it was constructed with), and `value() const`. The count must never go below the initial value (inc past it is fine). Then implement `total_area(const std::vector<std::unique_ptr<Shape>>&)` given the Shape/Circle/Square definitions in the boilerplate.",
        "#include <memory>\\n#include <vector>\\n\\nclass Shape {\\npublic:\\n    virtual ~Shape() = default;\\n    virtual double area() const = 0;\\n};\\nclass Circle : public Shape {\\npublic:\\n    explicit Circle(double r) : radius_(r) {}\\n    double area() const override { return 3.14159265358979 * radius_ * radius_; }\\nprivate:\\n    double radius_;\\n};\\nclass Square : public Shape {\\npublic:\\n    explicit Square(double s) : side_(s) {}\\n    double area() const override { return side_ * side_; }\\nprivate:\\n    double side_;\\n};\\n\\nclass Counter {\\npublic:\\n    // TODO\\nprivate:\\n    // TODO\\n};\\n\\ndouble total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {\\n    // TODO\\n}",
        [
            ("counts up", "Counter c; c.inc(); c.inc(); CHECK_EQ(c.value(), 2);", "Default start 0, two incs, value 2."),
            ("reset", "Counter c{5}; c.inc(); c.reset(); CHECK_EQ(c.value(), 5);", "Reset returns to the CONSTRUCTED value, not zero."),
            ("const-safe", "const Counter& view = c2; (void)view.value(); CHECK(true);", "value() must be const-callable on const references."),
            ("area polymorphic", "std::vector<std::unique_ptr<Shape>> v; v.push_back(std::make_unique<Square>(2.0)); v.push_back(std::make_unique<Circle>(1.0)); CHECK_NEAR(total_area(v), 7.14159, 0.001);", "4 + π, chosen at runtime through the base interface."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Counter và các hình",
        "Cài đặt lớp `Counter` với: constructor nhận giá trị ban đầu (mặc định 0), `inc()` (+1), `reset()` (về giá trị lúc khởi tạo), và `value() const`. Bộ đếm không bao giờ được xuống dưới giá trị ban đầu (inc vượt lên thì được). Sau đó cài `total_area(const std::vector<std::unique_ptr<Shape>>&)` với các định nghĩa Shape/Circle/Square cho sẵn trong boilerplate.",
        [("đếm lên", "Bắt đầu mặc định 0, hai lần inc, giá trị 2."), ("reset", "Reset về giá trị KHỞI TẠO, không phải số không."), ("an toàn với const", "value() phải gọi được trên tham chiếu const."), ("diện tích đa hình", "4 + π, được chọn lúc chạy qua giao diện lớp cha.")],
    ),
    solution="#include <memory>\\n#include <vector>\\n\\nclass Shape {\\npublic:\\n    virtual ~Shape() = default;\\n    virtual double area() const = 0;\\n};\\nclass Circle : public Shape {\\npublic:\\n    explicit Circle(double r) : radius_(r) {}\\n    double area() const override { return 3.14159265358979 * radius_ * radius_; }\\nprivate:\\n    double radius_;\\n};\\nclass Square : public Shape {\\npublic:\\n    explicit Square(double s) : side_(s) {}\\n    double area() const override { return side_ * side_; }\\nprivate:\\n    double side_;\\n};\\n\\nclass Counter {\\npublic:\\n    explicit Counter(int initial = 0) : initial_(initial), value_(initial) {}\\n    void inc() { ++value_; }\\n    void reset() { value_ = initial_; }\\n    int value() const { return value_; }\\nprivate:\\n    int initial_;\\n    int value_;\\n};\\n\\ndouble total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {\\n    double t = 0;\\n    for (const auto& s : shapes) t += s->area();\\n    return t;\\n}",
    wrong="#include <memory>\\n#include <vector>\\n\\nclass Shape {\\npublic:\\n    virtual ~Shape() = default;\\n    virtual double area() const = 0;\\n};\\nclass Circle : public Shape {\\npublic:\\n    explicit Circle(double r) : radius_(r) {}\\n    double area() const override { return 3.14159265358979 * radius_ * radius_; }\\nprivate:\\n    double radius_;\\n};\\nclass Square : public Shape {\\npublic:\\n    explicit Square(double s) : side_(s) {}\\n    double area() const override { return side_ * side_; }\\nprivate:\\n    double side_;\\n};\\n\\nclass Counter {\\npublic:\\n    explicit Counter(int initial = 0) : initial_(initial), value_(initial) {}\\n    void inc() { ++value_; }\\n    void reset() { value_ = 0; }\\n    int value() const { return value_; }\\nprivate:\\n    int initial_;\\n    int value_;\\n};\\n\\ndouble total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {\\n    double t = 0;\\n    for (const auto& s : shapes) t += s->area();\\n    return t;\\n}",
)

# ---- Module 10 practice ----
write_practice(
    M10, "m10-class-practice",
    "Class Practice: Invariants That Hold",
    "A temperature class guarding its range, and a stack built on vector with encapsulation.",
    "Luyện Class: Bất biến phải đứng vững",
    "Một lớp nhiệt độ canh chừng khoảng giá trị, và một stack dựng trên vector với đóng gói.",
    L10A, 25, "beginner",
    [
        challenge(
            "cpp10-temperature",
            "Temperature Class",
            "Implement class `Temperature` (Celsius): constructor validates -273.15..10000 (invalid → keeps 0.0); `set(double)` same rule; `celsius() const`; `is_freezing() const` (<= 0).",
            "#include <string>\\n\\nclass Temperature {\\npublic:\\n    // TODO\\nprivate:\\n    // TODO\\n};",
            [("valid range", "Temperature t{25.0}; CHECK_NEAR(t.celsius(), 25.0, 0.001);", "Valid values are kept."), ("absolute zero guard", "Temperature t{-300.0}; CHECK_NEAR(t.celsius(), 0.0, 0.001);", "Below -273.15 → falls back to 0.0."), ("freezing", "Temperature t{-5.0}; CHECK(t.is_freezing());", "-5°C is freezing."), ("set guarded", "Temperature t{10.0}; t.set(-999.0); CHECK_NEAR(t.celsius(), 10.0, 0.001);", "Invalid set leaves the value unchanged.")],
            level="independent",
        ),
    ],
    {"cpp10-temperature": vi_challenge("Lớp Temperature", "Cài đặt lớp `Temperature` (Celsius): constructor kiểm tra khoảng -273.15..10000 (sai → giữ 0.0); `set(double)` cùng luật; `celsius() const`; `is_freezing() const` (<= 0).", [("khoảng hợp lệ", "Giá trị hợp lệ được giữ lại."), ("chặn dưới không tuyệt đối", "Thấp hơn -273.15 → quay về 0.0."), ("đóng băng", "-5°C là đóng băng."), ("set có kiểm soát", "Set không hợp lệ giữ nguyên giá trị.")])},
    solutions=[
        ("cpp10-temperature", "#include <string>\\nclass Temperature {\\npublic:\\n    explicit Temperature(double c = 0.0) { set(c); }\\n    void set(double c) { if (c >= -273.15 && c <= 10000.0) celsius_ = c; }\\n    double celsius() const { return celsius_; }\\n    bool is_freezing() const { return celsius_ <= 0.0; }\\nprivate:\\n    double celsius_{0.0};\\n};", "#include <string>\\nclass Temperature {\\npublic:\\n    explicit Temperature(double c = 0.0) : celsius_(c) {}\\n    void set(double c) { celsius_ = c; }\\n    double celsius() const { return celsius_; }\\n    bool is_freezing() const { return celsius_ <= 0.0; }\\nprivate:\\n    double celsius_{0.0};\\n};"),
    ],
)

# ============================ MODULE 11: pointers-references ============================
M11 = "pointers-references"

L11A = "references-and-aliasing"
L11B = "pointers-and-nullptr"
L11C = "checkpoint-access"

write_module(
    M11,
    "References & Pointers",
    "Access without ownership: references as aliases, pointers as addresses, nullptr, and the lifetime question that governs them all.",
    "Tham chiếu & Con trỏ",
    "Truy cập mà không sở hữu: tham chiếu như bí danh, con trỏ như địa chỉ, nullptr, và câu hỏi vòng đời chi phối tất cả.",
    [L11A, L11B, L11C],
    ["m11-access-practice"],
)

write_lesson(
    M11, L11A,
    "References: Names for Real Objects",
    "Binding, the no-reseat rule, pass-by-reference APIs, and the lifetime warning that references cannot save you from.",
    10,
    '''
## A reference is an alias

```cpp
int score = 90;
int& alias = score;      // alias IS score — not a copy
alias = 95;
CHECK(score == 95);      // changed through the alias
```

Binding a reference writes no memory and calls no constructor: it is another *name* for an existing object. Rules that follow:

- A reference must be initialized when declared, and can never refer to a different object later (no reseating).
- `sizeof(alias)` is the size of the referent, `&alias` takes the referent's address — the language pretends the alias does not exist.
- There are no references to nothing: a reference is born pointing at an object (dangling is possible only through bugs — below).

## The API patterns (recap with teeth)

```cpp
void scale_all(std::vector<int>& v, int k);            // in-out: will modify
int  total(const std::vector<int>& v);                 // in: big, read-only
void bump(int& n);                                     // out: result through parameter
int  twice(int n);                                     // small value: plain by-value
```

## The one danger: dangling

```cpp
const std::string& name = make_greeting();   // if make_greeting returns BY VALUE...
// ...the temporary dies at the end of this statement; in many real cases name dangles
```

A reference promises *no ownership and no lifetime extension* (a temporary bound directly in an initializer is an exception — and relying on that exception is advanced). The beginner rule: **references must not outlive the object they name.** When data must survive the scope that created it, that is ownership — module 12's smart pointers, not references.
''',
    "Tham chiếu: Tên gọi cho đối tượng thật",
    "Gán kết (binding), quy tắc không-gán-lại, các mẫu API truyền theo tham chiếu, và cảnh báo vòng đời mà tham chiếu không thể cứu bạn.",
    '''
## Tham chiếu là một bí danh

```cpp
int score = 90;
int& alias = score;      // alias CHÍNH LÀ score — không phải bản sao
alias = 95;
CHECK(score == 95);      // thay đổi qua bí danh
```

Gán một tham chiếu không ghi bộ nhớ và không gọi constructor: nó chỉ là một *tên khác* cho đối tượng đã tồn tại. Các quy tắc theo sau:

- Tham chiếu phải được khởi tạo ngay khi khai báo, và không bao giờ trỏ sang đối tượng khác sau đó (không gán lại).
- `sizeof(alias)` là kích thước của đối tượng được trỏ, `&alias` lấy địa chỉ của đối tượng đó — ngôn ngữ giả vờ như bí danh không tồn tại.
- Không có tham chiếu đến "không gì cả": tham chiếu sinh ra đã trỏ vào một đối tượng (treo chỉ xảy ra qua bug — bên dưới).

## Các mẫu API (nhắc lại với răng sắc hơn)

```cpp
void scale_all(std::vector<int>& v, int k);            // in-out: sẽ sửa
int  total(const std::vector<int>& v);                 // in: dữ liệu lớn, chỉ đọc
void bump(int& n);                                     // out: kết quả qua tham số
int  twice(int n);                                     // giá trị nhỏ: truyền thường
```

## Một nguy hiểm duy nhất: treo (dangling)

```cpp
const std::string& name = make_greeting();   // nếu make_greeting trả về THEO GIÁ TRỊ...
// ...đối tượng tạm chết khi kết thúc câu lệnh; trong nhiều trường hợp thật, name bị treo
```

Tham chiếu hứa *không sở hữu và không kéo dài vòng đời* (trường hợp ngoại lệ: đối tượng tạm được gán trực tiếp trong initializer — và dựa vào ngoại lệ đó là chuyện nâng cao). Quy tắc người mới: **tham chiếu không được sống lâu hơn đối tượng mà nó gọi tên.** Khi dữ liệu phải sống sót qua scope đã tạo ra nó, đó là sở hữu — smart pointer ở module 12, không phải tham chiếu.
''',
)

write_lesson(
    M11, L11B,
    "Pointers: Addresses, Dereferencing, nullptr",
    "What a pointer really is, & and *, pointer vs reference, and the modern non-owning pointer rules.",
    12,
    '''
## An address you can hold

```cpp
int score = 90;
int* p = &score;      // p holds score's ADDRESS ("pointer to int")
CHECK(*p == 90);      // * dereferences: read/write through the address
*p = 95;
CHECK(score == 95);
```

`&x` takes an address; `*p` follows one. A pointer is a *value* (an address) — it can be copied, compared, and, unlike a reference, **reseated**:

```cpp
int a = 1, b = 2;
int* p = &a;
p = &b;               // now points at b — references can never do this
```

## nullptr: pointing at nothing, honestly

```cpp
int* p = nullptr;         // explicitly "no object"
if (p) { use(*p); }       // ALWAYS check before dereferencing
```

Dereferencing `nullptr` is a crash (undefined behavior, actually). Never initialize pointers to `0`/`NULL` (legacy); write `nullptr`. Never leave a pointer uninitialized.

## Pointer vs reference — choosing

| Question | Use |
| --- | --- |
| Must it always name an object? | reference (`&`) |
| Does "no object" need representing? | pointer + `nullptr` |
| Must the target be changeable later (reseat)? | pointer |
| Passing big read-only data? | `const&` (the everyday choice) |

In modern application code, **non-owning pointers appear far less than references** — mostly for optional targets and reseat-able observers (and as the thing you will meet in C-style APIs).

## The ownership boundary (say it out loud)

A raw pointer in modern C++ is a **non-owning view**: "I can *see* that object; its lifetime is someone else's business." The moment a pointer is expected to *keep the object alive*, raw pointers are the wrong tool — that is `std::unique_ptr`/`std::shared_ptr` (module 12). Core Guidelines R.3: "a raw pointer (a `T*`) is non-owning" — make your code say the same.
''',
    "Con trỏ: Địa chỉ, giải tham chiếu, nullptr",
    "Con trỏ thật sự là gì, & và *, con trỏ so với tham chiếu, và các quy tắc con trỏ không-owning hiện đại.",
    '''
## Một địa chỉ bạn có thể cầm

```cpp
int score = 90;
int* p = &score;      // p giữ ĐỊA CHỈ của score ("con trỏ tới int")
CHECK(*p == 90);      // * giải tham chiếu: đọc/ghi qua địa chỉ
*p = 95;
CHECK(score == 95);
```

`&x` lấy địa chỉ; `*p` đi theo địa chỉ. Con trỏ là một *giá trị* (một địa chỉ) — có thể sao chép, so sánh, và khác tham chiếu, **gán lại được**:

```cpp
int a = 1, b = 2;
int* p = &a;
p = &b;               // giờ trỏ vào b — tham chiếu không bao giờ làm được
```

## nullptr: trỏ vào không-gì-cả, một cách trung thực

```cpp
int* p = nullptr;         // tường minh "không có đối tượng"
if (p) { use(*p); }       // LUÔN kiểm tra trước khi giải tham chiếu
```

Giải tham chiếu `nullptr` là một crash (thực chất là hành vi không xác định). Đừng bao giờ khởi tạo con trỏ bằng `0`/`NULL` (cổ xưa); hãy viết `nullptr`. Đừng bao giờ để con trỏ không được khởi tạo.

## Con trỏ hay tham chiếu — cách chọn

| Câu hỏi | Dùng |
| --- | --- |
| Có bắt buộc luôn gọi tên một đối tượng? | tham chiếu (`&`) |
| Có cần biểu diễn "không có đối tượng"? | con trỏ + `nullptr` |
| Có cần đổi mục tiêu về sau (gán lại)? | con trỏ |
| Truyền dữ liệu lớn chỉ đọc? | `const&` (lựa chọn hằng ngày) |

Trong code ứng dụng hiện đại, **con trỏ không-owning xuất hiện ít hơn tham chiếu rất nhiều** — chủ yếu cho mục tiêu tùy chọn và observer có thể gán lại (và như thứ bạn sẽ gặp trong các API kiểu C).

## Ranh giới sở hữu (hãy nói to điều này)

Một con trỏ thô trong C++ hiện đại là **cái nhìn không-owning**: "tôi có thể *nhìn thấy* đối tượng đó; vòng đời của nó là việc của người khác." Khoảnh khắc một con trỏ bị kỳ vọng *giữ đối tượng còn sống*, con trỏ thô là sai công cụ — đó là việc của `std::unique_ptr`/`std::shared_ptr` (module 12). Core Guidelines R.3: "một con trỏ thô (một `T*`) là không-owning" — hãy để code của bạn nói điều tương tự.
''',
)

# ---- Module 11 checkpoint ----
write_checkpoint(
    M11, L11C,
    "Checkpoint: References and Pointers",
    "One graded challenge: choose the right access pattern and use nullptr safely.",
    15,
    '''
**Checkpoint — references and pointers.** Pass the graded challenge below to finish the module.

The tests exercise each signature's contract: which parameters are `const&`, which are `T*` allowed to be null, and which return through references.
''',
    "Checkpoint: Tham chiếu và con trỏ",
    "Một challenge có chấm: chọn đúng mẫu truy cập và dùng nullptr an toàn.",
    '''
**Checkpoint — tham chiếu và con trỏ.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Test kiểm tra đúng bản hợp đồng của từng chữ ký: tham số nào là `const&`, tham số nào là `T*` được phép null, và cái nào trả kết quả qua tham chiếu.
''',
    challenge(
        "cpp11-check-access",
        "Access Patterns",
        "Implement `bigger_of(const int* a, const int* b)` returning the pointed-to value that is larger, or 0 when either pointer is null; and `swap_through(int& a, int& b)` swapping through references.",
        "#include <string>\\n\\nint bigger_of(const int* a, const int* b) {\\n    // TODO — either may be nullptr\\n}\\nvoid swap_through(int& a, int& b) {\\n    // TODO\\n}",
        [
            ("both valid", "int x = 3, y = 9; CHECK_EQ(bigger_of(&x, &y), 9);", "Dereference and compare when both are non-null."),
            ("null tolerated", "CHECK_EQ(bigger_of(nullptr, nullptr), 0);", "Null pointers are legal input: return 0, never dereference."),
            ("swap", "int a = 1, b = 2; swap_through(a, b); CHECK_EQ(a, 2); CHECK_EQ(b, 1);", "References modify the caller's variables."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Các mẫu truy cập",
        "Cài đặt `bigger_of(const int* a, const int* b)` trả về giá trị được trỏ tới có số lớn hơn, hoặc 0 khi một trong hai con trỏ là null; và `swap_through(int& a, int& b)` hoán đổi qua tham chiếu.",
        [("cả hai hợp lệ", "Giải tham chiếu và so sánh khi cả hai khác null."), ("chấp nhận null", "Con trỏ null là input hợp lệ: trả 0, không bao giờ giải tham chiếu."), ("hoán đổi", "Tham chiếu sửa được biến của người gọi.")],
    ),
    solution="#include <string>\\nint bigger_of(const int* a, const int* b) {\\n    if (!a || !b) return 0;\\n    return *a > *b ? *a : *b;\\n}\\nvoid swap_through(int& a, int& b) {\\n    int tmp = a; a = b; b = tmp;\\n}",
    wrong="#include <string>\\nint bigger_of(const int* a, const int* b) {\\n    return *a > *b ? *a : *b;\\n}\\nvoid swap_through(int& a, int& b) {\\n    int tmp = a; a = b; b = tmp;\\n}",
)

# ---- Module 11 practice ----
write_practice(
    M11, "m11-access-practice",
    "Access Practice: The Lifetime Question",
    "Out-parameters through references, a null-safe finder returning pointers, and reseating done right.",
    "Luyện Truy cập: Câu hỏi vòng đời",
    "Out-parameter qua tham chiếu, một hàm tìm kiếm an toàn với null trả về con trỏ, và gán lại con trỏ đúng cách.",
    L11B, 25, "beginner",
    [
        challenge(
            "cpp11-find-or-null",
            "Find or nullptr",
            "Implement `find_value(const std::vector<int>& v, int target)` returning a `const int*` to the first match, or `nullptr` if absent.",
            "#include <vector>\\n\\nconst int* find_value(const std::vector<int>& v, int target) {\\n    // TODO\\n}",
            [("found", "std::vector<int> v{4, 8, 15}; const int* r = find_value(v, 8); CHECK(r && *r == 8);", "Pointer to the first match."), ("absent", "std::vector<int> v{4, 8}; CHECK(find_value(v, 9) == nullptr);", "Missing → nullptr, not a dangling pointer."), ("empty", "std::vector<int> v; CHECK(find_value(v, 1) == nullptr);", "Empty vector → nullptr.")],
            level="guided",
        ),
    ],
    {"cpp11-find-or-null": vi_challenge("Tìm hoặc nullptr", "Cài đặt `find_value(const std::vector<int>& v, int target)` trả về một `const int*` trỏ tới kết quả khớp đầu tiên, hoặc `nullptr` nếu không có.", [("tìm thấy", "Con trỏ tới kết quả khớp đầu tiên."), ("không có", "Không có → nullptr, không phải con trỏ treo."), ("rỗng", "Vector rỗng → nullptr.")])},
    solutions=[
        ("cpp11-find-or-null", "#include <vector>\\nconst int* find_value(const std::vector<int>& v, int target) {\\n    for (const int& x : v) {\\n        if (x == target) return &x;\\n    }\\n    return nullptr;\\n}", "#include <vector>\\nconst int* find_value(const std::vector<int>& v, int target) {\\n    for (const int& x : v) {\\n        if (x == target) return &x;\\n    }\\n    return &v[0];\\n}"),
    ],
)

# ============================ MODULE 12: memory-raii ============================
M12 = "memory-raii"

L12A = "stack-heap-lifetime"
L12B = "raii-and-smart-pointers"
L12C = "the-new-delete-lesson"
L12D = "checkpoint-raii"

write_module(
    M12,
    "Memory, RAII & Smart Pointers",
    "Stack vs heap, ownership, RAII, unique_ptr/shared_ptr — and one honest lesson on why raw new/delete are not written in modern code.",
    "Bộ nhớ, RAII & Smart Pointer",
    "Stack so với heap, sở hữu, RAII, unique_ptr/shared_ptr — và một bài học trung thực về vì sao new/delete thô không được viết trong code hiện đại.",
    [L12A, L12B, L12C, L12D],
    ["m12-raii-practice"],
)

write_lesson(
    M12, L12A,
    "Stack, Heap, and Lifetime",
    "Where objects live, when they die, and why the lifetime question precedes every pointer question.",
    11,
    '''
## Two homes for objects

**The stack** — automatic storage. Local variables live here; the compiler allocates and frees them:

```cpp
void f() {
    int x{5};                          // born when the line runs
    std::vector<int> v{1, 2, 3};       // born; its ELEMENTS live on the heap (below)
}                                      // both die here — guaranteed, reverse order
```

Stack allocation is nearly free and lifetimes are exact: enter scope → live; leave scope → dead. Every local, nested, and temporary object follows this rule.

**The heap** — dynamic storage for things whose size or lifetime must be decided at runtime. The `vector`'s elements, a `std::string`'s characters, objects shared between scopes: their *contents* live on the heap, but their *handles* (the vector/string object itself) are still stack locals.

## The lifetime question — ask it first

For every object: **who is allowed to use it, and until when?**

```
stack local      → lives to end of scope (automatic)
heap object      → lives until SOMETHING releases it (the next lessons: what and how)
```

## The three classic bugs (know their names)

- **Memory leak** — heap memory allocated, never released; the program slowly bloats.
- **Use-after-free / dangling** — using memory that was already released.
- **Double-free** — releasing the same memory twice.

Every one of them is an *ownership* mistake: either nobody owned the memory, or two things thought they did. The cure is not vigilance; it is making ownership **explicit and automatic** — which is exactly RAII.
''',
    "Stack, Heap, và Vòng đời",
    "Đối tượng sống ở đâu, chết khi nào, và vì sao câu hỏi vòng đời đến trước mọi câu hỏi về con trỏ.",
    '''
## Hai ngôi nhà cho đối tượng

**Stack** — bộ nhớ tự động. Biến cục bộ sống ở đây; compiler cấp phát và giải phóng thay bạn:

```cpp
void f() {
    int x{5};                          // sinh ra khi dòng này chạy
    std::vector<int> v{1, 2, 3};       // sinh ra; các PHẦN TỬ của nó sống trên heap (dưới)
}                                      // cả hai chết ở đây — được bảo đảm, thứ tự ngược
```

Cấp phát trên stack gần như miễn phí và vòng đời chính xác: vào scope → sống; rời scope → chết. Mọi đối tượng cục bộ, lồng nhau, và tạm thời đều theo luật này.

**Heap** — bộ nhớ động cho những thứ mà kích thước hay vòng đời phải quyết định lúc chạy. Các phần tử của `vector`, ký tự của `std::string`, đối tượng dùng chung giữa các scope: *nội dung* của chúng sống trên heap, nhưng *tay cầm* (chính đối tượng vector/string) vẫn là biến cục bộ trên stack.

## Câu hỏi vòng đời — hãy hỏi trước tiên

Với mọi đối tượng: **ai được phép dùng nó, và đến khi nào?**

```
biến cục bộ trên stack → sống đến hết scope (tự động)
đối tượng trên heap    → sống cho đến khi CÓ GÌ ĐÓ giải phóng nó (các bài sau: cái gì và như thế nào)
```

## Ba loại bug kinh điển (hãy biết tên của chúng)

- **Memory leak** — bộ nhớ heap được cấp nhưng không bao giờ được trả; chương trình chậm rãi phình to.
- **Use-after-free / con trỏ treo** — dùng bộ nhớ đã được trả về.
- **Double-free** — trả cùng một vùng bộ nhớ hai lần.

Cả ba đều là lỗi *sở hữu*: hoặc không ai sở hữu vùng nhớ đó, hoặc có hai thứ cùng nghĩ mình sở hữu. Liều thuốc không phải là cảnh giác; mà là làm cho sở hữu trở nên **tường minh và tự động** — đó chính xác là RAII.
''',
)

write_lesson(
    M12, L12B,
    "RAII and Smart Pointers",
    "Resource Acquisition Is Initialization: the C++ superpower, unique_ptr as the default owner, shared_ptr with care.",
    12,
    '''
## RAII in one sentence

**Wrap every resource in an object whose destructor releases it.** Acquire in the constructor, release in the destructor. Since destructors run deterministically at scope exit — even during exceptions — resources can no longer leak in normal, well-written code.

You have used RAII all along: `std::vector` owns its heap buffer; `std::ifstream` owns its file handle (module 13); `std::lock_guard` owns a lock (Intermediate). Now make it conscious:

```cpp
class FileGuard {                 // a hand-rolled RAII wrapper (for understanding)
public:
    explicit FileGuard(std::FILE* f) : f_(f) {}
    ~FileGuard() { if (f_) std::fclose(f_); }        // THE release happens here — always
    FileGuard(const FileGuard&) = delete;            // one owner: copying forbidden
    FileGuard& operator=(const FileGuard&) = delete;
    std::FILE* get() const { return f_; }
private:
    std::FILE* f_;
};
```

## std::unique_ptr: the default owner

```cpp
#include <memory>

auto owned = std::make_unique<Report>("q3");   // heap object, ONE owner
owned->render();                                // use like a pointer: ->
// no delete anywhere — the destructor frees it automatically
```

- Exactly one owner; copying is deleted (moving *transfers* ownership and nulls the source).
- Zero overhead over a raw pointer.
- `std::make_unique<T>(args...)` is how you create it — never `new`.

## std::shared_ptr: when there really are several owners

```cpp
auto shared = std::make_shared<Sensor>();      // reference-counted ownership
auto alias = shared;                            // both keep it alive; last one out cleans up
CHECK_EQ(alias.use_count(), 2);
```

Shared ownership has real costs (atomic counters, surprise-persistence lifetimes, cycles that leak). Beginner rule: default `unique_ptr`, reach for `shared_ptr` only when a genuine multi-owner *lifetime* exists — and even then, hold non-owning views as raw pointers/references (observers), never as extra shared copies.

## weak_ptr (a glance)

`std::weak_ptr` observes a shared_ptr without owning — the tool for breaking ownership cycles (parent↔child). Know it exists; the capstone never needs it.
''',
    "RAII và Smart Pointer",
    "Resource Acquisition Is Initialization: siêu năng lực của C++, unique_ptr làm owner mặc định, shared_ptr dùng cẩn trọng.",
    '''
## RAII trong một câu

**Bọc mọi tài nguyên trong một đối tượng mà destructor của nó sẽ giải phóng tài nguyên đó.** Lấy tài nguyên trong constructor, trả lại trong destructor. Vì destructor chạy xác định khi ra khỏi scope — kể cả khi có exception — tài nguyên không còn cách nào rò rỉ trong code viết tốt, thông thường.

Bạn đã dùng RAII suốt từ đầu: `std::vector` sở hữu buffer heap của nó; `std::ifstream` sở hữu file handle (module 13); `std::lock_guard` sở hữu một khóa (Trung cấp). Bây giờ hãy làm điều đó thành ý thức:

```cpp
class FileGuard {                 // một lớp bọc RAII viết tay (để hiểu)
public:
    explicit FileGuard(std::FILE* f) : f_(f) {}
    ~FileGuard() { if (f_) std::fclose(f_); }        // VIỆC trả tài nguyên xảy ra ở đây — luôn luôn
    FileGuard(const FileGuard&) = delete;            // một owner: cấm sao chép
    FileGuard& operator=(const FileGuard&) = delete;
    std::FILE* get() const { return f_; }
private:
    std::FILE* f_;
};
```

## std::unique_ptr: owner mặc định

```cpp
#include <memory>

auto owned = std::make_unique<Report>("q3");   // đối tượng heap, MỘT owner
owned->render();                                // dùng như con trỏ: ->
// không có delete ở bất kỳ đâu — destructor tự giải phóng
```

- Đúng một owner; sao chép bị cấm (move *chuyển giao* sở hữu và làm nguồn rỗng).
- Chi phí bằng không so với con trỏ thô.
- `std::make_unique<T>(args...)` là cách tạo nó — không bao giờ `new`.

## std::shared_ptr: khi thật sự có nhiều owner

```cpp
auto shared = std::make_shared<Sensor>();      // sở hữu theo bộ đếm tham chiếu
auto alias = shared;                            // cả hai giữ nó sống; người cuối cùng dọn dẹp
CHECK_EQ(alias.use_count(), 2);
```

Sở hữu dùng chung có chi phí thật (bộ đếm atomic, vòng đời "sống dai" bất ngờ, chu kỳ gây leak). Quy tắc người mới: mặc định `unique_ptr`, chỉ với tới `shared_ptr` khi có một *vòng đời* nhiều owner thật sự — và dù thế nào, hãy giữ các cái nhìn không-owning dưới dạng con trỏ thô/tham chiếu (observer), không bao giờ là các bản sao shared thêm.

## weak_ptr (liếc qua)

`std::weak_ptr` quan sát một shared_ptr mà không sở hữu — công cụ phá các chu kỳ sở hữu (cha↔con). Biết nó tồn tại; capstone không cần đến nó.
''',
)

write_lesson(
    M12, L12C,
    "The new/delete Lesson",
    "Read legacy owning-pointer code, name its exact failure modes, and translate it to modern C++ — the one and only time you write new/delete here.",
    11,
    '''
## The legacy pattern you WILL meet

```cpp
// Legacy style — for reading only. Never write this in new code.
Report* make_report() {
    Report* r = new Report("legacy");    // heap allocation, manual ownership
    return r;
}

void use() {
    Report* r = make_report();
    if (r->is_empty()) return;           // LEAK: early return skips the delete below
    r->render();
    delete r;                            // manual release — one path among many
}
```

Every line is a decision a human must remember forever. The failure modes are exactly module 12A's list, and this 12-line function already leaks: the early return. Real functions have loops, exceptions, and ten return paths — manual cleanup does not survive contact with real control flow.

## The same code, modern

```cpp
std::unique_ptr<Report> make_report() {
    return std::make_unique<Report>("modern");
}

void use() {
    auto r = make_report();
    if (r->is_empty()) return;     // no leak: unique_ptr's destructor runs
    r->render();
}                                   // freed here — every path, including throws
```

Ownership became a *type*. The compiler now enforces what the legacy version begged humans to remember.

## Your exercise: translator, not author

This module's challenges hand you legacy `new`/`delete` code and ask you to (1) name the bug, (2) rewrite it with RAII. You will write `new`/`delete` exactly once in this course — inside the "spot the bug" lesson, as the patient on the operating table. That is deliberate: Core Guidelines R.11 warns against `new`/`delete` outside low-level ownership code, and even there, wrapped.

## When DO raw pointers appear in modern code?

- **Non-owning observers**: a function parameter `const Report*` that may be null, or a class member that views another object it does not own.
- **Interop** with C-style APIs.
- **Inside the standard library and low-level ownership code** you will study in Intermediate.

Ownership flows through types (`unique_ptr`, containers, by-value members); access flows through references and non-owning pointers. That sentence is the module.
''',
    "Bài học new/delete",
    "Đọc code legacy dùng con trỏ sở hữu, gọi tên chính xác các kiểu lỗi của nó, và dịch sang C++ hiện đại — lần duy nhất bạn viết new/delete trong khóa này.",
    '''
## Mẫu legacy bạn SẼ gặp

```cpp
// Kiểu legacy — chỉ để đọc. Đừng bao giờ viết thế này trong code mới.
Report* make_report() {
    Report* r = new Report("legacy");    // cấp phát heap, sở hữu thủ công
    return r;
}

void use() {
    Report* r = make_report();
    if (r->is_empty()) return;           // LEAK: return sớm bỏ qua delete phía dưới
    r->render();
    delete r;                            // giải phóng thủ công — một đường trong nhiều đường
}
```

Mỗi dòng là một quyết định mà con người phải nhớ mãi mãi. Các kiểu lỗi đúng bằng danh sách của bài 12A, và hàm 12 dòng này đã rò rỉ ngay: lệnh return sớm. Hàm thật có vòng lặp, exception, và mười đường return — dọn dẹp thủ công không sống sót trước luồng điều khiển thật.

## Cùng đoạn code, phiên bản hiện đại

```cpp
std::unique_ptr<Report> make_report() {
    return std::make_unique<Report>("modern");
}

void use() {
    auto r = make_report();
    if (r->is_empty()) return;     // không leak: destructor của unique_ptr chạy
    r->render();
}                                   // giải phóng ở đây — mọi đường đi, kể cả khi ném exception
```

Sở hữu trở thành một *kiểu dữ liệu*. Compiler giờ thực thi điều mà phiên bản legacy chỉ có thể cầu xin con người ghi nhớ.

## Bài tập của bạn: dịch, không phải sáng tác

Các challenge của module này đưa cho bạn code legacy `new`/`delete` và yêu cầu bạn (1) gọi tên bug, (2) viết lại bằng RAII. Bạn sẽ viết `new`/`delete` đúng một lần trong khóa này — trong bài "tìm bug", với tư cách bệnh nhân trên bàn mổ. Điều đó là chủ ý: Core Guidelines R.11 khuyến cáo tránh `new`/`delete` ngoài code sở hữu cấp thấp, và ngay cả ở đó, cũng phải được bọc lại.

## Khi nào con trỏ thô TỒN TẠI trong code hiện đại?

- **Observer không-owning**: tham số hàm `const Report*` có thể null, hoặc thành viên lớp nhìn một đối tượng khác mà không sở hữu nó.
- **Tương thích** với API kiểu C.
- **Bên trong thư viện chuẩn và code sở hữu cấp thấp** bạn sẽ học ở Trung cấp.

Sở hữu chảy qua các kiểu (`unique_ptr`, container, thành viên theo giá trị); truy cập chảy qua tham chiếu và con trỏ không-owning. Câu đó chính là toàn bộ module này.
''',
)

# ---- Module 12 checkpoint ----
write_checkpoint(
    M12, L12D,
    "Checkpoint: RAII",
    "One graded challenge: translate legacy new/delete into RAII and prove the resource behavior.",
    15,
    '''
**Checkpoint — RAII.** Pass the graded challenge below to finish the module.

You will implement a small RAII owner (constructor acquires, destructor releases, copy deleted) — the pattern behind every smart pointer and every file stream.
''',
    "Checkpoint: RAII",
    "Một challenge có chấm: dịch legacy new/delete sang RAII và chứng minh hành vi tài nguyên.",
    '''
**Checkpoint — RAII.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Bạn sẽ cài một RAII owner nhỏ (constructor lấy tài nguyên, destructor trả lại, cấm sao chép) — mẫu hình đứng sau mọi smart pointer và mọi file stream.
''',
    challenge(
        "cpp12-check-raii-owner",
        "RAII Owner",
        "Implement class `IntBox`: constructor `explicit IntBox(int value)` stores a heap `int` (using new — the one sanctioned place), `get() const` returns the value, destructor frees it. Deleting copy construction/assignment is required. Then implement `make_doubled(int)` returning `std::unique_ptr<IntBox>` holding the doubled value.",
        "#include <memory>\\n\\nclass IntBox {\\npublic:\\n    // TODO\\nprivate:\\n    // TODO\\n};\\n\\nstd::unique_ptr<IntBox> make_doubled(int v) {\\n    // TODO\\n}",
        [
            ("stores", "IntBox b{21}; CHECK_EQ(b.get(), 21);", "Constructor acquires and stores."),
            ("doubled", "auto p = make_doubled(21); CHECK_EQ(p->get(), 42);", "make_unique with the doubled value."),
            ("no copy", "static_assert(!std::is_copy_constructible<IntBox>::value, \"must be non-copyable\"); CHECK(true);", "Copy construction must be deleted — one owner."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "RAII Owner",
        "Cài đặt lớp `IntBox`: constructor `explicit IntBox(int value)` lưu một `int` trên heap (dùng new — chỗ duy nhất được phép), `get() const` trả về giá trị, destructor giải phóng nó. Việc cấm copy constructor/assignment là bắt buộc. Sau đó cài `make_doubled(int)` trả về `std::unique_ptr<IntBox>` giữ giá trị nhân đôi.",
        [("lưu trữ", "Constructor lấy và lưu giá trị."), ("nhân đôi", "make_unique với giá trị đã nhân đôi."), ("cấm sao chép", "Copy constructor phải bị xóa — chỉ một owner.")],
    ),
    solution="#include <memory>\\n#include <type_traits>\\nclass IntBox {\\npublic:\\n    explicit IntBox(int value) : data_(new int{value}) {}\\n    ~IntBox() { delete data_; }\\n    IntBox(const IntBox&) = delete;\\n    IntBox& operator=(const IntBox&) = delete;\\n    int get() const { return *data_; }\\nprivate:\\n    int* data_;\\n};\\n\\nstd::unique_ptr<IntBox> make_doubled(int v) {\\n    return std::make_unique<IntBox>(v * 2);\\n}",
    wrong="#include <memory>\\n#include <type_traits>\\nclass IntBox {\\npublic:\\n    explicit IntBox(int value) : data_(new int{value}) {}\\n    ~IntBox() { delete data_; }\\n    int get() const { return *data_; }\\nprivate:\\n    int* data_;\\n};\\n\\nstd::unique_ptr<IntBox> make_doubled(int v) {\\n    return std::make_unique<IntBox>(v * 2);\\n}",
)

# ---- Module 12 practice ----
write_practice(
    M12, "m12-raii-practice",
    "RAII Practice: Own It Once",
    "Name-the-bug on leaking code, unique_ptr transfers, and a shared_ptr use-count check.",
    "Luyện RAII: Sở hữu một lần thôi",
    "Gọi tên bug trên code rò rỉ, chuyển giao unique_ptr, và kiểm tra use-count của shared_ptr.",
    L12B, 25, "beginner",
    [
        challenge(
            "cpp12-move-owner",
            "Ownership Transfer",
            "Implement `make_counter()` returning `std::unique_ptr<int>` holding 0, and `take_and_bump(std::unique_ptr<int> p)` that increments the value and RETURNS the same pointer onward.",
            "#include <memory>\\n\\nstd::unique_ptr<int> make_counter() {\\n    // TODO\\n}\\nstd::unique_ptr<int> take_and_bump(std::unique_ptr<int> p) {\\n    // TODO: bump the int, then return p (ownership flows on)\\n}",
            [("create", "auto p = make_counter(); CHECK(p && *p == 0);", "make_unique, not new."), ("bump", "auto p = make_counter(); ++(*p); auto q = take_and_bump(std::move(p)); CHECK(q && *q == 1);", "Ownership moves in and straight back out; the value is incremented."), ("source emptied", "auto p = make_counter(); auto q = take_and_bump(std::move(p)); CHECK(p == nullptr);", "After the move, the source unique_ptr is null — ownership moved.")],
            level="independent",
        ),
    ],
    {"cpp12-move-owner": vi_challenge("Chuyển giao sở hữu", "Cài `make_counter()` trả về `std::unique_ptr<int>` giữ giá trị 0, và `take_and_bump(std::unique_ptr<int> p)` tăng giá trị rồi TRẢ VỀ chính con trỏ đó.", [("tạo", "make_unique, không phải new."), ("tăng", "Sở hữu đi vào rồi đi thẳng ra; giá trị được tăng."), ("nguồn rỗng", "Sau lệnh move, unique_ptr nguồn là null — sở hữu đã chuyển đi.")])},
    solutions=[
        ("cpp12-move-owner", "#include <memory>\\nstd::unique_ptr<int> make_counter() {\\n    return std::make_unique<int>(0);\\n}\\nstd::unique_ptr<int> take_and_bump(std::unique_ptr<int> p) {\\n    ++(*p);\\n    return p;\\n}", "#include <memory>\\nstd::unique_ptr<int> make_counter() {\\n    return std::make_unique<int>(0);\\n}\\nstd::unique_ptr<int> take_and_bump(std::unique_ptr<int> p) {\\n    ++(*p);\\n    return std::make_unique<int>(*p);\\n}"),
    ],
)

print("modules 9-12 authored")
