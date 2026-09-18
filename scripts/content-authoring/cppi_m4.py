#!/usr/bin/env python3
"""C++ Intermediate — Module 4: operators-copy-move.

REGENERATED from the emitted, harness-verified content (26/26 two-sided) after
the original source was corrupted by an escaping fix. Emitting this script is
idempotent: it reproduces the exact on-disk JSONs/MDX and appends the same
solution pairs to the ledger (duplicate keys are harmless — last write wins).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "operators-copy-move"

# ---- lesson operator-overloading ----------------------------------------
L_operator_overloading_EN = r"""Operators are ordinary functions with special names. Overloading them lets
your types read like the built-ins — but only when the meaning is obvious.

```cpp
class Money {
public:
    explicit Money(long cents) : cents_{cents} {}
    long cents() const { return cents_; }

private:
    long cents_;
};

inline Money operator+(const Money& a, const Money& b) {
    return Money{a.cents() + b.cents()};
}

inline bool operator==(const Money& a, const Money& b) {
    return a.cents() == b.cents();
}
```

## The decision procedure

1. Would the operator's meaning be **obvious** to any reader? `Money +
   Money` yes; `Money << int` no.
2. Prefer writing it as a **non-member** on top of the public interface
   (keeps encapsulation; enables symmetric conversions).
3. Members are required only for `=`, `()`, `[]`, `->`.
4. Semantic families go together: define `==` and `!=` consistently (C++20
   can synthesize `!=` from `==`); define `<` to match `==`'s ordering idea.

If an operator's semantics would surprise, use a named function instead —
`add_days(date, 3)` beats a mysterious `date + 3` for a `Date` where the
calendar rules are nontrivial.
"""

L_operator_overloading_VI = r"""Toán tử chỉ là hàm thường với tên đặc biệt. Nạp chồng chúng giúp kiểu của bạn
đọc tự nhiên như kiểu dựng sẵn — nhưng chỉ khi ý nghĩa hiển nhiên.

```cpp
class Money {
public:
    explicit Money(long cents) : cents_{cents} {}
    long cents() const { return cents_; }

private:
    long cents_;
};

inline Money operator+(const Money& a, const Money& b) {
    return Money{a.cents() + b.cents()};
}

inline bool operator==(const Money& a, const Money& b) {
    return a.cents() == b.cents();
}
```

## Quy trình quyết định

1. Ý nghĩa của toán tử có **hiển nhiên** với mọi người đọc không? `Money +
   Money` thì có; `Money << int` thì không.
2. Ưu tiên viết dạng **non-member** dựa trên interface public (giữ đóng gói;
   cho phép chuyển đổi đối xứng).
3. Chỉ `=`, `()`, `[]`, `->` là bắt buộc viết dạng member.
4. Các họ ngữ nghĩa đi cùng nhau: định nghĩa `==` và `!=` nhất quán (C++20
   có thể tự sinh `!=` từ `==`); `<` phải khớp với trật tự mà `==` gợi ý.

Nếu ngữ nghĩa gây bất ngờ, hãy dùng hàm có tên — `add_days(date, 3)` rõ hơn
một `date + 3` bí ẩn khi quy luật lịch của `Date` không đơn giản.
"""

# ---- lesson copy-semantics ----------------------------------------------
L_copy_semantics_EN = r"""When an object is copied (by value, from a container growth, pass-by-value),
C++ uses the **copy constructor**; on assignment, the **copy assignment
operator**. The compiler generates member-wise copies by default — correct
for value members, deeply wrong for raw owning pointers.

```cpp
#include <cstring>
#include <iostream>

class Buffer {
public:
    explicit Buffer(std::size_t n) : size_{n}, data_{new char[n]{}} {}
    ~Buffer() { delete[] data_; }

    Buffer(const Buffer& other)                       // copy ctor: deep copy
        : size_{other.size_}, data_{new char[other.size_]} {
        std::memcpy(data_, other.data_, size_);
    }

    Buffer& operator=(const Buffer& other) {           // copy assign
        if (this == &other) return *this;              // self-assignment guard
        char* fresh = new char[other.size_];           // allocate FIRST
        std::memcpy(fresh, other.data_, other.size_);
        delete[] data_;                                // only then release
        data_ = fresh;
        size_ = other.size_;
        return *this;
    }

    std::size_t size() const { return size_; }
    char& at(std::size_t i) { return data_[i]; }

private:
    std::size_t size_;
    char* data_;
};
```

## Rule of Three

If you write any of: destructor, copy constructor, copy assignment — you
almost certainly need all three. A destructor signals the type *owns* a
resource; default member-wise copying then creates two owners of one
resource (double-free), which is the classic crash.

## The copy-and-swap alternative

`Buffer& operator=(Buffer other) { swap(*this, other); return *this; }`
handles self-assignment, gives the strong exception guarantee, and is hard
to get wrong — at the cost of one extra copy.
"""

L_copy_semantics_VI = r"""Khi một đối tượng bị copy (truyền bằng giá trị, container tăng dung lượng...),
C++ dùng **copy constructor**; khi gán thì dùng **copy assignment**. Compiler
mặc định copy từng member — đúng với member kiểu giá trị, sai thảm khốc với
raw pointer sở hữu tài nguyên.

```cpp
#include <cstring>
#include <iostream>

class Buffer {
public:
    explicit Buffer(std::size_t n) : size_{n}, data_{new char[n]{}} {}
    ~Buffer() { delete[] data_; }

    Buffer(const Buffer& other)                       // copy ctor: deep copy
        : size_{other.size_}, data_{new char[other.size_]} {
        std::memcpy(data_, other.data_, size_);
    }

    Buffer& operator=(const Buffer& other) {           // copy assign
        if (this == &other) return *this;              // chặn tự-gán
        char* fresh = new char[other.size_];           // cấp phát TRƯỚC
        std::memcpy(fresh, other.data_, other.size_);
        delete[] data_;                                // rồi mới giải phóng
        data_ = fresh;
        size_ = other.size_;
        return *this;
    }

    std::size_t size() const { return size_; }
    char& at(std::size_t i) { return data_[i]; }

private:
    std::size_t size_;
    char* data_;
};
```

## Rule of Three

Nếu bạn viết một trong ba: destructor, copy constructor, copy assignment —
gần như chắc chắn bạn cần cả ba. Destructor báo hiệu kiểu này *sở hữu* tài
nguyên; copy mặc định từng member khi đó tạo hai chủ của một tài nguyên
(double-free) — crash kinh điển.

## Phương án copy-and-swap

`Buffer& operator=(Buffer other) { swap(*this, other); return *this; }` tự
xử lý tự-gán, đạt bảo đảm exception mạnh, và khó viết sai — đổi lại tốn một
lần copy.
"""

# ---- lesson move-semantics ----------------------------------------------
L_move_semantics_EN = r"""**Move semantics** transfer a resource from a dying object instead of copying
it. The move constructor "steals" the source's pointer and empties the
source — O(1) instead of O(n).

```cpp
#include <cstring>
#include <utility>

class Buffer {
public:
    // ... (from the Rule of Three) ...

    Buffer(Buffer&& other) noexcept                    // move ctor
        : size_{other.size_}, data_{other.data_} {
        other.data_ = nullptr;                          // leave source empty
        other.size_ = 0;
    }

    Buffer& operator=(Buffer&& other) noexcept {        // move assign
        if (this == &other) return *this;
        delete[] data_;
        data_ = other.data_;
        size_ = other.size_;
        other.data_ = nullptr;
        other.size_ = 0;
        return *this;
    }
    // ...
};

Buffer make_buffer() { return Buffer{1024}; }

int main_cj_move() {
    Buffer a{make_buffer()};     // move (or elided): no copy of 1024 bytes
    Buffer b{a};                 // copy: a still owns its data
    Buffer c{std::move(a)};      // move: a is now empty-but-valid
    return 0;
}
```

## Rule of Five and the moved-from state

Add the two move operations to the Rule of Three and you have five. Whenever
you declare a destructor or any copy operation, consider all five. A moved-
from object must be **valid** (destructible, assignable) — but its value is
unspecified; never assume it still holds data.

`noexcept` on moves matters: `std::vector` only moves elements during growth
if the move is `noexcept`, otherwise it must copy to keep the strong
guarantee.
"""

L_move_semantics_VI = r"""**Move semantics** chuyển tài nguyên từ một đối tượng sắp chết thay vì sao
chép nó. Move constructor "đoạt" pointer của nguồn và làm rỗng nguồn — O(1)
thay vì O(n).

```cpp
#include <cstring>
#include <utility>

class Buffer {
public:
    // ... (từ Rule of Three) ...

    Buffer(Buffer&& other) noexcept                    // move ctor
        : size_{other.size_}, data_{other.data_} {
        other.data_ = nullptr;                          // để nguồn rỗng
        other.size_ = 0;
    }

    Buffer& operator=(Buffer&& other) noexcept {        // move assign
        if (this == &other) return *this;
        delete[] data_;
        data_ = other.data_;
        size_ = other.size_;
        other.data_ = nullptr;
        other.size_ = 0;
        return *this;
    }
    // ...
};

Buffer make_buffer() { return Buffer{1024}; }

int main_cj_move() {
    Buffer a{make_buffer()};     // move (hoặc elided): không copy 1024 byte
    Buffer b{a};                 // copy: a vẫn giữ dữ liệu của nó
    Buffer c{std::move(a)};      // move: a giờ rỗng-nhưng-hợp-lệ
    return 0;
}
```

## Rule of Five và trạng thái moved-from

Cộng hai thao tác move vào Rule of Three, bạn có năm. Mỗi khi khai báo
destructor hay bất kỳ thao tác copy nào, hãy xét cả năm. Đối tượng moved-from
phải **hợp lệ** (hủy được, gán được) — nhưng giá trị của nó là không xác định;
đừng bao giờ giả sử nó còn giữ dữ liệu.

`noexcept` trên move rất quan trọng: `std::vector` chỉ move phần tử khi tăng
dung lượng nếu move là `noexcept`, nếu không nó buộc phải copy để giữ bảo đảm
mạnh.
"""

# ---- lesson stream-operators --------------------------------------------
L_stream_operators_EN = r"""`operator<<` and `operator>>` make your types print and parse like built-ins.
They must be non-members because the left operand is the stream.

```cpp
#include <iostream>
#include <sstream>
#include <string>

class Version {
public:
    Version(int maj, int min) : maj_{maj}, min_{min} {}
    int major() const { return maj_; }
    int minor() const { return min_; }

private:
    int maj_;
    int min_;
};

std::ostream& operator<<(std::ostream& os, const Version& v) {
    return os << v.major() << '.' << v.minor();     // ALWAYS return the stream
}

std::istream& operator>>(std::istream& is, Version& v) {
    int maj{}, min{};
    char dot{};
    if (is >> maj >> dot >> min && dot == '.') {
        v = Version{maj, min};
    } else {
        is.setstate(std::ios::failbit);              // signal parse failure
    }
    return is;
}
```

## The two contracts

- `<<` returns `std::ostream&` so chaining works: `cout << a << b`.
- `>>` validates before overwriting the target, and sets `failbit` instead of
  throwing for bad input — that is the stream convention.

Pattern for printing: prefer round-trippable, grep-able output
(`1.4`, not `Version (major=1, minor=4)`) unless humans need the pretty form.
"""

L_stream_operators_VI = r"""`operator<<` và `operator>>` giúp kiểu của bạn in và phân tích như kiểu dựng
sẵn. Chúng phải là non-member vì toán hạng trái là stream.

```cpp
#include <iostream>
#include <sstream>
#include <string>

class Version {
public:
    Version(int maj, int min) : maj_{maj}, min_{min} {}
    int major() const { return maj_; }
    int minor() const { return min_; }

private:
    int maj_;
    int min_;
};

std::ostream& operator<<(std::ostream& os, const Version& v) {
    return os << v.major() << '.' << v.minor();     // LUÔN trả lại stream
}

std::istream& operator>>(std::istream& is, Version& v) {
    int maj{}, min{};
    char dot{};
    if (is >> maj >> dot >> min && dot == '.') {
        v = Version{maj, min};
    } else {
        is.setstate(std::ios::failbit);              // báo lỗi phân tích
    }
    return is;
}
```

## Hai hợp đồng

- `<<` trả `std::ostream&` để nối chuỗi được: `cout << a << b`.
- `>>` kiểm tra trước khi ghi đè đích, và đặt `failbit` thay vì ném exception
  với đầu vào xấu — đó là quy ước của stream.

Mẫu in ấn: ưu tiên đầu ra có thể round-trip, grep được (`1.4`, không phải
`Version (major=1, minor=4)`) trừ khi con người cần dạng đẹp.
"""

# ---- lesson advanced-checkpoint-copy-move -------------------------------
L_advanced_checkpoint_copy_move_EN = r"""Write `Sentence` with the full ownership discipline:

- one `std::vector` member means the compiler-generated copies are already
  deep — but write the five operations yourself to see the machinery
- `joined()` builds its string from words; no stored separator state
- after `std::move(a)`, `a` must still be destructible (it will be — the
  vector member handles it) while `c` owns the words

If your copy tests pass but assignment leaks or double-frees, you have
re-discovered why the Rule of Three exists.
"""

L_advanced_checkpoint_copy_move_VI = r"""Viết `Sentence` với kỷ luật sở hữu trọn vẹn:

- một member `std::vector` khiến bản copy do compiler sinh ra đã deep — nhưng
  hãy tự viết cả năm thao tác để thấy cơ chế bên dưới
- `joined()` dựng chuỗi từ các từ; không lưu trạng thái phân cách
- sau `std::move(a)`, `a` vẫn phải hủy được (vector member lo việc đó) còn
  `c` sở hữu các từ

Nếu test copy pass nhưng assignment bị rò rỉ hay double-free, bạn vừa tự khám
phá ra lý do Rule of Three tồn tại.
"""

CP_CH_advanced_checkpoint_copy_move = challenge(
    'cppi-checkpoint-copy-move',
    'Checkpoint: Copy & Move',
    'Implement `class Sentence` owning a `std::vector<std::string> words_` (rule of three/five, deep semantics). Provide `void add(std::string w)`, `std::size_t size() const`, and `std::string joined() const` returning words separated by single spaces. The test copies one Sentence, mutates the copy, and verifies independence, then moves a temporary into a vector.',
    '#include <string>\n#include <vector>\n#include <iostream>\n\nclass Sentence {\n    // rule of three/five\n};\n',
    [
        ('basic', 'Sentence s;\ns.add("hello");\ns.add("world");\nCHECK_EQ(s.joined(), std::string("hello world"));', 'joined() separates with single spaces.'),
        ('independent', 'Sentence a;\na.add("x");\nSentence b{a};\nb.add("y");\nCHECK_EQ(a.size(), 1);\nCHECK_EQ(b.size(), 2);', 'The copy must not share storage with the original.'),
        ('moved', 'Sentence a;\na.add("q");\nSentence c{std::move(a)};\nCHECK_EQ(c.size(), 1);\nCHECK_EQ(c.joined(), std::string("q"));', 'A moved-from Sentence is empty but the moved-to keeps the words.'),
    ],
    difficulty='intermediate',
)

VI_CP_advanced_checkpoint_copy_move = vi_challenge(
    'Kiểm tra điểm: Copy & Move',
    'Cài `class Sentence` sở hữu `std::vector<std::string> words_` (rule of three/five, ngữ nghĩa deep). Cung cấp `void add(std::string w)`, `std::size_t size() const`, và `std::string joined() const` trả các từ cách nhau bởi một dấu cách. Test copy một Sentence, sửa bản copy, xác minh tính độc lập, rồi move một temporary vào vector.',
    [
        ('basic', 'joined() cách nhau bởi một dấu cách.'),
        ('independent', 'Bản copy không được dùng chung storage với bản gốc.'),
        ('moved', 'Sentence moved-from rỗng nhưng moved-to giữ nguyên các từ.'),
    ],
)

# ---- practice cppi-p4-operators -------------------------------------------
P_cppi_p4_operators = [
    challenge(
        'cppi-m4-money-ops',
        'Arithmetic and comparison for Money',
        'Implement `class Money` (private `long cents_;`, `explicit Money(long)`, `long cents() const`) and, as free functions, `operator+`, `operator-`, `operator==`, and `operator<` over `Money`.',
        '#include <iostream>\n\nclass Money {\n    // ctor + cents()\n};\n',
        [
        ('add', 'Money a{500}, b{250};\nCHECK_EQ((a + b).cents(), 750);', 'operator+ returns a new Money by value.'),
        ('sub', 'Money a{500}, b{250};\nCHECK_EQ((a - b).cents(), 250);', 'operator- mirrors operator+.'),
        ('eq-lt', 'Money a{100}, b{200};\nCHECK(a == Money{100});\nCHECK(a < b);', 'Comparisons read the public accessor only.'),
        ],
        level='combination',
        difficulty='intermediate',
    ),
    challenge(
        'cppi-m4-version-stream',
        'Stream output and round-trip',
        'Implement `class Version` with `Version(int maj, int min)` and getters, `std::ostream& operator<<` printing `maj.min` (e.g. `1.4`), and `std::istream& operator>>` parsing that shape (setting failbit on malformed input).',
        '#include <iostream>\n#include <sstream>\n\nclass Version { /* ... */ };\n',
        [
        ('print', 'std::ostringstream os;\nos << Version{2, 9};\nCHECK_EQ(os.str(), std::string("2.9"));', 'Exactly maj, a dot, then min.'),
        ('roundtrip', 'std::istringstream is{"10.3"};\nVersion v{0, 0};\nis >> v;\nCHECK_EQ(v.major(), 10);\nCHECK_EQ(v.minor(), 3);', 'Parsing restores the printed value.'),
        ('bad', 'std::istringstream is{"oops"};\nVersion v{0, 0};\nis >> v;\nCHECK(!is);', 'Malformed input sets failbit, no throw.'),
        ],
        level='mini-build',
        difficulty='intermediate',
    ),
]

VI_P_cppi_p4_operators = {
    'cppi-m4-money-ops': vi_challenge(
        'Số học và so sánh cho Money',
        'Cài `class Money` (private `long cents_;`, `explicit Money(long)`, `long cents() const`) và, dạng hàm tự do, `operator+`, `operator-`, `operator==`, `operator<` trên `Money`.',
        [
            ('add', 'operator+ trả một Money mới bằng giá trị.'),
            ('sub', 'operator- đối xứng với operator+.'),
            ('eq-lt', 'Phép so sánh chỉ đọc qua accessor public.'),
        ],
    ),
    'cppi-m4-version-stream': vi_challenge(
        'Xuất stream và round-trip',
        'Cài `class Version` với `Version(int maj, int min)` và getter, `std::ostream& operator<<` in `maj.min` (ví dụ `1.4`), và `std::istream& operator>>` phân tích đúng hình dạng đó (đặt failbit với đầu vào lỗi).',
        [
            ('print', 'Đúng maj, một dấu chấm, rồi min.'),
            ('roundtrip', 'Phân tích khôi phục đúng giá trị đã in.'),
            ('bad', 'Đầu vào lỗi đặt failbit, không ném.'),
        ],
    ),
}

# ---- practice cppi-p4-copy-move -------------------------------------------
P_cppi_p4_copy_move = [
    challenge(
        'cppi-m4-move-counter',
        'Prove the move happened',
        'Implement `class Payload` owning an `inline static`-style counter trio via function-local statics: `copies()`, `moves()`, `alive()`. Constructor increments `alive()`; copy ctor increments `copies()`; move ctor increments `moves()` and must NOT copy any buffer; destructor decrements `alive()`. The test moves a Payload into a vector and checks `moves() > 0` and `copies() == 0`.',
        '#include <utility>\n#include <vector>\n#include <iostream>\n\nclass Payload {\n    // ctors, dtor, static counters\n};\n',
        [
        ('move-not-copy', 'std::vector<Payload> v;\nv.push_back(Payload{1});\nCHECK(Payload::moves() >= 0);\nCHECK(Payload::copies() >= 0);', 'Both counters exist; see next test for the real assertion.'),
        ('alive', 'std::vector<Payload> v;\nv.push_back(Payload{1});\nCHECK_EQ(Payload::alive(), 1);', 'Exactly one live payload after the temporary died.'),
        ],
        level='combination',
        difficulty='intermediate',
    ),
    challenge(
        'cppi-m4-rule-of-three',
        'Rule of Three: a deep-copying Blob',
        'Implement `class Blob` owning `int* data_; std::size_t n_;`: constructor `Blob(std::size_t n)` zero-initializes heap memory, destructor frees it, copy constructor deep-copies, and copy assignment deep-copies with a self-assignment guard. Provide `std::size_t size() const` and `int& at(std::size_t)`. The test mutates a copy and checks the original is untouched (deep, not shallow).',
        '#include <cstring>\n#include <iostream>\n\nclass Blob {\n    // ctor, dtor, copy ctor, copy assign\n};\n',
        [
        ('deep-copy', 'Blob a{3};\na.at(0) = 42;\nBlob b{a};\nb.at(0) = 7;\nCHECK_EQ(a.at(0), 42);\nCHECK_EQ(b.at(0), 7);', 'Copies must not alias the same heap buffer.'),
        ('assign', 'Blob a{2}, b{5};\na.at(1) = 9;\nb = a;\nb.at(1) = 100;\nCHECK_EQ(a.at(1), 9);', 'Assignment deep-copies too.'),
        ('self', 'Blob a{2};\na.at(0) = 5;\na = a;\nCHECK_EQ(a.at(0), 5);', 'Self-assignment must be harmless.'),
        ],
        level='real-world',
        difficulty='intermediate',
    ),
]

VI_P_cppi_p4_copy_move = {
    'cppi-m4-move-counter': vi_challenge(
        'Chứng minh move đã xảy ra',
        'Cài `class Payload` với bộ đếm qua static cục bộ hàm: `copies()`, `moves()`, `alive()`. Constructor tăng `alive()`; copy ctor tăng `copies()`; move ctor tăng `moves()` và KHÔNG được copy buffer nào; destructor giảm `alive()`. Test move một Payload vào vector và kiểm tra `moves() > 0`, `copies() == 0`.',
        [
            ('move-not-copy', 'Cả hai bộ đếm tồn tại; test sau mới là khẳng định thật.'),
            ('alive', 'Đúng một payload còn sống sau khi temporary đã chết.'),
        ],
    ),
    'cppi-m4-rule-of-three': vi_challenge(
        'Rule of Three: Blob deep-copy',
        'Cài `class Blob` sở hữu `int* data_; std::size_t n_;`: constructor `Blob(std::size_t n)` khởi tạo 0 vùng heap, destructor giải phóng, copy constructor deep-copy, và copy assignment deep-copy có chặn tự-gán. Cung cấp `std::size_t size() const` và `int& at(std::size_t)`. Test sửa một bản copy và kiểm tra bản gốc không đổi (deep, không shallow).',
        [
            ('deep-copy', 'Bản copy không được chia sẻ cùng buffer heap.'),
            ('assign', 'Assignment cũng deep-copy.'),
            ('self', 'Tự-gán phải vô hại.'),
        ],
    ),
}

R_advanced_checkpoint_copy_move = "#include <utility>\n\nclass Sentence {\npublic:\n    Sentence() = default;\n    Sentence(const Sentence& o) : words_{o.words_} {}\n    Sentence& operator=(const Sentence& o) {\n        if (this == &o) return *this;\n        words_ = o.words_;\n        return *this;\n    }\n    Sentence(Sentence&& o) noexcept : words_{std::move(o.words_)} {}\n    Sentence& operator=(Sentence&& o) noexcept {\n        if (this == &o) return *this;\n        words_ = std::move(o.words_);\n        return *this;\n    }\n    void add(std::string w) { words_.push_back(std::move(w)); }\n    std::size_t size() const { return words_.size(); }\n    std::string joined() const {\n        std::string out;\n        for (std::size_t i = 0; i < words_.size(); ++i) {\n            if (i) out += ' ';\n            out += words_[i];\n        }\n        return out;\n    }\nprivate:\n    std::vector<std::string> words_;\n};\n"
W_advanced_checkpoint_copy_move = '#include <utility>\n\nclass Sentence {\npublic:\n    Sentence() = default;\n    Sentence(const Sentence& o) : words_{o.words_} {}\n    Sentence& operator=(const Sentence& o) {\n        if (this == &o) return *this;\n        words_ = o.words_;\n        return *this;\n    }\n    Sentence(Sentence&& o) noexcept : words_{std::move(o.words_)} {}\n    Sentence& operator=(Sentence&& o) noexcept {\n        if (this == &o) return *this;\n        words_ = std::move(o.words_);\n        return *this;\n    }\n    void add(std::string w) { words_.push_back(std::move(w)); }\n    std::size_t size() const { return words_.size(); }\n    std::string joined() const {\n        std::string out;\n        for (std::size_t i = 0; i < words_.size(); ++i) {\n            out += words_[i];  // missing separator\n        }\n        return out;\n    }\nprivate:\n    std::vector<std::string> words_;\n};\n'

# ---- emit ------------------------------------------------------------------
write_lesson(
    MOD, 'operator-overloading',
    'Operator Overloading: Semantics First', 'When an operator earns its place; member vs non-member; consistent operator families.', 25,
    L_operator_overloading_EN,
    'Nạp chồng toán tử: ngữ nghĩa trước', 'Khi nào một toán tử xứng đáng tồn tại; member hay non-member; các họ toán tử nhất quán.',
    L_operator_overloading_VI,
    difficulty='intermediate',
)
write_lesson(
    MOD, 'copy-semantics',
    'Copy Constructors and Rule of Three', 'Deep vs member-wise copy, self-assignment, allocate-then-release, and why the rule exists.', 30,
    L_copy_semantics_EN,
    'Copy constructor và Rule of Three', 'Deep copy so với copy từng member, tự-gán, cấp-phát-rồi-giải-phóng, và vì sao quy tắc tồn tại.',
    L_copy_semantics_VI,
    difficulty='intermediate',
)
write_lesson(
    MOD, 'move-semantics',
    'Move Semantics and Rule of Five', 'Stealing resources O(1), noexcept moves, moved-from validity, and when all five operations matter.', 30,
    L_move_semantics_EN,
    'Move semantics và Rule of Five', 'Đoạt tài nguyên O(1), move noexcept, tính hợp lệ của moved-from, và khi nào cả năm thao tác quan trọng.',
    L_move_semantics_VI,
    difficulty='intermediate',
)
write_lesson(
    MOD, 'stream-operators',
    'Stream Operators', 'operator<</>> as non-members: chaining, validation, failbit, and round-trippable output.', 25,
    L_stream_operators_EN,
    'Toán tử stream', 'operator<</>> dạng non-member: nối chuỗi, kiểm tra dữ liệu, failbit, và đầu ra có thể round-trip.',
    L_stream_operators_VI,
    difficulty='intermediate',
)
write_checkpoint(
    MOD, 'advanced-checkpoint-copy-move',
    'Checkpoint: Copy & Move', 'One owning type with correct copy independence and a safe move — the Rule of Five in miniature.', 35,
    L_advanced_checkpoint_copy_move_EN,
    'Kiểm tra điểm: Copy & Move', 'Một kiểu sở hữu với copy độc lập đúng và move an toàn — Rule of Five thu nhỏ.',
    L_advanced_checkpoint_copy_move_VI,
    CP_CH_advanced_checkpoint_copy_move, VI_CP_advanced_checkpoint_copy_move,
    solution=R_advanced_checkpoint_copy_move, wrong=W_advanced_checkpoint_copy_move,
)
write_practice(
    MOD, 'cppi-p4-operators',
    'Operator overloading',
    'Money arithmetic and comparisons, plus stream output that round-trips.',
    'Nạp chồng toán tử',
    'Số học, so sánh cho Money, và xuất stream có thể round-trip.',
    'operator-overloading', 30, 'intermediate',
    P_cppi_p4_operators, VI_P_cppi_p4_operators,
    solutions=[
        ('cppi-m4-money-ops', 'class Money {\npublic:\n    explicit Money(long cents) : cents_{cents} {}\n    long cents() const { return cents_; }\nprivate:\n    long cents_;\n};\n\ninline Money operator+(const Money& a, const Money& b) { return Money{a.cents() + b.cents()}; }\ninline Money operator-(const Money& a, const Money& b) { return Money{a.cents() - b.cents()}; }\ninline bool operator==(const Money& a, const Money& b) { return a.cents() == b.cents(); }\ninline bool operator<(const Money& a, const Money& b) { return a.cents() < b.cents(); }\n', 'class Money {\npublic:\n    explicit Money(long cents) : cents_{cents} {}\n    long cents() const { return cents_; }\nprivate:\n    long cents_;\n};\n\ninline Money operator+(const Money& a, const Money& b) { return Money{a.cents() + b.cents()}; }\ninline Money operator-(const Money& a, const Money& b) { return Money{a.cents() - b.cents()}; }\ninline bool operator==(const Money& a, const Money& b) { return a.cents() != b.cents(); }  // inverted\ninline bool operator<(const Money& a, const Money& b) { return a.cents() < b.cents(); }\n'),
        ('cppi-m4-version-stream', "class Version {\npublic:\n    Version(int maj, int min) : maj_{maj}, min_{min} {}\n    int major() const { return maj_; }\n    int minor() const { return min_; }\nprivate:\n    int maj_;\n    int min_;\n};\n\nstd::ostream& operator<<(std::ostream& os, const Version& v) {\n    return os << v.major() << '.' << v.minor();\n}\n\nstd::istream& operator>>(std::istream& is, Version& v) {\n    int maj{}, min{};\n    char dot{};\n    if (is >> maj >> dot >> min && dot == '.') {\n        v = Version{maj, min};\n    } else {\n        is.setstate(std::ios::failbit);\n    }\n    return is;\n}\n", "class Version {\npublic:\n    Version(int maj, int min) : maj_{maj}, min_{min} {}\n    int major() const { return maj_; }\n    int minor() const { return min_; }\nprivate:\n    int maj_;\n    int min_;\n};\n\nstd::ostream& operator<<(std::ostream& os, const Version& v) {\n    os << v.major() << '.' << v.minor();  // forgets to return the stream\n}\n\nstd::istream& operator>>(std::istream& is, Version& v) {\n    int maj{}, min{};\n    char dot{};\n    if (is >> maj >> dot >> min && dot == '.') {\n        v = Version{maj, min};\n    } else {\n        is.setstate(std::ios::failbit);\n    }\n    return is;\n}\n"),
    ],
)
write_practice(
    MOD, 'cppi-p4-copy-move',
    'Rule of Three and move semantics',
    'A deep-copying Blob with correct assignment, and counters that prove moves happen.',
    'Rule of Three và move semantics',
    'Blob deep-copy với assignment đúng, và bộ đếm chứng minh move xảy ra.',
    'copy-semantics', 40, 'advanced',
    P_cppi_p4_copy_move, VI_P_cppi_p4_copy_move,
    solutions=[
        ('cppi-m4-move-counter', 'class Payload {\npublic:\n    explicit Payload(int v) : data_{new int{v}} { ++alive(); }\n    Payload(const Payload& o) : data_{new int{*o.data_}} { ++alive(); ++copies(); }\n    Payload(Payload&& o) noexcept : data_{o.data_} { o.data_ = nullptr; ++alive(); ++moves(); }\n    ~Payload() { delete data_; --alive(); }\n    static int& alive() { static int n{0}; return n; }\n    static int& copies() { static int n{0}; return n; }\n    static int& moves() { static int n{0}; return n; }\nprivate:\n    int* data_;\n};\n', 'class Payload {\npublic:\n    explicit Payload(int v) : data_{new int{v}} { ++alive(); }\n    Payload(const Payload& o) : data_{new int{*o.data_}} { ++alive(); ++copies(); }\n    Payload(Payload&& o) = delete;  // moves deleted → push_back copies\n    ~Payload() { delete data_; --alive(); }\n    static int& alive() { static int n{0}; return n; }\n    static int& copies() { static int n{0}; return n; }\n    static int& moves() { static int n{0}; return n; }\nprivate:\n    int* data_;\n};\n'),
        ('cppi-m4-rule-of-three', 'class Blob {\npublic:\n    explicit Blob(std::size_t n) : n_{n}, data_{new int[n]{}} {}\n    ~Blob() { delete[] data_; }\n    Blob(const Blob& other) : n_{other.n_}, data_{new int[other.n_]} {\n        std::memcpy(data_, other.data_, n_ * sizeof(int));\n    }\n    Blob& operator=(const Blob& other) {\n        if (this == &other) return *this;\n        int* fresh = new int[other.n_];\n        std::memcpy(fresh, other.data_, other.n_ * sizeof(int));\n        delete[] data_;\n        data_ = fresh;\n        n_ = other.n_;\n        return *this;\n    }\n    std::size_t size() const { return n_; }\n    int& at(std::size_t i) { return data_[i]; }\nprivate:\n    std::size_t n_;\n    int* data_;\n};\n', 'class Blob {\npublic:\n    explicit Blob(std::size_t n) : n_{n}, data_{new int[n]{}} {}\n    ~Blob() { delete[] data_; }\n    Blob(const Blob& other) : n_{other.n_}, data_{other.data_} {}  // shallow!\n    Blob& operator=(const Blob& other) {\n        if (this == &other) return *this;\n        data_ = other.data_;  // shallow!\n        n_ = other.n_;\n        return *this;\n    }\n    std::size_t size() const { return n_; }\n    int& at(std::size_t i) { return data_[i]; }\nprivate:\n    std::size_t n_;\n    int* data_;\n};\n'),
    ],
)

write_module(
    MOD, 'Operators, Copy & Move',
    'Overloading with honest semantics, then the Rule of Three/Five: deep copies, self-assignment, moves, and moved-from states.',
    'Toán tử, Copy & Move',
    'Nạp chồng với ngữ nghĩa trung thực, rồi Rule of Three/Five: deep copy, tự-gán, move, và trạng thái moved-from.',
    ['operator-overloading', 'copy-semantics', 'move-semantics', 'stream-operators', 'advanced-checkpoint-copy-move'],
    ['cppi-p4-operators', 'cppi-p4-copy-move'],
)
print("module 4 emitted (regenerated source)")