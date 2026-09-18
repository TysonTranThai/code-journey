#!/usr/bin/env python3
"""C++ Intermediate — Module 11: dsa (data structures & algorithms).

Authoring discipline: every C++ code string (tests, solutions, boilerplate) is
a raw triple-quoted string, so real newlines stay real and C++ "\\n" literals
stay literal. Snippets are self-contained: each test is its own translation
unit (solution.cpp is #included; no cross-test state).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "dsa"

# ---- lesson complexity ---------------------------------------------------------
L_complexity_EN = r"""
Big-O answers one question: *how does cost grow when input grows?* Not how
fast your machine is — how the curve bends.

| Complexity | Name | Example |
|---|---|---|
| O(1) | constant | `v[i]`, `m[key]` |
| O(log n) | logarithmic | binary search, `std::map` lookup |
| O(n) | linear | `std::find`, one pass |
| O(n log n) | linearithmic | `std::sort`, good divide & conquer |
| O(n²) | quadratic | nested loops over the same data |
| O(2ⁿ) | exponential | naive subset enumeration |

Rules of thumb for reading code:

- sequential loops multiply; nested loops over *independent* things multiply
  too — `for a in X: for b in Y:` is O(|X|·|Y|)
- drop constants and small terms: O(2n + 10) is O(n)
- amortized cost: one `vector::push_back` is O(1) amortized because the
  occasional O(n) growth is paid for by many cheap appends
- `std::unordered_map` is O(1) *average* — worst case O(n) when hashing
  degrades; the word "average" is part of the claim

Complexity is a design tool: choosing a hash map over a linear scan can
turn O(n²) into O(n) without touching anything else.
"""

L_complexity_VI = r"""
Big-O trả lời đúng một câu hỏi: *chi phí tăng thế nào khi input tăng?*
Không phải máy bạn nhanh hay chậm — mà là đường cong dốc thế nào.

| Độ phức tạp | Tên | Ví dụ |
|---|---|---|
| O(1) | hằng số | `v[i]`, `m[key]` |
| O(log n) | logarit | tìm kiếm nhị phân, tra cứu `std::map` |
| O(n) | tuyến tính | `std::find`, một lượt duyệt |
| O(n log n) | tuyến tính-logarit | `std::sort`, chia để trị tốt |
| O(n²) | bậc hai | vòng lặp lồng trên cùng một dữ liệu |
| O(2ⁿ) | mũ | liệt kê tập con kiểu ngây thơ |

Nguyên tắc đọc code:

- các vòng tuần tự nhân nhau; vòng lồng trên *các thứ độc lập* cũng nhân —
  `for a in X: for b in Y:` là O(|X|·|Y|)
- bỏ hằng số và số hạng nhỏ: O(2n + 10) là O(n)
- chi phí khấu hao: một lần `vector::push_back` là O(1) khấu hao vì sự lớn
  lên O(n) thỉnh thoảng được trả bằng nhiều lần thêm rẻ
- `std::unordered_map` là O(1) *trung bình* — xấu nhất O(n) khi hash suy
  giảm; chữ "trung bình" là một phần của tuyên bố

Độ phức tạp là công cụ thiết kế: chọn hash map thay vì quét tuyến tính có
thể biến O(n²) thành O(n) mà không đụng gì khác.
"""

# ---- lesson searching -----------------------------------------------------------
L_searching_EN = r"""
Linear search is `std::find` — O(n), works on anything with equality.
Binary search is different: it requires **sorted data** and random access,
and pays back with O(log n).

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v{1, 3, 5, 7, 9, 11};

bool has = std::binary_search(v.begin(), v.end(), 7);      // yes/no

auto lb = std::lower_bound(v.begin(), v.end(), 7);  // first >= 7
auto ub = std::upper_bound(v.begin(), v.end(), 7);  // first > 7
```

`lower_bound`/`upper_bound` are the workhorses: `lower_bound` gives the
first position where the value could be inserted keeping order;
`upper_bound` gives the last. The distance between them is the count of
equal elements. On `std::map`/`std::set`, the same-named members do this
in O(log n) without touching iterators.

The classic beginner bug: binary searching *unsorted* data. It silently
returns wrong answers — no exception, no warning. Sort first, or use a
structure that keeps itself sorted.

Implementing your own binary search is a rite of passage precisely because
the boundary arithmetic (`lo + (hi - lo) / 2`, `lo <= hi` vs `lo < hi`)
has consumed generations of programmers. The standard library versions
already survived that fight — prefer them.
"""

L_searching_VI = r"""
Tìm kiếm tuyến tính là `std::find` — O(n), chạy trên mọi thứ có phép so
sánh bằng. Tìm kiếm nhị phân thì khác: nó đòi hỏi **dữ liệu đã sắp** và
random access, và trả công bằng O(log n).

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v{1, 3, 5, 7, 9, 11};

bool has = std::binary_search(v.begin(), v.end(), 7);      // có/không

auto lb = std::lower_bound(v.begin(), v.end(), 7);  // đầu tiên >= 7
auto ub = std::upper_bound(v.begin(), v.end(), 7);  // đầu tiên > 7
```

`lower_bound`/`upper_bound` là lực lao động chính: `lower_bound` cho vị trí
đầu tiên có thể chèn giá trị mà vẫn giữ thứ tự; `upper_bound` cho vị trí
sau cùng. Khoảng cách giữa chúng là số phần tử bằng nhau. Trên
`std::map`/`std::set`, các member cùng tên làm điều này trong O(log n)
mà không cần iterator.

Bug kinh điển của người mới: tìm kiếm nhị phân trên dữ liệu *chưa sắp*.
Nó âm thầm trả câu sai — không exception, không cảnh báo. Sắp trước, hoặc
dùng cấu trúc tự giữ thứ tự.

Tự cài tìm kiếm nhị phân là nghi thức pass môn chính vì số học biên
(`lo + (hi - lo) / 2`, `lo <= hi` hay `lo < hi`) đã nuốt sống bao thế hệ
lập trình viên. Các phiên bản thư viện chuẩn đã sống sót qua trận đó —
hãy ưu tiên dùng chúng.
"""

# ---- lesson recursion-and-lists ----------------------------------------------------
L_recursion_EN = r"""
Recursion is a function calling itself on a smaller input. Every recursive
function needs a **base case** (when to stop) and a **recursive case**
(how to shrink). Missing or wrong base cases mean stack overflow.

```cpp
long long factorial(int n) {
    if (n <= 1) return 1;          // base case
    return n * factorial(n - 1);   // shrink toward the base
}
```

A linked list is the classic recursive structure: a node holds a value and
a pointer to the rest of the list.

```cpp
struct Node {
    int value;
    Node* next;
};

int length(const Node* head) {
    if (!head) return 0;                 // base: empty list
    return 1 + length(head->next);       // shrink: rest of the list
}
```

Manual list surgery — the operations the STL's `std::list` does for you:

```cpp
Node* push_front(Node* head, int v) {
    return new Node{v, head};            // caller owns the nodes
}

// reverse in place: three pointers, one pass
Node* reverse(Node* head) {
    Node* prev = nullptr;
    while (head) {
        Node* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}
```

Raw `new`/`delete` here is for *understanding* — production code wraps
nodes in `unique_ptr` (Module 8) or uses `std::forward_list`. Recursion
depth is also a memory decision: 10⁵ deep frames can overflow the stack
where an iterative loop would not.
"""

L_recursion_VI = r"""
Đệ quy là hàm tự gọi chính nó trên input nhỏ hơn. Mỗi hàm đệ quy cần một
**base case** (khi nào dừng) và một **recursive case** (cách thu nhỏ).
Thiếu hoặc sai base case nghĩa là tràn stack.

```cpp
long long factorial(int n) {
    if (n <= 1) return 1;          // base case
    return n * factorial(n - 1);   // thu nhỏ về phía base
}
```

Danh sách liên kết là cấu trúc đệ quy kinh điển: một node giữ giá trị và
một con trỏ tới phần còn lại của danh sách.

```cpp
struct Node {
    int value;
    Node* next;
};

int length(const Node* head) {
    if (!head) return 0;                 // base: danh sách rỗng
    return 1 + length(head->next);       // thu nhỏ: phần còn lại
}
```

Phẫu thuật danh sách thủ công — các thao tác mà `std::list` của STL làm
giúp bạn:

```cpp
Node* push_front(Node* head, int v) {
    return new Node{v, head};            // caller sở hữu các node
}

// đảo ngược tại chỗ: ba con trỏ, một lượt duyệt
Node* reverse(Node* head) {
    Node* prev = nullptr;
    while (head) {
        Node* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}
```

`new`/`delete` thủ công ở đây là để *hiểu* — code sản phẩm bọc node trong
`unique_ptr` (Module 8) hoặc dùng `std::forward_list`. Độ sâu đệ quy cũng
là quyết định bộ nhớ: 10⁵ khung hàm sâu có thể làm tràn stack trong khi
một vòng lặp không.
"""

# ---- lesson trees-and-graphs -------------------------------------------------------
L_trees_EN = r"""
A binary search tree keeps *sorted order alive through insertion*: left
subtree < node < right subtree. Lookup, insert, and erase are O(h) where h
is the tree height — O(log n) when the tree is balanced, O(n) when it
degenerates into a list.

```cpp
struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

bool contains(const TreeNode* n, int v) {
    if (!n) return false;
    if (v == n->value) return true;
    return v < n->value ? contains(n->left, v)
                        : contains(n->right, v);
}

TreeNode* insert(TreeNode* n, int v) {
    if (!n) return new TreeNode{v};
    if (v < n->value) n->left = insert(n->left, v);
    else if (v > n->value) n->right = insert(n->right, v);
    return n;   // duplicates are ignored
}
```

In-order traversal (left, node, right) visits a BST in sorted order —
the property that makes it a *sorted* container.

Graphs generalize: nodes + edges, no ordering promise. Breadth-first
search (BFS, queue) explores by distance; depth-first search (DFS, stack
or recursion) explores by depth. Their shapes in code:

```cpp
// BFS skeleton over an adjacency list
std::queue<int> q;
q.push(start);
visited[start] = true;
while (!q.empty()) {
    int cur = q.front(); q.pop();
    for (int next : adj[cur]) {
        if (!visited[next]) { visited[next] = true; q.push(next); }
    }
}
```

`std::map` is a balanced BST in disguise — after this lesson you know
what it is doing under its interface.
"""

L_trees_VI = r"""
Cây tìm kiếm nhị phân giữ *thứ tự sống sau mỗi lần chèn*: cây con trái <
node < cây con phải. Tra cứu, chèn và xoá là O(h) với h là chiều cao cây —
O(log n) khi cây cân bằng, O(n) khi nó thoái hóa thành danh sách.

```cpp
struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

bool contains(const TreeNode* n, int v) {
    if (!n) return false;
    if (v == n->value) return true;
    return v < n->value ? contains(n->left, v)
                        : contains(n->right, v);
}

TreeNode* insert(TreeNode* n, int v) {
    if (!n) return new TreeNode{v};
    if (v < n->value) n->left = insert(n->left, v);
    else if (v > n->value) n->right = insert(n->right, v);
    return n;   // phần tử trùng bị bỏ qua
}
```

Duyệt in-order (trái, node, phải) đi qua BST theo thứ tự tăng dần — tính
chất khiến nó là một container *có sắp*.

Đồ thị tổng quát hơn: node + cạnh, không hứa hẹn thứ tự. Tìm kiếm theo
chiều rộng (BFS, hàng đợi) khám phá theo khoảng cách; tìm kiếm theo chiều
sâu (DFS, stack hoặc đệ quy) khám phá theo độ sâu. Dáng vẻ trong code:

```cpp
// Khung BFS trên danh sách kề
std::queue<int> q;
q.push(start);
visited[start] = true;
while (!q.empty()) {
    int cur = q.front(); q.pop();
    for (int next : adj[cur]) {
        if (!visited[next]) { visited[next] = true; q.push(next); }
    }
}
```

`std::map` là một BST cân bằng trá hình — sau bài học này bạn biết nó đang
làm gì bên dưới interface.
"""

# ---- practice cppi-p11-algorithms --------------------------------------------------
R_BINARY_SEARCH = r'''#include <vector>

int binary_search_index(const std::vector<int>& v, int target) {
    int lo = 0, hi = static_cast<int>(v.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] == target) return mid;
        if (v[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
'''

W_BINARY_SEARCH = r'''#include <vector>

int binary_search_index(const std::vector<int>& v, int target) {
    int lo = 0, hi = static_cast<int>(v.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] == target) return mid;
        // BUG: both branches shrink the same way — target > mid is unreachable
        if (v[mid] < target) lo = mid + 1;
        else lo = mid - 1;
    }
    return -1;
}
'''

R_TWO_SUM = r'''#include <unordered_map>
#include <vector>

std::vector<int> two_sum(const std::vector<int>& nums, int target) {
    std::unordered_map<int, int> seen;   // value -> index
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
        auto it = seen.find(target - nums[i]);
        if (it != seen.end()) return {it->second, i};
        seen[nums[i]] = i;
    }
    return {};
}
'''

W_TWO_SUM = r'''#include <vector>

std::vector<int> two_sum(const std::vector<int>& nums, int target) {
    // BUG: returns the VALUES instead of their indices
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
        for (int j = i + 1; j < static_cast<int>(nums.size()); ++j) {
            if (nums[i] + nums[j] == target) return {nums[i], nums[j]};
        }
    }
    return {};
}
'''

# ---- practice cppi-p11-structures ------------------------------------------------------
R_REVERSE_LIST = r'''struct ListNode {
    int value;
    ListNode* next;
};

ListNode* reverse_list(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
        ListNode* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}
'''

W_REVERSE_LIST = r'''struct ListNode {
    int value;
    ListNode* next;
};

ListNode* reverse_list(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
        ListNode* next = head->next;
        head->next = prev;
        prev = head;
        // BUG: head never advances — infinite loop
    }
    return prev;
}
'''

R_ISLANDS = r'''#include <string>
#include <vector>

void sink(std::vector<std::string>& g, int r, int c) {
    if (r < 0 || r >= static_cast<int>(g.size())) return;
    if (c < 0 || c >= static_cast<int>(g[r].size())) return;
    if (g[r][c] != '1') return;
    g[r][c] = '0';
    sink(g, r + 1, c);
    sink(g, r - 1, c);
    sink(g, r, c + 1);
    sink(g, r, c - 1);
}

int count_islands(std::vector<std::string> grid) {
    int count = 0;
    for (int r = 0; r < static_cast<int>(grid.size()); ++r) {
        for (int c = 0; c < static_cast<int>(grid[r].size()); ++c) {
            if (grid[r][c] == '1') {
                ++count;
                sink(grid, r, c);
            }
        }
    }
    return count;
}
'''

W_ISLANDS = r'''#include <string>
#include <vector>

void sink(std::vector<std::string>& g, int r, int c) {
    if (r < 0 || r >= static_cast<int>(g.size())) return;
    if (c < 0 || c >= static_cast<int>(g[r].size())) return;
    if (g[r][c] != '1') return;
    g[r][c] = '0';
    sink(g, r + 1, c);
    sink(g, r - 1, c);
    sink(g, r, c + 1);
    sink(g, r, c - 1);
    // BUG: diagonal cells also connect — merges separate islands
    sink(g, r + 1, c + 1);
    sink(g, r - 1, c - 1);
    sink(g, r + 1, c - 1);
    sink(g, r - 1, c + 1);
}

int count_islands(std::vector<std::string> grid) {
    int count = 0;
    for (int r = 0; r < static_cast<int>(grid.size()); ++r) {
        for (int c = 0; c < static_cast<int>(grid[r].size()); ++c) {
            if (grid[r][c] == '1') {
                ++count;
                sink(grid, r, c);
            }
        }
    }
    return count;
}
'''

# ---- checkpoint: BST -------------------------------------------------------------------
R_BST = r'''struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

bool bst_contains(const TreeNode* n, int v) {
    if (!n) return false;
    if (v == n->value) return true;
    return v < n->value ? bst_contains(n->left, v)
                        : bst_contains(n->right, v);
}

TreeNode* bst_insert(TreeNode* n, int v) {
    if (!n) return new TreeNode{v, nullptr, nullptr};
    if (v < n->value) n->left = bst_insert(n->left, v);
    else if (v > n->value) n->right = bst_insert(n->right, v);
    return n;   // duplicates ignored
}
'''

W_BST = r'''struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

bool bst_contains(const TreeNode* n, int v) {
    if (!n) return false;
    if (v == n->value) return true;
    // BUG: branches inverted — smaller values searched on the right
    return v < n->value ? bst_contains(n->right, v)
                        : bst_contains(n->left, v);
}

TreeNode* bst_insert(TreeNode* n, int v) {
    if (!n) return new TreeNode{v, nullptr, nullptr};
    if (v < n->value) n->left = bst_insert(n->left, v);
    else if (v > n->value) n->right = bst_insert(n->right, v);
    return n;
}
'''

# ---- challenges ------------------------------------------------------------------------
CH_BINARY_SEARCH = challenge(
    "cppi-m11-binary-search",
    "Binary search: return the index",
    "Implement `int binary_search_index(const std::vector<int>& v, int target)` returning the index of `target` in the **sorted** vector, or -1 when absent. Use the classic two-pointer loop with `mid = lo + (hi - lo) / 2`.",
    r'''#include <vector>
#include <iostream>

// int binary_search_index(const std::vector<int>& v, int target)
''',
    [
        ("found", 'std::vector<int> v{1, 3, 5, 7, 9};\nCHECK_EQ(binary_search_index(v, 7), 3);\nCHECK_EQ(binary_search_index(v, 1), 0);\nCHECK_EQ(binary_search_index(v, 9), 4);', "First, middle, and last positions all work."),
        ("missing", 'std::vector<int> v{1, 3, 5};\nCHECK_EQ(binary_search_index(v, 4), -1);\nCHECK_EQ(binary_search_index(v, 0), -1);\nCHECK_EQ(binary_search_index(v, 10), -1);', "Below, between, and beyond — all absent."),
        ("empty", 'CHECK_EQ(binary_search_index({}, 5), -1);', "Empty input is absent, not a crash."),
        ("two-elements", 'std::vector<int> v{2, 4};\nCHECK_EQ(binary_search_index(v, 2), 0);\nCHECK_EQ(binary_search_index(v, 4), 1);', "The tiny case where boundary bugs live."),
    ],
    level="guided",
)

CH_TWO_SUM = challenge(
    "cppi-m11-two-sum",
    "Two-sum in one pass",
    "Implement `std::vector<int> two_sum(const std::vector<int>& nums, int target)` returning the indices `[i, j]` (i < j) of the two numbers adding to target, or an empty vector when no pair exists. The one-pass hash-map approach is O(n): before inserting nums[i], check whether `target - nums[i]` was already seen.",
    r'''#include <unordered_map>
#include <vector>
#include <iostream>

// std::vector<int> two_sum(const std::vector<int>& nums, int target)
''',
    [
        ("basic", 'auto r = two_sum({2, 7, 11, 15}, 9);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0], 0);\nCHECK_EQ(r[1], 1);', "2 + 7 = 9 at indices 0 and 1."),
        ("later-pair", 'auto r = two_sum({3, 2, 4}, 6);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0], 1);\nCHECK_EQ(r[1], 2);', "3 + 3 would reuse index 0 — the pair is 2 + 4."),
        ("none", 'CHECK(two_sum({1, 2, 3}, 100).empty());', "No pair: empty vector."),
        ("duplicates", 'auto r = two_sum({3, 3}, 6);\nCHECK_EQ(r.size(), 2);\nCHECK_EQ(r[0], 0);\nCHECK_EQ(r[1], 1);', "Two equal values still form a valid pair."),
    ],
    level="combination",
)

CH_REVERSE_LIST = challenge(
    "cppi-m11-reverse-list",
    "Reverse a linked list iteratively",
    "Implement `ListNode* reverse_list(ListNode* head)` reversing the chain in place with the three-pointer technique (prev, head, next) and returning the new head. `ListNode` is `{int value; ListNode* next;}`. No new nodes — relink the existing ones.",
    r'''#include <iostream>

struct ListNode {
    int value;
    ListNode* next;
};

// ListNode* reverse_list(ListNode* head)
''',
    [
        ("basic", 'ListNode c{3, nullptr};\nListNode b{2, &c};\nListNode a{1, &b};\nListNode* r = reverse_list(&a);\nCHECK_EQ(r->value, 3);\nCHECK_EQ(r->next->value, 2);\nCHECK_EQ(r->next->next->value, 1);\nCHECK_EQ(r->next->next->next, nullptr);', "1→2→3 becomes 3→2→1."),
        ("single", 'ListNode one{42, nullptr};\nCHECK_EQ(reverse_list(&one)->value, 42);', "A single node is its own reversed head."),
        ("empty", 'CHECK(reverse_list(nullptr) == nullptr);', "Empty list reverses to empty."),
    ],
    level="independent",
)

CH_COUNT_ISLANDS = challenge(
    "cppi-m11-count-islands",
    "Connected components (flood fill)",
    "Implement `int count_islands(const std::vector<std::string>& grid)` where '1' is land and '0' is water; an island is a maximal group of '1's connected horizontally or vertically. Sink each island as you find it (mutate the grid copy or use a visited matrix) and count the discoveries. This is DFS/BFS on a grid.",
    r'''#include <string>
#include <vector>
#include <iostream>

// int count_islands(const std::vector<std::string>& grid)
''',
    [
        ("one-island", 'std::vector<std::string> g{"110",\n                          "110",\n                          "000"};\nCHECK_EQ(count_islands(g), 1);', "All the 1s touch: one island."),
        ("three-islands", 'std::vector<std::string> g{"101",\n                          "010",\n                          "101"};\nCHECK_EQ(count_islands(g), 5);', "Diagonal does NOT connect: five separate islands."),
        ("all-water", 'std::vector<std::string> g{"000",\n                          "000"};\nCHECK_EQ(count_islands(g), 0);', "No land, no islands."),
        ("single-cell", 'std::vector<std::string> g{"1"};\nCHECK_EQ(count_islands(g), 1);', "One cell is one island."),
    ],
    level="real-world",
)

# ---- checkpoint -------------------------------------------------------------------------
CP_BST = challenge(
    "cppi-checkpoint-dsa",
    "Checkpoint: Binary search tree contains",
    "Implement `bool bst_contains(const TreeNode* n, int v)` on the given `TreeNode {int value; TreeNode* left; TreeNode* right;}` (left < node < right). Walk ONE path using the ordering — the recursive left-or-right branch, not both. Then implement `TreeNode* bst_insert(TreeNode* n, int v)` (ignore duplicates) so the second test can build a tree. Everything else is provided.",
    r'''#include <iostream>

struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

// bool bst_contains(const TreeNode* n, int v)
// TreeNode* bst_insert(TreeNode* n, int v)
''',
    [
        ("finds-deep", 'TreeNode a{1, nullptr, nullptr};\nTreeNode c{3, nullptr, nullptr};\nTreeNode b{2, &a, &c};\nCHECK(bst_contains(&b, 3));\nCHECK(bst_contains(&b, 1));\nCHECK(!bst_contains(&b, 4));', "Left leaf, right leaf, and a miss — one path each."),
        ("after-insert", 'TreeNode* root = nullptr;\nint values[] = {5, 3, 7, 6, 8};\nfor (int v : values) root = bst_insert(root, v);\nCHECK(bst_contains(root, 6));\nCHECK(!bst_contains(root, 4));', "Insert builds the BST; contains walks it."),
        ("duplicate-ignored", 'TreeNode* root = nullptr;\nroot = bst_insert(root, 5);\nroot = bst_insert(root, 5);\nCHECK(bst_contains(root, 5));', "Inserting twice changes nothing observable."),
    ],
    difficulty="intermediate",
)

VI_BINARY_SEARCH = vi_challenge(
    "Tìm kiếm nhị phân: trả về chỉ số",
    "Cài `int binary_search_index(const std::vector<int>& v, int target)` trả chỉ số của `target` trong vector **đã sắp**, hoặc -1 khi vắng mặt. Dùng vòng hai con trỏ kinh điển với `mid = lo + (hi - lo) / 2`.",
    [
        ("found", "Vị trí đầu, giữa, và cuối đều chạy đúng."),
        ("missing", "Dưới, giữa, và trên — đều vắng mặt."),
        ("empty", "Input rỗng là vắng mặt, không phải crash."),
        ("two-elements", "Trường hợp tí hon nơi bug biên sống."),
    ],
)

VI_TWO_SUM = vi_challenge(
    "Two-sum trong một lượt",
    "Cài `std::vector<int> two_sum(const std::vector<int>& nums, int target)` trả các chỉ số `[i, j]` (i < j) của hai số cộng bằng target, hoặc vector rỗng khi không có cặp nào. Cách hash-map một lượt là O(n): trước khi chèn nums[i], kiểm tra xem `target - nums[i]` đã thấy chưa.",
    [
        ("basic", "2 + 7 = 9 tại chỉ số 0 và 1."),
        ("later-pair", "3 + 3 sẽ tái sử dụng chỉ số 0 — cặp đúng là 2 + 4."),
        ("none", "Không có cặp: vector rỗng."),
        ("duplicates", "Hai giá trị bằng nhau vẫn lập thành cặp hợp lệ."),
    ],
)

VI_REVERSE_LIST = vi_challenge(
    "Đảo ngược danh sách liên kết theo vòng lặp",
    "Cài `ListNode* reverse_list(ListNode* head)` đảo chuỗi tại chỗ bằng kỹ thuật ba con trỏ (prev, head, next) và trả head mới. `ListNode` là `{int value; ListNode* next;}`. Không tạo node mới — nối lại các node sẵn có.",
    [
        ("basic", "1→2→3 trở thành 3→2→1."),
        ("single", "Một node tự là head sau khi đảo."),
        ("empty", "Danh sách rỗng đảo thành rỗng."),
    ],
)

VI_COUNT_ISLANDS = vi_challenge(
    "Thành phần liên thông (flood fill)",
    "Cài `int count_islands(const std::vector<std::string>& grid)` với '1' là đất và '0' là nước; một hòn đảo là nhóm '1' liên thông theo chiều ngang hoặc dọc. Chìm mỗi đảo khi tìm thấy (mutation bản sao grid hoặc dùng ma trận visited) và đếm số lần phát hiện. Đây là DFS/BFS trên lưới.",
    [
        ("one-island", "Mọi số 1 chạm nhau: một đảo."),
        ("three-islands", "Chéo KHÔNG nối: năm đảo riêng biệt."),
        ("all-water", "Không có đất, không có đảo."),
        ("single-cell", "Một ô là một đảo."),
    ],
)

VI_CP_BST = vi_challenge(
    "Kiểm tra điểm: BST contains",
    "Cài `bool bst_contains(const TreeNode* n, int v)` trên `TreeNode {int value; TreeNode* left; TreeNode* right;}` đã cho (trái < node < phải). Đi ĐÚNG MỘT đường dựa vào thứ tự — nhánh đệ quy trái-hoặc-phải, không phải cả hai. Sau đó cài `TreeNode* bst_insert(TreeNode* n, int v)` (bỏ qua trùng) để test thứ hai dựng cây. Còn lại đã cho sẵn.",
    [
        ("finds-deep", "Lá trái, lá phải, và một cú trượt — mỗi lần một đường."),
        ("after-insert", "Insert dựng BST; contains đi trên nó."),
        ("duplicate-ignored", "Chèn hai lần không đổi gì quan sát được."),
    ],
)

P1 = [CH_BINARY_SEARCH, CH_TWO_SUM]
VI_P1 = {"cppi-m11-binary-search": VI_BINARY_SEARCH, "cppi-m11-two-sum": VI_TWO_SUM}
P2 = [CH_REVERSE_LIST, CH_COUNT_ISLANDS]
VI_P2 = {"cppi-m11-reverse-list": VI_REVERSE_LIST, "cppi-m11-count-islands": VI_COUNT_ISLANDS}

# ---- emit --------------------------------------------------------------------------------
write_lesson(
    MOD, "complexity",
    "Complexity and Big-O",
    "Growth curves over machine speed: the complexity table, multiplication rules, and amortized vs average.",
    25, L_complexity_EN,
    "Độ phức tạp và Big-O",
    "Đường cong tăng trưởng hơn là tốc độ máy: bảng độ phức tạp, quy tắc nhân, và khấu hao khác trung bình.",
    L_complexity_VI,
)
write_lesson(
    MOD, "searching",
    "Searching: Linear and Binary",
    "std::find vs binary_search/lower_bound, the sorted-data requirement, and why hand-rolled binary search is a rite of passage.",
    25, L_searching_EN,
    "Tìm kiếm: tuyến tính và nhị phân",
    "std::find so với binary_search/lower_bound, yêu cầu dữ liệu đã sắp, và vì sao tự cài nhị phân là nghi thức pass môn.",
    L_searching_VI,
)
write_lesson(
    MOD, "recursion-and-lists",
    "Recursion and Linked Lists",
    "Base case discipline, list surgery with three pointers, and why production code reaches for unique_ptr or std::list instead.",
    30, L_recursion_EN,
    "Đệ quy và danh sách liên kết",
    "Kỷ luật base case, phẫu thuật danh sách với ba con trỏ, và vì sao code sản phẩm chọn unique_ptr hoặc std::list.",
    L_recursion_VI,
)
write_lesson(
    MOD, "trees-and-graphs",
    "Trees, BSTs, and Graph Traversal",
    "The BST invariant, in-order = sorted, BFS with a queue and DFS with a stack — and std::map as a balanced BST in disguise.",
    30, L_trees_EN,
    "Cây, BST, và duyệt đồ thị",
    "Bất biến BST, in-order = có thứ tự, BFS với hàng đợi và DFS với stack — và std::map là BST cân bằng trá hình.",
    L_trees_VI,
)

write_practice(
    MOD, "cppi-p11-algorithms",
    "Algorithm practice",
    "Hand-rolled binary search and the one-pass two-sum.",
    "Luyện thuật toán",
    "Tự cài tìm kiếm nhị phân và two-sum một lượt.",
    "searching", 35, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m11-binary-search", R_BINARY_SEARCH, W_BINARY_SEARCH),
        ("cppi-m11-two-sum", R_TWO_SUM, W_TWO_SUM),
    ],
)
write_practice(
    MOD, "cppi-p11-structures",
    "Structure practice",
    "Three-pointer list reversal and grid flood fill.",
    "Luyện cấu trúc",
    "Đảo danh sách ba con trỏ và flood fill trên lưới.",
    "trees-and-graphs", 35, "advanced", P2, VI_P2,
    solutions=[
        ("cppi-m11-reverse-list", R_REVERSE_LIST, W_REVERSE_LIST),
        ("cppi-m11-count-islands", R_ISLANDS, W_ISLANDS),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-dsa",
    "Checkpoint: Walk One Path",
    "BST contains and insert — the ordering discipline that separates O(log n) from O(n) without changing the answer.",
    35,
    r"""
`bst_contains` is the exam because the *wrong-looking* version passes the
eye test: searching both subtrees returns the same answers. It is just
O(n) instead of O(log n) — and on a degenerate tree, indistinguishable
from linear scan.

The discipline being tested:

- compare, then descend into exactly one subtree
- `!n` is the base case that means "absent", not an error
- `insert` mirrors the same walk and attaches at the null it reaches

This is the exact trade `std::map` makes for you: the balanced variant
keeps the tree height logarithmic so *every* lookup pays O(log n), never
O(n). After this module, you know what you are paying for.
""",
    "Kiểm tra điểm: Đi đúng một đường",
    "BST contains và insert — kỷ luật thứ tự tách O(log n) khỏi O(n) mà không đổi câu trả lời.",
    r"""
`bst_contains` là bài kiểm tra vì phiên bản *nhìn-sai* vẫn qua mắt: tìm cả
hai cây con trả cùng kết quả. Chỉ là O(n) thay vì O(log n) — và trên cây
thoái hóa, không phân biệt được với quét tuyến tính.

Kỷ luật được kiểm tra:

- so sánh, rồi đi xuống đúng một cây con
- `!n` là base case nghĩa là "vắng mặt", không phải lỗi
- `insert` đi đường tương tự và gắn vào null mà nó chạm tới

Đây chính là sự đánh đổi mà `std::map` làm giúp bạn: biến thể cân bằng giữ
chiều cao cây logarit để *mọi* tra cứu đều trả O(log n), không bao giờ
O(n). Sau module này, bạn biết mình đang trả tiền cho gì.
""",
    CP_BST, VI_CP_BST,
    solution=R_BST, wrong=W_BST,
)

write_module(
    MOD,
    "Data Structures and Algorithms",
    "The thinking layer: Big-O literacy, binary search, recursion and list surgery, BSTs and graph traversal.",
    "Cấu trúc dữ liệu và giải thuật",
    "Tầng tư duy: hiểu biết Big-O, tìm kiếm nhị phân, đệ quy và phẫu thuật danh sách, BST và duyệt đồ thị.",
    ["complexity", "searching", "recursion-and-lists", "trees-and-graphs", "advanced-checkpoint-dsa"],
    ["cppi-p11-algorithms", "cppi-p11-structures"],
)
print("module 11 emitted")
