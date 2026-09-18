#!/usr/bin/env python3
"""C++ Intermediate — Module 10: errors-and-files.

Authoring discipline: every C++ code string (tests, solutions, boilerplate) is
a raw triple-quoted string, so real newlines stay real and C++ "\\n" literals
stay literal. Snippets are self-contained: each test is its own translation
unit (solution.cpp is #included; no cross-test state). File I/O is graded via
string-based content processing (Beginner's cpp13 pattern) so tests stay
deterministic in the sandbox.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "errors-and-files"

# ---- lesson exceptions --------------------------------------------------------
L_exceptions_EN = r"""
C++ error handling has two channels: return values for *expected* outcomes,
and exceptions for *conditions the caller cannot quietly ignore*.

```cpp
#include <stdexcept>

int parse_port(const std::string& s) {
    int value = std::stoi(s);          // throws std::invalid_argument
    if (value < 0 || value > 65535)
        throw std::out_of_range("port out of range: " + s);
    return value;
}
```

The throwing family you will actually use, all in `<stdexcept>`:

- `std::invalid_argument` — the input is not parseable
- `std::out_of_range` — parseable but outside the legal domain
- `std::runtime_error` — failures only visible at runtime (I/O, network)
- `std::logic_error` — the *program* broke its own contract

Throw by value, catch by `const&`:

```cpp
try {
    int port = parse_port(user_input);
    use(port);
} catch (const std::out_of_range& e) {
    std::cerr << "bad port: " << e.what() << "\n";
} catch (const std::exception& e) {
    std::cerr << "error: " << e.what() << "\n";   // base-class fallback
}
```

Catch order matters: handlers are tried top-down, so put derived types
before bases. A bare `catch (...)` swallows everything — reserve it for
thread boundaries and last-resort barriers.
"""

L_exceptions_VI = r"""
Xử lý lỗi trong C++ có hai kênh: giá trị trả về cho kết quả *đúng như kỳ
vọng*, và ngoại lệ cho *các tình huống caller không thể làm ngơ*.

```cpp
#include <stdexcept>

int parse_port(const std::string& s) {
    int value = std::stoi(s);          // ném std::invalid_argument
    if (value < 0 || value > 65535)
        throw std::out_of_range("port out of range: " + s);
    return value;
}
```

Họ ngoại lệ bạn sẽ thực sự dùng, tất cả trong `<stdexcept>`:

- `std::invalid_argument` — input không phân tích được
- `std::out_of_range` — phân tích được nhưng ngoài miền hợp lệ
- `std::runtime_error` — lỗi chỉ thấy lúc chạy (I/O, mạng)
- `std::logic_error` — *chương trình* tự phá hợp đồng của chính nó

Ném bằng giá trị, bắt bằng `const&`:

```cpp
try {
    int port = parse_port(user_input);
    use(port);
} catch (const std::out_of_range& e) {
    std::cerr << "bad port: " << e.what() << "\n";
} catch (const std::exception& e) {
    std::cerr << "error: " << e.what() << "\n";   // dự phòng lớp cha
}
```

Thứ tự catch rất quan trọng: các handler được thử từ trên xuống, nên đặt
kiểu dẫn xuất trước lớp cha. `catch (...)` trần nuốt mọi thứ — hãy dành nó
cho biên giới thread và rào chắn cuối cùng.
"""

# ---- lesson custom-exceptions -----------------------------------------------------
L_custom_EN = r"""
When `what()` strings are not enough structure, define exception types.
Derive from `std::runtime_error` (or `logic_error`) and carry the *data*
the handler needs:

```cpp
#include <stdexcept>
#include <string>

class ValidationError : public std::runtime_error {
public:
    ValidationError(std::string field, std::string message)
        : std::runtime_error{field + ": " + message},
          field_{std::move(field)}, message_{std::move(message)} {}

    const std::string& field() const noexcept { return field_; }

private:
    std::string field_;
    std::string message_;
};
```

Rules that keep custom exceptions safe:

- constructor must not throw (it would abort during unwinding);
- `what()` is satisfied for free by `std::runtime_error`;
- copy members exist by default — exceptions are copied as they unwind,
  so members must be copyable;
- catch handlers get `const ValidationError&` and can read `.field()`
  without parsing strings.

Design the type around the *handler's* decision: what would a caller do
differently for this failure than for any other? If the answer is
"nothing", a plain `std::runtime_error` string was enough.
"""

L_custom_VI = r"""
Khi chuỗi `what()` chưa đủ cấu trúc, hãy định nghĩa kiểu ngoại lệ riêng.
Kế thừa từ `std::runtime_error` (hoặc `logic_error`) và mang theo *dữ liệu*
mà handler cần:

```cpp
#include <stdexcept>
#include <string>

class ValidationError : public std::runtime_error {
public:
    ValidationError(std::string field, std::string message)
        : std::runtime_error{field + ": " + message},
          field_{std::move(field)}, message_{std::move(message)} {}

    const std::string& field() const noexcept { return field_; }

private:
    std::string field_;
    std::string message_;
};
```

Các quy tắc giữ exception riêng an toàn:

- constructor không được phép ném (sẽ abort trong lúc unwinding);
- `what()` được đáp ứng miễn phí nhờ `std::runtime_error`;
- các member copy tồn tại mặc định — exception bị copy trong lúc unwinding,
  nên member phải copy được;
- handler nhận `const ValidationError&` và đọc `.field()` trực tiếp mà
  không cần parse chuỗi.

Hãy thiết kế kiểu xung quanh *quyết định của handler*: caller sẽ làm gì
khác với lỗi này so với lỗi khác? Nếu câu trả lời là "không gì cả" thì một
chuỗi `std::runtime_error` đơn giản đã đủ.
"""

# ---- lesson exception-safety ------------------------------------------------------
L_safety_EN = r"""
Exception safety is a guarantee a function makes about its state when an
exception flies through it. Three useful levels:

- **basic**: invariants hold; nothing leaks; the object is destructible —
  but the value may be anything valid.
- **strong**: the call either completes or has no effect (commit/rollback).
- **noexcept**: never throws; moves and destructors should be here.

The canonical strong-guarantee idiom is *copy-and-swap*: do the risky work
on a copy, then commit with non-throwing moves.

```cpp
Config& operator=(const Config& other) {
    Config tmp{other};      // may throw — *this untouched
    std::swap(data_, tmp.data_);  // no-throw commit
    return *this;
}
```

Where exceptions fly from matters: between `new` and `delete`, a throw
leaks; RAII (Module 8) closes that window by tying release to scope.
Destructors must be `noexcept` — a `throw` inside unwinding calls
`std::terminate`. This is why `std::vector::erase` with move-only types
demands move constructors marked `noexcept`: reallocation would otherwise
use the copying path.
"""

L_safety_VI = r"""
Exception safety là mức đảm bảo một hàm đưa ra về trạng thái của nó khi
một ngoại lệ bay xuyên qua. Ba cấp hữu ích:

- **basic**: bất biến được giữ; không rò rỉ; đối tượng vẫn hủy được —
  nhưng giá trị có thể là bất cứ giá trị hợp lệ nào.
- **strong**: lời gọi hoặc hoàn tất hoặc không có tác dụng gì
  (commit/rollback).
- **noexcept**: không bao giờ ném; move và destructor nên ở cấp này.

Idiom kinh điển cho đảm bảo strong là *copy-and-swap*: làm phần việc rủi ro
trên một bản copy, rồi commit bằng move không ném.

```cpp
Config& operator=(const Config& other) {
    Config tmp{other};            // có thể ném — *this nguyên vẹn
    std::swap(data_, tmp.data_);  // commit không ném
    return *this;
}
```

Ngoại lệ bay ra từ đâu mới là vấn đề: giữa `new` và `delete`, một cú ném
làm rò rỉ; RAII (Module 8) đóng khung cửa đó bằng cách gắn giải phóng vào
phạm vi. Destructor phải `noexcept` — một `throw` trong lúc unwinding sẽ
gọi `std::terminate`. Vì vậy `std::vector::erase` với kiểu move-only đòi
hỏi move constructor có `noexcept`: nếu không, reallocation sẽ rẽ sang
con đường copy.
"""

# ---- lesson files-streams ------------------------------------------------------------
L_files_EN = r"""
File I/O goes through streams. `ifstream` reads, `ofstream` writes, and
both close in their destructor — RAII again.

```cpp
#include <fstream>
#include <iostream>

std::ifstream in{"config.txt"};
if (!in) {                       // stream is false-y when open failed
    std::cerr << "cannot open config.txt\n";
    return 1;
}

std::string line;
while (std::getline(in, line)) {
    process(line);               // line excludes the trailing newline
}
// in closes here — automatically
```

A reference implementation for our graded pattern — filtering lines whose
content starts with `ERROR `:

```cpp
#include <sstream>
#include <string>
#include <vector>

std::string error_lines(const std::string& content) {
    std::istringstream in{content};          // same interface, in-memory
    std::string out;
    std::string line;
    while (std::getline(in, line)) {
        if (line.rfind("ERROR ", 0) == 0) {  // prefix check
            out += line;
            out += '\n';
        }
    }
    return out;
}
```

The graded tests in this module pass file *content* as a string — the
sandbox has no stable working directory for real files. The parsing
discipline is identical: read line-oriented, check the stream state, and
never assume the last line ends with a newline.

Common file bugs: reading without checking `if (!stream)`, mixing `>>`
and `getline` (the `>>` leaves `\n` in the buffer), and forgetting that
`getline` succeeds on the final line without a trailing `\n`.
"""

L_files_VI = r"""
I/O tệp đi qua stream. `ifstream` đọc, `ofstream` ghi, và cả hai đều đóng
trong destructor — RAII một lần nữa.

```cpp
#include <fstream>
#include <iostream>

std::ifstream in{"config.txt"};
if (!in) {                       // stream false-y khi mở thất bại
    std::cerr << "cannot open config.txt\n";
    return 1;
}

std::string line;
while (std::getline(in, line)) {
    process(line);               // line không chứa ký tự xuống dòng cuối
}
// in đóng tại đây — tự động
```

Một bản tham chiếu cho pattern được chấm điểm của chúng ta — lọc các dòng
có nội dung bắt đầu bằng `ERROR `:

```cpp
#include <sstream>
#include <string>
#include <vector>

std::string error_lines(const std::string& content) {
    std::istringstream in{content};          // cùng interface, trong bộ nhớ
    std::string out;
    std::string line;
    while (std::getline(in, line)) {
        if (line.rfind("ERROR ", 0) == 0) {  // kiểm tra tiền tố
            out += line;
            out += '\n';
        }
    }
    return out;
}
```

Các bài kiểm tra trong module này truyền *nội dung* tệp dưới dạng chuỗi —
sandbox không có thư mục làm việc ổn định cho tệp thật. Kỷ luật phân tích
thì giống hệt: đọc theo dòng, kiểm tra trạng thái stream, và đừng bao giờ
giả định dòng cuối kết thúc bằng `\n`.

Các lỗi tệp thường gặp: đọc mà không kiểm tra `if (!stream)`, trộn `>>`
với `getline` (`>>` để lại `\n` trong buffer), và quên rằng `getline` vẫn
thành công trên dòng cuối không có `\n` kết thúc.
"""

# ---- practice cppi-p10-exceptions --------------------------------------------------
R_VALIDATE_LINE = r'''#include <stdexcept>
#include <string>

int validate_line(const std::string& line) {
    if (line.empty()) throw std::invalid_argument("empty line");
    if (line[0] == '-') throw std::invalid_argument("negative line: " + line);
    int value = 0;
    for (char c : line) {
        if (c < '0' || c > '9') throw std::invalid_argument("non-digit: " + line);
        value = value * 10 + (c - '0');
    }
    if (value > 100) throw std::out_of_range("value too large: " + line);
    return value;
}
'''

W_VALIDATE_LINE = r'''#include <stdexcept>
#include <string>

int validate_line(const std::string& line) {
    if (line.empty()) throw std::invalid_argument("empty line");
    if (line[0] == '-') throw std::invalid_argument("negative line: " + line);
    int value = 0;
    for (char c : line) {
        if (c < '0' || c > '9') throw std::invalid_argument("non-digit: " + line);
        value = value * 10 + (c - '0');
    }
    // BUG: silently clamps instead of throwing out_of_range
    if (value > 100) return 100;
    return value;
}
'''

R_RECORDS = r'''#include <sstream>
#include <string>
#include <vector>

struct Record {
    std::string name;
    int quantity;
};

std::vector<Record> parse_records(const std::string& content) {
    std::vector<Record> out;
    std::istringstream in{content};
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        auto sep = line.find(':');
        if (sep == std::string::npos) continue;   // malformed: skip
        std::string name = line.substr(0, sep);
        std::string rest = line.substr(sep + 1);
        try {
            out.push_back({name, std::stoi(rest)});
        } catch (const std::exception&) {
            // malformed quantity: skip line
        }
    }
    return out;
}
'''

W_RECORDS = r'''#include <sstream>
#include <string>
#include <vector>

struct Record {
    std::string name;
    int quantity;
};

std::vector<Record> parse_records(const std::string& content) {
    std::vector<Record> out;
    std::istringstream in{content};
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        auto sep = line.find(':');
        if (sep == std::string::npos) continue;
        std::string name = line.substr(0, sep);
        std::string rest = line.substr(sep + 1);
        // BUG: unguarded stoi — a bad quantity aborts the whole parse
        out.push_back({name, std::stoi(rest)});
    }
    return out;
}
'''

# ---- checkpoint: field-aware exception -------------------------------------------------
R_PARSE_CONFIG = r'''#include <stdexcept>
#include <string>

class ConfigError : public std::runtime_error {
public:
    ConfigError(std::string line_no, std::string message)
        : std::runtime_error{"line " + line_no + ": " + message},
          line_no_{std::move(line_no)} {}

    const std::string& line_no() const noexcept { return line_no_; }

private:
    std::string line_no_;
};

int parse_config_value(const std::string& content) {
    int found = -1;
    int line_no = 0;
    std::size_t start = 0;
    while (start <= content.size()) {
        std::size_t end = content.find('\n', start);
        if (end == std::string::npos) end = content.size();
        std::string line = content.substr(start, end - start);
        ++line_no;
        if (line.rfind("value=", 0) == 0) {
            std::string rest = line.substr(6);
            if (rest.empty() || rest.find_first_not_of("0123456789") != std::string::npos) {
                throw ConfigError{std::to_string(line_no), "bad value: " + rest};
            }
            found = std::stoi(rest);
        }
        if (end == content.size()) break;
        start = end + 1;
    }
    if (found < 0) throw ConfigError{"?", "missing value= line"};
    return found;
}
'''

W_PARSE_CONFIG = r'''#include <stdexcept>
#include <string>

class ConfigError : public std::runtime_error {
public:
    ConfigError(std::string line_no, std::string message)
        : std::runtime_error{"line " + line_no + ": " + message},
          line_no_{std::move(line_no)} {}

    const std::string& line_no() const noexcept { return line_no_; }

private:
    std::string line_no_;
};

int parse_config_value(const std::string& content) {
    int found = -1;
    std::size_t start = 0;
    while (start <= content.size()) {
        std::size_t end = content.find('\n', start);
        if (end == std::string::npos) end = content.size();
        std::string line = content.substr(start, end - start);
        if (line.rfind("value=", 0) == 0) {
            std::string rest = line.substr(6);
            // BUG: reports line "0" instead of the real line number
            if (rest.empty() || rest.find_first_not_of("0123456789") != std::string::npos) {
                throw ConfigError{"0", "bad value: " + rest};
            }
            found = std::stoi(rest);
        }
        if (end == content.size()) break;
        start = end + 1;
    }
    if (found < 0) throw ConfigError{"?", "missing value= line"};
    return found;
}
'''

# ---- challenges ----------------------------------------------------------------------
CH_VALIDATE = challenge(
    "cppi-m10-validate-line",
    "Throw the right exception type",
    "Implement `int validate_line(const std::string& line)` interpreting the line as a non-negative integer: throw `std::invalid_argument` for an empty line, a leading '-', or any non-digit; throw `std::out_of_range` when the parsed value exceeds 100; otherwise return the value.",
    r'''#include <stdexcept>
#include <string>
#include <iostream>

// int validate_line(const std::string& line)
''',
    [
        ("valid", 'CHECK_EQ(validate_line("42"), 42);\nCHECK_EQ(validate_line("100"), 100);', "Boundary: 100 itself is legal."),
        ("invalid-arg", 'bool threw = false;\ntry { validate_line("-5"); } catch (const std::invalid_argument&) { threw = true; }\nCHECK(threw);', "A leading '-' is invalid_argument, not out_of_range."),
        ("out-of-range", 'bool threw = false;\ntry { validate_line("101"); } catch (const std::out_of_range&) { threw = true; }\nCHECK(threw);', "101 parses but leaves the domain: out_of_range."),
        ("exact-type", 'bool wrong = false;\ntry { validate_line("abc"); } catch (const std::out_of_range&) { wrong = true; } catch (const std::invalid_argument&) { wrong = false; }\nCHECK(!wrong);', "Type discipline: 'abc' must land in invalid_argument."),
    ],
    level="independent",
)

CH_ERROR_LINES = challenge(
    "cppi-m10-error-lines",
    "Filter error lines from file content",
    "Implement `std::string error_lines(const std::string& content)` that treats `content` as a text file (lines separated by \\n) and returns only the lines starting with `ERROR `, each followed by \\n. Use `std::istringstream` + `std::getline`.",
    r'''#include <sstream>
#include <string>
#include <iostream>

// std::string error_lines(const std::string& content)
''',
    [
        ("mixed", 'std::string out = error_lines(std::string{"INFO ok\\nERROR bad\\nINFO fine\\nERROR worse\\n"});\nCHECK(out == std::string{"ERROR bad\\nERROR worse\\n"});', "Keep order; drop everything not starting with the prefix."),
        ("none", 'CHECK(error_lines(std::string{"INFO a\\n"}).empty());', "No matches: empty output."),
        ("prefix-only", 'CHECK(error_lines(std::string{"XERROR no\\nERROR yes\\n"}) == std::string{"ERROR yes\\n"});', "The prefix must start at position 0."),
        ("no-trailing-newline", 'CHECK(error_lines(std::string{"a\\nERROR last"}) == std::string{"ERROR last\\n"});', "The final line may lack \\n — getline still yields it."),
    ],
    level="guided",
)

CH_RECORDS = challenge(
    "cppi-m10-parse-records",
    "Parse records with per-line error recovery",
    "Implement `std::vector<Record> parse_records(const std::string& content)` where each line is `name:quantity`. Skip blank lines and lines without ':'; parse the quantity with `std::stoi` guarded by try/catch so one malformed line never aborts the parse of the rest. `Record` is `{std::string name; int quantity;}`.",
    r'''#include <sstream>
#include <string>
#include <vector>
#include <iostream>

struct Record {
    std::string name;
    int quantity;
};

// std::vector<Record> parse_records(const std::string& content)
''',
    [
        ("happy-path", 'auto r = parse_records(std::string{"apple:3\\npear:1\\n"});\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0].name, std::string("apple"));\nCHECK_EQ(r[1].quantity, 1);', "Two clean lines, two records."),
        ("skip-malformed", 'auto r = parse_records(std::string{"good:2\\nbadline\\nalso:five\\nlast:4\\n"});\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0].name, std::string("good"));\nCHECK_EQ(r[1].name, std::string("last"));', "No ':' → skip; non-numeric quantity → skip, keep going."),
        ("blank-lines", 'auto r = parse_records(std::string{"\\nok:1\\n\\n"});\nCHECK_EQ(r.size(), 1);', "Blank lines are skipped, not errors."),
    ],
    level="combination",
)

# ---- checkpoint -----------------------------------------------------------------------
CP_CONFIG = challenge(
    "cppi-checkpoint-errors",
    "Checkpoint: Config parser with a field-aware exception",
    "Implement `int parse_config_value(const std::string& content)` scanning lines for one starting with `value=`. Return the parsed non-negative number. Throw a custom `ConfigError` (deriving from `std::runtime_error`, carrying the offending line number as a field, exposed via `line_no()`) when the value is missing, empty, or non-numeric — the exception's `what()` must read `line <N>: <message>` with the REAL line number (1-based).",
    r'''#include <stdexcept>
#include <string>
#include <iostream>

// Define ConfigError, then:
// int parse_config_value(const std::string& content)
''',
    [
        ("valid", 'CHECK_EQ(parse_config_value(std::string{"name=app\\nvalue=42\\n"}), 42);', "value=42 on line 2 parses to 42."),
        ("bad-value-line", 'bool threw = false;\nstd::string line_no;\ntry {\n    parse_config_value(std::string{"value=abc\\n"});\n} catch (const ConfigError& e) {\n    threw = true;\n    line_no = e.line_no();\n}\nCHECK(threw);\nCHECK_EQ(line_no, std::string("1"));', "The failure is on line 1 — line_no() must say so."),
        ("line-number-accurate", 'bool threw = false;\nstd::string line_no;\ntry {\n    parse_config_value(std::string{"a=1\\nb=2\\nvalue=\\n"});\n} catch (const ConfigError& e) {\n    threw = true;\n    line_no = e.line_no();\n}\nCHECK(threw);\nCHECK_EQ(line_no, std::string("3"));', "Empty value on line 3 — the field must carry 3, not 0."),
        ("missing-value", 'bool threw = false;\ntry { parse_config_value(std::string{"a=1\\n"}); } catch (const ConfigError&) { threw = true; }\nCHECK(threw);', "No value= line at all is also a ConfigError."),
    ],
    difficulty="intermediate",
)

VI_VALIDATE = vi_challenge(
    "Ném đúng kiểu ngoại lệ",
    "Cài `int validate_line(const std::string& line)` đọc dòng như một số nguyên không âm: ném `std::invalid_argument` cho dòng rỗng, dấu '-' đầu, hoặc ký tự không phải chữ số; ném `std::out_of_range` khi giá trị vượt 100; ngược lại trả giá trị.",
    [
        ("valid", "Biên: chính 100 là hợp lệ."),
        ("invalid-arg", "Dấu '-' đầu là invalid_argument, không phải out_of_range."),
        ("out-of-range", "101 phân tích được nhưng ngoài miền: out_of_range."),
        ("exact-type", "Kỷ luật kiểu: 'abc' phải rơi vào invalid_argument."),
    ],
)

VI_ERROR_LINES = vi_challenge(
    "Lọc dòng lỗi khỏi nội dung tệp",
    "Cài `std::string error_lines(const std::string& content)` coi `content` như một tệp văn bản (các dòng cách nhau bằng \\n) và trả về chỉ những dòng bắt đầu bằng `ERROR `, mỗi dòng theo sau là \\n. Dùng `std::istringstream` + `std::getline`.",
    [
        ("mixed", "Giữ thứ tự; bỏ mọi thứ không bắt đầu bằng tiền tố."),
        ("none", "Không khớp: kết quả rỗng."),
        ("prefix-only", "Tiền tố phải bắt đầu từ vị trí 0."),
        ("no-trailing-newline", "Dòng cuối có thể thiếu \\n — getline vẫn cho ra nó."),
    ],
)

VI_RECORDS = vi_challenge(
    "Phân tích bản ghi với phục hồi lỗi theo dòng",
    "Cài `std::vector<Record> parse_records(const std::string& content)` với mỗi dòng là `name:quantity`. Bỏ qua dòng trống và dòng không có ':'; phân tích số lượng bằng `std::stoi` bọc try/catch để một dòng hỏng không bao giờ hủy việc phân tích các dòng còn lại. `Record` là `{std::string name; int quantity;}`.",
    [
        ("happy-path", "Hai dòng sạch, hai bản ghi."),
        ("skip-malformed", "Không có ':' → bỏ qua; số lượng không phải số → bỏ qua, cứ tiếp tục."),
        ("blank-lines", "Dòng trống được bỏ qua, không phải lỗi."),
    ],
)

VI_CP_CONFIG = vi_challenge(
    "Kiểm tra điểm: Bộ phân tích config với ngoại lệ mang thông tin",
    "Cài `int parse_config_value(const std::string& content)` quét các dòng tìm dòng bắt đầu bằng `value=`. Trả số không âm đã phân tích. Ném `ConfigError` riêng (kế thừa `std::runtime_error`, mang số dòng vi phạm như một field, lộ qua `line_no()`) khi giá trị thiếu, rỗng, hoặc không phải số — `what()` của ngoại lệ phải đọc `line <N>: <message>` với số dòng THẬT (tính từ 1).",
    [
        ("valid", "value=42 ở dòng 2 phân tích thành 42."),
        ("bad-value-line", "Lỗi ở dòng 1 — line_no() phải báo đúng."),
        ("line-number-accurate", "Giá trị rỗng ở dòng 3 — field phải mang 3, không phải 0."),
        ("missing-value", "Hoàn toàn không có dòng value= cũng là ConfigError."),
    ],
)

P1 = [CH_VALIDATE, CH_ERROR_LINES]
VI_P1 = {"cppi-m10-validate-line": VI_VALIDATE, "cppi-m10-error-lines": VI_ERROR_LINES}
P2 = [CH_RECORDS]
VI_P2 = {"cppi-m10-parse-records": VI_RECORDS}

R_ERROR_LINES = r'''#include <sstream>
#include <string>

std::string error_lines(const std::string& content) {
    std::istringstream in{content};
    std::string out;
    std::string line;
    while (std::getline(in, line)) {
        if (line.rfind("ERROR ", 0) == 0) {
            out += line;
            out += '\n';
        }
    }
    return out;
}
'''

W_ERROR_LINES = r'''#include <sstream>
#include <string>

std::string error_lines(const std::string& content) {
    std::istringstream in{content};
    std::string out;
    std::string line;
    while (std::getline(in, line)) {
        // BUG: substring search instead of prefix match
        if (line.find("ERROR ") != std::string::npos) {
            out += line;
            out += '\n';
        }
    }
    return out;
}
'''

# ---- emit -----------------------------------------------------------------------------
write_lesson(
    MOD, "exceptions",
    "Exceptions: throw, try, catch",
    "The standard exception family, catch-by-const-ref, handler ordering, and when exceptions beat return codes.",
    25, L_exceptions_EN,
    "Ngoại lệ: throw, try, catch",
    "Họ ngoại lệ chuẩn, bắt bằng const-ref, thứ tự handler, và khi nào ngoại lệ hơn mã trả về.",
    L_exceptions_VI,
)
write_lesson(
    MOD, "custom-exceptions",
    "Custom Exception Types",
    "Deriving from std::runtime_error, carrying structured data, and designing the type around the handler's decision.",
    20, L_custom_EN,
    "Kiểu ngoại lệ riêng",
    "Kế thừa std::runtime_error, mang dữ liệu có cấu trúc, và thiết kế kiểu xung quanh quyết định của handler.",
    L_custom_VI,
)
write_lesson(
    MOD, "exception-safety",
    "Exception Safety Guarantees",
    "Basic, strong, noexcept; copy-and-swap; and why destructors must never throw.",
    25, L_safety_EN,
    "Các mức đảm bảo exception safety",
    "Basic, strong, noexcept; copy-and-swap; và vì sao destructor không bao giờ được ném.",
    L_safety_VI,
)
write_lesson(
    MOD, "files-streams",
    "File Streams and Content Processing",
    "ifstream/ofstream, getline loops, stream state checks, and a graded string-based parsing pattern.",
    30, L_files_EN,
    "File stream và xử lý nội dung",
    "ifstream/ofstream, vòng getline, kiểm tra trạng thái stream, và pattern phân tích dựa trên chuỗi được chấm điểm.",
    L_files_VI,
)

write_practice(
    MOD, "cppi-p10-exceptions",
    "Exception practice",
    "Type-precise validation and unguarded-stoi recovery.",
    "Luyện ngoại lệ",
    "Kiểm tra dữ liệu chuẩn-xác-kiểu và phục hồi stoi không được bọc.",
    "exceptions", 30, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m10-validate-line", R_VALIDATE_LINE, W_VALIDATE_LINE),
        ("cppi-m10-parse-records", R_RECORDS, W_RECORDS),
    ],
)

write_practice(
    MOD, "cppi-p10-files",
    "File content practice",
    "Line filtering over istringstream content.",
    "Luyện nội dung tệp",
    "Lọc dòng trên nội dung istringstream.",
    "files-streams", 25, "intermediate", [CH_ERROR_LINES], {"cppi-m10-error-lines": VI_ERROR_LINES},
    solutions=[
        ("cppi-m10-error-lines", R_ERROR_LINES, W_ERROR_LINES),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-errors",
    "Checkpoint: A Parser That Explains Itself",
    "A config parser with a custom exception carrying the real line number — structured errors end to end.",
    35,
    r"""
`parse_config_value` is the module's exam: it combines custom exception
design (Module lesson 2), line-based parsing (lesson 4), and accurate
diagnostics.

The three failure modes your parser must distinguish:

1. a `value=` line whose payload is empty or non-numeric →
   `ConfigError` with the real line number
2. no `value=` line at all → `ConfigError` with the missing-value message
3. a valid line → return the number

The line counter is the part that fails casually-written solutions:
increment per line *before* inspecting it, and count the final line even
when the content does not end with `\n`.

Tests assert on `e.line_no()` as a string field — proof that structured
exceptions carry more than a message can.
""",
    "Kiểm tra điểm: Bộ phân tích tự giải thích",
    "Một bộ phân tích config với ngoại lệ riêng mang số dòng thật — lỗi có cấu trúc từ đầu đến cuối.",
    r"""
`parse_config_value` là bài kiểm tra của module: nó kết hợp thiết kế ngoại
lệ riêng (bài 2), phân tích theo dòng (bài 4), và chẩn đoán chính xác.

Ba kiểu thất bại bộ phân tích của bạn phải phân biệt:

1. dòng `value=` có phần giá trị rỗng hoặc không phải số → `ConfigError`
   với số dòng thật
2. không có dòng `value=` nào → `ConfigError` với thông báo missing-value
3. dòng hợp lệ → trả về số

Bộ đếm dòng là phần khiến các giải pháp viết vội thất bại: tăng theo dòng
*trước* khi kiểm tra dòng đó, và đếm cả dòng cuối ngay cả khi nội dung
không kết thúc bằng `\n`.

Các test khẳng định trên `e.line_no()` như một field chuỗi — bằng chứng
rằng ngoại lệ có cấu trúc mang được nhiều hơn một thông điệp.
""",
    CP_CONFIG, VI_CP_CONFIG,
    solution=R_PARSE_CONFIG, wrong=W_PARSE_CONFIG,
)

write_module(
    MOD,
    "Error Handling and File I/O",
    "Failure as a first-class citizen: the standard exception family, custom types with data, safety guarantees, and line-oriented content processing.",
    "Xử lý lỗi và File I/O",
    "Thất bại là công dân hạng nhất: họ ngoại lệ chuẩn, kiểu riêng có dữ liệu, các mức đảm bảo an toàn, và xử lý nội dung theo dòng.",
    ["exceptions", "custom-exceptions", "exception-safety", "files-streams", "advanced-checkpoint-errors"],
    ["cppi-p10-exceptions", "cppi-p10-files"],
)
print("module 10 emitted")
