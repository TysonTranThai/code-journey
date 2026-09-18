#!/usr/bin/env python3
"""C++ Intermediate — Module 5: stl-fundamentals.

Authoring discipline: every C++ code string (tests, solutions, boilerplate) is
a raw triple-quoted string, so real newlines stay real and C++ "\\n" literals
stay literal. Snippets are self-contained: each test is its own translation
unit (solution.cpp is #included; no cross-test state).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "stl-fundamentals"

# ---- lesson sequence-containers --------------------------------------------
L_sequence_containers_EN = r"""
The STL hands you four containers that hold values in *your* order. Picking
between them is a complexity decision, not a style preference.

```cpp
#include <vector>
#include <array>
#include <deque>
#include <list>

std::vector<int> v{1, 2, 3};   // contiguous; O(1) index; O(1) amortized push_back
std::array<int, 3> a{1, 2, 3}; // fixed size; zero heap; O(1) index
std::deque<int> d{1, 2, 3};    // chunked; O(1) push_front AND push_back
std::list<int> l{1, 2, 3};     // doubly linked; O(1) splice/erase anywhere
```

## What each buys you

| Container | Random access | Insert/erase ends | Insert/erase middle |
|-----------|---------------|-------------------|---------------------|
| `vector`  | O(1)          | back O(1) amortized | O(n) |
| `array`   | O(1)          | — (fixed) | — (fixed) |
| `deque`   | O(1)          | both ends O(1) | O(n) |
| `list`    | — O(n)        | O(1) | O(1) at an iterator |

## The rule that bites everyone: iterator invalidation

- `vector`: **any** growth may reallocate — every iterator/pointer into it dies.
  `push_back` after storing an iterator is a dangling-iterator bug.
- `deque`: insertion at the ends invalidates iterators but **not** references.
- `list`: nothing ever invalidates except erasing the node you hold.

`vector` is the default. Reach for `deque` when you truly need both ends;
`list` only when you splice or hold iterators across many mutations.
"""

L_sequence_containers_VI = r"""
STL cung cấp bốn container giữ giá trị theo *thứ tự của bạn*. Chọn container
nào là quyết định về độ phức tạp, không phải guu stylistic.

```cpp
#include <vector>
#include <array>
#include <deque>
#include <list>

std::vector<int> v{1, 2, 3};   // liền kề; O(1) theo chỉ số; push_back O(1) khấu hao
std::array<int, 3> a{1, 2, 3}; // kích thước cố định; không dùng heap; O(1)
std::deque<int> d{1, 2, 3};    // theo khối; push_front VÀ push_back đều O(1)
std::list<int> l{1, 2, 3};     // liên kết đôi; splice/erase O(1) tại bất kỳ đâu
```

## Mỗi container cho bạn gì

| Container | Truy cập ngẫu nhiên | Chèn/xoá hai đầu | Chèn/xoá giữa |
|-----------|---------------------|------------------|----------------|
| `vector`  | O(1)                | cuối O(1) khấu hao | O(n) |
| `array`   | O(1)                | — (cố định) | — (cố định) |
| `deque`   | O(1)                | cả hai đầu O(1) | O(n) |
| `list`    | — O(n)              | O(1) | O(1) tại iterator |

## Quy tắc cắn người mới nhất: iterator invalidation

- `vector`: **mọi** lần lớn lên có thể reallocate — iterator/pointer trỏ vào
  nó đều chết. `push_back` sau khi giữ iterator là bug treo lơ lửng.
- `deque`: chèn ở hai đầu vô hiệu hoá iterator nhưng **không** vô hiệu hoá
  reference.
- `list`: không gì vô hiệu hoá trừ khi xoá chính node bạn đang giữ.

`vector` là lựa chọn mặc định. Dùng `deque` khi thật sự cần cả hai đầu;
`list` chỉ khi bạn splice hoặc giữ iterator qua nhiều lần thay đổi.
"""

# ---- lesson container-adapters ---------------------------------------------
L_container_adapters_EN = r"""
Three adapters wrap a container and expose exactly one discipline. They are
not containers themselves — you cannot iterate a `stack`.

```cpp
#include <stack>
#include <queue>

std::stack<int> s;   // LIFO: push, pop, top          (defaults to deque)
std::queue<int> q;   // FIFO: push, pop, front, back  (defaults to deque)

#include <queue>
std::priority_queue<int> pq;  // largest pops first by default
```

`priority_queue` is a heap facade, not a sorted list: `push` is O(log n),
`top` is O(1), but there is no iteration and no "update" — you push and pop.

A min-heap is spelled with the comparator form:

```cpp
#include <vector>
#include <queue>
#include <functional>

std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
```

When the ordering key is part of the value, give the element an
`operator<` (or pass a comparator) — the adapter then ranks whole objects.
That is exactly the mechanism Module 4's operator overloading feeds into.
"""

L_container_adapters_VI = r"""
Ba adapter bọc một container và chỉ lộ ra đúng một kỷ luật truy cập. Chúng
không phải container thật — bạn không thể iterate một `stack`.

```cpp
#include <stack>
#include <queue>

std::stack<int> s;   // LIFO: push, pop, top          (mặc định là deque)
std::queue<int> q;   // FIFO: push, pop, front, back  (mặc định là deque)

#include <queue>
std::priority_queue<int> pq;  // phần tử lớn nhất được pop trước
```

`priority_queue` là mặt nạ heap, không phải danh sách đã sắp: `push` O(log n),
`top` O(1), nhưng không có iteration và không có "update" — chỉ push và pop.

Min-heap viết bằng dạng comparator:

```cpp
#include <vector>
#include <queue>
#include <functional>

std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
```

Khi khoá sắp xếp là một phần của giá trị, hãy cho phần tử có `operator<`
(hoặc truyền comparator) — adapter khi đó xếp hạng cả đối tượng. Đây chính
là cơ chế mà nạp chồng toán tử ở Module 4 phục vụ.
"""

# ---- lesson associative-containers -----------------------------------------
L_associative_containers_EN = r"""
Associative containers trade *position* for *lookup*. Two families:

```cpp
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>

std::map<std::string, int> m;          // balanced tree: sorted order, O(log n)
std::unordered_map<std::string, int> u; // hash table: no order, O(1) average
std::set<std::string> s;               // unique keys, sorted
std::unordered_set<std::string> us;    // unique keys, hashed
```

## The decision: do you need order?

- Iterate **in sorted key order** or need `lower_bound` → the ordered family.
- Only single-key lookup, fastest possible → the unordered family.

Insertion is uniform, and `try_emplace` avoids a useless construction when
the key already exists:

```cpp
m[key] += 1;                  // inserts 0 first if absent (operator[])
m.try_emplace(key, 0).first->second += 1;  // no double lookup
```

One trap worth knowing early: `map[key]` **inserts** when the key is
missing. On a `const map&` you must use `.at()` or `.find()` — `operator[]`
does not even compile, and that constraint protects you.

Structures bindings make traversal read cleanly:

```cpp
for (const auto& [key, value] : m) {
    // sorted by key here
}
```
"""

L_associative_containers_VI = r"""
Container kết hợp đổi *vị trí* lấy *tra cứu*. Hai họ:

```cpp
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>

std::map<std::string, int> m;           // cây cân bằng: có thứ tự, O(log n)
std::unordered_map<std::string, int> u; // bảng băm: không thứ tự, O(1) trung bình
std::set<std::string> s;                // khoá duy nhất, có thứ tự
std::unordered_set<std::string> us;     // khoá duy nhất, băm
```

## Quyết định: bạn có cần thứ tự không?

- Duyệt **theo thứ tự khoá tăng dần** hoặc cần `lower_bound` → họ có thứ tự.
- Chỉ tra cứu theo khoá, muốn nhanh nhất có thể → họ unordered.

Chèn dữ liệu thống nhất, và `try_emplace` tránh dựng đối tượng vô ích khi
khoá đã tồn tại:

```cpp
m[key] += 1;                              // chèn 0 trước nếu chưa có (operator[])
m.try_emplace(key, 0).first->second += 1; // không tra cứu hai lần
```

Một bẫy đáng biết sớm: `map[key]` **chèn** khi khoá chưa có. Trên
`const map&` bạn buộc phải dùng `.at()` hoặc `.find()` — `operator[]` thậm
chí không biên dịch, và ràng buộc đó bảo vệ bạn.

Structured bindings giúp việc duyệt đọc gọn:

```cpp
for (const auto& [key, value] : m) {
    // tại đây các khoá đã theo thứ tự
}
"""
# ---- lesson choosing-containers --------------------------------------------
L_choosing_containers_EN = r"""
By now the STL menu is: sequence containers, adapters, and the associative
families. Choosing is a three-question checklist.

1. **How do you access it?** By position → `vector` (or `array` if fixed
   size). By key → `map`/`unordered_map`. By discipline only → adapter.
2. **Which ends?** Both ends O(1) → `deque`. Middle splicing with stable
   iterators → `list`. Everything else → `vector`.
3. **Is sorted order part of the contract?** Yes → ordered family. No →
   `unordered_map` for lookup speed.

Complexity in one table:

| Operation | vector | deque | list | map | unordered_map |
|---|---|---|---|---|---|
| index/front/back | O(1) | O(1) | O(n) | O(log n) | O(1) avg |
| insert at ends | O(1)* | O(1) | O(1) | O(log n) | O(1) avg |
| find by value/key | O(n) | O(n) | O(n) | O(log n) | O(1) avg |

\* amortized at the back.

The default plan in real code: `vector` by default, `unordered_map` for
lookups, `map` when output must be sorted, `priority_queue` for "best first"
processing, `deque` for sliding windows.
"""

L_choosing_containers_VI = r"""
Thực đơn STL đến lúc này: container tuần tự, adapter, và các họ kết hợp.
Chọn container là checklist ba câu hỏi.

1. **Bạn truy cập bằng gì?** Theo vị trí → `vector` (hoặc `array` nếu kích
   thước cố định). Theo khoá → `map`/`unordered_map`. Chỉ theo kỷ luật →
   adapter.
2. **Đầu nào?** Cả hai đầu O(1) → `deque`. splice ở giữa với iterator ổn
   định → `list`. Còn lại → `vector`.
3. **Thứ tự sort có nằm trong hợp đồng không?** Có → họ có thứ tự. Không →
   `unordered_map` để tra cứu nhanh.

Độ phức tạp gộp trong một bảng:

| Thao tác | vector | deque | list | map | unordered_map |
|---|---|---|---|---|---|
| index/front/back | O(1) | O(1) | O(n) | O(log n) | O(1) trung bình |
| chèn ở hai đầu | O(1)* | O(1) | O(1) | O(log n) | O(1) trung bình |
| tìm theo giá trị/khoá | O(n) | O(n) | O(n) | O(log n) | O(1) trung bình |

\* khấu hao ở đầu cuối.

Kế hoạch mặc định trong code thật: `vector` là mặc định, `unordered_map`
để tra cứu, `map` khi kết quả phải có thứ tự, `priority_queue` để xử lý
"tốt nhất trước", `deque` cho cửa sổ trượt.
"""

# ---- practice cppi-p5-sequence ----------------------------------------------
R_WINDOWED = r'''#include <deque>
#include <vector>

std::vector<int> windowed_max(const std::vector<int>& v, std::size_t k) {
    std::vector<int> out;
    if (k == 0 || v.empty()) return out;
    if (k >= v.size()) {
        int best = v[0];
        for (int x : v) best = x > best ? x : best;
        out.push_back(best);
        return out;
    }
    std::deque<std::size_t> dq;  // indices, values decreasing
    for (std::size_t i = 0; i < v.size(); ++i) {
        while (!dq.empty() && v[dq.back()] <= v[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() + k <= i) dq.pop_front();
        if (i + 1 >= k) out.push_back(v[dq.front()]);
    }
    return out;
}
'''

W_WINDOWED = r'''#include <deque>
#include <vector>

std::vector<int> windowed_max(const std::vector<int>& v, std::size_t k) {
    std::vector<int> out;
    if (k == 0 || v.empty()) return out;
    if (k >= v.size()) {
        int best = v[0];
        for (int x : v) best = x > best ? x : best;
        out.push_back(best);
        return out;
    }
    std::deque<std::size_t> dq;
    for (std::size_t i = 0; i < v.size(); ++i) {
        while (!dq.empty() && v[dq.back()] <= v[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() + k <= i) dq.pop_front();
        // BUG: off by one — drops the final window
        if (i + 1 > k && i + 1 <= v.size()) out.push_back(v[dq.front()]);
    }
    return out;
}
'''

R_PARTITION_LIST = r'''#include <list>

std::list<int> evens_first(std::list<int> l) {
    std::list<int> evens;
    for (auto it = l.begin(); it != l.end();) {
        if (*it % 2 == 0) {
            evens.splice(evens.end(), l, it++);  // O(1) node move, no copy
        } else {
            ++it;
        }
    }
    evens.splice(evens.end(), l);  // remaining odds keep their order
    return evens;
}
'''

W_PARTITION_LIST = r'''#include <list>

std::list<int> evens_first(std::list<int> l) {
    std::list<int> evens;
    for (auto it = l.begin(); it != l.end();) {
        if (*it % 2 == 0) {
            evens.splice(evens.end(), l, it++);
        } else {
            ++it;
        }
    }
    // BUG: pushes remaining odds in reverse
    while (!l.empty()) {
        evens.push_back(l.back());
        l.pop_back();
    }
    return evens;
}
'''

# ---- practice cppi-p5-associative -------------------------------------------
R_WORD_COUNT = r'''#include <map>
#include <string>
#include <vector>

std::map<std::string, int> word_counts(const std::vector<std::string>& words) {
    std::map<std::string, int> counts;
    for (const auto& w : words) ++counts[w];
    return counts;
}
'''

W_WORD_COUNT = r'''#include <map>
#include <string>
#include <vector>

std::map<std::string, int> word_counts(
    const std::vector<std::string>& words) {
    std::map<std::string, int> counts;
    for (const auto& w : words) counts[w] = 1;  // BUG: overwrites instead of counting
    return counts;
}
'''

R_DEDUPE_LAST = r'''#include <string>
#include <unordered_map>
#include <vector>

std::vector<std::string> dedupe_last(const std::vector<std::string>& v) {
    std::unordered_map<std::string, std::size_t> last_index;
    for (std::size_t i = 0; i < v.size(); ++i) last_index[v[i]] = i;
    std::vector<std::string> out;
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (last_index[v[i]] == i) out.push_back(v[i]);
    }
    return out;
}
'''

W_DEDUPE_LAST = r'''#include <string>
#include <unordered_set>
#include <vector>

std::vector<std::string> dedupe_last(const std::vector<std::string>& v) {
    std::unordered_set<std::string> seen;
    std::vector<std::string> out;
    for (const auto& s : v) {
        if (seen.insert(s).second) out.push_back(s);  // BUG: keeps FIRST occurrence
    }
    return out;
}
'''

# ---- checkpoint: top-k frequent words ---------------------------------------
R_TOPK = r'''#include <algorithm>
#include <map>
#include <string>
#include <vector>

std::vector<std::string> top_k(const std::vector<std::string>& words,
                               std::size_t k) {
    std::map<std::string, int> counts;
    for (const auto& w : words) ++counts[w];
    std::vector<std::pair<int, std::string>> ranked;
    for (const auto& [word, n] : counts) ranked.push_back({n, word});
    std::sort(ranked.begin(), ranked.end(),
              [](const auto& a, const auto& b) {
                  if (a.first != b.first) return a.first > b.first;
                  return a.second < b.second;  // ties: lexicographic
              });
    std::vector<std::string> out;
    for (std::size_t i = 0; i < ranked.size() && i < k; ++i) {
        out.push_back(ranked[i].second);
    }
    return out;
}
'''

W_TOPK = r'''#include <algorithm>
#include <map>
#include <string>
#include <vector>

std::vector<std::string> top_k(const std::vector<std::string>& words,
                               std::size_t k) {
    std::map<std::string, int> counts;
    for (const auto& w : words) ++counts[w];
    std::vector<std::pair<int, std::string>> ranked;
    for (const auto& [word, n] : counts) ranked.push_back({n, word});
    std::sort(ranked.begin(), ranked.end(),
              [](const auto& a, const auto& b) {
                  if (a.first != b.first) return a.first > b.first;
                  // BUG: ties broken in reverse — larger word first
                  return a.second > b.second;
              });
    std::vector<std::string> out;
    for (std::size_t i = 0; i < ranked.size() && i < k; ++i) {
        out.push_back(ranked[i].second);
    }
    return out;
}
'''

# ---- challenge definitions ---------------------------------------------------
CH_WINDOWED = challenge(
    "cppi-m5-windowed-max",
    "Sliding window maximum",
    "Implement `std::vector<int> windowed_max(const std::vector<int>& v, std::size_t k)` returning the maximum of every contiguous window of size k, in order. If `k` is 0 or `v` is empty return an empty vector; if `k >= v.size()` return a single-element vector with the overall maximum. Target O(n) with a monotonic `std::deque` of indices (pop from the back while the new value is greater-or-equal; pop the front when it falls out of the window).",
    r'''#include <deque>
#include <vector>
#include <iostream>

// std::vector<int> windowed_max(const std::vector<int>& v, std::size_t k)
''',
    [
        ("basic", 'auto r = windowed_max({4,2,12,11,-5,6,7}, 3);\nCHECK_EQ(r.size(), 5);\nCHECK_EQ(r[0], 12);\nCHECK_EQ(r[3], 11);\nCHECK_EQ(r[4], 7);', "Five windows of size 3 slide across seven values."),
        ("identity-k1", 'auto r = windowed_max({3,1,2}, 1);\nCHECK_EQ(r.size(), 3);\nCHECK_EQ(r[0], 3);\nCHECK_EQ(r[2], 2);', "Every window of size 1 is the value itself."),
        ("decreasing", 'auto r = windowed_max({5,4,3,2,1}, 2);\nCHECK_EQ(r.size(), 4);\nCHECK_EQ(r[0], 5);\nCHECK_EQ(r[3], 2);', "A decreasing input makes each window's max its first element."),
        ("oversized-k", 'auto r = windowed_max({1,9,3}, 10);\nCHECK_EQ(r.size(), 1);\nCHECK_EQ(r[0], 9);', "k beyond the size collapses to one overall max."),
    ],
    level="combination",
)

CH_PARTITION = challenge(
    "cppi-m5-partition-list",
    "Stable even/odd reorder with std::list",
    "Implement `std::list<int> evens_first(std::list<int> l)` that moves all even values before all odd values while preserving the relative order within each group. Use `std::list::splice` (O(1) node moves — no element copies). Example: {1,2,3,4,5} becomes {2,4,1,3,5}.",
    r'''#include <list>
#include <iostream>

// std::list<int> evens_first(std::list<int> l)
''',
    [
        ("basic", 'auto r = evens_first({1,2,3,4,5});\nstd::string s;\nfor (int x : r) s += std::to_string(x);\nCHECK_EQ(s, std::string("24135"));', "Evens 2,4 keep their order; odds 1,3,5 follow."),
        ("already-partitioned", 'auto r = evens_first({2,4,1,3});\nstd::string s;\nfor (int x : r) s += std::to_string(x);\nCHECK_EQ(s, std::string("2413"));', "Stability means no unnecessary reordering."),
        ("all-odd", 'auto r = evens_first({1,3,5});\nstd::string s;\nfor (int x : r) s += std::to_string(x);\nCHECK_EQ(s, std::string("135"));', "No evens: the list is unchanged."),
    ],
    level="independent",
)

CH_WORD_COUNT = challenge(
    "cppi-m5-word-count",
    "Ordered word counts",
    "Implement `std::map<std::string, int> word_counts(const std::vector<std::string>& words)` counting occurrences of each word. The returned `map` must iterate in sorted key order — that ordering is part of the contract, so an unordered_map will fail the sorted test.",
    r'''#include <map>
#include <string>
#include <vector>
#include <iostream>

// std::map<std::string, int> word_counts(const std::vector<std::string>& words)
''',
    [
        ("basic", 'auto m = word_counts({"b","a","b","c","a"});\nCHECK_EQ(m.size(), 3);\nCHECK_EQ(m.at("a"), 2);\nCHECK_EQ(m.at("b"), 2);\nCHECK_EQ(m.at("c"), 1);', "operator[] inserts 0 for missing keys, then ++ counts."),
        ("sorted-order", 'auto m = word_counts({"b","a","c"});\nstd::string keys;\nfor (const auto& [k, v] : m) keys += k;\nCHECK_EQ(keys, std::string("abc"));', "A std::map iterates keys in sorted order."),
        ("empty", 'CHECK_EQ(word_counts({}).size(), 0);', "No words, no entries."),
    ],
    level="imitation",
)

CH_DEDUPE = challenge(
    "cppi-m5-dedupe-last",
    "Deduplicate keeping the last occurrence",
    "Implement `std::vector<std::string> dedupe_last(const std::vector<std::string>& v)` removing duplicates so each value appears once — at the position of its LAST occurrence, preserving overall order. Example: {\"a\",\"b\",\"a\",\"c\"} becomes {\"b\",\"a\",\"c\"}. A single index map plus one pass is enough.",
    r'''#include <string>
#include <unordered_map>
#include <vector>
#include <iostream>

// std::vector<std::string> dedupe_last(const std::vector<std::string>& v)
''',
    [
        ("basic", 'auto r = dedupe_last({"a","b","a","c"});\nCHECK_EQ(r.size(), 3);\nCHECK_EQ(r[0], std::string("b"));\nCHECK_EQ(r[1], std::string("a"));\nCHECK_EQ(r[2], std::string("c"));', '"a" survives at its last position; earlier copy is dropped.'),
        ("no-duplicates", 'auto r = dedupe_last({"x","y"});\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0], std::string("x"));', "Nothing to remove."),
        ("all-same", 'auto r = dedupe_last({"z","z","z"});\nCHECK_EQ(r.size(), 1);\nCHECK_EQ(r[0], std::string("z"));', "The last occurrence is also the only survivor."),
    ],
    level="independent",
)

# ---- checkpoint --------------------------------------------------------------
CP_TOPK = challenge(
    "cppi-checkpoint-stl",
    "Checkpoint: Top-K frequent words",
    "Implement `std::vector<std::string> top_k(const std::vector<std::string>& words, std::size_t k)` returning the k most frequent words ordered by count descending; ties are broken lexicographically (smaller word first). If there are fewer than k distinct words, return all of them (still ordered). Combine a counting `std::map` with a sort (or a `std::priority_queue`) — the tie-break rule is the part most solutions get wrong.",
    r'''#include <algorithm>
#include <map>
#include <string>
#include <vector>
#include <iostream>

// std::vector<std::string> top_k(const std::vector<std::string>& words, std::size_t k)
''',
    [
        ("basic", 'auto r = top_k({"apple","banana","apple","cherry","banana","apple"}, 2);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0], std::string("apple"));\nCHECK_EQ(r[1], std::string("banana"));', "Counts 3, 2, 1 — order follows the counts."),
        ("tie-break", 'auto r = top_k({"b","a","c"}, 2);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0], std::string("a"));\nCHECK_EQ(r[1], std::string("b"));', "All tied at 1: lexicographic order decides."),
        ("k-beyond-distinct", 'auto r = top_k({"x","x","y"}, 10);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0], std::string("x"));\nCHECK_EQ(r[1], std::string("y"));', "Fewer distinct words than k: return them all."),
    ],
    difficulty="intermediate",
)

VI_WINDOWED = vi_challenge(
    "Cửa sổ trượt lớn nhất",
    "Cài `std::vector<int> windowed_max(const std::vector<int>& v, std::size_t k)` trả về giá trị lớn nhất của mỗi cửa sổ liên tiếp độ dài k, theo thứ tự. Nếu `k` bằng 0 hoặc `v` rỗng trả vector rỗng; nếu `k >= v.size()` trả vector một phần tử là giá trị lớn nhất toàn cục. Hướng tới O(n) với `std::deque` chỉ số đơn điệu (pop từ cuối khi giá trị mới lớn hơn hoặc bằng; pop đầu khi rơi khỏi cửa sổ).",
    [
        ("basic", "Năm cửa sổ độ dài 3 trượt qua bảy giá trị."),
        ("identity-k1", "Mỗi cửa sổ độ dài 1 chính là giá trị đó."),
        ("decreasing", "Input giảm dần khiến max của mỗi cửa sổ là phần tử đầu."),
        ("oversized-k", "k vượt quá kích thước thu về một max toàn cục."),
    ],
)

VI_PARTITION = vi_challenge(
    "Sắp lại chẵn/lẻ ổn định với std::list",
    "Cài `std::list<int> evens_first(std::list<int> l)` đưa tất cả giá trị chẵn lên trước số lẻ nhưng vẫn giữ thứ tự tương đối trong từng nhóm. Dùng `std::list::splice` (di chuyển node O(1) — không copy phần tử). Ví dụ: {1,2,3,4,5} thành {2,4,1,3,5}.",
    [
        ("basic", "Số chẵn 2,4 giữ nguyên thứ tự; số lẻ 1,3,5 theo sau."),
        ("already-partitioned", "Tính ổn định nghĩa là không sắp lại gì thừa."),
        ("all-odd", "Không có số chẵn: danh sách không đổi."),
    ],
)

VI_WORD_COUNT = vi_challenge(
    "Đếm từ có thứ tự",
    "Cài `std::map<std::string, int> word_counts(const std::vector<std::string>& words)` đếm số lần xuất hiện của mỗi từ. `map` trả về phải duyệt theo thứ tự khoá tăng dần — thứ tự đó là một phần của hợp đồng, nên unordered_map sẽ fail test sorted.",
    [
        ("basic", "operator[] chèn 0 cho khoá chưa có, rồi ++ để đếm."),
        ("sorted-order", "std::map duyệt khoá theo thứ tự tăng dần."),
        ("empty", "Không có từ nào, không có entry nào."),
    ],
)

VI_DEDUPE = vi_challenge(
    "Loại trùng giữ lần cuối",
    "Cài `std::vector<std::string> dedupe_last(const std::vector<std::string>& v)` loại phần tử trùng để mỗi giá trị chỉ xuất hiện một lần — tại vị trí LẦN CUỐI của nó, giữ nguyên thứ tự tổng thể. Ví dụ: {\"a\",\"b\",\"a\",\"c\"} thành {\"b\",\"a\",\"c\"}. Một index map cộng một lượt duyệt là đủ.",
    [
        ("basic", '"a" sống sót ở vị trí cuối; bản sao trước đó bị bỏ.'),
        ("no-duplicates", "Không có gì để loại bỏ."),
        ("all-same", "Lần cuối cũng là lần duy nhất còn lại."),
    ],
)

VI_CP_TOPK = vi_challenge(
    "Kiểm tra điểm: Top-K từ phổ biến",
    "Cài `std::vector<std::string> top_k(const std::vector<std::string>& words, std::size_t k)` trả về k từ phổ biến nhất, sắp theo số lần xuất hiện giảm dần; hoà được phá theo thứ tự từ điển (từ nhỏ hơn trước). Nếu số từ phân biệt ít hơn k, trả tất cả (vẫn có thứ tự). Kết hợp `std::map` đếm với sort (hoặc `std::priority_queue`) — quy tắc phá hoà là phần đa số solution làm sai.",
    [
        ("basic", "Số lần 3, 2, 1 — thứ tự theo số lần xuất hiện."),
        ("tie-break", "Cả ba hoà ở 1: thứ tự từ điển quyết định."),
        ("k-beyond-distinct", "Ít từ phân biệt hơn k: trả tất cả."),
    ],
)

P1 = [CH_WINDOWED, CH_PARTITION]
VI_P1 = {"cppi-m5-windowed-max": VI_WINDOWED, "cppi-m5-partition-list": VI_PARTITION}
P2 = [CH_WORD_COUNT, CH_DEDUPE]
VI_P2 = {"cppi-m5-word-count": VI_WORD_COUNT, "cppi-m5-dedupe-last": VI_DEDUPE}

# ---- emit --------------------------------------------------------------------
write_lesson(
    MOD, "sequence-containers",
    "Sequence Containers: The Complexity Decision",
    "vector, array, deque, and list compared by the operations you actually use — and the invalidation rules that make the choice real.",
    30, L_sequence_containers_EN,
    "Container tuần tự: quyết định theo độ phức tạp",
    "vector, array, deque, list so sánh theo đúng thao tác bạn dùng — và các quy tắc invalidation khiến việc chọn container là chuyện thật.",
    L_sequence_containers_VI,
)
write_lesson(
    MOD, "container-adapters",
    "Container Adapters: stack, queue, priority_queue",
    "One discipline each; the heap facade, min-heap spelling, and how operator< drives adapter ordering.",
    20, L_container_adapters_EN,
    "Adapter container: stack, queue, priority_queue",
    "Mỗi adapter một kỷ luật; mặt nạ heap, cách viết min-heap, và operator< dẫn dắt thứ tự của adapter.",
    L_container_adapters_VI,
)
write_lesson(
    MOD, "associative-containers",
    "Associative Containers: Ordered vs Unordered",
    "Tree vs hash tradeoffs, try_emplace, the map[key] insertion trap, and traversal with structured bindings.",
    30, L_associative_containers_EN,
    "Container kết hợp: có thứ tự vs không thứ tự",
    "Đánh đổi cây và băm, try_emplace, bẫy chèn của map[key], và duyệt bằng structured bindings.",
    L_associative_containers_VI,
)
write_lesson(
    MOD, "choosing-stl-containers",
    "Choosing the Right Container",
    "A three-question checklist plus one complexity table covering every container this course has met.",
    20, L_choosing_containers_EN,
    "Chọn container phù hợp",
    "Checklist ba câu hỏi cộng một bảng độ phức tạp cho mọi container khóa học đã gặp.",
    L_choosing_containers_VI,
)

write_practice(
    MOD, "cppi-p5-sequence",
    "Sequence container problems",
    "A monotonic-deque window maximum and a stable list partition via splice.",
    "Bài toán container tuần tự",
    "Max cửa sổ trượt bằng deque đơn điệu và phân vùng danh sách ổn định bằng splice.",
    "sequence-containers", 35, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m5-windowed-max", R_WINDOWED, W_WINDOWED),
        ("cppi-m5-partition-list", R_PARTITION_LIST, W_PARTITION_LIST),
    ],
)
write_practice(
    MOD, "cppi-p5-associative",
    "Associative container problems",
    "Sorted word counts and a dedupe that keeps the last occurrence.",
    "Bài toán container kết hợp",
    "Đếm từ có thứ tự và loại trùng giữ lần xuất hiện cuối.",
    "associative-containers", 30, "intermediate", P2, VI_P2,
    solutions=[
        ("cppi-m5-word-count", R_WORD_COUNT, W_WORD_COUNT),
        ("cppi-m5-dedupe-last", R_DEDUPE_LAST, W_DEDUPE_LAST),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-stl",
    "Checkpoint: STL in Combination",
    "Top-K frequent words: counting, ordering, and a tie-break that punishes hand-wavy solutions.",
    35,
    r"""
`top_k` is the module's exam: it needs a counting map, an ordering, and a
tie-break — all three from this module's lessons.

- counting: `std::map<std::string, int>` with `operator[]`'s insert-then-increment
- ordering: count descending
- tie-break: lexicographic (smaller word first) — decide this BEFORE coding

Sorting a vector of `(count, word)` pairs with a comparator that checks
`count != count` first is the cleanest deterministic form. A
`priority_queue` with the same comparator works equally well.

If your tie-break test fails while the basic test passes, your comparator
is silently depending on map iteration order or input order — exactly the
nondeterminism this course is training you to eliminate.
""",
    "Kiểm tra điểm: STL kết hợp",
    "Top-K từ phổ biến: đếm, sắp thứ tự, và quy tắc phá hoà trừng phạt solution qua loa.",
    r"""
`top_k` là bài kiểm tra của module: nó cần map để đếm, một thứ tự, và quy tắc
phá hoà — cả ba đến từ các bài học của module này.

- đếm: `std::map<std::string, int>` với cơ chế chèn-then-tăng của `operator[]`
- thứ tự: số lần xuất hiện giảm dần
- phá hoà: theo từ điển (từ nhỏ hơn trước) — hãy quyết định điều này TRƯỚC
  khi code

Sort một vector các cặp `(số lần, từ)` bằng comparator kiểm tra
`số lần khác nhau` trước là dạng sạch và tất định nhất. `priority_queue`
với comparator tương tự cũng được.

Nếu test phá hoà fail trong khi test basic pass, comparator của bạn đang âm
thầm dựa vào thứ tự duyệt của map hoặc thứ tự input — chính là tính không
tất định mà khóa học đang luyện bạn loại bỏ.
""",
    CP_TOPK, VI_CP_TOPK,
    solution=R_TOPK, wrong=W_TOPK,
)

write_module(
    MOD,
    "STL Fundamentals",
    "The standard library's core containers: sequence complexity, adapters, ordered vs unordered lookup, and the checklist for choosing between them.",
    "Nền tảng STL",
    "Các container cốt lõi của thư viện chuẩn: độ phức tạp tuần tự, adapter, tra cứu có và không thứ tự, và checklist chọn container.",
    ["sequence-containers", "container-adapters", "associative-containers", "choosing-stl-containers", "advanced-checkpoint-stl"],
    ["cppi-p5-sequence", "cppi-p5-associative"],
)
print("module 5 emitted")
