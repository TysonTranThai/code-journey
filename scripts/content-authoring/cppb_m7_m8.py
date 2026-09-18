#!/usr/bin/env python3
"""C++ Beginner — module 7 (collections) and module 8 (stl-algorithms)."""
from cppb import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 7: collections ============================
M7 = "collections"

L7A = "vector-and-array"
L7B = "map-set-pair"
L7C = "choosing-containers"
L7D = "checkpoint-collections"

write_module(
    M7,
    "Collections: vector, map, set",
    "The standard library containers that replace raw arrays: vector growth, associative lookup with map/set, and how to choose.",
    "Collection: vector, map, set",
    "Những container thư viện chuẩn thay thế mảng thô: vector tăng trưởng, tra cứu kết hợp với map/set, và cách lựa chọn.",
    [L7A, L7B, L7C, L7D],
    ["m7-vector-practice", "m7-map-practice"],
)

write_lesson(
    M7, L7A,
    "std::vector (and when std::array)",
    "The default container: construction, push_back, size, indexing with .at, iteration, and 2-D vectors.",
    12,
    '''
```cpp
#include <vector>

std::vector<int> scores;                 // empty
scores.push_back(9);                     // append: {9}
scores.push_back(7);                     // {9, 7}
std::vector<int> init{9, 7, 10};         // initializer list
std::vector<int> filled(5, 0);           // {0,0,0,0,0} — five zeros
```

## Why vector beats raw arrays

A raw C array `int a[10]` is a fixed block of bytes: no size knowledge, no bounds checks, decays to a pointer when passed, and cannot grow. `std::vector` is a resizable array that *knows its own length*, copies properly on assignment, and cleans up after itself (that last point is RAII — module 12). Rule of thumb with almost no exceptions: **if you are writing a raw array, you probably want a `std::vector` (known size) or `std::array` (fixed small size)**.

`std::array<int, 3>` is a thin wrapper over a fixed-size array that adds the standard-library conveniences (`.size()`, comparisons, STL algorithm compatibility) with zero overhead. Use it when the size is genuinely fixed at compile time.

## The everyday API

```cpp
scores.size()            // 2 — a size_t (unsigned); watch int/size_t comparisons
scores.at(1)             // 7 — bounds-checked; [] is the unchecked fast path
scores.back()            // 10
scores.pop_back()        // remove last
scores.empty()           // false
```

## Iterating

```cpp
for (int s : scores) { /* by value — copies each int */ }
for (const int& s : scores) { /* read-only, no copy */ }
for (int& s : scores) { s *= 2; }        // mutate in place
```

The `const&` form matters when elements are big (strings); for ints it is a wash. Module 11 explains the `&` fully.

## Growth and 2-D

`push_back` occasionally grows the vector's buffer (capacity ≥ size) — you do not manage that; just know `size()` is elements, `capacity()` is room. A 2-D grid is a vector of vectors: `std::vector<std::vector<int>> grid(rows, std::vector<int>(cols, 0));` then `grid[r][c]` (bounds-checked: `grid.at(r).at(c)`).
''',
    "std::vector (và khi nào dùng std::array)",
    "Container mặc định: khởi tạo, push_back, size, đánh chỉ số với .at, duyệt phần tử, và vector 2 chiều.",
    '''
```cpp
#include <vector>

std::vector<int> scores;                 // rỗng
scores.push_back(9);                     // thêm cuối: {9}
scores.push_back(7);                     // {9, 7}
std::vector<int> init{9, 7, 10};         // danh sách khởi tạo
std::vector<int> filled(5, 0);           // {0,0,0,0,0} — năm số không
```

## Vì sao vector thắng mảng thô

Một mảng C thô `int a[10]` là một khối byte cố định: không biết kích thước, không kiểm tra biên, suy biến thành con trỏ khi truyền đi, và không thể lớn lên. `std::vector` là mảng co giãn *tự biết độ dài*, được sao chép đúng khi gán, và tự dọn dẹp sau mình (điểm cuối cùng chính là RAII — module 12). Nguyên tắc gần như không ngoại lệ: **nếu bạn đang viết mảng thô, có lẽ bạn muốn một `std::vector` (kích thước linh hoạt) hoặc `std::array` (kích thước cố định nhỏ)**.

`std::array<int, 3>` là lớp bọc mỏng quanh mảng kích thước cố định, thêm các tiện nghi chuẩn (`.size()`, so sánh, tương thích thuật toán STL) với chi phí bằng không. Dùng nó khi kích thước thực sự cố định lúc biên dịch.

## API hằng ngày

```cpp
scores.size()            // 2 — một size_t (không dấu); cẩn thận khi so với int
scores.at(1)             // 7 — có kiểm tra biên; [] là đường nhanh không kiểm tra
scores.back()            // 10
scores.pop_back()        // bỏ phần tử cuối
scores.empty()           // false
```

## Duyệt

```cpp
for (int s : scores) { /* theo giá trị — sao chép từng int */ }
for (const int& s : scores) { /* chỉ đọc, không sao chép */ }
for (int& s : scores) { s *= 2; }        // sửa tại chỗ
```

Dạng `const&` quan trọng khi phần tử lớn (string); với int thì như nhau. Module 11 sẽ giải thích `&` trọn vẹn.

## Tăng trưởng và mảng 2 chiều

`push_back` thi thoảng mở rộng buffer của vector (capacity ≥ size) — bạn không phải quản lý; chỉ cần biết `size()` là số phần tử, `capacity()` là chỗ trống. Lưới 2 chiều là vector của các vector: `std::vector<std::vector<int>> grid(rows, std::vector<int>(cols, 0));` rồi `grid[r][c]` (có kiểm tra biên: `grid.at(r).at(c)`).
''',
)

write_lesson(
    M7, L7B,
    "map, set, and pair",
    "Associative containers: keyed lookup with map/unordered_map, uniqueness with set, and pair as a two-slot box.",
    12,
    '''
## std::map: key → value

```cpp
#include <map>
#include <string>

std::map<std::string, int> stock;
stock["pen"] = 120;                 // insert or overwrite
stock["ink"] += 5;                  // reads 0 if absent, then adds — subtle!
int pens = stock.at("pen");         // throws if key missing
if (stock.count("ink")) { /* present */ }
for (const auto& [item, qty] : stock) {   // C++17 structured binding, sorted by key
    std::cout << item << ": " << qty << '\\n';
}
```

`operator[]` **inserts a zero** when the key is absent — a legendary source of bugs in counting code. Use `[]` when you intend to insert/overwrite; use `.at()` or `find`/`count` when merely reading.

`std::map` keeps keys **sorted** (a tree underneath). `std::unordered_map` is the hash-table sibling: faster on average, no ordering. Default to `map` while learning (predictable order helps debugging); choose `unordered_map` when profiling says lookup is hot.

## std::set: uniqueness

```cpp
#include <set>
std::set<int> seen;
seen.insert(3);            // returns <iterator, bool inserted>
seen.insert(3);            // second insert does nothing
CHECK(seen.size() == 1);
bool has = seen.count(3);  // 1 = present
```

A `set` is a bag of unique, sorted keys — the direct answer to "have I seen this before?" and "which distinct values are there?".

## std::pair: a two-slot box

```cpp
#include <utility>
std::pair<std::string, int> entry{"pen", 120};
entry.first; entry.second;
```

Pairs show up naturally with maps (each entry is a pair) and as cheap two-value returns (`find` returns an iterator, `insert` returns pair<iterator,bool>). The structured binding `auto [k, v]` unpacks them elegantly.

## Coming up

Three containers is a *toolbox*, not a rulebook. Next: how to actually choose.
''',
    "map, set, và pair",
    "Container kết hợp: tra cứu theo khóa với map/unordered_map, tính duy nhất với set, và pair như một hộp hai ô.",
    '''
## std::map: khóa → giá trị

```cpp
#include <map>
#include <string>

std::map<std::string, int> stock;
stock["pen"] = 120;                 // chèn mới hoặc ghi đè
stock["ink"] += 5;                  // đọc 0 nếu chưa có, rồi cộng — tinh vi đấy!
int pens = stock.at("pen");         // ném exception nếu thiếu khóa
if (stock.count("ink")) { /* có mặt */ }
for (const auto& [item, qty] : stock) {   // structured binding C++17, sắp theo khóa
    std::cout << item << ": " << qty << '\\n';
}
```

`operator[]` **chèn số 0** khi khóa vắng mặt — nguồn bug huyền thoại trong code đếm. Dùng `[]` khi bạn chủ ý chèn/ghi đè; dùng `.at()` hoặc `find`/`count` khi chỉ đọc.

`std::map` giữ khóa **được sắp xếp** (bên dưới là cây). `std::unordered_map` là người anh em bảng băm: nhanh hơn trung bình, nhưng không có thứ tự. Mặc định dùng `map` khi còn học (thứ tự đoán được giúp việc debug); chọn `unordered_map` khi profiling nói tra cứu đang là điểm nóng.

## std::set: tính duy nhất

```cpp
#include <set>
std::set<int> seen;
seen.insert(3);            // trả về <iterator, bool chèn thành công>
seen.insert(3);            // lần chèn thứ hai không làm gì
CHECK(seen.size() == 1);
bool has = seen.count(3);  // 1 = có mặt
```

Một `set` là túi các khóa duy nhất, có sắp xếp — câu trả lời trực tiếp cho "mình đã gặp cái này chưa?" và "có những giá trị phân biệt nào?".

## std::pair: hộp hai ô

```cpp
#include <utility>
std::pair<std::string, int> entry{"pen", 120};
entry.first; entry.second;
```

Pair xuất hiện tự nhiên với map (mỗi phần tử là một pair) và như giá trị trả về hai-in-một (`find` trả iterator, `insert` trả pair<iterator,bool>). Structured binding `auto [k, v]` gói chúng lại một cách thanh lịch.

## Sắp tới

Ba container là một *hộp công cụ*, không phải luật. Bài sau: cách thực sự lựa chọn.
''',
)

write_lesson(
    M7, L7C,
    "Choosing a Container",
    "The decision table: sequence vs lookup vs uniqueness, plus the honesty about cost that professionals apply.",
    9,
    '''
## The beginner decision table

| Need | Container |
| --- | --- |
| An ordered list you iterate, append to, index | `std::vector` |
| Exactly N elements, fixed at compile time | `std::array` |
| Look up a value BY A KEY (name → phone) | `std::map` / `std::unordered_map` |
| Track "have I seen X?" / distinct values | `std::set` / `std::unordered_set` |
| Two values travelling together | `std::pair` (or a struct — module 9) |

If your answer is not in the table, the odds are it is `vector`. It genuinely is the default.

## Cost intuition (not a course in complexity)

- `vector`: index access O(1); append at end amortized O(1); insert in the middle O(n) — everything after it shifts.
- `map`/`set`: operations O(log n); keeps order.
- `unordered_map`/`unordered_set`: average O(1), worst-case degradation exists.

You do not memorize these tables; you remember *the shape of the tradeoff*: vector is compact and cache-friendly, trees trade a little per-op cost for sorted order, hashes gamble on speed. When a loop over a collection feels slow, the first question is "is the *container* right?" — the second is module 18's.

## The honesty rule

Choosing a container is an architectural statement about your data. `std::map<std::string, std::vector<int>> grades_by_student;` says "each student has many grades, looked up by name" — the declaration alone is documentation. When a container choice surprises a reviewer, either the choice or the name is wrong.
''',
    "Chọn Container",
    "Bảng quyết định: trình tự vs tra cứu vs tính duy nhất, cùng sự trung thực về chi phí mà dân chuyên áp dụng.",
    '''
## Bảng quyết định cho người mới

| Nhu cầu | Container |
| --- | --- |
| Danh sách có thứ tự để duyệt, thêm cuối, đánh chỉ số | `std::vector` |
| Đúng N phần tử, cố định lúc biên dịch | `std::array` |
| Tra giá trị THEO KHÓA (tên → số điện thoại) | `std::map` / `std::unordered_map` |
| Theo dõi "đã gặp X chưa?" / các giá trị phân biệt | `std::set` / `std::unordered_set` |
| Hai giá trị đi cùng nhau | `std::pair` (hoặc một struct — module 9) |

Nếu câu trả lời của bạn không có trong bảng, khả năng cao là `vector`. Thật sự đó là lựa chọn mặc định.

## Trực giác về chi phí (không phải môn học về độ phức tạp)

- `vector`: truy chỉ số O(1); thêm cuối khấu trừ O(1); chèn giữa O(n) — mọi thứ phía sau phải dời.
- `map`/`set`: thao tác O(log n); giữ thứ tự.
- `unordered_map`/`unordered_set`: trung bình O(1), có thể xấu đi trong trường hợp xấu nhất.

Bạn không cần học thuộc các bảng này; chỉ cần nhớ *hình dạng của sự đánh đổi*: vector gọn và thân thiện với cache, cây đánh đổi một chút chi phí mỗi thao tác để lấy thứ tự, bảng băm cá cược vào tốc độ. Khi một vòng lặp duyệt collection có vẻ chậm, câu hỏi đầu tiên là "có phải *container* đang sai?" — câu thứ hai thuộc về module 18.

## Quy tắc trung thực

Chọn container là một phát kiến kiến trúc về dữ liệu của bạn. `std::map<std::string, std::vector<int>> grades_by_student;` nói rằng "mỗi học sinh có nhiều điểm, tra theo tên" — riêng dòng khai báo đã là tài liệu. Khi một lựa chọn container khiến người review ngạc nhiên, thì hoặc lựa chọn hoặc cái tên đang sai.
''',
)

# ---- Module 7 checkpoint ----
write_checkpoint(
    M7, L7D,
    "Checkpoint: Collections",
    "One graded challenge: word frequency with map — insert-or-count done right.",
    15,
    '''
**Checkpoint — collections.** Pass the graded challenge below to finish the module.

The classic word-frequency task, graded on the exact behaviors where `operator[]` vs `.at()`/`count` matters.
''',
    "Checkpoint: Collection",
    "Một challenge có chấm: tần suất từ với map — chèn-hoặc-đếm đúng cách.",
    '''
**Checkpoint — collection.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Bài toán tần suất từ kinh điển, được chấm trên đúng những hành vi nơi `operator[]` so với `.at()`/`count` tạo ra khác biệt.
''',
    challenge(
        "cpp7-check-word-freq",
        "Word Frequency",
        "Implement `word_freq(text)` returning a `std::map<std::string,int>` counting lowercase space-separated words, and `most_common(freq)` returning the alphabetically-first among the most frequent.",
        "#include <map>\\n#include <string>\\n\\nstd::map<std::string, int> word_freq(const std::string& text) {\\n    // TODO\\n}\\nstd::string most_common(const std::map<std::string, int>& freq) {\\n    // TODO\\n}",
        [
            ("counts", "auto f = word_freq(std::string{\"b a b a c\"}); CHECK_EQ(f.at(std::string{\"a\"}), 2); CHECK_EQ(f.at(std::string{\"b\"}), 2); CHECK_EQ(f.at(std::string{\"c\"}), 1);", "Each word counted once per occurrence."),
            ("empty", "auto f = word_freq(std::string{\"\"}); CHECK(f.empty());", "No words → empty map."),
            ("most common", "CHECK(most_common(word_freq(std::string{\"b a b a c\"})) == std::string{\"a\"});", "a and b tie at 2; map iterates sorted, so 'a' wins."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Tần suất từ",
        "Cài đặt `word_freq(text)` trả về `std::map<std::string,int>` đếm các từ thường (lowercase) ngăn cách bởi dấu cách, và `most_common(freq)` trả về từ có tần suất cao nhất (từ đầu tiên theo thứ tự alphabet khi bằng nhau).",
        [("đếm", "Mỗi từ được đếm đúng số lần xuất hiện."), ("rỗng", "Không có từ → map rỗng."), ("phổ biến nhất", "a và b hòa ở 2; map duyệt theo thứ tự, nên 'a' thắng.")],
    ),
    solution="#include <map>\\n#include <string>\\n#include <sstream>\\nstd::map<std::string, int> word_freq(const std::string& text) {\\n    std::map<std::string, int> freq;\\n    std::istringstream in(text);\\n    std::string w;\\n    while (in >> w) ++freq[w];\\n    return freq;\\n}\\nstd::string most_common(const std::map<std::string, int>& freq) {\\n    std::string best;\\n    int best_n = -1;\\n    for (const auto& [w, n] : freq) {\\n        if (n > best_n) { best_n = n; best = w; }\\n    }\\n    return best;\\n}",
    wrong="#include <map>\\n#include <string>\\n#include <sstream>\\nstd::map<std::string, int> word_freq(const std::string& text) {\\n    std::map<std::string, int> freq;\\n    std::istringstream in(text);\\n    std::string w;\\n    while (in >> w) freq[w] = 1;\\n    return freq;\\n}\\nstd::string most_common(const std::map<std::string, int>& freq) {\\n    std::string best;\\n    int best_n = -1;\\n    for (const auto& [w, n] : freq) {\\n        if (n > best_n) { best_n = n; best = w; }\\n    }\\n    return best;\\n}",
)

# ---- Module 7 practice sets ----
write_practice(
    M7, "m7-vector-practice",
    "Vector Practice: Sequences",
    "Deduplicate preserving order, rotate, and merge two sorted vectors.",
    "Luyện Vector: Trình tự",
    "Khử trùng lặp giữ nguyên thứ tự, xoay vòng, và trộn hai vector đã sắp.",
    L7A, 25, "beginner",
    [
        challenge(
            "cpp7-dedupe",
            "Deduplicate (Keep Order)",
            "Implement `dedupe(items)`: return a new vector keeping the FIRST occurrence of each value, order preserved. {3,1,3,2,1} → {3,1,2}.",
            "#include <vector>\\n\\nstd::vector<int> dedupe(const std::vector<int>& items) {\\n    // TODO\\n}",
            [("keeps order", "CHECK((dedupe({3, 1, 3, 2, 1}) == std::vector<int>{3, 1, 2}));", "First occurrences, in first-seen order."), ("empty", "CHECK(dedupe({}).empty());", "Nothing in, nothing out.")],
            level="guided",
        ),
    ],
    {"cpp7-dedupe": vi_challenge("Khử trùng lặp (giữ thứ tự)", "Cài đặt `dedupe(items)`: trả về vector mới giữ lần xuất hiện ĐẦU TIÊN của mỗi giá trị, đúng thứ tự. {3,1,3,2,1} → {3,1,2}.", [("giữ thứ tự", "Lần xuất hiện đầu tiên, theo thứ tự xuất hiện."), ("rỗng", "Không vào, không ra.")])},
    solutions=[
        ("cpp7-dedupe", "#include <vector>\\n#include <set>\\nstd::vector<int> dedupe(const std::vector<int>& items) {\\n    std::set<int> seen;\\n    std::vector<int> out;\\n    for (int x : items) {\\n        if (seen.insert(x).second) out.push_back(x);\\n    }\\n    return out;\\n}", "#include <vector>\\nstd::vector<int> dedupe(const std::vector<int>& items) {\\n    return items;\\n}"),
    ],
)

write_practice(
    M7, "m7-map-practice",
    "Map & Set Practice: Lookups",
    "Inventory operations with map (and the []-inserts-zero trap), plus a set-based cross-check.",
    "Luyện Map & Set: Tra cứu",
    "Thao tác kho hàng bằng map (cùng cái bẫy []-chèn-số-0), kèm bài kiểm tra chéo bằng set.",
    L7B, 25, "beginner",
    [
        challenge(
            "cpp7-inventory",
            "Inventory Operations",
            "Implement `add_stock(map, item, qty)` (adds qty to item, inserting if needed) and `stock_of(map, item)` (returns qty, or 0 if absent — WITHOUT using operator[] on the read path).",
            "#include <map>\\n#include <string>\\n\\nstd::map<std::string, int> add_stock(std::map<std::string, int> stock, const std::string& item, int qty) {\\n    // TODO\\n}\\nint stock_of(const std::map<std::string, int>& stock, const std::string& item) {\\n    // TODO — reading a missing key must not insert\\n}",
            [("add new", "auto s = add_stock({}, std::string{\"pen\"}, 10); CHECK_EQ(s.at(std::string{\"pen\"}), 10);", "Inserting a new item with its qty."), ("add existing", "auto s = add_stock(add_stock({}, std::string{\"pen\"}, 10), std::string{\"pen\"}, 5); CHECK_EQ(s.at(std::string{\"pen\"}), 15);", "Adds to the existing quantity."), ("read missing", "CHECK_EQ(stock_of({}, std::string{\"ghost\"}), 0);", "Missing item reads as 0 without inserting anything.")],
            level="real-world",
        ),
    ],
    {"cpp7-inventory": vi_challenge("Thao tác kho hàng", "Cài đặt `add_stock(map, item, qty)` (cộng qty vào item, chèn mới nếu cần) và `stock_of(map, item)` (trả về số lượng, hoặc 0 nếu vắng — KHÔNG dùng operator[] trên đường đọc).", [("thêm mới", "Chèn item mới cùng số lượng."), ("thêm vào cái có sẵn", "Cộng vào số lượng hiện có."), ("đọc cái vắng", "Item vắng mặt đọc là 0 mà không chèn gì cả.")])},
    solutions=[
        ("cpp7-inventory", "#include <map>\\n#include <string>\\nstd::map<std::string, int> add_stock(std::map<std::string, int> stock, const std::string& item, int qty) {\\n    stock[item] += qty;\\n    return stock;\\n}\\nint stock_of(const std::map<std::string, int>& stock, const std::string& item) {\\n    auto it = stock.find(item);\\n    return it == stock.end() ? 0 : it->second;\\n}", "#include <map>\\n#include <string>\\nstd::map<std::string, int> add_stock(std::map<std::string, int> stock, const std::string& item, int qty) {\\n    stock[item] = qty;\\n    return stock;\\n}\\nint stock_of(const std::map<std::string, int>& stock, const std::string& item) {\\n    auto it = stock.find(item);\\n    return it == stock.end() ? 0 : it->second;\\n}"),
    ],
)

# ============================ MODULE 8: stl-algorithms ============================
M8 = "stl-algorithms"

L8A = "iterators-and-algorithms"
L8B = "lambdas-and-predicates"
L8C = "checkpoint-algorithms"

write_module(
    M8,
    "STL Algorithms & Lambdas",
    "Stop hand-rolling loops: sort, find, count_if, accumulate, reverse — and the lambdas that customize them.",
    "Thuật toán STL & Lambda",
    "Ngừng viết tay mọi vòng lặp: sort, find, count_if, accumulate, reverse — và các lambda tùy biến chúng.",
    [L8A, L8B, L8C],
    ["m8-algo-practice", "m8-lambda-practice"],
)

write_lesson(
    M8, L8A,
    "Iterators and the Algorithm Family",
    "begin/end as the language of ranges, the everyday algorithms, and why the standard library beats hand-rolled loops.",
    11,
    '''
## The idea

Every container hands out **iterators** — generalised positions — via `begin()` and `end()`. `begin()` points at the first element; `end()` points *one past the last* (a half-open range `[begin, end)`; `end` is never dereferenced). Algorithms speak this language, which is why they work identically on vector, array, string...

```cpp
#include <algorithm>
#include <numeric>
#include <vector>

std::vector<int> v{5, 3, 9, 1};

std::sort(v.begin(), v.end());                    // {1, 3, 5, 9}
auto it = std::find(v.begin(), v.end(), 5);       // iterator to 5, or v.end()
bool has = (it != v.end());
int n_odd  = std::count_if(v.begin(), v.end(), [](int x){ return x % 2 != 0; });
int sum    = std::accumulate(v.begin(), v.end(), 0);
std::reverse(v.begin(), v.end());
auto smallest = *std::min_element(v.begin(), v.end());
```

## Why prefer algorithms over hand-rolled loops

1. **Intent.** `std::sort` announces its purpose; a loop must be *read* to be understood.
2. **Correctness.** `std::sort` is battle-tested; your quicksort is a weekend project.
3. **Range-for can't do everything.** Sorting, searching, folding — range-for has no answer; algorithms do.

When a loop you write is just `for (auto& x : c) if (p(x)) ++n;`, the algorithm version (`std::count_if`) says the same thing in one line that cannot be misread.

## Ranges: the C++20 evolution (a glance)

C++20 adds `std::ranges::sort(v)` — same algorithms, container passed directly, fewer `.begin()`s. Know the name; this course teaches the iterator form because it underlies both and remains the lingua franca of documentation and real code.
''',
    "Iterator và đại gia đình thuật toán",
    "begin/end như ngôn ngữ của các dải (range), những thuật toán hằng ngày, và vì sao thư viện chuẩn thắng vòng lặp viết tay.",
    '''
## Ý tưởng

Mọi container phát cho bạn các **iterator** — "vị trí tổng quát" — qua `begin()` và `end()`. `begin()` trỏ vào phần tử đầu; `end()` trỏ *vào sau phần tử cuối* (một dải nửa mở `[begin, end)`; không bao giờ được giải tham chiếu `end`). Các thuật toán nói ngôn ngữ này, đó là lý do chúng hoạt động giống hệt trên vector, array, string...

```cpp
#include <algorithm>
#include <numeric>
#include <vector>

std::vector<int> v{5, 3, 9, 1};

std::sort(v.begin(), v.end());                    // {1, 3, 5, 9}
auto it = std::find(v.begin(), v.end(), 5);       // iterator tới 5, hoặc v.end()
bool has = (it != v.end());
int n_odd  = std::count_if(v.begin(), v.end(), [](int x){ return x % 2 != 0; });
int sum    = std::accumulate(v.begin(), v.end(), 0);
std::reverse(v.begin(), v.end());
auto smallest = *std::min_element(v.begin(), v.end());
```

## Vì sao ưu tiên thuật toán hơn vòng lặp viết tay

1. **Ý định.** `std::sort` công bố mục đích của nó; một vòng lặp phải được *đọc* mới hiểu.
2. **Tính đúng đắn.** `std::sort` đã qua hàng triệu lần chiến đấu; quicksort của bạn là một dự án cuối tuần.
3. **Range-for không làm được mọi thứ.** Sắp xếp, tìm kiếm, gộp — range-for không có câu trả lời; thuật toán thì có.

Khi một vòng lặp bạn viết chỉ là `for (auto& x : c) if (p(x)) ++n;`, phiên bản thuật toán (`std::count_if`) nói đúng điều đó trong một dòng không thể đọc nhầm.

## Ranges: bước tiến hóa C++20 (liếc qua)

C++20 thêm `std::ranges::sort(v)` — cùng các thuật toán, truyền thẳng container, bớt các `.begin()`. Hãy biết cái tên này; khóa này dạy dạng iterator vì nó là nền của cả hai và vẫn là ngôn ngữ chung của tài liệu lẫn code thật.
''',
)

write_lesson(
    M8, L8B,
    "Lambdas and Predicates",
    "Anonymous functions where algorithms need them: capture, parameters, and the comparator pattern for sort.",
    11,
    '''
## The shape

```cpp
auto is_even = [](int x) { return x % 2 == 0; };
```

A **lambda** is a nameless function you write inline: `[]` (capture clause), parameters, body. They exist so algorithms can carry their logic with them:

```cpp
std::count_if(v.begin(), v.end(), [](int x){ return x >= 60; });
```

## Capture: what the lambda can see

`[]` is empty → the lambda sees nothing outside. To use outside variables, list them:

```cpp
int limit = 60;
auto below = [limit](int x) { return x < limit; };   // copy limit in
auto bump  = [&total](int x) { total += x; };        // by reference (can modify)
```

Default to capturing by value `[limit]` — a snapshot is easy to reason about. `[&]` (capture everything by reference) is convenient and a footgun: it keeps *references* that can dangle if the lambda outlives the variables (module 11's theme, again). In this course: name what you capture.

## The comparator pattern

`std::sort`'s optional third argument answers "smaller how?":

```cpp
std::sort(v.begin(), v.end(), [](int a, int b){ return a > b; });   // descending
```

The comparator must be a *strict weak ordering* — practically: return true when `a` must come strictly before `b`. Returning `a <= b` breaks sorting in subtle ways (and UB in some algorithms). Compare `<`, never `<=`.

## Words with `std::string`

```cpp
std::sort(words.begin(), words.end(), [](const std::string& a, const std::string& b){
    return a.size() < b.size();      // by length
});
```

The same pattern scales to any "key": by length, by last character, by mapped-to value in a map. This comparator + a struct (module 9) is the exact shape of "sort my records by field".
''',
    "Lambda và vị từ",
    "Hàm vô danh đúng chỗ thuật toán cần: capture, tham số, và mẫu comparator cho sort.",
    '''
## Dạng chuẩn

```cpp
auto is_even = [](int x) { return x % 2 == 0; };
```

Một **lambda** là hàm không tên bạn viết ngay tại chỗ: `[]` (mệnh đề capture), tham số, thân hàm. Chúng tồn tại để các thuật toán mang theo logic của mình:

```cpp
std::count_if(v.begin(), v.end(), [](int x){ return x >= 60; });
```

## Capture: lambda nhìn thấy được gì

`[]` rỗng → lambda không nhìn thấy gì bên ngoài. Muốn dùng biến ngoài, hãy liệt kê:

```cpp
int limit = 60;
auto below = [limit](int x) { return x < limit; };   // sao chép limit vào
auto bump  = [&total](int x) { total += x; };        // theo tham chiếu (được sửa)
```

Mặc định hãy capture theo giá trị `[limit]` — một bản chụp thì dễ suy luận. `[&]` (capture tất cả theo tham chiếu) tiện lợi nhưng là cái bẫy: nó giữ các *tham chiếu* có thể trở nên treo nếu lambda sống lâu hơn biến (chủ đề quen thuộc của module 11). Trong khóa này: hãy gọi tên điều bạn capture.

## Mẫu comparator

Đối số thứ ba tùy chọn của `std::sort` trả lời câu hỏi "nhỏ hơn theo nghĩa nào?":

```cpp
std::sort(v.begin(), v.end(), [](int a, int b){ return a > b; });   // giảm dần
```

Comparator phải là một *thứ tự yếu ngặt* — trên thực tế: trả true khi `a` phải đứng *ngặt* trước `b`. Trả về `a <= b` phá hỏng việc sắp xếp theo cách tinh vi (và là UB trong một số thuật toán). Hãy so `<`, không bao giờ `<=`.

## Với `std::string`

```cpp
std::sort(words.begin(), words.end(), [](const std::string& a, const std::string& b){
    return a.size() < b.size();      // theo độ dài
});
```

Cùng mẫu đó mở rộng cho mọi "khóa": theo độ dài, theo ký tự cuối, theo giá trị mà map ánh xạ tới. Comparator này cộng với một struct (module 9) chính là hình dạng đúng của "sắp sổ của tôi theo trường".
''',
)

# ---- Module 8 checkpoint ----
write_checkpoint(
    M8, L8C,
    "Checkpoint: STL Algorithms",
    "One graded challenge: solve a data question with algorithms + lambdas, not hand-rolled loops.",
    15,
    '''
**Checkpoint — STL algorithms.** Pass the graded challenge below to finish the module.

Three data questions over one vector. The spirit of the module: if a standard algorithm exists for a step, use it.
''',
    "Checkpoint: Thuật toán STL",
    "Một challenge có chấm: giải các câu hỏi dữ liệu bằng thuật toán + lambda, không phải vòng lặp viết tay.",
    '''
**Checkpoint — thuật toán STL.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Ba câu hỏi dữ liệu trên cùng một vector. Tinh thần của module: nếu một thuật toán chuẩn tồn tại cho bước đó, hãy dùng nó.
''',
    challenge(
        "cpp8-check-data-questions",
        "Data Questions",
        "Given `std::vector<int> v`, implement `sorted_desc(v)` (new vector, sorted descending), `count_above(v, t)` (number of elements > t), and `sum_of_evens(v)` (sum of even elements). Empty input: empty vector / 0 / 0.",
        "#include <vector>\\n\\nstd::vector<int> sorted_desc(const std::vector<int>& v) {\\n    // TODO\\n}\\nint count_above(const std::vector<int>& v, int t) {\\n    // TODO\\n}\\nint sum_of_evens(const std::vector<int>& v) {\\n    // TODO\\n}",
        [
            ("desc order", "CHECK((sorted_desc({1, 5, 3}) == std::vector<int>{5, 3, 1}));", "Sort with a greater-than comparator; do not mutate the input."),
            ("count", "CHECK_EQ(count_above({1, 7, 4, 9}, 4), 2);", "7 and 9 are strictly above 4."),
            ("evens", "CHECK_EQ(sum_of_evens({1, 2, 3, 4, 6}), 12);", "2 + 4 + 6 = 12."),
            ("empty", "CHECK(sorted_desc({}).empty());", "Empty in, empty out."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Các câu hỏi dữ liệu",
        "Cho `std::vector<int> v`, cài đặt `sorted_desc(v)` (vector mới, sắp giảm dần), `count_above(v, t)` (số phần tử > t), và `sum_of_evens(v)` (tổng các phần tử chẵn). Input rỗng: vector rỗng / 0 / 0.",
        [("giảm dần", "Sắp với comparator greater-than; không được sửa input."), ("đếm", "7 và 9 là ngặt hơn 4."), ("chẵn", "2 + 4 + 6 = 12."), ("rỗng", "Rỗng vào, rỗng ra.")],
    ),
    solution="#include <vector>\\n#include <algorithm>\\n#include <numeric>\\nstd::vector<int> sorted_desc(const std::vector<int>& v) {\\n    std::vector<int> out = v;\\n    std::sort(out.begin(), out.end(), [](int a, int b){ return a > b; });\\n    return out;\\n}\\nint count_above(const std::vector<int>& v, int t) {\\n    return static_cast<int>(std::count_if(v.begin(), v.end(), [t](int x){ return x > t; }));\\n}\\nint sum_of_evens(const std::vector<int>& v) {\\n    return std::accumulate(v.begin(), v.end(), 0, [](int acc, int x){ return x % 2 == 0 ? acc + x : acc; });\\n}",
    wrong="#include <vector>\\n#include <algorithm>\\n#include <numeric>\\nstd::vector<int> sorted_desc(const std::vector<int>& v) {\\n    std::vector<int> out = v;\\n    std::sort(out.begin(), out.end(), [](int a, int b){ return a >= b; });\\n    return out;\\n}\\nint count_above(const std::vector<int>& v, int t) {\\n    return static_cast<int>(std::count_if(v.begin(), v.end(), [t](int x){ return x > t; }));\\n}\\nint sum_of_evens(const std::vector<int>& v) {\\n    return std::accumulate(v.begin(), v.end(), 0, [](int acc, int x){ return x % 2 == 0 ? acc + x : acc; });\\n}",
)

# ---- Module 8 practice sets ----
write_practice(
    M8, "m8-algo-practice",
    "Algorithms Practice: The Everyday Five",
    "find, count_if, min/max_element, accumulate, reverse — applied to questions a data analyst would actually ask.",
    "Luyện Thuật toán: Năm câu hằng ngày",
    "find, count_if, min/max_element, accumulate, reverse — áp dụng vào những câu hỏi mà một nhà phân tích dữ liệu thật sự hỏi.",
    L8A, 25, "beginner",
    [
        challenge(
            "cpp8-range-stats",
            "Range Stats",
            "Using algorithms (not hand loops): implement `spread(v)` = max − min (0 for empty), and `has_negative(v)`.",
            "#include <vector>\\n\\nint spread(const std::vector<int>& v) {\\n    // TODO\\n}\\nbool has_negative(const std::vector<int>& v) {\\n    // TODO\\n}",
            [("spread", "CHECK_EQ(spread({4, 9, 2}), 7);", "9 − 2 = 7 via min_element/max_element."), ("spread empty", "CHECK_EQ(spread({}), 0);", "Empty has no spread."), ("negative", "CHECK(has_negative({3, -1, 4}));", "count_if or any-style check.")],
            level="independent",
        ),
    ],
    {"cpp8-range-stats": vi_challenge("Thống kê khoảng", "Dùng thuật toán (không viết tay vòng lặp): cài đặt `spread(v)` = max − min (0 nếu rỗng), và `has_negative(v)`.", [("khoảng", "9 − 2 = 7 qua min_element/max_element."), ("rỗng", "Rỗng thì không có khoảng."), ("âm", "count_if hoặc kiểm tra kiểu any.")])},
    solutions=[
        ("cpp8-range-stats", "#include <vector>\\n#include <algorithm>\\nint spread(const std::vector<int>& v) {\\n    if (v.empty()) return 0;\\n    auto lo = *std::min_element(v.begin(), v.end());\\n    auto hi = *std::max_element(v.begin(), v.end());\\n    return hi - lo;\\n}\\nbool has_negative(const std::vector<int>& v) {\\n    return std::count_if(v.begin(), v.end(), [](int x){ return x < 0; }) > 0;\\n}", "#include <vector>\\n#include <algorithm>\\nint spread(const std::vector<int>& v) {\\n    if (v.empty()) return 0;\\n    auto lo = *std::min_element(v.begin(), v.end());\\n    auto hi = *std::max_element(v.begin(), v.end());\\n    return lo - hi;\\n}\\nbool has_negative(const std::vector<int>& v) {\\n    return std::count_if(v.begin(), v.end(), [](int x){ return x < 0; }) > 0;\\n}"),
    ],
)

write_practice(
    M8, "m8-lambda-practice",
    "Lambda Practice: Custom Keys",
    "Sort records by a secondary key and partition around a threshold.",
    "Luyện Lambda: Khóa tùy biến",
    "Sắp bản ghi theo khóa phụ, và phân vùng quanh một ngưỡng.",
    L8B, 25, "beginner",
    [
        challenge(
            "cpp8-sort-pairs",
            "Sort Pairs by Second",
            "Implement `by_second(pairs)`: return a new vector of `std::pair<std::string,int>` sorted by the int (ascending); ties keep alphabetical order of the string.",
            "#include <utility>\\n#include <vector>\\n#include <string>\\n\\nstd::vector<std::pair<std::string, int>> by_second(const std::vector<std::pair<std::string, int>>& pairs) {\\n    // TODO\\n}",
            [("by value", "auto in = std::vector<std::pair<std::string,int>>{{\"b\",2},{\"a\",1}}; auto out = by_second(in); CHECK(out[0].first == std::string{\"a\"});", "1 < 2, so {a,1} first."), ("tie alphabetical", "auto in = std::vector<std::pair<std::string,int>>{{\"b\",1},{\"a\",1}}; auto out = by_second(in); CHECK(out[0].first == std::string{\"a\"});", "Equal ints: compare strings as the tiebreak (a < b)."), ("input unchanged", "auto in = std::vector<std::pair<std::string,int>>{{\"b\",2},{\"a\",1}}; auto out = by_second(in); CHECK(in[0].first == std::string{\"b\"});", "Sort a copy — the input vector must stay as it was.")],
            level="real-world",
        ),
    ],
    {"cpp8-sort-pairs": vi_challenge("Sắp pair theo thứ hai", "Cài đặt `by_second(pairs)`: trả về vector mới các `std::pair<std::string,int>` sắp theo số int (tăng dần); khi bằng nhau thì giữ thứ tự alphabet của string.", [("theo giá trị", "1 < 2, nên {a,1} đứng trước."), ("hòa theo alphabet", "Số int bằng nhau: so chuỗi làm chữ số hòa (a < b)."), ("input không đổi", "Sắp trên bản sao — vector input phải giữ nguyên.")])},
    solutions=[
        ("cpp8-sort-pairs", "#include <utility>\\n#include <vector>\\n#include <string>\\n#include <algorithm>\\nstd::vector<std::pair<std::string, int>> by_second(const std::vector<std::pair<std::string, int>>& pairs) {\\n    std::vector<std::pair<std::string, int>> out = pairs;\\n    std::sort(out.begin(), out.end(), [](const auto& a, const auto& b){\\n        if (a.second != b.second) return a.second < b.second;\\n        return a.first < b.first;\\n    });\\n    return out;\\n}", "#include <utility>\\n#include <vector>\\n#include <string>\\n#include <algorithm>\\nstd::vector<std::pair<std::string, int>> by_second(const std::vector<std::pair<std::string, int>>& pairs) {\\n    std::vector<std::pair<std::string, int>> out = pairs;\\n    std::sort(out.begin(), out.end(), [](const auto& a, const auto& b){\\n        return a.second <= b.second;\\n    });\\n    return out;\\n}"),
    ],
)

print("modules 7-8 authored")
