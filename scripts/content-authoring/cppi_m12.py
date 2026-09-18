#!/usr/bin/env python3
"""C++ Intermediate — Module 12: final-project.

The capstone: a small library-manager CLI assembled from every module —
classes (M2-4), STL (M5), algorithms+functions (M6), modern C++ (M7),
RAII/ownership (M8), templates (M9), errors (M10), and DS&A thinking (M11).
Grading stays deterministic: persistence is modeled over strings and
in-memory state.

Authoring discipline: every C++ code string is a raw triple-quoted string.
Snippets are self-contained per translation unit.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "cppi-final-project"

# ---- lesson project-architecture ------------------------------------------------
L_architecture_EN = r"""
Before writing a line: the shape of the thing you are building. A small
library manager with four responsibilities, each in its own class:

```
┌─────────────────────────────────────────────┐
│  App            — the CLI loop (menu, I/O)  │
│    │ owned by unique_ptr                        │
│  Library        — the rules (add, borrow)   │
│    │ owns                                       │
│  vector<Book>   — the state (records)       │
│    └ serialized to                             │
│  string content — the persistence (M10)     │
└─────────────────────────────────────────────┘
```

Three architecture decisions worth making consciously:

1. **The App knows menus; the Library knows rules.** The app loop parses
   input and prints; it never edits the book vector directly. When you
   later swap a CLI for a GUI, the Library survives untouched.
2. **State is one collection, not five globals.** A `Library` owns a
   `std::vector<Book>`; nothing else touches it. Modules 2-4 gave you the
   class, Module 8 the ownership vocabulary for who holds it.
3. **Persistence is a boundary, not a sprinkle.** Exactly two functions
   (`serialize`, `deserialize`) convert between records and text. Module
   10's parsing discipline lives *here*, and nowhere else.

This layering is a miniature of real systems: presentation, domain,
storage. The names change; the seams do not.
"""

L_architecture_VI = r"""
Trước khi viết một dòng: hình dạng của thứ bạn sắp xây. Một trình quản lý
thư viện nhỏ với bốn trách nhiệm, mỗi trách nhiệm một lớp riêng:

```
┌─────────────────────────────────────────────┐
│  App            — vòng lặp CLI (menu, I/O)  │
│    │ được sở hữu bởi unique_ptr               │
│  Library        — luật chơi (thêm, mượn)    │
│    │ sở hữu                                     │
│  vector<Book>   — trạng thái (bản ghi)      │
│    └ serialize thành                           │
│  string content — lưu trữ (M10)             │
└─────────────────────────────────────────────┘
```

Ba quyết định kiến trúc đáng làm một cách có ý thức:

1. **App biết menu; Library biết luật.** Vòng lặp app phân tích input và
   in kết quả; nó không bao giờ sửa trực tiếp vector sách. Khi sau này
   bạn thay CLI bằng GUI, Library vẫn nguyên vẹn.
2. **Trạng thái là một collection, không phải năm biến toàn cục.** Một
   `Library` sở hữu `std::vector<Book>`; không ai khác đụng vào nó.
   Module 2-4 cho bạn lớp, Module 8 cho từ vựng sở hữu cho ai giữ nó.
3. **Lưu trữ là một biên giới, không phải rắc rắc khắp nơi.** Đúng hai
   hàm (`serialize`, `deserialize`) chuyển đổi giữa bản ghi và văn bản.
   Kỷ luật phân tích của Module 10 sống *ở đây*, và chỉ ở đây.
"""

# ---- lesson integration -------------------------------------------------------------
L_integration_EN = r"""
The capstone exercises every module. Where each one shows up:

| Module | Shows up as |
|---|---|
| M2-M4 classes | `Book`, `Library` with encapsulation, `const` correctness |
| M5 STL | `std::vector<Book>` storage, `std::map` for counts |
| M6 algorithms | `std::sort` the listing, `std::find_if` the search |
| M7 modern | `std::optional` for lookups, `enum class` Status |
| M8 RAII | ownership discipline if you hold resources |
| M9 templates | a generic `format_table` helper if you generalize |
| M10 errors | `ValidationError` carrying field data |
| M11 DSA | complexity awareness for search choices |

The integration lesson: **each seam is a place you already practiced.**
When the compiler complains, you now know which module's lesson to reread.

A worked skeleton to extend — search with `optional` + `find_if`:

```cpp
#include <algorithm>
#include <optional>
#include <vector>

class Library {
public:
    std::optional<const Book*> find(std::string_view title) const {
        auto it = std::find_if(books_.begin(), books_.end(),
                               [&](const Book& b) { return b.title() == title; });
        if (it == books_.end()) return std::nullopt;
        return &*it;
    }
private:
    std::vector<Book> books_;
};
```

Every piece is review; the composition is the new skill.
"""

L_integration_VI = r"""
Bài capstone exercised mọi module. Mỗi module xuất hiện ở đâu:

| Module | Xuất hiện dưới dạng |
|---|---|
| M2-M4 lớp | `Book`, `Library` với encapsulation, `const` correctness |
| M5 STL | `std::vector<Book>` lưu trữ, `std::map` cho bộ đếm |
| M6 thuật toán | `std::sort` danh sách, `std::find_if` tìm kiếm |
| M7 hiện đại | `std::optional` cho tra cứu, `enum class` Status |
| M8 RAII | kỷ luật sở hữu nếu bạn giữ tài nguyên |
| M9 template | một helper `format_table` generic nếu bạn tổng quát hóa |
| M10 lỗi | `ValidationError` mang dữ liệu theo field |
| M11 DSA | ý thức độ phức tạp khi chọn cách tìm kiếm |

Bài học tích hợp: **mỗi đường nối là một nơi bạn đã luyện.** Khi compiler
kêu than, giờ đây bạn biết phải đọc lại bài học của module nào.

Một khung mẫu để mở rộng — tìm kiếm với `optional` + `find_if`:

```cpp
#include <algorithm>
#include <optional>
#include <vector>

class Library {
public:
    std::optional<const Book*> find(std::string_view title) const {
        auto it = std::find_if(books_.begin(), books_.end(),
                               [&](const Book& b) { return b.title() == title; });
        if (it == books_.end()) return std::nullopt;
        return &*it;
    }
private:
    std::vector<Book> books_;
};
```

Mọi mảnh đều là ôn tập; việc ghép chúng mới là kỹ năng mới.
"""

# ---- lesson ship-it --------------------------------------------------------------------
L_ship_EN = r"""
You have built programs all course; the final module is about finishing
one. "Finishing" has a checklist:

1. **Requirements are testable.** Each capability has a concrete scenario:
   "adding a duplicate ISBN updates the quantity" — not "handles input".
2. **Errors are designed, not accidental.** Every failure the user can
   cause has a chosen channel: return `nullopt`, throw `ValidationError`,
   or print a message. Pick per case; document with the signature.
3. **The happy path is boring.** Read the main loop: if it is more than
   parse → dispatch → print, responsibilities leaked upward.
4. **State survives restart.** Serialize on change, deserialize on start;
   corrupt input degrades to "start empty" with a warning — never a crash.
5. **You can explain every file.** The final review is verbal: point at a
   line and say which decision it implements. If you cannot, that line is
   either unnecessary or undesigned.

The graded challenges below are the three seams learners most often get
wrong: the borrow/return state machine, the persistence round-trip, and
the validation boundary. Each is small; each is where "almost working"
programs actually break.
"""

L_ship_VI = r"""
Bạn đã dựng chương trình suốt khóa học; module cuối là về việc *hoàn thành*
một chương trình. "Hoàn thành" có checklist riêng:

1. **Yêu cầu phải kiểm thử được.** Mỗi tính năng có một kịch bản cụ thể:
   "thêm ISBN trùng sẽ cập nhật số lượng" — không phải "xử lý input".
2. **Lỗi được thiết kế, không phải ngẫu nhiên.** Mỗi lỗi user có thể gây
   ra có một kênh được chọn: trả `nullopt`, ném `ValidationError`, hoặc
   in thông báo. Chọn theo từng trường hợp; ghi rõ qua chữ ký hàm.
3. **Đường vui phải nhàm chán.** Đọc vòng lặp chính: nếu nhiều hơn
   parse → điều phối → in, thì trách nhiệm đã rò rỉ lên trên.
4. **Trạng thái sống sót qua lần khởi động lại.** Serialize khi thay đổi,
   deserialize khi khởi động; input hỏng suy giảm thành "bắt đầu rỗng"
   kèm cảnh báo — không bao giờ crash.
5. **Bạn giải thích được từng dòng.** Buổi review cuối là nói: chỉ vào
   một dòng và nói nó cài quyết định nào. Nếu không nói được, dòng đó
   hoặc là thừa, hoặc là chưa thiết kế.

Các bài chấm điểm dưới đây là ba đường nối mà người học hay sai nhất:
state machine mượn/trả, vòng round-trip lưu trữ, và biên giới kiểm tra
dữ liệu. Mỗi cái đều nhỏ; mỗi cái đều là nơi các chương trình "gần chạy"
thực sự gãy.
"""

# ---- practice: the three graded seams ---------------------------------------------------
R_BORROW = r'''#include <string>
#include <vector>

enum class BookState { Available, Borrowed };

class BorrowTracker {
public:
    bool borrow(const std::string& isbn) {
        auto& slot = state(isbn);
        if (slot == BookState::Borrowed) return false;
        slot = BookState::Borrowed;
        return true;
    }

    bool give_back(const std::string& isbn) {
        auto& slot = state(isbn);
        if (slot == BookState::Available) return false;
        slot = BookState::Available;
        return true;
    }

    bool is_borrowed(const std::string& isbn) const {
        for (const auto& [id, st] : states_)
            if (id == isbn) return st == BookState::Borrowed;
        return false;   // unknown book: not borrowed
    }

private:
    std::vector<std::pair<std::string, BookState>> states_;

    BookState& state(const std::string& isbn) {
        for (auto& [id, st] : states_)
            if (id == isbn) return st;
        states_.emplace_back(isbn, BookState::Available);
        return states_.back().second;
    }
};
'''

W_BORROW = r'''#include <string>
#include <vector>

enum class BookState { Available, Borrowed };

class BorrowTracker {
public:
    bool borrow(const std::string& isbn) {
        auto& slot = state(isbn);
        // BUG: does not check current state — double-borrow succeeds
        slot = BookState::Borrowed;
        return true;
    }

    bool give_back(const std::string& isbn) {
        auto& slot = state(isbn);
        if (slot == BookState::Available) return false;
        slot = BookState::Available;
        return true;
    }

    bool is_borrowed(const std::string& isbn) const {
        for (const auto& [id, st] : states_)
            if (id == isbn) return st == BookState::Borrowed;
        return false;
    }

private:
    std::vector<std::pair<std::string, BookState>> states_;

    BookState& state(const std::string& isbn) {
        for (auto& [id, st] : states_)
            if (id == isbn) return st;
        states_.emplace_back(isbn, BookState::Available);
        return states_.back().second;
    }
};
'''

R_ROUNDTRIP = r'''#include <sstream>
#include <string>
#include <vector>

struct Book {
    std::string title;
    int quantity;
};

std::string serialize(const std::vector<Book>& books) {
    std::string out;
    for (const auto& b : books) {
        out += b.title;
        out += '|';
        out += std::to_string(b.quantity);
        out += '\n';
    }
    return out;
}

std::vector<Book> deserialize(const std::string& content) {
    std::vector<Book> out;
    std::istringstream in{content};
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        auto sep = line.rfind('|');
        if (sep == std::string::npos) continue;
        try {
            Book b;
            b.title = line.substr(0, sep);
            b.quantity = std::stoi(line.substr(sep + 1));
            out.push_back(std::move(b));
        } catch (const std::exception&) {
            // corrupt line: skip
        }
    }
    return out;
}
'''

W_ROUNDTRIP = r'''#include <sstream>
#include <string>
#include <vector>

struct Book {
    std::string title;
    int quantity;
};

std::string serialize(const std::vector<Book>& books) {
    std::string out;
    for (const auto& b : books) {
        out += b.title;
        out += '|';
        out += std::to_string(b.quantity);
        out += '\n';
    }
    return out;
}

std::vector<Book> deserialize(const std::string& content) {
    std::vector<Book> out;
    std::istringstream in{content};
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        auto sep = line.rfind('|');
        if (sep == std::string::npos) continue;
        try {
            Book b;
            b.title = line.substr(0, sep);
            b.quantity = std::stoi(line.substr(sep + 1));
            out.push_back(std::move(b));
        } catch (const std::exception&) {
            // BUG: a corrupt line aborts the whole load
            throw;
        }
    }
    return out;
}
'''

R_VALIDATE = r'''#include <optional>
#include <string>
#include <vector>

struct NewBook {
    std::string title;
    int quantity;
};

enum class AddError { EmptyTitle, BadQuantity, Duplicate };

class Catalog {
public:
    explicit Catalog(std::vector<std::string> titles) : titles_{std::move(titles)} {}

    std::optional<AddError> validate(const NewBook& b) const {
        if (b.title.empty()) return AddError::EmptyTitle;
        if (b.quantity <= 0) return AddError::BadQuantity;
        for (const auto& t : titles_)
            if (t == b.title) return AddError::Duplicate;
        return std::nullopt;
    }

private:
    std::vector<std::string> titles_;
};
'''

W_VALIDATE = r'''#include <optional>
#include <string>
#include <vector>

struct NewBook {
    std::string title;
    int quantity;
};

enum class AddError { EmptyTitle, BadQuantity, Duplicate };

class Catalog {
public:
    explicit Catalog(std::vector<std::string> titles) : titles_{std::move(titles)} {}

    std::optional<AddError> validate(const NewBook& b) const {
        // BUG: checks quantity before emptiness — wrong error for "" with qty 0
        if (b.quantity <= 0) return AddError::BadQuantity;
        if (b.title.empty()) return AddError::EmptyTitle;
        for (const auto& t : titles_)
            if (t == b.title) return AddError::Duplicate;
        return std::nullopt;
    }

private:
    std::vector<std::string> titles_;
};
'''

# ---- challenges --------------------------------------------------------------------------
CH_BORROW = challenge(
    "cppi-m12-borrow-state",
    "Capstone seam 1: the borrow state machine",
    "Complete `BorrowTracker`: `bool borrow(const std::string& isbn)` moves an available (or unknown) book to Borrowed and returns true — but returns false and changes nothing if it is already Borrowed. `bool give_back(...)` is the mirror for returning. `bool is_borrowed(...) const` reports state; unknown books are not borrowed.",
    r'''#include <string>
#include <vector>
#include <iostream>

enum class BookState { Available, Borrowed };

// Complete class BorrowTracker { borrow, give_back, is_borrowed }
''',
    [
        ("happy-path", 'BorrowTracker t;\nCHECK_EQ(t.borrow("111"), true);\nCHECK_EQ(t.is_borrowed("111"), true);\nCHECK_EQ(t.give_back("111"), true);\nCHECK_EQ(t.is_borrowed("111"), false);', "Borrow flips Available→Borrowed; give_back flips it back."),
        ("double-borrow", 'BorrowTracker t;\nCHECK_EQ(t.borrow("222"), true);\nCHECK_EQ(t.borrow("222"), false);\nCHECK_EQ(t.is_borrowed("222"), true);', "The second borrow must be refused, not silently succeed."),
        ("return-unknown", 'BorrowTracker t;\nCHECK_EQ(t.give_back("ghost"), false);', "Returning a book never borrowed is refused."),
    ],
    level="combination",
)

CH_ROUNDTRIP = challenge(
    "cppi-m12-persistence",
    "Capstone seam 2: persistence round-trip",
    "Implement the pair `std::string serialize(const std::vector<Book>&)` and `std::vector<Book> deserialize(const std::string&)` with the record format `title|quantity` per line. `deserialize` skips blank lines, skips lines without `|`, and skips lines whose quantity is not a valid integer — one bad line never aborts the load. `Book` is `{std::string title; int quantity;}`.",
    r'''#include <sstream>
#include <string>
#include <vector>
#include <iostream>

struct Book {
    std::string title;
    int quantity;
};

// std::string serialize(const std::vector<Book>& books)
// std::vector<Book> deserialize(const std::string& content)
''',
    [
        ("roundtrip", 'std::vector<Book> books{{"C++ Primer", 3}, {"Effective Modern C++", 1}};\nauto restored = deserialize(serialize(books));\nCHECK_EQ(restored.size(), 2);\nCHECK_EQ(restored[0].title, std::string("C++ Primer"));\nCHECK_EQ(restored[0].quantity, 3);\nCHECK_EQ(restored[1].quantity, 1);', "Serialize → deserialize must reproduce every record."),
        ("corrupt-lines", 'auto restored = deserialize(std::string{"good:2\\nbroken\\nX|notanumber\\nlast|5\\n"});\nCHECK_EQ(restored.size(), 1);\nCHECK_EQ(restored[0].title, std::string("last"));\nCHECK_EQ(restored[0].quantity, 5);', "No '|' → skip; non-numeric quantity → skip. Only `last|5` survives."),
        ("empty-content", 'CHECK(deserialize(std::string{""}).empty());', "Empty file loads as an empty library."),
    ],
    level="real-world",
)

CH_VALIDATE = challenge(
    "cppi-m12-validation",
    "Capstone seam 3: the validation boundary",
    "Complete `Catalog::validate(const NewBook&) const` returning `std::optional<AddError>`: `EmptyTitle` for an empty title, `BadQuantity` for quantity <= 0, `Duplicate` when the title already exists in the catalog, and `std::nullopt` when the book may be added. Check in that order — a test feeds an empty title with quantity 0 and expects EmptyTitle.",
    r'''#include <optional>
#include <string>
#include <vector>
#include <iostream>

struct NewBook {
    std::string title;
    int quantity;
};

enum class AddError { EmptyTitle, BadQuantity, Duplicate };

// Complete class Catalog { validate }
''',
    [
        ("order-matters", 'Catalog c{std::vector<std::string>{"existing"}};\nauto e = c.validate(NewBook{"", 0});\nCHECK(e.has_value());\nCHECK(e.value() == AddError::EmptyTitle);', "Empty title wins over bad quantity — order is the contract."),
        ("duplicate", 'Catalog c{std::vector<std::string>{"existing"}};\nauto e = c.validate(NewBook{"existing", 1});\nCHECK(e.has_value());\nCHECK(e.value() == AddError::Duplicate);', "Existing titles are refused."),
        ("valid", 'Catalog c{std::vector<std::string>{"a"}};\nCHECK(!c.validate(NewBook{"fresh", 2}).has_value());', "A clean book yields nullopt — nothing blocks the add."),
    ],
    level="independent",
)

# ---- final checkpoint ---------------------------------------------------------------------
CP_CAPSTONE = challenge(
    "cppi-checkpoint-capstone",
    "Checkpoint: Library, assembled",
    "Assemble the capstone core: `class Library` holding `std::vector<Book>` with `void add(const Book&)`, `std::optional<const Book*> find(const std::string& title) const`, `std::size_t size() const`, and `std::string inventory() const` — a listing of `title|quantity` lines in insertion order (one per book, each ending with \\n; empty library yields an empty string). `Book` is `{std::string title; int quantity;}`.",
    r'''#include <optional>
#include <string>
#include <vector>
#include <iostream>

struct Book {
    std::string title;
    int quantity;
};

// Complete class Library { add, find, size, inventory }
''',
    [
        ("add-find", 'Library lib;\nlib.add(Book{"Clean Code", 2});\nCHECK_EQ(lib.size(), 1);\nauto f = lib.find("Clean Code");\nCHECK(f.has_value());\nCHECK_EQ((*f)->quantity, 2);\nCHECK(!lib.find("Ghost").has_value());', "add stores; find returns a pointer to the live book or nullopt."),
        ("inventory-format", 'Library lib;\nlib.add(Book{"A", 1});\nlib.add(Book{"B", 3});\nCHECK_EQ(lib.inventory(), std::string("A|1\\nB|3\\n"));', "Insertion order, `title|quantity`, one line each."),
        ("empty-inventory", 'Library lib;\nCHECK_EQ(lib.size(), 0);\nCHECK_EQ(lib.inventory(), std::string(""));', "An empty library inventories as an empty string."),
    ],
    difficulty="advanced",
)

VI_BORROW = vi_challenge(
    "Đường nối 1: state machine mượn/trả",
    "Hoàn thiện `BorrowTracker`: `bool borrow(const std::string& isbn)` chuyển sách Available (hoặc chưa biết) sang Borrowed và trả true — nhưng trả false và không đổi gì nếu đang Borrowed. `bool give_back(...)` là chiều ngược lại khi trả sách. `bool is_borrowed(...) const` báo trạng thái; sách chưa biết là không bị mượn.",
    [
        ("happy-path", "Borrow chuyển Available→Borrowed; give_back chuyển ngược lại."),
        ("double-borrow", "Lần mượn thứ hai phải bị từ chối, không được âm thầm thành công."),
        ("return-unknown", "Trả một cuốn chưa từng được mượn là bị từ chối."),
    ],
)

VI_ROUNDTRIP = vi_challenge(
    "Đường nối 2: vòng round-trip lưu trữ",
    "Cài cặp `std::string serialize(const std::vector<Book>&)` và `std::vector<Book> deserialize(const std::string&)` với định dạng bản ghi `title|quantity` mỗi dòng. `deserialize` bỏ qua dòng trống, bỏ qua dòng không có `|`, và bỏ qua dòng có số lượng không phải số nguyên hợp lệ — một dòng hỏng không bao giờ hủy toàn bộ lần tải. `Book` là `{std::string title; int quantity;}`.",
    [
        ("roundtrip", "Serialize → deserialize phải tái tạo đúng mọi bản ghi."),
        ("corrupt-lines", "Dòng không phân tích được bị bỏ qua, không phải kết thúc chương trình."),
        ("empty-content", "Tệp rỗng tải thành một thư viện rỗng."),
    ],
)

VI_VALIDATE = vi_challenge(
    "Đường nối 3: biên giới kiểm tra dữ liệu",
    "Hoàn thiện `Catalog::validate(const NewBook&) const` trả `std::optional<AddError>`: `EmptyTitle` cho tiêu đề rỗng, `BadQuantity` cho số lượng <= 0, `Duplicate` khi tiêu đề đã tồn tại, và `std::nullopt` khi sách được phép thêm. Kiểm tra theo đúng thứ tự đó — một test đưa tiêu đề rỗng với số lượng 0 và kỳ vọng EmptyTitle.",
    [
        ("order-matters", "Tiêu đề rỗng thắng số lượng xấu — thứ tự chính là hợp đồng."),
        ("duplicate", "Tiêu đề trùng bị từ chối."),
        ("valid", "Một cuốn sách sạch trả nullopt — không gì cản việc thêm."),
    ],
)

VI_CP_CAPSTONE = vi_challenge(
    "Kiểm tra điểm: Library hoàn chỉnh",
    "Lắp ráp lõi capstone: `class Library` giữ `std::vector<Book>` với `void add(const Book&)`, `std::optional<const Book*> find(const std::string& title) const`, `std::size_t size() const`, và `std::string inventory() const` — danh sách các dòng `title|quantity` theo thứ tự chèn (mỗi sách một dòng, kết thúc bằng \\n; thư viện rỗng cho chuỗi rỗng). `Book` là `{std::string title; int quantity;}`.",
    [
        ("add-find", "add lưu trữ; find trả con trỏ tới sách thật hoặc nullopt."),
        ("inventory-format", "Thứ tự chèn, `title|quantity`, mỗi sách một dòng."),
        ("empty-inventory", "Thư viện rỗng có bản kê khai là chuỗi rỗng."),
    ],
)

P1 = [CH_BORROW, CH_ROUNDTRIP, CH_VALIDATE]
VI_P1 = {
    "cppi-m12-borrow-state": VI_BORROW,
    "cppi-m12-persistence": VI_ROUNDTRIP,
    "cppi-m12-validation": VI_VALIDATE,
}

# ---- final checkpoint solution pair --------------------------------------------------------
R_CAPSTONE = r'''#include <optional>
#include <string>
#include <vector>

struct Book {
    std::string title;
    int quantity;
};

class Library {
public:
    void add(const Book& b) { books_.push_back(b); }

    std::optional<const Book*> find(const std::string& title) const {
        for (const auto& b : books_)
            if (b.title == title) return &b;
        return std::nullopt;
    }

    std::size_t size() const { return books_.size(); }

    std::string inventory() const {
        std::string out;
        for (const auto& b : books_) {
            out += b.title;
            out += '|';
            out += std::to_string(b.quantity);
            out += '\n';
        }
        return out;
    }

private:
    std::vector<Book> books_;
};
'''

W_CAPSTONE = r'''#include <optional>
#include <string>
#include <vector>

struct Book {
    std::string title;
    int quantity;
};

class Library {
public:
    void add(const Book& b) { books_.push_back(b); }

    std::optional<const Book*> find(const std::string& title) const {
        for (const auto& b : books_)
            if (b.title == title) return &b;
        return std::nullopt;
    }

    std::size_t size() const { return books_.size(); }

    std::string inventory() const {
        std::string out;
        for (const auto& b : books_) {
            out += b.title;
            out += '|';
            out += std::to_string(b.quantity);
            // BUG: missing the line separator — inventory is one long line
        }
        return out;
    }

private:
    std::vector<Book> books_;
};
'''

# ---- emit ---------------------------------------------------------------------------------
write_lesson(
    MOD, "project-architecture",
    "Project Architecture: The Three Seams",
    "App vs Library vs persistence: responsibilities, ownership, and where the boundaries live.",
    25, L_architecture_EN,
    "Kiến trúc dự án: ba đường nối",
    "App vs Library vs lưu trữ: trách nhiệm, sở hữu, và các biên giới nằm ở đâu.",
    L_architecture_VI,
)
write_lesson(
    MOD, "integration",
    "Integration: Every Module, One Program",
    "A module-by-module map of where each skill lands in the capstone, plus a worked find() skeleton.",
    25, L_integration_EN,
    "Tích hợp: mọi module, một chương trình",
    "Bản đồ module-theo-module cho từng kỹ năng đậu ở đâu trong capstone, cộng khung find() mẫu.",
    L_integration_VI,
)
write_lesson(
    MOD, "ship-it",
    "Ship It: The Finishing Checklist",
    "Testable requirements, designed errors, boring happy paths, durable state, and explainable lines.",
    20, L_ship_EN,
    "Hoàn thiện: checklist khép lại dự án",
    "Yêu cầu kiểm thử được, lỗi được thiết kế, đường vui nhàm chán, trạng thái bền, và dòng code giải thích được.",
    L_ship_VI,
)

write_practice(
    MOD, "cppi-p12-capstone",
    "Capstone seams",
    "The three graded seams: borrow state machine, persistence round-trip, and validation boundary.",
    "Các đường nối capstone",
    "Ba đường nối được chấm điểm: state machine mượn/trả, vòng round-trip lưu trữ, và biên giới kiểm tra dữ liệu.",
    "project-architecture", 45, "advanced", P1, VI_P1,
    solutions=[
        ("cppi-m12-borrow-state", R_BORROW, W_BORROW),
        ("cppi-m12-persistence", R_ROUNDTRIP, W_ROUNDTRIP),
        ("cppi-m12-validation", R_VALIDATE, W_VALIDATE),
    ],
)

write_checkpoint(
    MOD, "cppi-checkpoint-final",
    "Checkpoint: The Library, Assembled",
    "The capstone core object: add, find with optional, and an inventory serializer — the whole course in one class.",
    40,
    r"""
`Library` is the final exam because it is the course in miniature:

- `add`/`find`/`size` are encapsulation (M2-M4) with a clean interface
- `std::optional<const Book*>` is the modern result type (M7)
- `inventory()` is a serializer (M10) with an exact format contract

The format tests are deliberately strict — `A|1\nB|3\n`, insertion order,
empty string when empty — because *exact output* is what a persistence
boundary means in practice. "Close enough" is a parse error on the way
back in.

Finish here and you have touched every layer: types, containers,
algorithms, errors, and the seams between them. That is the intermediate
bar: not that you have seen the features, but that you can *assemble*
them into a small, working, explainable system.
""",
    "Kiểm tra điểm: Library hoàn chỉnh",
    "Đối tượng lõi của capstone: add, find với optional, và một serializer kê khai — cả khóa học gọn trong một lớp.",
    r"""
`Library` là bài thi cuối vì nó là phiên bản thu nhỏ của cả khóa học:

- `add`/`find`/`size` là encapsulation (M2-M4) với interface sạch
- `std::optional<const Book*>` là kiểu kết quả hiện đại (M7)
- `inventory()` là một serializer (M10) với hợp đồng định dạng chính xác

Các test định dạng cố tình nghiêm ngặt — `A|1\nB|3\n`, thứ tự chèn,
chuỗi rỗng khi rỗng — vì *đầu ra chính xác* là thứ biên giới lưu trữ
nghĩa trong thực tế. "Gần đủ" là một lỗi parse trên đường quay lại.

Hoàn thành ở đây nghĩa là bạn đã chạm mọi tầng: kiểu, container, thuật
toán, lỗi, và các đường nối giữa chúng. Đó là chuẩn trung cấp: không phải
bạn đã *thấy* các tính năng, mà là bạn có thể *lắp ráp* chúng thành một
hệ thống nhỏ, chạy được, giải thích được.
""",
    CP_CAPSTONE, VI_CP_CAPSTONE,
    solution=R_CAPSTONE, wrong=W_CAPSTONE,
)

write_module(
    MOD,
    "Intermediate Final Project",
    "The capstone: architecture, integration, and a finishing checklist — assemble the whole course into one working library manager.",
    "Dự án cuối khóa Trung cấp",
    "Capstone: kiến trúc, tích hợp, và checklist hoàn thiện — lắp cả khóa học thành một trình quản lý thư viện chạy được.",
    ["project-architecture", "integration", "ship-it", "cppi-checkpoint-final"],
    ["cppi-p12-capstone"],
)
print("module 12 emitted")
