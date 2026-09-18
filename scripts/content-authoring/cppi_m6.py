#!/usr/bin/env python3
"""C++ Intermediate — Module 6: iterators-algorithms.

Authoring discipline: every C++ code string (tests, solutions, boilerplate) is
a raw triple-quoted string, so real newlines stay real and C++ "\\n" literals
stay literal. Snippets are self-contained: each test is its own translation
unit (solution.cpp is #included; no cross-test state).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "iterators-algorithms"

# ---- lesson iterators -------------------------------------------------------
L_iterators_EN = r"""
An iterator is the glue between containers and algorithms: an object that
points into a sequence and can move to the next element. Every container
exposes `begin()` and `end()`, and `end()` is one-past-the-last — a marker,
never a value to dereference.

```cpp
#include <vector>
#include <iostream>

std::vector<int> v{10, 20, 30};
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << " ";           // dereference reads the element
}
*v.begin() = 11;                        // non-const iterators can write
```

The iterator categories, from weakest to strongest:

- **input/output** — single pass (stream iterators)
- **forward** — re-read, multi-pass (`forward_list`, `unordered_map`)
- **bidirectional** — plus `--it` (`list`, `map`, `set`)
- **random access** — plus `it + n`, `it1 - it2`, `it[n]` (`vector`, `deque`, `array`)

Category decides which algorithms you may call: `std::sort` needs random
access, so it works on `vector` but not on `list` (which offers its own
`l.sort()` member). `const` containers hand back `const_iterator`s — you
can read, you cannot write.
"""

L_iterators_VI = r"""
Iterator là chất keo nối container với algorithm: một đối tượng trỏ vào
trong dãy và có thể chuyển sang phần tử kế. Mỗi container đều có `begin()`
và `end()`, với `end()` là vị trí sau-phần-tử-cuối — một mốc đánh dấu,
không bao giờ được dereference.

```cpp
#include <vector>
#include <iostream>

std::vector<int> v{10, 20, 30};
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << " ";           // dereference để đọc phần tử
}
*v.begin() = 11;                        // iterator không const có thể ghi
```

Các cấp iterator, từ yếu đến mạnh:

- **input/output** — một lượt duyệt (stream iterator)
- **forward** — đọc lại được, nhiều lượt (`forward_list`, `unordered_map`)
- **bidirectional** — thêm `--it` (`list`, `map`, `set`)
- **random access** — thêm `it + n`, `it1 - it2`, `it[n]` (`vector`, `deque`, `array`)

Cấp iterator quyết định thuật toán bạn được phép gọi: `std::sort` cần random
access, nên chạy được trên `vector` nhưng không chạy trên `list` (list có
member `l.sort()` riêng). Container `const` trả về `const_iterator` — đọc
được, không ghi được.
"""

# ---- lesson algorithms-basics -----------------------------------------------
L_algorithms_EN = r"""
The `<algorithm>` header is a vocabulary of loops other people have already
written — tested, named, and complexity-documented. Reading code that uses
it is faster than reading hand-rolled loops.

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v{4, 1, 3, 1, 5};

auto it = std::find(v.begin(), v.end(), 3);      // iterator or end()
int n = std::count(v.begin(), v.end(), 1);       // how many 1s
bool has = std::any_of(v.begin(), v.end(),
                       [](int x) { return x > 4; });
std::sort(v.begin(), v.end());                   // O(n log n), ascending
std::reverse(v.begin(), v.end());
auto mx = *std::max_element(v.begin(), v.end());
```

Three habits that make algorithms safe:

1. **Check before dereferencing.** `std::find` returns `end()` when nothing
   matches; comparing against `end()` is the only safe move.
2. **Prefer the `_if` family with a predicate** instead of transforming
   data to fit a non-`_if` version.
3. **Read the complexity line.** `sort` is O(n log n); `count` is O(n);
   nothing here is free.
"""

L_algorithms_VI = r"""
Header `<algorithm>` là bộ từ vựng của những vòng lặp mà người khác đã viết
sẵn — được kiểm thử, có tên, và ghi rõ độ phức tạp. Đọc code dùng thuật toán
chuẩn nhanh hơn đọc vòng lặp viết tay.

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v{4, 1, 3, 1, 5};

auto it = std::find(v.begin(), v.end(), 3);      // iterator hoặc end()
int n = std::count(v.begin(), v.end(), 1);       // có bao nhiêu số 1
bool has = std::any_of(v.begin(), v.end(),
                       [](int x) { return x > 4; });
std::sort(v.begin(), v.end());                   // O(n log n), tăng dần
std::reverse(v.begin(), v.end());
auto mx = *std::max_element(v.begin(), v.end());
```

Ba thói quen giúp thuật toán an toàn:

1. **Kiểm tra trước khi dereference.** `std::find` trả `end()` khi không
   khớp; so sánh với `end()` là động tác an toàn duy nhất.
2. **Ưa họ `_if` với predicate** thay vì biến đổi dữ liệu để khớp bản
   không có `_if`.
3. **Đọc dòng độ phức tạp.** `sort` là O(n log n); `count` là O(n); không
   có gì ở đây là miễn phí.
"""

# ---- lesson transforming-algorithms -----------------------------------------
L_transforming_EN = r"""
Two algorithms produce new data from old: `std::transform` (map) and
`std::accumulate` (fold).

```cpp
#include <algorithm>
#include <numeric>
#include <string>
#include <vector>

std::vector<int> v{1, 2, 3};
std::vector<int> doubled;
std::transform(v.begin(), v.end(), std::back_inserter(doubled),
               [](int x) { return x * 2; });

long total = std::accumulate(v.begin(), v.end(), 0L);
std::string joined = std::accumulate(
    words.begin(), words.end(), std::string{},
    [](const std::string& a, const std::string& b) {
        return a.empty() ? b : a + " " + b;
    });
```

`std::back_inserter` is required when the destination is empty: transform
does not grow the container for you; writing through `doubled.begin()` on
an empty vector is undefined behavior.

`accumulate` takes an initial value and a binary operation. Its type rule
is subtle: the *initial value's type* is the accumulator's type — starting
with `0` instead of `0.0` silently truncates a double sum. This is the
classic beginner bug this lesson exists to prevent.
"""

L_transforming_VI = r"""
Hai thuật toán sinh dữ liệu mới từ dữ liệu cũ: `std::transform` (map) và
`std::accumulate` (fold).

```cpp
#include <algorithm>
#include <numeric>
#include <string>
#include <vector>

std::vector<int> v{1, 2, 3};
std::vector<int> doubled;
std::transform(v.begin(), v.end(), std::back_inserter(doubled),
               [](int x) { return x * 2; });

long total = std::accumulate(v.begin(), v.end(), 0L);
std::string joined = std::accumulate(
    words.begin(), words.end(), std::string{},
    [](const std::string& a, const std::string& b) {
        return a.empty() ? b : a + " " + b;
    });
```

`std::back_inserter` là bắt buộc khi đích còn rỗng: transform không tự lớn
container cho bạn; ghi qua `doubled.begin()` trên vector rỗng là hành vi
không xác định.

`accumulate` nhận giá trị khởi tạo và một phép toán nhị phân. Quy tắc kiểu
của nó tinh tế: *kiểu của giá trị khởi tạo* chính là kiểu của accumulator —
khởi đầu bằng `0` thay vì `0.0` sẽ âm thầm cắt cụt tổng số thực. Đây là bug
kinh điển của người mới mà bài học này tồn tại để ngăn chặn.
"""

# ---- lesson lambdas ----------------------------------------------------------
L_lambdas_EN = r"""
A lambda is an unnamed function object written where it is used. The syntax
has four parts: captures, parameters, return type (usually deduced), body.

```cpp
auto square = [](int x) { return x * x; };          // no capture
int factor = 3;
auto scale = [factor](int x) { return x * factor; }; // capture by value
auto push  = [&out](int x) { out.push_back(x); };    // capture by reference
auto all   = [=](int x) { return x * factor; };      // (C++20: explicit)
```

Capture semantics are the interview question *and* the bug source:

- `[factor]` copies at lambda-creation time — later changes to `factor`
  do not affect the lambda.
- `[&factor]` stores a reference — the lambda must not outlive `factor`.
  Returning a by-reference-capturing lambda from a function hands back a
  dangling reference.
- `[this]` captures the enclosing object's pointer; `[this, factor]` is
  the common correct combination.
- Mutable state needs `mutable`: `[n]() mutable { return ++n; }`.

Default capture-by-value (`[=]`) is deprecated in C++20 for `this`
scenarios; prefer listing what you capture — the list documents the
lambda's dependencies.
"""

L_lambdas_VI = r"""
Lambda là một function object không tên, viết ngay tại nơi sử dụng. Cú pháp
có bốn phần: capture, tham số, kiểu trả về (thường được suy luận), thân hàm.

```cpp
auto square = [](int x) { return x * x; };           // không capture
int factor = 3;
auto scale = [factor](int x) { return x * factor; }; // capture bằng giá trị
auto push  = [&out](int x) { out.push_back(x); };    // capture bằng reference
```

Ngữ nghĩa capture vừa là câu hỏi phỏng vấn vừa là nguồn bug:

- `[factor]` copy tại thời điểm tạo lambda — thay đổi `factor` sau đó
  không ảnh hưởng lambda.
- `[&factor]` lưu reference — lambda không được sống lâu hơn `factor`.
  Trả về lambda capture-bằng-reference từ một hàm đồng nghĩa trả về
  reference treo lơ lửng.
- `[this]` capture con trỏ của đối tượng bao ngoài; `[this, factor]` là
  kết hợp đúng thường gặp nhất.
- Trạng thái mutable cần `mutable`: `[n]() mutable { return ++n; }`.

Capture-mặc-định-theo-giá-trị (`[=]`) bị deprecated trong C++20 cho các
tình huống `this`; hãy liệt kê rõ bạn capture gì — danh sách đó chính là
tài liệu về phụ thuộc của lambda.
"""

# ---- practice cppi-p6-algorithms --------------------------------------------
R_MINMAX_STATS = r'''#include <algorithm>
#include <vector>

struct Stats {
    int min;
    int max;
    long sum;
};

Stats stats(const std::vector<int>& v) {
    if (v.empty()) return {0, 0, 0};
    auto p = std::minmax_element(v.begin(), v.end());
    long s = 0;
    for (int x : v) s += x;
    return {*p.first, *p.second, s};
}
'''

W_MINMAX_STATS = r'''#include <algorithm>
#include <vector>

struct Stats {
    int min;
    int max;
    long sum;
};

Stats stats(const std::vector<int>& v) {
    if (v.empty()) return {0, 0, 0};
    auto p = std::minmax_element(v.begin(), v.end());
    // BUG: min and max swapped
    return {*p.second, *p.first, 0};
}
'''

R_NORMALIZE = r'''#include <algorithm>
#include <string>
#include <vector>

std::vector<std::string> normalize(std::vector<std::string> v) {
    std::transform(v.begin(), v.end(), v.begin(),
                   [](std::string s) {
                       for (char& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
                       return s;
                   });
    std::sort(v.begin(), v.end());
    return v;
}
'''

W_NORMALIZE = r'''#include <algorithm>
#include <string>
#include <vector>

std::vector<std::string> normalize(std::vector<std::string> v) {
    std::transform(v.begin(), v.end(), v.begin(),
                   [](std::string s) {
                       for (char& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
                       return s;
                   });
    // BUG: never sorts
    return v;
}
'''

# ---- practice cppi-p6-lambdas ------------------------------------------------
R_SCORE_FILTER = r'''#include <algorithm>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int score;
};

std::vector<Student> passing(const std::vector<Student>& students, int cutoff) {
    std::vector<Student> out;
    std::copy_if(students.begin(), students.end(), std::back_inserter(out),
                 [cutoff](const Student& s) { return s.score >= cutoff; });
    std::sort(out.begin(), out.end(),
              [](const Student& a, const Student& b) { return a.score > b.score; });
    return out;
}
'''

W_SCORE_FILTER = r'''#include <algorithm>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int score;
};

std::vector<Student> passing(const std::vector<Student>& students, int cutoff) {
    std::vector<Student> out;
    std::copy_if(students.begin(), students.end(), std::back_inserter(out),
                 [cutoff](const Student& s) { return s.score >= cutoff; });
    std::sort(out.begin(), out.end(),
              [](const Student& a, const Student& b) { return a.score < b.score; });
    return out;
}
'''

# ---- checkpoint: running average with transform+accumulate -------------------
R_RUNNING_AVG = r'''#include <algorithm>
#include <numeric>
#include <vector>

std::vector<double> running_avg(const std::vector<int>& v) {
    std::vector<double> out(v.size());
    long prefix = 0;
    std::size_t seen = 0;
    std::transform(v.begin(), v.end(), out.begin(),
                   [&prefix, &seen](int x) {
                       prefix += x;
                       ++seen;
                       return static_cast<double>(prefix) / static_cast<double>(seen);
                   });
    return out;
}
'''

W_RUNNING_AVG = r'''#include <algorithm>
#include <numeric>
#include <vector>

std::vector<double> running_avg(const std::vector<int>& v) {
    std::vector<double> out(v.size());
    long prefix = 0;
    std::transform(v.begin(), v.end(), out.begin(),
                   [&prefix](int x) {
                       prefix += x;
                       // BUG: divides by the TOTAL size, not elements seen so far
                       return static_cast<double>(prefix) / static_cast<double>(v.size());
                   });
    return out;
}
'''

# ---- challenges --------------------------------------------------------------
CH_STATS = challenge(
    "cppi-m6-stats",
    "min/max/sum with std::minmax_element",
    "Implement `Stats stats(const std::vector<int>& v)` where `Stats` has `int min; int max; long sum;`. Return `{0, 0, 0}` for an empty vector. Use `std::minmax_element` for the extremes and accumulate the sum yourself (or with `std::accumulate`).",
    r'''#include <algorithm>
#include <vector>
#include <iostream>

struct Stats {
    int min;
    int max;
    long sum;
};

// Stats stats(const std::vector<int>& v)
''',
    [
        ("basic", 'auto s = stats({4, 1, 3, 1, 5});\nCHECK_EQ(s.min, 1);\nCHECK_EQ(s.max, 5);\nCHECK_EQ(s.sum, 14);', "minmax_element returns a pair of iterators into the vector."),
        ("single", 'auto s = stats({7});\nCHECK_EQ(s.min, 7);\nCHECK_EQ(s.max, 7);\nCHECK_EQ(s.sum, 7);', "One element is both min and max."),
        ("empty", 'auto s = stats({});\nCHECK_EQ(s.min, 0);\nCHECK_EQ(s.sum, 0);', "The empty case must be handled before dereferencing."),
        ("negatives", 'auto s = stats({-5, -1, -9});\nCHECK_EQ(s.min, -9);\nCHECK_EQ(s.max, -1);\nCHECK_EQ(s.sum, -15);', "Negatives must not break the extremes."),
    ],
    level="guided",
)

CH_NORMALIZE = challenge(
    "cppi-m6-normalize",
    "Normalize: lowercase + sort",
    "Implement `std::vector<std::string> normalize(std::vector<std::string> v)` returning a copy with every string lowercased and the whole vector sorted lexicographically. Use `std::transform` in place (it may take and return `v` by value) plus `std::sort`.",
    r'''#include <algorithm>
#include <cctype>
#include <string>
#include <vector>
#include <iostream>

// std::vector<std::string> normalize(std::vector<std::string> v)
''',
    [
        ("basic", 'auto r = normalize({"Beta", "alpha", "gamma"});\nCHECK_EQ(r.size(), 3);\nCHECK_EQ(r[0], std::string("alpha"));\nCHECK_EQ(r[1], std::string("beta"));\nCHECK_EQ(r[2], std::string("gamma"));', "Lowercase first, then the sort sees consistent case."),
        ("mixed-case", 'auto r = normalize({"B", "a"});\nCHECK_EQ(r[0], std::string("a"));\nCHECK_EQ(r[1], std::string("b"));', "Without lowercasing, \'B\' (66) sorts before \'a\' (97)."),
        ("empty", 'CHECK_EQ(normalize({}).size(), 0);', "Nothing to do."),
    ],
    level="independent",
)

CH_PASSING = challenge(
    "cppi-m6-passing",
    "Filter and rank with lambdas",
    "Given the `Student` struct in the boilerplate, implement `std::vector<Student> passing(const std::vector<Student>& students, int cutoff)` returning students with `score >= cutoff`, ordered by score **descending**. Use `std::copy_if` with a capture-by-value lambda, then `std::sort` with a comparator lambda.",
    r'''#include <algorithm>
#include <string>
#include <vector>
#include <iostream>

struct Student {
    std::string name;
    int score;
};

// std::vector<Student> passing(const std::vector<Student>& students, int cutoff)
''',
    [
        ("basic", 'std::vector<Student> in{{"a", 50}, {"b", 80}, {"c", 70}};\nauto r = passing(in, 60);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0].name, std::string("b"));\nCHECK_EQ(r[1].name, std::string("c"));', "Highest score first — the comparator returns a.score > b.score."),
        ("below-cutoff", 'std::vector<Student> in{{"a", 50}};\nCHECK_EQ(passing(in, 60).size(), 0);', "50 < 60: nobody passes."),
        ("all-pass-tied", 'std::vector<Student> in{{"a", 70}, {"b", 70}};\nauto r = passing(in, 60);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0].score, 70);\nCHECK_EQ(r[1].score, 70);', "Ties are acceptable — stability is not part of this contract."),
    ],
    level="combination",
)

# ---- checkpoint --------------------------------------------------------------
CP_RUNNING = challenge(
    "cppi-checkpoint-algorithms",
    "Checkpoint: Running average",
    "Implement `std::vector<double> running_avg(const std::vector<int>& v)` where element i is the average of v[0..i]. One `std::transform` with a by-reference captured prefix sum must produce the whole output (no manual loop in main). The empty vector returns an empty vector.",
    r'''#include <algorithm>
#include <vector>
#include <iostream>

// std::vector<double> running_avg(const std::vector<int>& v)
''',
    [
        ("basic", 'auto r = running_avg({2, 4, 6});\nCHECK_EQ(r.size(), 3);\nCHECK(r[0] > 1.99 && r[0] < 2.01);\nCHECK(r[1] > 2.99 && r[1] < 3.01);\nCHECK(r[2] > 3.99 && r[2] < 4.01);', "Averages are 2/1, 6/2, 12/3."),
        ("negative-dip", 'auto r = running_avg({10, -10});\nCHECK(r[0] > 9.99 && r[0] < 10.01);\nCHECK(r[1] > -0.01 && r[1] < 0.01);', "A negative second element drags the average to zero."),
        ("empty", 'CHECK_EQ(running_avg({}).size(), 0);', "No elements, no averages."),
    ],
    difficulty="intermediate",
)

VI_STATS = vi_challenge(
    "min/max/tổng với std::minmax_element",
    "Cài `Stats stats(const std::vector<int>& v)` với `Stats` gồm `int min; int max; long sum;`. Trả `{0, 0, 0}` cho vector rỗng. Dùng `std::minmax_element` cho hai cực trị và tự cộng tổng (hoặc dùng `std::accumulate`).",
    [
        ("basic", "minmax_element trả một pair các iterator trỏ vào vector."),
        ("single", "Một phần tử vừa là min vừa là max."),
        ("empty", "Trường hợp rỗng phải được xử lý trước khi dereference."),
        ("negatives", "Số âm không được làm sai các cực trị."),
    ],
)

VI_NORMALIZE = vi_challenge(
    "Chuẩn hoá: viết thường + sắp xếp",
    "Cài `std::vector<std::string> normalize(std::vector<std::string> v)` trả về bản sao với mọi chuỗi viết thường và cả vector được sắp theo từ điển. Dùng `std::transform` tại chỗ (có thể nhận và trả `v` bằng giá trị) cộng với `std::sort`.",
    [
        ("basic", "Viết thường trước để sort nhìn thấy cùng một kiểu chữ."),
        ("mixed-case", "Không viết thường thì 'B' (66) đứng trước 'a' (97)."),
        ("empty", "Không có gì để làm."),
    ],
)

VI_PASSING = vi_challenge(
    "Lọc và xếp hạng bằng lambda",
    "Với struct `Student` trong boilerplate, cài `std::vector<Student> passing(const std::vector<Student>& students, int cutoff)` trả về các học viên có `score >= cutoff`, sắp theo điểm **giảm dần**. Dùng `std::copy_if` với lambda capture-bằng-giá-trị, rồi `std::sort` với comparator lambda.",
    [
        ("basic", "Điểm cao nhất trước — comparator trả a.score > b.score."),
        ("below-cutoff", "50 < 60: không ai qua môn."),
        ("all-pass-tied", "Hoà điểm được chấp nhận — tính ổn định không nằm trong hợp đồng này."),
    ],
)

VI_CP_RUNNING = vi_challenge(
    "Kiểm tra điểm: Trung bình chạy dần",
    "Cài `std::vector<double> running_avg(const std::vector<int>& v)` trong đó phần tử i là trung bình của v[0..i]. Một `std::transform` duy nhất với prefix sum capture-bằng-reference phải sinh ra toàn bộ kết quả (không có vòng lặp thủ công trong main). Vector rỗng trả vector rỗng.",
    [
        ("basic", "Các trung bình là 2/1, 6/2, 12/3."),
        ("negative-dip", "Phần tử âm thứ hai kéo trung bình về 0."),
        ("empty", "Không phần tử, không trung bình."),
    ],
)

P1 = [CH_STATS, CH_NORMALIZE]
VI_P1 = {"cppi-m6-stats": VI_STATS, "cppi-m6-normalize": VI_NORMALIZE}
P2 = [CH_PASSING]
VI_P2 = {"cppi-m6-passing": VI_PASSING}

# ---- emit --------------------------------------------------------------------
write_lesson(
    MOD, "cpp-iterators",
    "Iterators: The Container-Algorithm Glue",
    "begin/end semantics, the four iterator categories, and why std::sort refuses a list.",
    25, L_iterators_EN,
    "Iterator: chất keo nối container với algorithm",
    "Ngữ nghĩa begin/end, bốn cấp iterator, và vì sao std::sort từ chối list.",
    L_iterators_VI,
)
write_lesson(
    MOD, "algorithms-basics",
    "Core Algorithms: find, count, sort, and Friends",
    "The everyday <algorithm> vocabulary, the end() check habit, _if predicates, and honest complexity.",
    25, L_algorithms_EN,
    "Thuật toán cốt lõi: find, count, sort và bạn bè",
    "Bộ từ vựng <algorithm> hằng ngày, thói quen kiểm tra end(), predicate _if, và độ phức tạp trung thực.",
    L_algorithms_VI,
)
write_lesson(
    MOD, "transforming-algorithms",
    "Transform and Accumulate: Map and Fold",
    "Producing new data: back_inserter necessity and accumulate's initial-value type trap.",
    25, L_transforming_EN,
    "Transform và Accumulate: map và fold",
    "Sinh dữ liệu mới: vì sao cần back_inserter và bẫy kiểu giá trị khởi tạo của accumulate.",
    L_transforming_VI,
)
write_lesson(
    MOD, "lambdas",
    "Lambda Functions and Captures",
    "The four-part syntax, value vs reference captures, lifetime dangers, and mutable state.",
    30, L_lambdas_EN,
    "Lambda và capture",
    "Cú pháp bốn phần, capture bằng giá trị hay reference, nguy cơ vòng đời, và trạng thái mutable.",
    L_lambdas_VI,
)

write_practice(
    MOD, "cppi-p6-algorithms",
    "Algorithm practice",
    "minmax_element statistics and a case-normalizing transform+sort.",
    "Luyện thuật toán",
    "Thống kê với minmax_element và transform+sort chuẩn hoá chữ hoa/thường.",
    "algorithms-basics", 30, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m6-stats", R_MINMAX_STATS, W_MINMAX_STATS),
        ("cppi-m6-normalize", R_NORMALIZE, W_NORMALIZE),
    ],
)
write_practice(
    MOD, "cppi-p6-lambdas",
    "Lambda practice",
    "Filter and rank students with copy_if plus a comparator.",
    "Luyện lambda",
    "Lọc và xếp hạng học viên bằng copy_if cộng comparator.",
    "lambdas", 25, "intermediate", P2, VI_P2,
    solutions=[
        ("cppi-m6-passing", R_SCORE_FILTER, W_SCORE_FILTER),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-algorithms",
    "Checkpoint: One Transform, Whole Answer",
    "Running averages with a single transform + captured prefix sum — stateful lambdas done right.",
    35,
    r"""
`running_avg` is the module's exam because it combines everything: a
`std::transform` that writes into a pre-sized output, a lambda capturing a
running prefix **by reference**, and correct division by the count seen so
far — not the total size.

The by-reference capture is the load-bearing decision: the lambda must
remember state between calls. The classic wrong answer divides the prefix
by `v.size()` every time — it looks plausible and fails exactly one test.

Before you code: what does the empty vector return? Decide, then make the
test prove it.
""",
    "Kiểm tra điểm: Một transform, trọn câu trả lời",
    "Trung bình chạy dần bằng một transform duy nhất + prefix sum bị capture — lambda có trạng thái làm đúng cách.",
    r"""
`running_avg` là bài kiểm tra của module vì nó gộp mọi thứ: một
`std::transform` ghi vào kết quả đã cấp phát sẵn, một lambda capture prefix
chạy dần **bằng reference**, và phép chia đúng cho số phần tử đã thấy —
không phải tổng kích thước.

Capture-bằng-reference là quyết định chịu lực: lambda phải nhớ trạng thái
giữa các lần gọi. Câu trả lời sai kinh điển là chia prefix cho `v.size()`
mọi lần — nghe hợp lý và fail đúng một test.

Trước khi code: vector rỗng trả về gì? Hãy quyết định, rồi để test chứng minh.
""",
    CP_RUNNING, VI_CP_RUNNING,
    solution=R_RUNNING_AVG, wrong=W_RUNNING_AVG,
)

write_module(
    MOD,
    "Iterators and Algorithms",
    "The algorithm vocabulary over begin/end: categories, find/count/sort, transform and accumulate, and lambda captures with correct lifetimes.",
    "Iterator và thuật toán",
    "Bộ từ vựng thuật toán trên nền begin/end: các cấp iterator, find/count/sort, transform và accumulate, và capture lambda đúng vòng đời.",
    ["cpp-iterators", "algorithms-basics", "transforming-algorithms", "lambdas", "advanced-checkpoint-algorithms"],
    ["cppi-p6-algorithms", "cppi-p6-lambdas"],
)
print("module 6 emitted")
