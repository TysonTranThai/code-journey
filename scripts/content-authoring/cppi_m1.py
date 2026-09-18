#!/usr/bin/env python3
"""C++ Intermediate — Module 1: memory, pointers & lifetime."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "memory-and-lifetime"

# ── lesson 1.1 — review ──────────────────────────────────────────────────────
L_REVIEW_EN = """
You finished Beginner, so you can already write functions, use `std::vector`,
read files, and reason about basic RAII. Intermediate starts by tightening the
mental model you will rely on for everything that follows: **every object has
a lifetime, and someone is responsible for it.**

## The three questions to ask about any object

1. **Where does it live?** — automatic (stack), static (global), or dynamic (heap).
2. **When does it die?** — end of scope, end of program, or an explicit `delete`.
3. **Who is responsible?** — one owner, always; everyone else borrows.

```cpp
#include <string>
#include <vector>

int counter = 42;                 // static: lives for the whole program

struct Session {
    std::string user;
    explicit Session(std::string u) : user{std::move(u)} {}
    ~Session() { /* release anything the session owns */ }
};

void demo() {
    int local = 7;                // automatic: dies at the closing brace
    Session s{"ana"};             // automatic; destructor runs at scope exit
    std::vector<int> v{1, 2, 3};  // the vector owns its heap buffer; frees it
}                                 // <- everything destroyed in REVERSE order
```

## Review: the discipline you already know

- Prefer `const` on anything that should not change.
- Pass non-trivial objects by `const&`; return by value.
- Containers manage their own memory — that is why they beat raw arrays.
- Initializer lists and `{}` braces beat `=` for consistency.

If any of those feel shaky, revisit the relevant Beginner module before
continuing; Intermediate builds every new idea on exactly these foundations.
"""

L_REVIEW_VI = """
Bạn đã hoàn thành Cơ bản: biết viết hàm, dùng `std::vector`, đọc file và suy
luận về RAII cơ bản. Trung cấp bắt đầu bằng cách siết lại mô hình tư duy mà
mọi phần sau sẽ dựa vào: **mọi đối tượng đều có vòng đời, và luôn có một chủ
sở hữu chịu trách nhiệm về nó.**

## Ba câu hỏi cần đặt ra với mọi đối tượng

1. **Nó sống ở đâu?** — tự động (stack), tĩnh (toàn cục), hay động (heap).
2. **Khi nào nó chết?** — hết phạm vi, kết thúc chương trình, hoặc lệnh `delete`.
3. **Ai chịu trách nhiệm?** — một chủ sở hữu duy nhất; mọi người khác chỉ mượn.

```cpp
#include <string>
#include <vector>

int counter = 42;                 // tĩnh: sống suốt chương trình

struct Session {
    std::string user;
    explicit Session(std::string u) : user{std::move(u)} {}
    ~Session() { /* giải phóng tài nguyên session sở hữu */ }
};

void demo() {
    int local = 7;                // tự động: chết khi đóng ngoặc
    Session s{"ana"};             // tự động; destructor chạy khi ra khỏi phạm vi
    std::vector<int> v{1, 2, 3};  // vector sở hữu buffer trên heap; tự giải phóng
}                                 // <- mọi thứ bị hủy theo thứ tự NGƯỢC lại
```

## Ôn lại kỷ luật bạn đã biết

- Dùng `const` cho mọi thứ không được thay đổi.
- Truyền đối tượng không tầm thường bằng `const&`; trả về bằng giá trị.
- Container tự quản lý bộ nhớ — đó là lý do chúng thắng mảng thô.
- Initializer list và cặp `{}` nhất quán hơn `=`.

Nếu phần nào còn lắt nhắt, hãy ôn lại module tương ứng của Cơ bản trước;
Trung cấp xây mọi ý mới trên đúng nền tảng này.
"""

# ── lesson 1.2 — references ──────────────────────────────────────────────────
L_REF_EN = """
A **reference** is a second name for an existing object. Once bound, a
reference can never refer to anything else — assignment goes through it to
the object. References must be initialized and can never be null.

```cpp
void double_it(int& out) { out *= 2; }       // non-const: writes through

void report(const std::string& name) {       // const&: read-only borrow
    std::cout << name << '\n';
}

int main_cj_reference() {
    int x = 5;
    int& alias = x;         // binding, not copying
    alias = 9;              // x is now 9
    double_it(x);           // x is now 18
    return 0;
}
```

## Choosing between by-value, by-reference, and const&

| You want... | Pass by | Why |
|---|---|---|
| a private copy the callee may change | value | cheap for small types |
| to modify the caller's object | `T&` | the callee writes through |
| read-only access, no copy | `const T&` | zero copy, cannot write |
| an optional "no object" state | pointer (later) or `std::optional` | references cannot be null |

## Rules that keep references safe

- Never return a reference to a local — the object dies before the caller reads it.
- Range-based loops over containers should take `const auto&` (read) or `auto&` (modify).
- A reference member makes a type non-assignable; usually prefer a pointer or value member.

```cpp
std::vector<int> data{3, 1, 2};
for (const auto& value : data) std::cout << value;   // read: no copy
for (auto& value : data) value *= 10;                // write in place
```
"""

L_REF_VI = """
**Reference** là tên thứ hai của một đối tượng đã tồn tại. Một khi đã được
gắn, reference không bao giờ trỏ sang đối tượng khác — phép gán đi xuyên qua
nó tới đối tượng gốc. Reference phải được khởi tạo và không bao giờ null.

```cpp
void double_it(int& out) { out *= 2; }       // non-const: ghi xuyên qua

void report(const std::string& name) {       // const&: mượn chỉ-đọc
    std::cout << name << '\n';
}

int main_cj_reference() {
    int x = 5;
    int& alias = x;         // gắn kết, không sao chép
    alias = 9;              // x giờ là 9
    double_it(x);           // x giờ là 18
    return 0;
}
```

## Chọn giữa truyền giá trị, truyền tham chiếu, và const&

| Bạn muốn... | Truyền bằng | Lý do |
|---|---|---|
| bản sao riêng mà hàm được thay đổi | giá trị | rẻ với kiểu nhỏ |
| sửa đối tượng của bên gọi | `T&` | hàm được ghi xuyên qua |
| chỉ đọc, không sao chép | `const T&` | không copy, không ghi được |
| trạng thái "có thể không có đối tượng" | pointer (sau này) hoặc `std::optional` | reference không thể null |

## Quy tắc giữ reference an toàn

- Không bao giờ trả về reference tới biến cục bộ — đối tượng chết trước khi bên gọi đọc.
- Vòng lặp range-based trên container nên dùng `const auto&` (đọc) hoặc `auto&` (sửa).
- Member kiểu reference khiến kiểu không thể gán; thường nên dùng pointer hoặc giá trị.

```cpp
std::vector<int> data{3, 1, 2};
for (const auto& value : data) std::cout << value;   // đọc: không copy
for (auto& value : data) value *= 10;                // ghi tại chỗ
"""

# ── lesson 1.3 — pointers ──────────────────────────────────────────────────
L_PTR_EN = """
A **pointer** stores the address of an object (or nothing, when `nullptr`).
Unlike a reference, a pointer can be reseated, compared, and incremented —
and it can be null, which makes it the tool for "maybe no object".

```cpp
int main_cj_pointer() {
    int value = 41;
    int* p = &value;          // p holds the address of value
    *p += 1;                  // dereference: value is now 42
    p = nullptr;              // p now points at nothing

    if (p) {                  // ALWAYS check before dereferencing
        std::cout << *p;
    }
    return 0;
}
```

## Reading pointer declarations out loud

- `int* p` — "p is a pointer to int".
- `const int* p` — pointer to const int: the *pointee* is read-only.
- `int* const p` — const pointer to int: the *pointer* cannot reseat.
- `const int* const p` — neither pointer nor pointee may change.

Read the declaration from right to left and `const` never surprises you.

## Pointer + const& decide most interfaces

```cpp
void rename(std::string* out, const std::string& fallback);
// out: optional (caller may pass nullptr) and written through
// fallback: required, read-only
```

A reference says "I need an object". A pointer says "I might not get one".
Document which contract each parameter has.
"""

L_PTR_VI = """
**Pointer** lưu địa chỉ của một đối tượng (hoặc không trỏ đâu cả, khi là
`nullptr`). Khác reference, pointer có thể trỏ lại, so sánh, tăng giảm —
và có thể null, nên nó là công cụ cho trạng thái "có thể không có đối tượng".

```cpp
int main_cj_pointer() {
    int value = 41;
    int* p = &value;          // p giữ địa chỉ của value
    *p += 1;                  // dereference: value giờ là 42
    p = nullptr;              // p không trỏ đâu cả

    if (p) {                  // LUÔN kiểm tra trước khi dereference
        std::cout << *p;
    }
    return 0;
}
```

## Đọc khai báo pointer thành lời

- `int* p` — "p là pointer tới int".
- `const int* p` — pointer tới const int: *đối tượng bị trỏ* chỉ đọc.
- `int* const p` — const pointer tới int: *pointer* không thể trỏ lại.
- `const int* const p` — cả pointer lẫn đối tượng đều không đổi.

Đọc khai báo từ phải sang trái, `const` sẽ không bao giờ gây bất ngờ.

## Pointer + const& quyết định phần lớn interface

```cpp
void rename(std::string* out, const std::string& fallback);
// out: tùy chọn (bên gọi có thể truyền nullptr) và được ghi xuyên qua
// fallback: bắt buộc, chỉ đọc
```

Reference nói "tôi cần một đối tượng". Pointer nói "có thể tôi không có".
Hãy ghi rõ hợp đồng của từng tham số.
"""

# ── lesson 1.4 — dynamic memory ──────────────────────────────────────────
L_DYN_EN = """
`new` allocates an object on the heap; `delete` destroys it. The pair is the
last resort in modern C++ — containers and smart pointers own heap memory for
you — but you must understand it because every tool you use is built on it.

```cpp
#include <string>

int main_cj_dynamic() {
    int* single = new int{7};            // one int on the heap
    delete single;                        // exactly one delete

    std::string* word = new std::string{"hi"};
    delete word;                          // destructor runs here

    int* arr = new int[5]{};              // array of 5 zeros
    delete[] arr;                         // NOTE the [] — must match new[]
    return 0;
}
```

## The three ways to leak

1. `new` without any `delete` — ownership forgotten.
2. Early `return` or thrown exception between `new` and `delete`.
3. `delete` on a pointer someone else also deletes — double free.

```cpp
void risky() {
    int* p = new int{1};
    if (p == nullptr) { /* cannot happen, but imagine an early return here */ }
    may_throw();                          // if this throws, p leaks
    delete p;
}
```

That second leak is the killer: it happens *rarely*, exactly when the program
is misbehaving. RAII (Module 8) removes the entire class of bugs by making a
destructor do the `delete` — and `std::vector` already does it for buffers.

## new/delete vs new[]/delete[]

They are different operators with different layouts. Mixing them is undefined
behavior. Rule of thumb: **you should almost never need either** — reach for
`std::vector`, `std::string`, or (Module 8) smart pointers first.
"""

L_DYN_VI = """
`new` cấp phát một đối tượng trên heap; `delete` hủy nó. Cặp này là lựa chọn
cuối cùng trong C++ hiện đại — container và smart pointer sở hữu bộ nhớ heap
giúp bạn — nhưng bạn phải hiểu nó vì mọi công cụ bạn dùng đều được xây trên nó.

```cpp
#include <string>

int main_cj_dynamic() {
    int* single = new int{7};            // một int trên heap
    delete single;                        // đúng một lần delete

    std::string* word = new std::string{"hi"};
    delete word;                          // destructor chạy tại đây

    int* arr = new int[5]{};              // mảng 5 phần tử 0
    delete[] arr;                         // CHÚ Ý dấu [] — phải khớp new[]
    return 0;
}
```

## Ba cách rò rỉ bộ nhớ

1. `new` mà không có `delete` nào — đánh mất ownership.
2. Lệnh `return` sớm hoặc exception ném ra giữa `new` và `delete`.
3. `delete` một pointer mà người khác cũng delete — double free.

```cpp
void risky() {
    int* p = new int{1};
    may_throw();                          // nếu hàm này ném, p bị rò rỉ
    delete p;
}
```

Rò rỉ thứ hai là hiểm họa nhất: nó xảy ra *hiếm khi*, đúng lúc chương trình
đang bất thường. RAII (Module 8) xóa sổ cả lớp lỗi này bằng cách để destructor
làm việc `delete` — còn `std::vector` đã làm sẵn điều đó cho buffer.

## new/delete khác new[]/delete[]

Chúng là hai toán tử khác nhau với bố cục bộ nhớ khác nhau. Trộn chúng là
hành vi không xác định. Nguyên tắc: **hầu như bạn không bao giờ cần cả hai** —
hãy chọn `std::vector`, `std::string`, hoặc (Module 8) smart pointer trước.
"""

# ── lesson 1.5 — const correctness ───────────────────────────────────────
L_CONST_EN = """
`const` is a promise you encode in the type system: this thing will not be
modified. Applied consistently it documents intent, lets the compiler catch
bugs, and unlocks read-only APIs.

```cpp
#include <string>
#include <vector>

long total(const std::vector<long>& prices) {   // promise: no mutation
    long sum = 0;
    for (const long& p : prices) sum += p;
    return sum;
}

class Cart {
public:
    long total() const { return total_; }        // const member: read-only view
    void add(long cents) { total_ += cents; }    // non-const: mutates
private:
    long total_{0};
};
```

## The const ladder

- `const T&` parameter — cheap read-only input.
- `T get() const` — a member function that does not mutate (`const` after `)`).
- `const` local — write once, never again; intent made explicit.
- `constexpr` (Module 7) — computable at compile time.

## How to think about it

Start maximal: make everything `const`. Removing `const` when you genuinely
need mutation is easy and safe; adding it back across a codebase never is.
Const on a member function is part of the *interface contract* — callers can
rely on it, and only a `mutable` member (rare, for caches/mutexes) may change
inside one.
"""

L_CONST_VI = """
`const` là lời hứa được mã hóa vào hệ thống kiểu: thứ này sẽ không bị sửa.
Áp dụng nhất quán, nó ghi lại ý định, giúp compiler bắt lỗi, và mở khóa các
API chỉ đọc.

```cpp
#include <string>
#include <vector>

long total(const std::vector<long>& prices) {   // lời hứa: không sửa
    long sum = 0;
    for (const long& p : prices) sum += p;
    return sum;
}

class Cart {
public:
    long total() const { return total_; }        // const member: góc nhìn chỉ đọc
    void add(long cents) { total_ += cents; }    // non-const: thay đổi trạng thái
private:
    long total_{0};
};
```

## Thang const

- Tham số `const T&` — đầu vào rẻ, chỉ đọc.
- `T get() const` — hàm thành viên không thay đổi đối tượng (`const` sau `)`).
- Biến cục bộ `const` — gán một lần, không gán nữa; ý định rõ ràng.
- `constexpr` (Module 7) — tính được lúc biên dịch.

## Cách tư duy

Bắt đầu từ mức tối đa: đặt `const` cho mọi thứ. Bỏ `const` khi thật sự cần
thay đổi thì dễ và an toàn; thêm lại trên cả một codebase thì không bao giờ vậy.
Const trên hàm thành viên là một phần *hợp đồng interface* — bên gọi được phép
tin tưởng, và chỉ member `mutable` (hiếm, cho cache/mutex) mới được đổi bên trong.
"""

# ── lesson 1.6 — stack vs heap ──────────────────────────────────────────
L_STACK_EN = """
The **stack** is a fast, bounded region for automatic objects; the **heap** is
a large, slower region you manage explicitly. Choosing where an object lives
is a design decision.

```cpp
#include <vector>

struct Sample { double readings[64]; };

Sample make_on_stack() {
    Sample s{};              // 512 bytes on the stack: fast, dies at return
    return s;                // moved/copied out — fine for most sizes
}

std::vector<Sample> make_many(int n) {
    std::vector<Sample> out;
    out.reserve(n);          // n * 512 bytes on the heap, owned by the vector
    for (int i = 0; i < n; ++i) out.push_back(make_on_stack());
    return out;              // one owner, automatic cleanup
}
```

## Trade-offs in one table

| | Stack | Heap |
|---|---|---|
| speed | very fast (pointer bump) | slower (allocator bookkeeping) |
| lifetime | ends at scope exit | until you free it |
| size | small (KB–MB limit) | large |
| failure mode | stack overflow | allocation throws `bad_alloc` |
| who cleans | compiler, always | you, via RAII |

## Practical guidance

- Local, small, scope-bound → stack (automatic). This is the default.
- Size known only at runtime, shared ownership, or big buffers → heap, owned by a container or smart pointer.
- Deep recursion with big locals overflows the stack — that is the classic crash when people "just add recursion".

Everything else in this course — containers, smart pointers, polymorphic
ownership — is machinery for putting heap memory under automatic-lifetime rules.
"""

L_STACK_VI = """
**Stack** là vùng nhớ nhanh, giới hạn dành cho đối tượng tự động; **heap** là
vùng lớn hơn, chậm hơn mà bạn quản lý tường minh. Chọn nơi đối tượng sống là
một quyết định thiết kế.

```cpp
#include <vector>

struct Sample { double readings[64]; };

Sample make_on_stack() {
    Sample s{};              // 512 byte trên stack: nhanh, chết khi return
    return s;                // được move/copy ra ngoài — ổn với kích thước nhỏ
}

std::vector<Sample> make_many(int n) {
    std::vector<Sample> out;
    out.reserve(n);          // n * 512 byte trên heap, vector là chủ sở hữu
    for (int i = 0; i < n; ++i) out.push_back(make_on_stack());
    return out;              // một chủ sở hữu, dọn dẹp tự động
}
```

## Đánh đổi trong một bảng

| | Stack | Heap |
|---|---|---|
| tốc độ | rất nhanh (tăng con trỏ) | chậm hơn (sổ sách allocator) |
| vòng đời | kết thúc khi ra khỏi phạm vi | đến khi bạn giải phóng |
| kích thước | nhỏ (giới hạn KB–MB) | lớn |
| lỗi gặp phải | tràn stack | cấp phát ném `bad_alloc` |
| ai dọn | compiler, luôn luôn | bạn, qua RAII |

## Hướng dẫn thực dụng

- Cục bộ, nhỏ, gắn với phạm vi → stack (tự động). Đây là mặc định.
- Kích thước chỉ biết lúc chạy, chia sẻ sở hữu, hoặc buffer lớn → heap, do container hoặc smart pointer sở hữu.
- Đệ quy sâu với biến cục bộ lớn sẽ tràn stack — crash kinh điển khi người ta "thêm đệ quy cho nhanh".

Mọi thứ còn lại trong khóa này — container, smart pointer, sở hữu đa hình —
đều là cơ chế đặt bộ nhớ heap dưới quy tắc vòng đời tự động.
"""

# ── practice sets ──────────────────────────────────────────────────────────
P1 = [
    challenge(
        "cppi-m1-ref-scale",
        "Scale through a reference",
        "Implement `void scale(int& value, int factor)` that multiplies `value` in place through the reference (no return value, no copies).",
        "#include <iostream>\n\nvoid scale(int& value, int factor);\n",
        [
            ("basic", "int v = 21;\nscale(v, 2);\nCHECK_EQ(v, 42);", "Assignment through the reference writes to the caller's int."),
            ("by-one", "int v = 5;\nscale(v, 1);\nCHECK_EQ(v, 5);", "Factor 1 leaves the value unchanged."),
            ("negative", "int v = -4;\nscale(v, -3);\nCHECK_EQ(v, 12);", "Negative factors multiply normally."),
        ],
        level="guided",
    ),
    challenge(
        "cppi-m1-ref-count-vowels",
        "Borrow, don't copy",
        "Implement `int count_vowels(const std::string& text)` taking the string by `const&` (no copy) and returning the number of vowels a e i o u (case-insensitive).",
        "#include <string>\n\nint count_vowels(const std::string& text);\n",
        [
            ("mixed", "CHECK_EQ(count_vowels(\"Programming\"), 3);", "o, a, i — count each once."),
            ("empty", "CHECK_EQ(count_vowels(\"\"), 0);", "The empty string borrows fine; zero vowels."),
            ("upper", "CHECK_EQ(count_vowels(\"AEIOU\"), 5);", "Uppercase vowels count too."),
        ],
        level="independent",
    ),
    challenge(
        "cppi-m1-ref-swap",
        "Swap through references",
        "Implement `void swap_ints(int& a, int& b)` exchanging the two caller objects using only references (no pointers, no return).",
        "#include <iostream>\n\nvoid swap_ints(int& a, int& b);\n",
        [
            ("swap", "int x = 1, y = 2;\nswap_ints(x, y);\nCHECK_EQ(x, 2);\nCHECK_EQ(y, 1);", "Classic three-line swap via a temporary."),
            ("same", "int x = 9;\nswap_ints(x, x);\nCHECK_EQ(x, 9);", "Swapping an object with itself must be harmless."),
        ],
        level="independent",
    ),
]

P2 = [
    challenge(
        "cppi-m1-ptr-deref-sum",
        "Dereference and sum",
        "Implement `int sum_through(const int* a, const int* b)` returning `*a + *b`. Either pointer may be null; treat a null as 0.",
        "#include <iostream>\n\nint sum_through(const int* a, const int* b);\n",
        [
            ("both", "int x = 3, y = 4;\nCHECK_EQ(sum_through(&x, &y), 7);", "Dereference each pointer once."),
            ("null-a", "int y = 4;\nCHECK_EQ(sum_through(nullptr, &y), 4);", "Null means 0 — check before dereferencing."),
            ("both-null", "CHECK_EQ(sum_through(nullptr, nullptr), 0);", "Two nulls sum to zero without crashing."),
        ],
        level="guided",
    ),
    challenge(
        "cppi-m1-ptr-max-of",
        "Optional result via pointer",
        "Implement `const int* max_of(const int* a, const int* b)`: return a pointer to the larger int; if both are null return nullptr; if one is null return the other's pointer.",
        "#include <iostream>\n\nconst int* max_of(const int* a, const int* b);\n",
        [
            ("both", "int x = 3, y = 9;\nCHECK_EQ(*max_of(&x, &y), 9);", "Return the address of the larger, not a copy."),
            ("one-null", "int x = 5;\nconst int* r = max_of(&x, nullptr);\nCHECK(r != nullptr);\nCHECK_EQ(*r, 5);", "One side missing → the other wins."),
            ("none", "CHECK(max_of(nullptr, nullptr) == nullptr);", "No objects → nullptr is the honest answer."),
        ],
        level="independent",
    ),
]

P3 = [
    challenge(
        "cppi-m1-const-thermo",
        "A const-correct thermometer",
        "Implement `struct Thermometer` with a private `double celsius_{0.0};`, `void set(double c)` storing the value, `double celsius() const` returning it, and `double fahrenheit() const` returning `celsius() * 9.0 / 5.0 + 32.0`. Both getters must be `const`.",
        "#include <iostream>\n\nstruct Thermometer {\n    // your declarations and one private member\n};\n",
        [
            ("roundtrip", "Thermometer t;\nt.set(100.0);\nCHECK_NEAR(t.celsius(), 100.0, 1e-9);\nCHECK_NEAR(t.fahrenheit(), 212.0, 1e-9);", "Getters marked const can be called on a const object later."),
            ("zero", "Thermometer t;\nCHECK_NEAR(t.fahrenheit(), 32.0, 1e-9);", "Default value 0 °C is 32 °F."),
            ("const-object", "Thermometer t;\nt.set(25.0);\nconst Thermometer& view = t;\nCHECK_NEAR(view.celsius(), 25.0, 1e-9);", "A const reference may only call const members — proof your getters are const."),
        ],
        level="combination",
    ),
]

VI_P1 = {
    "cppi-m1-ref-scale": vi_challenge("Phóng đại qua reference", "Cài `void scale(int& value, int factor)` nhân `value` tại chỗ qua reference (không trả giá trị, không sao chép).", [("basic", "Gán qua reference ghi vào int của bên gọi."), ("by-one", "Hệ số 1 giữ nguyên giá trị."), ("negative", "Hệ số âm nhân bình thường.")]),
    "cppi-m1-ref-count-vowels": vi_challenge("Mượn, đừng copy", "Cài `int count_vowels(const std::string& text)` nhận chuỗi bằng `const&` (không copy), trả số nguyên âm a e i o u (không phân biệt hoa thường).", [("mixed", "o, a, i — đếm mỗi lần một."), ("empty", "Chuỗi rỗng mượn bình thường; không nguyên âm."), ("upper", "Nguyên âm hoa cũng được đếm.")]),
    "cppi-m1-ref-swap": vi_challenge("Hoán đổi qua reference", "Cài `void swap_ints(int& a, int& b)` hoán đổi hai đối tượng của bên gọi chỉ bằng reference (không pointer, không return).", [("swap", "Hoán đổi ba dòng kinh điển qua biến tạm."), ("same", "Hoán đổi một đối tượng với chính nó phải vô hại.")]),
}
VI_P2 = {
    "cppi-m1-ptr-deref-sum": vi_challenge("Dereference và cộng", "Cài `int sum_through(const int* a, const int* b)` trả `*a + *b`. Con trỏ nào cũng có thể null; null tính là 0.", [("both", "Dereference mỗi pointer một lần."), ("null-a", "Null nghĩa là 0 — kiểm tra trước khi dereference."), ("both-null", "Hai null cộng lại bằng không, không crash.")]),
    "cppi-m1-ptr-max-of": vi_challenge("Kết quả tùy chọn qua pointer", "Cài `const int* max_of(const int* a, const int* b)`: trả pointer tới số lớn hơn; cả hai null thì trả nullptr; một null thì trả pointer bên kia.", [("both", "Trả địa chỉ của số lớn, không phải bản sao."), ("one-null", "Một bên vắng → bên kia thắng."), ("none", "Không có đối tượng → nullptr là câu trả lời trung thực.")]),
}
VI_P3 = {
    "cppi-m1-const-thermo": vi_challenge("Nhiệt kế const-correct", "Cài `struct Thermometer` với `double celsius_{0.0};` private, `void set(double c)`, `double celsius() const`, và `double fahrenheit() const` trả `celsius() * 9.0 / 5.0 + 32.0`. Cả hai getter phải là `const`.", [("roundtrip", "Getter const có thể gọi trên đối tượng const sau này."), ("zero", "Giá trị mặc định 0 °C là 32 °F."), ("const-object", "Const reference chỉ gọi được hàm const — bằng chứng getter của bạn là const.")]),
}

# full learner files (boilerplate merged) for the ledger
R_SCALE = "void scale(int& value, int factor) { value *= factor; }\n"
W_SCALE = "void scale(int& value, int factor) { value = factor; }\n"  # assignment instead of *=
R_VOWELS = "#include <string>\nint count_vowels(const std::string& text) {\n    int n = 0;\n    for (char c : text) {\n        char lo = static_cast<char>(c | 0x20);\n        if (lo=='a'||lo=='e'||lo=='i'||lo=='o'||lo=='u') ++n;\n    }\n    return n;\n}\n"
W_VOWELS = "#include <string>\nint count_vowels(const std::string& text) {\n    int n = 0;\n    for (char c : text) {\n        if (c=='a'||c=='e'||c=='i'||c=='o'||c=='u') ++n;  // forgets uppercase\n    }\n    return n;\n}\n"
R_SWAP = "void swap_ints(int& a, int& b) { int tmp = a; a = b; b = tmp; }\n"
W_SWAP = "void swap_ints(int& a, int& b) { int tmp = a; a = b; }\n"  # forgets to write b
R_SUM = "int sum_through(const int* a, const int* b) {\n    return (a ? *a : 0) + (b ? *b : 0);\n}\n"
W_SUM = "int sum_through(const int* a, const int* b) {\n    return *a + *b;  // dereferences null\n}\n"
R_MAX = "const int* max_of(const int* a, const int* b) {\n    if (!a) return b;\n    if (!b) return a;\n    return (*a >= *b) ? a : b;\n}\n"
W_MAX = "const int* max_of(const int* a, const int* b) {\n    return (*a >= *b) ? a : b;  // crashes when either is null\n}\n"
R_THERMO = "struct Thermometer {\npublic:\n    void set(double c) { celsius_ = c; }\n    double celsius() const { return celsius_; }\n    double fahrenheit() const { return celsius_ * 9.0 / 5.0 + 32.0; }\nprivate:\n    double celsius_{0.0};\n};\n"
W_THERMO = "struct Thermometer {\npublic:\n    void set(double c) { celsius_ = c; }\n    double celsius() { return celsius_; }  // not const\n    double fahrenheit() const { return celsius_ * 9.0 / 5.0 + 32.0; }\nprivate:\n    double celsius_{0.0};\n};\n"

write_practice(
    MOD, "cppi-p1-refs",
    "References: borrow and write through",
    "Warm-up with references: mutate through an alias, count without copying, swap in place.",
    "Reference: mượn và ghi xuyên qua",
    "Làm quen reference: sửa qua alias, đếm không copy, hoán đổi tại chỗ.",
    "references", 25, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m1-ref-scale", R_SCALE, W_SCALE),
        ("cppi-m1-ref-count-vowels", R_VOWELS, W_VOWELS),
        ("cppi-m1-ref-swap", R_SWAP, W_SWAP),
    ],
)

write_practice(
    MOD, "cppi-p1-pointers",
    "Pointers and the null contract",
    "Handle optional objects honestly: sum through possibly-null pointers, return an optional max.",
    "Pointer và hợp đồng null",
    "Đối xử trung thực với đối tượng tùy chọn: cộng qua pointer có thể null, trả max tùy chọn.",
    "pointers", 25, "intermediate", P2, VI_P2,
    solutions=[
        ("cppi-m1-ptr-deref-sum", R_SUM, W_SUM),
        ("cppi-m1-ptr-max-of", R_MAX, W_MAX),
    ],
)

write_practice(
    MOD, "cppi-p1-const",
    "Design a const-correct type",
    "Build a small type whose read-only API is enforced by const.",
    "Thiết kế kiểu const-correct",
    "Xây một kiểu nhỏ mà API chỉ-read được const bảo vệ.",
    "const-correctness", 20, "intermediate", P3, VI_P3,
    solutions=[
        ("cppi-m1-const-thermo", R_THERMO, W_THERMO),
    ],
)

# ── checkpoint 1 ──────────────────────────────────────────────────────────
CP1_CH = challenge(
    "cppi-checkpoint-memory",
    "Checkpoint: Memory & Lifetime",
    "Implement `long bounded_total(const long* values, int count, long cap)`: sum up to `count` values read through the pointer (stop early once the running total would exceed `cap` — in that case return `cap`). A null pointer with `count > 0`, or a negative `count`, must throw `std::invalid_argument`.",
    "#include <stdexcept>\n#include <iostream>\n\nlong bounded_total(const long* values, int count, long cap);\n",
    [
        ("simple", "long v[]{1, 2, 3};\nCHECK_EQ(bounded_total(v, 3, 100), 6);", "Normal path sums all values."),
        ("cap", "long v[]{50, 60, 5};\nCHECK_EQ(bounded_total(v, 3, 100), 100);", "50 fits; 60 would exceed → clamp at cap."),
        ("null", "CHECK_THROWS(bounded_total(nullptr, 2, 100));", "Null with a positive count is a caller bug → throw."),
        ("negative-count", "long v[]{1};\nCHECK_THROWS(bounded_total(v, -1, 100));", "Negative count is invalid → throw."),
    ],
    difficulty="intermediate",
)
VI_CP1 = vi_challenge(
    "Kiểm tra điểm: Bộ nhớ & Vòng đời",
    "Cài `long bounded_total(const long* values, int count, long cap)`: cộng tối đa `count` giá trị đọc qua pointer (dừng sớm khi tổng sẽ vượt `cap` — khi đó trả `cap`). Pointer null với `count > 0`, hoặc `count` âm, phải ném `std::invalid_argument`.",
    [("simple", "Đường thường cộng đủ giá trị."), ("cap", "50 vừa; 60 sẽ vượt → chặn tại cap."), ("null", "Null với count dương là lỗi của bên gọi → ném."), ("negative-count", "Count âm là bất hợp lệ → ném.")],
)

write_checkpoint(
    MOD, "advanced-checkpoint-memory",
    "Checkpoint: Memory & Lifetime",
    "Pointers with a null contract, const-correct input, and exception discipline in one function.",
    30,
    """
This checkpoint combines the module's skills into one function with an honest
contract:

- input is **borrowed** (`const long*`, possibly null) — never copied, never freed
- the count is validated — invalid input **throws**, it is not silently ignored
- the cap bounds the result — early exit is part of the spec, not a hack

Write `bounded_total` so all four tests pass, then compare with the reference:
notice there is no `new`, no `delete`, and no copy of the caller's data
anywhere. That is what lifetime-aware C++ looks like.
""",
    "Kiểm tra điểm: Bộ nhớ & Vòng đời",
    "Pointer với hợp đồng null, đầu vào const-correct, và kỷ luật exception trong một hàm.",
    """
Kiểm tra điểm này gộp kỹ năng của module vào một hàm với hợp đồng trung thực:

- đầu vào được **mượn** (`const long*`, có thể null) — không copy, không free
- count được kiểm tra — đầu vào bất hợp lệ thì **ném exception**, không bỏ qua
- cap chặn kết quả — dừng sớm là phần của đặc tả, không phải mẹo

Viết `bounded_total` để cả bốn test đều pass, rồi so với lời giải: không có
`new`, không có `delete`, không copy dữ liệu của bên gọi. Đó là C++ hiểu
vòng đời.
""",
    CP1_CH, VI_CP1,
    solution="#include <stdexcept>\n\nlong bounded_total(const long* values, int count, long cap) {\n    if ((values == nullptr && count > 0) || count < 0) {\n        throw std::invalid_argument(\"bounded_total: invalid input\");\n    }\n    long total = 0;\n    for (int i = 0; i < count; ++i) {\n        if (total + values[i] > cap) {\n            return cap;\n        }\n        total += values[i];\n    }\n    return total;\n}\n",
    wrong="#include <stdexcept>\n\nlong bounded_total(const long* values, int count, long cap) {\n    long total = 0;\n    for (int i = 0; i < count; ++i) {  // no validation, no cap\n        total += values[i];\n    }\n    return total;\n}\n",
)

# ── lessons ──────────────────────────────────────────────────────────
write_lesson(MOD, "fundamentals-review", "Intermediate Launchpad: the Model You Already Have", "Where objects live, when they die, and who is responsible — the three questions every later module builds on.", 15, L_REVIEW_EN, "Bệ phóng Trung cấp: mô hình bạn đã có", "Đối tượng sống ở đâu, chết khi nào, ai chịu trách nhiệm — ba câu hỏi mọi module sau đều dựa vào.", L_REVIEW_VI)
write_lesson(MOD, "references", "References: Second Names for Objects", "Bind once, borrow forever — when to pass by value, T&, and const& — and the rules that keep references safe.", 20, L_REF_EN, "Reference: tên thứ hai của đối tượng", "Gắn một lần, mượn mãi mãi — khi nào truyền giá trị, T&, và const& — cùng quy tắc giữ reference an toàn.", L_REF_VI)
write_lesson(MOD, "pointers", "Pointers: Addresses and the Null Contract", "Pointers as optional object handles: dereferencing, const placement, and what a pointer parameter promises.", 20, L_PTR_EN, "Pointer: địa chỉ và hợp đồng null", "Pointer như thẻ đối tượng tùy chọn: dereference, vị trí const, và điều tham số pointer hứa.", L_PTR_VI)
write_lesson(MOD, "dynamic-memory", "Dynamic Memory: new, delete, and Leaks", "How heap allocation really works, the three ways to leak, and why modern C++ avoids raw new/delete.", 25, L_DYN_EN, "Bộ nhớ động: new, delete, và rò rỉ", "Cấp phát heap hoạt động thế nào, ba cách rò rỉ, và vì sao C++ hiện đại tránh new/delete thô.", L_DYN_VI)
write_lesson(MOD, "const-correctness", "Const Correctness as Design", "const as an encoded promise: the const ladder, const member functions, and starting-maximal discipline.", 20, L_CONST_EN, "Const correctness như thiết kế", "const như lời hứa mã hóa: thang const, hàm thành viên const, và kỷ luật bắt đầu từ tối đa.", L_CONST_VI)
write_lesson(MOD, "stack-vs-heap", "Stack vs Heap: Choosing Where Objects Live", "The trade-off table, allocation failure modes, and the guidance that decides storage for every object.", 20, L_STACK_EN, "Stack vs Heap: chọn nơi đối tượng sống", "Bảng đánh đổi, chế độ lỗi cấp phát, và hướng dẫn quyết định nơi lưu trữ cho mọi đối tượng.", L_STACK_VI)

# ── emit module ──────────────────────────────────────────────────────────
write_module(
    MOD,
    "Memory, Pointers & Lifetime",
    "References vs pointers, dynamic allocation, const correctness, and the lifetime model that separates working C++ from crashing C++.",
    "Bộ nhớ, con trỏ & vòng đời",
    "Reference và pointer, cấp phát động, const correctness, và mô hình vòng đời phân biệt C++ chạy được với C++ bị crash.",
    [
        "fundamentals-review",
        "references",
        "pointers",
        "dynamic-memory",
        "const-correctness",
        "stack-vs-heap",
        "advanced-checkpoint-memory",
    ],
    ["cppi-p1-refs", "cppi-p1-pointers", "cppi-p1-const"],
)
print("module 1 emitted")

