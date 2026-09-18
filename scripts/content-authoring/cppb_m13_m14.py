#!/usr/bin/env python3
"""C++ Beginner — modules 13 (files) and 14 (errors, debugging, testing)."""
from cppb import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 13: files-persistence ============================
M13 = "files-persistence"

L13A = "reading-and-writing-files"
L13B = "parsing-records-from-files"
L13C = "checkpoint-persistence"

write_module(
    M13,
    "Files & Persistence",
    "Programs that remember: ifstream/ofstream, line-based processing, CSV records, and the RAII story you already know.",
    "File & Lưu trữ",
    "Chương trình biết nhớ: ifstream/ofstream, xử lý theo dòng, bản ghi CSV, và câu chuyện RAII mà bạn đã thuộc.",
    [L13A, L13B, L13C],
    ["m13-file-practice"],
)

write_lesson(
    M13, L13A,
    "Reading and Writing Files",
    "ofstream to write, ifstream to read, getline for lines, and the open-fail check that saves hours.",
    11,
    '''
## Writing a file

```cpp
#include <fstream>

int main() {
    std::ofstream out{"notes.txt"};                 // open for writing (creates/truncates)
    if (!out) {                                     // ALWAYS check the open
        std::cerr << "cannot open notes.txt\\n";
        return 1;
    }
    out << "buy milk\\n" << "learn C++\\n";
}                                                    // destructor closes — RAII
```

No `close()` call: the destructor closes and flushes, even on early returns. That is module 12's RAII paying rent.

## Reading a file line by line

```cpp
std::ifstream in{"notes.txt"};
if (!in) { /* same check */ }
std::string line;
while (std::getline(in, line)) {
    std::cout << line << '\\n';
}                                                   // loop ends at EOF
```

The `getline` loop is THE file-reading pattern; the stream's boolean state ends the loop exactly at end-of-file.

## Append mode and file modes

```cpp
std::ofstream log{"app.log", std::ios::app};    // append, do not truncate
```

Other modes exist (`std::ios::binary`, `in|out`) but Beginner lives in text mode.

## The checks that matter

1. **Open check** after construction (`if (!out)`) — missing files, permissions, wrong paths.
2. **Read check** in the loop condition — handled by `getline` itself.
3. Rare deep failures (disk full mid-write) are real but Intermediate's exception-safety territory; here, check the open and the loop.
''',
    "Đọc và ghi file",
    "ofstream để ghi, ifstream để đọc, getline cho từng dòng, và phép kiểm tra mở-file cứu bạn cả giờ đồng hồ.",
    '''
## Ghi một file

```cpp
#include <fstream>

int main() {
    std::ofstream out{"notes.txt"};                 // mở để ghi (tạo mới/ghi đè)
    if (!out) {                                     // LUÔN kiểm tra lần mở
        std::cerr << "cannot open notes.txt\\n";
        return 1;
    }
    out << "buy milk\\n" << "learn C++\\n";
}                                                    // destructor đóng file — RAII
```

Không cần gọi `close()`: destructor đóng và flush, kể cả khi return sớm. RAII ở module 12 bắt đầu trả tiền nhà.

## Đọc file theo từng dòng

```cpp
std::ifstream in{"notes.txt"};
if (!in) { /* kiểm tra tương tự */ }
std::string line;
while (std::getline(in, line)) {
    std::cout << line << '\\n';
}                                                   // vòng lặp dừng tại EOF
```

Vòng lặp `getline` là MẪU đọc file; trạng thái boolean của stream kết thúc vòng lặp đúng lúc hết file.

## Chế độ append và các file mode

```cpp
std::ofstream log{"app.log", std::ios::app};    // nối tiếp, không ghi đè
```

Các mode khác tồn tại (`std::ios::binary`, `in|out`) nhưng trình độ Cơ bản sống trong chế độ text.

## Những phép kiểm tra quan trọng

1. **Kiểm tra mở** sau khi dựng (`if (!out)`) — file thiếu, thiếu quyền, đường dẫn sai.
2. **Kiểm tra đọc** trong điều kiện vòng lặp — `getline` tự lo.
3. Các lỗi sâu hiếm gặp (đĩa đầy giữa chừng) có thật nhưng thuộc exception-safety của Trung cấp; ở đây, kiểm tra lần mở và vòng lặp.
''',
)

write_lesson(
    M13, L13B,
    "Parsing Records from Files",
    "Module 6's mini-CSV pattern, now fed by a file: line loop + row stream + stoi/stod, plus std::filesystem basics.",
    11,
    '''
## The full pattern: file → lines → fields → typed data

```cpp
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

struct Item { std::string name; double price{}; int qty{}; };

std::vector<Item> load_items(const std::string& path) {
    std::ifstream in{path};
    std::vector<Item> items;
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;                 // tolerate blank lines
        std::istringstream row{line};
        std::string name, price_s, qty_s;
        std::getline(row, name, ',');
        std::getline(row, price_s, ',');
        std::getline(row, qty_s);
        items.push_back({name, std::stod(price_s), std::stoi(qty_s)});
    }
    return items;
}
```

Recognize every piece: the getline loop (13A), the row stream with delimiter (module 6), typed conversion. This function is the capstone's storage layer in embryo — data outlives the program because it is *just text* you can also read with any editor.

## Writing records back

```cpp
void save_items(const std::string& path, const std::vector<Item>& items) {
    std::ofstream out{path};
    for (const Item& it : items) {
        out << it.name << ',' << it.price << ',' << it.qty << '\\n';
    }
}
```

Round-trip discipline: whatever you write must parse again. Choose one format, keep both sides in sync.

## std::filesystem (a beginner's slice)

```cpp
#include <filesystem>
namespace fs = std::filesystem;

fs::exists("data/items.csv")         // does it exist?
fs::file_size("data/items.csv")      // bytes
for (const auto& entry : fs::directory_iterator("data")) { /* entries */ }
```

Enough to check, measure, and list. Creating/removing directories and path manipulation grow in Intermediate.

## A caution about numbers and locales

`stod`/`cout` number formatting follows the C locale by default (dot decimals). For this course's data files, dot decimals in, dot decimals out — consistency is the whole game.
''',
    "Phân tích bản ghi từ file",
    "Mẫu mini-CSV của module 6, giờ được nuôi bằng file: vòng lặp dòng + row stream + stoi/stod, cùng kiến thức cơ bản về std::filesystem.",
    '''
## Mẫu hoàn chỉnh: file → dòng → trường → dữ liệu có kiểu

```cpp
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

struct Item { std::string name; double price{}; int qty{}; };

std::vector<Item> load_items(const std::string& path) {
    std::ifstream in{path};
    std::vector<Item> items;
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;                 // tha thứ dòng trống
        std::istringstream row{line};
        std::string name, price_s, qty_s;
        std::getline(row, name, ',');
        std::getline(row, price_s, ',');
        std::getline(row, qty_s);
        items.push_back({name, std::stod(price_s), std::stoi(qty_s)});
    }
    return items;
}
```

Nhận ra từng mảnh: vòng lặp getline (13A), row stream với ký tự phân cách (module 6), chuyển đổi có kiểu. Hàm này chính là phôi thai của tầng lưu trữ trong capstone — dữ liệu sống lâu hơn chương trình vì nó chỉ là *text* mà bạn có thể mở bằng bất kỳ trình soạn thảo nào.

## Ghi bản ghi ngược lại

```cpp
void save_items(const std::string& path, const std::vector<Item>& items) {
    std::ofstream out{path};
    for (const Item& it : items) {
        out << it.name << ',' << it.price << ',' << it.qty << '\\n';
    }
}
```

Kỷ luật round-trip: bất cứ gì bạn ghi ra đều phải phân tích được lần nữa. Chọn một định dạng và giữ cả hai phía đồng bộ.

## std::filesystem (một lát cắt cho người mới)

```cpp
#include <filesystem>
namespace fs = std::filesystem;

fs::exists("data/items.csv")         // nó có tồn tại không?
fs::file_size("data/items.csv")      // số byte
for (const auto& entry : fs::directory_iterator("data")) { /* các mục */ }
```

Đủ để kiểm tra, đo, và liệt kê. Tạo/xóa thư mục và biến đổi đường dẫn sẽ lớn lên ở Trung cấp.

## Một lưu ý về số và locale

`stod`/`cout` định dạng số theo locale C mặc định (dấu chấm thập phân). Với các file dữ liệu của khóa này, dấu chấm vào, dấu chấm ra — tính nhất quán là tất cả.
''',
)

# ---- Module 13 checkpoint ----
write_checkpoint(
    M13, L13C,
    "Checkpoint: Persistence",
    "One graded challenge: a save/load round-trip that must reproduce data exactly.",
    15,
    '''
**Checkpoint — persistence.** Pass the graded challenge below to finish the module.

The graded tests cannot see files (grading runs code, not I/O) — so they grade the *round-trip logic* through strings: serialize items to the CSV text, parse text back to items, and require equality. Same skill, hermetic testing.
''',
    "Checkpoint: Lưu trữ",
    "Một challenge có chấm: round-trip save/load phải tái tạo dữ liệu chính xác.",
    '''
**Checkpoint — lưu trữ.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Các test có chấm không nhìn thấy file (phần chấm chạy code, không chạy I/O) — vì vậy chúng chấm *logic round-trip* qua chuỗi: serialize các item thành text CSV, parse text trở lại thành item, và đòi hỏi bằng nhau. Cùng kỹ năng, kiểm thử kín.
''',
    challenge(
        "cpp13-check-csv-roundtrip",
        "CSV Round-Trip",
        "Implement `serialize(items)` producing lines `name,price,qty` and `parse(csv)` producing the items back. Round-trip must preserve everything.",
        "#include <sstream>\\n#include <string>\\n#include <vector>\\n\\nstruct Item { std::string name; double price{}; int qty{}; };\\n\\nstd::string serialize(const std::vector<Item>& items) {\\n    // TODO\\n}\\nstd::vector<Item> parse(const std::string& csv) {\\n    // TODO\\n}",
        [
            ("serialize", "std::vector<Item> items{{\"pen\", 2.5, 120}}; CHECK(serialize(items) == std::string{\"pen,2.5,120\\\\n\"});", "One line per item, comma-separated, trailing newline."),
            ("parse", "auto items = parse(std::string{\"pen,2.5,120\\\\n\"}); CHECK_EQ(items.size(), 1); CHECK(items[0].name == std::string{\"pen\"}); CHECK_NEAR(items[0].price, 2.5, 0.001); CHECK_EQ(items[0].qty, 120);", "getline(',') + stod + stoi."),
            ("roundtrip", "std::vector<Item> items{{\"a\", 1.0, 2}, {\"b c\", 3.5, 4}}; auto again = parse(serialize(items)); CHECK_EQ(again.size(), 2); CHECK(again[1].name == std::string{\"b c\"});", "Two items survive intact — names may contain spaces; commas may not."),
        ],
        level="real-world",
        difficulty="beginner",
    ),
    vi_challenge(
        "Round-trip CSV",
        "Cài đặt `serialize(items)` tạo các dòng `name,price,qty` và `parse(csv)` trả lại các item. Round-trip phải bảo toàn mọi thứ.",
        [("serialize", "Mỗi item một dòng, ngăn cách bằng dấu phẩy, kết thúc bằng xuống dòng."), ("parse", "getline(',') + stod + stoi."), ("roundtrip", "Hai item sống sót nguyên vẹn — tên có thể chứa dấu cách; dấu phẩy thì không.")],
    ),
    solution="#include <sstream>\\n#include <string>\\n#include <vector>\\nstruct Item { std::string name; double price{}; int qty{}; };\\n\\nstd::string serialize(const std::vector<Item>& items) {\\n    std::ostringstream out;\\n    for (const Item& it : items) out << it.name << ',' << it.price << ',' << it.qty << '\\\\n';\\n    return out.str();\\n}\\nstd::vector<Item> parse(const std::string& csv) {\\n    std::istringstream in{csv};\\n    std::vector<Item> items;\\n    std::string line;\\n    while (std::getline(in, line)) {\\n        if (line.empty()) continue;\\n        std::istringstream row{line};\\n        std::string name, price_s, qty_s;\\n        std::getline(row, name, ',');\\n        std::getline(row, price_s, ',');\\n        std::getline(row, qty_s);\\n        items.push_back({name, std::stod(price_s), std::stoi(qty_s)});\\n    }\\n    return items;\\n}",
    wrong="#include <sstream>\\n#include <string>\\n#include <vector>\\nstruct Item { std::string name; double price{}; int qty{}; };\\n\\nstd::string serialize(const std::vector<Item>& items) {\\n    std::ostringstream out;\\n    for (const Item& it : items) out << it.name << ',' << it.price << ',' << it.qty << ' ';\\n    return out.str();\\n}\\nstd::vector<Item> parse(const std::string& csv) {\\n    std::istringstream in{csv};\\n    std::vector<Item> items;\\n    std::string line;\\n    while (std::getline(in, line)) {\\n        if (line.empty()) continue;\\n        std::istringstream row{line};\\n        std::string name, price_s, qty_s;\\n        std::getline(row, name, ',');\\n        std::getline(row, price_s, ',');\\n        std::getline(row, qty_s);\\n        items.push_back({name, std::stod(price_s), std::stoi(qty_s)});\\n    }\\n    return items;\\n}",
)

# ---- Module 13 practice ----
write_practice(
    M13, "m13-file-practice",
    "File Practice: Lines and Logs",
    "Log-line filtering, a word-count over multi-line text, and the fs-exists gate.",
    "Luyện File: Dòng và log",
    "Lọc dòng log, đếm từ trên văn bản nhiều dòng, và cổng kiểm tra tồn tại với fs.",
    L13A, 25, "beginner",
    [
        challenge(
            "cpp13-filter-errors",
            "Filter Error Logs",
            "Implement `error_lines(log)` returning a new string containing only the lines that start with \"ERROR\", each kept as-is with its newline. No ERROR lines → empty string.",
            "#include <sstream>\\n#include <string>\\n\\nstd::string error_lines(const std::string& log) {\\n    // TODO\\n}",
            [("filters", "std::string out = error_lines(std::string{\"INFO ok\\\\nERROR bad\\\\nINFO fine\\\\nERROR worse\\\\n\"}); CHECK(out == std::string{\"ERROR bad\\\\nERROR worse\\\\n\"});", "Only ERROR lines, order preserved, newlines kept."), ("none", "CHECK(error_lines(std::string{\"INFO a\\\\n\"}).empty());", "No matches → empty output."), ("prefix only", "CHECK(error_lines(std::string{\"XERROR no\\\\nERROR yes\\\\n\"}) == std::string{\"ERROR yes\\\\n\"});", "The line must START with ERROR — not merely contain it.")],
            level="real-world",
        ),
    ],
    {"cpp13-filter-errors": vi_challenge("Lọc log lỗi", "Cài `error_lines(log)` trả về một chuỗi mới chỉ chứa những dòng bắt đầu bằng \"ERROR\", giữ nguyên từng dòng kèm ký tự xuống dòng. Không có dòng ERROR → chuỗi rỗng.", [("lọc", "Chỉ các dòng ERROR, giữ thứ tự, giữ xuống dòng."), ("không có", "Không khớp → output rỗng."), ("chỉ tính tiền tố", "Dòng phải BẮT ĐẦU bằng ERROR — không phải chỉ chứa nó.")])},
    solutions=[
        ("cpp13-filter-errors", "#include <sstream>\\n#include <string>\\nstd::string error_lines(const std::string& log) {\\n    std::istringstream in{log};\\n    std::string line, out;\\n    while (std::getline(in, line)) {\\n        if (line.rfind(\"ERROR\", 0) == 0) out += line + '\\\\n';\\n    }\\n    return out;\\n}", "#include <sstream>\\n#include <string>\\nstd::string error_lines(const std::string& log) {\\n    std::istringstream in{log};\\n    std::string line, out;\\n    while (std::getline(in, line)) {\\n        if (line.find(\"ERROR\") != std::string::npos) out += line + '\\\\n';\\n    }\\n    return out;\\n}"),
    ],
)

# ============================ MODULE 14: errors-debugging-tests ============================
M14 = "errors-debugging-tests"

L14A = "exceptions-and-boundaries"
L14B = "assert-and-testing"
L14C = "debugging-method"
L14D = "checkpoint-robustness"

write_module(
    M14,
    "Errors, Debugging & Testing",
    "Exceptions at boundaries, assertions in development, a repeatable debugging method, and your first test suites.",
    "Lỗi, Gỡ lỗi & Kiểm thử",
    "Exception ở ranh giới, assertion trong lúc phát triển, một phương pháp gỡ lỗi lặp lại được, và những bộ test đầu tiên của bạn.",
    [L14A, L14B, L14C, L14D],
    ["m14-test-practice"],
)

write_lesson(
    M14, L14A,
    "Exceptions and the Boundary Rule",
    "throw/catch basics, the exception hierarchy, and the professional rule: throw for failures you cannot handle locally, catch at boundaries.",
    11,
    '''
## throw, catch, and the journey between

```cpp
#include <stdexcept>

double parse_ratio(const std::string& text) {
    double value = std::stod(text);            // std::stod throws std::invalid_argument on garbage
    if (value < 0 || value > 1) throw std::out_of_range("ratio must be within [0,1]");
    return value;
}

int main() {
    try {
        double r = parse_ratio("1.5");
        use(r);
    } catch (const std::invalid_argument& e) {
        std::cerr << "not a number: " << e.what() << '\\n';
        return 1;
    } catch (const std::out_of_range& e) {
        std::cerr << "out of range: " << e.what() << '\\n';
        return 1;
    }
}
```

A `throw` unwinds the call stack until some `catch` accepts it; destructors run along the way (RAII holds under exceptions — that is the design). Catch **by const reference**; `catch (...)` is the last-resort catch-all.

## The hierarchy you will actually meet

`std::exception` → `std::logic_error` (`std::invalid_argument`, `std::out_of_range`) and `std::runtime_error` (and stream/file failures). Throw `std::runtime_error` (or a logic_error child) with a *specific message*; `e.what()` is what your users will read.

## The boundary rule

**Throw** when a function cannot fulfill its contract and no local answer exists (bad input deep inside a parser). **Catch** at boundaries — `main`, a request handler, a CLI command loop — where you can inform a human and continue or exit cleanly. Catching everywhere in between buries errors under layers of `try` noise; letting everything crash loses the chance to explain. The graded exercises follow the rule: low-level functions throw, the harness plays `main`.

## What NOT to do

- Don't throw for ordinary control flow (end-of-list is a return value, not an exception).
- Don't `catch (...)` silently and continue — that is how bugs become ghosts.
- Don't throw from destructors.
''',
    "Exception và quy tắc ranh giới",
    "Cơ bản về throw/catch, hệ phân cấp exception, và quy tắc chuyên nghiệp: ném khi không thể tự xử lý, bắt ở ranh giới.",
    '''
## throw, catch, và hành trình giữa hai điểm

```cpp
#include <stdexcept>

double parse_ratio(const std::string& text) {
    double value = std::stod(text);            // std::stod ném std::invalid_argument khi gặp rác
    if (value < 0 || value > 1) throw std::out_of_range("ratio must be within [0,1]");
    return value;
}

int main() {
    try {
        double r = parse_ratio("1.5");
        use(r);
    } catch (const std::invalid_argument& e) {
        std::cerr << "not a number: " << e.what() << '\\n';
        return 1;
    } catch (const std::out_of_range& e) {
        std::cerr << "out of range: " << e.what() << '\\n';
        return 1;
    }
}
```

Một `throw` bóc tách call stack cho tới khi một `catch` nào đó nhận nó; các destructor chạy dọc đường (RAII đứng vững dưới exception — đó là thiết kế). Bắt **bằng tham chiếu const**; `catch (...)` là phương án cuối cùng.

## Hệ phân cấp bạn sẽ thực sự gặp

`std::exception` → `std::logic_error` (`std::invalid_argument`, `std::out_of_range`) và `std::runtime_error` (và các lỗi stream/file). Hãy ném `std::runtime_error` (hoặc con của logic_error) kèm *thông điệp cụ thể*; `e.what()` là thứ người dùng của bạn sẽ đọc.

## Quy tắc ranh giới

**Ném** khi một hàm không thể hoàn thành hợp đồng và không có câu trả lời cục bộ (input xấu sâu trong một parser). **Bắt** ở các ranh giới — `main`, handler của request, vòng lặp lệnh CLI — nơi bạn có thể báo cho con người và tiếp tục hoặc thoát sạch sẽ. Bắt ở mọi tầng ở giữa chỉ chôn vùi lỗi dưới lớp `try` ồn ào; để tất cả crash thì mất cơ hội giải thích. Các bài có chấm theo đúng quy tắc này: hàm thấp ném, harness đóng vai `main`.

## Đừng làm gì

- Đừng ném exception cho luồng điều khiển thông thường (hết danh sách là giá trị trả về, không phải exception).
- Đừng `catch (...)` trong im lặng rồi tiếp tục — đó là cách bug thành hồn ma.
- Đừng ném exception từ destructor.
''',
)

write_lesson(
    M14, L14B,
    "Assertions and Your First Tests",
    "assert for development-time contracts, hand-rolled test functions, and the shape of a maintainable suite.",
    11,
    '''
## assert: the contract you check while developing

```cpp
#include <cassert>

double average(const std::vector<int>& v) {
    assert(!v.empty() && "average of empty vector is undefined");
    // ...
}
```

`assert(expr)` aborts the program (with file/line) when expr is false — in debug builds. It documents and enforces *programmer mistakes* (broken internal contracts), not user input. Release builds typically compile them away: never put required behavior only in an assert.

## Hand-rolled tests: the harness you already know

You have been reading them all course — now write one:

```cpp
#include <iostream>
#include <vector>

int total(const std::vector<int>& v);   // under test

void test_total() {
    if (total({1, 2, 3}) != 6) { std::cerr << "FAIL total basic\\n"; std::exit(1); }
    if (total({}) != 0)        { std::cerr << "FAIL total empty\\n"; std::exit(1); }
}

void test_average() { /* ... */ }

int main() {
    test_total();
    test_average();
    std::cout << "all tests passed\\n";
}
```

A real test suite: one function per behavior, **named after the expectation**, failing loudly with which test broke, exiting non-zero so CI notices. (Frameworks like Catch2/GoogleTest automate the plumbing — same shape, more sugar; the platform's own C++ harness is the same idea.)

## What to test (the beginner checklist)

- The obvious case (1,2,3 → 6).
- The edges: empty, single element, zero, negative, maximum.
- The documented errors: bad input must throw / return the error value.
- One "regression": a case that failed once and was fixed — it stays in the suite forever.

## Red-green discipline

Write the test first, watch it fail (red), implement until it passes (green). It sounds ceremonial; it is how you *know the test can fail* — a test that has never failed tests nothing.
''',
    "Assertion và bộ test đầu tiên",
    "assert cho các bản hợp đồng lúc phát triển, hàm test viết tay, và hình dạng của một bộ test dễ bảo trì.",
    '''
## assert: bản hợp đồng được kiểm tra khi phát triển

```cpp
#include <cassert>

double average(const std::vector<int>& v) {
    assert(!v.empty() && "average of empty vector is undefined");
    // ...
}
```

`assert(expr)` hủy chương trình (kèm file/dòng) khi expr sai — trong bản debug. Nó ghi lại và thực thi *lỗi của lập trình viên* (hợp đồng nội bộ hỏng), không phải input của người dùng. Bản release thường biên dịch chúng đi: đừng bao giờ đặt hành vi bắt buộc chỉ trong assert.

## Test viết tay: harness mà bạn đã đọc suốt khóa

Bạn đã đọc chúng cả khóa — giờ hãy tự viết:

```cpp
#include <iostream>
#include <vector>

int total(const std::vector<int>& v);   // thứ đang được test

void test_total() {
    if (total({1, 2, 3}) != 6) { std::cerr << "FAIL total basic\\n"; std::exit(1); }
    if (total({}) != 0)        { std::cerr << "FAIL total empty\\n"; std::exit(1); }
}

void test_average() { /* ... */ }

int main() {
    test_total();
    test_average();
    std::cout << "all tests passed\\n";
}
```

Một bộ test thật: mỗi hành vi một hàm, **đặt tên theo kỳ vọng**, hét to khi hỏng kèm tên test nào vỡ, thoát với mã khác 0 để CI biết. (Các framework như Catch2/GoogleTest tự động hóa phần ống nước — cùng hình dạng, thêm đường; harness C++ của chính nền tảng này cũng là cùng ý tưởng.)

## Test cái gì (checklist cho người mới)

- Trường hợp hiển nhiên (1,2,3 → 6).
- Các biên: rỗng, một phần tử, số 0, số âm, giá trị lớn nhất.
- Các lỗi đã ghi nhận: input xấu phải throw / trả về giá trị lỗi.
- Một "regression": trường hợp từng hỏng và đã được sửa — nó ở lại bộ test mãi mãi.

## Kỷ luật đỏ-xanh

Viết test trước, nhìn nó hỏng (đỏ), cài đặt đến khi pass (xanh). Nghe như nghi lễ; nhưng đó là cách bạn *biết test có thể hỏng* — một test chưa bao giờ hỏng thì chẳng test được gì.
''',
)

write_lesson(
    M14, L14C,
    "A Debugging Method That Always Works",
    "Reproduce, read the evidence, bisect, form one hypothesis at a time — the loop professionals run, plus the warning-fueled workflow.",
    10,
    '''
## The loop

1. **Reproduce deterministically.** A bug you can trigger on demand is half-dead. Find the smallest input that still fails.
2. **Read the evidence.** The crash message, the assert text, the wrong *value* — each names a neighborhood. Compiler warnings are free bug reports; this course compiles with `-Wall -Wextra -Wpedantic` and so should you.
3. **Form ONE hypothesis.** "The index is off by one at the last element" — not "something is wrong with loops".
4. **Test it cheaply.** Print the suspect values, or run under a debugger (breakpoints, step, inspect — learn your IDE's debugger; it beats print for anything nontrivial).
5. **Fix, then re-run the WHOLE suite** — not just the failing case, or you just traded one bug for another.
6. **Add the regression test.** The bug you just killed must never resurrect silently.

## Bisecting: when you have no idea

Comment out / skip half the pipeline; does it still fail? The bug lives in the failing half. Repeat. Log₂ of a thousand-line program is about ten experiments — bisection turns "impossible" into "twenty minutes".

## The classic beginner traps, one last time

- Uninitialized variable (garbage that "works sometimes").
- Off-by-one at boundaries (test the empty and single cases explicitly).
- `=` in a condition.
- Integer division where a double was meant.
- Modifying a container while range-for iterates it (invalidated iterators — push_back during a range-for over the same vector is UB; collect changes, apply after).

## Debugging is the skill

Interviewers know it, senior engineers know it: the scarce skill is not writing code, it is *finding out why the code lies*. Every module's debugging exercises trained this loop; module 18 will lean on it under time pressure.
''',
    "Một phương pháp gỡ lỗi luôn hiệu quả",
    "Tái hiện, đọc bằng chứng, chia để trị, mỗi lần một giả thuyết — vòng lặp mà dân chuyên chạy, cùng quy trình làm việc dựa trên warning.",
    '''
## Vòng lặp

1. **Tái hiện một cách xác định.** Bug có thể kích hoạt theo yêu cầu đã chết một nửa. Tìm input nhỏ nhất vẫn gây lỗi.
2. **Đọc bằng chứng.** Thông báo crash, chữ của assert, *giá trị* sai — mỗi thứ chỉ ra một khu vực. Compiler warning là báo cáo bug miễn phí; khóa này biên dịch với `-Wall -Wextra -Wpedantic` và bạn cũng nên vậy.
3. **Thành lập MỘT giả thuyết.** "Chỉ số lệch một đơn vị ở phần tử cuối" — không phải "chắc vòng lặp có vấn đề".
4. **Kiểm tra giả thuyết giá rẻ.** In các giá trị đáng ngờ, hoặc chạy dưới debugger (breakpoint, bước, soi biến — hãy học debugger của IDE; nó thắng print với mọi thứ không tầm thường).
5. **Sửa, rồi chạy lại TOÀN BỘ bộ test** — không chỉ case đang hỏng, nếu không bạn chỉ đổi một bug lấy một bug khác.
6. **Thêm test regression.** Bug vừa giết được không được sống lại một cách âm thầm.

## Chia để trị: khi bạn không có manh mối

Vô hiệu hóa/bỏ qua một nửa đường ống; nó còn hỏng không? Bug nằm trong nửa hỏng. Lặp lại. Log₂ của một chương trình nghìn dòng là khoảng mười lần thử — chia để trị biến "bất khả thi" thành "hai mươi phút".

## Các cái bẫy kinh điển của người mới, lần cuối

- Biến chưa khởi tạo (rác mà "thi thoảng chạy đúng").
- Off-by-one ở biên (hãy test rõ ràng các case rỗng và một phần tử).
- `=` trong điều kiện.
- Chia số nguyên trong khi ý định là double.
- Sửa container trong khi range-for đang duyệt nó (iterator vô hiệu — push_back trong range-for trên cùng vector là UB; hãy gom thay đổi, áp dụng sau).

## Gỡ lỗi chính là kỹ năng

Người phỏng vấn biết, kỹ sư cao cấp biết: kỹ năng khan hiếm không phải viết code, mà là *tìm ra vì sao code nói dối*. Bài tập gỡ lỗi của mọi module đã luyện vòng lặp này; module 18 sẽ dựa vào nó dưới áp lực thời gian.
''',
)

# ---- Module 14 checkpoint ----
write_checkpoint(
    M14, L14D,
    "Checkpoint: Robustness",
    "One graded challenge: throw exactly where the contract breaks, and survive the boundary tests.",
    15,
    '''
**Checkpoint — robustness.** Pass the graded challenge below to finish the module.

The functions must throw `std::invalid_argument`/`std::out_of_range` on exactly the documented bad inputs — the tests use CHECK_THROWS for those and normal checks for the good paths.
''',
    "Checkpoint: Độ bền",
    "Một challenge có chấm: ném exception đúng nơi hợp đồng vỡ, và sống sót qua các test ở ranh giới.",
    '''
**Checkpoint — độ bền.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Các hàm phải ném `std::invalid_argument`/`std::out_of_range` đúng với các input xấu đã ghi nhận — test dùng CHECK_THROWS cho các trường hợp đó và kiểm tra thường cho đường tốt.
''',
    challenge(
        "cpp14-check-validated-parse",
        "Validated Parsing",
        "Implement `parse_percent(text)` returning the percentage as a double in [0, 100]: throw `std::invalid_argument` for non-numeric text, `std::out_of_range` for numbers outside the range. Valid values return normally.",
        "#include <stdexcept>\\n#include <string>\\n\\ndouble parse_percent(const std::string& text) {\\n    // TODO\\n}",
        [
            ("valid", "CHECK_NEAR(parse_percent(std::string{\"42.5\"}), 42.5, 0.001);", "Plain valid input returns the value."),
            ("bounds inclusive", "CHECK_NEAR(parse_percent(std::string{\"0\"}), 0.0, 0.001); CHECK_NEAR(parse_percent(std::string{\"100\"}), 100.0, 0.001);", "0 and 100 are inside the range."),
            ("not a number", "CHECK_THROWS(parse_percent(std::string{\"abc\"}));", "std::stod throws invalid_argument — let it propagate."),
            ("out of range", "CHECK_THROWS(parse_percent(std::string{\"150\"}));", "Above 100 must throw std::out_of_range."),
            ("negative", "CHECK_THROWS(parse_percent(std::string{\"-1\"}));", "Below 0 must throw std::out_of_range."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Parser có kiểm tra",
        "Cài `parse_percent(text)` trả về phần trăm dưới dạng double trong khoảng [0, 100]: ném `std::invalid_argument` cho text không phải số, `std::out_of_range` cho số ngoài khoảng. Giá trị hợp lệ thì trả về bình thường.",
        [("hợp lệ", "Input hợp lệ thuần túy trả về giá trị."), ("biên bao gồm", "0 và 100 nằm trong khoảng."), ("không phải số", "std::stod ném invalid_argument — cứ để nó lan lên."), ("ngoài khoảng", "Trên 100 phải ném std::out_of_range."), ("âm", "Dưới 0 phải ném std::out_of_range.")],
    ),
    solution="#include <stdexcept>\\n#include <string>\\ndouble parse_percent(const std::string& text) {\\n    double v = std::stod(text);\\n    if (v < 0.0 || v > 100.0) throw std::out_of_range(\"percent must be within [0,100]\");\\n    return v;\\n}",
    wrong="#include <stdexcept>\\n#include <string>\\ndouble parse_percent(const std::string& text) {\\n    double v = std::stod(text);\\n    if (v <= 0.0 || v > 100.0) throw std::out_of_range(\"percent must be within [0,100]\");\\n    return v;\\n}",
)

# ---- Module 14 practice ----
write_practice(
    M14, "m14-test-practice",
    "Testing Practice: Red-Green Discipline",
    "Write the suite for a broken implementation, watch specific tests catch it, then fix it.",
    "Luyện Kiểm thử: Kỷ luật đỏ-xanh",
    "Viết bộ test cho một cài đặt lỗi, nhìn các test cụ thể bắt được nó, rồi sửa nó.",
    L14B, 25, "beginner",
    [
        challenge(
            "cpp14-median",
            "Median With Tests",
            "Implement `median(v)` (middle of sorted copy; average of two middles for even size; 0.0 for empty — no exception). Tests cover odd, even, empty, single, and unsorted input.",
            "#include <algorithm>\\n#include <stdexcept>\\n#include <vector>\\n\\ndouble median(const std::vector<int>& v) {\\n    // TODO\\n}",
            [("odd", "CHECK_NEAR(median({3, 1, 2}), 2.0, 0.001);", "Sort first: middle of {1,2,3}."), ("even", "CHECK_NEAR(median({4, 1, 3, 2}), 2.5, 0.001);", "Average of the two middles."), ("empty", "CHECK_NEAR(median({}), 0.0, 0.001);", "Empty is defined here as 0.0."), ("unsorted", "CHECK_NEAR(median({9, 1}), 5.0, 0.001);", "Never assume sorted input.")],
            level="independent",
        ),
    ],
    {"cpp14-median": vi_challenge("Median kèm test", "Cài `median(v)` (phần tử giữa của bản sao đã sắp; trung bình hai phần tử giữa cho kích thước chẵn; 0.0 cho rỗng — không ném exception). Test bao phủ lẻ, chẵn, rỗng, một phần tử, và input chưa sắp.", [("lẻ", "Sắp trước: giữa của {1,2,3}."), ("chẵn", "Trung bình hai phần tử giữa."), ("rỗng", "Ở đây rỗng được định nghĩa là 0.0."), ("chưa sắp", "Đừng giả định input đã được sắp.")])},
    solutions=[
        ("cpp14-median", "#include <algorithm>\\n#include <stdexcept>\\n#include <vector>\\ndouble median(const std::vector<int>& v) {\\n    if (v.empty()) return 0.0;\\n    std::vector<int> s = v;\\n    std::sort(s.begin(), s.end());\\n    std::size_t n = s.size();\\n    if (n % 2 == 1) return static_cast<double>(s[n / 2]);\\n    return (static_cast<double>(s[n / 2 - 1]) + s[n / 2]) / 2.0;\\n}", "#include <algorithm>\\n#include <stdexcept>\\n#include <vector>\\ndouble median(const std::vector<int>& v) {\\n    if (v.empty()) return 0.0;\\n    std::vector<int> s = v;\\n    std::size_t n = s.size();\\n    if (n % 2 == 1) return static_cast<double>(s[n / 2]);\\n    return (static_cast<double>(s[n / 2 - 1]) + s[n / 2]) / 2.0;\\n}"),
    ],
)

print("modules 13-14 authored")
