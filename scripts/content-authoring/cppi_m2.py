#!/usr/bin/env python3
"""C++ Intermediate — Module 2: object-oriented C++ (classes, ctors/dtors, static, composition)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "object-oriented-design"

# ── lesson texts ─────────────────────────────────────────────────────────────
L_CLASSES_EN = """
A **class** bundles state and the operations that keep that state valid.
Beginner showed you `class` for encapsulation; now we use it as a design tool:
decide the invariant first, then expose only operations that preserve it.

```cpp
#include <string>

class Timer {
public:
    void start() { running_ = true; ++starts_; }
    void stop()  { running_ = false; }
    bool running() const { return running_; }
    int  starts() const { return starts_; }   // invariant: counts every start

private:
    bool running_{false};
    int  starts_{0};
};
```

The invariant here is trivial ("starts_ counts calls to start"), but the
*shape* is what matters: state is private, operations are the only door,
`const` marks the read-only half of the interface.

## Design order that works

1. Write down the invariant in one sentence.
2. Choose members that make the invariant easy to keep.
3. Expose operations; make anything the invariant needs `private`.
4. Mark non-mutating operations `const`.

## Struct vs class, honestly

The only difference is the default access (`struct` public, `class` private).
Use `struct` for passive data aggregates, `class` when there is an invariant
to defend. Both are "classes" in C++'s eyes.
"""

L_CLASSES_VI = """
**Class** gộp trạng thái và các thao tác giữ trạng thái đó hợp lệ. Cơ bản đã
cho bạn `class` để đóng gói; giờ ta dùng nó như công cụ thiết kế: chọn bất
biến trước, rồi chỉ mở những thao tác giữ gìn bất biến đó.

```cpp
#include <string>

class Timer {
public:
    void start() { running_ = true; ++starts_; }
    void stop()  { running_ = false; }
    bool running() const { return running_; }
    int  starts() const { return starts_; }   // bất biến: đếm mọi lần start

private:
    bool running_{false};
    int  starts_{0};
};
```

Bất biến ở đây đơn giản ("starts_ đếm mỗi lần gọi start"), nhưng *hình dạng*
mới là điều quan trọng: trạng thái private, thao tác là cánh cửa duy nhất,
`const` đánh dấu nửa chỉ-đọc của interface.

## Thứ tự thiết kế hiệu quả

1. Viết bất biến trong một câu.
2. Chọn member khiến bất biến dễ được giữ.
3. Mở thao tác; đặt `private` cho mọi thứ bất biến cần.
4. Đánh dấu `const` cho thao tác không làm thay đổi.

## Struct với class, nói thẳng

Khác biệt duy nhất là quyền truy cập mặc định (`struct` public, `class`
private). Dùng `struct` cho gói dữ liệu thụ động, `class` khi có bất biến cần
bảo vệ. Với C++, cả hai đều là "class".
"""

L_CTOR_EN = """
**Constructors** put a new object into a valid state. C++ gives you several
kinds; you rarely need all of them, but you must recognize each.

```cpp
#include <string>
#include <vector>

class Inventory {
public:
    Inventory() = default;                          // default ctor
    explicit Inventory(int cap) : cap_{cap} {}      // converting ctor → explicit!
    Inventory(std::string owner, int cap)           // multi-parameter
        : owner_{std::move(owner)}, cap_{cap} {}

private:
    std::string owner_{"warehouse"};
    int cap_{0};
    std::vector<int> items_{};
};
```

## Member initializer lists

Prefer `: member_{value}` over assigning in the body — members are initialized
once, directly, and `const`/reference members have no other option. The order
of the list does not matter; **members initialize in declaration order**.

## explicit, always for one-argument constructors

Without `explicit`, `Inventory inv = 5;` compiles — a silent conversion from
`int`. `explicit` makes that a compile error while `Inventory inv{5};` still
works. Default rule: single-argument constructors are `explicit` unless you
*mean* implicit conversion.

## When you write none

If you declare no constructors, the compiler generates a default one that
value-initializes members with `{}` defaults. Often that is all you need —
`struct Point { double x{}; double y{}; };` needs nothing else.
"""

L_CTOR_VI = """
**Constructor** đưa đối tượng mới vào trạng thái hợp lệ. C++ cho bạn vài loại;
bạn hiếm khi cần hết, nhưng phải nhận ra từng loại.

```cpp
#include <string>
#include <vector>

class Inventory {
public:
    Inventory() = default;                          // default ctor
    explicit Inventory(int cap) : cap_{cap} {}      // ctor chuyển đổi → explicit!
    Inventory(std::string owner, int cap)           // nhiều tham số
        : owner_{std::move(owner)}, cap_{cap} {}

private:
    std::string owner_{"warehouse"};
    int cap_{0};
    std::vector<int> items_{};
};
```

## Member initializer list

Ưu tiên `: member_{value}` thay vì gán trong thân hàm — member được khởi tạo
một lần, trực tiếp, còn member `const`/reference không có lựa chọn nào khác.
Thứ tự trong list không quan trọng; **member khởi tạo theo thứ tự khai báo**.

## explicit, luôn cho constructor một tham số

Không có `explicit`, `Inventory inv = 5;` vẫn biên dịch — một chuyển đổi ngầm
từ `int`. `explicit` biến điều đó thành lỗi biên dịch, trong khi
`Inventory inv{5};` vẫn chạy. Quy tắc mặc định: constructor một tham số thì
`explicit`, trừ khi bạn *cố ý* cho chuyển đổi ngầm.

## Khi bạn không viết gì

Nếu bạn không khai báo constructor nào, compiler sinh một constructor mặc định
khởi tạo giá trị các member có mặc định `{}`. Thường là đủ —
`struct Point { double x{}; double y{}; };` không cần gì thêm.
"""

L_DTOR_EN = """
A **destructor** (`~ClassName`) runs automatically when an object dies —
scope exit for automatic objects, `delete` for heap objects, container
shrinking for elements. It is the "~" half of RAII: acquire in the
constructor, release in the destructor.

```cpp
#include <cstdio>

class FileLog {
public:
    explicit FileLog(const char* path) : handle_{std::fopen(path, "a")} {}
    ~FileLog() { if (handle_) std::fclose(handle_); }   // ALWAYS runs

    FileLog(const FileLog&) = delete;            // (Module 4: copy control)
    FileLog& operator=(const FileLog&) = delete;

private:
    std::FILE* handle_;
};

void use() {
    FileLog log{"app.log"};   // acquire
    // ... write via log ...
}                             // destructor closes the file — even on throw
```

## What belongs in a destructor

Only releasing what the object **owns**: file handles, locks, sockets,
heap memory. Members that own themselves (a `std::string` member, a
`std::vector` member) destroy themselves — you never write
`delete member_` for a value member.

## The two rules for now

1. If the class holds a raw resource it acquired, it needs a destructor.
2. If it does not hold one, **write no destructor at all** — the implicit one
   is correct, and a hand-written empty one only invites mistakes.

Deletion order: members destroy in reverse declaration order, then the
body runs... actually the body runs *first*, then members destroy in
reverse order. Base parts (Module 3) destroy after the derived body.
"""

L_DTOR_VI = """
**Destructor** (`~ClassName`) chạy tự động khi đối tượng chết — hết phạm vi
với đối tượng tự động, khi `delete` với đối tượng heap, khi container co lại
với phần tử. Nó là nửa "~" của RAII: lấy tài nguyên trong constructor, giải
phóng trong destructor.

```cpp
#include <cstdio>

class FileLog {
public:
    explicit FileLog(const char* path) : handle_{std::fopen(path, "a")} {}
    ~FileLog() { if (handle_) std::fclose(handle_); }   // LUÔN chạy

    FileLog(const FileLog&) = delete;            // (Module 4: copy control)
    FileLog& operator=(const FileLog&) = delete;

private:
    std::FILE* handle_;
};

void use() {
    FileLog log{"app.log"};   // lấy tài nguyên
    // ... ghi qua log ...
}                             // destructor đóng file — kể cả khi có exception
```

## Điều gì thuộc về destructor

Chỉ giải phóng những gì đối tượng **sở hữu**: file handle, lock, socket, bộ
nhớ heap. Member tự sở hữu mình (member `std::string`, member `std::vector`)
tự hủy — bạn không bao giờ viết `delete member_` cho member kiểu giá trị.

## Hai quy tắc cho hiện tại

1. Nếu class giữ tài nguyên thô nó tự lấy, nó cần một destructor.
2. Nếu không giữ, **đừng viết destructor** — bản ngầm định đã đúng, còn một
   destructor rỗng tay chỉ mời gọi sai sót.

Thứ tự hủy: thân hàm chạy *trước*, rồi member hủy theo thứ tự ngược khai báo.
Phần base (Module 3) hủy sau thân của derived.
"""

L_STATIC_EN = """
A **static member** belongs to the class, not to any one object: one copy
shared by every instance. Static data members are declared in the class and
defined once outside it (C++17 allows in-class initialization with
`inline`).

```cpp
#include <string>
#include <vector>

class IdGenerator {
public:
    static int next() { return ++counter_; }   // static member function: no this

private:
    inline static int counter_{0};             // one shared int
};

class Registry {
public:
    void add(std::string name) { names_.push_back(std::move(name)); }
    static std::size_t count(const Registry& r) { return r.names_.size(); }

private:
    std::vector<std::string> names_;
};
```

## The two kinds, cleanly separated

- **static data member** — shared state across all instances (counters, caches, config).
- **static member function** — callable without an object; has no `this`,
  so it may not touch non-static members (it may read *others'* via a parameter).

## Accessing

`ClassName::member` from anywhere with access; `member` from inside class
scope. Use cases that actually justify static state: instance counting,
shared immutable configuration, factory helpers. Everything else should be a
plain object — global mutable state is a design smell you will meet in
debugging challenges.
"""

L_STATIC_VI = """
**Static member** thuộc về class, không thuộc một đối tượng nào: một bản sao
duy nhất dùng chung cho mọi instance. Static data member được khai báo trong
class và định nghĩa một lần bên ngoài (C++17 cho phép khởi tạo ngay trong
class với `inline`).

```cpp
#include <string>
#include <vector>

class IdGenerator {
public:
    static int next() { return ++counter_; }   // hàm static: không có this

private:
    inline static int counter_{0};             // một int dùng chung
};

class Registry {
public:
    void add(std::string name) { names_.push_back(std::move(name)); }
    static std::size_t count(const Registry& r) { return r.names_.size(); }

private:
    std::vector<std::string> names_;
};
```

## Hai loại, tách bạch

- **static data member** — trạng thái dùng chung giữa mọi instance (bộ đếm, cache, cấu hình).
- **hàm thành viên static** — gọi được mà không cần đối tượng; không có `this`,
  nên không được đụng member thường (nhưng đọc được của *người khác* qua tham số).

## Truy cập

`ClassName::member` từ bất kỳ đâu có quyền; `member` từ bên trong phạm vi
class. Những trường hợp thực sự xứng đáng có static state: đếm instance, cấu
hình bất biến dùng chung, hàm factory. Còn lại nên là đối tượng thường —
trạng thái toàn cục mutable là mùi thiết kế bạn sẽ gặp trong bài gỡ lỗi.
"""

L_THIS_EN = """
Inside every non-static member function, `this` is the address of the object
the call runs on. You rarely *write* it — `balance_` means `this->balance_` —
but you use it deliberately in three places.

```cpp
#include <string>

class Account {
public:
    Account& deposit(long cents) {          // returning *this enables chaining
        balance_ += cents;
        return *this;
    }
    Account& withdraw(long cents) {
        balance_ -= cents;
        return *this;
    }
    bool same_as(const Account& other) const {
        return this == &other;               // identity: addresses compared
    }
    long balance() const { return balance_; }

private:
    long balance_{0};
};

// chaining: a.deposit(100).withdraw(30).deposit(5);
```

## The three deliberate uses

1. **Return `*this`** by reference for chaining and for assignment operators
   (Module 4's `operator=` does exactly this).
2. **Identity comparisons** — `this == &other` answers "is it literally the
   same object?" (distinct from `==` meaning equal values).
3. **Disambiguation** — when a parameter shadows a member, `this->name` picks
   the member; better, rename instead.

In `const` member functions, `this` is `const Account*` — that is the whole
mechanism by which const propagates to members.
"""

L_THIS_VI = """
Trong mọi hàm thành viên non-static, `this` là địa chỉ của đối tượng mà lời
gọi đang chạy trên đó. Bạn hiếm khi *viết* nó — `balance_` chính là
`this->balance_` — nhưng có ba chỗ bạn dùng nó một cách chủ đích.

```cpp
#include <string>

class Account {
public:
    Account& deposit(long cents) {          // trả *this để nối chuỗi lời gọi
        balance_ += cents;
        return *this;
    }
    Account& withdraw(long cents) {
        balance_ -= cents;
        return *this;
    }
    bool same_as(const Account& other) const {
        return this == &other;               // bản sắc: so địa chỉ
    }
    long balance() const { return balance_; }

private:
    long balance_{0};
};

// nối chuỗi: a.deposit(100).withdraw(30).deposit(5);
```

## Ba cách dùng chủ đích

1. **Trả `*this`** bằng reference để nối chuỗi và cho các toán tử gán
   (`operator=` ở Module 4 làm đúng điều này).
2. **So sánh bản sắc** — `this == &other` trả lời "có phải literally cùng một
   đối tượng?" (khác với `==` nghĩa là giá trị bằng nhau).
3. **Phân biệt** — khi tham số che member, `this->name` chọn member; tốt hơn
   hãy đổi tên.

Trong hàm thành viên `const`, `this` có kiểu `const Account*` — đó là toàn bộ
cơ chế để const lan xuống các member.
"""

L_COMP_EN = """
**Composition** — building a class out of member objects — is the default
relationship in C++. Inheritance (next module) is for substitutability, not
for code reuse; most "is-a" instincts are really "has-a".

```cpp
#include <string>
#include <vector>

class Engine {
public:
    void start() { running_ = true; }
    bool running() const { return running_; }
private:
    bool running_{false};
};

class Car {
public:
    void drive() { engine_.start(); }        // delegates; owns an Engine
    bool ready() const { return engine_.running(); }
private:
    Engine engine_;                           // composition: Car HAS an Engine
    std::vector<std::string> trips_;          // and HAS a trip log
};
```

## Why composition first

- The member's invariants stay encapsulated inside it; `Car` cannot corrupt
  `Engine`'s internals.
- Lifetime is automatic: `Car`'s members construct and destroy with it, in
  declaration order.
- Swapping an implementation (a `Battery` instead of `Engine`) touches one
  member declaration, not a hierarchy.

## When inheritance is genuinely right

When callers must treat different types uniformly *through one interface* —
shapes drawn the same way, handlers invoked the same way. If you cannot point
at a call site that holds a base-class reference/pointer, you do not need
inheritance. That call-site test decides Module 3's design exercises too.
"""

L_COMP_VI = """
**Composition** — xây class từ các đối tượng thành viên — là quan hệ mặc định
trong C++. Kế thừa (module sau) dùng cho khả năng thay thế, không phải để tái
sử dụng mã; phần lớn trực giác "is-a" thực ra là "has-a".

```cpp
#include <string>
#include <vector>

class Engine {
public:
    void start() { running_ = true; }
    bool running() const { return running_; }
private:
    bool running_{false};
};

class Car {
public:
    void drive() { engine_.start(); }        // ủy quyền; sở hữu một Engine
    bool ready() const { return engine_.running(); }
private:
    Engine engine_;                           // composition: Car CÓ một Engine
    std::vector<std::string> trips_;          // và CÓ nhật ký chuyến đi
};
```

## Vì sao composition trước

- Bất biến của member được đóng gói bên trong nó; `Car` không thể làm hỏng
  phần bên trong của `Engine`.
- Vòng đời tự động: member của `Car` khởi tạo và hủy cùng nó, theo thứ tự khai báo.
- Đổi một thành phần (thay `Engine` bằng `Battery`) chỉ đụng một dòng khai
  báo member, không phải cả một cây kế thừa.

## Khi nào kế thừa thực sự đúng

Khi bên gọi phải xử lý nhiều kiểu khác nhau *thông qua một interface* — các
hình vẽ cùng một cách, các handler được gọi cùng một cách. Nếu bạn không chỉ
ra được một điểm gọi nào giữ base-class reference/pointer thì bạn không cần
kế thừa. Bài test call-site này cũng quyết định các bài thiết kế ở Module 3.
"""

# ── practice sets ────────────────────────────────────────────────────────────
P1 = [
    challenge(
        "cppi-m2-class-counter",
        "A class with an invariant",
        "Implement `class BoundedCounter` with a private `int value_{0};` and private `int max_;`, a constructor `BoundedCounter(int max)` that stores `max` (assume positive), `void increment()` that increments unless doing so would exceed `max`, and `int value() const` / `int max() const` getters.",
        "#include <iostream>\n\nclass BoundedCounter {\n    // declarations\n};\n",
        [
            ("stops-at-max", "BoundedCounter c{3};\nc.increment(); c.increment(); c.increment(); c.increment();\nCHECK_EQ(c.value(), 3);", "The fourth increment would exceed max 3 → invariant forbids it."),
            ("starts-at-zero", "BoundedCounter c{5};\nCHECK_EQ(c.value(), 0);", "New counters start at 0."),
            ("getters-const", "BoundedCounter c{5};\nc.increment();\nconst BoundedCounter& view = c;\nCHECK_EQ(view.value(), 1);\nCHECK_EQ(view.max(), 5);", "Both getters must work through a const reference."),
        ],
        level="combination",
    ),
    challenge(
        "cppi-m2-ctor-explicit",
        "explicit shuts the trap",
        "Implement `class Meters` with `explicit Meters(double v)` storing `v` privately and `double value() const`. The test proves `Meters m = 3.0;` must NOT compile while `Meters m{3.0};` must — your class needs exactly one `explicit` one-argument constructor.",
        "#include <iostream>\n\nclass Meters {\n    // one explicit ctor + getter\n};\n",
        [
            ("brace-init", "Meters m{3.0};\nCHECK_NEAR(m.value(), 3.0, 1e-9);", "Direct initialization with braces works with explicit."),
            ("copy-list", "Meters m{2.5};\nMeters n{m};\nCHECK_NEAR(n.value(), 2.5, 1e-9);", "Copy from an existing object is still allowed."),
        ],
        level="guided",
    ),
    challenge(
        "cppi-m2-class-initializer-order",
        "Member initialization order",
        "Implement `class EventLog` with members `std::string name_;` then `int id_;` declared IN THAT ORDER, a constructor `EventLog(int id, std::string name)` initializing both via the member initializer list, and getters `const std::string& name() const` / `int id() const`.",
        "#include <string>\n#include <iostream>\n\nclass EventLog {\n    // name_ then id_, ctor, getters\n};\n",
        [
            ("values", 'EventLog e{7, "deploy"};\nCHECK_EQ(e.name(), "deploy");\nCHECK_EQ(e.id(), 7);', "Initializer list maps parameters to members regardless of order."),
            ("reference-getter", 'EventLog e{1, "x"};\nconst std::string& ref = e.name();\nCHECK_EQ(ref, "x");', "name() returns a const& — a borrow, not a copy."),
        ],
        level="independent",
    ),
]

P2 = [
    challenge(
        "cppi-m2-static-counter",
        "Count every instance",
        "Implement `class Tracked` with an `inline static int live_;` and `inline static int created_;`. The constructor increments both; the destructor decrements `live_`. Provide static getters `int live()` and `int created()`.",
        "#include <iostream>\n\nclass Tracked {\n    // ctor, dtor, inline static members, static getters\n};\n",
        [
            ("created", "Tracked a;\nTracked b;\n{ Tracked c; }\nCHECK_EQ(Tracked::created(), 3);", "created_ never decreases — it counts constructions."),
            ("live", "CHECK_EQ(Tracked::live(), 2);", "After the inner block, c's destructor ran → live is back to 2."),
            ("no-instance", "CHECK(Tracked::created() >= 2);", "Static members are callable without any instance."),
        ],
        level="combination",
    ),
    challenge(
        "cppi-m2-this-chain",
        "Chaining through *this",
        "Implement `class Ledger` with private `long total_{0};`, `Ledger& add(long cents)` and `Ledger& undo(long cents)` (each updates `total_` and returns `*this`), plus `long total() const`. The test chains calls.",
        "#include <iostream>\n\nclass Ledger {\n    // add/undo returning Ledger&, total getter\n};\n",
        [
            ("chain", "Ledger l;\nl.add(100).undo(30).add(5);\nCHECK_EQ(l.total(), 75);", "Each call returns the same object → chaining works."),
            ("single", "Ledger l;\nl.add(50);\nCHECK_EQ(l.total(), 50);", "Single calls behave like plain mutators."),
        ],
        level="guided",
    ),
    challenge(
        "cppi-m2-composition-engine",
        "Composition: a Car HAS an Engine",
        "Implement `class Engine` with `void start()`, `bool running() const` (private `bool running_{false};`), and `class Car` that owns an `Engine engine_` member plus `std::string model_;`, with `void drive()` (starts the engine) and `bool ready() const` (engine running).",
        "#include <string>\n#include <iostream>\n\nclass Engine { /* ... */ };\n\nclass Car { /* owns an Engine */ };\n",
        [
            ("delegation", 'Car c{"kia"};\nc.drive();\nCHECK(c.ready());', "Car exposes Engine's effect without exposing the Engine."),
            ("fresh-car", 'Car c{"honda"};\nCHECK(!c.ready());', "A new car's engine is not running."),
            ("model", 'Car c{"kia"};\nCHECK_EQ(c.model(), "kia");', "Car carries its own state too."),
        ],
        level="mini-build",
    ),
]

VI_P1 = {
    "cppi-m2-class-counter": vi_challenge("Class với bất biến", "Cài `class BoundedCounter` với `int value_{0};` và `int max_;` private, constructor `BoundedCounter(int max)` (giả sử max dương), `void increment()` chỉ tăng khi không vượt `max`, và getter `int value() const` / `int max() const`.", [("stops-at-max", "Lần tăng thứ tư sẽ vượt max 3 → bất biến cấm."), ("starts-at-zero", "Counter mới bắt đầu ở 0."), ("getters-const", "Cả hai getter phải gọi được qua const reference.")]),
    "cppi-m2-ctor-explicit": vi_challenge("explicit chặn cái bẫy", "Cài `class Meters` với `explicit Meters(double v)` lưu `v` private và `double value() const`. Test chứng minh `Meters m = 3.0;` phải KHÔNG biên dịch còn `Meters m{3.0};` phải chạy — class của bạn cần đúng một constructor một tham số có `explicit`.", [("brace-init", "Khởi tạo trực tiếp bằng ngoặc nhọn vẫn chạy với explicit."), ("copy-list", "Copy từ đối tượng có sẵn vẫn được phép.")]),
    "cppi-m2-class-initializer-order": vi_challenge('Thứ tự khởi tạo member', "Cài `class EventLog` với member `std::string name_;` rồi `int id_;` khai báo ĐÚNG THỨ TỰ đó, constructor `EventLog(int id, std::string name)` khởi tạo cả hai qua member initializer list, và getter `const std::string& name() const` / `int id() const`.", [("values", "Initializer list gán tham số vào member bất kể thứ tự."), ("reference-getter", "name() trả const& — một lần mượn, không phải bản sao.")]),
}

VI_P2 = {
    "cppi-m2-static-counter": vi_challenge("Đếm mọi instance", "Cài `class Tracked` với `inline static int live_;` và `inline static int created_;`. Constructor tăng cả hai; destructor giảm `live_`. Cung cấp static getter `int live()` và `int created()`.", [("created", "created_ không bao giờ giảm — nó đếm số lần khởi tạo."), ("live", "Sau khối trong, destructor của c đã chạy → live về 2."), ("no-instance", "Static member gọi được mà không cần instance nào.")]),
    "cppi-m2-this-chain": vi_challenge("Nối chuỗi qua *this", "Cài `class Ledger` với `long total_{0};` private, `Ledger& add(long cents)` và `Ledger& undo(long cents)` (mỗi hàm cập nhật `total_` và trả `*this`), cùng `long total() const`. Test nối chuỗi lời gọi.", [("chain", "Mỗi lời gọi trả cùng một đối tượng → nối chuỗi chạy được."), ("single", "Lời gọi đơn hoạt động như mutator bình thường.")]),
    "cppi-m2-composition-engine": vi_challenge("Composition: Car CÓ một Engine", "Cài `class Engine` với `void start()`, `bool running() const` (private `bool running_{false};`), và `class Car` sở hữu member `Engine engine_` cùng `std::string model_;`, với `void drive()` (khởi động máy) và `bool ready() const` (máy đang chạy).", [("delegation", "Car thể hiện hiệu ứng của Engine mà không lộ Engine ra ngoài."), ("fresh-car", "Xe mới thì máy chưa chạy."), ("model", "Car còn mang trạng thái riêng của nó.")]),
}

# full learner files for the ledger
R_COUNTER = "class BoundedCounter {\npublic:\n    explicit BoundedCounter(int max) : max_{max} {}\n    void increment() { if (value_ < max_) ++value_; }\n    int value() const { return value_; }\n    int max() const { return max_; }\nprivate:\n    int value_{0};\n    int max_;\n};\n"
W_COUNTER = "class BoundedCounter {\npublic:\n    explicit BoundedCounter(int max) : max_{max} {}\n    void increment() { ++value_; }  // ignores max — invariant broken\n    int value() const { return value_; }\n    int max() const { return max_; }\nprivate:\n    int value_{0};\n    int max_;\n};\n"
R_METERS = "class Meters {\npublic:\n    explicit Meters(double v) : v_{v} {}\n    double value() const { return v_; }\nprivate:\n    double v_;\n};\n"
W_METERS = "class Meters {\npublic:\n    explicit Meters(double v) : v_{v} {}\n    double value() const { return v_ * 2.0; }  // silently doubles\nprivate:\n    double v_;\n};\n"
R_EVENT = "class EventLog {\npublic:\n    EventLog(int id, std::string name) : name_{std::move(name)}, id_{id} {}\n    const std::string& name() const { return name_; }\n    int id() const { return id_; }\nprivate:\n    std::string name_;\n    int id_;\n};\n"
W_EVENT = "class EventLog {\npublic:\n    EventLog(int id, std::string name) : name_{std::move(name)}, id_{id} {}\n    const std::string& name() const { return std::to_string(id_); }  // wrong member\n    int id() const { return id_; }\nprivate:\n    std::string name_;\n    int id_;\n};\n"
R_TRACKED = "class Tracked {\npublic:\n    Tracked() { ++created(); ++live(); }\n    ~Tracked() { --live(); }\n    static int& live() { static int n{0}; return n; }\n    static int& created() { static int n{0}; return n; }\nprivate:\n};\n"
W_TRACKED = "class Tracked {\npublic:\n    Tracked() { ++created(); ++live(); }\n    ~Tracked() { ++live(); }  // destructor INCREMENTS live — backwards\n    static int& live() { static int n{0}; return n; }\n    static int& created() { static int n{0}; return n; }\nprivate:\n};\n"
R_LEDGER = "class Ledger {\npublic:\n    Ledger& add(long cents) { total_ += cents; return *this; }\n    Ledger& undo(long cents) { total_ -= cents; return *this; }\n    long total() const { return total_; }\nprivate:\n    long total_{0};\n};\n"
W_LEDGER = "class Ledger {\npublic:\n    Ledger& add(long cents) { total_ += cents; return *this; }\n    Ledger& undo(long cents) { total_ -= cents; }  // forgets return *this\n    long total() const { return total_; }\nprivate:\n    long total_{0};\n};\n"
R_CAR = "class Engine {\npublic:\n    void start() { running_ = true; }\n    bool running() const { return running_; }\nprivate:\n    bool running_{false};\n};\n\nclass Car {\npublic:\n    explicit Car(std::string model) : model_{std::move(model)} {}\n    void drive() { engine_.start(); }\n    bool ready() const { return engine_.running(); }\n    const std::string& model() const { return model_; }\nprivate:\n    Engine engine_;\n    std::string model_;\n};\n"
W_CAR = "class Engine {\npublic:\n    void start() { running_ = true; }\n    bool running() const { return running_; }\nprivate:\n    bool running_{false};\n};\n\nclass Car {\npublic:\n    explicit Car(std::string model) : model_{std::move(model)} {}\n    void drive() { Engine e; e.start(); }  // starts a LOCAL engine, not the member\n    bool ready() const { return engine_.running(); }\n    const std::string& model() const { return model_; }\nprivate:\n    Engine engine_;\n    std::string model_;\n};\n"

write_practice(
    MOD, "cppi-p2-classes",
    "Classes, constructors, invariants",
    "Design small types: an enforced counter, an explicit-only constructor, member ordering.",
    "Class, constructor, bất biến",
    "Thiết kế kiểu nhỏ: counter có ràng buộc, constructor chỉ-explicit, thứ tự member.",
    "classes-and-objects", 30, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m2-class-counter", R_COUNTER, W_COUNTER),
        ("cppi-m2-ctor-explicit", R_METERS, W_METERS),
        ("cppi-m2-class-initializer-order", R_EVENT, W_EVENT),
    ],
)

write_practice(
    MOD, "cppi-p2-static-this",
    "static members and this",
    "Shared class state done right, and chaining built on returning *this.",
    "static member và this",
    "Trạng thái class dùng chung đúng cách, và nối chuỗi nhờ trả về *this.",
    "static-members", 25, "intermediate", P2, VI_P2,
    solutions=[
        ("cppi-m2-static-counter", R_TRACKED, W_TRACKED),
        ("cppi-m2-this-chain", R_LEDGER, W_LEDGER),
        ("cppi-m2-composition-engine", R_CAR, W_CAR),
    ],
)

# ── checkpoint 2 ─────────────────────────────────────────────────────────────
CP_CH = challenge(
    "cppi-checkpoint-oop",
    "Checkpoint: Object-Oriented Design",
    "Implement `class Library` that owns a `std::vector<std::string> titles_;` plus an `inline static int copies_;` counting every title ever added across all instances. Provide: `void add(std::string title)` (push_back and bump the static counter), `std::size_t size() const`, `bool has(const std::string& title) const`, and `static int total_copies()`.",
    "#include <string>\n#include <vector>\n#include <iostream>\n\nclass Library {\n    // members, static counter, methods\n};\n",
    [
        ("add-and-size", 'Library lib;\nlib.add("zen");\nCHECK_EQ(lib.size(), 1);\nCHECK_EQ(lib.total_copies(), 1);', "Instance state and class state evolve together."),
        ("has", 'Library lib;\nlib.add("zen");\nCHECK(lib.has("zen"));\nCHECK(!lib.has("nope"));', "has() searches the owned vector."),
        ("shared-static", 'Library a;\nLibrary b;\na.add("x");\nb.add("y");\nCHECK_EQ(Library::total_copies(), 2);', "Two instances share one static counter."),
        ("const-correct", 'Library lib;\nlib.add("q");\nconst Library& view = lib;\nCHECK_EQ(view.size(), 1);\nCHECK(view.has("q"));', "Read-only calls must work through a const reference."),
    ],
    difficulty="intermediate",
)
VI_CP = vi_challenge(
    "Kiểm tra điểm: Thiết kế hướng đối tượng",
    "Cài `class Library` sở hữu `std::vector<std::string> titles_;` cùng `inline static int copies_;` đếm mọi đầu sách từng được thêm qua mọi instance. Cung cấp: `void add(std::string title)`, `std::size_t size() const`, `bool has(const std::string& title) const`, và `static int total_copies()`.",
    [
        ("add-and-size", "Trạng thái instance và trạng thái class tiến cùng nhau."),
        ("has", "has() tìm trong vector mà class sở hữu."),
        ("shared-static", "Hai instance dùng chung một bộ đếm static."),
        ("const-correct", "Lời gọi chỉ-đọc phải chạy được qua const reference."),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-oop",
    "Checkpoint: Object-Oriented Design",
    "One type combining encapsulated state, a shared static counter, and a const-correct read-only surface.",
    30,
    """
This checkpoint asks for one small type that gets four things right at once:

1. **Encapsulation** — the vector of titles is private; operations are the only door.
2. **Instance vs class state** — each `Library` has its own titles; `total_copies()` is shared.
3. **Const correctness** — `size()`/`has()` work through a `const Library&`.
4. **Pass-by-move** — `add(std::string title)` takes by value and moves in (one
   parameter serves both lvalues and rvalues).

Aim for the shortest implementation that satisfies all four tests.
""",
    "Kiểm tra điểm: Thiết kế hướng đối tượng",
    "Một kiểu kết hợp đúng bốn điều: trạng thái đóng gói, bộ đếm static dùng chung, bề mặt chỉ-read const-correct.",
    """
Kiểm tra điểm này đòi một kiểu nhỏ làm đúng bốn điều cùng lúc:

1. **Đóng gói** — vector sách là private; thao tác là cánh cửa duy nhất.
2. **Trạng thái instance vs class** — mỗi `Library` có sách riêng; `total_copies()` dùng chung.
3. **Const correctness** — `size()`/`has()` chạy được qua `const Library&`.
4. **Truyền bằng move** — `add(std::string title)` nhận bằng giá trị rồi move vào
   (một tham số phục vụ cả lvalue lẫn rvalue).

Hãy nhắm tới bản cài đặt ngắn nhất thỏa cả bốn test.
""",
    CP_CH, VI_CP,
    solution="#include <algorithm>\n\nclass Library {\npublic:\n    void add(std::string title) {\n        titles_.push_back(std::move(title));\n        ++copies_;\n    }\n    std::size_t size() const { return titles_.size(); }\n    bool has(const std::string& title) const {\n        return std::find(titles_.begin(), titles_.end(), title) != titles_.end();\n    }\n    static int total_copies() { return copies_; }\nprivate:\n    std::vector<std::string> titles_;\n    inline static int copies_{0};\n};\n",
    wrong="class Library {\npublic:\n    void add(std::string title) {\n        titles_.push_back(std::move(title));\n    }  // forgets the static counter\n    std::size_t size() const { return titles_.size(); }\n    bool has(const std::string& title) const {\n        return std::find(titles_.begin(), titles_.end(), title) != titles_.end();\n    }\n    static int total_copies() { return copies_; }\nprivate:\n    std::vector<std::string> titles_;\n    inline static int copies_{0};\n};\n",
)

# ── emit module ──────────────────────────────────────────────────────────────
write_lesson(MOD, "classes-and-objects", "Classes as Invariants", "Design order: invariant → members → operations; struct vs class without folklore.", 20, L_CLASSES_EN, "Class như bất biến", "Thứ tự thiết kế: bất biến → member → thao tác; struct với class không tô lâu.", L_CLASSES_VI)
write_lesson(MOD, "constructors", "Constructors and Member Initialization", "Default, explicit, multi-parameter; initializer lists and declaration-order initialization.", 25, L_CTOR_EN, "Constructor và khởi tạo member", "Default, explicit, nhiều tham số; initializer list và thứ tự khởi tạo theo khai báo.", L_CTOR_VI)
write_lesson(MOD, "destructors", "Destructors and Automatic Cleanup", "What belongs in ~T, what does not, destruction order, and the destructor's role in RAII.", 20, L_DTOR_EN, "Destructor và dọn dẹp tự động", "Điều gì thuộc về ~T, điều gì không, thứ tự hủy, và vai trò của destructor trong RAII.", L_DTOR_VI)
write_lesson(MOD, "static-members", "Static Members: Class-Level State", "Static data with inline initialization, static functions without this, and justified use cases.", 20, L_STATIC_EN, "Static member: trạng thái cấp class", "Static data với khởi tạo inline, hàm static không có this, và các trường hợp dùng chính đáng.", L_STATIC_VI)
write_lesson(MOD, "this-pointer", "The this Pointer", "Implicit in every call; deliberate when returning *this, comparing identity, or disambiguating.", 15, L_THIS_EN, "Con trỏ this", "Ngầm định trong mọi lời gọi; chủ đích khi trả *this, so sánh bản sắc, hay phân biệt tên.", L_THIS_VI)
write_lesson(MOD, "composition", "Composition Over Inheritance", "Building types from members: why has-a wins by default and the call-site test for real inheritance.", 20, L_COMP_EN, "Composition hơn kế thừa", "Xây kiểu từ member: vì sao has-a thắng mặc định, và bài test call-site cho kế thừa thật.", L_COMP_VI)

write_module(
    MOD,
    "Object-Oriented Design",
    "Classes as invariants: constructors, destructors, static members, this, and composition as the default structure.",
    "Thiết kế hướng đối tượng",
    "Class như bất biến: constructor, destructor, static member, this, và composition là cấu trúc mặc định.",
    ["classes-and-objects", "constructors", "destructors", "static-members", "this-pointer", "composition", "advanced-checkpoint-oop"],
    ["cppi-p2-classes", "cppi-p2-static-this"],
)
print("module 2 emitted")
