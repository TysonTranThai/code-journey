#!/usr/bin/env python3
"""C++ Intermediate — Module 3: inheritance, polymorphism, virtual destructors."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "inheritance-polymorphism"

L_INH_EN = """
**Inheritance** expresses "is-a": a derived class is a kind of its base, and
a derived object can be used where a base is expected. Begin with the shape:

```cpp
#include <string>

class Employee {
public:
    explicit Employee(std::string name) : name_{std::move(name)} {}
    const std::string& name() const { return name_; }

private:
    std::string name_;
};

class Engineer : public Employee {     // Engineer IS-A Employee
public:
    Engineer(std::string name, std::string specialty)
        : Employee{std::move(name)}, specialty_{std::move(specialty)} {}
    const std::string& specialty() const { return specialty_; }

private:
    std::string specialty_;
};
```

## What public inheritance means

- The derived object **contains** a full base subobject.
- Base `private` members exist in the derived object but are **not accessible**
  to the derived class — they belong to the base's implementation.
- Construction runs **base first**, then derived; destruction runs derived
  first, then base.

## The default is `private` inheritance — use `public` explicitly

`class D : B` inherits privately (implementation detail, almost never what
you want). Always write `: public B` for the substitutability relationship,
and if you find yourself reaching for private/protected inheritance, ask
whether composition says it better.

## What inheritance is NOT for

Reusing a helper. That is composition or a free function. Reach for
inheritance only when you need **substitutability** — different objects used
through one base interface (next lessons).
"""

L_INH_VI = """
**Kế thừa** diễn đạt "is-a": lớp dẫn xuất là một loại của base, và đối tượng
dẫn xuất có thể được dùng ở nơi cần base. Bắt đầu bằng hình dạng:

```cpp
#include <string>

class Employee {
public:
    explicit Employee(std::string name) : name_{std::move(name)} {}
    const std::string& name() const { return name_; }

private:
    std::string name_;
};

class Engineer : public Employee {     // Engineer IS-A Employee
public:
    Engineer(std::string name, std::string specialty)
        : Employee{std::move(name)}, specialty_{std::move(specialty)} {}
    const std::string& specialty() const { return specialty_; }

private:
    std::string specialty_;
};
```

## Public inheritance nghĩa là gì

- Đối tượng derived **chứa trọn** một base subobject.
- Member `private` của base tồn tại trong đối tượng derived nhưng lớp derived
  **không truy cập được** — chúng thuộc về phần cài đặt của base.
- Khởi tạo chạy **base trước**, rồi derived; hủy chạy derived trước, rồi base.

## Mặc định là kế thừa private — hãy viết `public` tường minh

`class D : B` kế thừa private (chi tiết cài đặt, gần như không bao giờ là điều
bạn muốn). Luôn viết `: public B` cho quan hệ thay thế được; còn nếu bạn định
dùng private/protected inheritance, hãy hỏi composition có nói tốt hơn không.

## Kế thừa KHÔNG phải để

Tái sử dụng một hàm phụ. Đó là composition hoặc hàm tự do. Chỉ dùng kế thừa
khi bạn cần **khả năng thay thế** — nhiều đối tượng khác nhau dùng qua một
interface base (các bài sau).
"""

L_PROT_EN = """
`protected` is the middle door: members the derived class may use, but the
outside world may not.

```cpp
#include <string>

class Account {
public:
    explicit Account(long cents) : balance_{cents} {}

private:
    long balance_;                     // invisible even to derived
};

class SavingsAccount : public Account {
public:
    SavingsAccount(long cents, double rate) : Account{cents}, rate_{rate} {}

    long balance() const {
        // return balance_;            // ERROR: base made it private
        return view_balance();          // via the protected accessor instead
    }
protected:
    long view_balance() const { return protected_balance(); }
private:
    // demo plumbing for this lesson's runnable shape
    static long protected_balance() { return 12345; }
    double rate_;
};
```

## Use protected sparingly — and never for data

`protected` member **functions** are a controlled extension point: the base
offers a hook the derived may call or override. `protected` member **data**
couples every future derived class to your storage decisions — a renaming in
the base now breaks all of them. Keep data `private` even from children, and
expose protected *operations* if derived classes genuinely need them.

## Constructor chaining

The derived constructor must initialize the base explicitly when the base has
no default constructor: `SavingsAccount(...) : Account{cents}, rate_{rate}`.
The base part is built first — you cannot touch `this` before it exists.
"""

L_PROT_VI = """
`protected` là cánh cửa giữa: member mà lớp dẫn xuất được dùng, nhưng thế
giới bên ngoài không được.

```cpp
#include <string>

class Account {
public:
    explicit Account(long cents) : balance_{cents} {}

private:
    long balance_;                     // cả derived cũng không thấy
};

class SavingsAccount : public Account {
public:
    SavingsAccount(long cents, double rate) : Account{cents}, rate_{rate} {}

    long balance() const {
        // return balance_;            // LỖI: base đã đặt private
        return view_balance();          // đi qua accessor protected
    }
protected:
    long view_balance() const { return protected_balance(); }
private:
    // phần cài minh họa cho bài chạy được của bài học
    static long protected_balance() { return 12345; }
    double rate_;
};
```

## Dùng protected tiết kiệm — và không bao giờ cho dữ liệu

Hàm thành viên `protected` là điểm mở rộng được kiểm soát: base cung cấp hook
mà derived có thể gọi hoặc override. Dữ liệu `protected` trói buộc mọi lớp
dẫn xuất sau này vào quyết định lưu trữ của bạn — đổi tên trong base giờ đây
làm gãy tất cả chúng. Hãy giữ dữ liệu `private` kể cả với con, và chỉ mở
*thao tác* protected nếu lớp dẫn xuất thật sự cần.

## Chuỗi constructor

Constructor của derived phải khởi tạo base tường minh khi base không có
constructor mặc định: `SavingsAccount(...) : Account{cents}, rate_{rate}`.
Phần base được dựng trước — bạn không thể đụng `this` trước khi nó tồn tại.
"""

L_ORDER_EN = """
Construction and destruction have a fixed order. Predict it and you can
reason about every resource a class hierarchy touches.

```cpp
#include <iostream>

class Base {
public:
    Base() { std::cout << "Base ctor\n"; }
    ~Base() { std::cout << "Base dtor\n"; }
};

class Derived : public Base {
public:
    Derived() { std::cout << "Derived ctor\n"; }
    ~Derived() { std::cout << "Derived dtor\n"; }
};

int main_cj_order() {
    { Derived d; }
    // prints: Base ctor, Derived ctor, Derived dtor, Base dtor
    return 0;
}
```

## The rules

1. **Bases construct first** (left to right in the base list).
2. **Members construct** in declaration order, after all bases.
3. The derived constructor **body** runs last.
4. Destruction is the exact **reverse**: body → members → bases.

## Why it must be so

A derived constructor may call base functions in its body — so the base must
already exist. The destructor runs when the derived part is about to vanish,
so it must run *before* the base part it may still use disappears. Memory
bugs and "virtual call in constructor" surprises (later lessons) both come
from forgetting this order.
"""

L_ORDER_VI = """
Khởi tạo và hủy có thứ tự cố định. Dự đoán đúng thứ tự, bạn sẽ suy luận được
mọi tài nguyên mà một hệ thống class chạm tới.

```cpp
#include <iostream>

class Base {
public:
    Base() { std::cout << "Base ctor\n"; }
    ~Base() { std::cout << "Base dtor\n"; }
};

class Derived : public Base {
public:
    Derived() { std::cout << "Derived ctor\n"; }
    ~Derived() { std::cout << "Derived dtor\n"; }
};

int main_cj_order() {
    { Derived d; }
    // in ra: Base ctor, Derived ctor, Derived dtor, Base dtor
    return 0;
}
```

## Các quy tắc

1. **Base được dựng trước** (trái sang phải theo danh sách base).
2. **Member được dựng** theo thứ tự khai báo, sau mọi base.
3. Thân constructor của derived chạy **cuối cùng**.
4. Hủy là chiều **ngược lại hoàn toàn**: thân → member → base.

## Vì sao buộc phải vậy

Constructor của derived có thể gọi hàm của base trong thân — vậy base phải đã
tồn tại. Destructor chạy khi phần derived sắp biến mất, nên nó phải chạy
*trước* phần base mà nó còn có thể dùng. Mọi lỗi bộ nhớ và bất ngờ "gọi hàm
ảo trong constructor" (bài sau) đều đến từ việc quên thứ tự này.
"""

L_OVERRIDE_EN = """
A derived class may **override** a base member function — but only if the
signatures match exactly, and the base must say the function *may* be
overridden (`virtual`, next lesson). Overriding is not overloading.

```cpp
#include <iostream>
#include <string>

class Animal {
public:
    virtual ~Animal() = default;
    virtual void speak() const { std::cout << "...\n"; }
};

class Dog : public Animal {
public:
    void speak() const override { std::cout << "Woof\n"; }  // overrides
    void speak(int times) const;                             // would OVERLOAD, not override
};

class Cat : public Animal {
public:
    void speak() const override { std::cout << "Meow\n"; }
};
```

## override: write it, always

`override` asks the compiler to verify a function really overrides something.
Without it, a typo or a `const` mismatch silently creates a *new* function:

```cpp
class Bird : public Animal {
public:
    void Speak() const override;   // compile error: no such base function (typo caught!)
    void speak() /* missing override + missing const */;   // new function, silent bug
};
```

## The matching checklist

Same name, same parameter types, same const-qualification, compatible
return type. `override` checks all of it for you at compile time — the
keyword costs nothing and removes an entire class of quiet bugs.
"""

L_OVERRIDE_VI = """
Lớp dẫn xuất có thể **override** hàm thành viên của base — nhưng chỉ khi chữ
ký khớp tuyệt đối, và base phải tuyên bố hàm đó *cho phép* bị override
(`virtual`, bài sau). Override không phải overload.

```cpp
#include <iostream>
#include <string>

class Animal {
public:
    virtual ~Animal() = default;
    virtual void speak() const { std::cout << "...\n"; }
};

class Dog : public Animal {
public:
    void speak() const override { std::cout << "Woof\n"; }  // override
    void speak(int times) const;                             // sẽ là OVERLOAD, không phải override
};

class Cat : public Animal {
public:
    void speak() const override { std::cout << "Meow\n"; }
};
```

## override: luôn viết nó

`override` yêu cầu compiler xác minh hàm này thật sự override điều gì. Không
có nó, một lỗi gõ phím hoặc lệch `const` lặng lẽ tạo ra một hàm *mới*:

```cpp
class Bird : public Animal {
public:
    void Speak() const override;   // lỗi biên dịch: base không có hàm này (bắt được lỗi gõ!)
    void speak() /* thiếu override + thiếu const */;   // hàm mới, bug câm lặng
};
```

## Danh sách khớp

Cùng tên, cùng kiểu tham số, cùng const-qualification, kiểu trả về tương
thích. `override` kiểm tra tất cả lúc biên dịch — từ khóa này không tốn gì
mà xóa sổ cả một lớp bug câm lặng.
"""

L_POLY_EN = """
**Polymorphism**: through a base-class reference or pointer, the *right*
override for the actual object runs — chosen at run time via the virtual
table.

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;              // pure virtual
    virtual const char* name() const = 0;
};

class Square : public Shape {
public:
    explicit Square(double s) : side_{s} {}
    double area() const override { return side_ * side_; }
    const char* name() const override { return "square"; }
private:
    double side_;
};

class Circle : public Shape {
public:
    explicit Circle(double r) : radius_{r} {}
    double area() const override { return 3.14159265358979 * radius_ * radius_; }
    const char* name() const override { return "circle"; }
private:
    double radius_;
};

double total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {
    double sum = 0;
    for (const auto& s : shapes) sum += s->area();   // dynamic dispatch per element
    return sum;
}
```

## The two conditions for dynamic dispatch

1. The call goes through a **reference or pointer** to the base.
2. The function is **virtual** in the base.

Call by value slices the object (a `Shape` copy of a `Square` loses the
derived parts) and dispatch never happens. Store shapes by pointer (a smart
pointer, Module 8) or reference, never by value, in polymorphic containers.

## Pure virtual and abstract types

`area() const = 0` makes `Shape` **abstract**: it cannot be instantiated, only
derived from. Derived classes must override every pure virtual or stay
abstract. This is how C++ expresses "interface".
"""

L_POLY_VI = """
**Đa hình**: qua reference hoặc pointer của base, phần override *đúng* cho
đối tượng thực tế sẽ chạy — được chọn lúc chạy qua bảng hàm ảo.

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;              // pure virtual
    virtual const char* name() const = 0;
};

class Square : public Shape {
public:
    explicit Square(double s) : side_{s} {}
    double area() const override { return side_ * side_; }
    const char* name() const override { return "square"; }
private:
    double side_;
};

class Circle : public Shape {
public:
    explicit Circle(double r) : radius_{r} {}
    double area() const override { return 3.14159265358979 * radius_ * radius_; }
    const char* name() const override { return "circle"; }
private:
    double radius_;
};

double total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {
    double sum = 0;
    for (const auto& s : shapes) sum += s->area();   // dispatch động từng phần tử
    return sum;
}
```

## Hai điều kiện để dispatch động

1. Lời gọi đi qua **reference hoặc pointer** tới base.
2. Hàm là **virtual** trong base.

Gọi bằng giá trị sẽ cắt xén đối tượng (một bản copy `Shape` của `Square` mất
phần derived) và dispatch không bao giờ xảy ra. Lưu các shape bằng pointer
(smart pointer, Module 8) hoặc reference, không bao giờ bằng giá trị, trong
container đa hình.

## Pure virtual và kiểu trừu tượng

`area() const = 0` biến `Shape` thành **trừu tượng**: không thể tạo instance,
chỉ có thể kế thừa. Lớp dẫn xuất phải override mọi pure virtual hoặc vẫn
trừu tượng. Đây là cách C++ diễn đạt "interface".
"""

L_VDTOR_EN = """
Deleting a derived object through a base pointer without a **virtual
destructor** is undefined behavior — typically the derived destructor never
runs and resources leak.

```cpp
#include <iostream>

class BaseBad {
public:
    ~BaseBad() { std::cout << "BaseBad dtor\n"; }       // NOT virtual
};

class DerivedBad : public BaseBad {
public:
    ~DerivedBad() { std::cout << "DerivedBad dtor\n"; } // never runs via Base*
};

class BaseGood {
public:
    virtual ~BaseGood() = default;                       // virtual: correct chain
};

class DerivedGood : public BaseGood {
public:
    ~DerivedGood() { std::cout << "DerivedGood dtor\n"; }
};
```

## The rule, stated once

**Any class intended for polymorphic deletion must have a public virtual
destructor.** If a type is not meant to be a base, keep its destructor
non-virtual (and preferably make the class `final`). The cost of `virtual
~T() = default` is one vtable pointer; the cost of forgetting it is leaks and
undefined behavior.

## When you will not be deleted via base*

If ownership never travels through a base pointer — pure value semantics, or
`std::unique_ptr<Derived>` with the deleter typed — a virtual destructor is
not required. But interfaces leak less when you simply follow the rule:
design a base → `virtual ~Base() = default;`, no exceptions.
"""

L_VDTOR_VI = """
Xóa một đối tượng derived qua pointer của base mà không có **virtual
destructor** là hành vi không xác định — thường thì destructor của derived
không bao giờ chạy và tài nguyên bị rò rỉ.

```cpp
#include <iostream>

class BaseBad {
public:
    ~BaseBad() { std::cout << "BaseBad dtor\n"; }       // KHÔNG virtual
};

class DerivedBad : public BaseBad {
public:
    ~DerivedBad() { std::cout << "DerivedBad dtor\n"; } // không bao giờ chạy qua Base*
};

class BaseGood {
public:
    virtual ~BaseGood() = default;                       // virtual: chuỗi đúng
};

class DerivedGood : public BaseGood {
public:
    ~DerivedGood() { std::cout << "DerivedGood dtor\n"; }
};
```

## Quy tắc, nói một lần

**Bất kỳ class nào định bị xóa đa hình phải có destructor ảo public.** Nếu
một kiểu không nhằm làm base, hãy giữ destructor non-virtual (và tốt nhất là
thêm `final` cho class). Chi phí của `virtual ~T() = default` là một con trỏ
vtable; chi phí của việc quên nó là rò rỉ và hành vi không xác định.

## Khi không bị xóa qua base*

Nếu ownership không bao giờ đi qua pointer của base — thuần value semantics,
hoặc `std::unique_ptr<Derived>` với deleter có kiểu — thì không bắt buộc
virtual destructor. Nhưng interface sẽ ít rò rỉ hơn nếu bạn đơn giản làm theo
quy tắc: thiết kế một base → `virtual ~Base() = default;`, không ngoại lệ.
"""

# ── practice sets ────────────────────────────────────────────────────────────
P1 = [
    challenge(
        "cppi-m3-inherit-chain",
        "Base and derived chain",
        "Implement `class Vehicle` with a constructor `Vehicle(int wheels)` and `int wheels() const` (private `int wheels_;`), and `class Bicycle : public Vehicle` with a constructor `Bicycle()` that passes 2 to the base and adds nothing else.",
        "#include <iostream>\n\nclass Vehicle {\n    // ctor + getter\n};\n\nclass Bicycle : public Vehicle {\n    // ctor chaining to base\n};\n",
        [
            ("chain", "Bicycle b;\nCHECK_EQ(b.wheels(), 2);", "Bicycle's ctor must forward 2 to Vehicle's ctor."),
            ("direct", "Vehicle v{4};\nCHECK_EQ(v.wheels(), 4);", "The base stands alone too."),
        ],
        level="guided",
    ),
    challenge(
        "cppi-m3-order-echo",
        "Predict construction order",
        "Implement `class Parent` with a constructor printing `parent` and a destructor printing `~parent`, and `class Child : public Parent` whose constructor prints `child` and destructor prints `~child`. Use std::cout exactly (no extra text). The test captures construction/destruction inside a scope.",
        "#include <iostream>\n\nclass Parent { /* print in ctor and dtor */ };\n\nclass Child : public Parent { /* same */ };\n",
        [
            ("order", "capture([]() { Child c; })", "Built base-first, destroyed in reverse."),
            ("reverse", "capture([]() { { Child c; } })", "Destructor order is the mirror of construction."),
        ],
        level="independent",
    ),
    challenge(
        "cppi-m3-protected-hook",
        "A protected extension point",
        "Implement `class Greeter` with `std::string greet() const` returning `\"Hello, \" + salutation()` where `salutation()` is a protected member function returning `\"world\"`. Implement `class FormalGreeter : public Greeter` overriding nothing but the base stays intact — the test calls both through their own types.",
        "#include <string>\n#include <iostream>\n\nclass Greeter {\n    // greet() + protected salutation()\n};\n",
        [
            ("base", "Greeter g;\nCHECK_EQ(g.greet(), std::string(\"Hello, world\"));", "The base composes greet from a protected hook."),
            ("derived-uses", "FormalGreeter f;\nCHECK_EQ(f.greet(), std::string(\"Hello, world\"));", "The derived inherits the whole shape."),
        ],
        level="combination",
    ),
]

P2 = [
    challenge(
        "cppi-m3-shapes",
        "Abstract shapes with dispatch",
        "Implement `class Shape` with a pure virtual `double area() const`, a pure virtual `const char* name() const`, and a public virtual destructor (`virtual ~Shape() = default;`). Implement `Square(double side)` and `Circle(double radius)` overriding both. The test stores them in a `std::vector<std::unique_ptr<Shape>>` and checks dispatch + the vtable-aware destructor path.",
        "#include <vector>\n#include <memory>\n#include <iostream>\n\nclass Shape {\n    // pure virtuals + virtual dtor\n};\n",
        [
            ("dispatch", "std::vector<std::unique_ptr<Shape>> v;\nv.push_back(std::make_unique<Square>(2.0));\nv.push_back(std::make_unique<Circle>(1.0));\nCHECK_NEAR(v[0]->area(), 4.0, 1e-9);\nCHECK_NEAR(v[1]->area(), 3.14159265358979, 1e-4);", "area() dispatches per element."),
            ("names", "std::vector<std::unique_ptr<Shape>> v;\nv.push_back(std::make_unique<Square>(1.0));\nCHECK_EQ(std::string(v[0]->name()), std::string(\"square\"));", "name() is also virtual."),
            ("abstract", "static_assert(std::is_abstract<Shape>::value, \"Shape must be abstract\");", "= 0 makes the class abstract."),
        ],
        level="combination",
    ),
    challenge(
        "cppi-m3-virtual-dtor",
        "Prove the virtual destructor",
        "Implement `class Resource` whose destructor increments an `inline static` counter `destroyed_`, and `class HeavyResource : public Resource` whose destructor also increments it. The base destructor must be virtual so deleting through `Resource*` destroys the HeavyResource part too.",
        "#include <iostream>\n\nclass Resource {\n    // virtual dtor + static counter\n};\n\nclass HeavyResource : public Resource {\n    // dtor bumps the counter\n};\n",
        [
            ("through-base", "Resource* r = new HeavyResource();\nint before = Resource::destroyed();\ndelete r;\nCHECK_EQ(Resource::destroyed(), before + 1);", "Deleting via Resource* must run the chain once (virtual dtor)."),
            ("still-abstract-free", "HeavyResource h;\nint before = Resource::destroyed();\n{ HeavyResource h2; }\nCHECK_EQ(Resource::destroyed(), before + 1);", "Scoped destruction works normally."),
        ],
        level="debugging",
    ),
    challenge(
        "cppi-m3-override-strict",
        "override catches the bug",
        "Implement `class Sensor` with `virtual std::string reading() const` returning `\"base\"`, and `class TempSensor : public Sensor` overriding it to return `\"22C\"`. The signature must match exactly (const included) and the override must use the `override` keyword.",
        "#include <string>\n#include <iostream>\n\nclass Sensor {\n    // virtual reading() + virtual dtor\n};\n\nclass TempSensor : public Sensor {\n    // override\n};\n",
        [
            ("dispatch", "Sensor* s = new TempSensor();\nstd::string r = s->reading();\ndelete s;\nCHECK_EQ(r, std::string(\"22C\"));", "Dispatch through base pointer returns the override."),
            ("base-fallback", "TempSensor t;\nSensor& ref = t;\nCHECK_EQ(ref.reading(), std::string(\"22C\"));", "Reference dispatch matches pointer dispatch."),
            ("virtual-dtor", "static_assert(std::has_virtual_destructor<Sensor>::value, \"Sensor needs a virtual destructor\");", "Any polymorphic base owns this obligation."),
        ],
        level="independent",
    ),
]

VI_P1 = {
    "cppi-m3-inherit-chain": vi_challenge("Chuỗi base và derived", "Cài `class Vehicle` với constructor `Vehicle(int wheels)` và `int wheels() const` (private `int wheels_;`), và `class Bicycle : public Vehicle` với constructor `Bicycle()` truyền 2 cho base và không thêm gì khác.", [("chain", "Constructor của Bicycle phải chuyển 2 cho constructor của Vehicle."), ("direct", "Base đứng độc lập được.")]),
    "cppi-m3-order-echo": vi_challenge("Dự đoán thứ tự khởi tạo", "Cài `class Parent` với constructor in `parent` và destructor in `~parent`, và `class Child : public Parent` constructor in `child`, destructor in `~child`. Dùng std::cout đúng chính xác (không chữ thừa). Test bắt việc dựng/hủy trong một phạm vi.", [("order", "Dựng base trước, hủy ngược lại."), ("reverse", "Thứ tự hủy là hình chiếu ngược của khởi tạo.")]),
    "cppi-m3-protected-hook": vi_challenge("Điểm mở rộng protected", "Cài `class Greeter` với `std::string greet() const` trả `\"Hello, \" + salutation()` trong đó `salutation()` là hàm thành viên protected trả `\"world\"`. Cài `class FormalGreeter : public Greeter` không override gì — test gọi cả hai qua kiểu của riêng chúng.", [("base", "Base ghép greet từ một hook protected."), ("derived-uses", "Derived kế thừa trọn vẹn hình dạng đó.")]),
}

VI_P2 = {
    "cppi-m3-shapes": vi_challenge("Shape trừu tượng với dispatch", "Cài `class Shape` với pure virtual `double area() const`, pure virtual `const char* name() const`, và virtual destructor public (`virtual ~Shape() = default;`). Cài `Square(double side)` và `Circle(double radius)` override cả hai. Test lưu chúng trong `std::vector<std::unique_ptr<Shape>>` và kiểm tra dispatch lẫn đường hủy có vtable.", [("dispatch", "area() dispatch theo từng phần tử."), ("names", "name() cũng là virtual."), ("abstract", "= 0 biến class thành trừu tượng.")]),
    "cppi-m3-virtual-dtor": vi_challenge("Chứng minh virtual destructor", "Cài `class Resource` có destructor tăng bộ đếm `inline static` tên `destroyed_`, và `class HeavyResource : public Resource` destructor cũng tăng nó. Destructor của base phải là virtual để xóa qua `Resource*` cũng hủy phần HeavyResource.", [("through-base", "Xóa qua Resource* phải chạy chuỗi đúng một lần (virtual dtor)."), ("still-abstract-free", "Hủy theo phạm vi vẫn hoạt động bình thường.")]),
    "cppi-m3-override-strict": vi_challenge("override bắt lỗi", "Cài `class Sensor` với `virtual std::string reading() const` trả `\"base\"`, và `class TempSensor : public Sensor` override trả `\"22C\"`. Chữ ký phải khớp tuyệt đối (kể cả const) và override phải dùng từ khóa `override`.", [("dispatch", "Dispatch qua pointer base trả về phần override."), ("base-fallback", "Dispatch qua reference khớp với pointer."), ("virtual-dtor", "Mọi base đa hình đều mang nghĩa vụ này.")]),
}

# ledger sources (full learner files)
R_VEHICLE = "class Vehicle {\npublic:\n    explicit Vehicle(int wheels) : wheels_{wheels} {}\n    int wheels() const { return wheels_; }\nprivate:\n    int wheels_;\n};\n\nclass Bicycle : public Vehicle {\npublic:\n    Bicycle() : Vehicle{2} {}\n};\n"
W_VEHICLE = "class Vehicle {\npublic:\n    explicit Vehicle(int wheels) : wheels_{wheels} {}\n    int wheels() const { return wheels_; }\nprivate:\n    int wheels_;\n};\n\nclass Bicycle : public Vehicle {\npublic:\n    Bicycle() {}  // relies on a default ctor Vehicle does not have -> compile error\n};\n"
R_ORDER = "class Parent {\npublic:\n    Parent() { std::cout << \\\"parent\\n\\\"; }\n    ~Parent() { std::cout << \\\"~parent\\n\\\"; }\n};\n\nclass Child : public Parent {\npublic:\n    Child() { std::cout << \\\"child\\n\\\"; }\n    ~Child() { std::cout << \\\"~child\\n\\\"; }\n};\n"
W_ORDER = "class Parent {\npublic:\n    Parent() { std::cout << \\\"parent\\n\\\"; }\n    ~Parent() { std::cout << \\\"~parent\\n\\\"; }\n};\n\nclass Child : public Parent {\npublic:\n    Child() { std::cout << \\\"child\\n\\\"; }\n    ~Child() { std::cout << \\\"parent\\n\\\"; }  // copy-paste bug\n};\n"
R_GREETER = "class Greeter {\npublic:\n    std::string greet() const { return std::string(\\\"Hello, \\\") + salutation(); }\nprotected:\n    virtual std::string salutation() const { return \\\"world\\\"; }\n};\n\nclass FormalGreeter : public Greeter {};\n"
W_GREETER = "class Greeter {\npublic:\n    std::string greet() const { return std::string(\\\"Hello\\\") + salutation(); }  // missing comma\nprotected:\n    virtual std::string salutation() const { return \\\"world\\\"; }\n};\n\nclass FormalGreeter : public Greeter {};\n"
R_SHAPES = "class Shape {\npublic:\n    virtual ~Shape() = default;\n    virtual double area() const = 0;\n    virtual const char* name() const = 0;\n};\n\nclass Square : public Shape {\npublic:\n    explicit Square(double s) : side_{s} {}\n    double area() const override { return side_ * side_; }\n    const char* name() const override { return \\\"square\\\"; }\nprivate:\n    double side_;\n};\n\nclass Circle : public Shape {\npublic:\n    explicit Circle(double r) : radius_{r} {}\n    double area() const override { return 3.14159265358979 * radius_ * radius_; }\n    const char* name() const override { return \\\"circle\\\"; }\nprivate:\n    double radius_;\n};\n"
W_SHAPES = "class Shape {\npublic:\n    virtual ~Shape() = default;\n    virtual double area() const = 0;\n    virtual const char* name() const = 0;\n};\n\nclass Square : public Shape {\npublic:\n    explicit Square(double s) : side_{s} {}\n    double area() const override { return side_ + side_; }  // wrong formula\n    const char* name() const override { return \\\"square\\\"; }\nprivate:\n    double side_;\n};\n\nclass Circle : public Shape {\npublic:\n    explicit Circle(double r) : radius_{r} {}\n    double area() const override { return 3.14159265358979 * radius_ * radius_; }\n    const char* name() const override { return \\\"circle\\\"; }\nprivate:\n    double radius_;\n};\n"
R_VDTOR = "class Resource {\npublic:\n    virtual ~Resource() { ++destroyed(); }\n    static int& destroyed() { static int n{0}; return n; }\n};\n\nclass HeavyResource : public Resource {\npublic:\n    ~HeavyResource() { ++Resource::destroyed(); }\n};\n"
W_VDTOR = "class Resource {\npublic:\n    ~Resource() { ++destroyed(); }  // not virtual\n    static int& destroyed() { static int n{0}; return n; }\n};\n\nclass HeavyResource : public Resource {\npublic:\n    ~HeavyResource() { ++Resource::destroyed(); }\n};\n"
R_SENSOR = "class Sensor {\npublic:\n    virtual ~Sensor() = default;\n    virtual std::string reading() const { return \\\"base\\\"; }\n};\n\nclass TempSensor : public Sensor {\npublic:\n    std::string reading() const override { return \\\"22C\\\"; }\n};\n"
W_SENSOR = "class Sensor {\npublic:\n    virtual ~Sensor() = default;\n    virtual std::string reading() const { return \\\"base\\\"; }\n};\n\nclass TempSensor : public Sensor {\npublic:\n    std::string reading() override { return \\\"22C\\\"; }  // missing const: overload, not override (and override keyword catches it)\n};\n"

write_practice(
    MOD, "cppi-p3-inheritance",
    "Inheritance mechanics",
    "Chain constructors, predict construction order, and use a protected hook.",
    "Cơ chế kế thừa",
    "Nối constructor, dự đoán thứ tự khởi tạo, và dùng một hook protected.",
    "inheritance", 30, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m3-inherit-chain", R_VEHICLE, W_VEHICLE),
        ("cppi-m3-order-echo", R_ORDER, W_ORDER),
        ("cppi-m3-protected-hook", R_GREETER, W_GREETER),
    ],
)

write_practice(
    MOD, "cppi-p3-polymorphism",
    "Polymorphism and the virtual destructor rule",
    "Abstract shapes with real dispatch, and a challenge that fails without a virtual destructor.",
    "Đa hình và quy tắc virtual destructor",
    "Shape trừu tượng với dispatch thật, và bài test gãy ngay khi thiếu virtual destructor.",
    "polymorphism", 35, "intermediate", P2, VI_P2,
    solutions=[
        ("cppi-m3-shapes", R_SHAPES, W_SHAPES),
        ("cppi-m3-virtual-dtor", R_VDTOR, W_VDTOR),
        ("cppi-m3-override-strict", R_SENSOR, W_SENSOR),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_CH = challenge(
    "cppi-checkpoint-polymorphism",
    "Checkpoint: Polymorphism",
    "Build a tiny notification system: `class Notifier` with a pure virtual `void send(const std::string& message) const`, a public virtual destructor, and a pure virtual `const char* channel() const`. Implement `EmailNotifier` (channel \"email\", send captures its message) and `SmsNotifier` (channel \"sms\"). The test dispatches through `std::vector<std::unique_ptr<Notifier>>`.",
    "#include <vector>\n#include <memory>\n#include <string>\n#include <iostream>\n\nclass Notifier {\n    // pure virtuals + virtual dtor\n};\n",
    [
        ("channels", "std::vector<std::unique_ptr<Notifier>> v;\nv.push_back(std::make_unique<EmailNotifier>());\nv.push_back(std::make_unique<SmsNotifier>());\nCHECK_EQ(std::string(v[0]->channel()), std::string(\"email\"));\nCHECK_EQ(std::string(v[1]->channel()), std::string(\"sms\"));", "channel() dispatches per element."),
        ("send-dispatch", "capture([]() {\n    std::vector<std::unique_ptr<Notifier>> v;\n    v.push_back(std::make_unique<EmailNotifier>());\n    v[0]->send(\"hi\");\n})", "send() runs through the base interface."),
        ("virtual-dtor", "static_assert(std::has_virtual_destructor<Notifier>::value, \"Notifier needs a virtual destructor\");", "Polymorphic deletion requires the virtual dtor."),
    ],
    difficulty="intermediate",
)
VI_CP = vi_challenge(
    "Kiểm tra điểm: Đa hình",
    "Xây hệ thống thông báo nhỏ: `class Notifier` với pure virtual `void send(const std::string& message) const`, virtual destructor public, và pure virtual `const char* channel() const`. Cài `EmailNotifier` (channel \"email\") và `SmsNotifier` (channel \"sms\"). Test dispatch qua `std::vector<std::unique_ptr<Notifier>>`.",
    [
        ("channels", "channel() dispatch theo từng phần tử."),
        ("send-dispatch", "send() chạy qua interface base."),
        ("virtual-dtor", "Xóa đa hình đòi hỏi virtual dtor."),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-polymorphism",
    "Checkpoint: Polymorphism",
    "An interface, two implementations, dispatch through a container of base pointers — the OOP module's core in one design.",
    35,
    """
Design and implement a small polymorphic system end to end:

- the **interface** (`Notifier`) owns no state — only the contract
- each implementation carries its own identity (`channel()`) and behavior (`send()`)
- the caller never mentions a concrete type after construction
- the base enforces the virtual-destructor rule so container cleanup is safe

If your solution needs a `dynamic_cast` or an `if` on type, re-read the
lesson on dispatch — polymorphism means the object itself answers.
""",
    "Kiểm tra điểm: Đa hình",
    "Một interface, hai cài đặt, dispatch qua container các base pointer — lõi của module OOP trong một thiết kế.",
    """
Thiết kế và cài một hệ thống đa hình nhỏ trọn vẹn:

- **interface** (`Notifier`) không giữ trạng thái — chỉ hợp đồng
- mỗi cài đặt mang nhận diện riêng (`channel()`) và hành vi riêng (`send()`)
- bên gọi không bao giờ nhắc kiểu cụ thể sau khi khởi tạo
- base áp đặt quy tắc virtual destructor để dọn container an toàn

Nếu lời giải của bạn cần `dynamic_cast` hay một `if` kiểm tra kiểu, hãy đọc
lại bài dispatch — đa hình nghĩa là đối tượng tự trả lời.
""",
    CP_CH, VI_CP,
    solution='class Notifier {\npublic:\n    virtual ~Notifier() = default;\n    virtual void send(const std::string& message) const = 0;\n    virtual const char* channel() const = 0;\n};\n\nclass EmailNotifier : public Notifier {\npublic:\n    void send(const std::string& message) const override { sent_email_ = message; }\n    const char* channel() const override { return "email"; }\n    static std::string sent_email_;\n};\nstd::string EmailNotifier::sent_email_;\n\nclass SmsNotifier : public Notifier {\npublic:\n    void send(const std::string& message) const override { sent_sms_ = message; }\n    const char* channel() const override { return "sms"; }\n    static std::string sent_sms_;\n};\nstd::string SmsNotifier::sent_sms_;\n',
    wrong='class Notifier {\npublic:\n    virtual ~Notifier() = default;\n    virtual void send(const std::string& message) const = 0;\n    virtual const char* channel() const = 0;\n};\n\nclass EmailNotifier : public Notifier {\npublic:\n    void send(const std::string& message) const override { sent_email_ = message; }\n    const char* channel() const override { return "EMAIL"; }  // wrong casing\n    static std::string sent_email_;\n};\nstd::string EmailNotifier::sent_email_;\n\nclass SmsNotifier : public Notifier {\npublic:\n    void send(const std::string& message) const override { sent_sms_ = message; }\n    const char* channel() const override { return "sms"; }\n    static std::string sent_sms_;\n};\nstd::string SmsNotifier::sent_sms_;\n',
)

# ── lessons + module ─────────────────────────────────────────────────────────
write_lesson(MOD, "inheritance", "Inheritance: Modeling IS-A", "Public inheritance as substitutability; base/derived construction; what inheritance is not for.", 25, L_INH_EN, "Kế thừa: mô hình hóa IS-A", "Public inheritance như khả năng thay thế; dựng base/derived; kế thừa không phải để làm gì.", L_INH_VI)
write_lesson(MOD, "protected-members", "Protected Members and Constructor Chaining", "The middle door, why protected data is a trap, and explicit base initialization.", 20, L_PROT_EN, "Protected member và nối constructor", "Cánh cửa giữa, vì sao dữ liệu protected là cái bẫy, và khởi tạo base tường minh.", L_PROT_VI)
write_lesson(MOD, "ctor-dtor-order", "Construction and Destruction Order", "Bases first, members in declaration order, destruction in reverse — and why it cannot be otherwise.", 20, L_ORDER_EN, "Thứ tự dựng và hủy", "Base trước, member theo thứ tự khai báo, hủy ngược lại — và vì sao không thể khác.", L_ORDER_VI)
write_lesson(MOD, "overriding", "Overriding and the override Keyword", "Exact signature matching, override vs overload, and how override turns silent bugs into compile errors.", 20, L_OVERRIDE_EN, "Override và từ khóa override", "Khớp chữ ký tuyệt đối, override khác overload, và override biến bug câm thành lỗi biên dịch.", L_OVERRIDE_VI)
write_lesson(MOD, "polymorphism", "Virtual Functions and Polymorphism", "Dynamic dispatch through base pointers, abstract classes, and why by-value storage breaks polymorphism.", 30, L_POLY_EN, "Hàm ảo và đa hình", "Dispatch động qua base pointer, class trừu tượng, và vì sao lưu theo giá trị phá đa hình.", L_POLY_VI)
write_lesson(MOD, "virtual-destructors", "Virtual Destructors", "Deleting through a base pointer without one is UB — the one-line rule and its cost.", 15, L_VDTOR_EN, "Virtual destructor", "Xóa qua base pointer thiếu virtual destructor là UB — quy tắc một dòng và cái giá của nó.", L_VDTOR_VI)

write_module(
    MOD,
    "Inheritance & Polymorphism",
    "Public inheritance, virtual dispatch, abstract interfaces, and the virtual-destructor rule that keeps polymorphic cleanup safe.",
    "Kế thừa & Đa hình",
    "Public inheritance, dispatch ảo, interface trừu tượng, và quy tắc virtual destructor giữ cho việc dọn dẹp đa hình an toàn.",
    ["inheritance", "protected-members", "ctor-dtor-order", "overriding", "polymorphism", "virtual-destructors", "advanced-checkpoint-polymorphism"],
    ["cppi-p3-inheritance", "cppi-p3-polymorphism"],
)
print("module 3 emitted")
