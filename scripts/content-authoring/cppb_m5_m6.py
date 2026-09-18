#!/usr/bin/env python3
"""C++ Beginner — module 5 (functions) and module 6 (strings)."""
from cppb import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 5: functions ============================
M5 = "functions"

L5A = "defining-and-calling"
L5B = "parameters-by-value-and-const-ref"
L5C = "overloads-and-decomposition"
L5D = "checkpoint-functions"

write_module(
    M5,
    "Functions",
    "Decompose programs into named, testable pieces: parameters, return values, pass-by-value vs const reference, overloads.",
    "Hàm",
    "Phân rã chương trình thành những mảnh có tên, có thể kiểm thử: tham số, giá trị trả về, truyền theo giá trị với tham chiếu const, nạp chồng hàm.",
    [L5A, L5B, L5C, L5D],
    ["m5-func-practice", "m5-refactor-practice"],
)

write_lesson(
    M5, L5A,
    "Defining and Calling Functions",
    "The anatomy of a function, why return beats print for graded logic, and single-responsibility sizing.",
    11,
    '''
## The shape

```cpp
double bmi(double weight_kg, double height_m) {
    return weight_kg / (height_m * height_m);
}

int main() {
    std::cout << bmi(70.0, 1.75) << '\\n';   // call with arguments
}
```

Read the first line as a contract: "given a weight and a height, I give back a double". The **parameters** (`weight_kg`, `height_m`) are the function's local variables, initialized from the caller's **arguments**. `return` hands the value back and ends the function immediately.

## Return values, not printed values

Beginners often print inside a function and return nothing:

```cpp
void bad(double w, double h) {
    std::cout << w / (h * h);   // computed, shown... and GONE
}
```

`bad` computed a value nobody can use. A function that **returns** can be printed, stored, tested, and combined:

```cpp
double b = bmi(70, 1.75);
if (b > 25) { /* ... */ }
```

This is also exactly how the platform grades: tests call your functions and check returns. Print for humans; return for programs.

## `void` and early return

`void` means "returns nothing" — a `void` function is a *procedure*, an action (`print_report()`, `program()`). Inside any function, `return;` exits early:

```cpp
void greet(const std::string& name) {
    if (name.empty()) return;   // nothing sensible to do
    std::cout << "Hi, " << name << '\\n';
}
```

## Size discipline

A function does **one thing**, at a size you can read without scrolling. When you write a comment like `// now validate the input` *inside* a function, that comment is usually a new function struggling to be born. Decomposition practice comes in 5C.
''',
    "Định nghĩa và gọi hàm",
    "Giải phẫu một hàm, vì sao return tốt hơn print cho logic có chấm điểm, và kích thước một-trách-nhiệm.",
    '''
## Dạng chuẩn

```cpp
double bmi(double weight_kg, double height_m) {
    return weight_kg / (height_m * height_m);
}

int main() {
    std::cout << bmi(70.0, 1.75) << '\\n';   // gọi với đối số
}
```

Hãy đọc dòng đầu như một bản hợp đồng: "cho tôi cân nặng và chiều cao, tôi trả lại một double". Các **tham số** (`weight_kg`, `height_m`) là biến cục bộ của hàm, được khởi tạo từ **đối số** của người gọi. `return` đưa giá trị trả về và kết thúc hàm ngay lập tức.

## Giá trị trả về, không phải giá trị in ra

Người mới thường in bên trong hàm và không trả về gì cả:

```cpp
void bad(double w, double h) {
    std::cout << w / (h * h);   // tính rồi... hiển thị... và BIẾN MẤT
}
```

`bad` tính một giá trị mà không ai dùng được. Hàm **trả về** giá trị thì có thể in, lưu, kiểm thử, và kết hợp:

```cpp
double b = bmi(70, 1.75);
if (b > 25) { /* ... */ }
```

Đây cũng chính là cách nền tảng chấm điểm: test gọi hàm của bạn và kiểm tra giá trị trả về. In ra cho người xem; return cho chương trình.

## `void` và return sớm

`void` nghĩa là "không trả về gì" — hàm `void` là một *thủ tục*, một hành động (`print_report()`, `program()`). Bên trong bất kỳ hàm nào, `return;` thoát ngay:

```cpp
void greet(const std::string& name) {
    if (name.empty()) return;   // không có gì đáng làm
    std::cout << "Hi, " << name << '\\n';
}
```

## Kỷ luật kích thước

Một hàm làm **một việc**, ở kích thước bạn đọc được mà không cần cuộn. Khi bạn viết comment kiểu `// giờ validate input` *bên trong* một hàm, comment đó thường là một hàm mới đang vùng vẫy để ra đời. Phần luyện phân rã ở bài 5C.
''',
)

write_lesson(
    M5, L5B,
    "Pass by Value, by Reference, and const&",
    "Copies vs aliases: why small values pass by value, why strings and vectors pass by const&, and a first taste of out-parameters.",
    12,
    '''
## Pass by value: a photocopy

```cpp
void double_it(int x) {   // x is a COPY
    x = x * 2;            // changes the copy, not the caller's variable
}

int n = 5;
double_it(n);
std::cout << n;           // still 5
```

By value, the function works on a photocopy. Safe, simple, and free for small things: `int`, `double`, `bool`, `char`.

## Pass by reference: the real thing

A **reference** (`&`) is an alias — another name for the caller's actual variable:

```cpp
void double_it(int& x) {  // x IS the caller's variable
    x = x * 2;
}

int n = 5;
double_it(n);
std::cout << n;           // 10
```

This is how a function hands results *back* through its parameters (an "out-parameter"). It is also how you accidentally modify things — so by default, don't.

## The workhorse: const reference

Reading a big object (a `std::string`, a `std::vector`) by value copies the whole thing — wasteful. Reading it by non-const reference grants write access you do not want. The answer is `const&`:

```cpp
int count_vowels(const std::string& text) {   // no copy, no writes
    int count = 0;
    for (char c : text) {
        char lower = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        if (lower=='a'||lower=='e'||lower=='i'||lower=='o'||lower=='u') ++count;
    }
    return count;
}
```

**The course rule:** small values by value; everything else by `const&`; plain `&` only when the function is *supposed* to modify the caller's object. You will see `const std::string&` in nearly every function signature from now on — it is the professional default.

(References are deep-dived again in module 11, where they meet pointers. Here, treat `&` as "the real variable" and `const&` as "the real variable, read-only".)
''',
    "Truyền theo giá trị, theo tham chiếu, và const&",
    "Bản sao so với bí danh: vì sao giá trị nhỏ truyền theo giá trị, vì sao string và vector truyền theo const&, và lần đầu chạm vào out-parameter.",
    '''
## Truyền theo giá trị: một bản photocopy

```cpp
void double_it(int x) {   // x là một BẢN SAO
    x = x * 2;            // sửa bản sao, không sửa biến của người gọi
}

int n = 5;
double_it(n);
std::cout << n;           // vẫn là 5
```

Theo giá trị, hàm làm việc trên một bản photocopy. An toàn, đơn giản, và miễn phí với thứ nhỏ: `int`, `double`, `bool`, `char`.

## Truyền theo tham chiếu: bản gốc

Một **tham chiếu** (`&`) là một bí danh — một tên khác cho biến thật của người gọi:

```cpp
void double_it(int& x) {  // x CHÍNH LÀ biến của người gọi
    x = x * 2;
}

int n = 5;
double_it(n);
std::cout << n;           // 10
```

Đây là cách một hàm đưa kết quả *trả ngược lại* qua tham số ("out-parameter"). Cũng là cách bạn vô tình sửa thứ không nên sửa — nên mặc định, đừng.

## Lao động chính: tham chiếu const

Đọc một đối tượng lớn (một `std::string`, một `std::vector`) theo giá trị nghĩa là sao chép toàn bộ — lãng phí. Đọc theo tham chiếu không-const lại trao quyền ghi mà bạn không muốn. Câu trả lời là `const&`:

```cpp
int count_vowels(const std::string& text) {   // không sao chép, không ghi
    int count = 0;
    for (char c : text) {
        char lower = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        if (lower=='a'||lower=='e'||lower=='i'||lower=='o'||lower=='u') ++count;
    }
    return count;
}
```

**Quy tắc của khóa học:** giá trị nhỏ truyền theo giá trị; mọi thứ khác truyền theo `const&`; `&` trần chỉ khi hàm *được thiết kế* để sửa biến của người gọi. Từ giờ bạn sẽ thấy `const std::string&` trong gần mọi chữ ký hàm — đó là mặc định chuyên nghiệp.

(Tham chiếu sẽ được đào sâu lại ở module 11, nơi chúng gặp con trỏ. Ở đây, hãy xem `&` là "biến thật" và `const&` là "biến thật, chỉ đọc".)
''',
)

write_lesson(
    M5, L5C,
    "Overloads and Decomposition",
    "Same name, different parameters; and the refactoring skill of splitting a monolithic program into testable functions.",
    11,
    '''
## Overloading: one name, several contracts

```cpp
int area(int side);                      // square
int area(int width, int height);         // rectangle
double area(double radius);              // circle
```

Three `area` functions coexist; the compiler picks by **parameter types and count** (the *signature*). Return type alone cannot distinguish overloads. Overloading is everywhere in the standard library — it is how one name `std::to_string` serves int, double, and more.

Use overloads when the *idea* is genuinely one thing measured differently. If the bodies share logic, have the thin overloads call the real implementation rather than copy-pasting it.

## Decomposition: the refactoring move

Start (a typical beginner monolith):

```cpp
int main() {
    // read 3 exam scores, print average, highest, and pass/fail
    // ... 40 lines of tangled std::cout and loops ...
}
```

Refactored:

```cpp
double average(const std::vector<int>& scores);
int highest(const std::vector<int>& scores);
bool passed(double avg);
```

`main` becomes four readable lines; each function is independently testable (the platform's tests can call `average({9,7,10})` directly); and each one is *reusable* by the next feature. That last point is the quiet superpower: decomposed code is the only kind that grows gracefully.

## The naming test

If you cannot name a function without "and" (`read_and_validate_and_sum`), it is two functions. Split at the "and".
''',
    "Nạp chồng và phân rã",
    "Cùng tên, tham số khác nhau; và kỹ năng refactor tách một chương trình nguyên khối thành các hàm có thể kiểm thử.",
    '''
## Nạp chồng: một tên, nhiều bản hợp đồng

```cpp
int area(int side);                      // hình vuông
int area(int width, int height);         // hình chữ nhật
double area(double radius);              // hình tròn
```

Ba hàm `area` cùng tồn tại; compiler chọn theo **kiểu và số lượng tham số** (theo *signature*). Riêng kiểu trả về không đủ để phân biệt các overload. Nạp chồng có ở khắp nơi trong thư viện chuẩn — đó là cách một cái tên `std::to_string` phục vụ int, double và hơn thế nữa.

Dùng overload khi *ý tưởng* thực sự là một thứ được đo theo cách khác. Nếu các phần thân chia sẻ logic, hãy để các overload mỏng gọi về phần cài đặt thật thay vì copy-paste.

## Phân rã: nước đi refactor

Điểm bắt đầu (một "nguyên khối" người mới điển hình):

```cpp
int main() {
    // đọc 3 điểm thi, in trung bình, cao nhất, và đậu/rớt
    // ... 40 dòng std::cout và vòng lặp rối bời ...
}
```

Sau khi refactor:

```cpp
double average(const std::vector<int>& scores);
int highest(const std::vector<int>& scores);
bool passed(double avg);
```

`main` còn lại bốn dòng dễ đọc; mỗi hàm có thể kiểm thử độc lập (test của nền tảng có thể gọi thẳng `average({9,7,10})`); và mỗi hàm *dùng lại được* cho tính năng kế tiếp. Điểm cuối cùng đó mới là siêu năng lực thầm lặng: chỉ code đã phân rã mới lớn lên một cách duyên dáng.

## Bài test đặt tên

Nếu bạn không đặt được tên hàm mà không có chữ "và" (`doc_va_validate_va_tinh_tong`), thì đó là hai hàm. Hãy tách ngay tại chữ "và".
''',
)

# ---- Module 5 checkpoint ----
write_checkpoint(
    M5, L5D,
    "Checkpoint: Functions",
    "One graded challenge: decompose a word problem into the exact functions the tests call.",
    15,
    '''
**Checkpoint — functions.** Pass the graded challenge below to finish the module.

The tests dictate the decomposition: you must provide exactly the named functions with exactly the right parameter styles (`const&` where big data flows in). Signatures are the contract.
''',
    "Checkpoint: Hàm",
    "Một challenge có chấm: phân rã một bài toán thực tế thành đúng các hàm mà test gọi tới.",
    '''
**Checkpoint — hàm.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Chính test quy định cách phân rã: bạn phải cung cấp đúng các hàm được gọi tên, với đúng kiểu tham số (`const&` ở nơi dữ liệu lớn chảy vào). Chữ ký hàm là bản hợp đồng.
''',
    challenge(
        "cpp5-check-textstats",
        "Text Stats Functions",
        "Implement three functions over a sentence: `word_count(text)` (space-separated words, non-empty), `longest_word(text)` (first longest on ties), and `contains_digit(text)` (true if any character is a digit).",
        "#include <string>\\n\\nint word_count(const std::string& text) {\\n    // TODO\\n}\\nstd::string longest_word(const std::string& text) {\\n    // TODO\\n}\\nbool contains_digit(const std::string& text) {\\n    // TODO\\n}",
        [
            ("word count", "CHECK_EQ(word_count(std::string{\"the quick brown fox\"}), 4);", "Count space-separated words."),
            ("longest", "CHECK(longest_word(std::string{\"I love linked lists\"}) == std::string{\"linked\"});", "First of the longest words wins (lists/linked are 6; linked is first)."),
            ("digit detection", "CHECK(contains_digit(std::string{\"room 42\"}));", "std::isdigit on each char (cast to unsigned char first)."),
            ("no digits", "CHECK(!contains_digit(std::string{\"no digits here\"}));", "No digit means false."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Các hàm thống kê văn bản",
        "Cài đặt ba hàm trên một câu: `word_count(text)` (các từ ngăn cách bởi dấu cách, khác rỗng), `longest_word(text)` (từ dài nhất đầu tiên khi bằng nhau), và `contains_digit(text)` (true nếu có ký tự chữ số nào).",
        [("đếm từ", "Đếm các từ ngăn cách bởi dấu cách."), ("từ dài nhất", "Từ dài nhất xuất hiện trước sẽ thắng (lists/linked đều 6; linked ra trước)."), ("phát hiện chữ số", "std::isdigit cho từng ký tự (ép sang unsigned char trước)."), ("không có chữ số", "Không có chữ số nghĩa là false.")],
    ),
    solution="#include <string>\\n#include <sstream>\\nint word_count(const std::string& text) {\\n    std::istringstream in(text);\\n    std::string w;\\n    int n = 0;\\n    while (in >> w) ++n;\\n    return n;\\n}\\nstd::string longest_word(const std::string& text) {\\n    std::istringstream in(text);\\n    std::string w, best;\\n    while (in >> w) if (w.size() > best.size()) best = w;\\n    return best;\\n}\\nbool contains_digit(const std::string& text) {\\n    for (char c : text) if (std::isdigit(static_cast<unsigned char>(c))) return true;\\n    return false;\\n}",
    wrong="#include <string>\\n#include <sstream>\\nint word_count(const std::string& text) {\\n    std::istringstream in(text);\\n    std::string w;\\n    int n = 0;\\n    while (in >> w) ++n;\\n    return n;\\n}\\nstd::string longest_word(const std::string& text) {\\n    std::istringstream in(text);\\n    std::string w, best;\\n    while (in >> w) if (w.size() >= best.size()) best = w;\\n    return best;\\n}\\nbool contains_digit(const std::string& text) {\\n    for (char c : text) if (std::isdigit(static_cast<unsigned char>(c))) return true;\\n    return false;\\n}",
)

# ---- Module 5 practice sets ----
write_practice(
    M5, "m5-func-practice",
    "Functions Practice: Contracts",
    "Write functions to spec: pure computations, a const& reader, and one out-parameter fix.",
    "Luyện Hàm: Bản hợp đồng",
    "Viết hàm đúng đặc tả: tính toán thuần, một hàm đọc với const&, và một bài sửa out-parameter.",
    L5A, 25, "beginner",
    [
        challenge(
            "cpp5-clamp",
            "Clamp",
            "Implement `clamp(value, low, high)`: value if in range, low if below, high if above. One return-statement version exists with the conditional operator — find it if you like.",
            "int clamp(int value, int low, int high) {\\n    // TODO\\n}",
            [("inside", "CHECK_EQ(clamp(5, 1, 10), 5);", "In range returns itself."), ("below", "CHECK_EQ(clamp(-3, 1, 10), 1);", "Below low returns low."), ("above", "CHECK_EQ(clamp(99, 1, 10), 10);", "Above high returns high.")],
            level="guided",
        ),
    ],
    {"cpp5-clamp": vi_challenge("Clamp", "Cài đặt `clamp(value, low, high)`: trả value nếu trong khoảng, low nếu thấp hơn, high nếu cao hơn. Có một bản một-lệnh dùng toán tử điều kiện — thử tìm xem.", [("trong khoảng", "Trong khoảng trả về chính nó."), ("thấp hơn", "Thấp hơn low trả về low."), ("cao hơn", "Cao hơn high trả về high.")])},
    solutions=[
        ("cpp5-clamp", "int clamp(int value, int low, int high) {\\n    if (value < low) return low;\\n    if (value > high) return high;\\n    return value;\\n}", "int clamp(int value, int low, int high) {\\n    if (value < low) return high;\\n    if (value > high) return low;\\n    return value;\\n}"),
    ],
)

write_practice(
    M5, "m5-refactor-practice",
    "Refactor Practice: Split the Monolith",
    "Take a working-but-tangled program description and give it the function shapes tests can call.",
    "Luyện Refactor: Tách nguyên khối",
    "Nhận một mô tả chương trình chạy được nhưng rối, và chuyển nó thành các hình dạng hàm mà test có thể gọi.",
    L5C, 25, "beginner",
    [
        challenge(
            "cpp5-min-max-avg",
            "Three Stats, Three Functions",
            "Implement `min_of`, `max_of` (both return int; empty vector returns 0), and `avg_of` (double, empty returns 0.0) over a vector of ints.",
            "#include <vector>\\n\\nint min_of(const std::vector<int>& v) {\\n    // TODO\\n}\\nint max_of(const std::vector<int>& v) {\\n    // TODO\\n}\\ndouble avg_of(const std::vector<int>& v) {\\n    // TODO\\n}",
            [("min", "CHECK_EQ(min_of({4, 2, 9, 7}), 2);", "Track the smallest while visiting once."), ("max", "CHECK_EQ(max_of({4, 2, 9, 7}), 9);", "Track the largest while visiting once."), ("avg", "CHECK_NEAR(avg_of({4, 2, 9}), 5.0, 0.001);", "Return a real division as double."), ("empty", "CHECK_EQ(max_of({}), 0);", "Empty input: 0 (and avg 0.0).")],
            level="independent",
        ),
    ],
    {"cpp5-min-max-avg": vi_challenge("Ba số liệu, ba hàm", "Cài đặt `min_of`, `max_of` (cả hai trả int; vector rỗng trả 0), và `avg_of` (double, rỗng trả 0.0) trên một vector các số nguyên.", [("min", "Theo dõi phần tử nhỏ nhất trong một lượt duyệt."), ("max", "Theo dõi phần tử lớn nhất trong một lượt duyệt."), ("avg", "Trả về phép chia số thực dưới dạng double."), ("rỗng", "Input rỗng: 0 (và avg 0.0).")])},
    solutions=[
        ("cpp5-min-max-avg", "#include <vector>\\nint min_of(const std::vector<int>& v) {\\n    if (v.empty()) return 0;\\n    int m = v[0];\\n    for (int x : v) if (x < m) m = x;\\n    return m;\\n}\\nint max_of(const std::vector<int>& v) {\\n    if (v.empty()) return 0;\\n    int m = v[0];\\n    for (int x : v) if (x > m) m = x;\\n    return m;\\n}\\ndouble avg_of(const std::vector<int>& v) {\\n    if (v.empty()) return 0.0;\\n    int t = 0; for (int x : v) t += x;\\n    return static_cast<double>(t) / v.size();\\n}", "#include <vector>\\nint min_of(const std::vector<int>& v) {\\n    if (v.empty()) return 0;\\n    int m = v[0];\\n    for (int x : v) if (x < m) m = x;\\n    return m;\\n}\\nint max_of(const std::vector<int>& v) {\\n    if (v.empty()) return 0;\\n    int m = v[0];\\n    for (int x : v) if (x > m) m = x;\\n    return m;\\n}\\ndouble avg_of(const std::vector<int>& v) {\\n    if (v.empty()) return 0.0;\\n    int t = 0; for (int x : v) t += x;\\n    return static_cast<double>(t) / v.size();\\n}\\n// extra helper that changes nothing"),
    ],
)

# ============================ MODULE 6: strings ============================
M6 = "strings"

L6A = "string-operations"
L6B = "parsing-with-stringstream"
L6C = "checkpoint-strings"

write_module(
    M6,
    "Strings & Text Processing",
    "std::string as the one string type: indexing, searching, building, and parsing structured text with stringstream.",
    "Chuỗi & Xử lý văn bản",
    "std::string là kiểu chuỗi duy nhất: đánh chỉ số, tìm kiếm, dựng chuỗi, và phân tích văn bản có cấu trúc bằng stringstream.",
    [L6A, L6B, L6C],
    ["m6-string-practice", "m6-parse-practice"],
)

write_lesson(
    M6, L6A,
    "std::string Operations",
    "Length, indexing with .at, substr, find, concatenation, comparison — and why .at beats [] while learning.",
    11,
    '''
```cpp
#include <string>

std::string s = "Code Journey";
```

## The everyday operations

```cpp
s.size()                 // 12  (length() is the same thing)
s[0]                     // 'C' — NO bounds checking
s.at(0)                  // 'C' — throws std::out_of_range if invalid
s.substr(5, 7)           // "Journey" — start index, count
s.find("Jour")           // 5 — index, or std::string::npos if absent
s + "!"                  // concatenation → "Code Journey!"
s == "Code Journey"      // true — value comparison, not pointer comparison
```

## `.at()` vs `[]` while you are learning

`[]` on a bad index is **undefined behavior** — it may print garbage, crash, or silently corrupt memory. `.at()` throws a catchable exception. In this course's exercises, prefer `.at()`: when you inevitably go one step too far, you get a clear error instead of a mystery. (`.at` does cost a bounds check; professionals drop to `[]` in hot loops once logic is proven — and say so in review.)

`std::string::npos` is the special "not found" value; compare with `==`, never print it.

## Characters

Indexing yields a `char`. Useful checks: `std::isdigit`, `std::isalpha`, `std::isspace`, `std::toupper`, `std::tolower` — all take an `int`; pass `static_cast<unsigned char>(c)` (a plain `char` can be negative and that is UB). Ugly but correct — the boilerplate does it, and now you know why.

## Building strings

Prefer `+`/`+=` for small builds; for assembling many pieces (and numbers), `std::ostringstream` (next lesson) reads better than a pile of `to_string` calls.
''',
    "Các phép toán trên std::string",
    "Độ dài, đánh chỉ số với .at, substr, find, nối chuỗi, so sánh — và vì sao .at an toàn hơn [] trong lúc học.",
    '''
```cpp
#include <string>

std::string s = "Code Journey";
```

## Các phép toán hằng ngày

```cpp
s.size()                 // 12  (length() cũng là nó)
s[0]                     // 'C' — KHÔNG kiểm tra biên
s.at(0)                  // 'C' — ném std::out_of_range nếu sai
s.substr(5, 7)           // "Journey" — chỉ số bắt đầu, số ký tự
s.find("Jour")           // 5 — chỉ số, hoặc std::string::npos nếu không có
s + "!"                  // nối chuỗi → "Code Journey!"
s == "Code Journey"      // true — so sánh giá trị, không phải so sánh con trỏ
```

## `.at()` với `[]` trong lúc bạn còn học

`[]` với chỉ số sai là **hành vi không xác định** — có thể in rác, crash, hoặc âm thầm hỏng bộ nhớ. `.at()` ném một exception có thể bắt được. Trong bài tập của khóa này, hãy ưu tiên `.at()`: khi bạn chắc chắn sẽ đi một bước quá xa, bạn nhận một lỗi rõ ràng thay vì một vụ án không có hung thủ. (`.at` tốn một lần kiểm tra biên; lập trình viên chuyên nghiệp chuyển về `[]` trong vòng lặp nóng khi logic đã được chứng minh — và nói rõ điều đó khi review.)

`std::string::npos` là giá trị đặc biệt "không tìm thấy"; so sánh bằng `==`, đừng bao giờ in nó ra.

## Ký tự (char)

Đánh chỉ số cho ra một `char`. Các phép kiểm tra hữu ích: `std::isdigit`, `std::isalpha`, `std::isspace`, `std::toupper`, `std::tolower` — tất cả nhận `int`; hãy truyền `static_cast<unsigned char>(c)` (một `char` trần có thể âm và điều đó là UB). Nhìn không đẹp nhưng đúng — boilerplate làm vậy, và giờ bạn biết lý do.

## Dựng chuỗi

Dùng `+`/`+=` cho việc dựng nhỏ; khi ghép nhiều mảnh (và cả số), `std::ostringstream` (bài sau) dễ đọc hơn một đống `to_string`.
''',
)

write_lesson(
    M6, L6B,
    "Parsing with stringstream",
    "Break structured text into typed data: >> for whitespace-separated fields, getline for lines, and the CSV loop.",
    11,
    '''
## The string as a stream

```cpp
#include <sstream>

std::string record = "Linh 20 8.5";
std::istringstream in(record);

std::string name;
int age = 0;
double gpa = 0.0;
in >> name >> age >> gpa;    // "Linh", 20, 8.5
```

`istringstream` treats a string like `std::cin`. `>>` skips whitespace and converts — an age arrives as a real `int`, not text. Reading past the end leaves variables untouched and fails the stream: check with `if (in >> x)` or `if (!in) ` after reading.

## Line by line: getline

```cpp
std::string line;
while (std::getline(in, line)) {   // in can be a file stream too (module 13)
    // process one whole line, spaces included
}
```

`getline` reads to the newline and strips it. Mixing `>>` and `getline` on the same stream needs care (`>>` leaves the newline behind — `in.ignore()` clears it) — this mixing is the single most common stream bug; the exercises exercise it deliberately.

## The mini-CSV pattern

```cpp
// line = "pen,2.5,120"
std::istringstream row{line};
std::string name, price_s, qty_s;
std::getline(row, name, ',');          // "pen"
std::getline(row, price_s, ',');       // "2.5"
std::getline(row, qty_s);              // "120"
double price = std::stod(price_s);     // convert text -> double
int qty = std::stoi(qty_s);
```

`std::getline(stream, out, ',')` reads up to a delimiter. `std::stoi`/`std::stod` convert text to numbers (they throw on garbage — module 14 handles that properly). This pattern is exactly your module 13 file work and the capstone's storage format, in miniature.

## Why not hand-rolled index arithmetic?

Because the stream tools express *intent* ("read a word", "read to comma") while index math expresses *mechanics* — and mechanics is where off-by-one bugs breed. Use the tools.
''',
    "Phân tích cú pháp với stringstream",
    "Tách văn bản có cấu trúc thành dữ liệu có kiểu: >> cho các trường ngăn cách bởi khoảng trắng, getline cho từng dòng, và vòng lặp CSV.",
    '''
## Chuỗi như một stream

```cpp
#include <sstream>

std::string record = "Linh 20 8.5";
std::istringstream in(record);

std::string name;
int age = 0;
double gpa = 0.0;
in >> name >> age >> gpa;    // "Linh", 20, 8.5
```

`istringstream` biến một chuỗi thành `std::cin`. `>>` bỏ qua khoảng trắng và chuyển kiểu — tuổi đến dưới dạng `int` thật, không phải text. Đọc quá cuối sẽ giữ nguyên biến và làm stream thất bại: kiểm tra bằng `if (in >> x)` hoặc `if (!in)` sau khi đọc.

## Từng dòng một: getline

```cpp
std::string line;
while (std::getline(in, line)) {   // in cũng có thể là file stream (module 13)
    // xử lý nguyên một dòng, kể cả dấu cách
}
```

`getline` đọc đến dấu xuống dòng và bỏ nó đi. Trộn `>>` và `getline` trên cùng một stream cần cẩn thận (`>>` để lại ký tự xuống dòng — `in.ignore()` dọn nó) — chính việc trộn này là bug stream phổ biến nhất; các bài tập sẽ chủ động cho bạn gặp nó.

## Mẫu mini-CSV

```cpp
// line = "pen,2.5,120"
std::istringstream row{line};
std::string name, price_s, qty_s;
std::getline(row, name, ',');          // "pen"
std::getline(row, price_s, ',');       // "2.5"
std::getline(row, qty_s);              // "120"
double price = std::stod(price_s);     // đổi text -> double
int qty = std::stoi(qty_s);
```

`std::getline(stream, out, ',')` đọc đến ký tự phân cách. `std::stoi`/`std::stod` đổi text thành số (chúng ném exception khi gặp rác — module 14 sẽ xử lý đúng cách). Mẫu này chính là phần làm việc với file ở module 13 và định dạng lưu trữ của capstone, ở phiên bản thu nhỏ.

## Vì sao không tự viết phép tính chỉ số?

Vì các công cụ stream diễn đạt *ý định* ("đọc một từ", "đọc đến dấu phẩy") trong khi phép tính chỉ số diễn đạt *cơ chế* — và cơ chế là nơi các bug off-by-one sinh sôi. Hãy dùng công cụ.
''',
)

# ---- Module 6 checkpoint ----
write_checkpoint(
    M6, L6C,
    "Checkpoint: Strings",
    "One graded challenge: parse CSV records into typed data with the stream tools.",
    15,
    '''
**Checkpoint — strings.** Pass the graded challenge below to finish the module.

You will parse `name,price,qty` records with the exact mini-CSV pattern from lesson 6B — getline with a delimiter, stoi/stod for conversion.
''',
    "Checkpoint: Chuỗi",
    "Một challenge có chấm: phân tích các bản ghi CSV thành dữ liệu có kiểu bằng công cụ stream.",
    '''
**Checkpoint — chuỗi.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Bạn sẽ phân tích các bản ghi `name,price,qty` bằng đúng mẫu mini-CSV ở bài 6B — getline với ký tự phân cách, stoi/stod để chuyển kiểu.
''',
    challenge(
        "cpp6-check-csv-parse",
        "Parse a CSV Record",
        "Implement `item_price(record)`, `item_qty(record)`, and `item_name(record)` for records shaped `\"pen,2.5,120\"` — name is text, price a double, qty an int.",
        "#include <string>\\n\\nstd::string item_name(const std::string& record) {\\n    // TODO\\n}\\ndouble item_price(const std::string& record) {\\n    // TODO\\n}\\nint item_qty(const std::string& record) {\\n    // TODO\\n}",
        [
            ("name", "CHECK(item_name(std::string{\"pen,2.5,120\"}) == std::string{\"pen\"});", "First comma-separated field."),
            ("price", "CHECK_NEAR(item_price(std::string{\"pen,2.5,120\"}), 2.5, 0.001);", "Second field, converted with std::stod."),
            ("qty", "CHECK_EQ(item_qty(std::string{\"pen,2.5,120\"}), 120);", "Third field, converted with std::stoi."),
            ("spaces in name", "CHECK(item_name(std::string{\"blue pen,2.5,120\"}) == std::string{\"blue pen\"});", "Names contain spaces — >> would stop at the first one; getline(row, out, ',') does not."),
        ],
        level="real-world",
        difficulty="beginner",
    ),
    vi_challenge(
        "Phân tích một bản ghi CSV",
        "Cài đặt `item_price(record)`, `item_qty(record)`, và `item_name(record)` cho các bản ghi dạng `\"pen,2.5,120\"` — name là text, price là double, qty là int.",
        [("tên", "Trường đầu tiên ngăn cách bởi dấu phẩy."), ("giá", "Trường thứ hai, chuyển bằng std::stod."), ("số lượng", "Trường thứ ba, chuyển bằng std::stoi."), ("tên có dấu cách", "Tên có chứa dấu cách — >> sẽ dừng ở dấu cách đầu tiên; getline(row, out, ',') thì không.")],
    ),
    solution="#include <string>\\n#include <sstream>\\nstd::string item_name(const std::string& record) {\\n    std::istringstream row{record};\\n    std::string name;\\n    std::getline(row, name, ',');\\n    return name;\\n}\\ndouble item_price(const std::string& record) {\\n    std::istringstream row{record};\\n    std::string name, price_s, qty_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, price_s, ',');\\n    std::getline(row, qty_s);\\n    return std::stod(price_s);\\n}\\nint item_qty(const std::string& record) {\\n    std::istringstream row{record};\\n    std::string name, price_s, qty_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, price_s, ',');\\n    std::getline(row, qty_s);\\n    return std::stoi(qty_s);\\n}",
    wrong="#include <string>\\n#include <sstream>\\nstd::string item_name(const std::string& record) {\\n    std::istringstream row{record};\\n    std::string name;\\n    row >> name;\\n    return name;\\n}\\ndouble item_price(const std::string& record) {\\n    std::istringstream row{record};\\n    std::string name, price_s, qty_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, price_s, ',');\\n    std::getline(row, qty_s);\\n    return std::stod(price_s);\\n}\\nint item_qty(const std::string& record) {\\n    std::istringstream row{record};\\n    std::string name, price_s, qty_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, price_s, ',');\\n    std::getline(row, qty_s);\\n    return std::stoi(qty_s);\\n}",
)

# ---- Module 6 practice sets ----
write_practice(
    M6, "m6-string-practice",
    "Strings Practice: Text Surgery",
    "Clean usernames, count vowels, reverse words, and a palindrome check.",
    "Luyện Chuỗi: Phẫu thuật văn bản",
    "Làm sạch username, đếm nguyên âm, đảo từ, và kiểm tra palindrome.",
    L6A, 25, "beginner",
    [
        challenge(
            "cpp6-palindrome",
            "Palindrome Check",
            "Implement `is_palindrome(text)`: true when the text reads the same backwards, ignoring case. ('Racecar' is a palindrome; spaces are NOT ignored — keep it simple.)",
            "#include <string>\\n\\nbool is_palindrome(const std::string& text) {\\n    // TODO\\n}",
            [("single", "CHECK(is_palindrome(std::string{\"x\"}));", "One character is trivially a palindrome."), ("racecar", "CHECK(is_palindrome(std::string{\"Racecar\"}));", "Case-insensitive: compare lowered chars."), ("not", "CHECK(!is_palindrome(std::string{\"hello\"}));", "hello reversed is olleh.")],
            level="guided",
        ),
    ],
    {"cpp6-palindrome": vi_challenge("Kiểm tra palindrome", "Cài đặt `is_palindrome(text)`: true khi văn bản đọc xuôi như đọc ngược, không phân biệt hoa/thường. ('Racecar' là palindrome; khoảng trắng KHÔNG được bỏ qua — giữ đơn giản.)", [("một ký tự", "Một ký tự hiển nhiên là palindrome."), ("racecar", "Không phân biệt hoa/thường: so sánh ký tự đã hạ xuống chữ thường."), ("không phải", "hello đảo lại là olleh.")])},
    solutions=[
        ("cpp6-palindrome", "#include <string>\\nbool is_palindrome(const std::string& text) {\\n    std::size_t i = 0, j = text.size();\\n    while (i < j) {\\n        --j;\\n        char a = static_cast<char>(std::tolower(static_cast<unsigned char>(text[i])));\\n        char b = static_cast<char>(std::tolower(static_cast<unsigned char>(text[j])));\\n        if (a != b) return false;\\n        ++i;\\n    }\\n    return true;\\n}", "#include <string>\\nbool is_palindrome(const std::string& text) {\\n    return false;\\n}"),
    ],
)

write_practice(
    M6, "m6-parse-practice",
    "Parsing Practice: Fields and Records",
    "Split key=value pairs, sum a column of CSV lines, and fix the >>-vs-getline mixing bug.",
    "Luyện Parsing: Trường và bản ghi",
    "Tách cặp key=value, tính tổng một cột của các dòng CSV, và sửa bug trộn >> với getline.",
    L6B, 25, "beginner",
    [
        challenge(
            "cpp6-csv-total",
            "Total a CSV Column",
            "Implement `total_second_field(csv)` where csv contains lines `name,number` (e.g. \"pen,2.5\\\\nbook,10\"). Return the sum of all the second fields as a double. Empty input → 0.0.",
            "#include <string>\\n\\ndouble total_second_field(const std::string& csv) {\\n    // TODO: loop lines with getline, parse each with istringstream + getline(',')\\n}",
            [("two rows", "CHECK_NEAR(total_second_field(std::string{\"pen,2.5\\\\nbook,10\"}), 12.5, 0.001);", "2.5 + 10 = 12.5"), ("empty", "CHECK_NEAR(total_second_field(std::string{\"\"}), 0.0, 0.001);", "Nothing to sum: 0.0"), ("one row", "CHECK_NEAR(total_second_field(std::string{\"ink,1.25\"}), 1.25, 0.001);", "A single line sums to itself.")],
            level="real-world",
        ),
    ],
    {"cpp6-csv-total": vi_challenge("Tổng một cột CSV", "Cài đặt `total_second_field(csv)` trong đó csv chứa các dòng `name,number` (ví dụ \"pen,2.5\\\\nbook,10\"). Trả về tổng của tất cả trường thứ hai dưới dạng double. Input rỗng → 0.0.", [("hai dòng", "2.5 + 10 = 12.5"), ("rỗng", "Không có gì để cộng: 0.0"), ("một dòng", "Một dòng đơn lẻ cộng bằng chính nó.")])},
    solutions=[
        ("cpp6-csv-total", "#include <string>\\n#include <sstream>\\ndouble total_second_field(const std::string& csv) {\\n    std::istringstream in{csv};\\n    std::string line;\\n    double total = 0.0;\\n    while (std::getline(in, line)) {\\n        if (line.empty()) continue;\\n        std::istringstream row{line};\\n        std::string name, num_s;\\n        std::getline(row, name, ',');\\n        std::getline(row, num_s);\\n        total += std::stod(num_s);\\n    }\\n    return total;\\n}", "#include <string>\\n#include <sstream>\\ndouble total_second_field(const std::string& csv) {\\n    std::istringstream in{csv};\\n    std::string line;\\n    double total = 0.0;\\n    while (std::getline(in, line)) {\\n        if (line.empty()) continue;\\n        std::istringstream row{line};\\n        std::string name, num_s;\\n        std::getline(row, name, ',');\\n        std::getline(row, num_s);\\n        total += 1.0;\\n    }\\n    return total;\\n}"),
    ],
)

print("modules 5-6 authored")
