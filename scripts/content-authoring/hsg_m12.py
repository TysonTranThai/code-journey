#!/usr/bin/env python3
"""HSG — Module 12: hsg-stl (STL cho thi đấu).

vector/pair/sort/unique, set/multiset, map, priority_queue, stack/queue,
deque — taught by problem shape, not API memorization. Conventions: T()
for test I/O (real newlines), cpp() for bodies.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

Q = chr(92)
NL = chr(10)


def cpp(s):
    return s.replace("{{NL}}", Q + "n")


def T(*lines):
    return "".join(l + NL for l in lines)


CPP_STD = cpp("""#include <iostream>
#include <algorithm>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <stack>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsg-stl"
write_module(
    M,
    "STL for Contests",
    "The standard containers as problem-solving tools: vector, set, map, priority_queue, stack, queue, deque — chosen by problem shape.",
    "STL cho thi đấu",
    "Các container chuẩn như công cụ giải bài: vector, set, map, priority_queue, stack, queue, deque — chọn theo dạng bài.",
    ["hsg-m12-sequence", "hsg-m12-associative", "hsg-cp-m12"],
    ["hsg-p12-stl"],
)

write_lesson(
    M,
    "hsg-m12-sequence",
    "Sequences: vector, stack, queue, deque",
    "The four workhorses, each with the access pattern it exists to serve.",
    14,
    """## vector — random access, amortized push_back

```cpp
vector<int> a(n);            // n zeros
a.push_back(x);              // amortized O(1)
a.erase(a.begin() + i);      // O(n) — shifts everything after i
sort(a.begin(), a.end());    // O(n log n)
```

`erase` in a loop is the classic O(n^2) trap; if order does not matter,
erase-swap (`a[i] = a.back(); a.pop_back();`) is O(1).

## stack — last in, first out

`push/pop/top/empty`, all O(1). Problem shapes: matching brackets,
undo operations, "nearest smaller element to the left", iterative DFS.

## queue — first in, first out

`push/pop/front/empty`. Problem shapes: BFS (module later), processing
arrivals in order, round-robin elimination.

## deque — both ends, O(1)

```cpp
deque<int> d;
d.push_back(x); d.push_front(y);
d.pop_back();    d.pop_front();
d[i];            // random access too
```

Sliding-window maximum (the monotonic deque, module later) is the
famous application; also "do something to both ends" simulations.

### Choosing

- Need index access? vector.
- Need only the latest? stack.
- Need FIFO fairness? queue.
- Need both ends? deque.
- The wrong choice is rarely a WA — it is the TLE or the 40-line
  hand-rolled array-with-head-and-tail that introduces bugs.
""",
    "Dãy: vector, stack, queue, deque",
    "Bốn chiến mã, mỗi cái tồn tại để phục vụ một kiểu truy cập.",
    """## vector — truy cập ngẫu nhiên, push_back khấu hao

```cpp
vector<int> a(n);            // n số 0
a.push_back(x);              // khấu hao O(1)
a.erase(a.begin() + i);      // O(n) — dồn mọi phần tử sau i
sort(a.begin(), a.end());    // O(n log n)
```

`erase` trong vòng lặp là bẫy O(n^2) kinh điển; nếu thứ tự không quan
trọng, erase-swap (`a[i] = a.back(); a.pop_back();`) là O(1).

## stack — vào sau ra trước

`push/pop/top/empty`, hết O(1). Dạng bài: khớp ngoặc, thao tác hoàn tác,
"phần tử nhỏ hơn gần nhất bên trái", DFS khử đệ quy.

## queue — vào trước ra trước

`push/pop/front/empty`. Dạng bài: BFS (module sau), xử lý khách theo
thứ tự đến, loại trừ vòng tròn.

## deque — hai đầu, O(1)

```cpp
deque<int> d;
d.push_back(x); d.push_front(y);
d.pop_back();    d.pop_front();
d[i];            // vẫn truy cập ngẫu nhiên
```

Cửa sổ trượt lớn nhất (deque đơn điệu, module sau) là ứng dụng nổi
tiếng; thêm các mô phỏng "làm gì đó ở cả hai đầu".

### Cách chọn

- Cần truy cập theo chỉ số? vector.
- Chỉ cần phần tử mới nhất? stack.
- Cần công bằng FIFO? queue.
- Cần cả hai đầu? deque.
- Chọn sai hiếm khi gây WA — nó gây TLE, hoặc mảng-tự-làm-40-dòng đầy
  bug.
""",
)

write_lesson(
    M,
    "hsg-m12-associative",
    "Associative: set, map, priority_queue",
    "Sorted containers and the heap — what each one answers in O(log n) or O(1).",
    13,
    """## set — sorted unique elements

```cpp
set<int> s;
s.insert(x);              // O(log n), silently ignored if present
s.erase(x);               // by value or by iterator
if (s.count(x)) ...       // O(log n) membership
auto it = s.lower_bound(x); // first element >= x
```

Problem shapes: "distinct count", "has this been seen?", "smallest
element >= x" (replacement searching), ordered deduplication. `multiset`
allows duplicates and its `erase(x)` removes **one** occurrence (the
find-iterator version is the precise one to reach for).

## map — sorted key -> value

```cpp
map<string, int> cnt;
++cnt[name];                  // default 0 then increment
for (auto& [k, v] : cnt) ...  // ordered iteration
```

Frequency tables with ordered output ("print words alphabetically with
counts"), coordinate compression bookkeeping, "which key is next after
k" (upper_bound). If you need no ordering, `unordered_map` is faster on
average (hash) but can be hacked/adversarially slow — in HSG settings
`map` is the safe default.

## priority_queue — the heap

```cpp
priority_queue<int> pq;                    // max-heap by default
pq.push(x); pq.pop(); int m = pq.top();    // O(log n), O(log n), O(1)
priority_queue<int, vector<int>, greater<int>> minpq;  // min-heap
```

Problem shapes: "repeatedly take the largest/smallest" (greedy
simulations, merging), top-k streaming, Dijkstra (later module). No
decrease-key, no iteration in order — it is not a sorted container.

### The complexity contract

insert/erase/query: set & map & pq — O(log n); vector push_back —
amortized O(1); anything sorted by sort() — pay O(n log n) once. When a
problem's constraints imply ~10^6+ operations, O(n^2) brute force is
dead on arrival and one of these containers is usually the intended fix.
""",
    "Liên hợp: set, map, priority_queue",
    "Container có thứ tự và heap — mỗi cái trả lời gì trong O(log n) hay O(1).",
    """## set — phần tử phân biệt, có thứ tự

```cpp
set<int> s;
s.insert(x);              // O(log n), bỏ qua nếu đã có
s.erase(x);               // theo giá trị hoặc theo iterator
if (s.count(x)) ...       // O(log n) kiểm tra thuộc
auto it = s.lower_bound(x); // phần tử đầu >= x
```

Dạng bài: "đếm phân biệt", "đã gặp chưa?", "phần tử nhỏ nhất >= x"
(tìm thay thế), khử trùng lặp có thứ tự. `multiset` cho phép trùng và
`erase(x)` của nó xóa **một** lần xuất hiện (bản theo iterator là cách
chính xác).

## map — khóa -> giá trị, có thứ tự

```cpp
map<string, int> cnt;
++cnt[name];                  // mặc định 0 rồi tăng
for (auto& [k, v] : cnt) ...  // duyệt có thứ tự
```

Bảng tần suất kèm xuất có thứ tự ("in từ theo alphabet kèm số đếm"),
sổ sách nén tọa độ, "khóa kế sau k" (upper_bound). Nếu không cần thứ tự,
`unordered_map` nhanh hơn trung bình (hash) nhưng có thể bị làm chậm
chủ động — trong bối cảnh HSG, `map` là mặc định an toàn.

## priority_queue — heap

```cpp
priority_queue<int> pq;                    // max-heap mặc định
pq.push(x); pq.pop(); int m = pq.top();    // O(log n), O(log n), O(1)
priority_queue<int, vector<int>, greater<int>> minpq;  // min-heap
```

Dạng bài: "lặp đi lặp lại lấy lớn nhất/nhỏ nhất" (mô phỏng tham lam,
trộn), top-k trực tuyến, Dijkstra (module sau). Không có decrease-key,
không duyệt theo thứ tự — nó không phải container có thứ tự.

### Bản hợp đồng độ phức tạp

insert/erase/truy vấn: set & map & pq — O(log n); vector push_back —
khấu hao O(1); sắp xếp bằng sort() — trả O(n log n) một lần. Khi giới
hạn của bài ngụ ý ~10^6+ phép toán, vét cạn O(n^2) chết ngay khi sinh
ra và một trong các container này thường là hướng giải định sẵn.
""",
)

A1 = challenge(
    "hsg-p12-distinct-order",
    "Distinct, in Order",
    T(
        "**Description:** Read n integers. Print the distinct values in ascending order,",
        "space-separated, then print the count of distinct values on the next line.",
        "",
        "**Input:** Line 1: n (1 <= n <= 2*10^5). Line 2: n integers (|a_i| <= 10^9).",
        "**Output:** Line 1: distinct values ascending. Line 2: their count.",
        "",
        "**Example:** `6` / `4 2 4 7 2 9` -> `2 4 7 9` / `4`.",
    ),
    [
        contest_test("sample", T("6", "4 2 4 7 2 9"), T("2 4 7 9", "4"),
                     "set dedupes and orders in one move."),
        contest_test("all same", T("3", "5 5 5"), T("5", "1"),
                     "One distinct value."),
        contest_test("all distinct", T("3", "1 2 3"), T("1 2 3", "3"),
                     "Sorted input stays sorted."),
        contest_test("negatives", T("4", "-1 -5 -1 0"), T("-5 -1 0", "3"),
                     "Negative values sort before zero."),
    ],
    level="imitation",
    difficulty="beginner",
)

A2 = challenge(
    "hsg-p12-word-count",
    "Word Census",
    T(
        "**Description:** Read n words. Print each distinct word once, in **alphabetical**",
        "order, followed by its count: `word count` per line.",
        "",
        "**Input:** Line 1: n (1 <= n <= 10^5). Next n lines: one word each (lowercase",
        "letters, <= 20 chars).",
        "**Output:** One line per distinct word: `word count`.",
        "",
        "**Example:** `4` / `banana` / `apple` / `banana` / `cherry` -> `apple 1` / `banana 2` / `cherry 1`.",
    ),
    [
        contest_test("sample", T("4", "banana", "apple", "banana", "cherry"),
                     T("apple 1", "banana 2", "cherry 1"),
                     "map iterates in key order — alphabetical here."),
        contest_test("single word", T("2", "hi", "hi"), T("hi 2"),
                     "One word twice."),
        contest_test("prefix words", T("3", "ab", "a", "abc"), T("a 1", "ab 1", "abc 1"),
                     "Shorter prefixes sort first."),
        contest_test("all distinct", T("3", "x", "y", "z"), T("x 1", "y 1", "z 1"),
                     "Counts are all 1."),
    ],
    level="guided",
    difficulty="beginner",
)

A3 = challenge(
    "hsg-p12-lowest",
    "Replacement Search",
    T(
        "**Description:** Maintain a multiset of n initial values. Process q operations:",
        "`+ x` inserts x; `- x` erases **one** occurrence of x (guaranteed present);",
        "`? x` prints the smallest stored value **>= x**, or `-1` if none exists.",
        "",
        "**Input:** Line 1: n q (1 <= n, q <= 2*10^5). Line 2: n initial values",
        "(|a_i| <= 10^9). Next q lines: an operation as described (|x| <= 10^9).",
        "**Output:** One line per `?` operation.",
        "",
        "**Example:** `3 3` / `2 5 8` / `? 6` / `+ 6` / `? 6` -> `8` / `6`.",
    ),
    [
        contest_test("sample", T("3 3", "2 5 8", "? 6", "+ 6", "? 6"), T("8", "6"),
                     "6 missing -> 8; after inserting 6, lower_bound finds it."),
        contest_test("exact hit", T("1 1", "7", "? 7"), T("7"),
                     "lower_bound returns the element itself."),
        contest_test("below all", T("2 1", "10 20", "? 1"), T("10"),
                     "Everything qualifies; smallest wins."),
        contest_test("above all", T("2 1", "10 20", "? 21"), T("-1"),
                     "No value >= 21."),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p12-gifts",
    "Two-Heap Gifts",
    T(
        "**Description:** You receive n gifts in order, gift i worth w_i. After each receipt,",
        "**while you hold more than one gift**, immediately give away the smallest-valued",
        "gift you hold. After all n steps, print the total worth of the gifts you still hold.",
        "",
        "**Input:** Line 1: n (1 <= n <= 2*10^5). Line 2: n integers w_i (|w_i| <= 10^9).",
        "**Output:** One integer — the total worth of kept gifts.",
        "",
        "**Example:** `4` / `3 1 4 2` -> `4` (+3 hold {3}; +1 give 1, hold {3}; +4 give 3, hold {4}; +2 give 2, hold {4}).",
    ),
    [
        contest_test("odd keep bigger", T("3", "5 1 9"), T("9"),
                     "+5 {5}; +1 give 1 {5}; +9 give 5 {9}. Total 9."),
        contest_test("n equals 1", T("1", "7"), T("7"),
                     "Holding one gift never triggers a give-away."),
        contest_test("two gifts", T("2", "4 6"), T("6"),
                     "+4 {4}; +6 hold two -> give the smaller 4, hold {6}. Total 6."),
        contest_test("negatives", T("4", "-1 -2 -3 -4"), T("-1"),
                     "Each step gives the most negative; -1 survives to the end."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p12-brackets",
    "Bracket Balance",
    T(
        "**Description:** Given a string of '(' and ')' plus q queries, each query replaces one",
        "character (given as position and new character). After **each** query print `YES` if",
        "the whole string is balanced, else `NO`.",
        "",
        "**Input:** Line 1: the string s (2 <= |s| <= 10^5, even length). Line 2: q",
        "(1 <= q <= 10^5). Next q lines: pos c (1 <= pos <= |s|, c is '(' or ')').",
        "**Output:** q lines: `YES` or `NO`.",
        "",
        "**Example:** `()` / `2` / `1 (` / `1 )` -> `NO` / `YES`.",
    ),
    [
        contest_test("sample", T("()", "2", "2 (", "2 )"), T("NO", "YES"),
                     "Flip to (( : unbalanced; flip back to () : balanced."),
        contest_test("hidden negative", T("()((", "1", "3 )"), T("NO"),
                     "State is ())(: total 0 but the prefix dips negative — a total-only check wrongly says YES."),
        contest_test("restore", T("()()", "2", "2 (", "2 )"), T("NO", "YES"),
                     "Flipping position 2 to ( breaks it; flipping back restores."),
        contest_test("swap head", T("()", "1", "1 )"), T("NO"),
                     ") ( has total 0 but starts negative — still unbalanced."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p12-distinct-order": vi_challenge(
        "Phân biệt, có thứ tự",
        T(
            "**Đề bài:** Đọc n số nguyên. In các giá trị phân biệt theo thứ tự tăng dần, cách nhau bởi dấu cách,",
            "rồi in số lượng giá trị phân biệt ở dòng dưới.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 2*10^5). Dòng 2: n số nguyên (|a_i| <= 10^9).",
            "**Dữ liệu ra:** Dòng 1: các giá trị phân biệt tăng dần. Dòng 2: số lượng.",
            "",
            "**Ví dụ:** `6` / `4 2 4 7 2 9` -> `2 4 7 9` / `4`.",
        ),
        [
            ("sample", "set khử trùng lặp và sắp xếp trong một bước."),
            ("all same", "Một giá trị phân biệt."),
            ("all distinct", "Input đã sắp vẫn giữ nguyên thứ tự."),
            ("negatives", "Số âm đứng trước số 0."),
        ],
    ),
    "hsg-p12-word-count": vi_challenge(
        "Tổng điều tra từ ngữ",
        T(
            "**Đề bài:** Đọc n từ. In mỗi từ phân biệt đúng một lần, theo **thứ tự alphabet**,",
            "kèm số lần xuất hiện: `từ số_lượng` mỗi dòng.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 10^5). n dòng tiếp: mỗi dòng một từ (chữ thường,",
            "<= 20 ký tự).",
            "**Dữ liệu ra:** Mỗi từ phân biệt một dòng: `từ số_lượng`.",
            "",
            "**Ví dụ:** `4` / `banana` / `apple` / `banana` / `cherry` -> `apple 1` / `banana 2` / `cherry 1`.",
        ),
        [
            ("sample", "map duyệt theo thứ tự khóa — alphabet ở đây."),
            ("single word", "Một từ xuất hiện hai lần."),
            ("prefix words", "Tiền tố ngắn hơn đứng trước."),
            ("all distinct", "Mọi số lượng đều là 1."),
        ],
    ),
    "hsg-p12-lowest": vi_challenge(
        "Tìm giá trị thay thế",
        T(
            "**Đề bài:** Giữ một multiset gồm n giá trị ban đầu. Xử lý q thao tác:",
            "`+ x` chèn x; `- x` xóa **một** lần xuất hiện của x (đảm bảo có);",
            "`? x` in giá trị nhỏ nhất **>= x** đang lưu, hoặc `-1` nếu không có.",
            "",
            "**Dữ liệu vào:** Dòng 1: n q (1 <= n, q <= 2*10^5). Dòng 2: n giá trị ban đầu",
            "(|a_i| <= 10^9). q dòng tiếp: một thao tác như mô tả (|x| <= 10^9).",
            "**Dữ liệu ra:** Mỗi thao tác `?` một dòng.",
            "",
            "**Ví dụ:** `3 3` / `2 5 8` / `? 6` / `+ 6` / `? 6` -> `8` / `6`.",
        ),
        [
            ("sample", "6 vắng -> 8; sau khi chèn 6, lower_bound tìm ra nó."),
            ("exact hit", "lower_bound trả về chính phần tử đó."),
            ("below all", "Mọi giá trị đều thỏa; nhỏ nhất thắng."),
            ("above all", "Không giá trị nào >= 21."),
        ],
    ),
    "hsg-p12-gifts": vi_challenge(
        "Quà và hai chồng",
        T(
            "**Đề bài:** Bạn nhận n món quà theo thứ tự, quà i có giá w_i. Sau mỗi lần nhận,",
            "**khi đang giữ nhiều hơn một món**, tặng ngay món nhỏ giá nhất đang giữ.",
            "Sau n bước, in tổng giá các món bạn còn giữ.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 2*10^5). Dòng 2: n số nguyên w_i (|w_i| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — tổng giá quà giữ được.",
            "",
            "**Ví dụ:** `4` / `3 1 4 2` -> `4` (xem vết chạy trong phần test).",
        ),
        [
            ("odd keep bigger", "+5 giữ {5}; +1 tặng 1, giữ {5}; +9 tặng 5, giữ {9}. Tổng 9."),
            ("n equals 1", "Giữ một món không bao giờ kích hoạt tặng."),
            ("two gifts", "+4 {4}; +6 giữ hai món -> tặng nhỏ hơn là 4, giữ {6}. Tổng 6."),
            ("negatives", "Mỗi bước tặng món âm nhất; -1 sống sót tới cuối."),
        ],
    ),
    "hsg-p12-brackets": vi_challenge(
        "Cân bằng ngoặc",
        T(
            "**Đề bài:** Cho xâu gồm '(' và ')' cùng q truy vấn, mỗi truy vấn thay một ký tự",
            "(cho vị trí và ký tự mới). Sau **mỗi** truy vấn in `YES` nếu toàn xâu cân bằng, ngược lại `NO`.",
            "",
            "**Dữ liệu vào:** Dòng 1: xâu s (2 <= |s| <= 10^5, độ dài chẵn). Dòng 2: q",
            "(1 <= q <= 10^5). q dòng tiếp: pos c (1 <= pos <= |s|, c là '(' hoặc ')').",
            "**Dữ liệu ra:** q dòng: `YES` hoặc `NO`.",
            "",
            "**Ví dụ:** `()` / `2` / `1 (` / `1 )` -> `NO` / `YES`.",
        ),
        [
            ("sample", "Đổi thành ( ( : mất cân bằng; đổi lại ( ) : cân bằng."),
            ("hidden negative", "Trạng thái là ())(: tổng 0 nhưng tiền tố chạm âm — kiểm tra chỉ-total sẽ sai."),
            ("restore", "Đổi vị trí 2 thành ( làm hỏng; đổi lại là phục hồi."),
            ("swap head", ") ( có tổng 0 nhưng khởi đầu âm — vẫn mất cân bằng."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p12-stl",
    "STL Problem Set",
    "Ordered dedup, frequency maps, lower_bound on a multiset, greedy with a heap, and stack-based validation.",
    "Bài tập STL",
    "Khử trùng lặp có thứ tự, bảng tần suất, lower_bound trên multiset, tham lam với heap, và kiểm tra bằng stack.",
    "hsg-m12-associative",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p12-distinct-order",
            CPP_STD + cpp("""    int n; in >> n;
    set<int> s;
    for (int i = 0; i < n; ++i) {
        int x; in >> x;
        s.insert(x);
    }
    bool first = true;
    for (int v : s) {
        if (!first) out << " ";
        out << v;
        first = false;
    }
    out << "{{NL}}" << s.size() << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    set<int> s;
    for (int i = 0; i < n; ++i) {
        int x; in >> x;
        s.insert(x);
    }
    bool first = true;
    for (int v : s) {
        if (!first) out << " ";
        out << v;
        first = false;
    }
    // near-miss: prints n instead of the distinct count
    out << "{{NL}}" << n << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p12-word-count",
            CPP_STD + cpp("""    int n; in >> n;
    map<string, long long> cnt;
    for (int i = 0; i < n; ++i) {
        string w; in >> w;
        ++cnt[w];
    }
    for (auto& p : cnt)
        out << p.first << " " << p.second << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    map<string, long long> cnt;
    for (int i = 0; i < n; ++i) {
        string w; in >> w;
        // near-miss: assigns instead of accumulating — every word
        // ends with count 1
        cnt[w] = 1;
    }
    for (auto& p : cnt)
        out << p.first << " " << p.second << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p12-lowest",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    multiset<int> s;
    for (int i = 0; i < n; ++i) {
        int x; in >> x;
        s.insert(x);
    }
    while (q--) {
        string op; in >> op;
        int x; in >> x;
        if (op == "+") s.insert(x);
        else if (op == "-") s.erase(s.find(x));
        else {
            auto it = s.lower_bound(x);
            out << (it == s.end() ? -1 : *it) << "{{NL}}";
        }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    multiset<int> s;
    for (int i = 0; i < n; ++i) {
        int x; in >> x;
        s.insert(x);
    }
    while (q--) {
        string op; in >> op;
        int x; in >> x;
        if (op == "+") s.insert(x);
        else if (op == "-") s.erase(s.find(x));
        else {
            // near-miss: upper_bound skips over an exact hit
            auto it = s.upper_bound(x);
            out << (it == s.end() ? -1 : *it) << "{{NL}}";
        }
    }
""") + END,
        ),
        (
            "hsg-p12-gifts",
            CPP_STD + cpp("""    int n; in >> n;
    priority_queue<int, vector<int>, greater<int>> pq;
    long long kept = 0;
    for (int i = 0; i < n; ++i) {
        long long w; in >> w;
        pq.push(w);
        // rule: while holding more than one gift, give the smallest
        if ((int)pq.size() > 1) pq.pop();
    }
    while (!pq.empty()) { kept += pq.top(); pq.pop(); }
    out << kept << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    priority_queue<int> pq;  // near-miss: max-heap — gives away the
                             // LARGEST gift each step, keeping junk
    long long kept = 0;
    for (int i = 0; i < n; ++i) {
        long long w; in >> w;
        pq.push(w);
        if ((int)pq.size() > 1) pq.pop();
    }
    while (!pq.empty()) { kept += pq.top(); pq.pop(); }
    out << kept << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p12-brackets",
            CPP_STD + cpp("""    string s; in >> s;
    int q; in >> q;
    int n = (int)s.size();
    vector<int> cur(n);
    for (int i = 0; i < n; ++i) cur[i] = (s[i] == '(' ? 1 : -1);
    // beginner-honest: recompute prefix depths per query (O(nq)).
    // Constraints here are small by design: n, q <= 2000.
    while (q--) {
        int pos; string c; in >> pos >> c;
        cur[pos - 1] = (c == "(" ? 1 : -1);
        long long run = 0;
        bool ok = true;
        for (int i = 0; i < n && ok; ++i) {
            run += cur[i];
            if (run < 0) ok = false;   // more ')' than '(' at some prefix
        }
        if (run != 0) ok = false;      // leftover unclosed '('
        out << (ok ? "YES" : "NO") << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    int q; in >> q;
    int n = (int)s.size();
    vector<int> cur(n);
    for (int i = 0; i < n; ++i) cur[i] = (s[i] == '(' ? 1 : -1);
    while (q--) {
        int pos; string c; in >> pos >> c;
        cur[pos - 1] = (c == "(" ? 1 : -1);
        // near-miss: only checks the TOTAL open == close — ignores
        // negative prefix depths, so "())" counts as balanced
        long long total = 0;
        for (int i = 0; i < n; ++i) total += cur[i];
        out << (total == 0 ? "YES" : "NO") << "{{NL}}";
    }
""") + END,
        ),
    ],
)

CH12 = challenge(
    "hsg-cp-m12-order",
    "Serving in Order",
    T(
        "**Description:** A counter serves customers. Process q events of three kinds:",
        "`1 x` — customer with ticket x joins the queue;",
        "`2` — serve (remove) the customer at the front;",
        "`3` — print the smallest ticket currently waiting, or `-1` if nobody waits.",
        "",
        "**Input:** Line 1: q (1 <= q <= 2*10^5). Next q lines: an event as described",
        "(1 <= x <= 10^9).",
        "**Output:** One line per event of kind 3.",
        "",
        "**Example:** `6` / `1 5` / `1 3` / `3` / `2` / `3` / `1 4` -> `3` / `5`.",
    ),
    [
        contest_test("sample", T("6", "1 5", "1 3", "3", "2", "3", "1 4"), T("3", "3"),
                     "min{5,3}=3; serve the front (5 joined first); 3 still waits."),
        contest_test("empty min", T("2", "3", "1 7"), T("-1"),
                     "Query before any arrival."),
        contest_test("serve empties", T("3", "1 9", "2", "3"), T("-1"),
                     "Queue drains, then queried."),
        contest_test("duplicates", T("5", "1 4", "1 4", "3", "2", "3"), T("4", "4"),
                     "Equal tickets: both print 4."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP12 = vi_challenge(
    "Phục vụ theo thứ tự",
    T(
        "**Đề bài:** Quầy phục vụ khách. Xử lý q sự kiện ba loại:",
        "`1 x` — khách có vé x xếp hàng;",
        "`2` — phục vụ (xóa) khách ở đầu hàng;",
        "`3` — in vé nhỏ nhất đang chờ, hoặc `-1` nếu không ai chờ.",
        "",
        "**Dữ liệu vào:** Dòng 1: q (1 <= q <= 2*10^5). q dòng tiếp: một sự kiện như mô tả",
        "(1 <= x <= 10^9).",
        "**Dữ liệu ra:** Mỗi sự kiện loại 3 một dòng.",
        "",
        "**Ví dụ:** `6` / `1 5` / `1 3` / `3` / `2` / `3` / `1 4` -> `3` / `5`.",
    ),
    [
        ("sample", "min{5,3}=3; phục vụ đầu hàng (5 vào trước); 3 vẫn chờ."),
        ("empty min", "Truy vấn trước khi có khách."),
        ("serve empties", "Hàng rỗng rồi mới truy vấn."),
        ("duplicates", "Vé bằng nhau: cả hai in 4."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m12",
    "Checkpoint — STL",
    "Pass the graded problem to finish the STL module.",
    15,
    """**Checkpoint — STL.** Pass the graded challenge below. It needs a
container that answers "smallest waiting" in O(log n) while still
serving the front in FIFO order — no single stock container does both,
so combine two (one for the queue order, one for the running minimum)
or exploit the small ticket values. Decide your data design *before*
coding; that is the actual skill this checkpoint grades.

**Điểm kiểm tra — STL.** Pass bài chấm bên dưới. Cần một container trả
lời "vé nhỏ nhất đang chờ" trong O(log n) mà vẫn phục vụ đầu hàng theo
FIFO — không có container sẵn nào làm cả hai, nên hãy kết hợp hai cái
(một cho thứ tự hàng, một cho minimum đang chạy) hoặc tận dụng giá trị
vé nhỏ. Quyết định thiết kế dữ liệu *trước khi* code — đó chính là kỹ
năng mà checkpoint này chấm.
""",
    "Checkpoint — STL",
    "Pass the graded problem to finish the STL module.",
    """**Điểm kiểm tra — STL.** Pass bài chấm bên dưới. Cần một container trả
lời "vé nhỏ nhất đang chờ" trong O(log n) mà vẫn phục vụ đầu hàng theo
FIFO — không có container sẵn nào làm cả hai, nên hãy kết hợp hai cái
(một cho thứ tự hàng, một cho minimum đang chạy) hoặc tận dụng giá trị
vé nhỏ. Quyết định thiết kế dữ liệu *trước khi* code — đó chính là kỹ
năng mà checkpoint này chấm.
""",
    CH12,
    VI_CP12,
    solution=CPP_STD + cpp("""    int q; in >> q;
    queue<long long> order;              // FIFO order of arrivals
    multiset<long long> waiting;         // tickets currently waiting
    while (q--) {
        int kind; in >> kind;
        if (kind == 1) {
            long long x; in >> x;
            order.push(x);
            waiting.insert(x);
        } else if (kind == 2) {
            if (!order.empty()) {
                waiting.erase(waiting.find(order.front()));
                order.pop();
            }
        } else {
            out << (waiting.empty() ? -1 : *waiting.begin()) << "{{NL}}";
        }
    }
""") + END,
    wrong=CPP_STD + cpp("""    int q; in >> q;
    queue<long long> order;
    multiset<long long> waiting;
    while (q--) {
        int kind; in >> kind;
        if (kind == 1) {
            long long x; in >> x;
            order.push(x);
            waiting.insert(x);
        } else if (kind == 2) {
            if (!order.empty()) {
                // near-miss: erases the SMALLEST ticket instead of the
                // front of the queue — the multiset and queue drift apart
                waiting.erase(waiting.begin());
                order.pop();
            }
        } else {
            out << (waiting.empty() ? -1 : *waiting.begin()) << "{{NL}}";
        }
    }
""") + END,
)

print("M12 done")
